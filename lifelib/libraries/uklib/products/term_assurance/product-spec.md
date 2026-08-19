# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/term-assurance.md` and resolved in
`sources.md` (same directory; numbering frozen, never renumbered), and [REG-R#] (the
cross-product reference library `references/regulatory-and-actuarial-references.md`,
whose own R-numbering is distinct; research provenance in
`_research/regulatory-actuarial.md`) — were extracted from the cited document. Values
marked **[std]** are standardizations introduced for the reference implementation; each
[std] table row carries a footnote giving the rationale and the observed range across
insurers. Facts the research file could not verify are flagged [unverified]. The
composite is drawn from three insurers' current retail products: one carrier's four
separate level, decreasing, increasing and family-income products [S1]–[S5], a second
carrier's single combined life policy [S6] [S7], and a third carrier's menu-plan life
cover [S8] [S9].

---

## Product overview and market role

UK term assurance is long-term insurance business, Regulated Activities Order Class I
"Life and annuity" — contracts of insurance on human life [R6]. It is a pure protection
product: a guaranteed level premium buys a death benefit for a fixed term, with **no
savings or investment element, no surrender value, and no paid-up value** — if premiums
stop, the policy lapses and nothing is payable regardless of how long it was held
[S6] [R8]. The FCA's market taxonomy distinguishes level term assurance, decreasing term
assurance (commonly tracking a repayment mortgage), increasing term assurance,
renewable term assurance, and family income benefit — the last described by the FCA as
"an ongoing monthly income" that "can be considered as a decreasing term assurance"
[R8].

Term assurance was the most purchased UK pure protection product in 2023: 436,000 new
term assurance policies were issued (against 1,065,000 new accelerated critical illness
policies) and 3.119m term assurance policies were in force; the top 5 insurers wrote
approximately 80% of new business premiums, and 79–87% of mortgage-related term
assurance over 2021–24 [R8]. The ABI average term assurance claim value in 2023 was
£54,600 [R8]. Distribution is intermediary-dominated with ~96% of commission paid
upfront, clawback periods of 2–4 years, and insurer Distribution Quality Management
systems tracking lapses [R9]. Reinsurers take a substantial share of the mortality risk
and influence pricing and product design [R8]; the frequently cited 70–90%+ cession
range is [unverified].

All three sourced insurers embed terminal illness cover (accelerated payment of the
death benefit on a sub-12-month life expectancy) at no extra cost [S1] [S6] [S8] [R8], and
all three guarantee premiums for life-only cover [S2] [S6] [S9]. **A key contrast with US
term life:** the UK policy simply expires at the end of the term. There is no US-style
post-level-term annually-renewable tail, and renewal/conversion options are not
standard in the current UK retail market (see Contractual mechanics — Expiry).

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Guaranteed-premium term assurance; non-participating; no cash values | [S2] [S6] [S9] [R8] |
| Benefit shape (model-point parameter) | (i) level lump sum; (ii) decreasing lump sum (mortgage protection); (iii) family income benefit (FIB, monthly income) | [S2] [S6] [S8]; packaging **[std]** (1) |
| Lives basis | Single life, or joint life first death (optional) | [S1] [S2] [S6]; scope **[std]** (2) |
| Regulatory class | Long-term insurance, Class I (life and annuity) | [R6] |
| Entry ages | 18–77 (decreasing: 18–74; FIB: 18–64) | [S2] [S3] [S7]; envelope **[std]** (3) |
| Maximum expiry age | 90th birthday (FIB: 70th birthday) | [S2] [S3] [S7]; envelope **[std]** (3) |
| Policy term | 1–50 years (decreasing: 5–50; FIB: 5–40); terminal illness cover requires term ≥ 2 years | [S2] [S4] [S7]; envelope **[std]** (3) |
| Maximum sum assured | £10,000,000 level/decreasing (subject to underwriting); FIB £10,000/month | [S2] [S4]; adoption **[std]** (4) |
| Minimum premium | £5/month | [S5]; adoption **[std]** (5) |
| Residence at outset | UK resident (one carrier: living in the UK ≥ 183 days in the last tax year; another also admits Channel Islands/Isle of Man/Gibraltar) | [S1] [S6] |
| Anchor model cell | Male 35 non-smoker, single life, level shape, term 25 years, sum assured £150,000, premium £12.00/month | **[std]** (6) |

