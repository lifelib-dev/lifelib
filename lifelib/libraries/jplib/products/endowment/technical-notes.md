# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite of `product-spec.md` (same
directory) — endowment assurance (*yōrō hoken*, 養老保険) as the first cell and educational
endowment (*gakushi hoken*, 学資保険) as the second — into a reference liability cash-flow
projection on paper. This is not any single insurer's product. [S#] and [R#] tags resolve
against `sources.md`, whose numbering is carried verbatim from `_research/endowment.md` and
is frozen; [REG-R#] tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct.
**[std]** marks a standardization introduced for the reference implementation; [unverified]
marks a claim that could not be confirmed against a retrieved document. **Every parameter
value here is identical to `product-spec.md`'s.** Eleven parameters appear here that the
specification does not name, and every one of them is internal to a construction the
specification defers to this document (its footnotes 6 and 21): the cash-value basis rate
`i_cv`, the acquisition-deduction rate `α`, the mortality multiplier `mort_be_factor`,
the waiver
loading `wv_load`, the waiver-qualification fraction `wv_frac`, the waived-state surrender
multiplier `wv_lapse_mult`, the surrender-rate table, the premium-default table, the
dynamic-surrender sensitivity `β`, the expense and commission scale, and the reference
valuation rate `i_std`. Each is **[std]** and each is derived, not asserted, below.

**This product states deltas against the savings chassis.** The policy value (*hokenryō
tsumitatekin*, 保険料積立金), surrender value (*kaiyaku-henreikin*, 解約返戻金), policy loan
(*keiyakusha kashitsuke*, 契約者貸付), automatic premium loan (*jidō furikae kashitsuke*,
自動振替貸付, APL), grace (*yūyo kikan*, 猶予期間), lapse (*shikkō*, 失効), reinstatement (*fukkatsu*, 復活)
and reduction of the sum assured (*gengaku*, 減額) machinery is specified once,
in [whole life technical notes (終身保険)](../whole_life/technical-notes.md), and is **not restated here**.
Four things are genuinely this product's and are given full treatment: a **finite term with
a 満期保険金** (*manki hokenkin*, maturity benefit) equal to the death benefit, which turns
the policy-value roll-forward into a real check; a **staged 学資金**
(*gakushikin*, education money) schedule that is data rather than formula; a death payment
(*shibō kyūfukin*, **死亡給付金**) that is a return of premiums rather than a sum assured;
and waiver of premium (*hokenryō haraikomi menjo*, **保険料払込免除**) on the policyholder
(*keiyakusha*, 契約者) — **a second decrement on a second life who is not the 被保険者**
(*hihokensha*, the insured). That last has no analogue in `uslib` or `uklib`.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  death claims, staged survival benefits, the maturity benefit, surrender benefits, expenses
  and commission — for a single-policy model point, in the sense the ESR current estimate
  (*genzai suikei*, 現在推計) requires: probability-weighted future cash flows on assumptions
  re-set at each 基準日 [REG-R15]. They are gross of reinsurance, which is a scope choice of
  this library and not a requirement of that entry. It is also the shape the appointed actuary
  (*hoken keirinin*, 保険計理人) 1号収支分析 consumes — a forward income-and-outgo projection over
  at least ten future years by product segment, re-runnable under prescribed scenarios
  [REG-R6] [REG-R22]. **Discounting, MOCE, required capital and every statutory reserve are
  out of scope** and are cited, not reproduced (see Valuation and reserve pointers).
- **Time index — three of them, and they are not the same.** The projection index `t` is
  **0-based and counts policy months**: `t = 0` is the first policy month and `t = 12n − 1`
  the last, `proj_len` is the **number** of projected months so the frame is
  `t = 0 … proj_len − 1`, and the contractual **policy year is the 1-based label
  `y(t) = 1 + ⌊t/12⌋`** with `duration(t) = ⌊t/12⌋` beside it. Month `t` runs from time `t`
  to time `t + 1`; flows at the start of the month fall at `t` and flows at its end at
  `t + 1`.
  Beside it runs the **anniversary** index `k`, **in years**, with `k = 0` at issue:
  everything that is a *value at a point in time* rather than a *flow during a period* is
  indexed by `k` — `W(k)`, `Wb(k)`, `SC(k)`, `V(k)`, `CV(k)`, `g(k)`, `G(k)`, `EPV(k)`, the
  loan balance `L(k)` and cumulative premiums `P × min(k, m)` — and **none of those numbers
  moved** when the projection index became a month. `SC(0)` is the deduction at issue and
  `W(n) = S` the value at maturity, as before.
  A benefit falling **between** two anniversaries reads the value at the elapsed month `u`
  instead, by **linear interpolation [std]** — from the value *after* the staged benefit at
  one anniversary to the value *before* the one at the next, which is the curve the contract
  traces. The 算出方法書 that would state the real within-year rule is a 基礎書類 filed with the
  金融庁 and is not published [REG-R2].
- **Projection frequency.** **Monthly**, on policy months (`Endowment_JP_S`). The contract is
  quoted in years — the term, the 保険料払込期間, the staged grid and the lapse curve are all
  annual — so the monthly step is finer than the guarantees rather than finer than the
  product. Three things follow. The **年払 premium** falls in one month out of twelve instead
  of being smeared across a year. Every payment that is a payment **on a date** — each 学資金,
  the 満期保険金 — falls in the single month whose end is that date, so the maturity payment is
  one month wide rather than one year. And the **final-period surrender carve-out** shrinks
  from a policy year to a month, which moves the maturing fraction.
  The only intra-year contractual structure on the composite is the calendar date of each
  学資金 — the 11月1日 following a stated attained age at the adopted carrier [S10], and four
  other fixed dates elsewhere [S1] [S3] [S7] [S13] — and the model still resolves every one
  of them to the policy anniversary following that age (`product-spec.md` footnote 13). No
  amount changes; the timing of each staged payment moves by between one and five months,
  always forward, always inside one policy year. The monthly grid does not fix that, because
  the model point table carries no calendar date to fix it with; what it does is make the
  approximation *visible*, since a staged payment now occupies one month and the months it
  might have occupied instead are rows a reader can point at.
- **Timing conventions [std].** Premium at the **start** of the anniversary months
  `t = 0, 12, …, 12(m − 1)`, in advance, and zero in the eleven months between each pair;
  maintenance expense at the start of each month, a twelfth of the annual amount, inflating
  once a policy year; renewal commission with the premium it is a percentage of; acquisition
  expense and initial commission at issue (the start of month `t = 0`); death claims and
  claim expenses at the **end** of the month of death; the 学資金 and the 満期保険金 at the
  **end** of the single month whose closing instant is the anniversary they fall on, to
  policies surviving that month's mortality; surrenders at the end of the month, **after**
  deaths and **after** any staged benefit just paid, valued on the surrender value net of it.
- **Rate conversion [std].** Both mortality decrements — the 被保険者's and the 契約者's — and
  voluntary surrender are quoted per annum and applied per month on the **effective**
  convention `r_m = 1 − (1 − r)^(1/12)`, so twelve months compound back to the annual rate
  exactly. The premium-default proportion that feeds the APL is **not** converted: it is the
  failure to pay one premium on one date, and is applied once per premium.
- **Age basis — two ages, not one.** 契約年齢 is attained age (*man-nenrei*, 満年齢) with the
  fractional year discarded at 契約日, incrementing on each 年単位の契約応当日 rather than on the
  birthday [S1] [S2] [S10] [S13]. The attained age of the 被保険者 in month `t` is therefore
  `x + ⌊t/12⌋` exactly, stepping on the anniversary. **On the 学資 cell there is a second
  age**, the 契約者's `y + ⌊t/12⌋`, which runs an entirely separate decrement over the months
  `t = 0 … 12m − 1` only. Both model cells sit at exact
  integer ages at issue, so the four different 満年齢 rounding rules in the composite do not
  bind on either [S1] [S2] [S10] [S13]. **The table does not share this basis**:
  生保標準生命表2018（死亡保険用）is built for a nearest-birthday (*hoken-nenrei hōshiki*, 保険年齢方式)
  basis [REG-R20]. The reference
  implementation reads it at the 満年齢 attained age with no adjustment **[std]**, as the
  chassis does, and the resulting understatement of up to half a year of age is named here,
  not hidden.
- **Currency.** JPY throughout, written ¥ with thousands separators. There is no currency
  layer on this product.
- **Model points.** Single-policy model points on an expected (probability-weighted) basis:
  survivorship multiplies per-policy cash flows. `point_id` parameterizes `Projection`;
  `point_id = 1` is the 養老 worked-example anchor cell and `point_id = 2` is the 学資 cell. No
  aggregation logic is specified here.
- **Termination — the sharpest delta from the chassis.** There is no tail and no terminal
  age. The projection length is exactly the 保険期間: `12n` months, `t = 0 … 12n − 1`. Every
  state closes at the end of the last one, `l(12n) = 0`, and the closing cash flow is a
  **certain payment of `S` to the survivors** at anniversary `n`, which is the close of the
  final month — not a decrement. The chassis runs to the table's terminal age ω because a 終身保険 has no expiry;
  importing ω here would project a contract that has already matured.
- **Contract boundary.** The premium is level and guaranteed for the whole of 保険料払込期間 with
  no unilateral repricing right in any retrieved 約款 [S1] [S2] [S8] [S10], so all `m` years
  of premium and all `n` years of benefit are inside any defensible boundary. Japan's ESR 柱1
  告示 were not opened in the research pass and their boundary text is [unverified] [REG-R16];
  the model implements no boundary test, projects the whole contract, and says so.
- **Rounding.** Intermediate values at full precision; displayed cash flows to **two decimal
  places [std]** and in-force probabilities to **six [std]**, which is the precision the
  tests assert.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) | Second cell (`point_id = 2`) |
|---|---|---|---|
| `policy_id` | str | `EN-JP-0001` | `EN-JP-0002` |
| `cell` | enum {endowment, education} | endowment | education |
| `sex` | enum {M, F} | M | M |
| `issue_age` (`x`) | int, 満年齢 — the 被保険者 | 30 | 0 |
| `ph_issue_age` (`y`) | int, 満年齢 — the 契約者; unused on the 養老 cell | — | 30 |
| `ph_sex` | enum {M, F} | — | M |
| `sum_assured` (`S`) | JPY — 基準保険金額 | 5,000,000 | 1,000,000 |
| `policy_term` (`n`) | int years | 30 | 22 |
| `prem_term` (`m`) | int years, `m ≤ n` | 30 | 17 |
| `premium_annual` (`P`) | JPY, level for years 1 … `m` | 181,140 | 108,564 |
| `schedule_id` | str — key into `benefit_schedule_table.csv` | `none` | `S_0_1` |
| `waiver` | bool — 保険料払込免除 on the 契約者 | false | true |
| `apl_elected` | bool — 自動振替貸付 elected (default on) | true | true |
| `pol_loan_util` | fraction of `cv_pp` drawn as 契約者貸付 | 0.00 | 0.00 |
| `dividend_type` | enum {none, five\_year} | none | none |
| `apl_default_mult` | multiplier on `default_rate(t)`; 0 switches the APL module off | 0.00 | 0.00 |
| `dyn_lapse` | bool — dynamic-surrender module | false | false |
| `mort_adj`, `wv_load`, `wv_frac`, `wv_lapse_mult` | the four class-(c) multipliers, carried per point; the `mort_adj` column is read by the `mort_be_factor()` cells | 1.00 | 1.00 |

