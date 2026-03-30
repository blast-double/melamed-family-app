# US Expat in Mexico City with US S‑Corp/C‑Corp and LLC: 2025 Tax Planning and Risk Analysis

## Executive Summary

This report analyzes the 2025 US federal tax implications for a US citizen living full‑time in Mexico City (330+ days per year, formal Mexican residency, exempt from Mexican income tax on foreign‑sourced income) who owns two US businesses: (1) a software company organized as either an S‑corporation or C‑corporation, from which no salary is taken and profits are reinvested; and (2) a US LLC from which the owner takes distributions.

Key points:

- As a US citizen, worldwide income is taxable in the US regardless of Mexican residence or Mexican exemptions, under the regime described in IRS Publication 54.[^1][^2]
- The taxpayer likely qualifies for the Foreign Earned Income Exclusion (FEIE) via the physical presence test (330 full days abroad) and can exclude up to 130,000 USD of **foreign earned income** for the 2025 tax year using Form 2555.[^3][^4][^5][^6]
- FEIE reduces **income tax** on qualifying earned income but does **not** reduce US self‑employment tax; net self‑employment earnings remain fully subject to SE tax even when FEIE is claimed.[^7][^1]
- S‑corp owner‑employees who receive distributions but no or very low W‑2 wages risk IRS reclassification and payroll tax assessments under the reasonable compensation doctrine.[^8][^9][^10]
- LLC distributive shares from an active trade or business are generally subject to self‑employment tax, regardless of cash distributions, when the member is actively involved.[^11][^12]
- The US–Mexico tax treaty primarily mitigates **double taxation** and allocates taxing rights, but it does not remove the underlying US citizenship‑based taxation; business profits are taxable in the other state mainly when attributable to a permanent establishment or fixed base.[^13][^14]
- Because little or no Mexican tax is paid under a local exemption, the Foreign Tax Credit (FTC) has limited utility; FEIE is usually more valuable for earned income in this low‑tax scenario.[^15][^16]
- Foreign account reporting (FBAR/FinCEN 114 and FATCA/Form 8938) and other international reporting obligations likely apply if foreign accounts and financial assets exceed relatively low thresholds.[^17][^18][^19]

The remainder of the report details how FEIE, self‑employment tax, entity structure, treaty rules, and reporting requirements interact for this profile and identifies high‑impact, legal tax‑minimization strategies and common audit risks.

***

## 1. Foreign Earned Income Exclusion (FEIE)

### 1.1 Eligibility via Physical Presence Test

The Foreign Earned Income Exclusion is available to US citizens and resident aliens with a **tax home** in a foreign country who have **foreign earned income** and meet either the bona fide residence test or the physical presence test, claimed using Form 2555 attached to Form 1040.[^5][^6][^20]

The **physical presence test** requires physical presence in one or more foreign countries for at least **330 full days** during any consecutive 12‑month period. A full day is a 24‑hour period from midnight to midnight in a foreign country; days in the US or in international waters/airspace do not count. The 12‑month period need not align with the calendar year, which provides some flexibility in planning.[^21][^4][^20][^3]

Given full‑time residence in Mexico City with 330+ days per year abroad and a foreign tax home, this profile generally qualifies for FEIE under the physical presence test, assuming no disqualifying US law issues and that personal services generating income are performed while physically outside the US.[^4][^20]

### 1.2 2025 FEIE Exclusion Limit and Covered Income

For the **2025** tax year, multiple expat‑oriented tax firms note that the maximum FEIE limit is **130,000 USD per qualifying taxpayer**. FEIE applies **only to foreign earned income**, typically defined as compensation for personal services performed abroad, including wages, salaries, professional fees, and self‑employment income from active services.[^6][^20][^3][^4][^5]

FEIE **does not** apply to:

- Dividends
- Interest
- Capital gains
- Rental income
- Pensions or annuities
- Purely passive income unrelated to services performed abroad[^4][^5]

These excluded income categories remain fully taxable and cannot be shielded by FEIE, although the Foreign Tax Credit may apply where foreign taxes are actually paid.[^5][^15]

### 1.3 What Counts as “Foreign Earned” in This Profile

The key determinant is **where the services are performed**, not where the client or entity is located. IRS guidance and expat practitioner materials emphasize that income for services actually performed outside the US counts as foreign earned, even if paid by a US company into a US bank account.[^2][^1]

For this profile:

- **LLC active income** (if the LLC is engaged in consulting, software development, or other services performed personally from Mexico) is typically foreign earned income up to the FEIE limit, provided the services are performed while in Mexico or other non‑US countries.
- If the software company is an **S‑corp** and pays wages for work physically done from Mexico, that W‑2 wage is generally foreign earned income potentially eligible for FEIE.
- If the software company is a **C‑corp** and pays a salary for services performed in Mexico, the wages are foreign earned income; corporate‑level retained earnings are not the shareholder’s income until distributed (e.g., as dividends), so they are not foreign earned income and cannot be excluded under FEIE.[^1][^5]

