# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`technical-notes.md`](technical-notes.md); the
product those notes describe is specified in [`product-spec.md`](product-spec.md), and every
source tag on this page resolves in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced: the five-line fee stack and the 해약공제 scale from
> one carrier's 상품요약서 [S2], the guarantee design and both guarantee charges from a
> second carrier's 상품안내장 [S1], the two deduction points and the 좌수/기준가격
> arithmetic from a 231-page 약관 [S7], the 연금 지급 apparatus from [S4] [S5] [S8], and
> the commission scale from the 2017 industry census [R1]. Everything else is **[std]**:
> every return assumption, both columns of `mort_table.csv` (a documented proxy for the
> 제10회 경험생명표, which is **not published** [REG-R33] [REG-R34]), the lapse curve, the
> insurer's own unit expenses, the 위험보험료 age scale, and the monthly discretization of
> a daily unit ledger. Replace them with company data before drawing any conclusion from
> the output. On this product that warning carries more weight than anywhere else in
> `krlib`, because two of the things the model is asked to value are **written options**
> and one deterministic path values an option at its intrinsic value only.

## Run it

```bash
python products/variable_annuity/run.py            # the anchor cell, point_id = 1
python products/variable_annuity/run.py 4          # the in-the-money GMAB cell
```

`run.py` prints the model point, the charge stack in month 0 laid out by base and by
deduction point, the two guarantees at 연금개시, the guarantee charges collected against
the guarantee cost incurred, the first thirteen months of the cash flow statement, the
undiscounted totals, the account-boundary reconciliation and the eight `check_*`
identities. Everything it prints is ASCII, so the output lands on a Windows console under
any code page: amounts are labelled `KRW`, and the product, both accounts and every Korean
term are romanized. The block below is that output with the horizontal rule lines
dropped, five over-long lines cut at the right margin with a trailing `...`, and three
sections elided at `[ ... ]`; the thirteen-row statement and the totals are reproduced
in full in [`technical-notes.md`](technical-notes.md):

```text
VA_KR_S - byeonaek yeongeum boheom (Variable Annuity), monthly grid, boheom nai
model point 1: VA-000001 - M boheom nai 40 at issue, gibon boheomnyo KRW 300,000 per month
  10-nyeonnap (120 premiums, KRW 36,000,000 boheomnyo chongaek); yeongeum gaesi nai 60; 240 ...
  guarantee form: bojeunghyeong (GMAB on); fund set bond50_eq50 (chaegwonhyeong floor 50% o ...
  return path 'base': gross asset return 3.00% bond / 3.00% equity, less unyong bosu 0.40% ...
  payout: jongsin yeongeum-hyeong, 10-year bojeung gigan, jeongaekhyeong, at 2.50% (decl_20 ...

charge stack, per contract, first month (KRW) - five bases, three deduction points
  from the premium, in the ilban gyejeong (never enters the teukbyeol gyejeong):
    gyeyak chegyeol biyong             15,510.00
    gyeyak gwalli biyong (nabip)       10,500.00
    gitabiyong                              0.00
    = teukbyeol gyejeong tuip         273,990.00   (91.33% of the gibon boheomnyo)
  from the gyeyakja jeongnibaek, on the wol gyeyak haedangil (wolgongjeaek):
    wiheom boheomnyo                       24.00
    gyeyak gwalli biyong (hu)               0.00   (steps in at nabip wallyo: 3,990.00)
    GMDB bojeung biyong                    15.98
    GMAB bojeung biyong, asset             57.08
    GMAB bojeung biyong, premium        9,000.00   (on boheomnyo chongaek 36,000,000, max 7 ...
  inside the gijun gagyeok, daily (modelled monthly):
    teukbyeol gyejeong unyong bosu        110.64
    jeungkwon georae / gicho fund           0.00   (nil in the base run [std])
  on surrender, out of the gyeyakja jeongnibaek:
    haeyak gongjeaek at t = 0         830,000.00   (pyojun haeyak gongjeaek cap 1,643,940.00)

the two guarantees at the yeongeum gaesi nai gyeyak haedangil (month 240)
  gyeyakja jeongnibaek AV(T)         43,883,943.57
  choejeo yeongeum jeongnipgeum K    36,000,000.00   (imi nabiphan boheomnyo, 100%)
  GMAB payoff max(0, K - AV(T))               0.00   <- INTRINSIC VALUE ON ONE PATH ONLY
  yeongeum jaewon transferred        43,883,943.57   (teukbyeol gyejeong -> ilban gyejeong)
  annuity factor / yeongeum yeonaek      20.139842     2,178,961.61 gross, 2,168,066.80 net
  reaching yeongeum gaesi                 0.092584   of 1.0000 contracts at issue

    [ the five-line Jensen's-inequality warning on what one path can value ]

guarantee charges collected against guarantee cost incurred, undiscounted (KRW)
  GMDB  charged        79,244.38   incurred         4,945.39   residual        74,298.99
  GMAB  charged       657,417.59   incurred             0.00   residual       657,417.59
  The residual is a SINGLE-PATH RESIDUAL and not a profit.

    [ the t = 0..12 rows of result_cf(), eleven columns ]
    [ the undiscounted totals over 960 months ]

account boundary: net_cf = net_cf_gen + net_cf_sep, at the first three months
  t =   0   net_cf       -43,227.86 = ilban      -300,818.34 + teukbyeol       257,590.48
  t =   1   net_cf       249,787.95 = ilban         6,362.85 + teukbyeol       243,425.10
  t =   2   net_cf       242,993.73 = ilban        13,167.96 + teukbyeol       229,825.77

checks
  check_av_roll_fwd()      True
  check_bond_floor()       True
  check_charge_split()     True
  check_gmdb_floor()       True
  check_net_cf()           True
  check_pols_roll_fwd()    True
  check_prem_alloc()       True
  check_surr_chg_cap()     True
```

