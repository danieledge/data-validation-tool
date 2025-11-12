# Getting Started with Data Validation Framework

## Quick Start

### 1. Generate Sample Data

```bash
cd data-validation-tool
python3 examples/generate_sample_data.py
```

This creates sample datasets with intentional data quality issues in `examples/sample_data/`:
- `customers.csv` - 1000+ customer records with ~10% data quality issues
- `transactions.csv` - 5000 transaction records with various issues
- `accounts.csv` - 500 account records with invalid account numbers

### 2. Run Validation

```bash
python3 test_validation.py
```

This will:
- Load the configuration from `examples/sample_config.yaml`
- Execute all validations defined in the config
- Generate reports in `examples/`:
  - `validation_report.html` - Interactive HTML report
  - `validation_summary.json` - Machine-readable JSON summary

### 3. View Results

Open `examples/validation_report.html` in your browser to see:
- Overall validation status
- Per-file validation results
- Detailed failure samples
- Statistics and metrics

## Installation (Optional)

For full CLI support:

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
cd data-validation-tool
pip install -e .

# Now you can use the CLI
data-validate validate examples/sample_config.yaml
data-validate list-validations
data-validate init-config my_config.yaml
```

## Test Results

The sample data validation should detect approximately:
- **8 Critical Errors**
- **5 Warnings**

### Detected Issues Include:
- Missing mandatory fields (~10-50 rows per file)
- Invalid email formats (~30 invalid emails)
- Invalid phone formats (~50 invalid phones)
- Duplicate customer IDs (~20 duplicates)
- Invalid status values (~20 invalid)
- Out of range balances (~20-30 transactions)
- Invalid date formats (~20 dates)
- Blank rows (~20 blank records)
- Invalid account numbers (~50 invalid formats)

## Customizing Validations

### Edit Configuration

Modify `examples/sample_config.yaml` to:
- Add/remove validation rules
- Change severity levels (ERROR vs WARNING)
- Adjust validation parameters
- Add new files to validate

### Example: Add Email Validation

```yaml
- type: "RegexCheck"
  severity: "ERROR"
  params:
    field: "email"
    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    message: "Invalid email format"
```

## Working with Real Data

### 1. Prepare Your Data Files

Place your CSV, Excel, or Parquet files in a directory:

```
my-data/
  customers.csv
  transactions.parquet
  accounts.xlsx
```

### 2. Create Configuration

```bash
# Generate template
python3 -m validation_framework.cli init-config my_validation.yaml

# Edit the configuration
# - Update file paths
# - Define expected schema
# - Add validation rules
```

### 3. Run Validation

```bash
python3 test_validation.py  # Or use CLI if installed
```

### 4. Review Results

- Open the HTML report for visual review
- Check JSON summary for programmatic processing
- Address failures and re-run validation

## Large File Support (200GB+)

The framework is optimized for large datasets:

### Configuration for Large Files

```yaml
processing:
  chunk_size: 100000        # Increase for more memory/better performance
  max_sample_failures: 50   # Limit samples to reduce report size
```

### Best Practices

1. **Use Parquet Format**: Much faster than CSV for large files
2. **Increase Chunk Size**: More memory but better performance
3. **Run Critical Validations First**: Use `enabled: false` for non-critical checks
4. **Monitor Memory**: Adjust chunk_size based on available RAM

### Example: 200GB File

```yaml
files:
  - name: "large_transactions"
    path: "/data/transactions_200gb.parquet"
    format: "parquet"

    validations:
      # Essential checks only for large files
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["transaction_id", "amount"]

      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["transaction_id"]

processing:
  chunk_size: 200000  # Process 200K rows at a time
  max_sample_failures: 100
```

## Integration with Pipelines

### Exit Codes

- `0` - Validation passed
- `1` - Critical errors found
- `2` - Warnings found (with `--fail-on-warning`)

### Bash Integration

```bash
#!/bin/bash

# Run validation
python3 test_validation.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Validation passed - proceeding with data load"
    ./load_data.sh
else
    echo "✗ Validation failed with code $EXIT_CODE"
    exit $EXIT_CODE
fi
```

### Airflow Integration

```python
from airflow import DAG
from airflow.operators.bash import BashOperator

validate_task = BashOperator(
    task_id='validate_data',
    bash_command='python3 /path/to/test_validation.py',
    dag=dag
)

load_task = BashOperator(
    task_id='load_data',
    bash_command='./load_data.sh',
    dag=dag
)

validate_task >> load_task  # Load only if validation passes
```

## Testing with Real Financial Data

See `docs/test_datasets.md` for open-source financial datasets:

### Recommended: IBM AML Data

1. Download from Kaggle: https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml

2. Create configuration for the dataset

3. Run validation to detect:
   - Missing transaction IDs
   - Invalid amounts
   - Duplicate transactions
   - Schema conformance

## Need Help?

- **Documentation**: See `README.md` for complete feature list
- **Examples**: Check `examples/` directory for sample configs
- **Custom Validations**: See `examples/custom_validations/` for examples
- **Issues**: Report problems on project repository

## Next Steps

1. ✅ Test with sample data (completed)
2. Create configuration for your real data
3. Run validation on subset of your data
4. Review and adjust validation rules
5. Integrate into your data pipeline
6. Monitor validation results over time

## Author

daniel edge
