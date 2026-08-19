# Product Specification

**Status:** Draft, 2026-08-03 (underlying research accessed 2026-08-03).

Scope note: this is a **standardized composite specification for reference modeling** — it does
not describe any single insurer's product. It is assembled from the primary and regulatory
sources catalogued in `sources.md` and extracted in `_research/whole-life.md`. Tags
[S#] (primary product documents) and [R#] (regulatory/actuarial references from the product
research file) and [REG-R#] (cross-product reference library,
`references/regulatory-and-actuarial-references.md`; research provenance in
`_research/regulatory-actuarial.md`, same R-numbering) mark sourced facts. **[std]** marks standardizations
introduced for the reference implementation; every **[std]** table row is footnoted with its
rationale and the observed range across insurers. Facts the research file could not verify are
flagged [unverified].

---

## Product overview and market role

Whole life (WL) insurance is permanent life insurance with level guaranteed premiums, a level
guaranteed face amount, and a schedule of guaranteed cash values that reaches the face amount
at age 100 (the endowment-at-100 design), with coverage in current policy forms continuing to a
contractual maturity at age 121 [S1] [S3]. The mainstream U.S. product is **participating**
(par) WL sold predominantly by mutual insurers: policies share in divisible surplus through
annual Board-declared dividends that are not guaranteed [S1] [S3] [S4]. The surveyed mutuals have
paid dividends without interruption for well over a century: one has done so since 1847 [S12],
a second since 1854 [S9], a third since 1868 [S2] and a fourth since 1872 [S4]. That fourth
carrier alone expects a $9.2 billion dividend payout for 2026, of which roughly $7.9 billion
goes to whole life policyowners [S5].

Product menus converge on a common chassis: a level-pay policy (premiums payable to roughly age
95–121), limited-pay variants (10-pay, 12/15-pay, 20-pay, paid-up-at-65), and, at some
carriers, accumulation-oriented short-pay designs (one such design is 10-pay with a $10,000
minimum annual premium at issue ages 0–60 [S10]; another offers payment periods from 5 years
to age 100 [S13]).

A structurally distinct sub-market is **non-participating simplified-issue final-expense (FE)
WL**: small faces ($2,000–$50,000), issue ages 45+, health-question underwriting without exams,
level or graded death benefits, and an explicit policy fee [S6] [S7] [S8]. This library models
both: a primary par design ("RefWL-Par") and a secondary FE variant ("RefWL-FE").

For liability modeling, WL's economics are dominated by the guaranteed cash value schedule, the
dividend scale (interest, mortality, and expense margins under the contribution principle
[S4] [R6]), paid-up additions (PUA) compounding [S14], policy loans with direct recognition
[S1] [S3], and low, level lapse behavior on mature par blocks (see technical notes).

---

## Representative specification

### Primary design: participating level-premium whole life ("RefWL-Par")

#### Table 1 — Chassis and guarantees

| Parameter | Representative value | Basis |
|---|---|---|
| Product type | Participating whole life; level guaranteed premium; level guaranteed face | [S1] [S3] |
| Nonforfeiture/guarantee mortality | 2017 CSO, composite, sex-distinct | [S1]; mandatory for issues on/after 2020-01-01 [R3] |
| Age basis | Age nearest birthday (ANB) | **[std]** (a) |
| Guaranteed interest (CV schedule) | 4.00% per year | [S1]; equals the Model 808 nonforfeiture floor rate [R1] |
| Endowment point | Guaranteed CV = face amount at age 100 | [S1] [S3] |
| Contractual maturity | Anniversary nearest attained age 121; death benefit guaranteed to 121 | [S1] |
| Premium period (base variant) | Level premiums payable to age 100 | **[std]** (b) |
| Limited-pay variants (parameter choices) | 10-pay; 20-pay; paid-up-at-65 | [S1] [S3] |
| Sex-distinct pricing | Yes (unisex in Montana and for tax-qualified business) | [S1] [S3] |

Footnotes:
- (a) **[std]** ANB: the 2017 CSO set is published in both ANB and ALB forms [R8]; the surveyed
  product documents do not state the carrier's age basis. ANB is chosen as the single basis for
  the reference implementation ("anniversary nearest" language in one carrier's maturity
  provision [S1] is consistent with ANB).
