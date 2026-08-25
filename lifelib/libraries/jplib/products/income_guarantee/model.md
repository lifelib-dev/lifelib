# Implementation Notes

**Status:** Draft, 2026-08-20. Built from
[`products/income_guarantee/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md). The protection chassis
it states deltas against is 定期保険, specified in
[`products/term_life/product-spec.md`](../term_life/product-spec.md) with its
[technical notes](../term_life/technical-notes.md) and implemented in
[`Term_JP_A`](../term_life/model.md) — this model carries that model's names for every
shared concept, and restates none of its machinery. `S#` and `R#` ids resolve
against [`sources.md`](sources.md), and `[REG-R#]` against
`references/regulatory-and-actuarial-references.md`.

> **This is a mechanics demonstration, not a pricing or reserving result.** What is sourced
> on this product is the *shape*: the instalment count `max(N − m + 1, G)`, the 最低支払保証期間
> (*saitei shiharai hoshō kikan*, minimum payment guarantee period) as an extension of the
> payment period past the expiry date rather than a floor inside it, the absence of any
> survival condition on the instalments, the absence of any surrender value (*kaiyaku-henreikin*,
> 解約返戻金) at any duration, premium cessation on the annuity event, the absence of
> renewal (*kōshin*, 更新), and the anchor cell's ¥2,565 monthly office premium, which is a
> published rate [S6]. Everything else quantitative is **[std]**: the mortality table
> shipped here is a construction and not a copy of the standard mortality table for death
> cover (*seiho hyōjun seimeihyō 2018*, 生保標準生命表2018), and the best-estimate factor, the
> four rate-class factors, the lapse table, every expense and commission level, the
> commutation discount rate and all four optional-module parameters are standardizations
> introduced for the reference implementation. Replace them with company data before
> drawing any conclusion from the output.

`IncomeTerm_JP_S` is the executable counterpart of `technical-notes.md`. It projects gross
best-estimate liability cash flows on a **monthly** grid for a single-policy model point of
survivor income term (*shūnyū hoshō hoken*, 収入保障保険) — a **death** benefit paid as a level
monthly income to a fixed expiry date, floored by the 最低支払保証期間. It is not income
protection: nothing here models a disability decrement, and a reader arriving from
`uklib`'s `IP_UK_S` should expect the family income benefit shape instead.

---

## Run it

From the repository root:

```bash
python products/income_guarantee/run.py        # the anchor cell, point_id = 1
python products/income_guarantee/run.py 6      # another model point
```

`run.py` prints the model point, the first twelve policy months, the last month of cover and
the run-off tail after it, the undiscounted totals, and every `check_*` cells. Its output is
ASCII-only, so it prints on a Windows console under any code page: amounts are written "JPY"
and the product name is romanized. In a session:

```python
import modelx as mx
model = mx.read_model("products/income_guarantee/IncomeTerm_JP_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[1].result_pols()    # the populations and decrement rates beside it
```

`Projection` takes a `point_id` and `Projection[1]` is the worked example's anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy month `t`, one column per cash flow
line, with `pols_if` first and `net_cf` last. The model and its `Projection` Space both
carry docstrings — `model.doc` describes the product and the projection basis, and
`model.Projection.doc` holds the full mapping between the technical notes' symbols and the
cells names.

---

## The projection horizon is longer than the policy term

This is the one structural fact the model exists to get right, and it drives the shape of
almost every cells. Where the insured event falls so late that fewer than `G` months remain,
the annuity payment period is **extended past the expiry date** until the guarantee has run
[S1 第3条第2項] [S3 第3条第3項] [S5] [S12] [S14]. So

    proj_len() = term_m() + guar_m() - 1

On the anchor cell that is 443 months against a 420-month term: a claim in policy month 420
pays its twenty-fourth instalment twenty-three months after cover ended. `pols_if(t)` is
zero for every `t` beyond `term_m()`, and in those months the only surviving lines are the
annuity instalments and their administration expense — `check_expired_cover()` asserts
exactly that, month by month. Terminating at `t = N` drops ¥2,645.21 of contractual claim
outgo on the anchor cell, 0.5967% of the total, and nothing else looks wrong afterwards,
which is what makes it the easiest error to make on this product and the least visible.

The guarantee is a **term extension, not a benefit floor**. Both readings pay the same
`max(N − m + 1, G)` instalments, so an undiscounted total cannot distinguish them; they
differ in *when*. `pay_count(m)` and `pay_end(m)` express the same contractual rule from
opposite ends — how many instalments a claim makes, and the month the last of them falls —
and `check_pay_count()` asserts `pay_count(m) == pay_end(m) − m + 1` for every month of
cover. `pay_end(m) = max(N, m + G − 1)` is the whole guarantee mechanic in one expression:
for `m <= N − G + 1` every stream ends at exactly `N` whenever it opened, because the expiry
date is fixed at issue.

---

## The in-payment ledger

`annuities_if(t)` is the notes' `R(t)`: the number of annuity instalments falling due in
month `t`, per policy issued. It is *not* a population of policies, which is why it is not
spelled `pols_*`, and it must never be summed with `pols_if(t)`. On the anchor cell
`annuities_if(420) = 0.016780` while `pols_if(420) = 0.145023`, and adding them produces a
number with no meaning.

The recursion is

    annuities_if(t) = annuities_if(t-1) - annuities_ended(t) + annuities_open(t)

with new claims entering in the **same** month, because the first instalment falls at the
end of the month of the insured event [S1 第3条第2項] [S5]. **The ledger is never decremented**
— not by the insured's mortality, which is what opened the stream, not by the recipient's,
and not by lapse, since a policy in claim cannot lapse and its premiums have ceased. On the
composite the instalments carry no survival condition [S1] [S5] [S14], confirmed from the
contract side by the one published factor table, which depends on the payment period and
explicitly not on the annuitant's age or sex [S13 別表1]. Applying the surviving-policy
factor `(1 − q_m)(1 − w_m)` to the ledger — the natural thing to do if `R` is mistaken for a
population of policies — cuts annuity outgo on the anchor cell from ¥443,313.69 to
¥245,605.66, an understatement of 44.6%. It is the largest single error available in this
model.

Two identities guard it, both implemented as `check_*` cells with a per-`t` signed residual:

- `check_annuity_ledger()` rebuilds `annuities_if(t)` directly from the claim vector — the
  streams `s` with `s <= t <= pay_end(s)` — with no reference to the recursion.
- `check_annuity_total()` checks the running total `annuities_cum(t)` against an independent
  count of the instalments each claim contributes at or before `t`. At `t = proj_len()`
  this is the notes' identity `sum of R(t) = sum of D(s) × n_pay(s)`: 2.955425 instalments
  against 0.016780 expected claims, an average of 176 instalments a claim, which is the
  number that says this is an income product and not a sum-assured one.

A consequence worth stating separately: the ledger **peaks at exactly month `N`**, where it
equals the sum of every claim the contract has ever made. An implementation that ends
streams one month early gets that identity wrong by one month's claims and nothing else
visibly changes.

---

## Two populations, and which cash flow line carries which

`pols_if(t)` and `annuities_if(t)` are disjoint, and every line of `result_cf()` belongs to
exactly one of them:

| Carried on `pols_if(t)` | Carried on `annuities_if(t)` |
|---|---|
| `premiums`, `expenses`, `commissions`, `claim_expenses` (through `pols_death`) | `claims_annuity`, `annuity_expenses` |

Two things follow that an implementation can easily get wrong. **Premiums stop on the
annuity event; the benefit does not** [S1 第12条第2項] [S3 第5条] [S8] — netting the two against
one combined population would collect ¥7,535.43 of premium on the anchor cell, 1.63% of the
total, from policies in claim and paying nothing. No explicit term is needed for the
cessation, because a policy in claim has already left `pols_if`; what the model must not do
is give the ledger a premium. And **`annuity_expenses` rides the ledger**, at ¥200 per
instalment **[std]**, not the in-force population: it is the one expense that survives the
end of the term, so attaching every expense to `pols_if` charges nothing at all in months
421 to 443, when instalments are still being paid. It has no analogue on the protection
chassis, which pays a lump sum and closes the file.

---

## Premium frequency is a timing feature, not an inert flag

`premium_mode` is implemented rather than carried and ignored: `prem_due_pp(t)` collects
`12 / f` months of premium at the start of each payment period and nothing in between. No
advance payment (*zennō*, 前納) or frequency discount is applied, because the discount is
insurer-set and unpublished **[std scope]** — so a policy year costs the same at all three
frequencies and only the timing moves. The anchor cell is 月払, which is the frequency the
only published rate grid is quoted in [S6], so the worked example is unaffected; model
points 3 (年払) and 6 (半年払) exercise the other two.

---

## The nine model points

| # | Cell | What it exercises |
|---|---|---|
| 1 | M30, 65歳満了, 保証2年, ¥150,000, 非喫煙者優良体, ¥2,565 | **Anchor.** The worked example, all modules off |
| 2 | F30, same otherwise, ¥2,175 | The female mortality construction |
| 3 | M45, 65歳満了, ¥150,000, ¥2,865, 年払 | A 20-year term; the annual frequency |
| 4 | M30, 60歳満了, ¥100,000, ¥1,410 | **一括受取 on**: every claim commuted |
| 5 | F40, 60歳満了, ¥100,000, ¥1,400 | **リビング・ニーズ on**, at a stream the cap does not bind |
| 6 | M35, 65歳満了, **保証5年**, ¥150,000, 喫煙者標準体, 半年払 | The 5年 guarantee, the worst rate class, the semi-annual frequency |
| 7 | M50, 60歳満了, ¥200,000, 非喫煙者標準体 | **保険料払込免除 on** |
| 8 | M70, 75歳満了, **保証5年 on a 5-year term**, ¥50,000, 喫煙者標準体 | **復活 on**, and the edge case `G = N`: every claim pays 60 instalments |
| 9 | F35, 65歳満了, ¥100,000, 喫煙者優良体 | The fourth rate class |

Every point projects without NaN and every `check_*` cells returns `True` on all nine.

---

## Inputs are external files

The model folder holds `__init__.py`, `_system.json` and the two Space folders and nothing
else — no `_data/`, no embedded values. The inputs are plain CSVs in the product directory
beside `run.py`, read at run time by the `Data` Space, which is unparameterized so each file
is read **once per model** however many policies are projected. `Data.input_dir()` resolves
to `_model.path.parent`, so the model works from any checkout location. This follows
`annuallife/TradLife_A`; `basiclife/BasicTerm_S` stores its inputs inside the model instead.
The trade-off is stated rather than hidden: copy the model folder without the CSVs and it
reads, then fails on first evaluation. In exchange a diff shows logic changes only, and an
input can be swapped in place — point `Data.mort_table_file` at another same-schema file and
the projection follows, with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Nine model points indexed by `point_id`, with a `policy_id` column | `point_id = 1` is the worked example's anchor cell; premiums as set out below |
| `mort_table.csv` | 死亡保険用 table rates by sex and attained age 20-89, the range this model can read | The library's one canonical **[std]** construction, anchored on the individual rates read from the IAJ table [R1] [REG-R18]; per-row `provenance` says which rows are anchors and which are interpolated, and is identical to the row every other `jplib` product ships for the same cell |
| `lapse_table.csv` | Annual ordinary lapse rate by policy year, five rows, the last applying to year 5 and beyond | **[std]** chassis table, reconciled to the LIAJ FY2024 個人保険 解約・失効率 of 5.6% [REG-R31]; nothing product-specific exists |
| `rate_class_table.csv` | `class_factor` and `mix_weight` for the four rate classes | **[std]**; no carrier publishes a class differential for this product [S2] [S5] [S6] [S14] [S16] |

**The mortality table is a construction, not a copy.** 生保標準生命表2018（死亡保険用）is published at
a stable public URL and anyone may go and read it [R1] [REG-R18], but its publisher
prohibits reproduction and transmission without written consent [REG-R21]. The library
therefore
*cites* the table, *quotes* the individual rates the worked example needs, and *ships* a
table whose anchor rows carry those quoted rates and whose remaining rows are log-linear
interpolations in `ln q` between the two neighbouring anchors, rounded to five decimals. The
anchor set is the **union** of every anchor any `jplib` product reads — both sexes at ages
20, 22, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80 and 85, plus male 31–34 — so the same
cell carries the same value *and* the same provenance in every product that ships it, and
the file is identical across the library up to the age range each model reads. Female rates
are read at the female anchors in their own right, not built as a ratio to the male rate.
No age is extrapolated: every shipped age lies strictly between two sourced anchors. The
anchors the worked example touches are male `q30 = 0.00068`, `q31 = 0.00069`,
`q32 = 0.00070` and `q45 = 0.00177`; `q44 = 0.00163`, `q63 = 0.00851` and `q64 = 0.00929`
are interpolated. Keep the second distinction separate from the first: even the real table
is a
**valuation** table carrying a ~2σ margin capped at 130% of the unadjusted rate [R2]
[REG-R20], so a best-estimate basis is a **[std]** adjustment of it either way. Here that
adjustment is `mort_be_factor` = 0.80 times the rate-class factor.

**Where the premiums come from.** Five model points carry a *published* monthly rate [S6]:
points 1, 2 and 3 from the 65歳満了 / 保証2年 / 非喫煙優良体型 / 年金月額¥150,000 grid (¥2,565 at M30,
¥2,175 at F30, ¥2,865 at M45), points 4 and 5 from the 60歳満了 / 年金月額¥100,000 grid (¥1,410 at
M30, ¥1,400 at F40). Three are **[std]** scalings of a published cell, and each says which
dimension it scales and which it leaves unpriced:

- point 6, ¥2,565 (the published M35 cell of the 65歳満了 / 保証2年 / 非喫煙優良体型 / ¥150,000 grid)
  × 1.35/0.70 for the rate class, rounded to **¥4,950**. The move from 保証2年 to 保証5年 is
  **not** priced — no carrier publishes a guarantee-length differential;
- point 7, ¥1,330 (the published M45 cell of the 60歳満了 / ¥100,000 grid) × 2 for the
  ¥200,000 monthly amount × 0.90/0.70 for the rate class = **¥3,420**. The move from age 45
  to age 50 is not priced, which that grid makes defensible: it is nearly flat in issue age
  (¥1,410 at 30 against ¥1,330 at 45) because the shortening term offsets rising mortality;
- point 9, ¥2,475 (the published F35 cell of the 65歳満了 / ¥150,000 grid) × 100/150 for the
  ¥100,000 monthly amount = ¥1,650, × 1.05/0.70 for the rate class = **¥2,475**.

Point 8 sits where no published grid reaches, and its ¥7,000 is **[std]**, at roughly the
undiscounted break-even on the model's own basis (−¥19.57 net over its 60-month term).
This file is the only place that distinction is recorded, because a model point table is
not an assumption table and carries no `provenance` column.

**One deliberate departure from the notes' layout.** `technical-notes.md` lists
`class_factor` among the model point attributes; it is held in `rate_class_table.csv`
instead, keyed by `rate_class`. The four factors are one **[std]** structure rather than
four free numbers — a smoker/non-smoker ratio of 1.50, a preferred/standard ratio of 0.778,
levels pinned by the requirement that the mix-weighted mean be 1.000, because 生保標準生命表2018 is
an all-lives basis — and a per-policy copy of a shared assumption is a place for the points
to drift apart. `check_class_factor_norm()` asserts that normalization, which a model point
column could not. The values are identical either way.

---

## Modules that are off in the base run

Five of the notes' optional constructions are implemented and switched off, so that the base
run reproduces the worked example while the machinery stays visible and testable. Four are
model point columns; the fifth is a `Projection` Reference.

| Module | Switch | Off value | What it does when on |
|---|---|---|---|
| Full commutation (一括受取) | model point `commutation` | `False` (point 4 excepted) | Settles the claim at the claim date with `commute_pp(t)`, an annuity-certain on `pay_count(t)` instalments at `commute_rate` = 0.65% p.a. **[std]**, and does **not** open the ledger for that claim — a full commutation extinguishes the contract [S1 第5条第2項] [S3 第6条第3項] [S12] [S14], so paying the lump sum *and* opening the stream doubles the benefit. Partial commutation is out of scope **[std scope]** |
| リビング・ニーズ特約 | model point `living_needs` | `False` (point 5 excepted) | Settles a **[std]** proportion `ln_take_up` of the month's claims as an acceleration at the 年金現価 less six months' interest and premium equivalent, capped at `ln_cap` = ¥30,000,000 and barred in the final year [S2] [S5] [S7]. Carved **out** of the death decrement, not added to it |
| 保険料払込免除 | model point `wop` | `False` (point 7 excepted) | Runs a two-state incidence/recovery chain **[std]** on the premium-paying population, on the 不慮の事故 plus 180 days plus 別表4 test [S1 第6条] [S3 第8条] [S5] [S6]. 別表4 is a materially lower bar than the 別表3 高度障害 schedule, so the incidence deliberately does not reuse `mort_rate`. The waiver is in the main contract (*shu-keiyaku*, 主契約), so it carries no extra premium |
| Reinstatement (復活) | model point `reinstatement` | `False` (point 8 excepted) | Returns a **[std]** proportion `reinst_rate` of each month's lapses to force `reinst_lag_m` months later — a single-lag approximation of the three-year `reinst_window_m` [S1 第17条] [S3] [S5] — paying arrears with interest through `prem_arrears_pp()`. The rate class carries over unchanged [S3], which matters because the class is a mortality parameter |
| Selective lapsation | Reference `sel_lapse_lambda` | `0.0` | Loads persisters' mortality by `1 + λ max(0, 1 − l(t)/l_ref)`. Weaker here than on the protection chassis, which has a periodic no-underwriting renewal to select against, but not absent: the rate class is fixed at issue and cannot be changed, so a life whose health deteriorates keeps a preferred rate while a life whose health improves cannot get one and may re-shop |

The リビング・ニーズ module has one product-specific consequence. Because the payout is the present
value of an income stream rather than a level sum assured, **the cap binds from month 1** on
the anchor cell's parameters, where the full 年金現価 at issue is ¥56,352,381.90, and stops
binding only in month 209. That is the opposite pattern to a level sum assured, where a cap
either always binds or never does. The `<= 6`-month timing shift the acceleration really
produces is ignored on this grid **[std]**.

Two of the notes' constructions are **not** implemented, and are named so the absence is not
read as an oversight. The **recipient-mortality variant**, which one carrier alone writes
[S3 第3条第3項], would need a post-event mortality basis on a life the contract never
underwrote, and the 年金開始後用 table stays on the 2007 vintage [REG-R11]; it is out of scope
**[std]**. And there is **no 更新** on this chassis [S5], so the renewal repricing and decline
decrement of the protection chassis are deliberately absent and the term is 歳満了 only,
derived from `expiry_age` rather than read as a policy term.

---

## Sign convention

The notes' `CF(t)` is already income-positive — they write `+ = inflow` — which is the
library-wide sign of `net_cf`, so there is no outgo-positive `liability_cf` companion to
publish: one stream, one sign, one name.

**`claims_annuity` is a death benefit here, and the column that is absent is a product
fact.** The instalments are paid on the death of the insured, or on the contractual 高度障害
state carried inside the same decrement as its accelerated equivalent — not on survival and
not on disability as such. The name records the benefit's *form*, and the same name carries a
*living* benefit in `LTC_JP_S` ([nursing care model notes (介護保険)](../nursing_care/model.md)) and
`Annuity_JP_A` ([individual annuity model notes (個人年金保険)](../individual_annuity/model.md)), so this model states
the contingency in the `claims` docstring and in the `result_cf` docstring rather than leaving
it to the column name. **There is no `claims_death` column**: the contract pays no lump sum on
death at any duration — a claim *opens* an annuity stream instead of settling one — so the
whole death benefit is `claims_annuity`, and a zero-valued `claims_death` would misdescribe
the contract rather than document it. Nor is there a bare `claims` column beside the four
`claims_*` splits: a statement that prints its own subtotal next to its parts stops adding to
`net_cf` unless the reader knows which column to skip. `check_net_cf()` re-adds the published
columns to `net_cf(t)` in every one of the 443 months and is the assertion that keeps both
properties true.

`claims_lapse` is identically zero because the
composite is 無解約返戻金型 with no 解約返戻金 at any duration [S2] [S5] [S6] [S7] [S9] [S15]. The zero
column is published rather than dropped, because a non-zero lapse row imported from a
cash-value chassis is one of the notes' listed pitfalls and a missing column would only hide
the product fact. For the same reason there is no `cv_pp` and no automatic premium loan
(*jidō furikae kashitsuke*, 自動振替貸付) anywhere in the model: with no cash value there is no
collateral to lend against, and one carrier states the absence in terms [S2].

One presentational note. The notes' worked-example *table* puts `E0 + c0` in a "Maint. +
acq." column and reserves "Comm." for the renewal commission; the model follows the notes'
own Notation table, where `E0` is `expense_acq` and both `c0` and `c_r` are `commissions`.
Only the column allocation differs — the notes' totals table separates "Commission (renewal)
¥21,577.36" from "Acquisition (`E0 + c0`) ¥30,390.00" and the model reproduces both to the
yen — and the test module maps between the two explicitly.

---

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue:
`pols_*` for policy counts, plural nouns for cash flows, `*_rate` for rates, `*_mth` for the
monthly form of an annual rate, `*_pp` for per-policy amounts, `claims(t, kind)` with an
uppercase `kind` string, `pols_if_at(t, timing)` for the within-month in-force reads. The
notes use compact actuarial symbols; the full mapping lives in the `Projection` docstring.

Five names are fixed library-wide rather than chosen here, and this product carries the
settled spelling of each:

| Library-wide name | What it means | Why not the alternative |
|---|---|---|
| `premium_mth_pp` | The level **monthly** office premium per policy | `premium_pp` is the *annual* per-policy premium everywhere in the library, so a monthly amount under that name would read as twelve times itself |
| `prem_mode_months` | The number of months in one premium payment period: 1, 6 or 12 | `prem_period` means a duration in the model's own grid unit, and a categorical premium-paying-period cells is `prem_period_type` — this is neither |
| `mort_rate_base` | The table rate in period `t`, before the **[std]** adjustments | `mort_rate_at_age(...)` is the lookup keyed by **age**; this one is indexed by projection month, so it is the base rate in `t`, not a table lookup |
| `check_pols_roll_fwd` | The per-period in-force roll-forward check, with `check_pols_roll_fwd_resid(t)` beside it | The settled name in both sister libraries, so one test can call the same check across every model |
| `check_net_cf` | The check that the published `result_cf()` columns add to `net_cf(t)`, with `check_net_cf_resid(t)` beside it | The settled `jplib` spelling; `check_cf_ledger` was retired because "ledger" already names this product's in-payment ledger, which is a different object |

Five further cases needed care in this product:

| Notes | Cells | Why |
|---|---|---|
| `R(t)` | `annuities_if` | A count of instalments falling due, not a population of policies, so deliberately not spelled `pols_*`. It and `pols_if` are disjoint and must never be summed |
| `q(t)`, `w(t)` | `mort_rate` / `mort_rate_mth`, `lapse_rate` / `lapse_rate_mth` | The unsuffixed name is the **annual** rate, library-wide. A monthly-grid model using `lapse_rate` for the monthly rate while spelling mortality `mort_rate_mth` would carry two conventions at once |
| `n_pay(m)`, `ends_at(m)` | `pay_count`, `pay_end` | The same contractual rule from opposite ends. Keeping both, rather than deriving one silently, is what lets `check_pay_count()` assert them against each other |
| *(no symbol)* | `pols_maturity` | The survivors of the last month of cover, who neither die nor lapse — their cover runs out. Bookkeeping, not a benefit: nothing is payable on survival. Without it the roll-forward appears to lose lives with no cause |
| `ea R(t)` | `annuity_expenses` | Out of `expenses` because it rides the ledger, and separate from `claim_expenses`, which is charged once per claim rather than once per instalment |

---

## Standardizations used

Every one of these carries its rationale in the cells docstring that uses it:
`mort_be_factor` = 0.80 (the chassis best-estimate factor) and the whole shipped mortality
table; the four `class_factor` values and their illustrative mix; the lapse table;
`expense_acq` ¥15,000, `expense_maint` ¥4,000 p.a., `expense_claim` ¥30,000,
`expense_annuity` ¥200 per instalment and `inflation_rate` 1.0%; `comm_init_rate` 50% and
`comm_renewal_rate` 5%; `commute_rate` 0.65% p.a. effective; death-before-lapse as the
processing order; and the incidence, take-up, lag and interest parameters of the optional
modules — `ln_take_up`, `wop_inc_rate`, `wop_rec_rate`, `reinst_rate`, `reinst_lag_m`,
`reinst_int_rate` and `sel_lapse_ref` — none of which any retrieved document quantifies.
Those seven carry their numeric values and their rationale in the *Optional modules* table
of [`technical-notes.md`](technical-notes.md), which is where a reader who wants to replace
one should look; the model's References hold the same numbers and nothing else.

Two deserve their range stated. `commute_rate` is the **best**-evidenced [std] number here:
one 特約条項 publishes a factor table with no dependence on the annuitant's age or sex [S13
別表1], fitting an annual annuity-due less a small constant at about 0.61% p.a., and three
carriers publish a worked commutation amount whose ratios cluster at 0.92190, 0.92183 and
0.92133 [S6] [S10] [S17], the last two implying 0.66%. The midpoint of those two anchors is
0.635%, and 0.65% is that rounded to the nearest 0.05%; the range to test over is
0.61%-1.45%.
`class_factor` is the **worst**-evidenced and the largest lever in the file: annuity outgo
on the anchor cell runs ¥443,313.69 at 0.70 and ¥846,803.38 at 1.35, a factor of 1.9 across
the composite's own four classes, on a premium quoted for the cheapest of them. It
multiplies with `mort_be_factor`, whose own range runs ¥426,306.73 to ¥552,708.11.

