# Advanced Configuration Guide

**Complex configurations, custom checks, and advanced features**

This guide covers advanced topics for power users who need complex validation scenarios, custom checks, and performance optimization.

---

## Table of Contents

1. [Complex Conditional Logic](#complex-conditional-logic)
2. [Custom Validation Rules](#custom-validation-rules)
3. [Performance Optimization](#performance-optimization)
4. [Advanced File Handling](#advanced-file-handling)
5. [Integration Patterns](#integration-patterns)
6. [Error Handling](#error-handling)
7. [Logging and Debugging](#logging-and-debugging)
8. [Best Practices](#best-practices)

---

## Complex Conditional Logic

### Nested Conditions

Apply conditions at multiple levels:

```yaml
- type: "ConditionalValidation"
  severity: "ERROR"
  params:
    # Top-level condition: check country
    condition: "country == 'US'"
    then_validate:
      # US-specific validations
      - type: "MandatoryFieldCheck"
        params:
          fields: ["state", "zip_code", "ssn"]

      # Nested condition: extra checks for California
      - type: "MandatoryFieldCheck"
        condition: "state == 'CA'"
        params:
          fields: ["ca_tax_id"]

      # Nested condition: high-value customers
      - type: "RegexCheck"
        condition: "customer_value > 50000"
        params:
          field: "ssn"
          pattern: "^[0-9]{3}-[0-9]{2}-[0-9]{4}$"

    else_validate:
      # International customers
      - type: "MandatoryFieldCheck"
        params:
          fields: ["passport_number", "country_code"]
```

### Multiple Condition Branches

Chain conditions for complex business rules:

```yaml
# Payment processing rules
- type: "ConditionalValidation"
  severity: "ERROR"
  params:
    condition: "payment_method == 'CREDIT_CARD'"
    then_validate:
      - type: "MandatoryFieldCheck"
        params:
          fields: ["card_number", "expiry", "cvv"]
      - type: "RegexCheck"
        params:
          field: "card_number"
          pattern: "^[0-9]{16}$"

- type: "ConditionalValidation"
  severity: "ERROR"
  params:
    condition: "payment_method == 'BANK_TRANSFER'"
    then_validate:
      - type: "MandatoryFieldCheck"
        params:
          fields: ["bank_account", "routing_number", "bank_name"]

- type: "ConditionalValidation"
  severity: "ERROR"
  params:
    condition: "payment_method == 'PAYPAL'"
    then_validate:
      - type: "MandatoryFieldCheck"
        params:
          fields: ["paypal_email"]
      - type: "RegexCheck"
        params:
          field: "paypal_email"
          pattern: "^[^@]+@[^@]+\\.[^@]+$"
```

### Complex Condition Expressions

```yaml
# Multiple AND conditions
- type: "MandatoryFieldCheck"
  severity: "ERROR"
  params:
    fields: ["overnight_shipping_fee"]
  condition: "order_type == 'EXPRESS' AND order_total > 100 AND shipping_country == 'US'"

# Multiple OR conditions
- type: "RangeCheck"
  severity: "WARNING"
  params:
    field: "discount_percentage"
    max_value: 50
  condition: "customer_tier == 'GOLD' OR customer_tier == 'PLATINUM' OR customer_tier == 'DIAMOND'"

# Complex combinations
- type: "MandatoryFieldCheck"
  severity: "ERROR"
  params:
    fields: ["manager_approval"]
  condition: "(order_total > 10000 OR order_type == 'BULK') AND customer_tier != 'PLATINUM'"

# NOT operator
- type: "RangeCheck"
  severity: "ERROR"
  params:
    field: "standard_shipping_days"
    min_value: 5
    max_value: 10
  condition: "NOT (shipping_method == 'EXPRESS' OR shipping_method == 'OVERNIGHT')"
```

---

## Custom Validation Rules

### Creating Inline Business Rules

For simple custom logic, use `InlineBusinessRuleCheck`:

```yaml
# Custom business rule with pandas expression
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "total_price == unit_price * quantity"
    description: "Total price must equal unit price times quantity"
    error_message: "Price calculation mismatch"

# Multiple field validation
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "discount_amount < original_price"
    description: "Discount cannot exceed original price"

# Complex calculation
- type: "InlineBusinessRuleCheck"
  severity: "WARNING"
  params:
    rule: "(commission_rate >= 0.05) & (commission_rate <= 0.20)"
    description: "Commission rate should be between 5% and 20%"

# Date logic
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "ship_date >= order_date"
    description: "Ship date cannot be before order date"
```

### Custom Regex Patterns

Create reusable regex patterns:

```yaml
# Credit card validation (Luhn algorithm not included)
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "credit_card"
    pattern: "^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})$"
    description: "Visa, MasterCard, or Amex format"

# Complex email with domain restrictions
- type: "InlineRegexCheck"
  severity: "WARNING"
  params:
    field: "business_email"
    pattern: "^[a-zA-Z0-9._%+-]+@(?:company1\\.com|company2\\.com|company3\\.com)$"
    description: "Email must be from approved domains"

# Product SKU format
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "sku"
    pattern: "^[A-Z]{3}-[0-9]{4}-[A-Z]{2}$"
    description: "SKU format: AAA-9999-AA"
```

### Reference Data Lookups

Validate against reference data files:

```yaml
# Lookup validation against reference file
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "country_code"
    lookup_file: "reference_data/valid_countries.csv"
    lookup_field: "code"
    description: "Country code must exist in reference data"

# Multiple field lookup
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "product_category"
    lookup_file: "reference_data/product_catalog.csv"
    lookup_field: "category_id"
    description: "Product category must be in catalog"
```

### Writing Python Custom Validations

For complex logic requiring Python code, create a custom validation class:

**File:** `validation_framework/validations/custom/my_validation.py`

```python
"""
Custom validation for specific business logic.
"""
from typing import Iterator, Dict, Any
import pandas as pd
from validation_framework.validations.base import DataValidationRule, ValidationResult


class MyCustomValidation(DataValidationRule):
    """
    Custom validation with specific business logic.

    Configuration:
        params:
            threshold (float): Custom threshold value
            check_field (str): Field to check
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        field = self.params.get("check_field", "unknown")
        return f"Custom validation for field '{field}'"

    def validate(
        self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]
    ) -> ValidationResult:
        """
        Execute custom validation logic.

        Args:
            data_iterator: Iterator yielding data chunks
            context: Validation context

        Returns:
            ValidationResult with pass/fail status
        """
        try:
            threshold = self.params.get("threshold", 0.0)
            check_field = self.params.get("check_field")

            if not check_field:
                return self._create_result(
                    passed=False,
                    message="Missing required parameter 'check_field'",
                    failed_count=1,
                )

            total_rows = 0
            failed_rows = []
            max_samples = context.get("max_sample_failures", 100)

            # Process each chunk
            for chunk in data_iterator:
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

                    if len(rows_to_check) == 0:
                        total_rows += len(chunk)
                        continue
                else:
                    rows_to_check = chunk

                # Custom validation logic here
                for idx, value in rows_to_check[check_field].items():
                    # Example: check if value exceeds threshold
                    if pd.notna(value) and float(value) > threshold:
                        if len(failed_rows) < max_samples:
                            failed_rows.append({
                                "row": int(total_rows + idx),
                                "field": check_field,
                                "value": float(value),
                                "message": f"Value {value} exceeds threshold {threshold}"
                            })

                total_rows += len(chunk)

            # Create result
            failed_count = len(failed_rows)

            if failed_count > 0:
                return self._create_result(
                    passed=False,
                    message=f"Found {failed_count} rows exceeding threshold",
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
            return self._create_result(
                passed=False,
                message=f"Error in custom validation: {str(e)}",
                failed_count=1,
            )
```

**Register the custom validation:**

```python
# File: validation_framework/validations/custom/__init__.py
from validation_framework.core.registry import register_validation
from validation_framework.validations.custom.my_validation import MyCustomValidation

# Register validation
register_validation("MyCustomValidation", MyCustomValidation)
```

**Use in configuration:**

```yaml
validations:
  - type: "MyCustomValidation"
    severity: "WARNING"
    params:
      check_field: "custom_metric"
      threshold: 100.0
```

See **[Developer Guide](DEVELOPER_GUIDE.md)** for complete custom validation development instructions.

---

## Performance Optimization

### Chunk Size Tuning

Adjust chunk size based on data characteristics:

```yaml
settings:
  # Small files (<1MB) - larger chunks
  chunk_size: 10000

  # Medium files (1-100MB) - default
  chunk_size: 1000

  # Large files (>100MB) - smaller chunks
  chunk_size: 500

  # Very large files (>1GB) - very small chunks
  chunk_size: 100
```

**Rules of thumb:**
- More columns → smaller chunks
- Wider rows → smaller chunks
- More memory → larger chunks
- Complex validations → smaller chunks

### Limiting Sample Failures

Reduce memory usage and report size:

```yaml
settings:
  # Development: see more failures
  max_sample_failures: 500

  # Production: limit samples
  max_sample_failures: 50

  # High-volume: minimal samples
  max_sample_failures: 10
```

### Ordering Validations

Order validations by speed (fast first):

```yaml
validations:
  # 1. File-level checks (fastest - run once)
  - type: "EmptyFileCheck"
    severity: "ERROR"

  - type: "RowCountRangeCheck"
    severity: "WARNING"
    params:
      min_rows: 100

  # 2. Schema checks (fast - run once)
  - type: "ColumnPresenceCheck"
    severity: "ERROR"
    params:
      columns: ["id", "email"]

  # 3. Simple field checks (fast - per row, simple operations)
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    params:
      fields: ["id", "email", "name"]

  - type: "RangeCheck"
    severity: "WARNING"
    params:
      field: "age"
      min_value: 0
      max_value: 120

  # 4. Pattern checks (medium - per row, regex matching)
  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "email"
      pattern: "..."

  # 5. Duplicate checks (slower - requires collecting data)
  - type: "DuplicateRowCheck"
    severity: "ERROR"
    params:
      key_fields: ["id"]

  # 6. Statistical checks (slowest - require multiple passes)
  - type: "StatisticalOutlierCheck"
    severity: "WARNING"
    params:
      field: "amount"
    enabled: true  # Can disable during development
```

### Parallel Processing

Process multiple files in parallel:

```bash
# Run multiple validation jobs in parallel
python3 -m validation_framework.cli validate file1.yaml &
python3 -m validation_framework.cli validate file2.yaml &
python3 -m validation_framework.cli validate file3.yaml &
wait  # Wait for all to complete
```

Or use shell script:

```bash
#!/bin/bash
# parallel_validate.sh

configs=("customers.yaml" "orders.yaml" "products.yaml")

for config in "${configs[@]}"; do
    python3 -m validation_framework.cli validate "$config" --json "${config%.yaml}_results.json" &
done

wait
echo "All validations complete"
```

### Disabling Expensive Validations

Disable slow validations during development:

```yaml
# Full production validation
- type: "StatisticalOutlierCheck"
  severity: "WARNING"
  params:
    field: "amount"
  enabled: true  # Enable in production

# Quick development validation
- type: "StatisticalOutlierCheck"
  severity: "WARNING"
  params:
    field: "amount"
  enabled: false  # Disable during development
```

---

## Advanced File Handling

### Excel Multi-Sheet Validation

Validate multiple sheets in one workbook:

```yaml
files:
  # Sheet 1
  - name: "customers"
    path: "workbook.xlsx"
    format: "excel"
    sheet_name: "Customers"
    validations: [...]

  # Sheet 2
  - name: "orders"
    path: "workbook.xlsx"
    format: "excel"
    sheet_name: "Orders"
    validations: [...]

  # Sheet 3
  - name: "products"
    path: "workbook.xlsx"
    format: "excel"
    sheet_name: "Products"
    validations: [...]
```

### JSON Nested Structure Handling

Handle nested JSON with flattening:

```yaml
- name: "api_response"
  path: "response.json"
  format: "json"
  flatten: true  # Flatten nested structures

  validations:
    # Original nested: {"user": {"profile": {"email": "..."}}}
    # Flattened field: user_profile_email
    - type: "RegexCheck"
      severity: "ERROR"
      params:
        field: "user_profile_email"
        pattern: "..."

    # Original: {"order": {"items": [...]}}
    # Field: order_items (array flattened to JSON string)
    - type: "MandatoryFieldCheck"
      severity: "ERROR"
      params:
        fields: ["order_items", "order_total"]
```

### JSON Lines (JSONL) Processing

```yaml
- name: "log_data"
  path: "logs.jsonl"
  format: "json"
  lines: true  # JSON Lines format (one object per line)

  validations:
    - type: "MandatoryFieldCheck"
      severity: "ERROR"
      params:
        fields: ["timestamp", "level", "message"]
```

### Parquet with Partitions

```yaml
# Single Parquet file
- name: "analytics"
  path: "data/analytics.parquet"
  format: "parquet"
  validations: [...]

# Note: For partitioned Parquet, validate each partition separately
# or use data processing tools to combine partitions first
```

### Custom Delimiters

```yaml
# Pipe-delimited
- name: "pipe_data"
  path: "data.psv"
  format: "csv"
  delimiter: "|"

# Tab-delimited
- name: "tab_data"
  path: "data.tsv"
  format: "csv"
  delimiter: "\t"

# Semicolon-delimited (European CSV)
- name: "euro_data"
  path: "data.csv"
  format: "csv"
  delimiter: ";"
```

### Encoding Handling

```yaml
# UTF-8 (default)
- name: "modern_data"
  path: "data.csv"
  format: "csv"
  encoding: "utf-8"

# Latin-1 (legacy systems)
- name: "legacy_data"
  path: "legacy.csv"
  format: "csv"
  encoding: "latin-1"

# Windows encoding
- name: "windows_data"
  path: "windows.csv"
  format: "csv"
  encoding: "cp1252"
```

---

## Integration Patterns

### CI/CD Pipeline Integration

```yaml
# .github/workflows/data-validation.yml
name: Data Validation

on:
  push:
    paths:
      - 'data/**'
      - 'validation_configs/**'

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

      - name: Run validation
        run: |
          python3 -m validation_framework.cli validate \
            validation_configs/production.yaml \
            --json results.json

      - name: Check validation results
        run: |
          if [ $? -ne 0 ]; then
            echo "Validation failed!"
            exit 1
          fi

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: validation-results
          path: results.json
```

### Airflow DAG Integration

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def check_validation_results(**context):
    """Check if validation passed."""
    import json

    with open('/path/to/results.json', 'r') as f:
        results = json.load(f)

    if results['overall_status'] != 'PASSED':
        raise ValueError(f"Validation failed: {results['total_errors']} errors")

    return results['total_errors']

with DAG(
    'data_validation_pipeline',
    default_args={
        'owner': 'data-team',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Daily data validation',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Run validation
    validate_task = BashOperator(
        task_id='validate_data',
        bash_command='''
        python3 -m validation_framework.cli validate \
            /path/to/config.yaml \
            --json /path/to/results.json
        '''
    )

    # Check results
    check_results = PythonOperator(
        task_id='check_results',
        python_callable=check_validation_results,
        provide_context=True,
    )

    # Send alert if failed
    alert_task = BashOperator(
        task_id='send_alert',
        bash_command='echo "Validation failed!" | mail -s "Data Quality Alert" team@company.com',
        trigger_rule='one_failed',
    )

    validate_task >> check_results >> alert_task
```

### Scheduled Cron Jobs

```bash
# /etc/cron.d/data-validation

# Daily validation at 2 AM
0 2 * * * user cd /path/to/project && python3 -m validation_framework.cli validate daily_config.yaml --html /reports/$(date +\%Y\%m\%d)_report.html

# Hourly validation for real-time data
0 * * * * user cd /path/to/project && python3 -m validation_framework.cli validate hourly_config.yaml --json /results/$(date +\%Y\%m\%d_\%H00).json

# Weekly comprehensive validation
0 3 * * 0 user cd /path/to/project && python3 -m validation_framework.cli validate weekly_config.yaml --html /reports/weekly_$(date +\%Y\%W).html
```

### API Wrapper

Create an API endpoint for on-demand validation:

```python
# api.py
from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate_data():
    """API endpoint for data validation."""
    try:
        # Get config path from request
        config_path = request.json.get('config_path')
        output_path = f"/tmp/validation_{id(request)}.json"

        # Run validation
        result = subprocess.run([
            'python3', '-m', 'validation_framework.cli',
            'validate', config_path,
            '--json', output_path
        ], capture_output=True, text=True)

        # Read results
        with open(output_path, 'r') as f:
            validation_results = json.load(f)

        return jsonify({
            'success': result.returncode == 0,
            'results': validation_results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
```

---

## Error Handling

### Graceful Failure Handling

```yaml
# Configuration designed for robust error handling

files:
  - name: "critical_data"
    path: "data/critical.csv"
    format: "csv"

    validations:
      # File-level checks catch issues early
      - type: "EmptyFileCheck"
        severity: "ERROR"

      # Schema checks prevent field-not-found errors
      - type: "ColumnPresenceCheck"
        severity: "ERROR"
        params:
          columns: ["id", "email", "amount"]

      # Field validations with proper error handling
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["id", "email"]

      # Complex validations that might fail
      - type: "RegexCheck"
        severity: "WARNING"  # Use WARNING if not critical
        params:
          field: "email"
          pattern: "..."
```

### Validation Result Checking

```bash
#!/bin/bash
# validate_and_notify.sh

# Run validation
python3 -m validation_framework.cli validate config.yaml --json results.json

# Check exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Validation PASSED"
    # Continue with data processing
    ./process_data.sh
elif [ $EXIT_CODE -eq 1 ]; then
    echo "Validation FAILED - check results.json"
    # Send notification
    mail -s "Validation Failed" team@company.com < results.json
    exit 1
else
    echo "Validation ERROR - command failed"
    exit 2
fi
```

### Python Error Handling

```python
import subprocess
import json
import logging

def run_validation(config_path: str) -> dict:
    """
    Run validation and return results.

    Returns:
        dict: Validation results
    Raises:
        ValidationError: If validation fails
        RuntimeError: If command fails
    """
    try:
        result = subprocess.run([
            'python3', '-m', 'validation_framework.cli',
            'validate', config_path,
            '--json', 'results.json'
        ], capture_output=True, text=True, check=False)

        # Read results
        with open('results.json', 'r') as f:
            validation_results = json.load(f)

        # Check if validation passed
        if result.returncode == 1:
            logging.error(f"Validation failed: {validation_results['total_errors']} errors")
            raise ValidationError(
                f"Validation failed with {validation_results['total_errors']} errors",
                results=validation_results
            )

        if result.returncode != 0:
            logging.error(f"Command failed: {result.stderr}")
            raise RuntimeError(f"Validation command failed: {result.stderr}")

        return validation_results

    except FileNotFoundError:
        logging.error("results.json not found")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in results: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


class ValidationError(Exception):
    """Validation failed with errors."""
    def __init__(self, message, results=None):
        super().__init__(message)
        self.results = results
```

---

## Logging and Debugging

### Verbose Output

```bash
# Enable verbose logging
python3 -m validation_framework.cli validate config.yaml --verbose
```

### Log Files

Logs are written to `logs/` directory:

```bash
# View recent logs
tail -f logs/validation_framework.log

# Search logs
grep "ERROR" logs/validation_framework.log

# View specific validation logs
grep "MandatoryFieldCheck" logs/validation_framework.log
```

### Debug Configuration

Create a debug-specific config:

```yaml
# debug_config.yaml
validation_job:
  name: "Debug Validation"
  description: "Minimal config for debugging"

settings:
  chunk_size: 10  # Very small chunks for debugging
  max_sample_failures: 5  # Limited samples

files:
  - name: "test_data"
    path: "test_sample.csv"  # Small test file
    format: "csv"

    validations:
      # Test one validation at a time
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["id"]
```

### Python Debugging

Add logging to custom validations:

```python
import logging

logger = logging.getLogger(__name__)

class MyValidation(DataValidationRule):
    def validate(self, data_iterator, context):
        logger.debug("Starting MyValidation")
        logger.debug(f"Parameters: {self.params}")

        for chunk_idx, chunk in enumerate(data_iterator):
            logger.debug(f"Processing chunk {chunk_idx}, size: {len(chunk)}")

            # Validation logic...

            logger.debug(f"Chunk {chunk_idx} complete, failures: {len(failed_rows)}")

        logger.info(f"MyValidation complete: {failed_count} failures in {total_rows} rows")

        return result
```

---

## Best Practices

### 1. Environment-Specific Configurations

```yaml
# dev_config.yaml
settings:
  chunk_size: 100  # Small for fast iteration
  max_sample_failures: 10

files:
  - name: "customers"
    path: "test_data/customers_sample.csv"  # Small test file

# prod_config.yaml
settings:
  chunk_size: 5000  # Optimized for production
  max_sample_failures: 100

files:
  - name: "customers"
    path: "/data/production/customers.csv"  # Full production data
```

### 2. Configuration Templates

Create reusable templates:

```yaml
# templates/common_validations.yaml
common_customer_validations: &customer_validations
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    params:
      fields: ["id", "email", "name"]

  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "email"
      pattern: "^[^@]+@[^@]+\\.[^@]+$"

# Use template
files:
  - name: "customers"
    path: "customers.csv"
    format: "csv"
    validations: *customer_validations
```

### 3. Version Control

```bash
# Store configs in git
git add validation_configs/
git commit -m "Update customer validation rules"
git push

# Tag releases
git tag -a v1.0.0 -m "Production validation rules v1.0.0"
git push --tags
```

### 4. Documentation

Document your validations:

```yaml
validation_job:
  name: "Customer Master Data Validation"
  description: |
    Validates customer master data before loading to CRM.

    Business Rules:
    - All customers must have ID, email, name
    - Email must be valid format
    - Age must be 18-120
    - Account balance cannot be negative

    Contacts: data-team@company.com
    Last Updated: 2024-11-13

files:
  - name: "customers"
    path: "data/customers.csv"
    format: "csv"

    validations:
      # Rule 1: Required fields per business requirement BR-001
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["customer_id", "email", "name"]
        description: "BR-001: Customer record completeness"

      # Rule 2: Email format per compliance requirement CMP-042
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "email"
          pattern: "..."
        description: "CMP-042: Valid email format required"
```

### 5. Testing Validations

Test with known good and bad data:

```bash
# Good data - should pass
python3 -m validation_framework.cli validate config.yaml \
  --path-override "test_data/good_customers.csv"

# Bad data - should fail
python3 -m validation_framework.cli validate config.yaml \
  --path-override "test_data/bad_customers.csv"
```

### 6. Monitoring and Alerting

Track validation trends:

```python
# monitor.py
import json
import datetime

def track_validation_metrics(results_file):
    """Track validation metrics over time."""
    with open(results_file, 'r') as f:
        results = json.load(f)

    metrics = {
        'timestamp': datetime.datetime.now().isoformat(),
        'job_name': results['job_name'],
        'status': results['overall_status'],
        'total_errors': results['total_errors'],
        'total_warnings': results['total_warnings'],
        'duration_seconds': results['duration_seconds'],
    }

    # Write to metrics database or file
    with open('metrics.jsonl', 'a') as f:
        f.write(json.dumps(metrics) + '\n')

    # Alert if thresholds exceeded
    if results['total_errors'] > 100:
        send_alert("High error count detected")
```

---

## Next Steps

- **[Examples](EXAMPLES.md)** - Real-world validation scenarios
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Create custom validations
- **[Technical Architecture](TECHNICAL_ARCHITECTURE.md)** - System internals

---

**Questions?** Review the [User Guide](USER_GUIDE.md) or check [Technical Guide](TECHNICAL_GUIDE.md) for detailed documentation.
