SELECT
    vehclass_id,
    class_name,
    YEAR(paidon) AS year,
    SUM(seats) AS total_seats,
    SUM(netprice_usd) AS total_netprice,
    SUM(total_usd) AS total_revenue,
    (SUM(total_usd) - SUM(netprice_usd)) / SUM(seats) AS EPS
FROM
    `12go`.analytic_test_booking
GROUP BY
    vehclass_id,
    class_name,
    YEAR(paidon)
ORDER BY
    year, EPS DESC;

   
 SELECT
    vehclass_id,
    class_name,
    SUM(CASE WHEN YEAR(paidon) = 2019 THEN seats ELSE 0 END) AS total_seats_2019,
    SUM(CASE WHEN YEAR(paidon) = 2023 THEN seats ELSE 0 END) AS total_seats_2023,
    SUM(CASE WHEN YEAR(paidon) = 2019 THEN netprice_usd ELSE 0 END) AS total_netprice_2019,
    SUM(CASE WHEN YEAR(paidon) = 2023 THEN netprice_usd ELSE 0 END) AS total_netprice_2023,
    SUM(CASE WHEN YEAR(paidon) = 2019 THEN total_usd ELSE 0 END) AS total_revenue_2019,
    SUM(CASE WHEN YEAR(paidon) = 2023 THEN total_usd ELSE 0 END) AS total_revenue_2023,
    (SUM(CASE WHEN YEAR(paidon) = 2019 THEN total_usd ELSE 0 END) - SUM(CASE WHEN YEAR(paidon) = 2019 THEN netprice_usd ELSE 0 END)) / SUM(CASE WHEN YEAR(paidon) = 2019 THEN seats ELSE 0 END) AS EPS_2019,
    (SUM(CASE WHEN YEAR(paidon) = 2023 THEN total_usd ELSE 0 END) - SUM(CASE WHEN YEAR(paidon) = 2023 THEN netprice_usd ELSE 0 END)) / SUM(CASE WHEN YEAR(paidon) = 2023 THEN seats ELSE 0 END) AS EPS_2023,
    (SUM(CASE WHEN YEAR(paidon) = 2023 THEN total_usd ELSE 0 END) - SUM(CASE WHEN YEAR(paidon) = 2023 THEN netprice_usd ELSE 0 END)) / SUM(CASE WHEN YEAR(paidon) = 2023 THEN seats ELSE 0 END) -
    (SUM(CASE WHEN YEAR(paidon) = 2019 THEN total_usd ELSE 0 END) - SUM(CASE WHEN YEAR(paidon) = 2019 THEN netprice_usd ELSE 0 END)) / SUM(CASE WHEN YEAR(paidon) = 2019 THEN seats ELSE 0 END) AS EPS_change
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(paidon) IN (2019, 2023)
GROUP BY
    vehclass_id,
    class_name
ORDER BY
    EPS_change DESC;


-- This query retrieves data required for the analysis of EPS (Earn Per Seat) by vehicle class for the years 2019 and 2023.


SELECT
    vehclass_id,
    netprice_usd,
    seats,
    netprice_usd / seats AS eps,
    YEAR(godate) AS year,
    refund_usd,
    total_usd,
    trip_duration_minutes
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023);


-- Query to Aggregate Data by Vehicle Class and Year:
-- This query aggregates the data to calculate metrics like average EPS, total net revenue, total seats, total refunds, and average trip duration by vehicle class and year.

SELECT
    vehclass_id,
    year,
    AVG(eps) AS avg_eps,
    SUM(netprice_usd) AS total_net_revenue,
    SUM(seats) AS total_seats,
    SUM(refund_usd) AS total_refunds,
    SUM(total_usd) AS total_revenue,
    AVG(trip_duration_minutes) AS avg_trip_duration
FROM
(
    SELECT
        vehclass_id,
        netprice_usd,
        seats,
        netprice_usd / seats AS eps,
        YEAR(godate) AS year,
        refund_usd,
        total_usd,
        trip_duration_minutes
    FROM
        `12go`.analytic_test_booking
    WHERE
        YEAR(godate) IN (2019, 2023)
) AS subquery
GROUP BY
    vehclass_id, year;



-- Query to Calculate EPS Growth between 2019 and 2023:
-- This query calculates the growth in EPS from 2019 to 2023 for each vehicle class.

SELECT
    vehclass_id,
    (eps_2023 - eps_2019) / eps_2019 * 100 AS eps_growth
FROM
(
    SELECT
        vehclass_id,
        MAX(CASE WHEN year = 2019 THEN avg_eps END) AS eps_2019,
        MAX(CASE WHEN year = 2023 THEN avg_eps END) AS eps_2023
    FROM
    (
        SELECT
            vehclass_id,
            YEAR(godate) AS year,
            AVG(netprice_usd / seats) AS avg_eps
        FROM
            `12go`.analytic_test_booking
        WHERE
            YEAR(godate) IN (2019, 2023)
        GROUP BY
            vehclass_id, YEAR(godate)
    ) AS eps_data
    GROUP BY vehclass_id
) AS eps_growth_data;

-- Query to Identify Top 3 Vehicle Classes Contributing to the Highest EPS in 2023:
-- This query identifies the top 3 vehicle classes that contributed the highest EPS in 2023.

SELECT
    vehclass_id,
    AVG(netprice_usd / seats) AS avg_eps
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) = 2023
GROUP BY
    vehclass_id
ORDER BY
    avg_eps DESC
LIMIT 3;


-- Query to Analyze Revenue Contribution by Vehicle Class:
-- This query analyzes the total revenue contribution by each vehicle class across the years 2019 and 2023.


SELECT
    vehclass_id,
    SUM(total_usd) AS total_revenue
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    vehclass_id
ORDER BY
    total_revenue DESC;



-- Query to Calculate Seat Usage Efficiency (EPS per Seat) by Vehicle Class:
-- This query calculates the seat usage efficiency by vehicle class, which is defined as EPS per seat.

SELECT
    vehclass_id,
    AVG(netprice_usd / seats) AS eps_per_seat
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    vehclass_id;