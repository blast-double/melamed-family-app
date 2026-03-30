# Federal Tax Law Knowledge Base — Agent Build Plan
**Version:** 2.0 | **Date:** March 2026
**Governing Law:** OBBBA (P.L. 119-21, signed July 4, 2025), SECURE 2.0, TCJA as amended
**Inflation Sources:** Rev. Proc. 2024-40 (2025), Rev. Proc. 2025-32 (2026), IRS Notice 2024-80, IRS Notice 2025-67

---

## Your Mission

Build a federal tax law knowledge base as a collection of focused markdown documents. Each document covers one cohesive topic and is designed for retrieval by a tax AI agent via vector store. Documents must be:

- Self-contained: every doc includes its own IRC citations, relevant forms, dollar thresholds, and agent rules
- Dense and factual: no narrative filler, no editorializing, law stated as fact
- 800-2,000 words per document by default: long enough to be comprehensive, short enough to retrieve precisely; documents covering multiple distinct subtopics may use an extended limit (noted per-file below)
- Consistent format: every document follows the template below

Do not combine topics to save space. Do not split a single topic across multiple documents unless the list below explicitly separates them.

---

## Universal Document Template

Every document must follow this exact structure:

```
# [Topic Name]
**IRC Section(s):** Section XXX
**Relevant Forms:** Form XXXX
**Tax Years Covered:** 2025-2026
**Last Updated:** March 2026

---

## Overview
[2-4 sentence factual summary of what this section covers and why it matters]

## Rules
[The actual law, stated as facts. Use numbered lists for sequential rules, bullet lists for
parallel items. Use tables for rates/thresholds. No paragraphs longer than 4 sentences.]

## Key Thresholds and Figures
[Table with all dollar amounts, specifying 2025 vs 2026 column where different]

## OBBBA Changes (if applicable)
**OLD RULE (pre-2025):** [prior law]
**NEW RULE (OBBBA):** [current law]
[Effective date of change]

## Agent Rules
> **AGENT RULE:** [Decision logic the agent must apply. Written as conditional: "If X, then Y."]

## Common Traps
> **TRAP:** [Specific error, penalty, or misapplication to flag]

## Cross-References
- Related doc: [filename]
- Related doc: [filename]
```

---

## File List and Build Specifications

Build every file below. The filename is the exact output filename. The specifications tell you what must be covered in that file.

---

### PART 0 - FOUNDATION

#### 00-gross-income-definition.md
IRC Section 61, Section 451, Reg. Section 1.451-2

Cover:
- The "all income from whatever source derived" standard
- Complete list: wages, salaries, tips, fees, commissions, business income, gains from property sales, rents, royalties, dividends, interest, alimony (pre-2019 agreements only), annuities, discharge of debt income, distributive share of partnership/S-corp income, gambling winnings, prizes, awards, barter income, imputed income, found property
- Supreme Court accession-to-wealth test (Commissioner v. Glenshaw Glass, 348 U.S. 426, 1955): undeniable accession to wealth, clearly realized, over which taxpayer has complete dominion
- Cash equivalency doctrine: property or services received in lieu of cash included at FMV
- Constructive receipt (Reg. Section 1.451-2(a)): income taxable when available without substantial restriction; examples: uncashed checks, credited bank interest, matured bond coupons
- Claim of right doctrine: income received without restriction is taxable in year received even if later repayment required (Section 1341 relief if repayment exceeds $3,000)
- Tax benefit rule (Section 111): recovery of previously deducted amount includable only to extent deduction produced tax benefit
- Assignment of income doctrine (Lucas v. Earl, 281 U.S. 111, 1930): income taxed to person who earns it; cannot be reassigned by contract before earned

AGENT RULE: Section 61 is the starting gate. Before analyzing any deduction, credit, or exclusion, confirm the item is gross income. If it falls under Sections 101-140, it is excluded before the calculation begins.

TRAP: Constructive receipt -- a taxpayer cannot defer income by refusing to cash a check or declining to access a credited account. Availability, not receipt, triggers taxation.

---

#### 00-gross-income-exclusions.md
IRC Sections 101-140

Cover each exclusion with: (a) the rule, (b) any dollar cap, (c) conditions required, (d) relevant form.

- Section 101: Life insurance death benefits excluded; accelerated death benefits for terminally ill (Section 101(g)) excluded; interest on death benefits IS taxable
- Section 102: Gifts and inheritances excluded from recipient; income earned on gifted property IS taxable; donor may have gift tax obligations
- Section 103: State/local bond interest excluded; private activity bond interest is AMT preference item (Form 6251)
- Section 104: Physical injury/sickness damages excluded; punitive damages NOT excluded; emotional distress NOT excluded unless attributable to physical injury; workers' compensation fully excluded
- Sections 105/106: Employer health insurance premiums excluded from employee income; employer HSA contributions excluded up to statutory limits
- Section 108: COD income generally includable; exclusions for bankruptcy, insolvency (to extent of insolvency), qualified farm debt, QRPBI, student loan forgiveness; attribute reduction rules apply
- Section 119: Meals/lodging for convenience of employer on business premises excluded; must be required condition of employment
- Section 121: Primary residence gain exclusion $250,000 (single) / $500,000 (MFJ); ownership test (owned 2 of last 5 years) AND use test (primary residence 2 of last 5 years); 24 months need not be consecutive; partial exclusion for unforeseen circumstances; reduced exclusion for non-qualified use periods
- Section 127: Employer educational assistance up to $5,250/year; undergraduate and graduate level; not limited to job-related
- Section 129: Dependent care assistance up to $5,000/year ($2,500 MFS) through employer plan
- Section 132: Fringe benefits -- no-additional-cost services, employee discounts, working condition, de minimis, qualified transportation ($325/month parking/transit 2025), on-premises athletic facilities, retirement planning services
- Section 135: US savings bond interest excluded if used for qualified higher education; income phase-outs apply
- Section 139: Qualified disaster relief payments excluded

AGENT RULE: When a taxpayer receives something of value, check Section 61 (is it income?), then Sections 101-140 (is it excluded?). Only amounts surviving both checks enter the AGI calculation.

TRAP: Section 121 non-qualified use -- if a taxpayer rents a home before converting to primary residence, the portion of gain attributable to rental period does NOT qualify for exclusion even if use test is otherwise met.

---

#### 00-tax-calculation-waterfall.md
IRC Sections 1, 62, 63, 67, 68

Cover the complete sequential calculation every tax return follows. For each step: what it is, what goes in/out, and which form/schedule it appears on.

THE WATERFALL:
Gross Income (Section 61)
minus Excluded Items (Sections 101-140)
= Total Gross Income (Form 1040, Line 9)
minus Above-the-Line Deductions (Section 62, Schedule 1 Part II)
= Adjusted Gross Income / AGI (Form 1040, Line 11)
minus Greater of: Standard Deduction OR Itemized Deductions (Schedule A)
minus Qualified Business Income Deduction (Section 199A, Form 8995/8995-A)
= Taxable Income (Form 1040, Line 15)
times Applicable Rate (ordinary brackets OR LTCG/QD schedule)
= Tentative Regular Tax
minus Nonrefundable Credits
= Regular Tax Liability
plus AMT if greater than regular tax (Form 6251)
plus Net Investment Income Tax (Section 1411, Form 8960)
plus Additional Medicare Tax (Section 3103, Form 8959)
plus Self-Employment Tax (Section 1401, Schedule SE) [50% deductible above-the-line]
plus Other taxes (household employment, recapture taxes)
minus Refundable Credits (EITC, ACTC, PTC)
minus Withholding (W-2 box 2, 1099 withholding)
minus Estimated Tax Payments (Form 1040-ES)
minus Prior Year Overpayment Applied
= Tax Due / Refund

