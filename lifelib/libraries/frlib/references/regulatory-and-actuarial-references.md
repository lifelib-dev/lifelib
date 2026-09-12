# Regulatory and Actuarial References — French Life Insurance

**Status:** Draft, 2026-08-26.

Curated reference library for the France section of the reference-product library. It
covers the prudential (Solvabilité II and the French statutory technical provisions),
supervisory and macroprudential, participation aux bénéfices and guaranteed-rate,
mortality/morbidity, conduct-and-distribution, legislation-and-tax,
professional-standards and accounting sources that the reference cash-flow-model
implementations (assurance-vie-euro / assurance-vie-uc / eurocroissance / per-assurance
/ rente-viagere / temporaire-deces / assurance-emprunteur / obseques / dependance) rely
on. Product folders cite entries on this page as **[REG-R#]** (e.g., `[REG-R1]`); the
R1–R49 numbering below is **frozen** — do not renumber or reuse numbers, as product
documentation cites against it. Within this page, plain `[R#]` refers to the same
entries. Facts drawn from a document that was actually retrieved carry its number;
claims from general knowledge or search-result summaries are tagged **[unverified]**;
failed or unfetched links are disclosed per entry — no URL on this page is fabricated.
All URLs accessed **2026-08-26** unless noted otherwise.

**Regulatory architecture in one line:** the ACPR (adossée à la Banque de France)
supervises French insurers under Solvabilité II as transposed into the Code des
assurances; the AMF shares conduct competence on unit-linked distribution through the
collective vehicles that back the *unités de compte*; and the Code des assurances
itself carries both the prudential rules (the *provisions techniques* of Livre III) and
the contract law (Livre I), which is why one code governs both what a French model must
reserve and what it must promise.

**Two French terms carry the whole library** and are used untranslated after first use.
**Fonds en euros** — the general account with a capital guarantee (*effet cliquet*: once
credited, interest cannot be taken back) and a discretionary annual *revalorisation*.
**Participation aux bénéfices (PB)** — the statutory minimum profit share owed to
policyholders collectively, computed from a *compte de participation aux résultats* and
either credited immediately to the *provision mathématique* or parked in the *provision
pour participation aux bénéfices* (PPB) for up to eight years.

**Scope note on capital:** the SCR and MCR exist under Solvabilité II [R1] [R4], and the
French statutory balance sheet carries its own eleven technical provisions [R6] — but
this library treats the capital layer as **cited-not-specified**: reference cash flow
models produce best-estimate liability cash flows; SCR aggregation, the risk-margin
projection and own funds are referenced, never specified. No risk-margin
cost-of-capital rate in this file was read from a retrieved instrument, so any such rate
in a product document is `**[std]**`.

**Host behaviour observed in this session.** `legifrance.gouv.fr` serves fully to a
plain fetcher and is the workhorse of this file; `franceassureurs.fr`, `insee.fr`,
`drees.solidarites-sante.gouv.fr`, `cnsa.fr`, `institutdesactuaires.com`,
`amf-france.org`, `eiopa.europa.eu` and `ifrs.org` all serve.

**Correction, 2026-08-26 — the ACPR is not blocked.** This header previously stated that
`acpr.banque-france.fr` and `banque-france.fr` "return HTTP 403 to every request, with and
without a browser User-Agent", and recorded [R11] and [R12] as known references only.
**That was false and is withdrawn.** The discriminator is the *fetcher*, not the
User-Agent: the plain fetcher used for the rest of this page is refused with an
"Accès refusé" body, while **`curl` gets HTTP 200 with byte-identical responses with and
without a browser User-Agent** — confirmed on the ACPR home page, on `www.banque-france.fr`,
on both *Analyses et Synthèses* landing pages, and on four ACPR PDFs (0.9–2.0 MB each,
`application/pdf`). The mistake was reinforced by a second trap: this host answers a
**wrong** path under `/system/files/` with **403 rather than 404**, so a single mistyped PDF
URL was indistinguishable from a domain-wide block. [R11] and [R12] have been re-fetched
with `curl`, read in full, and are now **Fetched: yes**.

**`eur-lex.europa.eu` sits behind an AWS WAF JavaScript challenge** and returns an empty
document to any non-browser client — that block is real and stands — so no Solvency II
or PRIIPs article number on this page was read from the instrument itself
[R1] [R2] [R3] [R33]. Six PDFs [R25] [R26] [R28] [R37] [R43] [R44] were returned as raw bytes
by the fetcher, and four more — the ACPR documents behind [R11] and [R12] — were downloaded
with `curl`; all ten were extracted locally with PyMuPDF. Figures from those are
transcriptions of extracted text, not of a rendered page. Chart-only values were not
transcribed, except where a chart's own data labels appear in the extracted text stream,
which is the case for the ACPR quartile, asset-yield and PPB series quoted at [R11].

---

## Product-relevance matrix

`x` = load-bearing for that product's specification, technical notes or model; `(x)` =
qualified, conditional or background relevance (the entry governs the product but does
not shape its cash flows, or reaches it only through a compartment or an option);
blank = not relevant. Column key: AVE = assurance-vie-euro, AVUC = assurance-vie-uc,
EC = eurocroissance, PER = per-assurance, RV = rente-viagere, TD = temporaire-deces,
ADE = assurance-emprunteur, OBS = obseques, DEP = dependance.

| R# | Reference (short name) | AVE | AVUC | EC | PER | RV | TD | ADE | OBS | DEP |
|----|------------------------|-----|------|----|-----|----|----|-----|-----|-----|
| R1 | Directive 2009/138/CE — Solvabilité II | x | x | x | x | x | x | x | x | x |
| R2 | Règlement délégué (UE) 2015/35 | x | x | x | x | x | x | x | x | x |
| R3 | Directive (UE) 2025/2 — Solvency II review | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R4 | EIOPA — Solvency II framework page | x | x | x | x | x | x | x | x | x |
| R5 | EIOPA — risk-free interest rate term structures | x | (x) | x | x | x | (x) | (x) | (x) | x |
| R6 | C. ass. art. R. 343-3 — eleven technical provisions | x | x | x | x | x | x | x | x | x |
| R7 | C. ass. art. R. 343-5 — PRE | x | | x | x | x | | | | |
| R8 | Provision pour aléas financiers — art. A. 331-2 (abrogated) | x | | x | x | x | | | | |
| R9 | C. ass. art. A. 341-1 — ACPR derogations | (x) | | (x) | (x) | (x) | | | | |
| R10 | CMF art. L. 612-1 — the ACPR | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R11 | ACPR — *Analyses et Synthèses* on the life market | x | (x) | x | x | | | | | |
| R12 | ACPR — Recommandation 2024-R-03 (devoir de conseil) | (x) | (x) | (x) | (x) | | | | | (x) |
| R13 | HCSF — CMF art. L. 631-2-1 (surrender freeze) | x | x | x | x | | | | | |
| R14 | C. ass. art. L. 331-3 — the PB obligation | x | | x | x | x | (x) | (x) | (x) | (x) |
| R15 | C. ass. arts. A. 132-10 to A. 132-15 — compte de participation | x | (x) | x | x | x | (x) | (x) | (x) | (x) |
| R16 | C. ass. arts. A. 132-16 / A. 132-16-1 — PPB eight-year rule | x | | x | x | x | | | | |
| R17 | C. ass. arts. A. 132-1 / A. 132-1-1 — maximum technical rate | x | | x | x | x | (x) | | x | x |
| R18 | C. ass. arts. A. 132-2 / A. 132-3 — TMG | x | | x | x | (x) | | | (x) | (x) |
| R19 | C. ass. art. L. 134-1 and R. 134-1 to R. 134-12 | (x) | (x) | x | | | | | | |
| R20 | Décret n° 2019-1437 — eurocroissance reform | | | x | | | | | | |
| R21 | Arrêté du 1er août 2006 — TGH05 / TGF05 | (x) | | (x) | x | x | | | | x |
| R22 | Arrêté du 20 décembre 2005 — TH 00-02 / TF 00-02 | (x) | | | | | x | x | x | x |
| R23 | C. ass. art. A. 335-1 and its Annexe — which table applies | x | x | x | x | x | x | x | x | x |
| R24 | INSEE — mortalité, espérance de vie | x | x | x | x | x | x | x | x | x |
| R25 | DREES *Études et Résultats* n° 1327 — APA over retirement | | | | (x) | (x) | | | | x |
| R26 | CNSA — *Chiffres clés de l'aide à l'autonomie 2024* | | | | | | | | | x |
| R27 | DREES *Études et Résultats* n° 1101 — private cover by risk | | | | | | (x) | (x) | | (x) |
| R28 | Institut des actuaires — atelier dépendance (2025) | | | | | | | | | x |
| R29 | C. ass. arts. L. 132-5-1 / L. 132-5-2 — renonciation | x | x | x | x | (x) | (x) | | (x) | (x) |
| R30 | C. ass. arts. A. 132-4 / A. 132-8 — note d'information, encadré | x | x | x | x | (x) | (x) | | (x) | (x) |
| R31 | C. ass. arts. L. 132-21 / L. 132-22 / L. 132-23-1 | x | x | x | x | (x) | (x) | | x | (x) |
| R32 | Devoir de conseil — art. L. 132-27-1 (abrogated) and the DDA | (x) | (x) | (x) | (x) | | (x) | (x) | (x) | (x) |
| R33 | PRIIPs — Règlement (UE) 1286/2014 and AMF DOC-2011-05 | (x) | x | (x) | (x) | | | | | |
| R34 | Loi PACTE art. 71 and CMF arts. L. 224-1 to L. 224-8 | | | | x | (x) | | | | |
| R35 | Loi n° 2022-270 du 28 février 2022 (loi Lemoine) | | | | | | | x | | |
| R36 | C. consommation arts. L. 313-8 / L. 313-30 — TAEA, substitution | | | | | | | x | | |
| R37 | France Assureurs — *Statistiques Convention AERAS 2023* | | | | | | (x) | x | | |
| R38 | CGCT art. L. 2223-33-1 — funeral financing formulas | | | | | | | | x | |
| R39 | Loi n° 2014-617 du 13 juin 2014 (loi Eckert) | (x) | (x) | (x) | (x) | | (x) | | x | |
| R40 | CGI art. 125-0 A — taxation of life insurance products | x | x | x | | | | | | |
| R41 | CGI arts. 990 I and 757 B — death benefits | x | x | x | x | | (x) | | x | |
| R42 | CGI art. 163 quatervicies — PER deductibility | | | | x | | | | | |
| R43 | Institut des actuaires — NPA 1 (pratiques générales) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R44 | Institut des actuaires — NPA 2 (modèles actuariels) | x | x | x | x | x | x | x | x | x |
| R45 | IFRS 17 *Insurance Contracts* | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R46 | France Assureurs — l'assurance vie en 2025 | x | x | (x) | x | | | | | |
| R47 | France Assureurs — l'assurance vie en 2024 | x | (x) | (x) | (x) | | | | | |
| R48 | France Assureurs — l'assurance vie en unités de compte en 2025 | (x) | x | (x) | (x) | | | | | |
| R49 | France Assureurs — chiffres clés and the 2025 market review | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |

---

## 1. Prudential — Solvabilité II, the Code des assurances and supervision

(frlib-reg-r1)=

### R1. Directive 2009/138/CE — Solvabilité II

- **Publisher:** European Parliament and Council (EUR-Lex)
- **URL:** https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32009L0138
- **Accessed:** 2026-08-26
- **Fetched:** no (AWS WAF JavaScript challenge; a plain fetch returns HTTP 202 with an
  empty body, and a browser User-Agent gets the same challenge page)
- **Annotation:** The Level 1 directive establishing the risk-based prudential regime
  for EU insurance and reinsurance undertakings, and the instrument France transposes
  into the Code des assurances — which is why the French prudential rules a modeller
  reads are code articles, not directive articles. Its central rule for a cash flow
  model — technical provisions equal a **best estimate** (the probability-weighted
  average of future cash flows discounted at the relevant risk-free term structure)
  plus a **risk margin** — is stated here on EIOPA's authority [R4], not read from the
  directive text. The article numbers usually cited for that rule (Art. 76–86) are
  **[unverified]** in this library, and no Solvency II article number anywhere on this
  page was read from the instrument itself. Governs the valuation basis of all nine
  frlib products; the models produce the gross best-estimate cash flows and stop short
  of the discounting.

(frlib-reg-r2)=

### R2. Règlement délégué (UE) 2015/35

- **Publisher:** European Commission (EUR-Lex)
- **URL:** https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R0035
- **Accessed:** 2026-08-26
- **Fetched:** no (same AWS WAF JavaScript challenge as R1)
- **Annotation:** The Level 2 implementing measures for Solvabilité II. EIOPA confirms
  it was **adopted 10 October 2014 and published 17 January 2015**, and that it is
  "directly applicable" without national implementation [R4] — so a French insurer's
  contract-boundary and expense rules come from this regulation rather than from the
  Code des assurances. Everything a French modeller would actually look up in it —
  contract boundaries, expense assumptions, the cost-of-capital risk margin, the
  standard-formula sub-modules including mass lapse — could not be read here and is
  **[unverified]**. Consequence for this library: no cost-of-capital rate, no lapse
  shock and no expense-inflation rule rests on a retrieved text, and every such figure
  in a product document is `**[std]**`.

(frlib-reg-r3)=

### R3. Directive (UE) 2025/2 — the Solvency II review

- **Publisher:** European Parliament and Council (EUR-Lex)
- **URL:** https://eur-lex.europa.eu/eli/dir/2025/2/oj
- **Accessed:** 2026-08-26
- **Fetched:** no (AWS WAF JavaScript challenge; three URL forms tried — `/eli/`,
  `/legal-content/.../HTML/`, `/legal-content/.../PDF/`)
- **Annotation:** The amending directive from the 2019–2021 Solvency II review. Exactly
  one fact about it is verified: EIOPA's own framework page states that Directive (EU)
  2025/2 amends the Solvency II framework and that **the new rules take effect
  30 January 2027** [R4]. Everything else commonly reported — entry into force
  28 January 2025, a reshaped proportionality regime, sustainability and climate-risk
  requirements, new macroprudential tools, liquidity risk management plans, and changes
  to the risk margin and the volatility adjustment — comes only from search-result
  summaries and is **[unverified]**. Forward-looking for every product: none of the
  nine frlib models implements a 2027 basis, and none should be read as doing so.

(frlib-reg-r4)=

### R4. EIOPA — "Solvency II" (regulation and policy framework page)

- **Publisher:** European Insurance and Occupational Pensions Authority
- **URL:** https://www.eiopa.europa.eu/browse/regulation-and-policy/solvency-ii_en
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** The verified carrier for R1–R3, and the only Solvency II source on
  this page that was actually read. Verified directly: Directive 2009/138/EC was
  adopted November 2009 and "sets out requirements applicable to insurance and
  reinsurance companies in the EU with the aim to ensure the adequate protection of
  policyholders and beneficiaries"; Delegated Regulation (EU) 2015/35 was adopted
  10 October 2014, published 17 January 2015 and is directly applicable; the regime is
  organised in **three pillars** (I quantitative — valuation of assets and liabilities
  and capital requirements; II governance, risk management and ORSA; III supervisory
  reporting and public disclosure); the approach is described as market-consistent,
  risk-based and proportionate; EIOPA delivered its technical advice on the 2020 review
  on 17 December 2020; and Directive (EU) 2025/2 amends the framework with new rules
  taking effect **30 January 2027** [R4]. Cite this entry, not R1–R3, for any statement
  of Solvency II fact in a frlib product document.

(frlib-reg-r5)=

### R5. EIOPA — Risk-free interest rate term structures

- **Publisher:** EIOPA
- **URL:** https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified: EIOPA publishes the relevant risk-free interest rate (RFR)
  term structures **monthly**, as ZIP packages, so that technical provisions for
  (re)insurance obligations are calculated consistently across the EU. Each package
  contains the risk-free rates, the **volatility adjustment**, the **matching
  adjustment fundamental spreads** and the **ultimate forward rate (UFR)** used in the
  extrapolation; a release calendar is published (2026 dates listed include
  3 September, 5 October, 5 November, 3 December); *shifted* RFR term structures are
  published semi-annually for financial-stability reporting (option-adjusted duration);
  and EIOPA disclaims liability for reliance on the data [R5]. **No numeric curve
  values were extracted here** — the frlib models use flat or scenario discount rates
  marked `**[std]**`, and a reader wanting a market-consistent valuation takes the
  published cash flows and applies a curve from this source. Most material to the
  long-duration general-account books (AVE, EC, PER, RV, DEP).

(frlib-reg-r6)=

### R6. Code des assurances, art. R. 343-3 — the eleven life technical provisions

- **Publisher:** Légifrance (Direction de l'information légale et administrative)
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739686
- **Accessed:** 2026-08-26
- **Fetched:** yes (version in force since 1 January 2020)
- **Annotation:** The single most load-bearing French prudential article, and the reason
  a French model carries two liability measures rather than one. Verified: for life,
  *nuptialité-natalité* and capitalisation operations the article enumerates **eleven**
  technical provisions, each engagement being provisionable under exactly one of them —
  (1) **provision mathématique**, the difference between the actuarial present values of
  the insurer's and the insured's respective commitments, *including future management
  costs*; (2) **provision pour participation aux bénéfices (PPB)**, profit shares
  attributed but not payable immediately after the close of the year that produced them;
  (3) **réserve de capitalisation**; (4) **provision de gestion**; (5) **provision pour
  aléas financiers (PAF)** [R8]; (6) **provision pour risque d'exigibilité (PRE)**,
  detailed at art. R. 343-5 [R7]; (7) provision pour frais d'acquisition reportés;
  (8) provision pour égalisation, for mortality fluctuations on group death business;
  (9) **provision de diversification**, for art. L. 134-1 commitments where holders'
  rights are individualised — the eurocroissance vehicle [R19]; (10) **provision
  collective de diversification différée**; (11) **provision de garantie à terme**.
  Valuation follows standards set by the Autorité des normes comptables and by
  ministerial arrêté [R6]. Item 1 is why a French PM is *not* a pure net-premium
  reserve; items 9–11 exist only for eurocroissance.

(frlib-reg-r7)=

### R7. Code des assurances, art. R. 343-5 — provision pour risque d'exigibilité (PRE)

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030576275
- **Accessed:** 2026-08-26
- **Fetched:** yes (version in force since 1 January 2016)
- **Annotation:** Verified: the PRE is constituted when the investments listed at
  art. R. 343-10 — excluding amortisable securities the undertaking has the capacity and
  intention to hold to maturity — are in a position of **net overall unrealised
  depreciation**. The annual charge is **one third of that net overall unrealised
  depreciation**, provided the balance-sheet total of the provision does not exceed the
  depreciation itself. Valuation rules are specified: quoted securities at the **30-day
  average price** before the inventory date, fund units at the 30-day average redemption
  price, other assets per art. R. 343-11; unrealised gains and losses on derivatives
  whose underlyings are eligible assets are included, unrealised losses only above the
  value of collateral [R7]. Relevant to the general-account books that hold the exposed
  assets (AVE, EC, PER, RV); a frlib model does not compute a PRE, but a document
  describing a French euro fund's balance sheet has to name it.

(frlib-reg-r8)=

### R8. Provision pour aléas financiers — Code des assurances, art. A. 331-2 (abrogated 1 January 2016) and the arrêté du 23 décembre 2008

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006787843 (art.
  A. 331-2); https://www.legifrance.gouv.fr/loda/id/JORFTEXT000020009363 (arrêté du
  23 décembre 2008)
- **Accessed:** 2026-08-26
- **Fetched:** yes for the article (the version served runs 14 September 2014 to
  1 January 2016, the last text before the Solvency II recodification); partial for the
  arrêté (Légifrance served the metadata and the list of amended articles, not the
  substantive text)
- **Annotation:** Verified from the article: the PAF bites when the **real rate of return
  on the assets, reduced by one fifth** (i.e. 80 % of it) is **less than** the quotient
  of (total technical interest + the minimum contractually guaranteed participation aux
  bénéfices under art. A. 132-2 [R18]) divided by the **average mathematical
  provisions**. When it bites, the charge is the difference between (a) mathematical
  provisions recomputed by discounting future payments at one of three permitted rates —
  **60 % of the average State-borrowing rate (TME)**, a weighted average of rates by
  asset category, or a prudently estimated future asset yield — and (b) the mathematical
  provisions at the inventory date; the provision is **reversed at the following
  inventory** [R8]. From the arrêté: it amended A. 331-2 and created an *Annexe à
  l'article A. 331-2*, applicable to financial years opening on or after 1 January 2009.
  **Caveat, carried forward deliberately:** A. 331-2 was abrogated at the 1 January 2016
  recodification. The provision plainly survives — R. 343-3 5° still names the PAF [R6]
  and A. 341-1 4° still regulates a derogation for it [R9] — but the *current* article
  carrying the computation was not located, so the **article reference is
  [unverified]** for current dates even though the mechanics are recorded from a
  retrieved text. Cite the mechanics, not the article.

(frlib-reg-r9)=

### R9. Code des assurances, art. A. 341-1 — ACPR derogations, including the PAF forward-yield estimate

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031773094/2025-03-27
- **Accessed:** 2026-08-26
- **Fetched:** yes (version in force since 1 January 2016)
- **Annotation:** Verified: the ACPR may authorise an undertaking to depart from
  arts. R. 343-3 and R. 343-7 in four cases — (1) statistical methods to estimate claims
  of the last two financial years; (2) retaining a lower internal estimate of
  outstanding claims than the regulatory formula where based on sufficient information
  and reliable statistics; (3) modifying the parameters of the *provision pour risques
  en cours* where recent claims or pricing history justify it; and (4) **for the
  provision pour aléas financiers, estimating the future rate of return of the assets
  backing technical commitments**, which the ACPR authorises where it considers the
  estimate rests on sufficient information and a reliable and prudent method [R9]. This
  is the hook by which a French insurer's PAF becomes a forward-looking,
  supervisor-approved calculation rather than a mechanical one — background for the
  general-account products, and the reason a PAF figure cannot be reproduced from public
  information alone.

(frlib-reg-r10)=

### R10. Code monétaire et financier, art. L. 612-1 — the ACPR

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048029779/2023-09-01
- **Accessed:** 2026-08-26
- **Fetched:** yes (version 1 September 2023 – 18 October 2024)
- **Annotation:** The institutional frame. Verified: the **Autorité de contrôle
  prudentiel et de résolution (ACPR)** pursues two objectives — preserving the stability
  of the financial system and protecting the clients, *assurés*, *adhérents* and
  beneficiaries of the entities it supervises. It monitors compliance with EU law, the
  Code monétaire et financier, the **Code des assurances**, the Code de la sécurité
  sociale, consumer protection law and professional conduct codes; examines
  authorisation applications; exercises permanent off-site and on-site supervision;
  checks solvency and liquidity requirements and customer-protection measures; and runs
  banking and insurance crisis prevention and resolution. It holds control powers,
  administrative police powers and sanctioning powers, and its *collège de résolution*
  is France's national resolution authority [R10]. Cite-only for modeling purposes: it
  explains who enforces every prudential and conduct entry on this page, and — because
  the ACPR is attached to the Banque de France — why the HCSF surrender-freeze power
  [R13] is triggered on the proposal of the Governor.

(frlib-reg-r11)=

### R11. ACPR — *Analyses et Synthèses* on the life market (n° 179, n° 180 and n° 175)

- **Publisher:** ACPR / Banque de France
- **URL:** https://acpr.banque-france.fr/system/files/2026-06/20260630_AS180_revalorisation_2025.pdf
  (n° 180, "Revalorisation 2025 des contrats d'assurance-vie et de capitalisation", 19 pp.,
  PDF creation date 30 June 2026);
  https://acpr.banque-france.fr/system/files/2026-05/20260522_AS_Assurance_vie_2025.pdf
  (n° 179, "L'assurance-vie en 2025", 17 pp., 22 May 2026);
  https://acpr.banque-france.fr/system/files/2025-08/20250804_AS175_Revalorisation_contrats_assurance_vie_2024.pdf
  (n° 175, "Revalorisation 2024 …", 19 pp., 4 August 2025);
  https://acpr.banque-france.fr/fr/publications-et-statistiques/publications/ndeg-179-lassurance-vie-en-2025
  and https://acpr.banque-france.fr/fr/publications-et-statistiques/publications/ndeg-180-revalorisation-2025-des-contrats-dassurance-vie-et-de-capitalisation
  (landing pages)
- **Accessed:** 2026-08-26
- **Fetched:** **yes** — all three PDFs and both landing pages, retrieved with **`curl`**
  (HTTP 200, `application/pdf`, 1 062 381 / 1 985 804 / 1 193 221 bytes) and extracted
  locally with PyMuPDF. This host 403s the plain fetcher used for the rest of this page
  but serves `curl` identically with and without a browser User-Agent; see the correction
  in the header. **URL correction:** the n° 179 path previously recorded here
  (`/system/files/2026-03/20260326_AS_Assurance_vie_2025.pdf`) does not exist — the host
  returns 403, not 404, for a wrong `/system/files/` path — and has been replaced by the
  `2026-05` path that the n° 179 landing page itself links to. **Caveat on n° 175:** its
  page headers carry an **"ACPR-RESTREINT"** marking although it is served from the ACPR's
  public publications area; it is cited here only for 2024 comparatives that n° 180
  restates independently.
- **Annotation:** **The single most load-bearing quantitative source in this library, and
  it was recorded as unreachable in error.** n° 180 (Jean-Luc Coron with Frédéric Ahado)
  covers **116 organismes and 36 053 versions de contrats** over the art. A. 344-2
  categories 1, 2, 4, 5 (individual) and 7, 11, 12, 14 (collective); unit-linked supports
  are out of scope except in one box. It fixes the definitions the rest of this library
  uses: *taux de revalorisation* = "*rendement garanti et participation aux bénéfices
  techniques et financiers*" per arts. **L. 132-22 and A. 132-7**, gross of the technical
  rate and of tax and social levies but **net of the chargement sur encours**; *taux
  technique* = the maximum discount rate for the insurer's commitments, no charges applied,
  fixed at subscription and capped by A. 132-1 [R17], and a floor the served rate may not
  breach; *taux de chargement* = chargements de gestion over average mathematical
  provisions. **Verified figures.** Euro-support mathematical provisions **€1 207 bn**
  (individual, end-2025, +2.5 %) and **€154 bn** (collective, +4.7 %). Average **taux de
  revalorisation 2.63 % in 2025** for individual contracts, unchanged on 2024, and
  **2.64 %** collective (2.53 % in 2024); category 4 is about **92 %** of individual euro
  encours. Dispersion: undertakings holding **50 % of encours** credited between **2.3 %
  and 2.9 %** (2.2–3.0 % in 2024); **inside one insurer** the encours-weighted gap between
  the best- and worst-revalued homogeneous contract groups (90th vs 10th percentile) is
  **0.99 point** (0.77 in 2024) and the least-revalued group sits **0.39 point below the
  mean**, so a policyholder with no commercial bonus is credited at least that much below
  2.63 %; UC-holding bonuses run "*souvent de 100 points de base, et allant jusqu'à plus de
  200 points de base*". By type: bancassureurs **2.70 %** on 65 % of encours, assureurs
  traditionnels **2.48 %**, mutuelles **3.17 %**, ORPS **2.39 %**. Asset side: *taux de
  rendement de l'actif* **2.8 %** in 2025 (2.5 % in 2024, near 2.0–2.2 % 2020–2023), half
  of undertakings between 2.4 % and 3.3 %, **bonds about 60 %** of life investments and
  about **60 % of fixed-coupon bonds maturing within four years carrying a coupon below
  3 %**. **PPB as a percentage of life provisions**: individual **5.1 / 5.4 / 5.4 / 4.9 /
  4.3 / 4.0 %** for 2020–2025, collective **2.3 / 2.6 / 2.6 / 2.0 / 1.9 / 2.0 %**; end-2025
  bancassureurs 4.2 % against assureurs traditionnels 3.6 %. **Taux technique moyen**
  individual **0.39 / 0.37 / 0.36 / 0.37 / 0.35 / 0.32 %** and collective **1.24 / 1.21 /
  1.12 / 1.04 / 1.01 / 0.98 %** over the same years, with the ACPR noting that
  "*l'essentiel des contrats actuellement commercialisés en France a un taux technique
  faible ou nul*". **Taux de chargement sur encours** individual **0.63 %** (0.62 % in
  2024) and collective **0.47 %** (0.42 %), with half of all undertakings between **0.5 %
  and 0.8 %**. Footnote 12 restates the sharing rule from the supervisor's own pen:
  "*seulement 85 % du compte financier … lui est destiné pour sa revalorisation,
  directement ou par l'intermédiaire de la PPB. Certains contrats peuvent contractuellement
  prévoir un pourcentage plus élevé*" — confirming [R15] and confirming that a contractual
  uplift above 85 % is real. Encadré 2 quantifies the smoothing over 1999–2023: reserves
  **divide the volatility of credited rates by five** relative to markets and redistribute
  about **1.6 % of encours a year** between cohorts. From n° 179 (Jean-Luc Coron and
  Céline Yang, on the ACPR's weekly and quarterly collection from about 90 undertakings):
  2025 premiums **€159.1 bn**, benefits **€115.1 bn** of which surrenders **€71.0 bn**,
  **net inflow €44.0 bn** — the highest since the series began in 2011 — with euro
  supports **+€6.4 bn**, positive again after five consecutive years of net outflow, and UC
  **+€37.6 bn**; a **preliminary** 2025 euro revaluation estimate of **2.65 %**, which
  n° 180 later settles at 2.63 % for individual contracts. From n° 175, the 2024
  comparatives: individual **2.63 %** (2.60 % in 2023), collective 2.53 %, PPB **4.3 %**
  against **4.9 % end-2023**. **What this changes for the frlib models.** The market
  average crediting rate, its dispersion, the average euro-fund charge and the PPB ratio
  are now sourced and **no longer carry `**[std]**` or `[unverified]`** — cite this entry.
  What the series does **not** publish, and what therefore stays `**[std]**`, is any
  *named insurer's* crediting rate, TMG or charge scale, any insurer's PPB target and
  release policy, and the per-contract distribution behind the 0.99-point within-insurer
  gap. Relevant to the savings products (AVE, EC, PER, and AVUC through the *chargement
  sur encours*).

(frlib-reg-r12)=

### R12. ACPR — Recommandation 2024-R-03 du 21 novembre 2024 (devoir de conseil)

- **Publisher:** ACPR
- **URL:** https://acpr.banque-france.fr/system/files/2024-12/20241022_recommandation_2024-R-03_0.pdf
- **Accessed:** 2026-08-26
- **Fetched:** **yes** — with **`curl`** (HTTP 200, `application/pdf`, 895 713 bytes,
  9 pp., PDF creation date 12 December 2024), text extracted locally with PyMuPDF. The URL
  above was always correct; it is the plain fetcher used for the rest of this page that
  this host refuses. See the correction in the header.
- **Annotation:** Verified, read in full. Full title: *Recommandation 2024-R-03 du
  21 novembre 2024 sur le recueil des informations relatives au client pour l'exercice du
  devoir de conseil et la fourniture d'un service de recommandation personnalisée en
  assurance*, issued under **arts. L. 612-1 II 3° and L. 612-29-1 al. 2 CMF**. **The
  application date is confirmed:** its closing line reads "*La présente recommandation
  remplace la recommandation 2013-R-01 du 8 janvier 2013, modifiée le 21 février 2020, à
  compter du 31 décembre 2025*" — so the previously `[unverified]` **31 December 2025**
  date stands, and the superseded text is named. **The scope is confirmed and is wider
  than the earlier summary allowed:** it addresses all distributors under
  **art. L. 511-1 III** of the Code des assurances including those acting in France under
  freedom of services or establishment, and covers all insurance products, group or
  individual, excluding **grands risques** (art. L. 111-6), **contrats collectifs à
  adhésion obligatoire** *and all contracts taken out by employers for employees and former
  employees*, products no longer distributed without tacit renewal, and capitalisation or
  assurance-vie contracts with a surrender or transfer value that no longer accept
  versements or arbitrages. It continues **Recommandation 2024-R-01 du 28 juin 2024** on
  the DDA and is the current supervisory overlay on top of the abrogated
  art. L. 132-27-1 [R32]. **For a savings contract** (§ 2.1.3 and Annexe 1) the distributor
  should collect the family and professional situation — explicitly because it is needed
  to help draft the **clause bénéficiaire** — the financial situation sufficient to assess
  the **capacity to bear losses**, financial knowledge and experience, and the objectives
  and **investment horizon(s)**; the risk profile must be set objectively, illustrated with
  scenarios, and not derived from knowledge and experience alone (§ 2.1.3.6); sustainability
  preferences are collected under **art. L. 522-5** of the Code des assurances as defined
  at **art. 2 § 4 of délégué (UE) 2017/2359**, taking account of the **EIOPA** guidance
  (§ 2.1.3.7). At the point of sale the distributor should flag **all charges on the
  contract and the underlying options and their effect on past performance** (§ 2.1.8.4)
  and the **tax consequences of a surrender within eight years** and of premiums paid
  **after the subscriber's 70th birthday** (§ 2.1.8.5) — the supervisor treating the
  eight-year and age-70 boundaries [R40] [R41] as sales-critical — and, for a **PER**, the
  illiquidity of the savings, the early-release routes, the rente-versus-capital exit and
  its tax treatment, and the right to change profile, management mode or the minimum
  securitisation rhythm under **art. D. 224-3 CMF** (§§ 2.1.8.8–2.1.8.10). **Two numbers
  worth carrying.** § 2.3.1: for any capitalisation or assurance-vie contract with a
  surrender or transfer value, where there has been **no operation for 4 years** — or
  **2 years** where a personalised recommendation service was provided — the distributor
  should re-contact the holder and refresh every piece of collected information; **the
  first observation window opens 24 October 2024**, making the first contact due at the
  latest on **23 October 2028**, or **23 October 2026** in the personalised-recommendation
  case. Footnote 25, quoting **art. A. 522-2** of the Code des assurances, fixes what
  counts as a *significant* versement or arbitrage: **≥ €2 500 and ≥ 20 % of encours**
  where encours is below **€100 000**, **≥ €30 000 and ≥ 25 %** at or above it. On a
  surrender paired with a new subscription (§ 2.3.4) the distributor should compare
  "*engagements de taux, table de référence du contrat, impact de l'antériorité fiscale du
  contrat faisant l'objet du rachat*" — supervisory acknowledgement that a legacy
  guaranteed rate and a legacy mortality table have value to the policyholder — and
  § 2.3.8 makes clear that formalising advice may never push an operation past the
  regulatory settlement deadlines, so the two-month surrender cap of L. 132-21 [R31]
  survives intact. **Still unverified:** a joint ACPR/AMF text on customers' sustainability
  preferences reported for **13 November 2025** — this recommendation does not mention it
  (it points to the EIOPA guidance, not to a joint national text) and no such document was
  retrieved. Background for the advised-sale products; it shapes the sales process, not the
  cash flows.

(frlib-reg-r13)=

### R13. Haut Conseil de stabilité financière — Code monétaire et financier, art. L. 631-2-1 (loi Sapin 2, art. 49)

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034386882
- **Accessed:** 2026-08-26
- **Fetched:** yes (version dated 8 April 2017)
- **Annotation:** The French macroprudential tail risk that has no UK or US analogue, and
  the reason a French lapse-stress scenario is not just a multiplier. Verified: the
  **HCSF** defines macroprudential policy and holds seven powers, of which **5° ter**
  lets it, **on a proposal of the Governor of the Banque de France (chair of the ACPR)**
  and to prevent a "serious and characterised threat" to financial stability, take
  temporary protective measures against insurance undertakings — limit the acceptance of
  premiums; restrict the disposal of assets; **limit the payment of surrender values**;
  **defer or restrict arbitrages and advances**; and restrict dividends to shareholders
  or distributions to mutual members. Duration: **three months maximum, renewable** if
  the conditions persist (after consulting the advisory committee), with the restriction
  on surrender values capped at **six consecutive months**. The HCSF must balance
  financial stability against policyholders' interests, and its decisions are
  challengeable before the Conseil d'État [R13]. The mechanism has never been triggered
  **[unverified]** — the article does not say so. Load-bearing for any mass-surrender
  stress on the surrenderable savings contracts.

---

## 2. Participation aux bénéfices, guaranteed rates and eurocroissance

**Read this before citing anything in this section.** The French minimum profit share is
commonly mis-stated as "85 % of the technical result and 90 % of the financial result".
Verified against Légifrance it is the other way round, and it is not a clean 90 %: the
*compte de participation aux résultats* is credited with **85 % of the balance of the
compte financier** and with the balance of the *compte technique* **less the insurer's
own share**, that share being the **greater of 10 % of the credit balance and 4.5 % of
annual premiums** [R15]. The policyholder share of a technical credit balance is
therefore *at most* 90 %, and can be materially less on a small technical result
relative to premium.

(frlib-reg-r14)=

### R14. Code des assurances, art. L. 331-3 — the statutory obligation to share profits

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006798728/
- **Accessed:** 2026-08-26
- **Fetched:** yes, but the version served runs 1 July 1994 to 1 January 2016
  (transferred by loi n° 94-5 du 4 janvier 1994, art. 5)
- **Annotation:** The whole of the primary obligation, in one sentence of verified text:
  "*Les entreprises d'assurance sur la vie ou de capitalisation doivent faire participer
  les assurés aux bénéfices techniques et financiers qu'elles réalisent, dans les
  conditions fixées par arrêté du ministre de l'économie et des finances.*" The
  legislature mandates the sharing and delegates the mechanics to an arrêté — which is
  what arts. A. 132-10 to A. 132-17 [R15] [R16] are. Case law and parliamentary answers
  hold that no category of contract is carved out of the obligation *a priori*.
  **Caveat:** the displayed version ends 1 January 2016, the date the Solvency II
  recodification took effect; whether the obligation still sits at L. 331-3 or has moved
  to a Livre I article could **not** be confirmed here and is **[unverified]**. Product
  documents should cite this entry for the **substance** and must not assert a current
  article number. Applies across life and capitalisation business, most materially to
  the general-account savings products.

(frlib-reg-r15)=

### R15. Code des assurances, arts. A. 132-10 to A. 132-15 — the compte de participation aux résultats

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000031738019/
  (section index); individual articles at
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514666 (A. 132-10),
  .../LEGIARTI000038714192/2019-07-01 (A. 132-11), .../LEGIARTI000031772866 (A. 132-12),
  .../LEGIARTI000049818224 (A. 132-14), .../LEGIARTI000031757226 (A. 132-15)
- **Accessed:** 2026-08-26
- **Fetched:** yes, all six URLs (formerly A. 331-4 to A. 331-8, renumbered effective
  1 January 2016)
- **Annotation:** The arithmetic of the minimum PB, verified article by article.
  **A. 132-10** (version 7 September 2017): the minimum PB applies to life undertakings
  under art. L. 310-1 and to *fonds de retraite professionnelle supplémentaire* under
  art. L. 381-1, for individual and collective contracts of every kind; it is determined
  **globally, not contract by contract**; *contrats à capital variable* (unit-linked) are
  **excluded** from the A. 132-11 to A. 132-15 machinery. **A. 132-11** (version 1 July
  2019): the account is credited with the balance of a **compte technique** less the
  insurer's technical share — "*le montant le plus élevé entre 10 % du solde créditeur*"
  and **4,5 % des primes annuelles** — and with investment income "*égale à 85 % du solde
  d'un compte financier*" whose components are set by A. 132-13; the article is
  structured in four parts (general operations; operations with a *comptabilité
  auxiliaire d'affectation*; supplementary pension schemes; category-12 commitments).
  **A. 132-12**: the **minimum annual PB** is the credit balance of that account, and the
  minimum amount of benefits is that figure less interest credited to mathematical
  provisions, plus, where relevant, an amount reflecting the gap between guaranteed rates
  and the average rate served in the year; **art. L. 134-1 (eurocroissance) contracts are
  excluded**. **A. 132-14** (version 24 October 2024): the financial result credited is
  average technical provisions net of reinsurance cessions times a **taux de rendement
  des placements** (net investment income on life operations over average investments
  held in the year), computed separately for the three A. 132-11 categories.
  **A. 132-15**: a **solde de réassurance cédée** line enters the account. Load-bearing
  for every general-account product; a multisupport contract's euro compartment is in
  scope even though its UC compartment is not.

(frlib-reg-r16)=

### R16. Code des assurances, arts. A. 132-16 and A. 132-16-1 — the eight-year rule and the exceptional reprise

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801820 (A. 132-16);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042611504 (A. 132-16-1)
- **Accessed:** 2026-08-26
- **Fetched:** yes (A. 132-16 version 1 January 2020; A. 132-16-1 version 5 December 2020)
- **Annotation:** The single most modeling-relevant French discretionary-benefit
  constraint. Verified: **A. 132-16** requires sums entered into the *provision pour
  participation aux bénéfices* to be allocated to the *provision mathématique* or paid to
  policyholders "*au cours des huit exercices suivant*" the year in which they were
  credited — the **eight-year rule** that makes the PPB a smoothing buffer with a hard
  release horizon; the maximum is **fifteen years** for *fonds de retraite
  professionnelle supplémentaire* and for commitments under a *comptabilité auxiliaire
  d'affectation* per art. L. 142-4. **A. 132-16-1** permits an **exceptional reprise** of
  the PPB only where, cumulatively, the life technical account showed a **negative
  balance in the last financial year** *and* the solvency capital requirement (or minimum
  margin requirement) is **no longer covered**; it requires an ACPR-approved recovery plan
  providing for **restitution out of subsequent results within a maximum of eight years**
  and prohibiting dividends, redemption of certificates or other distributions until the
  amounts taken back are restored [R16]. A model that credits a rate without also
  modeling the PPB stock has not modeled a French fonds en euros: the crediting rate and
  the PPB allocation are one two-lever system, bounded below by R15 and above in time by
  this entry.

(frlib-reg-r17)=

### R17. Code des assurances, arts. A. 132-1 and A. 132-1-1 — taux d'intérêt technique maximal

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514601 (A. 132-1);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801948 (A. 132-1-1)
- **Accessed:** 2026-08-26
- **Fetched:** yes (A. 132-1 in force since 7 September 2017; A. 132-1-1 version
  1 January 2020)
- **Annotation:** The statutory ceiling on any guaranteed rate a French tariff may use.
  Verified: **A. 132-1** requires tariffs to be built on a rate at most equal to **75 % of
  the average rate of French State borrowings (taux moyen des emprunts d'État, TME)
  computed on a semi-annual basis**, without exceeding, **beyond eight years**, the lower
  of **3.5 %** and **60 % of that average rate**; for contracts with **periodic premiums**
  or **variable capital**, whatever their duration, the rate cannot exceed the lower of
  **3.5 %** and **60 %** of the same average. For foreign-currency contracts the reference
  is that country's long-term State borrowing rate on the same basis. Rates in force at
  subscription apply, and non-scheduled contributions are re-tested at each payment; the
  article does not apply to collective insurance operations. **A. 132-1-1** fixes the
  mechanics: the *taux de référence* is the six-month arithmetic mean of rates observed on
  the primary and secondary markets for State borrowings on a semi-annual basis,
  multiplied by **60 %** or **75 %**; the maximum technical rate moves on a **0.25-point
  grid floored at zero**, and does **not** change while the monthly reference rate has not
  **fallen by at least 0.10 point** or **risen by at least 0.35 point** relative to the
  rate in force; when a threshold is crossed the new maximum is the grid rate immediately
  below the reference rate, and undertakings have **three months** to implement the
  change [R17]. Binding on every contract with a guaranteed technical rate; over an
  annuity's or a dependency rente's duration the binding limb is normally
  **min(3.5 %, 60 % of TME)**.

(frlib-reg-r18)=

### R18. Code des assurances, arts. A. 132-2 and A. 132-3 — taux minimum garanti (TMG)

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514622 (A. 132-2);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514611 (A. 132-3, current);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006786141/2007-05-02
  (A. 132-3, version 2 May 2007 – 1 August 2010)
- **Accessed:** 2026-08-26
- **Fetched:** yes, all three (A. 132-2 and current A. 132-3 both dated 7 September 2017)
- **Annotation:** Verified. **A. 132-2**: undertakings and FRPS may "*garantir dans leurs
  contrats un montant total d'intérêts techniques et de participations aux bénéfices*"
  which, related to the fraction of mathematical provisions the guarantee bites on, is not
  below the minima fixed under A. 132-3. Note the construction, which models get wrong:
  what is guaranteed is **technical interest *plus* PB**, expressed as a rate on the
  mathematical provision — the TMG is not a separate credit stacked on the technical
  rate. **A. 132-3 II**: guaranteed rates are **expressed on an annual basis** and fixed
  for a continuous period of **at least six months and at most the period from the
  guarantee's effective date to the end of the following financial year** (in practice up
  to about eighteen months). **A. 132-3 III**: such rates may not exceed the **minimum of
  (a) 150 % of the maximum technical rate defined at A. 132-1/A. 132-1-1 on the 75 %-TME
  reference at the effective date** and (b) **the higher of 120 % of that maximum
  technical rate and 110 % of the average rates served over the two preceding financial
  years**. **A. 132-3 IV**: a newly licensed undertaking may, until the close of the
  second financial year after authorisation, offer rates not exceeding **120 %** of the
  maximum technical rate. **Two extraction gaps, recorded rather than papered over:**
  paragraph I's ceiling is a *difference* whose first limb is "*80 % du produit de la
  moyenne des taux de rendement des actifs*" and whose **second limb the fetcher did not
  return**; and limb (b) of paragraph III comes from the fetched page's structured
  summary rather than a verbatim quote. Both should be re-read before use in a live
  pricing decision — **[unverified]** as verbatim text. Historic comparison (version
  2 May 2007 – 1 August 2010): the older text capped an annual minimum rate at **85 % of
  the average asset yield over the two preceding financial years**, limited the guarantee
  to **eight years**, and required a two-year average asset yield of at least **4/3** of
  the first-year minimum rate for new business — anyone quoting "85 % of the average asset
  yield" for a TMG is quoting superseded law. No public figure exists for what any
  individual insurer actually sets as its TMG, so every modelled TMG is `**[std]**`.

(frlib-reg-r19)=

### R19. Code des assurances, art. L. 134-1 and arts. R. 134-1 to R. 134-12 — eurocroissance

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611220 (L. 134-1);
  https://www.legifrance.gouv.fr/codes/id/LEGISCTA000039739657 (chapter R. 134-1 to
  R. 134-12); https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739643 (R. 134-4)
- **Accessed:** 2026-08-26
- **Fetched:** yes (L. 134-1 version 24 May 2019; R. 134-4 version 1 January 2020)
- **Annotation:** The legal basis of the third French savings compartment. Verified:
  **L. 134-1** lets life undertakings write commitments in case of life or death —
  **excluding temporary death cover** — which give rise to a **provision de
  diversification** intended to absorb fluctuations of the backing assets; the guaranteed
  benefit may be a **rente** or a **capital at maturity**; two contractual shapes are
  permitted, the benefit expressed partly in euros and partly in units of the provision de
  diversification, or expressed **solely in units of that provision before maturity with a
  euro-denominated guarantee at maturity**. A single premium may accordingly give rise to
  **three kinds of engagement** — *en euros*, *en unités de compte*, and giving rise to a
  provision de diversification — which is the legal basis for a three-compartment
  multisupport contract. From the chapter: R. 134-1 capital guarantee limits and the
  minimum value of the provision; **R. 134-2** individualisation of rights in *parts de
  provision de diversification* (units = total provision ÷ a common per-unit value);
  R. 134-3 permitted deductions; **R. 134-4** the participation account; **R. 134-5** the
  surrender and transfer value, fixing that the relevant duration "**cannot exceed the
  shorter of the guarantee maturity and eight years**"; R. 134-6 settlement at maturity
  and conversion into an annuity; R. 134-8 asset valuation at realisation value per
  R. 343-11 and R. 343-12; R. 134-10 pre-sale disclosure; **R. 134-12** asset transfers
  and reallocation, capped at **10 % of the amount of the provision de diversification**.
  R. 134-4 itself directs the credit balance of the participation account to three
  destinations — revaluing guaranteed benefits, crediting the provision de diversification
  (new units or a higher unit value), and funding the **provision collective de
  diversification différée** — and permits a deficit to be absorbed from that deferred
  reserve or by reducing the unit value within limits. **No percentages and no statutory
  time limits appear in the article**: the split is discretionary, and any modelled split
  is `**[std]**`.

(frlib-reg-r20)=

### R20. Décret n° 2019-1437 du 23 décembre 2019 — the eurocroissance reform under loi PACTE

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/eli/decret/2019/12/23/ECOT1930053D/jo/texte
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified: the décret implements the loi PACTE eurocroissance reform,
  replacing Chapitre IV of Titre III, Livre I of the Code des assurances. It restates the
  maturity guarantee as the sum of the *provision mathématique* and the value of the
  holder's share of the *provision de diversification*, with a minimum guarantee level set
  by decree; confirms the R. 134-5 rule that the relevant duration cannot exceed the
  shorter of the guarantee maturity and **eight years**; sets out the *provision collective
  de diversification différée* mechanics (revaluation of PM or PD at any time; absorption
  of debit balances by reprise or by reducing the unit value, within limits); and requires
  transfers of assets into a *comptabilité auxiliaire d'affectation* to be matched by
  reciprocal transfers of equal value under R. 343-11 and R. 343-12. **Entry into force
  1 January 2020**; existing contracts stay under the prior rules, and new contracts on
  the old basis could be written until **1 October 2020** [R20]. A widely repeated claim
  that the reform pushed the compulsory restitution of diversification provisions from
  eight to fifteen years appears only in secondary commentary and is **[unverified]**.

---

## 3. Mortality, morbidity and public statistics

(frlib-reg-r21)=

### R21. Arrêté du 1er août 2006 — homologation of TGH05 / TGF05 (annuity tables)

- **Publisher:** Légifrance (Journal officiel)
- **URL:** https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000820127
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified: the arrêté homologates two **generational annuity tables
  applicable from 1 January 2007** — **TGF05** for female lives and **TGH05** for male
  lives — replacing the generational table homologated in 1993. It amends a long list of
  Code des assurances articles including **A. 132-1, A. 132-4, A. 132-6, A. 160-2,
  A. 160-4, A. 310-1, A. 331-1-1, A. 331-1-2, A. 331-9-1, A. 332-7, A. 335-1 and
  A. 441-4-1**, covering euro conversion, life contract provisions, annuity thresholds and
  mortality-table application. Most provisions took effect on publication (**26 August
  2006**); article 4 defers the unit-linked and participation distribution provisions to
  **1 January 2007**, aligning with the new tables. The tables apply to annuity contracts
  subscribed **from 1 January 2007**; for older contracts, undertakings had to hold minimum
  reserves on the 1993 table until **1 August 2008** [R21]. **The tables themselves are not
  reproduced in this library** — they are cited by name and arrêté, and the frlib decrement
  CSVs are `**[std]**` proxies built from INSEE data [R24]. Primary for rente-viagere;
  reached by per-assurance and dependance through the annuity in payment, and by the
  savings products through an annuity conversion option.

(frlib-reg-r22)=

### R22. Arrêté du 20 décembre 2005 — homologation of TH 00-02 / TF 00-02 (non-annuity tables)

- **Publisher:** Légifrance (Journal officiel)
- **URL:** https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000636581
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified: homologates **TH 00-02** for male insureds and **TF 00-02** for
  female insureds, and carries forward **TD 88-90** and **TV 88-90** from the 1993 arrêté.
  TH 00-02 and TF 00-02 apply to "*contrats autres que de rente viagère*" — everything that
  is not a life annuity. For annuity contracts, undertakings may use homologated tables or
  their own experience data, with specific provisions on anti-selection; for non-annuity
  life contracts the arrêté permits adjusting the insured's age by the **décalage d'âge**
  (age shift) schedules annexed to each table [R23]. **In force 1 January 2006**, except the
  annuity-calculation provisions, in force **1 July 2006** [R22]. The reference basis for
  temporaire-deces, assurance-emprunteur (death and PTIA), obseques, the death benefit
  inside a euro contract, and the healthy-life mortality leg of a dependency model — again
  cited by name, never shipped.

(frlib-reg-r23)=

### R23. Code des assurances, art. A. 335-1 and its Annexe — which table applies to what

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000026806627 (A. 335-1);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019265297 (Annexe)
- **Accessed:** 2026-08-26
- **Fetched:** yes for both, but Légifrance served the article as version 21 December 2012
  to 1 January 2016 and the annexe as version 26 August 2006 to 1 January 2016 even when a
  current-date URL suffix was supplied; the **current placement of these provisions after
  the Solvency II recodification is [unverified]**
- **Annotation:** The article that decides which mortality basis a French tariff may use,
  and the one that makes *tables d'expérience* legal and, in the same breath, non-public.
  Verified: life and capitalisation tariffs comprise the undertaking's remuneration and are
  built on (i) a **taux d'intérêt technique** fixed per art. A. 132-1 [R17] and (ii)
  mortality tables, of which there are exactly **two permitted kinds** — **(a)** tables
  homologated by ministerial arrêté, **by sex**, established on insured populations for
  annuity contracts and on **INSEE** data for other contracts; or **(b)** tables established
  by the undertaking itself and **certified by an actuary independent of that undertaking,
  approved for the purpose by one of the actuarial associations recognised by the
  supervisor**, built on the undertaking's own experience data or on demographically
  equivalent data. Further verified rules: where one homologated table is used for all
  insureds it must be the sex-appropriate table producing the **most prudent** rate; for
  non-annuity survival contracts the homologated tables are applied with the annexed
  **age shifts**; for annuity contracts, **rates computed on experience tables may not be
  lower than those from the appropriate homologated tables by sex** — an explicit floor that
  caps the pricing benefit of an experience table; and a *forfait* method is permitted for
  collective annually renewable death contracts where justifiable. The **Annexe** contains
  **TF 00-02** and **TH 00-02** (ages 0–112, tabulated as $l_x$) and **TD 88-90** (ages
  0–106), plus two **décalage d'âge** schedules — TF 00-02 from **−11 years at ages 16–32**
  to **0 at age 94+**, TH 00-02 from **−13 years at ages 16–38** to **−3 at age 75+**.
  Load-bearing for all nine products.

(frlib-reg-r24)=

### R24. INSEE — Données nationales : mortalité, espérance de vie

- **Publisher:** Institut national de la statistique et des études économiques
- **URL:** https://www.insee.fr/fr/statistiques/8210111
- **Accessed:** 2026-08-26
- **Fetched:** yes (page publication date 15 July 2024)
- **Annotation:** The only freely redistributable French mortality series, and therefore the
  actual data source behind every decrement CSV this library ships. Verified: the page
  offers, in Excel files from 24 KB to 451 KB plus a full zip archive, **T69QMORT**
  (*quotients de mortalité pour 100 000 survivants à l'âge indiqué*), **T69SUR** (survivors
  per 100 000 live births), **T69ESP** (*espérance de vie par âge détaillé*), **T67**
  (mortality rates by sex and age group), **T68** (triennial tables) and **T70** (infant
  mortality); annual series run from **1946 for metropolitan France and 1994 for France as
  a whole**, the triennial tables from **1977** and **1999** respectively [R24]. The page
  does not state licence or reuse conditions; standard INSEE open-data terms are assumed and
  that assumption is **[unverified]** — confirm before redistributing derived CSVs. The
  frlib decrement tables are `**[std]**` proxies built from this series and anchored so that
  each product's best-estimate factor reproduces its own technical-notes placeholder
  exactly; TH 00-02 / TF 00-02 / TGH05 / TGF05 are cited by name and article
  [R21] [R22] [R23] but never shipped.

(frlib-reg-r25)=

### R25. DREES — *Études et Résultats* n° 1327, February 2025 (APA over the retirement lifetime)

- **Publisher:** Direction de la recherche, des études, de l'évaluation et des statistiques;
  author Patrick Aubert (Institut des politiques publiques)
- **URL:** https://drees.solidarites-sante.gouv.fr/sites/default/files/2025-02/ER%201327%20EDRAPA_MEL.pdf
- **Accessed:** 2026-08-26
- **Fetched:** yes (PDF downloaded, text extracted locally with PyMuPDF)
- **Annotation:** The public incidence-and-duration study a French dependency model has to
  calibrate against, built on the 2016 *échantillon interrégimes de retraités* matched to
  2017 APA/ASH individual records, on 2017 mortality and take-up conditions. Verified
  headline results: a retiree can expect **25.1 years** of retirement, of which **2.4 years**
  receiving the *allocation personnalisée d'autonomie* (**9.6–10 %** of the retirement
  period) — **3.3 years and 12 %** for women, **1.4 years and 6 %** for men; **57 % of
  retirees would receive APA at some point** (**69 %** of women, **44 %** of men), and
  separately **47 % of women and 29 % of men** for APA at home, **46 % and 24 %** in an
  institution. Among beneficiaries, expected APA duration is about **2.9 years** for men at
  home and **3.2 years (women) / 2.3 years (men)** in an institution. Mean age at entry into
  APA at home runs from **80.1 years** for men in the lowest pension quintile to **86.0
  years** in the highest — a **5.9-year** gradient overall, **7.5 years** for home APA and
  **3.4 years** among women. GIR is used throughout as the dependency scale (GIR 1 most
  dependent, GIR 6 most autonomous; GIR 1–4 confers entitlement) [R25]. Primary for
  dependance; longevity context for rente-viagere and per-assurance.

