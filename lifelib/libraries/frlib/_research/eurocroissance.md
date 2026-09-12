# Hybrid Savings Support with Guarantee at Maturity (eurocroissance) — research notes (France)

Research notes for the French *eurocroissance* support — a life-insurance or capitalisation
engagement that carries a capital guarantee **only at a contractual maturity**, with the saver's
interim value expressed in *parts de provision de diversification* (units of a diversification
provision) whose value floats with the market value of a ring-fenced asset pool. These notes are
the citation ground truth for the frlib eurocroissance product documents: source ids S1..S11 and
R1..R22 below are frozen — never renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document that
was actually fetched and read. `[unverified]` marks statements from general knowledge or from
secondary summaries of documents that could not be retrieved. Where a fetch failed the failure is
recorded and the item is kept only as a known reference (fetched_ok = false).

Scale note, stated up front because it shapes everything below: **eurocroissance is a very small
product with almost no public contractual documentation.** No insurer's *notice d'information*,
*conditions générales* or PRIIPs *document d'information clé* for a eurocroissance support could
be retrieved in this session. What is abundant and fully retrievable is the law: the Code des
assurances fixes the mechanics of this product in far more detail than it fixes the mechanics of
a *fonds en euros*, because the product is a statutory construct rather than a market convention.
The extraction below therefore leans on `[R#]` legal sources for mechanics and on `[S#]` insurer
web material and one published actuarial *mémoire* for parameter levels.

---

## Primary sources

### S1 — AXA France, "Fonds Croissance" (eurocroissance support product page)
- Publisher: AXA France Vie
- Doc type: Insurer product page (retail marketing page for the eurocroissance support)
- URL: https://www.axa.fr/epargne-retraite/assurance-vie/eurocroissance.html
- Retrieved: YES (page fetched and read).
- Content: describes Fonds Croissance as a support sitting between the *fonds en euros* and
  *unités de compte*, invested in bonds (government, corporate, private debt) plus diversified
  assets (equities, real estate, structured products). Two liability components named:
  *provision mathématique* (the guaranteed, euro-expressed part) and *provision de
  diversification* held in *parts*. States expressly that the insurer commits to **the number of
  parts but not to their value**. Guarantee: **100 % of net invested capital**, "totalement
  garanti à l'échéance", with a **10-year minimum maturity** measured from the first investment.
  Before maturity, amounts invested fluctuate up and down and "le risque de perte en capital peut
  être total ou partiel". Death: a *garantie décès plancher* ensures beneficiaries receive at
  least the net invested savings. Published annual net returns for the support: 2018 2.40 %,
  2019 3.00 %, 2020 2.60 %, 2021 3.00 %, 2022 3.30 %, 2023 3.30 %, 2024 and 2025 quoted as
  "2 à 4 %" with the Eurocroissance+ device; average annualised since 2017 **2.98 %** net of
  charges. No explicit charge percentages given on the page.

### S2 — AXA France, "Fonds Croissance" (second product path, retail)
- Publisher: AXA France Vie
- Doc type: Insurer product page
- URL: https://www.axa.fr/particuliers/epargne/assurance-vie/eurocroissance.html
- Retrieved: YES.
- Content: same product, additional detail. Guarantee **100 % du capital net investi at the
  10-year maturity**; capital loss possible before maturity. *Rachat* available at any time
  **without a surrender penalty**, subject to tax and social levies, but exposed to capital loss
  before the 10-year point. Asset mix "obligations et actifs diversifiés". Synthetic risk
  indicator **SRI 2/7**. Eurocroissance+ bonus "up to +2 % supplémentaires" on the annual return
  for money paid in during 2024–2025, transfers excluded. Charges: not stated in percentage
  terms; returns are quoted "nette de frais de gestion du contrat".

### S3 — AXA France, "Assurance-vie : AXA France annonce une hausse de ses rendements pour les supports en euros et eurocroissance" (press release, 15 January 2026)
- Publisher: AXA France
- Doc type: Insurer press release announcing 2025 credited rates
- URL: https://www.axa.fr/particuliers/qui-sommes-nous/espace-presse/epargne-retraite/assurance-vie-rendements-2025.html
- Retrieved: YES (full press release text).
- Content: 2025 rates. Euro supports **2.25 %–4.25 %** net (+0.25 pt vs 2024); Amadéo range
  2.35 %–4.35 %; PER "Ma Retraite" euro 2.50 %. Eurocroissance support **Fonds Croissance
  2.50 %–4.50 %**, **average net rate 3.13 %**, **+0.50 pt vs 2024**; Amadéo 2.60 %–4.60 %;
  PER "Ma Retraite" eurocroissance 3.25 %. Named contracts carrying the support: Arpèges,
  Excelium, Privilège, Odyssiel, Expantiel, Figures Libres, Optial, Amadéo, Ma Retraite.
  2026 bonus device: **+0.50 %** on savings already held before 1 January 2026 and **+2.00 %**
  on new 2026 payments, conditional on **at least 45 %** of savings in *unités de compte*, or on
  piloted/convention-based management. No encours figures disclosed.

### S4 — AXA France, "Dispositifs euro + et eurocroissance + 2026"
- Publisher: AXA France Vie
- Doc type: Insurer product page describing the bonus arrangement and its conditions
- URL: https://www.axa.fr/epargne-retraite/assurance-vie/bonus-euro-2026.html
- Retrieved: YES.
- Content: for 2026 payments, **+2 %** added to the base rate on both the euro support and the
  Fonds Croissance, giving up to **4.50 %** on Fonds Croissance and **4.25 %** on the euro
  support; **+0.5 %** on pre-2026 euro savings (up to 2.75 % total). Qualifying condition:
  piloted or convention management, or free management with **a minimum 45 % in unités de
  compte**. Conditions must hold to **31 December 2026** and, after any subsequent transaction,
  up to the profit-sharing attribution date, **no later than 1 April 2027**. Money-market funds
  excluded; initial payments arising from PACTE transfers excluded. States that guaranteed rates
  cannot exceed the ceiling in **article A. 132-3 du Code des assurances**.

### S5 — Generali France, "Fonds croissance" (newsroom topic index)
- Publisher: Generali France
- Doc type: Insurer press-room index page collecting eurocroissance announcements
- URL: https://presse.generali.fr/fonds-croissance.html
- Retrieved: YES (index page read; only headline figures present).
- Content: G Croissance 2014 was Generali's first eurocroissance fund (2014). A February 2020
  release states G Croissance 2014 showed a **net annualised performance of 5.37 % since
  inception** over its first five years. **G Croissance 2020** launched December 2020 as the
  PACTE-compliant successor. Funds referenced as available inside Himalia Patrimoine and ING
  Direct Vie contracts. No guarantee levels, maturities, charges or provision mechanics on this
  page.

### S6 — Generali France, "Assurance-vie & Retraite : Generali France annonce des rendements 2025 solides" (26 January 2026)
- Publisher: Generali France
- Doc type: Insurer press release announcing 2025 credited rates
- URL: https://www.generali.fr/actu/generali-strategie-diversification-2025-taux-pb/
- Retrieved: YES (press release text read).
- Content: 2025 euro-fund average **2.55 %** for life insurance (2024: 2.53 %) and **3.30 %**
  for PER (2024: 3.40 %), net of management charges. Describes the Fonds Croissance range as
  hybrid solutions offering "un compromis entre rendement et sécurité" with **partial capital
  guarantee at maturity**. The 2025 percentage for G Croissance 2020 / Générations Croissance
  Durable is **not** stated in this release; it points to a separate "Taux de Participation aux
  Bénéfices (PB) 2025" document which was not retrieved.

### S7 — Crédit Agricole Assurances (Predica), "Predica lance Objectif programmé, son premier support croissance / eurocroissance" (16 October 2014)
- Publisher: Crédit Agricole Assurances / Predica
- Doc type: Insurer press release (product launch)
- URL: https://www.ca-assurances.com/publication/predica-lance-objectif-programme-son-premier-support-croissance-eurocroissance/
- Retrieved: YES.
- Content: Predica's first-generation (2014 regime) support. **Duration 8 to 40 years**;
  **guarantee level 80 % to 100 %**, both chosen by the saver. Distributed by the Caisses
  régionales du Crédit Agricole and LCL inside Floriane, Espace Liberté 2, Lionvie Rouge Corinthe
  and Acuity. Minimum investment, charge levels and the pre/post-maturity mechanics are not
  stated in the release.

### S8 — FranceTransactions, "G CROISSANCE 2020 (Generali)" — fund fact page
- Publisher: FranceTransactions.com (third-party comparison site)
- Doc type: Third-party product fact sheet (secondary; used because Generali's own notice could
  not be retrieved — see S10)
- URL: https://www.francetransactions.com/assurance-vie/fonds-euro-croissance/g-croissance-2020-generali-eurocroissance.html
- Retrieved: YES (page published 7 February 2021; performance table updated 27 January 2026).
- Content: G Croissance 2020 — capital guarantee at maturity **80 %**; guarantee term **8 to 30
  years**, chosen by the client. Charges: *frais de gestion* **1.00 %**, *frais sur versements*
  **4.50 % maximum**, *frais de conversion* **0.50 %**. Annual net returns (net of management
  charges, gross of tax and social levies): 2020 0.52 %, 2022 0.05 %, 2023 3.67 %, 2024 3.55 %,
  2025 3.40 %. Available inside Himalia and Espace Invest 5; planned for L'Epargne Generali
  Platinum in 2021. Before maturity, capital loss risk partial or total. Because this is a
  third-party page and not the insurer's contractual document, its figures are treated as
  indicative and are marked as such where used.

### S9 — MoneyVox, "Eurocroissance : principe et fiscalité du contrat d'assurance vie"
- Publisher: MoneyVox (formerly cBanque), consumer finance publisher
- Doc type: Third-party product explainer carrying a cross-insurer rate table (secondary)
- URL: https://www.moneyvox.fr/assurance-vie/euro-croissance.php
- Retrieved: YES (page last updated 26 May 2026 per the fetched page).
- Content: cross-market table of **2025 net returns** on eurocroissance supports (net of
  management charges, before tax and social levies): G Croissance 2020 (Generali) **3.40 %**;
  Générations Croiss@nce durable (Generali) **3.40 %**; Agipi eurocroissance (AXA France)
  **3.00 %**; Fonds Croissance (AXA France) **2.50 %**; Afer eurocroissance (Abeille
  Assurances) **2.16 %**; G Croissance 2014 (Generali) **2.20 %**; Croissance Allocation Long
  Terme (Spirica) **0.90 %**. Also: minimum guarantee duration **8 years** from the first
  payment, with insurers free to set 10, 20, 30 or 40 years; the "eurocroissance" label
  described as reserved for 100 % guarantees with partial guarantees (commonly 80 %) labelled
  "croissance" — this labelling claim is **[unverified]**, see Gaps §3. Reports market size
  **€11.3 bn at March 2025** across **more than 700 000** contracts holding croissance or
  eurocroissance funds. Tax: ordinary assurance-vie regime, with the distinctive feature that
  social levies bite **at the fund's maturity** rather than annually (euro) or at surrender (UC)
  — this is confirmed independently at [R11].

