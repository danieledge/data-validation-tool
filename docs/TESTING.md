# Testing Guide

**Comprehensive guide to the data validation framework test suite**

This document covers the testing infrastructure, test organization, how to run tests, and guidelines for writing new tests.

---

## Table of Contents

1. [Test Suite Overview](#test-suite-overview)
2. [Running Tests](#running-tests)
3. [Test Organization](#test-organization)
4. [Test Coverage](#test-coverage)
5. [Writing New Tests](#writing-new-tests)
6. [Test Data Management](#test-data-management)
7. [CI/CD Integration](#cicd-integration)
8. [Troubleshooting](#troubleshooting)

---

## Test Suite Overview

### Statistics

- **Total Tests**: 115+
- **Test Files**: 4 main test modules
- **Coverage Target**: 43%
- **Current Coverage**: 48%
- **Testing Framework**: pytest

### Test Categories

| Category | Test File | Tests | Focus |
|----------|-----------|-------|-------|
| **Cross-File Validations** | `test_cross_file_validations.py` | 13 | Foreign key relationships, cross-file comparisons, duplicate detection |
| **Profiler** | `test_profiler.py` | 49 | Type detection, statistics, quality metrics, HTML reports |
| **File Checks** | `test_file_checks.py` | ~30 | Empty file, row count, file size validations |
| **Integration** | `test_integration.py` | ~23 | End-to-end validation workflows |

### Key Features Tested

- ✅ File-level validations (empty file, row count, file size)
- ✅ Schema validations (column presence, schema matching)
- ✅ Field-level validations (mandatory fields, regex, valid values, ranges)
- ✅ Record-level validations (duplicates, blank records, unique keys)
- ✅ Cross-file validations (referential integrity, comparisons, duplicates)
- ✅ Data profiling (type inference, statistics, quality metrics)
- ✅ HTML report generation
- ✅ Configuration loading and parsing
- ✅ Chunked data processing

---

## Running Tests

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with detailed output and show print statements
pytest -vv -s
```

### Run Specific Test Files

```bash
# Run cross-file validation tests
pytest tests/test_cross_file_validations.py -v

# Run profiler tests
pytest tests/test_profiler.py -v

# Run file check tests
pytest tests/test_file_checks.py -v

# Run integration tests
pytest tests/test_integration.py -v
```

### Run Specific Test Classes

```bash
# Run specific test class
pytest tests/test_profiler.py::TestTypeDetection -v

# Run specific test method
pytest tests/test_profiler.py::TestTypeDetection::test_detect_integer -v
```

### Run Tests with Coverage

```bash
# Run all tests with coverage report
pytest --cov=validation_framework --cov-report=html

# Open coverage report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Tests with Specific Markers

```bash
# Run only fast tests
pytest -m fast

# Run only slow tests
pytest -m slow

# Run tests that don't require external dependencies
pytest -m "not external"
```

### Run Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests using 4 parallel workers
pytest -n 4
```

---

## Test Organization

### Directory Structure

```
tests/
├── __init__.py
├── conftest.py                         # Pytest configuration and fixtures
├── test_cross_file_validations.py     # Cross-file validation tests
├── test_profiler.py                   # Data profiler tests
├── test_file_checks.py                # File-level validation tests
├── test_integration.py                # End-to-end integration tests
└── test_data/                         # Test data files
    ├── cross_file/
    │   ├── customers.csv
    │   ├── orders.csv
    │   └── historical_counts.csv
    ├── sample_data.csv
    ├── large_sample.csv
    └── test_config.yaml
```

### Test File Structure

Each test file follows a consistent structure:

```python
"""
Module docstring describing what is being tested.

Tests cover:
- Feature 1
- Feature 2
- Feature 3
"""

import pytest
# ... other imports ...


class TestFeatureGroup:
    """Test a specific feature group."""

    def setup_method(self):
        """Setup fixtures for each test."""
        # Initialize test data, profilers, validators, etc.

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up temp files, close connections, etc.

    def test_specific_behavior(self):
        """Test a specific behavior."""
        # Arrange: Setup test data
        # Act: Execute the code being tested
        # Assert: Verify expected behavior
```

---

## Test Coverage

### Current Coverage by Module

```
Module                                              Coverage
─────────────────────────────────────────────────────────────
validation_framework/profiler/engine.py                 94%
validation_framework/profiler/html_reporter.py          82%
validation_framework/profiler/profile_result.py         90%
validation_framework/core/registry.py                   68%
validation_framework/core/results.py                    67%
validation_framework/loaders/factory.py                 61%
validation_framework/validations/builtin/registry.py   100%
validation_framework/validations/base.py                44%
validation_framework/core/config.py                     23%
validation_framework/core/engine.py                     22%
─────────────────────────────────────────────────────────────
Overall                                                 48%
```

### Coverage Goals

- **Critical Modules**: 80%+ coverage
  - Profiler engine
  - Validation registry
  - Core results
  - All validation implementations

- **Important Modules**: 60%+ coverage
  - Configuration parsing
  - Loaders
  - Report generators

- **Overall Target**: 43%+ (currently at 48%)

### Generating Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=validation_framework --cov-report=html

# Generate terminal coverage report
pytest --cov=validation_framework --cov-report=term

# Generate XML coverage report (for CI/CD)
pytest --cov=validation_framework --cov-report=xml

# Fail if coverage drops below threshold
pytest --cov=validation_framework --cov-fail-under=43
```

---

## Writing New Tests

### Test Naming Conventions

```python
# Test files: test_<module_name>.py
test_field_checks.py
test_database_validations.py

# Test classes: Test<FeatureName>
class TestRangeCheck:
class TestDatabaseConnectivity:

# Test methods: test_<specific_behavior>
def test_valid_range_passes():
def test_invalid_range_fails():
def test_null_handling_with_allow_null_true():
```

### Test Structure (AAA Pattern)

```python
def test_referential_integrity_with_valid_keys(self):
    """Test that valid foreign keys pass referential integrity check."""
    # Arrange: Setup test data
    data = pd.DataFrame({'customer_id': [1, 2, 3]})
    context = {'file_path': 'test_orders.csv'}
    validation = ReferentialIntegrityCheck(
        name="test",
        severity=Severity.ERROR,
        params={
            'foreign_key': 'customer_id',
            'reference_file': 'customers.csv',
            'reference_key': 'id'
        }
    )

    # Act: Execute the validation
    result = validation.validate(iter([data]), context)

    # Assert: Verify expected behavior
    assert result.passed is True
    assert result.failed_count == 0
    assert result.total_checked == 3
```

### Using Fixtures

**Define fixtures in conftest.py:**

```python
# tests/conftest.py
import pytest
import pandas as pd
import tempfile
import os

@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file."""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test.csv")

    df = pd.DataFrame({
        'id': [1, 2, 3],
        'value': [10, 20, 30]
    })
    df.to_csv(file_path, index=False)

    yield file_path

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_validation_config():
    """Provide sample validation configuration."""
    return {
        "validation_job": {
            "name": "Test Job"
        },
        "settings": {
            "chunk_size": 1000
        },
        "files": [
            {
                "name": "test_file",
                "path": "test.csv",
                "format": "csv",
                "validations": []
            }
        ]
    }
```

**Use fixtures in tests:**

```python
def test_csv_loader(temp_csv_file):
    """Test CSV loader with temporary file."""
    loader = CSVLoader(temp_csv_file)
    data = next(loader.load())
    assert len(data) == 3
    assert "id" in data.columns
```

### Parameterized Tests

```python
@pytest.mark.parametrize("input_value,expected_type", [
    (42, "integer"),
    (3.14, "float"),
    ("hello", "string"),
    (True, "boolean"),
    ("2025-01-13", "date"),
    (None, "null")
])
def test_type_detection(profiler, input_value, expected_type):
    """Test type detection with various input types."""
    assert profiler._detect_type(input_value) == expected_type
```

### Testing Exceptions

```python
def test_missing_required_param_raises_error():
    """Test that missing required parameter raises ValueError."""
    with pytest.raises(ValueError, match="foreign_key is required"):
        validation = ReferentialIntegrityCheck(
            name="test",
            severity=Severity.ERROR,
            params={}  # Missing required params
        )
        validation.validate(iter([pd.DataFrame()]), {})
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

def test_database_connection_failure():
    """Test handling of database connection failure."""
    with patch('sqlalchemy.create_engine') as mock_engine:
        # Setup mock to raise exception
        mock_engine.side_effect = Exception("Connection failed")

        # Test that error is handled gracefully
        with pytest.raises(Exception, match="Connection failed"):
            loader = DatabaseLoader("postgresql://...")
            list(loader.load())
```

### Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_async_validation():
    """Test asynchronous validation."""
    result = await async_validate_data()
    assert result.passed is True
```

---

## Test Data Management

### Test Data Location

All test data files are stored in `tests/test_data/`:

```
tests/test_data/
├── cross_file/          # Cross-file validation test data
│   ├── customers.csv
│   ├── orders.csv
│   └── historical_counts.csv
├── sample_data.csv      # General purpose test data
├── large_sample.csv     # Large dataset for performance testing
└── configs/             # Test configuration files
    ├── simple.yaml
    └── complex.yaml
```

### Creating Test Data

**In-memory test data (preferred for unit tests):**

```python
def test_with_inmemory_data():
    """Test using in-memory DataFrame."""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    })
    # Use df for testing...
```

**Temporary file test data (for integration tests):**

```python
import tempfile
import os

def test_with_temp_file():
    """Test using temporary file."""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test.csv")

    df = pd.DataFrame({'id': [1, 2, 3]})
    df.to_csv(file_path, index=False)

    # Use file_path for testing...

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
```

**Permanent test data (for regression tests):**

```python
def test_with_fixture_data():
    """Test using permanent test data file."""
    test_file = "tests/test_data/sample_data.csv"
    df = pd.read_csv(test_file)
    # Use df for testing...
```

### Test Data Guidelines

1. **Keep test data small**: Use minimal data to test specific behavior
2. **Use descriptive names**: Make it clear what the test data represents
3. **Document edge cases**: Include comments explaining why specific values were chosen
4. **Version control**: Commit small test data files to git
5. **Generate large data**: For performance tests, generate data programmatically

---

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests with coverage
      run: |
        pytest --cov=validation_framework --cov-report=xml --cov-fail-under=43

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

### Pre-commit Hooks

```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

---

## Troubleshooting

### Common Issues

#### Issue: Tests fail with "Module not found"

**Solution**:

```bash
# Ensure you're in the project root directory
cd /path/to/data-validation-tool

# Install package in development mode
pip install -e .

# Or run tests with PYTHONPATH
PYTHONPATH=. pytest
```

#### Issue: Tests pass locally but fail in CI

**Possible causes**:
- Different Python version
- Missing test data files
- Different dependency versions
- Hardcoded file paths

**Solution**:

```bash
# Check Python version
python --version

# Ensure test data is committed
git add tests/test_data/

# Use relative paths
test_file = os.path.join(os.path.dirname(__file__), "test_data", "sample.csv")

# Pin dependency versions in requirements-dev.txt
```

#### Issue: Coverage drops unexpectedly

**Solution**:

```bash
# Generate detailed coverage report to identify untested code
pytest --cov=validation_framework --cov-report=html

# Open report to see which lines aren't covered
open htmlcov/index.html

# Add tests for uncovered lines
```

#### Issue: Tests are slow

**Solution**:

```bash
# Profile test execution time
pytest --durations=10

# Run tests in parallel
pip install pytest-xdist
pytest -n 4

# Mark slow tests and skip them for quick runs
pytest -m "not slow"
```

#### Issue: Temp files not cleaned up

**Solution**:

```python
import tempfile
import shutil

def test_with_proper_cleanup():
    """Test with guaranteed cleanup."""
    temp_dir = tempfile.mkdtemp()

    try:
        # Run test
        file_path = os.path.join(temp_dir, "test.csv")
        # ... test code ...
    finally:
        # Always cleanup, even if test fails
        shutil.rmtree(temp_dir)
```

---

## Best Practices

### 1. One Assertion Per Test (When Possible)

```python
# Good: Focused test
def test_validation_passes_with_valid_data():
    result = validation.validate(valid_data, context)
    assert result.passed is True

def test_validation_counts_failures_correctly():
    result = validation.validate(invalid_data, context)
    assert result.failed_count == 2

# Acceptable: Related assertions
def test_validation_result_structure():
    result = validation.validate(data, context)
    assert result.passed is False
    assert result.failed_count == 2
    assert len(result.sample_failures) == 2
```

### 2. Use Descriptive Test Names

```python
# Good
def test_referential_integrity_fails_when_foreign_key_not_in_reference():
def test_null_foreign_keys_allowed_when_allow_null_is_true():

# Bad
def test_validation():
def test_case_1():
```

### 3. Test Edge Cases

```python
def test_empty_dataframe():
    """Test with empty DataFrame."""

def test_single_row():
    """Test with single row."""

def test_all_nulls():
    """Test with all null values."""

def test_large_dataset():
    """Test with 1M+ rows."""
```

### 4. Keep Tests Independent

```python
# Good: Each test is independent
class TestValidation:
    def setup_method(self):
        self.data = create_test_data()

    def test_case_1(self):
        # Uses fresh data from setup_method

    def test_case_2(self):
        # Uses fresh data from setup_method

# Bad: Tests depend on each other
class TestValidation:
    data = None

    def test_setup(self):
        self.data = create_test_data()

    def test_validation(self):
        # Depends on test_setup running first
```

### 5. Use pytest Markers

```python
import pytest

@pytest.mark.slow
def test_large_file_processing():
    """Test that takes >5 seconds."""

@pytest.mark.integration
def test_end_to_end_validation():
    """Integration test."""

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Placeholder for future test."""
```

---

## Next Steps

- **[Developer Guide](DEVELOPER_GUIDE.md)** - Learn how to extend the framework
- **[Best Practices](BEST_PRACTICES.md)** - Validation best practices
- **[User Guide](USER_GUIDE.md)** - Configuration and usage

---

## Additional Resources

### Pytest Documentation

- [Official Pytest Docs](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Parametrize](https://docs.pytest.org/en/stable/parametrize.html)

### Testing Best Practices

- [Test-Driven Development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)
- [AAA Pattern](https://xp123.com/articles/3a-arrange-act-assert/)
- [FIRST Principles](https://github.com/tekguard/Principles-of-Unit-Testing)

---

**Questions or suggestions?** [Open an issue](https://github.com/danieledge/data-validation-tool/issues) to discuss testing improvements!
