# Euro-Fund Life Savings Contract (assurance vie — support en euros / fonds en euros) — research notes (France)

Research notes for the French individual life savings contract taken on its euro support — the
`fonds en euros` (euro fund), the capital-guaranteed, profit-participating account that sits inside
almost every French `contrat d'assurance vie`. These notes are the citation ground truth for the
frlib `assurance_vie_euro` product documents: source ids S1..S14 and R1..R18 below are frozen —
never renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document that was
actually fetched and read. `[unverified]` marks statements from general knowledge or from
secondary summaries of documents that could not be retrieved. Where a fetch failed the failure is
recorded and the item is kept only as a known reference (fetched_ok = false).

French terms of art are kept in French with a gloss on first use: `fonds en euros` (euro fund),
`participation aux bénéfices` (profit participation, PB), `provision pour participation aux
bénéfices` (PPB, the collective profit-participation reserve), `taux minimum garanti` (TMG, the
contractual minimum credited rate), `effet cliquet` (ratchet — credited interest is definitively
acquired), `rachat` (surrender), `avance` (policy loan), `arbitrage` (switch between supports),
`notice d'information` (the group-contract policy booklet), `document d'information clé` (DIC — the
PRIIPs KID), `prélèvements sociaux` (social levies), `quotité` (proportion/share).

---

## Primary sources

### S1 — Boursorama / Generali Vie, "BoursoVie — Notice d'information valant Conditions générales" (juillet 2025)
- Publisher: Generali Vie (insurer) and Boursorama / BoursoBank (souscripteur of the group contract)
- Doc type: Notice d'information valant conditions générales, 75 pp.
- URL: https://s.brsimg.com/content/pdf/banque/cg/cg-brsvie.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Dated JUILLET 2025.
- Content: full booklet for a `contrat d'assurance vie de groupe` with euro supports, unités de
  compte (UC) and an eurocroissance support. Dispositions essentielles: capital guarantee on the
  euro part "au moins égale aux sommes versées, nettes de frais"; no contractual PB on the two euro
  funds Eurossima and Euro Exclusif, allocation of technical and financial results governed by
  art. A132-16 of the Code des assurances; euro-fund value computed **daily in compound interest**,
  PB credited at 31 December value date; PB "définitivement acquise" once credited; on in-year
  dénouement (rachat total, décès, terme) only the TMG announced at the start of the year applies
  pro rata temporis; management charge 0.75% max p.a. of the mathematical provision **including the
  PB**, taken at 31 December value date pro rata temporis and again pro rata on a full in-year
  disinvestment; nil entry charges; nil arbitrage charges; partial surrender minimum EUR 1 000 with
  a EUR 1 000 residual account floor; programmed partial surrenders require EUR 10 000 on the euro
  funds; avances governed by a separate Règlement Général des Avances; full tax annexe (PFU rates,
  4 600/9 200 abattement, 990 I, 757 B, IFI, non-resident treatment).

### S2 — MACSF épargne retraite, "Notice d'information RES Multisupport" (réf. 16 10 201 Y, édition 10/2024)
- Publisher: MACSF épargne retraite (insurer); group contract subscribed by the association AMAP
- Doc type: Notice d'information, ~24 pp.
- URL: https://www.macsf.fr/content/download/4098/fichier/MACSF_1610201Y_Notice_information_RES_Multisupport.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Édition 10/2024.
- Content: `contrat d'assurance vie de groupe de type multisupport, à adhésion facultative`. Euro
  support "Fonds en euros RES" with a capital guarantee "égale aux sommes versées, nettes de
  frais"; PB allocated at 31 December each year to the mathematical provision as `intérêts
  complémentaires` **or** to the PPB, sums in the PPB to be applied to mathematical provisions
  "dans un délai maximum de 8 ans"; interim/renunciation-period rate fixed by the board at
  31 December for the following year under art. A132-3, revisable in-year; charges — entry 3% max
  on the euro fund, 1% max on free UC contributions and 0.6% on automatic ones, management 0.50%
  max taken at 31 December, garantie plancher décès/IFTD 0.10% on UC, arbitrage 2% max towards the
  euro fund and 0.20% max towards UC with the first twelve free, exit charges nil, association fee
  EUR 10 (individual) / EUR 20 (joint); minimum eight-year surrender-value table for the euro fund
  (EUR 1 000 single contribution, 3% entry, 0.50% management: 965.15, 960.32, 955.52 … ); avance
  available under a separate Règlement Général des Avances; L132-21 two-month settlement.

### S3 — Suravenir / Meilleurtaux Placement, "Meilleurtaux Placement Vie 2 — Notice" (contrat n° 2282, réf. 5980 (03.2026), mars 2026)
- Publisher: Suravenir (Crédit Mutuel Arkéa); group contract subscribed by the association VIREA
- Doc type: Notice d'information, 20 pp.
- URL: https://placement.meilleurtaux.com/images/docs-av/meilleurtaux-placement-vie-2/meilleurtaux-placement-vie-2-notice.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Dated mars 2026 — the most recent full
  notice in this set.
- Content: branches 20 (Vie-Décès) and 22 (unit-linked). Euro funds Suravenir Rendement 2 and
  Suravenir Opportunités 2 — the encadré states plainly that the contract **does not** carry a
  guarantee equal to premiums net of entry charges; the guarantee is premiums net of entry charges
  **less the annual management charges** and the optional death-cover premiums, increased by PB. No
  contractual PB; PB determined under art. A132-10 and set by the Directoire during Q1. Charges:
  0.00% entry, 0.60% p.a. on Suravenir Rendement 2, 3.00% max on Suravenir Opportunités 2, 0.60% on
  UC, 0.60%/1.20% under the arbitrage mandate, +0.14% if the accidental-death option is taken,
  0.00% arbitrage, 0.10% on ETF trades, 3% on annuity instalments, 1% for settlement in securities.
  Optional death guarantees cover the `capital sous risque` (the contract's loss), ages 12 to under
  70 at adhesion, **one-year waiting period**, no medical formalities, monthly premiums 0.15‰ to
  5.15‰ of capital at risk by age. Eight-year minimum surrender-value table for a EUR 1 000 net
  contribution at 0.60% FAG: 994.00, 988.03, 982.10, 976.21, 970.35, 964.53, 958.74, 952.99.
  Death capital settled within 30 days with penalty interest at double then triple the legal rate;
  surrender settled within 30 days with interest at 1.5× then 2× the legal rate. Tax table:
  PFU 12.8% before 8 years, 7.5% after 8 years below a EUR 150 000 premium threshold and 12.8%
  above, **prélèvements sociaux 17.2%** in every column; 4 600/9 200 abattement after 8 years;
  12.8%/7.5% non-final acompte with a dispense below RFR EUR 25 000 / 50 000.

### S4 — Suravenir / Épargnissimo, "Croissance Avenir — Notice" (contrat n° 2178, réf. 4023-13 (02.2023), février 2023)
- Publisher: Suravenir; group contract subscribed by the association SEREP
- Doc type: Notice d'information, 20 pp.
- URL: https://www.epargnissimo.fr/assets/files/docutheque/croissance-avenir/adhesion-et-gestion-du-contrat/notice.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Dated février 2023.
- Content: the single most useful document in this set for the `garantie brute / garantie nette`
  distinction, because it carries **both** kinds side by side. For the older fund **Suravenir
  Rendement** the contract "comporte une garantie en capital au moins égale aux sommes versées,
  nettes de frais" (gross of management charges); for **Suravenir Rendement 2** and **Suravenir
  Opportunités 2** it explicitly does not, the guarantee being premiums net of entry charges less
  the annual management charges. It also carries a **contractual** PB rate for Suravenir Rendement:
  "une participation aux bénéfices … calculée sur la base d'un taux de participation aux bénéfices
  de 90 %", with the profit account written out in full — credit side: contributions net of
  charges, opening mathematical provisions, incoming switches net of charges, 90% of releases from
  other technical provisions (réserve de capitalisation, provision de gestion, provision pour aléas
  financiers, excluding the PPB), and 90% of the contract's share of net investment income of the
  backing assets; debit side: closing mathematical provisions before revaluation, benefits paid,
  outgoing switches, annual management charges at a maximum rate of 0.60%, 90% of transfers to the
  other technical provisions, any prior-year debit balance, financial and administrative charges,
  and taxes; the whole positive balance is carried to the PPB common to contracts backed by the
  same asset pool. Charges as in S3 (0.00% entry, 0.60%/3.00% max/0.60%, 0.60%/0.80% under mandate).

### S5 — Suravenir, "Document d'informations spécifiques — Fonds en Euros Actif Général" (mise à jour 05/08/2026)
- Publisher: Suravenir
- Doc type: Document d'informations spécifiques (PRIIPs-style disclosure for the euro fund as an
  investment option), 3 pp.
- URL: https://espaceclient.suravenir.fr/o/documents/WsPUS/DIS_OPC/VIE00000CESR.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Update date 05/08/2026.
- Content: the euro fund described as a product in its own right. Predominantly bond allocation;
  "garantie en capital au moins égale aux montants nets investis"; the performance-scenario note
  states the guarantee is premiums net of entry charges "minorée chaque année des frais de gestion
  prélevés sur le contrat". Risk indicator **1 of 7**, the lowest class. Recommended minimum
  holding period **1 year** (contrast with the 8-year holding period quoted at contract level for
  tax reasons). No maturity date; unilateral surrender at any time, subject to the possibility of
  HCSF limitation described as "temporaire (maximum 6 mois renouvelable)". Costs internal to the
  fund only: entry 0.00%, exit 0.00%, management and other administrative/operating costs 0.24% of
  investment per year, transaction costs 0.03% per year, total EUR 48.37 on EUR 10 000 over one
  year = 0.48% impact — explicitly **excluding** the contract's own charges. Performance scenarios
  over one year on EUR 10 000: stress / unfavourable / intermediate all EUR 10 000 (0.00%),
  favourable EUR 10 268 (2.68%), based on the last six years.

### S6 — CNP Assurances, "Document d'informations clés — NUANCES 3D" (produced 22/07/2026)
- Publisher: CNP Assurances (groupe La Banque Postale), distributed through the BPCE network
- Doc type: DIC (PRIIPs KID), 3 pp.
- URL: https://dic.cnp.fr/wkd-web/kid-webapi/document/dic/BPCE/858
- Retrieved: YES (PDF downloaded, full text extracted). Production date 22/07/2026.
- Content: `contrat d'assurance de groupe sur la vie, à adhésion facultative`, euro and UC, now open
  only for the transformation of an existing life contract; maturity fixed between 10 and 30 years,
  renewable annually without limit. The euro support Nuances 3D Euro is "investi principalement en
  actifs obligataires" and its return "dépendra du taux de participation aux bénéfices qui pourra
  éventuellement être attribué au 31 décembre de chaque année". Carries the clearest statement of
  the **net guarantee**: "le contrat ne comporte pas de garantie en capital au moins égale aux
  sommes versées nettes de frais sur versement, mais il comporte une garantie en capital au moins
  égale aux sommes versées, nettes de frais sur versement et nettes de frais de gestion annuels".
  30-day renunciation; surrender settled within 30 days; recommended holding period 8 years "compte
  tenu de la fiscalité en vigueur". FGAP compensation capped at EUR 70 000 per insured per company.
  Aggregate cost disclosure across all underlying options: total costs on EUR 10 000 between
  EUR 489.23 and EUR 1 157.16 if exiting after 1 year (4.89%–11.57%), and between EUR 1 268.91 and
  EUR 10 385.95 if exiting after 8 years (1.65%–5.48% p.a.); entry-cost impact at 8 years 0.45% to
  1.09% p.a.; exit costs nil.

