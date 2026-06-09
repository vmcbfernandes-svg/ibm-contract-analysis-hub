import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Read the Excel file
file_path = 'Contract Base Reports Europe 02June2026.xlsx'
print(f"Reading file: {file_path}")

# Read the Component Details sheet
df = pd.read_excel(file_path, sheet_name='Component Details')

print(f"\nTotal records loaded: {len(df)}")
print(f"Columns in dataset: {df.columns.tolist()}")

# Map column letters to names based on the provided mapping
column_mapping = {
    'B': 'Country',
    'K': 'Auto Renewal Flag',
    'O': 'Brand',
    'P': 'Product Family',
    'Q': 'Machine Type',
    'R': 'Model',
    'S': 'Serial Number',
    'V': 'EOS Date',
    'X': 'Service Name',
    'Y': 'Service Level',
    'Z': 'SLA Type',
    'AD': 'L40 Name',
    'AH': 'Service Start Date',
    'AI': 'Service End Date',
    'AJ': 'Comp Status',
    'AL': 'Comp Total Amount USD'
}

# Get actual column names (Excel columns are 0-indexed in pandas)
# Column B = index 1, K = index 10, etc.
def excel_col_to_index(col_letter):
    """Convert Excel column letter to 0-based index"""
    result = 0
    for char in col_letter:
        result = result * 26 + (ord(char.upper()) - ord('A') + 1)
    return result - 1

# Create a mapping of our names to actual column names
actual_columns = {}
for excel_col, our_name in column_mapping.items():
    idx = excel_col_to_index(excel_col)
    if idx < len(df.columns):
        actual_columns[our_name] = df.columns[idx]

print(f"\nMapped columns: {actual_columns}")

# Rename columns for easier access
df_analysis = df.iloc[:, [excel_col_to_index(col) for col in column_mapping.keys()]].copy()
df_analysis.columns = list(column_mapping.values())

# Convert date columns to datetime
date_columns = ['EOS Date', 'Service Start Date', 'Service End Date']
for col in date_columns:
    df_analysis[col] = pd.to_datetime(df_analysis[col], errors='coerce')

# Convert amount to numeric
df_analysis['Comp Total Amount USD'] = pd.to_numeric(df_analysis['Comp Total Amount USD'], errors='coerce')

print("\n" + "="*80)
print("EUROPE CONTRACT ANALYSIS REPORT")
print("="*80)

# ============================================================================
# 1. SIGNINGS BY YEAR AND QUARTER (Contract Start Date) - Split by Service Name
# ============================================================================
print("\n\n1. CONTRACT SIGNINGS BY YEAR AND QUARTER (Split by Service Name)")
print("-" * 80)

df_analysis['Start Year'] = df_analysis['Service Start Date'].dt.year
df_analysis['Start Quarter'] = df_analysis['Service Start Date'].dt.quarter
df_analysis['Start YearQ'] = df_analysis['Start Year'].astype(str) + '-Q' + df_analysis['Start Quarter'].astype(str)

signings = df_analysis.groupby(['Start YearQ', 'Service Name']).size().reset_index(name='Number of Signings')
signings_pivot = signings.pivot(index='Start YearQ', columns='Service Name', values='Number of Signings').fillna(0)
signings_pivot['Total'] = signings_pivot.sum(axis=1)
signings_pivot = signings_pivot.sort_index()

print("\nSignings by Year-Quarter and Service Name:")
print(signings_pivot.to_string())

# ============================================================================
# 2. REVENUE BY YEAR AND QUARTER - Split by Service Name
# ============================================================================
print("\n\n2. TOTAL REVENUE BY YEAR AND QUARTER (Split by Service Name)")
print("-" * 80)

# For revenue, we need to consider the contract period
# Revenue should be recognized over the contract period
revenue_data = []

for idx, row in df_analysis.iterrows():
    if pd.notna(row['Service Start Date']) and pd.notna(row['Service End Date']) and pd.notna(row['Comp Total Amount USD']):
        start_date = row['Service Start Date']
        end_date = row['Service End Date']
        total_amount = row['Comp Total Amount USD']
        service_name = row['Service Name']
        
        # Calculate contract duration in days
        duration_days = (end_date - start_date).days
        if duration_days <= 0:
            continue
            
        # Allocate revenue to each quarter
        current_date = start_date
        while current_date <= end_date:
            quarter_end = pd.Timestamp(year=current_date.year, month=(current_date.quarter * 3), day=1) + pd.offsets.QuarterEnd(0)
            quarter_end = min(quarter_end, end_date)
            
            days_in_quarter = (quarter_end - current_date).days + 1
            revenue_in_quarter = (days_in_quarter / duration_days) * total_amount
            
            year_q = f"{current_date.year}-Q{current_date.quarter}"
            revenue_data.append({
                'YearQ': year_q,
                'Service Name': service_name,
                'Revenue': revenue_in_quarter
            })
            
            current_date = quarter_end + pd.Timedelta(days=1)

