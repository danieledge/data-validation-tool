# Data Validation Framework

A robust, production-grade CLI tool for validating data quality and completeness before data loads. Designed to handle large datasets (200GB+) with memory-efficient chunked processing.

## Features

- **Multiple Format Support**: CSV, Excel (.xlsx), Parquet
- **Large File Handling**: Optimized for 200GB+ datasets with chunked processing
- **22 Built-in Validation Types**:
  - File-level checks (empty files, row counts, file size)
  - Schema validation (column presence, data types)
  - Field-level checks (mandatory fields, regex patterns, valid values, ranges, date formats)
  - Record-level checks (duplicates, blank rows, uniqueness)
  - Advanced checks (statistical outliers, completeness, string length, precision)
  - Bespoke inline checks (custom regex, business rules, lookups)
- **Flexible Severity Levels**: ERROR vs WARNING with clear status reporting
- **Modern HTML Reports**:
  - Interactive dark-themed reports with data visualizations
  - Chart.js integration for validation insights
  - Collapsible sections and sample failures
  - Mobile-responsive design
- **Structured Logging**: Configurable log levels and file output for debugging
- **Comprehensive Test Suite**: 74 tests with 89% pass rate ensuring reliability
- **Extensible**: Easy to add custom validations via plugin architecture
- **CLI Interface**: Simple command-line usage with multiple options

## Installation

```bash
cd data-validation-tool
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Generate a Sample Configuration

```bash
data-validate init-config my_validation.yaml
```

### 2. Edit Configuration for Your Data

```yaml
validation_job:
  name: "Customer Data Validation"
  version: "1.0"

  files:
    - name: "customers"
      path: "data/customers.csv"
      format: "csv"

      validations:
        - type: "EmptyFileCheck"
          severity: "ERROR"

        - type: "MandatoryFieldCheck"
          severity: "ERROR"
          params:
            fields: ["customer_id", "email"]

        - type: "RegexCheck"
          severity: "ERROR"
          params:
            field: "email"
            pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

### 3. Run Validation

```bash
data-validate validate my_validation.yaml
```

### 4. View Reports

Open the generated `validation_report.html` in your browser for an interactive report.

## Available Validations

### File-Level Checks

| Validation | Description | Parameters |
|------------|-------------|------------|
| `EmptyFileCheck` | Checks file is not 0 bytes | None |
| `RowCountRangeCheck` | Validates row count range | `min_rows`, `max_rows` |
| `FileSizeCheck` | Validates file size limits | `min_size_mb`, `max_size_mb`, `max_size_gb` |

### Schema Checks

| Validation | Description | Parameters |
|------------|-------------|------------|
| `SchemaMatchCheck` | Validates column structure and types | `expected_schema`, `strict`, `check_order` |
| `ColumnPresenceCheck` | Checks required columns exist | `required_columns`, `case_sensitive` |

### Field-Level Checks

| Validation | Description | Parameters |
|------------|-------------|------------|
| `MandatoryFieldCheck` | Checks fields are not null/empty | `fields`, `allow_whitespace` |
| `RegexCheck` | Validates against regex pattern | `field`, `pattern`, `message`, `invert` |
| `ValidValuesCheck` | Checks values in allowed set | `field`, `valid_values`, `case_sensitive` |
| `RangeCheck` | Validates numeric ranges | `field`, `min_value`, `max_value` |
| `DateFormatCheck` | Validates date format | `field`, `format`, `allow_null` |

### Record-Level Checks

| Validation | Description | Parameters |
|------------|-------------|------------|
| `DuplicateRowCheck` | Detects duplicate rows | `key_fields` or `consider_all_fields` |
| `BlankRecordCheck` | Finds completely blank rows | `exclude_fields` |
| `UniqueKeyCheck` | Validates key uniqueness | `fields` |

## CLI Commands

### Validate Data

```bash
# Basic usage
data-validate validate config.yaml

# Custom output paths
data-validate validate config.yaml -o report.html -j results.json

# Fail on warnings
data-validate validate config.yaml --fail-on-warning

# Quiet mode
data-validate validate config.yaml --quiet
```

### List Available Validations

```bash
# All validations
data-validate list-validations

# Filter by category
data-validate list-validations --category field
```

### Initialize Config

```bash
data-validate init-config my_config.yaml
```

## Configuration Reference

### Complete Example

