# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify the reference liability cash-flow projection model
**`EC_FR_S`**, on a **monthly** grid, for the standardized composite eurocroissance support
defined in `product-spec.md` (same directory). This is not any single insurer's support.
[S#]/[R#] tags refer to the source list in `sources.md` (numbering carried verbatim from
`_research/eurocroissance.md`); [REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md`. **[std]** marks standardizations
introduced for the reference implementation; [unverified] marks claims not confirmed against
a retrieved document. Parameter values are identical to those in `product-spec.md`.

Two facts about the sourcing govern how these notes must be read. First, **no contractual
document for any eurocroissance support was retrieved** [S10]: the mechanics come from the
Code des assurances [R1] [R2] [R3] and from one published actuarial *mémoire* [R13], and
every insurer-level parameter is either a third-party fact-sheet figure [S8] or **[std]**.
Second, this product is a **fund-level** construct — the part value is common to all
engagements of an auxiliary account [R2 R. 134-2](#frlib-eurocroissance-r2), and the PCDD and the *provision pour
garantie à terme* are collective [R8] — so a single-policy projection is an abstraction that
must be handled explicitly; see "Known modeling pitfalls". The sibling euro-fund notes at
`../assurance_vie_euro/technical-notes.md` were drafted in parallel with these, so where the
two products are compared here the comparison is made against the Code des assurances
directly rather than against that document.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums in; surrender, death
  and maturity claims out; charges; the insurer's asset contributions) for single-policy
  eurocroissance model points on the two composite chassis — **Chassis A** (1° engagement:
  *provision mathématique* plus parts) and **Chassis B** (2° engagement: parts only, guarantee
  at maturity). Reserves are not computed here.
- **Projection frequency [std]: monthly**, on policy months, with the policy anniversary
  still the single date every annual event lands on. **A monthly grid is not a monthly
  product.** Every *contractual* mechanic of the composite is annual and the model keeps it
  there: the striking of the *compte de participation aux résultats* and the allocation of
  its balance [R2 R. 134-4](#frlib-eurocroissance-r2), the R. 134-3 base 5° performance
  levy taken at that striking, free *versements*, and the R. 134-12 *apport d'actifs*, all
  on the **anniversary**; the base 4° parts levy and scheduled *versements* at the
  **opening of the policy year**, where `product-spec.md` puts them. What the finer grid
  adds is what A. 134-5 already required and the annual grid could not express: the
  **re-striking of the diversification provision at an intermediate value in every month in
  which the participation account is not struck**, and a **forward** part value for an exit
  [R3 A. 134-5](#frlib-eurocroissance-r3) — so the conversion **removes** a documented
  simplification rather than adding one. It also puts mortality and *rachat* in the month
  they happen and maintenance expense where it is incurred. An annual step remains a
  well-defined special case of the recursions below and reproduces every anniversary value
  exactly — see *Anniversary equivalence* — but it is not what the reference model runs.
- **Time index [std].** `t` is **0-based** and counts **policy months**, as in lifelib's
  `basiclife/BasicTerm_S`: month `t` runs from time `t` to time `t + 1`, `t = 0` is the
  issue month, and the frame is `t = 0 … T − 1` with `T = proj_len = 12 n` the *number* of
  policy months projected; the last row is the month that ends at the *échéance*. Because
  every contractual schedule is annual, the policy year is **derived** and used as a lookup
  key: `dur(t) = t // 12` is the completed policy years at the start of month `t` and the
  contractual **policy year is the 1-based label `dur(t) + 1`**; where these notes say
  "policy year y" as contract language, the months are `t = 12(y − 1) … 12y − 1`. **Nothing
  is indexed by the policy year.** The **anniversary** is the last month of a policy year,
  `t ≡ 11 (mod 12)`, and that is where every annual event lands. An in-force cell opens at
  `t = 12 × duration_ifo`; elapsed time is recorded in whole policy years, so the frame
  always opens in the **first month of a policy year**. **The issue instant is not a row:**
  the initial *versement* creates the rights and strikes both provisions as the *opening
  state* of the first projected month, written `A_open(t)`, `pd_open(t)`, `N_open(t)`,
  `mg_open(t)` below and reached in the model as `own_assets_at(t, "BOM")` and its
  siblings; its cash flows are beginning-of-month flows of that first month. A few
  quantities are indexed by a **month boundary** `m` instead — `TEC`, `i_pm(m)`, the
  discount factor and the remaining term `rem(m) = (T − m)/12` years — with `m = 0` at
  issue and `m = T` at the *échéance*, so month `t` opens at `m = t` and is struck at
  `m = t + 1`.
- **Decrement and return conversion [std].** Every assumption in this product is published
  and tabulated **annually** — the mortality table by attained age, the *rachat total* and
  *rachat partiel* vectors by policy year, the scenario return by year — and the monthly
  figures the recursion applies are derived from them at the constant-force conversion, so
  that twelve compound back to exactly the annual figure:

  ```
  q_m(t)   = 1 − (1 − q(t))^(1/12)          w_m(t)  = 1 − (1 − w(t))^(1/12)
  w_pm(t)  = 1 − (1 − w_p(t))^(1/12)        r_m(t)  = (1 + r(t))^(1/12) − 1
  ```

  The unsuffixed symbols keep the annual meaning these notes tabulate. No retrieved French
  source states a conversion convention for any decrement, so the conversion is **[std]**.
- **The provisions are state variables, not cash flows.** Policy cash flows are premiums,
  claims, charges and expenses; `pm`, `pd`, `parts` and `part_value` drive claim amounts
  through the surrender, maturity and death formulas [R2 R. 134-5, R. 134-6](#frlib-eurocroissance-r2).
- **Two liability layers.** The savers' layer (`pm`, `pd`) is inside the auxiliary account.
  The insurer's layer (`pgt`, `insurer_contribution`, `pcdd`) is *not* the savers' money: the
  PGT is funded from own funds and sits outside the participation account [R3 A. 134-2](#frlib-eurocroissance-r3)
  [R1 L. 134-3](#frlib-eurocroissance-r1), and the PCDD is collective with no individual rights [R8 R. 343-3 10°](#frlib-eurocroissance-r8). Both
  are reported separately and never enter a benefit.
- **Timing conventions [std].** Monthiversary (BOM) processing. The charge in number of
  parts and the scheduled *versement* fall at the beginning of the month, **in the months
  that open a policy year** (`t ≡ 0 mod 12`); a *rachat partiel* at the beginning of every
  month; the asset return accrues over the month; at the **end of the month** (EOM) the two
  provisions are re-struck and `pd` and `part_value` determined, and any insurer
  contribution is computed on that striking; decrements and claims follow at EOM after the
  striking. **On the anniversary only** (`t ≡ 11 mod 12`), and before the striking, the
  participation account is struck and its balance allocated, the base 5° performance levy
  is taken on the policy year's accumulated financial performance, the insurer's asset
  affectations are made, and any free *versement* is paid and the provisions re-struck on
  the post-*versement* state — in the processing order below. State variables are stored at
  EOM.
- **Age basis.** *Âge atteint* (age last birthday) **[std]** — art. A. 335-1 applies the
  homologated tables with the annexed *décalages d'âge* rather than fixing a model age basis
  [REG-R23]. **Age changes on the policy anniversary, not on the birthday and not
  monthly**: `x + dur(t)` is the age entering the policy year of month `t` and
  `x + dur(t) + 1` the age attained at the anniversary that closes it. The annual mortality
  rate is read at the latter — the notes' `q(x + t + 1)`, which keeps the age rule the
  annual assumption was built on — and applied monthly at `q_m`.
- **Currency and rounding.** EUR; single-policy model points projected on an expected
  (probability-weighted) basis, `pols_if` multiplying per-policy amounts. Intermediate values
  at full precision; currency to the cent, parts and part values to four decimals **[std]**.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 (Chassis A), 2 (Chassis B) |
| `engagement_modality` | enum {`euro_and_parts`, `parts_only`} | `euro_and_parts` / `parts_only` |
| `issue_age` | int (âge atteint) | 57 |
| `sex` | enum {M, F} | M |
| `policy_term` | int, years to the *échéance* `n`; also the number of periods projected | 10 |
| `duration_ifo` | int, completed policy years at valuation — an elapsed count, already 0-based, and the first projected period of an in-force cell | 0 |
| `premium_gross` | currency, initial *versement*; the opening state of the first projected period | 10,000.00 |
| `premium_top_up` / `premium_top_up_t` | currency, free additional *versement*, and the **contractual policy year** at whose end it is paid (1-based, so policy year `k` is period `k − 1`; 0 means none) | 2,000.00 / 3 |
| `guarantee_rate` | %, `g` — share of net premiums guaranteed at `n` | 100 % |
| `entry_charge_rate` | %, base R. 134-3 1° | 2.00 % |
| `parts_charge_rate` | % p.a., base R. 134-3 4° | 0.80 % |
| `perf_charge_rate` | % of positive financial performance, base R. 134-3 5° | 10 % |
| `exit_charge_rate` | %, base R. 134-3 6° | 0.00 % |
| `part_value_init` / `min_part_value` | currency, part value at the account's inception and its contractual floor [R2 R. 134-1](#frlib-eurocroissance-r2) | 10.0000 / 5.0000 |
| `parts_ifo`, `pm_ifo`, `own_assets_ifo` | float / currency / currency — parts, PM and account assets at valuation (in-force cells) | — (new business) |
| `lock_up_years` | int, non-surrender period, capped at `min(n, 8)` [R2 R. 134-5](#frlib-eurocroissance-r2) | 0 |
| `surrender_indemnity_rate` | %, capped at 5 %; R. 132-5-3 lets the contract provide for **no indemnity at all** once ten years have elapsed [R10], and the reference contract charges none at any duration. `EC_FR_S` returns 0 beyond ten years unconditionally **[std]** | 0.00 % |
| `death_floor_flag` | bool — *garantie décès plancher* [S1] [S2] | true |
| `annuity_option_flag` | bool — conversion into a *rente viagère* at `n` [R2 R. 134-6](#frlib-eurocroissance-r2) | false |

---

## State variables

Every state variable below is the **closing** value of month `t`; its opening value is
written `X_open(t)`, which is `X(t−1)` in every month but the first projected one and, in
that one, the state the initial *versement* or the in-force extract creates.

| Variable | Description | Updated |
|---|---|---|
| `mg` | Guaranteed amount payable at the *échéance* = `g ×` cumulative net premiums, run down for exits [R13] | on each *versement* and exit |
| `own_assets` | Auxiliary-account assets attributable to the policy, at realisation value, **excluding** any outstanding insurer contribution [R2 R. 134-8](#frlib-eurocroissance-r2) | monthly recursion |
| `pm` | *Provision mathématique* = `mg` discounted at `i_pm` over the fractional remaining term (Chassis A only; identically 0 on Chassis B) [R2 R. 134-2](#frlib-eurocroissance-r2) | EOM re-strike, every month |
| `pd` | *Provision de diversification*, the savers' individualised rights [R8 R. 343-3 9°](#frlib-eurocroissance-r8) | EOM residual, floored, every month |
| `parts` | Number of *parts de provision de diversification* [R2 R. 134-2](#frlib-eurocroissance-r2) | levy at the opening of a policy year; on *versements* and exits |
| `part_value` | *Valeur de la part*, `pd / parts`; common to the whole auxiliary account [R2 R. 134-2](#frlib-eurocroissance-r2) | EOM; the A. 134-5 intermediate value in eleven months of twelve |
| `insurer_contribution` | Outstanding L. 134-3 asset contribution completing the representation (Chassis A) | EOM |
| `pgt` | *Provision pour garantie à terme*, insurer's own funds (Chassis B) [R3 A. 134-2](#frlib-eurocroissance-r3) | EOM |
| `pcdd` | *Provision collective de diversification différée*, fund-level [R8 R. 343-3 10°](#frlib-eurocroissance-r8) [R9] | anniversary *apport*, fund extension |
| `pols_if` | In-force probability at the **start** of month `t`; `pols_if(0) = 1`. The end-of-month count `l(t)` is `pols_if_at(t, "AFT_DECR")` | EOM decrements, at `q_m` then `w_m` |
| `cum_prem_net` | Cumulative net *versements*, the base of the death floor [S1] [S2] | on each *versement* and *rachat partiel* |

---

## Assumption inputs

Three classes are distinguished. Class (a) is contractual or statutory; class (b) is the
insurer's current discretionary scale, exercised inside the R. 134-4 destinations [R2];
class (c) is the modeler's view of experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Guarantee level `g` / maturity `n` | 100 % of net *versements* / 10 years | [S1] [S2]; 80 % and 8–30 [S8]; 80 %–100 % and 8–40 [S7] |
| Guarantee run-down for exits | `mg` reduced pro rata to surrenders and deaths | [R13] |
| PM definition (Chassis A) | `pm(t) = mg(t) × (1 + i_pm(t+1))^-(T-t-1)/12` — struck at the **month's** end, boundary `t + 1`, which is `(T − t − 1)/12` years short of the *échéance* | [R2 R. 134-2](#frlib-eurocroissance-r2) |
| PM discount rate `i_pm` | ≤ **90 % of the last TEC*n***, linear interpolation between bracketing maturities, longest TEC beyond the curve, **floor 0 %**, method choice irreversible per account. As retrieved, A. 134-1 fixes *n* as the holder's **guarantee maturity** (per-engagement method 1°) or the account's 1°-engagement **duration** (method 2°); this model applies method 1° and re-reads *n* as the **remaining** term at each valuation date — on a monthly grid, at every **month boundary** `m` and at the fractional remaining term `rem(m) = (T − m)/12` years, on the **most recently published** curve, row `m // 12` | haircut, interpolation and floor [R3 A. 134-1](#frlib-eurocroissance-r3); the remaining-term re-reading and its monthly frequency **[std]**, note below |
| Reference TEC10 | 2.50 % at month boundaries `m` = 0–71, 1.00 % from `m` = 72 (curve years 0–5 then 6+) → `i_pm` 2.25 %, then 0.90 % | **[std]**, product-spec (5) |
| Minimum part value | €5.00 — the part value may not be reduced below it to absorb a debit balance | requirement [R2 R. 134-1, R. 134-4](#frlib-eurocroissance-r2); level **[std]**, product-spec (2) |
| Surrender value | Chassis A `pm + parts × part_value`; Chassis B `parts × part_value`; **no guarantee before maturity on Chassis B** | [R2 R. 134-5](#frlib-eurocroissance-r2) |
| Maturity amount | at the *échéance*, the close of the **last projected month** `T − 1`: Chassis A `pm + parts × part_value`; Chassis B `max(parts × part_value, mg)` | [R2 R. 134-6](#frlib-eurocroissance-r2) |
| Death benefit | The current provision value; the maturity guarantee does **not** apply. Any death floor is a complementary guarantee provisioned **outside** the account | [R2 — no death article in Chapter IV, R. 134-7](#frlib-eurocroissance-r2) [R13] [S1] [S2] |
| Surrender indemnity | 0 %; statutory cap 5 % of the present value of the mutual engagements, and the contract **may** provide for none once ten years have elapsed | cap and the ten-year **permission** [R10]; level **[std]**, product-spec (3) |
| Permitted charge bases | The six of R. 134-3 only; base 3° unavailable in a 1° account | [R2 R. 134-3](#frlib-eurocroissance-r2) |
| PGT (Chassis B) | `max( PV(guarantees) − pd − pcdd, 0 )`, A. 132-18 tables, rate ≤ 90 % of TEC, no cash flows other than guarantee maturities and mortality. The shipped per-policy `pgt` omits the **survival factor** on the guarantee maturity **[std]** — see "The PGT's mortality driver" below | article [R3 A. 134-2](#frlib-eurocroissance-r3) [R10]; the omission **[std]** |
| PCDD release horizon / apport d'actifs | 15 years / ≤ 10 % of the PD at the affectation date, endowing the PCDD, re-allocated by year 16 | [R9 A. 132-16](#frlib-eurocroissance-r9); [R7 R. 134-12](#frlib-eurocroissance-r7) |
| Assets at realisation value | R. 343-11 / R. 343-12 | [R2 R. 134-8](#frlib-eurocroissance-r2) |

**The `n − k` re-reading of A. 134-1 — [std].** The article as retrieved gives the index
maturity as the holder's guarantee maturity (method 1°) or the auxiliary account's
1°-engagement duration (method 2°), and says nothing about how that maturity is re-read at
valuation dates after inception [R3 A. 134-1](#frlib-eurocroissance-r3). Two readings are
available: hold *n* fixed at the original term for the life of the engagement, or take the
**remaining** term at each valuation date, which is the horizon the guarantee is
actually discounted over.
These notes and `EC_FR_S` take the second — the first would discount a one-year promise at a
ten-year constant-maturity rate at the *échéance*, and A. 134-1's own method 2° keys the
index to a **duration**, which shortens as the engagements run off. The reading is
**[std]**; it is not stated in the article. `product-spec.md` states A. 134-1 as retrieved,
and **these notes are the source of truth for the value `i_pm` takes in the model.** The
choice is numerically invisible on a flat curve — the worked example's TEC is flat, so both
readings give `i_pm` = 2.25 % then 0.90 % — and live on a sloped one, which is why shipped
model point 10 runs the `sloped` scenario.

**The monthly frequency of the re-strike is also [std], and is the same article read
finer.** R. 134-2 defines the PM as the guaranteed amount discounted at the A. 134-1 rate,
a definition that has a value at every instant rather than only at a striking, and A. 134-5
requires the diversification provision to be re-struck at an intermediate value **at least
monthly** — which on Chassis A is impossible without a PM for the residual to be taken
against. So the model re-strikes `pm` every month at the **fractional** remaining term
`rem(t + 1)`. Holding it flat between annual strikings would make it a step function and
push a whole year of time effect onto the anniversary, so the intermediate part value would
be wrong in exactly the direction A. 134-5 exists to prevent. Two things follow. The
**remaining maturity** the curve is interpolated at moves month by month, while the **curve
row** does not: `tec_curve.csv` publishes one curve per elapsed year and the model reads
row `m // 12`, the *dernier TEC publié*, because interpolating a curve level between
published years would invent data the file does not contain. The consequence is a clean
split of the PM's movement into a **time effect that accrues monthly** and a **rate effect
that lands whole on the anniversary**; the worked example below shows it. And the funding
identity `pm(t) × (1 + i_pm(t+1))^rem(t+1) = mg(t)` then closes in **every month** rather
than only at anniversaries.

### (b) Insurer-discretionary current elements

| Input | Value | Basis |
|---|---|---|
| Entry charge (base 1°) | 2.00 % of each *versement* | [R13]; 4.50 % max [S8]; **[std]**, product-spec (7) |
| Parts levy (base 4°) | 0.80 % p.a. of parts, taken in the **first month of each policy year** on the opening part value `u_open(t)` | [R13]; routing **[std]**, product-spec (8) |
| Performance levy (base 5°) | 10 % of the **policy year's** positive financial-management performance, taken on the **anniversary**; 0 % of negative | [R13]; **[std]**, product-spec (9) |
| Exit charge (base 6°) / conversion charge (base 2°) | 0.00 % / 0.50 % of amounts converted (Chassis A) | **[std]**, product-spec (9); [S8] |
| Credit-balance allocation | Raise the **part value**; no new parts awarded | **[std]**, product-spec (10) |
| PCDD piloting target | Insurer's own euro-fund net rate **+0.30 %**; everything above it to the PCDD | [R13]; **[std]** in the base run (`pcdd = 0`) |
| Apport d'actifs level | 10 % of net premiums for the first three years | [R13]; **[std]** in the base run (0) |
| Credited-return context | 2025 net returns 0.90 %–3.40 % across seven supports; AXA Fonds Croissance 2.50 %–4.50 %, average 3.13 % | [S9] [S3] [S8] |
| Commercial bonus uplift | +2.00 % on new money in the promotion year, subject to a ≥ 45 % unit-linked condition. **Not an input to `EC_FR_S`**, and not held at zero by a switch: there is no uplift Reference, no cells and no model-point column, because a commercial promotion is a marketing device rather than a term of the statutory mechanics these notes specify. Recorded here as market context only | [S3] [S4]; out of scope **[std]** |

### (c) Behavioral / experience assumptions (modeler's view)

The regulatory tables the code points to — TH 00-02 / TF 00-02 for non-annuity contracts
[REG-R22], TGH05 / TGF05 for annuities [REG-R21], applied under art. A. 335-1 with the
annexed *décalages d'âge* [REG-R23] — are **cited by name and never shipped**; A. 132-18 also
permits an insurer's own table certified by an independent approved actuary [R10], so no
single market basis exists. The reference decrement table is a **[std]** proxy built from the
freely redistributable INSEE series [REG-R24].

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base mortality | 80 % × a **[std]** smooth Makeham curve *shaped like* the INSEE *quotients de mortalité* [REG-R24] and anchored so that the 80 % factor gives exactly **0.5000 %** at male 57, the worked example's entry age; sex-distinct, age last birthday; no improvement in the base run. It is **not** the INSEE series itself — `mort_table.csv` carries the same statement in its own provenance column | proxy **[std]**; shape from [REG-R24]; tables cited and never shipped [REG-R22] [REG-R23] |
| Full surrender (*rachat total*) | 2.5 % p.a., level | [R13] observes 2 %–3 % p.a.; level **[std]** |
| Partial surrender (*rachat partiel*) | 6 % of average encours in years 1–2, then 3 %; dynamic multipliers per Policyholder behavior modeling. **Annual, and spread over the twelve months at `w_pm`** — a rate on an *average* encours is a continuous drip, and an owner election can be made in any month | [R13] observes 6 % then 2 %–4 %; **[std]** |
| Asset return `r(t)` | 4.0 % p.a. base; the worked example uses an explicit shock path. **Annual, and spread over the twelve months at `r_m = (1 + r)^(1/12) − 1`** | scenario **[std]** |
| Asset management fees | 0.20 % equities, 0.10 % bonds, deducted from the asset return | [R13] |
| Insurer expenses | Acquisition 5 % of premiums; maintenance 0.20 % p.a. of `pm + pd`, **accrued at one twelfth a month**; acquisition commission 2 % of the initial premium | [R13] |
| Worked-example decrements | `mort_rate = 0`, `lapse_rate = 0`, so `pols_if(t) = 1` | **[std]** — isolates the provision mechanics |

Deterministic single-scenario projection is the base. The maturity guarantee is a put option
on the auxiliary account and its cost requires stochastic market-consistent valuation; the
*mémoire* runs 1 000 risk-neutral scenarios for exactly this reason [R13].

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t`, `m`, `x`, `n`, `T`, `g` | 0-based **policy month** index (`0…T−1`); **month boundary** (`0…T`), `m = 0` at issue; `issue_age`; guarantee maturity in **years**; `T = 12n`, the number of projected months; guarantee level |
| `dur(t)`, `y` | completed policy years `t // 12`; the contractual policy year `dur(t) + 1`. The anniversary is `t ≡ 11 (mod 12)`; `rem(m) = (T − m)/12` is the remaining term in years |
| `P(t)`, `P_net(t)` | gross and net scheduled *versement* at the **beginning of month** `t`, payable only where `t ≡ 0 (mod 12)`; `P_net = P × (1 − f_e)` |
| `P_0`, `P_net,0` | the initial *versement* and its net amount, paid at inception: the **opening state** of the first projected month, not a step in its roll forward |
| `X_open(t)` | the opening value of a state variable: `X(t−1)` in every month but the first projected one, and in that one the state `P_net,0` — or the in-force extract — creates |
| `f_e`, `f_p`, `f_perf`, `f_x` | entry 2.00 %, parts levy 0.80 % p.a., performance levy 10 %, exit 0.00 % |
| `mg(t)` | guaranteed amount payable at `n`, at the close of month `t` |
| `i_pm(m)` | PM discount rate **at month boundary `m`** = 90 % × TEC(`rem(m)`) read on the curve published at year `m // 12`, floored at 0 %. The haircut, the interpolation and the floor are [R3 A. 134-1](#frlib-eurocroissance-r3); reading the index maturity as the **remaining** term, and re-reading it every month, are **[std]**, see (a) above. Month `t` is struck at `i_pm(t+1)` and splits a beginning-of-month *versement* at `i_pm(t)` |
| `A(t)` | `own_assets(t)`, account assets attributable to the policy at the close of month `t`, excluding any outstanding insurer contribution |
| `pm(t)`, `pd(t)` | *provision mathématique*, *provision de diversification* |
| `N(t)`, `u(t)`, `u_min` | `parts(t)`; `part_value(t)` = `pd(t) / N(t)`; minimum part value €5.00 **[std]** |
| `r(t)`, `r_m(t)` | the **annual** gross asset return of the policy year containing month `t`, net of asset management fees; `r_m = (1 + r)^(1/12) − 1` is the return credited in the month |
| `I(t)`, `I_ytd(t)` | the month's financial performance `A_a(t) × r_m(t)`; and the same accumulated since the policy year opened |
| `L(t)`, `F(t)` | parts levy, in the **first month of a policy year**; performance levy, on the **anniversary**, on `I_ytd` |
| `C(t)`, `G(t)`, `D(t)` | `insurer_contribution(t)` (L. 134-3); `pgt(t)` (Chassis B); `pcdd(t)` (fund-level) |
| `q(x+dur(t)+1)`, `w(t)`, `w_p(t)` | the **annual** rates the tables above give: mortality read at the age attained at the anniversary that **closes** the policy year of month `t`; full surrender; partial surrender. `q_m`, `w_m` and `w_pm` are the monthly rates actually applied, `1 − (1 − ·)^(1/12)` |
| `l(t)` | the **end**-of-month in-force count — `pols_if_at(t, "AFT_DECR")` in the model, nil in the last projected month. The model's `pols_if(t)` is the **start**-of-month count — `pols_if(0) = 1` and `pols_if(t) = l(t−1)` thereafter — the weight on month `t`'s flows |

### The guaranteed amount

`mg_open(0) = g × P_net,0` and `mg(t) = mg_open(t) + g × P_net(t) − exits(t)`, where
`exits(t)` runs
the guarantee down pro rata to surrenders and deaths [R13]. In a single-policy expected-value
projection with no partial surrender, `mg(t)` is constant between *versements*.

### Provision mathématique and the split of a *versement* (Chassis A)

`pm` is **re-struck** every month, never accumulated [R2 R. 134-2](#frlib-eurocroissance-r2):

```
pm(t) = mg(t) × (1 + i_pm(t+1))^-rem(t+1)    (Chassis A)
pm(t) = 0                                     (Chassis B)
```

Month `t` closes at boundary `t + 1`, which is `rem(t + 1) = (T − t − 1)/12` years — a
**fractional** number of them in eleven months of twelve — short of the *échéance*, so
that is the horizon the striking discounts over.

A free *versement* paid on the anniversary of policy year `y`, immediately after the
striking at month `t = 12y − 1`, splits as follows and buys parts at the part value just
struck:

```
pm_added = g × P_net × (1 + i_pm(t+1))^-rem(t+1)   pd_added = P_net − pm_added
parts_added = pd_added / u(t)
```

A scheduled *versement* paid at the **beginning** of month `t` splits the same way one
month earlier, at `i_pm(t)` over `rem(t)`, and buys parts at the opening value `u_open(t)`.

In the last projected month, `t = T − 1`, the discount factor is 1, so
`pm(T−1) = mg(T−1)` identically: the *provision
mathématique* accumulated at the regulated rate reaches the guarantee exactly at the
*échéance*, which is what makes the Chassis A guarantee pre-funded by construction.

### Account assets, charges and the monthly re-striking

```
L(t)   = f_p × pd_open(t) × 1{t ≡ 0 mod 12}   (base 4°)   A_a(t) = A_open(t) − L(t)
I(t)   = A_a(t) × r_m(t)        I_ytd(t) = I(t) + I_ytd(t−1) × 1{t ≢ 0 mod 12}
F(t)   = f_perf × max( I_ytd(t), 0 ) × 1{t ≡ 11 mod 12}   (anniversary, base 5°)
A(t)   = A_a(t) + I(t) − F(t)   (before any versement)
N(t)   = N_open(t) × (1 − f_p × 1{t ≡ 0 mod 12})
```

Two of the six R. 134-3 bases keep an annual rhythm inside this monthly recursion, for two
different reasons. `L(t)` falls in the **first month of each policy year** because that is
where `product-spec.md` states it taken, on the opening part value: it is a contract term,
not an assumption, and while `(1 − f_p)^(1/12)` a month would compound back to the same
parts count it would change the **cash** taken, because the levy is valued on the
then-current `pd`. `F(t)` falls **on the anniversary** on the policy year's accumulated
performance because R. 134-3 5° levies on the balance of the participation account and
R. 134-4 strikes that account at least annually [R2]; a monthly levy would tax a positive
month inside a losing year, which the asymmetric `max(·, 0)` exists not to do, and would
have taken money in the worked example's policy year 6. A policy exiting between
anniversaries therefore pays no performance levy for the part year, which is what the
article's annual striking implies.

The two provisions are then re-struck, the diversification provision taking the residual and
stopping at its contractual floor [R2 R. 134-4](#frlib-eurocroissance-r2):

```
pd(t) = max( A(t) − pm(t), N(t) × u_min )   u(t) = pd(t) / N(t)
C(t)  = max( pm(t) + pd(t) − A(t), 0 )
G(t)  = max( mg(t) × (1 + i_pm(t+1))^-rem(t+1) − pd(t) − D(t), 0 )   (Chassis B) [R3 A. 134-2]
```

All four are struck **every month**. In the eleven months of a policy year in which the
participation account is not struck, `pd(t)` and `u(t)` are A. 134-5's *valeur
intermédiaire*; in the twelfth they are the striking of the account itself.

`C(t)` is the outstanding contribution the insurer must make to complete the representation
[R1 L. 134-3](#frlib-eurocroissance-r1); it carries no return to the savers and is repaid in full as soon as `A(t)`
covers `pm(t) + N(t) × u_min` **[std]**, product-spec (6). The **surrender value**
`pm(t) + pd(t)` therefore exceeds `A(t)` by exactly `C(t)` while the contribution is
outstanding. On Chassis B, `pm ≡ 0`, so `pd(t) = max(A(t), N(t) × u_min)` and the shortfall
against the guarantee appears instead as the PGT `G(t)`, which is on the **insurer's** balance
sheet, outside the participation account, and is not part of any benefit.

**The PGT's mortality driver is switched off — [std].** A. 134-2 admits exactly two
cash-flow drivers into the present value of the 2° guarantees: guarantee maturities and
mortality [R3 A. 134-2](#frlib-eurocroissance-r3). `G(t)` above, and `pgt()` in the model,
discount the guaranteed amount to `t` and apply **no survival factor**, so the present value
is the amount for a guarantee certain to be reached. The simplification is prudent — it
overstates the provision — and it is invisible on the worked example, where `mort_rate = 0`;
it is live on every decrement-bearing cell. On shipped model point 6 at the anniversary
closing policy year 7 — month `t` = 83 — the reported
`pgt` is **2,739.35**, against **2,477.36** with the five-year survival factor **0.972660**
that the shipped **[std]** table gives. A fund-level implementation of A. 134-2 should carry
`PV(t) = Σ_i mg_i(t) × (1 + i_pm(t+1))^-rem_i(t+1) × rem_i(t+1) p_(x_i+dur(t)+1)` over the
account's 2°
engagements; in this single-policy model the mortality decrement reaches the projection
through `pols_if` in `result_cf()` instead of through the provision.

### Exit and maturity values

```
surrender_value(t) = ( pm(t) + N(t) × u(t) ) × (1 − f_x)   A ;  ( N(t) × u(t) ) × (1 − f_x)   B
maturity_value(T−1)= pm + N × u at t = T−1                 A ;  max( N × u, mg ) at t = T−1   B
death_value(t)     = pm(t) + N(t) × u(t)                   A ;  N(t) × u(t)                   B
death_payout(t)    = max( death_value(t), cum_prem_net(t) )      if death_floor_flag [S1] [S2]
rider_claim(t)     = death_payout(t) − death_value(t)            outside the account [R2 R. 134-7]
```

Surrender and maturity forms are R. 134-5 and R. 134-6 verbatim [R2]; the death forms follow
from Chapter IV containing no death valuation article [R2] [R13]. A surrender is priced on
the **forward** part value the article requires — the striking of the month in which the
request falls, which is the next striking or intermediate value after it
[R3 A. 134-5](#frlib-eurocroissance-r3). The monthly grid delivers that rather than
standardizing it away: on the worked example's Chassis B a saver surrendering in month 65
receives **11,430.63**, not the 9,899.22 the anniversary striking at month 71 reports.

### Fund-level items (extension, held at zero in the base run)

```
D_open(t)     = D(t−1) + apport(t)                                (PCDD at start of period)
target_use(t) = ( euro_fund_rate(t) + 0.30 % ) × ( pm_open(t) + pd_open(t) ) − Δpm_rate(t)
D_target(t)   = D_open(t) + balance(t) − target_use(t)
D(t)          = max( min( D_open(t), D_target(t) ), 0 )
dotation(t)   = D(t) − D_open(t)
apport(t)     ≤ 0.10 × pd(t)   → credited to D_open(t), never to pd(t)     [R7 R. 134-12]
```

The piloting rule is the *mémoire*'s: run the fund at 30 bp above the insurer's own euro fund
and put everything else in the PCDD [R13]. Note that the first argument of the `min` is the
PCDD at the **start** of the year — last year's close plus the year's *transfert de richesse*
— and not the start-of-year figure plus the participation balance: the `min` is a **cap**
that holds the reserve at its opening level whenever the balance exceeds the target use, and
a version that added the balance inside both arguments would degenerate to
`D_open(t) + balance(t) − max(target_use(t), 0)` and let the PCDD grow without limit [R13].

The PCDD must be used within **fifteen years**
[R9]; the apport must be re-allocated out **no later than the sixteenth year** following
affectation, capped on the way out by the lowest of the affectation-date value plus its share
of net investment income plus the base-5° levies, 10 % of total PD, and total PCDD [R7 II](#frlib-eurocroissance-r7).
**The term "bonus de mutualisation" appears in no retrieved document**; the code calls this
*apport d'actifs* [R7], practitioners *transfert de richesse* [R13] [R21].

### Monthly processing order [std]

The order is not free: R. 134-4 and R. 134-12 III both say that asset affectations and
re-affectations completing the account's representation are made **on the dates the
participation account is struck, after its balance has been allocated** [R2] [R7]. That is
still true, within the anniversary month — the finer grid changes where in the year each
step falls, never the order of the steps that share a date.

The twelve steps below are the steps of **month `t`**, each tagged with the rhythm it
keeps. In the first projected month the opening quantities `A_open`, `pd_open`, `N_open`,
`mg_open` are the state the initial *versement* creates — this is where the issue instant
sits — and in every later month they are the previous month's close.

1. **BOM, annual — first month of the policy year.** Parts levy
   `L(t) = f_p × pd_open(t)` where `t ≡ 0 (mod 12)`, else nil; `N(t) = N_open(t) × (1 − f_p)`
   in that month and `N_open(t)` in the other eleven; assets reduced by `L(t)`
   (base R. 134-3 4°).
2. **BOM, annual assumption spread.** Partial surrenders paid at `w_pm(t)` on the opening
   provisions (base 6° on the way out), and `mg`, `N` and the death-floor base run down pro
   rata.
3. **BOM, annual — first month of the policy year.** Scheduled *versements* received net of
   the entry charge (base 1°) and split per the *versement* rule, at `i_pm(t)` over
   `rem(t)` and at the opening part value.
4. **Over the month.** Asset return `r_m(t) = (1 + r(t))^(1/12) − 1` accrues on the balance
   after steps 1–3: `I(t) = A_a(t) × r_m(t)`.
5. **EOM, monthly.** Accumulate the policy year's performance,
   `I_ytd(t) = I(t) + I_ytd(t−1)` unless `t` opens the policy year.
6. **Anniversary only — performance levy.** `F(t) = f_perf × max(I_ytd(t), 0)` (base 5°),
   nil in the other eleven months.
7. **Anniversary only — strike the participation account** and allocate its balance: raise
   `u` (the reference route), award new parts, revalue the guarantees subject to the two
   A. 134-3 tests, or endow the PCDD [R2 R. 134-4](#frlib-eurocroissance-r2).
8. **EOM, monthly.** Re-strike `pm(t)` from `mg(t)` and the current `i_pm(t+1)` over
   `rem(t+1)`; `pd(t)` = residual, floored at `N(t) × u_min`; `u(t) = pd(t) / N(t)`. In
   eleven months of twelve this is A. 134-5's intermediate value; in the twelfth it is the
   striking of step 7.
9. **Anniversary only — asset affectations:** `C(t)` (Chassis A) or `G(t)` (Chassis B),
   **after** step 7; the *apport d'actifs* endowing the PCDD falls here. (`C(t)` and `G(t)`
   are themselves read off the month's striking and so are reported every month.)
10. **Anniversary only — free *versements*** (the worked example's top-up on the
    anniversary that closes policy year 3, `t` = 35) split at the just-struck `i_pm(t+1)`
    and `u(t)`, and the provisions are re-struck on the post-*versement* state.
11. **EOM, annual assumptions spread.** Claims: deaths at `q_m`, then surrenders at `w_m`,
    each priced on the **month's own** striking — which is the forward value A. 134-5
    requires for a request made within the month — and the maturity in the last projected
    month `t = T − 1`;
    `l(t) = pols_if(t) × (1 − q_m(t)) × (1 − w_m(t))` with `pols_if(0) = 1` and
    `pols_if(t) = l(t−1)` thereafter, survivors maturing at `t = T − 1`, where `l(T−1) = 0`.
12. **EOM, monthly.** Maintenance expense accrues at one twelfth of 0.20 % p.a. on the
    month's own `pm + pd`, weighted by `l(t)`; acquisition costs fall in the month their
    *versement* does.

### Anniversary equivalence

Because `(1 − q_m)^12 = 1 − q` and `(1 − w_m)^12 = 1 − w` exactly, the in-force recursion
collapses over any twelve months of one policy year to
`l(t + 12) = l(t) × (1 − q) × (1 − w)` — the annual-step recursion, term for term — so
`pols_if(12k)` is the count an annual step carried entering policy year `k + 1`. Because
`(1 + r_m)^12 = 1 + r`, and because no cash moves inside a policy year except a *rachat
partiel*, the twelve monthly `I(t)` sum to `A_a × r` and compound the account to
`A_a × (1 + r)`, so the anniversary performance levy `f_perf × max(I_ytd, 0)` is the annual
model's `F(t)` to the cent. And the two contractual placements — the parts levy at the
opening of the policy year, the top-up on the anniversary — put the same cash at the same
instant on both grids.

**Every anniversary value is therefore identical on the two grids, to floating point** —
`A`, `pm`, `pd`, `N`, `u`, `mg`, `cum_prem_net`, `C`, `G`, `D`, `pm + pd`, the surrender,
death and maturity amounts, the A. 134-4 headroom, the A. 134-3 gates, `L` and `F`, each at
`t = 12k + 11` (and `l` at `t = 12k`). Measured against a pre-conversion snapshot of the
annual-step model over all eleven shipped model points, the largest absolute difference is
**1.3 × 10⁻¹⁰ EUR** on figures of order 10,000.

Three things do not agree, and none of them should:

- the **cash flows**, which now fall where they happen rather than at the year end — a
  claim at the end of the month of exit, a *versement* in its own month;
- the **maintenance expense**, which accrues at one twelfth a month on the month's own
  provision and in-force instead of once at the year-end striking. Twelve accruals cover
  exactly the year the annual grid charged once for, so the annual model's extra
  opening-striking charge — it needed `n + 1` point-in-time charges to cover `n` years of
  service — is **dropped**. Over a whole projection the shipped cells carry −0.2 % to
  −1.3 % of it, and model point 9 **+0.9 %**, its five annual *versements* stepping the
  provision up at the opening of each of its first five policy years so that the mid-year
  balances exceed the previous year end;
- on a cell that takes *rachats partiels* — shipped point 5 alone — the **asset-fed**
  values, because `w_pm` spreads the exit cash over twelve months instead of taking it all
  at the opening of the policy year, so more capital earns return early and the withdrawal
  base itself grows within the year. At the anniversaries `A` runs **+0.21 to +3.05 EUR**
  above the annual model, at most **0.031 %**; `u` at maturity is 25.097 against 25.0768,
  **+0.08 %**; total *rachats* over fifteen years are 3,878.27 against 3,869.49,
  **+0.23 %**. What still agrees exactly there is everything whose run-down is purely
  multiplicative — `mg`, `cum_prem_net`, `pm`, `N` and `l` — because `(1 − w_pm)^12 = 1 −
  w_p`. The asymmetry is real and is the price of reading a rate on an *average encours* as
  a continuous drip; an implementation that must have bit-exactness on all eleven points
  can gate `w_pm` to the opening month at the full annual rate, at the cost of the realism.

### Known modeling pitfalls

These are the specific ways an implementation of **this** product can look right and be
wrong. Each should become a test.

1. **Treating the Chassis B surrender value as guaranteed.** The single most important
   product fact. Before the maturity a 2° engagement pays `parts × part value` and **nothing
   else** [R2 R. 134-5](#frlib-eurocroissance-r2); a model that floors the surrender value at `g ×` premiums, or at the
   discounted guarantee, is modelling a contract that does not exist. Test: on the worked
   example's year-6 shock, Chassis B must surrender for **9,899.22**, i.e. **84.18 %** of net
   *versements*, not 11,760.00. (Policy year 6 closes at month `t` = 71.)
2. **Letting the PGT reach a policyholder.** The PGT is the insurer's own-funds provision,
   outside the participation account [R3 A. 134-2](#frlib-eurocroissance-r3) [R13]. A model that adds `pgt` to a
   benefit, or lets it feed the profit-sharing computation, is wrong. Test: `pgt` appears in
   no benefit column and in no participation balance.
3. **Accumulating the PM instead of re-striking it.** `pm(t)` is `mg(t)` discounted at the
   *current* `i_pm(t+1)` [R2 R. 134-2](#frlib-eurocroissance-r2). Rolling `pm(t−1)` forward at last year's rate silently
   removes the **rate effect** — +587.44 of the +824.18 policy-year-6 move (`t` = 59 to
   `t` = 71) in the worked example.
4. **Levying an encours charge on the PD in a 1° account.** R. 134-3 3° permits that levy only
   where the auxiliary account holds **no 1° engagements**, and no base permits a levy on the
   PM [R2]. Test: with `engagement_modality = euro_and_parts`, the recurring charge base must
   be the number of parts and the levy opening policy year 1 — `L(0)` — must be **15.64**,
   not 78.40. The other eleven months of the year carry none of it.
5. **Forgetting that the entry charge cuts the guarantee.** The guarantee is a percentage of
   premiums **net of the R. 134-3 1° charge** [R2 R. 134-2](#frlib-eurocroissance-r2) [R13]. Test: `mg` after the top-up
   on the anniversary of policy year 3, `mg(35)`, is **11,760.00**, not 12,000.00.
6. **Omitting the minimum part value.** A debit balance may reduce the part value only
   **within the limit of its minimum** [R2 R. 134-4](#frlib-eurocroissance-r2). Without the floor, Chassis A's `pd` goes
   negative in policy year 6 (`A(71) − pm(71) = −1,095.35`). Test: `part_value ≥ 5.0000` in
   every month on both chassis. The monthly grid adds *when*: the floor **first binds in
   month 66**, not at the anniversary.
7. **Paying the maturity guarantee to a death claim.** Chapter IV has no death valuation
   article; the death benefit is the current provision value [R2] [R13], and a death floor is
   a complementary guarantee provisioned **outside** the account [R2 R. 134-7](#frlib-eurocroissance-r2). Test: the
   policy-year-6 Chassis B death payout (`t` = 71) with the rider is 11,760.00, of which
   **1,860.78** is a rider
   claim reported outside the auxiliary-account columns.
8. **Applying the maturity `max(·, mg)` before the maturity, or at all on Chassis A.** The
   `max` exists only in the last projected month, `t = T − 1`, and only on Chassis B
   [R2 R. 134-6](#frlib-eurocroissance-r2). On Chassis A the maturity
   amount is `pm + parts × part value` there, **more** than `mg` whenever the parts retain
   any value — 12,765.89 against a guarantee of 11,760.00 here.
9. **Crediting the insurer's contribution to the savers.** `C(t)` completes the representation
   and is releasable when representation permits [R1 L. 134-3](#frlib-eurocroissance-r1); the reference treatment gives
   it no return to the savers **[std]**. A model that rolls the topped-up balance forward as
   savers' assets manufactures return out of the insurer's capital.
10. **Giving per-policy returns inside one auxiliary account.** The part value is **common to
    all engagements of the account** [R2 R. 134-2](#frlib-eurocroissance-r2), so savers with different maturities and
    guarantee levels in one account earn the same rate; differentiation is possible only
    through the number of parts or through differentiated PCDD distribution [R2 R. 134-4](#frlib-eurocroissance-r2)
    [R13]. Test: two model points in the same account share one `part_value` path.
11. **Ignoring the A. 134-3 and A. 134-4 gates.** Revaluing the guarantees out of the
    participation account requires **both** A. 134-3 tests to pass; converting parts into PM
    requires the A. 134-4 15 %-of-PM headroom and a five-year cooling period [R3]. Test: at
    `t = 59` — the anniversary closing policy year 5 — both A. 134-3 tests pass; at
    `t = 71` the second fails (`pd − N × u_min = 0.00` against `10 % × pm = 1,134.60`).
12. **Using the wrong discount article, or a same-day part value.** The PM rate is A. 134-1's
    90 %-of-TEC ceiling with a zero floor [R3] — read here at the remaining maturity, which
    is **[std]** and not the article — not the A. 132-1 maximum technical rate
    [REG-R17] and not the A. 132-3 TMG ceiling [REG-R18]; and the part value used for an
    exit is a **forward** value [R3 A. 134-5](#frlib-eurocroissance-r3), which this model
    now delivers: an exit in month `t` is priced on month `t`'s own striking, never on the
    anniversary before it. Test: the Chassis B surrender in month 65 is **11,430.63**, not
    the 9,899.22 of month 71.
13. **Paying an annual amount twelve times.** The hazard the finer grid creates: an amount
    the contract settles once a year, read by a per-`t` cash-flow cell, is paid in every
    month. Every annual item here is gated — the base 4° levy and the scheduled *versement*
    on `t ≡ 0 (mod 12)`, the base 5° levy, the free *versement* and the *apport d'actifs* on
    `t ≡ 11 (mod 12)`. Test: each is zero in every month the contract does not name.

### Cash flow outputs (per month `t`, probability-weighted by `pols_if`)

`pols_if(t)` below is the **start**-of-month in-force count — the notes' `l(t−1)`, and
`pols_if_init` in the first projected month — and is the
exposure every flow on that same `result_cf()` row is weighted by. The end-of-month count
`l(t)`
is `pols_if_at(t, "AFT_DECR")` in the model; it weights the maintenance expense and nothing else.

| Output | Formula |
|---|---|
| `premiums` | `P(t) × pols_if(t)` in the months that open a policy year, plus the free *versement* on its anniversary, with the initial *versement* `P_0` in the first projected month |
| `claims_death` | `q_m(t) × pols_if(t) × death_payout(t)` — settled at the end of the month of death |
| `claims_lapse` | `w_m(t) × pols_if(t) × (1 − q_m(t)) × surrender_value(t)` — at the month's own striking |
| `claims_maturity` | `pols_if × (1 − q_m) × maturity_value` in the last projected month, `t = T − 1` |
| `withdrawals` | partial *rachats* at `w_pm(t)` — an owner election, not a claim; in every month |
| `expenses` | `pols_if(t) × (`acquisition 5 % of *versements*, plus an acquisition commission of 2 % of the initial *versement* at issue`) + `maintenance **accrued monthly** at `(0.20 % / 12) × (pm(t) + pd(t)) × l(t)` — twelve accruals covering exactly the year the annual grid charged once for at its year-end striking, so **there is no separate opening charge**; all three levels [R13], as in the assumption table above |
| `charges_taken` | `L(t) + F(t) + f_e × P(t) + f_x ×` benefits — insurer income, reported separately; `L` only in the months that open a policy year and `F` only on anniversaries |
| `insurer_contribution` / `pgt` | own-funds items, reported separately, **never** in a claim column |

`result_cf_annual()` sums that frame into policy years — every cash flow column the total
of its twelve months, `pols_if` the count entering the year — so the monthly grid can be
laid beside the annual-step model this one replaced row for row. It is the frame
**regrouped**, not a second projection: `pols_if` and `premiums` agree on it exactly on
every shipped model point, `withdrawals` on every cell that takes no *rachat partiel*, and
`expenses` and the claim columns deliberately do not.

`liability_cf` prints outgo-positive; `net_cf(t) = −liability_cf(t)` is income-positive, and
`result_cf()` is indexed by `t` with `pols_if` first. Because `pols_if` is the
start-of-period
count, `result_cf()["pols_if"].iloc[0]` equals `pols_if_init()` on every model point, and
dividing any flow on a row by that row's `pols_if` recovers the per-policy amount.

The first row carries the initial *versement*, the entry charge on it and the acquisition
commission, **as well as** the first month's own levy, return and striking. That is the
merge of the issue instant into the first month: no row is lost from any total, and the
frame has `12(n − duration_ifo)` rows.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** — no eurocroissance lapse experience is public, and the
product is too small and too young to have any [R14] [R21]. The shapes are rationalized from
the incentive structure the code creates.

- **Base full surrender** 2.5 % p.a. [R13 observes 2 %–3 %](#frlib-eurocroissance-r13); **partial surrender** 6 % of
  average encours in years 1–2 then 3 % [R13 observes 6 % then 2 %–4 %](#frlib-eurocroissance-r13).
  Both are **annual** rates and are spread over their twelve months at `w_m` and `w_pm`.
  Every overlay below is a multiplier on the **annual** rate, applied *before* the monthly
  conversion, so each grades once a year as the behaviour it stands for does and not once a
  month.
- **Guarantee-imminent suppression (Chassis B).** `w(t) = w_base(t) × 0.5` over every month
  of the two policy years before the *échéance* — the years with `n − (dur(t) + 1) ≤ 2`
  still to run — whenever the guarantee is in the money, `N(t) × u(t) < mg(t)`
  **[std]**. The in-the-money test is read on the **month's own** striking, which is what
  the behavioural statement says; on every shipped model point that agrees with the
  anniversary reading in every month, the gate's state being slow-moving relative to a
  month. A saver who surrenders in that state gives up the entire guarantee [R2 R. 134-5](#frlib-eurocroissance-r2)
  — the strongest exit deterrent in the product.
- **Maturity.** 100 % of survivors take the maturity amount in the base run **[std]**, as the
  *mémoire* also assumes; it notes that modelling annuitisation or reinvestment instead could
  amplify or damp its results [R13]. The statutory default is in fact an arbitrage into an
  SRI ≤ 2 support unless the holder decides otherwise [R2 R. 134-6](#frlib-eurocroissance-r2) [R3 A. 134-6](#frlib-eurocroissance-r3), so a "roll
  into a low-risk support" variant is the natural extension.
- **Duration-8 tax spike.** The assurance-vie annual abattement (€4 600 / €9 200) becomes
  available at eight years [REG-R40], so the rate of **policy year 8** — the months
  `t = 84 … 95` on a new-business cell, `dur(t) + 1 = 8` — is `w_base × 1.5` **[std]** where
  `n > 8`.
- **Lock-up, and the last policy year.** Where `lock_up_years > 0`, `w(t) = w_p(t) = 0` for
  `dur(t) < lock_up_years` — policy years 1 to `lock_up_years` — except for the
  L. 132-23 hardship exits, which are not separately modeled **[std]** [R1] [R2 R. 134-5](#frlib-eurocroissance-r2).
  Both rates are likewise nil over the **whole of the last policy year**,
  `dur(t) ≥ n − 1`, where the survivors take the maturity amount instead. Both exclusions
  are read on `dur(t)` and not on the month: stating the second as "the last month" would
  open eleven months the annual grid closed and move the whole maturity claim.
  The thirty-day *renonciation* right [REG-R29] is now expressible on this grid and is
  nonetheless still **out of scope** — it is a cancellation of the contract *ab initio*
  rather than a decrement, and no retrieved document gives its take-up.
- **No surrender-penalty deterrent** is modeled, because the reference indemnity is zero
  [S2] [S8]; the *mémoire*'s point that the loss of the PCDD share is itself the penalty [R13]
  bites only where the PCDD extension is switched on. Any mass-surrender stress must respect
  the HCSF power to limit surrender payments for up to six consecutive months [REG-R13].

---

## Worked example

**Configuration.** One model point per chassis, same asset path, two separate auxiliary
accounts. Gross initial *versement* **€10 000.00** at inception and a free additional *versement*
of **€2 000.00** on the anniversary that closes policy year 3 — month `t` = 35 — [R13]; entry charge **2.00 %** [R13], so net
*versements* are 9 800.00 and 1 960.00 and cumulative net *versements* are **11 760.00**;
guarantee level `g` = **100 %** of net *versements* at a maturity `n` = **10 years**
[S1] [S2]; initial part value **€10.0000** [R13]; minimum part value **€5.0000** **[std]**;
parts levy **0.80 % p.a.** and performance levy **10 % of positive financial performance**
[R13]; exit charge and surrender indemnity **0 %** [S2] [S8]; male age 57 [R13].
`mort_rate = 0` and `lapse_rate = 0` throughout, so `pols_if(t) = 1` and the per-policy
provision path is the cash-flow path **[std]**. The **annual** gross asset return `r(t)` is
4.00 % over policy years 1–5 (months `t` = 0–59), **−25.00 %** over policy year 6
(`t` = 60–71) and 6.00 % after; the monthly returns the recursion applies are
`1.04^(1/12) − 1` = **0.327374 %**, `0.75^(1/12) − 1` = **−2.368842 %** and
`1.06^(1/12) − 1` = **0.486755 %**, and twelve of each compound back to 4.00 %, −25.00 %
and 6.00 % exactly. TEC10 = 2.50 % on the curves published at years 0–5 and
**1.00 %** from year 6 at every maturity, so the A. 134-1 discount rate `i_pm` = 90 % × TEC = **2.25 %** then
**0.90 %** [R3] **[std]**. The policy-year-6 double shock — equities down and rates down together —
is what makes the rebalancing visible.

The frame is **120 monthly rows**. The two tables below print its **anniversary** rows,
`t = 11, 23, … , 119` — row `t = 12y − 1` is the close of policy year `y`, and is the row
the annual-step model this one replaced carried for the same policy year. **Every number
in them is unchanged by the change of grid**; only the index moved. A third table then
prints the twelve months of policy year 6, which is what the annual grid could not report
at all. Each of the first two also has an *opening* line that is **not** a row of the
frame: it is the state the initial *versement* creates, which the model reaches as
`own_assets_at(0, "BOM")` and its siblings.

### Chassis A (1° engagement: euros and parts)

`L` is `0.80 % × pd_open` taken in the **opening** month of the policy year, `t = 12(y−1)`;
`pm(t) = mg(t) × (1 + i_pm(t+1))^-rem(t+1)`; `pd(t) = max(A(t) − pm(t), parts(t) × 5.00)`.
The `r(t)` column is the policy year's **annual** return; the account compounds at
`r_m = (1 + r)^(1/12) − 1` twelve times over, which lands on the same anniversary balance.

| t | policy year | r(t) | parts levy (at `t − 11`) | own assets `A` | `pm` | `pd` | parts | part value | insurer contrib. | surrender value |
|---|---|---|---|---|---|---|---|---|---|---|
| *opening* | — | — | 0.00 | 9,800.00 | 7,845.00 | 1,955.00 | 195.5001 | 10.0000 | 0.00 | 9,800.00 |
| 11 | 1 | 4.00 % | 15.64 | 10,136.60 | 8,021.51 | 2,115.09 | 193.9361 | 10.9061 | 0.00 | 10,136.60 |
| 23 | 2 | 4.00 % | 16.92 | 10,483.98 | 8,202.00 | 2,281.99 | 192.3846 | 11.8616 | 0.00 | 10,483.98 |
| 35 | 3 | 4.00 % | 18.26 | 12,802.49 | 10,063.85 | 2,738.65 | 212.8127 | 12.8688 | 0.00 | 12,802.49 |
| 47 | 4 | 4.00 % | 21.91 | 13,240.69 | 10,290.29 | 2,950.40 | 211.1102 | 13.9756 | 0.00 | 13,240.69 |
| 59 | 5 | 4.00 % | 23.60 | 13,692.90 | 10,521.82 | 3,171.08 | 209.4213 | 15.1421 | 0.00 | 13,692.90 |
| 71 | 6 | −25.00 % | 25.37 | 10,250.65 | 11,346.00 | 1,038.73 | 207.7460 | **5.0000** | 2,134.08 | 12,384.73 |
| 83 | 7 | 6.00 % | 8.31 | 10,795.42 | 11,448.11 | 1,030.42 | 206.0840 | 5.0000 | 1,683.11 | 12,478.53 |
| 95 | 8 | 6.00 % | 8.24 | 11,369.69 | 11,551.14 | 1,022.18 | 204.4353 | 5.0000 | 1,203.63 | 12,573.32 |
| 107 | 9 | 6.00 % | 8.18 | 11,975.03 | 11,655.10 | 1,014.00 | 202.7998 | 5.0000 | 694.07 | 12,669.10 |
| 119 | 10 | 6.00 % | 8.11 | 12,613.13 | **11,760.00** | 1,005.89 | 201.1774 | 5.0000 | 152.75 | **12,765.89** |

The `t` = 35 row is stated **after** the anniversary *versement*. Immediately before it,
`A = 10,842.49`, `pm = 8,386.54`, `pd = 2,455.95`, `parts = 190.8455`, `u = 12.8688`; the
*versement* then splits as `pm_added = 1 960.00 × 1.0225^-7 = 1,677.31`, `pd_added = 282.69`
and `parts_added = 282.69 / 12.8688 = 21.9672`, and `mg` rises from 9,800.00 to **11,760.00**.
Performance levies are 39.14, 40.48, 41.86, 51.12, 52.87, 0.00, 61.45, 64.72, 68.17, 71.80,
each taken on the anniversary `t` = 11, 23, … , 119 on that policy year's accumulated
performance; the parts levies in the column above are taken twelve months earlier, at
`t` = 0, 12, … , 108.

### Chassis B (2° engagement: parts only, guarantee at maturity)

`pm ≡ 0`, so `pd(t) = max(A(t), parts(t) × 5.00)` and the shortfall shows as the PGT.

| t | policy year | parts levy (at `t − 11`) | `pd` = own assets | parts | part value | `pgt` (own funds) |
|---|---|---|---|---|---|---|
| *opening* | — | 0.00 | 9,800.00 | 980.0000 | 10.0000 | 0.00 |
| 11 | 1 | 78.40 | 10,071.58 | 972.1600 | 10.3600 | 0.00 |
| 23 | 2 | 80.57 | 10,350.68 | 964.3827 | 10.7330 | 0.00 |
| 35 | 3 | 82.81 | 12,597.52 | 1,132.9370 | 11.1193 | 0.00 |
| 47 | 4 | 100.78 | 12,946.62 | 1,123.8735 | 11.5196 | 0.00 |
| 59 | 5 | 103.57 | 13,305.40 | 1,114.8825 | 11.9344 | 0.00 |
| 71 | 6 | 106.44 | **9,899.22** | 1,105.9635 | **8.9508** | **1,446.78** |
| 83 | 7 | 79.19 | 10,350.30 | 1,097.1158 | 9.4341 | 1,097.81 |
| 95 | 8 | 82.80 | 10,821.95 | 1,088.3388 | 9.9435 | 729.20 |
| 107 | 9 | 86.58 | 11,315.08 | 1,079.6321 | 10.4805 | 340.02 |
| 119 | 10 | 90.52 | **11,830.69** | 1,070.9951 | 11.0464 | 0.00 |

Again the `t` = 35 row is post-*versement*: immediately before it `pd = 10,637.52`,
`parts = 956.6677` and `u = 11.1193`, and the whole net 1 960.00 buys
`1 960.00 / 11.1193 = 176.2694` parts. Performance levies are 38.89, 39.96, 41.07, 49.99,
51.37, 0.00, 58.92, 61.61, 64.41, 67.35 on the anniversaries `t` = 11, 23, … , 119.

### What the monthly grid inserts: the twelve months of policy year 6

The two tables above are the anniversary rows, and the annual grid could print those. What
it could not print is what happens *inside* the year the shock falls in, `t` = 60 … 71 —
and on this product that is where the interesting month is. Every figure below is the
month's own striking, which is the value A. 134-5 requires an exit in that month to be
priced on.

| t | own assets `A` | `pm` | `pd` | part value | surrender value | `C` |
|---|---|---|---|---|---|---|
| 60 | 13,343.77 | 10,541.34 | 2,802.42 | 13.4897 | 13,343.77 | 0.00 |
| 63 | 12,417.78 | 10,600.15 | 1,817.63 | 8.7493 | 12,417.78 | 0.00 |
| 65 | 11,836.43 | 10,639.53 | 1,196.90 | 5.7614 | 11,836.43 | 0.00 |
| **66** | 11,556.04 | 10,659.28 | **1,038.73** | **5.0000** | 11,698.00 | **141.96** |
| 70 | 10,499.36 | 10,738.63 | 1,038.73 | 5.0000 | 11,777.36 | 1,278.00 |
| **71** | 10,250.65 | **11,346.00** | 1,038.73 | 5.0000 | **12,384.73** | **2,134.08** |

Three facts the annual grid could not state. The **part-value floor first binds in month
66**, not at the anniversary — `u` falls 13.4897 → 8.7493 → 5.7614 and then stops. The
**L. 134-3 contribution starts at 141.96 in month 66** and climbs to 2,134.08 by month 71,
rather than arriving whole at the year end. And the `pm` move splits cleanly in two: it
accretes from 10,541.34 to 10,738.63 over eleven months at the unchanged 2.25 % — the
**time effect** — and jumps to 11,346.00 in the twelfth, where the TEC curve is re-published
at 1.00 % — the **rate effect**, +607.37 in one month. The year-on-year +236.74 / +587.44
decomposition below is unchanged; the monthly grid says *when* each half happens.

On Chassis B over the same months, `pd` slides from 12,886.29 (month 60) to 9,899.22 (month
71) and the **PGT first becomes positive in month 68**, at 61.48, reaching 1,446.78 at the
anniversary:

| t | `pd` = own assets | part value | `pgt` | surrender value |
|---|---|---|---|---|
| 60 | 12,886.29 | 11.6516 | 0.00 | 12,886.29 |
| 65 | 11,430.63 | 10.3355 | 0.00 | **11,430.63** |
| **68** | 10,637.40 | 9.6182 | **61.48** | 10,637.40 |
| 71 | 9,899.22 | 8.9508 | 1,446.78 | 9,899.22 |

A saver who surrendered in month 65 would have received **11,430.63**, not the 9,899.22 the
annual grid reported for the year — the clearest possible demonstration that A. 134-5's
*forward* part value is a real number and not a rounding of the anniversary's.

### Exit values, and what the two chassis pay

| Event | Chassis A | Chassis B |
|---|---|---|
| Surrender at `t` = 71 (anniversary of policy year 6) | 12,384.73 (**105.31 %** of net *versements*) | 9,899.22 (**84.18 %**) |
| Surrender at `t` = 65 (mid-year, A. 134-5 intermediate value) | 11,836.43 | **11,430.63** |
| Death at `t` = 71, no rider | 12,384.73 | 9,899.22 |
| Death at `t` = 71 with the *garantie décès plancher* | 12,384.73 (rider claim 0.00) | 11,760.00 (rider claim **1,860.78**, outside the account) |
| Maturity at `t` = 119 (the *échéance*) | 12,765.89 = 11,760.00 + 1,005.89 | 11,830.69 = `max(11,830.69, 11,760.00)` |
| Guarantee binding at maturity? | yes, by construction (`pm(119) = mg`) | no — the account recovered to 0.60 % above `mg` |
| Insurer's own-funds cost, peak at an anniversary | contribution **2,134.08** at `t` = 71 | PGT **1,446.78** at `t` = 71 |
| Insurer's own-funds cost, peak over all months | contribution 2,134.08 at `t` = 71 | PGT **1,486.65** at `t` = 72 — one month into policy year 7, and above every anniversary figure |
| Social-levy base at maturity [R11] | 12,765.89 − 12,000.00 = **765.89** | 11,830.69 − 12,000.00 < 0, i.e. **nil** |

The social-levy base is the surrender value at the moment the guarantee is reached less the
premiums allocated to those engagements [R11 CSS L. 136-7 II 3° b)](#frlib-eurocroissance-r11); whether "primes versées"
means gross or net of the entry charge was not resolved from the retrieved text, so the table
uses **gross** premiums (12,000.00) and the alternative net figures are 1,005.89 and 70.69
respectively — **[unverified]**.

**Checks.** *(i)* The PM unwinds exactly onto the guarantee: `pm(119) = 11,760.00 ×
1.009^0 = 11,760.00 = mg(119)`, and the Chassis A maturity payout is that plus the parts at
their floor,
`201.1774 × 5.0000 = 1,005.89`, giving 12,765.89 — reproduced independently of the asset
path. *(ii)* The policy-year-6 PM move decomposes cleanly into its two drivers: at the
unchanged
2.25 % rate `pm(71)` would have been `11,760.00 × 1.0225^-4 = 10,758.56`, a **time effect of
+236.74** on `pm(59) = 10,521.82`; re-striking at 0.90 % gives `11,760.00 × 1.009^-4 =
11,346.00`, a **rate effect of +587.44**; the two sum to +824.18, which is exactly
`11,346.00 − 10,521.82`. On the monthly grid the time effect is visible as it accrues,
`pm(60) = 10,541.34` through `pm(70) = 10,738.63`, and the rate effect lands whole in month
71. *(iii)* The policy-year-6 asset roll is `A(71) = (13,692.90 − 25.37) ×
(1 − 0.25) = 10,250.65` — twelve months at `0.75^(1/12) − 1` compounding to exactly
`1 − 0.25` — with no performance levy, because the policy year's accumulated financial
performance was negative; `pd(71)` would have been `10,250.65 − 11,346.00 = −1,095.35`
without the floor, so
the floor binds at `207.7460 × 5.0000 = 1,038.73` and the insurer's contribution is
`11,346.00 + 1,038.73 − 10,250.65 = 2,134.08`. *(iv)* The parts count closes:
`212.8127 × 0.992^7 = 201.1774` on Chassis A and `1,132.9370 × 0.992^7 = 1,070.9951` on
Chassis B — seven levies, one at the opening of each of the last seven policy years, and
nothing in the other eighty-four months. *(v)* The A. 134-3 gates behave as expected: at
`t` = 59, `pd = 3,171.08 >
1.5 × (11,760.00 − 10,521.82) = 1,857.27` and `pd − N × u_min = 2,123.98 > 10 % × pm =
1,052.18`, so revaluing the guarantees is permitted; at `t` = 71 the second test fails,
`0.00 ≤ 1,134.60`. *(vi)* The A. 134-4 conversion headroom at `t` = 59 is the `C` solving
`pd − C − N × u_min = 15 % × (pm + C)`, i.e. **474.52**, on which the 0.50 % *frais de
conversion* [S8] would be 2.37. *(vii)* The rate conversions themselves:
`1.04^(1/12) − 1 = 0.00327374` and twelve of them compound to 4.00 % exactly; on the
decrement-bearing cells `1 − (1 − 0.00243005)^(1/12) = 0.00020273` compounds back to
0.00243005, and `1 − (1 − 0.06)^(1/12) = 0.00514301` back to 6.00 %.

**Two sensitivities worth stating in numbers.** At `g` = 80 % — Generali's published level
[S8] — the same path leaves `pm(71) = 9,076.80` and cuts the policy-year-6 Chassis A
contribution
from 2,134.08 to **829.17**, a 61 % reduction in the insurer's own-funds cost, which is why
the guarantee level and not the charge scale is the product's real dial. And on Chassis B, an
*apport d'actifs* of the statutory maximum **10 % of the PD** at `t` = 71 — 989.92, credited to
the PCDD, not to the savers' PD [R7 R. 134-12](#frlib-eurocroissance-r7) — would reduce the PGT from 1,446.78 to
**456.86** without changing any policyholder value by one cent.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers are cited,
not reproduced.

- **French statutory balance sheet.** Inside the auxiliary account only R. 343-3 items 1°, 4°,
  7°, 9°, 10° and 11° are admitted [R2 R. 134-9](#frlib-eurocroissance-r2) [R8] [REG-R6]. Assets are at realisation value
  [R2 R. 134-8](#frlib-eurocroissance-r2), so the *provision pour risque d'exigibilité* [REG-R7] and the *réserve de
  capitalisation* have no role inside it, and the technical result is volatile by construction
  [R13]. The PGT is computed **per auxiliary account**, on the A. 132-18 tables [R10] at a rate
  at most 90 % of the TEC at the account's 2°-engagement duration, counting **no cash flows
  other than guarantee maturities and mortality** [R3 A. 134-2](#frlib-eurocroissance-r3) — a deliberately narrow basis a
  model must not "improve" by adding lapses or expenses. The shipped per-policy `pgt` narrows
  it further, omitting the survival factor on the second of those two drivers **[std]**; see
  "The PGT's mortality driver is switched off" above.
- **Solvabilité II.** Technical provisions are best estimate plus risk margin [REG-R1]
  [REG-R2], discounted on the EIOPA risk-free term structures [REG-R5]; no numeric curve is
  reproduced here and any flat discount rate in this library is **[std]**. Future discretionary
  benefits — the part-value uplift the participation account can deliver — belong in the best
  estimate; the maturity guarantee is an option whose cost needs a stochastic market-consistent
  valuation, which is why the *mémoire* runs 1 000 scenarios [R13]. In the worked example that
  guarantee costs the insurer 2,134.08 (Chassis A) or 1,446.78 (Chassis B) on **one** scenario;
  its cost is convex in the asset shock and in the level of rates, so a deterministic run
  understates it.
- **IFRS 17 and professional standards.** Eurocroissance is an archetypal direct-participating
  contract, so the variable fee approach is the expected measurement model; its mechanics were
  not read from a retrieved text and are [unverified] [REG-R45], and the fulfilment cash flows
  are this same projection. NPA 2, *Modèles actuariels*, is the standard this documentation,
  worked example and test suite sit under [REG-R44].

---

## Key sensitivities and model risks

1. **The guarantee level `g`.** It sets how much of the account is locked into the guaranteed
   leg and therefore how much can bear risk. At `g` = 100 % and `i_pm` = 2.25 %, the PM is
   **80.1 %** of the initial net *versement*; at `g` = 80 % it is 64.0 %. This is the single
   largest dial and the sharpest observed difference across insurers [S1] [S8].
2. **The level of the TEC.** `i_pm` is 90 % of it [R3 A. 134-1](#frlib-eurocroissance-r3), and a 150 bp fall adds
   587.44 to `pm(71)` — the anniversary closing policy year 6 — in the worked example, more
   than twice the time effect, and all of it in the single month the curve is re-published.
   A model with a
   flat TEC assumption is not modelling this product's dominant risk.
3. **The minimum part value.** Nowhere published for any insurer [R2 R. 134-1](#frlib-eurocroissance-r2); it sets the
   floor of the diversification provision and therefore both the Chassis A maturity payout
   (12,765.89 against a bare guarantee of 11,760.00) and the point at which the insurer must
   start contributing assets. A pure **[std]**.
4. **Asset allocation and the shape of the shock.** The *mémoire* covers the guarantee with
   zero-coupon OATs to the maturity and puts the remainder in equities [R13]; the shape of the
   shock, not just its size, drives the result, because the two provisions respond to
   different risk factors.
5. **The PCDD piloting rule.** Discretionary, unpublished, bounded only by the fifteen-year
   release horizon [R9], and the biggest driver of the credited return [R13]. Held at zero
   here, which understates the smoothing the real product delivers.
6. **Charge structure and its legal base.** The permitted bases differ by chassis
   [R2 R. 134-3](#frlib-eurocroissance-r2), so the same economic charge cannot always be levied the same way; the levels
   are **[std]** because no statutory ceiling on any French life charge appears in the
   retrieved texts [REG-R30].
7. **Unanchored decrements.** No eurocroissance lapse experience is public, so the
   guarantee-imminent suppression and the duration-8 spike are **[std]** shapes; the mortality
   table is an INSEE-based **[std]** proxy [REG-R24], the regulatory tables being cited but
   never shipped [REG-R21] [REG-R22] [REG-R23] and A. 132-18 permitting certified insurer
   tables [R10].
8. **Single-policy abstraction.** The part value, the PCDD, the PGT and
   the *apport d'actifs* are all **account-level** quantities [R2 R. 134-2](#frlib-eurocroissance-r2) [R3 A. 134-2](#frlib-eurocroissance-r3) [R7],
   which a per-policy model can only approximate — and the *mémoire* records that pooling two
   maturity cohorts in one account produces **no** mutualisation benefit [R13]. The code's
   requirement of an intermediate valuation at least monthly and of a forward part value for
   exits [R3 A. 134-5](#frlib-eurocroissance-r3) is now **honoured** by the monthly grid;
   what remains an abstraction is the account-level nature of these four quantities.
9. **Data-provenance limits.** No contractual document exists in the source set [S10], the
   end-2025 market size is not published [R16], ACPR excludes the product from its weekly flows
   [R18], and the A. 134-7 return that would settle every parameter goes to the regulator
   unpublished [R3]. A calibration pass against a real *notice d'information* is required
   before any quantitative use.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-eurocroissance-r1
[R10]: #frlib-eurocroissance-r10
[R11]: #frlib-eurocroissance-r11
[R13]: #frlib-eurocroissance-r13
[R14]: #frlib-eurocroissance-r14
[R16]: #frlib-eurocroissance-r16
[R18]: #frlib-eurocroissance-r18
[R2]: #frlib-eurocroissance-r2
[R21]: #frlib-eurocroissance-r21
[R3]: #frlib-eurocroissance-r3
[R7]: #frlib-eurocroissance-r7
[R8]: #frlib-eurocroissance-r8
[R9]: #frlib-eurocroissance-r9
[REG-R1]: #frlib-reg-r1
[REG-R13]: #frlib-reg-r13
[REG-R17]: #frlib-reg-r17
[REG-R18]: #frlib-reg-r18
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R40]: #frlib-reg-r40
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[REG-R7]: #frlib-reg-r7
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
