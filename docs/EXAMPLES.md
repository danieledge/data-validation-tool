# Examples & Recipes

**Real-world validation scenarios and complete configurations**

This guide provides production-ready examples for common data validation scenarios. Each example includes complete configuration files and explanations.

---

## Table of Contents

1. [E-Commerce Data Validation](#e-commerce-data-validation)
2. [Financial Transactions](#financial-transactions)
3. [Customer Master Data](#customer-master-data)
4. [Healthcare Records](#healthcare-records)
5. [API Response Validation](#api-response-validation)
6. [Multi-File ETL Pipeline](#multi-file-etl-pipeline)
7. [AutoSys Job Integration](#autosys-job-integration)
8. [Data Warehouse Loading](#data-warehouse-loading)
9. [Real-Time Data Feeds](#real-time-data-feeds)
10. [Regulatory Compliance](#regulatory-compliance)

---

## E-Commerce Data Validation

**Scenario:** Validate daily order exports before loading into analytics database.

**Data:** Orders with customer info, products, pricing, shipping

**Business Rules:**
- All orders must have order ID, customer ID, and total
- Email addresses must be valid
- Order total must equal line items
- Shipping date >= order date
- Payment method determines required payment fields

**Configuration:**

```yaml
validation_job:
  name: "E-Commerce Order Validation"
  description: "Daily order data validation before analytics load"

settings:
  chunk_size: 5000
  max_sample_failures: 100

files:
  - name: "daily_orders"
    path: "/data/exports/orders_{YYYYMMDD}.csv"
    format: "csv"

    validations:
      # File-level checks
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "RowCountRangeCheck"
        severity: "WARNING"
        params:
          min_rows: 100      # Expect at least 100 orders per day
          max_rows: 100000   # Alert if unusually high

      # Required fields
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "order_id"
            - "customer_id"
            - "order_date"
            - "order_total"
            - "status"

      # Email validation
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "customer_email"
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
          message: "Invalid email format"

      # Status validation
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "status"
          valid_values:
            - "PENDING"
            - "PROCESSING"
            - "SHIPPED"
            - "DELIVERED"
            - "CANCELLED"
            - "REFUNDED"

      # Order total must be positive
      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "order_total"
          min_value: 0

      # Shipping date validation
      - type: "CrossFieldComparisonCheck"
        severity: "ERROR"
        params:
          field1: "order_date"
          field2: "shipping_date"
          operator: "<="
        description: "Shipping date must be after order date"

      # Payment method conditional validation
      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "payment_method == 'CREDIT_CARD'"
          then_validate:
            - type: "MandatoryFieldCheck"
              params:
                fields: ["card_last4", "card_type"]
            - type: "ValidValuesCheck"
              params:
                field: "card_type"
                valid_values: ["VISA", "MASTERCARD", "AMEX", "DISCOVER"]

      # Detect duplicate orders
      - type: "DuplicateRowCheck"
        severity: "ERROR"
        params:
          key_fields: ["order_id"]

      # Data quality checks
      - type: "CompletenessCheck"
        severity: "WARNING"
        params:
          field: "customer_phone"
          min_completeness: 80.0

      # Outlier detection for fraud
      - type: "StatisticalOutlierCheck"
        severity: "WARNING"
        params:
          field: "order_total"
          method: "zscore"
          threshold: 3.0
```

**Usage:**
```bash
# Daily validation
python3 -m validation_framework.cli validate ecommerce_orders.yaml \
  --html /reports/orders_$(date +%Y%m%d).html \
  --json /reports/orders_$(date +%Y%m%d).json

# Check exit code
if [ $? -ne 0 ]; then
  echo "Order validation failed - blocking load"
  exit 1
fi

# Proceed with load
./load_to_analytics.sh
```

---

## Financial Transactions

**Scenario:** Validate banking transactions for compliance and fraud detection.

**Business Rules:**
- All transactions need ID, account, amount, date
- Transaction amounts within limits
- Balance calculations correct
- Specific requirements for different transaction types
- High-value transactions need approval

**Configuration:**

```yaml
validation_job:
  name: "Banking Transaction Validation"
  description: "Transaction data validation for compliance and fraud detection"

settings:
  chunk_size: 10000
  max_sample_failures: 50

files:
  - name: "transactions"
    path: "/data/banking/transactions.csv"
    format: "csv"

    validations:
      # Critical fields
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "transaction_id"
            - "account_number"
            - "transaction_date"
            - "transaction_type"
            - "amount"
            - "currency"

      # Unique transaction IDs
      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["transaction_id"]

      # Transaction type validation
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "transaction_type"
          valid_values:
            - "DEPOSIT"
            - "WITHDRAWAL"
            - "TRANSFER"
            - "PAYMENT"
            - "FEE"
            - "INTEREST"

      # Currency codes
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "currency"
          valid_values: ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]

      # Amount validation
      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "amount"
          min_value: 0.01
          max_value: 1000000
        description: "Transaction amount limits"

      # High-value transaction approval
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["approved_by", "approval_timestamp"]
        condition: "amount > 50000"
        description: "High-value transactions require approval"

      # Withdrawal-specific validation
      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "transaction_type == 'WITHDRAWAL'"
          then_validate:
            - type: "MandatoryFieldCheck"
              params:
                fields: ["withdrawal_method", "atm_id"]
            - type: "RangeCheck"
              params:
                field: "amount"
                max_value: 10000
              description: "Withdrawal limits"

      # Transfer validation
      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "transaction_type == 'TRANSFER'"
          then_validate:
            - type: "MandatoryFieldCheck"
              params:
                fields: ["destination_account", "destination_routing"]

      # Account number format
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "account_number"
          pattern: "^[0-9]{10,12}$"
          message: "Invalid account number format"

      # Date format
      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "transaction_date"
          format: "%Y-%m-%d %H:%M:%S"
          allow_null: false

      # Fraud detection - statistical outliers
      - type: "StatisticalOutlierCheck"
        severity: "WARNING"
        params:
          field: "amount"
          method: "zscore"
          threshold: 4.0
        description: "Flag potential fraudulent transactions"

      # Balance check
      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        params:
          rule: "balance_after >= 0"
          description: "Balance cannot be negative after transaction"
          error_message: "Overdraft detected"
        condition: "account_type != 'OVERDRAFT_PROTECTION'"
```

---

## Customer Master Data

**Scenario:** Validate customer records before CRM system load.

**Business Rules:**
- Different requirements for business vs individual customers
- Email and phone validation
- Address completeness
- No duplicate customers

**Configuration:**

```yaml
validation_job:
  name: "Customer Master Data Validation"
  description: "CRM data validation - business and individual customers"

settings:
  chunk_size: 2000
  max_sample_failures: 100

files:
  - name: "customers"
    path: "/data/crm/customers.csv"
    format: "csv"

    validations:
      # Universal required fields
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "customer_id"
            - "customer_type"
            - "email"
            - "created_date"
            - "status"

      # No duplicate customer IDs
      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["customer_id"]

      # No duplicate emails
      - type: "DuplicateRowCheck"
        severity: "WARNING"
        params:
          key_fields: ["email"]
        description: "Warn on duplicate emails (might be legitimate)"

      # Customer type validation
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "customer_type"
          valid_values: ["INDIVIDUAL", "BUSINESS", "ENTERPRISE"]

      # Status validation
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "status"
          valid_values: ["ACTIVE", "INACTIVE", "SUSPENDED", "CLOSED"]

      # Email validation
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "email"
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

      # Phone validation (if present)
      - type: "RegexCheck"
        severity: "WARNING"
        params:
          field: "phone"
          pattern: "^\\+?[0-9]{10,15}$"
        description: "Phone format: 10-15 digits, optional +"

      # Individual customer validation
      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "customer_type == 'INDIVIDUAL'"
          then_validate:
            - type: "MandatoryFieldCheck"
              params:
                fields:
                  - "first_name"
                  - "last_name"
                  - "date_of_birth"

            - type: "DateFormatCheck"
              params:
                field: "date_of_birth"
                format: "%Y-%m-%d"

            - type: "RangeCheck"
              params:
                field: "age"
                min_value: 18
                max_value: 120
              description: "Age validation for individuals"

      # Business customer validation
      - type: "ConditionalValidation"
        severity: "ERROR"
        params:
          condition: "customer_type == 'BUSINESS' OR customer_type == 'ENTERPRISE'"
          then_validate:
            - type: "MandatoryFieldCheck"
              params:
                fields:
                  - "company_name"
                  - "tax_id"
                  - "industry"
                  - "employee_count"

            - type: "RegexCheck"
              params:
                field: "tax_id"
                pattern: "^[0-9]{2}-[0-9]{7}$"
                message: "Tax ID format: XX-XXXXXXX"

            - type: "RangeCheck"
              params:
                field: "employee_count"
                min_value: 1

      # Enterprise-specific validation
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["account_manager", "contract_value"]
        condition: "customer_type == 'ENTERPRISE'"

      # Address completeness (warning only)
      - type: "CompletenessCheck"
        severity: "WARNING"
        params:
          field: "address_line1"
          min_completeness: 90.0

      - type: "CompletenessCheck"
        severity: "WARNING"
        params:
          field: "city"
          min_completeness: 90.0

      # Data freshness
      - type: "FreshnessCheck"
        severity: "WARNING"
        params:
          check_type: "field_value"
          field: "last_updated"
          max_age_hours: 168  # 7 days
        description: "Customer records should be updated weekly"
```

---

## AutoSys Job Integration

**Scenario:** Integrate validation into AutoSys job scheduling to fail jobs on critical data issues.

**AutoSys JIL Configuration:**

```bash
# Data Validation Job
insert_job: VALIDATE_CUSTOMER_DATA
job_type: c
command: /apps/validation/scripts/validate_customer_data.sh
machine: prod-etl-01
owner: etluser
permission: gx,ge,wx,we
date_conditions: yes
days_of_week: mo,tu,we,th,fr
start_times: "02:00"
description: "Validate customer data - block load if critical errors"
alarm_if_fail: yes
max_run_alarm: 30
std_out_file: /logs/autosys/validate_customer_$AUTO_JOB_NAME.out
std_err_file: /logs/autosys/validate_customer_$AUTO_JOB_NAME.err

# Data Load Job (depends on validation success)
insert_job: LOAD_CUSTOMER_DATA
job_type: c
command: /apps/etl/scripts/load_customer_data.sh
machine: prod-etl-01
owner: etluser
permission: gx,ge,wx,we
condition: success(VALIDATE_CUSTOMER_DATA)
description: "Load customer data to warehouse (runs only if validation passes)"
alarm_if_fail: yes
std_out_file: /logs/autosys/load_customer_$AUTO_JOB_NAME.out
std_err_file: /logs/autosys/load_customer_$AUTO_JOB_NAME.err
```

**Validation Script (`validate_customer_data.sh`):**

```bash
#!/bin/bash
#
# AutoSys Data Validation Script
# Purpose: Validate customer data and fail job on critical errors
# Exit Codes:
#   0 = Validation passed
#   1 = Validation failed (critical errors)
#   2 = Script error

set -euo pipefail

# Configuration
CONFIG_FILE="/apps/validation/configs/customer_validation.yaml"
DATA_FILE="/data/staging/customer_data_$(date +%Y%m%d).csv"
REPORT_DIR="/reports/validation"
LOG_FILE="/logs/validation/customer_$(date +%Y%m%d_%H%M%S).log"

# Create directories if needed
mkdir -p "$REPORT_DIR" "$(dirname "$LOG_FILE")"

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Function to send alert
send_alert() {
    local subject="$1"
    local message="$2"

    echo "$message" | mail -s "$subject" data-team@company.com
}

# Main execution
main() {
    log "Starting customer data validation"
    log "Data file: $DATA_FILE"
    log "Config: $CONFIG_FILE"

    # Check if data file exists
    if [ ! -f "$DATA_FILE" ]; then
        log "ERROR: Data file not found: $DATA_FILE"
        send_alert "AutoSys Validation Failed - File Missing" \
            "Data file not found: $DATA_FILE\nJob: $AUTO_JOB_NAME\nServer: $(hostname)"
        exit 2
    fi

    # Check file is not empty
    if [ ! -s "$DATA_FILE" ]; then
        log "ERROR: Data file is empty: $DATA_FILE"
        send_alert "AutoSys Validation Failed - Empty File" \
            "Data file is empty: $DATA_FILE\nJob: $AUTO_JOB_NAME\nServer: $(hostname)"
        exit 1
    fi

    log "Data file exists and is not empty"

    # Run validation
    log "Executing validation framework..."

    REPORT_HTML="$REPORT_DIR/customer_$(date +%Y%m%d).html"
    REPORT_JSON="$REPORT_DIR/customer_$(date +%Y%m%d).json"

    python3 -m validation_framework.cli validate "$CONFIG_FILE" \
        --html "$REPORT_HTML" \
        --json "$REPORT_JSON" \
        2>&1 | tee -a "$LOG_FILE"

    EXIT_CODE=$?

    # Parse results from JSON
    if [ -f "$REPORT_JSON" ]; then
        ERROR_COUNT=$(python3 -c "import json; print(json.load(open('$REPORT_JSON'))['total_errors'])")
        WARNING_COUNT=$(python3 -c "import json; print(json.load(open('$REPORT_JSON'))['total_warnings'])")
        STATUS=$(python3 -c "import json; print(json.load(open('$REPORT_JSON'))['overall_status'])")

        log "Validation complete: Status=$STATUS, Errors=$ERROR_COUNT, Warnings=$WARNING_COUNT"
    else
        log "ERROR: Validation report not generated"
        send_alert "AutoSys Validation Failed - No Report" \
            "Validation did not generate report\nJob: $AUTO_JOB_NAME\nCheck logs: $LOG_FILE"
        exit 2
    fi

    # Handle results
    if [ $EXIT_CODE -eq 0 ]; then
        log "SUCCESS: Validation passed with $WARNING_COUNT warnings"

        # Send summary email if warnings exist
        if [ "$WARNING_COUNT" -gt 0 ]; then
            send_alert "AutoSys Validation Passed with Warnings" \
                "Customer data validation passed but has $WARNING_COUNT warnings.\nReview report: $REPORT_HTML\nJob: $AUTO_JOB_NAME"
        fi

        # Create success marker file for downstream jobs
        touch /tmp/customer_validation_success_$(date +%Y%m%d)

        exit 0

    elif [ $EXIT_CODE -eq 1 ]; then
        log "FAILED: Validation failed with $ERROR_COUNT errors"

        # Send failure alert with details
        send_alert "AutoSys Validation FAILED - BLOCKING LOAD" \
            "Customer data validation FAILED with $ERROR_COUNT critical errors.\n\nData load has been BLOCKED.\n\nReview report: $REPORT_HTML\nJSON results: $REPORT_JSON\nLog file: $LOG_FILE\n\nJob: $AUTO_JOB_NAME\nServer: $(hostname)\nData file: $DATA_FILE"

        # Create failure marker
        touch /tmp/customer_validation_failed_$(date +%Y%m%d)

        # Exit with failure code to fail AutoSys job
        exit 1

    else
        log "ERROR: Validation command failed with unexpected exit code: $EXIT_CODE"
        send_alert "AutoSys Validation Error" \
            "Validation command failed unexpectedly.\nExit code: $EXIT_CODE\nJob: $AUTO_JOB_NAME\nCheck logs: $LOG_FILE"
        exit 2
    fi
}

# Execute main function
main

```

**Notification Script (`send_validation_summary.sh`):**

```bash
#!/bin/bash
# Send daily validation summary to stakeholders

REPORT_DIR="/reports/validation"
TODAY=$(date +%Y%m%d)

# Collect all validation results for today
RESULTS=$(find "$REPORT_DIR" -name "*${TODAY}.json" -type f)

if [ -z "$RESULTS" ]; then
    echo "No validation reports found for $TODAY"
    exit 0
fi

# Generate summary
{
    echo "Data Validation Summary for $(date +%Y-%m-%d)"
    echo "=" | tr '=' '='
    echo ""

    for result_file in $RESULTS; do
        job_name=$(basename "$result_file" .json)
        status=$(python3 -c "import json; print(json.load(open('$result_file'))['overall_status'])")
        errors=$(python3 -c "import json; print(json.load(open('$result_file'))['total_errors'])")
        warnings=$(python3 -c "import json; print(json.load(open('$result_file'))['total_warnings'])")

        echo "Job: $job_name"
        echo "  Status: $status"
        echo "  Errors: $errors"
        echo "  Warnings: $warnings"
        echo ""
    done
} | mail -s "Daily Validation Summary - $(date +%Y-%m-%d)" data-team@company.com
```

**Monitoring Script (`check_validation_status.sh`):**

```bash
#!/bin/bash
# Check validation status and update monitoring dashboard

JSON_REPORT="$1"

if [ ! -f "$JSON_REPORT" ]; then
    echo "Report not found: $JSON_REPORT"
    exit 1
fi

# Extract metrics
STATUS=$(python3 -c "import json; print(json.load(open('$JSON_REPORT'))['overall_status'])")
ERRORS=$(python3 -c "import json; print(json.load(open('$JSON_REPORT'))['total_errors'])")
WARNINGS=$(python3 -c "import json; print(json.load(open('$JSON_REPORT'))['total_warnings'])")
DURATION=$(python3 -c "import json; print(json.load(open('$JSON_REPORT'))['duration_seconds'])")

# Send metrics to monitoring system (example: InfluxDB)
curl -i -XPOST 'http://monitoring-server:8086/write?db=data_quality' \
    --data-binary "validation_status,job=$AUTO_JOB_NAME status=\"$STATUS\",errors=$ERRORS,warnings=$WARNINGS,duration=$DURATION"

# Update dashboard
curl -X POST http://dashboard-api:8080/api/validation-status \
    -H "Content-Type: application/json" \
    -d "{\"job\":\"$AUTO_JOB_NAME\",\"status\":\"$STATUS\",\"errors\":$ERRORS,\"warnings\":$WARNINGS}"
```

**Complete AutoSys Box Job:**

```bash
# Complete ETL Pipeline with Validation
insert_job: ETL_CUSTOMER_BOX
job_type: b
owner: etluser
description: "Customer ETL pipeline with validation"

# Step 1: Extract data
insert_job: EXTRACT_CUSTOMER_DATA
job_type: c
box_name: ETL_CUSTOMER_BOX
command: /apps/etl/scripts/extract_customer_data.sh
machine: prod-etl-01
owner: etluser
description: "Extract customer data from source systems"

# Step 2: Validate data (blocks on failure)
insert_job: VALIDATE_CUSTOMER_DATA
job_type: c
box_name: ETL_CUSTOMER_BOX
command: /apps/validation/scripts/validate_customer_data.sh
machine: prod-etl-01
owner: etluser
condition: success(EXTRACT_CUSTOMER_DATA)
description: "Validate customer data - BLOCKS load on errors"
alarm_if_fail: yes

# Step 3: Load data (only runs if validation passes)
insert_job: LOAD_CUSTOMER_DATA
job_type: c
box_name: ETL_CUSTOMER_BOX
command: /apps/etl/scripts/load_customer_data.sh
machine: prod-etl-01
owner: etluser
condition: success(VALIDATE_CUSTOMER_DATA)
description: "Load validated customer data to warehouse"

# Step 4: Update metadata (runs even if load fails)
insert_job: UPDATE_METADATA
job_type: c
box_name: ETL_CUSTOMER_BOX
command: /apps/etl/scripts/update_metadata.sh
machine: prod-etl-01
owner: etluser
condition: done(LOAD_CUSTOMER_DATA)
description: "Update metadata regardless of load status"

# Step 5: Send notification
insert_job: SEND_NOTIFICATION
job_type: c
box_name: ETL_CUSTOMER_BOX
command: /apps/validation/scripts/send_validation_summary.sh
machine: prod-etl-01
owner: etluser
condition: done(UPDATE_METADATA)
description: "Send validation and load summary"
```

---

## Healthcare Records

**Scenario:** Validate patient records for HIPAA compliance and data quality.

**Business Rules:**
- Patient ID, MRN required
- Date formats standardized
- SSN validation for US patients
- Diagnosis codes valid
- Provider credentials verified

**Configuration:**

```yaml
validation_job:
  name: "Patient Records Validation"
  description: "HIPAA-compliant patient data validation"

settings:
  chunk_size: 1000
  max_sample_failures: 50

files:
  - name: "patient_records"
    path: "/data/healthcare/patients.csv"
    format: "csv"
    encoding: "utf-8"

    validations:
      # Critical identifiers
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "patient_id"
            - "mrn"  # Medical Record Number
            - "first_name"
            - "last_name"
            - "date_of_birth"
            - "gender"

      # Unique patient IDs
      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["patient_id", "mrn"]

      # Date of birth validation
      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "date_of_birth"
          format: "%Y-%m-%d"
          allow_null: false

      # Age validation
      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "age"
          min_value: 0
          max_value: 120

      # Gender validation
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "gender"
          valid_values: ["M", "F", "O", "U"]
          description: "M=Male, F=Female, O=Other, U=Unknown"

      # SSN validation for US patients
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "ssn"
          pattern: "^[0-9]{3}-[0-9]{2}-[0-9]{4}$"
        condition: "country == 'US'"

      # Insurance validation
      - type: "ConditionalValidation"
        severity: "WARNING"
        params:
          condition: "has_insurance == 'Y'"
          then_validate:
            - type: "MandatoryFieldCheck"
              params:
                fields: ["insurance_provider", "policy_number"]
            - type: "ValidValuesCheck"
              params:
                field: "insurance_provider"
                valid_values:
                  - "MEDICARE"
                  - "MEDICAID"
                  - "PRIVATE"
                  - "OTHER"

      # Diagnosis code format (ICD-10)
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "primary_diagnosis_code"
          pattern: "^[A-Z][0-9]{2}(\\.[0-9]{1,4})?$"
          message: "Invalid ICD-10 code format"

      # Provider NPI validation
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "provider_npi"
          pattern: "^[0-9]{10}$"
          message: "NPI must be 10 digits"

      # Email validation (if provided)
      - type: "RegexCheck"
        severity: "WARNING"
        params:
          field: "email"
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

      # Phone validation
      - type: "RegexCheck"
        severity: "WARNING"
        params:
          field: "phone"
          pattern: "^\\+?[0-9]{10,15}$"

      # Address completeness
      - type: "CompletenessCheck"
        severity: "WARNING"
        params:
          field: "address_line1"
          min_completeness: 95.0
        description: "Address required for patient contact"

      # Data freshness
      - type: "FreshnessCheck"
        severity: "WARNING"
        params:
          check_type: "field_value"
          field: "last_updated"
          max_age_hours: 24
        description: "Patient records should be updated daily"
```

---

## API Response Validation

**Scenario:** Validate API response data before processing.

**Data:** JSON responses from external API

**Configuration:**

```yaml
validation_job:
  name: "API Response Validation"
  description: "Validate external API response data"

settings:
  chunk_size: 1000
  max_sample_failures: 100

files:
  - name: "api_response"
    path: "/data/api/response_{timestamp}.json"
    format: "json"
    flatten: true  # Flatten nested JSON structures

    validations:
      # Check we have data
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "RowCountRangeCheck"
        severity: "WARNING"
        params:
          min_rows: 1
          max_rows: 10000

      # Flattened fields from nested JSON
      # Original: {"data": {"user": {"id": 123}}}
      # Flattened: data_user_id

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "data_user_id"
            - "data_user_email"
            - "data_timestamp"
            - "status_code"

      # Status code validation
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "status_code"
          valid_values: [200, 201, 204]
        description: "Only accept successful responses"

      # Email validation from nested field
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "data_user_email"
          pattern: "^[^@]+@[^@]+\\.[^@]+$"

      # Timestamp validation
      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "data_timestamp"
          format: "%Y-%m-%dT%H:%M:%S"

      # API response freshness
      - type: "FreshnessCheck"
        severity: "WARNING"
        params:
          check_type: "field_value"
          field: "data_timestamp"
          max_age_hours: 1
        description: "API data should be recent"
```

---

## Multi-File ETL Pipeline

**Scenario:** Validate multiple related files in an ETL pipeline.

**Files:** Customers, Orders, Order Items (relational data)

**Configuration:**

```yaml
validation_job:
  name: "Multi-File ETL Validation"
  description: "Validate complete order processing pipeline"

settings:
  chunk_size: 5000
  max_sample_failures: 100

files:
  # File 1: Customers
  - name: "customers"
    path: "/data/etl/customers.csv"
    format: "csv"

    validations:
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields: ["customer_id", "email", "name"]

      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["customer_id"]

      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "email"
          pattern: "^[^@]+@[^@]+\\.[^@]+$"

  # File 2: Orders
  - name: "orders"
    path: "/data/etl/orders.csv"
    format: "csv"

    validations:
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "order_id"
            - "customer_id"
            - "order_date"
            - "order_total"

      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["order_id"]

      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "order_date"
          format: "%Y-%m-%d"

      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "order_total"
          min_value: 0

  # File 3: Order Items
  - name: "order_items"
    path: "/data/etl/order_items.csv"
    format: "csv"

    validations:
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "order_item_id"
            - "order_id"
            - "product_id"
            - "quantity"
            - "unit_price"
            - "line_total"

      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["order_item_id"]

      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "quantity"
          min_value: 1

      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "unit_price"
          min_value: 0

      # Business rule: line_total = quantity * unit_price
      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        params:
          rule: "abs(line_total - (quantity * unit_price)) < 0.01"
          description: "Line total must equal quantity * unit price"
          error_message: "Price calculation mismatch"
```

---

## Data Warehouse Loading

**Scenario:** Pre-load validation for data warehouse dimensions and facts.

**Configuration:**

```yaml
validation_job:
  name: "Data Warehouse Load Validation"
  description: "Validate data before warehouse load"

settings:
  chunk_size: 10000
  max_sample_failures: 100

files:
  # Dimension Table
  - name: "dim_customer"
    path: "/data/warehouse/staging/dim_customer.parquet"
    format: "parquet"

    validations:
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "RowCountRangeCheck"
        severity: "WARNING"
        params:
          min_rows: 1000
        description: "Expect minimum customer dimension size"

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "customer_key"  # Surrogate key
            - "customer_id"   # Natural key
            - "effective_date"
            - "expiration_date"
            - "is_current"

      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["customer_key"]
        description: "Surrogate key must be unique"

      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "is_current"
          valid_values: ["Y", "N"]

      - type: "CrossFieldComparisonCheck"
        severity: "ERROR"
        params:
          field1: "effective_date"
          field2: "expiration_date"
          operator: "<="
        description: "Effective date must be before expiration date"

  # Fact Table
  - name: "fact_sales"
    path: "/data/warehouse/staging/fact_sales.parquet"
    format: "parquet"

    validations:
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "sales_key"
            - "date_key"
            - "customer_key"
            - "product_key"
            - "quantity"
            - "unit_price"
            - "total_amount"

      - type: "UniqueKeyCheck"
        severity: "ERROR"
        params:
          fields: ["sales_key"]

      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "quantity"
          min_value: 1

      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "unit_price"
          min_value: 0

      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "total_amount"
          min_value: 0

      # Additive fact check
      - type: "InlineBusinessRuleCheck"
        severity: "ERROR"
        params:
          rule: "abs(total_amount - (quantity * unit_price)) < 0.01"
          description: "Total must equal quantity * unit_price"
```

---

## Real-Time Data Feeds

**Scenario:** Validate streaming data feeds (micro-batches).

**Configuration:**

```yaml
validation_job:
  name: "Real-Time Feed Validation"
  description: "Validate 5-minute micro-batch feeds"

settings:
  chunk_size: 1000
  max_sample_failures: 50  # Limit for real-time

files:
  - name: "sensor_data"
    path: "/data/feeds/sensor_batch_{timestamp}.csv"
    format: "csv"

    validations:
      # Quick file checks
      - type: "EmptyFileCheck"
        severity: "ERROR"

      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "sensor_id"
            - "timestamp"
            - "temperature"
            - "pressure"
            - "status"

      # Timestamp validation
      - type: "DateFormatCheck"
        severity: "ERROR"
        params:
          field: "timestamp"
          format: "%Y-%m-%d %H:%M:%S"

      # Data freshness (must be recent)
      - type: "FreshnessCheck"
        severity: "ERROR"
        params:
          check_type: "field_value"
          field: "timestamp"
          max_age_hours: 1
        description: "Real-time data must be within 1 hour"

      # Sensor reading ranges
      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "temperature"
          min_value: -40
          max_value: 125
        description: "Temperature sensor range"

      - type: "RangeCheck"
        severity: "ERROR"
        params:
          field: "pressure"
          min_value: 0
          max_value: 1000
        description: "Pressure sensor range"

      # Status validation
      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "status"
          valid_values: ["ONLINE", "OFFLINE", "MAINTENANCE", "ERROR"]

      # Statistical outlier detection (flag anomalies)
      - type: "StatisticalOutlierCheck"
        severity: "WARNING"
        params:
          field: "temperature"
          method: "zscore"
          threshold: 3.0
        description: "Flag temperature anomalies"
```

---

## Regulatory Compliance

**Scenario:** GDPR, SOX, or regulatory compliance validation.

**Configuration:**

```yaml
validation_job:
  name: "Regulatory Compliance Validation"
  description: "GDPR and SOX compliance checks"

settings:
  chunk_size: 5000
  max_sample_failures: 0  # Zero tolerance for compliance

files:
  - name: "customer_data"
    path: "/data/compliance/customer_data.csv"
    format: "csv"

    validations:
      # GDPR: Consent tracking
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "consent_marketing"
            - "consent_data_processing"
            - "consent_timestamp"
        description: "GDPR: Consent must be recorded"

      - type: "ValidValuesCheck"
        severity: "ERROR"
        params:
          field: "consent_marketing"
          valid_values: ["YES", "NO"]
        description: "GDPR: Explicit consent values"

      # PII Encryption check
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "ssn_encrypted"
          pattern: "^ENC\\[[A-Za-z0-9+/=]+\\]$"
        description: "SOX: SSN must be encrypted"

      # Data retention compliance
      - type: "FreshnessCheck"
        severity: "WARNING"
        params:
          check_type: "field_value"
          field: "created_date"
          max_age_hours: 26280  # 3 years
        description: "GDPR: Flag records older than retention period"

      # Audit trail
      - type: "MandatoryFieldCheck"
        severity: "ERROR"
        params:
          fields:
            - "created_by"
            - "created_timestamp"
            - "modified_by"
            - "modified_timestamp"
        description: "SOX: Audit trail required"

      # No test data in production
      - type: "RegexCheck"
        severity: "ERROR"
        params:
          field: "email"
          pattern: "@(test|example|dummy)\\.com$"
          invert: true
        description: "Compliance: No test data in production"
```

---

## Quick Command Reference

```bash
# Basic validation
python3 -m validation_framework.cli validate config.yaml

# With reports
python3 -m validation_framework.cli validate config.yaml \
  --html report.html \
  --json results.json

# AutoSys integration (in script)
python3 -m validation_framework.cli validate config.yaml \
  --json results.json
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
  echo "Validation failed - blocking load"
  exit 1
fi

# Cron job
0 2 * * * cd /apps/validation && python3 -m validation_framework.cli validate daily.yaml --html /reports/$(date +\%Y\%m\%d).html

# Parallel processing
for config in configs/*.yaml; do
  python3 -m validation_framework.cli validate "$config" --json "results/$(basename $config .yaml).json" &
done
wait
```

---

## Next Steps

- **[User Guide](USER_GUIDE.md)** - Complete configuration reference
- **[Validation Catalog](VALIDATION_CATALOG.md)** - All validation types
- **[Advanced Guide](ADVANCED_GUIDE.md)** - Complex configurations
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Custom validations

---

**Need help with your specific scenario?** Review the [User Guide](USER_GUIDE.md) or create an issue in the repository.
