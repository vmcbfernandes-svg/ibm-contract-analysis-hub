import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# File paths for all 5 Geo files
files = {
    'NA': 'Contract Base Reports HWMA NA 02June2026.xlsx',
    'LA': 'Contract Base Reports HWMA LA 02june2026.xlsx',
    'Europe': 'Contract Base Reports HWMA Europe 02June2026.xlsx',
    'APAC': 'Contract Base Reports HWMA APAC 02June2026.xlsx',
    'MEA': 'Contract Base Reports HWMA MEA 02June2026.xlsx'
}

print("="*80)
print("WORLDWIDE CONTRACT ANALYSIS - HWMA")
print("="*80)
print(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "="*80)

# Column mapping (Excel columns to names)
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
    'AJ': 'Contract Status',
    'AL': 'Total Contract Value (USD)'
}

# Convert Excel column letters to indices (0-based)
def col_letter_to_index(letter):
    result = 0
    for char in letter:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1

# Load and combine all files
all_data = []
geo_summary = {}

print("\n1. LOADING DATA FROM ALL GEOS")
print("-" * 80)

for geo, filepath in files.items():
    try:
        print(f"\nLoading {geo}...")
        df = pd.read_excel(filepath, sheet_name='Component Details', header=None)
        
        # Extract only the required columns
        selected_cols = {}
        for col_letter, col_name in column_mapping.items():
            col_idx = col_letter_to_index(col_letter)
            if col_idx < len(df.columns):
                selected_cols[col_name] = df.iloc[:, col_idx]
        
        geo_df = pd.DataFrame(selected_cols)
        
        # Remove header row (first row contains column names)
        geo_df = geo_df.iloc[1:].reset_index(drop=True)
        
        # Add Geo identifier
        geo_df['Geo'] = geo
        
        geo_summary[geo] = len(geo_df)
        all_data.append(geo_df)
        print(f"  [OK] Loaded {len(geo_df):,} records from {geo}")
        
    except Exception as e:
        print(f"  [ERROR] Error loading {geo}: {str(e)}")

# Combine all data
print("\n2. COMBINING ALL DATASETS")
print("-" * 80)
df_ww = pd.concat(all_data, ignore_index=True)
print(f"\n[OK] Combined dataset created: {len(df_ww):,} total records")
print("\nRecords by Geo:")
for geo, count in geo_summary.items():
    print(f"  {geo}: {count:,}")

# Data Cleaning and Preparation
print("\n3. DATA CLEANING AND PREPARATION")
print("-" * 80)

# Convert date columns
date_columns = ['EOS Date', 'Service Start Date', 'Service End Date']
for col in date_columns:
    df_ww[col] = pd.to_datetime(df_ww[col], errors='coerce')

# Convert Total Contract Value to numeric
df_ww['Total Contract Value (USD)'] = pd.to_numeric(df_ww['Total Contract Value (USD)'], errors='coerce')

# Remove duplicates based on Serial Number + Service Start Date + Service Name
print("\nRemoving duplicates...")
initial_count = len(df_ww)
df_ww['unique_key'] = (df_ww['Serial Number'].astype(str) + '_' + 
                        df_ww['Service Start Date'].astype(str) + '_' + 
                        df_ww['Service Name'].astype(str))
df_ww = df_ww.drop_duplicates(subset='unique_key', keep='first')
duplicates_removed = initial_count - len(df_ww)
print(f"  [OK] Removed {duplicates_removed:,} duplicate records")
print(f"  [OK] Final dataset: {len(df_ww):,} unique contracts")

# Create EOS validation flags
print("\nCreating EOS validation flags...")
df_ww['EOS_Violation_Start'] = (df_ww['Service Start Date'] > df_ww['EOS Date']) & df_ww['EOS Date'].notna()
df_ww['EOS_Violation_End'] = (df_ww['Service End Date'] > df_ww['EOS Date']) & df_ww['EOS Date'].notna()
df_ww['EOS_Violation_Any'] = df_ww['EOS_Violation_Start'] | df_ww['EOS_Violation_End']

eos_violations = df_ww['EOS_Violation_Any'].sum()
print(f"  [OK] Identified {eos_violations:,} contracts with EOS violations ({eos_violations/len(df_ww)*100:.1f}%)")