(frlib-reg-r26)=

### R26. CNSA — *Les chiffres clés de l'aide à l'autonomie 2024*

- **Publisher:** Caisse nationale de solidarité pour l'autonomie
- **URL:** https://www.cnsa.fr/sites/default/files/2024-06/PUB-CNSA_Chiffres_cles_2024_Access-01.pdf
- **Accessed:** 2026-08-26
- **Fetched:** yes (28 pp., created 20 June 2024; PDF downloaded, text extracted locally
  with PyMuPDF)
- **Annotation:** The public benefit scale and the GIR mix — the natural anchors for a
  dependency-rente benefit design. Verified: CNSA devotes **€40.6 bn** to *aide à
  l'autonomie* in 2024; at December 2022 there were **1.3 million APA beneficiaries**, of
  which **794 000 at home** and **542 500 in an institution**, being **7.2 %** of the
  60-and-over population (estimated at **18.4 million**). **GIR distribution of APA
  beneficiaries in 2022** — *at home*: GIR 1 **2 %**, GIR 2 **18 %**, GIR 3 **22 %**, GIR 4
  **58 %**; *in an institution*: GIR 1 **13 %**, GIR 2 **44 %**, GIR 3 **19 %**, GIR 4
  **24 %**. **Monthly APA-at-home ceilings for 2024**: GIR 1 **€1 955.60**, GIR 2
  **€1 581.44**, GIR 3 **€1 143.09**, GIR 4 **€762.87**. Entitlement is assessed on the
  **grille AGGIR**; only GIR 1–4 qualify; the amount depends on GIR, income and the cost of
  the care plan. Net *aide sociale* spending on older people was **€8.2 bn** in 2022 [R26].
  Primary for dependance.

