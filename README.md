<div align="center">
  <img src="resources/images/datak9-web.png" alt="DataK9 Logo" width="300">

  # DataK9

  ## 🐕 Your K9 guardian for data quality

  **Production-grade data quality validation with no coding required**
</div>

A robust, extensible Python framework for validating data quality before loading to databases, data warehouses, or analytics platforms. Like a well-trained K9 unit, DataK9 vigilantly guards your data, sniffing out quality issues before they become problems. Designed to handle enterprise-scale datasets (200GB+) with memory-efficient chunked processing.

[![Version 2.3.0](https://img.shields.io/badge/version-2.3.0-blue.svg)](#-datak9-studio)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests: 115+ passing](https://img.shields.io/badge/tests-115%2B%20passing-brightgreen.svg)](tests/)
[![Coverage: 48%](https://img.shields.io/badge/coverage-48%25-yellow.svg)](htmlcov/)

**🎉 NEW in v2.3:** [DataK9 Studio - Visual Configuration IDE](#-datak9-studio) • Validation Type Wizard • Three-Panel Layout • Monaco Editor Integration

---

## 🚀 Quick Start

**Get up and running in 5 minutes**:

```bash
# 1. Install DataK9
cd data-validation-tool
pip install -r requirements.txt

# 2. Create configuration
# Option A: Use DataK9 Studio (no coding!)
# Online: https://raw.githack.com/danieledge/data-validation-tool/main/datak9-studio.html
# Or local: open datak9-studio.html
# Note: If you see an old version, hard refresh with Ctrl+Shift+R (or Cmd+Shift+R on Mac)

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
python3 -m validation_framework.cli validate validation.yaml

# 4. View results
open validation_report.html
```

**🎨 NEW: [DataK9 Studio →](https://raw.githack.com/danieledge/data-validation-tool/main/datak9-studio.html)** - Build validation configs with a modern IDE-style interface and validation wizard!

**New to DataK9?** Start with the **[5-Minute Quickstart →](docs/getting-started/quickstart-5min.md)**

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
- 🏗️ **Production Ready** - 115+ tests, comprehensive error handling
- 📊 **Well Architected** - Clean separation of concerns, design patterns
- 🧪 **Fully Tested** - Unit, integration, and end-to-end tests
- 📖 **Complete Documentation** - Architecture, API reference, examples

---

## 🎨 DataK9 Studio

**NEW!** Professional IDE-style configuration builder with Monaco editor integration - no coding required.

**🌐 Live Demo:** https://raw.githack.com/danieledge/data-validation-tool/main/datak9-studio.html

**💡 Cache Issue?** If you see an old version, hard refresh with **Ctrl+Shift+R** (or **Cmd+Shift+R** on Mac). Check the version badge in the top-right corner - should show **v2.3.0**.

**Key Features:**
- 🎯 **IDE-Style Interface** - Professional three-panel layout like VS Code
- 🧙 **Validation Wizard** - Choose from 35+ validation types organized in 10 color-coded categories
- 💻 **Monaco Editor** - VS Code's YAML editor with syntax highlighting
- 📱 **Mobile-First Design** - Responsive with drawer panels and optimized touch controls
- 🎨 **Modern UI** - DataK9-branded dark theme (K9 Blue & Guard Orange)
- 🗂️ **Multiple Files** - Configure complex multi-file validations
- 📋 **Category Organization** - File, Schema, Field, Record, Cross-File, Statistical validations
- ⚙️ **Advanced Settings** - chunk_size, max_sample_failures configuration
- 🔍 **Smart Parameters** - Type-specific inputs with validation and hints
- 📊 **Real-time Preview** - Live YAML generation with two-way sync
- 🎯 **Context Help** - Right panel auto-updates with relevant documentation

---

## 📊 Data Profiling

**NEW!** Analyze your data files to understand structure, quality, and patterns before creating validations. Like a K9 sniffing out the lay of the land!

```bash
# Profile any data file
python3 -m validation_framework.cli profile data.csv

# Generates:
# - Interactive HTML report with charts
# - Auto-generated validation config
# - Quality metrics and suggestions
```

**Features:**
- 📈 Interactive charts with quality metrics
- 🔍 Type inference (known vs inferred)
- 📊 Statistical distributions and correlations
- 💡 Auto-generated validation suggestions
- 📱 Mobile-responsive design
- 🗂️ Table of contents for easy navigation

**Learn More:** [Data Profiling Guide →](docs/using-datak9/data-profiling.md)

---

## 📚 Documentation

### New DataK9 Documentation

**Using DataK9** (For all users):
- **[5-Minute Quickstart](docs/getting-started/quickstart-5min.md)** - Get started in 5 minutes
- **[Configuration Guide](docs/using-datak9/configuration-guide.md)** - Complete YAML reference
- **[Validation Catalog](docs/using-datak9/validation-catalog.md)** - All 35+ validation types
- **[DataK9 Studio Guide](docs/using-datak9/studio-guide.md)** - Visual configuration IDE
- **[Data Profiling](docs/using-datak9/data-profiling.md)** - Analyze data before validation
- **[Reading Reports](docs/using-datak9/reading-reports.md)** - Understanding validation results
- **[Performance Tuning](docs/using-datak9/performance-tuning.md)** - Optimize for speed and memory
- **[Large Files](docs/using-datak9/large-files.md)** - Handling 200GB+ datasets
- **[AutoSys Integration](docs/using-datak9/autosys-integration.md)** - Enterprise job scheduling
- **[CI/CD Integration](docs/using-datak9/cicd-integration.md)** - GitHub Actions, GitLab, Jenkins
- **[Best Practices](docs/using-datak9/best-practices.md)** - ERROR vs WARNING, production patterns

**For Developers** (Technical users):
- **[Architecture](docs/for-developers/architecture.md)** - System design and components
- **[Custom Validations](docs/for-developers/custom-validations.md)** - Build your own rules
- **[Custom Loaders](docs/for-developers/custom-loaders.md)** - Add file format support
- **[Custom Reporters](docs/for-developers/custom-reporters.md)** - Create output formats
- **[API Reference](docs/for-developers/api-reference.md)** - Complete Python API
- **[Testing Guide](docs/for-developers/testing-guide.md)** - Test your customizations
- **[Contributing](docs/for-developers/contributing.md)** - Contribute to DataK9
- **[Design Patterns](docs/for-developers/design-patterns.md)** - Patterns used in DataK9

**Reference** (Quick lookup):
- **[CLI Reference](docs/reference/cli-reference.md)** - All command-line options
- **[Validation Reference](docs/reference/validation-reference.md)** - Quick validation lookup
- **[YAML Reference](docs/reference/yaml-reference.md)** - Complete YAML syntax
- **[Error Codes](docs/reference/error-codes.md)** - Exit codes and error messages
- **[Glossary](docs/reference/glossary.md)** - DataK9 terminology

**Industry Examples**:
- **[Finance](docs/examples/finance.md)** - Banking, trading, AML validation
- **[Healthcare](docs/examples/healthcare.md)** - HIPAA-compliant patient data
- **[E-Commerce](docs/examples/ecommerce.md)** - Customer, order, inventory validation

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
python3 -m validation_framework.cli validate config.yaml

if [ $? -ne 0 ]; then
  echo "DataK9 validation failed - blocking load"
  exit 1  # Fail AutoSys job
fi

# Proceed with load only if DataK9 approves
./load_data.sh
```

**See [AutoSys Integration Guide](docs/using-datak9/autosys-integration.md) for complete examples**

---

## 📊 Available Validations

### File-Level Checks (3)
- **EmptyFileCheck** - File not empty
- **RowCountRangeCheck** - Row count within range
- **FileSizeCheck** - File size limits

### Schema Checks (2)
- **SchemaMatchCheck** - Exact schema match
- **ColumnPresenceCheck** - Required columns exist

### Field-Level Checks (5)
- **MandatoryFieldCheck** - Required fields not null
- **RegexCheck** - Pattern validation
- **ValidValuesCheck** - Values in allowed list
- **RangeCheck** - Numeric ranges
- **DateFormatCheck** - Date format validation

### Record-Level Checks (3)
- **DuplicateRowCheck** - Detect duplicates
- **BlankRecordCheck** - Find empty rows
- **UniqueKeyCheck** - Unique constraints

### Conditional Validation (1)
- **ConditionalValidation** - If-then-else logic
- **Inline Conditions** - Apply any validation conditionally

### Advanced Checks (6)
- **StatisticalOutlierCheck** - Detect anomalies
- **CrossFieldComparisonCheck** - Field relationships
- **FreshnessCheck** - Data recency
- **CompletenessCheck** - Field completeness %
- **StringLengthCheck** - String length limits
- **NumericPrecisionCheck** - Decimal precision

### Cross-File Validations (3)
- **ReferentialIntegrityCheck** - Foreign key relationships between files
- **CrossFileComparisonCheck** - Compare aggregates across files
- **CrossFileDuplicateCheck** - Duplicates across multiple files

### Database Validations (3)
- **SQLCustomCheck** - Custom SQL-based validations
- **DatabaseReferentialIntegrityCheck** - Database foreign keys
- **DatabaseConstraintCheck** - Database constraint validation

### Temporal/Historical Validations (2)
- **BaselineComparisonCheck** - Compare against historical averages
- **TrendDetectionCheck** - Detect unusual growth/decline rates

### Statistical Validations (3)
- **DistributionCheck** - Validate statistical distributions
- **CorrelationCheck** - Column correlation validation
- **AdvancedAnomalyDetectionCheck** - Multiple anomaly detection methods

**See [Validation Catalog](docs/using-datak9/validation-catalog.md) for complete reference of all 35+ validations**

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

# Parquet support (highly recommended for large files)
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

# With custom output directory
python3 -m validation_framework.cli validate config.yaml --output-dir reports/

# With verbose output
python3 -m validation_framework.cli validate config.yaml --verbose

# Both HTML and JSON reports
python3 -m validation_framework.cli validate config.yaml \
  --output-dir reports/
```

### List Available Validations

```bash
# List all validations
python3 -m validation_framework.cli list-validations

# Filter by category
python3 -m validation_framework.cli list-validations --category field-level
```

### Exit Codes

DataK9 uses standard exit codes for integration:

- `0` - Validation passed (all ERROR validations passed; WARNINGs OK)
- `1` - Validation failed (ERROR-severity issues found)
- `2` - Command error (bad config, file not found, etc.)

**See [Error Codes Reference](docs/reference/error-codes.md) for complete guide**

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

**[Learn more about the architecture →](docs/for-developers/architecture.md)**

---

## 🚀 Performance

### Large File Support

**Tested with 200GB+ files:**
- ✅ Memory-efficient chunked processing
- ✅ Only one chunk in memory at a time
- ✅ Configurable chunk size
- ✅ Parquet format recommended for best performance (10x faster than CSV)

### Performance Characteristics

| File Size | Format  | Chunk Size | Time        | Memory  |
|-----------|---------|------------|-------------|---------|
| 1 MB      | CSV     | 1,000      | < 1 second  | < 10 MB |
| 100 MB    | CSV     | 10,000     | ~10 seconds | ~50 MB  |
| 1 GB      | Parquet | 50,000     | ~2 minutes  | ~200 MB |
| 50 GB     | Parquet | 100,000    | ~1 hour     | ~400 MB |
| 200 GB    | Parquet | 100,000    | ~4 hours    | ~400 MB |

**[Performance optimization guide →](docs/using-datak9/performance-tuning.md)**

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
condition: success(VALIDATE_DATA)  # Only runs if DataK9 approves
```

**[Complete AutoSys integration guide →](docs/using-datak9/autosys-integration.md)**

### CI/CD Pipeline

```yaml
# GitHub Actions
- name: DataK9 Validation
  run: |
    python3 -m validation_framework.cli validate config.yaml
    if [ $? -ne 0 ]; then
      echo "DataK9 validation failed"
      exit 1
    fi
```

**[Complete CI/CD integration guide →](docs/using-datak9/cicd-integration.md)**

### Python Script

```python
from validation_framework.core.engine import ValidationEngine

# Run DataK9 validation
engine = ValidationEngine.from_config("config.yaml")
report = engine.run()

# Check results
if report.overall_status != "PASSED":
    raise ValueError(f"DataK9 validation failed: {report.total_errors} errors")
```

**[Complete API reference →](docs/for-developers/api-reference.md)**

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

**[Complete Testing Guide →](docs/for-developers/testing-guide.md)**

---

## 🤝 Contributing

Contributions welcome! See **[Contributing Guide](docs/for-developers/contributing.md)** for:
- Setting up development environment
- Creating custom validations
- Writing tests
- Contribution guidelines

---

## 📖 Quick Links

### Getting Started
- [Installation & Quick Start](docs/getting-started/quickstart-5min.md)
- [Configuration Guide](docs/using-datak9/configuration-guide.md)
- [Validation Catalog](docs/using-datak9/validation-catalog.md)
- [DataK9 Studio Guide](docs/using-datak9/studio-guide.md)

### Advanced Topics
- [Performance Tuning](docs/using-datak9/performance-tuning.md)
- [Large Files (200GB+)](docs/using-datak9/large-files.md)
- [AutoSys Integration](docs/using-datak9/autosys-integration.md)
- [CI/CD Integration](docs/using-datak9/cicd-integration.md)

### Reference
- [CLI Reference](docs/reference/cli-reference.md)
- [Validation Reference](docs/reference/validation-reference.md)
- [YAML Reference](docs/reference/yaml-reference.md)
- [Error Codes](docs/reference/error-codes.md)

### Development
- [Architecture](docs/for-developers/architecture.md)
- [Custom Validations](docs/for-developers/custom-validations.md)
- [API Reference](docs/for-developers/api-reference.md)
- [Testing Guide](docs/for-developers/testing-guide.md)

### Support
- [GitHub Issues](https://github.com/danieledge/data-validation-tool/issues)
- [Discussion Forum](https://github.com/danieledge/data-validation-tool/discussions)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👤 Author

**Daniel Edge**

---

## 🌟 Why DataK9?

- ✅ **Production Ready** - Used for enterprise data pipelines
- ✅ **Well Documented** - Comprehensive documentation for all user levels
- ✅ **Actively Maintained** - Regular updates and improvements
- ✅ **Extensible** - Easy to add custom validations
- ✅ **Scalable** - Handles files from KB to 200GB+
- 🐕 **Vigilant Guardian** - Like a K9 unit, always on watch for data quality issues

**Ready to get started?** → **[5-Minute Quickstart](docs/getting-started/quickstart-5min.md)**

---

<div align="center">
  <strong>🐕 DataK9 - Your loyal guardian for data quality</strong>
</div>
