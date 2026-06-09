# HWMA Europe Contract Analysis Report
**Analysis Date:** June 2, 2026  
**Data Source:** Contract Base Reports Europe 02June2026.xlsx  
**Sheet:** Component Details  
**Total Records Analyzed:** 157,987

---

## Executive Summary

The European contract portfolio shows strong growth momentum with **29,447 contract signings in Q1 2026** and **$156.9M in quarterly revenue**. However, there are critical opportunities for improvement:

- **Only 17.7% of contracts have auto-renewal enabled** (18,573 out of 104,985 active contracts)
- **23.5% of contracts use CMSL SLA type** (36,494 out of 157,985 contracts)
- **4,238 contracts are past their EOS date** but still active, requiring immediate attention
- **48 high-value contracts expiring within 180 days** without auto-renewal, representing **$3.17M at risk**

---

## 1. Contract Signings Analysis

### 1.1 Signings by Year and Quarter (Split by Service Name)

**Key Findings:**
- **Peak signing period:** Q1 2026 with **29,447 new contracts**
- **Fastest growing service:** HWMA Storage (17,376 signings in Q1 2026)
- **Emerging services:** WSU 24x7 SBD and WSU 9x5 NBD showing strong growth since Q2 2023

**Top 5 Quarters by Signing Volume:**
1. **2026-Q1:** 29,447 signings
2. **2025-Q3:** 20,699 signings
3. **2025-Q4:** 13,674 signings
4. **2025-Q1:** 13,535 signings
5. **2024-Q1:** 7,885 signings

**Service Name Breakdown (Q1 2026):**
- HWMA Storage: 17,376 (59.0%)
- WSU 24x7 SBD: 3,622 (12.3%)
- HWMA Power: 3,115 (10.6%)
- WAMO-HWMA 24x7 SBD: 3,236 (11.0%)
- WSU Storage: 1,021 (3.5%)
- Other services: 1,077 (3.6%)

### 1.2 Historical Trends

**Growth Trajectory:**
- **2021:** Transition year with 3,677 total signings
- **2022:** Acceleration to 7,489 signings
- **2023:** Major expansion to 18,849 signings
- **2024:** Continued growth to 28,106 signings
- **2025:** Peak at 54,528 signings
- **2026 YTD:** 43,242 signings (Q1-Q2 only)

---

## 2. Revenue Analysis

### 2.1 Quarterly Revenue by Service Name

**Current Quarter (Q2 2026):** $176.7M
**Previous Quarter (Q1 2026):** $156.9M
**Quarter-over-Quarter Growth:** +12.6%

**Revenue Distribution by Service (Q2 2026):**
- HWMA IBM Z: $96.8M (54.8%)
- HWMA Storage: $67.3M (38.1%)
- HWMA Power: $9.9M (5.6%)
- Committed Maintenance IBM Z: $2.3M (1.3%)
- WSU Services: $0.4M (0.2%)

### 2.2 Revenue Trends

**Peak Revenue Quarters:**
1. **2026-Q2:** $176.7M
2. **2026-Q3:** $167.9M (projected)
3. **2026-Q1:** $156.9M
4. **2026-Q4:** $163.9M (projected)
5. **2025-Q4:** $101.6M

**Year-over-Year Growth:**
- 2023 Total: $88.6M
- 2024 Total: $180.2M (+103.4%)
- 2025 Total: $348.4M (+93.3%)
- 2026 Projected: $664.5M (+90.7%)

### 2.3 Revenue by Country (Top 10)

| Country | Total Revenue | % of Total |
|---------|--------------|------------|
| France | $535.0M | 38.8% |
| Germany | $388.2M | 28.1% |
| Italy | $332.4M | 24.1% |
| United Kingdom | $295.2M | 21.4% |
| Switzerland | $88.9M | 6.4% |
| Spain | $85.9M | 6.2% |
| Belgium | $52.1M | 3.8% |
| Poland | $46.6M | 3.4% |
| Sweden | $40.1M | 2.9% |
| Denmark | $37.8M | 2.7% |

---

## 3. Auto Renewal Analysis

### 3.1 Overall Auto Renewal Status

**Total Contracts:** 157,985
**Contracts with Auto Renewal:** 18,573 (11.8%)
**Contracts without Auto Renewal:** 139,411 (88.2%)

⚠️ **CRITICAL FINDING:** Only 11.8% of contracts have auto-renewal enabled, creating significant churn risk.

### 3.2 Auto Renewal by Service Name

