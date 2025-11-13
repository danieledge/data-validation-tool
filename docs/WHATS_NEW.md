# What's New

This document tracks new features, improvements, and changes in the Data Validation Tool.

---

## Version 2.0.0 (Current) - November 2025

### 🎉 Major New Features

#### 📊 Data Profiling
Comprehensive data analysis and exploration capabilities added to understand your data before validation.

**Key Features:**
- **Automatic Type Inference** - Detects numeric, string, datetime, boolean, and categorical columns
- **Statistical Analysis** - Calculates distributions, min/max, mean, median, quartiles
- **Quality Metrics** - Completeness, uniqueness, validity, consistency scores
- **Pattern Detection** - Identifies common patterns, formats, and anomalies
- **Interactive HTML Reports** - Beautiful, mobile-responsive reports with charts
- **Suggested Validations** - Auto-generates YAML validation configs based on analysis
- **Memory Efficient** - Handles 200GB+ files with constant ~400MB memory usage
- **Format Support** - CSV, Parquet, JSON, Excel

**Usage:**
```bash
dqa profile data.csv
dqa profile data.csv --format html --output report.html
```

**Documentation:**
- [Complete Profiling Guide](DATA_PROFILING.md)
- [View Live Examples](https://htmlpreview.github.io/?https://github.com/danieledge/data-validation-tool/blob/main/docs/example_profile_report.html)

---

### ✨ Enhancements

#### Enhanced Empty File Detection
The `EmptyFileCheck` validation now supports detecting both literal empty files (0 bytes) AND header-only files.

**New Parameter:**
- `check_data_rows` (boolean) - When `true`, verifies file has at least one data row, not just headers

**Example:**
```yaml
# Check for both empty files AND header-only files
- type: "EmptyFileCheck"
  severity: "ERROR"
  params:
    check_data_rows: true
```

**Supported Formats:** CSV, Excel, JSON, Parquet

---

### 🎨 User Experience Improvements

#### Mobile-Responsive HTML Reports
- Profile reports now render beautifully on tablets and mobile phones
- Responsive grids, fonts, and scrollable tables
- Touch-friendly navigation

#### Table of Contents in Reports
- All HTML profile reports now include an interactive Table of Contents
- Quick navigation to any section via anchor links

#### Improved File Size Display
- File sizes now display in appropriate units (B, KB, MB, GB)
- No more "0.00 MB" for small files

#### Enhanced Chart Loading
- Fallback CDN loading for Chart.js for better reliability
- Graceful error handling if charts fail to load
- User-friendly error messages

---

### 📚 Documentation Updates

#### New Documentation
- [Data Profiling Guide](DATA_PROFILING.md) - Complete profiling documentation
- [What's New](WHATS_NEW.md) - This changelog document
- Enhanced [Validation Catalog](VALIDATION_CATALOG.md) with all built-in validations

#### Reorganized Documentation
- [Getting Started](GETTING_STARTED.md) - Quick setup guide
- [User Guide](USER_GUIDE.md) - Comprehensive usage guide
- [Advanced Configuration](ADVANCED_CONFIGURATION.md) - Power user features
- [Examples & Recipes](EXAMPLES_AND_RECIPES.md) - Common patterns
- [Technical Architecture](TECHNICAL_ARCHITECTURE.md) - System design
- [Developer Guide](DEVELOPER_GUIDE.md) - Extending the framework

---

## Version 1.5.0 - October 2025

### Initial Features

#### Core Validation Engine
- YAML-based validation configuration
- Batch processing with chunked data loading
- Support for CSV, Excel, JSON, Parquet formats
- Flexible rule engine with severity levels (ERROR, WARNING, INFO)
- Detailed validation reports in JSON, HTML, and markdown

#### Built-in Validation Rules

**Column Validations:**
- NotNullCheck - Required field validation
- UniqueCheck - Uniqueness constraints
- DataTypeCheck - Type validation
- RegexPatternCheck - Pattern matching
- RangeCheck - Numeric range validation
- AllowedValuesCheck - Enumeration validation
- StringLengthCheck - Length constraints
- DateFormatCheck - Date/time validation
- EmailFormatCheck - Email validation
- CrossFieldComparisonCheck - Compare columns

**Row Validations:**
- RequiredFieldsCombinationCheck - Conditional requirements
- MutuallyExclusiveFieldsCheck - Mutual exclusivity
- ConditionalValidationCheck - If-then rules

**File Validations:**
- EmptyFileCheck - Empty file detection
- RowCountRangeCheck - Row count constraints
- FileSizeCheck - File size limits

**Dataset Validations:**
- DuplicateRowCheck - Duplicate detection
- OutlierDetectionCheck - Statistical outliers

#### Command-Line Interface
```bash
dqa validate config.yaml data.csv
dqa init
```

#### Developer Features
- Custom validation rule creation via base classes
- Plugin architecture for extensions
- Comprehensive error handling
- Detailed logging

---

## Upcoming Features (Roadmap)

See our [GitHub Issues](https://github.com/danieledge/data-validation-tool/issues) for planned features and enhancements.

### Planned for Version 2.1.0

- **Cross-File Validations** - Validate relationships between multiple datasets
- **Database Connectivity** - Direct database validation support
- **Temporal Validations** - Compare data against historical baselines
- **Statistical Validations** - Distribution tests, seasonality detection
- **SQL-based Custom Checks** - SQL query validations for databases

### Under Consideration

- Cloud storage integration (S3, Azure Blob, GCS)
- Data lineage tracking
- Validation scheduling and automation
- Web UI for configuration management
- REST API for validation as a service

---

## Migration Guides

### Upgrading to 2.0.0

**New Dependencies:**
Version 2.0.0 adds data profiling capabilities which require additional packages:

```bash
pip install --upgrade -r requirements.txt
```

**New packages:** scipy (for statistical analysis), jinja2 (for HTML templating)

**Breaking Changes:** None - All 1.x configurations remain compatible

**New Capabilities:**
- Use `dqa profile` command for data analysis
- Enhanced `EmptyFileCheck` with `check_data_rows` parameter

---

## Getting Help

- **Documentation:** [README.md](../README.md)
- **Issues:** [GitHub Issues](https://github.com/danieledge/data-validation-tool/issues)
- **Examples:** [Examples & Recipes](EXAMPLES_AND_RECIPES.md)
