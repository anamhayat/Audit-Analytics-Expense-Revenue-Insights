# Audit Analytics Project

A portfolio-ready Python project tailored to Anam Hayat's resume, focusing on audit analytics for expense and revenue monitoring, anomaly detection, duplicate checks, variance analysis, and KPI reporting.

## Project Objective
Build an end-to-end audit analytics workflow using Python and SQL-style logic to:
- validate expense and revenue transactions
- detect duplicate and suspicious transactions
- flag policy threshold breaches
- summarize cost center and department level KPIs
- generate outputs suitable for internal audit and compliance review

## Resume Alignment
This project reflects the profile described in the resume by demonstrating:
- Python and Pandas for data cleaning, transformation, and analytics
- SQL-style duplicate and anomaly logic
- KPI development for audit and compliance use cases
- automated reporting for expense and revenue insights
- stakeholder-friendly output tables for dashboards or Power BI integration

## Project Structure
```
audit_analytics_project/
├── data/
│   └── sample_transactions.csv
├── src/
│   ├── generate_sample_data.py
│   ├── audit_analytics.py
│   └── sql_checks.sql
├── README.md
└── requirements.txt
```

## Features
- Expense and revenue validation checks
- Duplicate transaction detection
- High-value and suspicious transaction flags
- Monthly variance analysis by department and cost center
- Vendor concentration analysis
- Audit summary export files for dashboarding

## How to Run
1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Generate sample data if needed
```bash
python src/generate_sample_data.py
```

3. Run the audit analytics pipeline
```bash
python src/audit_analytics.py
```

## Outputs
The script creates an `outputs/` folder with:
- cleaned transactions file
- flagged transactions file
- department KPI summary
- monthly variance summary
- vendor concentration summary

## Suggested Resume Project Title
**Audit Analytics – Expense, Revenue & Compliance Monitoring (Python, SQL, Pandas)**

## Interview Talking Points
- Designed a Python-based audit analytics pipeline for expense and revenue monitoring across departments.
- Automated duplicate detection, threshold checks, and anomaly flags to reduce manual audit effort.
- Built KPI summaries and variance analysis outputs that can feed Power BI dashboards.
- Applied SQL-style audit rules and data validation to improve transaction-level review quality.
