-- 1. Identify Top Routes by EPS in 2019
SELECT
    from_station_name,
    to_station_name,
    vehclass_id,
    class_name,
    SUM(seats) AS total_seats,
    SUM(netprice_usd) AS total_netprice,
    SUM(total_usd) AS total_revenue,
    (SUM(total_usd) - SUM(netprice_usd)) / SUM(seats) AS EPS,
    YEAR(paidon) AS year
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(paidon) = 2019
GROUP BY
    from_station_name, to_station_name, vehclass_id, class_name
ORDER BY
    EPS DESC
LIMIT 10;




-- 2. Compare the EPS of the Top 2019 Routes in 2023

SELECT
    from_station_name,
    to_station_name,
    vehclass_id,
    class_name,
    SUM(seats) AS total_seats,
    SUM(netprice_usd) AS total_netprice,
    SUM(total_usd) AS total_revenue,
    (SUM(total_usd) - SUM(netprice_usd)) / SUM(seats) AS EPS,
    YEAR(paidon) AS year
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(paidon) = 2023 AND
    (from_station_name, to_station_name, vehclass_id, class_name) IN (
        SELECT
            from_station_name,
            to_station_name,
            vehclass_id,
            class_name
        FROM
            `12go`.analytic_test_booking
        WHERE
            YEAR(paidon) = 2019
        GROUP BY
            from_station_name, to_station_name, vehclass_id, class_name
        ORDER BY
            SUM(total_usd - netprice_usd) / SUM(seats) DESC
        -- LIMIT 10
    )
GROUP BY
    from_station_name, to_station_name, vehclass_id, class_name, year
ORDER BY
    EPS DESC;



-- 3. Calculate EPS Decline or Increase Between 2019 and 2023

SELECT
    t2019.from_station_name,
    t2019.to_station_name,
    t2019.vehclass_id,
    t2019.class_name,
    t2019.EPS AS EPS_2019,
    t2023.EPS AS EPS_2023,
    (t2023.EPS - t2019.EPS) / t2019.EPS * 100 AS EPS_change_percentage
FROM
    (
        SELECT
            from_station_name,
            to_station_name,
            vehclass_id,
            class_name,
            (SUM(total_usd) - SUM(netprice_usd)) / SUM(seats) AS EPS
        FROM
            `12go`.analytic_test_booking
        WHERE
            YEAR(paidon) = 2019
        GROUP BY
            from_station_name, to_station_name, vehclass_id, class_name
        ORDER BY
            EPS DESC
        LIMIT 10
    ) AS t2019
LEFT JOIN
    (
        SELECT
            from_station_name,
            to_station_name,
            vehclass_id,
            class_name,
            (SUM(total_usd) - SUM(netprice_usd)) / SUM(seats) AS EPS
        FROM
            `12go`.analytic_test_booking
        WHERE
            YEAR(paidon) = 2023
        GROUP BY
            from_station_name, to_station_name, vehclass_id, class_name
    ) AS t2023
ON
    t2019.from_station_name = t2023.from_station_name AND
    t2019.to_station_name = t2023.to_station_name AND
    t2019.vehclass_id = t2023.vehclass_id AND
    t2019.class_name = t2023.class_name
ORDER BY
    EPS_change_percentage ASC;



-- 4. Analyze the Volume of Seats Sold on Declining Routes

SELECT
    from_station_name,
    to_station_name,
    vehclass_id,
    class_name,
    SUM(CASE WHEN YEAR(paidon) = 2019 THEN seats ELSE 0 END) AS seats_2019,
    SUM(CASE WHEN YEAR(paidon) = 2023 THEN seats ELSE 0 END) AS seats_2023,
    SUM(CASE WHEN YEAR(paidon) = 2023 THEN seats ELSE 0 END) - SUM(CASE WHEN YEAR(paidon) = 2019 THEN seats ELSE 0 END) AS seats_change
FROM
    `12go`.analytic_test_booking
WHERE
    (from_station_name, to_station_name, vehclass_id, class_name) IN (
        SELECT
            from_station_name,
            to_station_name,
            vehclass_id,
            class_name
        FROM
            `12go`.analytic_test_booking
        WHERE
            YEAR(paidon) = 2019
        GROUP BY
            from_station_name, to_station_name, vehclass_id, class_name
        ORDER BY
            SUM(total_usd - netprice_usd) / SUM(seats) DESC
        -- LIMIT 10
    )
GROUP BY
    from_station_name, to_station_name, vehclass_id, class_name
ORDER BY
    seats_change ASC;
