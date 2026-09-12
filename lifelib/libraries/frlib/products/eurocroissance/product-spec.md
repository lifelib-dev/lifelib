# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of the French **eurocroissance** support — a savings
engagement inside an *assurance vie* or *capitalisation* contract that gives rise to a
**provision de diversification** (a technical provision in which savers hold individualised
rights expressed in *parts*) and carries a capital guarantee **at a contractual maturity
only**. It does not describe any single insurer's support. Facts carrying a source tag —
[S#] (insurer and third-party product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/eurocroissance.md` and resolved against
`sources.md` in this directory — were extracted from the cited document. [REG-R#] resolves
against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R-numbering). Values
marked **[std]** are standardizations introduced for the reference implementation; each
[std] table row carries a numbered footnote giving the rationale and, where the research
recorded one, the observed range across insurers. Facts that could not be confirmed
against a retrieved document are flagged [unverified].

**The documentation position, stated up front, because it shapes every page below.**
Eurocroissance is a very small product with almost no public contractual documentation:
**no insurer's *notice d'information*, *conditions générales* or PRIIPs *document
d'information clé* for a eurocroissance support could be retrieved** [S10]. What is fully
retrievable is the law, which fixes the mechanics of this product in far more detail than
those of a *fonds en euros*, because eurocroissance is a statutory construct rather than a
market convention. The mechanics anchors are **arts. L. 134-1 to L. 134-5** [R1],
**R. 134-1 to R. 134-12** [R2], **A. 134-1 to A. 134-7** [R3], **loi PACTE art. 72** [R4],
**décret n° 2019-1437** [R5] and **décret n° 2025-1333** [R7], all read in full; parameter
*levels* come from insurer marketing pages [S1]–[S7], two third-party fact pages [S8] [S9]
and one published actuarial *mémoire* [R13]; every insurer-level parameter the code does
not fix is **[std]**.

---

## Product overview and market role

A **eurocroissance** engagement is not a contract; it is a *support* inside an ordinary
assurance-vie or capitalisation contract, defined by the kind of engagement the insurer
takes on. A single policy's premiums may simultaneously create *fonds en euros*
engagements, *unités de compte* engagements and diversification-provision engagements
[R1 L. 134-1](#frlib-eurocroissance-r1) [REG-R19]. Insurers may write these engagements in case of life or death,
**excluding temporary death assurance**; they may carry a guaranteed annuity or capital
**at a maturity fixed in the contract**, and they always give rise to a **provision de
diversification** absorbing fluctuations in the value of the backing assets [R1 L. 134-1](#frlib-eurocroissance-r1).
The engagements sit in one or more **comptabilités auxiliaires d'affectation** (ring-fenced
auxiliary accounts) kept by derogation from the Code de commerce [R1 L. 134-2](#frlib-eurocroissance-r1); their
assets are carried at **realisation (market) value** [R2 R. 134-8](#frlib-eurocroissance-r2); no creditor of the
insurer other than the policyholders and beneficiaries of those operations may claim on
them [R1 L. 134-4](#frlib-eurocroissance-r1); and Chapter IV applies **separately to each auxiliary account**
[R2 R. 134-11](#frlib-eurocroissance-r2).

Article L. 134-1 permits **two modalities**, and the difference between them is the whole
product [R1] [R4]:

- **Modality 1°** — the guaranteed annuity or capital is expressed **in euros and in parts
  of the diversification provision**. A *provision mathématique* (PM) equal to the maturity
  guarantee discounted at a regulated rate is carved out of every premium; the remainder
  buys parts. The surrender value is `PM + parts × part value`, so the saver holds a floor
  at every instant [R2 R. 134-2, R. 134-5](#frlib-eurocroissance-r2).
- **Modality 2°** — the guaranteed annuity or capital is expressed **only in parts before
  maturity**, with a **euro guarantee at the maturity**. There is **no provision
  mathématique and no guarantee whatsoever before maturity**; the surrender value is purely
  `parts × part value` [R1 L. 134-1](#frlib-eurocroissance-r1) [R2 R. 134-2, R. 134-5](#frlib-eurocroissance-r2) [R13].

Modality 2° is the **loi PACTE** structure: art. 72 of loi n° 2019-486 rewrote L. 134-1 to
create it, permitted existing 1° engagements to be transformed into 2° by agreement without
the tax consequences of a *dénouement*, and applies to contracts concluded from 1 January
2020 [R4] [R12 CGI 125-0 A I 2°](#frlib-eurocroissance-r12). Décret n° 2019-1437 rewrote the whole regulatory chapter
with effect from **1 January 2020**, old-regime contracts remaining writable until
**1 October 2020** [R5] [R2 R. 134-1 transitional](#frlib-eurocroissance-r2) [REG-R20]. In the words of the actuarial
*mémoire* that models both regimes side by side, the reform's structural change is that
**the continuous guarantee disappears, and with it the provision mathématique — producing
one common return for all savers instead of a return differentiated by entry date, maturity
and guarantee level** [R13].

**Market role.** Eurocroissance is the third French savings compartment, between the *fonds
en euros* (capital guaranteed at every instant, *effet cliquet*) and *unités de compte* (no
guarantee at all). It has never sold. Retrieved sizings: €7.1 bn at end-2022 and €7.6 bn at
mid-2023 across more than 470 000 contracts [R21]; **€11.1 bn (+24 %) across 673 000
contracts (+26 %) at end-2024** [R14]; €11.3 bn across more than 700 000 contracts at March
2025 [S9]; **no published figure for end-2025**, because France Assureurs' January 2026
release carries no eurocroissance line [R16]. Against a French life market of €1 989 bn at
end-2024 [R14] and €2 107 bn at end-2025 [R16] — unit-linked provisions alone were
€587.1 bn [R15] — eurocroissance is about **0.5 %** of the market. It is also close to
invisible in the statistics: ACPR's weekly life-flows collection **explicitly excludes
eurocroissance products** [R18], its annual revaluation study does not break them out [R19],
and the one complete data set, the annual A. 134-7 return by maturity year and guarantee
level, goes to the ACPR and the ministry and is **not published** [R3]. Sia Partners' 2023
verdict stands: only a handful of insurers offer the new eurocroissance [R21].

Published **2025 net returns**, net of management charges and gross of tax and social
levies, span **0.90 % to 3.40 %** across seven supports [S9] — G Croissance 2020 (Generali)
3.40 %, cross-checked at 3.40 % [S8]; Agipi eurocroissance (AXA) 3.00 %; Fonds Croissance
(AXA) 2.50 %, quoted by the insurer itself as a **2.50 %–4.50 %** range averaging **3.13 %**
[S3]; Afer eurocroissance 2.16 %; Croissance Allocation Long Terme (Spirica) 0.90 %. The
premium over the same insurer's *fonds en euros* is of the order of **25–60 bp** (AXA euro
2.25 %–4.25 % against Fonds Croissance 2.50 %–4.50 % [S3]; Generali euro-fund average 2.55 %
for life [S6]) — close to the **+30 bp** piloting objective the *mémoire* assumes [R13]. The
dispersion the product is supposed to have, and the euro fund is not, shows in G Croissance
2020's history: 0.52 % (2020), 0.05 % (2022), 3.67 % (2023), 3.55 % (2024), 3.40 % (2025)
[S8].

**This specification standardizes a single composite:** a eurocroissance support with a
**100 % guarantee of net premiums at a 10-year maturity** [S1] [S2], written on **two
chassis** held in **two separate auxiliary accounts** — **Chassis A** (1° engagement, the
pre-2020 generation) and **Chassis B** (2° engagement, the post-PACTE generation) — so that
the same asset path can be run through both and the effect of the reform read off directly.
The model these chassis feed is **`EC_FR_S`**, on a **monthly** grid.

---

## Representative specification

### Structure common to both chassis

| Parameter | Representative value | Basis |
|---|---|---|
| Legal form | Support inside an assurance-vie or capitalisation contract; L. 134-1 engagement | [R1] [REG-R19] |
| Ring-fencing | One *comptabilité auxiliaire d'affectation* per chassis; policyholder priority over all other creditors | [R1 L. 134-2, L. 134-4](#frlib-eurocroissance-r1); one account per chassis **[std]** (1) |
| Asset valuation inside the account | Realisation (market) value under R. 343-11 / R. 343-12 | [R2 R. 134-8](#frlib-eurocroissance-r2) |
| Technical provisions admitted inside the account | PM (R. 343-3 1°), provision de gestion (4°), frais d'acquisition reportés (7°), **provision de diversification** (9°), **provision collective de diversification différée** (10°), **provision pour garantie à terme** (11°) | [R2 R. 134-9](#frlib-eurocroissance-r2) [R8] [REG-R6] |
| Guarantee level `g` | **100 %** of net premiums | [S1] [S2]; 80 % observed [S8], 80 %–100 % [S7] |
| Guarantee maturity `n` | **10 years** from the first payment | [S1] [S2]; 8–30 [S8], 8–40 [S7] |
| Initial part value | **€10.00** | [R13] |
| Minimum part value | **€5.00** | requirement [R2 R. 134-1, R. 134-10 II](#frlib-eurocroissance-r2); level **[std]** (2) |
| Non-surrender (lock-up) period | **0 years**; contractual cap `min(n, 8 years)` | cap [R2 R. 134-5](#frlib-eurocroissance-r2); level **[std]** (3) |
| Surrender / transfer indemnity | **0 %**; statutory cap 5 % of the present value of the mutual engagements, and the contract **may** provide for none at all once it has been in force more than ten years | cap and the ten-year permission [R10 R. 132-5-3](#frlib-eurocroissance-r10); level **[std]** (3) |
| Anchor model cell | €10 000 gross single premium at issue; free additional premium of €2 000 gross at the end of policy year 3; male, age 57 at entry | **[std]** (4); premium sizes and age from [R13] |

Footnotes to [std] rows:

1. L. 134-2 permits 1° and 2° engagements to be **grouped in the same auxiliary account**
   [R1]. They are separated here because the part value is **common to all engagements of
   one account** [R2 R. 134-2](#frlib-eurocroissance-r2), so grouping would force one part-value path across both
   chassis and destroy the comparison this composite exists to make. Separation also
   mirrors the market: G Croissance 2014 and G Croissance 2020 are distinct funds [S5] [S8].
2. The contract **must** fix a minimum part value, strictly positive and expressed in
   euros, and disclose it before the first payment [R2 R. 134-1, R. 134-10 II 1°](#frlib-eurocroissance-r2). **No
   public figure was found for any insurer.** €5.00, i.e. 50 % of the €10.00 initial part
   value [R13], is the reference, and it is load-bearing: it is the floor below which the
   part value cannot be reduced to absorb a debit balance [R2 R. 134-4](#frlib-eurocroissance-r2), and therefore the
   second limb of the guarantee under Chassis A.
3. The code caps a contractual non-surrender period at the **lesser of the guarantee
   maturity and eight years** [R2 R. 134-5](#frlib-eurocroissance-r2) and the surrender indemnity at **5 %** of the
   present value of the mutual engagements; R. 132-5-3 further **permits** the contract to
   provide **no indemnity at all** once it has been in force more than ten years, which is a
   permission and not a prohibition [R10]. The reference contract charges none at any
   duration, and `EC_FR_S` returns zero beyond ten years unconditionally **[std]**, which is
   that permission taken up rather than a rule the article imposes. No retrieved insurer
   document states a lock-up; AXA says surrender is available at
   any time and carries **no penalty** [S2], and Generali's third-party sheet shows none
   either [S8]. Zero and zero are the reference. The *mémoire* notes no explicit penalty is
   needed, because the surrendering saver already walks away from his share of the PCDD
   [R13].
4. Pure modeling anchor, sized on the *mémoire*'s own cohort: €10 000 initial premium, free
   additional premiums of €2 000 paid by 15 %–30 % of savers, age 57 at subscription [R13].
   The additional premium sits at the end of year 3 so that the worked example exercises the
   mid-contract split of a *versement*.

### Chassis A — 1° engagement: euros and parts (legacy cell)

| Parameter | Representative value | Basis |
|---|---|---|
| Engagement type | Guarantee expressed **in euros and in parts** | [R1 L. 134-1 1°](#frlib-eurocroissance-r1) |
| Provision mathématique | `PM(t) = MG(t) × (1 + i_pm)^-(n-t)` — the maturity guarantee discounted | [R2 R. 134-2](#frlib-eurocroissance-r2) |
| Discount rate `i_pm` | **90 % of the last TEC*n*** published by the Banque de France, `n` = the holder's guarantee maturity (per-engagement method 1°) or the account's 1°-engagement duration (method 2°); linear interpolation between bracketing TEC maturities; longest available TEC beyond the curve; **floor 0 %**; the method choice binds the whole account and is **irreversible**. The article is silent on how that maturity is re-read at later valuation dates; `EC_FR_S` applies method 1° and takes the **remaining** term at each monthly valuation, which is **[std]** — `technical-notes.md` states that reading and is the source of truth for the value the model uses | article [R3 A. 134-1](#frlib-eurocroissance-r3); the remaining-term re-reading **[std]**, `technical-notes.md` |
| Reference TEC10 | **2.50 %** to year 5, **1.00 %** from year 6 (rate-shock scenario) → `i_pm` 2.25 % then 0.90 % | **[std]** (5) |
| Surrender / transfer value before maturity | `PM(t) + parts(t) × part value(t)`, less any R. 132-5-3 indemnity | [R2 R. 134-5](#frlib-eurocroissance-r2) |
| Maturity amount | the same quantity — `PM(n) + parts(n) × part value(n)` | [R2 R. 134-6](#frlib-eurocroissance-r2) |
| Effective floor | `MG + parts × minimum part value` — the PM reaches the guarantee at maturity, and the part value cannot fall below its contractual minimum | [R2 R. 134-2, R. 134-4](#frlib-eurocroissance-r2) |
| Insufficient representation | The insurer **completes the representation** by contributing assets backing its own reserves and provisions, releasable when representation permits | [R1 L. 134-3](#frlib-eurocroissance-r1); roll-forward treatment **[std]** (6) |
| Encours charge base | **Not available on the provision de diversification** — R. 134-3 3° permits that levy only where the account holds **no 1° engagements** | [R2 R. 134-3 3°](#frlib-eurocroissance-r2) |
| Guarantee revaluation out of the participation account | Permitted only if **both**: PD attaching to 1° guarantees > **1.5 ×** (zero-rate PM − actual PM), **and** (PD − its minimum) > **10 % of PM** | [R3 A. 134-3](#frlib-eurocroissance-r3) |
| Conversion of parts into PM | At most **once every five years**, and only if after conversion (PD − its minimum) > **15 % of that engagement's PM** | [R3 A. 134-4](#frlib-eurocroissance-r3) |

5. No TEC series value was retrieved. The level is anchored on the ACPR's macro backdrop for
   its 2024 revaluation study — the **10-year OAT averaged 3.0 %** in both 2023 and 2024
   [R19] — haircut for the shorter effective maturity and rounded; the 90 % factor is
   statutory [R3 A. 134-1](#frlib-eurocroissance-r3). The step down to 1.00 % in year 6 is a deliberate rate shock, so
   that the worked example exercises the rate-driven transfer of value from the
   diversification provision to the mathematical provision.
6. L. 134-3 says the insurer "completes" the representation and may re-allocate assets out
   when representation permits, without fixing how the contributed assets and their return
   are attributed [R1]. The reference treatment is an outstanding balance carrying **no
   return to the savers**, repaid in full as soon as the account's own assets cover
   `PM + parts × minimum part value` — consistent with the re-allocation cap set for the
   separate R. 134-12 mechanism, affectation-date realisation value **plus the assets' share
   of net investment income while inside the account** [R7 II](#frlib-eurocroissance-r7).

### Chassis B — 2° engagement: parts only, guarantee at maturity (primary cell)

| Parameter | Representative value | Basis |
|---|---|---|
| Engagement type | Guarantee expressed **only in parts before maturity**, in euros **at maturity** | [R1 L. 134-1 2°](#frlib-eurocroissance-r1) [R4] |
| Provision mathématique | **none** | [R1] [R13] |
| Surrender / transfer value before maturity | `parts(t) × part value(t)`, less any R. 132-5-3 indemnity — **no guarantee of any kind** | [R2 R. 134-5](#frlib-eurocroissance-r2) |
| Pre-sale disclosure | The **absence of any guarantee before maturity** must be stated in "caractères très apparents", with the maturity, the euro amount of the guarantee at maturity, any non-surrender period and the settlement arrangements | [R2 R. 134-10 I](#frlib-eurocroissance-r2) |
| Maturity amount | **`max( parts(n) × part value(n), MG(n) )`** — the only point at which the guarantee bites | [R2 R. 134-6](#frlib-eurocroissance-r2) |
| Maturity settlement | Notice **three months** before maturity; unless the holder decides otherwise expressly, settled as a benefit or **arbitraged into a support whose PRIIPs synthetic risk indicator is ≤ 2** | [R2 R. 134-6](#frlib-eurocroissance-r2) [R3 A. 134-6](#frlib-eurocroissance-r3) [REG-R33] |
| Provision pour garantie à terme (PGT) | `max( PV(guarantees) − PD − PCDD, 0 )`, per auxiliary account; PV on the **A. 132-18 mortality tables** at a rate ≤ 90 % of the TEC at the account's 2°-engagement duration, counting **no cash flows other than guarantee maturities and mortality**; funded from the insurer's **own funds**, **outside the participation account** | [R3 A. 134-2](#frlib-eurocroissance-r3) [R10 A. 132-18](#frlib-eurocroissance-r10) [R1 L. 134-3](#frlib-eurocroissance-r1) [R13] |
| Encours charge base | A levy on the **provision de diversification** is available, because the account holds no 1° engagements | [R2 R. 134-3 3°](#frlib-eurocroissance-r2) |
| Documented example | AXA **Fonds Croissance**: 100 % of net invested capital guaranteed at a **10-year minimum** maturity; capital loss before maturity may be total or partial; **SRI 2/7**; surrender at any time without penalty | [S1] [S2] |

### Charges (*prélèvements*)

Deductions may be taken **only** on the six bases listed at R. 134-3 [R2]: **1°** premiums
and incoming transfers or arbitrages; **2°** amounts arising from the R. 134-4 conversion of
parts into PM; **3°** the *provision de diversification*, **and only where the auxiliary
account holds no 1° engagements**; **4°** the *number of parts*; **5°** the balance of the
participation account **or alternatively** the performance of the financial management of
the account's assets; **6°** benefits paid and outgoing transfers or arbitrages. Base 3° is
therefore unavailable in Chassis A and base 2° is meaningless in Chassis B.

| Charge | Representative value | Basis |
|---|---|---|
| Entry charge (*frais sur versements*, base 1°) | **2.00 %** of each premium, deducted before rights are created | level [R13]; **4.50 % maximum** observed [S8]; adoption **[std]** (7) |
| Recurring charge (base 4°, levy in number of parts) | **0.80 % p.a.** of parts, taken at the start of each policy year on the opening part value | level [R13]; routing through base 4° **[std]** (8) |
| Performance charge (base 5°, second limb) | **10 %** of positive financial-management performance | [R13]; adoption **[std]** (9) |
| Conversion charge (base 2°) | **0.50 %** of amounts converted from parts into PM | [S8]; Chassis A only |
| Exit charge (base 6°) | **0 %** — permitted by the code, shown by neither insurer | [R2 R. 134-3 6°](#frlib-eurocroissance-r2) [S2] [S8]; level **[std]** (9) |
| Guaranteed-rate ceiling | Any rate the insurer guarantees on these contracts is subject to the **art. A. 132-3** ceiling | [S4] [REG-R18] |

7. The *mémoire* uses 2 % of premiums and states that a levy on premiums plus encours plus
   performance "est une pratique courante du marché actuellement" [R13]. Generali shows
   *frais sur versements* of **4.50 % maximum** [S8]; AXA publishes no percentage [S1] [S2].
   The entry charge reduces the **guaranteed amount too**, because the guarantee is a
   percentage of premiums **net of the charges permitted by R. 134-3 1°** [R2 R. 134-2](#frlib-eurocroissance-r2).
8. The *mémoire* levies **0.8 % p.a. of (PM + PD)** [R13]. That base is unlawful in a 1°
   account: R. 134-3 3° permits a levy on the PD only where the account holds no 1°
   engagements, and no base permits a levy on the PM [R2]. The reference implementation
   routes the same economic charge through base **4°, the number of parts**, available in
   both chassis. The consequence should not be smoothed away: in Chassis A the recurring
   charge bites on the diversification provision only, a small fraction of the account, so
   the insurer's recurring income is far lower than on Chassis B — one reason the 2014-regime
   product had poor economics for the insurer [R13].
9. The *mémoire* charges 10 % of positive financial income and passes 100 % of negative
   performance to savers [R13]. The consolidated R. 134-3 5° as retrieved states **no caps**
   and reads "**ou alternativement**" — a choice between the participation-account limb and
   the financial-performance limb [R2]. The *mémoire*'s statement that PACTE made the two
   levies **simultaneous**, capped at 15 % and 10 %, is **[unverified]**; the retrieved code
   text governs. Neither insurer shows an exit charge [S2] [S8], so zero is adopted.

### Fund-level machinery

| Item | Representative value | Basis |
|---|---|---|
| Participation account (*compte de participation aux résultats*) | Struck at least annually; a **credit balance** may go to (i) the PM by revaluing the guarantees, (ii) the PD by **awarding new parts** or **raising the part value**, (iii) the PCDD. A **debit balance** is absorbed by a *reprise* of the PCDD or by **reducing the part value, within the limit of its minimum value** | [R2 R. 134-4](#frlib-eurocroissance-r2) |
| Statutory minimum PB | **Does not apply**: art. A. 132-12 excludes art. L. 134-1 contracts | [REG-R15] |
| Credit-balance allocation route | **Raise the part value**; no new parts awarded | choice **[std]** (10) |
| PCDD (*provision collective de diversification différée*) | Collective smoothing reserve for the surrender value; no individual rights; must be used within **fifteen years** | [R8 R. 343-3 10°](#frlib-eurocroissance-r8) [R9 A. 132-16](#frlib-eurocroissance-r9) [R21] |
| PCDD in the base configuration | **0** | **[std]** (11) |
| Insurer asset contribution (*apport d'actifs*, trade name *transfert de richesse*) | Up to **10 % of the diversification provision** at the affectation date; enters at realisation value; **endows the PCDD** by the same amount; re-allocation capped at the lowest of (a) affectation-date value + share of net investment income + R. 134-3 5° levies, (b) 10 % of total PD, (c) total PCDD; **no later than the sixteenth year** following affectation; affectations happen on the participation-account striking dates, **after the balance has been allocated** | [R7 R. 134-12](#frlib-eurocroissance-r7) |
| Apport d'actifs in the base configuration | **0** | **[std]** (11) |
| Intermediate valuation | The diversification provision must be re-struck at an intermediate value **at least monthly** in every month in which the participation account is not struck; a surrender is priced on the **next** striking or intermediate value, i.e. on a **forward** part value | [R3 A. 134-5](#frlib-eurocroissance-r3) |
| Supervisory return | Annual ACPR return by **30 April**, separately for 1° and 2° engagements, **by maturity year and by guarantee level** on a scale of the proportion of premiums guaranteed, **origin 0, step 5 percentage points**; aggregated by ACPR, not published | [R3 A. 134-7](#frlib-eurocroissance-r3) |

10. R. 134-4 lets the credit balance reach the PD by awarding **new parts** or by **raising
    the part value** [R2]. Raising the part value is the reference route because it is what an
    annual-grid model can express without a per-cohort parts ledger. The choice is not
    neutral: because the part value is **common to all engagements of an account**
    [R2 R. 134-2](#frlib-eurocroissance-r2), returns can be differentiated by guarantee level or committed term
    only through the **number of parts** awarded or through **differentiated PCDD
    distribution** [R2 R. 134-2, R. 134-4](#frlib-eurocroissance-r2) [R13] — and the *mémoire*'s own
    model differentiates neither, which it flags as its most consequential simplification
    [R13]. Raising the part value forgoes the first of the two routes; the second is the
    fund-level PCDD extension, held at zero here.
11. Both are **collective**, fund-level items with no individual rights [R8 R. 343-3 10°](#frlib-eurocroissance-r8)
    [R7 I](#frlib-eurocroissance-r7), so a per-policy model cannot represent them without a fund-level extension; the
    technical notes give the recursions. For reference, the *mémoire*'s piloting recipe is to
    target the insurer's own euro-fund net rate **+0.30 %** and put everything else in the
    PCDD, and its *transfert de richesse* level is **10 % of net premiums for the first three
    years**, credited to the PCDD [R13].

---

## Contractual mechanics

**Premium, parts and the part value.** Premiums and incoming transfers or arbitrages, **net
of the entry charge permitted by R. 134-3 1°**, create individual rights expressed in a
**number of parts** of the diversification provision and, for 1° engagements only, in
*provision mathématique* [R2 R. 134-2](#frlib-eurocroissance-r2). The number of parts equals the diversification
provision divided by the **part value, which is common to all engagements of the auxiliary
account** [R2 R. 134-2](#frlib-eurocroissance-r2). The insurer **guarantees the number of parts but not their value**
[S1] [R13]: the count changes only on further premiums, surrenders, death, charges taken in
parts, or a profit allocation made in parts [R2 R. 134-3 4°, R. 134-4](#frlib-eurocroissance-r2).

**Splitting a *versement* under Chassis A.** For a 1° engagement, a net premium `P_net` paid
at time `t` raises the guaranteed amount by `g × P_net` and is split so that the share
carried to the *provision mathématique* accumulates at the regulated rate to exactly that
increment at the maturity:

```
pm_added    = g × P_net × (1 + i_pm(t))^-(n-t)
pd_added    = P_net − pm_added
parts_added = pd_added / part_value(t)
```

This is the operative form of R. 134-2: the PM **is** the maturity guarantee discounted at
the rate fixed by arrêté [R2] [R3 A. 134-1](#frlib-eurocroissance-r3). It has an unpleasant property the market
discovered the hard way — when the rate is low and the term short, the discount factor is
close to 1 and **the guaranteed leg absorbs almost the whole premium**, leaving little to
invest in risk assets, which is one reason the 2014-regime product could not out-earn a
mature *fonds en euros* [R13].

**The annual rebalancing.** The PM is not accumulated; it is **re-struck** at every account
striking from the then-current guaranteed amount and the then-current regulated rate. Two
effects therefore transfer value between the provisions every year: a **time effect** — one
year less of discounting, so the PM rises mechanically toward the guarantee — and a **rate
effect** — a fall in the TEC raises the discounted guarantee, so the PM rises again. Under
Chassis A the diversification provision is the **residual**: it absorbs both effects on top
of whatever the assets did. When the residual would fall below `parts × minimum part
value`, the part value stops at its contractual minimum [R2 R. 134-4](#frlib-eurocroissance-r2) and the insurer
completes the representation out of its own reserves [R1 L. 134-3](#frlib-eurocroissance-r1). Under Chassis B there is
no PM to squeeze the parts; the same shortfall appears instead as a **provision pour
garantie à terme** on the insurer's balance sheet, outside the participation account and
outside the savers' value [R3 A. 134-2](#frlib-eurocroissance-r3) [R13].

**The participation account.** A *compte de participation aux résultats* is struck; its
credit balance is allocated to the PM (by revaluing the guarantees, subject to the two
A. 134-3 tests), to the PD (new parts or a higher part value), or to the PCDD; a debit
balance is absorbed by a *reprise* of the PCDD or by **reducing the part value down to, but
not below, its contractual minimum** [R2 R. 134-4](#frlib-eurocroissance-r2). Asset affectations and re-affectations
completing the account's representation are made **on the dates the participation account is
struck, after its balance has been allocated** [R2 R. 134-4](#frlib-eurocroissance-r2) [R7 III](#frlib-eurocroissance-r7) — that sentence fixes
the annual processing order a model must use.

**Early surrender (*rachat*) — the single most important product fact.** Before the
maturity, **Chassis A (1°)** pays `PM(t) + parts(t) × part value(t)` less any indemnity
[R2 R. 134-5](#frlib-eurocroissance-r2): the PM is a floor, so the 2014-regime product carried a guarantee at every
instant. **Chassis B (2°)** pays `parts(t) × part value(t)` less any indemnity
[R2 R. 134-5](#frlib-eurocroissance-r2): **there is no guarantee whatsoever before maturity**, and the pre-sale
documentation must say so in "caractères très apparents" [R2 R. 134-10 I 3°](#frlib-eurocroissance-r2). AXA states the
point plainly on its own product page — before maturity the amounts invested fluctuate and
"le risque de perte en capital peut être total ou partiel" [S1], and surrender is available
at any time without penalty but exposed to that loss [S2]. The part value used is the one
struck at the **next** participation account, or the next monthly intermediate value divided
by the parts then outstanding, whichever comes first, so a surrender is priced on a
**forward** part value, never a same-day one [R3 A. 134-5](#frlib-eurocroissance-r3). The statutory hardship exits of
L. 132-23 survive any contractual non-surrender period [R1] [R2 R. 134-5](#frlib-eurocroissance-r2), and surrender
must be settled within **two months** [REG-R31 L. 132-21](#frlib-reg-r31).

**Maturity (*échéance*).** For 1° engagements the amount due is the R. 134-5 value,
`PM(n) + parts(n) × part value(n)`; for 2° engagements it is
`max( parts(n) × part value(n), the guarantee )` — **the only point at which the guarantee
bites** [R2 R. 134-6](#frlib-eurocroissance-r2). Unless the holder decides otherwise expressly, the amount is settled
as a benefit or arbitraged into a support with a PRIIPs synthetic risk indicator of **2 or
below** [R2 R. 134-6](#frlib-eurocroissance-r2) [R3 A. 134-6](#frlib-eurocroissance-r3) [REG-R33]; **three months** before maturity the holder
must be told where the money will go and how to change that [R2 R. 134-6](#frlib-eurocroissance-r2). If the contract
offers an annuity, the *capital constitutif* is that amount expressed in euros, the rights
become an ordinary R. 343-3 1° *provision mathématique* and **leave the auxiliary account**
[R2 R. 134-6](#frlib-eurocroissance-r2) — from that point the liability is a *rente viagère*.

**Death before maturity.** Chapter IV contains **no death-specific valuation article**:
R. 134-5 and R. 134-6 speak of the surrender or transfer value before maturity and of the
amount due **at maturity** [R2]. The maturity guarantee is therefore **not** given to a death
claim, and the death benefit is the current provision value — `PM + parts × part value`
under Chassis A, `parts × part value` under Chassis B [R2] [R13]. A death floor is a
**complementary guarantee** under R. 134-7, priced and provisioned **outside** the auxiliary
account with its individualised premium disclosed before the first payment [R2 R. 134-7,
R. 134-10 II 2°](#frlib-eurocroissance-r2). L. 134-1 excludes temporary death assurance from the chapter altogether
[R1].

---

## Riders and options

**In scope (modeled as flags):**

- **Garantie décès plancher** — a complementary death guarantee ensuring the beneficiaries
  receive at least the **net invested savings**; AXA carries one on Fonds Croissance
  [S1] [S2]. Provisioned **outside** the auxiliary account [R2 R. 134-7](#frlib-eurocroissance-r2), with its
  individualised premium disclosed before the first payment [R2 R. 134-10 II 2°](#frlib-eurocroissance-r2). Modeled as
  `death_floor_flag` with a floor equal to cumulative net premiums; the rider premium level
  is **[std]** (no public figure).
- **Annuity option at maturity** — the maturity amount becomes the *capital constitutif* of
  a *rente viagère*; the rights leave the auxiliary account and become an ordinary
  R. 343-3 1° mathematical provision [R2 R. 134-6](#frlib-eurocroissance-r2), priced on the regulatory generational
  tables TGH05 / TGF05 [REG-R21] [REG-R23]. Modeled as `annuity_option_flag`; the annuity
  itself is out of scope — see `../rente_viagere/technical-notes.md`.

**In scope, computed and reported but never exercised:**

- **Conversion of parts into PM (Chassis A only)** — the saver locks in more guarantee at
  the cost of upside [R2 R. 134-4](#frlib-eurocroissance-r2). Permitted at most **once every five years**, and only if
  after conversion the excess of the diversification provision over its minimum exceeds
  **15 % of that engagement's mathematical provision** [R3 A. 134-4](#frlib-eurocroissance-r3). A charge may be levied
  on the converted amounts [R2 R. 134-3 2°](#frlib-eurocroissance-r2); Generali's sheet shows *frais de conversion* of
  **0.50 %** [S8]. **The election itself is out of scope**: `conversion_headroom()` computes
  the A. 134-4 headroom and reports it, and nothing exercises the conversion. There is no
  election field in `model_point_table.csv` — see `model.md`.
- **Guarantee revaluation out of the participation account** — `gate_revalue_ok()` evaluates
  both A. 134-3 tests and reports the verdict; the reference credit-balance route raises the
  part value instead [R3 A. 134-3](#frlib-eurocroissance-r3).

**Out of scope for the composite:** **commercial bonus devices** — contractual promotions,
**not** the statutory *apport d'actifs*: AXA's **Eurocroissance +** adds **+2 %** to the base
rate on 2026 payments (and +0.5 % on pre-2026 euro savings), conditional on **at least 45 % of
savings in unités de compte** or on piloted/convention management, held to **31 December 2026**
and through to the attribution date, **no later than 1 April 2027**; money-market funds and
PACTE-transfer initial payments are excluded [S3] [S4]. It is a marketing term rather than a
term of the statutory mechanics this composite specifies, and it has **no counterpart in
`EC_FR_S`** — no uplift Reference, no cells, no model-point column and no eligibility flag.
Also out of scope: temporary death assurance, which L. 134-1 excludes [R1];
PER wrappers carrying a eurocroissance support (AXA's PER "Ma Retraite" eurocroissance
credited **3.25 %** for 2025 [S3]) — see `../per_assurance/`; the *fonds en euros* and
*unités de compte* compartments of the same policy — see `../assurance_vie_euro/` and
`../assurance_vie_uc/`; capitalisation contracts written on the same terms [R1 L. 134-1](#frlib-eurocroissance-r1); and
the *provision de gestion* and *provision pour frais d'acquisition reportés*, admitted into
the auxiliary account by R. 134-9 [R2] but not computed here.

---

## Variations across insurers

Only three insurers' eurocroissance terms could be documented at all, and only one of them
(Generali, and that through a third party) with charge levels [S8].

| Feature | AXA France — Fonds Croissance [S1] [S2] [S3] [S4] | Generali — G Croissance 2020 [S8], G Croissance 2014 [S5] | Predica / Crédit Agricole — Objectif Programmé [S7] |
|---|---|---|---|
| Regime | post-PACTE (2°: insurer commits to the number of parts, not their value) | 2020 vintage built for PACTE; 2014 vintage old regime | 2014 regime (launched 16 October 2014) |
| Guarantee level `g` | **100 %** of net invested capital | **80 %** | **80 %–100 %**, saver's choice |
| Guarantee term | **10 years minimum** from first investment | **8 to 30 years**, saver's choice | **8 to 40 years**, saver's choice |
| Entry charge | not published | **4.50 % max** | not published |
| Annual management charge | not published (returns quoted net) | **1.00 %** | not published |
| Conversion charge | not published | **0.50 %** | not published |
| Surrender penalty | **none** stated | none shown | not published |
| Death floor | **garantie décès plancher** — at least net invested savings | not documented | not documented |
| SRI | **2 / 7** | not documented | not documented |
| 2025 net return | **2.50 %–4.50 %**, average **3.13 %** | **3.40 %** (2020), **2.20 %** (2014) | closed to new business since 1 October 2020 [unverified] |
| Commercial bonus | **Eurocroissance +** | none documented | none documented |

Four further supports are known to exist from the cross-market rate table with no product
documentation retrieved: Générations Croiss@nce durable (Generali), Agipi eurocroissance
(AXA France), Afer eurocroissance (Abeille Assurances) and Croissance Allocation Long Terme
(Spirica) [S9].

What actually varies, and what does not:

1. **Fixed by law, identical across insurers.** The two modalities and their surrender and
   maturity formulas [R1] [R2 R. 134-5, R. 134-6](#frlib-eurocroissance-r2); the six permitted charge bases
   [R2 R. 134-3](#frlib-eurocroissance-r2); the part value being **common to all engagements of an auxiliary account**
   [R2 R. 134-2](#frlib-eurocroissance-r2); the 90 %-of-TEC discount ceiling and its irreversible per-account method
   choice [R3 A. 134-1](#frlib-eurocroissance-r3); the PGT definition [R3 A. 134-2](#frlib-eurocroissance-r3); the 15-year PCDD clock [R9]; the
   5 % surrender-indemnity cap [R10]; the 10 % / 16-year asset-contribution limits [R7]; the
   SRI ≤ 2 maturity default [R3]; and the social levy at the guarantee maturity [R11].
2. **The guarantee level `g`** is the sharpest observed difference — 80 % against 100 %
   [S8] [S1] — and it decides how much of the fund can sit in risk assets. The ACPR's own
   reporting granularity for `g` is a scale of the proportion of premiums guaranteed with
   **origin 0 and a step of 5 percentage points** [R3 A. 134-7](#frlib-eurocroissance-r3), the natural grid for a
   model's parameterisation.
3. **The maturity range offered**: 10 years fixed at AXA [S1] [S2], 8–30 at Generali [S8],
   8–40 at Predica [S7]. **There is no statutory minimum maturity in the current code.** The
   8-year figure repeated in the trade press [S9] [R21] traces to the 8-year assurance-vie
   tax threshold [REG-R40] and to the denomination arrêté contemplated by R. 134-1 [R2],
   which does not appear in the codified law. What the code does say is that a contractual
   **non-surrender** period may not exceed the lesser of the guarantee maturity and eight
   years [R2 R. 134-5](#frlib-eurocroissance-r2).
4. **The minimum part value** — nowhere published, for any insurer, and load-bearing
   [R2 R. 134-1](#frlib-eurocroissance-r2) — and **the charge structure**, which the code constrains only by **base**
   and not by **level** [R2 R. 134-3](#frlib-eurocroissance-r2). The disclosure regime caps nothing either: the
   *encadré* requires maximum charge amounts or percentages in four categories to be
   disclosed, not limited [REG-R30]. Every charge level here is either read from a
   third-party fact page [S8] or **[std]**.
5. **The PCDD piloting rule and the credit-balance allocation route**, discretionary,
   unpublished, and the biggest driver of the credited return [R13]. A structural consequence
   a modeler must respect: because the part value is **common**, savers with different
   maturities and different guarantee levels in the same auxiliary account all receive **the
   same rate of return**; differentiation is possible only through the number of parts or
   through differentiated PCDD distribution [R2 R. 134-2, R. 134-4](#frlib-eurocroissance-r2) [R13]. Any model that
   gives per-policy returns inside one 2° account is modelling something that does not exist.
6. **Commercial bonus devices** [S3] [S4] — openly marketed, conditional on unit-linked
   allocation, and not the statutory *apport d'actifs*.

**A naming caution.** The term **"bonus de mutualisation" appears in none of the retrieved
documents.** The code calls the mechanism *apport d'actifs* [R7] [R1 L. 134-3](#frlib-eurocroissance-r1);
practitioners call it *transfert de richesse* [R13] [R21]. Separately, the *mémoire* tests
whether pooling two maturity cohorts in one auxiliary account creates a "bénéfice de
mutualisation" and concludes it does **not** — pooling is very slightly value-destructive
before any operational simplification gain, because it shifts the short-maturity cohort onto
a longer and riskier asset allocation [R13].

**The denomination question.** R. 134-1 provides that an arrêté fixes a *dénomination* and
minimum conditions, "notamment en matière d'échéance et de niveau de garantie en capital",
for use of that name in documents intended for third parties [R2]. Searching the full
consolidated Code des assurances for "eurocroissance" and "euro-croissance" returns **zero
hits**, and the A. 134 chapter contains no denomination article [R3]. The widely repeated
claim that the name is **reserved for a 100 % guarantee**, with 80 %-guarantee funds having
to be called "croissance" [S9] [R21], therefore **could not be traced to any retrieved legal
text and is [unverified]** — the more so because Generali markets an 80 %-guarantee fund as
"G Croissance" and AXA a 100 %-guarantee fund as "Fonds Croissance" [S8] [S1].

---

## Regulatory context

**The statutory chapter.** Arts. L. 134-1 to L. 134-5 [R1], R. 134-1 to R. 134-12 [R2] and
A. 134-1 to A. 134-7 [R3] are the product. Chronology: ordonnance n° 2014-696 du 26 juin 2014
created Chapter IV [R1 L. 134-5](#frlib-eurocroissance-r1) [R22 — not retrieved](#frlib-eurocroissance-r22); the arrêté du 12 septembre 2014 fixed
the first A. 134 series [R6]; **loi PACTE art. 72** rewrote L. 134-1 on 22 May 2019 [R4];
décret n° 2019-1437 [R5] [REG-R20] and the arrêté du 26 décembre 2019 [R3] rewrote the
R. 134 and A. 134 chapters from 1 January 2020; the arrêté du 22 décembre 2022 rewrote
A. 134-6 [R3]; and **décret n° 2025-1333 du 26 décembre 2025** reinstated R. 134-12, the
asset-contribution mechanism, from **27 December 2025** [R7]. That last article is eight
months old at the access date, and its reinstatement implies the mechanism was absent from
the code beforehand; when it lapsed, and what governed in the interval, was not established.

**Prudential.** Art. R. 343-3 carries three technical provisions that exist **only** for
L. 134-1 engagements: 9° *provision de diversification*, 10° *provision collective de
diversification différée*, 11° *provision pour garantie à terme* [R8] [REG-R6]. R. 134-9
admits into the auxiliary account only R. 343-3 items 1°, 4°, 7°, 9°, 10° and 11° [R2].
Because the account's assets are held at **realisation value** [R2 R. 134-8](#frlib-eurocroissance-r2), the *provision
pour risque d'exigibilité* [REG-R7], the *provision pour dépréciation durable* and the
*réserve de capitalisation* have no purpose inside it, and the technical and financial
result becomes **volatile by construction** — the asset value determines the liability value,
the exact inverse of a *fonds en euros* [R13]. Under Solvabilité II, technical provisions are
best estimate plus risk margin, discounted on the EIOPA risk-free term structures [REG-R1]
[REG-R2] [REG-R5]; this library treats the capital layer as cited-not-specified. The
*mémoire* reports that removing the continuous guarantee improves the insurer's solvency
indicator by roughly **20–26 points**, worth about **13 %–20 %** more equity exposure at
unchanged solvency [R13].

**Participation aux bénéfices and guaranteed rates.** Eurocroissance sits **outside** the
statutory minimum PB machinery: art. A. 132-12 excludes art. L. 134-1 contracts [REG-R15].
What governs instead is R. 134-4, which fixes the **destinations** of the participation
account's balance but **no percentages and no time limits** [R2] [REG-R19] — so any modeled
split is **[std]**. The one hard timing constraint is A. 132-16: sums carried to the PCDD
must be used "dans les conditions fixées à l'article R. 134-4 et dans un délai de **quinze
ans**" [R9], against eight years for a euro fund's *provision pour participation aux
bénéfices* [REG-R16] — the largest smoothing advantage eurocroissance has over the euro fund
[R21]. Separately, any rate the insurer **guarantees** is subject to the art. A. 132-3
ceiling [S4] [REG-R18], keyed to the maximum technical rate of arts. A. 132-1 / A. 132-1-1
[REG-R17]. The rate used to **discount** the eurocroissance maturity guarantee is a different
and more permissive object: A. 134-1 lets the PM be computed at a rate **above the pricing
rate**, capped at 90 % of the TEC and floored at zero [R3]. A model that discounts the
guarantee at the A. 132-1 maximum technical rate has used the wrong article.

**Conduct and disclosure.** R. 134-10 fixes what must be disclosed before the first premium,
arbitrage or transfer, in "caractères très apparents": the guarantee maturity; the euro
amount of the guaranteed capital or annuity at maturity; where applicable the **absence of
any guarantee before maturity**; any non-surrender period; the maturity settlement
arrangements — plus the **minimum part value in euros**, the individualised premium for any
complementary guarantee, and the settlement, arbitrage and transfer delays [R2]. These sit on
top of the general regime: the *note d'information* and the one-page *encadré* [REG-R30], the
thirty-day *renonciation* right [REG-R29], and the annual-statement and publication duties of
L. 132-22, under which information on art. L. 134-1 engagements must be updated **at least
quarterly** and a specific statement is due **one month before** a contract's term [REG-R31].

**Taxation and social levies.** Income tax follows the ordinary assurance-vie regime of CGI
art. 125-0 A — gains taxed on *dénouement* or partial surrender, gain = sums repaid minus
premiums [R12] [REG-R40]. Converting a contract so that premiums buy unit-linked rights **or
diversification-provision rights** does **not** produce the tax consequences of a
*dénouement*, which preserves fiscal seniority on a move into eurocroissance
[R12 CGI 125-0 A I 2°](#frlib-eurocroissance-r12). Death benefits follow CGI 990 I: a €152 500 abatement per
beneficiary, then 20 % up to €700 000 of the taxable share and 31.25 % above [R12] [REG-R41].
The genuinely product-specific rule is the **social levy**: CSG/CRDS on
diversification-provision engagements is levied **"à l'atteinte de la garantie"** — when the
contractual maturity is reached — on a base of the surrender value of those engagements at
that moment less the premiums allocated to them net of premiums already included in partial
surrenders [R11 CSS L. 136-7 II 3° b)](#frlib-eurocroissance-r11). Euro-denominated rights are levied annually on
inscription; everything else on *dénouement* or death [R11]. Eurocroissance therefore sits
between the two: **no annual social-levy drag, but a levy event at maturity even if the
contract is not surrendered.**

**Macroprudential, standards, accounting.** The HCSF may, on a proposal of the Governor of
the Banque de France, **limit the payment of surrender values** and defer or restrict
arbitrages for up to six consecutive months [REG-R13]; a mass-surrender stress must respect
that ceiling. Actuarial model work falls under the Institut des actuaires' NPA 2, *Modèles
actuariels* [REG-R44]. French listed insurers report under IFRS 17 from 2023, and
eurocroissance is an archetypal direct-participating contract, so the variable fee approach
is the expected measurement model — its mechanics were not read from a retrieved text and are
[unverified] here [REG-R45].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-eurocroissance-r1
[R10]: #frlib-eurocroissance-r10
[R11]: #frlib-eurocroissance-r11
[R12]: #frlib-eurocroissance-r12
[R13]: #frlib-eurocroissance-r13
[R14]: #frlib-eurocroissance-r14
[R15]: #frlib-eurocroissance-r15
[R16]: #frlib-eurocroissance-r16
[R18]: #frlib-eurocroissance-r18
[R19]: #frlib-eurocroissance-r19
[R2]: #frlib-eurocroissance-r2
[R21]: #frlib-eurocroissance-r21
[R3]: #frlib-eurocroissance-r3
[R4]: #frlib-eurocroissance-r4
[R5]: #frlib-eurocroissance-r5
[R6]: #frlib-eurocroissance-r6
[R7]: #frlib-eurocroissance-r7
[R8]: #frlib-eurocroissance-r8
[R9]: #frlib-eurocroissance-r9
[REG-R1]: #frlib-reg-r1
[REG-R13]: #frlib-reg-r13
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R17]: #frlib-reg-r17
[REG-R18]: #frlib-reg-r18
[REG-R19]: #frlib-reg-r19
[REG-R2]: #frlib-reg-r2
[REG-R20]: #frlib-reg-r20
[REG-R21]: #frlib-reg-r21
[REG-R23]: #frlib-reg-r23
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R33]: #frlib-reg-r33
[REG-R40]: #frlib-reg-r40
[REG-R41]: #frlib-reg-r41
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[REG-R7]: #frlib-reg-r7
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