For above-the-line deductions (Section 62), list all: educator expenses ($300), student loan interest ($2,500), HSA contributions (Section 223), self-employed health insurance (Section 162(l)), SE tax deduction (50%), alimony paid (pre-2019 agreements), IRA contributions, moving expenses (military only post-OBBBA), penalty on early savings withdrawal, new OBBBA deductions (tips up to $25,000; overtime up to $12,500; auto loan interest up to $10,000; senior deduction $6,000 for taxpayers 65+) -- specify phase-outs and 2028 sunset dates for each OBBBA deduction.

AGENT RULE: AGI is the most important single number on a tax return. Dozens of phase-outs, limitations, and credit calculations reference AGI or MAGI. Always establish AGI before evaluating credits or itemized deductions.

TRAP: MAGI is not always the same as AGI. Different provisions use different MAGI definitions. Roth IRA MAGI adds back student loan interest and IRA deductions. ACA PTC MAGI adds back tax-exempt interest and Social Security. Always use the MAGI definition specific to the provision being applied.

---

#### 00-filing-status.md
IRC Sections 1, 2, 7703

Cover all five filing statuses with: (a) qualification rules, (b) 2025 and 2026 standard deduction, (c) bracket thresholds, (d) special rules.

- Single
- Married Filing Jointly (MFJ): includes same-sex marriages following Obergefell
- Married Filing Separately (MFS): consequences include loss of EITC, PTC, student loan interest deduction; 50% cap on dependent care exclusion; both must itemize or both take standard deduction
- Head of Household (HoH): requirements: unmarried (or considered unmarried), paid more than half cost of home, qualifying person lived in home more than half the year; "considered unmarried" rules for separated spouses
- Qualifying Surviving Spouse: two-year window after spouse's death with dependent child; uses MFJ bracket and standard deduction

Include: December 31 determination date, community property states (AZ, CA, ID, LA, NV, NM, TX, WA, WI) and Section 66 MFS treatment, impact on AMT/NIIT/Additional Medicare thresholds.

AGENT RULE: Filing status is determined on December 31. A taxpayer who divorces on December 31 is considered unmarried for the entire year.

TRAP: MFS is almost always more expensive. Run MFJ vs MFS comparison before recommending. Primary exception: income-driven student loan repayment plans, where MFS lowers the calculated payment.

---

#### 00-ordinary-income-brackets.md
IRC Sections 1(a)-(d), Rev. Proc. 2024-40, Rev. Proc. 2025-32

Include full bracket tables for all five filing statuses for both 2025 and 2026. Then cover:

- Marginal vs effective rate: only income within each bracket is taxed at that rate
- OBBBA made TCJA brackets permanent (no 2026 sunset)
- Qualified dividends and LTCG use separate rate schedule (0%/15%/20%): stack on top of ordinary income; applicable LTCG rate determined by where total taxable income falls, not just the capital gain
- Stacking order: ordinary income fills brackets first, then LTCG/QD sit on top
- Parallel tax systems stacking on same income: SE tax (Schedule SE), NIIT (Form 8960), Additional Medicare (Form 8959), AMT (Form 6251)
- Deduction value = deduction amount times marginal rate
- LTCG/QD thresholds for 2025 and 2026 by filing status
- SS wage base: $176,100 (2025) / $184,500 (2026)

AGENT RULE: To calculate the tax benefit of any deduction, multiply the deduction amount by the taxpayer's marginal rate. A $10,000 deduction is worth $2,200 to a 22% bracket taxpayer and $3,700 to a 37% bracket taxpayer.

---

### PART 1 - INCOME RECOGNITION

#### 01-capital-gains-losses.md
IRC Sections 1001, 1(h), 1211, 1212, Schedule D, Form 8949

Cover:
- Realization: gain/loss recognized on sale or exchange (Section 1001)
- Short-term (held 1 year or less): taxed at ordinary income rates
- Long-term (held more than 1 year): 0%/15%/20% -- tables for 2025 and 2026 by filing status
- Special rates: collectibles 28% (Section 1(h)(5)); unrecaptured Section 1250 gain 25%; Section 1202 QSBS exclusion
- Wash sale rule (Section 1091): loss disallowed if substantially identical security purchased within 30 days before or after sale; disallowed loss added to replacement share basis; does NOT apply to gains; crypto currently has no statutory wash sale rule
- Capital loss limitation: $3,000/year of net loss against ordinary income; excess carries forward indefinitely retaining character; no carryback for individuals
- Form 8949: Box A (covered, 1099-B with basis), Box B (covered, no basis), Box C (all others); flows to Schedule D
- Schedule D: nets short-term and long-term; applies rate schedule

AGENT RULE: Always determine holding period first. One day difference (held exactly 1 year vs 1 year + 1 day) can change the tax rate from 37% to 20% on large gains.

TRAP: Wash sales apply across all accounts the taxpayer controls including IRAs. Selling a stock at a loss in a taxable account and repurchasing in an IRA within the 61-day window triggers wash sale; the loss is permanently lost, not added to IRA basis.

---

#### 01-property-sales-recapture.md
IRC Sections 1231, 1245, 1250, 64, 65

Cover:
- Section 1231 property: real and depreciable property used in a trade or business held more than 1 year; net Section 1231 gains taxed at LTCG rates; net losses treated as ordinary losses; 5-year lookback rule -- ordinary loss recapture if taxpayer had net Section 1231 losses in prior 5 years
- Section 1245 recapture: personal property (equipment, vehicles, Section 179 property, intangibles); ALL depreciation previously claimed recaptured as ordinary income upon sale; applies only to extent of gain
- Section 1250 recapture: real property; recaptures only additional depreciation beyond straight-line as ordinary income (rarely triggered under MACRS); unrecaptured Section 1250 gain (straight-line depreciation on real property) taxed at maximum 25%
- Priority: Section 1245 recapture first; remaining gain is Section 1231 at LTCG rates
- Walkthrough example: sale of rental property -- trace Section 1245 (none for MACRS real property), unrecaptured Section 1250 at 25%, Section 1231 gain at LTCG rate

AGENT RULE: Every sale of a depreciable business asset must be analyzed in order: (1) How much depreciation was previously claimed? (2) Section 1245 or Section 1250 recapture on that amount? (3) Remaining gain is Section 1231. Never report a business property sale as a simple capital gain without checking for recapture.

TRAP: Cost segregation accelerates depreciation into personal property categories, increasing Section 1245 recapture exposure upon sale. Model recapture before advising a sale.

---

#### 01-basis-rules.md
IRC Sections 1011, 1012, 1014, 1015, 1016

