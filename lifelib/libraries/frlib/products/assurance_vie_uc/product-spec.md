# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26; see `sources.md`).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a French `contrat d'assurance vie multisupport` in its
unit-linked dimension — savings expressed in `unités de compte` (UC, units of a
designated fund) alongside a `fonds en euros` (the insurer's guaranteed general-account
fund). It does not describe any single insurer's product. Facts carrying a source tag —
[S#] (primary product documents: `notice d'information`, `conditions générales`,
`document d'informations clés`) and [R#] (regulatory/actuarial references), both numbered
per `_research/assurance-vie-uc.md` — resolve against `sources.md` in this directory;
[REG-R#] resolves against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R-numbering). Values
marked **[std]** are standardizations introduced for the reference implementation; each
[std] table row carries a numbered footnote giving the rationale and, where the research
file recorded one, the observed range across insurers. Facts the research file could not
verify are flagged [unverified].

The implementation anchor for mechanics is the **Generali/Spirica shape** — an individual
multisupport contract with one euro support and a set of UC supports, a UC management
charge levied periodically by cancelling units, and an **optional, age-rated `garantie
plancher` charged on the `capital sous risque`** — because it is the only design for which
a public age tariff exists in more than one insurer's documents [S1] [S3] [S4] [S7]. The
flat-charge automatic-floor family [S10] [S11] [S12] [S13] is a special case of the same
recursion and is specified under Variations.

**The euro leg is a pointer, not a second implementation.** This document specifies the
euro support only as an allocation share carrying a credited rate, because that is all the
UC model needs: the euro balance sizes the `capital sous risque` and is the first source
from which the `garantie plancher` premium is levied. The `fonds en euros` mechanics —
`taux minimum garanti`, `participation aux bénéfices`, the `provision pour participation
aux bénéfices` and the `effet cliquet` — belong to `products/assurance_vie_euro/` and are
neither restated nor re-implemented here.

---

## Product overview and market role

A `contrat multisupport` is a single life insurance contract whose savings are split, at the
policyholder's election, between a `fonds en euros` and one or more `supports en unités de
compte`, with free or cheap switching (`arbitrage`) between them [S1] [S3] [S4] [S7] [S10]
[S12] [S13]. Some contracts add a third leg, `eurocroissance` engagements giving rise to a
`provision de diversification` [S2] [S4] [S11] [REG-R19]; that leg belongs to
`products/eurocroissance/` and is out of scope here.

The UC leg is where the French market has grown. In 2025 UC premiums were 75.1 bn €, 39.1%
of all life premiums and up 13.2%; UC benefits paid were 32.6 bn €; net UC inflow was
42.5 bn €, the highest on record; and UC `provisions mathématiques` closed the year at
666.4 bn €, up 13.5% [R13] [REG-R48]. That is about 32% of total assurance vie `encours`,
thirteen points above 2005, against 68% still on euro supports [R14]. Aggregate UC
performance in 2025 was +5.5%, gross of contract charges and net of fund charges, with a
five-year average of +4.9% a year [R13].

The legal foundation is art. L. 131-1 al. 2 of the Code des assurances: the guaranteed
capital or annuity **may be expressed in `unités de compte`** made of securities or assets
offering sufficient protection of the invested savings and appearing on a list set by decree
in Conseil d'État [R1]. The rule that actually drives the model, though, is a *disclosure*
obligation rather than L. 131-1 itself: art. A. 132-5 requires the information document to
state that the insurer "ne s'engage que sur le nombre d'unités de compte, mais pas sur leur
valeur", and that the unit value reflects underlying assets, is not guaranteed, and
fluctuates with the markets [R2]. Every retrieved contract reproduces that sentence, several
in a box or in bold [S1] [S3] [S4 art. 17.1.1] [S7] [S10 ART 9.A] [S13 art. 32.5]. The
consequence is mechanical and total: **the state variable is a unit count, not a euro
amount**, every contract charge on UC is applied by cancelling units, and the account value
is `units × liquidation value`.

Against that background the product's only real insurance content is the `garantie plancher`
— a floor death benefit that pays at least the premiums invested if the units have fallen.
It is where the mortality risk, the market risk and the option cost of the contract all
live, and it is why this product needs a liability model rather than a spreadsheet of
fund-based charges.

---

## Representative specification

### Contract identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual multisupport savings contract (`contrat d'assurance sur la vie individuel multisupport`), whole of life, no fixed term | [S1] [S4] [S7]; whole-of-life choice **[std]** (1) |
| Legal basis for the UC leg | Art. L. 131-1 al. 2 C. ass.; eligible supports per R. 131-1 borrowing the R. 332-2 asset classes | [R1] [R3] [R4] |
| The guarantee actually given | The insurer commits on the **number** of units, not their value — mandatory statement under art. A. 132-5 | [R2]; reproduced in [S1] [S3] [S4 art. 17.1.1] [S7] [S10 ART 9.A] [S13 art. 32.5] |
| Legal form | Individual contract; the group form with individual membership (`contrat collectif à adhésion facultative`) is a variation | individual [S1] [S4] [S7]; group [S3] [S10] [S11] [S12] [S13]; choice **[std]** (1) |
| Lives assured | Single life; joint first-death and second-death designs excluded | designs [S1] [S3] [S4]; exclusion **[std]** (2) |
| Issue ages | 18 to 85 | maximum 85 at membership [S10 ART 4B]; lower bound **[std]** (3) |
| Minimum initial premium | 500 € | [S6]; observed 100 € [S7] [S8] to 500 € [S6] |
| Premium pattern modeled | Single premium at issue; `versements libres` and `versements programmés` exist and are excluded from the base projection | availability [S1] [S4] [S7]; exclusion **[std]** (4) |
| Recommended holding period | 8 years | [S5] [S12] |
| Renonciation | 30 calendar days from the date the subscriber is informed the contract is concluded; all sums repaid within 30 days | [REG-R29] [S4] [S5] [S10] [S12] |
| Unit conversion precision | Four decimal places (`au dix millième`) | [S13 art. 32.2]; published tables carry four to five decimals [S3 art. 21] [S4 art. 17] [S7] |
| Anchor model cell | Male, age 65, single premium 100,000 €, 70% UC / 30% euro, `garantie plancher` elected on the `simple` basis | **[std]** (5) |

Footnotes to [std] rows:

1. Contracts are commonly written `viagère` (whole of life) with an option for a fixed term
   [S4 art. 4] [S7]; PRO BTP writes an initial 8 years tacitly renewed [S12] [S13] and
   Suravenir a minimum of 8 years and a maximum of 85 less the policyholder's age [S7].
   Whole of life makes the projection horizon a decrement problem rather than a contractual
   one. The individual form is chosen over the group form because the group form adds one
   degree of freedom that matters only for tariff renegotiation — MACSF may revise the
   plancher rate "en cas de modification de la composition démographique du groupe et en
   fonction des résultats techniques de la garantie" [S10 ART 8.D].
2. Joint-life plancher pricing is published: on a first-death contract the two lives'
   premiums are **added**, on a second-death contract the **lower** is charged [S1] [S3]
   [S4]. A single life keeps one attained age in the tariff lookup; enabling joint lives
   changes the lookup, not the recursion.
3. Only the upper bound is sourced (85 at membership [S10 ART 4B]). The plancher rider has
   its own tighter age gate — over 12 and under 75 [S1] [S3] [S4], 12 to under 70 [S7] —
   specified below.
4. Minimum subsequent premiums observed: 100 € for a `versement libre` with 25 € per
   support, 25 € per `versement programmé` [S7]. Excluding them keeps the floor base and the
   UC cost basis single-tranche; a later premium adds to `cum_prem_net` and to the UC cost
   basis on the same date, with no change to the recursion.
5. Pure modeling choice. Age 65 sits where the published tariff is material (196 € a year
   per 10,000 € of `capital sous risque` at Spirica [S4], 1.96% p.a. of the net amount at
   risk) while leaving ten years before the age-75 cessation; 100,000 € sits inside every
   observed premium band; the 70/30 split is the mirror image of the 70% euro / 30% UC split
   Generali uses in its own statutory illustration [S3 art. 21].

### Supports and allocation

| Parameter | Representative value | Basis |
|---|---|---|
| UC universe | `OPC` (SICAV/FCP), `OPC indiciels` (ETF), `Actions` (direct equities), real-estate UC (SCPI, SCI, OPCI), private-equity and structured supports | [S1] [S3 art. 9] [S4] [S7] [S10 ART 9.A]; statutory eligibility [R3] [R4] |
| Suitability gate on FIA supports | Required on alternative-fund and financing-vehicle units unless the fund is a retail ELTIF or the contract is under an arbitrage mandate | [R5] |
| Mandatory offering | At least one UC holding 5%–15% of ESS / venture-capital securities, and at least one UC per State-recognised green or SRI label, with disclosure of the qualifying proportion | [R6] |
| UC supports modeled | One composite UC support | **[std]** (6) |
| Euro support | One `fonds en euros`, modeled as an allocation share with a credited rate net of its own management charge; mechanics in `products/assurance_vie_euro/technical-notes.md` | scope **[std]** (7) |
| Base allocation | 70% UC / 30% euro of the net premium | **[std]** (5) |
| Support-level rules not modeled | Real-estate concentration cap of 60% per premium or arbitrage [S13 art. 32.6]; reinvestment of distributed income into the support, increasing the unit count [S13 art. 32.3] [S4]; substitution of a support that disappears [R3 III](#frlib-assurance_vie_uc-r3) [S7]; redemption gating under arts. R. 131-8 to R. 131-12 [R7] | **[std]** (6) |

6. The reference model collapses the fund menu to one composite UC support with an
   exogenous liquidation value. The concentration cap [S13 art. 32.6], the bid/offer spreads
   on `Actions` and ETF [S4], reinvested distributions [S13 art. 32.3] and the gating rules
   [R7] all need support-level modeling, and none of them changes the shape of the liability
   — they change the path of one input. The `garantie plancher` is contract-level in every
   retrieved design except Afer's, which computes it support by support against a running
   average cost price (see Variations), so a single-support model is exact for the composite
   and an approximation for Afer.
7. Deliberate scope boundary, restated from the scope note. `euro_credit_rate` is the annual
   rate credited to the euro support **net of the euro management charge**, because that is
   the rate French insurers publish and the rate the euro model produces. The euro leg
   therefore contributes no margin line here; reading `net_cf` as the contract's total
   margin is a modeling error and is listed as such in the technical notes.

### Charges

| Parameter | Representative value | Basis |
|---|---|---|
| `Frais sur versement` (premium charge) | 1.00% of each premium, deducted before allocation | level **[std]** (8) |
| UC `frais de gestion sur encours` | 0.88% p.a. of the UC savings, levied **monthly by cancelling units** | level **[std]** (9); levy mechanics [S7] [S13 art. 32.4] |
| Euro `frais de gestion` | 0.66% p.a., embedded in `euro_credit_rate` | level **[std]** (9) |
| `Frais d'arbitrage` | 0.50% of the amount switched | [S13]; level **[std]** (10) |
| `Gestion pilotée` surcharge | +0.29% p.a. on UC; off in the base cell | [R13]; level **[std]** (11) |
| Fund-level recurring costs inside the UC | 1.60% p.a., borne within the fund — not insurer income | [R13]; use as a model input **[std]** (12) |
| Exit charge on surrender or death | Nil | [S1] [S3] [S4] [S7] [S10] [S11] [S13] |
| Charges not modeled | Annuity instalment charge 3% [S7] [S13]; insurer bid/offer spreads ±0.60% on `Actions` and ±0.10% on ETF [S4] [S7]; automatic-arbitrage option charge 0.50% of the amount transferred [S1], 1% on `sécurisation des plus-values` [S3], free [S4] [S13]; illiquid-UC disinvestment penalty 3% within three years of investment and ten of membership and 5% in the art. R. 132-5-3 cases [S10 ART 8.E] | **[std]** (6) |
| Charge disclosure regime | Per-UC table with ISIN, gross performance N−1, support fees, contract fees, **total fees** and retrocession rate, mandatory since 1 July 2022 | [R9]; instances at [S6] [S8] |

8. Observed `frais sur versement`: 4.50% maximum [S1]; nil [S3] [S4] [S6] [S7] [S8]; up to
   3% at the insurer's discretion [S13]; 3% on the euro fund and 1% on UC, 0.6% by direct
   debit [S10]; 0.5% on the euro fund and **nil on UC** [S11]. 1.00% is chosen as a non-zero
   mid-range level, because a zero premium charge makes the net-premium and gross-premium
   floor bases indistinguishable and hides the question the plancher definition turns on.
9. Anchored on the market average, not on the sample. France Assureurs reports the
   `encours`-weighted average **contract charge on UC of 0.88%** in 2025 — 0.82% for
   `gestion libre` and predefined allocations, 1.17% under `gestion sous mandat` — against
   **0.66% on euro supports** and 0.73% all in [R13] [R14] [REG-R48]. Contract-level rates
   retrieved run 0.475% [S11], 0.50% [S4] [S6], 0.50% including 0.20% of plancher financing
   plus a separate 0.10% cotisation [S10], 0.60% and 0.80% [S7] [S8], 0.75% [S3], 0.80%
   including plancher financing [S13], and 1.00% rising to 1.50% on ETF and direct equities
   [S1]. **No statutory ceiling on any French life charge appears in the retrieved texts** —
   art. A. 132-8 requires maxima to be *disclosed*, not capped [REG-R30] — which is why
   every charge level here is **[std]**.
10. Observed `frais d'arbitrage`: 1% with a 30 € postal / 15 € online minimum [S1]; nil
    online, 15 € per paper arbitrage after two free a year [S4] [S6]; 2% towards the euro
    fund and 0.20% towards UC with twelve free [S10]; **nil in all cases** [S11]; 0.5% in
    `gestion libre` with three free, free in the managed modes [S13]; not applicable [S8].
    0.50% is the PRO BTP level [S13] and sits in the middle. Flat-fee minima are
    administrative and do not scale, so they are not modeled.
11. The market spread between `gestion sous mandat` (1.17%) and `gestion libre` (0.82%) is
    35 bp [R13]; against the 0.88% all-UC average the surcharge is 29 bp. Contract-level
    surcharges retrieved: +0.60% [S1]; +0.20% to +0.70% by profile [S4] [S6]; +0.20% [S7]
    [S8]; +0.30% on both legs [S13]. The base cell runs `gestion libre`.
12. Not an insurer cash flow. Fund-level recurring costs reduce the liquidation value and
    therefore the account value, but they accrue to the fund manager, and only the
    retroceded share reaches the distributor. Averages over each insurer's own shelf: equity
    funds including ETF 1.87% of which 0.80% retroceded, bond 1.18% (0.53%), diversified
    1.90% (0.80%), real estate 1.12% (0.28%), unlisted 3.17% (0.78%) [S6]; and 1.23%
    (0.34%), 1.59% (0.49%), 2.41% (0.61%), 2.71% (0.62%), 0.98% (0.97%), structured 0.00%
    [S8]. These are contract-specific and not comparable like for like; the market
    `encours`-weighted average is 1.60% [R13]. The model carries them inside the unit-return
    scenario.

### Garantie plancher — the floor death benefit

| Parameter | Representative value | Basis |
|---|---|---|
| Availability | Optional rider, elected **at subscription only**, cancellable but not restartable | [S1] [S3] [S4] [S7]; the automatic form financed inside the management charge is [S10] [S11] [S12] [S13] — see Variations |
| Entry ages | Over 12 and under 75 | [S1] [S3] [S4]; 12 to under 70 [S7] |
| Cessation | The 75th birthday; also on total surrender, payment of the benefit, cancellation by either party | [S1] [S3] [S4] [S7] [S11]; 70 [S10]; 80 [S12] [S13] |
| Waiting period (`délai de carence`) | None | [S1] [S3] [S4]; one year [S7]; choice **[std]** (13) |
| Floor basis `simple` | Cumulative premiums **net of `frais sur versement`**, less partial surrenders and unrepaid `avances` with their interest | [S4 Annexe I] [S10 ART 10]; gross-premium variant [S1] [S3] [S13]; choice **[std]** (14) |
| Floor basis `indexee` | The same base indexed at **3.50% p.a.**, surrenders indexed on the same basis | rate and rule [S1] [S3] [S2]; applying them to the **net**-premium base above is **[std]** (14) |
| Floor basis `cliquet` | Ratchet to the highest account value observed at each ratchet date, reduced pro rata by partial surrenders, never below the `simple` floor | **[std]** (15) [unverified] |
| `Capital sous risque` (net amount at risk) | `max(0, floor − account value across all supports)`, capped at **300,000 €**; any excess reduces the floor | [S1] [S3] [S4]; 100,000 € per contract [S7]; no cap stated [S11] [S13] |
| Charge basis | An annual tariff per 10,000 € of `capital sous risque`, by **attained age at the calculation date** | [S4 Annexe I] [S1] [S3] [S7] |
| Charge formula as published | `Pr = K × (PA / 10 000) × 1/52`, computed each Friday, K the `capital sous risque` that day, PA the annual tariff for the attained age | [S4 Annexe I] |
| Charge formula modeled | `plancher_charge(t) = nar(t) × plancher_rate(age) / 12`, observed and levied monthly | **[std]** (16) |
| When the charge is zero | Whenever the account value is at or above the floor — the rider is a put and costs nothing out of the money | [S3 art. 21] [S4 art. 17.1.2] |
| Levy source and order | Monthly, in arrears, **first from the euro support**, then from the largest UC support by cancelling units | [S1] [S3] [S4]; Suravenir accumulates and levies by 31 December [S7] |
| Machinery not modeled | Minimum levy threshold 20 €/month deferred [S4], 15 € [S1] [S3]; unpaid premiums recovered from the benefit, with suspension, 40 days' notice and cancellation on default [S1] [S3] [S4]; exclusions — suicide in the first contract year, war, aviation and dangerous sports, the insured's intentional act, murder by the beneficiary (art. L. 132-24), with IAD expressly excluded [S4] and a longer list at [S7] | **[std]** (17) |
| Effect on minimum surrender values | Where the plancher is in force there are **no minimum surrender values expressed in euros**, and the deductions are capped neither in euros nor in units; art. A. 132-4-1 worked examples replace the table | [S4 art. 17.1.2] [S7] |

13. Only Suravenir imposes a waiting period, as part of a differently shaped rider that pays
    the `capital sous risque` itself [S7]. Zero keeps the first policy year on the same
    recursion as every later year; a non-zero `waiting_months` is a gate on `nar(t)`, not a
    new formula.
14. Both bases are sourced and they differ by the premium charge. Net premiums: Spirica's
    guaranteed capital is the sum of net premiums on all supports less surrenders, `avances`
    and unpaid interest [S4 Annexe I]; MACSF's death capital may not be less than total
    premiums net of entry charges since membership, less partial surrenders and outstanding
    advances [S10 ART 10]. Both are recorded in `_research/assurance-vie-uc.md` as summaries
    of the retrieved text rather than as transcribed wording, so neither is quoted here.
    Gross premiums: Generali options 1 and 2 [S1] [S3], PRO BTP [S13 art. 8.2]. Net is chosen
    because it makes the floor equal to the account value at issue, so the rider starts
    exactly at the money and `nar(0) = 0` is an assertable fact rather than an accident of
    the premium charge. The `indexee` row indexes this **net** base at 3.50%: the rate and
    the rule that surrenders are indexed on the same basis are Generali's option 2 [S1] [S3]
    [S2], but Generali applies both to a **gross**-premium base [S1] [S3], so the pairing
    shipped here is a **[std]** hybrid — no retrieved document indexes a net base at 3.50%.
15. **No retrieved document offers a ratchet.** The three indexation designs actually seen
    are none (Generali option 1, Spirica, MACSF, Suravenir, Afer), a fixed 3.50% p.a.
    (Generali option 2 [S1] [S3]) and a **discretionary** annual rate set by the insurer (PRO
    BTP [S12] [S13 art. 8.2]). `cliquet` is introduced here as a standardization so the model
    carries the three-way `plancher_basis` column, and its existence in the French market is
    [unverified]. Its ratchet period is a parameter, default 12 months. It differs from
    `simple` in two ways, both asserted in the worked example: it locks in account-value
    highs at each ratchet date, and it adjusts for a partial surrender **proportionally**
    (a ratchet is a value level) rather than by the nominal amount surrendered.
16. 1/12 of the annual tariff replaces the published 1/52 weekly step. On the published
    formula the monthly levy is the sum of the 52/12 = 4.3333 weekly premiums observed in the
    month; `PA/12` is the same annual cost applied once against a `capital sous risque`
    observed once instead of four or five times. What is lost is the intra-month path of the
    net amount at risk. Observation frequency in the sources: each Friday [S3] [S4], each
    Tuesday [S1], each month end [S7].
17. Threshold deferral, unpaid-premium recovery, the 40-day suspension procedure and the
    exclusions have no expected-value consequence at single-policy granularity: a deferred
    levy is collected the following month, an unpaid premium is recovered from the benefit,
    and the exclusions are a small negative adjustment to the death rate that no retrieved
    document quantifies. They are recorded so a portfolio implementation can add them.

Published tariffs, annual premium per 10,000 € of `capital sous risque` by attained age
(selected ages; the full tables run 12–74 for Generali and Spirica and 12–75 for Suravenir
and are reproduced in `_research/assurance-vie-uc.md` §7, which is the provenance of the
shipped rate table):

| Attained age | Generali [S1] [S3] | Spirica [S4] | Suravenir [S7] (monthly per 1,000 € rebased ×120) |
|---|---|---|---|
| ≤ 30 | 12 € | 17 € | 18 € |
| 35 | 15 € | 21 € | 24 € |
| 40 | 24 € | 28 € | 36 € |
| 45 | 40 € | 41 € | 60 € |
| 50 | 58 € | 61 € | 88.8 € |
| 55 | 82 € | 96 € | 124.8 € |
| 60 | 115 € | 140 € | 172.8 € |
| 65 | 172 € | 196 € | 258 € |
| 70 | 266 € | 285 € | 399.6 € |
| 74 | 377 € | 408 € | 565.2 € |

Expressed as annual rates on the `capital sous risque` the three tariffs run 0.12%–3.77%
(Generali), 0.17%–4.08% (Spirica) and 0.18%–6.18% (Suravenir), rising roughly geometrically
at 8%–10% a year over ages 40–74 — consistent with a mortality loading, but **no insurer
publishes the mortality table, the age definition, the expense loading or the margin behind
the tariff**, so the implied `qx` cannot be recovered from these documents. Suravenir's table
is printed as a monthly premium per 1,000 €; its `encadré` separately describes the cover as
"de 0,15 ‰ à 5,15 ‰ des capitaux sous risque", and the monthly-versus-annual reading of that
‰ phrasing is [unverified] [S7]. The reference implementation ships the **Spirica** column
[S4], the only tariff published together with an explicit premium formula.

### Surrender, partial surrender and arbitrage

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender right | At any time after the renonciation period; settlement within two months at most (art. L. 132-21), late payment bearing 1.5 × the legal rate for two months then twice | [REG-R31] [S10 ART 13]; contractual 30 days [S4] [S11] |
| Surrender value | Account value across all supports; no exit charge | [S1] [S3] [S4] [S7] [S10] [S11] [S13] |
| Partial surrender allocation | **Pro rata across supports** unless the policyholder elects otherwise; always pro rata when repaying an `avance` | [S10 ART 13.A]; default choice **[std]** (18) |
| Effect on the floor | The floor base is reduced by the amount surrendered (indexed on the same basis where `indexee`) | [S1] [S3] [S4 Annexe I]; capital-component variant [S13 art. 8.2] |
| Minimum surrender values | Tabulated for the first eight years, expressed **in number of units** for UC | [S3 art. 21] [S4 art. 17] [S7] [S10 ART 12.A] [S11]; the attribution of the duty to art. L. 132-5-2 is [unverified] here — the [REG-R29] entry covers that article's `note d'information` duty and eight-year renonciation-sanction cap and does not carry the tabulation |
| Base arbitrage pattern | One 10,000 € euro → UC arbitrage at month 3 in the worked cell | **[std]** (19) |
| Frictions not modeled | Arbitrage minimum 100 € with a 100 € residual [S7]; deferral of arbitrages out of a euro fund or real-estate UC for up to six months, and the insurer's right to limit investment into the euro fund [S7] [S10 ART 15]; value dating at J+3 for the UC leg of a total surrender [S10 ART 12.B–12.C]; `avances` capped at 60% of the UC savings at TME + 1% reset quarterly [S13 art. 33], always deducted from the plancher benefit [S1] [S3] [S4] [S7] [S10] [S13]; the HCSF's power to limit surrender payments for up to six consecutive months and to defer or restrict arbitrages and advances [REG-R13] | **[std]** (6) |

18. Pro rata is the only default stated in a retrieved contract [S10 ART 13.A], and MACSF
    excludes SCPI and private-debt UC from it. In a one-UC-support model pro rata across the
    euro and UC legs is the whole of the rule; with several UC supports it becomes a
    per-support split, and an election that empties the loss-making support first would
    change the UC cost basis and therefore the `prélèvements sociaux`.
19. A single euro → UC arbitrage exercises the three things only an arbitrage does: it moves
    value between the two legs without touching the floor, it buys units at the current
    liquidation value, and it generates a fee. A programmed arbitrage pattern is specified in
    the technical notes.

### Prélèvements sociaux and policyholder tax

| Parameter | Representative value | Basis |
|---|---|---|
| `Prélèvements sociaux` rate | **17.2%** — CSG 9.9%, CRDS 0.5%, prélèvement social 4.5%, contribution additionnelle 0.3%, prélèvement de solidarité 2.0% | [S4 Annexe II] |
| **UC timing** | Levied **only at `dénouement`** — partial or total surrender, term, or death of the insured — never year by year | [R8 II, 3°, c)](#frlib-assurance_vie_uc-r8) [S4 Annexe II] |
| **Euro timing** | Levied **annually**, when interest is credited to the contract | [R8 II, 3°, a)](#frlib-assurance_vie_uc-r8) [S4 Annexe II] |
| `Eurocroissance` timing | When the guarantee is reached; on death or total surrender, on the gains at that date | [R8 II, 3°, b)](#frlib-assurance_vie_uc-r8) [S4 Annexe II] |
| Restitution | Where the contract's final liquidation produces a negative base, the excess already levied under a) and b) is returned by set-off or reimbursement | [R8 III bis](#frlib-assurance_vie_uc-r8) |
| Taxable UC base at partial surrender | `W_uc × (1 − cost_basis / av_uc)` — the surrendered amount less its pro-rata cost | **[std]** (20) |
| Income tax on gains | PFONL 12.8% under eight years, 7.5% at or beyond, taken as a payment on account; then 7.5% on gains attributable to premiums up to 150,000 € and 12.8% above, with a 4,600 € / 9,200 € annual `abattement` | [S4 Annexe II] [REG-R40]; the 150,000 € threshold is [unverified] against the article text [REG-R40] |
| Death duties | CGI art. 990 I for premiums paid before age 70 — 152,500 € allowance per beneficiary, 20% then 31.25% above 700,000 €; CGI art. 757 B for premiums after 70 — ordinary succession duties on the premiums above a 30,500 € aggregate allowance | [S4 Annexe II] [S10 ART 19] [REG-R41] |
| Contract exempt from `taxe d'assurance` | Art. 995 CGI | [S10 ART 19] |
| Treatment of the plancher top-up | Outside the UC social-levy base | **[std]** (21) [unverified] |

20. The formula is the pro-rata-cost method implied by the general rule that the taxable
    `produit` of a partial surrender is the amount surrendered less the corresponding share
    of premiums. It is applied here to the **UC leg only**, because only the UC leg is taxed
    at `dénouement` [R8 II, 3°, c)](#frlib-assurance_vie_uc-r8). No retrieved document sets out the arithmetic for a
    multisupport partial surrender, so the split of a pro-rata surrender into a euro
    component already taxed and a UC component taxed now is a standardization.
21. No retrieved document states whether the amount paid **above** the account value under
    the `garantie plancher` is a `produit de placement` within art. L. 136-7 or a pure
    insurance benefit outside it. The model treats it as outside the levy base and flags the
    treatment [unverified]; the alternative reading changes the beneficiary's net proceeds,
    not the insurer's cash flow.

---

## Contractual mechanics

**Premium, allocation and the unit count.** A premium `P` is reduced by the `frais sur
versement` and the remainder is allocated across the supports on the policyholder's
instruction [S1] [S4] [S7] [S10] [S13]. The UC share buys units at the support's
liquidation value: `units = allocated amount / unit_price`, to four decimal places
[S13 art. 32.2]. From that point the insurer's commitment is the unit count [R2]. Every
UC charge in every retrieved contract is expressed as a percentage and applied by
**cancelling units** — quarterly at Generali and Spirica [S1] [S3] [S4], monthly at
Suravenir and PRO BTP [S7] [S13 art. 32.4], annually on 31 December at MACSF
[S10 ART 12.A]. Because the charge cancels units rather than deducting euros, the unit
count is a **deterministic, market-independent decreasing sequence** and the euro account
value is `units × unit_price`. The insurers publish that sequence themselves: Bourso Vie's
statutory eight-year table runs 100 → 99.2521 → 98.5098 → 97.7731 → 97.0418 → 96.3161 →
95.5957 → 94.8808 → 94.1711 units at 0.1875% a quarter [S3 art. 21], and Himalia's
0.25% a quarter gives 99.0037 → 98.0174 [S2]. Those are exactly `(1 − c/4)^{4y}`.

**UC management charge.** The composite levies `mgmt_fee_rate_uc / 12` of the units held at
the start of each month, cancelling `units × c/12` units and realising
`units × c/12 × unit_price` of charge income [S7] [S13 art. 32.4]. PRO BTP's is the most
explicit operative wording retrieved: the charge "ne peut dépasser 0,80 % par an de
l'épargne constituée sur chaque support en unités de compte", is computed on the number of
units held at the end of each calendar month, is levied at the next valuation date, reduces
the number of units held, and is **no longer levied beyond the 80th birthday**
[S13 art. 32.4]. Suravenir accrues daily on the daily balance and levies monthly in units
[S7].

**Arbitrage.** A switch between supports moves value without changing the contract's premium
history. The amount leaving the source support is reduced by the `frais d'arbitrage` and the
net amount buys units on the destination support at its liquidation value [S1] [S4] [S7]
[S10] [S13]. It is **not** a premium and **not** a surrender, so it leaves the `garantie
plancher` floor untouched — worth stating because both legs of the contract change and the
floor does not. Automatic arbitrage options are described under Riders and are excluded from
the base recursion.

**Garantie plancher.** On the insured's death before the cessation age the contract pays
at least the floor:

    death benefit = max(plancher_amount, account value)
                  = account value + capital sous risque

with `capital sous risque = min(cap, max(0, plancher_amount − account value))` and the cap
at 300,000 €, any excess reducing the floor [S1] [S3] [S4]. The identity in the second line
is the whole of the modeling content: **the insurer's death strain is exactly the net
amount at risk**, and it is zero whenever the units are worth more than the floor. The
charge is levied on that same net amount at risk, not on the account value: Spirica's
published formula is `Pr = K × (PA / 10 000) × 1/52` with `K` the `capital sous risque`
observed each Friday and `PA` the annual tariff for the attained age [S4 Annexe I], and
both Bourso Vie and Spirica state that where the account value exceeds the guaranteed
capital the cost is nil [S3 art. 21] [S4 art. 17.1.2].

Generali's own statutory illustration is the cleanest numeric evidence that the charge is
path-dependent. On a 10,000 € premium split 70% euro / 30% UC for an insured aged 50 with
option 1, the euro fund's year-1 surrender value is 6,947.50 € in the rising-UC scenario —
exactly `7,000 × (1 − 0.75%)`, so the plancher cost is **zero** — against 6,945.49 € in the
falling-UC scenario, a year-1 plancher cost of 2.01 € taken from the euro fund; by year 8
the comparison is 6,590.86 € versus 6,507.00 €. Under option 2 (3.50% indexation) the
year-1 figures are 6,945.82 € rising and 6,943.31 € falling, so even in the rising scenario
the indexed floor bites [S3 art. 21].

**Death, valuation and settlement.** Contracts differ on how the account value is measured
after death. Bourso Vie states that after death both the euro fund and the UC continue to
be valued until the settlement valuation date, so **UC values keep fluctuating up and down
after death** [S3 art. 19]; Afer fixes valuation to the Wednesday liquidation value
following receipt of the death certificate [S11]; Suravenir measures the `capital sous
risque` at the date the certificate is received [S7]. Art. L. 132-5 requires the capital to
be revalorised from the date of death until receipt of the L. 132-23-1 documents or deposit
with the Caisse des dépôts, at not less than a rate fixed by decree — a rate the fetched
article text does not expose [R11] [unverified]. Art. L. 132-23-1 gives the insurer fifteen
days to request the documents and one month from the complete file to pay [REG-R31]; the
version retrieved for the product file is the pre-2016 text, so any post-loi-Eckert detail
is [unverified] [R12]. The composite models a single settlement in the month of death and
carries the post-mortem valuation window as an unmodeled friction.

**Surrender and partial surrender.** A total surrender pays the account value across all
supports with no exit charge [S1] [S3] [S4] [S7] [S10] [S11] [S13] and ends the `garantie
plancher` [S1] [S3] [S4] [S11]. A partial surrender is allocated pro rata across the
supports by default [S10 ART 13.A], cancels units on the UC leg at the current liquidation
value, and reduces the floor base by the amount surrendered [S1] [S3] [S4 Annexe I]. Where a
beneficiary has formally accepted the benefit under art. L. 132-9 the contract becomes
unavailable and any surrender needs that beneficiary's express agreement [S10 ART 13.A].

**Prélèvements sociaux — the deliberate asymmetry.** This is the mechanic that most
distinguishes a French multisupport contract from a UK unit-linked bond, and it is statutory,
not an insurer choice. Art. L. 136-7 II, 3°, a) applies the levy "lors de leur inscription au
bon ou contrat" — annually, as interest is credited — for contracts whose rights are
expressed in euros **and for the euro-denominated component of a multisupport contract**;
II, 3°, c) applies it "lors du dénouement des bons ou contrats ou lors du décès de l'assuré"
for everything not already taxed, which is the unit-linked component [R8]. So on one contract
the social-levy cash flow has an annual component sized on the euro leg's credited interest
and a terminal component sized on the UC gain, and III bis provides restitution of the excess
where the final liquidation produces a negative base [R8] — the mechanism that refunds an
over-levied euro contribution on a contract whose UC leg has lost money. The two must be
modeled separately, and the UC component is contingent on a **gain**: on a UC loss it is zero.

**Information and renonciation.** The one-page `encadré` at the head of the proposal or
notice must state the contract type, the guarantees with a prominent statement that
unit-linked amounts are **not guaranteed and are subject to market fluctuations**, the
participation aux bénéfices, surrender availability and payment period, fees in four
categories **with maximum amounts or percentages**, the recommended holding duration,
beneficiary designation and a closing disclaimer [REG-R30]. The annual statement must show,
per support, the number of units held and their value at the last valuation date, and whether
the plancher has been renewed [S13 art. 19] [REG-R31]. Renonciation is 30 calendar days,
extended to 30 days after actual delivery of the note d'information where it was not
delivered, capped at eight years [REG-R29] [S5] [S12].

---

## Riders and options

**In scope, specified and enabled in the base cell:**

- **`Garantie plancher`** — the floor death benefit specified above. It is the only
  guarantee the reference model prices.

**In scope, specified and disabled in the base cell [std]:**

- **Automatic arbitrage options.** Five families appear, all implemented as scheduled
  arbitrages with a trigger rule. *`Investissement progressif`*: monthly arbitrages out of
  the euro fund into chosen UC, executed on the first Friday, minimum 100 € per arbitrage
  and 50 € per destination [S4 art. 11.2.1] [S7] [S13]. *`Sécurisation des plus-values`*:
  when the gain over an `assiette` exceeds a threshold of 5%, 10%, 15% or 20%, the whole
  observed gain is switched to a money-market support, observed each Friday and executed the
  following Monday, at 0.50% of the amount transferred [S1] [S4 art. 11.2.2] [S7]; Afer's
  published worked example resets a `valeur de référence` to
  `(100 × 20 + 40 × 25)/140 = 21.43 €` on a new investment, then switches
  `(28 − 21.43) × 140 = 920 €` of gain, which at the next day's 28.20 € is 32.62 units
  [S11 Annexe 4]. *`Limitation des moins-values`* in absolute and trailing forms, the
  trailing reference being the **highest** liquidation value reached since setup, minimum
  threshold 5% [S1 art. 14.4] [S4 art. 11.2.3] [S7] [S9]. *`Rééquilibrage automatique`* to a
  target allocation [S4 art. 11.2.4] [S7]. *`Dynamisation des intérêts`*: a chosen share of
  the previous year's euro-fund interest, net of charges and social levies, switched into UC
  each January [S11 Annexe 4] [S1] [S7]. Combination rules differ by insurer [S1] [S4] [S7].
- **`Gestion pilotée` / `mandat d'arbitrage`.** A delegated allocation at +0.20% to +0.70%
  p.a. [S1] [S4] [S6] [S7] [S8] [S13]. Modeled as a rate change on `mgmt_fee_rate_uc`, not
  as a new mechanic. At Generali ETF and direct equities are unavailable under it and no
  automatic arbitrage option may be combined with it [S1].

**Out of scope (listed):**

- `Garantie vie universelle` and `garantie vie entière` riders [S1] [S3]. The 500,000 €
  `capital sous risque` cap on the `vie universelle` is stated in Bourso Vie's Annexe 3
  alone [S3]; Himalia lists the two riders with no cap [S1].
- **IFTD trigger.** MACSF's automatic floor is triggered not only by death but by
  `Invalidité Fonctionnelle Totale et Définitive` — third-category Social Security
  invalidity, the surrender to be claimed within one year [S10 ART 10]. Adding it is a
  second decrement on the same net amount at risk.
- `Eurocroissance` engagements and the `provision de diversification` [S2] [S4] [S11]
  [REG-R19] — see `products/eurocroissance/`. Where present, the plancher may still be taken
  below age 75, at least 10% of the `valeur atteinte` must stay on the euro fund so the
  premium can be levied, and the premium is never levied on the `fonds croissance` [S2].
- Annuity conversion, at a 3% charge per instalment [S7] [S13] — see
  `products/rente_viagere/`.
- `Remise de titres` (settlement in securities) at 1% of the funds so settled [S7],
  available in the three cases of L. 131-1 with the no-voting-rights and 10%-holding
  restrictions [R1].
- `Avances` [S13 art. 33] and `nantissement` [S10 ART 15] [S4] [S7].
- Capitalisation contracts (`contrat de capitalisation`), said to mirror the same UC
  mechanics without the death benefit — **no capitalisation conditions were retrieved**, so
  every statement about them is [unverified].

---

## Variations across insurers

1. **Optional rider versus automatic cover.** Generali [S1] [S3], Spirica [S4] and Suravenir
   [S7] sell the plancher as an optional rider elected at subscription and priced by an
   explicit age-rated risk premium on the `capital sous risque`. MACSF [S10], Afer [S11] and
   PRO BTP [S12] [S13] grant it automatically and finance it inside the management charge.
   Chosen: the optional, age-rated form — the only one whose price is public, and the only
   one that isolates the option cost as its own cash flow. The automatic form is the same
   recursion with `plancher_rate` a flat, age-independent constant folded into
   `mgmt_fee_rate_uc`: MACSF's all-in cost is 0.30% p.a. of UC (0.10% explicit `cotisation`
   plus 0.20% of the 0.50% management charge), charged only to the year of the 70th birthday
   [S10 ART 8.B, 8.D]; Afer's is 0.055% p.a., "mutualisé entre tous les adhérents" and
   **explicitly independent of the member's age** [S11]; PRO BTP publishes no separate figure
   at all, the floor being financed inside the 0.80% UC charge [S13 art. 32.4].
