# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/universal-life.md`, and [REG-R#] (the
cross-product reference library `references/regulatory-and-actuarial-references.md`,
whose own R-numbering is distinct; research provenance in
`_research/regulatory-actuarial.md`) — were extracted from the cited document. Values marked
**[std]** are standardizations introduced for the reference implementation; each [std]
table row carries a footnote giving the rationale and the observed range across
insurers. Facts the research file could not verify are flagged [unverified]. The
implementation anchor for mechanics is one carrier's specimen policy (form P08VP1,
8/08; specimen cell Male 35 Standard Nonsmoker, $100,000) [S3].

---

## Product overview and market role

Universal life is defined by regulation as a life insurance policy "where separately
identified interest credits ... and mortality and expense charges are made to the
policy"; flexible-premium UL additionally lets the owner vary the amount and timing of
premiums and the amount of insurance [R1]. Definitions to the same effect are printed
in the AP&P Manual's own valuation item, Appendix **A-585** ¶¶7 and 3, now read at
first hand — the two texts were **not** compared line by line [REG-R155]. The
flexible/fixed distinction is not cosmetic: it is what switches on the funding ratio
in the statutory reserve (see `technical-notes.md`, "Valuation and reserve pointers").
The *current assumption* variant is the interest-sensitive, cash-value-oriented
chassis: the insurer declares a current credited interest rate and current charge
scales that may be more favorable than the contractual guarantees (minimum interest,
maximum charges), and revises them at its discretion subject to actuarial standards on
non-guaranteed elements [R1] [R8].

In the SOA/LIMRA 2015–2021 flexible-premium UL experience study, Current Assumption was
one of three main product focuses, at 27% of known exposure (Cash Accumulation 33%,
Lifetime Guarantee 27%); by policy count, fixed (non-indexed, non-variable) UL designs
are the most common chassis across all product focuses [R7]. Current-assumption UL
competes on credited rate and current charges rather than on secondary (no-lapse)
guarantees; guaranteed-death-benefit needs are served by dedicated GUL products with
lifetime no-lapse guarantees (one of the fetched products guarantees to attained
age 120) [S4], which are out of scope here.

Current-assumption fixed UL is not an SEC-registered product; no statutory prospectus
exists for it (prospectuses cover variable UL only) [unverified as a legal statement;
consistent with EDGAR searches recorded in the research file].

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Flexible-premium adjustable (universal) life, current assumption, fixed interest | [S1] [S3] [R1] |
| Policy form style | Individual, non-participating | [S3] |
| Interest crediting style | Portfolio: current rate declared periodically by insurer | [S2] [S3]; choice **[std]** (1) |
| Death benefit qualification test | Guideline Premium Test (GPT), elected at issue, irrevocable | [S3] [R2]; choice **[std]** (2) |
| Death benefit options | Option A (level) and Option B (face + AV); Option C out of scope | [S1] [S3]; scope **[std]** (3) |
| Issue ages | 18–85 | [S1] [S2]; band choice **[std]** (4) |
| Rate classes | 6 classes: Preferred Plus NT, Preferred NT, Standard Plus NT, Standard NT, Preferred Tobacco, Standard Tobacco | [S1] [S2] [S4]; 6-class structure **[std]** (5) |
| Minimum face amount | $100,000 | [S1]; choice **[std]** (6) |
| Maturity | None — no maturity date; charges and premiums cease at attained age 121, coverage continues for life | [S2] [S3] |
| Anchor model cell | Male 35, Standard Nonsmoker, $100,000 face, Option A, GPT | [S3] |

Footnotes to [std] rows:

1. Portfolio crediting chosen over new-money. Observed: one of the three fetched
   current-assumption products uses new-money (each net premium earns its declared
   rate locked for 12 months from receipt) [S1]; the other two, including the
   specimen, use periodically declared portfolio rates [S2] [S3]. Portfolio-style is
   the more common design and the simpler modeling default [unverified as to market
   share].
2. GPT chosen per the task's representative design and because the specimen cell itself
   elects GPT [S3]; CVAT (minimum DB floor 101% of AV in the specimen implementation
   [S3]) is the alternative under IRC 7702 [R2].
