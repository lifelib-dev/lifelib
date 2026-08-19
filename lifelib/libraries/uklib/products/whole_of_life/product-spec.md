# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03; see `sources.md`).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash flow modeling. It does not describe any single insurer's product. Facts carrying
a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial references),
both numbered per `_research/whole-of-life.md`, and [REG-R#] (the cross-product reference
library `references/regulatory-and-actuarial-references.md`, whose own R-numbering is
distinct; research provenance in `_research/regulatory-actuarial.md`) — were extracted from
the cited document and resolve against `sources.md`. Values marked **[std]** are
standardizations introduced for the reference implementation; each [std] table row carries a
footnote giving the rationale and the observed range across insurers. Facts the research file
could not verify are flagged [unverified].

Two product cells are specified, mirroring the two-cell structure of the US whole-life folder:

- **RefWOL-UW** — underwritten guaranteed whole of life (the research file's "Cell B";
  one adviser-distributed whole of life plan [S10] is the representative chassis).
- **RefWOL-O50** — over-50s guaranteed acceptance whole of life (the research file's "Cell A";
  two direct over-50s plans [S1] [S4] [S5] are the representative chassis).

A legacy unit-linked reviewable whole of life design [S15] is documented as a closed-book
variation only (see Variations).

---

## Product overview and market role

Whole of life assurance is a contract of insurance on human life with no fixed end date; it is
Class I ("Life and annuity") long-term insurance business under RAO Schedule 1 Part II, while
unit-linked variants fall in Class III ("Linked long term") [R5]. Both cells here are pure
protection products within the scope of the FCA's MS24/1 Pure Protection Market Study
(terms of reference announced August 2024; interim report January 2026; final report expected
Q3 2026) [R1] [R2].

**The underwritten cell** is adviser-distributed, fully medically underwritten cover with
premiums and sum assured guaranteed for life, sold for family protection, legacy and
inheritance-tax planning (typically written in trust) [S10] [S11] [S16]. Verified current
sellers include one with a standalone whole of life plan [S10] [S11] [S12], one offering life
cover with no end date inside a menu plan [S13] [S14], and one further insurer currently
marketing whole of life cover [S16]. The FCA treats underwritten whole of life as a live
category with a distinct target market and notes one insurer restricts new underwritten
policies at age 77 [R2].

**The over-50s cell** is direct-distributed guaranteed-acceptance cover: no medical questions,
fixed cash sum, level premiums that cease at an age cap while cover continues, a first-year
return-of-premium moratorium for non-accidental death, and no cash-in value at any time
[S1] [S4] [S7] [S9]. It is the UK analog of the US final-expense sub-market. The FCA's MS24/1
Annex 2 devotes a chapter to this cohort: guaranteed-acceptance over-50s customers pay on
average £71.73 in premiums per £1,000 sum assured versus £8.10 for underwritten whole of life,
reflecting anti-selection, older entry ages and shorter durations [R2].

**Contrast with US cash-value whole life.** Unlike the US participating whole life chassis
(guaranteed cash value schedule endowing at age 100, dividends, policy loans), both modern UK
cells are protection-only: there is **no cash-in value at any time** in any of the five
modern products fetched (six documents) [S1] [S4] [S5] [S7] [S9] [S10], no policyholder
dividend mechanism, and no policy loan facility. The liability is a pure-decrement death
benefit stream. Positive surrender value appears only in the legacy unit-linked reviewable
design, where it equals the value of investment units [S15].

---

## Representative specification

### Primary design: underwritten guaranteed whole of life ("RefWOL-UW")

#### Table 1 — Chassis, eligibility, underwriting

