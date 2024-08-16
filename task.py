import mysql.connector
import pandas as pd

# Database connection details
db_config = {
    'host': 'hrtest.12go.asia',
    'port': 20062,
    'user': 'hrtest-ro',
    'password': 'q2FTQezFKRmHp',
    'database': '12go'
}

# Connect to the database
connection = mysql.connector.connect(**db_config)

# Retrieve booking data
query = """
SELECT
    bid,
    paidon,
    seats,
    total_usd
FROM
    analytic_test_booking
WHERE
    YEAR(paidon) IN (2019, 2023)
"""
booking_data = pd.read_sql(query, connection)

# Close the connection
connection.close()

# Calculate EPS
booking_data['EPS'] = booking_data['total_usd'] / booking_data['seats']

# Add a year column for easier analysis
booking_data['year'] = pd.to_datetime(booking_data['paidon']).dt.year

# Separate data by year
eps_2019 = booking_data[booking_data['year'] == 2019]
eps_2023 = booking_data[booking_data['year'] == 2023]

# Calculate average EPS for each year
avg_eps_2019 = eps_2019['EPS'].mean()
avg_eps_2023 = eps_2023['EPS'].mean()

# Calculate the percentage change in EPS
eps_change = ((avg_eps_2023 - avg_eps_2019) / avg_eps_2019) * 100

print(f"Average EPS in 2019: {avg_eps_2019}")
print(f"Average EPS in 2023: {avg_eps_2023}")
print(f"Percentage Change in EPS: {eps_change:.2f}%")