# Extract Year and Quarter from Service Start Date
df_ww['Start_Year'] = df_ww['Service Start Date'].dt.year
df_ww['Start_Quarter'] = df_ww['Service Start Date'].dt.quarter
df_ww['Start_YearQuarter'] = df_ww['Start_Year'].astype(str) + '-Q' + df_ww['Start_Quarter'].astype(str)

# Identify Active and Future contracts
df_ww['Is_Active'] = df_ww['Contract Status'].str.upper().str.contains('ACTIVE', na=False)
df_ww['Is_Future'] = df_ww['Contract Status'].str.upper().str.contains('FUTURE', na=False)

print("\n" + "="*80)
print("4. CONTRACT SIGNINGS ANALYSIS")
print("="*80)

# Contract Signings by Year/Quarter
signings = df_ww.groupby(['Start_YearQuarter', 'Service Name']).size().reset_index(name='Contract_Count')
signings_pivot = signings.pivot_table(index='Start_YearQuarter', columns='Service Name', values='Contract_Count', fill_value=0)
signings_pivot['Total'] = signings_pivot.sum(axis=1)
signings_pivot = signings_pivot.sort_index()

print("\nContract Signings by Year/Quarter and Service Name:")
print(signings_pivot.to_string())

# Total signings by service
print("\n\nTotal Contract Signings by Service Name:")
service_signings = df_ww.groupby('Service Name').size().sort_values(ascending=False)
for service, count in service_signings.items():
    print(f"  {service}: {count:,}")

print("\n" + "="*80)
print("5. REVENUE ANALYSIS (TIME-BASED)")
print("="*80)

# Calculate contract duration in days
df_ww['Contract_Duration_Days'] = (df_ww['Service End Date'] - df_ww['Service Start Date']).dt.days

# Function to allocate revenue across quarters
def allocate_revenue_by_quarter(row):
    if pd.isna(row['Service Start Date']) or pd.isna(row['Service End Date']) or pd.isna(row['Total Contract Value (USD)']):
        return []
    
    start_date = row['Service Start Date']
    end_date = row['Service End Date']
    total_value = row['Total Contract Value (USD)']
    duration_days = (end_date - start_date).days
    
    if duration_days <= 0:
        return []
    
    daily_rate = total_value / duration_days
    
    allocations = []
    current_date = start_date
    
    while current_date <= end_date:
        quarter_start = pd.Timestamp(year=current_date.year, month=((current_date.quarter - 1) * 3) + 1, day=1)
        quarter_end = (quarter_start + pd.DateOffset(months=3)) - pd.Timedelta(days=1)
        
        period_start = max(current_date, quarter_start)
        period_end = min(end_date, quarter_end)
        
        if period_start <= period_end:
            days_in_period = (period_end - period_start).days + 1
            revenue_in_period = daily_rate * days_in_period
            
            allocations.append({
                'Year': period_start.year,
                'Quarter': period_start.quarter,
                'YearQuarter': f"{period_start.year}-Q{period_start.quarter}",
                'Service Name': row['Service Name'],
                'Revenue': revenue_in_period
            })
        
        current_date = quarter_end + pd.Timedelta(days=1)
    
    return allocations

print("\nAllocating revenue across time periods...")
revenue_allocations = []
for idx, row in df_ww.iterrows():
    allocations = allocate_revenue_by_quarter(row)
    revenue_allocations.extend(allocations)

df_revenue = pd.DataFrame(revenue_allocations)

if len(df_revenue) > 0:
    revenue_by_period = df_revenue.groupby(['YearQuarter', 'Service Name'])['Revenue'].sum().reset_index()
    revenue_pivot = revenue_by_period.pivot_table(index='YearQuarter', columns='Service Name', values='Revenue', fill_value=0)
    revenue_pivot['Total'] = revenue_pivot.sum(axis=1)
    revenue_pivot = revenue_pivot.sort_index()
    
    print("\nRevenue by Year/Quarter and Service Name (USD):")
    print(revenue_pivot.to_string())
    
    print("\n\nTotal Revenue by Service Name (USD):")
    service_revenue = df_revenue.groupby('Service Name')['Revenue'].sum().sort_values(ascending=False)
    for service, revenue in service_revenue.items():
        print(f"  {service}: ${revenue:,.2f}")
    
    print(f"\n\nTotal Worldwide Revenue: ${df_revenue['Revenue'].sum():,.2f}")