| Parameter | Representative value | Basis |
|---|---|---|
| Product type | Individual non-profit whole of life; guaranteed level premiums; guaranteed sum assured; no cash-in value at any time | [S10] |
| Lives assured | Single life (joint life first event / second event exist; out of scope) | [S10]; scope **[std]** (a) |
| Entry ages | 18–83 (age x = before (x+1)th birthday, i.e. age last birthday) | [S10] [S11] |
| Cover end age | None — whole of life, no maximum cover age | [S10] [S12] |
| Residency / underwriting | UK resident, registered with a UK doctor for 6 months before applying; full medical underwriting (health, occupation, lifestyle, family history) | [S10] [S11] [R2] |
| Rate factors | Age, health, occupation, nicotine use, amount/type of cover, optional benefits | [S11] |
| Smoker definition | Non-smoker: no tobacco/nicotine products for > 5 years; previous smoker: 12 months–5 years; smoker: < 12 months | [S10] |
| Sum assured limits | No stated maximum for level cover (escalation stops if sum assured would exceed £40m); £5m cap when increasing cover is selected at a second underwritten writer | [S10] [S13] |
| Minimum premium | £8/month or £80/year (as at 1 Jan 2025) | [S10] [S12] |
| Anchor model point | Male, entry age 40, non-smoker, £150,000 sum assured, level cover, monthly premium £101.25 | ages/limits within [S10]; cell and premium **[std]** (b) |

Footnotes:
- (a) **[std]** single life: the chassis carrier offers single, joint life first event (entry
  18–69) and joint life second event (18–83) [S10]; the other writer adds a payout-as-income
  option [S13]. The reference model is single-life; joint-life decrement structures are out
  of scope.
- (b) **[std]** anchor premium: underwritten whole of life premium rate tables are not public
  (research file gap: only example quotes and FCA averages exist). The anchor premium is
  derived from the FCA price-comparison metric of £8.10 in premiums per £1,000 sum assured
  for underwritten whole of life [R2], read as an annual rate per £1,000 (the same metric for
  over-50s plans, £71.73, reproduces the FCA's own stylised example — £30/month for £5,000 =
  £72.00 p.a. per £1,000 — so the annual reading is consistent; the reading itself is a
  drafting inference). £150,000 x 8.10/1,000 / 12 = £101.25/month. Not attributable to any
  insurer.

#### Table 2 — Benefit and exclusions

| Parameter | Representative value | Basis |
|---|---|---|
| Death benefit | Sum assured paid once, on death, then policy ends | [S10] |
| Terminal illness benefit | Sum assured accelerated on diagnosis of terminal illness: definite diagnosis, no known cure or beyond cure, death expected within 12 months, confirmed by the attending consultant; pays once then policy ends | [S10] [S12]; the other writer also includes terminal illness [S13] |
| Exclusions | Suicide or intentional self-inflicted injury within 12 months of start (or of a requested/milestone increase) → refund of premiums for that cover; no other stated exclusion on the core benefit | [S10] [S11] |
| Premium guarantee | Premiums guaranteed for life; change only on customer-initiated cover changes, increasing-cover escalation, or disclosure corrections | [S10] [S11] |
| Non-payment | Cover ends if premiums unpaid 2 months after due date; no reinstatement (new application required) | [S10] |
| Surrender | No cash-in value at any time; lapse forfeits all value | [S10] |
| Cooling-off | 30 days with premium refund | [S11] [S14] |

#### Table 3 — Options (elected at outset)

| Parameter | Representative value | Basis |
|---|---|---|
| Increasing cover (escalation) | Sum assured +3%, +5% or +RPI (capped 10%) each policy year; premium rises 2% for each 1% of cover increase; declining 3 increases removes the option permanently; increases stop if sum assured would exceed £40m | [S10] [S11] |
| Escalation modeled | Level cover in the base cell; 5% escalation variant (premium +10%/year) as the modeled alternative | choice **[std]** (c) |
| Milestone benefit (guaranteed insurability) | Sum assured increase without further underwriting within 90 days of life events (mortgage increase/house move, marriage/civil partnership, divorce/dissolution/separation, birth/adoption, ≥10% salary rise on promotion/job change, increase in IHT liability); cap = lower of original sum assured or £200,000 across all policies with that insurer; to age 54 (69 for IHT events); premium for the increase on original underwriting at current age | [S10] [S12] |
| Waiver-of-premium rider | Optional at extra cost, outset only; 6-month deferred period; own-occupation definition; entry 18–54; terminates at 70; monthly premiums required | [S10] [S11] |
| Cover reduction | Any time, floor at minimum premium | [S10] |
| Smoker-status review | Premium review possible after ≥ 12 months nicotine-free | [S10] |

