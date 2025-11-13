# Developer Guide

**Extending the Data Validation Framework**

This guide shows developers how to extend the framework with custom validations, loaders, and reporters.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Creating Custom Validations](#creating-custom-validations)
3. [Creating Custom Loaders](#creating-custom-loaders)
4. [Creating Custom Reporters](#creating-custom-reporters)
5. [Testing Custom Components](#testing-custom-components)
6. [Contributing Guidelines](#contributing-guidelines)
7. [API Reference](#api-reference)

---

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Clone and Setup

```bash
# Clone repository
git clone https://github.com/danieledge/data-validation-tool.git
cd data-validation-tool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Development Dependencies

```txt
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=3.0.0
pytest-mock>=3.6.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.950
```

### Project Structure

```
data-validation-tool/
├── validation_framework/     # Main package
│   ├── core/                 # Core components
│   ├── loaders/              # Data loaders
│   ├── validations/          # Validation rules
│   │   ├── builtin/          # Built-in validations
│   │   └── custom/           # Custom validations go here
│   └── reporters/            # Report generators
├── tests/                    # Test suite
├── docs/                     # Documentation
└── examples/                 # Example configurations
```

---

## Creating Custom Validations

### Step 1: Create Validation Class

Create a new file in `validation_framework/validations/custom/`:

```python
"""
Custom validation for business-specific logic.

File: validation_framework/validations/custom/my_validation.py
"""
from typing import Iterator, Dict, Any
import pandas as pd
from validation_framework.validations.base import DataValidationRule, ValidationResult
import logging

logger = logging.getLogger(__name__)


class MyCustomValidation(DataValidationRule):
    """
    Custom validation with specific business logic.

    Configuration:
        params:
            threshold (float): Custom threshold value
            check_field (str): Field to check
            comparison (str): Comparison operator ("gt", "lt", "eq")

    Example YAML:
        - type: "MyCustomValidation"
          severity: "ERROR"
          params:
            check_field: "revenue"
            threshold: 1000000
            comparison: "gt"
          condition: "customer_tier == 'PLATINUM'"
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        field = self.params.get("check_field", "unknown")
        threshold = self.params.get("threshold", 0)
        comparison = self.params.get("comparison", "gt")

        ops = {"gt": ">", "lt": "<", "eq": "==", "gte": ">=", "lte": "<="}
        op_symbol = ops.get(comparison, "?")

        return f"Checks '{field}' {op_symbol} {threshold}"

    def validate(
        self,
        data_iterator: Iterator[pd.DataFrame],
        context: Dict[str, Any]
    ) -> ValidationResult:
        """
        Execute custom validation logic.

        Args:
            data_iterator: Iterator yielding DataFrame chunks
            context: Validation context with file info and settings

        Returns:
            ValidationResult with pass/fail status and details
        """
        try:
            # Extract parameters
            check_field = self.params.get("check_field")
            threshold = self.params.get("threshold", 0.0)
            comparison = self.params.get("comparison", "gt")

            # Validate parameters
            if not check_field:
                return self._create_result(
                    passed=False,
                    message="Missing required parameter 'check_field'",
                    failed_count=1,
                )

            # Initialize tracking variables
            total_rows = 0
            failed_rows = []
            max_samples = context.get("max_sample_failures", 100)

            # Process each chunk
            for chunk_idx, chunk in enumerate(data_iterator):
                logger.debug(f"Processing chunk {chunk_idx}, size: {len(chunk)}")

                # Verify field exists
                if check_field not in chunk.columns:
                    return self._create_result(
                        passed=False,
                        message=f"Field '{check_field}' not found in data",
                        failed_count=1,
                    )

                # Apply conditional filter if specified
                if self.condition:
                    condition_mask = self._evaluate_condition(chunk)
                    rows_to_check = chunk[condition_mask]

                    # If no rows match condition in this chunk, skip
                    if len(rows_to_check) == 0:
                        total_rows += len(chunk)
                        continue
                else:
                    rows_to_check = chunk

                # Apply custom validation logic
                for idx, value in rows_to_check[check_field].items():
                    # Skip null values
                    if pd.isna(value):
                        continue

                    # Convert to numeric
                    try:
                        numeric_value = float(value)
                    except (ValueError, TypeError):
                        if len(failed_rows) < max_samples:
                            failed_rows.append({
                                "row": int(total_rows + idx),
                                "field": check_field,
                                "value": str(value),
                                "message": f"Non-numeric value: {value}"
                            })
                        continue

                    # Apply comparison
                    failed = False
                    if comparison == "gt" and not (numeric_value > threshold):
                        failed = True
                        message = f"Value {numeric_value} not > {threshold}"
                    elif comparison == "lt" and not (numeric_value < threshold):
                        failed = True
                        message = f"Value {numeric_value} not < {threshold}"
                    elif comparison == "eq" and not (numeric_value == threshold):
                        failed = True
                        message = f"Value {numeric_value} not == {threshold}"
                    elif comparison == "gte" and not (numeric_value >= threshold):
                        failed = True
                        message = f"Value {numeric_value} not >= {threshold}"
                    elif comparison == "lte" and not (numeric_value <= threshold):
                        failed = True
                        message = f"Value {numeric_value} not <= {threshold}"

                    if failed and len(failed_rows) < max_samples:
                        failed_rows.append({
                            "row": int(total_rows + idx),
                            "field": check_field,
                            "value": float(numeric_value),
                            "message": message
                        })

                total_rows += len(chunk)

            # Create result
            failed_count = len(failed_rows)

            if failed_count > 0:
                return self._create_result(
                    passed=False,
                    message=f"Found {failed_count} rows that don't meet threshold criteria",
                    failed_count=failed_count,
                    total_count=total_rows,
                    sample_failures=failed_rows,
                )

            return self._create_result(
                passed=True,
                message=f"All {total_rows} rows passed custom validation",
                total_count=total_rows,
            )

        except Exception as e:
            logger.exception("Error in MyCustomValidation")
            return self._create_result(
                passed=False,
                message=f"Error in custom validation: {str(e)}",
                failed_count=1,
            )
```

### Step 2: Register the Validation

Add registration to `validation_framework/validations/custom/__init__.py`:

```python
"""
Custom validations registration.
"""
from validation_framework.core.registry import register_validation
from validation_framework.validations.custom.my_validation import MyCustomValidation

# Register custom validation
register_validation("MyCustomValidation", MyCustomValidation)

# Register additional custom validations here
# register_validation("AnotherCustomValidation", AnotherCustomValidation)
```

### Step 3: Use in Configuration

```yaml
validations:
  - type: "MyCustomValidation"
    severity: "ERROR"
    params:
      check_field: "revenue"
      threshold: 1000000
      comparison: "gt"
    condition: "customer_tier == 'PLATINUM'"
```

### Step 4: Test the Validation

Create `tests/test_my_custom_validation.py`:

```python
"""
Tests for MyCustomValidation.
"""
import pytest
import pandas as pd
from validation_framework.validations.custom.my_validation import MyCustomValidation
from validation_framework.core.results import Severity


@pytest.fixture
def sample_data():
    """Create sample DataFrame for testing."""
    return pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5],
        "customer_tier": ["GOLD", "PLATINUM", "PLATINUM", "SILVER", "PLATINUM"],
        "revenue": [500000, 1500000, 2000000, 300000, 800000],
    })


def test_custom_validation_passes(sample_data):
    """Test validation passes when all values meet criteria."""
    validation = MyCustomValidation(
        name="RevenueCheck",
        severity=Severity.ERROR,
        params={
            "check_field": "revenue",
            "threshold": 1000000,
            "comparison": "gt"
        },
        condition="customer_tier == 'PLATINUM'"
    )

    def data_iter():
        yield sample_data

    context = {"max_sample_failures": 100}
    result = validation.validate(data_iter(), context)

    # Should pass: PLATINUM customers (rows 1,2,4) have revenue 1.5M, 2M, 0.8M
    # Row 4 with 0.8M fails, so overall should fail
    assert not result.passed
    assert result.failed_count == 1


def test_custom_validation_missing_field(sample_data):
    """Test validation fails gracefully when field missing."""
    validation = MyCustomValidation(
        name="RevenueCheck",
        severity=Severity.ERROR,
        params={
            "check_field": "nonexistent_field",
            "threshold": 1000000,
            "comparison": "gt"
        }
    )

    def data_iter():
        yield sample_data

    context = {"max_sample_failures": 100}
    result = validation.validate(data_iter(), context)

    assert not result.passed
    assert "not found" in result.message
```

---

## Creating Custom Loaders

### Step 1: Create Loader Class

Create `validation_framework/loaders/xml_loader.py`:

```python
"""
XML file loader for the Data Validation Framework.
"""
from typing import Iterator, Dict, Any
import pandas as pd
import xml.etree.ElementTree as ET
from validation_framework.loaders.base import DataLoader
import logging

logger = logging.getLogger(__name__)


class XMLLoader(DataLoader):
    """
    Loader for XML files.

    Parses XML files and yields DataFrame chunks.

    Configuration:
        root_tag (str): XML root element tag
        record_tag (str): Tag for each record
        chunk_size (int): Number of records per chunk
    """

    def __init__(
        self,
        file_path: str,
        chunk_size: int = 1000,
        root_tag: str = "root",
        record_tag: str = "record",
        **kwargs
    ):
        """
        Initialize XMLLoader.

        Args:
            file_path: Path to XML file
            chunk_size: Number of records to yield per chunk
            root_tag: Root element tag name
            record_tag: Record element tag name
        """
        super().__init__(file_path, chunk_size)
        self.root_tag = root_tag
        self.record_tag = record_tag

    def load(self) -> Iterator[pd.DataFrame]:
        """
        Load XML file and yield DataFrame chunks.

        Yields:
            DataFrame chunks with parsed XML data
        """
        try:
            logger.info(f"Loading XML file: {self.file_path}")

            # Parse XML incrementally
            context = ET.iterparse(self.file_path, events=('start', 'end'))
            context = iter(context)

            records = []

            for event, elem in context:
                if event == 'end' and elem.tag == self.record_tag:
                    # Convert XML element to dictionary
                    record = self._element_to_dict(elem)
                    records.append(record)

                    # Clear element to save memory
                    elem.clear()

                    # Yield chunk when chunk_size reached
                    if len(records) >= self.chunk_size:
                        df = pd.DataFrame(records)
                        yield df
                        records = []

            # Yield remaining records
            if records:
                df = pd.DataFrame(records)
                yield df

        except Exception as e:
            logger.error(f"Error loading XML file: {str(e)}")
            raise

    def _element_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        Convert XML element to dictionary.

        Args:
            element: XML element

        Returns:
            Dictionary representation of element
        """
        record = {}

        # Add element attributes
        record.update(element.attrib)

        # Add child elements
        for child in element:
            # Handle nested elements
            if len(child) > 0:
                record[child.tag] = self._element_to_dict(child)
            else:
                record[child.tag] = child.text

        return record

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get XML file metadata.

        Returns:
            Dictionary with file metadata
        """
        try:
            # Count records
            context = ET.iterparse(self.file_path, events=('end',))
            record_count = sum(1 for event, elem in context if elem.tag == self.record_tag)

            # Get sample record for columns
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            sample_record = root.find(f".//{self.record_tag}")

            columns = []
            if sample_record is not None:
                columns = list(self._element_to_dict(sample_record).keys())

            return {
                "row_count": record_count,
                "columns": columns,
                "column_count": len(columns),
                "file_format": "xml",
            }

        except Exception as e:
            logger.warning(f"Could not get XML metadata: {str(e)}")
            return {
                "row_count": None,
                "columns": [],
                "column_count": 0,
                "file_format": "xml",
            }
```

### Step 2: Register the Loader

Add to `validation_framework/loaders/factory.py`:

```python
from validation_framework.loaders.xml_loader import XMLLoader

class LoaderFactory:
    _loaders: Dict[str, Type[DataLoader]] = {
        "csv": CSVLoader,
        "excel": ExcelLoader,
        "json": JSONLoader,
        "parquet": ParquetLoader,
        "xml": XMLLoader,  # Add custom loader
    }

    extension_map = {
        ".csv": "csv",
        ".xlsx": "excel",
        ".xls": "excel",
        ".json": "json",
        ".jsonl": "json",
        ".parquet": "parquet",
        ".xml": "xml",  # Add extension mapping
    }
```

### Step 3: Use in Configuration

```yaml
files:
  - name: "xml_data"
    path: "data/records.xml"
    format: "xml"
    root_tag: "root"
    record_tag: "record"

    validations:
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["id", "name"]
```

---

## Creating Custom Reporters

### Step 1: Create Reporter Class

Create `validation_framework/reporters/pdf_reporter.py`:

```python
"""
PDF reporter for validation results.
"""
from validation_framework.reporters.base import Reporter
from validation_framework.core.results import ValidationReport
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import logging

logger = logging.getLogger(__name__)


class PDFReporter(Reporter):
    """
    Generates PDF validation reports.
    """

    def generate(self, report: ValidationReport, output_path: str):
        """
        Generate PDF report.

        Args:
            report: ValidationReport object
            output_path: Path for output PDF file
        """
        try:
            logger.info(f"Generating PDF report: {output_path}")

            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title = Paragraph(f"<b>{report.job_name}</b>", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))

            # Summary
            summary_text = f"""
            <b>Overall Status:</b> {report.overall_status.value}<br/>
            <b>Total Errors:</b> {report.total_errors}<br/>
            <b>Total Warnings:</b> {report.total_warnings}<br/>
            <b>Execution Time:</b> {report.execution_time}<br/>
            <b>Duration:</b> {report.duration_seconds:.2f} seconds
            """
            summary = Paragraph(summary_text, styles['Normal'])
            story.append(summary)
            story.append(Spacer(1, 20))

            # File reports
            for file_report in report.file_reports:
                # File header
                file_header = Paragraph(
                    f"<b>File: {file_report.file_name}</b>",
                    styles['Heading2']
                )
                story.append(file_header)

                # File status
                file_status = Paragraph(
                    f"Status: {file_report.status.value} | "
                    f"Errors: {file_report.error_count} | "
                    f"Warnings: {file_report.warning_count}",
                    styles['Normal']
                )
                story.append(file_status)
                story.append(Spacer(1, 12))

                # Validation results table
                table_data = [['Rule', 'Severity', 'Status', 'Failures']]

                for validation_result in file_report.validations:
                    table_data.append([
                        validation_result.rule_name,
                        validation_result.severity.value,
                        'PASS' if validation_result.passed else 'FAIL',
                        str(validation_result.failed_count)
                    ])

                table = Table(table_data)
                table.setStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ])
                story.append(table)
                story.append(Spacer(1, 20))

            # Build PDF
            doc.build(story)
            logger.info(f"PDF report generated successfully: {output_path}")

        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            raise
```

### Step 2: Use Custom Reporter

```python
from validation_framework.core.engine import ValidationEngine
from validation_framework.reporters.pdf_reporter import PDFReporter

# Run validation
engine = ValidationEngine.from_config("config.yaml")
report = engine.run()

# Generate PDF report
pdf_reporter = PDFReporter()
pdf_reporter.generate(report, "validation_report.pdf")
```

---

## Testing Custom Components

### Unit Test Template

```python
import pytest
import pandas as pd
from your_module import YourCustomValidation
from validation_framework.core.results import Severity


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        "field1": [1, 2, 3, 4, 5],
        "field2": ["a", "b", "c", "d", "e"],
    })


class TestYourCustomValidation:
    """Tests for YourCustomValidation."""

    def test_validation_passes(self, sample_data):
        """Test validation passes with valid data."""
        validation = YourCustomValidation(
            name="Test",
            severity=Severity.ERROR,
            params={"param1": "value1"}
        )

        def data_iter():
            yield sample_data

        context = {"max_sample_failures": 100}
        result = validation.validate(data_iter(), context)

        assert result.passed
        assert result.failed_count == 0

    def test_validation_fails(self, sample_data):
        """Test validation fails with invalid data."""
        # Modify data to cause failure
        sample_data.loc[0, "field1"] = -1

        validation = YourCustomValidation(
            name="Test",
            severity=Severity.ERROR,
            params={"param1": "value1"}
        )

        def data_iter():
            yield sample_data

        context = {"max_sample_failures": 100}
        result = validation.validate(data_iter(), context)

        assert not result.passed
        assert result.failed_count > 0

    def test_with_condition(self, sample_data):
        """Test validation with condition."""
        validation = YourCustomValidation(
            name="Test",
            severity=Severity.ERROR,
            params={"param1": "value1"},
            condition="field1 > 3"
        )

        def data_iter():
            yield sample_data

        context = {"max_sample_failures": 100}
        result = validation.validate(data_iter(), context)

        # Only rows 4 and 5 should be checked
        # Add assertions based on expected behavior
```

### Integration Test Template

```python
import tempfile
import yaml
from pathlib import Path
from validation_framework.core.engine import ValidationEngine


def test_custom_validation_integration(tmp_path):
    """Test custom validation in full pipeline."""
    # Create test data file
    data_file = tmp_path / "test_data.csv"
    data_file.write_text("field1,field2\n1,a\n2,b\n3,c")

    # Create config file
    config = {
        "validation_job": {
            "name": "Test Job",
            "description": "Integration test"
        },
        "settings": {
            "chunk_size": 1000,
            "max_sample_failures": 100
        },
        "files": [{
            "name": "test_data",
            "path": str(data_file),
            "format": "csv",
            "validations": [{
                "type": "YourCustomValidation",
                "severity": "ERROR",
                "params": {"param1": "value1"}
            }]
        }]
    }

    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config))

    # Run validation
    engine = ValidationEngine.from_config(str(config_file))
    report = engine.run(verbose=False)

    # Verify results
    assert report.overall_status.value in ["PASSED", "FAILED"]
    assert len(report.file_reports) == 1
```

---

## Contributing Guidelines

### Code Style

**Follow PEP 8**:
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names

**Type Hints**:
```python
def validate(
    self,
    data_iterator: Iterator[pd.DataFrame],
    context: Dict[str, Any]
) -> ValidationResult:
    pass
```

**Docstrings**:
```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When input is invalid
    """
    pass
```

### Testing Requirements

- Write tests for all new functionality
- Aim for 80%+ code coverage
- Test edge cases and error conditions
- Include integration tests for complex features

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and commit: `git commit -m "Add my feature"`
4. Push to branch: `git push origin feature/my-feature`
5. Create Pull Request with description
6. Ensure CI tests pass
7. Request review from maintainers

---

## API Reference

### Base Classes

#### DataValidationRule

```python
class DataValidationRule(ABC):
    def __init__(
        self,
        name: str,
        severity: Severity,
        params: Optional[Dict[str, Any]] = None,
        condition: Optional[str] = None
    )

    @abstractmethod
    def validate(
        self,
        data_iterator: Iterator[pd.DataFrame],
        context: Dict[str, Any]
    ) -> ValidationResult:
        """Execute validation logic"""

    @abstractmethod
    def get_description(self) -> str:
        """Get human-readable description"""

    def _evaluate_condition(self, df: pd.DataFrame) -> pd.Series:
        """Evaluate condition expression"""

    def _convert_condition_syntax(self, condition: str) -> str:
        """Convert SQL-like syntax to pandas"""

    def _create_result(
        self,
        passed: bool,
        message: str,
        failed_count: int = 0,
        total_count: int = 0,
        sample_failures: Optional[List[Dict]] = None
    ) -> ValidationResult:
        """Helper to create validation results"""
```

#### DataLoader

```python
class DataLoader(ABC):
    def __init__(self, file_path: str, chunk_size: int = 1000):
        self.file_path = file_path
        self.chunk_size = chunk_size

    @abstractmethod
    def load(self) -> Iterator[pd.DataFrame]:
        """Return iterator yielding DataFrame chunks"""

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return file metadata"""
```

#### Reporter

```python
class Reporter(ABC):
    @abstractmethod
    def generate(self, report: ValidationReport, output_path: str):
        """Generate report from ValidationReport"""
```

### Registry Functions

```python
def get_registry() -> ValidationRegistry:
    """Get global validation registry"""

def register_validation(name: str, validation_class: Type[DataValidationRule]):
    """Register validation type"""
```

### Results Classes

```python
@dataclass
class ValidationResult:
    rule_name: str
    severity: Severity
    passed: bool
    message: str
    failed_count: int = 0
    total_count: int = 0
    details: List[str] = field(default_factory=list)
    sample_failures: List[Dict] = field(default_factory=list)
    execution_time: float = 0.0

class FileValidationReport:
    file_name: str
    file_path: str
    file_format: str
    status: Status
    validations: List[ValidationResult]
    metadata: Dict[str, Any]
    execution_time: float

class ValidationReport:
    job_name: str
    execution_time: datetime
    duration_seconds: float
    overall_status: Status
    config: Dict[str, Any]
    file_reports: List[FileValidationReport]
    description: str
```

---

## Next Steps

- Review **[Technical Architecture](TECHNICAL_ARCHITECTURE.md)** for system internals
- See **[Examples](EXAMPLES.md)** for real-world validation scenarios
- Check **[User Guide](USER_GUIDE.md)** for configuration reference

---

**Questions?** Open an issue on GitHub or review the existing codebase for patterns and examples.