revenue_df = pd.DataFrame(revenue_data)
if not revenue_df.empty:
    revenue_summary = revenue_df.groupby(['YearQ', 'Service Name'])['Revenue'].sum().reset_index()
    revenue_pivot = revenue_summary.pivot(index='YearQ', columns='Service Name', values='Revenue').fillna(0)
    revenue_pivot['Total'] = revenue_pivot.sum(axis=1)
    revenue_pivot = revenue_pivot.sort_index()
    
    print("\nRevenue by Year-Quarter and Service Name (USD):")
    print(revenue_pivot.to_string())
else:
    print("\nNo revenue data available")

# ============================================================================
# 3. AUTO RENEWAL FLAG ANALYSIS - Split by Service Name
# ============================================================================
print("\n\n3. AUTO RENEWAL FLAG ANALYSIS (Split by Service Name)")
print("-" * 80)

auto_renewal = df_analysis.groupby(['Service Name', 'Auto Renewal Flag']).size().reset_index(name='Count')
auto_renewal_pivot = auto_renewal.pivot(index='Service Name', columns='Auto Renewal Flag', values='Count').fillna(0)

# Calculate percentages
auto_renewal_pivot['Total'] = auto_renewal_pivot.sum(axis=1)
for col in auto_renewal_pivot.columns[:-1]:
    auto_renewal_pivot[f'{col} %'] = (auto_renewal_pivot[col] / auto_renewal_pivot['Total'] * 100).round(2)

print("\nAuto Renewal Flag by Service Name:")
print(auto_renewal_pivot.to_string())

# ============================================================================
# 4. CMSL SLA TYPE ANALYSIS - Split by Service Name
# ============================================================================
print("\n\n4. CMSL SLA TYPE ANALYSIS (Split by Service Name)")
print("-" * 80)

sla_analysis = df_analysis.groupby(['Service Name', 'SLA Type']).size().reset_index(name='Count')
sla_pivot = sla_analysis.pivot(index='Service Name', columns='SLA Type', values='Count').fillna(0)

# Calculate percentages for CMSL
sla_pivot['Total'] = sla_pivot.sum(axis=1)
if 'CMSL' in sla_pivot.columns:
    sla_pivot['CMSL %'] = (sla_pivot['CMSL'] / sla_pivot['Total'] * 100).round(2)

print("\nSLA Type by Service Name:")
print(sla_pivot.to_string())

# ============================================================================
# 5. EOS DATE ANALYSIS
# ============================================================================
print("\n\n5. END OF SERVICE (EOS) DATE ANALYSIS")
print("-" * 80)

# Contracts with EOS dates in the past or near future
current_date = pd.Timestamp.now()
df_analysis['Days to EOS'] = (df_analysis['EOS Date'] - current_date).dt.days

eos_categories = []
for idx, row in df_analysis.iterrows():
    if pd.notna(row['Days to EOS']):
        if row['Days to EOS'] < 0:
            eos_categories.append('Past EOS')
        elif row['Days to EOS'] <= 90:
            eos_categories.append('EOS within 90 days')
        elif row['Days to EOS'] <= 180:
            eos_categories.append('EOS within 180 days')
        elif row['Days to EOS'] <= 365:
            eos_categories.append('EOS within 1 year')
        else:
            eos_categories.append('EOS > 1 year')
    else:
        eos_categories.append('No EOS Date')

df_analysis['EOS Category'] = eos_categories

eos_summary = df_analysis.groupby(['EOS Category', 'Service Name']).size().reset_index(name='Count')
eos_pivot = eos_summary.pivot(index='EOS Category', columns='Service Name', values='Count').fillna(0)
eos_pivot['Total'] = eos_pivot.sum(axis=1)

print("\nContracts by EOS Category and Service Name:")
print(eos_pivot.to_string())

# ============================================================================
# 6. CONTRACT STATUS ANALYSIS
# ============================================================================
print("\n\n6. CONTRACT STATUS ANALYSIS")
print("-" * 80)

status_summary = df_analysis.groupby(['Comp Status', 'Service Name']).size().reset_index(name='Count')
status_pivot = status_summary.pivot(index='Comp Status', columns='Service Name', values='Count').fillna(0)
status_pivot['Total'] = status_pivot.sum(axis=1)

print("\nContract Status by Service Name:")
print(status_pivot.to_string())

