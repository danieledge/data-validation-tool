# Data Validation Framework

**Production-grade data quality validation with no coding required**

A robust, extensible Python framework for validating data quality before loading to databases, data warehouses, or analytics platforms. Designed to handle enterprise-scale datasets (200GB+) with memory-efficient chunked processing.

[![Version 2.2.0](https://img.shields.io/badge/version-2.2.0-blue.svg)](docs/WHATS_NEW.md)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests: 115+ passing](https://img.shields.io/badge/tests-115%2B%20passing-brightgreen.svg)](tests/)
[![Coverage: 48%](https://img.shields.io/badge/coverage-48%25-yellow.svg)](htmlcov/)

**🎉 NEW in v2.2:** [Visual Config Builder](docs/WHATS_NEW.md#-visual-config-builder) • [Testing Suite (115+ tests)](docs/WHATS_NEW.md#-comprehensive-testing-suite) • [Testing Guide](docs/TESTING.md) • **[See What's New →](docs/WHATS_NEW.md)**

---

## 🚀 Quick Start

**Get up and running in 5 minutes**:

```bash
# 1. Install
cd data-validation-tool
pip install -r requirements.txt

# 2. Create configuration
# Option A: Use the visual config builder (no coding!)
# Online: https://raw.githack.com/danieledge/data-validation-tool/main/docs/config-builder.html
# Or local: open docs/config-builder.html

# Option B: Create YAML manually
cat > validation.yaml <<EOF
validation_job:
  name: "My First Validation"

settings:
  chunk_size: 1000

files:
  - name: "customers"
    path: "customers.csv"
    format: "csv"
    validations:
      - type: "EmptyFileCheck"
        severity: "ERROR"
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["customer_id", "email"]
EOF

# 3. Run validation
python3 -m validation_framework.cli validate validation.yaml --html report.html

# 4. View results
open report.html
```

**🎨 NEW: [Visual Config Builder →](https://raw.githack.com/danieledge/data-validation-tool/main/docs/config-builder.html)** - Build validation configs with an intuitive web interface!

**New to the framework?** Start with the **[Getting Started Guide →](docs/GETTING_STARTED.md)**

---

## ✨ Key Features

### For Business Users
- ✅ **No Coding Required** - Define validations in simple YAML configuration
- ✅ **35+ Built-in Validations** - File, schema, field, record, cross-file, database, temporal, and statistical checks
- ✅ **Professional Reports** - Interactive HTML and JSON outputs
- ✅ **Conditional Logic** - Apply different rules based on data values

### For Data Engineers
- ⚡ **Enterprise Scale** - Handles 200GB+ files with chunked processing
- 🔌 **Multiple Formats** - CSV, Excel, JSON, Parquet support
- 🎯 **AutoSys Integration** - Fail jobs on critical data issues
- 🔧 **Extensible** - Plugin architecture for custom validations

### For Developers
- 🏗️ **Production Ready** - 102 tests, comprehensive error handling
- 📊 **Well Architected** - Clean separation of concerns, design patterns
- 🧪 **Fully Tested** - Unit, integration, and end-to-end tests
- 📖 **Complete Documentation** - Architecture, API reference, examples

---

## 🎨 Visual Config Builder v2

**NEW v2!** Production-ready config builder with advanced features - no coding required.

**🌐 Live Demo:** https://raw.githack.com/danieledge/data-validation-tool/main/docs/config-builder.html

**Key Features:**
- 🗂️ **Multiple Files** - Configure complex multi-file validations
- 📋 **Template Library** - 5 pre-built templates for common scenarios
- 📥 **Import YAML** - Load and edit existing configurations
- 💾 **Auto-Save** - Browser localStorage with auto-save every 30 seconds
- 🔗 **Shareable URLs** - Generate links to share configurations
- ⚙️ **Advanced Settings** - chunk_size, fail_fast, log_level configuration
- 🎨 **Syntax Highlighting** - Color-coded YAML preview
- ⌨️ **Keyboard Shortcuts** - Ctrl+S, Ctrl+D, Ctrl+I, ? for help
- 📱 **Mobile-Optimized** - Full responsive design with touch controls
- 🔍 **Smart Parameters** - Type-specific inputs with validation and hints
- 📊 **Dashboard** - Real-time summary of files, validations, and severity counts

---

## 📊 Data Profiling

**NEW!** Analyze your data files to understand structure, quality, and patterns before creating validations.

```bash
# Profile any data file
python3 -m validation_framework.cli profile data.csv

# Generates:
# - Interactive HTML report with charts
# - Auto-generated validation config
# - Quality metrics and suggestions
```

### 🎨 View Live Examples

See the profiler in action with these interactive example reports:

| Example | Rows | Size | Preview |
|---------|------|------|---------|
| **Simple Customer Data** | 10 | 728 B | [View Report →](https://htmlpreview.github.io/?https://github.com/danieledge/data-validation-tool/blob/main/docs/example_profile_report.html) |
| **E-Commerce Orders** | 30 | 2.51 KB | [View Report →](https://htmlpreview.github.io/?https://github.com/danieledge/data-validation-tool/blob/main/docs/comprehensive_profile_report.html) |
| **Large Dataset** | 5,000 | 428 KB | [View Report →](https://htmlpreview.github.io/?https://github.com/danieledge/data-validation-tool/blob/main/docs/large_profile_report.html) |

**Features:**
- 📈 Interactive charts with quality metrics
- 🔍 Type inference (known vs inferred)
- 📊 Statistical distributions and correlations
- 💡 Auto-generated validation suggestions
- 📱 Mobile-responsive design
- 🗂️ Table of contents for easy navigation

**Learn More:** [Data Profiling Guide →](docs/DATA_PROFILING.md)

---

## 📚 Documentation

### Getting Started
- **🎉 [What's New](docs/WHATS_NEW.md)** - Latest features and changes (v2.1.0)
- **[Quick Start (5 minutes)](docs/GETTING_STARTED.md)** - Installation to first validation
- **[User Guide](docs/USER_GUIDE.md)** - Complete configuration reference
- **[Validation Catalog](docs/VALIDATION_CATALOG.md)** - All 35+ validation types documented
- **[Data Profiling Guide](docs/DATA_PROFILING.md)** - Analyze data before validation
- **⭐ [Best Practices](docs/BEST_PRACTICES.md)** - ERROR vs WARNING, essential validations, production tips
- **💡 [No-Code Custom Validations](docs/NO_CODE_CUSTOM_VALIDATIONS.md)** - Build custom rules without programming

### Advanced Usage
- **[Advanced Guide](docs/ADVANCED_GUIDE.md)** - Complex scenarios, performance tuning
- **[Handling Large Reports](docs/HANDLING_LARGE_REPORTS.md)** - Strategies for millions of rows
- **[Examples & Recipes](docs/EXAMPLES.md)** - 10 real-world validation scenarios
- **[AutoSys Integration](docs/EXAMPLES.md#autosys-job-integration)** - Block jobs on validation failures

### Technical Documentation
- **[Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)** - How the system works
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Create custom validations
- **[API Reference](docs/DEVELOPER_GUIDE.md#api-reference)** - Complete API documentation

---

## 🎯 Common Use Cases

### 1. Pre-Load Data Quality Checks

Validate data before loading to warehouse:

```yaml
validations:
  - type: "EmptyFileCheck"
    severity: "ERROR"
  - type: "RowCountRangeCheck"
    severity: "WARNING"
    params:
      min_rows: 1000
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    params:
      fields: ["id", "email", "created_date"]
```

### 2. Business Rule Validation

Apply conditional business logic:

```yaml
# Business accounts need company details
- type: "ConditionalValidation"
  severity: "ERROR"
  params:
    condition: "account_type == 'BUSINESS'"
    then_validate:
      - type: "MandatoryFieldCheck"
        params:
          fields: ["company_name", "tax_id"]
    else_validate:
      - type: "MandatoryFieldCheck"
        params:
          fields: ["first_name", "last_name"]
```

### 3. AutoSys Job Control

Block data loads on validation failures:

```bash
# validation_job.sh
python3 -m validation_framework.cli validate config.yaml --json results.json

if [ $? -ne 0 ]; then
  echo "Validation failed - blocking load"
  exit 1  # Fail AutoSys job
fi

# Proceed with load only if validation passes
./load_data.sh
```

**See [AutoSys Integration Guide](docs/EXAMPLES.md#autosys-job-integration) for complete examples**

---

## 📊 Available Validations

### File-Level Checks
- **EmptyFileCheck** - File not empty
- **RowCountRangeCheck** - Row count within range
- **FileSizeCheck** - File size limits

### Schema Checks
- **SchemaMatchCheck** - Exact schema match
- **ColumnPresenceCheck** - Required columns exist

### Field-Level Checks
- **MandatoryFieldCheck** - Required fields not null
- **RegexCheck** - Pattern validation
- **ValidValuesCheck** - Values in allowed list
- **RangeCheck** - Numeric ranges
- **DateFormatCheck** - Date format validation

### Record-Level Checks
- **DuplicateRowCheck** - Detect duplicates
- **BlankRecordCheck** - Find empty rows
- **UniqueKeyCheck** - Unique constraints

### Conditional Validation
- **ConditionalValidation** - If-then-else logic
- **Inline Conditions** - Apply any validation conditionally

### Advanced Checks
- **StatisticalOutlierCheck** - Detect anomalies
- **CrossFieldComparisonCheck** - Field relationships
- **FreshnessCheck** - Data recency
- **CompletenessCheck** - Field completeness %
- **StringLengthCheck** - String length limits
- **NumericPrecisionCheck** - Decimal precision

### Cross-File Validations 🆕
- **ReferentialIntegrityCheck** - Foreign key relationships between files
- **CrossFileComparisonCheck** - Compare aggregates across files
- **CrossFileDuplicateCheck** - Duplicates across multiple files

### Database Validations 🆕
- **SQLCustomCheck** - Custom SQL-based validations
- **DatabaseReferentialIntegrityCheck** - Database foreign keys
- **DatabaseConstraintCheck** - Database constraint validation

### Temporal/Historical Validations 🆕
- **BaselineComparisonCheck** - Compare against historical averages
- **TrendDetectionCheck** - Detect unusual growth/decline rates

### Statistical Validations 🆕
- **DistributionCheck** - Validate statistical distributions
- **CorrelationCheck** - Column correlation validation
- **AdvancedAnomalyDetectionCheck** - Multiple anomaly detection methods

**See [Validation Catalog](docs/VALIDATION_CATALOG.md) for complete reference of 35+ validations**

---

## 🔧 Installation

### Requirements
- Python 3.8 or higher
- pip

### Install

```bash
# Clone repository
git clone https://github.com/danieledge/data-validation-tool.git
cd data-validation-tool

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 -m validation_framework.cli --help
```

### Optional Dependencies

```bash
# Excel support
pip install openpyxl

# Parquet support
pip install pyarrow

# Development tools
pip install -r requirements-dev.txt
```

---

## 🎨 Usage Examples

### Basic Validation

```bash
# Run validation
python3 -m validation_framework.cli validate config.yaml

# With HTML report
python3 -m validation_framework.cli validate config.yaml --html report.html

# With JSON output
python3 -m validation_framework.cli validate config.yaml --json results.json

# Both reports
python3 -m validation_framework.cli validate config.yaml \
  --html report.html \
  --json results.json
```

### List Available Validations

```bash
python3 -m validation_framework.cli list-validations
```

### Exit Codes

- `0` - Validation passed
- `1` - Validation failed (errors found)
- `2` - Command error (bad config, file not found, etc.)

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────┐
│                  CLI Interface                      │
└──────────────────────┬─────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────┐
│            Validation Engine                        │
│  • Load configuration                               │
│  • Create loaders                                   │
│  • Execute validations                              │
│  • Generate reports                                 │
└──────┬─────────────────────────┬──────────────────┘
       │                         │
       ▼                         ▼
┌─────────────┐          ┌─────────────────┐
│   Loaders   │          │   Validations   │
│  • CSV      │          │  • File-level   │
│  • Excel    │          │  • Schema       │
│  • JSON     │          │  • Field-level  │
│  • Parquet  │          │  • Record-level │
└─────────────┘          │  • Conditional  │
                         └─────────────────┘
                                │
                                ▼
                         ┌─────────────────┐
                         │    Reporters    │
                         │  • HTML         │
                         │  • JSON         │
                         └─────────────────┘
```

**[Learn more about the architecture →](docs/TECHNICAL_ARCHITECTURE.md)**

---

## 🚀 Performance

### Large File Support

**Tested with 200GB+ files:**
- ✅ Memory-efficient chunked processing
- ✅ Only one chunk in memory at a time
- ✅ Configurable chunk size
- ✅ Parquet format recommended for best performance

### Performance Characteristics

| File Size | Format  | Chunk Size | Time        | Memory  |
|-----------|---------|------------|-------------|---------|
| 1 MB      | CSV     | 1,000      | < 1 second  | < 10 MB |
| 100 MB    | CSV     | 10,000     | ~10 seconds | ~50 MB  |
| 1 GB      | Parquet | 50,000     | ~2 minutes  | ~200 MB |
| 50 GB     | Parquet | 100,000    | ~1 hour     | ~400 MB |
| 200 GB    | Parquet | 100,000    | ~4 hours    | ~400 MB |

**[Performance optimization guide →](docs/ADVANCED_GUIDE.md#performance-optimization)**

---

## 🔌 Integration

### AutoSys Job Scheduling

```bash
# AutoSys JIL Definition
insert_job: VALIDATE_DATA
job_type: c
command: /apps/validation/validate_and_fail.sh
condition: success(EXTRACT_DATA)
alarm_if_fail: yes

insert_job: LOAD_DATA
job_type: c
command: /apps/etl/load.sh
condition: success(VALIDATE_DATA)  # Only runs if validation passes
```

**[Complete AutoSys integration guide →](docs/EXAMPLES.md#autosys-job-integration)**

### CI/CD Pipeline

```yaml
# GitHub Actions
- name: Validate Data
  run: |
    python3 -m validation_framework.cli validate config.yaml --json results.json
    if [ $? -ne 0 ]; then
      exit 1
    fi
```

### Python Script

```python
from validation_framework.core.engine import ValidationEngine

# Run validation
engine = ValidationEngine.from_config("config.yaml")
report = engine.run()

# Check results
if report.overall_status != "PASSED":
    raise ValueError(f"Validation failed: {report.total_errors} errors")
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=validation_framework --cov-report=html

# Open coverage report
open htmlcov/index.html
```

**Test Results:**
- 115+ tests passing
- 48% code coverage
- Unit, integration, and end-to-end tests
- Comprehensive profiler test suite with 49 tests

**[Complete Testing Guide →](docs/TESTING.md)** - Test organization, writing new tests, CI/CD integration

---

## 🤝 Contributing

Contributions welcome! See **[Developer Guide](docs/DEVELOPER_GUIDE.md)** for:
- Setting up development environment
- Creating custom validations
- Writing tests
- Contribution guidelines

---

## 📖 Additional Resources

### Documentation
- [What's New](docs/WHATS_NEW.md) - Latest features and changes
- [Getting Started](docs/GETTING_STARTED.md)
- [User Guide](docs/USER_GUIDE.md)
- [Validation Catalog](docs/VALIDATION_CATALOG.md)
- [Data Profiling Guide](docs/DATA_PROFILING.md)
- [Advanced Guide](docs/ADVANCED_GUIDE.md)
- [Examples](docs/EXAMPLES.md)
- [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Testing Guide](docs/TESTING.md) - Comprehensive testing documentation

### Support
- [GitHub Issues](https://github.com/danieledge/data-validation-tool/issues)
- [Discussion Forum](https://github.com/danieledge/data-validation-tool/discussions)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👤 Author

**daniel edge**

---

## 🌟 Highlights

- ✅ **Production Ready** - Used for enterprise data pipelines
- ✅ **Well Documented** - Comprehensive documentation for all users
- ✅ **Actively Maintained** - Regular updates and improvements
- ✅ **Extensible** - Easy to add custom validations
- ✅ **Scalable** - Handles files from KB to 200GB+

**Ready to get started?** → **[5-Minute Quick Start Guide](docs/GETTING_STARTED.md)**