### S7 — CNP Assurances, "Document d'informations clés — NUANCES PLUS" (produced 22/07/2026)
- Publisher: CNP Assurances
- Doc type: DIC (PRIIPs KID)
- URL: https://dic.cnp.fr/wkd-web/kid-webapi/document/dic/BPCE/859
- Retrieved: YES (PDF downloaded, full text extracted). Production date 22/07/2026.
- Content: same architecture as S6. Confirms the identical net-of-management-charges guarantee
  wording for the euro support Nuances Plus Euro, and the same dependence of the return on the PB
  rate awarded at 31 December.

### S8 — CNP Assurances, "Document d'informations clés — PERSPECTIVE CAPI"
- Publisher: CNP Assurances, distributed through La Banque Postale
- Doc type: DIC (PRIIPs KID)
- URL: https://dic.cnp.fr/wkd-web/kid-webapi/document/dic/LBP/C3C
- Retrieved: YES (PDF downloaded, full text extracted; the production date line was truncated in
  extraction and is not quoted here).
- Content: a **contrat de capitalisation individuel nominatif** (not an assurance vie), euro and UC,
  30-year maturity, extendable. Included deliberately as a contrast: here the euro support carries
  "une garantie en capital au moins égale aux sommes versées nettes de tous frais" — the gross-style
  guarantee, against the net-of-management-charges guarantee of S6/S7 from the same insurer.

### S9 — Aviva Vie / Aviva Épargne Retraite (now Abeille Vie / Abeille Épargne Retraite), "Contrat collectif d'assurance vie Multisupport Afer — Notice" (réf. 60121-1021, édition 10/2021)
- Publisher: co-insurers Aviva Vie and Aviva Épargne Retraite; contract subscribed by the
  association Afer
- Doc type: Notice d'information, ~56 pp. plus annexes
- URL: https://www.afer.fr/content/uploads/2022/02/60121-1021-notice-contrat-collectif-assurance-vie-multisupport-afer.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Édition 10/2021 — pre-rebranding vintage;
  the insurers are now Abeille Vie and Abeille Épargne Retraite (see S10, S11).
- Content: the association-run model. Euro support "Fonds Garanti en euros" with a capital guarantee
  "au moins égale aux sommes investies sur l'adhésion nettes de frais sur versements" (gross of
  management charges). PB clause: "une participation aux bénéfices égale à **100 %** des bénéfices
  financiers nets du Fonds Garanti en euros cantonné, distribuée après dotation ou reprise
  éventuelle à la provision pour participation aux bénéfices". Effet cliquet stated twice — the
  insurers "garantissent définitivement le maintien total des résultats acquis au 31 décembre de
  chaque année par un mécanisme appelé « effet de cliquet »", and once the year's allocation has
  been credited "elle ne peut plus être remise en cause"; the glossary defines effet de cliquet as
  the mechanism consolidating each year's return so that it cannot be called back and does not
  suffer market fluctuations, and notes it is reserved to euro contracts and to the euro funds of
  multisupport contracts. PPB dotation, management and release are decided jointly through the
  Comité de Surveillance de la Gestion des Fonds de l'Afer within the Code des assurances limits.
  Charges: 0.5% on contributions destined for the Fonds Garanti, nil on UC and on eurocroissance;
  0.475% p.a. management on the Fonds Garanti (after PB allocation) and on UC; 0.89% p.a. on the
  eurocroissance support; nil exit; nil arbitrage; non-optional death floor guarantee costing
  0.055% p.a. of UC and eurocroissance savings; asset-management charge on the Fonds Garanti capped
  at 0.1% of assets under management excluding OPCVM.

### S10 — Afer / Abeille Vie, "Multisupport Afer — Tableau des frais" (réf. 60142C - 2405, mai 2024)
- Publisher: Abeille Vie and Abeille Épargne Retraite, published on afer.fr
- Doc type: Standardised fee table ("tableau des frais" / fiche de transparence des frais), 2 pp.
- URL: https://www.afer.fr/content/uploads/2024/07/60142c-05-2024-fiche-transparence-des-frais-afer-multisupport-3-1.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Dated mai 2024.
- Content: minimum initial payment EUR 100; association fee EUR 20; annual charges — euro support
  0.475%, UC 0.475% plus the fund's own charges, eurocroissance 0.890%; average UC fund charges by
  asset class (equities 1.05%, bonds 0.74%, real estate 0.91%, diversified 1.45%) with the
  retrocession share shown; managed-portfolio profiles 1.01%–1.26%; death floor 0.055%.
  One-off charges at maximum rate: **0.5% on contributions to the Fonds Garanti en euros**, 0%
  additional on UC and eurocroissance; 0% mode-change; **0% arbitrage, unlimited free switches**;
  0% outgoing transfer; **3% on annuity instalments**; **0% surrender**.

### S11 — Afer, "Performances des supports à capital garanti" (web page)
- Publisher: Association Afer (afer.fr)
- Doc type: Product/performance page
- URL: https://www.afer.fr/performances-des-supports-a-capital-garanti/
- Retrieved: YES (HTML fetched with a browser User-Agent and converted to text; the PDFs linked from
  the page are loaded by script and were not retrieved).
- Content: Fonds Garanti en euros created in 1976, encours EUR 40 bn at 31/12/2024, managed by Ofi
  Invest Asset Management, mainly high-quality bonds with limited equity exposure; guaranteed at all
  times by Abeille Vie and Abeille Épargne Retraite. Two mechanics named explicitly: the **effet de
  cliquet**, and a **Taux Plancher Garanti** — an interim floor rate used in-year, pro rata temporis,
  to remunerate capital on rachat total or death settlement, with a top-up at the start of the
  following year equal to the difference between the definitive fund return and the floor rate; the
  floor is agreed each year between Afer and the insurers "dans le strict respect des textes
  règlementaires en vigueur". At 31 December each year the year's interest is added definitively to
  the capital. 2025 results: Fonds Garanti en euros **2.65%**, Afer Fonds Euros Retraite **3.50%**
  (management charge 0.625% p.a., insurer Abeille Retraite Professionnel), Afer Eurocroissance
  management charge 0.89% p.a. and closed to adhesions opened since 2 October 2020, valued weekly
  each Wednesday, capital guaranteed only at a term chosen between 10 and 40 years.

### S12 — Afer, "Communiqué de presse : Bilan et performances 2025" (web page)
- Publisher: Association Afer
- Doc type: Press-release landing page
- URL: https://www.afer.fr/espace-presse/communique-de-presse-resultats-2025/
- Retrieved: YES (HTML fetched with a browser User-Agent and converted to text; the linked PDF press
  release itself was not downloaded).
- Content: 748 000 members and close to EUR 57 bn of assets. 2025 rates, each stated "net de frais
  de gestion et hors prélèvements sociaux et fiscaux": Afer EuroGénération **4.05%**, Fonds Garanti
  en euros **2.65%**, Afer Fonds Euros Retraite **3.50%**.

### S13 — MAIF / MAIF VIE, "Les frais de l'assurance vie — Assurance vie Responsable et Solidaire" (réf. TDF16 - 06/26, situation au 02/06/2026)
- Publisher: MAIF VIE (insurer); group contract subscribed by MAIF
- Doc type: Standardised fee table, 2 pp. (served as a PDF from the maif.fr page URL)
- URL: https://www.maif.fr/tableau-frais-ars
- Retrieved: YES (PDF downloaded, text extracted row-wise). Situation date 02/06/2026.
- Content: minimum initial payment **EUR 30**; no association fee. Annual charges: **euro support
  0.80%**, UC 0.80%, plus 0.25% for the delegated-management option; UC fund charges by class
  (equities 1.40%, bonds 0.93%, real estate 1.81%, diversified 1.49%, private equity/private debt
  1.63%, money market 0.20%) with retrocession shares. One-off charges at maximum: **frais sur
  versement 0%**; mode change EUR 0; **arbitrage EUR 15, one free per year**; outgoing transfer
  EUR 0; **3% on annuity instalments**; **surrender EUR 0**.

### S14 — Afer, "Contrat collectif d'assurance vie — Notice, édition janvier 2025, Afer Génération"
- Publisher: Abeille Vie / Abeille Épargne Retraite for the Afer Génération contract
- Doc type: Notice d'information
- URL: https://www.afer.fr/content/uploads/2025/01/60190a-2501-dd-8549-avec-annexes-1.pdf
- Retrieved: NO — HTTP 404 (the file is no longer at that path). Kept as a known reference only. The
  Afer Génération euro fund (Afer EuroGénération) is covered here only through S11 and S12; its
  contractual mechanics, including the eight-year loyalty bonus reported on afer.fr, are
  **[unverified]** against a notice.

---

## Regulatory and actuarial references

### R1 — Code des assurances, article A132-1 (maximum technical interest rate)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514601
- Retrieved: YES (version in force from 07/09/2017).
- Content: tariffs for life insurance and capitalisation must be built on a rate at most equal to
  **75% of the taux moyen des emprunts de l'État français (TME)** computed on a six-month basis.
  For contracts of more than eight years the rate may not exceed the **lower of 3.5% and 60% of the
  TME**; the same 3.5%/60% ceiling applies to periodic-premium and variable-premium contracts
  whatever their duration. Foreign-currency contracts use the equivalent long-term state borrowing
  rate with the same 60% cap beyond eight years. The higher of the issuance rate and the secondary
  market yield is taken. The applicable ceiling is assessed at subscription, and for non-programmed
  payments at each payment date.

### R2 — Code des assurances, article A132-1-1 (the monthly reference rate and the 0.25-point scale)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039801948
- Retrieved: YES (version dated 01/01/2020).
- Content: the `taux de référence mensuel` is the six-month average of state borrowing rates
  multiplied by 60% or 75%. The maximum technical rate moves on a scale of origin 0 and step
  **0.25 point**, floored at 0. It stays unchanged as long as the reference rate has not fallen by
  at least **0.1 point** or risen by at least **0.35 point**; when it does, the new maximum
  technical rate is the rate immediately below the reference rate on the 0.25-point scale. Insurers
  have **three months** to implement a change.

### R3 — Code des assurances, article A132-2 (permission to guarantee a minimum rate)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514622
- Retrieved: YES (version dated 07/09/2017).
- Content: insurers and supplementary pension funds may, under the conditions of article A132-3,
  guarantee in their contracts a **total of technical interest and profit participation** which,
  related to the fraction of the mathematical provisions covered by the guarantee, is not lower than
  guaranteed minimum rates. This is the legal home of the TMG: it is a floor on **interest plus
  PB**, not a separate credit.

