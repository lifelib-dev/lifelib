# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`products/sofortrente/technical-notes.md`](technical-notes.md); the product it implements
is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result**, and on this
> product the two are further apart than the arithmetic makes them look, because the whole
> answer rests on a mortality table nobody may ship. The *mechanics* are cited, and since
> 2026-08-30 they are cited to clause text rather than to search records: the guaranteed
> annuity is struck once at inception by converting the *Einmalbeitrag* at a factor
> calculated on a first-order annuitant table — DAV 2004R (Aggregattafel) at one carrier
> [S2] [S3], "NÜRNBERGER Tafel 2013 R" at another [S4] — at an interest rate at or below the
> statutory *Höchstrechnungszins*, every retrieved tariff pricing **at** its vintage's cap
> [S2] [S4] [S6] [REG-R14] [REG-R15]; the *Rentengarantiezeit* is a tariff-level feature
> carried in a carrier's own product name for the immediate form as well as the deferred one
> [S4] [S5]; the *Kapitalrückgewähr* refunds the *Einmalbeitrag* less the **guaranteed**
> instalments already paid [S2] [S6]; the *Hinterbliebenenrente* is a *Zusatzversicherung*
> with its own condition set, beginning only after any guarantee period expires [S1] [S9];
> the *Überschussbeteiligung* is a statutory entitlement continuing through the payout phase,
> *Bewertungsreserven* included and *hälftig* [S2] [S3] [S10] [REG-R24]; and there is no
> *Rückkaufswert*, no lapse and no *Beitragsfreistellung* once the *Rentenbezug* has begun
> [S1] [S2] [S4] [R1] [R2] [R5] [REG-R28]. **Almost no level is sourced, and none of the few
> that are has been used to calibrate anything here.** The library was **drafted** under a
> policy that blocked all egress, with an exhausted `WebSearch` budget, so every number below
> was chosen as a **[std]** with a stated rationale out of the authoring model's own knowledge
> and none was fitted to market data. The citations have since been **re-verified against the
> primary documents** — 19 of this product's 32 source entries read `Retrieved: yes`, 12 still
> read `no` — and that pass produced four benchmarks the model can be judged against but was
> not built from: one carrier's guaranteed annuity scale, 151 € a month at 65 on 50 000 € with
> a 20-year guarantee [S8] — about 16 % below this model's [std] construction on the same case;
> one carrier group's
> payout-phase *Zinsüberschussanteil*, 3,35 % less the *Rechnungszins* for 2026 [S10]; market
> *Rentenfaktoren* of 29,09 € and 25,97 € per 10 000 € for 2021 and 2022 [R20]; and five
> carriers' *laufende Verzinsung* for 2026 [R21]. **No charge parameter and no portfolio sex
> mix was established at any carrier for any year** [S11] [S12] [S13] [R22] [R23]. DAV 2004 R
> and DAV 2004 R-Bestand are DAV property and are **cited by name, never shipped** [R10] [R11]
> [REG-R47] [REG-R49]. Replace the decrement, charge and surplus tables with company data
> before drawing any conclusion from the output.

## Run it

```bash
python products/sofortrente/run.py
python products/sofortrente/run.py 3       # the Kapitalrückgewähr cell, where R is solved
python products/sofortrente/run.py 9       # the same anchor cell nachschüssig
python products/sofortrente/run.py 10      # the in-force cell with a given annuity
```

Three lines to the same thing:
```python
import modelx as mx
model = mx.read_model("products/sofortrente/Sofort_DE_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by the month `t` with eight columns — the
six-line cash flow statement and `net_cf` in both orientations — and `result_pols()` puts the
state behind it beside it.

`t` is the library's **0-based** month index, counted in complete months from
*Vertragsbeginn*: a new-business point's first row is `t = 0`, `duration(t) = t // 12` is the
completed policy years and `policy_year(t) = t // 12 + 1` the contractual, 1-based label —
every formula that steps at the anniversary uses `duration(t)`. `proj_len()` is the **exclusive
end** of the frame, so the frame is `range(t_start(), proj_len())`, the last row is
`proj_len() − 1` and the row count is `proj_len() − t_start()`. On the anchor cell
`proj_len() = 672` and the frame is `t = 0 … 671`, 672 monthly rows; on the in-force point 10
`t_start() = 156` and the same `proj_len() = 672` gives 516 rows, `t = 156 … 671`.

The model and both its Spaces carry docstrings: `model.doc`
describes the product and says what makes it a payout model rather than a shortened
accumulation one, `model.Projection.doc` holds the full mapping from the technical notes'
symbols to the cells names, and `model.Data.doc` states the decrement proxy's construction,
its anchor and what a replacement must preserve.

## One payment in, and no behaviour at all

This is the first thing to know about the model and it is a statutory fact rather than a
simplification. Once the *Rentenbezug* has begun the policyholder has no right of termination,
so § 169 VVG is displaced by § 168 Abs. 3 VVG and § 165 VVG has nothing to apply to [R1] [R2]
[R5] [REG-R28]. The consequences reach further into a projection model than they look:

- **No `lapse_rate`, `lapse_rate_mth`, `av_pp_at`, `cv_pp` or any surrender cells exists**,
  at any duration: no *Rückkaufswert* table, no *Stornoabzug*, no cost-spreading rule.
