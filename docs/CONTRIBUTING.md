# Contributing Guide

Thank you for your interest in contributing to the Data Validation Tool! This guide will help you extend the framework with custom validations, loaders, and reporters.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Creating Custom Validations](#creating-custom-validations)
4. [Adding File Format Support](#adding-file-format-support)
5. [Creating Custom Reporters](#creating-custom-reporters)
6. [Code Style Guidelines](#code-style-guidelines)
7. [Testing](#testing)
8. [Documentation](#documentation)

---

## Getting Started

### Prerequisites

- Python 3.7+
- Git
- Basic understanding of pandas for data processing

### Project Structure

```
data-validation-tool/
├── validation_framework/       # Main package
│   ├── core/                  # Core engine and utilities
│   │   ├── engine.py          # Validation orchestrator
│   │   ├── config.py          # Configuration parser
│   │   ├── registry.py        # Validation registry
│   │   └── results.py         # Result data structures
│   ├── loaders/               # Data loaders
│   │   ├── base.py            # Base loader interface
│   │   ├── csv_loader.py      # CSV loader
│   │   ├── excel_loader.py    # Excel loader
│   │   ├── parquet_loader.py  # Parquet loader
│   │   └── factory.py         # Loader factory
│   ├── validations/           # Validation rules
│   │   ├── base.py            # Base validation classes
│   │   ├── builtin/           # Built-in validations
│   │   │   ├── file_checks.py
│   │   │   ├── schema_checks.py
│   │   │   ├── field_checks.py
│   │   │   ├── record_checks.py
│   │   │   ├── inline_checks.py
│   │   │   └── registry.py
│   │   └── custom/            # User custom validations
│   ├── reporters/             # Report generators
│   │   ├── base.py            # Base reporter interface
│   │   ├── html_reporter.py   # HTML reports
│   │   └── json_reporter.py   # JSON reports
│   └── cli.py                 # CLI interface
├── examples/                  # Example configurations
├── docs/                      # Documentation
└── tests/                     # Test suite
```

---

## Development Setup

### 1. Clone and Install

```bash
# Clone repository
git clone https://github.com/danieledge/data-validation-tool.git
cd data-validation-tool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black flake8
```

### 2. Verify Installation

```bash
# Run tests
pytest

# Check CLI works
data-validate --version

# List validations
data-validate list-validations
```

---

## Creating Custom Validations

### Step 1: Choose Validation Type

**File-Level Validation** - Checks file properties (size, existence, etc.)
- Runs before loading data
- Fast, no data processing
- Example: EmptyFileCheck, FileSizeCheck

**Data-Level Validation** - Checks actual data values
- Processes data in chunks
- For validating field values, records, etc.
- Example: RegexCheck, RangeCheck

### Step 2: Create Validation Class

Create a new file in `validation_framework/validations/custom/`:

**Example: IBAN Validation**

```python
# validation_framework/validations/custom/iban_check.py

from typing import Iterator, Dict, Any
import pandas as pd
import re
from validation_framework.validations.base import DataValidationRule
from validation_framework.core.results import ValidationResult


class IBANCheck(DataValidationRule):
    """
    Validates International Bank Account Numbers (IBAN).

    IBANs are standardized bank account identifiers used internationally.
    Format: CC99 XXXX XXXX XXXX (CC = country code, 99 = check digits)

    Parameters:
        field (str): Field containing IBAN values
        allowed_countries (list): List of allowed country codes (optional)

    Example YAML:
        - type: "IBANCheck"
          severity: "ERROR"
          params:
            field: "iban"
            allowed_countries: ["GB", "DE", "FR"]
    """

    # IBAN lengths by country
    IBAN_LENGTHS = {
        'GB': 22, 'DE': 22, 'FR': 27, 'ES': 24, 'IT': 27,
        'NL': 18, 'BE': 16, 'CH': 21, 'AT': 20, 'PT': 25
    }

    def get_description(self) -> str:
        """Return human-readable description."""
        field = self.params.get("field", "unknown")
        return f"IBAN validation for '{field}'"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """
        Validate IBAN format and check digits.

        Args:
            data_iterator: Iterator yielding DataFrame chunks
            context: Validation context (max_sample_failures, etc.)

        Returns:
            ValidationResult with pass/fail status and sample failures
        """
        field = self.params.get("field")
        allowed_countries = self.params.get("allowed_countries", [])

        if not field:
            return self._create_result(
                passed=False,
                message="Parameter 'field' is required",
                failed_count=1
            )

        total_rows = 0
        failed_rows = []
        max_samples = context.get("max_sample_failures", 100)

        # Process each chunk
        for chunk in data_iterator:
            # Check field exists
            if field not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field}' not found in data",
                    failed_count=1
                )

            # Validate each IBAN
            for idx, value in chunk[field].dropna().items():
                iban = str(value).replace(" ", "").upper()

                # Validate format
                is_valid, error_msg = self._validate_iban(iban, allowed_countries)

                if not is_valid:
                    if len(failed_rows) < max_samples:
                        failed_rows.append({
                            "row": int(total_rows + idx),
                            "field": field,
                            "value": str(value),
                            "message": error_msg
                        })

            total_rows += len(chunk)

        # Create result
        if failed_rows:
            return self._create_result(
                passed=False,
                message=f"Found {len(failed_rows)} invalid IBANs",
                failed_count=len(failed_rows),
                total_count=total_rows,
                sample_failures=failed_rows
            )

        return self._create_result(
            passed=True,
            message=f"All {total_rows} IBANs are valid",
            total_count=total_rows
        )

    def _validate_iban(self, iban: str, allowed_countries: list) -> tuple:
        """
        Validate IBAN format and check digits.

        Args:
            iban: IBAN string (without spaces)
            allowed_countries: List of allowed country codes

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check minimum length
        if len(iban) < 15:
            return False, "IBAN too short (minimum 15 characters)"

        # Extract country code
        country = iban[:2]

        # Check country code is letters
        if not country.isalpha():
            return False, f"Invalid country code '{country}'"

        # Check if country is allowed
        if allowed_countries and country not in allowed_countries:
            return False, f"Country code '{country}' not in allowed list"

        # Check country-specific length
        if country in self.IBAN_LENGTHS:
            expected_length = self.IBAN_LENGTHS[country]
            if len(iban) != expected_length:
                return False, f"Invalid length for {country} IBAN (expected {expected_length})"

        # Validate check digits
        check_digits = iban[2:4]
        if not check_digits.isdigit():
            return False, f"Invalid check digits '{check_digits}'"

        # Perform mod-97 check digit validation
        # Move first 4 chars to end and convert to numbers
        rearranged = iban[4:] + iban[:4]

        # Convert letters to numbers (A=10, B=11, ..., Z=35)
        numeric = ""
        for char in rearranged:
            if char.isdigit():
                numeric += char
            else:
                numeric += str(ord(char) - ord('A') + 10)

        # Check if mod 97 equals 1
        if int(numeric) % 97 != 1:
            return False, "Invalid IBAN check digits"

        return True, ""
```

### Step 3: Register the Validation

Create or update `validation_framework/validations/custom/__init__.py`:

```python
# validation_framework/validations/custom/__init__.py

from validation_framework.core.registry import register_validation
from .iban_check import IBANCheck

# Register validation so it can be used in YAML
register_validation("IBANCheck", IBANCheck)

# Make it importable
__all__ = ['IBANCheck']
```

### Step 4: Use in Configuration

```yaml
# config.yaml
validation_job:
  name: "IBAN Validation Example"

  files:
    - name: "bank_accounts"
      path: "data/accounts.csv"
      format: "csv"

      validations:
        - type: "IBANCheck"
          severity: "ERROR"
          params:
            field: "iban"
            allowed_countries: ["GB", "DE", "FR"]
```

### Step 5: Test Your Validation

```python
# tests/test_iban_check.py

import pytest
import pandas as pd
from validation_framework.validations.custom.iban_check import IBANCheck
from validation_framework.core.results import Severity

def test_iban_valid():
    """Test with valid IBANs."""
    validation = IBANCheck(severity=Severity.ERROR, params={"field": "iban"})

    # Create test data
    data = pd.DataFrame({
        "iban": [
            "GB82 WEST 1234 5698 7654 32",  # Valid UK IBAN
            "DE89 3704 0044 0532 0130 00"   # Valid DE IBAN
        ]
    })

    # Run validation
    result = validation.validate(iter([data]), {})

    # Assert passed
    assert result.passed
    assert result.failed_count == 0

def test_iban_invalid():
    """Test with invalid IBANs."""
    validation = IBANCheck(severity=Severity.ERROR, params={"field": "iban"})

    # Create test data with invalid IBANs
    data = pd.DataFrame({
        "iban": [
            "GB00 INVALID",           # Invalid format
            "XX89 3704 0044 0532 01"  # Invalid country
        ]
    })

    # Run validation
    result = validation.validate(iter([data]), {})

    # Assert failed
    assert not result.passed
    assert result.failed_count == 2

def test_iban_country_filter():
    """Test country filtering."""
    validation = IBANCheck(
        severity=Severity.ERROR,
        params={
            "field": "iban",
            "allowed_countries": ["GB"]  # Only allow UK
        }
    )

    data = pd.DataFrame({
        "iban": [
            "GB82 WEST 1234 5698 7654 32",  # Valid UK - should pass
            "DE89 3704 0044 0532 0130 00"   # Valid DE - should fail (not allowed)
        ]
    })

    result = validation.validate(iter([data]), {})

    # Should fail because DE not in allowed list
    assert not result.passed
    assert result.failed_count == 1
```

---

## Adding File Format Support

### Step 1: Create Loader Class

Create a new loader in `validation_framework/loaders/`:

**Example: XML Loader**

```python
# validation_framework/loaders/xml_loader.py

from typing import Iterator
import pandas as pd
import xml.etree.ElementTree as ET
from validation_framework.loaders.base import DataLoader, FileMetadata


class XMLLoader(DataLoader):
    """
    Loads data from XML files.

    Parameters:
        file_path (str): Path to XML file
        chunk_size (int): Number of records per chunk
        record_tag (str): XML tag for each record
    """

    def __init__(self, file_path: str, chunk_size: int = 50000,
                 record_tag: str = "record", **kwargs):
        """Initialize XML loader."""
        super().__init__(file_path, chunk_size, **kwargs)
        self.record_tag = record_tag

    def load(self) -> Iterator[pd.DataFrame]:
        """
        Load XML data in chunks.

        Yields:
            DataFrame chunks
        """
        records = []

        # Parse XML incrementally
        for event, elem in ET.iterparse(self.file_path, events=('end',)):
            if elem.tag == self.record_tag:
                # Convert XML element to dict
                record = self._element_to_dict(elem)
                records.append(record)

                # Clear element to save memory
                elem.clear()

                # Yield chunk when full
                if len(records) >= self.chunk_size:
                    yield pd.DataFrame(records)
                    records = []

        # Yield remaining records
        if records:
            yield pd.DataFrame(records)

    def get_metadata(self) -> FileMetadata:
        """
        Get file metadata.

        Returns:
            FileMetadata object
        """
        import os

        file_size = os.path.getsize(self.file_path)

        # Quick scan for record count (expensive for large files)
        # For production, consider caching or estimating
        record_count = 0
        for event, elem in ET.iterparse(self.file_path, events=('end',)):
            if elem.tag == self.record_tag:
                record_count += 1
                elem.clear()

        # Get column names from first record
        for event, elem in ET.iterparse(self.file_path, events=('end',)):
            if elem.tag == self.record_tag:
                columns = list(self._element_to_dict(elem).keys())
                elem.clear()
                break
        else:
            columns = []

        return FileMetadata(
            file_size_mb=file_size / (1024 * 1024),
            total_rows=record_count,
            column_count=len(columns),
            column_names=columns
        )

    def _element_to_dict(self, element: ET.Element) -> dict:
        """Convert XML element to dictionary."""
        return {child.tag: child.text for child in element}
```

### Step 2: Register in Factory

Update `validation_framework/loaders/factory.py`:

```python
from validation_framework.loaders.xml_loader import XMLLoader

class LoaderFactory:
    @classmethod
    def create_loader(cls, file_path: str, file_format: str = None,
                      chunk_size: int = 50000, **kwargs) -> DataLoader:
        """Create appropriate loader based on format."""

        # ... existing code ...

        elif file_format.lower() == "xml":
            return XMLLoader(file_path, chunk_size, **kwargs)

        else:
            raise ValueError(f"Unsupported file format: {file_format}")
```

### Step 3: Use in Configuration

```yaml
files:
  - name: "xml_data"
    path: "data/records.xml"
    format: "xml"
    params:
      record_tag: "customer"  # XML tag for each record
```

---

## Creating Custom Reporters

### Step 1: Create Reporter Class

Create a new reporter in `validation_framework/reporters/`:

**Example: Markdown Reporter**

```python
# validation_framework/reporters/markdown_reporter.py

from validation_framework.reporters.base import Reporter
from validation_framework.core.results import ValidationReport, Status


class MarkdownReporter(Reporter):
    """
    Generate Markdown format validation reports.

    Perfect for including in README files or documentation.
    """

    def generate(self, report: ValidationReport, output_path: str):
        """
        Generate Markdown report.

        Args:
            report: ValidationReport with results
            output_path: Path to output .md file
        """
        lines = []

        # Header
        lines.append(f"# {report.job_name}")
        lines.append("")
        lines.append(f"**Execution Time:** {report.execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Duration:** {report.duration_seconds:.2f}s")
        lines.append("")

        # Overall Status
        status_emoji = "✅" if report.overall_status == Status.PASSED else "❌"
        lines.append(f"## Overall Status: {status_emoji} {report.overall_status.value}")
        lines.append("")

        # Summary Table
        lines.append("| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Validations | {sum(f.total_validations for f in report.file_reports)} |")
        lines.append(f"| Errors | {report.total_errors} |")
        lines.append(f"| Warnings | {report.total_warnings} |")
        lines.append(f"| Files | {len(report.file_reports)} |")
        lines.append("")

        # File Results
        lines.append("## File Results")
        lines.append("")

        for file_report in report.file_reports:
            status_emoji = "✅" if file_report.status == Status.PASSED else "❌"
            lines.append(f"### {status_emoji} {file_report.file_name}")
            lines.append("")
            lines.append(f"**Path:** `{file_report.file_path}`")
            lines.append(f"**Status:** {file_report.status.value}")
            lines.append(f"**Errors:** {file_report.error_count}")
            lines.append(f"**Warnings:** {file_report.warning_count}")
            lines.append("")

            # Validation Results
            lines.append("| Validation | Severity | Status | Message |")
            lines.append("|------------|----------|--------|---------|")

            for result in file_report.validation_results:
                status_emoji = "✅" if result.passed else "❌"
                lines.append(
                    f"| {result.rule_name} | "
                    f"{result.severity.value} | "
                    f"{status_emoji} | "
                    f"{result.message} |"
                )

            lines.append("")

        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"Markdown report generated: {output_path}")
```

### Step 2: Use the Reporter

```python
from validation_framework.reporters.markdown_reporter import MarkdownReporter

# After running validation
md_reporter = MarkdownReporter()
md_reporter.generate(report, "validation_report.md")
```

---

## Code Style Guidelines

### Python Style

Follow PEP 8 with these conventions:

```python
# Imports
from typing import Iterator, Dict, Any  # Type hints first
import pandas as pd                     # Standard library
import re                               # Third-party
from validation_framework...            # Local imports

# Docstrings - Google style
def my_function(param1: str, param2: int) -> bool:
    """
    One-line summary.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is invalid
    """
    pass

# Comments
# Explain WHY, not WHAT
# Code should be self-documenting for WHAT

# Naming
class MyValidation:         # PascalCase for classes
    def my_method(self):     # snake_case for functions/methods
        my_variable = 5      # snake_case for variables
        MAX_SIZE = 1000      # UPPERCASE for constants
```

### Format Code

Use `black` for automatic formatting:

```bash
# Format all files
black validation_framework/

# Check without modifying
black --check validation_framework/
```

### Linting

Use `flake8` for style checking:

```bash
# Check code
flake8 validation_framework/

# Ignore specific rules in .flake8 file
```

---

## Testing

### Writing Tests

Create tests in `tests/` directory:

```python
# tests/test_my_validation.py

import pytest
import pandas as pd
from validation_framework.validations.custom.my_validation import MyValidation
from validation_framework.core.results import Severity

class TestMyValidation:
    """Test suite for MyValidation."""

    def test_valid_data(self):
        """Test with valid data - should pass."""
        validation = MyValidation(
            severity=Severity.ERROR,
            params={"field": "test_field"}
        )

        data = pd.DataFrame({"test_field": ["valid1", "valid2"]})
        result = validation.validate(iter([data]), {})

        assert result.passed
        assert result.failed_count == 0

    def test_invalid_data(self):
        """Test with invalid data - should fail."""
        validation = MyValidation(
            severity=Severity.ERROR,
            params={"field": "test_field"}
        )

        data = pd.DataFrame({"test_field": ["invalid1", "invalid2"]})
        result = validation.validate(iter([data]), {})

        assert not result.passed
        assert result.failed_count == 2

    def test_missing_field(self):
        """Test with missing field - should fail."""
        validation = MyValidation(
            severity=Severity.ERROR,
            params={"field": "missing_field"}
        )

        data = pd.DataFrame({"other_field": ["value"]})
        result = validation.validate(iter([data]), {})

        assert not result.passed
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_my_validation.py

# Run with coverage
pytest --cov=validation_framework --cov-report=html

# Run specific test
pytest tests/test_my_validation.py::TestMyValidation::test_valid_data
```

---

## Documentation

### Docstring Standards

All public classes, methods, and functions must have docstrings:

```python
class MyValidation(DataValidationRule):
    """
    One-line summary of what this validation does.

    More detailed explanation of the validation logic,
    when to use it, and any important notes.

    Parameters:
        field (str): Field to validate
        threshold (int): Threshold value for validation

    Example YAML:
        - type: "MyValidation"
          severity: "ERROR"
          params:
            field: "amount"
            threshold: 1000

    Example:
        >>> validation = MyValidation(Severity.ERROR, {"field": "amount"})
        >>> result = validation.validate(data_iterator, context)
    """
```

### Update Documentation

When adding features, update relevant docs:

- `docs/VALIDATION_REFERENCE.md` - For new validations
- `docs/TECHNICAL_GUIDE.md` - For advanced usage
- `docs/ARCHITECTURE.md` - For architectural changes
- `examples/` - Add example configurations

---

## Submission Guidelines

### Before Submitting

1. **Test your code**
   ```bash
   pytest
   ```

2. **Format code**
   ```bash
   black validation_framework/
   ```

3. **Check style**
   ```bash
   flake8 validation_framework/
   ```

4. **Update documentation**

5. **Add examples**

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-validation

# Make changes and commit
git add .
git commit -m "Add IBAN validation check"

# Push branch
git push origin feature/my-validation

# Create pull request on GitHub
```

### Commit Messages

Use clear, descriptive commit messages:

```
Add IBAN validation check

- Implements IBANCheck validation class
- Supports country-specific validation
- Includes mod-97 check digit verification
- Adds comprehensive tests
- Updates documentation
```

---

## Need Help?

- **Questions**: Open a [GitHub Discussion](https://github.com/danieledge/data-validation-tool/discussions)
- **Bugs**: File a [GitHub Issue](https://github.com/danieledge/data-validation-tool/issues)
- **Documentation**: Read the [Technical Guide](TECHNICAL_GUIDE.md)

---

**Thank you for contributing! 🎯**
