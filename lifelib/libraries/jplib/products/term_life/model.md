# Implementation Notes

**Status:** Draft, 2026-08-20. Built from [`technical-notes.md`](technical-notes.md); the
product those notes describe is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced: attained-age repricing at renewal (*kōshin*, 更新)
> with no health declaration (*kokuchi*, 告知), truncation at the renewal ceiling into an
> 80歳満了 term, the to-a-stated-age (*sai manryō*, 歳満了) shape never renewing, the
> absence of any surrender value (*kaiyaku-henreikin*, 解約返戻金) and hence of
> automatic premium loan (*jidō furikae kashitsuke*, 自動振替貸付), and the
> living-needs acceleration (a *tokuyaku*, rider — リビング・ニーズ特約)
> discount and per-insured cap. So,
> unusually for this repository, is the **premium**: carriers publish rate cards, and the
> anchor cell's ¥974 a month is a published figure [S2]. Everything else is **[std]** —
> the mortality factor, the lapse curve, the renewal-decline rate, the expense and
> commission levels, the premium scale above age 50 — and `mort_table.csv` is a documented
> **proxy** for 生保標準生命表2018（死亡保険用）, not that table. Replace it all with
> company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/term_life/run.py
python products/term_life/run.py 7        # another model point
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/term_life/Term_JP_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by the projection **month** `t`, one column per cash
flow line; `result_pols()` prints the counts, decrement rates, term index and premium beside
them, which is where a renewal boundary becomes legible — the row whose `decline_rate` is
non-zero and whose `prem_pp` changes on the next row. `model.Projection.doc` carries the
notes' symbols mapped to the cells names.

## The time index is 0-based and counts months

`t` follows the library-wide convention and its unit is the **policy month**: `t = 0` is
the first projected month, the frame is `range(proj_len())`, the last index is
`proj_len() - 1`, and `len(result_cf()) == proj_len()`. `proj_len()` is therefore the
**number** of projected months, not the last index; on the anchor cell it is 600 — fifty
years, twelve rows each — and `result_cf()` is indexed `0 .. 599`. Attained age is
`age(t) = age_at_entry() + t // 12`, so `age(0)` is the 契約年齢 itself and holds for the
twelve months of policy year 1, and `pols_if(0) == pols_if_init() == 1`.

The **contractual policy year is the 1-based label `policy_year(t) = 1 + t // 12`**, and
`duration(t) = t // 12` is the count of completed policy years; both are derived, never
indexed by. Two 1-based labels stay 1-based because they are contractual rather than
positional — the term index `term_index(t) = 1 + duration(t) // policy_term()` (`k = 1` in
the original 保険期間) and the `policy_year` key of `lapse_table.csv`, which `lapse_rate(t)`
reads at `policy_year(t)`.

The renewal boundaries — the **last month** of each 保険期間 — are `t = 119, 239, 359, 479`
on the anchor cell, i.e. `(t + 1) % term_months() == 0` where `term_months() = 12 n`, and
the repriced premium is first charged on the following row. `pols_if(t)` is additionally
defined at `t = proj_len()`, one row beyond the frame, where it is the survivors whose
cover expires at the ceiling (`pols_if(600) = 0.026042` on the anchor cell).

`result_cf()` reads back as an annual statement with `df.groupby(df.index // 12).sum()`.

## What the monthly grid changed, and what it did not

The contract is quoted in years — the 保険期間, the ceiling, the lapse curve, the mortality
table — so the monthly step is finer than the guarantees rather than finer than the
product. Four things follow.

**Rates convert; one-off proportions do not.** `mort_rate` and `lapse_rate` are the annual
rates the tables are stated on, and `mort_rate_mth` and `lapse_rate_mth` are the decrements
actually applied, on the effective convention `1 - (1 - r)^(1/12)`. `decline_rate` is
neither: it is the proportion of survivors who walk away when a 保険期間 ends, applied
unconverted in that one month.

**`pols_if` at the anniversaries did not move.** Because the conversion is the effective
one, `pols_if(12 j)` here equals the annual-step model's `pols_if(j)` to floating point —
`l(120) = 0.466683` and `l(600) = 0.026042`, the same two numbers. Every difference between
the two runs is a difference of cash flow **timing**, never of decrement basis.

