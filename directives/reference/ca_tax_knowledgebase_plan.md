# California Tax Law Knowledge Base — Agent Build Plan
**Version:** 2.0 | **Date:** March 2026
**Governing Law:** California Revenue and Taxation Code (R&TC) — California's independent Personal Income Tax (R&TC Part 10) and Corporate Franchise/Income Tax (R&TC Part 11)
**IRC Conformity Authority:** R&TC Section 17024.5 (PIT); R&TC Section 23051.5 (Corporate) — California incorporates IRC definitions as of January 1, 2025 per SB 711 (Conformity Act of 2025, signed October 1, 2025), effective for tax years beginning on or after January 1, 2025
**Key 2024–2026 Legislation:** SB 711 (Conformity Act of 2025); SB 167 (NOL Suspension/Credit Cap 2024–2026); SB 175 (Revenue Trigger for Early Sunset of SB 167); SB 132 (PTE Elective Tax Extension through 2030); AB 150 (PTE Elective Tax origination)
**Administering Agencies:** Franchise Tax Board (FTB) — income/franchise tax; California Department of Tax and Fee Administration (CDTFA) — sales/use tax; Employment Development Department (EDD) — payroll taxes; Office of Tax Appeals (OTA) — administrative appeals

---

## Critical Framing: Two Separate, Parallel Tax Systems

A California taxpayer files two entirely separate returns and pays two entirely separate tax liabilities:

1. **Federal return (Form 1040)** — governed by the Internal Revenue Code (IRC), administered by the IRS, calculates a federal tax liability.
2. **California return (Form 540 / 540NR)** — governed by the California Revenue and Taxation Code (R&TC), administered by the FTB, calculates a California tax liability.

These are independent obligations. California does not calculate tax on top of federal tax, and California tax is not derived from federal tax liability in any way.

**What conformity means:** California's R&TC could define every term — "gross income," "adjusted basis," "depreciation" — from scratch. Instead, R&TC Section 17024.5 says: for certain terms, California borrows the IRC's definition as of a specified date (January 1, 2025 per SB 711). This is a legislative drafting efficiency. It means California and federal law use the same *definition* of "gross income" (Section 61), for example — but what California does with that income (rates, deductions, credits, exemptions) is entirely its own law.

**Why Schedule CA exists:** Because California's income definitions are largely parallel to federal definitions, the Form 540 instructions use federal AGI as a computational starting point — add California-specific income (Column B), subtract California-specific exclusions (Column C), arrive at California AGI. This is a practical bridge, not a statement that California tax flows from federal tax. California AGI frequently differs from federal AGI, sometimes substantially.

**What OBBBA means for California:** OBBBA (P.L. 119-21) was signed July 4, 2025 — after California's January 1, 2025 IRC conformity date. California does not conform to any OBBBA provision unless the California Legislature separately enacts parallel legislation. As of March 2026, no such legislation has been enacted.

Every document in this knowledge base must reflect this two-system structure. When a document says "California conforms," it means California's independently enacted R&TC provision produces the same result as the IRC provision. When it says "California does not conform," it means the R&TC produces a different result and a Schedule CA adjustment is required.

---

## Your Mission

Build a California tax law knowledge base as a collection of focused markdown documents. Each document covers one cohesive California tax topic and is designed for retrieval by a tax AI agent via vector store. Documents must be:

- Self-contained: every doc includes its own R&TC citations, relevant FTB forms, dollar thresholds, and agent rules
- Dense and factual: no narrative filler, no editorializing, law stated as fact
- 800–2,000 words per document by default; extended limits noted per-file below
- Consistent format: every document follows the template below
- Conformity-explicit: every document states whether California's rule matches or differs from the parallel IRC provision

---

## Universal Document Template

```
# [Topic Name] — California
**R&TC Section(s):** Section XXXXX
**Parallel IRC Section:** IRC Section XXX
**California Conformity Status:** [Conforms | Does Not Conform | Partially Conforms — cite R&TC authority]
**Relevant FTB Forms:** Form XXXX, Schedule XXXX
**Tax Years Covered:** 2025–2026
**Last Updated:** March 2026
**Citation:** [FTB publication, R&TC statutory text, or practitioner alert with URL]

---

## Overview
[2–4 sentence factual summary of the California rule and how it differs from federal]

## California Rule
[The actual California law stated as facts. Numbered lists for sequential rules,
bullet lists for parallel items, tables for rates/thresholds. No paragraph longer than 4 sentences.]

## Conformity Analysis
**IRC RULE:** [What the IRC provides]
**CALIFORNIA RULE:** [What R&TC provides]
**Controlling Authority:** [R&TC section, SB/AB number, FTB regulation]
**Schedule CA Impact:** [Column B addition | Column C subtraction | No adjustment needed]
[Repeat block for each conformity/non-conformity item within the topic]

## Key Thresholds and Figures
[Table — 2025 column and 2026 column where figures differ]

## OBBBA Non-Conformity (where applicable)
**OBBBA PROVISION:** [What OBBBA enacted]
**CALIFORNIA STATUS:** [Does not conform — SB 711 conformity date predates OBBBA]

## Agent Rules
> **AGENT RULE:** [Conditional decision logic: "If X, then Y."]

## Common Traps
> **TRAP:** [California-specific error or misapplication]

## Cross-References
- Related doc: [filename]
```

---

## File List and Build Specifications

---

### PART 0 — FOUNDATION

#### 00-ca-two-system-framework.md
R&TC Sections 17024.5, 17041, 23051.5; SB 711

**This is the gateway document. Every other document depends on the concepts here.**

Cover:

THE TWO SYSTEMS:
- Federal income tax: IRC-governed, Form 1040, IRS-administered; entirely separate from California
- California Personal Income Tax (PIT): R&TC Part 10-governed, Form 540/540NR, FTB-administered
- California Corporate Franchise/Income Tax: R&TC Part 11-governed, Form 100/100S, FTB-administered
- The two liabilities are computed independently; paying one does not reduce the other
- California deduction for federal taxes paid: NOT ALLOWED — there is no deduction for federal income taxes on the California return

CONFORMITY MECHANISM — R&TC SECTION 17024.5:
- California's R&TC incorporates IRC definitions by reference as of a "specified date"
- SB 711 (signed October 1, 2025): updated specified date from January 1, 2015 to January 1, 2025 for tax years beginning on or after January 1, 2025
- Effect: California now uses the same definitions as the IRC as enacted through January 1, 2025
- Non-effect: this does NOT mean California adopted all federal law — explicit California departures in the R&TC override the general conformity date
- OBBBA (enacted July 4, 2025): falls after the conformity date; California does NOT conform to any OBBBA provision