**Both annual premiums are sourced, not constructed.** ¥15,095 per month for exactly the
anchor cell — 契約年齢 30, 満期 60, 保険金額 ¥5,000,000, male, contracts dated on or after 2025-01-02
— is published [S9], and ¥9,047 per month for exactly the second cell — 契約者 30 male, child
0, 22歳満期, 17-year paying period, 満期保険金 ¥1,000,000, S型 — is published with its total premiums
and receipts [S11]. The annual figure is 12 × the monthly one **[std]** (`product-spec.md`
footnote 5): 12 × ¥15,095 = ¥181,140 and 12 × ¥9,047 = ¥108,564, the latter reconciling to
the published ¥1,845,588 of total premiums over 17 years exactly [S11]. No carrier publishes
an annual-mode scale, so the modal discount a real 年払 rate would carry is not applied and
both annual premiums are slightly **overstated**. The direction matters more here than on
the chassis, because the number this product is sold on moves with it: one carrier states
plainly that paying in larger blocks lowers total premiums and raises the return ratio
(*henreiritsu*, 返戻率) [S16], and the highest published ratio in the research set,
129.2%, is quoted on a 一括払込 basis [S14]. The composite's premium is a 月払 one, so the
model's derived 返戻率 is a **monthly-basis ratio** and sits below a true 年払 figure. The
monthly projection grid does not change that: the grid is when the model looks, the payment
frequency is what the 契約者 chose, and the two are independent.

`schedule_id = none` on the 養老 cell is a product fact, not a missing value: the survival
benefit is a single payment at anniversary `k = n` and there is no staged schedule at all.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
The first block runs on the **monthly** index `t`; the second on the **anniversary** index
`k`, in years; the third reads the second at an elapsed month `u`.

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | **Total** in-force probability at the start of month t, `pols_if = pols_if_pay + pols_wv`; `pols_if(0) = 1` | sum of the two states |
| `pols_if_pay(t)` | In-force probability in the **premium-paying** state at the start of month t; `pols_if_pay(0) = 1` | monthly recursion |
| `pols_wv(t)` | In-force probability in the **waived** state at the start of month t; `pols_wv(0) = 0`; identically 0 on the 養老 cell | monthly recursion |
| `mort_rate(t)` | 被保険者 annual mortality (incl. 高度障害) applying in month t | table lookup at `x + ⌊t/12⌋` |
| `mort_rate_mth(t)` | The same rate per month, `1 − (1 − q)^(1/12)` | conversion **[std]** |
| `mort_rate_ph(t)` | 契約者 annual mortality driving the waiver, `t < 12m` only; 0 on the 養老 cell | table lookup at `y + ⌊t/12⌋` |
| `mort_rate_ph_mth(t)` | The same rate per month | conversion **[std]** |
| `lapse_rate(t)` | Annual voluntary surrender rate applying in month t | assumption table, at policy year `1 + ⌊t/12⌋` |
| `lapse_rate_mth(t)` | The same rate per month | conversion **[std]** |
| `default_rate(t)` | Premium-default proportion feeding the APL module (0 in base); **not** converted, and zero outside anniversary months | assumption table, at policy year `1 + ⌊t/12⌋` |

| Variable | Description | Updated |
|---|---|---|
| `benefit_pct(k)` | `g(k)` — the staged benefit due at anniversary k, as a fraction of `S` | schedule table |
| `prem_cum_pp(k)` | `P × min(k, m)` — cumulative premiums due over the first k policy years | closed form |
| `pol_val_pp(k)` | `W(k)` — policy value at anniversary k, **after** any staged benefit due at k | closed form |
| `pol_val_pre_pp(k)` | `Wb(k) = W(k) + S × g(k)` — the same value **before** that benefit | closed form |
| `surr_charge_pp(k)` | `SC(k)` — the acquisition deduction embedded in the surrender value | closed form |
| `cv_pp(k)` | `CV(k)` — payable 解約返戻金 at anniversary k | closed form |
| `reserve_pp(k)` | 平準純保険料式 policy reserve, reference quantity only — **never a cash flow** | closed form |
| `loan_pp(k)` | Outstanding APL + 契約者貸付 principal and interest at anniversary k | annual recursion |

| Variable | Description | Updated |
|---|---|---|
| `prem_cum_pp_m(u)` | `P × min(⌈u/12⌉, m)` — premiums actually **due** by elapsed month u | step function |
| `pol_val_pre_at_m(u)` | `Wb(u)` — policy value at elapsed month u, before any staged benefit due at u | interpolation **[std]** |
| `pol_val_at_m(u)` | `W(u)` — the same value after it | `Wb(u) − S × g(u/12)` at anniversaries |
| `surr_charge_at_m(u)` | `SC(u)` — the deduction at elapsed month u | the same linear schedule, read finely |
| `cv_at_m(u)` | `CV(u)` — payable 解約返戻金 at elapsed month u | `max(W(u) − SC(u), 0)` |

The anniversary family is read at `k = ⌊t/12⌋ + 1` by the flows of the **anniversary months** —
the closing value of the policy year — and `result_val()` therefore publishes one row per
anniversary `k`, not one per projection row. The `*_at_m` family is read at `u = t + 1`, the
closing instant of month `t`, by every flow in between; at `u = 12k` the two agree by
construction, which `check_staged_value` asserts.

The base run carries no loan and no APL cohort: `default_rate ≡ 0` and `pol_loan_util = 0`,
so `loan_pp ≡ 0` and every benefit is gross. The APL triangle, its exhaustion test and its
clawback are the chassis's and are exercised in both positions there.

**There is no `low_cv` and no suppression multiplier** (the chassis calls it `k`; `k` here
is the anniversary index in years and nothing else). No retrieved document offers a suppressed-surrender-value
(*tei-kaiyaku-henreikin-gata*, 低解約返戻金型) form of either product; the one
appearance of the term in the research set is on a different product group in a pricing
release [S9]. The chassis's signature mechanic — the cliff at 払込満了 and the surrender spike
on it — is **absent by construction here**, and so is the lapse-rate spike that goes with
it.

---

## Assumption inputs

Three classes, kept apart on purpose. The split is not a modelling nicety on this product:
the 返戻率 an insurer advertises is a ratio of guaranteed receipts to guaranteed premiums on a
無配当 design [S13] [S16] but a partly non-guaranteed one on a 有配当 design [S1] [S6] [S10], and
presenting a non-guaranteed element as certain is 断定的判断の提供 under 消費者契約法第4条 [REG-R38].

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| 死亡保険金 — 養老 cell | `S`, level for the term, net of loans and unpaid premiums | [S2] [S8] |
| 満期保険金 — 養老 cell | `S` on survival to anniversary `n`, **equal to the death benefit** | [R10] [S2] [S8] |
| 高度障害 / 重度障害 — 養老 cell | Deemed death on the notice date; no separate payment | [S2] [S15] |
| Premium `P` | Level and guaranteed for years 1 … `m`; none thereafter | [S1] [S2] [S8] [S10] |
| Staged 学資金 `g(k)` | 5% / 5% / 10% / 10% / 70% / 10% of `S` at anniversaries `k` = 3 / 6 / 12 / 15 / 18 / 20 | [S10] [S11]; grid **[std]**, timing **[std]** |
| 満期保険金 — 学資 cell | `S` at anniversary `k = n = 22`; total receipts 210% of `S` | [S10] [S11] |
| 死亡給付金 — 学資 cell | `max(cumulative premiums − 学資金 already paid − loans, 積立金)` | [S3] [S13]; form **[std]** |
| 保険料払込免除 trigger | The 契約者's death, 高度障害, or 身体障害 from a listed accident within 180 days, during 保険料払込期間 | [S1] [S10] [S16] |
| What the waiver promises | Every benefit paid in full **and each future premium treated as paid on its 契約応当日** | [S1] [S10] [S13] |
| Waiver carve-outs | 3-year suicide of the 契約者; the 後継保険契約者's intentional act; war — each **terminating** the contract against the policy reserve (*sekinin-junbikin*, 責任準備金) | [S1] [S3] [S7] [S10] |
| 解約返戻金 arguments | Elapsed months, capped at paid months, **and the timing of the 学資金 payments** | [S1] [S2] [S10] |
| 解約返戻金 constraints | Below cumulative premiums; capped at the death benefit; reduced by each 祝金 | [S7] |
| 免責 — suicide of the 被保険者 | 3 years from the 責任開始の日, paying the 積立金 or 責任準備金 rather than nothing | [S2] [S8]; frame [REG-R34] |
| Contestability (告知義務違反) | 2 years from the 責任開始期, on the 契約者's disclosure as well as the 被保険者's | [S1] [S6]; ceiling [REG-R35] |
| Policyholder protection | 90% of the 責任準備金 on insurer failure | [REG-R40] [REG-R41] |

### (b) Insurer-discretionary current elements

| Input | Snapshot value | Basis |
|---|---|---|
| Assumed interest rate — the pricing rate (*yotei riritsu*, 予定利率) | **1.00% p.a. on both cells**, for contracts dated on or after 2025-01-02 (学資保険 0.85% → 1.00%; 養老保険（一時払を除く）0.60% → 1.00%) | [S9]; adoption **[std]** |
| Cash-value basis rate `i_cv` | **1.00% p.a.** — the 予定利率 above, adopted directly | [S9]; adoption **[std]**, below |
| Acquisition deduction `α` | **0.25 of one annual premium**, grading linearly to zero at `m` | **[std]**, below |
| APL / 契約者貸付 interest `i_L` | **2.40% p.a.**, compound, held flat — a named **deviation** from the chassis's 2.75%, below | [S9]; ceilings 年8% / 半年4% [S1] [S10] |
| 契約者配当 | None — the composite is 無配当. The ５年ごと配当 variant is specified and **not implemented**: `dividend_type` is an attribute and the value is rejected by name | [S13] [S16]; variant [S1] [S10]; frame [REG-R9] |
| Deferral of paid 学資金 | Not modelled: each 学資金 is paid on its due date at a rate no document publishes | [S1] [S10] [S13]; scope **[std]** |
| 払済保険 / 学資年金 commutation | Not modelled in the base run; both need an unpublished company basis | [S7] [S10] |
| 減額 | Universal and specified in `product-spec.md`, **not modelled**: it is the chassis's mechanic, and on the 学資 cell it re-scales the whole staged grid because every payment is a percentage of 基準保険金額. One carrier refuses it once the 学資年金開始日 has arrived | [S1] [S2] [S6] [S10]; scope **[std]** |

**Why `i_cv` is the 予定利率 here, and why that is better than the chassis could manage.** On
the whole-life chassis the pricing rate had to be *solved* out of a published
surrender-value table, because no carrier published the rate. On this product the position
reverses: **no carrier publishes a surrender-value formula or a numeric surrender-value
table for either cell** — a sharper gap than the chassis's [S1] [S2] [S10] [REG-R2] — but
one carrier publishes the 予定利率 by name, by product group, before and after a dated revision,
and it is **1.00% for both product groups in the same release** [S9]. So the library adopts
the published rate as the cash-value basis and derives the loading rather than the rate.
Adopting it is the standardization; the number is sourced. The other legs of the basis stay
dark: the 予定死亡率, the 予定事業費率 and the surrender-value formula sit in the 保険料及び責任準備金の算出方法書, a
filed but unpublished 基礎書類 under 保険業法第4条第2項 [REG-R2].

**What the loading then is — a derived output, and a seam that shows.** With `i_cv` = 1.00%
and the male valuation table, the net level premium on the anchor cell is **π =
¥145,896.34** against a sourced gross premium of ¥181,140, an implied loading of
**¥35,243.66, or 19.457% of the gross premium**. That is a plausible number for a 30-year
endowment, and it is coherent because the premium and the rate come from the *same* carrier
and the *same* release [S9]. On the second cell the same calculation gives **π_g =
¥110,458.94 against ¥108,564 — a loading of −1.745%**, which no real product carries. The
reason is the composite's seam: that premium is a different carrier's [S11] and that carrier
does not publish its 予定利率. Restated as rates rather than loadings, the two cells' guaranteed
cash flows imply internal rates of **−0.4239%** on the 養老 cell and **+1.1592%** on the 学資
cell. Both are derived diagnostics, both are printed by the model, and neither is an input.

