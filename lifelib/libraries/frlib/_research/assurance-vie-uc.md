# Unit-linked multi-support life insurance (assurance vie multisupport — unités de compte) — research notes (France)

Research notes for the French multi-support life insurance contract (`contrat d'assurance vie
multisupport`) in its unit-linked dimension — savings expressed in `unités de compte` (UC,
"units of account") alongside a `fonds en euros` (the guaranteed euro-denominated fund), with
arbitrage between the two. These notes are the citation ground truth for the frlib
`assurance_vie_uc` product documents: source ids S1..S14 and R1..R18 below are frozen — never
renumber.

Access date for all citations: 2026-08-26.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document
that was actually fetched and read. `[unverified]` marks statements from general knowledge or
from secondary summaries of documents that could not be retrieved. Where a fetch failed the
failure is recorded and the item is kept only as a known reference (fetched_ok = false).

Retrieval method note: French insurer and regulator hosts frequently reject a plain fetcher.
Every PDF below was downloaded with a browser `User-Agent` and its text layer extracted
locally (PyMuPDF) rather than relying on a remote summariser; where that still failed the
failure is recorded verbatim.

Language note: French terms of art are kept in French and glossed on first use —
`unité de compte` (UC, a unit of a designated fund whose number, not value, the insurer
guarantees), `fonds en euros` (the insurer's guaranteed general-account fund),
`versement` (premium), `rachat` (surrender/withdrawal), `arbitrage` (switch between supports),
`valeur atteinte` / `épargne constituée` (account value), `capital sous risque` (net amount at
risk), `garantie plancher` (floor death benefit), `participation aux bénéfices` (profit
sharing), `prélèvements sociaux` (social levies), `notice d'information` (the policy booklet
for a group contract), `conditions générales` (policy conditions for an individual contract),
`document d'informations clés` (DIC — the PRIIPs KID).

---

## Primary sources

### S1 — Generali Vie, "Himalia — Note d'information valant Conditions générales" (PA8301CGP, October 2021)
- Publisher: Generali Vie (Generali France), individual life contract codes 8301/8302
- Doc type: Note d'information valant Conditions générales (policy conditions), 66 pp.
- URL: https://epargne.boursedirect.fr/uploads/files/products_fin/e1cf9a0d9a50ca064d2078bab00ec586/Himalia%20-%20Conditions%20G%C3%A9n%C3%A9rales.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Document code PA8301CGP — Octobre 2021.
  Retrieved from a distributor's document store (Bourse Direct); Generali's own host was not
  used.
- Content: a full-service individual multisupport contract. `Encadré` (the statutory summary
  box) fee schedule: `frais sur versements` 4.50% maximum; UC management charge 0.25% per
  quarter of the `valeur atteinte`, levied **by reducing the number of units**, i.e. 1.00% p.a.
  maximum; 0.375% per quarter (1.50% p.a.) on ETF (`OPC Indiciels`) and direct equity (`Actions`)
  supports; euro funds 0.90% p.a. (Actif Général, Euro Innovalia) and 1% (Elixence); the
  `fonds croissance` G Croissance 2020 1% p.a. levied weekly on the fund's asset value;
  `gestion pilotée` an extra 0.15% per quarter (0.60% p.a.) on UC; exit charges nil; arbitrage
  1% of the amount switched with a minimum of 30 € by post / 15 € online; the automatic
  arbitrage options (`sécurisation des plus-values`, `limitation des moins-values`,
  `limitation des moins-values relatives`) each charge 0.50% maximum of the amount transferred.
  Annexe 3 "Options garanties de prévoyance" carries the full `garantie plancher` terms and a
  published age tariff (see §7 below), a `garantie vie universelle` and a `garantie vie
  entière`. Gestion pilotée orientations with named advisers and equity bands. Automatic
  arbitrage options defined with `assiette` (reference base), weekly (Tuesday for the plancher
  premium, Friday for the options) observation and Monday execution.

### S2 — Generali Vie, "Document d'information valant Avenant aux Conditions générales du contrat d'assurance vie Himalia — G Croissance 2020" (PA8301AVTD, October 2020)
- Publisher: Generali Vie
- Doc type: Avenant (contract amendment) valant document d'information, 23 pp.
- URL: https://www.altaprofits.com/documentation/pdf/HIMALIA/Doc_info_valant_CG_Himalia.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Code PA8301AVTD (8301/8302) — Octobre 2020.
- Content: the amendment that adds `eurocroissance` engagements to Himalia. Used here only for
  what it says about the `garantie plancher` when a `provision de diversification` is present:
  the plancher may still be taken (`simple ou indexée`) below age 75; the policyholder must keep
  at least 10% of the contract's `valeur atteinte` on the euro fund so that the premium can be
  levied, with a warning letter if the euro share falls below 5%; the premium is never levied on
  the `fonds croissance`. Also carries the 8-year surrender-value simulation tables showing the
  UC unit count decaying at the quarterly rate.

### S3 — Generali Vie / Boursorama, "Bourso Vie — Notice d'information valant Conditions générales" (contract 5101)
- Publisher: Generali Vie (insurer), Boursorama (souscripteur / distributor)
- Doc type: Notice d'information valant Conditions générales (group contract with individual
  membership), 52 pp.
- URL: https://www.boursorama.com/pub/bourso/pdf/avie/cg-brsvie.pdf
- Retrieved: YES (PDF downloaded, full text extracted). No document code or date printed in the
  extracted text.
- Content: the online/low-charge end of the same insurer's range. `Frais sur versements` nil;
  UC (OPC, ETF) and Actions management charge 0.1875% per quarter, levied by reducing the number
  of units, i.e. 0.75% p.a. maximum; euro funds Eurossima and Euro Exclusif 0.75% p.a.; exit
  charges nil; the only "other" charge is 1% maximum of the amount transferred under the
  `sécurisation des plus-values` option. Article 9 lists the eligible UC universe as OPC,
  OPC Indiciels (ETF) and Actions. Article 19 "Revalorisation du capital en cas de décès" states
  that after death both the euro fund and the UC continue to be valued until the settlement
  valuation date, so UC values keep fluctuating up and down after death. Article 21 gives an
  8-year surrender-value table for a 10,000 € premium split 70% euro / 30% UC, with the UC
  column falling 100 → 99.2521 → 98.5098 → … → 94.1711 units, and separate euro-fund columns
  under `garantie plancher` option 1 and option 2 in rising / flat / falling UC scenarios.
  Annexe 3 repeats the Generali `garantie plancher` terms with the same age tariff as [S1] and a
  15 €/month levy threshold; the `garantie vie universelle` `capital sous risque` cap is
  500,000 € here.

### S4 — Spirica, "LINXEA Spirit 2 — Conditions Générales" (CG4445, 01/07/2024)
- Publisher: Spirica (Crédit Agricole Assurances), 16/18 bd de Vaugirard, 75015 Paris
- Doc type: Conditions générales (individual contract), 32 PDF pages, printed as 28 numbered pages
- URL: https://www.linxea.com/assets/uploads/2020/08/Nouvelle-CG-Spirit-2-1-1.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Page footer code "CG4445 - 01/07/2024".
- Content: the broker/online segment. Entry charges nil; UC management charge **0.125% deducted
  at the end of each quarter by reducing the number of units, i.e. 0.50% p.a.**; euro fund
  (Fonds Euro Nouvelle Génération) 2% p.a. maximum; Croissance Allocation Long Terme 1% p.a.
  plus a performance fee of at most 10% of positive fund performance; a 0.60% bid/offer spread
  on `Actions` supports and 0.10% on ETF supports applied by the insurer to the closing price;
  `gestion pilotée` an extra 0.05%–0.175% per quarter (0.2%–0.70% p.a.) by profile; arbitrages
  free online, two free per year on paper then 15 € per operation; the programmed-arbitrage
  options are free. Article 11.2 defines four programmed arbitrage options with their trigger
  parameters (see §9). Annexe I "Garantie de prévoyance (option)" carries the optional
  `garantie décès plancher`: entry ages > 12 and < 75, at subscription only; guaranteed capital
  = net premiums less rachats, avances and unpaid interest; `capital sous risque` capped at
  300,000 €; weekly (Friday) premium `Pr = K × (PA / 10 000) × 1/52`; a published annual tariff
  per 10,000 € of capital sous risque for ages 12–74; monthly levy in arrears on the last day of
  the month, first from the euro fund then from the largest UC support by cancelling units, with
  a 20 €/month deferral threshold; exclusions; cancellation rules; the guarantee ends at the 75th
  birthday. Article 17.1.2 states that where the plancher is taken there are **no minimum
  surrender values expressed in euros** and the plancher deductions are capped neither in euros
  nor in units. Annexe II sets out the tax and `prélèvements sociaux` treatment (see §11).

### S5 — Spirica, "LINXEA Spirit 2 — Document d'Informations Clés" (published 01/07/2026)
- Publisher: Spirica (ACPR register no. 1021306)
- Doc type: PRIIPs `document d'informations clés` (KID) for a multi-option product, 4 pp.
- URL: https://www.linxea.com/document/linxea-spirit-2-kid/
- Retrieved: YES (PDF downloaded, full text extracted). "Date de publication : 01/07/2026".
- Content: a current MOP KID. Warning "Vous êtes sur le point d'acheter un produit qui n'est pas
  simple"; risk indicator given as a **range**, "entre les classes de risque 1 et 7 sur 7",
  because the product's risk depends on the supports chosen; recommended holding period 8 years;
  30-day `renonciation`; FGAP protection 70,000 € per insurer per person for capital and 90,000 €
  for annuities in payment (art. L. 423-1 Code des assurances); cost tables expressed as ranges —
  total costs 50.25 €–1,668.95 € if exiting after 1 year and 404.84 €–30,028.49 € after 8 years
  on a 10,000 € investment, annual cost impact 0.50%–16.69% (1 yr) and 0.51%–8.77% (8 yr);
  composition of costs after 8 years: entry 0.00%–0.84%, exit 0.00%–1.35%, management and other
  administrative/operating 0.50%–4.43%, portfolio transaction 0.00%–7.43%, performance fees
  0.00%–4.63%. Confirms the optional `garantie décès plancher` and states the Croissance
  Allocation Long Terme engagement carries an 80% capital guarantee at maturity.

### S6 — Spirica, "Annexe — Les frais de l'assurance-vie — LINXEA Spirit 2" (transparence des frais table)
- Publisher: Spirica
- Doc type: the standardised fee-transparency annex published under the arrêté du 24 février 2022
  [R9], 2 pp.
- URL: https://www.spirica.fr/wp-content/uploads/2022/05/Frais-transparence-Linxea-Spirit-2.pdf
- Retrieved: YES (PDF downloaded, full text extracted). No edition date printed; the table is
  stated to reflect "le dernier exercice clos".
- Content: minimum initial premium 500 €; contract charges — euro fund 2.00% max, UC 0.50% max,
  Croissance Allocation Long Terme 1.00% max, `gestion pilotée ou standardisée` 0.70% max;
  **average ongoing charges of the underlying UC funds** in `gestion libre` — equity funds
  (including ETF, excluding private equity and direct equities) 1.87% of which 0.80% retroceded,
  bond funds 1.18% (0.53% retroceded), diversified funds 1.90% (0.80%), FCPR/other unlisted funds
  3.17% (0.78%), real-estate funds (OPCI, SCPI, SCI) 1.12% (0.28%); managed profiles — Montségur
  1.87%–1.90%, Yomoni 0.04%–0.13% (near-zero because the profiles use trackers); performance fee
  on the Croissance fund 10% max; `frais sur versement` 0.00%; change of management mode 0%
  online / 15 € paper; arbitrage 0% online / 15 € paper with 2 free paper arbitrages a year;
  outward transfer 0%; annuity instalment charge 0%; surrender charge 0%.

### S7 — Suravenir, "LINXEA AVENIR 2 — Conditions Contractuelles / Proposition d'assurances valant Note d'information" (avril 2022, contrat individuel multisupports n° 2259)
- Publisher: Suravenir (Crédit Mutuel Arkéa), 232 rue Général Paulet, BP 103, 29802 Brest
- Doc type: Conditions contractuelles valant note d'information, 58 pp. (18 numbered pages plus
  the supports annex)
