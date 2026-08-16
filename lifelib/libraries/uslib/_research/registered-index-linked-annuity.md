# Registered Index-Linked Annuity (RILA / buffered or structured annuity) — research notes (U.S.)

Access date for all citations: 2026-08-04.

Purpose: source library and extracted specifications to drive a reference liability
cash-flow projection model (lifelib/modelx style) for U.S. registered index-linked
annuities (RILAs, also called index-linked variable annuities / ILVAs, structured
annuities, or buffered annuities).

Citation discipline: every fact below is tagged with the source document it was
extracted from ([S#] primary product documents, [R#] regulatory/actuarial
references). Facts stated from general knowledge and not verified against a
retrieved document are tagged [unverified]. The S#/R# numbering here is local to
this product file and independent of the cross-product library numbering.

Modelling note up front: the single hardest component of a RILA cash-flow model is
the **Interim Value** (IV) — the daily fair value of an index-linked option between
term start and term end. Every major insurer builds it as
`IV = (fixed income asset proxy) + (derivative asset proxy)`, where the derivative
proxy is a small replicating portfolio of European options priced with
Black-Scholes. Sections "Interim value formulas" and "Variations across insurers"
below give the exact per-insurer algebra.

---

## Primary sources

### S1. Brighthouse Life Insurance Company of NY — "Brighthouse Shield Level Select 6-Year Annuity", Form S-3 registration statement
- Publisher: Brighthouse Life Insurance Company of NY ("BLNY"), CIK 0001167609
- Doc type: Securities Act registration statement / statutory prospectus (Form S-3,
  the pre-2024 RILA registration form). Filed 2019-02-06,
  accession 0001193125-19-030795.
- URL fetched: https://www.sec.gov/Archives/edgar/data/1167609/000119312519030795/d695141ds3.htm
- Retrieved: YES (full document downloaded and read; note sec.gov rejects generic
  fetchers with HTTP 403 — a declared User-Agent is required)
- Product: Brighthouse Shield Level Select 6-Year Annuity — "an individual single
  premium deferred index-linked separate account annuity contract". New York
  version only. Separate Account: Brighthouse Separate Account SA II.
- Why kept alongside S2: this filing documents the **older, pro-rata "accrued rate"
  interim value design**, which is materially simpler than the AG 54-era
  hypothetical-portfolio design in S2. Useful as a tractable first modelling
  target and as a historical contrast.

### S2. Brighthouse Life Insurance Company — "Brighthouse Shield Level II 6-Year Annuity", Rule 424(b)(3) prospectus
- Publisher: Brighthouse Life Insurance Company ("BLIC"), CIK 0000733076
- Doc type: statutory prospectus filed under Rule 424(b)(3), filed 2024-07-26,
  accession 0001193125-24-180915
- URL fetched: https://www.sec.gov/Archives/edgar/data/733076/000119312524180915/d747348d424b3.htm
- Retrieved: YES (full document downloaded and read)
- Product: Brighthouse Shield Level II 6-Year Annuity — individual single premium
  deferred index-linked separate account annuity contract.
- Why it matters: contains the **Appendix F "Interim Value of Shield Options"**
  with the complete Fixed Income Asset Proxy / Derivative Asset Proxy algebra and
  the per-crediting-type replicating option portfolios, plus fully worked numeric
  examples including the proportional Investment Amount reduction on withdrawal.

### S3. Pruco Life Insurance Company — "PRUDENTIAL FlexGuard — Flexible Premium Deferred Index-Linked and Variable Annuity ('B Series')", prospectus supplement
- Publisher: Pruco Life Insurance Company (Prudential)
- Doc type: prospectus supplement dated September 14, 2022 to the prospectus dated
  August 15, 2022, containing full amended-and-restated text of the index-strategy
  sections, the Interim Value discussion, and Appendix B (57 pages)
- URL fetched: https://www.prudential.com/content/dam/us/sites/pru-com/pru/opt2/annuities/annuity-prospectuses/S3-flex-guard-prosp-B-plaz.pdf
- Retrieved: YES (full PDF text extracted and read)
- Product: Prudential FlexGuard indexed variable annuity, B Series — a
  *combination* contract offering index strategies alongside variable investment
  subaccounts.
- Caveat: this is a 2022 supplement, not the current prospectus. Numbers below are
  as of that document. Do not treat as current pricing.

### S4. Equitable Financial Life Insurance Company — "Structured Capital Strategies PLUS 26", Form N-4 registration statement
- Publisher: Equitable Financial Life Insurance Company, CIK 0002039145
  (a parallel, essentially identical filing exists for Equitable Financial Life
  Insurance Company of America, CIK 0002038891)
- Doc type: Form N-4 registration statement (the post-2024 RILA form), filed
  2026-06-18, accession 0001193125-26-275133
- URL fetched: https://www.sec.gov/Archives/edgar/data/2039145/000119312526275133/d59590dn4.htm
- Retrieved: YES (full document downloaded and read)
- Product: Structured Capital Strategies PLUS (SCS PLUS 26) — index-linked annuity
  with a Structured Investment Option (SIO) of "Segments" plus a Guaranteed
  Interest Option (GIO). Non-unitized Separate Account No. 68 (NY) / 68A and 68E
  (AZ).
- Why it matters: the richest **segment-type menu** publicly documented (Standard,
  Annual Lock, Step Up, Dual Direction, Dual Step Up, Optimal Mix) with the exact
  Segment Rate of Return decision table for each, and the most detailed
  **Segment Interim Value** description including the Cap Calculation Factor and
  the implied-volatility interpolation procedure.

### S5. Allianz Life Insurance Company of North America / Allianz Life Variable Account B — "Allianz Index Advantage+ Select Income Annuity", Form N-4 initial registration statement
- Publisher: Allianz Life Insurance Company of North America (CIK 0000072499) /
  Allianz Life Variable Account B (CIK 0000836346)
- Doc type: Form N-4 initial registration statement, filed 2025-07-22,
  accession 0000836346-25-000047
- URL fetched: https://www.sec.gov/Archives/edgar/data/836346/000083634625000047/iaplusselectincomn4july2025.htm
- Retrieved: YES (full document downloaded and read)
- Product: Allianz Index Advantage+ Select Income Annuity.
- Why it matters: Allianz uses a structurally different presentation — a
  **"Daily Adjustment"** applied to an "Index Option Base" rather than a
  self-contained interim value — and offers both **buffer** and **floor**
  crediting methods side by side (Index Guard Strategy = -10% floor). Appendix C
  gives the Proxy Value formula for each of six crediting methods.
- Caveat: this is an *initial* N-4 filing; several fee-table cells are marked
  "[To be updated by amendment]" and the prospectus date is "[December XX, 2025]".
  Fee figures from this document are preliminary.

### S6. Lincoln Life & Annuity Company of New York — "Lincoln Level Advantage 2 B-Share Index-Linked Annuity", Form N-4/A
- Publisher: Lincoln Life & Annuity Company of New York, CIK 0001022095
- Doc type: Form N-4/A (pre-effective amendment), filed 2026-04-16,
  accession 0001104659-26-044336. Includes the SAI text with the Interim Value
  appendix and worked examples.
- URL fetched: https://www.sec.gov/Archives/edgar/data/1022095/000110465926044336/tm265270d1_n4a.htm
- Retrieved: YES (full document downloaded and read)
- Product: Lincoln Level Advantage 2 B-Share (and Advisory) Index-Linked Annuity
  Contracts.
- Why it matters: gives a **third algebraic form of the fixed income asset proxy**
  and a full grid of **worked Interim Value numeric examples** across index moves
  of -30%/-10%/+20%/+40% for 1-year and 6-year terms and for cap, trigger and
  dual-trigger accounts — ideal regression test vectors.

### Failed / blocked retrievals (do NOT treat as sources)
- Brighthouse "Understanding Interim Value" educational PDF —
  https://www.brighthousefinancial.com/content/dam/brighthouse-financial/public/pdfs/shield/Shield-Interim-Value-Educational-Resource.pdf
  — HTTP 403. fetched_ok = false.
- Brighthouse Shield current rate page —
  https://www.brighthousefinancial.com/products/annuities/shield-annuities/shield-rates/
  — HTTP 403. fetched_ok = false. No current declared cap/step/edge rates captured.
- Equitable performance cap rate page —
  https://equitable.com/annuities/variable-annuities/performance-cap-rates
  — request rejected by WAF. fetched_ok = false.
- Federal Register HTML of the RILA adopting release — redirects off-host to
  unblock.federalregister.gov. fetched_ok = false; the SEC PDF (R1) was used
  instead and is authoritative.

---

## Regulatory and actuarial references

### R1. U.S. Securities and Exchange Commission — Final rule, "Registration for Index-Linked Annuities and Registered Market Value Adjustment Annuities; Amendments to Form N-4 for Index-Linked Annuities, Registered Market Value Adjustment Annuities, and Variable Annuities; Other Technical Amendments"
- Publisher: SEC
- Release Nos. 33-11294; 34-100450; IC-35273; File No. S7-16-23; RIN 3235-AN30.
  17 CFR Parts 230, 232, 239, 274. 467 pages (conformed to Federal Register version).
- URL fetched: https://www.sec.gov/files/rules/final/2024/33-11294.pdf
- Retrieved: YES (full PDF; introduction and effective/compliance-date sections read
  in detail)

### R2. NAIC — Actuarial Guideline LIV, "Nonforfeiture Requirements for Index-Linked Variable Annuity Products" (AG 54)
- Publisher: National Association of Insurance Commissioners
- Doc type: adopted actuarial guideline plus project history (6 pages)
- URL fetched: https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-liv-230224.pdf
- Retrieved: YES (full text read)
- Adoption trail printed on the document: adopted by Life Actuarial (A) Task Force
  12/11/2022; adopted by Life Insurance and Annuities (A) Committee 2/24/2023.
- **Verified**: the guideline covering index-linked variable annuity nonforfeiture
  and interim values exists, is numbered **Actuarial Guideline LIV / AG 54**, and
  applies to all contracts (including riders, endorsements, amendments) issued on
  or after **July 1, 2024**.

### R3. NAIC — Valuation Manual, Jan. 1, 2026 edition, VM-21 "Requirements for Principle-Based Reserves for Variable Annuities"
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457 pages; VM-21 Sections 1 and 2 read in detail)

### R4. NAIC — Model #250, "Variable Annuity Model Regulation"
- Publisher: NAIC (October 2007 edition of the NAIC Model Laws compilation)
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: YES (13 pages; Sections 2, 3 and 7 read)