**Why `i_L` is 2.40% where the chassis sets 2.75% — a named deviation, not an oversight.**
The mechanic is the chassis's and is not restated here; the *rate* is not the chassis's, and
that is deliberate. The chassis picks 2.75% off one carrier's vintage 貸付利率 schedule — the
band a contract written under the older 予定利率 falls in — and marks the pick **[std]**. On
this product a carrier publishes its 契約貸付利率 by name and by vintage, **2.00% → 2.40% for
contracts dated on or after 2025-01-02**, in the same release that moved the 予定利率 to 1.00%
[S9]. Taking 2.40% keeps the loan rate and the pricing rate on one document and one vintage,
which is worth more here than agreement with the chassis — and the two are not required to
agree, for the reason both sets of notes give: the loan rate tracks the contract's own
vintage 予定利率, not the market, so a 終身保険 written on a different 予定利率 carries a different
loan rate by construction. What the two products do share is the 約款 ceiling, 年8% / 半年4%
[S1] [S10]. The rate is unused in the base run in any case; it binds only on model points 8
and 9.

**`α`, and why it is re-based on premium.** The chassis expresses the acquisition deduction
as `α × SA × max(0, m − k) / m` with `α` = 0.0090, calibrated against a published table.
That form is meaningless on the 学資 cell, where 基準保険金額 is a **benefit-scaling unit and not a
sum assured** — total premiums are 1.85 times it. The deduction is therefore re-based on one
annual premium **[std]**:

    SC(k) = α × P × max(0, m − k) / m,     α = 0.25

On the anchor cell that is `SC(0)` = ¥45,285 at issue, within 0.7% of the ¥45,000 the chassis
calibrated against a real published surrender-value run — so the only piece of genuine
Japanese surrender-value calibration in this library is carried across rather than
discarded. The construction satisfies the three sourced quantitative constraints [S7]: the
value is below cumulative premiums at every duration on both cells (rising monotonically to
92.0% at anniversary `k = n` on the 養老 cell; on the 学資 cell the ratio saw-tooths with the
schedule, peaking at 98.4% at `k = 11` — the anniversary before the third 学資金 — and
standing at 94.2% at `k = m`), it is capped at the death benefit, and each 学資金 reduces it.
It does **not**
reproduce the fourth, adjectival, constraint — that the early durations return "either
nothing at all or very little" [S7]: `CV(1)` is 55.4% of the first year's premium on the
anchor cell. `α` is the named lever and this is listed as a model risk.

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality — two lives, one table, opposite margins.** 生保標準生命表2018（死亡保険用）is the sourced
basis on both lives, read from the publisher's own PDF [REG-R18] [R1]. It **includes 高度障害
inside the death rate** [REG-R20] [R2], so the 養老 cell's 重度障害 benefit is not a separate
decrement. It is a **valuation** table: 2008/2009/2011 experience, an improvement allowance,
then a 数学的危険論による補整 sized to roughly a 2σ level [R2] [REG-R20] — so a best-estimate basis is
a **[std]** adjustment *of* a sourced table.

| Input | Value | Basis |
|---|---|---|
| Base table — male | 生保標準生命表2018（死亡保険用）男, at attained age; both worked-example cells are male | [REG-R18] [R1] |
| Base table — female | 生保標準生命表2018（死亡保険用）女, at attained age, built from **its own** sourced anchors — never derived from the male column | [REG-R18] [R1] |
| Interpolation between sourced ages | Log-linear in `ln q`, rounded to 5 decimals — the table's own granularity | **[std]** |
| `mort_be_factor` (被保険者) | **1.00** in the base run | **[std]** |
| `wv_load` (契約者, waiver) | **1.00** in the base run | **[std]**, below |
| `wv_frac` | **1.00** — every 契約者 death qualifies for the waiver | **[std]**, below |
| Improvement overlay | None | **[std]** |

`mort_be_factor = 1.00` means **the base run is a valuation-table run, not a best
estimate**,
taken so that every number in the worked example can be checked against a document anyone
can download. The IAJ's site terms prohibit reproduction and transmission without written
consent [REG-R21], so `jplib` cites the table by URL, quotes the individual rates its
worked example needs, and ships `mort_table.csv` as a **[std]** construction whose
`provenance` column points at the IAJ entry [REG-R18] row by row.

`mort_table.csv` is the **library-wide canonical construction**, identical row for row in
every `jplib` product that ships it, so one cell carries one value *and* one provenance
string wherever it appears. Every row says which of two things it is: an **ANCHOR** row is a
rate read from the published table and quoted under attribution, and an **INTERPOLATED** row
is the log-linear fill in `ln q` between the two neighbouring anchors, rounded to five
decimals. There is no extrapolation: both sexes run from an age-0 anchor upward, so every
non-anchor age lies strictly between two sourced anchors.

**Both sexes are built the same way, each from its own anchors.** There is no ratio, no sex
multiplier and no derivation of one column from the other — the female rates are the
published female rates at the anchor ages and the same interpolation between them. Over the
ages this product reads, the male anchors are 0, 1, 3, 5, 10, 15, 17, 18, 20, 22, 25, 30,
31, 32, 33, 34, 35, 40, 45, 50, 55 and 60, and the female anchors the same list without 31
to 34. Neither worked-example cell reads the female column; model points 5 and 6 are the
only ones that do.

The file is restricted to attained ages **0 to 60**, which is every age these nine model
points reach: the oldest, the 養老 anchor cell, matures at attained age 60.

**The margin points in opposite directions on the two lives, which is why they are two
inputs.** On the 契約者 the waiver is a *cost*, so a table that overstates mortality
**overstates** the liability and is prudent. On the 被保険者 child the death benefit is
approximately the reserve the contract already holds, so the same margin is nearly neutral —
`q` runs 0.00081 at age 0, 0.00022 at 3, 0.00010 at 10, 0.00046 at 18 and 0.00066 at 22 on
the male table [R1] [REG-R18], and the whole 22-year child decrement contributes ¥3,988.78
of claims against ¥1,521,101.61 of premium income on the second cell. One projection
carrying a margin that is conservative on one life and neutral on the other is a reason to
hold two mortality inputs rather than one basis. The freely redistributable 第23回生命表 is the
benchmark against which the margin can actually be sized [REG-R24].

**`wv_load` is the one place a separate disability decrement is right.** The table already
carries 高度障害 [REG-R20], so the waiver's death and 高度障害 triggers are inside `q`. The
**third** trigger — 身体障害 from a listed accident within 180 days, present at three of the six
carriers [S1] [S10] [S16] — is **not**. `wv_load` is the multiplier that would add it; it is
1.00 in the base run **[std]** because no retrieved source gives an incidence, and holding
it at 1.00 therefore *understates* the waiver. That is the exact opposite of the chassis's
ruling on 高度障害, where adding a decrement double-counts, and confusing the two is a pitfall.

**`wv_frac`, and what a carve-out actually does.** When the 3-year suicide carve-out, the
successor's intentional act or war bites, **the contract does not merely lose the waiver —
it terminates**, paying the 責任準備金 to the 契約者's legal heirs [S1] [S7] [S10]. `wv_frac` = 1.00
**[std]** in the base run because no retrieved source gives a suicide incidence by duration
for Japanese lives; the `1 − wv_frac` path exists, is wired, and produces the
`claims_ph_death` column, which is identically zero in the base run. That zero is a product
fact worth publishing, in the same way `claims(t, "LAPSE")` is on the UK term chassis.

**Surrender.** No carrier publishes a lapse or surrender curve by duration for either
product; this is the single largest assumption gap. The only public benchmark is the
industry 解約・失効率 of **5.6%** for FY2024, defined as surrendered-and-lapsed **sum assured**
over opening in-force sum assured, industry-wide across all product types [R9] [REG-R31] —
an amount-weighted, all-product bound used here as a sanity ceiling and nothing more.

| Policy year (`1 + ⌊t/12⌋`) | 1 | 2 | 3 … n−1 | **n** |
|---|---|---|---|---|
| Months `t` | 0 … 11 | 12 … 23 | 24 … 12n−13 | **12n−12 … 12n−1** |
| `lapse_rate(t)` **[std]**, per annum | 4% | 3% | 2% | **2%, then 0 in the last month** |

The rates in the table are **annual** and the model applies them per month on the effective
convention `w_m = 1 − (1 − w)^(1/12)` **[std]**, so twelve months of surrender compound back
to the annual rate exactly and the in-force ladder at the anniversaries is the one the
annual grid produced.
On the waived state the same table applies, multiplied by `wv_lapse_mult` = **1.00 [std]**,
and the multiplier acts on the monthly rate rather than the annual one.
Both rates are keyed in `lapse_table.csv` by the **contractual policy year**, a 1-based
label the projection reaches as `1 + ⌊t/12⌋`; the file's `policy_year` column is not the
frame's `t` and its values did not move when the frame became monthly.
The premium-default rate `u(t)` that feeds the APL module sits in the same table and is
**1.0% / 0.8% / 0.6% [std]** on the same 1 / 2 / 3-onwards shape, gated to zero in the base
run by `apl_default_mult` = 0. No retrieved document gives a default rate for either cell,
so it too is inherited from the chassis for the same comparability reason.

The 4 / 3 / 2 shape is inherited from the chassis so that the two products stay comparable.
Two deltas. First, **there is no cliff and therefore no spike**: the chassis's 17% at
払込満了 exists only because a 低解約返戻金型 surrender value steps up by `1/k` at 払込満了, and neither
cell has one. Second, the rate is forced to **0 [std] in the final month** `t = 12n − 1`: a
surrender at the close of that month and the maturity payment fall at the same instant at
the same amount, and an owner one month from a
guaranteed `S` does not take `CV(n) = S` early. The carve-out is one month and not the
final policy year — the eleven months before it carry the ordinary 2%, which is why the
maturing fraction moved when the grid did. Setting it to anything else double-counts
the terminal payment. `wv_lapse_mult` = 1.00 is a placeholder that is almost certainly too
high — a waived policy receives every benefit for no further premium and has a strictly
dominant reason to persist — and it is named so that it can be moved.

**Expenses and commission (levels all [std]; no carrier publishes an expense basis at all —
予定事業費率 is named in the 保険契約者保護機構 boilerplate and never quantified).** Inherited unchanged
from the chassis so that the products stay comparable:

| Input | Value |
|---|---|
| Acquisition expense `E0` | ¥50,000 per policy at issue **[std]** |
| Initial commission `c0` | 90% of the annual premium at issue **[std]** |
| Renewal commission `c_r` | 3% of premium, policy years 2 … `m` — the anniversary months `t = 12, 24, …, 12(m − 1)` — **on the premium-paying state only** **[std]** |
| Maintenance expense `e(t)` | ¥8,000 p.a., charged as **¥8,000 / 12 a month** over `t = 0 … 12n − 1`, inflating at 1.0% p.a. as `1.01^⌊t/12⌋` so the step falls once a policy year, **on both states** **[std]** |
| Claim expense `ec` | ¥20,000 per death claim **[std]** |
| Maturity and staged-benefit expense | None — folded into maintenance **[std]** |

