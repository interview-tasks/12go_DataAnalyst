SELECT
	bid,
	paidon,
	paygate_code,
	status_id,
	seller_id,
	operator_id,
	class_id,
	class_name,
	from_id,
	from_province_id,
	from_country_id,
	from_station_name,
	to_id,
	to_province_id,
	to_country_id,
	to_station_name,
	seats,
	vehclass_id,
	godate,
	trip_duration_minutes,
	payment_currency,
	cust_id,
	website_language,
	stamp,
	createdby,
	createdby_role_id,
	createdon,
	createdon_date,
	refund_date,
	refund_usd,
	netprice_usd,
	sysfee_usd,
	agfee_usd,
	total_usd,
	sysfee_total_usd,
	agfee_total_usd,
	netprice_total_usd,
	channel,
	user_agent,
	useragent,
	referer,
	landing,
	user_origin_country_id
FROM
	`12go`.analytic_test_booking;



	-- Query for Chart 1: Average Trip Duration in 2019 and 2023
SELECT
    YEAR(godate) AS year,
    AVG(trip_duration_minutes) AS avg_trip_duration
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    YEAR(godate);

-- Query for Chart 2: Top 5 Distribution of Transportation Modes in 2019 and 2023
SELECT
    class_name,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    class_name, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 3: Top 5 Revenue by Country of Origin in 2019 and 2023
SELECT
    from_country_id,
    YEAR(godate) AS year,
    SUM(netprice_usd) AS total_revenue
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    from_country_id, year
ORDER BY
    total_revenue DESC
LIMIT 5;

-- Query for Chart 4: Top 5 Language Preferences Comparison in 2019 and 2023
SELECT
    website_language,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    website_language, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 5: Top 5 User Agents Comparison in 2019 and 2023
SELECT
    user_agent,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    user_agent, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 6: Top 5 Countries Comparison in 2019 and 2023
SELECT
    from_country_id,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    from_country_id, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 7: Top 5 From Station Name Comparison in 2019 and 2023
SELECT
    from_station_name,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    from_station_name, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 8: Top 5 To Station Name Comparison in 2019 and 2023
SELECT
    to_station_name,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    to_station_name, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 9: Average Monthly Orders Count for 2019 and 2023
SELECT
    MONTH(godate) AS month,
    YEAR(godate) AS year,
    COUNT(*) AS order_count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    MONTH(godate), YEAR(godate);

-- Query for Chart 10: Average Monthly EPS for 2019 and 2023
SELECT
    MONTH(godate) AS month,
    YEAR(godate) AS year,
    AVG(netprice_usd / seats) AS avg_eps
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    MONTH(godate), YEAR(godate);

-- Query for Chart 11: Top 5 Created By Role ID Comparison in 2019 and 2023
SELECT
    createdby_role_id,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    createdby_role_id, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 12: Top 5 Channels Comparison in 2019 and 2023
SELECT
    channel,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    channel, year
ORDER BY
    count DESC
LIMIT 5;

-- Query for Chart 13: Top 5 User Origin Country Comparison in 2019 and 2023
SELECT
    user_origin_country_id,
    YEAR(godate) AS year,
    COUNT(*) AS count
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    user_origin_country_id, year
ORDER BY
    count DESC
LIMIT 5;