- URL: https://www.linxea.com/document/linxea-avenir-2-conditions-generales/
- Retrieved: YES (PDF downloaded, full text extracted). "Avril 2022".
- Content: a structurally different design of the floor benefit. Entry charges 0.00% in both the
  `gestion libre` and `mandat d'arbitrage` compartments; annual management charges 0.60% on the
  euro fund Suravenir Rendement 2, 3.00% max on Suravenir Opportunités 2, 0.60% on UC in
  `gestion libre`, and 0.60% euro / 0.80% UC in the `mandat d'arbitrage` compartment; charges are
  **computed daily on the daily balance** and levied in units and/or euros — for the euro funds
  once a year at the annual revalorisation, for UC **every month** by cancelling units; annuity
  instalment charge 3%; `remise de titres` 1%; ETF transactions 0.1% of amounts invested or
  disinvested; and "cotisations mensuelles de la garantie complémentaire optionnelle en cas de
  décès : de 0,15 ‰ à 5,15 ‰ des capitaux sous risque en fonction de l'âge". The optional death
  cover: subscription at outset only, ages 12 to under 70, **a one-year `délai de carence`
  (waiting period)** so cover starts at the end of year 1, no medical formalities; it pays the
  `capital sous risque`, defined as the positive difference between cumulative net premiums less
  rachats and unrepaid `avances` with their interest, and the surrender value at the date the
  death certificate is received; capped at **100,000 € per LINXEA Avenir 2 contract**; a long
  exclusion list (suicide in year 1, drugs, intentional acts, drink-driving, unlawful activities,
  aviation, air sports, high-risk sports, motor competition, war/riot, active participation in
  terrorism, nuclear events); it ends at the 75th birthday, on total surrender, annuity
  conversion or renonciation. The premium is computed at each month end from the policyholder's
  age and a **published monthly tariff per 1,000 € of capital sous risque** (ages "jusqu'à 30" to
  75), and the sum of monthly premiums is levied at the latest on 31 December each year or on
  total exit. Where the cover is in force **the euro funds carry no minimum guaranteed surrender
  value**, and the contract instead prints three worked examples under art. A. 132-4-1 of the
  Code des assurances. Worked UC arithmetic is printed: 100 units net of charges become
  100 × (1 − 0.60%) = 99.4000 in `gestion libre` and 100 × (1 − 0.80%) = 99.2000 under
  `mandat d'arbitrage` after one year. Minimum premiums: 100 € initial (100 € gestion libre /
  1,000 € mandat), 100 € for `versements libres` with 25 € per support, 25 € per
  `versement programmé`. Arbitrages: minimum 100 €, minimum 100 € remaining on any support
  partially switched, and arbitrages out of a euro fund or a real-estate UC may exceptionally be
  deferred for up to six months. Five programmed-arbitrage options with their parameters (§9).

### S8 — Suravenir, "LINXEA AVENIR 2 — Transparence de frais" (réf. TR_SURA_4E25_TUCFR)
- Publisher: Suravenir
- Doc type: the standardised fee-transparency table published under the arrêté du 24 février 2022
  [R9], 2 pp.
- URL: https://www.suravenir.fr/wp-content/uploads/pdf/L8312_LINXEA-Avenir-2_LINXEA.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Reference TR_SURA_4E25_TUCFR.
- Content: minimum initial premium 100.00 €; contract charges — euro fund 3.00% max, UC 0.60%
  max, `gestion mandat d'arbitrage` +0.20%; average ongoing charges of the underlying UC funds in
  `gestion libre` — equity funds (incl. ETF) 1.23% (0.34% retroceded), bond funds 1.59% (0.49%),
  real-estate funds (OPCI/SCPI/SCI) 2.71% (0.62%), diversified funds 2.41% (0.61%), private
  equity 0.98% (0.97%), structured funds 0.00% (0.00%); `mandat d'arbitrage` funds 2.39% (0.75%);
  `frais sur versement` 0.00%; annuity instalment charge 3.00%; arbitrage charge N/A.

### S9 — Suravenir, "Demande d'opération(s) : Stop-loss relatif" (réf. 5461 R, 06/2022)
- Publisher: Suravenir
- Doc type: option election form with the contractual definition of the option, 3 pp.
- URL: https://www.linxea.com/document/linxea-avenir-1-2-stop-loss/
- Retrieved: YES (PDF downloaded, full text extracted). Réf : 5461 R (06/2022).
- Content: the trailing stop-loss definition: when the net capital invested on a chosen source
  support reaches the loss threshold set by the policyholder, the **whole** of that capital is
  switched to one or two destination supports; the loss is measured as the difference between the
  support's capital value on the observation date and **the highest capital value reached since
  the option was set up**; minimum threshold 5%. Source supports must be drawn from those graded
  "D" in the Stop-loss column of the contract's supports annex.

### S10 — MACSF épargne retraite, "Notice d'information — RES MULTISUPPORT" (1610201Y)
- Publisher: MACSF épargne retraite (insurer), Association AMAP (souscripteur)
- Doc type: Notice d'information for a group contract with individual optional membership, 27 pp.
- URL: https://www.macsf.fr/content/download/4098/fichier/MACSF_1610201Y_Notice_information_RES_Multisupport.pdf
- Retrieved: YES (PDF downloaded, full text extracted). InDesign metadata dates the file
  2024-10-23; the printed reference is 1610201Y.
- Content: the mutual/affinity segment, and the clearest example of a **non-optional plancher
  financed inside the management charge**. Entry charges 3% max on the euro fund and 1% max
  (0.6% by direct debit) on UC; management charge 0.50% (0.45% above 450,000 € of net cumulative
  premiums) levied on 31 December, **of which 0.20% is allocated to the garantie plancher up to
  age 70**; a further explicit plancher `cotisation` of 0.10% on UC levied on 31 December until
  and including the year of the 70th birthday; arbitrage 2% max towards the euro fund and 0.20%
  max towards UC with the first twelve of the year free, automatic arbitrages free; surrender and
  arbitrage penalties of 3% on SCPI and unlisted private-debt UC within three years of investment
  and ten years of membership, and 5% in the cases provided by art. R. 132-5-3; membership fee
  10 € (20 € joint). ART 10 defines the plancher: automatic to the day of the 70th birthday,
  paying at least the total of premiums net of entry charges since membership less partial
  surrenders and outstanding advances, on death **or on IFTD** (`Invalidité Fonctionnelle Totale
  et Définitive`, 3rd-category Social Security invalidity, surrender to be requested within one
  year of the invalidity); capped at **762,245 € of net premiums across all MACSF UC contracts**;
  granted to 31 December of the membership year and tacitly renewed annually; on joint membership
  the age condition applies to the younger life and the guarantee only bites on the death/IFTD
  that ends the contract; the tariff may be revised by agreement between the souscripteur and the
  insurer if the group's demographics or the guarantee's technical results change. ART 11–12 set
  out the `provision mathématique` and surrender-value recursions in units, with an 8-year table
  (100 units gross, 99 after the 1% entry charge) falling 98.41 → 97.82 → … → 94.35 before age 70
  and 98.51 → 98.01 → … → 95.11 after 70 — exactly a 0.60% and 0.50% annual unit decrement. ART 9
  reproduces the statutory warning that the insurer commits only to the number of units. Maximum
  age at membership 85 (ART 4B). ART 19 names the tax articles: CGI 125-0 A on surrender, 757 B
  and 990 I on death, 158-6 on annuities, and exemption from `taxe d'assurance` under CGI 995.

### S11 — Afer, "Contrat collectif d'assurance vie multisupport Afer — Notice" (60121-1021, édition octobre 2021)
- Publisher: Association Afer (souscripteur); co-insurers Aviva Vie and Aviva Épargne Retraite,
  with Aviva Vie as lead co-insurer; GIE Afer as manager
- Doc type: Notice d'information for a group contract, 53 pp. including five annexes
- URL: https://www.afer.fr/content/uploads/2022/02/60121-1021-notice-contrat-collectif-assurance-vie-multisupport-afer.pdf
- Retrieved: YES (PDF downloaded, full text extracted). "NOTICE : ÉDITION OCTOBRE 2021".
- Content: the largest French association contract, and the only retrieved document containing a
  formal **`note technique` on the garantie plancher** (Annexe 3). Entry charges 0.5% on premiums
  allocated to the euro fund and **nil on UC and on the eurocroissance support**; management
  charges 0.475% p.a. on the euro fund and on UC, 0.89% p.a. on the eurocroissance engagement;
  **no arbitrage charges at all** between supports of the same membership; annual cost of the
  garantie plancher 0.055% of the savings invested in UC or eurocroissance; membership fee 20 €;
  minimum premium by cheque 100 €. The plancher is **non-optional** and applies to death before
  the 75th birthday. Annexe 3 defines the benefit per support as
  `max(épargne investie A, épargne constituée B)` where A = number of units × the
  `prix de revient unitaire moyen` (PRUM, the running average unit cost price) and B = number of
  units × the current liquidation value; the PRUM is recomputed at every investment
  (premium, incoming arbitrage or reinvested distribution) as a units-weighted average, and a
  four-row worked example is printed (500 units at 20.00 €, then 2,000 units at 21.00 € giving a
  PRUM of 20.80 €, a surrender of 198 units leaving the PRUM unchanged, then a distribution of
  50 units at 22.50 € giving 20.84 €), with the guarantee and the account value shown side by
  side at each step. Valuation uses the Wednesday liquidation value following receipt of the
  death certificate. The 0.055% cost is **mutualised across all members, is age-independent**,
  and for UC is computed monthly and deducted from distributed dividends; for the eurocroissance
  support it is computed weekly and deducted from the diversification-provision unit value.
  Total surrender ends the plancher, and it does not apply during the 30-day renonciation period.
  Annexe 4 gives worked examples of the two automatic arbitrage options
  (`Sécurisation des Performances`, `Dynamisation des Intérêts`) — see §9.

### S12 — SAF BTP VIE (PRO BTP), "Document d'informations clés générique — contrat Multisupport CONFIANCE" (13 mai 2025)
- Publisher: Société d'Assurances Familiales des Salariés et Artisans Vie (SAF BTP VIE), groupe
  PRO BTP
- Doc type: PRIIPs `document d'informations clés` (generic MOP KID), 4 pp.
- URL: https://www.probtp.com/files/live/sites/probtp/files/media/pdf/epargne/dici/dic_generique_contrat_multisupport_confiance.pdf
- Retrieved: YES (PDF downloaded, full text extracted). "Date de production du document : 13 mai 2025".
- Content: a generic KID for a group multisupport contract with three management modes
  (`Gestion Libre`, `Gestion à Horizon`, `Gestion Pilotée Profilée`). SRI presented as a range,
  "classe de risque 1 à 5 sur 7". The death benefit is described as a `garantie plancher` that
  bites if death occurs before the insured's 80th birthday, renewable annually at the insurer's
  discretion, paying the greater of the account value across all supports and the cumulative
  **gross** premiums less the capital component of any partial surrenders, **revalorised annually
  at a rate set by the insurer** — an indexed floor whose index is discretionary. Cost tables
  (per 10,000 € invested): total costs 73 €–648 € if exiting after 1 year and 724 €–4,553 € after
  8 years, corresponding to a reduction in yield of 0.7%–6.5% and 0.7%–3.7% respectively (the
  extracted PDF text transposes the two row labels; the € and % figures are consistent only in
  this reading); entry costs 0.00%–0.7%, exit costs 0.00%, portfolio transaction costs 0.0%–1.2%,
  other recurring costs 0.7%–2.1%, performance fees 0.00%. FGAP cover 70,000 € per member per
  insurer. Initial term 8 years, tacitly renewed; recommended holding period 8 years; 30-day
  renonciation; free surrender at any time; annuity conversion before the 75th birthday with a
  3% charge on each annuity instalment.

### S13 — SAF BTP VIE (PRO BTP), "Notice d'information résumant les conditions générales — contrat Multisupport CONFIANCE"
- Publisher: SAF BTP VIE
- Doc type: Notice d'information, 81 pp.
- URL: https://www.probtp.com/files/live/sites/probtp/files/media/pdf/epargne/notice-info-cg-multisupport-confiance.pdf
- Retrieved: YES (PDF downloaded, full text extracted). No edition code in the extracted text.
- Content: the contractual detail behind [S12]. Entry charges nil, premium charges set by the
  insurer up to 3%; **0.75% max p.a. on the euro-denominated rights and 0.80% max p.a. on the
  UC rights "au titre de la gestion du contrat et du financement de la garantie plancher"** —
  i.e. the floor benefit is financed inside a single UC charge; `Gestion Pilotée Profilée` an
  extra 0.30% max p.a. on both UC and euro; exit 3% on annuity instalments, nil on surrender;
  arbitrage 0.5% of the amount switched in `Gestion libre` with the first three of the year and
  all `investissement progressif` arbitrages free, and free in the two managed modes. Article
  8.2 states the plancher pays `max(épargne constituée, cumulative gross premiums less the
  capital component of partial surrenders, revalorised annually at a rate set by the insurer)`,
  less any unrepaid advances, on death before the 80th birthday. Article 32.4 is the operative
  charging clause: the UC charge "ne peut dépasser 0,80 % par an de l'épargne constituée sur
  chaque support en unités de compte", includes the plancher financing, **is no longer levied
  beyond the 80th birthday**, is computed on the number of units held at the end of each calendar
  month, is levied at the next valuation date, and reduces the number of units held. Article 32.2
  sets unit conversion to four decimal places (`au dix millième`); article 32.3 reinvests all
  distributed income in the support; article 32.6 caps real-estate UC at 60% of each transaction.
  Article 33 caps advances on UC at 60% of the UC savings, with a rate reset quarterly at at
  least TME + 1%. Article 19 requires an annual statement showing the number of units held per
  support, and annual notice of whether the plancher has been renewed or revoked.