- **The only decrement is death.** Where a *Hinterbliebenenrente* is in force there are two
  lives and the liability runs to the second death.
- **Class (c) of the technical notes contains a basis and no behaviour.** Every other model
  in the library needs a lapse rate, a paid-up rate and an option take-up rate; this one
  needs none, which makes it the one whose answer depends most purely on the mortality basis
  and the surplus assumption.
- **`premiums(t)` is the *Einmalbeitrag* at `t = 0` and nothing anywhere else.** An in-force
  point's frame does not contain `t = 0`, so it collects nothing: the premium was paid before
  the valuation date.

The model's one structural fork is therefore not two premium forms but **derived against
given**: `annuity_pp_init() == 0` strikes the *garantierte Rente* by equivalence, and a
positive value takes an annuity struck years ago on a basis this model does not reproduce, on
which `check_equivalence()` returns `True` without asserting anything and says so in its own
docstring rather than passing silently.

## The *Rentengarantiezeit* is a certain floor, not a second stream

Inside the guarantee period the instalment is payable **whether the annuitant is alive or
not** [R23], and the arithmetic that expresses this is a `max` and not a sum:
```
payment_factor(t) = max(γ(t), l_a(t)) + δ (1 − l_a(t)) l_s(t) (1 − γ(t))
```

Both errors this closes off are large and point in opposite directions. On the anchor cell
the guaranteed instalments over months 0 … 119 come to **48 073,0432 €**; decrementing them
for survival — the annuitant's leg alone — would pay 44 645,0162 €, **7,13 % below**, and
adding the certain floor instead of taking the `max` would pay 92 718,0594 €, **92,87 %
above**, because `γ + l_a` pays `1 + l_a` for the whole ten years. The survivor's leg carries
the `(1 − γ(t))` gate for the same reason: inside the guarantee the full instalment is
already going out, and adding `δ` on top would pay `1 + δ`.

The split into *who* receives the instalment is published rather than netted:
`annuity_payments(t, "ANNUITANT")` is paid on the strength of survival and
`claims(t, "GUARANTEE")` on the strength of a death, so the two commonest errors show up in a
**column** rather than in a total. `check_payment_factor()` asserts that the three legs
partition the instalment exactly, and `check_guarantee_certain()` that the factor is exactly 1
at every payment month inside the guarantee, whatever `δ` is.

## The *Kapitalrückgewähr* is solved, not evaluated

Where `refund_form() == "full"` the death benefit is the *Einmalbeitrag* less the guaranteed
instalments already paid, floored at zero. Because a larger refund means a smaller annuity, and
a smaller annuity runs the refund off more slowly, the pricing equation is **implicit in `R`**:
```
g(R) = R ä (1 + β) + Σ_t v^(t/12) d̃_a(t) max(SP − n(t) R, 0)  =  SP_net
```

`g` is increasing in `R` on `(0, R_max]` with `g(0) < SP_net`, so `annuity_pp_derived()`
bisects to `solve_tol = 1e-10` in at most `solve_max_iter = 200` steps, evaluating the sum
inline from the cached `tariff_lives` path rather than through a cells parameterized by the
trial `R` — which is what keeps the solve out of the dependency graph. **Computing `R_max` and
then subtracting a refund cost is a different — and wrong — answer, and the difference is not
a rounding.** On model point 3 the plain annuity is `R_max = 370,1660 €`; the refund leg
valued *at that annuity* is 13 546,3742 €, and dividing the remaining *Nettoeinmalbeitrag* by
`ä (1 + β)` gives **318,7362 €**. The solved answer is **298,8348 €**, 6,2 % lower, and the
refund leg at the solved annuity is 18 788,3117 € — nearly a fifth of the
*Nettoeinmalbeitrag*, and 39 % larger than the naive valuation of it. `refund_pv()` is
published so the identity can be *seen*, and `check_equivalence()` asserts it.

During an *Aufschubzeit* no instalment has been paid, so `cum_annuity_guar_pp(t) = 0` and the
refund is the whole *Einmalbeitrag*: the *Beitragsrückgewähr* on death before *Rentenbeginn*
falls out of the same machinery without a second mechanic, which model point 6 exercises.
**The refund is measured against the *guaranteed* annuity, not the total one** [std], argued
from the principle that a guaranteed benefit cannot be defined by reference to a
discretionary quantity; which reading a German carrier uses **was not established** and the
two diverge materially over twenty years (research gap 10). `check_refund_run_off()` closes
the loop by counting the instalments needed to exhaust the refund directly — `⌈SP / R⌉`, 335
on model point 3 — which is what catches a refund netted against the total annuity: the
*Überschussrente* would retire the capital sooner and the count would not match.

## The *Hinterbliebenenrente* is a gated leg, not a term in the benefit formula

