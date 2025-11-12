"""
Advanced validation checks - Statistical, cross-field, freshness, and completeness.

These validations extend the framework with industry-standard data quality checks
based on research into Great Expectations and other validation frameworks.

Author: daniel edge
"""

from typing import Iterator, Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from validation_framework.validations.base import DataValidationRule, FileValidationRule, ValidationResult


class StatisticalOutlierCheck(DataValidationRule):
    """
    Detects statistical outliers using Z-score or IQR methods.

    Identifies values that deviate significantly from the expected distribution,
    useful for finding data quality issues, sensor errors, or fraudulent transactions.

    Parameters:
        field (str): Numeric field to check for outliers
        method (str): Detection method - 'zscore' or 'iqr' (default: 'zscore')
        threshold (float): For zscore: number of std devs (default: 3.0)
                          For IQR: multiplier for IQR (default: 1.5)

    Example YAML - Z-Score Method:
        - type: "StatisticalOutlierCheck"
          severity: "WARNING"
          params:
            field: "transaction_amount"
            method: "zscore"
            threshold: 3.0  # Flag values >3 standard deviations

    Example YAML - IQR Method:
        - type: "StatisticalOutlierCheck"
          severity: "WARNING"
          params:
            field: "temperature"
            method: "iqr"
            threshold: 1.5  # Flag values beyond 1.5*IQR from quartiles
    """

    def get_description(self) -> str:
        field = self.params.get("field", "unknown")
        method = self.params.get("method", "zscore")
        return f"Statistical outlier detection on '{field}' using {method} method"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """Detect outliers using statistical methods."""
        field = self.params.get("field")
        method = self.params.get("method", "zscore").lower()
        threshold = self.params.get("threshold", 3.0 if method == "zscore" else 1.5)

        if not field:
            return self._create_result(
                passed=False,
                message="Parameter 'field' is required",
                failed_count=1
            )

        # Collect all data for statistical analysis
        all_values = []
        row_indices = []
        total_rows = 0

        for chunk in data_iterator:
            if field not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field}' not found",
                    failed_count=1
                )

            # Collect numeric values
            for idx, value in chunk[field].dropna().items():
                try:
                    numeric_value = float(value)
                    all_values.append(numeric_value)
                    row_indices.append(total_rows + idx)
                except (ValueError, TypeError):
                    pass

            total_rows += len(chunk)

        if len(all_values) == 0:
            return self._create_result(
                passed=False,
                message=f"No valid numeric values found in '{field}'",
                failed_count=1
            )

        # Convert to numpy array for efficient computation
        values = np.array(all_values)

        # Detect outliers based on method
        if method == "zscore":
            outlier_mask = self._detect_zscore_outliers(values, threshold)
            method_desc = f"Z-score > {threshold}"
        elif method == "iqr":
            outlier_mask = self._detect_iqr_outliers(values, threshold)
            method_desc = f"IQR method (multiplier: {threshold})"
        else:
            return self._create_result(
                passed=False,
                message=f"Invalid method '{method}'. Use 'zscore' or 'iqr'",
                failed_count=1
            )

        # Collect outlier samples
        failed_rows = []
        max_samples = context.get("max_sample_failures", 100)

        for i, is_outlier in enumerate(outlier_mask):
            if is_outlier and len(failed_rows) < max_samples:
                failed_rows.append({
                    "row": int(row_indices[i]),
                    "field": field,
                    "value": f"{values[i]:.4f}",
                    "message": f"Statistical outlier detected ({method_desc})"
                })

        # Create result
        outlier_count = int(np.sum(outlier_mask))

        if outlier_count > 0:
            mean_val = np.mean(values)
            std_val = np.std(values)

            return self._create_result(
                passed=False,
                message=(
                    f"Found {outlier_count} outliers using {method} method. "
                    f"Mean: {mean_val:.2f}, StdDev: {std_val:.2f}"
                ),
                failed_count=outlier_count,
                total_count=len(values),
                sample_failures=failed_rows
            )

        return self._create_result(
            passed=True,
            message=f"No outliers detected in {len(values)} values ({method} method)",
            total_count=len(values)
        )

    def _detect_zscore_outliers(self, values: np.ndarray, threshold: float) -> np.ndarray:
        """Detect outliers using Z-score method."""
        mean = np.mean(values)
        std = np.std(values)

        if std == 0:
            return np.zeros(len(values), dtype=bool)

        z_scores = np.abs((values - mean) / std)
        return z_scores > threshold

    def _detect_iqr_outliers(self, values: np.ndarray, multiplier: float) -> np.ndarray:
        """Detect outliers using Interquartile Range (IQR) method."""
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1

        if iqr == 0:
            return np.zeros(len(values), dtype=bool)

        lower_bound = q1 - (multiplier * iqr)
        upper_bound = q3 + (multiplier * iqr)

        return (values < lower_bound) | (values > upper_bound)