### S14 — BNP Paribas Cardif, key-information document portal
- Publisher: BNP Paribas Cardif
- Doc type: document portal (index page)
- URL: https://document-information-cle.cardif.fr/cgpi
- Retrieved: NO — page shell only; the contract list and DIC download links are rendered
  client-side and were not returned. Known reference only; no Cardif figure is cited anywhere in
  these notes.

---

## Regulatory and actuarial references

### R1 — Code des assurances, article L. 131-1
- Publisher: Légifrance (Direction de l'information légale et administrative)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611256
- Retrieved: YES (article page; version in force since 24 May 2019, as amended by loi n° 2019-486
  du 22 mai 2019 (loi PACTE) art. 72).
- Content: the founding article for unit-linked life insurance. In life insurance and
  capitalisation operations the guaranteed capital or annuity **may be expressed in
  `unités de compte` made up of securities or assets offering sufficient protection of the
  invested savings and appearing on a list drawn up by decree in Conseil d'État** (the list is
  R. 131-1 [R3]). Settlement is in cash, but delivery of the underlying securities or units is
  permitted in three cases: (1) securities traded on a regulated market, (2) non-regulated
  securities where the policyholder's election is irrevocable and the insurer agrees, and (3)
  units of alternative investment funds on the same terms. Delivery is barred where the
  securities confer voting rights, or where the policyholder and connected persons have held
  more than 10% of the issuer in the preceding five years; the 10% test applies to surrender
  requests made after the law's entry into force. **The much-quoted principle that the insurer
  commits only to the number of units and not to their value is not stated in L. 131-1 itself —
  it is imposed as a disclosure obligation by A. 132-5 [R2]** and is reproduced verbatim in the
  contracts [S4][S7][S10][S13].

### R2 — Code des assurances, article A. 132-5
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006786185
- Retrieved: YES (article page; version in force since 2 May 2007).
- Content: for contracts referred to in the second paragraph of L. 131-1, the information
  document must state that the insurer "ne s'engage que sur le nombre d'unités de compte, mais
  pas sur leur valeur", and that the value of those units, which reflects the value of underlying
  assets, is not guaranteed but is subject to upward and downward fluctuations depending in
  particular on financial-market movements. This is the source of the boxed warning that appears
  in every retrieved contract [S1][S3][S4][S7][S10][S13].

### R3 — Code des assurances, article R. 131-1
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043560691
- Retrieved: YES (article page; the version served was in force from 6 May 2026, as amended by
  décret n° 2026-341 du 30 avril 2026 art. 1).
- Content: the eligibility list for UC. It admits the asset classes enumerated in article
  R. 332-2 [R4] (points 1°, 2° a) and c), 2° bis, 2° ter, 3°, 4°, 5° and 8°), and, under
  conditions set by R. 131-2 to R. 131-4, the units or shares of point 9° bis (real-estate
  vehicles); it further admits collective-investment units, commercial-company shares,
  alternative-fund units, employee-savings fund units and associative/foundation securities on
  stated conditions. Part II imposes **concentration limits per unit type** — commercial-company
  shares capped at 10% of the contract's commitments and a 30% aggregate threshold for combined
  alternative investments. Part III requires the contract to provide a substitution mechanism
  when a unit ceases to be available. Note: the fetched summary paraphrases the enumerations; the
  precise wording of each limb of Part II was not extracted verbatim, so any use of an individual
  percentage from this article should be re-checked against the article text.

### R4 — Code des assurances, article R. 332-2
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037635496
- Retrieved: YES (article page; version dated 22 November 2018).
- Content: the master list of assets admitted in representation of regulated commitments, which
  R. 131-1 [R3] borrows to define UC eligibility. 1° bonds and securities issued or guaranteed by
  OECD states; 2° securities traded on recognised markets including corporate bonds, financing
  vehicles' instruments and `titres participatifs`; 2° bis and 2° ter negotiable short- and
  medium-term debt securities; 2° quater financing-vehicle obligations and shares; 3° SICAV
  shares and FCP (mutual fund) units limited to portfolios of the listed securities; 4° shares
  and securities traded on recognised markets; 5° and 5° bis insurance, reinsurance and
  capitalisation company shares; 8° investment-company shares and mutual-fund units on stated
  conditions; 9° bis units or shares of strictly real-estate companies and land vehicles in the
  OECD. Practical effect: OPCVM/FCP/SICAV, ETF (which are OPC), equities, bonds and structured
  debt come in through 2°/3°/4°/8°, and SCPI/OPCI/SCI come in through 9° bis subject to the
  R. 131-2 to R. 131-4 conditions.

### R5 — Code des assurances, article L. 131-1-1
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038507517
- Retrieved: YES (article page; version in force 24 October 2024, as amended by loi n° 2023-973 du
  23 octobre 2023 (loi Industrie verte) art. 35 V).
- Content: permits UC composed of alternative investment fund (FIA) and financing-vehicle units,
  subject to conditions relating in particular to the policyholder's financial situation,
  financial knowledge or experience. Funds designated as ELTIFs marketed to retail investors are
  exempt from those conditions, as are contracts under an arbitrage mandate (`gestion sous
  mandat`). This is the gate through which private-equity and private-debt UC — the FCPR/FPCI
  supports charged at 3.17% in [S6] and 0.98% in [S8] — reach retail multisupport contracts.

### R6 — Code des assurances, article L. 131-1-2
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049720147
- Retrieved: YES (article page; in force 1 January 2025, as amended by loi n° 2024-537 du 13 juin
  2024 (loi Industrie verte financement) art. 3).
- Content: a multisupport contract must reference **at least one UC composed of between 5% and
  15% of securities issued by** social-and-solidarity-economy undertakings (art. L. 3332-17-1 du
  Code du travail), venture-capital companies (loi n° 85-695 du 11 juillet 1985) or risk-focused
  or specialised professional funds (art. L. 214-28 or L. 214-154 du Code monétaire et
  financier); and, for each State-recognised label in energy/ecological transition financing or
  socially responsible investment, **at least one UC carrying that label**. The proportion of the
  contract's units meeting these conditions must be disclosed before conclusion or membership.
  It does not apply to contracts tied to cessation of professional activity.

### R7 — Code des assurances, chapitre R. 131-1 à R. 131-12 (unit-linked contracts)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000006158245/
- Retrieved: YES (chapter listing plus targeted reading of R. 131-8 to R. 131-12).
- Content: the operational plumbing of UC. R. 131-1-1/R. 131-1-2/D. 131-1-3/R. 131-1-4 govern
  professional and specialised funds and the assessment of investor competence; D. 131-1-5 lists
  the approved sustainability labels for R. 131-1-2 purposes [R6]; R. 131-2 to R. 131-6 govern
  unlisted real-estate vehicles (valuation, portfolio composition, substitution, liquidity,
  settlement); R. 131-7 requires the insurer's portfolio to match an indexed guarantee's
  reference composition. **R. 131-8 to R. 131-12 are the gating rules**: when the manager of a
  fund used as a UC suspends or restricts redemptions, the restriction applies only to requests
  made after the fund's last order centralisation before suspension; unexecuted requests roll to
  the next centralisation if the fund values daily or more often, and are otherwise cancelled;
  the insurer may not apply a liquidation value lower than the last published value; any
  proportional restriction the insurer applies must be at least as favourable as the fund's own;
  the policyholder must be informed without delay on a durable medium and given a full account of
  the measure's effects; R. 131-10 lists the information that must be kept accessible (units
  affected, description and estimated duration, deferral/revocation procedures, settlement terms)
  and makes the measures unenforceable against a client who was not advised of them; R. 131-11
  requires notification to the ACPR with supporting justification; R. 131-12 allows estimated
  values, updated and disclosed quarterly, where no current liquidation value exists.

### R8 — Code de la sécurité sociale, article L. 136-7 (CSG on `produits de placement`)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288474/2023-03-11
- Retrieved: YES (article page; version served dated 11 March 2023).
- Content: the article that produces the euro-versus-UC asymmetry. Under II, 3°, a) the levy
  applies **"lors de leur inscription au bon ou contrat"** — i.e. annually as interest is
  credited — for contracts whose rights are expressed in euros or foreign currency, **and for
  the euro-denominated component of a multisupport contract**. Under II, 3°, b) it applies when
  a guarantee is reached, for guaranteed components. Under II, 3°, c) it applies **"lors du
  dénouement des bons ou contrats ou lors du décès de l'assuré"** for everything not already
  taxed under a) or b) — which is the unit-linked component. III bis provides for the restitution
  of an `excédent` where the contract's final liquidation produces a negative base, limited to
  the contributions already levied under a) and b), by set-off or reimbursement at settlement.

### R9 — Arrêté du 24 février 2022 portant renforcement de la transparence sur les frais du plan d'épargne retraite et de l'assurance-vie
- Publisher: Journal officiel / Légifrance (JORFTEXT000045299785)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045299785
- Retrieved: YES (consolidated text page).
- Content: amends **article A. 522-1 du Code des assurances** to add disclosure of "total fees,
  expressed as a percentage, being the sum of management fees and recurring fees", with a
  three-month transitional allowance to use the prior year's data. Annex 1 prescribes the
  standardised per-UC table with columns: ISIN code, name, management company, gross performance
  of the support for year N−1, the support's own management fees, the support's net performance,
  the contract's management fees, **total fees**, final performance, and the commission
  retrocession rate. Article 5 sets entry into force at 1 July 2022 for the general provisions
  and 1 January 2023 for the annual-information requirements. The tables in [S6] and [S8] are
  instances of this regime.

### R10 — Loi n° 2014-617 du 13 juin 2014 relative aux comptes bancaires inactifs et aux contrats d'assurance vie en déshérence ("loi Eckert")
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000029095362
- Retrieved: YES (consolidated text page). Entry into force 1 January 2016.
- Content: the unclaimed-contracts regime. Insurers must search for deceased insureds against the
  RNIPP via a professional body (AGIRA) and settle within the statutory deadlines. Amends or
  creates Code des assurances articles L. 132-5 (post-mortem revalorisation [R11]), L. 132-9-3
  and L. 132-9-3-1 (the annual death-matching duty and beneficiary search), L. 132-22 and
  L. 132-23-1 (information and settlement deadlines [R12]), and L. 132-27-2 (deposit with the
  Caisse des dépôts). Unclaimed sums are deposited with the Caisse des dépôts et consignations
  ten years after the insurer learns of the death and are acquired by the State if still
  unclaimed twenty years later; the Caisse publishes an annual report. Note: the fetched summary
  renders the two periods as "10–30 years" and "30+ years"; the ten-plus-twenty reading is
  confirmed independently by [S11], which states deposit after ten years and escheat after a
  further twenty. Insurers must also publish an annual report on their search actions and the
  number and amount of unsettled contracts [unverified — stated in secondary summaries, not read
  in the statute text].

### R11 — Code des assurances, article L. 132-5 (post-mortem revalorisation)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029098941
- Retrieved: YES (article page; in force since 1 January 2016, as amended by loi n° 2014-617
  [R10]).
- Content: for contracts with a surrender value and for death covers with natural-person
  beneficiaries, the capital must be revalorised **from the date of the insured's death until
  receipt of the documents referred to in L. 132-23-1, or where applicable until deposit with the
  Caisse des dépôts under L. 132-27-2**, at a rate that may not be lower than a rate fixed by
  decree in Conseil d'État. The decree's numerical rate was not exposed in the fetched article
  text — treat the actual percentage as [unverified].

### R12 — Code des assurances, article L. 132-23-1 (settlement deadline and late interest)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000017841432/2013-07-28
- Retrieved: YES — but the URL is date-pinned and served the **19 December 2007 to 1 January 2016
  version**, i.e. the text as it stood before the loi Eckert amendments [R10].
- Content (as at the retrieved version): the insurer must pay the guaranteed capital or annuity
  within one month of receiving the documents necessary for payment following the insured's death
  or the contract's term; beyond that deadline the unpaid capital automatically bears interest at
  **the legal rate increased by one half for two months, then at double the legal rate**. The
  current (post-2016) wording, including the fifteen-day period for requesting documents, was not
  retrieved — treat any post-2016 detail as [unverified].