**`premium_mode` became live.** The annual model annualized every mode into one
start-of-year payment and carried the column inert; `prem_mode_months()` and
`prem_due_pp(t)` now pay 月払 monthly, 半年払 every sixth month and 年払 every twelfth.
`prem_pp` survives as the annualized **pricing** quantity — the repricing rule, the
commission scale and the renewal ladder are all quoted per annum — and is no longer the
cash flow.

**One [std] was retired rather than restated.** The annual model collected a whole year's
premium in advance from lives that might exit in month two and offset that against claims
booked at the end of the year, declaring the pair matched. Neither approximation survives
here, so neither offset is needed — and the anchor cell's undiscounted premium falls from
¥470,348.54 to ¥457,507.04 as a result.

### CSV time-like columns

| File | Column | Decision |
|---|---|---|
| `lapse_table.csv` | `policy_year` (1 … 5) | **Unchanged.** A contractual 1-based policy-year label, not the frame's `t`; `lapse_rate(t)` maps through `policy_year(t) = 1 + t // 12` and carries the last row forward. The rates stay **annual**; `lapse_rate_mth(t)` derives the month's decrement |
| `mort_table.csv` | `age` (20 … 80) | **Unchanged.** Attained age, not a time index; read through `age(t)` |
| `prem_rate_table.csv` | `issue_age`, `term_y` | **Unchanged.** An entry age and a term length, not points on the frame |
| `model_point_table.csv` | `issue_age`, `term_y`, `expiry_age`, `renew_ceiling` | **Unchanged.** Ages and term lengths. The table carries no duration, in-force offset or frame-position column — every model point is projected from issue at `t = 0` |

**No CSV value changed in the conversion to the monthly grid either.** Every input is
quoted in the unit the contract or the source states it in — an annual rate, an attained
age, a term in years — and the conversion to a month happens in the projection, once, where
it can be named.

## The horizon is the renewal ceiling, not the term

This is the structural difference from the UK and U.S. term models in this repository, not
a parameter difference. A fixed-year (*nen manryō*, 年満了) 更新型 contract **renews
automatically** at the end of every policy term (*hoken kikan*, 保険期間) unless the
policyholder gives notice, with no 告知 and no fresh underwriting, and the premium is
recomputed on attained age at the scale then in force [S1] [S4] [S8] [S12]. So
`proj_len()` is `12 × (renew_ceiling() - age_at_entry())`, not `12 × policy_term()`: a
ten-year term issued at age 30 is projected for **fifty** years — 600 months — across five
separately priced terms.

Three cells carry it. `term_index(t)` is the notes' `k`, the state variable a Japanese
term model needs and a UK one does not, because the premium is a function of the term
rather than of the projection year; `term_start_age(k)` is the attained age the term is priced
at; and `term_len(k)` is `min(n, w_r - x_k)`, where truncation at the ceiling lives. A
renewal that would carry the policy past attained age 80 renews as an 80歳満了 term
instead [S1] [S2] [S8], so an issue age of 35 has a final term of five years, priced over
its own five, and the projection still ends exactly at 80 — model point 4. Truncation
shortens the **term**, not the horizon; three other market rules exist [S4] [S7] [S12] and
importing one would change it.

A 歳満了 contract never renews [S1]: `term_index` is 1 and `decline_rate` zero in every
month, and `proj_len()` is `12 ×` the term. Model points 3, 6 and 9 are 歳満了.

Nothing else resets at a boundary. `pols_if` is continuous across it; no acquisition
expense and, in the base run, no commission is paid; and the suicide and contestability
clocks run from the original risk commencement date (*sekinin kaishi bi*, 責任開始日) and
do **not** restart [S1] [S4] [S7] [S8] — only reinstatement (*fukkatsu*, 復活) restarts
them [S1]. Neither clock is monetized, so neither is a cells, but treating a renewed term
as a fresh policy gets persistency, the strain pattern and both clocks wrong at once.

## Renewal decline is its own decrement

