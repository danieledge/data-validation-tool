# Handling Large Validation Reports

**Strategies for managing validation reports when processing millions of rows**

When validating very large datasets (millions of rows) with many failures, validation reports can become extremely large and difficult to manage. This guide provides strategies and configuration options to keep reports manageable while maintaining visibility into data quality issues.

---

## Table of Contents

1. [The Problem](#the-problem)
2. [Built-in Mitigation Features](#built-in-mitigation-features)
3. [Configuration Strategies](#configuration-strategies)
4. [Reporting Modes](#reporting-modes)
5. [External Failure Logging](#external-failure-logging)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## The Problem

### When Reports Become Too Large

**Scenario**: You're validating a 10 million row file and 2 million rows fail a validation check.

**Impact**:
- **Report file size**: Could be 1GB+ with all failure details
- **Memory usage**: Loading report in browser may fail
- **Processing time**: Generating report takes excessive time
- **Usability**: Impossible to review 2 million failures manually

### What You Actually Need

In practice, you rarely need to see every single failure. What you need is:

1. **Summary statistics**: How many failures, what percentage?
2. **Sample failures**: 10-100 examples to understand the pattern
3. **Actionable information**: What needs to be fixed?
4. **Trend data**: Is this getting better or worse?

---

## Built-in Mitigation Features

### Automatic Sample Limiting

**The framework automatically limits sample failures in reports:**

```python
# In validation_framework/core/results.py
def to_dict(self) -> dict:
    return {
        # ...
        "sample_failures": self.sample_failures[:10],  # Only 10 samples in report
        # ...
    }
```

**What this means:**
- Even if a validation collects 1,000 sample failures
- Only the first 10 are included in the JSON/HTML report
- Keeps report size manageable

### Failure Sample Collection Limits

**Most validations limit sample collection:**

```python
# In validation implementations
max_samples = 10
sample_failures = []

for chunk in data_iterator:
    if len(sample_failures) >= max_samples:
        break  # Stop collecting samples
    # ... collect samples
```

**Benefits:**
- Stops processing once enough samples are collected
- Doesn't waste time collecting unnecessary samples
- Reduces memory usage during validation

---

## Configuration Strategies

### Strategy 1: Adjust Chunk Size

**For datasets with many failures, use smaller chunks:**

```yaml
settings:
  chunk_size: 1000  # Smaller chunks = faster feedback
```

**Why this helps:**
- Validations can fail fast on first chunk
- Don't process entire file if first chunk fails
- Lower memory usage

### Strategy 2: Use Fail-Fast Mode

**Stop after first critical failure:**

```yaml
settings:
  fail_fast: true  # Stop on first ERROR
  chunk_size: 10000
```

**When to use:**
- Initial data quality checks
- Development/testing
- When first failure indicates systemic issue

**Implementation** (future feature - add to settings):
```python
# In engine, check after each validation
if fail_fast and result.severity == Severity.ERROR and not result.passed:
    break  # Stop processing
```

### Strategy 3: Conditional Validation

**Skip expensive validations if basics fail:**

```yaml
validations:
  # Run critical checks first
  - type: "EmptyFileCheck"
    severity: "ERROR"

  - type: "ColumnPresenceCheck"
    severity: "ERROR"
    params:
      columns: ["id", "amount"]

  # Only run expensive checks if basics pass
  - type: "ReferentialIntegrityCheck"
    severity: "ERROR"
    condition: "basic_checks_passed"  # Only if previous passed
    params:
      foreign_key: "customer_id"
      reference_file: "customers.csv"
      reference_key: "id"
```

### Strategy 4: Limit Sample Failures (Built-in)

**Reduce number of sample failures collected:**

```yaml
validation_job:
  name: "Large Dataset Validation"

  processing:
    chunk_size: 50000
    max_sample_failures: 10  # Collect max 10 samples per validation

files:
  - name: "large_file"
    path: "data.csv"
    validations:
      # ... your validations
```

**What this does:**
- Limits sample failure collection to 10 per validation
- Reduces memory usage
- Keeps reports small
- Default is 100 if not specified

**Recommended values:**
- `max_sample_failures: 5` - Minimal reports, fast
- `max_sample_failures: 10` - Standard (good for most cases)
- `max_sample_failures: 50` - Detailed analysis
- `max_sample_failures: 100` - Default, max recommended

### Strategy 5: Stratified Sampling

**For very large files, validate a sample:**

```bash
# Validate first 100k rows only
head -n 100001 large_file.csv > sample.csv
python3 -m validation_framework.cli validate config.yaml sample.csv
```

**Note**: Full sampling configuration is a future enhancement.

---

## Reporting Modes

### Mode 1: Summary Only (Recommended for Large Datasets)

**Generate reports with minimal detail:**

```yaml
reporting:
  mode: "summary"  # Only counts and percentages
  include_samples: false
  max_sample_failures: 0
```

**Report content:**
- Validation name and status
- Count of failures
- Success rate percentage
- NO sample failure details

**Best for:**
- Production monitoring
- Automated checks
- Dashboards

### Mode 2: Sample Mode (Default)

**Include representative samples:**

```yaml
reporting:
  mode: "detailed"
  include_samples: true
  max_sample_failures: 10  # Default
```

**Report content:**
- Full validation details
- Up to 10 sample failures per validation
- Enough to understand issues

**Best for:**
- Development
- Troubleshooting
- Manual review

### Mode 3: Full Detail Mode (Use Sparingly)

**Include all failure details (NOT recommended for large datasets):**

```yaml
reporting:
  mode: "full"
  include_samples: true
  max_sample_failures: 1000  # or -1 for unlimited
```

**⚠️ Warning:**
- Can create multi-GB reports
- May cause out-of-memory errors
- Only use for small datasets or targeted debugging

---

## External Failure Logging

### Strategy: Write Failures to Separate File

**For detailed failure analysis, write to dedicated failure file:**

```yaml
settings:
  failure_logging:
    enabled: true
    output_file: "failures_{date}.csv"
    max_rows: 10000  # Limit failure file size
```

**Benefits:**
- Keep main report small
- Detailed failures available separately
- Can process failures with other tools

### Implementation Pattern

```python
# Pseudo-code for validation with external logging
def validate(self, data_iterator, context):
    failure_file = context.get('failure_file')

    for chunk in data_iterator:
        # ... validation logic ...

        if failures_found:
            # Log to external file
            if failure_file:
                failures_df.to_csv(failure_file, mode='a', header=False)

            # Add limited samples to report
            sample_failures.extend(failures_df.head(10).to_dict('records'))
```

### Manual Approach

**Write failures during validation:**

```bash
# Run validation and extract failures
python3 -m validation_framework.cli validate config.yaml --json results.json

# Parse JSON and extract failures to CSV
python3 << EOF
import json
import pandas as pd

with open('results.json') as f:
    report = json.load(f)

all_failures = []
for file_report in report['file_reports']:
    for validation in file_report['validation_results']:
        if not validation['passed']:
            for failure in validation['sample_failures']:
                failure['validation'] = validation['rule_name']
                all_failures.append(failure)

df = pd.DataFrame(all_failures)
df.to_csv('validation_failures.csv', index=False)
print(f"Wrote {len(df)} failure samples to validation_failures.csv")
EOF
```

---

## Best Practices

### 1. Profile Before Validating

**Understand your data before running full validation:**

```bash
# Profile first to understand data quality
python3 -m validation_framework.cli profile large_file.csv --format html

# Review profile, then create targeted validations
```

**Benefits:**
- Know expected failure rates
- Set appropriate thresholds
- Avoid surprise massive failures

### 2. Incremental Validation

**Validate in stages:**

```yaml
# Stage 1: Critical structure checks
validation_job:
  name: "Stage 1 - Structure"
  files:
    - name: "data"
      path: "data.csv"
      validations:
        - type: "EmptyFileCheck"
          severity: "ERROR"
        - type: "ColumnPresenceCheck"
          severity: "ERROR"
          params:
            columns: ["id", "amount"]

# Stage 2: Data quality (only if Stage 1 passes)
# ... more detailed validations
```

**Benefits:**
- Fail fast on critical issues
- Don't waste time on detailed checks if basics fail
- Easier to identify root cause

### 3. Use Parquet Format

**For huge files, convert to Parquet first:**

```bash
# Convert CSV to Parquet
python3 << EOF
import pandas as pd
df = pd.read_csv('huge_file.csv', chunksize=100000)

first = True
for chunk in df:
    if first:
        chunk.to_parquet('huge_file.parquet', index=False)
        first = False
    else:
        chunk.to_parquet('huge_file.parquet', index=False, mode='append')
EOF

# Validate Parquet (10-100x faster)
python3 -m validation_framework.cli validate config.yaml huge_file.parquet
```

**Benefits:**
- 10-100x faster than CSV
- Lower memory usage
- Better for large datasets

### 4. Set Realistic Thresholds

**Don't expect perfection on massive datasets:**

```yaml
validations:
  # Allow some failures on huge datasets
  - type: "RegexCheck"
    severity: "WARNING"  # Not ERROR - some bad emails expected
    params:
      field: "email"
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  # Use percentage-based thresholds
  - type: "CompletenessCheck"
    severity: "ERROR"
    params:
      field: "phone_number"
      min_completeness_pct: 80  # Allow 20% missing
```

**Reality:**
- 10M rows with 1% failures = 100k failures
- Focus on keeping failure rate low, not zero

### 5. Automate Report Summarization

**Create summary reports for large validations:**

```bash
# Run validation
python3 -m validation_framework.cli validate config.yaml --json full_report.json

# Generate summary
python3 << EOF
import json

with open('full_report.json') as f:
    report = json.load(f)

print("Validation Summary")
print("=" * 50)
print(f"Status: {report['summary']['status']}")
print(f"Total Errors: {report['summary']['total_errors']}")
print(f"Total Warnings: {report['summary']['total_warnings']}")
print()

print("Failed Validations:")
for file_report in report['file_reports']:
    for validation in file_report['validation_results']:
        if not validation['passed']:
            print(f"  - {validation['rule_name']}: {validation['failed_count']} failures")
            print(f"    Success Rate: {validation['success_rate']}%")
EOF
```

### 6. Monitor Trends Over Time

**Track validation results to spot degradation:**

```bash
# Save validation metrics daily
DATE=$(date +%Y-%m-%d)
python3 -m validation_framework.cli validate config.yaml --json "results_${DATE}.json"

# Extract key metrics
jq '.summary | {date: "'$DATE'", errors: .total_errors, warnings: .total_warnings}' \
    results_${DATE}.json >> validation_metrics.jsonl

# Weekly review of trends
jq -s 'group_by(.date) | map({date: .[0].date, avg_errors: (map(.errors) | add / length)})' \
    validation_metrics.jsonl
```

---

## Troubleshooting

### Problem: Report File Too Large to Open

**Symptoms:**
- JSON file is >100MB
- Browser crashes loading HTML report
- JSON parsing fails

**Solutions:**

1. **Extract just the summary:**
   ```bash
   jq '.summary' huge_report.json > summary.json
   ```

2. **Count failures by validation:**
   ```bash
   jq '.file_reports[].validation_results[] | select(.passed == false) | {rule: .rule_name, failures: .failed_count}' huge_report.json
   ```

3. **Get top 10 failure types:**
   ```bash
   jq '.file_reports[].validation_results[] | select(.passed == false) | {rule: .rule_name, failures: .failed_count}' huge_report.json | \
       jq -s 'sort_by(.failures) | reverse | .[0:10]'
   ```

### Problem: Validation Takes Too Long

**Symptoms:**
- Validation runs for hours
- Memory usage keeps growing
- Process seems stuck

**Solutions:**

1. **Test on sample first:**
   ```bash
   head -n 10001 data.csv > sample.csv  # 10k rows
   python3 -m validation_framework.cli validate config.yaml sample.csv
   ```

2. **Use larger chunks:**
   ```yaml
   settings:
     chunk_size: 100000  # Larger chunks = fewer iterations
   ```

3. **Reduce cross-file validations:**
   - Cross-file checks are slowest
   - Consider running separately
   - Or limit to critical relationships only

4. **Profile the validation:**
   ```bash
   python3 -m cProfile -o validation.prof \
       -m validation_framework.cli validate config.yaml

   python3 << EOF
   import pstats
   p = pstats.Stats('validation.prof')
   p.sort_stats('cumulative').print_stats(20)
   EOF
   ```

### Problem: Out of Memory Errors

**Symptoms:**
- `MemoryError` exception
- Process killed by OS
- Validation stops midway

**Solutions:**

1. **Reduce chunk size:**
   ```yaml
   settings:
     chunk_size: 1000  # Much smaller chunks
   ```

2. **Process file in batches:**
   ```bash
   # Split large file
   split -l 1000000 huge_file.csv part_

   # Validate each part
   for part in part_*; do
       python3 -m validation_framework.cli validate config.yaml $part \
           --json ${part}_results.json
   done

   # Combine results
   python3 combine_reports.py part_*_results.json > combined_report.json
   ```

3. **Disable sample collection:**
   ```python
   # In validation implementation
   max_samples = 0  # Don't collect samples
   ```

---

## Future Enhancements

These features are planned to better handle large reports:

### 1. Report Streaming

**Write report incrementally during validation:**

```yaml
settings:
  streaming_report: true
  report_path: "results.jsonl"  # JSON Lines format
```

**Benefits:**
- No need to store entire report in memory
- Can monitor progress in real-time
- Process report with streaming tools

### 2. Database Backend

**Store validation results in database:**

```yaml
settings:
  result_backend: "sqlite"
  result_db: "validation_results.db"
```

**Benefits:**
- Query results with SQL
- No file size limits
- Historical analysis built-in

### 3. Configurable Sample Sizes

**Per-validation sample limits:**

```yaml
validations:
  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "email"
      pattern: "..."
      max_samples: 5  # Only collect 5 samples
```

### 4. Smart Sampling

**Collect diverse samples, not just first N:**

- Random sampling across chunks
- Stratified sampling by error type
- Representative failure examples

---

## Summary

### Quick Reference

**For datasets with <1M rows:**
- Use default settings
- Include sample failures (10 per validation)
- HTML reports work fine

**For datasets with 1M-10M rows:**
- Increase chunk size to 50k-100k
- Use Parquet format if possible
- Monitor report size, switch to summary mode if needed

**For datasets with >10M rows:**
- Use summary-only reports
- Write failures to external file if needed
- Consider sampling for expensive validations
- Use Parquet format
- Profile before full validation

**For datasets with high failure rates (>1%):**
- Focus on fixing data source
- Use WARNING instead of ERROR where appropriate
- Collect minimal samples (5-10)
- Monitor trends over time

---

## Next Steps

- **[Best Practices](BEST_PRACTICES.md)** - General validation best practices
- **[Advanced Guide](ADVANCED_CONFIGURATION.md)** - Performance optimization
- **[User Guide](USER_GUIDE.md)** - Configuration reference

---

**Questions or suggestions?** [Open an issue](https://github.com/danieledge/data-validation-tool/issues) to discuss improvements!