### R13 — France Assureurs, "L'assurance vie en unités de compte — Année 2025"
- Publisher: France Assureurs (the French insurance trade body)
- URL: https://www.franceassureurs.fr/wp-content/uploads/2025_assurance-vie-en-uc.pdf
- Retrieved: YES (PDF downloaded, full text extracted), 16 pp.
- Content: the market benchmark for UC. 2025 UC premiums 75.1 bn € (+13.2%), 39.1% of all
  life premiums; UC benefits paid 32.6 bn € (−1.5%); UC net inflow +42.5 bn €, the highest on
  record, within a total net inflow of +50.6 bn €; euro-to-UC transfers +2.7 bn € of which
  +1.2 bn € arbitrages; estimated net UC asset acquisition 55.1 bn €. Year-end 2025 UC
  `provisions mathématiques` 666.4 bn € (+13.5%), against 684.5 bn € of UC-backing investments.
  Asset breakdown: 567 bn € financing companies (~83% of UC investments) — 372 bn € equities,
  171 bn € bonds, 24 bn € commercial property; 252 bn € to French companies. 2025 overall UC
  performance +5.5% (gross of contract charges, net of fund charges); five-year average fund
  performance net of fund charges +4.9%. **Charges: the encours-weighted average of UC funds'
  recurring costs is 1.60% (down 2 bp), and the average contract charge on UC is 0.88%** —
  0.82% for `gestion libre` or predefined allocations without extra charges (441.6 bn € of
  provisions) and 1.17% for `gestion sous mandat`, standardised or piloted with extra charges
  (93.0 bn €); the euro-fund contract charge averages 0.66% and the all-in average 0.73%. The
  2024 comparatives are 0.83% / 1.19% / 0.88% / 0.66% / 0.73%.

### R14 — France Assureurs, "L'assurance vie en unités de compte en 2025" (chiffres clés page)
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/assurance-vie-unite-de-compte-2025/
- Retrieved: YES (web page).
- Content: the headline page for [R13]; the figures cited above were cross-checked against it.
  It additionally frames the UC share of total assurance vie `encours` at 32% at end-2025,
  13 points above 2005, against 68% for euro supports.

### R15 — AMF, Position-recommandation DOC-2011-05, "Guide des documents réglementaires des OPC" (created 18 February 2011, amended 16 February 2023)
- Publisher: Autorité des marchés financiers
- URL: https://www.amf-france.org/sites/institutionnel/files/private/2023-02/DOC-2011-05_VF14_PRIIPs.pdf
- Retrieved: YES (PDF downloaded, full text extracted), 44 pp.
- Content: the AMF's doctrine on the regulatory documents of collective investment schemes —
  the documents that describe the funds used as UC supports. Its `textes de référence` are
  article 78 of Directive 2009/65/EC, Regulation 583/2010, **Regulation (EU) No 1286/2014
  (PRIIPs) and Commission Delegated Regulation (EU) 2017/653**, and articles 411-106 to 411-120
  and 422-67 to 422-78 of the AMF General Regulation. It covers the DICI/DIC sections
  (objective, investment policy, risk and return profile, charges, past performance, practical
  information) and the specifics for FCPR/FCPI/FIP and OPCI. It is the retrievable anchor for the
  PRIIPs citation chain, since EUR-Lex itself could not be fetched (see [R17], [R18]).

### R16 — AMF, "Comprendre le document d'informations clés (DIC)" (guide pédagogique)
- Publisher: Autorité des marchés financiers
- URL: https://www.amf-france.org/sites/institutionnel/files/contenu_simple/guide/guide_pedagogique/Comprendre%20le%20document%20d'informations%20cles%20(DIC).pdf
- Retrieved: YES (PDF downloaded, full text extracted), 16 pp.
- Content: the AMF's retail guide to the DIC. The DIC is a European standardised document of
  two to three pages at most, precontractual, to be delivered a reasonable time before
  subscription, clear, accurate and not misleading, and expressly not a marketing document. It
  applies to SCPI, to collective investments (FCP, SICAV, SCPI) whether held through a PEA, a
  securities account, employee savings **or a unit-linked life insurance or capitalisation
  contract**, and to structured debt securities. Caveat: this edition still refers to the DICI /
  DIC transition ending in December 2019 and therefore predates the 2023 extension of the DIC to
  UCITS; the SRI scale and current performance-scenario rules are not described in it.

### R17 — Regulation (EU) No 1286/2014 (PRIIPs)
- Publisher: European Union / EUR-Lex
- URL: https://eur-lex.europa.eu/eli/reg/2014/1286/oj/eng
- Retrieved: NO — EUR-Lex returned an empty body to both the remote fetcher and a browser-UA
  download (HTML and PDF endpoints both returned zero bytes). Known reference only. Its
  existence, its application to insurance-based investment products and its status as the source
  of the `document d'informations clés` are confirmed indirectly by [R15] (which cites it as a
  `texte de référence`) and by the DIC documents themselves [S5][S12]. **No article number from
  this Regulation is asserted anywhere in these notes.**

### R18 — Commission Delegated Regulation (EU) 2017/653 (PRIIPs RTS)
- Publisher: European Union / EUR-Lex
- URL: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32017R0653
- Retrieved: NO — same failure mode as [R17]. Known reference only; cited as a `texte de
  référence` by [R15]. The SRI 1–7 scale, the performance-scenario set and the cost-composition
  table are described in these notes **only from the DIC documents that implement them**
  [S5][S12], never from the RTS text. Any statement about the MRM/CRM methodology, the four
  performance scenarios or the reduction-in-yield formula is [unverified] here.

---

## Extracted specifications

