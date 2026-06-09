import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Read the Excel file
file_path = 'Contract Base Reports GTMS WW 03June2026.xlsx'
sheet_name = 'Component Details'

print("Reading Excel file...")
df = pd.read_excel(file_path, sheet_name=sheet_name)

print(f"Total records loaded: {len(df)}")
print("\nColumn names in the sheet:")
print(df.columns.tolist())

# Map columns based on the provided information
column_mapping = {
    'B': 'Country',
    'K': 'Auto_Renewal_Flag',
    'O': 'Brand',
    'P': 'Product_Family',
    'Q': 'Machine_Type',
    'R': 'Model',
    'S': 'Serial_Number',
    'V': 'EOS_Date',
    'X': 'Service_Name',
    'Y': 'Service_Level',
    'Z': 'SLA_Type',
    'AD': 'L40_Name',
    'AH': 'Service_Start_Date',
    'AI': 'Service_End_Date',
    'AJ': 'Comp_Status',
    'AL': 'Comp_Total_Amount_USD'
}

# Get actual column names by index (Excel columns are 0-indexed in pandas)
def get_col_by_letter(letter):
    """Convert Excel column letter to 0-based index"""
    col_index = 0
    for char in letter:
        col_index = col_index * 26 + (ord(char.upper()) - ord('A') + 1)
    return col_index - 1

# Create a mapping of our names to actual column names
actual_columns = {}
for letter, name in column_mapping.items():
    idx = get_col_by_letter(letter)
    if idx < len(df.columns):
        actual_columns[name] = df.columns[idx]

print("\nMapped columns:")
for name, col in actual_columns.items():
    print(f"{name}: {col}")

# Rename columns for easier access
df_analysis = df.copy()
df_analysis = df_analysis.rename(columns={v: k for k, v in actual_columns.items()})

# Convert date columns to datetime
date_columns = ['EOS_Date', 'Service_Start_Date', 'Service_End_Date']
for col in date_columns:
    if col in df_analysis.columns:
        df_analysis[col] = pd.to_datetime(df_analysis[col], errors='coerce')

# Convert amount to numeric
if 'Comp_Total_Amount_USD' in df_analysis.columns:
    df_analysis['Comp_Total_Amount_USD'] = pd.to_numeric(df_analysis['Comp_Total_Amount_USD'], errors='coerce')

# Extract Year and Quarter from Service Start Date
df_analysis['Start_Year'] = df_analysis['Service_Start_Date'].dt.year
df_analysis['Start_Quarter'] = df_analysis['Service_Start_Date'].dt.quarter
df_analysis['Start_YearQuarter'] = df_analysis['Start_Year'].astype(str) + '-Q' + df_analysis['Start_Quarter'].astype(str)

# Extract Year and Quarter from Service End Date
df_analysis['End_Year'] = df_analysis['Service_End_Date'].dt.year
df_analysis['End_Quarter'] = df_analysis['Service_End_Date'].dt.quarter
df_analysis['End_YearQuarter'] = df_analysis['End_Year'].astype(str) + '-Q' + df_analysis['End_Quarter'].astype(str)

print("\n" + "="*80)
print("GLOBAL TOTAL MICROCODE SUPPORT (GTMS) CONTRACT ANALYSIS")
print("="*80)

# 1. Signings by Year and Quarter, split by Service Name
print("\n1. CONTRACT SIGNINGS BY YEAR AND QUARTER (Split by Service Name)")
print("-" * 80)
signings = df_analysis.groupby(['Start_YearQuarter', 'Service_Name']).size().reset_index(name='Count')
signings_pivot = signings.pivot(index='Start_YearQuarter', columns='Service_Name', values='Count').fillna(0)
signings_pivot['Total'] = signings_pivot.sum(axis=1)
signings_pivot = signings_pivot.sort_index()
print(signings_pivot.to_string())

print("\n\nTotal Signings by Service Name:")
total_signings = df_analysis.groupby('Service_Name').size().reset_index(name='Total_Contracts')
print(total_signings.to_string(index=False))