SCHEDULE CA AS A BRIDGE:
- Form 540 starts with federal AGI (Form 1040 Line 11) as a computational starting point
- Schedule CA Part I, Column B: Add back items excluded federally but taxable in California (e.g., federal bonus depreciation claimed above California's $25,000 Section 179 limit)
- Schedule CA Part I, Column C: Subtract items taxable federally but excluded in California (e.g., Social Security benefits — fully excluded in California; interest on U.S. obligations)
- Result: California AGI — the figure used for California-specific phase-outs and limitations
- California AGI ≠ federal AGI in virtually every return involving business income, depreciation, Social Security, or retirement income

MAJOR AREAS OF NON-CONFORMITY — SUMMARY TABLE (detail in individual docs):
| Item | Federal Rule | California Rule | R&TC Authority |
|------|-------------|----------------|----------------|
| Bonus depreciation | 100% (OBBBA permanent) | $0 — not allowed | R&TC §17250 |
| Section 179 | $2,500,000 (OBBBA) | $25,000; phase-out at $200,000 | R&TC §17255 |
| QBI deduction (§199A) | 20% deduction | Not allowed | R&TC §17024.5 (no conformity) |
| SALT deduction cap | $40,000 (OBBBA) | N/A — no deduction for CA taxes on CA return | R&TC §17220 |
| Capital gains rates | 0%/15%/20% LTCG | Ordinary rates up to 13.3% | R&TC §17041 |
| QSBS exclusion (§1202) | Up to 100% excluded | Not allowed | R&TC §18152.5 |
| NOL carryforward | Unlimited | 20 years (suspended 2024–2026) | R&TC §17276 |
| Estate/gift tax | Federal unified system | No California estate or gift tax | — |
| Social Security income | Up to 85% taxable | 100% excluded | R&TC §17087 |
| Miscellaneous itemized | Eliminated (TCJA/OBBBA) | Still allowed at 2% AGI floor | R&TC §17076 |
| Employee home office | Not deductible | Deductible as misc. itemized | R&TC §17076 |

AGENT RULE: Before answering any California tax question, confirm: (1) Is this about federal tax or California tax? These are separate liabilities on separate returns. (2) Does California conform to the relevant provision? Check the table above and the conformity master document. (3) What Schedule CA adjustment is required if California differs?

TRAP: The most common practitioner error is assuming that because a federal deduction or exclusion exists, it exists in California. Always verify California conformity independently. Federal law never automatically applies to California.

---

#### 00-ca-conformity-master.md
**Word limit: 2,500–3,500**
R&TC Sections 17024.5, 23051.5; SB 711 (Conformity Act of 2025)
**Citation:** SB 711 bill analysis, FTB.ca.gov; Grant Thornton alert "California conformity date update doesn't include OBBBA" (October 2025); KPMG Tax News Flash "California: Newly enacted law updates IRC conformity" (October 2025)

Cover:

CONFORMITY DATE HISTORY:
- Pre-SB 711: California conformed to IRC as of January 1, 2015 — a 10-year gap accumulated
- SB 711 signed October 1, 2025: moved specified date to January 1, 2025 for tax years beginning on or after January 1, 2025
- Practical effect: many TCJA provisions (2017) that California did not previously conform to are now incorporated — practitioners must audit all prior Schedule CA adjustments to determine which are still required

ITEMS NEWLY CONFORMED UNDER SB 711 (previously required Schedule CA adjustment, now conforming):
- Alimony: post-2018 agreements — non-deductible/non-includable (California now matches federal; for agreements after December 31, 2025, California separately codified the same treatment)
- Moving expense deduction: eliminated (military exception retained) — California now conforms
- Bicycle commuting benefit suspension: conforms
- Section 1031 like-kind exchange: personal property exclusion — conforms (only real property qualifies)
- Various technical corrections enacted between 2015 and 2025

ITEMS THAT REMAIN NON-CONFORMED (explicit California legislative departures that survive the conformity date update):
- Section 168(k) bonus depreciation: California has never conformed; explicitly decoupled in R&TC §17250; no bonus depreciation allowed
- Section 179: California cap is $25,000 with $200,000 phase-out (R&TC §17255); federal is $2,500,000 with $4,000,000 phase-out (OBBBA)
- Section 199A QBI deduction: California has no equivalent provision; no deduction allowed
- Section 163(j) business interest limitation: California does not conform; full deduction generally available
- Standard deduction: California has independent statutory amounts ($5,706/$11,412 for 2025); much lower than federal
- Personal exemption: California eliminated the personal exemption deduction but retains personal exemption CREDITS ($153 per exemption, 2025)
- Miscellaneous itemized deductions: California retains these at 2% AGI floor; TCJA/OBBBA elimination does not apply
- Section 1202 QSBS exclusion: California does not conform per R&TC §18152.5; full gain is taxable
- Section 461(l) excess business loss limitation: California does not conform; no similar limitation
- Corporate AMT (Section 59A BEAT): California maintains its own alternative minimum tax regime at 6.65%/7% rates

OBBBA PROVISIONS — ALL NON-CONFORMED (SB 711 conformity date precedes OBBBA enactment):
- Permanent TCJA income tax brackets: California has its own bracket structure; irrelevant
- Increased standard deduction: California has its own amounts; irrelevant
- Child Tax Credit increase to $2,200: no California equivalent; California uses CalEITC/YCTC instead
- 100% bonus depreciation (permanent): not conformed; CA continues $0 bonus
- Section 179 increase to $2,500,000: not conformed; CA remains at $25,000
- Section 174A domestic R&E immediate expensing: California independently allows immediate expensing; same result, different legal basis
- $15,000,000 estate/gift exemption: California has no estate or gift tax; irrelevant
- Section 163(j) EBITDA restoration: not conformed
- Tip/overtime/auto loan/senior deductions (above-the-line): not conformed
- SALT cap increase to $40,000: not applicable at California level
- Trump Accounts (Section 530A): not conformed
- EV credit termination: California has separate clean vehicle programs
- QSBS cap increase: not conformed (CA doesn't allow any QSBS exclusion)
- QOZ permanence: California has its own QOZ program with separate rules
- Saver's Credit conversion to matching contribution: no California equivalent
- Non-itemizer charitable deduction: not conformed
- 1% remittance excise tax: no California equivalent

R&D CREDIT CHANGES (SB 711 — effective for tax years beginning on or after January 1, 2025):
- ASC (Alternative Simplified Credit) method now available in California for the first time
- California ASC rate: 3% of QREs above 50% of prior 3-year average
- Reduced ASC rate: 1.3% if no QREs in any one of the prior 3 tax years
- Prior California law required use of the regular credit method only

AGENT RULE: SB 711 is the most consequential California tax legislation for 2025 returns. Any Schedule CA adjustment that was boilerplate on prior-year returns may no longer be needed if it relates to a provision now conformed. But all OBBBA-based federal changes (bonus depreciation, Section 179, tip deductions, senior deductions, etc.) still require California adjustments.

TRAP: Practitioners who auto-populate prior-year Schedule CA adjustments without reviewing SB 711 will over-adjust. And practitioners who assume OBBBA flows through to California because "SB 711 updated the conformity date" will under-adjust. These are opposite errors requiring opposite corrections.

---

#### 00-ca-gross-income-definition.md
R&TC Sections 17071, 17087, 17131, 17024.5; Schedule CA (540)
**Citation:** 2025 Instructions for Schedule CA (540), FTB.ca.gov; R&TC §17071

Cover:

CALIFORNIA GROSS INCOME — GENERAL RULE:
- R&TC §17071: gross income means all income from whatever source derived — mirrors IRC §61 through conformity
- California follows federal constructive receipt, cash equivalency, claim of right, and assignment of income doctrines via R&TC §17024.5

CALIFORNIA-SPECIFIC INCLUSIONS (Schedule CA Column B — add to federal AGI):
- Bonus depreciation claimed federally but not allowed in California — add back the difference
- Section 179 expensing above California's $25,000 limit — add back excess
- Federal QBI deduction (Section 199A) — add back (no California deduction)
- Federal tip/overtime/senior/auto loan deductions (OBBBA) — add back (not conformed)
- Interest on non-California state and local bonds (exempt federally, taxable in California)
- HSA contributions (deducted federally above the line) — add back (California does not conform to HSA deduction; discussed further in credits document)

CALIFORNIA-SPECIFIC EXCLUSIONS (Schedule CA Column C — subtract from federal AGI):
- Social Security benefits: fully excluded — subtract 100% of federal taxable SS (R&TC §17087)
- Interest on U.S. government obligations (Treasury bonds, savings bonds): excluded from California income
- Railroad retirement benefits (Tier 1 and Tier 2): excluded
- California lottery winnings: excluded from California income (R&TC §17156)
- Unemployment compensation: excluded from California income (R&TC §17083)
- State income tax refund: not taxable in California (no federal deduction for state tax on CA return, so no inclusion needed)

REGISTERED DOMESTIC PARTNERS (RDPs):
- California treats RDPs as married for all California income tax purposes
- An RDP may file as Single or HoH on the federal return while filing as MFJ or MFS on the California return
- This creates a situation where the California return cannot simply copy the federal filing status

AGENT RULE: California AGI is built by starting with federal AGI, then applying Schedule CA. Never apply California phase-outs or limitations to federal AGI directly. The numbers are frequently different. Social Security alone can create a $30,000+ AGI difference for a retired taxpayer.

TRAP: California does NOT allow an HSA deduction. Contributions deducted above the line federally must be added back on Schedule CA Column B. California also does not recognize HSA distributions as tax-free — distributions for medical expenses are NOT excluded from California income if the contributions were deducted federally.

---

#### 00-ca-tax-calculation-waterfall.md
R&TC Sections 17041, 17043, 17073, 17073.5, 23151, 23802
**Citation:** 2025 Instructions for Form 540, FTB.ca.gov

THE CALIFORNIA INDIVIDUAL TAX WATERFALL (Form 540):

```
Federal AGI (Form 1040 Line 11) — starting point only; not a California concept
+ Schedule CA Column B additions (California-taxable items not in federal AGI)
− Schedule CA Column C subtractions (California-excluded items in federal AGI)
= California AGI (Form 540, Line 17)

− Greater of California Standard Deduction OR California Itemized Deductions (Schedule CA Part II)
[Standard deduction: $5,706 single/MFS; $11,412 MFJ/HoH/QSS — 2025]
[No QBI deduction — Section 199A does not exist in California]
= California Taxable Income (Form 540, Line 19)

× California Tax Rate (9 brackets: 1% through 12.3%)
+ Mental Health Services Tax: 1% on taxable income exceeding $1,000,000
  [$500,000 threshold for MFS]
= Tentative California Tax

+ California AMT if greater than tentative tax (Schedule P)
  [Rate: 7% on AMTI above exemption; 2025 exemptions: $92,749 single/HoH,
   $123,667 MFJ/QSS, $61,830 MFS — Source: 2025 Form 540 Instructions, FTB]
= California Tax Before Credits

− Personal Exemption Credits (applied in this step, NOT as a deduction above)
  [$153 per personal exemption (2025); $475 per dependent (2025)]
  [Source: 2025 FTB Form 540 2EZ Tax Table]
− Nonrefundable Credits (in statutory order; cannot reduce tax below tentative minimum)
− Refundable Credits (CalEITC, YCTC, FYTC, excess SDI withholding)
− California Withholding (W-2 Box 16/17, 1099 withholding)
− Estimated Tax Payments (Form 540-ES)
= California Tax Due / Refund
```

KEY DIFFERENCES FROM FEDERAL WATERFALL:
- No QBI deduction step
- Personal exemptions are CREDITS applied after tax computation, not deductions before
- Mental Health Services Tax is a surcharge added on top of bracket tax — not a bracket
- California standard deduction is dramatically lower than federal ($5,706 vs $15,000 single for 2025)
- Capital gains taxed at ordinary rates (no separate LTCG rate schedule)
- No NIIT or Additional Medicare Tax — these are federal-only

AGENT RULE: California taxable income is computed entirely on Form 540 using California rules. The only role the federal Form 1040 plays is providing the AGI starting point for Schedule CA. A taxpayer with zero federal tax (e.g., due to QBI deduction, bonus depreciation, OBBBA tip deduction) may have substantial California taxable income because California allows none of those deductions.

TRAP: The personal exemption CREDIT ($153) is not a deduction — it does not reduce California AGI. It reduces California tax dollar-for-dollar after the rate is applied. A taxpayer in the 9.3% bracket saves $153, not $153 × 9.3%.

---

#### 00-ca-filing-status-residency.md
**Word limit: 2,000–3,000**
R&TC Sections 17014, 17015, 17015.5, 17041, 17042; FTB Publication 1031
**Citation:** FTB Pub. 1031 "Guidelines for Determining Resident Status" (2025)

Cover:

FILING STATUS:
- California recognizes: Single, MFJ, MFS, Head of Household, Qualifying Surviving Spouse — same 5 as federal
- PLUS: Registered Domestic Partners (RDPs) treated as married for all California purposes regardless of federal filing status
- RDP MFJ or MFS on California return while filing Single or HoH federally — different returns, different statuses
- December 31 determination date (same as federal)
- Community property states: California is a community property state; community income split 50/50 between spouses/RDPs for California income tax purposes

RESIDENCY — THE MOST CRITICAL CALIFORNIA-SPECIFIC DETERMINATION:
- Resident (R&TC §17014): person domiciled in California OR present in California for other than a temporary or transitory purpose; taxed on WORLDWIDE income
- Nonresident: domiciled outside California and not present for permanent/indefinite period; taxed ONLY on California-source income (R&TC §17951)
- Part-year resident: resident for part of the tax year; taxed on worldwide income during resident period AND California-source income during nonresident period
- Form 540NR used for nonresidents and part-year residents; Form 540 for full-year residents

DOMICILE VS RESIDENCE:
- Domicile: permanent home — place to which taxpayer intends to return; can have only one domicile
- Presence: physical presence for non-temporary purpose can create residency even without domicile in California
- Safe harbor (R&TC §17016): individual who is domiciled outside California and spends fewer than 9 months in California during the taxable year is presumed to be NOT a California resident — rebuttable presumption

DOMICILE FACTORS (FTB Pub. 1031 closest connections test):
- Location of spouse/children/dependents
- Location of principal residence
- State of voter registration
- State of vehicle registration
- Location of professional licenses
- Location of bank accounts and investments
- Location of social, religious, and professional memberships
- State of driver's license
No single factor is determinative; FTB considers the totality

SOURCING RULES:
- Wages/salary: sourced where services physically performed (R&TC §17951)
- Business/self-employment income: apportioned by sales-factor formula; market-based sourcing for services and intangibles (R&TC §§25120–25141)
- Rental income from California real property: California source always
- Capital gains from sale of California real property: California source always
- Capital gains from sale of intangibles (stocks, bonds, partnerships): sourced to taxpayer's state of residence — nonresidents generally not taxed
- Partnership/S-corp income: California-source determined at entity level; Schedule K-1 reflects California-source portion for nonresident partners/shareholders

NONRESIDENT WITHHOLDING:
- 7% withholding on California-source income paid to nonresidents (R&TC §18662)
- Form 592: Resident and Nonresident Withholding Statement (payer files with FTB)
- Form 592-B: Resident and Nonresident Withholding Tax Statement (issued to payee)

COMMUNITY PROPERTY:
- Community income (earned during marriage/RDP while domiciled in California) split 50/50
- MFS community property allocation: each spouse reports 50% of community income
- Full step-up in basis on both halves of community property at first spouse's/RDP's death (IRC §1014(b)(6), incorporated by conformity)

AGENT RULE: Before calculating California tax for any individual, determine residency status. A California resident owes California tax on income from every state and every country. A nonresident owes California tax only on California-source income. A single determination — residency — can change the California tax bill by hundreds of thousands of dollars for a high-income taxpayer.

TRAP: A person who claims to have "moved" to another state but continues spending the majority of their time in California, maintains their family home in California, and keeps children in California schools will be treated as a California resident. The FTB uses cell phone records, credit card records, airline records, E-ZPass data, and social media to verify physical presence. Documentary changes alone (new driver's license, new voter registration) are insufficient.

---

#### 00-ca-income-brackets-rates.md
R&TC Sections 17041, 17043; FTB annual rate schedules
**Citation:** 2025 California Tax Rate Schedules, FTB.ca.gov; 2025 Form 540 Instructions

Cover:

CALIFORNIA INDIVIDUAL INCOME TAX RATES — 9 BRACKETS:
| Rate | Filing Status | 2025 Taxable Income |
|------|--------------|---------------------|
| 1% | All | $0 – first bracket |
| 2% | | |
| 4% | | |
| 6% | | |
| 8% | | |
| 9.3% | | |
| 10.3% | | |
| 11.3% | | |
| 12.3% | | |

[NOTE TO BUILDER: Exact bracket thresholds by filing status must be pulled directly from the 2025 California Tax Rate Schedules PDF at ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf and the 2026 equivalent when published. The nine rates are confirmed; the income thresholds are inflation-adjusted annually. The 2025 document was not text-extractable; builder must render and transcribe the actual bracket tables.]

MENTAL HEALTH SERVICES TAX (R&TC §17043):
- Additional 1% surcharge on California taxable income EXCEEDING $1,000,000
- Threshold: $500,000 for MFS
- This threshold has NOT been adjusted for inflation since the Proposition 63 enactment in 2004
- Applied AFTER the bracket tax is computed; it is a surcharge, not a bracket
- Effective top combined rate: 13.3% (12.3% bracket + 1% MHS surcharge)
- MHS Tax CANNOT be offset by PTE elective tax credits

CAPITAL GAINS — CRITICAL DIFFERENCE FROM FEDERAL:
- California taxes ALL capital gains (short-term and long-term) at ordinary income rates
- There is NO 0%/15%/20% preferential rate schedule in California
- A taxpayer with $1,000,000 of long-term capital gain taxed at 20% federally is taxed at up to 13.3% in California — combined potential rate 33.3%
- Qualified dividends: also taxed at ordinary rates in California (no preferential rate)

STANDARD DEDUCTION (2025, per FTB.ca.gov 2025 Form 540 Instructions):
- Single or MFS: $5,706
- MFJ, HoH, Qualifying Surviving Spouse: $11,412

PERSONAL EXEMPTION CREDITS (2025, per FTB Form 540 2EZ Tax Table):
- Personal exemption credit: $153 per exemption
- Dependent exemption credit: $475 per qualifying dependent
- Senior/blind additional exemption: same $153 per qualifying exemption

AGENT RULE: California's 13.3% top rate is the highest state income tax rate in the United States. Combined with the 37% federal rate, a high-income California taxpayer faces a marginal rate exceeding 50% on ordinary income. Always model California tax separately and explicitly — never assume federal planning strategies reduce California tax proportionally.

TRAP: The Mental Health Services Tax threshold ($1,000,000) is not inflation-adjusted. It has been fixed since 2004. As nominal incomes rise, more taxpayers cross this threshold each year. It applies to the EXCESS above $1,000,000, not to the entire income amount.

---

### PART 1 — INCOME RECOGNITION

#### 01-ca-capital-gains-treatment.md
R&TC Sections 18152, 18152.5, 17024.5
**Citation:** R&TC §18152.5 (QSBS non-conformity); 2025 Schedule CA Instructions, FTB; CalCPA "Part 1: Time-Sensitive Tax Planning Under OBBBA" (2025)

- California taxes ALL capital gains at ordinary income rates — short-term and long-term
- Holding period: still tracked for federal purposes but produces NO rate differential on the California return
- Capital loss limitation: $3,000/year against ordinary income — California conforms to IRC §1211
- Wash sale rule: California conforms to IRC §1091
- QSBS exclusion (IRC §1202): California does NOT conform per R&TC §18152.5 — full gain taxable
  - OBBBA increased QSBS exclusion to $15,000,000 at federal level — California does not conform to ANY §1202 exclusion regardless of holding period
- Like-kind exchange (IRC §1031): California conforms to real property limitation
- Form FTB 3840: required when California real property exchanged for out-of-state property — annual reporting obligation until replacement property is sold
- California-source rules: gains from sale of California real property are California-source; gains from sale of intangibles (stocks, bonds) are sourced to taxpayer's state of residence

AGENT RULE: Never apply the federal 0%/15%/20% LTCG rate to a California calculation. All gain — short-term or long-term — is ordinary income in California. A California taxpayer who holds stock 10 years and sells for a $5,000,000 gain receives zero rate benefit in California.

TRAP: QSBS (Section 1202) exclusion is the single largest federal-California divergence for startup founders. A founder excluding $10,000,000 of QSBS gain federally owes California tax on the full $10,000,000 at ordinary rates up to 13.3%. The $1,330,000 California tax bill on income that is $0 federally is frequently a planning surprise.

---

#### 01-ca-property-sales-recapture.md
R&TC Sections 17024.5, 18100–18175
**Citation:** R&TC §§17250, 17255 (depreciation non-conformity basis for recapture differences)

- California conforms to the §1231/§1245/§1250 recapture framework in principle
- Critical difference: California depreciation base differs from federal — California allowed NO bonus depreciation and only $25,000 Section 179 (vs federal amounts)
- Effect: California adjusted basis is HIGHER than federal adjusted basis for assets that received bonus depreciation or excess Section 179 federally
- Effect on gain: California gain on sale is LOWER than federal gain (higher basis = lower gain)
- Unrecaptured §1250 gain: no 25% special rate in California — taxed at ordinary rates
- §1231 gain: no preferential LTCG rate in California — taxed at ordinary rates
- Form 3885A / Form 3885: California depreciation tracking; required whenever California depreciation differs from federal

AGENT RULE: Calculate California gain separately from federal gain on every business asset sale. Different depreciation history = different adjusted basis = different gain. Two gain calculations are always required.

---

#### 01-ca-basis-adjustments.md
R&TC Sections 17024.5, 18036, 18037, 18038; Form 3885A
**Citation:** 2025 Instructions for Form FTB 3885A, FTB.ca.gov

- Cost basis: California conforms to IRC §1012
- Adjusted basis: may differ from federal — California allowed no bonus depreciation and only $25,000 §179; California adjusted basis will be HIGHER for assets where federal took larger first-year deductions
- Gift basis (§1015): California conforms — carryover basis for gain; FMV if lower for loss
- Inherited basis (§1014): California conforms — step-up to FMV at date of death
- Community property full step-up: both halves of community property receive step-up at first death per IRC §1014(b)(6), incorporated by California through conformity; powerful California planning tool
- IRD: step-up does NOT apply to IRAs, 401(k)s, deferred compensation — fully taxable to beneficiary at ordinary rates; California conforms
- HSA basis: California does NOT recognize HSA accounts; contributions were never excluded from California income; distributions for medical expenses are NOT excluded; basis = all contributions made

AGENT RULE: Maintain two basis schedules for any depreciable business asset — one for federal, one for California. Use Form 3885A to reconcile California depreciation history.

TRAP: Community property full step-up is a critical California advantage. At the first spouse's death, the surviving spouse's half of community property ALSO gets a step-up — eliminating built-in gain on the entire asset. Separate property only gets a step-up on the decedent's half.

---

#### 01-ca-cancellation-of-debt.md
R&TC Sections 17131, 17131.4, 17131.8, 17144
**Citation:** R&TC §17131 (general COD inclusion); SB 711 conformity analysis

- General rule: COD income includable in California gross income — conforms to IRC §61(a)(12)
- Bankruptcy exclusion (IRC §108(a)(1)(A)): California conforms
- Insolvency exclusion (IRC §108(a)(1)(B)): California conforms
- Qualified farm debt (IRC §108(a)(1)(C)): California conforms
- QRPBI (qualified real property business indebtedness): California conforms
- Student loan forgiveness: California conforms to federal exclusion for qualifying programs
- Attribute reduction (IRC §108(b)): California conforms to ordering rules
- Form 982: California uses same Form 982 for attribute reduction reporting
- Nonrecourse debt foreclosure: no COD income (same as federal); difference between debt and FMV is §1001 gain

AGENT RULE: Verify each COD exclusion was not enacted after January 1, 2025. If a new federal COD exclusion was enacted via OBBBA or post-2025 legislation, it does not apply in California without separate California legislation.

---

#### 01-ca-cryptocurrency.md
R&TC §17024.5; FTB conformity to Notice 2014-21
**Citation:** FTB.ca.gov guidance on digital assets; 2025 Schedule CA Instructions

- California conforms to federal property treatment of cryptocurrency
- All federal taxable events are California taxable: sales, exchanges, mining/staking rewards, airdrops, DeFi swaps
- Critical difference: ALL crypto gains taxed at ordinary rates in California (no LTCG preference)
- Combined potential rate on long-term crypto gain: up to 33.3% (20% federal + 13.3% California)
- Basis: FIFO default, specific identification permitted — conforms
- California source: crypto gains are sourced to taxpayer's state of residence for nonresident analysis (intangible property rule)

---

#### 01-ca-social-security-exclusion.md
R&TC §17087
**Citation:** R&TC §17087; 2025 Schedule CA (540) Instructions, FTB.ca.gov

- California FULLY excludes Social Security benefits from California taxable income
- This is an absolute statutory exclusion — no combined income formula applies in California
- Railroad Tier 1 and Tier 2 retirement benefits: also excluded from California income
- Unemployment compensation: excluded from California income (R&TC §17083)
- Schedule CA Column C subtraction: subtract 100% of the amount on federal Form 1040 Line 6b
- Applies regardless of income level — a taxpayer with $5,000,000 of other income still excludes all Social Security

AGENT RULE: Always subtract the full amount of taxable Social Security (federal Form 1040 Line 6b) on Schedule CA. No calculation needed. This is unconditional.

TRAP: Do not apply any federal combined income test for California. There is no "up to 85% taxable" analysis in California — the answer is always 0% taxable.

---

### PART 2 — BUSINESS DEDUCTIONS AND CREDITS

#### 02-ca-depreciation-179-bonus.md
**Word limit: 2,000–2,500**
R&TC Sections 17201, 17250, 17255, 24349, 24356; Forms 3885A, 3885
**Citation:** 2025 Instructions for Form FTB 3885A, FTB.ca.gov; R&TC §17255; LSL CPAs "California Doesn't Play by Federal Rules" (2025); Aprio "California Updates IRC Conformity with SB 711" (2025)

BONUS DEPRECIATION:
- California has NEVER allowed bonus depreciation (IRC §168(k)) for any property in any year
- This predates TCJA; California decoupled from the original 30% and 50% bonus rates enacted in 2001–2002
- OBBBA restoration of permanent 100% bonus depreciation: not conformed; zero bonus allowed in California
- Schedule CA Column B: add back 100% of any bonus depreciation claimed on the federal return

SECTION 179:
- California limit: $25,000 (R&TC §17255)
- California phase-out: $200,000 threshold — §179 deduction reduced dollar-for-dollar when cost of §179 property exceeds $200,000
- Federal limit (OBBBA): $2,500,000; phase-out at $4,000,000
- Schedule CA Column B: add back any §179 deduction federally claimed above $25,000
- California amounts are NOT indexed for inflation; have been $25,000/$200,000 for many years
- Corporate: R&TC §24356 provides same $25,000/$200,000 California limits

MACRS:
- California conforms to MACRS recovery periods (5-year, 7-year, 15-year, 27.5-year, 39-year)
- Difference is solely in first-year treatment: no bonus, limited §179
- Example: a $100,000 machine placed in service in 2025
  - Federal: $100,000 deduction in year 1 (100% bonus under OBBBA)
  - California: Year 1 MACRS deduction only (approximately $20,000 for 5-year property)
  - Schedule CA Column B addition: $80,000 in year 1
  - California has higher basis going forward; smaller depreciation additions in subsequent years

LISTED PROPERTY:
- >50% business use required for MACRS/bonus: California conforms to §280F listed property rules
- Luxury auto limits: California conforms to §280F dollar caps but WITHOUT the federal bonus add-on
  - 2025 Year 1 California limit: $12,400 (no additional $8,000 bonus component)
  - Federal 2025 Year 1: $20,400 (with bonus)

QIP (Qualified Improvement Property):
- 15-year MACRS: California conforms
- 100% bonus on QIP: not allowed in California; regular 15-year depreciation applies

TRACKING REQUIREMENT:
- Form 3885A (individuals, estates, trusts): California depreciation — required whenever California depreciation differs from federal; tracks the running difference
- Form 3885 (corporations): same purpose for corporate returns

AGENT RULE: Every business asset placed in service by a California taxpayer requires TWO depreciation calculations — one federal, one California. The federal calculation uses bonus and full §179. The California calculation uses regular MACRS and $25,000 max §179. The difference is added back on Schedule CA each year until the asset is fully depreciated or sold.

TRAP: A business owner who claimed $500,000 of §179 federally on equipment purchases deducts only $25,000 in California. The $475,000 add-back creates California taxable income even if the federal return shows a loss. This is one of the most common reasons a small business owes California tax in a year with zero federal taxable income.

---

#### 02-ca-research-credit.md
R&TC Sections 17052.12, 23609; SB 711
**Citation:** SB 711 bill analysis, FTB.ca.gov; Cherry Bekaert "California R&D Tax Credit Planning Under SB 711" (2026); BDO "California Updates IRC Conformity and Research Credit Rules" (2025)

CALIFORNIA R&D CREDIT RATES:
- Regular credit: 24% of qualified research expenses (QREs) above base amount for in-house research
- Contract research: 12% of amounts paid to third parties for contract research
- Basic research payments: additional credit for payments to qualified universities

ALTERNATIVE SIMPLIFIED CREDIT (ASC) — NEW UNDER SB 711:
- Available for tax years beginning on or after January 1, 2025 (SB 711)
- California ASC rate: 3% of QREs above 50% of average annual QREs for prior 3 tax years
- Reduced rate: 1.3% if taxpayer had no QREs in any one of the prior 3 tax years
- Taxpayer elects ASC method; election is made annually

CALIFORNIA R&E EXPENSING — INDEPENDENT OF FEDERAL:
- California allows immediate deduction of all R&E expenditures — both domestic and foreign
- California NEVER adopted TCJA §174 mandatory 5-year (domestic) / 15-year (foreign) amortization
- California INDEPENDENTLY allows immediate expensing under its own R&TC provisions
- OBBBA §174A (restored domestic immediate expensing): same result in California but different legal basis — California's authority is independent of §174A

SB 167 CREDIT CAP:
- For tax years 2024–2026: aggregate business credits (excluding low-income housing credits) capped at $5,000,000 per tax year
- R&D credits subject to this cap
- Excess credits carry forward with extended carryforward period
- SB 175 revenue trigger: cap may not apply to 2025 and 2026 if California Director of Finance determines General Fund forecast is sufficient without the revenue from the suspension/cap

INTERACTION — §280C ELECTION:
- California R&D credit reduces the California R&E expense deduction unless taxpayer elects reduced credit rate (parallel to federal §280C)

CARRYFORWARD:
- Unused California R&D credits carry forward indefinitely

AGENT RULE: California's R&D credit rate (24% regular / 12% contract) is higher than the federal regular credit rate (20% / 6.5%). For R&D-intensive California businesses, the California credit is a significant benefit. But the $5,000,000 annual cap through 2026 limits utilization for large taxpayers.

---

#### 02-ca-nol-rules.md
R&TC Sections 17276, 17276.22, 17276.23, 24416; SB 167; SB 175
**Citation:** Moss Adams "California Enacts NOL Suspension and Credit Limitation Rules" (2024); RSM "California suspends NOLs and caps credit usage for three years" (2024); FTB.ca.gov NOL page

CALIFORNIA NOL RULES — PERMANENT STRUCTURE:
- Carryforward period: 20 years (R&TC §17276) — compare federal: unlimited carryforward
- Carryback: generally NOT allowed — exception: new businesses in first 3 years of operation, 2-year carryback
- 80% limitation: California does NOT conform to the federal 80%-of-taxable-income limitation; California NOLs can offset 100% of California taxable income (when not suspended)

NOL SUSPENSION — SB 167 (signed June 27, 2024):
- Suspended for tax years 2024, 2025, and 2026
- Applies to: individuals with net business income OR modified AGI of $1,000,000 or more; corporations with California taxable income of $1,000,000 or more
- Taxpayers below the $1,000,000 threshold are EXEMPT from the suspension — may still use NOL carryovers
- Suspended NOLs receive extended carryforward period (period is NOT lost):
  - Pre-2024 losses: 3 additional carryforward years
  - 2024 losses: 2 additional carryforward years
  - 2025 losses: 1 additional carryforward year

SB 175 REVENUE TRIGGER:
- As amended by SB 175: the NOL suspension will NOT apply to 2025 and 2026 tax years if the California Director of Finance determines the General Fund multi-year forecast is sufficient without the suspension revenue
- This is a potential early sunset — builder must verify whether the revenue trigger was activated for 2025 before finalizing document; check FTB.ca.gov for any Director of Finance determination

SECTION 461(l) EXCESS BUSINESS LOSS — NON-CONFORMITY:
- California does NOT conform to IRC §461(l) excess business loss limitation ($313,000/$626,000 federal cap)
- No similar California limitation exists
- A California business loss that would be capped at the federal level is fully usable in California (subject only to the NOL suspension if applicable)

AGENT RULE: For a California taxpayer with net business income or modified AGI above $1,000,000, NOL carryovers are suspended for 2024–2026. The NOL is not lost — it carries forward with extended period. But no current-year tax benefit is available during the suspension years.

TRAP: Three-layer federal limitation stack (§469 passive → §461(l) excess business loss → 80% NOL) has no California equivalent. A loss that survives all three federal filters may be freely usable in California (subject only to SB 167 suspension if income threshold met). The California loss landscape is more permissive.

---

#### 02-ca-home-office.md
R&TC Sections 17201, 17024.5, 17076
**Citation:** 2025 Instructions for Schedule CA (540), FTB.ca.gov; R&TC §17076

- Qualification requirements: California conforms to IRC §280A — regular and exclusive use as principal place of business or place to meet clients
- Self-employed: deduction on Schedule C; same as federal
- EMPLOYEES — CRITICAL CALIFORNIA DIFFERENCE:
  - Federal (post-TCJA/OBBBA): employee home office deduction completely eliminated
  - California: California did NOT conform to TCJA elimination of miscellaneous itemized deductions
  - California employees MAY deduct unreimbursed home office expenses as a miscellaneous itemized deduction subject to the 2% California AGI floor
  - This is a Schedule CA Column C subtraction for employees who itemize in California
- Simplified method: $5/sq ft, max 300 sq ft ($1,500 max) — California conforms

AGENT RULE: W-2 employees working from home cannot deduct home office expenses federally, but CAN deduct them in California as a miscellaneous itemized deduction. This is a meaningful California-specific benefit for remote workers.

---

#### 02-ca-se-tax-payroll.md
R&TC does not impose state self-employment tax; EDD administers payroll taxes
**Citation:** EDD "Contribution Rates, Withholding Schedules, and Meals and Lodging Values" (2025, 2026); EDD Contribution Rates and Benefit Amounts page

NO CALIFORNIA SELF-EMPLOYMENT TAX:
- California has no state self-employment tax
- SE tax is entirely a federal obligation (IRC §§1401/1402, Schedule SE)
- No California line on Form 540 for SE tax

CALIFORNIA PAYROLL TAXES — EMPLOYER AND EMPLOYEE OBLIGATIONS:

| Tax | Who Pays | Rate | Wage Base |
|-----|---------|------|-----------|
| PIT Withholding | Employee (employer withholds) | Per withholding tables | All wages |
| SDI (State Disability Insurance) | Employee | 1.2% (2025); 1.3% (2026) | No cap — all wages |
| UI (Unemployment Insurance) | Employer | Varies by experience (1.5%–6.2%) | $7,000/employee |
| ETT (Employment Training Tax) | Employer | 0.1% | $7,000/employee |

SDI NOTES:
- Wage base cap eliminated January 1, 2024 — SDI now applies to ALL wages with no ceiling
- Rate for 2025: 1.2%; rate for 2026: 1.3% (Source: EDD, CalChamber HRWatchdog Dec. 2025)
- High-wage employees pay significantly more SDI than under prior law (pre-2024 cap was $153,164)
- SDI withheld in excess of annual cap (applicable when employee has multiple California employers) is refundable on Form 540

WORKER CLASSIFICATION — AB 5 (DYNAMEX):
- California applies the ABC test to determine employee vs. independent contractor status
- Presumption is employment; contractor status requires ALL three prongs:
  - A: Worker is free from control of the hiring entity
  - B: Work is outside the usual course of the hiring entity's business
  - C: Worker is customarily engaged in an independently established trade or occupation
- The ABC test is stricter than the federal common law 20-factor test
- Misclassification penalties: Labor Code §226.8 — $5,000–$15,000 per violation for willful misclassification; $10,000–$25,000 for pattern/practice

AGENT RULE: SDI applies to all wages with no cap as of 2024. A California employee earning $500,000 pays $6,000 in SDI (2025). This is dramatically higher than pre-2024. Always use the no-cap rule for SDI calculations.

---

#### 02-ca-startup-costs.md
R&TC Sections 17201, 17024.5, 24365
- California conforms to IRC §195 (startup costs) and §248 (corporate organizational costs) through the January 1, 2025 conformity date
- $5,000 first-year deduction / 180-month amortization: same structure as federal
- New business NOL carryback: 2-year carryback available for new businesses in first 3 years; an exception to the general California no-carryback rule

---

#### 02-ca-meals-entertainment.md
R&TC Sections 17201, 17024.5, 24343
- Entertainment: 100% nondeductible — California conforms to post-TCJA federal rule
- Business meals: 50% deductible — California conforms
- Substantiation requirements: California conforms to five-element test
- OBBBA changes to §274: not conformed — irrelevant as OBBBA did not substantively change meals deductibility

---

#### 02-ca-hobby-loss-at-risk.md
R&TC Sections 17551, 17551.5
- §183 hobby loss: California conforms through conformity date — hobby income taxable, hobby expenses nondeductible
- §465 at-risk rules: California conforms through conformity date
- Phase-outs referencing AGI use California AGI (not federal AGI)

---

### PART 3 — PASSIVE ACTIVITIES AND REAL ESTATE

#### 03-ca-passive-activity-rules.md
R&TC Sections 17561, 17561.5
**Citation:** 2025 Instructions for Form FTB 3801, FTB.ca.gov

- California generally conforms to IRC §469 passive activity rules
- Seven material participation tests: California conforms (Reg. §1.469-5T)
- $25,000 rental loss allowance: California conforms — active participation; phase-out $100,000–$150,000 of California AGI (NOT federal AGI)
- Real estate professional exception (>750 hours): California conforms
- Suspended loss release on complete disposition: California conforms
- Grouping elections: California conforms
- Form FTB 3801: California Passive Activity Loss Limitations

AGENT RULE: California passive activity loss limitations use CALIFORNIA AGI for the $25,000 rental allowance phase-out. California AGI may differ from federal AGI, changing whether the allowance is fully available, partially available, or phased out.

---

#### 03-ca-real-estate-1031-cost-seg.md
R&TC Sections 18036, 24941–24955; Form FTB 3840
**Citation:** FTB.ca.gov real estate withholding page; 2025 Instructions for Form 593, FTB.ca.gov

SECTION 1031 LIKE-KIND EXCHANGE:
- California conforms to real property-only limitation (post-TCJA conformity via SB 711)
- 45-day identification / 180-day closing deadlines: conforms
- California clawback rule: if California real property is exchanged for out-of-state replacement property, the deferred California gain does NOT disappear
- Form FTB 3840: California Like-Kind Exchanges — required annual filing until replacement property is disposed of; FTB tracks and will assess the deferred California gain when replacement property is eventually sold
- Failure to file Form 3840: $500 per year penalty
- Related-party holding period: California conforms to 2-year requirement

COST SEGREGATION:
- California conforms to reclassification of building components into shorter-life personal property
- BUT: reclassified personal property does NOT qualify for California bonus depreciation ($0 allowed)
- California benefit of cost segregation is limited to shorter MACRS recovery periods only (not first-year expensing)

REAL ESTATE WITHHOLDING — FORM 593:
- 3⅓% withholding on total sales price for California real property sales by nonresidents
- Alternative: withhold at the applicable California rate on the computed gain (12.3% for individuals)
- Applies even if seller will owe no California tax (e.g., §121 exclusion applies)
- Seller must request withholding waiver or claim credit on Form 540NR
- Form 593 filed by settlement agent with FTB within 20 days after end of month in which transaction closed

AGENT RULE: Any 1031 exchange of California real property into out-of-state property requires annual Form FTB 3840 filings. This obligation follows the taxpayer (or successor) indefinitely until the replacement property is sold. Missing even one annual filing triggers a $500 penalty and may prompt FTB inquiry.

---

#### 03-ca-installment-sales.md
R&TC Sections 17024.5, 24667
- California conforms to IRC §453 installment method
- California gross profit ratio calculated independently from federal (California basis may differ)
- §453A interest on large obligations (>$5M): California conforms

---

### PART 4 — TAX CREDITS

#### 04-ca-credits-master.md
**Word limit: 3,000–4,000**
R&TC Sections 17052, 17052.1, 17052.6, 17053.5, 17053.98.1, 17054, 17054.5, 17058, 23609, 23636; Forms 3514, 3804-CR
**Citation:** FTB CalEITC page; FTB YCTC page; FTB.ca.gov (2025); SB 167 credit cap

SB 167 CREDIT CAP — APPLIES TO ALL BUSINESS CREDITS:
- For tax years 2024, 2025, and 2026: aggregate business credits (except low-income housing) capped at $5,000,000 per year
- Excess credits carry forward with extended carryforward period
- Revenue trigger (SB 175): cap may not apply to 2025/2026 if General Fund forecast is sufficient — verify before finalizing

CALIFORNIA EARNED INCOME TAX CREDIT (CalEITC) — R&TC §17052:
- Refundable; Form FTB 3514
- Tax year 2025 maximum credit: $3,756 (3+ qualifying children)
- Earned income limit: $32,900 (2025) — both earned income AND California AGI must be below this threshold
- Qualifying: requires earned income from employment or self-employment; investment income does not qualify
- Uses CALIFORNIA earned income figures, not federal EITC tables

YOUNG CHILD TAX CREDIT (YCTC) — R&TC §17052.1:
- Refundable; Form FTB 3514
- Tax year 2025 maximum: $1,189 per return
- Requires: CalEITC eligibility AND qualifying child under age 6 at end of tax year
- Available to zero-earned-income filers if wages do not exceed $35,640 and net loss does not exceed $35,640

FOSTER YOUTH TAX CREDIT (FYTC):
- Refundable; Form FTB 3514
- For former foster youth ages 18–25 who qualify for CalEITC
- Up to $1,189 (2025)

RENTER'S CREDIT — R&TC §17053.5:
- Nonrefundable; $60 (single/MFS) / $120 (MFJ/HoH/QSS) — 2025
- California AGI limits apply; California resident who paid rent for principal residence

CHILD AND DEPENDENT CARE CREDIT — R&TC §17052.6:
- Nonrefundable
- Percentage of federal credit based on California AGI
- Reduced by employer-provided dependent care exclusion

RESEARCH CREDIT — See 02-ca-research-credit.md

FILM/TELEVISION PRODUCTION CREDIT — Program 4.0 — R&TC §§17053.98.1/23698.1:
- One-time irrevocable election to receive refundable credit if credit exceeds tax liability
- Qualified production expenditures; allocation from California Film Commission
- SB 167 credit cap exemption status: verify — film credit may be subject to cap

LOW-INCOME HOUSING CREDIT — R&TC §§17058/23610.5:
- Nonrefundable
- EXEMPT from the SB 167 $5,000,000 annual credit cap
- 4-year carryforward

PTE ELECTIVE TAX CREDIT — See 06-ca-pte-elective-tax.md:
- Credit against personal California income tax for PTE elective tax paid at entity level
- Form 3804-CR; nonrefundable; 5-year carryforward
- Cannot offset Mental Health Services Tax

FEDERAL CREDITS WITH NO CALIFORNIA EQUIVALENT:
- Child Tax Credit (§24 / OBBBA $2,200): no California equivalent — California uses CalEITC/YCTC
- Premium Tax Credit (§36B): no California equivalent — Covered California administered separately
- Saver's Credit (§25B): no California equivalent
- AOTC / Lifetime Learning Credit: California has no equivalent higher education credits
- EV credits (§30D/§25E): California has separate clean vehicle programs independent of federal credits

AGENT RULE: California credits are applied in statutory order on Form 540. Nonrefundable credits cannot reduce tax below the tentative minimum tax (7% AMT). The SB 167 $5,000,000 cap on business credits must be verified each year to determine if revenue trigger has been activated.

TRAP: CalEITC and YCTC use CALIFORNIA-specific thresholds and earned income definitions. Never apply federal EITC tables to a California return. The income limits, credit amounts, and phase-outs differ.

---

### PART 5 — RETIREMENT

#### 05-ca-retirement.md
R&TC Sections 17501, 17085, 17501.5
**Citation:** 2025 Form 540 Instructions, FTB.ca.gov

CONTRIBUTIONS — CALIFORNIA CONFORMITY:
- 401(k)/403(b)/457(b): California conforms to deferral limits and employer contribution limits (SECURE 2.0 catch-up amounts)
- Traditional IRA: California conforms to deductibility phase-outs
- Roth IRA: California conforms to income phase-outs and non-taxability of qualified distributions
- SEP-IRA/SIMPLE IRA: California conforms
- HSA: California does NOT conform — contributions not deductible; distributions not excluded

DISTRIBUTIONS — CALIFORNIA CONFORMITY WITH ONE MAJOR ADDITION:
- RMDs: California conforms to SECURE 2.0 starting ages (73 for those born 1951–1959; 75 for born 1960+)
- 10% federal early withdrawal penalty: federal-only; not a California provision
- California 2.5% additional early distribution tax (R&TC §17085(c)): SEPARATE California tax on premature distributions (before age 59½) — assessed in ADDITION to the 10% federal penalty
- Exceptions to California 2.5% tax: generally parallel federal exceptions; verify each exception independently
- Combined penalty on unexcepted early distribution: 10% federal + 2.5% California = 12.5% total, plus income tax at both levels
- Roth conversions: taxable as ordinary income in California; conforms to federal treatment
- Backdoor Roth: pro-rata rule applies in California; Form 8606 tracks basis

CALIFORNIA PENSION TREATMENT:
- CalPERS, CalSTRS (California government pensions): fully taxable to California residents — no state pension exclusion
- Federal government pension: taxable to California residents; Davis v. Michigan (1989) prohibits taxing federal pensions of NONRESIDENTS but does NOT exempt California residents

AGENT RULE: Early distributions trigger BOTH the 10% federal penalty AND the 2.5% California additional tax. Total penalty before income tax is 12.5%. This is frequently overlooked in distribution planning.

---

### PART 6 — ENTITIES AND PAYROLL

#### 06-ca-entity-comparison-llc-fees.md
**Word limit: 2,500–3,500**
R&TC Sections 17941, 17942, 17935, 23151, 23153, 23221, 23802
**Citation:** FTB Pub. 3556 "LLC Filing Information" (2025), FTB.ca.gov; R&TC §17942; 2025 Instructions Form FTB 3536, FTB.ca.gov

MINIMUM FRANCHISE TAX — $800 ANNUAL:
- Every LLC, LP, LLP, and corporation doing business in California: $800 annual minimum tax
- R&TC §17941 (LLCs), §23153 (corporations)
- Due: 15th day of the 4th month of the taxable year
- First-year exemption (AB 85): applied only to entities formed January 1, 2021 through December 31, 2023 — EXPIRED; entities formed on or after January 1, 2024 owe $800 in their first year of existence
- S-corps: minimum $800 OR 1.5% of net income, whichever is greater (R&TC §23802)
- C-corps: minimum $800 OR 8.84% of net income, whichever is greater (R&TC §23151)
- LLC members: $800 minimum is in addition to the LLC fee

LLC ANNUAL FEE — R&TC §17942:
Based on total income from all sources derived from or attributable to California:

| Total California Income | Annual Fee |
|------------------------|------------|
| Under $250,000 | $0 |
| $250,000 – $499,999 | $900 |
| $500,000 – $999,999 | $2,500 |
| $1,000,000 – $4,999,999 | $6,000 |
| $5,000,000 or more | $11,790 |

Source: R&TC §17942; FTB Pub. 3556 (2025)

- "Total income" = gross receipts, NOT net income — a high-revenue, low-margin LLC faces full fee
- Estimated fee due: 15th day of 6th month (June 15 for calendar year) — Form FTB 3536
- Fee is IN ADDITION to the $800 minimum tax

ENTITY COMPARISON TABLE:
| Entity Type | California Tax | Rate/Minimum | Form | LLC Fee | QBI Deduction |
|-------------|---------------|-------------|------|---------|---------------|
| Sole Proprietor | Personal income tax | Up to 13.3% | 540 + Sch C | N/A | None |
| SMLLC | Personal income tax (disregarded) | Up to 13.3% | 540 + Sch C | Yes + $800 | None |
| Multi-Member LLC | Partnership taxation | Pass-through | 565 | Yes + $800 | None |
| S-Corp | 1.5% net income (min $800) | 1.5% | 100S | N/A | None |
| C-Corp | 8.84% of net income | 8.84% (min $800) | 100 | N/A | None |
| Partnership | Pass-through | Per partners | 565 | N/A | None |

NOTE: No entity receives a California QBI deduction — §199A does not exist in California.

CHECK-THE-BOX: California follows federal entity classification elections (Form 8832); no separate California election form required.

AGENT RULE: An LLC earning $5,000,000 in California revenue owes $11,790 LLC fee + $800 minimum tax = $12,590 in annual California minimums before any income tax. These are due even in a loss year. Budget for these fixed obligations.

TRAP: The LLC fee is based on TOTAL INCOME (gross revenue), not net profit. A business with $5,000,000 in revenue and a $100,000 net loss still owes the $11,790 fee. This catches many LLC owners off guard.

---

#### 06-ca-scorp.md
R&TC Sections 23800–23813; Form 100S
**Citation:** FTB.ca.gov S-Corps page; FTB S Corporation Manual Chapter 4

- California S election: follows federal S election automatically; opt-out available via Form FTB 3560
- Tax rate: 1.5% on California net income (minimum $800)
- Financial institution S-corps: 3.5% rate
- No QBI deduction: S-corp shareholders receive no California §199A deduction
- Reasonable compensation: California follows federal requirement — FTB may recharacterize distributions as wages
- Built-in gains tax: California conforms to §1374; 5-year recognition period after C-to-S conversion; taxed at highest California corporate rate
- Form 100S: California S Corporation Franchise or Income Tax Return
- Schedule K-1 (100S): issued to shareholders; reflects California-source income
- Form 7203: shareholder stock/debt basis — California requires same tracking

---

#### 06-ca-pte-elective-tax.md
R&TC Sections 19900–19907; AB 150; SB 132; Forms 3804, 3804-CR, 3893
**Citation:** FTB "Pass-Through Entity Elective Tax" page (FTB.ca.gov); SB 132 bill analysis, FTB.ca.gov; HCVT "Changes to California Pass-Through Entity Tax" (2025)

PURPOSE — SALT CAP WORKAROUND:
- Federal SALT cap ($40,000 under OBBBA for 2025–2029) limits deductibility of state taxes paid by individuals
- PTE elective tax bypasses this cap: the entity pays California income tax at the entity level; the entity deducts it as a business expense (IRS Notice 2020-75); partners/shareholders receive a California credit
- Result: the California state tax becomes a federal business deduction without SALT cap limitation

MECHANICS:
- Eligible entities: S-corps, partnerships, LLCs taxed as partnerships (not publicly traded partnerships; not combined reporting group members)
- Tax rate: 9.3% on qualified net income — the sum of each qualified taxpayer's pro-rata/distributive share and guaranteed payments subject to California PIT
- Qualified taxpayers: individuals, trusts, estates, and certain pass-through entities that are partners/shareholders/members

PAYMENT AND FORMS:
- Form 3893: Pass-Through Entity Elective Tax Payment Voucher — used for estimated payments
- Form 3804: Pass-Through Entity Elective Tax Calculation — filed with entity's return; makes the election
- Form 3804-CR: Pass-Through Entity Elective Tax Credit — claimed by each qualified taxpayer on their Form 540

PAYMENT TIMELINE:
- Payment 1 (June 15): greater of $1,000 or 50% of prior-year PTE tax
- Payment 2: remaining balance due by original return due date (March 15 for S-corps/partnerships; September 15 with extension)

SB 132 CHANGES (effective January 1, 2026):
- Prior law: failure to make full June 15 Payment 1 disqualified the entity from making the election
- SB 132: failure to make or fully make Payment 1 no longer disqualifies; instead, the qualified taxpayer's credit is reduced by 12.5% of their pro-rata share of the underpaid amount as of June 15
- Extension: SB 132 extends the PTE election through tax years beginning before January 1, 2031

CREDIT:
- Form 3804-CR: nonrefundable credit against California personal income tax
- Excess credit carryforward: 5 years
- CANNOT offset Mental Health Services Tax

FEDERAL TREATMENT:
- Entity-level PTE tax is deductible by the entity as a state tax business expense
- Reduces federal K-1 income to partners/shareholders
- Partners/shareholders report lower federal income; effectively bypass the SALT cap

AGENT RULE: For every California S-corp or partnership with qualified taxpayer owners, model the PTE election. Compare (1) no election — state tax limited by federal SALT cap; (2) election — entity deducts state tax federally, owners get California credit. Election is generally beneficial for owners with federal marginal rates above approximately 22%.

TRAP: The PTE credit cannot offset the Mental Health Services Tax. A partner with $2,000,000 of PTE income will have the 1% MHS Tax (approximately $10,000 on income above $1M) remaining after applying the PTE credit.

---

#### 06-ca-payroll-edd.md
EDD requirements; Labor Code; AB 5
**Citation:** EDD "Contribution Rates, Withholding Schedules" (2025, 2026); EDD.ca.gov

- SDI: 1.2% (2025), 1.3% (2026), no wage cap — employee-paid, employer-withholds
- UI: employer-only; 1.5%–6.2% experience-rated; $7,000 taxable wage base
- ETT: 0.1% on first $7,000; employer-only
- Form DE 9/DE 9C: quarterly employer payroll reports to EDD
- AB 5 ABC test: see 00-ca-two-system-framework.md or 02-ca-se-tax-payroll.md for full treatment
- Penalty for willful misclassification: $5,000–$15,000 per violation; $10,000–$25,000 for pattern/practice (Labor Code §226.8)

---

### PART 7 — ESTATE, GIFT, AND TRUSTS

#### 07-ca-no-estate-gift-tax.md
**Citation:** California Proposition 6 (1982); R&TC (no estate/gift provisions)

- California has NO state estate tax — repealed by Proposition 6, effective June 8, 1982
- California has NO state gift tax
- California has NO state generation-skipping transfer tax
- Federal estate/gift/GST taxes apply to California residents at federal rates (Form 706, Form 709)
- California estate tax return: does NOT exist — no filing obligation
- Inheritance received: not California taxable income to beneficiary (conforms to IRC §102)
- Income earned by estate after death: taxable on California Form 541
- Community property full step-up: critical California advantage — both halves of community property receive stepped-up basis at first death (IRC §1014(b)(6))
- Planning focus for California clients: entirely on federal unified credit and California income tax consequences of inherited assets; no state estate tax to plan around

---

#### 07-ca-trust-tax.md
R&TC Sections 17041(d), 17742–17745; Form 541
**Citation:** Legal Ruling 2019-02, FTB; 2025 Instructions for Form 541, FTB.ca.gov

RESIDENT vs. NONRESIDENT TRUST:
- California taxes trusts based on residency of TRUSTEE and BENEFICIARIES and source of income
- If ALL trustees are non-California residents AND all non-contingent beneficiaries are non-California residents AND no California-source income: generally no California tax
- If any non-contingent beneficiary is a California resident: proportionate share of accumulated income may be subject to California tax (Legal Ruling 2019-02 proportionate allocation method)

TAX RATES:
- Trusts use the same California rate schedule as individuals — brackets are compressed (same bracket thresholds as for individuals, which are very narrow at lower income levels)
- 12.3% top rate; plus 1% MHS Tax on trust income exceeding $1,000,000
- Strong incentive to distribute income to lower-bracket beneficiaries before year-end

GRANTOR TRUST:
- California conforms to federal grantor trust rules (§§671–679) — grantor taxed as owner
- Revocable trusts: grantor trust; income reported on grantor's return

FORM 541:
- California Fiduciary Income Tax Return
- Due: April 15; 5-month extension available (September 15)
- Schedule K-1 (541) to beneficiaries

NING TRUSTS:
- Nevada Incomplete Non-Grantor (NING) trusts do NOT achieve California income tax avoidance if the settlor or beneficiaries remain California residents
- FTB will apply Legal Ruling 2019-02 proportionate allocation to California-resident beneficiaries

AGENT RULE: A trust with California-resident non-contingent beneficiaries cannot escape California taxation on accumulated income regardless of where the trust is formed or where the trustee is located.

---

### PART 8 — CALIFORNIA-SPECIFIC PROVISIONS

#### 08-ca-itemized-deductions.md
**Word limit: 2,500–3,500**
R&TC Sections 17073.5, 17076, 17201, 17220, 17275; Schedule CA Part II
**Citation:** 2025 Instructions for Schedule CA (540), FTB.ca.gov; CalCPA "Part 1: Time-Sensitive Tax Planning Under OBBBA" (2025)

SALT — NO DEDUCTION FOR CALIFORNIA TAXES ON CALIFORNIA RETURN:
- California taxpayers cannot deduct California state income taxes on their California return (circular deduction)
- Real property taxes paid to California: deductible on the California return (no SALT cap applies at the California level)
- Other state income taxes (taxes paid to states other than California): deductible on California return — not subject to any cap
- Federal SALT cap ($40,000 under OBBBA / $10,000 prior): has NO application to the California return

PTET (PASS-THROUGH ENTITY TAX) WORKAROUND:
- IRS Notice 2020-75 approved entity-level PTE taxes as a federal deduction without SALT cap
- California's PTE elective tax qualifies — owners' California PIT is paid at entity level and deducted federally as a business expense
- See 06-ca-pte-elective-tax.md

MORTGAGE INTEREST:
- California conforms to $750,000 acquisition debt limit (via SB 711 TCJA conformity)
- Home equity interest: deductible only if proceeds used to buy/build/improve qualified home
- OBBBA made the $750,000 cap permanent federally: same result in California through pre-existing conformity

CHARITABLE CONTRIBUTIONS:
- California uses 50% AGI limit for cash gifts to public charities (NOT 60% as under prior federal law)
- Capital gain property: 30% AGI limit
- 5-year carryforward
- Written acknowledgment required for gifts of $250+; qualified appraisal for noncash gifts >$5,000
- OBBBA charitable changes (0.5% AGI floor, 35% rate cap for 37% bracket taxpayers): California does NOT conform — no floor, no rate cap

MEDICAL EXPENSES:
- California conforms to 7.5% AGI floor (using California AGI)

MISCELLANEOUS ITEMIZED DEDUCTIONS — CRITICAL CALIFORNIA DIFFERENCE:
- California did NOT conform to TCJA/OBBBA elimination of miscellaneous itemized deductions
- Still deductible in California subject to 2% of California AGI floor:
  - Unreimbursed employee business expenses (including home office)
  - Investment advisory fees
  - Tax preparation fees
  - Safe deposit box fees
  - Other qualifying miscellaneous expenses
- Schedule CA Part II Column C: subtract the California-allowed miscellaneous deductions

CASUALTY LOSSES:
- California conforms to federally-declared disaster requirement post-TCJA
- California also allows deductions for state-declared disasters (Governor proclamations)
- Recent California disasters (wildfires, flooding, landslides): check for active FTB disaster loss relief provisions
- $100 per-casualty floor and 10% AGI floor apply

HIGH-INCOME LIMITATION ON ITEMIZED DEDUCTIONS:
- California applies its own Pease-like limitation for high-income taxpayers
- Reduces itemized deductions by the lesser of: (a) 6% of California AGI in excess of threshold, OR (b) 80% of otherwise allowable itemized deductions
- [NOTE TO BUILDER: Verify the 2025 threshold for this limitation directly from 2025 Schedule CA instructions — the specific AGI threshold must be confirmed]

AGENT RULE: California itemized deductions require a completely separate calculation from federal. Three major differences: (1) no SALT cap; (2) miscellaneous itemized deductions survive at 2% floor; (3) California state income taxes are not deductible on the California return. Always evaluate itemized vs. standard deduction separately for each return.

---

#### 08-ca-amt.md
R&TC Sections 17062, 17063; Schedule P (540)
**Citation:** 2025 Form 540 Instructions, FTB.ca.gov (AMT exemption amounts extracted)

CALIFORNIA INDIVIDUAL AMT:
- Rate: 7% flat on AMTI above exemption (vs. federal 26%/28%)
- 2025 Exemption Amounts (Source: 2025 Form 540 Instructions, FTB):
  - Single or Head of Household: $92,749
  - Married/RDP Filing Jointly or Qualifying Surviving Spouse: $123,667
  - Married/RDP Filing Separately: $61,830
- [NOTE TO BUILDER: Verify 2026 exemption amounts when published; these are indexed annually]

AMT ADD-BACKS (items added to California taxable income for AMTI):
- Standard deduction (if taken)
- State income tax deduction (if itemized)
- Miscellaneous itemized deductions
- Depreciation difference (GDS vs ADS) — calculated independently using California depreciation basis, not federal
- ISO exercise spread: preference item in California; triggers California AMT
- Percentage depletion in excess of adjusted basis

AMT CREDIT (R&TC §17063):
- Credit for California AMT paid due to timing items (not exclusion items)
- Carries forward indefinitely
- Offsets future California regular tax when it exceeds California AMT

CORPORATE AMT:
- California corporate AMT: 6.65% rate; separate from individual AMT
- Federal corporate AMT (15% on adjusted financial statement income): California does NOT conform

AGENT RULE: California's 7% AMT rate is far lower than federal 26%/28%. Fewer California taxpayers trigger AMT than federal. But ISO exercise is a common California AMT trigger — model both regular tax and AMT when clients exercise ISOs.

---

#### 08-ca-estimated-tax-penalties.md
R&TC Sections 19136, 19131, 19132, 19133, 19164, 19187
**Citation:** 2025/2026 Instructions for Form 540-ES, FTB.ca.gov

ESTIMATED TAX REQUIREMENTS:
- Required if expected California tax owed ≥ $500 (after withholding and credits)
- $500 threshold — lower than federal's $1,000
- Due dates: April 15, June 15, September 15, January 15 (same calendar as federal)
- Form 540-ES; or pay via FTB Web Pay

SAFE HARBORS:
- 90% of current year California tax, OR
- 100% of prior year California tax
- 110% if prior year California AGI exceeded $150,000 ($75,000 for MFS)

PENALTY RATES:
| Penalty | Code Section | Rate | Maximum |
|---------|-------------|------|---------|
| Late filing | R&TC §19131 | 5%/month of unpaid tax | 25% |
| Late payment | R&TC §19132 | 0.5%/month | 25% |
| Underpayment of estimated tax | R&TC §19136 | Per quarter; federal underpayment rate | — |
| Demand to file | R&TC §19133 | $14,600 (2025) flat penalty | — |
| Accuracy-related | R&TC §19164 | 20% of underpayment | — |
| Fraud | R&TC §19187 | 75% of underpayment | — |

INTEREST:
- FTB charges interest at the federal underpayment rate; compounded daily
- Continues to accrue during OTA protests and appeals — not tolled

AGENT RULE: California's $500 estimated tax threshold is lower than the federal $1,000. Many more California taxpayers must make estimated payments. Failure to use the 110% safe harbor for prior-year California AGI above $150,000 can result in underpayment penalties even when total tax is paid.

---

#### 08-ca-audit-appeals.md
R&TC Sections 19057, 19058, 19059, 19060, 19331, 19381–19385; Government Code §§15670–15674
**Citation:** FTB Manual of Audit Procedures, Chapter 4 (MAP); FTB.ca.gov audit procedures; OTA.ca.gov

STATUTE OF LIMITATIONS — ASSESSMENT:
| Situation | California SOL | R&TC Authority |
|-----------|---------------|----------------|
| General rule | 4 years from later of return due date or filing date | §19057 |
| 25% or more income omission | 6 years | §19058 |
| No return filed | Unlimited | §19060 |
| Fraudulent return | Unlimited | §19060 |
| Federal change not reported | Extended 2 years from date of federal report | §18622 |

FEDERAL CHANGE REPORTING (R&TC §18622):
- Taxpayer must report federal adjustments to FTB within 6 months of federal determination becoming final
- Vehicle: amended California return (Form 540X) or authorized statement
- Failure to report: California SOL remains open indefinitely on those items
- This is the most commonly missed California filing requirement

AUDIT TYPES:
- Correspondence audit: document request by mail; most common
- Office audit: taxpayer comes to FTB
- Field audit: FTB examines taxpayer's books at business location
- Residency audit: special FTB program for high-income taxpayers claiming to have left California

PROTEST PROCESS:
- Notice of Proposed Assessment (NPA): FTB's equivalent of federal 90-day letter
- 60 days to file protest from NPA date
- FTB Settlement Bureau may negotiate resolution
- Notice of Action (NOA): FTB's final determination after protest

APPEALS — OFFICE OF TAX APPEALS (OTA):
- Independent agency; replaced State Board of Equalization tax appeals in 2018
- 30 days from NOA to file appeal with OTA
- 3-judge panel; oral hearings available
- Designated opinions are precedential

JUDICIAL REVIEW:
- After OTA: Superior Court (pay first, file for refund; or pay under protest)
- No direct equivalent of Tax Court petition without payment

COLLECTION:
- Installment agreements available
- Offer in Compromise (R&TC §19443): doubt as to collectibility, doubt as to liability, effective tax administration
- State tax liens and levies: FTB has independent authority

AGENT RULE: California's SOL is 4 years — one year longer than the federal 3-year general period. And if a federal audit results in changes, those changes must be reported to California within 6 months. Missing this 6-month window keeps the California SOL open indefinitely on the affected items.

TRAP: The 6-month federal change reporting rule is the single most commonly missed California compliance obligation. Every IRS audit closing agreement or revenue agent report must trigger a calendar reminder to file California Form 540X within 6 months.

---

#### 08-ca-nonresident-withholding.md
R&TC Sections 18662, 18666; Form 592, 592-B, 593
**Citation:** FTB "Real estate withholding" page; 2025 Instructions for Form 593, FTB.ca.gov; 2025 Instructions for Form 592, FTB.ca.gov

NONRESIDENT WITHHOLDING — GENERAL (7%):
- Required on California-source payments to nonresidents (R&TC §18662)
- Applies to: services performed in California, California rents, royalties, gambling winnings
- Rate: 7% of gross payment
- Payer files Form 592 with FTB; issues Form 592-B to payee
- Failure to withhold: payer is personally liable for the amount not withheld

REAL ESTATE WITHHOLDING — FORM 593:
- 3⅓% of total selling price, OR
- At the applicable California personal income tax rate on computed gain (typically 12.3% for individual sellers)
- Applies to all California real property sales regardless of seller's residency status
- Applies even when §121 exclusion applies — seller must claim waiver or credit
- Settlement agent files Form 593 with FTB within 20 days after end of month of closing
- Withholding waiver: seller may request reduced or eliminated withholding from FTB before closing

AGENT RULE: Real estate withholding (Form 593) applies to both resident and nonresident sellers. A California resident selling their primary residence and claiming the §121 exclusion still has 3⅓% withheld unless they request a withholding waiver in advance of closing.

---

#### 08-ca-pte-salt-planning.md
R&TC Sections 19900–19907; IRS Notice 2020-75
**Citation:** FTB PTE Elective Tax page; Deloitte "Considerations for California's Pass-Through Entity Tax"; HCVT analysis (2025)

Planning-focused document (see 06-ca-pte-elective-tax.md for mechanics). Cover:
- Break-even analysis: PTE election beneficial when owner's federal marginal rate × SALT overhang exceeds cost of accelerated state payment
- Modeling example: owner with $500,000 California K-1 income; SALT cap prevents deducting state tax federally; PTE election converts $46,500 state tax to full federal deduction
- Multi-state considerations: credit for taxes paid to other states — does the other state allow a credit for California PTE taxes passed through?
- Credit ordering on Form 540: PTE credit applied after other nonrefundable credits; cannot offset MHS Tax
- Guaranteed payments: included in qualified net income for PTE base — important for service partnerships

---

### PART 9 — SB 711 CONFORMITY REFERENCE

#### 09-ca-sb711-changes.md
**Word limit: 3,000–4,000**
SB 711 (Conformity Act of 2025), signed October 1, 2025
**Citation:** SB 711 bill analysis, FTB.ca.gov; KPMG Tax News Flash (October 2025); Grant Thornton SALT alert (October 2025); Aprio "California Updates IRC Conformity with SB 711" (2025); Baker Tilly "California's 2025 IRC conformity update" (2025)

Organize as:
1. Conformity date change: 2015 → 2025 and its practical meaning
2. Specific items newly conformed (practitioners must remove prior-year Schedule CA adjustments for these)
3. Specific items still non-conformed despite the date update (practitioners must retain Schedule CA adjustments)
4. OBBBA provisions — complete list, all non-conformed
5. R&D credit ASC changes (SB 711 §2)
6. Banking/financial institution apportionment changes

See 00-ca-conformity-master.md for the master non-conformity table. This document provides the narrative and legislative history.

---

### PART 10 — ADVANCED

#### 10-ca-residency-audit-defense.md
FTB Pub. 1031; Legal Ruling 2019-02; R&TC §§17014–17016
**Citation:** FTB Pub. 1031 "Guidelines for Determining Resident Status"; FTB Residency Audit procedures

Cover:
- FTB residency audits: FTB has dedicated high-wealth audit teams; California is one of the most aggressive states in auditing residency claims
- Burden of proof: taxpayer bears burden to prove non-California residency by clear and convincing evidence
- Evidence FTB examines: cell phone records, credit card transactions, airline records, E-ZPass/toll records, social media check-ins, school enrollment of children, medical provider records, charitable donation addresses, gym/club memberships
- Safe harbor: <9 months physical presence + domicile outside California = rebuttable presumption of nonresidency (R&TC §17016)
- Departure year: all California connections must be severed; new state connections affirmatively established; documentation of each day's location maintained for at least 4 years
- NING trusts: do not work for California residents; FTB applies Legal Ruling 2019-02

---

#### 10-ca-credit-other-states.md
R&TC Sections 18001–18006; Schedule S
**Citation:** 2025 Schedule S Instructions, FTB.ca.gov

- California residents who pay income tax to another state on the same income taxed by California may claim a credit to prevent double taxation
- Credit equals the LESSER of: (a) net income tax paid to the other state on the double-taxed income, or (b) California tax attributable to the same income
- Schedule S: Other State Tax Credit
- Credit cannot offset Mental Health Services Tax
- Cannot be applied against California corporate franchise minimum tax
- S-corp/partnership: credit flows through to individual owners for taxes paid by the entity at the entity level in other states (coordinate with PTE mechanics)

---

#### 10-ca-penalties-detailed.md
R&TC Sections 19131–19187
(Extended penalty reference — expands on 08-ca-estimated-tax-penalties.md to cover all penalty types with amounts, bases, and reasonable cause defenses)

---

### PART 11 — FORMS REFERENCE

#### 11-ca-forms-reference.md
**Word limit: 3,000–4,000**

Alphabetical/numerical table. For each form: number, full name, purpose, who files, due date, e-file threshold.

Must include at minimum:
Form 100, Form 100S, Form 100W, Form 100-ES, Form 109, Form 199, Form 540, Form 540NR, Form 540-ES, Form 540X (amended), Form 541, Form 565, Form 568, Form 588, Form 589, Form 590, Form 592, Form 592-B, Form 593, Form 3500, Form 3500A, Form 3502, Form 3510, Form 3514, Form 3519, Form 3520-BE, Form 3522 (LLC tax voucher), Form 3531, Form 3536 (LLC estimated fee), Form 3537, Form 3539, Form 3540, Form 3541, Form 3560 (S election opt-out), Form 3801 (passive activity losses), Form 3803, Form 3805E (installment sales), Form 3805V (NOL), Form 3805Z, Form 3840 (like-kind exchange out-of-state), Form 3843, Form 3853, Form 3885 (corporate depreciation), Form 3885A (individual depreciation), Form 3893 (PTE payment voucher), Form 3804 (PTE election), Form 3804-CR (PTE credit), Form 5805, Form 5805F, Schedule CA (540), Schedule CA (540NR), Schedule D (540), Schedule P (540) (AMT), Schedule R (apportionment), Schedule S (other state credit), Schedule K-1 (100S), Schedule K-1 (541), Schedule K-1 (565), Schedule K-1 (568), DE 4, DE 9, DE 9C, DE 542

---

## Build Order

1.  00-ca-two-system-framework.md     (conceptual foundation — everything depends on this)
2.  00-ca-conformity-master.md        (conformity table — all other documents reference this)
3.  00-ca-gross-income-definition.md
4.  00-ca-tax-calculation-waterfall.md
5.  00-ca-filing-status-residency.md
6.  00-ca-income-brackets-rates.md
7.  09-ca-sb711-changes.md            (current law baseline for 2025 returns)
8.  01-ca-capital-gains-treatment.md
9.  01-ca-property-sales-recapture.md
10. 01-ca-basis-adjustments.md
11. 01-ca-cancellation-of-debt.md
12. 01-ca-cryptocurrency.md
13. 01-ca-social-security-exclusion.md
14. 02-ca-depreciation-179-bonus.md
15. 02-ca-research-credit.md
16. 02-ca-nol-rules.md
17. 02-ca-startup-costs.md
18. 02-ca-home-office.md
19. 02-ca-se-tax-payroll.md
20. 02-ca-meals-entertainment.md
21. 02-ca-hobby-loss-at-risk.md
22. 03-ca-passive-activity-rules.md
23. 03-ca-real-estate-1031-cost-seg.md
24. 03-ca-installment-sales.md
25. 04-ca-credits-master.md
26. 05-ca-retirement.md
27. 06-ca-entity-comparison-llc-fees.md
28. 06-ca-scorp.md
29. 06-ca-pte-elective-tax.md
30. 06-ca-payroll-edd.md
31. 07-ca-no-estate-gift-tax.md
32. 07-ca-trust-tax.md
33. 08-ca-itemized-deductions.md
34. 08-ca-amt.md
35. 08-ca-estimated-tax-penalties.md
36. 08-ca-audit-appeals.md
37. 08-ca-nonresident-withholding.md
38. 08-ca-pte-salt-planning.md
39. 10-ca-residency-audit-defense.md
40. 10-ca-credit-other-states.md
41. 10-ca-penalties-detailed.md
42. 11-ca-forms-reference.md          (last — cross-references all prior documents)

---

## Corrections Log (v1.0 → v2.0)

The following errors were found and corrected during the v2.0 research pass:

| Item | v1.0 (Wrong) | v2.0 (Correct) | Source |
|------|-------------|----------------|--------|
| SDI rate 2025 | 1.1% | 1.2% | EDD.ca.gov |
| SDI rate 2026 | Not provided | 1.3% | EDD / NFP legislative monitor |
| Personal exemption credit | $144 | $153 | FTB Form 540 2EZ Tax Table 2025 |
| Dependent exemption credit | $446 | $475 | FTB Form 540 2EZ Tax Table 2025 |
| CA AMT exemptions | "Significantly lower than federal" (no figures) | $92,749 / $123,667 / $61,830 (2025) | 2025 Form 540 Instructions, FTB |
| PTE forms cited | Form 3893 only | Forms 3804, 3804-CR, AND 3893 | FTB PTE page |
| "Federal Baseline" framing | Implied California tax derived from federal | Two separate, parallel, independent systems | R&TC §17024.5 structure |
| SB 175 revenue trigger | Mentioned but not explained | Explained: Director of Finance determination can eliminate NOL suspension for 2025/2026 | RSM / Moss Adams / Grant Thornton analyses |
| Section 179 phase-out | Not stated | $200,000 threshold (R&TC §17255) | R&TC §24356; Intuit practitioner support |

## Items Requiring Builder Verification Before Finalizing Documents

The following items were not fully resolvable from available sources and must be verified by the document builder directly from FTB official sources:

1. **2025 California tax bracket thresholds by filing status**: The 2025 California Tax Rate Schedules PDF at ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf was not text-extractable. Builder must render and manually transcribe all bracket thresholds for all filing statuses. The 9 rates (1% through 12.3%) are confirmed; only the income thresholds need transcription.
2. **2026 California tax bracket thresholds and exemption amounts**: Published annually by FTB; verify when available.
3. **CA AMT exemptions for 2026**: 2025 confirmed ($92,749/$123,667/$61,830); 2026 figures not yet published.
4. **High-income itemized deduction limitation threshold**: The 6% of excess AGI / 80% cap applies above a specific California AGI threshold; exact 2025 threshold must be confirmed from 2025 Schedule CA instructions.
5. **SB 175 revenue trigger activation**: Whether the Director of Finance has issued a determination eliminating the NOL suspension and credit cap for 2025 and/or 2026 must be confirmed before finalizing 02-ca-nol-rules.md and 04-ca-credits-master.md.
6. **Film Credit (Program 4.0) SB 167 cap status**: Whether the film credit is subject to or exempt from the $5,000,000 annual business credit cap under SB 167 must be confirmed.
7. **2025/2026 senior/blind additional exemption credit amount**: Confirmed at $153 for personal exemption; the additional senior/blind amount should be confirmed from Form 540 directly (separate from personal exemption credit).
8. **CalEITC by number of children full table**: The $3,756 maximum is confirmed for 3+ children; the credit schedule for 0, 1, and 2 children must be pulled from Form FTB 3514 for the full table.

---

## Quality Checklist

Run before finalizing each document:

- R&TC section(s) cited in document header
- Parallel IRC section noted with explicit conformity status (Conforms / Does Not Conform / Partially Conforms)
- Citation line in header references a verifiable source (FTB.ca.gov URL, R&TC statutory text, named practitioner alert)
- All dollar amounts specify 2025 or 2026; amounts from the Corrections Log use corrected figures
- Conformity analysis section uses FEDERAL RULE → CALIFORNIA RULE → Controlling Authority format
- Schedule CA impact stated (Column B addition / Column C subtraction / no adjustment)
- At least one AGENT RULE block per document
- At least one TRAP block per document
- Cross-References section at bottom
- No opinions, no editorializing — law stated as fact
- No padding — every sentence carries information
- California AGI explicitly distinguished from federal AGI wherever phase-outs reference AGI
- Builder-verification items flagged in the document if the figure could not be confirmed
- OBBBA non-conformity noted wherever federal and California treatment diverges due to OBBBA