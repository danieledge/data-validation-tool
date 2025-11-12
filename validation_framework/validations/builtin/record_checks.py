"""
Record-level validation rules.

These validations check entire rows/records:
- Duplicate detection
- Blank/empty record detection
- Uniqueness constraints
"""

from typing import Iterator, Dict, Any, List
import pandas as pd
from validation_framework.validations.base import DataValidationRule, ValidationResult


class DuplicateRowCheck(DataValidationRule):
    """
    Detects duplicate rows based on specified key fields.

    This is critical for ensuring data integrity, especially for
    transactional data where each record should be unique.

    Configuration:
        params:
            key_fields (list): List of fields that define uniqueness
            consider_all_fields (bool): If True, checks ALL columns (default: False)

    Example YAML:
        # Check for duplicate customer IDs
        - type: "DuplicateRowCheck"
          severity: "ERROR"
          params:
            key_fields: ["customer_id"]

        # Check for duplicate transactions
        - type: "DuplicateRowCheck"
          severity: "ERROR"
          params:
            key_fields: ["transaction_id", "date"]
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        if self.params.get("consider_all_fields", False):
            return "Checks for duplicate rows across all fields"
        else:
            key_fields = self.params.get("key_fields", [])
            return f"Checks for duplicates based on: {', '.join(key_fields)}"

    def validate(self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]) -> ValidationResult:
        """
        Check for duplicate rows across all chunks.

        Note: For very large files (200GB+), this loads key fields into memory
        to track duplicates. Memory usage = number_of_rows * key_field_size.

        Args:
            data_iterator: Iterator yielding data chunks
            context: Validation context

        Returns:
            ValidationResult with details of duplicate rows
        """
        try:
            consider_all = self.params.get("consider_all_fields", False)
            key_fields = self.params.get("key_fields", [])

            if not consider_all and not key_fields:
                return self._create_result(
                    passed=False,
                    message="No key fields specified for duplicate check",
                    failed_count=1,
                )

            total_rows = 0
            failed_rows = []
            max_samples = context.get("max_sample_failures", 100)

            # Track seen keys to detect duplicates across chunks
            seen_keys = set()
            duplicate_count = 0

            # Process each chunk
            for chunk_idx, chunk in enumerate(data_iterator):
                # Determine which columns to check
                if consider_all:
                    check_cols = list(chunk.columns)
                else:
                    # Verify key fields exist
                    missing_fields = [f for f in key_fields if f not in chunk.columns]
                    if missing_fields:
                        return self._create_result(
                            passed=False,
                            message=f"Key fields not found in data: {', '.join(missing_fields)}",
                            failed_count=1,
                        )
                    check_cols = key_fields

                # Create composite key for each row
                for idx in range(len(chunk)):
                    # Build tuple of key values
                    row_key = tuple(chunk.iloc[idx][check_cols])

                    # Check if we've seen this key before
                    if row_key in seen_keys:
                        duplicate_count += 1

                        # Collect sample
                        if len(failed_rows) < max_samples:
                            row_data = chunk.iloc[idx].to_dict()
                            failed_rows.append({
                                "row": int(total_rows + idx),
                                "key_values": {k: row_data[k] for k in check_cols},
                                "message": f"Duplicate row detected"
                            })
                    else:
                        seen_keys.add(row_key)

                total_rows += len(chunk)

            # Create result
            if duplicate_count > 0:
                unique_keys = len(seen_keys)
                return self._create_result(
                    passed=False,
                    message=f"Found {duplicate_count} duplicate rows ({unique_keys} unique records)",
                    failed_count=duplicate_count,
                    total_count=total_rows,
                    sample_failures=failed_rows,
                )

            return self._create_result(
                passed=True,
                message=f"No duplicates found among {total_rows} rows",
                total_count=total_rows,
            )

        except Exception as e:
            return self._create_result(
                passed=False,
                message=f"Error during duplicate check: {str(e)}",
                failed_count=1,
            )


class BlankRecordCheck(DataValidationRule):
    """
    Detects completely blank/empty rows.

    A row is considered blank if all fields are null or empty strings.

    Configuration:
        params:
            exclude_fields (list, optional): Fields to ignore when checking for blanks

    Example YAML:
        - type: "BlankRecordCheck"
          severity: "WARNING"
          params:
            exclude_fields: ["optional_notes"]
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        exclude = self.params.get("exclude_fields", [])
        if exclude:
            return f"Checks for blank rows (excluding fields: {', '.join(exclude)})"
        return "Checks for completely blank rows"

    def validate(self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]) -> ValidationResult:
        """
        Check for blank rows across all chunks.

        Args:
            data_iterator: Iterator yielding data chunks
            context: Validation context

        Returns:
            ValidationResult with details of blank rows found
        """
        try:
            exclude_fields = self.params.get("exclude_fields", [])

            total_rows = 0
            failed_rows = []
            max_samples = context.get("max_sample_failures", 100)

            # Process each chunk
            for chunk_idx, chunk in enumerate(data_iterator):
                # Determine which columns to check
                check_cols = [col for col in chunk.columns if col not in exclude_fields]

                if not check_cols:
                    return self._create_result(
                        passed=False,
                        message="No columns to check after exclusions",
                        failed_count=1,
                    )

                # Find rows where all checked columns are null or empty
                for idx in range(len(chunk)):
                    row = chunk.iloc[idx][check_cols]

                    # Check if all values are null or empty strings
                    is_blank = True
                    for value in row:
                        if pd.notna(value) and str(value).strip() != '':
                            is_blank = False
                            break

                    if is_blank and len(failed_rows) < max_samples:
                        failed_rows.append({
                            "row": int(total_rows + idx),
                            "message": "Completely blank row detected"
                        })

                total_rows += len(chunk)

            # Create result
            blank_count = len(failed_rows)

            if blank_count > 0:
                return self._create_result(
                    passed=False,
                    message=f"Found {blank_count} completely blank rows",
                    failed_count=blank_count,
                    total_count=total_rows,
                    sample_failures=failed_rows,
                )

            return self._create_result(
                passed=True,
                message=f"No blank rows found among {total_rows} rows",
                total_count=total_rows,
            )

        except Exception as e:
            return self._create_result(
                passed=False,
                message=f"Error during blank record check: {str(e)}",
                failed_count=1,
            )


