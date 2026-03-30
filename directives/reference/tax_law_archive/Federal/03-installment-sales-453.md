# Installment Sales
**IRC Section(s):** Sections 453, 453A
**Relevant Forms:** Form 6252 (Installment Sale Income), Form 4797 (Sales of Business Property), Form 8949 / Schedule D
**Tax Years Covered:** 2025-2026
**Last Updated:** March 2026

---

## Overview

An installment sale is any disposition of property in which at least one payment is received after the close of the tax year in which the sale occurs (IRC 453(b)(1)). The installment method is the **default** reporting method for qualifying sales -- the taxpayer does not need to elect in; instead, a taxpayer must affirmatively elect **out** if they wish to report the full gain in the year of sale (IRS Publication 537 (2025)).

Under the installment method, gain is recognized proportionally as payments are received rather than in a single lump sum. Each payment the seller receives is treated as consisting of three components: (1) a tax-free return of the seller's adjusted basis, (2) taxable gain, and (3) interest income.

The installment method is reported on **Form 6252**, which must be filed in the year of the sale and in every subsequent year in which a payment is received (or the obligation remains outstanding) until the final payment is collected or the obligation is disposed of (IRS Form 6252 Instructions).

---

## Rules

### Gross Profit Ratio

The core mechanic of the installment method is the **gross profit ratio** (also called the gross profit percentage). Gain recognized in any year equals total payments received during the year (excluding interest) multiplied by this ratio.

**Gross Profit Ratio = Gross Profit / Contract Price**

The terms are defined as follows:

- **Selling Price**: The total agreed-upon price for the property, including cash, the fair market value (FMV) of other property received, and the principal amount of any installment obligation. Interest (stated or unstated) is excluded.

- **Gross Profit**: Selling Price minus the seller's Adjusted Basis in the property (including selling expenses). This represents the total gain to be recognized over the life of the installment obligation.

- **Contract Price**: Selling Price minus any qualifying indebtedness assumed by the buyer, **but** if the assumed mortgage exceeds the seller's adjusted basis, the excess is added back to the contract price. In effect, Contract Price equals the total of all payments the seller will actually receive from the buyer (directly or constructively).

If the mortgage assumed by the buyer equals or exceeds the seller's installment sale basis, the gross profit ratio will always be 100% (IRS Publication 537 (2025)).

**Example**: A seller sells property for $1,000,000. Adjusted basis is $400,000. The buyer assumes a $200,000 mortgage. Gross Profit = $1,000,000 - $400,000 = $600,000. Contract Price = $1,000,000 - $200,000 = $800,000. Gross Profit Ratio = $600,000 / $800,000 = **75%**. Each dollar of principal payment received triggers $0.75 of recognized gain.

### Depreciation Recapture

Depreciation recapture income under **Sections 1245 and 1250** is **not** eligible for installment treatment. All depreciation recapture must be recognized in full in the year of the sale, regardless of whether any installment payment has been received in that year (IRC 453(i); IRS Publication 537 (2025)).

- **Section 1245 recapture** (personal property such as equipment, vehicles, furniture): The lesser of gain recognized or total depreciation allowed/allowable is recharacterized as ordinary income.
- **Section 1250 recapture** (real property): Only the "additional depreciation" (excess over straight-line) is recaptured as ordinary income. Unrecaptured Section 1250 gain (the straight-line portion) is taxed at a maximum 25% rate.
- **Section 179 deduction recapture** is also recognized in full in the year of sale.

The recapture income is computed in Part III of Form 4797 and reported as ordinary income in Part II of Form 4797. It is also entered in Part I of Form 6252, but only gain **in excess of** the recapture amount is spread over the installment payments (IRS Publication 537 (2025); The Tax Adviser).

### Exclusions from the Installment Method

The following dispositions **cannot** use the installment method (IRC 453(b)(2), 453(k), 453(l)):

| Excluded Category | Statutory Basis |
|---|---|
| **Dealer dispositions** -- property held for sale to customers in the ordinary course of business | IRC 453(l) |
| **Inventory** (personal property regularly sold) | IRC 453(b)(2)(A) |
| **Publicly traded stocks and securities** | IRC 453(k)(2) |
| **Depreciation recapture income** (recognized in full in year of sale even if installment method applies to remainder) | IRC 453(i) |

Gain or loss on excluded property must be reported in full in the year of sale, even if payments are received in later years.

### Election Out of the Installment Method

A taxpayer may irrevocably elect out of installment reporting and recognize the entire gain in the year of sale (IRC 453(d)). This is done by **not** filing Form 6252 and instead reporting the sale on Form 8949, Form 4797, or Schedule D.

**Timing**: The election must be made by the due date (including extensions) of the return for the year of sale. An automatic 6-month extension is available -- if the return was timely filed without the election, the taxpayer may file an amended return within 6 months of the original due date (excluding extensions), writing "Filed pursuant to section 301.9100-2" at the top (IRS Publication 537 (2025)).

**Revocation**: The election out is generally **irrevocable** without IRS consent. The IRS will approve revocation only if the taxpayer can show circumstances that were not reasonably foreseeable at election time.