Four lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/variable_annuity/VA_KR_S")
model.Projection[1].result_cf()        # the worked example's anchor cell
model.Projection[1].result_charges()   # the fee stack, one column per line
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by projection month `t`, one column per cash
flow line. **The time index is 0-based**, lifelib's convention: `t = 0` is the month
containing the 계약일 and the first 기본보험료, `pols_if(0) == pols_if_init()`, and
`proj_len()` is the **number** of projected months, so the frame is `range(proj_len())`,
the last row is `proj_len() - 1` and `len(result_cf()) == proj_len()`. Policy year is a
contractual 1-based label derived from `t` and never indexed by: `policy_year(t)` =
`t // 12 + 1`, and `yrs_completed(t)` = `(t + 1) // 12` is the completed-years index of the
해약공제 scale. Three companion frames carry what a cash flow statement leaves out:
`result_pols()` the in-force movements and the annuity obligation count, `result_av()` the
계약자적립액 recursion beside the two guarantee bases and the surrender value, and
`result_charges()` the fee stack line by line — the frame this product exists to make
legible, because its ten columns are deducted from **four different bases at three
different times into two different accounts** — 기본보험료, the 계약자적립액 at
`BEF_DEDUCT`, the 보험료총액 and the 특별계정 순자산 at `AFT_DERISK`. (`run.py`'s
month-0 stack counts **five**, because it prints the 해약공제 as well, whose base is the
annualized 기본보험료.) `model.Projection.doc` carries the notes'
symbols mapped to the cells names and states the age basis; `model.Data.doc` says what each
input file is and, for the mortality table, what it is **not**.

## The identity `check_net_cf()` closes: `net_cf = net_cf_gen + net_cf_sep`

`net_cf(t) = net_cf_gen(t) + net_cf_sep(t)` at every projected month — the whole-contract
external cash flow is the sum of the 일반계정 (*ilban gyejeong*, general account) and
특별계정 (*teukbyeol gyejeong*, separate account) ledgers, in which every internal transfer
appears twice with opposite signs and cancels.

That is the one identity no other model in `krlib` has to state. 변액연금보험 is written on
a 특별계정 that 보험업법 제108조제1항제3호 enables and 감독규정 제5-6조제1항제3호 makes
mandatory [REG-R6] [REG-R15] [R4], and 제5-7조 lists **exhaustively** the transfers permitted
across the boundary [REG-R15]. `net_cf(t)` is the external stream — premiums in;
사망보험금, 해약환급금, 연금, 중도인출금, third-party fund costs, the insurer's own expenses
and commission out — and `check_net_cf()` reconstructs it from the two accounts:

| Transfer | 특별계정 | 일반계정 | Cells |
|---|---|---|---|
| 특별계정 투입보험료 | in | out | `prem_to_av` |
| 월공제액 + 특별계정 운용보수 | out | in | `av_charges` |
| 해약공제액 retained on a 해지 | out | in | `surr_charges` |
| 연금재원 at 연금개시 | out | in | `av_transfer` |

Two movements are deliberately absent from both ledgers because they never cross the
boundary. `prem_charges` — 계약체결비용, 납입 중 계약관리비용, 기타비용 — arrives with the
premium in the 일반계정 and simply does not leave it. `gmab_claims` is the GMAB top-up,
which moves **within** the 일반계정, from the 보증준비금 to the 연금재원; its cash-flow
consequence is a larger annuity for the rest of the projection, and that is where a reader
should look for it. `annuity_charges` is netted off the instalment [S4], so `claims_annuity`
is already the amount paid.

The check is written as a *reconciliation of two independently constructed ledgers* and not
as a restatement of the column sum, because that is what makes it informative: a model that
cannot state it has not represented the boundary. It closes to `val_tol = 1e-8` **relative
to the size of the month's gross flows**, which run to eight figures in won at
annuitisation; at `t = 240` the two ledgers are −₩4,062,956.72 and +₩3,861,950.39 against a
`net_cf` of −₩201,006.33, so an absolute tolerance would either be meaningless or fail on
float64 rounding alone.

## The horizon is the mortality table, not the contract

A 종신연금형 has no maturity date, so `proj_len()` is set by `omega_age = 120` **[std]**.
It is the **number** of projected months — the frame's exclusive end — so the anchor cell
runs `t = 0 … 959` in `proj_len()` = 960 rows, attained 보험나이 119 in the last row, and
model point 10, issued at 70, runs 600 rows ending at `t` = 599. `pols_maturity(t)` fires
in the last row, `t = proj_len() - 1`, and pays **nothing**: `claim_pp(t, "MATURITY")` is
structurally `0.0`. The cells exists so the
truncation is visible in `result_pols()` and closes `check_pols_roll_fwd()`, rather than
being absorbed into the last row's decrements where nobody would see it. `pols_if(959)` is
9.17e−08, so the tail is thin — but it is 719 months long, and the statement is
eleven-twelfths empty for the last sixty years of it.

`claims_maturity` is therefore a column of zeros in every row, and so are `withdrawals` and
`fund_expenses` on the base run. All three are published as columns rather than dropped:
a cash flow statement whose columns change shape with the model point is harder to read
than one with three honest zeros in it, and each of the three is live somewhere in the
shipped table or one CSV edit away — `withdrawals` on model point 9, `fund_expenses` at a
non-zero `fund_expense` rate, `claims_maturity` nowhere at all, which is itself the fact.

## The premium meets the contract at two points, and the deduction steps *up*

Confusing them is the commonest way to get a Korean variable model wrong, and the
conditions are explicit [S7 제2조]. At **premium payment**, in the 일반계정,
`prem_charge_pp` is taken out of the gross premium and never enters the fund. On the
**월계약해당일**, `mth_deduct_pp` — the 월공제액 — is cancelled out of the 계약자적립액. The
특별계정 운용보수 is different again: it is deducted inside the **기준가격**
[S7 제43조제2호], so it is written as a factor on the growth (`fund_growth`) rather than as
a unit cancellation, and `check_charge_split()` asserts that the gross asset return splits
exactly into the fee and the credited return.

The consequence a model most easily gets wrong is at **납입완료**. The 계약관리비용 for the
period *after* the premium term is collected *during* it, inside the 특별계정 투입보험료
[R2], and drawn back out month by month afterwards — so at `pay_months()` the monthly
deduction rises by ₩3,990 with no premium arriving to offset it: `mth_deduct_pp(119)` =
₩9,557.24 against `mth_deduct_pp(120)` = ₩13,568.72. [S2]'s own illustration shows the same
thing from the other side: its cumulative separate-account contribution falls from
₩32,877,360 at ten years to ₩32,393,520 at twenty.

On the anchor cell, per contract, in the premium period:

```
납입보험료                                          300,000.00
- 계약체결비용            5.17% of 기본보험료         15,510.00
- 계약관리비용(납입 중)   3.50% of 기본보험료         10,500.00
- 기타비용                0.00%                            0.00
= 특별계정 투입보험료                               273,990.00   (91.33%)
```

`check_prem_alloc()` asserts that 91.33%, which sits inside the 91.3%–91.5% three carriers
publish on this cell [S1] [S2] [S6] and inside [R1]'s industry band of
「납입보험료의 5~15%를 … 차감한 후 85~95%만 투자」. It subtracts 추가납입보험료 first, that
premium carrying no loading at all [S1], and it widens the expected ratio by the
계약체결비용 from `t = 12 × acq_charge_years`, where that charge stops.

