"""
File-level validation rules.

These validations check file properties before data processing:
- File existence
- Empty file detection (0 bytes)
- Row count constraints
- File size limits
"""

from typing import Iterator, Dict, Any
import pandas as pd
from pathlib import Path
from validation_framework.validations.base import FileValidationRule, ValidationResult


class EmptyFileCheck(FileValidationRule):
    """
    Validates that a file is not empty (0 bytes).

    This is a critical check that should run before any data processing.
    An empty file often indicates an upstream failure in data generation.

    Configuration:
        severity: ERROR or WARNING (typically ERROR)

    Example YAML:
        - type: "EmptyFileCheck"
          severity: "ERROR"
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        return "Checks that the file is not empty (0 bytes)"

    def validate_file(self, context: Dict[str, Any]) -> ValidationResult:
        """
        Check if file is empty.

        Args:
            context: Must contain 'file_path' key

        Returns:
            ValidationResult with passed=True if file has content
        """
        try:
            file_path = context.get("file_path")
            if not file_path:
                return self._create_result(
                    passed=False,
                    message="File path not provided in context",
                    failed_count=1,
                )

            # Check file size
            file_size = Path(file_path).stat().st_size

            if file_size == 0:
                return self._create_result(
                    passed=False,
                    message=f"File is empty (0 bytes): {file_path}",
                    failed_count=1,
                )

            return self._create_result(
                passed=True,
                message=f"File contains data ({file_size} bytes)",
                total_count=1,
            )

        except FileNotFoundError:
            return self._create_result(
                passed=False,
                message=f"File not found: {file_path}",
                failed_count=1,
            )

        except Exception as e:
            return self._create_result(
                passed=False,
                message=f"Error checking file: {str(e)}",
                failed_count=1,
            )


class RowCountRangeCheck(FileValidationRule):
    """
    Validates that the total row count falls within specified range.

    Useful for detecting data loading issues where too few or too many
    rows might indicate a problem.

    Configuration:
        params:
            min_rows (int, optional): Minimum expected rows
            max_rows (int, optional): Maximum expected rows

    Example YAML:
        - type: "RowCountRangeCheck"
          severity: "WARNING"
          params:
            min_rows: 100
            max_rows: 1000000
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        min_rows = self.params.get("min_rows")
        max_rows = self.params.get("max_rows")

        if min_rows and max_rows:
            return f"Checks that row count is between {min_rows} and {max_rows}"
        elif min_rows:
            return f"Checks that row count is at least {min_rows}"
        elif max_rows:
            return f"Checks that row count is at most {max_rows}"
        else:
            return "Checks row count (no limits specified)"

    def validate_file(self, context: Dict[str, Any]) -> ValidationResult:
        """
        Check if row count is within specified range.

        Args:
            context: Must contain 'total_rows' or 'estimated_rows' key with row count

        Returns:
            ValidationResult indicating if row count is acceptable
        """
        try:
            # Get actual row count from context (populated by engine)
            # Try total_rows first (accurate), then estimated_rows (from metadata)
            actual_rows = context.get("total_rows") or context.get("estimated_rows", 0)

            min_rows = self.params.get("min_rows")
            max_rows = self.params.get("max_rows")

            # Check minimum
            if min_rows is not None and actual_rows < min_rows:
                return self._create_result(
                    passed=False,
                    message=f"Row count {actual_rows} is below minimum {min_rows}",
                    failed_count=1,
                    total_count=1,
                )

            # Check maximum
            if max_rows is not None and actual_rows > max_rows:
                return self._create_result(
                    passed=False,
                    message=f"Row count {actual_rows} exceeds maximum {max_rows}",
                    failed_count=1,
                    total_count=1,
                )

            return self._create_result(
                passed=True,
                message=f"Row count {actual_rows} is within acceptable range",
                total_count=1,
            )

        except Exception as e:
            return self._create_result(
                passed=False,
                message=f"Error checking row count: {str(e)}",
                failed_count=1,
            )


class FileSizeCheck(FileValidationRule):
    """
    Validates that file size is within acceptable limits.

    Useful for detecting unexpectedly large files that might cause
    processing issues or indicate data quality problems.

    Configuration:
        params:
            min_size_mb (float, optional): Minimum file size in MB
            max_size_mb (float, optional): Maximum file size in MB
            max_size_gb (float, optional): Maximum file size in GB (alternative)

    Example YAML:
        - type: "FileSizeCheck"
          severity: "WARNING"
          params:
            max_size_gb: 250
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        min_mb = self.params.get("min_size_mb")
        max_mb = self.params.get("max_size_mb")
        max_gb = self.params.get("max_size_gb")

        if max_gb:
            return f"Checks that file size does not exceed {max_gb} GB"
        elif min_mb and max_mb:
            return f"Checks that file size is between {min_mb} and {max_mb} MB"
        elif max_mb:
            return f"Checks that file size does not exceed {max_mb} MB"
        elif min_mb:
            return f"Checks that file size is at least {min_mb} MB"
        else:
            return "Checks file size (no limits specified)"

    def validate_file(self, context: Dict[str, Any]) -> ValidationResult:
        """
        Check if file size is within acceptable range.

        Args:
            context: Must contain 'file_path' key

        Returns:
            ValidationResult indicating if file size is acceptable
        """
        try:
            file_path = context.get("file_path")
            if not file_path:
                return self._create_result(
                    passed=False,
                    message="File path not provided in context",
                    failed_count=1,
                )

            # Get file size in bytes
            file_size_bytes = Path(file_path).stat().st_size
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_size_gb = file_size_bytes / (1024 * 1024 * 1024)

            # Check against limits
            min_mb = self.params.get("min_size_mb")
            max_mb = self.params.get("max_size_mb")
            max_gb = self.params.get("max_size_gb")

            # Convert GB to MB if specified
            if max_gb:
                max_mb = max_gb * 1024

            # Check minimum
            if min_mb is not None and file_size_mb < min_mb:
                return self._create_result(
                    passed=False,
                    message=f"File size {file_size_mb:.2f} MB is below minimum {min_mb} MB",
                    failed_count=1,
                )

            # Check maximum
            if max_mb is not None and file_size_mb > max_mb:
                return self._create_result(
                    passed=False,
                    message=f"File size {file_size_gb:.2f} GB exceeds maximum {max_mb/1024:.2f} GB",
                    failed_count=1,
                )

            return self._create_result(
                passed=True,
                message=f"File size {file_size_gb:.2f} GB is within acceptable range",
                total_count=1,
            )

        except FileNotFoundError:
            return self._create_result(
                passed=False,
                message=f"File not found: {file_path}",
                failed_count=1,
            )

        except Exception as e:
            return self._create_result(
                passed=False,
                message=f"Error checking file size: {str(e)}",
                failed_count=1,
            )
