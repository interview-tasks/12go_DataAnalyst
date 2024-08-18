import matplotlib.pyplot as plt
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

# Function to fetch data from the database
def fetch_data(query):
    return pd.read_sql(query, engine)

# Function to create comparison bar charts with proper y-axis scaling
def create_comparison_chart(df_2019, df_2023, column, title, xlabel, ylabel):
    # Combine and rank data for consistent comparison
    combined = pd.concat([df_2019, df_2023]).groupby(column).sum().reset_index()
    top_combined = combined.nlargest(5, 'num_bookings')
    
    # Reindex original dataframes to only include top items
    df_2019_top = df_2019[df_2019[column].isin(top_combined[column])]
    df_2023_top = df_2023[df_2023[column].isin(top_combined[column])]
    
    # Prepare data for plotting
    comparison = pd.DataFrame({
        '2019': df_2019_top.groupby(column)['num_bookings'].sum(),
        '2023': df_2023_top.groupby(column)['num_bookings'].sum()
    }).fillna(0)  # Fill NaN with 0 for better comparison
    
    ax = comparison.plot(kind='bar', figsize=(10, 6))
    ax.set_ylim(0, comparison.max().max() * 1.1)  # Set y-axis limits from 0 to slightly above the max value
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    return ax.figure

# Initialize the PDF
pdf_path = 'comparison_charts.pdf'
pdf = PdfPages(pdf_path)

# 1. Average Trip Duration in 2019 and 2023
query_avg_trip_duration = """
SELECT 
    YEAR(godate) as year, 
    AVG(trip_duration_minutes) as avg_duration 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    year
"""
df_avg_trip_duration = fetch_data(query_avg_trip_duration)
ax = df_avg_trip_duration.plot(kind='bar', x='year', y='avg_duration', color='lightblue', figsize=(10, 6))
ax.set_ylim(0, df_avg_trip_duration['avg_duration'].max() * 1.1)  # Adjust y-axis limit
plt.title('Average Trip Duration in 2019 and 2023')
plt.xlabel('Year')
plt.ylabel('Average Trip Duration (Minutes)')
plt.grid(True)
pdf.savefig(ax.figure)
plt.show()

# 2. Top 5 Distribution of Transportation Modes
query_transport_modes = """
SELECT 
    class_name, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    class_name, year
"""
df_transport_modes = fetch_data(query_transport_modes)

# Split data by year
df_transport_modes_2019 = df_transport_modes[df_transport_modes['year'] == 2019]
df_transport_modes_2023 = df_transport_modes[df_transport_modes['year'] == 2023]

