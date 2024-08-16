-- Calculate EPS for each booking in 2019 and 2023
WITH eps_data AS (
    SELECT
        YEAR(paidon) AS year,
        SUM(total_usd) AS total_revenue,
        SUM(seats) AS total_seats,
        SUM(total_usd) / SUM(seats) AS eps
    FROM
        `12go`.analytic_test_booking
    WHERE
        YEAR(paidon) IN (2019, 2023)
    GROUP BY
        YEAR(paidon)
)
SELECT
    year,
    total_revenue,
    total_seats,
    eps
FROM
    eps_data;
 
   
 
-- 1. EPS by From and To Stations

   
SELECT
    from_id,
    to_id,
    YEAR(paidon) AS year,
    SUM(total_usd) / SUM(seats) AS eps
FROM
    `12go`.analytic_test_booking
WHERE
    paidon BETWEEN '2019-01-01' AND '2019-12-31'
    OR paidon BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY
    from_id, to_id, YEAR(paidon)
ORDER BY
    from_id, to_id, year;
   

-- 2. EPS by Operator

SELECT
    operator_id,
    YEAR(paidon) AS year,
    SUM(total_usd) / SUM(seats) AS eps
FROM
    `12go`.analytic_test_booking
WHERE
    paidon BETWEEN '2019-01-01' AND '2019-12-31'
    OR paidon BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY
    operator_id, YEAR(paidon)
ORDER BY
    operator_id, year;
   
   
--  3. EPS by Vehicle Class
  
 SELECT
    class_name,
    YEAR(paidon) AS year,
    SUM(total_usd) / SUM(seats) AS eps
FROM
    `12go`.analytic_test_booking
WHERE
    paidon BETWEEN '2019-01-01' AND '2019-12-31'
    OR paidon BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY
    class_name, YEAR(paidon)
ORDER BY
    class_name, year;

-- 4. EPS by Country of Origin
   
  SELECT
    from_country_id,
    YEAR(paidon) AS year,
    SUM(total_usd) / SUM(seats) AS eps
FROM
    `12go`.analytic_test_booking
WHERE
    paidon BETWEEN '2019-01-01' AND '2019-12-31'
    OR paidon BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY
    from_country_id, YEAR(paidon)
ORDER BY
    from_country_id, year;

   
--  5. Price Trends Over Time
   
  SELECT
    YEAR(paidon) AS year,
    AVG(total_usd / seats) AS avg_price_per_seat
FROM
    `12go`.analytic_test_booking
WHERE
    paidon BETWEEN '2019-01-01' AND '2019-12-31'
    OR paidon BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY
    YEAR(paidon)
ORDER BY
    year;