2. **What the floor is measured against.** Gross premiums [S1] [S3] [S13]; net premiums [S4]
   [S10]; the `capital sous risque` itself as the benefit [S7]; and, uniquely, Afer's
   **per-support** floor of `number of units × PRUM`, the `prix de revient unitaire moyen`
   recomputed at every investment as a units-weighted average and left unchanged by
   surrenders — `(500 × 20 + 2000 × 21)/2500 = 20.80 €`, then
   `(2302 × 20.80 + 50 × 22.50)/2352 = 20.84 €` in its published example [S11 Annexe 3].
   Chosen: contract-level net premiums. The PRUM design is a genuinely different liability —
   a strip of per-support puts rather than one contract-level put — and deserves its own
   model point flag if an Afer-shaped book is in scope.
3. **Indexation of the floor.** None [S4] [S7] [S10] [S11]; fixed 3.50% p.a. [S1] [S3]; a
   rate set annually at the insurer's discretion [S12] [S13 art. 8.2]. Chosen: `simple` in
   the base cell with `indexee` at 3.50% as a parameterised variant. The discretionary form
   is a class-(b) insurer-discretionary element in the technical notes, not a contractual
   one, and the model holds the snapshot rate.
4. **Cessation age and cap.** Cessation: 70 [S10]; 75 [S1] [S3] [S4] [S7] [S11]; 80 [S12]
   [S13]. Chosen: 75 — and the choice matters more than it looks, since on the shipped
   Spirica tariff the rate at 74 is 408/17 = **24×** the rate at ages 12–30 [S4], and the
   other two published tariffs are steeper still (Generali 377/12 and Suravenir 565.2/18,
   both 31×), so the last five years carry a large share of the lifetime charge and
   extending to 80 runs past the last published age. Cap: `capital sous risque`
   capped at 300,000 € [S1] [S3] [S4]; 100,000 € per contract [S7]; MACSF caps the
   **premiums** covered at 762,245 € across all its UC contracts [S10]; no cap stated [S11]
   [S13]. Chosen: 300,000 €, the majority value. It never binds on the anchor cell; it binds
   on large contracts in deep drawdowns, exactly where the guarantee matters.
