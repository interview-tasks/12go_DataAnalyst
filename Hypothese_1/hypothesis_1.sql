-- Analyze refund rates by departure station (from_id)
SELECT
    from_id,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) AS refund_count,
    ROUND(SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 4) AS refund_rate
FROM
    `12go`.analytic_test_booking
GROUP BY
    from_id
ORDER BY
    refund_rate DESC;

-- Analyze refund rates by arrival station (to_id)
SELECT
    to_id,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) AS refund_count,
    ROUND(SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 4) AS refund_rate
FROM
    `12go`.analytic_test_booking
GROUP BY
    to_id
ORDER BY
    refund_rate DESC;


-- Analyze refund rates by operator
SELECT
    operator_id,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) AS refund_count,
    ROUND(SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 4) AS refund_rate
FROM
    `12go`.analytic_test_booking
GROUP BY
    operator_id
ORDER BY
    refund_rate DESC;


-- Analyze refund rates by vehicle class
SELECT
    class_name,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) AS refund_count,
    ROUND(SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 4) AS refund_rate
FROM
    `12go`.analytic_test_booking
GROUP BY
    class_name
ORDER BY
    refund_rate DESC;



-- Analyze refund rates by departure country (from_country_id)
SELECT
    from_country_id,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) AS refund_count,
    ROUND(SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 4) AS refund_rate
FROM
    `12go`.analytic_test_booking
GROUP BY
    from_country_id
ORDER BY
    refund_rate DESC;

-- Analyze refund rates by arrival country (to_country_id)
SELECT
    to_country_id,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) AS refund_count,
    ROUND(SUM(CASE WHEN refund_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 4) AS refund_rate
FROM
    `12go`.analytic_test_booking
GROUP BY
    to_country_id
ORDER BY
    refund_rate DESC;