### R5. Actuarial Standards Board — ASOP No. 2, "Nonguaranteed Elements for Life Insurance and Annuity Products" (Doc. No. 204)
- Publisher: Actuarial Standards Board
- URL fetched: http://www.actuarialstandardsboard.org/wp-content/uploads/2021/12/asop002_204-2.pdf
- Retrieved: YES (33 pages; Sections 1 and 2 read)
- Note: the title has changed from the older "Nonguaranteed Charges or Benefits for
  Life Insurance Policies and Annuity Contracts" to "Nonguaranteed Elements for
  Life Insurance and Annuity Products".

### R6. American Academy of Actuaries — "Index-Linked Variable Annuity (ILVA) / Registered Index-Linked Annuity (RILA)" policy paper
- Publisher: American Academy of Actuaries, Life Practice Council
- Doc type: policy paper, 26 pages, dated December 2025 (file name Life-PolicyPaper120225.pdf)
- URL fetched: https://actuary.org/wp-content/uploads/2025/12/Life-PolicyPaper120225.pdf
- Retrieved: YES (full PDF text extracted and read)
- Why it matters: contains a **fully worked numeric hypothetical-portfolio interim
  value example** (6-year, 10% buffer, Black-Scholes inputs given) plus a survey of
  common ILVA product features and an open-source Excel Lambda library reproducing
  the AG 54 calculation.

---

## Extracted specifications

### 1. Product architecture and terminology

The same object goes by different names per insurer. Map for modelling:

| Concept | S1/S2 Brighthouse | S3 Prudential | S4 Equitable | S5 Allianz | S6 Lincoln |
|---|---|---|---|---|---|
| index-linked bucket | Shield Option | Index Strategy | Segment | Index Option | Indexed Segment |
| notional that index return applies to | Investment Amount | Index Strategy Base | Segment Investment | Index Option Base | Indexed Crediting Base |
| downside protection | Shield Rate | Buffer | Segment Buffer | Buffer / Floor | Protection Level / Dual Rate |
| upside limit | Cap Rate / Step Rate / Edge Rate | Cap Rate / Step Rate / Participation Rate / Tier | Performance Cap Rate / Participation Rate | Cap / Trigger Rate / Participation Rate | Performance Cap / Performance Trigger Rate / Dual Performance Trigger Rate / Dual Rate |
| daily fair value | Interim Value | Interim Value | Segment Interim Value | Daily Adjustment (applied to Index Option Base) | Interim Value |
| return credited at term end | Performance Rate | Index Credit | Segment Rate of Return | Performance Credit | Performance Rate |

Sources: [S1][S2][S3][S4][S5][S6].

AG 54 supplies the regulator-side vocabulary that the Brighthouse and Lincoln
prospectuses adopt verbatim: **Index Strategy Base**, **Index Strategy Term**,
**Interim Value**, **Strategy Value**, **Hypothetical Portfolio**, **Fixed Income
Asset Proxy**, **Derivative Asset Proxy**, **Trading Cost** [R2].

Separate-account structure: RILA index-linked options are held in a **non-unitized**
separate account [S4][R2]. Per the Academy survey, of ILVA separate accounts: none
are registered with the SEC, all are non-unitized, and they may be insulated or
non-insulated [R6]. Statutory accounting treatment is separate account; U.S. GAAP
treatment is general account; RBC splits C0–C1 general account, C3–C4 separate
account [R6].

### 2. Issue ages, premiums, contract limits

| Item | Value | Source |
|---|---|---|
| Owner and Annuitant issue ages | 0–85 | [S1][S2] |
| Minimum Purchase Payment | $25,000; prior approval required below $25,000 or at/above $1,000,000 | [S1][S2] |
| Minimum Account Value | $2,000 (below this, a withdrawal request is treated as a full withdrawal) | [S1][S2] |
| Minimum Allocation to a Shield Option | $500 | [S1] |
| Minimum Partial Withdrawal | $500 | [S1] |
| Maturity Date (forced annuitization) | Contract anniversary after the oldest Owner's 90th birthday, or 10 years from issue, whichever is later | [S2] (S1: first day of month following Annuitant's 90th birthday or 10 years, whichever later) |
| Maximum age for initial purchase | 85 (oldest Owner; Key Life for a Beneficiary Annuity) | [S3] |
| Minimum initial Purchase Payment | $25,000 | [S3] |
| Minimum initial contribution | $25,000, all contract types | [S4] |
| Issue ages by contract type | NQ 0–85; Traditional IRA 0–85; Roth IRA 0–85; SEP IRA 20–85 | [S4] |
| Minimum additional contribution | $500 (NQ, SEP); $50 (traditional IRA, Roth IRA) | [S4] |
| Contribution cut-off age | No additional contributions after the Owner reaches age 86, or the first contract anniversary if later | [S4] |
| Aggregate contribution limits | $2,500,000 across SCS contracts with same owner/annuitant; $5,000,000 across all Equitable annuity accumulation contracts | [S4] |
| Minimum allocation to an Indexed Account | $2,000; reallocation only on an Indexed Anniversary Date | [S6] |
| Free Look | 10 days after receipt (longer in some states) | [S1][S2] |

### 3. Crediting strategy menus

**Brighthouse Shield Level Select (S1)** — Terms 1, 3 or 6 years. Shield Rates:
Shield 10, Shield 15, Shield 25. Indices: S&P 500 (price return), Russell 2000
(price return), MSCI EAFE (price return). Rate Crediting Type: Cap Rate or Step
Rate (Step Rate offered on 1-Year Terms) [S1].

**Brighthouse Shield Level II (S2)** — Terms **1, 2, 3 or 6** years. Shield Rates:
Shield 10, Shield 15, Shield 25. Indices: S&P 500, Russell 2000, MSCI EAFE,
**Nasdaq-100** (all price return). Rate Crediting Types: **Cap Rate, Step Rate, or
Step Rate Edge** [S2].

**Prudential FlexGuard (S3)** — Three index strategies: Point-to-Point with Cap,
Tiered Participation Rate, Step Rate Plus. Terms 1, 3, 6 years. Indices: S&P 500,
MSCI EAFE, Invesco QQQ ETF, iShares Russell 2000 ETF, AB 500 Plus Index. Buffers
offered: **5%, 10%, 15%, 20%, and 100%** — the 100% buffer is a full-protection
option [S3]. Pennsylvania excludes the 5%-buffer Step Rate Plus and Tiered
Participation Rate strategies [S3].

**Equitable SCS PLUS 26 (S4)** — Segment Options: **Standard, Annual Lock, Step Up,
Dual Direction, Dual Step Up, Optimal Mix**. Segment Buffers range from the first
**10% to 40%** of loss. Indices in the current appendix: S&P 500 Price Return,
Russell 2000 Price Return, MSCI EAFE Price Return, NASDAQ-100 Price Return; Optimal
Mix segments blend 3 (U.S.) or 4 (Global) component indices. Segment Durations 1, 3
and 6 years [S4]. Segments start weekly: "There is generally a Segment Transaction
Date every Thursday" [S4].

Current Segment Type grid from the S4 appendix "Investment Options available under
the contract" (Segment Buffer / minimum Performance Cap Rate for the life of the
segment / Participation Rate):

| Calculation method | Durations | Segment Buffers offered | Minimum Performance Cap Rate (6yr / 3yr / 1yr) | Participation Rate |
|---|---|---|---|---|
| Standard | 6, 3, 1 yr | -10%, -15%, -20%, -40% | 12% / 6% / 2% | 100% |
| Step Up | 6, 1 yr | -10% (6yr); -10%, -15% (1yr) | 12% / — / 2% | 100% |
| Dual Direction | 6, 3, 1 yr | -10%, -15%, -20% | 12% / 6% / 2% | 100% |
| Dual Step Up | 1 yr | -10%, -15% | — / — / 2% | 100% |
| Annual Lock | 6 yr | -10% | 2% | 100% |

Source: [S4]. Equitable commits that "we will always offer a Segment Option with a
Segment Buffer that protects the first 10% of loss" [S4].

**Allianz Index Advantage+ Select Income (S5)** — Six crediting methods:
Index Performance Strategy, Index Guard Strategy, Index Dual Precision Strategy,
Index Precision Strategy, Index Protection Strategy with Trigger, Index Protection
Strategy with Cap. Buffers of **10%, 20%, or 30%**; Index Guard Strategy uses a
**-10% Floor**. Terms of 1, 3 and 6 years [S5].

**Lincoln Level Advantage 2 (S6)** — Indexed Accounts on **1-Year or 6-Year** terms.
Four upside mechanics: (i) Performance Cap, (ii) Performance Trigger Rate,
(iii) Dual Performance Trigger Rate, (iv) Dual Rate (with a Performance Cap above
it). Protection Levels of 10%, 15%, 20%, 25%; Dual Rates of 10%, 15%. Annual Lock
6-year accounts and "Dual Plus" accounts are also offered. Secure Lock+ performance
lock feature [S6].

### 4. Term-end crediting formulas (exact)

Notation used below: `IPR` = index performance rate over the term
(`= Index(T)/Index(0) - 1`); `B` = buffer / shield rate (positive number, e.g. 0.10);
`C` = cap rate; `PR` = participation rate; `SR` = step / trigger / edge rate;
`F` = floor (positive number).

**Buffer + Cap (the canonical design)** — Brighthouse Shield Options with a Cap Rate
[S1][S2]:
```
if IPR <= 0:  PerformanceRate = min(0, IPR + B)
elif 0 < IPR < C: PerformanceRate = IPR
else (IPR >= C): PerformanceRate = C
```
S1 states this verbatim as "the lesser of: zero or the Index Performance increased
by the Shield Rate", with worked example: -15% index performance with Shield 10 ->
-5% Performance Rate; and "The Performance Rate can never be greater than zero if
the Index Performance is negative" [S1].

**Buffer + Step Rate (trigger / step-up)** — Brighthouse Shield Options with a Step
Rate [S1][S2]:
```
if IPR < 0:  PerformanceRate = min(0, IPR + B)
else (IPR >= 0): PerformanceRate = SR
```
[S1] worked contrast: with a 10% Cap and 15% index performance the Performance Rate
is 10%; with an 8% Step Rate it is 8%. With 0% index performance the Cap design
gives 0% and the Step design gives 8% [S1].