`expenses(t)` is **acquisition plus maintenance only**. The claim expense is its own cells,
`claim_expenses(t)`, deducted explicitly in `net_cf(t)` and published as its own
`claim_expenses` column; the annuity administration expense is a third, `annuity_expenses(t)`,
because it rides the ledger rather than the in-force population. The notes' worked-example
table prints the last two combined in a single "Claim + ann. exp" column — that is a
presentational grouping in the notes, and the model publishes the three separately.

The 年金現価 cap of ¥300,000,000 [S8] is a contractual ceiling on the present value of the
instalments. It is **not implemented**, and it binds on none of the nine shipped points —
the largest present value in the set is the anchor cell's ¥56,352,381.90, under a fifth
of it.

Discounting is out of scope for the library, so the notes' four present-value diagnostics
are not cells either. They were reproduced against this model, and reproducing them takes
the notes' own **split timing**: the start-of-month leg — premiums, maintenance, renewal
commission — discounted at `(t − 1) / 12`, and the end-of-month leg — the instalments, the
claim expense and the annuity administration expense — at `t / 12`. That gives −¥73,865.82
at 0.5%, −¥49,216.50 at 1% and −¥10,895.85 at 2%, which is the notes' table to the yen. A
reader who instead discounts the whole of `net_cf(t)` at `t / 12` gets −¥73,998.78,
−¥49,465.63 and −¥11,336.00. The gap is small and is entirely a timing artefact, but on a
product whose claim leg discounts far harder than its premium leg it is worth knowing which
convention produced a printed number.