### S10 — Generali France, G Croissance 2014 / G Croissance 2020, notice d'information and document d'information clé
- Publisher: Generali Vie
- Doc type: Notice d'information / conditions générales / PRIIPs DIC
- URL: not located
- Retrieved: NO (no public URL for these documents could be found; Generali's own pages point to
  the *notice d'information valant conditions générales* but do not expose a PDF). Kept as a
  known reference only. Nothing is cited from it; the G Croissance parameters used here come
  from S8 and are flagged as third-party.

### S11 — Profession CGP, "Fonds eurocroissance : l'âge de raison ?"
- Publisher: Profession CGP (adviser trade press)
- Doc type: Market analysis article
- URL: https://www.professioncgp.com/article/paroles-dexperts/analyses-points-de-vue/fonds-eurocroissance-lage-de-raison.html
- Retrieved: NO — HTTP 403 Forbidden on two attempts (host blocks automated fetches). Known
  reference only; no content from it is cited.

---

## Regulatory and actuarial references

### R1 — Code des assurances, Partie législative, Livre Ier Titre III Chapitre IV "Engagements donnant lieu à constitution d'une provision de diversification" (art. L. 134-1 à L. 134-5)
- Publisher: Légifrance (Direction de l'information légale et administrative)
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000029141706/
  and https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611220 (L. 134-1)
- Retrieved: YES (Légifrance section and article pages; the full chapter text was additionally
  read verbatim from the consolidated Code des assurances PDF at
  https://codes.droit.org/PDF/Code%20des%20assurances.pdf, edition 2026-07-19, last modification
  2026-06-27, downloaded with a browser User-Agent).
- Content: **L. 134-1** (in force 24 May 2019, from LOI n° 2019-486 art. 72) authorises life
  insurers to write engagements in case of life or death, **excluding temporary death
  assurance**. Those engagements may include a guaranteed annuity or capital **at maturity** and
  give rise to a *provision de diversification* intended to absorb fluctuations in the
  representing assets. Two modalities: **1°** annuity/capital guaranteed expressed **in euros and
  in parts of the diversification provision**; **2°** annuity/capital guaranteed expressed
  **only in parts before maturity**, with a **guarantee at maturity expressed in euros**.
  Engagements written under 1° may, by agreement, be transformed into 2°; where the transformation
  is not a new contract, the insurer or intermediary must inform the policyholder of the changes,
  and article 3 of ordonnance n° 2014-696 does not apply to that transformation. A single life
  policy's premiums may simultaneously create euro engagements, unit-linked engagements and
  diversification-provision engagements. Capitalisation contracts may be written on the same
  terms.
  **L. 134-2**: the insurer keeps one or more *comptabilités auxiliaires d'affectation*
  (ring-fenced auxiliary accounts) for these engagements, by derogation from the Code de
  commerce; 1° and 2° engagements may be grouped in the same auxiliary account.
  **L. 134-3**: where representation of **1°** engagements is insufficient the insurer completes
  it by contributing assets backing its own reserves/provisions (other than those representing
  its regulated commitments), and may re-allocate assets out when representation permits. For
  **2°** engagements, where the assets are insufficient to secure the maturity guarantee the
  insurer constitutes a **provision pour garantie à terme** and backs it with an equivalent asset
  contribution, releasable when representation permits.
  **L. 134-4** (in force 1 January 2022, ordonnance n° 2021-1192 art. 34): no creditor of the
  insurer other than the policyholders/beneficiaries of these operations may claim on the assets
  and rights in the auxiliary accounts.
  **L. 134-5** (created by ordonnance n° 2014-696 du 26 juin 2014 art. 1): a *décret en Conseil
  d'État* sets application conditions.

### R2 — Code des assurances, Partie réglementaire, art. R. 134-1 à R. 134-12
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000029426878/
  and https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739654 (R. 134-1),
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739643 (R. 134-4)
- Retrieved: YES (Légifrance pages; full chapter text also read verbatim from the consolidated
  Code des assurances PDF, edition 2026-07-19).
- Content (all articles from décret n° 2019-1437 du 23 décembre 2019 art. 1, in force 1 January
  2020, except R. 134-12 which is from décret n° 2025-1333, in force 27 December 2025):
  **R. 134-1** — the guaranteed capital (or the capital constitutive of the guaranteed annuity)
  payable at maturity may not exceed an amount determined from mortality tables and pricing rates
  fixed by *arrêté*. The contract must fix a **minimum value of the part de provision de
  diversification**, strictly positive and expressed in euros. An *arrêté* is to determine a
  **denomination** and minimum conditions "notamment en matière d'échéance et de niveau de
  garantie en capital" that contracts must meet to use that denomination in documents intended
  for third parties. Transitional: contracts in force at entry into force stay under the previous
  articles, and new contracts could be written under the old regime until **1 October 2020**.
  **R. 134-2** — premiums and incoming transfers/arbitrages, **net of the charges permitted by
  R. 134-3 1°**, create individual rights expressed in **number of parts** of the diversification
  provision and, for **1°** engagements, in *provision mathématique*. The number of parts equals
  the diversification provision divided by the **part value, which is common to all
  engagements**. For 1° engagements the *provision mathématique* equals **the maturity guarantee
  discounted at a rate fixed by arrêté** (see R3, A. 134-1).
  **R. 134-3** — the contract states the insurer's deductions. Deductions may be taken **only**
  on: 1° premiums and incoming transfers/arbitrages; 2° amounts arising from the R. 134-4
  conversion; 3° **the diversification provision, only where the auxiliary account contains no
  1° engagements**; 4° **the number of parts**; 5° the balance of the participation account
  **or alternatively** the performance of the financial management of the auxiliary account's
  assets; 6° benefits paid and outgoing transfers/arbitrages.
  **R. 134-4** — a *compte de participation aux résultats* is established. A **credit balance**
  is allocated to (1) the *provision mathématique* by revaluing the guarantees, on conditions set
  by arrêté; (2) the *provision de diversification*, by awarding **new parts** or by **increasing
  the part value**; (3) the *provision collective de diversification différée*. A **debit
  balance** is offset by a *reprise* of the deferred collective provision or by **reducing the
  part value, within the limit of its minimum value**. Asset affectations/re-affectations
  completing the representation of the auxiliary account are made **on the dates the
  participation account is struck, after its balance has been allocated**. The deferred
  collective provision may be released at any time to revalue the mathematical or diversification
  provision. For 1° engagements the contract may provide for **conversion of parts into
  provision mathématique** on conditions set by arrêté.
  **R. 134-5** — the period referred to in the tenth *alinéa* of L. 132-23 (the period during
  which the engagements may be made non-surrenderable) **may not exceed the lesser of the
  guarantee maturity and eight years**. Before maturity, the *valeur de rachat ou de transfert*
  of **1°** engagements = the holder's *provision mathématique* + (his number of parts × part
  value), less any indemnity under R. 132-5-3. For **2°** engagements it = (number of parts ×
  part value), less any R. 132-5-3 indemnity.
  **R. 134-6** — at the guarantee maturity, amounts due on **1°** engagements = the R. 134-5
  second-*alinéa* value; on **2°** engagements = **the greater of the R. 134-5 third-*alinéa*
  value and the guarantee**. Unless the holder decides otherwise expressly, that amount is
  settled as a benefit or **arbitraged into a support whose characteristics are fixed by arrêté**
  (see R3, A. 134-6). **Three months before maturity** the holder must be informed on paper or
  another durable medium of the destination of the amount and how to change it. If the contract
  offers an annuity, the annuity is computed on a *capital constitutif* equal to that amount,
  expressed in euros; on conversion the rights move to an ordinary R. 343-3 1° mathematical
  provision and leave the auxiliary account.
  **R. 134-7** — complementary guarantees are allowed; their mathematical provision is **not**
  held inside the auxiliary account.
  **R. 134-8** — assets in the auxiliary account are carried at **realisation value** (market
  value) under R. 343-11/R. 343-12, by derogation from R. 343-9/R. 343-10.
  **R. 134-9** — the technical provisions of these operations are those at R. 343-3 **1°, 4°,
  7°, 9°, 10° and 11°**.
  **R. 134-10** — pre-sale disclosure, in "caractères très apparents": the guarantee maturity;
  the euro amount of the guaranteed capital or annuity at maturity; where applicable a statement
  that **there is no guarantee before maturity**; where applicable the period during which the
  engagements are not surrenderable; the maturity settlement arrangements. Also to be given: the
  **minimum value of the part in euros**; the individualised premium for any complementary
  guarantee; and the settlement/transfer/arbitrage delays and the delay for crediting rights
  after a premium.
  **R. 134-11** — the chapter applies **separately to each auxiliary account**.
  **R. 134-12** — see R7.

### R3 — Code des assurances, Partie réglementaire (Arrêtés), art. A. 134-1 à A. 134-7
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801782 (A. 134-1),
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801776 (A. 134-2),
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801769 (A. 134-3),
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046824887 (A. 134-6)
- Retrieved: YES (four Légifrance article pages; A. 134-4, A. 134-5 and A. 134-7 read verbatim
  from the consolidated Code des assurances PDF, edition 2026-07-19).
- Content (A. 134-1 to A. 134-5 and A. 134-7 from the **arrêté du 26 décembre 2019 art. 1**, in
  force 1 January 2020; A. 134-6 from the **arrêté du 22 décembre 2022**, in force 1 January
  2023):
  **A. 134-1** — for R. 134-2, and by derogation from art. 142-3 of ANC regulation n° 2015-11,
  the *provision mathématique* may be computed at a rate **above the pricing rate**, capped by
  one of two methods: **1°** per engagement, **90 % of the last TECn index published by the
  Banque de France**, n = the holder's guarantee maturity, with **linear interpolation** between
  the two bracketing TEC maturities where no exact TECn exists; **2°** 90 % of the last TECn
  where n = the **duration** of all 1° engagements of the auxiliary account, same interpolation
  rule. For a maturity or duration beyond the longest available TEC, the rate may not exceed the
  longest-maturity TEC. The choice of method binds **all** engagements of one auxiliary account
  and is **irreversible**. The rate **may not be negative**; if the ceiling is negative the
  insurer uses **0 %**.
  **A. 134-2** — the **provision pour garantie à terme** (R. 343-3 11°) is constituted **per
  auxiliary account** and equals the positive difference between the **present value of the 2°
  guarantees** and the sum of the corresponding **provision de diversification** and the
  **provision collective de diversification différée**. That present value uses the **mortality
  tables of A. 132-18** and rates **at most equal to those of A. 134-1 2°**, with the duration
  computed on 2° engagements only, and **counts no cash flows other than guarantee maturities and
  mortality**.
  **A. 134-3** — revaluation of the guarantees under R. 134-4 second *alinéa* is permitted only
  if both hold: **1°** the diversification provision attaching to 1° guarantees exceeds **1.5 ×**
  the difference between the mathematical provisions computed at a **zero** discount rate and the
  actual mathematical provisions; **2°** the excess of that diversification provision over its
  **minimum amount** (computed from the R. 134-1 minimum part value) exceeds **10 % of the
  mathematical provisions**.
  **A. 134-4** — the R. 134-4 conversion of parts into *provision mathématique* may occur **only
  once every five years**, and only if after conversion the excess of the diversification
  provision over its minimum amount exceeds **15 % of the mathematical provision** of that
  engagement.
  **A. 134-5** — an **intermediate amount of the diversification provision must be computed at
  least monthly** in every month in which the participation account is not struck; it equals the
  realisation value of the assets (R. 343-11/R. 343-12) minus the provisions of R. 343-3 1°, 4°,
  7°, 10° and 11°. For R. 134-2 second *alinéa* and R. 134-5, the part value to use is the value
  determined at the next striking of the participation account, or, if an intermediate amount is
  computed first, that intermediate amount divided by the number of parts at its computation date.
  **A. 134-6** — the supports into which maturity proceeds may be arbitraged under R. 134-6
  second *alinéa* are those whose **synthetic risk indicator (PRIIPs Delegated Regulation (EU)
  2017/653 art. 3) is ≤ 2**; where no SRI exists, an analogous indicator is computed.
  **A. 134-7** — annual ACPR reporting **by 30 April**, separately for 1° and 2° engagements,
  **by maturity year and by guarantee level**: number of contracts/adhesions in force; amount of
  mathematical provisions; amount of the diversification provision; premiums paid and incoming
  transfers/arbitrages; balance-sheet value of the auxiliary-account assets by R. 332-2
  nomenclature. **The guarantee level is reported on a scale of the proportion of premiums
  guaranteed, with origin 0 and a step of 5 percentage points.** ACPR aggregates and transmits to
  the minister, with the list of undertakings concerned.

### R4 — LOI n° 2019-486 du 22 mai 2019 relative à la croissance et la transformation des entreprises (loi PACTE), article 72
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000038496267
- Retrieved: YES.
- Content: rewrites L. 134-1 to create the **two modalities** (1° euros + parts; 2° parts only
  before maturity with a euro guarantee at maturity), i.e. the "eurocroissance 2.0" structure
  with **no euro guarantee during the accumulation phase**. Permits transformation of existing
  1° engagements into 2° by agreement of the parties without the tax consequences of a
  *dénouement* and disapplying article 3 of ordonnance n° 2014-696. The same article 72 carries
  the unrelated ESG obligations on life contracts (at least one qualifying unit of account from
  **1 January 2020**; a **5 %–10 %** allocation to solidarity or venture-capital vehicles from
  **1 January 2022**). Provisions apply to contracts concluded or subscriptions made from
  1 January 2020.

### R5 — Décret n° 2019-1437 du 23 décembre 2019 relatif aux contrats d'assurance ou de capitalisation comportant des engagements donnant lieu à constitution d'une provision de diversification
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000039667326
- Retrieved: YES (JORF text page read).
- Content: the implementing decree for PACTE art. 72. Rewrites the whole of Chapter IV of the
  regulatory part (R. 134-1 to R. 134-11 as summarised at R2), amends R. 343-3 (art. 2) to add
  the **provision de diversification** (9°), **provision collective de diversification différée**
  (10°) and **provision pour garantie à terme** (11°), and (per the actuarial *mémoire* at R13,
  citing its art. 6) makes the *transfert de richesse* mechanism permanent. In force
  **1 January 2020**.

### R6 — Arrêté du 12 septembre 2014 relatif aux engagements donnant lieu à la constitution d'une provision de diversification
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000029446963
- Retrieved: YES (JORF text page read).
- Content: the **first-generation (2014 regime)** arrêté; created A. 134-1 to A. 134-7 in their
  original form. Parameters read from the fetched text: discount rate for the mathematical
  provision capped at **90 % of the last TEC index** for the guarantee maturity or the liability
  duration, with the longest TEC used beyond the available range (A. 134-1, the rule PACTE
  retained); tracking error of a reference-index-linked support capped at **1 % or 5 % of the
  reference index volatility** (A. 134-5, old numbering); conversion permitted only **once every
  five years** and the residual diversification provision after conversion must be **≥ 15 % of
  the mathematical provision** (A. 134-6, old numbering); and — in the old A. 331-4 — the
  deferred diversification reserve capped at **8 %** of the greater of the zero-rate mathematical
  provisions and the auxiliary-account asset value, with a **maximum 8-year** holding period.
  Those two 2014 constraints (the 8 % cap and the 8-year clock) are the ones PACTE removed and
  lengthened respectively — see R9.

### R7 — Décret n° 2025-1333 du 26 décembre 2025 relatif aux apports d'actifs destinés à garantir les contrats d'assurance comportant des engagements donnant lieu à constitution d'une provision de diversification
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053174741
- Retrieved: YES (JORF text page read; the resulting R. 134-12 text also read verbatim in the
  consolidated code PDF).
- Content: reinstates **R. 134-12**, the insurer's asset-contribution ("*apport d'actifs*",
  known in the trade as the *transfert de richesse*) mechanism. **I** — an insurer that meets the
  representation of its regulated commitments and its solvency-margin / SCR coverage may
  contribute to the auxiliary account cash held in a qualifying R. 332-16 account, or any asset
  listed at R. 342-4, **up to 10 % of the diversification provision recorded at the affectation
  date**. Contributed assets enter the auxiliary account at **realisation value** (R. 343-11/12);
  any difference from the prior book value goes through the insurer's income statement. The
  contribution **gives rise to a matching dotation to the provision collective de diversification
  différée**. **II** — when the level of its engagements permits, the insurer may re-allocate
  assets back out, capped at the **lowest of three amounts**: (1) the realisation value of the
  assets at their affectation date plus their share of net investment income while in the account
  plus the R. 134-3 5° levies on financial-management performance over the same period; (2)
  **10 % of the total diversification provision**; (3) the total **provision collective de
  diversification différée**. Re-allocation must happen **no later than during the sixteenth year
  following the year of affectation**, and triggers a matching *reprise* of the deferred
  collective provision. **III** — affectations and re-affectations happen on the dates the
  R. 134-4 participation account is struck, after its balance has been allocated. Art. 2 updates
  the R. 343-1 cross-reference from R. 134-14 to R. 134-12. In force the day after publication,
  i.e. **27 December 2025**.