- (b) **[std]** pay-to-100: observed level-pay periods are to age 95, 99, or 121 (three
  variants of one carrier's chassis [S1]) and to age 100 (two other carriers [S3] [S12]).
  Pay-to-100 is chosen because it aligns the premium period with the endowment-at-100 cash
  value schedule, which simplifies the reference recursion without misrepresenting any surveyed
  design.

#### Table 2 — Premiums, fees, and underwriting

| Parameter | Representative value | Basis |
|---|---|---|
| Gross premium rates | Input rate table per $1,000 by issue age, sex, class (level, guaranteed) | [S1] [S3]; carrier rate books are non-public — the shipped illustrative table is **[std]** (c) |
| Policy fee | $0 (rates fully banded) | **[std]** (d) |
| Modal factors (× annual premium) | Semi-annual 0.515; quarterly 0.26265; monthly 0.085833 | [S1] (e) |
| Premium mode modeled | Annual | **[std]** (f) |
| Issue ages | Level pay 0–80; 10-pay 0–75; 20-pay 0–70; paid-up-at-65 0–45 | [S1] (another carrier issues 10/12/15/20-pay to 0–75 [S3]) |
| Minimum face amount | $25,000 | [S1] [S3] |
| Representative model-point face | $100,000 | **[std]** (g) |
| Underwriting classes | 3 classes: Preferred Non-tobacco, Standard Non-tobacco, Tobacco | **[std]** (h) |
| Substandard | Out of scope (table extras up to class 16 / table P exist in market) | [S1] [S3] |
| Face banding | Out of scope (premium/dividend rates band by face in market) | [S1] [S3] |

Footnotes:
- (c) **[std]** premium table: par WL gross premium rate books are producer-portal-only for the
  surveyed carriers (research gap). One carrier documents only that basic annual premium varies
  by issue age, sex, class, and band [S3]. The reference implementation treats the gross
  premium as a model-point input; the illustrative value used in the technical notes
  ($18.00 per $1,000 at male NT issue age 45) is **[std]** and not attributable to any carrier.
- (d) **[std]** $0 policy fee: observed range — one carrier charges $0 with "continuous
  banding replicat[ing] a $100 policy fee" [S1]; a second charges $50/yr on three of its
  plans and none on its 10/12/15/20-pay plans [S3]; the FE plan charges $36/yr [S7]. $0
  (the first of those conventions) is chosen so the per-$1,000 premium fully determines
  premium income; the FE variant keeps its explicit $36 fee.
- (e) One carrier's modal factors are adopted as the representative set [S1]; a second
  carrier's are 0.5117 / 0.2589 / 0.0870 [S3] and the FE carrier's 0.52 / 0.275 / 0.089
  [S7] — see Variations.
- (f) **[std]** annual mode: the reference projection is annual (see technical notes); modal
  loadings are a premium-income refinement that does not change the mechanics.
- (g) **[std]** $100,000 model point: inside all observed minimum-face rules ($25,000 general
  minimum [S1] [S3]; $100,000 preferred-class minimum at one carrier [S1]) and used
  consistently in the worked example of the technical notes.
- (h) **[std]** 3 classes: observed structures have 5–6 classes (one carrier: Preferred Plus NT,
  Preferred NT, Non-smoker, Standard Smoker, Rated NT, Rated Smoker [S1]; another: Ultra
  Preferred NT, Select Preferred NT, Non-Tobacco, Select Preferred Tobacco, Tobacco [S3]).
  Three classes preserve the preferred/standard/tobacco distinctions that drive rate and
  dividend variation without carrying carrier-specific class ladders.

#### Table 3 — Dividends

| Parameter | Representative value | Basis |
|---|---|---|
| Participation | Annual dividend, declared by the Board, not guaranteed | [S1] [S3] [S4] |
| Dividend determination | Contribution principle; three-factor formula (interest + mortality + expense margins vs. the guaranteed basis) | [S4] [R6] |
| Dividend interest rate (DIR), 2026 snapshot | 6.00% | **[std]** (i) |
| First dividend | None in policy year 1; first dividend credited at the end of policy year 2 | **[std]** (j) |
| Dividend options modeled | Cash; premium reduction; accumulation at interest; paid-up additions (PUA) | [S2] [S3] [S4] |
| Default dividend option | Paid-up additions | [S1] [S2]; most policyowners elect it at one surveyed carrier [S4] [S5] |
| PUA purchase basis (dividend purchases) | Net single premium at attained age on 2017 CSO / 4.00% (guarantee basis), no purchase load | **[std]** (k) |
| PUAs participate in dividends | Yes | [S14]; CV of PUAs = PUA face at age 100 [S1] |
| Dividend accumulation interest | Credited at the declared DIR (rate declared annually with the scale) | [S2]; modeled at the DIR **[std]** (l) |
| Terminal dividends | Not modeled | **[std]** (m) |

Footnotes:
- (i) **[std]** 6.00% DIR: 2026 declared DIRs observed — 5.75% at one carrier [S4], and
  6.60%, 6.40%, 6.25% and 6.00% at four others [S14, secondary aggregator]. 6.00% sits
  centrally in the 5.75%–6.60% range and gives a clean 2.00% spread over the 4.00%
  guarantee. The DIR is a scale input, not a policy yield: mortality and expense experience
  also drive the dividend [S14].
- (j) **[std]** no year-1 dividend: a real cross-insurer design split — one carrier pays no
  dividend in policy year 1 [S1]; another pays a first-year dividend [S3]. The no-year-1
  convention is adopted because it is the traditional protection-design pattern; switching the
  first-dividend year is a one-parameter change in the model.
- (k) **[std]** unloaded NSP on the guarantee basis: the contractual PUA-purchase basis is not
  published by any surveyed carrier. Using the 2017 CSO / 4% endowment-at-100 net single
  premium makes the PUA cash value reach PUA face at age 100, matching the contractual
  statement that the CV of PUAs equals their face at age 100 [S1]. Purchase loads observed in
  the market apply to PUA **rider** premium payments (7.5%–10% of each payment at one carrier,
  with guaranteed maxima [S3]), not to dividend purchases; the rider load is modeled (Riders).
- (l) **[std]** accumulation at DIR: one carrier declares the accumulation interest rate annually
  with the dividend scale [S2]; no separate rate is published, so the DIR is reused.
- (m) **[std]** no terminal dividends: one carrier's death benefit formula includes "dividends
  credited at death" [S1], but no surveyed source quantifies a terminal dividend scale; omitted.

#### Table 4 — Loans, surrender, and termination provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Policy loan rate | Fixed 6.0% per year in arrears (equivalently 5.66038% payable in advance) | [S1] [S3]; one carrier's contractual 6%→4% late-duration step-down [S1] is not modeled **[std]** |
| Direct recognition | Yes — dividends on loaned values reflect the loan rate | [S1] [S3] |
| Maximum loan | Cash value of base + additions, less existing loans and loan interest to the next anniversary | [S1] |
| Loan interest capitalization | Unpaid interest added to loan principal on the policy anniversary | [S1] |
| Variable-loan-rate alternative | Out of scope (VLR/adjustable-rate regimes without direct recognition exist market-wide) | [S1] [S3] [S9] |
| Withdrawals / partial surrender | Surrender of paid-up additions (no base-policy partial withdrawal) | [S9]; mechanics **[std]** (n) |
| Grace period | 31 days | [S1] [S3] |
| Automatic premium loan (APL) | Available; loans premium due if CV sufficient | [S1] |
| Nonforfeiture options | Cash surrender; reduced paid-up (RPU); extended term insurance (ETI) | [S3] [R1] |
| Automatic nonforfeiture option | Extended term insurance | **[std]** (o) |
| Reinstatement | Within 5 years of default, evidence of insurability, arrears with 6% compound interest | [S1] [S3] |
| Suicide/contestability | Standard 2-year provisions | [S7 for the FE forms]; par contract wording not captured — **[std]** (p) |
| Free look | 10 days (state variations) | [S1] |

Footnotes:
- (n) **[std]** withdrawal mechanics: one carrier documents that "surrenders" on its WL are
  surrenders of paid-up additional insurance [S9]; the exact ordering rules are contract
  wording not captured in the research file. The reference model implements partial surrender
  as surrender of PUA face at its cash value (see technical notes).
- (o) **[std]** ETI as automatic option: one carrier's lapse provision applies the nonforfeiture
  option "elected at issue" [S1]; no surveyed document states a default. ETI is adopted as the
  automatic option in the reference contract; RPU-at-election is also modeled.
- (p) **[std]** 2-year suicide/contestability: verified only for the FE forms (2 years; 1 year
  in ND [S7]). Applied to the par design as a standardization; immaterial to cash flow
  projection at the modeled granularity.

### Secondary design: non-participating simplified-issue final-expense WL ("RefWL-FE")

Parameterized from the FE carrier's simplified-issue plan (level and graded benefit
variants) [S6] [S7] [S8].

