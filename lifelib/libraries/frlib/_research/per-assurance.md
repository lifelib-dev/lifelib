# Retirement Savings Plan, insurance form (Plan d'Épargne Retraite individuel assurantiel) — research notes (France)

Research notes for the French **PER individuel assurance** — the individual retirement savings
plan created by the loi PACTE and taken out as membership of a *contrat d'assurance de groupe*
(group life insurance contract) rather than as a securities account. These notes are the
citation ground truth for the frlib `per_assurance` product documents: source ids S1..S10 and
R1..R24 below are frozen — never renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document that
was actually fetched and read. `[unverified]` marks statements from general knowledge or from
secondary summaries of documents that could not be retrieved. Where a fetch failed the failure is
recorded and the item is kept only as a known reference (fetched_ok = false).

Language note: French terms of art are kept in French and glossed on first use — *versements*
(contributions), *fonds en euros* (the with-profits-like guaranteed euro fund), *unités de compte*
(UC, unit-linked funds), *participation aux bénéfices* (profit sharing), *gestion pilotée par
horizon* (default lifecycle/glide-path management), *arrérages* (annuity instalments), *notice
d'information* (the contractual information booklet that doubles as policy conditions), *quittance
d'arrérages* (annuity payment slip).

---

## Primary sources

### S1 — SMAvie BTP (PRO BTP), "PER Individuel CONFIANCE BTP — Notice d'information valant conditions générales"
- Publisher: SMAvie BTP, with the association GPBF (Groupement de Prévoyance des Bâtisseurs de
  France) as *souscripteur* of the group contract
- Doc type: notice d'information valant conditions générales, 47 pp., dated "Juin 2026"
- URL: https://www.probtp.com/files/live/sites/probtp/files/media/pdf/epargne/perin-notice-information.pdf
- Retrieved: YES (PDF downloaded, full text extracted with PyMuPDF; 47 pages, 129 200 characters).
- Content: the most complete single contract in the sample. Group life contract with optional
  individual membership; benefits in *rente viagère* (life annuity, optionally reversionary) or
  capital from the earliest of pension liquidation and the legal retirement age; capital guarantee
  on the euro part equal to premiums net of loading less management charges and withdrawals;
  contractual *participation aux bénéfices* on the euro part; 100 % of UC coupons and dividends
  reinvested. Charges: no *frais de dossier*; 4 % max on each *versement*; 0,084 % per month
  (≈ 1 % p.a., of which 0,12 % p.a. for the *garantie plancher* death floor) on both the euro
  support and UC, levied on end-of-month balance; capital exit free; annuity exit 1 % max of
  *arrérages* paid; 1 % p.a. on assets backing annuities in payment; arbitrage 0,30 % under the
  three *horizon retraite* profiles, 0,50 % under *gestion libre* with the first arbitrage each year
  free, "A Contrario" option 0,50 % capped at €5; transfer indemnity 1 % max, nil after five years
  from the first *versement* or from the L. 224-1 maturity; GPBF association levy €0,96 per contract
  per year. Euro support: guaranteed technical rate 0 % gross of charges, "aucun taux minimum garanti
  contractuel et aucune clause de fidélité"; interest credited weekly, the weekly rate derived from a
  quarterly prospective assessment of profit sharing, definitively acquired each Friday. Three glide
  paths (Prudent/Équilibré/Dynamique Horizon Retraite), rebalanced semi-annually in Q2 and Q4, with
  a full 20-band allocation table per profile (reproduced in §5 below). Planned retirement age chosen
  between the L. 161-17-2 minimum and 80, automatically rolled forward one year if not exercised,
  then tacitly renewed 12 months at a time past 80. Annuity: quarterly in arrears with a proportional
  first instalment, mortality table **in force at the date of adhesion** for sums from tax-deductible
  voluntary *versements* and from an incoming transfer made at adhesion, **in force at annuity
  commencement** for other sums; technical rate per regulation at the date of the request; commutation
  to a lump sum where the monthly annuity falls below the A. 160-2-1 threshold. Partial capital exit
  minimum €750, residual balance ≥ €750 with ≥ €150 per support. *Garantie plancher*: death benefit
  not less than premiums net of charges minus benefits already paid; the *Capital Complémentaire*
  top-up is pro-rated once aggregate net premiums across the member's SMAvie contracts exceed
  €800 000; guarantee ceases at the member's 70th birthday, on total surrender, on transfer, or on
  cancellation; first-year suicide excluded. Seven early-release cases quoted verbatim from
  L. 224-4 including the under-18 case.

### S2 — Generali Vie / Le Cercle des Épargnants, "Le PER Generali Patrimoine — Notice d'information" (PA9601NIB, Mai 2020)
- Publisher: Generali Vie, group contract subscribed by the association Le Cercle des Épargnants
- Doc type: notice d'information, 40 pp., code PA9601NIB, dated May 2020
- URL: https://assets.placement-direct.fr/2020-06/Notice_information_PER_Generali_062020.pdf
- Retrieved: YES (PDF downloaded, full text extracted; 40 pages, 228 904 characters).
- Content: group life contract with individual, optional membership. Charges: 4,50 % max on the
  initial, free, scheduled or incoming-transfer *versement*; €30 association fee at adhesion;
  UC management 0,25 % per quarter (1 % p.a.) for standard UC, 0,275 % per quarter (1,10 % p.a.) for
  index ETFs and for direct equities; euro fund 0,90 % max p.a. of the euro mathematical provision;
  *gestion pilotée* 0,125 % per quarter (0,50 % p.a.); *gestion horizon retraite* 0,125 % per quarter
  (0,50 % p.a.); loss-limitation options 0,05 % per quarter (0,20 % p.a.); no charge on annuity
  *arrérages*; no charge on exceptional surrender; individual transfer out 1 % of the transfer value
  during the first five years and nil from the fifth anniversary; arbitrage 0,50 % max with a €30
  minimum by post or €15 online; *sécurisation des plus-values* option 0,50 % of the amount moved;
  annuity-phase management 0,60 % p.a. of the euro mathematical provision. Minimum initial
  *versement* €1 000 under *gestion libre* (€100 minimum per support), €2 000 under *gestion pilotée*
  and *gestion horizon retraite*; subsequent *versements* €300 / €1 000; scheduled *versements* from
  €75 monthly, €200 quarterly, €400 half-yearly, €800 yearly; direct equities require €10 000 per
  line; the euro fund is limited to 40 % of any *versement*. Three horizon profiles, each a blend of
  a *gestion pilotée* orientation and a single investment-grade euro government bond UC, rebalanced
  semi-annually free of charge (grids in §5). Profit sharing on the euro fund: no contractual PB
  clause; the insurer sets an annual PB amount under art. A. 132-16 of the Code des assurances,
  allocated by criteria fixed at the start of the year (UC proportion on the membership, size,
  management mode, seniority), with the served rate not below the *taux minimum garanti* announced at
  the start of the year; PB credited with value date 31 December; on any exit during the year only
  the announced *taux minimum garanti* applies pro rata temporis. Annuity conversion: technical
  interest rate **0 %**, mortality table in force at liquidation, reversion freely set between 50 %
  and 200 % in 10 % steps to a named beneficiary, *annuités garanties* limited to life expectancy at
  liquidation minus five years, *rente par paliers* with 2 or 3 steps, each intermediate step ≤ 10
  years, variation limited to −50 % and +100 %; *arrérages* quarterly in arrears with no proration on
  death except reversion; commutation to a lump sum where the annuity does not exceed the A. 160-2-1
  amount, quoted in the notice as €240 per quarter. Death during accumulation: capital to named
  beneficiaries, but a *rente temporaire d'éducation* to minor children until their 25th birthday,
  and a life annuity to the spouse/PACS partner where the children are adult; annuity computed at the
  tariff in force at the date of death and free of *arrérage* charges. Compartment 3 sums (and
  transfers of compartment 3) may only be paid as a life annuity.

### S3 — MACSF épargne retraite, "Notice d'information RES RETRAITE" (16 10 301 E, édition 10/2024)
- Publisher: MACSF épargne retraite, group contract subscribed by AMAP (Association Médicale
  d'Assistance et de Prévoyance)
- Doc type: notice d'information, 25 pp., code 16 10 301 E, édition 10/2024
- URL: https://www.macsf.fr/content/download/16986/fichier/MACSF_1610301E_Notice_information_RES_Retraite.pdf
- Retrieved: YES (PDF downloaded, full text extracted; 25 pages, 109 973 characters).
- Content: PER individuel written as a group life contract in euros and UC. Charges: 3 % max on free
  *cotisations*, 2,5 % max under a *convention d'abonnement* (always at least 0,5 pp below the
  free-contribution rate); no incoming transfer fee; management 0,50 % on the *Fonds en euros RES
  Fonds de Pension* and 0,50 % on UC, both levied on 31 December; exit — no charge on capital, 3 %
  max on each gross annuity instalment, no charge on exceptional surrender; transfer out 1 % before
  the fifth anniversary of adhesion, nil thereafter or once the member has liquidated a compulsory
  pension or reached the L. 161-17-2 age; all arbitrages free, whether automatic or in the *profil
  Libre*; profile changes free; *garantie plancher* charge 0,10 % p.a. on UC balances at 31 December,
  ceasing after the 31 December following the member's 70th birthday; unlisted-asset penalties 3 %
  (private debt in *profil Libre*) and 5 % (unlisted assets in *profil Libre*) on disinvestment; €10
  one-off association fee. Three horizon profiles branded Détente (prudent horizon retraite),
  Harmonie (équilibré) and Tonus (dynamique), each securing progressively into low-risk supports
  with a synthetic risk indicator ≤ 2 including the euro fund, with free automatic arbitrage twice a
  year on 15 March and 15 September driven by the planned retirement age; the profiles are stated to
  meet the minimum low-risk and unlisted-asset allocations imposed by loi n° 2023-973 (industrie
  verte). Annuity phase: the mathematical provision equals the value of the annuity commitments
  computed on the regulatory mortality table and a **0 % technical interest rate**. Death during
  accumulation: capital equal to the accumulated retirement savings, floored by the *garantie
  plancher* — total contributions net of loading plus interest net of management charges earned on
  the euro fund — granted to the 70th birthday and capped at €762 245 across all contracts.
  Membership requires French tax residence in metropolitan France or the DROM; no loyalty bonus and
  no paid-up value. Includes a printed eight-year minimum transfer-value table on maximum charges.

### S4 — Spirica / LinXea, "LINXEA SPIRIT PER — Conditions Générales valant Notice d'information" (CG9403, 01/10/2020)
- Publisher: Spirica (Crédit Agricole Assurances group), group contract subscribed by the
  Association Retraite Falguière, distributed by LinXea
- Doc type: conditions générales valant notice, 52 pp., code CG9403 dated 01/10/2020
- URL: https://assets.suncel.io/61f14731fceb386b06ff8f0b/hifKK-Linxea_Spirit_PER_CG9403_20201001-1.pdf
- Retrieved: YES (PDF downloaded, full text extracted; 56 pages, 254 608 characters).
- Content: the low-charge end of the market. **No** *frais sur versement*; €10 association fee;
  UC management 0,125 % per quarter (0,50 % p.a.); euro fund (*Fonds Euro PER Nouvelle Génération*)
  **2 % max p.a.**; a *Support Croissance Allocation Long Terme* carrying a *provision de
  diversification* with an 80 % capital guarantee at maturity, 1 % p.a. plus a performance fee of up
  to 10 % of positive annual performance; *Gestion Pilotée à Horizon* carries no extra charge, while
  the (non-default) *Gestion Pilotée* costs 0,2 %–0,7 % p.a. depending on profile; annuity
  *quittance d'arrérages* 0,50 % max, capped at 1 % of the monthly social security ceiling per
  instalment; annuity support management 2 % max p.a.; transfer out 1 % max before the fifth
  anniversary. Default management is *Gestion Pilotée à Horizon* on the "Équilibré Horizon Retraite"
  profile; three profiles offered; minimum €500 per *versement* into a profile; automatic arbitrage
  whenever a threshold is crossed and at least every six months; the insurer may unilaterally change
  a profile's allocation to keep the regulatory de-risking. Annuity options: plain life, reversionary
  50 %–150 % in 10 % steps, *annuités garanties* bounded by art. A. 335-1 (life expectancy minus five
  years), reversionary with guaranteed annuities (reversion 50 %–100 %), and stepped annuities with at
  most two changes and first two periods ≤ 10 years each. Annuity amount depends on the accumulated
  value net of social and tax levies, the dates of birth, the mortality table in force at conversion,
  the option chosen, the frequency, the number of guaranteed annuities, the technical rate in force
  (capped by regulation), and the 0,50 % service charge; the insurer does not guarantee the annuity
  amount; annuities in payment are revalued through the technical and financial profit-sharing
  account. Small-annuity commutation stated at €80 per month, scaled by the number of months in the
  payment period.

### S5 — Spirica / ASAC-FAPES (ERES), "Le PER ERES by Spirica — Conditions Générales valant Notice d'information" (CG9406, 01/10/2022)
- Publisher: Spirica, group contract subscribed by the Association PERF, distributed under the
  ASAC-FAPES / ERES brand
- Doc type: conditions générales valant notice, 34 pp., code CG9406 dated 01/10/2022
- URL: https://www.gpm.fr/wp-content/uploads/2022/12/CONDITIONS_GENERALES_PER_ERES_SPIRICA.pdf
- Retrieved: YES (PDF downloaded, full text extracted; 36 pages, 236 849 characters).
- Content: **same insurer as S4, materially different pricing** — 4,80 % max on the initial
  *versement*, on free and scheduled *versements* **and on incoming transfers**; €25 association fee
  at first adhesion; UC management 0,25 % per quarter (1 % p.a.) in *Gestion Libre* but 0,2125 % per
  quarter (0,85 % p.a.) under *Gestion Pilotée à Horizon* and *Gestion Pilotée avec
  Désensibilisation*; euro fund 2,3 % max p.a.; annuity *arrérages* free; annuity support management
  2,30 % max p.a.; transfer out 1 % max before the fifth anniversary; first arbitrage each calendar
  year free then 0,50 % max; arbitrages inside a de-risking profile free; SCPI UC pay through 90 % of
  dividends rather than 100 %. No contractual profit-sharing clause on the euro part and no loyalty
  bonus.

