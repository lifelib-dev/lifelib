# Implementation Notes

**Status:** Draft, 2026-08-20. Built from
[`products/fx_whole_life/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md). Both state **deltas**
against the savings chassis, 終身保険: its
[product specification](../whole_life/product-spec.md) and its
[technical notes](../whole_life/technical-notes.md) carry the inherited mechanics, and its
model is [`WholeLife_JP_A`](../whole_life/model.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the surrender-value formula and the base the
> surrender charge (*kaiyaku kōjo*, 解約控除) is applied to, the symmetry of the
> market value adjustment, MVA (*shijō kakaku chōsei*, 市場価格調整), the 増加死亡保険金額
> (*zōka shibō hokenkin-gaku*, death-benefit uplift) defined against a 予定利率
> (*yotei riritsu*, assumed interest rate) basis, the
> reduced surrender-value ratio (*tei-kaiyaku-henreikin wariai*, 低解約返戻金割合) ramp, the
> ±50銭 conversion spread and the one-year dead zone on the target test. The charge stack
> is not: every carrier in the source set refuses to quantify its
> mortality-and-expense charge in identical words [S2] [S7], so the three charge rates
> are **back-solved** from one carrier's published guaranteed surrender-value run [S2]
> and carry the whole surrender-benefit stream. The mortality table is a **[std]**
> construction anchored to individual published rates, not a copy of a table whose
> publisher restricts redistribution [REG-R21]. Replace all of it with company data
> before drawing any conclusion from the numbers.

## Run it

```bash
python products/fx_whole_life/run.py            # the anchor cell
python products/fx_whole_life/run.py 3          # the single-premium MVA cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/fx_whole_life/FXWholeLife_JP_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy month `t` with one column per cash
flow line. `result_pols()` gives the decrement columns and `result_av()` the per-policy
account-value and surrender layers.

The model and its `Projection` Space both carry docstrings — `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names.

## The policy currency is the model currency

Every state variable, every assumption and every cash-flow column is in **US dollars**.
Yen enters only through `fx_rate(t)` and `fx_spread()`, and the exchange rate is a model
point column — an exchange rate buried in a recursion is an economic assumption
disguised as a product feature, and cannot be varied by the point that owns it.

The yen ledger is **three translations, not one**: premiums cross at `e + s` under the
yen-payment-in rider (*en nyūkin tokuyaku*, 円入金特約), benefits at `e − s` under the
yen-payment-out rider (*en shiharai tokuyaku*, 円支払特約), and expenses and commission
at the plain `e`, because they are the insurer's own costs and never cross the
policyholder boundary. So

    net_cf_jpy(t) != net_cf(t) x fx_rate(t)

identically. The gap is the insurer's currency conversion fee (*kawase tesūryō*, 為替手数料)
spread income, and the model publishes it as its own column `fx_spread_jpy` rather than
letting it hide inside a translated net figure: ¥125.17 in month 0 on the anchor cell and
¥39,146 over the whole run.
`check_fx_ledger()` asserts `net_cf_jpy = net_cf x fx_rate + fx_spread_jpy` in every
month, on every model point.

Model point 8 settles in US dollars throughout — both yen riders off — and its
`fx_spread_jpy` column is zero while `net_cf_jpy` reduces to a single-rate translation.
That is the parameter position the difference is measured against.

## Two shapes on one chassis

`shape` is a model point column and it changes more than rates. The state variable both
shapes share is the account value (*tsumitatekin*, 積立金), credited at the declared
crediting rate (*tsumitate riritsu*, 積立利率) and floored at the contract's own assumed
interest rate (*yotei riritsu*, 予定利率); the payable value is the surrender value
(*kaiyaku-henreikin*, 解約返戻金).

| | `LEVEL` | `SINGLE` |
|---|---|---|
| Premium | level, guaranteed, monthly | one 一時払保険料 at 契約日 |
| 積立利率 | redeclared monthly, floored at the contract's own 予定利率 | fixed for a 15-year 積立利率適用期間 |
| Death benefit | `SA + IDB(t)` | `max(AV(t), CV(t))` — no sum assured above the fund |
| 市場価格調整 | none | on surrender inside the rate period |
| In-force charges | 維持費 and 保障部分 deducted from the 積立金 | none — they sit inside the declared rate [S10] |
| 自動振替貸付 | present | **structurally absent** — there is no premium to advance |
| Target rider | not offered | optional |

The automatic premium loan (*jidō furikae kashitsuke*, 自動振替貸付) row and the target-rider
row are the point. The two shapes have different **decrement sets**, not merely different
rates, and the model rejects a SINGLE point carrying `apl_on` or a LEVEL point carrying
`target_on` or `dyn_lapse` by name rather than silently pricing a contract that does not
exist.

The "no in-force charge on SINGLE" row is not an assumption but a fit: reproducing that
shape's published `CV(36)` run requires the fund to grow at the declared 積立利率 exactly,
which pins `maint_rate` and `coi_charged` to zero for it. Both live in
`charge_table.csv` with that reasoning in their `provenance` column.

## Inputs are external files

Five CSVs in `products/fx_whole_life/`, beside `run.py`, read at run time. The model
folder holds `__init__.py` and `_system.json` per Space and nothing else — no `_data/`,
no IOSpec, no embedded values — so a diff of the model shows logic changes only. This is
the `annuallife/TradLife_A` layout, not `basiclife/BasicTerm_S`'s embedded inputs. The
trade-off is real and worth stating: **the model is not portable on its own.** Copying
the `FXWholeLife_JP_S` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | 8 model points, indexed by `point_id` | point 1 is the notes' anchor cell, premium sourced [S2]; the rest **[std]** |
| `mort_table.csv` | annual `q` by sex and attained age, 18 to ω | the library's canonical **[std]** proxy, anchored row by row to published rates [REG-R18]; see below |
| `lapse_table.csv` | annual surrender rate by shape and policy year | SINGLE calibrated to a published four-year exit statistic [R5]; LEVEL **[std]** with no public anchor |
| `charge_table.csv` | the shape's charge, surrender-charge, 低解約返戻金, MVA and 特別積立金 parameters | charge stack back-solved [S2]; 解約控除 and 低解約返戻金 scales sourced [S3] [S2]; MVA constants fitted to the published table [S3] |
| `fx_path_table.csv` | an optional TTM path by policy year | month 1 is the published reference level [S11]; the rest **[std]** illustrative, read only where a point sets `fx_path` |

Every row of every assumption table carries a `provenance` column saying whether the
value is sourced or **[std]**, and which. It is the only place in the library outside
`sources.md` and `_research/` where a source may be named at all, and it is not
rendered.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every policy. They live in the unparameterized `Data` Space instead, where they are
evaluated once per model however many policies are projected, and `Projection` reaches
them through its `data` Reference. `Data.input_dir()` resolves to `_model.path.parent`
at run time, so the model works from any checkout location.

### The mortality table is a construction, not a copy

生保標準生命表2018（死亡保険用）is published free at a stable public URL by 日本アクチュアリー会 and
anyone can go and read a rate in it — the sharpest contrast in this library with
`uklib`, whose current CMI tables cannot be read at all without a subscription. But the
publisher's site terms prohibit reproduction and transmission to third parties
[REG-R21], so `jplib` must not ship a copy.

What it ships instead is the library's **one canonical [std] proxy**, built once for all
nine products and restricted here to the attained ages this product's model points can
reach. Every rate the nine products quote from the published table is an **anchor row**,
read from the IAJ table and carried under attribution — for the male life
`q30 = 0.00068`, `q35 = 0.00077`, `q40 = 0.00118`, `q45 = 0.00177`, `q50 = 0.00285`,
`q55 = 0.00422`, `q60 = 0.00653`, `q65 = 0.01015`, `q90 = 0.15760` and the terminal
`q109 = 1.00000`, for the female life `q30 = 0.00037`, `q60 = 0.00363` and the terminal
`q113 = 1.00000` among them [REG-R18] — and every other age is **interpolated**,
log-linear in `ln q` between its two neighbouring anchors and rounded to the published
table's own five decimal places. There is no extrapolation anywhere: both sexes run from
an age-0 anchor to a terminal anchor. Each row's `provenance` column says which of the
two it is, so the same attained age carries the same rate *and* the same provenance in
every product in the library. It is **not** the published table and no conclusion about
Japanese insured-lives mortality should be drawn from it.

`omega_age()` is read **off the table** — the first age at which `q = 1` — rather than
hard-coded, so replacing the table moves the projection horizon with it. One consequence
is visible in `run.py`'s last rows: `q = 1` at the terminal age is an *annual* rate, so
`q_m = 1` and the whole terminal policy year is spent in its first month. The remaining
eleven rows are structurally empty and are carried rather than trimmed, because the
horizon is stated as `12 (ω − x + 1)` months; the zeros are an emptied cohort, not lost
lives, and the roll-forward closes a year earlier. The table starts
at attained age 18, which is **narrower than the 契約年齢 envelope** the representative
product allows: a model point issued younger raises on the lookup rather than being
priced off a rate nobody published. That is a scope limit of the shipped file, not of the
model, and it is asserted as one in the test module.

The table is also a *valuation* table carrying an explicit margin sized to about 2σ
[REG-R20], not best-estimate experience. The adjustment for that is `mort_be_factor`,
carried on the model point in a column named `mort_adj`, and it moves the
**decrement only**: `coi_rate(t)` reads the same table
unadjusted, because the cost-of-insurance basis is a pricing element the insurer sets in
its 算出方法書 [REG-R2]. Wiring one lever to both would make the model absorb its own
mortality sensitivity inside the account value. Model point 7 runs
`mort_be_factor = 1.20` and the two rates part company there.

## The charge stack is a fit, and the fit is the evidence

`prem_charge_early` (38% of each premium over policy months 0–23), `prem_charge_late`
(13% thereafter) and `maint_rate` (0.50% p.a. of the 積立金) are three **[std]**
parameters back-solved from nine published dollar figures spanning forty-seven years
[S2]. They reproduce that whole run to within **1.75%** at every duration and to
**0.03%** at duration 50, and the same three parameters reproduce the *other* published
table — the 低解約返戻金特則 form, a different premium and a different contract — to within
5.20% out to duration 20. A back-solve is re-solved whenever its inputs move: adopting
the library's canonical mortality proxy changed the cost-of-insurance basis at every
attained age above 40, and `prem_charge_late` re-solved from 12% to 13% with the other
two unmoved. The model reproduces the notes' own figures for both fits cell
for cell, and the test module carries both tables hard-coded — the model's values and the
published ones side by side, so that the deviation is asserted rather than described.

Two independent consequences fall out of the fit rather than being imposed, and both are
checks on it. Under the prospective definition of the uplift benchmark the fund crosses
its 予定利率 benchmark by **+US$8.73** at 払込満了 — a contract that is almost exactly
self-funding at the guaranteed floor, which is what actuarial equivalence predicts. And
the account value overtakes the sum assured at month **740**, attained age 101, where the
net amount at risk goes to zero and the cost-of-insurance charge stops.

One caveat the fit does not cover, and it shows in a shipped model point. The
reduced-surrender-value special condition (*tei-kaiyaku-henreikin tokusoku*, 低解約返戻金特則)
form's lower premium of US$225.00 is **not** self-funding to the terminal age at this
charge stack: on model point 2 the 積立金 is exhausted in the sixth decade and the
guaranteed 終身 cover is thereafter carried by the insurer rather than by the fund, with a
nil surrender value. `charge_coi()` is capped at what the fund holds so that the 積立金 can
never run negative — it is an account, not a debt — and without that cap the shortfall
compounds into the net amount at risk and the projection diverges. The notes already flag
that published table's durations 30, 40 and 50 as `[unverified]`, and this is the same fact
seen from the model side.

## Two mechanics that vanish at the guaranteed floor

The base run credits at `ic = i0`, the contract's own 予定利率 — the guaranteed column of
the only published surrender-value run, and the only crediting figure for the LEVEL
shape that is a contract term rather than an illustration [S2].

`av0_pp(t)`, the uplift's benchmark, is defined **[std]** as the account value the *same*
recursion produces with `ic` replaced by `i0` and the benchmark benefit held at `SA`. It
follows that whenever `ic = i0` the two funds coincide exactly, so `idb_pp(t)` is
identically zero and `special_reserve_pp(t)` with it. The published guaranteed column
shows 特別積立金 of (0) at both 10 and 20 years [S2], so that is what a correct
implementation must produce: **a non-zero uplift or top-up on the base run is a bug, not
a refinement**, and both are tests.

The special reserve top-up (*tokubetsu tsumitatekin*, 特別積立金) itself is not merely
set to zero; it is a fitted mechanic that happens to be zero here. It is a share of the
fund's excess over its benchmark, 0.24 at ten years and 0.16 at twenty, fitted to the
four published amounts — 147 and 527 on the 3.50% column, 302 and 1,120 on the 4.00%
column — with a worst deviation of 3.7%. The fit is asserted in the test module against
the anchor cell run at each of the two illustration rates, so the two shares are checked
against the document rather than merely carried. Model point 5 credits 3.50% and both
mechanics come alive there, on its own smaller cell.

## Modules that are off in the base run

Seven of the notes' optional constructions are implemented and switched off on the anchor
cell, so that the base run reproduces the worked example while the machinery stays
visible and testable. Every one of them is asserted in **both** positions.

| Module | Switch | Off value | Exercised on | What it does |
|---|---|---|---|---|
| The prospective uplift basis | `idb_basis` | `"fund"` | point 7 | Measures the uplift against `av0_pro_pp(t)`, the fund needed at `t` to carry `SA` with no future premiums on the same charge basis, run backwards from `AV0(T) = SA`. It does *not* give an identically zero uplift — −US$21,818.29 at ten years, +US$8.73 at 払込満了, +US$67.86 at fifty years and +US$22,617.69 at the terminal month — and a definition that manufactures a positive uplift on the guaranteed run contradicts the one document that shows that run, which is why it is the switch and not the base |
| The uplift ratchet | `idb_ratchet` | `True`, and inert there | point 7 (off) | Holds `idb_pp` at its running maximum. It ships *on* and makes no difference in the base run, because the uplift is identically zero at the floor; it is sourced to the ご契約のしおり and not to the extracted 約款第46条 text, so it is `[unverified]` and carried as a switch rather than wired in |
| The 低解約返戻金特則 | `low_cv` | `False` | points 2, 6 | Suppresses the surrender value to `kl`: 0.70 while four or more premium-paying years remain, stepping to 0.775, 0.85, 0.925 and 1.00 on whole remaining years rounded **up**. The step is a cliff; interpolating across it is wrong. It has no release date on a 終身払 contract, so that combination is rejected rather than given one |
| The 自動振替貸付 | `apl_on` | `False` | point 6 | Redirects `apl_nonpay_share` of the surrender decrement into `pols_if_apl(t)` while `apl_intercept(t)` holds — a policy does not lapse while its surrender value can advance the premium — accumulates the advance at `apl_int_rate` in `loan_pp(t)` and repays it out of whatever the policy is eventually paid. On point 6 it engages in policy month 3, the first month the surrender value covers a premium. **Structurally absent on the SINGLE shape** |
| Dynamic surrender on the FX rate | `dyn_lapse` | `False` | point 4 | Multiplies the annual surrender rate by `min(2.5, max(0.5, 1 + β(CV(t)(e − s)/P_jpy0 − 1)))` with `β = 2.0` **[std]**: a policyholder in yen profit surrenders, one in yen loss holds on. SINGLE only, because the yen profit is measured against a single premium paid at a known rate |
| An FX path | `fx_path` | `False` | point 7 | Reads `fx_path_table.csv` by policy year instead of holding the model point's `fx_ttm` flat, its last row carried forward |
| The target-value rider | `target_on` / `target_action` | `False` / `"none"` | points 3 (convert), 4 (surrender) | Converts or surrenders the contract at `target_month()`. `target_action` has **no default** where the rider is elected; see below |

Two further levers are model point columns rather than modules, and both ship at their
neutral value. `mort_be_factor` is 1.00 on every point but 7, where it is 1.20 — **at 1.00
the
base run is a valuation-table run, not a best estimate** [REG-R20]. `mva_delta` is 0.0
everywhere but point 4, where it is −1.0% and the adjustment turns negative.

The two levers interact with the horizon in a way worth naming: because `mort_be_factor`
moves
the decrement, point 7's cohort is exhausted at attained age 108 — where `1.20 × 0.90733`
is capped at 1 — a year before the table's terminal age, while `coi_rate` still reads
0.90733 there. Nothing is truncated; the load simply reaches 1 first.

## The target-value rider, and what a deterministic run cannot say

`target_month()` is the first month at or after the contractual one-year dead zone at
which the **yen-converted surrender value** reaches the 目標額. Two things about that test
are easy to get wrong and both are contractual [S9]: it runs on `cv_pp`, after FX and
after the MVA, not on `av_pp`; and the dead zone is real. On the base SINGLE cell the
model converts at month **52**; testing the account value instead converts at month 39,
thirteen months early, and the two counterfactuals that drop one deduction at a time land
at month 41 (no 解約控除) and month 50 (no MVA). All four are in the test module.

`target_action` has **no default**. The 約款 converts the contract to a yen whole life
[S8] [S9]; at every focus-monitored distributor most ターゲット型 policies are instead
**surrendered** on the hit and the same product immediately re-sold to the same customer,
paying the front-loaded commission twice [R5] [R6]. The contract and the evidence
disagree and neither is the modeller's to assume silently, so the model point must
choose. Under `"surrender"` the value leaves through `claims(t, "LAPSE")`; under
`"convert"` it leaves through `conversions(t)`, and **the yen contract it becomes is out
of scope** — this ledger is denominated in dollars and the converted liability is not.
That scope boundary is **[std]**, and it is why the two elections differ in where the
money is booked rather than in how much of it there is. Model point 3 converts, model
point 4 surrenders.

Only point 3 is the notes' cell. Point 4 carries the negative 市場価格調整 and dynamic
surrender as well, so its trigger lands at month **33** rather than 52 — the deliberate
variant, not a discrepancy, and the test module pins both months so a reader does not
read point 4 against the notes' anchor.

What a deterministic run cannot do is value the *option*. On one path the rider either
converts at one determinate month or never converts, so its time value is zero by
construction — the same degeneracy `uklib`'s RPI ratchet suffers under a monotone index
path. A scenario set is the only instrument that can price it and this library does not
ship one.

## The account-value charges are not cash flows

`charge_init`, `charge_maint` and `charge_coi` are internal transfers from the 積立金 to
the insurer. They move `av_pp` and appear **nowhere** in `net_cf`; the insurer's outgo is
the expense and commission stream instead. Booking a charge as revenue alongside the
premium that funded it double-counts the premium, and `check_net_cf()` rebuilds `net_cf`
from the premium decomposed into the part that reaches the fund plus the charge, so it
would catch exactly that.

The order inside the month is fixed, because it changes the answer at the third decimal
and the published run is reproduced to the dollar: premium in, then `charge_init`, then
`charge_maint`, then `charge_coi` on the net amount at risk measured *after* the
maintenance charge, then interest at `(1 + ic)^(1/12)` — the geometric twelfth root
**[std]**, not `ic/12`.

## Sign convention

The notes' `CF(t)` is already income positive — premiums less claims, surrender
benefits, conversions, claim expense, acquisition and maintenance expense and commission —
which is the library-wide sign of
`net_cf`, so there is no outgo-positive `liability_cf` companion to publish: one stream,
one sign, one name.

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever
those models have an analogue: `pols_*` for policy counts, plural nouns for cash flows,
`*_rate` for annual rates with `*_rate_mth` for the monthly ones, `*_pp` for per-policy
amounts, `claims(t, kind)` with an uppercase `kind`, and `av_pp_at(t, timing)` /
`pols_if_at(t, timing)` for the within-month reads. The technical notes use compact
actuarial symbols; the full mapping lives in the `Projection` Space docstring. Six cases
needed care:

| Notes | Cells | Why |
|---|---|---|
| `AV(t)`, `CV(t)` | `av_pp` / `cv_pp` | The savings chassis pays a cash surrender value and has no account value; this product has both, and **they are not interchangeable** — `CV = AV (1 − mva − sc) kl`, so every charge in the product sits between the two names |
| `AV0(t)` | `av0_pp` / `av0_pro_pp` | One symbol, two defensible definitions — the same recursion at `i0`, and the prospective fund at `i0` — and the model point chooses between them with `idb_basis`. Collapsing them to one name would have hidden that the choice is worth US$22,617.69 at the terminal month |
| `q(t)` | `mort_rate` / `coi_rate` | One symbol for the decrement and for the cost-of-insurance basis, which are a *different kind of assumption*: `mort_be_factor` moves the first and must never move the second |
| `C_init`, `C_maint`, `C_coi` | `charge_init` / `charge_maint` / `charge_coi` | Named as charges, not as cash flows, because they are internal transfers from the 積立金 and appear in no `result_cf()` column |
| `CF_JPY(t)` | `net_cf_jpy` / `fx_spread_jpy` | The yen ledger is two published quantities, not one: the three-rate translation and the spread income that separates it from `net_cf × e`. A single yen column would have to hide one of them |
| *(no symbol)* | `conversions` | A target conversion is deliberately **not** a `claims` kind. It is an owner election moving the liability to another product line rather than a benefit payment — the same distinction that spells withdrawals `withdrawals` rather than `claims_wd` — and the notes' column list had nowhere to book it until this column was added |

`prem_due_pp(t)` is the premium *due* per policy in month `t` and `premiums(t)` the income
actually received, which differ wherever the 自動振替貸付 is advancing: the fund is credited,
the insurer is paid nothing. It is spelled `prem_due_pp` rather than `premium_pp` because
`premium_pp` is the library's name for an **annual** per-policy premium, and this one is a
time-varying amount due in a month; the level monthly amount is `premium_mth_pp()`.
`pols_payer(t)` and `pols_if_apl(t)` are the two cohorts whose sum is `pols_if(t)`, and the
premium column is carried on the first alone.

`claim_expenses(t)` is its own cells and its own `result_cf()` column, and `expenses(t)` is
acquisition and maintenance only. The two are driven by different levers — the death
decrement and the in-force count — so folding one into the other would hide which of them
moved; this is the settled library meaning of `expenses`.

The in-force roll-forward check is `check_pols_roll_fwd()` / `check_pols_roll_fwd_resid(t)`,
the settled name in both sister libraries, and the multiplier that turns the shipped
valuation table into the projection basis is `mort_be_factor`.

## Standardizations used

Everything quantitative that is not a contract term. The load-bearing ones:

| Standardization | Value | Why |
|---|---|---|
| Charge stack `φ1` / `φ2` / `μ` | 38% / 13% / 0.50% p.a. | back-solved from the published guaranteed run [S2]; no carrier publishes the rates |
| Monthly interest convention | `(1 + i)^(1/12)` | stated because the published run is reproduced to the dollar |
| Mortality construction | one canonical library table, log-linear in `ln q` between sourced anchors | the published table may be cited and quoted but not redistributed [REG-R21] |
| `mort_be_factor` | 1.00 | the base run is a valuation-table run, so every figure is checkable |
| MVA constants `A` / `r0` / `d` | 0.10% / 3.00% / 0.70 | fitted to the published 15-year rate table [S3] |
| 特別積立金 rates | 0.24 / 0.16 | fitted to four published amounts [S2] |
| LEVEL surrender curve | 8 / 7 / 6 / 5 / 5 / 4 / 3% | no public anchor of any kind exists |
| SINGLE surrender curve | 28 / 23 / 18 / 14 / 8% | calibrated to a 60.90% four-year exit [R5] |
| FX path | flat at ¥159.43 | this library models contractual cash flows, not an FX view [S11] |
| Expenses and commission | US$300 / US$60 p.a. / US$150; 90% and 3%, or 5.5% and 0.75% p.a. | no carrier publishes an expense basis; only the upfront *pattern* is evidenced [R5] [S13] |
| `apl_nonpay_share` | 0.30 | no source splits the surrender decrement into voluntary and non-payment parts |
| `apl_int_rate` | 2.75% p.a. | the savings chassis's own level, taken unchanged — this product changes whether a shape *has* an APL, not what it costs |
| The APL cohort's loan | one aggregate average, `loan_total / pols_if_apl` | exact for the total and approximate per policy at exit; a full entry-year triangle would add a dimension the module's evidence does not support |
| `charge_coi` cap | the charge cannot exceed the fund | the 積立金 is an account, not a debt; without the cap the 特則 point's shortfall compounds into the net amount at risk and diverges |
| `av0_pro_pp` terminal condition | `AV0(T) = SA` | not stated in the notes, but uniquely pinned by them: with `AV0(T) = 0` the three early figures still match and the terminal one comes out at +72,515.47 instead of +22,617.69 |
| Interpolated ages | log-linear in `ln q` between the two neighbouring anchors, five decimals | no extrapolation anywhere: both sexes run from an age-0 anchor to a terminal anchor |
| Dynamic surrender `β` / floor / cap | 2.0 / 0.5 / 2.5 | no retrieved source quantifies FX-driven surrender behaviour at all |
| Premiums on points 5, 6 and 7 | US$120.00 / US$560.00 / US$180.00 | only the anchor cell's US$239.60 and the 特則 form's US$225.00 are published; these are chosen so the fund stays positive |
| Target scope boundary | the yen contract is out of scope | this ledger is in dollars |

## Tests

`tests/test_model_conventions_jp.py` asserts the house style — the layout, the
`Data`/`Projection` split, the read-once property, the docstrings, the naming, the
`check_*` contract and the read-write-re-read round trip — parametrized over the model
registry.

`tests/test_fx_whole_life_jp.py` asserts this product, in 121 tests:

- **The notes' worked example, hard-coded as module-level tables** — `TRACE` for the
  month 0, 1 and 2 traces, `FIRST_PERIODS` for the printed cash-flow table, `CALIBRATION`
  for the nine-duration fit and `MVA_ROW` for the rate-move row — carrying the digits the
  notes display and no more, so a reviewer can lay the module beside the document and
  compare by eye. The tolerance on each trace line is derived from the digits printed
  rather than chosen. Also the 特則 cross-check to the cent, the whole-run dollar and yen
  totals, the ¥125.17 month-0 and ¥39,146 whole-run spread, the whole-run yen identity
  summed **on the FX path** rather than translated once at the issue-date rate, and
  `Σ D + Σ S = 1` to nine decimals. The 特別積立金 shares get the same treatment: the anchor
  cell is re-run at each illustration rate and the two top-ups are asserted against the
  published 147 / 527 and
  302 / 1,120 within the 3.7% the fit claims, so the second fitted mechanic is checked
  against its document rather than only described.
- **Every entry in the notes' Known modeling pitfalls list**, each named after its
  pitfall; a comment block at the head of the module pairs the two so that a pitfall
  without a test is visible. Among them: the dollar ledger not stirring when the exchange
  rate is moved, the charges staying out of `net_cf`, `av_pp` not being `cv_pp`, the MVA
  being symmetric rather than floored and zero on a 積立利率計算基準日, the surrender charge's
  base being the 積立金, the target test running on the surrender value with all three
  counterfactual months, the dead zone, the uplift and the top-up being identically zero
  at the floor, `mort_be_factor` not moving the charge, the APL's absence on the SINGLE
  shape,
  the policy month rather than the calendar month, the geometric twelfth root, the
  低解約返戻金 release as a step, the fund overtaking the sum assured at month 740 with the
  charge floored and the benefit not, the fund being *exhausted* on the 低解約返戻金特則 point
  with `charge_coi` capped at what it holds, and a refused claim still paying the fund.
- **Each optional module in both positions**, off in the base run and switched on where a
  model point elects it, including the two target elections booking the same money in
  different columns.
- **The identities**: the five `check_*` cells on all eight model points, plus the
  in-force roll-forward rebuilt month by month independently of the recursion, on all
  eight.
- **The structural product facts**: no maturity and no tail states; the horizon read off
  the table, 109 male and 113 female, with the terminal year emptying in its first month
  because `q = 1` is an annual rate; 終身払 resolved against the horizon; death before
  surrender as the processing order; the shipped mortality table's row-by-row provenance
  and its sourced anchors; and an issue age the table cannot serve raising rather than
  being priced silently.
- **The scope refusals**: nine model point mutations that must be rejected by name — the
  yen-premium shape, a non-USD currency, an unknown uplift basis or target action, an
  invalid sex, the APL on the SINGLE shape, the target rider or dynamic surrender on the
  LEVEL shape, and the 低解約返戻金特則 on a 終身払 contract.
- **Both halves of the external-input bargain**: an input swapped by repointing a
  filename Reference with no formula change, and a read → write → re-read round trip that
  reproduces the worked example once the CSVs travel with the model.

```bash
python -m pytest tests/test_fx_whole_life_jp.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R5]: #jplib-fx_whole_life-r5
[R6]: #jplib-fx_whole_life-r6
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[std]: #jplib-std
<!-- END generated citation links -->