#### Table 5 — RefWL-FE

| Parameter | Representative value | Basis |
|---|---|---|
| Participation | Non-participating | [unverified] — no retrieved document for this plan mentions dividends [S6] [S7] [S8]; modeled non-par (q) |
| Underwriting | Simplified issue: health questions, Rx/MIB checks, tele-interview; no exams | [S6] [S7] |
| Level plan | Issue ages 45–85; face $2,000–$50,000 ($5,000 min in WA; $2,000–$40,000 in CA) | [S6] [S7] [S8] |
| Graded plan | Issue ages 45–80; face $2,000–$20,000 | [S6] [S7] |
| Graded death benefit | Natural-cause death in policy years 1–2 pays 110% of premiums paid; accidental death pays full face from day 1 | [S6] [S7] |
| Classes | Level: Standard Tobacco / Non-tobacco; Graded: single Standard class | [S7] |
| Sample annual premium rates per $1,000 | Level male NT: age 45 $24.99, age 65 $59.05, age 85 $202.19; Level female NT age 65 $42.48; Graded male age 65 $103.00, female age 65 $69.50 | [S7] (California edition) |
| Policy fee | $36 per year, added to all premiums | [S7] |
| Modal factors | Semi-annual 0.52; quarterly 0.275; monthly 0.089 | [S7] |
| Guaranteed values | Builds cash value (loanable); premiums never increase; benefits never decrease | [S8]; CV basis not published — **[std]** (r) |
| Maturity | Age 100 (120 in FL); face less loans and loan interest paid at maturity | [S8] |
| Suicide exclusion | 2 years (1 year in ND); return of premium less loans | [S7] |
| Representative model point | Male NT, issue age 65, $15,000 level plan: annual premium 15 × $59.05 + $36 = $921.75 | [S7] rates; model-point choice **[std]** (s) |

