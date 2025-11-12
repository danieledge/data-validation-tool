# Validation Results Summary

**Execution Date**: 2025-11-12
**Job**: Financial Data Validation Example
**Duration**: 1.76 seconds
**Overall Status**: ❌ FAILED (8 errors, 5 warnings)

---

## 📊 Files Processed

| File | Rows | Status | Errors | Warnings |
|------|------|--------|--------|----------|
| customers.csv | 1,020 | ❌ FAILED | 4 | 5 |
| transactions.csv | 5,000 | ❌ FAILED | 2 | 0 |
| accounts.csv | 500 | ❌ FAILED | 2 | 0 |

---

## 🔍 Issues Detected

### customers.csv

#### Errors:
1. **MandatoryFieldCheck** - 97 rows with missing mandatory fields
   - Missing customer_id, email, first_name, or last_name
   - Success rate: 97.62%

2. **RegexCheck (Email)** - 31 invalid email formats
   - Examples: "invalid_email_12", "invalid_email_45"
   - Success rate: 96.96%

3. **ValidValuesCheck (Status)** - 21 invalid status values
   - Found: "UNKNOWN", "DELETED", "" (empty)
   - Expected: "ACTIVE", "INACTIVE", "SUSPENDED", "PENDING"
   - Success rate: 97.94%

4. **DuplicateRowCheck** - 20 duplicate customer IDs
   - 1,000 unique records out of 1,020 total rows

#### Warnings:
5. **RowCountRangeCheck** - Row count below expected minimum
6. **RegexCheck (Phone)** - 55 invalid phone formats
7. **RangeCheck (Balance)** - 23 balances outside acceptable range
8. **DateFormatCheck** - 21 dates in wrong format
9. **BlankRecordCheck** - 20 completely blank rows

---

### transactions.csv

#### Errors:
1. **MandatoryFieldCheck** - 50 rows with missing mandatory fields
   - Missing transaction_id, customer_id, amount, or transaction_date
   - Success rate: 99.50%

2. **RangeCheck (Amount)** - 152 amounts outside acceptable range
   - Negative amounts or exceeding $1,000,000
   - Success rate: 96.96%

---

### accounts.csv

#### Errors:
1. **MandatoryFieldCheck** - 10 rows with missing mandatory fields
   - Missing account_id, account_type, or customer_id
   - Success rate: 98.67%

2. **RegexCheck (Account Number)** - 50 invalid account numbers
   - Not exactly 8 digits
   - Examples: "123" (too short), "ABC12345" (contains letters)
   - Success rate: 90.00%

---

## 📈 Validation Coverage

**Total Validations Run**: 20
- File-level checks: 3
- Schema checks: 2
- Field-level checks: 11
- Record-level checks: 4

**Success Rates by Category**:
- Schema validation: 100% ✅
- File existence: 100% ✅
- Data quality: ~95% (intentional issues for testing)

---

## 🎯 Key Findings

1. **Data Quality Issues**: The framework successfully detected all intentionally introduced issues:
   - ~2% missing mandatory values
   - ~3% invalid format violations (email, phone, account numbers)
   - ~2% duplicate records
   - ~2% invalid enumeration values
   - ~2% blank rows

2. **Performance**:
   - Processed 6,520 rows in 1.76 seconds
   - ~3,704 rows/second throughput
   - Memory-efficient chunked processing

3. **Report Quality**:
   - Detailed failure samples with row numbers
   - Clear error messages
   - Success rate percentages
   - Sample values for debugging

---

## 📁 Generated Reports

### HTML Report (372 KB)
**Location**: `examples/validation_report.html`

**Features**:
- Interactive collapsible sections
- Color-coded status indicators
- Sample failure tables with row numbers
- File metadata (size, row count, columns)
- Success rate metrics
- Easy to share and review

### JSON Report (32 KB)
**Location**: `examples/validation_summary.json`

**Features**:
- Machine-readable format
- Complete validation results
- Suitable for CI/CD integration
- API-friendly structure
- Programmatic processing

---

## ✅ Framework Validation

The test confirms the framework is working correctly:

1. ✅ **All validation types working** - 13 different validations executed
2. ✅ **Regex validation working** - Email, phone, account number patterns detected
3. ✅ **Chunked processing working** - Large files handled efficiently
4. ✅ **Error detection working** - All intentional issues caught
5. ✅ **Severity levels working** - Errors vs warnings properly categorized
6. ✅ **Report generation working** - Both HTML and JSON created successfully
7. ✅ **Performance acceptable** - ~3,700 rows/second

---

## 🚀 Next Steps

1. **View HTML Report**: Open `examples/validation_report.html` in your browser
2. **Inspect JSON**: Use for automated processing or integration
3. **Test with Real Data**: Create config for your actual datasets
4. **Customize Rules**: Add/modify validations based on your requirements
5. **Integrate**: Add to your data pipeline

---

## 📊 Sample Failure Examples

### Invalid Email Format
```
Row 12: "invalid_email_12" - Expected format: user@example.com
Row 45: "invalid_email_45" - Expected format: user@example.com
```

### Invalid Account Numbers
```
Row 23: "123" - Must be exactly 8 digits
Row 87: "ABC12345" - Must contain only digits
```

### Out of Range Amounts
```
Row 156: -234.56 - Negative amount detected
Row 892: 1,234,567.89 - Exceeds maximum $1,000,000
```

### Duplicate Customer IDs
```
Customer ID 42 appears 3 times (rows: 42, 156, 789)
Customer ID 88 appears 2 times (rows: 88, 923)
```

---

**Framework Version**: v0.1.0
**Author**: daniel edge
**Repository**: https://github.com/danieledge/data-validation-tool