If all services generating business income are performed from Mexico City (and other non‑US locations), most active service income can qualify as foreign earned income, subject to the FEIE cap and other limitations.

### 1.4 Interaction of FEIE With LLC, S‑Corp, and C‑Corp Income

**Single‑member LLC taxed as a sole proprietorship or multi‑member LLC taxed as a partnership**:

- For US tax purposes, the LLC is generally pass‑through; the owner reports business income and deductions on Schedule C (sole proprietor) or Schedule E/K‑1 (partnership).
- Expat tax guidance and Form 2555 instructions confirm that self‑employment income from services performed abroad can be treated as foreign earned income eligible for FEIE.[^6][^5]
- Critically, FEIE operates at the **owner level**, not the entity level: the taxpayer calculates net self‑employment income, then applies FEIE to the portion that is foreign earned income, up to 130,000 USD.

**S‑corporation**:

- The S‑corp must pay **reasonable compensation** as W‑2 wages to shareholder‑employees providing services; those wages are the primary candidate for FEIE when services are performed abroad.[^9][^8]
- Remaining profits pass through as S‑corp income on Schedule K‑1. Pass‑through income is generally **not** treated as earned compensation for services in the same way as wages and may not qualify as foreign earned income, depending on the facts and whether the income is tied to the shareholder’s own services.[^2][^1]
- Distributions in excess of basis are typically taxable as capital gain, also not eligible for FEIE.[^1]

**C‑corporation**:

- Compensation paid as W‑2 wages for work performed in Mexico can be foreign earned income eligible for FEIE.
- Retained corporate earnings are taxed at the corporate level; when later distributed as dividends, those dividends are **not** foreign earned income and cannot be excluded with FEIE.[^5]

In practice, to maximize FEIE usage, foreign‑based owner‑operators usually:

- Pay themselves a **salary** from whichever entity they work for, reflecting compensation for services performed abroad.
- Classify that salary as foreign earned income and exclude up to the FEIE limit via Form 2555.

The current profile, with **zero salary from the software company** and only distributions from the LLC, underutilizes FEIE and raises other risks discussed in later sections.

***

## 2. Self‑Employment Tax and FEIE

### 2.1 FEIE Does Not Reduce Self‑Employment Tax

IRS guidance explicitly states that taxpayers must include **all self‑employment income** when calculating net earnings subject to US self‑employment (SE) tax, even if some or all of that income is excluded from income tax under the foreign earned income exclusion. In other words, FEIE reduces **income tax** but not SE tax.[^7]

The IRS example for a consultant abroad shows that a taxpayer with 95,000 USD of foreign earned income and 68,000 USD of net profit must still pay self‑employment tax on the full 68,000 USD even when FEIE is claimed. Expat tax commentary reinforces that FEIE does not eliminate FICA/SE obligations on self‑employment income unless the individual is covered by a foreign social security system under a totalization agreement, which Mexico does not currently have with the US for US citizens resident there.[^22][^7]

For an LLC treated as a sole proprietorship or partnership, this means:

- The owner’s **distributive share of active business income** is generally subject to SE tax regardless of whether it is excluded from income tax using FEIE.[^12][^11]

### 2.2 Self‑Employment Exposure for LLC Distributions

For **single‑member LLCs taxed as disregarded entities** and **multi‑member LLCs taxed as partnerships**, IRS and tax court authority generally treat active members’ distributive shares as **self‑employment income** when they materially participate, particularly after cases such as *Renkemeyer*. Practitioner guidance also emphasizes that SE tax is based on distributive share of active income, not on actual cash distributions.[^11][^12]

Key implications:

- If the LLC conducts an active trade or business and the owner works in it, the **entire net business income** is usually considered SE income.
- The fact that the owner takes distributions rather than a formal salary is irrelevant; SE tax hinges on **earnings**, not withdrawals.

Given this, the current profile likely owes US SE tax on the LLC’s active net income even if much or all of that income is excluded from income tax under FEIE.

### 2.3 Strategies to Reduce Self‑Employment Tax

Given FEIE does not mitigate SE tax, common strategies used by foreign‑based owner‑operators include:

- **Electing S‑corp treatment** for an LLC or operating via an S‑corp, then splitting owner‑operator compensation between:
  - W‑2 **reasonable salary** subject to payroll tax (Social Security and Medicare);
  - S‑corp **distributions** not subject to SE tax, though still subject to income tax.