### 1. Contract structure — what a `contrat multisupport` is
- A single life insurance contract whose savings are split, at the policyholder's election,
  between a `fonds en euros` (capital-guaranteed, insurer's general account) and one or more
  `supports en unités de compte` (market risk borne by the policyholder), with free switching
  (`arbitrage`) between them [S1][S3][S4][S7][S10][S12][S13]. Some contracts add a third leg,
  `eurocroissance` engagements giving rise to a `provision de diversification` [S2][S4][S11].
- Legal forms observed: **individual contract** (`contrat d'assurance sur la vie individuel`) —
  Himalia [S1], LINXEA Spirit 2 [S4], LINXEA Avenir 2 (n° 2259) [S7]; **group contract with
  individual optional membership** (`contrat collectif à adhésion facultative`) — Bourso Vie
  (souscripteur Boursorama) [S3], RES Multisupport (souscripteur Association AMAP) [S10], Afer
  (souscripteur Association Afer) [S11], Multisupport CONFIANCE [S12][S13]. The group form
  matters for modelling only in that the tariff can be renegotiated between the `souscripteur`
  and the insurer — MACSF may revise the plancher rate "en cas de modification de la composition
  démographique du groupe et en fonction des résultats techniques de la garantie" [S10 ART 8.D].
- Benefits: a capital sum or annuity to the insured if alive at the term (where the contract has
  a fixed term), or to the designated `bénéficiaires` on death before term [S1][S4][S7][S13].
  Contracts are commonly written `viagère` (whole of life) by default with an option for a fixed
  term [S4 art. 4][S7]. Term ranges: Suravenir minimum 8 years, maximum 85 minus the
  policyholder's age [S7]; PRO BTP initial term 8 years, tacitly renewed annually [S12][S13].
- The contract is not cancellable unilaterally by the insurer, save for non-renewal beyond the
  initial term with two months' notice [S12][S13].

### 2. What a UC is legally — the number/value split
- Art. L. 131-1 al. 2 permits capital or annuities to be expressed in `unités de compte` made of
  securities or assets offering sufficient protection of the invested savings and appearing on a
  list set by decree in Conseil d'État [R1].
- The operative modelling rule is a **disclosure obligation**, art. A. 132-5: the notice must
  state that the insurer "ne s'engage que sur le nombre d'unités de compte, mais pas sur leur
  valeur", and that the unit value reflects underlying assets, is not guaranteed and fluctuates
  with markets [R2]. Every retrieved contract reproduces it, some in bold or in a box
  [S1][S3][S4 art. 17.1.1][S7][S10 ART 9.A][S13 art. 32.5].
- Consequence for the model: **the state variable is a unit count, not a euro amount.** All
  contract charges on UC are expressed as a percentage that is applied by cancelling units, so
  the unit count is a deterministic, market-independent decreasing sequence, and the euro account
  value is `units × NAV` [S1][S3][S4][S7][S13].
- Unit conversion precision: PRO BTP computes to four decimal places (`au dix millième`)
  [S13 art. 32.2]. Published surrender tables carry four to five decimals [S3 art. 21]
  [S4 art. 17][S7].
- Distributed income on a UC support is reinvested in that support and increases the unit count
  [S13 art. 32.3][S4]; Afer treats reinvested distributions as an "investissement" for PRUM
  purposes [S11 Annexe 3].
- Settlement is normally in cash; delivery of the underlying securities is possible in the three
  cases of L. 131-1, with the no-voting-rights and 10%-holding restrictions [R1]. Suravenir
  offers `remise de titres` on total surrender, death or term at a charge of 1% of the funds
  settled in securities [S7].

### 3. Eligible supports (`supports en unités de compte`)
- Statutory list: R. 131-1 [R3] admits the R. 332-2 [R4] classes — OECD sovereign bonds (1°),
  regulated-market securities and corporate debt (2°, 2° bis, 2° ter, 2° quater), SICAV shares
  and FCP units (3°, 8°), listed equities (4°), insurance-company shares (5°) — plus, on the
  conditions of R. 131-2 to R. 131-4, the real-estate vehicles of 9° bis. Concentration limits
  apply per unit type under R. 131-1 II (commercial-company shares capped at 10% of the
  contract's commitments, a 30% aggregate threshold for combined alternative investments)
  [R3 — percentages read from a paraphrased fetch; verify against the article before use].
- FIA and financing-vehicle units require a suitability gate on the policyholder's financial
  situation, knowledge or experience, unless the fund is a retail ELTIF or the contract is under
  an arbitrage mandate [R5].
- Mandatory offering: at least one UC holding 5%–15% of ESS/venture-capital securities, and at
  least one UC per State-recognised green or SRI label, with disclosure of the proportion of
  qualifying units before subscription [R6].
- Universes actually offered:
  - Bourso Vie: `OPC`, `OPC Indiciels (ETF)` and `Actions` (direct equities) [S3 art. 9].
  - Himalia: OPC, ETF, Actions, plus supports requiring a specific investment avenant such as
    SCPI, SCI, OPCI, complex financial instruments, bonds and FCPR [S1].
  - LINXEA Spirit 2: UC of all kinds plus `Actions` and `ETF` with their own bid/offer spreads,
    plus SCPI/SCI/SC, private equity and structured products via annexes [S4][S6].
  - LINXEA Avenir 2: "unités de compte obligataires, en actions, diversifiées, immobilières
    (SCI, SCP, SCPI ou OPCI), des produits structurés, des supports à fenêtre de
    commercialisation ou des unités de compte de toute nature" [S7].
  - MACSF: UC "de toute nature", with dedicated annexes for SCPI, private-debt vehicles (Tikehau
    Financement Entreprises, Andera Dette Privée) carrying their own valuation and penalty rules
    [S10 ART 9.A].
  - Afer: a limited menu of Afer-branded funds plus the Afer Eurocroissance support [S11].
- Real-estate concentration cap: PRO BTP caps real-estate UC at **60% of each premium or
  arbitrage** [S13 art. 32.6]. No equivalent cap appears in the other retrieved contracts.
- Substitution: if a support is delisted or disappears, the contract must provide for replacement
  by a like unit or by transfer to the default euro fund [R3 III][S7].
- Gating: where a fund suspends or restricts redemptions, R. 131-8 to R. 131-12 govern which
  requests are affected, the valuation floor (not below the last published value), automatic
  roll-forward or cancellation, the durable-medium notification, the ACPR notification and the
  use of estimated values with quarterly disclosure [R7]. Suravenir independently reserves the
  right to defer arbitrages out of a euro fund or a real-estate UC for up to six months [S7].

### 4. Contract charges on UC — levels and levy mechanics
Market averages (2025, encours-weighted, France Assureurs survey of individual assurance vie,
capitalisation and PER): **contract charge on UC 0.88%** — 0.82% in `gestion libre`, 1.17% under
`gestion sous mandat` — against 0.66% on euro supports and 0.73% overall; underlying UC funds'
recurring costs average **1.60%** [R13].

Contract-level UC management charges retrieved:

| Contract | UC management charge | Levy mechanics |
|---|---|---|
| Himalia (Generali) [S1] | 0.25%/quarter = **1.00% p.a.** max; 0.375%/quarter = 1.50% p.a. on ETF and Actions; +0.15%/quarter (0.60% p.a.) under gestion pilotée | quarterly, by reducing the number of units |
| Bourso Vie (Generali) [S3] | 0.1875%/quarter = **0.75% p.a.** max on OPC, ETF and Actions | quarterly, by reducing the number of units |
| LINXEA Spirit 2 (Spirica) [S4][S6] | 0.125%/quarter = **0.50% p.a.**; gestion pilotée +0.05% to +0.175%/quarter (0.2%–0.70% p.a.) | quarterly, by reducing the number of units |
| LINXEA Avenir 2 (Suravenir) [S7][S8] | **0.60% p.a.** gestion libre; **0.80% p.a.** under mandat d'arbitrage | accrued daily on the daily balance, levied **monthly** by cancelling units |
| RES Multisupport (MACSF) [S10] | **0.50% p.a.** (0.45% above 450,000 € of net premiums), of which 0.20% funds the plancher to age 70; **plus** a separate 0.10% plancher cotisation | annually on 31 December, prorated for units acquired or disinvested during the year |
| Afer [S11] | **0.475% p.a.** on UC and on the euro fund; plus 0.055% p.a. plancher cost | not stated for UC in the retrieved pages beyond "après valorisation"; the plancher element is computed monthly and deducted from distributed dividends |
| Multisupport CONFIANCE (PRO BTP) [S13] | **0.80% p.a.** max on UC **including** the plancher financing (0.75% on euro rights); Gestion Pilotée Profilée +0.30% p.a. on both | computed on the number of units at the end of each calendar month, levied at the next valuation date, reducing the number of units; not levied beyond the 80th birthday |

Worked unit decrements published by the insurers themselves (these are the arithmetic the model
must reproduce):
- Bourso Vie, 0.1875% per quarter: 100 → 99.2521 → 98.5098 → 97.7731 → 97.0418 → 96.3161 →
  95.5957 → 94.8808 → 94.1711 over eight years, i.e. an annual factor of
  `(1 − 0.001875)^4 = 0.9925208…` [S3 art. 21].
- Suravenir, 0.60% and 0.80% p.a.: 100 → 99.4000 and 100 → 99.2000 after one year [S7].
- MACSF, 99 units after a 1% entry charge: 98.41, 97.82, 97.23, 96.65, 96.07, 95.49, 94.92, 94.35
  before age 70 (annual factor 0.9940 = 1 − 0.50% − 0.10%) and 98.51, 98.01, 97.52, 97.03, 96.55,
  96.07, 95.59, 95.11 after age 70 (factor 0.9950) [S10 ART 12.A].
- Himalia, 0.25% per quarter: 99.0037 → 98.0174 → … (annual factor `(1 − 0.0025)^4 = 0.990037…`)
  [S2].

Other charges:
- `Frais sur versement` (premium charge): 4.50% max [S1]; nil [S3][S4][S6][S7][S8]; up to 3%
  set by insurer decision [S13]; 3% max on the euro fund and 1% max (0.6% by direct debit) on UC
  [S10]; 0.5% on premiums to the euro fund and **nil on UC** [S11].
- `Frais d'arbitrage`: 1% of the amount with a 30 € (post) / 15 € (online) minimum [S1]; nil
  online and 15 € per paper arbitrage after two free per year [S4][S6]; 2% max towards the euro
  fund and 0.20% max towards UC with the first twelve of the year free [S10]; nil in all cases
  [S11]; 0.5% in gestion libre with three free per year and free in managed modes [S13]; not
  applicable [S8].
- Automatic-arbitrage option charges: 0.50% of the amount transferred [S1]; 1% max on
  `sécurisation des plus-values` [S3]; free [S4][S13].
- Bid/offer spreads applied by the insurer: ±0.60% on `Actions`, ±0.10% on ETF [S4]; 0.1% on ETF
  transactions [S7].
- Exit charges on surrender or death: nil in every retrieved contract [S1][S3][S4][S7][S10][S11]
  [S13]. Annuity instalment charges: 3% [S7][S13]; nil [S6].
- Surrender/arbitrage penalties on illiquid UC: MACSF 3% on SCPI and private-debt UC disinvested
  within three years of investment and ten years of membership, and 5% in the cases of
  art. R. 132-5-3 [S10 ART 8.E].
- Fund-level ongoing charges (borne inside the UC, additional to the contract charge):

| Fund class | Spirica / LINXEA Spirit 2 [S6] | Suravenir / LINXEA Avenir 2 [S8] |
|---|---|---|
| Equity funds (incl. ETF) | 1.87% (0.80% retroceded) | 1.23% (0.34%) |
| Bond funds | 1.18% (0.53%) | 1.59% (0.49%) |
| Diversified funds | 1.90% (0.80%) | 2.41% (0.61%) |
| Real-estate funds (OPCI/SCPI/SCI) | 1.12% (0.28%) | 2.71% (0.62%) |
| Private equity / unlisted (FCPR, FPCI, FPS) | 3.17% (0.78%) | 0.98% (0.97%) |
| Structured funds | not broken out | 0.00% (0.00%) |
| Managed profiles | Montségur 1.87%–1.90%; Yomoni 0.04%–0.13% | mandat d'arbitrage 2.39% (0.75%) |

  Market-wide, the encours-weighted average is 1.60% [R13].
- These per-support and total-fee tables are published under the arrêté du 24 février 2022,
  which prescribes the ISIN / name / management company / gross performance N−1 / support fees /
  net performance / contract fees / **total fees** / final performance / retrocession-rate
  columns and required publication from 1 July 2022 [R9].

### 5. Garantie plancher — the benefit definition
The `garantie plancher` (floor death benefit) pays, on the insured's death, at least a defined
floor amount, so the beneficiaries are protected against a fall in the UC values. Two structural
families were retrieved:

**(a) Optional rider, priced by an explicit risk premium.**
- Generali (Himalia, Bourso Vie): available **only at subscription**, insured aged over 12 and
  under 75; two options —
  - **Option 1 (`plancher simple`)**: `capital plancher` = the sum of **gross** premiums paid to
    the euro fund(s), the UC supports and the fonds croissance, less any surrenders, advances and
    unpaid interest [S1][S3].
  - **Option 2 (`plancher indexée`)**: the same sum **indexed at an annual rate of 3.50%**, with
    surrenders indexed on the same basis [S1][S3][S2].
  - `Capital sous risque` (net amount at risk) = the guaranteed floor minus the account value at
    the calculation date, **capped at 300,000 €**; any excess reduces the floor [S1][S3].
- Spirica (LINXEA Spirit 2): optional, at subscription only, insured over 12 and under 75;
  guaranteed capital = the sum of **net** premiums on all supports less surrenders, advances and
  unpaid interest; `capital sous risque` **capped at 300,000 €** [S4 Annexe I].
- Suravenir (LINXEA Avenir 2): a differently shaped rider — it pays **the `capital sous risque`
  itself**, defined as the positive difference between cumulative net premiums (less surrenders,
  advances and their interest) and the surrender value at the date the death certificate is
  received; **capped at 100,000 € per contract**; entry ages 12 to under 70; **a one-year
  `délai de carence`** so cover begins only at the end of year 1; no medical formalities
  [S7].

**(b) Automatic cover, financed inside the management charge.**
- MACSF: granted automatically to the day of the 70th birthday; the death capital may not be
  less than total premiums net of entry charges since membership, less partial surrenders and
  outstanding advances; **also triggered by IFTD** (total and definitive functional invalidity,
  3rd-category Social Security invalidity, the surrender to be claimed within one year and
  evidenced); capped at **762,245 € of net premiums across all MACSF UC contracts**; granted to
  31 December of the membership year and tacitly renewed [S10 ART 10].
- Afer: automatic, applies to death **before the 75th birthday**, per support; benefit =
  `max(épargne investie, épargne constituée)` where `épargne investie` = number of units × PRUM
  (see §6) [S11 Annexe 3].
- PRO BTP: automatic, applies where death occurs **before the 80th birthday**, then renewable
  annually at the insurer's discretion and ceasing automatically at 80; benefit =
  `max(épargne constituée on all supports, cumulative gross premiums less the capital component
  of partial surrenders, revalorised annually at a rate set by the insurer)`, less unrepaid
  advances — an indexed floor whose index is **discretionary, not contractual** [S12][S13 art. 8.2].

**Variant not found.** No retrieved document offers a `plancher cliquet` (a ratchet on the
highest account value previously reached). The three indexation designs actually seen are: no
indexation (Generali option 1, Spirica, MACSF, Suravenir, Afer), a fixed 3.50% p.a. (Generali
option 2), and a discretionary annual rate (PRO BTP). Treat the existence of a market `cliquet`
variant as [unverified].

Termination of the guarantee, in every case: total surrender, payment of the death benefit,
policyholder cancellation, insurer cancellation, or the age limit — 70 [S10], 75 [S1][S3][S4][S7]
[S11], 80 [S12][S13].

### 6. Garantie plancher — the Afer PRUM construction
Afer's `note technique` (Annexe 3 to the notice) is the only retrieved document that specifies
the floor at support level with a running average cost price [S11]:
- For each UC support, the floor is `number of units held × PRUM`, where the
  `prix de revient unitaire moyen` is recomputed at every investment:
  `PRUM(1) = price of the first units`;
  `PRUM(n+1) = (PRUM(n) × units held before the new investment + price of the new investment) /
  (units held before + units bought)`.
  An "investment" is a premium, an incoming arbitrage or the reinvestment of a distribution.
- Surrenders and outgoing arbitrages reduce the unit count but **leave the PRUM unchanged**, so
  the floor scales down proportionally.
- Published worked example (reproduced because it is the arithmetic a model must match):

| Date | Operation | Amount | NAV | Units bought/sold/distributed | Units held | PRUM | Floor | Account value |
|---|---|---|---|---|---|---|---|---|
| 01/01/2006 | premium | 10,000 | 20.00 | 500 | 500 | 20.00 | 10,000 | 10,000 |
| 16/07/2006 | premium | 42,000 | 21.00 | 2,000 | 2,500 | 20.80 | 52,000 | 52,500 |
| 01/09/2007 | surrender | 4,000 | 20.20 | 198 | 2,302 | 20.80 | 47,882 | 46,500 |
| 25/09/2008 | distribution | 1,125 | 22.50 | 50 | 2,352 | 20.84 | 49,016 | 52,920 |

  with `20.80 = (500 × 20 + 2,000 × 21) / 2,500` and
  `20.84 = (2,302 × 20.80 + 50 × 22.50) / 2,352` [S11 Annexe 3].
- Valuation on death uses the Wednesday liquidation value following receipt of the death
  certificate (or the preceding trading day), provided the certificate arrives before 16:00 on
  the preceding working day [S11].

### 7. Garantie plancher — how it is priced (the modelling heart)
Two pricing regimes appear, and they are structurally different for a cash flow model.

**(a) Explicit risk premium on the `capital sous risque`, age-rated.**
- Formula, published verbatim by Spirica:
  `Pr = K × (PA / 10 000) × 1/52`
  where `Pr` is the weekly premium calculated each Friday, `K` is the `capital sous risque`
  observed that Friday, and `PA` is the annual premium per 10,000 € of capital sous risque for
  the insured's age at the calculation date [S4 Annexe I].
- **When the account value exceeds the guaranteed capital, the cost is nil** — the rider is a put
  and the premium is only charged when it is in the money [S3 art. 21][S4 art. 17.1.2].
- Observation frequency: **each Friday** at Spirica [S4] and Bourso Vie [S3]; **each Tuesday** at
  Himalia [S1]; **at each month end** at Suravenir [S7].
- Levy: the monthly premium is the sum of the weekly premiums, taken in arrears on the last day of
  the month, **first from the euro fund** and then from the largest UC support by cancelling units
  [S1][S3][S4]. Suravenir instead accumulates the monthly premiums and levies them at the latest
  on 31 December, in units and/or euros [S7].
- Minimum levy threshold, deferred to the next month if not met: **15 €/month** at Generali
  [S1][S3]; **20 €/month** at Spirica [S4].
- Unpaid premiums are recovered from the benefit on surrender, term or death [S1][S3][S4].
- If the premium exceeds the account value the insurer suspends the guarantee, gives 40 days'
  notice by registered letter to pay, and cancels definitively on default [S1][S3][S4].
- Joint lives: on a first-death contract the two lives' premiums are **added**; on a second-death
  contract the **lower** of the two premiums is charged [S1][S3][S4].
- Where a `fonds croissance` is present the policyholder must keep at least 10% of the account
  value on the euro fund so the premium can be levied, with a warning letter below 5%; the
  premium is never taken from the fonds croissance [S1][S2].

Published tariffs — annual premium per 10,000 € of `capital sous risque` by attained age:

| Age | Generali [S1][S3] | Spirica [S4] | Suravenir [S7] (rebased: monthly rate per 1,000 € × 12 × 10) |
|---|---|---|---|
| 12–30 | 12 € | 17 € | 18 € |
| 31 | 12 € | 18 € | 18 € |
| 32 | 12 € | 19 € | 19.2 € |
| 33 | 13 € | 19 € | 21.6 € |
| 34 | 14 € | 20 € | 22.8 € |
| 35 | 15 € | 21 € | 24 € |
| 36 | 17 € | 22 € | 25.2 € |
| 37 | 18 € | 24 € | 27.6 € |
| 38 | 20 € | 25 € | 30 € |
| 39 | 21 € | 26 € | 33.6 € |
| 40 | 24 € | 28 € | 36 € |
| 41 | 26 € | 30 € | 40.8 € |
| 42 | 29 € | 32 € | 45.6 € |
| 43 | 33 € | 36 € | 49.2 € |
| 44 | 36 € | 39 € | 54 € |
| 45 | 40 € | 41 € | 60 € |
| 46 | 43 € | 44 € | 66 € |
| 47 | 47 € | 47 € | 72 € |
| 48 | 51 € | 51 € | 76.8 € |
| 49 | 54 € | 56 € | 82.8 € |
| 50 | 58 € | 61 € | 88.8 € |
| 51 | 62 € | 67 € | 94.8 € |
| 52 | 67 € | 73 € | 100.8 € |
| 53 | 72 € | 80 € | 108 € |
| 54 | 77 € | 87 € | 115.2 € |
| 55 | 82 € | 96 € | 124.8 € |
| 56 | 87 € | 103 € | 132 € |
| 57 | 93 € | 110 € | 141.6 € |
| 58 | 100 € | 120 € | 150 € |
| 59 | 107 € | 130 € | 160.8 € |
| 60 | 115 € | 140 € | 172.8 € |
| 61 | 123 € | 151 € | 186 € |
| 62 | 134 € | 162 € | 201.6 € |
| 63 | 145 € | 174 € | 217.2 € |
| 64 | 158 € | 184 € | 237.6 € |
| 65 | 172 € | 196 € | 258 € |
| 66 | 188 € | 208 € | 282 € |
| 67 | 205 € | 225 € | 307.2 € |
| 68 | 223 € | 243 € | 336 € |
| 69 | 243 € | 263 € | 366 € |
| 70 | 266 € | 285 € | 399.6 € |
| 71 | 290 € | 315 € | 436.8 € |
| 72 | 317 € | 343 € | 475.2 € |
| 73 | 345 € | 375 € | 519.6 € |
| 74 | 377 € | 408 € | 565.2 € |
| 75 | — | — | 618 € |

  Generali's table is printed as an annual premium per 10,000 € for ages "de 12 à 32 ans" = 12 €
  through 74 = 377 € [S1][S3]. Spirica's is printed the same way for "12 à 30 ans" = 17 € through
  74 = 408 € [S4]. Suravenir's is printed as a **monthly** premium per 1,000 € of capital sous
  risque, "jusqu'à 30 ans" = 0.15 € through 75 = 5.15 €; the third column above multiplies by 12
  and by 10 to put it on the same basis. Suravenir separately describes the rates as "de 0,15 ‰ à
  5,15 ‰ des capitaux sous risque" per month [S7]; on the monthly-rate reading the annualised
  charge runs from 0.18% to 6.18% of the capital sous risque. **The monthly-versus-annual reading
  of the ‰ figures is [unverified]** — the tariff table itself is unambiguous ("Prime par mois
  pour un capital sous risque de 1 000 €"), and the third column follows the table.
  Expressed as annual rates on the capital sous risque, the three tariffs run 0.12%–3.77%
  (Generali), 0.17%–4.08% (Spirica) and 0.18%–6.18% (Suravenir). All three rise roughly
  geometrically with age, at about 8%–10% a year over ages 40–74 — consistent with a mortality
  loading, but **no insurer publishes the mortality table or the loading behind the tariff**, so
  the implied `qx` cannot be recovered from these documents.

**(b) Implicit financing inside the UC management charge, flat and age-independent.**
- MACSF: 0.10% p.a. of the UC balance as an explicit `cotisation`, **plus** 0.20% of the 0.50%
  management charge allocated to the guarantee, i.e. an all-in 0.30% p.a. of UC, charged only
  until and including the year of the 70th birthday [S10 ART 8.B, 8.D].
- PRO BTP: no separate figure — the plancher is financed inside the 0.80% p.a. UC charge, which
  ceases at the 80th birthday [S13 art. 32.4].
- Afer: 0.055% p.a. of the savings invested in UC or eurocroissance, "mutualisé entre tous les
  adhérents", **explicitly independent of the member's age** [S11].
- Modelling consequence: in family (b) the charge is a flat rate on the account value, so it is
  a deterministic drag on the unit count; in family (a) it is a stochastic charge proportional to
  `max(0, floor − account value)`, which is path-dependent and correlated with the UC return.

**Numeric illustration of family (a) published by the insurer.** Bourso Vie's 8-year table, on a
10,000 € premium split 70% euro / 30% UC, insured aged 50, `garantie plancher` option 1: the euro
fund's year-1 surrender value is 6,947.50 € in the rising-UC scenario — exactly
`7,000 × (1 − 0.75%)`, i.e. the plancher cost is **zero** — against 6,945.49 € in the falling-UC
scenario, i.e. a year-1 plancher cost of 2.01 € taken out of the euro fund. By year 8 the same
comparison is 6,590.86 € versus 6,507.00 € [S3 art. 21]. Under option 2 (3.50% indexation) the
year-1 figures are 6,945.82 € rising / 6,943.31 € falling, so even in the rising scenario the
indexed floor bites [S3].

**Exclusions** (family (a) riders): suicide, conscious or unconscious, in the first contract year;
war, on terms to be set by future legislation; aviation risks (air competitions, raids,
acrobatics) and dangerous sports (combat sports, gliding, hang-gliding, microlight, parachuting,
mountaineering, bungee jumping); death from accident or illness resulting from the insured's
intentional act; murder of the insured by the beneficiary (art. L. 132-24 Code des assurances);
and all causes provided by law [S1][S3][S4]. Spirica adds explicitly that `invalidité absolue et
définitive` (IAD) does **not** trigger the guarantee [S4]. Suravenir's list is longer and adds
narcotics, drink-driving, unlawful activities, motor competition/records, civil or foreign war,
riot, active participation in terrorism, and nuclear events [S7]. MACSF, by contrast, extends the
cover to IFTD [S10].

**Regulatory hook.** Where the plancher deductions make it impossible to state generic surrender
values in advance, art. A. 132-4-1 du Code des assurances requires the insurer to publish worked
examples instead; Suravenir cites it expressly and prints three scenarios [S7], Spirica prints
scenarios at ±10% p.a. for an insured aged 40 [S4 art. 17.1.2], Generali prints ±50% over 8 years
for an insured aged 50 [S1][S3].

### 8. Gestion pilotée / gestion sous mandat
- Three delegation models appear: `gestion libre` (self-directed), `gestion pilotée` /
  `mandat d'arbitrage` (the insurer or a mandatary manages the allocation), and
  `gestion à horizon` / `gestion profilée` (a rule-based glide path by horizon or risk profile)
  [S4][S5][S7][S12][S13].
- Extra charge: +0.60% p.a. (0.15%/quarter) [S1]; +0.2% to +0.70% p.a. (0.05%–0.175%/quarter) by
  profile [S4][S6]; +0.20% p.a. (0.60% → 0.80% on UC) [S7][S8]; +0.30% p.a. on both UC and euro
  [S13]. Market average: `gestion sous mandat` costs 1.17% against 0.82% for `gestion libre`
  [R13].
- Restrictions: at Generali, ETF and direct equities are **not available** in gestion pilotée, and
  none of the automatic arbitrage options may be combined with it [S1]. At Suravenir the two
  compartments are segregated — supports eligible for the mandate become inaccessible in gestion
  libre, and the programmed arbitrage options are available only if **only** the gestion libre
  compartment is open [S7]. Minimum 1,000 € to open the mandate compartment [S7].
- Named profiles with published equity bands (Himalia): DNCA Diversifié Équilibre 40%–60%
  equities; Financière de l'Échiquier Carte Blanche 75%–95%; Financière de l'Échiquier Prudent
  20%–40%; Rothschild Dynamique 20%–80% [S1]. Spirica's LINXEA Spirit 2 offers Montségur
  (Défensif/Équilibre/Dynamique/Agressif) and Yomoni (Défensif/Équilibre/Tonique/Offensif)
  profiles [S6]. Suravenir publishes profile-level KIDs (défensif, équilibré, dynamique, agressif,
  équilibré responsable) [S7 documentation index].
- Arbitrages performed inside a managed profile are free [S1][S4][S13]; changing between profiles
  or between management modes is charged (1% with a 15 €/30 € minimum at Generali [S1]; 0% online
  / 15 € on paper at Spirica [S6]).
- Information duty: policyholders under a mandate must be told of the arbitrages performed at
  least once a year and on termination of the mandate [S13 art. 19].

### 9. Automatic arbitrage options
Names and parameters differ by insurer; the mechanisms fall into five families.

**Investissement progressif** (`dollar-cost averaging` out of the euro fund into UC).
- Spirica: available once the contract exceeds 5,000 €; monthly arbitrages from the euro fund to
  selected UC over a chosen number of months; minimum 100 € per arbitrage and 50 € per
  destination support; executed on the **first Friday of each month**; ends when the euro fund is
  insufficient; 15 days' notice to change [S4 art. 11.2.1].
- Suravenir: minimum 1,000 € total to be switched, available on the first Friday equivalent
  schedule of monthly/quarterly/half-yearly/annual arbitrages; if set up at inception it must
  cover the whole invested capital; sums added to the source support after setup are ignored
  [S7].
- PRO BTP: arbitrages under the `investissement progressif` option are free [S13].

**Sécurisation des plus-values** (profit lock-in into a low-risk support).
- Spirica: contract value above 5,000 €; threshold at least 5% and a whole number; a single
  destination `fonds de sécurisation`; the `assiette de sécurisation` = cumulative net investments
  less the pro-rata of units disinvested (excluding units cancelled by the securing arbitrages
  themselves and by UC management charges); minimum arbitrage 100 €, minimum 50 € per destination
  support [S4 art. 11.2.2].
- Generali: contract value at least 10,000 € (excluding fonds croissance, ETF and Actions) to set
  up, terminating below 5,000 €; thresholds fixed at **5%, 10%, 15% or 20%**; the account value is
  compared to the `assiette` **each Friday**; if the gain exceeds the reference amount the whole
  observed gain is switched on the **following Monday's** valuation date to one of six named
  money-market `supports de sécurisation` (ISINs published in the conditions); each arbitrage
  costs 0.50% of the amount transferred; the option terminates automatically on a partial
  surrender, an arbitrage, an advance, or a switch to gestion pilotée [S1].
- Suravenir: threshold at least 5% of the net invested capital; the gain is computed **daily**;
  the order is placed on the working day following the valuation that triggered it; the threshold
  is chosen support by support; new supports are not covered [S7].
- Afer (`Sécurisation des Performances`): a `valeur de référence` per support, reset at each new
  investment to the average acquisition price since the reference date; a chosen trigger rate; a
  fully worked four-step example is published — reference value 20 €, 100 units, threshold 15%; a
  1,000 € premium at 25 € adds 40 units and resets the reference to
  `(100 × 20 + 40 × 25)/140 = 21.43 €`; at a NAV of 28 € the observed performance is 30.7%, the
  gain is `(28 − 21.43) × 140 = 920 €`, and at the next day's NAV of 28.20 € this is
  `920 / 28.20 = 32.62` units switched to the euro fund, leaving 107.376 units and a new reference
  value of 28.20 € [S11 Annexe 4].

**Limitation des moins-values / stop-loss** (loss cut-out), in absolute and trailing forms.
- Generali offers both: `limitation des moins-values`, whose `valeur liquidative de référence` is
  the NAV at the first date after setup on which the support's savings are positive; and
  `limitation des moins-values relatives`, whose reference is the **highest NAV reached** since
  that date. Thresholds 5%, 10%, 15% or 20%; observation each Friday; execution on the following
  Monday; the **whole** value of the support is switched to the chosen securing support; charge
  0.50% of the amount transferred; the two are mutually exclusive but compatible with the other
  options [S1 art. 14.4].
- Spirica offers the same two variants under one option: for absolute limitation the trigger base
  is cumulative net investments less gross disinvestments; for relative limitation it is the units
  held × the highest NAV reached since setup, adjusted up on investment (at the highest NAV since
  the investment date) and down pro rata on disinvestment. Threshold at least 5% (whole number),
  and the **percentage of the support to disinvest** is itself a parameter, at least 5%. Checked
  **daily** against the latest known NAVs, executed on the first working day after the breach;
  minimum arbitrage 100 €; the option ends automatically when the contract's `valeur atteinte`
  falls below 1,000 €; it may run alongside `sécurisation des plus-values` [S4 art. 11.2.3].
- Suravenir offers `stop-loss relatif` only, trailing from the highest capital value since setup,
  minimum threshold 5%, switching the **whole** net invested capital of the source support to one
  or two destinations; it is the only option that may be combined with
  `sécurisation des plus-values` [S7][S9].

**Rééquilibrage automatique** (rebalancing to a target allocation).
- Spirica: annually on the contract anniversary, restoring the whole `valeur atteinte` to the
  target allocation chosen [S4 art. 11.2.4].
- Suravenir: monthly, quarterly, half-yearly or annually, executed **on the 20th of the month** at
  the end of each period, across at least two selected supports; supports not selected are
  untouched; the option is stopped automatically by any arbitrage or partial surrender and is not
  reinstated by default; scheduled premiums must be dated between the 1st and 10th of the month
  [S7].

**Dynamisation des intérêts / des plus-values** (recycling euro-fund interest into UC).
- Afer (`Dynamisation des Intérêts`): a chosen annual percentage of the previous year's euro-fund
  interest, net of management charges and social levies, is switched free of charge into chosen UC
  on the first Wednesday trading day of January; a minimum trigger amount applies — the published
  example uses 20,000 € on the euro fund, a definitive rate of 2%, hence 400 € of interest, a 50%
  dynamisation level giving 200 €, against a 150 € minimum [S11 Annexe 4].
- Generali (`dynamisation des plus-values`): the `assiette` is cumulative net investments in the
  Actif Général euro fund; the gain is measured against the value reached on 1 January [S1].
- Suravenir also lists `dynamisation des plus-values` among its five programmed options [S7].

Combination rules: Suravenir allows only `sécurisation des plus-values` + `stop-loss relatif` and
forbids every other pairing [S7]; Generali forbids `sécurisation` alongside `transferts
programmés`, `dynamisation` or `rachats partiels programmés` but allows the limitation options
with everything [S1]; Spirica allows the two loss/gain options together [S4].

### 10. Rachat (surrender and partial withdrawal) and arbitrage
- Every retrieved contract carries a surrender right at any time after the 30-day renonciation
  period, with settlement within a statutory maximum of two months from receipt of a complete
  request (art. L. 132-21) [S10 ART 13], or a contractual 30 days [S4][S11].
- Default allocation of a partial surrender: **pro rata across supports**, unless the policyholder
  elects the supports (and excluding SCPI and private-debt UC from the pro-rata default at MACSF)
  [S10 ART 13.A]. A surrender to repay an `avance` is always pro rata [S10].
- Where a beneficiary has formally accepted the benefit (art. L. 132-9), the contract becomes
  unavailable and any surrender needs the accepting beneficiary's express agreement [S10 ART 13.A].
- Value dating: MACSF values the UC leg of a total surrender at J+3 working days after the
  surrender's effective date J, and determines each UC liquidation value on the evening of the
  following working day [S10 ART 12.B–12.C];
  Suravenir dates online arbitrages received before 23:00 to the next working day and other
  requests to at most the second working day [S7]. Generali settles ETF and Actions at a single
  daily reference price in EUR [S1].
- Arbitrage minimums and residuals: Suravenir minimum 100 € per arbitrage and a 100 € minimum
  remaining on any partially switched support (unless disinvested entirely) [S7]; Spirica
  minimum 100 € per programmed arbitrage and 50 € per destination support [S4].
- Insurer's right to refuse: MACSF may temporarily limit or refuse investment into the euro fund
  "afin de préserver la performance ou la sécurité de l'épargne de l'ensemble des Adhérents"
  [S10 ART 15]; Suravenir may defer arbitrages out of a euro fund or a real-estate UC for up to
  six months [S7].
- Pledged contracts (`nantissement`, `délégation`) require the creditor's prior agreement to
  arbitrage [S10 ART 15] and suspend certain programmed options [S4][S7].
- `Avances` (policy loans): PRO BTP caps advances on UC at 60% of the UC savings, at a quarterly
  reset rate of at least TME + 1% [S13 art. 33]. Advances and their interest are always deducted
  from the plancher benefit [S1][S3][S4][S7][S10][S13].
- Minimum surrender values for the first eight years must be tabulated (art. L. 132-5-2); every
  contract prints them, **in number of units for UC** [S3 art. 21][S4 art. 17][S7][S10 ART 12.A]
  [S11]. Where an optional plancher is in force, Spirica states there are no minimum surrender
  values in euros [S4], and Suravenir states the euro funds carry no minimum guaranteed surrender
  value [S7].

### 11. Prélèvements sociaux — the euro/UC asymmetry
- Rate: **17.2%**, composed of CSG 9.9%, CRDS 0.5%, prélèvement social 4.5%, contribution
  additionnelle 0.3%, prélèvement de solidarité 2.0% [S4 Annexe II].
- **Euro fund: levied annually**, when interest is credited to the contract ("lors de leur
  inscription en compte annuelle"), and again on death for gains that have not already borne the
  levy [S4 Annexe II][R8 II, 3°, a)].
- **UC: levied only at `dénouement`** — on partial or total surrender, at term, or on the death of
  the insured — never year by year [S4 Annexe II][R8 II, 3°, c)].
- `Eurocroissance` / diversification-provision supports: levied when the guarantee is reached,
  i.e. at the engagement's maturity; on death or total surrender, on the gains observed at that
  date [S4 Annexe II][R8 II, 3°, b)].
- Restitution: where the final liquidation of the contract produces a negative base, the excess
  already levied under a) and b) is returned to the contract by set-off or reimbursement
  [R8 III bis]. This is the mechanism that refunds an over-levied euro-fund contribution in a
  multisupport contract whose UC component has lost money.
