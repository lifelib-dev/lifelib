# Product Specification

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** A *standardized composite specification* for reference liability cash-flow modeling; not any
single insurer's product. [S#] (primary product documents) and [R#] (regulatory/actuarial references) are
numbered per `_research/deferred-income-annuity.md`. [REG-R#] resolves against the cross-product library
`references/regulatory-and-actuarial-references.md`, whose shared numbering now runs **R1–R157** as **one**
space, with most of the **R73–R149** block unused: R1–R34 of life origin (provenance
`_research/regulatory-actuarial.md`), R35–R72 annuity-specific (provenance
`_research/regulatory-actuarial-annuities.md`), and
**R150–R157 the AP&P Manual appendix and actuarial-guideline prints read on 2026-08-06**.
**[std]** marks standardizations introduced
for the reference implementation; every [std] table row carries a footnote giving the rationale and the
observed range. [unverified] marks claims not confirmed against a retrieved document.

**Representative design.** Base case = the **flexible-premium archetype** [S2], together with a second
carrier's flexible-premium design [S3]: flexible premium, each premium buying a guaranteed paid-up income
slice at then-current purchase rates, return of premium on death in deferral on every option except Life
Only, a one-time ±5-year income start date adjustment, an optional 1–4% annual increase, and payment
acceleration as the only in-force liquidity. **A third carrier's design** [S4] [S5] is the extended case,
adding commutation. The **QLAC overlay** is a restriction set on the base case.

**Structural warning, up front.** A DIA has **no account value** — no credited rate, no index crediting, no
M&E or rider charge, no surrender charge, no free-withdrawal corridor, no market value adjustment, no benefit
base, no interim value. See "Parameters that do not exist for this product"; do not carry empty parameter
tables for them. **Income-phase mechanics are not restated here:** once income begins a DIA *is* a
single-premium immediate annuity, and payout forms, refund mechanics, survivor reduction, COLA escalation and
survivorship weighting are specified in `products/immediate_annuity/product-spec.md` and
`products/immediate_annuity/technical-notes.md`. This document specifies the **deferral phase**, the
**transition to income** and the **QLAC overlay**.

---

## Product overview and market role

VM-01 defines a DIA as "an annuity contract that guarantees a periodic payment for the life of the annuitant
or a term certain and payments begin 13 months or later from the issue date if the contract holder and/or
annuitant survives to a predetermined future age" [R9]. The Insurance Compact's uniform standard states the
same architecture contractually: an individual deferred paid-up non-variable annuity "with no cash surrender
values prior to the commencement of annuity payments", single or flexible premiums, "specified income
payments beginning on a specified income commencement date for each premium paid", all funds in the general
account [R13].

The fact that drives every modeling decision: **each premium immediately and irrevocably buys a fully
guaranteed paid-up annuity** — "All income benefits, based on the specified income commencement date and
specified income option associated with each premium paid, shall be guaranteed" [R13 §3.H(1)](#uslib-deferred_income_annuity-r13) — and the
slices are combined into one payment stream at the income start date [S1] [S2] [S3] [S4]. One carrier states it
plainly: "Each payment purchases a specific amount of guaranteed lifetime income, based on annuity purchase
rates that are in effect at the time each purchase payment is made" [S3].

The contract states **dollars of income, not rates**, and the Compact expressly relieves the insurer of
disclosure: "Since the premium and income benefit are fully defined in the contract, the mortality table and
interest rate used in the deferral period and for determining the contractually specified income payable do
not need to be disclosed in the contract or the Actuarial Memorandum" [R13 §1.B(1)(a)](#uslib-deferred_income_annuity-r13). No purchase-rate
table or income-per-$100,000 figure was obtained from any source, so the purchase-rate function in
`technical-notes.md` is an explicit **[std]** construction. The product is sold as pure longevity insurance
with no fees and no market performance to track, to a client "between the ages of 50 and 65 and ready to
retire in five to 10 years" with "$250,000 and $1.5 million" in investable assets [S2]; the qualified-money
variant, the QLAC, additionally removes the contract's value from the RMD account balance [R4] [R5].

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Flexible-premium deferred paid-up non-variable annuity; general account only; irrevocable | [R13] [S2] [S3] |
| Participation | Non-participating (no dividends) | **[std]** (1) |
| Contract nature | No cash surrender value, no withdrawals, no loans before the income start date | [S1] [S2] [R13 §3.P](#uslib-deferred_income_annuity-r13) |
| Market types | Nonqualified; Traditional / Roth / SEP / Custodial IRA; QLAC IRA and Custodial QLAC IRA | [S2] [S4] |
| Market type — base model | Nonqualified, with QLAC as an overlay switch | scope **[std]** (2) |
| Age basis | Age nearest birthday ("74 years, six months and one day old ⇒ contract issue age 75") | [S2] |
| Minimum issue age (annuitant) | 22 | [S2] [S4] |
| Maximum issue age — nonqualified and Roth IRA | 85 | **[std]** (3) |
| Maximum issue age — traditional IRA | 73 | **[std]** (4) |
| Issue ages — QLAC | 41–83 | [S2]; band **[std]** (5) |
| Annuitants | Up to two; cannot be changed after issue; joint annuitant must be a spouse | [S2] [S4] |
| Income option | Elected at issue; cannot be changed thereafter | [S1] [S2] [S4] |
| Anchor model cell | Female 60 ANB, nonqualified, $100,000 at issue + $50,000 at policy year 6, income start age 80, Life with Cash Refund, monthly | **[std]** (6) |

1. No retrieved product is participating. The Compact contemplates one, pricing dividend-purchased income
   either on "current annuity purchase rates" or on the rates used for the related premium [R13 §3.T](#uslib-deferred_income_annuity-r13); a
   participating form would also lose the Model #245 §3.A exemption (Regulatory context) [R11].
2. All four insurers issue both [S1] [S2] [S3] [S4]. The nonqualified form carries the fullest feature set
   (acceleration and commutation are nonqualified-only [S1] [S2] [S4]), so QLAC is modeled as a restriction set.
3. Observed: 80 [S1] [S3], 85 [S4], 88 [S2]; 80–88 across [S6]. 85 coincides with the modal maximum
   income-start age (footnote 11) and the QLAC ceiling, keeping one age cap in the model rather than three.
   It is not the binding constraint: the 13-month minimum deferral (footnote 9) together with the age-85
   income-start cap (footnote 11) makes the **effective** maximum issue age **83 ANB** — the same ceiling the
   QLAC band carries (footnote 5) — so the 85 row never binds on its own.
4. Observed: 68 [S3, 2018], 69 [S2, 2019] — both pre-SECURE-vintage documents keyed to an RMD age of 70½ and
   superseded by the current applicable RMD ages of 73/75 [S1] [S4] — 71 [S4], 73 [S1] [S6]. 73 is
   the post-SECURE representative; the mechanism behind it is the rule that issue age is "no later than
   2 years before the client's RMD age" [S1].
5. Observed minima 31 [S3], 35 [S1], 41 [S2]; maxima 80 [S1], 82 [S3] [S4], 83 [S2] [S6]. The archetype's band
   is adopted. The minimum is purely a product rule — the regulation sets only the age-85 outside date
   [R1 (q)(1)(ii)](#uslib-deferred_income_annuity-r1).
6. Pure modeling choice, carried identically into `technical-notes.md`. Age 60 with a 20-year deferral sits
   inside the stated target market [S2]; two premiums exercise the slice mechanic; Cash Refund is permitted on
   both nonqualified contracts and QLACs [S2].

### Premium

| Parameter | Representative value | Basis |
|---|---|---|
| Premium pattern | Flexible: any number of premiums during the deferral period | [S2] [S3] [S4] [R13] |
| Minimum initial premium | $10,000 | [S1] [S2] [S3] [S6] |
| Minimum subsequent premium | $500 | **[std]** (7) |
| Maximum cumulative premium without home-office approval | $1,500,000 | **[std]** (8) |
| Cut-off for subsequent premiums | None accepted within **13 months** of the income start date | [S2] [S4] |
| Cut-off for 1035 exchanges / transfers | 16 months before the income start date | [S4] |
| Pricing of each premium | Company's then-current annuity purchase rates, by attained age, income start date and income option | [R13 §3.B(1)(b)](#uslib-deferred_income_annuity-r13) [S3] |
| Floor on current purchase rates | Income purchased must be not less than that in a new contract of the same class, attained age and commencement date | [R13 §3.B(1)(c)](#uslib-deferred_income_annuity-r13) |
| Confirmation of each subsequent premium | Premium, additional income purchased, option and start date, within **30 days** | [R13 §3.B(1)(d)](#uslib-deferred_income_annuity-r13) |
| Free look on each subsequent premium | Cancel by returning the confirmation within **10 calendar days**; premium refunded | [S2] [S3] [R13 §3.B(1)(d)](#uslib-deferred_income_annuity-r13) |
| Minimum monthly income payment | $100 | [S2] |
| QLAC aggregate premium limit — 2026 | $210,000 | [R3] [S4] |
| Aggregation of cumulative-premium limits | Across all DIAs of the insurer group with the same owner or annuitant | [S2] |

7. Observed: $100 [S1] [S3], $500 [S2] [S4]. $500 is taken with the archetype and the extended case
   [S2] [S4] because it produces materially fewer slices in a flexible-premium projection; the choice
   changes no mechanic.
8. Observed: $1,000,000 [S3], $1,500,000 [S2], $2,000,000 [S1] [S4]. The archetype's value is taken. All four
   are soft limits — larger amounts require home-office approval, not prohibition [S1] [S2] [S3] [S4].

### Deferral period and income start date

| Parameter | Representative value | Basis |
|---|---|---|
| Minimum deferral | **13 months** from contract issue | **[std]** (9) |
| Maximum deferral | **30 years** from contract issue | **[std]** (10) |
| Maximum income start age — nonqualified and Roth | **85** | **[std]** (11) |
| Maximum income start — traditional IRA | April 1 of the year following the year the owner attains the applicable RMD age (73, or 75 for owners born in 1960 or later) | [S1] [S4] |
| Income start ceiling — QLAC | Annuity starting date no later than the first day of the month next following the 85th anniversary of the owner's birth | [R1 (q)(1)(ii)](#uslib-deferred_income_annuity-r1) [S1] [S2] [S3] [S4] [REG-R57] |
| Income start floor — QLAC | After the required beginning date. This is a **product** rule, not a QLAC rule — the regulation sets no earliest commencement date | [S1] [S2] |
| Income start day of month | Any day between the 1st and the 28th | [S2] |
| Payment frequency menu | Monthly, quarterly, semiannual, annual | [S1] [S2] [S3] [S4] |
| Payment frequency — base model | Monthly, fixed at issue, not changeable | [S1] [S2]; choice **[std]** (12) |
| Payment timing — base model | Arrears (payment at the end of each payment period) | **[std]** (13) |

9. Two conventions coexist: **13 months** [S2] [S4], matching the VM-01 statutory floor [R9] and the Florida
   annuitization mandate [S2]; **24 full months** [S1] [S3]. The current distributor table lists one of those
   two carriers at 13 months [S6] — a conflict the research file could not resolve because no current
   primary document for that carrier could be retrieved [S9] [S11]; both figures stand on the record.
   13 months is chosen as the regulatory minimum and the more common design.
10. Observed: 30 years [S2] [S4], 40 years [S1] [S3], both across five insurers [S6]. 30 is taken with the
    archetype; in practice the maximum income-start age binds first.
11. Observed: 85 [S1] [S3] [S6], 90 [S2] [S4]. 85 is modal, matches the regulation-fixed QLAC ceiling
    [R1 (q)(1)(ii)](#uslib-deferred_income_annuity-r1) and keeps one age cap across market types (footnote 3).
12. All four insurers offer all four frequencies [S1] [S2] [S3] [S4]. Fixed at issue at two of them [S1] [S2] —
    it cannot change even on an annuity-date adjustment [S2] — but changeable at a third [S3]. The
    fixed-at-issue convention is adopted.
13. No retrieved DIA document states advance versus arrears. Arrears matches
    `products/immediate_annuity/product-spec.md` so one payout chassis serves both products; the model
    exposes `pay_timing ∈ {advance, arrears}`.

### Income start date adjustment (the principal in-force option)

| Parameter | Representative value | Basis |
|---|---|---|
| Direction and magnitude | One-time change, up to **5 years earlier or 5 years later** | [S1] [S2] [S3] [S4] |
| Number of exercises | Once over the life of the contract; new date irrevocable | [S2]; count **[std]** (14) |
| Floor on the new date | At least **13 months** after the most recent premium payment | [S1] [S2] [S3] [S4] |
| Ceiling on the new date | Within the maximum deferral period and the maximum income-start age | [S1] [S2] [S4] |
| What cannot change | Income option; day of month; payment frequency | [S1] [S2] |
| Minimum resulting payment | $100 monthly | [S2] |
| Excluded forms | Life Only and Joint Life Only; one carrier additionally excludes Joint and Survivor Life Only and Period Certain | [S1] [S3] [S4] |
| Repricing basis | Originally scheduled payment; new annuity date; **Moody's Seasoned Baa Corporate Bond Yield** at the request date; **Annuity 2012 Mortality Table**; plus an **interest rate change adjustment set forth in the contract** | [S2] (another carrier states the same construction against the **A2000** tables [S1]) |
| Direction of income impact | Advancing the date **reduces** the payment; deferring **increases** it | [S4] [S5] |
| Explicit charge for the change | None disclosed; any charge must be disclosed | [S1] [S2] [S3] [S4] [R13 §§3.M, 1.B(1)(d)](#uslib-deferred_income_annuity-r13) |

14. One-time at all four insurers [S1] [S2] [S3] [S4]; one of them adds a one-time right to accelerate back
    after a deferral [S3]; **a further carrier in the distributor comparison allows two changes**, the only
    multi-change design identified [S6]. One exercise is adopted and the count is exposed.

### Income options (payout forms)

| Parameter | Representative value | Basis |
|---|---|---|
| Single-life forms | Life Only (no death benefit in either phase); Life with Cash Refund; Life with Installment Refund; Life with Period Certain | [S2] [S4] |
| Unbundled variant | Life Only **with 100% Return of Purchase Payments Death Benefit** — ROP in deferral, pure life annuity after income start | [S4] |
| Period certain range | 10–30 years | [S2]; range **[std]** (15) |
| Joint forms | Each single-life form in a joint version with survivor reduction | [S2] [S4] |
| Survivor percentage menu | 50%, 66⅔%, 75%, 100% | [S1] [S2] [S4]; menu **[std]** (16) |
| Reduction trigger | Switch: reduction on the death of **either** annuitant, or of the **primary** annuitant only | [S1] [S2] [S4] |
| Joint × certain-period interaction | If the first annuitant dies inside a guaranteed period, payments to the survivor are **not reduced until the end of that period** | [S1] [S3] |
| Convertible joint | Switch; convertible options guarantee **two** payouts — joint, and the corresponding single-life payout on conversion — so the joint payout is **lower** | [S2]; base = non-convertible **[std]** (17) |
| Convertible joint — period certain limit | 10 years | [S2] |
| Refund mechanics | Cash Refund: lump-sum shortfall of premiums over payments made. Installment Refund: payments continue in the same amount and frequency until they equal the premiums. Period Certain: payments continue to the end of the certain period. Beneficiary may elect the present value instead under Installment Refund and Period Certain | [S1] [S2] [S3] |
| Compact framing of refunds | Income payments made before a return-of-premium death benefit "shall be considered period certain income" | [R13 definitions](#uslib-deferred_income_annuity-r13) |

15. Observed: 5–30 years [S1 period-certain-only, S3], 10–30 years [S1 life-with-guarantee, S2], up to 30
    years [S4]. The Compact floor is five years minimum with a twenty-year maximum deferral for a
    period-certain-only contract [R13 §3.H(3)](#uslib-deferred_income_annuity-r13). 10–30 is taken with the archetype; period-certain-only is out
    of base scope.
16. Observed: 100/66⅔/50% [S1]; ½, ⅔, ¾ [S2]; 50/67/75% [S4]. The union {50, 66⅔, 75, 100} is adopted, which
    is exactly the set carried in `products/immediate_annuity/product-spec.md` so the two payout chassis
    share one menu; 100% must be retained because it is the *only* continuance one carrier permits on a joint
    Cash Refund form [S1] — the joint counterpart of the anchor cell's payout form.
17. Non-convertible is the simpler pricing equation and the default at three of four insurers. One carrier
    alone exposes the distinction and its pricing consequence [S2] — the most model-relevant pricing subtlety
    in the family — and it is specified as a switch in `technical-notes.md`.

### Death benefit during the deferral period (the central design fork)

| Parameter | Representative value | Basis |
|---|---|---|
| Base form | **100% return of premiums paid, no interest**, lump sum | [S1] [S2] [S3] [S4] [R13 §3.I(1)(a)](#uslib-deferred_income_annuity-r13) |
| Applies to | All income options **except** Life Only and Joint Life Only | [S1] [S3] [S4] |
| No-death-benefit form | Single Life — No Death Benefit: no death benefit before or after the income start date | [S2] |
| No-death-benefit form — conditions | Deferral period of **10 years or longer**; income start date **cannot be changed**; state restrictions apply | [S2] (18) |
| Trigger | Death of the owner (or of the annuitant where the owner is a non-natural person) | [S1] [S3] [S4] |
| Permitted calculation methods | (a) percentage of premiums paid; (b) percentage of premiums paid plus interest; (c) flat dollar amount; (d) any combination | [R13 §3.I(1)](#uslib-deferred_income_annuity-r13) |
| Application to subsequent premiums | Must be provided for both the initial premium and any additional premiums | [R13 §3.I(2)](#uslib-deferred_income_annuity-r13) |
| Charges used in determining the death benefit | None disclosed in any retrieved source; any such charge must appear on the specifications page | [S1] [S2] [S3] [S4] [R13 §2.B(2)](#uslib-deferred_income_annuity-r13) |
| Spousal continuation | Where the surviving spouse is joint annuitant and sole primary beneficiary the contract may continue instead of paying the benefit; on non-convertible continuation **no further premiums are allowed** | [S1] [S2] [S4] |
| Terminal-illness acceleration | Death benefit payable on diagnosis with life expectancy of 12 months or fewer (except Life Only forms) | [S4]; out of base scope |
| Cover-page disclosure — no death benefit | "The contract does not provide access to funds prior to the income commencement date. No death benefit is available to a beneficiary if the annuitant dies prior to the income commencement date." | [R13 §2.A(8)](#uslib-deferred_income_annuity-r13) [R10 §9](#uslib-deferred_income_annuity-r10) |
| Cover-page disclosure — with death benefit | "The contract does not provide access to funds prior to the income commencement date other than payment of the death benefit." | [R13 §2.A(9)](#uslib-deferred_income_annuity-r13) |

18. The research file records an unresolved internal inconsistency: the option is said to be unavailable in
    "Connecticut or New York" in the body of the archetype guide and in "Connecticut or Florida" in its
    footnotes and product highlights [S2]. Both stand; neither is asserted. Separately, **no source offered a
    "percentage of premiums plus interest" deferral death benefit**, though the Compact permits it
    [R13 §3.I(1)(b)](#uslib-deferred_income_annuity-r13).

### Annual increase (COLA)

| Parameter | Representative value | Basis |
|---|---|---|
| Menu | 1%, 2%, 3% or 4% | [S2]; menu **[std]** (19) |
| Base model election | None (0%); 2% in the COLA variant | scope **[std]** (19) |
| Mechanics | Fixed compound increase on each anniversary of the income start date | [S2] [S3] [S4] |
| Election | At issue only; cannot be cancelled or changed | [S1] [S2] [S3] [S4] |
| Trade-off | Initial payments are smaller than on an otherwise identical contract | [S1] [S2] [S4] |
| Age condition | Owner at least 59½ at the first income payment | [S1] |
| Availability on QLAC | Not offered | [S1] [S3] [S4] (20) |
| Availability on other qualified contracts | May be limited or unavailable because of RMD rules | [S2] [S3] [S4] |
| Index linkage | None — every observed option is a fixed compound escalator, not CPI-linked | [S1] [S2] [S3] [S4] |

19. Observed: 1–3% [S1, and one further carrier per S6], 1–4% [S2], 2/3/4% [S4], 1–5% [two carriers per
    S6]. The archetype's 1–4% is adopted; the base model runs at 0% so the payout stream is level, and
    exposes `cola_rate`.
20. **Correction worth stating:** a QLAC "does not fail" the not-variable/not-indexed requirement "merely
    because it provides for a cost-of-living adjustment as described in paragraph (o)(2)" [R1 (q)(4)(iv)](#uslib-deferred_income_annuity-r1).
    The market is more restrictive than the regulation — three of the four carriers exclude COLA from
    their QLAC offering [S1] [S3] [S4] and the fourth limits it on qualified contracts [S2].

### Liquidity

| Parameter | Representative value | Basis |
|---|---|---|
| Cash surrender value | **None**, at any time before the income start date | [S1] [S2] [R13 scope](#uslib-deferred_income_annuity-r13) |
| Withdrawals before income start | **None** | [S1] [S2] |
| Loans | **Prohibited** by the uniform standard | [R13 §3.P](#uslib-deferred_income_annuity-r13) |
| Payment acceleration — amount | Next scheduled monthly payment plus five subsequent payments = **six months of income in one sum**; no payments for the following five months | [S1]; three-or-six variant [S2] [S4] |
| Payment acceleration — uses | **2** over the life of the contract | **[std]** (21) |
| Payment acceleration — conditions | Owner at least 59½; monthly frequency; nonqualified only; at least one regular payment between uses | [S1] [S2] [S4] |
| Payment acceleration — characterization | Expressly "not a liquidity feature" — a timing shift, not a withdrawal | [S2] |
| Payment acceleration on QLAC | Not available | [S4] |
| Commutation — base model | Not offered | [S1] [S2] [S3] |
| Commutation — extended model | Up to **100% of the present value of remaining guaranteed income payments**; nonqualified only; 59½ or older; **an interest-rate adjustment charge applies**; no limit on the number of withdrawals; life-contingent tail preserved (payments resume at the end of the would-be guaranteed period if the annuitant is living) | [S4] [S5] |
| Commutation — regulatory frame | Lump sum only; non-commuted benefits unaffected; must be an actuarial present value; the interest rate "can be adjusted for changes in interest rates … between the issue date and the commutation date", intended "to reduce interest risk in the event of rising interest rate after issue" | [R13 §§3.F(1)–(7)](#uslib-deferred_income_annuity-r13) |
| Commutation on QLAC | Prohibited after the required beginning date, other than a rescission right not exceeding 90 days from purchase | [R1 (q)(1)(iv)](#uslib-deferred_income_annuity-r1) [R2 §202(a)(4)](#uslib-deferred_income_annuity-r2) [REG-R57] |
| Feature interlocks | Six-month waiting periods interlock acceleration, commutation and the start-date adjustment in both directions | [S4] |

21. Observed: 1 use [S3], 2 uses [S1] [S4], 5 uses [S2]. Two is modal and is adopted; the count is a parameter.
    Eligibility also differs — one carrier requires a guarantee or cash-refund period with at least six months
    remaining [S3], and another requires the acceleration period to fall in the same tax year on
    qualified contracts [S4].

### Parameters that do not exist for this product

An implementer arriving from a fixed, indexed or variable deferred annuity chassis will look for the
following and must not find them. Their absence is a structural feature confirmed at contract level, not a
research gap [S1 fn.1] [S2 product highlights] [S4] [R13].

| Parameter class | Status |
|---|---|
| Account value / accumulation value | **Does not exist.** "There is also no accumulation or cash value … and, therefore, no liquidity" [S2] |
| Credited or declared interest rate; guaranteed minimum crediting rate | **Do not exist.** The contract states dollars of income, and the deferral-period interest and mortality basis need not be disclosed at all [R13 §1.B(1)(a)](#uslib-deferred_income_annuity-r13) |
| Index crediting parameters — caps, participation rates, spreads, buffers, floors, index terms | **Do not exist.** The product is non-variable and non-indexed; a QLAC is additionally *required* not to be indexed [R1 (q)(1)(vii)](#uslib-deferred_income_annuity-r1) |
| M&E charge, administrative charge, contract fee, rider charges | **Do not exist.** No retrieved document discloses any explicit charge — "There are no fees" [S2]. Pricing margin is embedded in the purchase rate [R13 §1.B(1)(a)](#uslib-deferred_income_annuity-r13) |
| Surrender charge schedule; free-withdrawal corridor | **Do not exist.** There is nothing to surrender [S1] [S2] [R13] |
| Market value adjustment | **Does not exist.** The nearest analogue is the interest-rate adjustment on commutation in the extended case [S4] [R13 §3.F(7)](#uslib-deferred_income_annuity-r13) |
| Benefit base, roll-up, step-ups, withdrawal percentages by attained-age band | **Do not exist.** There is no living-benefit rider layer; the income guarantee *is* the contract |
| Interim value | **Does not exist** (an AG 54 concept for index-linked variable annuities [REG-R44]) |
| Lapse / surrender assumption | **Not applicable.** For contracts with "no account value or surrender benefit, such as some contracts within the Payout Annuity Reserving Category …, this section is not applicable" [R9] |
| Annuitization rate assumption | **Prescribed at 0%** at all projection intervals [R9]; the contract annuitizes by construction at the income start date |
| Policy loan parameters | **Prohibited** [R13 §3.P](#uslib-deferred_income_annuity-r13) |
| Premium / persistency bonus | Not offered by any retrieved product [S1] [S2] [S3] [S4] |

The only non-guaranteed quantity in the product is the **current annuity purchase rate applied to a future
premium** [R13 §3.B(1)(b)–(c)](#uslib-deferred_income_annuity-r13), and even that is floored at the rate a new contract of the same class
receives.

---

## Contractual mechanics

**Premium and the income-slice mechanic.** Each premium *k* paid at time *t\_k* generates a paid-up annuity
priced on "the attained age of the annuitant, the specified income commencement date and specified income
option, and the company's then current annuity purchase rates" [R13 §3.B(1)(a)–(b)](#uslib-deferred_income_annuity-r13), so the guaranteed annual
income at the income start date is

    B  =  sum over k of  P_k  x  pr( x + t_k , T - t_k , f )

with `pr(.)` the purchase rate (annual income per dollar of premium), `x + t_k` the attained age at payment,
`T - t_k` the remaining deferral and `f` the income option elected at issue. Because purchase rates are set
at each payment and are never published, `pr(.)` is a **[std]** construction — see `technical-notes.md`.

**Deferral-phase death benefit.** On death of the owner (or of the annuitant where the owner is an entity)
before the income start date the benefit is a lump-sum return of premiums paid, without interest
[S1] [S2] [S3] [S4]:

    DB_deferral  =  100%  x  (cumulative premiums paid to the date of death)

payable on every option except Life Only and Joint Life Only, which carry **no death benefit either before or
after** the income start date [S1] [S3] [S4]. Economics of the fork: with ROP, deferral mortality is close to
neutral (the premium comes back); without it, deferral deaths release the entire reserve as mortality gain —
which is why the no-death-benefit form buys materially more income for the same premium and why it is
conditioned on a deferral of ten years or longer [S2; derived from S1–S4, R13].

**Income start date adjustment.** Payments are recalculated on actuarial-equivalence inputs one carrier
discloses in full: "Your originally scheduled annuity payment; the new annuity date; Moody's Seasoned Baa
Corporate Bond Yield rate at the time we receive the annuity date change request; the Annuity 2012 Mortality
Table; an interest rate change adjustment set forth in the contract" [S2]; another states the same construction
against the A2000 tables [S1]. Advancing reduces the payment, deferring increases it [S4] [S5]. Where a change
right is granted the contract must disclose the alternatives, the timing and frequency limits and any
explicit charge, and must **either** state the mortality and interest assumption used for actuarial
equivalence **or** contain a table of alternative income benefits [R13 §§3.M, 3.H(1)](#uslib-deferred_income_annuity-r13).

**Transition to income.** On the income start date the slices are paid as one stream in the form elected at
issue [S1] [S2] [S3] [S4] and the contract becomes a SPIA — mechanics in
`products/immediate_annuity/product-spec.md`. Two DIA-specific carry-overs: the **refund base is
cumulative premiums paid**, not a single premium [S2] [S4]; and the Compact treats income payments made before
a return-of-premium death benefit as **period certain income** [R13 definitions](#uslib-deferred_income_annuity-r13), which is what lets a
cash-refund or installment-refund DIA be valued as a life annuity with a derived certain period.

**Payment acceleration and commutation.** Acceleration is a timing shift, not a withdrawal — expressly "not a
liquidity feature" [S2]. Its 59½ gate exists because of the IRC §72(q) 10% additional tax [R8]; one carrier warns
that exercising it on a policy purchased before 59½ can trigger that tax retroactively, plus interest, on
payments received before 59½ [S1]. Commutation exists only in the extended case, and, distinctively, "except
for the Period Certain option, if you are still living at the end of the period when your guaranteed income
payments would have stopped", the insurer resumes income payments until death — the life-contingent
tail survives commutation [S4]. **The interest-rate adjustment formula is not published in any retrieved
document** [S4] [S5]; the Compact supplies only the principle [R13 §3.F(7)](#uslib-deferred_income_annuity-r13), so the construction in
`technical-notes.md` is **[std]**/[unverified].

**QLAC overlay.** The same contract in qualified money under the seven conditions of §1.401(a)(9)-6(q)(1):
the premium limitation; commencement no later than the first day of the month next following the 85th
anniversary of birth; RMD compliance after commencement; **no commutation benefit, cash surrender right or
other similar feature after the required beginning date** (other than a rescission right not exceeding 90
days from purchase); no death benefits other than those in (q)(3); a statement that the contract is
**intended to be a QLAC**; and that it is **not variable under section 817, indexed, or similar**
[R1] [REG-R57]. Specifics:

- **Premium limit** $200,000 as enacted, indexed (base period the calendar quarter beginning **July 1, 2022**,
  increments rounded to the **next lowest multiple of $10,000**); **$210,000 for 2026**, unchanged from 2025
  [R1 (q)(2)(ii), (q)(4)(ii)(A)](#uslib-deferred_income_annuity-r1) [R2 §202(a)(2)](#uslib-deferred_income_annuity-r2) [R3], independently confirmed by a carrier document [S4]. The limit
  is reduced by premiums paid to this contract and to any other contract intended to be a QLAC under any
  401(a), 403(a), 403(b), 408 or governmental 457(b) arrangement [R1 (q)(2)(ii)(B)](#uslib-deferred_income_annuity-r1); the issuer may rely on
  the owner's written representation [R5 (h)(2)](#uslib-deferred_income_annuity-r5). **The percentage-of-account-balance limit is gone** —
  SECURE 2.0 § 202(a)(1) directed Treasury to eliminate the 25% requirement and the codified text now
  contains only a dollar limitation [R1] [R2], so pre-2023 documents stating 25% and $130,000 are superseded
  [S2].
- **Permitted death benefits** are exhaustive [R1 (q)(3)](#uslib-deferred_income_annuity-r1): a life annuity to a sole-beneficiary surviving
  spouse not exceeding 100% of the employee's payment; a life annuity to another beneficiary not exceeding
  the applicable percentage; or, in lieu of a life annuity, a **return of premiums** "up to the amount by
  which the premium payments made with respect to the QLAC exceed the payments already made under the QLAC",
  payable by the end of the calendar year following the year of death and treated as an RMD (not
  rollover-eligible) where death is after the required beginning date [R1 (q)(3)(v)](#uslib-deferred_income_annuity-r1). **The applicable
  percentage is 0 where the contract provides a return of premium** [R1 (q)(3)(iii)(C)](#uslib-deferred_income_annuity-r1) — so a QLAC carries a
  ROP death benefit **or** a beneficiary life annuity, never both. The contract's value is excluded from the
  RMD account balance [R4], a rule that applies to IRAs but **not to a Roth IRA** [R5] [R5 (h)(4)](#uslib-deferred_income_annuity-r5).
- **Market implementation and failure modes.** The archetype permits only Single Life — No Refund, Cash Refund
  and No Death Benefit plus Joint and Survivor — Cash Refund, excluding Installment Refund and Period Certain
  [S2]; the extended case likewise excludes Period Certain and Installment Refund [S4]; a further carrier excludes
  guarantee periods and subsequent premiums [S3]; commutation, acceleration and inflation protection are all
  off [S4]. An excess premium ends QLAC status **on the date paid** unless returned to the non-QLAC portion of
  the account by the end of the following calendar year (returning it is not a prohibited commutation)
  [R1 (q)(4)(i)(B)](#uslib-deferred_income_annuity-r1); any other failure voids status **retroactively to the date of purchase**
  [R1 (q)(4)(iii)(A)](#uslib-deferred_income_annuity-r1). A joint-and-survivor QLAC survives a post-purchase, pre-commencement divorce under
  QDRO conditions [R1 (q)(3)(vii)](#uslib-deferred_income_annuity-r1) [R2 §202(a)(3)](#uslib-deferred_income_annuity-r2), retroactive to contracts purchased on or after July 2,
  2014 [R2 §202(c)(1)(B)](#uslib-deferred_income_annuity-r2); the archetype's pre-SECURE-2.0 guide shows the old, harsher treatment and illustrates
  what changed [S2].

---

## Riders and options

**In scope (modeled, or modeled as switches):** annual increase / inflation protection option (COLA), 1%–4%
compound on each income-start anniversary, elected at issue and irrevocable [S1] [S2] [S3] [S4], base 0%;
annuity date adjustment rider / income start date adjustment option, one-time ±5 years with repricing
[S1] [S2] [S3] [S4]; payment acceleration [S1] [S2] [S3] [S4]; commutation / withdrawal of guaranteed income
payments, extended case only [S4] [S5]; the QLAC endorsement — the statement of intent required by
[R1 (q)(1)(vi)](#uslib-deferred_income_annuity-r1) plus the restriction set above [S2] [S4]; and the deferral-phase death benefit switch (ROP vs
none), which is the product's central pricing fork rather than a rider proper [S1] [S2] [S3] [S4].

**Out of scope (described, not modeled):** terminal-illness acceleration of the death benefit [S4]; spousal
continuation and beneficiary-IRA continuation, including the QLAC rules that spousal continuances are not
allowed and that a spouse keeping the contract holds it as a spousal beneficiary IRA with no new premiums
[S2]; custodial QLAC IRA forms where payee and beneficiary must be the custodian [S2]; participating /
dividend forms [R13 §3.T](#uslib-deferred_income_annuity-r13); misstatement of age or sex adjustments, corrected at interest "not exceeding 6%"
[R13 §3.R](#uslib-deferred_income_annuity-r13); up to ten payees per contract [S2]; evidence-of-survival requirements [R13 §3.L](#uslib-deferred_income_annuity-r13); the
beneficiary's election of the present value of remaining payments [S1] [S2] [S3]; the ten-day free look on each
subsequent premium, carried as a cancellation flag only [S2] [S3] [R13 §3.B(1)(d)](#uslib-deferred_income_annuity-r13); and state overrides
(Florida's mandate that the **annuity date** be advanceable on all options — including the No-Refund options —
to as early as 13 months after issue, which is a start-date-adjustment override and not the payment
acceleration feature [S2];
the extended-case product unavailable in CA, IL, NC, OR, PA and TX, its start-date adjustment unavailable in
CT and NY, and its commutation unavailable in MO [S4]).

---

## Variations across insurers

1. **Minimum deferral — 13 vs 24 months.** 13 [S2] [S4], matching VM-01 [R9]; 24 full months [S1] [S3], against
   13 months for one of those two carriers in the current distributor table [S6] — unresolved [S9] [S11].
   **Chosen: 13 months**, the regulatory minimum and the more common design.
2. **Maximum deferral — 30 vs 40 years.** 30 at three of the six products surveyed; 40 at the other three
   [S1] [S2] [S3] [S4] [S6]. **Chosen: 30**, with the archetype; the income-start age binds
   first.
3. **Maximum income-start age — 85 vs 90 (nonqualified).** 85 at four of the six products surveyed;
   90 at the other two [S1] [S2] [S3] [S4] [S6]. **Chosen: 85** — also the regulation-fixed QLAC
   ceiling [R1], so the model carries one age cap.
4. **Deferral death benefit packaging.** All four default to 100% ROP [S1] [S2] [S3] [S4]; what varies is the
   no-death-benefit corner — implicit in a Life Only election [S1] [S3] [S4], an explicit option conditioned on
   a 10+ year deferral [S2], or fully unbundled [S4]. **Chosen: the unbundled treatment as the model's
   parameterization** (a `db_form` switch independent of the payout form, which makes the two mortality
   exposures independent), while the representative *product* defaults to ROP on every option but Life Only.
5. **Income start date adjustment.** Uniform ±5 years, one time [S1] [S2] [S3] [S4], with one carrier's
   accelerate-back right [S3] and another's two changes [S6] as exceptions; Florida forces
   acceleration on all options [S2] and the extended-case product cannot offer it in CT or NY [S4].
   **Chosen: one-time ±5 years on the archetype's repricing recipe**, the only fully disclosed one [S1] [S2].
6. **COLA range — 1% to 5% across the market.** 1–3% [S1]; 1–4% [S2]; 1–5% [S3 per S6]; 2/3/4% [S4]; all
   fixed compound escalators elected at issue, none CPI-linked. **Chosen: 1–4%**, base model 0%.
7. **Post-income liquidity.** Acceleration everywhere but with different limits — 2 uses / 6 months [S1];
   5 / 3 or 6 [S2]; 1 use and only with a guarantee or refund period with ≥6 months left [S3]; 2 / 3 or 6
   [S4]. Only one carrier offers true commutation [S4] [S5]. **Chosen: 2 uses of a six-month acceleration in
   the base case, commutation only in the extended case** — the single largest liability-modeling difference
   across the four products.
8. **Joint reduction trigger and convertibility.** Reduction on the death of either annuitant versus of the
   primary annuitant coexist [S1] [S2] [S4]; one carrier alone exposes convertible vs non-convertible and states
   that convertible joint payouts are lower because they *also* guarantee a single-life payout if one
   annuitant dies during deferral [S2]. **Chosen: non-convertible base with a convertible switch**, trigger
   likewise a switch, matching the immediate-annuity chassis.
9. **Minimum premium.** $10,000 at four of five products [S1] [S2] [S3] [S6]; the fifth alone $15,000 [S4].
   Subsequent minima split $100 [S1] [S3] vs $500 [S2] [S4]. **Chosen: $10,000 / $500.**
10. **Source-vintage caveat.** The archetype guide is 2019 and its QLAC figures ($130,000, 25% of balance, RMD
    age 70½) are superseded [S2] [R1] [R2] [R3]; the current guide could not be retrieved [S8]. A second
    carrier's fact sheet is January 2018 and references RMD age 70½ [S3]. The current-vintage primary sources
    are a June 2026 product overview [S1] and a February 2026 fact sheet [S4]. Two further carriers'
    parameters come only from a distributor comparison [S6] [S9]. *Mechanics* are stable across these vintages; *tax and age parameters*
    follow the current-law sources [R1] [R2] [R3].

---

## Regulatory context

**NAIC Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805).** It **does** apply during
deferral — the Section 2 exclusions cover immediate annuities and "any deferred annuity contract after
annuity payments have commenced", and a DIA before the income commencement date is in none of them [R10]. The
cash-surrender requirement is conditional, biting only "if a contract provides for a lump sum settlement at
maturity, or at any other time" [R10 §3.A(2)](#uslib-deferred_income_annuity-r10), so a contract that never offers a lump sum never triggers it;
what *is* triggered is the paid-up annuity benefit [R10 §3.A(1)](#uslib-deferred_income_annuity-r10), satisfied by construction [R13 §3.H(1)](#uslib-deferred_income_annuity-r13),
with Section 7 governing its valuation and Section 9 forcing the prominent disclosure realized as the
Compact's cover-page language [R10] [R13 §§2.A(8)–(9)](#uslib-deferred_income_annuity-r13). **Correction to a common misstatement:** the Model
#805 indexed nonforfeiture interest rate is the lesser of 3% and the five-year Constant Maturity Treasury
rate (rounded to the nearest 1/20th of one percent) **reduced by 125 basis points, subject to a floor of 15
basis points (0.15%)** — **not** a 1% floor [REG-R42]. The research file left "floored at 1%" [unverified]
because its own extract did not capture Section 4.B [R10]; the fully fetched text settles it at 15 bp
[REG-R42]. Largely academic here — a DIA has no cash value and the minimum nonforfeiture amount (net
considerations of 87.5% of gross, less a $50 annual contract charge and other stated items
[REG-R42] [R10 §4.A(1)](#uslib-deferred_income_annuity-r10)) never binds — but the number should not be propagated wrongly.

**IIPRC uniform standard IIPRC-A02-I-LONG.** The Compact's "Individual Deferred Paid-Up Non-Variable Annuity
Contract Standards (Commonly Marketed as Deferred Income Annuities or Longevity Annuities)", adopted
August 5, 2017 and effective November 20, 2017, is the contractual-language authority throughout this
document and the closest substitute for a specimen contract, none having been located [R13]. It supplies the
scope definition, the closed list of permitted death benefit formulas [R13 §3.I(1)](#uslib-deferred_income_annuity-r13), the purchase-rate rule
for subsequent premiums [R13 §3.B](#uslib-deferred_income_annuity-r13), the commutation rules [R13 §3.F](#uslib-deferred_income_annuity-r13), the loan prohibition [R13 §3.P](#uslib-deferred_income_annuity-r13), and
the filing accommodation that matters most — a **comparative-adequacy certification** in lieu of a
nonforfeiture demonstration, certifying "that the income benefit provided under this contract is greater than
that guaranteed at issue for the same premium under any non-variable deferred annuity contract offered by the
company that provides cash surrender values during the deferral period or on the income commencement date"
[R13 §1.B(1)(g)](#uslib-deferred_income_annuity-r13). Its `ICCxx` prefix is why DIA forms appear as `ICC11–P101` [S1] and `ICC12-FPDIA12` [S2]
[R13 §2.A(6)](#uslib-deferred_income_annuity-r13).

**NAIC Annuity Disclosure Model Regulation (Model #245) — with a numbering correction.** The annuity
disclosure model is **#245**; **#250 is the Variable Annuity Model Regulation**, which defines a variable
annuity by reference to separate-account investment experience and does not reach a general-account DIA
[R11] [R12] [REG-R43] [REG-R45]. Model #245 probably does not apply to a plain DIA either: Section 3.A exempts
"immediate and deferred annuities that contain no non-guaranteed elements" [R11] and every income benefit in
a non-participating DIA is guaranteed [R13 §3.H(1)](#uslib-deferred_income_annuity-r13) — a direct reading of the retrieved text, though
**whether individual states apply the exemption to DIAs was not verified** [unverified]. A participating DIA
would not be exempt on that ground [R11] [R13 §3.T](#uslib-deferred_income_annuity-r13). Separately, the Suitability in Annuity Transactions Model
Regulation (**Model #275**, 2020 best-interest revision) binds at the distribution layer — new-business mix
and the 1035-exchange flows that feed a DIA as an exchange destination [REG-R46] [REG-R56].

**Valuation Manual — VM-01, VM-22 and VM-V.** VM-01 supplies the statutory definition [R9]. **VM-22, "PBR for
Non-Variable Annuities", names Deferred Income Annuity contracts explicitly in the Payout Annuity Reserving
Category** [R9 §3.F.1.a](#uslib-deferred_income_annuity-r9) [REG-R36] and constitutes CARVM for contracts in scope, applying for valuation dates
on or after January 1, 2026 with an elective three-year transition on VM-A/VM-C/VM-M/VM-V for newly issued
business [R9] [REG-R36]. For contracts not passing the Stochastic Exclusion Test, **VM-V Section 1 "Income
Annuities" — not VM-22 — carries the statutory maximum valuation interest rate**, its scope expressly
including "deferred income annuity contracts issued after Dec. 31, 2017" [R9] [REG-R37]; VM-V §1 supersedes
the interest-rate guidance in AG IX-B and the interest references in AG IX-C [REG-R37]. A model citing "VM-22
income annuity interest rates" against the current Valuation Manual is citing the wrong section [REG-R36].
**VM-21 does not apply** — it is the variable-annuity standard [REG-R35] [REG-R36]. The guideline family
incorporated by VM-C (AG II, VIII, IX, IX-A/B/C, XIII, XXXIII, XXXV, XL, XLI) is indexed at [REG-R41].

**Formulaic CARVM — Appendix A-820 and Actuarial Guideline XXXIII, now read in the AP&P Manual print.** The NAIC
*Accounting Practices and Procedures Manual*, which this library had recorded as a paid publication it could not fetch
[REG-R110 limit](#uslib-reg-r110), is in fact a **free download**, and both items were read in full from it on 2026-08-06:
**A-820, "Minimum Life and
Annuity Reserve Standards"** with A-821 and A-822 [REG-R153], and **AG 33, "Determining CARVM Reserves for Annuity
Contracts With Elective Benefits"** [REG-R151] — the printed title, not the wording IRS Rev. Rul. 2002-6 uses. A-820
¶6 makes the minimum standard for an individual annuity contract the triple **method ¶¶14–15, interest ¶¶7–10,
mortality Appendix A-821**, and ¶14 excludes only employer-plan group annuity business, so an individual DIA is
squarely inside CARVM [REG-R153 ¶¶6, 14–15](#uslib-reg-r153). AG 33 then interprets that CARVM: it applies "to all annuity contracts
subject to CARVM, where any elective benefits … are available to the contract owner", with **no product list and no
size or premium threshold**, so the ±5-year income start date adjustment, payment acceleration and (extended case)
commutation each put the contract inside it — while a cell offering **none** of them, such as a **Life Only QLAC**,
falls outside AG 33 although CARVM still applies, AG 33's own *Definitions* expressly treating a deferred annuity
"where no benefit options are available" as non-elective [REG-R151]. Three consequences matter at specification
level: the start-date adjustment **changes the valuation
interest rate**, because the annuitization guarantee duration runs from issue to the assumed commencement date and
the ±5 years can cross A-820 ¶8.c.i's guarantee-duration bands; a **commutation right bars** AG 33 *Text* 4(B)'s
annuitization treatment for the payments it can reach; and the guideline's **7% expense-allowance floor has no base**
here, being expressed on an accumulation fund this product does not have. AG 33 carries **no formulas, tables or
factors** beyond that 7% cap and its 1998–2000 grade-in percentages, and **never cites SVL §5a by number** — the
§5a pairing this library uses is its own, made on content [REG-R151].

**Annuity valuation mortality.** Model #821 recognizes the 2012 Individual Annuity Reserving (2012 IAR)
table, a generational table combining the 2012 IAM Period Table with Projection Scale G2 [REG-R59]; VM-M
prints the application formula and the rounding rule [R9] [REG-R59], and the Academy/SOA development report
records the LATF margin of 10% at ages up to and including 100, grading down 1% per year above 100 until an
ultimate mortality cap of 0.40000 [R14] [REG-R60]. The AP&P print says the same: **A-821 ¶11** prescribes the 2012 IAR
table for any individual annuity or pure endowment contract issued on or after January 1, 2015 (¶10, the Annuity 2000
table for issues from January 1, 2001 through December 31, 2014), and **¶14 prints the no-chaining rounding rule with
its own counter-example** [REG-R153]. A-821 **prints only** the 2012 IAM Period Table and Scale G2, however — the
Annuity 2000 table, 1983 Table "a" and the 1994 GAR table are named and not printed, and **no standard is printed for
individual annuities issued before January 1, 2001** [REG-R153]. Annuitant mortality is a different and lighter basis than
insured-life mortality — the 2017 CSO and 2015 VBT families must **never** be used for annuitant longevity
[REG-R59] [REG-R61].

**Federal securities regulation — none applies.** A DIA is a non-registered, general-account, non-variable,
non-indexed contract; EDGAR full-text searches located no DIA specimen contract and no retrieved source
describes SEC registration, a prospectus, Form N-4 or a Key Information Table for any of these products
[research-file finding; the framework for why fixed annuities are state-regulated non-securities is at
REG-R53] [unverified as a legal statement]. This is the sharpest contrast with the registered index-linked
and variable annuity chassis in this library [REG-R49] [REG-R52].

**IRC § 72 (nonqualified taxation).** The excludable portion of each payment is the exclusion ratio —
investment in the contract over expected return — capped at the unrecovered investment, with any unrecovered
investment remaining at death allowed as a deduction for the annuitant's last taxable year
[R8 §72(b)](#uslib-deferred_income_annuity-r8) [REG-R55]. Investment in the contract is aggregate premiums less amounts previously received
excludably [R8 §72(c)](#uslib-deferred_income_annuity-r8) — for a flexible-premium DIA, the sum of all purchase payments. The 10% additional tax
on premature distributions, with its 59½, death, disability and substantially-equal-periodic-payments
exceptions [R8 §72(q)](#uslib-deferred_income_annuity-r8), is why every acceleration and commutation feature is gated at 59½ [S1] [S3] [S4].
Section 72(s) governs required distributions on the holder's death [R8].

**IRC § 401(a)(9) and the QLAC.** The current rules live in **paragraph (q)**, not the old "A-17" Q&A format:
T.D. 10001 (89 FR 58886, July 19, 2024, effective September 17, 2024) restructured them and implemented
SECURE 2.0 § 202 [R1 credit line](#uslib-deferred_income_annuity-r1) [R6] [REG-R58]; the original rule was T.D. 9673, "Longevity Annuity
Contracts", 79 FR 37633 (July 2, 2014) [R7]. Cite **§ 1.401(a)(9)-6(q)** for current law [R1] [REG-R57] and
**SECURE 2.0 Act of 2022 § 202** (Division T of Pub. L. 117-328) for the statutory command that raised the
dollar limit from $125,000 to $200,000, eliminated the 25%-of-account-balance limit, preserved
joint-and-survivor benefits through divorce and permitted a rescission period not exceeding 90 days
[R2] [REG-R58]. The RMD exclusion is § 1.401(a)(9)-5(b)(4) [R4], applied to IRAs by § 1.408-8(h) and switched
off for Roth IRAs by § 1.408-8(h)(4) [R5].

**Accounting and professional standards.** Under LDTI a payout annuity carries a liability for future policy
benefits with annually reviewed assumptions and **no market risk benefit** — there is no account value for an
MRB to attach to [REG-R34] [REG-R71]. The tax reserve is the greater of net surrender value (zero here) and
92.81% of the NAIC-prescribed method, capped at the statutory reserve [REG-R16]. Pricing is governed by ASOP
54 [REG-R70], the projection by ASOP 7 [REG-R27], model governance by ASOP 56 [REG-R32], asset adequacy
opinions by ASOP 22 [REG-R29]. ASOP 2's scope covers non-guaranteed elements for annuity products [REG-R26];
whether a DIA's current purchase rate for a future premium falls within it was not verified [unverified] —
the operative constraint on that rate is the Compact's "current annuity purchase rates" floor
[R13 §3.B(1)(c)](#uslib-deferred_income_annuity-r13).

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-deferred_income_annuity-r1
[R10]: #uslib-deferred_income_annuity-r10
[R11]: #uslib-deferred_income_annuity-r11
[R12]: #uslib-deferred_income_annuity-r12
[R13]: #uslib-deferred_income_annuity-r13
[R14]: #uslib-deferred_income_annuity-r14
[R2]: #uslib-deferred_income_annuity-r2
[R3]: #uslib-deferred_income_annuity-r3
[R4]: #uslib-deferred_income_annuity-r4
[R5]: #uslib-deferred_income_annuity-r5
[R6]: #uslib-deferred_income_annuity-r6
[R7]: #uslib-deferred_income_annuity-r7
[R8]: #uslib-deferred_income_annuity-r8
[R9]: #uslib-deferred_income_annuity-r9
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R32]: #uslib-reg-r32
[REG-R34]: #uslib-reg-r34
[REG-R35]: #uslib-reg-r35
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R41]: #uslib-reg-r41
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R44]: #uslib-reg-r44
[REG-R45]: #uslib-reg-r45
[REG-R46]: #uslib-reg-r46
[REG-R49]: #uslib-reg-r49
[REG-R52]: #uslib-reg-r52
[REG-R55]: #uslib-reg-r55
[REG-R56]: #uslib-reg-r56
[REG-R57]: #uslib-reg-r57
[REG-R58]: #uslib-reg-r58
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R61]: #uslib-reg-r61
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