### R4 — Code des assurances, article A132-3 (caps on the taux minimum garanti)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514611
- Retrieved: YES (version in force from 07/09/2017).
- Content: guaranteed rates may not exceed the lower of **150% of the maximum technical interest
  rate** (itself referenced to 75% of the TME at the guarantee's effective date) and, alternatively
  capped at, the **higher of 120% of the maximum technical rate and 110% of the average of the
  average rates credited to policyholders over the last two financial years**. A guaranteed rate
  must be fixed for a continuous period of **at least six months and at most the period running to
  the end of the following financial year**, with an exception allowing a shorter period for an
  individual subscriber where the whole group has benefited since the start of the year. Newly
  authorised undertakings may use 120% of the maximum technical rate for up to two years.
  Guaranteed participations for the current **and** the following year are charged against the
  ceiling, unless the undertaking has not explicitly fixed the value of the rate, in which case only
  the current year counts.

### R5 — Code des assurances, Section V "Participation aux bénéfices techniques et financiers", articles A132-10 to A132-17
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000031738019/
- Retrieved: YES (section page listing the articles with their version dates).
- Content: **A132-10** (v. 07/09/2017) sets the minimum profit participation for life insurers and
  supplementary pension funds, applying to individual and collective contracts of all kinds and
  excluding variable-capital contracts. **A132-11** (v. 16/06/2021) defines the `compte de
  participation aux résultats`: the technical component covers underwriting results and management
  charges for categories 1 to 7; the insurer's retained share of the technical result is the
  **greater of 10% of the credit balance and 4.5% of annual premiums** — i.e. at least **90%** of
  the technical result goes to policyholders; and **85% of the balance of a financial account** is
  credited to the participation account. **A132-16** (v. 01/01/2020) allows the participation to be
  credited directly to mathematical provisions or carried to the profit-participation provision, and
  requires sums in that provision to be applied to mathematical provisions or paid to policyholders
  **within the eight financial years following** the year in which they were carried there.
  **A132-17** (v. 07/09/2017) requires equal treatment of paid-up and premium-paying contracts of
  the same category and the same mathematical provision.

### R6 — Code des assurances, articles A331-3, A331-4 and A331-9 (pre-2016 numbering of the same rules)
- Publisher: Légifrance
- URLs:
  - A331-3 https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006787891/2006-08-26
  - A331-4 https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006787932
  - A331-9 https://www.legifrance.gouv.fr/affichCodeArticle.do?categorieLien=cid&cidTexte=LEGITEXT000006073984&dateTexte=&idArticle=LEGIARTI000006787955
- Retrieved: YES for all three, but Légifrance served **historic versions**: A331-3 as in force
  25/10/1995–02/05/2007, A331-4 as in force 14/09/2014–01/01/2016, A331-9 as in force
  27/08/1995–01/01/2016. These articles were the numbering used before the 2015/2016 recast into
  A132-10 et seq. [R5].
- Content: A331-3 — the obligation to distribute a minimum share of technical and financial results
  applies to individual and collective contracts of all kinds written in France, excluding
  collective death-benefit contracts, and does not apply to variable-capital contracts. A331-4 — the
  minimum participation is determined globally from a participation account; the insurer's share of
  the technical result is the greater of 10% of the credit balance and 4.5% of annual premiums, and
  **85% of the financial account balance** is credited. A331-9 — the participation may be credited
  directly to mathematical provisions or carried, partly or wholly, to the profit-participation
  provision, and sums so carried must be applied to mathematical provisions or paid to subscribers
  **within the eight financial years following**. Because the retrieved texts are historic versions,
  cite R5 for anything relied on as current law.

### R7 — Code des assurances, article L132-21 (surrender value, transfer value, two-month deadline)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030461815
- Retrieved: YES (version dated 01/01/2016).
- Content: the insurer must pay the surrender value at the contractant's request within a period
  **not exceeding two months**; transfer values must be remitted to the receiving undertaking within
  periods set by decree. Beyond those deadlines unpaid sums bear interest of right at the legal rate
  **increased by half for two months, then at double the legal rate**. The contract must state how
  the surrender value, the transfer value and the paid-up value are calculated, and no reduction
  charge may be deducted from the mathematical provision on the basis of contractual tariff
  parameters.

### R8 — Code monétaire et financier, article L631-2-1 (Haut Conseil de stabilité financière — the loi Sapin 2 powers)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034386882
- Retrieved: YES (version in force from 08/04/2017).
- Content: paragraph **5° bis** lets the HCSF modulate the rules for constituting and releasing the
  `provision pour participation aux bénéfices` for the insurance undertakings concerned.
  Paragraph **5° ter** lets it take conservatory measures: temporarily limiting the payment of
  surrender values, restricting the free disposal of assets, temporarily limiting the ability to
  make arbitrages or to grant advances, and limiting the acceptance of premiums. Measures under
  5° ter are decided "pour une période maximale de **trois mois**, qui peut être renouvelée", with
  the surrender-value restriction subject to the stricter limit that it "ne peuvent être maintenues
  plus de **six mois consécutifs**"; renewal requires prior consultation of the advisory committee
  on financial legislation and regulation. The introduction of these powers by loi n° 2016-1691
  (loi Sapin 2), article 49, is **[unverified]** — the statute itself was not retrieved.

### R9 — Code de la sécurité sociale, article L136-7 (CSG on investment products — the timing rule)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288474
- Retrieved: YES (version dated 21/02/2026).
- Content: this is the article that makes the French euro fund distinctive for a cash-flow model.
  Products attached to bons or contrats de capitalisation **whose rights are expressed in euros** are
  charged **"lors de leur inscription au bon ou contrat"** — when they are credited to the contract,
  i.e. annually as the PB is added — while the unit-linked portion is charged at dénouement or on
  the insured's death. On a partial surrender of a contract whose UC portion has already borne the
  contribution, the taxable base is computed pro rata on premiums. The article does not state a rate;
  it refers to the rate fixed at article L136-8.

### R10 — Code général des impôts, article 125-0 A (income taxation of life-insurance products)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044989424
- Retrieved: YES (version dated 01/01/2022).
- Content: annual abattement of **EUR 4 600** (single, divorced, widowed) or **EUR 9 200** (married
  or PACS, joint taxation), applied to the aggregate taxable products of all the taxpayer's
  contracts, for contracts of at least eight years (six years for 1983–1989 subscriptions). Flat
  withholding at **12.8%**, reduced to **7.5%** where the duration condition is met, for premiums
  paid from 27 September 2017. Exemption where the contract ends because of the beneficiary's
  redundancy (`licenciement`), second- or third-category invalidity, or conversion into a life
  annuity. The EUR 150 000 premium threshold is not in this article; it is in article 200 A [R11].

### R11 — Code général des impôts, article 200 A (the prélèvement forfaitaire unique and the EUR 150 000 threshold)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053546896
- Retrieved: YES (version dated 21/02/2026).
- Content: default flat rate **12.8%**. For life-insurance products from premiums paid from
  27 September 2017 on a contract of at least eight years, the reduced rate applies to the products
  corresponding to outstanding premiums **within EUR 150 000**; above that threshold only a fraction
  of the products qualifies, obtained by multiplying total products by the ratio of the EUR 150 000
  threshold (reduced by pre-27-September-2017 premiums) to post-27-September-2017 premiums; the
  remaining fraction is taxed at 12.8%. The taxpayer may make an express global option for the
  progressive `barème` covering all income otherwise subject to the PFU.

### R12 — Code général des impôts, article 990 I (death levy on premiums paid before age 70)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288653
- Retrieved: YES (version dated 11/03/2023).
- Content: sums due by an insurer by reason of the insured's death, and not falling under article
  757 B, bear a levy after a flat abattement of **EUR 152 500 per beneficiary**, at **20%** on the
  fraction up to **EUR 700 000** and **31.25%** above. Beneficiaries exempt from gift/transfer duties
  under articles 795, 795-0 A, 796-0 bis and 796-0 ter (spouse, PACS partner, and siblings meeting
  the statutory conditions) are outside the levy.

### R13 — Code général des impôts, article 757 B (death duties on premiums paid after age 70)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288569
- Retrieved: YES (version dated 11/03/2023).
- Content: sums due by an insurer by reason of the insured's death are subject to droits de mutation
  par décès according to the beneficiary's relationship to the deceased, but only on **the fraction
  of premiums paid after the insured's seventieth birthday** — the accumulated products are not
  taxed under this article — after a **global EUR 30 500 abattement** covering all contracts on the
  same life. Retirement savings products under articles L224-1 and L225-1 of the Code monétaire et
  financier are taxed in full where the holder dies after 70, whatever the timing of premiums.

### R14 — ACPR, "Revalorisation 2025 des contrats d'assurance-vie et de capitalisation", Analyses et synthèses n° 180 (30 June 2026)
- Publisher: Autorité de contrôle prudentiel et de résolution / Banque de France
- URL: https://acpr.banque-france.fr/system/files/2026-06/20260630_AS180_revalorisation_2025.pdf
- Retrieved: YES — but note the route: WebFetch returned HTTP 403 twice on both the publication page
  and the PDF; the PDF was then downloaded successfully with a browser User-Agent and its full text
  extracted. Study by Jean-Luc Coron with Frédéric Ahado; covers **116 undertakings and 36 053
  contract versions**; unit-linked contracts are outside its scope except in a dedicated box.
- Content: the single most load-bearing quantitative reference for this product. Euro-support
  mathematical provisions of individual contracts EUR 1 207 bn end-2025 (EUR 1 178 bn end-2024,
  +2.5%); collective EUR 154 bn (EUR 147 bn, +4.7%). Average **taux de revalorisation 2.63%** for
  individual contracts in 2025, unchanged on 2024, "nets de prélèvements sur encours et avant
  prélèvements sociaux"; 2.64% for collective contracts (2.53% in 2024). Dispersion: undertakings
  representing 50% of encours credited between 2.3% and 2.9% (a 0.6 point band, against 2.2%–3.0%
  in 2024); within a single insurer, the spread between the best- and worst-revalued homogeneous
  contract groups (90th vs 10th percentile by mathematical provisions) averaged **0.99 point**
  (0.77 in 2024), and the least-revalued group sits **0.39 point** below the mean (0.40 in 2024);
  UC-holding bonuses "souvent de 100 points de base, et allant jusqu'à plus de 200 points de base".
  By type: bancassureurs (65% of encours) 2.70%, traditional insurers 2.48%, mutuelles (2% of
  encours) 3.17%. Category 4 contracts are about 92% of individual euro encours. Asset-side: the
  `taux de rendement de l'actif` (TRA) rose to **2.8%** in 2025 (2.5% in 2024, near 2.1–2.2% from
  2020 to 2023); bonds are about 60% of life insurers' investments; half of undertakings show a TRA
  between 2.4% and 3.3%; about 60% of fixed-coupon bonds maturing within four years carry a coupon
  below 3%. Market context: 10-year OAT averaged 3.4% in 2025, Livret A 2.2%, inflation +0.9%.
  **PPB**: 4.0% of life provisions for individual contracts end-2025 (4.3% end-2024) and 2.0% for
  collective (1.9%); by type 4.2% for bancassureurs (4.6%) and 3.6% for traditional insurers (3.5%),
  bancassureurs having released significant amounts while traditional insurers added to theirs.
  **Taux technique** (average, weighted by mathematical provisions): individual 0.39/0.37/0.36/0.37/
  0.35/**0.32%** for 2020–2025; collective 1.24/1.21/1.12/1.04/1.01/**0.98%**; "l'essentiel des
  contrats actuellement commercialisés en France a un taux technique faible ou nul". **Taux de
  chargement** paid by policyholders on euro supports: individual **0.63%** in 2025 (0.62% in 2024),
  0.64% for traditional insurers and 0.63% for bancassureurs; collective 0.47% (0.42%), 0.58% for
  bancassureurs and 0.42% for ORPS; half of all undertakings between 0.5% and 0.8%. Footnote 12
  states the sharing rule directly: "les dispositions du Code des assurances (article A. 132-10 et
  suivants) prévoient que seulement 85 % du compte financier … lui est destiné pour sa
  revalorisation, directement ou par l'intermédiaire de la PPB. Certains contrats peuvent
  contractuellement prévoir un pourcentage plus élevé." Box 2 summarises Débats économiques et
  financiers n° 50, "Mutualisation intercohortes des risques dans les contrats d'assurance-vie en
  euros en France": over 1999–2023 the smoothing divides the volatility of credited rates by five
  relative to financial markets, reserves redistribute about **1.6% of encours per year**, contracts
  held 2006–2011 gained an extra 1.6% p.a. while those held 2012–2021 contributed 2.3% p.a. to
  building the reserves. Definitions box: taux de revalorisation = the contract's "rendement garanti
  et participation aux bénéfices techniques et financiers" per articles L132-22 and A132-7, gross of
  the technical rate and of tax and social levies but **net of charges on encours**; taux technique =
  the maximum rate at which the insurer's commitments are discounted, fixed at subscription and
  limited by A132-1, never reduced by charges, and a floor the credited rate cannot fall below.

### R15 — ACPR, "L'assurance-vie en 2025", Analyses et synthèses n° 179 (22 May 2026)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/system/files/2026-05/20260522_AS_Assurance_vie_2025.pdf
- Retrieved: YES (403 on the publication page via WebFetch; PDF downloaded with a browser
  User-Agent and text extracted). Based on the ACPR's weekly and quarterly flow collection from
  about 90 undertakings, roughly 70 for life.
- Content: 2025 flows — premiums EUR 159.1 bn, benefits EUR 115.1 bn of which surrenders EUR 71.0 bn
  and claims EUR 44.1 bn; **net inflow EUR 44.0 bn**, the highest since the series began in 2011 and
  93.1% above the 2024 peak of EUR 22.8 bn, driven by premiums +12.2% and surrenders −6.3%. Split:
  euro supports **+EUR 6.4 bn**, positive again after five consecutive years of net outflow;
  UC +EUR 37.6 bn (85% of the total). Preliminary estimate of the 2025 euro revaluation rate
  **2.65%** net of charges on encours and before social levies, against a Livret A rate falling from
  2.4% to 1.7% in August 2025 and 1.5% in February 2026. Capital-guaranteed contracts EUR 1 361 bn
  end-2025; UC encours EUR 612 bn end-2025 against EUR 343 bn end-2016; UC have returned about 2.0%
  a year net of fund and contract charges since 2020. Assurance vie and retirement savings are 32.9%
  of French households' financial wealth, EUR 2 153.5 bn. Non-surrenderable contracts (mostly
  retirement) took in EUR 8.8 bn net, PER +EUR 12.8 bn.

### R16 — ACPR, "Revalorisation 2024 des contrats d'assurance-vie et de capitalisation", Analyses et synthèses n° 175 (4 August 2025)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/system/files/2025-08/20250804_AS175_Revalorisation_contrats_assurance_vie_2024.pdf
- Retrieved: YES (downloaded with a browser User-Agent, text extracted). **Caveat: the published PDF
  carries an "ACPR-RESTREINT" marking in its page header although it is served from the ACPR's
  public publications area.** It is used here only for prior-year comparatives that R14 restates.
- Content: euro-support mathematical provisions EUR 1 178 bn (individual) and EUR 147 bn (collective)
  end-2024; category "contrats individuels à prime unique ou versements libres (y compris groupes
  ouverts)" more than 91% of individual encours; collective "contrats collectifs en cas de vie" 71%
  of retirement encours. Average revaluation 2.63% individual (+3 bp) and 2.53% collective (+2 bp) in
  2024, after a two-year rise of +66 bp and +42 bp respectively. PPB 4.3% of life provisions for
  individual contracts end-2024 against **4.9% end-2023**, and 1.9% collective against 2.0%. Average
  technical rate 0.35% (individual) and 1.01% (collective); average charge rate 0.62% and 0.42%.

### R17 — France Assureurs, "Nos chiffres clés — L'assurance vie" (web page)
- Publisher: France Assureurs (the French insurance trade body)
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/lassurance-vie/
- Retrieved: YES (HTML fetched with a browser User-Agent and converted to text).
- Content: **EUR 2 088 bn** of assurance vie encours at end-2025; **EUR 75.9 bn** of unit-linked
  contributions in 2025, up 14.4%; EUR 19.3 bn of contributions in June 2026 alone. (The page is a
  headline-figures dashboard; the underlying statistical notes were not retrieved.)

### R18 — Commission Delegated Regulation (EU) 2015/35 (Solvency II delegated acts)
- Publisher: EUR-Lex
- URL: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R0035
- Retrieved: NO — EUR-Lex returned an empty body via WebFetch and HTTP 202 with a zero-length body
  to a direct fetch. Kept as a known reference only. Nothing in these notes relies on its text; the
  Solvency II treatment of `future discretionary benefits` (the PPB and the discretionary share of
  the euro fund's return), of management actions and of the time value of options and guarantees is
  deferred to the cross-product reference library and is **[unverified]** here.

---

## Extracted specifications

### 1. Contract form and legal wrapper
- The dominant retail form is a **`contrat d'assurance vie de groupe` à adhésion facultative**: a
  group policy signed between an insurer and a subscribing body (an association or a bank), which
  individuals join by `adhésion`. Verified across BoursoVie (Generali Vie / Boursorama) [S1], RES
  Multisupport (MACSF épargne retraite / association AMAP) [S2], Meilleurtaux Placement Vie 2
  (Suravenir / association VIREA) [S3], Croissance Avenir (Suravenir / association SEREP) [S4],
  Multisupport Afer (Aviva–Abeille co-insurers / association Afer) [S9] and Nuances 3D (CNP
  Assurances) [S6].
- Genuinely **individual** contracts also exist: CNP's Perspective Capi is a "contrat de
  capitalisation individuel nominatif" [S8]. A `contrat de capitalisation` is not an assurance vie —
  it has no insured life and no beneficiary clause — but its euro support behaves identically.
- Group-contract governance: the subscribing association's general meeting alone may authorise
  changes to the `dispositions essentielles` defined at art. R141-6 of the Code des assurances, may
  delegate signature of avenants to its board for at most eighteen months, must inform members at
  least three months before an avenant takes effect (art. L141-4), and on termination of the group
  contract existing adhesions continue (art. L141-6) with no further payments accepted [S3].
- Underwriting classification: branches **20 (Vie-Décès)** and **22** (contracts linked to
  investment funds) [S3].
- Association membership fees where an association subscribes: EUR 20 one-off (Afer) [S9][S10];
  EUR 10 individual / EUR 20 joint (MACSF/AMAP) [S2]; none for MAIF [S13].
- Recommended holding period is **8 years**, and the reason given is fiscal, not economic: "Durée de
  détention recommandée : 8 ans compte tenu de la fiscalité en vigueur" [S6]. MACSF states a default
  contract duration of at least eight years [S2]. The euro **support** on its own carries a
  recommended minimum holding period of only **1 year** [S5].
- Premium forms: a `versement initial` (initial payment), `versements libres` (ad-hoc top-ups) and
  `versements libres programmés` (regular contributions) — all three offered on BoursoVie [S1]. A
  `versement unique` (single premium) is simply the case where no further payments are made; none of
  the retrieved notices restricts the contract to one payment.
- Multisupport vs monosupport: every contract retrieved here is **multisupport** — the euro fund is
  one support among UC and, in two cases, an eurocroissance support [S1][S2][S3][S4][S9]. A
  monosupport euro contract is the degenerate case with the UC allocation set to zero; no
  monosupport notice was retrieved, so the claim that monosupport contracts are now rarely marketed
  is **[unverified]**.

### 2. The capital guarantee — `garantie brute` versus `garantie nette`
This is the single most important contractual distinction for a cash-flow model, and the retrieved
documents split cleanly.

- **Gross-style guarantee (floor = premiums net of entry charges only).**
  - Suravenir Rendement (the older fund): "le contrat comporte une garantie en capital au moins
    égale aux sommes versées, nettes de frais" [S4].
  - Multisupport Afer, Fonds Garanti en euros: "une garantie en capital au moins égale aux sommes
    investies sur l'adhésion nettes de frais sur versements" [S9].
  - CNP Perspective Capi: "une garantie en capital au moins égale aux sommes versées nettes de tous
    frais" [S8].
- **Net-of-management-charges guarantee (floor erodes each year by the management charge).**
  - Suravenir Rendement 2 and Suravenir Opportunités 2: the encadré says outright that the contract
    "ne comporte pas de garantie en capital au moins égale aux sommes versées, nettes de frais"; the
    body defines the guarantee as premiums net of entry charges "diminuées des frais annuels de
    gestion" and of any optional death-cover premiums [S3][S4].
  - CNP Nuances 3D and Nuances Plus: "ne comporte pas de garantie en capital au moins égale aux
    sommes versées nettes de frais sur versement, mais … nettes de frais sur versement et nettes de
    frais de gestion annuels" [S6][S7].
  - Suravenir's fund-level disclosure states the same in one line: guarantee equal to premiums net
    of entry charges "minorée chaque année des frais de gestion prélevés sur le contrat" [S5].
- **The numbers.** Suravenir publishes the minimum surrender values for a EUR 1 000 net contribution
  on Suravenir Rendement 2 at a 0.60% management charge, with no PB: 994.00, 988.03, 982.10, 976.21,
  970.35, 964.53, 958.74, **952.99** at the end of years 1 to 8 [S3]. That is exactly
  1 000 × (1 − 0.006)^n. MACSF publishes the same construction for a EUR 1 000 single contribution
  at 3% entry and 0.50% management: 970 net, then 965.15, 960.32, 955.52 … , i.e. 970 × 0.995^n [S2].
- **The MACSF wording is not decisive.** Its encadré describes the euro guarantee as "égale aux
  sommes versées, nettes de frais" — which reads gross — yet its own eight-year table shows the floor
  falling at 0.50% a year [S2]. Where a notice says "nettes de frais" without qualifying which
  charges, only the surrender-value table settles the question.
- The market shift from gross to net guarantees around 2010 is widely described but is
  **[unverified]** here: no retrieved document dates the change. What is verified is that a single
  insurer can run both designs at once — Suravenir's Rendement is gross and its Rendement 2 is net,
  inside the same notice [S4].
- The guarantee is a floor on the **account value**, not a return promise: the euro fund's risk
  indicator is **1 of 7**, and in the stress, unfavourable and intermediate one-year scenarios the
  investor gets back exactly EUR 10 000 on EUR 10 000, with a favourable scenario of EUR 10 268
  (2.68%) [S5].

### 3. Effet cliquet — the ratchet
- Definition, from the Afer glossary: "Mécanisme qui permet de consolider les rendements acquis
  chaque année. Ils ne peuvent pas être remis en cause et ne subissent pas la fluctuation des
  marchés financiers. Cet effet de cliquet est réservé aux contrats en euros ou aux fonds en euros
  des contrats multisupport." [S9]
- Operative wording: the insurers "garantissent définitivement le maintien total des résultats
  acquis au 31 décembre de chaque année par un mécanisme appelé « effet de cliquet » : au 31 décembre
  de chaque année, la rémunération de l'année écoulée s'ajoute à l'épargne constituée sur le Fonds
  Garanti en euros" [S9]; and once a year's distribution has been credited "elle ne peut plus être
  remise en cause" [S9].
- Same mechanic on a bancassurance contract: "La participation aux bénéfices vient augmenter la
  valeur atteinte sur ce fonds et est alors définitivement acquise à l'adhésion. Elle sera,
  elle-même, revalorisée dans les mêmes conditions que les versements effectués" [S1].
- **Crediting date and compounding.** BoursoVie: the euro-fund account value is computed **daily in
  compound interest**, and the annual PB is credited at **31 December value date**, including for
  sums surrendered or switched during the year provided the adhesion is still in force on the
  following 1 January [S1]. MACSF credits at 31 December [S2]. CNP describes the PB as awarded "au
  31 décembre de chaque année" [S6][S7]. Suravenir's board decides the PB during **Q1 of the
  following year** and applies it to the contract [S3][S4].
- **Charge interaction.** BoursoVie's 0.75% management charge is levied at 31 December value date on
  the mathematical provision "en ce compris l'éventuelle participation aux bénéfices" [S1]; Afer's
  0.475% is levied "après affectation de la participation aux bénéfices" [S9]. So the charge base
  includes the year's credited interest — the ratchet applies to the net-of-charge amount, not the
  gross.

### 4. Taux minimum garanti (TMG) and the regulatory caps
- Statutory architecture: A132-2 permits an insurer to guarantee a **total of technical interest plus
  profit participation** not lower than stated minimum rates [R3]; A132-3 caps those rates; A132-1
  and A132-1-1 fix the maximum technical interest rate that anchors the cap [R1][R2][R4].
- Maximum technical rate: **75% of the TME** for contracts of up to eight years; **min(3.5%, 60% of
  the TME)** for contracts of more than eight years and for periodic- or variable-premium contracts
  of any duration [R1]. The rate moves on a **0.25-point scale from origin 0, floored at 0**, and
  only when the monthly reference rate has fallen by 0.1 point or risen by 0.35 point; insurers have
  three months to implement a change [R2].
- TMG ceiling: the lower of **150% of the maximum technical rate**, and separately the higher of
  120% of the maximum technical rate and **110% of the average of the average rates credited over
  the last two financial years** [R4].
- Duration of a TMG: at least **six months** and at most the period from the guarantee's effective
  date to **the end of the following financial year** [R4]. A TMG announced for the current calendar
  year, as BoursoVie does, sits comfortably inside that window.
- **Current practice is TMG = 0 or near-zero.** The ACPR's average `taux technique` on individual
  euro contracts was **0.32% in 2025**, falling from 0.39% in 2020, and the ACPR states that
  "l'essentiel des contrats actuellement commercialisés en France a un taux technique faible ou
  nul" [R14]. Note that the taux technique is not the TMG — it is the maximum discount rate for the
  insurer's commitments, fixed at subscription, gross of charges, and a floor below which the
  credited rate cannot fall [R14].
- Contract evidence:
  - Meilleurtaux Placement Vie 2 and Croissance Avenir have **no guaranteed interest rate at all**
    under their "Rendement minimum garanti et participation" heading — the only guarantee stated is
    the capital floor net of charges [S3][S4].
  - BoursoVie references a "taux minimum garanti annoncé en début d'année pour l'exercice civil en
    cours": the PB rate credited may not be lower than it, and on a dénouement during the year
    (rachat total, décès, terme) "seul le taux minimum garanti annoncé en début d'année sera attribué
    au prorata temporis" [S1]. The announced value is not in the notice.
  - MACSF applies, during the 30-day renunciation window and for in-year partial surrenders, a rate
    "déterminé par le Conseil d'Administration de l'Assureur au 31 décembre de chaque année pour
    l'année suivante, en conformité avec les dispositions prévues par l'article A132-3", revisable
    in-year "selon la réglementation en vigueur" [S2].
  - Afer names the same object a **Taux Plancher Garanti**: used pro rata temporis in-year for rachat
    total and death settlement, with a top-up at the start of the following year equal to the
    difference between the definitive fund return and the floor rate [S11].
- **No public figure exists for the TMG of any contract in this set.** The drafter must treat the
  representative TMG as a `[std]` parameter; the ACPR average taux technique (0.32%) is the closest
  public anchor and is a different quantity [R14].

### 5. Participation aux bénéfices — the statutory minimum and the profit account
- Statutory sharing rule (current numbering): the `compte de participation aux résultats` is credited
  with **85% of the balance of the financial account**, and the insurer may retain from the technical
  result at most the **greater of 10% of its credit balance and 4.5% of annual premiums**, so at
  least **90% of the technical result** flows to policyholders [R5, art. A132-11]. The pre-2016
  numbering (A331-4) carries the identical 85% / 10%-or-4.5% construction [R6].
- The regulator states the practical consequence plainly: only 85% of the financial account "lui est
  destiné pour sa revalorisation, directement ou par l'intermédiaire de la PPB", and "certains
  contrats peuvent contractuellement prévoir un pourcentage plus élevé" [R14].
- Scope: individual and collective contracts of all kinds, excluding variable-capital contracts
  [R5, art. A132-10][R6, art. A331-3]. Equal treatment is required between paid-up and
  premium-paying contracts of the same category and the same mathematical provision
  [R5, art. A132-17].
- **Contractual PB is the exception, not the rule.** BoursoVie: "il n'est pas prévu de participation
  aux bénéfices contractuelle" for Eurossima and Euro Exclusif; the allocation follows art. A132-16
  and the PB rate is the amount allocated divided by the mathematical provision [S1]. Meilleurtaux
  Placement Vie 2 and the Rendement 2 / Opportunités 2 funds of Croissance Avenir: "il n'existe pas
  de participation aux bénéfices contractuelle", the amount determined annually under art. A132-10
  and set by the Directoire in Q1 [S3][S4].
- **Contractual PB where it does exist:**
  - Suravenir Rendement: a stated **90%** PB rate with the account written out in full — credit side
    contributions net of charges, opening mathematical provisions, incoming switches net of charges,
    **90% of releases from other technical provisions** (réserve de capitalisation, provision de
    gestion, provision pour aléas financiers, excluding the PPB) and **90% of the contract's share of
    net investment income** of the backing assets (coupons, dividends, interest, rents, realised
    gains and losses); debit side closing mathematical provisions before revaluation, benefits paid,
    outgoing switches, **management charges at a maximum rate of 0.60%**, 90% of transfers to other
    technical provisions, any prior-year debit balance, financial and administrative charges and
    taxes. The whole positive balance is carried to the PPB common to contracts backed by the same
    asset pool [S4].
  - Multisupport Afer: **100%** of the net financial profits of the ring-fenced (`cantonné`) Fonds
    Garanti, distributed after any transfer to or release from the PPB [S9].
- Per-contract allocation: PB = PB rate × the adhesion's mathematical provision on the fund, weighted
  by the time the sums were present on the fund during the year [S1].
- MACSF frames the same idea in results terms: the contract participates in technical and financial
  results at 31 December, both for contracts in force and for annuities in payment, on the same
  footing as every other contract backed by the Fonds en euros RES [S2].

### 6. The PPB and its eight-year clock
- Rule: the participation may be credited directly to mathematical provisions **or** carried, partly
  or wholly, to the provision pour participation aux bénéfices; sums carried there must be applied to
  mathematical provisions or paid to policyholders **within the eight financial years following** the
  year in which they were carried [R5, art. A132-16][R6, art. A331-9].
- Contract restatement: "à la provision pour participation aux bénéfices. Les sommes portées à cette
  provision sont affectées à la provision mathématique de chaque contrat dans un délai maximum de
  8 ans" [S2].
- Purpose, from an insurer's own booklet: the co-insurers "peuvent affecter une partie des revenus du
  Fonds Garanti en euros à la Provision pour Participation aux Bénéfices (PPB) afin de lisser les
  rendements … dans le temps et de constituer des réserves pour pallier des revenus à la baisse", the
  dotation, management and release being handled jointly through the association's supervisory
  committee "dans le respect des modalités et délais décrits dans le Code des assurances" [S9].
- **Market levels.** PPB as a percentage of life provisions: **4.0%** for individual contracts and
  **2.0%** for collective at end-2025, against 4.3% and 1.9% at end-2024 [R14], and 4.9% and 2.0% at
  end-2023 [R16]. By type at end-2025: bancassureurs **4.2%** (4.6% in 2024), traditional insurers
  **3.6%** (3.5%) — bancassureurs released, traditional insurers added [R14].
- **How much smoothing it buys.** Over 1999–2023 the reserve mechanism divides the volatility of
  credited rates by five relative to financial markets; each year the reserves redistribute about
  **1.6% of encours** between cohorts; contracts held over 2006–2011 gained an extra 1.6% a year while
  those held over 2012–2021 contributed 2.3% a year to building the reserves [R14, box 2, summarising
  Débats économiques et financiers n° 50 — the underlying paper was not retrieved].
- The HCSF may modulate the rules for constituting and releasing the PPB [R8, 5° bis].

### 7. Taux servi — what euro funds actually credited
- **Market averages, net of charges on encours and before social levies** [R14]:

  | Year | Individual contracts | Collective contracts |
  |---|---|---|
  | 2024 | 2.63% | 2.53% |
  | 2025 | 2.63% | 2.64% |

  The ACPR's earlier flow note gives a preliminary 2025 estimate of **2.65%** [R15]; the definitive
  figure in the revaluation study is 2.63% [R14].
- **Dispersion between insurers**: undertakings representing 50% of encours credited between **2.3%
  and 2.9%** in 2025, a 0.6 point band, narrower than the 2.2%–3.0% band of 2024 [R14]. By type:
  bancassureurs 2.70% (65% of encours), traditional insurers 2.48%, mutuelles 3.17% (2% of
  encours) [R14].
- **Dispersion inside one insurer**: the spread between the best- and worst-revalued homogeneous
  contract groups (90th vs 10th percentile of mathematical provisions) averaged **0.99 point** in
  2025 against 0.77 in 2024; the least-revalued group is **0.39 point below the mean** (0.40 in
  2024) [R14]. Bonuses conditioned on holding unit-linked supports are "souvent de 100 points de
  base, et allant jusqu'à plus de 200 points de base" [R14]. The 2.63% average therefore **includes**
  bonuses; an unbonused policyholder is at least 0.39 point below it [R14].
- **Named 2025 rates published by the insurer itself**, all "net de frais de gestion et hors
  prélèvements sociaux et fiscaux" [S11][S12]:

  | Fund | 2025 rate |
  |---|---|
  | Afer Fonds Garanti en euros | 2.65% |
  | Afer Fonds Euros Retraite | 3.50% |
  | Afer EuroGénération | 4.05% |

  Afer's 2024 Fonds Garanti rate (reported elsewhere as 2.51%) is **[unverified]** — no Afer document
  giving it was retrieved. MAIF's reported 2025 rate of 3.05% is likewise **[unverified]**: the MAIF
  document retrieved here is a fee table, not a rate announcement [S13].
- **The asset side that pays for it**: the ACPR's `taux de rendement de l'actif` reached **2.8%** in
  2025 (2.5% in 2024; near 2.1–2.2% from 2020 to 2023), with half of undertakings between 2.4% and
  3.3%; bonds are about 60% of life insurers' investments, and about 60% of fixed-coupon bonds
  maturing within four years still carry a coupon below 3% [R14]. Context rates in 2025: 10-year OAT
  3.4% average, Livret A 2.2% average, inflation +0.9% [R14].
- Suravenir's fund-level favourable one-year scenario, drawn from the last six years' experience, is
  **2.68%** [S5] — a useful independent sanity check on the market average.

### 8. Charges
- **Market averages on euro supports** (ratio of management charges paid by policyholders to average
  mathematical provisions) [R14]: individual **0.63%** in 2025 (0.62% in 2024) — 0.64% for
  traditional insurers, 0.63% for bancassureurs; collective 0.47% (0.42%). Half of all undertakings,
  individual and collective combined, sit between **0.5% and 0.8%**, a band that has been stable
  since 2020 [R14].
- **Contract-level charges, all figures from the documents themselves:**

  | Contract [source] | Frais sur versement (euro support) | Frais de gestion (euro support) | Frais d'arbitrage | Frais de rachat |
  |---|---|---|---|---|
  | BoursoVie — Generali Vie [S1] | 0% | 0.75% max p.a. | 0% | 0% (except illiquid UC, below) |
  | RES Multisupport — MACSF [S2] | 3% max | 0.50% max p.a. | 2% max into the euro fund; 0.20% max into UC, first 12 free | 0% |
  | Meilleurtaux Placement Vie 2 — Suravenir [S3] | 0% | 0.60% (Rendement 2); 3.00% max (Opportunités 2) | 0% | 0% |
  | Croissance Avenir — Suravenir [S4] | 0% | 0.60% (Rendement 2); 3.00% max (Opportunités 2) | not stated | 0% |
  | Multisupport Afer — Abeille [S9][S10] | 0.5% | 0.475% p.a. | 0%, unlimited free | 0% |
  | Assurance vie Responsable et Solidaire — MAIF VIE [S13] | 0% | 0.80% p.a. | EUR 15, one free per year | EUR 0 |

- **Charge timing and base.** BoursoVie levies 0.75% max at 31 December value date on the
  mathematical provision **including the year's PB**, pro rata temporis for payments and
  disinvestments during the year, and again pro rata on a full in-year disinvestment of the euro
  fund [S1]. MACSF levies 0.50% max at 31 December [S2]. Afer applies 0.475% "après affectation de
  la participation aux bénéfices" [S9].
- **Charges inside the euro fund, separate from the contract's charges.** Suravenir's fund-level
  disclosure gives management and other administrative/operating costs of **0.24% p.a.** and
  transaction costs of **0.03% p.a.**, a total impact of **0.48%** (EUR 48.37 on EUR 10 000) over one
  year, and states explicitly that these are internal to the fund and exclude the contract's own
  charges [S5]. Afer caps the Fonds Garanti's asset-management charge at **0.1% of assets under
  management excluding OPCVM** [S9]. A model that treats the credited rate as already net of the
  contract charge must not deduct these again.
- **Other charge lines worth carrying:**
  - Death floor guarantee: 0.055% p.a. of UC and eurocroissance savings (Afer) [S9][S10]; 0.10% p.a.
    on UC at 31 December (MACSF) [S2]; +0.14% on the annual management charge for the accidental
    death option (Suravenir) [S3][S4]; optional death cover priced at **0.15‰ to 5.15‰ of capital at
    risk per month by age**, ages 12 to under 70 at adhesion, after a **one-year waiting period**,
    no medical formalities (Suravenir) [S3][S4].
  - Annuity conversion: **3% of arrérages** — identical at Afer [S10], MAIF [S13] and Suravenir
    [S3][S4].
  - Illiquid UC exit penalties: BoursoVie up to **20%** of gross sums disinvested from named supports
    under art. R132-5-3 [S1]; MACSF 3% on SCPI and unlisted private-debt supports within three years
    of investment and ten years of the adhesion, and 5% in the R132-5-3 cases [S2]. These are UC
    features, not euro-fund features, but they sit in the same charge table.
  - Boursorama's `sécurisation des plus-values` option costs 1% max of the amount transferred [S1];
    ETF trades on the Suravenir contracts cost 0.10% of amounts invested or disinvested [S3][S4];
    settlement in securities costs 1% of the funds settled that way [S3].
- **PRIIPs aggregate cost disclosure** (all underlying options of one contract): CNP Nuances 3D shows
  total costs of EUR 489.23 to EUR 1 157.16 on EUR 10 000 if exiting after one year (4.89%–11.57%),
  and EUR 1 268.91 to EUR 10 385.95 if exiting after eight years (1.65%–5.48% a year), with entry
  costs contributing 0.45%–1.09% a year at eight years and exit costs nil [S6]. The wide range is the
  spread across investment options, not the euro fund alone.

### 9. Minimum amounts
- Minimum initial payment: **EUR 30** (MAIF) [S13]; **EUR 100** (Afer) [S10]; **EUR 300** (BoursoVie,
  gestion libre; also EUR 300 under gestion pilotée of which at least EUR 150 to the mandate) [S1].
- Minimum subsequent free payment: EUR 300 (BoursoVie), EUR 500 per listed share [S1].
- Programmed payments (BoursoVie): EUR 50 monthly, EUR 150 quarterly, EUR 300 half-yearly or
  yearly [S1].
- Minimum arbitrage: EUR 50 (BoursoVie), EUR 500 per share; the residual per support must not fall
  below EUR 25 (EUR 500 for shares) [S1].
- Minimum partial surrender: **EUR 1 000** with a **EUR 1 000** residual account value and a EUR 25
  residual per support (BoursoVie) [S1]; programmed partial surrenders EUR 150 monthly / EUR 300
  quarterly / EUR 500 half-yearly or yearly, and only if at least **EUR 10 000** sits on the euro
  funds (BoursoVie) [S1]; EUR 200 per programmed partial surrender whatever the frequency
  (MACSF) [S2].
- Automatic switching of the euro fund's gain to UC triggers above EUR 100 (BoursoVie) [S1] or
  EUR 25.00 cumulative (Suravenir) [S3].

### 10. Rachat, avance and the Sapin 2 suspension
- **Free surrender right.** Every contract in this set carries a `faculté de rachat`, partial or
  total, at any time [S1][S2][S3][S6]. The euro support is described as one the investor "peut
  racheter unilatéralement et à tout instant" [S5].
- **Settlement deadline.** Statutory maximum **two months** [R7], restated by BoursoVie [S1] and
  MACSF [S2]; Suravenir and CNP contract for **30 days** [S3][S6]. Late payment bears interest at
  the legal rate increased by half for two months then double the legal rate [R7][S3]; on the death
  benefit Suravenir contracts for double then triple the legal rate [S3].
- **No surrender penalty.** 0% or EUR 0 in every fee table retrieved [S2][S10][S13], and nil frais de
  sortie on the Suravenir contracts other than the annuity and in-kind options [S3]. The only exit
  charges that survive are the R132-5-3 penalties on illiquid unit-linked supports [S1][S2] — they do
  not touch the euro fund.
- **Surrender order.** Absent instruction, BoursoVie surrenders first from Eurossima, then Euro
  Exclusif, then the largest UC [S1]. That default matters for a model: an unspecified withdrawal
  drains the euro fund first.
- **Avance (policy loan).** Offered by every insurer here, but on terms held **outside** the notice:
  BoursoVie refers to a "Règlement Général des Avances en vigueur au jour de sa demande" which the
  member must sign, with the insurer free to accept or refuse [S1]; MACSF likewise [S2]; Suravenir
  grants an avance "sous réserve de l'accord de Suravenir, dont les modalités et la tarification lui
  seront communiquées sur simple demande" [S3]. **No rate, no maximum quotité and no maximum term is
  published in any retrieved document** — the usual market description (up to about 60–80% of the
  euro-fund savings, up to three years renewable, interest at the credited rate plus a margin) is
  **[unverified]**.
- An avance in force blocks or suspends most options — programmed arbitrages, fractional investment,
  gain-securing, gain-dynamising and programmed partial surrenders all end automatically on a request
  for an avance [S1][S3]. Outstanding avances and their interest are deducted from the death capital
  and from any settlement [S3].
- **Beneficiary acceptance blocks liquidity.** Once a designated beneficiary has accepted under
  art. L132-9, the policyholder can no longer surrender, take an avance, revoke the beneficiary or
  pledge the contract without that beneficiary's agreement [S1][S3].
- **Loi Sapin 2 / HCSF.** The Haut Conseil de stabilité financière may, under art. L631-2-1 5° ter of
  the Code monétaire et financier, temporarily limit the payment of surrender values, restrict the
  free disposal of assets, temporarily limit arbitrages and avances, and limit the acceptance of
  premiums; measures run for **at most three months, renewable**, and the surrender-value restriction
  "ne peuvent être maintenues plus de six mois consécutifs" [R8]. Suravenir discloses the power to
  investors, describing it as "temporaire (maximum 6 mois renouvelable), générale et
  exceptionnelle" [S5] — note that the insurer's summary and the statute do not line up exactly (see
  Gaps). Separately, the HCSF may modulate PPB constitution and release rules [R8, 5° bis]. The
  insurer itself cannot terminate the contract except under the anti-money-laundering provisions of
  art. R113-14 [S5].
- **Renunciation.** Thirty calendar days from signature or receipt of the adhesion certificate
  [S2][S6][S9]. During that window the first contribution is invested on the euro fund and earns the
  board-set A132-3 rate [S2].

### 11. Death benefit and beneficiary designation
- The death capital equals the contract's account value — `épargne acquise` — determined at the date
  the insurer learns of the death (registration following receipt of the death certificate or the
  acte de notoriété), less outstanding avances and their interest, plus any optional death cover
  [S3]. The euro-fund part carries its own in-year revaluation: BoursoVie credits only the announced
  TMG pro rata temporis to the date of dénouement [S1]; MACSF applies the board-set A132-3 rate pro
  rata from 1 January to the valuation date of the death capital [S2]; Afer applies the Taux Plancher
  Garanti pro rata with a top-up the following year [S11].
- Statutory revaluation of the death capital from the death to settlement is required by
  art. L132-5 of the Code des assurances [S3].
- Settlement: 30 days from receipt of the complete file (Suravenir), with penalty interest at double
  then triple the legal rate [S3]; two months (BoursoVie) [S1].
- **Designation of the beneficiary** may be made on the adhesion form and later by avenant, by
  private deed or by notarised deed, either by name or by quality (`énoncé de qualité`) [S1][S3].
  Acceptance by a named beneficiary is irrevocable, is made by an avenant signed by insurer, insured
  and beneficiary or by a deed notified to the insurer, and where the designation is gratuitous
  cannot occur until at least thirty days after the insured has been informed the contract is
  concluded; after the insured's death acceptance is free [S3].
- Optional death riders on the Suravenir contracts cover the `capital sous risque` — the positive
  difference between cumulative net premiums (less surrenders, less unrepaid avances and interest)
  and the surrender value — with a **one-year waiting period**, entry ages 12 to under 70, and no
  medical formalities [S3][S4]. MACSF grants a `garantie plancher` on death/IFTD automatically to the
  member's 70th birthday, costing 0.10% p.a. on UC [S2]. These riders exist because the **UC** part
  can lose money; the euro part cannot, given its capital floor.
- Unclaimed contracts: sums unclaimed become the State's after a further period [S1][S9] — the loi
  Eckert regime is referenced only obliquely in the retrieved documents and its details are
  **[unverified]**.

### 12. Taxation of rachat
- Only the `produits` (the gain) inside a surrender are taxed; the capital portion is not. The exact
  pro-rata formula for splitting a partial surrender between capital and gain is not stated in any
  retrieved document and is **[unverified]**.
- **Prélèvement forfaitaire unique (PFU)** on products from premiums paid from 27 September 2017
  [S3][R10][R11]:

  | Contract duration at surrender | Income tax rate | Prélèvements sociaux |
  |---|---|---|
  | 0 to 8 years | 12.8% | 17.2% |
  | Over 8 years, premiums within EUR 150 000 | 7.5% | 17.2% |
  | Over 8 years, premiums above EUR 150 000 | 12.8% on the excess fraction | 17.2% |

  The EUR 150 000 threshold is assessed on premiums paid and not repaid at 31 December of the year
  preceding the surrender, across all the taxpayer's life and capitalisation contracts [S3][R11].
  Above it, only the fraction of products obtained by multiplying total products by the ratio of the
  threshold (reduced by pre-27-September-2017 premiums) to post-27-September-2017 premiums gets the
  7.5% rate; the rest is taxed at 12.8% [R11].
- **Abattement**: after the eighth anniversary, an annual allowance of **EUR 4 600** (single,
  divorced, widowed) or **EUR 9 200** (joint taxation), applied across all the taxpayer's contracts
  [S1][S3][R10].
- **Mechanics of collection**: the insurer withholds a non-final acompte of 12.8% before eight years
  or 7.5% after, and the final liability is settled on the income tax return; the taxpayer may make
  an express and irrevocable **global** option for the progressive barème covering all PFU income;
  individuals whose reference income two years earlier was below EUR 25 000 (single) or EUR 50 000
  (joint) may ask to be exempted from the acompte at the latest when requesting the surrender [S3].
- **Legacy regime**: for products from premiums paid up to 26 September 2017, income tax or, on
  option, the `prélèvement forfaitaire libératoire` at **35%** before four years, **15%** between four
  and eight years, and **7.5%** after eight years, with the same 4 600/9 200 abattement after eight
  years [S1].
- **Exemptions** under art. 125-0 A: redundancy (`licenciement`) of the beneficiary, second- or
  third-category invalidity, and conversion of the contract into a life annuity [R10]; BoursoVie's
  tax annexe adds the standard reservation that these are general indications with no contractual
  value [S1].
- Life annuities taken instead of a lump sum are taxed on a fraction of their amount determined by
  the annuitant's age at entry into enjoyment, under art. 158-6 CGI and art. L136-7 CSS [S1].
- The contract enters the **IFI** (real-estate wealth tax) base for the fraction of its surrender
  value at 1 January representing certain real-estate unit-linked assets [S1].
- Non-residents: French withholding or a treaty rate applies, and they are **exempt from prélèvements
  sociaux on production of evidence** [S1].

### 13. Prélèvements sociaux — the `au fil de l'eau` rule on the euro fund
This is the mechanic that most distinguishes a French euro fund from a foreign guaranteed account,
and it must be modelled explicitly.

- **Rate: 17.2%** [S3]. The composition usually quoted (CSG 9.2% + CRDS 0.5% + prélèvement de
  solidarité 7.5%) is **[unverified]** — neither art. L136-8 CSS nor art. 235 ter CGI was retrieved.
- **Timing.** Under art. L136-7 II of the Code de la sécurité sociale, products attached to contracts
  **whose rights are expressed in euros** are charged "lors de leur inscription au bon ou contrat" —
  that is, **each year, as the PB is credited**, whether or not anything is withdrawn. Unit-linked
  products are charged only at dénouement or on the insured's death [R9]. Under a multisupport
  contract, the euro portion follows the annual-inscription rule while the UC portion waits [R9].
- Contract corroboration: Suravenir's `dynamisation des plus-values` option switches the euro fund's
  annual gain to UC "diminuée des prélèvements sociaux" [S3] — the levy has already been taken at
  crediting. Boursorama's tax annexe states that products are subject to the social levies "dans les
  conditions prévues à l'article L136-7 du Code de la sécurité sociale" [S1].
- Consequence for a projection: the euro-fund account value compounds **net of 17.2% of each year's
  credited interest**, whereas the UC account compounds gross and settles the levy only on exit. A
  model that applies the levy only at surrender will overstate the euro fund's accumulated value.
  The published minimum-surrender-value tables are explicitly **before** social and tax levies
  [S1][S2][S3], so they cannot be used to calibrate this.
- On a partial surrender of a unit-linked contract whose products have already borne the
  contribution, the taxable base is computed in proportion to premiums withdrawn over total premiums
  paid [R9]. The corresponding refund mechanism where cumulated levies at inscription exceed those
  finally due at dénouement is **[unverified]**.
- On death, products not yet taxed at the date of death bear the social levies at dénouement [S1].

### 14. Death taxation
- **Premiums paid before the insured's 70th birthday — art. 990 I CGI** [R12][S1]: a flat levy after
  an abattement of **EUR 152 500 per beneficiary** across all contracts, at **20%** on the fraction up
  to **EUR 700 000** and **31.25%** above. Beneficiaries exempt from transfer duties under arts. 795,
  795-0 A, 796-0 bis and 796-0 ter — spouse, PACS partner, and qualifying siblings — are outside the
  levy [R12].
- **Premiums paid after the 70th birthday — art. 757 B CGI** [R13][S1]: droits de mutation par décès
  according to the beneficiary's relationship to the deceased, on the **fraction of premiums** paid
  after 70 exceeding a **global EUR 30 500 abattement** appreciated across all beneficiaries and all
  contracts on the same life. The accumulated products are not taxed under this article [R13]; the
  BoursoVie annexe states the same, adding that the abattement is global whatever the number of
  beneficiaries and adhesions [S1].
- Retirement savings products under arts. L224-1 and L225-1 CMF are taxed in full where the holder
  dies after 70 whatever the timing of premiums [R13] — relevant to the sibling `per_assurance`
  product, not to this one.

### 15. Protection, information and market context
- **Guarantee fund**: the Fonds de garantie des assurances de personnes (FGAP) compensates up to
  **EUR 70 000 per insured, adherent or beneficiary per company**, whatever the number of contracts
  [S6]. Suravenir contributes annually and refers to arts. L423-1 et seq. of the Code des
  assurances [S5].
- **Annual information**: the ACPR defines the credited rate by reference to arts. L132-22 and A132-7
  of the Code des assurances (and L223-21 of the Code de la mutualité) as the contract's "rendement
  garanti et participation aux bénéfices techniques et financiers", gross of the technical rate and of
  tax and social levies but **net of charges on encours** [R14]. A `relevé de situation annuel` is
  part of the contractual documentation [S6]. The texts of L132-22 and A132-7 were not retrieved
  directly.
- **Minimum surrender values over the first eight years** must be shown in the notice, and are, in
  every notice retrieved [S1][S2][S3][S4]; where optional charges make them indeterminate, art.
  A132-4-1 allows worked examples instead [S3].
- **Standardised fee tables**: Afer [S10] and MAIF [S13] both publish one in an identical layout
  (minimum initial payment, association fee, annual charges by support, average UC fund charges with
  the retrocession share, then one-off charges by operation). The legal or professional obligation
  behind that common format was not retrieved and is **[unverified]**.
- **Market size and flows.** Euro-support mathematical provisions of individual contracts
  **EUR 1 207 bn** end-2025 (EUR 1 178 bn end-2024); collective **EUR 154 bn** [R14]. Total assurance
  vie encours **EUR 2 088 bn** end-2025 [R17]; capital-guaranteed contracts EUR 1 361 bn and UC
  EUR 612 bn end-2025 against EUR 343 bn end-2016 [R15]. 2025 flows: premiums EUR 159.1 bn, benefits
  EUR 115.1 bn (surrenders EUR 71.0 bn, claims EUR 44.1 bn), **net inflow EUR 44.0 bn** of which euro
  supports **+EUR 6.4 bn** — positive again after five years of net outflow — and UC +EUR 37.6 bn
  [R15]. UC contributions EUR 75.9 bn in 2025, +14.4% [R17]. Assurance vie and retirement savings are
  32.9% of household financial wealth, EUR 2 153.5 bn [R15].
- **Population of undertakings** in the ACPR revaluation study: 116 organisations and 36 053 contract
  versions — 58 under the Code des assurances (14 of them bancassureurs), 24 mutuelles, 18 ORPS,
  16 under the Code de la sécurité sociale [R14].
- **Prudential treatment** — the Solvency II handling of the euro fund's future discretionary
  benefits, of the PPB and of the time value of the capital guarantee — is **[unverified]** here: the
  delegated regulation could not be retrieved [R18]. It belongs in the cross-product reference file.

### 16. Parameters with no public figure (candidates for `[std]`)
The drafter should expect to standardise these; no retrieved document supplies a value.
- The **TMG** actually announced by any of these insurers for any year [S1][S2][S11]. Nearest public
  anchor: the ACPR average taux technique, 0.32% for individual contracts in 2025 [R14] — a different
  quantity.
- The **avance** interest rate, maximum quotité and maximum term [S1][S2][S3].
- The insurer's **PPB dotation and release policy** — the split of the year's distributable result
  between direct crediting and the PPB. Only the outer bounds are public: at least 85% of the
  financial account and 90% of the technical result must reach policyholders [R5], and the PPB must
  be released within eight years [R5]. Aggregate levels are published (4.0% of provisions end-2025)
  [R14] but no insurer publishes its own dotation rule.
- The **asset mix and reinvestment rate** behind any one euro fund. Public anchors only: bonds about
  60% of life insurers' assets, TRA 2.8% in 2025 with half of undertakings between 2.4% and 3.3%, and
  about 60% of bonds maturing within four years carrying coupons below 3% [R14].
- **Lapse and partial-withdrawal experience.** Only aggregate flows are public — EUR 71.0 bn of
  surrenders against EUR 1 361 bn of guaranteed-capital encours in 2025 [R15] — with no split by
  duration, age or contract vintage.
- **Mortality** for the death benefit. Not researched in this file; the euro fund's death benefit is
  the account value, so mortality drives the timing of dénouement rather than the amount. Table
  choice belongs to `_research/regulatory-actuarial.md`.
- The **UC-holding bonus** rule that produces the 100–200 bp uplifts the ACPR observes [R14]: no
  retrieved contract states its own bonus grid.

---

## Variations across insurers

| Feature | BoursoVie — Generali Vie [S1] | RES Multisupport — MACSF [S2] | Meilleurtaux Placement Vie 2 / Croissance Avenir — Suravenir [S3][S4] | Nuances 3D / Nuances Plus — CNP [S6][S7] | Multisupport Afer — Abeille [S9][S10] | ARS — MAIF VIE [S13] |
|---|---|---|---|---|---|---|
| Wrapper | Group, bank-distributed | Group via association AMAP | Group via associations VIREA / SEREP | Group, bank-distributed | Group via association Afer | Group, mutual-distributed |
| Euro funds offered | Eurossima, Euro Exclusif | Fonds en euros RES | Suravenir Rendement (legacy), Rendement 2, Opportunités 2 | Nuances 3D Euro / Nuances Plus Euro | Fonds Garanti en euros (+ EuroGénération, Euros Retraite) [S11] | single euro support |
| Capital guarantee | premiums net of charges [S1] | "nettes de frais", but the 8-year table erodes at 0.50% p.a. | Rendement: gross; Rendement 2 / Opportunités 2: **net of annual management charges** | **net of annual management charges** | premiums net of **entry** charges | not stated in the fee table |
| Contractual PB | none — statutory allocation under A132-16 | none stated — statutory allocation at 31 Dec | Rendement **90%** with a fully specified profit account; Rendement 2 / Opportunités 2 none | none — PB awarded at 31 Dec | **100%** of net financial profits of the ring-fenced fund | not stated in the fee table |
| PPB mention in the notice | via A132-16 | yes, with the **8-year** release limit | yes — whole positive balance carried to a shared PPB | not in the DIC | yes, managed jointly through the Comité de Surveillance | not stated |
| In-year rate on dénouement | TMG announced at the start of the year, pro rata | board-set A132-3 rate, pro rata | rate set at least annually by Suravenir, pro rata | not stated in the DIC | **Taux Plancher Garanti**, pro rata, with a top-up next year [S11] | not stated |
| Frais sur versement (euro) | 0% | **3% max** | 0% | 0.45%–1.09% p.a. impact at 8 yrs (all options) | **0.5%** | 0% |
| Frais de gestion (euro) | 0.75% max | 0.50% max | 0.60% (Rendement 2) | not disclosed separately in the DIC | **0.475%** | **0.80%** |
| Arbitrage | 0% | 2% into the euro fund / 0.20% into UC, 12 free | 0% | not disclosed | 0%, unlimited | EUR 15, 1 free/yr |
| Surrender charge | 0% (20% max on named illiquid UC under R132-5-3) | 0% (3% / 5% penalties on SCPI and private debt) | 0% | none | 0% | EUR 0 |
| Settlement deadline | 2 months | 2 months | **30 days** | **30 days** | not extracted | not stated |
| Minimum initial payment | EUR 300 | not stated | not stated | not stated | **EUR 100** | **EUR 30** |
| Distinctive feature | daily compounding of the euro account; eurocroissance support alongside | high entry charge, low management charge — the mutual/professional model | two generations of euro fund in one notice, one gross-guaranteed and one net | the plainest published statement of the net guarantee | association governance, 100% PB, ring-fenced fund, Taux Plancher Garanti | zero entry charge, EUR 30 entry ticket, single euro support |

What actually varies, in order of importance for a model:

1. **Whether the guarantee erodes.** Gross-guaranteed funds (Suravenir Rendement, Afer Fonds Garanti,
   CNP Perspective Capi) hold the floor at premiums net of entry charges; net-guaranteed funds
   (Suravenir Rendement 2 / Opportunités 2, CNP Nuances 3D / Nuances Plus) let it fall by the
   management charge each year [S3][S4][S6][S7][S8][S9]. Both designs coexist at the same insurer.
2. **Where the charge sits.** The mutual and association contracts front-load (MACSF 3% entry /
   0.50% annual; Afer 0.5% / 0.475%), the online and bancassurance contracts charge nothing at entry
   and more annually (BoursoVie 0% / 0.75%; MAIF 0% / 0.80%; Suravenir 0% / 0.60%) [S1][S2][S10][S13]
   [S3]. Over eight years these are not equivalent, and the ACPR's 0.63% market average sits in the
   middle of the annual-charge cluster [R14].
3. **Whether PB is contractual.** Most contracts leave the sharing to the statutory minimum and the
   insurer's discretion [S1][S3]; Suravenir Rendement fixes 90% with a written profit account [S4];
   Afer fixes 100% of net financial profits of a ring-fenced fund [S9]. A contractual percentage
   materially changes the projection: it removes the insurer's discretion over the numerator.
4. **The in-year credited rate.** Every insurer needs a rule for a policyholder leaving mid-year, and
   they all use a floor rate applied pro rata temporis — called TMG [S1], the A132-3 board rate [S2],
   the annual Suravenir rate [S3], or the Taux Plancher Garanti [S11]. Afer alone commits to a
   following-year top-up to the definitive rate [S11].
5. **Bonuses.** The ACPR observes UC-conditioned uplifts of 100 to more than 200 basis points and a
   0.99 point spread between the best and worst credited contract groups inside a single insurer
   [R14]. None of the retrieved notices publishes its bonus grid, so this variation is real, large
   and undocumented at contract level.
6. **Settlement speed**, 30 days versus the statutory two months [S3][S6] against [S1][S2][R7].

Representative design for a reference implementation: a multisupport group contract with a single
euro support, zero entry charge, an annual management charge of about 0.60%–0.80% levied at
31 December on the account value including the year's credited interest, a capital guarantee net of
those management charges, no contractual PB percentage, a TMG of zero, an annual credited rate
announced early in the following year and definitively acquired on crediting, social levies of 17.2%
taken at crediting, and free surrender at any time with no penalty. That is BoursoVie [S1],
Meilleurtaux Placement Vie 2 [S3] and MAIF [S13] with their differences ironed out, and it sits on
the ACPR's central figures — 2.63% credited, 0.63% charged, 0.32% technical rate [R14].

---

## Gaps and caveats

1. **ACPR blocks plain fetchers.** Both ACPR publication pages and both ACPR PDFs returned HTTP 403
   to WebFetch, twice. They were retrieved by re-requesting the same URLs with a browser
   User-Agent, and the full text was extracted; the entries for R14, R15 and R16 record that route
   explicitly. Nothing in them is quoted from a search summary.
2. **AS175 carries an internal marking.** The published PDF of Analyses et synthèses n° 175 [R16]
   shows "ACPR-RESTREINT" in its page header although it is served from the ACPR's public
   publications area. It is used here only for prior-year comparatives (PPB 4.9% end-2023, 2024
   averages) that R14 restates independently.
3. **Solvency II not retrieved.** EUR-Lex returned an empty body and then HTTP 202 with zero bytes
   [R18]. Everything about the prudential treatment of the euro fund — future discretionary
   benefits, the PPB in own funds, the time value of the guarantee — is **[unverified]** in this
   file and must be sourced in `_research/regulatory-actuarial.md`.
4. **Web search budget was exhausted mid-research.** Several carriers named in the brief were never
   reached: AXA France, Sogécap, Predica / Crédit Agricole Assurances, Spirica, Groupama, Swiss Life
   France, BNP Paribas Cardif, AG2R La Mondiale. Generali is covered only indirectly, as the insurer
   of BoursoVie [S1]. The insurer sample here is six groups (Generali, MACSF, Suravenir, CNP, Abeille
   /Afer, MAIF VIE) across thirteen retrieved documents, which is enough for the structural claims
   but not for a market-wide charge distribution — for that, use the ACPR's own distribution [R14].
5. **One primary document 404'd.** The Afer Génération notice of January 2025 [S14] is no longer at
   the URL indexed for it. Afer EuroGénération's mechanics — including the reported eight-year
   loyalty bonus and the routing of its interest to the Afer Génération Dynamisant support — are
   **[unverified]**; only its 2025 rate of 4.05% is sourced [S11][S12].
6. **No TMG value is public.** Contracts announce a TMG or floor rate at the start of each year
   [S1][S2][S11] but none of the retrieved documents states the announced number for any year. The
   ACPR's average taux technique (0.32% individual, 0.98% collective, 2025) [R14] is a regulatory
   discount-rate statistic, not a TMG, and must not be substituted for one without saying so.
7. **Avance terms are not published.** All three insurers that address the avance push its terms into
   a separate `Règlement Général des Avances` or "communicated on request" [S1][S2][S3]. Rate,
   maximum quotité and maximum duration are **[unverified]**.
8. **Secondary-only rate figures were not adopted.** Afer's 2024 rate (reported as 2.51%), MAIF's
   2025 rate (reported as 3.05%), and the Facts & Figures market estimate of 2.65% appeared only in
   search summaries; no primary document was retrieved for any of them, and they are recorded here as
   **[unverified]** rather than cited. The rates that are cited come from Afer's own pages [S11][S12]
   and the ACPR [R14][R15].
9. **Légifrance served historic versions for the A331 series.** A331-3, A331-4 and A331-9 were
   returned as in force in 1995–2007, 2014–2016 and 1995–2016 respectively [R6]. They are kept
   because insurers' own documents still refer to that numbering, but the operative modern text is
   A132-10 to A132-17 [R5]. Article A331-9 was retrieved through the legacy `affichCodeArticle.do`
   URL form, which does not carry a version selector.
10. **Statutes behind the codified text were not retrieved.** Loi n° 2016-1691 (Sapin 2) art. 49, loi
    n° 2019-486 (PACTE) and its transferability provision (art. L132-23-2 of the Code des assurances),
    and the loi Eckert regime for unclaimed contracts are all referenced in these notes only through
    their codified effect or not at all; the attributions are **[unverified]**.
11. **Statute and insurer disagree on the HCSF suspension window.** Art. L631-2-1 5° ter sets a
    three-month renewable measure with surrender restrictions capped at six consecutive months [R8];
    Suravenir's investor disclosure describes the whole power as "maximum 6 mois renouvelable" [S5].
    The statute governs; the divergence is noted so that a drafter does not propagate the insurer's
    simplification.
12. **Social-levy composition unverified.** The 17.2% total is sourced from a product document [S3]
    and the timing rule from the statute [R9], but the 9.2 / 0.5 / 7.5 split was not confirmed
    against art. L136-8 CSS or art. 235 ter CGI, and the refund mechanism where levies taken at
    inscription exceed those finally due at dénouement was not retrieved at all.
13. **The capital/gain split of a partial surrender is not sourced.** No retrieved document gives the
    formula apportioning a partial surrender between returned capital and taxable products. Treat it
    as **[unverified]** until art. 125-0 A's implementing provisions are read.
14. **MACSF's guarantee wording is ambiguous and its table is the tiebreaker.** The encadré says the
    euro guarantee equals premiums "nettes de frais" while the eight-year minimum surrender table
    falls at 0.50% a year [S2]. Any general statement of the form "French euro funds guarantee
    premiums net of entry charges" is therefore unsafe; read the table, not the summary box.
15. **Charge figures are maxima, not actuals.** BoursoVie, MACSF and Suravenir Opportunités 2 state
    their management charges as "maximum" [S1][S2][S3]. The ACPR's 0.63% average is an *actual* ratio
    of charges paid to average mathematical provisions [R14], and is the better calibration target.
16. **The standardised fee table has no sourced legal basis here.** Afer [S10] and MAIF [S13] publish
    identically structured tables, which points to a common obligation or professional commitment,
    but the instrument was not retrieved and the attribution is **[unverified]**.
17. **Mortality and longevity are out of scope in this file.** The euro fund's death benefit is the
    account value, so no decrement table was researched here. TH00-02/TF00-02 and TGH05/TGF05 and the
    INSEE population tables belong to `_research/regulatory-actuarial.md` and to the annuity and
    protection products.