else:
    print("\n[WARNING] No revenue data available for allocation")

print("\n" + "="*80)
print("6. AUTO-RENEWAL ANALYSIS")
print("="*80)

# Auto-renewal analysis
auto_renewal_on = df_ww['Auto Renewal Flag'].str.upper().str.contains('ON|YES|TRUE|Y', na=False)
total_contracts = len(df_ww)
auto_renewal_count = auto_renewal_on.sum()
auto_renewal_pct = (auto_renewal_count / total_contracts * 100) if total_contracts > 0 else 0

print(f"\nOverall Auto-Renewal Statistics:")
print(f"  Total Contracts: {total_contracts:,}")
print(f"  Auto-Renewal ON: {auto_renewal_count:,} ({auto_renewal_pct:.1f}%)")
print(f"  Auto-Renewal OFF: {total_contracts - auto_renewal_count:,} ({100 - auto_renewal_pct:.1f}%)")

print("\n\nAuto-Renewal by Service Name:")
auto_renewal_by_service = df_ww.groupby('Service Name').agg({
    'Auto Renewal Flag': lambda x: (x.str.upper().str.contains('ON|YES|TRUE|Y', na=False)).sum(),
    'Serial Number': 'count'
}).rename(columns={'Auto Renewal Flag': 'Auto_Renewal_ON', 'Serial Number': 'Total_Contracts'})
auto_renewal_by_service['Auto_Renewal_Pct'] = (auto_renewal_by_service['Auto_Renewal_ON'] / auto_renewal_by_service['Total_Contracts'] * 100)
auto_renewal_by_service = auto_renewal_by_service.sort_values('Auto_Renewal_Pct', ascending=False)

for service, row in auto_renewal_by_service.iterrows():
    print(f"  {service}:")
    print(f"    Total: {int(row['Total_Contracts']):,} | Auto-Renewal ON: {int(row['Auto_Renewal_ON']):,} ({row['Auto_Renewal_Pct']:.1f}%)")

print("\n" + "="*80)
print("7. CMSL SLA ANALYSIS")
print("="*80)

# CMSL SLA analysis
cmsl_contracts = df_ww['SLA Type'].str.upper().str.contains('CMSL', na=False)
cmsl_count = cmsl_contracts.sum()
cmsl_pct = (cmsl_count / total_contracts * 100) if total_contracts > 0 else 0

print(f"\nOverall CMSL SLA Statistics:")
print(f"  Total Contracts: {total_contracts:,}")
print(f"  CMSL Contracts: {cmsl_count:,} ({cmsl_pct:.1f}%)")
print(f"  Non-CMSL Contracts: {total_contracts - cmsl_count:,} ({100 - cmsl_pct:.1f}%)")

print("\n\nCMSL SLA by Service Name:")
cmsl_by_service = df_ww.groupby('Service Name').agg({
    'SLA Type': lambda x: (x.str.upper().str.contains('CMSL', na=False)).sum(),
    'Serial Number': 'count'
}).rename(columns={'SLA Type': 'CMSL_Contracts', 'Serial Number': 'Total_Contracts'})
cmsl_by_service['CMSL_Pct'] = (cmsl_by_service['CMSL_Contracts'] / cmsl_by_service['Total_Contracts'] * 100)
cmsl_by_service = cmsl_by_service.sort_values('CMSL_Pct', ascending=False)

for service, row in cmsl_by_service.iterrows():
    print(f"  {service}:")
    print(f"    Total: {int(row['Total_Contracts']):,} | CMSL: {int(row['CMSL_Contracts']):,} ({row['CMSL_Pct']:.1f}%)")

print("\n" + "="*80)
print("8. EOS COMPLIANCE ANALYSIS (CRITICAL)")
print("="*80)

