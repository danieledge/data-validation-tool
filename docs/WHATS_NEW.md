# What's New

This document tracks new features, improvements, and changes in the Data Validation Tool.

---

## Version 2.2.0 (Current) - January 2025

### 🎨 Visual Config Builder v2 - Complete Overhaul

**No-code validation configuration!** Comprehensive, production-ready config builder with advanced features.

**NEW in v2 - All 4 Enhancement Phases Implemented:**

**Phase 1 - Critical Features:**
- **Multiple File Support** - Add/remove files dynamically, configure each independently
- **Template Library** - 5 pre-built templates (Basic Quality, E-Commerce, Financial, CRM, Data Warehouse)
- **Import YAML** - Load existing configurations for editing
- **Advanced Settings Panel** - Configure chunk_size, max_sample_failures, fail_fast, log_level

**Phase 2 - UX Improvements:**
- **Auto-Save** - Configuration saved to browser localStorage every 30 seconds
- **Parameter Validation** - Required field indicators and type-specific inputs (text, number, boolean, select, file_picker, list)
- **Cross-File Reference Picker** - Dropdown to select reference files for referential integrity checks
- **Summary Dashboard** - Real-time counts of files, validations, errors, and warnings

**Phase 3 - Polish:**
- **YAML Syntax Highlighting** - Color-coded preview with keys, values, comments, strings, numbers
- **Keyboard Shortcuts** - Ctrl+S (save), Ctrl+D (download), Ctrl+I (import), ? (help)
- **Enhanced Mobile Layout** - Tab switcher, touch-friendly buttons (44px minimum), responsive grids
- **Validation Tooltips** - Help icons with examples and hints for each validation type

**Phase 4 - Advanced Features:**
- **Shareable URLs** - Generate URL with base64-encoded configuration in hash for sharing
- **Load from URL** - Automatically loads configuration from shared URL
- **Saved Configurations Manager** - Browse and load previously saved configurations
- **Modal Dialogs** - Template selector, YAML import, share URL, saved configs, help

**How to Use:**
```bash
# Option 1: Online version (no download needed)
# Visit: https://raw.githack.com/danieledge/data-validation-tool/main/docs/config-builder.html

# Option 2: Local version
open docs/config-builder.html

# Build your validation config visually
# Download the generated YAML file
# Run validation
python3 -m validation_framework.cli validate config.yaml --html report.html
```

**Live Demo:**
- **Interactive Config Builder**: https://raw.githack.com/danieledge/data-validation-tool/main/docs/config-builder.html
- **GitHub Source**: https://github.com/danieledge/data-validation-tool/blob/main/docs/config-builder.html

**Benefits:**
- ✅ **Production-Ready** - Advanced settings, multiple files, template library
- ✅ **No Coding Required** - Visual interface with guided parameter forms
- ✅ **Save & Share** - Auto-save, shareable URLs, saved config manager
- ✅ **Mobile-Friendly** - Full responsive design with touch-optimized controls
- ✅ **35+ Validations** - All validation types with tooltips and examples
- ✅ **Smart Workflows** - Import existing configs, start from templates, keyboard shortcuts
- ✅ **Perfect for All Users** - Business analysts, data engineers, developers

---

### 🧪 Comprehensive Testing Suite

**115+ tests with 48% code coverage** across all framework components.

**New Test Modules:**
- **Profiler Tests** (49 tests) - Type detection, statistics, quality metrics, HTML reports
- **Testing Documentation** - Complete guide for running tests and writing new ones

**Test Coverage:**
- Profiler engine: 94%
- HTML reporter: 82%
- Profile results: 90%
- Validation registry: 100%

**Features:**
- Unit, integration, and end-to-end tests
- Parameterized testing with pytest
- Fixture-based test data management
- CI/CD integration examples
- Comprehensive troubleshooting guide

**Documentation:**
- **[Testing Guide](TESTING.md)** - Complete testing documentation
  - How to run tests (all, specific files, with coverage)
  - Test organization and structure
  - Writing new tests (AAA pattern, fixtures, mocking)
  - CI/CD integration
  - Best practices

**Running Tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=validation_framework --cov-report=html

# Run specific test module
pytest tests/test_profiler.py -v