Footnotes:
- (c) **[std]** escalation choice: observed escalation menus are 3%/5%/RPI-capped-10% with a
  2-for-1 premium step at the chassis carrier [S10] and fixed 2%–5% or
  RPI-applied-between-2%-and-10% at the other underwritten writer [S13]. 5% is picked as the
  modeled variant because it exercises the premium-escalates-faster-than-benefit feature
  (premium +10%/year vs benefit +5%/year) that dominates escalating-cover cash flow shape.

### Secondary design: over-50s guaranteed acceptance whole of life ("RefWOL-O50")

#### Table 4 — Chassis, eligibility, rating

| Parameter | Representative value | Basis |
|---|---|---|
| Product type | Individual whole of life paying a fixed cash sum on death after year 1; guaranteed acceptance, no medical questions; no cash-in value at any time | [S1] [S4] [S7] [S9] |
| Lives assured | Single life only | [S2] [S8] |
| Entry ages | 50–80 | [S4] [S8] [S9]; band choice **[std]** (d) |
| Residency | UK resident (one plan: ≥183 days in UK in the last tax year [S4]; another excludes Channel Islands / Isle of Man [S1]) | [S1] [S4] |
| Rate factors | Age at outset and smoker status only (plus chosen cash sum / premium) | [S1] [S4]; market-wide smoker differential [R2] |
| Smoker definition | Non-smoker: no tobacco, e-cigarettes or nicotine replacement in the last 12 months | [S4] |
| Cash sum limits | Minimum £500; aggregation cap £10,000 across same-insurer policies | min [S1]; cap [S4] [S5] [S9]; cap choice **[std]** (e) |
| Premium range | £5–£75/month per policy; £100/month aggregate cap across same-insurer policies | [S6]; caps [S1] [S7] [S9]; range choice **[std]** (f) |
| Payment method | Monthly Direct Debit only | [S1] [S4] [S7] [S9] |
| Anchor model point | Entry age 70, non-smoker, £30/month premium, £5,000 cash sum | [R2] stylised pair; cell **[std]** (g) |

Footnotes:
- (d) **[std]** entry 50–80: observed windows are 49–85 at one of the four plans surveyed
  [S1] and 50–80 at the other three [S4] [S8] [S9]. 50–80 is the modal window; the FCA notes
  entrants at 79–80 are the cohort most likely to receive less than premiums paid [R2].
- (e) **[std]** £10,000 cap: observed aggregation caps are £18,000 total cover plus £100/month
  premiums at one plan [S1], a £10,000 cash sum at two others ([S4] [S5]; and [S9], which also
  caps payments at £100/month across policies), and a premium-cap-driven limit of £100/month at
  the fourth [S7]. £10,000 is the modal cash-sum cap. Aggregation caps are immaterial to a
  per-policy model.
- (f) **[std]** premium range: observed per-plan ranges are £4–£100/month [S2],
  £5–£75/month [S6] and £7–£50/month [S8]; a fourth plan allows reduction to a
  £3.95/month floor [S9]. The middle range [S6] is adopted.
- (g) **[std]** anchor cell: the premium/cash-sum pair is the FCA's stylised representative
  example (£30/month, £5,000 sum assured, tipping point 13 years 11 months) [R2]. Observed
  quote anchors: £20/month at age 50 non-smoker buys £5,694 [S2]; £25/month
  non-smoker buys £7,643 at 50, £6,046 at 60, £3,701 at 70, £1,893 at 80 [S6] — that second
  plan's age-70 rate would imply roughly £4,400 for £30/month, so the FCA pair sits slightly
  rich to that quote; it is adopted because the crossover arithmetic then reproduces the
  FCA's published tipping point exactly. Entry age 70 also matches the pro-rata paid-up value
  worked example (policy taken at 70 → 240 expected monthly payments) [S9].

