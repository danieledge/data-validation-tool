# Data Validation Tool Documentation

Welcome to the comprehensive documentation for the Data Validation Tool - a production-grade Python framework for validating large-scale datasets before loading into your data warehouse or analytics platform.

## 📚 Documentation Index

### For Business Analysts
- **[Business Analyst Guide](BA_GUIDE.md)** - Define custom validations without coding
- **[Quick Start Guide](#quick-start)** - Get started in 5 minutes
- **[Validation Reference](VALIDATION_REFERENCE.md)** - Complete list of all available checks

### For Developers & Technical Users
- **[Architecture Overview](ARCHITECTURE.md)** - System design and components
- **[Technical Guide](TECHNICAL_GUIDE.md)** - Advanced usage and customization
- **[API Reference](API_REFERENCE.md)** - Python API documentation
- **[Contributing Guide](CONTRIBUTING.md)** - How to extend the framework

### Additional Resources
- **[Example Configurations](../examples/)** - Sample YAML configs
- **[Test Datasets Guide](test_datasets.md)** - Open source data for testing

---

## 🎯 What is the Data Validation Tool?

The Data Validation Tool is a robust, extensible framework that validates data quality and completeness **before** loading into your data warehouse. It helps you:

- ✅ Catch data quality issues early
- ✅ Define validation rules in simple YAML configuration
- ✅ Handle massive datasets (200GB+) efficiently
- ✅ Generate beautiful, actionable HTML reports
- ✅ Integrate into CI/CD pipelines
- ✅ Support multiple formats (CSV, Excel, Parquet, JSON)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/danieledge/data-validation-tool.git
cd data-validation-tool

# Install dependencies
pip install -r requirements.txt

# Install the tool
pip install -e .
```

### Run Your First Validation

1. **Create a YAML configuration file** (`my_validation.yaml`):

```yaml
validation_job:
  name: "My First Validation"
  version: "1.0"

  files:
    - name: "customer_data"
      path: "data/customers.csv"
      format: "csv"

      validations:
        # Check file is not empty
        - type: "EmptyFileCheck"
          severity: "ERROR"

        # Check email format
        - type: "RegexCheck"
          severity: "ERROR"
          params:
            field: "email"
            pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

        # Check age is reasonable
        - type: "RangeCheck"
          severity: "WARNING"
          params:
            field: "age"
            min_value: 18
            max_value: 120

  output:
    html_report: "validation_report.html"
    json_summary: "validation_summary.json"
    fail_on_error: true
```

2. **Run the validation**:

```bash
python3 -m validation_framework.cli validate my_validation.yaml
```

3. **View the report** - Open `validation_report.html` in your browser to see a beautiful dark-themed report with all validation results.

---

## 📊 Key Features

### 1. **Handles Large Datasets**
- Chunked processing for 200GB+ files
- Memory-efficient streaming
- Configurable chunk sizes

### 2. **22 Built-in Validation Types**

#### File-Level Checks (3)
- Empty file detection
- Row count validation
- File size limits

#### Schema Checks (2)
- Column presence
- Schema matching

#### Field-Level Checks (5)
- Mandatory field validation
- Regex pattern matching
- Value range checks
- Date format validation
- Allowed/blocked value lists

#### Record-Level Checks (3)
- Duplicate detection
- Blank record identification
- Unique key constraints

#### BA-Friendly Custom Checks (3 - No Coding!)
- Custom regex patterns
- Business rule expressions
- Reference data lookups

#### Advanced Quality Checks (6 - NEW!)
- Statistical outlier detection (Z-score, IQR)
- Cross-field comparison
- Data freshness validation
- Completeness percentage
- String length constraints
- Numeric precision validation

### 3. **Modern, Mobile-Friendly Reports**
- Dark theme (Tokyo Night color scheme)
- Responsive design for mobile and desktop
- Auto-expanding failed validations
- Clear error visualization
- Printable reports

### 4. **Extensible Architecture**
- Add custom validation types
- Plugin-based system
- Registry pattern for discovery

### 5. **Multiple Format Support**
- CSV (any delimiter)
- Excel (XLS, XLSX)
- Parquet
- JSON
- Custom formats

---

## 💡 Common Use Cases

### Financial Data Validation
```yaml
validations:
  # Account balance must be non-negative
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule: "account_balance >= 0"
      description: "Account balance cannot be negative"

  # UK sort code format
  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "sort_code"
      pattern: "^[0-9]{2}-[0-9]{2}-[0-9]{2}$"
```

### Customer Data Validation
```yaml
validations:
  # Email format
  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "email"
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  # Valid countries only
  - type: "InlineLookupCheck"
    severity: "ERROR"
    params:
      field: "country_code"
      check_type: "allow"
      reference_values: ["US", "UK", "CA", "AU", "DE", "FR"]
```

### Transaction Data Validation
```yaml
validations:
  # Transaction amount must be positive
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule: "amount > 0"
      description: "Transaction amount must be positive"

  # Date cannot be in future
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule: "transaction_date <= today"
      description: "Transaction date cannot be in future"
```

---

## 🔧 CLI Commands

### Validate Data
```bash
# Run validation
data-validate validate config.yaml

# With custom output directory
data-validate validate config.yaml --output-dir ./reports/

# Verbose mode
data-validate validate config.yaml --verbose
```

### List Available Validations
```bash
data-validate list-validations
```

### Generate Sample Config
```bash
data-validate init-config sample_config.yaml
```

### Check Version
```bash
data-validate version
```

---

## 📖 Next Steps

### For Business Analysts
1. Read the **[Business Analyst Guide](BA_GUIDE.md)** to learn how to define custom validations without coding
2. Check out **[Validation Reference](VALIDATION_REFERENCE.md)** for all available validation types
3. Explore the **[BA-Friendly Example Config](../examples/ba_friendly_config.yaml)**

### For Developers
1. Review the **[Architecture Overview](ARCHITECTURE.md)** to understand system design
2. Read the **[Technical Guide](TECHNICAL_GUIDE.md)** for advanced usage
3. Learn how to create custom validations in the **[Contributing Guide](CONTRIBUTING.md)**

---

## 🆘 Getting Help

- **Examples**: Check the `examples/` directory for sample configurations
- **Issues**: Report bugs at [GitHub Issues](https://github.com/danieledge/data-validation-tool/issues)
- **Validation Reference**: See [VALIDATION_REFERENCE.md](VALIDATION_REFERENCE.md) for all check types

---

## 📝 License

MIT License - Copyright 2024 Daniel Edge

---

**Happy Validating! 🎯**