Cover:
- Cost basis (Section 1012): purchase price plus acquisition costs
- Adjusted basis (Section 1016): cost basis plus improvements minus depreciation, Section 179, casualty losses
- Gifted property (Section 1015): carryover basis for gain purposes; if FMV < donor's basis at gift, loss basis is FMV; no gain or loss if sale price falls between the two
- Inherited property (Section 1014): stepped-up to FMV at date of death; eliminates built-in gain or loss; does NOT apply to IRD (IRA balances, deferred compensation, installment obligations)
- Community property step-up: both halves receive step-up at death of either spouse (Section 1014(b)(6))
- ESPP/ISO stock: compensation income recognized at purchase/exercise affects basis; disqualifying vs qualifying dispositions
- Mutual fund basis methods: FIFO (default), specific identification, average cost (mutual funds only)
- Crypto basis: specific identification permitted with adequate records; FIFO is default

AGENT RULE: You cannot calculate gain or loss without knowing adjusted basis. Always ask: What did the taxpayer pay? What adjustments have occurred? Was it gifted or inherited?

TRAP: Step-up in basis does NOT apply to retirement accounts. IRAs and 401(k)s are IRD -- the full value is taxable as ordinary income to the beneficiary when distributed.

---

#### 01-cancellation-of-debt.md
IRC Section 108, Form 982, Form 1099-C

Cover:
- General rule: COD income includable in gross income (Section 61(a)(12))
- Exclusions (Section 108): (1) bankruptcy discharge -- Title 11; (2) insolvency -- excluded to extent insolvent immediately before discharge; (3) qualified farm indebtedness; (4) QRPBI; (5) student loan forgiveness under qualifying programs
- Attribute reduction (Section 108(b)): when excluded, reduce in order: NOLs, general business credits (33 cents per dollar), passive activity losses, capital loss carryforwards, basis of property, foreign tax credit carryovers
- Form 982: reduction of tax attributes; filed with return in year of discharge
- Nonrecourse debt foreclosure: no COD income -- difference between debt and FMV is Section 1001 gain
- Recourse debt foreclosure: two events -- (1) Section 1001 gain/loss (FMV vs adjusted basis); (2) COD income (debt in excess of FMV)

AGENT RULE: When debt is cancelled: (1) Is an exclusion available? (2) If yes, what attributes must be reduced and in what order? (3) Is Form 982 required?

---

#### 01-cryptocurrency-digital-assets.md
IRC Sections 61, 1001, Notice 2014-21, Rev. Rul. 2023-14, Form 1099-DA, Form 8949

Cover:
- Property treatment: virtual currency is property for federal tax purposes (Notice 2014-21)
- Taxable events: sale for fiat; exchange of one crypto for another; use to purchase goods/services; mining/staking rewards; airdrops; hard forks; DeFi swaps
- Non-taxable events: buying crypto with fiat; transferring between own wallets; holding
- Mining and staking income: ordinary income at FMV on date of receipt (Rev. Rul. 2023-14); basis equals income recognized
- Basis tracking: FIFO default; specific identification permitted with adequate records; cannot use average cost
- Form 1099-DA: effective 2025 tax year; custodial brokers must report; non-custodial/DeFi self-reported; Form 8949 still required for each transaction
- Form 1040 digital asset checkbox: must answer even if no 1099 received
- No statutory wash sale rule currently applies to crypto
- OBBBA: $300 de minimis exclusion for personal use transactions -- confirm specific provision details

AGENT RULE: Every crypto trade is a taxable event. If the taxpayer cannot produce cost basis records, use FIFO as default and document the limitation.

---

#### 01-social-security-taxation.md
IRC Section 86

Cover:
- Up to 85% of Social Security benefits are taxable as ordinary income
- Combined income formula: AGI + tax-exempt interest + 50% of Social Security benefits
- Thresholds: 0% taxable -- combined income less than $25,000 (single) / $32,000 (MFJ); up to 50% taxable -- $25,000-$34,000 (single) / $32,000-$44,000 (MFJ); up to 85% taxable -- above $34,000 (single) / $44,000 (MFJ)
- Thresholds NOT inflation-adjusted since 1984
- Tax-exempt interest (municipal bonds) counts in combined income formula
- MFS taxpayers who lived with spouse at any point during year: 85% is taxable

AGENT RULE: Social Security taxation uses combined income, not AGI. Tax-exempt interest must be added back. Advising SS recipients to hold municipal bonds provides no benefit for this calculation.

---

### PART 2 - BUSINESS DEDUCTIONS AND CREDITS

#### 02-qbi-deduction-199a.md
IRC Section 199A, Reg. Sections 1.199A-1 through 1.199A-6, Form 8995, Form 8995-A

Cover:
- 20% deduction of QBI for pass-through entities; OBBBA made permanent; added $400 minimum deduction; widened phase-in range
- QBI definition: net income/gain/deduction/loss from qualified US trade or business; excludes investment income, reasonable compensation, guaranteed payments
- W-2/UBIA limitation above phase-out: greater of (a) 50% of W-2 wages or (b) 25% of W-2 wages + 2.5% of unadjusted basis of qualified property
- Specified service trade or business (SSTB): health, law, accounting, actuarial science, performing arts, consulting, athletics, financial services, brokerage -- completely phased out above income thresholds; provide 2025 and 2026 phase-out ranges by filing status
- Overall limitation: 20% of taxable income net of LTCG and qualified dividends
- Aggregation election (Reg. Section 1.199A-4): combining businesses to meet W-2 wage test
- Real estate safe harbor (Rev. Proc. 2019-38): 250 hours of rental services per year; self-rentals and triple-net leases generally excluded
- Negative QBI: carries forward to next year

AGENT RULE: For S-corp and partnership owners -- (1) confirm not SSTB above threshold; (2) calculate QBI net of all adjustments; (3) apply W-2/UBIA limitation if above phase-out; (4) apply overall 20% of taxable income cap.

---

#### 02-rd-expenditures-174a-41.md
IRC Sections 174A (OBBBA), 174 (prior law), 41, Form 6765

Section 174 history:
- Pre-TCJA: immediate expensing of all R&E
- TCJA 2017: required 5-year amortization (domestic) / 15-year (foreign) for amounts paid after December 31, 2021
- OBBBA: restored immediate expensing for domestic R&E via new Section 174A; effective for tax years beginning after December 31, 2024; foreign R&E still amortized 15 years; transition: taxpayers with deferred amortization from 2022-2024 may elect catch-up

Section 41 R&D Credit:
- Regular credit: 20% of QREs above base amount
- Alternative Simplified Credit (ASC): 14% of QREs above 50% of prior 3-year average; 6% if no QREs in prior 3 years
- Four-part test: technological in nature, permitted purpose, elimination of uncertainty, process of experimentation
- QREs: wages, supplies used in research, contract research (65% of amounts paid)
- Startup payroll offset: less than $5M gross receipts AND 5 years or fewer in existence; applied against FICA on Form 6765
- Interaction: Section 280C election takes reduced credit to avoid reducing Section 174A deduction

---

#### 02-depreciation-179-bonus.md
IRC Sections 167, 168, 168(k), 179, 280F