#### Table 5 — Benefit structure and first-year moratorium

| Parameter | Representative value | Basis |
|---|---|---|
| Death after year 1 | Fixed cash sum, any cause | [S1] [S4] [S8] [S9] |
| Non-accidental death in year 1 | Return of all premiums paid; no interest or uplift stated in any fetched document | [S1] [S4] [S7] [S9] |
| Accidental death (from day 1) | Full cash sum | [S1] [S4] [S7] [S9] |
| Accident definition | Death within 90 days of accidental bodily injury; injury by "external, violent and visible means", not sickness/disease | [S1] [S4]; a third plan's "fatal accident" wording similar [S7]; a fourth: unpredicted, unintentional event causing physical injury [S9] |
| Suicide in year 1 | Explicitly non-accidental → refund of payments | [S9]; also treated as non-accidental in a second plan [S4] |
| Accidental-death exclusions | Criminal act; flying other than fare-paying passenger; hazardous pursuits; self-inflicted injury; war/riot/civil commotion; alcohol/drug abuse; natural causes/illness | [S1] [S4] [S7] |
| Terminal illness | None in this cell | [S1] [S4] [S7] [S9] (absence per the research variations table) |
| Claims interest | Interest from death to payment at Bank of England Base Rate − 0.5%, floor 0.5% p.a. (one plan: where payment delayed > 2 months [S9]) | [S1] [S9] |

#### Table 6 — Premiums, cessation, lapse, options

| Parameter | Representative value | Basis |
|---|---|---|
| Premiums | Level, fixed at outset, guaranteed never to increase | [S1] [S4] [S7] [S9] |
| Premium cessation | Policy anniversary on/after the 90th birthday; cover continues for life | [S4] [S5] [S9]; choice **[std]** (h) |
| Surrender value | None at any time; cancellation after the 30-day cooling-off returns nothing | [S1] [S4] [S5] [S7] [S9] |
| Arrears / lapse | 60 days to make good a missed payment; death within the window → claim reduced by unpaid amounts; then cancellation with nothing back | [S4] [S9]; choice **[std]** (i) |
| Paid-up value | None in the base design (the pro-rata paid-up value offered by one plan is the modeled variation — see Variations) | [S1] [S4] [S7]; one plan's exception [S9] |
| Premium reduction | Once per policy, irreversible, floor at minimum premium; cash sum reduces (two plans [S1] [S4]; a third: reducible to a £3.95/month floor, once-only limit not stated [S9]) | [S1] [S4] [S9] |
| Cooling-off | 30 days with premium refund | [S1] [S4] [S8] [S9] |
| Funeral benefit option | Free to add; cash sum paid directly to the funeral provider and put towards the funeral (one plan names a partner funeral director giving a 10% discount on eligible services [S3]) | [S3] [S9]; out of model scope (payee redirection only) |
| Consumer warning (documented) | Depending on how long you live, total premiums paid may be greater than the cash sum paid out (wording varies by insurer); inflation erodes the fixed cash sum | [S1] [S2] [S4] [S5] [S8] [S9] |

Footnotes:
- (h) **[std]** cessation at 90: across the four plans surveyed the observed cessation rules
  are the anniversary on/after the 95th birthday [S1], up to and including the 90th birthday
  [S4] [S5], 30 years or the anniversary after the 90th birthday, whichever first [S8], and the
  anniversary on/after the 90th birthday [S9]. The FCA: caps apply "typically ... from age 90,
  although we see some insurers applying this from age 95", with one insurer adding the
  30-year cap to limit over-payment [R2]. Age-90 anniversary is the mode.