## The premium-based guarantee charge is not basis points on the fund

`gmab_charge_prem_pp` is **연 0.30% of 보험료총액** — 「이미 납입한 보험료 및 추후 납입할
기본보험료 합계」, past *and* future premium — for at most seven years [S1]. On the anchor
cell that is ₩9,000 a month against a first-year account of about ₩3.2 million: over 3% a
year of the fund at outset, below 0.5% by year seven. It is a separate cells with a
separate base from `gmab_charge_asset_pp` — ₩57.08 in the same month, a factor of 158 —
for exactly that reason; collapsing the two misstates the early-duration cash flow by an
order of magnitude.

It also **stops before the premiums do**. 「납입기간(최대 7년) 동안」 [S1] is the *shorter*
of the two, so on a 10년납 contract the charge ends at `t = 84` and the 월공제액 falls 57.8%
in one month, from ₩15,422.57 to ₩6,504.62, while the premium keeps arriving for three more
years. That is the single largest discontinuity in the charge stack and it is invisible in
any model that puts guarantee charges on the account value.

Model point 8 shows the asymmetry 추가납입 creates. A paid additional premium is
이미 납입한 보험료, so it grows `gmab_prem_base_pp` **and** the guarantee strike
`prem_paid_pp` — from ₩36,000,000 to ₩72,000,000 by annuitisation — but the charge stops at
seven years and the strike does not.

## What the guarantees are, and what one path says about them

`gmdb_claim_pp(t) = max(0, prem_paid_pp(t) - av_pp(t))` is a real expected cash flow on
this path: the mortality decrement is a probability applied to a deterministic account
value, so a monthly strip of intrinsic values weighted by `pols_death(t)` is a defensible
expected cost. `gmab_claim_pp()` is `max(0, K(T) - AV(T))` at the **single** date
`T = t_ann()`, weighted by `pols_annuitised()`, which carries every decrement — mortality
**and** lapse — that occurred before it. The GMAB is void on surrender, on lapse, on death
before annuitisation and on 조기연금개시 [S1] [S6] [S7 제50조제3항] [S8] [S10] [R1]. On the
anchor cell **9.26% of contracts reach `t_ann()`**, so a model treating the guarantee as a
floor on the account at every duration would overstate its cost roughly tenfold.

On one path both figures are **intrinsic values**. By Jensen's inequality each is a lower
bound on the expected cost, and each is exactly zero whenever the path lands the account
above the strike:

| Point | Scenario | 투자수익률 | `av_ann_pp()` | `gmab_base_pp()` | `gmab_claim_pp()` |
|---|---|---|---|---|---|
| 1 | `base` | 2.50% | ₩43,883,943.57 | ₩36,000,000 | **₩0.00** |
| 4 | `low` | −1.00% | ₩25,958,820.39 | ₩36,000,000 | **₩10,041,179.61** |
| 5 | `high` | 3.75% | ₩52,811,343.37 | ₩36,000,000 | **₩0.00** |

The base run therefore collects ₩657,417.59 of GMAB charge against an intrinsic cost of
zero; model point 4 collects ₩603,909.13 against ₩929,653.88, and **the charge does not
cover the guarantee on the low path**. `run.py` prints both gaps and labels each what it is
— **a single-path residual, not a profit**. The statutory 보증준비금 is a CTE(70) over a
thousand scenarios, or a standard factor table, whichever is greater
[REG-R10] [REG-R26] [R1] [R12]; **this model publishes neither**, and nothing it prints is a
reserve. The standard factor exists precisely because a deterministic number is
meaningless.

`return_scenario.csv` carries a constant per fund and **no volatility, no correlation and
no time series**, because none was retrieved [R10] [S11]. That is the largest gap in the
model and it is structural rather than clerical: a guarantee's cost is a distributional
quantity and this run is a point on the distribution. Publishing the limit is the only
honest thing a single-path model can do with a written option, so it is published in
`run.py`, in the notes and here rather than left for a reader to infer.

## The 해약환급금 has no guarantee, and cannot have one