5. **Levy frequency on UC, waiting period, `frais sur versement`.** Levy: quarterly [S1]
   [S3] [S4]; daily accrual with a monthly levy [S7]; monthly on end-of-month units [S13];
   annually on 31 December [S10]; not stated for UC in the retrieved Afer pages [S11].
   Chosen: monthly, matching the model's grid — the difference is second-order but
   systematic, and it is a named pitfall in the technical notes. Waiting period: none [S1]
   [S3] [S4] [S10] [S11] [S13], one year at Suravenir in exchange for no medical formalities
   [S7]; chosen: none. `Frais sur versement`: 4.50% maximum [S1] down to nil [S3] [S4] [S6]
   [S7] [S8], and nil on UC with 0.5% on the euro leg [S11]; chosen 1.00% **[std]**
   (footnote 8).
6. **Bancassurance is missing from the sample.** Cardif's key-information portal returned a
   page shell with the document list rendered client-side, and Sogécap, AXA, CNP and Predica
   were not reached. The sample is therefore weighted towards broker/online and
   mutual/association contracts, which are cheaper than the market average [R13]. Charge
   levels here are anchored on the France Assureurs averages [R13] [R14] [REG-R48], not on
   the sample mean, and any statement about bancassurance charge levels is [unverified].
7. **Document vintages vary.** Himalia [S1] and Afer [S11] are October 2021, Suravenir [S7]
   April 2022, Spirica's conditions [S4] July 2024, MACSF [S10] carries October 2024 file
   metadata, PRO BTP's DIC [S12] May 2025 and Spirica's KID [S5] July 2026; Bourso Vie [S3]
   carries no date at all in its extracted text. Charge levels and tariffs move, and the
   France Assureurs series [R13] is the only 2025-vintage market-wide figure. Afer's
   retrieved notice names Aviva Vie and Aviva Épargne Retraite as co-insurers [S11]; that
   business has since been sold and rebranded, and the current names are [unverified].