- (i) **[std]** 60-day arrears: observed processes are 30 days + 14-day reminder then
  cancellation, reinstatable within 6 months by paying arrears [S1], a cancellation
  right after 60 days unpaid [S4], 30 days' grace [S7], and 60 days with claims
  in the window reduced by unpaid amounts, e.g. £3,050 − £10 = £3,040 [S9].
  The 60-day pattern with that claim-offset rule [S9] is adopted.

---

## Contractual mechanics

Notation here is shared with `technical-notes.md`. Let P be the monthly premium, SA the sum
assured (cash sum), t the policy month (t = 1, 2, ...), CumPrem(t) = cumulative premiums paid
to the end of month t, and T_cess the number of months from the start date to the premium
cessation date.

### RefWOL-UW mechanics

- **Benefit.** The sum assured is paid once, on death or on earlier diagnosis of terminal
  illness (life expectancy under 12 months, consultant-confirmed), and the policy then ends
  [S10] [S12]. There is no maturity, no renewal, no conversion and no surrender value [S10].
- **Suicide clause.** Death by suicide or intentional self-inflicted injury within 12 months
  of the start date (or of an increase, for the increased portion) pays a return of premiums
  for that cover instead of the sum assured [S10] [S11]:

      DeathBenefit(t) = CumPrem(t)   if suicide/self-inflicted and t <= 12
                      = SA           otherwise

- **Premiums.** Guaranteed level for life: P(t) = P for all t while in force [S10]. Monthly or
  annual Direct Debit [S10]. Non-payment: cover ends 2 months after an unpaid due date with
  nothing payable and no reinstatement [S10].
- **Increasing-cover variant.** With annual benefit escalation rate e (3%, 5%, or RPI capped
  at 10%), applied at each policy anniversary, and the contractual 2-for-1 premium step
  (premiums rise 2% for each 1% of cover increase) [S10]:

      SA(y) = SA_0 x (1 + e)^(y-1)
      P(y)  = P_0  x (1 + 2e)^(y-1)          (y = policy year)

  With e = 5%: after 10 years the sum assured is x1.6289 and the premium x2.5937 — the
  premium/benefit ratio drifts upward at (1+2e)/(1+e) − 1 ≈ 4.8% per year (derived). Opting
  out of an increase three times removes the option permanently; increases stop if the sum
  assured would exceed £40m [S10].
- **Milestone benefit.** An option (not an obligation) to increase SA without underwriting on
  listed life events, capped at the lower of the original sum assured and £200,000 aggregate,
  exercisable to age 54 (69 for IHT events) [S10] [S12]. The base model carries it as an
  out-of-scope option (see Riders).

### RefWOL-O50 mechanics

- **Death benefit with 12-month moratorium.** From day 1, accidental death (per the Table 5
  definition and exclusions) pays the full cash sum; non-accidental death in months 1–12 pays
  a return of premiums paid (the fetched documents state no interest or uplift on the
  refund); any death from month 13 pays the cash sum [S1] [S4] [S7] [S9]:

      DeathBenefit(t) = SA                     if accidental (any t)
                      = CumPrem(t)             if non-accidental and t <= 12
                      = SA                     if t >= 13

- **Premiums and cessation.** Level premiums by monthly Direct Debit from the start date
  until the policy anniversary on/after the 90th birthday **[std]** (h); cover then continues
  for life without premiums [S4] [S5] [S9]:

      CumPrem(t) = P x min(t, T_cess)

  For the anchor cell (entry on the 70th birthday), T_cess = 240 months, matching the
  pro-rata paid-up worked example (240 expected payments for a policy taken at 70) [S9].
  Maximum premiums payable = 240 x £30 = £7,200 against a £5,000 cash sum.
