# Implementation Notes

**Status:** Draft, 2026-08-20. Built from [`technical-notes.md`](technical-notes.md) (the
product as a liability cash flow model on paper) and [`product-spec.md`](product-spec.md)
(the representative contract those notes model). Source tags resolve against
[`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The contractual
> mechanics are sourced — the 死亡給付金 as cumulative premiums paid, the 解約返戻金
> (*kaiyaku-henreikin*, surrender value) capped at that same amount, the unavailability of
> surrender from the 年金支払開始日, the unconditional 確定年金 instalments, the 年金の一括払
> factor table, the 自動振替貸付 interest ceiling and the conditions of the 税制適格特約
> (*zeisei tekikaku tokuyaku*), the tax-qualification rider (*tokuyaku*, 特約). Nearly
> everything quantitative is a standardization. The two assumed interest rates (*yotei
> riritsu*, 予定利率) are published [S5] [S8] but the 予定事業費率 and the 年金支払開始時費用 are
> calibrated **[std]** against one published specimen [S6], because the 算出方法書 is a
> 基礎書類 filed with the FSA and not published [REG-R2]; no carrier publishes an expense basis, a commission scale or a
> lapse curve by duration; and the mortality basis is **not** a published table.
> 生保標準生命表2018 and the 2007 年金開始後用 table are readable at stable public URLs but cannot be
> redistributed [REG-R21], so this library ships a documented proxy anchored to quoted
> rates — the canonical library-wide 死亡保険用 table, and three spot rates on 年金開始後用.
> Replace the assumption tables with company data, and the mortality basis with a licensed
> one, before drawing any conclusion from the output.

`Annuity_JP_A` is the annual-grid model of the fixed individual annuity insurance (*teigaku
kojin nenkin hoken*, 定額個人年金保険) composite with the 税制適格特約 attached. It is the
library's **payout chassis**: the deferral phase is a savings accumulation and the payout
phase is the annuity machinery the other stream-benefit products point at.

## Run it

```bash
python products/individual_annuity/run.py        # the worked example's anchor cell
python products/individual_annuity/run.py 4      # another model point
```

`run.py` prints the model point, the annuitisation quantities, the head and the tail of
`result_cf()`, the undiscounted total, and every `check_*()` cells. Its output is ASCII
only, so it prints on a Windows console under any code page: amounts are written "JPY" and
Japanese terms are romanized.

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/individual_annuity/Annuity_JP_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the anchor cell of the notes' worked
example. `result_cf()` returns a `DataFrame` indexed by policy year `t` with `pols_if` first
and `net_cf` last. `result_pols()` publishes the decrement and value runs beside it — the
two in-force measures, the decrements that move them, and the fund, death benefit and
surrender value that price them — because on this product the relationship between those
three values *is* the product, and printing them only inside a cash flow is not enough.

## The product is two contracts joined at one date

Before the annuity commencement date (*nenkin shiharai kaishi bi*, 年金支払開始日) the liability
is a savings fund: a level office premium net of the 予定事業費率 accumulates at the deferral
予定利率 with a **survivorship release**, against a 死亡給付金 capped at cumulative premiums and a
解約返戻金 capped at the 死亡給付金. After that date the liability is a stream of instalments that
does not depend on survival at all.

Everything switches at `t = n`, and the model puts each switch in exactly one cells:

| What switches | Where it lives |
|---|---|
| The mortality table, 死亡保険用 to 年金開始後用 | `mort_table_name(t)` |
| The best-estimate factor, 0.85 to 1.10 | `mort_be_factor(t)` |
| The availability of surrender | `cv_pp(t)`, `lapse_rate_base(t)` |
| The in-force rule, decrementing to unconditional | `pols_if(t)` |
| The expense level, ¥4,000 to ¥2,000 p.a. | `expenses(t)` |

`n` is read off the model point's own 年金支払開始日 rather than summed from the 保険料払込期間 and
the 据置期間, and `annuity_start_age()` raises unless the two agree. That check has to sit on
the path every projection takes: reached only through `tax_rider()` it would validate the
base form's model points never, and two spellings of one date is how a projection silently
annuitises on the wrong year.

Two in-force measures are carried, following `SPIA_US_S`. **`pols_if` counts contracts with
an obligation open; `lives_if` counts annuitants alive.** They separate in the deferral
phase because lapse removes a contract without removing a life, and in the payout phase for
the opposite reason: on a 確定年金 the instalments are unconditional, so `pols_if` is flat
through the certain period while `lives_if` runs down on the payout table. At the anchor
cell `lives_if` falls from 0.91268274 to 0.77848987 over the ten payout years — 14.70% of
the annuitants alive at 65 die — without moving a single yen of projected cash flow.
Collapsing the two is the notes' second pitfall and the single most likely way to build this
product wrongly.

## The fund and the surrender value are different quantities

`av_pp` is the premium reserve fund (*hokenryō tsumitatekin*, 保険料積立金); `cv_pp` is the
解約返戻金. The recursion

```
V(t+1) = [ (V(t) + NP(t)) (1 + i_d) - q'(x+t) DB(t+1) ] / (1 - q'(x+t))
```

divides by `(1 - q')` because the premiums of those who die are released to the survivors
net of the death benefit paid. Since `DB` is capped at cumulative premiums and `V` is not,
that release turns positive from the duration at which `V` first exceeds `DB` — policy year
13 at the anchor cell — and the excess of `av_pp` over `db_pp`, ¥791,563.274447 by `t = 34`,
is precisely the survival benefit the design buys. It is what pays for the annuity.

So the ceiling is applied to `cv_pp` and never to `av_pp`. Clipping the fund instead would
pass `check_cv_cap()` and destroy the 年金原資: annuitising ¥5,400,000 instead of
¥6,261,482.08 buys 13.7% less annuity. `check_cv_cap()` asserts `cv_pp(t) <= db_pp(t)` at
every deferral duration, which is the sourced invariant [S2] [S4]; the crossover is where
that residual reaches zero and stays there.

The recursion uses `mort_rate_pricing`, the 予定死亡率 at 100% of the 死亡保険用 table, and never
`mort_rate`, the best-estimate decrement — `av_pp` is a contractual quantity and not an
experience projection. Lapse does not appear in it at all: the surrender release is the
解約控除, which accrues to the insurer rather than to the surviving fund. `check_fund()`
catches both of the ways this recursion is usually built wrongly, since a model that had put
lapse into it, or that had used the best-estimate rate in place of `q'`, fails there rather
than silently misstating the 年金原資.

## The annuitisation transition

At `t = n` three things happen in one step: the 年金原資 `F = V(n)` is struck net of any loan
balance; the 基本年金額 `B` is derived from it once and never recomputed; and the mortality
table and its best-estimate factor both switch. `B` is rounded **down to the nearest ¥100**
inside the model, because Japanese specimens are published at that granularity and it is a
contractual amount rather than a display convention [S3] [S5] [S6] [S10] — worth ¥15.281 a
year of annuity at the anchor cell, given up rather than rounded away on the screen.

The conversion rate is `i_p` = 0.65%, not the deferral rate: the payout phase is priced on
its own 予定利率, published separately and left unchanged when that carrier's deferral rates
moved [S5]. Using `i_d` to buy the annuity overstates `B` by 1.55% at `k` = 10 — in the
direction a reader would not guess, since the payout rate is the *lower* one, so each yen of
年金原資 buys less annuity, not more.

## Two mortality tables, and why the model ships anchors rather than coefficients

生保標準生命表2018（死亡保険用）and 生保標準生命表2007（年金開始後用）are published by 日本アクチュアリー会 at stable public
URLs, free and in full — a real contrast with the CMI tables `uklib` cannot read at all. But
the publisher's terms prohibit reproduction and transmission to third parties without
written consent [REG-R21], so this library **ships no copy of either**. What it ships are two
**[std]** constructions, built differently because their anchor sets are.

`death_cover_2018` is the **canonical `jplib` table**: one file, shared by every product in
the library that reads 生保標準生命表2018（死亡保険用）, so that a given cell carries the same value and
the same provenance wherever it is shipped. Its anchor rows are rates read from the IAJ table
and quoted under attribution [REG-R18]; every age between two anchors is graduated
**log-linearly in `ln q`**, evaluated in double precision and rounded to five decimal places.
Nothing is extrapolated — both sexes run from an age-0 anchor to a terminal anchor — and both
sexes carry their own sourced anchors, so there is no age setback on this table.

`annuity_payout_2007` is a Makeham law `mu(x) = A + B c**x`, `q(x) = 1 - exp(-mu(x))`, solved
in closed form from three published male spot rates, with those three reproduced exactly by
construction and the off-anchor residuals stated rather than hidden in `technical-notes.md`.
Only male spot rates were retrieved for it, so its female rows are the male construction with
a **four-year age setback [std]** — the setback the published terminal ages imply, 126
against 122. No number in the worked example depends on it, the anchor cell being male.

The implementation ships the **anchors**, not the Makeham coefficients the notes display.
Those coefficients are rounded for print and the payout factors are not reproducible from
them. `mort_anchor_table.csv` therefore carries, per table and sex, the anchor ages and rates
and the terminal age; `mort_table.csv` carries the rate the stated graduation produces at
every age, with a `provenance` column marking each row as a sourced anchor or a graduated
value; and `check_mort_graduation()` asserts that the two files still agree — log-linear on
死亡保険用, Makeham on 年金開始後用. Once a licensed or company table is dropped in, a `False` there
is the correct answer, which is why it reports a residual rather than raising.

One caution for a reader holding the notes: the 49% and 89% by which the death-cover table
overstates payout-phase mortality at ages 80 and 90 are comparisons of the two **published**
tables [R3] [REG-R18]. The death-cover halves of that comparison are sourced anchors and come
back exactly from `mort_table.csv`; the payout halves do not, because that table is anchored
only at 60/80/100 and reads 0.077578 at age 90 against the published 0.08318, so the model's
own tables give 49% and 103%. What holds in both is the direction and the materiality, which
is what the pitfall is about.

## Inputs are external files

Seven CSVs live beside `run.py`, not inside the model folder. This is the
`annuallife/TradLife_A` layout rather than `basiclife/BasicTerm_S`'s embedded IOSpec: the
model folder holds `__init__.py` and `_system.json` per Space and nothing else, so a diff of
the model shows logic changes only. The trade-off is that the model is not portable on its
own — copying `Annuity_JP_A/` without its parent's CSVs produces a model that reads and then
fails on first evaluation.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Nine model points, indexed by `point_id` | Point 1 is the notes' anchor cell; its premium is the annualization of a published specimen at the identical model point [S6] |
| `mort_table.csv` | The two [std] mortality tables, by table, sex and age | 死亡保険用 is the canonical library-wide table, log-linear between sourced anchors; 年金開始後用 is a Makeham construction. **Not** a copy of any 日本アクチュアリー会 file [REG-R18] [R3] [REG-R19] |
| `mort_anchor_table.csv` | The published rates each construction is anchored to, and the table's terminal age | Quoted rates [REG-R18] [R3] [REG-R19]; both sexes sourced on 死亡保険用, and the 年金開始後用 female rows a four-year age setback **[std]** |
| `lapse_table.csv` | The [std] 解約・失効 curve, in three phase segments | Anchored to a market-wide 3.4% for FY2024 [R15] [REG-R31]; the duration shape is a standardization |
| `pricing_table.csv` | The two 予定利率, `β`, `θ`, the 解約控除 shape, the two best-estimate factors, the rounding step, and the loan, dividend and dynamic-lapse parameters | [S8] [S5] [S11] [S4] and **[std]** where no document discloses the value |
| `expense_table.csv` | Best-estimate cash expenses and commission | **[std, new here]** throughout |
| `commute_factor_table.csv` | The 年金の一括払 factors for 1–14 remaining instalments | One carrier's published table, verbatim [S2] |

Every assumption row carries a `provenance` column tagging it `[std] …` or with the source
it came from. The readers and every `*_file` Reference live on the `Data` Space, which takes
no parameters, so each file is read **once per model** however many model points are
projected. `Data.input_dir()` resolves to `_model.path.parent` at run time and is never
hard-coded, which is what lets a licensed table drop in as a same-schema CSV with no formula
change.

## Modules that are off in the base run

Six of the notes' optional constructions are implemented and switched off at the anchor
cell, so that the base run reproduces the worked example while the machinery stays visible
and testable. Each is a model point column, so a non-anchor point exercises it.

| Module | Column | Off value | On at |
|---|---|---|---|
| 保証期間付終身年金 life-annuity election | `payout_form` | `certain` | points 4 and 9 |
| 年金の一括払 commutation | `commute_rate` | 0.0 | point 5, at 100% |
| APL (自動振替貸付) | `apl_on` | false | point 7 |
| 契約者貸付 policy loan | `loan_on` | false | point 8 |
| 契約者配当 dividend | `div_rate` | 0.000 | point 8, at 0.2% |
| Dynamic lapse | `rate_new` | 0.0100 (= `i_d`) | point 8, at 1.50% |

Three of them are worth stating in more than a table row.

**保証期間付終身年金 is priced on a basis no model can know.** The election is made at the
年金支払開始日 on the 基礎率 then in force, thirty-five years out at the anchor cell [S2] [S9].
Holding it at the issue basis is a **[std]** modeling choice and the reason base-run take-up
is zero rather than a guess. The module also changes `proj_len()`, which runs to the payout
table's terminal age instead of `n + k`, and `pols_if()`, which is flat through the
guarantee and then runs off on the best-estimate payout basis. Model point 9 is the anchor
cell with nothing changed but the payout form, so the two `B` figures are directly
comparable: ¥281,300 against ¥638,100 out of the same ¥6,261,482.08, because the annuity-due
factor is 22.032668 against 9.714338. That ratio is the product fact the module exists to
show.

**年金の一括払 switches on a composite artefact, not a product feature.** The published factors
imply about 0.40% p.a. while the composite's payout 予定利率 is 0.65%, and the two come from
different carriers [S2] [S5]. At `t = n` with ten instalments remaining the factor 9.921
returns ¥6,330,590.10 against a gross 年金原資 of ¥6,261,482.08, 1.1037% more. Nor is the table
an annuity-due at any positive rate: a single remaining instalment is factored at 1.010 and
two at 2.016, which would need `v > 1`. The model therefore uses the table **verbatim** over
1–14 and the 0.40% annuity-due only outside it, exactly as the notes prescribe, and leaves
base take-up at zero. A production model must re-derive the factors on its own payout basis.

**自動振替貸付 is an election, not a no-lapse rule.** With `apl_on`, the lapse decrement is
suppressed only while the 解約返戻金 is at least one premium and the outstanding balance has not
outgrown it; the balance compounds at the contractual cap of 8% p.a. [S4]; and the moment
principal and interest exceed the 解約返戻金 the whole in-force lapses. On point 7 the module
engages at `t` = 2, carries the contract for six years, and terminates it at `t` = 8. Wiring
it on by default would remove lapse from the model for the wrong reason — and one carrier's
product has no such facility at all [S2].

### Semantics the notes do not fix

Four of the modules needed a reading the notes leave open. Each is resolved here in the
formula's docstring as well as in this list, because a reader who disagrees needs to find
the choice, not infer it.

1. **The APL premium is lent, not received.** While the facility is running,
   `premiums(t)` is zero: the insurer lends the premium rather than collecting it
   **[std]**. And the 保険料積立金 recursion still credits `NP(t)` in the year the facility
   fails, which is an annual-grid artefact worth one year of fund accretion.
2. **The 契約者貸付 drawdown rule.** Half the 解約返戻金 drawn at policy year 20 **[std]**,
   compounding at the sourced 2.40% [S11] [S8] and capped at the 解約返戻金. Both parameters
   are rows in `pricing_table.csv` and neither is sourced as a behaviour.
3. **The 契約者配当 declaration rule.** The composite is a 5年ごと利差配当 design [S4]; the model
   declares `div_rate` on the fund annually and accumulates it at the sourced 0.60% [S11],
   which is a **[std]** simplification of the five-year cycle. Zero in the base run, so no
   shipped figure depends on it — and under the 税制適格特約 the accumulation may never be paid
   in cash, so it appears in `annuity_amount_pp()` and nowhere in the cash flow [S1] [R10].
4. **Dynamic lapse has no premium-shock driver.** Premiums and the 予定利率 are both fixed at
   issue, so the multiplier keys off a **rise** in the new-business 予定利率 instead [S8]:
   `M(t) = min(2, max(1, 1 + 20 max(0, i_new - i_d)))` **[std]**.

減額, 払済 and 復活 are **not** implemented **[std scope]**. On an annual grid a premium unpaid
at `t` terminates the contract at `t`: there is no partial-year 払込猶予期間 state and no
reinstatement re-entry. This model's `lapse_rate` is therefore a net-of-復活 rate by
construction, and a user substituting a gross experience rate will over-decrement.

## Sign convention

The notes print `CF(t)` **income positive**, which is the library-wide sign of `net_cf`, so
this model publishes **no `liability_cf` cells** — that absence is a fact about which
orientation the notes chose, not an omission. A reader comparing the payout years with
`SPIA_US_S`, whose notes print outgo-positive, must flip the sign: this model's payout rows
are large negatives. The anchor cell runs +¥73,414.78 at `t` = 0, turns negative at `t` =
27, and sums undiscounted to −¥516,539.46.

## Naming

Cells names follow lifelib and the library's settled vocabulary. `pols_if(t)` is the count
at the start of period `t` and is the weight on that same `result_cf()` row; `pols_if_at(t,
timing)` gives the within-year reads and `av_pp_at(t, timing)` does the same for the fund;
`prem_to_av_pp` is the premium credited to it; `claims(t, kind)` produces
`claims_annuity`, `claims_death`, `claims_lapse` and `claims_commutation`, each named for
the `kind` that produces it; `mort_rate` and `lapse_rate` are annual, this being an
annual-grid model. The full mapping from the notes' actuarial symbols to the cells names is
the table in the `Projection` docstring, headed `Notes symbol`. Twelve cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `V(t)` and `CV(t)` | `av_pp` / `cv_pp` | Two quantities that are routinely collapsed into one "policy value": the fund runs past the death benefit, the surrender value is capped at it. The library's ruling puts the surrender quantity under `cv_pp`, and this model keeps both |
| `q'(x+t)` and `q(t)` | `mort_rate_pricing` / `mort_rate` | The 予定死亡率 inside the fund and the best-estimate decrement on the in-force are different numbers in every year, and only the first is contractual |
| `l(t)` and `L(t)` | `pols_if` / `lives_if` | Contracts with an obligation open against annuitants alive. On a 確定年金 they come apart completely, and the second weights nothing |
| `w(t)` | `lapse_rate` / `lapse_rate_base` / `lapse_dyn_factor` | The applied rate, the table rate and the dynamic multiplier are three cells because the applied rate is also what 自動振替貸付 overrides — in both directions |
| `B` | `annuity_amount_pp` / `annuity_pp` | The amount struck once at `t = n`, and the instalment payable in a given year. One is a scalar and the other a schedule; sharing a name hides the fact that `B` is never recomputed |
| `F` | `annuity_fund_pp` | Not `av_pp(n)`: the 年金原資 is the fund **net of any loan balance**, and it is the loan deduction that makes the two different cells |
| `E0`, `e(t)` and `ec` | `expenses` / `claim_expenses` | `expenses` is acquisition plus maintenance **only** — the library-wide meaning — and the claim expense is a cells, a `result_cf()` column and a `net_cf` term of its own, because it is the one expense that scales with claims rather than with in-force |
| *(no symbol)* | `pols_maturity` | The library-wide count whose cover ends at the **scheduled end** of the contract, whether or not anything is paid for reaching it — the meaning `BasicTerm_S` and `Term_UK_A` give the name. Here that end is the last 確定年金 instalment. It is not a decrement and not a benefit, but the in-force roll-forward does not close without it, and there is no `claims(t, "MATURITY")` to go with it |
| *(annuity stream)* | `claims_annuity` | Named for the benefit's **form** — a stream rather than a lump sum — so the name alone does not say which contingency pays it. Here it is a **living** benefit, paid on the annuitant surviving to a payment date; the same column is a **death** benefit in [IncomeTerm_JP_S](../income_guarantee/model.md) and a living benefit in [LTC_JP_S](../nursing_care/model.md). The `claims` and `result_cf` docstrings both state the contingency |
| *(APL balance)* | `apl_bal` | The 自動振替貸付 balance per policy. The **same concept** as the savings chassis's `loan_apl_pp(t, s)` in [WholeLife_JP_A](../whole_life/model.md), in a **different shape**: that chassis tracks APL advances as cohorts by vintage year `s`, so its balance carries a second argument, while this product advances at most one premium a year against a single fund and so carries one scalar balance per `t`. A reader moving between the two is reading the same mechanic, not two of them |
| *(table lookup)* | `mort_rate_at_age` / `mort_rate_base` | The library-wide split: `mort_rate_at_age(table, x)` is the lookup keyed by **age**, the single point at which the model touches its mortality input, while `mort_rate_base(t)` is the table rate in **period** `t`. A lookup named for the file it reads hides which of the two a call site wanted |
| *(identities)* | `check_pols_roll_fwd` / `check_lives_roll_fwd` | The settled name for a per-period in-force roll-forward in both sister libraries, matching `SPIA_US_S`, `DIA_US_S` and `PA_UK_S`. `check_lives_roll_fwd` is carried separately because the two measures decrement differently and a model that had collapsed them would still close one of the two |

Three absences are product facts rather than gaps: there is no premium income after 払込満了 and
none at all once the annuity is in payment; there is no lapse decrement and no surrender
value from `t = n - 1`; and there is no maturity *payment*, because the contract does not
mature into a lump sum — it pays its last instalment and ends. `pols_maturity` counts the
contracts reaching that scheduled end; `claims(t, "MATURITY")` does not exist.

## Standardizations used

Every quantitative parameter is either source-tagged in a CSV `provenance` column or marked
`[std]` there. The ones that move the answer most:

1. **`β` = 6.5% and `θ` = 1.0%** — one deferral loading and one payout loading, rather than
   an invented 新契約費 / 維持費 / 集金費 split that no source can confirm; the 算出方法書 is a 基礎書類
   filed with the FSA and not published [REG-R2]. Calibrated at a single model point against
   a published specimen [S6], where they reproduce that carrier's 年金原資 of approximately
   ¥6,260,000 as ¥6,261,482 and its 基本年金額 of ¥638,300 as ¥638,100, −0.031%. A production
   user should re-fit across all six of the specimen's points rather than inherit a
   one-point calibration.
2. **The two mortality constructions and their best-estimate factors**, 0.85 in deferral and
   1.10 in payment. The direction of each is structural — one table is prudent against death
   and the other against longevity — while the size of 1.10 sits on an [unverified] margin,
   because the 作成概要 for the 2007 年金開始後用 table was not retrieved.
3. **The 解約控除**: one annual premium running off linearly over ten policy years. Both 約款
   state the shape and not the parameters [S2] [S4]. The base amount is what makes the
   sourced invariant hold — at the anchor cell `cv_pp(1)` is ¥7,976.18 against ¥180,000 of
   premium paid, nil-or-negligible as both 約款 require, while `cv_pp(0)` is zero.
4. **The lapse curve.** The only public figure is a market-wide 3.4% for FY2024 whose
   denominator is pre-annuitisation in-force 契約高, not policy count [R15] [REG-R31]. On the
   anchor cell the shipped curve averages **3.4160%** weighted by `pols_if` and **2.4754%**
   weighted by `av_pp`, both over `t = 0 … n − 1`. The two weightings are not
   interchangeable and a calibration must say which one it used, which is why
   `lapse_rate_mean(weighting)` is a published cells and not a comment.
5. **The module semantics listed above** — the lent APL premium, the loan drawdown rule, the
   annual dividend declaration and the dynamic-lapse driver. None of them moves a shipped
   figure, because all four are off in the base run; all four move a model point that is
   shipped, which is why they are parameters in `pricing_table.csv` and not constants.

## Tests

`tests/test_model_conventions_jp.py` asserts the house style for every model in the library:
the folder layout, the `Data` / `Projection` split, the read-once property, the docstring
contract, the naming rules, `result_cf()`'s column conventions, that every model point
projects without NaN, and that `read → write → re-read` reproduces the same file set and the
same numbers.

`tests/test_individual_annuity_jp.py` asserts what this product owes on top of that. The
notes' worked example is hard-coded there — the annuitisation quantities (`F` =
¥6,261,482.075674, `ä(10, 0.65%)` = 9.71433757, `B` raw ¥638,115.281 rounding to ¥638,100,
一括受取率 115.9534%, 年金受取率 118.1667%), the four deferral rows, the fund and surrender value at
the crossover, the last deferral year, the payout rows, the year-by-year traces and both
totals — so that a reviewer can check it against the notes by eye. Every pitfall the notes
list earns a test named after it: the two tables and their opposite margins, instalments
that are certain rather than life-contingent, the cap that binds on `cv_pp` and not on
`av_pp`, the lapse decrement that stops at `t = n - 1`, 払込満了 against the 年金支払開始日, the two
予定利率, the death benefit that stops growing, the commutation factors that are not the payout
basis, the lapse rate whose denominator is 契約高, dividends that are zero rather than absent,
the APL that is an election, and the 基本年金額 that is struck once. Each of the six optional
modules is asserted in **both** positions, off and on, and the structural facts — no tail
states, a horizon that is the payout table's terminal age on the life form, a zero 据置期間, the
0.70 tontine ratio, the payout table's female setback, and the model points the model rejects
by name — are
asserted too.

Seven `check_*()` cells assert the identities the notes imply, each taking no argument and
returning a `bool` over all `t`, with the signed per-period residual at `check_*_resid(t)`.
All seven return `True` on all nine shipped model points.

| Check | Identity |
|---|---|
| `check_pols_roll_fwd()` | `l(t) - l(t+1) = deaths + lapses + commutations + expiries` |
| `check_lives_roll_fwd()` | `L(t) - L(t+1) = L(t) q(t)`, on whichever table the phase reads |
| `check_fund()` | `(V(t) + NP(t))(1 + i_d) = q' DB(t+1) + (1 - q') V(t+1)` over the deferral phase |
| `check_cv_cap()` | `cv_pp(t) <= db_pp(t)` at every deferral duration |
| `check_annuity_total()` | the undiscounted guaranteed instalments sum to `kB`, or `gB` on the life form |
| `check_net_cf()` | the published `result_cf()` columns add up to `net_cf(t)` |
| `check_mort_graduation()` | the shipped rates are still the graduation of the quoted anchors |

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #jplib-individual_annuity-r10
[R15]: #jplib-individual_annuity-r15
[R3]: #jplib-individual_annuity-r3
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R21]: #jplib-reg-r21
[REG-R31]: #jplib-reg-r31
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