Footnotes to [std] rows:

1. Packaging varies: one carrier writes one policy with three payout bases [S6] [S7];
   a second, a menu plan with five payout shapes (level/increasing/decreasing lump sum,
   level/increasing income) [S8]; the third sells the shapes as four separate
   products [S2]. The composite treats benefit shape as a model-point parameter with
   three values (increasing-shape products are represented via the indexation option
   instead).
2. Joint life first death is the standard joint basis across all three insurers
   [S1] [S2] [S6]. One carrier additionally writes dual life and joint life second event
   [S9]; both are excluded from the composite.
3. Envelope = the limits of two of the three carriers, which agree closely (entry to
   77, expiry by 90, terms 1–50 [S2] [S3] [S7]); FIB limits per the family-income
   product of one of them (entry to 64, expiry by 70, terms 5–40 [S2] [S4]). The third
   carrier is materially wider (entry 18–88, expiry to 89, terms 1–72 [S9]) and is
   treated as an outlier. The minimum-expiry-age-29 rule seen at one carrier [S2] [S3]
   is unique to it and not carried into the composite. Terminal illness cover is not
   provided on that carrier's 1-year (2-year increasing-shape) minimum terms [S2]; TIC
   automatic for terms of 2+ years [S4].
4. One carrier publishes £10m (level/decreasing), £4m increasing, £10,000/month family
   income (£4,000 with CI) [S2] [S4]; a second publishes no monetary maximum [S6]; the
   third is unlimited (£5m cap with the increasing option) [S9].
