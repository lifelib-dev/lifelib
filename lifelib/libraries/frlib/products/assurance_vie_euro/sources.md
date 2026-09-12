# Sources

Source ids — [S#] primary product documents, [R#] regulatory and actuarial references —
are carried **verbatim** from `_research/assurance-vie-euro.md` and are frozen: never
renumber. Only ids actually cited in `product-spec.md` or `technical-notes.md` are listed
here. **No id is omitted:** all fourteen primary sources S1–S14 and all eighteen
regulatory references R1–R18 recorded in the research file are cited by the two documents
in this directory, so there are no gaps in the numbering below. Nothing new was fetched at
drafting; every access date is **2026-08-26**, the research file's own access date.

Two retrieval failures are carried forward rather than papered over: **S14** returned
HTTP 404 and **R18** returned an empty body, and both are listed below with
`Retrieved: NO`. Everything that rests on them is tagged [unverified] in the documents.

---

## Primary product sources [S#]

(frlib-assurance_vie_euro-s1)=

### S1 — Generali Vie / Boursorama, "BoursoVie — Notice d'information valant Conditions générales" (juillet 2025)
- Publisher / doc type: Generali Vie (insurer), Boursorama–BoursoBank (souscripteur of the group contract); `notice d'information valant conditions générales`, 75 pp.
- URL: https://s.brsimg.com/content/pdf/banque/cg/cg-brsvie.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: group-contract wrapper; daily compound valuation and PB credited at 31 December value date; PB definitively acquired and itself revalued; absence of contractual PB; `prorata temporis` PB allocation; 0.75% max management charge on the PM including the year's PB; nil entry and arbitrage charges; TMG announced at the start of the year and applied pro rata on in-year `dénouement`; minimum payments and partial surrenders; surrender order across supports; `avance` and beneficiary-acceptance blocks; two-month settlement; art. L136-7 social levies; the tax annexe.

(frlib-assurance_vie_euro-s2)=

### S2 — MACSF épargne retraite, "Notice d'information RES Multisupport" (réf. 16 10 201 Y, édition 10/2024)
- Publisher / doc type: MACSF épargne retraite (insurer), group contract subscribed by the association AMAP; `notice d'information`, ~24 pp.
- URL: https://www.macsf.fr/content/download/4098/fichier/MACSF_1610201Y_Notice_information_RES_Multisupport.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: PB allocated at 31 December to the PM or to the PPB, with the **eight-year** release limit restated in the contract; board-set art. A132-3 rate applied pro rata in-year; 3% max entry charge and 0.50% max management charge; the eight-year minimum surrender-value table (970 × 0.995ⁿ) that settles the charge base and the guarantee form; association fee; 30-day renunciation; two-month settlement; nil surrender charge.

(frlib-assurance_vie_euro-s3)=

### S3 — Suravenir / Meilleurtaux Placement, "Meilleurtaux Placement Vie 2 — Notice" (contrat n° 2282, réf. 5980 (03.2026), mars 2026)
- Publisher / doc type: Suravenir (Crédit Mutuel Arkéa), group contract subscribed by the association VIREA; `notice d'information`, 20 pp.
- URL: https://placement.meilleurtaux.com/images/docs-av/meilleurtaux-placement-vie-2/meilleurtaux-placement-vie-2-notice.pdf
- Retrieved: YES (PDF downloaded, full text extracted). The most recent full notice in the set.
- Used for: branches 20 and 22; the explicit **net-of-management-charges** guarantee; no contractual PB and no guaranteed interest rate; 0.00% entry and 0.60% management charge on Suravenir Rendement 2; the eight-year minimum surrender-value table (1 000 × 0.994ⁿ); optional death cover on the `capital sous risque` (0.15‰–5.15‰ monthly, one-year waiting period); 30-day settlement with penalty interest; `dynamisation des plus-values` net of social levies; **`prélèvements sociaux` 17.2%** and the PFU table; 3% annuity charge; `avance` terms held outside the notice.

(frlib-assurance_vie_euro-s4)=

### S4 — Suravenir / Épargnissimo, "Croissance Avenir — Notice" (contrat n° 2178, réf. 4023-13 (02.2023), février 2023)
- Publisher / doc type: Suravenir, group contract subscribed by the association SEREP; `notice d'information`, 20 pp.
- URL: https://www.epargnissimo.fr/assets/files/docutheque/croissance-avenir/adhesion-et-gestion-du-contrat/notice.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the gross/net guarantee contrast inside a single notice (Suravenir Rendement gross, Rendement 2 and Opportunités 2 net); the **contractual 90% PB rate** with the profit account written out in full, including the debit line for management charges at a 0.60% maximum and the carry of the whole positive balance to a shared PPB; the pre-2016 A331 numbering still used by insurers; optional death cover.

(frlib-assurance_vie_euro-s5)=

### S5 — Suravenir, "Document d'informations spécifiques — Fonds en Euros Actif Général" (mise à jour 05/08/2026)
- Publisher / doc type: Suravenir; PRIIPs-style disclosure of the euro fund as an investment option, 3 pp.
- URL: https://espaceclient.suravenir.fr/o/documents/WsPUS/DIS_OPC/VIE00000CESR.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the guarantee described in one line as premiums net of entry charges "minorée chaque année des frais de gestion"; risk indicator **1 of 7** and the flat stress/unfavourable/intermediate one-year scenarios; recommended holding period of one year for the support; unilateral surrender at any time; the HCSF power as the insurer summarises it ("maximum 6 mois renouvelable"); the fund's own internal costs (0.24% + 0.03% = 0.48% impact) and their explicit exclusion of the contract's charges; FGAP contribution.

(frlib-assurance_vie_euro-s6)=

### S6 — CNP Assurances, "Document d'informations clés — NUANCES 3D" (produced 22/07/2026)
- Publisher / doc type: CNP Assurances (groupe La Banque Postale), distributed through the BPCE network; DIC (PRIIPs KID), 3 pp.
- URL: https://dic.cnp.fr/wkd-web/kid-webapi/document/dic/BPCE/858
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the clearest published statement of the **net guarantee**; the euro support's return depending on the PB rate awarded at 31 December; the eight-year recommended holding period given for fiscal reasons; maturity fixed between 10 and 30 years and renewable annually without limit; 30-day renunciation and 30-day surrender settlement; **FGAP EUR 70 000** per insured per company; the PRIIPs aggregate cost ranges.

(frlib-assurance_vie_euro-s7)=

### S7 — CNP Assurances, "Document d'informations clés — NUANCES PLUS" (produced 22/07/2026)
- Publisher / doc type: CNP Assurances; DIC (PRIIPs KID).
- URL: https://dic.cnp.fr/wkd-web/kid-webapi/document/dic/BPCE/859
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: confirmation that the identical net-of-management-charges guarantee wording and the same 31 December PB dependence apply to a second CNP euro support — the evidence that S6 is a house design, not a one-off.

(frlib-assurance_vie_euro-s8)=

### S8 — CNP Assurances, "Document d'informations clés — PERSPECTIVE CAPI"
- Publisher / doc type: CNP Assurances, distributed through La Banque Postale; DIC for a `contrat de capitalisation individuel nominatif`.
- URL: https://dic.cnp.fr/wkd-web/kid-webapi/document/dic/LBP/C3C
- Retrieved: YES (PDF downloaded, full text extracted; the production-date line was truncated in extraction and is not quoted).
- Used for: the deliberate contrast — a genuinely individual contract whose euro support carries the **gross-style** guarantee ("nettes de tous frais") from the same insurer that writes the net guarantee in S6 and S7.

(frlib-assurance_vie_euro-s9)=

### S9 — Aviva Vie / Aviva Épargne Retraite (now Abeille), "Contrat collectif d'assurance vie Multisupport Afer — Notice" (réf. 60121-1021, édition 10/2021)
- Publisher / doc type: co-insurers Aviva Vie and Aviva Épargne Retraite, contract subscribed by the association Afer; `notice d'information`, ~56 pp. plus annexes.
- URL: https://www.afer.fr/content/uploads/2022/02/60121-1021-notice-contrat-collectif-assurance-vie-multisupport-afer.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Pre-rebranding vintage.
- Used for: the operative **`effet de cliquet`** wording and the glossary definition; the **100%** contractual PB on the ring-fenced Fonds Garanti, distributed after any PPB dotation or release; the PPB's stated smoothing purpose and its joint governance; the gross-style guarantee (premiums net of entry charges); 0.5% entry and 0.475% management charge levied after the PB allocation; the 0.055% death-floor charge; the 0.1% cap on the fund's asset-management charge; association fee; 30-day renunciation.

(frlib-assurance_vie_euro-s10)=

### S10 — Afer / Abeille Vie, "Multisupport Afer — Tableau des frais" (réf. 60142C - 2405, mai 2024)
- Publisher / doc type: Abeille Vie and Abeille Épargne Retraite, published on afer.fr; standardised fee table, 2 pp.
- URL: https://www.afer.fr/content/uploads/2024/07/60142c-05-2024-fiche-transparence-des-frais-afer-multisupport-3-1.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: EUR 100 minimum initial payment; EUR 20 association fee; 0.475% annual charge on the euro support; **0.5% on contributions to the Fonds Garanti**; 0% arbitrage with unlimited free switches; 0% surrender charge; **3% on annuity instalments**.

(frlib-assurance_vie_euro-s11)=

### S11 — Afer, "Performances des supports à capital garanti" (web page)
- Publisher / doc type: Association Afer (afer.fr); product and performance page.
- URL: https://www.afer.fr/performances-des-supports-a-capital-garanti/
- Retrieved: YES (HTML fetched with a browser User-Agent and converted to text; the PDFs linked from the page are script-loaded and were **not** retrieved).
- Used for: the **`Taux Plancher Garanti`** — an in-year floor rate applied pro rata on `rachat total` and death, with a following-year top-up to the definitive fund return, the only such top-up in the set; the `effet de cliquet` named again at fund level; the Fonds Garanti's 2025 rate of 2.65%; fund size and management arrangements.

(frlib-assurance_vie_euro-s12)=

### S12 — Afer, "Communiqué de presse : Bilan et performances 2025" (web page)
- Publisher / doc type: Association Afer; press-release landing page.
- URL: https://www.afer.fr/espace-presse/communique-de-presse-resultats-2025/
- Retrieved: YES (HTML fetched with a browser User-Agent and converted to text; the linked PDF press release itself was not downloaded).
- Used for: the 2025 rates published by the insurer itself, each stated "net de frais de gestion et hors prélèvements sociaux et fiscaux" — Afer EuroGénération **4.05%**, Fonds Garanti en euros 2.65%, Afer Fonds Euros Retraite 3.50%.

(frlib-assurance_vie_euro-s13)=

### S13 — MAIF VIE, "Les frais de l'assurance vie — Assurance vie Responsable et Solidaire" (réf. TDF16 - 06/26, situation au 02/06/2026)
- Publisher / doc type: MAIF VIE (insurer), group contract subscribed by MAIF; standardised fee table, 2 pp. served as a PDF from the page URL.
- URL: https://www.maif.fr/tableau-frais-ars
- Retrieved: YES (PDF downloaded, text extracted row-wise).
- Used for: **EUR 30** minimum initial payment and no association fee; **0.80%** annual charge on the euro support — the top of the observed range; 0% `frais sur versement`; EUR 15 arbitrage with one free per year; EUR 0 surrender charge; 3% on annuity instalments.

(frlib-assurance_vie_euro-s14)=

### S14 — Afer, "Contrat collectif d'assurance vie — Notice, édition janvier 2025, Afer Génération"
- Publisher / doc type: Abeille Vie / Abeille Épargne Retraite for the Afer Génération contract; `notice d'information`.
- URL: https://www.afer.fr/content/uploads/2025/01/60190a-2501-dd-8549-avec-annexes-1.pdf
- Retrieved: **NO — HTTP 404** (the file is no longer at that path). Kept as a known reference only.
- Used for: the record, in "Variations across insurers", that Afer EuroGénération's contractual mechanics — including the reported eight-year loyalty bonus — are **[unverified]**, only its 2025 rate being sourced through S11 and S12.

---

## Regulatory and actuarial references (product research numbering) [R#]

(frlib-assurance_vie_euro-r1)=

### R1 — Code des assurances, art. A132-1 — maximum technical interest rate
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514601
- Retrieved: YES (version in force from 07/09/2017).
- Used for: the ceiling that anchors the TMG cap — 75% of the TME, and beyond eight years (and for periodic-premium contracts of any duration) the lower of 3.5% and 60% of the TME.

(frlib-assurance_vie_euro-r2)=

### R2 — Code des assurances, art. A132-1-1 — the monthly reference rate and the 0.25-point scale
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801948
- Retrieved: YES (version dated 01/01/2020).
- Used for: the mechanics of the maximum technical rate — the 0.25-point grid floored at zero, the 0.10 / 0.35 point trigger thresholds, and the three months allowed to implement a change.

(frlib-assurance_vie_euro-r3)=

### R3 — Code des assurances, art. A132-2 — permission to guarantee a minimum rate
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514622
- Retrieved: YES (version dated 07/09/2017).
- Used for: the construction that decides how a TMG is modeled — what may be guaranteed is a **total of technical interest and profit participation**, so the TMG is a floor on the credited rate, not a separate credit stacked on it.

(frlib-assurance_vie_euro-r4)=

### R4 — Code des assurances, art. A132-3 — caps on the taux minimum garanti
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514611
- Retrieved: YES (version in force from 07/09/2017).
- Used for: the TMG ceiling (the lower of 150% of the maximum technical rate, and the higher of 120% of it and 110% of the average rates credited over the last two financial years) and its duration window of at least six months and at most to the end of the following financial year.

(frlib-assurance_vie_euro-r5)=

### R5 — Code des assurances, Section V "Participation aux bénéfices techniques et financiers", arts. A132-10 to A132-17
- Légifrance (section page listing the articles with their version dates). URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000031738019/
- Retrieved: YES.
- Used for: the whole statutory PB machinery the model implements — A132-10 scope and the exclusion of `contrats à capital variable`; **A132-11** the 85% of the `compte financier` and the technical balance less the greater of 10% of it and 4.5% of premiums; A132-12 the minimum benefit; **A132-16** the PPB's eight-year release horizon; A132-17 equal treatment.

(frlib-assurance_vie_euro-r6)=

### R6 — Code des assurances, arts. A331-3, A331-4 and A331-9 — pre-2016 numbering of the same rules
- Légifrance. URLs: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006787891/2006-08-26 (A331-3); https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006787932 (A331-4); https://www.legifrance.gouv.fr/affichCodeArticle.do?categorieLien=cid&cidTexte=LEGITEXT000006073984&dateTexte=&idArticle=LEGIARTI000006787955 (A331-9)
- Retrieved: YES for all three, but Légifrance served **historic versions** (in force 1995–2007, 2014–2016 and 1995–2016 respectively). Cite R5 for anything relied on as current law.
- Used for: corroboration that the identical 85% / 10%-or-4.5% construction and the identical eight-year PPB horizon predate the 2016 recodification — which matters because insurers' own documents still cite this numbering [S4].

(frlib-assurance_vie_euro-r7)=

### R7 — Code des assurances, art. L132-21 — surrender value and the two-month deadline
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030461815
- Retrieved: YES (version dated 01/01/2016).
- Used for: the statutory two-month surrender settlement and the penalty interest that follows it (1.5× the legal rate for two months, then twice); the requirement that the contract state how the surrender value is computed; the prohibition on reduction charges against the mathematical provision.

(frlib-assurance_vie_euro-r8)=

### R8 — Code monétaire et financier, art. L631-2-1 — the HCSF powers (loi Sapin 2)
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034386882
- Retrieved: YES (version in force from 08/04/2017).
- Used for: 5° ter — temporary limitation of surrender payments, restriction of asset disposal, deferral of `arbitrages` and `avances`, limitation of premium acceptance, for at most three months renewable with the surrender restriction capped at six consecutive months; and 5° bis — modulation of PPB constitution and release. The attribution to loi n° 2016-1691 art. 49 is **[unverified]**: the statute itself was not retrieved.

(frlib-assurance_vie_euro-r9)=

### R9 — Code de la sécurité sociale, art. L136-7 — CSG on investment products, and the timing rule
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288474
- Retrieved: YES (version dated 21/02/2026).
- Used for: the rule that makes the euro fund distinctive for a cash-flow model — products on contracts **whose rights are expressed in euros** are charged "lors de leur inscription au bon ou contrat", annually as the PB is credited, while the unit-linked portion waits for `dénouement` or death. The article fixes the timing but **not the base or the rate**, which is why the levy base is **[std]** here.

(frlib-assurance_vie_euro-r10)=

### R10 — Code général des impôts, art. 125-0 A — income taxation of life-insurance products
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044989424
- Retrieved: YES (version dated 01/01/2022).
- Used for: the eight-year threshold and the EUR 4 600 / EUR 9 200 annual abattement; the 12.8% / 7.5% flat rates for premiums paid from 27 September 2017; the exemptions on `licenciement`, invalidity and annuitisation. This is the behavioural driver behind the duration-8 surrender step.

(frlib-assurance_vie_euro-r11)=

### R11 — Code général des impôts, art. 200 A — the PFU and the EUR 150 000 threshold
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053546896
- Retrieved: YES (version dated 21/02/2026).
- Used for: the default 12.8% flat rate, and the **EUR 150 000** outstanding-premium threshold above which only a computed fraction of products keeps the 7.5% rate — the article in which that threshold was actually verified.

(frlib-assurance_vie_euro-r12)=

### R12 — Code général des impôts, art. 990 I — death levy on premiums paid before age 70
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288653
- Retrieved: YES (version dated 11/03/2023).
- Used for: the EUR 152 500 abattement per beneficiary, the 20% rate to EUR 700 000 and 31.25% above, and the exemption of spouses, PACS partners and qualifying siblings.

(frlib-assurance_vie_euro-r13)=

### R13 — Code général des impôts, art. 757 B — death duties on premiums paid after age 70
- Légifrance. URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288569
- Retrieved: YES (version dated 11/03/2023).
- Used for: the ordinary inheritance scale applied to the **fraction of premiums** paid after the insured's 70th birthday, after a global EUR 30 500 abattement, with accumulated products outside the charge.

(frlib-assurance_vie_euro-r14)=

### R14 — ACPR, "Revalorisation 2025 des contrats d'assurance-vie et de capitalisation", *Analyses et synthèses* n° 180 (30 June 2026)
- ACPR / Banque de France. URL: https://acpr.banque-france.fr/system/files/2026-06/20260630_AS180_revalorisation_2025.pdf
- Retrieved: YES — but note the route: a plain fetcher returned HTTP 403 twice on both the publication page and the PDF; the PDF was then downloaded successfully **with a browser User-Agent** and its full text extracted. Covers 116 undertakings and 36 053 contract versions.
- Used for: the single most load-bearing quantitative reference here — euro-support mathematical provisions; the **2.63%** average 2025 `taux de revalorisation` and its definition (net of charges on encours, before social levies); the 2.3%–2.9% dispersion band, the 0.99-point intra-insurer spread and the 0.39-point position of the least-revalued group; UC-holding bonuses of 100–200+ bp; the **0.63%** average charge rate; the **2.8%** `taux de rendement de l'actif` and its dispersion; the 0.32% average `taux technique`; the **4.0%** PPB ratio; box 2 on inter-cohort smoothing; and footnote 12's direct restatement of the 85% rule.

(frlib-assurance_vie_euro-r15)=

### R15 — ACPR, "L'assurance-vie en 2025", *Analyses et synthèses* n° 179 (22 May 2026)
- ACPR / Banque de France. URL: https://acpr.banque-france.fr/system/files/2026-05/20260522_AS_Assurance_vie_2025.pdf
- Retrieved: YES (HTTP 403 on the publication page via a plain fetcher; the PDF was downloaded with a browser User-Agent and its text extracted).
- Used for: 2025 flows — EUR 159.1 bn of premiums, EUR 115.1 bn of benefits of which EUR 71.0 bn surrenders, **EUR 44.0 bn** net inflow, euro supports **+EUR 6.4 bn** after five years of outflow; capital-guaranteed and UC encours; the Livret A path against which the dynamic surrender assumption is rationalized; assurance vie as 32.9% of household financial wealth.

(frlib-assurance_vie_euro-r16)=

### R16 — ACPR, "Revalorisation 2024 des contrats d'assurance-vie et de capitalisation", *Analyses et synthèses* n° 175 (4 August 2025)
- ACPR / Banque de France. URL: https://acpr.banque-france.fr/system/files/2025-08/20250804_AS175_Revalorisation_contrats_assurance_vie_2024.pdf
- Retrieved: YES (downloaded with a browser User-Agent, text extracted). **Caveat carried forward: the published PDF shows an "ACPR-RESTREINT" marking in its page header although it is served from the ACPR's public publications area.**
- Used for: prior-year comparatives only, and only where R14 restates them independently — the PPB at 4.3% of individual life provisions at end-2024 against **4.9% at end-2023**.

(frlib-assurance_vie_euro-r17)=

### R17 — France Assureurs, "Nos chiffres clés — L'assurance vie" (web page)
- France Assureurs (trade body). URL: https://www.franceassureurs.fr/nos-chiffres-cles/lassurance-vie/
- Retrieved: YES (HTML fetched with a browser User-Agent and converted to text; the underlying statistical notes were not retrieved).
- Used for: total assurance vie encours of **EUR 2 088 bn** at end-2025.

(frlib-assurance_vie_euro-r18)=

### R18 — Commission Delegated Regulation (EU) 2015/35 (Solvency II delegated acts)
- EUR-Lex. URL: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R0035
- Retrieved: **NO** — EUR-Lex returned an empty body to a plain fetch and HTTP 202 with a zero-length body to a direct request. Kept as a known reference only.
- Used for: the honest statement that nothing in these documents about the Solvency II treatment of future discretionary benefits, management actions or the time value of the capital guarantee rests on a retrieved instrument; all of it is **[unverified]**.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the France cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose R1–R49 numbering is frozen
there and is prefixed `REG-` in product documents to avoid collision with the product
research numbering above. Entries cited by the two documents in this directory:

- **REG-R2** — Règlement délégué (UE) 2015/35. Level 2 Solvency II; blocked at EUR-Lex, so no contract-boundary, expense or risk-margin figure in this library comes from a retrieved text.
- **REG-R4** — EIOPA Solvency II framework page. The verified carrier for the best-estimate-plus-risk-margin structure and the three-pillar architecture.
- **REG-R5** — EIOPA risk-free interest rate term structures. Where a reader takes these cash flows and applies a market-consistent curve; no numeric curve is reproduced.
- **REG-R6** — C. ass. art. R343-3, the eleven life technical provisions. Locates the `provision mathématique` and the PPB, and explains why a French PM includes future management costs.
- **REG-R7** — C. ass. art. R343-5, `provision pour risque d'exigibilité`. Named as part of the general account behind the fund; not computed here.
- **REG-R8** — `Provision pour aléas financiers`, art. A331-2 (abrogated). Mechanics recorded from a retrieved text; the current article reference is [unverified].
- **REG-R9** — C. ass. art. A341-1, ACPR derogations. The hook by which the PAF becomes a supervisor-approved forward-looking calculation.
- **REG-R13** — HCSF, CMF art. L631-2-1. The surrender-freeze power, its three-month renewable window and the six-consecutive-month cap, and the fact that it has never been triggered ([unverified]).
- **REG-R14** — C. ass. art. L331-3. The primary statutory obligation to share technical and financial results; the current article number is [unverified] after the 2016 recodification.
- **REG-R15** — C. ass. arts. A132-10 to A132-15, the `compte de participation aux résultats`. The article-by-article verification of the 85% / 10%-or-4.5% arithmetic and of the A132-14 basis that puts the PPB inside the financial account.
- **REG-R16** — C. ass. arts. A132-16 and A132-16-1. The eight-year release rule the PPB vintage ledger implements, and the two cumulative conditions for an exceptional `reprise`.
- **REG-R17** — C. ass. arts. A132-1 and A132-1-1, maximum technical rate. Cross-check on R1 and R2.
- **REG-R18** — C. ass. arts. A132-2 and A132-3, TMG. Cross-check on R3 and R4, and the source of the ruling that every modelled TMG is `**[std]**`.
- **REG-R23** — C. ass. art. A335-1 and its Annexe. Which mortality tables a French tariff may use, and the TH 00-02 / TF 00-02 age shifts.
- **REG-R24** — INSEE mortality series. The only freely redistributable French mortality data and the actual source behind the decrement proxy.
- **REG-R29** — C. ass. arts. L132-5-1 and L132-5-2, `renonciation`. The 30-day unwind and its repayment clock.
- **REG-R30** — C. ass. arts. A132-4 and A132-8, `note d'information` and `encadré`. Why the retrieved notices disclose charge **maxima** rather than levels — and therefore why every charge level here is a maximum or `**[std]**`.
- **REG-R31** — C. ass. arts. L132-21, L132-22 and L132-23-1. Surrender settlement; the annual statement and the website publication of average served rates; the death-payment clock.
- **REG-R39** — Loi n° 2014-617 (loi Eckert). Unclaimed contracts, the ten-year transfer to the Caisse des dépôts and the twenty-year escheat.
- **REG-R40** — CGI art. 125-0 A. The duration thresholds and abattements behind the duration-8 surrender step; notes that the EUR 150 000 threshold is [unverified] in the text fetched there.
- **REG-R41** — CGI arts. 990 I and 757 B. Death taxation, and the PER carve-out that does *not* apply to assurance vie.
- **REG-R44** — Institut des actuaires NPA 2, *Modèles actuariels*. The professional standard this model documentation sits under.
- **REG-R45** — IFRS 17. Direct-participating measurement; the variable fee approach's mechanics are [unverified].
- **REG-R47** — France Assureurs, "L'assurance vie en 2024". The independent PPB anchor: EUR 53.6 bn at end-2024, −11.1% year on year, about 4% of euro-support provisions mathématiques.

---

## Provenance note

Extraction details — the per-source facts, the extracted specification sections, the
cross-insurer variation table and the gaps register these documents draw on — live in
`_research/assurance-vie-euro.md`. The cross-product bibliography with full annotations is
`references/regulatory-and-actuarial-references.md`.

**One provenance conflict is worth stating plainly.** The cross-product entry REG-R11
records the ACPR *Analyses et Synthèses* life-market series as **unfetchable**, HTTP 403
with and without a browser User-Agent, and calls that "the most consequential gap in this
library"; it also carries a different URL for n° 179 than the one below. This product's
research reached n° 179 and n° 180 at the URLs recorded at R14 and R15 by re-requesting
them with a browser User-Agent, and extracted their full text. Where the two disagree,
these documents cite **R14, R15 and R16** — the PDFs that were actually downloaded and
read — and no ACPR figure anywhere in them comes from a search-result summary. The
cross-product entry is not cited for any figure.

Gaps inherited by this specification, each visible as a `**[std]**` or [unverified] tag in
the documents: **no TMG value is public** for any contract in the set, and the ACPR's
average `taux technique` is a different quantity; **no insurer publishes its PPB dotation
or release policy**, only the statutory bounds and the aggregate ratio; **no contract
publishes its UC-holding bonus grid**; **`avance` terms are unpublished** by all three
insurers that offer them; the composition of the 17.2% social levy and the base it applies
to were not confirmed against a retrieved text; the capital/gain split of a partial
surrender is not sourced; **no French lapse experience is public** below aggregate market
flows; and **Solvency II could not be read at all**. Six insurer groups across thirteen
retrieved documents support the structural claims here but not a market-wide charge
distribution — for that, use the ACPR's own distribution [R14]. Thirteen, not fourteen:
S1–S14 are the ids, and [S14] 404'd. Carriers named in the research brief but
never reached — AXA France, Sogécap, Predica, Spirica, Groupama, Swiss Life France, BNP
Paribas Cardif, AG2R La Mondiale — are recorded as unresearched, not approximated.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R14]: #frlib-assurance_vie_euro-r14
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