3. Options A and B are universal across the fetched products; a return-of-premium
   Option C is offered by some (one caps C at 2x initial face [S1]; the specimen
   offers C [S3]) and is excluded to keep the reference recursion minimal.
4. Observed issue-age ranges: 15 days–85 including a juvenile class [S1]; 18–85 with
   preferred classes capped at 75 [S2]; 18–85 for the GUL contrast product [S4]. The
   composite drops juvenile issues.
5. Observed: 6–7 classes typical (7 on one current-assumption product, including a
   juvenile class [S1]; 5 on another [S2]; 6 on the GUL contrast product [S4]).
6. Observed: $100,000 all classes [S1]; $50,000 Non-Tobacco/Tobacco and $100,000
   preferred classes [S2].

### Interest

| Parameter | Representative value | Basis |
|---|---|---|
| Guaranteed minimum annual effective interest rate | 2.00% | range 2%–3% [S1] [S2] [S3]; pick **[std]** (7) |
| Current declared annual effective rate (snapshot) | 4.00% | **[std]** (8) |
| Crediting frequency (contract) | Daily, 365-day year, at no less than the guaranteed rate; excess interest discretionary, uniform by class | [S3] |
| Rate on loaned AV | Guaranteed rate (2.00%) | design [S2] [S3]; value **[std]** (7)(15) |

7. Observed guaranteed minimums: 2% (2014-era form still sold in 2023) [S1]; 2.5%
   (2015-era form) [S2]; 3% policy years 2+ (2008-era specimen form) [S3].
   Guaranteed minimums correlate with issue era; new issues cluster at 2%
   or below following the 2021 IRC 7702 rate change (transition insurance interest
   rate 2%) [R2] [unverified for the market generally]. 2.00% chosen as representative
   of current new issues.
8. Current declared crediting rates are not published in the fetched public documents,
   and the one current-rates page that was attempted returned HTTP 403 [S5]. 4.00% is
   a pure modeling assumption for the snapshot current scale; the model should treat it
   as a non-guaranteed element revisable under ASOP 2 discipline [R8].

### Charges (per policy unless stated; "current" = snapshot NGE scale, "guaranteed" = contractual maximum)

| Parameter | Representative value | Basis |
|---|---|---|
| Premium expense load — current | 6% of each premium, all years | [S1]; adoption as composite **[std]** (9) |
| Premium expense load — guaranteed maximum | 9% of each premium | [S1]; adoption as composite **[std]** (9) |
| Per-policy administrative charge | $7.50/month, current = guaranteed, to age 121 | [S3]; adoption as composite **[std]** (10) |
| Per-unit (coverage) expense charge | $0.26 per $1,000 face/month, policy years 1–10; $0.156 per $1,000/month years 11 to age 121; 0 thereafter | [S3]; adoption as composite **[std]** (11) |
| Guaranteed maximum monthly COI rates | Specimen table per $1,000 NAAR by policy year (issue age 35): yr 1: 0.10090; yr 5: 0.12840; yr 10: 0.19940; yr 20: 0.45950; yr 30: 1.27900; yr 40: 3.23010; yr 50: 9.24140; yr 60: 23.81220; yr 70: 46.82420; yr 77: 77.62690; yrs 78–86 (attained ages 112–120): 83.33330 (= 1000/12); yr 87+ (age 121+): 0 | [S3]; adoption as composite **[std]** (12) |
| Current monthly COI rates | 60% of the guaranteed maximum rate at every duration | **[std]** (12) |
| Rider charges | 0 (base model carries a placeholder) | scope **[std]** (see Riders) |

9. Observed premium loads: 6% current / 9% guaranteed max, all years [S1]; 10% all
   years, single stated rate [S2]; 6.95% guaranteed max, current may be lower [S3].
   The 6%/9% pair is adopted because it exhibits the typical current-vs-guaranteed
   NGE gap; the load itself is a non-guaranteed element in that design [S1].
