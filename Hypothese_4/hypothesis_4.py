import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from matplotlib.backends.backend_pdf import PdfPages

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
    cust_id,
    from_country_id AS dep_country,
    to_country_id AS arr_country,
    user_agent,
    website_language AS website_lang,
    class_name
FROM
    `12go`.analytic_test_booking
WHERE
    YEAR(godate) IN (2019, 2023)
"""

# Execute the query and save the data into a DataFrame
df = pd.read_sql(query, engine)

# Save all figures to a PDF
with PdfPages('booking_insights.pdf') as pdf:
    
    # 1. Top 10 Distribution of Transportation Modes
    plt.figure(figsize=(10, 6))
    top10_modes = df['class_name'].value_counts().nlargest(10)
    top10_modes.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Distribution of Transportation Modes')
    plt.xlabel('Transport Mode')
    plt.ylabel('Number of Bookings')
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 2. Top 10 Geographic Analysis of Bookings
    plt.figure(figsize=(14, 8))
    top10_dep_countries = df['dep_country'].value_counts().nlargest(10)
    sns.heatmap(top10_dep_countries.to_frame().T, cmap='Blues', annot=True, fmt='d')
    plt.title('Top 10 Geographic Analysis of Bookings by Departure Country')
    pdf.savefig()
    plt.close()

    # 3. Top 10 Revenue by Transportation Mode (by country)
    plt.figure(figsize=(10, 6))
    top10_countries_by_revenue = df.groupby('dep_country')['netprice_usd'].sum().nlargest(10)
    top10_transport_mode = df[df['dep_country'].isin(top10_countries_by_revenue.index)]
    top10_transport_mode.groupby('class_name')['netprice_usd'].sum().plot(kind='bar', color='orange')
    plt.title('Top 10 Revenue by Transportation Mode (Top Countries)')
    plt.xlabel('Transport Mode')
    plt.ylabel('Total Revenue (USD)')
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 4. Cancellation and Refund Rates
    df['status'] = df['refund_usd'].apply(lambda x: 'Refunded' if x > 0 else 'Confirmed')
    status_counts = df.groupby(['class_name', 'status']).size().unstack().fillna(0)
    status_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['green', 'red'])
    plt.title('Cancellation and Refund Rates by Transport Mode')
    plt.xlabel('Transport Mode')
    plt.ylabel('Number of Bookings')
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 5. Booking Patterns Over Time
    df['godate'] = pd.to_datetime(df['year'], format='%Y')
    monthly_bookings = df.set_index('godate').resample('M').size()
    monthly_bookings.plot(kind='line', figsize=(10, 6))
    plt.title('Booking Patterns Over Time')
    plt.xlabel('Time (Monthly)')
    plt.ylabel('Number of Bookings')
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 6. Top 10 Customer Language Preferences and Comparison between 2019 and 2023
    plt.figure(figsize=(10, 6))
    top10_languages = df['website_lang'].value_counts().nlargest(10)
    top10_languages.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title('Top 10 Customer Language Preferences')
    plt.ylabel('')
    pdf.savefig()
    plt.close()

    plt.figure(figsize=(12, 6))
    lang_2019 = df[df['year'] == 2019]['website_lang'].value_counts().nlargest(10)
    lang_2023 = df[df['year'] == 2023]['website_lang'].value_counts().nlargest(10)
    plt.bar(lang_2019.index, lang_2019.values, alpha=0.7, label='2019', color='blue')
    plt.bar(lang_2023.index, lang_2023.values, alpha=0.7, label='2023', color='orange')
    plt.title('Top 10 Language Preferences: 2019 vs 2023')
    plt.xlabel('Website Language')
    plt.ylabel('Number of Bookings')
    plt.legend()
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 7. Top 10 Revenue by Country of Origin
    plt.figure(figsize=(10, 6))
    df.groupby('dep_country')['netprice_usd'].sum().nlargest(10).plot(kind='bar', color='purple')
    plt.title('Top 10 Revenue by Country of Origin')
    plt.xlabel('Country')
    plt.ylabel('Total Revenue (USD)')
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 8. Influence of Top 5 User Agents on Booking Success
    plt.figure(figsize=(10, 6))
    top5_user_agents = df['user_agent'].value_counts().nlargest(5).index
    user_agent_success = df[df['user_agent'].isin(top5_user_agents)].groupby(['user_agent', 'status']).size().unstack().fillna(0)
    user_agent_success.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'orange'])
    plt.title('Influence of Top 5 User Agents on Booking Success')
    plt.xlabel('User Agent')
    plt.ylabel('Number of Bookings')
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 9. Impact of Trip Duration on Revenue
    plt.figure(figsize=(10, 6))
    plt.scatter(df['trip_duration_minutes'], df['netprice_usd'], color='red')
    plt.title('Impact of Trip Duration on Revenue')
    plt.xlabel('Trip Duration (Minutes)')
    plt.ylabel('Revenue (USD)')
    plt.grid(True)
    pdf.savefig()
    plt.close()

    # 10. Refund Amount Analysis
    plt.figure(figsize=(10, 6))
    sns.histplot(df['refund_usd'].dropna(), bins=20, color='cyan', kde=True)
    plt.title('Refund Amount Analysis')
    plt.xlabel('Refund Amount (USD)')
    plt.ylabel('Frequency')
    plt.grid(True)
    pdf.savefig()
    plt.close()

print("All charts have been saved to 'booking_insights.pdf'.")