- Carefully calibrating salaries to be “reasonable” to withstand IRS scrutiny while minimizing payroll taxes.[^10][^8][^9]
- In some countries, using a **totalization agreement** and paying into the foreign social security system to avoid US SE tax, but Mexico does not provide this route to fully avoid US SE on US‑sourced self‑employment income.[^22]

For this Mexico‑based profile, the most realistic SE‑tax‑reduction lever is S‑corp structuring and salary optimization, while recognizing that some Social Security/Medicare tax will remain unavoidable.

***

## 3. Reasonable Compensation Rules for S‑Corp Owner‑Employees

### 3.1 IRS Position on Reasonable Compensation

The IRS requires S‑corporations to pay **reasonable compensation** to shareholder‑employees in return for services provided before making non‑wage distributions. Form 1120‑S instructions state that distributions and other payments to a corporate officer must be treated as wages to the extent they represent reasonable compensation for services rendered.[^9]

Reasonable compensation is defined as the value that would ordinarily be paid for similar services by similar enterprises under similar circumstances. IRS and practitioner guidance indicate that:[^8][^10]

- Wages should be paid **before** distributions.
- A shareholder‑employee can take wages without distributions, but not the reverse.
- Underpaying wages in favor of distributions raises red flags and can lead the IRS to reclassify distributions as wages, imposing back payroll taxes and penalties.[^10][^8]

### 3.2 Risks of Taking Zero Salary

Operating an S‑corp where the shareholder‑employee provides substantial services but takes **zero salary** and reinvests all profits creates several risks:

- The IRS can argue that the owner should have received a reasonable salary for services rendered and reclassify a portion of corporate distributions or retained earnings as wages.[^9][^10]
- Reclassification can trigger:
  - Back Social Security and Medicare taxes,
  - Employer payroll tax liabilities,
  - Penalties and interest.
- The pattern of no wages and significant profits, especially in a service or software business where income is primarily from the shareholder’s efforts, is a well‑known audit trigger according to S‑corp audit technique guides and practitioner analysis.[^10][^9]

For a foreign‑based owner, the IRS can still enforce these rules because the S‑corp is a US entity with US filing obligations.

### 3.3 Structuring S‑Corp Compensation Legally

To align with IRS expectations while retaining tax efficiency:

- Determine a **reasonable market salary** for the role (CEO/CTO/founder‑developer) based on duties, time commitment, and comparable wages.[^8][^10]
- Pay that amount as **W‑2 wages** from the S‑corp; this salary is subject to US payroll taxes but may qualify as foreign earned income if the services are performed in Mexico, making it excludable under FEIE up to the limit.[^4][^5]
- Treat remaining distributable profits as **S‑corp distributions**, which are not subject to SE tax, though they remain subject to income tax (and generally are not foreign earned income).[^11][^9]
- Maintain documentation of the reasonable compensation analysis (job description, comparative salary data, hours worked) in case of audit.

This structure allows the owner to satisfy reasonable compensation rules, apply FEIE to foreign‑performed salary, and reduce SE tax compared with a pure sole‑proprietor/LLC model.

***

## 4. S‑Corp vs. C‑Corp Implications When Reinvesting Profits

### 4.1 Taxation of S‑Corps With Reinvested Profits

An S‑corp is a pass‑through entity; its income, deductions, and credits flow through to shareholders regardless of whether profits are distributed. Key points when profits are reinvested:[^2][^1]

- Shareholders report their share of S‑corp income on their personal returns even if no cash is distributed.
- Corporate‑level retention of earnings does not defer the shareholder’s income tax liability.
- Reasonable compensation rules still apply even when profits are retained.

For an S‑corp with a foreign‑based owner who takes no salary:

- The owner may recognize pass‑through income on Schedule K‑1 but have no W‑2 wages eligible for FEIE.
- This can lead to **higher US income tax** because FEIE primarily applies to wages and self‑employment income, not to pass‑through profits disconnected from direct service compensation.

### 4.2 Taxation of C‑Corps With Reinvested Profits

A C‑corp is a separate taxpayer subject to corporate income tax; shareholders are taxed only when they receive dividends or sell shares at a gain. When profits are reinvested:[^1]

- The corporation pays US corporate income tax on its profits.
- Retained earnings can be used to fund growth without immediate shareholder‑level taxation.
- Shareholders face taxation later on **dividends** (qualified or non‑qualified rates) or capital gains upon sale.

For a foreign‑based US shareholder taking no dividends:

- There may be **no current personal income** from the C‑corp, so FEIE is not directly relevant for retained corporate profits.
- If the shareholder also receives **no salary**, then there is no foreign earned income from that entity, and the tax planning focus shifts to other income sources (LLC, other wages) for FEIE utilization.

