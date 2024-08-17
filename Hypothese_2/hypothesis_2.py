import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# Data for 2019
data_2019 = {
    "from_station_name": ["Chiang Mai Town", "Kuala Lumpur Airport", "Queen Aliya Amman Jordan", "Casablanca Airport", "zzDoNotUse", "Incheon Airport", "Manama Airport", "Berlin Tegel Airport", "Narita Airport", "Soekarno Hatta Airport"],
    "to_station_name": ["Suvarnabhumi Airport", "Heathrow Airport", "Istanbul New Airport", "Istanbul New Airport", "Manama Airport", "Phnom Penh Airport", "Jeddah Airport", "Domodedovo Airport", "Hanoi Noi Bai Airport", "Sorong Airport"],
    "country": ["Thailand", "Malaysia", "Jordan", "Morocco", "Bahrain", "South Korea", "Bahrain", "Germany", "Japan", "Indonesia"],
    "vehclass_id": ["bus", "avia", "avia", "avia", "avia", "avia", "avia", "avia", "avia", "avia"],
    "class_name": ["Express", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy"],
    "total_seats": [1, 1, 1, 1, 1, 3, 1, 2, 2, 1],
    "total_netprice": [20.02, 0.0, 0.0, 0.0, 0.0, 267.02, 0.0, 0.0, 482.97, 0.0],
    "total_revenue": [3458.58, 710.25, 561.58, 443.27, 365.77, 1228.48, 318.94, 606.69, 1085.83, 291.02],
    "EPS": [3438.56, 710.25, 561.58, 443.27, 365.77, 320.49, 318.94, 303.35, 301.43, 291.02],
    "year": [2019] * 10
}

# Data for 2023
data_2023 = {
    "from_station_name": ["Dubai International Airport", "Suvarnabhumi Airport", "Abidjan Airport", "Suvarnabhumi Airport", "Casablanca Airport", "Abidjan Airport", "Charles de Gaulle Airport", "Beijing Daxing Airport", "Harare Airport", "Singapore Airport"],
    "to_station_name": ["Agadir Airport", "Charles de Gaulle Airport", "Casablanca Airport", "Amsterdam Schiphol Airport", "Abidjan Airport", "Bamako Airport", "Suvarnabhumi Airport", "Narita Airport", "OR Tambo Airport", "Hong Kong Airport"],
    "country": ["UAE", "Thailand", "Ivory Coast", "Thailand", "Morocco", "Ivory Coast", "France", "China", "Zimbabwe", "Singapore"],
    "vehclass_id": ["avia", "avia", "avia", "avia", "avia", "avia", "avia", "avia", "avia", "avia"],
    "class_name": ["Economy", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy", "Economy"],
    "total_seats": [1, 5, 8, 2, 8, 2, 5, 2, 1, 2],
    "total_netprice": [0.0, 652.72, 1744.64, 865.65, 1318.92, 0.0, 562.31, 885.95, 0.0, 0.0],
    "total_revenue": [608.38, 3530.67, 6307.94, 1903.58, 5346.09, 996.19, 2857.59, 1797.44, 452.60, 880.06],
    "EPS": [608.38, 575.59, 570.41, 518.96, 503.40, 498.10, 459.06, 455.74, 452.60, 440.03],
    "year": [2023] * 10
}

# Create DataFrames
df_2019 = pd.DataFrame(data_2019)
df_2023 = pd.DataFrame(data_2023)

# Combine the two DataFrames
df_combined = pd.concat([df_2019, df_2023])

# Visualization: 2019 vs 2023 EPS Route Comparison
plt.figure(figsize=(8, 6))
sns.barplot(x='from_station_name', y='EPS', hue='year', data=df_combined)
plt.title('2019 vs 2023 EPS Route Comparison')
plt.xlabel('From Station Name')
plt.ylabel('EPS')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig('eps_route_comparison.png')
plt.close()

# Filter out routes that were in the top 2019 EPS but are not in 2023 EPS
top_2019_routes = df_2019.nlargest(5, 'EPS')
top_2019_routes_names = top_2019_routes['from_station_name'].tolist()

# Check if these routes are present in the top of 2023
not_in_2023 = df_2023[~df_2023['from_station_name'].isin(top_2019_routes_names)]

# Visualization: EPS Comparison for Top 2019 Routes (Highlighting those not in 2023)
plt.figure(figsize=(8, 6))
sns.barplot(x='from_station_name', y='EPS', hue='year', data=df_combined[df_combined['from_station_name'].isin(top_2019_routes_names)])
plt.title('EPS Comparison for Top 2019 Routes (2019 vs. 2023)')
plt.xlabel('From Station Name')
plt.ylabel('EPS')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig('eps_comparison_top_routes.png')
plt.close()

# Highlight routes that were top in 2019 but not in 2023
if not not_in_2023.empty:
    plt.figure(figsize=(8, 6))
    sns.barplot(x='from_station_name', y='EPS', hue='year', data=not_in_2023)
    plt.title('Top 2019 Routes Not in Top 2023')
    plt.xlabel('From Station Name')
    plt.ylabel('EPS')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig('eps_not_in_2023.png')
    plt.close()

# EPS Comparison for both 2019 and 2023 in one chart
plt.figure(figsize=(8, 6))
sns.barplot(x='from_station_name', y='EPS', hue='year', data=df_combined)
plt.title('EPS Comparison by Route (2019 vs. 2023)')
plt.xlabel('From Station Name')
plt.ylabel('EPS')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig('eps_comparison_all_routes.png')
plt.close()

# Calculate Overall EPS Statistics
overall_eps_2019 = df_2019['EPS'].mean()
overall_eps_2023 = df_2023['EPS'].mean()

# Visualization: Overall EPS Comparison
plt.figure(figsize=(8, 6))
sns.barplot(x=['2019', '2023'], y=[overall_eps_2019, overall_eps_2023])
plt.title('Overall EPS Comparison (2019 vs. 2023)')
plt.ylabel('Average EPS')
plt.tight_layout()
plt.savefig('overall_eps_comparison.png')
plt.close()

# Country-based insights
# Top countries in 2019 by EPS
top_countries_2019 = df_2019.groupby('country')['EPS'].mean().nlargest(5)
# Top countries in 2023 by EPS
top_countries_2023 = df_2023.groupby('country')['EPS'].mean().nlargest(5)

# Visualization: Top Countries by EPS in 2019 and 2023
plt.figure(figsize=(8, 6))
sns.barplot(x=top_countries_2019.index, y=top_countries_2019.values)
plt.title('Top 5 Countries by Average EPS in 2019')
plt.xlabel('Country')
plt.ylabel('Average EPS')
plt.tight_layout()
plt.savefig('top_countries_2019.png')
plt.close()

plt.figure(figsize=(8, 6))
sns.barplot(x=top_countries_2023.index, y=top_countries_2023.values)
plt.title('Top 5 Countries by Average EPS in 2023')
plt.xlabel('Country')
plt.ylabel('Average EPS')
plt.tight_layout()
plt.savefig('top_countries_2023.png')
plt.close()

# Create PDF with all charts
pdf = FPDF()

# Add the eps_comparison_all_routes
pdf.add_page()
pdf.image('eps_comparison_all_routes.png', x=10, y=10, w=180)

# Add the EPS Comparison Chart for Top 2019 Routes
pdf.add_page()
pdf.image('eps_comparison_top_routes.png', x=10, y=10, w=180)

# Add the EPS Not in 2023 Chart
if not not_in_2023.empty:
    pdf.add_page()
    pdf.image('eps_not_in_2023.png', x=10, y=10, w=180)

# Add the Overall EPS Comparison Chart
pdf.add_page()
pdf.image('overall_eps_comparison.png', x=10, y=10, w=180)

# Add the Country-based Insights
pdf.add_page()

# Add the Top Countries by EPS in 2019 Chart
pdf.image('top_countries_2019.png', x=10, y=10, w=180)

# Add the Top Countries by EPS in 2023 Chart
pdf.add_page()
pdf.image('top_countries_2023.png', x=10, y=10, w=180)

# Add a summary page with insights
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, f"Summary of Insights:\n\n"
                      f"1. 2019 vs 2023 EPS Route Comparison:\n"
                      f"   - This chart compares EPS for the top routes in both 2019 and 2023. Significant changes in EPS between the two years highlight shifts in route profitability.\n\n"
                      f"   - Focus on the routes in Thailand that saw a decline in EPS from 2019 to 2023.\n"
                      f"2. Overall EPS Comparison:\n"
                      f"   - The average EPS decreased from {overall_eps_2019:.2f} in 2019 to {overall_eps_2023:.2f} in 2023.\n"
                      f"   - This suggests a general decline in profitability per seat across routes.\n\n"
                      f"3. Top 2019 Routes Not Performing in 2023:\n"
                      f"   - Some of the top-performing routes in 2019 did not maintain their positions in 2023.\n"
                      f"   - For instance, routes like {', '.join(not_in_2023['from_station_name'].unique())} saw significant drops in EPS.\n\n"
                      f"4. Country-Based Trends:\n"
                      f"   - In 2019, the top countries by EPS were: {', '.join(top_countries_2019.index)}.\n"
                      f"   - By 2023, the top countries shifted to: {', '.join(top_countries_2023.index)}.\n"
                      f"   - This indicates changes in market dynamics and profitability across regions.\n\n",)

# Add a summary page with detailed actionable insights
pdf.add_page()
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, 'Actionable Insights', ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, f"1. Targeted Promotions:\n"
                      f"   - Focus on routes that saw a decline in EPS from 2019 to 2023.\n"
                      f"   - Consider offering promotions such as discounts, bundle offers, and loyalty rewards to regain market share.\n"
                      f"   - Track the effectiveness of these promotions using key performance indicators like conversion rate and booking volume.\n\n"
                      f"2. Market Analysis:\n"
                      f"   - Conduct competitor analysis and gather customer feedback to understand the shifts in top-performing routes and countries.\n"
                      f"   - Use demand forecasting and price sensitivity analysis to optimize route offerings and pricing strategies.\n\n"
                      f"3. Service Enhancements:\n"
                      f"   - Assess service quality on underperforming routes and identify areas for improvement.\n"
                      f"   - Consider partnerships with local businesses and upgrading services to provide added value to customers.\n"
                      f"   - Communicate service enhancements effectively through targeted marketing campaigns.\n")


# Save the PDF
pdf_output_path = 'eps_analysis_report.pdf'
pdf.output(pdf_output_path)

# Display the path of the generated PDF report
print(f"PDF report generated and saved as: {pdf_output_path}")
