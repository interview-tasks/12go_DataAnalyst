from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd

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

# Retrieve booking data for 2019 and 2023
query = """
SELECT
    bid,
    paidon,
    seats,
    total_usd
FROM
    analytic_test_booking
WHERE
    paidon BETWEEN '2019-01-01' AND '2019-12-31'
    OR paidon BETWEEN '2023-01-01' AND '2023-12-31'
"""
booking_data = pd.read_sql(query, engine)

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
