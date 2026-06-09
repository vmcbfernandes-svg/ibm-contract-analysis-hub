import pandas as pd
import numpy as np
from datetime import datetime

# Read the Excel file
file_path = 'Contract Base Reports HWMA EMEA 02June2026.xlsx'
print(f'Reading file: {file_path}\n')

# Read the Component Details sheet, skipping the first row if it's a header
df = pd.read_excel(file_path, sheet_name='Component Details', header=0)

# Remove any rows where the service name column contains 'Service Name' (header rows)
service_name_col_temp = df.columns[23]
df = df[df[service_name_col_temp] != 'Service Name']
df = df.reset_index(drop=True)

print(f'Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns\n')

# Map column letters to indices (A=0, B=1, etc.)
# Column B - Country name (index 1)
# Column K - Auto Renewal Flag (index 10)
# Column O - Brand (index 14)
# Column P - Product Family (index 15)
# Column Q - Machine Type (index 16)
# Column R - Model (index 17)
# Column S - Serial Number (index 18)
# Column V - EOS Date (index 21)
# Column X - Service Name (index 23)
# Column Y - Service level (index 24)
# Column Z - SLA Type (index 25)
# Column AD - L40 Name (index 29)
# Column AH - Service Start Date (index 33)
# Column AI - Service End Date (index 34)
# Column AJ - Comp Status (index 35)
# Column AL - Comp Total Amount USD (index 37)

print('Column mapping:')
for i, col in enumerate(df.columns):
    print(f'{i}: {col}')

print('\n' + '='*80)
print('DATA ANALYSIS')
print('='*80)

# Get column names by index
country_col = df.columns[1]
auto_renewal_col = df.columns[10]
brand_col = df.columns[14]
product_family_col = df.columns[15]
machine_type_col = df.columns[16]
model_col = df.columns[17]
serial_col = df.columns[18]
eos_date_col = df.columns[21]
service_name_col = df.columns[23]
service_level_col = df.columns[24]
sla_type_col = df.columns[25]
l40_name_col = df.columns[29]
start_date_col = df.columns[33]
end_date_col = df.columns[34]
comp_status_col = df.columns[35]
total_amount_col = df.columns[37]

print(f'\nKey columns identified:')
print(f'Service Name: {service_name_col}')
print(f'Service Start Date: {start_date_col}')
print(f'Service End Date: {end_date_col}')
print(f'Auto Renewal: {auto_renewal_col}')
print(f'SLA Type: {sla_type_col}')
print(f'Total Amount: {total_amount_col}')
print(f'Comp Status: {comp_status_col}')
print(f'EOS Date: {eos_date_col}')

# Convert date columns to datetime
df[start_date_col] = pd.to_datetime(df[start_date_col], errors='coerce')
df[end_date_col] = pd.to_datetime(df[end_date_col], errors='coerce')
df[eos_date_col] = pd.to_datetime(df[eos_date_col], errors='coerce')

# Convert total amount to numeric
df[total_amount_col] = pd.to_numeric(df[total_amount_col], errors='coerce')

# Extract year and quarter from start date
df['Start_Year'] = df[start_date_col].dt.year
df['Start_Quarter'] = df[start_date_col].dt.quarter
df['Start_YearQuarter'] = df['Start_Year'].astype(str) + '-Q' + df['Start_Quarter'].astype(str)

# Extract year and quarter from end date
df['End_Year'] = df[end_date_col].dt.year
df['End_Quarter'] = df[end_date_col].dt.quarter
df['End_YearQuarter'] = df['End_Year'].astype(str) + '-Q' + df['End_Quarter'].astype(str)

print('\n' + '='*80)
print('1. CONTRACT SIGNINGS BY YEAR/QUARTER AND SERVICE NAME')
print('='*80)

# Group by Start Year/Quarter and Service Name
signings = df.groupby(['Start_YearQuarter', service_name_col]).size().reset_index(name='Count')
signings_pivot = signings.pivot(index='Start_YearQuarter', columns=service_name_col, values='Count').fillna(0)
print('\nContract Signings (Start Date) by Year/Quarter and Service Name:')
print(signings_pivot.to_string())
print(f'\nTotal Signings: {signings["Count"].sum():.0f}')

