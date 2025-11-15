# What is DataK9?

**DataK9** is a production-grade data quality framework that guards your data pipelines with vigilance and precision. Like a K9 unit that sniffs out problems before they escalate, DataK9 catches data quality issues before they reach production.

---

## The K9 Concept 🐕

**Why K9 (Canine)?**

Just like security forces use K9 units for detection and protection, DataK9:
- **Sniffs out issues** - Detects data quality problems before humans notice
- **Guards your pipelines** - Provides continuous protection for your data
- **Stays vigilant** - Always alert, never misses a check
- **Trains to your needs** - Configurable validation rules for your specific use case
- **Loyal and reliable** - Production-grade, enterprise-ready framework

---

## What Does DataK9 Do?

DataK9 validates data **before** it enters your data warehouse, analytics platform, or downstream systems. It helps you:

### Catch Issues Early ✅
- Find data quality problems before they cause production issues
- Prevent bad data from polluting your warehouse
- Save time and money by catching errors upfront

### Define Rules Easily 📝
- Write validation rules in simple YAML configuration
- Or use DataK9 Studio visual IDE (no coding required!)
- 35+ built-in validation types ready to use

### Handle Massive Datasets 💪
- Process 200GB+ files efficiently
- Memory-efficient chunked processing
- Only uses ~400MB RAM regardless of file size

### Generate Actionable Reports 📊
- Beautiful HTML reports with dark theme
- JSON output for CI/CD integration
- Clear identification of failed rows and issues

### Integrate Seamlessly 🔗
- AutoSys batch job integration
- CI/CD pipeline ready
- Works with Airflow and other orchestration tools

---

## Who Uses DataK9?

### Data Engineers
"I use DataK9 to validate data before loading to Snowflake. It catches schema changes and data quality issues that would otherwise break our pipelines."

### Business Analysts
"With DataK9 Studio, I can build validation rules without coding. I define the business logic, and DataK9 enforces it."

### QA Engineers
"DataK9 is part of our automated testing. Every data file gets validated before it goes to production."

### Compliance Officers
"We use DataK9 to ensure PII fields are properly formatted and regulatory requirements are met."

---

## Key Features

### 35+ Built-in Validation Rules

**File-Level Checks:**
- EmptyFileCheck - Ensure files aren't empty
- RowCountRangeCheck - Verify expected row counts
- FileSizeCheck - Check file size constraints

**Schema Checks:**
- SchemaMatchCheck - Validate column structure
- ColumnPresenceCheck - Ensure required columns exist

**Field-Level Checks:**
- MandatoryFieldCheck - Require non-null values
- RegexCheck - Pattern matching (emails, phone numbers, etc.)
- ValidValuesCheck - Whitelist/blacklist values
- RangeCheck - Numeric and date ranges
- DateFormatCheck - Validate date formats

**Record-Level Checks:**
- DuplicateRowCheck - Find duplicate records
- BlankRecordCheck - Detect empty rows
- UniqueKeyCheck - Ensure primary key uniqueness

**Advanced Checks:**
- StatisticalOutlierCheck - Detect anomalies using Z-score or IQR
- CrossFieldComparisonCheck - Validate relationships between fields
- FreshnessCheck - Ensure data isn't stale
- CompletenessCheck - Percentage-based completeness

**And many more!** → [Complete Validation Catalog](../reference/validation-reference.md)

---

### DataK9 Studio - Visual IDE

Build validation rules without writing YAML:
- 🎨 Drag-and-drop validation builder
- 💻 Live YAML preview
- 📁 Project management
- 🔄 Import/export configurations
- 📱 Mobile-responsive
- 🌙 Dark theme

→ [DataK9 Studio Guide](studio-guide.md)

---

### Memory-Efficient Processing

DataK9 uses **chunked processing** to handle massive files:

| File Size | Memory Used | Processing Time |
|-----------|-------------|-----------------|
| 1 MB | ~50 MB | < 1 second |
| 100 MB | ~200 MB | ~10 seconds |
| 1 GB | ~400 MB | ~2 minutes |
| 10 GB | ~400 MB | ~20 minutes |
| 200 GB | ~400 MB | ~4 hours (Parquet) |

