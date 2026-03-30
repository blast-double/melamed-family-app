# Pass-Through Entity SALT Planning — California

*Last Edited: 2026-03-26*

**R&TC Section(s):** Sections 19900–19907, 17052.10
**Parallel IRC Section:** N/A (state-level election); IRS Notice 2020-75
**California Conformity Status:** N/A — California standalone provision
**Relevant FTB Forms:** Form 3804, Form 3804-CR, Form 3893
**Tax Years Covered:** 2025–2026 (extended through 2030 by SB 132)
**Last Updated:** March 2026
**Citations:**
- [FTB PTE Elective Tax Help Page](https://www.ftb.ca.gov/file/business/credits/pass-through-entity-elective-tax/help.html)
- [FTB Tax News — PTE Elective Tax](https://www.ftb.ca.gov/about-ftb/newsroom/tax-news/index.html)
- [2025 Instructions for Form 3804-CR](https://www.ftb.ca.gov/forms/2025/2025-3804-cr-instructions.html)
- [FTB SB 132 Bill Analysis](https://www.ftb.ca.gov/tax-pros/law/legislation/2025-2026/SB132-062425.pdf)
- [IRS Notice 2020-75](https://www.irs.gov/pub/irs-drop/n-20-75.pdf)
- [Deloitte — Considerations for California's Pass-Through Entity Tax](https://www.deloitte.com/us/en/services/tax/articles/california-pass-through-entity-tax.html)
- [Grant Thornton — CA Extends PTE Tax, Amends Apportionment for Banks](https://www.grantthornton.com/insights/alerts/tax/2025/salt/a-e/ca-extends-pte-tax-amends-apportionment-for-banks-07-24)
- [Grant Thornton — The OBBBA and Potential State Tax Impact](https://www.grantthornton.com/insights/alerts/tax/2025/insights/the-obbba-and-potential-state-tax-impact)
- [RSM — Pass-Through Entity Elections Are Here to Stay](https://rsmus.com/insights/services/business-tax/pass-through-entity-elections-are-here-to-stay-what-you-need-to-know.html)
- [EY Tax Alert — California PTE Tax](https://taxnews.ey.com/news/2021-1007)
- [Moss Adams — California Proposes SALT Cap Workaround](https://www.mossadams.com/articles/2021/01/ca-proposes-salt-cap-workaround)

---

## Overview

The California Pass-Through Entity (PTE) Elective Tax is a SALT cap workaround that allows eligible partnerships, LLCs, and S corporations to pay a 9.3% entity-level tax on their qualified net income (QNI). In exchange, qualifying owners receive a nonrefundable credit against their personal income tax. Because the PTE tax is treated as a business deduction at the entity level for federal purposes (per IRS Notice 2020-75), it bypasses the SALT deduction cap that otherwise limits individual state tax deductions. This document focuses on the planning analysis — for the mechanics of the election, see the underlying PTE elective tax document (06-ca-pte-elective-tax.md).

---

## California Rule — Planning Framework

### Break-Even Analysis

The PTE election is beneficial when the federal tax savings from converting a capped individual SALT deduction into an uncapped entity-level business deduction exceeds any incremental costs or lost benefits.

**When the PTE election is clearly beneficial:**
- The owner's SALT deduction is already at or above the cap ($40,000 under OBBBA for 2025+; was $10,000 under TCJA for 2018–2024)
- The owner is in a high federal marginal tax bracket (32%+ / 35% / 37%)
- The entity has positive California-source net income
- All qualifying owners consent to the election

**When the PTE election may not be beneficial:**
- The owner's total SALT deductions are below the cap (the deduction would have been available anyway)
- The owner has significant other credits that could be displaced by the PTE credit ordering rules
- The entity has losses (no QNI to tax)
- The owner is in a low federal marginal bracket

### Modeling Example

**Assumptions:** Single taxpayer; $500,000 of K-1 income from a California S corporation; no other SALT deductions used; 37% federal marginal rate; 9.3% CA tax rate; OBBBA SALT cap of $40,000.

**Without PTE Election:**
- California tax on $500,000 K-1 income: ~$46,500 (9.3% effective)
- Federal SALT deduction: Limited to $40,000 (OBBBA cap)
- Federal tax savings from SALT deduction: $40,000 x 37% = $14,800
- SALT overhang (non-deductible CA tax): $46,500 - $40,000 = $6,500
- Lost federal deduction: $6,500 x 37% = $2,405

**With PTE Election:**
- S corporation pays 9.3% PTE tax on $500,000 QNI = $46,500
- PTE tax deducted at entity level on federal Schedule K-1 (reduces owner's federal K-1 income by $46,500)
- Owner's federal taxable income reduced by $46,500 (no SALT cap applies to entity-level deduction)
- Federal tax savings: $46,500 x 37% = $17,205
- Owner claims PTE credit of $46,500 against California personal income tax
- Net CA tax effect: approximately zero (credit offsets liability, subject to ordering rules)
- Net federal benefit: $17,205 - $14,800 = **$2,405 additional federal savings**

The benefit increases as the SALT overhang grows (i.e., when total state taxes significantly exceed the SALT cap).

### Post-OBBBA Considerations

The OBBBA increased the SALT cap from $10,000 to $40,000 (with a phasedown for high-income taxpayers above $500,000 MAGI). This reduces the SALT overhang for many taxpayers, potentially reducing the PTE election benefit. However:

- Taxpayers with income well above $500,000 see the SALT cap phased down, increasing the overhang
- The PTE election converts 100% of the entity-level state tax into a federal deduction, not just the amount up to the cap
- The PTE election remains beneficial for any taxpayer whose total state taxes exceed the SALT cap (even at $40,000)

Per Grant Thornton analysis, the PTE election regimes will "continue to be appealing for many individual PTE owners who could still exceed the elevated SALT cap or are over the MAGI limit."

---

## Multi-State Considerations

### Credit for Taxes Paid to Other States

When a California resident owns interests in PTEs that operate in multiple states, the interaction between PTE taxes paid to other states and the California Other State Tax Credit (Schedule S) must be analyzed.

- If the other state also has a PTE election and the entity elects in both states, the California PTE credit may be reduced by credits available from other states
- The California OSTC (R&TC Sections 18001–18006) allows credit for net income taxes paid to other states on the same income, but credit ordering rules may limit the benefit

### Apportionment

For multi-state PTEs, the QNI subject to California PTE tax is the California-apportioned income of qualifying owners. Only income sourced to California and taxable under California law is included in QNI.

---

## Credit Ordering Rules

The PTE credit is applied against the owner's California "net tax" after other nonrefundable credits. The specific ordering:

1. Nonrefundable credits that do not have a carryover provision
2. Nonrefundable credits with a carryover provision (in order of expiration)
3. **PTE elective tax credit (Form 3804-CR)**

**Critical limitation:** The PTE credit **cannot reduce or offset** the Behavioral Health Services Tax (formerly Mental Health Services Tax) — the 1% additional tax on taxable income over $1,000,000 (R&TC Section 17043(c)(1)). This means high-income taxpayers will always owe the BHS Tax regardless of PTE credits.

**Carryforward:** Unused PTE credit carries forward for up to **five years** or until exhausted.

For taxable years beginning on or after January 1, 2024, and before January 1, 2027, the $5,000,000 business credit limitation does NOT apply to the PTE elective tax credit.

---

## Guaranteed Payments

Guaranteed payments to partners and members for services or use of capital are **included in qualified net income** (QNI) for PTE tax purposes. This means:

- The entity pays 9.3% PTE tax on guaranteed payments (in addition to other K-1 income)
- The partner/member receives a PTE credit for their share
- The guaranteed payment is still deducted at the entity level for entity-level tax computation
- For federal purposes, the PTE tax on guaranteed payments is deductible at the entity level

This treatment ensures that guaranteed payments receive the same SALT cap workaround benefit as other pass-through income.

---

## Key Thresholds and Figures

| Item | Value |
|---|---|
| PTE tax rate | 9.3% of QNI |
| SALT cap (OBBBA, 2025+) | $40,000 ($20,000 MFS) |
| SALT cap phasedown | 30% of MAGI over $500,000 ($250,000 MFS) |
| PTE credit carryforward | 5 years |
| BHS Tax (not offset by PTE credit) | 1% on income over $1,000,000 |
| June 15 prepayment requirement | 50% of prior year PTE tax or $1,000 (whichever is greater) |
| Tax years available | 2021–2025 (AB 150); 2026–2030 (SB 132) |

---

## Election Mechanics (Summary)

- Election made on the entity's original, timely filed return (irrevocable for the tax year)
- **June 15 prepayment:** Must pay at least 50% of the prior year PTE tax or $1,000 (whichever is greater) by June 15 of the election year
- For 2021–2025 tax years: failure to make the June 15 payment disqualified the election entirely
- For 2026–2030 tax years (SB 132): failure to make the June 15 payment results in a 12.5% reduction of the credit rather than complete disqualification — a more forgiving rule
- Full PTE tax due with the timely filed return
- All qualifying owners must consent to inclusion of their pro rata/distributive share in QNI

---

## OBBBA Non-Conformity

The OBBBA does not modify or restrict state PTE tax regimes. IRS Notice 2020-75 remains fully in effect. The final OBBBA legislation removed earlier House and Senate draft language that would have placed restrictions on PTE tax regime utilization. The PTE election continues to be a valid SALT cap workaround for all post-OBBBA tax years.

California extended its PTE regime through 2030 (SB 132, enacted June 27, 2025) in anticipation of the OBBBA's extension of the SALT cap.

---

## Agent Rules

1. **Run the break-even analysis for every PTE owner.** The PTE election is not always beneficial. Compare the federal tax savings from the uncapped entity-level deduction against any lost credits or timing costs.

2. **The PTE credit cannot offset the BHS Tax.** For owners with income over $1,000,000, the 1% BHS Tax will always apply. Do not include the BHS Tax liability when projecting the PTE credit benefit.

3. **Guaranteed payments are included in QNI.** Do not exclude them from the PTE tax computation.

4. **The June 15 prepayment is required.** For 2026+ years, underpayment results in a 12.5% credit reduction (not disqualification). Still, timely payment is strongly advisable.

5. **PTE tax is excluded from estimated tax computation.** The PTE tax liability is not included in the individual's Form 540-ES estimated tax calculation. However, the PTE credit reduces the estimated tax the individual must pay.

6. **Multi-state analysis is essential.** If the entity operates in multiple states with PTE elections, coordinate the elections and credit ordering across jurisdictions.

---

## Common Traps

1. **Assuming the PTE election is always beneficial.** For taxpayers whose SALT deductions are below the cap, the election may produce no benefit or even a net cost due to credit ordering.

2. **Missing the June 15 prepayment.** For 2021–2025, this killed the election entirely. For 2026+, it reduces the credit by 12.5%.

3. **Forgetting the BHS Tax exclusion.** The PTE credit does not offset the BHS Tax, creating an irreducible 1% tax floor for high-income taxpayers.

4. **Not accounting for the OBBBA SALT cap increase.** The $40,000 cap (up from $10,000) reduces the SALT overhang. Recalculate the break-even for all owners.

5. **Failing to get all owner consents.** Every qualifying owner must consent to the election. One non-consenting owner can prevent the election for all.

6. **Ignoring credit carryforward.** If the PTE credit exceeds the current year's net tax, the unused portion carries forward five years. Track these carryforwards.

---

## Cross-References

- [06-ca-pte-elective-tax.md] — Full mechanics of the PTE election, QNI computation, Form 3804
- [08-ca-itemized-deductions.md] — SALT deduction rules at the individual level
- [08-ca-estimated-tax-penalties.md] — PTE tax excluded from estimated tax computation
- [10-ca-credit-other-states.md] — OSTC interaction with multi-state PTE elections
- [11-ca-forms-reference.md] — Form 3804, Form 3804-CR, Form 3893 filing details