**Buffer + Edge Rate (Step Rate Edge)** — Brighthouse Shield Level II: "The rate
credited at the Term End Date if the Index Performance is equal to or greater than
the Shield Rate" — i.e. the trigger threshold is `-B`, not zero [S2]. Equivalent to
Equitable's Dual Step Up [S4] and Allianz's Index Dual Precision Strategy [S5].

**Investment Amount roll-forward at term end** [S1][S2]:
```
PerformanceRateAdjustment = InvestmentAmount(term start, adjusted for withdrawals)
                            x PerformanceRate
InvestmentAmount(term end) = InvestmentAmount(term start, adj) + PerformanceRateAdjustment
```
Worked in [S1]: $50,000 + $4,000 = $54,000.

**Prudential FlexGuard index credits** [S3]:
- *Point-to-Point with Cap*: if `IPR >= C` credit `C`; if `0 < IPR < C` credit `IPR`;
  if `IPR` negative but `|IPR| <= B` credit 0; otherwise credit `IPR + B`
  (the negative index return in excess of the buffer).
- *Tiered Participation Rate*: if `0 <= IPR < TierLevel`, credit `IPR x PR1`. If
  `IPR >= TierLevel`, credit `TierLevel x PR1 + (IPR - TierLevel) x PR2`. Downside
  identical to the above.
- *Step Rate Plus*: if `0 <= IPR <= SR`, credit `SR`. If `IPR > SR`, credit
  `max(IPR x PR, SR)`. Downside identical.
  Example parameters used in the S3 illustration: 1-Year Step Rate Plus, S&P 500,
  Step Rate 5%, Participation Rate 90%, Buffer 5%; 3-Year Point-to-Point Cap Rate
  75%, Buffer 10%; 6-Year Tiered Participation Rate Tier 1 100%, Tier 2 140%, Tier
  Level 30%, Buffer 10% [S3].

**Equitable Segment Rate of Return by segment type** [S4]:
- *Standard*: if `IPR x PR > Cap` -> `Cap`; if `0 < IPR x PR <= Cap` -> `IPR x PR`;
  if flat or negative within the buffer -> `0%`; if negative beyond the buffer ->
  negative, equal to the excess over the buffer.
- *Step Up*: if `IPR x PR >= 0` -> `Cap` (the cap doubles as the step rate);
  negative within buffer -> `0%`; beyond buffer -> excess.
  Discontinuity flagged in the document: with an 8.00% cap, `IPR = 0.00%` gives
  8.00% but `IPR = -0.01%` gives 0.00% [S4].
- *Dual Direction*: if `IPR x PR > Cap` -> `Cap`; if `0 < IPR x PR <= Cap` ->
  `IPR x PR`; **if negative within the buffer -> `|IPR|` (a positive credit equal to
  the absolute value of the index loss)**; if beyond the buffer -> excess.
  The Participation Rate applies only to positive index performance; it is not
  applied to the absolute value branch [S4]. Discontinuity: with a -20% buffer,
  `IPR = -20.00%` gives +20.00% but `IPR = -20.01%` gives -0.01% [S4].
- *Dual Step Up*: if `IPR > 0` -> `Cap`; if `-B <= IPR <= 0` -> `Cap`; if beyond the
  buffer -> excess. (i.e. the cap is paid for any return down to and including the
  buffer.)
- *Annual Lock*: the Segment Rate of Return is the **cumulative compounding** of
  each Annual Lock Yearly Rate of Return, each computed as the Standard rule applied
  to that one-year period, with the ending amount for one lock period becoming the
  starting amount of the next. Intra-period index fluctuation is ignored. The Annual
  Lock Anniversary amounts "are not credited to the contract, are not the Segment
  Interim Value, and cannot be received upon surrender or withdrawal" [S4].
- *Optimal Mix*: Standard rule applied to a cumulative weighted average of 3 (U.S.)
  or 4 (Global) component indices [S4].

**Allianz Performance Credits** [S5]: Trigger Rate paid on a Term End Date if the
current Index Value is >= the Index Value on the Term Start Date (Index Protection
with Trigger, Index Precision, Index Dual Precision). For Index Dual Precision the
Trigger Rate is *also* paid when the index return is negative but the loss is within
the buffer. The Cap and Participation Rate apply "for the entire Term length; we do
not apply the Cap and any Participation Rate annually on a 3-year or 6-year Term
Index Option" [S5]. Index Protection Strategy with Trigger and with Cap cannot
produce a negative Performance Credit [S5].

**Lincoln crediting mechanics** [S6]: Dual Performance Trigger Rate "will either
provide a specific rate of return if the performance of the Index is positive, zero
or negative within the Protection Level or be added to the Index performance
percentage and the Protection Level if the Index performance is negative and beyond
the Protection Level". Dual Rate "will provide either a minimum rate of return if
the Index performance is between zero and the Dual Rate, or will be added to the
Index performance if the Index performance is negative, and a Performance Cap that
applies if the Index performance exceeds the Dual Rate" [S6].

### 5. INTERIM VALUE FORMULAS (the critical modelling component)

#### 5a. Regulatory template — AG 54 hypothetical portfolio [R2]

AG 54 defines the target that all the prospectus formulas below are calibrated to:

- `Hypothetical Portfolio = Fixed Income Asset Proxy + Derivative Asset Proxy` [R2].
- **Index Strategy Base must equal Strategy Value at the Index Strategy Term start
  date** [R2].
- The **Fixed Income Asset Proxy** is "a hypothetical fixed income asset with a yield
  that results in (i) At the beginning of the Index Strategy Term, the book value of
  the Fixed Income Asset Proxy equal to the Index Strategy Base less the Derivative
  Asset Proxy value; and (ii) At the end of the Index Strategy Term, the book value
  of the Fixed Income Asset Proxy, assuming no change in yield, projected to equal
  the Index Strategy Base" [R2]. In other words, the fixed leg is a zero-coupon
  accretion from `(Base - option budget)` up to `Base` over the term, which
  amortises the option budget. Academy restates this as "a hypothetical zero-coupon
  bond" whose yield "allows for the recovery of the 'unearned' option budget
  initially spent to fund option(s) over the Index Strategy Term" [R6].
- The **Derivative Asset Proxy** is "a package of hypothetical derivative assets
  established at the beginning of an Index Strategy Term that is designed to
  replicate credits provided by an Index Strategy at the end of an Index Strategy
  Term" [R2].
- "Interim Values must be materially consistent with the value of the Hypothetical
  Portfolio over the Index Strategy Term **less a provision for the cost
  attributable to reasonably expected or actual Trading Costs** at the time the
  Interim Value is calculated" [R2].
- Market value of the fixed leg "may be determined by a fair value methodology or by
  applying an MVA to the book value" — states decide whether including or excluding
  an MVA is appropriate [R2, drafting note]. This is precisely why insurers differ
  on the MVA term (section 5b–5f below).
- Certification requirements: assumptions (implied volatilities, risk-free rates,
  dividend yields) must be "consistent with the observable market prices of
  derivative assets over the Index Strategy Term, whenever possible", with
  acceptable techniques listed as "the standard Black-Scholes method, Monte-Carlo
  Simulation techniques, and other market consistent option valuation techniques for
  more complex options" [R2].
- Alternative (non-hypothetical-portfolio) methods are permitted only with a
  demonstration of material consistency "for each combination of Index Strategy and
  Index Strategy Term under a reasonable number of realistic economic scenarios that
  include index changes that test crediting constraints and recognize initial option
  pricing market conditions" [R2].
- The Interstate Compact standard (IIPRC-03-I-ILVA) is **narrower**: it "requires the
  use of the Hypothetical Portfolio methodology and does not allow for materially
  consistent approaches" [R6]. Academy also reports the demonstration scenario set
  used: volatility assumptions of 20% and 25%, and index strategy term performance
  from -30% to +30% in 5% increments [R6].

#### 5b. Brighthouse Shield Level II — Appendix F (verbatim structure) [S2]

```
InterimValue(ShieldOption) = (1) + (2)

(1) market value of the Fixed Income Asset Proxy
    = (A - B) x [ (1 + C) / (1 + D) ] ^ E
      A = Investment Amount on the Business Day the Interim Value is calculated
      B = market value of the Derivative Asset Proxy under INITIAL market
          conditions, with straight-line amortization to the end of the Term
      C = Market Value Rate on the Term Start Date
      D = Market Value Rate on the Business Day the Interim Value is calculated
      E = total days remaining in the Term divided by 365

(2) current market value of the Derivative Asset Proxy
```
- **Market Value Rate** = "the Constant Maturity Treasury (CMT) rate with a maturity
  equal to that of the Term"; linearly interpolated between the two closest CMT
  maturities if an exact match is unavailable [S2].
- The `[(1+C)/(1+D)]^E` factor is explicitly described as applying "a Market Value
  Adjustment to address any changes in interest rates from the Term Start Date to
  the day the Interim Value is calculated" [S2].
- Derivative Asset Proxy is valued with the **Black-Scholes Model**, and "reflects
  the impact of the Cap Rate, Step Rate, Edge Rate, and Shield Rate at the end of the
  Term as well as the estimated cost of exiting the replicating options prior to the
  Term End Date" [S2].

Replicating portfolios by crediting type [S2]:
```
Cap Rate option:         ATMC - OTMC - OTMP
Step Rate option:        (Step Rate x ATMBC) - OTMP
Step Rate Edge option:   (Edge Rate x ITMBC) - OTMP
```
where ATMC = at-the-money call, OTMC = out-of-the-money call, OTMP =
out-of-the-money put, ATMBC = at-the-money binary call, ITMBC = in-the-money binary
call. "For purposes of the Interim Value formula, the value of the out-of-the-money
call will be zero if a Cap Rate Shield Option is uncapped" [S2].

Key economic warnings stated in the document, all of which a model must reproduce:
"the out-of-the-money put will almost always reduce the Interim Value, even when the
current Index Value on a Business Day is higher than the Index Value on the Term
Start Date"; and "you could have negative Interim Value, even if the Index Value has
increased at the time of the calculation" [S2].

Worked numeric example from [S2] (Shield Option, index 500 -> 600, i.e. +20% index
performance, 6 months remaining, Market Value Rate 3% on the calculation date):
```
Market value of Fixed Income Asset Proxy   $49,452.40
Market value of Derivative Asset Proxy      $4,062.37
Interim Value                              $53,514.77
```

