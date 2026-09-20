# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes derive the standardized composite Korean deferred variable
annuity — 변액연금보험 (*byeonaek yeongeum boheom*) — specified in `product-spec.md` in
this directory into the arithmetic of the reference model **`VA_KR_S`**. Where the two
disagree the specification governs and this document is wrong. The composite describes no
single insurer's contract; it is built on one carrier's 상품요약서 for the expense stack,
the surrender-charge scale and the fund charges [S2] and on a second carrier's 상품안내장
for the guarantee design and both guarantee charges [S1], and the reason those two may be
joined and others may not is argued once in `product-spec.md` and not repeated here.

[S#] tags refer to primary product documents — 약관 (*yakgwan*, policy conditions),
상품요약서 (*sangpum yoyakseo*, the statutory product summary), 상품안내장 and 상품설명서 —
and [R#] to product-specific regulatory and actuarial references; both resolve in
`sources.md` in this directory, whose numbering is carried verbatim from
`_research/variable-annuity.md` and is never renumbered. [REG-R#] resolves against the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
own R1–R62 numbering is distinct from this product's. **[std]** marks a standardization
introduced for the reference implementation; every one of them is also tagged in
`product-spec.md` and carries a rationale in the `provenance` column of the CSV it lives
in. [unverified] marks a claim the research pass could not confirm against a retrieved
document. **Every parameter value below is the value in `product-spec.md` and the value
in the shipped CSVs.**

`VA_KR_S` runs on a **monthly** grid with every age in **보험나이** (*boheom nai*,
insurance age). It is the library's only 특별계정 (*teukbyeol gyejeong*, separate account)
product and the only one whose cash flows cross an account boundary, so **every flow below
is labelled with the account it falls in**, and the identity that the two account ledgers
add back to the whole-contract cash flow is asserted by the model rather than argued in
prose. Amounts are in Korean won; because Korean documents quote in 만원 (10,000) and 억원
(100,000,000), both forms are given where a Korean reader would expect one —
₩36,000,000 (3,600만원).

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows for one contract: 영업보험료 received,
  사망보험금 (death benefit), 해약환급금 (*haeyak hwanreupgeum*, surrender value), 연금
  (annuity instalments), 중도인출금 (*jungdo inchulgeum*, partial withdrawals), the
  third-party costs borne by separate-account assets, and the insurer's own expenses and
  commission. The 책임준비금, the 보증준비금 (*bojeung junbigeum*, guarantee reserve), the
  해약환급금준비금, the IFRS 17 CSM and the K-ICS 요구자본 are **not** computed; see
  *Valuation and reserve pointers*.
- **Two periods, one projection.** 연금개시 전 보험기간 (the deferral) runs
  「계약일부터 연금개시나이 계약해당일의 전일까지」 and the 연금개시 후 보험기간 (the
  payout) from there for life [S1] [S7 제2조]. `t_ann()` is the boundary month. The
  특별계정 exists strictly for `t < t_ann()` and is empty afterwards, the whole
  계약자적립액 (*gyeyakja jeongnibaek*, account value) having moved to the 일반계정 (general
  account) 「연금개시시점부터 계약자적립액 모두에 대하여 특별계정에서 일반계정으로
  자동전환하여 공시이율로 운용합니다」 [S6].
- **Projection frequency: monthly**, 0-based. `t = 0` is the month containing the 계약일 and
  the first 기본보험료; row `t` of `result_cf()` carries month `t`. `proj_len()` is the
  **number of projected months and not the last row index**: the frame is
  `t = 0 … proj_len() − 1`, so the anchor cell has `proj_len()` = 960 rows, 0 … 959.
  Policy year is the contractual 1-based label derived from `t`: `policy_year(t)` =
  ⌊t/12⌋ + 1, so the first policy year is `t = 0 … 11`.
- **The monthly grid is itself a [std] standardization, and a consequential one.** The
  계약자적립액 is contractually a **daily** 좌수 (*jwasu*, unit count) × 기준가격
  (*gijun gagyeok*, unit price) ledger quoted per 1,000좌 [S7 제43조], valued every business
  day [S7 제37조] [S7 제42조]. Collapsing it onto months also collapses the **two-business-day
  pricing lag** that applies to every 펀드변경, 중도인출 and 해지 [S5] [S7 제39조]
  [S7 제50조제2항]. 감독규정 제7-65조제2항 expressly permits an annualized-premium basis for
  the 계약자적립액 instead [REG-R18]; the model does not use that permission and states the
  discretization it does use.
- **The account recursion itself is [std].** Its exact form sits in the **산출방법서**
  (*sanchul bangbeopseo*), a filed 기초서류 that is not public [REG-R18 제7-64조](#krlib-reg-r18). The
  recursion in `av_pp` is **consistent with, and not derived from,** the retrieved
  documents, and the same limit applies to the surrender value and to the annuity
  conversion. It is the hard boundary on how far a public-source reconstruction of a
  Korean variable annuity can go, and it is stated here rather than buried in a footnote.
- **Age basis: 보험나이 throughout.** 만나이 (age last birthday) at the 계약일 with a
  remainder of six months or more rounded up and less than six months discarded,
  incrementing on the **policy anniversary** and not on the birthday
  [REG-R25 제21조](#krlib-reg-r25). The research file records no 보험나이 article read from
  the retrieved 약관, so no [S#] pinpoint is claimed for it. It is the contractual age, the
  index of every Korean rate card, and the basis both shipped mortality tables are
  graduated on, so no shift is applied anywhere. The one place Korean practice uses 만나이
  instead is the 가입나이 envelope, 만15세–70세 [S1] [S2], which is an issue rule and not a
  projection quantity.
- **Model points and rounding.** Single-contract model points on an expected
  (probability-weighted) basis with `pols_if_init = 1.0`, so every `*_pp` cells is per
  contract and every `result_cf()` column is that quantity weighted by the in-force count
  on the same row. No intermediate rounding anywhere; displayed figures are rounded
  independently for display.
- **Sign convention: `net_cf` is income-positive**, income less outgo, and it is natively
  so — there is no `liability_cf` companion on this product and the worked example prints
  the stream the way the model produces it. `net_cf(0)` is **negative** on the anchor cell,
  because the insurer's own acquisition expense and the first year's commission together
  exceed the first month's premium.
- **Investment return is not a liability cash flow.** The gross separate-account return and
  the 특별계정 운용보수 (*unyong bosu*, management fee) drive the account value and are
  published as `inv_income_pp` and `mgmt_fee_pp`, but neither is a column of `result_cf()`.
  This library projects gross liability cash flows and leaves the asset side, discounting
  and every reserve to a layer that consumes them.
- **What the model computes and what it does not.** It computes the 계약자적립액 and the
  해약환급금, both contractual quantities [REG-R18] [REG-R19] [REG-R20]; it computes the
  **intrinsic value** of both guarantees on one path and publishes it as such. **It is a
  mechanics demonstration, not a pricing or reserving result**, and on this product that
  sentence carries more weight than anywhere else in `krlib`, because the two things it is
  asked to value are options.

---

## Model point attributes

Every column of `model_point_table.csv`, with the cells that reads it. The anchor cell is
model point **1**, the illustration point three independent carriers publish
[S1] [S2] [S6].

| Column | Cells | Type | Anchor value | Note |
|---|---|---|---|---|
| `policy_id` | `policy_id()` | str | `VA-000001` | label only |
| `sex` | `sex()` | enum {M, F} | M | selects the mortality column |
| `age_at_entry` | `age_at_entry()` | int, **보험나이** | 40 | 가입나이 envelope 만15–70 [S1] [S2] |
| `basic_prem_pp` | `basic_prem_pp()` | KRW/month | 300,000 | 기본보험료, level, in advance |
| `pay_term` | `pay_term()` | years | 10 | 납입기간; `pay_months()` = 120 |
| `annuity_age` | `annuity_age()` | int, **보험나이** | 60 | 연금개시나이, band 45–80 [S1] [S2] |
| `gmab` | `gmab_flag()` | 0/1 | 1 | 1 보증형, 0 미보증형 [S4] [S5] |
| `fund_set` | `fund_set()` | key of `fund_table` | `bond50_eq50` | 채권형 50% / 주식형 50% |
| `scenario_id` | `scenario_id()` | key of `return_scenario` | `base` | 투자수익률 2.50% |
| `crediting_basis` | `crediting_basis()` | key of `crediting_table` | `decl_2026` | payout-phase rate ladder |
| `addl_prem_ratio` | `addl_prem_ratio()` | ratio of 기본보험료 | 0.0 | 추가납입 module, off |
| `wd_ratio` | `wd_ratio()` | ratio of 해약환급금 | 0.0 | 중도인출 module, off |
| `wd_start_year` | `wd_start_year()` | completed policy years | 0 | 계약해당일 of the first 중도인출 |
| `pols_if_init` | `pols_if_init()` | count | 1.0 | contracts at issue |

Derived on the anchor: `prem_ann_pp()` = ₩3,600,000, `prem_total_pp()` = **₩36,000,000
(3,600만원)**, `t_ann()` = **240**, `defer_years()` = 20, `bond_floor()` = **0.50** (the
>12년 rung), `proj_len()` = **960** months, so the last row is `t` = 959 (attained
보험나이 119, terminal age `omega_age` = 120 **[std]**).

### The ten shipped model points

| # | sex | 가입 | 기본보험료 | 납입 | 연금개시 | GMAB | fund_set | scenario | crediting | module | what it exercises |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M | 40 | 300,000 | 10 | 60 | on | bond50_eq50 | base | decl_2026 | — | **anchor**; the three-carrier illustration cell |
| 2 | F | 40 | 300,000 | 10 | 60 | on | bond50_eq50 | base | decl_2026 | — | sex: the annuity factor, not the account |
| 3 | M | 40 | 300,000 | 10 | 60 | **off** | bond50_eq50 | base | decl_2026 | — | 미보증형: guarantee and both charges removed |
| 4 | M | 40 | 300,000 | 10 | 60 | on | bond50_eq50 | **low** | decl_2026 | — | GMAB **in the money** at −1.00% |
| 5 | M | 40 | 300,000 | 10 | 60 | on | bond50_eq50 | **high** | decl_2026 | — | the 3.75% mandated illustration return |
| 6 | M | 55 | 500,000 | 5 | 65 | on | bond80_eq20 | base | decl_2026 | — | <12년 ladder rung; 표준해약공제액 cap **binds** |
| 7 | F | 48 | 200,000 | 5 | 60 | on | bond70_eq30 | base | decl_2026 | — | =12년 ladder rung; cap **binds** |
| 8 | M | 35 | 300,000 | 10 | 60 | on | bond50_eq50 | base | decl_2026 | 추가납입 100% | strike ₩72,000,000; the charge/strike asymmetry |
| 9 | F | 45 | 400,000 | 10 | 62 | on | bond50_eq50 | base | decl_2026 | 중도인출 10%/yr from the 11th anniversary | proportional re-basing of both guarantees |
| 10 | F | 70 | 1,000,000 | 5 | 80 | on | bond80_eq20 | base | **min_guar** | — | issue-envelope corners; 최저보증이율 ladder |

Every point satisfies the issue envelope of `product-spec.md`: 가입나이 ≤ 70,
연금개시나이 45–80, 기본보험료 ≤ ₩1,000,000 per 구좌 [S1] [S2] [S9], and the minimum
거치기간 after 납입완료.

---

## State variables

Every one is a cells of `Projection` and every one is per contract except `pols_*`. The
account-value cells are stated at the **end** of the month; the in-force count is stated
at the **start**, so a row of `result_cf()` reads as the exposure the month opens with and
the flows that month produces.

| Symbol | Cells | Description | Updated |
|---|---|---|---|
| F_j(t) | `fund_pp(t, j)` | Balance of fund j at the end of month t | monthly |
| — | `fund_pp_at(t, j, timing)` | The same inside the month, at one of four timings | within month |
| AV(t) | `av_pp(t)` | 계약자적립액 at the end of month t = Σ_j F_j(t) | monthly |
| — | `av_pp_at(t, timing)` | The same inside the month | within month |
| — | `bond_weight(t)` | 채권형 share of the account at the end of month t | monthly |
| K_d(t) | `prem_paid_pp(t)` | 이미 납입한 보험료 — the strike of **both** guarantees | premium; 중도인출 |
| DB(t) | `db_pp(t)` | 사망보험금 = Max[AV(t), K_d(t)], 연금개시 전 only | monthly |
| — | `gmdb_claim_pp(t)` | GMDB top-up = max(0, K_d(t) − AV(t)) | monthly |
| C(t) | `surr_chg_pp(t)` | 해약공제액 applying to a surrender at the end of month t | annually |
| CV(t) | `cv_pp(t)` | 해약환급금 = max(0, AV(t) − C(t)) | monthly |
| — | `wd_cum_pp(t)` | Cumulative 중도인출금 to the end of month t | on withdrawal |
| — | `prem_paid_gross_pp(t)` | Premiums actually paid, **before** any withdrawal reduction | monthly |
| B(t) | `gmab_prem_base_pp(t)` | 보험료총액, the base of the premium-based GMAB charge | monthly |
| l(t) | `pols_if(t)` | Contracts in force at the **start** of month t | monthly |
| — | `pols_if_at(t, timing)` | The same inside the month: `BEF_DECR` / `BEF_LAPSE` / `AFT_DECR` | within month |
| d(t) | `pols_death(t)` | Expected deaths in month t | monthly |
| s(t) | `pols_lapse(t)` | Expected 해지 in month t, on the survivors of the deaths | monthly |
| — | `pols_maturity(t)` | Survivors carried out at the horizon | horizon month only |
| l(T) | `pols_annuitised()` | Count reaching the 연금개시 계약해당일 | once |
| — | `pols_annuity_oblig(t)` | Count an instalment is owed to in month t | annually |

**Four one-off scalars are struck once, at `t_ann()`, and never move again**:
`av_ann_pp()` = AV(T−1), `gmab_base_pp()` = K(T), `annuity_fund_pp()` = 연금재원 and
`annuity_net_pp()` = the instalment actually paid. The contract permits the insurer to
move the annuity with the 공시이율 as it is re-declared [S5] and to re-strike the
연금생명표 in the policyholder's favour [S1] [S2] [S5]; the model holds both **level**
**[std]** and says so.

**`pols_if(t)` is a genuine contract count on both sides of annuitisation** — deferred
contracts before `t_ann()`, living annuitants after it. It is **not** the count an annuity
instalment is owed to: inside the 10-year 보증기간 that is `pols_annuity_oblig(t)` =
`pols_annuitised()`, every contract that reached annuitisation whether the annuitant lives
or not, 「사망하더라도 남은 보증기간의 연금은 지급됩니다」 [S2] [S5]. The step down at the
end of the 보증기간 is real and is visible in the worked example.

---

## Assumption inputs

Three classes, following the house arrangement, because they behave differently under
governance. (a) is what the contract promises and the insurer cannot change; (b) is what
the insurer declares and may re-declare; (c) is the modeller's own view. On this product
(c) is unusually thin and unusually consequential, and it says so.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Cells / CSV | Basis |
|---|---|---|---|
| 계약체결비용 | **5.17%** of 기본보험료 = ₩15,510/month, ten years from the 계약일 | `acq_charge_pp` | [S2] |
| 계약관리비용, 납입기간 이내 | **3.50%** of 기본보험료 = ₩10,500/month | `maint_charge_in_pp` | [S2] |
| 계약관리비용, 납입기간 이후 | **1.33%** of 기본보험료 = ₩3,990/month (the document prints ₩4,000) | `maint_charge_after_pp` | [S2] [S7 제2조] |
| 위험보험료 band | **0.004%–0.011%** of 기본보험료 = ₩12–₩32/month | `risk_prem_table.csv` | [S2] [S4] |
| 최저사망보험금 보증비용 | **연 0.07%** of 계약자적립액, monthly at rate/12 | `gmdb_charge_pp` | [S1] |
| 최저연금적립금 보증비용, asset | **연 0.25%** of 계약자적립액, monthly at rate/12 | `gmab_charge_asset_pp` | [S1] |
| 최저연금적립금 보증비용, premium | **연 0.30%** of 보험료총액, monthly, **for at most 7 years** | `gmab_charge_prem_pp` | [S1] |
| 특별계정 운용보수 | 채권형 **연 0.40%**, 주식형 **연 0.60%**, daily at rate/365 | `fund_table.csv` | [S2] |
| 해약공제액 | **₩830,000 × (n − k) ÷ n** in completed years k, nil from k = n, with n = min(납입기간, 7) = **7** on the anchor | `surr_chg_pp` | [S2], fitted to its published scale; the fit **[std]** |
| 해약공제기간 cap | **7 years** where the 납입기간 is 7 years or more | `surr_chg_years` = 7 | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 표준해약공제액 | 5% × 연납순보험료 × min(납입기간, 12) = **₩1,643,940** on the anchor | `surr_chg_cap_pp` | [REG-R19] [REG-R20] |
| 해약환급금 zero floor | 「… 음(陰)의 값인 경우에는 이를 영(零)으로 처리한다」 | `cv_pp` | [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 사망보험금 | **Max[계약자적립액, 이미 납입한 보험료]**, no 기본사망보험금 | `db_pp` | [S1] [S4] [S10] [R2] |
| GMDB is compulsory | 감독규정 제7-60조제7호 requires a 최저사망보험금 on 변액보험 | — | [REG-R16] |
| 최저연금적립금 strike | **이미 납입한 보험료 at 100%**, at the single date T | `gmab_base_pp` | [S1] [R2] |
| GMAB void on early exit | not payable on 해지, on death before T, or on 조기연금개시 | `gmab_claim_pp` | [S1] [S6] [S7 제50조제3항] |
| Mandatory 채권형 ladder | 거치기간 <12년 ≥80%, =12년 ≥70%, >12년 ≥50% | `bond_floor` | [S1] [R1] |
| Pre-annuitisation de-risking | 채권형 topped to **80%** at the three 계약해당일 inside 「개시일 − 3년」 | `derisk_amount_pp` | [S1] |
| 추가납입 cap | **200%** of basic premium paid and payable, cumulative, **no loading** | `addl_prem_cap_ratio` | [S1] |
| 중도인출 limits | ≤50% of 해약환급금 [S1] [S2] [S5]; residual 계약자적립액 ≥ ₩5,000,000 per 구좌 [S1] [S5] (**[S2] publishes ₩3,000,000**); cumulative ≤ premiums paid inside 10 years [S1] [S2] [S5] | `wd_pp` | [S1] [S2] [S5] [REG-R58] |
| 중도인출 re-basing | 이미 납입한 보험료 × (AV − W) ÷ AV, proportional | `prem_paid_pp` | [S2] [S7 제51조제8항] |
| 최저보증이율, payout | 경과 5년 미만 **1.00%** / 5–10년 **0.75%** / 10년 이상 **0.50%** | `crediting_table.csv` | [S1] |
| 보증지급기간 | **10 years**, 종신연금형 정액형, annual instalments in advance | `guar_period_years` = 10 | [S1] [S2] [S5] |
| 연금수령기간 중 계약관리비용 | **연금 연액의 0.5%**, netted off each payment | `annuity_charge_pp` | [S4] |
| 중도인출 수수료 | **None** | — | [S1] [S2] [S9] |
| 추가납입 수수료 | **None** — but the fee-stack carrier [S2] charges **1.5%**, so this line is not its | — | [S1]; conflict recorded in `product-spec.md` |
| GMDB extinguishes at 연금개시 | 「일반적으로 연금개시 후 보장은 소멸됨」 | `db_pp` = 0 for t ≥ T | [R2] |
| Account boundary | the movements 감독규정 제5-7조 permits between the two accounts | `net_cf_gen` / `net_cf_sep` | [REG-R15] |
| 예정이율 | **none exists** — a variable contract's accumulation is the fund | — | [REG-R9] [REG-R48] |
| 무·저해지환급형 | **barred** on 변액보험 by 제7-66조제4항제1호 | — | [REG-R19] |

### (b) Insurer-discretionary current elements

Two lines only, and they are the two the product's economics turn on after the fee stack.
Both are re-set by the insurer and neither is guaranteed at the level shown.

| Input | Value | Cells | Basis |
|---|---|---|---|
| 공시이율, payout phase | **2.50%** at every duration | `decl_rate` | **[std]**: the 2026 평균공시이율 [REG-R48] |
| Credited rate actually used | Max[공시이율, 최저보증이율] = **2.50%** at every duration | `credit_rate` | derived; the floor never binds |
| 특별계정 fund menu and allocation | 채권형 50% / 주식형 50%, no rebalancing | `fund_table.csv` | allocation **[std]**; fees [S2] |
| 기타비용 | **0.00%** | `other_charge_pp` | **[std]**: named by [R2], quantified nowhere |
| 증권거래비용, 기초펀드 보수 | **0.00%**; observed 0.00–0.79% and 0.01–0.45% | `fund_expense_pp` | **[std]**; both ex-post estimates [S2] [S4] |
| 모집수수료 scale, years 1–5 | **1.34% / 0.41% / 0.28% / 0.25% / 0.11%** of 보험료총액 | `comm_rate` | [R1 <표 Ⅴ-3>](#krlib-variable_annuity-r1), 2017 census mean |

The 공시이율 is re-declared **monthly** off a published 공시기준이율, majority-weighted to
the insurer's own 운용자산이익률 under a formula each carrier parameterizes for itself
[REG-R18] [REG-R24]. Holding it level is a **[std]** simplification that is exact only
where the rate is level, and on this basis it is. It matters in exactly one place — the
annuity factor at `t_ann()` — because the model strikes the annuity once and holds it.

The 모집수수료 scale is a **channel** assumption before it is a level assumption. [R1]'s
2017 census puts the observed year-one range at 0.63%–2.38% and the five-year total at
1.10%–3.13%; bancassurance and online 계약체결비용 were capped at 50% of the tied-agent
level from 2016, and the one 변액연금 [R1] found buyable directly online carried **no
acquisition commission at all**. The composite is a **전속설계사** (tied agent) contract
**[std]** and the direction of that choice is stated rather than absorbed.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

Every row here is **[std]**. That is not a formatting accident: it is the finding. The
제10회 경험생명표 is not published in full [REG-R33] [REG-R34], the 참조순보험요율 display
does not reach the life side [REG-R61], no Korean carrier publishes a unit expense cost
[R2] [S12], and no retrieved document publishes a 변액연금 lapse table or a single
dynamic-lapse parameter [R1].

| Input | Value | Cells / CSV | Rationale |
|---|---|---|---|
| 보험사망률 q(x) | Makeham `mu(x)/0.80`, ages 15–120, `q(120) = 1` | `mort_table.csv` | **[std]** 25% heavier in force than the annuitant basis |
| 연금사망률 q_a(x) | Makeham `mu(x) = A + B c^(x−65)` | `mort_table.csv` | **[std]** form; anchored on [REG-R33] |
| — A | **0.0002** | — | **[std]** |
| — c | **1.10** | — | **[std]** |
| — B, male | **0.007040013548** | — | solved so complete e(65) rounds to **23.7** [REG-R33] |
| — B, female | **0.004803209921** | — | solved so complete e(65) rounds to **27.1** [REG-R33] |
| Annual q from mu | `q(x) = 1 − exp(−mu(x)(c−1)/ln c)` | `mort_table.csv` | **[std]** closed form |
| Monthly split | `1 − (1 − q)^(1/12)` | `mort_rate_mth` | **[std]** uniform force |
| 해지율, annual by policy year | **0.28 / 0.22 / 0.17 / 0.14 / 0.12 / 0.10 / 0.09 / 0.08 ultimate** | `lapse_table.csv` | level calibrated to [R1]; shape **[std]** |
| 해지율 after 연금개시 | **0.00** | `lapse_rate` | **[std]**: no retrieved document permits surrender of a 종신연금형 |
| Monthly split | `1 − (1 − w)^(1/12)` | `lapse_rate_mth` | **[std]** |
| Decrement order | **death first, then 해지** | `pols_death`, `pols_lapse` | **[std]** |
| Insurer acquisition expense | **₩300,000 per contract at issue** | `expense_acq` | **[std]**; a per-contract amount, not a rate |
| Insurer maintenance expense | **₩3,000 per contract per month**, level, no inflation | `expense_maint` | **[std]** |
| Gross asset return, `base` | **3.00% p.a.** on both funds → blended 투자수익률 **2.50%** | `return_scenario.csv` | **[std]**, back-solved from [R2] [REG-R48] |
| Gross asset return, `low` | **−0.50%** → blended **−1.00%** | `return_scenario.csv` | **[std]**, the mandated low illustration [R2] |
| Gross asset return, `high` | **+4.25%** → blended **+3.75%** | `return_scenario.csv` | **[std]**, 평균공시이율 × 1.5 [R2] |
| Volatility, correlation, time series | **none** | — | **[std]**: none was retrieved [R10] [S11] |
| 위험보험료 age scale | 15 → 0.000040, 30 → 0.000055, 40 → **0.000080**, 50 → 0.000095, 60 → 0.000110 | `risk_prem_table.csv` | level [S2] [S4]; **scale [std]** |
| Terminal age omega | **120** | `omega_age` | **[std]** |

**The mortality construction, and how thin its anchor is.** Both columns of
`mort_table.csv` come from one Makeham law fitted to **two published numbers**: the 제10회
경험생명표 65세 기대여명 of 23.7 years for men and 27.1 for women [REG-R33]. The implied
complete expectation at 보험나이 40 on the annuitant basis is **46.425** (M) and **50.292**
(F) — curtate plus a half-year, computed off the shipped table — against the population
완전생명표 figures of 41.9 and 47.4 [REG-R38], gaps of 4.5 and 2.9 years beside the 4.2 and
3.4 the two published 65세 figures themselves imply, so the extrapolation is at least
internally consistent. It is not the 경험생명표, it is not
published, and **the whole of it is [std]**; substituting a filed basis is a CSV
replacement and no formula changes.

**The 고도재해장해급여금 of ₩10,000,000 per 구좌 is charged for and never paid.** The
위험보험료 buys it [S1] [S2], the model collects the 위험보험료 in the 월공제액, and the
benefit is absent because **no 장해 incidence rate on this contract's basis was
retrieved**: the 참조순보험요율 display is a **장기손해보험** display and does not reach
the life side, and although it does carry 상해 후유장해 grids, their values were not
extracted and a non-life 상해 rate is not a life 고도재해장해 rate [REG-R34] [REG-R61].
The bias is small
— ₩24 a month at issue — and it runs one way, in the insurer's favour. It is stated rather
than hidden.

---

## Cash flow components and recursions

### Notation

| Symbol | Cells | Meaning |
|---|---|---|
| t | (index of `result_cf`) | projection month, 0-based; row t carries month t |
| N | `proj_len()` | number of projected months; rows run 0 … N − 1 |
| x | `age_at_entry()` | 가입나이, **보험나이** |
| x + ⌊t/12⌋ | `age(t)` | attained **보험나이** in month t |
| y | `policy_year(t)` | policy year containing month t, = ⌊t/12⌋ + 1 |
| k | `yrs_completed(t)` | completed whole policy years at the **end** of month t, = ⌊(t+1)/12⌋ |
| n_p, 12 n_p | `pay_term()`, `pay_months()` | 납입기간 in years and in months |
| y_a, T | `annuity_age()`, `t_ann()` | 연금개시나이 and the month of its 계약해당일 |
| m | `defer_years()` | 연금개시 전 보험기간 in whole years |
| j | `fund_ids()` | fund index; 1 = 채권형, 2 = 주식형 |
| w_j, f_j, i_j | `fund_alloc`, `fund_mgmt_fee`, `gross_return` | allocation, 운용보수, gross asset return of fund j |
| g_j | `fund_growth(j)` | one month's growth factor `(1+i_j)^(1/12)(1 − f_j/12)` |
| P | `basic_prem_pp()` | 기본보험료, per month |
| P(t), A(t) | `premium_mth_pp`, `addl_prem_pp` | 기본보험료 and 추가납입보험료 payable in month t |
| alpha, beta_1, beta_2, gamma | `acq_charge_pp`, `maint_charge_in_pp`, `maint_charge_after_pp`, `other_charge_pp` | the four expense lines |
| L | `loading_rate()` | 부가보험료율 = alpha + beta_1 + gamma rates = **0.0867** |
| P_sa(t) | `prem_to_av_pp(t)` | 특별계정 투입보험료 reaching the fund in month t |
| R(t) | `risk_prem_pp(t)` | 위험보험료 |
| c_d(t), c_a(t), c_p(t) | `gmdb_charge_pp`, `gmab_charge_asset_pp`, `gmab_charge_prem_pp` | the three guarantee-charge components |
| B(t) | `gmab_prem_base_pp(t)` | 보험료총액, the base of c_p |
| D(t) | `mth_deduct_pp(t)` | 월공제액 = R + beta_2 + c_d + c_a + c_p |
| W(t) | `wd_pp(t)` | 중도인출금 |
| F_j(t), AV(t) | `fund_pp`, `av_pp` | fund balance and 계약자적립액 at the end of month t |
| I(t), M(t) | `inv_income_pp`, `mgmt_fee_pp` | gross separate-account return and 운용보수 taken |
| K_d(t) | `prem_paid_pp(t)` | 이미 납입한 보험료 — the strike of both guarantees |
| DB(t), C(t), CV(t) | `db_pp`, `surr_chg_pp`, `cv_pp` | 사망보험금, 해약공제액, 해약환급금 |
| K(T) | `gmab_base_pp()` | 최저연금적립금 strike |
| i_c | `annuity_int_rate()` | credited rate the annuity is struck at |
| ä | `annuity_factor()` | 종신연금형 10년 보증기간부 annuity-due factor |
| Y, Y_net | `annuity_ann_pp()`, `annuity_net_pp()` | 연금 연액, gross and net of the payout charge |
| q(x), q_a(x) | `mort_rate_at_age`, `ann_mort_rate_at_age` | 보험사망률 and 연금사망률 |
| l(t), d(t), s(t) | `pols_if`, `pols_death`, `pols_lapse` | in force at the start of month t; deaths; 해지 |
| CF(t) | `net_cf(t)` | whole-contract external cash flow, **income positive** |
| CF_g, CF_s | `net_cf_gen`, `net_cf_sep` | the 일반계정 and 특별계정 ledgers |

Dimensional check: P, P_sa, D, W, F_j, AV, I, M, K_d, DB, C, CV, K(T), Y and every flow
are currency; alpha, beta, gamma, L, w_j, f_j, i_j, q, l and every ratio are dimensionless;
ä has dimensions of years, and `annuity_fund_pp / ä` is currency per year. `c_p` is a rate
per annum on a currency **that is not the fund**, which is the single most important
dimensional statement in this document.

### The two deduction points, and why they are not one

Confusing them is the commonest way to get a Korean variable model wrong, and the policy
conditions are explicit [S7 제2조]:

> 「월공제액이라 함은 해당월의 위험보험료, 계약관리비용(납입기간 종료 후 유지관련비용),
> 최저사망적립금 보증비용 및 … 보증비용의 합계액을 말합니다. … 다만, 계약체결비용,
> 계약관리비용(납입기간 중 유지관련비용), 계약관리비용(기타비용)은 보험료를 납입할 때
> 공제하며 …」

So there are **three** places a charge is taken and they are not interchangeable:

1. **Out of the premium, in the 일반계정** — 계약체결비용, 납입 중 계약관리비용, 기타비용.
   This money **never enters the 특별계정**. It is `prem_charge_pp(t)`.
2. **Out of the 계약자적립액, by cancelling units on the 월계약해당일** — the 월공제액:
   위험보험료, 납입 **후** 계약관리비용, and both guarantee charges. It is
   `mth_deduct_pp(t)`, and it moves 특별계정 → 일반계정.
3. **Inside the 기준가격** — the 특별계정 운용보수, deducted out of net assets before the
   unit price is struck [S7 제43조제2호]. The policyholder never sees a deduction; the unit
   price is simply lower. It is `mgmt_fee_pp(t)` and it is written as a **factor on the
   growth**, not as a unit cancellation.

The identity [R2] states is

```
특별계정 투입보험료 = 납입보험료 − (계약체결비용 + 납입 중 계약유지비용 + 기타비용)
                    = 순보험료 + 납입 후 계약유지비용
```

and the **second line is the one that matters**: the 계약관리비용 for the period *after*
납입완료 is collected during the premium-paying period and carried inside the account
value, then drawn back out month by month once premiums stop. That is why the monthly
deduction **steps up** at 납입완료 with no premium arriving to offset it, and why [S2]'s
own illustration shows its cumulative separate-account contribution *falling* from
₩32,877,360 at ten years to ₩32,393,520 at twenty.

### Premium and the front-end deduction (일반계정)

```
P(t)        = P                      for t < min(12 n_p, T),  else 0
A(t)        = a P                    for t < min(12 n_p, T) and while headroom remains
alpha(t)    = 0.0517 P               for t < min(12 n_p, 120 months, T)      [S2]
beta_1(t)   = 0.0350 P               for t < min(12 n_p, T)                  [S2]
gamma(t)    = 0.0000 P                                                       [std]
prem_charge_pp(t) = alpha(t) + beta_1(t) + gamma(t)
P_sa(t)     = P(t) − prem_charge_pp(t) + A(t)
```

The 계약체결비용 runs for **the shorter of ten years and the 납입기간** **[std]**: [S2]
prints ten years on its own 10년납 contract, where the two coincide, and a charge on a
premium cannot outlive the premium. The 추가납입보험료 attracts **no loading** and enters
the fund in full [S1], which is why it is added *after* the charge and is subtracted before
`check_prem_alloc()` tests the ratio.

`prem_alloc_ratio(t)` = (P(t) − prem_charge_pp(t)) / P = **1 − L = 0.9133** while both
front-end charges run, rising to 1.0000 once the 계약체결비용 stops. Three carriers'
first-year illustrations put the realised ratio at 91.3%, 91.3% and 91.4% on this cell
[S1] [S2] [S6], and [R1]'s industry band is 「납입보험료의 5~15%를 … 차감한 후 85~95%만
투자」. `check_prem_alloc()` asserts it at every month.

### The 월공제액 (특별계정 → 일반계정)

```
R(t)   = r(age(t)) P                                            r from risk_prem_table
beta_2 = 0.0133 P                    for 12 n_p <= t < T,  else 0            [S2]
c_d(t) = (0.0007 / 12) x av_pp_at(t, "BEF_DEDUCT")                           [S1]
c_a(t) = (0.0025 / 12) x av_pp_at(t, "BEF_DEDUCT")   if gmab_flag() = 1      [S1]
c_p(t) = (0.0030 / 12) x B(t)        for t < min(12 n_p, 84 months, T)       [S1]
B(t)   = 보험료총액 = 12 n_p P + (추가납입 paid before month t)               [S1]

D(t)   = min[ R(t) + beta_2(t) + c_d(t) + c_a(t) + c_p(t) ,
              max(0, av_pp_at(t, "BEF_DEDUCT")) ]                            [std] cap
```

**The two asset-based guarantee charges are struck on the account value *after* the
premium has gone in**, at the `BEF_DEDUCT` timing — that is a modelling choice and it is
tagged where it is made. The **premium-based** component `c_p` is not on the fund at all:
its base is 「이미 납입한 보험료(특약보험료 제외) 및 추후 납입할 기본보험료 합계」, the
whole premium the policyholder has undertaken to pay, past *and* future [S1]. On the anchor
cell that is a flat **₩9,000 a month against a first-year account value of ₩3,216,621
— over 3% a year of the fund at outset**, falling below 0.5% a year by the seventh
year, after which it stops entirely. A model that treats guarantee charges as basis points
on the account value misstates this contract's early-duration cash flow by an order of
magnitude, which is why the asset and premium components are separate cells with separate
bases and separate stopping rules.

The **cap at the available account value** is **[std]**. The contract's own remedy for an
unpayable deduction is to end the premium holiday or to lapse the contract [S1]; neither is
represented, and on the shipped points the cap never binds.

### 중도인출 and the guarantee re-basing

```
W(t) = 0 unless the module is on, t is a 계약해당일 (t mod 12 = 0 and t > 0; t = 0 is the
       계약일 itself, not an anniversary), t >= 12 x wd_start_year
     = min[ wd_ratio x CV, 0.50 x CV, AV_after_deduct − 5,000,000,
            (premiums paid − withdrawals to date) if t < 120 months ]   [S1] [S2] [S5]

K_d(t) = [ K_d(t−1) + P(t) + A(t) ] x (AV_bef − W(t)) / AV_bef      [S2] [S7 제51조제8항]
```

where `AV_bef` is the account after the 월공제액 and before the withdrawal. **Without the
proportional re-basing a policyholder could withdraw the fund and keep the strike**, and
[R1] is explicit that the reduction is a guarantee-risk mitigant and not a convenience:
「중도인출금은 최저보증한도에서 차감된다」. The ten-year cumulative limit is a **tax** rule
showing through into the policy conditions — it is what keeps the 소득세법 시행령 제25조
ten-year exemption open [REG-R58]. The model takes **one withdrawal a year** on the
계약해당일 **[std]**, against a contract permitting twelve [S1].

### The mandatory pre-annuitisation de-risking

```
derisk_amount_pp(t) = max(0, 0.80 x AV_aft_deduct(t) − bond_aft_deduct(t))
                      at t = T − 36, T − 24, T − 12 only                       [S1]
```

「「연금지급개시일 − 3년」시점부터 매년 연계약해당일에 … 채권형 … 계약자적립액의 합계가
펀드 전체 계약자적립액의 80% 미만인 경우 … 자동 조정됩니다」 [S1]. It **conserves the
total**: money moves between funds and never out of the account, which is why it does not
appear in `check_av_roll_fwd_resid`. It is applied **after** the 월공제액 and **before**
the month's growth **[std]**. Unlike 펀드자동재배분 and 펀드자동전환옵션 — which the base
run leaves off, a single deterministic path being unable to distinguish them from a
different fixed allocation — this one is **not optional and is on**.

### The account recursion

Fund by fund, in the order the month applies them:

```
F_j(t, BEF_PREM)   = 0 for t = 0, else F_j(t−1)   (no account before the first premium)
F_j(t, BEF_DEDUCT) = F_j(t, BEF_PREM) + P_sa(t) w_j
F_j(t, AFT_DEDUCT) = F_j(t, BEF_DEDUCT)
                     − [D(t) + W(t)] x F_j(t, BEF_DEDUCT) / AV(t, BEF_DEDUCT)
F_j(t, AFT_DERISK) = F_j(t, AFT_DEDUCT) +/- the de-risking transfer
F_j(t)             = F_j(t, AFT_DERISK) x g_j,      g_j = (1 + i_j)^(1/12) (1 − f_j/12)

AV(t) = SUM_j F_j(t)
```

so that, summed over funds,

```
AV(t) = [ AV(t−1) + P_sa(t) − D(t) − W(t) ] grown at the fund-weighted g
      = AV(t−1) + P_sa(t) − D(t) − W(t) + I(t) − M(t)
```

which is exactly the residual `check_av_roll_fwd_resid(t)` drives to zero, with the
연금재원 transfer subtracted in the month `t = T`. The opening balance `AV(t−1)` is **nil
in `t = 0`**, so the identity closes on the first row too — the row that carries the single
premium, the 계약체결비용 and the whole first month's charge stack. The 월공제액 and the
중도인출 are taken **pro rata across funds** on the `BEF_DEDUCT` weights **[std]**.

Two quantities fall out of the growth step and are published separately, because they land
in different places:

```
I(t) = SUM_j F_j(t, AFT_DERISK) [ (1 + i_j)^(1/12) − 1 ]        gross return, to the fund
M(t) = SUM_j F_j(t, AFT_DERISK) (1 + i_j)^(1/12) f_j / 12       운용보수, to the 일반계정
```

`check_charge_split()` asserts `I(t) − M(t) = AV(t) − AV(t, AFT_DERISK)` at every month.
That identity is the guard against the charge-base confusion this product is most often
modelled wrong at: **four different bases in one stack** — the fund (운용보수, both
asset-based guarantee charges), the premium (계약체결비용, 계약관리비용, 위험보험료), the
보험료총액 (the premium-based guarantee charge) and the 연금 연액 (the payout charge).

The 운용보수 is taken **monthly at rate/12** against a contractual **rate/365 daily**
**[std]**, the monthly grid having no daily step. Note that the disclosed 투자수익률 is
already net of it: [S6]'s illustration shows a gross-to-net gap of 0.01 percentage points
on a product with no guarantee charge — far too small to contain a management fee — while
[S1]'s gap of 0.32pp is exactly its two account-based guarantee charges.

### Benefits before 연금개시

```
DB(t) = Max[ AV(t), K_d(t) ]                                             [S1] [S4] [S10]
gmdb_claim_pp(t) = max(0, K_d(t) − AV(t))          the 일반계정 보증준비금 part  [R2]
n     = min(n_p, 7)                    the 해약공제기간; 7 on the anchor, 5 on points 6, 7, 10
C(t)  = min(0.2305555556 x 12 P, surr_chg_cap_pp()) x (n − k) / n,  nil from k = n
CV(t) = max(0, AV(t) − C(t))                                             [REG-R19]
```

`check_gmdb_floor()` asserts `DB(t) = AV(t) + gmdb_claim_pp(t)` at every month — the death
benefit splits **exactly** into the part released from the 특별계정 and the part met from
the 일반계정 보증준비금, and that split is what makes the two account ledgers add back to
`net_cf`.

The 해약공제액 runs off **linearly in the amount, not in the ratio**. All three retrieved
scales fit `C × (n − k) ÷ n` exactly [S2] [S4] [S5]; the published *ratio* falls far faster
only because its denominator is growing. Expressing `C` as **23.05556% of the annualized
기본보험료** so that [S2]'s ₩830,000 scales to other cells is **[std]**. The charge **is**
the unamortised 계약체결비용 [R2], which is why the composite takes its acquisition cost
and its surrender charge from one carrier: pairing [S2]'s 5.17% with [S5]'s ₩1,077,000
would recover more on surrender than was ever loaded.

The 표준해약공제액 cap is `0.05 × 12P × (1 − L) × min(n_p, 12)` [REG-R19] [REG-R20]. Note
6 to 별표 14 further requires the acquisition cost loaded onto the premium to be discounted
at the 평균공시이율 and netted off the cap; **no retrieved document works that netting**,
so the exact residual cap is **[unverified]** [REG-R21] and the model applies the gross
cap. It binds on three shipped points, all 5년납. `check_surr_chg_cap()` asserts
compliance.

### Annuitisation, at the single month T

```
AV(T)  = av_ann_pp()            = av_pp(T − 1)
K(T)   = gmab_base_pp()         = prem_paid_pp(T − 1)                              [S1] [R2]
GMAB   = gmab_claim_pp()        = max(0, K(T) − AV(T))    if gmab_flag() = 1
연금재원 = annuity_fund_pp()      = AV(T) + GMAB                                     [S6]

i_c    = Max[공시이율, 최저보증이율] at duration 0
ä      = SUM_{k=0..9} v^k  +  SUM_{k=10..omega−y_a−1} v^k (k p_{y_a}),  v = 1/(1 + i_c)
Y      = 연금재원 / ä
Y_net  = Y (1 − 0.005)                                                             [S4]
```

Three things about this block are load-bearing.

**The GMAB is a European option struck on one date.** It is not payable on 해지, not
payable on death before T, and forfeited on 조기연금개시 — 「만기 전에 사망 또는 해약이
발생하는 경우 이 보증은 성립하지 않으며」 [S1] [S6] [S7 제50조제3항] [S8] [S10] [R1] — so
its payoff is weighted by `pols_annuitised()`, which carries **every** decrement that
occurred before T. A model treating it as a floor on the account at every duration would
overstate its cost by the whole of the pre-annuitisation exit probability, which on a
seven-year persistency below 30% [R1] is most of it.

**The account-value part and the guarantee part move differently.** `av_transfer(t)` moves
AV(T) from the 특별계정 to the 일반계정 and appears in **both** ledgers with opposite
signs; the GMAB top-up moves **inside** the 일반계정, from the 보증준비금 to the 연금재원,
and so appears in **neither**. Its only cash-flow consequence is a larger annuity for the
rest of the projection, and that is where a reader should look for it.

**The first ten instalments are certain and the rest are life-contingent.** Inside the
보증기간 the weight is one whatever the annuitant does, which is the arithmetic statement
of 「사망하더라도 남은 보증기간의 연금은 지급됩니다」 [S2] [S5]. The sum is truncated at
`omega_age` for consistency with the projection horizon.

### Decrements

```
q(t)      = 보험사망률(age(t))     for t < T,     연금사망률(age(t)) for t >= T
q_mth(t)  = 1 − (1 − q(t))^(1/12)
w(t)      = 해지율 by policy year for t < T,      0 for t >= T
w_mth(t)  = 1 − (1 − w(t))^(1/12)

d(t) = l(t) q_mth(t)                                    death first        [std]
s(t) = [ l(t) − d(t) ] w_mth(t)                         then 해지          [std]
l(t+1) = l(t) − d(t) − s(t) − pols_maturity(t)
```

**The two periods are priced on different mortality tables in Korea and the model does not
pretend otherwise**: 보험사망률 through the deferral, 연금사망률 from `t_ann()`. The switch
is visible in the worked example — `mort_rate(239)` = 0.0054591503 on the insurance basis
and `mort_rate(240)` = 0.0047847455 on the annuitant basis, a **12.35% drop across one
month** that is a change of table and not a change of risk.

`pols_maturity(t)` is nil except in the horizon month, where it carries out the survivors
so that the roll-forward closes. **A 종신연금형 pays nothing at the horizon**, so
`claims_maturity` is structurally zero at every t; the column exists so that the truncation
at `omega_age` is visible rather than absorbed into the last row's decrements.

### Processing order (month t = 0 … N − 1)

The order is not presentational: five of the flows depend on it, and two of the `check_*`
identities exist only because it is fixed.

1. **Premium**, received into the **일반계정**: `prem_pp(t)` = 기본보험료 + 추가납입보험료.
2. **Front-end deduction**, retained in the **일반계정**: `prem_charge_pp(t)`. This money
   never enters the 특별계정 and never comes back out of one.
3. **Transfer to the 특별계정**: `prem_to_av_pp(t)`, allocated across funds at the
   **fixed** `fund_alloc(j)`. Timing `BEF_DEDUCT`.
4. **월공제액**, cancelled out of the 계약자적립액 pro rata across funds. The two
   asset-based guarantee charges are struck on `av_pp_at(t, "BEF_DEDUCT")` — **after** the
   premium has gone in. Capped at the available account value **[std]**.
5. **중도인출**, taken with the 월공제액, pro rata across funds. Timing `AFT_DEDUCT`.
6. **Guarantee-base re-basing**: `prem_paid_pp(t)` grows by the month's premiums and is
   then scaled by (AV − W) ÷ AV.
7. **Mandatory de-risking** at `t = T − 36, −24, −12`. Timing `AFT_DERISK`. Conserves the
   total.
8. **Growth**, fund by fund: gross asset return first, then the 운용보수, which is inside
   the 기준가격 [S7 제43조제2호].
9. **Decrements** on `pols_if(t)`: **death first, then 해지** **[std]**; `pols_maturity`
   only in the horizon month.
10. **Benefits** on the **end-of-month** account: 사망보험금 Max[AV(t), K_d(t)],
    해약환급금 max(0, AV(t) − C(t)).
11. **At t = T**: `annuity_fund_pp()` = AV(T) + GMAB; the account-value part transfers
    특별계정 → 일반계정, the GMAB top-up moves inside the 일반계정. The 특별계정 is empty
    from here.
12. **Payout phase**: an annual instalment at `t = T, T+12, T+24, …`, level, owed to
    `pols_annuitised()` while the 보증기간 runs and to `pols_if(t)` afterwards. Death
    decrement on the 연금사망률; no lapse; no surrender; no death benefit.

Two consequences worth stating because they are easy to get backwards. **The benefit is
struck on the end-of-month account**, so a death in month t is paid on AV(t), after that
month's deduction and growth. And **the guarantee charges are struck before the growth**,
on `BEF_DEDUCT`, so a rising month raises next month's charge and not this month's.

### Net cash flow

```
net_cf(t) = premiums(t)
          − claims_death(t) − claims_lapse(t) − claims_annuity(t) − claims_maturity(t)
          − withdrawals(t) − fund_expenses(t) − expenses(t) − commissions(t)
```

income-positive, and **every internal transfer is absent by construction**, which is what
makes the columns of `result_cf()` sum to this line. There is no `claims` column beside the
four `claims_*` columns: a cash flow statement must not publish its own subtotal beside its
parts. The `claims(t, kind)` cells stays and takes `DEATH`, `LAPSE`, `ANNUITY`,
`MATURITY`.

The two account ledgers decompose it:

```
CF_s(t) = prem_to_av(t) − av_charges(t) − surr_charges(t) − claims_from_av(t, DEATH)
          − claims(t, LAPSE) − withdrawals(t) − av_transfer(t) − fund_expenses(t)

CF_g(t) = premiums(t) + av_charges(t) + surr_charges(t) + av_transfer(t)
          − prem_to_av(t) − gmdb_claims(t) − claims(t, ANNUITY) − claims(t, MATURITY)
          − expenses(t) − commissions(t)
```

Every transfer that appears in these two lines is one of the movements 감독규정 제5-7조
permits between the two accounts [REG-R15]: premium receipt and benefit payment, transfer
to the general account of the amounts needed for risk cover and for acquisition,
maintenance and administration, the management fee, and the 연금재원 moved at 연금개시.
Each appears in both with opposite signs, so their sum is the whole-contract external cash
flow **and nothing else**. `check_net_cf()` asserts exactly that at every month, and it is
the identity a 변액연금보험 has to cross the 특별계정 / 일반계정 boundary to state. **A
model that cannot state it has not represented the boundary.**

Eight `check_*()` cells are published, each taking no argument and returning a `bool`,
with the signed per-month residual under `<name>_resid(t)`:

| Check | What it asserts |
|---|---|
| `check_net_cf()` | `net_cf = net_cf_gen + net_cf_sep` — the account-boundary identity |
| `check_pols_roll_fwd()` | `l(t) − l(t+1) = d(t) + s(t) + pols_maturity(t)` |
| `check_av_roll_fwd()` | the 계약자적립액 recursion, including the 연금재원 transfer at T |
| `check_charge_split()` | `I(t) − M(t) = AV(t) − AV(t, AFT_DERISK)` |
| `check_gmdb_floor()` | `DB(t) = AV(t) + gmdb_claim_pp(t)` |
| `check_bond_floor()` | the 채권형 weight meets the mandatory ladder at every month |
| `check_surr_chg_cap()` | the 해약공제액 stays inside the 표준해약공제액 |
| `check_prem_alloc()` | the premium allocation matches the published fee stack |

All eight are `True` on all ten shipped model points.

### Optional modules (all off in the base run)

| Module | Control | State on the anchor | Exercised by |
|---|---|---|---|
| 추가납입보험료 | `addl_prem_ratio` | **off** | point 8, at 100% of the 기본보험료 |
| 중도인출 | `wd_ratio`, `wd_start_year` | **off** | point 9, 10% a year from the 11th anniversary |
| The GMAB itself | `gmab` | **on** | point 3 turns it off (미보증형) |
| The return path | `scenario_id` | `base` (2.50%) | points 4 (−1.00%) and 5 (3.75%) |
| The 최저보증이율 ladder | `crediting_basis` | **inert** — 2.50% exceeds every step | point 10 (`min_guar`) |
| The 채권형 ladder rung | `fund_set` + `defer_years` | >12년, floor 50% | points 6 (<12년) and 7 (=12년) |
| 증권거래비용, 기초펀드 보수 | `fund_expense` rate | **0.00** | not exercised; a CSV change |

**Documented in `product-spec.md` and deliberately not implemented**: 펀드자동재배분,
펀드자동전환옵션, 조기연금개시, 일반계정 전환, 보험계약대출, 감액, 보험료 납입
일시중지/중지/종료, 성과·장기유지 보너스, the roll-up / step-up / ratchet GMAB bases, the
CPPI-funded monthly-ratchet guarantee that carries **no** guarantee charge [S6], the
elective switchable GMAB [S9], and the 실적배당 종신연금 (GLWB) in which the money stays in
the separate account through the payout phase [S2] [S7] [S8] [S10]. Every one of them is a
first-order lever on guarantee cost and none of them can be exercised meaningfully on one
deterministic path.

**One implementation limitation of the 추가납입 module, stated rather than discovered
later.** `gmab_prem_base_pp(t)` counts 추가납입 paid *before* month t using a closed form
that assumes the cumulative 200% cap has not yet bitten. On the shipped points it never
does — point 8 accumulates ₩36,000,000 of additional premium against a cap of ₩72,000,000 —
but a user who raises `addl_prem_ratio` past the point where the cap binds will find the
charge base and the actual premium diverge.

---

## Policyholder behavior modeling

**Lapse is static and exogenous here, and it is neither in reality.** That sentence is the
whole of this section's content and everything else is its justification.

The scale is annual by policy year — **0.28 / 0.22 / 0.17 / 0.14 / 0.12 / 0.10 / 0.09 /
0.08 ultimate** — converted to a monthly rate by `1 − (1 − w)^(1/12)` **[std]** and applied
to the survivors of the month's deaths. Its **level** is calibrated to the only published
Korean figure for this product: 「변액보험의 7년 평균 유지율은 30% 미만으로 알려져 있다」,
itself second-hand inside [R1] and reported from a 2016 금융감독원 release that was not
retrieved. The scale produces a lapse-only seven-year persistency of **0.28891508** and,
with mortality, an in-force count at month 84 of **0.28606298**. Its **shape** by duration
is **[std]**: a monotone run-down from the first-year rate to the ultimate, with the
ultimate starting in the eighth policy year, the duration at which the 해약공제 has run off
and [R1]'s seven-to-ten-year break-even window opens. **No Korean carrier publishes a
변액연금 적용해지율** [S12].

**The market and reserving convention is dynamic, and the model does not use it.** [R1]
states the convention plainly:

> 「동적해지율이란 최저보증 발생률(In-the-moneyness)에 따라 해지율을 달리 적용하는
> 방법으로, 최저보증 발생률이 높을수록 해지율을 감소시키고, 최저보증 발생률이 낮을수록
> 해지율을 증가시켜야 한다」

but **no retrieved document publishes a functional form or a single parameter**. Any
dynamic-lapse formula written here would be a [std] construction dressed as a cited one, so
the base run does not attempt one. The consequence is stated where it bites: on a path
where the guarantee goes deeply in the money, a static lapse rate lets contracts leave that
a real policyholder would keep, and the guarantee cost is understated in exactly the
scenarios that drive the reserve. Substituting a dynamic form is a change to
`lapse_rate(t)` alone and touches nothing else in the model.

**The other behaviours the contract permits are switches, not hazards.** 추가납입 and
중도인출 are modelled as deterministic per-model-point rules — 100% of the basic premium
every month, 10% of the surrender value once a year — because there is no Korean
utilisation study to calibrate an intensity against. The point of the two modules is not to
predict take-up; it is to show what take-up does to the guarantee bases, and the two work
in opposite directions:

- **추가납입 grows the strike without a loading.** Point 8's GMAB strike is
  **₩72,000,000** against the anchor's ₩36,000,000, and its 보험료총액 charge base grows
  with the premiums actually paid. The **asymmetry** is the interesting part: `c_p` stops
  at seven years while the strike keeps growing for the remaining three years of the
  premium term, so late additional premium buys guarantee for nothing [S1].
- **중도인출 shrinks the strike proportionally.** Point 9's strike falls from a
  contractual ₩48,000,000 to **₩25,509,168**, and every won of the reduction is the
  re-basing rule doing what [R1] says it is for.

**Every option the policyholder holds points the same way, and none of them can be
exercised on one path.** 조기연금개시 is available only where the guarantee is out of the
money [S1] [S9] [S10]; 일반계정 전환 is offered at or above 130% of premiums paid,
irreversibly [R1]; and the automatic transfer at a CPPI barrier is the same trade made by
the insurer instead [S6]. A deterministic run has no mechanism to represent a decision that
depends on a distribution, and the model does not pretend to.

**Annuitisation is certain in this model.** Every contract reaching `t_ann()` annuitises,
on the 종신연금형 10년 보증기간부 정액형 form **[std]**, which is the modal election, the
only one exercising both longevity and a guarantee period, and the form the 소득세법
종신형 연금보험 route is written around — that route requiring the guarantee period to sit
within the published 기대여명 [REG-R58]. The market menu is uniform across carriers —
보증기간 of 10 / 15 / 20 years, to age 100, or 기대여명보증, in 정액형 or 체증형
[S1] [S2] [S5] — and choosing among them is a policyholder decision this model does not
model.

---

## Worked example

Everything in this section was read off `VA_KR_S` and can be reproduced by running it.
`tests/test_variable_annuity_kr.py` asserts these figures against the model cell by cell
to the precision shown, so a discrepancy between this document and the model is a failure
of the library and not a rounding matter.

```
cd /home/user/lifelib-products
python lifelib/libraries/krlib/products/variable_annuity/run.py
```

**One arithmetic caveat governs every trace below.** The model computes in IEEE-754 double
precision with no intermediate rounding. `0.2305555556 × 3,600,000` is
**830,000.0001599999**, not ₩830,000 exactly, and the residue propagates through the whole
surrender-charge scale; `0.000080 × 300,000` is **24.000000000000004**. Traces therefore
use the model's own values rather than the round contractual ones, and every figure quoted
as a *result* is the model's own. Where an intermediate is printed rounded, a figure
recomputed by hand from it can differ in its last digit or two.

### The anchor cell and every assumption it uses

**Model point 1**, `policy_id` `VA-000001`: 남자, **보험나이 40**, 기본보험료 **₩300,000
월납**, **10년납**, **연금개시나이 60**, **보증형**, 채권형 50% / 주식형 50%, the `base`
return path, the `decl_2026` crediting basis, no 추가납입 and no 중도인출,
`pols_if_init` 1.0. This is the illustration cell **three independent carriers publish**
[S1] [S2] [S6] and the only cell at which the composite's parameters can be checked
against published surrender-value tables.

Derived, at the precision the model produces:

```
pay_months()                                 120
t_ann()                                      240
defer_years()                                 20
proj_len()                                   960      rows 0 ... 959; (120 − 40) x 12
prem_ann_pp()                          3,600,000.00
prem_total_pp()                       36,000,000.00   (3,600만원)
loading_rate()                                 0.0867
bond_floor()                                   0.50   the >12년 rung
surr_chg_cap_pp()                      1,643,940.00   표준해약공제액, 별표 14
```

Every assumption value the cell uses, in full, with tags:

| Quantity | Cells | Value | Tag |
|---|---|---|---|
| 계약체결비용 rate | `charge_rate("acq_charge")` | 0.0517 | [S2] |
| 계약관리비용 납입 중 rate | `charge_rate("maint_charge_in")` | 0.0350 | [S2] |
| 기타비용 rate | `charge_rate("other_charge")` | 0.0000 | **[std]** |
| 계약관리비용 납입 후 rate | `charge_rate("maint_charge_after")` | 0.0133 | [S2] |
| 위험보험료 rate at 보험나이 40 | `risk_prem_rate(40)` | 0.000080 | level [S2] [S4]; scale **[std]** |
| — at 보험나이 50 | `risk_prem_rate(50)` | 0.000095 | **[std]** |
| GMDB 보증비용 rate | `charge_rate("gmdb_charge")` | 0.0007 p.a. | [S1] |
| GMAB 보증비용, asset | `charge_rate("gmab_charge_asset")` | 0.0025 p.a. | [S1] |
| GMAB 보증비용, premium | `charge_rate("gmab_charge_prem")` | 0.0030 p.a. | [S1] |
| 특별계정 운용보수, 채권형 | `fund_mgmt_fee(1)` | 0.0040 p.a. | [S2] |
| 특별계정 운용보수, 주식형 | `fund_mgmt_fee(2)` | 0.0060 p.a. | [S2] |
| 증권거래비용·기초펀드 보수 | `charge_rate("fund_expense")` | 0.0000 | **[std]** |
| 해약공제 level rate | `charge_rate("surr_charge")` | 0.2305555556 | [S2], expressed as a ratio **[std]** |
| 표준해약공제액 rate | `charge_rate("surr_charge_cap")` | 0.0500 | [REG-R20] |
| 연금수령기간 중 계약관리비용 | `charge_rate("annuity_charge")` | 0.0050 | [S4]; adoption **[std]** |
| 모집수수료, years 1–5 | `comm_rate(1..5)` | 0.0134 / 0.0041 / 0.0028 / 0.0025 / 0.0011 | [R1 <표 Ⅴ-3>](#krlib-variable_annuity-r1) |
| Insurer acquisition expense | `charge_rate("expense_acq")` | 300,000.0 per contract | **[std]** |
| Insurer maintenance expense | `charge_rate("expense_maint")` | 3,000.0 per contract per month | **[std]** |
| Fund allocation | `fund_alloc(1)`, `fund_alloc(2)` | 0.5, 0.5 | **[std]** |
| Gross asset return, both funds | `gross_return(1)`, `gross_return(2)` | 0.0300 | **[std]**, back-solved from [R2] [REG-R48] |
| Monthly growth factor, 채권형 | `fund_growth(1)` | 1.0021321143490463 | derived |
| Monthly growth factor, 주식형 | `fund_growth(2)` | 1.0019650366374175 | derived |
| 보험사망률, 보험나이 40 M | `mort_rate(0)` | 0.0011138523 | **[std]** Makeham |
| — monthly | `mort_rate_mth(0)` | 9.286844533373806e-05 | **[std]** |
| — 보험나이 41 | `mort_rate(12)` | 0.0011989710 | **[std]** |
| — 보험나이 50 | `mort_rate(120)` | 0.0024695609 | **[std]** |
| — 보험나이 59 (last deferral month) | `mort_rate(239)` | 0.0054591503 | **[std]** |
| 연금사망률, 보험나이 60 M | `mort_rate(240)` | 0.0047847455 | **[std]**; e(65) = 23.7 [REG-R33] |
| 해지율, policy year 1 | `lapse_rate(0)` | 0.28 | level [R1]; shape **[std]** |
| — monthly | `lapse_rate_mth(0)` | 0.027004030272665847 | **[std]** |
| — policy year 2 | `lapse_rate(12)` | 0.22 | **[std]** |
| — policy year 8+ | `lapse_rate(119)` | 0.08 | **[std]** |
| 공시이율, payout | `annuity_int_rate()` | 0.025 | **[std]**, 2026 평균공시이율 [REG-R48] |

### The charge stack in month 0, per contract

Five lines, three deduction points, four bases. This is the table the rest of the worked
example is arithmetic on.

| Line | Cells | Amount, KRW | Base | Account |
|---|---|---|---|---|
| 계약체결비용 | `acq_charge_pp(0)` | **15,510.00** | 기본보험료 | 일반계정, out of the premium |
| 계약관리비용, 납입 중 | `maint_charge_in_pp(0)` | **10,500.00** | 기본보험료 | 일반계정, out of the premium |
| 기타비용 | `other_charge_pp(0)` | **0.00** | 기본보험료 | 일반계정, out of the premium |
| = 특별계정 투입보험료 | `prem_to_av_pp(0)` | **273,990.00** | — | 일반계정 → 특별계정 |
| 위험보험료 | `risk_prem_pp(0)` | **24.000000000000004** | 기본보험료 | 특별계정 → 일반계정 |
| 계약관리비용, 납입 후 | `maint_charge_after_pp(0)` | **0.00** (₩3,990.00 from t = 120) | 기본보험료 | 특별계정 → 일반계정 |
| GMDB 보증비용 | `gmdb_charge_pp(0)` | **15.98275** | 계약자적립액 `BEF_DEDUCT` | 특별계정 → 일반계정 |
| GMAB 보증비용, asset | `gmab_charge_asset_pp(0)` | **57.081250000000004** | 계약자적립액 `BEF_DEDUCT` | 특별계정 → 일반계정 |
| GMAB 보증비용, premium | `gmab_charge_prem_pp(0)` | **9,000.00** | 보험료총액 ₩36,000,000 | 특별계정 → 일반계정 |
| = 월공제액 | `mth_deduct_pp(0)` | **9,097.063999999998** | — | 특별계정 → 일반계정 |
| 특별계정 운용보수 | `mgmt_fee_pp(0)` | **110.64426393373063** | 특별계정 순자산 | inside the 기준가격 |
| 증권거래비용·기초펀드 보수 | `fund_expense_pp(0)` | **0.00** | 특별계정 자산 | 특별계정 → third parties |
| 해약공제액 if surrendered now | `surr_chg_pp(0)` | **830,000.0001599999** | annualized 기본보험료 | 특별계정 → 일반계정 |

`prem_alloc_ratio(0)` = **0.9133** exactly, the ratio three carriers publish at 91.3%,
91.3% and 91.4% on this cell [S1] [S2] [S6].

**Read the first-year totals off that table.** 계약체결비용 ₩186,120 + 계약관리비용
₩126,000 + 위험보험료 ₩288 + GMAB premium component ₩108,000, plus the two account-based
guarantee charges of ₩5,576.29 — **₩425,984.29 on ₩3,600,000 of premium, 11.83%** —
against [R1]'s industry band of 「선취상품은 납입보험료의 5~15%를 … 차감한 후 85~95%만
투자」. **Over a quarter of the first year's charge is the premium-based guarantee component
alone**, and it is not on the fund: the two charges struck on the account are ₩1,219.81 and
₩4,356.47 in a year in which the account is still being built.

### The surrender-charge scale, to the won

`surr_chg_pp(12k)` for k = 0 … 8, being the specification's published table:

```
k = 0   830,000.0001599999
k = 1   711,428.5715657143
k = 2   592,857.1429714285
k = 3   474,285.7143771428
k = 4   355,714.2857828572
k = 5   237,142.8571885714
k = 6   118,571.4285942857
k = 7         0.0
k = 8         0.0
```

against the 표준해약공제액 cap of **₩1,643,940.00**, which the level charge is **50.5%**
of and so does not bind on this cell. It binds on points 6, 7 and 10, all 5년납.

### First periods of the base run

Per contract-equivalent, income-positive, to two decimal places — the form `run.py` prints.
`claims_annuity`, `claims_maturity`, `withdrawals` and `fund_expenses` are **0.00 at every
row shown here** and are omitted; they are columns of `result_cf()` all the same.

| t | `pols_if` | `premiums` | `claims_death` | `claims_lapse` | `expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|
| 0 | 1.0000000000 | 300,000.00 | 27.86 | 0.00 | 303,000.00 | 40,200.00 | **−43,227.86** |
| 1 | 0.9729056091 | 291,871.68 | 54.21 | 0.00 | 2,918.72 | 39,110.81 | 249,787.95 |
| 2 | 0.9465453242 | 283,963.60 | 79.11 | 0.00 | 2,839.64 | 38,051.12 | 242,993.73 |
| **3** | 0.9208992552 | 276,269.78 | 102.63 | **5,833.06** | 2,762.70 | 37,020.15 | 230,551.24 |
| 4 | 0.8959480508 | 268,784.42 | 124.81 | 12,142.30 | 2,687.84 | 36,017.11 | 217,812.35 |
| 5 | 0.8716728841 | 261,501.87 | 145.71 | 18,116.58 | 2,615.02 | 35,041.25 | 205,583.30 |
| 6 | 0.8480554382 | 254,416.63 | 165.39 | 23,769.13 | 2,544.17 | 34,091.83 | 193,846.11 |
| 7 | 0.8250778927 | 247,523.37 | 183.90 | 29,112.73 | 2,475.23 | 33,168.13 | 182,583.38 |
| 8 | 0.8027229098 | 240,816.87 | 201.28 | 34,159.69 | 2,408.17 | 32,269.46 | 171,778.28 |
| 9 | 0.7809736215 | 234,292.09 | 217.58 | 38,921.90 | 2,342.92 | 31,395.14 | 161,414.54 |
| 10 | 0.7598136169 | 227,944.09 | 232.86 | 43,410.83 | 2,279.44 | 30,544.51 | 151,476.44 |
| 11 | 0.7392269297 | 221,768.08 | 247.14 | 50,004.27 | 2,217.68 | 29,716.92 | 139,582.06 |
| **12** | 0.7191980263 | 215,759.41 | 280.40 | 40,913.80 | 2,157.59 | **8,846.14** | 163,561.47 |
| 13 | 0.7043896277 | 211,316.89 | 295.75 | 43,992.11 | 2,113.17 | 8,663.99 | 156,251.87 |
| 14 | 0.6898861362 | 206,965.84 | 310.35 | 46,933.14 | 2,069.66 | 8,485.60 | 149,167.09 |
| 15 | 0.6756812739 | 202,704.38 | 324.23 | 49,741.13 | 2,027.04 | 8,310.88 | 142,301.11 |

The account behind those rows, per contract:

| t | `av_pp` | `mth_deduct_pp` | `surr_chg_pp` | `cv_pp` | `prem_paid_pp` | `db_pp` | `gmdb_claim_pp` |
|---|---|---|---|---|---|---|---|
| 0 | 265,435.59 | 9,097.06 | 830,000.00 | **0.00** | 300,000.00 | 300,000.00 | 34,564.41 |
| 1 | 531,344.02 | 9,167.85 | 830,000.00 | **0.00** | 600,000.00 | 600,000.00 | 68,655.98 |
| 2 | 797,726.13 | 9,238.76 | 830,000.00 | **0.00** | 900,000.00 | 900,000.00 | 102,273.87 |
| **3** | 1,064,582.77 | 9,309.79 | 830,000.00 | **234,582.77** | 1,200,000.00 | 1,200,000.00 | 135,417.23 |
| 4 | 1,331,914.78 | 9,380.95 | 830,000.00 | 501,914.78 | 1,500,000.00 | 1,500,000.00 | 168,085.22 |
| 11 | 3,216,620.89 | 9,882.65 | 711,428.57 | 2,505,192.32 | 3,600,000.00 | 3,600,000.00 | 383,379.11 |
| 12 | 3,487,786.59 | 9,954.83 | 711,428.57 | 2,776,358.02 | 3,900,000.00 | 3,900,000.00 | 412,213.41 |

Three features of these sixteen rows are the product, and each is traced or explained
below.

**`claims_lapse` is nil at t = 0, 1, 2 and ₩5,833.06 at t = 3.** The 해약공제액 of
₩830,000 exceeds the 계약자적립액 for the first three months, and the statutory zero floor
[REG-R19 제7-66조제1항제1호](#krlib-reg-r19) turns the difference into **nothing rather than a debt**.
[S6]'s own illustration shows exactly this: a surrender value of zero at three months on an
account of ₩821,751. It is not a modelling artefact; it is the product, and it is the
single most consumer-visible fact about a Korean front-loaded variable annuity.

**`commissions` falls by a factor of 3.36 at t = 12**, from ₩29,716.92 to ₩8,846.14: the
first-year 1.34% of 보험료총액 giving way to the second-year 0.41% [R1 <표 Ⅴ-3>](#krlib-variable_annuity-r1). The
in-force count falls only 2.7% across the same month, so essentially the whole of the step
is the commission scale.

**`net_cf` is negative in month 0 and only in month 0** across the whole premium-paying
period. The ₩300,000 of premium is met by ₩303,000 of the insurer's own expense and
₩40,200 of commission, so the contract opens **−₩43,227.86**. From month 1 the acquisition
expense is gone and the row is strongly positive; the first twelve months sum to
**+₩2,104,181.53**.

### Hand trace, month 0 — the two deduction points and the first growth

```
Premium, 일반계정
  P(0)                                                     =   300,000.0000000000
  alpha(0) = 0.0517 x 300,000                              =    15,510.0000000000
  beta_1(0) = 0.0350 x 300,000                             =    10,500.0000000000
  gamma(0) = 0.0000 x 300,000                              =         0.0000000000
  prem_charge_pp(0)                                        =    26,010.0000000000
  P_sa(0) = 300,000 − 26,010                               =   273,990.0000000000
  prem_alloc_ratio(0) = 273,990 / 300,000                  =         0.9133

Into the funds at the fixed allocation (BEF_DEDUCT)
  F_1(0, BEF_DEDUCT) = 0 + 273,990 x 0.50                  =   136,995.0000000000
  F_2(0, BEF_DEDUCT) = 0 + 273,990 x 0.50                  =   136,995.0000000000
  AV(0, BEF_DEDUCT)                                        =   273,990.0000000000

월공제액, struck on AV(0, BEF_DEDUCT)
  R(0)   = 0.000080 x 300,000                              =        24.0000000000
  beta_2 = 0 (t < pay_months())                            =         0.0000000000
  c_d(0) = (0.0007 / 12) x 273,990                         =        15.9827500000
  c_a(0) = (0.0025 / 12) x 273,990                         =        57.0812500000
  c_p(0) = (0.0030 / 12) x 36,000,000                      =     9,000.0000000000
  D(0)                                                     =     9,097.0640000000

  AV(0, AFT_DEDUCT) = 273,990 − 9,097.064                  =   264,892.9360000000
  pro rata, both funds equal:  264,892.936 / 2             =   132,446.4680000000
  no de-risking at t = 0, so AFT_DERISK = AFT_DEDUCT

Growth, fund by fund
  (1.03)^(1/12)                                            =         1.0024662697723037
  g_1 = (1.03)^(1/12) x (1 − 0.0040/12)                    =         1.0021321143490463
  g_2 = (1.03)^(1/12) x (1 − 0.0060/12)                    =         1.0019650366374175
  F_1(0) = 132,446.468 x g_1                               =   132,728.8590149033
  F_2(0) = 132,446.468 x g_2                               =   132,706.7301621166
  AV(0)                                                    =   265,435.5891770198

  I(0)   = 264,892.936 x [(1.03)^(1/12) − 1]               =       653.2974409536
  M(0)   = 264,892.936 x (1.03)^(1/12) x 0.0050/12         =       110.6442639337
  check:  264,892.936 + 653.297441 − 110.644264            =   265,435.5891770198  OK

Decrements and benefits
  q(0) = 0.0011138523;  q_mth(0) = 1 − (1 − q)^(1/12)      =         0.0000928684
  d(0) = 1.0 x 0.00009286844533                            =         0.0000928684
  w(0) = 0.28;  w_mth(0) = 1 − (0.72)^(1/12)               =         0.0270040303
  s(0) = (1 − 0.00009286845) x 0.02700403027               =         0.0270015225
  l(1) = 1 − 0.0000928684 − 0.0270015225                   =         0.9729056091

  K_d(0) = 300,000;  DB(0) = Max(265,435.59, 300,000)      =   300,000.0000000000
  C(0)   = min(830,000.00016, 1,643,940) x (7 − 0)/7       =   830,000.0001599999
  CV(0)  = max(0, 265,435.589 − 830,000.000)               =         0.0000000000   <- floor

Cash flow row
  premiums(0)     = 300,000 x 1.0                          =   300,000.0000000000
  claims_death(0) = 300,000 x 0.00009286844533             =        27.8605336001
  claims_lapse(0) = 0.00 x 0.0270015225                    =         0.0000000000
  expenses(0)     = (300,000 + 3,000) x 1.0                =   303,000.0000000000
  commissions(0)  = (0.0134/12) x 36,000,000 x 1.0         =    40,200.0000000000

  net_cf(0) = 300,000 − 27.8605336 − 0 − 303,000 − 40,200  =   −43,227.8605336001
```

**Read the account boundary off that row.** `net_cf_gen(0)` = **−300,818.3366588763** and
`net_cf_sep(0)` = **+257,590.4761252762**; they sum to −43,227.86053360 to within
8.7e−11, which is `check_net_cf_resid(0)`. Both ledgers reconcile line by line, and the
two lines a reader is most likely to put on the wrong side are the 해약공제액 and the
death claim:

```
net_cf_gen(0)  = + premiums(0)                                    300,000.0000000000
                 + av_charges(0)   = D(0) + M(0)                    9,207.7082639337
                 + surr_charges(0) = min(C(0), AV(0)) x s(0)        7,167.1650202870
                 − prem_to_av(0)                                  273,990.0000000000
                 − gmdb_claims(0)  = gmdb_claim_pp(0) x d(0)            3.2099430970
                 − expenses(0)                                    303,000.0000000000
                 − commissions(0)                                  40,200.0000000000
                                                                = −300,818.3366588763

net_cf_sep(0)  = + prem_to_av(0)                                  273,990.0000000000
                 − av_charges(0)                                    9,207.7082639337
                 − surr_charges(0)                                  7,167.1650202870
                 − claims_from_av(0, DEATH) = AV(0) x d(0)             24.6505905031
                                                                = +257,590.4761252762
```

So the 일반계정 received ₩300,000, kept ₩26,010 of front-end charges and sent ₩273,990
across; took back the ₩9,097.06 월공제액 and the ₩110.64 운용보수, and took the
₩7,167.17 of 해약공제액 retained on the month's surrenders — the whole account value of
the surrendering contracts, the charge exceeding it — and paid ₩303,000 of its own
expenses, ₩40,200 of commission and **only the ₩3.21 GMDB top-up** of the ₩27.86 death
claim, the other ₩24.65 being the 계약자적립액 released by the 특별계정. The 특별계정
received ₩273,990 and gave up ₩16,399.52 in the same month, of which ₩9,097.06 was the
월공제액 cancelled before the growth: the ₩264,892.94 that then grew is the account after
that cancellation and before the ₩110.64 운용보수, which is taken **inside** the 기준가격.

### Hand trace, month 3 — where the surrender value clears the floor

The first month in which a surrendering policyholder receives anything, and therefore the
first month with a `claims_lapse` line.

```
Opening
  AV(2)                     = F_1(2) + F_2(2)              = 797,726.1281495993
  F_1(2) = 398,929.0515490024,  F_2(2) = 398,797.0766005968

Premium and transfer
  P_sa(3) = 300,000 − 26,010                               = 273,990.0000000000
  F_1(3, BEF_DEDUCT) = 398,929.0515490024 + 136,995        = 535,924.0515490024
  F_2(3, BEF_DEDUCT) = 398,797.0766005968 + 136,995        = 535,792.0766005968
  AV(3, BEF_DEDUCT)                                        = 1,071,716.1281495993

월공제액
  R(3)   = 24.000000000000004
  c_d(3) = (0.0007/12) x 1,071,716.1281495993              =      62.5167741421
  c_a(3) = (0.0025/12) x 1,071,716.1281495993              =     223.2741933645
  c_p(3) = (0.0030/12) x 36,000,000                        =   9,000.0000000000
  D(3)                                                     =   9,309.7909675066

  AV(3, AFT_DEDUCT) = 1,071,716.1281496 − 9,309.7909675    = 1,062,406.3371820927
  F_1 share = 535,924.0515490024 / 1,071,716.1281495993    =       0.5000615718
  F_1(3, AFT_DEDUCT)                                       = 531,268.5828448085
  F_2(3, AFT_DEDUCT)                                       = 531,137.7543372842

Growth
  F_1(3) = 531,268.5828448085 x 1.0021321143490463         = 532,401.3082134894
  F_2(3) = 531,137.7543372842 x 1.0019650366374175         = 532,181.4594840726
  AV(3)                                                    = 1,064,582.7676975620

Surrender value — the floor releases
  C(3): yrs_completed(3) = (3 + 1) // 12 = 0, so k = 0     = 830,000.0001599999
  CV(3) = max(0, 1,064,582.7676975620 − 830,000.0001600)  = 234,582.7675375621  <- first
  compare CV(2) = max(0, 797,726.128 − 830,000.000) = 0.00

Decrements
  l(3) = 0.9208992552115434
  d(3) = 0.9208992552115434 x 0.00009286844533373806       =       0.0000855225
  s(3) = (0.9208992552115434 − 0.0000855225) x 0.02700403  =       0.0248656819

Cash flow row
  premiums(3)     = 300,000 x 0.9208992552115434           = 276,269.7765634630
  claims_death(3) = 1,200,000 x 0.00008552248214049331     =     102.6269785686
  claims_lapse(3) = 234,582.7675375621 x 0.0248656819141   =   5,833.0604801209
  expenses(3)     = 3,000 x 0.9208992552115434             =   2,762.6977656346
  commissions(3)  = 40,200 x 0.9208992552115434            =  37,020.1500595040

  net_cf(3) = 276,269.7765635 − 102.6269786 − 5,833.0604801
              − 2,762.6977656 − 37,020.1500595              = 230,551.2412796349
```

**The death benefit is ₩1,200,000 and the account is ₩1,064,583**, so the GMDB is in the
money by **₩135,417.23** — and it is in the money at every month up to t = 122 — the
whole premium-paying period and three months beyond it, `gmdb_claim_pp(123)` being the
first zero — because premium at a 91.33% allocation cannot outrun premiums-paid until
compound return has had a decade to work. That is the structural point about a
return-of-premium GMDB on a front-loaded contract: **it is in the money by construction
at short durations**, and its cost is a decreasing function of duration rather than a
random one.

### Hand trace, month 120 — 납입완료, and the deduction that steps *up*

The premium stops and the monthly deduction **rises by 42%**, because the 계약관리비용 for
the period after 납입완료 was collected inside the premium and is now drawn back out of the
fund.

```
Opening
  AV(119)                                                  = 35,813,337.7735828300
  F_1(119) = 17,998,819.2913504020,  F_2(119) = 17,814,518.4822324300

Premium — none
  P(120) = 0 (t = 120 = pay_months());  P_sa(120)          =           0.0000000000
  AV(120, BEF_DEDUCT) = AV(119)                            =  35,813,337.7735828300

월공제액 — three of the five lines have changed since month 0
  R(120)   = risk_prem_rate(50) x 300,000 = 0.000095 x 3e5 =          28.5000000000
  beta_2   = 0.0133 x 300,000        <- steps IN at t = 120 =       3,990.0000000000
  c_d(120) = (0.0007/12) x 35,813,337.7735828              =       2,089.1113701257
  c_a(120) = (0.0025/12) x 35,813,337.7735828              =       7,461.1120361631
  c_p(120) = 0            <- stopped at t = 84 (7 years)   =           0.0000000000
  D(120)                                                   =      13,568.7234062888

  compare D(119) = 24 + 0 + 2,085.3970430603 + 7,447.8465823581
                                                           =       9,557.2436254184
  the step is +4,011.48: beta_2 3,990.00, the age band 4.50, and 16.98 of
  growth in c_d (+3.71) and c_a (+13.27) on a larger account

  AV(120, AFT_DEDUCT)                                      =  35,799,769.0501765460
  F_1(120, AFT_DEDUCT) = 17,992,000.0163041000
  F_2(120, AFT_DEDUCT) = 17,807,769.0338724400

Growth
  F_1(120) = 17,992,000.0163041 x 1.0021321143490463        =  18,030,361.0177069050
  F_2(120) = 17,807,769.0338724 x 1.0019650366374175        =  17,842,761.9524546680
  AV(120)                                                   =  35,873,122.9701615730

Benefits and decrements
  K_d(120) = 36,000,000 (all 120 premiums paid)
  DB(120)  = Max(35,873,122.97, 36,000,000)                 =  36,000,000.0000000000
  gmdb_claim_pp(120) = 36,000,000 − 35,873,122.97           =     126,877.0298384279
  C(120) = 0 (k = 10 >= 7);  CV(120) = AV(120)              =  35,873,122.9701615730
  l(120) = 0.2213584991;  d(120) = 0.0000456065;  s(120) = 0.0015324551

Cash flow row
  premiums(120)                                             =           0.0000000000
  claims_death(120) = 36,000,000 x 0.00004560650207599255   =       1,641.8340747357
  claims_lapse(120) = 35,873,122.9701616 x 0.0015324551487  =      54,973.9519946892
  expenses(120)     = 3,000 x 0.2213584991                  =         664.0754971924
  commissions(120)  = 0 (year 11 > 5)                       =           0.0000000000

  net_cf(120) = −1,641.8340747 − 54,973.9519947 − 664.0754972 = −57,279.8615666174
```

**The statement flips sign here and never comes back.** Month 119 is +₩9,418.79 and month
120 is −₩57,279.86: the premium that carried the row is gone and the surrender stream is
not. Every subsequent month of the deferral is negative, and the account boundary confirms
where the money is — `net_cf_gen(120)` = **+5,640.336569994052** (the 일반계정 still
collects the 월공제액 and the 운용보수 and the retained 해약공제액) and `net_cf_sep(120)` =
**−62,920.198136611405** (the 특별계정 pays out the surrendering and dying accounts and has
no premium coming in).

### Month 204 — the mandatory de-risking bites

At `t = T − 36 = 204`, the first of the three annual 계약해당일 inside the 「연금개시일 −
3년」 window, the 채권형 weight at the `AFT_DEDUCT` timing is **0.5060742578243943** — the
value `bond_weight(203)` also carries, above the 50% ladder floor for a 20-year deferral but
below the 80% the de-risking rule targets [S1]. `bond_weight(204)` is the **post**-transfer
0.8000266764480309.

```
  AV(204, AFT_DEDUCT)                                       =  41,211,386.0778102300
  bond  = F_1(204, AFT_DEDUCT)                              =  20,856,021.6232423860
  target = 0.80 x 41,211,386.0778102                        =  32,969,108.8622481820
  derisk_amount_pp(204) = 32,969,108.8622482 − 20,856,021.6232424
                                                            =  12,113,087.2390057970

  F_1(204, AFT_DERISK) = 20,856,021.6232424 + 12,113,087.2390058
                                                            =  32,969,108.8622481820
  F_2(204, AFT_DERISK) = 20,355,364.4545678 − 12,113,087.2390058
                                                            =   8,242,277.2155620450
  total unchanged                                           =  41,211,386.0778102270
```

Two consequences are visible in the output and neither is decoration. The **운용보수 falls
from ₩17,143.34 to ₩15,148.11** in one month — an 11.6% drop with no change in the account
— because 29.4% of the account, three fifths of the 주식형 balance, has moved from a 0.60%
fund to a 0.40% one. And `bond_weight(t)` stays above 0.80 from here to annuitisation
without any further transfer
(`derisk_amount_pp(216)` and `derisk_amount_pp(228)` are both **0.00**), because the
채권형 carries the lower 운용보수 on the same gross asset return and so **drifts upwards**
on its own. On a path with different returns by fund it would not, and the two later
windows would fire.

### The rows where the product does something

Every event row of the anchor cell's statement, to two decimal places.

| t | event | `pols_if` | `premiums` | `claims_death` | `claims_lapse` | `claims_annuity` | `expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|---|---|
| 0 | issue; acquisition expense | 1.0000000000 | 300,000.00 | 27.86 | 0.00 | 0.00 | 303,000.00 | 40,200.00 | −43,227.86 |
| 3 | 해약환급금 clears the zero floor | 0.9208992552 | 276,269.78 | 102.63 | 5,833.06 | 0.00 | 2,762.70 | 37,020.15 | 230,551.24 |
| 12 | commission steps to year 2 | 0.7191980263 | 215,759.41 | 280.40 | 40,913.80 | 0.00 | 2,157.59 | 8,846.14 | 163,561.47 |
| 83 | last month of the GMAB premium charge | 0.2883626523 | 86,508.80 | 1,072.96 | 54,234.14 | 0.00 | 865.09 | 0.00 | 30,336.61 |
| 84 | **GMAB premium charge stops** (7 years) | 0.2860629838 | 85,818.90 | 1,168.83 | 48,216.27 | 0.00 | 858.19 | 0.00 | 35,575.60 |
| 119 | last premium | 0.2229441583 | 66,883.25 | 1,519.23 | 55,276.40 | 0.00 | 668.83 | 0.00 | 9,418.79 |
| 120 | **납입완료**; deduction steps up | 0.2213584991 | 0.00 | 1,641.83 | 54,973.95 | 0.00 | 664.08 | 0.00 | −57,279.86 |
| 121 | first full post-premium month | 0.2197804374 | 0.00 | 1,630.13 | 54,673.17 | 0.00 | 659.34 | 0.00 | −56,962.64 |
| 203 | before de-risking | 0.1215837337 | 0.00 | 1,744.87 | 34,696.10 | 0.00 | 364.75 | 0.00 | −36,805.73 |
| 204 | **de-risking to 80% 채권형** | 0.1206998103 | 0.00 | 1,897.78 | 34,502.45 | 0.00 | 362.10 | 0.00 | −36,762.34 |
| 239 | last deferral month | 0.0932722265 | 0.00 | 1,866.77 | 28,329.63 | 0.00 | 279.82 | 0.00 | −30,476.22 |
| 240 | **연금개시**; first instalment | 0.0925841296 | 0.00 | 0.00 | 0.00 | **200,728.58** | 277.75 | 0.00 | −201,006.33 |
| 241 | a payout month with no instalment | 0.0925471325 | 0.00 | 0.00 | 0.00 | 0.00 | 277.64 | 0.00 | −277.64 |
| 252 | second instalment, still guaranteed | 0.0921411381 | 0.00 | 0.00 | 0.00 | 200,728.58 | 276.42 | 0.00 | −201,005.00 |
| 348 | **last guaranteed instalment** | 0.0868296734 | 0.00 | 0.00 | 0.00 | 200,728.58 | 260.49 | 0.00 | −200,989.07 |
| 360 | **first life-contingent instalment** | 0.0858776937 | 0.00 | 0.00 | 0.00 | **186,188.58** | 257.63 | 0.00 | −186,446.21 |
| 959 | horizon; `pols_maturity` carries out | 0.0000000917 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | −0.00 |

Four of those rows carry the product's structure.

**t = 84, the GMAB premium charge stops.** The 월공제액 falls from ₩15,422.57 to
₩6,504.62, a **57.8% drop in one month**, because `c_p` is levied 「납입기간(최대 7년)
동안」 [S1] and the seventh year has ended. Nothing else changes: `c_d` and `c_a` rise
smoothly with the account, and the premium keeps arriving for three more years. This is the
single largest discontinuity in the charge stack and it is invisible in any model that
puts guarantee charges on the account value.

**t = 240, annuitisation.** `claims_death` and `claims_lapse` go to zero permanently — the
death cover extinguishes at 연금개시 [R2] and no retrieved document permits surrender of a
종신연금형 — and `claims_annuity` appears. The 특별계정 is emptied: `net_cf_sep(240)` =
**−4,062,956.72108272**, exactly the `av_transfer`, and `net_cf_gen(240)` =
**+3,861,950.3910125117**, the same amount less the instalment and the month's expense.

**t = 241 and every non-anniversary month afterwards** carry nothing but the insurer's own
₩3,000-per-contract maintenance expense, weighted by a slowly falling annuitant count. The
statement is eleven-twelfths empty for sixty years — t = 240 to t = 959.

**t = 360, the 보증기간 ends.** The instalment falls from **₩200,728.58** to
**₩186,188.58**, a **7.24% step**, not because the annuity changed — `annuity_net_pp()` is
the same ₩2,168,066.80 — but because the weight changed from `pols_annuitised()` =
0.09258412964405735, every contract that reached annuitisation, to `pols_if(360)` =
0.08587769374658065, the ones whose annuitant is still alive. Ten years of annuitant
mortality at 보험나이 60–70 is **7.24%** of the cohort.

### The two guarantees at t_ann() = 240

| Quantity | Cells | Value |
|---|---|---|
| 계약자적립액 at T | `av_ann_pp()` | **43,883,943.57329801** |
| 최저연금적립금 strike K(T) | `gmab_base_pp()` | **36,000,000.0** |
| GMAB payoff max(0, K − AV) | `gmab_claim_pp()` | **0.0** |
| 연금재원 | `annuity_fund_pp()` | **43,883,943.57329801** |
| Credited rate at annuitisation | `annuity_int_rate()` | **0.025** |
| Annuity factor, 10년 보증 종신 | `annuity_factor()` | **20.139842488678187** |
| 연금 연액, gross | `annuity_ann_pp()` | **2,178,961.6079652957** |
| 연금수령기간 중 계약관리비용 | `annuity_charge_pp()` | **10,894.80803982648** |
| 연금 연액 actually paid | `annuity_net_pp()` | **2,168,066.7999254693** |
| Contracts reaching T | `pols_annuitised()` | **0.09258412964405735** |

```
  Y     = 43,883,943.57329801 / 20.139842488678187          =  2,178,961.6079652957
  Y_net = 2,178,961.6079652957 x (1 − 0.005)                =  2,168,066.7999254693
  claims_annuity(240) = 2,168,066.7999254693 x 0.09258412964405735
                                                            =    200,728.5776812762
```

**Only 9.26% of contracts reach annuitisation.** That number is the point [R1] makes and
it is the single most important number in this document: against a seven-year persistency
below 30% and 8% ultimate lapse thereafter, **a model treating the GMAB as a floor at every
duration would overstate its cost roughly tenfold.** The guarantee is a European option
struck on one date, void on every earlier exit [S1] [S6] [S7 제50조제3항], and the exit
probability is 90.7%.

**The GMAB finishes out of the money on this path**, so its intrinsic cost is **exactly
zero** while the full ₩657,417.59 of charge is collected. That is **an artefact of the
path, not a finding about the guarantee**, and the gap is a **single-path residual and not
a profit**. `run.py` labels it so and so does this document. Model point 4, on the mandated
−1.00% return, is the counter-example: there the strike bites at **₩10,041,179.61** per
annuitising contract, ₩929,653.88 of expected cost against ₩603,909.13 of charge — **the
charge does not cover the guarantee on the low path.** The statutory 보증준비금 is a
CTE(70) over a thousand scenarios or a standard factor, whichever is greater
[REG-R10] [REG-R26] [R1], and **this model publishes neither**.

### Undiscounted totals

Over t = 0 … 959, income-positive:

```
pols_if            (a sum of counts, not money)      99.6122423885
premiums                                      15,215,257.48
claims_death                                     310,883.37
claims_lapse                                  11,077,101.66
claims_annuity                                 5,759,786.33
claims_maturity                                        0.00
withdrawals                                            0.00
fund_expenses                                          0.00
expenses                                         598,836.73
commissions                                      617,364.10
net_cf                                        −3,148,714.71
```

Guarantee memo lines, undiscounted, from the same run:

```
gmdb_charges  collected                           79,244.38
gmdb_claims   incurred                             4,945.39
gmab_charges  collected                          657,417.59
gmab_claims   incurred                                 0.00
```

Four of those numbers repay a second look.

**`premiums` totals ₩15,215,257.48 against a contractual ₩36,000,000** — **42.26%**. The
whole of the difference is lapse: a contract that pays all 120 premiums pays ₩36,000,000,
and the expected contract pays 42% of that because 78% of the cohort has gone by the last
premium. **That single ratio is the economics of a Korean front-loaded variable annuity**:
the acquisition cost is levied on a premium stream that mostly does not arrive, which is
why the 해약공제 exists and why 감독규정 제7-66조 caps it.

**`claims_lapse` at ₩11,077,101.66 is 72.8% of `premiums`.** Surrender, not death and not
annuity, is what this product mostly pays. The 사망보험금 total of ₩310,883.37 is 2.0% of
premiums and the annuity total of ₩5,759,786.33 is 37.9%, but the annuity is paid to the
9.26% who stay.

**`commissions` totals ₩617,364.10 against 2.39% × ₩36,000,000 = ₩860,400 unweighted** —
71.8%, the in-force weighting of the five-year scale. The 2.39% is the sum of [R1]'s five
per-year means; the same table reports a mean *total* of **2.11%**, and the two differ
because a mean of contract totals is not the sum of per-year means. The model runs the
per-year scale, so the unweighted figure to compare against is 2.39%. `expenses` totals
₩598,836.73, of which ₩300,000 is the day-one acquisition amount, so **more than half of
the insurer's own lifetime expense on this contract falls in month 0**.

**`net_cf` sums to −₩3,148,714.71** and must be negative: undiscounted, the insurer
receives ₩15.2m and pays ₩17.1m of benefits plus ₩1.2m of its own costs over eighty years.
The sign becomes meaningful only when the stream is discounted, which this library does not
do. **`Σ pols_if` = 99.61** is the expected number of contract-months of exposure — 8.3
contract-years — against a 960-month projection: another statement of the same persistency
fact.

### Reading the shape of the result

The statement has **four regions** and each says something about the product.

**Months 0–119, the premium-paying deferral.** Strongly positive after month 0 and falling
on trend, from +₩249,787.95 at t = 1 to +₩9,418.79 at t = 119, because the premium is
weighted by an in-force count that falls from 0.9729 to 0.2229 while the surrender stream
per surviving contract grows with the account. The fall is **not** monotone: the row steps
*up* at t = 12, 24, 36, 48, 60, 72 and 84, the seven policy-year boundaries at which the
annual 해지율 drops a rung and the month's `claims_lapse` falls with it. **The insurer's
positive cash flow is a melting block of ice**, and the melting is lapse.

**Months 120–239, the paid-up deferral.** Uniformly negative, between −₩57,279.86 and
−₩30,476.22, because nothing comes in and the surrender stream is at its largest per
contract. **This is where the 계약관리비용 collected in the premium period is spent**, and
the model shows both halves of that transaction — the money went into the account at
t < 120 and comes back out as `mth_deduct_pp` at t ≥ 120.

**Month 240, the hinge.** ₩4,062,956.72 of 계약자적립액 crosses from the 특별계정 to the
일반계정 in one movement, the death and surrender streams stop dead, and the annuity
starts. **The 특별계정 is empty from here** and the remaining 719 months are a general-
account liability.

**Months 240–959, the payout.** Ten annual instalments of ₩200,728.58 — t = 240, 252, …,
348, the whole 10-year 보증기간 — guaranteed regardless of survival, then a
life-contingent stream falling from ₩186,188.58 with the
annuitant count, and ₩277-and-falling of maintenance expense in every intervening month for
sixty years. The tail is thin and long: `pols_if(959)` is 9.17e−08.

**What the four regions say together** is that this is not one product but two bolted at
month 240 — a front-loaded separate-account savings contract with a 90.7% exit probability,
and a general-account life annuity on the 9.3% who survive it. **The guarantees straddle
the join**: the GMDB is a monthly strip of puts on the first, worth ₩4,945.39 in expected
cost against ₩79,244.38 of charge on this path, and the GMAB is a single European put at
the join itself, worth zero here and ₩929,653.88 on the low path. Neither number is a
valuation, and the 별표 24 CTE(70) that would be is not computed.

### Contrasts across model points

The same anchor cell on four variations, showing which lever moves what:

| Point | Variation | `av_ann_pp()` | `gmab_claim_pp()` | `annuity_net_pp()` | Σ `net_cf` |
|---|---|---|---|---|---|
| 1 | anchor, 투자수익률 2.50% | 43,883,943.5733 | 0.0 | 2,168,066.7999 | −3,148,714.7117 |
| 2 | female | 43,883,943.5733 | 0.0 | **2,006,441.2426** | — |
| 3 | 미보증형 (GMAB off) | **46,722,879.2288** | — | 2,308,323.1589 | −4,033,326.0 |
| 4 | 투자수익률 −1.00% | 25,958,820.3874 | **10,041,179.6126** | 1,778,564.0588 | −192,370.8500 |
| 5 | 투자수익률 3.75% | 52,811,343.3686 | 0.0 | 2,609,121.0337 | −5,173,103.5565 |

**Point 2 has the same account value as point 1 to the last digit.** The 계약자적립액 is a
per-contract quantity and mortality enters only through the *counts* and through the
*annuity factor*: `annuity_factor()` is 20.139842488678187 for the male and
**21.762174205458386** for the female, so the same ₩43,883,943.57 buys **7.45% less annual
income**. That is the whole of the sex effect on this product, and it lands entirely at
t_ann().

**Point 3 quantifies the guarantee's price to the policyholder.** Removing the GMAB and
both its charges raises the terminal account by **₩2,838,935.66** — 6.47% — and the annuity
by the same 6.47%. Over twenty years, 0.25% a year of the fund plus 0.30% a year of
₩36,000,000 for seven years costs the policyholder **about one and a third years' annuity
income**.

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**. Every valuation layer consumes them
and is **cited, not implemented**. On this product one of those layers is not merely
uncomputed but **uncomputable from this run**, and that is stated first.

- **보증준비금 (guarantee reserve) — the one this model cannot produce.** 감독규정
  제6-11조의5 requires a reserve inside retained earnings for expected losses on benefit
  guarantees [REG-R10], and the calculation delegated to 시행세칙 별표 24 is 「사망률,
  해지율, 자산이익률(**1,000개**)을 이용하여 만기까지 장래 예상되는 순손실액을 현가로
  환산한 상위 30% 평균 금액」 — a **CTE(70) over a thousand scenarios** — or a standard
  factor table, **whichever is greater** [R1] [REG-R26]. **The standard factor exists
  precisely because a deterministic number is meaningless.** This model runs one path and
  publishes an intrinsic value; it publishes neither the CTE(70) nor a factor result, and
  the factor tables reproduced in `product-spec.md` are at second hand from [R1] and are
  **[unverified]** against the rule itself [REG-R26]. Note the incentive the factor table
  creates and the model surfaces: it is indexed to 주식비중한도, 「기초서류상 최대
  주식투자 비중을 적용함」, so **a lower equity cap is a lower reserve floor** — which is
  why `check_bond_floor()` is a compliance check and not a housekeeping one.
- **책임준비금, and the 해약환급금준비금 beside it.** 보험업법 제120조 requires the reserve
  and delegates its computation to the FSS Governor [REG-R3]; 감독규정 제6-11조 sets it as a
  current-estimate quantity [REG-R10]. On top of it Korea appropriates a **해약환급금준비금**
  inside retained earnings, to stop a balance sheet distributing earnings the contractual
  surrender-value floor would later demand [REG-R11] — it has no counterpart anywhere else
  in this repository. Here it is **not** inert: the 해약공제액 is ₩830,000 running off over
  seven years and the surrender value is nil for the first three months, so the gap between
  account value and surrender value is real at short durations.
- **계약자적립액 and 해약환급금 are the two quantities this model does compute**, both
  contractual: 감독규정 제7-65조제1항 makes the 계약자적립액 whatever the 산출방법서 says it
  is — and permits an annualized-premium basis at 제7-65조제2항, which this model does not
  use — and 제7-66조제1항 makes the surrender value the 계약자적립액 less the 해약공제액
  floored at zero, with 별표 14's 표준해약공제액 as the cap [REG-R18] [REG-R19] [REG-R20].
  **The 산출방법서 is not public**, so the recursion is [std] and says so.
- **The 특별계정 itself is a statutory construct.** 보험업법 제108조 requires a separate
  account for 변액보험 and 감독규정 제5-6조 and 제5-7조 govern its establishment and the
  movements permitted between it and the 일반계정 [REG-R6] [REG-R15]. `net_cf_gen` and
  `net_cf_sep` are written against that article and `check_net_cf()` asserts they close.
- **K-IFRS 제1117호 and K-ICS have both been in force since 2023-01-01** [REG-R60]
  [REG-R13], so Korea runs an economic-value solvency measure and a CSM-based earnings
  measure together and live. The fulfilment cash flows are this vector with a risk
  adjustment and a CSM layered on. **On a variable annuity the CSM question is sharper than
  elsewhere**, because the fee stack is a stream of charges on a fund and the guarantee is
  an embedded derivative; nothing product-specific to 변액연금 on that treatment was
  retrieved. The 계리가정 guideline's functional form is **[unverified]** at instrument
  level [REG-R27], and **별표 22, the K-ICS shock schedule including the 대량해지 shock,
  was not retrieved** [REG-R26] [unverified].
- **The 공시이율 is not a discount rate.** It appears in this model in exactly one place —
  the annuity factor at `t_ann()` — and it is the **contract's own basis**, not a statement
  about value. Nothing in `result_cf()` is discounted.
- **Professional and supervisory frame.** The work sits under a 선임계리사's verification
  duties at 보험업법 제181조 and 제184조 [REG-R5]; the 기초서류 are filed under 제5조제3호
  with 제128조의2 requiring compliance [REG-R2]; and the 수수료 안내표 this document's
  charge stack reproduces is itself a disclosure obligation [REG-R22] [R2].
- **Policyholder taxation does not enter the insurer's liability cash flows** and is
  specified in `product-spec.md`. Two rules nonetheless show through into the modelled
  mechanics and are cited where they do: the **ten-year cumulative withdrawal limit** in
  `wd_pp`, which is what keeps the 소득세법 시행령 제25조 exemption open, and the
  requirement that a tax-exempt 종신형's guarantee period lie inside the published 기대여명
  [REG-R58].

---

## Key sensitivities and model risks

Dominant assumptions, in order of how far they move the answer.

1. **The return path, and not merely its mean.** It moves the terminal account by a factor
   of two across the three mandated illustration returns — ₩25,958,820 at −1.00%,
   ₩43,883,944 at 2.50%, ₩52,811,343 at 3.75% — and it is the **only** thing that decides
   whether the GMAB pays at all. **Volatility is worth more than drift here** and the model
   has none: `return_scenario.csv` carries a constant per fund, no volatility, no
   correlation and no time series, because **none was retrieved** [R10] [S11]. This is the
   largest single gap in the model and it is structural: a guarantee's cost is a
   distributional quantity and this run is a point.
2. **Lapse, because it decides who is there to be paid.** Only **9.26%** of contracts reach
   annuitisation, so the GMAB's expected cost is nine-tenths a lapse assumption and
   one-tenth an option-pricing problem. The scale's level is calibrated to a single
   second-hand sentence [R1] and its shape is **[std]**. And **the convention is dynamic
   and the model is static** — [R1] states the in-the-moneyness form and publishes no
   parameter — so on precisely the paths where the guarantee matters, the model lets
   contracts leave that would stay. The bias runs one way: **guarantee cost understated**.
3. **The premium-based guarantee charge, because nothing else in the stack behaves like
   it.** ₩9,000 a month on a first-year fund of ₩3.22m is over 3% a year; the same ₩9,000 in
   year seven is under 0.5%; in year eight it is zero. Its base is the 보험료총액 and not
   the fund, its term is the shorter of the 납입기간 and seven years, and it grows with
   추가납입 while the strike it pays for grows further and for longer. Getting any of those
   four facts wrong changes the early-duration cash flow by an order of magnitude.
4. **The mortality basis, which is entirely [std] and rests on two published numbers.**
   The 제10회 경험생명표 is not published [REG-R33] [REG-R34]; both columns of
   `mort_table.csv` are a Makeham law fitted to the 65세 기대여명 of 23.7 and 27.1 years,
   with the insurance basis a **[std]** 25% loading on the force. It drives the GMDB cost
   through the deferral and the **entire** payout liability afterwards — the annuity factor
   is 20.14 for a male and 21.76 for a female on the same fund, a 7.45% swing in income
   from the table alone. Substituting a filed basis is a CSV replacement.
5. **The 해약공제 level, which is a channel choice as much as a number.** Three retrieved
   scales differ by 42% — ₩830,000 [S2], ₩1,077,000 [S5], ₩1,180,000 [S4] — all on the same
   cell and all the same function. The composite takes the lowest, because the surrender
   charge **is** the unamortised 계약체결비용 [R2] and must come from the same carrier as the
   5.17%. The composite is therefore a **cheap tied-channel contract at both ends** and its
   surrender recoveries are correspondingly low; the 2017 market-mean first-year
   해지공제율 of 25.6% of premiums paid [R1 <표 Ⅴ-2>](#krlib-variable_annuity-r1) is
   `C = ₩1,075,200` on the same function, and on it the `surr_charges` total of
   ₩430,510.48 becomes **₩545,164.49 — 26.6% higher**, less than the 29.5% rise in `C`
   because the charge is capped at the account value at short durations.
6. **The insurer's own expense, which is unsourced in its entirety.** ₩300,000 at issue and
   ₩3,000 a month are **[std]** with no inflation, and **no Korean carrier publishes a unit
   cost** — the 사업비 disclosure is of *charges*, not of costs [R2] [S12]. They total
   ₩598,836.73 undiscounted, 3.9% of premiums received, and they are the only line in the
   statement with no document behind it at all.
7. **Discretization, in three places at once.** The account is a **daily** unit ledger
   modelled monthly [S7 제43조]; the 운용보수 is contractually **rate/365 daily** and is
   taken at rate/12; and the two-business-day pricing lag on every switch, withdrawal and
   surrender [S5] [S7 제39조] is absent. Each is small and they compound in one direction on
   a rising path. Changing any one changes the answer, so all three are documented.
8. **Omissions with a stated sign.** 증권거래비용 and 기초펀드 보수 are zero against
   observed ranges of 0.00–0.79% and 0.01–0.45% [S2] [S4], so the modelled drag is
   understated by up to about half a percentage point a year. The 고도재해장해급여금 is
   charged for and never paid. Both run in the insurer's favour, both are stated, and
   neither is large.

### Known modeling pitfalls

These are the specific ways an implementation of **this** product looks right and is wrong.
Each is checkable against the shipped model, and most are already asserted by one of the
eight `check_*()` cells.

1. **Putting the guarantee charges on the account value.** The GMAB charge has **two**
   components on **two different bases**: 0.25% a year of the 계약자적립액 and 0.30% a year
   of the **보험료총액** [S1]. On the anchor cell at t = 0 they are ₩57.08 and ₩9,000.00 —
   a factor of **158**. Collapsing them onto the fund understates month-0 charge income by
   ₩8,942.92 per contract and misstates the whole first-year cash flow.
   *Test:* `gmab_charge_asset_pp(0) == 57.081250000000004` and
   `gmab_charge_prem_pp(0) == 9000.0` on point 1.
2. **Running the premium-based guarantee charge for the whole premium term.** It is levied
   「납입기간(최대 7년) 동안」 [S1] — the *shorter* of the two. On a 10년납 contract it stops
   at t = 84, three years before the premiums do, and the 월공제액 falls 57.8% in that one
   month, from ₩15,422.57 to ₩6,504.62. Running it to t = 120 adds ₩324,000 of undiscounted
   charge per persisting contract that the contract does not permit.
   *Test:* `gmab_charge_prem_pp(83) == 9000.0` and `gmab_charge_prem_pp(84) == 0.0`.
3. **Expecting the monthly deduction to fall at 납입완료.** It **rises**: from ₩9,557.24 at
   t = 119 to ₩13,568.72 at t = 120, because the 계약관리비용 for the period *after*
   납입완료 was collected inside the premium and is now drawn out of the fund [S2]
   [S7 제2조]. A model that stops all charges when premiums stop overstates the account by
   roughly ₩4,000 a month for the remaining ten years.
   *Test:* `mth_deduct_pp(120) > mth_deduct_pp(119)` and
   `maint_charge_after_pp(119) == 0.0`, `maint_charge_after_pp(120) == 3990.0`.
4. **Letting the front-end charges reach the 특별계정.** 계약체결비용, 납입 중 계약관리비용
   and 기타비용 are deducted **from the premium in the 일반계정** and never enter the fund
   [S7 제2조]; only the 월공제액 and the 운용보수 come out of the account. Conflating the
   two deduction points either double-charges the fund or gives it ₩26,010 a month it never
   receives. The observable is the allocation ratio: **0.9133**, against 91.3%, 91.3% and
   91.4% published on this cell [S1] [S2] [S6].
   *Test:* `check_prem_alloc()`, and `prem_alloc_ratio(0) == 0.9133`.
5. **Treating the 운용보수 as a unit cancellation.** It is deducted inside the 기준가격,
   out of net assets before the unit price is struck [S7 제43조제2호], so it is a **factor on
   the growth** and not a deduction from the account. Modelled as a cancellation it would
   change the base every other charge is struck on. The identity that separates them is
   `I(t) − M(t) = AV(t) − AV(t, AFT_DERISK)`.
   *Test:* `check_charge_split()` on every model point, and `mgmt_fee_pp(0) ==
   110.64426393373063`.
6. **Treating the GMAB as a floor on the account at every duration.** It is a **European
   option struck on one date**, void on 해지, on death before T and on 조기연금개시
   [S1] [S6] [S7 제50조제3항] [R1]. Weighting it by `pols_if(t)` at every t rather than by
   `pols_annuitised()` at T alone overstates its cost by the whole 90.74% pre-annuitisation
   exit probability — **roughly tenfold** on this cell.
   *Test:* `pols_annuitised() == 0.09258412964405735` and `gmab_claims(t) == 0.0` for every
   `t != t_ann()`.
7. **Reading the GMAB residual as profit.** ₩657,417.59 of charge is collected against
   ₩0.00 of intrinsic cost on the base path. That is **a single-path residual**: the option
   was written, the path finished out of the money, and by Jensen's inequality the
   intrinsic value is a *lower bound* on the expected cost. Model point 4 is the
   counter-example — ₩929,653.88 of cost against ₩603,909.13 of charge on the mandated
   −1.00% return.
   *Test:* on point 1, `gmab_claim_pp() == 0.0`; on point 4,
   `gmab_claim_pp() == 10041179.61262558`.
8. **Netting the GMDB and paying only the excess.** The death benefit is
   Max[계약자적립액, 이미 납입한 보험료] and it splits **exactly** into the account value
   released from the 특별계정 and the top-up met from the 일반계정 보증준비금 [R2].
   Projecting only the top-up as the claim understates gross benefit outgo by the whole
   account value; projecting both double-counts.
   *Test:* `check_gmdb_floor()`, and `claims_death(0) == 27.860533600121418` against
   `gmdb_claims(0) = gmdb_claim_pp(0) x pols_death(0)`.
9. **Forgetting the statutory zero floor on the surrender value.** `cv_pp` is
   **max(0, AV − C)** [REG-R19 제7-66조제1항제1호](#krlib-reg-r19). Without the floor the first three months
   produce a *negative* surrender value — −₩564,564.41 at t = 0 — which a naive model would
   book as income. `claims_lapse` is 0.00 at t = 0, 1 and 2 and ₩5,833.06 at t = 3, and
   [S6] publishes exactly this shape.
   *Test:* `cv_pp(2) == 0.0`, `cv_pp(3) == 234582.76753756206`.
10. **Running the 해약공제 off linearly in the *ratio* instead of the *amount*.** All three
    retrieved scales are `C × (7 − k) ÷ 7` in the **amount** [S2] [S4] [S5]; the published
    ratio falls far faster only because its denominator is growing. A ratio-linear run-off
    over-recovers at every duration but the first.
    *Test:* the nine values of `surr_chg_pp(12k)` above, to the won.
11. **Ignoring the 표준해약공제액 cap because it does not bind on the anchor.** It is
    ₩1,643,940 against a level charge of ₩830,000, so it is invisible on point 1 — and it
    **binds exactly** on points 6, 7 and 10, all 5년납, where the scaled charge would
    otherwise exceed it (point 6: ₩1,369,950 charge against a ₩1,369,950 cap).
    *Test:* `check_surr_chg_cap()` on all ten points, and
    `surr_chg_pp(0) == surr_chg_cap_pp()` on points 6, 7 and 10.
12. **Using `pols_if(t)` as the annuity payment weight inside the 보증기간.** The instalment
    is owed to every contract that annuitised, alive or not, for ten years
    [S2] [S5]. `pols_annuity_oblig(348) = 0.09258412964405735` while
    `pols_if(348) = 0.08682967335056192` — a **6.6%** difference on the last guaranteed
    instalment, and the step at t = 360 from ₩200,728.58 to ₩186,188.58 is the whole of the
    guarantee's value showing up at once.
    *Test:* `pols_annuity_oblig(348) == pols_annuitised()` and
    `pols_annuity_oblig(360) == pols_if(360)`.
13. **Keeping the death benefit or the surrender value alive after 연금개시.** Both stop:
    the cover extinguishes at 연금개시 [R2] and no retrieved document permits surrender of a
    종신연금형. `claims_death(t)` and `claims_lapse(t)` are **0.00 for every t ≥ 240**.
    *Test:* `claims(240, "DEATH") == 0.0` and `lapse_rate(240) == 0.0`.
14. **Using one mortality table across the join.** Korea prices the deferral on the
    보험사망률 and the payout on a separate, lighter 연금사망률, and neither is public
    [REG-R34]. `mort_rate(239) = 0.0054591503` and `mort_rate(240) = 0.0047847455` — a
    **12.35% fall across one month** that is a change of table, not of risk. Using the
    annuitant basis through the deferral understates the GMDB cost; using the insurance
    basis in the payout understates the annuity.
    *Test:* both values on point 1, and `mort_rate_at_age(60) != ann_mort_rate_at_age(60)`.
15. **Reading `proj_len()` as the last row index.** It is the **number of projected
    months**, the frame's exclusive end: the frame is `range(proj_len())` and the last row
    is `proj_len() − 1`. The anchor has **960** rows, 0 … 959, and `(120 − 40) × 12 = 960`.
    An off-by-one either drops the horizon month, in which `pols_maturity` carries out the
    survivors and the in-force roll-forward closes, or adds a phantom row past it.
    *Test:* `len(result_cf()) == proj_len()` and `result_cf().index[-1] == proj_len() − 1`
    on every model point, and `check_pols_roll_fwd()`.
16. **Reversing the decrement order, or applying both rates to the opening count.** Death
    is taken first and 해지 on the survivors [std]: `s(0) = (1 − d_rate) × w_mth`, not
    `l(0) × w_mth`. The difference is second-order in a month and first-order over 240 of
    them.
    *Test:* `pols_lapse(0) == 0.02700152245035668` against
    `pols_if(0) * lapse_rate_mth(0) == 0.027004030272665847`.
17. **Striking the asset-based guarantee charges before the premium goes in.** They are
    struck on `av_pp_at(t, "BEF_DEDUCT")`, **after** the transfer. At t = 0 that is the
    difference between charging on ₩273,990 and charging on zero — `gmdb_charge_pp(0)`
    would be 0.00 instead of ₩15.98, and the month-0 account would be wrong by the
    difference.
    *Test:* `gmdb_charge_pp(0) == 15.98275` and `av_pp_at(0, "BEF_PREM") == 0.0`.
18. **Forgetting the mandatory 채권형 ladder, or applying the wrong rung.** It is by
    **연금개시 전 보험기간**, not by fund choice: <12년 ≥80%, =12년 ≥70%, >12년 ≥50%
    [S1] [R1]. The anchor's 20-year deferral takes the 50% rung; points 6 and 7 take 80%
    and 70%. It binds both the premium allocation and the account mix and survives every
    later 펀드변경, and the insurer's own reserve floor is indexed to the equity cap
    [R1] [REG-R26].
    *Test:* `check_bond_floor()` on all ten points, and `bond_floor()` = 0.50 / 0.80 / 0.70
    on points 1, 6 and 7.
19. **Skipping the pre-annuitisation de-risking, or applying it at the wrong times.** It
    fires at the three annual 계약해당일 inside 「개시일 − 3년」 — t = 204, 216, 228 on the
    anchor — tops the 채권형 to **80%**, and **conserves the total** [S1]. On the anchor it
    moves ₩12,113,087.24 at t = 204 and nothing afterwards, because the bond fund's lower
    운용보수 keeps the weight above 80% on its own.
    *Test:* `derisk_amount_pp(204) == 12113087.239005797`, `derisk_amount_pp(216) == 0.0`,
    and `check_av_roll_fwd()` — which would break if the transfer did not conserve.
20. **Failing to re-base the guarantee strikes on a 중도인출.** 이미 납입한 보험료 is
    reduced **proportionally**, by (AV − W) ÷ AV [S2] [S7 제51조제8항], and it is the strike
    of **both** guarantees. Without it a policyholder withdraws the fund and keeps the
    strike. On point 9 the strike falls from a contractual ₩48,000,000 to **₩25,509,168**.
    *Test:* `gmab_base_pp() == 25509167.99999999` on point 9.
21. **Publishing a `claims` column beside the `claims_*` columns.** The house rule is that
    the columns of `result_cf()` sum to `net_cf`; a subtotal beside its parts breaks that
    and silently double-counts in any downstream aggregation. The `claims(t, kind)` cells
    stays.
    *Test:* `"claims" not in result_cf().columns` and the column sum identity.
22. **Reading `net_cf` as including investment return.** It does not: this library projects
    **gross liability cash flows** and the separate-account return is an asset-side
    quantity. `inv_income_pp` and `mgmt_fee_pp` exist and are not columns. A reader who
    adds them gets a number that is neither a liability cash flow nor a profit.
    *Test:* `"inv_income" not in result_cf().columns`; `check_net_cf()`.
23. **Treating `charge_income(t)` as revenue.** Most of it is an **internal transfer**
    between the two accounts, and adding it to `premiums` counts the same money twice. It
    is a memo cells and the docstring says so; the external cash flow is `net_cf`.
    *Test:* `check_net_cf()`, which would fail if any transfer reached `net_cf`.
24. **Running the model on 만나이.** Every table, every model point age and the whole rate
    card are **보험나이** [REG-R25 제21조](#krlib-reg-r25); the 완전생명표 and every Korean
    population statistic are 만나이 [REG-R38] [REG-R39]. The six-month rule makes the two
    differ for half of all issue dates, so the error is worth about half a year of ageing on
    every row and **raises nothing**.
    *Test:* the registry metadata records the basis per model and the conventions suite
    reads it.
25. **Presenting `mort_table.csv` as the 경험생명표.** It is a **[std]** Makeham
    construction on two published life expectancies, and the 제10회 경험생명표 is not
    published [REG-R33] [REG-R34]. Every row of the CSV carries a `provenance` cell that
    says so.
    *Test:* the `provenance` column is non-empty on every row of every CSV, and the
    conventions suite asserts it.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-variable_annuity-r1
[R10]: #krlib-variable_annuity-r10
[R2]: #krlib-variable_annuity-r2
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R15]: #krlib-reg-r15
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R24]: #krlib-reg-r24
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R3]: #krlib-reg-r3
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R58]: #krlib-reg-r58
[REG-R6]: #krlib-reg-r6
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
