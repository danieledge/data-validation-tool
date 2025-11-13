# Custom Validations Without Coding

**Build powerful custom validation rules using configuration only - no Python required!**

This guide shows you how to create sophisticated custom validations using YAML configuration, conditional logic, and inline checks. Perfect for business users and analysts who want to implement custom rules without writing code.

---

## Table of Contents

1. [Overview: What You Can Do Without Code](#overview-what-you-can-do-without-code)
2. [Pattern 1: Conditional Validations](#pattern-1-conditional-validations)
3. [Pattern 2: Inline Business Rules](#pattern-2-inline-business-rules)
4. [Pattern 3: Complex Multi-Field Validations](#pattern-3-complex-multi-field-validations)
5. [Pattern 4: Custom Lookup Validations](#pattern-4-custom-lookup-validations)
6. [Pattern 5: Combining Multiple Checks](#pattern-5-combining-multiple-checks)
7. [Real-World Examples](#real-world-examples)

---

## Overview: What You Can Do Without Code

### Built-in Validations You Can Combine

You can create custom rules by combining:

- ✅ **35+ built-in validation types**
- ✅ **Conditional logic** (if-then-else)
- ✅ **Inline conditions** on any validation
- ✅ **Python expressions** in parameters
- ✅ **Cross-field comparisons**
- ✅ **Lookup tables/reference files**

### What You DON'T Need

- ❌ Writing Python code
- ❌ Creating custom validation classes
- ❌ Understanding the framework internals
- ❌ Development environment setup

---

## Pattern 1: Conditional Validations

### Basic If-Then-Else Logic

**Use Case**: Different rules for different data types

```yaml
validations:
  # Business accounts need company information
  - type: "ConditionalValidation"
    severity: "ERROR"
    params:
      condition: "account_type == 'BUSINESS'"
      then_validate:
        - type: "MandatoryFieldCheck"
          params:
            fields: ["company_name", "tax_id", "business_type"]
        - type: "RegexCheck"
          params:
            field: "tax_id"
            pattern: "^\\d{2}-\\d{7}$"
      else_validate:
        - type: "MandatoryFieldCheck"
          params:
            fields: ["first_name", "last_name", "date_of_birth"]
```

### Multiple Conditions

**Use Case**: Complex business logic with multiple branches

```yaml
validations:
  # Different validation rules by customer tier
  - type: "ConditionalValidation"
    severity: "ERROR"
    params:
      condition: "customer_tier == 'PLATINUM'"
      then_validate:
        - type: "RangeCheck"
          params:
            field: "credit_limit"
            min_value: 100000  # Platinum needs high limit
        - type: "MandatoryFieldCheck"
          params:
            fields: ["dedicated_account_manager"]
      else_validate:
        - type: "ConditionalValidation"
          params:
            condition: "customer_tier == 'GOLD'"
            then_validate:
              - type: "RangeCheck"
                params:
                  field: "credit_limit"
                  min_value: 50000
            else_validate:
              - type: "RangeCheck"
                params:
                  field: "credit_limit"
                  min_value: 5000
```

### Inline Conditions (Simpler Alternative)

**Use Case**: Apply any validation conditionally

```yaml
validations:
  # Only validate shipping address for physical products
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    condition: "product_type == 'PHYSICAL'"  # Inline condition
    params:
      fields: ["shipping_address", "shipping_city", "shipping_zip"]

  # Only check age for alcohol products
  - type: "RangeCheck"
    severity: "ERROR"
    condition: "product_category == 'ALCOHOL'"
    params:
      field: "customer_age"
      min_value: 21
```

---

## Pattern 2: Inline Business Rules

### Using Python Expressions

**Use Case**: Custom business logic in one line

```yaml
validations:
  # Discount can't exceed product price
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule_name: "discount_vs_price"
      expression: "discount_amount <= price"
      error_message: "Discount cannot exceed product price"

  # Order date must be before or equal to ship date
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule_name: "order_before_ship"
      expression: "pd.to_datetime(order_date) <= pd.to_datetime(ship_date)"
      error_message: "Order date must be before ship date"

  # Total must equal sum of line items (with tolerance)
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule_name: "total_matches_lines"
      expression: "abs(total_amount - (item1_price + item2_price + item3_price)) < 0.01"
      error_message: "Total does not match sum of line items"
```

### Complex Calculations

**Use Case**: Business rules with calculations

```yaml
validations:
  # Gross profit margin must be at least 20%
  - type: "InlineBusinessRuleCheck"
    severity: "WARNING"
    params:
      rule_name: "minimum_margin"
      expression: "((revenue - cost) / revenue) >= 0.20"
      error_message: "Gross profit margin below 20%"

  # Commission is correct (5% for sales < 10000, 7% for >= 10000)
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule_name: "commission_calculation"
      expression: |
        (sale_amount < 10000 and commission == sale_amount * 0.05) or
        (sale_amount >= 10000 and commission == sale_amount * 0.07)
      error_message: "Commission calculation is incorrect"

  # Age derived from birth date is correct
  - type: "InlineBusinessRuleCheck"
    severity: "WARNING"
    params:
      rule_name: "age_calculation"
      expression: |
        age == (pd.Timestamp.now().year - pd.to_datetime(birth_date).dt.year)
      error_message: "Age does not match birth date"
```

---

## Pattern 3: Complex Multi-Field Validations

### Cross-Field Comparisons

**Use Case**: Fields must relate correctly to each other

```yaml
validations:
  # End date must be after start date
  - type: "CrossFieldComparisonCheck"
    severity: "ERROR"
    params:
      field1: "end_date"
      field2: "start_date"
      comparison: ">"
      message: "End date must be after start date"

  # Maximum limit can't exceed approved limit
  - type: "CrossFieldComparisonCheck"
    severity: "ERROR"
    params:
      field1: "credit_limit"
      field2: "approved_limit"
      comparison: "<="

  # Quantity shipped can't exceed quantity ordered
  - type: "CrossFieldComparisonCheck"
    severity: "ERROR"
    params:
      field1: "quantity_shipped"
      field2: "quantity_ordered"
      comparison: "<="
```

### Mutually Exclusive Fields

**Use Case**: Only one field can have a value

```yaml
validations:
  # Either email or phone must be provided, not both
  - type: "MutuallyExclusiveFieldsCheck"
    severity: "ERROR"
    params:
      fields: ["primary_email", "primary_phone"]
      require_at_least_one: true
      allow_multiple: false

  # Payment method: only one can be selected
  - type: "MutuallyExclusiveFieldsCheck"
    severity: "ERROR"
    params:
      fields: ["credit_card", "paypal", "bank_transfer", "cash"]
      require_at_least_one: true
      allow_multiple: false
```

### Required Field Combinations

**Use Case**: If one field has a value, others are required

```yaml
validations:
  # If discount is applied, must have discount_code and approval_id
  - type: "RequiredFieldsCombinationCheck"
    severity: "ERROR"
    params:
      trigger_field: "discount_amount"
      required_fields: ["discount_code", "discount_approval_id"]
      trigger_condition: "> 0"

  # If international shipment, need customs info
  - type: "RequiredFieldsCombinationCheck"
    severity: "ERROR"
    params:
      trigger_field: "country"
      required_fields: ["customs_value", "hs_code", "customs_description"]
      trigger_condition: "!= 'USA'"
```

---

## Pattern 4: Custom Lookup Validations

### Validating Against Reference Data

**Use Case**: Check if values exist in lookup tables

```yaml
validations:
  # Product code must exist in product catalog
  - type: "InlineLookupCheck"
    severity: "ERROR"
    params:
      field: "product_code"
      lookup_file: "reference_data/product_catalog.csv"
      lookup_column: "product_code"
      error_message: "Invalid product code"

  # Store ID must be in active stores list
  - type: "InlineLookupCheck"
    severity: "ERROR"
    params:
      field: "store_id"
      lookup_file: "reference_data/active_stores.csv"
      lookup_column: "store_id"
      error_message: "Store ID not found in active stores"

  # Country code must be valid ISO code
  - type: "InlineLookupCheck"
    severity: "ERROR"
    params:
      field: "country_code"
      lookup_file: "reference_data/iso_country_codes.csv"
      lookup_column: "code"
```

### Multi-Column Lookups

**Use Case**: Validate combinations against reference data

```yaml
validations:
  # State-City combination must be valid
  - type: "InlineLookupCheck"
    severity: "WARNING"
    params:
      field: ["state", "city"]  # Composite lookup
      lookup_file: "reference_data/valid_state_city.csv"
      lookup_columns: ["state", "city"]
      error_message: "Invalid state-city combination"
```

---

## Pattern 5: Combining Multiple Checks

### Layered Validation Strategy

**Use Case**: Multiple validation rules for the same field

```yaml
validations:
  # Email validation (multiple layers)
  - type: "MandatoryFieldCheck"
    severity: "ERROR"
    params:
      fields: ["email"]

  - type: "RegexCheck"
    severity: "ERROR"
    params:
      field: "email"
      pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - type: "StringLengthCheck"
    severity: "ERROR"
    params:
      field: "email"
      max_length: 100

  - type: "InlineLookupCheck"
    severity: "WARNING"
    params:
      field: "email"
      lookup_file: "reference_data/disposable_email_domains.csv"
      lookup_column: "domain"
      error_message: "Disposable email domain detected"
      inverse_lookup: true  # Fail if found in list
```

### Composite Business Rule

**Use Case**: Complex rule requiring multiple validations

```yaml
validations:
  # Valid order requires:
  # 1. Customer exists
  - type: "ReferentialIntegrityCheck"
    severity: "ERROR"
    params:
      foreign_key: "customer_id"
      reference_file: "customers.csv"
      reference_key: "id"

  # 2. Order amount is reasonable
  - type: "RangeCheck"
    severity: "ERROR"
    params:
      field: "order_amount"
      min_value: 0.01
      max_value: 1000000

  # 3. Discount doesn't exceed order amount
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      expression: "discount_amount <= order_amount"
      error_message: "Discount exceeds order amount"

  # 4. Payment method matches order type
  - type: "ConditionalValidation"
    severity: "ERROR"
    params:
      condition: "order_type == 'SUBSCRIPTION'"
      then_validate:
        - type: "ValidValuesCheck"
          params:
            field: "payment_method"
            allowed_values: ["CREDIT_CARD", "BANK_TRANSFER"]

  # 5. Total matches line items
  - type: "CrossFileComparisonCheck"
    severity: "ERROR"
    params:
      aggregation: "sum"
      column: "line_item_amount"
      comparison: "=="
      reference_file: "order_lines.csv"
      reference_aggregation: "sum"
      reference_column: "amount"
      tolerance_pct: 0.1
```

---

## Real-World Examples

### Example 1: E-Commerce Order Validation

```yaml
validation_job:
  name: "Order Validation - No Code"

files:
  - name: "orders"
    path: "orders.csv"
    validations:
      # Basic structure
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          key_columns: ["order_id"]

      # Customer must exist
      - type: "ReferentialIntegrityCheck"
        severity: "ERROR"
        params:
          foreign_key: "customer_id"
          reference_file: "customers.csv"
          reference_key: "id"

      # Order date validations
      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "order_date"
          format: "%Y-%m-%d"

      - type: "FreshnessCheck"
        severity: "WARNING"
        params:
          date_field: "order_date"
          max_age_days: 90

      # Amount validations
      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "subtotal"
          min_value: 0.01

      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        params:
          rule_name: "total_calculation"
          expression: "abs(total - (subtotal + tax + shipping)) < 0.01"
          error_message: "Total does not match subtotal + tax + shipping"

      # Discount validations
      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        condition: "discount > 0"  # Only check when discount applied
        params:
          rule_name: "discount_limit"
          expression: "discount <= subtotal * 0.50"  # Max 50% discount
          error_message: "Discount exceeds 50% of subtotal"

      - type: "RequiredFieldsCombinationCheck"
        severity: "ERROR"
        params:
          trigger_field: "discount"
          trigger_condition: "> 0"
          required_fields: ["discount_code", "discount_reason"]

      # Shipping validations for physical products
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        condition: "product_type == 'PHYSICAL'"
        params:
          fields: ["shipping_address", "shipping_city", "shipping_zip"]

      # Payment validations
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "payment_method"
          allowed_values: ["CREDIT_CARD", "DEBIT_CARD", "PAYPAL", "BANK_TRANSFER"]

      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "payment_method in ['CREDIT_CARD', 'DEBIT_CARD']"
          then_validate:
            - type: "MandatoryFieldCheck"
              params:
                fields: ["card_last_4", "card_brand"]
```

### Example 2: Employee Data Validation

```yaml
validation_job:
  name: "Employee Data Validation"

files:
  - name: "employees"
    path: "employees.csv"
    validations:
      # Required fields
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["employee_id", "first_name", "last_name", "hire_date", "department"]

      # Employee ID format
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "employee_id"
          pattern: "^EMP\\d{6}$"
          error_message: "Employee ID must be format EMP######"

      # Email validation
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "email"
          pattern: "^[a-zA-Z0-9._%+-]+@company\\.com$"
          error_message: "Email must be company domain"

      # Department must be valid
      - type: "InlineLookupCheck"
        severity: "ERROR"
        params:
          field: "department"
          lookup_file: "reference_data/departments.csv"
          lookup_column: "department_code"

      # Salary validations by level
      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "level == 'JUNIOR'"
          then_validate:
            - type: "RangeCheck"
              params:
                field: "salary"
                min_value: 40000
                max_value: 60000

      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "level == 'SENIOR'"
          then_validate:
            - type: "RangeCheck"
              params:
                field: "salary"
                min_value: 80000
                max_value: 150000

      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "level == 'EXECUTIVE'"
          then_validate:
            - type: "RangeCheck"
              params:
                field: "salary"
                min_value: 150000

      # Manager must be a valid employee
      - type: "ReferentialIntegrityCheck"
        severity: "ERROR"
        condition: "manager_id is not None"
        params:
          foreign_key: "manager_id"
          reference_file: "employees.csv"  # Self-referential
          reference_key: "employee_id"
          allow_null: true

      # Hire date validations
      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "hire_date"
          format: "%Y-%m-%d"

      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        params:
          rule_name: "hire_date_not_future"
          expression: "pd.to_datetime(hire_date) <= pd.Timestamp.now()"
          error_message: "Hire date cannot be in the future"

      # Termination date must be after hire date
      - type: "CrossFieldComparisonCheck"
        severity: "ERROR"
        condition: "termination_date is not None"
        params:
          field1: "termination_date"
          field2: "hire_date"
          comparison: ">"

      # Benefits eligibility (must work at least 30 days)
      - type: "InlineBusinessRuleCheck"
        severity: "WARNING"
        condition: "benefits_enrolled == True"
        params:
          rule_name: "benefits_eligibility"
          expression: "(pd.Timestamp.now() - pd.to_datetime(hire_date)).days >= 30"
          error_message: "Employee enrolled in benefits before 30-day waiting period"
```

### Example 3: Financial Transaction Validation

```yaml
validation_job:
  name: "Transaction Validation"

files:
  - name: "transactions"
    path: "transactions.csv"
    validations:
      # Transaction ID must be unique
      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          key_columns: ["transaction_id"]

      # Account must exist
      - type: "ReferentialIntegrityCheck"
        severity: "ERROR"
        params:
          foreign_key: "account_id"
          reference_file: "accounts.csv"
          reference_key: "account_id"

      # Transaction type must be valid
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "transaction_type"
          allowed_values: ["DEBIT", "CREDIT", "TRANSFER", "FEE", "INTEREST"]

      # Amount must be positive
      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "amount"
          min_value: 0.01

      # DEBIT transactions must not exceed account balance
      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        condition: "transaction_type == 'DEBIT'"
        params:
          rule_name: "sufficient_funds"
          expression: "amount <= account_balance"
          error_message: "Insufficient funds for debit transaction"

      # TRANSFER transactions need both from and to accounts
      - type: "RequiredFieldsCombinationCheck"
        severity: "ERROR"
        params:
          trigger_field: "transaction_type"
          trigger_condition: "== 'TRANSFER'"
          required_fields: ["from_account", "to_account"]

      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        condition: "transaction_type == 'TRANSFER'"
        params:
          rule_name: "transfer_different_accounts"
          expression: "from_account != to_account"
          error_message: "Cannot transfer to the same account"

      # Transaction time validations
      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "transaction_timestamp"
          format: "%Y-%m-%d %H:%M:%S"

      - type: "FreshnessCheck"
        severity: "WARNING"
        params:
          date_field: "transaction_date"
          max_age_days: 1

      # Fee calculations
      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        condition: "transaction_type == 'FEE'"
        params:
          rule_name: "fee_calculation"
          expression: "fee_amount == amount"
          error_message: "Fee amount doesn't match transaction amount"

      # Interest calculations
      - type: "InlineBusinessRuleCheck"
        severity: "WARNING"
        condition: "transaction_type == 'INTEREST'"
        params:
          rule_name: "interest_reasonable"
          expression: "amount <= account_balance * 0.10"  # Max 10% interest at once
          error_message: "Interest amount seems unusually high"

      # Duplicate detection (same account, amount, time)
      - type: "DuplicateRowCheck"
        severity: "WARNING"
        params:
          columns: ["account_id", "amount", "transaction_timestamp"]
```

---

## Tips and Best Practices

### 1. Start Simple, Then Layer

Don't try to build complex rules immediately:

```yaml
# Start with basic checks
- type: "MandatoryFieldCheck"
  severity: "ERROR"
  params:
    fields: ["order_id", "amount"]

# Then add format validation
- type: "RangeCheck"
  severity: "ERROR"
  params:
    field: "amount"
    min_value: 0

# Finally add business logic
- type: "InlineBusinessRuleCheck"
  severity: "ERROR"
  params:
    expression: "amount <= credit_limit"
    error_message: "Amount exceeds credit limit"
```

### 2. Use Descriptive Error Messages

Help users understand what went wrong:

```yaml
# Bad - Generic message
- type: "RangeCheck"
  params:
    field: "age"
    min_value: 18

# Good - Specific message
- type: "RangeCheck"
  params:
    field: "age"
    min_value: 18
  error_message: "Customer must be 18 or older to open an account"
```

### 3. Test with Real Data

Always test your validations with actual data:

```bash
# Profile your data first
python3 -m validation_framework.cli profile data.csv --format html

# Then run validation
python3 -m validation_framework.cli validate config.yaml --html report.html
```

### 4. Use Inline Conditions for Readability

Inline conditions are often clearer than nested ConditionalValidation:

```yaml
# Harder to read
- type: "ConditionalValidation"
  params:
    condition: "country == 'USA'"
    then_validate:
      - type: "RegexCheck"
        params:
          field: "zip_code"
          pattern: "^\\d{5}$"

# Easier to read
- type: "RegexCheck"
  condition: "country == 'USA'"
  params:
    field: "zip_code"
    pattern: "^\\d{5}$"
```

### 5. Document Your Business Rules

Add comments to explain complex logic:

```yaml
validations:
  # Commission tiers:
  # - Sales < $10k: 5%
  # - Sales $10k-$50k: 7%
  # - Sales > $50k: 10%
  - type: "InlineBusinessRuleCheck"
    severity: "ERROR"
    params:
      rule_name: "commission_tiers"
      expression: |
        (sale_amount < 10000 and commission == sale_amount * 0.05) or
        (10000 <= sale_amount < 50000 and commission == sale_amount * 0.07) or
        (sale_amount >= 50000 and commission == sale_amount * 0.10)
      error_message: "Commission does not match tier structure"
```

---

## When You Need Custom Code

You should write custom Python validation code when:

1. **Complex algorithms** - Advanced statistical calculations, ML models
2. **External APIs** - Need to call web services for validation
3. **Performance critical** - Optimization needed for massive datasets
4. **Reusable library** - Building validations to share across many projects

See the [Developer Guide](DEVELOPER_GUIDE.md) for creating custom validation classes.

---

## Next Steps

- **[Best Practices](BEST_PRACTICES.md)** - ERROR vs WARNING, essential validations
- **[Examples & Recipes](EXAMPLES_AND_RECIPES.md)** - More real-world patterns
- **[Validation Catalog](VALIDATION_CATALOG.md)** - All available validation types
- **[Developer Guide](DEVELOPER_GUIDE.md)** - When you need custom code

---

**Questions or examples to add?** [Open an issue](https://github.com/danieledge/data-validation-tool/issues) or contribute to this guide!