10. Observed per-policy charges: $10/month current, $30/month guaranteed max [S1];
    $5/month all years to 121 [S2]; $7.50/month (specimen) [S3]. The specimen value is
    adopted (implementation anchor); the model treats it as both current and
    guaranteed, understating the observed guaranteed max (up to $30 [S1]).
11. Observed per-unit charges: rate per $1,000 face varying by sex/class/issue
    age/size/duration [S1]; per $1,000 of *initial* face by age/sex/class, all years
    to 121 [S2]; $26.00/month per $100,000 years 1–10 then $15.60/month years 11–86
    (= $0.26 then $0.156 per $1,000/month; the higher first-10-year charge is
    acquisition-cost recovery) [S3]. Specimen values adopted verbatim for the anchor
    cell; the year-10 step-down is retained.
12. The specimen guaranteed COI table is a 2008-era (2001 CSO basis) table [S3]; no
    2017 CSO-era specimen COI table was obtained (research gap). Guaranteed rates for
    policy years not listed are interpolated log-linearly **[std]**. The current scale
    (60% of guaranteed, flat across durations) is a pure modeling assumption: current
    (non-guaranteed) COI scales are not published in public documents — only
    guaranteed maxima appear in the specimen [S3]. All three current-assumption source
    products charge COI monthly per $1,000 of net amount at risk with current scales
    at or below guaranteed maxima [S1] [S2] [S3]; charging less than maximums must be
    uniform by class [S3].

### Surrender, withdrawal, loan

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender charge — initial amount | $9.00 per $1,000 initial face | **[std]** (13) |
| Surrender charge — runoff | Declines linearly by $1.00 per $1,000 per year, amortized monthly (1/12 per month); zero from the start of policy year 10 | 9-year pattern [S1] [S2]; monthly amortization mechanics [S3]; amount **[std]** (13) |
| Surrender charge — layers | Each face-increase layer carries its own schedule; face decreases do not reduce the surrender charge | [S3] |
| Cash surrender value (CSV) | AV − surrender charge | [S3] [R1] |
| Net cash surrender value (NCSV) | CSV − policy debt | [S3] |
| Partial withdrawal | From first policy anniversary; minimum $200; fee $25; no surrender charge assessed on withdrawal | [S2] [S3] |
| Free partial withdrawal amount | 10% of AV per policy year, first withdrawal each year | 10%-of-value carve-out [S3]; simplification **[std]** (14) |
| Policy loan — charged rate | 2.75% annual, accrued daily, capitalized if unpaid at policy year end | design [S3]; value **[std]** (15) |
| Policy loan — credited rate on loaned AV | 2.00% (guaranteed rate) — 0.75% guaranteed spread | spread [S3]; level **[std]** (15) |
| Maximum loan | AV − 3 x most recent monthly deduction − surrender charge − existing policy debt | [S3] |
| Loan repayment priority | Payments while a loan is outstanding are treated as loan repayments unless designated as premium | [S3] |

13. Observed surrender charge designs: 9-year decreasing schedule, rate per $1,000 by
    sex/class/issue age [S1]; declining over first 9 policy years, pro-rata partial
    charge on face decreases [S2]; fixed dollar schedule — initial $921 per $100,000
    (= $9.21 per $1,000) reducing by $92.10/year amortized in monthly twelfths, zero
    after end year 10 [S3]. The composite takes the 9-year runoff (the modal length)
    with the specimen's monthly-amortization mechanics and rounds the specimen's
    initial level to $9.00 per $1,000.
14. The specimen's free-withdrawal carve-out is: first withdrawal in a policy year,
    during the first 15 policy years, up to the lesser of $10,000 or 10% of net cash
    surrender value; withdrawals under Option A that would increase the net amount at
    risk otherwise reduce total face [S3]. The composite simplifies to 10% of AV per
    year with no 15-year limit, which is the pattern the task standardizes on.