Footnotes:
- (q) Participation status is a research gap: final-expense WL from the FE carrier is
  generally non-participating [unverified]. Modeled as non-par; confirm from a specimen
  policy.
- (r) **[std]** FE guaranteed CV basis: no CV table or basis is published in the retrieved
  documents. The reference implementation reuses the RefWL-Par nonforfeiture machinery
  (2017 CSO / 4%, endow at 100) for the FE variant's CV schedule as a standardization.
- (s) **[std]** model point: age-65 male NT at $15,000 sits centrally in the issue-age and
  face ranges [S6] [S7]; the premium is computed from the sourced CA rate table [S7].

---

## Contractual mechanics

Notation here is shared with the technical notes: policy year `t = 1, 2, …`, issue age `x`,
face `F`, gross annual premium `G`, guaranteed cash value at the end of year `t` `CV_t`,
dividend `D_t`, PUA face `PUAF_t`, PUA cash value `PUACV_t`, loan balance `L_t`.

### Premium provisions

Premiums are level and guaranteed for the premium period (to age 100 in the base variant; 10
or 20 years, or to age 65, in the limited-pay variants) **[std choice of menu]** [S1] [S3].
Modal premiums equal the annual premium times the modal factor (Table 2) [S1]. Nonpayment
within the 31-day grace period lapses the policy into the nonforfeiture provision [S1]; if APL
is elected and loan value is sufficient, the premium is loaned instead [S1].

### Death benefit provisions

Following one carrier's contractual formula [S1]:

