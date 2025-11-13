# Data Profiling Guide

**Comprehensive Data Analysis and Quality Assessment**

Data profiling is a powerful feature that analyzes your data files to understand their structure, quality, and characteristics. Use profiling before creating validations to make data-driven decisions about what checks to implement.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [What Does Profiling Analyze?](#what-does-profiling-analyze)
4. [Using the Profile Command](#using-the-profile-command)
5. [Understanding Profile Reports](#understanding-profile-reports)
6. [Type Inference: Known vs Inferred](#type-inference-known-vs-inferred)
7. [Quality Metrics Explained](#quality-metrics-explained)
8. [Auto-Generated Validations](#auto-generated-validations)
9. [Profiling Large Files](#profiling-large-files)
10. [Best Practices](#best-practices)

---

## Overview

Data profiling provides a comprehensive analysis of your data including:

- **Schema Discovery**: Automatic detection of data types with confidence levels
- **Statistical Analysis**: Distributions, ranges, means, medians, correlations
- **Quality Assessment**: Completeness, validity, consistency, uniqueness scores
- **Pattern Detection**: Common patterns in string data
- **Validation Suggestions**: Recommended checks based on actual data
- **Config Generation**: Ready-to-use YAML configuration file

### When to Use Profiling

✅ **Before implementing validations** - Understand your data first
✅ **When documenting datasets** - Generate comprehensive data dictionaries
✅ **During data analysis** - Discover patterns and anomalies
✅ **For quality assessment** - Measure data quality objectively
✅ **When troubleshooting** - Investigate data quality issues

---

## Quick Start

### Basic Usage

```bash
# Profile a CSV file
python3 -m validation_framework.cli profile data/customers.csv

# Output:
# ✅ HTML report generated: customers_profile_report.html
# ✅ Validation config saved: customers_validation.yaml
```

The profiler auto-generates three files:

1. **HTML Report** (`*_profile_report.html`) - Interactive visual report
2. **Validation Config** (`*_validation.yaml`) - Ready-to-use YAML configuration
3. **JSON Export** (optional) - Machine-readable profile data

### Custom Output Paths

```bash
python3 -m validation_framework.cli profile data.csv \
  -o my_profile.html \
  -c my_validation.yaml \
  -j profile_data.json
```

### Format Detection

The profiler auto-detects file format from extension:

```bash
# Automatically detected formats
python3 -m validation_framework.cli profile data.csv      # CSV
python3 -m validation_framework.cli profile data.xlsx     # Excel
python3 -m validation_framework.cli profile data.json     # JSON
python3 -m validation_framework.cli profile data.parquet  # Parquet

# Explicit format specification
python3 -m validation_framework.cli profile data.txt --format csv
```

---

## What Does Profiling Analyze?

### File-Level Analysis

- **File size** and format
- **Row count** - Total records in dataset
- **Column count** - Number of fields
- **Processing time** - Analysis duration
- **Overall quality score** - Aggregate quality assessment (0-100%)

### Column-Level Analysis

For each column, profiling analyzes:

#### 1. Type Information
- **Declared type** (if schema provided)
- **Inferred type** from actual data
- **Confidence level** (0-100%)
- **Known vs Inferred** indicator
- **Type conflicts** - When data doesn't match inferred type

#### 2. Statistical Measures
- **Count** - Total values
- **Null count** - Missing values
- **Null percentage** - Completeness indicator
- **Unique count** - Distinct values
- **Cardinality** - Ratio of unique to total values

For numeric fields:
- **Min/Max** - Value range
- **Mean** - Average value
- **Median** - Middle value
- **Standard deviation** - Spread of values
- **Quartiles** - Q1, Q2 (median), Q3

For string fields:
- **Min/Max/Average length** - String length statistics
- **Pattern samples** - Common patterns (e.g., "AAA-999")

#### 3. Frequency Analysis
- **Mode** - Most common value
- **Top values** - Most frequent values with counts and percentages
- **Value distribution** - Frequency histogram

#### 4. Quality Metrics
- **Completeness** (0-100%) - Percentage of non-null values
- **Validity** (0-100%) - Percentage matching inferred type
- **Uniqueness** (0-100%) - Cardinality measure
- **Consistency** (0-100%) - Pattern consistency score
- **Overall score** - Weighted quality assessment
- **Issues** - Detected quality problems

#### 5. Pattern Analysis
- **Pattern detection** - Common string patterns
- **Pattern frequency** - How often patterns appear
- **Format inference** - Date formats, email patterns, etc.

### Cross-Column Analysis

- **Correlations** - Relationships between numeric columns
- **Correlation strength** - Strong (>0.7) or Moderate (0.5-0.7)
- **Correlation type** - Pearson correlation coefficient

---

## Using the Profile Command

### Command Syntax

```bash
python3 -m validation_framework.cli profile [OPTIONS] FILE_PATH
```

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | File format (csv, excel, json, parquet) | Auto-detect |
| `--html-output` | `-o` | HTML report path | `<filename>_profile_report.html` |
| `--json-output` | `-j` | JSON output path | None |
| `--config-output` | `-c` | Validation config path | `<filename>_validation.yaml` |
| `--chunk-size` | - | Rows per chunk for large files | 50000 |
| `--log-level` | - | Logging level | INFO |

### Examples

#### Profile with All Outputs

```bash
python3 -m validation_framework.cli profile customers.csv \
  -o reports/customer_profile.html \
  -j reports/customer_profile.json \
  -c configs/customer_validation.yaml
```

#### Profile Large Parquet File

```bash
# Increase chunk size for better performance
python3 -m validation_framework.cli profile large_data.parquet \
  --chunk-size 100000
```

#### Profile with Debug Logging

```bash
python3 -m validation_framework.cli profile data.csv \
  --log-level DEBUG
```

### Command Output

The command prints a summary to the console:

```
🔍 Profiling customers.csv...

📊 Profile Summary:
  • File: customers.csv
  • Size: 45.23 MB
  • Rows: 1,250,000
  • Columns: 12
  • Overall Quality Score: 87.5%
  • Processing Time: 3.42s

✅ HTML report generated: customers_profile_report.html
✅ Validation config saved: customers_validation.yaml

💡 To run validations, use:
   python3 -m validation_framework.cli validate customers_validation.yaml --html report.html

💡 Top Validation Suggestions:
  • EmptyFileCheck (ERROR)
    Prevent empty file loads
  • MandatoryFieldCheck (ERROR)
    8 fields have >95% completeness
  • UniqueKeyCheck (ERROR)
    Field appears to be a unique identifier
  • RangeCheck (WARNING)
    Values range from 0 to 1000000
  • DateFormatCheck (ERROR)
    Detected date format: %Y-%m-%d
```

---

## Understanding Profile Reports

### HTML Report Structure

The interactive HTML report contains:

#### 1. Header Section
- File name and metadata
- Profiling timestamp
- Processing time
- Overall quality score with color coding:
  - **Excellent** (90-100%) - Green
  - **Good** (75-89%) - Blue
  - **Fair** (50-74%) - Orange
  - **Poor** (<50%) - Red

#### 2. Summary Cards
- File size
- Format
- Total rows
- Total columns
- Overall quality score

#### 3. Quality Overview Charts

**Completeness Chart (Bar)**
- Shows percentage of non-null values per column
- Identifies fields with missing data
- Color: Purple gradient

**Quality Scores Chart (Radar)**
- Compares overall quality vs validity across columns
- Identifies problematic fields
- Multi-dataset comparison

#### 4. Column Profiles

Each column displays:

**Header**
- Column name
- Type badge (Known/Inferred)
- Data type

**Type Information Card**
- Inferred type
- Declared type (if provided)
- Confidence percentage
- Visual confidence bar

**Statistics Card**
- Total values
- Null count and percentage
- Unique values and percentage
- Range (for numeric)
- Mean (for numeric)

**Quality Metrics Card**
- Overall score
- Completeness
- Validity
- Uniqueness
- Detected issues (if any)

**Top Values Table**
- Most frequent values
- Count and percentage
- Visual percentage bar

#### 5. Correlations Section

Shows significant correlations (|correlation| > 0.5) between numeric columns:
- Column pairs
- Correlation coefficient (-1 to 1)
- Strength (Strong/Moderate)
- Direction (Positive/Negative)

#### 6. Suggested Validations

Lists recommended validation checks with:
- Validation type
- Severity (ERROR/WARNING)
- Reason for suggestion
- Confidence level
- Parameters to use

#### 7. Generated Configuration

**YAML Configuration**
- Complete validation config
- Copy button for easy copying
- Ready to use immediately

**CLI Command**
- Exact command to run validations
- Uses generated config file

### Interactive Features

- **Charts** - Powered by Chart.js for interactive visualization
- **Copy Button** - One-click config copying
- **Responsive Design** - Works on mobile and desktop
- **Dark Theme** - Easy on the eyes
- **Collapsible Sections** - Organize large profiles

---

## Type Inference: Known vs Inferred

Understanding the difference between known and inferred types is critical for data quality.

### Known Types

**Indicator**: Green badge with "(Known)"
**Source**: Declared schema or definitive type information
**Confidence**: Always 100%

```yaml
# Example: Providing a declared schema
declared_schema:
  customer_id: "integer"
  email: "string"
  balance: "float"
```

When you provide a schema, types are **known** because you've explicitly declared them.

### Inferred Types

**Indicator**: Blue badge with "(Inferred)"
**Source**: Analysis of actual data values
**Confidence**: 0-100% based on data consistency

The profiler infers types by:

1. **Analyzing each value** in the column
2. **Detecting patterns** (numeric, date, boolean, string)
3. **Calculating confidence** based on consistency

#### Confidence Levels

| Confidence | Meaning |
|------------|---------|
| 100% | All values match inferred type |
| 90-99% | Very consistent, minor exceptions |
| 75-89% | Mostly consistent, some conflicts |
| 50-74% | Moderate consistency, significant conflicts |
| <50% | Low consistency, mixed types |

### Type Conflict Detection

When data doesn't consistently match the inferred type, conflicts are flagged:

```
Type Conflicts:
  • string: 125 values (2.5%)
  • null: 50 values (1.0%)
```

This indicates:
- Primary inferred type might be `integer`
- But 2.5% of values are strings
- And 1% are nulls

#### Example: The "123" Problem

A field containing all numbers stored as strings:

```csv
customer_id
"1001"
"1002"
"1003"
```

**Inferred Type**: `integer`
**Confidence**: 100% (all values are numeric)
**Known**: False (no schema provided)

**Warning**: While the data _looks_ numeric, it's actually stored as strings. This is an important distinction!

The profile report will show:
- **Inferred Type**: integer
- **Confidence**: 100%
- **Is Known**: False
- **Note**: "Field of all numbers in a large dataset could infer that the schema is a number, but we don't know for certain it's always a number."

### Best Practice

1. **Review inferred types** carefully
2. **Check confidence levels** - Lower confidence means inconsistent data
3. **Investigate type conflicts** - Why are there mixed types?
4. **Provide schemas** when possible for known types
5. **Validate type assumptions** with domain experts

---

## Quality Metrics Explained

### Completeness

**Range**: 0-100%
**Meaning**: Percentage of non-null values

```
Completeness = (Non-Null Count / Total Count) × 100
```

#### Interpretation

| Score | Interpretation | Action |
|-------|---------------|--------|
| 100% | Perfect completeness | Enforce with MandatoryFieldCheck |
| 95-99% | Excellent | Consider MandatoryFieldCheck |
| 90-94% | Good | Acceptable for most use cases |
| 75-89% | Fair | Review why data is missing |
| <75% | Poor | Investigate data source |

### Validity

**Range**: 0-100%
**Meaning**: Percentage of values matching the inferred type

```
Validity = Type Confidence × 100
```

#### Interpretation

| Score | Interpretation | Action |
|-------|---------------|--------|
| 100% | All values match type | Data is type-consistent |
| 95-99% | Mostly consistent | Check type conflicts |
| 90-94% | Some inconsistencies | Review and clean data |
| <90% | Type problems | Investigate data quality |

### Uniqueness

**Range**: 0-100%
**Meaning**: Cardinality - ratio of unique to total values

```
Uniqueness = (Unique Count / Total Count) × 100
```

#### Interpretation

| Score | Field Type | Suggested Validation |
|-------|-----------|---------------------|
| 100% | Unique identifier | UniqueKeyCheck |
| 50-99% | High cardinality | Good for analysis |
| 10-49% | Medium cardinality | Normal field |
| 1-9% | Low cardinality | ValidValuesCheck |
| <1% | Very low cardinality | Possibly constant |

### Consistency

**Range**: 0-100%
**Meaning**: Pattern consistency across string values

```
Consistency = (Top Pattern Frequency / Total Values) × 100
```

#### Interpretation

| Score | Interpretation | Example |
|-------|---------------|---------|
| >90% | Highly consistent | All phone numbers follow same format |
| 70-90% | Mostly consistent | Most dates in same format |
| 50-69% | Moderate consistency | Mixed patterns acceptable |
| <50% | Low consistency | Investigate data entry |

### Overall Score

Weighted average of all quality dimensions:

```
Overall = (0.3 × Completeness) +
          (0.3 × Validity) +
          (0.2 × Uniqueness) +
          (0.2 × Consistency)
```

#### Weighting Rationale

- **Completeness (30%)** - Critical for usability
- **Validity (30%)** - Critical for correctness
- **Uniqueness (20%)** - Important for analysis
- **Consistency (20%)** - Important for processing

---

## Auto-Generated Validations

The profiler automatically suggests validations based on data analysis.

### Suggestion Criteria

#### 1. EmptyFileCheck (ERROR)

**Always suggested**
**Reason**: Prevent loading empty files
**Confidence**: 100%

```yaml
- type: "EmptyFileCheck"
  severity: "ERROR"
```

#### 2. RowCountRangeCheck (WARNING)

**Suggested when**: File has rows
**Parameters**:
- `min_rows`: 50% of current count
- `max_rows`: 200% of current count

**Reason**: Detect unexpected data volume changes

```yaml
- type: "RowCountRangeCheck"
  severity: "WARNING"
  params:
    min_rows: 5000
    max_rows: 20000
  # Expect approximately 10000 rows based on profile
```

#### 3. MandatoryFieldCheck (ERROR)

**Suggested when**: Field has >95% completeness
**Confidence**: 95%

**Reason**: Highly complete fields should remain mandatory

```yaml
- type: "MandatoryFieldCheck"
  severity: "ERROR"
  params:
    fields: ["customer_id", "email", "name"]
  # 3 fields have >95% completeness
```

#### 4. RangeCheck (WARNING)

**Suggested when**: Numeric field with min/max values
**Confidence**: 90%

**Reason**: Values typically fall within observed range

```yaml
- type: "RangeCheck"
  severity: "WARNING"
  params:
    field: "balance"
    min_value: 0.0
    max_value: 1000000.0
  # Values range from 0.0 to 1000000.0
```

#### 5. ValidValuesCheck (ERROR)

**Suggested when**:
- Cardinality < 5%
- Unique count < 20

**Confidence**: 85%

**Reason**: Low cardinality indicates enumerated values

```yaml
- type: "ValidValuesCheck"
  severity: "ERROR"
  params:
    field: "account_type"
    valid_values: ["BASIC", "STANDARD", "PREMIUM"]
  # Low cardinality field with 3 unique values
```

#### 6. UniqueKeyCheck (ERROR)

**Suggested when**:
- Cardinality > 99%
- Row count > 100

**Confidence**: 95%

**Reason**: Field appears to be a unique identifier

```yaml
- type: "UniqueKeyCheck"
  severity: "ERROR"
  params:
    fields: ["customer_id"]
  # Field appears to be a unique identifier
```

#### 7. DateFormatCheck (ERROR)

**Suggested when**:
- Inferred type is "date"
- Format can be detected

**Confidence**: 80%

**Reason**: Enforce consistent date formats

```yaml
- type: "DateFormatCheck"
  severity: "ERROR"
  params:
    field: "created_date"
    format: "%Y-%m-%d"
  # Detected date format: %Y-%m-%d
```

### Using Generated Config

The auto-generated config is production-ready:

```bash
# 1. Profile data
python3 -m validation_framework.cli profile data.csv

# 2. Review generated config
cat data_validation.yaml

# 3. Customize if needed (optional)
vim data_validation.yaml

# 4. Run validations
python3 -m validation_framework.cli validate data_validation.yaml \
  --html validation_report.html
```

### Customizing Suggestions

Review and adjust:

1. **Severity levels** - Change ERROR to WARNING or vice versa
2. **Range limits** - Tighten or loosen based on business rules
3. **Valid values** - Add/remove accepted values
4. **Mandatory fields** - Adjust based on business requirements
5. **Add custom logic** - Include conditional validations

---

## Profiling Large Files

### Performance Considerations

The profiler is optimized for large files (200GB+) using chunked processing.

#### Default Settings

- **Chunk size**: 50,000 rows
- **Memory usage**: ~400 MB peak
- **Correlation limit**: 20 numeric columns

#### Optimization Tips

**1. Increase Chunk Size**

For systems with more memory:

```bash
python3 -m validation_framework.cli profile large_data.parquet \
  --chunk-size 100000
```

**2. Use Parquet Format**

Parquet is faster than CSV for large files:

- Columnar format
- Built-in compression
- Faster reading

**3. Limit Correlation Analysis**

Only first 20 numeric columns are analyzed for correlations to prevent memory issues.

### Performance Benchmarks

| File Size | Format | Chunk Size | Time | Memory |
|-----------|--------|------------|------|--------|
| 1 MB | CSV | 50K | <1s | <10 MB |
| 100 MB | CSV | 50K | ~10s | ~50 MB |
| 1 GB | Parquet | 50K | ~2min | ~200 MB |
| 50 GB | Parquet | 100K | ~1hr | ~400 MB |
| 200 GB | Parquet | 100K | ~4hrs | ~400 MB |

### Large File Best Practices

1. **Use Parquet** for files >1GB
2. **Increase chunk size** if memory allows
3. **Run on server** rather than laptop for 50GB+ files
4. **Profile samples first** to understand data before full profile
5. **Schedule during off-hours** for very large files

---

## Best Practices

### 1. Profile Before Validating

Always profile data before creating validation configurations:

```bash
# Step 1: Profile
python3 -m validation_framework.cli profile new_data.csv

# Step 2: Review profile report
open new_data_profile_report.html

# Step 3: Use generated config as starting point
cp new_data_validation.yaml production_validation.yaml

# Step 4: Customize based on business rules
vim production_validation.yaml
```

### 2. Use Profiling for Documentation

Generate data dictionaries for datasets:

```bash
# Profile dataset
python3 -m validation_framework.cli profile dataset.csv \
  -o docs/dataset_profile.html \
  -j docs/dataset_profile.json
```

The HTML report serves as comprehensive documentation:
- Schema with types
- Statistics and ranges
- Quality metrics
- Sample values

### 3. Regular Profile Updates

Re-profile periodically to detect data drift:

```bash
# Profile weekly
0 0 * * 0 cd /data && python3 -m validation_framework.cli profile \
  dataset.csv -o profiles/$(date +\%Y-\%m-\%d)_profile.html
```

Compare profiles over time to identify:
- Schema changes
- Quality degradation
- Value range expansion
- New patterns

### 4. Review Suggested Validations Critically

Don't blindly accept all suggestions:

✅ **Good Practice**:
```yaml
# Review suggestion
- type: "RangeCheck"
  severity: "WARNING"  # Changed from ERROR
  params:
    field: "balance"
    min_value: 0.0      # Makes business sense
    max_value: 1000000.0 # Increased from 500000 based on domain knowledge
```

❌ **Bad Practice**:
```yaml
# Accepting without review
- type: "ValidValuesCheck"
  severity: "ERROR"
  params:
    field: "country"
    valid_values: ["US", "UK", "CA"]
    # ⚠️ What if new countries are added legitimately?
```

### 5. Combine Profile Data with Domain Knowledge

Profiling shows what data **is**, not what it **should be**.

**Example**:
- Profile shows: `balance` ranges from -5000 to 1000000
- Domain knowledge says: Balances should be ≥ 0
- **Action**: Override suggested range with business rule

```yaml
- type: "RangeCheck"
  severity: "ERROR"
  params:
    field: "balance"
    min_value: 0.0          # Business rule
    max_value: 1000000.0    # From profile
```

### 6. Use JSON Export for Automation

Integrate profiling into data pipelines:

```python
import json

# Profile data
# python3 -m validation_framework.cli profile data.csv -j profile.json

# Load profile
with open('profile.json') as f:
    profile = json.load(f)

# Check quality score
if profile['overall_quality_score'] < 80:
    send_alert("Data quality below threshold")

# Check for schema changes
expected_columns = set(['id', 'name', 'email'])
actual_columns = set(col['name'] for col in profile['columns'])

if expected_columns != actual_columns:
    send_alert(f"Schema mismatch: {actual_columns - expected_columns}")
```

### 7. Profile Samples for Very Large Datasets

For 1TB+ datasets, profile a representative sample first:

```bash
# Extract sample
head -n 100000 huge_dataset.csv > sample.csv

# Profile sample
python3 -m validation_framework.cli profile sample.csv

# Review and decide if full profile is needed
```

### 8. Version Control Profile Reports

Track profile reports in git (as documentation):

```bash
git add docs/dataset_profile.html
git commit -m "Update dataset profile - Q4 2024"
```

Or store in data catalog/documentation system.

### 9. Share Profiles with Stakeholders

HTML reports are stakeholder-friendly:
- No technical knowledge required
- Visual and interactive
- Comprehensive but accessible

Share with:
- Data analysts - For understanding data
- Business users - For validation rules
- Data engineers - For pipeline design
- QA teams - For testing strategies

### 10. Validate the Validator

Test generated configs on a sample before production:

```bash
# 1. Profile
python3 -m validation_framework.cli profile data.csv

# 2. Test on sample
head -n 1000 data.csv > sample.csv
python3 -m validation_framework.cli validate data_validation.yaml

# 3. Review results and adjust

# 4. Deploy to production
```

---

## Summary

Data profiling is an essential step in implementing robust data validations:

✅ **Discover** - Understand your data structure and quality
✅ **Document** - Generate comprehensive data dictionaries
✅ **Decide** - Make data-driven validation decisions
✅ **Deploy** - Use auto-generated configs as a starting point
✅ **Monitor** - Track data quality over time

**Next Steps**:
- [User Guide](USER_GUIDE.md) - Learn about all validation types
- [Advanced Guide](ADVANCED_GUIDE.md) - Complex validation scenarios
- [Best Practices Guide](BEST_PRACTICES.md) - Implementation guidance

---

**Happy Profiling! 📊**