### 4.3 Trade‑offs for This Profile

**S‑corp advantages and issues:**

- Allows conversion of part of active income into distributions not subject to SE tax, which is attractive when FEIE can offset W‑2 salary but not SE income on the owner’s distributive share.
- Requires paying reasonable salary, which generates payroll tax obligations and administrative overhead.[^9][^10]
- Pass‑through income is taxed currently even when profits are reinvested, potentially creating cash‑flow strain.

**C‑corp advantages and issues:**

- Enables deferral of shareholder‑level tax on retained earnings used for growth, at the cost of corporate‑level tax and potential future double taxation on dividends or gains.[^1]
- No reasonable compensation rule at the shareholder level per se, but if the shareholder works for the company and receives no salary, the IRS can still challenge transfer pricing or constructive dividend issues in extreme cases.
- Provides less direct access to FEIE since retained earnings are not foreign earned income; FEIE would apply only to wages actually paid for foreign‑performed services.

Given that the software business currently pays **no salary** to the owner and reinvests all profits, the core tax planning question is whether it is presently an S‑corp creating phantom pass‑through income (with no FEIE optimization and reasonable compensation risk) or a C‑corp keeping income at the corporate level (potentially deferring shareholder tax but foregoing FEIE opportunities and facing C‑corp‑level tax).

***

## 5. LLC Distributions: Tax Treatment and Planning

### 5.1 Income vs. Distributions

For tax purposes, the key distinction is between **taxable income allocations** and **cash distributions**:

- In a single‑member LLC treated as a sole proprietorship, income and expenses are reported directly on Schedule C; withdrawals are not themselves taxable events.
- In a multi‑member LLC treated as a partnership, partners are taxed on their **distributive share** of income (from Schedule K‑1) regardless of actual cash distributions; distributions are generally non‑taxable returns of capital until basis is exhausted.[^11]

Thus, tax liability is driven by **earnings**, not by how much cash is taken out as distributions.[^11]

### 5.2 Self‑Employment Tax on LLC Income

Guidance on LLCs explains that for SMLLCs taxed as sole proprietorships and multi‑member LLCs taxed as partnerships, owners are subject to self‑employment tax on their distributive share of the LLC’s active income when they materially participate.[^12][^11]

Key elements:

- Courts have generally held that LLC members who actively provide services and participate in management are not “limited partners” for purposes of the SE tax exception and must pay SE tax on their distributive shares.[^12]
- Passive investors who do not materially participate may avoid SE tax on certain partnership/LLC income, but that is typically not the case for single‑founder operators.

For this profile, where the LLC is an operating business and the owner takes distributions tied to active work, the owner’s share of net income is almost certainly self‑employment income subject to SE tax.

### 5.3 Planning Opportunities With LLCs

Potential strategies include:

- **Elect S‑corp treatment** for the LLC (Form 2553), allowing a portion of profits to be taken as distributions not subject to SE tax, with the remainder paid as W‑2 salary and potentially excluded under FEIE when work is performed abroad.[^8][^9]
- Ensure robust **expense tracking and deductions** (equipment, software, home office, travel related to the foreign work location, etc.) to reduce net self‑employment income before SE tax is applied.[^1]
- Use entity‑level retirement contributions (e.g., Solo 401(k) or SEP‑IRA) based on earned income to reduce taxable income, recognizing that contributions are limited by compensation levels.[^1]

***

## 6. US–Mexico Income Tax Treaty Considerations

### 6.1 Business Profits and Permanent Establishment

The US–Mexico Income Tax Convention allocates taxing rights over **business profits** such that a contracting state may tax the business profits of an enterprise of the other state only to the extent they are attributable to a **permanent establishment** in that state. Business profits attributable to a permanent establishment include profits from assets or activities of that establishment determined on a net basis with deductions for expenses.[^13]

For a US citizen resident in Mexico operating US entities primarily serving US clients, the treaty primarily becomes relevant when Mexico might assert taxing rights over business profits sourced to a **Mexican permanent establishment**. Where income is viewed as US‑sourced and no Mexican permanent establishment exists for the US entity, Mexico often does not tax that income, especially under local rules providing exemptions to certain foreign‑sourced income for foreign residents.[^23][^14]

### 6.2 Independent Personal Services

Article 14 of the treaty addresses **independent personal services**, stating that income derived by an individual resident of one contracting state from independent personal services is taxable only in that state unless the individual has a fixed base or regularly available office in the other state; in that case, the other state may tax income attributable to that fixed base. This functions similarly to the business profits/permanent establishment concept but at the individual level.[^13]

