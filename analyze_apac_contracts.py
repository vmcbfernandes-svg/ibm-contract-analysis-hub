import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the Excel file
file_path = "Contract Base Reports HWMA APAC 02June2026.xlsx"
print(f"Loading {file_path}...")

# Read the Component Details sheet
df = pd.read_excel(file_path, sheet_name="Component Details")

print(f"Total records loaded: {len(df)}")
print(f"\nColumns in the dataset: {df.columns.tolist()}")

# Map column letters to actual column names
# Column B - Country name
# Column K - Auto Renewal Flag
# Column O - Brand
# Column P - Product Family
# Column Q - Machine Type
# Column R - Model
# Column S - Serial Number
# Column V - EOS Date
# Column X - Service Name
# Column Y - Service level
# Column Z - SLA Type
# Column AD - L40 Name
# Column AH - Service Start Date
# Column AI - Service End Date
# Column AJ - Comp Status
# Column AL - Comp Total Amount USD

# Get column names by index (0-based)
country_col = df.columns[1]  # Column B
auto_renewal_col = df.columns[10]  # Column K
brand_col = df.columns[14]  # Column O
product_family_col = df.columns[15]  # Column P
machine_type_col = df.columns[16]  # Column Q
model_col = df.columns[17]  # Column R
serial_col = df.columns[18]  # Column S
eos_date_col = df.columns[21]  # Column V
service_name_col = df.columns[23]  # Column X
service_level_col = df.columns[24]  # Column Y
sla_type_col = df.columns[25]  # Column Z
l40_name_col = df.columns[29]  # Column AD
service_start_col = df.columns[33]  # Column AH
service_end_col = df.columns[34]  # Column AI
comp_status_col = df.columns[35]  # Column AJ
comp_total_usd_col = df.columns[37]  # Column AL

print(f"\nMapped columns:")
print(f"Country: {country_col}")
print(f"Auto Renewal: {auto_renewal_col}")
print(f"Service Name: {service_name_col}")
print(f"Service Start: {service_start_col}")
print(f"Service End: {service_end_col}")
print(f"Comp Status: {comp_status_col}")
print(f"Comp Total USD: {comp_total_usd_col}")
print(f"SLA Type: {sla_type_col}")
print(f"EOS Date: {eos_date_col}")

# Convert date columns to datetime
df[service_start_col] = pd.to_datetime(df[service_start_col], errors='coerce')
df[service_end_col] = pd.to_datetime(df[service_end_col], errors='coerce')
df[eos_date_col] = pd.to_datetime(df[eos_date_col], errors='coerce')

# Convert amount to numeric
df[comp_total_usd_col] = pd.to_numeric(df[comp_total_usd_col], errors='coerce')

# Create Year and Quarter columns for contract start
df['Start_Year'] = df[service_start_col].dt.year
df['Start_Quarter'] = df[service_start_col].dt.quarter
df['Start_YearQuarter'] = df['Start_Year'].astype(str) + '-Q' + df['Start_Quarter'].astype(str)

# Create Year and Quarter columns for contract end
df['End_Year'] = df[service_end_col].dt.year
df['End_Quarter'] = df[service_end_col].dt.quarter
df['End_YearQuarter'] = df['End_Year'].astype(str) + '-Q' + df['End_Quarter'].astype(str)

print("\n" + "="*80)
print("ANALYSIS REPORT: HWMA APAC CONTRACT DATA")
print("="*80)

# ============================================================================
# 1. CONTRACT SIGNINGS BY YEAR/QUARTER SPLIT BY SERVICE NAME
# ============================================================================
print("\n1. CONTRACT SIGNINGS BY YEAR/QUARTER (Split by Service Name)")
print("-" * 80)

signings = df[df[service_start_col].notna()].groupby(['Start_YearQuarter', service_name_col]).size().reset_index(name='Count')
signings_pivot = signings.pivot(index='Start_YearQuarter', columns=service_name_col, values='Count').fillna(0)
signings_pivot['Total'] = signings_pivot.sum(axis=1)
signings_pivot = signings_pivot.sort_index()

