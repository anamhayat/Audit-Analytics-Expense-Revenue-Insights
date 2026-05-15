-- Duplicate invoice and amount check
SELECT invoice_id, vendor_name, amount, COUNT(*) AS duplicate_count
FROM transactions
GROUP BY invoice_id, vendor_name, amount
HAVING COUNT(*) > 1;

-- High-value transactions
SELECT *
FROM transactions
WHERE amount >= 150000;

-- High-value cash transactions
SELECT *
FROM transactions
WHERE payment_mode = 'Cash'
  AND amount >= 50000;

-- Department monthly variance base
SELECT
    DATE_TRUNC('month', transaction_date) AS month,
    department,
    transaction_type,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY 1, 2, 3;

-- Suspicious transactions using z-score logic would typically be computed in Python or advanced SQL
