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
- **Projection frequency.** **Annual**, on policy years running anniversary to anniversary
  (`Endowment_JP_A`). The only intra-year contractual structure on the composite is the
  calendar date of each 学資金 — the 11月1日 following a stated attained age at the adopted
  carrier [S10], and four other fixed dates elsewhere [S1] [S3] [S7] [S13] — and the annual
  grid resolves every one of them to the policy anniversary following that age
  (`product-spec.md` footnote 13). No amount changes; the timing of each staged payment
  moves by between one and five months, always forward, always inside one policy year.
- **Timing conventions [std].** Premium at the **start** of each policy year, in advance,
  for years 1 … `m`; maintenance expense and renewal commission at the start of each year;
  acquisition expense and initial commission at issue (start of year 1); death claims and
  claim expenses at the **end** of the policy year of death; the 学資金 and the 満期保険金 at the
  **end** of the policy year, to policies surviving that year's mortality; surrenders at the
  end of the policy year, **after** deaths and **after** any staged benefit due at that
  anniversary, valued on the surrender value net of that benefit.
- **Age basis — two ages, not one.** 契約年齢 is attained age (*man-nenrei*, 満年齢) with the
  fractional year discarded at 契約日, incrementing on each 年単位の契約応当日 rather than on the
  birthday [S1] [S2] [S10] [S13]. The attained age of the 被保険者 in year `t` is therefore `x +
  t − 1` exactly. **On the 学資 cell there is a second age**, the 契約者's `y + t − 1`, which
  runs an entirely separate decrement over `t = 1 … m` only. Both model cells sit at exact
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
  age. The projection length is exactly the 保険期間: `T = n`. Every state closes at `t = n`,
  and the closing cash flow is a **certain payment of `S` to the survivors**, not a
  decrement. The chassis runs to the table's terminal age ω because a 終身保険 has no expiry;
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
129.2%, is quoted on a 一括払込 basis [S14]. The model's derived 返戻率 is therefore a
**monthly-basis ratio evaluated on an annual grid** and sits below a true 年払 figure.

`schedule_id = none` on the 養老 cell is a product fact, not a missing value: the survival
benefit is a single payment at `t = n` and there is no staged schedule at all.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | **Total** in-force probability at the start of policy year t, `pols_if = pols_if_pay + pols_wv`; `pols_if(1) = 1` | sum of the two states |
| `pols_if_pay(t)` | In-force probability in the **premium-paying** state at the start of policy year t; `pols_if_pay(1) = 1` | annual recursion |
| `pols_wv(t)` | In-force probability in the **waived** state at the start of year t; `pols_wv(1) = 0`; identically 0 on the 養老 cell | annual recursion |
| `mort_rate(t)` | 被保険者 mortality (incl. 高度障害) in year t | table lookup at `x + t − 1` |
| `mort_rate_ph(t)` | 契約者 mortality driving the waiver, `t ≤ m` only; 0 on the 養老 cell | table lookup at `y + t − 1` |
| `lapse_rate(t)` | Voluntary surrender rate in year t | assumption table |
| `default_rate(t)` | Premium-default rate feeding the APL module (0 in base) | assumption table |
| `benefit_pct(t)` | `g(t)` — the staged benefit due at anniversary t, as a fraction of `S` | schedule table |
| `pol_val_pp(t)` | `W(t)` — policy value at anniversary t, **after** any staged benefit due at t | closed form |
| `pol_val_pre_pp(t)` | `Wb(t) = W(t) + S × g(t)` — the same value **before** that benefit | closed form |
| `surr_charge_pp(t)` | `SC(t)` — the acquisition deduction embedded in the surrender value | closed form |
| `cv_pp(t)` | `CV(t)` — payable 解約返戻金 at anniversary t | closed form |
| `reserve_pp(t)` | 平準純保険料式 policy reserve, reference quantity only — **never a cash flow** | closed form |
| `loan_pp(t, s)` | Outstanding APL + 契約者貸付 principal and interest, by entry year `s` | chassis recursion |

The base run carries no loan and no APL cohort: `default_rate ≡ 0` and `pol_loan_util = 0`,
so `loan_pp ≡ 0` and every benefit is gross. The APL triangle, its exhaustion test and its
clawback are the chassis's and are exercised in both positions there.

**There is no `low_cv` and no `k`.** No retrieved document offers a suppressed-surrender-value
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
| 満期保険金 — 養老 cell | `S` on survival to `t = n`, **equal to the death benefit** | [R10] [S2] [S8] |
| 高度障害 / 重度障害 — 養老 cell | Deemed death on the notice date; no separate payment | [S2] [S15] |
| Premium `P` | Level and guaranteed for years 1 … `m`; none thereafter | [S1] [S2] [S8] [S10] |
| Staged 学資金 `g(t)` | 5% / 5% / 10% / 10% / 70% / 10% of `S` at `t` = 3 / 6 / 12 / 15 / 18 / 20 | [S10] [S11]; grid **[std]**, timing **[std]** |
| 満期保険金 — 学資 cell | `S` at `t = n = 22`; total receipts 210% of `S` | [S10] [S11] |
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
as `α × SA × max(0, m − t) / m` with `α` = 0.0090, calibrated against a published table.
That form is meaningless on the 学資 cell, where 基準保険金額 is a **benefit-scaling unit and not a
sum assured** — total premiums are 1.85 times it. The deduction is therefore re-based on one
annual premium **[std]**:

    SC(t) = α × P × max(0, m − t) / m,     α = 0.25