**When electing out is beneficial**:
- Current-year capital losses or net operating losses are available to absorb the gain.
- Tax rates are expected to increase in future years.
- The seller wants to simplify ongoing compliance.
- The seller wants to avoid potential Section 453A interest charges on large obligations.

### Contingent Payment Sales

A contingent payment sale occurs when the total selling price cannot be determined by the end of the tax year of sale -- for example, when the price includes an earn-out based on future business profits (IRC 453; Treas. Reg. 15a.453-1(c)).

The regulations provide three tiers of rules based on what is determinable:

1. **Maximum selling price determinable** (Treas. Reg. 15a.453-1(c)(2)): Basis is recovered ratably assuming the maximum price will be received. The gross profit ratio is computed using the stated maximum. If the maximum price is later reduced, the ratio is recomputed prospectively.

2. **No maximum price, but fixed payment period** (Treas. Reg. 15a.453-1(c)(3)): Basis is allocated in equal annual increments over the payment period. Gain each year = actual payments received minus the allocated basis for that year.

3. **Neither maximum price nor fixed period determinable** (Treas. Reg. 15a.453-1(c)(4)): Basis is recovered in equal annual increments over **15 years** from the date of sale. If payments in a given year are less than the allocated basis, no loss is recognized; instead, the excess basis is reallocated over the remaining years. A loss is recognized only if the obligation becomes worthless under the standard bad-debt timing rules.

---

## Key Thresholds and Figures

| Item | Threshold / Rate | Source |
|---|---|---|
| Installment sale definition | At least 1 payment received after end of tax year of sale | IRC 453(b)(1) |
| Section 453A sales price threshold | Sales price must exceed **$150,000** | IRC 453A(b)(1) |
| Section 453A aggregate obligation threshold | Year-end outstanding installment obligations must exceed **$5,000,000** | IRC 453A(b)(2) |
| Interest rate on deferred tax liability | IRC 6621(a)(2) underpayment rate in effect in last month of taxpayer's tax year | IRC 453A(c)(2) |
| Maximum capital gains rate (for deferred tax calc) | 20% (plus 3.8% NIIT if applicable) | IRC 1(h), 1411 |
| Unrecaptured Section 1250 gain rate | Maximum **25%** | IRC 1(h)(1)(E) |
| Contingent sale -- default basis recovery period (neither max price nor fixed period) | **15 years** | Treas. Reg. 15a.453-1(c)(4) |
| Election out deadline | Due date of return (including extensions); automatic 6-month extension available | IRC 453(d); Reg. 1.9100-2 |

---

## Section 453A Interest Charge

Section 453A imposes an annual interest charge on the deferred tax liability associated with large installment obligations. The purpose is to reduce the time-value benefit of deferring gain recognition.

### When Section 453A Applies

Both conditions must be met:
1. The **sales price** of the property exceeds **$150,000** (per obligation).
2. The **aggregate face amount** of all installment obligations arising during the tax year and outstanding at year-end exceeds **$5,000,000** (measured at the taxpayer level; for partnerships/S corps, applied at the partner/shareholder level).

### Calculation Steps

1. **Deferred Tax Liability** = Unrecognized Gain on Outstanding Obligations x Maximum Tax Rate
   - Unrecognized Gain = Outstanding Obligation Balance x Gross Profit Percentage
   - Maximum Tax Rate = applicable rate under IRC 1, 11, or 1201 (e.g., 20% for long-term capital gains, 37% for ordinary income)

2. **Applicable Percentage** = (Aggregate Obligations Outstanding at Year-End - $5,000,000) / Aggregate Obligations Outstanding at Year-End