(frlib-reg-r27)=

### R27. DREES — *Études et Résultats* n° 1101, 31 January 2019 (people covered by private insurers, by social risk)

- **Publisher:** DREES; authors Alexis Montaut and Raphaële Adjerad
- **URL:** https://drees.solidarites-sante.gouv.fr/publications/etudes-et-resultats/premiere-estimation-du-nombre-de-personnes-couvertes-par-les
- **Accessed:** 2026-08-26
- **Fetched:** yes (landing page and abstract)
- **Annotation:** Verified: the first estimate, on **2016** data, of the number of people
  covered by complementary insurers by social risk — **23–30 million** covered for
  invalidity (0.3–0.4 million receiving benefits), **10.4 million** for supplementary
  retirement (2.2 million receiving), and **4.8 million** covered for **dépendance** as a
  principal protection; in 2016 complementary bodies collected **€70 bn** in contributions
  and paid **€51 bn** of social-risk benefits, and multi-coverage materially widens the
  invalidity estimates [R27]. Background market-sizing and take-up context for the
  protection products; superseded on the dependency numbers by R28, which is both more
  recent and more granular.

(frlib-reg-r28)=

### R28. Institut des actuaires — atelier technique "Assurance dépendance : état des lieux, solutions assurantielles et innovations pour le bien-vieillir" (24 November 2025)