class UniqueKeyCheck(DataValidationRule):
    """
    Validates that a field or combination of fields contains only unique values.

    Similar to DuplicateRowCheck but specifically for primary key validation.

    Configuration:
        params:
            fields (list): List of fields that should be unique

    Example YAML:
        - type: "UniqueKeyCheck"
          severity: "ERROR"
          params:
            fields: ["customer_id"]
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        fields = self.params.get("fields", [])
        return f"Checks uniqueness of: {', '.join(fields)}"

    def validate(self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]) -> ValidationResult:
        """
        Check uniqueness of specified fields.

        Args:
            data_iterator: Iterator yielding data chunks
            context: Validation context

        Returns:
            ValidationResult with details of duplicate keys
        """
        try:
            fields = self.params.get("fields", [])
            if not fields:
                return self._create_result(
                    passed=False,
                    message="No fields specified for uniqueness check",
                    failed_count=1,
                )

            total_rows = 0
            failed_rows = []
            max_samples = context.get("max_sample_failures", 100)

            # Track seen keys
            seen_keys = {}  # Maps key -> first row number where seen
            duplicate_count = 0

            # Process each chunk
            for chunk_idx, chunk in enumerate(data_iterator):
                # Verify fields exist
                missing_fields = [f for f in fields if f not in chunk.columns]
                if missing_fields:
                    return self._create_result(
                        passed=False,
                        message=f"Fields not found in data: {', '.join(missing_fields)}",
                        failed_count=1,
                    )

                # Check each row
                for idx in range(len(chunk)):
                    # Build composite key
                    if len(fields) == 1:
                        row_key = chunk.iloc[idx][fields[0]]
                    else:
                        row_key = tuple(chunk.iloc[idx][fields])

                    # Skip null keys
                    if pd.isna(row_key) or (isinstance(row_key, tuple) and any(pd.isna(v) for v in row_key)):
                        continue

                    # Check if seen before
                    if row_key in seen_keys:
                        duplicate_count += 1

                        if len(failed_rows) < max_samples:
                            key_dict = {k: chunk.iloc[idx][k] for k in fields}
                            failed_rows.append({
                                "row": int(total_rows + idx),
                                "key_values": key_dict,
                                "first_seen_row": seen_keys[row_key],
                                "message": f"Duplicate key found (first occurrence at row {seen_keys[row_key]})"
                            })
                    else:
                        seen_keys[row_key] = total_rows + idx

                total_rows += len(chunk)

            # Create result
            if duplicate_count > 0:
                return self._create_result(
                    passed=False,
                    message=f"Found {duplicate_count} duplicate keys (should be unique)",
                    failed_count=duplicate_count,
                    total_count=total_rows,
                    sample_failures=failed_rows,
                )

            return self._create_result(
                passed=True,
                message=f"All {len(seen_keys)} keys are unique across {total_rows} rows",
                total_count=total_rows,
            )

        except Exception as e:
            return self._create_result(
                passed=False,
                message=f"Error during unique key check: {str(e)}",
                failed_count=1,
            )