```
DB_t = F                                  (base face)
     + PUAF_t                             (paid-up additions face)
     + term rider face (if any)
     + dividend accumulations (option C balances)
     + dividends credited at death        (not modeled — [std], Table 3 note (m))
     + unwaived premium refund beyond month of death (not modeled — [std])
     − L_t − accrued loan interest
     − premium due and unpaid
     − accelerated benefits previously taken
```

In the reference model with the PUA dividend option: `DB_t = F + PUAF_t − L_t` **[std]**
(simplification of the [S1] formula to the modeled components).

### Guaranteed cash value mechanics

Guaranteed cash values are contractual, printed in the policy, and must be at least the
Standard Nonforfeiture Law minimum: cash surrender value ≥ present value of future guaranteed
benefits (including existing paid-up additions) minus the present value of future adjusted
premiums, minus indebtedness [R1]. Adjusted premiums are a uniform percentage of gross premiums
such that their present value at issue equals the present value of guaranteed benefits plus the
statutory acquisition-expense allowance: 1% of the amount of insurance plus 125% of the
nonforfeiture net level premium, with the NNLP capped at 4% of the amount [R1]. The
nonforfeiture basis for current issues is 2017 CSO mortality [R3] at the Valuation-Manual
nonforfeiture interest rate (historically 125% of the statutory valuation rate, floored at
4.00% [R1]); the representative contract uses 4.00% [S1].

Contractually: `CV_t` grows on the guarantee basis and equals `F` at age 100 [S1] [S3];
`PUACV_t` equals `PUAF_t` at age 100 [S1]. The reference model reads `CV_t` from a table input
generated on the 2017 CSO / 4% basis (technical notes give both the conceptual formula and the
practical treatment).

### Dividends and credits

Dividends are declared annually by the Board and are not guaranteed [S1] [S3] [S4]. The
determination follows the contribution principle: divisible surplus is allocated to policies in
proportion to their contribution to it [R6]. One carrier's published mechanics are the
model's anchor: the annual dividend equals the excess of an experience-based accumulated
value — beginning guaranteed value plus premium, less a mortality-and-expense charge based on
actual company results, accumulated at the dividend interest rate — over the ending guaranteed
value [S4]. Equivalently, a three-factor formula with interest, mortality, and expense margins
against the guaranteed basis; the exact carrier parametrizations are proprietary, so the
reference parametrization is **[std]** (technical notes). Dividend scales vary in practice by
sex, class, band, issue age, duration, and loan status under direct recognition [S3] [S1].

Dividend options (union across carriers, [S2] [S3]): cash; reduce premium (excess to cash or to
PUAs); accumulate at interest (rate declared annually); paid-up additions (default [S1] [S2]);
one-year term variants (OYT up to cash value, up to 2× face, or to a target face with PUA
balance — six lettered dividend options at one carrier [S2]; at another, OYT = guaranteed CV
via a term-purchase rider [S3]); premium offset [S2] [S3]; loan/loan-interest repayment
[S2] [S3]. The reference model implements cash, premium reduction, accumulation, and PUA
(Table 3).

Each dollar of dividend under the PUA option buys `1 / NSP_{x+t}` of paid-up face, where
`NSP_{x+t}` is the attained-age net single premium on the guarantee basis **[std]** (Table 3
note (k)). PUAs are themselves dividend-eligible [S14], increase the death benefit dollar-for-
dollar of face, and are surrenderable at their cash value [S9]**/[std]**.

### Policy loans