Cover:
- MACRS property classes, half-year convention, mid-quarter convention trigger (more than 40% of depreciable property placed in service in Q4), ADS requirements
- Section 179 expensing: OBBBA doubled to $2,500,000 (2025); phase-out at $4,000,000; cannot exceed taxable income from active business; provide 2026 inflation-adjusted amount
- Bonus depreciation (Section 168(k)): OBBBA restored 100% permanently for property placed in service after January 19, 2025; new and used property; 5/7/15-year MACRS and QIP; does NOT apply to 27.5-year or 39-year property
- Luxury auto limits (Section 280F): 2025 Year 1 $12,400 ($20,400 with bonus), Year 2 $19,800, Year 3 $11,900, Year 4+ $7,160; include 2026 figures
- Heavy SUV cap: Section 179 limited to $31,300 (2025) for vehicles over 6,000 lbs GVWR; inflation-adjusted annually
- Listed property: more than 50% business use required for MACRS/bonus; recapture if drops to 50% or below
- Standard mileage rate: cannot switch from actual to standard after first year; include 2025 rate
- Qualified Improvement Property (QIP): 15-year MACRS, eligible for 100% bonus

---

#### 02-startup-costs-195-248.md
IRC Sections 195, 248, 709

Cover:
- Startup costs (Section 195): costs incurred before business begins that would be deductible if incurred after; examples: market research, pre-opening advertising, employee training, professional fees
- First-year deduction: $5,000 reduced dollar-for-dollar when total startup costs exceed $50,000
- Amortization: remainder over 180 months beginning with month business begins
- Organizational costs (Section 248 corps / Section 709 partnerships): same structure -- $5,000 first-year / 180-month amortization; costs of forming the entity
- Non-qualifying costs: stock issuance costs, asset acquisition costs -- capitalized separately
- Election: made by deducting on first return; no separate statement required
- Abandoned start-up: costs deductible as loss in year taxpayer abandons the effort

---

#### 02-home-office-280a.md
IRC Section 280A, Rev. Proc. 2013-13

Cover:
- Qualification: regular and exclusive use as (a) principal place of business, (b) place to meet clients in normal course, or (c) separate structure used in business
- Principal place of business: qualifies if used for administrative/management activities and no other fixed location is available for these
- Regular method: actual home expenses times (office sq ft / total sq ft); includes mortgage interest/rent, utilities, insurance, repairs, depreciation; depreciation recaptured at 25% upon home sale
- Simplified method: $5/sq ft up to 300 sq ft = maximum $1,500; no depreciation; no recapture on sale
- Gross income limitation: deduction cannot exceed gross income from business use; carryforward of disallowed amounts
- S-corp shareholders: cannot deduct directly; must use accountable plan reimbursement or arm's-length rental with corporation
- Employees: no deduction post-TCJA; exceptions for reservists, performing artists, fee-basis government officials

---

#### 02-se-tax-health-insurance.md
IRC Sections 1401, 1402, 162(l), Schedule SE, Form 7206

Cover:
- SE tax rates: 15.3% on first $176,100 (2025) / $184,500 (2026) of net SE income; 2.9% Medicare on all SE income above SS wage base; 0.9% Additional Medicare on SE income above $200,000 (single) / $250,000 (MFJ) -- thresholds NOT indexed
- Net SE income = 92.35% of Schedule C / K-1 SE income
- Above-the-line deduction: 50% of SE tax (Section 164(f))
- Section 162(l) self-employed health insurance: 100% of premiums for health, dental, vision, qualifying LTC insurance; cannot exceed net profit from business; cannot deduct if eligible for employer-subsidized plan during the month; calculated on Form 7206
- Long-term care limits: age-based; provide 2025 and 2026 limits by age bracket
- S-corp shareholders (more than 2%): premiums must be included in W-2 Box 1 (not Boxes 3/5); then deducted above-the-line on Form 7206

---

#### 02-meals-entertainment-274.md
IRC Section 274

Cover:
- Entertainment: 100% nondeductible post-TCJA (permanent under OBBBA); applies to tickets, golf, hunting, vacation packages regardless of business discussion
- Business meals: 50% deductible; bona fide business purpose required; taxpayer or employee must be present; not lavish or extravagant; required substantiation: amount, time/place, business purpose, business relationship
- Employer on-premises meals (Section 119): OBBBA eliminated employer deduction starting 2026; employee income exclusion preserved for 2025
- DOT workers: 80% deductible
- Adequate records: contemporaneous; five required elements

---

#### 02-hobby-loss-at-risk.md
IRC Sections 183, 465

Section 183 Hobby Loss:
- For-profit presumption: profit in 3 of 5 consecutive years (2 of 7 for horses)
- Nine-factor test (Reg. Section 1.183-2(b)): businesslike manner, expertise, time/effort, asset appreciation, success in similar activities, income/loss history, profit amounts, financial status, personal pleasure
- Post-TCJA/OBBBA: hobby income fully taxable as ordinary income; hobby expenses completely nondeductible

Section 465 At-Risk:
- Applied BEFORE Section 469 passive activity rules
- Losses limited to amounts at risk: cash contributed + adjusted basis of contributed property + recourse debt + qualified nonrecourse real estate financing
- Does NOT include nonrecourse debt (other than qualified real estate), stop-loss protections, amounts not economically at risk
- Disallowed losses suspended and carried forward; released when at-risk amount increases

---

#### 02-nol-excess-business-loss.md
IRC Sections 172, 461(l)

Cover:
- Post-TCJA/OBBBA NOL rules: indefinite carryforward; no carryback (exception: farming -- 2-year carryback); 80% of taxable income limitation per year
- NOL computation: combine all income and loss; capital losses in excess of capital gains excluded from NOL
- CARES Act 5-year carryback for 2018-2020 NOLs: expired; not applicable to current years
- Section 461(l) Excess Business Loss Limitation: OBBBA made permanent; non-corporate taxpayers cannot deduct business losses exceeding $313,000 (single) / $626,000 (MFJ) for 2025 (inflation-adjusted annually); excess becomes NOL carryforward; applied after Section 469; include 2026 figures

TRAP: Section 461(l) is applied AFTER Section 469. A loss surviving passive activity limitation is still subject to the excess business loss cap. The excess converts to an NOL carryforward, then subject to the 80% limitation -- a three-layer limitation stack.

---

### PART 3 - PASSIVE ACTIVITIES AND REAL ESTATE

#### 03-passive-activity-rules-469.md
IRC Section 469, Reg. Sections 1.469-1 through 1.469-11

Cover:
- Two categories: (1) trade or business without material participation; (2) rental activity with exceptions
- Seven material participation tests (Reg. Section 1.469-5T) -- taxpayer must meet ONE:
  1. More than 500 hours during year
  2. Substantially all participation in the activity
  3. More than 100 hours and not less than anyone else
  4. Significant participation activities aggregate more than 500 hours
  5. Material participation in 5 of last 10 years
  6. Material participation in any 3 prior years (personal service)
  7. Facts and circumstances -- regular, continuous, substantial; fewer than 100 hours does not qualify
- Passive loss limitation: losses offset only passive income; excess suspended and carried forward
- Suspended loss release: all suspended losses released upon complete taxable disposition
- Rental presumption: passive regardless of participation; exception for real estate professionals (Section 469(c)(7)) -- more than 750 hours in real property trades/businesses with material participation, more than in other activities
- $25,000 rental loss allowance: with active participation; phases out $0.50 per dollar of AGI above $100,000; eliminated at $150,000
- Grouping elections (Reg. Section 1.469-4): related activities treated as single activity; difficult to unwind
- Self-charged interest: interest from lending to passive activity treated as passive income