### R8 — Code des assurances, art. R. 343-3 (catalogue of life technical provisions)
- Publisher: Légifrance, via the consolidated Code des assurances PDF
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739686 ;
  https://codes.droit.org/PDF/Code%20des%20assurances.pdf
- Retrieved: YES (text read verbatim from the consolidated PDF; version from décret n° 2019-1437
  art. 2).
- Content: the definitions the eurocroissance balance sheet uses. **9° Provision de
  diversification** — for L. 134-1 engagements, a provision "destinée à absorber les fluctuations
  des actifs affectés à ces engagements et sur laquelle les souscripteurs ou adhérents détiennent
  des droits individualisés sous forme de parts". **10° Provision collective de diversification
  différée** — for L. 134-1 engagements, "destinée au lissage de la valeur de rachat des
  contrats". **11° Provision pour garantie à terme** — for **2°** engagements only, "destinée à
  faire face à une insuffisance d'actifs au regard des garanties à échéance contractées".
  An engagement may be provisioned under only one category. Also present in the same article:
  1° provision mathématique, 4° provision de gestion, 7° provision pour frais d'acquisition
  reportés — the other three provisions R. 134-9 admits into the auxiliary balance sheet.

### R9 — Code des assurances, art. A. 132-16 (holding period for profit-sharing reserves)
- Publisher: Légifrance, via the consolidated Code des assurances PDF
- URL: https://codes.droit.org/PDF/Code%20des%20assurances.pdf
- Retrieved: YES (text read verbatim; version from the arrêté du 26 décembre 2019 art. 2).
- Content: amounts carried to the ordinary *provision pour participation aux bénéfices* must be
  applied to mathematical provisions or paid to policyholders **within the eight financial years**
  following the one for which they were provided. **"Pour les engagements relevant de l'article
  L. 134-1, les sommes portées à la provision collective de diversification différée sont
  utilisées dans les conditions fixées à l'article R. 134-4 et dans un délai de quinze ans."**
  That is the statutory basis for the **15-year** PCDD clock (against 8 years for a euro fund's
  PPB), and it is the single largest smoothing advantage eurocroissance has over the euro fund.

### R10 — Code des assurances, art. A. 132-18 (tariff bases) and art. R. 132-5-3 (surrender-penalty cap)
- Publisher: Légifrance, via the consolidated Code des assurances PDF
- URL: https://codes.droit.org/PDF/Code%20des%20assurances.pdf
- Retrieved: YES (both texts read verbatim; A. 132-18 from the arrêté du 14 août 2017,
  R. 132-5-3 from décret n° 2024-539 du 12 juin 2024 art. 2).
- Content: **A. 132-18** — life tariffs are built on a technical interest rate set under A. 132-1
  and on one of: (a) tables homologated by ministerial arrêté, built by sex, on insured-population
  data for life annuities and on **INSEE** data for other contracts; or (b) tables built by the
  insurer (with or without sex distinction) and **certified by an independent actuary approved by
  a recognised actuarial association**. Where a single table is used for all insureds it must be
  the appropriate table producing the most prudent tariff; for non-annuity "en cas de vie"
  contracts the (a) tables are used with the annexed **age shifts** (*décalages d'âge*). This is
  the article A. 134-2 points to for valuing the *provision pour garantie à terme*.
  **R. 132-5-3** — the surrender/transfer indemnity may not exceed **5 %** of the present value
  of the mutual engagements (raised to 20 % or 10 % in narrow unlisted-asset cases), and **the
  contract may provide for no indemnity at all once it has been in force for more than ten
  years**. This is the *indemnité* R. 134-5 deducts from the eurocroissance surrender value.

### R11 — Code de la sécurité sociale, art. L. 136-7 (social levy on investment income)
- Publisher: Légifrance, via the consolidated Code de la sécurité sociale PDF
- URL: https://codes.droit.org/PDF/Code%20de%20la%20s%C3%A9curit%C3%A9%20sociale.pdf
- Retrieved: YES (text read verbatim; version from LOI n° 2026-103 du 19 février 2026 art. 24).
- Content: II 3° sets when the social contribution bites on capitalisation bonds and
  assurance-vie. **a)** on inscription to the contract for euro/currency-denominated rights,
  including the euro-denominated share of a multi-support contract "dont une part peut être
  affectée à l'acquisition de droits exprimés en unités de compte … ou de droits donnant lieu à
  la constitution d'une provision de diversification". **b)** — the eurocroissance-specific rule
  — **"A l'atteinte de la garantie pour les engagements donnant lieu à la constitution d'une
  provision de diversification et pour lesquels un capital ou une rente est garantie à une
  échéance fixée au contrat."** The base is then **the surrender value of those engagements at
  the moment the guarantee is reached, less the premiums allocated to them net of premiums
  already included in partial surrenders**. **c)** on *dénouement* of the contract or on the
  insured's death, computed net of amounts that already bore the contribution under a) and b).

### R12 — Code général des impôts, art. 125-0 A and art. 990 I
- Publisher: Légifrance, via the consolidated Code général des impôts PDF
- URL: https://codes.droit.org/PDF/Code%20g%C3%A9n%C3%A9ral%20des%20imp%C3%B4ts.pdf
- Retrieved: YES (both texts read verbatim; 125-0 A version from LOI n° 2021-1900 art. 35,
  990 I from LOI n° 2023-171 art. 3).
- Content: **125-0 A I 1°** — gains on capitalisation bonds and like placements are taxed on
  *dénouement* or partial surrender whatever the subscription date; exempt where the contract is
  wound up by a life annuity or on redundancy, early retirement, or 2nd/3rd-category invalidity of
  the holder or spouse; gain = sums repaid minus premiums paid. An exemption applies, within
  **€4 600** (single) / **€9 200** (jointly taxed couple) per year, where a contract meeting the
  duration condition is surrendered and the whole proceeds are paid into a **PER** before
  31 December of the surrender year. **125-0 A I 2°** — "**la transformation partielle ou totale
  d'un bon ou contrat … permettant qu'une part ou l'intégralité des primes versées soient
  affectées à l'acquisition de droits exprimés en unités de compte … ou de droits donnant lieu à
  la constitution d'une provision de diversification n'entraîne pas les conséquences fiscales
  d'un dénouement**", by endorsement or by a new contract with the same insurer. This is the
  provision that lets a euro contract be converted into eurocroissance while keeping its fiscal
  seniority. **990 I** — the death levy outside art. 757 B: after a **20 %** proportional
  abatement for qualifying contracts and a **€152 500** fixed abatement per beneficiary,
  **20 %** on the taxable share up to **€700 000** and **31.25 %** above.

### R13 — Peltier, M. and Odier, C., "Eurocroissance : quels sont les impacts attendus de la loi PACTE ?" (mémoire, Certificat d'Expertise Actuarielle, Institut du Risk Management / Institut des actuaires; supervisor R. Ennajar-Sayadi; authors from AXA and Allianz)
- Publisher: Institut des actuaires (mémoires library)
- URL: https://www.institutdesactuaires.com/docs/mem/8e47df87101af694559589fb43a46a29.pdf
- Retrieved: YES (86-page PDF downloaded and full text extracted). Undated on its cover; internal
  references (COVID, 2020 launches, an AXA internal-model calibration "à fin 2016") place it
  in **2020–2021** — the date is **[unverified]**.