- Modelling consequence: on a multisupport contract the social-levy cash flow is **not** a single
  end-of-contract item. It has an annual component sized on the euro fund's credited interest and
  a terminal component sized on the UC gain, plus a possible refund. The two must be modelled
  separately.

### 12. Income tax and death duties (as stated by the insurers)
- Gains (`produits`) on surrender are taxed at `dénouement` only; the contract's duration runs
  from the first premium to the surrender [S4 Annexe II].
- Two-step levy: a `prélèvement forfaitaire obligatoire non libératoire` (PFONL) of **12.8%**
  where the contract is under eight years old and **7.5%** at eight years or more, taken by the
  insurer as a payment on account, with a possible exemption for reference incomes below
  25,000 € (single) / 50,000 € (joint); then reconciliation the following year against the
  flat tax or the progressive scale, with restitution of any excess [S4 Annexe II].
- At eight years or more: **7.5%** on the share of gains attributable to premiums not exceeding
  150,000 € of un-surrendered premiums, and **12.8%** on the excess; plus an allowance of
  **4,600 €** (single) / **9,200 €** (jointly assessed) applied first to the 7.5% band [S4].
- Exemptions on redundancy, early retirement, 2nd/3rd-category invalidity, or judicial liquidation
  of a self-employed activity, provided the surrender is requested before the end of the following
  year [S4].
