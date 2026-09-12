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
- **Projection frequency.** **Monthly** — the model is `Term_JP_S`. The whole library runs
  on one grid, and this product converted to it. The contract is still quoted in years —
  the sum assured is level, the premium is level within each policy term (*hoken kikan*,
  保険期間), and the lapse and mortality bases are annual — so the monthly step is finer
  than the guarantees rather than finer than the product. What it buys is three things the
  annual step could not do. The **payment mode** becomes a cash flow rather than a column:
  月払, 半年払 and 年払 now differ, which matters because Japanese rate cards are quoted
  monthly [S2]. The **更新 boundary** is one month rather than one year, so the renewal
  decline stands alone instead of being averaged against twelve months of ordinary lapse.
  And the grace period (*yūyo kikan*, 猶予期間) of about one month [S1] [S8] is for the first
  time shorter than a step rather than longer — so the unpaid-premium exit at a renewal is
  representable, even though the composite still folds it into one decline rate for want of
  a take-up assumption. The
  [survivor income term technical notes (収入保障保険)](../income_guarantee/technical-notes.md)
  were monthly from the start because that benefit is a monthly income stream.
- **Time index.** `t` is **0-based** and its unit is the **policy month**: `t = 0` is the
  first projected month, the frame runs `t = 0, 1, …, T − 1`, and `T = proj_len()` is the
  **number** of projected months, not the last index. Period `t` runs from time `t` to time
  `t + 1`. The **contractual policy year is the 1-based label `y(t) = 1 + ⌊t/12⌋`** and
  `duration(t) = ⌊t/12⌋` is the count of completed policy years; a schedule quoted "by
  policy year" — the lapse table below — is read at `y(t)`. Attained age is `x + ⌊t/12⌋`,
  so it steps on the anniversary and not on the month.
- **Timing conventions [std].** Premiums at the start of the month they fall due in, on the
  contract's own payment mode — every month on 月払, every sixth on 半年払, every twelfth on
  年払; maintenance expense at the start of each month, a twelfth of the annual amount;
  acquisition expense and initial commission at issue; death and 高度障害 claims and their
  claim expense at the end of the month in which they arise; ordinary lapse at the end of
  the month, after deaths; the renewal (*kōshin*, 更新) decline at the end of a boundary
  month, after lapse.
- **Rate conversion [std].** Mortality and lapse are quoted per annum and applied per month
  on the **effective** convention `r_m = 1 − (1 − r)^(1/12)`, so that twelve months compound
  back to the annual rate exactly. A nominal `r / 12` would not, and the difference is
  material where the rate is large: 9% a year is 0.782842% a month effective against 0.75%
  nominal, a 4.4% difference in the month's exits. The **renewal decline is not converted**:
  it is a one-off proportion of the survivors of the single month a 保険期間 ends in, not a
  rate per unit time.
- **Age basis [std].** Issue age (*keiyaku nenrei*, 契約年齢) is age last birthday
  (*man-nenrei*, 満年齢) with fractions discarded [S1]; attained age in month `t` is
  `x + ⌊t/12⌋`, so `age(0) = x` and it holds for the twelve months of policy year 1.
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
  rounding: on the anchor cell undiscounted net cash flow is +¥47,254.64 to the ceiling
  against −¥16,071.24 over the first ten years. Reporting either without naming the
  convention says nothing.
- **Rounding.** Intermediates at full precision; displayed cash flows to two decimals of a
  yen, in-force to six decimals **[std]**. Premium rates round to the whole yen per month,
  which is the granularity published rate cards are quoted at [S2] [S9] [S10].

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
| `l(t)` | In-force probability at the **start** of month t; `l(0) = 1` | monthly recursion |
| `k(t)` | Term index: 1 in the original 保険期間, 2 after the first 更新, … | boundary months |
| `P_m(t)`, `P_a(t)` | Monthly and annualized premium in force; constant within a term | boundary months |
| `q(t)`, `q_m(t)` | Best-estimate death-and-高度障害 rate (**one** decrement), annual and per month | assumption lookup |
| `w(t)`, `w_m(t)` | Ordinary lapse rate (end of month, after deaths), annual and per month | assumption lookup |
| `d(t)` | Renewal-decline **proportion**; non-zero only in a boundary month, never converted | boundary months |
| `D(t)` | Expected claims in month t = `l(t) × q_m(t)` | monthly |
| `lap(t)` | Lapsed-but-reinstatable population, 36 monthly vintages (復活 module; 0 in base run) | monthly |
| `CF(t)` | Net cash flow of month t, insurer perspective (+ = inflow) | monthly |

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
| Suicide-exclusion offset | None: policy years 1–3 (`t = 0 … 35`) claims are not reduced for excluded suicides | clause [S1]; offset **[std]** (3) |

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