- Content: the single most useful actuarial description of the product available publicly. It
  sets out the old (2014) and new (PACTE) mechanics side by side with explicit formulas, models
  both stochastically over 1 000 scenarios, and states its own parameterisation. Everything used
  from it is reproduced in the Extracted specifications below (§§4–9, 12–14, 19). Its headline
  conclusions: removing the continuous guarantee removes the *provision mathématique* and
  therefore gives **one common return for all savers**; the insurer's solvency indicator improves
  by roughly **20–26 points**, worth about **13 %–20 %** more equity exposure at unchanged
  solvency; savers' expected return is roughly unchanged but the tails widen (about **+26 to
  +30 bps** in the best scenarios, **−36 bps** in the worst); and pooling two maturity cohorts in
  one fund produces **no mutualisation benefit** — it shifts the short-maturity cohort onto a
  longer, riskier asset allocation.

### R14 — France Assureurs, "En 2024, l'assurance vie a confirmé son attractivité" (communiqué de presse, 31 January 2025)
- Publisher: France Assureurs (the French insurance trade body)
- URL: https://www.franceassureurs.fr/espace-presse/les-communiques-de-presse/assurance-vie-attractivite-2024/
- Retrieved: YES.
- Content: the only retrieved document that sizes eurocroissance directly. **At end-December
  2024, eurocroissance encours = €11.1 bn, +24 % year on year, across 673 000 contracts in force,
  +26 %.** Whole market for comparison: encours **€1 989 bn** (+4.2 %); 2024 premiums **€173.3 bn**
  (+14 %); benefits **€143.8 bn** (−5 %); net inflows **+€29.4 bn**; unit-linked **38 %** of
  full-year premiums (44 % in December); UC net inflows **+€34.4 bn**; euro net inflows
  **−€5.0 bn**. Eurocroissance is therefore about **0.56 %** of the French life market by encours.

### R15 — France Assureurs, "L'assurance vie en 2024" (chiffres clés page, published 23 September 2025)
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/lassurance-vie-en-2024/
- Retrieved: YES.
- Content: market aggregates on the euro/UC split only — **no eurocroissance line**. Total
  premiums **€174.9 bn** (+14.7 %); total encours **€1 985.8 bn** (+3.9 %); *provisions
  mathématiques* **€1 932.2 bn** (+4.4 %); *provision pour participation aux bénéfices*
  **€53.6 bn** (−11.1 %); net inflows **+€28.5 bn**; UC premiums **€66.3 bn** (+8.1 %), UC
  encours **€587.1 bn** (+10.3 %), UC net inflows **+€33.2 bn**, UC **30 %** of provisions; euro
  premiums **€108.6 bn** (+19.2 %) with euro net inflows **−€4.7 bn**. Useful as the denominator
  and as evidence that eurocroissance is not broken out in the standard statistical presentation.

### R16 — France Assureurs, "L'assurance vie en 2025 : une collecte solide au service de l'économie française" (communiqué de presse, 27 January 2026)
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/espace-presse/lassurance-vie-en-2025-une-collecte-solide-au-service-de-leconomie-francaise/
- Retrieved: YES.
- Content: 2025 premiums **€192.1 bn** (+10 %); benefits **€141.4 bn** (−3 %); net inflows
  **+€50.6 bn**, the first year above €50 bn since 2010; end-2025 encours **€2 107 bn** (+6.1 %,
  +€122 bn). UC **39 %** of premiums (+13 %), euro 61 % (+8 %); UC net inflows **+€42.5 bn**,
  euro net inflows **+€8.1 bn** (positive after five years of outflows). PER assurantiel: 2025
  contributions **€20.2 bn** (+16 %), ~1 million new contracts, 7.9 million holders, encours
  **€111.9 bn**. **This release carries no eurocroissance figure** — the 2024 release [R14] does,
  the 2025 one does not.

### R17 — ACPR, "Analyses et synthèses n° 170 — Le marché de l'assurance-vie en 2024" (27 March 2025)
- Publisher: Autorité de contrôle prudentiel et de résolution / Banque de France
- URL: https://acpr.banque-france.fr/system/files/2025-03/20250327_AS170_assurance_vie_2024.pdf
- Retrieved: YES — but **only via `curl` with a browser User-Agent**; plain WebFetch returns HTTP
  403 on this host. 14-page PDF, full text extracted.
- Content: 2024 net inflows on surrenderable supports **+€22.8 bn** (after −€2.3 bn in 2023), the
  highest since the series began in 2011; premiums +€14.9 bn (+10.2 %); benefits −€10.1 bn
  (−8.5 %), of which surrenders −€8.4 bn (−11.1 %) and death claims −€2.7 bn (−4.0 %). Gross
  inflow growth came from euro supports (+€15.1 bn, +17.3 %) while UC stabilised (−€0.2 bn); the
  UC share of premiums fell 5 points to **38 %**. **Contains no eurocroissance figures.**

### R18 — ACPR, "Analyses et synthèses n° 146 — Le marché de l'assurance-vie en 2022" (20 March 2023)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/system/files/import/acpr/medias/documents/20230320_as146_av_2022_vf.pdf
- Retrieved: YES (via `curl` with a browser User-Agent; 13-page PDF, full text extracted).
- Content: cited here for one methodological fact that matters to anyone trying to size this
  product from ACPR data. The study rests on ACPR's weekly life-flows collection from about 70
  undertakings and "**se concentre sur l'analyse des supports rachetables (excluant l'épargne
  retraite et les produits eurocroissance)**". **Eurocroissance is explicitly excluded from
  ACPR's weekly life-insurance flow statistics**, which is why market sizing has to come from
  France Assureurs [R14] or from the A. 134-7 annual return [R3], which is not published.

### R19 — ACPR, "Analyses et synthèses n° 175 — Revalorisation 2024 des contrats d'assurance-vie et de capitalisation" (4 August 2025)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/system/files/2025-08/20250804_AS175_Revalorisation_contrats_assurance_vie_2024.pdf
- Retrieved: YES (via `curl` with a browser User-Agent; 19-page PDF, full text extracted).
- Content: the annual revaluation study, covering **122 undertakings and 32 253 contract
  versions**; unit-linked contracts are excluded from the revaluation analysis. Macro backdrop
  for 2024: French growth 1.0 % (0.9 % in 2023), inflation 2.0 % (4.9 % in 2023), 10-year OAT
  averaging **3.0 %** in both 2024 and 2023, which the ACPR notes eases the burden of guaranteed
  technical rates on euro supports. Retirement (épargne retraite) encours €147 bn at end-2024
  (+2.1 %). **Searching the full extracted text finds no eurocroissance or
  provision-de-diversification section**: this study does not break the product out either.

### R20 — ACPR, "Analyses et synthèses — L'assurance-vie en 2025" (n° 179, 26 March 2026)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/system/files/2026-03/20260326_AS_Assurance_vie_2025.pdf
- Retrieved: NO — HTTP 403 on WebFetch (twice) **and** on `curl` with a browser User-Agent, which
  succeeded on the three other ACPR PDFs above. Known reference only; nothing is cited from it.

### R21 — Sia Partners, "Eurocroissance : un nouvel élan" (17 November 2023)
- Publisher: Sia Partners (consultancy)
- Doc type: Practitioner analysis
- URL: https://www.sia-partners.com/fr/publications/publications-de-nos-experts/eurocroissance-un-nouvel-elan
- Retrieved: YES.
- Content: describes the post-PACTE structure — the whole premium invested in parts of the
  diversification provision; the PCDD smoothing over **15 years** (against 8 under the original
  version); the PGT constituted when PD + PCDD fall short of the discounted guarantee; a part
  value common to all savers with a contractual floor. Market sizing: eurocroissance encours
  **€7.1 bn at end-2022** and **€7.6 bn at mid-2023, +41 %**, across **more than 470 000**
  contracts, against total life encours of €1 907 bn at end-August 2023. Observes that "seule une
  poignée d'assureurs proposent le nouvel Eurocroissance". States a minimum duration of 8 years
  and a guarantee defined contractually as a percentage of contributions — the 8-year minimum is
  a market convention rather than a rule of the current code, see Gaps §3.

### R22 — Ordonnance n° 2014-696 du 26 juin 2014 favorisant la contribution de l'assurance vie au financement de l'économie
- Publisher: Légifrance
- URL: not resolved (a guessed Légifrance identifier returned an empty page; the search budget was
  exhausted before a verified URL could be obtained)
- Retrieved: NO. Known reference only. What is verified about it comes from the texts that cite
  it: it **created** Chapter IV (its art. 1 created L. 134-5 and, by the same article, the rest of
  the chapter) [R1], and its **article 3** governs the transformation of existing contracts into
  diversification-provision engagements — L. 134-1 expressly disapplies that article 3 to the
  1°→2° transformation introduced by PACTE [R1][R4]. The content of article 3 itself is
  **[unverified]**.

---

## Extracted specifications

### 1. Legal form, and the two statutory modalities
- Eurocroissance is not a contract; it is a **support inside an ordinary assurance-vie or
  capitalisation contract**, defined by the type of engagement the insurer takes on. A single
  policy's premiums may simultaneously create euro engagements, unit-linked engagements and
  diversification-provision engagements [R1 L. 134-1].
- The insurer may write engagements **in case of life or death, except temporary death
  assurance**; they may carry a guaranteed annuity or capital **at maturity** and always give
  rise to a *provision de diversification* absorbing asset fluctuations [R1 L. 134-1].
- **Modality 1° ("old" eurocroissance / eurodiversifié shape)** — the guaranteed annuity or
  capital is expressed **in euros and in parts of the diversification provision**. There is a
  *provision mathématique*, and hence a floor on the surrender value at every instant
  [R1 L. 134-1][R2 R. 134-2, R. 134-5].
- **Modality 2° ("new" / PACTE eurocroissance)** — the guaranteed annuity or capital is expressed
  **only in parts before maturity**, with a **euro guarantee at maturity**. There is **no
  provision mathématique and no guarantee before maturity**; the surrender value is purely the
  part value times the number of parts [R1 L. 134-1][R2 R. 134-2, R. 134-5][R13].
- Engagements written under 1° can be **transformed into 2° by agreement**, with notification of
  the changes and without the tax consequences of a *dénouement*; article 3 of ordonnance
  n° 2014-696 does not apply [R1 L. 134-1][R4].