- Death: **art. 990 I CGI** — for premiums paid before age 70, a 20% levy on the death capital
  above a **152,500 €** allowance per beneficiary, rising to 31.25% above 700,000 €; **art. 757 B
  CGI** — for premiums paid after age 70, ordinary succession duties on the premiums above a
  **30,500 €** aggregate allowance. Surviving spouses, PACS partners and qualifying siblings are
  exempt [S4 Annexe II][S10 ART 19].
- IFI: rachetable contracts are within the `impôt sur la fortune immobilière` base to the extent
  of the 1 January surrender value representing taxable real-estate assets held inside the UC
  [S4 Annexe II][S1].
- The contract is exempt from `taxe d'assurance` (art. 995 CGI) [S10 ART 19]; annuity payments are
  taxed under art. 158-6 CGI [S10 ART 19].
- All of the above is reproduced from insurer annexes, which state expressly that the tax summary
  is indicative and non-contractual [S4][S1].

### 13. PRIIPs DIC (KID) content
- The DIC is a European standardised precontractual document of at most two to three pages, to be
  delivered a reasonable time before subscription, and expressly not a marketing document [R16].
  For UC it applies both to the insurance wrapper (a multi-option product, MOP) and to the
  underlying funds [R16][R15].
- SRI: presented on the 1–7 scale. Because a multisupport contract's risk depends on the supports
  chosen, the MOP DIC gives a **range**: "entre les classes de risque 1 et 7 sur 7" [S5]; "classe
  de risque 1 à 5 sur 7" [S12]. The insurer refers the reader to the per-support documents for the
  specific SRI [S5][S12].
- Cost tables are likewise ranges. LINXEA Spirit 2 (10,000 € invested, 0% return assumed in
  year 1): total costs 50.25 €–1,668.95 € after 1 year and 404.84 €–30,028.49 € after 8 years;
  annual reduction in yield 0.50%–16.69% (1 yr) and 0.51%–8.77% (8 yr); composition after 8 years —
  entry 0.00%–0.84%, exit 0.00%–1.35%, management and administrative 0.50%–4.43%, portfolio
  transaction 0.00%–7.43%, performance fees 0.00%–4.63% [S5]. Multisupport CONFIANCE (10,000 €):
  total costs 73 €–648 € after 1 year and 724 €–4,553 € after 8 years, i.e. 0.7%–6.5% and
  0.7%–3.7% reduction in yield; entry 0.00%–0.7%, exit 0.00%, transaction 0.0%–1.2%, other
  recurring 0.7%–2.1%, performance fees 0.00% [S12].
- Recommended holding period: **8 years** in both retrieved MOP KIDs, justified by the contract's
  initial term and by the eight-year tax threshold [S5][S12].
- Guarantee-scheme disclosure: FGAP cover of **70,000 € per person per insurer** for capital, and
  **90,000 €** for annuities in payment (art. L. 423-1 Code des assurances) [S5]; PRO BTP states
  the 70,000 € figure and describes the ACPR's transfer tender in a failure [S12].
- Performance scenarios: **not extracted**. The two retrieved MOP DICs both omit numeric
  performance scenarios and refer to the per-support documents instead [S5][S12]. The four-scenario
  set (stress, unfavourable, moderate, favourable) prescribed by Delegated Regulation 2017/653 is
  therefore [unverified] against any document read in this session (see [R18]).
- Renonciation: 30 calendar days from receipt of the membership certificate or from signature of
  the subscription form [S5][S12][S4][S10].

### 14. Loi Eckert — unclaimed contracts and post-mortem treatment
- Insurers must check at least annually whether insureds have died, by consulting a professional
  body with access to the RNIPP (AGIRA), and must search for beneficiaries [R10].
- Settlement deadline: one month from receipt of the documents necessary for payment, after which
  the unpaid capital bears interest at the **legal rate plus one half for two months, then at
  double the legal rate** [R12 — retrieved version is pre-2016; the post-Eckert wording was not
  read].
- Post-mortem revalorisation: art. L. 132-5 requires the capital to be revalorised from the date
  of death until receipt of the L. 132-23-1 documents (or until deposit with the Caisse des dépôts
  under L. 132-27-2), at not less than a rate fixed by decree [R11]. **Contracts implement this
  differently for UC**: Bourso Vie states that after death both the euro fund and the UC continue
  to be valued to the settlement date, so UC values keep fluctuating up and down [S3 art. 19];
  Afer fixes the valuation to the Wednesday following receipt of the death certificate
  [S11 Annexe 3]; Suravenir measures the capital sous risque at the date the death certificate is
  received [S7].
- Deposit and escheat: sums unclaimed ten years after the insurer learns of the death are
  transferred to the Caisse des dépôts et consignations (accessible through the Ciclade service),
  and are acquired by the State a further twenty years later if still unclaimed [S11][R10].
- Prescription: two years from the event giving rise to the action (art. L. 114-1) [S13 art. 20].
- Annual information: the policyholder must receive a statement showing, per support, the number
  of units held and their value at the last valuation date, and the surrender value of the euro
  fund [S13 art. 19].

### 15. Market context and calibration anchors
- 2025: UC premiums 75.1 bn € (39.1% of all life premiums); UC benefits 32.6 bn €; UC net inflow
  +42.5 bn €; euro→UC transfers +2.7 bn € of which +1.2 bn € arbitrages; UC mathematical
  provisions 666.4 bn € at year end (+13.5%), about 32% of total assurance vie savings [R13][R14].
- 2025 aggregate UC performance +5.5% (gross of contract charges, net of fund charges); five-year
  average fund performance net of fund charges +4.9%; 2025 segment contributions: equities +8.1%,
  asset-allocation funds +5.3%, bonds and bond funds +2.2%, money market +2.0%, real-estate UC
  −2.9% [R13].
- Charge anchors for calibration: contract charge on UC 0.88% (0.82% gestion libre / 1.17% gestion
  sous mandat), euro fund 0.66%, all-in 0.73%; underlying fund recurring costs 1.60% [R13].