**Withdrawal mechanics — proportional reduction of the notional** [S2]:
```
InvestmentAmount_after = InvestmentAmount_before
                         x (1 - GrossWithdrawal / InterimValue_at_withdrawal)
```
Worked: `$50,000 x (1 - $20,000 / $53,514.77) = $31,313.57` [S2]. The reduced
Investment Amount then serves as the new term-start Investment Amount for the
remainder of the term. Note the asymmetry the prospectus calls out: "a withdrawal
when Interim Value is less than the Investment Amount will cause a greater
percentage reduction in the Investment Amount that remains in your Shield Option
relative to the percentage reduction for the same withdrawal amount when Interim
Value is greater than the Investment Amount" [S2].

#### 5c. Brighthouse Shield Level Select — the older pro-rata accrual design [S1]

No option pricing at all. Interim Value = Investment Amount adjusted by a
Performance Rate computed with **time-prorated** rates:
```
AccruedShieldRate = ShieldRate x (days elapsed since Term Start) / (total days in Term)
AccruedCapRate    = CapRate    x (days elapsed) / (total days)
AccruedStepRate   = StepRate   x (days elapsed) / (total days)
   with 365 days assumed in each calendar year of a Term
```
Then the term-end Performance Rate rules are applied with the accrued rates
substituted for the full rates. Worked example [S1]: $50,000, Shield 10, 10% Cap,
1-Year Term, index 500 -> 600 at day 183:
```
IndexPerformance = (600 - 500) / 500 = 20%
AccruedCapRate   = 10% x 183/365 = 5%
PerformanceRate  = 5%  (capped by the accrued cap)
PerformanceRateAdjustment = $50,000 x 5% = $2,500
InterimValue = $50,000 + $2,500 = $52,500
```
Also documented: Accrued Shield Rate 10% x 183/365 = 5%; Accrued Step Rate
8% x 183/365 = 4% [S1]. Consequence noted in the document: "If negative Index
Performance is constant during the Term, the Interim Value will be lower the earlier
a withdrawal is made during the Term because the Shield Rate is accruing" [S1].

This design predates AG 54's July 1, 2024 effective date [R2] and would not satisfy
the Hypothetical Portfolio requirement without a material-consistency demonstration.

#### 5d. Prudential FlexGuard — Appendix B [S3]

```
InterimValue(IndexStrategy) = (1) + (2)

(1) fair value of the Index Strategy Base
    = (A - B) x [ (1 + C) / (1 + D) ] ^ E
      A = Index Strategy Base on the Valuation Day
      B = fair value of the replicating portfolio of options under INITIAL market
          conditions, WITH UPDATED TIME TO EXPIRY
      C = Market Value Index Rate on the Index Strategy Start Date
      D = Market Value Index Rate on the Valuation Day
      E = total days remaining in the Index Strategy Term / 365

(2) fair value of the replicating portfolio of options
```
**Pennsylvania variant**: term B is instead "the fair value of the replicating
portfolio of options under initial market conditions, **with straight-line
amortization to the end of the Index Strategy Term**" [S3] — i.e. the same
convention Brighthouse uses nationally [S2]. So a model needs both amortisation
conventions as a switch.

**Market Value Index Rate** = "the Bloomberg Barclays U.S. Intermediate Credit Index
rate ... the rate for the maturity using a set duration. The duration is set to
represent the duration of the investments supporting the Index Strategy and may not
match the actual length of the Index Strategy" [S3]. Note this is a *credit* index,
not Treasury — contrast Brighthouse's CMT [S2].

Replicating portfolios [S3]:
```
Cap Rate strategy:                AMC - OMC - OMP
Step Rate Plus strategy:          (Step Rate x BC) + (Participation Rate x OMC) - OMP
Tiered Participation Rate:        AMC + [(2nd Tier PR - 1st Tier PR) x OMC] - OMP
```
where AMC = at-the-money call, OMC = out-of-the-money call, OMP =
out-of-the-money put, BC = binary call "(inclusive of the bull spread)" [S3].

Worked example from [S3] (Index Effective Date 12/2/2019, $150,000 across three
strategies, 9 months elapsed; months assumed 30 days, years 365 days):

| | Step Rate Plus 1yr | PTP Cap 3yr | Tiered Part 6yr |
|---|---|---|---|
| Index Strategy Base | $49,500 | $49,500 | $51,000 |
| Buffer | 5% | 10% | 10% |
| Strategy rate | Step 5% | Cap 75% | Tiers 100%/140%, Tier Level 30% |
| Market Index Rate at start | 2.00% | 5.00% | 8.00% |
| Market Index Rate at valuation | 3.00% | 6.00% | 9.00% |
| **Index return -20%** — fair value of base | $48,496.25 | $46,847.82 | $45,813.71 |
| — options value | $(7,401.540) | $(6,166.880) | $(5,753.380) |
| — Interim Value | $41,094.71 | $40,680.95 | $40,060.33 |
| **Index return +20%** — options value | $8,887.29 | $10,009.66 | $13,519.43 |
| — Interim Value | $57,383.54 | $56,857.49 | $59,333.14 |

Source: [S3]. Note the fixed-leg fair value is identical in the up and down
scenarios, confirming it is index-independent.

Withdrawal mechanics [S3]: "Any time a partial withdrawal occurs between Index
Strategy Start and End Dates, the Index Strategy Base will be reduced in the same
proportion that the total withdrawal reduced the Interim Value." Worked:
```
Base $50,000; Interim Value $70,000; gross withdrawal $50,000
ratio = 50,000 / 70,000 = 71.429%
Base adjustment = $50,000 x 71.429% = $35,714.29
Base after withdrawal = $50,000 - $35,714.29 = $14,285.71
```
and a second example where a $14,000 withdrawal against a $14,000 Interim Value
zeroes a $14,285.71 base [S3].

#### 5e. Equitable Segment Interim Value — three components [S4]

```
SegmentInterimValue = (1) Fair Value of hypothetical Fixed Instruments
                    + (2) Fair Value of hypothetical Derivatives
                    + (3) Cap Calculation Factor
```

**(1) Fixed instruments** — "defined as its present value, as expressed in the
following formula: `(Segment Investment)/(1 + rate)^(time to maturity)`" [S4]. The
rate is an *investment rate* on investment-grade fixed income, described as the
risk-free rate plus "the spread over risk-free rates for selected investment grade
index maturity points". Equitable notes the choice of investment rates over swap
rates "will result in a lower value for that component" [S4]. Time to maturity is
"a fraction, in which the numerator is the number of days remaining in the Segment
Duration and the denominator is the average number of days in each year of the
Segment Duration for that Segment" [S4].

Note the structural difference from S2/S3: Equitable discounts the **full** Segment
Investment (no subtraction of an initial option budget), then adds a separate,
always-positive Cap Calculation Factor.

**(2) Hypothetical derivatives** — the option inventory [S4]:
```
(A) At-the-Money Call        strike = index at segment inception
(B) Out-of-the-Money Call    strike = index increased by the Performance Cap Rate
                              (or, for Participation Rates > 100%,
                               index increased by Cap Rate / Participation Rate)
(C) Out-of-the-Money Put     strike = index decreased by the Segment Buffer
(D) At-the-Money Binary Call strike = index at segment inception
(E) At-the-Money Put         strike = index at segment inception
(F) Out-of-the-Money Binary Put  strike = index at inception minus Segment Buffer
(G) In-the-Money Binary Call strike = index decreased by the Segment Buffer
(H) At-the-Money Rainbow Call    strike = relative component indices at inception
(I) Out-of-the-Money Rainbow Call strike = relative component indices increased by Cap
(J) Out-of-the-Money Rainbow Put  strike = relative component indices decreased by Buffer
```
Combinations by segment type [S4]:
```
Standard        : (A) - (B) - (C)
Step Up         : (D) - (C)
Dual Direction  : (A) - (B) + (E) - (C) - (F)      [uses TWO instances of (C)]
Dual Step Up    : (G) - (C)
Optimal Mix     : (H) - (I) - (J)
Annual Lock     : a single "extended exotic option that periodically settles and
                  resets in strike price on the Index"
```
Pricing model: "a market standard model for valuing a European option on the Index,
assuming a continuous dividend yield or net convenience value, with inputs that are
consistent with market prices that reflect the estimated cost of exiting the
hypothetical Derivatives prior to Segment maturity" [S4]. Each hypothetical option
has notional on the Segment Start Date equal to the Segment Investment [S4].

**Implied volatility input procedure (verbatim structure)** [S4]: daily implied
volatility quotes are obtained from third parties for options with the closest
maturities above and below the actual remaining time and, for each maturity, the
closest moneyness values above and below the actual moneyness. Then:
(a) interpolate to the same moneyness at the nearest shorter maturity;
(b) interpolate to the same moneyness at the nearest longer maturity;
(c) linearly interpolate between (a) and (b) for the segment's remaining time.
Other inputs: swap rates (linear interpolation across adjacent maturities) and a
projected annual index dividend yield [S4].

**(3) Cap Calculation Factor** — "a return of estimated expenses for the portion of
the Segment Duration that has not elapsed ... always positive and declines during
the course of the Segment" [S4]. Worked example: "if the estimated expenses for a
one-year Segment are calculated by us to be $10, then at the end of 146 days (with
219 days remaining in the Segment), the Cap Calculation Factor would be $6, because
$10 x 219/365 = $6" [S4].