---

#### 03-real-estate-cost-seg-1031.md
IRC Sections 168, 1031, Rev. Proc. 2011-14

Cost Segregation:
- Engineering study reclassifies building components: 5/7/15-year personal property vs 27.5/39-year real property
- Common reclassifications: electrical systems serving equipment (5-year), carpeting (5-year), land improvements -- parking lots, fencing, landscaping (15-year)
- Interaction: reclassified property eligible for 100% bonus depreciation under OBBBA
- Look-back study (Rev. Proc. 2011-14): catch-up depreciation in current year without amended returns; automatic consent
- Recapture risk: Section 1245 recapture on all personal property components upon sale

Section 1031 Like-Kind Exchange:
- Defers gain on exchange of real property held for productive use or investment for like-kind real property held for same purpose
- Like-kind: any US real property for any other US real property; personal property excluded post-TCJA
- Timeline: identify replacement property within 45 days of closing; close within 180 days
- Boot: cash or non-like-kind property triggers gain recognition to extent of boot; mortgage relief is boot
- Basis: carryover basis from relinquished property preserves deferred gain
- Related party rule: both parties must hold property 2 years
- Reverse exchanges: Exchange Accommodation Titleholder (EAT) parking arrangement; 180-day maximum

---

#### 03-installment-sales-453.md
IRC Sections 453, 453A, Form 6252

Cover:
- Default method when at least one payment received after year of sale
- Gross profit ratio: Gross Profit divided by Contract Price; each payment times ratio equals gain recognized
- Gross profit = selling price minus adjusted basis; Contract price = selling price minus qualifying indebtedness assumed (excess over basis added back to contract price)
- Exclusions from installment method: dealer property, publicly traded securities, recaptured depreciation (recognized in full in year of sale)
- Section 453A interest: obligations with face value more than $5 million outstanding at year end; interest charged on deferred tax at applicable federal rate
- Election out: recognize all gain in year of sale; irrevocable; beneficial when losses available or future brackets expected to rise
- Contingent payment sales: special rules when total selling price not fixed

---

### PART 4 - TAX CREDITS

#### 04-tax-credits-master.md
**Word limit: 2,500-3,500** (covers 8+ distinct credits with phase-outs, amounts, and OBBBA changes)

IRC Sections 21, 24, 25A, 25B, 32, 36B, 38, 41, Form 3800

Cover each credit: amount, refundable vs nonrefundable, phase-out thresholds, form, OBBBA changes.

Child Tax Credit (Section 24): $2,200 per qualifying child under 17 (OBBBA); ACTC partially refundable; phase-out at $400,000 (MFJ) / $200,000 (others); 2025 and 2026 figures

Child and Dependent Care (Section 21): up to $3,000 (one dependent) / $6,000 (two+) times 20%-35% AGI-based percentage; nonrefundable; reduced by employer-provided dependent care exclusion

American Opportunity Tax Credit (Section 25A): 100% of first $2,000 + 25% of next $2,000 = max $2,500; 40% refundable; first 4 years only; phase-out $80,000-$90,000 (single) / $160,000-$180,000 (MFJ)

Lifetime Learning Credit (Section 25A): 20% of up to $10,000 = max $2,000; nonrefundable; no year limit; same income phase-outs as AOTC

Saver's Credit (Section 25B): 10%/20%/50% of retirement contributions up to $2,000 ($4,000 MFJ); nonrefundable currently; OBBBA converts to matching contribution deposited to retirement account starting 2027

Premium Tax Credit (Section 36B): refundable; reconciled on Form 8962 against advance payments; OBBBA confirmed no income cap

Earned Income Tax Credit (Section 32): refundable; income limits and maximum credit by qualifying children for 2025 and 2026; investment income limit $11,600 (2025)

General Business Credit (Section 38, Form 3800): umbrella combining R&D (Section 41), WOTC (Section 51), disabled access (Section 44), others; limited to tax liability less tentative minimum tax; 1-year carryback, 20-year carryforward

Energy credit OBBBA rollbacks: Section 30D EV credit terminated after September 30, 2025; Section 25C, Section 25D expired December 31, 2025; Section 48D semiconductor credit increased to 35%; commercial wind/solar safe harbor if construction began before June 2026

---

### PART 5 - RETIREMENT

#### 05-retirement-contributions.md
IRC Sections 401, 402, 408, 408A, 415, 219, IRS Notice 2024-80, IRS Notice 2025-67

Full table of all 2025 and 2026 contribution limits. Cover:

- 401(k)/403(b)/457(b): employee deferral; employer match separate from deferral; total Section 415 limit; catch-up 50+; SECURE 2.0 super catch-up 60-63 ($11,250 both years)
- Traditional IRA: deductibility phase-outs for active participants -- 2025: $79,000-$89,000 single; $126,000-$146,000 MFJ active participant; non-active spouse phase-out; nondeductible contributions tracked on Form 8606
- Roth IRA: income phase-out -- 2025: $150,000-$165,000 single; $236,000-$246,000 MFJ; no RMDs during owner's lifetime; cannot deduct contributions
- SEP-IRA: 25% of compensation up to $70,000 (2025) / $72,000 (2026); employer-only contributions
- SIMPLE IRA: $16,500 (2025) / $17,000 (2026); employer match required (2% nonelective or 3% match)
- Backdoor Roth: nondeductible traditional IRA then convert to Roth; pro-rata rule (Section 408(d)(2)) applies proportionally across all pre-tax IRA balances; Form 8606 tracks basis
- Mega backdoor Roth: after-tax 401(k) to in-plan Roth conversion or Roth IRA rollover; plan must permit

---

#### 05-retirement-distributions.md
IRC Sections 72, 401(a)(9), 4974, SECURE 2.0

Cover:
- 10% early withdrawal penalty (Section 72(t)): before age 59 1/2; all exceptions: death, disability, SEPP, age 55 separation from service, medical expenses more than 7.5% AGI, health insurance during unemployment, qualified reservist, first-time homebuyer $10,000 lifetime, higher education, IRS levy, QDRO, birth/adoption up to $5,000
- SEPP/Section 72(t): at least 5 years or until age 59 1/2 whichever is later; three methods: RMD method, fixed amortization, fixed annuitization; modification triggers 10% penalty plus interest on all prior distributions
- RMDs (Section 401(a)(9)): SECURE 2.0 raised starting age to 73 (born 1951-1959) and 75 (born 1960+); RMD = prior year-end balance divided by IRS Uniform Lifetime Table factor; first RMD may delay to April 1 following year (creates double-up in year two); penalty 25% of shortfall (reduced to 10% if corrected within 2 years)
- Inherited IRA post-SECURE: 10-year rule for most non-spouse beneficiaries; eligible designated beneficiaries (surviving spouse, minor children, disabled/chronically ill, not more than 10 years younger) may use stretch; annual RMDs required within 10-year window if decedent was already taking RMDs per 2024 final regulations
- Roth conversions: taxed as ordinary income in year of conversion; no 10% penalty if direct conversion; separate 5-year clock per conversion for penalty purposes on earnings

---

### PART 6 - ENTITIES AND PAYROLL

#### 06-entity-comparison.md
IRC Sections 1, 11, 301, 1361, 701, Reg. Sections 301.7701-1 through -3