# Run in parallel
pytest -n 4
```

---

### 📚 Enhanced Documentation

**New Documentation:**
- **[Testing Guide](TESTING.md)** - 700+ lines covering test suite, writing tests, CI/CD
- Visual Config Builder documentation in README

**Improvements:**
- Updated README with config builder quick start
- Updated test counts (102 → 115+ tests)
- Added config builder to quick start section

---

### 🔧 Improvements

**Code Quality:**
- All 49 profiler tests passing
- Improved type detection accuracy
- Better error handling in statistical calculations

**Developer Experience:**
- Comprehensive test fixtures
- Clear test naming conventions
- Documented test patterns and best practices

---

### 📈 Statistics

- **Total Validations**: 35+ validation types
- **Total Tests**: 115+ (up from 102)
- **Code Coverage**: 48% (above 43% target)
- **Documentation Pages**: 12 comprehensive guides
- **Test Modules**: 4 main test files
- **New Features**: Visual config builder, comprehensive testing

---

## Version 2.1.0 - November 2025

### 🎉 Major New Features

#### 📁 Cross-File Validations
Validate relationships and consistency across multiple data files.

**New Validations:**
- **ReferentialIntegrityCheck** - Validate foreign key relationships between files
- **CrossFileComparisonCheck** - Compare aggregates between files
- **CrossFileDuplicateCheck** - Detect duplicates across multiple files

**Use Cases:**
- Ensure customer IDs in orders file exist in customers file
- Validate total amounts match across related files
- Check for duplicate keys across archive and active files

**Example:**
```yaml
- type: "ReferentialIntegrityCheck"
  severity: "ERROR"
  params:
    foreign_key: "customer_id"
    reference_file: "customers.csv"
    reference_key: "id"
```

---

#### 🗄️ Database Connectivity
Direct database validation support for PostgreSQL, MySQL, SQL Server, Oracle, and SQLite.

**New Validations:**
- **SQLCustomCheck** - Execute custom SQL queries for validation
- **DatabaseReferentialIntegrityCheck** - Check foreign keys within databases
- **DatabaseConstraintCheck** - Validate database constraints

**New Components:**
- **DatabaseLoader** - Load data from databases in chunks
- Support for all major database engines

**Use Cases:**
- Validate data in databases without extracting to files
- Execute complex SQL-based business rules
- Check referential integrity directly in the database

**Example:**
```yaml
- type: "SQLCustomCheck"
  severity: "ERROR"
  params:
    connection_string: "postgresql://user:pass@localhost/db"
    sql_query: |
      SELECT customer_id, email
      FROM customers
      WHERE email NOT LIKE '%@%'
```

**Installation:**
```bash
pip install sqlalchemy psycopg2-binary  # PostgreSQL
pip install sqlalchemy pymysql          # MySQL
```

---

#### ⏰ Temporal/Historical Validations
Compare current data against historical baselines to detect anomalies.

**New Validations:**
- **BaselineComparisonCheck** - Compare metrics against historical averages
- **TrendDetectionCheck** - Detect unusual growth/decline rates

**Use Cases:**
- Detect unusual drops/spikes in row counts
- Alert on unexpected data volume changes
- Monitor business metrics over time

**Example:**
```yaml
- type: "BaselineComparisonCheck"
  severity: "WARNING"
  params:
    metric: "count"
    baseline_file: "historical_counts.csv"
    lookback_days: 30
    tolerance_pct: 20
```

---

#### 📊 Advanced Statistical Validations
Sophisticated statistical tests for data quality.

**New Validations:**
- **DistributionCheck** - Validate data follows expected distributions (normal, uniform, exponential)
- **CorrelationCheck** - Validate correlations between columns
- **AdvancedAnomalyDetectionCheck** - Multiple anomaly detection methods (IQR, Z-score, Isolation Forest)

**Methods:**
- Statistical distribution tests (Shapiro-Wilk, Kolmogorov-Smirnov)
- Correlation analysis (Pearson, Spearman, Kendall)
- Machine learning-based anomaly detection

**Use Cases:**
- Detect when data patterns change unexpectedly
- Monitor expected relationships between variables
- Find fraudulent transactions or data entry errors

**Example:**
```yaml
- type: "DistributionCheck"
  severity: "WARNING"
  params:
    column: "age"
    expected_distribution: "normal"

- type: "CorrelationCheck"
  severity: "WARNING"
  params:
    column1: "price"
    column2: "quantity_sold"
    min_correlation: -0.8

- type: "AdvancedAnomalyDetectionCheck"
  severity: "WARNING"
  params:
    column: "price"
    method: "isolation_forest"
    max_anomaly_pct: 2
```

**Installation:**
```bash
pip install scipy                # For statistical tests
pip install scikit-learn         # For Isolation Forest
```

---

### 📚 Documentation Updates

- Updated [Validation Catalog](VALIDATION_CATALOG.md) with 12+ new validation types
- Added examples for all new validations
- Documented database connection strings for all supported databases
- Added statistical validation methodology documentation

---

### 📦 Dependencies

**New Optional Dependencies:**
```bash
# Database connectivity
pip install sqlalchemy psycopg2-binary pymysql pyodbc cx-Oracle

# Statistical validations
pip install scipy scikit-learn
```

All optional - only install what you need!

---

## Version 2.0.0 - November 2025

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