- **Crossover ("tipping point").** Cumulative premiums first exceed the cash sum at

      t* = floor(SA / P) + 1   months        (level premiums, before cessation)

  Anchor: floor(5000/30) + 1 = 167 months = 13 years 11 months — reproducing the FCA's
  stylised tipping point (£30/month premium, £5,000 sum assured, tipping point after
  13 years 11 months) [R2]. A crossover exists whenever SA < P x T_cess. Firms model this
  ex ante by cohort (age, smoker status) within Consumer Duty fair value assessments [R2].
- **No surrender value; lapse.** Stopping premiums (after the 60-day arrears window **[std]**
  (i)) cancels the plan with nothing back [S1] [S4] [S7] [S9]. Death within the arrears window
  pays the claim reduced by unpaid amounts [S9]. The pro-rata paid-up variation replaces
  forfeiture with a pro-rata paid-up cash sum once at least half the expected payments have
  been made (see Variations) [S9].
- **Claims interest.** Interest is added from the date of death (in one plan, where payment
  is delayed more than 2 months) to payment at BoE Base Rate − 0.5%, floor 0.5% p.a.
  [S1] [S9]. The reference model treats settlement as immediate and excludes claims interest
  **[std]** (technical notes, conventions).

---

## Riders and options

**In scope (modeled):**

- *RefWOL-UW:* terminal illness acceleration (an integral benefit, not a rider — it
  accelerates the same sum assured) [S10] [S12] [S13]; increasing-cover escalation (5% variant
  **[std]** (c)) [S10].
- *RefWOL-O50:* the first-year accidental/non-accidental benefit split [S1] [S4] [S7] [S9]; the
  pro-rata paid-up variation [S9]; and, from two other plans, the RPI-increasing variant
  and the 2x accidental multiplier as documented alternatives (see Variations) [S4] [S7].

**Described, out of model scope:**

- Waiver of premium (RefWOL-UW): 6-month deferred period, own occupation, entry 18–54, ends
  at 70, extra cost [S10] [S11] — a disability decrement outside the base pure-death model.
- Milestone benefit / guaranteed insurability (RefWOL-UW) [S10] [S12] — an anti-selective
  option on sum assured increases; flagged as a model risk, not projected.
