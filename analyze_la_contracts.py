import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Read the Excel file
file_path = "Contract Base Reports HWMA LA 02june2026.xlsx"
print(f"Reading file: {file_path}")

# Read the Component Details sheet
df = pd.read_excel(file_path, sheet_name="Component Details")

print(f"\nTotal records loaded: {len(df)}")
print(f"Columns in dataset: {df.columns.tolist()}")

# Map column letters to actual column names
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

# Get actual column names by index (Excel columns are 0-indexed in pandas)
# Column B = index 1, K = index 10, etc.
excel_to_index = {
    'B': 1, 'K': 10, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
    'V': 21, 'X': 23, 'Y': 24, 'Z': 25, 'AD': 29, 'AH': 33, 'AI': 34,
    'AJ': 35, 'AL': 37
}

# Create a mapping of our names to actual column names
actual_columns = {}
for letter, name in column_mapping.items():
    idx = excel_to_index[letter]
    if idx < len(df.columns):
        actual_columns[name] = df.columns[idx]
        print(f"{letter} ({name}): {df.columns[idx]}")

# Rename columns for easier access
rename_dict = {v: k for k, v in actual_columns.items()}
df = df.rename(columns=rename_dict)

# Convert date columns to datetime
date_columns = ['Service Start Date', 'Service End Date', 'EOS Date']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Convert amount to numeric
if 'Comp Total Amount USD' in df.columns:
    df['Comp Total Amount USD'] = pd.to_numeric(df['Comp Total Amount USD'], errors='coerce')

print("\n" + "="*80)
print("DATA QUALITY CHECK")
print("="*80)

print(f"\nService Start Date - Valid dates: {df['Service Start Date'].notna().sum()}")
print(f"Service End Date - Valid dates: {df['Service End Date'].notna().sum()}")
print(f"EOS Date - Valid dates: {df['EOS Date'].notna().sum()}")
print(f"Comp Total Amount USD - Valid amounts: {df['Comp Total Amount USD'].notna().sum()}")

# Extract Year and Quarter from Service Start Date
df['Start Year'] = df['Service Start Date'].dt.year
df['Start Quarter'] = df['Service Start Date'].dt.quarter
df['Start YearQuarter'] = df['Start Year'].astype(str) + '-Q' + df['Start Quarter'].astype(str)

# Extract Year and Quarter from Service End Date
df['End Year'] = df['Service End Date'].dt.year
df['End Quarter'] = df['Service End Date'].dt.quarter
df['End YearQuarter'] = df['End Year'].astype(str) + '-Q' + df['End Quarter'].astype(str)

print("\n" + "="*80)
print("ANALYSIS 1: CONTRACT SIGNINGS BY YEAR/QUARTER AND SERVICE NAME")
print("="*80)

# Filter valid start dates
df_valid_start = df[df['Service Start Date'].notna()].copy()

# Group by Year-Quarter and Service Name
signings = df_valid_start.groupby(['Start YearQuarter', 'Service Name']).size().reset_index(name='Count')
signings_pivot = signings.pivot(index='Start YearQuarter', columns='Service Name', values='Count').fillna(0)

print("\nContract Signings by Year-Quarter and Service Name:")
print(signings_pivot.to_string())

# Total by Year-Quarter
print("\n\nTotal Signings by Year-Quarter:")
total_signings = df_valid_start.groupby('Start YearQuarter').size().reset_index(name='Total Contracts')
print(total_signings.to_string(index=False))

print("\n" + "="*80)
print("ANALYSIS 2: REVENUE BY YEAR/QUARTER AND SERVICE NAME")
print("="*80)

# For revenue calculation, we need to consider the contract period
# Revenue recognition: distribute total amount across contract period

