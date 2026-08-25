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
model = mx.read_model("products/term_life/Term_JP_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy year `t`, one column per cash flow
line; `result_pols()` prints the counts, decrement rates, term index and premium beside
them, which is where a renewal boundary becomes legible — the row whose `decline_rate` is
non-zero and whose `prem_pp` changes on the next row. `model.Projection.doc` carries the
notes' symbols mapped to the cells names.

## The horizon is the renewal ceiling, not the term

This is the structural difference from the UK and U.S. term models in this repository, not
a parameter difference. A fixed-year (*nen manryō*, 年満了) 更新型 contract **renews
automatically** at the end of every policy term (*hoken kikan*, 保険期間) unless the
policyholder gives notice, with no 告知 and no fresh underwriting, and the premium is
recomputed on attained age at the scale then in force [S1] [S4] [S8] [S12]. So
`proj_len()` is `renew_ceiling() - age_at_entry()`, not `policy_term()`: a ten-year term
issued at age 30 is projected for **fifty** years across five separately priced terms.

Three cells carry it. `term_index(t)` is the notes' `k`, the state variable a Japanese
term model needs and a UK one does not, because the premium is a function of the term
rather than of the policy year; `term_start_age(k)` is the attained age the term is priced
at; and `term_len(k)` is `min(n, w_r - x_k)`, where truncation at the ceiling lives. A
renewal that would carry the policy past attained age 80 renews as an 80歳満了 term
instead [S1] [S2] [S8], so an issue age of 35 has a final term of five years, priced over
its own five, and the projection still ends exactly at 80 — model point 4. Truncation
shortens the **term**, not the horizon; three other market rules exist [S4] [S7] [S12] and
importing one would change it.

A 歳満了 contract never renews [S1]: `term_index` is 1 and `decline_rate` zero in every
year, and `proj_len()` is the term. Model points 3, 6 and 9 are 歳満了.

Nothing else resets at a boundary. `pols_if` is continuous across it; no acquisition
expense and, in the base run, no commission is paid; and the suicide and contestability
clocks run from the original risk commencement date (*sekinin kaishi bi*, 責任開始日) and
do **not** restart [S1] [S4] [S7] [S8] — only reinstatement (*fukkatsu*, 復活) restarts
them [S1]. Neither clock is monetized, so neither is a cells, but treating a renewed term
as a fresh policy gets persistency, the strain pattern and both clocks wrong at once.

## Renewal decline is its own decrement

`decline_rate(t)` is non-zero **only** in a boundary year, and the lives it removes are
taken **after** mortality and **after** ordinary lapse — the notes' steps 3, 4 and 5,
exposed as `pols_if_at(t, "BEF_LAPSE")` and `pols_if_at(t, "BEF_DECLINE")`. Where it
applies it is the larger exit: in year 10 of the anchor cell it removes 0.08235591 of the
0.11175249 lives that leave, 74% of all exits. Folding it into `lapse_rate` makes the
boundary invisible and mis-times most of the cohort's departure, so it has its own rate,
its own count (`pols_decline`) and its own term in the roll-forward check.

Two behaviours roll into the one rate: the policyholder who gives notice, and the one
whose **first renewed premium goes unpaid through grace**, where the renewal is treated as
never having happened and the contract terminates at the original expiry [S1] [S7]. Only
the first is a decision. Both leave at the boundary, and neither may appear in force in
year `t + 1` collecting the renewed premium — which is what the processing order enforces.

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

with `f = 248` per month and `P_m` rounded half up to the yen before annualization, as
rate cards are quoted [S2] [S9] [S10]. Four cells are sourced — male ages 30, 40 and 50
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
| `lapse_table.csv` | Annual lapse by policy year, 9 / 7 / 6 / 5.5 / 5 percent, last row carried forward | **[std]** shape; level reconciled to [REG-R31] |
| `prem_rate_table.csv` | Marginal monthly rate per ¥5,000,000 and the ¥248 flat element, four cells, `is_anchor` marking one row per sex | [S2] rate cards, decomposed row by row in `provenance` |

Every assumption row carries a `provenance` column with its tag and, in the premium table,
the arithmetic of the decomposition. The trade-off: **the model is not portable on its
own.** Copying `Term_JP_A/` without its parent's CSVs gives a model that reads and then
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
| リビング・ニーズ特約 | `living_needs` | `0` | points 6, 9 | Accelerates the death benefit at `A − A i_ln / 2 −` six months' premiums on `A` [S1] [S7] [S8] [S12], as a share of the existing decrement. Barred within a year of a non-renewable expiry [S1] [S7] — the final projected year, and only that one |
| 保険料の払込の免除 | `wop` | `0` | point 7 | A two-state chain on the premium-paying population, on an accident producing a 別表4 state within 180 days [S1] [S8] [S12] [S14] — a much lower bar than the 別表3 test for 高度障害, so it does **not** reuse `mort_rate()` |
| 復活 | `reinstatement` | `0` | point 8 | The lapsed-but-reinstatable pool and its three-year window [S1], tracked **by vintage**: the window runs from each life's own 失効, and one blanket balance drops a cohort a year early or late |
| Contract boundary | `contract_boundary` | `ceiling` | point 5 | `current_term` truncates at the end of the 保険期間 in force at the valuation date. The two answers have opposite signs, **+¥50,400.25** against **−¥15,878.74**, and the ESR treatment settling it is [unverified] here [REG-R16] |
| Selective lapsation | `sel_lapse_lambda` | `0.0` | — | `q_eff = q (1 + λ max(0, 1 − l(t)/l_ref))`, with `sel_lapse_ref = 1.0` **[std]** so the reference block is the cohort at issue. One-directional: renewal takes no 告知 [S1] [S4] [S8] [S12], so an uninsurable life renews while a healthy one re-shops, four times over on the anchor cell |
| Renewal-decline elasticity | `decline_beta` | `0.0` | — | `d = min(d_max, d_0 (P_a(k+1)/P_a(k))^β)`, the flat 15% at zero. The jump it responds to accelerates: ×1.87, ×2.16, ×2.28, ×2.66, so `decline_max = 0.50` **[std]** binds at β = 2 on every boundary and at β = 1 on none |
| Age-basis shift | `mort_age_shift` | `False` | — | `q_x → sqrt(q_x q_(x+1))`. 契約年齢 is age last birthday (*man-nenrei*, 満年齢) [S1] and the table is built for age nearest birthday (*hoken-nenrei*, 保険年齢) [REG-R20], so the base run reads half a year early and understates. The shift moves `q` **up** — 0.73% at age 30, 4.15% at 40 — and one moving it down has the sign wrong |
| Commission at 更新 | `comm_new_term_rate` | `0.0` | — | Pays acquisition commission in the first year of each renewed term. A 更新 is not new business [S1] [S4], but no document discloses a commission scale at all, so the zero is a choice — and a first-year scale would flip the **sign** of years 11, 21, 31 and 41 |

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

Premiums are annual in advance with no allowance for premiums ceasing at a mid-year exit,
which slightly overstates income; the offsetting understatement is the end-of-year claim
timing. The notes are explicit that the two are a matched pair, so a further half-year
adjustment would double-count the correction.

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
| `P_m(k)`, `P_a(k)` | `premium_mth_pp(t)`, `prem_pp(t)` | Indexed by the *term* in the notes and by the policy year here, so every cash flow line is indexed alike; `term_index(t)` resolves it and `check_prem_level()` asserts the premium is still level within each 保険期間 |
| `d(t)` | `decline_rate` | Deliberately not any variant of *lapse*. Different year, different population, different size — the name is the first line of defence against the two being merged |
| `lap(t)` | `pols_lapse_pool` | A **stock** — the lapsed lives still inside the three-year window — where `pols_lapse` is the year's **flow** into it |

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
reviewer can check it by eye: the year 1, 2, 3, 10 and 11 rows to the yen, `l(t)` to six
decimals, the renewal ladder ¥974 → ¥1,823 → ¥3,933 → ¥8,976 → ¥23,881 with
`l(11) = 0.466683` through `l(51) = 0.026042`, the year-10 exit split
0.00049977 / 0.02889681 / 0.08235591, and fifty-year undiscounted totals of ¥470,348.54 of
premium, ¥309,768.95 of claims and **+¥50,400.25** of net cash flow against **−¥15,878.74**
over the first ten years — plus the decline sensitivity at all three of the notes' points
(+¥92,123.94 / +¥50,400.25 / +¥22,587.91).

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
