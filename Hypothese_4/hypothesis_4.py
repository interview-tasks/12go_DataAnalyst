import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection details from environment variables
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Create the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# Query to fetch the relevant data
query = """
SELECT
    operator_id,
    vehclass_id,
    netprice_usd,
    seats,
    netprice_usd / seats AS eps,
    refund_usd,
    total_usd,
    trip_duration_minutes,
    YEAR(godate) AS year,
    cust_id
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
"""

# Execute the query and save the data into a DataFrame
df = pd.read_sql(query, engine)

# Group by operator and year for analysis
grouped = df.groupby(['operator_id', 'year']).agg({
    'eps': 'mean',
    'netprice_usd': 'sum',
    'seats': 'sum',
    'refund_usd': 'sum',
    'total_usd': 'sum',
    'trip_duration_minutes': 'mean',
    'cust_id': 'count'  # Assuming each customer ID is unique for bookings, count customers as a proxy for bookings
}).reset_index()

# Insights and Plots

# 1. EPS by Operator for 2019 vs 2023
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.plot(subset['operator_id'], subset['eps'], marker='o', label=f'EPS {year}')
plt.title('EPS by Operator for 2019 vs 2023')
plt.xlabel('Operator ID')
plt.ylabel('Average EPS')
plt.legend()
plt.grid(True)
plt.show()

# 2. Total Net Revenue by Operator
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.bar(subset['operator_id'], subset['netprice_usd'], alpha=0.6, label=f'Total Net Revenue {year}')
plt.title('Total Net Revenue by Operator for 2019 vs 2023')
plt.xlabel('Operator ID')
plt.ylabel('Total Net Revenue (USD)')
plt.legend()
plt.grid(True)
plt.show()

# 3. Total Seats by Operator for 2019 vs 2023
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.bar(subset['operator_id'], subset['seats'], alpha=0.6, label=f'Total Seats {year}')
plt.title('Total Seats by Operator for 2019 vs 2023')
plt.xlabel('Operator ID')
plt.ylabel('Total Seats')
plt.legend()
plt.grid(True)
plt.show()

# 4. Refund Impact on Net Revenue by Operator
grouped['net_revenue_after_refund'] = grouped['netprice_usd'] - grouped['refund_usd']
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.bar(subset['operator_id'], subset['net_revenue_after_refund'], alpha=0.6, label=f'Net Revenue After Refund {year}')
plt.title('Net Revenue After Refund by Operator for 2019 vs 2023')
plt.xlabel('Operator ID')
plt.ylabel('Net Revenue After Refund (USD)')
plt.legend()
plt.grid(True)
plt.show()

# 5. EPS Growth Comparison by Operator between 2019 and 2023
grouped['eps_growth'] = grouped.groupby('operator_id')['eps'].pct_change().fillna(0)
eps_growth = grouped[grouped['year'] == 2023][['operator_id', 'eps_growth']]
plt.figure(figsize=(14, 8))
plt.bar(eps_growth['operator_id'], eps_growth['eps_growth'])
plt.title('EPS Growth by Operator from 2019 to 2023')
plt.xlabel('Operator ID')
plt.ylabel('EPS Growth (%)')
plt.grid(True)
plt.show()

# 6. Average Trip Duration by Operator
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.plot(subset['operator_id'], subset['trip_duration_minutes'], marker='o', label=f'Average Trip Duration {year}')
plt.title('Average Trip Duration by Operator for 2019 vs 2023')
plt.xlabel('Operator ID')
plt.ylabel('Average Trip Duration (Minutes)')
plt.legend()
plt.grid(True)
plt.show()

# 7. Seat Usage Efficiency (EPS per Seat) by Operator
seat_efficiency = df.groupby('operator_id').apply(lambda x: (x['netprice_usd'] / x['seats']).mean()).reset_index(name='eps_per_seat')
plt.figure(figsize=(14, 8))
plt.bar(seat_efficiency['operator_id'], seat_efficiency['eps_per_seat'])
plt.title('Seat Usage Efficiency (EPS per Seat) by Operator')
plt.xlabel('Operator ID')
plt.ylabel('EPS per Seat (USD)')
plt.grid(True)
plt.show()

# 8. Top 3 Operators Contributing to the Highest EPS in 2023
top_eps_operators = grouped[grouped['year'] == 2023].nlargest(3, 'eps')
plt.figure(figsize=(14, 8))
plt.bar(top_eps_operators['operator_id'], top_eps_operators['eps'], color='green')
plt.title('Top 3 Operators Contributing to the Highest EPS in 2023')
plt.xlabel('Operator ID')
plt.ylabel('Average EPS')
plt.grid(True)
plt.show()

# 9. Distribution of EPS by Operator in 2023
plt.figure(figsize=(14, 8))
plt.hist(df[df['year'] == 2023]['eps'], bins=20, color='skyblue')
plt.title('Distribution of EPS by Operator in 2023')
plt.xlabel('EPS')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# 10. Customer Booking Volume by Operator
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.bar(subset['operator_id'], subset['cust_id'], alpha=0.6, label=f'Customer Bookings {year}')
plt.title('Customer Booking Volume by Operator for 2019 vs 2023')
plt.xlabel('Operator ID')
plt.ylabel('Total Bookings')
plt.legend()
plt.grid(True)
plt.show()

# Summary of insights
insights = [
    "1. EPS by operator shows variability across different operators, with noticeable changes between 2019 and 2023.",
    "2. Total net revenue by operator highlights which operators are driving revenue.",
    "3. Total seats by operator for 2019 vs 2023 shows which operators have maintained or increased capacity.",
    "4. Refunds significantly impact net revenue for certain operators, highlighting areas for improvement.",
    "5. EPS growth from 2019 to 2023 shows certain operators have improved while others may have declined.",
    "6. Average trip duration by operator indicates the efficiency and preferences of different operators.",
    "7. Seat usage efficiency (EPS per seat) varies by operator, indicating potential for optimizing seat allocation.",
    "8. The top 3 operators for EPS in 2023 provide a benchmark for other operators.",
    "9. Distribution of EPS by operator in 2023 helps understand how EPS is spread across operators.",
    "10. Customer booking volume by operator gives insight into the popularity and market share of different operators."
]

# Print insights
for i, insight in enumerate(insights, 1):
    print(insight)