# Overall EOS violations
eos_start_violations = df_ww['EOS_Violation_Start'].sum()
eos_end_violations = df_ww['EOS_Violation_End'].sum()
eos_any_violations = df_ww['EOS_Violation_Any'].sum()

print(f"\nOverall EOS Violation Statistics:")
print(f"  Total Contracts: {total_contracts:,}")
print(f"  Start Date after EOS: {eos_start_violations:,} ({eos_start_violations/total_contracts*100:.1f}%)")
print(f"  End Date after EOS: {eos_end_violations:,} ({eos_end_violations/total_contracts*100:.1f}%)")
print(f"  Any EOS Violation: {eos_any_violations:,} ({eos_any_violations/total_contracts*100:.1f}%)")

# EOS violations by Service Name
print("\n\nEOS Violations by Service Name:")
eos_by_service = df_ww.groupby('Service Name').agg({
    'EOS_Violation_Start': 'sum',
    'EOS_Violation_End': 'sum',
    'EOS_Violation_Any': 'sum',
    'Serial Number': 'count'
}).rename(columns={'Serial Number': 'Total_Contracts'})
eos_by_service['Violation_Pct'] = (eos_by_service['EOS_Violation_Any'] / eos_by_service['Total_Contracts'] * 100)
eos_by_service = eos_by_service.sort_values('EOS_Violation_Any', ascending=False)

for service, row in eos_by_service.iterrows():
    if row['EOS_Violation_Any'] > 0:
        print(f"  {service}:")
        print(f"    Total: {int(row['Total_Contracts']):,} | Violations: {int(row['EOS_Violation_Any']):,} ({row['Violation_Pct']:.1f}%)")
        print(f"    Start Violations: {int(row['EOS_Violation_Start']):,} | End Violations: {int(row['EOS_Violation_End']):,}")

# EOS violations by Product Family
print("\n\nEOS Violations by Product Family (Top 10):")
eos_by_product = df_ww[df_ww['EOS_Violation_Any']].groupby('Product Family').size().sort_values(ascending=False).head(10)
for product, count in eos_by_product.items():
    print(f"  {product}: {count:,}")

# EOS violations by Geo
print("\n\nEOS Violations by Geo:")
eos_by_geo = df_ww.groupby('Geo').agg({
    'EOS_Violation_Any': 'sum',
    'Serial Number': 'count'
}).rename(columns={'Serial Number': 'Total_Contracts'})
eos_by_geo['Violation_Pct'] = (eos_by_geo['EOS_Violation_Any'] / eos_by_geo['Total_Contracts'] * 100)
eos_by_geo = eos_by_geo.sort_values('EOS_Violation_Any', ascending=False)

for geo, row in eos_by_geo.iterrows():
    print(f"  {geo}: {int(row['EOS_Violation_Any']):,} violations ({row['Violation_Pct']:.1f}% of {int(row['Total_Contracts']):,} contracts)")

# EOS violations by Country (Top 10)
print("\n\nEOS Violations by Country (Top 10):")
eos_by_country = df_ww[df_ww['EOS_Violation_Any']].groupby('Country').size().sort_values(ascending=False).head(10)
for country, count in eos_by_country.items():
    print(f"  {country}: {count:,}")

# EOS violations by Contract Status
print("\n\nEOS Violations by Contract Status:")
eos_by_status = df_ww[df_ww['EOS_Violation_Any']].groupby('Contract Status').size().sort_values(ascending=False)
for status, count in eos_by_status.items():
    print(f"  {status}: {count:,}")

# Revenue associated with EOS violations
eos_violation_revenue = df_ww[df_ww['EOS_Violation_Any']]['Total Contract Value (USD)'].sum()
total_revenue = df_ww['Total Contract Value (USD)'].sum()
eos_revenue_pct = (eos_violation_revenue / total_revenue * 100) if total_revenue > 0 else 0

print(f"\n\nRevenue Associated with EOS Violations:")
print(f"  Total Revenue: ${total_revenue:,.2f}")
print(f"  EOS Violation Revenue: ${eos_violation_revenue:,.2f} ({eos_revenue_pct:.1f}%)")

print("\n" + "="*80)
print("9. ADDITIONAL BUSINESS INSIGHTS")
print("="*80)