`decline_rate(t)` is non-zero **only** in a boundary month, and the lives it removes are
taken **after** mortality and **after** ordinary lapse — the notes' steps 3, 4 and 5,
exposed as `pols_if_at(t, "BEF_LAPSE")` and `pols_if_at(t, "BEF_DECLINE")`. In the month it
applies it dwarfs the other two: at `t = 119` on the anchor cell it removes 0.08235591 of
the 0.08474749 lives that leave, **97.2%** of that month's exits. The annual grid could
only say 74%, because it was comparing one renewal decision with twelve months of ordinary
lapse. Folding it into `lapse_rate` makes the boundary invisible and mis-times most of the
cohort's departure, so it has its own proportion, its own count (`pols_decline`) and its own
term in the roll-forward check — and it is never converted to a monthly rate, because it is
a decision taken on a date.

Two behaviours roll into the one rate: the policyholder who gives notice, and the one
whose **first renewed premium goes unpaid through grace**, where the renewal is treated as
never having happened and the contract terminates at the original expiry [S1] [S7]. Only
the first is a decision. Both leave at the boundary, and neither may appear in force at
`t + 1` collecting the renewed premium — which is what the processing order enforces. The
monthly grid makes the second *representable* for the first time, since grace is about a
month long [S1] [S8]; separating them would need a take-up assumption the sources do not
give, so the composite keeps one rate.

## One decrement, one benefit

生保標準生命表2018（死亡保険用）**includes 高度障害** (*kōdo shōgai*, severe disability)
inside its death rate [REG-R20], and the contract pays one sum assured and terminates on
whichever event becomes payable first [S1] [S8]. `mort_rate(t)` is therefore the combined
decrement and there is **no disability incidence anywhere in this model**; adding one on
top of the table double-counts the benefit, the notes' first-listed pitfall and the same
shape as the terminal-illness ruling in the UK term model. The リビング・ニーズ特約 module
follows the rule too: an acceleration is a re-timing and re-pricing of the death benefit,
not a second claim, so `ln_share(t)` **splits** the decrement rather than adding to it.

## The premium chassis is mostly sourced

Japanese carriers publish rate cards, so the structure decomposes exactly [S2]:

    P_m(k) = f + r(sex, x_k, m_k) * SA / 5,000,000
    P_a(k) = 12 * P_m(k)

with `f = 248` per month and `P_m` rounded half up to the whole yen, which is the
granularity rate cards are quoted at [S2] [S9] [S10]. On this grid `P_m` is the cash flow
and `P_a` the pricing quantity; `prem_mode_months()` decides how many months' worth of
`P_m` fall in a given month. Four cells are sourced — male ages 30, 40 and 50
and female age 30, all at a ten-year term — and `prem_rate_m()` uses the published cell
wherever one exists. Ages 60 and 70 are published by **no** carrier and the anchor cell
reaches both, so the extension off the `is_anchor` row of the matching sex is unavoidable
rather than optional:

    r(sex, x, m) = r_anchor * qbar(x, m) / qbar(x_a, m_a)

Applied where a published cell already exists it back-casts to ¥958.9 a month at age 30
against the published ¥974 (−1.5%) and ¥1,806.4 at age 40 against ¥1,823 (−0.9%); it gives
¥8,976 at 60 and ¥23,881 at 70. That is reassuring about the *form* of the scale and says
nothing about the *level* an insurer will charge decades out — the notes' third-largest
lever. `qbar` averages **table** rates, through `mort_table_mean()`, never the
best-estimate `mort_rate()`: feeding the 0.80 factor into a rate card would move it by an
assumption unrelated to pricing. The ¥248 is likewise a **premium** component and not an
expense recovery [S2]; it enters the model only through `prem_pp()`, and crediting it
against `expenses()` counts it twice.

## `claims_lapse` is a column of zeros, deliberately