Loans are available at any time (including policy year 1) up to the cash value of base plus
additions less loans and loan interest to the next anniversary [S1]. The representative loan
rate is fixed 6% in arrears (5.66038% in advance) with **direct recognition**: dividends on
loaned values reflect loan-rate interest rather than the portfolio DIR [S1] [S3]. Unpaid loan
interest capitalizes on the anniversary [S1]. Loans and accrued interest reduce death proceeds
and surrender values [S1] [S3] [S9]. Market alternatives — one carrier's electable variable loan
rate (Moody's-linked, 4.5% floor, no direct recognition) [S1] and another's default
adjustable loan rate (no direct recognition) [S3] — are out of scope. Sustained heavy loan
utilization can trigger overloan protection mechanics (one carrier's rider: forced RPU when the
loan exceeds 99% of CV, insured ≥ 75, duration ≥ 15) [S11]; not modeled.

### Grace, lapse, and reinstatement

31-day grace [S1] [S3]. On default, the elected (or automatic **[std]**) nonforfeiture option
applies: cash surrender (`CV_t + PUACV_t + dividend accumulations − L_t`), reduced paid-up
(face = surrender value divided by the attained-age NSP), or extended term insurance (level
term of face `DB_t − L_t` for the duration purchasable by the surrender value at the
attained age) [S3] [R1]; the paid-up benefit must be at least actuarially equivalent to the cash
surrender value [R1]. Reinstatement within 5 years with evidence of insurability and payment of
arrears with 6% compound interest [S1] [S3].

### Maturity, conversion, and exchanges

The contract matures on the anniversary nearest age 121 [S1]; the guaranteed CV equals face at
age 100 and the PUA CV equals PUA face there [S1], so from age 100 the policy is economically
an endowment riding at face. The reference model pays `F + PUAF` as a maturity benefit at age
100 and terminates **[std]** (technical notes). Term-to-WL conversions are permitted market
practice [S1] and enter the model only through model-point provenance; 1035 exchanges [S1] [S3]
are out of scope.

---

## Riders

### In scope

- **Paid-up additions rider (flexible PUA purchases).** Policyowner payments (scheduled plus
  catch-up/unscheduled) purchase paid-up additions directly. Observed mechanics: one carrier's
  rider — expense charge 7.5% of each payment on 10/15-pay, 10% on other products, guaranteed
  maximum at the same level; minimum initial scheduled payment $300/yr; +10%/yr increases
  without evidence up to 100% cumulative [S3]; another carrier's PUA riders cap payments at
  an Annual Payment Limit set at issue [S11]. Reference parametrization: PUA rider premium
  `A_t` buys `A_t × (1 − 0.10) / NSP_{x+t−1}` of paid-up face (BOY payment, attained age
  `x+t−1`) — a 10% load **[std]** chosen from the observed 7.5%–10% current-charge range
  [S3] (guaranteed maxima equal the current charges at that carrier [S3]). Rider PUAs merge
  into the same PUA account as dividend PUAs.
- **Term-blend rider (target face with crossover).** A one-year-term plus PUA blend maintains a
  Target Face Amount: each year the dividend (plus rider premium) first buys OYT for the gap
  between target and permanent face, remainder buys PUAs; as PUAs grow, term is displaced until
  crossover to fully paid-up coverage. Observed: two lettered dividend options at one carrier
  (target ≤ 9× base; increasing-target variant) [S2]; a blend rider at a second (target ≤ 300%
  of base, expense charge current 8–10% capped 10–12%, requires a companion dividend option)
  [S3]; and a term-and-PUA blend rider at a third [S11]. The reference model implements a
  simplified blend (technical notes) with target = 2× base face **[std]** (inside all
  observed caps).

### Out of scope (present in market, listed for completeness)

Waiver of premium on disability (6-month wait, own-occ definitions, terminates ~65)
[S1] [S3] [S11]; accidental death benefit [S6] [S11]; guaranteed insurability / purchase options
[S3] [S11]; children's term [S11]; accelerated death benefit for terminal illness (near-
universal, 12-month prognosis) [S6] [S11] [S12]; chronic illness / LTC acceleration and LTC
riders with lien mechanics [S3] [S11] [S12]; index participation features [S1]; overloan
protection [S11]; exchange-of-insured and other business riders [S1] [S3] [S11]; FE accidental
death rider (additional DB = face) [S6].

---

## Variations across insurers

1. **Premium period menus** differ but converge on level-pay-to-~100/121 plus {10, 12/15,
   20}-pay plus paid-up-at-65; every surveyed carrier offers a 10-pay [S1] [S3] [S10] [S13].
   Representative choice: pay-to-100 base + 10/20/65 variants — the intersection of the menus.
2. **Guaranteed CV interest**: one rate for all products at one carrier (4%) vs. product-specific
   2%–3.75% at another (with 0% after age 100) [S1] [S3]. The guarantee rate must therefore
   be a per-product model parameter. 4.00% chosen: it is the first carrier's contractual basis
   and the Model 808 floor [S1] [R1].