# 2. Revenue by Year and Quarter
print("\n\n2. TOTAL REVENUE BY YEAR AND QUARTER (Split by Service Name)")
print("-" * 80)
print("\nRevenue by Contract Start Date:")
revenue_start = df_analysis.groupby(['Start_YearQuarter', 'Service_Name'])['Comp_Total_Amount_USD'].sum().reset_index()
revenue_start_pivot = revenue_start.pivot(index='Start_YearQuarter', columns='Service_Name', values='Comp_Total_Amount_USD').fillna(0)
revenue_start_pivot['Total'] = revenue_start_pivot.sum(axis=1)
revenue_start_pivot = revenue_start_pivot.sort_index()
print(revenue_start_pivot.to_string())

print("\n\nRevenue by Contract End Date:")
revenue_end = df_analysis.groupby(['End_YearQuarter', 'Service_Name'])['Comp_Total_Amount_USD'].sum().reset_index()
revenue_end_pivot = revenue_end.pivot(index='End_YearQuarter', columns='Service_Name', values='Comp_Total_Amount_USD').fillna(0)
revenue_end_pivot['Total'] = revenue_end_pivot.sum(axis=1)
revenue_end_pivot = revenue_end_pivot.sort_index()
print(revenue_end_pivot.to_string())

print("\n\nTotal Revenue by Service Name:")
total_revenue = df_analysis.groupby('Service_Name')['Comp_Total_Amount_USD'].sum().reset_index()
total_revenue.columns = ['Service_Name', 'Total_Revenue_USD']
total_revenue['Total_Revenue_USD'] = total_revenue['Total_Revenue_USD'].apply(lambda x: f"${x:,.2f}")
print(total_revenue.to_string(index=False))

# 3. Auto Renewal Analysis
print("\n\n3. AUTO RENEWAL FLAG ANALYSIS (Split by Service Name)")
print("-" * 80)
auto_renewal = df_analysis.groupby(['Service_Name', 'Auto_Renewal_Flag']).size().reset_index(name='Count')
auto_renewal_pivot = auto_renewal.pivot(index='Service_Name', columns='Auto_Renewal_Flag', values='Count').fillna(0)
auto_renewal_pivot['Total'] = auto_renewal_pivot.sum(axis=1)

# Calculate percentages
for col in auto_renewal_pivot.columns:
    if col != 'Total':
        auto_renewal_pivot[f'{col}_Pct'] = (auto_renewal_pivot[col] / auto_renewal_pivot['Total'] * 100).round(2)

print(auto_renewal_pivot.to_string())

# 4. CMSL SLA Type Analysis
print("\n\n4. CMSL SLA TYPE ANALYSIS (Split by Service Name)")
print("-" * 80)
sla_analysis = df_analysis.groupby(['Service_Name', 'SLA_Type']).size().reset_index(name='Count')
sla_pivot = sla_analysis.pivot(index='Service_Name', columns='SLA_Type', values='Count').fillna(0)
sla_pivot['Total'] = sla_pivot.sum(axis=1)

# Calculate CMSL percentage
if 'CMSL' in sla_pivot.columns:
    sla_pivot['CMSL_Pct'] = (sla_pivot['CMSL'] / sla_pivot['Total'] * 100).round(2)

print(sla_pivot.to_string())

# 5. EOS Date Analysis
print("\n\n5. END OF SERVICE (EOS) DATE ANALYSIS")
print("-" * 80)
current_date = pd.Timestamp.now()
df_analysis['Days_to_EOS'] = (df_analysis['EOS_Date'] - current_date).dt.days

# Machines approaching EOS (within 1 year)
approaching_eos = df_analysis[df_analysis['Days_to_EOS'].between(0, 365)]
print(f"\nMachines approaching EOS within 1 year: {len(approaching_eos)}")
if len(approaching_eos) > 0:
    eos_by_service = approaching_eos.groupby('Service_Name').size().reset_index(name='Count')
    print(eos_by_service.to_string(index=False))

# Machines past EOS with active contracts
past_eos = df_analysis[df_analysis['Days_to_EOS'] < 0]
print(f"\n\nMachines past EOS date: {len(past_eos)}")
if len(past_eos) > 0:
    past_eos_by_service = past_eos.groupby('Service_Name').size().reset_index(name='Count')
    print(past_eos_by_service.to_string(index=False))

