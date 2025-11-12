## Open Source Financial Datasets for Testing

This document lists publicly available financial datasets suitable for testing the Data Validation Framework.

---

## 1. IBM AML-Data (Anti-Money Laundering)

**Recommended for Testing**

### Description
Synthetic financial transaction data generated using multi-agent simulation. Includes bank transfers, purchases, credit card transactions, checks, etc. Some transactions are labeled as money laundering for ML training purposes.

### Details
- **Format**: CSV
- **License**: CDLA-Sharing-1.0 (data), Apache-2.0 (code)
- **Size**: Large dataset with millions of transactions
- **Quality**: Synthetic but realistic

### Download
- **Kaggle (improved version)**: https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml
- **IBM Box (original)**: https://ibm.box.com/v/AML-Anti-Money-Laundering-Data

### Typical Fields
- Transaction ID
- From/To Account
- Amount
- Timestamp
- Transaction Type
- Is Laundering (label)

### Sample Validation Config
```yaml
validation_job:
  name: "IBM AML Data Validation"

  files:
    - name: "transactions"
      path: "data/ibm_aml_transactions.csv"
      format: "csv"

      validations:
        - type: "EmptyFileCheck"
          severity: "ERROR"

        - type: "MandatoryFieldCheck"
          severity: "ERROR"
          params:
            fields: ["Transaction_ID", "From_Account", "To_Account", "Amount", "Timestamp"]

        - type: "RangeCheck"
          severity: "WARNING"
          params:
            field: "Amount"
            min_value: 0.01
            max_value: 10000000

        - type: "UniqueKeyCheck"
          severity: "ERROR"
          params:
            fields: ["Transaction_ID"]
```

---

## 2. Banking Dataset (GitHub - ahsan084)

### Description
Detailed information about banking transactions and customer data for financial analysis and predictive modeling.

### Details
- **Format**: CSV
- **License**: MIT
- **Repository**: https://github.com/ahsan084/Banking-Dataset

### Download
Clone the repository:
```bash
git clone https://github.com/ahsan084/Banking-Dataset.git
```

---

## 3. Berka Dataset (PKDD'99)

### Description
Real anonymized data from a Czech bank, used in the PKDD'99 Discovery Challenge. Contains account information, transactions, loans, and demographic data.

### Details
- **Format**: CSV (multiple tables)
- **Size**: ~1MB
- **Quality**: Real anonymized data

### Download
Available from various sources:
- http://lisp.vse.cz/pkdd99/Challenge/
- https://data.world/lpetrocelli/czech-financial-dataset-real-anonymized-transactions

### Tables
- account.csv
- card.csv
- client.csv
- disp.csv
- district.csv
- loan.csv
- order.csv
- trans.csv (transactions)

### Sample Validation Config
```yaml
validation_job:
  name: "Berka Dataset Validation"

  files:
    - name: "transactions"
      path: "berka/trans.csv"
      format: "csv"
      delimiter: ";"

      validations:
        - type: "MandatoryFieldCheck"
          severity: "ERROR"
          params:
            fields: ["trans_id", "account_id", "date", "amount"]

        - type: "DateFormatCheck"
          severity: "ERROR"
          params:
            field: "date"
            format: "%y%m%d"  # YYMMDD format
```

---

## 4. Kaggle Credit Card Fraud Detection

### Description
Credit card transactions dataset with fraud labels. Highly imbalanced dataset (0.172% frauds).

### Details
- **Format**: CSV
- **Size**: ~150MB, 284,807 transactions
- **License**: Open Database License (DbCL)
- **Download**: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

### Fields
- Time, V1-V28 (PCA features), Amount, Class (fraud label)

---

## 5. Sample Data Generator

### Description
Use the included sample data generator to create test datasets with known data quality issues.

### Generate Sample Data
```bash
cd data-validation-tool
python examples/generate_sample_data.py
```

This creates:
- `customers.csv` - Customer data with various issues
- `transactions.parquet` - Transaction data in Parquet format
- `accounts.xlsx` - Account data in Excel format

### Known Issues Included
- Missing mandatory fields (~1-2%)
- Invalid email/phone formats (~3-5%)
- Duplicate IDs (~1-2%)
- Out of range values (~2-3%)
- Invalid enum values (~2%)
- Blank rows (~2%)
- Invalid account numbers (~10%)

### Test Configuration
```bash
data-validate validate examples/sample_config.yaml
```

---

## 6. World Bank Open Data

### Description
Global financial and development data including economic indicators, poverty statistics, and country-specific metrics.

### Details
- **Format**: CSV, XML, JSON (API available)
- **License**: CC BY 4.0
- **Website**: https://data.worldbank.org/

### Use Case
Good for validating macroeconomic data, time series, and cross-country datasets.

---

## 7. US Treasury Data (Data.gov)

### Description
Various US government financial datasets including spending, debt, and budget data.

### Details
- **Format**: CSV, JSON, XML
- **License**: Public Domain
- **Website**: https://data.gov (search "treasury" or "financial")

---

## Recommendations by File Size

### Small Files (<10MB)
- Berka Dataset
- Generated sample data
- Good for quick testing and development

### Medium Files (10MB-1GB)
- Kaggle Credit Card Fraud
- Banking Dataset (GitHub)
- Good for validation logic testing

### Large Files (>1GB)
- IBM AML-Data
- Good for performance testing with chunked processing
- Test with large chunk_size settings

---

## Testing Checklist

When testing with a new dataset:

1. **File Format Test**
   - Ensure loader correctly handles the format
   - Verify metadata extraction

2. **Schema Validation**
   - Test column detection
   - Verify data type inference

3. **Data Quality Checks**
   - Run mandatory field checks
   - Test format validations (email, phone, etc.)
   - Check for duplicates

4. **Performance Test**
   - Monitor memory usage with large files
   - Test chunked processing
   - Verify execution time

5. **Report Generation**
   - Check HTML report renders correctly
   - Verify JSON output structure
   - Ensure sample failures are captured

---

## Creating Custom Test Data

For specific testing needs, create custom datasets with tools like:

- **Faker** (Python): Generate realistic fake data
- **Mockaroo**: Web-based test data generator
- **Synthea**: Synthetic medical data (adaptable)

Example with Faker:
```python
from faker import Faker
import pandas as pd

fake = Faker()

data = []
for _ in range(10000):
    data.append({
        'customer_id': fake.random_int(1, 100000),
        'name': fake.name(),
        'email': fake.email(),
        'balance': fake.pyfloat(left_digits=5, right_digits=2, positive=True)
    })

df = pd.DataFrame(data)
df.to_csv('test_customers.csv', index=False)
```

---

## Support

For issues with specific datasets or validation configs, please open an issue on the project repository.