print(signings_pivot.to_string())
print(f"\nTotal Signings: {signings_pivot['Total'].sum():.0f}")

# ============================================================================
# 2. TOTAL REVENUE BY YEAR/QUARTER
# ============================================================================
print("\n\n2. TOTAL REVENUE BY YEAR/QUARTER (Split by Service Name)")
print("-" * 80)
print("Note: Revenue allocated based on contract start date")

revenue_start = df[df[service_start_col].notna()].groupby(['Start_YearQuarter', service_name_col])[comp_total_usd_col].sum().reset_index()
revenue_start_pivot = revenue_start.pivot(index='Start_YearQuarter', columns=service_name_col, values=comp_total_usd_col).fillna(0)
revenue_start_pivot['Total'] = revenue_start_pivot.sum(axis=1)
revenue_start_pivot = revenue_start_pivot.sort_index()

print("\nRevenue by Contract Start Date:")
print(revenue_start_pivot.to_string())
print(f"\nTotal Revenue: ${revenue_start_pivot['Total'].sum():,.2f}")

# ============================================================================
# 3. AUTO RENEWAL FLAG ANALYSIS
# ============================================================================
print("\n\n3. AUTO RENEWAL FLAG ANALYSIS (Split by Service Name)")
print("-" * 80)

auto_renewal_analysis = df.groupby([service_name_col, auto_renewal_col]).size().reset_index(name='Count')
total_by_service = df.groupby(service_name_col).size().reset_index(name='Total')

auto_renewal_summary = auto_renewal_analysis.merge(total_by_service, on=service_name_col)
auto_renewal_summary['Percentage'] = (auto_renewal_summary['Count'] / auto_renewal_summary['Total'] * 100).round(2)

print("\nAuto Renewal Distribution:")
for service in auto_renewal_summary[service_name_col].unique():
    service_data = auto_renewal_summary[auto_renewal_summary[service_name_col] == service]
    print(f"\n{service}:")
    for _, row in service_data.iterrows():
        print(f"  {row[auto_renewal_col]}: {row['Count']} contracts ({row['Percentage']:.2f}%)")

