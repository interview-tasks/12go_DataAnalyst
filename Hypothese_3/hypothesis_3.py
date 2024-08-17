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

# Query to fetch data for 2019 and 2023
query = """
SELECT
    YEAR(godate) AS year,
    vehclass_id,
    class_name,
    SUM(total_usd) AS total_revenue,
    COUNT(*) AS total_seats,
    SUM(total_usd) / COUNT(*) AS eps
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
GROUP BY
    year, vehclass_id, class_name
ORDER BY
    year, total_revenue DESC
LIMIT 10;
"""

# Execute the query and save the data into a DataFrame
df = pd.read_sql(query, engine)

# Separate the data for 2019 and 2023
df_2019 = df[df['year'] == 2019]
df_2023 = df[df['year'] == 2023]

# Merge the dataframes on vehclass_id to compare
df_comparison = pd.merge(df_2019, df_2023, on='vehclass_id', suffixes=('_2019', '_2023'))

# Print the comparison dataframe
print(df_comparison[['vehclass_id', 'class_name_2019', 'total_revenue_2019', 'eps_2019', 'total_revenue_2023', 'eps_2023']])

# Plot the EPS comparison between 2019 and 2023
plt.figure(figsize=(10, 6))
plt.barh(df_comparison['class_name_2019'], df_comparison['eps_2019'], color='blue', alpha=0.6, label='2019')
plt.barh(df_comparison['class_name_2019'], df_comparison['eps_2023'], color='green', alpha=0.6, label='2023')
plt.xlabel('Earn Per Seat (EPS)')
plt.title('EPS Comparison for Top 10 Vehicle Classes (2019 vs 2023)')
plt.legend()
plt.show()