- **Publisher:** Institut des actuaires (presenters A. Treilhou, S. Ayadi, A. Petit,
  V. Touzé)
- **URL:** https://www.institutdesactuaires.com/global/gene/link.php?doc_id=20056&fg=1
- **Accessed:** 2026-08-26
- **Fetched:** yes (37-slide PDF downloaded, text extracted locally with PyMuPDF;
  chart-only values were not transcribed and are not cited)
- **Annotation:** By some distance the densest public source available for French dependency
  insurance, and the only one that gives a real benefit design. Verified **market, 2024**:
  **2.4 million people** insured against the dependency risk through insurance undertakings
  (**−6.9 %** on 2023), of which contracts where dependency is the *principal* guarantee
  represent **58 %**; **€618.1 m** of premiums (**−3 %**), **88 %** on
  principal-and-only guarantees; for those contracts the **average annual premium is €472
  individual and €106 collective**, the **average age at subscription is 64**; **€357.3 m**
  of benefits paid (**+6.3 %**); **€6.4 bn** of provisions at 31 December 2024 (**−1.9 %**);
  **41 900 annuities in payment** with an **average monthly annuity of €583**; **28 400 new
  contracts** (**−13.7 %**). Across all bodies, **6.0 million** people were insured in 2024
  (**56 % mutuelles, 40 % insurance undertakings, 4 % institutions de prévoyance**).
  Verified **product design** (the OCIRP points-based collective contract, a real market
  design): contributions of **0.40 % to 1.50 % of the PMSS** buy *points de rente
  dépendance*; a minimum guaranteed monthly annuity of **€200 to €750** for **total
  dependency (GIR 1–2)** and **50 % of it, €100 to €375**, for **partial dependency
  (GIR 3)**; a **0.60 % PMSS** compulsory base plus a **0.40 % PMSS** option
  (**€15.70/month in 2025**) lifts the GIR 1–2 minimum by €200 to **€500** and the GIR 3
  minimum by €100 to **€250**. Verified **claim definition**: automatic recognition where
  APA is in payment for GIR 1–2; otherwise certification by the insurer's medical officer, a
  state of dependency lasting **more than three months**, and inability to perform **2 or 3
  of the 4 *actes de la vie courante***. Verified **behaviour and pricing**: continuation
  after leaving the employer without medical selection at the same tariff **within six
  months**, and **no reduction value** — the guarantee is maintained for life even if
  contributions stop; the *valeur d'acquisition* scale requires **two series per age**,
  mortality of the generation (healthy and future disabled) and future prevalence of
  disability in the generation, and is more sensitive to the technical rate the younger the
  insured; individual contracts show subscription ages **60–75**, no medical selection and
  no guaranteed minimum annuity [R28]. **No public French incidence table by age and GIR
  exists**, so every frlib incidence rate is `**[std]**`, calibrated against the prevalence
  and duration figures here and in R25/R26.