There is no 解約返戻金 and no paid-up value at any duration on this composite
[S1] [S4] [S6] [S8] [S9] [S10] [S13] [S14], so an ordinary lapse is a pure decrement: it
moves `pols_if` and pays nothing. `claims(t, "LAPSE")` exists, returns zero and gets a
column in `result_cf()`, because a non-zero lapse row imported from a model with cash
surrender values is one of the notes' pitfalls — and because **one of the eight carriers
whose position is documented does write this design with a surrender value** [S12]. A
Japan term chassis cannot assume the absence the way a UK one can, so the zero is asserted from sources, not from the class.

There is no 自動振替貸付, stated in terms by one carrier [S7], and no collateral for a
policy loan (*keiyakusha kashitsuke*, 契約者貸付) either — the second being an inference from
the missing surrender value rather than a citation, since that same carrier points its
policyholders at the 契約貸付制度 [S7] and the document appearing to rule the policy loan out
could not be extracted [S11]. Importing the APL mechanic that the
[whole life technical notes (終身保険)](../whole_life/technical-notes.md)
carries would create a no-lapse cushion this contract does not have; grace, then force-out (*shikkō*, 失効), then 復活-or-not is the whole persistency machinery.

## Inputs are external files

The model folder holds `__init__.py`, `_system.json` and the two Space directories, and
nothing else — no `_data/`, no IOSpec, no embedded values. The four CSVs live beside
`run.py`: the `annuallife/TradLife_A` layout rather than `basiclife/BasicTerm_S`'s, so a
diff of the model shows logic changes only.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Nine points. Point 1 is the anchor cell (M30 / 年満了 10年 / ceiling 80 / ¥10,000,000, which the premium scale prices at ¥974 a month); the rest carry the female rate cell, both 歳満了 shapes, ceiling truncation, the `current_term` boundary, all three riders and both ends of the issue-age and sum-assured envelopes. **No premium column** — the premium is looked up, not stored, which is what makes the repricing at 更新 fall out of the same lookup | the cells are **[std]**; the price they resolve to at issue is [S2] |
| `mort_table.csv` | Table `qx` by sex and attained age 20–80, 122 rows | the canonical `jplib` **[std]** construction, shared across the library, anchored on rates quoted from [REG-R18] [R4] and log-linearly interpolated between them |
| `lapse_table.csv` | Annual lapse by **contractual, 1-based** policy year (read at `policy_year(t)`), 9 / 7 / 6 / 5.5 / 5 percent, last row carried forward | **[std]** shape; level reconciled to [REG-R31] |
| `prem_rate_table.csv` | Marginal monthly rate per ¥5,000,000 and the ¥248 flat element, four cells, `is_anchor` marking one row per sex | [S2] rate cards, decomposed row by row in `provenance` |

Every assumption row carries a `provenance` column with its tag and, in the premium table,
the arithmetic of the decomposition. The trade-off: **the model is not portable on its
own.** Copying `Term_JP_S/` without its parent's CSVs gives a model that reads and then
fails on first evaluation.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache, and readers placed there would re-read every file for
every model point. They live in the unparameterized `Data` Space instead, where each file
is read **once per model**. `Data.input_dir()` resolves to `_model.path.parent` at run
time, so the model works from any checkout; `prem_anchor_table()` is derived from
`prem_rate_table()` rather than read from a fifth file.

### The mortality table is a proxy, and says so

生保標準生命表2018（死亡保険用）is published by 日本アクチュアリー会 free and in full at a
stable public URL [REG-R18] [R3] [R4] — anyone can retrieve it and check a rate, the
sharpest contrast in this repository with the UK term model, whose CMI tables cannot be
read at all without a subscription. **But the publisher's site terms prohibit reproduction
and transmission without written consent** [REG-R21], so the library must not ship a copy.

`mort_table.csv` is therefore a **[std]** construction: the **canonical `jplib` proxy**,
one file shared by every product in this library rather than a per-product reconstruction,
so that a cell carries the same rate *and* the same provenance wherever it is shipped. Its
anchors are the union of the rates read from the published table across the library's
research passes [REG-R18] — more ages than this product's own pass read [R4] — and every
other age is log-linear in `ln q` between its two neighbouring anchors, at the published
table's own five-decimal granularity, with no extrapolation anywhere. Each row's
`provenance` says which of the two it is. The rows shipped here run from attained age 20 to
attained age 80, the range this product's model points can reach. The
anchoring is what makes the model reproduce the worked example's rates exactly; nothing
about Japanese mortality should be read off the interpolated rows. The shipped rates are
also **table** rates: `mort_be_factor` is applied in `Projection` to reach a best-estimate
basis, because 標準生命表2018 is a **valuation** table carrying a risk-theory margin sized
near 2σ and capped at 130% of the unadjusted rate [REG-R20].

