import csv
import random
from datetime import datetime, timedelta

# Generate 5000 rows of realistic e-commerce data
records = []
start_date = datetime(2024, 1, 1)

statuses = ['COMPLETED', 'SHIPPED', 'PENDING', 'CANCELLED']
categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty']
countries = ['USA', 'UK', 'CA', 'FR', 'DE', 'AU', 'ES', 'IT']
first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank',
               'Grace', 'Henry', 'Iris', 'Jack', 'Kelly', 'Leo', 'Mia', 'Noah',
               'Olivia', 'Paul', 'Quinn', 'Rachel']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
              'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez']

for i in range(5000):
    order_id = 100001 + i
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    name = f"{fname} {lname}"

    # 5% missing emails
    if random.random() < 0.05:
        email = ""
    else:
        email = f"{fname.lower()}.{lname.lower()}@email.com"

    order_date = (start_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')

    # Amount varies by category
    category = random.choice(categories)
    if category == 'Electronics':
        amount = round(random.uniform(500, 5000), 2)
    elif category == 'Clothing':
        amount = round(random.uniform(50, 500), 2)
    elif category == 'Books':
        amount = round(random.uniform(10, 100), 2)
    else:
        amount = round(random.uniform(20, 1000), 2)

    status = random.choice(statuses)
    quantity = random.randint(1, 20)
    country = random.choice(countries)

    # Discount varies by status
    if status == 'CANCELLED':
        discount = 0.0
    elif status == 'COMPLETED':
        discount = round(random.uniform(5, 25), 1)
    else:
        discount = round(random.uniform(0, 15), 1)

    records.append({
        'order_id': order_id,
        'customer_name': name,
        'email': email,
        'order_date': order_date,
        'amount': amount,
        'status': status,
        'quantity': quantity,
        'product_category': category,
        'shipping_country': country,
        'discount_pct': discount
    })

# Write to CSV
with open('large_example_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print(f"Generated {len(records)} records")