3. **Interest Charge** = Deferred Tax Liability x Applicable Percentage x IRC 6621(a)(2) Underpayment Rate (in effect in the last month of the taxpayer's tax year)

### Deductibility of the Interest

- **Individuals**: The Section 453A interest charge is generally treated as **nondeductible personal interest** (The Tax Adviser).
- **Corporations**: May deduct the interest as a business expense.

### Example

Seller enters a $50 million installment sale; entire obligation remains outstanding at year-end. Gross profit percentage is 100%.

- Deferred Tax Liability: $50M x 20% = $10,000,000
- Applicable Percentage: ($50M - $5M) / $50M = 90%
- Interest Charge (at 3% underpayment rate): $10M x 90% x 3% = **$270,000 per year**

(Source: WealthStone Group; The Tax Adviser)

### Exceptions

Section 453A does **not** apply to:
- Sales of personal-use property.
- Sales of farm property (if not a dealer) under IRC 453A(b)(3).
- Any disposition to which the installment method does not apply.

The $5 million threshold is computed per taxpayer. Married individuals filing jointly are **not** treated as a single person for this threshold (TAM 9853002).

---

## OBBBA Changes (if applicable)

No changes to Sections 453 or 453A were enacted under the One Big Beautiful Bill Act (OBBBA) as of March 2026. The installment sale rules, including the Section 453A interest charge thresholds, remain unchanged from their Tax Cuts and Jobs Act (TCJA) posture. Monitor for any future reconciliation or tax reform legislation that could modify the $5 million threshold or the treatment of depreciation recapture in installment sales.

---

## Agent Rules

1. **Default method**: If a sale qualifies (at least one payment after year of sale, not an excluded category), the installment method applies automatically. Do not treat it as an election-in situation.
2. **Always separate depreciation recapture**: When analyzing an installment sale of depreciable property, first isolate the Section 1245/1250 recapture amount and report it in full in year of sale. Only the gain exceeding recapture flows through the installment method.
3. **Compute gross profit ratio precisely**: Gross Profit / Contract Price, not Gross Profit / Selling Price. The distinction matters when the buyer assumes a mortgage.
4. **Check the $5M threshold annually**: Section 453A interest is recalculated each year based on year-end outstanding balances. The applicable percentage is locked in the year the obligation arises but the deferred tax liability changes as payments reduce the outstanding balance.
5. **Election out is irrevocable**: Confirm the taxpayer understands this before proceeding. Once reported in full, the taxpayer cannot switch back to installment reporting without IRS consent.
6. **Contingent payment sales -- identify the tier**: Determine whether a maximum selling price exists, whether the payment period is fixed, or neither. The basis recovery rules differ significantly across the three scenarios.
7. **Form 6252 every year**: File Form 6252 in the year of sale and every subsequent year until the obligation is fully collected or disposed of, even in years when no payment is received.
8. **Related-party sales**: Watch for IRC 453(e) -- if the related buyer resells within 2 years, the original seller must accelerate gain recognition. Flag any related-party installment sale for this rule.
9. **Interest on the note**: Ensure the installment obligation carries adequate stated interest at or above the applicable federal rate (AFR) under IRC 1274(d). If not, OID or unstated interest rules apply.

---

## Common Traps

1. **Confusing Selling Price with Contract Price**: Using the selling price as the denominator in the gross profit ratio instead of the contract price will understate the ratio when the buyer assumes debt, leading to underreported gain in early years.

2. **Forgetting depreciation recapture in year of sale**: Taxpayers sometimes defer the entire gain, including recapture, which triggers underpayment penalties when caught.

3. **Missing Section 453A interest**: Taxpayers with large installment obligations who fail to compute and pay the annual interest charge face assessments with interest and penalties. This is particularly common in real estate and business sales exceeding $5 million.

4. **Electing out without strategic analysis**: Electing out when the taxpayer has no losses to absorb the gain, or when current rates are favorable, wastes the deferral benefit. Conversely, failing to elect out when large losses are available wastes those losses.

5. **Failing to file Form 6252 in zero-payment years**: The form must be filed every year the obligation is outstanding, not only in years when a payment is received.

6. **Related-party resale acceleration**: When property is sold on installment to a related party who then resells within 2 years, the original seller must recognize gain as if the resale proceeds were received directly (IRC 453(e)). This is frequently overlooked in family transactions.

7. **Contingent sales -- wrong basis recovery method**: Applying the standard gross profit ratio to a contingent sale (instead of the tiered rules in Treas. Reg. 15a.453-1(c)) produces incorrect gain calculations and potential IRS adjustments.

8. **Nondeductible interest for individuals**: The Section 453A interest charge is personal interest for individuals and is **not** deductible. Failing to account for this cost in planning overstates the net benefit of installment deferral.

9. **Installment sale of a business -- single asset treatment**: Selling a business in a single transaction requires allocating the selling price across asset classes. Some assets (inventory, receivables) cannot use the installment method; others (real property, goodwill) can. Treating the entire sale as a single installment asset is incorrect.

---

## Cross-References

| Topic | Document / Section |
|---|---|
| Basis rules (adjusted basis for gain computation) | `01-basis-rules.md` |
| Capital gains and losses (rate structure, netting) | `01-capital-gains-losses.md` |
| Property sales and depreciation recapture (Sections 1245, 1250, 1231) | `01-property-sales-recapture.md` |
| Ordinary income brackets (for Section 453A max rate) | `00-ordinary-income-brackets.md` |
| QBI deduction (potential interaction with installment income) | `02-qbi-deduction-199a.md` |
| Cancellation of debt (when installment obligation is cancelled) | `01-cancellation-of-debt.md` |
| OBBBA complete changes | `09-obbba-complete-changes.md` |
| IRS Publication 537 (2025) -- Installment Sales | [irs.gov/publications/p537](https://www.irs.gov/publications/p537) |
| Form 6252 and Instructions | [irs.gov/forms-pubs/about-form-6252](https://www.irs.gov/forms-pubs/about-form-6252) |
| Treas. Reg. 15a.453-1 (Contingent payment rules) | [law.cornell.edu/cfr/text/26/15a.453-1](https://www.law.cornell.edu/cfr/text/26/15a.453-1) |
| IRS Practice Unit -- Interest on Deferred Tax Liability | [irs.gov/pub/fatca/int_practice_units/interest-on-deferred-tax-liability.pdf](https://www.irs.gov/pub/fatca/int_practice_units/interest-on-deferred-tax-liability.pdf) |