def calculate_quarterly_revenue(row):
    """Calculate revenue for each quarter the contract is active"""
    if pd.isna(row['Service Start Date']) or pd.isna(row['Service End Date']) or pd.isna(row['Comp Total Amount USD']):
        return []
    
    start_date = row['Service Start Date']
    end_date = row['Service End Date']
    total_amount = row['Comp Total Amount USD']
    
    # Calculate total days in contract
    total_days = (end_date - start_date).days
    if total_days <= 0:
        return []
    
    # Daily rate
    daily_rate = total_amount / total_days
    
    # Generate all quarters in the contract period
    quarters = []
    current = start_date
    
    while current <= end_date:
        year = current.year
        quarter = (current.month - 1) // 3 + 1
        quarter_start = pd.Timestamp(year=year, month=(quarter-1)*3+1, day=1)
        
        # Calculate quarter end
        if quarter == 4:
            quarter_end = pd.Timestamp(year=year, month=12, day=31)
        else:
            next_quarter_start = pd.Timestamp(year=year, month=quarter*3+1, day=1)
            quarter_end = next_quarter_start - pd.Timedelta(days=1)
        
        # Calculate overlap
        overlap_start = max(start_date, quarter_start)
        overlap_end = min(end_date, quarter_end)
        
        if overlap_start <= overlap_end:
            days_in_quarter = (overlap_end - overlap_start).days + 1
            revenue = daily_rate * days_in_quarter
            quarters.append({
                'YearQuarter': f"{year}-Q{quarter}",
                'Revenue': revenue,
                'Service Name': row['Service Name']
            })
        
        # Move to next quarter
        if quarter == 4:
            current = pd.Timestamp(year=year+1, month=1, day=1)
        else:
            current = pd.Timestamp(year=year, month=quarter*3+1, day=1)
    
    return quarters

# Calculate revenue for all contracts
print("\nCalculating quarterly revenue distribution...")
all_revenue_records = []
for idx, row in df.iterrows():
    quarters = calculate_quarterly_revenue(row)
    all_revenue_records.extend(quarters)

if all_revenue_records:
    revenue_df = pd.DataFrame(all_revenue_records)
    revenue_summary = revenue_df.groupby(['YearQuarter', 'Service Name'])['Revenue'].sum().reset_index()
    revenue_pivot = revenue_summary.pivot(index='YearQuarter', columns='Service Name', values='Revenue').fillna(0)
    
    print("\nRevenue by Year-Quarter and Service Name (USD):")
    print(revenue_pivot.to_string())
    
    print("\n\nTotal Revenue by Year-Quarter (USD):")
    total_revenue = revenue_df.groupby('YearQuarter')['Revenue'].sum().reset_index()
    total_revenue['Revenue'] = total_revenue['Revenue'].apply(lambda x: f"${x:,.2f}")
    print(total_revenue.to_string(index=False))
else:
    print("\nNo valid revenue data found.")

print("\n" + "="*80)
print("ANALYSIS 3: AUTO RENEWAL FLAG ANALYSIS")
print("="*80)

if 'Auto Renewal Flag' in df.columns:
    # Overall auto renewal stats
    total_contracts = len(df)
    auto_renewal_on = df['Auto Renewal Flag'].fillna('').astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON'])
    auto_renewal_count = auto_renewal_on.sum()
    auto_renewal_pct = (auto_renewal_count / total_contracts * 100) if total_contracts > 0 else 0
    
    print(f"\nOverall Auto Renewal Statistics:")
    print(f"Total Contracts: {total_contracts}")
    print(f"Auto Renewal ON: {auto_renewal_count} ({auto_renewal_pct:.2f}%)")
    print(f"Auto Renewal OFF: {total_contracts - auto_renewal_count} ({100-auto_renewal_pct:.2f}%)")
    
    # By Service Name
    print("\n\nAuto Renewal by Service Name:")
    service_auto_renewal = df.groupby('Service Name').apply(
        lambda x: pd.Series({
            'Total': len(x),
            'Auto Renewal ON': x['Auto Renewal Flag'].fillna('').astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON']).sum()
        })
    ).reset_index()
    service_auto_renewal['Auto Renewal OFF'] = service_auto_renewal['Total'] - service_auto_renewal['Auto Renewal ON']
    service_auto_renewal['% Auto Renewal ON'] = (service_auto_renewal['Auto Renewal ON'] / service_auto_renewal['Total'] * 100).round(2)
    
    print(service_auto_renewal.to_string(index=False))
else:
    print("\nAuto Renewal Flag column not found.")

print("\n" + "="*80)
print("ANALYSIS 4: CMSL SLA TYPE ANALYSIS")
print("="*80)