Renewal commission on the paying state only and maintenance on both is not a detail: a
waived policy costs the insurer administration and pays the distributor nothing.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | **month** index, 0-based: t = 0 … 12n − 1; policy year `y(t) = 1 + ⌊t/12⌋`; the 被保険者's attained age in month t is `x + ⌊t/12⌋` |
| `k` | **anniversary** index **in years**, k = 0 at issue: month `t` closes policy year `k = ⌊t/12⌋ + 1` when `(t + 1) mod 12 = 0` |
| `u` | **elapsed month** at which a value is read, `u = t + 1` for the flows of month `t`; `u = 12k` is anniversary `k` |
| `x`, `y` | 契約年齢 of the 被保険者 and of the 契約者 (学資 cell only) |
| `n`, `m` | 保険期間 in years; 保険料払込期間 in years, `m ≤ n` |
| `S`, `P` | 基準保険金額; annual premium, payable at the start of the anniversary months `t = 0, 12, …, 12(m − 1)` |
| `g(k)` | staged 学資金 due at anniversary k, as a fraction of `S`; 0 on the 養老 cell |
| `G(k)` | `Σ_{s ≤ k} g(s)` — cumulative staged fraction paid to and including anniversary k |
| `q(t)`, `q_p(t)` | 被保険者 **annual** mortality applying in month t; 契約者 annual mortality, zero from `t = 12m` on |
| `q_m(t)`, `q_pm(t)` | the same two per month, `1 − (1 − q)^(1/12)` **[std]** |
| `w(t)`, `w_m(t)` | annual voluntary surrender rate applying in month t, and the same per month |
| `u(t)` | premium-default **proportion** (APL module): one decision on one date, never converted, zero outside anniversary months |
| `l(t)` | **total** in-force probability at the start of month t (`pols_if`), `l = l_p + h` — the same `l` the 終身 and 外貨建 chassis use, where there is only one state |
| `l_p(t)`, `h(t)` | in-force probability in the paying state (`pols_if_pay`) and the waived state (`pols_wv`) |
| `D(t)`, `Dp(t)` | expected 被保険者 deaths in month t; expected 契約者 decrements in month t |
| `R(t)` | expected in force at the end of month t, after mortality, before surrender |
| `Sr(t)` | expected surrenders at the end of month t |
| `A(z, j)`, `ä(z, j)` | j-year endowment-assurance EPV of 1 at age z; j-year annuity-due, both on `i_cv` and the table |
| `π`, `π_g` | net level premium on the cash-value basis, 養老 cell and 学資 cell |
| `W(k)`, `Wb(k)` | policy value at anniversary k, after and before the staged benefit due at k |
| `SC(k)`, `V(k)`, `CV(k)` | acquisition deduction; ordinary surrender value; payable 解約返戻金, all at anniversary k |
| `W(u)`, `Wb(u)`, `SC(u)`, `CV(u)` | the same four read at an **elapsed month** u, by linear interpolation **[std]** |
| `DB(t)` | death benefit for a death in month t, payable at the end of it |
| `L(k)` | loan + APL principal and interest at anniversary k — it compounds **annually**, on the 契約応当日 |
| `i_cv`, `i_L`, `i_std` | cash-value basis rate; loan rate; reference valuation rate |
| `α` | acquisition-deduction rate, per unit of one annual premium |
| `E0`, `e(t)`, `c0`, `c_r`, `ec` | acquisition expense; maintenance; initial and renewal commission; claim expense |
| `CF(t)` | net cash flow of month t, **income-positive** (`net_cf`) |
| `ρ` | 返戻率 — the derived return ratio (below) |

**Dimensional check.** `q`, `q_p`, `w`, `u`, `g`, `G`, `α`, `c0`, `c_r`, `l`, `h` and `ρ`
are dimensionless, and so are `l_p` and `q_p`; `i_cv`, `i_L`, `i_std` are per annum; `A` and `ä` are pure numbers (`ä`
in years of premium, so `S × A / ä` is ¥ per year); `S`, `P`, `W`, `Wb`, `SC`, `V`, `CV`,
`DB`, `L`, `E0`, `e`, `ec` are ¥; every term of `CF(t)` is ¥ per policy issued **per month** —
`e(t)` is a twelfth of the annual maintenance expense, and `P` falls in one month out of
twelve rather than being spread over the year.
`g(k)` is a fraction of `S`, never of a premium — the two are within a factor of two of each
other on the second cell, so the check is not idle.

### The staged schedule is data

`g(k)` is read from `benefit_schedule_table.csv`, keyed by `schedule_id`, one row per
payment, with a `provenance` column on every row. The key column is `k`, the **anniversary**
the payment falls on with `k = 0` at issue — a time point in **years**, already 0-based, and
**not** the projection's month index: the payment at `k` is the staged claim of the single
month `t = 12k − 1`, whose closing instant is that anniversary.

    schedule_id   k   benefit_pct   provenance
    S_0_1         3   0.05          S型 grid, child 契約年齢 0-1 [S10]; timing [std]
    S_0_1         6   0.05          "
    S_0_1        12   0.10          "
    S_0_1        15   0.10          "
    S_0_1        18   0.70          "
    S_0_1        20   0.10          "
    J            18   1.00          J型 degenerate variant [S10]; timing [std]

The 満期保険金 of 100% at anniversary `n` is **not** a schedule row: it is always present, on both cells,
and is held separately so that a schedule with no rows at all still matures. The observed
designs run from a single 100% payment [S10] through three 20% 祝金 plus a five-instalment
学資年金 [S7] to four equal payments of 100% each [S13], so **any implementation that hard-codes
a shape is modelling one carrier**. The `J` row is retained precisely because a grid that
collapses to two payments is the sharpest test that the schedule is data.

### The two policy-value constructions

They differ because the two products insure different things, and the difference is not
cosmetic.

**養老 cell — an endowment assurance, so the death benefit is inside the EPV.**

    π      = S × A(x, n) / ä(x, m)
    W(k)   = S × A(x + k, n − k) − π × ä(x + k, max(m − k, 0))
    Wb(k)  = W(k)                                        (g is identically zero)
    DB(t)  = S − L(t)

where `A(z, j)` is the j-year endowment assurance — 1 at the end of the year of death within
j years, or 1 on survival to j. At `k = n`, `A(x + n, 0) = 1` and `ä(·, 0) = 0`, so **`W(n)
= S` exactly, by construction**; at `k = 0`, `π` is defined so that `W(0) = 0`. That identity is why the 養老 cell is a better test of a
savings model than the chassis is: a whole-life reserve that drifts can hide for decades,
while an endowment reserve that does not converge on its own maturity benefit is wrong on
the first run.

**学資 cell — survival benefits only, because the death benefit releases the value.**

    EPV(k) = S × [ Σ_{s > k} g(s) · v^(s−k) · (s−k)p_(x+k)  +  v^(n−k) · (n−k)p_(x+k) ]
    π_g    = EPV(0) / ä(x, m)
    W(k)   = EPV(k) − π_g × ä(x + k, max(m − k, 0))
    Wb(k)  = W(k) + S × g(k)
    DB(t)  = max( P × min(t + 1, m) − S × G(t) − L(t),  Wb(t + 1) )

The `Σ_{s > k}` is what makes `W(k)` the value **after** the staged benefit due at `k`,
which is the sourced fact that each 祝金 reduces the surrender value [S7] and that one carrier
computes the value from the elapsed months **and** the 学資金 timing [S1]. Excluding the death
benefit from the EPV is the **[std]** step, and it is one carrier's own wording read
literally: its 死亡払戻金 *is* the 責任準備金相当額 [S10], so on that design the decrement is exactly
value-neutral, and the composite's max-form dominates it [S3] [S13]. At `k = n` there is no
future staged benefit and no future premium, so **`W(n) = S` exactly** here too.

`DB(t)` is the only place all three indices meet in one line, and each term sits on the
clock it belongs to. A death in month `t` is paid at the end of it, so the value limb is the
interpolated `Wb(t + 1)` at elapsed month `u = t + 1`; the premiums *due* are the
`min(⌈(t + 1)/12⌉, m)` that have actually fallen by then, which steps up once a policy year
rather than once a period; and the staged benefits **already received** are those at
anniversaries up to and including `⌊t/12⌋`, which is `G(⌊t/12⌋)`, because a payment falling
at the close of month `t` is still inside `Wb(t + 1)`.

Then, on both cells, at every anniversary `k`,

    SC(k) = α × P × max(0, m − k) / m
    V(k)  = max(0, W(k) − SC(k))
    CV(k) = V(k)

with **no 低解約返戻金型 multiplier**: `CV` and `V` are the same series on this product. Between
anniversaries the three are read at an elapsed month `u` by linear interpolation **[std]** —
`Wb(u)` from `W(k)` to `Wb(k + 1)`, which is the curve the contract traces between one
staged benefit and the next, and `SC(u) = α P (12m − u) / 12m`, which is the same linear run-off read finely rather than a
second schedule — with `CV(u) = max(0, W(u) − SC(u))` as before. The 算出方法書 that would state the carrier's real
within-year rule is a 基礎書類 filed with the 金融庁 and is not published [REG-R2], so the
interpolation is a standardization and is flagged as one; at `u = 12k` it reproduces the
anniversary value exactly, which `check_staged_value` asserts.

**The premium term in `DB(t)` is deemed-paid, not cash-paid.** `P × min(⌈(t + 1)/12⌉, m)`
counts every premium falling due by the end of month `t`, whether or not the 契約者 was alive
to pay it, because the waiver
provides that each future premium is *treated as having been paid* on its 契約応当日 [S1] [S10]
[S13]. The same wording is why **`CV(k)` is identical in both states**: the surrender value
is computed as if the premiums had been paid, so the waived and paying states share one
policy value. A model that keeps two value series is modelling a contract nobody wrote.

### The waiver as a state transition, not a benefit

`W(k)` is the reference quantity for the reserve; the waiver produces **no outgo line at
all**. What it produces is the absence of premium income, which is why it can be omitted
without any claim column looking wrong. On the 学資 cell, for `t = 0 … 12n − 1`, every line
on the **monthly** rates:

    q_pm(t)       = 0  for t ≥ 12m                        (no premium left to waive)
    l(t)          = l_p(t) + h(t)                         (total in force)
    D(t)          = l(t) × q_m(t)                          (被保険者 deaths, both states)
    Dp(t)         = l_p(t) × (1 − q_m(t)) × q_pm(t)         (契約者 decrements, paying only)
    to waived     = wv_frac × Dp(t)
    terminating   = (1 − wv_frac) × Dp(t)                 (pays Wb(t + 1) to the heirs)

    l_p_after(t)  = l_p(t) × (1 − q_m(t)) × (1 − q_pm(t))
    h_after(t)    = h(t) × (1 − q_m(t)) + wv_frac × Dp(t)
    R(t)          = l_p_after(t) + h_after(t)

    l_p(t + 1)    = l_p_after(t) × (1 − w_m(t))
    h(t + 1)      = h_after(t) × (1 − min(1, wv_lapse_mult × w_m(t)))

The waiver multiplier acts on the **monthly** surrender rate, not on the annual one: a
waived policy that surrenders at half the ordinary pace does so at half the pace in every
month, rather than at half an annual rate spread unevenly over twelve. Twelve months of each
line compound back to the annual recursion the previous grid ran, so the transition
probabilities at the anniversaries are the ones it produced.

The two lives are **independent [std]** — no retrieved document gives a dependency and none
could. Where the 契約者 is the child's parent, common-accident dependence is real and
unmodelled.

**`q_pm(t) = 0 for t ≥ 12m` is a modelling ruling and earns its own sentence.** The
premium-paying months are `t = 0 … 12m − 1`, so the decrement stops with the last of them. The 約款 make
every waiver trigger conditional on the event falling *during* 保険料払込期間 [S1] [S10], and the
termination-without-waiver path is the failure mode of that same provision [S1] [S7] [S10].
After 払込満了 there is no premium to waive and nothing for the provision to fail at, so the
composite **[std]** treats the contract as continuing through the 契約者's death by succession
[S1] [S7] [S10] [S13] and drops the second decrement entirely. On the second cell that
covers the months `t = 204 … 263`, policy years 18 to 22 of the 22-year term — the years in
which 86% of the receipts fall — and carrying the decrement through them would move a
further **0.8250%** of policies out of the premium-paying state, which wherever
`wv_frac < 1` terminates a share of them and deletes their maturity benefits.

