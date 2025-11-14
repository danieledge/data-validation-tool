# What's New

This document tracks new features, improvements, and changes in the Data Validation Tool.

---

## Version 2.5.0 (Current) - January 2025

### 📋 Validation Templates & EmptyFileCheck Clarification

**One-click validation setup!** Pre-configured templates let you add complete validation suites instantly, plus clarified how EmptyFileCheck handles headers.

**Validation Templates:**
- **🛡️ Essential File Checks** - Minimum validations every file needs (2 checks)
  - `EmptyFileCheck` - Prevents processing files with no data
  - `RowCountRangeCheck` - Ensures expected data volume
- **✅ Data Quality Basics** - Common integrity checks (4 checks)
  - `MandatoryFieldCheck` - Ensures critical fields populated
  - `UniqueKeyCheck` - Validates primary key uniqueness
  - `DuplicateRowCheck` - Detects duplicate records
  - `BlankRecordCheck` - Finds completely empty rows
- **🏗️ Schema Validation Suite** - Complete structure checks (3 checks)
  - `ColumnPresenceCheck` - Verifies required columns exist
  - `DataTypeCheck` - Validates column data types
  - `SchemaMatchCheck` - Enforces exact schema compliance
- **🚀 Production Ready** - Comprehensive suite (9 checks total)
  - Combines all Essential + Quality + Schema validations
  - Pre-configured with sensible defaults and severity levels

**How to Use Templates:**
1. Navigate to any file configuration
2. Click "Use Template" button (next to "Add Validation")
3. Select from 4 pre-configured templates
4. All validations added instantly with proper defaults
5. Customize parameters as needed

**EmptyFileCheck Clarification:**
- Enhanced description now explains header detection logic
- **CSV files**: If `has_header: true` in config, first row excluded from count
- **CSV files**: If `has_header: false`, all rows counted as data
- **Excel files**: First row treated as header by default
- Check fails if zero data rows remain after excluding headers
- Saves processing time by failing immediately on empty files

**Template Modal Design:**
- Clean card-based layout with emoji icons
- Color-coded borders matching validation categories
- Shows all included validations for each template
- One-click application with success confirmation
- Hover states for better interactivity

**Benefits:**
- ⚡ **Quick Setup** - Add 9 validations with one click
- 📚 **Best Practices** - Templates based on common patterns
- 🎯 **Consistent Standards** - Ensures minimum validation coverage
- 🚀 **Production Ready** - Complete suite for production use

---

## Version 2.4.0 - January 2025

### 📚 Comprehensive Helper Text & Guidance System

**Every setting and validation now includes detailed, contextual help!** Clean, crisp explanations throughout the entire config builder, making it easier than ever to configure complex validation rules.

**Advanced Settings Guidance:**
- **Chunk Size Recommendations** - Visual guide with specific values by file size:
  - 💾 Small files (<100K rows): 5,000-10,000
  - 📊 Medium files (100K-1M rows): 10,000-50,000
  - 🗄️ Large files (>1M rows): 50,000-100,000
  - ⚡ Low memory systems: 1,000-5,000
  - Explains memory/performance tradeoffs clearly
- **Max Sample Failures** - How to prevent overwhelming logs with thousands of errors
- **Log Levels** - Detailed descriptions: DEBUG (verbose), INFO (recommended), WARNING, ERROR
- **Fail Fast** - When to use immediate stopping vs complete validation reports

**Enhanced Validation Descriptions:**
- **21 Comprehensive Descriptions** - Every validation type now includes:
  - **Bold Purpose Statement** - What the validation does in one sentence
  - **Detailed Functionality** - How it works and what it checks
  - **Use Case Guidance** - When and why to use this validation
  - **Real-World Examples** - Practical scenarios and sample values
- **Advanced Validations** - Extra detail for complex types:
  - `StatisticalOutlierCheck`: Explains 3 standard deviation threshold (±3σ)
  - `ReferentialIntegrityCheck`: Foreign key relationship validation details
  - `DistributionCheck`: Statistical distribution pattern validation
  - `CorrelationCheck`: Field relationship consistency monitoring

**Field-Level Help Throughout:**
- **File Format Details** - CSV, Excel, JSON, Parquet format explanations
- **Severity Guidance** - Clear ERROR vs WARNING use cases in both modal and cards
- **Parameter Context** - Specific guidance for each validation type's parameters
- **Modal Catalog** - Improved short descriptions with technical precision

**Visual Enhancements:**
- Consistent helper text styling across all sections
- Color-coded info boxes for critical guidance (chunk size)
- Important terms highlighted with `<strong>` tags
- Proper line-height and spacing for multi-line helpers

---

## Version 2.3.0 - January 2025

### 🎨 Visual Config Builder v3 - Complete UI/UX Redesign

**Major redesign with three-panel layout and validation wizard!** Professional, modern interface inspired by leading open-source config builders.

**Clarity-Focused Theme & Multi-Selection:**

**Multiple Validation Selection:**
- **Multi-Select Modal** - Click to toggle multiple validations at once
- **Smart Button Text** - Shows count when multiple selected ("Add 3 Validations")
- **Batch Addition** - Add all selected validations with single click
- **Clear Feedback** - Visual toggle states with color-coded borders