5. Only one carrier publishes a value ("Cover from only £5 a month", "Fixed premiums
   from £5 a month") [S5]; another references a "minimum premium limit" without a
   public value [S6]; the often-quoted market range of £5–£10/month is [unverified].
6. Premium rates are not public — retail premiums are quote-engine outputs, and no
   insurer publishes per-mille rate tables (research gap; the per-mille
   characterisation of UK protection pricing is itself [unverified]). The £12.00/month
   anchor premium is a pure modeling value. Sum assured £150,000 is a round-number
   standardization; the ABI average term claim of £54,600 (2023, whole in-force) [R8]
   anchors the order of magnitude, with new mortgage-related business typically larger.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level, guaranteed for the full policy term (life-only cover) | [S2] [S6] [S9] |
| Frequency | Monthly (annual available); composite default monthly | [S1] [S6]; default **[std]** (7) |
| Payment method | Direct debit, in sterling (one carrier: from a UK, Channel Islands, Isle of Man or Gibraltar bank account) | [S6] |
| Rating factors | Age, smoker status, health, lifestyle, occupation, type/amount of cover; gender-neutral | [S7] [R8]; gender neutrality [unverified] (8) |
| Rate structure | Not public (quote-engine pricing); the office premium is a model-point input, backed by a **[std]** mortality proxy basis in the technical notes | gap; **[std]** (8) |
| Annual-mode refund at claim | One carrier refunds the remaining months' premium in the policy year on a full-cover claim; not modeled | [S1]; scope **[std]** (7) |

7. Monthly direct debit is the dominant retail mode (one carrier requires direct debit
   [S6]); the composite standardizes on monthly and ignores the annual-mode claim-time
   refund [S1] and that carrier's deduction of grace-window unpaid premiums from claims
   [S6] as immaterial modal refinements.
8. Disclosed rating factors: one carrier lists age, occupation, health, lifestyle,
   smoking habits, type and amount of cover [S7]; FCA adds that reinsurers shape
   risk-based adjustments [R8]. None of the three insurers lists sex as a rating
   factor, but the gender-neutral pricing requirement itself was not confirmed from a
   fetched document [unverified]. No insurer publishes premium rate tables — the
   technical notes specify a [std] mortality proxy basis from public tables and take
   the office premium itself as a model-point input (no premium-rate table is
   constructed).

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Death benefit — level shape | Sum assured, constant | [S1] [S6] |
| Death benefit — decreasing shape | Outstanding balance of a notional capital-and-interest (repayment) mortgage, decreasing monthly at schedule rate `j` | [S1] [S6] [S8] |
| Decreasing schedule rate `j` | Client-selected at outset; representative default 6% p.a. | observed range [S4] [S8] [S9] [S6]; pick **[std]** (9) |
| Death benefit — FIB shape | Monthly income `I` from death (paid in arrears) to the end of the term; representative `I` = £1,000/month | [S2] [S6] [S8]; value **[std]** (10) |
| FIB commutation | Remaining instalments commutable to a lump sum, reduced "fairly and reasonably" for early payment | [S6] [S8] |
| Terminal illness benefit | 100% acceleration of the death benefit on a two-limb definition: (i) no known cure / progressed beyond cure, and (ii) consultant's opinion of death expected within 12 months; amount = cover calculated at the date the definition is met; included at no extra cost, terms ≥ 2 years | [S1] [S6] [S8] [R8]; term floor [S2] [S4] |
| Suicide exclusion | No payment if death results from suicide or intentional self-inflicted injury within 12 months of commencement; the only standard exclusion | [S1] [S6] [S8] |
| Other exclusions | None standard; case-by-case underwriting exclusions may appear in the policy schedule | [S1] [S3] |
| Payout ends the policy | Policy terminates on payment of the (single) main benefit; joint policies pay once | [S1] [S6] [S8] |
| Expiry | Cover ceases at the end of the term; no maturity value, no renewal, no conversion | [S1] [S2] [S6] [S8] [R8] |

9. Observed: one carrier — the client chooses the decreasing rate from 5%, 7%, 8% or
   10% [S4], the rate appearing in the policy schedule [S1]; a second — default
   schedule at a yearly rate of 6%, or a chosen rate in 0%–15% where the
   mortgage-interest-rate feature applies [S8] [S9]; the third — a fixed rate set at
   application and shown in the schedule, value/range not published [S6] [S7]. 6% is
   chosen as the representative default because it is the only observed insurer
   *default* [S8] and sits inside both the first carrier's menu range (5–10%) [S4] and
   the second carrier's selectable range [S8] [S9]. Two of the three carriers warn that
   cover may not repay the mortgage if the actual loan rate exceeds the schedule rate
   [S1] [S3] [S8].
10. FIB benefit is expressed as a monthly amount [S6]; one carrier's family-income
    product caps it at £10,000/month (£4,000 with CI) [S2]. £1,000/month is a
    round-number modeling value (£12,000/year, same order as the anchor lump-sum cell
    over a mid-length run-off).

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| Indexation (RPI) option | At each anniversary, cover increases by the 12-month RPI change, capped at 10%; no increase if RPI ≤ 0%; premium increases by 1.5 × the cover increase %, capped at 15%; option removed after 3 consecutive declines | [S1] [S2] [S6] [S7]; composite **[std]** (11) |
| FIB under indexation | Fixed 3%/5% escalation variants exist with instalments continuing to increase during payment; excluded from the composite | [S6] [S7]; scope **[std]** (11) |
| Guaranteed insurability option (GIO) | On life events (marriage/civil partnership, divorce/dissolution, birth/adoption, mortgage increase, salary increase): increase without further underwriting, capped at the lower of 100% of original cover and £200,000 across all exercises; exercise within 6 months of the event; all lives under 55; written as a new policy at then-current rates | [S1] [S6]; composite **[std]** (12) |
| Waiver of premium (WOP) | Optional, extra premium; premiums waived after a 26-week deferred period of incapacity (own-occupation definition, specified-work-tasks fallback), until recovery, claim, or expiry | [S1] [S2]; composite **[std]** (13) |

11. Observed indexation bases: one carrier — RPI, no increase if the change is below
    1%, cover cap 10%, premium × 1.5 capped 15% [S1] [S2]; a second — RPI (measured
    over the 12 months ending 12 weeks before the anniversary month) capped 10% with
    premium × 1.5 capped 15%, or fixed 3%/5%, RPI ≤ 0% → no change [S6] [S7]; the third
    — RPI with a minimum of 2% and maximum of 10%, or fixed 2–5%, premium × 1.2
    [S8] [S9]. The composite takes RPI/10%-cap/×1.5/15%-cap (the mode of the first two
    [S1] [S2] [S6] [S7]), the ≤ 0% floor of the second [S6], and the
    3-consecutive-declines removal rule (the first two; the third removes after 2
    [S8]). The second carrier's FIB-shape escalation uniquely carries no premium
    increase [S6]; the third's income shapes increase premiums × 1.2 [S8]; both
    excluded.
12. Observed GIO caps: one carrier — lower of 100% of original cover and £200,000,
    events exercised within 6 months, not after age 55 [S1] (family-income variant
    capped at £1,400/month [S2]); a second — total across exercises lower of
    original cover and £200,000 (FIB: £8,000/year equivalent), new policy within 180
    days of the event, repeatable until 55 [S6]; the third — lowest of half the
    original cover and £200,000 (income covers: £10,000/year) [S8]. The composite
    takes the £200,000/100% cap and 6-month window; all three implement the increase
    as a separate policy at then-current rates [S1] [S6] [S8].
13. Observed WOP: one carrier — 26 consecutive weeks of incapacity before waiver;
    own-occupation, or 3-of-6 specified work tasks if not in paid work [S1] [S2];
    a second — deferred period per the policy schedule; own-occupation, or 2-of-6 work
    tasks where work stopped > 12 months before; claims to age 71 [S6] [S7]; the third
    — no WOP exists on the plan (zero occurrences in the 84-page plan details)
    [S8]. The composite includes WOP as an optional rider with the first carrier's
    26-week deferred period [S1] (the only concretely published deferral).

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender value | None ("This isn't the kind of policy that you can 'cash in'") | [S6] [R8] |
| Paid-up value | None | [S1] [S6] [S8] |
| Grace period | 60 days from each due date; claims in the window paid net of unpaid premiums; cancellation (lapse) after 60 days, no refund | [S1] [S6] |
| Cooling-off | 30 days from commencement, full premium refund | [S1] [S6] |
| Reinstatement | No general contractual reinstatement right in the fetched conditions; not modeled | scope **[std]** (14) |
| Misrepresentation remedies | Careless: policy amended to the terms that would have applied — if higher premiums would have applied, cover reduced to (premium actually charged × original cover ÷ higher premium); deliberate/reckless: cancellation and refusal of claims | [S1]; statutory frame [REG-R20] |

14. One carrier's suicide clause runs "from the date cover started or restarted"
    [S8], implying some restart mechanism, but no fetched document sets out a general
    reinstatement provision; the composite terminates lapsed policies finally.

---

## Contractual mechanics

### Premium provisions

The office premium is level and guaranteed for the full term for life-only cover
[S2] [S6] [S9]: monthly premium `P_m` (composite default mode), annualized premium
`P_a = 12 × P_m` **[std annualization for the annual-grid model]**. Premiums are due
monthly by direct debit [S6]; a 60-day grace period applies from each due date, after
which the policy is cancelled with no refund and no residual value [S1] [S6]. There are
no premium reviews on the composite: reviewable premiums exist in the market only on
critical illness covers attached to these chassis [S2] [S6] [S8], which are out of
scope. If the indexation option is exercised, the premium increases by 1.5 × the
applied cover increase percentage (cap 15% p.a.) — the only in-force mechanism by
which the premium can change, apart from policyholder-requested alterations, which
are out of scope [S1] [S2] [S6].

### Death and terminal illness benefit

Let `n` = term in years, `N = 12n` months, `k` = completed policy months at the date
of claim, `SA0` = initial sum assured.

**Level shape.** Benefit `DB = SA0` (times the cumulative indexation factor if the
option is exercised) [S1] [S6].

**Decreasing shape (mortgage protection).** The benefit is the outstanding balance of
a notional repayment (capital-and-interest) loan of `SA0` over `N` months at the
schedule rate, decreasing monthly, while premiums stay level [S1] [S6] [S8]:

    j_m = (1 + j)^(1/12) − 1                      (monthly effective schedule rate) [std convention]
    B(k) = SA0 × [(1+j_m)^N − (1+j_m)^k] / [(1+j_m)^N − 1]

with `j` = 6% **[std]** (footnote 9). Since `(1+j_m)^12 = 1+j`, whole-year balances
reduce to `B(12t) = SA0 × [(1+j)^n − (1+j)^t] / [(1+j)^n − 1]`. The conversion of the
insurer's quoted "yearly interest rate" [S8] to a monthly rate is standardized as the
effective-rate root **[std]**; a nominal-/12 convention is a permissible variant and
the difference is small at these rates.

**Family income benefit shape.** On death (or terminal illness acceptance) at month
`k`, the policy pays `I` per month, in arrears, from the claim to the end of the term
— `N − k` instalments [S2] [S6] [S8]. The instalment stream is an annuity-certain: it
does not depend on any life after the claim. The claimant may commute remaining
instalments to a lump sum, reduced "fairly and reasonably" to reflect early payment
[S6] [S8]; the commutation basis is insurer-discretionary (see technical notes,
assumption class (b)). The FCA characterises FIB as decreasing term assurance in
present-value terms: the maximum possible remaining payments reduce over time [R8].

**Terminal illness.** The full death benefit is accelerated when both limbs of the
definition are met — (i) the illness has no known cure or has progressed beyond cure,
and (ii) the attending consultant expects death within 12 months [S1] [S6] [S8] [R8].
The amount paid is the cover amount calculated at the date the definition is met, so
for the decreasing shape a TI payment can be lower than a later death payment would
have been [S1]. Payment of the benefit ends the policy [S1] [S6] [S8]. For modeling,
TI is a timing acceleration of the same benefit, not an additional benefit (see
technical notes).

**Suicide exclusion.** No benefit is paid if death results from suicide or
intentional self-inflicted injury within 12 months of commencement [S1] [S6] [S8]
(one carrier frames it as the "first year" [S1]; another runs it from start or restart
and excludes self-inflicted TI claims at any time [S8]).

### Joint life

The composite joint basis is joint life first death: one benefit, paid on the first
death or terminal illness of either life, ending the policy [S1] [S2] [S6]. Separation
options (splitting a joint policy into two single-life policies on divorce/
dissolution or mortgage change without full underwriting) exist at two of the three
carriers [S1] [S6] but are out of scope, as is one carrier's replacement-cover option
for the surviving life after a first-death claim [S1].

### Expiry — no post-term tail (UK vs US)

At the end of the term the policy simply expires: cover ceases, nothing is payable,
and there is no maturity value [S1] [S6] [S8] [R8]. **There is no US-style post-level-term
annually-renewable tail.** Renewal and conversion options are not standard in the
current UK retail market: none of the three insurers' fetched current products
contains a renewal or conversion option, and one carrier's old conversion option is
explicitly "no longer offered" [S2]. The FCA records renewable term assurance as
offered in the UK market [R8], so a renewal feature should be treated as an optional
extension of the reference model, never as core. A projection model therefore
terminates all states at month `N` with no tail liability.

---

## Riders and options

**In scope (modeled or parameterized):**

- **Terminal illness benefit** — embedded, no extra premium, terms ≥ 2 years
  [S1] [S6] [S8] [S2] [S4]; modeled as claim-timing acceleration.
- **Indexation (RPI) option** — per the Options table; modeled via the cumulative
  indexation factor with take-up behavior in the technical notes [S1] [S6] [S8].
- **Guaranteed insurability option** — described; generates new policies at market
  rates, so it creates no liability on the modeled policy and is not projected
  **[std scope]** [S1] [S6] [S8].
- **Waiver of premium** — optional rider; 26-week deferral [S1]; a premium-waiver
  state is sketched in the technical notes but excluded from the base projection
  **[std scope]**.

**Out of scope:** critical illness cover and CI riders (guaranteed or reviewable
premiums) [S2] [S6] [S8]; one carrier's fracture and treatment benefits [S6];
children's covers; free pre-completion covers (free life cover ≤ £300,000 / accidental
death benefit ≤ £300,000 at one carrier [S2]; house purchase cover ≤ £500,000 at
another [S6]); joint-policy separation and replacement options [S1] [S6]; one carrier's
mortgage repayment guarantee (pays the actual outstanding mortgage balance rather than
the notional schedule) [S8]; dual life and joint life second event bases [S9];
renewable/convertible term (not present in any fetched current product [S2] [R8]);
commutation of FIB during payment is described contractually by one carrier but not
exercised in the base model [S6].