### Processing order (month t = 0 … 12n − 1, i.e. policy years 1 … n)

1. **Start of the month — premium, in anniversary months only.** Collect `P × l_p(t)` when
   `t mod 12 = 0` and `t < 12m` — on the **paying** state alone, never on `l(t)` — and
   nothing in the other eleven months. The waived state is in force and pays nothing. On an
   APL cohort the premium is not collected in cash: the advance is applied to it and it
   appears only as growth in `L` (chassis).
2. **Start of the month — expenses and commission.** `e(t) × l(t)` **every** month, a
   twelfth of the annual amount, on the whole in force; renewal commission
   `c_r × P × l_p(t)` in the anniversary months `t = 12, 24, …, 12(m − 1)`, on the paying
   state only, because it follows the premium it is a percentage of. At `t = 0`
   additionally `E0` and `c0 × P`.
3. **Start of the month — APL test** (module on), in anniversary months only: the premium
   default is a failure to pay one premium on one date. Chassis, unchanged, run against
   `CV`.
4. **Values.** Compute `Wb(t + 1)`, `W(t + 1)`, `SC(t + 1)`, `CV(t + 1)` at the closing
   elapsed month `u = t + 1`, by interpolation **[std]** between the anniversaries `u` lies
   between; in an anniversary month they *are* the anniversary values `Wb(k)`, `W(k)`,
   `SC(k)`, `CV(k)` with `k = (t + 1)/12`.
5. **End of the month — 被保険者 deaths.** `D(t) = l(t) × q_m(t)`, on the whole in force; outgo
   `DB(t) × D(t)`, floored at zero; claim expense `ec × D(t)`.
6. **End of the month — 契約者 decrement**, on the paying state only and only for `t < 12m`:
   `Dp(t) = l_p(t) × (1 − q_m(t)) × q_pm(t)`, split by `wv_frac` into a transition to the
   waived state and a termination paying `Wb(t + 1)`.
7. **End of the month — staged benefit, in anniversary months only.** `S × g(k) × R(t)` when
   `t = 12k − 1`, to everything in force at that anniversary, in **both** states. It is not
   a decrement and it terminates nothing. In the other eleven months it is zero: a 学資金 is
   a payment on a date.
8. **End of the month — maturity, at `t = 12n − 1` only.** `S × R(12n − 1)`, at anniversary
   `n`. The carve-out from surrender is that single month, not the whole final year.
9. **End of the month — surrenders**, on survivors of both mortality decrements, valued on
   `CV(t + 1)` — that is, **net of any staged benefit just paid**: `Sr(t) = l_p_after(t) ×
   w_m(t) + h_after(t) × min(1, wv_lapse_mult × w_m(t))`; outgo
   `max(0, CV(t + 1) − L(⌊t/12⌋)) × Sr(t)`. The waiver multiplier is applied to the
   **monthly** rate, so a waived policy surrenders at half the pace every month rather than
   at half an annual rate spread unevenly.
10. **Loan roll-up and in-force update.** The loan and APL balances compound **annually**, at
    the 契約応当日, because the 約款 states a 年利 capitalised there; the populations
    `l_p(t + 1)` and `h(t + 1)` update every month, as above.
11. **At the end of `t = 12n − 1`** everything closes: `l(12n) = l_p(12n) = h(12n) = 0`.
    There are no tail states.

### Net cash flow

Income-positive, per policy issued:

    CF(t) = P × l_p(t) × 1{t mod 12 = 0, t < 12m}         (premiums)
          − DB(t) × D(t)                                  (被保険者 death claims)
          − ec × D(t)                                     (claim expense)
          − Wb(t + 1) × (1 − wv_frac) × Dp(t)             (契約者 death, waiver refused)
          − S × g((t + 1)/12) × R(t) × 1{(t+1) mod 12 = 0}  (staged 学資金)
          − S × R(12n − 1) × 1{t = 12n − 1}               (満期保険金)
          − max(0, CV(t + 1) − L(⌊t/12⌋)) × Sr(t)         (surrender benefits)
          − e(t) × l(t)                                   (maintenance expense, a twelfth a month)
          − c_r × P × l_p(t) × 1{t mod 12 = 0, 12 <= t < 12m}  (renewal commission)
          − (E0 + c0 × P) × 1{t = 0}                      (acquisition)

`net_cf` is income-positive throughout, so there is no outgo-positive `liability_cf`
companion on this product: one stream, one sign, one name. The result columns are
`premiums`, `claims_death`, `claims_staged`, `claims_maturity`, `claims_lapse`,
`claims_ph_death`, `expenses`, `claim_expenses`, `commissions` and `net_cf`, with `pols_if`
first, then `pols_if_pay` and `pols_wv` beside it. `claims_staged` and `claims_ph_death` are
named for the `kind` arguments `"STAGED"` and `"PH_DEATH"` that produce them.

**`expenses` is the policy expense and nothing else.** The `expenses` column carries `E0`
and `e(t)`; the claim handling expense `ec × D(t)` is a per-claim cost, not a per-policy
one, and it is published as its own `claim_expenses` column and deducted explicitly in
`CF(t)` above. The worked example below therefore prints the two as two columns.

**Roll-forward identity.** Every policy leaves by exactly one route and the term is finite:

    Σ_t D(t) + Σ_t (1 − wv_frac) × Dp(t) + Σ_t Sr(t) + R(12n − 1) = 1,   and   l(12n) = 0

`check_pols_roll_fwd()` takes no argument and returns a bool over all `t`; the per-`t`
signed residual lives at `check_pols_roll_fwd_resid(t)`. A second check has no analogue on
the chassis: `check_pol_val_terminal()` asserts `pol_val_pp(n) == sum_assured` at the final
anniversary, to the displayed precision, on both cells.

### 返戻率 as a derived output

The number both products are sold on is a ratio of **contractual amounts on one policy that
survives, pays every premium, takes every benefit in cash and receives no dividend** — not a
probability-weighted quantity, not discounted, not net of tax:

    ρ = ( S × Σ_k g(k) + S ) / ( P × m )

`henreiritsu()` is a cells with no argument returning `ρ`. On the anchor cell `ρ = 5,000,000
/ 5,434,200 = 92.0099%`; on the second cell `ρ = 2,100,000 / 1,845,588 = 113.7849%`, against
the "approx. 113.7%" the carrier publishes for exactly that plan [S11] — the carrier
truncates rather than rounds. Four things must be said about it, and all four are testable:

- **It is not a rate of return.** Restated as one, the anchor cell's guaranteed cash flows
  imply **−0.4239% p.a.** and the second cell's **+1.1592% p.a.**
- **It is undefined on a policy that surrenders**, and it is not the ratio the model's own
  cash-flow statement produces, which is probability-weighted and carries expenses.
- **It is unbounded on a waived policy**, where the denominator stops growing and the
  numerator does not — which is why `henreiritsu()` reads the *contractual* premium term `P
  × m` and never the projected premium income.
- **It moves with payment frequency and volume band** [S13] [S14] [S16], so a ratio computed
  from a 月払 premium is a lower bound on the carrier's own 年払 figure. The projection now
  steps in months, but the premium it collects is still the **年払** one: the monthly grid
  changed *when* the premium falls, not *which* premium it is, and `ρ` did not move.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions; no public calibration evidence
exists for any of them on either product.

- **Base surrender.** The duration table in class (c): flat 2% from year 3, **no cliff and
  no spike**, and zero in the final year.
- **The waived state is not a lapse state.** There is no premium to miss, so the
  premium-default decrement `u(t)` and the APL do not run there at all; only voluntary
  surrender and the 被保険者's death can end a waived policy before maturity. Applying a
  premium-default decrement to the waived state models a decrement the contract does not
  have.
- **Premium default and the APL.** Chassis, unchanged: a decrement out of the paying cohort
  into an APL cohort, **not** a lapse — a policy does not lapse while the cash value can
  carry the premium [S1] [S10]. Off in the base run. Two of the six carriers do not offer
  the APL at all [S6] [S13], so the off position is a product variant and not merely a
  switch.
- **Reinstatement (復活) is not modelled [std]**, and it costs more here than on the chassis.
  Within three years of lapse a Japanese policy comes back [S1] [S10]; on this product two
  carriers additionally pay a 学資金 **whose payment date fell while the policy was lapsed**,
  provided the policy is later reinstated [S1] [S10]. So lapse is not terminal even for
  benefits already due, and treating every exit as terminal understates later-duration in
  force, premium income, staged benefits and the maturity benefit together.