| Policy year `y(t)` | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| Projection months `t` | 0–11 | 12–23 | 24–35 | 36–47 | 48+ |
| Annual lapse `w(t)` **[std]** | 9% | 7% | 6% | 5.5% | 5% |
| Monthly `w_m(t) = 1 − (1 − w)^(1/12)` | 0.782842% | 0.603288% | 0.514520% | 0.470048% | 0.426532% |

`lapse_table.csv` is keyed by the **contractual, 1-based** policy year, so `lapse_rate(t)`
reads it at `y(t) = 1 + ⌊t/12⌋` and carries the last row forward; the table itself stays
annual — the rate is the observation — and `lapse_rate_mth(t)` derives the month's
decrement from it. The simple mean over the first ten
years is 5.75% and the in-force-weighted mean 5.94%, both a little above 5.6% — the
expected direction, since the industry figure is dominated by long-duration in-force sum
assured while this is an early-duration protection curve. The level is anchored; the
**shape** is a convention with no Japanese published evidence behind it. Lapse pays
nothing: there is no 解約返戻金 [S1].

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
| Renewal commission `c_r` | 5% of premiums from policy year 2, i.e. `t ≥ 12` | **[std]** |
| Commission at 更新 | **None** in the base run | **[std]** (4) |
| Maintenance expense `e_m(t)` | ¥4,000 p.a. taken as ¥4,000/12 a month, inflating 1.0% **a year** | **[std]** |
| Claim expense `ec` | ¥30,000 per death / 高度障害 claim | **[std]** |

4. A 更新 is not new business — no new 保険証券 is issued and no 告知 taken [S1] [S4] — so
   the base run pays no acquisition commission at a renewal. That is a choice, not a fact:
   no document in the set discloses a commission scale at all, and a scale paying
   first-year rates on each renewed term would change the sign of the cash flow at
   `t = 120, 240, 360` and `480`. The model exposes it as a switch and the pitfall list
   tests it.