For this profile, the treaty primarily protects against **Mexican** taxation of US‑sourced services performed from Mexico when no fixed base is recognized in Mexico under treaty concepts or when domestic Mexican law provides an exemption for certain foreign‑sourced income of foreign residents. However, the treaty does **not** exempt the taxpayer from US worldwide taxation as a US citizen.[^14][^23]

### 6.3 Practical Impact

Given the Mexican exemption from tax on foreign‑source income for certain foreign residents and the lack of significant Mexican tax paid, the treaty’s role is more about confirming non‑taxation in Mexico and avoiding double taxation than about reducing US tax.[^23][^14]

The treaty also coordinates withholding on dividends, interest, and royalties, but in this fact pattern those are secondary compared with active business income and salary.

***

## 7. Foreign Tax Credit (FTC) vs. FEIE

### 7.1 Overview of FEIE vs. FTC

The **Foreign Earned Income Exclusion (FEIE)** removes up to a fixed amount of **foreign earned income** from US taxable income, whereas the **Foreign Tax Credit (FTC)** provides a **dollar‑for‑dollar credit** against US tax for foreign income taxes paid, subject to limitation formulas.[^15]

Comparison points from expat tax resources:

- FEIE applies only to **earned income** (wages and self‑employment) and is capped at 130,000 USD per person for 2025.[^15][^5]
- FTC can apply to earned and passive income (interest, dividends, rents) and has **no nominal cap**, but credits cannot exceed the US tax on the same income and require actual foreign tax paid.
- FEIE is typically favored in **low‑tax or zero‑tax** countries, while FTC is often superior where foreign tax rates are higher than US rates.[^24][^15]

### 7.2 Limited Usefulness of FTC With Little or No Mexican Tax

The FTC is only available where foreign income taxes are actually paid; if no foreign tax is paid, there is no credit to claim. For US expats in Mexico who are exempt from Mexican income tax on foreign‑sourced income, this makes FTC largely irrelevant for that income.[^16]

In this profile, because Mexican law allows an exemption from income tax on certain foreign‑sourced income earned by qualifying foreign residents and the taxpayer is not paying Mexican income tax on the US‑based business income, FTC will not significantly reduce US tax.[^14][^16][^23]

### 7.3 Interaction and Edge Cases

Key interaction rules:

- The same income cannot be used for both FEIE and FTC; if income is excluded under FEIE, foreign taxes paid on that income cannot generate an FTC.[^22][^15]
- Taxpayers can **mix** strategies: use FEIE for a portion of foreign earned income, FTC for other income or excess foreign taxes, and neither for US‑source income.

Edge cases relevant to this profile:

- If in the future the taxpayer begins paying Mexican tax (e.g., due to a change in status or law), then FTC may become relevant, and a reevaluation of FEIE vs. FTC strategy would be warranted.
- If there is passive foreign‑source income taxed by Mexico, FTC could apply to that income even if FEIE is used for active salary.

***

## 8. IRS Forms and Reporting Requirements for This Profile

### 8.1 Form 2555 – Foreign Earned Income Exclusion

Form 2555 is used to claim FEIE (and, where relevant, the foreign housing exclusion/deduction). For 2025:[^6][^5]

- It allows exclusion of up to 130,000 USD of foreign earned income per qualifying taxpayer.
- It requires information about foreign residence, tax home, the qualification test used (physical presence), and details about foreign earned income.
- It is filed with Form 1040, not as a standalone return.[^5][^6]

### 8.2 Form 8938 (FATCA) – Specified Foreign Financial Assets

Under FATCA, US persons with foreign financial assets exceeding certain thresholds must file Form 8938. For individuals living abroad, current guidance indicates:[^25][^17]

- **Single** foreign residents must file if total specified foreign financial assets exceed 200,000 USD on the last day of the year or 300,000 USD at any time during the year.[^17]
- **Married filing jointly abroad**: thresholds double to 400,000 USD year‑end or 600,000 USD during the year.[^17]

Specified foreign financial assets include foreign bank accounts, foreign securities, interests in foreign entities, and certain foreign pensions and life‑insurance policies. US business interests held through US entities are not foreign assets for Form 8938, but personally held foreign accounts in Mexico or elsewhere generally are.[^25][^17]

### 8.3 FBAR (FinCEN Form 114) – Foreign Bank Account Reporting

US persons must file FBAR if the aggregate maximum value of foreign financial accounts exceeds **10,000 USD** at any time during the calendar year.[^18][^19][^26]

Key features:

- The 10,000 USD threshold is based on **aggregate maximum value**, not per‑account limits.[^19][^18]
- FBAR is filed electronically with FinCEN, separate from the tax return, by April 15 with an automatic extension to October 15.[^19]
- It covers foreign bank accounts, brokerage accounts, and accounts over which the person has signature authority, including certain business accounts.[^18][^19]