---

## Regulatory context

**Unit-linked law.** Art. L. 131-1 permits the guaranteed capital or annuity to be expressed
in `unités de compte` made of securities or assets offering sufficient protection and
appearing on a decree list; settlement is normally in cash, with delivery of the underlying
securities permitted in three cases and barred where the securities confer voting rights or
where the policyholder and connected persons have held more than 10% of the issuer in the
preceding five years [R1]. The eligibility list is R. 131-1, which admits the R. 332-2 asset
classes — OECD sovereign bonds, regulated-market securities and corporate debt, SICAV shares
and FCP units, listed equities, insurance-company shares — plus, on the conditions of
R. 131-2 to R. 131-4, the real-estate vehicles of 9° bis [R3] [R4]. R. 131-1 II imposes
concentration limits per unit type; the percentages reported in the research file come from
a paraphrased fetch rather than verbatim article text and are **not quoted here** [R3].
Alternative-fund and financing-vehicle units require a suitability gate unless the fund is a
retail ELTIF or the contract is under an arbitrage mandate [R5], and every multisupport
contract must reference at least one UC holding 5%–15% of social-economy or venture-capital
securities and at least one UC per State-recognised green or SRI label [R6].

**Redemption gating.** Arts. R. 131-8 to R. 131-12 govern a suspended fund: the restriction
applies only to requests made after the fund's last order centralisation before suspension;
unexecuted requests roll forward if the fund values daily or more often and are otherwise
cancelled; the insurer may not apply a liquidation value lower than the last published one;
any proportional restriction it applies must be at least as favourable as the fund's own;
the policyholder must be informed without delay on a durable medium and the measures are
unenforceable against a client who was not advised of them; the ACPR must be notified; and
quarterly-disclosed estimated values may be used where no current value exists [R7].

