# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify a reference liability cash-flow projection model — model
name **`TD_FR_S`**, **monthly** grid — for the standardized composite French *assurance
temporaire décès* defined in `product-spec.md` (same directory). This is not any single
insurer's product. [S#]/[R#] tags refer to the source list in `sources.md` (numbering carried
from `_research/temporaire-deces.md`; frozen); [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own R-numbering).
**[std]** marks standardizations introduced for the reference implementation; [unverified]
marks claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`. Cells names, model-point columns and CSV headers are English
`lower_snake_case`; French terms of art keep their French form in prose.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — cotisations, death claims,
  PTIA claims, expenses and commission — for a single-policy model point, on an expected
  (probability-weighted) basis. Discounting, the *provision mathématique* recursion, the
  Solvabilité II risk margin and the capital layers are out of scope (see Valuation and reserve
  pointers).
- **Projection frequency [std]: monthly.** Monthly steps (monthiversary processing) are the
  model. **A monthly grid is not a monthly product.** Every *contractual* element here is on an
  annual cycle — the one-year cover renewed by *tacite reconduction* and repriced at each
  renewal [S1] [S2] [S3] [S6] [S8] [S9], the benefit schedule, the art. L. 132-7 suicide year,
  the first-year commission rate, the `constante` equivalence — and the model keeps every one of
  them on the anniversary. What the finer grid adds is the timing of everything that is *not*
  contractually annual: the modal cotisation collected on the cycle the disclosed
  *frais de fractionnement* and *frais d'échéance* exist to price, claims settled in the month
  of claim, and maintenance expense accruing where it is incurred. An annual step remains a
  well-defined special case of the recursion below and reproduces its in-force and every
  annual contractual quantity at every anniversary exactly — see *Annual equivalence* — but it is
  not what the reference model runs.
- **Time index [library-wide].** `t` is **0-based** and counts **policy months**, as in
  lifelib's `basiclife/BasicTerm_S` and the other monthly models of this library: `t = 0` is the
  first policy month, month `t` runs from time `t` to time `t + 1`, and `proj_len` is the
  **number** of projected months — the exclusive end of the frame — so the projection runs
  `t = 0 … proj_len − 1` and `result_cf()` has `proj_len` rows. Because every contractual
  schedule is annual, the policy year is **derived** and used as a lookup key: `dur(t) = t // 12`
  is the completed policy years at the start of month `t`, the contractual **policy year** is the
  1-based label `policy_year(t) = dur(t) + 1`, and the attained age is `x(t) = issue_age + dur(t)`.
  The **anniversary** that opens policy year `k` is month `t = 12(k − 1)`, and where these notes
  say "policy year k" as contract language the months are `t = 12(k − 1) … 12k − 1`. Nothing is
  indexed by the policy year.
- **Projection horizon.** `n = proj_len_y = cover_end_age − issue_age` is the horizon in
  **policy years**, which is how the contract states it, and `proj_len = 12n` is the frame in
  months. Month `t` falls in the policy year at attained age `issue_age + dur(t)`, so the last
  covered policy year is the one at attained age `cover_end_age − 1`. For the worked
  configuration, `n = 75 − 58 = 17` and `proj_len = 12 × 17 = 204`, i.e. `t = 0 … 203`, the last
  covered policy year being months 192–203 at attained age 74.
- **Timing conventions [std].** Monthiversary (BOM) processing. The cotisation instalment at
  the **beginning** of each month the elected *fractionnement* makes it due — annual in advance
  is the contracts' base mode [S1] [S2] [S6] [S7] [S8] [S9] and collects in the first month of
  each policy year; maintenance expense and commission at the beginning of the month; death and
  PTIA claims at the **end of the month of claim**, not of the policy year; lapses at the end of
  the month, **after** both insured decrements; acquisition expense and the initial commission
  rate at issue. Decrement rates are quoted **annual effective** throughout and subscripted `m`
  where the monthly rate actually applied is meant.
- **Age basis.** *Différence de millésime* — calendar year minus year of birth, irrespective of
  birth month [S1] [S2] [S6] [S7]. The age steps at the **policy anniversary**,
  `x(t) = issue_age + dur(t)`, and **not monthly**: the finer grid does not make the age basis
  finer, and every tariff and cover-limit lookup is therefore flat across a policy year. The real
  millésime age steps on 1 January, so an implementation on real dates carries a fractional
  offset of at most one year **[std]**.
- **Termination.** All states terminate at the end of month `t = proj_len − 1`: cover ceases at
  the age limit, nothing is payable, there is no maturity value and no conversion
  [S3] [S5] [S11] [S15] [S16]. `pols_if(proj_len)` is never a weight on a cash flow, but it is
  **not** unused: it is the survivor term of the closure identity below, and it is what the
  lapse rate in the final projected policy **year** — zero, by the convention set out under
  *Lapse* — decides.
