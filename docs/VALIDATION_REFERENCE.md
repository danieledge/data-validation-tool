# Validation Reference Guide

Complete reference for all 16 built-in validation types in the Data Validation Tool.

---

## Table of Contents

1. [File-Level Validations](#file-level-validations)
2. [Schema Validations](#schema-validations)
3. [Field-Level Validations](#field-level-validations)
4. [Record-Level Validations](#record-level-validations)
5. [BA-Friendly Custom Validations](#ba-friendly-custom-validations)

---

## File-Level Validations

These validations check file-level properties before processing the data.

### 1. EmptyFileCheck

**Purpose**: Detects if a file is empty (zero rows of data).

**Use Cases**:
- Ensure data files contain actual data
- Catch upstream pipeline failures
- Validate data extraction completed

**Configuration**:
```yaml
- type: "EmptyFileCheck"
  severity: "ERROR"
```

**Parameters**: None

**Example Output**:
- **Pass**: "File contains data (5,000 rows)"
- **Fail**: "File is empty (0 data rows)"

---

### 2. RowCountRangeCheck

**Purpose**: Validates that the number of rows falls within expected range.

**Use Cases**:
- Detect incomplete data loads
- Identify data volume anomalies
- Validate expected dataset size

**Configuration**:
```yaml
- type: "RowCountRangeCheck"
  severity: "WARNING"
  params:
    min_rows: 1000
    max_rows: 100000
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `min_rows` | integer | No | Minimum expected rows |
| `max_rows` | integer | No | Maximum expected rows |

**Example Output**:
- **Pass**: "Row count 5,432 is within range (1,000 - 100,000)"
- **Fail**: "Row count 500 is below minimum (expected >= 1,000)"

---

### 3. FileSizeCheck

**Purpose**: Validates file size is within acceptable limits.

**Use Cases**:
- Prevent processing of corrupt files
- Detect data volume issues
- Resource planning

**Configuration**:
```yaml
- type: "FileSizeCheck"
  severity: "WARNING"
  params:
    min_size_mb: 1
    max_size_mb: 5000
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `min_size_mb` | float | No | Minimum file size in MB |
| `max_size_mb` | float | No | Maximum file size in MB |

**Example Output**:
- **Pass**: "File size 125.43 MB is within range"
- **Fail**: "File size 0.01 MB is below minimum (1 MB)"

---

## Schema Validations

These validations check the structure and schema of the data.

### 4. SchemaMatchCheck

**Purpose**: Validates that the file schema matches expected column names and types.

**Use Cases**:
- Ensure data structure hasn't changed
- Validate ETL transformations
- Catch column renames or removals

**Configuration**:
```yaml
- type: "SchemaMatchCheck"
  severity: "ERROR"
  params:
    expected_schema:
      customer_id: "int64"
      first_name: "object"
      last_name: "object"
      email: "object"
      signup_date: "object"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `expected_schema` | dict | Yes | Column names and data types |

**Data Types**: `int64`, `float64`, `object` (string), `bool`, `datetime64`

**Example Output**:
- **Pass**: "Schema matches expected structure (5 columns)"
- **Fail**: "Missing columns: ['email', 'phone']. Extra columns: ['contact']"

---

### 5. ColumnPresenceCheck

**Purpose**: Ensures specific required columns are present.

**Use Cases**:
- Check for mandatory columns
- Validate data extract completeness
- Simpler alternative to full schema check

**Configuration**:
```yaml
- type: "ColumnPresenceCheck"
  severity: "ERROR"
  params:
    required_columns:
      - "customer_id"
      - "email"
      - "first_name"
      - "last_name"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `required_columns` | list | Yes | List of column names that must exist |

**Example Output**:
- **Pass**: "All required columns present (4/4)"
- **Fail**: "Missing required columns: ['email', 'phone']"

---

## Field-Level Validations

These validations check individual field values.

### 6. MandatoryFieldCheck

**Purpose**: Ensures critical fields do not contain null/empty values.

**Use Cases**:
- Validate primary keys are populated
- Ensure required fields have values
- Detect incomplete records

**Configuration**:
```yaml
- type: "MandatoryFieldCheck"
  severity: "ERROR"
  params:
    field: "customer_id"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field name to check |

**Example Output**:
- **Pass**: "All 5,000 rows have value for 'customer_id'"
- **Fail**: "Found 23 rows with missing/null 'customer_id'"

**Sample Failures**:
```
Row #145: Field 'customer_id' is missing or null
Row #892: Field 'customer_id' is missing or null
```

---

### 7. RegexCheck

**Purpose**: Validates field values match a regular expression pattern.

**Use Cases**:
- Validate email addresses
- Check phone number formats
- Ensure ID formats (e.g., "EMP123456")
- Validate postcodes, ZIP codes

**Configuration**:
```yaml
# Email validation
- type: "RegexCheck"
  severity: "ERROR"
  params:
    field: "email"
    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    description: "Valid email address format"

# UK postcode
- type: "RegexCheck"
  severity: "ERROR"
  params:
    field: "postcode"
    pattern: "^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$"
    description: "UK postcode format"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field name to validate |
| `pattern` | string | Yes | Regex pattern to match |
| `description` | string | No | Human-readable description |

**Common Patterns**:
- **Email**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$`
- **UK Phone**: `^\\+44[0-9]{10}$`
- **US Phone**: `^\\+1[0-9]{10}$`
- **US ZIP**: `^[0-9]{5}(-[0-9]{4})?$`
- **Date (YYYY-MM-DD)**: `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`

**Example Output**:
- **Pass**: "All 5,000 email values match pattern"
- **Fail**: "Found 15 invalid email formats"

**Sample Failures**:
```
Row #234: 'john.smith@' does not match email pattern
Row #567: 'invalid.email' does not match email pattern
```

---

### 8. ValidValuesCheck

**Purpose**: Ensures field values are from an allowed list.

**Use Cases**:
- Validate status codes
- Check country codes
- Ensure categorical values are valid
- Validate product codes

**Configuration**:
```yaml
- type: "ValidValuesCheck"
  severity: "ERROR"
  params:
    field: "status"
    valid_values:
      - "ACTIVE"
      - "INACTIVE"
      - "PENDING"
      - "SUSPENDED"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field name to validate |
| `valid_values` | list | Yes | List of allowed values |

**Example Output**:
- **Pass**: "All 5,000 'status' values are valid"
- **Fail**: "Found 8 invalid status values"

**Sample Failures**:
```
Row #123: 'ARCHIVED' is not in allowed values [ACTIVE, INACTIVE, PENDING, SUSPENDED]
Row #456: 'DELETED' is not in allowed values [ACTIVE, INACTIVE, PENDING, SUSPENDED]
```

---

### 9. RangeCheck

**Purpose**: Validates numeric field values are within specified range.

**Use Cases**:
- Check age is reasonable
- Validate amounts are positive
- Ensure percentages are 0-100
- Check quantity limits

**Configuration**:
```yaml
# Age range
- type: "RangeCheck"
  severity: "WARNING"
  params:
    field: "age"
    min_value: 18
    max_value: 120

# Percentage range
- type: "RangeCheck"
  severity: "ERROR"
  params:
    field: "discount_percent"
    min_value: 0
    max_value: 100
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field name to validate |
| `min_value` | number | No | Minimum allowed value (inclusive) |
| `max_value` | number | No | Maximum allowed value (inclusive) |

**Example Output**:
- **Pass**: "All 5,000 'age' values within range (18-120)"
- **Fail**: "Found 12 'age' values outside range"

**Sample Failures**:
```
Row #234: age=150 exceeds maximum (120)
Row #567: age=5 below minimum (18)
```

---

### 10. DateFormatCheck

**Purpose**: Validates date/datetime fields match expected format.

**Use Cases**:
- Ensure consistent date formats
- Validate date parsing will succeed
- Check datetime formats for timestamps

**Configuration**:
```yaml
# ISO date format
- type: "DateFormatCheck"
  severity: "ERROR"
  params:
    field: "signup_date"
    date_format: "%Y-%m-%d"

# UK date format
- type: "DateFormatCheck"
  severity: "ERROR"
  params:
    field: "birth_date"
    date_format: "%d/%m/%Y"

# US datetime format
- type: "DateFormatCheck"
  severity: "ERROR"
  params:
    field: "created_at"
    date_format: "%m/%d/%Y %H:%M:%S"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field name to validate |
| `date_format` | string | Yes | Python strftime format string |

**Common Date Formats**:
- **YYYY-MM-DD**: `%Y-%m-%d` (e.g., 2024-12-25)
- **DD/MM/YYYY**: `%d/%m/%Y` (e.g., 25/12/2024)
- **MM/DD/YYYY**: `%m/%d/%Y` (e.g., 12/25/2024)
- **ISO DateTime**: `%Y-%m-%dT%H:%M:%S` (e.g., 2024-12-25T14:30:00)

**Format Codes**:
- `%Y` - Year (4 digits)
- `%m` - Month (01-12)
- `%d` - Day (01-31)
- `%H` - Hour (00-23)
- `%M` - Minute (00-59)
- `%S` - Second (00-59)

**Example Output**:
- **Pass**: "All 5,000 dates match format YYYY-MM-DD"
- **Fail**: "Found 7 dates with invalid format"

**Sample Failures**:
```
Row #234: '25/12/2024' does not match format %Y-%m-%d
Row #567: '2024-13-01' is not a valid date
```

---

## Record-Level Validations

These validations check properties across entire records.

### 11. DuplicateRowCheck

**Purpose**: Detects duplicate rows in the dataset.

**Use Cases**:
- Find duplicate customer records
- Detect duplicate transactions
- Identify data loading errors

**Configuration**:
```yaml
# Check all columns
- type: "DuplicateRowCheck"
  severity: "WARNING"

# Check specific columns only
- type: "DuplicateRowCheck"
  severity: "WARNING"
  params:
    columns:
      - "customer_id"
      - "email"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `columns` | list | No | Specific columns to check (default: all columns) |

**Example Output**:
- **Pass**: "No duplicate rows found (5,000 unique rows)"
- **Fail**: "Found 15 duplicate rows"

**Sample Failures**:
```
Row #234: Duplicate of row #123
Row #567: Duplicate of row #400
```

---

### 12. BlankRecordCheck

**Purpose**: Detects rows where all values are null/empty.

**Use Cases**:
- Find completely empty rows
- Detect data loading errors
- Clean up datasets

**Configuration**:
```yaml
- type: "BlankRecordCheck"
  severity: "WARNING"
```

**Parameters**: None

**Example Output**:
- **Pass**: "No blank records found"
- **Fail**: "Found 3 completely blank rows"

**Sample Failures**:
```
Row #234: All fields are blank/null
Row #567: All fields are blank/null
```

---

### 13. UniqueKeyCheck

**Purpose**: Ensures specified key field(s) contain unique values.

**Use Cases**:
- Validate primary key uniqueness
- Check unique constraints
- Ensure no duplicate IDs

**Configuration**:
```yaml
# Single column key
- type: "UniqueKeyCheck"
  severity: "ERROR"
  params:
    key_columns:
      - "customer_id"

# Composite key
- type: "UniqueKeyCheck"
  severity: "ERROR"
  params:
    key_columns:
      - "account_id"
      - "transaction_date"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key_columns` | list | Yes | Column(s) that should be unique |

**Example Output**:
- **Pass**: "All 5,000 'customer_id' values are unique"
- **Fail**: "Found 8 duplicate 'customer_id' values"

**Sample Failures**:
```
Row #234: Duplicate key 'CUST001' (also appears in row #123)
Row #567: Duplicate key 'CUST002' (also appears in row #400)
```

---

## BA-Friendly Custom Validations

These validations allow Business Analysts to define custom checks without writing Python code.

### 14. InlineRegexCheck

**Purpose**: Define custom regex patterns directly in YAML.

**Use Cases**:
- Validate custom ID formats
- Check organization-specific patterns
- Validate any text format

**Configuration**:
```yaml
# Employee ID format
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "employee_id"
    pattern: "^EMP[0-9]{6}$"
    description: "Employee ID must be EMP followed by 6 digits"

# Credit card format
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "credit_card"
    pattern: "^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$"
    description: "Credit card format: ####-####-####-####"

# Check that names DON'T contain numbers
- type: "InlineRegexCheck"
  severity: "WARNING"
  params:
    field: "customer_name"
    pattern: "[0-9]"
    description: "Customer names should not contain numbers"
    should_match: false
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field name to validate |
| `pattern` | string | Yes | Regex pattern |
| `description` | string | Yes | What you're checking |
| `should_match` | boolean | No | True if should match, False if should NOT match (default: true) |

**Example Output**:
- **Pass**: "All employee_id values match pattern EMP######"
- **Fail**: "Found 5 invalid employee_id formats"

---

### 15. InlineBusinessRuleCheck

**Purpose**: Define business rules using SQL-like expressions.

**Use Cases**:
- Validate business logic
- Check conditional rules
- Enforce business constraints

**Configuration**:
```yaml
# Age must be 18 or older
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "age >= 18"
    description: "Customers must be 18 or older"
    error_message: "Customer age is below minimum requirement of 18"

# Amount within range
- type: "InlineBusinessRuleCheck"
  severity: "WARNING"
  params:
    rule: "amount >= 0 & amount <= 1000000"
    description: "Amount must be positive and reasonable"
    error_message: "Amount is outside acceptable range"

# Date in past
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "transaction_date <= today"
    description: "Transaction date cannot be in future"
    error_message: "Transaction date is in the future"

# Conditional logic
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "(account_type == 'SAVINGS' & interest_rate > 0) | (account_type != 'SAVINGS')"
    description: "Savings accounts must have interest rate"
    error_message: "Savings account has zero interest rate"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `rule` | string | Yes | Business rule expression |
| `description` | string | Yes | What the rule checks |
| `error_message` | string | Yes | Message when rule fails |

**Supported Operators**:
| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `status == 'ACTIVE'` |
| `!=` | Not equal to | `type != 'CLOSED'` |
| `>` | Greater than | `amount > 100` |
| `<` | Less than | `age < 65` |
| `>=` | Greater or equal | `balance >= 0` |
| `<=` | Less or equal | `discount <= 50` |
| `&` | AND | `age >= 18 & age <= 65` |
| `|` | OR | `status == 'ACTIVE' | status == 'PENDING'` |

**Special Values**:
- `today` - Current date
- `now` - Current datetime

**Example Output**:
- **Pass**: "All 5,000 rows pass business rule"
- **Fail**: "Found 12 rows that violate business rule"

---

### 16. InlineLookupCheck

**Purpose**: Validate against allowed or blocked value lists defined in YAML.

**Use Cases**:
- Check against approved lists
- Block unwanted values
- Validate reference data

**Configuration**:
```yaml
# Allowed countries
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "country_code"
    check_type: "allow"
    reference_values:
      - "US"
      - "UK"
      - "CA"
      - "AU"
      - "DE"
      - "FR"
    description: "Only customers from supported countries"

# Blocked email domains
- type: "InlineLookupCheck"
  severity: "WARNING"
  params:
    field: "email_domain"
    check_type: "deny"
    reference_values:
      - "tempmail.com"
      - "throwaway.email"
      - "guerrillamail.com"
    description: "Temporary email providers not allowed"

# Valid product codes
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "product_code"
    check_type: "allow"
    reference_values:
      - "PROD-001"
      - "PROD-002"
      - "PROD-003"
    description: "Product must be in approved catalog"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field to check |
| `check_type` | string | Yes | "allow" (whitelist) or "deny" (blacklist) |
| `reference_values` | list | Yes | List of values to check against |
| `description` | string | Yes | What you're checking |

**Check Types**:
- **allow**: Values MUST be in the list (whitelist)
- **deny**: Values MUST NOT be in the list (blacklist)

**Example Output**:
- **Pass**: "All country_code values in approved list"
- **Fail**: "Found 5 invalid country_code values"

**Sample Failures**:
```
Row #234: 'XX' not in approved list [US, UK, CA, AU, DE, FR]
Row #567: 'YY' not in approved list [US, UK, CA, AU, DE, FR]
```

---

## Summary Table

| Validation Type | Category | Coding Required | Use Case |
|----------------|----------|-----------------|----------|
| EmptyFileCheck | File | No | Detect empty files |
| RowCountRangeCheck | File | No | Check row count |
| FileSizeCheck | File | No | Check file size |
| SchemaMatchCheck | Schema | No | Validate schema |
| ColumnPresenceCheck | Schema | No | Check columns exist |
| MandatoryFieldCheck | Field | No | Check not null |
| RegexCheck | Field | No | Pattern matching |
| ValidValuesCheck | Field | No | Value lists |
| RangeCheck | Field | No | Numeric ranges |
| DateFormatCheck | Field | No | Date formats |
| DuplicateRowCheck | Record | No | Find duplicates |
| BlankRecordCheck | Record | No | Find blank rows |
| UniqueKeyCheck | Record | No | Unique constraints |
| InlineRegexCheck | Custom | **No (BA-Friendly)** | Custom patterns |
| InlineBusinessRuleCheck | Custom | **No (BA-Friendly)** | Business rules |
| InlineLookupCheck | Custom | **No (BA-Friendly)** | Reference data |

---

## Need More Help?

- **BA Guide**: [BA_GUIDE.md](BA_GUIDE.md) - Non-technical guide for Business Analysts
- **Examples**: Check `examples/` directory for sample configurations
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details

---

**Happy Validating! 🎯**