---

## 4. Conduct, contract information and distribution

(frlib-reg-r29)=

### R29. Code des assurances, arts. L. 132-5-1 and L. 132-5-2 — renonciation

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731314 (L. 132-5-1);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731328 (L. 132-5-2)
- **Accessed:** 2026-08-26
- **Fetched:** yes (both in force since 1 April 2018)
- **Annotation:** Verified. **L. 132-5-1**: any natural person who has signed a proposal or a
  life insurance or capitalisation contract may renounce by registered letter or registered
  electronic mail with acknowledgement of receipt within **thirty full calendar days from
  the moment they are informed that the contract is concluded**; the deadline expires at
  midnight on the last day and is **not** extended if it falls on a weekend or public
  holiday; the undertaking must repay **all sums paid** within **thirty full calendar days
  of receipt** of the notice, and unrepaid sums bear interest automatically at **1.5 × the
  legal rate for two months**, then at **twice the legal rate**; the right does not apply to
  contracts with a maximum duration of two months. **L. 132-5-2**: before conclusion the
  insurer must hand over a *note d'information*, or the proposal/contract may itself serve as
  that note where it carries the **encadré** [R30] at its head, and the document must include
  "*un modèle de rédaction destiné à faciliter l'exercice de la faculté de renonciation*";
  the **sanction** for non-delivery is that the renunciation period runs to the thirtieth
  calendar day after actual delivery, **capped at eight years** from the date the subscriber
  is informed the contract is concluded [R29]. Load-bearing for the savings products, where a
  thirty-day unwind is a real first-duration lapse effect; assurance emprunteur follows the
  consumer-credit regime instead [R35] [R36].