## Modules that are off in the base run

Eight of the notes' optional constructions are implemented and switched off, so the base
run reproduces the worked example while the machinery stays visible and testable. Three
are model point columns and five are References on `Projection`.

| Module | Switch | Off value | On where | What it does |
|---|---|---|---|---|
| リビング・ニーズ特約 | `living_needs` | `0` | points 6, 9 | Accelerates the death benefit at `A − A i_ln / 2 −` six months' premiums on `A` [S1] [S7] [S8] [S12], as a share of the existing decrement. Barred within a year of a non-renewable expiry [S1] [S7] — on this grid the last twelve months, `t ≥ proj_len() - 12`, which is the clause itself rather than the annual grid's one-row approximation of it |
| 保険料の払込の免除 | `wop` | `0` | point 7 | A two-state chain on the premium-paying population, on an accident producing a 別表4 state within 180 days [S1] [S8] [S12] [S14] — a much lower bar than the 別表3 test for 高度障害, so it does **not** reuse `mort_rate()` |
| 復活 | `reinstatement` | `0` | point 8 | The lapsed-but-reinstatable pool and its three-year window [S1], tracked **by vintage** — 36 monthly vintages, where the annual grid had three: the window runs from each life's own 失効, and one blanket balance drops a cohort early or late |
| Contract boundary | `contract_boundary` | `ceiling` | point 5 | `current_term` truncates at the end of the 保険期間 in force at the valuation date. The two answers have opposite signs, **+¥47,254.64** against **−¥16,071.24**, and the ESR treatment settling it is [unverified] here [REG-R16] |
| Selective lapsation | `sel_lapse_lambda` | `0.0` | — | `q_eff = q (1 + λ max(0, 1 − l(t)/l_ref))`, with `sel_lapse_ref = 1.0` **[std]** so the reference block is the cohort at issue. One-directional: renewal takes no 告知 [S1] [S4] [S8] [S12], so an uninsurable life renews while a healthy one re-shops, four times over on the anchor cell |
| Renewal-decline elasticity | `decline_beta` | `0.0` | — | `d = min(d_max, d_0 (P_a(k+1)/P_a(k))^β)`, the flat 15% at zero. The jump it responds to accelerates: ×1.87, ×2.16, ×2.28, ×2.66, so `decline_max = 0.50` **[std]** binds at β = 2 on every boundary and at β = 1 on none |
| Age-basis shift | `mort_age_shift` | `False` | — | `q_x → sqrt(q_x q_(x+1))`. 契約年齢 is age last birthday (*man-nenrei*, 満年齢) [S1] and the table is built for age nearest birthday (*hoken-nenrei*, 保険年齢) [REG-R20], so the base run reads half a year early and understates. The shift moves `q` **up** — 0.73% at age 30, 4.15% at 40 — and one moving it down has the sign wrong |
| Commission at 更新 | `comm_new_term_rate` | `0.0` | — | Pays acquisition commission in the first **month** of each renewed term. A 更新 is not new business [S1] [S4], but no document discloses a commission scale at all, so the zero is a choice — and a first-year scale would flip the **sign** at `t = 120, 240, 360` and `480` |

Two scope limits are stated rather than approximated. The 復活 arrears at 年6% compound
[S1] are **not** monetized: they settle premiums for years in which this projection
collected none, and recognizing them needs a missed-premium ledger the notes do not
specify **[std scope]**. And a *partial* acceleration leaves a reduced contract in force at
a reduced premium [S1] [S7] — a second transition, not one benefit with two amounts — so
`ln_amount()` **raises** rather than approximating it. It cannot arise here anyway: the
¥30,000,000 cap is per **insured**, aggregated across that insurer's contracts
[S1] [S7] [S8] [S12], so at the composite's ceiling it is *exactly reached* and reduces
nothing. `ln_cap_binds()` tests that with a **strict** inequality and is `False` on model
point 9, which sits on the boundary.

