import os
import numpy as np
import pandas as pd

INPUT_PATH = 'data/sample_transactions.csv'
OUTPUT_DIR = 'outputs'
HIGH_VALUE_THRESHOLD = 150000
CASH_THRESHOLD = 50000

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['transaction_date'])
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def add_validation_flags(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work['year_month'] = work['transaction_date'].dt.to_period('M').astype(str)
    work['is_missing_key_field'] = work[['department', 'cost_center', 'vendor_name', 'invoice_id']].isna().any(axis=1)
    work['is_high_value'] = work['amount'] >= HIGH_VALUE_THRESHOLD
    work['is_cash_high_value'] = (work['payment_mode'].eq('Cash')) & (work['amount'] >= CASH_THRESHOLD)
    work['is_duplicate_invoice'] = work.duplicated(subset=['invoice_id', 'vendor_name', 'amount'], keep=False)

    dept_month_avg = work.groupby(['department', 'year_month'])['amount'].transform('mean')
    dept_month_std = work.groupby(['department', 'year_month'])['amount'].transform('std').fillna(0)
    work['z_score'] = np.where(dept_month_std > 0, (work['amount'] - dept_month_avg) / dept_month_std, 0)
    work['is_statistical_anomaly'] = work['z_score'].abs() >= 3

    work['audit_flag_count'] = work[[
        'is_missing_key_field', 'is_high_value', 'is_cash_high_value',
        'is_duplicate_invoice', 'is_statistical_anomaly'
    ]].sum(axis=1)

    work['audit_status'] = np.where(work['audit_flag_count'] > 0, 'Review', 'OK')
    return work

def department_kpis(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['department', 'transaction_type'], as_index=False).agg(
        transaction_count=('transaction_id', 'count'),
        total_amount=('amount', 'sum'),
        flagged_transactions=('audit_status', lambda x: (x == 'Review').sum()),
        high_value_txns=('is_high_value', 'sum'),
        duplicate_txns=('is_duplicate_invoice', 'sum'),
        anomaly_txns=('is_statistical_anomaly', 'sum')
    )

def monthly_variance(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.groupby(['year_month', 'department', 'transaction_type'], as_index=False)['amount'].sum()
    monthly = monthly.sort_values(['department', 'transaction_type', 'year_month'])
    monthly['previous_month_amount'] = monthly.groupby(['department', 'transaction_type'])['amount'].shift(1)
    monthly['variance'] = monthly['amount'] - monthly['previous_month_amount']
    monthly['variance_pct'] = np.where(
        monthly['previous_month_amount'].fillna(0) != 0,
        (monthly['variance'] / monthly['previous_month_amount']) * 100,
        np.nan
    )
    return monthly

def vendor_concentration(df: pd.DataFrame) -> pd.DataFrame:
    vendor = df[df['transaction_type'] == 'Expense'].groupby('vendor_name', as_index=False).agg(
        expense_amount=('amount', 'sum'),
        transaction_count=('transaction_id', 'count'),
        flagged_transactions=('audit_status', lambda x: (x == 'Review').sum())
    )
    total = vendor['expense_amount'].sum()
    vendor['expense_share_pct'] = (vendor['expense_amount'] / total * 100).round(2)
    return vendor.sort_values('expense_amount', ascending=False)

def main():
    df = load_data(INPUT_PATH)
    audited = add_validation_flags(df)
    flagged = audited[audited['audit_status'] == 'Review'].sort_values(['audit_flag_count', 'amount'], ascending=[False, False])

    audited.to_csv(f'{OUTPUT_DIR}/cleaned_transactions.csv', index=False)
    flagged.to_csv(f'{OUTPUT_DIR}/flagged_transactions.csv', index=False)
    department_kpis(audited).to_csv(f'{OUTPUT_DIR}/department_kpi_summary.csv', index=False)
    monthly_variance(audited).to_csv(f'{OUTPUT_DIR}/monthly_variance_summary.csv', index=False)
    vendor_concentration(audited).to_csv(f'{OUTPUT_DIR}/vendor_concentration_summary.csv', index=False)

if __name__ == '__main__':
    main()