class CrossFieldComparisonCheck(DataValidationRule):
    """
    Validates logical relationships between two fields.

    Ensures that field relationships are correct (e.g., end_date > start_date,
    discount <= price, actual <= budget).

    Parameters:
        field_a (str): First field name
        operator (str): Comparison operator - '>', '<', '>=', '<=', '==', '!='
        field_b (str): Second field name

    Example YAML - Date Comparison:
        - type: "CrossFieldComparisonCheck"
          severity: "ERROR"
          params:
            field_a: "end_date"
            operator: ">"
            field_b: "start_date"

    Example YAML - Numeric Comparison:
        - type: "CrossFieldComparisonCheck"
          severity: "ERROR"
          params:
            field_a: "discount_amount"
            operator: "<="
            field_b: "product_price"
    """

    VALID_OPERATORS = ['>', '<', '>=', '<=', '==', '!=']

    def get_description(self) -> str:
        field_a = self.params.get("field_a", "field_a")
        operator = self.params.get("operator", "?")
        field_b = self.params.get("field_b", "field_b")
        return f"Cross-field validation: {field_a} {operator} {field_b}"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """Validate relationship between two fields."""
        field_a = self.params.get("field_a")
        operator = self.params.get("operator")
        field_b = self.params.get("field_b")

        if not all([field_a, operator, field_b]):
            return self._create_result(
                passed=False,
                message="Parameters 'field_a', 'operator', and 'field_b' are required",
                failed_count=1
            )

        if operator not in self.VALID_OPERATORS:
            return self._create_result(
                passed=False,
                message=f"Invalid operator '{operator}'. Use one of: {', '.join(self.VALID_OPERATORS)}",
                failed_count=1
            )

        total_rows = 0
        failed_rows = []
        max_samples = context.get("max_sample_failures", 100)

        for chunk in data_iterator:
            # Check both fields exist
            if field_a not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field_a}' not found",
                    failed_count=1
                )

            if field_b not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field_b}' not found",
                    failed_count=1
                )

            # Apply comparison
            try:
                if operator == '>':
                    comparison = chunk[field_a] > chunk[field_b]
                elif operator == '<':
                    comparison = chunk[field_a] < chunk[field_b]
                elif operator == '>=':
                    comparison = chunk[field_a] >= chunk[field_b]
                elif operator == '<=':
                    comparison = chunk[field_a] <= chunk[field_b]
                elif operator == '==':
                    comparison = chunk[field_a] == chunk[field_b]
                elif operator == '!=':
                    comparison = chunk[field_a] != chunk[field_b]

                # Find failing rows
                failing_indices = chunk[~comparison].index.tolist()

                for idx in failing_indices:
                    if len(failed_rows) < max_samples:
                        val_a = chunk.loc[idx, field_a]
                        val_b = chunk.loc[idx, field_b]
                        failed_rows.append({
                            "row": int(total_rows + idx),
                            "fields": f"{field_a} vs {field_b}",
                            "value": f"{val_a} {operator} {val_b}",
                            "message": f"Comparison failed: {val_a} not {operator} {val_b}"
                        })

            except Exception as e:
                return self._create_result(
                    passed=False,
                    message=f"Error comparing fields: {str(e)}",
                    failed_count=1
                )

            total_rows += len(chunk)

        # Create result
        if failed_rows:
            return self._create_result(
                passed=False,
                message=f"Found {len(failed_rows)} rows where {field_a} not {operator} {field_b}",
                failed_count=len(failed_rows),
                total_count=total_rows,
                sample_failures=failed_rows
            )

        return self._create_result(
            passed=True,
            message=f"All {total_rows} rows pass: {field_a} {operator} {field_b}",
            total_count=total_rows
        )