- Both modalities may be **grouped inside the same auxiliary account** (*comptabilité auxiliaire
  d'affectation*) [R1 L. 134-2]. The chapter's rules then apply **separately to each auxiliary
  account** [R2 R. 134-11].
- Capitalisation contracts may be written on the same terms [R1 L. 134-1].
- Policyholders of the auxiliary account have **priority over all other creditors of the insurer**
  on the assets and rights recorded in it, including in insolvency [R1 L. 134-4].

### 2. Chronology, and what the PACTE reform actually changed
- **2004–2006**: the *fonds eurodiversifié*, the first attempt at this structure [R13 —
  contextual, no primary text retrieved, **[unverified]**].
- **26 June 2014**: ordonnance n° 2014-696 creates Chapter IV and with it eurocroissance
  [R1 L. 134-5][R22 — not retrieved].
- **12 September 2014**: the arrêté fixing the first A. 134 series [R6].
- **2016 and 2018 décrets**: enable and then extend the *transfert de richesse* [R13 —
  **[unverified]**, the two décrets were not retrieved]. Per R13 the 2018 extension ran to 2021
  before PACTE made it permanent.
- **22 May 2019**: loi PACTE art. 72 rewrites L. 134-1, creating the 2° modality [R4].
- **23 December 2019** décret n° 2019-1437 and **26 December 2019** arrêté rewrite the R. 134 and
  A. 134 chapters; in force **1 January 2020**, with old-regime contracts still writable until
  **1 October 2020** [R5][R2 R. 134-1 transitional][R3].
- **22 December 2022** arrêté rewrites A. 134-6 (the SRI ≤ 2 rule), in force 1 January 2023 [R3].
- **26 December 2025** décret n° 2025-1333 reinstates R. 134-12 (asset contributions), in force
  **27 December 2025** [R7].
- What changed at PACTE, in the words of the actuarial *mémoire* [R13]:
  1. **The continuous (any-instant) guarantee disappears**, and with it the *provision
     mathématique*. This is the structural change; it produces **a single return common to all
     savers** rather than a return differentiated by entry date, maturity and guarantee level.
  2. **Asset-eligibility restrictions lifted.** The old R. 134-13 and R. 134-14, which imposed
     euro-fund-like constraints on the assets backing the guaranteed part, were deleted
     [R13 citing décret n° 2014-1008 du 4 septembre 2014 — **[unverified]**, that décret was not
     retrieved; the deletion is confirmed indirectly because R. 134-13/R. 134-14 do not exist in
     the current chapter [R2]].
  3. **The *transfert de richesse* is made permanent**, giving insurers visibility on
     competitiveness against the euro fund [R13; the current statutory form is R. 134-12 [R7]].
  4. **The 8-year minimum commitment duration is removed** as a regulatory requirement
     [R13]; what survives in the code is a **cap** of 8 years on any contractual non-surrender
     period [R2 R. 134-5], not a floor on the maturity.
  5. **Charge restrictions relaxed**, notably the ability to levy **in number of parts**
     [R13][R2 R. 134-3 4°]. But see §9 for a discrepancy on whether the participation-account
     levy and the asset-performance levy can now be taken simultaneously.
  6. The **PCDD's 8 % volume cap is removed** and its holding period extended from 8 to
     **15 years** [R13][R9].

### 3. The balance sheet of a eurocroissance auxiliary account
Assets, and only the following technical provisions, sit inside the ring-fenced account
[R2 R. 134-8, R. 134-9][R8]:

| Item | Code reference | Role |
|---|---|---|
| Assets, at **realisation (market) value** | R. 134-8, R. 343-11/12 | derogates from the amortised-cost treatment used for a euro fund |
| **Provision mathématique (PM)** | R. 343-3 1° | only for **1°** engagements; the discounted maturity guarantee |
| **Provision de diversification (PD)** | R. 343-3 9° | the savers' individualised rights, held in *parts* |
| **Provision collective de diversification différée (PCDD)** | R. 343-3 10° | smoothing reserve for the surrender value; collective, no individual rights |
| **Provision pour garantie à terme (PGT)** | R. 343-3 11° | only for **2°** engagements; shortfall of assets against the maturity guarantees |
| Provision de gestion (4°), provision pour frais d'acquisition reportés (7°) | R. 343-3 | admitted by R. 134-9 |

- Because assets are held at market value, the *provision pour risque d'exigibilité*, the
  *provision pour dépréciation durable* and the *réserve de capitalisation* have no purpose
  inside the account, and the technical/financial result becomes **volatile by construction** —
  it is the asset value that determines the liability value, the exact inverse of a euro fund
  [R13].
- The PGT is **outside the participation account** — it does not enter the profit-sharing
  computation, and it is funded from the insurer's **own funds** [R1 L. 134-3][R3 A. 134-2][R13].
- Complementary guarantees (e.g. a death floor) are provisioned **outside** the auxiliary account
  [R2 R. 134-7]. AXA's *garantie décès plancher* on Fonds Croissance is such a guarantee
  [S1][S2].

### 4. Premium, parts and the valeur de la part
- Premiums and incoming transfers/arbitrages, **net of the entry charge permitted by R. 134-3
  1°**, create rights expressed in **number of parts** and, for 1° engagements only, in
  *provision mathématique* [R2 R. 134-2].
- **Number of parts = provision de diversification ÷ part value**, and **the part value is common
  to all engagements** of the account [R2 R. 134-2]. Under the 2° modality this is the whole of
  the saver's value; under 1° it is the non-guaranteed remainder.
- The **initial part value is arbitrary**; the *mémoire* initialises it at **€10** [R13].
- Recursions used by the *mémoire* [R13], written for a 2° (post-PACTE) fund where PM = 0:
  - at t = 0: `PD_0 = net premiums` and `parts_0 = PD_0 / part_value_0`;
  - `PD_i(t) after revaluation = PD_i(t) before revaluation + PB allocated to PD_i(t)
     − PD surrendered(t) − PD on death(t)`;
  - `part_value(t) end of year = part_value(t) start of year
     × PD(t) after revaluation / PD(t) before revaluation`;
  - `PB allocated to PD(t) = Max( PB-account balance net of PCDD movements(t),
     minimum part value × number of parts(t) − PD at start of year(t) )`
    — i.e. the allocation can be negative (the part value falls) but never far enough to take the
    part value below its contractual floor.
- The insurer **guarantees the number of parts but not their value**; the number changes only on
  further premiums, surrenders, death, charges taken in parts, or a profit allocation made in
  parts [R13][S1][R2 R. 134-3 4°, R. 134-4].
- A **minimum value of the part**, strictly positive and expressed in euros, must be fixed by the
  contract and disclosed before the first payment [R2 R. 134-1, R. 134-10 II 1°]. **No public
  figure for this floor was found for any insurer** — a reference implementation must treat it as
  `[std]`.
- The diversification provision must be re-struck at an **intermediate value at least monthly** in
  every month in which the participation account is not struck; that intermediate value is
  `realisation value of assets − (PM + provision de gestion + frais d'acquisition reportés + PCDD
  + PGT)`, and the part value used for a surrender is the one from the next account striking or,
  if earlier, the next intermediate value ÷ the parts then outstanding [R3 A. 134-5].

### 5. The guarantee: level, term, and how it is financed
- The guarantee is **a percentage of premiums paid, net of charges, payable at a maturity fixed
  at subscription**: `MG = g × total net premiums`, with **g between 0 % and 100 %** [R13].
- The *mémoire* runs down the guaranteed amount for exits: `MG(t) = ( total net premiums(t)
  − Σ (surrenders − deaths) ) × g` [R13].
- The guaranteed capital (or the capital constitutive of the guaranteed annuity) is **capped** at
  an amount determined from mortality tables and pricing rates set by arrêté [R2 R. 134-1]. The
  arrêté fixing those tables/rates is not identified in the A. 134 series as retrieved
  — **[unverified]** which text supplies them.
- ACPR's annual return records the guarantee level on a scale of **the proportion of premiums
  guaranteed, origin 0, step 5 percentage points** [R3 A. 134-7]. That is the regulator's own
  granularity for `g` and is the natural grid for a model's parameterisation.
- Observed guarantee levels and terms in the market:
  - AXA Fonds Croissance: **g = 100 %** of net invested capital, term **10 years minimum**
    [S1][S2].
  - Generali G Croissance 2020: **g = 80 %**, term **8 to 30 years**, saver's choice [S8].
  - Predica Objectif Programmé (2014 regime): **g = 80 % to 100 %**, term **8 to 40 years**
    [S7].
- **There is no statutory minimum maturity in the current code.** The 8-year figure quoted
  everywhere in the trade press comes from (a) the 8-year assurance-vie tax threshold and (b) the
  denomination arrêté contemplated by R. 134-1, which does not appear in the codified law — see
  Gaps §3. What the code does say is that a contractual **non-surrender period** may not exceed
  **the lesser of the guarantee maturity and eight years** [R2 R. 134-5][R1 L. 132-23 tenth
  *alinéa*].
- Financing the guarantee differs by modality:
  - **1°**: the guarantee is pre-funded through the **provision mathématique**, i.e. the
    discounted guarantee is carved out of the premium at outset and the remainder goes to the PD.
    The PM grows mechanically as the maturity approaches and as rates fall, squeezing the
    risk-bearing portion [R2 R. 134-2][R13].
  - **2°**: nothing is carved out. **The whole premium buys parts.** The guarantee is financed
    only if and when the assets fall short, through the **PGT**, funded by the insurer's own
    funds [R1 L. 134-3][R3 A. 134-2][R13].

### 6. Provision mathématique (1° engagements) and its discount rate
- `PM = maturity guarantee discounted at a rate fixed by arrêté` [R2 R. 134-2].
- The rate may exceed the pricing rate but is capped at **90 % of the last TECn** published by the
  Banque de France, on one of two bases — **per engagement** with n = that saver's guarantee
  maturity, or **per auxiliary account** with n = the duration of all 1° engagements — with
  **linear interpolation** between bracketing TEC maturities, the **longest available TEC** used
  beyond the curve, the choice of basis binding the whole account and **irreversible**, and a
  **floor of 0 %** if the ceiling computes negative [R3 A. 134-1].
- The *mémoire*'s implementation, for its "old eurocroissance" runs [R13]:
  `PM_i(t) = MG_i(t) / (R_pm × R_t)^N` with `R_pm = 90 %`, `R_t = (1/TEC_t)^(1/t)` and N the
  contract term. It also carries the guarantee through exits:
  `MG_i(t) after movements = MG_i(t) × (1 − (partial lapse + full lapse) − death prob) + net
  premiums_i(t) × g`.
  (The `R_t` expression as printed in the *mémoire* is dimensionally odd — a discount factor of
  the form `1/(1+TEC)` would be expected — so an implementation should treat the **90 % haircut
  on the TEC and the discounting of MG to maturity** as the load-bearing content, not the printed
  algebra.)
- Revaluing the guarantees out of the participation account is only permitted when **both**
  A. 134-3 tests pass: PD attaching to 1° guarantees > **1.5 ×** (zero-rate PM − actual PM), and
  (PD − its minimum) > **10 % of PM** [R3 A. 134-3].

### 7. Provision pour garantie à terme (2° engagements)
- Constituted **per auxiliary account**, equal to the **positive** difference between the
  **present value of the 2° guarantees** and **(PD + PCDD)** [R3 A. 134-2].
- Present value uses the **A. 132-18 mortality tables** and rates **at most equal to A. 134-1 2°**
  (i.e. ≤ 90 % of the TEC at the account's 2°-engagement duration), and counts **no cash flows
  other than guarantee maturities and mortality** — no lapses, no expenses [R3 A. 134-2].
- The *mémoire*'s form [R13]:
  `PGT(t) = Max( MG_discounted(t) − PD(t) − PCDD(t), 0 )`, with
  `MG_discounted(t) = MG(t) / Max(0; (R_pm × R_t)^T)` and `R_pm = 90 %`.
- Backed by an **equivalent asset contribution from the insurer's own funds**; released back when
  representation permits, i.e. on a *retour à meilleure fortune* [R1 L. 134-3][R13].
- **Excluded from the participation account** [R3 A. 134-2 by construction][R13]. A model that
  lets the PGT feed the profit-sharing computation is wrong.

### 8. The participation account and the allocation of its balance
- A *compte de participation aux résultats* is struck; its **credit balance** goes to any mix of
  [R2 R. 134-4]:
  1. the **PM**, by revaluing the guarantees (subject to A. 134-3);
  2. the **PD**, by **awarding new parts** or by **raising the part value**;
  3. the **PCDD**.
- Its **debit balance** is absorbed by a **reprise of the PCDD** or by **reducing the part value,
  down to but not below its contractual minimum** [R2 R. 134-4].
- The *mémoire*'s account [R13]:
  - Income: premiums, transfers and incoming arbitrages; net investment income; reinsurance
    commission retrocession; positive change in unrealised gains.
  - Charges: benefits, transfers and outgoing arbitrages; change in technical provisions (PD and
    PCDD); charges (*chargements*); loss carried forward; negative change in unrealised gains.
  - `Balance = income − charges`; then
    `balance net of PCDD movements = balance − PCDD dotation/reprise`.
- The lever the reform hands the insurer is the **choice between raising the part value (which
  raises every saver's surrender value, and therefore the base on which encours charges are
  taken) and endowing the PCDD (which defers the distribution)** [R13]. Raising **the number of
  parts** rather than the part value is the mechanism PACTE allows for differentiating returns by
  objective criteria such as guarantee level or committed term — because the part **value** must
  be common to all [R2 R. 134-2, R. 134-4][R13].
- Asset affectations and re-affectations completing the account's representation happen **on the
  dates the participation account is struck, after the balance has been allocated**
  [R2 R. 134-4][R7 III]. That fixes the annual processing order for a model.

### 9. Charges (prélèvements)
- The contract must state the insurer's deductions and how they are set and taken. Deductions may
  be taken **only** on the six bases listed at R. 134-3 [R2]:

  | # | Base | Note |
  |---|---|---|
  | 1° | premiums and incoming transfers/arbitrages | the entry load; R. 134-2 nets it before rights are created |
  | 2° | amounts arising from the R. 134-4 conversion of parts into PM | 1° engagements only |
  | 3° | **the provision de diversification** | permitted **only if the auxiliary account holds no 1° engagements** |
  | 4° | **the number of parts** | the unit-linked-style levy PACTE added |
  | 5° | the **balance of the participation account** *or alternatively* the **performance of financial management** of the account's assets | the code as consolidated to 2026-06-27 says "**ou alternativement**" |
  | 6° | benefits paid, outgoing transfers/arbitrages | the exit load |

- **Discrepancy to record.** The *mémoire* states that PACTE made the participation-account levy
  and the asset-performance levy **simultaneous**, where the 2014 regime forced a choice, and
  quotes caps of **15 %** on the participation-account balance and **10 %** on financial
  management performance [R13]. The consolidated R. 134-3 5° as retrieved contains **neither
  cap** and still reads "**ou alternativement**" [R2]. Treat the 15 % / 10 % caps and the
  simultaneity as **[unverified]**; the retrieved code text governs.
- Note the practical consequence of R. 134-3 3°: **an encours-based charge on the diversification
  provision is only available in a pure 2° fund.** A mixed account (1° and 2° grouped under
  L. 134-2) cannot levy on the PD, and must reach the same economics through 4°, 5° or 6°.
- Observed charge levels:
  - **Generali G Croissance 2020** (third-party fact sheet [S8]): *frais de gestion* **1.00 %**,
    *frais sur versements* **4.50 % maximum**, *frais de conversion* **0.50 %**.
  - **AXA Fonds Croissance**: no percentages published; returns quoted net of contract management
    charges; surrender stated to carry **no penalty** [S1][S2].
  - **Actuarial modelling levels used by [R13]** — the closest thing to a documented market
    convention: entry charge **2 % of premiums**; annual management charge **0.8 % of encours**
    (`(PM + PD) × 0.8 %`); performance charge **10 % of positive financial income**, so
    `Charges(t) = (PM(t) + PD(t)) × 0.8 % + 10 % × Max(financial income(t), 0)`. The authors
    state that a levy on premiums plus encours plus performance "est une pratique courante du
    marché actuellement" and that they chose it in preference to a levy on the participation
    account balance. They also model, on the insurer's own cost side, acquisition costs **5 % of
    premiums**, management costs **0.2 % of encours**, acquisition commission **2 % of the
    initial premium**, and asset-management fees of **0.20 %** on equities and **0.10 %** on
    bonds.
- The maximum guaranteed rate ceiling of **A. 132-3** applies to any rate an insurer guarantees
  on these contracts [S4].

### 10. Early surrender (rachat) and transfer
- **1° engagements**: surrender/transfer value before maturity = **PM + (number of parts × part
  value)**, less any R. 132-5-3 indemnity [R2 R. 134-5]. The PM is a floor, so the 2014-regime
  product carried a guarantee at every instant.
- **2° engagements**: surrender/transfer value before maturity = **number of parts × part value**,
  less any R. 132-5-3 indemnity. **There is no guarantee whatsoever before maturity**, and the
  pre-sale documentation must say so in "caractères très apparents" [R2 R. 134-5,
  R. 134-10 I 3°].
- The part value used is the one struck at the next participation account, or the next monthly
  intermediate value ÷ parts outstanding, whichever comes first [R3 A. 134-5]. In practice
  a surrender is priced on a **forward** part value, not a same-day one.
- **Surrender penalty**: the R. 132-5-3 indemnity is capped at **5 %** of the present value of the
  mutual engagements, and **the contract may provide no indemnity at all once ten years have
  elapsed** [R10]. AXA states surrender is available at any time **without penalty** [S2];
  Generali's third-party sheet shows no surrender penalty either, only entry, management and
  conversion charges [S8].
- **Lock-up**: the contract may stipulate that the engagements are **not surrenderable** for a
  period capped at **min(guarantee maturity, 8 years)** [R2 R. 134-5], and that period must be
  disclosed before the first payment [R2 R. 134-10 I 4°]. The L. 132-23 hardship exits (expiry of
  unemployment benefit, judicial liquidation of a self-employed activity, 2nd/3rd-category
  invalidity, serious illness/handicap/accident of a dependent child, death of the spouse or PACS
  partner, over-indebtedness) survive the lock-up [R1 L. 132-23].
- **[R13]** notes that no explicit surrender penalty is needed in practice, because "l'Eurocroissance
  a déjà intrinsèquement une pénalité de rachat par la non-distribution de la PCDD" — the
  surrendering saver walks away from his share of the smoothing reserve.

### 11. Maturity (échéance)
- **1°**: amount due = the R. 134-5 second-*alinéa* value, i.e. **PM + parts × part value**
  [R2 R. 134-6].
- **2°**: amount due = **max( parts × part value, the guarantee )** [R2 R. 134-6]. This is the
  only point at which the guarantee bites.
- Unless the holder decides otherwise **expressly**, the amount is either settled as a benefit or
  **arbitraged into a support with a synthetic risk indicator ≤ 2** [R2 R. 134-6][R3 A. 134-6].
  An SRI of 2 corresponds, per [R13], to a volatility band of roughly **0.5 %–2 %**.
- **Three months before maturity** the holder must be told, on paper or a durable medium, where
  the money will go and how to change that [R2 R. 134-6].
- If the contract offers an annuity, the *capital constitutif* is that maturity amount, expressed
  in euros; on conversion the rights become an ordinary R. 343-3 1° mathematical provision and
  **leave the auxiliary account** [R2 R. 134-6]. From that point the liability is a *rente
  viagère*, not a eurocroissance engagement.
- The *mémoire* models the whole cohort surrendering in full at maturity, and says explicitly that
  modelling annuitisation or reinvestment instead could amplify or damp the effects it studies
  [R13].

### 12. Death before maturity
- The code **does not give the maturity guarantee to a death claim.** R. 134-5 and R. 134-6 speak
  of the surrender/transfer value before maturity and of the amount due **at maturity**; there is
  no death-specific valuation article in Chapter IV [R2].
- Consistently, the *mémoire* prices death at the current provision value:
  `Deaths(t) = death probability(t) × (PM(t) + PD(t))`, with PM = 0 in the post-PACTE fund; the
  released amount reduces the guaranteed amount pro rata through the `MG after movements`
  recursion [R13].
- A death floor is therefore a **complementary guarantee** under R. 134-7, priced and provisioned
  **outside** the auxiliary account [R2 R. 134-7], with its individualised premium disclosed
  before the first payment [R2 R. 134-10 II 2°]. AXA's Fonds Croissance carries a *garantie décès
  plancher* ensuring beneficiaries receive **at least the net invested savings** — standard or
  optional depending on the contract [S1][S2].
- The social levy is settled on death under L. 136-7 II 3° c), net of amounts already levied at
  the guarantee maturity or on the euro part [R11]. The death levy of CGI 990 I then applies to
  the sums paid [R12].
- L. 134-1 excludes **temporary death assurance** from this chapter altogether [R1].

### 13. PCDD — the smoothing reserve
- Defined as a provision "destinée au lissage de la valeur de rachat des contrats" for L. 134-1
  engagements [R8 R. 343-3 10°]. It is **collective**: no saver holds individual rights in it.
- Fed from the credit balance of the participation account [R2 R. 134-4] and from the insurer's
  asset contribution [R7 I].
- **Released at any time** to revalue the PM or the PD [R2 R. 134-4], and used to absorb a debit
  balance [R2 R. 134-4].
- **Must be used within fifteen years**, against eight for a euro fund's *provision pour
  participation aux bénéfices* [R9 A. 132-16]. Under the 2014 regime the limit was **eight years**
  and the reserve was additionally capped at **8 %** of the greater of the zero-rate mathematical
  provisions and the auxiliary-account asset value [R6][R13]; **PACTE removed the volume cap
  entirely** [R13][R21].
- The *mémoire*'s piloting rule, which is a usable `[std]` recipe [R13]:
  - target return `PB_target(t) = net rate credited by the euro fund(t) + 0.30 %`;
  - `target PCDD use(t) = PB_target(t) × (PM(t) + PD(t) at start of year) − change in PM from
    rate movements(t)`;
  - `PCDD target(t) = PCDD at start of year(t) + participation account balance(t) − target PCDD
    use(t)`;
  - `PCDD(t) end of year = Max( Min( PCDD start of year(t), PCDD target(t) ), 0 )`;
  - `dotation/reprise(t) = PCDD end of year(t) − PCDD start of year(t)`, with
    `PCDD start of year(t) = PCDD end of year(t−1) + transfert de richesse(t)`.
  In words: **run the fund at 30 bp above the insurer's own euro fund, and put everything else in
  the PCDD.**
- The *mémoire* records that its model does **not** differentiate PCDD distribution by the saver's
  guarantee level or term, and flags that as the most consequential simplification it makes
  [R13]. Differentiating it is exactly what PACTE's "new parts" allocation route was designed to
  allow [R2 R. 134-4].

### 14. Asset contribution by the insurer (transfert de richesse) — what the brief calls the "bonus"
- The mechanism now lives at **R. 134-12**, reinstated by décret n° 2025-1333 with effect from
  **27 December 2025** [R7].
- Conditions and limits, as retrieved [R7]:
  - the insurer must meet **representation of its regulated commitments and its solvency-margin /
    SCR coverage**;
  - it may contribute cash from a qualifying R. 332-16 account or any R. 342-4 asset,
    **up to 10 % of the diversification provision at the affectation date**;
  - contributed assets enter at **realisation value**, the revaluation difference passing through
    the insurer's own income statement;
  - the contribution **endows the PCDD** by the same amount — it does **not** go straight to the
    savers' PD;
  - it may be re-allocated back out, capped at the **lowest** of (a) affectation-date realisation
    value + its share of net investment income while inside + the R. 134-3 5° performance levies
    over the same period, (b) **10 % of total PD**, (c) total PCDD;
  - re-allocation **no later than during the sixteenth year** following the year of affectation,
    triggering a matching PCDD *reprise*;
  - affectations and re-affectations are made **on the participation-account striking dates,
    after the balance has been allocated**.
- The *mémoire* describes the pre-2025 shape of the same mechanism [R13]: permanent under PACTE,
  **conditional on TEC10 being below the recurring yield of the general fund**, limited so that
  (transferred assets ÷ eurocroissance premiums) stays below the euro fund's **unrealised-gain
  ratio**, and additionally below (euro-fund benefits ÷ euro-fund total asset value) — the second
  limit non-binding in practice because eurocroissance premiums are tiny next to euro-fund
  benefits. Those conditions are **[unverified]** against the retrieved R. 134-12, which states
  the **10 % / 16-year** limits instead. An implementation should use R. 134-12 as retrieved and
  treat the TEC10 condition as historical or as coming from a text not retrieved here.
- The *mémoire*'s modelling level: `transfert de richesse(t) = net premiums(t) × 10 %` for the
  **first three years** only, credited to the PCDD, and — in its asset model — **invested
  entirely in equities** [R13].
- **The term "bonus de mutualisation" appears in none of the retrieved documents.** The code
  calls it *apport d'actifs* [R7][R1 L. 134-3]; practitioners call it *transfert de richesse*
  [R13][R21]. Separately, [R13] tests whether pooling two maturity cohorts in one auxiliary
  account creates a "bénéfice de mutualisation" and concludes it does **not** — the pooling is
  very slightly value-destructive, before any operational simplification gain. Insurer-level
  commercial "bonus" devices do exist but are contractual marketing, not the statutory mechanism:
  AXA's **Eurocroissance +** adds **+2 %** to the base rate on 2026 payments (and +0.5 % on
  pre-2026 euro savings) conditional on **≥ 45 % in unités de compte** or piloted/convention
  management, held to 31 December 2026 and through to the attribution date, no later than
  1 April 2027 [S3][S4].