Full comparison table: Sole Proprietor, SMLLC, Multi-Member LLC, S-Corp, C-Corp, Partnership. For each: tax treatment, SE tax exposure, QBI eligibility, owner compensation treatment, capital raise flexibility, liability protection, formation/maintenance costs.

Cover:
- Check-the-box elections (Form 8832): default classifications; election options; effective date up to 75 days retroactive / 12 months prospective
- C-corp: 21% flat rate; double taxation on dividends; accumulated earnings tax (Section 531) at 20% beyond reasonable business needs; Section 1202 QSBS eligibility; fiscal year flexibility
- S-corp: pass-through taxation; 100 shareholder limit; one class of stock; reasonable compensation requirement; built-in gains tax (Section 1374) -- 21% on appreciated assets sold within 5-year recognition period after C-to-S conversion; PTTP rules
- Partnership: special allocations if substantial economic effect; Section 754 election for inside/outside basis adjustment; hot asset rules (Section 751)

---

#### 06-scorp-payroll-compliance.md
IRC Sections 3101, 3111, 3121, 3301, 6302, 6672, Forms 941/940/W-2/W-3/7203

Cover:
- Reasonable compensation requirement: more than 2% shareholders performing services must receive W-2 wages comparable to third-party rate (Watson v. US, 668 F.3d 1008, 8th Cir. 2012); IRS actively challenges underpayment
- Form 941: quarterly payroll tax return; due dates April 30, July 31, October 31, January 31
- Form 940: annual FUTA; 6% on first $7,000 of wages; credit up to 5.4% for state unemployment taxes = net 0.6% federal
- Deposit schedules: monthly (prior-year liability less than $50,000); semi-weekly ($50,000 or more); $100,000 next-day rule
- W-2: January 31 deadline; e-file required for 10 or more forms
- Form 7203: shareholder stock and debt basis; required for shareholders claiming losses, receiving distributions, or disposing of stock; basis limits loss deductions
- Trust Fund Recovery Penalty (Section 6672): 100% penalty personally assessed against responsible persons who willfully fail to remit withheld payroll taxes; applies to any person with authority to determine which creditors are paid

---

### PART 7 - ESTATE, GIFT, AND TRUSTS

#### 07-estate-gift-tax.md
IRC Sections 2001-2210, 2501-2524, 2601-2664, Forms 706/709

Cover:
- Unified transfer tax: estate and gift tax share one exemption; OBBBA permanently raised to $15,000,000 per individual ($30,000,000 MFJ); indexed for inflation after 2026; prior law would have reduced to approximately $7,000,000 in 2026
- Top rate: 40% on taxable transfers above exemption
- Annual gift exclusion: $19,000 per recipient (2025-2026); gift splitting (Section 2513) doubles to $38,000 per recipient
- Form 709: required when gifts exceed annual exclusion; due April 15; no tax due until cumulative taxable gifts exceed unified credit
- Portability (Section 2010(c)(4)): DSUE transferable to surviving spouse; must elect on timely filed Form 706; Rev. Proc. 2022-32 provides 5-year automatic extension for late elections
- GST tax (Section 2601): separate 40% tax on transfers to skip persons; GST exemption equals unified exemption ($15,000,000)
- Special use valuation (Section 2032A): farm/business real property at use value; reduces estate by up to $1,390,000 (2025); 10-year recapture if sold or converted
- Section 6166: estate tax on closely held business paid over up to 14 years; 2% interest on first $1,570,000 (2025)
- Marital deduction (Section 2056): unlimited for transfers to US citizen spouse; QTIP trusts qualify if all income paid to spouse annually
- Charitable deduction (Section 2055): unlimited

---

#### 07-trust-fiduciary-tax.md
IRC Sections 641-679, 1(e), Forms 1041/K-1

Cover:
- Trust tax rates: 37% bracket at $15,650 (2025) / $16,100 (2026) -- dramatically compressed vs individual brackets
- Simple trust (Section 651): must distribute all income currently; deduction for distributions; no charitable deduction
- Complex trust (Section 661): may accumulate income, make corpus distributions, make charitable contributions; deduction capped at DNI
- DNI (Section 643): cap on distribution deduction and measure of character passing through to beneficiaries
- Grantor trust rules (Sections 671-679): grantor taxed as owner; revocable trusts and IDGTs; income reported on grantor's return
- Form 1041: due April 15; 5.5-month extension available (September 30 deadline); Schedule K-1 to beneficiaries for income, deductions, credits
- NIIT: trusts subject to 3.8% at $15,650 threshold (2025) -- strong incentive to distribute to lower-bracket beneficiaries
- Section 645 election: treat qualified revocable trust as part of decedent's estate; allows fiscal year use
- Charitable remainder trusts (Section 664): income to non-charitable beneficiary, remainder to charity; income ordering: ordinary income then capital gains then other income then corpus
- QSSTs and ESBTs: trust structures eligible to hold S-corp stock

---

### PART 8 - INTERNATIONAL

#### 08-international-fbar-fatca.md
**Word limit: 2,000-3,000** (covers 5 distinct international topics plus OBBBA changes)

IRC Sections 911, 901, 6038D, 31 USC Section 5314, FinCEN 114, Forms 8938/2555/1116/5471/8621

FBAR (FinCEN 114):
- Required: aggregate foreign account value more than $10,000 at any point during calendar year
- Due: April 15; automatic extension to October 15; filed through BSA E-Filing System (not with 1040)
- Penalties: non-willful up to $16,000/year; willful -- greater of $165,353 or 50% of account balance per violation; criminal penalties possible

FATCA (Form 8938):
- Filed with Form 1040; thresholds by residency and filing status: US resident single $50,000 year-end / $75,000 at any point; MFJ $100,000 / $150,000; foreign resident single $200,000 / $300,000; MFJ $400,000 / $600,000
- Penalty: $10,000 failure to disclose; up to $60,000 additional after IRS notice; 40% underpayment penalty on undisclosed assets

Foreign Earned Income Exclusion (Section 911, Form 2555):
- $130,000 (2025) / $132,900 (2026)
- Must meet bona fide residence test OR physical presence test (330 full days in 12-month period)
- Foreign housing exclusion/deduction available in addition

Foreign Tax Credit (Section 901, Form 1116):
- Dollar-for-dollar credit; cannot exceed US tax on same income; income baskets; 1-year carryback, 10-year carryforward

PFIC (Sections 1291-1298, Form 8621):
- Foreign corporation: 75%+ passive income OR 50%+ passive assets; most foreign mutual funds qualify
- Default excess distribution method: punitive -- taxed at highest rate plus interest charges; mark-to-market election or QEF election available
- Annual Form 8621 reporting required for every PFIC holding

OBBBA International Changes:
- GILTI renamed NCTI; Section 250 deduction reduced to 40% (effective rate approximately 12.6%)
- FDII renamed FDDEI
- BEAT rate: 10.5%
- 1% excise tax on outbound remittance transfers effective January 1, 2026

---

### PART 9 - OBBBA MASTER REFERENCE

#### 09-obbba-complete-changes.md
**Word limit: 3,000-4,000** (master reference covering 30+ provisions across permanent, temporary, and repealed categories)

P.L. 119-21, signed July 4, 2025