### S6 — Spirica / Bourse Direct, "PLAN D'EPARGNE RETRAITE — VERSION ABSOLUE RETRAITE, Conditions Générales valant Notice" (CG9401, 01/07/2020)
- Publisher: Spirica, group contract subscribed by the Association Retraite Falguière, distributed
  by Bourse Direct
- Doc type: conditions générales valant notice, 36 pp., code CG9401 dated 01/07/2020
- URL: https://epargne.boursedirect.fr/uploads/files/products_fin/9e5e145c7d6b6709b8e8547d1e79e26d/Conditions%20G%C3%A9n%C3%A9rales.pdf
- Retrieved: YES (PDF downloaded, full text extracted; 36 pages, 285 402 characters).
- Content: third Spirica-carried PER, third price point — 3,50 % max on initial, free and scheduled
  *versements*; €10 association fee; UC 0,25 % per quarter (1 % p.a.); euro fund 2,30 % max p.a.;
  *Support Croissance Allocation Long Terme* 1 % p.a. plus up to 10 % performance fee, with an 80 %
  capital guarantee at maturity; *Gestion Pilotée à Horizon* free, *Gestion Pilotée* 0,20 % per
  quarter (0,80 % p.a.) whatever the profile; annuity *arrérages* 0,50 % max; transfer out 1 % max
  before the fifth anniversary; ad hoc arbitrages 0,80 % max with a €50 minimum; option arbitrages
  0,50 % capped at €300. Transfers settled within two months.

### S7 — Suravenir / SEREP, "Suravenir PER — Notice, contrat d'assurance de groupe n° 2240" (réf. 5257-2, 09/2021)
- Publisher: Suravenir (Crédit Mutuel Arkéa group), group contract n° 2240 subscribed by the
  association SEREP, distributed by assurancevie.com among others
- Doc type: notice, 27 numbered pages (58 PDF pages), réf. 5257-2 (09/2021)
- URL: https://www.assurancevie.com/asv/document/public/contract_type_file/notice_suravenir_per_vf.pdf
- Retrieved: YES (PDF downloaded, full text extracted; 58 pages, 321 752 characters).
- Content: charges — **0 %** at adhesion and on premiums; annual management 0,80 % on euro rights and
  0,60 % on UC in *gestion libre* and in *gestion à horizon*, 0,80 %/0,90 % under an arbitrage
  mandate; charges accrue daily on the daily balance and are levied once a year (euro fund, by
  31 December or on total exit) and monthly (UC); 0 % on annuity *quittances*; transfer indemnity
  1,00 % of the capital if requested within five years of the effective date of adhesion, not due
  after the contract maturity; 0 % surrender charge; 0 % management-mode change; **0,80 % on annuity
  reserves**; 0 % incoming transfer; 0 % arbitrage, including the automatic horizon arbitrages;
  0,10 % on amounts invested/disinvested in ETFs. Optional death cover: reimburses the *capital sous
  risque* — the positive difference between cumulative premiums net of charges less exits and the
  transfer value at the date the death certificate is received — for members aged 12 to under 70 at
  adhesion, after a one-year waiting period, with no medical underwriting, capped at €100 000 per
  contract, ending at the 75th birthday; monthly premium **0,15 ‰ to 5,15 ‰ of the capital at risk**
  by age, printed as a full age table (€0,15 to age 30, €0,30 at 40, €0,50 at 45, €0,79 at 51,
  €1,44 at 60, €2,15 at 65, €2,80 at 68, €3,33 at 70, €3,96 at 72 per €1 000 of capital at risk per
  month). Euro fund: **guaranteed annual interest rate 0,00 %** gross of management charges for the
  whole contract term, with a capital guarantee equal to premiums net of loading and transfer fees,
  less annual management charges and the optional death-cover premiums, plus profit sharing under
  art. A. 132-10; partial exits during the year are revalued pro rata temporis at the served annual
  rate, total exits at a rate fixed annually by the insurer. Default allocation is "Équilibré Horizon
  Retraite"; three profiles with the statutory minimum low-risk shares quoted verbatim (§5); low risk
  is defined as SRRI ≤ 3, or an insurer-computed analogue ≤ 3 where no SRRI exists; automatic
  quarterly rebalancing. Annuity: monthly in arrears from the first day of the month following
  receipt of the file; amount set from age, reversion beneficiary's age, options, **the annuitants'
  mortality table in force at the annuity effective date and a technical interest rate of 0,00 %**;
  reversion 1 %–100 %; *annuités garanties* between 5 and 25 years and at most life expectancy minus
  five years, in 5-year steps; increasing and decreasing stepped annuities; annual life certificate
  required within 30 days on pain of suspension. Contains a complete taxation matrix by compartment
  reproduced in §12.

### S8 — BNP Paribas Cardif (Cardif Retraite), "Les frais du PER assurantiel — Contrat BNP Paribas Multiplacements PER" (mise à jour 23 mars 2026)
- Publisher: Cardif Retraite (a *Fonds de Retraite Professionnelle Supplémentaire* governed by the
  Code des assurances), association souscriptrice UFEP
- Doc type: standardised fee table published under the fee-transparency *accord de place* and the
  arrêté du 24 février 2022 [R16], 1 p.
- URL: https://document-information-cle.cardif.fr/documents/18841382/18862673/BNP%20Paribas%20Multiplacements%20PER/46cc3b6b-3105-1839-d441-67cf6152aa31
- Retrieved: YES (PDF downloaded, full text extracted; 1 page).
- Content: the regulated fee grid in its prescribed layout. Minimum initial *versement* **€30**;
  association fee €20. Annual plan charges: euro fund 0,70 % max, UC 0,70 % max, Eurocroissance not
  applicable, *gestion pilotée par horizon* 0,70 % max. Average fund charges: equity funds 1,43 %
  (0,94 % retroceded), bond funds 0,91 % (0,45 %), real-estate funds 2,00 % (0,50 %), diversified
  1,17 % (0,57 %); *gestion pilotée* averages 1,39 % prudent and 1,26 % équilibré for contracts sold
  to 12 November 2024, 1,26 % équilibré for contracts sold from 13 November 2024. One-off charges:
  *frais sur versement* **2,50 % max**; arbitrage 1 % max, no free arbitrages; outgoing transfer
  1 % max of the retirement savings before the fifth year from the effective date of adhesion and
  0 % from the fifth year, **plus up to 15 % reduction applied to the euro-fund share in computing
  the transfer value**; *frais sur les versements de rente* **1,5 % max** of each gross instalment;
  no surrender charge.

### S9 — BNP Paribas Cardif (Cardif Retraite), "Notice du Plan d'Épargne Retraite Individuel BNP Paribas Multiplacements PER — Fonds en euros Retraite et liste des supports en unités de compte" (supports en vigueur au 21 juillet 2026)
- Publisher: Cardif Retraite / BNP Paribas
- Doc type: annex to the notice carrying the standardised per-support performance-and-charge table
  required by the arrêté du 24 février 2022, 10 pp.
- URL: https://document-information-cle.cardif.fr/documents/18841382/18862670/BNP%20Paribas%20Multiplacements%20PER/9fe8c347-935c-3790-18e4-9813b369d531
- Retrieved: YES (PDF downloaded, full text extracted; 10 pages, 74 145 characters).
- Content: for every UC — ISIN, label, management company, currency, SRI 1–7, gross asset performance
  N-1 and 5-year annualised, asset management charge and the retroceded part, net asset performance,
  contract management charge (0,70 % throughout), total charges, and the final performance for the
  contract holder. For the euro fund: **"Taux de rendement de l'actif du fonds en euros en 2025 :
  3,38 % / Taux annuel de frais de gestion : 0,70 % / Taux de rendement net servi en 2025 : 2,75 %"**,
  with a note that Cardif Retraite retrocedes no commission on euro commitments. Also states the
  concentration limits on illiquid UC: real-estate plus private assets ≤ €10 000 000 and ≤ 50 % of
  the surrender value; ≤ €2 000 000 per OPCI; ≤ €500 000 per SCPI; ≤ €1 000 000 per private-asset
  support.

### S10 — Predica / Crédit Agricole Assurances, "Predica lance PER Assurance et LCL Retraite PER" (communiqué de presse, 26 novembre 2019)
- Publisher: Crédit Agricole Assurances (Predica)
- Doc type: press release, 2 pp.
- URL: https://www.ca-assurances.com/wp-content/uploads/CPPDA-PER-ASSURANCE.pdf
- Retrieved: YES (PDF downloaded, full text extracted; 2 pages).
- Content: launch specification of the two Crédit Agricole group retail PERs. *PER Assurance*
  (Crédit Agricole branches): minimum initial *versement* €500; euro fund; *gestion pilotée à
  horizon* with three profiles prudent/équilibré/dynamique, or *gestion libre* with 91 supports;
  *frais sur versements* **2,5 %** on initial, regular and free contributions; exit as capital in one
  go or fractionné, or as a life annuity, individual or reversionary. *LCL Retraite PER*: identical
  except 140 supports in *gestion libre*. No charge detail beyond the entry loading, and no notice
  d'information was retrieved for either contract.

---

## Regulatory and actuarial references

### R1 — LOI n° 2019-486 du 22 mai 2019 (loi PACTE), article 71
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000038496266
- Retrieved: YES (article text as published in the JORF).
- Content: the enabling article. Section I inserts a new Chapitre IV "Plans d'épargne retraite" into
  the Code monétaire et financier, defining plans that allow individuals to accumulate savings
  delivered as a life annuity or as capital at retirement. Section II keeps the 16 % employer
  contribution rate for collective plans subject to SME-allocation conditions; Section III grants a
  three-year transitional rate for existing collective plans; Section IV sets effective dates.
  Section V authorises the Government, within twelve months, to legislate by ordonnance to harmonise
  retirement savings — unified rules for collective and individual products, amendments to the
  insurance code on group contracts, the tax treatment of retirement savings (deductibility,
  exemptions and annuity taxation), investment rules for employee funds, and consequential
  adaptations. Sections VI–IX amend the Code des assurances, Code de la mutualité and Code monétaire
  et financier on unclaimed contracts and transfers to the Caisse des dépôts et consignations.

### R2 — Rapport au Président de la République relatif à l'ordonnance n° 2019-766 du 24 juillet 2019 portant réforme de l'épargne retraite
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000038811825
- Retrieved: YES.
- Content: the explanatory report for the ordonnance taken under R1. Creates one collective company
  plan (replacing the PERCO), one category-specific company plan (replacing "article 83" contracts)
  and one individual plan (replacing the PERP and Madelin contracts), marketable from 1 October 2019.
  Article 2 lets holders of PERP, Madelin, PERCO, Préfon, CRH, COREM and article 83 contracts transfer
  their savings into a new PER. Article 9 carries the transitional provisions for transforming
  existing products. States the two headline liberalisations: early release for the purchase of the
  main residence, and free choice between annuity and capital at retirement for savings other than
  compulsory employer contributions. The report does not itself describe the default *gestion pilotée*
  or the transfer-fee cap.

### R3 — Code monétaire et financier, Chapitre IV "Plans d'épargne retraite", Section 1 "Dispositions communes" (L. 224-1 to L. 224-8)
- Publisher: Légifrance
- URLs:
  - chapter index — https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000038507457/
  - L. 224-1 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038507575
  - L. 224-2 / L. 224-3 / L. 224-3-1 — https://www.legifrance.gouv.fr/codes/id/LEGISCTA000038507582
  - L. 224-3 (consolidated) — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044563706
  - L. 224-4 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048805611
  - L. 224-4 / L. 224-5 / L. 224-6 — https://www.legifrance.gouv.fr/codes/id/LEGISCTA000038507607
  - L. 224-6 (consolidated) — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048252425
- Retrieved: YES (each URL fetched separately; L. 224-1 and L. 224-4 obtained verbatim in French).
- Content: **L. 224-1** (in force since 1 October 2019) — natural persons may pay sums into a PER;
  its object is "l'acquisition et la jouissance de droits viagers personnels ou le versement d'un
  capital, payables au titulaire à compter, au plus tôt, de la date de liquidation de sa pension dans
  un régime obligatoire d'assurance vieillesse ou de l'âge mentionné à l'article L. 161-17-2 du code
  de la sécurité sociale"; the plan gives rise either to a *compte-titres* or, with an insurer, a
  mutuelle or a *institution de prévoyance*, to "l'adhésion à un contrat d'assurance de groupe dont
  l'exécution est liée à la cessation d'activité professionnelle"; the plan must offer the holder the
  possibility of acquiring a life annuity at that maturity together with a reversion option.
  **L. 224-2** — the three compartments: 1° *versements volontaires du titulaire*; 2° sums from
  employee savings (intéressement, participation, employer *abondement*, *prime de partage de la
  valeur*, unused time-savings-account days); 3° compulsory employee and employer contributions in a
  mandatory company plan; voluntary contributions are barred for holders under 18. **L. 224-3** (in
  force since 24 October 2024) — insurance-form plans acquire rights expressed in euros, in *parts
  de provision de diversification*, in *unités de rente* or in *unités de compte*, subject to
  art. L. 131-1 of the Code des assurances; unless the holder expressly decides otherwise, sums
  follow an allocation that progressively reduces financial risk; at least one alternative allocation
  must be offered, including allocations to solidarity funds (art. L. 3332-17-1 Code du travail) and
  to labelled ecological-transition or SRI funds; the risk-reducing allocations correspond to
  long-term profiles qualified by a ministerial *arrêté* that weighs risk exposure and expected
  return; paragraphs 3 to 6 do not apply to plans backed by *unités de rente* guarantees.
  **L. 224-4** (in force since 14 June 2026) — savings are blocked, and may be released or
  surrendered before maturity only in the listed cases: 1° death of the spouse or PACS partner;
  2° invalidity of the holder, of a child, of the spouse or PACS partner (2° and 3° of art. L. 341-4
  of the Code de la sécurité sociale); 2° bis serious illness, disability or a particularly grave
  accident affecting a dependent child; 3° over-indebtedness (art. L. 711-1 Code de la consommation);
  4° expiry of unemployment insurance rights, or a former director/board member without an employment
  contract or corporate office for at least two years; 5° cessation of self-employment following a
  judicial liquidation under Title IV of Book VI of the Code de commerce or any situation justifying
  the release in the view of the president of the commercial court in a *conciliation* under
  art. L. 611-4; 6° use of the savings to acquire the main residence, **excluding rights arising from
  compulsory contributions**; 7° the holder is under 18 at the date of the request. Paragraph II —
  the holder's death before maturity closes the plan. **L. 224-5** — at maturity, rights from
  compulsory employer contributions are delivered as a life annuity; other rights are delivered at
  the holder's choice as "un capital, libéré en une fois ou de manière fractionnée" or as a life
  annuity, unless the holder has irrevocably opted for the annuity beforehand. **L. 224-6** (in force
  since 25 October 2023) — rights under accumulation are transferable to any other PER; transfer does
  not alter the surrender or liquidation conditions; transfer fees "ne peuvent excéder 1 % des droits
  acquis" and are nil after five years from the first *versement* in the plan or where the transfer
  occurs from the L. 224-1 maturity; rights in a mandatory company plan are transferable only once
  membership ceases to be compulsory; group insurance contracts may reduce the transfer value within
  regulatory limits where the transfer right exceeds the asset share backing the provisions; the
  manager-change notice may not exceed six months.

