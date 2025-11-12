# Validation Reference Guide

Complete reference for all 22 built-in validation types in the Data Validation Tool.

---

## Table of Contents

1. [File-Level Validations](#file-level-validations)
2. [Schema Validations](#schema-validations)
3. [Field-Level Validations](#field-level-validations)
4. [Record-Level Validations](#record-level-validations)
5. [Bespoke Validation Checks](#bespoke-validation-checks)
6. [Advanced Validation Checks](#advanced-validation-checks)

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

## Bespoke Validation Checks

These validations allow users to define custom checks without writing Python code.

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

## Advanced Validation Checks

These validations were added based on research into leading data quality frameworks like Great Expectations.

### 17. StatisticalOutlierCheck

**Purpose**: Detects statistical outliers using Z-score or IQR methods.

**Use Cases**:
- Detect fraudulent transactions
- Identify sensor errors
- Find data quality issues
- Validate measurement accuracy

**Configuration**:
```yaml
# Z-Score method
- type: "StatisticalOutlierCheck"
  severity: "WARNING"
  params:
    field: "transaction_amount"
    method: "zscore"
    threshold: 3.0  # >3 standard deviations

# IQR method
- type: "StatisticalOutlierCheck"
  severity: "WARNING"
  params:
    field: "temperature"
    method: "iqr"
    threshold: 1.5  # 1.5 * IQR from quartiles
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Numeric field to check |
| `method` | string | No | 'zscore' or 'iqr' (default: 'zscore') |
| `threshold` | float | No | Threshold value (default: 3.0 for zscore, 1.5 for iqr) |

**Methods**:
- **zscore**: Flags values beyond N standard deviations from mean
- **iqr**: Uses Interquartile Range (Q3-Q1) to detect outliers

**Example Output**:
- **Pass**: "No outliers detected in 5,000 values (zscore method)"
- **Fail**: "Found 12 outliers using zscore method. Mean: 100.5, StdDev: 15.2"

---

### 18. CrossFieldComparisonCheck

**Purpose**: Validates logical relationships between two fields.

**Use Cases**:
- Verify end_date > start_date
- Ensure discount <= price
- Check actual <= budget
- Validate min <= max

**Configuration**:
```yaml
# Date comparison
- type: "CrossFieldComparisonCheck"
  severity: "ERROR"
  params:
    field_a: "end_date"
    operator: ">"
    field_b: "start_date"

# Numeric comparison
- type: "CrossFieldComparisonCheck"
  severity: "ERROR"
  params:
    field_a: "discount_amount"
    operator: "<="
    field_b: "product_price"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field_a` | string | Yes | First field name |
| `operator` | string | Yes | Comparison: >, <, >=, <=, ==, != |
| `field_b` | string | Yes | Second field name |

**Example Output**:
- **Pass**: "All 5,000 rows pass: end_date > start_date"
- **Fail**: "Found 15 rows where discount_amount not <= product_price"

---

### 19. FreshnessCheck

**Purpose**: Validates file or data is fresh (recently updated).

**Use Cases**:
- Ensure daily data loads completed
- Verify SLA compliance
- Check data currency
- Monitor pipeline health

**Configuration**:
```yaml
# File age check
- type: "FreshnessCheck"
  severity: "WARNING"
  params:
    check_type: "file"
    max_age_hours: 24  # File modified within 24 hours

# Data age check (future enhancement)
- type: "FreshnessCheck"
  severity: "ERROR"
  params:
    check_type: "data"
    max_age_hours: 48
    date_field: "transaction_timestamp"
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `check_type` | string | No | 'file' or 'data' (default: 'file') |
| `max_age_hours` | int | Yes | Maximum age in hours |
| `date_field` | string | Conditional | Required if check_type='data' |

**Example Output**:
- **Pass**: "File is fresh (2.5 hours old, max: 24)"
- **Fail**: "File is 36.2 hours old (max: 24)"

---

### 20. CompletenessCheck

**Purpose**: Validates field completeness (percentage of non-null values).

**Use Cases**:
- Ensure critical fields are populated
- Measure data quality
- Monitor data collection
- SLA compliance

**Configuration**:
```yaml
# 95% completeness required
- type: "CompletenessCheck"
  severity: "WARNING"
  params:
    field: "email"
    min_completeness: 0.95  # 95%

# 100% completeness required
- type: "CompletenessCheck"
  severity: "ERROR"
  params:
    field: "customer_id"
    min_completeness: 1.0  # 100%
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Field to check |
| `min_completeness` | float | Yes | Min completeness (0.0-1.0 or 0-100) |

**Example Output**:
- **Pass**: "Completeness 98.5% meets minimum 95%"
- **Fail**: "Completeness 92.3% is below minimum 95%. Missing 38 of 500 values"

---

### 21. StringLengthCheck

**Purpose**: Validates string field length is within acceptable range.

**Use Cases**:
- Prevent database truncation
- Validate ID formats
- Check description quality
- Ensure proper data entry

**Configuration**:
```yaml
# Min and max length
- type: "StringLengthCheck"
  severity: "ERROR"
  params:
    field: "product_code"
    min_length: 5
    max_length: 20

# Minimum only
- type: "StringLengthCheck"
  severity: "WARNING"
  params:
    field: "description"
    min_length: 10  # At least 10 characters
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | String field to check |
| `min_length` | int | No | Minimum length |
| `max_length` | int | No | Maximum length |

**Note**: At least one of min_length or max_length is required.

**Example Output**:
- **Pass**: "All 5,000 values have valid length"
- **Fail**: "Found 25 values with invalid length"

**Sample Failures**:
```
Row #234: Length 3 < minimum 5
Row #567: Length 25 > maximum 20
```

---

### 22. NumericPrecisionCheck

**Purpose**: Validates numeric precision (decimal places).

**Use Cases**:
- Validate currency fields (2 decimals)
- Check measurement precision
- Ensure database compatibility
- Prevent rounding errors

**Configuration**:
```yaml
# Exact precision (currency)
- type: "NumericPrecisionCheck"
  severity: "ERROR"
  params:
    field: "price"
    exact_decimal_places: 2

# Maximum precision
- type: "NumericPrecisionCheck"
  severity: "WARNING"
  params:
    field: "measurement"
    max_decimal_places: 4
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `field` | string | Yes | Numeric field to check |
| `max_decimal_places` | int | No | Maximum allowed decimals |
| `exact_decimal_places` | int | No | Required exact decimals |

**Note**: Either max_decimal_places or exact_decimal_places is required.

**Example Output**:
- **Pass**: "All 5,000 values have valid precision"
- **Fail**: "Found 40 values with invalid precision"

**Sample Failures**:
```
Row #234: Has 4 decimals, requires exactly 2
Row #567: Has 5 decimals, maximum is 4
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
| InlineRegexCheck | Bespoke | **No** | Custom patterns |
| InlineBusinessRuleCheck | Bespoke | **No** | Business rules |
| InlineLookupCheck | Bespoke | **No** | Reference data |
| **StatisticalOutlierCheck** | **Advanced** | **No** | **Detect outliers** |
| **CrossFieldComparisonCheck** | **Advanced** | **No** | **Field relationships** |
| **FreshnessCheck** | **Advanced** | **No** | **Data currency** |
| **CompletenessCheck** | **Advanced** | **No** | **Missing values** |
| **StringLengthCheck** | **Advanced** | **No** | **String length** |
| **NumericPrecisionCheck** | **Advanced** | **No** | **Decimal precision** |

---

## Need More Help?

- **BA Guide**: [BA_GUIDE.md](BA_GUIDE.md) - Guide for defining custom validations without coding
- **Examples**: Check `examples/` directory for sample configurations
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details

---

**Happy Validating! 🎯**
