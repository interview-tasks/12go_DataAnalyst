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
 