# Summary of Auto Renewal ON
auto_on = df[df[auto_renewal_col].astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON'])]
print(f"\n\nTotal Contracts with Auto Renewal ON: {len(auto_on)} ({len(auto_on)/len(df)*100:.2f}% of total)")

auto_on_by_service = auto_on.groupby(service_name_col).size().reset_index(name='Count')
total_by_service_dict = df.groupby(service_name_col).size().to_dict()
auto_on_by_service['Total'] = auto_on_by_service[service_name_col].map(total_by_service_dict)
auto_on_by_service['Percentage'] = (auto_on_by_service['Count'] / auto_on_by_service['Total'] * 100).round(2)

print("\nAuto Renewal ON by Service Name:")
print(auto_on_by_service.to_string(index=False))

# ============================================================================
# 4. CMSL SLA TYPE ANALYSIS
# ============================================================================
print("\n\n4. CMSL SLA TYPE ANALYSIS (Split by Service Name)")
print("-" * 80)

cmsl_contracts = df[df[sla_type_col].astype(str).str.upper().str.contains('CMSL', na=False)]
print(f"\nTotal Contracts with CMSL SLA Type: {len(cmsl_contracts)} ({len(cmsl_contracts)/len(df)*100:.2f}% of total)")

cmsl_by_service = cmsl_contracts.groupby(service_name_col).size().reset_index(name='CMSL_Count')
cmsl_by_service['Total'] = cmsl_by_service[service_name_col].map(total_by_service_dict)
cmsl_by_service['Percentage'] = (cmsl_by_service['CMSL_Count'] / cmsl_by_service['Total'] * 100).round(2)

print("\nCMSL Contracts by Service Name:")
print(cmsl_by_service.to_string(index=False))

# All SLA Types distribution
print("\n\nAll SLA Types Distribution:")
sla_distribution = df.groupby([service_name_col, sla_type_col]).size().reset_index(name='Count')
for service in sla_distribution[service_name_col].unique():
    service_data = sla_distribution[sla_distribution[service_name_col] == service]
    print(f"\n{service}:")
    for _, row in service_data.iterrows():
        total = total_by_service_dict.get(service, 1)
        pct = (row['Count'] / total * 100)
        print(f"  {row[sla_type_col]}: {row['Count']} ({pct:.2f}%)")

# ============================================================================
# 5. EOS DATE ANALYSIS
# ============================================================================
print("\n\n5. EOS DATE ANALYSIS")
print("-" * 80)

# Contracts extending beyond EOS date
contracts_beyond_eos = df[(df[service_end_col].notna()) & 
                          (df[eos_date_col].notna()) & 
                          (df[service_end_col] > df[eos_date_col])]

print(f"\nContracts extending beyond EOS date: {len(contracts_beyond_eos)}")
if len(contracts_beyond_eos) > 0:
    print("\nBreakdown by Service Name:")
    beyond_eos_by_service = contracts_beyond_eos.groupby(service_name_col).size().reset_index(name='Count')
    print(beyond_eos_by_service.to_string(index=False))
    
    print("\nSample contracts extending beyond EOS:")
    sample_cols = [country_col, service_name_col, machine_type_col, model_col, 
                   eos_date_col, service_end_col, comp_status_col]
    print(contracts_beyond_eos[sample_cols].head(10).to_string(index=False))

# ============================================================================
# 6. CONTRACT STATUS ANALYSIS
# ============================================================================
print("\n\n6. CONTRACT STATUS ANALYSIS")
print("-" * 80)

status_distribution = df.groupby([comp_status_col, service_name_col]).size().reset_index(name='Count')
status_pivot = status_distribution.pivot(index=comp_status_col, columns=service_name_col, values='Count').fillna(0)
status_pivot['Total'] = status_pivot.sum(axis=1)

print("\nContract Status Distribution:")
print(status_pivot.to_string())

# ============================================================================
# 7. ADDITIONAL INSIGHTS FOR SALES MOTION
# ============================================================================
print("\n\n7. ADDITIONAL INSIGHTS FOR SALES MOTION & REVENUE OPTIMIZATION")
print("="*80)

# 7.1 Contracts expiring soon (next 6 months)
print("\n7.1 RENEWAL OPPORTUNITIES - Contracts Expiring in Next 6 Months")
print("-" * 80)
today = pd.Timestamp.now()
six_months = today + pd.DateOffset(months=6)

expiring_soon = df[(df[service_end_col] >= today) & (df[service_end_col] <= six_months)]
print(f"\nTotal contracts expiring in next 6 months: {len(expiring_soon)}")
print(f"Total revenue at risk: ${expiring_soon[comp_total_usd_col].sum():,.2f}")

expiring_by_service = expiring_soon.groupby(service_name_col).agg({
    comp_total_usd_col: ['count', 'sum']
}).reset_index()
expiring_by_service.columns = ['Service Name', 'Contract Count', 'Total Revenue']
print("\nBy Service Name:")
print(expiring_by_service.to_string(index=False))

# Expiring without auto-renewal
expiring_no_auto = expiring_soon[~expiring_soon[auto_renewal_col].astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1', 'ON'])]
print(f"\nContracts expiring WITHOUT auto-renewal: {len(expiring_no_auto)}")
print(f"Revenue at risk (no auto-renewal): ${expiring_no_auto[comp_total_usd_col].sum():,.2f}")

# 7.2 Top countries by contract value
print("\n\n7.2 TOP COUNTRIES BY CONTRACT VALUE")
print("-" * 80)
country_revenue = df.groupby(country_col)[comp_total_usd_col].sum().sort_values(ascending=False).head(10)
print(country_revenue.to_string())

# 7.3 Average contract value by service
print("\n\n7.3 AVERAGE CONTRACT VALUE BY SERVICE NAME")
print("-" * 80)
avg_contract_value = df.groupby(service_name_col)[comp_total_usd_col].agg(['mean', 'median', 'count']).round(2)
avg_contract_value.columns = ['Average', 'Median', 'Count']
print(avg_contract_value.to_string())

# 7.4 Product Family Analysis
print("\n\n7.4 TOP PRODUCT FAMILIES BY CONTRACT COUNT")
print("-" * 80)
product_family_counts = df.groupby(product_family_col).size().sort_values(ascending=False).head(10)
print(product_family_counts.to_string())

# 7.5 Brand Analysis
print("\n\n7.5 BRAND DISTRIBUTION")
print("-" * 80)
brand_distribution = df.groupby(brand_col).agg({
    comp_total_usd_col: ['count', 'sum']
}).reset_index()
brand_distribution.columns = ['Brand', 'Contract Count', 'Total Revenue']
brand_distribution = brand_distribution.sort_values('Total Revenue', ascending=False)
print(brand_distribution.to_string(index=False))

# 7.6 Service Level Analysis
print("\n\n7.6 SERVICE LEVEL DISTRIBUTION")
print("-" * 80)
service_level_dist = df.groupby([service_name_col, service_level_col]).size().reset_index(name='Count')
for service in service_level_dist[service_name_col].unique():
    service_data = service_level_dist[service_level_dist[service_name_col] == service]
    print(f"\n{service}:")
    for _, row in service_data.iterrows():
        print(f"  {row[service_level_col]}: {row['Count']}")

# 7.7 Contract Duration Analysis
print("\n\n7.7 CONTRACT DURATION ANALYSIS")
print("-" * 80)
df['Contract_Duration_Days'] = (df[service_end_col] - df[service_start_col]).dt.days
df['Contract_Duration_Years'] = df['Contract_Duration_Days'] / 365.25

duration_stats = df.groupby(service_name_col)['Contract_Duration_Years'].agg(['mean', 'median', 'min', 'max']).round(2)
duration_stats.columns = ['Avg Years', 'Median Years', 'Min Years', 'Max Years']
print(duration_stats.to_string())

# 7.8 Upcoming EOS machines (next 12 months)
print("\n\n7.8 MACHINES REACHING EOS IN NEXT 12 MONTHS")
print("-" * 80)
twelve_months = today + pd.DateOffset(months=12)
eos_soon = df[(df[eos_date_col] >= today) & (df[eos_date_col] <= twelve_months)]
print(f"\nMachines reaching EOS in next 12 months: {len(eos_soon)}")

if len(eos_soon) > 0:
    eos_by_product = eos_soon.groupby(product_family_col).size().sort_values(ascending=False).head(10)
    print("\nTop Product Families reaching EOS:")
    print(eos_by_product.to_string())
    
    # Check if these have active contracts
    eos_with_active = eos_soon[eos_soon[comp_status_col].astype(str).str.upper().str.contains('ACTIVE', na=False)]
    print(f"\nMachines with ACTIVE contracts reaching EOS: {len(eos_with_active)}")
    print("These are UPSELL opportunities for hardware refresh!")

print("\n" + "="*80)
print("END OF ANALYSIS REPORT")
print("="*80)

# Save summary to file
with open('apac_analysis_output.txt', 'w') as f:
    f.write("HWMA APAC CONTRACT ANALYSIS SUMMARY\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total Contracts: {len(df)}\n")
    f.write(f"Total Revenue: ${df[comp_total_usd_col].sum():,.2f}\n")
    f.write(f"Contracts with Auto Renewal: {len(auto_on)} ({len(auto_on)/len(df)*100:.2f}%)\n")
    f.write(f"Contracts with CMSL SLA: {len(cmsl_contracts)} ({len(cmsl_contracts)/len(df)*100:.2f}%)\n")
    f.write(f"Contracts expiring in 6 months: {len(expiring_soon)}\n")
    f.write(f"Revenue at risk (6 months): ${expiring_soon[comp_total_usd_col].sum():,.2f}\n")
    f.write(f"Machines reaching EOS in 12 months: {len(eos_soon)}\n")

print("\nAnalysis complete! Summary saved to 'apac_analysis_output.txt'")

# Made with Bob