if 'SLA Type' in df.columns:
    # Overall CMSL stats
    total_contracts = len(df)
    cmsl_contracts = df['SLA Type'].fillna('').astype(str).str.upper().str.contains('CMSL')
    cmsl_count = cmsl_contracts.sum()
    cmsl_pct = (cmsl_count / total_contracts * 100) if total_contracts > 0 else 0
    
    print(f"\nOverall CMSL SLA Type Statistics:")
    print(f"Total Contracts: {total_contracts}")
    print(f"CMSL Contracts: {cmsl_count} ({cmsl_pct:.2f}%)")
    print(f"Non-CMSL Contracts: {total_contracts - cmsl_count} ({100-cmsl_pct:.2f}%)")
    
    # By Service Name
    print("\n\nCMSL SLA Type by Service Name:")
    service_cmsl = df.groupby('Service Name').apply(
        lambda x: pd.Series({
            'Total': len(x),
            'CMSL': x['SLA Type'].fillna('').astype(str).str.upper().str.contains('CMSL').sum()
        })
    ).reset_index()
    service_cmsl['Non-CMSL'] = service_cmsl['Total'] - service_cmsl['CMSL']
    service_cmsl['% CMSL'] = (service_cmsl['CMSL'] / service_cmsl['Total'] * 100).round(2)
    
    print(service_cmsl.to_string(index=False))
    
    # Show unique SLA Types
    print("\n\nUnique SLA Types in dataset:")
    unique_sla = df['SLA Type'].value_counts()
    print(unique_sla.to_string())
else:
    print("\nSLA Type column not found.")

print("\n" + "="*80)
print("ANALYSIS 5: EOS DATE VALIDATION")
print("="*80)

# Check for contracts extending beyond EOS date
if 'EOS Date' in df.columns and 'Service End Date' in df.columns:
    df_with_eos = df[(df['EOS Date'].notna()) & (df['Service End Date'].notna())].copy()
    contracts_beyond_eos = df_with_eos[df_with_eos['Service End Date'] > df_with_eos['EOS Date']]
    
    print(f"\nTotal contracts with EOS Date: {len(df_with_eos)}")
    print(f"Contracts extending beyond EOS Date: {len(contracts_beyond_eos)}")
    
    if len(contracts_beyond_eos) > 0:
        print(f"Percentage: {len(contracts_beyond_eos)/len(df_with_eos)*100:.2f}%")
        print("\nWARNING: These contracts extend beyond machine EOS date!")
        print("\nSample of contracts beyond EOS (first 10):")
        cols_to_show = ['Country', 'Service Name', 'Machine Type', 'Model', 'Serial Number', 
                       'EOS Date', 'Service End Date', 'Comp Status']
        available_cols = [col for col in cols_to_show if col in contracts_beyond_eos.columns]
        print(contracts_beyond_eos[available_cols].head(10).to_string(index=False))
    else:
        print("OK: All contracts end before or on EOS date.")
else:
    print("\nEOS Date or Service End Date column not found.")

print("\n" + "="*80)
print("ANALYSIS 6: CONTRACT STATUS ANALYSIS")
print("="*80)

if 'Comp Status' in df.columns:
    print("\nContract Status Distribution:")
    status_dist = df['Comp Status'].value_counts()
    print(status_dist.to_string())
    
    print("\n\nContract Status by Service Name:")
    status_by_service = pd.crosstab(df['Service Name'], df['Comp Status'], margins=True)
    print(status_by_service.to_string())
else:
    print("\nComp Status column not found.")

print("\n" + "="*80)
print("ANALYSIS 7: ADDITIONAL INSIGHTS FOR SALES MOTION")
print("="*80)

# 1. Contracts expiring soon (within next 6 months)
print("\n1. CONTRACTS EXPIRING IN NEXT 6 MONTHS (Renewal Opportunities):")
today = pd.Timestamp.now()
six_months = today + pd.DateOffset(months=6)

expiring_soon = df[(df['Service End Date'] >= today) & (df['Service End Date'] <= six_months)].copy()
print(f"\nTotal contracts expiring in next 6 months: {len(expiring_soon)}")