- **Dynamic surrender on the value-to-premium ratio [std] (optional module, off in base).**
  The chassis's form carries over, `w_dyn(t) = w(t) × min(3.0, max(1.0, 1 + β × max(0,
  CV(t + 1) / cumprem(t + 1) − 1)))` with `β` = 2.0 **[std]** and `cumprem(k) = P × min(k,
  m)`, both read at the period's closing anniversary. On the
  anchor cell the ratio never reaches 1 — it peaks at 92.0% at maturity — so the module is
  inert there, which is itself the finding: a 30-year 養老保険 at a 1.00% 予定利率 gives its owner
  no point at which surrendering beats persisting on value grounds alone.
- **Election of the staged schedule.** The type, once elected, cannot be changed after issue
  [S7], so `schedule_id` is a model-point attribute and never a projected decision.
- **免責 and 告知義務違反 incidence are zero in the base run [std].** Where a claim is refused the
  composite pays the 保険料積立金 rather than nothing [S2] [S8] — but two carriers on the 学資 cell
  pay **nothing at all, not even the reserve**, where the 契約者 intentionally kills the
  insured child [S1] [S10]. A model that assumes the zero-payment position universally
  overstates the insurer by the whole reserve.
- **The grace-period trap is not modelled [std], and it is the reason the waiver is not an
  overlay.** Stated identically at three carriers: if the waiver event happens while a
  premium is unpaid inside the grace period, that premium must be paid by the end of the
  grace period **or the waiver is refused** [S1] [S6] [S10]. A 契約者 who dies one week into
  arrears loses the entire benefit. That is a direct interaction between the premium-default
  decrement and the waiver decrement, and it is why the waiver cannot be applied as an
  independent multiplier on a premium stream. The model has no arrears state — the monthly
  grid is now fine enough to carry one, but the grace period is a calendar-day rule the model
  point table gives no date for — so the interaction is out of scope and named rather than
  approximated.

---

## Worked example

**Every figure below was recomputed numerically before it was written.**

### Anchor cell (`point_id = 1`) — 養老保険

Male, 契約年齢 30 (満年齢), 基準保険金額 ¥5,000,000, 保険期間 30 years (満期 at attained age 60), 保険料払込期間 30
years, annual premium **¥181,140** (= 12 × the published ¥15,095 monthly premium for exactly
this cell [S9]). `n = 30` policy years, `t = 0 … 359` months, attained ages 30 to 59. 死亡保険金 = 満期保険金 =
¥5,000,000 [R10] [S2] [S8]. No waiver, no loan, no APL, no dividend.

**Assumption values used, in full.** `i_cv` = **1.00%** [S9]; `α` = **0.25** of one annual
premium, so `SC(0)` = ¥45,285 at issue **[std]**; `mort_be_factor` = **1.00 [std]**;
`lapse_rate` = 4% /
3%
/ 2% … 2% per annum, **0% in the final month `t = 359`** **[std]**; `E0` = ¥50,000,
`c0` = 0.90, `c_r` = 0.03, `e(t)` = ¥8,000 / 12 × 1.01^⌊t/12⌋ a month, `ec` = ¥20,000, all
**[std]**; `i_L` = 2.40% [S9], unused because
`loan_pp ≡ 0`.

**The mortality rates.** These are 生保標準生命表2018（死亡保険用）男 rates read at the anchor ages
`q30 = 0.00068`, `q31 = 0.00069`, `q32 = 0.00070`, `q33 = 0.00072`, `q34 = 0.00074`,
`q35 = 0.00077`, `q40 = 0.00118`, `q45 = 0.00177`, `q50 = 0.00285`, `q55 = 0.00422` and
`q60 = 0.00653` [R1] [REG-R18], with the intervening ages filled by **[std]** log-linear
interpolation in `ln q` rounded to five decimals. They are **not** illustrative
placeholders: every rate here is either read from the published table or interpolated
between two rates that were, and `mort_table.csv` says which each row is.

| age | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `q` | .00068 | .00069 | .00070 | .00072 | .00074 | .00077 | .00084 | .00091 | .00099 | .00108 | .00118 | .00128 | .00139 | .00151 | .00163 |

| age | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `q` | .00177 | .00195 | .00214 | .00236 | .00259 | .00285 | .00308 | .00333 | .00361 | .00390 | .00422 | .00461 | .00503 | .00548 | .00598 |

**The cash-value construction.** `A(30, 30)` = 0.74664983 and `ä(30, 30)` = 25.58836739 on
`i_cv` = 1.00% and the male table, so **π = ¥145,896.34** — an implied loading of
¥35,243.66, 19.457% of the gross premium. The resulting values, with `SC(k) = 0.25 × 181,140
× (30 − k) / 30`, are indexed by the **anniversary** `k`, in years (`k = 0` at issue, and
`k` is the close of the month `t = 12k − 1`); the months in between read them by
interpolation **[std]**:

| k | `W(k)` | `SC(k)` | `CV(k)` | cumulative premiums | `CV(k)` / cum. prem. |
|---|---|---|---|---|---|
| 1 | 144,053.26 | 43,775.50 | 100,277.76 | 181,140 | 55.4% |
| 5 | 735,250.45 | 37,737.50 | 697,512.95 | 905,700 | 77.0% |
| 15 | 2,313,975.49 | 22,642.50 | 2,291,332.99 | 2,717,100 | 84.3% |
| 29 | 4,804,598.71 | 1,509.50 | 4,803,089.21 | 5,253,060 | 91.4% |
| **30** | **5,000,000.00** | **0.00** | **5,000,000.00** | **5,434,200** | **92.0%** |

`W(30) = S` exactly, which is the identity `check_pol_val_terminal()` asserts, and the last
column never reaches 100% — this contract does not return its premiums even at maturity.

**First months of the base run.** Per policy issued, income-positive, to two decimal
places, indexed by the 0-based **policy month** `t` with the contractual policy year `y(t)`
beside it. The `expenses` column carries a twelfth of the annual maintenance charge, and at
`t = 0` the acquisition expense as well; the claim handling expense is the separate
`claim_expenses` column beside it. `pols_if` is the total in force, which on this cell
equals `pols_if_pay` because there is no waiver and therefore no second state.

Two columns are non-zero in **one month out of twelve** — the 年払 premium and the renewal
commission that follows it — and the maturity payment in exactly one month of the whole 360.

| t | y(t) | age | `pols_if(t)` | premiums | claims_death | claims_maturity | claims_lapse | expenses | claim_exp | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 30 | 1.000000 | 181,140.00 | 283.42 | 0.00 | 0.00 | 50,666.67 | 1.13 | 163,026.00 | −32,837.22 |
| 1 | 1 | 30 | 0.996547 | 0.00 | 282.44 | 0.00 | 0.00 | 664.36 | 1.13 | 0.00 | −947.94 |
| 2 | 1 | 30 | 0.993107 | 0.00 | 281.47 | 0.00 | 0.00 | 662.07 | 1.13 | 0.00 | −944.67 |
| 11 | 1 | 30 | 0.962671 | 0.00 | 272.84 | 0.00 | 327.82 | 641.78 | 1.09 | 0.00 | −1,243.53 |
| 12 | 2 | 31 | 0.959347 | 173,776.15 | 275.90 | 0.00 | 273.66 | 645.96 | 1.10 | 5,213.28 | +167,366.24 |
| … | | | | | | | | | | | |
| 358 | 30 | 59 | 0.496231 | 0.00 | 1,239.84 | 0.00 | 4,157.88 | 441.48 | 4.96 | 0.00 | −5,844.16 |
| **359** | **30** | 59 | 0.495148 | 0.00 | 1,237.14 | **2,474,504.99** | 0.00 | 440.52 | 4.95 | 0.00 | **−2,476,187.59** |

**Trace, `t = 0` (the first policy month).** `q(0) = 0.00068` is the annual table rate and
`q_m(0) = 1 − (1 − 0.00068)^(1/12) = 0.0000566843` the decrement applied, so
`D(0) = 0.0000566843`; death claims = 5,000,000 × that = 283.42; claim expense = 1.13.
Survivors of mortality `R(0) = 0.9999433157`, and `w_m(0) = 1 − (1 − 0.04)^(1/12) =
0.0033960532`, so `Sr(0) = 0.0033958607`. **The surrender benefit is nil**, and that is the
product rather than a rounding: at the end of the first month the interpolated policy value
is `W(1) / 12 = 12,004.44` against a 解約控除 of `45,285 × 359/360 = 45,159.21`, so
`CV = max(0, W − SC) = 0`. The 約款's 「ご契約後短期間で解約されたときには、解約返還金がない場合があります」
[S2] is a statement the annual grid could not make: at the first *anniversary* the value has
already outrun the deduction and `CV(1)` is ¥100,277.76. On this cell the crossover is the
**fourth** month.
Expenses = 50,000.00 + 8,000/12 = 50,666.67; commission = 0.90 × 181,140 = 163,026.00.
`CF(0) = 181,140.00 − 283.42 − 1.13 − 0.00 − 50,666.67 − 163,026.00 = −32,837.22`. Update:
`l_p(1) = 0.9999433157 × 0.9966039468 = 0.996547`.

**Trace, `t = 12` (the first month of policy year 2).** The premium falls again — one of the
twelve months that carry it — at `181,140 × 0.959347 = 173,776.15`, and the renewal
commission with it at `0.03 × 173,776.15 = 5,213.28`. The attained age steps to 31, so
`q(12) = 0.00069`; the lapse rate steps to 3%. Maintenance = `(8,000 / 12) × 1.01 × 0.959347
= 645.96`. `CF(12) = 173,776.15 − 275.90 − 1.10 − 273.66 − 645.96 − 5,213.28 = +167,366.24`.

**Trace, the maturity month `t` = 359.** The 満期保険金 falls at the anniversary 30, which is
the close of the month 359, so it is **one month wide** rather than one year.
`l(359) = 0.495148`, `q(359) = 0.00598` and `q_m = 0.000499704`, so `D(359) = 0.000247428`
and death claims = 1,237.14 with claim expense 4.95. `R(359) = 0.494901`, and because
`lapse_rate(359) = 0` **every one of those survivors matures**: `claims_maturity` =
5,000,000 × 0.494901 = **2,474,504.99**. `CF(359) = −1,237.14 − 4.95 − 2,474,504.99 −
440.52 = −2,476,187.59`, against −5,844.16 one month earlier.

**The maturity payment is the largest single item in the stream and on this grid it is one
month wide.** Unlike the chassis's behavioural cliff it is a *certain* payment — the only
uncertainty in it is how many policies reach it.

**The surrender carve-out shrank with the grid, and that changed the answer.** `lapse_rate`
is zero in the final period so that a surrender and the maturity payment, which fall at the
same instant at the same amount, are not both booked. On the annual grid that suppressed
surrender for the whole of policy year 30 — twelve months in which an owner could in fact
still surrender. Here only the month whose *end* is the maturity date is suppressed, so the
other eleven carry the ordinary 2%, and the maturing fraction falls from 0.5042 to
**0.4949** accordingly. That is the largest single difference between the two grids on this
cell.

**Roll-forward check.** Over the 360 months, `Σ D(t) = 0.042768495`, `Σ Sr(t) = 0.462330508`
and the maturing survivors 0.494900998, summing to **1.000000000**, with `l(360) = 0`.
Undiscounted totals per policy issued: premiums 3,931,162.67; death claims 213,842.47;
maturity 2,474,504.99; surrender benefits 899,875.29; expenses 245,871.00 (maintenance
195,871.00, acquisition 50,000.00); claim expense 855.37; commission 275,526.68;
`Σ CF(t)` = **−179,313.13**. Undiscounted, the contract loses money; discounting is out of
scope and is what makes the sign meaningful. **Half the block reaches maturity** — 0.4949 of
policies issued — which is the structural difference from every protection product in this
library.

Premium income and commission are **identical** to the annual grid's, because both are
annual and fall at the same anniversaries on the same survivorship; what moved is the
benefit side and the maturity fraction.

`henreiritsu()` returns **92.0099%** = 5,000,000 / 5,434,200, reproducing the derived figure
in `product-spec.md` [S9] — a contractual ratio, unchanged by the projection grid.

### Second cell (`point_id = 2`) — 学資保険

契約者 male 契約年齢 30, 被保険者 (the child) 契約年齢 0, 22歳満期 (`n` = 22), 保険料払込期間 17 years, 基準保険金額
¥1,000,000, S型 grid at child 契約年齢 0–1, annual premium **¥108,564** (= 12 × ¥9,047 [S11]),
`waiver = true`. Staged benefits at anniversaries `k` = 3 / 6 / 12 / 15 / 18 / 20 of 5% /
5% / 10% / 10% / 70% / 10% of `S`, then 満期保険金 100% at `k` = 22 [S10] [S11]. Each of those
payments is the staged claim of the single month `t = 12k − 1` — 35, 71, 143, 179, 215, 239
and 263 — and zero in the other 257.

**Additional assumption values.** `i_cv` = 1.00% [S9]; `α` = 0.25, so `SC(0)` = ¥27,141
**[std]**; `wv_frac` = 1.00, `wv_load` = 1.00, `wv_lapse_mult` = 1.00, all **[std]**; child
mortality at attained age `⌊t/12⌋` and 契約者 mortality at attained age `30 + ⌊t/12⌋` for
`t < 204`,
both from 生保標準生命表2018（死亡保険用）男 [R1] [REG-R18] on the same **[std]** interpolation:

| child age | 0 | 1 | 2 | 3 | 4 | 5–10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `q` | .00081 | .00056 | .00035 | .00022 | .00015 | .00010 | .00012 | .00014 | .00016 | .00019 | .00023 | .00030 | .00038 | .00046 | .00052 | .00059 | .00062 |

The rates **read** from the published table over this range are those at ages 0, 1, 3, 5,
10, 15, 17, 18, 20 and 22 [R1] [REG-R18]; ages 2, 4, 6–9, 11–14, 16, 19 and 21 are the
**[std]** log-linear fill between them, and `mort_table.csv` says which each row is. The
same split holds over the adult range, where the read ages are 25, 30–35, 40, 45, 50, 55
and 60.
The 契約者 rates over ages 30–46 are the anchor cell's first seventeen. `π_g` = **¥110,458.94**
against a gross premium of ¥108,564 — the −1.745% loading discussed in class (b).

`pols_if` here is the **total** in force and `pols_if_pay + pols_wv` reproduces it row by
row; the premium is carried on `pols_if_pay` alone and every benefit on `pols_if`. The
index is the 0-based policy month, so the staged payment due at anniversary `k` falls in the
single month `t = 12k − 1` — months 35, 71, 143, 179, 215 and 239 on this grid.

| t | y(t) | child age | 契約者 age | `pols_if` | `pols_if_pay` | `pols_wv` | premiums | claims_death | claims_staged | claims_lapse | expenses | claim_exp | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 30 | 1.000000 | 1.000000 | 0.000000 | 108,564.00 | 7.33 | 0.00 | 0.00 | 50,666.67 | 1.35 | 97,707.60 | −39,818.95 |
| 1 | 1 | 0 | 30 | 0.996537 | 0.996480 | 0.000056 | 0.00 | 7.31 | 0.00 | 0.00 | 664.36 | 1.35 | 0.00 | −673.01 |
| 2 | 1 | 0 | 30 | 0.993085 | 0.992973 | 0.000113 | 0.00 | 7.28 | 0.00 | 3.95 | 662.06 | 1.34 | 0.00 | −674.63 |
| **35** | **3** | 2 | 32 | 0.912569 | 0.910734 | 0.001835 | 0.00 | 9.01 | **45,627.11** | 408.37 | 620.61 | 0.53 | 0.00 | −46,665.63 |
| 36 | 4 | 3 | 33 | 0.911007 | 0.909123 | 0.001884 | 98,698.00 | 6.42 | 0.00 | 422.51 | 625.74 | 0.33 | 2,960.94 | +94,682.06 |
| … | | | | | | | | | | | | | | |
| 192 | 17 | 16 | 46 | 0.699318 | 0.687606 | 0.011712 | 74,649.23 | 28.35 | 0.00 | 1,905.39 | 546.67 | 0.35 | 2,239.48 | +69,928.99 |
| 204 | 18 | 17 | — | 0.685126 | 0.672338 | 0.012788 | 0.00 | 37.76 | 0.00 | 2,005.55 | 540.93 | 0.43 | 0.00 | −2,584.68 |
| **215** | **18** | 17 | — | 0.672321 | 0.659771 | 0.012549 | 0.00 | 37.41 | **470,609.46** | 1,195.15 | 530.82 | 0.43 | 0.00 | −472,373.26 |
| **239** | **20** | 19 | — | 0.645072 | 0.633031 | 0.012041 | 0.00 | 30.17 | 64,504.36 | 1,062.39 | 519.54 | 0.56 | 0.00 | −66,117.02 |
| **263** | **22** | 21 | — | 0.618782 | 0.607233 | 0.011550 | 0.00 | 31.98 | 0.00 | 0.00 | 508.39 | 0.64 | 0.00 | −619,291.48 |

`claims_maturity` is 618,750.47 at `t = 263`, the last month, and zero elsewhere;
`claims_ph_death` is 0.00 in every month, because `wv_frac` = 1.00.

**Trace, `t = 0` (the first policy month) — and the `max` in `DB` finally switches.** Premium
= 108,564.00 × 1.000000 = 108,564.00. Child decrement: the annual rate is `q(0) = 0.00081`
and the monthly one `q_m(0) = 0.0000675251`, so `D(0) = 0.0000675251`. The death benefit is
`DB(0) = max(cumprem(1) − S·G(0) − L, Wb(1))` read at the end of the month: the
return-of-premiums limb is one annual premium, **¥108,564**, and the value limb is the
interpolated `Wb` at elapsed month 1, **¥9,304.50** — so the *premium* limb binds. Death
claims = 108,564 × 0.0000675251 = 7.33; claim expense = 1.35.

That is worth stopping on, because the notes' own instruction is that **both limbs must be
evaluated** and the annual grid never switched between them: at the first *anniversary* the
policy value has already reached ¥111,653.97 against one premium of ¥108,564, so the value
limb bound at every duration and a model that hard-coded it would have passed. The monthly
grid makes the crossover visible — cumulative premiums step up by a whole 年払 premium in
each anniversary month while the value accrues through the year to overtake it, so the
refund limb binds early in each policy year and the value limb late in it. It switches **85
times in 264 months**: eleven months of policy year 1, then fewer each year — ten, ten,
nine, eight … — until the value pulls clear for good in policy year 13. Hard-coding either
limb is right eleven months a year at best.

契約者 decrement: `q_p(0) = 0.00068` annually and `q_p,m(0) = 0.0000566843` a month, so
`Dp(0) = 0.0000566805`, all of it into the waived state. The surrender benefit is nil in the
first months for the same reason as on the 養老 cell: the interpolated value has not yet
outrun the 解約控除. Expenses = 50,000.00 + 8,000/12 = 50,666.67; commission = 0.90 × 108,564
= 97,707.60. `CF(0) = 108,564.00 − 7.33 − 1.35 − 50,666.67 − 97,707.60 = −39,818.95`.

**Trace, `t = 35` — the first staged benefit, and it is one month wide.** `g(3) = 0.05` falls
at the anniversary 3, which is the close of the month 35, so `claims_staged = 1,000,000 ×
0.05 × R(35) = 45,627.11` — paid to the waived state as well as to the paying one, and
nowhere else in the twelve months of policy year 3. The value falls by exactly that benefit
at the anniversary, which is the sourced constraint [S7] and is what the interpolation is
built to respect: `pol_val_pre_at_m(u)` runs from the value *after* the staged payment at one
anniversary to the value *before* the one at the next, so a 祝金 is never smeared backwards
over the twelve months preceding it.

**Trace, `t = 215` — the 70% payment.** The 契約者 decrement has been gone since the month 204
(`q_p = 0` from `12m = 204`), so `pols_wv` runs off on child mortality and surrender alone.
`claims_staged = 1,000,000 × 0.70 × R(215) = 470,609.46` in that one month, and the surrender
value falls by the ¥700,000 paid at that anniversary: `CV(17) = 1,738,755.93` against
`CV(18) = 1,056,811.08`.

**Roll-forward check.** `Σ D(t) = 0.004962269`, `Σ (1 − wv_frac) × Dp(t) = 0`,
`Σ Sr(t) = 0.376287258` and the maturing survivors 0.618750473, summing to **1.000000000**.
Undiscounted totals per policy issued: premiums 1,521,101.61; death claims 3,988.78; staged
benefits 771,160.39; maturity 618,750.47; surrender benefits 308,128.19; `claims_ph_death`
0.00; expenses 201,918.51 (maintenance 151,918.51, acquisition 50,000.00); claim expense
99.25; commission 140,083.73; `Σ CF(t)` = **−523,027.70**. Premium income and commission are
identical to the annual grid's. The maturing fraction **fell**, from 0.6303 to 0.6188, for
the same reason as on the 養老 cell: the final-period surrender carve-out is now one month
rather than twelve, so eleven more months of ordinary surrender run before maturity.

**What the waiver is worth on this cell.** Ignoring lapse, the cumulative probability of
entering the waived state over the 17 premium-paying years is **1.861464%**, and the EPV of
the waived premiums at 1.00% is **¥11,384.94** against a premium EPV of ¥1,702,626.54 —
**0.6687% of the premium stream**, or about a tenth of one annual premium. The amount at
risk is `P × (m − k)` at anniversary `k`: **¥1,845,588 at issue**, which is 1.85 times the
満期保険金 the contract
will pay, running off to zero at anniversary 17 while the maturity benefit is still five
years
away. Small probability, large amount, running off on a different schedule from every other
cash flow in the model — which is exactly the shape of error that survives a sensibility
check on the base case. In the projected stream it shows up only as the 1.7% of the last
premium-paying period's income that is missing, and in nothing else at all.

`henreiritsu()` returns **113.7849%** = 2,100,000 / 1,845,588, against the carrier's
published "approx. 113.7%" for exactly this plan [S11].

---

## Valuation and reserve pointers

This library projects gross liability cash flows. Every valuation layer consumes them and is
cited, never reproduced.

- **Standard policy reserve (*hyōjun sekinin junbikin*, 標準責任準備金).** 保険業法第116条 obliges the
  reserve and delegates the accumulation method and the level of the assumed coefficients
  for long-term contracts [REG-R4]. 施行規則第68条 fixes the scope, and a conventional 養老保険 or
  学資保険 with a fixed 予定利率 and a real 保険料積立金 is squarely **in** it [R3] [REG-R7]; 第69条 splits
  the reserve into 保険料積立金, 未経過保険料, 払戻積立金 and contingency reserve (*kiken junbikin*, 危険準備金),
  with net level premium method (*heijun jun-hokenryō-shiki*, 平準純保険料式) as the floor for
  anything out of scope [R3] [REG-R8]. 平成8年大蔵省告示第48号 sets the method (平準純保険料式, no Zillmer
  adjustment), the table (生保標準生命表2018（死亡保険用）for contracts concluded from 1 April 2018) and
  the standard valuation rate (*hyōjun riritsu*, 標準利率) machinery, which references the lower
  of the three-year and ten-year mean 10-year JGB yield and is determined annually [R4]
  [REG-R10] [REG-R11]; the 2021 amendments brought USD- and AUD-denominated contracts into
  scope from 2022-04-01, which is the currency boundary this yen composite sits inside [R5]
  [REG-R12]. **The current numeric 標準利率 could not be established from any retrieved official
  document** [R4] [R5], so `i_std` is **[std]** and defaults to `i_cv` = 1.00%, which makes
  `reserve_pp(k) − V(k) = SC(k)` exactly testable. 危険準備金 is prescribed by sub-class and is
  not modelled [R3] [REG-R8]; 価格変動準備金 under 保険業法第115条 is asset-driven and out of scope
  entirely [REG-R3]. `reserve_pp` produces no cash flow.
- **On this product the reserve is also a contractual amount, which the chassis's framing
  does not cover.** The 約款 use 積立金 and 責任準備金 interchangeably — one carrier defines 積立金 as
  the 責任準備金 for the base contract computed by the method the company determines [S2] [S3],
  and a second identically [S13] — and that quantity **floors a benefit**: the 学資 cell's
  死亡給付金 [S3] [S13], the refused claim [S2] [S8] and the war-risk reduction [S2] [S8] are all
  defined against it. A model that treats the reserve as purely a valuation output cannot
  compute this product's benefits, which is why `pol_val_pre_pp` is a cash-flow input and
  `reserve_pp` is not.
- **ESR.** From **31 March 2026** insurers are supervised on 経済価値ベースのソルベンシー規制, with
  liabilities at 現在推計 plus MOCE, re-measured at each 基準日 on assumptions re-set then,
  discounted on a prescribed curve and calibrated in principle to 99.5%; early corrective
  action triggers below **100%**, replacing the old ソルベンシー・マージン比率 **200%** trigger [REG-R15]
  [REG-R17]. This projection is the 現在推計 cash-flow engine and nothing more: `BEL = Σ_t v(t)
  × [outgo(t) − income(t)]` over the recursion above, with `v(t)`, MOCE and the
  standard-formula coefficients out of scope — the 柱告示 were not opened and their
  coefficients are [unverified] [REG-R16]. The regime change bites on *this* product
  specifically: a 30-year 養老保険 written at a 1.00% 予定利率 [S9] is a long, fixed, guaranteed
  maturity obligation, and the old basis was ロックイン; under a re-measured basis that guarantee
  is re-valued on each 基準日's curve.
- **The 意見書 chain.** 保険業法第121条第1項第1号 requires the 保険計理人 appointed under 第120条 to confirm in
  an 意見書 that the reserve is soundly accumulated [REG-R5] [REG-R6]; the IAJ 実務基準 turns that
  into the **1号収支分析**, a forward income-and-outgo analysis over at least ten future years by
  product segment under prescribed scenarios, with sufficiency tested over the first five
  [REG-R22].
- **Accounting.** **IFRS 17 is not mandatory in Japan** — IFRS applies as 指定国際会計基準 on a
  voluntary basis [REG-R47]. J-GAAP statutory reserving, the ESR economic balance sheet and
  IFRS 17 are three bases over one set of projected cash flows, and this model keeps the
  cash flows basis-agnostic, with discounting, margins and tax layered on top.
- **Disclosure, binding on the outputs rather than on the values.** The supervisory
  guideline requires the 解約返戻金 amount or its method to be disclosed and the 自動振替貸付 to be at
  the policyholder's election with prompt notice (監督指針 IV-1-10, IV-1-12) [REG-R14]; the
  statutory 説明義務 covers the surrender-value profile [REG-R39]. Both bear on a product whose
  surrender value is below cumulative premiums at every duration on both cells. The **返戻率**
  raises the sharper question: no FSA, 消費者庁 or 国民生活センター publication specific to its
  disclosure was located, so any claim that the disclosure is *regulated* would be
  [unverified] — the published ratios are carrier marketing disclosures, and on a 有配当 design
  part of the ratio is not guaranteed [REG-R38].
- **Tax is not modelled.** A lump-sum 満期保険金 is 一時所得 and a staged stream is 雑所得 [R6]
  [REG-R46]; premiums fall in the 一般生命保険料控除 basket [R7] [R8] [REG-R43]. `jplib` models
  contractual cash flows, not the policyholder's tax position.

---

## Key sensitivities and model risks

In rough order of leverage on this product:

1. **The maturity benefit, and how many policies reach it.** 0.4949 of the anchor cell's
   policies mature, and the payment is ¥2,474,504.99 against a ¥3,931,162.67 premium stream
   — 63% of all income leaves in **one month**, `t = 359`. Every lapse assumption is
   therefore a *maturity* assumption: the surrender-rate table moves the largest cash flow in
   the model through the survivorship factor, not through the surrender-benefit column. The
   monthly grid raised the leverage slightly rather than lowering it: the carve-out that
   stops the last surrender from colliding with the maturity payment is now one month rather
   than one policy year, so eleven more months of surrender run before the benefit falls and
   the maturing fraction is 0.4949 where the annual grid said 0.5042.
2. **The cash-value construction, and now also its within-year shape.** `i_cv` is sourced
   [S9], but `α` is **[std]** and carries the whole ¥899,875.29 surrender-benefit stream on
   the anchor cell. The monthly grid adds a second standardization on top of it: eleven
   readings in twelve are **interpolated [std]** between anniversaries, because the 算出方法書
   that would give the real within-year rule is unpublished [REG-R2]. Unlike the chassis,
   there is **no published surrender-value table for either cell to calibrate against** [S1]
   [S2] [S10], so the calibration is inherited rather than fitted, and the construction is
   more generous in the early durations than one carrier's qualitative description [S7]. A
   user with a real 算出方法書 replaces `pol_val_pp` and changes nothing else.
3. **The waiver decrement.** 1.48% cumulative probability against an amount at risk that
   starts at 1.85 times the maturity benefit. Omitting it understates the liability by 0.65%
   of the premium stream — small, but invisible: no claim column changes, only premium
   income. Holding `wv_load` at 1.00 additionally *excludes* the accident-caused 身体障害
   trigger that three of six carriers write [S1] [S10] [S16], so the base run is on the low
   side twice over.
4. **The staged schedule.** Total receipts range from 100% to 400% of 基準保険金額 across the six
   carriers [S1] [S3] [S7] [S10] [S13] — a four-fold spread that is an artefact of how each
   scales 基準保険金額. A model that treats the grid as anything but data is modelling one
   carrier.
5. **The −1.745% loading on the second cell.** A composite that takes a premium from one
   carrier and a 予定利率 from another produces a net premium above the gross premium, which no
   real product carries. It is visible, it is a derived output, and it is why the
   internal-rate diagnostics are printed beside it. It is also what makes the education
   cell's death benefit switch limbs 85 months in 264 on this grid, where the annual grid
   never switched at all.
6. **The 予定利率 / 標準利率 gap.** The 予定利率 is sourced at 1.00% [S9]; the numeric 標準利率 could not be
   established [R4] [R5]. On a guaranteed 30-year maturity obligation the spread between
   them determines whether the statutory reserve behaves at all, and `reserve_pp ≥ V ≥ CV`
   is not an invariant under 逆ざや.
7. **Mortality margin, and its two signs.** `mort_be_factor = 1.00` puts the base run on a
   valuation table with a roughly-2σ margin [REG-R20]. On the anchor cell claims move
   proportionately; on the second cell the child decrement contributes ¥3,988.78 against
   ¥1.52m of premium income and moving it changes almost nothing, while the same margin on
   the 契約者 is the difference between a prudent and a best-estimate waiver cost.
8. **復活, and the 学資金 that survives a lapse.** Not modelled, so in force is understated; and
   on this product a lapse does not even extinguish a benefit already due, because two
   carriers pay a 学資金 whose date fell during the lapsed period once the policy is reinstated
   [S1] [S10].
9. **Common-accident dependence between the two lives.** The composite treats them as
   independent **[std]** because no retrieved document gives a dependency. Where the 契約者 is
   the child's parent, the joint event is exactly the one that matters and it is unmodelled.

Known modeling pitfalls:

- **The maturity benefit is certain, not a decrement.** At the end of month `t = 12n − 1`,
  whose closing instant is anniversary `n`, the survivors are paid `S` with probability 1
  [R10] [S2] [S8]. Modelling maturity as a rate, or letting the projection run past
  `t = 12n − 1` on a terminal age imported from the whole-life chassis, is wrong in both
  directions.
- **Surrender must be suppressed in the final month, and only in it.** A surrender at the
  close of the last month and the maturity payment fall at the same instant at the same
  amount; running both double-counts the terminal payment, and running the surrender instead
  of the maturity misclassifies 61% of the anchor cell's undiscounted outgo into the wrong
  column. On the monthly grid the carve-out is `t = 12n − 1` alone: suppressing the whole
  final *year*, as an annual grid necessarily did, deletes eleven months of genuine
  surrender and overstates the maturing fraction — which is exactly the 0.5042 → 0.4949 move
  the conversion produced on the anchor cell.
- **The policy value must converge on the maturity benefit.** `pol_val_pp(n) == sum_assured`
  exactly at the final anniversary, on **both** cells. That identity is what makes an
  endowment a real test of a
  savings model, and it is the one thing a whole-life chassis can never check.
- **Two lives, two decrements, one policy.** The waiver runs on the 契約者's mortality at
  `y + ⌊t/12⌋`; every benefit runs on the 被保険者's at `x + ⌊t/12⌋` [S1] [S10]. Reading one table at
  one age for both is the most likely implementation error on the second cell — and on the
  anchor cell the two ages coincide, so it will not show there.
- **The 契約者 decrement stops at `12m`.** Every waiver trigger is conditional on the event
  falling during 保険料払込期間 [S1] [S10]. The premium-paying months are `t = 0 … 12m − 1`, so
  carrying `q_pm` to `t = 12m` and beyond moves policies out of the paying state the contract
  leaves in it, and does so in exactly the years when 86% of the second cell's receipts fall.
- **The three clocks are not interchangeable.** `t` counts **months** from 0; `k` is an
  anniversary **in years** with `k = 0` at issue; `u` is an **elapsed month** at which a
  value is read, `u = t + 1` for the flows of month `t`. Reading a value cells at `t` rather
  than at `t + 1` gives the row its *opening* balance and silently misstates every surrender
  benefit, every 学資 death benefit and every staged claim; reading `cv_pp(t)` where
  `cv_at_m(t + 1)` is meant is worse, because it is off by a factor of twelve in the index
  and still returns a plausible number. `SC(0)`, `W(n) = S` and the schedule's
  3 / 6 / 12 / 15 / 18 / 20 are all on the `k` clock in years, and **none of them moved**
  when the projection index became a month.
- **Only the projection index became monthly.** The contractual constructions did not: the
  policy value, the surrender charge, the surrender value, the loan balance and the staged
  schedule are all defined at the 年単位の契約応当日 and all stayed annual. Converting *them* to
  a monthly recursion would invent a within-year rule the 算出方法書 does not publish
  [REG-R2]; what the model does instead is read them between anniversaries by a declared
  interpolation and agree with them exactly at every anniversary.
- **The waiver produces no benefit outgo.** It removes premium income and leaves every claim
  column unchanged [S1] [S10] [S13]. Booking a "waiver benefit" double-counts; and because
  omitting the waiver altogether changes no claim column either, neither error is visible in
  a benefit reconciliation.
- **Premiums on a waived policy are deemed paid.** The return-of-premiums death benefit
  keeps growing at `P × min(⌈u/12⌉, m)` on a policy that pays nothing, and the surrender value is
  the same in both states for the same reason [S1] [S10] [S13]. Netting the waived premiums
  out of either understates both.
- **高度障害 is inside the death rate; accident-caused 身体障害 is not.** 生保標準生命表2018（死亡保険用）already
  includes 高度障害 [REG-R20] [R2], so a separate disability decrement on the 被保険者 double-counts
  — but the waiver's third trigger, 身体障害 from a listed accident within 180 days [S1] [S10]
  [S16], is genuinely additional and `wv_load` = 1.00 leaves it out. The two cases point
  opposite ways.
- **A waiver carve-out terminates the contract; it does not merely remove the waiver.**
  Three-year suicide of the 契約者, the 後継保険契約者's intentional act and war each end the policy
  against the 責任準備金 paid to the 契約者's heirs [S1] [S7] [S10]. `claims_ph_death` is zero in
  the base run and must become non-zero as soon as `wv_frac < 1`.
- **The staged benefit is not a claim and not a decrement.** It is paid on survival at a
  fixed date to a policy still in force, in **both** states, and it terminates nothing [S10]
  [S11]. Weighting it by a decrement rate, or paying it only from the premium-paying state,
  understates it.
- **Each staged benefit reduces the surrender value by its own amount.** `CV` falls from
  1,738,755.93 to 1,056,811.08 across anniversaries `k = 17 → 18` on the second cell, and one carrier
  computes the value from the elapsed months **and** the 学資金 timing [S1] [S7]. A model that
  pays the staged benefit beside the value rather than out of it inflates every later
  surrender.
- **The staged schedule is data.** It is read from a table keyed by `schedule_id`, and the
  `J` variant — one payment of 100%, then maturity — must run without touching the code
  [S10].
- **Both limbs of the 学資 death benefit must be evaluated, and on this grid both bind.** On
  the annual grid the reserve limb dominated at every *anniversary* and the `max` never
  switched. Read month by month it switches **85 times in 264**: the premium limb steps up by
  a whole 年払 premium in each anniversary month and the value accretes through the year to
  overtake it, so the refund limb binds early in each policy year and the value limb late in
  it, until the value pulls clear for good in policy year 13. Hard-coding either limb is
  right eleven months a year at best — and the annual grid could not have told anyone that
  [S3] [S13].
- **`henreiritsu()` is a contractual ratio, not a model output ratio.** It reads `P × m` and
  the scheduled benefits, never the projected premium income or the probability-weighted
  claims; it is undefined for a policy that surrenders and unbounded for one that is waived;
  and computed from a 月払 premium it sits below the carrier's own published 年払 figure [S11]
  [S16]. It did not move when the grid did, and it should not have: `ρ` is a ratio of
  contractual amounts, not of projected ones.
- **There is no cliff on this product.** No retrieved document offers a 低解約返戻金型 form of
  either cell. Importing the chassis's 0.70 suppression multiplier, its step at `m`, or its 15%
  surrender spike models a product that does not exist here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-endowment-r1
[R10]: #jplib-endowment-r10
[R2]: #jplib-endowment-r2
[R3]: #jplib-endowment-r3
[R4]: #jplib-endowment-r4
[R5]: #jplib-endowment-r5
[R6]: #jplib-endowment-r6
[R7]: #jplib-endowment-r7
[R8]: #jplib-endowment-r8
[R9]: #jplib-endowment-r9
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R12]: #jplib-reg-r12
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R16]: #jplib-reg-r16
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R24]: #jplib-reg-r24
[REG-R3]: #jplib-reg-r3
[REG-R31]: #jplib-reg-r31
[REG-R34]: #jplib-reg-r34
[REG-R35]: #jplib-reg-r35
[REG-R38]: #jplib-reg-r38
[REG-R39]: #jplib-reg-r39
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R43]: #jplib-reg-r43
[REG-R46]: #jplib-reg-r46
[REG-R47]: #jplib-reg-r47
[REG-R5]: #jplib-reg-r5
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