### R4 — Code monétaire et financier, Section 3 "Le plan d'épargne retraite individuel" (L. 224-28 to L. 224-39) and Section 4 "Transferts" (L. 224-40)
- Publisher: Légifrance
- URLs:
  - https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000038818200/
  - https://www.legifrance.gouv.fr/affichCode.do?idSectionTA=LEGISCTA000038818819&cidTexte=LEGITEXT000006072026
- Retrieved: YES (both).
- Content: **L. 224-28** — "Le titulaire du plan d'épargne retraite individuel doit être âgé de dix-
  huit ans au moins à la date de l'ouverture de ce plan"; the plan is funded in cash and by transfers
  from other retirement plans. **L. 224-29** — duty of advice: the manager must propose a suitable
  plan after assessing the prospect's situation, financial knowledge, long investment horizon, return
  expectations, objectives including sustainability preferences, and retirement needs, and must
  explain the plan's characteristics, its financial management methods, the availability conditions
  and the applicable tax and social treatment. **L. 224-30** — from five years before retirement the
  holder may ask the manager about their rights and the exit options suited to their situation; the
  manager must notify that possibility six months in advance. **L. 224-30-1** — an individual PER may
  be registered and distributed as a PEPP. **L. 224-40** — savings in art. L. 144-1 and L. 144-2
  insurance contracts (including the PERP), art. L. 132-23 public-service supplementary schemes, the
  hospital scheme (CRH), *union mutualiste retraite* contracts (COREM), art. L. 3334-1 PERCO and
  article 83 contracts may be transferred into a PER; "les frais encourus à l'occasion d'un transfert
  … ne peuvent excéder un montant fixé par décret"; a PERCO-to-individual-PER transfer is allowed only
  once every three years.

### R5 — Code monétaire et financier, partie réglementaire, Chapitre IV "Plans d'épargne retraite" (R. 224-1 to D. 224-18)
- Publisher: Légifrance
- URLs:
  - chapter — https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000038870991/
  - Section 1 (R. 224-1 to R. 224-6-1) — https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000038870993/
  - D. 224-3 — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038871086
- Retrieved: YES (all three).
- Content: **D. 224-3** (version of 1 October 2019, quoted verbatim) — the risk-reducing allocations
  invest in assets suited to a long horizon; they "garantissent une diminution progressive de la part
  des actifs à risque élevé ou intermédiaire et une augmentation progressive de la part des actifs
  présentant un profil d'investissement à faible risque, à mesure que la date de liquidation
  envisagée par le titulaire approche"; that date may be changed at any time within the limits of
  D. 224-5; "le rythme minimal de sécurisation et la nature des actifs présentant un profil
  d'investissement à faible risque sont précisés par arrêté du ministre chargé de l'économie"; and
  the plan must let the holder opt out of the minimum de-risking pace on express request.
  **R. 224-1** lists the eligible securities (shares, fund units, real-estate funds, ELTIFs).
  **R. 224-2** sets the mandatory annual statement: identification, value of rights at 31 December
  and its history, contributions by L. 224-2 category and total withdrawals/surrenders, **all charges
  taken in the year with the total expressed in euros**, the transfer value at 31 December and the
  transfer conditions and cost, and for each asset "la performance annuelle brute de frais, la
  performance annuelle nette de frais, les frais annuels prélevés"; for group insurance contracts,
  the profit sharing and the average yield; for de-risking allocations, performance and the
  de-risking schedule; and the availability rules of L. 224-4 and L. 224-5. **R. 224-3-2** restricts
  professional investment vehicles to experienced investors or minimum tickets of €100 000 (€5 000 for
  insurance contracts); **R. 224-3-4** uses criteria such as a portfolio above €500 000 or
  professional financial experience. **D. 224-4** — early release is paid as a single payment of all
  or part of the eligible rights, at the holder's choice. **D. 224-5** — the plan must set out how the
  holder expresses their choice of delivery method. **R. 224-6** — where the transfer value of the
  mathematical provisions exceeds the asset share representing them, the plan may reduce that value
  "sans que cette réduction puisse toutefois excéder **15 %** de la valeur des droits individuels du
  titulaire relatifs à des engagements exprimés en euros". **D. 224-18** — for transfers of legacy
  products under L. 224-40, fees may not exceed 1 % of acquired rights and are nil after **ten years**
  from the first contribution, with a six-month processing deadline.

### R6 — Arrêté du 7 août 2019 portant application de la réforme de l'épargne retraite, article 1 (consolidated)
- Publisher: Légifrance (LODA)
- URLs: https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000039802054 (article 1, consolidated —
  this is the URL actually fetched); https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038906774
  (the arrêté's landing page, recorded from a search result but **not** fetched)
- Retrieved: YES for the article-1 URL (fetched three times with different prompts to extract both
  of its quantitative tables and the verbatim French of parts 1° b to 4° b); NO for the landing page.
- Content: the *rythme minimal de sécurisation*. Four qualified profiles — *prudent horizon
  retraite*, *équilibré horizon retraite*, *dynamique horizon retraite*, *offensif horizon retraite*.
  Part (a) of each fixes the minimum share of low-risk assets as a percentage of the plan balance by
  distance to the holder's envisaged liquidation date (grid in §5). Part (b) of each fixes the
  minimum share of *versements* directed to the assets listed at III (ELTIFs, alternative investment
  funds, commercial-company securities managed by portfolio management companies, sustainable
  collective vehicles), quoted verbatim: prudent "6 % jusqu'à 20 ans … 4 % jusqu'à 15 ans … 2 %
  jusqu'à 10 ans"; équilibré "8 % … 6 % … 5 % … 3 % jusqu'à 5 ans"; dynamique "12 % … 10 % … 7 % …
  5 %"; offensif "15 % … 12 % … 9 % … 6 %", each band expressed as "avant la date de liquidation
  envisagée par le titulaire". "Les seuils mentionnés aux 1° b, 2° b, 3° b et 4° b sont réduits de
  30 %" for company plans, with a compliance date of 31 December 2026.

### R7 — Arrêté du 1er juillet 2024 modifiant l'arrêté du 7 août 2019 portant application de la réforme de l'épargne retraite
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000049880444
- Retrieved: YES.
- Content: the instrument that inserted the unlisted-asset minima of R6 part (b), taken under loi
  n° 2023-973 du 23 octobre 2023 relative à l'industrie verte. "Le présent arrêté entre en vigueur le
  24 octobre 2024." Confirms the four profiles and the 30 % reduction of the thresholds for company
  plans, and the eligible asset categories.

### R8 — Code des assurances, Chapitre II "Plans d'épargne retraite donnant lieu à l'adhésion à un contrat d'assurance de groupe" (L. 142-1 to L. 142-8)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000006157902/
- Retrieved: YES (section fetched twice, once for the article-by-article structure and once for
  L. 142-3 in French).
- Content: **L. 142-1** — the chapter applies to PERs and to French sub-accounts of the PEPP taken
  out as group insurance. **L. 142-2** — tariffs are set from mortality parameters and a technical
  interest rate defined in the contract; a ministerial *arrêté* fixes the maximum technical rate
  (see R9). **L. 142-3** — permitted *garanties complémentaires*: death, disability income, loss of
  autonomy, unemployment, and a value guarantee; benefits under the death, disability and
  unemployment covers may not give the insured more than they would have had absent the risk, and the
  loss-of-autonomy benefit may not exceed **twice** the rights otherwise acquired; unemployment and
  value guarantees are restricted for PEPP sub-accounts. **L. 142-4** — the insurer must keep a
  *comptabilité auxiliaire d'affectation* (ring-fenced auxiliary accounting) for these commitments;
  existing commitments had to be moved into it by **1 January 2023**, without prejudice to
  policyholders and with an equitable asset split reflecting investment horizons. **L. 142-5** —
  creditors of the insurer other than the plan's policyholders have no claim on the ring-fenced
  assets, which carry a priority for policyholder claims. **L. 142-6** — where the ring-fenced assets
  no longer cover the commitments, insurer and subscribers must agree a recovery plan, failing which
  the ACPR sets the terms. **L. 142-7** — until 1 January 2026 insurers could transfer ring-fenced
  retirement portfolios into PERs subject to ACPR approval. **L. 142-8** — the transfer value of
  products with *unités de rente* guarantees is set by a method that reflects acquired rights and the
  insurer's solvency coverage, detailed by decree.

### R9 — Code des assurances, partie arrêtés, articles A. 142-1 to A. 142-4
- Publisher: Légifrance
- URLs: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038933717/2022-05-11 ,
  https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000006156967/2026-01-01
- Retrieved: YES (both).
- Content: **A. 142-1** (version of 12 August 2019) — "Les tarifs pratiqués par les entreprises
  d'assurance au titre des plans d'épargne retraite sont établis d'après un taux d'intérêt technique
  **au plus égal à 0 %**", with exceptions for certain mutual and social-security arrangements. The
  article makes no reference to mortality tables. **A. 142-2** sets the conditions for the
  loss-of-autonomy *garantie complémentaire* (benefit reduction limits, medical underwriting, annual
  revaluation); **A. 142-3** requires that cover to be presented in a separate chapter of the policy
  with its own premium; **A. 142-4** requires annual disclosure of the revalued benefit and the
  premium paid for it.

### R10 — Code des assurances, articles A. 160-2 and A. 160-2-1 (commutation of small annuities)
- Publisher: Légifrance
- URLs: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043743273 (A. 160-2),
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043743285 (A. 160-2-1)
- Retrieved: YES (both).
- Content: **A. 160-2**, in force since 22 July 2023 — a life insurer may, with the annuitant's
  agreement and under A. 160-3 and A. 160-4, buy back annuities and annuity increases where the
  monthly *quittances d'arrérages* do not exceed **€110** including statutory increases, either at
  settlement or while the annuity is in payment; for payment periods longer than a month the
  threshold is multiplied by the number of months in the period. No indexation mechanism is stated.
  **A. 160-2-1**, the PER-specific predecessor, applied a **€100** monthly threshold between
  1 July 2021 and 22 July 2023 and was then abrogated; several contracts in the sample still cite it
  (S1, S7) or its earlier €80 level (S4).

### R11 — Code des assurances, article A. 335-1 (mortality bases for tariffs)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006788627/2006-08-26
- Retrieved: YES.
- Content: tariffs must use either (a) tables homologated by ministerial *arrêté*, established by sex
  from insured populations for annuities or from INSEE data for other contracts, or (b) the
  undertaking's own experience tables certified by an independent actuary, with or without sex
  differentiation. For annuities, including temporary ones, a tariff built on a category (b) table
  "ne peut être inférieur à celui qui résulterait de l'utilisation des tables appropriées mentionnées
  au a" — the certified experience table can never produce a cheaper annuity than the regulatory
  table. The technical interest rate is set under art. A. 132-1. The article does not itself name
  TH00-02, TF00-02, TGH05 or TGF05.

### R12 — Arrêté du 1er août 2006 portant homologation des tables de mortalité pour les rentes viagères
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000820127/
- Retrieved: YES.
- Content: article 2 — "Les tables prévues au quatrième alinéa de l'article A. 335-1 du code des
  assurances pour les contrats de rente viagère sont à compter du 1er janvier 2007 : — la table
  **TGF05** ci-annexée concernant les assurés de sexe féminin ; — la table **TGH05** ci-annexée
  concernant les assurés de sexe masculin", replacing the generation table homologated by the arrêté
  du 28 juillet 1993. The arrêté also creates art. A. 335-1-1 on the consistent application of age
  shifts to the rates. The retrieved text does not mention TH00-02 / TF00-02, and states no rule on
  the number of *annuités garanties*.

### R13 — Code général des impôts, article 163 quatervicies (deduction of retirement savings contributions)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038836248
- Retrieved: YES (version in force 21 February 2026).
- Content: contributions to PERPs (art. L. 144-2 Code des assurances), individual supplementary
  retirement contracts, public-sector supplementary schemes and plans d'épargne retraite under the
  Code monétaire et financier are deductible from *revenu net global*. The annual limit is the
  difference between (1) "10 % de ses revenus d'activité professionnelle … retenus dans la limite de
  huit fois le montant annuel du plafond" of the social security ceiling, or 10 % of that annual
  ceiling if higher, and (2) the sum of contributions already deducted or exempted under articles 83,
  154 bis, 154 bis-0 A and 156. Unused allowance may be carried forward — the retrieved consolidated
  text reads "peut être utilisée au cours de l'une des **cinq** années suivantes". Married and PACS
  couples may pool their limits on express request. Persons newly becoming French tax residents get
  an extra allowance equal to three times the annual difference.

### R14 — Code général des impôts, article 990 I (levy on death benefits from life insurance)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288653
- Retrieved: YES (version in force since 11 March 2023).
- Content: a **€152 500** flat abatement per beneficiary, then **20 %** on the taxable share up to
  €700 000 and **31,25 %** above. Applies where the beneficiary is French tax resident at the date of
  death and has been for at least six of the previous ten years, or where the insured was French tax
  resident at death. Beneficiaries exempt under arts. 795, 795-0 A, 796-0 bis and 796-0 ter are
  outside the levy. Art. 990 I bis provides a further 20 % proportional abatement for sums from
  contracts meeting specified investment conditions.

### R15 — Code général des impôts, article 757 B (death benefits from premiums after 70, and the PER-specific rule)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006305367
- Retrieved: YES (version in force since 11 March 2023, as amended by loi n° 2023-171).
- Content: sums due by an insurer on the insured's death attract inheritance duty by reference to the
  beneficiary's relationship, **limited to premiums paid after age seventy**. The PER-specific
  exception is explicit: sums "dues … à raison du décès **après l'âge de soixante-dix ans du titulaire
  d'un plan d'épargne retraite**" (or of an approved PEPP) are subject to inheritance duty **in their
  entirety**, without the premium limitation. Paragraph II applies a **global abatement of €30 500**
  across all contracts on the same insured's life.

### R16 — Arrêté du 24 février 2022 portant renforcement de la transparence sur les frais du plan d'épargne retraite et de l'assurance-vie
- Publisher: Légifrance (JORF), published 6 March 2022
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045299785
- Retrieved: YES.
- Content: amends arts. L. 132-22, L. 522-5 and A. 522-1 of the Code des assurances and art. L. 224-7
  of the Code monétaire et financier. Prescribes an identical standardised table for life insurance
  and for PERs, with the columns: ISIN and asset label; management company; gross asset performance
  N-1; asset management charges; net asset performance; contract/plan management charges; **total
  charges**, defined as the sum of asset charges and recurring contract charges; final performance
  for the holder; commission retrocession rate. In force from 1 July 2022, and from 1 January 2023
  for the annual statements under L. 132-22 and L. 224-7. S8 and S9 are live instances of the
  resulting disclosure.

### R17 — BOFiP, BOI-IR-BASE-20-50-20 "IR — Base d'imposition — Limites de déduction des cotisations et primes d'épargne retraite"
- Publisher: Direction générale des Finances publiques (bofip.impots.gouv.fr)
- URL: https://bofip.impots.gouv.fr/bofip/1124-PGP.html
- Retrieved: YES.
- Content: the deduction limit is the gross ceiling (10 % of professional income capped at 8 PASS)
  less the professional retirement savings already built up (deducted or exempted employer/employee
  contributions). The limit "s'apprécie de manière individuelle pour chaque membre du foyer fiscal".
  The PASS of the **calendar year preceding** the *versement* applies. There is a floor of 10 % of the
  PASS for those with low or no professional income. Unused allowance carries forward (the retrieved
  page states five subsequent years, cross-referring to BOI-IR-BASE-20-50-30). Spouses may pool on
  express request.

### R18 — impots.gouv.fr, "Épargne retraite" (particulier)
- Publisher: Direction générale des Finances publiques
- URL: https://www.impots.gouv.fr/particulier/epargne-retraite
- Retrieved: YES.
- Content: voluntary *versements* are deductible from global income, with an option for the
  self-employed to deduct against professional income instead. The household ceiling is "10 % du
  montant net de l'ensemble des revenus d'activité déclarés au titre de l'année N-1", with a minimum
  of **€4 710** and a maximum of **€37 680**, computed from the previous year's PASS, and increased
  by unused allowance "au cours des trois années précédentes"; the ceiling is reduced by employer
  contributions to a PERCO/PERECO/PERO within the income-tax-exempt limit of **€7 419**, and by up to
  10 days of time-savings-account days. PERO compartment-3 rights must be taken as an annuity; other
  compartments may be taken as annuity, capital or a mix, and the capital may be fractionné.

### R19 — impots.gouv.fr, "Comment sont imposées les sommes du plan d'épargne de retraite populaire (PERP) ?"
- Publisher: Direction générale des Finances publiques
- URL: https://www.impots.gouv.fr/particulier/questions/comment-sont-imposees-les-sommes-du-plan-depargne-de-retraite-populaire-perp
- Retrieved: YES.
- Content: contributions to PERP, PREFON, COREM, CGOS, PERE, article 83 and the post-2019 PERIN/PERO/
  PERECO are declared under "Charges déductibles"; taxpayers may waive the deduction in exchange for
  lighter exit taxation. Return-form mapping at exit: annuities from deducted sources on lines
  1AS–1DS; annuities from non-deducted contributions or from employee savings on 1AW–1DW; capital from
  PERP/Préfon/Madelin/article 83 on 1AS–1DS unless the 7,5 % flat rate or *quotient* is elected
  (1AT–1DT); **capital from PERO/PERIN/PERECO on lines 1AI–1DI, taxed at ordinary income-tax rates
  without the 10 % deduction**; capital from non-deducted contributions or employee savings on
  1AW–1DW. The page states no social-levy rates or annuity abatement fractions.

### R20 — service-public.gouv.fr, fiche F36526 "Plan d'épargne retraite (PER) — PER individuel"
- Publisher: Direction de l'information légale et administrative
- URL: https://www.service-public.gouv.fr/particuliers/vosdroits/F36526/0
- Retrieved: YES.
- Content: the definitive plain-language statement of the regime. Two forms — *PER bancaire*
  (compte-titres via a credit institution or investment firm) and *PER d'assurance* (membership of a
  *contrat d'assurance de groupe*, giving access to a *fonds en euros* and to UC, with a beneficiary
  clause taxed like life insurance). Minimum age 18, no upper age limit, no status condition. Three
  compartments as in L. 224-2. Voluntary contributions deductible **until age 70**; the salaried
  ceiling quoted as "10 % de vos revenus d'activité (nets de frais professionnels) de 2025 (avec un
  maximum de 37 680 €), ou 4 710 € si ce montant est plus élevé"; carry-forward of three years for
  2024–2025 allowances and five years from 2026. Early release: the L. 224-4 list including the
  serious-illness-of-a-dependent-child case and the under-18 case, with compulsory contributions
  excluded from the main-residence case. Exit: capital in one or several instalments, annuity, or a
  mix. Taxation for **deducted** contributions — annuity taxed as pension income with the 10 %
  abatement, social levies on the taxable fraction of a *rente viagère à titre onéreux* graded by age
  (70 % under 50, 50 % at 50–59, 40 % at 60–69, 30 % at 70+), at 17,2 % for 2025; capital: the
  contribution part at the progressive scale with no social levies, the investment gain at the 30 %
  PFU (12,8 % + 17,2 %) to 31 December 2025 and 31,4 % (12,8 % + 18,6 %) from 2026. For
  **non-deducted** contributions — annuity taxed as a *rente viagère à titre onéreux* with 18,6 %
  social levies on the taxable fraction; capital: contributions exempt from income tax and social
  levies, gains at the PFU. Death: *PER bancaire* falls into the estate; *PER d'assurance* is taxed
  under the life-insurance rules with €152 500 per beneficiary, 20 % up to €700 000 and 31,25 % above
  for death before 70, and a €30 500 global abatement plus inheritance duty for death after 70.