---

## Variations across insurers

1. **Packaging.** Separate single-shape products ([S2]) vs one policy with three
   payout bases ([S6]) vs a menu plan with five shapes including income options
   ([S8]). Composite: one chassis, benefit shape as a parameter — the second of those
   three structures [S6], which maps cleanly to a model-point field.
2. **Age/term envelope.** Two of the three carriers agree closely (entry to 77, expiry
   by 90, terms 1–50) [S2] [S3] [S7]; the third is much wider (18–88, expiry 89, terms
   to 72) [S9]. Composite: the two-carrier envelope [S2] [S3] [S7] — two of three
   insurers, and the tighter, more typical bounds.
3. **Decreasing schedule rate.** Client-picked menu 5/7/8/10% ([S4]) vs default
   6% or chosen 0–15% ([S8] [S9]) vs fixed rate in the schedule, value unpublished
   ([S6] [S7]). Composite: client-selected with 6% default (footnote 9). One carrier's
   actual-balance mortgage repayment guarantee [S8] is a distinctive design
   and excluded.
4. **FIB premium under escalation.** At one carrier, escalating FIB instalments carry
   no premium increase [S6]; at a second, income shapes increase premiums × 1.2 [S8];
   the third's family-income product increases premiums × 1.5 [S2]. Composite: FIB
   escalation excluded entirely — the variation is too wide to standardize honestly.
