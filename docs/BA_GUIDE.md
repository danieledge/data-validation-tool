# Business Analyst Guide to Custom Validations

## No Coding Required!

This guide shows you how to define custom data validation rules without writing Python code. Everything is done in the YAML configuration file.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Custom Regex Patterns](#custom-regex-patterns)
3. [Business Rules](#business-rules)
4. [Reference Data Lookups](#reference-data-lookups)
5. [Common Examples](#common-examples)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Step 1: Open the Configuration File

Edit your YAML configuration file (e.g., `my_validation.yaml`)

### Step 2: Add Your Custom Validation

Copy one of the templates below and modify it for your needs

### Step 3: Run the Validation

```bash
python3 test_validation.py
```

### Step 4: Check the Report

Open the generated HTML report to see results

---

## Custom Regex Patterns

Use **InlineRegexCheck** to validate data formats without coding!

### Basic Template

```yaml
- type: "InlineRegexCheck"
  severity: "ERROR"  # or "WARNING"
  params:
    field: "field_name_here"
    pattern: "your_regex_pattern_here"
    description: "Human-readable description of what you're checking"
```

### Real-World Examples

#### Validate UK Postcodes

```yaml
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "postcode"
    pattern: "^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$"
    description: "UK postcode format (e.g., SW1A 1AA, M1 1AA)"
```

#### Validate Employee ID Format

```yaml
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "employee_id"
    pattern: "^EMP[0-9]{6}$"
    description: "Employee ID must be EMP followed by 6 digits"
```

**Example matches**: EMP123456, EMP999999
**Example fails**: EMP12345 (too short), emp123456 (lowercase), EMP-123456 (hyphen)

#### Validate Phone Numbers

```yaml
# UK Phone Numbers
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "phone"
    pattern: "^\\+44[0-9]{10}$"
    description: "UK phone must start with +44 and have 10 digits"

# US Phone Numbers
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "phone"
    pattern: "^\\+1[0-9]{10}$"
    description: "US phone must start with +1 and have 10 digits"
```

#### Check for Unwanted Characters

```yaml
# Names should NOT contain numbers
- type: "InlineRegexCheck"
  severity: "WARNING"
  params:
    field: "customer_name"
    pattern: "[0-9]"
    description: "Customer names should not contain numbers"
    should_match: false  # Important! We DON'T want matches
```

#### Validate Account Numbers

```yaml
# 8-digit account number
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "account_number"
    pattern: "^[0-9]{8}$"
    description: "Account number must be exactly 8 digits"

# Account number with prefix
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "account_number"
    pattern: "^ACC-[0-9]{6}$"
    description: "Account number must be ACC- followed by 6 digits"
```

### Common Regex Patterns (Copy & Paste!)

| What You Want to Check | Pattern | Example Match |
|------------------------|---------|---------------|
| Email address | `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` | user@example.com |
| UK Postcode | `^[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2}$` | SW1A 1AA |
| US ZIP Code | `^[0-9]{5}(-[0-9]{4})?$` | 12345 or 12345-6789 |
| Date (YYYY-MM-DD) | `^[0-9]{4}-[0-9]{2}-[0-9]{2}$` | 2024-12-25 |
| Date (DD/MM/YYYY) | `^[0-9]{2}/[0-9]{2}/[0-9]{4}$` | 25/12/2024 |
| Only numbers | `^[0-9]+$` | 12345 |
| Only letters | `^[a-zA-Z]+$` | ABC |
| No special chars | `^[a-zA-Z0-9 ]+$` | ABC 123 |
| Credit card | `^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$` | 1234-5678-9012-3456 |
| Currency (£) | `^£[0-9]{1,3}(,[0-9]{3})*\.[0-9]{2}$` | £1,234.56 |

---

## Business Rules

Use **InlineBusinessRuleCheck** to define business logic without coding!

### Basic Template

```yaml
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"  # or "WARNING"
  params:
    rule: "your_business_rule_here"
    description: "What you're checking"
    error_message: "Message when rule fails"
```

### Available Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `status == 'ACTIVE'` |
| `!=` | Not equal to | `type != 'CLOSED'` |
| `>` | Greater than | `amount > 100` |
| `<` | Less than | `age < 65` |
| `>=` | Greater than or equal | `balance >= 0` |
| `<=` | Less than or equal | `discount <= 50` |
| `&` | AND (both must be true) | `age >= 18 & age <= 65` |
| `|` | OR (one must be true) | `status == 'ACTIVE' | status == 'PENDING'` |

### Real-World Examples

#### Age Restrictions

```yaml
# Must be 18 or older
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "age >= 18"
    description: "Customers must be 18 years or older"
    error_message: "Customer age is below minimum requirement of 18"

# Must be between 18 and 65
- type: "InlineBusinessRuleCheck"
  severity: "WARNING"
  params:
    rule: "age >= 18 & age <= 65"
    description: "Customers should be between 18 and 65"
    error_message: "Customer age is outside typical range"
```

#### Amount Validations

```yaml
# Amount must be positive
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "amount > 0"
    description: "Transaction amount must be positive"
    error_message: "Amount is zero or negative"

# Amount within reasonable range
- type: "InlineBusinessRuleCheck"
  severity: "WARNING"
  params:
    rule: "amount >= 1 & amount <= 1000000"
    description: "Amount should be between £1 and £1,000,000"
    error_message: "Amount is outside normal range"
```

#### Date Validations

```yaml
# End date must be after start date
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "end_date > start_date"
    description: "End date must be after start date"
    error_message: "End date is before start date"

# Date cannot be in future
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "transaction_date <= today"
    description: "Transaction date cannot be in the future"
    error_message: "Transaction date is in the future"
```

#### Conditional Logic

```yaml
# VIP customers must have high balance
- type: "InlineBusinessRuleCheck"
  severity: "WARNING"
  params:
    rule: "(customer_type == 'VIP' & balance >= 10000) | (customer_type != 'VIP')"
    description: "VIP customers should have balance of at least £10,000"
    error_message: "VIP customer has balance below £10,000"

# Savings accounts must have interest rate
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "(account_type == 'SAVINGS' & interest_rate > 0) | (account_type != 'SAVINGS')"
    description: "Savings accounts must have an interest rate"
    error_message: "Savings account has zero interest rate"
```

---

## Reference Data Lookups

Use **InlineLookupCheck** to validate against allowed/blocked lists!

### Basic Template

```yaml
- type: "InlineLookupCheck"
  severity: "ERROR"  # or "WARNING"
  params:
    field: "field_name"
    check_type: "allow"  # or "deny"
    reference_values:
      - "value1"
      - "value2"
      - "value3"
    description: "What you're checking"
```

### Check Type: Allow vs Deny

- **allow**: Values MUST be in the list (whitelist)
- **deny**: Values MUST NOT be in the list (blacklist)

### Real-World Examples

#### Approved Countries Only

```yaml
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
      - "ES"
      - "IT"
    description: "Only customers from approved countries"
```

#### Block Temporary Email Providers

```yaml
- type: "InlineLookupCheck"
  severity: "WARNING"
  params:
    field: "email_domain"
    check_type: "deny"
    reference_values:
      - "tempmail.com"
      - "throwaway.email"
      - "guerrillamail.com"
      - "10minutemail.com"
    description: "Temporary email providers not allowed"
```

#### Valid Product Codes

```yaml
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "product_code"
    check_type: "allow"
    reference_values:
      - "PROD-001"
      - "PROD-002"
      - "PROD-003"
      - "PROD-004"
      - "PROD-005"
    description: "Product must be in approved catalog"
```

#### Valid Status Values

```yaml
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "order_status"
    check_type: "allow"
    reference_values:
      - "PENDING"
      - "PROCESSING"
      - "SHIPPED"
      - "DELIVERED"
      - "CANCELLED"
    description: "Order status must be valid"
```

---

## Common Examples

### Financial Data

```yaml
# Account balance checks
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "balance >= 0"
    description: "Account balance cannot be negative"
    error_message: "Negative balance detected"

# Transaction amount limits
- type: "InlineBusinessRuleCheck"
  severity: "WARNING"
  params:
    rule: "transaction_amount >= 0 & transaction_amount <= 50000"
    description: "Transaction amount should be reasonable"
    error_message: "Transaction amount is outside normal range"

# Sort code format (UK)
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "sort_code"
    pattern: "^[0-9]{2}-[0-9]{2}-[0-9]{2}$"
    description: "UK sort code format (##-##-##)"
```

### Customer Data

```yaml
# Email format
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "email"
    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    description: "Valid email address format"

# Age restrictions
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "age >= 18"
    description: "Customer must be 18 or older"
    error_message: "Customer is under 18"

# Valid customer types
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "customer_type"
    check_type: "allow"
    reference_values:
      - "INDIVIDUAL"
      - "BUSINESS"
      - "VIP"
      - "PARTNER"
    description: "Customer type must be valid"
```

### Product Data

```yaml
# SKU format
- type: "InlineRegexCheck"
  severity: "ERROR"
  params:
    field: "sku"
    pattern: "^[A-Z]{3}-[0-9]{5}$"
    description: "SKU must be 3 letters, dash, 5 numbers"

# Price must be positive
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    rule: "price > 0"
    description: "Product price must be positive"
    error_message: "Price is zero or negative"

# Valid categories
- type: "InlineLookupCheck"
  severity: "ERROR"
  params:
    field: "category"
    check_type: "allow"
    reference_values:
      - "ELECTRONICS"
      - "CLOTHING"
      - "FOOD"
      - "BOOKS"
      - "TOYS"
    description: "Product category must be valid"
```

---

## Troubleshooting

### My Regex Pattern Isn't Working

**Problem**: Pattern doesn't match expected values

**Solutions**:
1. Test your pattern online: https://regex101.com/
2. Remember to escape special characters with `\\` (e.g., `\\.` for a period)
3. Use `^` at start and `$` at end to match whole string
4. Check if `should_match: false` is needed

### My Business Rule Fails for All Rows

**Problem**: All rows fail the rule

**Solutions**:
1. Check field names match exactly (case-sensitive!)
2. Verify data types (numbers vs strings)
3. Use `&` for AND, `|` for OR (not "AND" or "OR")
4. Test with simpler rules first

### Reference Lookup Doesn't Find Matches

**Problem**: Valid values are being rejected

**Solutions**:
1. Check for exact matches (case-sensitive!)
2. Check for extra spaces in data
3. Verify you're using `check_type: "allow"` not `"deny"`
4. Make sure field name is correct

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| `AND` instead of `&` | Use `&` for AND logic |
| `OR` instead of `|` | Use `|` for OR logic |
| Forgot `\\` before `.` | Escape: `\\.` |
| Wrong `check_type` | Use "allow" or "deny" |
| Typo in field name | Check spelling exactly |

---

## Need Help?

1. Check the `examples/ba_friendly_config.yaml` file for more examples
2. Look at the generated HTML report for detailed error messages
3. Start with simple validations and build up complexity
4. Test on a small sample of data first

---

**Remember**: You don't need to be a programmer! These validations are designed for Business Analysts to define and maintain.

Happy Validating! 🎯