### R21 — economie.gouv.fr (Bercy Infos), "Comment fonctionne le plan d'épargne retraite (PER) individuel ?" (written 01/06/2026)
- Publisher: Ministère de l'Économie et des Finances
- URL: https://www.economie.gouv.fr/particuliers/gerer-mon-argent/gerer-mon-budget-et-mon-epargne/comment-fonctionne-le-plan-depargne-retraite-individuel
- Retrieved: YES — **but only with a browser User-Agent**. Two successive plain WebFetch attempts
  returned HTTP 403; the page was then retrieved by curl with a Chrome User-Agent and an
  `Accept-Language: fr-FR` header, and the HTML converted to text locally.
- Content: the government's own 2026 restatement. "Depuis le 1er janvier 2026, les versements
  effectués sur votre plan d'épargne retraite après vos 70 ans ne sont plus déductibles." Default
  management is *gestion pilotée*: "lorsque le départ en retraite est lointain, l'épargne peut être
  investie sur des actifs plus risqués et plus rémunérateurs. À l'approche de l'âge de la retraite,
  l'épargne est progressivement orientée vers des supports moins risqués." The *PER d'assurance*
  differs from the *PER bancaire* chiefly in giving access to the *fonds en euros*. Carry-forward: up
  to five years for sums paid from 2026, three years for the unused 2024 and 2025 allowances; spouses
  may pool. Taxation, deducted contributions: annuity at the pension regime after the 10 % abatement,
  social levies on the part of the annuity corresponding to voluntary contributions after an
  age-graded abatement of 30 % under 50, 50 % at 50–59, 60 % at 60–69, 70 % over 69, at 17,2 % rising
  to **18,6 % for annuities paid from 1 January 2026**; capital: contributions at the progressive
  scale with no social levies, gains at 30 % to 31 December 2025 and **31,4 %** thereafter. Taxation,
  non-deducted contributions: annuity as *rente viagère à titre onéreux* with the same age-graded
  abatements and 18,6 % social levies on the gains part; capital: contributions exempt, gains at the
  same PFU. Transfers: free after five years of holding or after the plan's maturity, otherwise
  charged up to 1 % of the accumulated savings. Death: the plan closes; *compte-titres* form falls
  into the estate, insurance form follows the life-insurance rules with the 990 I / 757 B split
  turning on the age at death.

### R22 — France Assureurs, "L'ASSURANCE RETRAITE — Année 2024" (juillet 2025)
- Publisher: France Assureurs, Direction Statistiques & Recherche Économique
- Doc type: annual statistical report, 37 pp.
- URL: https://www.franceassureurs.fr/wp-content/uploads/lassurance-retraite-en-2024.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Content: the authoritative market picture for the insurance-carried PER. All PERs (loi PACTE) at
  31 December 2024: 6,9 million insured, +18,3 % on 2023, of which 61 % individual and 39 % company
  plans; 1,2 million new insured in 2024 (1,0 million new subscriptions, 0,2 million transfers in);
  contributions excluding incoming transfers €13,2 bn (+20,5 %), of which 80 % individual; UC
  represent 64 % of contributions (€8,5 bn); incoming transfers €4,2 bn, of which €1,8 bn reinvested
  in UC; mathematical provisions €93,6 bn (+23,9 %), of which 76 % individual; UC €41,9 bn = 45 % of
  provisions, 51 % for plans still in accumulation. **PER individuels only** (insurance undertakings
  under the Code des assurances): 4 195 500 plans in force at end-2024 (+18,7 %), of which
  3 799 800 (91 %) in accumulation and 395 700 in payment; contributions €10 496 m (+20,2 %) of which
  €6 838 m (65 %) into UC; benefits €2 837 m (+30,7 %), split €1 744 m from plans in accumulation
  (€93 m death benefits, €1 651 m early releases and transfers) and €1 093 m from plans in payment
  (annuities in payment €516 m, capital exits €305 m, small annuities commuted at outset €272 m).
  Averages: annuity in payment **€1 300 per year**; commuted small annuity **€16 200**; capital exit
  **€12 500**; mathematical provisions €70,7 bn (+22,6 %), €63,0 bn in accumulation and €7,7 bn in
  payment; UC €32,9 bn = 47 % of provisions (52 % in accumulation); average balance **€16 600** in
  accumulation and **€19 500** in payment.

### R23 — France Assureurs, "L'assurance vie en 2025 : une collecte solide au service de l'économie française" and the chiffres-clés pages
- Publisher: France Assureurs
- URLs: https://www.franceassureurs.fr/espace-presse/lassurance-vie-en-2025-une-collecte-solide-au-service-de-leconomie-francaise/ ,
  https://www.franceassureurs.fr/nos-chiffres-cles/lassurance-vie/ ,
  https://www.franceassureurs.fr/nos-chiffres-cles/les-donnees-globales/
- Retrieved: YES (all three).
- Content: PER assurantiel at 31 December 2025 — **7,9 million insured** (+1,0 million over twelve
  months) and **€111,9 bn** of *encours*; 2025 *versements* €20,2 bn (+16 %); net inflow €11,0 bn;
  about 1 million new PERs opened in 2025 (137 900 in December alone, €3,1 bn of December
  *versements*). Cross-market context at 30 June 2025: 12,4 million PER holders across all providers
  and €136,1 bn, of which insurance undertakings held 75 %. Life insurance for scale: *encours*
  €2 088–2 107 bn at end-2025, UC 39 % of 2025 contributions (46 % in December), UC contributions
  €75,9 bn (+14,4 %). The chiffres-clés pages give no PER-specific figures and no average *fonds en
  euros* revaluation rate.

### R24 — presse.economie.gouv.fr (DG Trésor), "Épargne retraite : déploiement du PER — près de 12,7 millions de titulaires et plus de 141 milliards d'encours au troisième trimestre 2025"
- Publisher: Ministère de l'Économie et des Finances / Direction générale du Trésor
- URL: https://presse.economie.gouv.fr/386-cp-epargne-retraite-deploiement-du-per-pres-de-127-millions-de-titulaires-et-plus-de-141-milliards-dencours-au-troisieme-trimestre-2025/
- Retrieved: YES (press release dated 16 February 2026).
- Content: at 30 September 2025, **12,7 million** PER holders and **€141,1 bn** of *encours*, +19 %
  over twelve months, split **PER individuels €82,4 bn**, PER d'entreprise collectifs €31,7 bn, PER
  obligatoires €27,1 bn. Over 80 % of assets invested in France and the EU, over 60 % financing
  companies through equity and private debt, more than €5 bn in unlisted assets. Statistics are
  "les données consolidées des fédérations professionnelles distribuant des PER (FA, AFG, FNMF et
  FIPS)" — i.e. they span both the insurance and the *compte-titres* form. No assurantiel/bancaire
  split and no contribution or transfer figures are given.

---

## Extracted specifications

### 1. Product structure and legal form