**Prudential.** Technical provisions under Solvabilité II are a best estimate plus a risk
margin, the best estimate being the probability-weighted average of future cash flows
discounted at the relevant risk-free term structure [REG-R1] [REG-R4] — stated on EIOPA's
authority, since EUR-Lex could not be fetched and no Solvency II article number in this
library was read from the instrument [REG-R1] [REG-R2]. On the French statutory balance
sheet art. R. 343-3 enumerates eleven technical provisions and defines the **provision
mathématique** as the difference between the actuarial present values of the insurer's and
the insured's respective commitments, including future management costs [REG-R6]. It does
**not** say which of the eleven carries a `unités de compte` engagement, nor that a UC
engagement is measured as a unit count at the liquidation value, and no retrieved statutory
or ACPR text does — so the conventional reading is [unverified], with MACSF's notice, which
writes its own `provision mathématique` and surrender values in units, the closest retrieved
support [S10 ART 11–12]. On that reading a French UC model's first liability measure is
arithmetic and its second, the plancher liability, is not. **No retrieved ACPR or insurer document
states how the `garantie plancher` liability is valued** — closed-form option valuation,
stochastic projection or unearned premium — and `acpr.banque-france.fr` returned HTTP 403 to
every request, so this library asserts nothing about it. The mortality basis a French tariff
may use is fixed by art. A. 335-1: tables homologated by ministerial arrêté, by sex,
established on INSEE data for non-annuity contracts, or tables built by the undertaking on
its own experience and **certified by an independent actuary** [REG-R23]. INSEE's national
series is the only freely redistributable French mortality data and is the source behind the
decrement tables this library ships [REG-R24].

