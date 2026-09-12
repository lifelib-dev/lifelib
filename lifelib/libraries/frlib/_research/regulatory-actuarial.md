# French regulatory and actuarial reference library — annotated bibliography

Cross-product references for France life insurance liability cash flow modeling. Compiled
2026-08-26 (all access dates 2026-08-26). Citation ids **R1–R49 are frozen**: the nine frlib
product documents cite these tags verbatim as `[REG-R#]`; never renumber. Facts recorded under
an entry were read directly from the fetched document. `[unverified]` marks a claim taken from
general knowledge or from a search-result summary of a document that could **not** be retrieved.
`Retrieved: YES` means the annotated content was actually fetched and read in this session;
`Retrieved: NO` records the failure and the reason, and anything resting on that entry alone is
`[unverified]`.

Regulatory architecture in one line: prudential supervision is Solvency II as transposed into
the **Code des assurances**, enforced by the **ACPR** (an authority attached to the Banque de
France); conduct and information duties sit in the Code des assurances Livre I and, for
distribution, in Livre V after the DDA transposition; the **AMF** regulates the underlying
collective investment vehicles used as *unités de compte*; the **HCSF** holds a macroprudential
power to freeze surrenders; and a distinctive French layer — *participation aux bénéfices*
(profit sharing), the *provision pour participation aux bénéfices* and the statutory mortality
tables — sits on top of, and is legally independent of, the Solvency II balance sheet.

Two French terms carry the whole library and are used untranslated after first use:

- **fonds en euros** — the general account with a capital guarantee (*effet cliquet*: once
  credited, interest cannot be taken back) and a discretionary annual *revalorisation*.
- **participation aux bénéfices (PB)** — the statutory minimum profit share owed to
  policyholders collectively, computed from a *compte de participation aux résultats* and
  either credited immediately to the *provision mathématique* or parked in the
  **provision pour participation aux bénéfices (PPB, sometimes PPE)** for up to eight years.

Scope note on capital: the SCR and MCR exist under Solvency II [R1][R4], but this library treats
the capital layer as **cited-not-specified**. The models produce best-estimate liability cash
flows; SCR aggregation, the risk margin projection and own funds are referenced only.

**Product key** used in the "Products" line of each entry:
`AVE` assurance vie fonds en euros · `AVUC` assurance vie unités de compte · `EC` eurocroissance
· `PER` PER assurantiel · `RV` rente viagère immédiate · `TD` temporaire décès ·
`ADE` assurance emprunteur · `OBS` obsèques · `DEP` dépendance.

**Host behaviour observed in this session** (see also *Gaps and caveats*):
`legifrance.gouv.fr` serves fully to a plain fetcher and is the workhorse of this file;
`franceassureurs.fr`, `insee.fr`, `drees.solidarites-sante.gouv.fr`, `cnsa.fr`,
`institutdesactuaires.com`, `amf-france.org`, `eiopa.europa.eu` and `ifrs.org` all serve.

**Correction, 2026-08-26.** An earlier version of this file recorded that
`acpr.banque-france.fr` and `banque-france.fr` "return HTTP 403 to every request, with and
without a browser User-Agent". **That is false and is withdrawn.** The ACPR host serves
normally; the discriminator is the *fetcher*, not the User-Agent. The plain WebFetch tool used
for the rest of this sweep is refused with an "Accès refusé" page, while `curl` retrieves the
same URLs with **HTTP 200 and byte-identical responses with and without a browser
User-Agent** — verified on `https://acpr.banque-france.fr/` (200), `https://www.banque-france.fr/fr`
(200), both *Analyses et Synthèses* landing pages (200) and four ACPR PDFs (200,
`application/pdf`, 0.9–2.0 MB each). A second trap compounded the error: this host answers a
**wrong** path under `/system/files/` with **403**, not 404, so one mistyped PDF URL looked
exactly like a domain-wide block. Both ACPR entries [R11][R12] have been re-fetched with `curl`,
read in full, and are now `Retrieved: YES`; everything this file previously deferred to
"the ACPR is blocked" has been rewritten against the documents.

**`eur-lex.europa.eu` sits behind an AWS WAF JavaScript challenge** and returns an empty
document to any non-browser client. That block is real and stands: every EUR-Lex entry below is
`Retrieved: NO`.

---

## 1. Prudential — Solvency II

### R1. Directive 2009/138/CE — Solvabilité II
- Publisher: European Parliament and Council (EUR-Lex)
- Doc type: directive (consolidated text)
- URL: https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32009L0138
- Retrieved: **NO** — EUR-Lex is behind an AWS WAF JavaScript challenge; a plain fetch returns
  HTTP 202 with an empty body, and a browser User-Agent gets the same challenge page. Known
  reference only.
- Content: the Level 1 directive establishing the risk-based prudential regime for EU insurance
  and reinsurance undertakings. Its description in this library is taken from EIOPA's own
  framework page [R4], not from the directive text. Its central rule for a cash flow model —
  technical provisions equal a **best estimate** (probability-weighted average of future cash
  flows discounted at the relevant risk-free term structure) plus a **risk margin** — is stated
  by EIOPA [R4] and is the basis on which the French products in this library are valued; the
  specific article numbers (Art. 76–86) are **[unverified]** here because the text could not be
  read.
- Products: all nine.

### R2. Règlement délégué (UE) 2015/35
- Publisher: European Commission (EUR-Lex)
- Doc type: delegated regulation
- URL: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R0035
- Retrieved: **NO** — same AWS WAF challenge as R1. Known reference only.
- Content: the Level 2 implementing measures for Solvency II. EIOPA confirms it was **adopted
  10 October 2014 and published 17 January 2015**, and that it is "directly applicable" without
  national implementation [R4]. The detailed articles a French modeller needs — contract
  boundaries, expense assumptions, the cost-of-capital risk margin, the standard formula
  sub-modules — could not be read here and are **[unverified]**.
- Products: all nine.

### R3. Directive (UE) 2025/2 — the Solvency II review
- Publisher: European Parliament and Council (EUR-Lex)
- Doc type: amending directive
- URL: https://eur-lex.europa.eu/eli/dir/2025/2/oj
- Retrieved: **NO** — AWS WAF challenge (three URL forms tried: `/eli/`, `/legal-content/.../HTML/`,
  `/legal-content/.../PDF/`). Known reference only.
- Content: the amending directive from the 2019–2021 Solvency II review. EIOPA's own page
  states that Directive (EU) 2025/2 amends the Solvency II framework and that **the new rules
  take effect 30 January 2027** [R4] — that date is verified. Everything else commonly reported
  about it (entry into force 28 January 2025, proportionality regime, sustainability and
  climate-risk requirements, macroprudential tools, liquidity risk management plans, changes to
  the risk margin and the volatility adjustment) comes only from search-result summaries and is
  **[unverified]**.
- Products: all nine (forward-looking; none of the frlib models implements a 2027 basis).

### R4. EIOPA — "Solvency II" (regulation and policy framework page)
- Publisher: European Insurance and Occupational Pensions Authority
- Doc type: regulator framework page
- URL: https://www.eiopa.europa.eu/browse/regulation-and-policy/solvency-ii_en
- Retrieved: **YES**
- Content: verified directly — Directive 2009/138/EC was adopted November 2009 and "sets out
  requirements applicable to insurance and reinsurance companies in the EU with the aim to
  ensure the adequate protection of policyholders and beneficiaries"; Delegated Regulation (EU)
  2015/35 was adopted 10 October 2014 and published 17 January 2015 and is directly applicable;
  the regime is organised in three pillars (I quantitative — valuation of assets and liabilities
  and capital requirements; II governance, risk management and ORSA; III supervisory reporting
  and public disclosure); the approach is described as market-consistent, risk-based and
  proportionate; EIOPA delivered its technical advice on the 2020 review on 17 December 2020;
  **Directive (EU) 2025/2 amends the framework with new rules taking effect 30 January 2027**.
  This entry is the verified carrier for R1–R3.
- Products: all nine.

### R5. EIOPA — Risk-free interest rate term structures
- Publisher: EIOPA
- Doc type: data and technical documentation hub
- URL: https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en
- Retrieved: **YES**
- Content: EIOPA publishes the relevant risk-free interest rate (RFR) term structures **monthly**,
  as ZIP packages, so that technical provisions for (re)insurance obligations are calculated
  consistently across the EU. The packages contain the risk-free rates, the **volatility
  adjustment**, the **matching adjustment fundamental spreads** and the **ultimate forward rate
  (UFR)** used in the extrapolation. A release calendar is published (dates listed for 2026
  include 3 September, 5 October, 5 November, 3 December). EIOPA additionally publishes
  *shifted* RFR term structures semi-annually for financial-stability reporting (option-adjusted
  duration). EIOPA disclaims liability for reliance on the data. Numeric curve values were not
  extracted here — the frlib models use flat or scenario discount rates marked `[std]`.
- Products: all nine (discounting), most materially AVE, EC, PER, RV, DEP.

---

## 2. Prudential — French technical provisions (Code des assurances, French GAAP)

