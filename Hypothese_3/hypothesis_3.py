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
"""

# Execute the query and save the data into a DataFrame
df = pd.read_sql(query, engine)

# Group by vehicle class and year for analysis
grouped = df.groupby(['vehclass_id', 'year']).agg({
    'eps': 'mean',
    'netprice_usd': 'sum',
    'seats': 'sum',
    'refund_usd': 'sum',
    'total_usd': 'sum',
    'trip_duration_minutes': 'mean'
}).reset_index()

# Insights and Plots

# 1. EPS by Vehicle Class for 2019 vs 2023
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.plot(subset['vehclass_id'], subset['eps'], marker='o', label=f'EPS {year}')
plt.title('EPS by Vehicle Class for 2019 vs 2023')
plt.xlabel('Vehicle Class ID')
plt.ylabel('Average EPS')
plt.legend()
plt.grid(True)
plt.show()

# 2. Total Net Revenue by Vehicle Class
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.bar(subset['vehclass_id'], subset['netprice_usd'], alpha=0.6, label=f'Total Net Revenue {year}')
plt.title('Total Net Revenue by Vehicle Class for 2019 vs 2023')
plt.xlabel('Vehicle Class ID')
plt.ylabel('Total Net Revenue (USD)')
plt.legend()
plt.grid(True)
plt.show()

# 3. Seat Occupancy Comparison between 2019 and 2023
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.bar(subset['vehclass_id'], subset['seats'], alpha=0.6, label=f'Seats {year}')
plt.title('Seat Occupancy by Vehicle Class for 2019 vs 2023')
plt.xlabel('Vehicle Class ID')
plt.ylabel('Total Seats')
plt.legend()
plt.grid(True)
plt.show()

# 4. Refund Impact on Net Revenue by Vehicle Class
grouped['net_revenue_after_refund'] = grouped['netprice_usd'] - grouped['refund_usd']
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.bar(subset['vehclass_id'], subset['net_revenue_after_refund'], alpha=0.6, label=f'Net Revenue After Refund {year}')
plt.title('Net Revenue After Refund by Vehicle Class for 2019 vs 2023')
plt.xlabel('Vehicle Class ID')
plt.ylabel('Net Revenue After Refund (USD)')
plt.legend()
plt.grid(True)
plt.show()

# 5. EPS Growth Comparison between 2019 and 2023
grouped['eps_growth'] = grouped.groupby('vehclass_id')['eps'].pct_change().fillna(0)
eps_growth = grouped[grouped['year'] == 2023][['vehclass_id', 'eps_growth']]
plt.figure(figsize=(14, 8))
plt.bar(eps_growth['vehclass_id'], eps_growth['eps_growth'])
plt.title('EPS Growth by Vehicle Class from 2019 to 2023')
plt.xlabel('Vehicle Class ID')
plt.ylabel('EPS Growth (%)')
plt.grid(True)
plt.show()

# 6. Average Trip Duration by Vehicle Class
plt.figure(figsize=(14, 8))
for year in [2019, 2023]:
    subset = grouped[grouped['year'] == year]
    plt.plot(subset['vehclass_id'], subset['trip_duration_minutes'], marker='o', label=f'Average Trip Duration {year}')
plt.title('Average Trip Duration by Vehicle Class for 2019 vs 2023')
plt.xlabel('Vehicle Class ID')
plt.ylabel('Average Trip Duration (Minutes)')
plt.legend()
plt.grid(True)
plt.show()

# 7. Seat Usage Efficiency (EPS per Seat) by Vehicle Class
seat_efficiency = df.groupby('vehclass_id').apply(lambda x: (x['netprice_usd'] / x['seats']).mean()).reset_index(name='eps_per_seat')
plt.figure(figsize=(14, 8))
plt.bar(seat_efficiency['vehclass_id'], seat_efficiency['eps_per_seat'])
plt.title('Seat Usage Efficiency (EPS per Seat) by Vehicle Class')
plt.xlabel('Vehicle Class ID')
plt.ylabel('EPS per Seat (USD)')
plt.grid(True)
plt.show()

# 8. Top 3 Vehicle Classes Contributing to the Highest EPS in 2023
top_eps_classes = grouped[grouped['year'] == 2023].nlargest(3, 'eps')
plt.figure(figsize=(14, 8))
plt.bar(top_eps_classes['vehclass_id'], top_eps_classes['eps'], color='green')
plt.title('Top 3 Vehicle Classes Contributing to the Highest EPS in 2023')
plt.xlabel('Vehicle Class ID')
plt.ylabel('Average EPS')
plt.grid(True)
plt.show()

# 9. Distribution of EPS by Vehicle Class in 2023
plt.figure(figsize=(14, 8))
plt.hist(df[df['year'] == 2023]['eps'], bins=20, color='skyblue')
plt.title('Distribution of EPS by Vehicle Class in 2023')
plt.xlabel('EPS')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# 10. Revenue Contribution by Vehicle Class
revenue_contribution = grouped.groupby('vehclass_id')['total_usd'].sum().reset_index()
plt.figure(figsize=(14, 8))
plt.bar(revenue_contribution['vehclass_id'], revenue_contribution['total_usd'], color='purple')
plt.title('Revenue Contribution by Vehicle Class')
plt.xlabel('Vehicle Class ID')
plt.ylabel('Total Revenue (USD)')
plt.grid(True)
plt.show()

# Summary of insights
insights = [
    "1. EPS by vehicle class shows variability across different classes, with noticeable changes between 2019 and 2023.",
    "2. Total net revenue by vehicle class highlights which classes are driving revenue.",
    "3. Seat occupancy has varied between 2019 and 2023, affecting overall revenue.",
    "4. Refunds significantly impact net revenue in some vehicle classes.",
    "5. EPS growth from 2019 to 2023 shows certain classes have improved while others may have declined.",
    "6. Average trip duration by vehicle class indicates which classes might be preferred for longer or shorter trips.",
    "7. Seat usage efficiency (EPS per seat) varies, indicating potential for optimizing seat allocation.",
    "8. The top 3 vehicle classes for EPS in 2023 provide a benchmark for other classes.",
    "9. Distribution of EPS by vehicle class in 2023 helps understand how EPS is spread across classes.",
    "10. Revenue contribution by vehicle class gives insight into which classes are the most profitable."
]

# Print insights
for i, insight in enumerate(insights, 1):
    print(insight)