Given residency in Mexico and likely use of Mexican bank accounts, FBAR filing is often required.

### 8.4 Other Possible Forms

Depending on the exact structure and ownership of the US entities and any foreign entities or accounts, other forms may apply:

- **Form 5471** for US persons who are officers, directors, or shareholders in certain foreign corporations (not applicable if all operating entities are US entities).
- **Form 8865** for interests in foreign partnerships.
- **Form 8858** for foreign disregarded entities.

Even if not currently relevant, these forms matter if future structuring involves Mexican or other foreign entities.[^2][^1]

***

## 9. High‑Impact Legal Tax Reduction Strategies for This Profile

This section synthesizes the above rules into practical, high‑impact strategies tailored to a US citizen resident in Mexico with US entities and minimal foreign tax paid.

### 9.1 Maximize FEIE on Genuine Foreign‑Performed Compensation

- Ensure that **compensation for services performed from Mexico** is clearly characterized as earned income (wages or self‑employment) so it can qualify as foreign earned income.
- For the LLC or S‑corp, pay yourself a **foreign‑source salary** reflecting work actually done from Mexico, then exclude up to 130,000 USD under FEIE.[^4][^6][^5]
- Use the **physical presence test** carefully to ensure 330+ full days abroad in a consistent 12‑month period spanning the tax year.[^3][^21]

Impact: Reduces US income tax substantially on the first 130,000 USD of foreign earned income; especially valuable in a low‑tax country like Mexico where no FTC is available.

### 9.2 Shift From Pure LLC SE Income Toward S‑Corp Salary + Distributions

- Consider **electing S‑corp status** for the LLC (if not already in place) or restructuring operations into a single S‑corp entity.
- Pay a **reasonable salary** that is:
  - High enough to satisfy IRS reasonable compensation standards, and
  - Low enough to reduce total payroll tax burden.
- Treat additional profits as **S‑corp distributions** not subject to SE tax.

Impact: By reducing the share of income exposed to SE tax while keeping salary within FEIE limits, this can materially reduce combined income and payroll tax liability.[^10][^8][^9]

### 9.3 Align Software Company Structure With Goals

Depending on whether the software business is currently an S‑corp or C‑corp:

- If it is an **S‑corp**:
  - Start paying a **reasonable foreign‑source salary** to create FEIE‑eligible income and satisfy reasonable compensation rules.
  - Accept current taxation of pass‑through profits but consider whether they can be minimized via reinvestment in deductible expenses and retirement contributions.
- If it is a **C‑corp**:
  - Decide whether the goal is **deferral** (leave profits in the company) or **personal cash flow**.
  - If personal cash is needed, pay a salary (eligible for FEIE) rather than dividends (not eligible for FEIE and potentially double taxed).

Impact: Proper structuring can either enhance FEIE usage (through salary) or intentionally defer personal‑level tax via a C‑corp, at the cost of corporate‑level tax.

### 9.4 Aggressive but Defensible Expense and Retirement Planning

- Carefully document and deduct all ordinary and necessary business expenses for the LLC/S‑corp: software, hosting, subcontractors, professional fees, and a properly calculated home office for work done from Mexico.[^2][^1]
- Use **retirement plans** (Solo 401(k), SEP‑IRA) to shelter income; contributions are generally based on earned income (salary or SE income) and can significantly reduce taxable income.

Impact: Reduces both income and, in the case of self‑employment income, the base for SE tax.

### 9.5 Maintain Compliance With FEIE, FBAR, and FATCA

- File Form 2555 correctly each year, maintaining a calendar and travel logs to document physical presence abroad.[^6][^4]
- File FBAR whenever foreign account balances exceed 10,000 USD in aggregate; penalties for non‑compliance can be severe.[^26][^18][^19]
- File Form 8938 if specified foreign financial assets exceed expat thresholds (200,000–300,000 USD single, higher if married).[^17]

Impact: While not a tax‑reduction strategy per se, full compliance avoids large penalties that can wipe out tax savings.

### 9.6 Consider Long‑Term Planning Around Residency and Entity Location

- Monitor any changes in Mexican tax residency rules or the special exemption applicable to US citizens; if Mexico begins taxing this income, FTC strategy may become more favorable than FEIE.[^23][^14]
- If operations grow substantially, consider whether forming or using a Mexican or other foreign entity would produce a better overall tax outcome, recognizing the added complexity (CFC rules, Form 5471, etc.).[^2][^1]

Impact: Strategic adjustments over time can optimize between FEIE, FTC, and deferral as facts and laws change.

***

## 10. Common Mistakes and Audit Risks for US Expats With US Pass‑Through Income