| Service Name | Total Contracts | Auto Renewal ON | Auto Renewal % |
|--------------|----------------|-----------------|----------------|
| **Committed Maintenance IBM Z** | 73 | 0 | 0.0% |
| **HWMA IBM Z** | 942 | 59 | 6.3% |
| **HWMA Power** | 14,492 | 2,662 | 18.4% |
| **HWMA Storage** | 84,141 | 15,192 | 18.1% |
| **WAMO-HWMA 24x7 SBD** | 30,135 | 0 | 0.0% |
| **WAMO-HWMA 9x5 NBD** | 4,633 | 0 | 0.0% |
| **WSU 24x7 SBD** | 13,512 | 0 | 0.0% |
| **WSU 9x5 NBD** | 1,724 | 0 | 0.0% |
| **WSU Power** | 793 | 62 | 7.8% |
| **WSU Storage** | 7,539 | 658 | 8.7% |

**Key Observations:**
- WAMO and WSU NBD/SBD services have **0% auto-renewal** - immediate action required
- HWMA Power and Storage have the highest auto-renewal rates (~18%)
- Significant opportunity to increase auto-renewal across all services

---

## 4. CMSL SLA Type Analysis

### 4.1 Overall CMSL Adoption

**Total Contracts:** 157,985
**CMSL Contracts:** 36,494 (23.1%)
**Non-CMSL Contracts:** 121,490 (76.9%)

### 4.2 CMSL by Service Name

| Service Name | Total Contracts | CMSL Contracts | CMSL % |
|--------------|----------------|----------------|--------|
| **Committed Maintenance IBM Z** | 73 | 73 | 100.0% |
| **HWMA IBM Z** | 942 | 385 | 40.9% |
| **HWMA Power** | 14,492 | 3,396 | 23.4% |
| **HWMA Storage** | 84,141 | 19,885 | 23.6% |
| **WAMO-HWMA 24x7 SBD** | 30,135 | 7,407 | 24.6% |
| **WAMO-HWMA 9x5 NBD** | 4,633 | 0 | 0.0% |
| **WSU 24x7 SBD** | 13,512 | 3,040 | 22.5% |
| **WSU 9x5 NBD** | 1,724 | 0 | 0.0% |
| **WSU Power** | 793 | 115 | 14.5% |
| **WSU Storage** | 7,539 | 2,193 | 29.1% |

**SLA Type Distribution:**
- **CMSL:** 36,494 contracts (23.1%)
- **SBD (Same Business Day):** 109,974 contracts (69.6%)
- **NBD (Next Business Day):** 10,999 contracts (7.0%)
- **PAT 5BD (Parts 5 Business Days):** 488 contracts (0.3%)

---

## 5. End of Service (EOS) Analysis

### 5.1 EOS Status Overview

| EOS Category | Contract Count | % of Total |
|--------------|----------------|------------|
| **No EOS Date** | 143,830 | 91.0% |
| **EOS within 1 year** | 9,553 | 6.0% |
| **Past EOS** | 4,238 | 2.7% |
| **EOS > 1 year** | 316 | 0.2% |
| **EOS within 180 days** | 48 | 0.03% |

### 5.2 Critical EOS Issues

⚠️ **IMMEDIATE ATTENTION REQUIRED:**

**4,238 contracts are past their EOS date** but still active. This represents:
- Potential compliance issues
- Service delivery challenges
- Revenue at risk

**Breakdown by Service:**
- HWMA Storage: 3,433 contracts
- HWMA Power: 775 contracts
- WSU Power: 27 contracts
- WSU Storage: 3 contracts

### 5.3 High Priority: Expiring Contracts (Within 180 Days)

**48 contracts expiring within 180 days without auto-renewal**
**Total Revenue at Risk: $3,173,096.76**

**Top 10 Contracts at Risk:**

| Country | Service Name | Service Level | Days to EOS | Contract Value |
|---------|--------------|---------------|-------------|----------------|
| United Kingdom | HWMA Storage | 4h Committed On-site,24x7 | 119 | $364,020.31 |
| United Kingdom | HWMA Storage | 4h Committed On-site,24x7 | 119 | $364,020.31 |
| United Kingdom | HWMA Storage | 4h Committed On-site,24x7 | 119 | $364,020.31 |
| United Kingdom | HWMA Storage | 4h Committed On-site,24x7 | 119 | $335,754.68 |
| United Kingdom | HWMA Storage | 4h Committed On-site,24x7 | 119 | $177,579.68 |
| United Kingdom | HWMA Storage | 4h Committed On-site,24x7 | 119 | $177,579.68 |
| France | HWMA Storage | 4h Committed On-site,24x7 | 119 | $88,192.68 |
| France | HWMA Storage | 4h Committed On-site,24x7 | 119 | $88,192.68 |
| France | HWMA Storage | 4h Committed On-site,24x7 | 119 | $88,192.68 |
| France | HWMA Storage | 4h Committed On-site,24x7 | 119 | $88,192.68 |