if len(expiring_soon) > 0:
    expiring_by_service = expiring_soon.groupby('Service Name').agg({
        'Comp Total Amount USD': ['count', 'sum']
    }).round(2)
    expiring_by_service.columns = ['Count', 'Total Value (USD)']
    print("\nBy Service Name:")
    print(expiring_by_service.to_string())
    
    # Check auto renewal status
    expiring_no_auto = expiring_soon[~expiring_soon['Auto Renewal Flag'].fillna('').astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON'])]
    print(f"\nContracts expiring WITHOUT auto-renewal: {len(expiring_no_auto)}")
    print(f"   Potential revenue at risk: ${expiring_no_auto['Comp Total Amount USD'].sum():,.2f}")

# 2. Top countries by contract value
print("\n\n2. TOP COUNTRIES BY CONTRACT VALUE:")
if 'Country' in df.columns:
    country_value = df.groupby('Country').agg({
        'Comp Total Amount USD': ['count', 'sum']
    }).round(2)
    country_value.columns = ['Contract Count', 'Total Value (USD)']
    country_value = country_value.sort_values('Total Value (USD)', ascending=False)
    print(country_value.head(10).to_string())

# 3. Service mix analysis
print("\n\n3. SERVICE MIX ANALYSIS:")
service_mix = df.groupby('Service Name').agg({
    'Comp Total Amount USD': ['count', 'sum', 'mean']
}).round(2)
service_mix.columns = ['Contract Count', 'Total Value (USD)', 'Avg Contract Value (USD)']
service_mix['% of Total Contracts'] = (service_mix['Contract Count'] / len(df) * 100).round(2)
service_mix['% of Total Revenue'] = (service_mix['Total Value (USD)'] / service_mix['Total Value (USD)'].sum() * 100).round(2)
print(service_mix.to_string())

# 4. Brand and Product Family analysis
print("\n\n4. TOP BRANDS BY CONTRACT VALUE:")
if 'Brand' in df.columns:
    brand_value = df.groupby('Brand').agg({
        'Comp Total Amount USD': ['count', 'sum']
    }).round(2)
    brand_value.columns = ['Contract Count', 'Total Value (USD)']
    brand_value = brand_value.sort_values('Total Value (USD)', ascending=False)
    print(brand_value.head(10).to_string())

print("\n\n5. TOP PRODUCT FAMILIES BY CONTRACT VALUE:")
if 'Product Family' in df.columns:
    product_value = df.groupby('Product Family').agg({
        'Comp Total Amount USD': ['count', 'sum']
    }).round(2)
    product_value.columns = ['Contract Count', 'Total Value (USD)']
    product_value = product_value.sort_values('Total Value (USD)', ascending=False)
    print(product_value.head(10).to_string())

# 6. Contract duration analysis
print("\n\n6. CONTRACT DURATION ANALYSIS:")
df_with_dates = df[(df['Service Start Date'].notna()) & (df['Service End Date'].notna())].copy()
df_with_dates['Contract Duration (Days)'] = (df_with_dates['Service End Date'] - df_with_dates['Service Start Date']).dt.days
df_with_dates['Contract Duration (Years)'] = df_with_dates['Contract Duration (Days)'] / 365.25

duration_stats = df_with_dates.groupby('Service Name')['Contract Duration (Years)'].agg(['count', 'mean', 'min', 'max']).round(2)
duration_stats.columns = ['Count', 'Avg Duration (Years)', 'Min Duration (Years)', 'Max Duration (Years)']
print(duration_stats.to_string())

# 7. Upsell opportunities - contracts without auto-renewal
print("\n\n7. UPSELL OPPORTUNITY: CONTRACTS WITHOUT AUTO-RENEWAL")
no_auto_renewal = df[~df['Auto Renewal Flag'].fillna('').astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON'])].copy()
print(f"\nTotal contracts without auto-renewal: {len(no_auto_renewal)}")
print(f"Total value: ${no_auto_renewal['Comp Total Amount USD'].sum():,.2f}")

upsell_by_service = no_auto_renewal.groupby('Service Name').agg({
    'Comp Total Amount USD': ['count', 'sum']
}).round(2)
upsell_by_service.columns = ['Count', 'Total Value (USD)']
print("\nBy Service Name:")
print(upsell_by_service.to_string())

# 8. Non-CMSL contracts (potential upgrade opportunity)
print("\n\n8. UPSELL OPPORTUNITY: NON-CMSL CONTRACTS (Potential CMSL Upgrades)")
if 'SLA Type' in df.columns:
    non_cmsl = df[~df['SLA Type'].fillna('').astype(str).str.upper().str.contains('CMSL')].copy()
    print(f"\nTotal non-CMSL contracts: {len(non_cmsl)}")
    print(f"Total value: ${non_cmsl['Comp Total Amount USD'].sum():,.2f}")
    
    non_cmsl_by_service = non_cmsl.groupby('Service Name').agg({
        'Comp Total Amount USD': ['count', 'sum']
    }).round(2)
    non_cmsl_by_service.columns = ['Count', 'Total Value (USD)']
    print("\nBy Service Name:")
    print(non_cmsl_by_service.to_string())

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nReport generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Made with Bob