### 15. Conversion of parts into provision mathématique (1° engagements only)
- The contract may allow parts of the PD to be **converted into provision mathématique**, i.e.
  the saver locks in more guarantee at the cost of upside [R2 R. 134-4].
- Permitted **only once every five years**, and only if after conversion the excess of the
  diversification provision over its minimum (computed from the R. 134-1 minimum part value)
  exceeds **15 % of that engagement's mathematical provision** [R3 A. 134-4].
- A charge may be levied on the converted amounts [R2 R. 134-3 2°]. Generali's third-party sheet
  shows *frais de conversion* of **0.50 %** [S8].
- Not available on 2° engagements, which have no PM.

### 16. Disclosure and supervisory reporting
- Before a **first premium, arbitrage or transfer** into these engagements, in "caractères très
  apparents" [R2 R. 134-10 I]: the **guarantee maturity**; the **euro amount** of the guaranteed
  capital or annuity at maturity; where applicable, a statement of the **absence of any guarantee
  before maturity**; where applicable, the **non-surrender period**; and the **maturity
  settlement arrangements**. Also disclosed [R2 R. 134-10 II]: the **minimum part value in
  euros**; the individualised premium for any complementary guarantee; and the settlement /
  arbitrage / transfer delays and the delay for crediting rights after a premium.