### 10.1 Underusing or Misapplying FEIE

- Failing to file Form 2555 despite qualifying, resulting in unnecessarily high US tax.[^27][^6]
- Treating non‑earned income such as dividends or capital gains as foreign earned income, which the IRS explicitly disallows.[^4][^5]
- Miscounting days for the physical presence test and falling short of 330 full days.

### 10.2 Ignoring Self‑Employment Tax

- Assuming FEIE eliminates SE tax on Schedule C or partnership/LLC income; IRS guidance makes clear that SE tax is calculated on net earnings before FEIE.[^7][^22]
- Treating active LLC income as exempt from SE tax without a solid legal basis; tax court cases have repeatedly rejected such positions for active members.[^12]

### 10.3 S‑Corp Reasonable Compensation Failures

- Taking large S‑corp distributions with little or no wages, which the IRS specifically warns is improper and subject to reclassification.[^9][^10]
- Not documenting how the compensation level was determined.

### 10.4 International Reporting Non‑Compliance

- Failing to file FBAR when total foreign accounts exceed 10,000 USD at any time.[^18][^19]
- Failing to file Form 8938 when foreign asset thresholds are met, or misunderstanding that US‑incorporated entities are not “foreign assets” even if operating abroad.[^25][^17]

### 10.5 Treaty and Residency Assumptions

- Assuming that Mexican residency or treaty protections eliminate US tax obligations; US citizens remain subject to worldwide taxation regardless of residence.[^2][^1]
- Misapplying treaty business profits or independent personal services articles without understanding permanent establishment or fixed base concepts.

***

## Conclusion

For a US citizen living full‑time in Mexico City with US‑based LLC and software operations and no or minimal Mexican tax, the most powerful tools for reducing US tax are: (1) properly structured **foreign‑source salary** eligible for FEIE, (2) **S‑corp structuring** to mitigate self‑employment tax while respecting reasonable compensation rules, and (3) rigorous compliance with FBAR/FATCA and other international reporting rules to avoid penalty‑driven losses.[^3][^7][^15][^17][^5][^9]

The current posture—taking LLC distributions, reinvesting all software company profits, taking no salary, and paying no Mexican tax—leaves SE tax largely unaddressed and creates S‑corp reasonable compensation risk if the software entity is an S‑corp. Adjusting compensation structures, entity elections, and FEIE usage, ideally with a cross‑border tax specialist familiar with US–Mexico issues, can materially reduce ongoing tax liability while staying within US and Mexican law.[^14][^13][^23][^8][^2]

---

## References