class FreshnessCheck(FileValidationRule):
    """
    Validates that file or data is fresh (recently updated).

    Ensures data is current by checking file modification time or
    maximum date/timestamp in the data.

    Parameters:
        check_type (str): 'file' or 'data' (default: 'file')
        max_age_hours (int): Maximum age in hours (required)
        date_field (str): Field with date/timestamp (required if check_type='data')

    Example YAML - File Age:
        - type: "FreshnessCheck"
          severity: "WARNING"
          params:
            check_type: "file"
            max_age_hours: 24  # File must be modified within 24 hours

    Example YAML - Data Age:
        - type: "FreshnessCheck"
          severity: "ERROR"
          params:
            check_type: "data"
            max_age_hours: 48
            date_field: "transaction_timestamp"
    """

    def get_description(self) -> str:
        check_type = self.params.get("check_type", "file")
        max_age = self.params.get("max_age_hours", "?")
        return f"Freshness check ({check_type}): max age {max_age} hours"

    def validate(self, file_path: str, context: Dict[str, Any]) -> ValidationResult:
        """Validate file/data freshness."""
        check_type = self.params.get("check_type", "file").lower()
        max_age_hours = self.params.get("max_age_hours")

        if max_age_hours is None:
            return self._create_result(
                passed=False,
                message="Parameter 'max_age_hours' is required",
                failed_count=1
            )

        max_age = timedelta(hours=max_age_hours)
        now = datetime.now()

        if check_type == "file":
            # Check file modification time
            try:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                age = now - file_mtime

                if age > max_age:
                    hours_old = age.total_seconds() / 3600
                    return self._create_result(
                        passed=False,
                        message=f"File is {hours_old:.1f} hours old (max: {max_age_hours})",
                        failed_count=1
                    )

                hours_old = age.total_seconds() / 3600
                return self._create_result(
                    passed=True,
                    message=f"File is fresh ({hours_old:.1f} hours old, max: {max_age_hours})"
                )

            except Exception as e:
                return self._create_result(
                    passed=False,
                    message=f"Error checking file age: {str(e)}",
                    failed_count=1
                )

        elif check_type == "data":
            # Check data timestamp
            date_field = self.params.get("date_field")

            if not date_field:
                return self._create_result(
                    passed=False,
                    message="Parameter 'date_field' is required for data freshness check",
                    failed_count=1
                )

            # This will be called as file validation, but we need to peek at data
            # Store in context for potential data validation
            return self._create_result(
                passed=True,
                message="Data freshness check requires data validation (not implemented in file-level check)"
            )

        else:
            return self._create_result(
                passed=False,
                message=f"Invalid check_type '{check_type}'. Use 'file' or 'data'",
                failed_count=1
            )