Transactions that trigger the Segment Interim Value ("Segment Interim Value
Transactions"): withdrawal (including systematic withdrawals and RMDs); transfer to
a different investment option; deduction of account value to pay fees; surrender or
annuitization; payment of a death claim; free-look cancellation [S4]. Note that the
optional death benefit charge, if deducted mid-segment, comes out of the Segment
Interim Value [S4].

#### 5f. Allianz Daily Adjustment — a delta rather than a level [S5]

Allianz does not publish an "Interim Value"; it publishes an adjustment applied to
the Index Option Base:
```
Daily Adjustment = [ (a) change in Proxy Value + (b) proxy interest ] x Index Option Base

(a) change in Proxy Value = current Proxy Value - beginning Proxy Value
(b) proxy interest        = beginning Proxy Value x (1 - time remaining during the Term)
      time remaining = days remaining in Term / Term length
      Term length    = days from Term Start Date to Term End Date
```
Proxy Values are expressed per unit of base [S5]. The proxy interest term is
"approximated by the value of amortizing the cost of the Proxy Investment over the
Term to zero" [S5] — economically the same option-budget amortisation that appears
as term B in [S2] and [S3], but here added rather than subtracted. Note there is
**no interest-rate MVA factor** in the Allianz formula.

Proxy Value formulas by crediting method [S5]:
```
Index Performance Strategy      : (ATM call) - (OTM call) - (OTM put)
Index Guard Strategy (FLOOR)    : (ATM call) - (OTM call) - (ATM put) + (OTM put)
Index Dual Precision Strategy   : [Trigger Rate x (ITM binary call)] - (OTM put)
Index Precision Strategy        : [Trigger Rate x (ATM binary call)] - (OTM put)
Index Protection w/ Trigger     : Trigger Rate x (ATM binary call)
Index Protection w/ Cap         : (ATM call) - (OTM call)
```
The Index Guard (floor) construction is the notable one: buy the ATM call spread,
sell an ATM put, and buy back an OTM put so the short put exposure stops at the
floor. Allianz states: "the out-of-the-money put will almost always reduce, and
never exceed, the negative impact of the at-the-money put for the Index Guard
Strategy" [S5]. For the Index Dual Precision Strategy the binary call is
in-the-money because it pays if the index ratio is >= "90% for a 10% Buffer, 80% for
a 20% Buffer, or 70% for a 30% Buffer" [S5].

Maximum losses from a negative Daily Adjustment, as disclosed [S5]:
**-99%** for Index Dual Precision, Index Precision and Index Performance strategies;
**-35%** for Index Guard; the Index Protection strategies (with Trigger and with
Cap) cannot have a negative Daily Adjustment. The Daily Adjustment is "generally
negatively affected by: interest rate decreases, dividend rate increases, poor
market performance, and the expected volatility of Index prices" — with the sign of
the volatility sensitivity differing by strategy: increases in expected volatility
hurt Dual Precision / Precision / 1-year Performance strategies, while *decreases*
in expected volatility hurt Index Guard [S5].

#### 5g. Lincoln Interim Value [S6]

```
InterimValue(Segment) = (1) + (2)

(1) Fixed Income Asset Proxy = C x [ 1 / (1+E)^D  x  (1+E)^D / (1+F)^D ]
      C = Crediting Base of the Segment on the Valuation Date
      D = total calendar days remaining in the Indexed Term / 365
      E = Discount Rate applying to the Segment on its Start Date
          (or the Reset Date if Secure Lock+ was exercised)
      F = Discount Rate applying to the Segment on the Valuation Date

(2) market value of the Derivative Asset Proxy, determined solely by us
```
Written this way the fixed leg is presented as an accretion-to-book factor
`1/(1+E)^D` multiplied by an MVA factor `(1+E)^D/(1+F)^D`; algebraically it
collapses to `C / (1+F)^D`. For **Annual Lock** segments the definition of C changes:
"the initial Crediting Base of the Segment that has been proportionately adjusted for
any withdrawals, surrender charges, premium taxes, or rider fees and charges that
have occurred during the Indexed Term prior to the Valuation Date" [S6].

**Discount Rate** = "derived from the Reference Rate, which is the sum of a U.S.
Constant Maturity Treasury (CMT) yield plus a market observable spread of investment
grade U.S. corporate bonds", with linear interpolation of CMT yields across
maturities [S6]. Lincoln reserves "the right to change the methodology of the Interim
Value calculation at any time and at our sole discretion" [S6].

Option inventory [S6]:
```
A. At-the-money call    E. At-the-money put
B. Out-of-the-money call (strike at the Performance Cap)
C. Out-of-the-money put  (strike at the Protection Level)
D. Digital option        (pays the Performance Trigger Rate under zero/positive returns)
F. "Dual structure"      (pays the Dual Performance Trigger Rate or Dual Rate at term
                          end independent of the underlying index return)
```
Combinations [S6]:
```
Cap + Protection Level                       : A - B - C
Performance Trigger Rate + Protection Level  : D - C
Dual Performance Trigger + Protection Level  : F - C
Dual Plus Segment                            : F + B(at Dual Rate) - B(at Performance Cap) - E
Annual Lock                                  : a replicating structure tied to the compounded
                                               yearly performance, "adjusted by us to account
                                               for additional market risks"
```

**Worked Interim Value grids from [S6]** (Indexed Crediting Base $1,000; 10%
Protection Level; caps 12% (1yr) / 100% (6yr)):

| Scenario | 1yr, 9mo elapsed, cap 12% | 6yr, 69mo elapsed, cap 100% | 6yr, 15mo elapsed, cap 100% |
|---|---|---|---|
| Index -30%: fixed proxy / deriv proxy / IV | $997 / $(197) / $800 | $997 / $(197) / $800 | $940 / $(163) / $777 |
| Index -10%: fixed / deriv / IV | $997 / $(28) / $969 | $997 / $(27) / $970 | $940 / $(6) / $934 |
| Index +20%: fixed / deriv / IV | $997 / $104 / $1,101 | $997 / $203 / $1,200 | $940 / $210 / $1,150 |
| Index +40%: fixed / deriv / IV | $997 / $119 / $1,116 | $997 / $401 / $1,398 | $940 / $335 / $1,275 |

Trigger-rate grid (1-year, 15% Protection Level, 12.5% Performance Trigger Rate):
7 months elapsed -> fixed $983; index -15% deriv $(30) IV $953; index -5% deriv $30
IV $1,013; index +10% deriv $93 IV $1,076; index +20% deriv $113 IV $1,096. At
4 months elapsed the fixed proxy is $973 and IVs are $940 / $997 / $1,056 / $1,078
respectively [S6].

Dual-trigger grid (1-year, 10% Protection Level, 6% Dual Performance Trigger Rate):
9 months elapsed -> fixed $993; index -15% IV $989; -5% IV $1,036; +10% IV $1,052;
+20% IV $1,052. 3 months elapsed -> fixed $980; IVs $956 / $1,000 / $1,029 /
$1,035 [S6]. Note the +10% and +20% cases give the same IV, as expected for a
capped digital payoff.

#### 5h. Academy worked hypothetical-portfolio example [R6]

Assumptions: 10% buffer, 500% cap rate (effectively uncapped), 100% participation
rate, generic index with ATM strike 1,000, risk-free yield r = 4%, ATM implied
volatility 20.47% (with a volatility surface across moneyness/maturity), dividend
yield q = 2%, term t = 6 years, 6-year zero coupon bond yield 2.33%. Derivative
Asset Proxy values computed with Black-Scholes.

| t | Index | Fixed proxy value | OTM put (short) | ATM call (long) | OTM call (short) | Deriv total | Trading costs | Contract value | Interim value |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1,000.00 | 87.09 | (9.10) | 22.04 | (0.00) | 12.94 | 0.01 | 100.02 | — |
| 1 | 1,100.00 | 89.12 | (6.65) | 24.97 | (0.00) | 18.32 | 0.02 | 107.43 | 107.43 |
| 2 | 1,210.00 | 91.20 | (4.48) | 28.03 | (0.00) | 23.55 | 0.02 | 114.73 | 114.73 |
| 3 | 1,331.00 | 93.32 | (2.60) | 30.99 | (0.00) | 28.39 | 0.03 | 121.68 | 121.68 |
| 4 | 1,464.10 | 95.50 | (0.84) | 34.68 | (0.00) | 33.84 | 0.03 | 129.31 | 129.31 |
| 5 | 1,610.51 | 97.72 | (0.09) | 38.55 | (0.00) | 38.46 | 0.04 | 136.14 | 136.14 |
| 6 | 1,771.56 | 100.00 | — | 77.16 | — | 77.16 | — | 177.16 | — |

Source: [R6]. This confirms the AG 54 boundary conditions numerically: the fixed
proxy starts at `Base - option budget` (87.09 = 100 - 12.94 + rounding) and accretes
to exactly 100.00 at term end, and the interim value is undefined at t=0 and t=6
(those are Strategy Values, not Interim Values). The Academy also publishes an Excel
Lambda function library reproducing this (functions `BlackScholes`, `GetVol`,
`OptionStrategy`, `DerivativeProxyAsset`, `FixedProxyAsset`, `HypotheticalPortfolio`)
[R6].

### 6. Charges

RILAs are largely **charge-light** on the index-linked side: "While no fees or
charges are deducted from the amounts held in the Index Strategies, the available
Cap Rates, Participation Rates, Tier Levels, and Step Rates reflect the expenses
related to the Index Strategies" [S3]. Brighthouse Shield Level II lists the
complete charge inventory as "(i) Withdrawal Charges; and (ii) Premium Tax and other
taxes" [S2]. Equitable and Lincoln both describe the cap as an "implicit ongoing
fee" [S4][S6]. Academy: "Most contracts do not have explicit fees other than for
optional benefits" [R6].

**No M&E charge is levied on index-linked options in any of S1–S4 or S6.**
[unverified] whether any RILA in the market applies an explicit M&E charge to
index-linked account value; none of the retrieved documents does.

Surrender / withdrawal charge schedules actually retrieved:

| Source | Basis | Schedule |
|---|---|---|
| S1 Brighthouse Shield Level Select 6-Yr | % of amount withdrawn in excess of the Free Withdrawal Amount, by complete contract years since Issue Date | yr0 7%, yr1 7%, yr2 6%, yr3 5%, yr4 4%, yr5 3%, yr6+ 0% |
| S2 Brighthouse Shield Level II 6-Yr | same | yr0 7%, yr1 7%, yr2 6%, yr3 5%, yr4 4%, yr5 3%, yr6+ 0% |
| S4 Equitable SCS PLUS 26, Series B | % of **contributions** withdrawn, by year following each contribution | yr1 8%, yr2 8%, yr3 7%, yr4 6%, yr5 5%, yr6 4%, yr7+ 0% |
| S4 Equitable, Select and Advisory series | — | No withdrawal charge |
| S5 Allianz Index Advantage+ Select Income | % of Purchase Payment withdrawn | "up to 8% ... declining to 0%" (full grid marked to be updated by amendment) |
| S6 Lincoln Level Advantage 2 B-Share | % of Purchase Payments surrendered/withdrawn, over a 6-year period | 7%, 7%, 6%, 5%, 4%, 3% |

Sources as tagged. Brighthouse worked example [S2]: $100,000 payment; $80,000
Account Value at the start of contract year 6; full withdrawal -> free amount
$8,000 (10%), charge 3% x $72,000 = $2,160, cash value $77,840.

Equitable charge ordering rules [S4]: withdrawal charge is determined separately for
each contribution, FIFO. "During the first six contract years, for withdrawal charge
purposes we will consider the 10% free amount withdrawn first until exhausted (which
will reduce earnings but not contributions), then contributions until exhausted (on
a FIFO basis). After the sixth contract year ... the 10% free amount first, then
contributions not subject to withdrawal charges, then earnings, and then
contributions subject to withdrawal charges" [S4]. "Any amount deducted to pay
withdrawal charges is also subject to that same withdrawal charge percentage" [S4]
— i.e. the charge is grossed up.

Equitable transaction expenses [S4]: sales load on purchases None; Transfer Fee $35
(currently waived; reserved for transfers in excess of 12 per contract year);
Third Party Transfer or Exchange Fee $55 (currently waived); Special Service Charges
up to $90 (express mail, wire transfer, duplicate contract, check preparation).

Allianz annual fees, **preliminary** [S5]: Base Contract 1.95% min and max
("comprised of two charges referred to as the 'product fee' and the 'rider fee for
the Income Benefit' ... As a percentage of the Charge Base, plus an amount
attributable to the estimated contract maintenance charge based on expected Contract
sales"); Investment Options (AZL Government Money Market Fund) 0.65%; optional
benefit 0.20% (Maximum Anniversary Value Death Benefit), assessed on the Charge
Base. Illustrative lowest/highest annual cost $2,321 / $2,476 on $100,000 [S5].
These cells are adjacent to "[To be updated by amendment]" markers — treat as
provisional.

Prudential CDSC [S3]: the mechanism is described (percentage of each applicable
Purchase Payment surrendered/withdrawn, FIFO, "gross" vs "net" withdrawal handling)
but the numeric CDSC grid lives in a cross-referenced "Annuity Owner Transaction
Expenses" table in the companion variable-subaccount prospectus that was not in the
retrieved supplement. **Gap** — see Gaps section.

### 7. Free withdrawal provisions

| Source | Provision |
|---|---|
| S1, S2 | Free Withdrawal Amount is **zero in the first Contract Year**; thereafter 10% of Account Value as of the prior Contract Anniversary, less amounts already withdrawn in the current Contract Year. Non-cumulative, no carry-over. |
| S3 | "Charge Free Withdrawal amount during each Annuity Year is equal to 10% of all Purchase Payments that are currently subject to a CDSC." Not available if the contract is surrendered. Not carried over. Minimum partial withdrawal $100. |
| S4 | Series B: 10% of account value per contract year free of withdrawal charge. |
| R6 | Industry survey: "Free withdrawal provisions ranging from 1% to 20%". |

Sources as tagged.

### 8. Death benefits

| Source | Design |
|---|---|
| S1 | Owner age 76+ at issue: death benefit = Account Value. Owner age 75 or younger: **Return of Premium** death benefit = greater of Account Value or Purchase Payment, "reduced proportionately by the percentage reduction in Account Value ... for each partial withdrawal (including any applicable Withdrawal Charge)". Determined as of the end of the Business Day on which due proof of death and an acceptable payment election are received. |
| S2 | Same structure but the age break moves to **81+ / 80 or younger**; the proportional reduction applies across Shield Options, the Fixed Account, and the Holding Account. |
| S3 | "The Death Benefit is the Return of Purchase Payments Death Benefit." |
| S4 | Standard death benefit plus an optional **Highest Anniversary Value Death Benefit** (a Guaranteed Minimum Death Benefit) electable at issue unless the owner is over age 75, for an additional charge. |
| S5 | "Traditional Death Benefit ... automatically provided by the Contract for no additional fee"; optional Maximum Anniversary Value Death Benefit at 0.20% of Charge Base. |

**Critical modelling point**: the death benefit is paid using the **Interim Value**,
not the Investment Amount, if death occurs mid-term. [S1]: "we will pay the Interim
Value, which may be less than if you held the Contract until all of your Shield
Option(s) reach their Term End Date". [S2]: Interim Value "is the amount that is
available for annuitization, death benefits, withdrawals, Surrenders, and
Performance Lock". [S4]: payment of a death claim is a Segment Interim Value
Transaction. [S6]: "Contract Adjustments are applied to withdrawals, surrenders,
reallocations, annuitizations and Death Benefit payments prior to the End Date of an
Indexed Term". So the ROP guarantee sits on top of a value that can itself be
depressed by a negative interim value — the GMDB is genuinely in the money in stress.

### 9. Annuitization / income options

- [S1]: Life Annuity; Life Annuity with 10 Years of Income Payments Guaranteed;
  Joint and Last Survivor Annuity; Joint and Last Survivor Annuity with 10 Years
  guaranteed. Fixed payment basis or any other option acceptable to the insurer.
- [S2]: narrower — (i) Life Annuity with 10 Years of Annuity Payments Guaranteed;
  (ii) Joint and Last Survivor Annuity with 10 Years of Annuity Payments Guaranteed.
- [S1]: "If the Contract is annuitized prior to a Term End Date, we will use the
  Interim Value to calculate the Income Payments".
- **Payout factors / annuity purchase rate tables were not located in any retrieved
  document.** See Gaps.

### 10. Fixed / general account options and transfer mechanics

- [S1][S2]: a **Fixed Account** is available (Appendix D), part of the general
  account, with a Fixed Account Term (minimum not less than 1 year in S2) and a
  **Minimum Guaranteed Interest Rate not less than 1%**, and in any event not less
  than the minimum allowed by state law [S1][S2].
- [S2] adds a **Holding Account**, also general account, credited daily at a declared
  effective annual rate with a guaranteed minimum not less than 1%. It receives
  maturing amounts when the same Shield Option and the Fixed Account are both
  unavailable, and holds them until the next Contract Anniversary [S2].
- The only "Market Value Adjustment" language in the Brighthouse Shield Level II
  prospectus appears inside the Interim Value appendix (the `[(1+C)/(1+D)]^E`
  factor); **no separate fixed-account MVA formula is defined in that document**
  [S2].
- Transfers: only during the **Transfer Period** — "the five (5) calendar days
  following the Contract Anniversary coinciding with the Term End Date" [S1]. During
  the Transfer Period the Interim Value of a Shield Option equals the Investment
  Amount at the Term End Date (i.e. no option-value adjustment) [S2]. Partial
  transfers of a Shield Option are not permitted except during the Transfer Period
  [S2].
- Automatic renewal: "At the Term End Date, the Investment Amount will automatically
  be renewed into the same Shield Option, with the new Step Rate, unless you elect to
  transfer" [S1]. Thirty days' advance notice of maturing options and where to find
  new rates [S1][S2].
- [S3]: FlexGuard is a combination contract — transfers from Index Strategies to
  Variable Investment Subaccounts are allowed at any time; reallocation into Index
  Strategies only on Index Anniversary Dates. Failure to give timely instructions
  routes value to a Holding Account invested in the PSF PGIM Government Money Market
  Portfolio, potentially for up to a year [S3].
- [S4]: Segment Type Holding Accounts hold contributions pending investment in a
  Segment and are part of the GIO. Dollar cap averaging accounts also exist [S4].

### 11. Performance Lock

- [S2]: "For any Shield Option, once during each Term you may elect to lock the
  Interim Value. Once an Interim Value is locked it is irrevocable for the remainder
  of that Term. The Performance Lock Value will be used as value of the Shield Option
  for the remainder of the Term." Locking is by Notice on a particular Business Day.
  After a lock, a withdrawal reduces the Performance Lock Value **dollar-for-dollar**
  rather than proportionally, and transfers become permissible on any Contract
  Anniversary [S2].
- [S5]: Performance Lock is available; Allianz "will not execute your request for a
  Performance Lock on Index Protection Strategy with Trigger or Index Protection
  Strategy with Cap Index Options if the Daily Adjustment is zero" [S5].
- [S6]: Lincoln's **Secure Lock+** locks the Interim Value and **resets the
  Performance Cap** for the remainder of the term; "we will not offer a Reset Rate
  under Secure Lock+ less than 3.50%" [S6]. The reset Discount Rate becomes input E
  in the Interim Value formula [S6].
- [R6] lists performance lock among the "more complex index strategies" parameters.

Modelling consequence: after a lock the option leg vanishes and the bucket becomes a
fixed accrual to term end, with dollar-for-dollar withdrawal accounting.

### 12. Guaranteed minimum non-guaranteed-element floors (contract-level guarantees)

These are the **guaranteed elements** in ASOP No. 2 terms [R5] and are what a
projection model must floor renewal assumptions at:

| Source | Guarantee |
|---|---|
| S1 | Minimum Guaranteed Cap Rate: not less than **2%** (1-Year Term), **6%** (3-Year), **8%** (6-Year). Minimum Guaranteed Step Rate: not less than **1.5%**. Minimum Guaranteed Interest Rate (Fixed Account): not less than **1%**. |
| S2 | Minimum Guaranteed Cap Rate: not less than **2%** / **6%** / **8%** for 1-/3-/6-Year Terms. Minimum Guaranteed **Edge** Rate: not less than **2%**. Minimum Guaranteed **Step** Rate: not less than **2%** (raised from 1.5% in S1). Minimum Guaranteed Interest Rate: not less than **1%**. |
| S4 | Minimum Limit on Index Gain for the life of the Segment: **12%** (6-year), **6%** (3-year), **2%** (1-year); Participation Rate 100%. |
| S6 | No 1-Year Indexed Account with a Performance Cap or Performance Trigger Rate below **4.00%**; no 6-Year Annual Lock account with a Performance Cap below **5.00%**; no 1-Year account with a Dual Performance Trigger Rate below **5.00%**; no 6-Year Performance Cap account with a Performance Cap below **21.00%**; no 6-Year Dual Plus account with a Performance Cap below **27.00%**; no Secure Lock+ Reset Rate below **3.50%**. |

Renewal rates are reset each term start and are non-guaranteed elements: "New Cap
Rates will be set for Index Strategy Terms upon Index Anniversary Dates. These Cap
Rates will be set based upon the current interest rate and market environment" [S3].
"Trigger Rates, Caps, and Participation Rates may be adjusted on the next Term Start
Date and may vary significantly from Term to Term" [S5]. Under ASOP No. 2, "index
parameters used to determine credited interest" are explicitly listed as examples of
NGEs, and "minimum index parameters" are listed as examples of guaranteed elements
[R5].

### 13. Regulatory framework — SEC registration [R1]

- Adopting release: **Release Nos. 33-11294; 34-100450; IC-35273; File No. S7-16-23;
  RIN 3235-AN30**, amending 17 CFR Parts 230, 232, 239 and 274 [R1].
- **Effective date: September 23, 2024.** **Compliance date: May 1, 2026**, except
  for rule 156 and the technical amendments to Forms N-3 and N-6, for which
  compliance is required on the effective date [R1].
- Mechanics of the transition [R1]: RILA issuers must file a post-effective
  amendment under final rule 485(a) effective on or before May 1, 2026 using final
  Form N-4; all initial registration statements and post-effective amendments filed
  on Form N-4 and effective on or after May 1, 2026 must comply.
- Statutory basis: "Division AA, Title I of the Consolidated Appropriations Act, 2023
  ('RILA Act')", **Pub. L. 117-328; 136 Stat. 4459 (Dec. 29, 2022)**, which directed
  the Commission to adopt a new registration form for RILAs within 18 months of
  enactment; had the Commission failed, RILA issuers could have begun registering on
  existing Form N-4 anyway [R1].
- Proposing release: Investment Company Act Release No. 35028 (Sept. 29, 2023)
  [88 FR 71088 (Oct. 13, 2023)] [R1].
- The rule extends the same registration/filing/disclosure framework to **registered
  market value adjustment annuities**; the two are collectively "non-variable
  annuities" and "differ only with respect to the manner in which interest is
  calculated and credited" [R1].
- The release's own description of RILA mechanics, useful as a neutral definition:
  an investor allocates purchase payments to index-linked options whose returns
  "(both gains and losses) are based at least in part on the performance of an index
  or other benchmark ... over a set period of time ('crediting period')"; upside is
  limited by "cap rates" and/or "participation rates" (collectively "limits on
  gains") and downside by "buffers" or "floors" (collectively "limits on losses").
  "A cap rate places an upper limit on an investor's ability to participate in the
  index's upside performance directly. A participation rate sets an investor's return
  to some specified percentage of the index's return. A buffer limits the investor's
  exposure to losses up to a fixed percentage. A floor places a lower limit on the
  investor's exposure to loss." [R1]
- The release names three distinct early-withdrawal costs: surrender charges;
  **"interim value adjustments" (IVAs)**, which "adjust the contract value if amounts
  are withdrawn ... from an index-linked option before the end of its crediting
  period"; and a positive or negative MVA — collectively "contract adjustments" [R1].
  "The IVA will adjust the contract value based, generally, on a complex formula
  where the IVA may change daily and can be positive or negative" [R1].
- Market size cited: RILA sales of **$47.4 billion in 2023**, 15% higher than the
  prior year and more than quintupled since 2017 ($9.2 billion); Q4 2023 was the
  first quarter in which RILA sales surpassed variable annuity sales [R1, citing
  LIMRA].
- Form N-4 content items relevant to modelling documentation: Item 3 Key Information
  Table; Items 6 and 17 "Principal Disclosure Regarding Index-Linked Options and MVA
  Options"; Items 4, 7 and 22 "Addition of Contract Adjustments ... to Fee and
  Expense Disclosures"; Item 31A "Information about Contracts with Index-Linked
  and/or MVA Options" [R1, table of contents].

### 14. Regulatory framework — NAIC nonforfeiture and reserving

**AG 54 [R2]** — see section 5a for the substantive requirements. Additional points:
- Purpose: "to specify the conditions under which an Index-Linked Variable Annuity
  (ILVA) is consistent with the definition of a variable annuity and exempt from
  Model 805 and specify nonforfeiture requirements consistent with variable
  annuities" [R2].
- Scope: "any index-linked annuity exempt from the NAIC Model 805 on the basis that
  it is a variable annuity and includes index-linked crediting features that are
  built into policies or contracts (with or without unitized subaccounts) or added to
  such by rider, endorsement, or amendment" [R2].
- Consequence of non-compliance: "An ILVA that does not comply with the principles
  and requirements of this guideline is not considered a variable annuity and
  therefore is subject to Model 805" [R2].
- "ILVA nonforfeiture benefits for Index Strategies subject to this guideline must
  comply with **Section 7 of Model 250 not including Section 7.B** with net
  investment return consistent with the requirements for determining Interim Values
  in this guideline" [R2].
- Effective date: contracts issued on or after **July 1, 2024** [R2].
- Filing requirement: an actuarial memorandum with each ILVA product filing,
  including certifications on equity, market-consistency of derivative valuation
  assumptions, material consistency with the Hypothetical Portfolio methodology, and
  reasonableness of Trading Costs; plus descriptions of the Fixed Income Asset Proxy
  value, **the market value adjustment formula, if any**, the market value of the
  Derivative Asset Proxy including Trading Costs, and "All formulas, methodologies
  and assumptions used to calculate these values for each Index Strategy and Index
  Strategy Term as well as the sources for all assumptions" [R2].
- Drafting history: the subgroup deliberately **removed** specific MVA requirements
  because consensus was unreachable on (1) whether MVA term lengths other than the
  Fixed Income Asset Proxy maturity should be allowed and (2) whether MVAs should be
  optional at all; the "equity" principle was left to guide state review instead
  [R2, project history]. This is the direct cause of the cross-insurer MVA variation
  documented in section 5.

**Model #250 [R4]** — Variable Annuity Model Regulation. Section 7 "Nonforfeiture
Benefits". Section 7.B (the provision AG 54 carves out): "To the extent that a
variable annuity contract provides benefits that do not vary in accordance with the
investment performance of a separate account before the annuity commencement date,
the contract shall contain provisions that satisfy the requirements of [the Standard
Nonforfeiture Law for Deferred Annuities] and shall not otherwise be subject to this
section" [R4]. Section 7.D.(2): "The minimum nonforfeiture amount at any time at or
prior to the commencement of any annuity payments shall be equal to an accumulation
up to that time at rates of interest equal to the net investment return ... of the
net considerations ... paid prior to that time, decreased by [charges]" [R4].
Section 7.C requires, on cessation of considerations, a paid-up annuity benefit and
(if the contract provides lump-sum settlement) a cash surrender benefit, with the
right to defer determination and payment while the NYSE is closed or the SEC has
declared an emergency [R4]. AG 54's background section quotes Model 250's definition
of variable annuities as "contracts that provide for annuity benefits that vary
according to the investment experience of a separate account" [R2].

**VM-21 applicability [R3]** — this needs care and is frequently mis-stated. VM-21
Section 2.A.1 brings in variable deferred annuity contracts, variable immediate
annuity contracts, group annuity contracts with GMDB/VAGLB-like guarantees, and "any
other policy or contract which contains guarantees similar in nature to GMDBs or
VAGLBs ... where there is no other explicit reserve requirement" [R3]. But
**Section 2.A.3 states: "Separate account contracts that guarantee an index and do
not offer GMDBs or VAGLBs are excluded from the scope of these requirements."** [R3]

So, for modelling purposes:
- A bare accumulation RILA with **no** GMDB and no living benefit is outside VM-21
  per Section 2.A.3 [R3].
- A RILA with a Return-of-Premium death benefit (S1, S2, S3) or a Highest Anniversary
  Value GMDB (S4) or a Maximum Anniversary Value GMDB (S5) offers a GMDB and
  therefore is not excluded by 2.A.3 [S1][S2][S3][S4][S5][R3].
- Section 2.A.2: VM-21 does not apply to contracts under VM-A-255 (Modified
  Guaranteed Annuities), "however, they do apply to contracts listed above that
  include one or more subaccounts containing features similar in nature to those
  contained in modified guaranteed annuities (MGAs) (e.g., market value adjustments)"
  [R3].
- Section 2.A.1 guidance note directs case-by-case evaluation of designs that do not
  clearly fit, "taking into consideration ... whether the contractual amounts paid in
  the absence of the guarantee are based on the investment performance of a
  market-value fund or market-value index (whether or not part of the company's
  separate account)" [R3].
- VM-21 effective for valuation dates on or after Jan. 1, 2020, with an elective
  phase-in of up to 36 months (extendable to seven years with domiciliary
  commissioner approval) [R3].
- The Academy's product-taxonomy table places ILVA statutory nonforfeiture under
  **MO-250** (versus MO-805 for FIA), statutory accounting as Separate Account, RBC
  as "C0–C1: General Account, C3–C4: Separate Account", and U.S. GAAP as General
  Account [R6].

**ASOP No. 2 [R5]** — "Nonguaranteed Elements for Life Insurance and Annuity
Products", Doc. No. 204, effective for actuarial services performed on or after
**June 1, 2022**. Scope covers "the determination and, if applicable, illustration of
NGEs for life insurance and annuity policies written on individual policy forms where
NGEs may vary at the discretion of the insurer"; examples of in-scope products
include "universal life, indeterminate premium life, and deferred annuity products.
Such products may be fixed, variable, or **indexed**" [R5]. Definition 2.4: an NGE is
"Any premium, charge, or benefit within an insurance policy that 1) affects policy
costs or values, 2) is not guaranteed in the policy, and 3) can be changed at the
discretion of the insurer", with examples including "index parameters used to
determine credited interest" [R5]. Definition 2.3: guaranteed elements include
"minimum index parameters" [R5]. Structural requirements the standard imposes:
a determination policy (2.2), an NGE framework (2.5), NGE scales (2.6), policy
classes (2.8), and periodic review of in-force NGEs (3.4.2) [R5]. Renewal cap /
participation rate setting in a RILA projection model is therefore an NGE process
governed by this ASOP.

Other ASOPs the Academy flags as potentially applicable to ILVA work: ASOP Nos. 1, 2,
7, 12, 15, 19, 22, 41, 52, 54 and 56 [R6].

### 15. Survey of common ILVA/RILA product features [R6]

Straight from the Academy's market survey (useful for calibrating a "representative"
model):
- Contingent deferred sales charge (CDSC) for durations of **three to 10 years**
- Free withdrawal provisions ranging from **1% to 20%**
- Fixed accounts common, or transfer accounts for interim holding of premiums
- Index crediting methods: PTP buffer with cap rate, participation rate, or trigger
  rate; PTP **dual direction** buffer with cap rate or trigger rate; PTP **floor**
  with cap rate, participation rate, or trigger rate
