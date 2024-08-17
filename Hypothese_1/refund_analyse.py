import matplotlib.pyplot as plt
from fpdf import FPDF
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

# Query to fetch the data
query = """
SELECT
    IFNULL(orders.order_year, refunds.refund_year) AS year,
    IFNULL(orders.total_orders, 0) AS total_orders,
    IFNULL(refunds.refund_count, 0) AS refund_count,
    IFNULL((refunds.refund_count / NULLIF(orders.total_orders, 0)), 0) AS refund_rate
FROM
    (
        SELECT
            YEAR(paidon) AS order_year,
            COUNT(*) AS total_orders
        FROM
            `12go`.analytic_test_booking
        GROUP BY
            order_year
    ) AS orders
RIGHT JOIN
    (
        SELECT
            YEAR(refund_date) AS refund_year,
            COUNT(*) AS refund_count
        FROM
            `12go`.analytic_test_booking
        WHERE
            refund_date IS NOT NULL
        GROUP BY
            refund_year
    ) AS refunds
ON
    orders.order_year = refunds.refund_year
ORDER BY year;
"""

# Execute the query and save the data into a DataFrame
df = pd.read_sql(query, engine)

# Replace anomalies with descriptive text
def calculate_refund_rate(row):
    if row['total_orders'] == 0:
        if row['refund_count'] > 0:
            return "N/A (No Orders)"
        else:
            return "0.0000"
    elif row['refund_rate'] > 1:
        return "Anomaly"
    else:
        return row['refund_rate']

df['refund_rate'] = df.apply(calculate_refund_rate, axis=1)

# Correct the refund_rate column for string cases before rounding
def safe_round(refund_rate):
    try:
        return round(float(refund_rate), 4)
    except (ValueError, TypeError):
        return refund_rate

# Apply the safe rounding function
df['refund_rate'] = df['refund_rate'].apply(safe_round)

# Convert refund_rate to float for visualization (ignore anomalies for plotting)
df['refund_rate_float'] = pd.to_numeric(df['refund_rate'], errors='coerce')

# Generate refund statistics
total_orders = df['total_orders'].sum()
total_refunds = df['refund_count'].sum()
refund_percentage = (total_refunds / total_orders) * 100 if total_orders > 0 else 0

# Round numbers for the statistics
total_orders_rounded = f"{total_orders:,}"
total_refunds_rounded = f"{total_refunds:,}"
refund_percentage_rounded = round(refund_percentage, 2)

# Calculate yearly refund statistics
yearly_refund_stats = []
for _, row in df.iterrows():
    year = int(row['year'])
    total_orders_year = row['total_orders']
    refund_count_year = row['refund_count']
    
    if total_orders_year > 0:
        refund_stat = f"{year}: 1 of every {round(total_orders_year / refund_count_year)} orders refunded ({row['refund_rate']} refund rate)"
    else:
        refund_stat = f"{year}: N/A (No Orders)"
    
    yearly_refund_stats.append(refund_stat)

yearly_refund_stats_str = "\n".join(yearly_refund_stats)

# Visualization: Total Orders and Refunds by Year
plt.figure(figsize=(12, 6))
plt.bar(df['year'], df['total_orders'], color='blue', alpha=0.7, label='Total Orders')
plt.bar(df['year'], df['refund_count'], color='red', alpha=0.7, label='Refund Count')
plt.title('Total Orders and Refund Count by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.xticks(df['year'])
plt.savefig('total_orders_refunds_by_year.png')
plt.close()

# Visualization: Refund Rate by Year with Labels
plt.figure(figsize=(12, 6))
plt.plot(df['year'], df['refund_rate_float'], marker='o', linestyle='-', color='green', label='Refund Rate')

# Adding data labels
for i, txt in enumerate(df['refund_rate_float']):
    plt.annotate(f'{txt:.4f}', (df['year'].iloc[i], df['refund_rate_float'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Refund Rate by Year')
plt.xlabel('Year')
plt.ylabel('Refund Rate')
plt.xticks(df['year'])
plt.legend()
plt.grid(True)
plt.savefig('refund_rate_by_year.png')
plt.close()

# Focused Analysis: Pre-COVID (2019) vs. Post-COVID (2023)
df_focus = df[df['year'].isin([2019, 2023])]

# Visualization: 2019 vs 2023
plt.figure(figsize=(8, 6))
width = 0.35
years = df_focus['year']
total_orders = df_focus['total_orders'].astype(int)
refund_count = df_focus['refund_count'].astype(int)

plt.bar(years - width/2, total_orders, width, label='Total Orders', color='blue')
plt.bar(years + width/2, refund_count, width, label='Refund Count', color='red')

plt.title('Comparison of Total Orders and Refund Count: 2019 vs 2023')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(years)
plt.legend()
plt.savefig('comparison_2019_2023.png')
plt.close()

# Create a PDF and add the saved images
pdf = FPDF()

# Introduction Page
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, 'Refund Analysis Report', ln=True, align='C')
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, 'Prepared by Ismat Samadov', ln=True, align='C')
pdf.ln(20)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, f"This report provides an analysis of refunds for orders made on the 12Go platform. The data "
                      f"covers multiple years, focusing on the refund rates and their trends. The report includes "
                      f"visual comparisons of key metrics and provides actionable insights based on the findings.\n\n"
                      f"Refund Statistics:\n"
                      f"Total Orders: {total_orders_rounded}\n"
                      f"Total Refunds: {total_refunds_rounded}\n"
                      f"Overall Refund Percentage: {refund_percentage_rounded}%\n\n"
                      f"Yearly Refund Statistics:\n{yearly_refund_stats_str}")

# Add the first image
pdf.add_page()
pdf.image('total_orders_refunds_by_year.png', x=10, y=10, w=180)

pdf.add_page()

# Add the second image
pdf.image('refund_rate_by_year.png', x=10, y=10, w=180)

pdf.add_page()

# Add the third image
pdf.image('comparison_2019_2023.png', x=10, y=10, w=180)

# Actionable Insights Page
pdf.add_page()
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, 'Actionable Insights', ln=True, align='C')
pdf.ln(10)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "1. Station-Specific Decline: Certain stations may show a higher decline in EPS, "
                      "indicating decreased demand or increased competition. Consider targeted marketing or "
                      "adjusting services at these stations.\n\n"
                      "2. Operator Performance: Identify underperforming operators who might be causing "
                      "operational inefficiencies or customer dissatisfaction. Work with them to improve service quality.\n\n"
                      "3. Vehicle Class Impact: Analyze which vehicle classes are contributing to the decline in EPS. "
                      "Adjust pricing, add value-added services, or promote higher-margin classes accordingly.\n\n"
                      "4. Country-Specific Trends: Tailor marketing efforts and pricing strategies to reflect "
                      "regional demand differences by analyzing country-specific EPS trends.\n\n")

# Save the PDF
pdf_output_path = '12go_analysis_visualizations.pdf'
pdf.output(pdf_output_path)

pdf_output_path