**How it works:**
- Reads data in chunks (default: 50,000 rows)
- Processes one chunk at a time
- Never loads entire file into memory
- Configurable chunk size

---

### Multiple Format Support

- **CSV** - Any delimiter, headers, quoted fields
- **Excel** - XLS, XLSX, multiple sheets
- **Parquet** - Columnar format (10x faster than CSV!)
- **JSON** - Arrays and JSON Lines (JSONL/NDJSON)
- **Databases** - Direct SQL query validation

---

### Enterprise-Ready Features

**AutoSys Integration:**
- Proper exit codes (0=pass, 1=errors, 2=config error)
- Designed for batch job orchestration
- Handles failures gracefully

**CI/CD Integration:**
- JSON output for machine parsing
- Works with Jenkins, GitLab CI, GitHub Actions
- Fail build on validation errors

**Production-Grade:**
- Comprehensive error handling
- Detailed logging
- 115+ unit tests
- Battle-tested with 200GB+ files

---

## How DataK9 Works

```
1. You create a YAML config
   ↓
2. DataK9 reads your data file in chunks
   ↓
3. Each validation rule runs on each chunk
   ↓
4. Results are aggregated
   ↓
5. HTML/JSON report is generated
   ↓
6. Exit code indicates pass/fail
```

---

## DataK9 vs Other Tools

### DataK9 vs Great Expectations

| Feature | DataK9 | Great Expectations |
|---------|--------|-------------------|
| Configuration | YAML | Python code |
| Visual IDE | Yes (DataK9 Studio) | No |
| Large files (200GB+) | Excellent | Requires Spark |
| Learning curve | Low | High |
| No-code options | Yes | No |
| AutoSys integration | Built-in | Manual |

### DataK9 vs dbt Tests

| Feature | DataK9 | dbt Tests |
|---------|--------|-----------|
| File validation | Yes | No (database only) |
| Pre-load validation | Yes | No (post-load) |
| Standalone use | Yes | Requires dbt project |
| Format support | CSV, Excel, Parquet, JSON, DB | Database tables only |

### DataK9 vs Manual Python Scripts

| Feature | DataK9 | Manual Scripts |
|---------|--------|----------------|
| Maintenance | Framework maintained | You maintain code |
| Configuration | YAML (no coding) | Python code required |
| Reports | Professional HTML/JSON | DIY |
| Validation library | 35+ built-in | Build everything |
| Testing | 115+ tests included | You write tests |

---

## Common Use Cases

### 1. Pre-Warehouse Validation
"Validate customer data before loading to Snowflake"

```yaml
validations:
  - type: "SchemaMatchCheck"
    severity: "ERROR"
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    params:
      fields: ["customer_id", "email"]
  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "email"
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

### 2. Financial Data Quality
"Ensure transaction data meets regulatory requirements"

```yaml
validations:
  - type: "RangeCheck"
    severity: "ERROR"
    params:
      field: "transaction_amount"
      min_value: 0
  - type: "FreshnessCheck"
    severity: "ERROR"
    params:
      date_field: "transaction_date"
      max_age_days: 1
```

### 3. Healthcare Data Compliance
"Validate patient data for HIPAA compliance"

```yaml
validations:
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    params:
      fields: ["patient_id", "dob", "diagnosis_code"]
  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "ssn"
      pattern: "^[0-9]{3}-[0-9]{2}-[0-9]{4}$"
```

→ [More Examples](../examples/)

---

## Getting Started

Ready to let DataK9 guard your data?

1. **[Install DataK9](../getting-started/installation.md)** - 5-minute setup
2. **[Quickstart Guide](../getting-started/quickstart-5min.md)** - Your first validation
3. **[Configuration Guide](configuration-guide.md)** - Learn YAML configuration
4. **[Validation Catalog](../reference/validation-reference.md)** - Browse all 35+ validations

---

## Need Help?

- **[FAQ](faq.md)** - Frequently asked questions
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Examples](../examples/)** - Real-world scenarios
- **[GitHub Issues](https://github.com/danieledge/data-validation-tool/issues)** - Report bugs

---

**🐕 Let DataK9 guard your data quality!**
