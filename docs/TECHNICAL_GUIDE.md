# Technical Guide

Advanced usage guide for developers and technical users of the Data Validation Tool.

---

## Table of Contents

1. [Advanced Configuration](#advanced-configuration)
2. [Custom Validations](#custom-validations)
3. [Performance Tuning](#performance-tuning)
4. [Integration Patterns](#integration-patterns)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

---

## Advanced Configuration

### Multi-File Validation

Validate multiple files in a single job:

```yaml
validation_job:
  name: "Multi-File Validation"
  version: "1.0"

  files:
    # Customer master data
    - name: "customers"
      path: "data/customers.csv"
      format: "csv"
      validations:
        - type: "UniqueKeyCheck"
          severity: "ERROR"
          params:
            key_columns: ["customer_id"]

    # Transaction data
    - name: "transactions"
      path: "data/transactions.parquet"
      format: "parquet"
      validations:
        - type: "MandatoryFieldCheck"
          severity: "ERROR"
          params:
            field: "transaction_id"

    # Reference data
    - name: "products"
      path: "data/products.xlsx"
      format: "excel"
      params:
        sheet_name: "Product_Master"
      validations:
        - type: "EmptyFileCheck"
          severity: "ERROR"

  output:
    html_report: "multi_file_report.html"
    json_summary: "multi_file_summary.json"
```

### Custom Delimiters and Encoding

```yaml
files:
  - name: "pipe_delimited"
    path: "data/file.txt"
    format: "csv"
    params:
      delimiter: "|"
      encoding: "utf-8"

  - name: "tab_delimited"
    path: "data/file.tsv"
    format: "csv"
    params:
      delimiter: "\t"
      encoding: "latin1"
```

### Chunk Size Configuration

Adjust chunk size based on available memory:

```yaml
files:
  - name: "large_file"
    path: "data/200gb_file.csv"
    format: "csv"
    chunk_size: 100000  # 100k rows per chunk (higher = faster but more memory)

  - name: "medium_file"
    path: "data/10gb_file.csv"
    format: "csv"
    chunk_size: 50000   # 50k rows per chunk (default)
```

**Guidelines**:
- **Small files (<1GB)**: 100,000 - 200,000 rows
- **Medium files (1-50GB)**: 50,000 - 100,000 rows
- **Large files (>50GB)**: 20,000 - 50,000 rows
- Adjust based on available RAM and row width

### Complex Validation Combinations

Combine multiple validation types:

```yaml
validations:
  # Email must exist and be valid
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    params:
      field: "email"

  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "email"
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - type: "InlineLookupCheck"
    severity: "WARNING"
    params:
      field: "email_domain"
      check_type: "deny"
      reference_values: ["tempmail.com", "throwaway.email"]
```

---

## Custom Validations

### Creating a Custom Validation

**Example: Bank Account Number Validation**

```python
# validations/custom/bank_account_check.py

from typing import Iterator, Dict, Any
import pandas as pd
from validation_framework.validations.base import DataValidationRule
from validation_framework.core.results import ValidationResult

class BankAccountCheck(DataValidationRule):
    """
    Validates UK bank account numbers (8 digits).

    Parameters:
        field (str): Field containing account numbers
        allow_spaces (bool): Whether to allow spaces in numbers
    """

    def get_description(self) -> str:
        field = self.params.get("field", "unknown")
        return f"UK Bank Account validation for '{field}'"

    def validate(self, data_iterator: Iterator[pd.DataFrame],
                 context: Dict[str, Any]) -> ValidationResult:
        """
        Validate account numbers are 8 digits.
        """
        field = self.params.get("field")
        allow_spaces = self.params.get("allow_spaces", False)

        if not field:
            return self._create_result(
                passed=False,
                message="No field specified",
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
                account_str = str(value)

                # Remove spaces if allowed
                if allow_spaces:
                    account_str = account_str.replace(" ", "")

                # Check if 8 digits
                if not (account_str.isdigit() and len(account_str) == 8):
                    if len(failed_rows) < max_samples:
                        failed_rows.append({
                            "row": int(total_rows + idx),
                            "field": field,
                            "value": str(value),
                            "message": "Must be 8 digits"
                        })

            total_rows += len(chunk)

        if failed_rows:
            return self._create_result(
                passed=False,
                message=f"Found {len(failed_rows)} invalid account numbers",
                failed_count=len(failed_rows),
                total_count=total_rows,
                sample_failures=failed_rows
            )

        return self._create_result(
            passed=True,
            message=f"All {total_rows} account numbers valid",
            total_count=total_rows
        )
```

**Register the validation**:

```python
# validations/custom/__init__.py

from validation_framework.core.registry import register_validation
from .bank_account_check import BankAccountCheck

# Register so it can be used in YAML
register_validation("BankAccountCheck", BankAccountCheck)
```

**Use in YAML**:

```yaml
validations:
  - type: "BankAccountCheck"
    severity: "ERROR"
    params:
      field: "account_number"
      allow_spaces: false
```

### File-Level Custom Validation

For validations that don't need to process data:

```python
from validation_framework.validations.base import FileValidationRule
from validation_framework.core.results import ValidationResult
import os

class FilenamePatternCheck(FileValidationRule):
    """
    Validates filename matches expected pattern.

    Parameters:
        pattern (str): Regex pattern for filename
    """

    def get_description(self) -> str:
        return "Filename pattern validation"

    def validate(self, file_path: str, context: dict) -> ValidationResult:
        import re
        pattern = self.params.get("pattern")
        filename = os.path.basename(file_path)

        if re.match(pattern, filename):
            return self._create_result(
                passed=True,
                message=f"Filename '{filename}' matches pattern"
            )
        else:
            return self._create_result(
                passed=False,
                message=f"Filename '{filename}' doesn't match pattern '{pattern}'",
                failed_count=1
            )
```

---

## Performance Tuning

### Optimizing Chunk Size

**Benchmark different chunk sizes**:

```python
import time
import pandas as pd

def benchmark_chunk_size(file_path, chunk_sizes=[10000, 50000, 100000, 200000]):
    """Benchmark different chunk sizes."""
    results = {}

    for chunk_size in chunk_sizes:
        start = time.time()
        row_count = 0

        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            row_count += len(chunk)

        elapsed = time.time() - start
        results[chunk_size] = {
            'time': elapsed,
            'rows': row_count,
            'rows_per_sec': row_count / elapsed
        }

        print(f"Chunk size {chunk_size}: {elapsed:.2f}s ({row_count/elapsed:.0f} rows/sec)")

    return results

# Usage
benchmark_chunk_size("data/large_file.csv")
```

### Memory Profiling

**Track memory usage**:

```python
import tracemalloc
from validation_framework.core.engine import ValidationEngine
from validation_framework.core.config import ValidationConfig

# Start tracking
tracemalloc.start()

# Run validation
config = ValidationConfig.from_yaml("config.yaml")
engine = ValidationEngine(config)
report = engine.run()

# Get memory stats
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()
```

### Parquet for Large Files

Convert CSV to Parquet for better performance:

```python
import pandas as pd
import pyarrow.parquet as pq

def csv_to_parquet(csv_path, parquet_path, chunk_size=100000):
    """
    Convert large CSV to Parquet format.

    Parquet is columnar and compressed, much faster to read.
    """
    # Read CSV in chunks, write to Parquet
    first_chunk = True

    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        if first_chunk:
            # Write first chunk with schema
            chunk.to_parquet(parquet_path, engine='pyarrow', index=False)
            first_chunk = False
        else:
            # Append subsequent chunks
            chunk.to_parquet(parquet_path, engine='pyarrow', index=False,
                            append=True)

# Usage
csv_to_parquet("data/200gb_file.csv", "data/200gb_file.parquet")
```

**Performance comparison**:
- CSV (200GB): ~30 minutes to read
- Parquet (60GB compressed): ~5 minutes to read
- **6x faster** with Parquet!

---

## Integration Patterns

### CI/CD Integration

**GitHub Actions**:

```yaml
# .github/workflows/data-validation.yml

name: Data Validation

on:
  push:
    paths:
      - 'data/**'
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2am

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .

      - name: Run validation
        run: |
          data-validate validate config/production.yaml

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: validation-report
          path: validation_report.html

      - name: Check validation result
        run: |
          if [ -f validation_summary.json ]; then
            # Parse JSON and check status
            status=$(python -c "import json; print(json.load(open('validation_summary.json'))['overall_status'])")
            if [ "$status" != "PASSED" ]; then
              echo "Validation failed!"
              exit 1
            fi
          fi
```

**Jenkins Pipeline**:

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install -e .
                '''
            }
        }

        stage('Validate') {
            steps {
                sh '''
                    . venv/bin/activate
                    data-validate validate config/pipeline.yaml
                '''
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML([
                    reportDir: '.',
                    reportFiles: 'validation_report.html',
                    reportName: 'Data Validation Report'
                ])
            }
        }
    }

    post {
        failure {
            emailext(
                subject: "Data Validation Failed",
                body: "Check the validation report for details.",
                to: "team@example.com"
            )
        }
    }
}
```

### Apache Airflow Integration

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import subprocess

def run_data_validation(**context):
    """Run data validation as Airflow task."""
    result = subprocess.run(
        ['data-validate', 'validate', 'config/airflow.yaml'],
        capture_output=True,
        text=True
    )

    # Store return code in XCom
    context['task_instance'].xcom_push(key='validation_status',
                                       value=result.returncode)

    if result.returncode != 0:
        raise Exception(f"Validation failed: {result.stderr}")

    return "Validation passed"

def check_validation_status(**context):
    """Check if validation passed."""
    status = context['task_instance'].xcom_pull(
        task_ids='validate_data',
        key='validation_status'
    )

    return status == 0

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_validation_pipeline',
    default_args=default_args,
    description='Daily data validation',
    schedule_interval='0 2 * * *',  # 2am daily
    catchup=False,
)

validate_task = PythonOperator(
    task_id='validate_data',
    python_callable=run_data_validation,
    provide_context=True,
    dag=dag,
)

# Downstream tasks only run if validation passes
load_to_warehouse = PythonOperator(
    task_id='load_to_warehouse',
    python_callable=lambda: print("Loading to warehouse..."),
    dag=dag,
)

validate_task >> load_to_warehouse
```

### Python API Usage

```python
from validation_framework.core.engine import ValidationEngine
from validation_framework.core.config import ValidationConfig
from validation_framework.reporters.html_reporter import HTMLReporter
from validation_framework.reporters.json_reporter import JSONReporter

def validate_data_programmatically():
    """
    Use the validation framework programmatically.
    """
    # Load configuration
    config = ValidationConfig.from_yaml("config.yaml")

    # Customize configuration programmatically
    config.output_settings['html_report'] = "custom_report.html"

    # Run validation
    engine = ValidationEngine(config)
    report = engine.run(verbose=True)

    # Access results programmatically
    print(f"Overall status: {report.overall_status}")
    print(f"Total errors: {report.total_errors}")
    print(f"Total warnings: {report.total_warnings}")

    # Process each file
    for file_report in report.file_reports:
        print(f"\nFile: {file_report.file_name}")
        print(f"  Status: {file_report.status}")
        print(f"  Errors: {file_report.error_count}")

        # Check specific validations
        for result in file_report.validation_results:
            if not result.passed:
                print(f"  Failed: {result.rule_name} - {result.message}")

    # Generate custom reports
    html_reporter = HTMLReporter()
    html_reporter.generate(report, "custom_report.html")

    json_reporter = JSONReporter()
    json_reporter.generate(report, "custom_summary.json")

    # Return success/failure for integration
    return report.overall_status.value == "PASSED"

if __name__ == "__main__":
    success = validate_data_programmatically()
    exit(0 if success else 1)
```

---

## Troubleshooting

### Common Issues

#### Issue: Out of Memory Error

**Symptom**: Python crashes with `MemoryError` or system runs out of RAM.

**Solution**:
1. Reduce chunk size in configuration
2. Close other applications
3. Process files one at a time
4. Use Parquet format instead of CSV

```yaml
files:
  - name: "large_file"
    chunk_size: 20000  # Reduce from default 50000
```

#### Issue: Slow Performance

**Symptom**: Validation takes hours for large files.

**Solutions**:
1. Convert CSV to Parquet format
2. Increase chunk size (if memory allows)
3. Use SSD instead of HDD
4. Reduce number of validations

**Benchmark**:
```bash
# Time the validation
time data-validate validate config.yaml
```

#### Issue: Regex Pattern Not Matching

**Symptom**: All values fail regex validation when they look correct.

**Solutions**:
1. Test regex at https://regex101.com/
2. Remember to escape special characters with `\\`
3. Use raw strings in Python (but not needed in YAML)

**Common mistakes**:
```yaml
# Wrong - single backslash
pattern: "\d{3}-\d{2}-\d{4}"

# Correct - double backslash in YAML
pattern: "\\d{3}-\\d{2}-\\d{4}"
```

#### Issue: Missing Dependencies

**Symptom**: `ModuleNotFoundError` for pyarrow or openpyxl.

**Solution**:
```bash
# Install optional dependencies
pip install pyarrow      # For Parquet
pip install openpyxl     # For Excel
pip install colorama     # For colored output
```

### Debug Mode

Enable verbose logging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run validation
from validation_framework.core.engine import ValidationEngine
from validation_framework.core.config import ValidationConfig

config = ValidationConfig.from_yaml("config.yaml")
engine = ValidationEngine(config)
report = engine.run(verbose=True)
```

---

## Best Practices

### 1. Configuration Management

**Use version control for configs**:
```bash
git add config/production.yaml
git commit -m "Update validation rules"
```

**Environment-specific configs**:
```
config/
├── development.yaml
├── staging.yaml
└── production.yaml
```

### 2. Validation Strategy

**Fail fast with file-level checks**:
```yaml
validations:
  # Run these first
  - type: "EmptyFileCheck"
    severity: "ERROR"
  - type: "ColumnPresenceCheck"
    severity: "ERROR"

  # Then run data validations
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
```

**Use appropriate severity levels**:
- **ERROR**: Must fix before loading data
- **WARNING**: Should investigate but not blocking

### 3. Performance Optimization

**Order validations by cost**:
```yaml
# Cheap validations first
- type: "EmptyFileCheck"        # Fast
- type: "ColumnPresenceCheck"   # Fast
- type: "MandatoryFieldCheck"   # Medium
- type: "RegexCheck"            # Expensive
```

**Use sampling for exploratory analysis**:
```python
# Validate only first N rows
def validate_sample(file_path, n_rows=10000):
    """Quick validation of first N rows."""
    # Implementation
    pass
```

### 4. Report Management

**Organize reports by date**:
```yaml
output:
  html_report: "reports/validation_{{ date }}.html"
  json_summary: "reports/summary_{{ date }}.json"
```

**Archive old reports**:
```bash
# Keep last 30 days
find reports/ -name "*.html" -mtime +30 -delete
```

### 5. Error Handling

**Always check return codes in scripts**:
```bash
#!/bin/bash
data-validate validate config.yaml

if [ $? -ne 0 ]; then
    echo "Validation failed!"
    # Send alert
    # Don't load data
    exit 1
fi

echo "Validation passed, proceeding with data load"
# Load data to warehouse
```

---

## Advanced Topics

### Parallel File Processing

While not currently implemented, you can process files in parallel manually:

```python
from concurrent.futures import ProcessPoolExecutor
from validation_framework.core.engine import ValidationEngine
from validation_framework.core.config import ValidationConfig

def validate_file(file_config):
    """Validate a single file."""
    # Create config with single file
    config = ValidationConfig({
        'validation_job': {
            'name': f"Validation_{file_config['name']}",
            'files': [file_config],
            'output': {...}
        }
    })

    engine = ValidationEngine(config)
    return engine.run()

# Load all file configs
all_files = [...]  # Your file configs

# Process in parallel
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(validate_file, all_files))

# Aggregate results
```

### Custom Reporters

Create specialized report formats:

```python
from validation_framework.reporters.base import Reporter
import csv

class CSVReporter(Reporter):
    """Generate CSV report of failures."""

    def generate(self, report, output_path):
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['File', 'Validation', 'Severity', 'Status', 'Message'])

            for file_report in report.file_reports:
                for result in file_report.validation_results:
                    writer.writerow([
                        file_report.file_name,
                        result.rule_name,
                        result.severity.value,
                        'PASS' if result.passed else 'FAIL',
                        result.message
                    ])
```

---

## Next Steps

- **[Architecture Overview](ARCHITECTURE.md)** - Understand the system design
- **[API Reference](API_REFERENCE.md)** - Python API documentation
- **[Contributing](CONTRIBUTING.md)** - Extend the framework

---

**Questions or Issues?**

- [GitHub Issues](https://github.com/danieledge/data-validation-tool/issues)
- [Documentation](README.md)