- **Three months before maturity**, notice of the destination of the proceeds and of how to
  change it [R2 R. 134-6].
- The consolidated code also carries a **model note d'information** for *plans d'épargne retraite
  populaire* that include a provision de diversification, requiring a transfer-value table for at
  least the **first eight years** split between the diversification and mathematical provisions,
  the transfer value at the diversification provision expressed **in number of parts** for a
  generic part count, and a very prominent statement that **the insurer commits only to the number
  of parts and not to the part value, which fluctuates up and down**, plus a statement that
  charges may be **unlimited in number of parts** where they cannot be quantified in advance.
  This model is **PERP-scoped**, and the exact article number (in the A. 132-5-x series) is
  **[unverified]**; it is recorded because it is the only place in the code that shows the
  standard consumer wording for this product family.
- **Annual ACPR return by 30 April**, separately for 1° and 2° engagements, **by maturity year and
  by guarantee level (origin 0, 5-point steps)**: contracts in force, mathematical provisions,
  diversification provision, premiums and incoming transfers/arbitrages, and the balance-sheet
  value of the account's assets by R. 332-2 nomenclature; aggregated by ACPR and sent to the
  minister with the list of undertakings [R3 A. 134-7]. **These aggregates are not published**,
  which is why the market has to be sized from France Assureurs [R14].

### 17. Taxation and social levies
- **Income tax**: the ordinary assurance-vie regime of CGI 125-0 A applies — gains taxed on
  *dénouement* or partial surrender, exemption where the contract is wound up as a life annuity or
  on redundancy / early retirement / 2nd–3rd category invalidity, gain = sums repaid minus
  premiums [R12]. The 8-year seniority thresholds and the PFU rate split (7.5 % / 12.8 % around a
  €150 000 premium threshold) are the standard assurance-vie parameters but were **not located in
  the retrieved CGI text** and are **[unverified]** here; they belong to the euro/UC research
  files.
- **Transformation neutrality**: converting all or part of a contract so that premiums buy
  unit-linked rights **or diversification-provision rights** does **not** produce the tax
  consequences of a *dénouement*, whether done by endorsement or by a new contract with the same
  insurer [R12 CGI 125-0 A I 2°]. This is what preserves fiscal seniority on a move into
  eurocroissance. A conversion condition of "at least 10 % of euro engagements" and a **0.32 %**
  transfer levy are reported by a secondary source [S9]; **neither appears in the current CGI
  text** as retrieved, and both are **[unverified]** — most likely historical.
- **Social levies — the genuinely product-specific rule**: CSG/CRDS on diversification-provision
  engagements is levied **"à l'atteinte de la garantie"**, i.e. when the contractual maturity is
  reached, on a base of **the surrender value of those engagements at that moment minus the
  premiums allocated to them, net of premiums already included in partial surrenders**
  [R11 CSS L. 136-7 II 3° b)]. Euro-denominated rights are levied annually on inscription
  (a)); everything else is levied on *dénouement* or death (c)), net of what was already taken
  under a) and b). So eurocroissance sits between the two: **no annual social-levy drag, but a
  levy event at maturity even if the contract is not surrendered**.
- **Death**: CGI 990 I — 20 % proportional abatement for qualifying contracts, **€152 500** fixed
  abatement per beneficiary, then **20 %** up to **€700 000** of taxable share and **31.25 %**
  above [R12].

### 18. Market size, distribution, and published returns
- **Encours and contract counts** (all from retrieved documents):

  | Date | Eurocroissance encours | Contracts | Source |
  |---|---|---|---|
  | end-2022 | €7.1 bn | — | [R21] |
  | mid-2023 | €7.6 bn (+41 %) | > 470 000 | [R21] |
  | end-2024 | **€11.1 bn (+24 %)** | **673 000 (+26 %)** | [R14] |
  | March 2025 | €11.3 bn | > 700 000 (croissance + eurocroissance) | [S9] |
  | end-2025 | not published | not published | [R16] carries no eurocroissance line |

- Against a market of **€1 989 bn** at end-2024 [R14] / **€2 107 bn** at end-2025 [R16],
  eurocroissance is roughly **0.5 %** of French life insurance. For scale, unit-linked alone was
  **€587.1 bn** at end-2024 [R15].
- **Published 2025 net returns on eurocroissance supports** (net of management charges, gross of
  tax and social levies) [S9], cross-checked where possible:

  | Support | Insurer | 2025 | Cross-check |
  |---|---|---|---|
  | G Croissance 2020 | Generali | 3.40 % | 3.40 % [S8] |
  | Générations Croiss@nce durable | Generali | 3.40 % | — |
  | Agipi eurocroissance | AXA France | 3.00 % | — |
  | Fonds Croissance | AXA France | 2.50 % | range 2.50 %–4.50 %, average **3.13 %** [S3] |
  | G Croissance 2014 | Generali | 2.20 % | — |
  | Afer eurocroissance | Abeille Assurances | 2.16 % | — |
  | Croissance Allocation Long Terme | Spirica | 0.90 % | — |

- **Comparison with euro funds in the same year**: AXA euro 2.25 %–4.25 % against Fonds Croissance
  2.50 %–4.50 % [S3]; Generali euro-fund average **2.55 %** for life and **3.30 %** for PER [S6].
  The eurocroissance premium over the euro fund at the same insurer is of the order of
  **25–60 bp**, which is close to the **30 bp** target the *mémoire* assumed as the piloting
  objective [R13].
- **Longer history for one support** [S1]: AXA Fonds Croissance 2.40 % (2018), 3.00 % (2019),
  2.60 % (2020), 3.00 % (2021), 3.30 % (2022), 3.30 % (2023), "2 à 4 %" (2024, 2025), average
  annualised since 2017 **2.98 %**. G Croissance 2020, launched into the 2020–2022 rate trough,
  shows 0.52 % (2020) and 0.05 % (2022) before recovering to 3.67 % / 3.55 % / 3.40 %
  (2023/24/25) [S8] — a spread of over 350 bp across five years, which is the volatility the
  product is supposed to have and the euro fund is not.
- **Why it has not sold.** The reasons given by [R13], which interviewed AXA and Allianz, and
  echoed by [R21]:
  - the split between PM and parts under the 2014 regime was **hard to explain**, produced a
    **different return for every saver** depending on entry date, maturity and guarantee level,
    and generated an information regime so heavy that it raised *renonciation* risk;
  - **implementation cost**: frequent publication of part values, ring-fenced accounting, asset
    and ALM skills normally outsourced to asset managers had to be brought in-house, plus IT and
    distributor training;
  - **the low-rate environment**: with rates low, the PM absorbed most of the premium, leaving
    little to invest in risk assets, so the product could not out-earn a mature euro fund sitting
    on decades of accumulated unrealised gains;
  - **poor economics for the insurer**: the any-instant guarantee was capital-expensive, and the
    2014 charging rules forced a choice between a levy on the participation account and a levy on
    asset performance, with no levy in number of parts;
  - several large carriers, **Allianz among them, simply never launched** a eurocroissance fund
    [R13];
  - post-PACTE, the remaining brakes are **no track record**, a product still more complex than a
    euro fund or a UC, an awkward position in the range (does it replace the euro fund or the UC
    sleeve?), and the fact that the *transfert de richesse*, when used, **dilutes the euro fund's
    unrealised gains** and so cuts into the insurer's own economics [R13].
  - Sia Partners' 2023 verdict is the same in one line: "seule une poignée d'assureurs proposent
    le nouvel Eurocroissance" [R21].

### 19. A documented parameter set for a reference implementation
Everything in this section is from the published actuarial *mémoire* [R13]. It is the only
retrieved document that states a complete, internally consistent parameterisation, and it is a
defensible anchor for `[std]` choices. Annual time step throughout.

| Parameter | Value | Note |
|---|---|---|
| Initial premium | €10 000 | homogeneous cohort |
| Free additional premiums | 15 %–30 % of savers pay **€2 000** | same guarantee rate and maturity as the initial premium |
| Entry charge | **2 %** of each premium | reduces the guaranteed amount too |
| Annual management charge | **0.8 %** of (PM + PD) | PM = 0 for the post-PACTE fund |
| Performance charge | **10 %** of positive financial income | i.e. 90 % of positive asset performance to savers, 100 % of negative |
| Guarantee rate `g` | **100 %** of net premiums | sensitivities run at other levels |
| Maturity | **10 years** (single-cohort run); 10 and 15 years (two-cohort run) | |
| Age at subscription | **57** | |
| Mortality | "Table de Mortalité TH00-05" as printed | almost certainly a typo for the regulatory **TH 00-02**; treat the exact table as **[unverified]** |
| Partial surrenders | **6 %** of average encours in years 1–2, then **2 %–4 %** | no dynamic lapse modelled |
| Full surrenders | **2 %–3 %** per year | no surrender penalty modelled |
| Initial part value | **€10** | arbitrary by construction |
| Discount haircut `R_pm` | **90 %** | the A. 134-1 factor |
| Transfert de richesse | **10 % of net premiums**, first **3 years**, to the PCDD, invested 100 % in equities | |
| PCDD target return uplift | **+0.30 %** over the insurer's own euro fund | the piloting objective |
| Asset allocation | guarantee covered with zero-coupon OATs of maturity equal to the term; remainder in equities (Euro Stoxx 50 characteristics) | deliberately simplified two-asset SAA |
| Asset management fees | **0.20 %** equities, **0.10 %** bonds | deducted from asset return |
| Insurer's own costs | acquisition **5 %** of premiums, management **0.2 %** of encours, acquisition commission **2 %** of the initial premium | variable costs only, no fixed costs |
| Cost of capital (risk margin) | **6 %** | the pre-reform Solvency II figure |
| Scenarios | 1 000 stochastic market scenarios | risk-neutral; the authors note real-world scenarios could change conclusions |

Insurer top-up (*abondement*) recursion, for the 1° (old) product where the insurer must make good
a debit balance [R13]:
`abondement(t) = −Min( 0, participation-account balance net of PCDD(t) − PB allocated to PD(t) )`,
accumulating into a `solde débiteur` carried forward as a charge of the next participation account.

---

## Variations across insurers