Organize by: Permanent Changes | Temporary Changes with sunset dates | Repealed/Terminated Provisions.

Cover every item below with old rule, new rule, and effective date.

PERMANENT:
- TCJA income tax brackets made permanent (no 2026 sunset)
- Standard deduction increased and permanent -- include 2025 and 2026 amounts for all filing statuses
- Personal exemption permanently eliminated
- Child Tax Credit $2,200 plus inflation indexing (permanent)
- Section 199A QBI deduction permanent plus $400 minimum deduction
- 100% bonus depreciation (permanent, retroactive to January 19, 2025)
- Section 179 doubled to $2,500,000 (permanent)
- Section 163(j) EBITDA calculation restored (permanent)
- Section 174A domestic R&E immediate expensing (permanent)
- Estate/gift exemption $15,000,000 permanent
- Section 461(l) excess business loss limitation permanent
- AMT exemptions preserved; phase-out rate doubled to 50%
- Mortgage interest cap at $750,000 permanent
- 60% AGI charitable contribution limit permanent
- Section 1202 QSBS cap raised to $15,000,000; graduated holding period
- QOZ program made permanent with rural provisions
- Moving expense deduction permanently repealed (military exception retained)
- Section 48D semiconductor credit increased to 35%

TEMPORARY (sunset noted):
- SALT cap raised to $40,000 for 2025-2029; increases 1% annually; reverts to $10,000 in 2030; phase-down reduces cap by $0.30 per dollar of MAGI above $500,000
- Tip income deduction up to $25,000 above-the-line (expires 2028)
- Overtime premium pay deduction up to $12,500 above-the-line (expires 2028)
- Auto loan interest deduction up to $10,000 on US-assembled vehicles (expires 2028)
- Senior deduction $6,000 for taxpayers 65+ (expires 2028)

NEW PROGRAMS:
- Trump Accounts (Section 530A): $5,000/year contribution limit; $1,000 government seed for births in 2025-2028; contributions begin July 4, 2026
- Non-itemizer charitable deduction reinstated: $1,000 (single) / $2,000 (MFJ)
- 1% remittance excise tax effective January 1, 2026
- Tiered endowment excise tax up to 8% for universities with large per-student endowments

REPEALED/TERMINATED:
- Section 30D new EV credit: terminated for vehicles acquired after September 30, 2025
- Section 25E used EV credit: same termination date
- Section 25C home efficiency credits: expired December 31, 2025
- Section 25D solar/residential energy credits: expired December 31, 2025

OTHER NOTABLE:
- Dependent Care FSA raised to $7,500
- Adoption credit: up to $5,000 refundable portion
- Charitable deduction: 0.5% AGI floor for itemizers; benefit capped at 35% rate for 37% bracket taxpayers
- Saver's Credit converts to matching contribution deposited to retirement account starting 2027
- 1099-K threshold: $20,000 and 200 or more transactions

---

### PART 10 - ADVANCED AND PROCEDURES

#### 10-amt.md
IRC Sections 55-59, Form 6251

Cover:
- Parallel tax system; taxpayer pays higher of regular tax or AMT
- AMT calculation: start with taxable income; add back adjustments and preference items; subtract exemption; multiply by 26%/28%
- Key add-backs: standard deduction, personal exemptions, SALT, miscellaneous itemized deductions, excess percentage depletion, ISO spread at exercise, accelerated depreciation difference (GDS vs ADS)
- 26% rate: on AMTI up to $232,600 (2025); 28% above that amount; include 2026 thresholds
- Exemptions (2025): $88,100 (single); $137,000 (MFJ); phase-out begins at $626,350 (single); OBBBA doubled phase-out rate to 50% (previously 25%); include 2026 figures
- AMT credit (Section 53): for AMT paid due to timing items (not exclusion items); carries forward indefinitely; offsets future regular tax when it exceeds AMT
- Common triggers: large capital gains, ISO exercise, high state income taxes, accelerated depreciation

---

#### 10-niit-additional-medicare.md
IRC Sections 1411, 3103, Forms 8960/8959

Cover:
- NIIT (Section 1411): 3.8% on lesser of (a) net investment income or (b) MAGI above threshold; thresholds $200,000 (single/HoH), $250,000 (MFJ), $125,000 (MFS) -- NOT inflation-adjusted since 2013
- Net investment income: interest, dividends, capital gains, passive activity income, rents, royalties, annuities; excludes active trade/business income, wages, SE income, retirement account distributions, excluded Section 121 gain
- Additional Medicare Tax (Section 3103): 0.9% on wages and SE income above same thresholds; employer does not match; withheld on W-2 wages exceeding $200,000 regardless of filing status; reconciled on Form 8959
- Stacking: NIIT and Additional Medicare are separate parallel taxes; a taxpayer with high investment income AND high wages can owe both
- Estimated payments: both taxes require estimated payments if withholding is insufficient to avoid Section 6654 penalty

---

#### 10-penalties-interest.md
IRC Sections 6601, 6621, 6651, 6654, 6662, 6663, 6672, 6694

Cover each penalty with rate, base, maximum, and exceptions:
- Failure to file (Section 6651(a)(1)): 5% per month of unpaid tax; max 25%; reduced when FTP also applies concurrently
- Failure to pay (Section 6651(a)(2)): 0.5% per month; max 25%; reduced to 0.25% during active installment agreement
- Combined maximum note: when both apply, FTF rate reduced by FTP rate; combined max is 47.5%
- Failure to pay estimated taxes (Section 6654): applies when withholding plus estimates is less than 90% of current year OR 100% of prior year tax (110% if prior year AGI more than $150,000); four safe harbors
- Accuracy-related (Section 6662): 20% of underpayment from negligence, disregard, or substantial understatement (more than $5,000 or 10% of correct tax); 40% for gross valuation misstatements
- Fraud (Section 6663): 75% of underpayment; civil standard; intent to evade required; tolls statute of limitations
- Economic substance (Section 6662(b)(6)): 20% if disclosed, 40% if not; NO reasonable cause defense
- IRS interest: federal short-term rate plus 3%; compounds daily; not deductible for individuals
- Reasonable cause exception: good faith reliance on qualified written professional advice; does NOT apply to economic substance penalties
- Section 6694 preparer penalties: unreasonable positions (substantial authority standard); willful/reckless conduct

---

#### 10-irs-procedures-audit.md
IRC Sections 6501, 6502, 6503, 7421-7430

Cover:
- General SOL (Section 6501(a)): 3 years from later of return due date or filing date
- 6-year SOL (Section 6501(e)): substantial omission of income (more than 25% of gross income stated)
- Unlimited SOL: no return filed; fraudulent return; undisclosed foreign financial assets; FBAR violations
- Audit types: correspondence, office, field; IDR (Information Document Request) process
- Notice of Deficiency (90-day letter): 90 days to petition Tax Court (150 outside US); filing petition stops collection
- CP2000 automated underreporter: IRS computer match of 1099s/W-2s to return; not an audit; respond within 60 days
- Collections: installment agreements; offer in compromise (Section 7122) -- three grounds: doubt as to collectibility, doubt as to liability, effective tax administration; currently not collectible status
- Appeals: administrative appeal independent of exam; written protest required for cases more than $25,000
- Forum selection: Tax Court (do not pay first); District Court / Court of Federal Claims (pay first, sue for refund; jury trial available in District Court)
- Innocent spouse relief (Section 6015): traditional (Section 6015(b)); separation of liability (Section 6015(c)); equitable (Section 6015(f)); no time limit for equitable relief post-Taxpayer First Act

