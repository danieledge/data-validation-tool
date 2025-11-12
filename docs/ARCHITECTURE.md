# Architecture Overview

This document provides a comprehensive technical overview of the Data Validation Tool's architecture, design patterns, and implementation details.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [Design Patterns](#design-patterns)
4. [Data Flow](#data-flow)
5. [Performance Considerations](#performance-considerations)
6. [Extensibility](#extensibility)

---

## System Overview

The Data Validation Tool is built using a modular, plugin-based architecture that separates concerns and allows for easy extension. The system is designed to handle large-scale datasets (200GB+) efficiently through chunked processing and streaming.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Interface                          │
│                   (validation_framework.cli)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Validation Engine                         │
│                  (core/engine.py)                           │
│                                                             │
│  - Orchestrates validation workflow                        │
│  - Manages file processing                                 │
│  - Collects results                                        │
└──────┬────────────────┬─────────────────┬──────────────────┘
       │                │                 │
       ▼                ▼                 ▼
┌──────────┐    ┌──────────────┐   ┌──────────────┐
│ Config   │    │ Data Loaders │   │ Validation   │
│ Parser   │    │  (Factory)   │   │  Registry    │
│          │    │              │   │              │
│ YAML     │    │ - CSV        │   │ - File Rules │
│ Parser   │    │ - Excel      │   │ - Schema     │
│          │    │ - Parquet    │   │ - Field      │
│          │    │ - JSON       │   │ - Record     │
└──────────┘    └──────────────┘   └──────┬───────┘
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │ Validation Rules      │
                              │ (Base Classes)        │
                              │                       │
                              │ - ValidationRule      │
                              │ - FileValidationRule  │
                              │ - DataValidationRule  │
                              └───────────────────────┘
                                          │
       ┌──────────────────────────────────┼────────────────┐
       ▼                                  ▼                ▼
┌──────────────┐              ┌──────────────┐   ┌──────────────┐
│   Results    │              │   Reporters  │   │   Custom     │
│  Aggregation │              │              │   │  Validators  │
│              │              │ - HTML       │   │              │
│ - Status     │              │ - JSON       │   │ User-defined │
│ - Counts     │              │              │   │ validations  │
│ - Samples    │              │              │   │              │
└──────────────┘              └──────────────┘   └──────────────┘
```

### Technology Stack

- **Language**: Python 3.7+
- **Core Libraries**:
  - `pandas` - Data manipulation and chunked processing
  - `pyarrow` - Parquet file handling
  - `openpyxl` - Excel file support
  - `pyyaml` - Configuration parsing
  - `jinja2` - HTML report templating
  - `click` - CLI framework

---

## Core Components

### 1. Validation Engine (`core/engine.py`)

The central orchestration component that coordinates the entire validation process.

**Responsibilities**:
- Parse YAML configuration
- Initialize data loaders for each file
- Execute validations sequentially per file
- Aggregate results into comprehensive report
- Trigger report generation

**Key Classes**:

```python
class ValidationEngine:
    """
    Main validation orchestrator.

    Processes multiple files, executes validations,
    and generates comprehensive reports.
    """

    def __init__(self, config: ValidationConfig):
        """Initialize engine with parsed configuration."""

    def run(self, verbose: bool = True) -> ValidationReport:
        """
        Execute all validations.

        Returns:
            ValidationReport with all results
        """
```

**Processing Flow**:
1. Load and validate YAML configuration
2. For each file in configuration:
   - Create appropriate data loader
   - Execute all validations for that file
   - Collect results and metadata
3. Aggregate results into final report
4. Generate HTML and JSON outputs

---

### 2. Configuration Parser (`core/config.py`)

Handles parsing and validation of YAML configuration files.

**Responsibilities**:
- Parse YAML configuration
- Validate configuration structure
- Provide strongly-typed configuration objects

**Key Classes**:

```python
class ValidationConfig:
    """
    Parsed and validated configuration.

    Attributes:
        job_name: Name of validation job
        files: List of files to validate
        validations: Validation rules per file
        output_settings: Report generation settings
    """
```

**Validation**:
- Required fields present
- File paths are valid
- Validation types are registered
- Parameter types are correct

---

### 3. Data Loaders (`loaders/`)

Handle reading different file formats with chunked processing for memory efficiency.

**Factory Pattern**:

```python
class LoaderFactory:
    """
    Creates appropriate data loader based on file format.

    Supports: CSV, Excel, Parquet, JSON, Custom
    """

    @classmethod
    def create_loader(cls, file_path: str, file_format: str,
                      chunk_size: int = 50000) -> DataLoader:
        """
        Create and return appropriate loader.

        Args:
            file_path: Path to data file
            file_format: Format type (csv, excel, parquet, json)
            chunk_size: Rows per chunk for processing

        Returns:
            Appropriate DataLoader instance
        """
```

**Loaders**:

1. **CSVLoader** (`loaders/csv_loader.py`)
   - Handles CSV files with any delimiter
   - Uses `pandas.read_csv()` with `chunksize`
   - Configurable delimiter, encoding

2. **ExcelLoader** (`loaders/excel_loader.py`)
   - Reads Excel files (XLS, XLSX)
   - Uses `pandas.read_excel()` with `chunksize`
   - Supports multiple sheets

3. **ParquetLoader** (`loaders/parquet_loader.py`)
   - Optimized for Parquet format
   - Uses `pyarrow.parquet.ParquetFile.iter_batches()`
   - Most efficient for large files

4. **JSONLoader** (`loaders/json_loader.py`)
   - Handles JSON and JSON Lines formats
   - Chunked reading for large files

**Base Interface**:

```python
class DataLoader(ABC):
    """
    Abstract base class for all data loaders.
    """

    @abstractmethod
    def load(self) -> Iterator[pd.DataFrame]:
        """
        Load data in chunks.

        Yields:
            DataFrame chunks of configured size
        """

    @abstractmethod
    def get_metadata(self) -> FileMetadata:
        """
        Get file metadata (size, rows, columns).

        Returns:
            FileMetadata object
        """
```

---

### 4. Validation Registry (`core/registry.py`)

Global registry for validation rule discovery and instantiation.

**Registry Pattern**:

```python
class ValidationRegistry:
    """
    Global registry for validation rules.

    Allows dynamic registration and lookup of validation types.
    """

    def register(self, name: str, rule_class: Type[ValidationRule]):
        """Register a validation rule class."""

    def get(self, name: str) -> Type[ValidationRule]:
        """Retrieve a validation rule class by name."""

    def list_all(self) -> List[str]:
        """List all registered validation types."""

# Global instance
_global_registry = ValidationRegistry()

# Registration function
def register_validation(name: str, rule_class: Type[ValidationRule]):
    """Register a validation with the global registry."""
    _global_registry.register(name, rule_class)
```

**Auto-Registration**:

All built-in validations are automatically registered on import:

```python
# validation_framework/validations/builtin/registry.py

def register_all_builtin_validations():
    """Register all built-in validations."""
    # File-level
    register_validation("EmptyFileCheck", EmptyFileCheck)
    register_validation("RowCountRangeCheck", RowCountRangeCheck)

    # Schema
    register_validation("SchemaMatchCheck", SchemaMatchCheck)

    # Field-level
    register_validation("MandatoryFieldCheck", MandatoryFieldCheck)
    register_validation("RegexCheck", RegexCheck)

    # ... etc

# Auto-register on module import
register_all_builtin_validations()
```

---

### 5. Validation Rules (`validations/`)

The core validation logic organized by type.

**Base Classes** (`validations/base.py`):

```python
class ValidationRule(ABC):
    """
    Abstract base for all validation rules.

    Template method pattern for consistent execution.
    """

    def __init__(self, severity: Severity, params: Dict[str, Any] = None):
        """Initialize with severity and parameters."""
        self.severity = severity
        self.params = params or {}

    @abstractmethod
    def get_description(self) -> str:
        """Return human-readable description."""

    def _create_result(self, passed: bool, message: str, **kwargs) -> ValidationResult:
        """Helper to create standardized results."""


class FileValidationRule(ValidationRule):
    """
    Base for file-level validations.

    These run before processing data (check file properties).
    """

    @abstractmethod
    def validate(self, file_path: str, context: Dict[str, Any]) -> ValidationResult:
        """Validate file-level properties."""


class DataValidationRule(ValidationRule):
    """
    Base for data-level validations.

    These process data in chunks for memory efficiency.
    """

    @abstractmethod
    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """Validate data across chunks."""
```

**Implementation Structure**:

```
validations/
├── base.py                  # Base classes
├── builtin/                 # Built-in validations
│   ├── file_checks.py       # File-level validations
│   ├── schema_checks.py     # Schema validations
│   ├── field_checks.py      # Field-level validations
│   ├── record_checks.py     # Record-level validations
│   ├── inline_checks.py     # Bespoke custom checks
│   └── registry.py          # Auto-registration
└── custom/                  # User custom validations
    └── (user-defined files)
```

**Example Implementation**:

```python
class RegexCheck(DataValidationRule):
    """
    Validates field values against regex pattern.
    """

    def get_description(self) -> str:
        field = self.params.get("field", "unknown")
        pattern = self.params.get("pattern", "")
        return f"Regex check on '{field}': {pattern}"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """
        Validate field values against regex.

        Processes data in chunks for memory efficiency.
        """
        field = self.params.get("field")
        pattern = self.params.get("pattern")

        # Compile regex once
        regex = re.compile(pattern)

        total_rows = 0
        failed_rows = []
        max_samples = context.get("max_sample_failures", 100)

        # Process each chunk
        for chunk in data_iterator:
            if field not in chunk.columns:
                return self._create_result(
                    passed=False,
                    message=f"Field '{field}' not found"
                )

            # Validate each row in chunk
            for idx, value in chunk[field].dropna().items():
                if not regex.match(str(value)):
                    if len(failed_rows) < max_samples:
                        failed_rows.append({
                            "row": int(total_rows + idx),
                            "field": field,
                            "value": str(value),
                            "message": "Does not match pattern"
                        })

            total_rows += len(chunk)

        # Return result
        if failed_rows:
            return self._create_result(
                passed=False,
                message=f"Found {len(failed_rows)} invalid values",
                failed_count=len(failed_rows),
                total_count=total_rows,
                sample_failures=failed_rows
            )

        return self._create_result(
            passed=True,
            message=f"All {total_rows} values valid",
            total_count=total_rows
        )
```

---

### 6. Results (`core/results.py`)

Data structures for representing validation results.

**Key Classes**:

```python
class Severity(Enum):
    """Validation severity levels."""
    ERROR = "ERROR"
    WARNING = "WARNING"

class Status(Enum):
    """Validation status."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"

class ValidationResult:
    """
    Result from a single validation rule.

    Attributes:
        rule_name: Name of validation
        passed: Whether validation passed
        severity: ERROR or WARNING
        message: Summary message
        failed_count: Number of failures
        total_count: Total records checked
        sample_failures: Sample of failed records
    """

class FileValidationReport:
    """
    Aggregated results for a single file.

    Attributes:
        file_name: Name of file
        file_path: Full path
        status: Overall status (PASSED, FAILED, WARNING)
        validation_results: List of ValidationResult
        metadata: File metadata
        error_count: Count of ERROR severity failures
        warning_count: Count of WARNING severity failures
    """

class ValidationReport:
    """
    Complete validation report for all files.

    Attributes:
        job_name: Name of validation job
        overall_status: Aggregated status
        file_reports: List of FileValidationReport
        total_errors: Total ERROR count
        total_warnings: Total WARNING count
        execution_time: When validation ran
        duration_seconds: How long it took
    """
```

---

### 7. Reporters (`reporters/`)

Generate human-readable and machine-readable outputs.

**Base Interface**:

```python
class Reporter(ABC):
    """Abstract base for all reporters."""

    @abstractmethod
    def generate(self, report: ValidationReport, output_path: str):
        """
        Generate report file.

        Args:
            report: Validation results
            output_path: Where to write report
        """
```

**HTML Reporter** (`reporters/html_reporter.py`):

- Uses Jinja2 templating
- Embedded template (no external files needed)
- Modern dark theme (Tokyo Night)
- Mobile-responsive design
- Auto-expands failed validations

**JSON Reporter** (`reporters/json_reporter.py`):

- Machine-readable output
- Complete validation results
- Suitable for CI/CD integration
- Easily parseable by other tools

---

## Design Patterns

### 1. Factory Pattern

Used in `LoaderFactory` to create appropriate data loaders based on file format.

**Benefits**:
- Decouples loader creation from usage
- Easy to add new file formats
- Centralized loader instantiation logic

### 2. Registry Pattern

Used in `ValidationRegistry` for validation rule discovery.

**Benefits**:
- Dynamic registration of validation types
- No hard-coded validation lists
- Easy to add custom validations
- Plugin-based architecture

### 3. Template Method Pattern

Used in `ValidationRule` base class.

**Benefits**:
- Consistent validation execution
- Standardized result creation
- Reusable common logic
- Clear extension points

### 4. Iterator Pattern

Used throughout for chunked data processing.

**Benefits**:
- Memory-efficient processing
- Handles large files (200GB+)
- Lazy evaluation
- Consistent interface

### 5. Strategy Pattern

Each validation rule is a strategy for validating data.

**Benefits**:
- Interchangeable validation algorithms
- Easy to combine multiple validations
- Clear separation of concerns

---

## Data Flow

### Validation Execution Flow

```
1. User invokes CLI
   └─> data-validate validate config.yaml

2. CLI loads and parses YAML
   └─> Creates ValidationConfig object

3. ValidationEngine initialized
   └─> Receives config

4. For each file in config:

   a. Create data loader
      └─> LoaderFactory.create_loader()

   b. Get file metadata
      └─> loader.get_metadata()

   c. Execute file-level validations
      └─> Pass file path directly

   d. Execute data-level validations
      └─> Pass data iterator (chunks)
      └─> Each validation processes chunks
      └─> Aggregate results across chunks

   e. Collect results
      └─> Create FileValidationReport

5. Aggregate all file results
   └─> Create ValidationReport

6. Generate reports
   └─> HTMLReporter.generate()
   └─> JSONReporter.generate()

7. Return exit code
   └─> 0 if passed, 1 if failed
```

### Chunk Processing Flow

```
Data File (200GB)
     │
     ├─> Read chunk 1 (50,000 rows)
     │   └─> Pass to Validation 1
     │   └─> Pass to Validation 2
     │   └─> Pass to Validation N
     │
     ├─> Read chunk 2 (50,000 rows)
     │   └─> Pass to Validation 1
     │   └─> Pass to Validation 2
     │   └─> Pass to Validation N
     │
     └─> Read chunk M (remaining rows)
         └─> Pass to Validation 1
         └─> Pass to Validation 2
         └─> Pass to Validation N

Note: Validations aggregate results across all chunks
```

---

## Performance Considerations

### 1. Chunked Processing

**Strategy**: Process data in configurable chunks (default 50,000 rows).

**Benefits**:
- Constant memory usage regardless of file size
- Can process files larger than available RAM
- Parallelizable in future versions

**Configuration**:
```yaml
files:
  - name: "large_file"
    path: "data/200gb_file.csv"
    chunk_size: 100000  # Adjust based on available memory
```

### 2. Streaming Approach

**Strategy**: Use Python generators/iterators throughout.

**Benefits**:
- Lazy evaluation
- No unnecessary data materialization
- Memory efficient

### 3. Format-Specific Optimizations

**Parquet**:
- Uses PyArrow's native batch reading
- Columnar format reduces I/O
- Best performance for large files

**CSV**:
- Configurable delimiter
- Low memory mode enabled
- Type inference disabled for speed

**Excel**:
- Sheet-specific loading
- Chunked reading where possible

### 4. Regex Compilation

**Strategy**: Compile regex patterns once, reuse across chunks.

```python
# Compile once
regex = re.compile(pattern)

# Reuse across all chunks
for chunk in data_iterator:
    for value in chunk[field]:
        if regex.match(value):  # Fast
            ...
```

### 5. Sample Collection

**Strategy**: Collect only N sample failures (default 100).

**Benefits**:
- Prevents unbounded memory growth
- Faster report generation
- Sufficient for debugging

---

## Extensibility

### Adding Custom Validations

The framework is designed for easy extension. Here's how to add custom validations:

**Step 1: Create validation class**

```python
# validations/custom/my_validation.py

from validation_framework.validations.base import DataValidationRule
from validation_framework.core.results import ValidationResult

class MyCustomValidation(DataValidationRule):
    """
    Custom validation for specific business logic.
    """

    def get_description(self) -> str:
        return "My custom validation"

    def validate(self, data_iterator, context):
        """
        Implement validation logic.

        Access parameters via self.params
        """
        # Your logic here
        pass
```

**Step 2: Register validation**

```python
from validation_framework.core.registry import register_validation
from .my_validation import MyCustomValidation

register_validation("MyCustomValidation", MyCustomValidation)
```

**Step 3: Use in YAML**

```yaml
validations:
  - type: "MyCustomValidation"
    severity: "ERROR"
    params:
      custom_param: "value"
```

### Adding New File Formats

**Step 1: Create loader class**

```python
# loaders/my_format_loader.py

from validation_framework.loaders.base import DataLoader

class MyFormatLoader(DataLoader):
    """Loader for custom file format."""

    def load(self):
        """Yield data chunks."""
        # Your loading logic
        pass

    def get_metadata(self):
        """Return file metadata."""
        # Your metadata logic
        pass
```

**Step 2: Register in factory**

```python
# loaders/factory.py

class LoaderFactory:
    @classmethod
    def create_loader(cls, file_path, file_format, **kwargs):
        if file_format == "myformat":
            return MyFormatLoader(file_path, **kwargs)
        # ... existing formats
```

### Adding New Reporters

**Step 1: Create reporter class**

```python
# reporters/my_reporter.py

from validation_framework.reporters.base import Reporter

class MyReporter(Reporter):
    """Custom report format."""

    def generate(self, report, output_path):
        """Generate custom report."""
        # Your reporting logic
        pass
```

**Step 2: Use in code**

```python
from reporters.my_reporter import MyReporter

reporter = MyReporter()
reporter.generate(validation_report, "output.myformat")
```

---

## Error Handling

### Graceful Degradation

The framework handles missing optional dependencies gracefully:

```python
try:
    import pyarrow
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False

def load_parquet(file_path):
    if not HAS_PYARROW:
        raise RuntimeError(
            "PyArrow is required for Parquet files. "
            "Install with: pip install pyarrow"
        )
    # Load parquet
```

### Validation Error Handling

Each validation catches and reports errors:

```python
def validate(self, data_iterator, context):
    try:
        # Validation logic
        pass
    except Exception as e:
        return self._create_result(
            passed=False,
            message=f"Validation error: {str(e)}",
            failed_count=1
        )
```

---

## Testing Strategy

### Unit Tests

- Test each validation independently
- Mock data iterators
- Verify results structure

### Integration Tests

- Test complete validation workflows
- Use real sample data
- Verify report generation

### Performance Tests

- Benchmark with large files
- Memory profiling
- Chunk size optimization

---

## Future Enhancements

### Potential Improvements

1. **Parallel Processing**
   - Process multiple files concurrently
   - Parallel chunk processing

2. **Distributed Computing**
   - Spark/Dask integration
   - Cloud-native execution

3. **Advanced Analytics**
   - Data profiling
   - Statistical analysis
   - Anomaly detection

4. **Interactive Reports**
   - Searchable/filterable results
   - Chart visualizations
   - Export to Excel

5. **API Server**
   - REST API for validation
   - Web UI for configuration
   - Real-time monitoring

---

## Conclusion

The Data Validation Tool's architecture provides:

✅ **Modularity** - Clear separation of concerns
✅ **Extensibility** - Easy to add new validations and formats
✅ **Performance** - Handles 200GB+ files efficiently
✅ **Usability** - Simple YAML configuration
✅ **Reliability** - Comprehensive error handling

The design patterns and architectural decisions make the framework production-ready while remaining accessible to both technical and non-technical users.

---

**For more information, see:**
- [Technical Guide](TECHNICAL_GUIDE.md) - Advanced usage
- [API Reference](API_REFERENCE.md) - Python API docs
- [Contributing](CONTRIBUTING.md) - Extend the framework