- Performance lock
- Index crediting periods of **one, two, three, or six years**
- "Market value adjustment formulas are typically calculated at the contract level and
  analogous fixed income proxy market values can be incorporated into the interim
  value formula within each index strategy option"
- "Withdrawals made during the interim period typically include a proportional
  reduction to optional benefit bases when the benefit base is not equal to the
  account value"
- "Black-Scholes and Monte-Carlo are commonly used methodologies for valuing option
  costs within the Derivative Asset Proxy"
- "Fixed Asset Hypothetical discount rate is often an external index such as the
  Bloomberg US aggregate index rate, Treasury Constant Maturity yield, Bloomberg US
  Credit or Corporate Index"
- Separate accounts: none registered with the SEC, all non-unitized, may be insulated
  or non-insulated
- Most contracts have no explicit fees other than for optional benefits

---

## Variations across insurers

**1. Interim value: three algebraic families.**
- *Fixed proxy net of option budget, with an explicit interest MVA factor* —
  Brighthouse `(A - B) x [(1+C)/(1+D)]^E` [S2] and Prudential
  `(A - B) x [(1+C)/(1+D)]^E` [S3]. These are the closest literal implementation of
  AG 54's Fixed Income Asset Proxy definition [R2].
- *Full notional discounted at a single current rate, with a separate positive
  expense rebate* — Equitable `SegmentInvestment / (1 + rate)^(time to maturity)`
  plus a **Cap Calculation Factor** [S4]. Lincoln's
  `C x [1/(1+E)^D x (1+E)^D/(1+F)^D]` is presented as accretion-times-MVA but
  reduces to the same shape [S6].