fig = create_comparison_chart(df_transport_modes_2019, 
                        df_transport_modes_2023, 
                        'class_name', 
                        'Top 5 Distribution of Transportation Modes', 
                        'Transport Mode', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 3. Top 5 Revenue by Country of Origin
query_revenue_by_country = """
SELECT 
    from_country_id, 
    SUM(netprice_usd) as total_revenue, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    from_country_id, year
"""
df_revenue_by_country = fetch_data(query_revenue_by_country)

# Split data by year
df_revenue_by_country_2019 = df_revenue_by_country[df_revenue_by_country['year'] == 2019]
df_revenue_by_country_2023 = df_revenue_by_country[df_revenue_by_country['year'] == 2023]

# Combine and rank data for consistent comparison
combined_revenue = pd.concat([df_revenue_by_country_2019, df_revenue_by_country_2023]).groupby('from_country_id').sum()
top_combined_revenue = combined_revenue.nlargest(5, 'total_revenue')

# Reindex original dataframes to only include top items
df_revenue_by_country_2019_top = df_revenue_by_country_2019[df_revenue_by_country_2019['from_country_id'].isin(top_combined_revenue.index)]
df_revenue_by_country_2023_top = df_revenue_by_country_2023[df_revenue_by_country_2023['from_country_id'].isin(top_combined_revenue.index)]

# Prepare data for plotting
comparison_revenue = pd.DataFrame({
    '2019': df_revenue_by_country_2019_top.groupby('from_country_id')['total_revenue'].sum(),
    '2023': df_revenue_by_country_2023_top.groupby('from_country_id')['total_revenue'].sum()
}).fillna(0)  # Fill NaN with 0 for better comparison

ax = comparison_revenue.plot(kind='bar', figsize=(10, 6))
ax.set_ylim(0, comparison_revenue.max().max() * 1.1)  # Set y-axis limits from 0 to slightly above the max value
plt.title('Top 5 Revenue by Country of Origin in 2019 and 2023')
plt.xlabel('Country')
plt.ylabel('Total Revenue (USD)')
plt.grid(True)
pdf.savefig(ax.figure)
plt.show()

# 4. Top 5 Language Preferences Comparison
query_language_prefs = """
SELECT 
    website_language, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    website_language, year
"""
df_language_prefs = fetch_data(query_language_prefs)

# Split data by year
df_language_prefs_2019 = df_language_prefs[df_language_prefs['year'] == 2019]
df_language_prefs_2023 = df_language_prefs[df_language_prefs['year'] == 2023]

fig = create_comparison_chart(df_language_prefs_2019, 
                        df_language_prefs_2023, 
                        'website_language', 
                        'Top 5 Language Preferences Comparison', 
                        'Language', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 5. Top 5 User Agents Comparison
query_user_agents = """
SELECT 
    user_agent, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    user_agent, year
"""
df_user_agents = fetch_data(query_user_agents)

# Split data by year
df_user_agents_2019 = df_user_agents[df_user_agents['year'] == 2019]
df_user_agents_2023 = df_user_agents[df_user_agents['year'] == 2023]

fig = create_comparison_chart(df_user_agents_2019, 
                        df_user_agents_2023, 
                        'user_agent', 
                        'Top 5 User Agents in 2019 and 2023', 
                        'User Agent', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 6. Top 5 Countries Comparison
query_top_countries = """
SELECT 
    from_country_id, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    from_country_id, year
"""
df_top_countries = fetch_data(query_top_countries)

# Split data by year
df_top_countries_2019 = df_top_countries[df_top_countries['year'] == 2019]
df_top_countries_2023 = df_top_countries[df_top_countries['year'] == 2023]

fig = create_comparison_chart(df_top_countries_2019, 
                        df_top_countries_2023, 
                        'from_country_id', 
                        'Top 5 Countries in 2019 and 2023', 
                        'Country', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 7. Top 5 From Station Name Comparison
query_from_station_names = """
SELECT 
    from_station_name, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    from_station_name, year
"""
df_from_station_names = fetch_data(query_from_station_names)

# Split data by year
df_from_station_names_2019 = df_from_station_names[df_from_station_names['year'] == 2019]
df_from_station_names_2023 = df_from_station_names[df_from_station_names['year'] == 2023]

fig = create_comparison_chart(df_from_station_names_2019, 
                        df_from_station_names_2023, 
                        'from_station_name', 
                        'Top 5 From Station Names in 2019 and 2023', 
                        'Station Name', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 8. Top 5 To Station Name Comparison
query_to_station_names = """
SELECT 
    to_station_name, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    to_station_name, year
"""
df_to_station_names = fetch_data(query_to_station_names)

# Split data by year
df_to_station_names_2019 = df_to_station_names[df_to_station_names['year'] == 2019]
df_to_station_names_2023 = df_to_station_names[df_to_station_names['year'] == 2023]

fig = create_comparison_chart(df_to_station_names_2019, 
                        df_to_station_names_2023, 
                        'to_station_name', 
                        'Top 5 To Station Names in 2019 and 2023', 
                        'Station Name', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 9. Average Monthly Orders Count for 2019 and 2023
query_monthly_orders = """
SELECT 
    MONTH(godate) as month, 
    COUNT(*) as num_orders, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    month, year
"""
df_monthly_orders = fetch_data(query_monthly_orders)

# Pivot the data for better visualization
ax = df_monthly_orders.pivot(index='month', columns='year', values='num_orders').plot(kind='bar', figsize=(10, 6))
ax.set_ylim(0, df_monthly_orders['num_orders'].max() * 1.1)  # Adjust y-axis limit
plt.title('Average Monthly Orders Count in 2019 and 2023')
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.grid(True)
pdf.savefig(ax.figure)
plt.show()

# 10. Average Monthly EPS for 2019 and 2023
query_monthly_eps = """
SELECT 
    MONTH(godate) as month, 
    AVG(netprice_usd / seats) as avg_eps, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    month, year
"""
df_monthly_eps = fetch_data(query_monthly_eps)

# Pivot the data for better visualization
ax = df_monthly_eps.pivot(index='month', columns='year', values='avg_eps').plot(kind='bar', figsize=(10, 6))
ax.set_ylim(0, df_monthly_eps['avg_eps'].max() * 1.1)  # Adjust y-axis limit
plt.title('Average Monthly EPS in 2019 and 2023')
plt.xlabel('Month')
plt.ylabel('Average EPS')
plt.grid(True)
pdf.savefig(ax.figure)
plt.show()

# 11. Top 5 Created By Role ID Comparison
query_createdby_role = """
SELECT 
    createdby_role_id, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    createdby_role_id, year
"""
df_createdby_role = fetch_data(query_createdby_role)

# Split data by year
df_createdby_role_2019 = df_createdby_role[df_createdby_role['year'] == 2019]
df_createdby_role_2023 = df_createdby_role[df_createdby_role['year'] == 2023]

fig = create_comparison_chart(df_createdby_role_2019, 
                        df_createdby_role_2023, 
                        'createdby_role_id', 
                        'Top 5 Created By Role ID in 2019 and 2023', 
                        'Role ID', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 12. Top 5 Channels Comparison
query_channel = """
SELECT 
    channel, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    channel, year
"""
df_channel = fetch_data(query_channel)

# Split data by year
df_channel_2019 = df_channel[df_channel['year'] == 2019]
df_channel_2023 = df_channel[df_channel['year'] == 2023]

fig = create_comparison_chart(df_channel_2019, 
                        df_channel_2023, 
                        'channel', 
                        'Top 5 Channels in 2019 and 2023', 
                        'Channel', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 13. Top 5 User Origin Country Comparison
query_user_origin_country = """
SELECT 
    user_origin_country_id, 
    COUNT(*) as num_bookings, 
    YEAR(godate) as year 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    user_origin_country_id, year
"""
df_user_origin_country = fetch_data(query_user_origin_country)

# Split data by year
df_user_origin_country_2019 = df_user_origin_country[df_user_origin_country['year'] == 2019]
df_user_origin_country_2023 = df_user_origin_country[df_user_origin_country['year'] == 2023]

fig = create_comparison_chart(df_user_origin_country_2019, 
                        df_user_origin_country_2023, 
                        'user_origin_country_id', 
                        'Top 5 User Origin Countries in 2019 and 2023', 
                        'Country', 'Number of Bookings')
pdf.savefig(fig)
plt.show()

# 14. Total Order Count Comparison between 2019 and 2023
query_order_count = """
SELECT 
    YEAR(godate) as year, 
    COUNT(*) as total_orders 
FROM 
    `12go`.analytic_test_booking 
WHERE 
    YEAR(godate) IN (2019, 2023)
GROUP BY 
    year
"""
df_order_count = fetch_data(query_order_count)
ax = df_order_count.plot(kind='bar', x='year', y='total_orders', color='purple', figsize=(10, 6))
ax.set_ylim(0, df_order_count['total_orders'].max() * 1.1)  # Adjust y-axis limit
plt.title('Total Order Count Comparison between 2019 and 2023')
plt.xlabel('Year')
plt.ylabel('Total Orders')
plt.grid(True)
pdf.savefig(ax.figure)
plt.show()

# Close the PDF file
pdf.close()

print(f"All charts have been generated and saved in {pdf_path}.")