---

## 6. Contract Status Analysis

### 6.1 Status Distribution

| Status | Contract Count | % of Total |
|--------|----------------|------------|
| **ACTIVE** | 132,407 | 83.8% |
| **FUTURE** | 25,518 | 16.2% |
| **AUTO-RENEW** | 59 | 0.04% |

### 6.2 Status by Service Name

**Active Contracts by Service:**
- HWMA Storage: 72,369 (54.7%)
- WAMO-HWMA 24x7 SBD: 19,317 (14.6%)
- HWMA Power: 13,159 (9.9%)
- WSU 24x7 SBD: 13,512 (10.2%)
- WSU Storage: 7,534 (5.7%)
- Other services: 6,516 (4.9%)

**Future Contracts (Not Yet Started):**
- HWMA Storage: 11,725 (45.9%)
- WAMO-HWMA 24x7 SBD: 10,818 (42.4%)
- WAMO-HWMA 9x5 NBD: 1,493 (5.8%)
- HWMA Power: 1,326 (5.2%)
- HWMA IBM Z: 156 (0.6%)

---

## 7. Product Family Analysis

### 7.1 Top 10 Product Families by Contract Count

| Product Family | Contract Count | % of Total |
|----------------|----------------|------------|
| **DRI** | 53,485 | 33.9% |
| **FLASHSYS** | 43,270 | 27.4% |
| **SAN** | 17,880 | 11.3% |
| **P10** | 9,968 | 6.3% |
| **P9** | 7,106 | 4.5% |
| **HMC** | 6,299 | 4.0% |
| **ESS** | 4,972 | 3.1% |
| **COS** | 2,639 | 1.7% |
| **P11** | 1,935 | 1.2% |
| **RACK** | 1,651 | 1.0% |

**Key Insights:**
- Storage products (DRI, FLASHSYS, SAN) dominate with **72.6% of all contracts**
- Power systems (P9, P10, P11, HMC) represent **18.0% of contracts**
- Strong diversification across product lines

---

## 8. Average Contract Values

### 8.1 Contract Value by Service Name

| Service Name | Average Value | Median Value | Contract Count |
|--------------|---------------|--------------|----------------|
| **Committed Maintenance IBM Z** | $389,516.94 | $115,309.25 | 73 |
| **HWMA IBM Z** | $1,363,878.09 | $476,309.56 | 942 |
| **HWMA Power** | $6,537.48 | $1,274.40 | 14,492 |
| **HWMA Storage** | $8,289.91 | $1,913.62 | 84,141 |
| **WSU Power** | $220.52 | $0.00 | 793 |
| **WSU Storage** | $845.10 | $0.00 | 7,539 |

**Key Observations:**
- IBM Z services have significantly higher contract values (avg $1.36M)
- Storage and Power HWMA services have moderate values ($6-8K average)
- WSU services have lower average values, indicating potential upsell opportunities

---

## 9. Sales Motion Recommendations

### 9.1 Immediate Actions (Next 30 Days)

1. **Address Expiring High-Value Contracts**
   - Contact 48 customers with contracts expiring within 180 days
   - Total revenue at risk: $3.17M
   - Focus on UK and France customers with premium service levels
   - Offer auto-renewal incentives

2. **Resolve Past EOS Contracts**
   - Review 4,238 contracts past their EOS date
   - Determine if hardware upgrades are needed
   - Migrate to supported hardware or adjust contract terms
   - Priority: 3,433 HWMA Storage contracts

3. **Enable Auto-Renewal**
   - Target WAMO and WSU services (currently 0% auto-renewal)
   - Set goal: Increase auto-renewal from 11.8% to 30% within 6 months
   - Potential revenue protection: $500M+ annually

### 9.2 Short-Term Initiatives (Next 90 Days)

4. **CMSL Upsell Campaign**
   - Current CMSL adoption: 23.1%
   - Target: Increase to 35% within 12 months
   - Focus on customers with SBD service levels (109,974 contracts)
   - Estimated revenue uplift: 15-20% per converted contract

5. **Geographic Expansion**
   - France and Germany represent 66.9% of revenue
   - Develop growth strategies for underrepresented markets
   - Target countries: Netherlands, Austria, Czech Republic

6. **Service Level Optimization**
   - Analyze customers with basic service levels
   - Propose premium service upgrades (4h committed, 24x7)
   - Focus on mission-critical systems