# Services with highest growth in signings
print("\n\n[GROWTH] SERVICES WITH HIGHEST GROWTH IN SIGNINGS")
print("-" * 80)
signings_by_year = df_ww.groupby(['Start_Year', 'Service Name']).size().reset_index(name='Count')
signings_pivot_year = signings_by_year.pivot_table(index='Service Name', columns='Start_Year', values='Count', fill_value=0)
if len(signings_pivot_year.columns) >= 2:
    latest_year = signings_pivot_year.columns[-1]
    previous_year = signings_pivot_year.columns[-2]
    signings_pivot_year['Growth'] = signings_pivot_year[latest_year] - signings_pivot_year[previous_year]
    signings_pivot_year['Growth_Pct'] = ((signings_pivot_year[latest_year] - signings_pivot_year[previous_year]) / 
                                          signings_pivot_year[previous_year] * 100).replace([np.inf, -np.inf], 0)
    growth_services = signings_pivot_year.sort_values('Growth', ascending=False).head(5)
    print(f"\nTop 5 Services by Growth ({previous_year} to {latest_year}):")
    for service, row in growth_services.iterrows():
        print(f"  {service}: {int(row[previous_year])} -> {int(row[latest_year])} (+{int(row['Growth'])}, {row['Growth_Pct']:.1f}%)")

# Revenue concentration by Service Name
print("\n\n[REVENUE] REVENUE CONCENTRATION BY SERVICE NAME")
print("-" * 80)
revenue_by_service = df_ww.groupby('Service Name')['Total Contract Value (USD)'].sum().sort_values(ascending=False)
total_revenue = revenue_by_service.sum()
revenue_by_service_pct = (revenue_by_service / total_revenue * 100)
print("\nTop Services by Revenue:")
for i, (service, revenue) in enumerate(revenue_by_service.head(5).items(), 1):
    print(f"  {i}. {service}: ${revenue:,.2f} ({revenue_by_service_pct[service]:.1f}%)")

# Low Auto-Renew penetration
print("\n\n[AUTO-RENEWAL] LOW AUTO-RENEWAL PENETRATION (RENEWAL OPPORTUNITY)")
print("-" * 80)
low_auto_renewal = auto_renewal_by_service[auto_renewal_by_service['Auto_Renewal_Pct'] < 50].sort_values('Total_Contracts', ascending=False)
print("\nServices with <50% Auto-Renewal (sorted by contract count):")
for service, row in low_auto_renewal.head(5).iterrows():
    opportunity = int(row['Total_Contracts']) - int(row['Auto_Renewal_ON'])
    print(f"  {service}: {row['Auto_Renewal_Pct']:.1f}% ({int(row['Auto_Renewal_ON']):,}/{int(row['Total_Contracts']):,})")
    print(f"    -> Opportunity: {opportunity:,} contracts")

# CMSL adoption gaps
print("\n\n[CMSL] CMSL ADOPTION GAPS (UPSELL POTENTIAL)")
print("-" * 80)
low_cmsl = cmsl_by_service[cmsl_by_service['CMSL_Pct'] < 30].sort_values('Total_Contracts', ascending=False)
print("\nServices with <30% CMSL Adoption (sorted by contract count):")
for service, row in low_cmsl.head(5).iterrows():
    opportunity = int(row['Total_Contracts']) - int(row['CMSL_Contracts'])
    print(f"  {service}: {row['CMSL_Pct']:.1f}% ({int(row['CMSL_Contracts']):,}/{int(row['Total_Contracts']):,})")
    print(f"    -> Opportunity: {opportunity:,} contracts")

# Contracts approaching EOS but still active
print("\n\n[EOS-APPROACHING] CONTRACTS APPROACHING EOS (IMMEDIATE RISK/OPPORTUNITY)")
print("-" * 80)
today = pd.Timestamp.now()
df_ww['Days_to_EOS'] = (df_ww['EOS Date'] - today).dt.days
approaching_eos = df_ww[(df_ww['Days_to_EOS'] > 0) & (df_ww['Days_to_EOS'] <= 180) & (df_ww['Is_Active'])]
print(f"\nActive contracts with EOS within 180 days: {len(approaching_eos):,}")
if len(approaching_eos) > 0:
    eos_by_service_approaching = approaching_eos.groupby('Service Name').size().sort_values(ascending=False)
    print("\nBreakdown by Service Name:")
    for service, count in eos_by_service_approaching.head(5).items():
        print(f"  {service}: {count:,}")