On the anchor cell that is `SC(0)` = ¥45,285, within 0.7% of the ¥45,000 the chassis
calibrated against a real published surrender-value run — so the only piece of genuine
Japanese surrender-value calibration in this library is carried across rather than
discarded. The construction satisfies the three sourced quantitative constraints [S7]: the
value is below cumulative premiums at every duration on both cells (rising monotonically to
92.0% at `t = n` on the 養老 cell; on the 学資 cell the ratio saw-tooths with the schedule,
peaking at 98.4% at `t = 11` — the year before the third 学資金 — and standing at 94.2% at `t
= m`), it is capped at the death benefit, and each 学資金 reduces it. It does **not**
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
the male table [R1] [REG-R18], and the whole 22-year child decrement contributes ¥4,120.71
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

| Policy year `t` | 1 | 2 | 3 … n−1 | **n** |
|---|---|---|---|---|
| `lapse_rate(t)` **[std]** | 4% | 3% | 2% | **0%** |

On the waived state the same table applies, multiplied by `wv_lapse_mult` = **1.00 [std]**.
The premium-default rate `u(t)` that feeds the APL module sits in the same table and is
**1.0% / 0.8% / 0.6% [std]** on the same 1 / 2 / 3-onwards shape, gated to zero in the base
run by `apl_default_mult` = 0. No retrieved document gives a default rate for either cell,
so it too is inherited from the chassis for the same comparability reason.