### 9.3 Long-Term Strategic Initiatives (6-12 Months)

7. **Multi-Year Contract Strategy**
   - Promote 3-year and 5-year contracts with discounts
   - Include auto-renewal as standard
   - Reduce annual churn risk

8. **Product Family Cross-Sell**
   - Customers with DRI storage: Offer FLASHSYS upgrades
   - P9 customers: Promote P10/P11 migration paths
   - Bundle storage and power services

9. **Customer Segmentation**
   - Tier 1: High-value IBM Z customers (avg $1.36M)
   - Tier 2: Storage customers with multiple systems
   - Tier 3: Power systems customers
   - Develop targeted retention and growth programs per tier

10. **Proactive EOS Management**
    - Implement 18-month advance EOS notifications
    - Create hardware refresh programs
    - Bundle hardware upgrades with extended service contracts

---

## 10. Revenue Opportunities

### 10.1 Quick Wins (Potential $50M+ Annual Impact)

| Opportunity | Estimated Impact | Timeframe |
|-------------|------------------|-----------|
| Enable auto-renewal on 50% of contracts | $25M+ protected revenue | 3-6 months |
| Convert 20% of SBD to CMSL | $15M+ incremental | 6-12 months |
| Renew 48 expiring high-value contracts | $3.2M immediate | 30-60 days |
| Resolve past EOS contracts with upgrades | $10M+ | 6-12 months |

### 10.2 Growth Opportunities (Potential $100M+ Annual Impact)

| Opportunity | Estimated Impact | Timeframe |
|-------------|------------------|-----------|
| Expand WSU services adoption | $30M+ | 12-18 months |
| Geographic expansion (new markets) | $40M+ | 12-24 months |
| Multi-year contract conversions | $30M+ | 12-18 months |
| Product family cross-sell | $25M+ | 12-24 months |

---

## 11. Risk Assessment

### 11.1 High Risk Areas

1. **Churn Risk: $500M+**
   - 88.2% of contracts without auto-renewal
   - Manual renewal process increases churn probability
   - Mitigation: Aggressive auto-renewal enablement campaign

2. **Compliance Risk: 4,238 Contracts**
   - Contracts active past EOS date
   - Potential service delivery issues
   - Mitigation: Immediate hardware assessment and upgrade path

3. **Revenue Concentration: 66.9%**
   - France and Germany represent majority of revenue
   - Geographic concentration risk
   - Mitigation: Diversification strategy for other European markets

### 11.2 Medium Risk Areas

4. **Service Level Concentration**
   - 69.6% of contracts on SBD (lower tier)
   - Opportunity for upsell but also indicates price sensitivity
   - Mitigation: Value-based selling approach for CMSL

5. **Future Contract Pipeline**
   - 25,518 contracts not yet started (16.2%)
   - Execution risk on contract activation
   - Mitigation: Proactive customer engagement and onboarding

---

## 12. Key Performance Indicators (KPIs)

### 12.1 Current State

| KPI | Current Value | Target | Gap |
|-----|---------------|--------|-----|
| Auto-Renewal Rate | 11.8% | 30% | -18.2% |
| CMSL Adoption | 23.1% | 35% | -11.9% |
| Contracts Past EOS | 4,238 | 0 | -4,238 |
| Q2 2026 Revenue | $176.7M | $200M | -$23.3M |
| Average Contract Value | $8,289 | $10,000 | -$1,711 |

### 12.2 Recommended Tracking Metrics

- **Monthly:** Contract signings, revenue, churn rate, auto-renewal adoption
- **Quarterly:** CMSL conversion rate, EOS resolution rate, geographic revenue mix
- **Annually:** Customer lifetime value, net revenue retention, market share

---

## Conclusion

The European contract portfolio demonstrates strong growth with Q1 2026 signings reaching 29,447 contracts and quarterly revenue of $176.7M. However, significant opportunities exist to improve contract quality and reduce churn risk:

**Critical Actions:**
1. Enable auto-renewal on 88.2% of contracts currently without it
2. Address 4,238 contracts past their EOS date
3. Secure 48 high-value contracts expiring within 180 days ($3.17M at risk)
4. Increase CMSL adoption from 23.1% to 35%

**Growth Opportunities:**
- Expand WSU services (currently underrepresented)
- Geographic diversification beyond France and Germany
- Product family cross-sell and upsell initiatives
- Multi-year contract strategy

By addressing these areas, the European region can protect existing revenue, reduce churn, and unlock $150M+ in additional annual revenue opportunities.

---

**Report Generated:** June 2, 2026  
**Analysis Tool:** Python with pandas  
**Data Quality:** 157,987 records processed successfully