```yaml
validation_job:
  name: "Production Data Validation"
  version: "1.0"

  files:
    - name: "transactions"
      path: "/data/transactions.parquet"
      format: "parquet"

      validations:
        # File checks
        - type: "EmptyFileCheck"
          severity: "ERROR"

        - type: "RowCountRangeCheck"
          severity: "WARNING"
          params:
            min_rows: 1000
            max_rows: 10000000

        - type: "FileSizeCheck"
          severity: "WARNING"
          params:
            max_size_gb: 250

        # Schema
        - type: "SchemaMatchCheck"
          severity: "ERROR"
          params:
            expected_schema:
              transaction_id: "integer"
              account_number: "string"
              amount: "float"
              transaction_date: "date"
              status: "string"

        # Field validations
        - type: "MandatoryFieldCheck"
          severity: "ERROR"
          params:
            fields: ["transaction_id", "account_number", "amount"]

        - type: "RegexCheck"
          severity: "ERROR"
          params:
            field: "account_number"
            pattern: "^\\d{8}$"
            message: "Account number must be 8 digits"

        - type: "ValidValuesCheck"
          severity: "ERROR"
          params:
            field: "status"
            valid_values: ["COMPLETED", "PENDING", "FAILED"]

        - type: "RangeCheck"
          severity: "WARNING"
          params:
            field: "amount"
            min_value: 0
            max_value: 1000000

        - type: "DateFormatCheck"
          severity: "ERROR"
          params:
            field: "transaction_date"
            format: "%Y-%m-%d"

        # Record checks
        - type: "DuplicateRowCheck"
          severity: "ERROR"
          params:
            key_fields: ["transaction_id"]

        - type: "UniqueKeyCheck"
          severity: "ERROR"
          params:
            fields: ["transaction_id"]

  output:
    html_report: "validation_report.html"
    json_summary: "validation_summary.json"
    fail_on_error: true
    fail_on_warning: false

  processing:
    chunk_size: 50000        # Rows per chunk
    parallel_files: false    # Process files in parallel
    max_sample_failures: 100 # Max failures to show in report
```

## Custom Validations

Create custom validations by extending the `ValidationRule` base class:

```python
# validations/custom/bank_account_check.py
from validation_framework.validations.base import DataValidationRule, ValidationResult
import pandas as pd
from typing import Iterator, Dict, Any

class BankAccountCheck(DataValidationRule):
    """Validates 8-digit bank account numbers."""

    def get_description(self) -> str:
        return "Validates bank account numbers (8 digits)"

    def validate(self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]) -> ValidationResult:
        field = self.params.get("field")
        failed_rows = []
        total_rows = 0

        for chunk in data_iterator:
            for idx, value in chunk[field].items():
                if not self._is_valid_account(str(value)):
                    failed_rows.append({
                        "row": int(total_rows + idx),
                        "value": str(value),
                        "message": "Invalid bank account format"
                    })
                total_rows += len(chunk)

        return self._create_result(
            passed=len(failed_rows) == 0,
            message=f"Validated {total_rows} account numbers",
            failed_count=len(failed_rows),
            total_count=total_rows,
            sample_failures=failed_rows[:100]
        )

    def _is_valid_account(self, value: str) -> bool:
        return len(value) == 8 and value.isdigit()
```

Register your custom validation:

```python
from validation_framework.core.registry import register_validation
from validations.custom.bank_account_check import BankAccountCheck

register_validation("BankAccountCheck", BankAccountCheck)
```

## Performance Considerations

### Large Files (200GB+)

The framework is optimized for large files:

1. **Chunked Processing**: Files are read in chunks (default 50K rows)
2. **Memory Efficiency**: Only one chunk in memory at a time
3. **Parquet Format**: Use Parquet for best performance on large files
4. **Chunk Size**: Adjust `chunk_size` in config based on available memory

```yaml
processing:
  chunk_size: 100000  # Increase for more memory, better performance
```

### Optimization Tips

- **Use Parquet for 200GB+ files**: Faster than CSV, better compression
- **Adjust chunk size**: Balance between memory and performance
- **Limit sample failures**: Set `max_sample_failures` to avoid large reports
- **Run critical validations first**: Use `enabled: false` to skip non-essential checks

## Exit Codes

- `0`: Validation passed (or warnings only if not failing on warnings)
- `1`: Validation failed with errors
- `2`: Validation failed with warnings (when `--fail-on-warning` is set)

## Integration with Autopsy

The tool is designed to integrate with Autopsy or other orchestration systems:

```bash
# In your pipeline
data-validate validate config.yaml
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "Validation failed with code $EXIT_CODE"
  exit $EXIT_CODE
fi

# Proceed with data load
```

## Logging

The framework includes structured logging with configurable levels:

```bash
# Set log level
data-validate validate config.yaml --log-level DEBUG

# Write logs to file
data-validate validate config.yaml --log-file validation.log

# Both options
data-validate validate config.yaml --log-level INFO --log-file app.log
```

**Log Levels:**
- `DEBUG`: Detailed information for diagnosing problems
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failures

**Log Output Includes:**
- Timestamp
- Log level (with colors in console)
- Module name
- Function name and line number (in file logs)
- Message

## Development & Testing

### Running Tests

The framework includes a comprehensive test suite with 74 tests:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=validation_framework --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m slow          # Long-running tests

# Run tests in verbose mode
pytest -v

# Open coverage report
open htmlcov/index.html
```

### Test Categories

- **Unit Tests** (56 tests): Individual component testing
  - Registry pattern
  - Configuration parsing
  - Data loaders
  - Validation rules

- **Integration Tests** (6 tests): End-to-end workflows
  - Full validation pipelines
  - Report generation
  - Large dataset handling

### Code Quality

```bash
# Type checking with mypy
mypy validation_framework

# Code formatting with black
black validation_framework tests

# Import sorting with isort
isort validation_framework tests

# Linting with flake8
flake8 validation_framework
```

## License

MIT License

## Author

daniel edge