- A PER is a savings plan whose object is "l'acquisition et la jouissance de droits viagers
  personnels ou le versement d'un capital", payable to the holder at the earliest from the
  liquidation of a compulsory pension or the legal retirement age of art. L. 161-17-2 of the Code de
  la sécurité sociale [R3 L. 224-1].
- Two legal vehicles. The *PER bancaire* opens a **compte-titres** with a credit institution or
  investment firm. The *PER assurantiel* is **membership of a group life insurance contract "dont
  l'exécution est liée à la cessation d'activité professionnelle"** [R3 L. 224-1][R20][R21]. The
  practical difference the state itself emphasises is that only the insurance form gives access to
  the *fonds en euros* [R21]. All four notices in the sample are group contracts with optional
  individual membership, subscribed by an association acting as *souscripteur*: GPBF for SMAvie BTP
  [S1], Le Cercle des Épargnants for Generali [S2], AMAP for MACSF [S3], Association Retraite
  Falguière / Association PERF for Spirica [S4][S5][S6], SEREP for Suravenir [S7], UFEP for Cardif
  [S9]. The association charges its own fee: €0,96 per contract per year [S1], €30 at adhesion [S2],
  €10 [S3][S4][S6], €25 [S5], €20 [S8].
- The plan must offer the possibility of acquiring a life annuity at maturity together with a
  reversion option [R3 L. 224-1] — the annuity option is a statutory feature of every PER, not a
  commercial choice.
- Assets backing an insurance-form PER are **ring-fenced** in a *comptabilité auxiliaire
  d'affectation*; creditors other than the plan's policyholders have no claim on them, and an
  under-coverage triggers a recovery plan agreed with the subscribers or imposed by the ACPR
  [R8 L. 142-4 to L. 142-6]. Legacy commitments had to be moved into the ring fence by 1 January 2023
  [R8 L. 142-4].
- A PER may be carried by a life insurer or by a *Fonds de Retraite Professionnelle Supplémentaire*
  (FRPS). Cardif Retraite is an FRPS [S9]; SMAvie BTP, Generali Vie, MACSF épargne retraite, Spirica
  and Suravenir write their PERs as life insurers under the Code des assurances [S1][S2][S3][S4][S7].
  The prudential consequences of the FRPS regime were not researched here [unverified].
- An individual PER may additionally be registered as a PEPP [R4 L. 224-30-1]; no PEPP-registered
  French contract was retrieved [unverified].

### 2. Eligibility, opening and minimum contributions

- Minimum age 18 at opening [R4 L. 224-28][R20]; voluntary contributions are barred for holders under
  18 [R3 L. 224-2]. No upper age limit and no employment-status condition [R20].
- MACSF requires French tax residence in metropolitan France or the DROM [S3]. No residence condition
  appears in the other notices [S1][S2][S4][S7].
- Minimum initial *versement* across the sample: **€30** (Cardif) [S8]; **€500** (Predica PER
  Assurance and LCL Retraite PER [S10]; Spirica per profile in *Gestion Pilotée à Horizon* [S4]);
  **€1 000** (Generali *gestion libre*) and **€2 000** (Generali *gestion pilotée* / *horizon
  retraite*), reduced to €300 / €1 000 where scheduled contributions are set up at adhesion [S2].
  Subsequent free *versements*: €300 (Generali *gestion libre*), €1 000 (Generali piloted), €500
  (Spirica). Scheduled *versements* from €75 monthly / €200 quarterly / €400 half-yearly / €800
  yearly [S2]. No minimum is stated in [S1][S3][S7].
- The planned retirement age is declared at adhesion and may be changed at any time [R5 D. 224-3].
  S1 requires it to lie between the L. 161-17-2 minimum and **80**, rolls it forward automatically by
  one year if the member does not liquidate, and then extends the accumulation phase by tacit
  12-month renewals past 80; a statutory change to the retirement age automatically resets the
  declared age [S1].
- Cancellation period: 30 calendar days [S4][S7].
- No minimum or maximum age for the *rente* itself is set by statute; entry to the optional death
  cover is age-limited (12 to under 70 at adhesion, cover ends at 75) [S7], and the *garantie
  plancher* ends at 70 [S1][S3].

### 3. The three compartments

Art. L. 224-2 defines three sources of funds, and everything downstream — exit form, taxation, early
release — keys off them [R3]:

| Compartment | Source | Exit form | Main-residence early release |
|---|---|---|---|
| C1 — *versements volontaires* | the holder's own contributions [R3 L. 224-2 1°] | capital (one go or *fractionné*) or annuity, holder's choice [R3 L. 224-5] | allowed [R3 L. 224-4 I 6°] |
| C2 — *épargne salariale* | intéressement, participation, employer *abondement*, *prime de partage de la valeur*, unused CET days [R3 L. 224-2 2°] | capital or annuity, holder's choice [R3 L. 224-5] | allowed [R3 L. 224-4 I 6°] |
| C3 — *versements obligatoires* | compulsory employee and employer contributions in a mandatory company plan [R3 L. 224-2 3°] | **life annuity only** [R3 L. 224-5] | **excluded** [R3 L. 224-4 I 6°] |

- The compartment structure survives a transfer: sums transferred into an individual PER keep their
  origin and their treatment [S3 ART 13 A][S2 art. 24.1]. Generali states expressly that sums
  transferred in from compartment 3 may only be paid as a life annuity [S2]; SMAvie BTP states that
  annuity liquidation is compulsory for the part of the savings coming from a transfer of compulsory
  contributions [S1].
- For a model of the individual retail PER, compartments 2 and 3 arise only through incoming
  transfers; the primary flow is compartment 1.

### 4. Supports: fonds en euros, unités de compte, provision de diversification

- Insurance-form plans may express rights in **euros**, in ***parts de provision de diversification***,
  in ***unités de rente***, or in ***unités de compte*** composed of eligible securities, subject to
  art. L. 131-1 of the Code des assurances [R3 L. 224-3].
- Euro-fund capital guarantee, as drafted in the sample: premiums net of entry loading, less
  management charges levied over the contract's life and less withdrawals [S1]; "sommes versées
  nettes de frais" [S2]; premiums net of loading plus interest net of management charges [S3];
  premiums net of loading reduced each year by the charges taken [S4][S5][S6]; premiums net of
  loading and transfer fees, less annual management charges and the optional death-cover premiums
  [S7]. Suravenir is explicit that its guarantee is **not** a floor at gross premiums: "le contrat ne
  comporte pas de garantie en capital au moins égale aux sommes versées, nettes de frais" [S7 encadré].
- UC carry no capital guarantee; the insurer commits only to the **number** of units, not their value
  (art. A. 132-5 Code des assurances) [S1][S2].