# 6. Contract Status Analysis
print("\n\n6. CONTRACT STATUS ANALYSIS")
print("-" * 80)
status_analysis = df_analysis.groupby(['Comp_Status', 'Service_Name']).size().reset_index(name='Count')
status_pivot = status_analysis.pivot(index='Comp_Status', columns='Service_Name', values='Count').fillna(0)
status_pivot['Total'] = status_pivot.sum(axis=1)
print(status_pivot.to_string())

# 7. Geographic Distribution
print("\n\n7. GEOGRAPHIC DISTRIBUTION (Top 15 Countries)")
print("-" * 80)
country_dist = df_analysis.groupby('Country').agg({
    'Serial_Number': 'count',
    'Comp_Total_Amount_USD': 'sum'
}).reset_index()
country_dist.columns = ['Country', 'Contract_Count', 'Total_Revenue_USD']
country_dist = country_dist.sort_values('Total_Revenue_USD', ascending=False).head(15)
country_dist['Total_Revenue_USD'] = country_dist['Total_Revenue_USD'].apply(lambda x: f"${x:,.2f}")
print(country_dist.to_string(index=False))

# 8. Additional Insights for Sales Motion
print("\n\n8. ADDITIONAL INSIGHTS FOR SALES MOTION")
print("-" * 80)

# Contracts expiring in next 6 months
six_months_out = current_date + pd.DateOffset(months=6)
expiring_soon = df_analysis[
    (df_analysis['Service_End_Date'] >= current_date) & 
    (df_analysis['Service_End_Date'] <= six_months_out)
]
print(f"\nContracts expiring in next 6 months: {len(expiring_soon)}")
print(f"Total revenue at risk: ${expiring_soon['Comp_Total_Amount_USD'].sum():,.2f}")

if len(expiring_soon) > 0:
    expiring_by_service = expiring_soon.groupby('Service_Name').agg({
        'Serial_Number': 'count',
        'Comp_Total_Amount_USD': 'sum'
    }).reset_index()
    expiring_by_service.columns = ['Service_Name', 'Count', 'Revenue_USD']
    expiring_by_service['Revenue_USD'] = expiring_by_service['Revenue_USD'].apply(lambda x: f"${x:,.2f}")
    print("\nBy Service Name:")
    print(expiring_by_service.to_string(index=False))

# Average contract value by service
print("\n\nAverage Contract Value by Service Name:")
avg_value = df_analysis.groupby('Service_Name')['Comp_Total_Amount_USD'].agg(['mean', 'median', 'count']).reset_index()
avg_value.columns = ['Service_Name', 'Mean_USD', 'Median_USD', 'Count']
avg_value['Mean_USD'] = avg_value['Mean_USD'].apply(lambda x: f"${x:,.2f}")
avg_value['Median_USD'] = avg_value['Median_USD'].apply(lambda x: f"${x:,.2f}")
print(avg_value.to_string(index=False))

# Product Family Analysis
print("\n\nTop 10 Product Families by Contract Count:")
product_family = df_analysis.groupby('Product_Family').agg({
    'Serial_Number': 'count',
    'Comp_Total_Amount_USD': 'sum'
}).reset_index()
product_family.columns = ['Product_Family', 'Contract_Count', 'Total_Revenue_USD']
product_family = product_family.sort_values('Contract_Count', ascending=False).head(10)
product_family['Total_Revenue_USD'] = product_family['Total_Revenue_USD'].apply(lambda x: f"${x:,.2f}")
print(product_family.to_string(index=False))

print("\n\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)

# Save summary to file
with open('GTMS_WW_Analysis_Summary.txt', 'w') as f:
    f.write("="*80 + "\n")
    f.write("GLOBAL TOTAL MICROCODE SUPPORT (GTMS) CONTRACT ANALYSIS\n")
    f.write("Analysis Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total Contracts: {len(df_analysis)}\n")
    f.write(f"Total Revenue: ${df_analysis['Comp_Total_Amount_USD'].sum():,.2f}\n")
    f.write(f"Date Range: {df_analysis['Service_Start_Date'].min()} to {df_analysis['Service_End_Date'].max()}\n")

print("\nSummary saved to: GTMS_WW_Analysis_Summary.txt")

# Made with Bob