**Clarity-Focused Theme Overhaul:**
- **Enhanced Contrast** - Improved text and UI element visibility (WCAG AA compliant)
- **Better Typography** - 15px base font, 1.6 line-height, refined letter-spacing
- **Improved Icon Visibility** - Icons now use proper on-container colors for maximum contrast
- **Refined Color Palette** - Higher contrast validation type colors (#60A5FA, #A78BFA, #34D399, #FBBF24, #F472B6, #2DD4BF)
- **Enhanced Spacing** - Increased padding throughout (sidebar: 280px, content: 32px, cards: 20px)
- **Better Visual Hierarchy** - Larger titles (28px page, 22px modal), improved card borders (1.5px)
- **Smoother Interactions** - Subtle card lift on hover, refined transitions, better elevation shadows
- **Professional Polish** - Rounded corners (14-20px), improved button styling, enhanced modal design

**NEW in v3 - Complete Interface Overhaul:**

**Three-Panel Layout:**
- **Sidebar Navigation** (280px) - Job settings, files list with badges, advanced settings
- **Main Workspace** (fluid) - Form-based configuration with clear sections
- **Live Preview Panel** (400px) - Real-time YAML preview with syntax highlighting
- **Mobile-First Design** - Hidden sidebar with hamburger menu, collapsible preview panel

**Validation Type Selection Wizard:**
- **21 Validation Types** organized into 6 color-coded categories:
  - 📄 **File Validations** (Blue) - EmptyFileCheck, RowCountRangeCheck, FileSizeCheck
  - 🏗️ **Schema Validations** (Purple) - SchemaMatchCheck, ColumnPresenceCheck, DataTypeCheck
  - ✏️ **Field Validations** (Green) - MandatoryFieldCheck, RegexCheck, ValidValuesCheck, RangeCheck, DateFormatCheck, StringLengthCheck, CompletenessCheck
  - 📋 **Record Validations** (Orange) - DuplicateRowCheck, BlankRecordCheck, UniqueKeyCheck
  - 🔗 **Cross-File Validations** (Pink) - ReferentialIntegrityCheck, CrossFileComparisonCheck, CrossFileDuplicateCheck
  - 📊 **Statistical Validations** (Teal) - StatisticalOutlierCheck, DistributionCheck, CorrelationCheck
- **Interactive Modal** - Visual selection with descriptions, severity picker (ERROR/WARNING)
- **Smart Selection** - Disabled confirm button until validation type selected
- **Hover States** - Clear visual feedback on hover and selection

**Design Improvements:**
- **Modern Card-Based UI** - Validation cards with color-coded left borders
- **Hierarchical Navigation** - Collapsible sidebar with nested items
- **Responsive Breakpoints** - Mobile (<768px), Tablet (768-1024px), Desktop (>1024px)
- **Professional Color Palette** - Dark theme with distinct category colors
- **Smooth Animations** - Fade-in modals, hover transitions, mobile sidebar slide
- **Touch-Friendly** - 44px minimum touch targets on mobile

**UX Research Foundation:**
Analyzed 6 leading open-source projects (n8n.io, OpenAPI-GUI, Grafana, Google YAML Editor, HeyForm, GrapesJS) to identify best UX patterns and implement proven design solutions.

**How to Use:**
```bash
# Open the config builder
open config-builder/index.html

# Features:
# 1. Click "Add Your First File" in Job Settings
# 2. Click "Add Validation" to open the wizard
# 3. Select validation type from organized categories
# 4. Choose severity level (ERROR/WARNING)
# 5. Configure parameters in form fields
# 6. See real-time YAML preview in right panel
# 7. Download generated YAML configuration
```

**Benefits:**
- ✅ **Intuitive Navigation** - Three-panel layout matches industry standards
- ✅ **Visual Organization** - Color-coded validation categories
- ✅ **Clear Workflows** - Wizard-based validation selection
- ✅ **Professional Design** - Modern, polished interface
- ✅ **Mobile Optimized** - Full responsive design with proper mobile UX
- ✅ **Real-Time Feedback** - Live YAML preview updates as you configure
- ✅ **Research-Backed** - UX patterns from leading open-source projects

---

## Version 2.2.0 - January 2025

### 🎨 Visual Config Builder v2 - Complete Overhaul

**No-code validation configuration!** Comprehensive, production-ready config builder with advanced features.

**NEW in v2 - All 4 Enhancement Phases Implemented:**

**Phase 1 - Critical Features:**
- **Multiple File Support** - Add/remove files dynamically, configure each independently
- **Template Library** - 5 generic templates (Blank, Single File - Basic/Complete, Multiple Files, Schema Validation)
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
- ✅ **Production-Ready** - Advanced settings, multiple files, generic template library
- ✅ **No Coding Required** - Visual interface with guided parameter forms
- ✅ **Save & Share** - Auto-save, shareable URLs, saved config manager
- ✅ **Mobile-Optimized** - Full responsive design with stacked buttons, touch-friendly controls (44px targets)
- ✅ **35+ Validations** - All validation types with tooltips and examples
- ✅ **Smart Workflows** - Import existing configs, start from templates, keyboard shortcuts
- ✅ **Clear UI** - Severity dropdown with labels and color-coding to prevent confusion
- ✅ **Perfect for All Users** - Business analysts, data engineers, developers

**Recent Improvements (v2.2.1):**
- 🎯 **Generic Templates** - Replaced use-case specific templates with flexible, reusable ones
- 📱 **Enhanced Mobile UX** - Buttons stack vertically, proper spacing, 44px touch targets
- 🎨 **Clearer Severity Selection** - Added "Severity:" label and emoji indicators (🔴 ERROR, 🟡 WARNING)
- ✅ **Better Accessibility** - All interactive elements meet touch target size standards

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
