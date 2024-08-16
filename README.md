## README.md

### Introduction
This repository contains SQL scripts for analyzing the Earn Per Seat (EPS) metrics from transportation data. The analysis is based on various hypotheses aimed at identifying trends and opportunities for improvement.

### Hypotheses Based on the Analysis

#### Hypothesis 1: Station-Specific Decline
**Observation**: If certain `from_id` or `to_id` stations show a greater decline in EPS, it may indicate decreased demand or increased competition at these stations.

**Recommendation**: Investigate the reasons for decreased demand and consider targeted marketing or adjusting service offerings at these stations.

**SQL Script**: `station_specific_decline.sql`

#### Hypothesis 2: Operator Performance
**Observation**: If certain `operator_ids` are underperforming, this could indicate operational inefficiencies or issues with customer satisfaction.

**Recommendation**: Work with underperforming operators to identify areas for improvement and enhance service quality.

**SQL Script**: `operator_performance.sql`

#### Hypothesis 3: Impact of Vehicle Class
**Observation**: If certain vehicle classes, identified by `class_name`, are contributing to the decline in EPS, it may be due to pricing strategies or changes in customer preferences.

**Recommendation**: Consider adjusting pricing, adding value-added services, or promoting higher-margin vehicle classes.

**SQL Script**: `vehicle_class_impact.sql`

#### Hypothesis 4: Country-Specific Trends
**Observation**: If `from_country_id` shows significant EPS differences, it might reflect changes in demand or competition in specific countries.

**Recommendation**: Tailor marketing efforts and pricing strategies to reflect regional differences in demand.

**SQL Script**: `country_specific_trends.sql`

### How to Run the Scripts

1. Ensure that you have access to the `12go` database.
2. Use a MySQL client or an IDE like Visual Studio Code with the SQLTools extension to run the provided SQL scripts.
3. Each script can be run independently to analyze specific aspects of the data as outlined in the hypotheses.

### SQL Scripts

#### 1. Station-Specific Decline

**File**: `station_specific_decline.sql`

```sql
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
```

#### 2. Operator Performance

**File**: `operator_performance.sql`

```sql
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
```

#### 3. Impact of Vehicle Class

**File**: `vehicle_class_impact.sql`

```sql
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
```

#### 4. Country-Specific Trends

**File**: `country_specific_trends.sql`

```sql
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
```

### Conclusion
These scripts will help you analyze the EPS data from various perspectives, such as station-specific trends, operator performance, vehicle class impact, and country-specific trends. The insights derived from these analyses can guide strategic decisions to improve business performance.

---

### Next Steps
- Execute each script to gather insights.
- Interpret the results to understand trends and make data-driven recommendations.
- Adjust business strategies accordingly based on the analysis.