## Sign convention

The notes' `CF(t)` is already **income positive** — they write `+ = inflow` — which is the
library-wide sign of `net_cf`, so there is no outgo-positive `liability_cf` companion to
publish: one stream, one sign, one name. Lapse and the renewal decline contribute no term
to `net_cf` at all; they act only through `pols_if`.

Premiums fall at the start of the month they are due in and claims at the end of the month
they arise in. There is no half-year correction to make and none to double-count: the
annual model needed one because it collected a whole year's premium from lives that could
exit in month two and booked their claims twelve months late, and this one does neither.

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S` wherever it has an analogue —
`pols_*` for counts, plural nouns for cash flows, `*_rate` for rates, `*_pp` for
per-policy amounts, `claims(t, kind)`, `pols_if_at(t, timing)`. The full map is in the
`Projection` docstring. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `q(t)` and `qbar(x, m)` | `mort_rate` / `mort_table_mean` | Different bases, not one quantity at two arguments: the decrement is best-estimate, the premium scale's shape parameter is the unadjusted table rate |
| (margin removal) | `mort_be_factor` | The multiplier turning the shipped **valuation** table into the projection's best-estimate basis carries one name across all nine models. Not `mort_ae_factor`: an actual-to-expected ratio is a different quantity, measured rather than assumed |
| roll-forward identity | `check_pols_roll_fwd()` / `check_pols_roll_fwd_resid(t)` | The per-period in-force roll-forward check has one name in every model of this library and both sister libraries, so one test calls it across all of them |
| `P_m(k)`, `P_a(k)` | `premium_mth_pp(t)`, `prem_pp(t)` | Indexed by the *term* in the notes and by the policy month here, so every cash flow line is indexed alike; `term_index(t)` resolves it and `check_prem_level()` asserts the premium is still level within each 保険期間. `prem_due_pp(t)` is the third of the family and the only one that is a cash flow: what the payment mode makes fall in month `t` |
| `d(t)` | `decline_rate` | Deliberately not any variant of *lapse*. Different month, different population, different size, and not even the same kind of quantity — a one-off proportion rather than a rate per unit time — so it is the one decrement here with no `*_mth` companion |
| `lap(t)` | `pols_lapse_pool` | A **stock** — the lapsed lives still inside the three-year window — where `pols_lapse` is the month's **flow** into it |

There is deliberately no `cv_pp` and no account value. The absence is a product fact, and
it is why this chassis carries a plain lapse model while the
[whole life technical notes (終身保険)](../whole_life/technical-notes.md)
carries 自動振替貸付.

## Standardizations used

`mort_be_factor = 0.80` (the largest single lever and the least evidenced number); the
lapse curve 9 / 7 / 6 / 5.5 / 5 percent; `decline_base = 0.15` with `decline_beta = 0` and
the elasticity cap `decline_max = 0.50`; `sel_lapse_ref = 1.0`, the cohort at issue;
`expense_acq = 15,000`,
`expense_maint = 4,000` inflating at `inflation_rate = 0.01`, `expense_claim = 30,000`;
`comm_init_rate = 0.50` and `comm_renewal_rate = 0.05`; the premium extension above the
published age-50 cell and the annualization `P_a = 12 P_m`; `ln_interest_rate = 0.02` and
`ln_take_up = 0.10`; `wop_inc_rate = 0.0008` with `wop_rec_rate = 0`;
`reinstate_rate = 0.10` over a `reinstate_window` of 3 years, the window itself being
sourced [S1]; the log-linear interpolation
of the mortality table; and death-before-lapse-before-decline as the processing order.
Each rationale is in `technical-notes.md` and in the cells docstring that uses it.

**Four of them are arbitrary placeholders, and are labelled as such rather than dressed
up as estimates**: `ln_take_up = 0.10`, `ln_interest_rate = 0.02`, `wop_inc_rate = 0.0008`
and `reinstate_rate = 0.10`. No retrieved document gives an acceleration take-up, a rider
discount rate, a 別表4 accident-disability incidence or a reinstatement rate; no observed
range can be quoted for any of the four; and nothing in the sources bounds them. Three are
deliberately round so that no reader mistakes them for measurements, and the fourth
(`wop_inc_rate`) is explicitly *not* scaled off `mort_rate()`, because 別表4 is a much
lower bar than the 別表3 test the table's 高度障害 loading covers and a derivation off `q`
would be false precision.

The only defence any of the four has is the switch: **the module each one drives is off in
the base run**, so the worked example and every figure this model publishes are independent
of all four. Each is live on exactly one model point — 6 and 9 for `ln_take_up` and
`ln_interest_rate`, 7 for `wop_inc_rate`, 8 for `reinstate_rate` — and what those points
demonstrate is the *mechanics* of the module, never the level. Two of the four have a
bounded and stateable effect even so: `ln_interest_rate` enters halved, so it moves the
accelerated payment by 0.5% per percentage point, and `reinstate_window = 3` beside
`reinstate_rate` is **sourced** [S1] where the rate is not. Replace all four before reading
anything off model points 6 to 9.

## Tests

`tests/test_term_life_jp.py` asserts the notes' worked example **hard-coded**, so a
reviewer can check it by eye: the `t = 0, 1, 2, 11, 12, 119` and `120` rows to the yen,
`l(t)` to six decimals, the renewal ladder ¥974 → ¥1,823 → ¥3,933 → ¥8,976 → ¥23,881 with
`l(120) = 0.466683` through `l(600) = 0.026042`, the `t = 119` exit split
0.00003972 / 0.00235186 / 0.08235591, and 600-month undiscounted totals of ¥457,507.04 of
premium, ¥302,433.43 of claims and **+¥47,254.64** of net cash flow against **−¥16,071.24**
over the first 120 months — plus the decline sensitivity at all three of the notes' points
(+¥86,882.78 / +¥47,254.64 / +¥20,786.34). It also pins the frame itself: the
`result_cf()` index is `range(proj_len())`, so it starts at 0 and ends at
`proj_len() - 1`.

Two tests are about the **conversion** rather than about the product. One asserts that
`pols_if(12 j)` reproduces the annual-step model's survivorship at every anniversary, which
is what makes the two runs comparable; the other that twelve monthly decrements compound
back to the annual rate exactly, `(1 - q_m)^12 = q` and `(1 - w_m)^12 = w`, so a reader can
see that the grid changed and the basis did not.

Each of the notes' twelve pitfalls earns a test named after it — that 高度障害 is not a
second decrement, that 更新 reprices without re-issuing, that truncation shortens the term
and not the horizon, that a failed first renewed premium is an expiry rather than a
mid-term lapse, that the living-needs cap is *exactly reached* and does not bind, and the
rest. The eight optional modules are asserted in **both** positions.

Five `check_*` cells assert the identities continuously, each with a per-`t` signed
residual at `check_*_resid(t)`: `check_pols_roll_fwd` (the roll-forward, with the 復活 inflow as
its own term), `check_lapse_pool` (the pool's one inflow and two outflows),
`check_pols_payer` (payers and waived lives partition the in-force), `check_prem_level`
and `check_net_cf` (the statement's columns add up to its own total). All five return
`True` on all nine model points. Four of them close to `roll_fwd_tol = 1e-12`, an identity
between cells evaluated in one expression; `check_net_cf` closes to a separate named
`cash_tol = 1e-8`, because it re-reads yen amounts of order 1e5 back out of the
`result_cf()` `DataFrame` and the round trip leaves float64 rounding the tighter tolerance
would reject. `cash_tol` is still far below one yen, the smallest error a reader adding up
the printed statement could see. `tests/test_model_conventions_jp.py` adds the house
style, parametrized over the registry rather than restated here.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #jplib-term_life-r3
[R4]: #jplib-term_life-r4
[REG-R16]: #jplib-reg-r16
[REG-R18]: #jplib-reg-r18
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R31]: #jplib-reg-r31
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