(frlib-reg-r30)=

### R30. Code des assurances, arts. A. 132-4 and A. 132-8 — note d'information and the *encadré*

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046824912 (A. 132-4);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031773778 (A. 132-8)
- **Accessed:** 2026-08-26
- **Fetched:** yes (A. 132-4 version 1 January 2023, modified by the arrêté du 22 décembre
  2022; A. 132-8 version 1 January 2016)
- **Annotation:** The two articles that decide what a French product document must disclose —
  and therefore what a reference product specification can legitimately claim to know.
  Verified: **A. 132-4** and its annexe prescribe the **note d'information** in five blocks —
  (1) identification of contract and insurer; (2) contract characteristics, including the
  definition of the guarantees, duration, premium arrangements, "*délai et modalités de
  renonciation au contrat*", claims procedure and specifics for life, unit-linked and group
  contracts; (3) **guaranteed return and participation aux bénéfices**, covering guaranteed
  interest rates and their duration, reduction, surrender and transfer values, and the method
  of calculating and allocating PB; (4) complaints handling and any mediation body; (5)
  reference to the SFCR where applicable. **A. 132-8** prescribes the **encadré** at the head
  of the proposal, draft contract or notice, **not exceeding one page**, in eight sections in
  fixed order: (1) type of contract; (2) the guarantees with clause references, and for
  unit-linked a prominent statement that the amounts invested are **not guaranteed and are
  subject to market fluctuations**; (3) participation aux bénéfices and the applicable
  percentages; (4) surrender and transfer availability and the payment period; (5) **fees in
  four categories** — entry and premium charges, recurring annual charges, exit charges, and
  other charges — **with maximum amounts or percentages**; (6) recommended holding duration
  in prescribed wording; (7) beneficiary designation; (8) a closing disclaimer [R30]. Note
  what this does *not* do: it requires maxima to be disclosed, not levels to be capped. No
  statutory ceiling on any French life charge appears in the retrieved texts, which is why
  every charge level in an frlib model is `**[std]**`.

(frlib-reg-r31)=

### R31. Code des assurances, arts. L. 132-21, L. 132-22 and L. 132-23-1 — surrender, annual information, payment on death

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030461815 (L. 132-21);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048252743 (L. 132-22);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611225 (L. 132-23-1)
- **Accessed:** 2026-08-26
- **Fetched:** yes (L. 132-21 version 1 January 2016; L. 132-22 version 24 October 2024;
  L. 132-23-1 version 24 May 2019)
- **Annotation:** Verified. **L. 132-21**: the contract must state how the **valeur de
  rachat**, the **valeur de transfert** and the **valeur de réduction** are computed;
  reduction penalties may not be charged directly against the mathematical provision; the
  insurer may grant **avances** up to the surrender value; a requested surrender must be paid
  within **two months** at most, with late payment bearing interest at **1.5 × the legal rate
  for two months** then **twice the legal rate**. **L. 132-22**: the annual statement must
  give the surrender value (or transfer value for professional retirement contracts), the
  reduction value where relevant, guaranteed capital amounts, the premium, "*le rendement
  garanti et la participation aux bénéfices techniques et financiers*", the average
  guaranteed return and PB rates for comparable contracts open and closed to new business,
  the ESG dimension of the investment policy, the **average asset yield for the contract
  category**, and, for unit-linked, unit values and charges; the insurer must **publish on
  its website within 90 business days of 31 December** the average guaranteed returns,
  average charge rates, the **average net return served to policyholders**, tax and
  social-contribution rates and average PB rates, contract by contract, keeping the
  information online for at least **five years**; unit-linked and art. L. 134-1 information
  is updated at least **quarterly**, and a specific statement is due **one month before** a
  contract's term. **L. 132-23-1**: on being notified of the death and having identified the
  beneficiary, the insurer has **fifteen days** to request the documents needed for payment
  and must pay within **one month** of receiving the complete file; overrun of the
  fifteen-day step triggers **twice the legal rate for one month then three times**, overrun
  of the payment deadline **twice the legal rate for two months then three times**, with the
  initial fifteen days counting toward that calculation; the insurer may not ask twice for
  the same document [R31]. The two-month surrender settlement and the death-payment clock are
  real timing items for a monthly model; the obseques revaluation between death and payment
  hangs off L. 132-23-1 [R38].

(frlib-reg-r32)=

### R32. Devoir de conseil — Code des assurances art. L. 132-27-1 (abrogated) and Directive (UE) 2016/97 (DDA)

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000020195154/2026-07-01
  (L. 132-27-1); https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000031967447 (Directive
  (UE) 2016/97, Légifrance landing page)
- **Accessed:** 2026-08-26
- **Fetched:** yes for the article (version 1 July 2010 – 1 October 2018, since abrogated);
  partial for the directive (Légifrance serves only a metadata landing page pointing to
  EUR-Lex, and EUR-Lex is blocked — see R1)
- **Annotation:** Verified from the article: the pre-DDA French *devoir de conseil* required
  the insurer, before concluding an individual life contract with surrender values or a
  capitalisation contract, to specify the requirements and needs expressed by the subscriber,
  record their financial situation and objectives and the reasons motivating the advice given
  on a particular contract, and "*s'enquiert auprès du souscripteur … de ses connaissances et
  de son expérience en matière financière*"; where the customer withheld the information the
  insurer had to warn them before conclusion, and the advice had to be adapted to the
  complexity of the contract; it did not apply where an intermediary under art. L. 511-1
  presented the contract. This abrogated text is retained here because it is what most French
  product literature still paraphrases. Verified from the Légifrance landing page for the
  DDA: **entry into force 22 February 2016**, **transposition deadline 23 February 2018**,
  repealing Directive 2002/92/CE with effect from 23 February 2018; France transposed by
  **ordonnance n° 2018-361 du 16 mai 2018** and **décret n° 2018-431 du 1er juin 2018**, in
  force **1 October 2018** (some provisions 23 February 2019). The **substantive** DDA
  requirements — the definition of insurance distribution, the IPID, the demands-and-needs
  test, the appropriateness and suitability tests for insurance-based investment products,
  remuneration and conflicts of interest, and the Code des assurances Livre V articles
  L. 521-1 ff. and L. 522-1 ff. that replaced L. 132-27-1 — **were never read** and are all
  **[unverified]**. Conduct background across the advised-sale products; no cash flow
  consequence.

(frlib-reg-r33)=

### R33. PRIIPs — Règlement (UE) n° 1286/2014 and AMF Position-recommandation DOC-2011-05

- **Publisher:** European Parliament and Council (EUR-Lex); Autorité des marchés financiers
- **URL:** https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32014R1286 (PRIIPs);
  https://www.amf-france.org/sites/institutionnel/files/private/2023-02/DOC-2011-05_VF14_PRIIPs.pdf
  (AMF DOC-2011-05)