1. [Tax Guide for U.S. Citizens and Resident Aliens Abroad ...](https://www.efile.com/tax-service/forms/tax-guide-for-us-citizens-and-resident-aliens-abroad-pub-54/) - Navigate tax obligations abroad with Pub 54 - Tax Guide for US Citizens and Resident Aliens Abroad. ...

2. [Pub. 54: Tax Rules for U.S. Citizens & Resident Aliens Abroad](https://accountinginsights.org/pub-54-tax-rules-for-u-s-citizens-resident-aliens-abroad/) - Learn the core principles of U.S. taxation for Americans living abroad. This guide clarifies how to ...

3. [Physical Presence Test: What It Is, How It Works](https://www.investopedia.com/terms/p/physical-presence-test.asp) - The physical presence test allows taxpayers to claim the foreign earned income exclusion if they hav...

4. [Physical presence test 2026: 330-day rule explained](https://www.taxesforexpats.com/articles/expat-tax-rules/physical-presence-test.html) - Complete guide to IRS physical presence test: 330-day requirement, calculation examples, vs bona fid...

5. [IRS Form 2555 Foreign Earned Income Exclusion for Expats](https://www.manaycpa.com/irs-form-2555-foreign-earned-income-exclusion/) - Living abroad? Use IRS Form 2555 to lower your U.S. taxes. Manay CPA helps expats qualify and file t...

6. [How To Fill Out IRS Form 2555 For The Foreign Earned ...](https://usataxgurus.com/how-to-fill-out-irs-form-2555/) - If you live and work outside the United States, you may not have to pay U.S. taxes on all of your in...

7. [Self-employment tax for businesses abroad | Internal Revenue Service](https://www.irs.gov/individuals/international-taxpayers/self-employment-tax-for-businesses-abroad) - Self-Employment Tax for Businesses Abroad

8. [The S Corp Owner's Guide to Reasonable Compensation - RCReports](https://rcreports.com/brochure/what-is-reasonable-compensation-a-primer-for-s-corp-owners/) - Read this primer for S Corp Owner primer to learn the basics of reasonable compensation, why it's es...

9. [S corporation compensation and medical insurance issues - IRS](https://www.irs.gov/businesses/small-businesses-self-employed/s-corporation-compensation-and-medical-insurance-issues) - When computing compensation for employees and shareholders, S corporations may run into a variety of...

10. [S-corp reasonable compensation: what every tax preparer should ...](https://www.natptax.com/news-insights/blog/s-corp-reasonable-compensation-what-every-tax-preparer-should-know/) - Distributions over wages raise red flags for S corporations. Master reasonable compensation rules be...

11. [How Are LLC Distributions Taxed? 2025 Guide](https://1800accountant.com/blog/how-are-llc-distributions-taxed) - Learn how LLC distributions are taxed for single-member, partnership, S corp, and C corp LLCs—plus b...

12. [IRS pursuing self-employment taxes from LLC members](https://www.journalofaccountancy.com/issues/2018/may/self-employment-taxes-llc-members/) - IRS court victories asserting that LLC members should pay self-employment taxes on distributive shar...

13. [United States – Mexico Income Tax Convention](https://www.irs.gov/pub/irs-trty/mexico.pdf) - In such case the provisions of Article 7 (Business Profits) or Article 14 (Independent Personal. Ser...

14. [Mexico expat taxes: Guide for US citizens](https://wise.com/us/blog/mexico-expat-taxes) - If you're a US expat in Mexico, check out this guide to know whether you're subject to Mexican taxes...

15. [FEIE vs FTC: Which U.S. Expat Tax Strategy Is Best for You?](https://www.greenbacktaxservices.com/knowledge-center/feie-vs-ftc/) - Compare the Foreign Earned Income Exclusion (FEIE) and Foreign Tax Credit (FTC). Learn which saves y...

16. [Which is better: Foreign Tax Credit or FEIE? | Expat US Tax](https://www.expatustax.com/foreign-tax-credit-vs-foreign-earned-income-exclusion/) - Unsure whether to use the Foreign Tax Credit or Foreign Earned Income Exclusion as a U.S. expat? Lea...

17. [IRS Form 8938: Filing requirements & who must report (2026)](https://www.taxesforexpats.com/articles/fbar-fatca/form-8938.html) - Filing your 2025 return? Learn who must file Form 8938, what foreign assets to report, and how to av...

18. [Fbar Vs. Form 8938: What's...](https://www.expattaxonline.com/fincen-form-114/) - Report your UK pension as foreign income on your US tax return using Form 1040. Utilize Form 1116 fo...

19. [FBAR Filing Guide 2026: FinCEN Form 114 Requirements - SDO CPA](https://www.sdocpa.com/fbar-filing-guide/) - Complete FBAR filing guide for U.S. persons with foreign accounts. Learn the $10,000 threshold, Apri...

20. [Foreign Earned Income Exclusion Form 2555](https://support.taxslayer.com/hc/en-us/articles/360015702472-Foreign-Earned-Income-Exclusion-Form-2555) - If you are working and/or living abroad and meet certain requirements, you may be eligible to use th...

21. [Physical Presence Test: How to Qualify - 1040 Abroad](https://1040abroad.com/blog/using-feie-physical-presence-test-for-us-expats/) - Learn how the physical presence test helps U.S. expats qualify for the foreign earned income exclusi...

22. [Do Expats Pay US Self-Employment Tax on Foreign Earned Income?](https://brighttax.com/blog/expats-self-employment-tax-foreign-earned-income/) - Many American expats wonder whether they have to pay US self-employment tax on their foreign earned ...

23. [Taxes in Mexico: What US Expats Need to Know](https://brighttax.com/blog/taxes-in-mexico-for-us-expats/) - Mexico is home to the largest population of US expats in the world, so we've made this guide about e...

24. [Feie Qualifying Income...](https://www.expertsforexpats.com/advice/tax/foreign-tax-credits-vs-foreign-earned-income-exclusion) - If you are a US expat or are subject to US taxes but live abroad and earn income from outside the US...

25. [Form 8938 and FATCA Reporting - A Guide for Expats in 2025](https://www.onlinetaxman.com/form-8938-fatca-reporting-guide-expats-2026/) - Did you know that, as an expat, the Foreign Account Tax Compliance Act (FATCA) is just as important ...

26. [FBAR Filing Requirements: 2025 Guide - Gordon Law Group](https://gordonlaw.com/learn/fbar-filing/) - Confused about your FBAR filing requirements? Learn who needs to file FinCEN Form 114 and what to do...

27. [Ultimate Tax Guide for US Expats Living in Mexico](https://www.greenbacktaxservices.com/country-guide/taxes-in-mexico-us-expats/) - Discover tax tips for US expats in Mexico. Learn about filing requirements, deductions, and how to m...