**Macroprudential.** Art. L. 631-2-1 CMF lets the HCSF, on a proposal of the Governor of the
Banque de France and to prevent a serious and characterised threat to financial stability,
limit the payment of surrender values and **defer or restrict arbitrages and advances** —
three months at a time, renewable, with the surrender restriction capped at six consecutive
months [REG-R13]. It has no UK or US analogue and it is the reason a French mass-surrender
stress on a multisupport contract is not simply a lapse multiplier.

**Conduct and disclosure.** The `document d'informations clés` (DIC) is the PRIIPs
key-information document: a standardised precontractual document of at most two to three
pages, delivered a reasonable time before subscription, and expressly not a marketing
document [R16]. For a multisupport contract it is written as a multi-option product, so the
summary risk indicator is a **range** — "entre les classes de risque 1 et 7 sur 7" [S5],
"classe de risque 1 à 5 sur 7" [S12] — and so are the cost tables: 50.25 €–1,668.95 € of
total costs after one year and 404.84 €–30,028.49 € after eight on 10,000 € [S5];
73 €–648 € and 724 €–4,553 € [S12]. Both retrieved MOP DICs **omit numeric performance
scenarios** and defer to the per-support documents. The AMF's doctrine DOC-2011-05 is the
retrievable anchor for the PRIIPs chain and cites Regulation (EU) 1286/2014 and Delegated
Regulation (EU) 2017/653 as reference texts [R15] [REG-R33]; **neither regulation could be
fetched** — EUR-Lex returned empty bodies to every endpoint tried — so no PRIIPs article
number, no SRI methodology, no performance-scenario definition and no reduction-in-yield
formula is asserted anywhere in these documents [R17] [R18] [REG-R33] [unverified]. The
`note d'information` and the `encadré` are prescribed by arts. A. 132-4 and A. 132-8
[REG-R30], and the per-support fee transparency table by the arrêté du 24 février 2022, in
force from 1 July 2022 [R9], of which [S6] and [S8] are instances.

