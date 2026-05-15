import os
import numpy as np
import pandas as pd

np.random.seed(42)
rows = 1200
months = pd.date_range('2025-01-01', '2025-12-01', freq='MS')
departments = ['Finance', 'Operations', 'Sales', 'HR', 'IT']
cost_centers = ['CC101', 'CC102', 'CC201', 'CC301', 'CC401', 'CC501']
vendors = ['Alpha Supplies', 'Bright Systems', 'CareMed', 'Delta Services', 'Epsilon Tech', 'FastLogix']
transaction_types = ['Expense', 'Revenue']
payment_modes = ['Bank Transfer', 'Card', 'Cash', 'UPI']

records = []
for i in range(rows):
    tx_date = np.random.choice(months) + pd.to_timedelta(np.random.randint(0, 28), unit='D')
    dept = np.random.choice(departments)
    cc = np.random.choice(cost_centers)
    tx_type = np.random.choice(transaction_types, p=[0.7, 0.3])
    vendor = np.random.choice(vendors)
    amount = round(np.random.gamma(3, 18000), 2)
    if tx_type == 'Revenue':
        amount = round(np.random.gamma(4, 25000), 2)
    payment_mode = np.random.choice(payment_modes, p=[0.45, 0.25, 0.1, 0.2])
    invoice_id = f'INV{10000 + np.random.randint(0, 3000)}'
    employee_id = f'EMP{100 + np.random.randint(0, 90)}'
    records.append([
        f'TX{i+1:05d}', pd.Timestamp(tx_date).date(), dept, cc, tx_type,
        vendor, amount, payment_mode, invoice_id, employee_id
    ])

df = pd.DataFrame(records, columns=[
    'transaction_id', 'transaction_date', 'department', 'cost_center', 'transaction_type',
    'vendor_name', 'amount', 'payment_mode', 'invoice_id', 'employee_id'
])

dupes = df.sample(25, random_state=7).copy()
dupes['transaction_id'] = [f'DUP{i:03d}' for i in range(len(dupes))]
df = pd.concat([df, dupes], ignore_index=True)

suspicious_idx = df.sample(18, random_state=11).index
df.loc[suspicious_idx, 'amount'] = df.loc[suspicious_idx, 'amount'] * 6
cash_idx = df.sample(20, random_state=15).index
df.loc[cash_idx, 'payment_mode'] = 'Cash'

os.makedirs('data', exist_ok=True)
df.to_csv('data/sample_transactions.csv', index=False)
print('Generated data/sample_transactions.csv')
