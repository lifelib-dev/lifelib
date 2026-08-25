# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite of `product-spec.md` (same
directory) into a reference liability cash-flow projection on paper. They describe no
single insurer's contract. [S#] and [R#] resolve against `sources.md` in this directory,
numbering carried verbatim from `_research/term-life.md` and frozen; [REG-R#] resolves
against `references/regulatory-and-actuarial-references.md`, whose own R-numbering is
distinct and must never be read across. **[std]** marks a standardization introduced for
the reference implementation; [unverified] marks a claim not confirmed against a retrieved
document. **Every contractual parameter here is identical to `product-spec.md`'s.** What
is new is the assumption basis — a best-estimate mortality adjustment, a lapse table, a
renewal-decline rate, an expense and commission structure, and a premium scale beyond the
published ages. No retrieved document supplies any of them, so every one is **[std]** with
its rationale given where it is introduced.

This is the library's **protection chassis**. The
[survivor income term technical notes (収入保障保険)](../income_guarantee/technical-notes.md)
(survivor income term) state only their deltas against this file: the decrement recursion,
the premium chassis, the expense and commission structure and the processing order are
specified here once and are not restated there.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — premiums, death and
  severe disability (*kōdo shōgai*, 高度障害) claims, claim expenses, maintenance expenses
  and commission — for a single-policy model point of level term life (*teiki hoken*, 定期保険),
  in the sense the ESR current estimate (*genzai suikei*, 現在推計) requires:
  probability-weighted future cash flows on assumptions re-set at the 基準日 rather than
  locked in at issue [REG-R15]. The same projection is the shape of the item-1
  income-and-outgo analysis (*ichi-gō shūshi bunseki*, 1号収支分析) — premiums, claims,
  expenses and surrenders by segment over at least ten future years [REG-R22].
- **Discounting, MOCE, required capital and reserving are out of scope**, cited and not
  reproduced (see Valuation and reserve pointers). `jplib` computes no ratio and builds no
  policy reserve (*sekinin-junbikin*, 責任準備金).
- **Projection frequency.** Annual — the model is `Term_JP_A`. Nothing in the composite has
  intra-year contractual structure: the sum assured is level and the premium is level
  within each policy term (*hoken kikan*, 保険期間). The one intra-year mechanic that
  matters, the grace period (*yūyo kikan*, 猶予期間) of about one month [S1] [S8], sits
  inside a decrement the annual grid represents as a rate. The
  [survivor income term technical notes (収入保障保険)](../income_guarantee/technical-notes.md)
  run monthly because that benefit is a monthly income stream; this product does not
  need to.
- **Timing conventions [std].** Premiums at the start of each policy year (annualized, in
  advance); maintenance expense at the start of the year; acquisition expense and initial
  commission at issue; death and 高度障害 claims and their claim expense at the end of the
  policy year in which they arise; ordinary lapse at the end of the year, after deaths;
  the renewal (*kōshin*, 更新) decline at the end of a boundary year, after lapse.
- **Age basis [std].** Issue age (*keiyaku nenrei*, 契約年齢) is age last birthday
  (*man-nenrei*, 満年齢) with fractions discarded [S1]; attained age in year `t` is `x + t − 1`.
  生保標準生命表2018（死亡保険用）is built for an age nearest birthday (*hoken-nenrei*, 保険年齢) basis
  [REG-R20], so reading it at 満年齢 reads it half a year early and
  **understates** mortality. The base run accepts and states that bias; an optional shift
  `q_x → sqrt(q_x · q_{x+1})` raises the rate by about 0.7% at age 30 and 4.2% at age 40
  on the [std] table below. This resolves the mismatch `product-spec.md` footnote 3 flags.
- **Currency.** JPY throughout [S1]. No FX layer on this product.
- **Model points.** Single-policy, on an expected (probability-weighted) basis:
  survivorship multiplies per-policy cash flows. No aggregation logic is specified here.
  `point_id = 1` is the worked example's anchor cell.
- **Termination.** A to-a-stated-age (*sai manryō*, 歳満了) contract ends at the end of its
  term with nothing payable [S1] [S8] [S10] [S14]. A fixed-year (*nen manryō*, 年満了)
  更新型 contract ends only at the **renewal ceiling of attained age 80** [S1] [S2] [S8],
  because until then it renews. No 満期保険金, no surrender value (*kaiyaku-henreikin*, 解約返戻金),
  no tail state of any kind [S1] [S4] [S8] [S9] [S10] [S13] [S14].
- **Contract boundary — the paragraph this product forces.** A UK term assurance guarantees
  its premium for the whole term, so the boundary is the term. A Japanese 年満了 contract
  guarantees it only **within** the current 保険期間: at each 更新 the insurer recomputes it
  on attained age and the scale then in force [S1] [S4] [S8] [S12]. That is a unilateral
  repricing right exercisable every ten years — but a *scale-level* right, not an
  individual one, because renewal takes no 告知 and no fresh underwriting [S1] [S4] [S8]
  [S12], so the insurer cannot reprice a life for its own deterioration. The ESR
  standard-model coefficients that would settle where the boundary falls are [unverified]
  here — the 柱告示 were not retrieved [REG-R16] — so the model does not rule. It
  **projects to the ceiling in the base run [std]** and carries a `contract_boundary`
  switch truncating at the end of the current 保険期間. The two differ by more than a
  rounding: on the anchor cell undiscounted net cash flow is +¥50,400.25 to the ceiling
  against −¥15,878.74 over the first ten years. Reporting either without naming the
  convention says nothing.
- **Rounding.** Intermediates at full precision; displayed cash flows to two decimals of a
  yen, in-force to six decimals **[std]**. Premium rates round to the whole yen per month
  before annualization, as published rate cards do [S2] [S9] [S10].

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, 満年齢, 20–65 | 30 |
| `term_type` | enum {nen, sai} — 年満了 / 歳満了 | nen |
| `term_y` (`n`) | int years (年満了); implied by `expiry_age` (歳満了) | 10 |
| `expiry_age` | int (歳満了 only: 60/65/70/80) | — |
| `renew_ceiling` (`w_r`) | int, attained age at which renewal stops | 80 |
| `sum_assured` (`SA`) | JPY, ¥1,000,000–¥30,000,000 in ¥1,000,000 units | 10,000,000 |
| `premium_mode` | enum {monthly, semiannual, annual} | monthly |
| `living_needs` | bool (rider; base run false) | false |
| `wop` | bool (保険料の払込の免除; base run false) | false |
| `reinstatement` | bool (復活 module; base run false) | false |
| `contract_boundary` | enum {ceiling, current_term} | ceiling |

**The premium is not one of them.** `P_m` (`premium_mth_pp`) and the flat element `f`
(`policy_fee_m`, ¥248) are *derived* from the premium scale, keyed on sex, the entry age of
the term in force and that term's length — which is what makes the repricing at 更新 fall
out of the same lookup as the issue premium instead of needing a second column. Carrying
the premium on the model point would freeze it at the issue value and hide the repricing.

`P_m` is nonetheless a **published** figure at the anchor cell rather than a modeling
construction — the sharpest documentary contrast with `uklib`, where no premium basis is
observable and the anchor premium had to be invented. Three carriers price this exact cell
at ¥974, ¥980 and ¥1,068 [S2] [S9] [S5]; ¥974 is taken because that carrier publishes
enough grid to decompose it. **[std]** here covers only the choice of cell and the
annualization `P_a = 12 × P_m = 11,688`.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at the **start** of year t; `l(1) = 1` | annual recursion |
| `k(t)` | Term index: 1 in the original 保険期間, 2 after the first 更新, … | boundary years |
| `P_a(t)` | Annualized premium in force in year t; constant within a term | boundary years |
| `q(t)` | Best-estimate death-and-高度障害 rate (**one** decrement) | assumption lookup |
| `w(t)` | Ordinary lapse rate (end of year, after deaths) | assumption lookup |
| `d(t)` | Renewal-decline rate; non-zero **only** in a boundary year | boundary years |
| `D(t)` | Expected claims in year t = `l(t) × q(t)` | annual |
| `lap(t)` | Lapsed-but-reinstatable population (復活 module; 0 in base run) | annual |
| `CF(t)` | Net cash flow of year t, insurer perspective (+ = inflow) | annual |

Two of these a Japanese term model needs and a UK one does not: `k(t)`, because the premium
is a function of the term index rather than of `t`, and `d(t)`, because leaving at a
renewal boundary is a different event from lapsing mid-term. Two clocks — the three-year
suicide window and the two-year contestability window, both running from the 責任開始日 and
**neither restarting on 更新** [S1] [S4] [S7] [S8] — are contract state the base run tracks
but does not monetize; they bind only if the 復活 module is on, since 復活 is the one event
that restarts them [S1].

There is deliberately **no** `cv_pp` and no account value. The composite has no 解約返戻金
for the whole term [S1] [S4] [S6] [S8] [S9] [S10] [S13] [S14], and with no surrender value
there is no automatic premium loan (*jidō furikae kashitsuke*, 自動振替貸付) to carry the
policy through non-payment: one carrier states that absence in terms [S7]. A policy loan
(*keiyakusha kashitsuke*, 契約者貸付) has no collateral either, but that is an inference
from the missing surrender value and **not** a sourced fact — the carrier stating the APL
absence points its policyholders at its 契約貸付制度 instead [S7], and the one document that
appears to rule the policy loan out could not be text-extracted [S11] [unverified]. The
absence is a product fact: it is why this chassis carries a plain lapse model, and why the
APL mechanic is specified in the
[whole life technical notes (終身保険)](../whole_life/technical-notes.md) and not here.

---

## Assumption inputs

Three classes, kept separate. The first is cited and the insurer cannot change it; the
second is discretionary and, on this product, nearly empty; the third is the modeler's view
and is **[std]** throughout, because no Japanese public source supplies it.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Sum assured | `SA` level for the term, unchanged through 更新 | [S1] [S4] [S8] [S9] [S12] |
| Death benefit | `SA` on death in the 保険期間; terminates the contract | [S1] [S4] [S8] [S12] |
| 高度障害保険金 | **`SA`**, the same amount, on a 別表3 state; terminates the contract | [S1] [S4] [S8] [S9] [S12] |
| Ordering | Whichever becomes payable first is paid; the other then is not | [S1] [S8] |
| Premium | Level within the 保険期間; **not** guaranteed beyond it | [S1] [S4] [S8] [S12] |
| Premium structure | `P_m = f + r(sex, x, n) × SA / 5,000,000`, `f = 248` per month | [S2] |
| 更新 | Automatic unless declined 2 weeks before expiry; same term and `SA`; repriced on attained age; no 告知 | [S1] [S4] [S8] [S12] |
| Renewal ceiling | Attained age 80; a renewal passing it truncates to an 80歳満了 term | [S1] [S2] [S8] |
| 歳満了 | Never renews | [S1] |
| Clocks | Suicide 3 years, contestability 2 years, from 責任開始日; restart on 復活 only | [S1] [S4] [S7] [S8] [REG-R34] [REG-R35] |
| 猶予期間 | To the last day of the month after the 払込期月 (~1 month); then 失効 | [S1] [S8] |
| 復活 | 3 years, against arrears at 年6% compound [S1]; on evidence of health [S8] | [S1] [S8] |
| 解約返戻金 | **None**, whole term | [S1] [S4] [S6] [S8] [S9] [S10] [S13] [S14] |
| 自動振替貸付 | **Absent** — one carrier states it in terms | [S7] |
| 契約者貸付 | Not modeled. No 解約返戻金 exists to lend against, but the one document appearing to rule the policy loan out could not be extracted | inference; [S11] [unverified] |
| リビング・ニーズ特約 (a *tokuyaku*, rider) | `指定保険金額 − 6 months' interest − 6 months' premiums`; cap ¥30,000,000 per insured aggregated across contracts; barred within 1 year of a non-renewable expiry | [S1] [S7] [S8] [S12] |
| 保険料の払込の免除 | Accident on or after 責任開始時, 別表4 state within 180 days | [S1] [S8] [S12] [S14] |
| 満期保険金 | None | [S1] [S8] [S10] [S14] |

### (b) Insurer-discretionary current elements

On 無配当 protection business this class is **almost empty**, and the emptiness is why the
classes are separated at all: on the
[whole life technical notes (終身保険)](../whole_life/technical-notes.md) and the
[FX whole life technical notes (外貨建終身保険)](../fx_whole_life/technical-notes.md),
declared 契約者配当 and 積立利率 live here. Three residual items:

| Input | Snapshot value | Basis |
|---|---|---|
| 契約者配当 | **Nil** — 「この保険契約については、契約者配当はありません。」 | [S1] [S8] [S9] [S10] [S14]; one carrier writes a 有配当 design [S7] |
| Renewal rate scale | The scale in force at each future renewal is the insurer's. Modeled as the **current** scale extended by mortality | mechanic [S1] [S4] [S8] [S12]; scale **[std]** |
| 前納 discount, 高額割引 | Insurer-set and unpublished; not modeled | [S1] [S7] [S9] [S14]; scope **[std]** |

The renewal scale is the one genuinely discretionary lever with a large cash-flow effect,
and it is invisible. Treating the current scale as persistent is a **[std]** assumption,
not a neutral one.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Mortality — one decrement, and why.** 生保標準生命表2018（死亡保険用）**includes 高度障害
inside its death rate** [REG-R20]. Death and 高度障害 are therefore one decrement carrying
one sum assured, which is what the contract does: either benefit terminates the policy and
the other is then not paid [S1] [S8]. Projecting the table `qx` for death and adding a
高度障害 incidence on top double-counts the benefit.

The table is freely readable at a stable public URL [REG-R18] [R3] [R4] — the sharpest
contrast in this library with `uklib`, whose current CMI tables are subscriber-restricted —
but its publisher prohibits reproduction and transmission to third parties without written
consent [REG-R21]. The library therefore **cites** the table, **quotes** the rates the
worked example needs, and **ships** `mort_table.csv` as a **[std]** construction whose
`provenance` column points at the IAJ entries.

The shipped file is the **canonical `jplib` proxy**, one construction shared by every
product in this library rather than a per-product reconstruction, so that a cell carries
the same rate and the same provenance wherever it is shipped. Its anchors are the union of
the rates read from the table across the library's research passes, which is why more ages
are anchored here than this product's own pass read; the rows this product ships run from
attained age 20 to attained age 80, the range its model points can reach:

| Step | Rule | Basis |
|---|---|---|
| Anchors | Male 死亡保険用 `q20 = 0.00059`, `q22 = 0.00066`, `q25 = 0.00067`, `q30 = 0.00068`, `q31 = 0.00069`, `q32 = 0.00070`, `q33 = 0.00072`, `q34 = 0.00074`, `q35 = 0.00077`, `q40 = 0.00118`, `q45 = 0.00177`, `q50 = 0.00285`, `q55 = 0.00422`, `q60 = 0.00653`, `q65 = 0.01015`, `q70 = 0.01544`, `q75 = 0.02637`, `q80 = 0.05006`; female 死亡保険用 at the same ages except 31–34, `q30 = 0.00037`, `q60 = 0.00363` among them | read from the table [REG-R18], the subset this product's own pass read also [R4] |
| Interpolation | Log-linear in `ln q` between the two neighbouring anchors, rounded to 5 decimals — the published table's own granularity. No extrapolation: every non-anchor age lies strictly between two anchors | **[std]** |
| Best estimate | `q(t) = 0.80 × q_x^tab` | **[std]** (1) |
| Age read | At 満年齢, unshifted; optional `sqrt(q_x · q_{x+1})` shift | **[std]** |
| Improvement | None in the base run | **[std]** (2) |
| Suicide-exclusion offset | None: years 1–3 claims are not reduced for excluded suicides | clause [S1]; offset **[std]** (3) |

1. The 作成概要 states the margin in the publisher's words: a risk-theory adjustment sized
   to hold the exceedance probability near 2σ, **capped at 130% of the unadjusted rate**
   [REG-R20]. Removing a margin at its cap implies `1/1.3 = 0.769`. Against that, the table
   already carries a forward improvement allowance — 2.5% p.a. for five years then 1.0% for
   three [REG-R20] — and its base experience is 2008, 2009 and 2011. **0.80** is a round
   central choice between the two. No observed range can be given: no Japanese insurer
   publishes protection experience by duration and the research pass found no equivalent of
   the FCA's published data. This factor is the model's largest lever.
2. Eight years of population improvement since the table's effective date are not projected
   **[std]**. A production basis applying an improvement scale must re-derive footnote 1,
   because part of the 0.80 stands in for it.
3. Immaterial at these claim levels and unsupported by any incidence split in the sources.
   Note the direction: the suicide 免責 pays the 責任準備金 to the policyholder rather than
   nothing [S1], so even a modeled exclusion is not a clean claim saving.

**Lapse.** Japan's only published industry-wide persistency figure is the LIAJ's FY2024
解約・失効率 for 個人保険: **5.6%** of opening in-force sum assured, down 0.3 points
[REG-R31]. It is a whole-market number across all shapes and durations, not a duration
curve, so the reference table is **[std]** and is reconciled to it explicitly:

| Policy year | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| Annual lapse `w(t)` **[std]** | 9% | 7% | 6% | 5.5% | 5% |

The simple mean over the first ten years is 5.75% and the in-force-weighted mean 5.94%,
both a little above 5.6% — the expected direction, since the industry figure is dominated
by long-duration in-force sum assured while this is an early-duration protection curve. The
level is anchored; the **shape** is a convention with no Japanese published evidence behind
it. Lapse pays nothing: there is no 解約返戻金 [S1].

**Renewal decline.** At each 更新 boundary a proportion `d` of survivors leave rather than
accept the repriced contract. This decrement has **no `uklib` analogue** and it is large:
on the anchor cell the monthly premium moves from ¥974 to ¥1,823 at the first renewal, a
factor of **1.87** [S2]. Against that, renewal is the default — it happens unless notice is
given, and the notice period is **2 weeks** [S1] [S8], the shortest of the three observed
(2 weeks, 1 month, 2 months [S1] [S8] [S7] [S4]), which is the design that maximizes
renewal by inertia. No carrier publishes a take-up or decline rate, so `d = 15%` **[std]**
at every boundary. Two things roll into it that a production model should separate: the
policyholder who gives notice, and the policyholder whose **first renewed premium goes
unpaid through grace**, in which case the renewal is treated as never having happened and
the contract terminates at the original expiry [S1] [S7]. Both leave at the boundary; only
the first is a decision.

**Expenses and commission (all levels [std]; no Japanese public source exists).**

| Input | Value | Note |
|---|---|---|
| Acquisition expense `E0` | ¥15,000 per policy at issue | **[std]** |
| Initial commission `c0` | 50% of the first-year annualized premium, at issue | **[std]** |
| Renewal commission `c_r` | 5% of premiums from year 2 | **[std]** |
| Commission at 更新 | **None** in the base run | **[std]** (4) |
| Maintenance expense `e(t)` | ¥4,000 p.a., inflating 1.0% p.a. | **[std]** |
| Claim expense `ec` | ¥30,000 per death / 高度障害 claim | **[std]** |

4. A 更新 is not new business — no new 保険証券 is issued and no 告知 taken [S1] [S4] — so
   the base run pays no acquisition commission at a renewal. That is a choice, not a fact:
   no document in the set discloses a commission scale at all, and a scale paying
   first-year rates on each renewed term would change the sign of the cash flow in years
   11, 21, 31 and 41. The model exposes it as a switch and the pitfall list tests it.

The **¥248 monthly policy fee is a premium component, not an expense recovery** [S2]. It
enters the model only through `P_a`; crediting it against `e(t)` counts it twice.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning | cells |
|---|---|---|
| `t` | policy year, `t = 1..N`; `N = w_r − x` for 年満了, `n` for 歳満了 | — |
| `x` | 契約年齢 (満年齢); attained age in year t is `x + t − 1` | `age` |
| `k` | term index; `k = 1 + floor((t − 1) / n)` for 年満了 | `term_index` |
| `SA` | sum assured, JPY, level | `sum_assured` |
| `f` | flat monthly policy element, ¥248 | `policy_fee_m` |
| `r(sex, x, m)` | marginal monthly rate per ¥5,000,000 of cover, entry age x, term m | `prem_rate_m` |
| `P_m(k)`, `P_a(k)` | monthly and annualized premium in term k; `P_a = 12 × P_m` | `premium_mth_pp`, `prem_pp` |
| `q(t)` | best-estimate death-and-高度障害 rate | `mort_rate` |
| `w(t)` | ordinary lapse rate | `lapse_rate` |
| `d(t)` | renewal-decline rate; 0 unless t is a boundary year | `decline_rate` |
| `l(t)` | in-force probability at the start of year t; `l(1) = 1` | `pols_if` |
| `D(t)` | expected claims in year t = `l(t) × q(t)` | `pols_death` |
| `E0`, `e(t)` | acquisition expense; maintenance `4,000 × 1.01^(t−1)` per policy | `expense_acq`, `expenses` |
| `c0`, `c_r` | initial commission `0.50 × P_a(1)`; renewal rate 0.05 | `commissions` |
| `ec` | claim expense per claim, ¥30,000 | `expense_claim` |
| `CF(t)` | net cash flow of year t (+ inflow) | `net_cf` |

Dimensional check: `q`, `w`, `d`, `l`, `D` are dimensionless probabilities; `SA`, `E0`,
`e`, `ec`, `P_a` are JPY per policy per year; `f` and `P_m` are JPY **per month**, so every
expression using them carries an explicit `× 12`; `r` is JPY per month per ¥5,000,000 of
cover, so `r × SA / 5,000,000` is JPY per month. Every term of `CF(t)` is JPY per year per
policy issued.

### Premium chassis

The published rate structure decomposes exactly [S2]:

    P_m(k) = f + r(sex, x_k, m_k) * SA / 5,000,000
    x_k    = x + (k - 1) * n              (attained age at the k-th term's start)
    m_k    = min(n, w_r - x_k)            (truncation at the ceiling)
    P_a(k) = 12 * P_m(k)

At the anchor cell `r(M, 30, 10) = 363` and `P_m(1) = 248 + 2 × 363 = 974` [S2],
reproducing the published figure to the yen; at the first renewal `r(M, 40, 10) = 787.5`
and `P_m(2) = 1,823` [S2]; at the second, `r(M, 50, 10) = 1,842.5` and `P_m(3) = 3,933`
[S2]. **Ages 60 and 70 are published by no carrier**, and the anchor cell reaches both. The
[std] extension:

    r(sex, x, m) = r(sex, 50, 10) * qbar(x, m) / qbar(50, 10)
    qbar(x, m)   = mean of q_a^tab over a = x .. x+m-1   (table rates, not best estimate)

anchored on the published age-50 cell and rounded to the whole yen per month. It back-casts
to ¥958.9 at age 30 against the published ¥974 (−1.5%) and to ¥1,806.4 at age 40 against
¥1,823 (−0.9%) — close enough to use, and stated so the size of the approximation is
visible rather than trusted. It gives `P_m = ¥8,976` at age 60 and `¥23,881` at age 70 on
¥10,000,000 of cover.

### Decrement recursion and processing order

For `t = 1..N`, in this order **[std]**:

1. **Start of year.** Premium income `P_a(k(t)) × l(t)`; maintenance `e(t) × l(t)`; renewal
   commission `c_r × P_a(k(t)) × l(t)` for `t ≥ 2`. At `t = 1` additionally `E0` and `c0`
   per policy issued (`l(1) = 1`).
2. **Decrement lookup.** `q(t)` at attained age `x + t − 1`; `w(t)` from the lapse table;
   `d(t) = d` if `t mod n = 0` and `t < N`, else 0.
3. **End of year — claims.** `D(t) = l(t) × q(t)`; claim outgo `SA × D(t)`; claim expense
   `ec × D(t)`. One decrement, one benefit: death and 高度障害 are not added.
4. **End of year — ordinary lapse.** `l(t) × (1 − q(t)) × w(t)` leave, applied to survivors
   of mortality. **Nothing is paid** — there is no 解約返戻金 [S1].
5. **End of a boundary year — renewal decline.**
   `l(t) × (1 − q(t)) × (1 − w(t)) × d(t)` leave, applied after lapse. Nothing is paid.
6. **Roll forward**, plus any 復活 reinstatements (zero in the base run).

       l(t+1) = l(t) * (1 - q(t)) * (1 - w(t)) * (1 - d(t)) + lap(t) * rho

7. **Repricing at a boundary.** `k(t+1) = k(t) + 1` and `P_a` is recomputed at attained age
   `x + t` over the term `m = min(n, w_r − (x + t))`. The projection horizon does **not**
   change; the term shortens instead.

At `t = N` the projection ends: no maturity payment, no run-off, no tail states [S1] [S8]
[S10] [S14]. The identity the model must satisfy at every `t` is

    l(t) - l(t+1) = D(t) + lapses(t) + declines(t) - reinstatements(t)

which `check_pols_roll_fwd()` asserts over all `t` and returns as a single `bool`. The
reinstatement term is zero in the base run and is carried in the identity anyway, so the
same residual closes in **both** positions of the 復活 switch rather than one form of the
check being right for each.

### Net cash flow

    CF(t) = P_a(k(t)) * l(t)                          (premiums)
          - SA * D(t)                                 (death and 高度障害 claims)
          - ec * D(t)                                 (claim expense)
          - e(t) * l(t)                               (maintenance)
          - c_r * P_a(k(t)) * l(t) * 1{t >= 2}        (renewal commission)
          - (E0 + c0) * 1{t = 1}                      (acquisition)

`net_cf` is income-positive, per the library convention. Lapse and decline contribute no
term: they act only through `l(t)`. A `claims_lapse` column exists and is identically zero
— the zero is the product fact worth publishing, as it is in `Term_UK_A`.

Known bias of the annual-in-advance convention **[std]**: a full year's premium is
collected at the start of each year with no allowance for premiums ceasing at mid-year
exits, so premium income is slightly overstated; the offsetting understatement is the
end-of-year claim timing. Do **not** apply both this convention and a separate half-year
premium adjustment.

### Optional modules (all off in the base run)

- **リビング・ニーズ特約.** Acceleration incidence `a(t)` **[std]** (no retrieved document
  gives incidence). On an accelerated amount `A ≤ min(SA, 30,000,000)`:

      payout = A - A * i_ln * 0.5 - 6 months' premiums on A

  with `i_ln` a **[std]** snapshot rate. A full acceleration extinguishes the contract
  retroactively to the claim date; a partial one reduces `SA` from that date and the
  reduced premium continues [S1] [S7] — two transitions, not one benefit with two amounts.
  Barred within one year of a non-renewable expiry [S1] [S7] [S8]; on a 更新型 cell that bar
  bites only in the ceiling term.
- **保険料の払込の免除.** A waiver state on the accident-plus-180-days-plus-別表4 test [S1]
  [S8] [S12] [S14] with **[std]** incidence. 別表4 is a materially lower bar than 別表3 —
  loss of one eye, deafness in both ears, loss of one limb at wrist or ankle [S1] — so the
  waiver incidence is **not** the 高度障害 incidence and must not reuse `q(t)`. While the
  waiver runs, premium income stops, cover continues and alteration rights switch off [S1].
- **復活.** A lapsed-but-reinstatable population with a three-year window `W = 3` [S1].
  The window runs from **each life's own 失効**, so the pool is carried by vintage and not
  as one balance with an indicator on it — a single indicator drops a whole cohort a year
  early or late:

      lap(t)              = sum over s in [t - W, t - 1] of lapses(s) * (1 - rho)^(t - 1 - s)
      lapses(s)           = l(s) * (1 - q(s)) * w(s)
      reinstatements into l(t+1) = lap(t) * rho
      window expiries(t)  = lapses(t - W) * (1 - rho)^W

  with `rho` **[std]**. One inflow and two outflows, and the ledger
  `lap(t) − lap(t+1) = reinstatements(t) + expiries(t) − lapses(t)` is what
  `check_lapse_pool()` asserts — it closes with the module off as well as on, because the
  pool is tracked either way. Renewal declines never enter it: a declined renewal is an
  expiry, not a 失効, and there is nothing to reinstate. Off in the base run: any value of
  `rho` is an invention with a material persistency effect and no carrier publishes one.
  Reinstatement restarts both clocks from the new 責任開始 [S1] — the only event that does.
- **Contract boundary.** `contract_boundary = current_term` truncates at the end of the
  term in force at the valuation date.

### What the [survivor income term technical notes (収入保障保険)](../income_guarantee/technical-notes.md) inherits

Unchanged from this file: the decrement recursion and processing order (steps 1–7), the
premium chassis `P_m = f + r × SA / 5,000,000` with its renewal repricing, the [std]
mortality construction and its 0.80 factor, the lapse table, the renewal-decline treatment,
the expense and commission structure, the age basis and the timing conventions. What
changes there: a monthly grid, and a benefit replaced by an annuity-certain income stream
with 最低支払保証期間 as its floor — so the in-payment ledger is **not** decremented, while
premium income still carries `l(t)`.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions. Japanese public evidence on
behaviour is thinner than the UK's: one published lapse rate for the whole market
[REG-R31], and nothing on duration, channel or renewal take-up.

- **Base lapse [std].** The duration table above, reconciled to 5.6% as shown. Channel is
  not represented; career agents sold 56.7% of the most recently bought policies [R9] — a
  share of purchases, not of cover — and agent-sold and direct-sold persistency are not the
  same, but no split is published.
- **Renewal decline [std].** `d = 15%`, flat. The refinement the flat rate defers: decline
  should rise with the premium jump, which itself accelerates — the anchor cell's premium
  multiplies by 1.87, then 2.16, then 2.28, then 2.66 across four renewals. A reference
  elasticity form is

      d(t) = min(d_max, d_0 * (P_a(k+1) / P_a(k))^beta)

  with `d_0 = 15%`, base run `beta = 0` giving the flat rate, and `d_max = 50%`, all
  three **[std]**. The cap is a guard on the elasticity form rather than a behavioural
  view: at `beta = 1` the largest jump on the anchor cell (×2.66) reaches only 40%, so
  the cap binds at no boundary, while at `beta = 2` even the smallest (×1.87) reaches 53%
  and it binds at all four. Half the survivors is the round level at which one boundary
  removes 0.27 of the original cohort — more than three times the 0.08 the base 15%
  removes, and over half the 0.45 that the ten preceding years of ordinary lapse remove.
  No document narrows any of the three.
- **Selective lapsation [std] (optional).** Lapsers and decliners are healthier on average,
  and the effect is stronger here than on a UK term policy because the 更新 decision recurs
  at ages where the premium is large and health is known:

      q_eff(t) = q(t) * [1 + lambda * max(0, 1 - l(t) / l_ref)]

  with `lambda` **[std]**, base run `lambda = 0`, and `l_ref = 1` **[std]** — the reference
  is the cohort at issue, so the loading is driven by the proportion of the original block
  that has left, which is the quantity anti-selection is a function of. The mechanism is
  one-directional: renewal takes **no 告知** [S1] [S4] [S8] [S12], so a life that has become
  uninsurable elsewhere renews while a healthy life re-shops.
- **Rebroking.** The Japanese analogue of the UK rebroking driver is the 更新 decision
  itself rather than a mid-term switch, so it is modeled through `d(t)` and not as a
  separate lapse multiplier **[std scope]**.
- **減額.** Permitted above an insurer-set floor, premium reset, **no** 払戻金 arising [S1]
  [S8]. Not modeled: it changes `SA` and `P_a` together, which is a model-point
  re-parameterization rather than a decrement **[std scope]**.
- **クーリング・オフ.** Out of scope: the model begins with cover in force and the
  eight-day statutory population [REG-R36] already out [S1].

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 契約年齢 30 (満年齢), 年満了 10年 更新型, renewal
ceiling attained age 80, 保険金額 ¥10,000,000, 月払保険料 **¥974** [S2], `P_a = ¥11,688`
**[std annualization]**. Horizon `N = 80 − 30 = 50` years; boundary years `t = 10, 20, 30,
40`. Base run: no rider, no waiver, no 復活, no selective lapsation, boundary = ceiling.

**Every assumption value the cell uses.** The table rates below come from the canonical
`jplib` proxy of 生保標準生命表2018（死亡保険用）男. Attained ages 30–35 and 40 are sourced
anchors, **read from the published table** [REG-R18] [R4]; ages 36–39 are the **[std]**
log-linear interpolation between the age-35 and age-40 anchors, rounded to 5 decimals. The
best-estimate rate is `q(t) = 0.80 × q_x^tab` **[std]**:

| attained age | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `q_x^tab` | 0.00068 | 0.00069 | 0.00070 | 0.00072 | 0.00074 | 0.00077 | 0.00084 | 0.00091 | 0.00099 | 0.00108 | 0.00118 |
| `q(t)` | 0.000544 | 0.000552 | 0.000560 | 0.000576 | 0.000592 | 0.000616 | 0.000672 | 0.000728 | 0.000792 | 0.000864 | 0.000944 |
| anchor? | yes | yes | yes | yes | yes | yes | no | no | no | no | yes |

Lapse `w(t)` = 9% / 7% / 6% / 5.5% / 5% from year 5 **[std]**; renewal decline `d` = 15% at
boundary years **[std]**; `E0` = ¥15,000, `c0` = 0.50 × 11,688 = ¥5,844, `c_r` = 5% from
year 2, `e(t)` = 4,000 × 1.01^(t−1), `ec` = ¥30,000, all **[std]**.

| t | age | `l(t)` | `P_a` | Premiums | Claims | Claim exp | Maint. + acq. | Commission | `CF(t)` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 30 | 1.000000 | 11,688 | 11,688.00 | 5,440.00 | 16.32 | 19,000.00 | 5,844.00 | −18,612.32 |
| 2 | 31 | 0.909505 | 11,688 | 10,630.29 | 5,020.47 | 15.06 | 3,674.40 | 531.51 | +1,388.85 |
| 3 | 32 | 0.845373 | 11,688 | 9,880.72 | 4,734.09 | 14.20 | 3,449.46 | 494.04 | +1,188.93 |
| 10 | 39 | 0.578436 | 11,688 | 6,760.76 | 4,997.69 | 14.99 | 2,530.51 | 338.04 | −1,120.47 |
| 11 | 40 | 0.466683 | 21,876 | 10,209.17 | 4,405.49 | 13.22 | 2,062.04 | 510.46 | +3,217.97 |

**Trace, year 1.** `l(1) = 1`; premiums `= 11,688 × 1 = 11,688.00`.
`q(1) = 0.80 × 0.00068 = 0.000544`, so `D(1) = 0.000544`. Claims
`= 10,000,000 × 0.000544 = 5,440.00`; claim expense `= 30,000 × 0.000544 = 16.32`. Expenses
`= E0 + e(1) = 15,000.00 + 4,000.00 = 19,000.00`; commission `= c0 = 0.50 × 11,688 =
5,844.00`. `CF(1) = 11,688.00 − 5,440.00 − 16.32 − 19,000.00 − 5,844.00 = −18,612.32`.
Roll forward: `l(2) = 1 × (1 − 0.000544) × (1 − 0.09) = 0.999456 × 0.91 = 0.909505`.

**Trace, year 2.** Premiums `= 11,688 × 0.90950496 = 10,630.29`.
`q(2) = 0.80 × 0.00069 = 0.000552`; `D(2) = 0.90950496 × 0.000552 = 0.00050205`; claims
`= 5,020.47`; claim expense `= 15.06`. Maintenance `= 4,000 × 1.01 × 0.90950496 =
4,040 × 0.90950496 = 3,674.40`. Renewal commission `= 0.05 × 10,630.29 = 531.51`.
`CF(2) = 10,630.29 − 5,020.47 − 15.06 − 3,674.40 − 531.51 = +1,388.85`. Roll forward:
`l(3) = 0.90950496 × (1 − 0.000552) × (1 − 0.07) = 0.845373`.

**Trace, year 3.** Premiums `= 11,688 × 0.84537271 = 9,880.72`.
`q(3) = 0.80 × 0.00070 = 0.000560`; `D(3) = 0.84537271 × 0.000560 = 0.00047341`; claims
`= 4,734.09`; claim expense `= 14.20`. Maintenance
`= 4,000 × 1.01^2 × 0.84537271 = 4,080.40 × 0.84537271 = 3,449.46`. Renewal commission
`= 0.05 × 9,880.72 = 494.04`.
`CF(3) = 9,880.72 − 4,734.09 − 14.20 − 3,449.46 − 494.04 = +1,188.93`.

**Trace, year 10 — the boundary year.** `l(10) = 0.57843599`; premiums
`= 11,688 × 0.57843599 = 6,760.76` on the **old** premium, because the repricing takes
effect at the start of year 11 and not before. `q(10) = 0.80 × 0.00108 = 0.000864`;
`D(10) = 0.00049977`; claims `= 4,997.69`; claim expense `= 14.99`. Maintenance
`= 4,000 × 1.01^9 × 0.57843599 = 2,530.51`; renewal commission `= 338.04`.
`CF(10) = 6,760.76 − 4,997.69 − 14.99 − 2,530.51 − 338.04 = −1,120.47`. Roll forward, in
the processing order and no other: after mortality
`0.57843599 × (1 − 0.000864) = 0.57793622`; after ordinary lapse
`× (1 − 0.05) = 0.54903941`; after the renewal decline `× (1 − 0.15) = 0.46668350`. So
`l(11) = 0.466683`, and the three exits in year 10 are 0.00049977 deaths, 0.02889681
lapses and **0.08235591 renewal declines** — the decline is 74% of all exits that year, and
a model folding it into the lapse rate cannot see it.

**Trace, year 11 — the repriced term.** Attained age at renewal is `30 + 10 = 40`, so
`P_m(2) = 248 + 2 × 787.5 = 1,823` [S2] and `P_a(2) = 21,876`. Premiums
`= 21,876 × 0.46668350 = 10,209.17` — **higher than year 10's despite 19% fewer policies**,
because the premium multiplied by 1.87. `q(11) = 0.80 × 0.00118 = 0.000944`;
`D(11) = 0.00044055`; claims `= 4,405.49`; claim expense `= 13.22`. Maintenance
`= 4,000 × 1.01^10 × 0.46668350 = 2,062.04`; renewal commission
`= 0.05 × 10,209.17 = 510.46`.
`CF(11) = 10,209.17 − 4,405.49 − 13.22 − 2,062.04 − 510.46 = +3,217.97`.

**The renewal ladder**, five numbers per renewal:

| Renewal | at t | attained age | `P_m` | `P_a` | jump | `l(t+1)` |
|---|---|---|---|---|---|---|
| — (issue) | — | 30 | 974 [S2] | 11,688 | — | 1.000000 |
| 1st | 10 | 40 | 1,823 [S2] | 21,876 | ×1.87 | 0.466683 |
| 2nd | 20 | 50 | 3,933 [S2] | 47,196 | ×2.16 | 0.234147 |
| 3rd | 30 | 60 | 8,976 **[std]** | 107,712 | ×2.28 | 0.115211 |
| 4th | 40 | 70 | 23,881 **[std]** | 286,572 | ×2.66 | 0.054121 |

Cover ends at attained age 80 with `l(51) = 0.026042` — 2.6% of the cohort still in force
after fifty years and four repricings, paying ¥286,572 a year for ¥10,000,000 of cover.
That row is the economically important one and is not a modeling artefact: a renewable term
at attained-age rates converges on term-cost pricing, and the reason carriers cap renewal
at 80 is that beyond it the product stops being purchasable.

**Totals over the fifty years, undiscounted:** premiums ¥470,348.54, claims ¥309,768.95,
net cash flow **+¥50,400.25**. Over the first ten years alone — the
`contract_boundary = current_term` answer — net cash flow is **−¥15,878.74**. The shape is
the protection shape: a deep first-year strain (¥20,844 of acquisition cost against ¥11,688
of premium), thin positive margins through the middle of each term, a negative year
immediately before each renewal as the level premium falls behind the rising mortality
cost, and a jump back into surplus the year after.

---

## Valuation and reserve pointers

This library projects gross cash flows. Every valuation layer consumes them and is cited,
never reproduced:

- Standard policy reserve (*hyōjun sekinin-junbikin*, **標準責任準備金**). 保険業法第116条第2項
  delegates the accumulation method and coefficient levels for the contracts the ordinance
  specifies [REG-R4]; 施行規則第68条 fixes the set [REG-R7] and 第69条第1項 the taxonomy
  保険料積立金 / 未経過保険料 / 払戻積立金 / 危険準備金 [REG-R8]. 平成8年大蔵省告示第48号 supplies
  the method — net level premium method (*heijun jun-hokenryō-shiki*, **平準純保険料式**),
  no Zillmer adjustment — and the table vintage: contracts from 2018-04-01 value on
  生保標準生命表2018（死亡保険用）[REG-R10] [REG-R11]. The standard valuation interest rate
  (*hyōjun riritsu*, 標準利率) resets annually for regular-premium yen business off
  three- and ten-year means of 10-year JGB yields with safety coefficients by band, on a
  0.5% trigger and 0.25% rounding, effective the following 1 April [REG-R10]; its **current
  numeric value could not be established from any retrieved document and is [unverified]**.
- Contingency reserve (*kiken junbikin*, **危険準備金**) is one of the four 第69条第1項
  components [REG-R8]. 価格変動準備金 is asset-driven and outside a liability projection.
- **The valuation table is not this model's basis.** 標準生命表2018 carries an explicit ~2σ
  margin capped at 130% of the unadjusted rate plus a forward improvement allowance
  [REG-R20], while `q(t)` here is a **[std]** adjustment of it. The same projection cannot
  serve the statutory reserve and the current estimate without swapping the basis; say
  which is in use at every point.
- **ESR.** From 2026-03-31 insurers report on the 経済価値ベースのソルベンシー規制: assets at
  fair value, liabilities as 現在推計 + MOCE, required capital at 99.5% over one year, early
  corrective action below **ESR 100%** [REG-R15]. That regime change is why an
  assumption-parameterized, re-runnable projection is the operative artefact — the old
  ソルベンシー・マージン比率 basis locked mortality, lapse and interest at issue [REG-R15].
  The old 200% trigger and the new 100% trigger are not comparable quantities [REG-R17]
  [REG-R15]. `jplib` computes neither ratio.
- **The professional use of this projection.** 保険業法第121条第1項第1号 requires the
  保険計理人's 意見書 [REG-R6]; the IAJ practice standard turns it into the 1号収支分析 — a
  forward projection of premiums, claims, expenses and surrenders by 区分経理 segment over
  **at least ten future years**, open and closed, sufficiency tested over the first five
  [REG-R22]. The recursion above is that projection, per policy.
- **Accounting.** IFRS 17 is **voluntary** in Japan — IFRS applies as 指定国際会計基準 to
  insurers that elect it [REG-R47]. One projection feeds three separate measurement bases
  (J-GAAP [REG-R10], ESR [REG-R15], IFRS where adopted); conflating them gets wrong which
  assumptions are locked in.
- **On insurer failure**, 生命保険契約者保護機構 covers up to **90% of the 責任準備金** under a
  rate delegated by 保険業法第270条の3 [REG-R40] [REG-R41]. Cited, never modeled.

---

## Key sensitivities and model risks

In rough order of leverage:

1. **The best-estimate mortality factor.** `0.80` **[std]** is the largest single lever and
   the least evidenced. Its justification is arithmetic on the published margin — a 130% cap
   implies `1/1.3 = 0.769` — offset by improvement already inside the table [REG-R20]. A
   user with own experience should replace it before anything else in this file.
2. **The renewal-decline rate.** `d = 15%` **[std]** is the largest structural lever and has
   no `uklib` analogue. Undiscounted net cash flow over the fifty years runs **+¥92,123.94
   at d = 0%, +¥50,400.25 at 15%, +¥22,587.91 at 30%** — a factor of four across a range no
   document narrows.
3. **The renewal rate scale beyond age 50.** Nothing is published above the age-50 cell
   [S2], and the anchor cell spends its last twenty years there. The [std] extension
   back-casts to within 1.5% at age 30 and 0.9% at age 40, which is reassuring about the
   *form* and says nothing about the *level* an insurer will charge in 2056.
4. **Contract boundary.** Whether the liability runs to the ceiling or to the end of the
   current 保険期間 changes the sign of the undiscounted answer on this cell. The model does
   not rule; the ESR coefficient 告示 that would settle it were not retrieved [REG-R16].
5. **Selective lapsation across renewals.** Renewal takes no 告知 [S1] [S4] [S8] [S12], so
   the anti-selection is structural and repeats four times on this cell. Base run
   `lambda = 0` understates late-duration claims by construction.
6. **Early-duration lapse against front-loaded acquisition cost.** ¥20,844 of year-1 outgo
   against ¥11,688 of year-1 premium makes the first three lapse rates decide how long the
   strain takes to recover. No Japanese clawback evidence exists in the sources.
7. **Expense inflation on small premiums, and the age basis.** ¥4,000 p.a. of maintenance
   against ¥11,688 of premium is a third of the first-term load, so the 1.0% **[std]**
   inflation rate is a poor one to leave unexamined; and the 満年齢 / 保険年齢 mismatch [S1]
   [REG-R20] understates `q` by about 0.7% at age 30 rising to 4.2% at age 40 — small
   beside item 1, but systematic and in one direction.

Known modeling pitfalls:

- **高度障害 is not a second decrement.** 生保標準生命表2018（死亡保険用）includes 高度障害 in
  its death rate [REG-R20], and the contract pays one benefit and terminates on either
  event [S1] [S8]. Adding a 高度障害 incidence on top of the table double-counts claims.
- **更新 reprices; it does not re-issue.** `l(t)` is continuous across the boundary — no
  reset to 1, no acquisition expense in the base run, no new 保険証券 [S1] [S4]. The suicide
  and contestability clocks run from the original 責任開始日 and **do not** restart on 更新
  [S1] [S4] [S7] [S8]; only 復活 restarts them [S1]. Treating each renewed term as a fresh
  policy gets persistency, strain pattern and both clocks wrong at once.
- **Truncation at the ceiling shortens the term, not the horizon.** A renewal that would
  carry the policy past attained age 80 renews as an 80歳満了 term [S1] [S2] [S8], so an
  issue age of 35 has a final term of 5 years and the projection still ends exactly at 80.
  Three other market rules exist — shorten to expiry age 90, shorten *or lengthen* to a
  指定年齢, auto-convert to another product [S4] [S7] [S12] — and importing one changes the
  horizon.
- **歳満了 never renews.** Such a model point has one term, one premium and no repricing
  [S1]; applying the renewal machinery to it invents cover the contract does not have.
- **Lapse pays nothing.** There is no 解約返戻金 for the whole term [S1] [S4] [S6] [S8] [S9]
  [S10] [S13] [S14], so `claims_lapse` is identically zero and lapse acts only through
  `l(t)`. One of the eight carriers whose position is documented *does* have a surrender
  value [S12] — a Japan term chassis
  cannot assume the absence the way a UK one can, so the zero is asserted from the
  composite's sources, not from the product class.
- **There is no 自動振替貸付 on this chassis.** With no 解約返戻金 there is no collateral, and
  one carrier states the absence in terms [S7]. Importing the APL mechanic from the
  [whole life technical notes (終身保険)](../whole_life/technical-notes.md)
  creates a no-lapse cushion the contract does not have; the supervisory guideline in any
  case requires an APL, where one exists, to run **at the policyholder's election** rather
  than automatically [REG-R14]. Grace → 失効 → 復活-or-not is the whole persistency
  machinery here.
- **The ¥248 policy fee is premium, not expense.** It sits inside `P_m` [S2] and enters the
  model only through `P_a`; crediting it against maintenance expense counts it twice, and
  `P_a` must reconstruct as `12 × (248 + 2 × 363) = 11,688` on the anchor cell.
- **Renewal decline is not lapse.** It applies only in boundary years, only after mortality
  and ordinary lapse, and it dominates them: in year 10 of the anchor cell it is 0.08235591
  of 0.11175249 total exits. Folding it into `w(t)` makes the boundary invisible and
  mis-times most of the cohort's departure.
- **A failed first renewal premium is an expiry, not a lapse.** Where the first premium of
  the renewed contract goes unpaid through grace, the renewal is treated as never having
  happened and the contract terminates at the **original** expiry rather than being 解除
  [S1] [S7]. Those lives must not appear in force in year `t + 1` collecting the renewed
  premium, and must not be counted as a mid-term lapse of a term that never began.
- **The living-needs cap is per insured, aggregated across contracts** — not per contract
  [S1] [S7] [S8] [S12]. Inside the composite's ¥1,000,000–¥30,000,000 envelope it is
  therefore *exactly reached* at the ceiling and never reduces a single-contract payment. A
  model reporting the cap biting at `SA = 30,000,000` has a strict-versus-weak inequality
  error; a model applying it per contract has misread the clause.
- **Read the table at the right age.** 契約年齢 is 満年齢 [S1] and 標準生命表2018 is built for
  保険年齢 [REG-R20]. The base run reads at 満年齢 and understates, so the shift module must
  move `q` up, not down.
- **Naming the boundary is part of reporting the number.** The same cell gives +¥50,400.25
  to the ceiling and −¥15,878.74 over the current term. Neither is an ESR current estimate
  on its own, because the ESR standard-model treatment of a no-underwriting auto-renewal is
  [unverified] here [REG-R16].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #jplib-term_life-r3
[R4]: #jplib-term_life-r4
[R9]: #jplib-term_life-r9
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R16]: #jplib-reg-r16
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R31]: #jplib-reg-r31
[REG-R34]: #jplib-reg-r34
[REG-R35]: #jplib-reg-r35
[REG-R36]: #jplib-reg-r36
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R47]: #jplib-reg-r47
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