3. **First-year dividend**: paid by one carrier [S3], not paid by another [S1]. Chosen: none in
   year 1 (Table 3 note (j)).
4. **Loan regimes**: fixed-with-direct-recognition vs. variable/adjustable-without-direct-
   recognition; one carrier defaults to fixed 6% with DR (VLR electable at year 10) [S1],
   a second defaults to ALR without DR (fixed 6% + DR electable at issue) [S3], and a third's
   loan rate is variable [S9]. Direct recognition is always paired with the fixed rate
   [S1] [S3]. Chosen: fixed 6% with DR — it is the regime that interacts with the dividend
   scale and therefore the one worth modeling explicitly.
5. **Dividend banding** by face exists at one carrier (level-pay, $1M+) and at another (all
   products, multiple bands) [S1] [S3]. Not modeled: a single-band reference policy avoids
   carrying band schedules.
6. **Term-blend mechanisms** are universal but carrier-named — three of the surveyed carriers
   each brand their own [S2] [S3] [S11]; a single generic blend rider represents them.
7. **Policy fee**: $0 / $50 / $36 observed [S1] [S3] [S7] — see Table 2 note (d).
8. **Accumulation-oriented WL** (short-pay, early-CV designs at three of the surveyed carriers
   [S3] [S9] [S10] [S13]) is represented only through the 10-pay variant; early-CV
   enhancement mechanics are not separately modeled.
9. **FE WL** differs structurally (tiny faces, 45+ issue, simplified issue, graded DB tier,
   explicit fee, endow at 100, no dividends mentioned) [S6] [S7] [S8] — hence the separate
   RefWL-FE variant rather than parameter overrides on RefWL-Par.

---

## Regulatory context

**Standard Nonforfeiture Law (NAIC Model 808).** Sets the minimum cash surrender values and
paid-up nonforfeiture benefits that define WL's guaranteed value floor: the adjusted-premium
method with the 1%-of-amount + 125%-of-NNLP expense allowance, actuarial equivalence of
paid-up options, smooth progression of CV schedules, and the nonforfeiture interest rule
(historically 125% of the valuation rate, min 4.00%; Valuation-Manual-prescribed for current
issues) [R1]. The representative 4%/2017 CSO guarantee basis is exactly this law's current
operative basis [S1] [R1] [R3].