The 4 / 3 / 2 shape is inherited from the chassis so that the two products stay comparable.
Two deltas. First, **there is no cliff and therefore no spike**: the chassis's 17% at `t =
m` exists only because a 低解約返戻金型 surrender value steps up by `1/k` at 払込満了, and neither cell
has one. Second, `lapse_rate(n) = 0` **[std]**: a surrender at the end of the final policy
year and the maturity payment fall on the same anniversary, and an owner one year from a
guaranteed `S` does not take `CV(n) = S` early. Setting it to anything else double-counts
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
| Renewal commission `c_r` | 3% of premium, years 2 … `m`, **on the premium-paying state only** **[std]** |
| Maintenance expense `e(t)` | ¥8,000 p.a. to `t = n`, inflating at 1.0% p.a., **on both states** **[std]** |
| Claim expense `ec` | ¥20,000 per death claim **[std]** |
| Maturity and staged-benefit expense | None — folded into maintenance **[std]** |

Renewal commission on the paying state only and maintenance on both is not a detail: a
waived policy costs the insurer administration and pays the distributor nothing.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy year, t = 1 … n; the 被保険者's attained age in year t is `x + t − 1` |
| `x`, `y` | 契約年齢 of the 被保険者 and of the 契約者 (学資 cell only) |
| `n`, `m` | 保険期間 in years; 保険料払込期間 in years, `m ≤ n` |
| `S`, `P` | 基準保険金額; annual premium, payable at the start of years 1 … m |
| `g(t)` | staged 学資金 due at anniversary t, as a fraction of `S`; 0 on the 養老 cell |
| `G(t)` | `Σ_{s ≤ t} g(s)` — cumulative staged fraction paid to and including t |
| `q(t)`, `q_p(t)` | 被保険者 mortality in year t; 契約者 mortality in year t, zero for t > m |
| `w(t)`, `u(t)` | voluntary surrender rate; premium-default rate (APL module) |
| `l(t)` | **total** in-force probability at the start of year t (`pols_if`), `l = l_p + h` — the same `l` the 終身 and 外貨建 chassis use, where there is only one state |
| `l_p(t)`, `h(t)` | in-force probability in the paying state (`pols_if_pay`) and the waived state (`pols_wv`) |
| `D(t)`, `Dp(t)` | expected 被保険者 deaths in year t; expected 契約者 decrements in year t |
| `R(t)` | expected in force at the anniversary, after mortality, before surrender |
| `Sr(t)` | expected surrenders in year t |
| `A(z, k)`, `ä(z, k)` | k-year endowment-assurance EPV of 1 at age z; k-year annuity-due, both on `i_cv` and the table |
| `π`, `π_g` | net level premium on the cash-value basis, 養老 cell and 学資 cell |
| `W(t)`, `Wb(t)` | policy value at anniversary t, after and before the staged benefit due at t |
| `SC(t)`, `V(t)`, `CV(t)` | acquisition deduction; ordinary surrender value; payable 解約返戻金 |
| `DB(t)` | death benefit for a death in year t |
| `L(t)` | loan + APL principal and interest at the start of year t |
| `i_cv`, `i_L`, `i_std` | cash-value basis rate; loan rate; reference valuation rate |
| `α` | acquisition-deduction rate, per unit of one annual premium |
| `E0`, `e(t)`, `c0`, `c_r`, `ec` | acquisition expense; maintenance; initial and renewal commission; claim expense |
| `CF(t)` | net cash flow of year t, **income-positive** (`net_cf`) |
| `ρ` | 返戻率 — the derived return ratio (below) |

**Dimensional check.** `q`, `q_p`, `w`, `u`, `g`, `G`, `α`, `c0`, `c_r`, `l`, `h` and `ρ`
are dimensionless, and so are `l_p` and `q_p`; `i_cv`, `i_L`, `i_std` are per annum; `A` and `ä` are pure numbers (`ä`
in years of premium, so `S × A / ä` is ¥ per year); `S`, `P`, `W`, `Wb`, `SC`, `V`, `CV`,
`DB`, `L`, `E0`, `e`, `ec` are ¥; every term of `CF(t)` is ¥ per policy issued per year.
`g(t)` is a fraction of `S`, never of a premium — the two are within a factor of two of each
other on the second cell, so the check is not idle.

### The staged schedule is data

`g(t)` is read from `benefit_schedule_table.csv`, keyed by `schedule_id`, one row per
payment, with a `provenance` column on every row:

    schedule_id   t   benefit_pct   provenance
    S_0_1         3   0.05          S型 grid, child 契約年齢 0-1 [S10]; timing [std]
    S_0_1         6   0.05          "
    S_0_1        12   0.10          "
    S_0_1        15   0.10          "
    S_0_1        18   0.70          "
    S_0_1        20   0.10          "
    J            18   1.00          J型 degenerate variant [S10]; timing [std]

The 満期保険金 of 100% at `t = n` is **not** a schedule row: it is always present, on both cells,
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
    W(t)   = S × A(x + t, n − t) − π × ä(x + t, max(m − t, 0))
    Wb(t)  = W(t)                                        (g is identically zero)
    DB(t)  = S − L(t)

where `A(z, k)` is the k-year endowment assurance — 1 at the end of the year of death within
k years, or 1 on survival to k. At `t = n`, `A(x + n, 0) = 1` and `ä(·, 0) = 0`, so **`W(n)
= S` exactly, by construction**. That identity is why the 養老 cell is a better test of a
savings model than the chassis is: a whole-life reserve that drifts can hide for decades,
while an endowment reserve that does not converge on its own maturity benefit is wrong on
the first run.

**学資 cell — survival benefits only, because the death benefit releases the value.**

    EPV(t) = S × [ Σ_{s > t} g(s) · v^(s−t) · (s−t)p_(x+t)  +  v^(n−t) · (n−t)p_(x+t) ]
    π_g    = EPV(0) / ä(x, m)
    W(t)   = EPV(t) − π_g × ä(x + t, max(m − t, 0))
    Wb(t)  = W(t) + S × g(t)
    DB(t)  = max( P × min(t, m) − S × G(t − 1) − L(t),  Wb(t) )

The `Σ_{s > t}` is what makes `W(t)` the value **after** the staged benefit due at `t`,
which is the sourced fact that each 祝金 reduces the surrender value [S7] and that one carrier
computes the value from the elapsed months **and** the 学資金 timing [S1]. Excluding the death
benefit from the EPV is the **[std]** step, and it is one carrier's own wording read
literally: its 死亡払戻金 *is* the 責任準備金相当額 [S10], so on that design the decrement is exactly
value-neutral, and the composite's max-form dominates it [S3] [S13]. At `t = n` there is no
future staged benefit and no future premium, so **`W(n) = S` exactly** here too.

Then, on both cells,

    SC(t) = α × P × max(0, m − t) / m
    V(t)  = max(0, W(t) − SC(t))
    CV(t) = V(t)

with **no 低解約返戻金型 multiplier**: `CV` and `V` are the same series on this product.

**The premium term in `DB(t)` is deemed-paid, not cash-paid.** `P × min(t, m)` counts every
premium falling due to `t`, whether or not the 契約者 was alive to pay it, because the waiver
provides that each future premium is *treated as having been paid* on its 契約応当日 [S1] [S10]
[S13]. The same wording is why **`CV(t)` is identical in both states**: the surrender value
is computed as if the premiums had been paid, so the waived and paying states share one
policy value. A model that keeps two value series is modelling a contract nobody wrote.

### The waiver as a state transition, not a benefit

`W(t)` is the reference quantity for the reserve; the waiver produces **no outgo line at
all**. What it produces is the absence of premium income, which is why it can be omitted
without any claim column looking wrong. On the 学資 cell, for `t = 1 … n`:

    q_p(t)        = 0  for t > m                          (no premium left to waive)
    l(t)          = l_p(t) + h(t)                         (total in force)
    D(t)          = l(t) × q(t)                            (被保険者 deaths, both states)
    Dp(t)         = l_p(t) × (1 − q(t)) × q_p(t)            (契約者 decrements, paying only)
    to waived     = wv_frac × Dp(t)
    terminating   = (1 − wv_frac) × Dp(t)                 (pays Wb(t) to the heirs)

    l_p_after(t)  = l_p(t) × (1 − q(t)) × (1 − q_p(t))
    h_after(t)    = h(t) × (1 − q(t)) + wv_frac × Dp(t)
    R(t)          = l_p_after(t) + h_after(t)

    l_p(t + 1)    = l_p_after(t) × (1 − w(t))
    h(t + 1)      = h_after(t) × (1 − wv_lapse_mult × w(t))

The two lives are **independent [std]** — no retrieved document gives a dependency and none
could. Where the 契約者 is the child's parent, common-accident dependence is real and
unmodelled.

**`q_p(t) = 0 for t > m` is a modelling ruling and earns its own sentence.** The 約款 make
every waiver trigger conditional on the event falling *during* 保険料払込期間 [S1] [S10], and the
termination-without-waiver path is the failure mode of that same provision [S1] [S7] [S10].
After 払込満了 there is no premium to waive and nothing for the provision to fail at, so the
composite **[std]** treats the contract as continuing through the 契約者's death by succession
[S1] [S7] [S10] [S13] and drops the second decrement entirely. On the second cell that
covers five years of the 22-year term — the years in which 86% of the receipts fall — and
carrying the decrement through them would terminate a further 0.8367% of policies and
delete their maturity benefits.

### Processing order (policy year t = 1 … n)

1. **Start of year — premium.** Collect `P × l_p(t)` if `t ≤ m` — on the **paying** state
   alone, never on `l(t)`. The waived state is in force and pays nothing. On an APL cohort
   the premium is not collected in cash: the advance is applied to it and it appears only as
   growth in `L` (chassis).
2. **Start of year — expenses and commission.** `e(t) × l(t)`, on the whole in force;
   renewal commission `c_r × P × l_p(t)` for `2 ≤ t ≤ m`, on the paying state only. At
   `t = 1` additionally `E0` and `c0 × P`.
3. **Start of year — APL test** (module on). Chassis, unchanged, run against `CV`.
4. **Values.** Compute `W(t)`, `Wb(t)`, `SC(t)`, `V(t)`, `CV(t)` at the year-end
   anniversary.
5. **End of year — 被保険者 deaths.** `D(t) = l(t) × q(t)`, on the whole in force; outgo
   `DB(t) × D(t)`,
   floored at zero; claim expense `ec × D(t)`.
6. **End of year — 契約者 decrement**, on the paying state only and only for `t ≤ m`: split by
   `wv_frac` into a transition to the waived state and a termination paying `Wb(t)`.
7. **End of year — staged benefit.** `S × g(t) × R(t)`, to everything in force at the
   anniversary, in **both** states. It is not a decrement and it terminates nothing.
8. **End of year — maturity, at `t = n` only.** `S × R(n)`.
9. **End of year — surrenders**, on survivors of both mortality decrements, valued on
   `CV(t)` — that is, **net of the staged benefit just paid**: `Sr(t) = l_p_after(t) × w(t)
   + h_after(t) × wv_lapse_mult × w(t)`; outgo `max(0, CV(t) − L(t)) × Sr(t)`.
10. **Loan roll-up and in-force update** per the chassis, then `l_p(t+1)` and `h(t+1)` above.
11. **At `t = n`** everything closes: `l(n + 1) = l_p(n + 1) = h(n + 1) = 0`. There are no
    tail states.

### Net cash flow

Income-positive, per policy issued:

    CF(t) = P × l_p(t) × 1{t <= m}                        (premiums)
          − DB(t) × D(t)                                  (被保険者 death claims)
          − ec × D(t)                                     (claim expense)
          − Wb(t) × (1 − wv_frac) × Dp(t)                 (契約者 death, waiver refused)
          − S × g(t) × R(t)                               (staged 学資金)
          − S × R(n) × 1{t = n}                           (満期保険金)
          − max(0, CV(t) − L(t)) × Sr(t)                  (surrender benefits)
          − e(t) × l(t)                                   (maintenance expense)
          − c_r × P × l_p(t) × 1{2 <= t <= m}             (renewal commission)
          − (E0 + c0 × P) × 1{t = 1}                      (acquisition)

`net_cf` is income-positive throughout; where an outgo-positive orientation is printed it
survives as `liability_cf`, with `net_cf(t) == −liability_cf(t)`. The result columns are
`premiums`, `claims_death`, `claims_staged`, `claims_maturity`, `claims_lapse`,
`claims_ph_death`, `expenses`, `claim_expenses`, `commissions` and `net_cf`, with `pols_if`
first, then `pols_if_pay` and `pols_wv` beside it. `claims_staged` and `claims_ph_death` are
named for the `kind` arguments `"STAGED"` and `"PH_DEATH"` that produce them.

**`expenses` is the policy expense and nothing else.** The `expenses` column carries `E0`
and `e(t)`; the claim handling expense `ec × D(t)` is a per-claim cost, not a per-policy
one, and it is published as its own `claim_expenses` column and deducted explicitly in
`CF(t)` above. The worked example below therefore prints the two as two columns.

**Roll-forward identity.** Every policy leaves by exactly one route and the term is finite:

    Σ_t D(t) + Σ_t (1 − wv_frac) × Dp(t) + Σ_t Sr(t) + R(n) = 1,   and   l(n+1) = 0

`check_pols_roll_fwd()` takes no argument and returns a bool over all `t`; the per-`t`
signed residual lives at `check_pols_roll_fwd_resid(t)`. A second check has no analogue on
the chassis: `check_pol_val_terminal()` asserts `pol_val_pp(n) == sum_assured` to the
displayed precision, on both cells.

### 返戻率 as a derived output

The number both products are sold on is a ratio of **contractual amounts on one policy that
survives, pays every premium, takes every benefit in cash and receives no dividend** — not a
probability-weighted quantity, not discounted, not net of tax:

    ρ = ( S × Σ_t g(t) + S ) / ( P × m )

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
  from a 月払 premium on an annual grid is a lower bound on the carrier's own figure.

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
  The chassis's form carries over, `w_dyn(t) = w(t) × min(3.0, max(1.0, 1 + β × max(0, CV(t)
  / cumprem(t) − 1)))` with `β` = 2.0 **[std]** and `cumprem(t) = P × min(t, m)`. On the
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
  independent multiplier on a premium stream. The annual grid has no arrears state, so the
  interaction is out of scope and named rather than approximated.

---

## Worked example

**Every figure below was recomputed numerically before it was written.**

### Anchor cell (`point_id = 1`) — 養老保険

Male, 契約年齢 30 (満年齢), 基準保険金額 ¥5,000,000, 保険期間 30 years (満期 at attained age 60), 保険料払込期間 30
years, annual premium **¥181,140** (= 12 × the published ¥15,095 monthly premium for exactly
this cell [S9]). `T = n = 30` policy years, attained ages 30 to 59. 死亡保険金 = 満期保険金 =
¥5,000,000 [R10] [S2] [S8]. No waiver, no loan, no APL, no dividend.

**Assumption values used, in full.** `i_cv` = **1.00%** [S9]; `α` = **0.25** of one annual
premium, so `SC(0)` = ¥45,285 **[std]**; `mort_be_factor` = **1.00 [std]**; `lapse_rate` = 4% /
3%
/ 2% … 2% / **0% at t = 30** **[std]**; `E0` = ¥50,000, `c0` = 0.90, `c_r` = 0.03, `e(t)` =
¥8,000 × 1.01^(t−1), `ec` = ¥20,000, all **[std]**; `i_L` = 2.40% [S9], unused because
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
¥35,243.66, 19.457% of the gross premium. The resulting values, with `SC(t) = 0.25 × 181,140
× (30 − t) / 30`:

| t | `W(t)` | `SC(t)` | `CV(t)` | cumulative premiums | `CV(t)` / cum. prem. |
|---|---|---|---|---|---|
| 1 | 144,053.26 | 43,775.50 | 100,277.76 | 181,140 | 55.4% |
| 5 | 735,250.45 | 37,737.50 | 697,512.95 | 905,700 | 77.0% |
| 15 | 2,313,975.49 | 22,642.50 | 2,291,332.99 | 2,717,100 | 84.3% |
| 29 | 4,804,598.71 | 1,509.50 | 4,803,089.21 | 5,253,060 | 91.4% |
| **30** | **5,000,000.00** | **0.00** | **5,000,000.00** | **5,434,200** | **92.0%** |

`W(30) = S` exactly, which is the identity `check_pol_val_terminal()` asserts, and the last
column never reaches 100% — this contract does not return its premiums even at maturity.

**First periods of the base run.** Per policy issued, income-positive, to two decimal
places. The `expenses` column carries maintenance, and at `t = 1` the acquisition expense as
well; the claim handling expense is the separate `claim_expenses` column beside it.
`pols_if` is the total in force, which on this cell equals `pols_if_pay` because there is no
waiver and therefore no second state.

| t | age | q(t) | `pols_if(t)` | premiums | claims_death | claims_maturity | claims_lapse | expenses | claim_expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 30 | 0.00068 | 1.000000 | 181,140.00 | 3,400.00 | 0.00 | 4,008.38 | 58,000.00 | 13.60 | 163,026.00 | −47,307.98 |
| 2 | 31 | 0.00069 | 0.959347 | 173,776.15 | 3,309.75 | 0.00 | 7,113.43 | 7,751.53 | 13.24 | 5,213.28 | 150,374.92 |
| 3 | 32 | 0.00070 | 0.929925 | 168,446.56 | 3,254.74 | 0.00 | 7,357.98 | 7,588.93 | 13.02 | 5,053.40 | 145,178.50 |
| 4 | 33 | 0.00072 | 0.910688 | 164,962.07 | 3,278.48 | 0.00 | 9,936.68 | 7,506.26 | 13.11 | 4,948.86 | 139,278.67 |
| 5 | 34 | 0.00074 | 0.891832 | 161,546.43 | 3,299.78 | 0.00 | 12,432.08 | 7,424.35 | 13.20 | 4,846.39 | 133,530.63 |
| … | | | | | | | | | | | |
| 29 | 58 | 0.00548 | 0.520387 | 94,262.89 | 14,258.60 | 0.00 | 49,715.35 | 5,500.66 | 57.03 | 2,827.89 | 21,903.35 |
| **30** | 59 | 0.00598 | 0.507184 | 91,871.40 | 15,164.82 | **2,520,757.67** | 0.00 | 5,414.72 | 60.66 | 2,756.14 | **−2,452,282.61** |

**Trace, year 1.** `D(1) = 1.000000 × 0.00068 = 0.00068`; death claims = 5,000,000 × 0.00068
= 3,400.00; claim expense = 20,000 × 0.00068 = 13.60. Survivors of mortality `R(1) = 1 −
0.00068 = 0.999320`, so `Sr(1) = 0.999320 × 0.04 = 0.0399728`; `CV(1) = W(1) − SC(1) =
144,053.259234 − 43,775.50 = 100,277.759234`, so surrender benefits = 100,277.759234 ×
0.0399728 = 4,008.38. Expenses = 50,000.00 + 8,000.00 = 58,000.00, with the claim expense
13.60 beside them; commission = 0.90 × 181,140 = 163,026.00. `CF(1) = 181,140.00 − 3,400.00
− 13.60 − 4,008.38 − 50,000.00 − 8,000.00 − 163,026.00 = −47,307.98`. Update: `l_p(2) =
0.999320 × 0.96 = 0.9593472`.

**Trace, year 2.** Premiums = 181,140 × 0.9593472 = 173,776.15. `D(2) = 0.9593472 × 0.00069
= 0.00066195`; claims = 5,000,000 × 0.00066195 = 3,309.75; claim expense = 13.24. `R(2) =
0.9593472 × 0.99931 = 0.958685250`, so `Sr(2) = 0.958685250 × 0.03 = 0.028760558`; `CV(2) =
289,598.918098 − 42,266.00 = 247,332.918098`, so surrender benefits = 247,332.918098 ×
0.028760558 = 7,113.43. Maintenance = 8,000 × 1.01 × 0.9593472 = 7,751.53; renewal
commission = 0.03 × 181,140 × 0.9593472 = 5,213.28. `CF(2) = 173,776.15 − 3,309.75 − 13.24 −
7,113.43 − 7,751.53 − 5,213.28 = 150,374.92`. Update: `l_p(3) = 0.958685250 × 0.97 =
0.929924693`.

**Trace, year 3.** Premiums = 181,140 × 0.929924693 = 168,446.56. `D(3) = 0.929924693 ×
0.00070 = 0.000650947`; claims = 3,254.74; claim expense = 13.02. `R(3) = 0.929924693 ×
0.99930 = 0.929273746`, `Sr(3) = 0.929273746 × 0.02 = 0.018585475`; `CV(3) = 436,655.869405
− 40,756.50 = 395,899.369405`, so surrender benefits = 395,899.369405 × 0.018585475 =
7,357.98. Maintenance = 8,000 × 1.01² × 0.929924693 = 7,588.93; renewal commission =
5,434.20 × 0.929924693 = 5,053.40. `CF(3) = 168,446.56 − 3,254.74 − 13.02 − 7,357.98 −
7,588.93 − 5,053.40 = 145,178.50`.

**Trace, the maturity year `t = 30`.** `l(30) = 0.507184498`, `q(30) = 0.00598`, so `D(30) =
0.003032963` and death claims = 5,000,000 × 0.003032963 = 15,164.82, with claim expense
60.66. `R(30) = 0.507184498 × (1 − 0.00598) = 0.504151534`, and because `lapse_rate(30) = 0`
**every one of those survivors matures**: `claims_maturity` = 5,000,000 × 0.504151534 =
**2,520,757.67**. Maintenance = 8,000 × 1.01²⁹ × 0.507184498 = 5,414.72; renewal commission
= 5,434.20 × 0.507184498 = 2,756.14. `CF(30) = 91,871.40 − 15,164.82 − 60.66 − 2,520,757.67
− 5,414.72 − 2,756.14 = −2,452,282.61`, against +21,903.35 one year earlier. **The maturity
payment is the largest single item in the stream and it is one year wide**, and unlike the
chassis's cliff it is a *certain* payment rather than a behavioural one — the only
uncertainty in it is how many policies reach it.

**Roll-forward check.** Over the 30 years, `Σ D(t) = 0.043174852`, `Σ Sr(t) = 0.452673614`
and the maturing survivors `R(30) = 0.504151534`, summing to **1.000000000**, with `l(31) =
0.504151534` before the maturity payment and 0 after it. Undiscounted totals per policy
issued: premiums 3,931,162.67; death claims 215,874.26; maturity 2,520,757.67; surrender
benefits 887,154.17; expenses 247,991.55 (maintenance 197,991.55, acquisition 50,000.00);
claim expense 863.50; commission 275,526.68; `Σ CF(t)` = **−217,005.15**. Undiscounted,
the contract loses money; discounting is out of scope and is what makes the sign meaningful.
**Half the block reaches maturity** — 0.5042 of policies issued — which is the structural
difference from every protection product in this library.

`henreiritsu()` returns **92.0099%** = 5,000,000 / 5,434,200, reproducing the derived figure
in `product-spec.md` [S9].

### Second cell (`point_id = 2`) — 学資保険

契約者 male 契約年齢 30, 被保険者 (the child) 契約年齢 0, 22歳満期 (`n` = 22), 保険料払込期間 17 years, 基準保険金額
¥1,000,000, S型 grid at child 契約年齢 0–1, annual premium **¥108,564** (= 12 × ¥9,047 [S11]),
`waiver = true`. Staged benefits at `t` = 3 / 6 / 12 / 15 / 18 / 20 of 5% / 5% / 10% / 10% /
70% / 10% of `S`, then 満期保険金 100% at `t` = 22 [S10] [S11].

**Additional assumption values.** `i_cv` = 1.00% [S9]; `α` = 0.25, so `SC(0)` = ¥27,141
**[std]**; `wv_frac` = 1.00, `wv_load` = 1.00, `wv_lapse_mult` = 1.00, all **[std]**; child
mortality at attained age `t − 1` and 契約者 mortality at attained age `29 + t` for `t ≤ 17`,
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
row; the premium is carried on `pols_if_pay` alone and every benefit on `pols_if`.

| t | child age | 契約者 age | `pols_if` | `pols_if_pay` | `pols_wv` | premiums | claims_death | claims_staged | claims_lapse | expenses | claim_expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 30 | 1.000000 | 1.000000 | 0.000000 | 108,564.00 | 90.44 | 0.00 | 3,441.59 | 58,000.00 | 16.20 | 97,707.60 | −50,691.83 |
| 2 | 1 | 31 | 0.959222 | 0.958570 | 0.000652 | 104,066.21 | 120.57 | 0.00 | 5,766.83 | 7,750.52 | 10.74 | 3,121.99 | 87,295.56 |
| 3 | 2 | 32 | 0.929925 | 0.928651 | 0.001274 | 100,818.08 | 110.14 | 46,479.96 | 4,946.12 | 7,588.93 | 6.51 | 3,024.54 | 38,661.89 |
| … | | | | | | | | | | | | | |
| 17 | 16 | 46 | 0.699318 | 0.687606 | 0.011712 | 74,649.23 | 364.78 | 0.00 | 24,311.57 | 6,560.04 | 4.20 | 2,239.48 | 41,169.16 |
| 18 | 17 | — | 0.685126 | 0.672338 | 0.012788 | 0.00 | 457.38 | **479,405.94** | 14,475.47 | 6,491.18 | 5.21 | 0.00 | **−500,835.19** |
| 20 | 19 | — | 0.657442 | 0.645171 | 0.012271 | 0.00 | 368.92 | 65,710.05 | 12,867.48 | 6,354.10 | 6.84 | 0.00 | −85,307.38 |
| 22 | 21 | — | 0.630707 | 0.618935 | 0.011772 | 0.00 | 391.04 | 0.00 | 0.00 | 6,218.23 | 7.82 | 0.00 | −636,933.05 |

`claims_maturity` is 630,315.97 at `t = 22` and zero elsewhere; `claims_ph_death` is 0.00 in
every year, because `wv_frac` = 1.00.

**Trace, year 1.** Premium = 108,564.00 × 1.000000 = 108,564.00. Child decrement: `D(1) =
1.000000 × 0.00081 = 0.00081`; `DB(1) = max(108,564 − 0, Wb(1) = 111,653.970487) =
111,653.970487`, so death claims = 111,653.970487 × 0.00081 = 90.44 and claim expense =
20,000 × 0.00081 = 16.20. 契約者 decrement: `Dp(1) = 1.000000 × (1 − 0.00081) × 0.00068 =
0.000679449`, all of it into the waived state. Paying state after mortality = 1 × 0.99919 ×
0.99932 = 0.998510551; waived = 0.000679449; `R(1) = 0.999190000`. `g(1) = 0`, so no staged
benefit. `Sr(1) = 0.999190 × 0.04 = 0.039967600`; `CV(1) = 111,653.970487 − 25,544.4706 =
86,109.499898`, so surrender benefits = 86,109.499898 × 0.039967600 = 3,441.59. Expenses =
50,000.00 + 8,000.00 = 58,000.00, with the claim expense 16.20 beside them; commission =
0.90 × 108,564 = 97,707.60. `CF(1) = 108,564.00 − 90.44 − 16.20 − 3,441.59 − 58,000.00 −
97,707.60 = −50,691.83`. Update: `l_p(2) = 0.998510551 × 0.96 = 0.958570129`, `h(2) =
0.000679449 × 0.96 = 0.000652271`.

**Trace, year 3 — the first staged benefit.** Premium = 108,564 × 0.928651118 = 100,818.08.
`D(3) = (0.928651118 + 0.001273560) × 0.00035 = 0.000325474`; `DB(3) = max(3 × 108,564 − 0,
Wb(3) = 338,386.301776) = 338,386.30` — the value limb binds and the cumulative-premium limb
325,692.00 does not — so death claims = 338,386.301776 × 0.000325474 = 110.14 and claim
expense 6.51. `Dp(3) = 0.928651118 × (1 − 0.00035) × 0.00070 = 0.000649828`, into the waived
state; `R(3) = 0.927676262 + 0.001922943 = 0.929599205`. **Staged benefit:** `g(3) = 0.05`,
so `claims_staged = 1,000,000 × 0.05 × 0.929599205 = 46,479.96` — paid to the waived state
as well as to the paying one. `CV(3) = W(3) − SC(3) = 288,386.301776 − 22,351.4118 =
266,034.890011`; note that `W(3)` is the value **after** the ¥50,000 payment, so the
surrender value falls by exactly the benefit. `Sr(3) = 0.929599205 × 0.02 = 0.018591984`,
giving surrender benefits 4,946.12. Maintenance = 8,000 × 1.01² × 0.929924678 = 7,588.93;
renewal commission = 0.03 × 108,564 × 0.928651118 = 3,024.54. `CF(3) = 100,818.08 − 110.14 −
6.51 − 46,479.96 − 4,946.12 − 7,588.93 − 3,024.54 = 38,661.89`.

**Trace, year 18 — the 70% payment, and the year the 契約者 stops mattering.** No premium (`t >
m = 17`) and therefore no renewal commission. `q_p(18) = 0`, so the 契約者 decrement is gone
and `pols_wv` now runs off on child mortality and surrender alone: 0.012788161 at the start
of year 18 against 0.011712229 at the start of year 17, having stopped growing. `D(18) =
0.685125982 × 0.00038 = 0.000260348`; `DB(18) = max(1,845,588 − 300,000, Wb(18) =
1,756,811.077206) = 1,756,811.08`, so death claims = 457.38 and claim expense 5.21. `R(18) =
0.684865634`; `claims_staged = 1,000,000 × 0.70 × 0.684865634 = 479,405.94`. `CV(18) = W(18)
= 1,056,811.077206`, down from 1,738,755.93 at `t = 17` — the surrender value falls by the
¥700,000 paid, exactly as the sourced constraint requires [S7] — so surrender benefits =
1,056,811.077206 × 0.013697313 = 14,475.47. `CF(18) = −457.38 − 5.21 − 479,405.94 −
14,475.47 − 6,491.18 = −500,835.19`.

**Roll-forward check.** `Σ D(t) = 0.005018426`, `Σ (1 − wv_frac) × Dp(t) = 0`, `Σ Sr(t) =
0.364665608` and the maturing survivors `R(22) = 0.630315966`, summing to **1.000000000**.
Undiscounted totals per policy issued: premiums 1,521,101.61; death claims 4,120.71; staged
benefits 785,574.68; maturity 630,315.97; surrender benefits 299,647.45; `claims_ph_death`
0.00; expenses 203,460.43 (maintenance 153,460.43, acquisition 50,000.00); claim expense
100.37; commission 140,083.73; `Σ CF(t)` = **−542,201.73**.

**What the waiver is worth on this cell.** Ignoring lapse, the cumulative probability of
entering the waived state over the 17 premium-paying years is **1.861464%**, and the EPV of
the waived premiums at 1.00% is **¥11,384.94** against a premium EPV of ¥1,702,626.54 —
**0.6687% of the premium stream**, or about a tenth of one annual premium. The amount at
risk is `P × (m − t)`: **¥1,845,588 at issue**, which is 1.85 times the 満期保険金 the contract
will pay, running off to zero at `t = 17` while the maturity benefit is still five years
away. Small probability, large amount, running off on a different schedule from every other
cash flow in the model — which is exactly the shape of error that survives a sensibility
check on the base case. In the projected stream it shows up only as the 1.7% of year-17
premium income that is missing, and in nothing else at all.

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
  `reserve_pp(t) − V(t) = SC(t)` exactly testable. 危険準備金 is prescribed by sub-class and is
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

1. **The maturity benefit, and how many policies reach it.** 0.5042 of the anchor cell's
   policies mature, and the payment is ¥2,520,757.67 against a ¥3,931,162.67 premium stream
   — 64% of all income leaves in one year. Every lapse assumption is therefore a *maturity*
   assumption: the surrender-rate table moves the largest cash flow in the model through the
   survivorship factor, not through the surrender-benefit column.
2. **The cash-value construction.** `i_cv` is sourced [S9], but `α` is **[std]** and carries
   the whole ¥887,154.17 surrender-benefit stream on the anchor cell. Unlike the chassis,
   there is **no published surrender-value table for either cell to calibrate against** [S1]
   [S2] [S10], so the calibration is inherited rather than fitted, and the construction is
   more generous in the early durations than one carrier's qualitative description [S7]. A
   user with a real 算出方法書 replaces `pol_val_pp` and changes nothing else.
3. **The waiver decrement.** 1.86% cumulative probability against an amount at risk that
   starts at 1.85 times the maturity benefit. Omitting it understates the liability by 0.66%
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
   internal-rate diagnostics are printed beside it.
6. **The 予定利率 / 標準利率 gap.** The 予定利率 is sourced at 1.00% [S9]; the numeric 標準利率 could not be
   established [R4] [R5]. On a guaranteed 30-year maturity obligation the spread between
   them determines whether the statutory reserve behaves at all, and `reserve_pp ≥ V ≥ CV`
   is not an invariant under 逆ざや.
7. **Mortality margin, and its two signs.** `mort_be_factor = 1.00` puts the base run on a
   valuation table with a roughly-2σ margin [REG-R20]. On the anchor cell claims move
   proportionately; on the second cell the child decrement contributes ¥4,120.71 against
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

- **The maturity benefit is certain, not a decrement.** At `t = n` the survivors are paid
  `S` with probability 1 [R10] [S2] [S8]. Modelling maturity as a rate, or letting the
  projection run past `t = n` on a terminal age imported from the whole-life chassis, is
  wrong in both directions.
- **`lapse_rate(n)` must be zero.** A surrender at the end of the final policy year and the
  maturity payment fall on the same anniversary at the same amount; running both
  double-counts the terminal payment, and running the surrender instead of the maturity
  misclassifies 61% of the anchor cell's undiscounted outgo into the wrong column.
- **The policy value must converge on the maturity benefit.** `pol_val_pp(n) == sum_assured`
  exactly, on **both** cells. That identity is what makes an endowment a real test of a
  savings model, and it is the one thing a whole-life chassis can never check.
- **Two lives, two decrements, one policy.** The waiver runs on the 契約者's mortality at `y +
  t − 1`; every benefit runs on the 被保険者's at `x + t − 1` [S1] [S10]. Reading one table at
  one age for both is the most likely implementation error on the second cell — and on the
  anchor cell the two ages coincide, so it will not show there.
- **The 契約者 decrement stops at `m`.** Every waiver trigger is conditional on the event
  falling during 保険料払込期間 [S1] [S10]. Carrying `q_p` past `t = m` terminates policies the
  contract does not terminate, and does so in exactly the years when 86% of the second
  cell's receipts fall.
- **The waiver produces no benefit outgo.** It removes premium income and leaves every claim
  column unchanged [S1] [S10] [S13]. Booking a "waiver benefit" double-counts; and because
  omitting the waiver altogether changes no claim column either, neither error is visible in
  a benefit reconciliation.
- **Premiums on a waived policy are deemed paid.** The return-of-premiums death benefit
  keeps growing at `P × min(t, m)` on a policy that pays nothing, and the surrender value is
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
  1,738,755.93 to 1,056,811.08 across `t = 17 → 18` on the second cell, and one carrier
  computes the value from the elapsed months **and** the 学資金 timing [S1] [S7]. A model that
  pays the staged benefit beside the value rather than out of it inflates every later
  surrender.
- **The staged schedule is data.** It is read from a table keyed by `schedule_id`, and the
  `J` variant — one payment of 100%, then maturity — must run without touching the code
  [S10].
- **Both limbs of the 学資 death benefit must be evaluated.** On the composite's [std] basis
  the reserve limb dominates at every duration, so the `max` never switches; that is a
  property of this cell's negative loading, not of the contract [S3] [S13], and a point with
  a positive loading binds the other way. Hard-coding either limb passes on this cell and
  fails on the next.
- **`henreiritsu()` is a contractual ratio, not a model output ratio.** It reads `P × m` and
  the scheduled benefits, never the projected premium income or the probability-weighted
  claims; it is undefined for a policy that surrenders and unbounded for one that is waived;
  and computed from a 月払 premium on an annual grid it sits below the carrier's own published
  figure [S11] [S16].
- **There is no cliff on this product.** No retrieved document offers a 低解約返戻金型 form of
  either cell. Importing the chassis's `k` = 0.70 multiplier, its step at `m`, or its 15%
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
