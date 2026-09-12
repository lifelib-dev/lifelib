# Sources

Source ids, titles, publishers, URLs, access dates and retrieval markers are carried over
**verbatim** from `_research/assurance-vie-uc.md`, the citation ground truth for the [S#] and
[R#] tags in `product-spec.md` and `technical-notes.md`. Ids are never renumbered. Sources in
the research file that are not cited by either document are omitted, leaving a gap: **the only
omitted id is S14** (BNP Paribas Cardif's key-information document portal — page shell only,
the contract list rendered client-side; no Cardif figure is cited anywhere, and the resulting
absence of any bancassurance document from the sample is disclosed in `product-spec.md`,
Variations item 6). Every S1–S13 and R1–R18 entry below is cited at least once. No new source
was fetched at drafting.

Access date for every entry, including the cross-product [REG-R#] entries: **2026-08-26**.

Retrieval method carried over from the research file: French insurer and regulator hosts
frequently reject a plain fetcher, so every PDF below was downloaded with a browser
`User-Agent` and its text layer extracted locally with PyMuPDF. Where that still failed the
failure is recorded and the item is kept only as a known reference.

---

## Primary product sources [S#]

(frlib-assurance_vie_uc-s1)=

### S1. Generali Vie — "Himalia — Note d'information valant Conditions générales" (PA8301CGP, October 2021)
- Publisher: Generali Vie (Generali France), individual contract codes 8301/8302
- Doc type: Note d'information valant Conditions générales, 66 pp.
- URL: https://epargne.boursedirect.fr/uploads/files/products_fin/e1cf9a0d9a50ca064d2078bab00ec586/Himalia%20-%20Conditions%20G%C3%A9n%C3%A9rales.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Code PA8301CGP — Octobre 2021, from a
  distributor's document store (Bourse Direct); Generali's own host was not used.
- Used for: the full-service charge schedule (4.50% max `frais sur versement`, UC charge
  0.25%/quarter by reducing the number of units, 1.50% p.a. on ETF and `Actions`, arbitrage 1%
  with 30 €/15 € minima); Annexe 3's `garantie plancher` — options 1 and 2 (gross premiums,
  and gross premiums indexed 3.50% p.a.), the 300,000 € `capital sous risque` cap, weekly
  Tuesday observation with a monthly levy and a 15 € threshold, the joint-life rule, the
  exclusions, the 40-day suspension and the published age tariff; the automatic arbitrage
  options; the `garantie vie universelle` and `vie entière` riders; the ±50% eight-year
  art. A. 132-4-1 illustration.

(frlib-assurance_vie_uc-s2)=

### S2. Generali Vie — "Document d'information valant Avenant … Himalia — G Croissance 2020" (PA8301AVTD, October 2020)
- Publisher: Generali Vie
- Doc type: Avenant valant document d'information, 23 pp.
- URL: https://www.altaprofits.com/documentation/pdf/HIMALIA/Doc_info_valant_CG_Himalia.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Code PA8301AVTD — Octobre 2020.
- Used for: the plancher's interaction with an `eurocroissance` engagement — still available
  below age 75, at least 10% of the `valeur atteinte` to stay on the euro fund so the premium
  can be levied (warning letter below 5%), never levied on the `fonds croissance`; and the
  eight-year unit decay at 0.25% a quarter (99.0037 → 98.0174).

(frlib-assurance_vie_uc-s3)=

### S3. Generali Vie / Boursorama — "Bourso Vie — Notice d'information valant Conditions générales" (contract 5101)
- Publisher: Generali Vie (insurer), Boursorama (souscripteur)
- Doc type: Notice d'information valant Conditions générales, group contract with individual
  membership, 52 pp.
- URL: https://www.boursorama.com/pub/bourso/pdf/avie/cg-brsvie.pdf
- Retrieved: YES (PDF downloaded, full text extracted). **No document code or date printed in
  the extracted text** — the vintage is unknown.
- Used for: the low-charge variant (nil entry charges, UC charge 0.1875%/quarter by reducing
  units); art. 9's UC universe; **art. 19**, that UC values keep fluctuating between death and
  settlement; **art. 21**, the eight-year table whose UC column runs 100 → 99.2521 → … →
  94.1711 units and whose euro columns show a **zero** plancher cost out of the money and
  2.01 € in year 1 in the falling scenario; Annexe 3's plancher terms and age tariff.

(frlib-assurance_vie_uc-s4)=

### S4. Spirica — "LINXEA Spirit 2 — Conditions Générales" (CG4445, 01/07/2024)
- Publisher: Spirica (Crédit Agricole Assurances)
- Doc type: Conditions générales, individual contract, 32 PDF pages
- URL: https://www.linxea.com/assets/uploads/2020/08/Nouvelle-CG-Spirit-2-1-1.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Footer code "CG4445 - 01/07/2024".
- Used for: the implementation anchor. Charges (nil entry, UC 0.125% at each quarter end by
  reducing units, `gestion pilotée` band, ±0.60%/±0.10% spreads, free online arbitrage);
  art. 11.2's four programmed arbitrage options; **Annexe I**, the optional `garantie décès
  plancher` — ages over 12 and under 75, the net-premium floor, the 300,000 € cap, the
  published formula `Pr = K × (PA / 10 000) × 1/52` observed each Friday, the age tariff per
  10,000 € that this model ships as its rate table, the monthly levy taken first from the euro
  fund then from the largest UC support, the 20 € threshold, the exclusions and cessation at
  75; art. 17.1.1's A. 132-5 warning; art. 17.1.2, no minimum surrender values in euros and a
  nil cost out of the money; and **Annexe II**, the 17.2% `prélèvements sociaux` and its five
  components, the euro/UC timing asymmetry, the PFONL rates, the 4,600 €/9,200 € `abattement`
  and CGI arts. 990 I and 757 B.

(frlib-assurance_vie_uc-s5)=

### S5. Spirica — "LINXEA Spirit 2 — Document d'Informations Clés" (published 01/07/2026)
- Publisher: Spirica (ACPR register no. 1021306)
- Doc type: PRIIPs `document d'informations clés` for a multi-option product, 4 pp.
- URL: https://www.linxea.com/document/linxea-spirit-2-kid/
- Retrieved: YES (PDF downloaded, full text extracted). "Date de publication : 01/07/2026".
- Used for: the MOP KID shape — SRI as a range ("entre les classes de risque 1 et 7 sur 7"),
  cost ranges of 50.25 €–1,668.95 € after one year and 404.84 €–30,028.49 € after eight on
  10,000 €, the eight-year recommended holding period, 30-day `renonciation`, FGAP cover of
  70,000 €/90,000 €, and the omission of numeric performance scenarios.

(frlib-assurance_vie_uc-s6)=

### S6. Spirica — "Annexe — Les frais de l'assurance-vie — LINXEA Spirit 2"
- Publisher: Spirica
- Doc type: fee-transparency annex under the arrêté du 24 février 2022 [R9], 2 pp.
- URL: https://www.spirica.fr/wp-content/uploads/2022/05/Frais-transparence-Linxea-Spirit-2.pdf
- Retrieved: YES (PDF downloaded, full text extracted). No edition date; the table reflects
  "le dernier exercice clos".
- Used for: the 500 € minimum initial premium; contract charge maxima (euro 2.00%, UC 0.50%,
  `gestion pilotée ou standardisée` 0.70%); the average ongoing charges of the underlying UC
  funds by asset class with retrocession rates; nil `frais sur versement`; arbitrage at 0%
  online / 15 € paper.

(frlib-assurance_vie_uc-s7)=

### S7. Suravenir — "LINXEA AVENIR 2 — Conditions Contractuelles valant Note d'information" (April 2022, contract n° 2259)
- Publisher: Suravenir (Crédit Mutuel Arkéa)
- Doc type: Conditions contractuelles valant note d'information, 58 pp.
- URL: https://www.linxea.com/document/linxea-avenir-2-conditions-generales/
- Retrieved: YES (PDF downloaded, full text extracted). "Avril 2022".
- Used for: the **monthly levy mechanics** — charges accrued daily on the daily balance and
  levied on UC monthly by cancelling units, with the published one-year arithmetic 99.4000 and
  99.2000 units; the differently shaped optional death cover paying the `capital sous risque`
  itself, capped at 100,000 € per contract, ages 12 to under 70, a **one-year `délai de
  carence`**, no medical formalities, a monthly tariff per 1,000 €, month-end computation with
  a levy by 31 December, and cessation at 75; the statement that the euro funds then carry no
  minimum guaranteed surrender value and art. A. 132-4-1 examples replace it; arbitrage minima
  and the six-month deferral power; the five programmed options; `remise de titres` at 1%; and
  the 3% annuity instalment charge.

(frlib-assurance_vie_uc-s8)=

### S8. Suravenir — "LINXEA AVENIR 2 — Transparence de frais" (réf. TR_SURA_4E25_TUCFR)
- Publisher: Suravenir
- Doc type: fee-transparency table under the arrêté du 24 février 2022 [R9], 2 pp.
- URL: https://www.suravenir.fr/wp-content/uploads/pdf/L8312_LINXEA-Avenir-2_LINXEA.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Reference TR_SURA_4E25_TUCFR.
- Used for: the 100 € minimum initial premium; contract charge maxima (euro 3.00%, UC 0.60%,
  `mandat d'arbitrage` +0.20%); the average ongoing charges of the underlying UC funds by asset
  class with retrocession rates; nil `frais sur versement`; the 3.00% annuity charge.

(frlib-assurance_vie_uc-s9)=

### S9. Suravenir — "Demande d'opération(s) : Stop-loss relatif" (réf. 5461 R, 06/2022)
- Publisher: Suravenir
- Doc type: option election form carrying the contractual definition, 3 pp.
- URL: https://www.linxea.com/document/linxea-avenir-1-2-stop-loss/
- Retrieved: YES (PDF downloaded, full text extracted). Réf : 5461 R (06/2022).
- Used for: the trailing stop-loss definition — the loss measured against the **highest**
  capital value reached since setup, a 5% minimum threshold, and the switch of the whole
  capital of the source support.

(frlib-assurance_vie_uc-s10)=

### S10. MACSF épargne retraite — "Notice d'information — RES MULTISUPPORT" (1610201Y)
- Publisher: MACSF épargne retraite (insurer), Association AMAP (souscripteur)
- Doc type: Notice d'information, group contract with individual optional membership, 27 pp.
- URL: https://www.macsf.fr/content/download/4098/fichier/MACSF_1610201Y_Notice_information_RES_Multisupport.pdf
- Retrieved: YES (PDF downloaded, full text extracted). File metadata dates it 2024-10-23;
  printed reference 1610201Y.
- Used for: the clearest example of a **non-optional plancher financed inside the management
  charge** — ART 10 (automatic to the 70th birthday, floor of premiums net of entry charges,
  also triggered by **IFTD**, capped at 762,245 € of net premiums, tacitly renewed), ART 8.B
  (0.10% `cotisation` plus 0.20% of the 0.50% management charge) and ART 8.D (tariff revisable
  with the `souscripteur`); entry and arbitrage charges; ART 8.E's illiquid-UC penalties;
  ART 9.A's A. 132-5 warning; **ART 11–12's `provision mathématique` and surrender-value
  recursions written in units** — the only retrieved primary document that measures a UC
  provision that way, and the closest support for the conventional reading of [REG-R6];
  ART 12.A's eight-year unit tables at 0.60% and 0.50% a year;
  ART 12.B–12.C's J+3 dating; **ART 13.A's pro-rata default allocation of a partial
  surrender** and the accepting-beneficiary rule; ART 15; ART 4B's maximum age 85; ART 19's
  tax articles including CGI 995.

(frlib-assurance_vie_uc-s11)=

### S11. Afer — "Contrat collectif d'assurance vie multisupport Afer — Notice" (60121-1021, October 2021)
- Publisher: Association Afer (souscripteur); co-insurers Aviva Vie and Aviva Épargne Retraite
- Doc type: Notice d'information, group contract, 53 pp. with five annexes
- URL: https://www.afer.fr/content/uploads/2022/02/60121-1021-notice-contrat-collectif-assurance-vie-multisupport-afer.pdf
- Retrieved: YES (PDF downloaded, full text extracted). "ÉDITION OCTOBRE 2021". Caveat carried
  over: the Aviva France business has since been sold and rebranded, so the current co-insurer
  names are [unverified] and this notice must not be cited for them.
- Used for: nil UC entry charges with 0.5% on euro premiums, 0.475% p.a. management on both
  legs, **no arbitrage charges at all**; the automatic, age-independent plancher at 0.055% p.a.
  "mutualisé entre tous les adhérents"; **Annexe 3**, the `note technique` defining the floor
  per support as `max(units × PRUM, account value)` with the running-average PRUM recursion and
  its worked example (20.80 € then 20.84 €), and the Wednesday valuation after receipt of the
  death certificate; **Annexe 4**, the worked `Sécurisation des Performances` and
  `Dynamisation des Intérêts` examples; and the ten-year deposit / twenty-year escheat reading
  of the loi Eckert periods.

(frlib-assurance_vie_uc-s12)=

### S12. SAF BTP VIE (PRO BTP) — "Document d'informations clés générique — contrat Multisupport CONFIANCE" (13 May 2025)
- Publisher: SAF BTP VIE, groupe PRO BTP
- Doc type: PRIIPs `document d'informations clés` (generic MOP KID), 4 pp.
- URL: https://www.probtp.com/files/live/sites/probtp/files/media/pdf/epargne/dici/dic_generique_contrat_multisupport_confiance.pdf
- Retrieved: YES (PDF downloaded, full text extracted). Produced 13 mai 2025.
- Used for: the SRI range ("classe de risque 1 à 5 sur 7"); cost ranges of 73 €–648 € after one
  year and 724 €–4,553 € after eight per 10,000 €; the eight-year term and holding period; the
  30-day `renonciation`; FGAP 70,000 €; the 3% annuity charge; and the **plancher biting before
  the 80th birthday on gross premiums revalorised annually at a rate set by the insurer** — the
  discretionary-indexation design. Caveat carried over: the extracted text transposes the cost
  table's row labels, and only the reverse reading is arithmetically consistent with a 10,000 €
  investment; that is the reading used.

(frlib-assurance_vie_uc-s13)=

### S13. SAF BTP VIE (PRO BTP) — "Notice d'information résumant les conditions générales — contrat Multisupport CONFIANCE"
- Publisher: SAF BTP VIE
- Doc type: Notice d'information, 81 pp.
- URL: https://www.probtp.com/files/live/sites/probtp/files/media/pdf/epargne/notice-info-cg-multisupport-confiance.pdf
- Retrieved: YES (PDF downloaded, full text extracted). No edition code in the extracted text.
- Used for: art. 8.2's floor of `max(épargne constituée, gross premiums less the capital
  component of partial surrenders, revalorised annually at a discretionary rate)` before the
  80th birthday; **art. 32.4**, the operative charging clause — a UC charge capped at 0.80%
  p.a. of the `épargne constituée` per support, including the plancher financing, ceasing
  beyond the 80th birthday, **computed on the number of units held at the end of each calendar
  month**, levied at the next valuation date and reducing the number of units; art. 32.2's
  four-decimal unit conversion; art. 32.3's reinvestment of income; art. 32.5's A. 132-5
  warning; art. 32.6's 60% real-estate cap; art. 33's `avances` at 60% of UC savings and
  TME + 1%; art. 19's annual statement and plancher-renewal notice; the 0.5% arbitrage charge
  with three free a year; and the +0.30% managed-mode surcharge.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(frlib-assurance_vie_uc-r1)=

### R1. Code des assurances, art. L. 131-1
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038611256
- Retrieved: YES (article page; in force since 24 May 2019, as amended by loi n° 2019-486 (loi
  PACTE) art. 72).
- Used for: the permission to express guaranteed capital or annuities in `unités de compte`
  drawn from a decree list, and the settlement rules — cash by default, delivery of the
  underlying securities in three cases, barred on voting-right securities and on a >10%
  holding in the preceding five years. Carried caveat, repeated in both documents: **the
  number-not-value principle is not in L. 131-1 itself** — it is imposed by A. 132-5 [R2].

(frlib-assurance_vie_uc-r2)=

### R2. Code des assurances, art. A. 132-5
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006786185
- Retrieved: YES (article page; in force since 2 May 2007).
- Used for: the disclosure obligation that drives the whole model — the insurer "ne s'engage
  que sur le nombre d'unités de compte, mais pas sur leur valeur", the unit value being
  unguaranteed and market-dependent.

(frlib-assurance_vie_uc-r3)=

### R3. Code des assurances, art. R. 131-1
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043560691
- Retrieved: YES (article page; version in force from 6 May 2026).
- Used for: the UC eligibility list borrowing the R. 332-2 classes [R4], the real-estate
  vehicles admitted on the R. 131-2 to R. 131-4 conditions, and Part III's substitution
  requirement. Carried caveat: the fetch paraphrased the enumerations, so **the concentration
  percentages of Part II are not quoted** in either document.

(frlib-assurance_vie_uc-r4)=

### R4. Code des assurances, art. R. 332-2
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037635496
- Retrieved: YES (article page; version dated 22 November 2018).
- Used for: the asset classes R. 131-1 borrows — OECD sovereign bonds, regulated-market
  securities and corporate debt, SICAV shares and FCP units, listed equities, insurance-company
  shares, and the 9° bis real-estate vehicles. Carried caveat: the limbs were summarised, not
  transcribed.

(frlib-assurance_vie_uc-r5)=

### R5. Code des assurances, art. L. 131-1-1
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038507517
- Retrieved: YES (article page; in force 24 October 2024).
- Used for: the suitability gate on alternative-fund and financing-vehicle units, and the
  exemptions for retail ELTIFs and contracts under an arbitrage mandate.

(frlib-assurance_vie_uc-r6)=

### R6. Code des assurances, art. L. 131-1-2
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049720147
- Retrieved: YES (article page; in force 1 January 2025).
- Used for: the mandatory offering — at least one UC holding 5%–15% of social-economy,
  venture-capital or specialised-fund securities, at least one UC per State-recognised green or
  SRI label, and disclosure of the qualifying proportion.

(frlib-assurance_vie_uc-r7)=

### R7. Code des assurances, arts. R. 131-1 to R. 131-12 (unit-linked chapter)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000006158245/
- Retrieved: YES (chapter listing plus targeted reading of R. 131-8 to R. 131-12).
- Used for: the redemption-gating rules — which requests a suspension catches, roll-forward or
  cancellation, the floor at the last published liquidation value, the at-least-as-favourable
  restriction, durable-medium notification and unenforceability against an uninformed client,
  ACPR notification, and quarterly-disclosed estimated values.

(frlib-assurance_vie_uc-r8)=

### R8. Code de la sécurité sociale, art. L. 136-7 (CSG on `produits de placement`)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047288474/2023-03-11
- Retrieved: YES (article page; version served dated 11 March 2023).
- Used for: the euro/UC asymmetry the tax modeling turns on — II, 3°, a) the levy at inscription
  for euro rights **and for the euro component of a multisupport contract**; II, 3°, b) at the
  guarantee; II, 3°, c) at `dénouement` or on death for the unit-linked component; and III bis,
  restitution of an excess where the final liquidation gives a negative base.

(frlib-assurance_vie_uc-r9)=

### R9. Arrêté du 24 février 2022 (transparence sur les frais du PER et de l'assurance-vie)
- Publisher: Journal officiel / Légifrance (JORFTEXT000045299785)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045299785
- Retrieved: YES (consolidated text page).
- Used for: the prescribed per-support table (ISIN, management company, gross performance N−1,
  support fees, net performance, contract fees, **total fees**, final performance, retrocession
  rate) and its 1 July 2022 entry into force — the regime [S6] and [S8] instantiate.

(frlib-assurance_vie_uc-r10)=

### R10. Loi n° 2014-617 du 13 juin 2014 ("loi Eckert")
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000029095362
- Retrieved: YES (consolidated text page). In force 1 January 2016.
- Used for: the annual RNIPP search through a professional body, the beneficiary search, deposit
  with the Caisse des dépôts ten years after the insurer learns of the death, and escheat twenty
  years later. The ten-plus-twenty reading is corroborated by [S11]; the insurer's annual
  reporting duty is [unverified].

(frlib-assurance_vie_uc-r11)=

### R11. Code des assurances, art. L. 132-5 (post-mortem revalorisation)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029098941
- Retrieved: YES (article page; in force since 1 January 2016).
- Used for: the duty to revalorise the death capital from the date of death to receipt of the
  L. 132-23-1 documents or deposit with the Caisse des dépôts, at not less than a decreed rate.
  **The decree's numerical rate was not exposed in the fetched text** and is [unverified].

(frlib-assurance_vie_uc-r12)=

### R12. Code des assurances, art. L. 132-23-1 (settlement deadline and late interest)
- Publisher: Légifrance
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000017841432/2013-07-28
- Retrieved: YES — **but the URL is date-pinned and served the 19 December 2007 to 1 January
  2016 version**, i.e. the text before the loi Eckert amendments [R10].
- Used for: the one-month deadline and the legal-rate interest ladder as they stood in that
  version. The current wording, including the fifteen-day document-request step, is [unverified]
  here and is cited instead from [REG-R31], which was fetched current.

(frlib-assurance_vie_uc-r13)=

### R13. France Assureurs — "L'assurance vie en unités de compte — Année 2025"
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/wp-content/uploads/2025_assurance-vie-en-uc.pdf
- Retrieved: YES (PDF downloaded, full text extracted), 16 pp.
- Used for: the **charge levels this model's [std] parameters are set from** — the
  `encours`-weighted average contract charge on UC of 0.88% (0.82% `gestion libre`, 1.17%
  `gestion sous mandat`), 0.66% on euro supports, 0.73% all in, and 1.60% of recurring costs
  inside the underlying funds. Also 2025 UC premiums of 75.1 bn € (39.1% of life premiums), UC
  benefits of 32.6 bn €, net inflow of 42.5 bn €, UC `provisions mathématiques` of 666.4 bn €,
  performance of +5.5% and a five-year average of +4.9%. The ~4.9%-of-provisions aggregate
  outflow anchoring the surrender table is **derived** from this entry, not published in it.

(frlib-assurance_vie_uc-r14)=

### R14. France Assureurs — "L'assurance vie en unités de compte en 2025" (chiffres clés page)
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/assurance-vie/assurance-vie-unite-de-compte-2025/
- Retrieved: YES (web page).
- Used for: cross-checking [R13], and the UC share of total assurance vie `encours` — 32% at
  end-2025, thirteen points above 2005, against 68% for euro supports.

(frlib-assurance_vie_uc-r15)=

### R15. AMF — Position-recommandation DOC-2011-05, "Guide des documents réglementaires des OPC"
- Publisher: Autorité des marchés financiers
- URL: https://www.amf-france.org/sites/institutionnel/files/private/2023-02/DOC-2011-05_VF14_PRIIPs.pdf
- Retrieved: YES (PDF downloaded, full text extracted), 44 pp. Created 18 February 2011, amended
  16 February 2023.
- Used for: the retrievable anchor of the PRIIPs citation chain — DOC-2011-05 names Regulation
  (EU) No 1286/2014 and Delegated Regulation (EU) 2017/653 among its `textes de référence`,
  which is how those instruments are referred to at all given that EUR-Lex could not be fetched.

(frlib-assurance_vie_uc-r16)=

### R16. AMF — "Comprendre le document d'informations clés (DIC)" (guide pédagogique)
- Publisher: Autorité des marchés financiers
- URL: https://www.amf-france.org/sites/institutionnel/files/contenu_simple/guide/guide_pedagogique/Comprendre%20le%20document%20d'informations%20cles%20(DIC).pdf
- Retrieved: YES (PDF downloaded, full text extracted), 16 pp.
- Used for: what a DIC is — a European standardised precontractual document of two to three
  pages at most, delivered a reasonable time before subscription, expressly not a marketing
  document, applying to collective investments held through a unit-linked life contract.
  Carried caveat: this edition predates the 2023 extension of the DIC to UCITS and does not
  describe the current SRI scale or performance-scenario rules.

(frlib-assurance_vie_uc-r17)=

### R17. Regulation (EU) No 1286/2014 (PRIIPs)
- Publisher: European Union / EUR-Lex
- URL: https://eur-lex.europa.eu/eli/reg/2014/1286/oj/eng
- Retrieved: **NO** — EUR-Lex returned an empty body to both a remote fetcher and a browser-UA
  download (HTML and PDF endpoints both zero bytes). Known reference only, `fetched_ok = false`.
- Used for: nothing substantive. Cited only in the disclosure that **no PRIIPs article number is
  asserted anywhere** in these documents; its existence and its status as the source of the
  `document d'informations clés` rest on [R15] and on the DICs themselves [S5] [S12].

(frlib-assurance_vie_uc-r18)=

### R18. Commission Delegated Regulation (EU) 2017/653 (PRIIPs RTS)
- Publisher: European Union / EUR-Lex
- URL: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32017R0653
- Retrieved: **NO** — same failure mode as [R17]. Known reference only, `fetched_ok = false`.
- Used for: nothing substantive. Cited only in the disclosure that the SRI 1–7 methodology, the
  performance-scenario set and the reduction-in-yield formula are **[unverified]** here and are
  described only from the DICs that implement them [S5] [S12].

---

## Cross-product references ([REG-R#])

Cited with the [REG-R#] prefix to avoid collision with this product's own R-numbering. Full
annotated entries, with URLs and retrieval markers, live in
`references/regulatory-and-actuarial-references.md` (R1–R49 frozen).

| Tag | Short title | Relevance here | Retrieval status (per that file) |
|---|---|---|---|
| REG-R1 | Directive 2009/138/CE — Solvabilité II | best estimate + risk margin as the valuation frame | **not fetched** (EUR-Lex WAF); article numbers [unverified] |
| REG-R2 | Règlement délégué (UE) 2015/35 | why no cost-of-capital rate, lapse shock or expense rule here rests on a retrieved text | **not fetched** (same) |
| REG-R4 | EIOPA — Solvency II framework page | the authority on which the best-estimate definition is stated | fetched |
| REG-R6 | C. ass. art. R. 343-3 — eleven technical provisions | enumerates the eleven provisions and defines the `provision mathématique`; it does **not** say which of them carries a `unités de compte` engagement, so that placement is [unverified] here | fetched |
| REG-R13 | HCSF — CMF art. L. 631-2-1 (loi Sapin 2 art. 49) | power to limit surrenders and to **defer or restrict arbitrages** | fetched |
| REG-R19 | C. ass. art. L. 134-1 and R. 134-1 to R. 134-12 | the `eurocroissance` third leg, cross-referenced and out of scope | fetched |
| REG-R23 | C. ass. art. A. 335-1 and its Annexe | which mortality tables a French tariff may lawfully use | fetched, but in a pre-2016 version; current placement [unverified] |
| REG-R24 | INSEE — mortalité, espérance de vie | the only redistributable French mortality data, behind every shipped decrement CSV | fetched; licence terms [unverified] |
| REG-R29 | C. ass. arts. L. 132-5-1 / L. 132-5-2 | the 30-day `renonciation`, the `note d'information` duty and the eight-year sanction cap; it does **not** carry the eight-year minimum-surrender-value table, which is cited to the insurer documents instead | fetched |
| REG-R30 | C. ass. arts. A. 132-4 / A. 132-8 | maxima must be **disclosed, not capped** — why every charge level here is [std] | fetched |
| REG-R31 | C. ass. arts. L. 132-21 / L. 132-22 / L. 132-23-1 | two-month surrender settlement, the death-payment clock, the annual UC statement | fetched (current versions) |
| REG-R33 | PRIIPs — Règlement (UE) 1286/2014 and AMF DOC-2011-05 | the DIC regime; insurance-side SRI and scenario mechanics [unverified] | regulation not fetched; AMF document fetched |
| REG-R39 | Loi n° 2014-617 (loi Eckert) | ten-year deposit and twenty-year escheat of unclaimed proceeds | fetched |
| REG-R40 | CGI art. 125-0 A | the eight-year threshold that shapes the surrender assumption | fetched; the 150,000 € threshold [unverified] |
| REG-R41 | CGI arts. 990 I and 757 B | beneficiary-side death taxation, pre- and post-70 premiums | fetched |
| REG-R43 | Institut des actuaires — NPA 1 | the professional frame for assumption setting | fetched |
| REG-R44 | Institut des actuaires — NPA 2 (modèles actuariels) | the standard this documentation and test suite are written against | fetched; NPA 4 not retrieved |
| REG-R45 | IFRS 17 | the accounting frame; VFA mechanics [unverified] | fetched (landing page only) |
| REG-R48 | France Assureurs — assurance vie en UC en 2025 | the cross-product market charge and performance averages | fetched |

---

## Provenance note

Extraction details live in `_research/assurance-vie-uc.md`: which fact came from which
document, the browser-`User-Agent`-plus-PyMuPDF retrieval method, the two EUR-Lex failures
[R17] [R18], the ACPR 403 that leaves the prudential and reserving treatment of the `garantie
plancher` **entirely uncited**, the superseded version of L. 132-23-1 [R12], the undated Bourso
Vie document [S3], the ambiguous ‰ phrasing in Suravenir's `encadré` [S7], the transposed
cost-table row labels in PRO BTP's DIC [S12], and the absence of any bancassurance document
from the sample (S14 not retrieved). It also records the two findings that shape this product's
documents most: **no retrieved document offers a `plancher cliquet`**, and no insurer publishes
the mortality table, age definition, expense loading or margin behind its plancher tariff, so
the tariff cannot be decomposed into `qx` plus loading.

The cross-product bibliography `references/regulatory-and-actuarial-references.md` plays the
same role for [REG-R#] tags. Standardizations marked **[std]** in `product-spec.md` and
`technical-notes.md` are introduced at drafting and are not attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-assurance_vie_uc-r10
[R12]: #frlib-assurance_vie_uc-r12
[R13]: #frlib-assurance_vie_uc-r13
[R15]: #frlib-assurance_vie_uc-r15
[R17]: #frlib-assurance_vie_uc-r17
[R18]: #frlib-assurance_vie_uc-r18
[R2]: #frlib-assurance_vie_uc-r2
[R4]: #frlib-assurance_vie_uc-r4
[R9]: #frlib-assurance_vie_uc-r9
[REG-R31]: #frlib-reg-r31
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