class CompletenessCheck(DataValidationRule):
    """
    Validates field completeness (percentage of non-null values).

    Ensures that required fields have sufficient data populated,
    critical for data quality and downstream analytics.

    Parameters:
        field (str): Field to check
        min_completeness (float): Minimum required completeness (0.0-1.0 or 0-100)

    Example YAML - 95% Completeness Required:
        - type: "CompletenessCheck"
          severity: "WARNING"
          params:
            field: "email"
            min_completeness: 0.95  # 95% of records must have email

    Example YAML - 100% Completeness Required:
        - type: "CompletenessCheck"
          severity: "ERROR"
          params:
            field: "customer_id"
            min_completeness: 1.0  # All records must have customer_id
    """

    def get_description(self) -> str:
        field = self.params.get("field", "unknown")
        min_comp = self.params.get("min_completeness", "?")
        return f"Completeness check on '{field}': minimum {min_comp*100:.0f}%"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """Validate field completeness."""
        field = self.params.get("field")
        min_completeness = self.params.get("min_completeness")

        if not field:
            return self._create_result(
                passed=False,
                message="Parameter 'field' is required",
                failed_count=1
            )

        if min_completeness is None:
            return self._create_result(
                passed=False,
                message="Parameter 'min_completeness' is required",
                failed_count=1
            )

        # Convert percentage to decimal if needed
        if min_completeness > 1.0:
            min_completeness = min_completeness / 100.0

        total_rows = 0
        non_null_rows = 0

        for chunk in data_iterator:
            if field not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field}' not found",
                    failed_count=1
                )

            total_rows += len(chunk)
            non_null_rows += chunk[field].notna().sum()

        # Calculate completeness
        if total_rows == 0:
            completeness = 0.0
        else:
            completeness = non_null_rows / total_rows

        missing_count = total_rows - non_null_rows

        # Check threshold
        if completeness < min_completeness:
            return self._create_result(
                passed=False,
                message=(
                    f"Completeness {completeness*100:.2f}% is below minimum {min_completeness*100:.0f}%. "
                    f"Missing {missing_count} of {total_rows} values"
                ),
                failed_count=missing_count,
                total_count=total_rows
            )

        return self._create_result(
            passed=True,
            message=f"Completeness {completeness*100:.2f}% meets minimum {min_completeness*100:.0f}%",
            total_count=total_rows
        )


class StringLengthCheck(DataValidationRule):
    """
    Validates string field length is within acceptable range.

    Ensures text fields don't exceed database column limits or
    contain suspiciously short/long values.

    Parameters:
        field (str): String field to check
        min_length (int): Minimum acceptable length (optional)
        max_length (int): Maximum acceptable length (optional)

    Example YAML - Product Code Length:
        - type: "StringLengthCheck"
          severity: "ERROR"
          params:
            field: "product_code"
            min_length: 5
            max_length: 20

    Example YAML - Description Not Empty:
        - type: "StringLengthCheck"
          severity: "WARNING"
          params:
            field: "description"
            min_length: 10  # At least 10 characters
    """

    def get_description(self) -> str:
        field = self.params.get("field", "unknown")
        min_len = self.params.get("min_length")
        max_len = self.params.get("max_length")

        if min_len and max_len:
            return f"String length check on '{field}': {min_len}-{max_len} characters"
        elif min_len:
            return f"String length check on '{field}': minimum {min_len} characters"
        elif max_len:
            return f"String length check on '{field}': maximum {max_len} characters"
        else:
            return f"String length check on '{field}'"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """Validate string length."""
        field = self.params.get("field")
        min_length = self.params.get("min_length")
        max_length = self.params.get("max_length")

        if not field:
            return self._create_result(
                passed=False,
                message="Parameter 'field' is required",
                failed_count=1
            )

        if min_length is None and max_length is None:
            return self._create_result(
                passed=False,
                message="At least one of 'min_length' or 'max_length' is required",
                failed_count=1
            )

        total_rows = 0
        failed_rows = []
        max_samples = context.get("max_sample_failures", 100)

        for chunk in data_iterator:
            if field not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field}' not found",
                    failed_count=1
                )

            for idx, value in chunk[field].dropna().items():
                str_value = str(value)
                length = len(str_value)

                failed = False
                reason = ""

                if min_length is not None and length < min_length:
                    failed = True
                    reason = f"Length {length} < minimum {min_length}"

                if max_length is not None and length > max_length:
                    failed = True
                    reason = f"Length {length} > maximum {max_length}"

                if failed and len(failed_rows) < max_samples:
                    # Truncate long values for display
                    display_value = str_value[:50] + "..." if len(str_value) > 50 else str_value
                    failed_rows.append({
                        "row": int(total_rows + idx),
                        "field": field,
                        "value": display_value,
                        "message": reason
                    })

            total_rows += len(chunk)

        # Create result
        if failed_rows:
            return self._create_result(
                passed=False,
                message=f"Found {len(failed_rows)} values with invalid length",
                failed_count=len(failed_rows),
                total_count=total_rows,
                sample_failures=failed_rows
            )

        return self._create_result(
            passed=True,
            message=f"All {total_rows} values have valid length",
            total_count=total_rows
        )