- Two contracts in the sample offer a *provision de diversification* support ("Croissance Allocation
  Long Terme") with an **80 % capital guarantee of net premiums at maturity**, charged 1 % p.a. plus
  a performance fee of up to 10 % of positive annual performance [S4][S6].
- Concentration limits on illiquid UC (Cardif): real-estate plus private assets ≤ €10 000 000 and
  ≤ 50 % of the surrender value; ≤ €2 000 000 per OPCI; ≤ €500 000 per SCPI; ≤ €1 000 000 per
  private-asset support [S9]. Generali caps the euro fund at **40 % of any *versement*** in *gestion
  libre* and *gestion pilotée* [S2] — a striking inversion of the usual assurance vie constraint.
- OPCI/SCPI entry loads inside the wrapper can be material: SMAvie BTP levies up to **10 %** entry
  rights on its REGARD IMMOBILIER 2 unit (5 % acquired to the vehicle, 5 % to the management company)
  [S1]; MACSF applies 3 % and 5 % disinvestment penalties on unlisted supports held in the *profil
  Libre* [S3].

### 5. Gestion pilotée par horizon — the default management and its glide path

This is the single most model-relevant feature of the PER.

- **Default by law.** Unless the holder expressly decides otherwise, *versements* follow an allocation
  that progressively reduces financial risk [R3 L. 224-3]. The plan must let the holder opt out of the
  minimum de-risking pace on express request [R5 D. 224-3]. In the sample: SMAvie BTP defaults to
  "Equilibré Horizon Retraite" [S1]; Spirica and Suravenir default to "Équilibré Horizon Retraite"
  [S4][S7]; Generali's product is sold under "Gestion Horizon Retraite" with the "Équilibré" profile
  as the reference [S2].
- **The statutory minimum grid** [R6, art. 1, part (a) of each profile], expressed as the minimum
  share of the plan balance held in low-risk assets, by years remaining to the holder's envisaged
  liquidation date:

| Profile | ≥ 10 years out | from 10 years out | from 5 years out | from 2 years out |
|---|---|---|---|---|
| Prudent horizon retraite | 30 % | 60 % | 80 % | 90 % |
| Équilibré horizon retraite | — | 20 % | 50 % | 70 % |
| Dynamique horizon retraite | — | — | 30 % | 50 % |
| Offensif horizon retraite | — | — | 30 % | 50 % |

  Suravenir reproduces this grid verbatim as its own product specification [S7], and Generali's three
  profiles hit exactly these percentages (prudent 30/60/80/90 against the Bluebay investment-grade
  euro government bond UC; équilibré 0/20/50/70; dynamique 0/30/50 over bands "plus de 10 ans / de 10
  à 5 ans / de 5 à 2 ans / moins de 2 ans") [S2]. Treat the regulatory grid as the modelling default:
  in this market it is not a floor that insurers beat, it is the product.
- **Definition of "low risk".** The nature of low-risk assets is fixed by *arrêté* [R5 D. 224-3].
  Suravenir defines it as a synthetic risk indicator (SRRI) **≤ 3**, or an insurer-computed analogue
  ≤ 3 where no SRRI exists [S7]; MACSF uses supports with a synthetic risk indicator **≤ 2**,
  including the euro fund [S3]. The two definitions are not the same, and the arrêté's own wording
  was not extracted verbatim [unverified].
- **Minimum unlisted-asset share** since 24 October 2024 [R6 part (b)][R7], as a share of *versements*
  routed to eligible vehicles (ELTIFs, AIFs, commercial-company securities, sustainable collective
  vehicles), with thresholds cut by 30 % for company plans and a 31 December 2026 compliance date:

| Profile | to 20 years out | to 15 years out | to 10 years out | to 5 years out |
|---|---|---|---|---|
| Prudent | 6 % | 4 % | 2 % | — |
| Équilibré | 8 % | 6 % | 5 % | 3 % |
| Dynamique | 12 % | 10 % | 7 % | 5 % |
| Offensif | 15 % | 12 % | 9 % | 6 % |

  MACSF states its three profiles comply [S3]. SMAvie BTP's grids carry a private-equity line
  (Eurazeo Private Value Europe 3) at 6 %/4 %/2 %/0 % on the prudent profile and 12 %→0 % on the
  dynamic profile [S1] — an implementation of exactly this rule.
- **A real insurer glide path, band by band** — SMAvie BTP, "Prudent Horizon Retraite", allocation of
  both contributions and existing balance, by years remaining [S1]:

| Years remaining | Euro support | REGARD IMMOBILIER 2 | REGARD PRUDENT | REGARD RESP. FLEXIBLE | EURAZEO PVE 3 |
|---|---|---|---|---|---|
| > 19 down to < 16 | 30 % | 22 % | 17 % | 25 % | 6 % |
| < 15 down to < 11 | 45 % | 18 % | 13 % | 20 % | 4 % |
| < 10 down to < 6 | 60 % | 13 % | 10 % | 15 % | 2 % |
| < 5 down to < 3 | 80 % | 10 % | 5 % | 5 % | 0 % |
| < 2 | 95 % | 2 % | 2 % | 1 % | 0 % |
| < 1 | 100 % | 0 % | 0 % | 0 % | 0 % |

  The "Equilibré" profile on the same product runs 20 % → 22 % → 25 % → 50 % → 70 % → 80 % in the euro
  support over the same bands, and "Dynamique" runs 0 % → 0 % → 10 % → 30 % → 50 % → 65 % [S1]. Note
  that SMAvie BTP's ladder is defined on **20 one-year bands**, not on the four regulatory bands.
- **Rebalancing frequency** differs and matters for a monthly or annual model: semi-annual, in Q2 and
  Q4 [S1]; semi-annual, free [S2]; semi-annual on fixed dates 15 March and 15 September [S3];
  whenever a threshold is crossed and at least every six months [S4]; **quarterly** [S7].
- **Who bears the arbitrage cost:** free at Generali, Spirica (horizon profiles), Suravenir and MACSF
  [S2][S4][S5][S7][S3]; 0,30 % of amounts switched at SMAvie BTP [S1].
- Under a horizon profile the holder generally **cannot** make their own arbitrages [S1][S2][S4].
- Changing the declared retirement date triggers an immediate re-allocation of the whole balance
  [S3][S4], which a projection model must treat as an instantaneous mix change, not a gradual one.
- Insurers reserve the right to change a profile's underlying allocation unilaterally to keep the
  regulatory de-risking [S3][S4] — so the published grid is a snapshot, not a contractual promise.

### 6. Charges — the full taxonomy with published figures

Every figure below is a **maximum** stated in a notice or in a regulated fee table.

| Charge | S1 SMAvie BTP | S2 Generali | S3 MACSF | S4 Spirica/LinXea | S5 Spirica/ERES | S6 Spirica/Bourse Direct | S7 Suravenir | S8 Cardif | S10 Predica |
|---|---|---|---|---|---|---|---|---|---|
| *Frais sur versement* | 4 % | 4,50 % | 3 % (2,5 % under *abonnement*) | 0 % | 4,80 % (incl. incoming transfers) | 3,50 % | 0 % | 2,50 % | 2,5 % |
| Association fee | €0,96 p.a. | €30 once | €10 once | €10 once | €25 once | €10 once | n/s | €20 once | n/s |
| Euro fund AUM charge | 0,084 %/month ≈ 1 % p.a. (incl. 0,12 % *garantie plancher*) | 0,90 % p.a. | 0,50 % p.a. | 2,00 % p.a. | 2,30 % p.a. | 2,30 % p.a. | 0,80 % p.a. | 0,70 % p.a. | n/s |
| UC AUM charge | same ≈ 1 % p.a. | 1 % p.a. (1,10 % on ETFs and equities) | 0,50 % p.a. | 0,50 % p.a. | 1 % p.a. free mgt / 0,85 % p.a. piloted | 1 % p.a. | 0,60 % p.a. (0,90 % under arbitrage mandate) | 0,70 % p.a. | n/s |
| Horizon-management surcharge | none (inside the 1 %) | 0,50 % p.a. | none | none | none | none | none | none (inside the 0,70 %) | n/s |
| Discretionary *gestion pilotée* surcharge | n/a | 0,50 % p.a. | n/a | 0,20 %–0,70 % p.a. | n/a | 0,80 % p.a. | n/a | n/a | n/a |
| Arbitrage | 0,30 % piloted / 0,50 % free management, first free each year | 0,50 %, min €30 by post, €15 online | 0 % | n/s in encadré | 1st free each year then 0,50 % | 0,80 %, min €50 | 0 % | 1 % | n/s |
| Outgoing transfer | 1 %, nil after 5 years | 1 % in first 5 years, nil after | 1 % before 5th anniversary, nil after | 1 % before 5th anniversary | 1 % before 5th anniversary | 1 % before 5th anniversary | 1 % if within 5 years | 1 % before year 5, 0 % after, **plus up to 15 % euro-fund reduction** | n/s |
| Capital exit | 0 % | 0 % | 0 % | n/s | n/s | n/s | 0 % | 0 % | n/s |
| *Frais d'arrérages* on the annuity | 1 % of instalments | 0 % | **3 %** of each gross instalment | 0,50 %, capped at 1 % of the monthly PASS per instalment | 0 % | 0,50 % | 0 % | **1,5 %** of each gross instalment | n/s |
| Annuity-phase AUM charge | ≈ 1 % p.a. on assets backing annuities | 0,60 % p.a. | n/s | 2 % p.a. on the annuity support | 2,30 % p.a. | n/s | **0,80 % p.a. on annuity reserves** | n/s | n/s |
| Death-cover charge | 0,12 % p.a. (inside the 1 %) | n/s | 0,10 % p.a. on UC to age 70 | optional, not priced in encadré | n/a | optional | 0,15 ‰–5,15 ‰ per month of capital at risk, by age | n/a | n/a |

- Other one-offs found: SMAvie BTP "A Contrario" automatic arbitrage 0,50 % capped at €5 per operation
  [S1]; Generali *sécurisation des plus-values* 0,50 % of the amount moved [S2]; Spirica option
  arbitrages 0,50 % capped at €300 [S6]; Suravenir 0,10 % on ETF trades [S7]; MACSF unlisted-asset
  penalties of 3 % (private debt) and 5 % (unlisted equity) in the *profil Libre* [S3]; SMAvie BTP
  10 % maximum entry rights on its property unit [S1].
- **Fund-level charges are separate and larger than the wrapper charge.** Cardif's published averages
  for its PER: equity funds 1,43 % p.a. (0,94 % retroceded to distributor and plan manager), bond
  funds 0,91 % (0,45 %), real-estate funds 2,00 % (0,50 %), diversified 1,17 % (0,57 %); piloted
  profiles average 1,39 % prudent and 1,26 % équilibré [S8]. Total cost of ownership on a UC therefore
  runs roughly 1,6 %–2,7 % p.a. before any horizon surcharge.
- Charge **basis and timing** differ and are load-bearing for a monthly model: end-of-month balance,
  monthly [S1]; quarterly on UC by cancelling units, annually on the euro fund with value date
  31 December on a pro rata temporis basis [S2]; annually at 31 December on both [S3]; accrued
  **daily** on the daily balance, levied annually on the euro fund and monthly on UC [S7].

### 7. Interest crediting, technical rate, and participation aux bénéfices

- **Maximum technical interest rate for a PER is 0 %** — "Les tarifs pratiqués par les entreprises
  d'assurance au titre des plans d'épargne retraite sont établis d'après un taux d'intérêt technique
  au plus égal à 0 %" [R9 A. 142-1]. Every contract that states a rate states 0 %: guaranteed annual
  rate 0 % gross of charges with no contractual *taux minimum garanti* and no loyalty clause [S1];
  technical rate 0 % for annuity conversion [S2]; annuity mathematical provision at a 0 % technical
  rate [S3]; guaranteed annual interest rate 0,00 % for the whole contract term [S7]. **A PER euro
  fund has no guaranteed accumulation rate; it has a guaranteed capital floor plus profit sharing.**
- Generali is the exception on the accumulation side: it announces a *taux minimum garanti* at the
  start of each civil year, the PB rate served cannot fall below it, and on any exit during the year
  only that announced rate applies pro rata temporis [S2].
- **Profit sharing.** The statutory framework is arts. L. 132-29, A. 132-10, A. 132-11 and following
  of the Code des assurances, and the PB may be used to revalue euro commitments, to revalue
  annuities in payment, or be placed in whole or in part in a *provision pour participation aux
  bénéfices* for later redistribution and smoothing [S1 §12]. Generali determines the annual PB amount
  under art. A. 132-16 and allocates it by criteria set at the start of the year — the UC proportion
  on the membership, the balance, the management mode, the seniority — so several PB rates coexist on
  one contract [S2]. Spirica and Suravenir have **no contractual PB clause** on the euro part
  [S4][S5][S6][S7]; SMAvie BTP does [S1].
- **Crediting frequency** varies enormously: weekly, at a rate derived from a quarterly prospective PB
  assessment, definitively acquired each Friday [S1]; daily compounding with the annual PB credited at
  value date 31 December [S2]; annual at 31 December [S3]; annual with pro rata temporis treatment of
  partial exits at the served annual rate and of total exits at a rate fixed annually by the insurer
  [S7].
- A euro fund **crediting data point**: Cardif Retraite's PER euro fund earned a gross asset return of
  **3,38 %** in 2025, bore a **0,70 %** annual management charge, and served a **net rate of 2,75 %**
  [S9]. That is the only complete gross-charge-net triple retrieved. No industry-average *fonds en
  euros* revaluation rate was found on the France Assureurs pages fetched [R23].
- 100 % of UC coupons and dividends are reinvested [S1][S4][S6], except SCPI units at Spirica/ERES
  where 90 % is passed through [S5].

### 8. Blocage and the cas de déblocage anticipé

- Savings are blocked until the earliest of pension liquidation and the L. 161-17-2 age
  [R3 L. 224-1]. The contracts describe the accumulation phase as having **no surrender right except
  in the statutory cases** [S2][S3][S4][S7].
- The statutory list, as consolidated at 14 June 2026 [R3 L. 224-4 I], is **seven** items, not six:
  1. death of the spouse or PACS partner;
  2. invalidity of the holder, a child, the spouse or PACS partner, within the 2° and 3° of
     art. L. 341-4 of the Code de la sécurité sociale;
  2 bis. serious illness, disability or a particularly grave accident affecting a dependent child;
  3. over-indebtedness within art. L. 711-1 of the Code de la consommation, at the request of the
     over-indebtedness commission;
  4. expiry of unemployment insurance rights, or a former director / *membre du directoire* /
     *membre du conseil de surveillance* who has not liquidated a pension and has held neither an
     employment contract nor a corporate office for at least two years;
  5. cessation of self-employment following a judicial liquidation under Title IV of Book VI of the
     Code de commerce, or any situation justified by the president of the commercial court in a
     *conciliation* under art. L. 611-4;
  6. use of the savings to acquire the **main residence** — rights from compulsory contributions
     (C3) cannot be released for this reason;
  7. the holder is under 18 at the date of the request.
- The government's own consumer pages still describe **six** cases [R21], while service-public.fr
  lists the serious-illness and the under-18 cases as well [R20]. SMAvie BTP's June 2026 notice
  reproduces all seven [S1]. The classic "six cas de déblocage anticipé" formulation is therefore
  out of date; the modelling list should be the statutory one.
- Early release is paid as a **single payment** of all or part of the eligible rights, at the holder's
  choice [R5 D. 224-4]. SMAvie BTP requires the triggering event to occur after adhesion and before
  the planned retirement age, sets a €750 minimum on a partial release, requires a residual balance
  of at least €750 with €150 per support, and pays within ten working days [S1]. Generali, MACSF and
  Suravenir levy **no charge** on an exceptional surrender [S2][S3][S7].
- Death of the holder before maturity **closes the plan** [R3 L. 224-4 II][R21].
- Statistically, early releases and transfers together are by far the largest accumulation-phase
  outflow: €1 651 m in 2024 against €93 m of death benefits, on €70,7 bn of individual-PER provisions
  [R22]. No public split between the seven causes was found [unverified].

### 9. Exit at retirement — capital or annuity

- At maturity, C3 rights are delivered as a **life annuity**; C1 and C2 rights are delivered at the
  holder's choice as **"un capital, libéré en une fois ou de manière fractionnée"** or as a life
  annuity, unless the holder has irrevocably opted for the annuity beforehand [R3 L. 224-5]. Both
  forms may be mixed [R20][R21].
- The irrevocable annuity election may be made at adhesion or later; the insurer must warn the member
  in writing of its irrevocable character [S1][S2][S4].
- Fractional capital exit is genuinely fractional: SMAvie BTP sets a €750 minimum per instalment with
  a €750 residual and €150 per support, and pays within ten working days net of tax and social levies
  [S1]. Once a fractional capital settlement has begun, MACSF accepts no further contributions [S3].
- Take-up in practice, from the only public breakdown found: of €1 093 m paid in 2024 on individual
  PERs in the payment phase, **€516 m** were annuities in payment, **€305 m** capital exits and
  **€272 m** small annuities commuted to a lump sum at outset; average annuity **€1 300 p.a.**,
  average capital exit **€12 500**, average commuted amount **€16 200** [R22]. About **9,4 %** of
  individual PER plans (395 700 of 4 195 500) were in the payment phase at end-2024 [R22].
- The manager must, from five years before retirement, answer questions about rights and suitable
  exit options, and must notify the holder of that right six months in advance [R4 L. 224-30].

### 10. Annuity conversion mechanics

- **Technical rate 0 %** by regulation [R9 A. 142-1], confirmed in the contracts [S2][S3][S7].
- **Mortality basis.** Art. A. 335-1 allows either homologated tables or the insurer's own experience
  tables certified by an independent actuary, but an experience-table tariff can never be cheaper
  than the homologated table for annuities [R11]. The homologated annuity tables are the generational
  **TGF05** (female lives) and **TGH05** (male lives) [R12]. No contract in the sample names its
  table; they refer to "la table de mortalité en vigueur" [S2][S4][S7] or "la table de mortalité des
  rentiers en vigueur à la date d'effet de la rente" [S7].
- **Which vintage of the table applies** is the subtle point. SMAvie BTP freezes the table **in force
  at the date of adhesion** for sums from tax-deductible voluntary *versements* and from an incoming
  transfer made at adhesion, and uses the table **in force at annuity commencement** for everything
  else [S1]. Generali, Spirica and Suravenir all use the table in force at conversion [S2][S4][S7].
  A model that assumes a single conversion basis will misprice the S1-style guarantee.
- **Payment frequency and timing**: quarterly in arrears, with a proportional first instalment where
  the effective date does not coincide with a calendar quarter [S1]; quarterly in arrears from the
  first day of the quarter following liquidation, with no proration on death except reversion [S2];
  monthly in arrears from the first day of the month following receipt of the file [S7].
- **Annuity options observed**:
  - plain life annuity [all];
  - **reversion** — 50 %–200 % in 10 % steps [S2]; 50 %–150 % in 10 % steps, or 50 %–100 % when
    combined with guaranteed annuities [S4]; **1 %–100 %** [S7]; the reversion beneficiary is fixed
    definitively at annuity set-up [S1];
  - **annuités garanties** — the number is bounded by art. A. 335-1 at the annuitant's life
    expectancy at the annuity effective date **minus five years** [S2][S4]; Suravenir narrows this to
    between 5 and 25 years in 5-year steps [S7]; SMAvie BTP offers the option and pays the remaining
    instalments to the designated beneficiaries [S1];
  - **rente par paliers** — 2 or 3 steps, intermediate steps ≤ 10 years, variation limited to −50 %
    and +100 % [S2]; at most two changes with the first two periods ≤ 10 years each [S4]; Suravenir
    publishes fixed schemes, e.g. 100 % for 5 or 10 years then 200 %, or 100 % / 125 % / 150 % [S7].
- **Small-annuity commutation.** An insurer may substitute a single capital payment, with the
  annuitant's agreement, where the monthly *quittance d'arrérages* does not exceed **€110** including
  statutory increases, the threshold being multiplied by the number of months in the payment period
  [R10 A. 160-2]. Contracts still quote the older PER-specific figures — €240 per quarter [S2] and
  €80 per month [S4] — reflecting the €100 and €80 vintages of art. A. 160-2-1 [R10]. This mechanism
  is not marginal: it accounted for €272 m of 2024 individual-PER benefits, at an average of €16 200
  per case [R22].
- Annuities in payment are revalued through the profit-sharing account [S1][S4][S7], on the
  membership anniversary [S1].
- **Reversion recomputation:** Suravenir recomputes the reversionary annuity if the surviving spouse
  or PACS partner at death is not the one who held that status at liquidation, or if another
  entitled person appears [S7] — a genuine option cost that no sampled tariff quantifies.
- Annuitants must return an annual life certificate; failure suspends payment until it is produced,
  after which arrears are paid [S2][S7].

### 11. Taxation on entry — deductibility and the plafond

- C1 *versements* are deductible from *revenu net global* under CGI art. 163 quatervicies; the
  self-employed may instead deduct against professional income under art. 154 bis or 154 bis-0 A
  [R13][R18][S7 annexe fiscale].
- **The plafond épargne retraite** is the greater of 10 % of the prior year's net professional income
  capped at 8 PASS, and 10 % of the PASS, less professional retirement contributions already deducted
  or exempted (arts. 83, 154 bis, 154 bis-0 A, 156) [R13][R17]. The PASS used is that of the calendar
  year **preceding** the *versement* [R17].
- Published euro figures, for *versements* made in the year whose ceiling is computed on the prior
  year's PASS: minimum **€4 710**, maximum **€37 680** [R18][R20]; the ceiling is reduced by employer
  contributions to a PERCO/PERECO/PERO within the income-tax-exempt limit of **€7 419**, and by up to
  10 days of time-savings-account days [R18]. The two figures are consistent with a PASS of €47 100
  (4 710 = 10 % × 47 100; 37 680 = 10 % × 8 × 47 100); the €7 419 figure corresponds to 16 % of a
  PASS of €46 368 — i.e. the two are drawn from **different PASS vintages**, so a model should
  parameterise the PASS rather than hard-code any of them [unverified as to the intended vintage of
  €7 419].
- **Carry-forward**: unused allowance from the three preceding years may be added [R18][R20], and the
  consolidated CGI text now reads five years [R13], with the transition being three years for the
  unused 2024 and 2025 allowances and five years for sums paid from 2026 [R20][R21].
- Married and PACS couples may pool their ceilings on express request [R13][R17][R21].
- **From 1 January 2026, contributions paid after the holder's 70th birthday are no longer
  deductible** [R21][R20].
- **The holder may decline the deduction.** That election is the pivot of the whole exit tax
  treatment [R19][R20][R21][S7].

### 12. Taxation at exit — by compartment and by the deduction election

Suravenir's tax annex sets out the full matrix, which matches the government pages [S7][R20][R21]:

| Origin | On payment in | Capital exit | Annuity exit |
|---|---|---|---|
| C1, contributions **deducted** | deducted under CGI 163 quatervicies (or 154 bis / 154 bis-0 A) | contribution part: income tax at the progressive scale **without the 10 % pension deduction**, no social levies. Gains: PFU 12,8 % + social levies | taxed as a pension after the 10 % abatement; social levies on the *rente viagère à titre onéreux* taxable fraction |
| C1, contributions **not deducted** | no tax relief | contribution part **exempt** from income tax and social levies. Gains: PFU 12,8 % + social levies | taxed as a *rente viagère à titre onéreux*: income tax on the age-graded taxable fraction only; social levies on the taxable fraction |
| C2 (*épargne salariale*) | already taxed in the source scheme | exempt contribution: social levies on the gains only. Non-exempt: PFU 12,8 % + social levies on the gains | *rente viagère à titre onéreux* with the age-graded abatement; social levies on the taxable fraction |
| C3 (*versements obligatoires*) | already taxed in the source scheme | **capital exit not permitted**, except commutation of a small annuity | pension regime after the 10 % abatement; social levies at **10,1 %** |

- The **age-graded fractions** for a *rente viagère à titre onéreux* [R20][R21][S7]:

| Age at the annuity's first payment | Abatement | Taxable fraction |
|---|---|---|
| under 50 | 30 % | 70 % |
| 50 to 59 | 50 % | 50 % |
| 60 to 69 | 60 % | 40 % |
| 70 and over | 70 % | 30 % |

- **Social levy rates**: 17,2 % through 31 December 2025 and **18,6 % from 1 January 2026**, applying
  both to annuities paid from that date and to the gains component of a capital exit, so the flat
  levy on gains moves from **30 %** (12,8 % + 17,2 %) to **31,4 %** (12,8 % + 18,6 %) [R20][R21]. C3
  annuities bear 10,1 % [S7].
- Capital from a PERIN is reported on lines 1AI–1DI and "taxed at ordinary income-tax rates without
  reduction" — the 7,5 % flat option and the *quotient* available for PERP capital do **not** apply to
  the PERIN [R19].
- Taxation on an **early release** was not researched line by line; service-public states that where
  contributions were deducted, the released capital is taxed at the marginal income-tax rate
  [unverified as to the treatment of each of the seven causes — several are in practice exempt, but
  no retrieved official document sets that out].

### 13. Death benefits

- **During accumulation**, the holder's death closes the plan [R3 L. 224-4 II]. In the insurance form
  the accumulated savings go to the named beneficiaries as capital or annuity under the life
  insurance rules [R20][R21]; in the *compte-titres* form they fall into the estate [R20][R21].
- **Contractual death benefit** in the sample: the accumulated savings at the date the death is
  notified, valued on the ordinary valuation rules, with the euro part revalued to that date
  [S3 ART 11]. Generali additionally converts the benefit into a *rente temporaire d'éducation* to
  minor children until their 25th birthday, or a life annuity to the spouse/PACS partner where the
  children are adult, computed at the tariff in force at the date of death and free of *arrérage*
  charges [S2].
- **Garantie plancher** (a death floor at premiums paid) is standard rather than optional in two
  contracts:
  - SMAvie BTP — benefit not less than premiums net of charges minus benefits already paid; the
    *Capital Complémentaire* top-up is the shortfall of the account value against that floor, pro-rated
    once aggregate net premiums across the member's covered contracts exceed **€800 000**; cover runs
    one year and renews annually, ceases at the **70th birthday**, on total surrender, on transfer or
    on cancellation; first-year suicide, war, terrorism and nuclear events excluded; charged **0,12 %
    p.a.** inside the 1 % management charge, revisable by agreement between GPBF and the insurer
    according to the guarantee's results or the group's demography [S1].
  - MACSF — the settled amount cannot be less than contributions net of loading plus euro-fund
    interest net of management charges; granted to the **70th birthday** and capped at **€762 245**
    across all contracts; charged **0,10 % p.a.** on UC balances at 31 December, ceasing after the
    31 December following the 70th birthday; revisable by agreement between subscriber and insurer for
    demographic or experience reasons [S3].
- **Optional death cover** (Suravenir): reimburses the *capital sous risque*, defined as the positive
  difference between cumulative premiums net of charges less exits and the transfer value at the date
  the death certificate is received; open to members aged 12 to under 70 at adhesion, after a one-year
  waiting period, **no medical underwriting**, capped at **€100 000** per contract, ending at the
  **75th birthday** or earlier on surrender, annuity conversion, total capital exit, transfer or
  cancellation; monthly premium **0,15 ‰ to 5,15 ‰ of the capital at risk by age**, printed as a full
  age table (€0,15 per €1 000 per month to age 30, €0,30 at 40, €0,50 at 45, €0,79 at 51, €1,10 at 56,
  €1,44 at 60, €2,15 at 65, €2,80 at 68, €3,05 at 69, €3,33 at 70, €3,64 at 71, €3,96 at 72); standard
  exclusions including first-year suicide [S7]. This is the only published mortality rate card in the
  sample and is directly usable as a decrement/charge basis for a death rider.
- **During the annuity phase**: reversion continues at the elected rate to the beneficiary named
  definitively at set-up; guaranteed annuities continue at the full amount to the designated
  beneficiaries; absent either option the annuity stops at death [S1][S2][S7].
- **Estate taxation of the insurance form** [R14][R15][R20][R21]:
  - death **before 70** — art. 990 I: **€152 500** abatement per beneficiary, then **20 %** on the
    taxable share up to €700 000 and **31,25 %** above;
  - death **after 70** — art. 757 B: **the whole death benefit** enters the inheritance-duty base, not
    just the premiums paid after 70, because CGI 757 B contains an express PER carve-out — "les
    sommes … dues … à raison du décès après l'âge de soixante-dix ans du titulaire d'un plan
    d'épargne retraite" — subject to a **€30 500** global abatement across all contracts on the same
    life [R15].
  - The trigger is therefore the **age at death**, not the age at which each premium was paid — the
    opposite of ordinary assurance vie. Crossing 70 alive is a cliff edge in the PER assurance, and
    it coincides with the age at which the *garantie plancher* stops [S1][S3] and, from 2026, with
    the age at which contributions stop being deductible [R21].

### 14. Transferability and transfer value

- Rights under accumulation are transferable to **any** other PER; transfer does not change the
  surrender or liquidation conditions [R3 L. 224-6].
- **PER → PER fee cap: 1 % of acquired rights, nil after five years from the first *versement* in the
  plan, or where the transfer occurs from the L. 224-1 maturity** [R3 L. 224-6][R21]. Every contract
  in the sample reproduces the 1 % / five-year rule [S1][S2][S3][S4][S5][S6][S7][S8]. MACSF adds that
  the fee is also nil once the member has liquidated a compulsory pension or reached the L. 161-17-2
  age [S3].
- **Legacy product → PER** (PERP, Madelin, PERCO, article 83, PREFON, COREM, CRH) is a different rule:
  1 % of acquired rights, nil after **ten years** from the first contribution, with a six-month
  processing deadline [R5 D. 224-18], under the enabling article L. 224-40 [R4]. A PERCO-to-individual-
  PER transfer is limited to once every three years [R4 L. 224-40]. Incoming transfers are free at
  MACSF and Suravenir [S3][S7] but bear the full 4,80 % entry loading at Spirica/ERES [S5].
- **The 15 % transfer-value reduction is the sleeper.** Where the transfer right on the mathematical
  provisions exceeds the asset share representing them, the plan may reduce the transfer value, "sans
  que cette réduction puisse toutefois excéder **15 %** de la valeur des droits individuels du
  titulaire relatifs à des engagements exprimés en euros" [R5 R. 224-6][R3 L. 224-6]. Cardif states
  it explicitly in its regulated fee table alongside the 1 % cap [S8]; MACSF states the right in
  general terms [S3]. In a rising-rate scenario this dominates the 1 % fee by an order of magnitude.
- Every contract publishes a **minimum transfer-value table for the first eight years** on maximum
  charges [S1 §7.4][S2][S3][S4][S7] — the French equivalent of a reduction-in-yield disclosure, and a
  natural validation target for a projection model.
- Settlement times: 10 working days [S1], 15 days from expiry of the transfer cancellation period
  [S2], up to 2 months [S4][S6].

### 15. Information duties and the standardised fee disclosure

- The annual statement required by R. 224-2 must give the value of rights at 31 December and its
  history, contributions by L. 224-2 category, withdrawals and surrenders, **all charges taken in the
  year with the total in euros**, the transfer value and transfer conditions and cost, and per asset
  the gross-of-charges annual performance, the net-of-charges annual performance and the annual
  charges taken; for group insurance contracts, the profit sharing and the average yield; for
  de-risking allocations, the performance and the de-risking schedule [R5 R. 224-2].
- The arrêté du 24 février 2022 prescribes a standardised fee table with a defined column set,
  including a **"frais totaux"** column combining asset charges and recurring contract charges, in
  force from 1 July 2022 and from 1 January 2023 for the annual statements [R16]. S8 and S9 are live
  instances: S8 is the plan-level grid, S9 the per-support grid.
- Duty of advice at sale: suitability assessment covering the prospect's situation, financial
  knowledge, horizon, return expectations, objectives including sustainability preferences and
  retirement needs, plus disclosure of characteristics, management methods, availability conditions
  and the tax and social treatment [R4 L. 224-29].
- Pre-retirement consultation right from five years out, with a six-month advance notification
  [R4 L. 224-30].

### 16. Market size and behaviour — parameters for assumption setting

- All PERs, all providers, 30 September 2025: **12,7 million** holders and **€141,1 bn**, +19 % over
  twelve months; PER individuels **€82,4 bn**, PER d'entreprise collectifs €31,7 bn, PER obligatoires
  €27,1 bn [R24].
- Insurance-carried PERs, 31 December 2025: **7,9 million** insured and **€111,9 bn**; 2025
  *versements* **€20,2 bn** (+16 %); net inflow €11,0 bn; about 1 million new plans in 2025 [R23].
  At 30 June 2025 insurers held **75 %** of the €136,1 bn all-provider *encours* [R23].
- PER individuels written by insurers, 31 December 2024 [R22]:
  - **4 195 500** plans in force, +18,7 %; **3 799 800** (91 %) in accumulation, **395 700** in payment;
  - contributions **€10 496 m** (+20,2 %), of which **€6 838 m (65 %)** into UC;
  - benefits **€2 837 m**: €93 m death, €1 651 m early release and transfer, €516 m annuities in
    payment, €305 m capital exits, €272 m small annuities commuted;
  - mathematical provisions **€70,7 bn**, €63,0 bn in accumulation and €7,7 bn in payment; UC
    **€32,9 bn = 47 %** of provisions and **52 %** in accumulation;
  - average balance **€16 600** in accumulation and **€19 500** in payment; average annuity in payment
    **€1 300 p.a.**; average capital exit **€12 500**; average commuted small annuity **€16 200**.
- Derived ratios useful as behavioural assumptions, computed from [R22] and flagged as derived rather
  than published: benefits from accumulation-phase plans run about **2,8 %** of accumulation-phase
  provisions per year (1 744 / 63 000); death benefits about **0,15 %** (93 / 63 000); the ratio of
  new money to opening provisions is roughly **18 %**, reflecting a young book still in rapid growth.
  Every one of these is contaminated by the market's growth phase and none should be read as a
  steady-state assumption.
- No public data was found on: the split of early releases between the seven statutory causes; the
  proportion of holders who decline the tax deduction; the distribution of horizon profiles chosen;
  the proportion who opt irrevocably for the annuity; or lapse/transfer-out rates by duration
  [unverified].

### 17. Prudential and valuation context

- PER assurance commitments sit in a ring-fenced *comptabilité auxiliaire d'affectation* with a
  priority claim for policyholders and an ACPR-supervised recovery mechanism on under-coverage
  [R8 L. 142-4 to L. 142-6].
- Tariffs use a technical rate of at most 0 % [R9 A. 142-1] and, for annuities, a mortality basis at
  least as prudent as the homologated TGF05/TGH05 generational tables [R11][R12].
- The annuity-phase mathematical provision is "la valeur des engagements de rente, fonction de la
  table de mortalité et du taux d'intérêt technique à 0 % tels que définis par la réglementation en
  vigueur" [S3 ART 12 B] — i.e. a 0 %-discounted expected present value on the regulatory table, which
  makes the statutory reserve a pure life-contingent annuity factor with no interest offset.
- Profit sharing is governed by arts. L. 132-29 and A. 132-10 / A. 132-11 and following, with the
  *provision pour participation aux bénéfices* as the smoothing device [S1 §12][S7].
- Solvency II technical provisions, SCR and risk margin for this business were **not** researched
  here; they belong to the frlib cross-product reference library. Nothing in this file should be read
  as a statement about the Solvency II treatment of a PER [unverified].

### 18. What has no public figure — mark these [std] when drafting

- Any **annuity conversion rate** or annuity factor. No sampled insurer publishes a rate card; the
  notices say only "the table in force" and "the technical rate in force" [S1][S2][S4][S7]. The
  TGF05/TGH05 tables themselves are annexed to a public arrêté [R12] but were not extracted here.
- **Lapse, transfer-out, early-release and annuitisation election rates** by duration and age.
- The **proportion of holders who decline the deduction**, which drives the exit tax split.
- The **mix between horizon profiles** and the proportion who opt out of *gestion pilotée*.
- **Expense loadings by function** (acquisition, maintenance, claims). Only the charge cap is public,
  never the insurer's own unit cost.
- **The insurer's PB policy** — the target rate, the smoothing horizon, and the level of the
  *provision pour participation aux bénéfices*. Only one gross/charge/net triple was retrieved
  (Cardif 3,38 % / 0,70 % / 2,75 % for 2025) [S9].
- **UC return and volatility assumptions**, and the mapping from the horizon grid's asset buckets to
  a modelled return process.
- The **cost of the reversion recomputation option** [S7] and of the *rente par paliers* options
  [S2][S4][S7].
- The **exact wording of the arrêté defining "actifs présentant un profil d'investissement à faible
  risque"** — the two contract definitions found (SRRI ≤ 3 [S7], synthetic risk indicator ≤ 2 [S3])
  disagree.

---

## Variations across insurers

| Feature | SMAvie BTP [S1] | Generali [S2] | MACSF [S3] | Spirica — LinXea [S4] | Spirica — ERES [S5] | Spirica — Bourse Direct [S6] | Suravenir [S7] | Cardif [S8][S9] | Predica [S10] |
|---|---|---|---|---|---|---|---|---|---|
| Distribution | mutual, sector association | association + IFA/online | professional mutual | online broker | IFA network | online broker | online brokers | retail bank | retail bank |
| *Frais sur versement* | 4 % | 4,50 % | 3 % / 2,5 % | **0 %** | **4,80 %** | 3,50 % | **0 %** | 2,50 % | 2,5 % |
| Euro fund charge | ≈ 1 % | 0,90 % | **0,50 %** | 2,00 % | 2,30 % | 2,30 % | 0,80 % | 0,70 % | n/s |
| UC charge | ≈ 1 % | 1,00–1,10 % | **0,50 %** | **0,50 %** | 0,85–1,00 % | 1,00 % | 0,60 % | 0,70 % | n/s |
| Horizon management surcharge | none | 0,50 % | none | none | none | none | none | none | n/s |
| *Frais d'arrérages* | 1 % | **0 %** | **3 %** | 0,50 % capped | 0 % | 0,50 % | **0 %** | 1,5 % | n/s |
| Annuity-phase AUM charge | ≈ 1 % | 0,60 % | n/s | 2,00 % | 2,30 % | n/s | 0,80 % | n/s | n/s |
| Death floor | *garantie plancher* included, to 70, €800 k cap | none stated | *garantie plancher* included, to 70, €762 245 cap | optional | optional | optional | optional rider, priced 0,15–5,15 ‰/month, €100 k cap, to 75 | none stated | n/s |
| Euro fund crediting | **weekly**, definitively acquired each Friday | daily compounding, PB at 31 December | annual at 31 December | annual | annual | annual | annual, daily-accrued charges | annual | n/s |
| Contractual PB clause | yes | no (but a *taux minimum garanti* is announced each year) | not stated in encadré | no | no | no | no | n/s | n/s |
| Glide-path bands | **20 one-year bands** | 4 regulatory bands | age-driven, published in a financial annex | regulatory minima | regulatory minima | regulatory minima | regulatory minima quoted verbatim | regulatory minima | 3 profiles |
| Rebalancing | semi-annual, Q2 and Q4 | semi-annual | semi-annual, 15 Mar / 15 Sep | threshold-driven, at least semi-annual | at least semi-annual | at least semi-annual | **quarterly** | n/s | n/s |
| Annuity table vintage | **frozen at adhesion** for deductible C1 and adhesion-date transfers, current otherwise | current at liquidation | current | current | current | current | current | n/s | n/s |
| Annuity frequency | quarterly in arrears | quarterly in arrears | n/s | n/s | n/s | n/s | **monthly in arrears** | n/s | n/s |
| Reversion range | contract-specified | 50–200 % in 10 % steps | on option | 50–150 % (50–100 % with guaranteed annuities) | n/s | n/s | **1–100 %** | n/s | individual or reversionary |
| Distinctive | GPBF levy €0,96/yr; retirement age capped at 80 then tacitly renewed; "A Contrario" arbitrage | euro fund capped at 40 % of a *versement*; *rente temporaire d'éducation* to minors to 25 | all arbitrages free; French residence required; unlisted-asset penalties | *provision de diversification* support with 80 % maturity guarantee | 4,80 % loading applied to incoming transfers too | ad hoc arbitrage 0,80 % with €50 floor | published age-rated death-cover premium table; SRRI ≤ 3 low-risk definition | FRPS carrier; 15 % transfer-value reduction stated in the fee table; €30 minimum *versement* | 91 vs 140 supports across the two brands |

**The dominant variation is distributor, not insurer.** Spirica writes S4, S5 and S6 under the same
insurance licence, with the same *Fonds Euro PER Nouvelle Génération*, the same three horizon
profiles and the same annuity options — yet the entry loading runs 0 % / 4,80 % / 3,50 %, the euro
fund charge 2,00 % / 2,30 % / 2,30 %, the UC charge 0,50 % / 1,00 % / 1,00 %, and the *arrérage*
charge 0,50 % / 0 % / 0,50 %. Any statement of the form "insurer X charges Y on a PER" is meaningless
in this market; the contract, not the carrier, is the unit of analysis.

**The product mechanics, by contrast, are close to uniform,** because the statute fixes them: three
compartments [R3 L. 224-2], the same seven early-release cases [R3 L. 224-4], the same exit menu
[R3 L. 224-5], the same 1 %/five-year transfer cap [R3 L. 224-6], a 0 % maximum technical rate
[R9 A. 142-1], and a de-risking grid that most insurers simply adopt at its regulatory minimum
[R6][S2][S7]. A reference implementation can therefore model **one** PER assurance with the statutory
mechanics and treat the charge basis as a parameter set.

Representative design for a reference implementation: an annual-step model of a compartment-1 PER
individuel assurance with a euro fund and a UC bucket; *gestion pilotée par horizon* on the
"Équilibré Horizon Retraite" regulatory grid (0 % / 20 % / 50 % / 70 % low-risk at ≥ 10, 10, 5 and 2
years to the declared retirement date) with annual rebalancing; entry loading, separate euro and UC
AUM charges, a 1 % transfer indemnity for the first five years, and an *arrérage* charge; euro-fund
crediting as a guaranteed capital floor plus a profit-sharing rate; exit at the declared retirement
age as capital, fractional capital or a 0 %-technical-rate life annuity on a generational table; and a
death benefit equal to the account value, optionally floored at premiums net of charges to age 70.
That covers S1–S9 with configuration.

Variations that exist but were **not** modelled or sourced here: the *PER bancaire* (compte-titres)
form, whose accumulation has no insurance mechanics at all and whose death treatment is the ordinary
estate [R20][R21]; PER d'entreprise collectif and PER obligatoire, which share the compartments and
the exit rules but differ in funding and governance [R2][R22]; *unités de rente* products, for which
L. 224-3's de-risking paragraphs are switched off [R3] and L. 142-8 sets a special transfer value
[R8]; and the *provision de diversification* support, which belongs to the frlib `eurocroissance`
product [S4][S6].

---

## Gaps and caveats

1. **No annuity rate card exists.** Not one of the ten primary sources publishes an annuity
   conversion factor, a rated age, or a tariff. The contracts say only "la table de mortalité en
   vigueur" and "le taux d'intérêt technique en vigueur" [S1][S2][S4][S7]. Everything about the
   annuity's price in a reference implementation must be built from the public regulatory basis
   (TGF05/TGH05 [R12], technical rate ≤ 0 % [R9]) and marked **[std]**.
2. **TGF05/TGH05 rate tables were not extracted.** The arrêté du 1er août 2006 was retrieved and its
   article 2 confirms the two tables by name [R12], but the annexed rate tables themselves were not
   pulled and are not reproduced here. Any decrement CSV shipped with this product must be a [std]
   proxy, exactly as uklib does with CMI tables.
3. **Two `economie.gouv.fr` fetches returned HTTP 403** through the plain fetcher. The page was then
   retrieved with a browser User-Agent via curl and converted locally [R21]; its content is quoted as
   verified, but the retrieval route is non-standard and is recorded as such. The
   `cardif.fr/transparence-frais...` landing page was retrieved but proved to be a link hub carrying
   no figures of its own; the figures come from the two Cardif PDFs behind it [S8][S9].
4. **No Predica, LCL, AXA, Sogécap, Swiss Life, Abeille, Groupama, AG2R La Mondiale or Malakoff
   Humanis notice d'information was retrieved.** The only Crédit Agricole group document obtained is
   a 2019 press release [S10], whose figures (€500 minimum, 2,5 % loading) are launch-date and may be
   stale; a search for Predica's PER notice returned only document-index and PRIIPs-portal pages. The
   bancassurance segment — which on the France Assureurs numbers writes the bulk of the market — is
   therefore represented in this file by fee tables [S8][S9][S10] and not by policy conditions.
5. **Four of the ten primary contracts are 2020–2022 vintages** (Generali PA9601NIB May 2020 [S2],
   Spirica CG9403 October 2020 [S4], CG9401 July 2020 [S6], CG9406 October 2022 [S5], Suravenir
   réf. 5257-2 September 2021 [S7]). They therefore predate the *loi industrie verte* unlisted-asset
   minima that took effect on 24 October 2024 [R7], and their glide paths show no private-equity
   line. Only S1 (June 2026), S3 (October 2024), S8 (March 2026) and S9 (July 2026) are current-regime
   documents. Charge levels in the older notices should be treated as indicative, not as today's
   rate card.
6. **The carry-forward period is stated inconsistently across official sources.** The consolidated
   CGI art. 163 quatervicies as retrieved reads "l'une des cinq années suivantes" [R13] and BOFiP
   likewise says five [R17], while impots.gouv.fr still says three [R18]; service-public.fr and
   economie.gouv.fr resolve it as three years for the unused 2024–2025 allowances and five years from
   2026 [R20][R21]. The 2026 transition is the reason, but the CGI verbatim sentence for the
   three-year rule was not isolated, so the exact statutory drafting is **[unverified]**.
7. **Plafond euro figures mix PASS vintages.** €4 710 and €37 680 are consistent with a PASS of
   €47 100; the €7 419 employer-contribution exemption limit corresponds to 16 % of a PASS of €46 368
   [R18]. The page does not state which year each applies to. Parameterise the PASS; do not hard-code
   these numbers.
8. **The "six cas de déblocage anticipé" is now wrong.** The consolidated L. 224-4 in force at
   14 June 2026 lists seven items including 2° bis (serious illness of a dependent child) and 7°
   (holder under 18) [R3]. economie.gouv.fr still says six [R21]; service-public.fr lists the extra
   ones [R20]; SMAvie BTP's June 2026 notice reproduces all seven [S1]. The commencement date and
   the amending instrument for 2° bis and 7° were not identified [unverified].
9. **Social levy rates are in transition and were sourced only from government consumer pages.** The
   move from 17,2 % to 18,6 % from 1 January 2026, and the corresponding 30 % → 31,4 % flat rate on
   gains, are stated by both service-public.fr [R20] and economie.gouv.fr [R21], but the enacting
   finance or social-security law was not retrieved and is **[unverified]**.
10. **Early-release taxation by cause was not researched.** Only the general statement that deducted
    contributions released early are taxed at the marginal rate was found; the exemptions that apply
    in practice to several of the seven causes are not documented from any retrieved source
    [unverified].
11. **The arrêté defining "actifs à faible risque" was not retrieved.** D. 224-3 delegates the
    definition to a ministerial arrêté [R5], and the two contract definitions found conflict
    (SRRI ≤ 3 [S7] versus synthetic risk indicator ≤ 2 [S3]). The regulatory definition is therefore
    **[unverified]**, and a model that classifies assets as low-risk must state which convention it
    adopts.
12. **The exact band labels of the unlisted-asset table are as the fetcher rendered them.** R6's
    part (b) percentages were extracted verbatim in French ("6 % jusqu'à 20 ans avant la date de
    liquidation envisagée…"), but the surrounding table structure of the consolidated arrêté was
    described differently by two successive fetches of the same URL, and no page image was inspected.
    The percentages are verified; the interpretation of "jusqu'à N ans" as a band rather than a
    threshold is **[unverified]**.
13. **No ACPR, EIOPA, Institut des actuaires or DREES document was retrieved for this product.** The
    prudential and reserving layer is therefore cited only through the Code des assurances
    [R8][R9][R11] and is deliberately left as **cited-not-specified**, consistent with the frlib
    posture on capital.
14. **The WebSearch budget was exhausted part-way through the session** (200 of 200 calls). The
    remainder of the discovery was done through the DuckDuckGo HTML endpoint via curl and through
    direct URL construction. Coverage of insurers is consequently opportunistic rather than
    systematic, and the absence of a given insurer from this file says nothing about its market
    position.
15. **The DG Trésor market figures span both PER forms.** The 12,7 million holders and €141,1 bn at
    Q3 2025 are consolidated across insurers, asset managers, mutuelles and provident institutions
    [R24]; the assurantiel subset is given separately by France Assureurs as 7,9 million and
    €111,9 bn at end-2025 [R23]. The two must not be mixed. The 2024 France Assureurs report [R22]
    remains the only source with a benefit-by-type breakdown, and it is a year older than the
    headline figures.