print('\n' + '='*80)
print('2. REVENUE BY YEAR/QUARTER AND SERVICE NAME')
print('='*80)

# For revenue calculation, we need to allocate revenue across the contract period
# Create a function to calculate quarterly revenue
def calculate_quarterly_revenue(row):
    if pd.isna(row[start_date_col]) or pd.isna(row[end_date_col]) or pd.isna(row[total_amount_col]):
        return []
    
    start = row[start_date_col]
    end = row[end_date_col]
    total_amount = row[total_amount_col]
    
    # Calculate total days
    total_days = (end - start).days
    if total_days <= 0:
        return []
    
    # Generate all quarters in the contract period
    quarters = []
    current = start
    while current <= end:
        year = current.year
        quarter = (current.month - 1) // 3 + 1
        quarter_start = pd.Timestamp(year=year, month=(quarter-1)*3+1, day=1)
        if quarter == 4:
            quarter_end = pd.Timestamp(year=year+1, month=1, day=1) - pd.Timedelta(days=1)
        else:
            quarter_end = pd.Timestamp(year=year, month=quarter*3+1, day=1) - pd.Timedelta(days=1)
        
        # Calculate overlap
        overlap_start = max(start, quarter_start)
        overlap_end = min(end, quarter_end)
        
        if overlap_start <= overlap_end:
            overlap_days = (overlap_end - overlap_start).days + 1
            revenue = (overlap_days / total_days) * total_amount
            quarters.append({
                'YearQuarter': f'{year}-Q{quarter}',
                'Revenue': revenue,
                'Service': row[service_name_col]
            })
        
        # Move to next quarter
        if quarter == 4:
            current = pd.Timestamp(year=year+1, month=1, day=1)
        else:
            current = pd.Timestamp(year=year, month=(quarter)*3+1, day=1)
    
    return quarters

# Calculate revenue for all contracts
all_revenue = []
for idx, row in df.iterrows():
    all_revenue.extend(calculate_quarterly_revenue(row))

revenue_df = pd.DataFrame(all_revenue)
if not revenue_df.empty:
    revenue_summary = revenue_df.groupby(['YearQuarter', 'Service'])['Revenue'].sum().reset_index()
    revenue_pivot = revenue_summary.pivot(index='YearQuarter', columns='Service', values='Revenue').fillna(0)
    print('\nQuarterly Revenue by Service Name (USD):')
    print(revenue_pivot.to_string())
    print(f'\nTotal Revenue: ${revenue_summary["Revenue"].sum():,.2f}')
else:
    print('\nNo revenue data available')

print('\n' + '='*80)
print('3. AUTO RENEWAL ANALYSIS BY SERVICE NAME')
print('='*80)

auto_renewal_analysis = df.groupby([service_name_col, auto_renewal_col]).size().reset_index(name='Count')
total_by_service = df.groupby(service_name_col).size().reset_index(name='Total')
auto_renewal_analysis = auto_renewal_analysis.merge(total_by_service, on=service_name_col)
auto_renewal_analysis['Percentage'] = (auto_renewal_analysis['Count'] / auto_renewal_analysis['Total'] * 100).round(2)

print('\nAuto Renewal Flag Analysis:')
print(auto_renewal_analysis.to_string(index=False))