**Standard Valuation Law (NAIC Model 820) and the Valuation Manual.** Model 820 is the legal
root of statutory reserving (CRVM, minimum standards, and — post-2009 amendments — the
principle-based valuation sections that make the Valuation Manual operative) [REG-R1]. The
law is codified in the AP&P Manual as **Appendix A-820**, which has now been read in full and
supplies what this library previously took at one remove [REG-R153]. Its **¶11 prints the CRVM
this product runs on** — modified net premiums as a uniform percentage of the respective
contract premiums, an expense allowance capped at the net level annual premium on the
**nineteen-year premium whole life plan at an age one year higher than the issue age**, and a
reserve that is "the excess, **if any**" — with no discrepancy against the Model 820 print
[REG-R153 ¶11](#uslib-reg-r153). Its **¶¶7–10 make the valuation interest rate computable** rather than merely
named: `I = .03 + W(R1 − .03) + (W/2)(R2 − .09)` rounded to the nearer quarter of 1%, on the
lesser of the 36- and 12-month Moody's seasoned-corporate-bond averages ending June 30 of the
year *preceding* issue, with `W` from the ¶8.a life table by **guarantee duration** — .50 to
10 years, .45 over 10 to 20, .35 over 20 — and a life-only half-of-1% stability rule against
the published prior-year rate [REG-R153 ¶¶7–10](#uslib-reg-r153). `W` is a per-model-point lookup, not a product
constant: RefWL-Par runs to maturity at 121 and always takes .35, while RefWL-FE matures at 100,
so its issue ages 80–85 fall in the .45 band.
Its **¶16** is the aggregate nonforfeiture-basis floor, aggregate rather than seriatim and
excluding disability and accidental death benefits [REG-R153 ¶16](#uslib-reg-r153). Two limits stay: **A-820
never names the 2017 CSO** — ¶5.a prescribes the 2001 CSO for standard-basis ordinary issues
from 1 January 2004, later tables entering only through its forward reference or through the
Valuation Manual (¶23), so this product's 2017 CSO basis is sourced to VM-02 [R3], not to
A-820; and A-820 carves **preneed** policies out to **Appendix A-817**, which was **not
retrieved** [REG-R153 ¶5](#uslib-reg-r153) [REG-R110]. For ordinary life issued on/after 2020-01-01 — the PBR
*accreditation* year; the trigger A-820 ¶¶3–4 actually print is issue **on or after 1 January
2017**, with earlier issues grandfathered onto ¶¶5–22 and the PBR provisions stated not to
apply to them, and with **no elective transition, phase-in or company election anywhere in
A-820** [REG-R153 ¶¶3–4](#uslib-reg-r153) — VM-20 governs: a seriatim net premium reserve on
2017 CSO, plus deterministic and stochastic reserves unless exclusion tests are passed;
traditional par WL typically passes the deterministic exclusion test because valuation net
premiums do not exceed the substantial guaranteed gross premiums, leaving NPR-only blocks
[R3]. Companies under the Life PBR Exemption (< $300M individual life premium) value under
VM-A/VM-C (pre-PBR CRVM) [R3]. VM-02 prescribes minimum nonforfeiture mortality/interest
(2017 CSO mandatory from 2020; preferred-structure tables prohibited for nonforfeiture) [R3].

**Illustrations (NAIC Model 582; ASOP 24).** Par WL dividend illustrations are constrained by
the disciplined current scale (based on actual recent experience, certified annually by the
illustration actuary), the illustrated scale being no more favorable than the lesser of DCS
and the currently payable scale, and the self-support and lapse-support tests [R2]. Dividend
accumulation credits in illustrations cannot exceed the DCS earned rate [R2]. ASOP 24 governs
the illustration actuary's certification practice [REG-R30]. These rules discipline the
non-guaranteed scale a model may treat as "current."

**Dividend and NGE standards (ASOP 15; ASOP 2).** ASOP 15 requires the contribution principle
for allocating divisible surplus and frames dividend-scale determination and disclosure [R6].
ASOP 2 governs non-guaranteed elements other than dividends (e.g., indeterminate-premium
non-par WL) and explicitly excludes policyholder dividends [R7] — relevant to the RefWL-FE
variant only if its premiums were indeterminate (they are guaranteed level here [S6]).

**Federal tax (IRC §7702, §7702A, §807).** §7702 requires CVAT or GPT-plus-corridor
compliance; for contracts issued after 2020 the fixed 4%/6% test rates are replaced by the
lower "insurance interest rate" (2% transitional for 2021), which raised permissible WL
funding levels [R4]. §7702A's 7-pay test makes limited-pay WL and PUA-rider funding the main
MEC risk: 10-pay premiums sit near 7-pay limits and face decreases can retroactively create
MECs [R5] [S3]; carriers administer 7-pay premiums on 2017 CSO [S1]. §807 defines tax reserves
as the greater of net surrender value and 92.81% of the CRVM/VM reserve, capped at statutory
[REG-R16] — one reason the statutory projection engine also feeds the tax basis.

**Experience/table infrastructure.** The 2017 CSO set (valuation and nonforfeiture) is
published by the SOA in composite/smoker-distinct/preferred-structure, ANB/ALB variants [R8];
the 2015 VBT and ILEC studies provide the experience bases for best-estimate assumptions
[REG-R18] [R9] (see technical notes).

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-whole_life-r1
[R2]: #uslib-whole_life-r2
[R3]: #uslib-whole_life-r3
[R4]: #uslib-whole_life-r4
[R5]: #uslib-whole_life-r5
[R6]: #uslib-whole_life-r6
[R7]: #uslib-whole_life-r7
[R8]: #uslib-whole_life-r8
[R9]: #uslib-whole_life-r9
[REG-R1]: #uslib-reg-r1
[REG-R110]: #uslib-reg-r110
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
[REG-R18]: #uslib-reg-r18
[REG-R30]: #uslib-reg-r30
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