The **¥248 monthly policy fee is a premium component, not an expense recovery** [S2]. It
enters the model only through `P_m`; crediting it against `e_m(t)` counts it twice.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning | cells |
|---|---|---|
| `t` | projection **month**, 0-based: `t = 0..T−1`. `T = 12(w_r − x)` for 年満了, `12n` for 歳満了 | — |
| `T` | the **number** of projected months, `proj_len()`; the last index is `T − 1` | `proj_len` |
| `y(t)`, `duration(t)` | contractual policy year `1 + ⌊t/12⌋`, and completed years `⌊t/12⌋` | `policy_year`, `duration` |
| `x` | 契約年齢 (満年齢); attained age in month t is `x + ⌊t/12⌋` | `age` |
| `k` | term index, contractual and **1-based**; `k = 1 + ⌊duration(t) / n⌋` for 年満了 | `term_index` |
| `SA` | sum assured, JPY, level | `sum_assured` |
| `f` | flat monthly policy element, ¥248 | `policy_fee_m` |
| `r(sex, x, m)` | marginal monthly rate per ¥5,000,000 of cover, entry age x, term m | `prem_rate_m` |
| `P_m(k)`, `P_a(k)` | monthly and annualized premium in term k; `P_a = 12 × P_m` | `premium_mth_pp`, `prem_pp` |
| `p` | months between premium payments: 1 on 月払, 6 on 半年払, 12 on 年払 | `prem_mode_months` |
| `Pd(t)` | premium falling due in month t: `p × P_m` if `t mod p = 0`, else 0 | `prem_due_pp` |
| `q(t)`, `q_m(t)` | best-estimate death-and-高度障害 rate, annual and `1 − (1 − q)^(1/12)` | `mort_rate`, `mort_rate_mth` |
| `w(t)`, `w_m(t)` | ordinary lapse rate, annual and `1 − (1 − w)^(1/12)` | `lapse_rate`, `lapse_rate_mth` |
| `d(t)` | renewal-decline proportion; 0 unless `(t + 1) mod 12n = 0`, i.e. unless month t is the last of a 保険期間 | `decline_rate` |
| `l(t)` | in-force probability at the start of month t; `l(0) = 1` | `pols_if` |
| `D(t)` | expected claims in month t = `l(t) × q_m(t)` | `pols_death` |
| `E0`, `e_m(t)` | acquisition expense; maintenance `(4,000 / 12) × 1.01^(y(t) − 1)` per policy | `expense_acq`, `expenses` |
| `c0`, `c_r` | initial commission `0.50 × P_a(k = 1)`, the first term's annualized premium (`prem_pp(0)`); renewal rate 0.05 from `t = 12` | `commissions` |
| `ec` | claim expense per claim, ¥30,000 | `expense_claim` |
| `CF(t)` | net cash flow of month t (+ inflow) | `net_cf` |

Dimensional check: `q`, `w`, `l`, `D` are dimensionless probabilities, and so is `d` — but
`q` and `w` are rates **per year** while `q_m`, `w_m` and `d` apply to a **month**. `SA`,
`E0` and `ec` are JPY per policy; `P_a` is JPY per policy per year and is a pricing quantity
rather than a cash flow; `f`, `P_m`, `Pd` and `e_m` are JPY per policy **per month**; `r` is
JPY per month per ¥5,000,000 of cover, so `r × SA / 5,000,000` is JPY per month. Every term
of `CF(t)` is JPY per **month** per policy issued.

### Premium chassis