The German market treats the survivor's annuity as a *Zusatzversicherung* — a rider with its
own condition set, for which the GDV publishes model conditions [S9] — so it is a separate
gated leg here with its own insured life, and it is **off in the base run**. Switched on it
makes the contract a joint-life last-survivor annuity: `proj_len()` takes the **maximum** of
the annuitant's horizon, the guarantee's own end and the second life's horizon, and on model
point 4 the second life is three years younger, so `proj_len() = 708` and the frame runs to
`t = 707`, three years past the annuitant's own horizon. `(1 − l_a(t)) l_s(t)` is the probability that the annuitant
is dead and the second life alive at the payment instant, **assuming independence** [std]:
real joint lives are positively dependent, so this overstates the joint-life annuity value
and understates the rider's cost, and no delib source quantifies the dependence. The
*Anwartschaft* lapsing on the second life's prior death needs no separate rule — `l_s(t)` is
already zero in that state — and nothing is refunded, the cover having been consumed.

## The *Überschussrente* steps at the anniversary and ratchets

The annuity paid is `garantierte Rente + Überschussrente`, and **only the first is a
promise**: in payment the RfB-funded part supports "eine lebenslang zahlbare Rente, deren Höhe
jedoch nicht garantiert ist. Die hieraus gezahlten Renten sind jeweils nur für ein
Versicherungsjahr zugesagt" [S2], and it may be reduced [S6] [R21]. The second is declared out
of surplus actually earned, and the model carries two properties of it that are easy to get
wrong on a monthly grid:

- **It steps at the policy anniversary and nowhere else** — "erstmals zum Ende des ersten
  Versicherungsjahres" [S4], "am Ende des Versicherungsjahres" [S10], [S15]. Compounding an
  annual rate monthly is the obvious wrong reading; `check_annuity_roll_fwd_resid(t)` leaves a
  residual at every `t` that is not a multiple of twelve if you do.
- **It ratchets.** An increment bought as paid-up annuity under the *Bonusrente* mechanic does
  not come back off — "Die jeweils erreichte Rentenhöhe kann nicht mehr sinken" [S4] — so
  `annuity_pp(t) ≥ annuity_pp(t − 1)` at every `t`. **The model's ratchet is a modelling
  choice, not a universal**: it holds for the dynamic form, whereas the constant and
  teildynamic forms may be reduced [S2] [S6] [R19], which the base run does not project.

The *Überschussverwendung* forms are a **profile**, not separate mechanics: the constant
form opens highest and is flat, the volldynamic form opens at nothing and rises with each
declaration, the teildynamic form is intermediate on both axes, and the *Bonusrente* is the
crediting mechanic underneath the rising ones. **The three market forms are not calibrated to
equal present value here**, and a user who needs them to be must do that calibration;
asserting equality would be a wrong test rather than a right one. Nor does the base run
**reduce** a declared *Überschussrente*, which is what the consumer literature says happens
to the *konstante* form when the insurer earns less than projected [R21] — the notes'
sensitivity section prices that downside instead.

On the anchor cell the whole modelled *Überschussrente* is **10 617,37 €** undiscounted over
fifty-six years, against a guaranteed stream of 90 804,02 €. It is also what turns the sign
of the undiscounted total: model point 14 is the anchor with the surplus switched off and
collects 1 869,74 € more than it pays, where the anchor pays out 8 747,64 € more than it
collects. Neither figure is an economic result — these are undiscounted flows — but the
difference between them is exactly the quantity the four forms distribute.

## The mortality surface is generational, and the tariff is unisex

Two separate objects, and conflating either with its neighbour is a listed pitfall.

**Generational, not period.** `q` is read at `(attained age, birth cohort)`, never at
`(attained age, projection year)`: `birth_year` is its own model point attribute and is never
derived from the calendar [R10] [REG-R49]. The model builds
`q(x, sex, cohort, basis) = q_table(x) (1 − λ(x))^(cohort + x − 2025)`, so the shipped tables
are the period tables of 2025 and the exponent is the calendar year in which the life attains
age `x`, less 2025. It may be **negative** — an in-force point issued in 2012 attains its ages
before 2025 and reads heavier mortality — and it is not floored. Rebuilding the anchor's
annuity factor with `λ ≡ 0` gives **250,6755** against 263,5711, so a period proxy would
overstate the annuity a given *Einmalbeitrag* buys by **5,1 %** — 381,32 € rather than
362,67 € — on that account alone, which dwarfs every other assumption in the model.

**First order for pricing, second order for the projection.** `mort_rate_tariff` is
first-order and unisex and is used only inside the pricing sums; `mort_rate` is second-order
and sex-specific and drives the decrement. The *Sicherheitszuschlag* between them is
**two-dimensional** — 20 % lighter in level (`SECOND = 1.20 × FIRST`) and improving 25 %
faster (`λ_FIRST = 1.25 λ_SECOND`) — because prudence in an annuity table must reach the rate
of improvement as well as its level [REG-R47]. The consequence is visible: the ratio
`mort_rate_tariff / mort_rate` is 0,66667 at `t = 0` and 0,63843 at `t = 240`, where a
level-only margin would hold it constant. Collapsing the two bases destroys the systematic
*Risikoüberschuss* the *Überschussrente* is largely financed from.

**Unisex.** German new business has had to be unisex since 21 December 2012 [REG-R34], so
the tariff factor is struck at `table_sex = "U"`, a `mix_male = 0.45` blend of the
sex-distinct series computed in the model and never a row of the CSV, because no real
sex-distinct table carries one. Letting `sex()` into the tariff reproduces a tariff unlawful
in Germany. The direction of `ρ_M` is argued and its magnitude is not observed, and **no
German carrier publishes a mix** (research gap 13).