- *A delta applied to the notional rather than a value* — Allianz's
  `Daily Adjustment = [ΔProxyValue + proxy interest] x IndexOptionBase`, with **no
  interest-rate MVA term at all** [S5].

**2. The option-budget amortisation convention differs.** Brighthouse uses initial
market conditions "with **straight-line amortization** to the end of the Term" [S2];
Prudential uses initial market conditions "with **updated time to expiry**"
nationally but switches to straight-line amortisation **in Pennsylvania** [S3];
Allianz amortises the beginning Proxy Value linearly via
`beginning Proxy Value x (1 - time remaining)` [S5]. A general model needs this as a
configuration switch.

**3. The discount rate reference differs.** Brighthouse: **CMT** with maturity equal
to the Term, linearly interpolated [S2]. Lincoln: **CMT plus a market-observable
investment-grade corporate spread** [S6]. Prudential: **Bloomberg Barclays U.S.
Intermediate Credit Index** at a set duration that "may not match the actual length
of the Index Strategy" [S3]. Equitable: an investment-grade index rate constructed as
risk-free plus a spread, explicitly noting it is higher than swap rates and therefore
produces a lower fixed-leg value [S4]. AG 54's project history explains why this
varies: MVA requirements were deliberately left out of the guideline [R2].

**4. Buffer vs floor.** Buffers dominate. Only Allianz among the retrieved sources
offers an explicit **floor** product (Index Guard Strategy, -10% Floor) alongside
buffers, and it needs a four-option replicating portfolio rather than three [S5].
Prudential's **100% buffer** is a full-protection option achieved within the buffer
framework rather than a floor [S3]. The Academy confirms both exist in the market
("PTP floor with cap rate, participation rate, or trigger rate") [R6], and the SEC
release treats buffers and floors as the two species of "limits on losses" [R1].