- Redemption/benefit ratio: UC benefits 32.6 bn € against UC provisions of 666.4 bn € implies an
  aggregate outflow rate of roughly 4.9% of provisions in 2025 — **a derived figure, not a
  published one**, and it mixes surrenders, deaths and maturities [derived from R13].
- No insurer publishes lapse, surrender or mortality experience for these contracts, and no
  retrieved document gives a `garantie plancher` claims ratio.

### 16. What the retrieved documents do NOT give a modeller
- **No mortality basis.** The three published plancher tariffs [S1][S3][S4][S7] are rate cards; the
  underlying table (TH00-02/TF00-02, an experience table, or a loaded regulatory table), the age
  definition (attained age, age next birthday), the expense loading and the profit margin are all
  undisclosed. Any decomposition of the tariff into `qx` plus loading is **[std]** work for the
  reference implementation.
- **No surrender or arbitrage behaviour.** No lapse table, no arbitrage frequency, no
  dynamic-lapse formula appears in any retrieved document.
- **No unit-fund return assumption** beyond the illustrative ±10% p.a. [S4], ±50% over 8 years
  [S1][S3] and 0% [S5] used in statutory surrender-value tables. These are disclosure conventions,
  not best estimates.
- **No expense basis.** Charges are disclosed; the insurer's actual acquisition and maintenance
  expenses are not.
- **No reserving basis for the plancher.** Neither the ACPR nor any insurer document retrieved
  states how the `garantie plancher` liability is valued (whether by a closed-form option
  valuation, by stochastic projection, or by an unearned-premium approach). See the gaps below.

---

## Variations across insurers

| Feature | Generali — Himalia [S1] | Generali — Bourso Vie [S3] | Spirica — LINXEA Spirit 2 [S4][S6] | Suravenir — LINXEA Avenir 2 [S7][S8] | MACSF — RES Multisupport [S10] | Afer [S11] | PRO BTP — Multisupport CONFIANCE [S12][S13] |
|---|---|---|---|---|---|---|---|
| Legal form | individual | group, individual membership | individual | individual | group (association AMAP) | group (association Afer) | group, individual membership |
| `Frais sur versement` | 4.50% max | nil | nil | nil | 3% euro / 1% UC (0.6% by DD) | 0.5% euro, **nil UC** | up to 3% |
| UC management charge | 1.00% p.a. (1.50% ETF/Actions) | 0.75% p.a. | 0.50% p.a. | 0.60% p.a. (0.80% under mandate) | 0.50% p.a. (0.45% > 450k €) incl. 0.20% plancher | 0.475% p.a. | 0.80% p.a. **incl.** plancher |
| Levy frequency on UC | quarterly | quarterly | quarterly | daily accrual, **monthly** levy | annual (31 Dec) | not stated for UC | **monthly** (end of calendar month) |
| Gestion pilotée surcharge | +0.60% p.a. | none offered in the retrieved text | +0.2% to +0.70% p.a. | +0.20% p.a. | no surcharge stated; profile arbitrages free | not in the retrieved text | +0.30% p.a. |
| Arbitrage charge | 1%, min 30 €/15 € | nil (1% on `sécurisation`) | nil online, 15 € paper after 2 free | none stated ("N/A" in the fee table) | 2% to euro, 0.20% to UC, 12 free | **nil** | 0.5%, 3 free/yr |
| Plancher: optional or automatic | **optional** rider | **optional** rider | **optional** rider | **optional** rider | **automatic** | **automatic** | **automatic** |
| Plancher floor definition | option 1 gross premiums; option 2 gross premiums **indexed 3.50% p.a.** | same two options | net premiums | pays the capital sous risque itself | premiums net of entry charges | `max(units × PRUM, account value)` per support | gross premiums revalorised at a **discretionary** annual rate |
| Age limit | < 75 at entry, ends at 75 | < 75 at entry, ends at 75 | > 12 and < 75 at entry, ends at 75 | 12 to < 70 at entry, ends at 75 | ends at 70 | ends at 75 | ends at 80 |
| Cap on cover | CSR ≤ 300,000 € | CSR ≤ 300,000 € | CSR ≤ 300,000 € | CSR ≤ 100,000 € per contract | 762,245 € of net premiums, all MACSF UC contracts | none stated | none stated |
| Waiting period | none | none | none | **1 year** | none | 30-day renonciation only | none |
| Plancher pricing | age tariff on CSR, weekly (Tuesday), monthly levy, 15 € threshold | age tariff on CSR, weekly (Friday), monthly levy, 15 € threshold | age tariff on CSR, weekly (Friday), `Pr = K×(PA/10000)×1/52`, monthly levy, 20 € threshold | age tariff on CSR, month-end, levied by 31 Dec | flat 0.30% p.a. of UC, age-independent | flat 0.055% p.a., age-independent, mutualised | inside the 0.80% UC charge |
| Other death/invalidity cover | vie universelle, vie entière | vie universelle (CSR ≤ 500,000 €), vie entière | — | — | **IFTD trigger** alongside death | — | — |
| Automatic arbitrage options | sécurisation PV; limitation MV; limitation MV relatives; dynamisation; transferts programmés (0.50% each) | sécurisation PV (1%) | investissement progressif; sécurisation PV; limitation MV (absolute and relative); rééquilibrage (free) | rééquilibrage; investissement progressif; sécurisation PV; stop-loss relatif; dynamisation PV | automatic arbitrages free | sécurisation des performances; dynamisation des intérêts (free) | investissement progressif free; others per mode |

Representative design for a reference implementation: **the Generali/Spirica shape** — an
individual multisupport contract with one euro fund and a set of UC supports; a UC management
charge levied periodically by cancelling units; free or cheap arbitrage; and an **optional,
age-rated `garantie plancher` charged on the capital sous risque, computed at short intervals and
levied monthly by cancelling units, ceasing at 75, with a cap on the net amount at risk**. That
design isolates every mechanic the brief asks for and is the only one for which a public tariff
table exists in more than one insurer's documents. The MACSF/PRO BTP/Afer shape — a flat,
age-independent charge financing an automatic floor — is a simple special case: the plancher
premium becomes a constant addition to the UC management charge and the guarantee is a pure
liability with no matching premium stream.

Institutional and product variations (context, not modelled here):
- `Eurocroissance` supports (a `provision de diversification` with a guarantee at maturity) sit
  inside the same contracts and are covered by the same plancher [S1][S2][S4][S11]; they are the
  subject of a separate frlib product and are not specified here.
- Capitalisation contracts (`contrat de capitalisation`) are said to mirror the same UC mechanics
  without the death benefit, and companion capitalisation versions of Himalia and LINXEA Spirit 2
  are known to exist — but **no capitalisation conditions were retrieved**, so every statement
  about them is [unverified] and none is relied on here.
- Bancassurance contracts (Predica, Sogécap, Cardif, CNP) were not retrieved; their charge levels
  are commonly reported to sit above the broker/online segment, which is consistent with the
  0.82%/1.17% split in [R13], but no bancassurance document was read [unverified].

---

## Gaps and caveats

1. **EUR-Lex could not be fetched.** Both Regulation (EU) 1286/2014 [R17] and Delegated Regulation
   (EU) 2017/653 [R18] returned empty bodies from every endpoint tried (remote fetcher, HTML and
   PDF with a browser User-Agent). Consequently **no PRIIPs article number, no SRI methodology
   (MRM/CRM), no performance-scenario definition and no reduction-in-yield formula is asserted
   from the source text**. Everything said about the DIC in §13 is read from the two DIC documents
   themselves [S5][S12] and from the AMF's own doctrine [R15][R16].
2. **Performance scenarios were not obtained.** Both retrieved MOP DICs omit numeric performance
   scenarios and defer to per-support documents [S5][S12]. A per-support DIC with the four
   scenarios was not retrieved. Any four-scenario table in the drafted documents must be built as
   **[std]** and labelled as such.
3. **ACPR could not be reached.** `acpr.banque-france.fr` returned HTTP 403 to the plain fetcher
   and HTTP 404 to both the French and English `analyses-et-syntheses` paths with a browser
   User-Agent. No ACPR publication is cited. In particular, **the prudential and reserving
   treatment of the `garantie plancher` — how the liability is valued, whether by closed-form
   option pricing, stochastic projection or unearned premium — is entirely uncited**, and the
   ACPR's published average euro-fund yield for 2025 (reported in the press as 2.6%) is
   [unverified].
4. **No actuarial literature was retrieved on GMDB pricing.** The web-search budget for the session
   was exhausted before the Institut des actuaires' `mémoires` collection could be searched; only
   the institute's landing page was read, which confirms a public `mémoires d'actuariat`
   collection exists at
   https://www.institutdesactuaires.com/se-documenter/memoires/memoires-d-actuariat-4651 but
   yields no document. **Nothing in these notes describes how a French insurer actually reserves
   for or hedges the plancher.**
5. **Article R. 131-1 percentages are second-hand.** The 10% and 30% concentration limits in
   R. 131-1 II [R3] come from a paraphrased fetch of the article, not from verbatim text. Do not
   quote them in a product document without re-reading the article. The same caution applies to
   the R. 332-2 enumeration [R4], whose limbs were summarised rather than transcribed.
6. **L. 132-23-1 was retrieved in a superseded version.** The URL used is date-pinned to
   2013-07-28 and served the 2007–2016 text [R12]. The one-month deadline and the
   legal-rate-plus-half / double-legal-rate interest ladder are from that version; the current
   post-loi-Eckert wording, including the fifteen-day acknowledgement period, is [unverified].
7. **L. 132-5's minimum revalorisation rate is not known.** The article defers to a decree in
   Conseil d'État and the fetched text does not expose the number [R11].
8. **Loi Eckert deposit/escheat periods.** The Légifrance fetch rendered them as "10–30 years" and
   "30+ years"; the ten-years-then-twenty reading adopted here rests on the Afer notice [S11].
   The insurer's annual unclaimed-contracts reporting duty is [unverified].
9. **Suravenir's ‰ tariff is ambiguous in one place.** The `encadré` describes the cover as
   "de 0,15 ‰ à 5,15 ‰ des capitaux sous risque" for `cotisations mensuelles`, while the tariff
   table is headed "Prime par mois pour un capital sous risque de 1 000 €" [S7]. The table is
   unambiguous and is what §7 uses; the ‰ phrasing is recorded but its monthly-versus-annual
   reading is [unverified].
10. **PRO BTP's DIC cost table has transposed row labels in the extracted text.** The "Coûts
    totaux" row carries percentages and the "Incidence sur le rendement" row carries euros [S12];
    only the reverse reading is arithmetically consistent with a 10,000 € investment, and that is
    the reading used. Re-check against the rendered PDF before quoting.
11. **Cardif, Sogécap, AXA, CNP and Predica were not sourced.** The Cardif DIC portal returned a
    page shell with no document list [S14]; the remaining bancassurers were not reached before the
    search budget ran out. The insurer sample is therefore weighted towards broker/online and
    mutual/association contracts, which are cheaper than the market average [R13]. Charge levels in
    the drafted product specification should be anchored on the France Assureurs averages [R13],
    not on the sample mean of [S1]–[S13].
12. **No `plancher cliquet` was found.** The ratchet variant named in the product brief does not
    appear in any retrieved document. Only three indexation designs were seen: none, a fixed
    3.50% p.a. [S1][S3], and a discretionary annual rate [S12][S13]. Treat a cliquet variant as
    [unverified] or introduce it explicitly as **[std]**.
13. **Document vintages vary.** Himalia [S1] is dated October 2021, Afer [S11] October 2021,
    Suravenir [S7] April 2022, Spirica's conditions [S4] July 2024, MACSF [S10] carries October
    2024 file metadata, PRO BTP's DIC [S12] May 2025, and Spirica's KID [S5] July 2026. Charge
    levels and tariffs move; the France Assureurs series [R13] is the only 2025-vintage
    market-wide figure. Bourso Vie [S3] carries no date at all in its extracted text.
14. **Fund-level charge averages are contract-specific.** The 1.87%/1.18%/1.12% and
    1.23%/1.59%/2.71% figures in [S6] and [S8] are averages over each insurer's own UC shelf at
    its last closed financial year, weighted by that insurer's holdings. They are not comparable
    like for like, and neither is comparable with the market 1.60% [R13] except as an order of
    magnitude.
15. **Afer's insurers were renamed.** The retrieved notice names Aviva Vie and Aviva Épargne
    Retraite as co-insurers [S11]; the Aviva France business was sold and rebranded (Abeille
    Assurances) after that edition. The current co-insurer names are [unverified] here and the
    notice must not be cited for them.
16. **No public rate card for the plancher beyond the three tables reproduced.** The Generali
    [S1][S3], Spirica [S4] and Suravenir [S7] tariffs are the only published prices found. They are
    reproduced here as numeric data from publicly distributed contract documents; they are not
    experience tables and must not be presented as such.