The Solvency II balance sheet does **not** replace the French statutory (French GAAP, "comptes
sociaux") technical provisions. Both exist. The PB obligation [R14][R15] and the PPB
eight-year rule [R16] operate on the **French GAAP** accounts, not on the Solvency II ones —
which is exactly why a French model must carry both a *provision mathématique* recursion and a
best-estimate projection.

### R6. Code des assurances, art. R. 343-3 — the eleven life technical provisions
- Publisher: Légifrance (Direction de l'information légale et administrative)
- Doc type: regulatory code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739686
- Retrieved: **YES** (version in force since **1 January 2020**)
- Content: verified — for life, *nuptialité-natalité* and capitalisation operations, the article
  enumerates eleven technical provisions, each engagement being provisionable under exactly one
  of them:
  1. **provision mathématique** — the difference between the actuarial present values of the
     insurer's and the insured's respective commitments, *including future management costs*;
  2. **provision pour participation aux bénéfices (PPB)** — profit shares attributed to
     policyholders but not payable immediately after the close of the financial year that
     produced them;
  3. **réserve de capitalisation** — a reserve against depreciation of the undertaking's assets
     and reduction of their income;
  4. **provision de gestion** — future management charges not covered elsewhere;
  5. **provision pour aléas financiers (PAF)** — compensates a decline in asset yield;
  6. **provision pour risque d'exigibilité (PRE)** — for commitments in case of overall
     depreciation of the assets listed in art. R. 343-10, detailed in art. R. 343-5 [R7];
  7. **provision pour frais d'acquisition reportés**;
  8. **provision pour égalisation** — mortality fluctuations on group death business;
  9. **provision de diversification** — absorbs asset fluctuations for art. L. 134-1
     commitments where holders' rights are individualised (the eurocroissance vehicle) [R19];
  10. **provision collective de diversification différée** — smooths surrender values on
      art. L. 134-1 commitments;
  11. **provision de garantie à terme** — asset shortfall against a maturity guarantee under
      art. L. 134-1.
  Valuation follows the accounting standards set by the Autorité des normes comptables and by
  ministerial arrêté.
- Products: AVE, AVUC, EC, PER, RV, TD, ADE, OBS, DEP (items 9–11 only EC).

### R7. Code des assurances, art. R. 343-5 — provision pour risque d'exigibilité (PRE)
- Publisher: Légifrance
- Doc type: regulatory code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030576275
- Retrieved: **YES** (version in force since **1 January 2016**)
- Content: verified — the PRE is constituted when the investments listed at art. R. 343-10
  (excluding amortisable securities the undertaking has the capacity and intention to hold to
  maturity) are in a position of **net overall unrealised depreciation**. The annual charge is
  **one third of the net overall unrealised depreciation**, provided the balance-sheet total of
  the provision does not exceed that depreciation. Valuation rules: quoted securities at the
  **30-day average price** before the inventory date; fund units at the 30-day average
  redemption price; other assets per art. R. 343-11. Unrealised gains and losses on derivatives
  whose underlyings are eligible assets are included, unrealised losses only above the value of
  collateral.
- Products: AVE, EC, PER, RV (the general-account books that hold the exposed assets).

### R8. Provision pour aléas financiers — Code des assurances, art. A. 331-2 (abrogated 1.1.2016) and the arrêté du 23 décembre 2008
- Publisher: Légifrance
- Doc type: arrêté-level code article (historic version) + amending arrêté
- URLs:
  - art. A. 331-2 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006787843
  - arrêté du 23 décembre 2008 — https://www.legifrance.gouv.fr/loda/id/JORFTEXT000020009363
- Retrieved: **YES** for the article (the version displayed runs **14 September 2014 to
  1 January 2016**, i.e. the last text before the Solvency II recodification); **PARTIAL** for
  the arrêté — Légifrance served the metadata and the list of amended articles but not the
  substantive text.
- Content: verified from the article — the PAF bites when the **real rate of return on the
  assets, reduced by one fifth** (i.e. 80 % of it), is **less than** the quotient of
  (total technical interest + the minimum contractually guaranteed participation aux bénéfices
  under art. A. 132-2 [R18]) divided by the **average mathematical provisions**. When it bites,
  the charge is the difference between (a) mathematical provisions recomputed by discounting
  future payments at one of three permitted rates — **60 % of the average State-borrowing rate
  (TME)**, a weighted average of rates by asset category, or a prudently estimated future asset
  yield — and (b) the mathematical provisions at the inventory date. The provision is **reversed
  at the following inventory**. From the arrêté: it amended art. A. 331-2 and created an
  *Annexe à l'article A. 331-2*, applicable to **financial years opening on or after 1 January
  2009** (optional application in 2008).
  **Caveat**: art. A. 331-2 was abrogated at the 1 January 2016 recodification. R. 343-3 5°
  [R6] still names the PAF and art. A. 341-1 4° [R9] still refers to it, so the provision
  survives; the *current* article carrying the computation was not located, and the formula
  above is therefore recorded from the last pre-2016 text. Treat the article reference — not the
  mechanics — as **[unverified]** for current dates.
- Products: AVE, EC, PER, RV.

### R9. Code des assurances, art. A. 341-1 — ACPR derogations, including the PAF forward-yield estimate
- Publisher: Légifrance
- Doc type: arrêté-level code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031773094/2025-03-27
- Retrieved: **YES** (confirmed as art. A. 341-1, version in force since **1 January 2016**)
- Content: verified — the ACPR may authorise an undertaking to depart from arts. R. 343-3 and
  R. 343-7 in four cases: (1) statistical methods to estimate claims of the last two financial
  years; (2) retaining a lower internal estimate of outstanding claims than the regulatory
  formula, where based on sufficient information and reliable statistics; (3) modifying the
  parameters of the *provision pour risques en cours* where recent claims or pricing history
  justifies it; and (4) **for the provision pour aléas financiers, estimating the future rate of
  return of the assets backing technical commitments** — the ACPR "autorise à retenir ce taux si
  elle considère que son estimation repose sur des" sufficient information and a reliable and
  prudent method. This is the hook by which a French insurer's PAF becomes a forward-looking,
  supervisor-approved calculation rather than a mechanical one.
- Products: AVE, EC, PER, RV.

---

## 3. Supervision and macroprudential powers

### R10. Code monétaire et financier, art. L. 612-1 — the ACPR
- Publisher: Légifrance
- Doc type: legislative code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048029779/2023-09-01
- Retrieved: **YES** (version 1 September 2023 – 18 October 2024)
- Content: verified — the **Autorité de contrôle prudentiel et de résolution (ACPR)** pursues two
  objectives: preserving the stability of the financial system and protecting the clients,
  *assurés*, *adhérents* and beneficiaries of the entities it supervises. It monitors compliance
  with EU law, the Code monétaire et financier, the **Code des assurances**, the Code de la
  sécurité sociale, consumer protection law and professional conduct codes; it examines
  authorisation applications, exercises permanent off-site and on-site supervision, checks
  solvency and liquidity requirements and customer-protection measures, and runs banking and
  insurance crisis prevention and resolution. It holds control powers, administrative police
  powers and sanctioning powers; its *collège de résolution* is France's national resolution
  authority.
- Products: all nine.

### R11. ACPR — *Analyses et Synthèses* on the life market
- Publisher: ACPR / Banque de France
- Doc type: statistical study series
- URLs:
  - n° 180, "Revalorisation 2025 des contrats d'assurance-vie et de capitalisation" (19 pp.,
    PDF creation date 30 June 2026) —
    https://acpr.banque-france.fr/system/files/2026-06/20260630_AS180_revalorisation_2025.pdf
  - n° 179, "L'assurance-vie en 2025" (17 pp., PDF creation date 22 May 2026) —
    https://acpr.banque-france.fr/system/files/2026-05/20260522_AS_Assurance_vie_2025.pdf
  - n° 175, "Revalorisation 2024 des contrats d'assurance-vie et de capitalisation" (19 pp.,
    PDF creation date 4 August 2025) —
    https://acpr.banque-france.fr/system/files/2025-08/20250804_AS175_Revalorisation_contrats_assurance_vie_2024.pdf
  - landing pages —
    https://acpr.banque-france.fr/fr/publications-et-statistiques/publications/ndeg-179-lassurance-vie-en-2025
    and
    https://acpr.banque-france.fr/fr/publications-et-statistiques/publications/ndeg-180-revalorisation-2025-des-contrats-dassurance-vie-et-de-capitalisation
- Retrieved: **YES** — all three PDFs and both landing pages, with **`curl`** (HTTP 200,
  `application/pdf`, 1 062 381 / 1 985 804 / 1 193 221 bytes), text extracted locally with
  PyMuPDF. The host 403s the plain fetcher used for the rest of this sweep but serves `curl`
  identically with and without a browser User-Agent; see the correction in the header.
  **URL correction:** the path previously recorded for n° 179
  (`/system/files/2026-03/20260326_AS_Assurance_vie_2025.pdf`) does not exist and returns 403 —
  this host answers a wrong `/system/files/` path with 403 rather than 404. The working path
  above is the one the n° 179 landing page itself links to.
  **Caveat on n° 175:** its page headers carry an **"ACPR-RESTREINT"** marking although it is
  served from the ACPR's public publications area. Nothing below rests on it alone — n° 180
  restates every 2024 comparative used here.
- Content: verified, read directly. **Scope of n° 180** — study by Jean-Luc Coron with Frédéric
  Ahado, covering **116 organismes and 36 053 versions de contrats** (58 under the Code des
  assurances of which 14 bancassureurs, 24 mutuelles, 18 ORPS, 16 under the Code de la sécurité
  sociale); unit-linked supports are outside its scope except for one dedicated box. The
  contract perimeter is the art. A. 344-2 categories 1, 2, 4 and 5 (individual) and 7, 11, 12
  and 14 (collective); category 3 (assurance en cas de décès, including obsèques) and
  categories 8–9 (unit-linked) are excluded.
  - **Definitions the series fixes** (encadré 1). *Taux de revalorisation* = the rate made of the
    contract's "*rendement garanti et de la participation aux bénéfices techniques et
    financiers*" as defined at arts. **L. 132-22 and A. 132-7** of the Code des assurances —
    **gross of the technical rate and of tax and social levies, but net of the chargement sur
    encours**. *Taux technique* = the maximum rate at which the insurer's commitments are
    discounted, no charges applied, fixed at subscription and limited by **A. 132-1** [R17]; the
    rate served may not fall below it. *Taux de chargement* = chargements de gestion paid by the
    policyholder over average mathematical provisions. All rates are weighted by the average of
    opening and closing mathematical provisions.
  - **Euro-support mathematical provisions**: individual contracts **€1 207 bn end-2025**
    (€1 178 bn end-2024, **+2.5 %**); collective **€154 bn** (€147 bn, **+4.7 %**).
  - **Average taux de revalorisation**: individual **2.63 % in 2025**, unchanged on 2024;
    collective **2.64 %** (2.53 % in 2024, +11 bp). Category 4 carries the individual average —
    about **92 %** of individual euro encours (category 1 4 %, category 5 4 %).
  - **Dispersion between undertakings** (individual): those representing **50 % of encours**
    credited between **2.3 % and 2.9 %** in 2025 — a 0.6-point band, narrower than the
    2.2 %–3.0 % (0.8-point) band of 2024. Quartile series 2020–2025, 1st quartile / mean /
    3rd quartile: 0.9 / 1.3 / 1.4, 0.9 / 1.3 / 1.4, 1.5 / 1.9 / 2.2, 2.2 / 2.6 / 3.0,
    2.2 / 2.6 / 3.0, **2.3 / 2.6 / 2.9**. Collective: 50 % of encours between **2.1 % and 3.1 %**.
  - **Dispersion inside one undertaking** — the figure a model of policyholder heterogeneity
    actually needs. Measured between homogeneous contract groups (90th vs 10th percentile by
    mathematical provisions), the encours-weighted market average gap is **0.99 point in 2025**
    (0.77 in 2024), and the least-revalued group sits **0.39 point below the insurer's mean**
    (0.40 in 2024). The ACPR states outright that a policyholder receiving none of the
    commercial bonuses is credited **at least that 0.39 point below the 2.63 % average**.
    UC-holding bonuses are "*souvent de 100 points de base, et allant jusqu'à plus de 200 points
    de base*".
  - **By type of undertaking** (individual, 2025): **bancassureurs 2.70 %** on **65 %** of
    encours; **assureurs traditionnels 2.48 %** on 30 %; **mutuelles 3.17 %** on 2 %;
    **ORPS 2.39 %** on 3 %. Collective: bancassureurs highest at **2.79 %**, assureurs
    traditionnels and ORPS **2.62 %** each; ORPS hold **52 %** of collective encours.
  - **Asset side**: the *taux de rendement de l'actif* (TRA, financial income net of financial
    charges over net book value, 16 largest life insurers) was **2.1 / 2.2 / 2.0 / 2.2 / 2.5 /
    2.8 %** for 2020–2025; half of undertakings sit between **2.4 % and 3.3 %** in 2025.
    **Bonds are about 60 % of life insurers' and ORPS' investments**, and about **60 % of
    fixed-coupon bonds maturing within four years carry a coupon below 3 %** — the reinvestment
    tailwind that funded the 2025 rate.
  - **PPB as a percentage of life provisions** — the calibration anchor for a PPB buffer.
    Individual contracts: **5.1 / 5.4 / 5.4 / 4.9 / 4.3 / 4.0 %** for 2020–2025. Collective:
    **2.3 / 2.6 / 2.6 / 2.0 / 1.9 / 2.0 %**. End-2025 by type: bancassureurs **4.2 %**
    (4.6 % in 2024) and assureurs traditionnels **3.6 %** (3.5 %) — the bancassureurs released,
    the traditional insurers added. The stock has fallen every year since 2022.
  - **The 85 % rule, restated by the supervisor** (n° 180, footnote 12): "*Les dispositions du
    Code des assurances (article A. 132-10 et suivants) prévoient que seulement 85 % du compte
    financier … lui est destiné pour sa revalorisation, directement ou par l'intermédiaire de la
    PPB. Certains contrats peuvent contractuellement prévoir un pourcentage plus élevé.*"
    Confirms [R15] and confirms that a contractual uplift above 85 % is a real market feature.
  - **Taux technique moyen** (n° 180, tableau 1), weighted by mathematical provisions:
    individual **0.39 / 0.37 / 0.36 / 0.37 / 0.35 / 0.32 %** for 2020–2025; collective
    **1.24 / 1.21 / 1.12 / 1.04 / 1.01 / 0.98 %**. By type in 2025: assureurs traditionnels
    0.39 %, bancassureurs 0.25 %. The ACPR states that "*l'essentiel des contrats actuellement
    commercialisés en France a un taux technique faible ou nul*".
  - **Taux de chargement sur encours** (n° 180, tableaux 2–3): individual **0.63 % in 2025**
    (0.62 % in 2024) — assureurs traditionnels 0.64 %, bancassureurs 0.63 %; collective
    **0.47 %** (0.42 %) — bancassureurs 0.58 %, ORPS 0.42 %. Individual and collective together,
    **half of all undertakings charge between 0.5 % and 0.8 %**, and that quartile band has not
    moved since 2020.
  - **Market context 2025**: 10-year OAT **3.4 %** on annual average (3.0 % in 2024), Livret A
    **2.2 %** (3.1 %), inflation **+0.9 %** (+2.0 %).
  - **Smoothing, quantified** (n° 180, encadré 2, summarising *Débats économiques et financiers*
    n° 50, "Mutualisation intercohortes des risques dans les contrats d'assurance-vie en euros en
    France"): over **1999–2023** the collective reserves **divide the volatility of credited
    rates by five** relative to financial markets and **redistribute about 1.6 % of encours a
    year** between cohorts; contracts held 2006–2011 gained an extra **1.6 % a year**, those
    held 2012–2021 contributed **2.3 % a year** to building the reserves.
  - **Unit-linked, from n° 180's encadré 3**: UC encours **€612 bn end-2025** against €343 bn
    end-2016, capital-guaranteed contracts **€1 361 bn**; UC asset mix equities 32 %, allocation
    funds 17 %, bonds 12 %, structured equity products held directly 10 %, money market 5 %,
    real estate 4 %.
  - **Flows, from n° 179** (study by Jean-Luc Coron and Céline Yang, on the ACPR's weekly and
    quarterly flow collection from about 90 undertakings, about 70 for life): 2025 premiums
    **€159.1 bn**, benefits **€115.1 bn** of which surrenders **€71.0 bn** and death/maturity
    claims **€44.1 bn**; **net inflow €44.0 bn**, the highest since the series began in 2011 and
    **+93.1 %** on the 2024 peak of €22.8 bn, on premiums **+12.2 %** and surrenders **−6.3 %**.
    By support: euro **+€6.4 bn**, positive again **after five consecutive years of net
    outflow**; UC **+€37.6 bn** (85 % of the total). Non-surrenderable (mostly retirement)
    contracts **+€8.8 bn**, of which PER **+€12.8 bn** against **−€3.9 bn** on other
    non-surrenderable contracts. Assurance vie and retirement savings are **32.9 %** of French
    households' financial wealth, **€2 153.5 bn**.
  - **Two vintages of the same 2025 rate, both recorded.** n° 179 (May 2026) gives a
    **preliminary estimate of 2.65 %** for the 2025 euro revaluation, net of charges on encours
    and before social levies; n° 180 (June 2026) gives the **definitive 2.63 %** for individual
    contracts on the full 116-undertaking collection. Cite **2.63 %** for the individual euro
    average; the 2.65 % is the earlier flow-based estimate, not a different concept.
  - **2024 comparatives from n° 175**, consistent with n° 180's restatement: individual
    **2.63 %** (2.60 % in 2023), collective **2.53 %**; PPB **4.3 %** of life provisions for
    individual contracts end-2024 against **4.9 % end-2023**; taux technique 0.35 % / 1.01 %;
    taux de chargement 0.62 % / 0.42 %; euro-support PM €1 178 bn / €147 bn.
  - **What is still not in this series, and stays `**[std]**`**: any *named insurer's* crediting
    rate, TMG or charge scale; the per-contract distribution behind the 0.99-point within-insurer
    gap; and any insurer's PPB target ratio or release policy. The market **average and
    dispersion** are now sourced here and no longer need a `[std]` tag — an frlib euro-fund
    crediting rate calibrated to 2.63 % with a ±0.3-point spread can cite this entry directly.
- Products: AVE, AVUC, EC, PER.

### R12. ACPR — Recommandation 2024-R-03 du 21 novembre 2024 (devoir de conseil)
- Publisher: ACPR
- Doc type: supervisory recommendation (9 pp., PDF creation date 12 December 2024)
- URL: https://acpr.banque-france.fr/system/files/2024-12/20241022_recommandation_2024-R-03_0.pdf
- Retrieved: **YES** — with **`curl`** (HTTP 200, `application/pdf`, 895 713 bytes), text
  extracted locally with PyMuPDF. The URL above, already on file, is correct and always was; it
  is the plain fetcher used for the rest of this sweep that this host refuses, not the URL that
  was wrong. See the correction in the header.
- Content: verified, read in full. Full title: *Recommandation 2024-R-03 du 21 novembre 2024 sur
  le recueil des informations relatives au client pour l'exercice du devoir de conseil et la
  fourniture d'un service de recommandation personnalisée en assurance*. Issued under
  **arts. L. 612-1 II 3° and L. 612-29-1 al. 2 of the Code monétaire et financier**.
  - **Application date, now verified.** Closing line: "*La présente recommandation remplace la
    recommandation 2013-R-01 du 8 janvier 2013, modifiée le 21 février 2020, à compter du
    31 décembre 2025.*" The previously `[unverified]` **31 December 2025** date is correct, and
    the text it replaces is named.
  - **Scope (§ 1), now verified and wider than the earlier summary said.** Addressed to all
    distributors under **art. L. 511-1 III** of the Code des assurances, *including* those acting
    in France under freedom of services or of establishment. It covers **all insurance products,
    group or individual**, and excludes: **grands risques** (art. L. 111-6); **contrats
    collectifs à adhésion obligatoire** and all contracts taken out by employers for employees
    and former employees; products no longer distributed and without tacit renewal; and
    capitalisation and assurance-vie contracts carrying a surrender or transfer value that no
    longer accept versements or arbitrages. It continues and completes **Recommandation
    2024-R-01 du 28 juin 2024** on the DDA (directive (UE) 2016/97), and yields to
    product-specific recommendations.
  - **What must be collected for a euro/UC savings contract** (§ 2.1.3, detailed in Annexe 1):
    family and professional situation — explicitly because it is needed to help draft the
    **clause bénéficiaire**; financial situation sufficient to assess the **capacity to bear
    losses** and the size of the projected investment; **knowledge and experience** in financial
    matters; and the **objectives and investment horizon(s)**. The risk profile must be set
    objectively (§ 2.1.3.6), illustrated with scenarios of how the savings could move, not
    overstated against the stated needs, and **not** determined from knowledge and experience
    alone. Sustainability preferences must be collected under **art. L. 522-5** of the Code des
    assurances, as defined at **art. 2 § 4 of délégué (UE) 2017/2359**, taking account of the
    **EIOPA** guidance on integrating them into the suitability assessment (§ 2.1.3.7).
  - **Point-of-sale disclosures a savings model should assume are made** (§ 2.1.8): the reasons
    for the recommendation; a clear and balanced explanation of the contract and every
    recommended investment option; **all charges on the contract and on the underlying options
    and their effect on past performance** (§ 2.1.8.4); the **tax consequences of a surrender
    within eight years** of the contract taking effect and of premiums paid **after the
    subscriber's 70th birthday** (§ 2.1.8.5) — i.e. the supervisor treats the eight-year and
    age-70 tax boundaries [R40][R41] as sales-critical; and, for a **PER**, the illiquidity of
    the savings, the exhaustive early-release routes, the rente-versus-capital exit options and
    their tax treatment, and the right to change investment profile, management mode or the
    minimum securitisation rhythm under **art. D. 224-3 CMF** (§§ 2.1.8.8–2.1.8.10).
  - **The one clause with a modelling-adjacent number** (§ 2.3.1). For every capitalisation or
    assurance-vie contract with a surrender or transfer value, where there has been **no
    operation for 4 years** — or **2 years** where a personalised recommendation service was
    provided — the distributor should contact the holder and refresh all the collected
    information. **The first observation window opens 24 October 2024**, so the first contact
    falls due **at the latest on 23 October 2028**, or **23 October 2026** where a personalised
    recommendation service was given. Contracts with only *programmed* operations
    (art. A. 522-2) count as dormant for this purpose.
  - **Materiality thresholds for a "significant" operation** (footnote 25, quoting
    **art. A. 522-2** of the Code des assurances): a versement or arbitrage **≥ €2 500 and
    ≥ 20 % of the contract's encours** where encours is **below €100 000**; **≥ €30 000 and
    ≥ 25 %** where encours is **≥ €100 000**. These are the statutory sizes at which advice
    duties re-trigger on a top-up or a switch.
  - **Surrender and switch conduct** (§§ 2.3.2–2.3.5): on an arbitrage or versement into a
    unit-linked support of the kind described in the last sentence of the second paragraph of
    **art. L. 132-5-4** (collective vehicles mainly invested in unlisted assets, PEA-PME-eligible
    securities or sociétés de capital-risque), warn on the variable value and on any **indemnity
    reducing the surrender or transfer value under art. R. 132-5-3**; on a surrender touching
    such a support, advise excluding it from the operation; on a surrender of a UC carrying a
    capital guarantee at a holding term, warn that surrendering early forfeits the guarantee; on
    a surrender within eight years, state the tax consequences. Where a surrender is paired with
    a new subscription (§ 2.3.4), the distributor should set out the comparison explicitly —
    the ACPR names "*engagements de taux, table de référence du contrat, impact de
    l'antériorité fiscale du contrat faisant l'objet du rachat*", which is a supervisory
    acknowledgement that a legacy guaranteed rate and a legacy mortality table have economic
    value to the policyholder.
  - **Advice must not delay the operation** (§ 2.3.8): the formalisation of advice may never push
    an operation past the regulatory settlement or valuation deadlines — for a surrender, the
    two-month cap of art. L. 132-21 [R31] survives the advice duty intact.
  - **Modelling relevance**: none of this changes a cash flow directly; it shapes the sales
    process and it is the current conduct overlay on top of the abrogated art. L. 132-27-1 [R32].
    The 4-year / 2-year re-contact cycle and the A. 522-2 materiality thresholds are the closest
    it comes to a lapse or arbitrage assumption, and neither is a rate.
  - **Still unverified.** A joint ACPR/AMF text on customers' sustainability preferences reported
    for **13 November 2025** remains **[unverified]** — this recommendation does not mention it
    (it points to the **EIOPA** guidance, not to a joint national text), and no such document was
    retrieved here.
- Products: AVE, AVUC, EC, PER, DEP (the advised-sale products).

### R13. Loi Sapin 2, art. 49 → Code monétaire et financier, art. L. 631-2-1 (HCSF)
- Publisher: Légifrance
- Doc type: legislative code article (inserted by loi n° 2016-1691 du 9 décembre 2016, art. 49)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034386882
- Retrieved: **YES** (version dated **8 April 2017**)
- Content: verified — the **Haut Conseil de stabilité financière (HCSF)** defines macroprudential
  policy and holds seven powers. Power **5° ter** lets it, **on a proposal of the Governor of the
  Banque de France (chair of the ACPR)** and to prevent a "serious and characterised threat" to
  financial stability, take temporary protective measures against insurance undertakings:
  limit the acceptance of premiums; restrict the disposal of assets; **limit the payment of
  surrender values**; **defer or restrict arbitrages and advances** on contracts; restrict
  dividends to shareholders or distributions to mutual members. Duration: **a maximum of three
  months, renewable** if the conditions persist (after consulting the advisory committee), with
  the restriction on surrender values capped at **six consecutive months**. The HCSF must
  balance financial stability against the interests of policyholders and members; its decisions
  are challengeable before the Conseil d'État. The mechanism has never been triggered
  **[unverified]** — not stated in the article.
- Products: AVE, AVUC, EC, PER (surrenderable savings contracts). Load-bearing for any lapse or
  mass-surrender stress test.

---

## 4. Participation aux bénéfices

**Read this before citing anything in this section.** The rule is commonly mis-stated as
"85 % of the technical result and 90 % of the financial result". Verified against Légifrance,
it is the other way round and is not a clean 90 %: the *compte de participation aux résultats*
is credited with **85 % of the balance of the compte financier** and with the balance of the
*compte technique* **less the insurer's own share**, that share being the **greater of 10 % of
the credit balance and 4.5 % of annual premiums** [R15]. So the policyholder share of a
technical credit balance is *at most* 90 %, and can be materially less on a small technical
result relative to premium.

### R14. Code des assurances, art. L. 331-3 — the statutory obligation to share profits
- Publisher: Légifrance
- Doc type: legislative code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006798728/
- Retrieved: **YES** — but the version served runs **1 July 1994 to 1 January 2016** (transferred
  by loi n° 94-5 du 4 janvier 1994, art. 5).
- Content: verified text — "*Les entreprises d'assurance sur la vie ou de capitalisation doivent
  faire participer les assurés aux bénéfices techniques et financiers qu'elles réalisent, dans
  les conditions fixées par arrêté du ministre de l'économie et des finances.*" That is the whole
  of the primary obligation: the legislature mandates the sharing and delegates the mechanics to
  an arrêté, which is what arts. A. 132-10 to A. 132-17 [R15][R16] are. Case law and
  parliamentary answers hold that no category of contract is carved out of the obligation
  *a priori*.
  **Caveat**: the displayed version ends 1 January 2016, which is the date the Solvency II
  recodification took effect. Whether the obligation still sits at L. 331-3 or has moved to a
  Livre I article could **not** be confirmed here and is **[unverified]**; product documents
  should cite this entry for the *substance* and not assert a current article number.
- Products: AVE, EC, PER, RV, TD, ADE, OBS, DEP (life and capitalisation generally).

### R15. Code des assurances, arts. A. 132-10 to A. 132-15 — the compte de participation aux résultats
- Publisher: Légifrance
- Doc type: arrêté-level code articles (formerly A. 331-4 to A. 331-8, renumbered effective
  1 January 2016)
- URLs:
  - section index (A. 132-10 to A. 132-17) —
    https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000031738019/
  - A. 132-10 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514666
  - A. 132-11 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038714192/2019-07-01
  - A. 132-12 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031772866
  - A. 132-14 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049818224
  - A. 132-15 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031757226
- Retrieved: **YES** for all six URLs.
- Content: verified, article by article.
  - **A. 132-10** (version 7 September 2017): the minimum PB applies to life undertakings under
    art. L. 310-1 and to *fonds de retraite professionnelle supplémentaire* under art. L. 381-1,
    for individual and collective contracts of every kind; it is determined **globally**, not
    contract by contract; *contrats à capital variable* (unit-linked) are excluded from the
    A. 132-11 to A. 132-15 machinery; references to *provision mathématique* take the Livre III
    Titre IV meaning.
  - **A. 132-11** (version 1 July 2019): the *compte de participation aux résultats* is credited
    with the balance of a **compte technique** less "*la participation de l'assureur aux
    bénéfices de la gestion technique, qui est constituée par le montant le plus élevé entre
    10 % du solde créditeur*" and **4,5 % des primes annuelles**; and with a share of investment
    income "*égale à 85 % du solde d'un compte financier*" whose components are set by
    art. A. 132-13. The article is structured in four parts (general operations; operations with
    a *comptabilité auxiliaire d'affectation*; supplementary pension schemes; category-12
    commitments). Reinsurance enters via art. A. 132-15.
  - **A. 132-12** (in force since 1 January 2016, modified by the arrêté du 28 décembre 2015):
    the **minimum annual PB** is the credit balance of the A. 132-11 account; the minimum amount
    of benefits is that figure less interest credited to mathematical provisions, plus, where
    relevant, an amount reflecting the gap between guaranteed rates and the average rate served
    in the year. Contracts under art. L. 134-1 (eurocroissance) are **excluded**.
  - **A. 132-14** (version 24 October 2024): the financial result credited to the account is the
    product of average technical provisions net of reinsurance cessions for the relevant
    categories and a **taux de rendement des placements**, plus net financial income on assets
    transferred with a portfolio divided by (1 − the ceding undertaking's retained unrealised
    gains ratio). The investment return rate is net investment income on life operations over
    average investments held in the year, computed separately for the three categories of
    commitment identified in A. 132-11.
  - **A. 132-15** (in force since 1 January 2016): a **solde de réassurance cédée** line enters
    the account — for pure risk reinsurance, the difference between claims borne by reinsurers
    and premiums ceded; for mixed treaties, the risk element must be isolated.
- Products: AVE (primary), EC, PER, RV, TD, ADE, OBS, DEP. Not AVUC for the A. 132-11 machinery
  (unit-linked contracts are excluded), though a multisupport contract's euro compartment is in
  scope.

### R16. Code des assurances, arts. A. 132-16 and A. 132-16-1 — the eight-year rule and the exceptional reprise
- Publisher: Légifrance
- Doc type: arrêté-level code articles (formerly A. 331-9)
- URLs:
  - A. 132-16 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801820
  - A. 132-16-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042611504
- Retrieved: **YES** (A. 132-16 version 1 January 2020; A. 132-16-1 version 5 December 2020)
- Content: verified.
  - **A. 132-16**: sums entered into the *provision pour participation aux bénéfices* must be
    allocated to the *provision mathématique* or paid to policyholders "*au cours des huit
    exercices suivant*" the year in which they were credited — the **eight-year rule** that makes
    the PPB a smoothing buffer with a hard release horizon. Exceptions: for *fonds de retraite
    professionnelle supplémentaire* and for commitments under a *comptabilité auxiliaire
    d'affectation* per art. L. 142-4, the maximum is **fifteen years**.
  - **A. 132-16-1**: an **exceptional reprise** of the PPB is possible only where, cumulatively,
    the life technical account showed a **negative balance in the last financial year** *and* the
    solvency capital requirement (or minimum margin requirement) is **no longer covered**. It
    requires an ACPR-approved recovery plan providing for **restitution out of subsequent results
    within a maximum of eight years** and prohibiting dividends, redemption of certificates or
    other distributions until the amounts taken back are restored.
- Products: AVE (primary), EC, PER, RV. The eight-year rule is the single most modelling-relevant
  French discretionary-benefit constraint.

---

## 5. Guaranteed and technical interest rates

### R17. Code des assurances, arts. A. 132-1 and A. 132-1-1 — taux d'intérêt technique maximal
- Publisher: Légifrance
- Doc type: arrêté-level code articles
- URLs:
  - A. 132-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514601
  - A. 132-1-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801948
- Retrieved: **YES** (A. 132-1 in force since **7 September 2017**; A. 132-1-1 version
  **1 January 2020**)
- Content: verified.
  - **A. 132-1**: tariffs must be built on a rate at most equal to **75 % of the average rate of
    French State borrowings (taux moyen des emprunts d'État, TME) computed on a semi-annual
    basis**, without exceeding, **beyond eight years**, the lower of **3.5 %** and **60 % of that
    average rate**. For contracts with **periodic premiums** or **variable capital**, whatever
    their duration, the rate cannot exceed the lower of **3.5 %** and **60 %** of the same
    average. For contracts denominated in a foreign currency the reference is that country's
    long-term State borrowing rate, on the same basis. Rates in force at subscription apply;
    non-scheduled contributions are re-tested at each payment. The article does not apply to
    collective insurance operations.
  - **A. 132-1-1**: the **taux de référence** is the arithmetic mean over the last six months of
    rates observed on the primary and secondary markets for State borrowings on a semi-annual
    basis, multiplied by **60 %** or **75 %** as the case requires; that product is the *monthly
    reference rate*. The maximum technical rate moves on a **0.25-point grid floored at zero**,
    and does **not** change while the monthly reference rate has not fallen by at least
    **0.10 point** or risen by at least **0.35 point** relative to the rate in force; when a
    threshold is crossed the new maximum is the grid rate immediately below the reference rate.
    Undertakings have **three months** to implement a change.
- Products: AVE, EC, PER, RV, TD, OBS, DEP (any contract with a guaranteed technical rate; RV and
  DEP most materially, since annuity pricing capitalises the rate over decades).

### R18. Code des assurances, arts. A. 132-2 and A. 132-3 — taux minimum garanti (TMG)
- Publisher: Légifrance
- Doc type: arrêté-level code articles
- URLs:
  - A. 132-2 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514622
  - A. 132-3 (current) — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514611
  - A. 132-3 (version 2 May 2007 – 1 August 2010) —
    https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006786141/2007-05-02
- Retrieved: **YES** for all three (A. 132-2 and current A. 132-3 both dated **7 September 2017**).
- Content: verified.
  - **A. 132-2**: undertakings and FRPS may "*garantir dans leurs contrats un montant total
    d'intérêts techniques et de participations aux bénéfices qui, rapporté à la fraction des
    provisions mathématiques desdits contrats sur laquelle prend effet la garantie, ne sera pas
    inférieur à des taux minima garantis*" fixed under A. 132-3. Note the construction: what is
    guaranteed is **technical interest *plus* PB**, expressed as a rate on the mathematical
    provision — the TMG is not a separate credit on top of the technical rate.
  - **A. 132-3 I** (current): for a given financial year, the **total guaranteed PB** under
    A. 132-2 must be below a ceiling computed as the positive difference between "*80 % du
    produit de la moyenne des taux de rendement des actifs*" and (the second limb of the
    subtraction was not fully extracted from the fetched page — recorded as incomplete).
  - **A. 132-3 II**: guaranteed rates are **expressed on an annual basis** and fixed for a
    continuous period of **at least six months and at most the period from the effective date of
    the guarantee to the end of the following financial year** (so, in practice, up to about
    eighteen months).
  - **A. 132-3 III**: guaranteed rates under II may not exceed the **minimum of (a) 150 % of the
    maximum technical rate defined at A. 132-1/A. 132-1-1 by reference to 75 % of the TME at the
    effective date of the guarantee** and (b) **the higher of 120 % of that maximum technical
    rate and 110 % of the average rates served to policyholders over the two preceding financial
    years** — limb (b) is recorded from the fetched page's structured summary rather than from a
    verbatim quote, and should be re-read before being relied on for a live pricing decision.
  - **A. 132-3 IV**: by derogation from I and III, a newly licensed undertaking may, until the
    close of the **second financial year after authorisation**, offer rates not exceeding
    **120 % of the maximum technical rate** on the 75 %-TME reference.
  - Historic comparison (version 2 May 2007 – 1 August 2010): the older text framed the cap
    differently — a minimum rate could be fixed annually for the following year not exceeding
    **85 % of the average asset yield rates over the two preceding financial years**, with the
    guarantee limited to **eight years**, and a new contract offering such a guarantee required
    the undertaking's two-year average asset yield to be at least **4/3 of the first-year
    minimum rate**. Anyone citing "85 % of the average asset yield" for a TMG is citing this
    superseded text.
- Products: AVE (primary), EC, PER, RV, OBS, DEP.

---

## 6. Eurocroissance and the provision de diversification

### R19. Code des assurances, art. L. 134-1 and arts. R. 134-1 to R. 134-12
- Publisher: Légifrance
- Doc type: legislative + regulatory code articles
- URLs:
  - L. 134-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611220
  - chapter R. 134-1 to R. 134-12 — https://www.legifrance.gouv.fr/codes/id/LEGISCTA000039739657
  - R. 134-4 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739643
- Retrieved: **YES** (L. 134-1 version **24 May 2019**; R. 134-4 version **1 January 2020**)
- Content: verified.
  - **L. 134-1**: life undertakings may write commitments in case of life or death — **excluding
    temporary death cover** — which give rise to a **provision de diversification** intended to
    absorb fluctuations of the backing assets. The guaranteed benefit may be a **rente** or a
    **capital at maturity**, on conditions set by decree. Two contractual shapes are permitted:
    the benefit expressed partly in euros and partly in units of the provision de
    diversification; or expressed **solely in units of the provision before maturity, with a
    euro-denominated guarantee at maturity**. A premium under a life contract may accordingly
    give rise to three kinds of engagement — **en euros**, **en unités de compte**, and **donnant
    lieu à constitution d'une provision de diversification** — which is the legal basis for a
    three-compartment multisupport contract.
  - **Chapter R. 134-1 to R. 134-12**: R. 134-1 capital guarantee limits and the minimum value of
    the provision; R. 134-2 individualisation of rights in *parts de provision de
    diversification* (number of units = total provision divided by a common per-unit value);
    R. 134-3 permitted deductions; R. 134-4 the participation account; R. 134-5 surrender and
    transfer value, which fixes that the relevant duration "**cannot exceed the shorter of the
    guarantee maturity and eight years**"; R. 134-6 settlement at maturity and conversion into an
    annuity; R. 134-7 supplementary guarantees; R. 134-8 asset valuation in the dedicated
    accounting (realisation value per R. 343-11 and R. 343-12); R. 134-9 classification of
    technical provisions; R. 134-10 pre-sale disclosure; R. 134-11 separate application per
    accounting unit; R. 134-12 asset transfers and reallocation, capped at **10 % of the amount
    of the provision de diversification**.
  - **R. 134-4**: the credit balance of the participation account goes to three destinations —
    revaluing guaranteed benefits, crediting the provision de diversification (new units or a
    higher unit value), and funding the **provision collective de diversification différée**.
    When the account is in deficit that deferred reserve may be drawn down to revalue the
    provision mathématique or the provision de diversification, or the unit value may be reduced
    within limits. No percentages or statutory time limits appear in the article itself.
- Products: EC (primary); AVE/AVUC where a multisupport contract carries a eurocroissance
  compartment.

### R20. Décret n° 2019-1437 du 23 décembre 2019 (eurocroissance reform under loi PACTE)
- Publisher: Légifrance
- Doc type: décret
- URL: https://www.legifrance.gouv.fr/eli/decret/2019/12/23/ECOT1930053D/jo/texte
- Retrieved: **YES**
- Content: verified — the décret implements the loi PACTE eurocroissance reform, replacing
  Chapitre IV of Titre III, Livre I of the Code des assurances. It restates the maturity
  guarantee as the sum of the *provision mathématique* and the value of the holder's share of the
  *provision de diversification*, with a minimum guarantee level set by decree; confirms the
  R. 134-5 rule that the relevant duration cannot exceed the shorter of the guarantee maturity
  and **eight years**; sets out the *provision collective de diversification différée* mechanics
  (revaluation of PM or PD at any time; absorption of debit balances by reprise or by reducing
  the unit value, within limits); and requires that transfers of assets into a *comptabilité
  auxiliaire d'affectation* be matched by reciprocal transfers of equal value valued under
  R. 343-11 and R. 343-12. **Entry into force 1 January 2020**; existing contracts stay under
  the prior rules, and new contracts on the old basis could be written until **1 October 2020**.
  A widely repeated claim that the reform pushed the compulsory restitution of diversification
  provisions from eight to fifteen years appears only in secondary commentary and is
  **[unverified]**.
- Products: EC.

---

## 7. Mortality tables

### R21. Arrêté du 1er août 2006 — homologation of TGH05 / TGF05 (annuity tables)
- Publisher: Légifrance (Journal officiel)
- Doc type: arrêté
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000820127
- Retrieved: **YES**
- Content: verified — the arrêté homologates two **generational annuity tables applicable from
  1 January 2007**: **TGF05** for female lives and **TGH05** for male lives, replacing the
  generational table homologated in 1993. It amends a long list of Code des assurances articles
  including **A. 132-1, A. 132-4, A. 132-6, A. 160-2, A. 160-4, A. 310-1, A. 331-1-1, A. 331-1-2,
  A. 331-9-1, A. 332-7, A. 335-1 and A. 441-4-1**, covering euro conversion, life contract
  provisions, annuity thresholds and mortality-table application. Most provisions took effect on
  publication (**26 August 2006**); article 4 defers the unit-linked and participation
  distribution provisions to **1 January 2007**, aligning with the new tables. The tables apply
  to annuity contracts subscribed **from 1 January 2007**; for older contracts, undertakings had
  to hold minimum reserves on the 1993 table until **1 August 2008**.
- Products: RV (primary), PER (annuity option), DEP (annuity in payment), AVE/EC (annuity
  conversion option).

### R22. Arrêté du 20 décembre 2005 — homologation of TH 00-02 / TF 00-02 (non-annuity tables)
- Publisher: Légifrance (Journal officiel)
- Doc type: arrêté
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000636581
- Retrieved: **YES**
- Content: verified — homologates **TH 00-02** for male insureds and **TF 00-02** for female
  insureds, and carries forward **TD 88-90** and **TV 88-90** from the 1993 arrêté. TH 00-02 and
  TF 00-02 apply to "*contrats autres que de rente viagère*" — everything that is not a life
  annuity. For annuity contracts, undertakings may use homologated tables or their own experience
  data, with specific provisions on anti-selection. For non-annuity life contracts the arrêté
  permits adjusting the insured's age by the **décalage d'âge** (age shift) schedules annexed to
  each table. **In force 1 January 2006**, except the annuity-calculation provisions, in force
  **1 July 2006**.
- Products: TD (primary), ADE (death and PTIA), OBS, AVE (death benefit), DEP (mortality of the
  healthy and dependent lives).

### R23. Code des assurances, art. A. 335-1 and its Annexe — which table applies to what
- Publisher: Légifrance
- Doc type: arrêté-level code article and annexe
- URLs:
  - A. 335-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000026806627
  - Annexe (1) art. A. 335-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019265297
- Retrieved: **YES** for both. Légifrance served the article as version **21 December 2012 to
  1 January 2016** and the annexe as version **26 August 2006 to 1 January 2016** even when a
  current-date URL suffix was supplied; the *current* placement of these provisions after the
  Solvency II recodification is **[unverified]**.
- Content: verified.
  - **A. 335-1**: life and capitalisation tariffs comprise the undertaking's remuneration and are
    built on (i) a **taux d'intérêt technique** fixed per art. A. 132-1 [R17] and (ii) mortality
    tables, of which there are exactly **two permitted kinds**:
    **(a)** tables homologated by ministerial arrêté, **by sex**, established on insured
    populations for annuity contracts and on **INSEE** data for other contracts; or
    **(b)** tables established by the undertaking itself and **certified by an actuary
    independent of that undertaking, approved for the purpose by one of the actuarial
    associations recognised by the supervisor** — the *tables d'expérience*. Experience tables
    must be built on the undertaking's own experience data or on demographically equivalent
    experience data.
    Additional rules: where a homologated table is used as a single table for all insureds, it
    must be the sex-appropriate table producing the **most prudent** rate; for non-annuity
    survival contracts the homologated tables are applied with the annexed **age shifts**; for
    annuity contracts, **rates computed on experience tables may not be lower than those from the
    appropriate homologated tables by sex** (an explicit floor); for collective annually
    renewable death contracts a *forfait* method may be used if justifiable.
  - **Annexe**: contains **TF 00-02** (female, ages 0–112, tabulated as $l_x$, "nombre de vivants
    à l'âge x"), **TH 00-02** (male, ages 0–112, same form) and **TD 88-90** (ages 0–106),
    together with two **décalage d'âge** schedules — for TF 00-02 running from **−11 years at
    ages 16–32** up to **0 at age 94+**, and for TH 00-02 from **−13 years at ages 16–38** up to
    **−3 at age 75+**.
- Products: all nine. This is the article that makes *tables d'expérience* legal and, in the same
  breath, makes them non-public.

### R24. INSEE — Données nationales : mortalité, espérance de vie
- Publisher: Institut national de la statistique et des études économiques
- Doc type: statistical dataset landing page
- URL: https://www.insee.fr/fr/statistiques/8210111
- Retrieved: **YES** (page publication date **15 July 2024**)
- Content: verified — the page offers, in Excel (.xlsx) files from 24 KB to 451 KB plus a full
  zip archive:
  **T69QMORT** *quotients de mortalité pour 100 000 survivants à l'âge indiqué*;
  **T69SUR** survivors at each age per 100 000 live births;
  **T69ESP** *espérance de vie par âge détaillé*;
  **T67** mortality rates by sex and age group; **T68** triennial tables; **T70** infant
  mortality. Annual series run from **1946 for metropolitan France and 1994 for France as a
  whole**; the triennial tables from **1977** and **1999** respectively. The page does not state
  licence or reuse conditions; standard INSEE open-data terms are assumed and that assumption is
  **[unverified]**.
  This is the **only freely redistributable French mortality series**. The frlib decrement CSVs
  are `**[std]**` proxies built from this series, anchored so that each product's
  best-estimate factor reproduces its own technical-notes placeholder exactly — TH 00-02 /
  TF 00-02 / TGH05 / TGF05 are cited by name and article [R21][R22][R23] but never shipped.
- Products: all nine.

---

## 8. Morbidity, dependency and population data

### R25. DREES — *Études et Résultats* n° 1327, février 2025 (APA over the retirement lifetime)
- Publisher: Direction de la recherche, des études, de l'évaluation et des statistiques
- Doc type: statistical study (7 pp.), author Patrick Aubert (Institut des politiques publiques)
- URL: https://drees.solidarites-sante.gouv.fr/sites/default/files/2025-02/ER%201327%20EDRAPA_MEL.pdf
- Retrieved: **YES** (PDF downloaded, full text extracted)
- Content: verified — built on the 2016 *échantillon interrégimes de retraités* matched to 2017
  APA/ASH individual records, on 2017 mortality and take-up conditions. Headline results:
  a retiree can expect **25.1 years** of retirement, of which **2.4 years** receiving the
  *allocation personnalisée d'autonomie* (**9.6–10 %** of the retirement period); **3.3 years and
  12 %** for women, **1.4 years and 6 %** for men. **57 % of retirees would receive APA at some
  point (69 % of women, 44 % of men)**; separately **47 % of women and 29 % of men** for APA at
  home and **46 % and 24 %** in an institution. Among beneficiaries, expected APA duration is
  about **2.9 years for men at home** and **3.2 years (women) / 2.3 years (men) in an
  institution**. Mean age at entry into APA at home ranges from **80.1 years** for men in the
  lowest pension quintile to **86.0 years** in the highest — a **5.9-year** gradient overall and
  **7.5 years** for home APA; the gradient is **3.4 years** among women. GIR is used throughout
  as the dependency scale (GIR 1 most dependent, GIR 6 most autonomous; GIR 1–4 confers
  entitlement).
- Products: DEP (primary), RV and PER (longevity context).

### R26. CNSA — *Les chiffres clés de l'aide à l'autonomie 2024*
- Publisher: Caisse nationale de solidarité pour l'autonomie
- Doc type: statistical yearbook (28 pp., created 20 June 2024)
- URL: https://www.cnsa.fr/sites/default/files/2024-06/PUB-CNSA_Chiffres_cles_2024_Access-01.pdf
- Retrieved: **YES** (PDF downloaded, full text extracted)
- Content: verified — CNSA devotes **€40.6 bn** to *aide à l'autonomie* in 2024. At December 2022
  there were **1.3 million APA beneficiaries**, of which **794 000 at home** and **542 500 in an
  institution**; **7.2 %** of the 60-and-over population (estimated at **18.4 million**) received
  APA at 31 December 2022. **GIR distribution of APA beneficiaries in 2022** (source DREES,
  enquête Aide sociale):
  *at home* — GIR 1 **2 %**, GIR 2 **18 %**, GIR 3 **22 %**, GIR 4 **58 %**;
  *in an institution* — GIR 1 **13 %**, GIR 2 **44 %**, GIR 3 **19 %**, GIR 4 **24 %**.
  **Monthly APA-at-home ceilings for 2024**: GIR 1 **€1 955.60**, GIR 2 **€1 581.44**,
  GIR 3 **€1 143.09**, GIR 4 **€762.87**. Entitlement is assessed on the **grille AGGIR**; only
  GIR 1–4 qualify; the amount depends on GIR, income and the cost of the care plan. Net *aide
  sociale* spending on older people was **€8.2 bn** in 2022. The document also records 3.1 million
  people under 60 living at home reporting at least one severe functional limitation in 2021
  (6.8 % of that age group).
- Products: DEP (primary). The GIR mix and the APA ceilings are the natural anchors for a
  dependency-rente benefit scale.

### R27. DREES — *Études et Résultats* n° 1101, 31 January 2019 (people covered by private insurers, by social risk)
- Publisher: DREES; authors Alexis Montaut and Raphaële Adjerad
- Doc type: statistical study
- URL: https://drees.solidarites-sante.gouv.fr/publications/etudes-et-resultats/premiere-estimation-du-nombre-de-personnes-couvertes-par-les
- Retrieved: **YES** (landing page and abstract)
- Content: verified — first estimate, on **2016** data, of the number of people covered by
  complementary insurers by social risk: **23–30 million** covered for invalidity (0.3–0.4 million
  receiving benefits), **10.4 million** for supplementary retirement (2.2 million receiving), and
  **4.8 million** covered for **dépendance** as a principal protection. In 2016 complementary
  bodies collected **€70 bn** in contributions and paid **€51 bn** of social-risk benefits.
  Multi-coverage materially widens the invalidity estimates.
- Products: DEP, TD, ADE (market sizing and take-up context).

### R28. Institut des actuaires — atelier technique "Assurance dépendance : état des lieux, solutions assurantielles et innovations pour le bien-vieillir" (24 November 2025)
- Publisher: Institut des actuaires (presenters A. Treilhou, S. Ayadi, A. Petit, V. Touzé)
- Doc type: technical workshop deck (37 slides)
- URL: https://www.institutdesactuaires.com/global/gene/link.php?doc_id=20056&fg=1
- Retrieved: **YES** (PDF downloaded, full text extracted)
- Content: verified. **French dependency insurance market, 2024**: **2.4 million people** insured
  against the dependency risk through insurance undertakings (**−6.9 %** on 2023), of which
  contracts where dependency is the *principal* guarantee represent **58 %**; **€618.1 m** of
  premiums (**−3 %**), of which **88 %** on principal-and-only dependency guarantees; for those
  contracts the **average annual premium is €472 individual and €106 collective**, and the
  **average age at subscription is 64**; **€357.3 m** of benefits paid (**+6.3 %**); **€6.4 bn**
  of provisions at 31 December 2024 (**−1.9 %**); **41 900 annuities in payment** on individual
  principal-and-only dependency contracts with an **average monthly annuity of €583**;
  **28 400 new contracts** (**−13.7 %**). Across all bodies, **6.0 million** people were insured
  for the dependency risk in 2024 (**56 % mutuelles, 40 % insurance undertakings, 4 % institutions
  de prévoyance**). Survey findings: roughly **one French person in ten** holds a dependency
  contract, half of them subscribed by the insured themselves; typical annuities are **below
  €500/month**.
  **Product design (OCIRP points-based collective contract, a real market design)**: contributions
  of **0.40 % to 1.50 % of the PMSS** buy *points de rente dépendance*; a minimum guaranteed
  monthly annuity of **€200 to €750** for **total dependency (GIR 1–2)** and **50 % of it, €100 to
  €375**, for **partial dependency (GIR 3)**; a **0.60 % PMSS** compulsory base plus a **0.40 %
  PMSS** optional layer (**€15.70/month in 2025**) raises the GIR 1–2 minimum by €200/month to
  **€500** and the GIR 3 minimum by €100/month to **€250**. Claim recognition: automatic where APA
  is in payment for GIR 1–2; otherwise the state of dependency must be certified by the insurer's
  medical officer, must have lasted **more than three months**, and the insured must be unable to
  perform **2 or 3 of the 4 *actes de la vie courante***. Portability: continued contributions on
  leaving the employer without medical selection at the same tariff **within six months**; no
  reduction value is applied — the guarantee is maintained for life even if contributions stop.
  Pricing: the *valeur d'acquisition* by age requires two series per age — **mortality of the
  generation (healthy and future disabled)** and the **future prevalence of disability in the
  generation**; the scale is sensitive to the technical rate, the revaluation coefficient, the
  loading rate and the guaranteed minimum annuity, and is more rate-sensitive the younger the
  insured. Individual contracts are characterised by **subscription ages between 60 and 75**, no
  medical selection and no guaranteed minimum annuity; collective contracts by younger lives,
  better pooling and lower expenses.
- Products: DEP (primary, and by some distance the densest public source available for it).

---

## 9. Conduct, contract information and distribution

### R29. Code des assurances, arts. L. 132-5-1 and L. 132-5-2 — renonciation
- Publisher: Légifrance
- Doc type: legislative code articles
- URLs:
  - L. 132-5-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731314
  - L. 132-5-2 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731328
- Retrieved: **YES** (both in force since **1 April 2018**)
- Content: verified.
  - **L. 132-5-1**: any natural person who has signed a proposal or a life insurance or
    capitalisation contract may renounce by registered letter or registered electronic mail with
    acknowledgement of receipt, within **thirty full calendar days from the moment they are
    informed that the contract is concluded**. The deadline expires at midnight on the last day
    and is **not** extended if it falls on a weekend or public holiday. The undertaking must repay
    **all sums paid** within **thirty full calendar days of receipt** of the notice. Unrepaid sums
    bear interest automatically at **1.5 × the legal rate for two months**, then at **twice the
    legal rate**. The right does not apply to contracts with a maximum duration of two months.
  - **L. 132-5-2**: before the contract is concluded the insurer must hand over a *note
    d'information*, or the proposal/contract may itself serve as that note where it carries the
    **encadré** [R30] at its head stating the nature of the contract, the fees, the guarantees and
    the availability of surrender. The document must include "*un modèle de rédaction destiné à
    faciliter l'exercice de la faculté de renonciation*". **Sanction**: where the documents are
    not delivered, the renunciation period runs to the thirtieth calendar day after actual
    delivery, **capped at eight years from the date the subscriber is informed the contract is
    concluded**.
- Products: AVE, AVUC, EC, PER, RV, TD, OBS, DEP (ADE follows the consumer-credit regime instead).

### R30. Code des assurances, arts. A. 132-4 and A. 132-8 — note d'information and the *encadré*
- Publisher: Légifrance
- Doc type: arrêté-level code articles
- URLs:
  - A. 132-4 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046824912
  - A. 132-8 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031773778
- Retrieved: **YES** (A. 132-4 version **1 January 2023**, modified by the arrêté du 22 décembre
  2022; A. 132-8 version **1 January 2016**)
- Content: verified.
  - **A. 132-4** (and its annexe) prescribes the **note d'information** in five blocks:
    (1) identification of the contract and the insurer; (2) contract characteristics — definition
    of the guarantees, duration, premium payment arrangements, "*délai et modalités de
    renonciation au contrat*", claims procedure, plus specifics for life, unit-linked and group
    contracts; (3) **guaranteed return and participation aux bénéfices** — guaranteed interest
    rates and their duration, reduction, surrender and transfer values, and the method of
    calculating and allocating PB; (4) complaints handling and any mediation body; (5) reference
    to the SFCR where applicable.
  - **A. 132-8** prescribes the **encadré** at the head of the proposal, draft contract or notice,
    **not exceeding one page**, with eight sections in fixed order: (1) type of contract
    (individual life, group, capitalisation; for group contracts a warning that members' rights
    may be changed by amendment); (2) the guarantees with clause references, capital or annuity,
    whether capital is guaranteed equal to net premiums for euro contracts, and for unit-linked a
    prominent statement that the amounts invested are **not guaranteed and are subject to market
    fluctuations**; (3) participation aux bénéfices and the applicable percentages; (4) surrender
    and transfer availability and the payment period; (5) **fees in four categories** — entry and
    premium charges, recurring annual charges, exit charges, and other charges, with maximum
    amounts or percentages; (6) recommended holding duration, in prescribed wording; (7)
    beneficiary designation; (8) a closing disclaimer that the box only summarises the essentials.
- Products: AVE, AVUC, EC, PER, RV, TD, OBS, DEP.

### R31. Code des assurances, arts. L. 132-21, L. 132-22 and L. 132-23-1 — surrender, annual information, payment on death
- Publisher: Légifrance
- Doc type: legislative code articles
- URLs:
  - L. 132-21 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030461815
  - L. 132-22 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048252743
  - L. 132-23-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611225
- Retrieved: **YES** (L. 132-21 version **1 January 2016**; L. 132-22 version **24 October 2024**;
  L. 132-23-1 version **24 May 2019**)
- Content: verified.
  - **L. 132-21**: the contract must state how the **valeur de rachat**, the **valeur de
    transfert** and the **valeur de réduction** are computed; reduction penalties may not be
    charged directly against the mathematical provision. The insurer may grant **avances** up to
    the surrender value. A requested surrender must be paid within **two months** at most;
    transfers within periods set by decree. Late payment bears interest at **1.5 × the legal rate
    for two months**, then **twice the legal rate**.
  - **L. 132-22**: the annual statement must give the surrender value (or transfer value for
    professional retirement contracts), the reduction value where relevant, guaranteed capital
    amounts, the premium, "*le rendement garanti et la participation aux bénéfices techniques et
    financiers*", the average guaranteed return and PB rates for comparable contracts both open
    and closed to new business, the ESG dimension of the investment policy, the **average asset
    yield for the contract category**, and, for unit-linked, unit values and charges. The insurer
    must **publish on its website, within 90 business days of 31 December**, the average
    guaranteed returns, average charge rates, the **average net return served to policyholders**,
    tax and social-contribution rates, and average PB rates, contract by contract and flagged for
    availability to new business, keeping the information online for at least **five years**.
    Unit-linked and art. L. 134-1 contract information is updated at least **quarterly**; a
    specific statement is due **one month before** a contract's term.
  - **L. 132-23-1**: on being notified of the death and having identified the beneficiary, the
    insurer has **fifteen days** to request the documents needed for payment, and must pay within
    **one month** of receiving the complete file. Overrun of the fifteen-day step triggers
    **twice the legal rate for one month then three times**; overrun of the one-month payment
    deadline triggers **twice the legal rate for two months then three times**; the initial
    fifteen days count toward that two-month calculation. The insurer may not ask twice for the
    same document, and a failure to request a required document does not suspend the payment
    deadline.
- Products: AVE, AVUC, EC, PER, RV, TD, OBS, DEP.

### R32. Devoir de conseil — Code des assurances art. L. 132-27-1 (abrogated) and Directive (UE) 2016/97 (DDA) with its French transposition
- Publisher: Légifrance
- Doc type: legislative code article (historic) + directive landing page
- URLs:
  - L. 132-27-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000020195154/2026-07-01
  - Directive (UE) 2016/97 (Légifrance landing page) —
    https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000031967447
- Retrieved: **YES** for the article (version **1 July 2010 – 1 October 2018**, since abrogated);
  **PARTIAL** for the directive — Légifrance serves only a metadata landing page that points to
  EUR-Lex for the substantive text, and EUR-Lex is blocked [R1].
- Content: verified.
  - **L. 132-27-1** (the pre-DDA French *devoir de conseil*, retained here because it is the text
    most product literature still paraphrases): before concluding an individual life contract with
    surrender values, a capitalisation contract, or before a member joins certain contracts, the
    insurer must specify the requirements and needs expressed by the subscriber, record their
    financial situation and objectives and the reasons motivating the advice given on a particular
    contract, and "*s'enquiert auprès du souscripteur … de ses connaissances et de son expérience
    en matière financière*"; where the customer withholds the information, the insurer must warn
    them before conclusion; the advice must be adapted to the complexity of the contract. It did
    not apply where an intermediary under art. L. 511-1 presented or proposed the contract.
  - **Directive (UE) 2016/97**: verified from the Légifrance landing page — **entry into force
    22 February 2016**, **transposition deadline 23 February 2018**, repealing Directive
    2002/92/CE with effect from 23 February 2018. France transposed it by **ordonnance
    n° 2018-361 du 16 mai 2018** and **décret n° 2018-431 du 1er juin 2018**, in force
    **1 October 2018** (some provisions 23 February 2019). The substantive DDA requirements
    (definition of insurance distribution, the IPID, the demands-and-needs test, the
    appropriateness and suitability tests for insurance-based investment products, remuneration
    and conflicts of interest, and the new Code des assurances Livre V articles L. 521-1 and
    following / L. 522-1 and following) could not be read from a retrieved text and are
    **[unverified]**.
- Products: AVE, AVUC, EC, PER, DEP, TD, OBS (advised sales); ADE via the consumer-credit regime.

### R33. PRIIPs — Règlement (UE) n° 1286/2014 and AMF Position-recommandation DOC-2011-05
- Publisher: European Parliament and Council (EUR-Lex); Autorité des marchés financiers
- Doc type: regulation + national regulator position/recommendation
- URLs:
  - Règlement (UE) 1286/2014 —
    https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32014R1286
  - AMF DOC-2011-05 —
    https://www.amf-france.org/sites/institutionnel/files/private/2023-02/DOC-2011-05_VF14_PRIIPs.pdf
- Retrieved: **NO** for the regulation (EUR-Lex WAF block, as R1); **YES** for the AMF document
  (PDF downloaded, 44 pp., "Document créé le 18 février 2011, modifié le 16 février 2023").
- Content: verified from the AMF document — DOC-2011-05, *Guide des documents réglementaires des
  OPC*, cites as its reference texts **article 78 of Directive 2009/65/CE, Regulation 583/2010,
  Règlement (UE) n° 1286/2014, Règlement délégué (UE) 2017/653** and articles 411-106 to 411-120
  and 422-67 to 422-78 of the AMF General Regulation. It applies to OPCVM, general-purpose
  investment funds, private-equity funds, OPCI, funds of alternative funds, professional funds
  and employee-savings funds, and governs the **DICI** and the **DIC (KID)** for those vehicles —
  naming, investment objective and policy, **risk and reward profile**, **charges**, past
  performance, practical information, and formula funds. Because French unit-linked contracts are
  overwhelmingly wrapped around these same collective vehicles, this document is the operative
  national doctrine on the disclosure attaching to a UC. The **insurance-side** PRIIPs mechanics —
  the SRI 1–7 summary risk indicator, the four performance scenarios, the RIY cost measure and
  the recommended holding period, all set by Règlement délégué (UE) 2017/653 — could not be read
  from a retrieved text and are **[unverified]** here.
- Products: AVUC (primary), EC, PER, AVE (multisupport contracts).

---

## 10. Retirement — the PER

### R34. Loi PACTE art. 71 and Code monétaire et financier arts. L. 224-1 to L. 224-8
- Publisher: Légifrance
- Doc type: statute article + legislative code articles
- URLs:
  - loi n° 2019-486 du 22 mai 2019, art. 71 —
    https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000038496266
  - CMF L. 224-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038507575
  - CMF section L. 224-1 to L. 224-8 —
    https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000038507459/2019-10-23/
- Retrieved: **YES** for all three (L. 224-1 version **1 October 2019**)
- Content: verified.
  - **Art. 71 of the loi PACTE** creates the **plan d'épargne retraite (PER)** as a new Chapitre IV
    of Livre II, Titre II of the Code monétaire et financier, in force at a date fixed by decree
    and **no later than 1 January 2020**.
  - **L. 224-1**: individuals may pay sums into a PER whose object is the acquisition and
    enjoyment of **personal lifetime rights** or the payment of a **capital**, payable from the
    date the holder liquidates a compulsory old-age pension (or reaches the statutory age). The
    plan must offer the possibility of acquiring a **rente viagère** at maturity, with a
    reversion option. It is operated either through a securities account or, for insurance
    versions, through a **contrat d'assurance de groupe**.
  - **L. 224-2**: three funding sources — voluntary payments by the holder; employer
    profit-sharing, incentive payments and employer contributions; compulsory employer/employee
    contributions in the relevant collective plans. These are the **three compartments**.
  - **L. 224-3**: investments must offer "sufficient protection of the savings invested"; the
    **default allocation progressively de-risks with proximity to retirement** ("gestion pilotée
    par horizon"), and the holder may choose another profile, including a solidarity option.
  - **L. 224-4**: exhaustive list of **early release** cases — death of the spouse or PACS
    partner, disability, over-indebtedness, exhaustion of unemployment benefit, judicial
    liquidation of the business, and **purchase of the principal residence**; compulsory
    contributions may **not** be released for a residence purchase.
  - **L. 224-5**: compulsory contributions convert to a **lifetime annuity**; other rights may be
    taken as a lump sum (single or staged) or as an annuity, unless the holder made an
    irrevocable annuity election at opening.
  - **L. 224-6**: rights are **transferable to any other PER**; the transfer does not change the
    conditions of redemption or liquidation; **transfer fees may not exceed 1 % of acquired
    rights and are waived after five years from the first payment or once the holder reaches
    retirement age**; compulsory-contribution rights transfer only on leaving the employer;
    changing plan requires 18 months' notice.
  - **L. 224-7**: the holder must be kept informed of the value of the plan and of transfer
    options, and receive **annual performance data gross and net of fees** for each investment.
- Products: PER (primary); RV (the annuity leg of a liquidated PER).

---

## 11. Assurance emprunteur

### R35. Loi n° 2022-270 du 28 février 2022 (loi Lemoine)
- Publisher: Légifrance (Journal officiel)
- Doc type: statute
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045268729
- Retrieved: **YES**
- Content: verified article by article.
  **Titre I** — art. 1 replaces the twelve-month cancellation window with **résiliation à tout
  moment** for borrower insurance, amending both the Code des assurances and the Code de la
  mutualité; art. 2 removes the "de groupe" restriction from the Code de la consommation
  substitution articles and requires any refusal to be explicit and to list **all** reasons and
  the missing information or guarantees; art. 3 imposes an **annual notification** of the
  cancellation right and its procedure, with administrative fines of **€3 000 for individuals and
  €15 000 for legal persons**, and requires loan offers to mention the right to cancel at any time
  after signature; art. 4 extends the cost disclosure to **eight years**; art. 5 sets a **ten
  business day** deadline to process a substitution request; art. 7 sets the sanctions framework;
  **art. 8 fixes entry into force — 1 June 2022 for new loan offers and 1 September 2022 for
  contracts already in force**.
  **Titre II** — art. 9 **droit à l'oubli**: insurers may not seek information about a cancer or
  hepatitis C beyond **five years** from the end of treatment, with a decree to follow by
  31 July 2022 if negotiations on other diseases failed; **art. 10 removes the medical
  questionnaire** where the **insured share of the borrower's loans is at most €200 000 and the
  loan matures before the borrower's 60th birthday**, effective **1 June 2022**; art. 11 requires
  a report to Parliament after two years on the effect on risk pooling, tariffs and access.
- Products: ADE (primary).

### R36. Code de la consommation, arts. L. 313-8 and L. 313-30 — TAEA, fiche standardisée, substitution
- Publisher: Légifrance
- Doc type: legislative code articles
- URLs:
  - L. 313-8 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731512
  - L. 313-30 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271935
- Retrieved: **YES** (both version **1 June 2022**)
- Content: verified.
  - **L. 313-8**: any document given to the borrower about the loan insurance must state the cost
    in three ways — (1) as a **taux annuel effectif de l'assurance (TAEA)** allowing comparison
    with the loan's overall effective rate, (2) as a **total amount in euros over eight years and
    over the full loan term**, and (3) as an **amount per payment period in euros**, stating
    whether it is added to the loan instalment. The lender must at the same time hand over the
    **fiche standardisée d'information** referred to at art. L. 313-10, plus a notice explaining
    the right to cancel the insurance at any time after signature of the loan offer. Applies to
    loan offers issued from 1 June 2022 and to existing insurance contracts from 1 September 2022.
  - **L. 313-30**: the lender may not refuse another insurance contract as security if it presents
    an **equivalent level of guarantee** to the contract it proposes; any refusal must be an
    explicit decision listing all the reasons and identifying the missing information and
    guarantees. The same rules apply when the borrower exercises the cancellation right under
    insurance law (from 1 September 2022 for contracts in force). The article as fetched does not
    itself carry the ten-working-day response deadline or a fee prohibition; those sit in loi
    Lemoine arts. 5 and 1 [R35].
- Products: ADE (primary).

### R37. France Assureurs — *Statistiques Convention AERAS, année 2023* (November 2024)
- Publisher: France Assureurs (published as Fédération Française de l'Assurance)
- Doc type: statistical dossier (20 pp.), statistics stopped at 20 November 2024
- URL: https://www.franceassureurs.fr/wp-content/uploads/aeras_dossier_stat_2023_csp_vf.pdf
- Retrieved: **YES** (PDF downloaded, full text extracted)
- Content: verified. **Applications**: **2.9 million** loan-insurance applications were assessed
  in 2023 for mortgage and professional credit (down 1.1 million on 2022, tracking a **−41 %** fall
  in new household housing credit). **90.0 %** presented no aggravated health risk and got
  standard terms; **7.6 % (224 068 applications)** presented an *risque aggravé de santé* — after
  **9.6 % in 2022 and 12.1 % in 2021**, the fall attributed to the loi Lemoine questionnaire
  removal and the five-year *droit à l'oubli* [R35]; **2.4 %** were closed without follow-up.
  Excluding pending and abandoned files, an offer was made on **99.6 %** of all applications.
  Aggravated-risk applications also covered **PTIA in 95 %** of cases and
  **incapacité-invalidité in 90 %**.
  **Outcomes on aggravated risks**: **94.5 %** received an offer covering at least death
  (**202 961** applications). Excluding files sent to the very-high-risk pool, offers with
  **no surprime and no exclusion**: **death 65 %** (64 % in 2022), **PTIA 87 %** (87 %),
  **incapacité-invalidité 51 %** (52 %). Death cover was offered **with a surprime in 31 %** and
  without a surprime but with an exclusion or limitation in **4 %**. **6 209** files went to the
  very-high-risk pool, of which **40.3 %** received an offer. **76 000** *garanties invalidité
  spécifiques* were offered in 2023 (over 2.0 million since 2011).
  **Premium pooling (écrêtement des surprimes)**: **18 569 borrowers** benefited in 2023 (711 for
  the first time), for **€4.6 m** of capped premiums; **€44.6 m** cumulative since 2007, financed
  half by insurers and half by banks. Average age of beneficiaries **46.4** (new beneficiaries
  **43.1**); **39 %** under 40, **18 %** aged 60+. Besides death, **89 %** of the files cover PTIA
  and **56 %** incapacité-invalidité; **22 %** are *délégation* contracts. **Average insured
  capital €82 700, average intended term 18.1 years.** **The average insurance rate as a
  percentage of initial capital is 1.01 % before écrêtement and 0.65 % after — a 36 % reduction.**
  **Market shape**: **€11.8 bn** of borrower-insurance premiums in 2023; **85 % (€9 987 m)** on
  contracts taken out by credit institutions for their clients and **15 % (€1 824 m)** on
  *délégation d'assurance* contracts (**22 %** for mortgages alone, 3 % professional, 2 %
  consumer); by loan type **67 % mortgage, 25 % consumer, 9 % professional**; by guarantee
  **69 % death, 30 % incapacité-invalidité, 2 % unemployment**. Processing times: at the
  convention's **second level**, 98.7 % of a 15 631-file April 2023 sample were handled within
  three weeks, average **3.1 days**; at the **third level** (managed by the BCAC), **79 %** within
  eight business days.
  The AERAS convention's own numeric thresholds — the age limit, the insured-capital ceiling and
  the *taux d'effort* trigger for écrêtement — are **not** in this document and are
  **[unverified]**.
- Products: ADE (primary); TD (underwriting-decision context).

---

## 12. Obsèques and unclaimed contracts

### R38. Code général des collectivités territoriales, art. L. 2223-33-1 — funeral financing formulas
- Publisher: Légifrance
- Doc type: legislative code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027762422
- Retrieved: **YES** (version **28 July 2013**, inserted by loi n° 2013-672 du 26 juillet 2013,
  art. 73)
- Content: verified, full text: "*Les formules de financement d'obsèques prévoient expressément
  l'affectation à la réalisation des obsèques du souscripteur ou de l'adhérent, à concurrence de
  leur coût, du capital versé au bénéficiaire.*" In one sentence this is what makes a French
  *contrat obsèques* different from an ordinary small whole-of-life policy: the capital paid to
  the beneficiary is **earmarked, up to the cost of the funeral**, for the subscriber's funeral.
  Anything above that cost falls back to the ordinary life-insurance rules. Art. L. 132-23-1 of
  the Code des assurances [R31] separately requires the death capital to be **revalued between
  death and payment**, on terms the contract must state.
- Products: OBS (primary).

### R39. Loi n° 2014-617 du 13 juin 2014 (loi Eckert) — inactive accounts and unclaimed life contracts
- Publisher: Légifrance (Journal officiel)
- Doc type: statute
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000029095362/
- Retrieved: **YES**
- Content: verified — an account is **inactive** after **12 months** without operation and without
  contact from the holder (**5 years** for savings and securities accounts); for a deceased
  holder, 12 months after death without contact from an heir. A life insurance contract is
  **unclaimed** where the benefit has not been claimed for **10 years** after the insurer knew of
  the death or after the contract's term. Insurers must "*consultent chaque année*" the national
  register of natural persons (RNIPP) to identify deceased policyholders. Balances and unclaimed
  proceeds are transferred to the **Caisse des dépôts et consignations** after **10 years**, the
  transfer taking place within one month of the deadline, and become **State property after
  20 years** at the CDC. Revaluation of the death guarantee may not fall below a rate set by
  ministerial arrêté and continues **until the deposit with the CDC**. **In force 1 January 2016**
  with limited exceptions.
- Products: AVE, AVUC, EC, PER, TD, OBS (any contract with a death benefit that can go unclaimed).

---

## 13. Tax

### R40. Code général des impôts, art. 125-0 A — taxation of life insurance products
- Publisher: Légifrance
- Doc type: legislative code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038836732/2019-10-01
- Retrieved: **YES** (version **1 October 2019 – 1 January 2020**)
- Content: verified — duration thresholds: **six years** for contracts taken out between
  1 January 1983 and 31 December 1989, **eight years** for contracts from 1 January 1990. For
  contracts meeting the threshold, an **annual abattement** applies to gains accrued from
  1 January 1998: **€4 600** for a single, widowed or divorced taxpayer and **€9 200** for a
  couple taxed jointly; it applies first to products attached to premiums paid **before
  27 September 2017**, then to products on premiums paid from that date where the art. 200 A
  option is not exercised. Withholding rates, **for premiums paid up to 26 September 2017**:
  **7.5 %** at or beyond the 6/8-year threshold, **15 %** for 4–6 years, **25 %** for 2–4 years,
  **35–45 %** under 2 years. **For premiums paid from 27 September 2017**: **12.8 %** standard,
  **7.5 %** at or beyond the 6/8-year threshold. Exemptions from income tax where the contract
  terminates by conversion into an annuity, or on redundancy, early retirement, disability of the
  holder or of the spouse. The **€150 000** total-premium threshold above which the 7.5 % rate
  ceases to apply to the excess is widely reported but was **not** confirmed in the fetched text —
  **[unverified]**. Social contributions (prélèvements sociaux) are outside this article.
- Products: AVE, AVUC, EC (policyholder behaviour: the eight-year threshold is the single
  strongest driver of French partial-surrender timing).

### R41. Code général des impôts, arts. 990 I and 757 B — death benefits
- Publisher: Légifrance
- Doc type: legislative code articles
- URLs:
  - 990 I — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288653
  - 757 B — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006305367
- Retrieved: **YES** (both version **11 March 2023**)
- Content: verified.
  - **990 I** — the *prélèvement* on sums paid by insurers on death in respect of premiums paid
    **before the insured's 70th birthday**: a fixed **abattement of €152 500 per beneficiary**
    across all contracts, then **20 % up to €700 000** of each beneficiary's taxable share and
    **31.25 % above**. A further **20 % proportional reduction** applies to certain qualifying
    unit-linked contracts (contracts entered into after 1 January 2014 or substantially modified
    by then, invested in collective vehicles, SME shares meeting employment and revenue
    thresholds, real-estate and social-housing funds, and venture/equity funds). Excluded:
    annuities acquired "*moyennant le versement de primes régulièrement échelonnées … pendant une
    durée d'au moins quinze ans*". Exempt: spouses and PACS partners (via the arts. 795–796
    inheritance exemptions) and, in defined cases, non-resident beneficiaries.
  - **757 B** — sums payable on death in respect of premiums paid **after the insured's 70th
    birthday** fall into the ordinary inheritance-tax scale by relationship, but only as to the
    **premiums**, after a single global **abattement of €30 500** across all contracts on the same
    insured's life: "*L'ensemble des sommes, rentes ou valeurs visées au I dues à raison du ou des
    contrats conclus sur la tête d'un même assuré fait l'objet d'un abattement global de
    30 500 €*". Investment gains on those premiums are outside the charge. For a **plan d'épargne
    retraite** and for the pan-European PEPP, the **whole** payout is taxable where death occurs
    after age 70.
- Products: AVE, AVUC, EC, TD, OBS, PER (the 757 B PER carve-out is specific and load-bearing).

### R42. Code général des impôts, art. 163 quatervicies — PER deductibility
- Publisher: Légifrance
- Doc type: legislative code article
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038836248
- Retrieved: **YES** (version dated **21 February 2026**)
- Content: verified — contributions to *plans d'épargne retraite populaire*, supplementary pension
  schemes and qualifying retirement contracts are deductible from net global income within an
  annual ceiling equal to the **greater of 10 % of professional income capped at eight times the
  annual PASS, and 10 % of the PASS**, less amounts already deducted under other retirement
  provisions. Unused ceiling may be used in **one of the following years** — the fetched summary
  reports **five** following years, which conflicts with the three-year figure in the tax
  administration's guidance; the discrepancy is recorded and the carry-forward length is
  **[unverified]**. Spouses and PACS partners filing jointly may, on request, **pool** their
  ceilings. A person newly resident in France gets a **tripled** first-year ceiling.
- Products: PER (primary). The deduction is what makes PER inflows behave differently from
  assurance vie inflows and belongs in any PER premium-behaviour assumption.

---

## 14. Professional standards and accounting

### R43. Institut des actuaires — Norme de Pratique Actuarielle 1 (NPA 1), *Pratiques actuarielles générales*
- Publisher: Institut des actuaires
- Doc type: professional standard (16 pp.)
- URL: https://www.institutdesactuaires.com/docs/2016133854_npa1-pratiques-actuarielles-ge-769-ne-769-rales-normes-de-pratique-recommande-769-e-ag-ia-150615.pdf
- Retrieved: **YES** (PDF downloaded, full text extracted)
- Content: verified — NPA 1 is a **category 3 professional standard, i.e. a *pratique
  recommandée***. Under art. 28 of the Institut's Statuts (June 2014), members "*devraient
  normalement se conformer à la pratique recommandée sauf s'il y a des motifs valables et
  justifiables de ne pas le faire*", and a member who departs from it must be able to explain
  clearly why and to identify the material respects in which they departed. NPA 1 is the French
  translation of the IAA's **ISAP 1**, approved 18 November 2012, and was **adopted by the
  Institut des Actuaires on 15 June 2015**. Its sections cover assignment acceptance, knowledge of
  the environment, external sources, materiality, **data quality**, assumptions and methodologies
  (whether chosen by the actuary or imposed), reasonable judgement, vocabulary, cross-references
  and the effective date.
- Products: all nine (professional frame for the assumption setting the models make explicit).

### R44. Institut des actuaires — Norme de Pratique Actuarielle 2 (NPA 2), *Modèles actuariels*
- Publisher: Institut des actuaires
- Doc type: professional standard (12 pp.)
- URL: https://www.institutdesactuaires.com/docs/2016133917_npa2-mode-768-les-actuariels-norme-de-pratique-recommande-769-e-ag-ia-150615.pdf
- Retrieved: **YES** (PDF downloaded, full text extracted)
- Content: verified — NPA 2 is likewise a **category 3 *pratique recommandée***, **adopted
  15 June 2015 with effect from 1 January 2016**, produced by the Institut's actuarial-standards
  working group (not a translation of an ISAP). It "*vise à s'appliquer à tout modèle actuariel,
  qu'il soit basé sur des logiciels externes ou des développements internes*", and its
  recommendations follow a **principle of proportionality** — to be read consistently with the
  size of the undertaking receiving the model, its resources and market presence, and with the
  stakes and complexity of the modelling. Its scope covers the critical processes of the actuarial
  function, including **pricing** and the technical studies attached to new products such as
  profitability studies. This is the standard that a reference implementation like frlib sits
  under when it publishes model documentation, a worked example and a test suite.
- Products: all nine.

### R45. IFRS 17 *Insurance Contracts*
- Publisher: IFRS Foundation
- Doc type: standard landing page
- URL: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/
- Retrieved: **YES**
- Content: verified — IFRS 17 was **issued May 2017** and is **effective for annual reporting
  periods beginning on or after 1 January 2023** (earlier application permitted if IFRS 9 is also
  applied). It replaced **IFRS 4** (2004), which had permitted "a wide variety of accounting
  practices for insurance contracts". Under the general measurement model an entity measures a
  group of contracts as "a risk-adjusted present value of the future cash flows (the **fulfilment
  cash flows**)", consistent with observable market information, plus "an amount representing the
  unearned profit in the group of contracts (the **contractual service margin**)". IFRS 17
  "includes an optional simplified measurement approach, or **premium allocation approach**, for
  simpler insurance contracts"; a **variable fee approach** exists for direct participating
  contracts but its mechanics are not set out on the fetched page and are **[unverified]** here.
  Insurance revenue, insurance service expenses and insurance finance income/expenses are
  presented separately. French listed insurers report on this basis from 2023; there is no French
  carve-out, and the fulfilment-cash-flow engine is the same projection a Solvency II best
  estimate needs [R1][R4] — the differences are discounting, the risk adjustment versus the risk
  margin, grouping and the CSM layer, not the per-policy cash flows.
- Products: all nine.

---

## 15. Market context

### R46. France Assureurs — "L'assurance vie en 2025 : une collecte solide au service de l'économie française" (press release, 27 January 2026)
- Publisher: France Assureurs
- Doc type: press release
- URL: https://www.franceassureurs.fr/espace-presse/lassurance-vie-en-2025-une-collecte-solide-au-service-de-leconomie-francaise/
- Retrieved: **YES**
- Content: verified, all 2025 figures. **Encours €2 107 bn** at end-December 2025, **+6.1 %**
  (**+€122 bn**) year on year. **Cotisations €192.1 bn**, **+10 %** (**+€17.1 bn**);
  December 2025 alone €16.1 bn, the highest December on record (+17 %). **Prestations €141.4 bn**,
  **−3 %** (**−€5.0 bn**). **Collecte nette +€50.6 bn**, up €22.1 bn on 2024 and above €50 bn for
  the first time since 2010. Split: **UC 39 % of cotisations, euro 61 %** (46 % UC in December);
  net inflows **UC +€42.5 bn, euro +€8.1 bn**. **PER assurantiels**: **€20.2 bn** of payments in
  2025 (**+16 %**), about **1 million** new plans, **7.9 million** holders at end-2025
  (**+1.0 million**), **encours €111.9 bn**, net inflow **+€11.0 bn** (the last two figures from
  the companion chiffres-clés page, same publisher, same date).
- Products: AVE, AVUC, EC, PER.

### R47. France Assureurs — "L'assurance vie en 2024" (chiffres clés, 23 September 2025)
- Publisher: France Assureurs
- Doc type: statistical page
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/lassurance-vie-en-2024/
- Retrieved: **YES**
- Content: verified, 2024. **Encours €1 985.8 bn (+3.9 %)**. **Cotisations €174.9 bn (+14.7 %)** —
  individual €160.0 bn (+16.4 %), collective €14.9 bn (−0.4 %); by support, **euro €108.6 bn
  (+19.2 %)** and **UC €66.3 bn (+8.1 %)**. **Provisions mathématiques €1 932.2 bn (+4.4 %)**,
  split **€1 345.1 bn on euro supports (≈70 %)** and **€587.1 bn on UC (+10.3 %, ≈30 %)**.
  **Prestations €146.4 bn (−3.1 %)**. **Collecte nette €28.5 bn** — UC **+€33.2 bn**, euro
  **−€4.7 bn**. **Provision pour participation aux bénéfices €53.6 bn at end-2024, −11.1 % on
  end-2023** — i.e. roughly **4 % of euro-support provisions mathématiques**, the single most
  useful public calibration point for a PPB buffer in a fonds en euros model. The page carries no
  average euro-fund revaluation rate.
- Products: AVE (primary), AVUC, EC, PER.

### R48. France Assureurs — "L'assurance vie en unités de compte en 2025" (6 May 2026)
- Publisher: France Assureurs
- Doc type: statistical page
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/assurance-vie-unite-de-compte-2025/
- Retrieved: **YES**
- Content: verified, 2025. **UC cotisations €75.1 bn**, **39.1 %** of all life premiums,
  **+13.2 %**. **UC provisions mathématiques €666.4 bn, +13.5 %**. **Net inflow €42.5 bn**, "its
  highest historical level" (against €34.3 bn in 2022). **UC-backed placements €684.5 bn**, of
  which **€567 bn financing enterprises (83 %)** — €372 bn equities, €171 bn bonds, €24 bn real
  estate. **Performance of UC supports +5.5 %** in 2025, "*brute des frais des contrats en UC et
  nette des coûts récurrents des fonds*"; **five-year average +4.9 % a year**.
  **Charges — the two figures a UC model needs**: **recurring fund costs 1.60 %** (down 2 bp on
  2024) and **contract charges on UC 0.88 %** (stable). These are market averages, not any
  insurer's rate card.
- Products: AVUC (primary), EC, PER, AVE (multisupport).

### R49. France Assureurs — chiffres clés landing page and the president's 2025 market review
- Publisher: France Assureurs
- Doc type: statistical landing page + signed market commentary
- URLs:
  - https://www.franceassureurs.fr/nos-chiffres-cles/lassurance-vie/
  - https://www.franceassureurs.fr/nos-positions/tribunes-de-notre-presidente/proteger-aujourdhui-construire-demain/ (25 March 2026)
- Retrieved: **YES** for both
- Content: verified — landing page: **encours €2 088 bn at end-2025** (a slightly earlier vintage
  than the €2 107 bn of R46, from a different cut), **UC cotisations €75.9 bn in 2025, +14.4 %**,
  and monthly premium updates (€19.3 bn in June 2026, page last updated 30 July 2026).
  Commentary: "*Près de 200 milliards d'euros de cotisations en 2025*", **net inflows €51 bn**,
  **encours €2 107 bn**; insurers hold about **€2 800 bn** invested in the economy, roughly
  **93 % of French GDP**; 2025 natural-event claims **€5.2 bn**, of which hail €2.2 bn. Neither
  page gives assurance emprunteur, obsèques or dépendance premium totals; for those see R37 and
  R28. A widely quoted **5.7 million active contrats obsèques in 2024** attributed to France
  Assureurs could not be sourced to a France Assureurs page here and is **[unverified]**.
- Products: all nine (market sizing).

---

## Extracted specifications

Everything below was read from a retrieved document unless tagged `[unverified]`. Where no public
figure exists, that is said in terms, so that the drafting stage knows to introduce a `**[std]**`
with a footnote rather than to hunt for a citation that does not exist.

### 1. Statutory technical provisions a French life model must know about
Eleven French GAAP life provisions [R6]: provision mathématique (PM, including future management
costs); provision pour participation aux bénéfices (PPB); réserve de capitalisation; provision de
gestion; provision pour aléas financiers (PAF); provision pour risque d'exigibilité (PRE);
provision pour frais d'acquisition reportés; provision pour égalisation; provision de
diversification; provision collective de diversification différée; provision de garantie à terme.
Each engagement is provisionable under exactly one head [R6].

- **PM** = PV(insurer's commitments) − PV(insured's commitments), *inclusive of future management
  costs* [R6]. This is why a French PM is not a pure net-premium reserve.
- **PRE** annual charge = **one third** of the net overall unrealised depreciation on
  R. 343-10 assets, capped so the balance-sheet provision never exceeds that depreciation; quoted
  assets marked at the **30-day average price** before inventory [R7].
- **PAF** trigger = *(real asset yield × 0.80)* **<** *(technical interest + minimum contractually
  guaranteed PB) ÷ average PM*; charge = recomputed PM (discounted at **60 % of TME**, or a
  category-weighted average, or a prudent estimated forward yield) − PM at inventory; **reversed
  at the next inventory** [R8]. The forward-yield variant requires **ACPR authorisation** [R9].
- **Réserve de capitalisation** — defined but not parameterised in the retrieved texts; it is fed
  and released on realised bond gains and losses, which is **[unverified]** here.
- **Solvency II best estimate + risk margin** sits alongside, not instead of, all of the above
  [R1][R4]. The frlib models produce best-estimate style cash flows; no risk-margin
  cost-of-capital rate was verified from a retrieved document, so any such rate is `**[std]**`.

### 2. Participation aux bénéfices — the numbers
- The obligation itself: life and capitalisation undertakings **must** share technical and
  financial profits with policyholders, on terms fixed by arrêté [R14].
- The minimum is computed **globally**, not contract by contract, over individual and collective
  contracts of all kinds [R15, A. 132-10]. *Contrats à capital variable* (unit-linked) are outside
  the A. 132-11 to A. 132-15 machinery [R15].
- **Compte de participation aux résultats** is credited with [R15, A. 132-11]:
  - the **compte technique** balance **less the insurer's technical share**, that share being the
    **greater of 10 % of the credit balance and 4.5 % of annual premiums** — so the policyholder
    share of a technical profit is **at most 90 %** and can be less;
  - **85 % of the compte financier balance**.
- The **minimum annual PB** is the credit balance of that account; the minimum *benefit* is that
  figure less interest already credited to PM, plus, where relevant, an amount reflecting the gap
  between guaranteed rates and the average rate served [R15, A. 132-12].
- **Investment return rate** for the financial account = net investment income on life operations
  ÷ average investments held in the year, computed separately for the three A. 132-11 categories
  [R15, A. 132-14]. Ceded reinsurance enters as a separate balance [R15, A. 132-15].
- **PPB release: eight financial years** from the year of allocation, to PM or to policyholders;
  **fifteen years** for FRPS and for L. 142-4 *comptabilité auxiliaire d'affectation* [R16].
- **Exceptional PPB reprise**: only where the life technical account was in deficit in the last
  year **and** the SCR (or minimum margin) is no longer covered; requires an ACPR-approved plan
  with **restitution within a maximum of eight years** and a distribution ban until restored [R16].
- **Market calibration**: PPB stock **€53.6 bn at end-2024, −11.1 % on 2023**, against euro-support
  PM of **€1 345.1 bn** — about **4 %** [R47]. No public per-insurer PPB rate exists; a model's PPB
  target ratio is `**[std]**`.

### 3. Interest rate caps — technical rate and TMG
- **Maximum technical rate** [R17, A. 132-1]: ≤ **75 % of the TME** (semi-annual average); beyond
  **eight years**, ≤ **min(3.5 %, 60 % of TME)**; for **periodic-premium or variable-capital**
  contracts, ≤ **min(3.5 %, 60 % of TME)** whatever the duration. Rates in force at subscription
  apply; non-scheduled contributions are re-tested at each payment. Collective operations are out
  of scope.
- **Reference-rate mechanics** [R17, A. 132-1-1]: reference rate = six-month arithmetic mean of
  State-borrowing rates on primary and secondary markets, semi-annual basis, × **60 %** or
  **75 %**; the maximum technical rate moves on a **0.25-point grid floored at 0**; it is
  unchanged while the monthly reference rate has not **fallen ≥ 0.10 point** or **risen
  ≥ 0.35 point**; **three months** to implement a change.
- **TMG** [R18]: what is guaranteed is **technical interest + PB** as a rate on the PM fraction
  covered [A. 132-2]. Guaranteed rates are **annualised** and fixed for **≥ 6 months and ≤ the
  period from the guarantee's effective date to the end of the following financial year** (about
  18 months) [A. 132-3 II]. Cap = **min(150 % of the maximum technical rate on the 75 %-TME
  reference, max(120 % of that rate, 110 % of the average rates served over the two preceding
  years))** [A. 132-3 III; limb (b) recorded from a structured summary, re-read before pricing
  use]. Guaranteed PB in a year is capped by reference to **80 % of the average asset-yield
  product** [A. 132-3 I; second limb of the difference not extracted]. Newly licensed undertakings:
  **120 %** of the maximum technical rate until the close of the second year after authorisation
  [A. 132-3 IV].
- Superseded but still widely quoted: an annual minimum rate not exceeding **85 % of the two-year
  average asset yield**, guaranteed for at most **eight years**, with a new-business test of a
  two-year average asset yield ≥ **4/3** of the first-year minimum rate [R18, the 2007–2010 text].
- **No public figure** exists for what any individual insurer actually sets as its TMG; observed
  practice is a TMG of 0 % on most new fonds en euros with occasional promotional guarantees —
  **[unverified]**, and any modelled TMG is `**[std]**`.

### 4. Fonds en euros — what is contractual and what is discretionary
- Contractual: the capital guarantee and the technical rate within the A. 132-1 cap [R17]; any
  TMG within the A. 132-3 caps [R18]; the minimum PB [R15]; the eight-year PPB release [R16].
- Discretionary: the annual *revalorisation* above the guaranteed floor, the split between
  immediate credit and PPB allocation, and the charge levels within the encadré's disclosed maxima
  [R30].
- **Charges**: art. A. 132-8 requires the encadré to disclose fees in **four categories** — entry
  and premium charges, recurring annual charges, exit charges, other charges — **with maximum
  amounts or percentages**, on **at most one page** [R30]. No statutory cap on any of them exists
  in the retrieved texts. The **market average** is now sourced: *chargement sur encours* on euro
  supports **0.63 %** for individual contracts and **0.47 %** for collective contracts in 2025,
  with half of all undertakings between **0.5 % and 0.8 %** [R11]. Any *named product's* charge
  level remains `**[std]**`.
- **Average rate served**: **obtainable, and now recorded** — the ACPR *Analyses et Synthèses*
  series was retrieved with `curl` and read [R11]. The average *taux de revalorisation* of euro
  supports is **2.63 % in 2025** for individual contracts (unchanged on 2024) and **2.64 %** for
  collective contracts, net of chargement sur encours and before social levies; undertakings
  representing 50 % of encours credited between **2.3 % and 2.9 %**; within a single insurer the
  gap between the best- and worst-revalued homogeneous contract groups averages **0.99 point**,
  and a policyholder with no commercial bonus is credited at least **0.39 point** below the
  market mean [R11]. The France Assureurs pages do not publish the rate [R47][R49]. A modelled
  crediting rate calibrated on those figures cites [R11] and no longer needs `**[std]**`; a
  *named insurer's* rate still does.
- **Surrender**: paid within **two months** at most; late payment at **1.5 × the legal rate for
  two months then 2 ×** [R31]. Avances (policy loans) are permitted up to the surrender value
  [R31].

### 5. Unités de compte
- Excluded from the A. 132-11 to A. 132-15 PB machinery [R15] — a UC support carries no statutory
  profit share, only the fund's own performance.
- The encadré must state prominently that amounts invested in UC are **not guaranteed and are
  subject to market fluctuations** [R30].
- The annual statement must give unit values and charges, and UC information must be refreshed at
  least **quarterly** [R31].
- **Market charge levels, 2025** [R48]: **recurring fund costs 1.60 %** (−2 bp on 2024) and
  **contract charges on UC 0.88 %** (stable). **Performance +5.5 %** in 2025, gross of contract
  charges and net of fund costs; **five-year average +4.9 % a year**.
- **Market size, 2025** [R48]: UC cotisations **€75.1 bn**, **39.1 %** of life premiums; UC PM
  **€666.4 bn** (+13.5 %); UC net inflow **€42.5 bn**.
- The DIC/KID for the underlying vehicles is governed by PRIIPs and AMF doctrine [R33]; the SRI
  1–7 scale, the performance scenarios and the RIY cost measure are **[unverified]** here.

### 6. Eurocroissance
- Legal basis: art. L. 134-1 [R19] — commitments in case of life or death, **excluding temporary
  death cover**, giving rise to a **provision de diversification**; benefit may be a **rente** or a
  **capital at maturity**; two shapes — part euro / part diversification units, or **wholly in
  diversification units before maturity with a euro guarantee at maturity**.
- A single premium may create **three kinds of engagement** — euros, unités de compte, and
  provision de diversification [R19].
- **Eight years**: the relevant duration cannot exceed the shorter of the guarantee maturity and
  **eight years** [R19, R. 134-5; R20].
- **Units**: number of *parts de provision de diversification* = total provision ÷ a common
  per-unit value [R19, R. 134-2]. Asset reallocations capped at **10 % of the provision de
  diversification** [R19, R. 134-12].
- **Participation account** [R19, R. 134-4]: credit balance goes to revaluing guaranteed benefits,
  to the provision de diversification (new units or a higher unit value), or to the **provision
  collective de diversification différée**; a deficit may be absorbed from that deferred reserve or
  by reducing the unit value within limits. **No percentages and no time limits** are set in the
  article — the split is discretionary and any modelled split is `**[std]**`.
- Excluded from the A. 132-12 minimum-PB computation [R15].
- Assets valued at realisation value per R. 343-11/R. 343-12 [R19][R20].
- **In force 1 January 2020**; old-basis contracts could still be written to **1 October 2020**
  [R20].

### 7. PER assurantiel
- **Three compartments**: voluntary payments; employer profit-sharing/incentive/contributions;
  compulsory employer and employee contributions [R34, L. 224-2].
- **Default management**: horizon-based de-risking unless the holder chooses otherwise [R34,
  L. 224-3].
- **Early release**, exhaustive: death of spouse/PACS partner, disability, over-indebtedness,
  exhaustion of unemployment benefit, judicial liquidation of the business, **purchase of the
  principal residence** (not from the compulsory compartment) [R34, L. 224-4].
- **Payout**: compulsory contributions → **lifetime annuity**; other rights → lump sum (single or
  staged) or annuity, unless an **irrevocable annuity election** was made at opening [R34,
  L. 224-5]. The plan must offer a **rente viagère with a reversion option** [R34, L. 224-1].
- **Transfers**: to any other PER; **fees ≤ 1 % of acquired rights, waived after five years from
  the first payment or at retirement age**; compulsory-compartment rights transfer only on leaving
  the employer; **18 months' notice** to change plan [R34, L. 224-6].
- **Information**: annual performance **gross and net of fees** per investment [R34, L. 224-7].
- **Tax in**: deduction of the greater of **10 % of professional income capped at 8 × PASS** and
  **10 % of PASS**, less other retirement deductions; ceiling poolable between spouses/PACS
  partners; **tripled** first-year ceiling for new residents; carry-forward length **[unverified]**
  (fetched text says five following years, the tax administration's guidance says three) [R42].
- **Tax out on death after 70**: the **whole** payout is taxable under art. 757 B — the PER does
  **not** get the premiums-only treatment that assurance vie gets [R41].
- **Market**: **€20.2 bn** paid into PER assurantiels in 2025 (+16 %), ≈**1 million** new plans,
  **7.9 million** holders, **€111.9 bn** encours, net inflow **+€11.0 bn** [R46].

### 8. Rente viagère — tables and rates
- **Annuity tables**: **TGH05** (male) and **TGF05** (female), generational, homologated by the
  arrêté du 1er août 2006 and applicable to annuity contracts **subscribed from 1 January 2007**;
  minimum reserves on the 1993 table for older contracts until **1 August 2008** [R21].
- **Non-annuity tables**: **TH 00-02** (male) and **TF 00-02** (female), homologated by the arrêté
  du 20 décembre 2005, **in force 1 January 2006** (annuity-calculation provisions 1 July 2006),
  with **TD 88-90** and **TV 88-90** carried over from 1993 [R22].
- **Which table when** [R23, A. 335-1]: homologated tables **by sex** — insured-population based
  for annuities, INSEE based for everything else — **or** the undertaking's own **tables
  d'expérience certified by an independent actuary approved by an actuarial association recognised
  by the supervisor**. Where a single table is used for all insureds it must be the sex-appropriate
  table giving the **most prudent** rate. For annuities, **rates on experience tables may not be
  lower than rates on the appropriate homologated tables** — an explicit floor that caps the
  pricing benefit of experience tables.
- **Age shifts (décalage d'âge)** for non-annuity survival contracts [R23, Annexe]: TF 00-02 runs
  from **−11 years at ages 16–32** to **0 at 94+**; TH 00-02 from **−13 years at ages 16–38** to
  **−3 at 75+**. Tables are tabulated as $l_x$ over ages **0–112** (TD 88-90 over 0–106).
- **Technical rate** for the annuity: capped by A. 132-1 [R17]; over an annuity's duration the
  binding limb is normally **min(3.5 %, 60 % of TME)**.
- A **gender-neutral TGHF05** built from TGH05 and TGF05 in a **60 % male / 40 % female** mix,
  reported as mandatory for collective supplementary-retirement contracts from **24 October 2024**,
  appears only in a search summary and is **[unverified]**.
- **The tables themselves are not redistributed by this library.** The frlib decrement CSVs are
  `**[std]**` proxies built from the freely reusable INSEE series [R24] and anchored so each
  product's own best-estimate factor reproduces its technical-notes placeholder exactly.

### 9. Temporaire décès and obsèques
- Table: **TH 00-02 / TF 00-02** with the annexed age shifts [R22][R23].
- No statutory minimum or maximum sum assured, no statutory term limits, and no public rate card
  exist in the retrieved corpus — every sum assured, age range and premium rate in the frlib TD and
  OBS models is `**[std]**`.
- **Obsèques specifics** [R38]: the capital paid to the beneficiary is, by statute, **earmarked for
  the subscriber's funeral up to its cost**. Art. L. 132-23-1 requires the **death capital to be
  revalued between death and payment** on terms the contract must state [R31].
- **Payment on death** [R31]: **15 days** to request documents, **1 month** to pay after the
  complete file; overrun penalties **2 × the legal rate for one month then 3 ×** (document step)
  and **2 × for two months then 3 ×** (payment step).
- **Unclaimed contracts** [R39]: unclaimed after **10 years** from the insurer's knowledge of death
  or the contract's term; annual **RNIPP** search obligation; transfer to the **CDC** after
  **10 years** (within one month of the deadline); **State property after 20 years**; revaluation
  continues to the CDC deposit at not less than a rate set by arrêté.
- Market: **5.7 million active contrats obsèques in 2024** is quoted in secondary press as a France
  Assureurs figure but could not be sourced to the publisher — **[unverified]** [R49].

### 10. Assurance emprunteur
- **Guarantees**: décès, **PTIA** (perte totale et irréversible d'autonomie), incapacité–invalidité
  (ITT/IPT/IPP), and optionally perte d'emploi [R37].
- **Premium split by guarantee, 2023** [R37]: **décès 69 %**, **incapacité-invalidité 30 %**,
  **perte d'emploi 2 %**. By loan type: **mortgage 67 %, consumer 25 %, professional 9 %**.
- **Market size, 2023** [R37]: **€11.8 bn** of premiums; **85 % (€9 987 m)** bank group contracts,
  **15 % (€1 824 m)** *délégation d'assurance* (**22 %** on mortgages alone).
- **Rate level — the one public price point** [R37]: among borrowers benefiting from the AERAS
  pooling mechanism, the **average insurance rate is 1.01 % of initial capital before écrêtement
  and 0.65 % after**, on an **average insured capital of €82 700** over an **average intended term
  of 18.1 years**, at an **average age of 46.4**. These are aggravated-risk lives, so they bound a
  standard rate from above rather than describing it. No standard-risk rate table is public — the
  frlib ADE premium rate is `**[std]**`.
- **Underwriting outcomes, 2023** [R37]: **7.6 %** of 2.9 million applications present an
  aggravated health risk; **94.5 %** of those get an offer covering at least death; of those offers
  (outside the pool), **65 % death / 87 % PTIA / 51 % incapacité-invalidité** with no surprime and
  no exclusion; death cover carries a **surprime in 31 %** of cases and an exclusion or limitation
  without surprime in **4 %**; **40.3 %** of the 6 209 very-high-risk pool files get an offer.
- **Loi Lemoine** [R35]: **résiliation à tout moment**; **no medical questionnaire** where the
  insured share ≤ **€200 000** and the loan matures **before the borrower's 60th birthday**;
  **droit à l'oubli reduced to five years** from end of treatment for cancers and hepatitis C;
  annual notification duty with fines of **€3 000 / €15 000**; **ten business days** to process a
  substitution; cost disclosure over **eight years**; in force **1 June 2022** (new offers) and
  **1 September 2022** (contracts in force).
- **Disclosure** [R36]: **TAEA**, total euro cost over eight years and over the full term, euro
  amount per period, plus the **fiche standardisée d'information**; the lender may not refuse an
  alternative contract of **equivalent guarantee** and must give an explicit, fully reasoned
  refusal.
- **Quotité** (the share of the loan each co-borrower insures, e.g. 50/50 or 100/100) is a
  contractual election with no statutory floor or ceiling in the retrieved texts — the frlib
  quotité assumption is `**[std]**`.

### 11. Dépendance
- **Scale**: the **grille AGGIR**, six *groupes iso-ressources*; **GIR 1** most dependent, **GIR 6**
  most autonomous; **GIR 1–4** confer APA entitlement [R25][R26].
- **Population**: **1.3 million APA beneficiaries** at December 2022 — **794 000 at home**,
  **542 500 in institutions**; **7.2 %** of the **18.4 million** people aged 60+ [R26].
- **GIR mix of APA beneficiaries, 2022** [R26]: at home **GIR 1 2 % / GIR 2 18 % / GIR 3 22 % /
  GIR 4 58 %**; in institutions **GIR 1 13 % / GIR 2 44 % / GIR 3 19 % / GIR 4 24 %**.
- **Public benefit scale — monthly APA-at-home ceilings, 2024** [R26]: **GIR 1 €1 955.60**,
  **GIR 2 €1 581.44**, **GIR 3 €1 143.09**, **GIR 4 €762.87**.
- **Incidence and duration** [R25]: **57 % of retirees** ever receive APA (**69 %** women,
  **44 %** men); expected APA duration over the whole retiree population **2.4 years** (**3.3**
  women, **1.4** men), i.e. **9.6–10 %** of a **25.1-year** expected retirement; among
  beneficiaries roughly **2.9 years** (men, at home) and **2.3–3.2 years** in institutions;
  **mean entry age 80.1 to 86.0** across pension quintiles for home APA.
- **Insurance market, 2024** [R28]: **2.4 million** insured through insurance undertakings
  (**−6.9 %**), **58 %** on contracts where dependency is the principal guarantee; **€618.1 m**
  premiums (**−3 %**), **88 %** from principal-and-only dependency guarantees; **average annual
  premium €472 individual / €106 collective**; **average subscription age 64**; **€357.3 m**
  benefits (**+6.3 %**); **€6.4 bn** provisions; **41 900 annuities in payment** with an **average
  monthly annuity of €583**; **28 400** new contracts (**−13.7 %**). Across all bodies, **6.0
  million** insured (**56 % mutuelles / 40 % insurers / 4 % institutions de prévoyance**).
- **Benefit design points that are real, not invented** [R28]: contributions of **0.40 %–1.50 % of
  the PMSS**; guaranteed minimum monthly annuity **€200–€750** for **total dependency (GIR 1–2)**
  and **€100–€375** for **partial dependency (GIR 3), set at 50 % of the GIR 1–2 annuity**; a
  **0.60 % PMSS** base plus **0.40 % PMSS** option (**€15.70/month in 2025**) lifting the GIR 1–2
  minimum to **€500** and the GIR 3 minimum to **€250**.
- **Claim definition** [R28]: automatic recognition where APA is in payment for GIR 1–2; otherwise
  medical certification by the insurer's officer, a state of dependency lasting **more than three
  months**, and inability to perform **2 or 3 of the 4 *actes de la vie courante***.
- **Behaviour** [R28]: continuation after leaving the employer without medical selection at the same
  tariff **within six months**; **no reduction value** — the guarantee is maintained for life even
  if contributions stop. Individual contracts: subscription ages **60–75**, no medical selection,
  no guaranteed minimum annuity.
- **Pricing inputs** [R28]: two series per age — **mortality of the generation (healthy and future
  disabled)** and **future prevalence of disability in the generation**; the acquisition-value
  scale is sensitive to the technical rate, the revaluation coefficient, the loading rate and the
  guaranteed minimum annuity, more so at younger ages.
- **No public French incidence table by age and GIR exists.** Every incidence rate in the frlib
  dépendance model is `**[std]**`, calibrated against the prevalence and duration figures above.

### 12. Contract information and policyholder behaviour drivers
- **Renonciation**: **30 full calendar days** from being informed the contract is concluded;
  repayment within **30 calendar days**; interest **1.5 × legal rate for two months then 2 ×**;
  extension to the 30th day after actual delivery where documents were withheld, **capped at eight
  years** [R29].
- **Encadré**: at most **one page**, eight fixed sections, fee maxima disclosed in four categories
  [R30].
- **Annual statement and website publication**: within **90 business days of 31 December**, kept
  online **five years**; UC information at least **quarterly**; a statement **one month before**
  the term [R31].
- **Tax thresholds that drive surrender timing** [R40]: **eight years** (six for pre-1990
  contracts); annual abattement **€4 600 / €9 200**; **7.5 %** beyond the threshold, **12.8 %**
  before it for post-26-September-2017 premiums; older tranches **15 % / 25 % / 35–45 %**. The
  **€150 000** premium threshold is **[unverified]**.
- **Tax thresholds on death** [R41]: **€152 500** per beneficiary then **20 % / 31.25 %** above
  **€700 000** for pre-70 premiums; **€30 500** global abattement then the inheritance scale for
  post-70 premiums; PER fully taxable on death after 70.
- **Macroprudential tail risk** [R13]: the HCSF may suspend surrenders and arbitrages for up to
  **three months, renewable**, with the surrender restriction capped at **six consecutive months**.
  A lapse-stress scenario should be able to represent this.

### 13. What has no public number and must be standardised
**Corrected 2026-08-26.** The market **average euro-fund crediting rate and its dispersion** used
to head this list, on the false premise that the ACPR was blocked. They are now sourced from the
retrieved *Analyses et Synthèses* n° 180 [R11] — 2.63 % individual / 2.64 % collective in 2025,
a 2.3 %–2.9 % band across undertakings holding half the encours, a 0.99-point spread inside a
single insurer — and are no longer `**[std]**`. The same applies to the average *chargement sur
encours* (0.63 % / 0.47 %) and the PPB ratio (4.0 % of life provisions end-2025). What remains
genuinely unavailable is everything *per insurer* or *per contract*.

The following are **not** available from any retrieved public source and must be `**[std]**` in the
product documents, with a footnote naming the gap:
insurer-specific TMG;
acquisition, administration and asset-management charge levels for any named product; surrender and
arbitrage charge scales; commission rates; per-insurer PPB target ratios and release policy;
lapse and partial-surrender rates by duration; the per-contract distribution behind the
0.99-point within-insurer revaluation gap [R11]; ADE standard-risk premium rates and quotité mixes;
dépendance incidence rates by age and GIR and the healthy/disabled mortality split; obsèques
sum-assured distributions; and any certified *table d'expérience* (legal under A. 335-1 [R23] and
by construction private).

---

## Variations across insurers

This is the cross-product **regulatory** file. It carries no `S#` primary product documents — no
notice d'information, conditions générales or DIC was fetched here, and none is cited. What
follows is therefore the *latitude the regulation leaves*, plus what the retrieved market
aggregates say about how that latitude is actually used. Insurer-by-insurer variation with
document citations belongs in the nine per-product research files.

| Dimension | What is fixed by law | What varies between carriers | Evidence |
|---|---|---|---|
| Minimum PB | 85 % of the financial account; technical account less the greater of 10 % of its credit balance and 4.5 % of premiums; computed **globally** | Which contracts are grouped into which *catégorie* for the global computation; how much is credited immediately vs parked in the PPB | [R15][R16]; per-insurer policy not public — `[std]` |
| PPB | Release within **8 years** (15 for FRPS / L. 142-4) | Target stock, build-up pace, release policy in a falling-rate year | [R16]; market stock €53.6 bn ≈ 4 % of euro PM at end-2024 [R47], and **4.3 % of life provisions end-2024 falling to 4.0 % end-2025** on individual contracts, 4.2 % bancassureurs vs 3.6 % traditional insurers [R11]; per-insurer target still `[std]` |
| Technical rate | ≤ 75 % TME; ≤ min(3.5 %, 60 % TME) beyond 8 years or on periodic premiums | Whether any technical rate is used at all; the ACPR states "*l'essentiel des contrats actuellement commercialisés en France a un taux technique faible ou nul*", with a PM-weighted average of **0.32 %** in 2025 on individual contracts and **0.98 %** on collective ones — the stronger claim that *most* new contracts are written at exactly **0 %** is not in the document and stays **[unverified]** | [R17][R11] |
| TMG | Caps at A. 132-3; duration ≥ 6 months and ≤ ~18 months | Whether a TMG is offered at all, and at what level; promotional guarantees on new money, and UC-holding bonuses "*souvent de 100 points de base, et allant jusqu'à plus de 200 points de base*" [R11] | [R18]; per-insurer TMG levels not public — `[std]` |
| Mortality basis | Homologated tables **or** certified *tables d'expérience*; annuity rates on experience tables floored at homologated-table rates | Which insurers hold certified experience tables and how much they load; the certifying actuary is named only in supervisory filings | [R23] |
| UC charges | Must be disclosed in the encadré with maxima, in four categories | Level: market average **contract charge 0.88 %** on UC and **fund cost 1.60 %** in 2025, with real dispersion around both | [R30][R48] |
| UC range | Must be an eligible asset; DIC required | Number and type of supports, presence of SCPI/SCI, private-equity and structured products | [R33]; per-contract, not public here |
| Eurocroissance | 8-year duration cap; provision de diversification and its deferred collective reserve | Guarantee level at maturity (below or at 100 %), split of the participation account between PM revaluation, unit-value uplift and the deferred reserve — **no statutory split** | [R19][R20] |
| PER | 3 compartments; transfer fee ≤ 1 %, nil after 5 years; exhaustive early-release list | Management-mandate design (horizon glide path), annuity conversion basis, guaranteed table | [R34] |
| Assurance emprunteur | TAEA and fiche standardisée; equivalence of guarantees; résiliation à tout moment; no questionnaire below €200 000 / age 60 | Bank *contrat groupe* vs *délégation* (85 % / 15 % of premiums in 2023); premium expressed on initial vs outstanding capital; ITT franchise length; quotité | [R35][R36][R37] |
| Dépendance | AGGIR/GIR scale is public; APA entitlement is GIR 1–4 | Whether the contract triggers on GIR 1–2 only or also GIR 3(–4); AVQ-based versus GIR-based definitions; waiting periods; annuity in euros vs in points; guaranteed minimum annuity | [R25][R26][R28] |
| Obsèques | Capital earmarked to the funeral up to its cost; revaluation between death and payment | Whether the contract is *en capital* or *en prestations* (bundled funeral services); revaluation rate; single vs periodic premium | [R31][R38] |

Two structural observations that the drafting stage should carry into the product documents:

1. **The regulation constrains the floor, not the offer.** Almost every number a French policy
   actually shows a customer — the crediting rate, the charges, the TMG, the surrender penalty
   scale — is set by the insurer within a statutory envelope, and none of it is published per
   insurer. That is why the frlib parameter tables will be `**[std]**`-heavy and why each `[std]`
   footnote should point at the specific article that bounds it.
2. **The euro fund's discretion is a two-lever system.** The insurer chooses the crediting rate
   *and* the PPB allocation, subject to the global minimum PB [R15] and the eight-year release
   [R16]. A model that credits a rate without also modelling the PPB stock has not modelled a
   French fonds en euros; the two levers together are the product.

---

## Gaps and caveats

1. **WITHDRAWN — "the ACPR is unreachable" was wrong.** This caveat previously reported that
   every request to `acpr.banque-france.fr` returned **HTTP 403** with an "Accès refusé" body,
   with and without a browser User-Agent, and concluded that the average *taux de revalorisation*
   of fonds en euros, its dispersion, the average *chargement sur encours* and the PPB ratio were
   unobtainable. **All of that is false.** The host serves normally; the discriminator is the
   *fetcher*, not the User-Agent. `curl` returns **HTTP 200** on the ACPR home page, on
   `www.banque-france.fr`, on both *Analyses et Synthèses* landing pages and on every PDF tried,
   byte-identical with and without a browser User-Agent, while the plain fetcher used for the
   rest of this sweep is refused. The error was compounded by a second trap: this host answers a
   **wrong** `/system/files/` path with **403 rather than 404**, so one mistyped n° 179 URL
   looked like a domain-wide block rather than a typo.
   **What was actually lost, and has now been recovered.** *Analyses et Synthèses* n° 179, n° 180
   and n° 175, and Recommandation 2024-R-03, were downloaded with `curl` and read in full;
   [R11] and [R12] are rewritten against them and are `Retrieved: YES`. The average euro-fund
   rate is **2.63 % for 2024 and 2.63 % for 2025** on individual contracts — not "about 2.6 %
   from press summaries" — with the dispersion, the chargement and the PPB ratio all in the
   documents. The `[unverified]` tag on those figures is **withdrawn**.
   **What still limits them.** The series publishes market aggregates only: no named insurer's
   crediting rate, TMG or charge scale appears in it, so those stay `**[std]**`. n° 175 carries
   an **"ACPR-RESTREINT"** page marking although served from the public publications area; it is
   used here only for comparatives that n° 180 restates. A CCSF report on dépendance disclosure
   was recorded as 403'ing on `banque-france.fr`; no URL for it was kept, so it has not been
   re-tried — given the above, assume it is retrievable with `curl` and re-fetch it before
   treating it as a gap.
   **Method note for any future sweep of this library: a 403 from `acpr.banque-france.fr` means
   either the wrong fetcher or the wrong path. Retry with `curl` before recording a block.**
2. **EUR-Lex is behind an AWS WAF JavaScript challenge.** Directive 2009/138/CE [R1], Règlement
   délégué (UE) 2015/35 [R2], Directive (UE) 2025/2 [R3] and Règlement (UE) 1286/2014 [R33] could
   not be read; four URL forms were tried (`/legal-content/.../?uri=`, `/legal-content/.../HTML/`,
   `/legal-content/.../PDF/`, `/eli/`), all returning HTTP 202 with an empty body or the challenge
   page. Their content is described from EIOPA's framework page [R4] and the AMF's national
   doctrine [R33]. **No Solvency II article number, no risk-margin cost-of-capital rate and no
   PRIIPs SRI/RIY parameter in this file was read from the instrument itself.**
3. **Directive (EU) 2025/2 detail is unverified.** Only the application date — **30 January
   2027** — is verified, from EIOPA [R4]. Proportionality, sustainability, macroprudential tools
   and any risk-margin change are **[unverified]**.
4. **Two Code des assurances renumberings are only partly pinned down.**
   (a) Art. L. 331-3 [R14] served a version running to **1 January 2016**, implying it moved at the
   Solvency II recodification; the current article number is **[unverified]** and product documents
   should cite the substance, not a live article number.
   (b) Art. A. 335-1 and its annexe [R23] likewise served **2012–2016** and **2006–2016** versions
   even when a current-date URL suffix was supplied; the mortality-table rules described are
   certainly the operative ones, but their **current article placement is [unverified]**.
5. **The PAF computation article is abrogated.** The formula recorded at [R8] is from art. A. 331-2
   as it stood **14 September 2014 – 1 January 2016**. The provision itself plainly survives —
   R. 343-3 5° names it [R6] and A. 341-1 4° regulates a derogation for it [R9] — but the current
   article carrying the calculation was not located. Cite the mechanics, not the article, for
   current dates.
6. **Art. A. 132-3 was not fully extracted.** Paragraph I's ceiling is a *difference* whose second
   limb the fetcher did not return, and paragraph III's second limb (120 % / 110 %) came from the
   fetcher's structured summary rather than a verbatim quote. Both are recorded as such in [R18]
   and in *Extracted specifications* §3. Re-read A. 132-3 before using either in a live pricing
   context.
7. **Two internal conflicts are left standing rather than resolved.**
   (a) Carry-forward under CGI art. 163 quatervicies: the fetched page reported **five** following
   years, the tax administration's published guidance reports **three** [R42]. Marked
   **[unverified]**.
   (b) End-2025 encours: **€2 107 bn** on the press release and chiffres-clés pages [R46][R49]
   versus **€2 088 bn** on the landing page [R49]. Different cuts of the same series; both
   recorded, neither reconciled.
8. **CGI art. 125-0 A's €150 000 threshold is unverified.** The 7.5 %/12.8 % split by total
   premiums paid is standard practice but did not appear in the fetched text of the article [R40].
9. **The DDA's substantive requirements were never read.** Légifrance serves only a metadata
   landing page for Directive (UE) 2016/97 and points to EUR-Lex [R32]. The IPID, the
   demands-and-needs test, the suitability regime for insurance-based investment products, and the
   Code des assurances Livre V articles (L. 521-1 ff., L. 522-1 ff.) that replaced art. L. 132-27-1
   are all **[unverified]**. The abrogated L. 132-27-1 text is retained because it is what most
   French product literature still paraphrases.
10. **AERAS convention thresholds are missing.** The 2023 statistical dossier [R37] gives outcomes
    and premium levels but not the convention's own eligibility parameters — the age limit, the
    insured-capital ceiling, and the *taux d'effort* trigger for écrêtement. All **[unverified]**.
11. **No restricted or proprietary table is reproduced.** TH 00-02, TF 00-02, TD 88-90, TGH05 and
    TGF05 are cited by name, arrêté and code article [R21][R22][R23] but the $l_x$ values are not
    copied into this library; certified *tables d'expérience* are private by construction [R23].
    The frlib decrement CSVs are `**[std]**` proxies from INSEE population data [R24], anchored so
    that each product's best-estimate factor reproduces its own technical-notes placeholder
    exactly. The TGHF05 gender-neutral table (60 % male / 40 % female, reported mandatory for
    collective supplementary-retirement contracts from 24 October 2024) is **[unverified]**.
12. **INSEE licence terms were not stated on the dataset page** [R24]; standard INSEE open-data
    reuse is assumed and that assumption is **[unverified]**. Confirm before redistributing derived
    CSVs.
13. **PDF text extraction was done locally, not by the fetcher.** For the DREES study [R25], the
    CNSA yearbook [R26], the Institut des actuaires dépendance deck [R28], the AERAS dossier
    [R37] and both NPA standards [R43][R44], the fetcher returned raw PDF bytes and the text was
    extracted locally with PyMuPDF before being read. The same applies, a step further removed,
    to the four ACPR documents behind [R11] and [R12] — *Analyses et Synthèses* n° 175, n° 179
    and n° 180 and Recommandation 2024-R-03 — which were downloaded with **`curl`**, not the
    fetcher, and then extracted the same way. Figures quoted from all of these are transcriptions
    of extracted text, not of a rendered page; **chart-only values were transcribed only where
    the chart's data labels appear in the extracted text stream** (which is the case for the
    ACPR quartile, TRA and PPB series quoted in [R11], each of which carries its numbers as text)
    and not otherwise — the *taux de dépendance par âge* chart in [R28], for example, is **not**
    transcribed and is not cited.
14. **Institut des actuaires standards index 404'd.** The normes-professionnelles index page
    returned HTTP 404; NPA 1 and NPA 2 were reached by direct PDF URL [R43][R44]. **NPA 3, NPA 4
    (best-estimate provisions in non-life and life) and NPA 5 (data) were not retrieved**, and
    their existence and dates are **[unverified]** from search summaries only. NPA 4 in particular
    would be the most directly relevant standard to this library and should be retrieved before the
    reference file is finalised.
15. **IFRS 17's variable fee approach was not described by the fetched page** [R45]. Since French
    fonds en euros and eurocroissance are the archetypal direct-participating contracts, the VFA
    mechanics matter and are **[unverified]** here.
16. **The web-search budget was exhausted mid-session** (200 of 200 calls). Later entries were
    reached by direct URL construction from Légifrance link tables — which worked well, since
    Légifrance article pages expose the `LEGIARTI` hrefs of cited articles. Two consequences: no
    search was run for a French-language IFRS 17 / ANC accounting source, and no search was run to
    confirm the current article numbers flagged in caveat 4.
17. **This file contains no `S#` sources.** It is the cross-product regulatory library; primary
    insurer documents (notice d'information, conditions générales, DIC, tableau de garanties,
    fiche standardisée d'information) belong in the nine per-product research files and are cited
    there. The *Variations across insurers* section above is accordingly written from regulatory
    latitude and market aggregates, not from carrier documents.
