# Tax Calculation Waterfall — California Individual (Form 540)
**R&TC Section(s):** Sections 17041, 17043, 17073, 17073.5, 17054, 17054.5, 23151, 23802
**Parallel IRC Section:** IRC Sections 1, 55-59, 63, 151
**California Conformity Status:** Does Not Conform — California has an entirely independent tax computation with its own brackets, rates, deductions, credits, and AMT
**Relevant FTB Forms:** Form 540, Schedule CA (540), Schedule P (540), Form 540NR
**Tax Years Covered:** 2025-2026
**Last Updated:** March 2026
**Citations:**
- [FTB 2025 Form 540 Instructions](https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html)
- [FTB 2025 California Tax Rate Schedules](https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf)
- [FTB 2025 Schedule P (540) — Alternative Minimum Tax](https://www.ftb.ca.gov/forms/2025/2025-540-p.pdf)
- [FTB Tax News October 2025 — 2025 Inflation Adjustments](https://www.ftb.ca.gov/about-ftb/newsroom/tax-news/2025/10.html)
- [FTB 2025 Form 540](https://www.ftb.ca.gov/forms/2025/2025-540.pdf)
- [FTB Deductions Page](https://www.ftb.ca.gov/file/personal/deductions/index.html)

---

## Overview

The California individual income tax computation follows a specific waterfall from federal AGI through California adjustments, deductions, tax rates, credits, and additional taxes. Form 540 is the primary vehicle. This document traces every step of that waterfall for tax years 2025-2026, identifying the key divergences from the federal computation at each stage.

## California Rule: The Full Individual Tax Waterfall

### Step 1: Start with Federal AGI

**Form 540, Line 13:** Enter federal adjusted gross income from Form 1040, line 11b.

This is the starting point. The entire California computation builds from the federal AGI figure. If the taxpayer has no differences between federal and California income, Schedule CA is not required and the federal AGI flows directly.

### Step 2: Schedule CA Adjustments — Subtractions

**Form 540, Line 14:** Enter the net subtraction from Schedule CA (540), Part I, line 27, Column B.

Column B subtractions reduce federal AGI toward California AGI. Common subtractions include:
- Social Security benefits (100% excluded from CA)
- U.S. government bond interest
- Unemployment compensation
- State tax refund (if included federally)
- Railroad retirement benefits
- California lottery winnings
- Section 163(j) business interest denied federally but allowed in CA
- Section 174 R&E amortization difference (full deduction in CA)

### Step 3: Subtotal

**Form 540, Line 15:** Subtract Line 14 from Line 13.

### Step 4: Schedule CA Adjustments — Additions

**Form 540, Line 16:** Enter the net addition from Schedule CA (540), Part I, line 27, Column C.

Column C additions increase the subtotal toward California AGI. Common additions include:
- Bonus depreciation add-back
- Section 179 excess add-back
- QBI deduction add-back (Section 199A)
- HSA contributions, deductions, and earnings
- Out-of-state municipal bond interest
- OBBBA-specific deductions add-back (tip, overtime, auto, senior)
- Employer HSA contributions excluded federally

### Step 5: California AGI

**Form 540, Line 17:** Combine Line 15 and Line 16. This is California adjusted gross income.

California AGI is a critical figure. It determines:
- Eligibility for various California credits (e.g., CalEITC, Renter's Credit)
- Phaseout thresholds for exemption credits
- The basis for calculating itemized deduction limitations

### Step 6: Standard Deduction or Itemized Deductions

**Form 540, Line 18:** Enter the California standard deduction OR California itemized deductions.

#### California Standard Deduction (2025)

| Filing Status | Amount |
|--------------|--------|
| Single | $5,706 |
| Married/RDP Filing Jointly | $11,412 |
| Married/RDP Filing Separately | $5,706 |
| Head of Household | $11,412 |
| Qualifying Surviving Spouse/RDP | $11,412 |

These amounts are dramatically lower than the federal standard deduction ($16,100 single / $32,200 MFJ under OBBBA). Many taxpayers who use the standard deduction federally will still itemize for California because the California standard deduction is so low.

#### California Itemized Deductions — Key Differences from Federal

| Deduction | Federal Rule | California Rule |
|-----------|-------------|-----------------|
| State and local taxes (SALT) | $40,000 cap (OBBBA) | No cap; but no deduction for CA state income tax on CA return |
| Home mortgage interest | $750,000 acquisition debt limit | $1,000,000 acquisition debt limit |
| Miscellaneous itemized (2% floor) | Suspended (TCJA/OBBBA) | Allowed — deductible to extent exceeding 2% of federal AGI |
| Medical/dental expenses | Above 7.5% of AGI | Above 7.5% of AGI (same) |
| Charitable contributions | Standard federal limits | Same as federal (conformed) |
| Personal casualty losses | Only for federally declared disasters | CA own disaster loss rules |

### Step 7: California Taxable Income

**Form 540, Line 19:** Subtract Line 18 from Line 17. If less than zero, enter zero. This is California taxable income.

### Step 8: Compute Tax Using California Rate Schedules

**Form 540, Line 31:** Compute the tax on Line 19 taxable income using the applicable California Tax Rate Schedule (Schedule X, Y, or Z).

California imposes nine progressive tax brackets from 1% to 12.3%. See [00-ca-income-brackets-rates.md](00-ca-income-brackets-rates.md) for the full rate tables.

**Critical difference:** California taxes ALL income at ordinary rates. There is NO preferential rate for long-term capital gains or qualified dividends. Federal rates of 0%/15%/20% for capital gains do not apply. Capital gains income stacked on top of other income can push a California taxpayer into the 12.3% bracket (or 13.3% with the Behavioral Health Services Tax).

### Step 9: Exemption Credits

**Form 540, Line 32:** Enter exemption credits.

California uses exemption **credits** (direct reductions of tax), not exemption **deductions** (reductions of taxable income). This is a fundamental structural difference from the federal system (which suspended personal exemptions entirely under TCJA/OBBBA).

#### 2025 Exemption Credit Amounts

| Type | Credit Amount |
|------|-------------|
| Personal (single, MFS, HoH) | $153 per filer |
| Personal (MFJ, QSS) | $306 (combined for both spouses) |
| Senior (65+) | Additional $153 per qualifying senior |
| Blind | Additional $153 per qualifying blind person |
| Dependent | $475 per dependent |

Exemption credits phase out for higher-income taxpayers. The phaseout begins when federal AGI exceeds:
- $252,203 (single)
- $504,411 (MFJ/QSS)
- $378,310 (HoH)

The phaseout reduces each exemption credit by $6 for every $2,500 ($1,250 MFS) of AGI above the threshold.

### Step 10: Tax After Exemption Credits

**Form 540, Line 33:** Subtract Line 32 from Line 31. If zero or less, enter zero.

### Step 11: Special Taxes

**Form 540, Line 34:** Tax from Schedule G-1 (Tax on Lump-Sum Distributions) or FTB 5870A (Tax on Accumulation Distribution of Trusts), if applicable.

**Form 540, Line 35:** Add Line 33 and Line 34.

### Step 12: Nonrefundable Credits

**Form 540, Lines 40-48:** Apply nonrefundable credits against the tax. These include:

- Child and Dependent Care Expenses Credit (Code 232) — CA-source care only; federal AGI must be $100,000 or less
- Joint Custody Head of Household Credit (Code 170)
- Dependent Parent Credit (Code 173)
- Senior Head of Household Credit (Code 163)
- California Competes Tax Credit
- Motion Picture / TV Credit
- Pass-through entity elective tax credit
- Various other special credits

Nonrefundable credits cannot reduce tax below zero.

### Step 13: Other Taxes

**Form 540, Line 61:** Alternative Minimum Tax (AMT) from Schedule P (540).
**Form 540, Line 62:** Behavioral Health Services Tax (1% on taxable income over $1,000,000).
**Form 540, Line 63:** Other taxes (early distribution penalties, credit recapture).

#### California AMT (Schedule P)

California imposes its own AMT at a flat 7% rate (versus federal rates of 26%/28%):

1. Start with California taxable income.
2. Add back AMT preference items and adjustments (similar to federal but with CA-specific modifications).
3. Compute Alternative Minimum Taxable Income (AMTI).
4. Apply AMT exemption: $92,749 (single/HoH), $123,667 (MFJ/QSS), $61,830 (MFS) for 2025. These phase out at higher AMTI levels.
5. Multiply the excess by 7%.
6. Subtract regular tax. If positive, the difference is the California AMT.

Small business exemption: AMT income does not include items from trades or businesses with gross receipts under $1,000,000.

#### Behavioral Health Services Tax

Renamed from Mental Health Services Tax for TY 2025 onwards per the Behavioral Health Services Act:
- Applies to taxable income exceeding $1,000,000 ($500,000 if MFS).
- Rate: 1%.
- The $1,000,000 threshold is **not** indexed for inflation (static since enactment by Proposition 63 in 2004).
- Effect: The top marginal rate on income above $1M is 12.3% + 1% = **13.3%**.

### Step 14: Total Tax

**Form 540, Line 64:** Add Line 48 (tax after nonrefundable credits) + Line 61 (AMT) + Line 62 (Behavioral Health Services Tax) + Line 63 (other taxes).

### Step 15: Refundable Credits

**Form 540, Lines 74-78:** Refundable credits that can create a refund even if no tax is owed:

- California Earned Income Tax Credit (CalEITC) — up to $3,756 for TY 2025
- Young Child Tax Credit (YCTC) — up to $1,189 for children under 6
- Foster Youth Tax Credit (FYTC)
- Elective Tax Credit (PTE)
- Excess SDI/VPDI withheld

### Step 16: Payments and Withholding

**Form 540, Lines 71-73, 80-82:** Apply payments against total tax:

- California income tax withheld (W-2, 1099, Form 592-B/593)
- Estimated tax payments (Form 540-ES)
- Extension payment (FTB 3519)
- Overpayment from prior year applied

### Step 17: Tax Due or Refund

**Form 540, Line 91:** If total payments exceed total tax, the difference is a refund or can be applied to next year's estimated tax. If total tax exceeds payments, the balance is tax due.

## Key Differences from Federal — Summary Table

| Feature | Federal (IRC/OBBBA) | California (R&TC/Form 540) |
|---------|---------------------|---------------------------|
| Starting point | Gross income to AGI | Federal AGI (from Form 1040) |
| Above-the-line deductions | QBI, SALT, etc. | No QBI; limited conformity |
| Standard deduction | $16,100 / $32,200 | $5,706 / $11,412 |
| Personal exemption | Suspended | Exemption CREDITS ($153/$475) |
| Tax brackets | 7 brackets (10%-37%) | 9 brackets (1%-12.3%) |
| Top rate (with surcharge) | 37% | 13.3% (12.3% + 1% BHST) |
| Capital gains rate | 0%/15%/20% preferential | Ordinary rates (up to 13.3%) |
| NIIT | 3.8% on investment income >$250K MFJ | Does not apply |
| Additional Medicare Tax | 0.9% on earned income >$250K MFJ | Does not apply |
| AMT rate | 26%/28% | 7% flat |
| AMT exemption (MFJ) | $137,000 | $123,667 |
| EITC | Federal EITC | CalEITC (separate, more generous income threshold) |
| Child Tax Credit | $2,200 (OBBBA) | No CTC (YCTC for under-6 only) |

## Conformity Analysis

**IRC RULE:** Tax computation under IRC Sections 1, 55-59, 63, 151 with TCJA/OBBBA modifications.

**CALIFORNIA RULE:** Independent computation under R&TC Sections 17041-17048 (rates), 17073-17073.5 (standard deduction), 17054 (exemption credits), Schedule P (AMT).

**Controlling Authority:** R&TC Part 10 (Personal Income Tax Law)

**Schedule CA Impact:** Schedule CA bridges federal AGI to California AGI. All subsequent computations (deductions, rates, credits) use California-specific rules.

## Agent Rules

> **AGENT RULE:** When computing California tax, NEVER use federal bracket rates. Apply the California Tax Rate Schedule (X for single/MFS, Y for MFJ/QSS, Z for HoH) to California taxable income from Form 540, line 19.

> **AGENT RULE:** For any taxpayer with taxable income exceeding $1,000,000 ($500,000 MFS), compute the Behavioral Health Services Tax at 1% on the excess. This cannot be avoided or reduced by credits.

> **AGENT RULE:** When a taxpayer has capital gains or qualified dividends, do NOT apply the federal preferential rate for California. These are taxed at the same ordinary rates as wages and business income.

> **AGENT RULE:** Always evaluate whether itemizing is beneficial for California even if the taxpayer uses the standard deduction federally. The California standard deduction is much lower, making itemization more likely to be advantageous.

> **AGENT RULE:** The personal exemption credit phases out at higher income. Always check if federal AGI exceeds the phaseout thresholds ($252,203 single / $504,411 MFJ / $378,310 HoH) and reduce exemption credits accordingly.

## Common Traps

> **TRAP:** Applying the federal 0%/15%/20% capital gains rate on a California return. California has NO preferential capital gains rate. A taxpayer selling appreciated stock who pays 15% federally may owe up to 13.3% to California on the same gain.

> **TRAP:** Assuming the federal Child Tax Credit ($2,200 OBBBA) applies in California. It does not. California has no CTC. The Young Child Tax Credit (YCTC, up to $1,189) only applies to children under 6 and requires CalEITC eligibility.

> **TRAP:** Forgetting the California AMT. At a 7% rate it seems small, but it catches taxpayers with large state tax deductions, incentive stock option exercises, or significant preference items. The AMT exemption amounts are lower than federal.

> **TRAP:** Assuming the $1,000,000 Behavioral Health Services Tax threshold is inflation-adjusted. It is not. It has been static since Proposition 63 in 2004. Inflation has pushed significantly more taxpayers above this threshold than when it was enacted.

> **TRAP:** Miscellaneous itemized deductions subject to the 2% floor are deductible for California even though they are suspended federally. Failing to claim them on the California return means leaving money on the table. Common examples: unreimbursed employee expenses, tax preparation fees, investment advisory fees.

## Cross-References

- Related doc: [00-ca-two-system-framework.md](00-ca-two-system-framework.md) — Two-system architecture overview
- Related doc: [00-ca-conformity-master.md](00-ca-conformity-master.md) — Conformity/non-conformity reference
- Related doc: [00-ca-gross-income-definition.md](00-ca-gross-income-definition.md) — Income inclusions and exclusions
- Related doc: [00-ca-income-brackets-rates.md](00-ca-income-brackets-rates.md) — Full bracket tables
- Related doc: [00-ca-filing-status-residency.md](00-ca-filing-status-residency.md) — Filing status and residency