- **No cash value anywhere.** Art. L. 132-23 forbids both *rachat* and *réduction* on a
  temporaire décès [R3]. The model has **no account value, no surrender cells, no paid-up
  state**, and `claims_lapse(t)` is structurally zero at every `t`.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive**
  (cotisations +, claims and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to
  euro cents **[std]**.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 |
| `premium_form` | enum {revisable, constante} | revisable |
| `benefit_shape` | enum {constant, decreasing} | constant |
| `benefit_schedule_id` | str (key into `benefit_schedule.csv`) | constant |
| `sex` | enum {M, F} — reporting only; pricing is unisex [R10] | M |
| `smoker` | enum {N, S} — feeds `rating_factor`, no published level | N |
| `issue_age` | int (*différence de millésime*) | 58 |
| `sum_assured` | EUR | 150,000 |
| `cover_end_age` | int (death cover ceases at this attained age) | 75 |
| `ptia_end_age` | int (PTIA cover ceases at this attained age) | 65 |
| `premium_rate_id` | str (key into `premium_rate_table.csv`) | maif_2019 |
| `rating_factor` | float (*surprime* multiplier on the tariff rate) | 1.00 |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | annual |
| `level_premium` | EUR; 0 = derive by equivalence (`constante` form only) | 0 |
| `waiting_period_y` | int (*délai d'attente*, years) | 0 |
| `accident_multiplier` | float (additional accidental capital, 1.00 = option off) | 1.00 |
| `issue_date` | date | — |

`premium_form` is the column a UK or US reader is most likely to get wrong, and it is the
first entry in Known modeling pitfalls. `sex` is carried but **must not** enter pricing:
art. L. 111-7 forbids sex-based premium and benefit differences for contracts written from
21 December 2012 [R10], while the homologated valuation tables remain sex-specific
[R6] [REG-R22] — the same tension `products/rente_viagere/` faces from the other side.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len_y` | Number of projected policy **years** = `cover_end_age − issue_age` | once per model point |
| `proj_len` | Number of projected **months** = `12 × proj_len_y`; the frame is `t = 0 … proj_len − 1` | once per model point |
| `duration_mth(t)` | Completed policy months at the start of month t = `t` | derived |
| `duration(t)` | Completed policy years at the start of month t = `t // 12` | derived |
| `policy_year(t)` | Contractual 1-based policy-year label = `duration(t) + 1` | derived |
| `age(t)` | Attained age of month t's policy year = `issue_age + duration(t)` | annual, on the anniversary |
| `pols_if(t)` | In-force probability at the start of month t; `pols_if(0) = 1` | monthly recursion |
| `prem_rate(t)` | Tariff rate at `age(t)`, read from `premium_rate_table.csv` | annual, on the anniversary |
| `prem_freq_load(t)` | Fractionation multiplier for `prem_freq`, from `freq_loading_table.csv` | lookup |
| `prem_instalments()` | Instalments per policy year for `prem_freq`, from the same file | lookup |
| `prem_cycle()` | Months between instalments = `12 / prem_instalments()` | once per model point |
| `prem_pp(t)` | **Annual** cotisation per in-force policy for month t's policy year | annual, on the anniversary |
| `prem_inst_pp(t)` | Instalment collected at BOM = `prem_pp(t) / prem_instalments()` in a due month, else 0 | monthly |
| `benefit_pp(t)` | Capital payable on a month-t death or PTIA claim | annual, on the anniversary (schedule) |
| `mort_rate(t)` | **Annual** dependent rate of the death decrement at `age(t)` | annual, on the anniversary |
| `ptia_rate(t)` | **Annual** dependent rate of the PTIA decrement; **0** once `age(t) ≥ ptia_end_age` | annual, on the anniversary |
| `decr_rate(t)` | The combined annual insured decrement `mort_rate(t) + ptia_rate(t)` | annual, on the anniversary |
| `decr_rate_mth(t)` | `1 − (1 − decr_rate(t))^(1/12)`, the monthly insured decrement applied | monthly |
| `mort_rate_mth(t)` | `decr_rate_mth(t) × mort_rate(t) / decr_rate(t)`, the monthly death rate applied | monthly |
| `ptia_rate_mth(t)` | `decr_rate_mth(t) × ptia_rate(t) / decr_rate(t)`, the monthly PTIA rate applied | monthly |
| `lapse_rate(t)` | **Annual** lapse rate of month t's policy year; **0** through the final policy year | annual, on the anniversary |
| `lapse_rate_mth(t)` | `1 − (1 − lapse_rate(t))^(1/12)`, applied at EOM after the insured decrements | monthly |
| `suicide_factor(t)` | Death-benefit exclusion factor; < 1 through policy year 1 only, never applied to PTIA | annual, on the anniversary |
| `pols_death(t)` | Expected deaths in month t = `pols_if(t) × mort_rate_mth(t)` | monthly |
| `pols_ptia(t)` | Expected PTIA claims in month t = `pols_if(t) × ptia_rate_mth(t)` | monthly |
| `pols_lapse(t)` | Expected lapses in month t, on survivors of both decrements | monthly |
| `premiums(t)` | `prem_inst_pp(t) × pols_if(t)` | monthly |
| `claims_death(t)` | `benefit_pp(t) × pols_death(t) × suicide_factor(t)` | monthly |
| `claims_ptia(t)` | `benefit_pp(t) × pols_ptia(t)` | monthly |
| `claims_lapse(t)` | **Structurally 0** — a lapse pays nothing [R3] | monthly |
| `expenses(t)` | Acquisition + one twelfth of maintenance + claim expense + commission | monthly |
| `net_cf(t)` | Net liability cash flow, income-positive | monthly |

There is **no** account-value state variable, **no** surrender-value state variable and **no**
paid-up state. That is a statutory fact about the product, not a modeling simplification
[R3] [S7] [S9].

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Cotisation rule | `sum_assured × prem_rate(age(t)) × rating_factor × prem_freq_load`, **plus the fixed *frais d'échéance* once a year** where the mode is fractionated | [S1] [S2] [S3] [S4] [S6] [S7] [S9]; fee [S1] |
| Tariff rate table | The published attained-age grid below, ages 18–74 | [S3] |
| Repricing | At the effective date and again at **every annual renewal**, on attained age | [S1] [S2] [S3] [S4] [S6] [S7] [S9] [S10] |
| Death benefit | `sum_assured`, constant, from any cause | [S1] [S2] [S3] [S6] [S7] [S9] |
| PTIA benefit | The **same** capital, paid early to the insured; payment ends the contract | [S1] [S2] [S3] [S6] [S8] |
| Death/PTIA cumulation | Prohibited; the PTIA capital is due only if the insured is alive at payment | [S1] [S2] |
| PTIA cessation | At `ptia_end_age`, earlier than `cover_end_age` at five of the eight carriers but equal at one [S1] and absent at one [S9], so the two ages are separate model-point columns | [S3]; pattern [S2] [S6] [S7] [S8]; exceptions [S1] [S9] |
| Premium cessation | On death and on recognition of PTIA | [S3] [S7] |
| Suicide | Death cover "de nul effet" in the **first year**; covered from the second; clock restarts on an increase, for the increment only. The alinéa 4 immediate cover with its 120 000 € floor is confined to principal-residence loan cover and **does not apply here** | [R1] [R2] |
| Surrender / paid-up value | **None**, by statute; expiry at `cover_end_age` pays nothing | [R3] [S3] [S5] [S7] [S9] [S11] |
| Fractionation loading `prem_freq_load` | Annual 1.000 (with a 1 % direct-debit discount at one carrier); half-yearly 1.0250; quarterly 1.0400; monthly 1.0400, plus a fixed *frais d'échéance* of 3 € / 6 € / 15 € (10 instalments) or 18 € (12) | [S1] |
| Age basis | *Différence de millésime* | [S1] [S2] [S6] [S7] |

**The attained-age tariff table** [S3] — *tarif de base annuel*, in per cent of the guaranteed
capital, by attained age. The only complete French standalone temporaire décès rate card in the
corpus; shipped as `premium_rate_table.csv` under `rate_id = maif_2019`:

| Age | Rate | Age | Rate | Age | Rate | Age | Rate | Age | Rate |
|---|---|---|---|---|---|---|---|---|---|
| 18–34 | 0,15 % | 42 | 0,32 % | 50 | 0,64 % | 58 | 1,05 % | 66\* | 2,55 % |
| 35 | 0,17 % | 43 | 0,36 % | 51 | 0,69 % | 59 | 1,13 % | 67\* | 2,78 % |
| 36 | 0,17 % | 44 | 0,40 % | 52 | 0,74 % | 60 | 1,56 % | 68\* | 2,88 % |
| 37 | 0,19 % | 45 | 0,44 % | 53 | 0,79 % | 61 | 1,68 % | 69\* | 3,14 % |
| 38 | 0,20 % | 46 | 0,48 % | 54 | 0,85 % | 62 | 1,81 % | 70\* | 3,43 % |
| 39 | 0,22 % | 47 | 0,52 % | 55 | 0,91 % | 63 | 1,97 % | 71\* | 3,74 % |
| 40 | 0,24 % | 48 | 0,56 % | 56 | 0,93 % | 64 | 2,14 % | 72\* | 4,09 % |
| 41 | 0,29 % | 49 | 0,60 % | 57 | 0,99 % | 65 | 2,33 % | 73\* | 4,46 % |
| | | | | | | | | 74\* | 4,86 % |

\* Entry is capped at 65, so ages 66–74 are in-force rates only — the carrier's own footnote
reads "la dernière colonne vous indique donc le tarif de base, **en cours de contrat**, pour
couvrir le risque de décès entre 65 et 75 ans" [S3]. The carrier's own two worked examples fix
the rule: 20 000 € at age 34 → 20 000 × 0,15/100 = **30 €** for one year; 150 000 € at age 49 →
150 000 × 0,60/100 = **900 €** for one year [S3]. **Vintage caveat:** the grid is a 2019–2021
edition; use it for shape, not level (product spec, footnote 7) [S3] [S4] [S10].

### (b) Insurer-discretionary current elements

Thin, but not empty — and thinner than it looks, because the discretion on this product bites
through the **rate card**, not through a bonus or a charge scale.

| Input | Snapshot value | Basis |
|---|---|---|
| Tariff drift (experience repricing of the class) | **0 % p.a.** — the rate card is frozen at its retrieved vintage in the base run **[std]** (1) | discretion cited at **two** carriers: "l'accroissement de la fréquence et/ou du coût moyen des sinistres" [S1] and "les résultats des garanties Assurance Décès" [S6]. A third reserves repricing for legislative or regulatory change only, with 15 days to terminate on a tariff change [S7] |
| *Revalorisation* / indexation of capital and cotisation | **Off** in the base run **[std]** (1) | PASS-linked [S1] [S7]; insurer-set rate [S2] [S6] |
| *Surprime* level (`rating_factor`) | **1.00** (standard rates) **[std]** (2) | mechanics [S1] [S2] [S3] [S6]; no published scale |
| Participation aux bénéfices | **None at policy level.** Computed globally across the insurer's life book where it exists at all | [S1] [S2]; none at all [S9] |
| Post-death revalorisation | Not projected — a sub-annual window between death and settlement | [S1] [S2] [S3] [S6]; [REG-R39] |

1. Both levers reprice the contract in force, and both are exogenous to the liability model: an
   experience re-rating multiplies `prem_rate`, an indexation multiplies `sum_assured` and
   `prem_pp` together. Setting both to zero keeps the base run reproducible from cited data
   alone. Note the asymmetry the contracts record: an increase decided by the insurer gives the
   member 30 days (15 at one carrier) to terminate, while an increase arising from age, index
   or law "n'ouvre droit ni à contestation ni à résiliation" [S1] [S7].
2. No insurer publishes a *surprime* scale [S1] [S2] [S3] [S6] [S7]. The only public French
   price evidence on rated lives is on borrower cover — average 1,01 % of initial capital before
   *écrêtement* and 0,65 % after [REG-R37] — which bounds a standard rate from above.

### (c) Behavioral / experience assumptions (modeler's view)

**Every input in this class is [std].** No French insurer publishes a mortality table, an A/E
factor, a PTIA incidence rate, an expense loading, a commission scale or a lapse rate for this
product [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S12].

**Mortality.** The regulatory non-annuity tables are **TH 00-02** (male) and **TF 00-02**
(female), homologated by the arrêté du 20 décembre 2005 with effect from 1 January 2006 and
built by INSEE on French mortality observed over 2000–2002 [R6] [R9] [REG-R22]. They are annexed
to an *arrêté* and are **cited by name, never shipped** in this library [REG-R22] [REG-R23].
Where a single homologated table is used for all insureds it must be the one giving the most
prudent tariff — the male table for a death cover [R4]; the alternative in market practice is a
blend, and the Institut des actuaires' working group uses **60 % TH 00-02 / 40 % TF 00-02** as
its unisex death basis [R13]. Neither choice is prescribed by any retrieved text, so adopting
one is **[std]**. The shipped `mort_table.csv` is therefore a **[std] Gompertz-form
proxy**, not a fitted table:

    mort_rate(x) = 0.00400 × 1.09^(x − 58),   ages 18–74

The 9 % per year of age is measured against the one observable French artefact, the published
tariff grid, and it sits at the **top** of what that grid shows rather than inside a tight band.
The grid rises at roughly **7–9 % per year of age from age 35** [S3]; over ages 42–58 the
step-by-step ratio `r(x+1)/r(x)` runs from **1,022** (the flat step 55 → 56, 0,91 % → 0,93 %) to
**1,125** (42 → 43) with a **median near 1,076** [S3]. Compounded, the same grid gives
`(1,05/0,32)^(1/16) − 1 = 7,7 %` a year over 42–58, `(4,86/2,55)^(1/8) − 1 = 8,4 %` over 66–74,
and `(4,86/0,17)^(1/39) − 1 = 8,98 %` over the whole rated span 35 → 74 — the last of which is
what 9 % is anchored to. It is a tariff gradient, not a mortality gradient, so the choice remains
**[std]**, and of the two unsourced numbers in this basis the slope is the more exposed on a
17-year run (see the sensitivities section). INSEE's national series [REG-R24] is the intended base for a
user-supplied replacement; it is *population*, not insured, mortality, and the reference library
records that the INSEE page **states no licence or reuse conditions** — standard open-data terms
are assumed there and that assumption is [unverified], so confirm before redistributing derived
CSVs [REG-R24]. **The anchor a substitute table must preserve is `mort_rate` at age 58 = 0.00400**,
so the worked example still closes.

*Décalages d'âge — and why they do not reach this product.* The annexed age shifts are imposed
by a clause whose scope excludes a death cover: "pour les contrats **en cas de vie** autres que
les contrats de rente viagère, les tables mentionnées au a sont utilisées en corrigeant l'âge de
l'assuré conformément aux décalages d'âge ci-annexés" [R4] [R6] [REG-R23]. A temporaire décès is
a contract *en cas de décès*, so on the retrieved texts **no shift applies to it**, and a user
who replaces `mort_table.csv` with TH 00-02 should load that table unshifted. Where the shifts do
bite, the profession recommends applying them **to the q(x), not to the l(x)**, because shifting
l(x) produces erratic q(x) growth and hence erratic provisions [R9]. The numeric annexe to the
current art. A. 132-18 was not retrieved [R4]; the abrogated A. 335-1 annexe carried shifts from
−11 years at ages 16–32 to 0 at 94+ for TF 00-02 and from −13 years at ages 16–38 to −3 at 75+
for TH 00-02 [REG-R23] — a −13-year shift is worth a factor of about 3 on this proxy's slope,
which is why applying one where it is not required is not a rounding error. The **[std]** proxy
therefore carries **no shift**, for both reasons: the rule does not reach a death cover, and a
shift applied to a proxy that was never a homologated table would be theatre.

**PTIA incidence.** No retrieved French source gives a PTIA incidence rate at any age. The model
uses `ptia_rate(x) = ptia_ratio × mort_rate(x)` with `ptia_ratio = 0.20` **[std]** for
`age(t) < ptia_end_age`, and **0** thereafter. The only public French figure that touches PTIA at
all is an underwriting-outcome statistic — 87 % of aggravated-risk applications received a PTIA
offer with no surprime and no exclusion, against 65 % for death [REG-R37] — which says nothing
about incidence. 0.20 is a placeholder chosen so PTIA is a visible but clearly secondary
decrement; it is the assumption in this file most in need of a real source.

**Lapse.** No insurer publishes a lapse rate and nothing in the corpus supports one
[S1] [S2] [S3] [S6] [S7] [S8] [S9]. The reference table is **[std]**, shaped by the one thing the
contracts do tell us — that voluntary exit is easy and cheap, because there is nothing to forfeit
[R3] and notice periods run from "at any time" to one month before the échéance
[S1] [S2] [S3] [S8] [S9]:

| Policy year (contractual, `= dur(t) + 1`) | 1 | 2 | 3 | 4+ |
|---|---|---|---|---|
| `lapse_rate(t)` **[std]** (3) | 12 % | 10 % | 8 % | 6 % |

These are **annual** rates and they stay annual: the table ships as `lapse_table.csv` keyed by
the contractual **policy year**, so the model reads it through `policy_year(t) = dur(t) + 1` —
months `t = 0 … 11` take the 12 %, and policy years from the fourth take the last row — and they
reach the month at `w_m(t) = 1 − (1 − w(t))^(1/12)` like any ordinary lapse.

**In the final projected policy year the lapse rate is zero: `w(n − 1) = 0` [std].** Lapses fall
at the *end* of the month (processing order, step 9), and the end of the last projected policy
year is the moment the cover expires — a lapse and an expiry are then the same event paying the
same nothing, so the whole surviving cohort is booked as an expiry, `l(12n)`. The zero covers
the **whole** of that policy year, months `12(n − 1) … 12n − 1`, and not merely its last month:
the convention is stated of a policy year, and zeroing only month `12n − 1` would leave eleven
months of 6 % lapse inside the final year. **No cash flow moves either way**, but the convention
is load-bearing for the closure identity: it decides the split between `Σ pols_lapse` and
`l(12n)`, and it is what the worked example's 0,64859269 / 0,27886852 reproduces — the survivor
term being exactly the one an annual step produces. Taking the table rate literally through the
last year instead gives roughly 0,666 lapses and 0,266 survivors, the same total and a different
split.

3. **No observed range exists** — not one of the eight retrieved carriers, and neither
   secondary guide, publishes a lapse rate [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S13] [S16]. The
   shape is a modeler's construction: elevated in the first three years to absorb the 30-day
   *renonciation* window [REG-R29] [S1] [S2] [S3] and early-duration attrition, then flat.
   Nothing about the levels is sourced, and a user with experience data should replace the whole
   table.

**Suicide-exclusion factor.** Art. L. 132-7 makes the death cover void for suicide in the first
year [R1]. The model applies

    suicide_factor(t) = 0.98 for dur(t) = 0,   1.000 for dur(t) ≥ 1   **[std]**

— the first year is contractual policy year 1, months `t = 0 … 11` — to **death claims only**.
The statute voids the cover "au cours de la **première année** du contrat" [R1], so the
exclusion covers the whole of that policy year; a monthly grid does not turn a statutory year
into a month. No retrieved
source gives a suicide share of deaths at any age — INSEE cause-of-death data was not fetched
for this research — so 0.98 is a placeholder standing for "about 2 % of first-year deaths are
excluded suicides". Setting it to 1.000 is a defensible variant; what is **not** defensible is
applying it to PTIA, or applying it beyond the first year, both of which are pitfalls below.

**Expenses and commission (all levels [std]; the structures are cited where they exist).**

| Input | Value | Basis |
|---|---|---|
| Acquisition expense `acq_expense` | 250 € per policy at issue | **[std]** (4) |
| Initial commission rate `comm_rate_init` | 40 % of the first-year cotisation | **[std]** (4) |
| Renewal commission rate `comm_rate_renew` | 5 % of the cotisation from policy year 2, i.e. `dur(t) ≥ 1` | **[std]** (4) |
| Maintenance expense `maint_expense` | 25 € per policy p.a., accruing at one twelfth a month and inflating at `expense_infl` | **[std]** (4) |
| Expense inflation `expense_infl` | 2 % p.a. flat | **[std]** (4) |
| Claim expense `claim_expense` | 150 € per death or PTIA claim | **[std]** (4) |
| Association subscription | 0 € (individual wrapper); 1,30 € per member per year in a group wrapper | [S1]; wrapper choice **[std]** (4) |
| Technical rate `tech_rate` | 0,5 % p.a., used **only** for the `constante` equivalence, never to discount the published cash flows | **[std]** (5) |

4. **No observed range exists.** No French insurer publishes an expense loading, an acquisition
   cost or a commission scale for this product [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S12]; the
   *chargements de gestion* are built into the tariff and are not separately disclosed anywhere,
   which is precisely why art. R. 343-3 has to require the *provision mathématique* to carry them
   [R11]. The **only** disclosed charge figures in the whole corpus are the fractionation
   loadings and *frais d'échéance* [S1], the 1,30 € association subscription [S1] and the 3 %
   annuity conversion charge [S3], and none of them is an expense assumption. The levels above
   are round-number placeholders sized so that year-one acquisition cost (250 € + 40 % of the
   cotisation) is of the same order as the year-one cotisation at the anchor age.
5. The Institut des actuaires' own illustrations for a death cover use technical rates of
   **0,5 %** and **0 %** against a 1 % interest assumption [R13]; art. A. 132-1 caps a French
   tariff rate at min(3,5 %, 60 % TME) for contracts *à primes périodiques* of any duration
   [R5] [REG-R17], so 0,5 % is well inside the cap. Adopting 0,5 % rather than 0 % is **[std]**.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | the **0-based** month index, `t = 0 … 12n − 1`, `12n = proj_len`, `n = proj_len_y = cover_end_age − issue_age` |
| `dur(t)` | completed policy years at the start of month t, `t // 12` |
| `policy_year(t)` | the contractual 1-based policy year label, `dur(t) + 1` |
| `x(t)` | attained age of month t's policy year = `issue_age + dur(t)` |
| `SA` | `sum_assured` |
| `r(x)` | tariff rate at attained age x, from `premium_rate_table.csv` |
| `f` | `rating_factor`; `φ` = `prem_freq_load` |
| `F` | `prem_freq_fee`, the fixed **annual** *frais d'échéance* — a euro amount, not a rate, and nil on the annual mode [S1] |
| `k` | `prem_instalments`, the instalments per policy year: 1 / 2 / 4 / 12 [S1]; `prem_cycle = 12 / k` months |
| `P_tar(t)` | `prem_tariff_pp(t)`, the **annual** tariff cotisation of month t's policy year, **before** `F` |
| `P(t)` | `prem_pp(t)`, the **annual** cotisation charged per in-force policy for month t's policy year, `= P_tar(t) + F` |
| `P_inst(t)` | `prem_inst_pp(t)`, the instalment collected at the beginning of month t: `P(t) / k` when `t mod prem_cycle = 0`, else 0 |
| `P_lev` | the level cotisation of the `constante` form, also before `F` |
| `B(t)` | `benefit_pp(t)`, the capital payable on a month-t claim |
| `q_d(t)` | `mort_rate(t)`, dependent **annual** rate of the death decrement of month t's policy year |
| `q_p(t)` | `ptia_rate(t)`, dependent **annual** rate of the PTIA decrement of the same year |
| `q(t)` | `decr_rate(t) = q_d(t) + q_p(t)`, the combined annual insured decrement; `q_m(t)` is the monthly rate applied |
| `q_dm(t)`, `q_pm(t)` | `mort_rate_mth(t)`, `ptia_rate_mth(t)`: `q_m(t)` split in the ratio `q_d : q_p` — see *Monthly rates from annual assumptions* |
| `w(t)` | `lapse_rate(t)`, the **annual** lapse rate of month t's policy year; `w = 0` through the final projected policy year **[std]** |
| `w_m(t)` | `lapse_rate_mth(t) = 1 − (1 − w(t))^(1/12)`, applied at EOM after both insured decrements **[std order]** |
| `σ(t)` | `suicide_factor(t)`, below 1 through policy year 1 |
| `l(t)` | `pols_if(t)`, in force at the start of month t (at time t); `l(0) = 1` |
| `p_τ(y)` | tariff survivorship entering **policy year** y, decrements only, no lapse: `p_τ(0) = 1`, `p_τ(y+1) = p_τ(y)(1 − q_d − q_p)` at the year's rates |
| `v` | `1 / (1 + tech_rate)`; `v^y` is a **policy-year** discount factor |
| `E0`, `e(t)` | acquisition expense; maintenance expense = `(25/12) × 1.02^dur(t)` per month |
| `c0`, `c_r` | initial commission rate (0.40); renewal commission rate (0.05) |
| `ec` | claim expense (150) |

`q_d`, `q_p` and `w` are per-annum probabilities and `q_dm`, `q_pm`, `w_m` per-month ones (all
dimensionless); `SA`, `B`, `P` are EUR; `P_inst` and every cash-flow component is EUR per month.

### Monthly rates from annual assumptions [std]

Every assumption in this product is published, calibrated and tabulated **annually**: the
mortality proxy is an annual table by attained age, the PTIA rate is a ratio on it, and the lapse
vector is by policy year. The monthly rates the recursion applies are derived from them at the
constant-force conversion, so that twelve months compound back to **exactly** the annual rate:

    q_m(t)  = 1 − (1 − q_d(t) − q_p(t))^(1/12)
    q_dm(t) = q_m(t) × q_d(t) / (q_d(t) + q_p(t))          zero-safe: 0 when q_d + q_p = 0
    q_pm(t) = q_m(t) × q_p(t) / (q_d(t) + q_p(t))          ( = ptia_ratio × q_dm(t) )
    w_m(t)  = 1 − (1 − w(t))^(1/12)

**The two insured rates are converted together and split afterwards, not converted apart.**
`q_d` and `q_p` are *dependent* rates of one two-decrement table and are therefore additive
(pitfall 4), so the rate the annual recursion applies — and therefore the rate the monthly one
has to reproduce — is their **sum**. Converting each separately and adding the results,
`(1 − (1 − q_d)^(1/12)) + (1 − (1 − q_p)^(1/12))`, gives a twelve-month insured survival of
0,9952029339 against the annual 0,9952000000 at the anchor cell: an error of 2,6 × 10⁻⁶ in `l`
at the very first anniversary and 1,0 × 10⁻⁵ by month 204, which would break both the
anniversary equivalence and the closure split. The proportional split also keeps
`q_pm / q_dm = ptia_ratio` exactly, so the acceleration ratio the product is built on survives
the conversion untouched; and where the PTIA gate has closed, `q_p = 0` and the formula
degenerates to the plain `1 − (1 − q_d)^(1/12)`.

**No exception is made for any rate.** Unlike `uslib`'s `Term_US_S`, this product carries no
shock lapse tied to a named date inside a policy year, so there is nothing to leave unspread;
the one rate these notes do put on a boundary — the zero of the final projected policy year — is
a rate for the whole of that year rather than for a month of it. No retrieved French source
states a conversion convention for any decrement, so the conversion itself is **[std]**; what is
not optional is that it reproduce the annual factor.

### Cotisation by premium form

**`revisable`** — the French default, and the product's signature.
`P_tar(t) = SA × r(x(t)) × f × φ`, which changes at every **anniversary** because `r` is read at
the new attained age [S1] [S2] [S3] [S4] [S6] [S7] [S9] [S10]. The contracts reprice "à chaque
échéance annuelle", so `P_tar` is flat across the twelve months of a policy year and there are
`n` distinct cotisations over `12n` months.

**`constante`** — a **[std]** construction (product spec, footnote 2). If `level_premium > 0` it
is used directly; otherwise `P_lev` is derived by actuarial equivalence with the revisable stream
over the whole cover period, on **tariff survivorship** (insured decrements only, no lapse) and
the technical rate:

    P_lev = [ Σ_{y=0..n−1} v^y · p_τ(y) · SA · r(x(12y)) · f · φ ] / [ Σ_{y=0..n−1} v^y · p_τ(y) ]

i.e. a survivorship-and-discount-weighted average of the same grid rates; `P_tar(t) = P_lev` for
all `t`. The sum runs over **policy years**, not months: the equivalence is an annual
construction and stays one on the monthly grid, so `v` and `p_τ` take a policy-year argument and
`P_lev`, the annuity-due factor 15,449728 and the present value 60 476,25 € are all unchanged by
the conversion. Re-striking the equivalence monthly would move `P_lev` and break the identity
these notes assert.

**Then the fee, once a year, under either form:**

    P(t)      = P_tar(t) + F
    P_inst(t) = P(t) / k   if  t mod prem_cycle = 0,   else 0

`F` is the fixed annual *frais d'échéance* attached to the payment frequency — 0 € annual,
3 € half-yearly, 6 € quarterly, 18 € monthly [S1]. It is a **euro amount, not a second
percentage**: `φ` is already a multiplier inside `P_tar`, and billing `F` as a further percentage
load, or loading the already-loaded cotisation with it, overstates premium income (pitfall 13).
`P(t)` is what the policyholder is charged, so it is what enters `premiums(t)` and the commission
base, while the `constante` equivalence above is struck on `P_tar` alone — `F` is the same amount
under either form, so it neither belongs in the equivalence nor changes it. The worked example
runs on the **annual** mode, where `F = 0`, `P(t) = P_tar(t)` and `k = 1`, so the whole
cotisation is collected in the first month of each policy year and nothing in the other eleven;
the three fractionated model points are where the two differ, e.g. 933,20 € against 915,20 € at
`t = 0` on model point 4, collected as twelve instalments of 77,77 €.

**The instalment is where the finer grid changes an answer rather than its resolution.** `φ` and
`F` exist *because* the cotisation is paid in instalments, and an annual grid could only charge
the loaded amount whole at the start of the year — pricing a service it never modelled. On the
monthly grid the instalments after the first are collected on a block that has already lost
lives, so the premium-cessation rule of the contracts [S3] [S7] finally bites: the three
fractionated model points collect 1,6 % to 3,1 % less than the annual grid did. The fee is
divided among the instalments with the rest, which is literally what
`freq_loading_table.csv` records of the monthly mode ("18 EUR frais d'echeance over 12
instalments"), so `k` instalments still sum to exactly `P(t)` and pitfall 13 is untouched:
`P(t) − P_tar(t) = 18,00 €` at every `t`.

### Decrements and the in-force recursion

`q_d` and `q_p` are **dependent** rates — rates of decrement in a two-decrement table, not
independent single-decrement rates. Therefore they are **additive**:

    pols_death(t) = l(t) × q_dm(t)
    pols_ptia(t)  = l(t) × q_pm(t)
    pols_lapse(t) = l(t) × (1 − q_dm(t) − q_pm(t)) × w_m(t)
    l(t+1)        = l(t) × (1 − q_dm(t) − q_pm(t)) × (1 − w_m(t)),    l(0) = 1

with `q_d(t) + q_p(t) < 1` required at every `t`, and the PTIA switch-off a hard gate on the
attained age rather than a taper: `q_p(t) = ptia_ratio × q_d(t)` if `x(t) < ptia_end_age`, else
`0`. Because `x(t)` steps on the anniversary, the gate closes on an anniversary too. This is what
"the PTIA capital is an anticipated payment of the death capital, and its payment ends the
contract" means arithmetically [S1] [S2] [S3] [S6]: a life that leaves through the PTIA decrement
is gone from `l` and can never generate a death claim. **Closure identity**, which a test should
assert:

    Σ_{t=0..12n−1} [ pols_death(t) + pols_ptia(t) + pols_lapse(t) ] + l(12n) = 1

**Annual equivalence.** Because `q_dm + q_pm` and `w_m` each compound back to their annual
values and both are constant within a policy year, the recursion collapses over any twelve months
of one policy year to

    l(t + 12) = l(t) × (1 − q_d − q_p) × (1 − w)

— the annual-step recursion, term for term. The in-force **at every anniversary** is therefore
identical on the two grids, to floating point: `l(12k)` here equals the annual model's `l(k)`,
measured at 2,3 × 10⁻¹⁵ or better across all twelve shipped model points. So is every
anniversary-dated contractual quantity — the tariff rate `r(x)`, the cotisation `P`, the capital
`B`, the annual decrement rates themselves, the level cotisation `P_lev` and the annuity-due
factor behind it — and so is the expiring cohort `l(12n)`. **Nothing else agrees, and nothing
else should:** the cash flows are where the finer grid does its work. `result_cf_annual()` sums
the monthly frame into policy years so the two can be laid side by side.

### Benefit amounts and claims

`B(t) = SA × benefit_factor(benefit_schedule_id, policy_year(t))` — `benefit_schedule.csv` is
keyed by the contractual policy year, so the lookup maps through `t + 1` — with
`benefit_factor ≡ 1.0` for
`benefit_schedule_id = constant`, the only schedule shipped [S1] [S2] [S3] [S6] [S7] [S8] [S9]:

    claims_death(t) = B(t) × pols_death(t) × σ(t)
    claims_ptia(t)  = B(t) × pols_ptia(t)
    claims_lapse(t) = 0                                   [R3]

`σ` never touches `claims_ptia`: art. L. 132-7 voids the **death** cover for suicide in the
first year, `t = 0` [R1], and PTIA is not death. With `accident_multiplier > 1` an additional capital
`(accident_multiplier − 1) × B(t) × acc_share` is payable on the accidental share of claims
[S1] [S2] [S6] [S7] [S9] [S12]; `acc_share` has **no source in the corpus** and the base run sets
it to 0 **[std]**.

### Expenses, commission and net cash flow

    premiums(t)    = P_inst(t) × l(t)                        with P(t) = P_tar(t) + F
    commissions(t) = c0 × premiums(t)                        for dur(t) = 0
                   = c_r × premiums(t)                       for dur(t) ≥ 1
    expenses(t)    = E0 · 1{t = 0} + (25/12) · 1.02^dur(t) × l(t)
                     + ec × (pols_death(t) + pols_ptia(t)) + commissions(t)
    net_cf(t)      = premiums(t) − claims_death(t) − claims_ptia(t) − expenses(t)
    liability_cf(t) = −net_cf(t)

The commission **rate** is a policy-year rate and steps on the anniversary; the **base** is the
instalment actually collected, so a fractionated payer earns it in instalments too and an
annual-mode payer's commission is unchanged from the annual grid.

Maintenance expense accrues at a twelfth a month and inflates **by policy year**,
`1.02^dur(t)`, stepping at anniversaries rather than compounding continuously — the frlib house
form, shared with `Obseques_FR_S`, `ADE_FR_S` and `Dep_FR_S`, and the way these notes tabulate
the charge. (`uslib`'s `Term_US_S` uses the continuous `1.02^(t/12)`; this library does not
follow it there, and the difference is measurable: 254,60 € of maintenance over the worked
configuration stepped against 256,89 € continuous.) Twelve twelfths of 25 € is the annual charge,
so a policy that runs a full year carries what it did on the annual grid; what changes materially
is that a **decrementing block carries less** of it, because the charge is borne by the in-force
of each month rather than of the anniversary — 254,60 € against the annual grid's 263,96 €. The
acquisition expense stays a single amount in month 0: it is a flat per-policy cost, not a fraction
of any instalment.

`result_cf()` publishes, indexed by the month `t`: `pols_if`, `premiums`, `claims_death`,
`claims_ptia`, `claims_lapse`, `expenses`, `commissions`, `net_cf`, `liability_cf`.
`result_cf_annual()` publishes the same columns summed into policy years and indexed by
`policy_year`, with `pols_if` taken at the **start** of the year, `l(12(k − 1))` — the number the
annual-step model carried on the same row.

### Processing order (monthiversary)

For `t = 0 … 12n − 1`, in this order. Each step is tagged by where it lands: **[A-anniv]** an
annual contract term landing whole on the anniversary, **[A-spread]** an annual assumption
spread at `1 − (1 − r)^(1/12)`, **[M]** a genuinely monthly quantity.

1. **[A-anniv]** Set `x(t) = issue_age + dur(t)`. If `x(t) ≥ cover_end_age`, stop — the
   projection is over.
2. **[A-anniv] Anniversary only (`t mod 12 = 0`) — reprice.** Look up `r(x(t))`, compute
   `P_tar(t)` per the premium form and add the fee once, `P(t) = P_tar(t) + F`. Both are then
   constant across the twelve months of the policy year: the contracts reprice "à chaque échéance
   annuelle" [S1] [S2] [S3] [S7], and spreading the repricing over the months would be a
   different product.
3. **[M] BOM — collect the instalment** if the elected mode makes one due,
   `P_inst(t) = P(t)/k` when `t mod prem_cycle = 0` and 0 otherwise:
   `premiums(t) = P_inst(t) × l(t)`.
4. **[M] BOM — commission** on the cotisation *collected*: `c0 × premiums(t)` through policy
   year 1 (`dur(t) = 0`) and `c_r × premiums(t)` thereafter. The rate is **[A-anniv]**; the base
   is the instalment.
5. **[M] BOM — expenses** on the in-force: one twelfth of the maintenance charge,
   `(25/12) × 1.02^dur(t) × l(t)`, plus `E0` in month 0 only. The inflation factor is
   **[A-anniv]**, stepping at the anniversary.
6. **[A-anniv]** Compute `B(t)` from the benefit schedule, read at `policy_year(t) = dur(t) + 1`,
   and `σ(t)`, which is 0,98 through the whole of policy year 1 and 1 thereafter.
7. **[A-spread] Decrements.** Look up the **annual** `q_d(t)`; set `q_p(t) = 0` if
   `x(t) ≥ ptia_end_age`, else `ptia_ratio × q_d(t)`. Convert the **sum** to the month and split
   it: `q_m = 1 − (1 − q_d − q_p)^(1/12)`, `q_dm = q_m q_d/(q_d + q_p)`,
   `q_pm = q_m q_p/(q_d + q_p)`.
8. **[M] EOM — claims:** `claims_death(t)` (with `σ(t)`) and `claims_ptia(t)`, plus the claim
   expense on both, settled at the end of the **month** of claim. Claimants have already paid the
   month's instalment in step 3; this is the model's reading of "premium payment ceases at death
   and at PTIA" [S3] [S7] **[std]**.
9. **[A-spread] EOM — lapses:** apply `w_m(t) = 1 − (1 − w(t))^(1/12)` to the survivors of both
   insured decrements. A lapse pays nothing [R3]. Through the whole of the final projected policy
   year, `dur(t) = n − 1`, `w(t) = 0` **[std]**: the end of that year is also the moment the cover
   expires, so the survivors leave as an expiry rather than as a lapse. The two events pay the
   same nothing, and no cash flow moves — but they land on different sides of the closure
   identity.
10. **[M]** Update `l(t+1) = l(t) × (1 − q_dm(t) − q_pm(t)) × (1 − w_m(t))`.
11. **[A-anniv]** `w_cum` is read by the selective-lapsation module **at the anniversary**, so
    the loaded `q_d` stays one annual rate for its policy year (behaviour section below).

After `t = 12n − 1` the projection ends with no maturity payment and no tail state; the only
value defined beyond the frame is the expiring cohort `l(12n)`.

### Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each
one is a test.

1. **Assuming a level cotisation.** The French default is `revisable`, not `constante`
   [S1] [S2] [S3] [S6] [S7] [S9] [S10]. Assert that `prem_pp(t)` varies with `t` on the
   revisable form, and specifically that `prem_pp(24) / prem_pp(12) = 1.56 / 1.13 = 1.380531`
   in the worked configuration — policy year 3 against policy year 2. Assert too that it moves
   **only** at the anniversary: 17 distinct cotisations over 204 months, not 204.
2. **Paying the capital twice.** PTIA is an acceleration, not an addition [S1] [S2] [S3] [S6].
   Assert `Σ(pols_death + pols_ptia) ≤ 1` and
   `Σ(claims_death + claims_ptia) = SA × Σ(pols_death + pols_ptia) − (1 − σ(0)) × SA ×
   Σ_{t=0..11} pols_death(t)` exactly — the suicide withholding covers the twelve months of
   policy year 1. A life removed by the PTIA decrement must not appear in `l(t+1)`.
3. **Forgetting that PTIA cover stops first.** `ptia_end_age < cover_end_age` in five of the
   eight retrieved carriers [S2] [S3] [S6] [S7] [S8]. Assert `claims_ptia(t) = 0` for every
   `t` with `x(t) ≥ ptia_end_age` — in the worked configuration, exactly zero for
   `t = 84 … 203`, the whole of the policy year at attained age 65 onwards.
4. **Mixing the competing-risk conventions.** These notes use **additive dependent rates**
   (`q_d + q_p`). An implementation using independent rates,
   `1 − (1 − q_d)(1 − q_p)`, gets 0.00479680 against 0.00480000 at `t = 0` — a 3.2 × 10⁻⁶
   difference in the rate and 0.48 € of first-year expected claims per 150 000 € of capital.
   Immaterial here, material at older ages and higher rates. Declare the convention and test it.
   On the monthly grid the same convention decides how the two rates reach the month; see
   pitfall 15.
5. **Inventing a surrender value.** There is none, by statute [R3] [S7] [S9]. Assert
   `claims_lapse(t) == 0.0` at every `t`, and that no `av_pp_at` / cash-value cells exist.
6. **Getting the age basis wrong.** *Différence de millésime*, not age nearest birthday
   [S1] [S2] [S6] [S7]. A one-year shift moves `prem_pp(0)` from 1 575,00 € (age 58) to
   1 695,00 € (age 59) — a 7,6 % error in year one that compounds through the whole projection.
   The age steps at the **anniversary**, so assert `x(11) = 58` and `x(12) = 59`, not `x(1) = 59`.
7. **Smoothing the tariff away.** The grid steps +38 % from age 59 to 60 against a trend of
   about +8 % [S3]. Assert `prem_rate` is a table lookup and that `r(60)/r(59) = 1.380531`
   survives; a fitted curve will not reproduce it.
8. **Misapplying the suicide factor.** `σ` applies to `claims_death` through the whole of
   **policy year 1**, months `t = 0 … 11`, and never to `claims_ptia` [R1]. The statute names a
   year, so a monthly grid does not shrink it to month 0. Assert
   `claims_death(11) = 0.98 × B(11) × pols_death(11)`,
   `claims_death(12) = B(12) × pols_death(12)` with no factor, and
   `claims_ptia(0) = B(0) × pols_ptia(0)` with no factor. Also assert the model does **not**
   carry the art. R. 132-5 immediate-cover ceiling of 120 000 €, which belongs to
   principal-residence loan cover only [R1] [R2].
9. **Double-counting the premium-cessation rule.** Instalments are in advance and claims are at
   month end, so a claimant has already paid the month's instalment. Do **not** additionally
   multiply `premiums(t)` by `(1 − q_dm − q_pm)` — that applies the rule twice. On the monthly
   grid the item it would double-count is one month's decrement on one instalment, about
   0,04 % of the month's income at the anchor age, because the finer grid has already put the
   real effect where it belongs: the instalments after the first are collected on a block that
   has genuinely lost lives.
10. **Running past the age limit.** `proj_len = 12 × (cover_end_age − issue_age)` is the
    **number** of projected months — 204 on the worked configuration — so the last row is
    `t = 203`. There is no benefit, no cotisation and no maturity value at `t = proj_len`, and
    `l(proj_len)` is never used in a cash flow [S3] [S5] [S11] — but it is used in the closure
    identity, and it is only well defined once `w = 0` in the final policy year is stated.
    Assert both: `lapse_rate(t) = 0` at **every** `t` from 192 to 203 while `lapse_rate_base(t)`
    is still the table's 6 %, `lapse_rate(191) = 6 %`, and that the four closure terms sum to 1.
11. **Expecting the two premium forms to collect the same total.** The `constante` equivalence
    is struck on **tariff survivorship** (no lapse). Once lapses truncate the expensive late
    years, the projected premium total under `constante` **exceeds** the revisable one —
    36 367,46 € against 31 999,13 € in the worked configuration. That is correct, not a bug;
    a test that asserts equality of projected premium totals is testing the wrong identity.
    The identity that *does* hold is `Σ v^t p_τ(t) P(t)` equal across the two forms.
12. **Applying `rating_factor` to the benefit.** A *surprime* scales the cotisation only, never
    the capital [S1] [S2] [S3] [S6]. Assert `claims_death` is invariant to `rating_factor`.
13. **Double-charging the fractionation loading.** `prem_freq_load` (`φ`) is a multiplier
    embedded in the cotisation TTC; the *frais d'échéance* (`F`) are a separate fixed fee, in
    euros [S1]. Applying both as percentage loads, or applying the loading and then also billing
    the fee as a percentage, overstates premium income. The fee is charged **once a year** and it
    **is** part of what the policyholder pays, so it enters `premiums(t)` and the commission base
    but stays out of the `constante` equivalence. Assert `P(0) = 915,20 + 18,00 = 933,20 €` on
    model point 4 (monthly, 200 000 € at attained age 45) and `P(t) − P_tar(t) = 18,00 €` at
    every `t` — and, on the monthly grid, `P_inst(0) = 933,20 / 12 = 77,77 €` with an instalment
    due in every month, against `prem_cycle = 6` and instalments in months 0 and 6 only on model
    point 10.
14. **Treating the accidental option as a benefit multiplier.** It pays an *additional* capital
    on the accidental share of claims [S1] [S2] [S6] [S7], not a uniform uplift on every claim.
    With `acc_share = 0` in the base run, `accident_multiplier` must have **no** effect on any
    cash flow — a good invariance test.
15. **Splitting the two dependent decrements independently on the monthly grid.** `q_d` and
    `q_p` are additive (pitfall 4), so it is their **sum** the annual recursion applies and their
    sum that must compound back. Converting each apart,
    `(1 − (1 − q_d)^(1/12)) + (1 − (1 − q_p)^(1/12))`, misses the annual insured-decrement factor
    by 2,6 × 10⁻⁶ at the first anniversary and leaves 1,0 × 10⁻⁵ of error in `l` by month 204 —
    enough to break the anniversary equivalence and the closure split, and enough to lose the
    exact `q_pm / q_dm = ptia_ratio`. Convert the sum and split it in the rates' own proportion.
16. **Spreading a contract term because the grid is finer.** The repricing, the benefit
    schedule, the suicide year, the first-year commission rate, the *constante* equivalence and
    the zero lapse of the final year are all **contractual** and land on the policy year, whole.
    A monthly grid is not a monthly product. Assert that each is constant across the twelve
    months of a policy year.
17. **Collecting a fractionated cotisation whole at the anniversary.** The reverse error: it
    preserves the annual grid's premium totals and makes `φ` and the *frais d'échéance*
    meaningless, since both exist to price the instalment cycle. Collect `P(t)/k` on the mode's
    own cycle and let the totals move; the three fractionated model points then collect 1,6 % to
    3,1 % less than an annual grid reported, which is the premium-cessation rule acting where it
    could not before.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; there is no French calibration
evidence for any of them.

- **Base lapse [std].** The duration table above. Channel and wrapper matter and are not
  modeled: a *bancassurance* contract terminates when the bank account closes [S8], which is a
  lapse driver with no actuarial counterpart in the mutual contracts.
- **Premium-shock lapse [std] (optional module, off in the base run).** The revisable form
  hands the policyholder a rising bill, and the grid's own +38 % step at age 60 [S3] is exactly
  where an affordability response would show. Reference multiplier on `w(t)`:

      M_shock(t) = 1 + β × max(0, P(t)/P(t−12) − 1 − g0)

  with `g0 = 0.10` and `β = 1.5` **[std]**. The ratio is between consecutive **renewals**, so the
  previous cotisation is read twelve months back: on a monthly grid `P(t)/P(t−1)` would be 1 in
  eleven months of twelve and the module would never fire at all. Base run `β = 0`, so
  `M_shock ≡ 1`. `M_shock ≡ 1` through the whole of policy year 1, which has no previous renewal
  to compare with. Switched on in the worked configuration it takes the value 1.420796 through
  the whole of policy year 3 — months 24 to 35, ratio 1.380531 — and 1 everywhere else; the
  elevated **annual** rate is then spread over those twelve months at `w_m` like any other
  ordinary lapse.
- **Selective lapsation [std] (optional module, off in the base run).** Lapsers are healthier on
  average, so persisters' mortality is loaded:

      q_d_eff(t) = q_d(t) × [ 1 + λ × max(0, w_cum(12·dur(t)) − w_ref) ]

  with `w_ref = 0.30` and `λ = 0.25` **[std]**. Base run `λ = 0`. `w_cum` moves every month, but
  it is read **at the anniversary**, so the loading is one number for the whole policy year and
  `q_d` stays the *annual* rate of that year — which is what the library's `*_rate` /
  `*_rate_mth` split requires, and the only basis the module was ever calibrated on. The
  deterioration is a multiplier on the **annual** rate, applied before the monthly conversion, so
  it grades once a year and not once a month. On this product the effect is larger than on a UK
  level-premium term policy, because cumulative lapse reaches 64,9 % of the original cohort over
  the worked configuration's 17 years.
- **No dynamic surrender behavior, no renonciation decrement, no indexation take-up.** There is
  nothing to surrender [R3], so the whole of the exit machinery is lapse and a lapse pays
  nothing; the 30-day *renonciation* window [REG-R29] [S1] [S2] [S3] sits inside the year-1 lapse
  rate **[std]**; and indexation is not modeled because it reprices capital and cotisation
  together on an exogenous index [S1] [S2] [S6] [S7], with refusal definitive at three carriers
  [S2] [S6] [S7] — a one-way absorbing state if it were modeled.

---

## Worked example

**Configuration.** `premium_form = revisable`, `benefit_shape = constant`
(`benefit_schedule_id = constant`, factor 1.0 at every `t`), `issue_age = 58`,
`sum_assured = 150 000 €`, `cover_end_age = 75`, `ptia_end_age = 65`,
`premium_rate_id = maif_2019`, `rating_factor = 1.00`, `prem_freq = annual`
(`prem_freq_load = 1.000`, `prem_instalments = 1`, so the whole cotisation falls in the first
month of each policy year), `waiting_period_y = 0`, `accident_multiplier = 1.00`. Hence
`n = 75 − 58 = 17` policy years, `proj_len = 204` months, the frame is `t = 0 … 203`, and the
two tables below are the twelve months of policy year 1 and the **entire** projection summed
into policy years.

**Assumptions, each tagged.** Tariff rates `r(x)` for ages 58–74 read from the published grid
[S3] — 1,05 / 1,13 / 1,56 / 1,68 / 1,81 / 1,97 / 2,14 / 2,33 / 2,55 / 2,78 / 2,88 / 3,14 /
3,43 / 3,74 / 4,09 / 4,46 / 4,86 % — each read once, at the anniversary opening its policy year,
so `P(t)` is flat across that year's twelve months. Mortality
`q_d(t) = 0.00400 × 1.09^dur(t)` **[std]**, an **annual** rate. PTIA
`q_p(t) = 0.20 × q_d(t)` for `dur(t) ≤ 6` (attained ages 58–64) and **0** from `dur(t) = 7`,
i.e. from month 84 (attained age 65 = `ptia_end_age`) **[std]**. Lapse 12 % / 10 % / 8 % / 6 %
from the fourth year **[std]**, annual rates read from the policy-year-keyed table at
`policy_year(t) = dur(t) + 1`, with `w = 0` through the whole of policy year 17 (months 192–203)
because the last projected year ends at expiry (processing order, step 9) — the assumption that
fixes the lapse/survivor split in the closure check below, though it moves no cash flow. All
four rates reach the month at `1 − (1 − r)^(1/12)`, the insured pair converted on its **sum** and
split in the ratio `q_d : q_p`. Suicide factor `σ = 0.98` through policy year 1 (months 0–11),
1.000 thereafter, applied to death claims only **[std]** [R1]. Expenses **[std]**:
`E0 = 250 €` at issue, `(25/12) × 1.02^dur(t)` per in-force policy per month, initial commission
40 % of the cotisation collected through policy year 1, renewal commission 5 % of it from policy
year 2, claim expense 150 € per death or PTIA claim. No accident option, no indexation, no
tariff drift, no behavior modules.

`expenses` below is the total of acquisition, maintenance, claim expense and commission.
All amounts in euros; `pols_if` to six decimals; cash flows to the cent.

### The months of policy year 1 (`t = 0 … 11`)

These twelve rows are `result_cf()` row for row, and they are what an **annual-mode** policy
looks like on a monthly grid: the whole cotisation and the whole acquisition cost fall in month
0 and nothing else does, so month 0 is strongly positive and the eleven months after it carry
only claims and a twelfth of the maintenance charge. Model point 4 is the contrast — twelve
instalments of 77,77 €.

| t | pols_if | premiums | claims_death | claims_ptia | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 1,575.00 | 49.11 | 10.02 | 882.14 | 630.00 | 633.73 |
| 1 | 0.989007 | 0.00 | 48.57 | 9.91 | 2.12 | 0.00 | −60.60 |
| 2 | 0.978135 | 0.00 | 48.03 | 9.80 | 2.10 | 0.00 | −59.93 |
| 3 | 0.967383 | 0.00 | 47.51 | 9.70 | 2.07 | 0.00 | −59.28 |
| 4 | 0.956748 | 0.00 | 46.98 | 9.59 | 2.05 | 0.00 | −58.62 |
| 5 | 0.946231 | 0.00 | 46.47 | 9.48 | 2.03 | 0.00 | −57.98 |
| 6 | 0.935829 | 0.00 | 45.96 | 9.38 | 2.01 | 0.00 | −57.34 |
| 7 | 0.925542 | 0.00 | 45.45 | 9.28 | 1.98 | 0.00 | −56.71 |
| 8 | 0.915367 | 0.00 | 44.95 | 9.17 | 1.96 | 0.00 | −56.09 |
| 9 | 0.905305 | 0.00 | 44.46 | 9.07 | 1.94 | 0.00 | −55.47 |
| 10 | 0.895353 | 0.00 | 43.97 | 8.97 | 1.92 | 0.00 | −54.86 |
| 11 | 0.885510 | 0.00 | 43.49 | 8.87 | 1.90 | 0.00 | −54.26 |

`expenses(0) = 250 + 2,08 + 0,06 + 630 = 882,14 €`: the acquisition cost, one twelfth of the
25 € annual maintenance charge, the claim expense on the month's 0,00040088 of claim events, and
the 40 % initial commission on the whole annual cotisation collected in this month.

**The month-0 decrement is the check on the rate conversion.** `q_d(0) = 0,00400` and
`q_p(0) = 0,00080`, so the annual insured decrement is `q(0) = 0,00480` and
`q_m(0) = 1 − (1 − 0,0048)^(1/12) = 0,00040088`, split 0,00033407 / 0,00006681 in the exact
ratio 0,20; `w(0) = 12 %` gives `w_m(0) = 1 − (1 − 0,12)^(1/12) = 0,01059624`. So
`l(1) = (1 − 0,00040088)(1 − 0,01059624) = 0,989007` ✓, and twelve such months land on
`l(12) = 0,875776` — the annual model's `l(1)`, exactly.

### The same frame summed into policy years (years 1–17)

Each row is the total of its twelve months, produced by `result_cf_annual()`; `pols_if` is
`l(12(k − 1))`, the count **entering** the policy year, which is the number the annual-step
model this replaced carried on the same row. The **Total** row covers all seventeen years.

| policy year (months t) | age | r(x) | pols_if | premiums | claims_death | claims_ptia | expenses | net_cf |
|---|---|---|---|---|---|---|---|---|
| 1 (0–11) | 58 | 1,05 % | 1.000000 | 1,575.00 | 554.94 | 113.25 | 904.22 | 2.58 |
| 2 (12–23) | 59 | 1,13 % | 0.875776 | 1,484.44 | 546.03 | 109.21 | 96.12 | 733.09 |
| 3 (24–35) | 60 | 1,56 % | 0.784075 | 1,834.73 | 538.15 | 107.63 | 111.97 | 1,076.98 |
| 4 (36–47) | 61 | 1,68 % | 0.717235 | 1,807.43 | 541.82 | 108.36 | 109.47 | 1,047.77 |
| 5 (48–59) | 62 | 1,81 % | 0.670010 | 1,819.08 | 551.70 | 110.34 | 109.19 | 1,047.84 |
| 6 (60–71) | 63 | 1,97 % | 0.625542 | 1,848.48 | 561.45 | 112.29 | 109.83 | 1,064.91 |
| 7 (72–83) | 64 | 2,14 % | 0.583667 | 1,873.57 | 571.01 | 114.20 | 110.28 | 1,078.07 |
| 8 (84–95) | 65 | 2,33 % | 0.544230 | 1,902.08 | 580.35 | 0.00 | 110.83 | 1,210.91 |
| 9 (96–107) | 66 | 2,55 % | 0.507836 | 1,942.47 | 590.28 | 0.00 | 112.12 | 1,240.07 |
| 10 (108–119) | 67 | 2,78 % | 0.473561 | 1,974.75 | 599.98 | 0.00 | 113.04 | 1,261.73 |
| 11 (120–131) | 68 | 2,88 % | 0.441280 | 1,906.33 | 609.40 | 0.00 | 108.94 | 1,187.98 |
| 12 (132–143) | 69 | 3,14 % | 0.410875 | 1,935.22 | 618.48 | 0.00 | 109.74 | 1,207.00 |
| 13 (144–155) | 70 | 3,43 % | 0.382236 | 1,966.60 | 627.16 | 0.00 | 110.68 | 1,228.76 |
| 14 (156–167) | 71 | 3,74 % | 0.355260 | 1,993.01 | 635.36 | 0.00 | 111.39 | 1,246.25 |
| 15 (168–179) | 72 | 4,09 % | 0.329849 | 2,023.62 | 643.01 | 0.00 | 112.34 | 1,268.27 |
| 16 (180–191) | 73 | 4,46 % | 0.305913 | 2,046.56 | 650.03 | 0.00 | 112.92 | 1,283.61 |
| 17 (192–203) | 74 | 4,86 % | 0.283369 | 2,065.76 | 675.04 | 0.00 | 113.62 | 1,277.10 |
| **Total** | | | | **31,999.13** | **10,094.20** | **775.29** | **2,666.69** | **18,462.95** |

`claims_lapse = 0.00` in every month and is omitted from the table for space; it is a required
column of `result_cf()`. The **Total** row is the sum **at full precision, then rounded** — for
`claims_death` that is 10 094,20 € against 10 094,19 € if the seventeen already-rounded cells are
added, a one-cent accumulation. Assert the full-precision total.

**Cross-checks against the annual grid this replaced.** The `pols_if` column is *the same
number, row for row*, because it is a pure anniversary quantity and the monthly rates compound
back to the annual ones; so are `age`, `r(x)` and `prem_pp`. **`premiums` is unchanged to the
cent, row for row and in total (31 999,13 €)**, because an annual-mode cotisation is collected on
the anniversary and weighted by the anniversary in-force under either grid — and so is
`commissions`, a policy-year rate on it.

Claims and expenses are not, and the direction is the informative part. Death claims fall from
10 396,90 € to **10 094,20 €** (−2,9 %) and PTIA claims from 804,25 € to **775,29 €** (−3,6 %),
because a block that is losing lives every month is exposed for less of the year than an
anniversary weighting assumes; the PTIA gap is the larger of the two because the PTIA years are
the early high-lapse ones. Expenses fall from 2 676,38 € to **2 666,69 €** (−0,36 %), the net of
maintenance falling from 263,96 € to 254,60 € (−3,5 %, the same decrementing-block effect on a
charge now borne monthly) against the claim expense following its own smaller base. `net_cf`
is the residual and rises from 18 121,59 € to **18 462,95 €** (+1,9 %). One sign changes with
it: policy year 1 moves from −38,72 € to **+2,58 €**, so the shape to describe is no longer
"almost no new-business strain" but "the first year is marginally positive" — the year's
cotisation now slightly more than paying the year's acquisition cost.

**Level-premium variant.** The same cell with `premium_form = constante` and
`level_premium = 0`, so `P_lev` is derived by equivalence at `tech_rate = 0,5 %`:

    P_lev = 60,476.2476 / 15.449728 = 3,914.3891 €   (displayed 3,914.39)

The variant table below carries `P_lev` **unrounded**. Every displayed row is stable at two
decimals under either treatment; only the premium total moves, to 36 367,47 € if `P_lev` is
rounded to the cent before projecting.

Selected policy years of the resulting projection, from its own `result_cf_annual()` —
decrements, benefits and `pols_if` are identical to the table above, only the premium and the
commission change, and the **Total** row covers all seventeen years, not only the five displayed:

| policy year | age | prem_pp | premiums | claims_death | claims_ptia | expenses | net_cf |
|---|---|---|---|---|---|---|---|
| 1 | 58 | 3,914.39 | 3,914.39 | 554.94 | 113.25 | 1,839.98 | 1,406.22 |
| 2 | 59 | 3,914.39 | 3,428.13 | 546.03 | 109.21 | 193.30 | 2,579.59 |
| 3 | 60 | 3,914.39 | 3,069.17 | 538.15 | 107.63 | 173.69 | 2,249.70 |
| 8 | 65 | 3,914.39 | 2,130.33 | 580.35 | 0.00 | 122.24 | 1,427.74 |
| 17 | 74 | 3,914.39 | 1,109.22 | 675.04 | 0.00 | 65.79 | 368.39 |
| **Total** | | | **36,367.46** | **10,094.20** | **775.29** | **3,703.89** | **21,794.07** |

`P_lev = 3 914,3891 €` and the premium total 36 367,46 € are **unchanged** by the conversion:
the equivalence is annual and this point pays annually, so both the striking and the collection
live on the anniversary.

The two forms are the whole point of this product. The revisable premium runs from 1 575,00 €
to 7 290,00 € — a factor of **4,6286**, exactly `r(74)/r(58) = 4,86/1,05` and independent of
the capital — while the level premium is flat at 3 914,39 €, above the tariff until policy year
9 and below it from policy year 10. The revisable form has almost no new-business strain (policy
year 1 is +2,58 €); the level form is strongly positive in policy year 1 (+1 406,22 €) and would
carry a real *provision mathématique* against the later years [R11] [R13].

**Checks.**

*The cotisation rule, from the source's own example.* The carrier publishes "150 000 € ×
(0,60 : 100) = 900 € pour un an" at attained age 49 [S3]. The same rule at attained age 58
gives `P(0) = 150 000 × 1,05/100 = 1 575,00 €`, and the last year's rate reproduces
`150 000 × 4,86/100 = 7 290,00 €`. The ratio 7 290,00 / 1 575,00 = 4,6286 equals
4,86 / 1,05 = 4,6286 — the premium multiple over the contract depends only on the grid, not on
the capital, which is a one-line test of the whole premium engine.

*Policy year 3 rebuilt from scratch, a different way.* The in-force rebuild is exact on either
grid, because it runs on the **annual** factors: `l(12) = (1 − 0,00400 − 0,00080)(1 − 0,12) =
0,99520 × 0,88 = 0,875776`; `q_d = 0,00400 × 1,09 = 0,004360` and `q_p = 0,000872` in policy
year 2, so `l(24) = 0,875776 × (1 − 0,005232) × 0,90 = 0,875776 × 0,8952912 = 0,78407455`,
matching the table's 0.784075.

The cash-flow rebuild is now a single **month's** product, because a policy year's claims are the
sum of twelve of them. Take month 24, the first of policy year 3. The annual rates are
`q_d = 0,00400 × 1,09² = 0,0047524` and `q_p = 0,00095048`, so `q = 0,00570288` and
`q_m = 1 − (1 − 0,00570288)^(1/12) = 0,00047649`, split `q_dm = 0,00039707` and
`q_pm = 0,00007941`. Then `claims_death(24) = 150 000 × 0,78407455 × 0,00039707 = 46,70` and
`claims_ptia(24) = 150 000 × 0,78407455 × 0,00007941 = 9,34`. Expenses:
`(25/12) × 1,02² × 0,78407455 = 1,6995` maintenance, `0,05 × 2 340,00 × 0,78407455 = 91,7367`
commission on the whole annual cotisation collected this month, `150 × 0,78407455 × 0,00047649 =
0,0560` claim expense — total 93,49. And `1 834,73 − 46,70 − 9,34 − 93,49 = 1 685,20`, the
frame's `net_cf(24)`. The policy-year row above is the sum of that month and the eleven after
it: 1 076,98 €.

*The decrements close, and nothing is paid twice.* Summing the three exits over the 204 months:
deaths 0,06737020, PTIA claims 0,00516859, lapses 0,64859269, plus `l(204) = 0,27886852` —
total **1,00000000** exactly. The **survivor term is identical to the annual grid's**, being a
pure anniversary quantity; the three exit terms are not, and the reallocation is the expected
one — a decrementing block reaches the claim decrements later in the year, so fewer lives leave
through them and correspondingly more leave as a lapse (the annual grid read 0,06939268 /
0,00536169 / 0,64637711). The split is what `w = 0` in the final policy year decides.

Multiplying total claim events by the capital,
`150 000 × (0,06737020 + 0,00516859) = 10 880,82 €`, against claims actually paid of
`10 094,20 + 775,29 = 10 869,49 €`. The difference is **11,33 €**, which is precisely the
policy-year-1 suicide withholding `0,02 × 150 000 × 0,00377512` — the deaths of the twelve
months of policy year 1 — [R1], so the exclusion factor is the *only* thing standing between
expected claim events and expected claim amounts, which is what "PTIA is an acceleration, not an
addition" means arithmetically.

*The level premium is a weighted average of the grid.* Independently of the equivalence
formula, `P_lev / SA` should be the `v^y p_τ(y)`-weighted mean of the seventeen grid rates.
That mean is **2,60959276 %**, and `150 000 × 0,0260959276 = 3 914,3891 €` — the same figure,
reached without ever forming the premium stream. The weights sum to `15,449728`, the annuity-due
factor, and `P_lev × 15,449728 = 60 476,25 €` equals the present value of the revisable stream
on the same basis. Note what this identity does **not** say: the *projected* premium totals
differ (36 367,46 € against 31 999,13 €), because lapses remove policies before the expensive
late years that the level premium has already been charging for. Pitfall 11.

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a
declared grid. The valuation layers consume them and are cited, not reproduced.

- **The French statutory *provision mathématique*.** Art. R. 343-3 defines it as the difference
  between the present values of the two parties' commitments and requires it to **include an
  estimate of future management costs** equal to the *chargements de gestion* built into the
  tariff [R11] [REG-R6]. On the **revisable** form the PM is close to nil at each anniversary —
  the year's cotisation buys the year's risk, so what remains is an unearned-premium and
  outstanding-claims position [R11] [R13]. On the **constante** form it builds and releases in
  the classic way: where the premium rate is flat while the death rate rises, "un montant de PRC
  est toujours constitué pendant la durée" [R13]. That contrast is the reason the `constante`
  form is carried at all. The *provision pour risques croissants* of art. R. 343-7 is defined for
  *maladie* and *invalidité*, not death [R12]; the death-cover analogue is the R. 343-3 PM —
  "la même provision de prime s'appelle PM en vie et PRC en non-vie" [R13]. Art. A. 343-1-1
  requires acquisition loadings to enter the premium-payer's commitment and floors the result at
  zero, at the surrender value and at the reduced-capital provision; the last two are **zero**
  here [R3] [R13], so the operative floor is non-negativity. Art. 142-3 of ANC 2015-11 (as
  amended by ANC 2016-12) fixes the rate at no more than the tariff rate and the table at the one
  in force when the tariff was applied, with the option to migrate in-force contracts at each
  annual inventory and to spread a change of basis over at most eight years [R13].
- **Medical selection.** The Institut's illustrative claims abatement for a selected book is
  **70 % in year 1, 50 % in year 2, 20 % in year 3** [R13]. It is not applied in the base run —
  stacking a selection abatement on an already-[std] mortality proxy would compound two unsourced
  choices — but it is the first refinement a user with real experience should make, and it
  changes the sign of the early-duration provision [R13].
- **Solvabilité II best estimate.** Probability-weighted future cash flows discounted at the
  relevant risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R4], with EIOPA
  publishing the curves monthly [REG-R5]. `BEL = Σ_t v(t) × liability_cf(t)` over the recursion
  above. **No cost-of-capital rate, contract-boundary rule or standard-formula shock in this
  library was read from a retrieved instrument**, so every such figure is **[std]** [REG-R2].
- **Contract boundary — the open question on this product.** The contract is a one-year cover
  renewed by *tacite reconduction* whose tariff the insurer recomputes at every renewal
  [S1] [S2] [S3] [S6] [S7] [S9] and, at two of them, may also reprice for class experience
  [S1] [S6]. Whether
  the Solvabilité II contract boundary therefore ends at the next renewal — as it would for a
  reviewable-premium contract — could **not** be determined: the Delegated Regulation's boundary
  rules were not retrievable [REG-R2] and the point is **[unverified]**. The model's posture:
  project to the age limit and publish the full stream; a boundary-truncated view is obtained by
  truncating `result_cf()` after the first **twelve** rows, `t = 0 … 11`, or equivalently
  `result_cf_annual()` after its first row. Do not bake the truncation into the projection.
- **IFRS 17 and professional standards.** Fulfilment cash flows plus a contractual service
  margin, effective from 1 January 2023 with no French carve-out [REG-R45]; the same
  expected-cash-flow engine feeds it, and grouping, CSM and risk adjustment are out of scope.
  *Norme de Pratique Actuarielle 2 — Modèles actuariels*, adopted 15 June 2015 with effect from
  1 January 2016, expressly covers pricing models and the technical studies attached to new
  products [REG-R44]; NPA 4, on best-estimate life provisions, was not retrieved and is
  [unverified] [REG-R44].

---

## Key sensitivities and model risks

In rough order of leverage for a French protection block:

1. **The premium form.** Switching `revisable` → `constante` moves projected premium income by
   +13,7 % (31 999,13 € → 36 367,46 €) and `net_cf` by +18,04 % on the worked configuration,
   with no change to a single claim. It is the largest single structural lever in the model, and
   the `constante` side of it is **[std]** — no French standalone contract in the corpus uses it
   [S1] [S2] [S3] [S6] [S7] [S9] [S10].
2. **Mortality basis.** The reference basis is a **[std]** Gompertz proxy because TH 00-02 /
   TF 00-02 are annexed to an *arrêté* and not redistributed here [R6] [REG-R22] [REG-R23], and
   no French insurer publishes a basis [S1]–[S9]. Both the level (`q_d` at 58) and the slope
   (9 % per year of age) are unsourced; the slope is the more dangerous of the two on a
   17-year run, since it compounds. It is calibrated to the published tariff grid's own
   gradient and sits at the top of it — the grid compounds at 7,7 % a year over ages 42–58 and
   8,98 % over the whole rated span 35 → 74 [S3] — and a tariff gradient is not a mortality
   gradient.
3. **Lapse.** Nothing in the corpus supports any lapse rate. Cumulative lapse reaches **64,9 %**
   of the original cohort over the worked configuration, so the assumption governs how much of
   the rising-premium tail is ever collected — and on a revisable contract the late years are
   the profitable ones, which inverts the usual protection intuition that early lapse is what
   hurts.
4. **PTIA incidence ratio.** `ptia_ratio = 0.20` is a pure placeholder with **no source at
   all**. It moves 775,29 € of claims in the worked configuration — 7,1 % of total claims — and
   it interacts with `ptia_end_age`, since the whole of that exposure sits in the first seven
   policy years.
5. **Contract boundary.** If the boundary is one year rather than the full cover period, the
   entire projection beyond month 11 leaves the technical provision. Nothing in this library
   resolves it [REG-R2].
6. **Tariff drift.** The base run freezes the rate card at its retrieved vintage, but the same
   carrier's current page implies about 0,189 % at age 35 against the grid's 0,17 % [S3] [S4],
   and two of the eight carriers reserve an explicit right to reprice on class experience
   [S1] [S6]. A
   drift assumption is a premium-income assumption, not a mortality one.
7. **Expense levels on small capitals, and the suicide factor.** Minimum capitals run from
   6 097,96 € [S9] to 100 000 € [S8]; at the representative carrier's 20 000 € minimum [S3] [S4]
   the year-one cotisation at age 58 is 210 € against 250 € of acquisition expense **[std]**, so
   the per-policy expense assumption, not mortality, decides whether the cell is viable. The
   suicide factor is worth only 11,33 € here — immaterial to the result, material to correctness,
   because an implementation that applies it to PTIA, or to every year, or that imports the
   120 000 € immediate-cover ceiling from loan business [R1] [R2], is wrong in a way the totals
   will not reveal.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-temporaire_deces-r1
[R10]: #frlib-temporaire_deces-r10
[R11]: #frlib-temporaire_deces-r11
[R12]: #frlib-temporaire_deces-r12
[R13]: #frlib-temporaire_deces-r13
[R2]: #frlib-temporaire_deces-r2
[R3]: #frlib-temporaire_deces-r3
[R4]: #frlib-temporaire_deces-r4
[R5]: #frlib-temporaire_deces-r5
[R6]: #frlib-temporaire_deces-r6
[R9]: #frlib-temporaire_deces-r9
[REG-R1]: #frlib-reg-r1
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R37]: #frlib-reg-r37
[REG-R39]: #frlib-reg-r39
[REG-R4]: #frlib-reg-r4
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