# Contracts violating EOS (compliance risk)
print("\n\n[EOS-VIOLATION] CONTRACTS VIOLATING EOS (COMPLIANCE & REVENUE LEAKAGE RISK)")
print("-" * 80)
print(f"\nTotal contracts with EOS violations: {eos_any_violations:,}")
print(f"Revenue at risk: ${eos_violation_revenue:,.2f}")
print("\nTop offending segments:")
print("\n  By Service:")
for service, row in eos_by_service.head(3).iterrows():
    if row['EOS_Violation_Any'] > 0:
        print(f"    {service}: {int(row['EOS_Violation_Any']):,} violations")
print("\n  By Geo:")
for geo, row in eos_by_geo.head(3).iterrows():
    if row['EOS_Violation_Any'] > 0:
        print(f"    {geo}: {int(row['EOS_Violation_Any']):,} violations")

# Upsell opportunities by Service Level
print("\n\n[UPSELL] UPSELL OPPORTUNITIES BY SERVICE LEVEL")
print("-" * 80)
service_level_dist = df_ww.groupby(['Service Name', 'Service Level']).size().reset_index(name='Count')
print("\nService Level Distribution by Service Name:")
for service in df_ww['Service Name'].unique()[:5]:
    service_data = service_level_dist[service_level_dist['Service Name'] == service].sort_values('Count', ascending=False)
    if len(service_data) > 0:
        print(f"\n  {service}:")
        for _, row in service_data.head(3).iterrows():
            print(f"    {row['Service Level']}: {int(row['Count']):,}")

# Geo/Country performance differences
print("\n\n[GEO-PERFORMANCE] GEO/COUNTRY PERFORMANCE DIFFERENCES")
print("-" * 80)
geo_performance = df_ww.groupby('Geo').agg({
    'Serial Number': 'count',
    'Total Contract Value (USD)': 'sum',
    'Auto Renewal Flag': lambda x: (x.str.upper().str.contains('ON|YES|TRUE|Y', na=False)).sum(),
    'SLA Type': lambda x: (x.str.upper().str.contains('CMSL', na=False)).sum()
}).rename(columns={
    'Serial Number': 'Total_Contracts',
    'Total Contract Value (USD)': 'Total_Revenue',
    'Auto Renewal Flag': 'Auto_Renewal_Count',
    'SLA Type': 'CMSL_Count'
})
geo_performance['Avg_Contract_Value'] = geo_performance['Total_Revenue'] / geo_performance['Total_Contracts']
geo_performance['Auto_Renewal_Pct'] = (geo_performance['Auto_Renewal_Count'] / geo_performance['Total_Contracts'] * 100)
geo_performance['CMSL_Pct'] = (geo_performance['CMSL_Count'] / geo_performance['Total_Contracts'] * 100)
geo_performance = geo_performance.sort_values('Total_Revenue', ascending=False)

print("\nGeo Performance Summary:")
for geo, row in geo_performance.iterrows():
    print(f"\n  {geo}:")
    print(f"    Contracts: {int(row['Total_Contracts']):,}")
    print(f"    Revenue: ${row['Total_Revenue']:,.2f}")
    print(f"    Avg Contract Value: ${row['Avg_Contract_Value']:,.2f}")
    print(f"    Auto-Renewal: {row['Auto_Renewal_Pct']:.1f}%")
    print(f"    CMSL Adoption: {row['CMSL_Pct']:.1f}%")

# Data quality issues
print("\n\n[DATA-QUALITY] DATA QUALITY ISSUES")
print("-" * 80)
missing_data = {
    'Country': df_ww['Country'].isna().sum(),
    'Auto Renewal Flag': df_ww['Auto Renewal Flag'].isna().sum(),
    'Service Name': df_ww['Service Name'].isna().sum(),
    'Service Start Date': df_ww['Service Start Date'].isna().sum(),
    'Service End Date': df_ww['Service End Date'].isna().sum(),
    'Total Contract Value': df_ww['Total Contract Value (USD)'].isna().sum(),
    'EOS Date': df_ww['EOS Date'].isna().sum()
}
print("\nMissing Data Summary:")
for field, count in missing_data.items():
    if count > 0:
        pct = count / len(df_ww) * 100
        print(f"  {field}: {count:,} ({pct:.1f}%)")