`cv_pp(t) = max(0, av_pp(t) - surr_chg_pp(t))`, the zero floor being statutory
[REG-R19 제7-66조제1항제1호](#krlib-reg-r19). On the representative scale it is **zero for the first three
months** and the `claims_lapse` column of `result_cf()` shows it: nil at `t = 0, 1, 2`, and
₩5,833.06 at `t = 3` on a `cv_pp(3)` of ₩234,582.77. That is not a modelling artefact —
[S6]'s own illustration shows a surrender value of zero at three months on an account of
₩821,751. Without the floor the model would book a *negative* surrender value of
−₩564,564.41 at `t = 0` as income.

변액보험 is also **barred** from the 무해지 / 저해지환급형 forms by 제7-66조제4항제1호
[REG-R19], so the cliff-shaped surrender curve that dominates this library's protection
products cannot appear here. The 해약공제액 is instead the unamortised 계약체결비용 [R2],
running off linearly **in the amount** over the 납입기간 capped at seven years, and it is
capped again by the **표준해약공제액** of 별표 14 [REG-R20]:

```
surr_chg_pp(t) = min(0.2305555556 x 12 x 기본보험료, surr_chg_cap_pp()) x (n - k) / n
surr_chg_cap_pp() = 5% x 12 x 기본보험료 x (1 - 8.67%) x min(납입기간, 12)
```

On the anchor cell that is ₩830,000.00 against a cap of ₩1,643,940.00 — 50.5% of it, which
is [S2]'s own position and reproduces the specification exactly. The cap **binds on three
shipped model points**, all 5년납: point 6 at ₩1,369,950 = ₩1,369,950, point 7 at ₩547,980
and point 10 at ₩2,739,900, where the level charge scaled from the anchor would otherwise
exceed it. `check_surr_chg_cap()` asserts it never does. Note 6 to 별표 14 further requires
the loaded acquisition cost to be discounted and netted off the cap; no retrieved document
works that netting, so the exact residual cap is **[unverified]** [REG-R21] and the model
applies the gross cap.

## The fund mix drifts, and the de-risking is not optional

Two funds — 채권형 and 주식형 — are the minimum that exercises a pro-rata allocation, a
per-fund 운용보수 and the mandatory bond floor at once; real menus run from 5 to 51 funds
[S4] [S5] [S10]. The three shipped allocation sets sit **on** the three rungs of the
mandatory 채권형 ladder rather than slack of it: 80% below twelve years of 연금개시 전
보험기간, 70% at exactly twelve, 50% above it [S1] [R1].

With no rebalancing the realised mix drifts, and on these scenarios it drifts **upwards**:
the 채권형 carries the lower 운용보수 on the same gross asset return, so the anchor's bond
weight runs 0.5000417 at `t = 0` to 0.5060743 at `t = 203`. Then the mandatory
pre-annuitisation de-risking bites — 「「연금지급개시일 − 3년」시점부터 매년 연계약해당일에
… 채권형 … 이 80% 미만인 경우 자동 조정됩니다」 [S1] — and at `t = 204` moves
₩12,113,087.24 into the bond fund, after which the weight holds at 0.80. This is **on** in
the base run, and `check_bond_floor()` asserts the weight meets the ladder at every month.
펀드자동재배분 and 펀드자동전환옵션 are off, because a single deterministic path cannot
distinguish either from a different fixed allocation.

## Modules that are off in the base run

`추가납입` and `중도인출` are switched off on the anchor so the account recursion is a clean
function of premium, charges and return, and both are retained as live terms because each
**leaks the guarantee**. Model point 8 turns 추가납입 on at 100% of the 기본보험료; model
point 9 turns 중도인출 on at 10% of the 해약환급금 once a year from the eleventh
계약해당일 (`t = 132`, the start of the twelfth policy year), and the proportional
re-basing [S2] [S7 제51조제8항] cuts its guarantee base from ₩48,000,000 to
₩25,509,168.00 by annuitisation against ₩23,847,432.46 of cumulative withdrawal. Without that adjustment a policyholder could withdraw the fund and keep the
strike, which [R1] names as the reason the rule exists:
「중도인출금은 최저보증한도에서 차감된다」.

The 미보증형 is model point 3 — `gmab_flag = 0` removes the guarantee and both charge
components together — because the GMAB has been elective since April 2016 [R2] [R1] and the
same chassis has to carry both forms. It is also the point that prices the guarantee to the
policyholder: the terminal account rises by ₩2,838,935.66, **6.47%**, and the annuity by the
same 6.47%, so twenty years of 0.25% a year of the fund plus seven years of 0.30% a year of
₩36,000,000 costs about one and a third years' annuity income.

One implementation limitation of the 추가납입 module, stated here rather than discovered
later: `gmab_prem_base_pp(t)` counts 추가납입 paid before month `t` with a closed form that
assumes the cumulative 200% cap has not yet bitten. On the shipped points it never does —
point 8 accumulates ₩36,000,000 against a cap of ₩72,000,000 — but raising
`addl_prem_ratio` past that point makes the charge base and the actual premium diverge.

**Documented in `product-spec.md` and deliberately not implemented**: 펀드자동재배분,
펀드자동전환옵션, 조기연금개시, 일반계정 전환, 보험계약대출, 감액, 보험료 납입
일시중지/중지/종료, 성과·장기유지 보너스, the roll-up / step-up / ratchet GMAB bases, the
CPPI-funded monthly-ratchet guarantee that carries **no** guarantee charge [S6], the
elective switchable GMAB [S9], and the 실적배당 종신연금 (GLWB) in which the money stays in
the separate account through the payout phase [S2] [S7] [S8] [S10]. Every one of them is a
first-order lever on guarantee cost, and none of them can be exercised meaningfully on one
deterministic path.

## Inputs are external files

Eight CSVs in this directory — `model_point_table.csv`, `mort_table.csv`,
`lapse_table.csv`, `fund_table.csv`, `charge_table.csv`, `risk_prem_table.csv`,
`return_scenario.csv`, `crediting_table.csv` — read by the model at run time rather than
stored inside it. The model folder holds `__init__.py` and `_system.json` and its two Space
folders, and nothing else: no `_data/`, no IOSpec, no embedded values, so a diff of the
model shows logic changes only and a table can be swapped without touching a formula. This
is the `annuallife/TradLife_A` layout; contrast `basiclife/BasicTerm_S`, which keeps its
inputs inside the model.

The consequence worth knowing is that **the model is not portable on its own**: copying the
`VA_KR_S` folder without its parent's CSVs produces a model that reads and then fails on
first evaluation.

### Read once, in `Data`

`Data` is unparameterized and holds `input_dir()`, the eight `*_file` filename References
and one `pd.read_csv` reader per file. `Projection` is parameterized by `point_id`, so each
`Projection[N]` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. `input_dir()` returns `_model.path.parent`,
resolved at run time, so the model works wherever the repository is checked out.

Three tables carry a compound key — `mort_table` by `(sex, age)`, `fund_table` by
`(fund_set, fund_id)`, `return_scenario` by `(scenario_id, fund_id)` — and three are read
**without** an index, because the lookup is a band test on a half-open interval rather than
a key lookup: `lapse_table` on completed policy years, `risk_prem_table` on attained
보험나이, `crediting_table` on completed years since annuitisation.

`charge_table` deserves its own sentence. It is the 상품요약서's own **수수료 안내표**, one
row per charge line, and it is a table rather than a block of scalar References because the
five lines this product turns on — 계약체결비용, 계약관리비용, 위험보험료, 최저보증비용 and
특별계정 운용보수 — are deducted **from different bases at different times and land in
different accounts**. Its `base`, `timing` and `account` columns carry that beside each rate,
so a reader can see the shape of the stack without reading a formula.

Every file but `model_point_table.csv` carries a `provenance` column and every cell in it
begins with a citation tag. That is the library's rule and here it is load-bearing: **no
row of `mort_table.csv` is a transcription**, and neither is any row of
`return_scenario.csv`. A model point is a configuration rather than an assumption, which is
why the one file exempt from the rule is exempt.

### `mort_table.csv` is a construction on two published numbers

Two bases on one file. `ann_mort_rate` is the 연금사망률 (연금생명표) proxy: a Makeham
`mu(x) = A + B c^(x-65)` with `A = 0.0002` and `c = 1.10` **[std]**, with `B` solved so the
complete expectation of life at 65 is **exactly** the 제10회 경험생명표 65세 기대여명 of
23.7 years male and 27.1 female [REG-R33] — `B = 0.007040013548` (M) and `0.004803209921`
(F). `mort_rate` is the 보험사망률 basis, the same curve at `mu / 0.80` **[std]**, Korea
pricing annuities on a separate and lighter table. Terminal age 120, at which `q = 1` by
construction.

The cross-check against the public series is coherent rather than fitted: the construction
implies an insured `e(40)` of 46.5 (M) and 50.4 (F) on the annuity basis, against 41.9 and
47.4 for the whole population [REG-R38] — gaps of 4.6 and 3.0 years, beside the 4.2 and
3.4 years the two published 65세 기대여명 figures imply. **The 경험생명표 qx table is not
published** [REG-R34] and this file must never be presented as it; the 참조순보험요율
display that publishes Korean morbidity does not reach the life side [REG-R61]. The named
to-do is to fetch the 완전생명표 single-year qx from KOSIS and record the table id
[REG-R39].

The table drives more of the answer than its two lines suggest. It sets the GMDB cost
through the deferral and the **entire** payout liability afterwards: `annuity_factor()` is
20.139842488678187 for the male anchor and 21.762174205458386 for the female of model point
2, so the same ₩43,883,943.57 buys **7.45% less annual income**. Substituting a filed basis
is a CSV replacement and nothing else.

### `lapse_table.csv` is calibrated to one second-hand sentence

The scale runs 28% / 22% / 17% / 14% / 12% / 10% / 9% and 8% ultimate from the eighth policy
year, giving a lapse-only **seven-year persistency of 0.28891508** — against the only
published Korean figure for this product, 「변액보험의 7년 평균 유지율은 30% 미만으로
알려져 있다」, itself second-hand inside [R1] and reported from a 2016 금융감독원 release
that was not retrieved. The **level** is that calibration; the **shape** by duration is
**[std]**, a monotone run-down whose ultimate starts where the 해약공제 has run off and
[R1]'s seven-to-ten-year break-even window opens. **No Korean carrier publishes a 변액연금
적용해지율** [S12].

Lapse here is **static and exogenous, and it is neither in reality**. [R1] states the market
and reserving convention plainly — 동적해지율, lapse varying with the guarantee's
in-the-moneyness — but publishes **no functional form and no parameter**, so any dynamic
formula here would be a [std] construction dressed as a cited one and the base run does not
attempt one. The bias runs one way and is worth naming: on precisely the paths where the
guarantee matters, the model lets contracts leave that would stay, so **guarantee cost is
understated**. Every policyholder option on this contract points the same way —
조기연금개시 is available only where the guarantee is out of the money [S1] [S9] [S10], and
일반계정 전환 is offered at 130% of premiums paid [R1] — and a deterministic run can
exercise none of them.

### `return_scenario.csv` — every return assumption is `[std]`

One annual **gross** separate-account asset return per fund, held constant for the whole
projection. Gross, so that the 특별계정 운용보수 is a modelled cash flow rather than an
assumption folded into a net rate. The base run sets the blended 투자수익률 to the **2026
평균공시이율 of 2.50%** [REG-R48] — the middle of the three returns a Korean variable
illustration must show [R2] — and works back to a gross 3.00% at the 50/50 anchor
allocation. `low` and `high` are the other two mandated returns, −1.00% and
2.50% × 1.5 = 3.75%, grossed up the same way.

The only realised Korean returns retrieved are the top of a cross-sectional distribution in
a trade article [R10] and one live fund panel at a 기준가격 of 904.24원 against the
statutory 1,000.00 opening price after fourteen years [S11] — a fund below its launch value
after fourteen years, which is worth keeping in view beside a 2.50% assumption. Neither is a
basis for a return assumption and neither is used as one.

### The other four tables

- **`charge_table.csv`** is the most sourced file in the model. 계약체결비용 5.17%,
  계약관리비용 3.50% in payment and 1.33% after, 위험보험료, the 해약공제 anchor of ₩830,000
  and the fund charges are [S2]; both guarantee charges — 0.07% GMDB, 0.25% + 0.30% GMAB —
  are [S1]; the 연금수령기간 중 계약관리비용 of 0.5% is [S4]; the five-year commission scale
  1.34 / 0.41 / 0.28 / 0.25 / 0.11% of 보험료총액 is [R1 <표 Ⅴ-3>](#krlib-variable_annuity-r1). Three rows are **[std]**:
  `other_charge` and `fund_expense` at zero, and the insurer's own `expense_acq` and
  `expense_maint`. The 표준해약공제액 cap row is [REG-R20].
- **`fund_table.csv`** — the per-fund 운용보수 0.40% and 0.60% are [S2], inside the
  0.20%–0.89% observed across five documents [S1] [S2] [S4] [S5] [S9]; the three allocation
  sets are **[std]**, set on the mandatory 채권형 rungs [S1] [R1].
- **`risk_prem_table.csv`** — the level is [S2]'s published 0.004%–0.011% band; the grading
  across it by attained 보험나이 is **[std]**.
- **`crediting_table.csv`** — the 공시이율 of 2.50% is the 2026 평균공시이율 [REG-R48]
  adopted as the declared rate **[std]**, held level though the contract moves it monthly
  off the 공시기준이율 [REG-R18] [REG-R24]; the 최저보증이율 ladder 1.00 / 0.75 / 0.50% is
  [S1]. The `min_guar` basis is a **[std]** diagnostic on which the declared rate is nil, so
  that `Max[공시이율, 최저보증이율]` resolves to the floor and model point 10 exercises the
  ladder — `credit_rate` 0.0100, 0.0075, 0.0050 at 0, 5 and 10 completed years.

### No input column is the frame's `t`

Under the 0-based convention a CSV column that carries the model's time index would be
keyed 0-based. **None of the eight files has one**, so no input values moved when the
index convention was settled:

- **`lapse_table.csv` `dur_from`** — a contractual **policy year**, 1-based (1 … 8), read
  by `lapse_rate(t)` as a band test against `policy_year(t)` = `t // 12 + 1`. Left alone;
  the reader does the mapping.
- **`crediting_table.csv` `dur_from`** — **completed years since 연금개시**, an elapsed
  count and already 0-based (0 / 5 / 10), read by `decl_rate(k)` and `min_guar_rate(k)` on
  the payout clock `k`, not on `t`. Left alone.
- **`charge_table.csv` `line`** — the rows `comm_yr1` … `comm_yr5` are **policy-year
  labels** inside the line name, read by `comm_rate(y)` with `y = policy_year(t)`. Left
  alone.
- **`model_point_table.csv` `wd_start_year`** — the number of **completed policy years**
  after which the 중도인출 module starts (11 on model point 9; 0 = off), an elapsed count
  and so already 0-based. Read by `wd_pp(t)` as `t < 12 * wd_start_year()`, i.e. the first
  withdrawal falls on the eleventh 계약해당일, `t = 132`, the start of the twelfth policy
  year. Left alone: it is not a point on the frame's axis and not a 1-based policy-year
  label.
- **`mort_table.csv` `age`** and **`risk_prem_table.csv` `age_from`** — attained
  **보험나이**, not time. Read with `age(t)` = `age_at_entry() + t // 12`. Left alone.
- **`fund_table.csv`** and **`return_scenario.csv`** have no time dimension at all.

## Sign convention

`net_cf` is **income positive**: income less outgo, the library-wide orientation, and it is
natively so — the technical notes print the stream the way the model produces it, so there
is no `liability_cf` companion on this product. `net_cf(0)` is **negative** on the anchor
cell (−₩43,227.86) because the insurer's own acquisition expense and the first year's
commission together exceed the first month's premium.

There is no `claims` **column** in `result_cf()`. The four `claims_*` split lines are
published instead, so the columns sum to `net_cf` without a reader having to know which to
skip; an aggregate beside the splits would double-count the whole benefit outgo. The
`claims(t, kind)` cells stays and takes `DEATH`, `LAPSE`, `ANNUITY`, `MATURITY`.

Investment return is **not** a liability cash flow. `inv_income_pp` and `mgmt_fee_pp` drive
the account value and are published in `result_av()` and `result_charges()`, but neither is
a column of `result_cf()`: this library projects gross liability cash flows and leaves the
asset side, the discounting and every reserve to a layer that consumes them.

`pols_if(t)` is the count in force at the **start** of month `t` and is the weight carried
by every cash flow on that row. It is a genuine policy count on both sides of
annuitisation — contracts before `t_ann()`, living annuitants after it. The count an
annuity instalment is actually owed to is `pols_annuity_oblig(t)`, which is *every* contract
that annuitised while the 10-year 보증기간 runs, alive or not [S2] [S5], and the survivors
only afterwards. The step down at the end of the 보증기간 is real, is visible in
`result_pols()`, and is the whole of the guarantee's value showing up at once: the
instalment falls from ₩200,728.58 to ₩186,188.58 at `t = 360`, a 7.24% step, with
`annuity_net_pp()` unchanged at ₩2,168,066.80.

## Naming

lifelib's vocabulary throughout: `pols_*` for counts, plural nouns for cash flows, `*_rate`
for rates, `*_pp` for per-contract amounts, `claims(t, kind)` with an uppercase `kind`, and
`pols_if_at(t, timing)`, `av_pp_at(t, timing)`, `fund_pp_at(t, j, timing)` for the
within-month reads. `lapse_rate` is the **annual** rate and `lapse_rate_mth` the monthly
one, matching `mort_rate` / `mort_rate_mth`. The mandatory names — `model_point`,
`proj_len`, `age`, `pols_if`, `mort_rate`, `claims`, `expenses`, `net_cf`, `result_cf` —
are all present and mean what they mean everywhere else in the repository.

### The notes' symbols, and where they live

`Projection.doc` carries the full 95-row mapping from the technical notes' symbols to the
cells names, which is the most useful thing in the file for a reader holding the notes
beside the model. The rows that matter most:

| Notes | Cells | Notes | Cells |
|---|---|---|---|
| `T` | `t_ann()` | `D(t)` | `mth_deduct_pp(t)` |
| `P_sa(t)` | `prem_to_av_pp(t)` | `c_p` | `gmab_charge_prem_pp(t)` |
| `AV(t)` | `av_pp(t)` | `c_a` | `gmab_charge_asset_pp(t)` |
| `K(T)` | `gmab_base_pp()` | `c_d` | `gmdb_charge_pp(t)` |
| `K_d(t)` | `prem_paid_pp(t)` | `C`, `C_max` | `surr_chg_pp(t)`, `surr_chg_cap_pp()` |
| `CF_g`, `CF_s` | `net_cf_gen(t)`, `net_cf_sep(t)` | `M(t)` | `mgmt_fee_pp(t)` |

### Names this product argued for, and against

Three came out of `krlib`'s cross-model naming review.

- **`surr_chg_pp` and `surr_chg_cap_pp`**, not `surr_charge_pp` / `surr_charge_max_pp`.
  The 해약공제액 and its 별표 14 ceiling are the same quantity capped, and the pair reads as
  a pair. `surr_charges(t)` — plural, no `_pp` — is the *transfer* of the retained amount to
  the 일반계정, which is a different thing on a different account, and the plural/`_pp`
  distinction is what keeps them apart.
- **`decl_rate` for the 공시이율**, the same name `delib` uses for the declared laufende
  Verzinsung. Romanizing it to `gongsi_iyul` would have been the only romanized cells name
  in the library, and the concept is not Korea-specific even though its regulation is.
- **`prem_int_rate` was argued for and rejected**, because this product does not have a
  예정이율 at all: a variable annuity's accumulation account *is* the fund, and a full-text
  search of the 감독규정 returns zero occurrences of 예정이율, which speaks only of the
  계약자적립액 적용이율 [REG-R9] [REG-R48]. Carrying the name with a null value would have
  implied a pricing rate the contract does not have. `annuity_int_rate()` is the payout-phase
  crediting rate and is a different quantity.

Beyond those: `gmab_*` and `gmdb_*` are used untranslated because GMAB and GMDB are the
terms [R1] itself uses in its English abstract, and `av_pp` for 계약자적립액 rather than
`account_value_pp`, matching `savings/CashValue_SE`.

## Standardizations used

Every row is **[std]**. The sourced contractual parameters are in
[`product-spec.md`](product-spec.md) and [`technical-notes.md`](technical-notes.md) and are
not repeated. "Observed range" is what the retrieved documents actually bound, and several
of them bound nothing at all — which is said rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| projection grid | monthly | the 계약자적립액 is contractually a **daily** 좌수 × 기준가격 ledger quoted per 1,000좌 [S7 제43조]; months are the coarsest grid on which the 월공제액 is a distinct event | none; 감독규정 제7-65조제2항 permits an annualized-premium basis instead [REG-R18] and the model uses neither |
| pricing lag | none | the two-business-day lag on every 펀드변경, 중도인출 and 해지 [S5] [S7 제39조] [S7 제50조제2항] falls inside a month and is dropped with it | two business days, universal across the retrieved set |
| 운용보수 timing | rate / 12 monthly | contractually rate / 365 daily inside the 기준가격 [S7 제43조제2호]; taken monthly with the rest of the stack | none; the discretization gain is small and one-directional on a rising path |
| `omega_age` | 120 | a 종신연금형 has no maturity, so the horizon is the mortality table's terminal age | none published; the 제10회 경험생명표 terminal age is not disclosed [REG-R34] |
| mortality construction | Makeham `A + B c^(x-65)`, `A = 0.0002`, `c = 1.10`, `B` = 0.007040013548 (M) / 0.004803209921 (F), solved to the published 기대여명 | the 제10회 경험생명표 is not published [REG-R33] [REG-R34] and the 참조순보험요율 display does not reach the life side [REG-R61] | check: implied `e(40)` 46.4 M / 50.3 F against the population 41.9 / 47.4 [REG-R38]; single-year qx not fetchable [REG-R39] |
| 보험사망률 loading | `mu / 0.80` | Korea prices annuities on a separate and lighter table; the 25% loading on the force is the standardization, not the two-table structure | none published for either basis |
| lapse shape | 28/22/17/14/12/10/9/8% | monotone run-down to an ultimate starting where the 해약공제 runs off; the **level** is calibrated to a 7-year persistency below 30% [R1] | nothing published: no Korean carrier discloses a 변액연금 적용해지율 [S12] |
| lapse dynamics | none | [R1] states the 동적해지율 convention and publishes no functional form and no parameter | none; the bias is one-way — guarantee cost understated |
| monthly rate conversion | `1 − (1 − w)^(1/12)`, applied to survivors of the month's deaths | uniform force within the year, the library-wide convention | none needed |
| decrement order | death, then 해지 | a surrender is an act of a living policyholder | fixed by the contract's own sequence |
| gross return | constant per fund; blended 2.50% / −1.00% / 3.75% | the three returns a Korean illustration must show [R2] at the 2026 평균공시이율 [REG-R48], grossed up for the 운용보수 | **no realised series retrieved**: one trade-article cross-section [R10] and one fund panel at 904.24원 after 14 years [S11] |
| volatility, correlation | **none** | a constant path cannot carry either | none retrieved; this is the model's largest gap and it is structural |
| fund menu | two funds, 채권형 / 주식형 | the minimum that exercises a pro-rata allocation, a per-fund 운용보수 and the bond floor at once | 5 to 51 funds across the retrieved set [S4] [S5] [S10] |
| allocations | 80/20, 70/30, 50/50 | set **on** the three rungs of the mandatory 채권형 ladder rather than slack of it [S1] [R1] | the ladder itself is contractual, the choice to sit on it is not |
| `other_charge` | 0.00% | 기타비용 is named by [R2]'s identity and confirmed deducted at premium payment [S7 제2조], but **no retrieved 상품요약서 quantifies it**; zero makes the allocation reproduce the observed 91.33% exactly | none published; the line is kept because the identity needs it |
| `fund_expense` | 0.00% | 증권거래비용 and 기초펀드 보수 are ex-post estimates of actual spend, not contractual rates [S2], so the modelled charges stay contractual | 0.00–0.79% and 0.01–0.45% [S2] [S4]; the omission understates the drag by up to about 0.5 points a year |
| 위험보험료 age scale | 0.0040% at 15 rising to 0.0110% at 60+ | the **level** is [S2]'s published 0.004%–0.011% band; the grading across it is the standardization | the band is published; the scale is not |
| 고도재해장해급여금 | charged for, never paid | no 장해 incidence rate on this contract's basis was retrieved: the 참조순보험요율 display is a 장기손해보험 one and does not reach the life side, and its 상해 후유장해 grids were not extracted [REG-R34] [REG-R61] | none; the bias favours the insurer, is small, and is stated |
| `acq_charge_years` | `min(10, 납입기간)` | [S2] prints ten years on its own 10년납 contract, where the two coincide; a charge on a premium cannot outlive the premium | ten years across the retrieved set; [S4] prints 6.12% for ten years then zero |
| 해약공제 composite | ₩830,000 anchor, run off linearly **in the amount** | the surrender charge **is** the unamortised 계약체결비용 [R2], so it must come from the same carrier as the 5.17% | ₩830,000 [S2], ₩1,077,000 [S5], ₩1,180,000 [S4] on the same cell — a 42% spread; the market-mean scale [R1 <표 Ⅴ-2>](#krlib-variable_annuity-r1) would raise `surr_charges` about 30% |
| 월공제액 cap | capped at the available account value | a deduction cannot make the account negative; no retrieved document states the rule | none published |
| guarantee-charge timing | struck on `av_pp_at(t, "BEF_DEDUCT")` | after the premium, before the growth, so a rising month raises next month's charge and not this month's | fixed by the 월계약해당일 ordering [S7 제2조]; the within-month position is the standardization |
| annuity frequency | annual, in advance | the granularity the 연금 연액 and the 0.5% payout charge are published on [S4] | monthly and annual both offered across the set |
| annuity level | held level after it starts | the contract moves it with the 공시이율 [S5]; holding it level is exact only if the rate never moves | none; the 공시기준이율 formula is carrier-parameterized [REG-R24] |
| 연금생명표 at annuitisation | not re-struck | the contract permits a re-strike in the policyholder's favour [S1] [S2] [S5]; not modelling it favours neither side systematically | none published |
| 연금수령기간 중 계약관리비용 | 0.5% of the 연금 연액, netted off | [S4]'s proportional form taken over [S2]'s per-구좌 monthly form because it is scale-free | [S2]: min(영업보험료 3.5%, ₩4,000) per 구좌 per month |
| `expense_acq`, `expense_maint` | ₩300,000 at issue, ₩3,000 a month, no inflation | **no Korean carrier publishes a unit cost**: the 사업비 disclosure is of *charges*, not of costs [R2] [S12] | none published at all; they total ₩598,836.73, 3.9% of premiums received |
| commission channel | 전속설계사 scale of [R1 <표 Ⅴ-3>](#krlib-variable_annuity-r1) | the census's own average; bancassurance and online acquisition costs were capped at 50% of it from 2016 and the one online 변액연금 [R1] found paid none | 0.63–2.38% in year 1 and 1.10–3.13% in total across the 2017 census |
| the account recursion | consistent with, not derived from, the retrieved documents | its exact form sits in the **산출방법서**, a filed 기초서류 that is not public [REG-R18 제7-64조](#krlib-reg-r18) [REG-R2] | none; the same limit applies to the surrender value and the annuity conversion |
| `roll_fwd_tol`, `val_tol` | 1e-10, 1e-8 | one closes identities between counts of order 1; the other closes money identities relative to gross flows of order 1e7 at annuitisation | both far below one won |

Two of these are worth reading twice, because they are the ones a reviewer should attack
first. **The return path is the whole answer** — it moves the terminal account by a factor
of two across the three mandated illustrations and it is the only thing that decides whether
the GMAB pays at all — and it is [std] end to end with no distribution behind it. **The
insurer's own expense is unsourced in its entirety**, and it is the only line in the
statement with no document behind it of any kind.

## Tests

`tests/test_variable_annuity_kr.py` asserts the notes' worked example **hard-coded**, so a
reviewer can check it by eye rather than by re-running the model:

- The month-0 charge stack to the last float digit — `acq_charge_pp(0) = 15,510.0`,
  `maint_charge_in_pp(0) = 10,500.0`, `other_charge_pp(0) = 0.0`,
  `prem_to_av_pp(0) = 273,990.0`, `risk_prem_pp(0) = 24.000000000000004`,
  `gmdb_charge_pp(0) = 15.98275`, `gmab_charge_asset_pp(0) = 57.081250000000004`,
  `gmab_charge_prem_pp(0) = 9,000.0`, `mth_deduct_pp(0) = 9,097.063999999998`,
  `mgmt_fee_pp(0) = 110.64426393373063` — and `prem_alloc_ratio(0) = 0.9133` exactly,
  against the three carriers who publish it [S1] [S2] [S6].
- The `t = 0 … 12` cash flow statement to the won, and the four columns that are `0.00` in
  **every** row — `claims_annuity`, `claims_maturity`, `withdrawals`, `fund_expenses` —
  asserted as zeros rather than left implied.
- The nine values of `surr_chg_pp(12k)` for `k = 0 … 8`, from ₩830,000.0001599999 down to
  0.0 at `k = 7`, against the cap of ₩1,643,940.00 — the run-off being linear **in the
  amount**, which is the pitfall the row-by-row assertion exists to catch.
- The undiscounted totals: ₩15,215,257.48 of premium, ₩11,077,101.66 of surrender value,
  ₩5,759,786.33 of annuity, ₩310,883.37 of death claims and **−₩3,148,714.71** of net cash
  flow, with `Σ pols_if = 99.6122423885`.
- The two guarantees at `t_ann() = 240`: `av_ann_pp() = 43,883,943.57329801`,
  `gmab_base_pp() = 36,000,000.0`, `gmab_claim_pp() = 0.0`,
  `annuity_factor() = 20.139842488678187`, `annuity_net_pp() = 2,168,066.7999254693`,
  `pols_annuitised() = 0.09258412964405735`, and `claims_annuity(240) = 200,728.5776812762`.

Each of the notes' twelve pitfalls earns a test named after it:

1. `gmab_charge_asset_pp(0)` and `gmab_charge_prem_pp(0)` differ by a factor of 158 — the
   two components are on two bases and must not be collapsed.
2. `gmab_charge_prem_pp(83) == 9000.0` and `gmab_charge_prem_pp(84) == 0.0` — the charge
   runs for the *shorter* of the 납입기간 and seven years.
3. `mth_deduct_pp(120) > mth_deduct_pp(119)`, with `maint_charge_after_pp(119) == 0.0` and
   `maint_charge_after_pp(120) == 3990.0` — the deduction steps **up** at 납입완료.
4. `check_prem_alloc()` and `prem_alloc_ratio(0) == 0.9133` — the front-end charges never
   reach the 특별계정.
5. `check_charge_split()` on every point and `mgmt_fee_pp(0) == 110.64426393373063` — the
   운용보수 is a factor on the growth, not a unit cancellation.
6. `pols_annuitised() == 0.09258412964405735` and `gmab_claims(t) == 0.0` for every
   `t != t_ann()` — the GMAB is a European option on one date, not a floor at every
   duration.
7. On point 1 `gmab_claim_pp() == 0.0`; on point 4 `gmab_claim_pp() == 10041179.61262558`
   with ₩929,653.88 of cost against ₩603,909.13 of charge — the residual is a path, not a
   profit.
8. `check_gmdb_floor()` and `claims_death(0) == 27.860533600121418` — the death benefit
   splits exactly into the account value released and the 보증준비금 top-up.
9. `cv_pp(2) == 0.0` and `cv_pp(3) == 234582.76753756206` — the statutory zero floor
   [REG-R19 제7-66조제1항제1호](#krlib-reg-r19).
10. The surrender-charge scale above, asserting run-off in the amount and not the ratio.
11. `check_surr_chg_cap()` on all ten points, with `surr_chg_pp(0) == surr_chg_cap_pp()` on
    points 6, 7 and 10 — the 별표 14 cap binds exactly there and is invisible on the anchor.
12. `pols_annuity_oblig(348) == pols_annuitised()` and
    `pols_annuity_oblig(360) == pols_if(360)`, with the instalment stepping from
    ₩200,728.58 to ₩186,188.58 — the 보증기간 weight is not `pols_if`.

Beyond the pitfalls the module asserts the boundary and the shape: `net_cf_sep(240)` =
−4,062,956.72108272 and `net_cf_gen(240)` = +3,861,950.3910125117 summing to
`net_cf(240)`; `bond_weight(203) == 0.5060742578243943` against `bond_weight(204) ==
0.8000266764480309` with `derisk_amount_pp(204) == 12113087.239005797`; the other nine model
points' `proj_len`, `av_ann_pp`, `gmab_claim_pp` and totals as the notes tabulate them,
including model point 3's ₩2,838,935.66 guarantee-free uplift, model point 8's
₩72,000,000 strike, model point 9's re-based ₩25,509,168.00 and model point 10's
`credit_rate` ladder of 0.0100 / 0.0075 / 0.0050. The optional modules are asserted in
**both** positions of their switch, and reading the anchor at 만나이 instead of 보험나이 is
asserted to move the answer, so the age basis cannot silently drift.

`tests/test_model_conventions_kr.py` adds the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout, the external inputs
with no orphan CSV, the `provenance` column on every assumption CSV, the docstrings and
their required phrases, the `result_cf()` contract — indexed by `t`, first column `pols_if`,
a `net_cf` column, all names `lower_snake_case`, no NaN, length equal to `proj_len()` — and
that every `check_*()` returns `True` on **every** shipped model point.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-variable_annuity-r1
[R10]: #krlib-variable_annuity-r10
[R12]: #krlib-variable_annuity-r12
[R2]: #krlib-variable_annuity-r2
[R4]: #krlib-variable_annuity-r4
[REG-R10]: #krlib-reg-r10
[REG-R15]: #krlib-reg-r15
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R24]: #krlib-reg-r24
[REG-R26]: #krlib-reg-r26
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R48]: #krlib-reg-r48
[REG-R6]: #krlib-reg-r6
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