- **Accessed:** 2026-08-26
- **Fetched:** no for the regulation (EUR-Lex AWS WAF challenge, as R1); yes for the AMF
  document (PDF downloaded, 44 pp., "Document créé le 18 février 2011, modifié le 16 février
  2023")
- **Annotation:** This is where the AMF's shared conduct competence over unit-linked business
  actually bites: French UC supports are overwhelmingly wrapped around collective vehicles the
  AMF regulates, so the disclosure attaching to a *unité de compte* is governed by AMF
  doctrine as much as by insurance law. Verified from the AMF document: DOC-2011-05, *Guide
  des documents réglementaires des OPC*, cites as its reference texts **article 78 of
  Directive 2009/65/CE, Regulation 583/2010, Règlement (UE) n° 1286/2014, Règlement délégué
  (UE) 2017/653** and articles 411-106 to 411-120 and 422-67 to 422-78 of the AMF General
  Regulation; it applies to OPCVM, general-purpose investment funds, private-equity funds,
  OPCI, funds of alternative funds, professional funds and employee-savings funds, and governs
  the **DICI** and the **DIC (KID)** for those vehicles — naming, investment objective and
  policy, **risk and reward profile**, **charges**, past performance, practical information
  and formula funds [R33]. The **insurance-side** PRIIPs mechanics — the SRI 1–7 summary risk
  indicator, the four performance scenarios, the RIY cost measure and the recommended holding
  period, all set by Règlement délégué (UE) 2017/653 — could not be read from a retrieved text
  and are **[unverified]** here. Primary for assurance-vie-uc; reaches the other savings
  products through their UC compartments.

---

## 5. Legislation and tax — retirement, borrower insurance, obsèques and the CGI

(frlib-reg-r34)=

### R34. Loi PACTE art. 71 and Code monétaire et financier arts. L. 224-1 to L. 224-8 — the PER

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000038496266 (loi
  n° 2019-486 du 22 mai 2019, art. 71);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038507575 (CMF L. 224-1);
  https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000038507459/2019-10-23/
  (section L. 224-1 to L. 224-8)
- **Accessed:** 2026-08-26
- **Fetched:** yes, all three (L. 224-1 version 1 October 2019)
- **Annotation:** The constitutive text of the French retirement savings plan, verified
  article by article. **Art. 71 of the loi PACTE** creates the **plan d'épargne retraite
  (PER)** as a new Chapitre IV of Livre II, Titre II of the CMF, in force at a date fixed by
  decree and no later than 1 January 2020. **L. 224-1**: a PER's object is the acquisition
  and enjoyment of **personal lifetime rights** or the payment of a **capital**, payable from
  the liquidation of a compulsory old-age pension (or the statutory age); the plan must offer
  the possibility of acquiring a **rente viagère** at maturity, with a reversion option; the
  insurance version is operated through a **contrat d'assurance de groupe**. **L. 224-2**:
  three funding sources and therefore **three compartments** — voluntary payments; employer
  profit-sharing, incentive payments and employer contributions; compulsory employer/employee
  contributions. **L. 224-3**: investments must offer "sufficient protection of the savings
  invested", and the **default allocation progressively de-risks with proximity to
  retirement** (*gestion pilotée par horizon*), the holder being free to choose another
  profile. **L. 224-4**: an exhaustive list of **early release** cases — death of the spouse
  or PACS partner, disability, over-indebtedness, exhaustion of unemployment benefit, judicial
  liquidation of the business, and **purchase of the principal residence**, the last not
  available from the compulsory compartment. **L. 224-5**: compulsory contributions convert to
  a **lifetime annuity**; other rights may be taken as a lump sum (single or staged) or as an
  annuity unless an irrevocable annuity election was made at opening. **L. 224-6**: rights are
  **transferable to any other PER**, with **transfer fees capped at 1 % of acquired rights and
  waived after five years from the first payment or once the holder reaches retirement age**;
  compulsory-contribution rights transfer only on leaving the employer; changing plan requires
  18 months' notice. **L. 224-7**: annual performance data **gross and net of fees** per
  investment [R34]. Primary for per-assurance; the annuity leg of a liquidated PER is the
  rente-viagere model.

(frlib-reg-r35)=

### R35. Loi n° 2022-270 du 28 février 2022 (loi Lemoine)

- **Publisher:** Légifrance (Journal officiel)
- **URL:** https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045268729
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** The statute that rewrote French borrower insurance, verified article by
  article. **Titre I** — art. 1 replaces the twelve-month cancellation window with
  **résiliation à tout moment**, amending both the Code des assurances and the Code de la
  mutualité; art. 2 removes the "de groupe" restriction from the Code de la consommation
  substitution articles and requires any refusal to be explicit and to list **all** reasons
  and the missing information or guarantees; art. 3 imposes an **annual notification** of the
  cancellation right and its procedure, with administrative fines of **€3 000 for individuals
  and €15 000 for legal persons**, and requires loan offers to mention the right to cancel at
  any time after signature; art. 4 extends the cost disclosure to **eight years**; art. 5 sets
  a **ten business day** deadline to process a substitution request; art. 7 sets the sanctions
  framework; **art. 8 fixes entry into force — 1 June 2022 for new loan offers and
  1 September 2022 for contracts already in force**. **Titre II** — art. 9 **droit à
  l'oubli**: insurers may not seek information about a cancer or hepatitis C beyond **five
  years** from the end of treatment; **art. 10 removes the medical questionnaire** where the
  **insured share of the borrower's loans is at most €200 000 and the loan matures before the
  borrower's 60th birthday**, effective **1 June 2022**; art. 11 requires a report to
  Parliament after two years on the effect on risk pooling, tariffs and access [R35]. Primary
  for assurance-emprunteur, and the direct cause of the fall in aggravated-risk applications
  recorded at R37.

(frlib-reg-r36)=

### R36. Code de la consommation, arts. L. 313-8 and L. 313-30 — TAEA, fiche standardisée, substitution

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731512 (L. 313-8);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045271935 (L. 313-30)
- **Accessed:** 2026-08-26
- **Fetched:** yes (both version 1 June 2022)
- **Annotation:** Verified. **L. 313-8**: any document given to the borrower about the loan
  insurance must state the cost in three ways — as a **taux annuel effectif de l'assurance
  (TAEA)** allowing comparison with the loan's overall effective rate; as a **total amount in
  euros over eight years and over the full loan term**; and as an **amount per payment period
  in euros**, stating whether it is added to the loan instalment. The lender must at the same
  time hand over the **fiche standardisée d'information** referred to at art. L. 313-10, plus
  a notice explaining the right to cancel the insurance at any time after signature of the
  loan offer; the rules apply to loan offers issued from 1 June 2022 and to existing insurance
  contracts from 1 September 2022. **L. 313-30**: the lender may not refuse another insurance
  contract as security if it presents an **equivalent level of guarantee** to the one it
  proposes, and any refusal must be an explicit decision listing all the reasons and
  identifying the missing information and guarantees; the same rules apply when the borrower
  exercises the cancellation right under insurance law [R36]. The article as fetched does not
  itself carry the ten-working-day response deadline or a fee prohibition — those sit in loi
  Lemoine arts. 5 and 1 [R35]. Primary for assurance-emprunteur: the TAEA and the
  eight-year/full-term euro cost are exactly the quantities an ADE model has to be able to
  produce.

(frlib-reg-r37)=

### R37. France Assureurs — *Statistiques Convention AERAS, année 2023* (November 2024)

- **Publisher:** France Assureurs (published as Fédération Française de l'Assurance)
- **URL:** https://www.franceassureurs.fr/wp-content/uploads/aeras_dossier_stat_2023_csp_vf.pdf
- **Accessed:** 2026-08-26
- **Fetched:** yes (20-pp. PDF downloaded, text extracted locally with PyMuPDF; statistics
  stopped at 20 November 2024)
- **Annotation:** The only public French document that puts a price on borrower insurance.
  Verified **applications**: **2.9 million** loan-insurance applications assessed in 2023 for
  mortgage and professional credit (down 1.1 million on 2022, tracking a **−41 %** fall in new
  household housing credit); **90.0 %** presented no aggravated health risk; **7.6 %
  (224 068)** presented a *risque aggravé de santé*, after **9.6 % in 2022 and 12.1 % in
  2021**, the fall attributed to the loi Lemoine questionnaire removal and the five-year
  *droit à l'oubli* [R35]; excluding pending and abandoned files, an offer was made on
  **99.6 %** of applications. Verified **outcomes on aggravated risks**: **94.5 %** received an
  offer covering at least death (**202 961** applications); excluding files sent to the
  very-high-risk pool, offers with **no surprime and no exclusion** ran at **death 65 %, PTIA
  87 %, incapacité-invalidité 51 %**; death cover was offered **with a surprime in 31 %** of
  cases; **6 209** files went to the very-high-risk pool, of which **40.3 %** received an
  offer. Verified **premium pooling (écrêtement des surprimes)**: **18 569 borrowers**
  benefited in 2023 for **€4.6 m** of capped premiums (**€44.6 m** cumulative since 2007,
  financed half by insurers and half by banks); average age **46.4**; **average insured
  capital €82 700**, **average intended term 18.1 years**; and — **the one public price
  point** — **the average insurance rate is 1.01 % of initial capital before écrêtement and
  0.65 % after, a 36 % reduction**. Verified **market shape**: **€11.8 bn** of premiums in
  2023, **85 % (€9 987 m)** on bank group contracts and **15 % (€1 824 m)** on *délégation
  d'assurance* (**22 %** for mortgages alone); by loan type **67 % mortgage, 25 % consumer,
  9 % professional**; by guarantee **69 % death, 30 % incapacité-invalidité, 2 %
  unemployment** [R37]. Two cautions: these are aggravated-risk lives, so the 1.01 %/0.65 %
  rates bound a standard rate from above rather than describing it, and no standard-risk rate
  table is public, so the frlib ADE premium rate is `**[std]**`. The AERAS convention's own
  numeric thresholds — age limit, insured-capital ceiling, *taux d'effort* trigger — are
  **not** in this document and are **[unverified]**.

(frlib-reg-r38)=

### R38. Code général des collectivités territoriales, art. L. 2223-33-1 — funeral financing formulas

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027762422
- **Accessed:** 2026-08-26
- **Fetched:** yes (version 28 July 2013, inserted by loi n° 2013-672 du 26 juillet 2013,
  art. 73)
- **Annotation:** One sentence of verified full text, and it is the whole difference between a
  French *contrat obsèques* and an ordinary small whole-of-life policy: "*Les formules de
  financement d'obsèques prévoient expressément l'affectation à la réalisation des obsèques du
  souscripteur ou de l'adhérent, à concurrence de leur coût, du capital versé au
  bénéficiaire.*" The capital paid to the beneficiary is **earmarked, up to the cost of the
  funeral**, for the subscriber's funeral; anything above that cost falls back to the ordinary
  life-insurance rules [R38]. Read with art. L. 132-23-1 of the Code des assurances [R31],
  which separately requires the death capital to be **revalued between death and payment** on
  terms the contract must state — the revaluation and the earmarking together are what an
  obseques model has to represent. Primary for obseques.

(frlib-reg-r39)=

### R39. Loi n° 2014-617 du 13 juin 2014 (loi Eckert) — inactive accounts and unclaimed life contracts

- **Publisher:** Légifrance (Journal officiel)
- **URL:** https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000029095362/
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified: an account is **inactive** after **12 months** without operation and
  without contact from the holder (**5 years** for savings and securities accounts), or, for a
  deceased holder, 12 months after death without contact from an heir; a life insurance
  contract is **unclaimed** where the benefit has not been claimed for **10 years** after the
  insurer knew of the death or after the contract's term; insurers must "*consultent chaque
  année*" the national register of natural persons (**RNIPP**) to identify deceased
  policyholders; balances and unclaimed proceeds transfer to the **Caisse des dépôts et
  consignations** after **10 years**, within one month of the deadline, and become **State
  property after 20 years** at the CDC; revaluation of the death guarantee may not fall below a
  rate set by ministerial arrêté and continues **until the deposit with the CDC**. **In force
  1 January 2016** with limited exceptions [R39]. Background for every contract with a death
  benefit; most material to obseques, where small capitals and elderly beneficiaries make
  unclaimed proceeds and continued revaluation a live cash flow item.

(frlib-reg-r40)=

### R40. Code général des impôts, art. 125-0 A — taxation of life insurance products

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038836732/2019-10-01
- **Accessed:** 2026-08-26
- **Fetched:** yes (version 1 October 2019 – 1 January 2020)
- **Annotation:** The single strongest driver of French partial-surrender timing, and therefore
  a behavioural assumption rather than a tax calculation as far as this library is concerned.
  Verified duration thresholds: **six years** for contracts taken out between 1 January 1983
  and 31 December 1989, **eight years** for contracts from 1 January 1990. For contracts
  meeting the threshold an **annual abattement** applies to gains accrued from 1 January 1998
  — **€4 600** for a single, widowed or divorced taxpayer and **€9 200** for a couple taxed
  jointly — applied first to products attached to premiums paid **before 27 September 2017**,
  then to products on premiums paid from that date where the art. 200 A option is not
  exercised. Verified withholding rates: for premiums paid **up to 26 September 2017**,
  **7.5 %** at or beyond the 6/8-year threshold, **15 %** for 4–6 years, **25 %** for 2–4
  years, **35–45 %** under 2 years; for premiums paid **from 27 September 2017**, **12.8 %**
  standard and **7.5 %** at or beyond the threshold. Income tax exemptions apply where the
  contract terminates by conversion into an annuity, or on redundancy, early retirement or
  disability of the holder or spouse [R40]. The **€150 000** total-premium threshold above
  which the 7.5 % rate ceases to apply to the excess is widely reported but was **not**
  confirmed in the fetched text — **[unverified]**. Social contributions are outside this
  article. Load-bearing for the surrender assumptions of the savings products; a model that
  puts no lapse spike at duration 8 has ignored it.

(frlib-reg-r41)=

### R41. Code général des impôts, arts. 990 I and 757 B — death benefits

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288653 (990 I);
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006305367 (757 B)
- **Accessed:** 2026-08-26
- **Fetched:** yes (both version 11 March 2023)
- **Annotation:** Verified. **990 I** — the *prélèvement* on sums paid by insurers on death in
  respect of premiums paid **before the insured's 70th birthday**: a fixed **abattement of
  €152 500 per beneficiary** across all contracts, then **20 % up to €700 000** of each
  beneficiary's taxable share and **31.25 % above**; a further **20 % proportional reduction**
  applies to certain qualifying unit-linked contracts (entered into after 1 January 2014 or
  substantially modified by then, invested in collective vehicles, SME shares meeting
  employment and revenue thresholds, real-estate and social-housing funds, and venture/equity
  funds); annuities acquired "*moyennant le versement de primes régulièrement échelonnées …
  pendant une durée d'au moins quinze ans*" are excluded, and spouses and PACS partners are
  exempt via the arts. 795–796 inheritance exemptions. **757 B** — sums payable on death in
  respect of premiums paid **after the insured's 70th birthday** fall into the ordinary
  inheritance-tax scale by relationship, but only as to the **premiums**, after a single global
  **abattement of €30 500** across all contracts on the same insured's life; investment gains
  on those premiums are outside the charge. **The PER carve-out is specific and load-bearing:**
  for a **plan d'épargne retraite** and for the pan-European PEPP, the **whole** payout is
  taxable where death occurs after age 70 — the PER does not get the premiums-only treatment
  assurance vie gets [R41]. Shapes beneficiary-side behaviour and the relative attractiveness
  of pre-70 funding across the savings and protection products.

(frlib-reg-r42)=

### R42. Code général des impôts, art. 163 quatervicies — PER deductibility

- **Publisher:** Légifrance
- **URL:** https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038836248
- **Accessed:** 2026-08-26
- **Fetched:** yes (version dated 21 February 2026)
- **Annotation:** Verified: contributions to *plans d'épargne retraite populaire*,
  supplementary pension schemes and qualifying retirement contracts are deductible from net
  global income within an annual ceiling equal to the **greater of 10 % of professional income
  capped at eight times the annual PASS, and 10 % of the PASS**, less amounts already deducted
  under other retirement provisions; spouses and PACS partners filing jointly may on request
  **pool** their ceilings; a person newly resident in France gets a **tripled** first-year
  ceiling [R42]. **One conflict is left standing rather than resolved:** the fetched text
  reports that unused ceiling may be used in **five** following years, while the tax
  administration's published guidance reports **three** — the carry-forward length is therefore
  **[unverified]**. The deduction is what makes PER inflows behave differently from assurance
  vie inflows (year-end contribution spikes, contribution levels keyed to the ceiling) and
  belongs in any PER premium-behaviour assumption.

---

## 6. Professional standards and accounting

(frlib-reg-r43)=

### R43. Institut des actuaires — Norme de Pratique Actuarielle 1 (NPA 1), *Pratiques actuarielles générales*

- **Publisher:** Institut des actuaires
- **URL:** https://www.institutdesactuaires.com/docs/2016133854_npa1-pratiques-actuarielles-ge-769-ne-769-rales-normes-de-pratique-recommande-769-e-ag-ia-150615.pdf
- **Accessed:** 2026-08-26
- **Fetched:** yes (16-pp. PDF downloaded, text extracted locally with PyMuPDF; the Institut's
  normes-professionnelles index page returned HTTP 404, so this was reached by direct PDF URL)
- **Annotation:** Verified: NPA 1 is a **category 3 professional standard, i.e. a *pratique
  recommandée***. Under art. 28 of the Institut's Statuts (June 2014), members "*devraient
  normalement se conformer à la pratique recommandée sauf s'il y a des motifs valables et
  justifiables de ne pas le faire*", and a member who departs from it must be able to explain
  clearly why and to identify the material respects in which they departed. NPA 1 is the
  French translation of the IAA's **ISAP 1**, approved 18 November 2012, and was **adopted by
  the Institut des Actuaires on 15 June 2015**; its sections cover assignment acceptance,
  knowledge of the environment, external sources, materiality, **data quality**, assumptions
  and methodologies (whether chosen by the actuary or imposed), reasonable judgement,
  vocabulary, cross-references and the effective date [R43]. The professional frame for the
  assumption-setting these models make explicit — background rather than operative, since a
  reference implementation is not an actuarial opinion.

(frlib-reg-r44)=

### R44. Institut des actuaires — Norme de Pratique Actuarielle 2 (NPA 2), *Modèles actuariels*

- **Publisher:** Institut des actuaires
- **URL:** https://www.institutdesactuaires.com/docs/2016133917_npa2-mode-768-les-actuariels-norme-de-pratique-recommande-769-e-ag-ia-150615.pdf
- **Accessed:** 2026-08-26
- **Fetched:** yes (12-pp. PDF downloaded, text extracted locally with PyMuPDF)
- **Annotation:** The standard this library sits under, and the reason its documents look the
  way they do. Verified: NPA 2 is likewise a **category 3 *pratique recommandée***, **adopted
  15 June 2015 with effect from 1 January 2016**, produced by the Institut's
  actuarial-standards working group and not a translation of an ISAP. It "*vise à s'appliquer
  à tout modèle actuariel, qu'il soit basé sur des logiciels externes ou des développements
  internes*", and its recommendations follow a **principle of proportionality** — read
  consistently with the size of the undertaking receiving the model, its resources and market
  presence, and with the stakes and complexity of the modeling. Its scope covers the critical
  processes of the actuarial function, including **pricing** and the technical studies attached
  to new products such as profitability studies [R44]. Directly load-bearing for all nine
  products: it is the standard against which a published model documentation, worked example
  and test suite are judged. **Not retrieved and therefore [unverified]:** NPA 3, NPA 4
  (best-estimate provisions in non-life and life) and NPA 5 (data). NPA 4 would be the most
  directly relevant standard to this library and should be retrieved before this file is
  finalised.

(frlib-reg-r45)=

### R45. IFRS 17 *Insurance Contracts*

- **Publisher:** IFRS Foundation
- **URL:** https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/
- **Accessed:** 2026-08-26
- **Fetched:** yes (standard landing page; the standard text itself was not read)
- **Annotation:** Verified: IFRS 17 was **issued May 2017** and is **effective for annual
  reporting periods beginning on or after 1 January 2023** (earlier application permitted if
  IFRS 9 is also applied); it replaced **IFRS 4** (2004), which had permitted "a wide variety
  of accounting practices for insurance contracts". Under the general measurement model an
  entity measures a group of contracts as "a risk-adjusted present value of the future cash
  flows (the **fulfilment cash flows**)", consistent with observable market information, plus
  "an amount representing the unearned profit in the group of contracts (the **contractual
  service margin**)"; the standard "includes an optional simplified measurement approach, or
  **premium allocation approach**, for simpler insurance contracts"; and insurance revenue,
  insurance service expenses and insurance finance income/expenses are presented separately
  [R45]. A **variable fee approach** exists for direct participating contracts but its
  mechanics are not set out on the fetched page and are **[unverified]** here — which matters,
  because the fonds en euros and eurocroissance are the archetypal direct-participating
  contracts. French listed insurers report on this basis from 2023 and there is no French
  carve-out.

---

## 7. Market context

(frlib-reg-r46)=

### R46. France Assureurs — "L'assurance vie en 2025 : une collecte solide au service de l'économie française" (27 January 2026)

- **Publisher:** France Assureurs
- **URL:** https://www.franceassureurs.fr/espace-presse/lassurance-vie-en-2025-une-collecte-solide-au-service-de-leconomie-francaise/
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified 2025 market figures. **Encours €2 107 bn** at end-December 2025,
  **+6.1 %** (**+€122 bn**) year on year. **Cotisations €192.1 bn**, **+10 %** (**+€17.1 bn**),
  with December 2025 alone at €16.1 bn, the highest December on record (+17 %). **Prestations
  €141.4 bn**, **−3 %** (**−€5.0 bn**). **Collecte nette +€50.6 bn**, up €22.1 bn on 2024 and
  above €50 bn for the first time since 2010. Split of cotisations: **UC 39 %, euro 61 %**
  (46 % UC in December); net inflows **UC +€42.5 bn, euro +€8.1 bn**. **PER assurantiels**:
  **€20.2 bn** of payments in 2025 (**+16 %**), about **1 million** new plans, **7.9 million**
  holders at end-2025 (**+1.0 million**), **encours €111.9 bn**, net inflow **+€11.0 bn** (the
  last two figures from the companion chiffres-clés page, same publisher, same date) [R46].
  Market context for the savings and retirement products; no per-insurer or per-contract figure
  is derivable from it.

(frlib-reg-r47)=

### R47. France Assureurs — "L'assurance vie en 2024" (chiffres clés, 23 September 2025)

- **Publisher:** France Assureurs
- **URL:** https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/lassurance-vie-en-2024/
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified 2024 figures, and the one page on this list that yields a genuine
  model calibration point. **Encours €1 985.8 bn (+3.9 %)**. **Cotisations €174.9 bn
  (+14.7 %)** — individual €160.0 bn (+16.4 %), collective €14.9 bn (−0.4 %); by support,
  **euro €108.6 bn (+19.2 %)** and **UC €66.3 bn (+8.1 %)**. **Provisions mathématiques
  €1 932.2 bn (+4.4 %)**, split **€1 345.1 bn on euro supports (≈70 %)** and **€587.1 bn on UC
  (+10.3 %, ≈30 %)**. **Prestations €146.4 bn (−3.1 %)**. **Collecte nette €28.5 bn** — UC
  **+€33.2 bn**, euro **−€4.7 bn**. And the calibration point: **provision pour participation
  aux bénéfices €53.6 bn at end-2024, −11.1 % on end-2023** — roughly **4 % of euro-support
  provisions mathématiques**, the most useful public anchor for a PPB buffer in a fonds en
  euros model [R47]. The page carries **no** average euro-fund revaluation rate; that number
  lives in the ACPR series [R11], which — contrary to what this file previously recorded —
  was retrievable and has been read: **2.63 % in 2024 and 2.63 % in 2025** on individual
  contracts. The two sources agree on the PPB: €53.6 bn ≈ 4 % of euro-support provisions
  mathématiques here, **4.3 % of life provisions end-2024 falling to 4.0 % end-2025** at
  [R11].

(frlib-reg-r48)=

### R48. France Assureurs — "L'assurance vie en unités de compte en 2025" (6 May 2026)

- **Publisher:** France Assureurs
- **URL:** https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/assurance-vie-unite-de-compte-2025/
- **Accessed:** 2026-08-26
- **Fetched:** yes
- **Annotation:** Verified 2025 figures, including the two charge levels a unit-linked model
  actually needs. **UC cotisations €75.1 bn**, **39.1 %** of all life premiums, **+13.2 %**;
  **UC provisions mathématiques €666.4 bn, +13.5 %**; **net inflow €42.5 bn**, "its highest
  historical level" (against €34.3 bn in 2022); **UC-backed placements €684.5 bn**, of which
  **€567 bn financing enterprises (83 %)** — €372 bn equities, €171 bn bonds, €24 bn real
  estate; **performance of UC supports +5.5 %** in 2025, "*brute des frais des contrats en UC
  et nette des coûts récurrents des fonds*", with a **five-year average of +4.9 % a year**.
  **Charges: recurring fund costs 1.60 %** (down 2 bp on 2024) and **contract charges on UC
  0.88 %** (stable) [R48]. These are market averages with real dispersion around them, not any
  insurer's rate card — an frlib UC charge parameter cites this entry and still carries
  `**[std]**`.

(frlib-reg-r49)=

### R49. France Assureurs — chiffres clés landing page and the president's 2025 market review

- **Publisher:** France Assureurs
- **URL:** https://www.franceassureurs.fr/nos-chiffres-cles/lassurance-vie/;
  https://www.franceassureurs.fr/nos-positions/tribunes-de-notre-presidente/proteger-aujourdhui-construire-demain/
  (25 March 2026)
- **Accessed:** 2026-08-26
- **Fetched:** yes for both
- **Annotation:** Verified. Landing page: **encours €2 088 bn at end-2025** — a slightly
  earlier vintage than the €2 107 bn of R46, from a different cut of the same series — **UC
  cotisations €75.9 bn in 2025, +14.4 %**, and monthly premium updates (€19.3 bn in June 2026,
  page last updated 30 July 2026). Commentary: "*Près de 200 milliards d'euros de cotisations
  en 2025*", **net inflows €51 bn**, **encours €2 107 bn**; insurers hold about **€2 800 bn**
  invested in the economy, roughly **93 % of French GDP**; 2025 natural-event claims **€5.2 bn**,
  of which hail €2.2 bn [R49]. **Two disclosures.** The €2 088 bn / €2 107 bn discrepancy is
  recorded and not reconciled — both are France Assureurs figures from different cuts. And
  neither page gives assurance emprunteur, obsèques or dépendance premium totals (for those see
  R37 and R28); in particular, a widely quoted **5.7 million active contrats obsèques in 2024**
  attributed to France Assureurs could **not** be sourced to a France Assureurs page here and is
  **[unverified]**. Background market sizing for all nine products.

---

### The three measurement bases one projection feeds

A French life insurer values the same book three times, and all three valuations consume the
same per-policy projection of premiums, claims, expenses and discretionary benefits.

**Solvabilité II technical provisions.** Best estimate — the probability-weighted average of
future cash flows discounted at the EIOPA risk-free term structure [R5] — plus a risk margin,
under the directive [R1] and the delegated regulation [R2] as described by EIOPA [R4] and as
transposed into the Code des assurances. Contract boundaries, the cost-of-capital rate and the
standard-formula shocks were never read from a retrieved instrument, so every one of them is
`**[std]**` in this library, and the SCR and MCR layers are cited-not-specified.

**The Code des assurances statutory provision mathématique.** The French GAAP *comptes sociaux*
balance sheet does **not** disappear under Solvabilité II: both exist, side by side. The
provision mathématique is the difference between the present values of the two parties'
commitments, **including future management costs**, and it sits alongside ten other named
provisions [R6], among them the PPB [R6] [R16], the PRE [R7] and the PAF [R8] [R9]. This is the
balance sheet the participation aux bénéfices obligation actually operates on — the minimum PB
[R14] [R15] and the eight-year PPB release [R16] are computed on the statutory accounts, not on
the Solvency II ones, which is precisely why a French model must carry a *provision
mathématique* recursion as well as a best-estimate projection. The technical rate inside that
recursion is capped by A. 132-1 [R17] and any guaranteed uplift by A. 132-3 [R18].

**IFRS 17.** Fulfilment cash flows — a risk-adjusted present value of future cash flows — plus
a contractual service margin releasing profit over coverage, effective from 1 January 2023 with
no French carve-out [R45]. The variable fee approach for direct-participating business, which is
what a fonds en euros and a eurocroissance contract are, could not be read from a retrieved page
and is **[unverified]** here.

**What this library computes: none of the three.** The frlib models publish gross
best-estimate-style liability cash flows per model point, income-positive, undiscounted, on a
declared grid. The discounting, the margins, the statutory provision recursion and the CSM
layer belong to a layer above — which is the only honest way to serve three bases from one
projection, and the reason every product document says so in its own scope note.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-reg-r1
[R10]: #frlib-reg-r10
[R11]: #frlib-reg-r11
[R12]: #frlib-reg-r12
[R13]: #frlib-reg-r13
[R14]: #frlib-reg-r14
[R15]: #frlib-reg-r15
[R16]: #frlib-reg-r16
[R17]: #frlib-reg-r17
[R18]: #frlib-reg-r18
[R19]: #frlib-reg-r19
[R2]: #frlib-reg-r2
[R20]: #frlib-reg-r20
[R21]: #frlib-reg-r21
[R22]: #frlib-reg-r22
[R23]: #frlib-reg-r23
[R24]: #frlib-reg-r24
[R25]: #frlib-reg-r25
[R26]: #frlib-reg-r26
[R27]: #frlib-reg-r27
[R28]: #frlib-reg-r28
[R29]: #frlib-reg-r29
[R3]: #frlib-reg-r3
[R30]: #frlib-reg-r30
[R31]: #frlib-reg-r31
[R32]: #frlib-reg-r32
[R33]: #frlib-reg-r33
[R34]: #frlib-reg-r34
[R35]: #frlib-reg-r35
[R36]: #frlib-reg-r36
[R37]: #frlib-reg-r37
[R38]: #frlib-reg-r38
[R39]: #frlib-reg-r39
[R4]: #frlib-reg-r4
[R40]: #frlib-reg-r40
[R41]: #frlib-reg-r41
[R42]: #frlib-reg-r42
[R43]: #frlib-reg-r43
[R44]: #frlib-reg-r44
[R45]: #frlib-reg-r45
[R46]: #frlib-reg-r46
[R47]: #frlib-reg-r47
[R48]: #frlib-reg-r48
[R49]: #frlib-reg-r49
[R5]: #frlib-reg-r5
[R6]: #frlib-reg-r6
[R7]: #frlib-reg-r7
[R8]: #frlib-reg-r8
[R9]: #frlib-reg-r9
[unverified]: #frlib-unverified
<!-- END generated citation links -->
