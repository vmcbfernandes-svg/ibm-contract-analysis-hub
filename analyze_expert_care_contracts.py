import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import sys
import io

# Set UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

warnings.filterwarnings('ignore')

# File path
file_path = "Contract Base Reports Expert Care Power Storage 03june2026.xlsx"
sheet_name = "Component Details"

print("=" * 80)
print("EXPERT CARE POWER STORAGE CONTRACT ANALYSIS")
print("=" * 80)
print(f"\nReading file: {file_path}")
print(f"Sheet: {sheet_name}\n")

try:
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    print(f"[OK] File loaded successfully")
    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    
    # Display column names with their indices
    print("\n" + "=" * 80)
    print("COLUMN MAPPING")
    print("=" * 80)
    for idx, col in enumerate(df.columns):
        print(f"Column {chr(65 + idx)}: {col}")
    
    # Map columns according to specification
    column_mapping = {
        'Country': df.columns[1] if len(df.columns) > 1 else None,  # Column B
        'Auto Renewal Flag': df.columns[10] if len(df.columns) > 10 else None,  # Column K
        'Brand': df.columns[14] if len(df.columns) > 14 else None,  # Column O
        'Product Family': df.columns[15] if len(df.columns) > 15 else None,  # Column P
        'Machine Type': df.columns[16] if len(df.columns) > 16 else None,  # Column Q
        'Model': df.columns[17] if len(df.columns) > 17 else None,  # Column R
        'Serial Number': df.columns[18] if len(df.columns) > 18 else None,  # Column S
        'EOS Date': df.columns[21] if len(df.columns) > 21 else None,  # Column V
        'Service Name': df.columns[23] if len(df.columns) > 23 else None,  # Column X
        'Service Level': df.columns[24] if len(df.columns) > 24 else None,  # Column Y
        'SLA Type': df.columns[25] if len(df.columns) > 25 else None,  # Column Z
        'L40 Name': df.columns[29] if len(df.columns) > 29 else None,  # Column AD
        'Contract Start Date': df.columns[33] if len(df.columns) > 33 else None,  # Column AH
        'Contract End Date': df.columns[34] if len(df.columns) > 34 else None,  # Column AI
        'Contract Status': df.columns[35] if len(df.columns) > 35 else None,  # Column AJ
        'Total Contract Value': df.columns[37] if len(df.columns) > 37 else None,  # Column AL
    }
    
    print("\n" + "=" * 80)
    print("MAPPED COLUMNS")
    print("=" * 80)
    for key, value in column_mapping.items():
        print(f"{key}: {value}")
    
    # Create working dataframe with mapped columns
    df_work = pd.DataFrame()
    for key, col_name in column_mapping.items():
        if col_name and col_name in df.columns:
            df_work[key] = df[col_name]
    
    # Data cleaning and preparation
    print("\n" + "=" * 80)
    print("DATA CLEANING & PREPARATION")
    print("=" * 80)
    
    initial_count = len(df_work)
    print(f"Initial record count: {initial_count:,}")
    
    # Convert date columns
    date_columns = ['Contract Start Date', 'Contract End Date', 'EOS Date']
    for col in date_columns:
        if col in df_work.columns:
            df_work[col] = pd.to_datetime(df_work[col], errors='coerce')
    
    # Convert Total Contract Value to numeric
    if 'Total Contract Value' in df_work.columns:
        df_work['Total Contract Value'] = pd.to_numeric(df_work['Total Contract Value'], errors='coerce')
    
    # Remove invalid records
    df_clean = df_work.copy()
    
    # Remove records with missing start or end dates
    if 'Contract Start Date' in df_clean.columns and 'Contract End Date' in df_clean.columns:
        df_clean = df_clean.dropna(subset=['Contract Start Date', 'Contract End Date'])
        print(f"After removing missing dates: {len(df_clean):,} records")
    
    # Remove records where end date is before start date
    if 'Contract Start Date' in df_clean.columns and 'Contract End Date' in df_clean.columns:
        df_clean = df_clean[df_clean['Contract End Date'] >= df_clean['Contract Start Date']]
        print(f"After removing invalid date ranges: {len(df_clean):,} records")
    
    # Flag EOS violations
    if 'EOS Date' in df_clean.columns and 'Contract End Date' in df_clean.columns:
        df_clean['EOS_Violation'] = df_clean['Contract End Date'] > df_clean['EOS Date']
        eos_violations = df_clean['EOS_Violation'].sum()
        print(f"EOS violations identified: {eos_violations:,} records")
    
    # Extract year and quarter from Contract Start Date
    if 'Contract Start Date' in df_clean.columns:
        df_clean['Year'] = df_clean['Contract Start Date'].dt.year
        df_clean['Quarter'] = df_clean['Contract Start Date'].dt.quarter
        df_clean['YearQuarter'] = df_clean['Year'].astype(str) + '-Q' + df_clean['Quarter'].astype(str)
    
    # Calculate contract duration in days
    if 'Contract Start Date' in df_clean.columns and 'Contract End Date' in df_clean.columns:
        df_clean['Duration_Days'] = (df_clean['Contract End Date'] - df_clean['Contract Start Date']).dt.days
    
    records_removed = initial_count - len(df_clean)
    print(f"\nTotal records removed: {records_removed:,} ({records_removed/initial_count*100:.1f}%)")
    print(f"Final clean dataset: {len(df_clean):,} records")
    
    # ========================================================================
    # ANALYSIS 1: SIGNINGS TREND
    # ========================================================================
    print("\n" + "=" * 80)
    print("1. CONTRACT SIGNINGS TREND ANALYSIS")
    print("=" * 80)
    
    if 'Service Name' in df_clean.columns and 'YearQuarter' in df_clean.columns:
        signings_by_service = df_clean.groupby(['YearQuarter', 'Service Name']).size().reset_index(name='Signings')
        signings_pivot = signings_by_service.pivot(index='YearQuarter', columns='Service Name', values='Signings').fillna(0)
        
        print("\nSignings by Quarter and Service:")
        print(signings_pivot.to_string())
        
        # Overall trend
        signings_total = df_clean.groupby('YearQuarter').size().reset_index(name='Total_Signings')
        print("\n\nTotal Signings by Quarter:")
        print(signings_total.to_string(index=False))
        
        # Growth analysis
        if len(signings_total) > 1:
            signings_total['Growth_%'] = signings_total['Total_Signings'].pct_change() * 100
            print("\n\nQuarter-over-Quarter Growth:")
            print(signings_total[['YearQuarter', 'Total_Signings', 'Growth_%']].to_string(index=False))
    
    # ========================================================================
    # ANALYSIS 2: REVENUE ANALYSIS
    # ========================================================================
    print("\n" + "=" * 80)
    print("2. REVENUE ANALYSIS (TIME-BASED)")
    print("=" * 80)
    
    if all(col in df_clean.columns for col in ['Total Contract Value', 'Duration_Days', 'Service Name']):
        # Calculate daily revenue rate
        df_clean['Daily_Revenue'] = df_clean['Total Contract Value'] / df_clean['Duration_Days'].replace(0, np.nan)
        
        # For simplicity, aggregate by year-quarter based on contract start
        revenue_by_service = df_clean.groupby(['YearQuarter', 'Service Name'])['Total Contract Value'].sum().reset_index()
        revenue_pivot = revenue_by_service.pivot(index='YearQuarter', columns='Service Name', values='Total Contract Value').fillna(0)
        
        print("\nRevenue by Quarter and Service (USD):")
        print(revenue_pivot.to_string())
        
        # Total revenue by quarter
        revenue_total = df_clean.groupby('YearQuarter')['Total Contract Value'].sum().reset_index()
        revenue_total.columns = ['YearQuarter', 'Total_Revenue_USD']
        print("\n\nTotal Revenue by Quarter:")
        print(revenue_total.to_string(index=False))
        
        # Service comparison
        service_revenue = df_clean.groupby('Service Name')['Total Contract Value'].agg(['sum', 'mean', 'count']).reset_index()
        service_revenue.columns = ['Service Name', 'Total_Revenue', 'Avg_Contract_Value', 'Contract_Count']
        service_revenue = service_revenue.sort_values('Total_Revenue', ascending=False)
        print("\n\nRevenue by Service (Overall):")
        print(service_revenue.to_string(index=False))
    
    # ========================================================================
    # ANALYSIS 3: AUTO RENEWAL ANALYSIS
    # ========================================================================
    print("\n" + "=" * 80)
    print("3. AUTO RENEWAL ANALYSIS")
    print("=" * 80)
    
    if 'Auto Renewal Flag' in df_clean.columns and 'Service Name' in df_clean.columns:
        # Overall auto renewal stats
        total_contracts = len(df_clean)
        auto_renewal_on = df_clean['Auto Renewal Flag'].str.upper().isin(['ON', 'YES', 'TRUE', '1']).sum()
        auto_renewal_pct = (auto_renewal_on / total_contracts * 100) if total_contracts > 0 else 0
        
        print(f"\nOverall Auto Renewal Statistics:")
        print(f"Total Contracts: {total_contracts:,}")
        print(f"Auto Renewal ON: {auto_renewal_on:,}")
        print(f"Auto Renewal %: {auto_renewal_pct:.1f}%")
        
        # By service
        renewal_by_service = df_clean.groupby('Service Name').agg(
            Auto_Renewal_Count=('Auto Renewal Flag', lambda x: (x.str.upper().isin(['ON', 'YES', 'TRUE', '1'])).sum()),
            Total_Count=('Auto Renewal Flag', 'count')
        ).reset_index()
        renewal_by_service['Auto_Renewal_%'] = (renewal_by_service['Auto_Renewal_Count'] / renewal_by_service['Total_Count'] * 100)
        renewal_by_service = renewal_by_service.sort_values('Auto_Renewal_%', ascending=False)
        
        print("\n\nAuto Renewal by Service:")
        print(renewal_by_service.to_string(index=False))
    
    # ========================================================================
    # ANALYSIS 4: SLA (CMSL) PENETRATION
    # ========================================================================
    print("\n" + "=" * 80)
    print("4. SLA (CMSL) PENETRATION ANALYSIS")
    print("=" * 80)
    
    if 'SLA Type' in df_clean.columns and 'Service Name' in df_clean.columns:
        # Overall CMSL stats
        total_contracts = len(df_clean)
        cmsl_contracts = df_clean['SLA Type'].str.upper().str.contains('CMSL', na=False).sum()
        cmsl_pct = (cmsl_contracts / total_contracts * 100) if total_contracts > 0 else 0
        
        print(f"\nOverall CMSL Statistics:")
        print(f"Total Contracts: {total_contracts:,}")
        print(f"CMSL Contracts: {cmsl_contracts:,}")
        print(f"CMSL Penetration %: {cmsl_pct:.1f}%")
        
        # By service
        cmsl_by_service = df_clean.groupby('Service Name').agg(
            CMSL_Count=('SLA Type', lambda x: x.str.upper().str.contains('CMSL', na=False).sum()),
            Total_Count=('SLA Type', 'count')
        ).reset_index()
        cmsl_by_service['CMSL_%'] = (cmsl_by_service['CMSL_Count'] / cmsl_by_service['Total_Count'] * 100)
        cmsl_by_service = cmsl_by_service.sort_values('CMSL_%', ascending=False)
        
        print("\n\nCMSL Penetration by Service:")
        print(cmsl_by_service.to_string(index=False))
    
    # ========================================================================
    # ANALYSIS 5: EOS COMPLIANCE CHECK
    # ========================================================================
    print("\n" + "=" * 80)
    print("5. EOS COMPLIANCE CHECK")
    print("=" * 80)
    
    if 'EOS_Violation' in df_clean.columns:
        total_contracts = len(df_clean)
        eos_violations = df_clean['EOS_Violation'].sum()
        eos_violation_pct = (eos_violations / total_contracts * 100) if total_contracts > 0 else 0
        
        print(f"\nEOS Compliance Summary:")
        print(f"Total Contracts: {total_contracts:,}")
        print(f"EOS Violations: {eos_violations:,}")
        print(f"Violation Rate: {eos_violation_pct:.1f}%")
        
        if eos_violations > 0 and 'Total Contract Value' in df_clean.columns:
            revenue_at_risk = df_clean[df_clean['EOS_Violation']]['Total Contract Value'].sum()
            print(f"Revenue at Risk (USD): ${revenue_at_risk:,.2f}")
        
        # By service
        if 'Service Name' in df_clean.columns:
            eos_by_service = df_clean.groupby('Service Name').agg(
                EOS_Violations=('EOS_Violation', 'sum'),
                Total_Count=('EOS_Violation', 'count')
            ).reset_index()
            eos_by_service['Violation_%'] = (eos_by_service['EOS_Violations'] / eos_by_service['Total_Count'] * 100)
            eos_by_service = eos_by_service.sort_values('Violation_%', ascending=False)
            
            print("\n\nEOS Violations by Service:")
            print(eos_by_service.to_string(index=False))
    
    # ========================================================================
    # ADVANCED INSIGHTS
    # ========================================================================
    print("\n" + "=" * 80)
    print("6. ADVANCED INSIGHTS & RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n📊 KEY FINDINGS:")
    
    # Service mix analysis
    if 'Service Name' in df_clean.columns and 'Total Contract Value' in df_clean.columns:
        service_mix = df_clean.groupby('Service Name').agg(
            Total_Revenue=('Total Contract Value', 'sum'),
            Contract_Count=('Total Contract Value', 'count')
        ).reset_index()
        service_mix['Avg_Value'] = service_mix['Total_Revenue'] / service_mix['Contract_Count']
        service_mix = service_mix.sort_values('Total_Revenue', ascending=False)
        
        print("\n1. SERVICE MIX ANALYSIS:")
        print(service_mix.to_string(index=False))
    
    # Contract status distribution
    if 'Contract Status' in df_clean.columns:
        status_dist = df_clean['Contract Status'].value_counts()
        print("\n2. CONTRACT STATUS DISTRIBUTION:")
        for status, count in status_dist.items():
            pct = (count / len(df_clean) * 100)
            print(f"   {status}: {count:,} ({pct:.1f}%)")
    
    # Geographic distribution
    if 'Country' in df_clean.columns:
        country_dist = df_clean['Country'].value_counts().head(10)
        print("\n3. TOP 10 COUNTRIES BY CONTRACT COUNT:")
        for country, count in country_dist.items():
            pct = (count / len(df_clean) * 100)
            print(f"   {country}: {count:,} ({pct:.1f}%)")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    
    # Save summary to file
    output_file = "Expert_Care_Analysis_Summary.txt"
    with open(output_file, 'w') as f:
        f.write("EXPERT CARE POWER STORAGE CONTRACT ANALYSIS SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Records Analyzed: {len(df_clean):,}\n")
        f.write("=" * 80 + "\n")
    
    print(f"\n✓ Summary saved to: {output_file}")

except FileNotFoundError:
    print(f"❌ Error: File '{file_path}' not found!")
    print("Please ensure the file is in the current directory.")
except Exception as e:
    print(f"❌ Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()

# Made with Bob
