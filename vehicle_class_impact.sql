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