**5. Buffer depth.** Brighthouse: 10/15/25 [S1][S2]. Prudential: 5/10/15/20/100 [S3].
Equitable: 10/15/20/40 [S4]. Allianz: 10/20/30 buffers plus a -10% floor [S5].
Lincoln: Protection Levels 10/15/20/25 [S6]. The **10% buffer is universal**, and
both Equitable and Prudential contractually commit to always offering it
(Equitable explicitly; Prudential by continuing availability) [S4].

**6. Term length.** 1, 3 and 6 years are near-universal; Brighthouse Shield Level II
adds a 2-year term [S2]; Lincoln offers only 1-year and 6-year [S6]; the Academy
survey reports one, two, three or six years [R6].

**7. Dual-direction / absolute-return designs.** Equitable's Dual Direction pays
`|IPR|` for losses within the buffer [S4]; Allianz's Index Dual Precision pays the
Trigger Rate for losses within the buffer [S5]; Lincoln's Dual Performance Trigger
Rate and Dual Rate accounts do the same [S6]; Brighthouse's Step Rate Edge triggers
at `-B` rather than 0 [S2]. Prudential (as of S3) has no dual-direction strategy.

**8. Withdrawal accounting is uniform and is the single most important behavioural
rule.** All five insurers reduce the index-linked notional **proportionally to the
reduction in interim value**, not by the dollar amount withdrawn [S2][S3][S4][S6],
and all warn that the proportional reduction can exceed the dollar withdrawal when
the interim value is below the notional [S2][S3][S6]. The one exception is a
**locked** bucket: after a Performance Lock, Brighthouse reduces the Performance Lock
Value **dollar-for-dollar** [S2].

**9. Charge structure.** Almost all of S1–S4 and S6 carry **no explicit asset-based
charge** on index-linked value; the cap is the fee. Allianz's Select Income variant is
the outlier with an explicit 1.95% base contract fee assessed on a Charge Base,
because it bundles a guaranteed-income rider [S5].

**10. Fee-series structure.** Equitable sells three series off one chassis —
**Series B** (8%-grading-to-0 withdrawal charge over 6 years), **Select** (no
withdrawal charge, lower caps), and **Advisory** (no withdrawal charge) [S4].
Lincoln likewise has B-Share and Advisory [S6]. A model should parameterise the
withdrawal-charge schedule and the cap level jointly, since they trade off.

**Which design is representative.** For a reference implementation, the best single
target is a **single-premium, 6-year-chassis buffered RILA with 1/3/6-year point-to-
point terms, buffers of 10/15/20/25, Cap / Step (trigger) / Dual crediting types, a
7-7-6-5-4-3-0 withdrawal charge on amounts above a 10%-of-account-value free
withdrawal (zero in year 1), a Return-of-Premium GMDB, no explicit asset charge, and
an AG 54 hypothetical-portfolio interim value of the form
`(Base - amortised option budget) x [(1+r0)/(1+rt)]^(days remaining/365) + BS(replicating options)`.**
That is essentially the Brighthouse Shield Level II design [S2], it matches AG 54's
literal definitions [R2], it matches the Academy's worked example structure [R6], and
it is the closest to the industry mode reported in the Academy survey [R6].

---

## Gaps and caveats

1. **No current declared rate sheet was retrievable.** Both the Brighthouse Shield
   rates page and the Equitable performance cap rates page returned 403 / WAF
   rejections. All cap, step, edge, trigger and participation rates quoted above are
   either (a) contractual guaranteed minima or (b) illustrative values used inside
   prospectus examples. No actual currently-declared rate is recorded here.
   Illustrative-only values include: Brighthouse 10% Cap / 8% Step [S1]; Equitable
   60% cap with 110% participation on a 6-year -20% Standard segment, 9% cap on a
   1-year Step Up, 90% cap with 105% participation on a 6-year -10% Dual Direction
   [S4]; Prudential 5% Step / 90% participation, 75% 3-year cap, 100%/140% tiers with
   a 30% tier level [S3]; Lincoln 12% 1-year cap, 100% 6-year cap, 12.5% trigger, 6%
   dual trigger [S6].

2. **Annuitization payout factors and annuity purchase rate tables were not found**
   in any retrieved document. Annuity option *names* are documented [S1][S2] but the
   mortality basis, assumed interest rate and factor tables are not. These normally
   live in the contract specimen or the SAI, neither of which was located for these
   products.

3. **Prudential's CDSC percentage grid is missing.** The retrieved FlexGuard
   supplement cross-references "Annuity Owner Transaction Expenses" in the companion
   variable-subaccount prospectus, which was not retrieved. The 10%-of-purchase-
   payments Charge Free Withdrawal and the FIFO/gross-vs-net mechanics *are*
   documented [S3].

4. **Allianz fee figures are provisional.** The S5 filing is an initial N-4 with
   "[To be updated by amendment]" markers and a placeholder prospectus date
   "[December XX, 2025]". The 1.95% / 0.65% / 0.20% figures and the $2,321 / $2,476
   cost illustration should be re-verified against the effective prospectus before
   use.

5. **The Prudential source is dated.** S3 is a September 2022 supplement. FlexGuard
   has since been re-registered on Form N-4 under the 2024 rule [R1]; index strategy
   menus, buffers and rates will have changed.

6. **Athene (Amplify), Symetra (Trek), Jackson (Market Link Pro) and Transamerica
   (Structured Index Advantage) were identified in EDGAR full-text search results but
   their main prospectus documents were not retrieved or read.** EDGAR full-text
   search returned 228 hits for "Amplify" across N-4 filings by Athene Annuity & Life
   Co (CIK 0000837332) and Athene Annuity & Life Assurance Co of New York (CIK
   0001590625), and Transamerica N-4 filings referencing "Index Advantage" (CIK
   0001164098 / 0001571931), but the hits returned were exhibits (powers of attorney,
   underwriting agreements) rather than prospectus bodies. No facts from those
   insurers are asserted anywhere above.

7. **No specimen contract / policy form was located for any of these products.** All
   product facts come from prospectuses, which are the governing offering documents
   but are not the contract itself. Contract schedule pages (which carry the
   policy-specific Minimum Guaranteed Cap Rate, Minimum Guaranteed Interest Rate,
   etc.) are referenced repeatedly [S1][S2] but not reproduced.

8. **Trading Costs are required by AG 54 [R2] and appear in the Academy example [R6],
   but no retrieved prospectus quantifies them.** Brighthouse [S2], Equitable [S4] and
   Lincoln [S6] all say the derivative valuation "reflects the estimated cost of
   exiting" the options, without a number. A model will need this as a free
   parameter.

9. **No SOA research paper on RILA hedging or interim-value construction was
   retrieved.** The Academy policy paper [R6] is the substitute and is the stronger
   source for the interim-value mechanics; the SOA literature was not searched
   exhaustively. [unverified] whether specific SOA sections have published RILA
   hedging research.

10. **The IIPRC standard IIPRC-03-I-ILVA is quoted only second-hand** through the
    Academy paper [R6]. The Compact standard itself was not retrieved; the statement
    that the Compact "requires the use of the Hypothetical Portfolio methodology and
    does not allow for materially consistent approaches" rests on [R6], not on the
    Compact document.

11. **AG 54's post-adoption status**: the retrieved PDF [R2] is the version carrying
    the LATF (12/11/2022) and A Committee (2/24/2023) adoption stamps. Adoption by
    the NAIC Executive (EX) Committee and Plenary is widely reported as having
    occurred in March 2023, but that final step is **not** stamped on the retrieved
    document. [unverified] as to the exact Plenary adoption date; the July 1, 2024
    effective date **is** stated in the retrieved text [R2].

12. **Tax treatment** is only lightly covered here (deferral; ordinary income on
    distributions; 10% additional tax before 59½; no incremental benefit inside an
    IRA) [S3][S4]. No IRC or Treasury regulation source was retrieved for this file.