15. Observed loan designs: fixed accrual up to 3.25% with the loaned AV credited at
    the 3% guaranteed rate (0.75% spread) [S3]; 5% in arrears with 2.5% credited
    (2.5% spread) [S2]; variable rate at Moody's Corporate Bond Yield Average, floor
    3% [S1]. The composite keeps the specimen's 0.75% guaranteed spread on top of the
    [std] 2.00% guarantee, giving a 2.75% charged rate.

### Premium, grace, lapse, reinstatement

| Parameter | Representative value | Basis |
|---|---|---|
| Premium flexibility | Amount and timing at owner's discretion; planned premium is a billing target only, no guarantee of coverage | [S3] [R1] |
| Minimum premium remittance | $50 | [S3] |
| Representative planned premium (anchor cell) | $150/month ($1,800/year) | **[std]** (16) |
| Guideline premiums (anchor cell, incl. specimen riders) | GSP $34,138.15; GLP $2,825.52; 7-pay premium $6,702.10 | [S3] (specimen cell includes riders) |
| Grace period | 61 days; triggered when AV less policy debt on a monthly payment date cannot cover the current monthly deduction | [S2] [S3] |
| Required grace payment | At least 3 x the monthly deduction due, plus premium load | [S3] |
| Death during grace | DB proceeds reduced by overdue charges | [S3] |
| Lapse | At end of grace without required payment, policy terminates with no value | [S3] |
| No-lapse guarantee | 5 years from issue on minimum-premium condition; NOT modeled in the base reference model | [S1]; scope **[std]** (17) |
| Reinstatement | Within 5 years of end of grace; evidence of insurability; premium (net of load) covering grace-period deductions and loan interest plus 3 months forward; COI schedule resumes as if lapse never occurred | [S3] |

16. Pure modeling choice for the worked examples; the specimen planned annual premium
    for the anchor cell was $4,124.59 including riders [S3]. $150/month is set well
    below guideline limits so GPT/MEC constraints do not bind in the base projection.
17. Observed lapse protection on current-assumption UL: short built-in NLG (5 years on
    minimum premium [S1]) or optional flexible-duration shadow-account endorsements
    (one such endorsement carries a catch-up provision [S2]). Lifetime
    secondary guarantees belong to dedicated GUL products [S4]. The base model excludes
    all secondary guarantees; modeling them changes the reserve regime (AG 38 / VM-20
    ULSG treatment [REG-R6] [REG-R7]).

---

## Contractual mechanics

### Premium provisions