**Unclaimed contracts, guarantee scheme and policyholder tax.** The loi Eckert obliges
insurers to consult the RNIPP annually through a professional body and to search for
beneficiaries; a contract is unclaimed where the benefit has not been claimed ten years after
the insurer knew of the death, at which point the proceeds transfer to the Caisse des dépôts
et consignations and become State property twenty years later [R10] [REG-R39] [S11]. The FGAP
covers 70,000 € per person per insurer for capital and 90,000 € for annuities in payment,
under art. L. 423-1 [S5]; PRO BTP's DIC states the 70,000 € capital figure and describes the
ACPR's transfer tender on a failure, and gives no annuity figure [S12]. Policyholder gains are taxed at `dénouement` only, with the
eight-year threshold, the 7.5%/12.8% split and the 4,600 € / 9,200 € annual `abattement`
[S4 Annexe II] [REG-R40]; death benefits fall under CGI arts. 990 I and 757 B according to
whether the premium was paid before or after the insured's 70th birthday [S4 Annexe II]
[S10 ART 19] [REG-R41]. None of it is an insurer cash flow — but the eight-year threshold is
a behavioral fact of the first order, and a model that puts no surrender spike at duration
eight has ignored it [REG-R40].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-assurance_vie_uc-r1
[R10]: #frlib-assurance_vie_uc-r10
[R11]: #frlib-assurance_vie_uc-r11
[R12]: #frlib-assurance_vie_uc-r12
[R13]: #frlib-assurance_vie_uc-r13
[R14]: #frlib-assurance_vie_uc-r14
[R15]: #frlib-assurance_vie_uc-r15
[R16]: #frlib-assurance_vie_uc-r16
[R17]: #frlib-assurance_vie_uc-r17
[R18]: #frlib-assurance_vie_uc-r18
[R2]: #frlib-assurance_vie_uc-r2
[R3]: #frlib-assurance_vie_uc-r3
[R4]: #frlib-assurance_vie_uc-r4
[R5]: #frlib-assurance_vie_uc-r5
[R6]: #frlib-assurance_vie_uc-r6
[R7]: #frlib-assurance_vie_uc-r7
[R8]: #frlib-assurance_vie_uc-r8
[R9]: #frlib-assurance_vie_uc-r9
[REG-R1]: #frlib-reg-r1
[REG-R13]: #frlib-reg-r13
[REG-R19]: #frlib-reg-r19
[REG-R2]: #frlib-reg-r2
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R33]: #frlib-reg-r33
[REG-R39]: #frlib-reg-r39
[REG-R4]: #frlib-reg-r4
[REG-R40]: #frlib-reg-r40
[REG-R41]: #frlib-reg-r41
[REG-R48]: #frlib-reg-r48
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