The published rate structure decomposes exactly [S2]:

    P_m(k) = f + r(sex, x_k, m_k) * SA / 5,000,000
    x_k    = x + (k - 1) * n              (attained age at the k-th term's start)
    m_k    = min(n, w_r - x_k)            (truncation at the ceiling)
    P_a(k) = 12 * P_m(k)                  (a pricing quantity, not a cash flow)
    Pd(t)  = p * P_m(k(t))  if t mod p = 0, else 0      (what actually falls due)

`P_m` is the rate card's own quantity and, on this grid, the cash flow as well: the annual
step had to annualize it to get a row and this one does not. The **payment mode** decides
how many months' worth fall in a given month — `p = 1` on 月払, 6 on 半年払, 12 on 年払, the
first instalment of each at `t = 0` — and the mode changes the **timing** and not the annual
amount, because mode discounts and 前納 discounts are insurer-set and unpublished
[S1] [S7] [S9] [S14] **[std]**.

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

For `t = 0..T−1`, in this order **[std]**:

1. **Start of month.** Premium income `Pd(t) × l(t)` — zero in the months the mode does not
   make a payment fall in; maintenance `e_m(t) × l(t)`; renewal commission
   `c_r × Pd(t) × l(t)` for `t ≥ 12`. At `t = 0` additionally `E0` and `c0` per policy
   issued (`l(0) = 1`).
2. **Decrement lookup.** `q(t)` at attained age `x + ⌊t/12⌋` and `q_m(t)` from it; `w(t)`
   from the lapse table, read at policy year `y(t)`, and `w_m(t)` from it;
   `d(t) = d` if `(t + 1) mod 12n = 0` and `t < T − 1`, else 0.
3. **End of month — claims.** `D(t) = l(t) × q_m(t)`; claim outgo `SA × D(t)`; claim expense
   `ec × D(t)`. One decrement, one benefit: death and 高度障害 are not added.
4. **End of month — ordinary lapse.** `l(t) × (1 − q_m(t)) × w_m(t)` leave, applied to
   survivors of mortality. **Nothing is paid** — there is no 解約返戻金 [S1].
5. **End of a boundary month — renewal decline.**
   `l(t) × (1 − q_m(t)) × (1 − w_m(t)) × d(t)` leave, applied after lapse. Nothing is paid.
   Note the asymmetry: the first two factors are monthly conversions of annual rates and the
   third is not converted at all, because it is one decision taken on one date.
6. **Roll forward**, plus any 復活 reinstatements (zero in the base run).

       l(t+1) = l(t) * (1 - q_m(t)) * (1 - w_m(t)) * (1 - d(t)) + lap(t) * rho_m

7. **Repricing at a boundary.** `k(t+1) = k(t) + 1` and `P_m` is recomputed at the attained
   age reached at the renewal, `x + duration(t) + 1`, over the term
   `m = min(n, w_r − (x + duration(t) + 1))`. The projection horizon does **not** change;
   the term shortens instead.

Because the conversion in step 6 is the effective one, `l` at every anniversary is exactly
what an annual-step projection of the same bases produces: `(1 − q_m)^12 = (1 − q)` and
`(1 − w_m)^12 = (1 − w)`, and the decline falls in the month the policy year ends either
way. That is the arithmetic check that the grid was changed and the basis was not.

At `t = T − 1` the projection ends: no maturity payment, no run-off, no tail states [S1] [S8]
[S10] [S14]. The identity the model must satisfy at every `t` is

    l(t) - l(t+1) = D(t) + lapses(t) + declines(t) - reinstatements(t)

which `check_pols_roll_fwd()` asserts over all `t` and returns as a single `bool`. The
reinstatement term is zero in the base run and is carried in the identity anyway, so the
same residual closes in **both** positions of the 復活 switch rather than one form of the
check being right for each.

### Net cash flow

    CF(t) = Pd(t) * l(t)                              (premiums)
          - SA * D(t)                                 (death and 高度障害 claims)
          - ec * D(t)                                 (claim expense)
          - e_m(t) * l(t)                             (maintenance)
          - c_r * Pd(t) * l(t) * 1{t >= 12}           (renewal commission)
          - (E0 + c0) * 1{t = 0}                      (acquisition)

`net_cf` is income-positive, per the library convention. Lapse and decline contribute no
term: they act only through `l(t)`. A `claims_lapse` column exists and is identically zero
— the zero is the product fact worth publishing, as it is in `Term_UK_S`.

**A [std] the annual grid needed and this one does not.** On an annual step a full year's
premium was collected in advance from lives that might exit in month two, which overstated
premium income, and the offsetting understatement was the end-of-year claim timing; the two
were declared a matched pair and a further half-year adjustment was forbidden. Here a policy
pays for the months it is in force and its claim falls in the month it arises, so neither
approximation is made and neither offset is needed. What remains is a within-month
convention only — premium at the start of the month, claims at the end of it — worth about a
fortnight of interest on one month's cash flow, which this model does not discount in any
case. The visible consequence is that undiscounted premium income on the anchor cell falls
from ¥470,348.54 to ¥457,507.04.

### Optional modules (all off in the base run)

- **リビング・ニーズ特約.** Acceleration incidence `a(t)` **[std]** (no retrieved document
  gives incidence). On an accelerated amount `A ≤ min(SA, 30,000,000)`:

      payout = A - A * i_ln * 0.5 - 6 months' premiums on A

  with `i_ln` a **[std]** snapshot rate. A full acceleration extinguishes the contract
  retroactively to the claim date; a partial one reduces `SA` from that date and the
  reduced premium continues [S1] [S7] — two transitions, not one benefit with two amounts.
  Barred within **one year** of a non-renewable expiry [S1] [S7] [S8], which on the monthly
  grid is the last twelve months of the projection, `t ≥ T − 12`; on a 更新型 cell that bar
  bites only in the ceiling term. The annual grid could only approximate the clause by
  barring the whole final projected year, which was the same length by coincidence of the
  grid rather than by reading the clause.
- **保険料の払込の免除.** A waiver state on the accident-plus-180-days-plus-別表4 test [S1]
  [S8] [S12] [S14] with **[std]** incidence. 別表4 is a materially lower bar than 別表3 —
  loss of one eye, deafness in both ears, loss of one limb at wrist or ankle [S1] — so the
  waiver incidence is **not** the 高度障害 incidence and must not reuse `q(t)`. While the
  waiver runs, premium income stops, cover continues and alteration rights switch off [S1].
- **復活.** A lapsed-but-reinstatable population with a three-year window `W = 3` [S1].
  The window runs from **each life's own 失効**, so the pool is carried by vintage and not
  as one balance with an indicator on it — a single indicator drops a whole cohort a year
  early or late:

      lap(t)              = sum over s in [max(0, t - W), t - 1] of lapses(s) * (1 - rho)^(t - 1 - s)
      lapses(s)           = l(s) * (1 - q(s)) * w(s)
      reinstatements into l(t+1) = lap(t) * rho
      window expiries(t)  = lapses(t - W) * (1 - rho)^W, and 0 for t < W

  (the vintage index `s` is the same 0-based projection index as `t`, so `lap(0) = 0`)

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
ceiling attained age 80, 保険金額 ¥10,000,000, 月払保険料 **¥974** [S2], 月払 mode, so
`P_a = ¥11,688` **[std annualization]**. Horizon `N = 80 − 30 = 50` years, which on the
monthly grid is **600 rows**, `t = 0..599`; the boundary months — the last month of each
保険期間 — are `t = 119, 239, 359, 479` (the last months of policy years 10, 20, 30 and 40).
Base run: no rider, no waiver, no 復活, no selective lapsation, boundary = ceiling.

**Every assumption value the cell uses.** The table rates below come from the canonical
`jplib` proxy of 生保標準生命表2018（死亡保険用）男. Attained ages 30–35 and 40 are sourced
anchors, **read from the published table** [REG-R18] [R4]; ages 36–39 are the **[std]**
log-linear interpolation between the age-35 and age-40 anchors, rounded to 5 decimals. The
best-estimate annual rate is `q(t) = 0.80 × q_x^tab` **[std]**, and the decrement actually
applied to a month is `q_m(t) = 1 − (1 − q(t))^(1/12)`:

| attained age | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `q_x^tab` | 0.00068 | 0.00069 | 0.00070 | 0.00072 | 0.00074 | 0.00077 | 0.00084 | 0.00091 | 0.00099 | 0.00108 | 0.00118 |
| `q(t)` | 0.000544 | 0.000552 | 0.000560 | 0.000576 | 0.000592 | 0.000616 | 0.000672 | 0.000728 | 0.000792 | 0.000864 | 0.000944 |
| `q_m(t)` | 0.00004534 | 0.00004601 | 0.00004668 | 0.00004801 | 0.00004934 | 0.00005134 | 0.00005601 | 0.00006068 | 0.00006601 | 0.00007203 | 0.00007870 |
| anchor? | yes | yes | yes | yes | yes | yes | no | no | no | no | yes |

Lapse `w(t)` = 9% / 7% / 6% / 5.5% / 5% from policy year 5 **[std]**, read by policy year
`y(t) = 1 + ⌊t/12⌋` and applied as `w_m(t) = 1 − (1 − w(t))^(1/12)` — 0.00782842 a month in
policy year 1. The renewal decline `d` = 15% at a boundary month **[std]** is **not**
converted: it is a one-off proportion of the survivors of that single month, not a rate per
unit time. `E0` = ¥15,000, `c0` = 0.50 × 11,688 = ¥5,844, `c_r` = 5% of premium income from
`t = 12` (the first month of policy year 2), `e_m(t)` = (4,000 / 12) × 1.01^(y(t) − 1),
`ec` = ¥30,000, all **[std]**.

The `t` column below is the model's own 0-based index and its unit is the **policy month** —
the `result_cf()` row label — with the policy year `y(t)` beside it.

| t | y(t) | age | `l(t)` | `P_m` | Premiums | Claims | Claim exp | Maint. + acq. | Commission | `CF(t)` |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 30 | 1.000000 | 974 | 974.00 | 453.45 | 1.36 | 15,333.33 | 5,844.00 | −20,658.14 |
| 1 | 1 | 30 | 0.992127 | 974 | 966.33 | 449.88 | 1.35 | 330.71 | 0.00 | +184.40 |
| 2 | 1 | 30 | 0.984315 | 974 | 958.72 | 446.33 | 1.34 | 328.11 | 0.00 | +182.94 |
| 11 | 1 | 30 | 0.916723 | 974 | 892.89 | 415.68 | 1.25 | 305.57 | 0.00 | +170.38 |
| 12 | 2 | 31 | 0.909505 | 974 | 885.86 | 418.48 | 1.26 | 306.20 | 44.29 | +115.63 |
| 119 | 10 | 39 | 0.551431 | 974 | 537.09 | 397.19 | 1.19 | 201.03 | 26.85 | −89.17 |
| 120 | 11 | 40 | 0.466683 | 1,823 | 850.76 | 367.28 | 1.10 | 171.84 | 42.54 | +268.00 |

**Trace, `t = 0` — the first policy month.** `l(0) = 1`; premiums `= 974 × 1 = 974.00`, one
month's premium and not a year's. `q(0) = 0.80 × 0.00068 = 0.000544`, so
`q_m(0) = 1 − (1 − 0.000544)^(1/12) = 0.0000453446` and `D(0) = 0.0000453446`. Claims
`= 10,000,000 × 0.0000453446 = 453.45`; claim expense `= 30,000 × 0.0000453446 = 1.36`.
Expenses `= E0 + e_m(0) = 15,000.00 + 4,000/12 = 15,333.33`; commission
`= c0 = 0.50 × 11,688 = 5,844.00`.
`CF(0) = 974.00 − 453.45 − 1.36 − 15,333.33 − 5,844.00 = −20,658.14`. Roll forward:
`w_m(0) = 1 − (1 − 0.09)^(1/12) = 0.00782842`, so
`l(1) = 1 × (1 − 0.0000453446) × (1 − 0.00782842) = 0.992127`.

**Trace, `t = 1`.** Premiums `= 974 × 0.99212659 = 966.33`. The rates are unchanged —
attained age and policy year both still step on the anniversary — so
`D(1) = 0.99212659 × 0.0000453446 = 0.00004499`; claims `= 449.88`; claim expense `= 1.35`.
Maintenance `= (4,000 / 12) × 1.01^0 × 0.99212659 = 330.71`. **No renewal commission**: the
5% scale starts at `t = 12`, the first month of policy year 2, not at the second row of the
frame. `CF(1) = 966.33 − 449.88 − 1.35 − 330.71 = +184.40`.

**Trace, `t = 12` — the first month of policy year 2.** Attained age 31, so
`q(12) = 0.80 × 0.00069 = 0.000552` and `q_m(12) = 0.00004601`; lapse moves to 7%, so
`w_m(12) = 0.00603288`. Premiums `= 974 × 0.90950496 = 885.86`; claims `= 418.48`;
maintenance `= (4,000 / 12) × 1.01 × 0.90950496 = 306.20`; renewal commission
`= 0.05 × 885.86 = 44.29`. `CF(12) = 885.86 − 418.48 − 1.26 − 306.20 − 44.29 = +115.63`.

**Trace, `t = 119` — the boundary month.** `l(119) = 0.55143099`; premiums
`= 974 × 0.55143099 = 537.09` on the **old** premium, because the repricing takes effect at
`t = 120` and not before. `q(119) = 0.80 × 0.00108 = 0.000864`, `q_m = 0.00007203`;
`D(119) = 0.00003972`; claims `= 397.19`; claim expense `= 1.19`. Maintenance
`= (4,000 / 12) × 1.01^9 × 0.55143099 = 201.03`; renewal commission `= 26.85`.
`CF(119) = 537.09 − 397.19 − 1.19 − 201.03 − 26.85 = −89.17`. Roll forward, in the
processing order and no other: after mortality `0.55143099 × (1 − 0.00007203) = 0.55139127`;
after ordinary lapse `× (1 − 0.00426532) = 0.54903941`; after the renewal decline
`× (1 − 0.15) = 0.46668350`. So `l(120) = 0.466683`, and the three exits of that **month**
are 0.00003972 deaths, 0.00235186 lapses and **0.08235591 renewal declines** — the decline is
**97.2%** of the exits of the month it falls in. The annual grid could only say 74%, because
it was comparing one renewal decision with twelve months of ordinary lapse.

**Trace, `t = 120` — the first month of the repriced term.** Attained age at renewal is
`30 + 10 = 40`, so `P_m(2) = 248 + 2 × 787.5 = 1,823` [S2] and `P_a(2) = 21,876`. Premiums
`= 1,823 × 0.46668350 = 850.76` — **higher than `t = 119`'s despite 15% fewer policies**,
because the premium multiplied by 1.87. `q(120) = 0.80 × 0.00118 = 0.000944`,
`q_m = 0.00007870`; `D(120) = 0.00003672`; claims `= 367.28`; claim expense `= 1.10`.
Maintenance `= (4,000 / 12) × 1.01^10 × 0.46668350 = 171.84`; renewal commission
`= 0.05 × 850.76 = 42.54`.
`CF(120) = 850.76 − 367.28 − 1.10 − 171.84 − 42.54 = +268.00`.

**The same statement by policy year.** `result_cf()` grouped on `⌊t/12⌋` gives the annual
view, with `l` read at the anniversary. It is not the annual-grid model's statement and is
not meant to be: the premium is now collected only from the months a policy is actually in
force, so every premium row is lower.

| y − 1 | `l(12(y−1))` | Premiums | Claims | Claim exp | Maint. + acq. | Commission | Net |
|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 11,194.92 | 5,211.80 | 15.64 | 18,831.25 | 5,844.00 | −18,707.77 |
| 1 | 0.909505 | 10,282.20 | 4,857.30 | 14.57 | 3,554.08 | 514.11 | +1,342.14 |
| 2 | 0.845373 | 9,603.52 | 4,602.46 | 13.81 | 3,352.69 | 480.18 | +1,154.39 |
| 9 | 0.578436 | 6,601.80 | 4,882.11 | 14.65 | 2,471.01 | 330.09 | −1,096.06 |
| 10 | 0.466683 | 9,968.77 | 4,303.62 | 12.91 | 2,013.48 | 498.44 | +3,140.32 |

**The renewal ladder**, five numbers per renewal. `at t` is the boundary **month** — the
last month of the expiring term — so the repriced premium is first charged at `t + 1`:

| Renewal | at t | attained age | `P_m` | `P_a` | jump | `l(t+1)` |
|---|---|---|---|---|---|---|
| — (issue) | — | 30 | 974 [S2] | 11,688 | — | 1.000000 |
| 1st | 119 | 40 | 1,823 [S2] | 21,876 | ×1.87 | 0.466683 |
| 2nd | 239 | 50 | 3,933 [S2] | 47,196 | ×2.16 | 0.234147 |
| 3rd | 359 | 60 | 8,976 **[std]** | 107,712 | ×2.28 | 0.115211 |
| 4th | 479 | 70 | 23,881 **[std]** | 286,572 | ×2.66 | 0.054121 |

Every `l(t+1)` in that table is the number the annual grid published, to the six decimals it
displayed, and so is `l(600) = 0.026042` at the ceiling. That is not a coincidence and it is
the check that the conversion was done right: the monthly decrements are the **effective**
equivalents of the annual ones, `(1 − q_m)^12 = (1 − q)` and `(1 − w_m)^12 = (1 − w)`
exactly, and the renewal decline falls in the month the policy year ends either way. **Every
difference between the two grids is a difference of cash flow timing and none is a
difference of basis.**

Cover ends at attained age 80 with `l(600) = 0.026042` — 2.6% of the cohort still in force
after fifty years and four repricings, paying ¥286,572 a year for ¥10,000,000 of cover.
That row is the economically important one and is not a modeling artefact: a renewable term
at attained-age rates converges on term-cost pricing, and the reason carriers cap renewal
at 80 is that beyond it the product stops being purchasable.

**Totals over the 600 months, undiscounted:** premiums ¥457,507.04, claims ¥302,433.43,
net cash flow **+¥47,254.64**. Over the first 120 months alone — the
`contract_boundary = current_term` answer — net cash flow is **−¥16,071.24**. The shape is
the protection shape seen a month at a time: one very deep month at issue (¥20,844 of
acquisition cost against ¥974 of premium, where the annual grid had a whole year's ¥11,688
sitting on the same row to meet it), thin positive months through the middle of each term,
months turning negative as each 保険期間 runs out and the level premium falls behind the
rising mortality cost, and a jump back into surplus in the first month of the repriced term.

**Why the totals moved.** The annual grid collected ¥470,348.54 of premium and this one
collects ¥457,507.04, 2.7% less, for one reason: it stops collecting from lives that have
already left. On an annual step a policy that lapsed in the second month of a policy year
had nonetheless paid that whole year's premium in advance, and the notes offset that
overstatement against claims booked at the end of the year, declaring the two a matched pair
and warning against correcting either alone. The monthly grid makes neither approximation,
so it needs neither offset — and the ¥3,145.61 the net cash flow falls by is the residue of
a **[std]** this version of the model no longer has to make.

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
   no `uklib` analogue. Undiscounted net cash flow over the 600 months runs **+¥86,882.78
   at d = 0%, +¥47,254.64 at 15%, +¥20,786.34 at 30%** — a factor of four across a range no
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
6. **Early-duration lapse against front-loaded acquisition cost.** ¥20,844 of outgo at
   `t = 0` against ¥11,688 of premium on the same `t = 0` row makes the first three lapse
   rates decide how long the strain takes to recover. No Japanese clawback evidence exists
   in the sources.
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
  model only through `P_m` itself; crediting it against maintenance expense counts it twice,
  and `P_m` must reconstruct as `248 + 2 × 363 = 974` on the anchor cell, `P_a` as
  `12 × 974 = 11,688`.
- **Renewal decline is not lapse, and it is not a rate.** It applies only in boundary
  **months**, only after mortality and ordinary lapse, and it is never converted to a
  monthly equivalent, because it is a decision taken on a date rather than a hazard running
  through a period. It dominates the month it falls in: at `t = 119` on the anchor cell it
  is 0.08235591 of 0.08474749 total exits, **97.2%**. Folding it into `w(t)` makes the
  boundary invisible and mis-times most of the cohort's departure.
- **A failed first renewal premium is an expiry, not a lapse.** Where the first premium of
  the renewed contract goes unpaid through grace, the renewal is treated as never having
  happened and the contract terminates at the **original** expiry rather than being 解除
  [S1] [S7]. Those lives must not appear in force at `t + 1` collecting the renewed
  premium, and must not be counted as a mid-term lapse of a term that never began. The
  monthly grid makes the two *separable* for the first time — grace is about a month long
  [S1] [S8], which is now one step rather than a fraction of one — but separating them needs
  a take-up assumption the sources do not give, so the composite still carries one rate.
- **The living-needs cap is per insured, aggregated across contracts** — not per contract
  [S1] [S7] [S8] [S12]. Inside the composite's ¥1,000,000–¥30,000,000 envelope it is
  therefore *exactly reached* at the ceiling and never reduces a single-contract payment. A
  model reporting the cap biting at `SA = 30,000,000` has a strict-versus-weak inequality
  error; a model applying it per contract has misread the clause.
- **Read the table at the right age.** 契約年齢 is 満年齢 [S1] and 標準生命表2018 is built for
  保険年齢 [REG-R20]. The base run reads at 満年齢 and understates, so the shift module must
  move `q` up, not down.
- **Naming the boundary is part of reporting the number.** The same cell gives +¥47,254.64
  to the ceiling and −¥16,071.24 over the current term. Neither is an ESR current estimate
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