Premiums are flexible in amount and timing; the planned premium is only a billing
target [S3] [R1]. Each premium is processed as: (1) deduct the premium expense load;
(2) credit the net premium to the account value (AV; the specimen's "accumulated value") [S3]:

    net premium = gross premium x (1 - premium load rate)

The current load rate (6%) may be less than the guaranteed maximum (9%); lesser
charges apply uniformly by class [S1] [S3]. Minimum remittance $50 [S3]. Premiums that
would cause cumulative premiums (less a portion of withdrawals) to exceed the GPT
guideline limit — the greater of the guideline single premium and the sum of guideline
level premiums — are refused/refunded; the insurer may force distributions to maintain
IRC 7702 status [S3] [R2]. Premiums that would fail the 7-pay test are refunded unless
the owner elects MEC status in writing [S3] [R3].

### Death benefit provisions

- Option A (level): DB = total face amount F. Option B (increasing): DB = F + AV
  [S1] [S3].
- The DB payable is the greater of the option amount and the minimum DB under the
  elected qualification test [S3]. Under GPT the minimum DB is AV x the corridor
  factor at attained age [S3] [R2]:

  | Attained age | Corridor % | Attained age | Corridor % |
  |---|---|---|---|
  | 0–40 | 250 | 61 | 128 |
  | 41 | 243 | 62 | 126 |
  | 42 | 236 | 63 | 124 |
  | 43 | 229 | 64 | 122 |
  | 44 | 222 | 65 | 120 |
  | 45 | 215 | 66 | 119 |
  | 46 | 209 | 67 | 118 |
  | 47 | 203 | 68 | 117 |
  | 48 | 197 | 69 | 116 |
  | 49 | 191 | 70 | 115 |
  | 50 | 185 | 71 | 113 |
  | 51 | 178 | 72 | 111 |
  | 52 | 171 | 73 | 109 |
  | 53 | 164 | 74 | 107 |
  | 54 | 157 | 75–90 | 105 |
  | 55 | 150 | 91 | 104 |
  | 56 | 146 | 92 | 103 |
  | 57 | 142 | 93 | 102 |
  | 58 | 138 | over 93 | 101 |
  | 59 | 134 | | |
  | 60 | 130 | | |

  (Specimen GPT corridor table; it implements the IRC 7702 cash value corridor
  [S3] [R2].)
- Option changes: to A or B only, at most once per policy year; total face is adjusted
  so the DB is unchanged at the change date; a change is rejected if it would create a
  MEC unless requested [S3].
- Death benefit proceeds = DB − policy debt − due and unpaid monthly deductions during
  grace; interest is paid on proceeds from the date of death [S3].
- Face increases require evidence of insurability (specimen: insured no older than 90,
  minimum increase $25,000) and create a new coverage layer with its own COI rates,
  coverage charge, and surrender charge; decreases are limited to one per year, none
  in year 1, and reduce layers LIFO [S3] [S2].

### Account value mechanics

The contract credits interest daily (365-day year) at no less than the guaranteed
rate; excess interest is discretionary and uniform by class [S3]. The contractual
roll-forward [S3]:

- On the policy date: AV = net premium − first monthly deduction.
- On each other day: AV = prior-day AV + interest + net premiums received −
  withdrawals and withdrawal fees − (on a monthly payment date) the monthly deduction.

The monthly deduction is taken on each monthly payment date (the same day each month
as the policy date) before the monthly deduction end date (attained age 121), and pays
for the FOLLOWING policy month's coverage [S3].

### Charges and credits

    monthly deduction = per-unit coverage charge
                      + per-policy administrative charge
                      + rider charges
                      + cost of insurance (COI) charge                     [S3]

    COI charge = (monthly COI rate / 1000) x NAAR                          [S3]

    NAAR = DB (as of the most recent monthly payment date) / NAAR factor
         − AV (measured at the beginning of the policy month,
               before the monthly deduction)                               [S3]

The NAAR factor discounts one month at the guaranteed annual rate: the specimen shows
1.0024663 = 1.03^(1/12) at its 3% guarantee [S3]; at the composite 2.00% guarantee
**[std]** the factor is 1.02^(1/12) = 1.0016516 (derived). Guaranteed maximum COI
rates grade to 1000/12 per month at attained ages 112–120 (a single month's charge
equals the full NAAR) and to zero at 121+ [S3]. The insurer may charge current rates
below the guaranteed maxima, uniformly by class [S3]; guaranteed maxima are capped by
CSO valuation mortality — 2001 CSO on the 2008-era specimen form [S3]; 2017 CSO for
new issues on/after 2020-01-01 [R4] [unverified — from search-result context, not a
fetched primary document].

### Loans

Available on the sole security of the AV (specimen: after free-look; minimum loan
$200) [S3]. Maximum loan = AV − 3x most recent monthly deduction − surrender charge −
existing policy debt [S3]. Interest accrues daily at the charged rate (composite 2.75%
**[std]**, footnote 15), is due at policy year end, and is capitalized if unpaid [S3].
The loaned portion of AV is credited at the guaranteed rate (a design feature in both
fetched fixed-loan products) [S2] [S3]. Payments while debt is outstanding repay the
loan unless designated as premium [S3].

### Withdrawals (partial surrenders)

Allowed on/after the first policy anniversary; minimum $200; fee $25; no surrender
charge on withdrawal; remaining net cash surrender value must stay >= $500 (specimen)
[S3]. Under Option A a withdrawal that would increase the NAAR reduces total face,
except for the free partial withdrawal amount (composite: 10% of AV per policy year,
first withdrawal each year **[std]**, footnote 14) [S3]. Under Option B withdrawals
reduce AV only [S3].

### Grace, lapse, reinstatement

Grace is triggered if AV less policy debt on a monthly payment date cannot cover the
current monthly deduction [S2] [S3]; the Model 585 default definition is lapse when
NCSV first equals zero, with grace of at least 30 days and 30-day advance written
notice [R1]. Composite: 61-day grace [S2] [S3]; required payment >= 3x the monthly
deduction due plus premium load [S3]; if the insured dies in grace, proceeds are
reduced by overdue charges; on expiry of grace unpaid, the policy terminates with no
value [S3]. Reinstatement within 5 years with evidence of insurability and the
catch-up premium described above [S3].

### Renewal / conversion / maturity

There is no renewal or conversion structure (coverage is permanent and premiums
flexible). The policy does not mature: at attained age 121 monthly deductions cease,
premiums are no longer accepted, loans and loan repayments remain available (loan
interest continues to accrue), withdrawals are not allowed, interest continues to be
credited, and coverage continues for life [S3]; another fetched product similarly
discontinues premiums and charges at attained age 121 [S2]. IRS guidance on
post-age-100 coverage was noted as unsettled in the specimen [S3].

---

## Riders

**In scope (described, charged at 0 in the base model [std]):** none are projected in
the base reference model; the monthly-deduction formula carries a rider-charge term as
a placeholder so that rider modules can be added without changing the recursion [S3
formula structure].

Commonly attached riders on this chassis, for context:

- Terminal illness accelerated death benefit: e.g., up to 75% of DB, $500,000 max,
  12-month prognosis, no surrender charge on the lump sum [S1]; up to 60% of DB or
  $1 million [S2].
- Chronic illness acceleration: up to 50% of DB ($500,000 max), ADL/cognitive
  triggers, lien design; optional up to 100% of DB with 2% monthly benefit capped at
  the IRS per diem x 30 [S1]; an acceleration rider whose terms the fetched producer
  guide does not state [S2]; LTC rider, cash indemnity 2%/3%/4% monthly up to 2x the
  HIPAA per diem [S4].

**Out of scope:** accidental death benefit [S1] [S2]; children's term [S2]; disability
benefit crediting a monthly amount to the policy [S2]; additional/annual renewable
term riders including additional-insured term [S1] [S3]; surrender value enhancement
rider [S3]; charitable giving benefit (+1% of face) [S1]; return-of-premium windows on
GUL [S4]; an endorsement paying the death benefit as an installment income stream [S2];
no-lapse guarantee/shadow-account endorsements [S1] [S2] [S4] (see footnote 17).

---

## Variations across insurers

1. **Crediting style.** New-money 12-month rate locks per premium (one of the three
   [S1]) vs periodically declared portfolio rate (the other two [S2] [S3]).
   Representative choice: portfolio — more common and the simpler modeling default
   [unverified as to market share].
2. **Guaranteed minimum interest.** 2%–3% among fetched forms, correlated with issue
   era (3% on the 2008 form [S3]; 2.5% on the 2015 form [S2]; 2% on the 2014/2023 form
   [S1]). Chosen: 2.00%, representative of the post-2021 IRC 7702 rate environment
   [R2] **[std]**.
3. **Premium loads.** 6%–10% [S1] [S2] [S3]; some insurers keep a current-vs-guaranteed
   gap (6%/9% [S1]) making the load itself an NGE; others state a single rate
   [S2] [S3]. Chosen: 6%/9% to exercise the NGE machinery.
4. **Per-policy and per-unit charges.** Per-policy $5–$10/month current, $30/month
   guaranteed max observed [S1] [S2] [S3]. Per-unit charge bases differ: initial face
   [S2] vs coverage-layer face with a step-down after year 10 [S3] vs
   duration-varying [S1]. Chosen: specimen values with the year-10 step-down, because
   the specimen is the mechanics anchor.
5. **Surrender charges.** 9–10 year runoff is standard; expressed as rate per $1,000
   by sex/class/age [S1] [S2] or fixed dollar amount with linear monthly amortization
   [S3]. Chosen: 9-year, dollar-per-$1,000, monthly amortization.
6. **COI structure.** All fetched products: monthly rate per $1,000 NAAR, guaranteed
   maxima (CSO-capped), lower current scales, rates varying by issue
   age/sex/class/duration [S1] [S2] [S3]. Chosen: specimen guaranteed table + flat 60%
   current factor **[std]** (current scales are not public — see spec footnote 12).
7. **DB options.** A and B universal; C (return of premium) offered by some [S1] [S3].
   Chosen: A and B only.
8. **Loans.** Fixed-rate with guaranteed spread (0.75% [S3]; 2.5% [S2]) vs variable
   Moody's-indexed with 3% floor [S1]. Chosen: fixed with 0.75% spread.
9. **Lapse protection.** Short built-in NLG (5 years [S1]) vs optional shadow-account
   endorsement [S2] vs dedicated GUL [S4]. Chosen: 5-year NLG disclosed but not
   modeled (spec footnote 17). The market separates "current assumption" from
   "lifetime guarantee" focuses, each ~27% of UL exposure, cash accumulation 33% [R7].
10. **Vintage caveat.** The fetched documents span 2008–2023 form eras; parameter
    LEVELS are era-representative while MECHANICS are stable across eras (research
    file caveat). Composite levels here follow the newest-era guarantees (2%) with
    specimen-era mechanics.

---

## Regulatory context

**NAIC Universal Life Insurance Model Regulation (Model 585).** Defines UL and governs
valuation (CRVM adaptation via Guaranteed Maturity Premium/Fund and the r-ratio),
UL-specific nonforfeiture (retrospective minimum CSV with expense-allowance
amortization; surrender charges permissible above that floor), mandatory policy
provisions (guarantees stated in the policy; interest credits not conditional beyond
24 months; grace of at least 30 days with notice), and the prescribed annual report to
policyowners [R1] [REG-R5 same document](#uslib-reg-r5). The composite's charge/guarantee structure
and annual-report-driven disclosure assumptions sit inside this frame.

**AP&P Appendix A-585 — the valuation half, and only that half.** The requirement the
Valuation Manual actually routes a UL reserve to is the AP&P Manual's Appendix A item
**A-585**, now read in full [REG-R155]; the GMP/GMF construction above is therefore
sourced first-hand rather than through the model regulation. Two things the print
settles. It **does not name Model #585 anywhere** — its "Relevant NAIC Model
Laws/Regulations" line names only the **Standard Valuation Law (#820)** — so "A-585
*is* Model 585 Section 5" is unsupported by it, and the two texts were **not compared**
[REG-R155] [REG-R5]. And it carries **definitions and valuation requirements only**: the
nonforfeiture floor, the mandatory policy provisions and the annual report to
policyowners listed in the paragraph above, together with Model #585's separate
interest-indexed UL requirements, are **not** in A-585 and keep citing Model #585
[R1] [REG-R5] [REG-R155]. A-585 prints **no effective date and no number of any kind**;
every rate, table and factor is delegated to Appendix **A-820** by year of issue, so no
applicability date may be read off A-585 itself [REG-R155] [REG-R153].

**IRC 7702 (life insurance definition).** The contract must pass CVAT or the guideline
premium test plus cash value corridor; the composite elects GPT, so the guideline
premium limit and the corridor factor table are contractual mechanics [S3] [R2]. For
contracts issued after 2020-12-31 the fixed statutory rates were replaced by the
dynamic insurance interest rate (2% during the 2021 transition) [R2] [REG-R13]. Exact
statutory wording should be re-verified before hard-coding (research file caveat on
the automated summary) [R2].

**IRC 7702A (MEC).** The 7-pay test with material-change and retroactive-reduction
rules determines MEC status; consequences are distribution taxation changes, not cash
flow changes — the insurer-side behavior in the composite is refund of MEC-causing
premiums absent owner election [S3] [R3] [REG-R14].

**Valuation Manual / VM-20 (PBR).** The Valuation Manual became operative 2017-01-01
and PBR an accreditation standard from 2020-01-01 [R5]; the operative date is printed
in operative rules by the AP&P codification of the Standard Valuation Law — A-820 ¶3
applies the principle-based ¶¶23–27 to policies issued on or after "the January 1,
2017, operative date of the Valuation Manual" and ¶4 keeps earlier issues on ¶¶5–22,
to which those provisions "shall not apply" [REG-R153 ¶¶3–4](#uslib-reg-r153); **the 2020-01-01
accreditation date has no counterpart in A-820, which contains no elective transition,
phase-in or company election at all** [REG-R153]. VM-20 sets principle-based
reserve requirements (net premium reserve plus deterministic/stochastic components
with exclusion tests) for life products including UL [REG-R3]. This library projects
gross liability cash flows only; reserve layers are pointed to, not reproduced (see
technical notes).

**2017 CSO.** The current statutory valuation/nonforfeiture mortality family
(composite and smoker-distinct, loaded/unloaded, preferred structure, ANB/ALB
variants) [R4] [REG-R17]; mandatory for new issues from 2020-01-01, used for reserves,
nonforfeiture, 7702/7702A, and as the cap for UL guaranteed COI rates, terminal age
121 [unverified — from search-result context, not a fetched primary document]. The
specimen's nonforfeiture basis is the earlier 2001 CSO ANB [S3].

**ASOP No. 2 (non-guaranteed elements).** Current credited rate, current COI, and
current loads are NGEs: scales must be based on reasonable expectations of future
experience, revised only when anticipated experience factors change, and not set to
recoup past losses [R8] [REG-R26 same standard](#uslib-reg-r26). This constrains how the model's NGE
re-rating logic may behave.

**Illustrations (Model 582 / ASOP 24).** Sales illustrations for this product operate
under the disciplined-current-scale regime with self-support and lapse-support tests
[R6]. Illustration mechanics are out of model scope but explain why current scales are
publicly illustrated but not guaranteed.

**Reg XXX / AG 38 (secondary guarantees).** Relevant only if the no-lapse guarantee or
a shadow-account endorsement is modeled: Model 830 Section 7 and AG 38 govern reserves
for UL with secondary guarantees on pre-PBR business [REG-R6] [REG-R7]. Excluded with
the NLG (spec footnote 17). A citation caution now that the AP&P print has been read:
the manual's **A-830** is a flat sequence of paragraphs **with no sections at all**, so
a "Section 7" cite does not resolve against it — the ULSG construction sits at
**¶¶29–32** — and the words "Model #830" and "Regulation XXX" appear nowhere in that
print [REG-R154]. A-830 ¶32.b floors the ULSG reserve by the minimum reserves required
by "other appendices governing universal life plans" **without naming the item**, and
that cross-reference must **not** be resolved to A-585 on the A-830 text
[REG-R154 ¶32](#uslib-reg-r154).

**IIPRC uniform standards.** Multi-state UL forms (e.g., the "ICC14"-prefixed form
in [S1]) are filed under the Interstate Compact's uniform standards for individual
flexible premium adjustable life [R10 — located but not read; no facts cited from it](#uslib-universal_life-r10).

**Tax reserves.** IRC 807 defines life insurance tax reserves off the NAIC-prescribed
method (greater of net surrender value and 92.81% of the CRVM/VM reserve, capped at
statutory) [REG-R16] — a downstream consumer of the same projected cash flows.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-universal_life-r1
[R2]: #uslib-universal_life-r2
[R3]: #uslib-universal_life-r3
[R4]: #uslib-universal_life-r4
[R5]: #uslib-universal_life-r5
[R6]: #uslib-universal_life-r6
[R7]: #uslib-universal_life-r7
[R8]: #uslib-universal_life-r8
[REG-R13]: #uslib-reg-r13
[REG-R14]: #uslib-reg-r14
[REG-R153]: #uslib-reg-r153
[REG-R154]: #uslib-reg-r154
[REG-R155]: #uslib-reg-r155
[REG-R16]: #uslib-reg-r16
[REG-R17]: #uslib-reg-r17
[REG-R3]: #uslib-reg-r3
[REG-R5]: #uslib-reg-r5
[REG-R6]: #uslib-reg-r6
[REG-R7]: #uslib-reg-r7
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
