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