# ============================================================================
# 7. ADDITIONAL INSIGHTS FOR SALES MOTION
# ============================================================================
print("\n\n7. ADDITIONAL INSIGHTS FOR SALES MOTION")
print("-" * 80)

# A. Contracts expiring soon without auto-renewal
print("\n7A. HIGH PRIORITY: Contracts expiring within 180 days WITHOUT Auto Renewal")
expiring_no_renewal = df_analysis[
    (df_analysis['Days to EOS'] <= 180) & 
    (df_analysis['Days to EOS'] > 0) &
    (df_analysis['Auto Renewal Flag'] != 'Yes')
][['Country', 'Service Name', 'Service Level', 'Days to EOS', 'Comp Total Amount USD']].sort_values('Days to EOS')

print(f"\nTotal contracts: {len(expiring_no_renewal)}")
print(f"Total revenue at risk: ${expiring_no_renewal['Comp Total Amount USD'].sum():,.2f}")
if not expiring_no_renewal.empty:
    print("\nTop 10 by contract value:")
    print(expiring_no_renewal.nlargest(10, 'Comp Total Amount USD').to_string())

# B. Revenue by Country and Service Name
print("\n\n7B. REVENUE BY COUNTRY AND SERVICE NAME")
country_revenue = df_analysis.groupby(['Country', 'Service Name'])['Comp Total Amount USD'].sum().reset_index()
country_revenue_pivot = country_revenue.pivot(index='Country', columns='Service Name', values='Comp Total Amount USD').fillna(0)
country_revenue_pivot['Total'] = country_revenue_pivot.sum(axis=1)
country_revenue_pivot = country_revenue_pivot.sort_values('Total', ascending=False)

print("\nTop 10 Countries by Revenue:")
print(country_revenue_pivot.head(10).to_string())

# C. Average contract value by Service Name
print("\n\n7C. AVERAGE CONTRACT VALUE BY SERVICE NAME")
avg_contract_value = df_analysis.groupby('Service Name')['Comp Total Amount USD'].agg(['mean', 'median', 'count']).round(2)
avg_contract_value.columns = ['Average Value', 'Median Value', 'Number of Contracts']
print(avg_contract_value.to_string())

# D. Product Family Analysis
print("\n\n7D. TOP PRODUCT FAMILIES BY CONTRACT COUNT")
product_family = df_analysis.groupby(['Product Family', 'Service Name']).size().reset_index(name='Count')
product_family_pivot = product_family.pivot(index='Product Family', columns='Service Name', values='Count').fillna(0)
product_family_pivot['Total'] = product_family_pivot.sum(axis=1)
product_family_pivot = product_family_pivot.sort_values('Total', ascending=False)

print("\nTop 10 Product Families:")
print(product_family_pivot.head(10).to_string())

# E. Upsell Opportunities - Contracts with low service levels
print("\n\n7E. UPSELL OPPORTUNITIES: Contracts with Basic Service Levels")
basic_service = df_analysis[df_analysis['Service Level'].str.contains('Basic|Standard', case=False, na=False)]
upsell_summary = basic_service.groupby(['Service Name', 'Service Level']).agg({
    'Comp Total Amount USD': ['sum', 'count']
}).round(2)
print(f"\nTotal contracts with basic/standard service: {len(basic_service)}")
print(f"Total revenue: ${basic_service['Comp Total Amount USD'].sum():,.2f}")
print("\nBreakdown by Service Name and Level:")
print(upsell_summary.to_string())

# F. Contracts past EOS date still active
print("\n\n7F. ATTENTION REQUIRED: Contracts Past EOS Date")
past_eos = df_analysis[
    (df_analysis['Days to EOS'] < 0) &
    (df_analysis['Comp Status'].str.contains('Active', case=False, na=False))
][['Country', 'Service Name', 'EOS Date', 'Service End Date', 'Comp Total Amount USD']].sort_values('EOS Date')

print(f"\nTotal contracts past EOS: {len(past_eos)}")
if not past_eos.empty:
    print("\nSample contracts (first 10):")
    print(past_eos.head(10).to_string())

print("\n" + "="*80)
print("END OF REPORT")
print("="*80)

# Save summary to file
output_file = 'europe_analysis_output.txt'
with open(output_file, 'w') as f:
    f.write("EUROPE CONTRACT ANALYSIS SUMMARY\n")
    f.write("="*80 + "\n\n")
    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total Records: {len(df_analysis)}\n")
    f.write(f"Date Range: {df_analysis['Service Start Date'].min()} to {df_analysis['Service End Date'].max()}\n")
    f.write(f"\nTotal Contract Value: ${df_analysis['Comp Total Amount USD'].sum():,.2f}\n")

print(f"\nSummary saved to: {output_file}")

# Made with Bob