5. **Indexation loading.** Premium multiplier 1.5 at two carriers ([S1] [S2],
   [S6] [S7]) vs 1.2 at the third ([S8]); RPI floor: <1% no increase ([S1]) vs ≤0%
   ([S6]) vs 2% minimum applied ([S8]). Composite: ×1.5 (the mode) with the ≤0%
   floor [S6].
6. **GIO caps.** 100% of original cover at two carriers ([S1], [S6]) vs 50% at the
   third ([S8]); all cap at £200,000. Composite: 100%/£200,000.
7. **Waiver of premium.** 26-week deferral, 3-of-6 tasks fallback ([S1]) vs
   schedule-set deferral, 2-of-6 tasks ([S6]) vs not offered at all ([S8]).
   Composite: optional rider, 26-week deferral — the published mode; the third carrier
   shows WOP is not universal [S8].
8. **Suicide clause.** Year one ([S1]) vs 12 months ([S6]) vs 12 months
   from start or restart ([S8]). Substantively identical; composite: 12 months.
9. **Minimum premium.** £5/month published at one carrier ([S5]) vs no published value
   at the other two, one of which references a "minimum premium limit" without giving a
   value ([S6]). Composite: £5/month, the only public value.
10. **What does not vary.** Guaranteed level premiums for life-only cover, embedded
    terminal illness on the two-limb 12-month definition, no surrender or paid-up
    values, and expiry without value are uniform across all three insurers
    [S1] [S2] [S6] [S8] [S9]; the 60-day grace and 30-day cooling-off are documented at
    two of the three carriers [S1] [S6] (not extracted from the third's plan details).
    These are the invariant core of the composite.

---

## Regulatory context

**Prudential — Solvency UK (PRA).** The PRA concluded the Solvency II Review with
PS15/24 (15 November 2024); Solvency II assimilated law was replaced by PRA rules "in
full from the end of 2024", the reformed regime to be known as "Solvency UK" [R5].
For a term assurance liability model the operative valuation rules are: the best
estimate is the probability-weighted average of future cash-flows, discounted on the
relevant risk-free term structure, on realistic assumptions, gross of reinsurance
(reinsurance recoverables separate) [R1]; the projection must include benefit
payments, expenses, premiums, intermediary payments and policyholder-charged taxation
[R2]; and the contract boundary for guaranteed-premium term assurance is the full
policy term, because the insurer has no unilateral right to reprice — reviewable
premium business must instead be tested under the "premiums fully reflect the risks"
rules [R3]. Technical provisions are best estimate plus risk margin [REG-R1]; the
risk margin uses a 4% cost-of-capital rate with a life risk-tapering factor λ = 0.9
(floor 0.25) [REG-R4] — cited, not reproduced, in this library.

**Conduct — FCA.** Pure protection distribution is conducted under ICOBS, which
applies to non-investment insurance contracts [REG-R11]; the customer's best
interests rule is ICOBS 2.5.-1R, sitting alongside PROD 4 product governance and the
Consumer Duty [R9] [REG-R12]. The FCA's pure protection market study (MS24/1) is the
current conduct backdrop, examining commission structures, lapse patterns, and the
value chain including reinsurer influence [R8] [R9].

**Classification and consumer law.** Term assurance is Class I long-term business
under the RAO 2001, Schedule 1 Part II [R6]. Consumer misrepresentation remedies
follow the CIDRA 2012 regime (reasonable-care duty; graduated remedies for
deliberate/reckless vs careless misrepresentation) [REG-R20], which one carrier's
policy remedies mirror contractually [S1]. FSCS protection is 100% of a valid claim
with no upper limit [S1].

**Tax.** Protection policies are written to satisfy the qualifying-policy conditions
(one carrier's conditions reference para 19(3) of Schedule 15 to ICTA 1988 for option
compatibility) [S1]; benefits are commonly stated to be free of income and capital
gains tax [unverified — not confirmed from a fetched document]. Death benefits paid
to the estate may attract inheritance tax unless the policy is written in trust or
benefits pass to a spouse/civil partner; trusts are the promoted IHT route [S7]. At
insurer level, post-2012 protection business is excluded from BLAGAB and taxed on
trade profits under Finance Act 2012 Part 2 — a per-product tax-basis flag, not a
cash-flow driver, in this library [REG-R17].

**Professional standards.** Technical actuarial work on UK term assurance (pricing,
reserving, technical provisions) falls under FRC TAS 100 v2.0 (effective 1 July 2023)
[R15] and TAS 200: Insurance v2.0 (effective 1 January 2025) [R16].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-term_assurance-r1
[R15]: #uklib-term_assurance-r15
[R16]: #uklib-term_assurance-r16
[R2]: #uklib-term_assurance-r2
[R3]: #uklib-term_assurance-r3
[R5]: #uklib-term_assurance-r5
[R6]: #uklib-term_assurance-r6
[R8]: #uklib-term_assurance-r8
[R9]: #uklib-term_assurance-r9
[REG-R1]: #uklib-reg-r1
[REG-R11]: #uklib-reg-r11
[REG-R12]: #uklib-reg-r12
[REG-R17]: #uklib-reg-r17
[REG-R20]: #uklib-reg-r20
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