# Summary of contracts with auto renewal ON
auto_on = df[df[auto_renewal_col].astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON'])]
print(f'\nContracts with Auto Renewal ON: {len(auto_on)} ({len(auto_on)/len(df)*100:.2f}% of total)')

print('\n' + '='*80)
print('4. CMSL SLA TYPE ANALYSIS BY SERVICE NAME')
print('='*80)

sla_analysis = df.groupby([service_name_col, sla_type_col]).size().reset_index(name='Count')
sla_analysis = sla_analysis.merge(total_by_service, on=service_name_col)
sla_analysis['Percentage'] = (sla_analysis['Count'] / sla_analysis['Total'] * 100).round(2)

print('\nSLA Type Analysis:')
print(sla_analysis.to_string(index=False))

# Summary of CMSL contracts
cmsl_contracts = df[df[sla_type_col].astype(str).str.upper() == 'CMSL']
print(f'\nContracts with CMSL SLA Type: {len(cmsl_contracts)} ({len(cmsl_contracts)/len(df)*100:.2f}% of total)')

print('\n' + '='*80)
print('5. EOS DATE ANALYSIS')
print('='*80)

# Check contracts that extend beyond EOS date
df['Days_After_EOS'] = (df[end_date_col] - df[eos_date_col]).dt.days
contracts_after_eos = df[df['Days_After_EOS'] > 0]
print(f'\nContracts ending AFTER EOS date: {len(contracts_after_eos)} ({len(contracts_after_eos)/len(df)*100:.2f}% of total)')
print('These contracts may need attention as machines cannot have contracts after EOS date.')

if len(contracts_after_eos) > 0:
    print('\nTop 10 contracts with longest period after EOS:')
    top_eos = contracts_after_eos.nlargest(10, 'Days_After_EOS')[[service_name_col, serial_col, eos_date_col, end_date_col, 'Days_After_EOS']]
    print(top_eos.to_string(index=False))

print('\n' + '='*80)
print('6. CONTRACT STATUS ANALYSIS')
print('='*80)

status_analysis = df.groupby([comp_status_col, service_name_col]).size().reset_index(name='Count')
print('\nContract Status by Service Name:')
status_pivot = status_analysis.pivot(index=comp_status_col, columns=service_name_col, values='Count').fillna(0)
print(status_pivot.to_string())

print('\n' + '='*80)
print('7. ADDITIONAL INSIGHTS FOR SALES MOTION')
print('='*80)

# Contracts ending soon (within next 6 months)
today = pd.Timestamp.now()
six_months = today + pd.DateOffset(months=6)
ending_soon = df[(df[end_date_col] >= today) & (df[end_date_col] <= six_months)]
print(f'\n7.1 RENEWAL OPPORTUNITIES')
print(f'Contracts ending in next 6 months: {len(ending_soon)}')
if len(ending_soon) > 0:
    renewal_value = ending_soon[total_amount_col].sum()
    print(f'Total value at risk: ${renewal_value:,.2f}')
    print('\nBy Service Name:')
    renewal_by_service = ending_soon.groupby(service_name_col).agg({
        total_amount_col: ['count', 'sum']
    }).round(2)
    print(renewal_by_service.to_string())

# Average contract value by service
print(f'\n7.2 AVERAGE CONTRACT VALUE BY SERVICE')
avg_value = df.groupby(service_name_col)[total_amount_col].agg(['count', 'mean', 'sum']).round(2)
avg_value.columns = ['Count', 'Avg_Value_USD', 'Total_Value_USD']
print(avg_value.to_string())

# Contract duration analysis
df['Contract_Duration_Days'] = (df[end_date_col] - df[start_date_col]).dt.days
print(f'\n7.3 CONTRACT DURATION ANALYSIS')
duration_stats = df.groupby(service_name_col)['Contract_Duration_Days'].agg(['mean', 'min', 'max']).round(0)
duration_stats.columns = ['Avg_Days', 'Min_Days', 'Max_Days']
print(duration_stats.to_string())

# Geographic distribution
print(f'\n7.4 GEOGRAPHIC DISTRIBUTION')
geo_dist = df.groupby([country_col, service_name_col]).size().reset_index(name='Count')
geo_pivot = geo_dist.pivot(index=country_col, columns=service_name_col, values='Count').fillna(0)
print(geo_pivot.to_string())

# Contracts without auto renewal
print(f'\n7.5 UPSELL OPPORTUNITY: CONTRACTS WITHOUT AUTO RENEWAL')
no_auto_renewal = df[~df[auto_renewal_col].astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON'])]
print(f'Contracts without auto renewal: {len(no_auto_renewal)} ({len(no_auto_renewal)/len(df)*100:.2f}%)')
if len(no_auto_renewal) > 0:
    no_renewal_value = no_auto_renewal[total_amount_col].sum()
    print(f'Total value: ${no_renewal_value:,.2f}')
    print('\nBy Service Name:')
    no_renewal_by_service = no_auto_renewal.groupby(service_name_col).agg({
        total_amount_col: ['count', 'sum']
    }).round(2)
    print(no_renewal_by_service.to_string())

print('\n' + '='*80)
print('ANALYSIS COMPLETE')
print('='*80)

# Made with Bob