print("\n" + "="*80)
print("10. TOP 5 GLOBAL OPPORTUNITIES")
print("="*80)

print("\n1. AUTO-RENEWAL EXPANSION")
print("   -> Target: Services with low auto-renewal rates")
print("   -> Potential: Convert manual renewals to auto-renewal")
for service, row in low_auto_renewal.head(3).iterrows():
    opportunity = int(row['Total_Contracts']) - int(row['Auto_Renewal_ON'])
    print(f"     * {service}: {opportunity:,} contracts")

print("\n2. CMSL UPSELL")
print("   -> Target: Non-CMSL contracts in key services")
print("   -> Potential: Upgrade to CMSL SLA")
for service, row in low_cmsl.head(3).iterrows():
    opportunity = int(row['Total_Contracts']) - int(row['CMSL_Contracts'])
    print(f"     * {service}: {opportunity:,} contracts")

print("\n3. EOS COMPLIANCE & MIGRATION")
print(f"   -> Target: {eos_any_violations:,} contracts violating EOS")
print(f"   -> Revenue at Risk: ${eos_violation_revenue:,.2f}")
print("   -> Action: Migrate to supported hardware or negotiate exceptions")

print("\n4. PROACTIVE EOS MANAGEMENT")
print(f"   -> Target: {len(approaching_eos):,} active contracts approaching EOS (within 180 days)")
print("   -> Action: Engage customers early for hardware refresh or migration")

print("\n5. GEO-SPECIFIC GROWTH")
print("   -> Target: Underperforming geos in key metrics")
print("   -> Action: Share best practices from high-performing geos")
for geo, row in geo_performance.iterrows():
    if row['Auto_Renewal_Pct'] < 40 or row['CMSL_Pct'] < 20:
        print(f"     * {geo}: Auto-Renewal {row['Auto_Renewal_Pct']:.1f}%, CMSL {row['CMSL_Pct']:.1f}%")

print("\n" + "="*80)
print("11. STRATEGIC RECOMMENDATIONS")
print("="*80)

print("\n[SALES-MOTION] RECOMMENDATIONS:")
print("  1. Implement auto-renewal campaigns for services with <50% adoption")
print("  2. Create EOS migration playbooks for proactive customer engagement")
print("  3. Develop geo-specific strategies based on performance gaps")
print("  4. Establish quarterly EOS compliance reviews")
print("  5. Train sales teams on CMSL value proposition for upsell")

print("\n[UPSELL-CROSSSELL] RECOMMENDATIONS:")
print("  1. Bundle CMSL upgrades with contract renewals")
print("  2. Offer hardware refresh programs for EOS-approaching contracts")
print("  3. Create service level upgrade paths with clear ROI")
print("  4. Develop product family-specific service packages")
print("  5. Leverage high-performing geos as reference accounts")

print("\n[REVENUE-PROTECTION] RECOMMENDATIONS:")
print(f"  1. URGENT: Address {eos_any_violations:,} EOS violations (${eos_violation_revenue:,.2f} at risk)")
print("  2. Implement automated EOS monitoring and alerting")
print("  3. Create exception process for post-EOS support")
print("  4. Establish data quality improvement program")
print("  5. Develop compliance dashboard for executive visibility")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nTotal Contracts Analyzed: {len(df_ww):,}")
print(f"Total Revenue: ${df_ww['Total Contract Value (USD)'].sum():,.2f}")
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "="*80)

# Save the consolidated dataset
output_file = 'WW_Consolidated_Contract_Data.xlsx'
print(f"\nSaving consolidated dataset to {output_file}...")
df_ww.to_excel(output_file, index=False)
print(f"[OK] Dataset saved successfully")

print("\n[OK] Analysis complete! Check the output above for detailed insights.")

# Made with Bob
