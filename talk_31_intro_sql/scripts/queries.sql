-- BASIC STATEMENTS
SELECT emp_id, fname, lname, start_date, title
FROM employee
WHERE title = 'Head Teller';

/* WHERE end_date IS NULL
AND NOT (title = 'Teller' OR start_date < '2003-01-01') */

SELECT emp_id, fname, lname, start_date, title
FROM employee
WHERE (title = 'Head Teller' AND start_date > '2002-01-01')
    OR (title = 'Teller' AND start_date > '2003-01-01');

/* SELECT account_id, product_cd, open_date, avail_balance
FROM account
ORDER BY avail_balance DESC; */

-- SIMPLE OPERATIONS
select account_id, avail_balance,
	round(avail_balance * 0.01, 2) as one_percent_charge,
	round(15/NULLIF(avail_balance, 0)*100, 2) loyalty_gift
from account;

-- GROUPING
SELECT title, count(*)
FROM employee
GROUP BY  title
;

-- AGGREGATE FUNCTIONS
SELECT MAX(avail_balance) max_balance,
MIN(avail_balance) min_balance,
AVG(avail_balance) avg_balance,
SUM(avail_balance) tot_balance,
COUNT(*) num_accounts
FROM account
WHERE product_cd = 'CHK';
-- GROUP BY product_cd
-- HAVING MIN(avail_balance) > 2000
;

-- JOINS
SELECT e.fname, e.lname, d.name
FROM employee e JOIN department d
ON e.dept_id = d.dept_id;

SELECT a.account_id, a.cust_id, a.open_date, a.product_cd
FROM account a INNER JOIN employee e
	ON a.open_emp_id = e.emp_id
	INNER JOIN branch b
	ON e.assigned_branch_id = b.branch_id
WHERE e.start_date <= '2003-01-01'
AND (e.title = 'Teller' OR e.title = 'Head Teller')
AND b.name = 'Woburn Branch';

-- SELF JOINS
/* SELECT e.fname, e.lname,
e_mgr.fname mgr_fname, e_mgr.lname mgr_lname
FROM employee e INNER JOIN employee e_mgr
ON e.superior_emp_id = e_mgr.emp_id; */

-- OUTER JOINS
/* SELECT a.account_id, a.cust_id, b.name
FROM account a LEFT OUTER JOIN business b
ON a.cust_id = b.cust_id; */

SELECT a.account_id, a.product_cd,
	CONCAT(i.fname, ' ', i.lname) person_name,
	b.name business_name
FROM account a LEFT OUTER JOIN individual i
ON a.cust_id = i.cust_id
LEFT OUTER JOIN business b
ON a.cust_id = b.cust_id;


-- SUBQUERIES & COMMON TABLE EXPRESSIONS (CTE)
SELECT d.dept_id, d.name, e_cnt.how_many num_employees
FROM department d INNER JOIN
(SELECT dept_id, COUNT(*) how_many
FROM employee
GROUP BY dept_id) e_cnt
ON d.dept_id = e_cnt.dept_id;

WITH e_cnt AS (SELECT dept_id, COUNT(*) how_many
	FROM employee
	GROUP BY dept_id)
SELECT d.dept_id, d.name, e_cnt.how_many num_employees
FROM department d INNER join e_cnt
ON d.dept_id = e_cnt.dept_id;

-- CONDITIONAL LOGIC
SELECT c.cust_id, c.fed_id,
case WHEN c.cust_type_cd = 'I' THEN
	(SELECT CONCAT(i.fname, ' ', i.lname)
	 FROM individual i
	 WHERE i.cust_id = c.cust_id)
WHEN c.cust_type_cd = 'B' THEN
	(SELECT b.name
	FROM business b
	WHERE b.cust_id = c.cust_id)
ELSE 'Unknown'
	END name
FROM customer c;


-- WINDOW FUNCTIONS
with monthly_trans as (
	select date_trunc('month', cast(txn_date as timestamp)) yymm, sum(amount) monthly_amount
	from "transaction" t 
	group by date_trunc('month', cast(txn_date as timestamp))
)
select yymm, SUM(monthly_amount) OVER (ORDER BY yymm) AS running_total
from monthly_trans;

-- LAG
with monthly_trans as (
	select date_trunc('month', cast(txn_date as timestamp)) yymm, sum(amount) monthly_amount
	from "transaction" t 
	group by date_trunc('month', cast(txn_date as timestamp))
),
monthly_running_trans as (
	select yymm, SUM(monthly_amount) OVER (ORDER BY yymm) AS running_total
	from monthly_trans
)
SELECT yymm,
       running_total,
       running_total - LAG(running_total, 1) OVER
         (ORDER BY running_total)
         AS difference,
       round(running_total / LAG(running_total, 1) OVER
         (ORDER BY running_total), 2) * 100 
         AS percentage
FROM monthly_running_trans;