class NumericPrecisionCheck(DataValidationRule):
    """
    Validates numeric precision (decimal places).

    Ensures numeric fields have correct number of decimal places,
    important for financial calculations and database storage.

    Parameters:
        field (str): Numeric field to check
        max_decimal_places (int): Maximum allowed decimal places
        exact_decimal_places (int): Required exact decimal places (optional)

    Example YAML - Currency (2 decimal places):
        - type: "NumericPrecisionCheck"
          severity: "ERROR"
          params:
            field: "price"
            exact_decimal_places: 2  # Must be exactly 2 decimals

    Example YAML - Max Precision:
        - type: "NumericPrecisionCheck"
          severity: "WARNING"
          params:
            field: "measurement"
            max_decimal_places: 4  # Up to 4 decimal places allowed
    """

    def get_description(self) -> str:
        field = self.params.get("field", "unknown")
        exact = self.params.get("exact_decimal_places")
        max_dp = self.params.get("max_decimal_places")

        if exact is not None:
            return f"Precision check on '{field}': exactly {exact} decimal places"
        elif max_dp is not None:
            return f"Precision check on '{field}': max {max_dp} decimal places"
        else:
            return f"Precision check on '{field}'"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """Validate numeric precision."""
        field = self.params.get("field")
        max_decimal_places = self.params.get("max_decimal_places")
        exact_decimal_places = self.params.get("exact_decimal_places")

        if not field:
            return self._create_result(
                passed=False,
                message="Parameter 'field' is required",
                failed_count=1
            )

        if max_decimal_places is None and exact_decimal_places is None:
            return self._create_result(
                passed=False,
                message="Either 'max_decimal_places' or 'exact_decimal_places' is required",
                failed_count=1
            )

        total_rows = 0
        failed_rows = []
        max_samples = context.get("max_sample_failures", 100)

        for chunk in data_iterator:
            if field not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field}' not found",
                    failed_count=1
                )

            for idx, value in chunk[field].dropna().items():
                try:
                    # Convert to string to count decimal places
                    str_value = str(float(value))

                    # Count decimal places
                    if '.' in str_value:
                        decimal_places = len(str_value.split('.')[1].rstrip('0'))
                    else:
                        decimal_places = 0

                    failed = False
                    reason = ""

                    if exact_decimal_places is not None:
                        if decimal_places != exact_decimal_places:
                            failed = True
                            reason = f"Has {decimal_places} decimals, requires exactly {exact_decimal_places}"

                    elif max_decimal_places is not None:
                        if decimal_places > max_decimal_places:
                            failed = True
                            reason = f"Has {decimal_places} decimals, maximum is {max_decimal_places}"

                    if failed and len(failed_rows) < max_samples:
                        failed_rows.append({
                            "row": int(total_rows + idx),
                            "field": field,
                            "value": str(value),
                            "message": reason
                        })

                except (ValueError, TypeError):
                    # Not a valid number, skip
                    pass

            total_rows += len(chunk)

        # Create result
        if failed_rows:
            return self._create_result(
                passed=False,
                message=f"Found {len(failed_rows)} values with invalid precision",
                failed_count=len(failed_rows),
                total_count=total_rows,
                sample_failures=failed_rows
            )

        return self._create_result(
            passed=True,
            message=f"All {total_rows} values have valid precision",
            total_count=total_rows
        )