---

## Tests

`tests/test_model_conventions_jp.py` asserts the house style over every registered model —
the folder layout, the `Data`/`Projection` split, the read-once property, the docstring
contract, the `lower_snake_case` naming, the retired-name register, the `check_*` protocol,
the `result_cf` column conventions, that every model point projects without NaN, and that
`read → write → re-read` reproduces the same file set and the same numbers.

`tests/test_income_guarantee_jp.py` asserts this product's own facts. The notes' seven-row
worked example is hard-coded as a module-level table, to the precision the notes display —
money to the second decimal, in-force to six, the claim and ledger populations to nine and
the decrement rates to twelve, because `q_m` at attained age 30 is about 3.17e-05 and six
decimals would leave it with two significant figures — 0.000032 against 0.000031738873, a
0.8% distortion carried into every claim of the first policy year. Beside it sit the
decrement vector at the three months where something moves, the month-1 and month-13 traces
line by line, the four sourced anchors and the three interpolated table rates the notes
quote, the totals table, the structural
quantities behind it, and the four present-value diagnostics with the split timing that
reproduces them.

Then one test named for each of the **thirteen** entries in the notes' *Known modeling
pitfalls* list. Three of them build the wrong answer explicitly, so that the test fails
loudly rather than merely differing: the decremented ledger at ¥245,605.66, the ¥7,535.43 a
netted population would collect, and the ¥2,645.21 tail a truncated horizon would drop.
Then the seven `check_*` cells and the in-force roll-forward on all nine model points; each of
the five optional modules in both positions, the switched-on ones on the model point that
carries them; and the structural facts — the annuity-certain benefit, the `G = N` edge cell,
premium frequency as a timing feature, the lapse sensitivity whose sign is the opposite of
the chassis's, the mortality lever's range, and the model point envelope enforced by name.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-income_guarantee-r1
[R2]: #jplib-income_guarantee-r2
[REG-R11]: #jplib-reg-r11
[REG-R18]: #jplib-reg-r18
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R31]: #jplib-reg-r31
[std]: #jplib-std
<!-- END generated citation links -->