## Payment frequency, timing and the *Aufschubzeit*

Instalments are paid at the **start** of a payment month and a payment is made if the payee
is alive at that same instant, so the survival index of a payment is `t` under both timings
and the two conventions differ **only in which months carry an instalment**: under `advance`
the first falls at `defer_mths()`, under `arrears` at `defer_mths() + 12/payment_freq`. A
`G`-year guarantee covers `G × m` instalments at every frequency and under both timings,
which is why `guar_end_mth()` is `first_pay_mth() + 12 G` and not a frequency expression.

The *nachschüssig* variant is measurable rather than assumed, because model point 9 is the
anchor cell with nothing else changed. Its tariff factor is 262,6686 against 263,5711, and
the whole of that 0,9026 difference is checkable in one line: arrears does not pay the
instalment at `t = 0`, worth 1; against that, its guarantee window is `1 … 120` rather than
`0 … 119`, so the instalment at `t = 120` is certain for it and survival-contingent for
advance, worth `v¹⁰ (1 − l̃(120)) = 0,0974363`. The guaranteed annuity rises in exactly the
inverse proportion, by **0,34 %** — not the 5 % of `_research/sofortrente.md` section 8,
which is an annual-annuity identity applied to a monthly one. The research file is frozen and
is not amended; the correction is recorded in the technical notes. The *Aufschubzeit* is
implemented and off in the base run, and all three of its effects fall out of the pricing sum
without a second mechanic: interest accrues, mortality accrues so the survivors share the
fund of those who died, and the annuity starts at an older age.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Sofort_DE_S/` holds nothing but formulas:

```
products/sofortrente/
  model_point_table.csv  mort_table.csv  improvement_table.csv      <- inputs live here
  surplus_scale_table.csv  hoechstrechnungszins_table.csv
  run.py  model.md  product-spec.md  technical-notes.md  sources.md
  Sofort_DE_S/                     <- formulas only
    __init__.py  _system.json         (the model docstring, and the serializer version)
    Data/__init__.py                  (reads the CSVs, once per model)
    Projection/__init__.py            (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input file beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory and
no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache, and readers placed there would re-read every file for every model
point. They live instead in an unparameterized **`Data`** Space, which `Projection` references
as `data`, so each file is read once per model however many points are projected. The
conventions suite counts the reads and asserts the file set.

| File | Reference / Cells | Contents and provenance |
|---|---|---|
| `model_point_table.csv` | `model_point_file` / `model_point_table()` | Fourteen points. **Point 1 is the worked-example anchor cell** (100 000 €, M65 born 1960, 2025 vintage, 10-year *Rentengarantiezeit*, monthly *vorschüssig*, `i = 1,00 %`, *teildynamisch*), **[std]**; points 2–14 exercise the plain *Leibrente*, each death-benefit option, a joint-life cell, all four frequencies, both timings, all four surplus forms, a five-year *Aufschubzeit*, an in-force cell with a given annuity, a 0,25 %-era vintage, both ends of the age envelope and the surplus switched off. The only file without a `provenance` column: a model point is a configuration, not an assumption |
| `mort_table.csv` | `mort_table_file` / `mort_table()` | Annual death rates by `(basis, sex, age)` in four series, `{FIRST, SECOND} × {M, F}`, ages 50–120. A **[std]** Gompertz–Makeham proxy and **not DAV 2004 R**, which is DAV property and is cited by name, never shipped [R10] [REG-R49]. **The anchor a replacement must preserve** is that the `mix_male = 0.45` blend of the FIRST series reproduces the research file's own `q_base(x)` — to 2,5 × 10⁻⁷ relative, the female factor being a six-decimal rounding of `0.4375/0.55` |
| `improvement_table.csv` | `improvement_file` / `improvement_table()` | The *Trendfunktion* `λ(x)` by `(basis, age)`: **[std]** 1,5 % a year to age 70 on the second-order basis, tapering linearly to zero at 105, with the first-order basis improving 25 % faster. DAV 2004 R's own trend is **not public and was not reachable** — the DAV derivation and the contemporaneous expositions are members' and conference materials with no open address [R10] [R12] |
| `surplus_scale_table.csv` | `surplus_scale_file` / `surplus_scale_table()` | `surplus_init_pct` and `surplus_growth` for the *Überschussverwendung* forms. **[std]** and **uncalibrated**: one carrier group's payout-phase declaration is now in the corpus — 3,35 % less the *Rechnungszins* for 2026, interest surplus only [S10] — and one carrier's realised increase, 0,75 % for 2024 [S8], but neither was used to set these values and the shipped two-component shape does not match either. The corpus still gives no range [R21] [R22] (research gap 4 narrows) |
| `hoechstrechnungszins_table.csv` | `hoechstrechnungszins_file` / `hoechstrechnungszins_table()` | The statutory rate history by vintage band [REG-R14] [REG-R15]; the two mid-year steps of 1994 and 2000 are assigned **[std]** to the rate in force on 1 January of the split year |

**No input file is keyed by the frame's `t`,** so the move to the 0-based convention left every
CSV byte-identical. The time-like columns and why each stands: `mort_table.csv` and
`improvement_table.csv` key on `age`, an **attained age** read at `age(t, life)`;
`hoechstrechnungszins_table.csv` keys on `year_from`/`year_to`, **calendar years** matched
against `entry_year()`; and in `model_point_table.csv`, `entry_year`, `birth_year` and
`surv_birth_year` are calendar years, `entry_age` and `surv_age` are ages, `defer_years` and
`guar_years` are contractual **durations in years**, and `duration_mth_init` is an **elapsed
count** of months — already 0-based by nature, and the frame's first `t` exactly because a
count of completed months and a 0-based month index are the same number.

Every file but the model point table carries a final `provenance` column, one tag per row, per
the library's second ruling. `Data.input_dir()` resolves the location from `_model.path.parent`
when the model is read, so it works wherever the repository is checked out. **The trade-off:**
the model is not portable on its own — copy `Sofort_DE_S/` without the CSVs and it reads fine,
then fails on first evaluation. What you gain is that a diff of the model shows logic changes
only, and an input can be swapped in place with no formula change.

## The published identities

Nine `check_*` cells, each taking no argument and returning one `bool` over all `t`, with the
per-period residual at `check_*_resid(t)`. The library's first ruling makes the first
mandatory; the rest are this product's own. **`check_net_cf`, in one line** — delib ruling 1:

```
net_cf(t) == premiums(t) − 1{payment month}·pols_if_init·annuity_pp(t)·payment_factor(t)
             − claims(t, "REFUND") − expenses(t)
```

That is **not a restatement of the definition**. `net_cf` reaches the instalment outgo
through the two *published* legs — `annuity_payments(t)` and `claims(t, "GUARANTEE")` —
while the identity rebuilds it through the single `max()` payment factor, so what it asserts
is that the split into those legs is **exhaustive and non-overlapping**. A survivor's annuity
paid on top of a guaranteed instalment, or a certain floor counted additively, leaves a
residual. The instalment term carries the payment-month indicator because `payment_factor(t)`
is defined at every `t` while only some `t` carry an instalment on a quarterly, half-yearly
or annual point.

The other eight: `check_lives_roll_fwd` (the survival recursion, and the closure
`Σ_t lives_death + lives_if(n+1) == lives_if(t₀)` built by direct summation for each life in
scope); `check_annuity_roll_fwd` (the anniversary step and the *Bonusrente* ratchet);
`check_refund_run_off` (one guaranteed instalment per payment month, non-increasing, zero by
the end, and the independent `⌈SP/R⌉` count — identically zero where no refund was bought);
`check_payment_factor` (the three legs partition the instalment); `check_guarantee_certain`
(`payment_factor(t) == 1` inside the *Rentengarantiezeit*, whatever `δ`); `check_equivalence`
(`SP_net == R ä (1 + β) + refund_pv()`, to `roll_fwd_tol` **scaled by `net_single_prem()`**,
the identity being an equality between euro amounts of order 10⁵ while the refund solve
converges on `R` rather than on the residual); `check_death_option_xor` (the **[std]**
exclusivity of the death-benefit families, asserted rather than assumed); and
`check_tariff_int_rate` (an **inequality** against the cap of the contract's own vintage,
because § 2 DeckRV sets a maximum and not a rate [REG-R14]; every tariff retrieved for this
product in fact prices **at** its vintage's cap [S2] [S4] [S6], so the inequality is the right
test for the right reason and not because below-cap pricing was observed).

## Modules that are off in the base run

Five constructions are implemented and switched off, so the base run reproduces the worked
example while the machinery stays visible and testable. Each is switched on by a **model point
column** rather than by a Space Reference, because on this product every option is elected
once at inception and is thereafter a parameter rather than a decision.

| Module | Switch | Off value | On at | What it does |
|---|---|---|---|---|
| *Rentengarantiezeit* | `guar_years` | 0 on points 2–4, 6, 11 | 10 y on point 1; 5–30 y across points 5, 7, 8, 10, 12, 13 | Makes `certain_floor(t)` 1 for `12 G` months, so the instalment is payable whether the annuitant lives or not [R23] |
| *Kapitalrückgewähr* | `refund_form` | `none` | `full` on points 3 and 6 | Adds the implicit refund leg to the pricing equation and settles `max(SP − C(t), 0)` on deaths during month `t` |
| *Hinterbliebenenrente* | `surv_pct` | 0,00 | 0,60 on point 4, 1,00 on point 5 | Brings a second life into the projection, gates its leg by `(1 − γ(t))`, and extends `proj_len()` to that life's horizon [S9] |
| *Aufschubzeit* | `defer_years` | 0 | 5 on point 6 | Moves `first_pay_mth()`, accrues interest and mortality before *Rentenbeginn*, and makes the refund the whole *Einmalbeitrag* inside the window |
| *Überschussrente* | `surplus_form` | `none` on point 14 | `teildynamisch` on the anchor; `konstant` and `volldynamisch` elsewhere | Adds `R u₀ (1 + ψ)^k` from the first payment month, stepping at the anniversary and ratcheting |

Two further constructions are described in the sources and are **not implemented**, each for
a stated reason: a **commuted settlement of the *Restgarantiezeit***, whose basis was not
established at any carrier (research gap 10), so implementing it would mean inventing the
basis rather than modelling it; and the ***Bewertungsreserven*** share, which does continue
in the payout phase [S3] [REG-R24] but is a function of the HGB balance sheet and the
*Sicherungsbedarf* test [REG-R9] rather than of this policy's path, so it belongs to a layer
that consumes these cash flows.

## Sign convention

`net_cf` is **income positive** — the *Einmalbeitrag* in, instalments, death benefits and
expenses out — which is the library-wide sign. `liability_cf` publishes the same stream
outgo-positive, the technical notes' own orientation, with `net_cf(t) = −liability_cf(t)`
exactly, and both are columns of `result_cf()` so the identity is verifiable in the frame
rather than only in prose. A Solvency II best estimate is `Σ v(t) × liability_cf(t)` over
whatever risk-free term structure the valuation layer supplies, plus a risk margin [REG-R1]
[REG-R4] [REG-R6]; nothing in this library discounts. The shape to expect on a new-business
point is one large positive month at `t = 0` — the whole *Einmalbeitrag* against a single
instalment and the acquisition expense, 97 394,57 € on the anchor cell — and a long negative
tail decaying with survival, which is what a *Deckungsrückstellung* is held against and which
this model does not compute.

`expenses` is the notes' total: acquisition at `t = 0`, maintenance on `pols_if(t)`, and the
per-instalment cost on `payment_factor(t)` — the last is not a slip, because a survivor's
annuity in payment is a **second** payment run and a beneficiary's guaranteed instalment
costs the same to pay as the annuitant's. The tariff *loadings* `expense_load_alpha` and
`expense_load_beta` are pricing parameters and appear only in the equivalence; the gap
between the loadings and the expenses is the modelled *Kostenüberschuss*, 300,00 € at
inception on the anchor cell.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those
models have an analogue — `pols_*` for exposure, plural nouns for cash flows, `*_rate` for
rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase `kind` string, and
`check_*()` returning one bool over all `t` with the residual at `check_*_resid(t)`. Beyond
that, this model sits on the **payout-annuity chassis** the repository already has in
`uslib/immediate_annuity/SPIA_US_S`, `uklib/pension_annuity/PA_UK_S` and
`frlib/rente_viagere/Rente_FR_S`: `duration_mth`, `horizon_mths`, `is_payment_mth`,
`certain_floor`, `payment_factor`, `lives_if`, `lives_death`, `annuity_pp`,
`annuity_payments`, `check_lives_roll_fwd` and `check_payment_factor` mean the same thing on
all four, and `result_pols()` is the same second frame. `payment_surv_mth` and
`payment_factor_life`, which those three carry to separate the survival index of a payment
from the month it falls in, are **absent** here: the payment instant is the start of month
`t` under both timings, so the two indices coincide and a second cells would only restate
`lives_if`. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l(t)` and the exposure weight | `lives_if(t, life)` / `pols_if(t)` | They are **different quantities** here. `lives_if` is a survival probability per life; `pols_if` is the probability that a payment **obligation** remains — 1 while the guarantee runs or the annuitant lives, and positive after the annuitant's death while a survivor's annuity can still come into payment. The conventions suite exempts a payout product's `pols_if` from the policy-count reading **by docstring**, so the exemption is earned in the file rather than granted by a list |
| `R`, `U(t)`, `A(t)` | `annuity_guar_pp` / `annuity_surp_pp` / `annuity_pp` | Three amounts, one per cells: the immutable *garantierte Rente*, the declared *Überschussrente*, and their sum. Publishing only the first models less than the payment; publishing only the third loses the distinction between a promise and a declaration |
| `q⁽¹⁾(x)`, `q⁽²⁾(x)` | `mort_rate_tariff` / `mort_rate` | **Different objects, not two readings of one table**: first-order unisex for pricing, second-order sex-specific for the projection. `mort_rate` is the library's shared name and takes the projection basis, as it does in every other delib model |
| `C(t)` | `cum_annuity_guar_pp` | Deliberately *not* `cum_annuity_pp`, the name `SPIA_US_S`, `PA_UK_S` and `Rente_FR_S` use, because it accumulates the **guaranteed** instalment alone. The longer name is the [std] refund-basis decision made visible at the point of use |
| `ä` | `annuity_factor` | The notes' `ä`, and **not** the market's `a12`: `a12 = annuity_factor() / payment_freq()`, so the research file's `a12 = 20,426` is `annuity_factor() = 245,11`. `Rente_FR_S` carries the same name for the **French** unit — the value of one unit of *annual* rente, `sum(l(t) v^t) / 12` — so its `annuity_factor` is this model's `a12` and not this cells |
| `l̃(k)` | `tariff_lives` | The first-order survival path, used only inside the pricing sums and running from inception whatever `t_start()` is. Kept apart from `lives_if` so that the equivalence stays acyclic |

## Standardizations used

Everything in this table is **[std]**: a parameter or convention chosen for the reference
implementation where the corpus is silent. None is any carrier's value, and for this product the
list is longer than for any other in the library. The drafting pass ran **no search for it at
all** (research gap 1); the 2026-08-30 re-verification then opened 19 of this product's 32
sources and reached its mechanics and almost none of its levels — one carrier's annuity scale
[S8], one carrier group's surplus declaration [S10], and no charge parameter anywhere — so the
table stands.

| [std] | Value | Rationale |
|---|---|---|
| Mortality proxy | `q_base(x) = 1 − exp(−(A + B c^x (c−1)/ln c))`, `A = 0.0002`, `B = 1.5e-5`, `c = 1.10` | The research file's own printed law, life expectancy 24,29 years at 65 — a **prudent annuitant** shape of the right order for a German first-order basis. DAV 2004 R is DAV property and is not shipped [R10] [REG-R49]. **Measurably lighter than a real tariff basis**: on the one carrier quotation now in the corpus the constructed annuity is about **16 % high** [S8], and the model is not refitted to it here |
| Sex split | `FIRST/M = 1.250000 q_base`, `FIRST/F = 0.795455 q_base` | Chosen so the `mix_male` blend reproduces `q_base` itself, which is what lets every annuity factor printed in the research file be traced into this model. Exact to 2,5 × 10⁻⁷ relative |
| First-order level margin | `SECOND = 1.20 × FIRST` | The direction is established — prudent means *lighter* for an annuity [R10] [REG-R47] — and the size was not (research gap 12) |
| Closing row and cap | `q = 1` at attained age 120; every series capped at 1.0 | Forces the survival path to zero inside the `omega_age` horizon. The cap binds only on `SECOND/M` at ages 117–119, where `1.20 × FIRST` would stop being a probability |
| *Trendfunktion* | `λ_SECOND = 1,5 %` to age 70, tapering linearly to 0 at 105 | A plausible German annuitant improvement shape; DAV 2004 R's own trend is not public [R10] [R12] |
| First-order trend margin | `λ_FIRST = 1.25 × λ_SECOND` | Prudence for an annuity must reach the **rate** of improvement, not only its level [REG-R47]. The size is the modeller's view |
| `mort_base_year`, `omega_age` | 2025; 121 | The base year makes the shipped tables the period tables of 2025, so the anchor's cohort exponent at 65 is exactly zero; the limiting age is an upper bound the proxy reaches zero survival before |
| Monthly rates | `1 − (1 − q)^(1/12)` | A uniform force of mortality across the policy year, under which twelve monthly survivals compound back to the annual one exactly |
| `mix_male` ρ_M | 0.45 | A **direction with no magnitude**: a unisex tariff on sex-distinct tables favours women, so a voluntary annuitant portfolio's female share exceeds the population share [REG-R34]. No carrier publishes a mix (research gap 13) |
| `expense_load_alpha` α | 2,5 % of `SP` | A single-premium annuity's acquisition cost is one commission plus an issue expense, with no premium stream to amortise against. **No charge parameter was established at any carrier** (research gap 8) |
| `expense_load_beta` β | 2,0 % of the annuity value | Covers a payment run whose per-policy cost is roughly constant in euros — right on 100 000 €, too small on 25 000 €, which is itself why minimum *Einmalbeiträge* exist |
| Acquisition expense | 2,0 % of `SP` + 200 € | Sized so the tariff over-recovers modestly, which is the right direction and the source of the modelled *Kostenüberschuss* — 2 500 € taken against 2 200 € incurred on the anchor cell |
| Maintenance / payment expense | 60 € a year on `pols_if`; 1,50 € per instalment | The two running costs a payout annuity actually has: the annual *Standmitteilung* and proof-of-life routine, and the payment run itself. Both fall on the insurer by the AVB — "Vor jeder Rentenzahlung können wir **auf unsere Kosten** einen amtlichen Lebensnachweis … verlangen" [S4] [S2] — so the direction is sourced; **the levels are not** [S15] |
| `expense_infl` | 1,5 % p.a., stepping at the **policy anniversary** | Every step in this product falls on an anniversary; nothing happens on 31 December |
| Surplus scale | `konstant` 20 %/0 %; `teildynamisch` 10 %/1,0 %; `volldynamisch` 0 %/2,0 % | The corpus gives the *shape* [R19] [R21] and the 20 % opening share sits mid-way in the 15–25 % gap between guaranteed and total annuity, which **no retrieved document quantifies** and which stays [unverified]. The growth rates are round numbers consistent with a *Zinsüberschuss* of one to two points over a 1,00 % *Rechnungszins* — a shape [S10]'s declared 2,35 % for 2026 supports without validating these numbers, which were **not derived from it**. **Not calibrated to equal present value, and not calibrated to any carrier's declaration** |
| Surplus increase date | The policy anniversary | No specimen *Rentenanpassungsmitteilung* was located [S15], but the rule is now read at four sources: "erstmals zum Ende des ersten Versicherungsjahres" [S4], "am Ende des Versicherungsjahres" and "für den Monat vor dem Jahrestag der Versicherung" [S10], "jedem Versicherungsjahrestag" [S6]. **No longer a standardization in substance**, only in the absence of a specimen |
| Refund basis | Netted against the **guaranteed** instalments | **No longer a standardization**: two AVB state it — "bereits gezahlte Renten werden nur in der Höhe der zu Vertragsbeginn garantierten Renten abgezogen" [S2], "abzgl. der bis zum Todeszeitpunkt gezahlten garantierten Renten" [S6]. The modeller's argument turned out to be the market's rule |
| Death-benefit exclusivity | Refund **xor** (guarantee period, survivor's annuity) | Which carriers permit the combination was not established (research gap 10), and the refund's implicit equation is written against a plain annuity leg |
| Payment timing | *vorschüssig*, first instalment at `t = 0` | **Contradicted by the retrieved market and retained anyway.** Two AVB pay in arrears — "Die erste Rente wird einen Monat nach dem vereinbarten Versicherungsbeginn gezahlt" [S4], and one payment period after inception at [S6]; the GDV template does not settle it [S1]. Moving the default moves the worked example and the golden tests, so it is reported rather than changed (`technical-notes.md`, correction 6). Model point 9 measures the alternative at 0,34 % |
| Joint-life dependence | Independent lives | Real joint lives are positively dependent, so this **overstates** the joint-life annuity value and understates the rider's cost. No delib source quantifies it |
| Age basis | `entry_age + t // 12`, with `entry_year == birth_year + entry_age` on every shipped point | An internal-consistency convention, not a contract fact; a real book carries a fractional offset of up to a year |
| *Höchstrechnungszins* split years | 1994 and 2000 assigned to the 1 January rate | The statutory steps fall mid-year and a model point carries one vintage [REG-R15]. `kapitallebensversicherung/deckrv_table.csv` resolves the same two years to the **higher** of the pair instead, so the two tables agree on 2000 and differ on 1994 — 3,50 % here, 4,00 % there. Neither is derivable from [REG-R15], so the divergence is recorded here and in this file's `provenance` column rather than silently reconciled. No delib model point in either product carries a 1994 vintage — the earliest anywhere in the library is 2005 — so no shipped number turns on it |
| Annuitant selection, proof of life | No adjustment factor on the first-order table; suspension not modelled | DAV 2004 R is an annuitant-experience table understood to carry *Selektionsfaktoren* already [REG-R49], so selection belongs inside the basis; a failed life certificate is a timing effect on an unchanged obligation |
| Tolerances | `roll_fwd_tol = 1e-8`; `solve_tol = 1e-10`; `solve_max_iter = 200` | The refund solve is the only numerical solve in the model, so `solve_tol` is a change of answer rather than of runtime |
| Commercial envelope and model points | Entry ages 60–85; *Einmalbeitrag* 25 000–500 000 € around 100 000 €; fourteen cells | One carrier's limits are now read and the envelope is **not** moved to them: Allianz takes a *Mindesteinmalbeitrag* of **3 000 €** and a *Höchsteintrittsalter* of **85** [S7], so the age ceiling matches and the ticket floor is an order of magnitude conservative. No upper ticket limit and no lower entry age was established anywhere (research gap 7). The anchor is the notes' worked example; the rest exercise one mechanic each |

The only quantities in this model that are **not** standardizations are structural, and each
is now carried by clause text: the conversion at inception on a first-order annuitant table at
a rate at or below the statutory cap [S2] [S4] [REG-R14] [REG-R15]; the guaranteed annuity's
immutability thereafter [REG-R27]; the guarantee period paying regardless of survival [S1]
[S4]; the refund being the *Einmalbeitrag* less the **guaranteed** instalments paid [S2] [S6];
the survivor's annuity being a rider that begins after any guarantee period [S1] [S9]; surplus
participation continuing through the payout phase, *Bewertungsreserven* *hälftig* [S2] [S3]
[S10] [REG-R24]; the anniversary as the only step date [S4] [S6] [S10]; and the absence of any
surrender, lapse or paid-up state at any duration [S1] [S2] [S4] [R1] [R2] [R5] [REG-R28].

## Tests

`tests/test_sofortrente_de.py` asserts the technical notes' worked example — every printed
row of the anchor cell's 672-month frame to the cent, `pols_if` to six decimals, and the
totals summed at full precision rather than from the rounded cells, which differ by 17 cents
on `net_cf` and which the test asserts too — the derived quantities and the annuity factor
behind them, the notes' three independent rebuilds and its two closure identities, the
*nachschüssig*, in-force and surplus-off variants, every `check_*` identity with its residual,
and **one test per listed modeling pitfall**, eighteen of them.

The single sweep over the whole model point table belongs to
`tests/test_model_conventions_de.py`, which is also where every `check_*()` is called on
every point, so this module does not repeat it.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-sofortrente-r1
[R10]: #delib-sofortrente-r10
[R11]: #delib-sofortrente-r11
[R12]: #delib-sofortrente-r12
[R19]: #delib-sofortrente-r19
[R2]: #delib-sofortrente-r2
[R20]: #delib-sofortrente-r20
[R21]: #delib-sofortrente-r21
[R22]: #delib-sofortrente-r22
[R23]: #delib-sofortrente-r23
[R5]: #delib-sofortrente-r5
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R24]: #delib-reg-r24
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R4]: #delib-reg-r4
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R6]: #delib-reg-r6
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
