# Sources

Source ids, titles, publishers, URLs, retrieval markers and access dates are carried over
**verbatim** from `_research/obseques.md`, the citation ground truth for the [S#]/[R#] tags in
`product-spec.md` and `technical-notes.md`. Ids are never renumbered. Entries in the research
file that neither document cites are omitted here, leaving gaps: dropped are **S4** (CNP's
regulated-information index page — the route by which the three CNP standardised tables [S5]
[S6] [S7] were located, cited by them and not separately), **S17** (a *note d'information* that
returned HTTP 410 Gone), **S18** and **S20** (two further insurer documents, one 403 and one not
attempted), **R12** (the CCSF press release, HTTP 403 — the avis itself is kept at [R11] as the
non-retrieved anchor for the CCSF commitments), **R18** (a service-public page carrying no
figure either document needs) and **R25** (a secondary commentary whose host rejected the
fetch). No new sources were fetched at drafting; nothing here is marked "added at drafting".

Access date for every entry: **2026-08-26**. [REG-R#] sources were accessed 2026-08-26 per
`references/regulatory-and-actuarial-references.md`.

---

## Primary product sources [S#]

(frlib-obseques-s1)=

### S1. Mutex SA / Harmonie Mutuelle, "NÉOBSIA Garantie obsèques en capital — Conditions générales" (14 pp.)
- Publisher / type: Mutex SA, insurer under the Code des assurances, branche 20 Vie-Décès, distributed by Harmonie Mutuelle; *conditions générales valant note d'information*
- URL: https://www.harmonie-mutuelle.fr/sites/default/files/2024-02/CG-GARANTIEOBSEQUES.pdf
- Retrieved: YES (PDF downloaded, full text extracted with PyMuPDF).
- Used for: the implementation anchor for the contract chassis — whole-life legal form, entry 18–84 with no medical selection, capital 2000–10000 €, six premium forms, the one-year *délai d'attente* with premium refund, the accident definition, exclusions and the surrender-value benefit in an excluded case, the full charge structure (5 % / 0.40 % / 0.57 % / 0.80 %), PB credited to the capital, post-mortem revalorisation on the TME rule, *rachat* at the *provision mathématique*, *réduction* and the L. 132-20 non-payment path, the beneficiary cascade, and the per-1000 € worked grid at entry age 65.

(frlib-obseques-s2)=

### S2. Mutex SA, "NÉOBSIA CAPITAL OBSÈQUES — tableaux comparatifs des cotisations et des valeurs de rachat" (ref 2560394, 18/08/2025, 12 pp.)
- Publisher / type: Mutex SA, Harmonie Mutuelle distribution; CCSF standardised examples table
- URL: https://www.harmonie-mutuelle.fr/sites/default/files/pdf/Tableaux_comparatifs_Neobsia_HM_18-08-2025.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: temporary-premium rates at entry 50 and 60 for a 5000 € capital; the temporary-premium surrender grid that peaks at 5074 € and then declines; the statement that the capital is revalued annually via the PB; and the record that this distribution marks *viager* and *prime unique* as NA.

(frlib-obseques-s3)=

### S3. Mutex SA, "NÉOBSIA PRESTATIONS OBSÈQUES — tableaux comparatifs" (01/07/2025, 6 pp.)
- Publisher / type: Mutex SA; CCSF standardised examples table for the *prestations* form
- URL: https://www.mutex.fr/app/uploads/2025/06/tableaux-neobsia_prestations.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the *prestations* packages (3500 / 4500 / 6000 €) and the fact that its premiums for a 5000 € capital at entry 50 are identical to the capital-form table [S2] — the evidence that the services form is the same tariff, which is why it is out of model scope.

(frlib-obseques-s5)=

### S5. CNP Assurances SA, "Trésor Prévoyance Garantie Obsèques 2 — tableaux comparatifs" (01/01/2026, 6 pp.)
- Publisher / type: CNP Assurances SA (341 737 062 RCS Nanterre), Amétis distribution; CCSF standardised examples table
- URL: https://www.cnp.fr/media/fichiers/particuliers/operations-et-infos-reglementees/tableaux-comparatifs-contrats-obseques/tresor-prevoyance-garantie-obseques-2-ametis
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the most complete public rate card in the set — seven premium forms at entry 50 / 60 / 70 for a 5000 € capital, including the *prime unique* (4274.04 / 4548.60 / 4819.56 €) that supplies the `single_prem_rate` table and the RefOBS-UNI cell; the *viager*, *temporaire* and paid-up surrender grids; the subsidiary premium-form table in the worked example; the statement that premiums are never indexed and that the values exclude PB; and the 5000 €-is-close-to-the-average-funeral-cost footnote.

(frlib-obseques-s6)=

### S6. CNP Assurances Prévoyance / La Banque Postale, "Solution Obsèques de La Banque Postale — tableaux comparatifs" (12/11/2025, 6 pp.)
- Publisher / type: CNP Assurances Prévoyance, La Banque Postale distribution; CCSF standardised examples table
- URL: https://www.cnp.fr/media/fichiers/particuliers/operations-et-infos-reglementees/tableaux-comparatifs-contrats-obseques/solution-obseques-de-la-banque-postale
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: four premium forms and their rates; the no-indexation clause; and the age-60 table in which the cumulative lifetime premium is identical at ages 90 and 95 (9400 €), from which cessation near age 90 is **inferred, not stated** — the evidence behind the `prem_cease_age` fork.

(frlib-obseques-s7)=

### S7. CNP Assurances / Mgéfi, "PLURIO Solutions Obsèques Mgéfi n° MI-12-001 — tableaux comparatifs" (26/10/2023, 6 pp.)
- Publisher / type: CNP Assurances, group contract of La Mutuelle Générale de l'Économie, des Finances et de l'Industrie; CCSF standardised examples table
- URL: https://www.cnp.fr/media/fichiers/particuliers/operations-et-infos-reglementees/tableaux-comparatifs-contrats-obseques/plurio-solutions-obseques-mgefi-mi-12-001
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: a third premium-form menu and its rates, the no-indexation clause, and the 5000 € funeral-cost footnote. Dated before the CCSF commitments but already in the standardised format.

(frlib-obseques-s8)=

### S8. VIASANTÉ Mutuelle / UCR, "Notice d'information — SÉRÉNITÉ OBSÈQUES" (Notice V3.1, 8 pp. + annexe)
- Publisher / type: VIASANTÉ Mutuelle (Livre II du Code de la mutualité, SIREN 777 927 120), administered by UCR (Orias 07 000 616), group contract subscribed by the ADPM; *notice d'information*
- URL: https://ucr.fr/wp-content/uploads/2025/11/Notice-Serenite-Obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the only published technical basis in the set — surrender values on **table TH 00-02 at a technical rate of 0.75 %**; the form-dependent entry-age bands; the one-year *carence* with a refund net of the assistance premium of **12 €/year**; the **2× accidental-death enhancement from year 2** capped at 20000 €; the surrender right acquired only once **one annual premium** has been paid; the *mutualité*-code charge caps (10 % / 10.3 % of premium, ≤ 2.5 % of capital, 0.4 % + 3.3 % ongoing, 5 % inside the provision for 8 years, 5 % surrender penalty for 10); the long exclusion list and the net-premiums substitution; and the post-mortem revalorisation TME rule.

(frlib-obseques-s9)=

### S9. Macif Santé Prévoyance, "Garantie Obsèques — Note d'information détaillée" (U 821 - UNI/PREI/G OBS/05 - 07/26, 20 pp.)
- Publisher / type: Macif Santé Prévoyance (Livre II du Code de la mutualité, SIREN 779 558 501); *note d'information détaillée*, guarantees in force 1 July 2026
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/NID_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the **premium-linked revalorisation** design — PB into a *fonds de revalorisation*, credited to the *provision mathématique* on 1 April of the following year, "*la revalorisation s'accompagne d'une augmentation des cotisations restant à payer, d'un taux équivalent*" — together with its annexe C PB accounts; the acquisition charge expressed as ≤ 5.38 % of the guaranteed capital; the one-year *carence* with a refund net of instalment charges; the "jusqu'à 80 ans" premium form; the two-month surrender settlement; and the annexe B surrender grids.

(frlib-obseques-s10)=

### S10. Macif Santé Prévoyance, "GARANTIE OBSÈQUES — tableaux comparatifs" (01/01/2026, 6 pp.)
- Publisher / type: Macif Santé Prévoyance; CCSF standardised examples table
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/tableaux-comparatifs-garantie-obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: four premium forms including "jusqu'à 80 ans" at entry 50 / 60 / 70; the *viager* surrender grids at all three entry ages; and the footnote restating the *fonds de revalorisation* mechanism and the matching uprating of remaining premiums.

(frlib-obseques-s11)=

### S11. Macif Santé Prévoyance, "Garantie Obsèques — Document d'informations clés" (DIC / PRIIPs KID, ref 07/26, 3 pp.)
- Publisher / type: Macif Santé Prévoyance; PRIIPs key information document
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/DIC_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the explicit warning that total premiums may exceed the death capital; the performance scenario (3000 € capital at entry 60 growing to 3038.56 / 3633.50 / 4400.77 € at 1 / 15 / 30 years) from which the **1.2854 % p.a.** illustrative revalorisation rate is derived; the 2.2 % annual-to-monthly instalment loading; the reduction in yield of 1.77 % p.a. over 30 years and the risk class 2 of 7; the zero exit penalty; the 70000 € FGAP cap; and the use of table TH 00-02 for the lifetime-premium life expectancy.

(frlib-obseques-s12)=

### S12. Macif Santé Prévoyance, "Garantie Obsèques — Synthèse" (9 pp., in force 1 July 2026)
- Publisher / type: Macif Santé Prévoyance; pre-contractual contract synthesis
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/synthese_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the **17580 €** aggregate cap on whole-life death guarantees per insured; entry 18–80 by *différence de millésime* with no medical formality; the exclusions and the *provision mathématique* payable in each excluded case; the default beneficiary clause and the mandatory earmarking wording; and the right to change the designated funeral operator at any time.

(frlib-obseques-s13)=

### S13. Macif Santé Prévoyance, "Assurance Obsèques — Document d'information sur le produit d'assurance (DIPA)" (01/26, 2 pp.)
- Publisher / type: Macif Santé Prévoyance; IPID
- URL: https://www.macif.fr/files/live/sites/maciffr/files/dipa/DIPA_garantie_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the clearest statement in the set of the **two contract forms sold side by side** — *prestations* formulas equivalent to capitals of 3800 € and 4580 €, and a *capital* formula of 2000 € or 3000 € with complementary capitals to 13000 €; subscription without medical formality; and the one-year waiting period for death by illness.

(frlib-obseques-s14)=

### S14. AXA France, "Tableaux des exemples normalisés — Serenova" (ref 2007517 08 2025, 6 juin 2025, 3 pp.)
- Publisher / type: AXA France Vie / AXA Assurances Vie Mutuelle, association ANPERE named on the document; CCSF standardised examples table
- URL: https://media.axa.fr/content/dam/axa-fr/image/particuliers/sante/document-pdf/pdf-tableau-serenova-2025-v2.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: **the numerical anchor of the worked example** — the *viager* premium of 336.03 €/year at entry 50 for a 5000 € capital, the *temporaire* 10 ans premium of 651.26 €/year, and the quinquennial surrender-value grids that supply `surr_scale`; and, uniquely in the retrieved set, the **contractually guaranteed** uprating "*le contrat prévoit une revalorisation annuelle de 1 % du capital souscrit sans augmentation de la cotisation*". Also the entry-age 69 limit on the 20-year term and the excluded couple discount.

(frlib-obseques-s15)=

### S15. SOGECAP SA, "CONTRAT GARANTIE OBSEQUES formule BUDGET — tableau CCSF" (01/07/2025, 3 pp.)
- Publisher / type: SOGECAP SA (086 380 730 RCS Nanterre), Société Générale Assurances; CCSF standardised examples table
- URL: https://www.assurances.societegenerale.com/fileadmin/2025/tableau_CCSF_BUDGET.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: four premium forms including the *prime unique*; the discretionary revalorisation wording ("*le capital garanti **peut** être majoré de la participation aux résultats*"); the tables that run lifetime premiums to attained age **115** with no cessation and reach **24019 €** of cumulative lifetime premiums against a 5000 € capital; and the **entry-70 *viager*** surrender grid, whose values reach exactly 5000 € at 40 and 45 years — at attained age 110, a lifetime-premium provision converging on the capital at great age, not a paid-up one.

(frlib-obseques-s16)=

### S16. BPCE Vie SA, "SECUR' OBSEQUES — tableaux comparatifs des cotisations et valeurs de rachat" (juillet 2025, 3 pp.)
- Publisher / type: BPCE Vie SA (349 004 341 RCS Paris); CCSF standardised examples table
- URL: https://dda.assurances.groupebpce.com/pdfs/tableaux_comparatifs_des_cotisations_et_valeurs_de_rachat_secur_obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the most explicit PB formula in the set — "*90 % des bénéfices techniques et financiers, déduction faite d'un taux de prélèvement de gestion sur encours égal à 1 % et du taux d'intérêt technique garanti à l'adhésion, visé à l'article A 335-1 du Code des assurances*", allocated so that the capital rises with premiums unchanged; and the design that offers **only two temporary terms**, neither lifetime nor single.

(frlib-obseques-s19)=

### S19. PFG — Pompes Funèbres Générales (groupe OGF), "Comment financer ses obsèques ?"
- Publisher / type: PFG (groupe OGF); product/guide web page
- URL: http://www.pfg.fr/assurance-obseques/nos-guides-conseils/financer-obseques (the https form 301-redirects here)
- Retrieved: **NO — HTTP 403 Forbidden on both attempts, on both the https and the redirected http URL.** Known reference only; no PFG or OGF wording is quoted anywhere.
- Used for: one **[unverified]** variation note only — a search-engine snippet describing a capital contract of 1000 € to 15000 € revalued annually, with no waiting period where the premium is paid in one instalment. Recorded as a failed fetch, not as a fact.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(frlib-obseques-r1)=

### R1. Légifrance, Code général des collectivités territoriales, art. L. 2223-33
- URL: https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006192270/
- Retrieved: YES (sub-section page, articles L. 2223-31 à L. 2223-34-2).
- Used for: the prohibition of advance offers of funeral services except *formules de financement d'obsèques* — the article that makes an insurance contract the only lawful way to pre-pay a funeral.

(frlib-obseques-r2)=

### R2. Légifrance, CGCT art. L. 2223-33-1
- URL: https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006192270/
- Retrieved: YES (same page as R1).
- Used for: the earmarking rule — the capital paid to the beneficiary is affected to the subscriber's funeral, up to its cost. Cited alongside the cross-product entry [REG-R38], which carries the same article's full verbatim text.

(frlib-obseques-r3)=

### R3. Légifrance, CGCT art. L. 2223-34-1 (version in force since 28 July 2013)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027783339
- Retrieved: YES (article page with legislative history; the sub-section listing page returns only the first paragraph).
- Used for: the "*contenu détaillé et personnalisé*" voiding rule for advance-*prestations* clauses; the **85 %** PB quota with its pro-rating by mathematical provisions and deduction of technical interest; the attribution of the current wording to loi n° 2013-672 du 26 juillet 2013 arts. 73–74; and the recorded caveat that the quota is drafted for the *prestations* form and may not reach a pure capital contract.

(frlib-obseques-r4)=

### R4. Légifrance, CGCT art. L. 2223-34-2 (version of 14 May 2009)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000020625551/2026-08-25
- Retrieved: YES.
- Used for: the national file of advance-*prestations* contracts, created by loi n° 2009-526 du 12 mai 2009 art. 25 — the statutory counterpart of the AGIRA search at [R19].

(frlib-obseques-r5)=

### R5. Légifrance, CGCT art. L. 2223-35-1 (in force since 16 December 2005)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006390319
- Retrieved: YES (article page with legislative history).
- Used for: the lifelong freedom to change the nature of the funeral, the mode of burial, the service content, the designated operator and any *mandataire*; the limit of chargeable amounts to the general conditions' management charges; the **15000 € fine per infringement**; and Légifrance's own attribution to loi n° 2005-1564 du 15 décembre 2005 art. 15 (V), which conflicts with the widespread attribution recorded at [R21].

(frlib-obseques-r6)=

### R6. Légifrance, LOI n° 2008-1350 du 19 décembre 2008 relative à la législation funéraire ("loi Sueur")
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000019960926
- Retrieved: YES (JORF consolidated text).
- Used for: what the loi Sueur actually contains — art. 7 amending L. 2223-33, **art. 8 adding the legal-rate interest floor on the capital paid by the subscriber of an advance-*prestations* contract**, and art. 9 creating the national file; and, equally, what it does **not** contain, namely the detailed-description and freedom-to-modify obligations.

(frlib-obseques-r7)=

### R7. Légifrance, Code des assurances, Section I "Dispositions générales" (arts. L. 132-1 à L. 132-27-2)
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073984/LEGISCTA000006174038/
- Retrieved: YES (fetched twice; the second fetch returned full text for L. 132-13 and L. 132-20).
- Used for: art. L. 132-1 (assurance on one's own head, the legal form of the product); L. 132-3 (prohibited lives, premiums fully refunded); L. 132-5-1 (30-day *renonciation*); L. 132-13 (the death capital outside *rapport à succession* unless premiums were "*manifestement exagérées eu égard à ses facultés*"); and L. 132-20 (no action to compel payment; 10 days then 40 days, then termination or *réduction*) — the statutory basis of the non-payment path in the recursion.

(frlib-obseques-r8)=

### R8. Légifrance, Code des assurances art. L. 132-5 (version of 1 January 2016)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006792939
- Retrieved: YES (full verbatim text).
- Used for: the requirement that the contract state the conditions of allocation of technical and financial profits — the hook art. L. 2223-34-1 CGCT hangs its PB rule on — and the requirement to state how the capital is revalued between death and payment, with a floor rate fixed by decree.

(frlib-obseques-r9)=

### R9. Légifrance, Code des assurances art. L. 132-22 (version of 24 October 2024)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006793125
- Retrieved: YES (key provisions returned; long article, only the material paragraphs).
- Used for: the annual statement of surrender value, guaranteed return and technical and financial profit sharing — the disclosure the insurer notices implement, cross-referenced by art. L. 2223-34-1 CGCT.

(frlib-obseques-r10)=

### R10. Légifrance, Code des assurances art. L. 132-23 (version of 14 June 2026)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006793141
- Retrieved: YES (full verbatim text).
- Used for: the rule that only temporary death assurance and annuities in payment may carry neither *réduction* nor *rachat*, so that a whole-life funeral contract necessarily carries both — the article that disposes of the assumption that lifetime-premium contracts have no surrender value; and the insurer's power to substitute *rachat* for *réduction* below a decreed threshold.

(frlib-obseques-r11)=

### R11. Comité consultatif du secteur financier, "Avis du 8 octobre 2024 — Les contrats d'assurance obsèques"
- Publisher: CCSF, hosted by Banque de France
- URL: https://www.banque-france.fr/system/files/import/ccsf/ccsf_avis_contrats_obseques.pdf (also served with the query string `?v=1738946978`)
- Retrieved: **NO — HTTP 403 Forbidden on three attempts, on both URL forms.**
- Used for: nothing directly. It is listed because every statement about the CCSF commitments in these documents is attributed to it and is therefore tagged **[unverified]**, resting on the four secondary summaries [R13]–[R16] and on the sixteen standardised tables actually retrieved.

(frlib-obseques-r13)=

### R13. MoneyVox, "Assurance obsèques : ce qui va changer en juillet pour votre contrat"
- Publisher / type: MoneyVox — **secondary source**
- URL: https://www.moneyvox.fr/assurance/actualites/104034/assurance-obseques-ce-qui-va-changer-en-juillet-pour-votre-contrat
- Retrieved: YES.
- Used for: the content of the CCSF commitments effective 1 July 2025 — the standardised table for entry ages 50 / 60 / 70 at a 5000 € capital, the **one-year cap on the *délai de carence*** against previously observed two-year periods, the obligation to offer temporary alternatives, the limitation of exclusions, and the non-binding character of the avis. All **[unverified]** against [R11].

(frlib-obseques-r14)=

### R14. La finance pour tous (IEFP), "Assurances obsèques : une amélioration des pratiques attendue pour juillet 2025" (31 October 2024)
- Publisher / type: IEFP — **secondary source**
- URL: https://www.lafinancepourtous.com/2024/10/31/assurances-obseques-une-amelioration-des-pratiques-attendue-pour-juillet-2025/
- Retrieved: YES.
- Used for: the market figures attributed to the CCSF avis — more than 5.3 million contracts in force in 2023, a 1.8 bn € portfolio, about 190 000 deaths covered a year, an average capital of about 5000 € — and the two contract structures and three premium modes. All **[unverified]** against [R11].

(frlib-obseques-r15)=

### R15. Planète CSCA, "Le CCSF adopte un avis pour une meilleure lisibilité et un renforcement des garanties des contrats d'assurance obsèques"
- Publisher / type: Planète CSCA (brokers' federation) — **secondary source**
- URL: https://www.planetecsca.fr/actualites/pratiques-du-metier/le-ccsf-adopte-un-avis-pour-une-meilleure-lisibilite-et-un-renforcement-des-garanties-des-contrats-dassurance-obseques/
- Retrieved: YES.
- Used for: 1.8 bn € of premiums and 539 000 new policies in 2023; the described contents of the standardised table and the requirement that it be downloadable; and the same commitments as [R13]. All **[unverified]** against [R11].

(frlib-obseques-r16)=

### R16. Institut national de la consommation, "Contrats d'assurance obsèques : pour une meilleure lisibilité et un renforcement des garanties"
- Publisher / type: INC — **secondary source**
- URL: https://www.inc-conso.fr/content/assurance/contrats-dassurance-obseques-pour-une-meilleure-lisibilite-et-un-renforcement-des-garanties
- Retrieved: YES, but thin (no figures).
- Used for: the scope of the CCSF work — individual contracts and group contracts with individual membership, on a **whole-life** guarantee, excluding savings contracts and fixed-term guarantee contracts. **[unverified]** against [R11].

(frlib-obseques-r17)=

### R17. service-public.gouv.fr, "Qui doit payer les frais d'obsèques ?" (fiche F17059, verified 1 January 2026)
- Publisher / type: DILA; public information sheet
- URL: https://www.service-public.gouv.fr/particuliers/vosdroits/F17059
- Retrieved: YES.
- Used for: the estate-side scale figures — up to **5965 €** drawable from the deceased's bank account for funeral costs under art. L. 312-1-4 CMF, and **1500 €** of funeral expenses deductible from the estate; and the characterisation of the *contrat obsèques* as a *prévoyance* contract with single, temporary or lifetime premiums.

(frlib-obseques-r19)=

### R19. service-public.gouv.fr / AGIRA, "Demander la recherche d'un contrat d'assurance obsèques" (service R63577)
- Publisher / type: DILA / AGIRA; online service description
- URL: https://www.service-public.gouv.fr/particuliers/vosdroits/R63577
- Retrieved: YES.
- Used for: the AGIRA search service and the **3 business day** deadline for an insurer to respond — the operational counterpart of the national file created by art. L. 2223-34-2 CGCT [R4].

(frlib-obseques-r20)=

### R20. service-public.gouv.fr, "Obsèques : une notice d'information obligatoire pour mieux accompagner les familles" (actualité A19044)
- Publisher / type: DILA; news item
- URL: https://www.service-public.gouv.fr/particuliers/actualites/A19044
- Retrieved: YES.
- Used for: **décret n° 2026-770 du 13 août 2026** and the arrêté of the same date (art. R. 2223-24-1 CGCT), obliging every funeral operator to hand families a standardised neutral information notice from **1 October 2026** — a duty on the operator, not on the insurer.

(frlib-obseques-r21)=

### R21. AFIF, "La souscription d'un contrat de prévoyance décès obsèques — explications et conseils" (11 pp.)
- Publisher / type: Association française d'information funéraire, association loi 1901 — **consumer body, secondary for legal text**
- URL: https://www.afif.asso.fr/francais/conseils/prevoyance.obseques.pdf
- Retrieved: YES (PDF downloaded, full text extracted).
- Used for: the two contract categories (*prestations* versus capital) and the three settlement forms (*prime unique*, *primes périodiques viagères*, *primes périodiques durant une période déterminée*); the warning that lifetime premiums may total several times the price of the funeral; the market description of the *délai de carence* and of the accident definition excluding myocardial infarction, coronary and cardio-vascular conditions and emotional shock; the prohibition since décret n° 95-653 du 9 mai 1995 on a funeral operator holding client money in advance; the registration obligation for funeral firms selling insurance; and the attribution of L. 2223-34-1 to loi n° 2004-1343 du 9 décembre 2004, with the recorded conflict on L. 2223-35-1 against [R5].

(frlib-obseques-r22)=

### R22. Boursorama, "Quel est le coût moyen des obsèques et comment le réduire ?" (16 October 2025)
- Publisher / type: Boursorama, reporting a Silver Alliance study — **secondary source**
- URL: https://www.boursorama.com/budget/actualites/quel-est-le-cout-moyen-des-obseques-et-comment-le-reduire-97ff12aed4ecf90a41dedadec558e76d
- Retrieved: YES (the underlying study itself was not retrieved).
- Used for: the average French funeral cost of **4730 € in 2025**, split **5044 € inhumation / 4434 € crémation** — the secondary corroboration of the 5000 € benchmark that seven insurers assert independently.

(frlib-obseques-r23)=

### R23. Légifrance, Code de la mutualité (table of contents only)
- URL: https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006074067
- Retrieved: **PARTIAL — the code's landing page loads and confirms the code identity, but none of the individual articles could be retrieved:** L. 223-8, L. 221-18, L. 223-19-1, **L. 223-20-1** (the 2.5 %-of-capital acquisition-charge cap quoted by [S8]), L. 223-22, L. 223-22-1, L. 223-25-4 and R. 223-9.
- Used for: recording that failure. Everything attributed to those articles in these documents rests on the insurer notices [S8] [S9], and the article texts themselves are **[unverified]**.

(frlib-obseques-r24)=

### R24. Légifrance, Code général des impôts (table of contents only)
- URL: https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006069577
- Retrieved: **PARTIAL — the code's landing page loads (dated 25 August 2026) but arts. 990 I, 757 B and 125-0 A were never read:** the intermediate table-of-contents page exceeded the fetcher's 10 MB content limit and the article search is JavaScript-rendered.
- Used for: recording that failure. The *applicability* of arts. 990 I and 757 B to these contracts is verified from four primary documents [S1] [S9] [S11] [S13]; the numerical thresholds and rates are **[unverified]** in this product's research file and are carried in the documents on the cross-product entry [REG-R41] alone.

---

## Cross-product references ([REG-R#])

Cited with the [REG-R#] prefix to avoid collision with this product's own R-numbering. Full
annotated entries — titles, publishers, URLs, retrieval markers, access date 2026-08-26 — live
in `references/regulatory-and-actuarial-references.md`, whose R1–R49 numbering is frozen.
Entries cited by the two documents in this directory:

| Tag | Short title | Gloss — why these documents cite it | Retrieval status per that file |
|---|---|---|---|
| REG-R1 | Directive 2009/138/CE — Solvabilité II | the valuation basis these cash flows feed | not fetched (EUR-Lex WAF challenge) |
| REG-R2 | Règlement délégué (UE) 2015/35 | contract boundaries, expenses and shocks were never read, so every such figure is [std] | not fetched (same challenge) |
| REG-R4 | EIOPA — Solvency II framework page | the authority on which the best-estimate-plus-risk-margin rule is stated | fetched |
| REG-R5 | EIOPA — risk-free interest rate term structures | the curve the best estimate discounts at; this model stops short of it | fetched |
| REG-R6 | C. ass. art. R. 343-3 — the eleven technical provisions | defines the *provision mathématique* including future management costs — the quantity the surrender value equals | fetched |
| REG-R14 | C. ass. art. L. 331-3 — the PB obligation | the statutory source of the revalorisation | fetched (version to 1 January 2016; current placement [unverified]) |
| REG-R15 | C. ass. arts. A. 132-10 to A. 132-15 — compte de participation | the arithmetic of the minimum PB, determined globally not contract by contract | fetched |
| REG-R16 | C. ass. art. A. 132-16 — PPB eight-year rule | the release horizon on profit shares not yet credited to the capital | fetched |
| REG-R17 | C. ass. arts. A. 132-1 / A. 132-1-1 — maximum technical rate | caps any guaranteed rate inside the tariff at min(3.5 %, 60 % of TME) for periodic premiums | fetched |
| REG-R22 | Arrêté du 20 décembre 2005 — TH 00-02 / TF 00-02 | the homologated non-annuity tables, cited by name and never shipped | fetched |
| REG-R23 | C. ass. art. A. 335-1 and its Annexe | which table a tariff may use, the *décalage d'âge* schedules, and the ages 0–112 tabulation that fixes omega | fetched (version to 1 January 2016; current placement [unverified]) |
| REG-R24 | INSEE — mortalité, espérance de vie | the only freely redistributable French mortality series, and the source of the [std] decrement proxies | fetched |
| REG-R29 | C. ass. arts. L. 132-5-1 / L. 132-5-2 — renonciation | 30 days, full refund, extension to eight years where the notice was not delivered | fetched |
| REG-R30 | C. ass. arts. A. 132-4 / A. 132-8 — note d'information, encadré | requires charge **maxima** to be disclosed, not limited — why every expense level is [std] | fetched |
| REG-R31 | C. ass. arts. L. 132-21 / L. 132-22 / L. 132-23-1 | the two-month surrender settlement and the death-payment clock the post-mortem revalorisation runs against | fetched |
| REG-R38 | CGCT art. L. 2223-33-1 — funeral financing formulas | the full verbatim earmarking sentence; primary for this product | fetched |
| REG-R39 | Loi n° 2014-617 (loi Eckert) | unclaimed proceeds to the Caisse des dépôts after ten years, revalorisation continuing until deposit | fetched |
| REG-R41 | CGI arts. 990 I and 757 B — death benefits | the verified thresholds this product's own [R24] could not fetch | fetched |
| REG-R44 | Institut des actuaires — NPA 2 (*Modèles actuariels*) | the recommended-practice standard this documentation sits under | fetched |
| REG-R45 | IFRS 17 *Insurance Contracts* | fulfilment cash flows plus CSM, no French carve-out | fetched (landing page) |
| REG-R49 | France Assureurs — chiffres clés and 2025 market review | records that the widely quoted 5.7 million *contrats obsèques* figure could not be sourced | fetched |

---

## Provenance note

Extraction details live in `_research/obseques.md`. That file records which facts came from which
source; the [unverified] flags carried into these documents (everything attributed to the CCSF
avis, the CGI thresholds, the Code de la mutualité article texts, the PFG snippet, the simple-
versus-compound reading of the 1 % uprating wording, the inference of premium cessation near
age 90 from [S6], and the mutualité-code article numbers); the failed fetches ([R11] and the
dropped R12 — HTTP 403 on the CCSF avis and its press release; the dropped S17 — HTTP 410 Gone;
the dropped S18 and [S19] — HTTP 403; the dropped R25 — request rejected); the partial fetches
([R23] and [R24]); and the table-extraction artefacts, of which four are material — a
thousands-separator loss in one worked grid whose figures were reconstructed from the annual
premium and are internally consistent, one illegible cumulative figure that is therefore not
quoted, one age-60 annual premium that is omitted rather than guessed, and one row of a
standardised table that extracted with no figures in any column. Every euro figure quoted in
these documents appeared verbatim in the extracted text of a retrieved document, or is derived
by stated arithmetic from figures that did.

Two structural cautions from the research file are carried into the documents rather than
buried here. The retrieved documents span 26/10/2023 to 01/07/2026, and where they disagree the
difference may be distribution-specific rather than a change over time. And the standardised
tables are illustrations, not contracts: each states that it has no contractual value and that
its surrender values exclude the *participation aux bénéfices*.

The cross-product bibliography `references/regulatory-and-actuarial-references.md` (accessed
2026-08-26; research provenance in `_research/regulatory-actuarial.md`) plays the same role for
[REG-R#] tags. Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md`
are introduced at drafting and are attributable to no source — in this product they include
every behavioural and expense assumption without exception, because no public French source
gives a lapse, surrender, paid-up or guaranteed-issue mortality figure for a *contrat obsèques*.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R11]: #frlib-obseques-r11
[R13]: #frlib-obseques-r13
[R16]: #frlib-obseques-r16
[R19]: #frlib-obseques-r19
[R21]: #frlib-obseques-r21
[R23]: #frlib-obseques-r23
[R24]: #frlib-obseques-r24
[R4]: #frlib-obseques-r4
[R5]: #frlib-obseques-r5
[REG-R38]: #frlib-reg-r38
[REG-R41]: #frlib-reg-r41
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