---

#### 10-judicial-doctrines.md
IRC Section 7701(o); Common Law Doctrines

Cover each doctrine: definition, legal source, application, penalty exposure.

Economic substance (Section 7701(o)): codified 2010; conjunctive two-prong -- objective (meaningful change in economic position apart from tax effects) AND subjective (substantial non-tax purpose); strict-liability 20%/40% penalties; no reasonable cause defense

Substance over form: IRS may recharacterize where legal form diverges from economic reality; Frank Lyon Co. v. US (1978)

Step transaction doctrine: collapses multi-step series into single transaction; three tests: binding commitment test, end result test, interdependence test

Business purpose doctrine (Gregory v. Helvering, 293 U.S. 465, 1935): transactions without genuine non-tax business purpose may be disregarded

Sham transaction doctrine: lacks economic substance and non-tax purpose; Knetsch v. US (1960)

Assignment of income (Lucas v. Earl, 281 U.S. 111, 1930): taxed on income you earn; cannot shift by contract before earned; fruit/tree analogy

Constructive receipt (Reg. Section 1.451-2): income available without restriction is taxable whether or not physically received

Tax benefit rule (Section 111): recovery of previously deducted amount includable only to extent deduction provided tax benefit

Claim of right (Section 1341): taxable in receipt year; if repayment more than $3,000, deduct repayment OR take credit equal to tax paid in prior year -- whichever is greater

Related party rules (Sections 267, 318): loss disallowance between 13 categories of related parties; constructive ownership/attribution rules for stock ownership determinations

---

#### 10-itemized-deductions-salt.md
**Word limit: 2,500-3,500** (covers 7 deduction categories with OBBBA changes, phase-outs, and PTET rules)

IRC Sections 163, 164, 165, 170, 213, Schedule A

Cover:
- SALT (Section 164): OBBBA raised to $40,000 for 2025-2029; increases 1% annually; phase-down reduces cap $0.30 per dollar of MAGI above $500,000; reverts to $10,000 in 2030; includes state/local income taxes OR sales taxes (election) and property taxes; does NOT include foreign taxes
- PTET pass-through entity tax elections: IRS Notice 2020-75 approved; entity deducts state tax as business expense; partners/shareholders receive state tax credit; OBBBA preserved
- Mortgage interest (Section 163(h)): acquisition debt up to $750,000 ($375,000 MFS) permanently under OBBBA; home equity interest deductible only if proceeds used to buy/build/improve qualified residence; points deductible in year paid on purchase of principal residence
- Charitable (Section 170): OBBBA 0.5% AGI floor for itemizers; cash to public charities 60% AGI limit; capital gain property 30% limit; 5-year carryforward; written acknowledgment required for gifts of $250 or more; qualified appraisal for noncash gifts more than $5,000; non-itemizer deduction $1,000 (single) / $2,000 (MFJ) for 2026+; 35% rate cap on benefit for 37% bracket taxpayers
- Casualty losses (Section 165): federally declared disasters only post-TCJA; OBBBA expanded to state-declared disasters for 2026+; 10% AGI floor and $100 per-casualty floor
- Medical (Section 213): deductible above 7.5% of AGI (permanently extended by OBBBA); includes premiums if not pre-tax, age-based LTC premium limits, qualified medical expenses
- Miscellaneous itemized: all eliminated; exceptions for reservists, performing artists, fee-basis government officials
- Overall limitation: OBBBA Pease-like limitation -- benefit of itemized deductions capped at 35% rate for taxpayers in the 37% bracket

---

### PART 11 - FORMS REFERENCE

#### 11-forms-master-reference.md
**Word limit: 3,000-4,000** (reference table covering 60+ forms with filing details)

Alphabetical/numerical table. For each form: number, full name, purpose, who files, due date, e-file threshold.

Must include at minimum:
FinCEN 114, Form 709, Form 706, Form 940, Form 941, Form 982, Form 1040, Form 1040-ES, Form 1041, Form 1065, Form 1098, Form 1098-T, Form 1099-B, Form 1099-C, Form 1099-DA, Form 1099-K, Form 1099-MISC, Form 1099-NEC, Form 1099-R, Form 1116, Form 1120, Form 1120-S, Form 2555, Form 3520, Form 3520-A, Form 4562, Form 4797, Form 5329, Form 5471, Form 6251, Form 6252, Form 7203, Form 7206, Form 8283, Form 8582, Form 8606, Form 8615, Form 8621, Form 8824, Form 8832, Form 8938, Form 8949, Form 8959, Form 8960, Form 8962, Form 8995, Form 8995-A, Schedule A, Schedule B, Schedule C, Schedule D, Schedule E, Schedule K-1 (1065), Schedule K-1 (1041), Schedule K-1 (1120-S), Schedule SE, W-2, W-3

---

## Build Order

Build in this exact sequence to respect dependencies:

1.  00-gross-income-definition.md
2.  00-gross-income-exclusions.md
3.  00-tax-calculation-waterfall.md
4.  00-filing-status.md
5.  00-ordinary-income-brackets.md
6.  10-judicial-doctrines.md          (doctrines inform interpretation of everything)
7.  09-obbba-complete-changes.md      (current law depends on this)
8.  01-capital-gains-losses.md
9.  01-property-sales-recapture.md
10. 01-basis-rules.md
11. 01-cancellation-of-debt.md
12. 01-cryptocurrency-digital-assets.md
13. 01-social-security-taxation.md
14. 02-qbi-deduction-199a.md
15. 02-rd-expenditures-174a-41.md
16. 02-depreciation-179-bonus.md
17. 02-startup-costs-195-248.md
18. 02-home-office-280a.md
19. 02-se-tax-health-insurance.md
20. 02-meals-entertainment-274.md
21. 02-hobby-loss-at-risk.md
22. 02-nol-excess-business-loss.md
23. 03-passive-activity-rules-469.md
24. 03-real-estate-cost-seg-1031.md
25. 03-installment-sales-453.md
26. 04-tax-credits-master.md
27. 05-retirement-contributions.md
28. 05-retirement-distributions.md
29. 06-entity-comparison.md
30. 06-scorp-payroll-compliance.md
31. 07-estate-gift-tax.md
32. 07-trust-fiduciary-tax.md
33. 08-international-fbar-fatca.md
34. 10-amt.md
35. 10-niit-additional-medicare.md
36. 10-penalties-interest.md
37. 10-irs-procedures-audit.md
38. 10-itemized-deductions-salt.md
39. 11-forms-master-reference.md      (last; cross-references everything)

---

## Quality Checklist

Run before finalizing each document:

- IRC section(s) cited in document header
- All dollar amounts specify 2025 or 2026
- OBBBA changes formatted as OLD RULE then NEW RULE with effective date
- At least one AGENT RULE block
- At least one TRAP block
- Cross-References section at bottom linking to related filenames
- No opinions, no editorializing -- law stated as fact
- No padding -- every sentence carries information
- 800-2,000 words per document (or per-file extended limit where noted)
- Relevant form numbers cited inline wherever a filing obligation exists
