# Implementation Notes

**Status:** Draft, 2026-08-20. Built from [`technical-notes.md`](technical-notes.md); the
product it implements is specified in [`product-spec.md`](product-spec.md). Every parameter
value here is one of theirs, and where the model carries something the notes do not settle,
it is named below rather than absorbed.

> **This is a mechanics demonstration, not a pricing or reserving result.** What is sourced
> on this product is the contractual machinery: the either/or public-certification and
> company-basis trigger, the once-only care lump sum (*kaigo ichijikin*, 介護一時金) that does
> **not** terminate the contract, the survival-tested care annuity (*kaigo nenkin*, 介護年金)
> paid in advance with its ten-instalment cap and retroactive extinction, the 保険料払込免除
> (*hokenryō haraikomi menjo*, premium waiver) firing one grade **below** the lump sum, and
> the outright nil surrender value (*kaiyaku-henreikin*, 解約返戻金) [S1] [S2] [S4] [S7] [S8]
> [S12]. Everything quantitative is a **[std]** standardization. No carrier publishes 予定発生率
> (assumed incidence), assumed interest rate (*yotei riritsu*, 予定利率) or 予定死亡率 for this
> product, the regulator confirms there is nothing standard to publish for 第三分野
> (*dai-san-bun'ya*, third-sector) business [R10], and
> the 算出方法書 is a filed 基礎書類 that is not public [REG-R2] — so the office premium is a
> model-point **input**, the mortality table is a constructed proxy, and the whole morbidity
> basis is built in public from the government's certification rate (*nintei-ritsu*, 認定率)
> and grade composition [R4] [R5] [REG-R30]. Replace the assumption tables with company data
> before drawing any conclusion from the output.

`LTC_JP_S` is the modelx implementation of the notes: a monthly, single-model-point
projection of gross best-estimate liability cash flows for nursing-care insurance
(*kaigo hoken*, 介護保険) on the public-scheme-linked (*kōteki kaigo hoken rendō-gata*,
公的介護保険連動型) design.

**The chassis.** This product states its deltas against the `jplib` third-sector chassis,
whose model is [`Medical_JP_S`](../medical/model.md) and whose documents are
[the medical product specification](../medical/product-spec.md) and
[the medical technical notes](../medical/technical-notes.md). `LTC_JP_S` does **not**
inherit from that model in modelx — `Projection._bases` is empty and every formula here is
written out — so the relationship is documentary, not structural. What is inherited in
substance is the monthly grid, the timing conventions, the attained age (*man-nenrei*, 満年齢)
basis, the mortality construction from 第三分野標準生命表2018, the lapse table and the expense
structure; what is replaced outright is the benefit machinery. `Medical_JP_S` is
**frequency × severity × limit** with two day ledgers that never bind; `LTC_JP_S` is
**incidence into an absorbing state** with a payment counter that does. There is no `d_pay`,
no `d_ben`, no `L1`, no `LA` and no `agg_days_*` cells anywhere in this model.

## Run it

From the repository root:

```
python lifelib/libraries/jplib/products/nursing_care/run.py       # anchor cell, point 1
python lifelib/libraries/jplib/products/nursing_care/run.py 5     # another model point
```

or, three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("lifelib/libraries/jplib/products/nursing_care/LTC_JP_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked example's anchor cell and
reproduces the notes' four-row table, its month-by-month trace and its policy-year-1
aggregate to the precision the notes display. `result_cf()` is a tidy `DataFrame` indexed by
policy month `t`; `result_pols()` is its policy-count companion. The `Projection` docstring
holds the full mapping between the notes' symbols and the cells names.

## Four ledgers, nested rather than disjoint

This is not the third-sector chassis's frequency × severity × limit shape. It is **incidence
into an absorbing state**, and it is carried as four ledgers:

| Cells | What it counts |
|---|---|
| `pols_act(t)` | In force, not yet certified at `grade_waiver()` — pays premium, exposed to lapse |
| `care_w(t)` | Entered `grade_waiver()` — 保険料払込免除 running, lapse suspended |
| `care_l(t)` | Entered `grade_lump()` — the 介護一時金 has been paid to these lives |
| `care_n(t)` | Entered `grade_annuity()` — the 介護年金 is in payment |

`pols_if(t) = pols_act(t) + care_w(t)` is the definition. The other two are **marginal
first-entry counters riding on the same survival ledger**, not compartments, and the fact
that makes them work is an ordering rather than a sum:

```
care_n(t) <= care_l(t) <= care_w(t) <= pols_if(t)     at every t
```

`check_nesting()` asserts exactly that, and never a total. Adding the three together counts
the same lives three times, and losing the ordering lets a life start the annuity before its
lump sum has been paid — which the contract forbids, since an unpaid lump sum is paid
*together with* the first instalment [S1].

The ordering is preserved by the recursion rather than imposed on it, and that took the
entry pools to be different for the three grades. `pols_entry_w(t)` is drawn from
`pols_act(t)` alone, because a life already certified at the waiver grade cannot enter it
again. `pols_entry_l(t)` and `pols_entry_n(t)` are drawn from **everyone in force who has
not yet reached that grade** — `pols_if(t) - care_l(t)` and `pols_if(t) - care_n(t)` — which
includes lives already on waiver, because progression up the certification ladder is the
dominant route into the higher grades, not direct entry from health. Since the grade shares
fall as the grade rises, the monthly entry rates are ordered the same way and the nesting
follows.

## 認定率 is a prevalence, and the conversion has two terms

What the government publishes is a point-in-time **count of certified persons** — 19.4% of
第1号被保険者 at 31 March 2024, and 50.8% of them at 要介護2以上 [R4] [R5] [REG-R30]. It is not a
flow of new certifications, and multiplying it by a benefit amount as if it were an annual
claim frequency is the notes' first-listed pitfall. In an illness-death model with no
recovery the conversion is an identity, not an approximation:

```
i_G(x) = prev_G'(x) / (1 - prev_G(x))  +  prev_G(x) x (mu_C(x) - mu_H(x))
```

Three implementation decisions follow, and each is a way the arithmetic can be wrong while
the code still runs.

`prev_slope(t)` is the **analytic** derivative of the fitted logistic, `beta x prev x (1 -
prev/prev_ceil)`, not a difference quotient: this term goes straight into the claim rate, so
a numerical derivative would put its noise there too.

**The second term is not a refinement.** A rising prevalence understates incidence, because
the certified population is simultaneously being drained by its own excess mortality. It
enters as `prev_G x (k - 1) x mort_rate`, where `k = care_mort_mult = 2.75`, so `k` is not
only a post-onset assumption: setting it to 1 — which is what "there is no impaired-life
table, so leave it out" amounts to — cuts lifetime lump-sum claims on the anchor cell by
about 31%. That coupling is the least obvious property of this model, and the test suite
runs the `k = 1` case to hold the size of it.

The dimensional check that catches the whole family of errors: `prev` and `prev_G` are
dimensionless proportions, `beta` carries units of 1/year, and both terms are therefore
rates per year and may be added. A formula that adds a prevalence to a rate is the commonest
way to get this wrong. The conversion also rests on a **stationary-population assumption
[std]** — the cross-sectional 認定率 by age read as the path a cohort will follow — which the
notes state and the model inherits unchanged.

## The annuity ledger: in advance, capped, and a partial product

`ann_count(t)` sums the cohorts entering at `t`, `t − 12`, …, `t − 12(n_A − 1)`, each
weighted by `care_surv(s, t)`. Three things in that sentence are load-bearing.

The `j = 0` term is `pols_entry_n(t)` itself — **payment in advance, on the entry month**
[S1] [S7]. Deferring the first instalment by a year removes roughly a tenth of the annuity
liability and misdates all of it.

`care_surv(s, t)` is a **partial product** of the monthly care-state survival factors from
`s` to `t`, never a ratio `SC(t)/SC(s)` of cumulative products. The care-state mortality
rate reaches 1 at the terminal age, so the cumulative product underflows to zero and the
ratio form divides by zero exactly where the tail of this liability lives.

`pols_term(t)` is the cohort taking its last permitted instalment. It is removed from
`care_n`, `care_l`, `care_w` and hence from `pols_if` — the contract's retroactive
extinction on the tenth instalment [S1], expressed on a monthly grid. **On the anchor cell
the cap binds**: entrants take 4.62 instalments on average, 14.9% of them reach the tenth,
and removing the cap raises lifetime annuity cost by 11.4%. Do not carry the medical
chassis's intuition across — there the 通算 aggregate limit reads zero forever.

`check_ann_ledger()` rebuilds the month's instalments by scanning **every** month in the cap
window and keeping the annual anniversaries, instead of stepping back in twelves. A ledger
that paid the first instalment a year late, ran past the cap, or used the ratio form of
`care_surv` shows up in its residual rather than in a total, where it would be invisible.

## The waiver band: premium on `pols_act`, lapse on `pols_act`

Two of the notes' pitfalls, and they are one product fact seen twice. The waiver fires at
要介護1以上, one grade below the lump sum and two below the annuity [S1] [S8], so there is a
real band of lives for whom the contract has stopped collecting premium and has not yet paid
anything.

`premiums(t) = premium_mth_pp() x pols_act(t)`, never `x pols_if(t)`: charging premium to the
whole in-force block overstates lifetime premium income by 5.85% on the anchor cell — the
¥92,738 the waiver takes out, which is 5.53% of the in-force-weighted total. At age 85 the
band on waiver is 30.1% of the surviving block. Renewal commission rides on `premiums(t)`, so it
stops when the waiver stops the premium; maintenance expense rides on `pols_if(t)`, because
the policy is still administered when nobody is paying for it.

`pols_lapse(t)` is taken from `pols_act(t)` alone. With the premium waived and treated as
paid, and with no 解約返戻金 to surrender for, a life on waiver has nothing to lapse [S1] [S2].
Applying lapse to `pols_if` destroys the annuity liability it took thirty years to build.
There is no automatic premium loan (*jidō furikae kashitsuke*, 自動振替貸付) machinery here
either: with no surrender value there is nothing to lend against [S2] [REG-R14], so a missed
premium lapses the contract outright and the savings-chassis logic must not be inherited.

## The step at age 65, and where "180日" means two different things

`f_age(t)` is the sub-65 specified-disease (*tokutei shippei*, 特定疾病) gate: 0.20 below 65
where the company-basis limb is written, 0.05 without it, 1.00 at 65 and over [S1] [S4]
[S12] [R1] [R3]. Entry into 要介護2以上 jumps 6.1× between age 64 and age 65 on the shipped
basis. That step is a real feature of the product — a smooth curve through 65 misprices
every issue age in the lower half of the 40–79 issue range, which is most of it — and the
gate is the company-basis limb's **only** effect in the model: the limb's own adjudication
is out of scope **[std scope]**.

"180日" names two mechanisms in this market and an implementation must not carry one of them
twice. An exclusion period (*futanpo kikan*, 不担保期間) or a 認知症診断責任開始期 means cover has not
started; the 180-day (90-day where dementia-defined) test inside the company-basis trigger
means the care state must have **persisted**. The composite has the second and not the first
on the care benefits, so `waiting_mths()` is zero on the anchor cell and claims run from
month 0. The one waiting period in the model belongs to the rider. Related timing trap, also
implemented: a 要介護認定 takes effect **retroactively to the application date** [R1], so every
claim is dated at the month the trigger is met, not at notification.

## Absences that are product facts

Stated rather than left to inspection, and each asserted by a test so it cannot be added
back by accident:

- **No day ledger of any kind.** No `d_pay`, no `d_ben`, no `agg_days_*`, no 日額. The unit of
  account is an annual annuity instalment, not a paid day, so the 支払限度日数 machinery of the
  third-sector chassis has no counterpart.
- **No `cv_pp`.** There is no 解約返戻金 at any duration [S1] [S2] [S7] [S8]. `claims(t,
  "LAPSE")` exists, returns zero and is published as a zero column, because a missing column
  would hide the product fact rather than state it.
- **No `claims_death`.** The contract terminates on death with nothing payable [S1] [S11].
- **No maturity.** Cover and premiums are both whole of life (終身), so `proj_len()` is set by
  the mortality table's terminal age — 116 male, 118 female, read from the table rather than
  hard-coded — and there is no `policy_term`, no maturity benefit and no renewal.

## Inputs are external files

The model folder holds formulas only. Its five inputs are plain CSVs in this directory, read
once per model by the `Data` Space and reached from `Projection` through its `data`
Reference:

```
products/nursing_care/
  model_point_table.csv       <- inputs live here
  mort_table.csv
  lapse_table.csv
  prevalence_table.csv
  grade_share_table.csv
  run.py
  model.md  product-spec.md  technical-notes.md  sources.md
  LTC_JP_S/                   <- formulas only
    __init__.py  _system.json
    Data/__init__.py          (reads the CSVs, once per model)
    Projection/__init__.py    (the by-policy projection)
```

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eight model points indexed by `point_id`. **Point 1 is the worked-example anchor cell** (male 60 / ¥3,000,000 on 要介護2以上 / ¥600,000 a year from 要介護3以上 / ¥11,500 a month); points 2–8 exercise the sexes, the 40–79 issue range, both benefit-threshold pairs, a five-instalment annuity and each optional module | anchor cell **[std]**, the notes' worked example |
| `mort_table.csv` | Table mortality by sex and attained age, 40 to the terminal age, with a `provenance` column on every row | **[std]** log-linear graduation through eighteen anchor rates quoted from 第三分野標準生命表2018 [REG-R18] [REG-R20]; **not a copy** of the published table [REG-R21] |
| `lapse_table.csv` | Annual lapse by policy year, 9 / 7 / 6 / 5.5 / 5 / 4.5 / 3 % | **[std]** durational shape, anchored to the 5.6% p.a. industry 解約・失効率 [REG-R31] |
| `prevalence_table.csv` | The two sourced 認定率 anchors and the three logistic parameters fitted through them | anchors [R4] [R5] [REG-R30]; the logistic **[std]** |
| `grade_share_table.csv` | Share of all certified persons at each grade **or above** | grade composition [R4] [REG-R30]; constant across ages **[std]** |

This follows lifelib's `annuallife/TradLife_A`, which keeps its input beside the model and
reads it at run time, rather than `basiclife/BasicTerm_S`, which stores its inputs *inside*
the model. `Data.input_dir()` resolves from `_model.path.parent`, so it works wherever the
repository is checked out. **The trade-off:** copy `LTC_JP_S/` without the CSVs and it reads
fine, then fails on first evaluation. What it buys is that a diff of the model shows logic
changes only, and that a company basis drops in by replacing a same-schema file — no formula
changes. Both halves are covered by tests.

### The mortality table is a construction, not a copy

第三分野標準生命表2018 is published free, in full, at a stable public URL, so anyone can retrieve it
and check a rate — a real contrast with the restricted tables `uklib` has to work around.
**But the publisher's site terms prohibit reproduction** [REG-R21], so this library ships a
documented proxy anchored to a table you can go and read.

`mort_table.csv` is that proxy, and it is now the **library-wide canonical** one: the same
file, cell for cell and provenance string for provenance string, is shipped by every `jplib`
product that reads 第三分野標準生命表2018. Its construction has two parts.

**Anchors.** Eighteen rows — nine per sex — carry a rate **quoted** from the published table
[REG-R18] [REG-R20]: ages 40, 60, 65, 75, 80, 85, 90, 115 and 116 for males, and 40, 60, 65,
70, 75, 80, 85, 90 and 118 for females. Each says so in its `provenance` column, marked
`ANCHOR`, and each is a quoted rate inside a **[std]** construction rather than a copy of
the table [REG-R21]. The male `q60 = 0.00548` the worked example quotes is one of them.

**Graduation.** Between adjacent anchors the rate is log-linear in age,

```
q(x) = q(a) x ( q(b) / q(a) ) ** ( (x - a) / (b - a) )      for a <= x <= b
```

which reproduces **every anchor exactly by construction** — nothing sourced is disturbed by
the fitting — and is locally the Gompertz family, the family the published table itself
follows over this range. Above the last female anchor at 90 the female curve is continued at
the male age-90-to-115 log-slope and closed on the sourced female terminal rate. The shipped
file is restricted to ages 40 and over, which is the whole of this product's issue-age
range, and `q = 1` at the terminal ages 116 and 118.

The property that matters for this product is that the incidence identity reads the
mortality basis at **every** age — its second term is `prev_G x (k - 1) x mort_rate(x)` — so
every derived rate is an output of whichever mortality table is underneath it. Under the
canonical table six of the eight ages in the notes' entry-rate ladder (60, 65, 75, 80, 85
and 90, male) now sit on a **quoted** rate rather than on a fitted one, and the other two
are interpolated between quoted rates. That is a strictly better position than the single-pin
graduation this product shipped before, which agreed with the source at exactly one age.

What remains **[std]** is the interpolation rule and the extension of the female curve above
90, both of which say so in the `provenance` column.

**The prevalence tail above age 82 is the larger of the two, and it carries the claims.**
The logistic in `prevalence_table.csv` is pinned to the two sourced 認定率 at ages 70 and 82
and to nothing above 82. It has **three** parameters and **two** anchors, so one degree of
freedom is unidentified, and the free one — `prev_ceil = 0.95` **[std]** — is exactly the
one that sets the tail. `prev(90) = 0.662` and `prev(100) = 0.894` are therefore **unsourced
extrapolations**, not fitted values, and **40.2%** of the anchor cell's lifetime benefit
outgo (74.7% at issue age 79, model point 8) falls at attained age 83 or over. That is a
first-order model risk, not a detail of the fit: refitting the same anchors at
`prev_ceil` = 0.60 / 0.50 / 0.40 gives `prev(90)` = 0.517 / 0.459 / 0.388 and moves lifetime
benefit outgo by −4.2% / −5.8% / −6.7%, with the *timing* of the claims moving more than the
total. `technical-notes.md` sets this out under *Key sensitivities and model risks*, and a
test pins both tail rates and the extrapolated claim share so neither can drift into looking
sourced.

## Modules that are off in the base run

Each is implemented, switched off on the anchor cell so the base run reproduces the worked
example, and exercised in its other position by a shipped model point.

| Module | Switch | Off (anchor cell) | On |
|---|---|---|---|
| State-tested annuity and its recovery decrement | `annuity_test`, `rec_rate` | `survival`, 0.0 | point 5: `state` with the notes' 5% p.a. placeholder — recovery cuts that point's lifetime annuity claims by 12.4% |
| Anti-selective lapse, loading **incidence** | `sel_lapse_lambda` | 0.0 | point 8: 0.30, where cumulative lapse has passed the 20% reference point |
| 認知症一時金特約 (*ninchishō ichijikin tokuyaku*), a dementia lump-sum rider (*tokuyaku*, 特約) | `dementia_rider` | false | point 6: adds ¥47,673 of lifetime rider claims |
| 1-year 不担保期間 of the simplified-underwriting design | `waiting_1y` | false | point 7: zeroes all three entry rates and every claim for `t < 12` |
| Company-basis trigger limb | `company_limb` | true, so the sub-65 gate is 0.20 | point 4: written off, dropping the gate to 0.05 |

The recovery rate and the state test **must be tested together**. `rec_rate()` returns zero
unless the annuity is state-tested, so with the rate at zero the switch is an exact no-op —
the test suite asserts that the state-tested run with `rec_rate = 0` reproduces the
survival-tested run cash flow for cash flow. Recovery is deliberately scoped to the annuity
ledger **[std scope]**: a paid lump sum cannot be unpaid [S1], and a recovery decrement on
`care_l` would let the same life claim the once-only benefit twice.

**Known limit of that switch: a recovered life keeps its 保険料払込免除 for life.** `rec_rate` is
the rate of falling **below the annuity grade** `G_N` = 要介護3, not the rate of returning to
health, and it is applied to `care_n` alone. A life that recovers therefore leaves the
annuity ledger and may re-qualify on a new 介護年金支払基準日, but stays in `care_w`: it never
re-enters `pols_act`, never resumes premium and is never again exposed to lapse.

For the step the switch models this is **correct** — `G_W` = 要介護1 is two grades below `G_N`,
so a 要介護3 → 要介護2 downgrade stops a state-tested annuity and leaves the waiver running,
which is what the ladder says [S1] [S2] [S8]. What is **not** modelled is recovery below
`G_W`, the downgrade that would end the waiver and restore the premium. No retrieved source
publishes a transition matrix between grades, and a single rate cannot carry two thresholds,
so the model implements the threshold it can evidence and names the other as a gap. The
direction is known: under `annuity_test = state` with `rec_rate` > 0, **premium income is a
lower bound** and the waived band an upper bound — a lower bound in the exact sense that
`pols_act(t)`, and so every premium, is *identical* to the `rec_rate = 0` run while the
annuity ledger is materially smaller. The one route by which recovery reaches `care_w` is
the ten-payment cap, and it moves it **upward**: a recovered life takes no tenth instalment,
so `pols_term(t)` extinguishes fewer contracts. Nothing ever releases a life back into
`pols_act`. The base run is unaffected — `rec_rate` is zero there — and
`test_a_recovered_life_keeps_its_waiver_for_life` asserts every clause of this, so it is a
documented limit rather than a silent one.

Two further constructions are outside the model and named rather than hidden: the right to
change base rates (基礎率変更権), whose *exercise* is not modelled although the parameterized
incidence basis is precisely the capability the regime asks for [R10] [REG-R15]; and
reinstatement (*fukkatsu*, 復活), which belongs here as a **new model point** rather than as a
negative lapse, because the 責任開始期 resets to the 復活日 [S1] [S2].

## Sign convention

The notes' `net_cf(t)` is already **income positive** — premiums less claims, acquisition
and maintenance expense, the claim-handling expense and commission, each on its own line —
which is the library-wide sign of `net_cf`. So unlike the models whose notes
print the stream outgo-positive, there is no `liability_cf` companion column here: one
stream, one sign, one name. `check_net_cf()` re-adds the statement from exactly the columns
`result_cf()` publishes, so a cash flow that exists in `net_cf` but not in the statement, or
the reverse, fails a test rather than hiding in a total.

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S` wherever it has an analogue: `pols_*`
for policy counts, plural nouns for cash flows, `*_rate` for annual rates with `*_rate_mth`
for their monthly counterparts, `*_pp` for per-policy amounts, `claims(t, kind)` with an
uppercase `kind`, and `pols_if_at(t, timing)` for the within-month reads. The notes use
compact actuarial symbols and the full mapping lives in the `Projection` docstring. Four
cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `act(t)` | `pols_act` | `act` beside `care_w` reads as an abbreviation of "actual" rather than as a policy count, and every policy count in the library starts `pols_` |
| `term(t)` | `pols_term` | It is a policy count, not a term of the contract — and the bare word in a life model reads as the policy term, which this whole-of-life product does not have |
| `i_G` / `i_G_m` | `inc_rate_l` / `inc_rate_l_mth` | The library rule is that a bare `*_rate` is annual and `*_rate_mth` monthly, matching `mort_rate` / `mort_rate_mth` and `lapse_rate` / `lapse_rate_mth` |
| `prev(x)`, `prev_G(x)` | `prev_rate`, `prev_grade` | These are **proportions**, not rates; naming them `*_rate` beside the entry rates would invite the one substitution the whole product must avoid |

Four further names carry library-wide rulings rather than this product's own reasoning, and
each means the same thing in all nine `jplib` models:

| Name | Ruling |
|---|---|
| `premium_mth_pp()` | `*_mth_pp` is a **monthly** per-policy premium and a bare `premium_pp` an **annual** one. This product's `P` is monthly, so it is `premium_mth_pp` |
| `prem_period_type()` | `prem_period` is a **duration** in the model's own grid unit. This cells returns a category (終身払), so it carries the `_type` suffix; the model point column keeps the name `prem_period` |
| `mort_be_factor` | The multiplier turning the shipped valuation table into the projection basis, spelled the same way in all nine models. It is **not** an actual-to-expected ratio, which is a different thing |
| `claims_annuity` | The name is the benefit's **form** — a stream of instalments — not its contingency, and the library uses it for both kinds. Here it is a **living** benefit: the 介護年金 is paid while the insured **survives** in a certified care state at 要介護3以上, and death stops it. In `IncomeTerm_JP_S` the same column is a **death** benefit paid to the survivors. Both the `claims(t, "ANNUITY")` docstring and the `result_cf()` docstring say which, on their first line, so a reader of one model cannot carry the other's meaning across |
| `expenses` / `claim_expenses` | `expenses(t)` is **acquisition and maintenance only**. The claim-handling expense is its own cells, deducted on its own line in `net_cf(t)` and published as its own `claim_expenses` column of `result_cf()`. `technical-notes.md` prints the two combined in its worked-example `expenses` column, and says so at the table |

## Standardizations used

Everything the notes mark **[std]** is carried unchanged: `mort_be_factor = 1.25`; the care-state
mortality multiple `care_mort_mult = 2.75`; the prevalence logistic (`prev_ceil = 0.95`,
`prev_beta = 0.194069`, `prev_x_mid = 85.710591`); the constant grade shares 0.715 / 0.508 /
0.340; the sub-65 gate 0.20, or 0.05 without the company-basis limb; `rec_rate = 0`; the
monthly conversion of every annual rate; uniform incidence within the policy year; the
processing order of incidence, then mortality, then lapse; the lapse table; ¥20,000
acquisition expense; ¥250 monthly maintenance inflating at 1.0% p.a.; ¥5,000 per claim
event; initial commission at 150% of annualized premium and renewal at 3.0% from policy year
2; and the office premium itself, ¥11,500 a month on the anchor cell.

Three standardizations are the model's own, because the notes do not settle them, and all
three are declared in the `Projection` docstring as well as here:

1. **The shape of the mortality construction** — the log-linear interpolation rule between
   the quoted anchors, and the extension of the female curve above its last anchor at 90.
   The notes publish rates, not a table; the shape that joins them is the model's own.
2. **The rider's incidence** — `dementia_share = 0.35` of the entry rate into the lump-sum
   grade, after a six-month 認知症診断責任開始期, with the MCI limb and the dementia limb carried
   as **one** event paying `(1 + mci_fraction) x dementia_amount` at the dementia date. No
   published dementia incidence basis appears in any retrieved source; the merge gets the
   amount right and dates the 10% MCI limb late.
3. **A cap at 1 on `mort_rate` and `mort_rate_care`** — a guard, not an assumption. On the
   shipped table `2.75 q` first exceeds 1 at male age **105** and female age **111**, so the
   cap binds from there; without it the monthly conversion `1 - (1 - q)^(1/12)` returns a
   complex number at the terminal age.

The build corrected `technical-notes.md` where it and the model disagreed, and they now
agree. In three places the notes' own arithmetic was wrong: the prevalence at age 60 and
every prevalence, slope and incidence figure derived from it (a relative error of about 6e-6
in the notes' arithmetic), the corresponding digits in the three month traces, and the
description of `mort_be_factor = 1.25` as the reciprocal of the *midpoint* of the sourced
70%–85% band, which it is not — 0.80 is a round value inside the band, and the value 1.25 is
unchanged.

The fourth restatement is the adoption of the **library-wide canonical** mortality table
described above, and it is the largest. Every **derived** figure in the notes that reads the
mortality basis was recomputed on it — not adjusted, but re-derived from the contractual
mechanics. **Nothing sourced moved**: the one rate the worked example quotes, male
`q60` = 0.00548, is an anchor of the canonical table and is unchanged, so the worked
example's four rows, all three month traces and the whole policy-year-1 aggregate are
unchanged to the last displayed digit. What moved is everything computed off the table at
ages **other than** 60:

- the entry-rate ladder into 要介護2以上 at ages 64 to 90 — 0.000295 / 0.001795 / 0.004795 /
  0.012413 / 0.030456 / 0.065003 / 0.115568, against 0.000296 / 0.001808 / 0.004861 /
  0.012716 / 0.030609 / 0.062836 / 0.108219 before — with age 60 unchanged at 0.000134;
- the gradients it quotes: 65-to-90 is now a factor of **64** (was 60) and 60-to-90 a factor
  of **862** (was 807);
- the lifetime loss ratio, 34.7% (was 34.6%), with lapse off 53.5% (was 53.4%) and at half
  lapse 43.5% (was 43.3%);
- the share of the block in force at age 85, **0.126** (was 0.123), and the premium exposure
  behind the two premium-scale ratios, **41.8%** and **27.3%** (were 41.5% and 27.2%);
- the annuity ledger's average instalment count and tenth-instalment share, **4.62** and
  **14.9%** (were 4.66 and 15.1%);
- the waiver's yen cost, **¥92,738** and 5.53% of the in-force-weighted premium (was ¥91,922
  and 5.52%);
- four sensitivities — `k` = 4's annuity effect **−8.3%** (was −8.4%), the five-instalment
  cap **−25.9%** (was −26.1%), `f_sub65` = 1's loss ratio **36.1%** (was 35.9%) — and the two
  module totals, point 5's annuity **¥360,416** (was ¥337,364) and point 6's rider
  **¥47,673** (was ¥46,890);
- and the age at which the care-state mortality cap first binds, male **105** and female
  **111** (were 103 and 108).

Figures that were recomputed and found unchanged at the precision they are quoted were left
alone rather than restated: the 6.1× step at 65, the 30.1% waiver band at age 85, the 5.85%
premium overstatement, `k` = 1's −31.0% and `k` = 4's +12.4% on the lump sum, the grade
shares' +7.5%, the cap's +11.4%, point 5's −12.4% recovery effect, and the crossover to
negative `net_cf` in policy month 228 at attained age 79. Every figure on both lists is
asserted by a test, so the restatement is held in place rather than trusted.
`product-spec.md` needed no change: it carries none of the derived figures, and every
contractual parameter in the notes is unchanged and still identical to its.

## Tests

`tests/test_model_conventions_jp.py` asserts the house style — the external-inputs layout,
the read-once property, the `Data` / `Projection` split, the docstring contract, the
`result_cf` column vocabulary, the no-argument `check_*` shape and the read-write-re-read
round trip. `tests/test_nursing_care_jp.py` asserts this product, in five blocks:

- **The worked example**, hard-coded as module-level tables so a reviewer can check it
  against the notes by eye: every assumption value the notes list, the four-row table, all
  three month traces term by term, the policy-year-1 aggregate with its closing ledgers, and
  the entry-rate ladder by attained age — the one contract with the notes that binds at ages
  other than the pinned age 60.
- **Every entry in the notes' *Known modeling pitfalls* list**, one test each, named after
  the pitfall. Each is a way an implementation can look right and be wrong, so each test is
  written to fail if the pitfall were committed rather than to restate the right answer.
- **The identities**: the in-force roll-forward naming every decrement, and all four
  `check_*` cells with their per-`t` residuals, on all eight model points.
- **Each optional module in both positions** — off in the base run and switched on. Where
  the switch is a model point column rather than a Space Reference, the test copies the
  model *and its external inputs* to a temporary directory and edits the copy, so the
  shipped tables are never written to.
- **The structural facts and the notes' key sensitivities**: the nesting, the binding cap,
  the in-advance annuity, the partial-product survival, the step at 65, the whole-of-life
  run-off, the absent day ledger, the zero lapse claim, the mortality cap, and the eight
  sensitivity figures the notes quote — so a change of basis that moved one of them would
  have to move the document too.

The mortality-table test is the one worth naming on its own: it asserts that every row is
marked **[std]**, that the eighteen `ANCHOR` rows carry exactly the rates the library quotes
from 第三分野標準生命表2018, and that between adjacent anchors the log of the rate is **linear in
age**, so the file can be read off in two lines and reproduces every sourced rate exactly.
That is what keeps the redistribution position checkable rather than merely stated — and it
is what makes the same table verifiably the same table in every product that ships it.

```bash
python -m pytest lifelib/libraries/jplib/tests/test_nursing_care_jp.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-nursing_care-r1
[R10]: #jplib-nursing_care-r10
[R3]: #jplib-nursing_care-r3
[R4]: #jplib-nursing_care-r4
[R5]: #jplib-nursing_care-r5
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R30]: #jplib-reg-r30
[REG-R31]: #jplib-reg-r31
[std]: #jplib-std
<!-- END generated citation links -->