Only three insurers' eurocroissance terms could be documented at all, and only one of them
(Generali, and that via a third party) with charge levels. The table records what was retrieved.

| Feature | AXA France — Fonds Croissance [S1][S2][S3][S4] | Generali — G Croissance 2020 [S8], G Croissance 2014 [S5] | Predica/Crédit Agricole — Objectif Programmé [S7] |
|---|---|---|---|
| Regime | post-PACTE (2° modality: insurer commits to the number of parts, not their value) | G Croissance 2020 built for PACTE; G Croissance 2014 is the old regime | 2014 regime (launched 16 October 2014) |
| Guarantee level `g` | **100 %** of net invested capital | **80 %** | **80 % to 100 %**, saver's choice |
| Guarantee term | **10 years minimum** from first investment | **8 to 30 years**, saver's choice | **8 to 40 years**, saver's choice |
| Entry charge | not published | **4.50 % max** | not published |
| Annual management charge | not published (returns quoted net) | **1.00 %** | not published |
| Conversion charge | not published | **0.50 %** | not published |
| Surrender penalty | **none** stated | none shown | not published |
| Death floor | **garantie décès plancher** — at least net invested savings | not documented | not documented |
| SRI | **2 / 7** | not documented | not documented |
| 2025 net return | **2.50 %–4.50 %**, average **3.13 %** | **3.40 %** (2020 vintage), **2.20 %** (2014 vintage) | fund **closed to new business since 1 October 2020** [unverified — reported by a secondary source, not retrieved] |
| Commercial bonus | **Eurocroissance +**: +2 % on 2026 payments, +0.5 % on pre-2026 euro savings, conditional on ≥ 45 % in UC or piloted/convention management | none documented | none documented |
| Distribution | Arpèges, Excelium, Privilège, Odyssiel, Expantiel, Figures Libres, Optial, Amadéo, PER "Ma Retraite" | Himalia, Espace Invest 5, L'Epargne Generali Platinum, Himalia Patrimoine, ING Direct Vie | Floriane, Espace Liberté 2 (Crédit Agricole); Lionvie Rouge Corinthe, Acuity (LCL) |

Other supports known to exist from the cross-market rate table [S9], with no product
documentation retrieved: **Générations Croiss@nce durable** (Generali), **Agipi eurocroissance**
(AXA France), **Afer eurocroissance** (Abeille Assurances), **Croissance Allocation Long Terme**
(Spirica).

What actually varies, and what does not:
- **Fixed by law, identical across insurers**: the two modalities and their surrender/maturity
  formulas [R1][R2 R. 134-5, R. 134-6]; the six permitted charge bases [R2 R. 134-3]; the part
  value being **common to all engagements of an auxiliary account** [R2 R. 134-2]; the 90 %-of-TEC
  discount ceiling and its irreversible per-account method choice [R3 A. 134-1]; the PGT
  definition [R3 A. 134-2]; the 15-year PCDD clock [R9]; the 5 % surrender-indemnity cap and its
  disappearance after ten years [R10]; the 10 % / 16-year asset-contribution limits [R7]; the
  ≤ SRI 2 maturity default [R3 A. 134-6]; and the social levy at the guarantee maturity [R11].
- **Set by the insurer, and the real product levers**: the **guarantee level `g`** (80 % vs 100 %
  is the sharpest observed difference, and it is what decides how much of the fund can sit in
  risk assets); the **maturity range offered** (10 fixed at AXA, 8–30 at Generali, 8–40 at
  Predica); the **minimum part value** (nowhere published); the **charge structure**, which the
  code constrains only by base and not by level; and the **PCDD piloting rule**, which is
  discretionary and unpublished and which drives the credited return more than anything else.
- **Set by the insurer and openly marketed**: the commercial bonus devices, which are conditional
  on unit-linked allocation and are contractual promotions, not the statutory *apport d'actifs*
  [S3][S4].
- **A structural consequence a modeller must respect**: because the part value is common,
  **savers with different maturities and different guarantee levels in the same auxiliary account
  all receive the same rate of return**. Differentiation is possible only through the number of
  parts or through differentiated PCDD distribution [R2 R. 134-2, R. 134-4][R13]. Any model that
  gives per-policy returns in a 2° fund is modelling something that does not exist.

---

## Gaps and caveats

1. **No contractual document was retrieved for any eurocroissance support.** No *notice
   d'information*, no *conditions générales*, no PRIIPs *document d'information clé*. S10 records
   the Generali documents as a known reference with no URL. Every product-level parameter above
   comes from insurer marketing pages [S1][S2][S3][S4][S5][S6][S7] or from third-party fact pages
   [S8][S9]. In particular, **charge levels for AXA and Predica, and the minimum part value for
   every insurer, are unknown**; a reference implementation must mark them `[std]`.

2. **Failed fetches.** ACPR's "L'assurance-vie en 2025" (n° 179) returned **HTTP 403** on
   WebFetch twice and on `curl` with a browser User-Agent [R20], even though the same technique
   retrieved three other ACPR PDFs [R17][R18][R19]. Profession CGP's eurocroissance analysis
   returned **HTTP 403** twice [S11]. The Légifrance page for **ordonnance n° 2014-696** was not
   resolved [R22] — a guessed identifier returned an empty page and the web-search budget was
   exhausted before a verified URL could be obtained, so the ordonnance's article 3 (the
   transformation regime L. 134-1 disapplies) is uncharacterised. **Note for future work**: ACPR
   and France Assureurs PDFs are reachable with `curl -A "<browser UA>"` where a plain fetcher
   403s; that technique was used for [R17][R18][R19] and for the consolidated code PDFs behind
   [R1][R2][R3][R8][R9][R10][R11][R12].

3. **The "eurocroissance" denomination arrêté appears never to have been issued.** R. 134-1 third
   *alinéa* provides that an arrêté "détermine une dénomination et les conditions minimales,
   s'agissant notamment de l'échéance et du niveau de garantie en capital" for use of that name
   in documents intended for third parties [R2]. Searching the **full consolidated Code des
   assurances** (872 pages, edition 2026-07-19, last modified 2026-06-27) for the strings
   "eurocroissance" and "euro-croissance" returns **zero hits**, and the A. 134 chapter
   (A. 134-1 to A. 134-7, all retrieved) contains no denomination article. The widely repeated
   claims that the name "eurocroissance" is **reserved for a 100 % guarantee** and requires a
   **minimum 8-year maturity**, with 80 %-guarantee funds having to be called "croissance"
   [S9][R21], therefore **could not be traced to any retrieved legal text and are marked
   [unverified]**. It is possible the arrêté exists uncodified; it is equally possible the
   convention is purely commercial. Note that Generali markets an 80 %-guarantee fund as
   "G Croissance" and AXA a 100 %-guarantee fund as "Fonds Croissance" [S8][S1], which is not
   consistent with the reported convention either.

4. **R. 134-3 5° discrepancy.** The actuarial *mémoire* states that PACTE allows the levy on the
   participation-account balance and the levy on financial-management performance to be taken
   **simultaneously**, and quotes caps of **15 %** and **10 %** respectively [R13]. The
   consolidated R. 134-3 5° as retrieved reads "sur le solde du compte de participation aux
   résultats **ou alternativement** sur les performances de la gestion financière des actifs" and
   states **no caps** [R2]. The retrieved code text governs; the *mémoire*'s statement and the
   15 % / 10 % caps are **[unverified]**.

5. **Transfert de richesse conditions differ between sources.** [R13] describes the mechanism as
   conditional on **TEC10 < the recurring yield of the general fund**, and limited by the euro
   fund's unrealised-gain ratio and by the ratio of euro-fund benefits to euro-fund assets. The
   reinstated R. 134-12 [R7] states instead a **10 % of PD** contribution limit, a three-way
   re-allocation cap, and a **16-year** deadline, and conditions the contribution on the
   insurer's own regulated-commitment representation and solvency coverage. The two descriptions
   are not obviously reconcilable; the *mémoire*'s conditions predate décret n° 2025-1333 and are
   **[unverified]** against the current text. The 2016 and 2018 décrets that first enabled the
   mechanism were not retrieved.

6. **The mémoire's date and one of its tables.** The Institut des actuaires *mémoire* [R13] is
   undated on its cover; its placement in 2020–2021 is inferred from internal references and is
   **[unverified]**. Its mortality table is printed as "TH00-05", which is not a French regulatory
   table name — almost certainly **TH 00-02** — so the exact base table is **[unverified]**. Its
   printed discount expression `R_t = (1/TEC_t)^(1/t)` is dimensionally suspect and should not be
   copied literally; only the 90 % TEC haircut and the discounting of the guaranteed amount to
   maturity are load-bearing.

7. **Eurocroissance is invisible in the standard statistics.** ACPR's weekly life-flows collection
   **explicitly excludes eurocroissance products** [R18], the annual market study does not break
   them out [R17], and neither does the revaluation study [R19]. France Assureurs published a
   eurocroissance line in its January 2025 release [R14] but **not** in its January 2026 release
   [R16], so the end-2025 encours and contract count are **not available from a retrieved
   source**. The only complete data set — the A. 134-7 return by maturity year and guarantee level
   [R3] — goes to ACPR and the ministry and is **not published**. Anyone needing a 2025 or 2026
   market size will have to obtain it from France Assureurs directly.

8. **Regulatory tables are cited, not shipped.** A. 134-2 values the PGT on the **A. 132-18**
   tables [R3][R10]; those are the homologated regulatory tables (TH/TF 00-02 for capital
   contracts, TGH/TGF 05 for annuities) annexed to the arrêté du 1er août 2006, which is
   **[unverified]** here because that arrêté was not retrieved in this session, and which is in
   any case restricted from redistribution. The frlib decrement CSVs must be `[std]` proxies built
   from INSEE data, as the house contract requires. A. 132-18 also permits **insurer tables
   certified by an independent approved actuary** [R10], which is why no single market mortality
   basis exists for this product.

9. **Tax parameters outside the eurocroissance-specific rule.** The PFU rate split and the
   €150 000 premium threshold were **not located** in the retrieved CGI text and are
   **[unverified]** here; the €4 600 / €9 200 PER-transfer exemption, the transformation
   neutrality of CGI 125-0 A I 2°, the 990 I abatements and rates, and the CSS L. 136-7 II 3° b)
   "atteinte de la garantie" trigger **were** retrieved and are safe. The reported **10 %
   conversion condition** and **0.32 % transfer levy** [S9] appear nowhere in the current CGI as
   retrieved and are **[unverified]**.

10. **PERP disclosure model.** The model *note d'information* wording quoted in §16 ("the insurer
    commits only to the number of parts…") was read verbatim from the consolidated code, but its
    exact article number in the A. 132-5-x series is **[unverified]** and it is **PERP-scoped**,
    not a general eurocroissance disclosure rule. It is recorded only because it is the sole place
    in the code that fixes consumer-facing wording for a diversification provision.

11. **Living texts.** The Code des assurances edition used is dated **2026-07-19** (last
    modification 2026-06-27); L. 132-23 as read carries a version from **LOI n° 2026-492 du
    12 juin 2026**, L. 136-7 CSS from **LOI n° 2026-103 du 19 février 2026**, and R. 134-12 is
    **eight months old** at the access date. R. 134-12's reinstatement in December 2025 means the
    asset-contribution mechanism was **absent from the code for some period** before that; when
    it lapsed and what governed in the interval was not established. Check for later amendments
    before relying on any article number here.

12. **One insurer, one modality.** Only AXA's Fonds Croissance was documented clearly enough to
    identify its modality (2°, guarantee at maturity only) [S1][S2]. Whether Generali's
    G Croissance 2020, Afer eurocroissance, Agipi eurocroissance or Spirica's Croissance
    Allocation Long Terme are written under 1° or 2° is **unknown**; G Croissance 2014 and
    Predica's Objectif Programmé are pre-2020 and therefore presumptively 1°, but neither was
    confirmed against a contractual document.
