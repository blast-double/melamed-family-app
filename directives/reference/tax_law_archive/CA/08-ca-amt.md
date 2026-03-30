# Alternative Minimum Tax (AMT) — California

*Last Edited: 2026-03-26*

**R&TC Section(s):** Sections 17062, 17063
**Parallel IRC Section:** IRC Sections 55–59 (individual); IRC Section 56A (corporate, post-IRA)
**California Conformity Status:** Partially Conforms
**Relevant FTB Forms:** Schedule P (540), Schedule P (540NR), Schedule P (100), Form 3510
**Tax Years Covered:** 2025–2026
**Last Updated:** March 2026
**Citations:**
- [2025 Form 540 Instructions — Line 61 (AMT)](https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html)
- [2025 Schedule P (540) PDF](https://www.ftb.ca.gov/forms/2025/2025-540-p.pdf)
- [2025 Form 3510 — Credit for Prior Year AMT](https://www.ftb.ca.gov/forms/2025/2025-3510.pdf)
- [FTB Tax Calculator, Tables, Rates — AMT](https://www.ftb.ca.gov/file/personal/tax-calculator-tables-rates.asp)
- [2025 Form 540-ES Instructions](https://www.ftb.ca.gov/forms/2025/2025-540-es-instructions.html)
- [IRS Form 6251 Instructions (2025)](https://www.irs.gov/pub/irs-pdf/i6251.pdf)
- [EY Tax Alert 2025-2032 — California SB 711 Conformity](https://taxnews.ey.com/news/2025-2032-california-updates-general-date-conformity-to-internal-revenue-code-while-continuing-to-decouple-from-significant-federal-provisions)

---

## Overview

California imposes its own Alternative Minimum Tax (AMT) on individuals and corporations, separate from and in addition to the federal AMT. The California AMT operates under the same general framework as the federal AMT — computing a parallel tax base with specific add-backs and preference items — but at a significantly lower rate. The California individual AMT rate is a flat 7%, compared to the federal graduated 26%/28% rate structure. This lower rate means fewer California taxpayers trigger AMT at the state level, but certain specific items (particularly incentive stock option exercises) remain common AMT triggers in California.

---

## California Rule

### Individual AMT (R&TC Section 17062)

California computes AMT on Schedule P (540) for residents and Schedule P (540NR) for nonresidents and part-year residents. The computation follows this sequence:

1. Start with California taxable income (Form 540, line 19).
2. Add back AMT adjustment and preference items (Schedule P, Part I).
3. Subtract the AMT exemption amount.
4. Apply the flat 7% AMT rate to the Alternative Minimum Taxable Income (AMTI) above the exemption.
5. Compute the tentative minimum tax.
6. If the tentative minimum tax exceeds the regular California tax, the excess is the AMT.

### 2025 AMT Exemption Amounts

| Filing Status | Exemption Amount |
|---|---|
| Single / Head of Household | $92,749 |
| Married Filing Jointly / Qualifying Surviving Spouse | $123,667 |
| Married Filing Separately | $61,830 |

The exemption phases out at 25% of AMTI above specified thresholds. For taxpayers with AMTI significantly above the exemption phase-out range, the effective exemption reduces to zero.

### AMT Rate

California uses a **flat 7% rate** on AMTI above the exemption amount. This contrasts with the federal AMT, which imposes 26% on the first $248,300 of AMTI (above the exemption) and 28% on amounts above that threshold (for 2025, MFJ).

The 7% flat rate makes California AMT substantially less burdensome than federal AMT in absolute terms, though it still functions as a meaningful minimum tax floor.

### Small Business Exemption

AMT income does not include income, adjustments, and items of tax preference related to any trade or business of a qualified taxpayer who has gross receipts, less returns and allowances, during the taxable year of less than $1,000,000 from all trades or businesses. This exemption can eliminate AMT exposure for smaller business owners.

### Child AMT

A child under age 19 or a full-time student under age 24 may owe California AMT if the sum of their taxable income (line 19) and preference items exceeds $9,750 plus the child's earned income.

---

## AMT Add-Backs and Preference Items

The following items are added back (or adjusted) when computing California AMTI on Schedule P (540):

| Line | Item | Description |
|---|---|---|
| 1 | Standard deduction | If the taxpayer claimed the standard deduction instead of itemizing, the entire standard deduction is an AMT add-back. |
| 2 | Medical expenses | The AMT allows only 2.5% AGI floor (vs. 7.5% regular); add back the difference. |
| 3 | Property taxes | State and local property taxes deducted as itemized deductions are added back for AMT. |
| 4 | Home mortgage interest | Interest on home equity debt not used to buy/build/improve the home is an AMT add-back. |
| 5 | Miscellaneous itemized deductions | The full amount of miscellaneous itemized deductions (which California uniquely allows at the 2% floor) is an AMT add-back. This is a critical California-specific item because these deductions exist only on the California return. |
| 6 | Property tax refunds | Refunds of taxes added back in line 3 must be subtracted. |
| 7 | Investment interest | Adjustment for the difference between regular tax and AMT investment interest calculations. |
| 8 | Post-1986 depreciation | Difference between regular tax depreciation and AMT depreciation (using California basis, which may differ from federal basis due to non-conformity with bonus depreciation and Section 179). |
| 9 | Adjusted gain or loss | Gain/loss adjustments for assets with different AMT and regular tax basis. |
| 10 | Incentive stock options (ISOs) and California Qualified Stock Options (CQSOs) | The spread on ISO exercise (fair market value minus exercise price) is an AMT preference item. This is the single most common trigger of California AMT for technology employees and startup founders. |
| 11 | Passive activities | AMT passive activity adjustments. |
| 12 | Beneficiaries of estates and trusts | AMT adjustments passed through on Schedule K-1 (541). |
| 13 | Other adjustments | Percentage depletion, tax-exempt interest from private activity bonds, intangible drilling costs, and other preference items. |

---

## Conformity Analysis

| Feature | Federal AMT | California AMT | Conforms? |
|---|---|---|---|
| Individual rate | 26% / 28% graduated | 7% flat | No |
| Exemption (Single/HoH) | $88,100 (2025) | $92,749 | No |
| Exemption (MFJ) | $137,000 (2025) | $123,667 | No |
| ISO exercise spread | Yes — AMT preference | Yes — AMT preference | Yes |
| Depreciation adjustment | Federal basis | California basis (differs from federal) | Partial |
| Misc. itemized add-back | N/A (suspended federally) | Full add-back of 2% deductions | CA-specific |
| Corporate AMT | 15% AFSI (post-IRA) | 6.65% rate | No |
| Corporate AMT conformity to IRA | IRC Section 56A (Book Minimum Tax) | Does NOT conform | No |

### Corporate AMT

California imposes a corporate AMT at a rate of **6.65%** (compared to the regular corporate tax rate of 8.84%). The federal corporate AMT was repealed by the TCJA in 2017 but was effectively reinstated under the Inflation Reduction Act (IRA) of 2022 as the 15% Corporate Alternative Minimum Tax on Adjusted Financial Statement Income (AFSI) for corporations with average annual AFSI exceeding $1 billion.

**California does NOT conform to the federal 15% AFSI-based corporate AMT.** California instead continues to apply its own corporate AMT at the 6.65% rate under the pre-existing R&TC framework. SB 711 specifically decouples from IRC Section 56A.

S corporations are **not subject** to California AMT at the entity level.

---

## Key Thresholds and Figures

| Item | 2025 Amount |
|---|---|
| Individual AMT rate | 7% (flat) |
| Corporate AMT rate | 6.65% |
| Exemption — Single/HoH | $92,749 |
| Exemption — MFJ/QSS | $123,667 |
| Exemption — MFS | $61,830 |
| Exemption phase-out rate | 25% of AMTI above threshold |
| Small business gross receipts exemption | < $1,000,000 |
| Child AMT threshold | $9,750 + earned income |
| AMT credit carryforward | Indefinite |

---

## AMT Credit (R&TC Section 17063)

When AMT is triggered by **timing items** (items that will reverse in future years, such as depreciation differences or ISO exercise spreads), the taxpayer generates a **Minimum Tax Credit (MTC)** that carries forward indefinitely against future regular tax liability.

Form 3510, Credit for Prior Year Alternative Minimum Tax, is used to compute and claim the credit. The credit is computed by separating "exclusion items" (permanent differences) from "deferral items" (timing differences). Only the AMT attributable to deferral items generates the credit.

Common timing items that generate MTC:
- ISO exercise spread (reverses when stock is sold)
- Depreciation timing differences (reverse over the remaining asset life)
- Passive activity adjustments (reverse when activity is disposed)

The MTC carries forward indefinitely until fully utilized. It cannot be refunded, but it effectively ensures that AMT paid on timing items is recovered over future years.

For taxable years beginning on or after January 1, 2024, and before January 1, 2027, the $5,000,000 credit limitation on business credits does **not** apply to the credit for prior year AMT.

---

## OBBBA Non-Conformity

The OBBBA does not make significant changes to the individual federal AMT, as the TCJA provisions were extended. California's non-conformity to OBBBA has limited AMT impact. The primary OBBBA-related issue is that California does not conform to OBBBA changes that affect the AMT base indirectly (e.g., bonus depreciation restoration, Section 179 increases), which continue to create basis differences between federal and California AMT computations.

---

## Agent Rules

1. **California's 7% AMT is much lower than federal.** Fewer California taxpayers trigger AMT at the state level compared to the federal level. However, the existence of miscellaneous itemized deductions (a California-only item) as an add-back means some taxpayers who would not trigger federal AMT may trigger California AMT.

2. **ISO exercise is the most common California AMT trigger.** For technology employees exercising incentive stock options, the spread (FMV minus exercise price) on the exercise date is an AMT preference item. Given California's concentration of tech companies and startups, this is frequently the dominant AMT driver.

3. **Use California basis for depreciation adjustments.** Because California does not conform to federal bonus depreciation (Section 168(k)) or enhanced Section 179 limits, the depreciation basis for AMT purposes uses California's (generally slower) depreciation schedules. The AMT adjustment is the difference between California regular tax depreciation and California AMT depreciation.

4. **Track the AMT credit carryforward.** Any AMT paid on timing items generates a credit on Form 3510. This credit carries forward indefinitely and should be claimed in future years when regular tax exceeds tentative minimum tax.

5. **Small business exemption.** Verify whether the taxpayer qualifies for the $1,000,000 gross receipts exemption, which can eliminate AMT entirely for qualifying small business owners.

---

## Common Traps

1. **Ignoring California AMT because federal AMT was not triggered.** The different rate structure, exemption amounts, and California-specific add-backs (especially miscellaneous itemized deductions) mean California AMT can apply even when federal AMT does not.

2. **Using federal depreciation basis for California AMT.** California has its own depreciation schedules due to non-conformity with bonus depreciation and Section 179. The AMT depreciation adjustment must use California basis, not federal basis.

3. **Failing to claim the prior year AMT credit.** Taxpayers who paid AMT in prior years due to ISO exercises or depreciation timing may have substantial credits available. These credits carry forward indefinitely and should be reviewed each year.

4. **Not planning around ISO exercises.** The ISO exercise spread is the most controllable AMT trigger. Consider exercising options in stages across multiple tax years to stay below the AMT threshold.

5. **Overlooking the corporate AMT.** While S corporations are exempt, C corporations are subject to the 6.65% California corporate AMT. Do not assume the federal corporate AMT repeal (pre-IRA) or the IRA's AFSI regime applies to California.

---

## Cross-References

- [08-ca-itemized-deductions.md] — Miscellaneous itemized deductions are a key AMT add-back
- [09-ca-sb711-changes.md] — SB 711 non-conformity affects depreciation basis used in AMT
- [08-ca-estimated-tax-penalties.md] — AMT included in estimated tax calculations; safe harbor uses prior year tax including AMT
- [11-ca-forms-reference.md] — Schedule P (540), Form 3510 filing details
