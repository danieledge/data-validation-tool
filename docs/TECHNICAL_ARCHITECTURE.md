# Technical Architecture

**Internal system design and implementation details**

This document explains how the Data Validation Framework works internally, its architecture, design patterns, and technical implementation.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Module Reference](#module-reference)
7. [Extension Points](#extension-points)
8. [Performance Characteristics](#performance-characteristics)
9. [Error Handling](#error-handling)
10. [Testing Strategy](#testing-strategy)

---

## System Overview

The Data Validation Framework is a modular, extensible Python-based system for validating data quality across multiple file formats.

### Key Design Principles

1. **Separation of Concerns**: Each component has a single, well-defined responsibility
2. **Extensibility**: Plugin architecture allows custom validations and loaders
3. **Performance**: Chunked processing handles large files efficiently
4. **Configuration-Driven**: No code required for standard validations
5. **Type Safety**: Leverages Python type hints throughout
6. **Testability**: Components are loosely coupled and easily testable

### Technology Stack

- **Python 3.8+**: Core language
- **Pandas**: Data processing and manipulation
- **PyYAML**: Configuration parsing
- **pytest**: Testing framework
- **Jinja2**: HTML report generation

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Entry Point                          │
│                  validation_framework.cli                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Validation Engine                           │
│                  (core/engine.py)                                │
│  • Orchestrates validation workflow                              │
│  • Loads configuration                                           │
│  • Creates loaders and validations                               │
│  • Generates reports                                             │
└─────┬───────────────────────────────────────────┬───────────────┘
      │                                           │
      ▼                                           ▼
┌─────────────────────┐              ┌─────────────────────────────┐
│  Configuration      │              │   Validation Registry       │
│  (core/config.py)   │              │   (core/registry.py)        │
│  • Parses YAML      │              │   • Stores validation types │
│  • Validates config │              │   • Plugin registration     │
└─────────────────────┘              └─────────────────────────────┘
      │                                           │
      ▼                                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Loader Factory                              │
│                  (loaders/factory.py)                            │
│  • Creates appropriate loader based on file format               │
└────────────┬────────────────────────────────────────────────────┘
             │
    ┌────────┴────────┬────────────┬──────────────┬──────────────┐
    ▼                 ▼            ▼              ▼              ▼
┌─────────┐    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│CSV      │    │Excel     │  │JSON      │  │Parquet   │  │Custom    │
│Loader   │    │Loader    │  │Loader    │  │Loader    │  │Loaders   │
└────┬────┘    └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │              │             │             │             │
     └──────────────┴─────────────┴─────────────┴─────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   Data Iterator             │
                    │   (yields DataFrame chunks) │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Validation Rules                                │
│                  (validations/base.py)                           │
│  • Abstract base class                                           │
│  • Condition evaluation                                          │
│  • Result creation                                               │
└────────────┬────────────────────────────────────────────────────┘
             │
    ┌────────┴────────┬────────────┬──────────────┬──────────────┐
    ▼                 ▼            ▼              ▼              ▼
┌─────────┐    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│File     │    │Schema    │  │Field     │  │Record    │  │Custom    │
│Level    │    │Checks    │  │Checks    │  │Checks    │  │Checks    │
└────┬────┘    └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │              │             │             │             │
     └──────────────┴─────────────┴─────────────┴─────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   ValidationResult          │
                    │   (core/results.py)         │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │   Report Generation         │
                    │   (reporters/)              │
                    │   • HTML Reporter           │
                    │   • JSON Reporter           │
                    └─────────────────────────────┘
```

---

## Core Components

### 1. Validation Engine (`core/engine.py`)

**Purpose**: Orchestrates the entire validation workflow

**Key Responsibilities**:
- Load and parse configuration
- Create data loaders for each file
- Instantiate validation rules
- Execute validations in order
- Collect and aggregate results
- Generate reports

**Key Methods**:
```python
class ValidationEngine:
    def __init__(self, config: ValidationConfig)
    def run(self, verbose: bool) -> ValidationReport
    def _validate_file(self, file_config, verbose) -> FileValidationReport
    def generate_html_report(self, report, output_path)
    def generate_json_report(self, report, output_path)
```

**Workflow**:
1. Parse configuration from YAML
2. For each file in configuration:
   - Create appropriate loader
   - Get file metadata
   - For each validation rule:
     - Instantiate validation class
     - Create data iterator
     - Execute validation
     - Collect results
3. Aggregate results
4. Generate reports

---

### 2. Configuration System (`core/config.py`)

**Purpose**: Parse and validate YAML configuration

**Key Classes**:
```python
class ValidationConfig:
    job_name: str
    description: str
    chunk_size: int
    max_sample_failures: int
    files: List[Dict[str, Any]]

    @classmethod
    def from_yaml(cls, config_path: str) -> ValidationConfig
    def to_dict(self) -> Dict[str, Any]
```

**Configuration Validation**:
- Validates required fields
- Checks file paths exist
- Validates severity levels
- Infers file formats from extensions
- Parses validation parameters

**Design Pattern**: Builder pattern for configuration construction

---

### 3. Registry System (`core/registry.py`)

**Purpose**: Plugin architecture for validation rules

**Key Features**:
- Singleton pattern for global registry
- Register validation classes by name
- Retrieve validation classes for instantiation
- List available validations

**Key Methods**:
```python
class ValidationRegistry:
    def register(self, name: str, validation_class: Type[DataValidationRule])
    def get(self, name: str) -> Type[DataValidationRule]
    def is_registered(self, name: str) -> bool
    def list_available(self) -> List[str]

# Global functions
def get_registry() -> ValidationRegistry
def register_validation(name: str, validation_class)
```

**Auto-Registration**:
Built-in validations are automatically registered on import:
```python
# validation_framework/validations/builtin/registry.py
def register_all_builtin_validations():
    register_validation("MandatoryFieldCheck", MandatoryFieldCheck)
    register_validation("RangeCheck", RangeCheck)
    # ... all built-in validations
```

---

### 4. Loader System (`loaders/`)

**Purpose**: Abstract file format differences

**Base Class** (`loaders/base.py`):
```python
class DataLoader(ABC):
    @abstractmethod
    def load(self) -> Iterator[pd.DataFrame]
        """Return iterator yielding data chunks"""

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]
        """Return file metadata (row count, columns, etc.)"""
```

**Loader Factory** (`loaders/factory.py`):
```python
class LoaderFactory:
    _loaders: Dict[str, Type[DataLoader]] = {
        "csv": CSVLoader,
        "excel": ExcelLoader,
        "json": JSONLoader,
        "parquet": ParquetLoader,
    }

    @classmethod
    def create_loader(cls, file_path, file_format, **kwargs) -> DataLoader

    @classmethod
    def register_loader(cls, format_name, loader_class)
```

**Design Pattern**: Factory pattern with registration mechanism

**Implementations**:
- **CSVLoader**: Uses `pd.read_csv()` with chunking
- **ExcelLoader**: Uses `pd.read_excel()` with sheet support
- **JSONLoader**: Handles JSON arrays and JSON Lines with flattening
- **ParquetLoader**: Uses `pd.read_parquet()` with columnar efficiency

---

### 5. Validation Rule System (`validations/`)

**Base Class** (`validations/base.py`):
```python
class DataValidationRule(ABC):
    def __init__(self, name, severity, params, condition=None):
        self.name = name
        self.severity = severity
        self.params = params
        self.condition = condition

    @abstractmethod
    def validate(self, data_iterator, context) -> ValidationResult:
        """Execute validation logic"""

    @abstractmethod
    def get_description(self) -> str:
        """Human-readable description"""

    def _evaluate_condition(self, df) -> pd.Series:
        """Evaluate condition expression"""

    def _create_result(self, passed, message, **kwargs) -> ValidationResult:
        """Helper to create validation results"""
```

**Validation Categories**:
1. **File-Level**: Operate on entire file (EmptyFileCheck, RowCountRangeCheck)
2. **Schema**: Validate structure (SchemaMatchCheck, ColumnPresenceCheck)
3. **Field-Level**: Per-field validation (MandatoryFieldCheck, RangeCheck, RegexCheck)
4. **Record-Level**: Cross-row validation (DuplicateRowCheck, UniqueKeyCheck)
5. **Conditional**: If-then-else logic (ConditionalValidation)
6. **Advanced**: Statistical and complex (StatisticalOutlierCheck, CrossFieldComparisonCheck)

**Design Pattern**: Template Method pattern - base class defines workflow, subclasses implement specifics

---

### 6. Results System (`core/results.py`)

**Purpose**: Standardized validation results

**Key Classes**:
```python
@dataclass
class ValidationResult:
    rule_name: str
    severity: Severity
    passed: bool
    message: str
    failed_count: int
    total_count: int
    sample_failures: List[Dict]
    execution_time: float

class FileValidationReport:
    file_name: str
    file_path: str
    status: Status
    validations: List[ValidationResult]

    def add_result(self, result: ValidationResult)
    def update_status(self)

class ValidationReport:
    job_name: str
    execution_time: datetime
    overall_status: Status
    file_reports: List[FileValidationReport]

    def add_file_report(self, file_report)
    def update_overall_status(self)
    def to_dict(self) -> Dict
```

**Status Enum**:
```python
class Status(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"

class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
```

---

### 7. Reporter System (`reporters/`)

**Purpose**: Generate output reports

**Base Class** (`reporters/base.py`):
```python
class Reporter(ABC):
    @abstractmethod
    def generate(self, report: ValidationReport, output_path: str)
```

**Implementations**:
- **HTMLReporter** (`reporters/html_reporter.py`):
  - Uses Jinja2 templates
  - Generates styled, interactive HTML
  - Includes summary, details, sample failures

- **JSONReporter** (`reporters/json_reporter.py`):
  - Serializes ValidationReport to JSON
  - Machine-readable for integration
  - Preserves all validation details

---

## Data Flow

### Detailed Execution Flow

```
1. CLI Entry
   ├─> Parse command line arguments
   └─> Load configuration file

2. Configuration Loading
   ├─> Parse YAML
   ├─> Validate structure
   ├─> Resolve file paths
   └─> Create ValidationConfig object

3. Engine Initialization
   ├─> Create ValidationEngine(config)
   └─> Get validation registry

4. For Each File:
   ├─> Create Loader
   │   ├─> Detect/validate format
   │   ├─> Create appropriate loader instance
   │   └─> Get file metadata
   │
   ├─> For Each Validation:
   │   ├─> Get validation class from registry
   │   ├─> Instantiate with parameters
   │   ├─> Create data iterator (chunked)
   │   │
   │   ├─> Execute Validation:
   │   │   ├─> For each chunk:
   │   │   │   ├─> Evaluate condition (if present)
   │   │   │   ├─> Filter rows by condition
   │   │   │   ├─> Apply validation logic
   │   │   │   ├─> Collect failures
   │   │   │   └─> Continue to next chunk
   │   │   │
   │   │   └─> Create ValidationResult
   │   │
   │   └─> Add result to FileValidationReport
   │
   └─> Add FileValidationReport to ValidationReport

5. Aggregation
   ├─> Calculate overall status
   ├─> Count total errors/warnings
   └─> Calculate execution time

6. Report Generation
   ├─> HTML Report (if requested)
   └─> JSON Report (if requested)

7. Exit
   └─> Return exit code (0=pass, 1=fail, 2=error)
```

### Data Iterator Pattern

**Why Chunked Processing?**
- Memory efficiency for large files
- Consistent interface across file formats
- Enables streaming validation

**Implementation**:
```python
def load(self) -> Iterator[pd.DataFrame]:
    """Yield DataFrame chunks"""
    for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size):
        yield chunk

# Usage in validation
for chunk in data_iterator:
    # Process this chunk
    for idx, row in chunk.iterrows():
        # Validate row
        pass
```

**Memory Characteristics**:
- Only `chunk_size` rows in memory at once
- Validations process incrementally
- Sample failures collected up to `max_sample_failures`

---

## Design Patterns

### 1. Factory Pattern

**Used in**: Loader creation, Validation instantiation

**Purpose**: Create objects without specifying exact class

**Implementation**:
```python
class LoaderFactory:
    _loaders = {"csv": CSVLoader, "excel": ExcelLoader, ...}

    @classmethod
    def create_loader(cls, file_path, file_format, **kwargs):
        loader_class = cls._loaders[file_format]
        return loader_class(file_path, **kwargs)
```

**Benefits**:
- Easy to add new loaders
- Centralized creation logic
- Runtime format selection

---

### 2. Registry Pattern

**Used in**: Validation rule registration

**Purpose**: Plugin architecture for extensibility

**Implementation**:
```python
class ValidationRegistry:
    def __init__(self):
        self._validations: Dict[str, Type[DataValidationRule]] = {}

    def register(self, name, validation_class):
        self._validations[name] = validation_class

    def get(self, name):
        return self._validations[name]
```

**Benefits**:
- Decouple validation discovery from usage
- Enable custom validations
- Auto-registration on import

---

### 3. Template Method Pattern

**Used in**: DataValidationRule base class

**Purpose**: Define workflow skeleton, let subclasses fill in steps

**Implementation**:
```python
class DataValidationRule(ABC):
    def validate(self, data_iterator, context):
        # Template method - defines workflow
        # Subclasses implement specific logic
        pass

    @abstractmethod
    def get_description(self):
        # Must be implemented by subclasses
        pass
```

---

### 4. Iterator Pattern

**Used in**: Data loading

**Purpose**: Sequential access without exposing underlying representation

**Benefits**:
- Uniform interface for all file formats
- Memory-efficient streaming
- Lazy evaluation

---

### 5. Strategy Pattern

**Used in**: Conditional validation, severity handling

**Purpose**: Select algorithm at runtime

**Example**:
```python
class ConditionalValidation:
    def validate(self, data_iterator, context):
        if condition_true:
            # Strategy 1: Execute then_validate
            self._execute_validations(then_validate_configs, ...)
        else:
            # Strategy 2: Execute else_validate
            self._execute_validations(else_validate_configs, ...)
```

---

### 6. Singleton Pattern

**Used in**: ValidationRegistry

**Purpose**: Single global registry instance

**Implementation**:
```python
_global_registry = None

def get_registry() -> ValidationRegistry:
    global _global_registry
    if _global_registry is None:
        _global_registry = ValidationRegistry()
    return _global_registry
```

---

## Module Reference

### Core Modules

```
validation_framework/
├── __init__.py
├── cli.py                    # Command-line interface
├── core/
│   ├── __init__.py
│   ├── engine.py             # ValidationEngine - main orchestrator
│   ├── config.py             # ValidationConfig - YAML parsing
│   ├── registry.py           # ValidationRegistry - plugin system
│   ├── results.py            # ValidationResult, Report classes
│   └── logging_config.py     # Logging configuration
├── loaders/
│   ├── __init__.py
│   ├── base.py               # DataLoader abstract base
│   ├── factory.py            # LoaderFactory
│   ├── csv_loader.py         # CSV file support
│   ├── excel_loader.py       # Excel file support
│   ├── json_loader.py        # JSON file support
│   └── parquet_loader.py     # Parquet file support
├── validations/
│   ├── __init__.py
│   ├── base.py               # DataValidationRule base class
│   ├── builtin/
│   │   ├── __init__.py
│   │   ├── registry.py       # Auto-registration
│   │   ├── file_checks.py    # File-level validations
│   │   ├── schema_checks.py  # Schema validations
│   │   ├── field_checks.py   # Field-level validations
│   │   ├── record_checks.py  # Record-level validations
│   │   ├── conditional.py    # Conditional validation
│   │   ├── inline_checks.py  # Inline/custom checks
│   │   └── advanced_checks.py # Statistical validations
│   └── custom/
│       └── __init__.py       # Custom validations
└── reporters/
    ├── __init__.py
    ├── base.py               # Reporter abstract base
    ├── html_reporter.py      # HTML report generation
    └── json_reporter.py      # JSON report generation
```

### Dependencies

**Core Dependencies**:
- `pandas >= 1.3.0` - Data manipulation
- `pyyaml >= 5.4.0` - YAML parsing
- `jinja2 >= 3.0.0` - HTML templating

**Optional Dependencies**:
- `openpyxl >= 3.0.0` - Excel support
- `pyarrow >= 5.0.0` - Parquet support
- `colorama >= 0.4.0` - Colored console output

---

## Extension Points

### 1. Custom Data Loaders

**Create a custom loader for new file formats**:

```python
from validation_framework.loaders.base import DataLoader
from validation_framework.loaders.factory import LoaderFactory
import pandas as pd

class XMLLoader(DataLoader):
    def load(self) -> Iterator[pd.DataFrame]:
        # Custom XML parsing logic
        # Yield DataFrame chunks
        pass

    def get_metadata(self) -> Dict[str, Any]:
        # Return file metadata
        pass

# Register the loader
LoaderFactory.register_loader("xml", XMLLoader)
```

---

### 2. Custom Validations

**Create custom validation rules**:

```python
from validation_framework.validations.base import DataValidationRule, ValidationResult
from validation_framework.core.registry import register_validation

class MyCustomValidation(DataValidationRule):
    def get_description(self) -> str:
        return "My custom validation logic"

    def validate(self, data_iterator, context) -> ValidationResult:
        # Custom validation logic
        # Process chunks
        # Return ValidationResult
        pass

# Register the validation
register_validation("MyCustomValidation", MyCustomValidation)
```

---

### 3. Custom Reporters

**Create custom report formats**:

```python
from validation_framework.reporters.base import Reporter
from validation_framework.core.results import ValidationReport

class PDFReporter(Reporter):
    def generate(self, report: ValidationReport, output_path: str):
        # Generate PDF report
        pass
```

---

## Performance Characteristics

### Time Complexity

**Per Validation**:
- File-level checks: O(1) - single pass
- Schema checks: O(1) - metadata only
- Field checks: O(n) - one pass through data
- Duplicate checks: O(n log n) - requires sorting/hashing
- Statistical checks: O(n) to O(2n) - may require multiple passes

**Overall**: O(v * n) where v = number of validations, n = number of rows

### Space Complexity

**Memory Usage**:
- Chunk size: `chunk_size * number_of_columns * 8 bytes` (approximate)
- Sample failures: `max_sample_failures * number_of_failed_validations`
- Metadata: O(1) per file

**Example**:
- 1000 rows/chunk × 50 columns × 8 bytes = ~400 KB per chunk
- 100 sample failures × 10 validations = up to 1000 failure records

### Scalability

**File Size**:
- ✅ 1 MB - 100 MB: Excellent performance
- ✅ 100 MB - 1 GB: Good performance
- ✅ 1 GB - 10 GB: Acceptable performance with tuning
- ⚠️  10 GB+: Use Parquet format, increase chunk size

**Number of Validations**:
- Linear scaling: 10 validations ≈ 10x time of 1 validation
- Consider disabling expensive validations in development

**Optimization Strategies**:
1. Increase chunk_size for more columns/memory
2. Decrease chunk_size for less memory
3. Use Parquet for large files (10x faster than CSV)
4. Limit sample failures for faster reporting
5. Order validations by speed (fast first)
6. Disable statistical checks during development

---

## Error Handling

### Error Categories

**1. Configuration Errors** (exit code 2):
- Invalid YAML syntax
- Missing required fields
- File not found
- Invalid parameters

**2. Validation Failures** (exit code 1):
- Data quality issues
- Business rule violations
- Returns ValidationResult with passed=False

**3. Runtime Errors** (exit code 2):
- File read errors
- Memory errors
- Unexpected exceptions

### Error Handling Strategy

```python
try:
    # Validation logic
    result = validation.validate(data_iterator, context)
except FileNotFoundError:
    # Handle missing files
    logger.error("File not found")
    # Return error result
except pd.errors.ParserError:
    # Handle parsing errors
    logger.error("Cannot parse file")
except Exception as e:
    # Catch-all for unexpected errors
    logger.exception("Unexpected error")
    # Return error result
```

**Graceful Degradation**:
- Individual validation failures don't stop execution
- Errors are captured as ValidationResult objects
- Full report generated even with some failures

---

## Testing Strategy

### Test Pyramid

```
       ┌─────────────┐
       │   Manual    │  End-to-end scenarios
       │   Testing   │  (exploratory)
       └─────────────┘
      ┌───────────────┐
      │  Integration  │  Full workflows
      │     Tests     │  (pytest)
      └───────────────┘
    ┌───────────────────┐
    │   Component Tests  │  Individual validations
    │    (Unit Tests)    │  (pytest)
    └───────────────────┘
  ┌───────────────────────┐
  │     Smoke Tests        │  Quick sanity checks
  │  (Built-in fixtures)   │  (pytest)
  └───────────────────────┘
```

### Test Categories

**1. Unit Tests**:
- Test individual validation classes
- Mock data iterators
- Verify ValidationResult correctness

**2. Integration Tests**:
- Test full validation workflows
- Use actual test data files
- Verify end-to-end results

**3. Fixture Tests**:
- Test with sample data files
- Verify file format handling
- Test edge cases

**Test Coverage**:
- Target: 80%+ code coverage
- Critical paths: 100% coverage
- Edge cases: Well-documented

See **[Test Case Documentation](TEST_DOCUMENTATION.md)** for comprehensive testing guide.

---

## Next Steps

- **[Developer Guide](DEVELOPER_GUIDE.md)** - Create custom validations and extensions
- **[User Guide](USER_GUIDE.md)** - Configuration and usage
- **[Examples](EXAMPLES.md)** - Real-world scenarios

---

**Questions about architecture?** Review the [Developer Guide](DEVELOPER_GUIDE.md) for extension development details.