- Free life cover during underwriting, up to £1,500,000 (RefWOL-UW) [S12].
- Funeral benefit option (RefWOL-O50): redirects the cash sum to a funeral provider (one plan
  names a partner funeral director with a 10% discount on eligible services [S3]; another
  leaves the provider unnamed in the T&C, sends the payout directly to the provider, pays the
  estate instead on year-1 death, makes removal irreversible and the option incompatible with
  trust or assignment, and states that the option itself is "not regulated by the Financial
  Conduct Authority" [S9]) — payee redirection with no cash flow amount effect.
- Premium reduction options (both cells) [S1] [S4] [S9] [S10] and, in one plan, payment holidays
  (up to 2 holidays of up to 6 months, ≥ 12 months apart, after year 1; missed amounts repaid
  or netted off the payout) [S9].
- Payout-as-income option (one carrier's menu plan; not on joint life second death) [S13].
- Joint-life structures (both cells' providers) [S10] [S13]; jointless in the O50 cell anyway
  [S2] [S8].
- Wellness-programme premium adjustments (healthy-living discounts/rewards) [S16] —
  non-standard mechanics; that plan's provisions were not fetched (research gap).

---

## Variations across insurers

1. **Entry windows (O50).** 49–85 at one of the four plans [S1] vs 50–80 at the other three
   [S4] [S8] [S9]. Chosen: 50–80 (modal) **[std]** (d).
2. **Premium cessation (O50).** Anniversary on/after 95th birthday [S1]; to and
   including the 90th birthday [S4]; min(30 years, anniversary after 90th) [S8] (the design
   the FCA singles out as limiting over-payment [R2]); anniversary on/after 90th [S9].
   Chosen: age-90 anniversary **[std]** (h), the FCA-documented typical cap [R2].
3. **Accidental death enhancement.** One of the four plans pays 2 x the cash sum on death by
   fatal accident on/after the first anniversary (1x other causes), with the enhancement void
   if death occurs while living outside Europe/USA/Canada/Australia/NZ [S7] [S8]. The other
   three plans pay 1x for accidental death at all durations [S1] [S4] [S9]. The 2x multiplier
   is carried as a variation flag in the model.
4. **Indexation (O50).** Only one of the four plans offers an increasing variant: cash sum
   reviewed annually in line with RPI (floor 0%, cap 10% p.a.), premiums increase by RPI x 1.5
   (cap 15% p.a.); declining one increase freezes cash sum and premium permanently; cash-sum
   indexation continues after premiums cease at 90 [S4]. The other three are
   fixed-sum-only [S1] [S8] [S9]. Carried as a variation with the premium-escalates-faster
   feature mirroring the UW cell's 2-for-1 step.
5. **Paid-up value (O50).** One plan's pro-rata paid-up value: if at least half of the expected
   payments (start to the final payment date) have been made and payments stop, the policy
   stays entitled to a reduced payout = full payout x (payments made / expected payments) —
   e.g. 180 of 240 payments on a £3,500 payout → 0.75 x £3,500 = £2,625 [S9]. If less than
   half are paid the policy cancels with nothing. This materially changes lapse economics:
   late lapse creates a paid-up liability instead of a forfeiture profit (see technical
   notes). The other three plans forfeit everything on lapse [S1] [S4] [S7].
6. **Arrears handling (O50).** 30 + 14 days then cancellation, reinstatable within 6 months
   [S1]; 60-day cancellation right [S4]; 30 days' grace [S7]; 60 days
   with claim offset [S9]. Chosen: 60 days with claim offset **[std]** (i).
7. **Funeral options (O50).** One plan names a partner funeral director, pays out direct to
   that director and gives a 10% service discount [S3]. A second leaves the provider unnamed
   in the T&C with the same redirection design [S9]. A third historically offered a
   funeral-director option with a £250 contribution [unverified — third-party broker material
   only; that carrier's official funeral-benefit page shows no such option].
8. **UW entry ages and limits.** 18–83 single life (18–69 joint first event) at the chassis
   carrier [S10] vs 18–88 with sum assured unlimited, or £5m if increasing, at the other
   [S13]. Chosen: the chassis carrier's ages [S10] (the mechanics anchor).
9. **UW escalation menus.** 3%/5%/RPI-capped-10% with 2-for-1 premium steps [S10] vs
   fixed 2–5% or RPI applied between 2% and 10% [S13]. Chosen: the 2-for-1 menu [S10],
   5% variant **[std]** (c).
10. **Legacy unit-linked reviewable whole of life (closed-book variation, not a modeled
    cell).** Premiums buy units; a monthly deduction from the fund pays for life cover;
    premium and cover are guaranteed only to the first review — reviews usually start after
    10 years, then typically 5-yearly, reducing to annual past a certain age; a failed review
    forces a premium increase or cover cut (default on lost contact: cut cover) [S15]. Two
    bases: *maximum cover* (minimal reserve, illustrative ~£8/month per £100,000, steep
    premium jumps at reviews as life cover costs "rise sharply from age 65") vs
    *standard/balanced cover* (illustrative ~£50/month per £100,000, building a unit reserve
    that subsidises later mortality charges) [S15]. Surrender value equals the value of
    units, if any — the one whole of life design here with a positive cash-in value [S15].
    Optional accelerated critical illness / permanent disability benefits typically expire
    at e.g. 65 [S15]. Modern UK whole of life (RefWOL-UW) is deliberately non-reviewable
    ("guaranteed") [S10]; the causal link to historic review shocks is [unverified].
11. **Why these representative choices.** Three of the four over-50s plans [S1] [S4] [S9] are
    near-identical on the chassis (guaranteed acceptance, fixed cash sum, moratorium with
    ADB, cessation age, no cash-in value); the composite takes that chassis with the modal
    parameter at each point of divergence, and carries the accidental multiplier [S7], the
    RPI indexation [S4] and the pro-rata paid-up value [S9] as switchable variations — this mirrors
    the research file's own representative-design conclusion. The chassis carrier [S10] is
    the cleanest underwritten representative: guaranteed premiums, terminal illness
    acceleration, suicide-only exclusion, 2-for-1 escalation, guaranteed insurability, no
    cash value.

---

## Regulatory context

**Prudential — PRA / Solvency UK.** Both cells are Class I long-term insurance business [R5]
written by PRA-authorised insurers (the fetched providers' FCA/PRA registration numbers are
recorded in the research file [S1] [S4] [S7] [S9] [S10]). Liabilities are valued under the PRA
Rulebook Technical Provisions Part: technical provisions for all insurance obligations, at
the amount payable to transfer them immediately to another UK Solvency II firm,
market-consistent, with value = best estimate + risk margin; the risk-margin cost-of-capital
rate is 4% as fixed by the IRPR Regulations [R3], which also introduced a life-business
risk-tapering factor lambda of 0.9 (floor 0.25) [REG-R4]. Solvency II assimilated law was
revoked on 31 December 2024 and restated into PRA rules ("Solvency UK") effective the same
date [R4]. FSCS protection is 100% of the claim, with continuity of cover the first objective
for life policies [S1] [S8] [S10].

**Conduct — FCA.** ICOBS applies to the distribution, effecting and carrying out of
non-investment insurance contracts [REG-R11]; the classification of these plans as pure
protection contracts sold under ICOBS rather than COBS is [unverified] at handbook-glossary
level (research file gap). The Consumer Duty applies to retail market business [REG-R12], and
MS24/1 Annex 2 records its operative bite on the over-50s cell: firms must assess fair value
by cohort within Fair Value Assessments including ex-ante tipping-point modelling, and
communications must enable informed choice about the over-payment risk [R2]. The FCA also
articulates the lapse-supported economics directly: without the cross-subsidy from long-lived
continuers, "insurers would need to rely on lapses to remain profitable", particularly with
no surrender value [R2]. Consumer misrepresentation in these consumer sales is governed by
CIDRA 2012 (reasonable-care duty; graduated remedies for deliberate/reckless vs careless
misrepresentation — the structure visible in one carrier's conditions [S4]) [REG-R20].

**Tax.** The cash sum / sum assured is normally free of income tax and CGT but forms part of
the deceased's estate for inheritance tax unless the policy is written in trust
[S1] [S4] [S8] [S9]; the underwritten cell is actively marketed for IHT planning (in trust,
covering the IHT liability itself), with trust registration (TRS) requirements at claim
[S10] [S11] [S16]. At company level, FA 2012 Part 2 taxes BLAGAB on the I-E basis while
protection business is excluded from BLAGAB and taxed on trade profits — a reference model
needs a per-product tax-basis flag rather than a tax engine [REG-R17]; whether a given
over-50s or whole of life contract falls in "protection business" as defined turns on
issue-date and definition details not researched here [unverified — research file gap on
qualifying-policy rules]. The policyholder chargeable-event-gains regime (ITTOIA 2005 Part 4
Chapter 9, with HMRC's IPTM as the working interpretation) bites surrender-value-bearing
designs — here only the legacy unit-linked variation [S15] — not the modern protection-only
cells, which have no surrender value to generate gains [REG-R15] [REG-R16].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-whole_of_life-r1
[R2]: #uklib-whole_of_life-r2
[R3]: #uklib-whole_of_life-r3
[R4]: #uklib-whole_of_life-r4
[R5]: #uklib-whole_of_life-r5
[REG-R11]: #uklib-reg-r11
[REG-R12]: #uklib-reg-r12
[REG-R15]: #uklib-reg-r15
[REG-R16]: #uklib-reg-r16
[REG-R17]: #uklib-reg-r17
[REG-R20]: #uklib-reg-r20
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
