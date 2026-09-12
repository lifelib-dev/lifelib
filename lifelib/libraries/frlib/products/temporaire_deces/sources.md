# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/temporaire-deces.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are omitted,
so the numbering has gaps: **S14** (Abeille Assurances comparison page — HTTP 403 on two
attempts, nothing citable), **R22** (France Assureurs home page — the assurance vie monthly
figure it carries is cited from [REG-R49] instead) and **R23** (economie.gouv.fr AERAS page,
HTTP 403; service-public fiche F2377, HTTP 404 after redirect — no official government-portal
description of the product exists in this file) are **not cited** by `product-spec.md` or
`technical-notes.md` and are therefore absent below. Access date for all sources: **2026-08-26**.
No sources were newly added at drafting. Cross-product [REG-R#] tags are listed in their own
section at the end.

---

## Primary product sources

(frlib-temporaire_deces-s1)=

### S1 — MAAF Vie, "Assurance décès — Notice d'information" (Réf. TDR. 014-06/2026)
- Publisher / doc type: MAAF Vie (SA, RCS Niort 337 804 819); *notice d'information* for a *contrat d'assurance de groupe sur la vie à adhésion facultative*, group contract n° 02120 subscribed by ANS Vie-Covéa, 22 pp.; tax content stated in force at 1 January 2026
- URL: https://www.maaf.fr/fr/files/live/sites/maaf/files/DOCUMENTS/Vie_quotidienne/CG/MAAF_Conditions_generales_Assurance_deces_2313.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: the attained-age revision rule; *branche 20*; the group wrapper; entry 18–75 and cessation at 85; PTIA/death non-cumulation; the **full fractionation and *frais d'échéance* table** and its 9,61 € worked example; the 1,30 € association subscription; PASS indexation; global participation aux bénéfices; the 990 I / 757 B tax mechanics and the *prélèvements sociaux* exclusion; unclaimed-capital and prescription timers; the 30-day termination right on an insurer-decided increase

(frlib-temporaire_deces-s2)=

### S2 — Macif, "Notice d'information — Garantie Décès, Capital forfaitaire" (garanties en vigueur au 1er janvier 2019)
- Publisher / doc type: Prévoyance Aésio Macif (insurer); Macif and Macif-Mutualité (subscribers of group contracts n° 219.002-A and -B); *notice d'information* for a *contrat d'assurance collectif à adhésion facultative*, 21 pp.
- URL: https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_prevoyance/PAM/NID_Deces_20190708.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: the self-description as a *contrat temporaire décès*; **PTIA as an anticipated payment due only if the insured is alive at payment**; PTIA cessation five years before death cessation (75 vs 80); the *différence de millésime* worked example (2019 − 1967 = 52); annual cotisation evolving with age and revalorisation; the 60-day / 76 000 € provisional accident cover; suicide within 12 months; underwriting outcomes; in-force re-rating on a change of occupation or sport; the 3 450 € Sécurité sociale *capital décès*

(frlib-temporaire_deces-s3)=

### S3 — MAIF VIE, "Assurance décès — Rassurcap Solutions, Note d'information"
- Publisher / doc type: MAIF VIE (SA, RCS Niort 330 432 782); *note d'information* for an **individual** contract, 24 pp. Retrieved via a third-party mirror (coover.fr) because MAIF's own contractual-documentation host was not reachable. **Vintage 2019–2021** — its internal worked examples are dated April/September 2019
- URL: https://www.coover.fr/wp-content/uploads/2021/08/assurance-deces-maif-rassurcap-solutions.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: **the representative design and the only complete published attained-age rate card in the corpus** (ages 18–74, reproduced in `technical-notes.md`), with the carrier's own two worked examples (20 000 € at 34 → 30 €; 150 000 € at 49 → 900 €); the individual annual contract renewed by *tacite reconduction*; entry ≤ 65, death cover to the échéance after 75, IPA/PTIA to the échéance after 65; minimum capital 20 000 €; the four formality-free increases; the 30-day / 15 000 € provisional accident cover; payout modes and the 3 % annuity conversion charge; premium cessation at death or IPA; the 305 € declaration duty

(frlib-temporaire_deces-s4)=

### S4 — MAIF, "Assurance Décès : Protégez vos proches" (product page, Rassurcap Solutions)
- Publisher / doc type: MAIF; insurer product page, current edition
- URL: https://www.maif.fr/famille-vie-quotidienne/assurance-deces
- Retrieved: YES
- Used for: the current headline parameters of the same product as S3 — minimum capital 20 000 €, simplified underwriting to age 40 for up to 250 000 €, maximum subscription age 65, the **6,29 €/month at age 35 for 40 000 €** price point that evidences rate drift against the S3 grid, and the explicit "recalcul chaque année"

(frlib-temporaire_deces-s5)=

### S5 — MAIF, consumer guide pages "Assurance décès à fonds perdus" and "Fin du contrat d'assurance décès"
- Publisher / doc type: MAIF; two insurer consumer-guide pages (dated 31 March 2023 and 9 August 2018)
- URL: https://www.maif.fr/famille-vie-quotidienne/guide-assurance-deces/a-fonds-perdus and https://www.maif.fr/famille-vie-quotidienne/guide-assurance-deces/fin-de-contrat-assurance-deces
- Retrieved: YES (both)
- Used for: the *fonds perdu* character in an insurer's own words — "les cotisations versées restent acquises à l'assureur" — and the contrast with a *vie entière* contract, which may carry a *tableau de rachat* where a temporaire may not; restates the simplified-underwriting thresholds

(frlib-temporaire_deces-s6)=

### S6 — Mutex, "Assurance Décès — Conditions générales / Notice d'information" (doc 20318)
- Publisher / doc type: Mutex; *conditions générales* / *notice d'information*, group contract with voluntary membership, 16 pp.
- URL: https://www.mutex.fr/app/uploads/2022/06/20318_-_assurance_deces_-_conditions_generales.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: **the only published numeric formalités-médicales grid** (≤ 40 000 € and ≤ 50 → no formality but a 12-month *délai d'attente* with return of cotisations; > 40 000 € → *questionnaire médical*, no waiting period; > 50 → *Déclaration de Bonne Santé*); entry 18–80, cessation 85 death / 80 PTIA; PTIA compulsorily attached to the death cover and terminating the adhesion; the "BON POUR ACCORD" *surcotisation* procedure within 15 days; repricing on age, revalorisation, legislation **and the results of the death guarantees**; the 10-day / LRAR / 40-day non-payment path

(frlib-temporaire_deces-s7)=

### S7 — AXA France Vie / ANPERE, "Prévoyance — Notice d'Information Avizen"
- Publisher / doc type: AXA France Vie and AXA Assurances Vie Mutuelle; subscriber ANPERE; *notice d'information* for a *contrat d'assurance de groupe à adhésion facultative*, 40 pp. Retrieved via a third-party mirror. **Vintage: the tax section states the regime in force at 01/09/2013 — its structural clauses are used here, its tax figures are not**
- URL: https://guide.reassurez-moi.fr/guide/wp-content/uploads/2018/12/conditions-generales-assurance-deces-axa.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: **"Article 13 - Rachat et réduction. Votre adhésion ne comporte ni valeur de rachat, ni valeur de réduction"**; IPT as the acceleration, ceasing at 67 against death cover to 85; the *capital décès double garantie* second decrement; *double effet*; the *rente éducation* 100/125/150 % steps and the *rente décès* halved at 65; pricing by age, occupational tariff group and smoker status; the art. L. 132-26 age-error rule; suicide "conscient ou inconscient"; premium cessation at death or IPT; PASS indexation ceasing at 70; the 15-day termination right on a tariff change

(frlib-temporaire_deces-s8)=

### S8 — ANTARIUS (Société Générale group), "Assurance Temporaire Décès — Document d'information sur le produit d'assurance" (Antarius Protection Premium, Série C, février 2018)
- Publisher / doc type: ANTARIUS SA (SIREN 402 630 826), distributed through Crédit du Nord and associated banks; **IPID**, 2 pp., release code T3_18_V17.1_20180926.00
- URL: https://www.assurances.societegenerale.com/fileadmin/2023/IPID/Antarius/IPID_APP_022018.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: the *bancassurance* variant — cover conditional on holding a bank account at the group and on French/Monaco tax residence, **all guarantees ceasing if either condition fails**; entry 18 to under 66, death cover to the anniversary after 70, PTIA to the anniversary after 65; capital 100 000 – 1 000 000 €; the *Double Effet* rider capped at 500 000 €; the 10 % / 10 000 € *avance*; first-year suicide exclusion; suicide clause running from start **or restart**

(frlib-temporaire_deces-s9)=

### S9 — MUTUALP / mutuelle LA FRONTALIÈRE, "Notice « GARANTIE DÉCÈS » — Notice d'information valant Conditions Générales au 1er janvier 2023" (n° 06015000005/01)
- Publisher / doc type: MUTUALP (insurer, Livre II du Code de la mutualité); mutuelle LA FRONTALIÈRE (subscriber, SIREN 421110305); *notice d'information valant conditions générales*, 9 pp.
- URL: https://www.mutuelle-lafrontaliere.fr/storage/app/media/documents%20pr%C3%A9voyance/NOTICE%20DECES%20MUTUALP_LA%20FRONTALIERE_2023.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: the *Code de la mutualité* form of the same product, self-described as "de type « assurance temporaire décès »"; **"Le contrat ne comprend pas de faculté de rachat"** and **"Le contrat ne prévoit pas de participation aux bénéfices"**; the 3-month *délai d'attente*; base capital 6 097,96 € to a 45 000 € ceiling; accidental supplement at **+50 %**; cessation at 31 December of the year of the 65th birthday; **no PTIA cover**; cotisations set each year by attained age changing on 1 January; the 30-day *mutualité* suspension timer

(frlib-temporaire_deces-s10)=

### S10 — MetLife France, "Assurance décès : protéger sa famille" (product page)
- Publisher / doc type: MetLife France; insurer product page (no page date shown)
- URL: https://www.metlife.fr/assurance-prevoyance/assurance-deces/
- Retrieved: YES
- Used for: the widest envelope in the corpus — subscription 18–84, temporary death cover to 90, capital to 50 M€ death and 20 M€ PTIA; pricing on age, health, occupation and smoker status with non-smoker status revisable after 12 months; and the **8,24 €/month "in year one" for a 40-year-old non-smoker with 50 000 €** price point, whose own wording signals annual revision

(frlib-temporaire_deces-s11)=

### S11 — MetLife France, "Assurance décès à fonds perdus" (guide page)
- Publisher / doc type: MetLife France; insurer guide page
- URL: https://www.metlife.fr/assurance-prevoyance/assurance-deces/fonds-perdu/
- Retrieved: YES
- Used for: a second insurer's own definition of the *fonds perdu* character — if death does not occur during cover, "les cotisations auront été versées « pour rien »" — and the contrast with the *vie entière* contract, which permits partial or total recovery through a surrender clause at a higher premium

(frlib-temporaire_deces-s12)=

### S12 — MACSF, "Plan de prévoyance — libéraux" (product page)
- Publisher / doc type: MACSF; insurer product page. **The three profession-specific DIPA PDFs it links were NOT retrieved** — the page exposes only truncated `/content/download/...` paths, so the parameters below are recorded at page level with no capital amounts, age tables or premium structure
- URL: https://www.macsf.fr/nos-produits-services/sante-prevoyance/prevoyance/plan-de-prevoyance/plan-de-prevoyance-liberaux
- Retrieved: YES (page only)
- Used for: the **triplement accidentel** variant — capital doubled for an accident and **tripled** for a road-traffic accident, terrorism, an *attentat* or an *agression*; IFTD as the PTIA acceleration under another name; entry to the day before the 57th birthday (50th for *infirmières*), i.e. profession-segmented age limits

(frlib-temporaire_deces-s13)=

### S13 — La Banque Postale, "Assurance temporaire décès" (guide page, 31/05/2023)
- Publisher / doc type: La Banque Postale; insurer/bank guide page
- URL: https://www.labanquepostale.fr/particulier/accompagner/actualites-et-conseils/actus/assurance-temporaire-deces.html
- Retrieved: YES
- Used for: the annual contract with *tacite reconduction* as the norm, with some contracts extending to 5 years — a claim **not** confirmed against any insurer contract document and therefore carried as [unverified] in the product documents

(frlib-temporaire_deces-s15)=

### S15 — Previssima, "Qu'est-ce qu'une assurance temporaire décès ?" (updated 11 February 2025)
- Publisher / doc type: Previssima, a French insurance and social-protection reference site — **secondary**, not a product document; reference article
- URL: https://www.previssima.fr/question-pratique/quest-ce-quune-assurance-temporaire-deces.html
- Retrieved: YES
- Used for: the **capital constant / capital décroissant** distinction and the statement that the decreasing form is "common in loan insurance"; and "Si le risque garanti ne survient pas pendant cette période, aucune somme n'est versée"

(frlib-temporaire_deces-s16)=

### S16 — Meilleurtaux, "Focus assurance temporaire décès" (page dated 22 June 2026)
- Publisher / doc type: Meilleurtaux, a broker — **secondary**, not a product document; broker guide page
- URL: https://www.meilleurtaux.com/comparateur-assurance/assurance-deces/guide-assurance-deces/focus-assurance-temporaire-deces.html
- Retrieved: YES
- Used for: the *fonds perdus* statement "aucun capital n'est versé et les cotisations déjà payées ne sont pas remboursées"; and the 10/15/20-year terms mentioned alongside the annual form, carried as [unverified] because the page says nothing about the premium being level

---

## Regulatory and actuarial references (product research numbering)

(frlib-temporaire_deces-r1)=

### R1 — Code des assurances, art. L. 132-7 (suicide)
- Publisher: Légifrance. **Version en vigueur : 20 août 2026**, modified by LOI n° 2026-794 du 18 août 2026 – art. 18 (V)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006792964
- Retrieved: YES (two independent fetches, consistent)
- Used for: the first-year nullity of the death cover for suicide, cover from the second year, and the clock restarting on the increment after any increase; the alinéa 4 immediate cover confined to principal-residence loan cover; and the new alinéa bringing death by *aide à mourir* within the cover from 20 August 2026, which no retrieved product document yet reflects

(frlib-temporaire_deces-r2)=

### R2 — Code des assurances, art. R. 132-5 (the suicide-cover ceiling)
- Publisher: Légifrance. Version en vigueur : 5 avril 2002
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006811988
- Retrieved: YES
- Used for: the figure that makes L. 132-7 alinéa 4 operative — "Le plafond … ne peut être inférieur à 120 000 Euros" — and, by its scope, the conclusion that it does **not** reach a standalone temporaire décès

(frlib-temporaire_deces-r3)=

### R3 — Code des assurances, art. L. 132-23 (no *réduction*, no *rachat*)
- Publisher: Légifrance. Version en vigueur : 14 juin 2026
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038837141
- Retrieved: YES
- Used for: the single article that removes every cash value from this product — "Les assurances temporaires en cas de décès … ne peuvent comporter ni réduction ni rachat" — and hence the absence of any account-value or surrender state variable and the structural zero of `claims_lapse`

(frlib-temporaire_deces-r4)=

### R4 — Code des assurances, art. A. 132-18 (tariff bases: technical rate and mortality tables)
- Publisher: Légifrance. Version en vigueur : 7 septembre 2017 (arrêté du 14 août 2017 – art. 1); the full French text is additionally reproduced verbatim inside R13
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514715
- Retrieved: YES
- Used for: the two admissible families of mortality table and the certified-experience-table route; the "most prudent tariff" rule where a single family-(a) table is used; the *décalage d'âge* requirement, which the article confines to *contrats **en cas de vie*** other than annuities and which therefore does **not** reach a temporaire décès (values **not** retrieved either — the Légifrance page carries only a pointer to the JO facsimile); the *méthode forfaitaire* permitted for annually cancellable collective death contracts; and the [unverified] status of art. A. 132-18-1, read only from a section listing

(frlib-temporaire_deces-r5)=

### R5 — Code des assurances, art. A. 132-1 (maximum technical interest rate)
- Publisher: Légifrance. Version en vigueur : 7 septembre 2017
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035514601
- Retrieved: YES
- Used for: the 75 %-of-TME cap, the min(3,5 %, 60 % TME) cap beyond eight years, and the clause binding contracts *à primes périodiques* "quelle que soit leur durée" — the one that reaches an annually renewable temporaire décès. The rate-step *barème* reported by secondary summaries was **not visible** in the retrieved text and is [unverified]

(frlib-temporaire_deces-r6)=

### R6 — Arrêté du 20 décembre 2005 relatif aux tables de mortalité (NOR ECOT0591210A)
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000636581
- Retrieved: YES
- Used for: the homologation of **TH 00-02** (male) and **TF 00-02** (female) with effect from 1 January 2006, their application to contracts other than *rentes viagères*, and the *décalage d'âge* wording later carried into A. 132-18. The tables themselves are cited by name and **never shipped** in this library

(frlib-temporaire_deces-r7)=

### R7 — Arrêté du 1er août 2006 portant homologation des tables de mortalité pour les rentes viagères
- Publisher: Légifrance (JORF)
- URL: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000820127
- Retrieved: YES
- Used for: the homologation of the generational **TGH05 / TGF05** from 1 January 2007 for annuity contracts — relevant to this product only where a death capital is converted into a *rente*

(frlib-temporaire_deces-r8)=

### R8 — Code des assurances, art. A. 335-1 and its annexe (abrogated)
- Publisher: Légifrance. In force 26 August 2006 → 1 January 2016; **abrogated by the arrêté du 28 décembre 2015** with effect from 1 January 2016
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019265297
- Retrieved: YES
- Used for: the fact that any citation of "A. 335-1" in a current French product document is a **legacy reference**, the operative successor being A. 132-18 [R4]

(frlib-temporaire_deces-r9)=

### R9 — Institut des actuaires, "Notice d'utilisation — Tables de mortalité TH 00-02 et TF 00-02"
- Publisher / doc type: Institut des actuaires; professional notice, 17 pp. Heads itself "ARRÊTÉ DU 29 DÉCEMBRE 2005" against Légifrance's 20 December [R6]; both agree the tables took effect 1 January 2006, and the discrepancy was **not** resolved
- URL: https://www.institutdesactuaires.com/docs/2007017232113_NOTICETHTF0002.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: the profession's recommendation that the *décalages d'âge* be applied **to the q(x), not to the l(x)**, because shifting l(x) produces erratic q(x) growth and hence erratic provisions; and the confirmation that TH/TF 00-02 are period tables built on INSEE data and do not apply to *rentes viagères*. Its numeric table extracts are **not reproduced** in this library

(frlib-temporaire_deces-r10)=

### R10 — Code des assurances, art. L. 111-7 (unisex pricing)
- Publisher: Légifrance. Version en vigueur : 24 octobre 2024 (LOI n° 2023-973 du 23 octobre 2023 – art. 35)
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027783391
- Retrieved: YES
- Used for: the prohibition of direct and indirect sex-based differences in premiums and benefits, and the surviving derogation limited to contracts and group-contract adhesions "conclus ou effectuées au plus tard le 20 décembre 2012" — hence unisex new business from 21 December 2012, and the reconciliation problem against the sex-specific homologated tables. The underlying CJEU case number is [unverified]

(frlib-temporaire_deces-r11)=

### R11 — Code des assurances, art. R. 343-3 (life technical provisions)
- Publisher: Légifrance. Version en vigueur : 1er janvier 2020
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039739686
- Retrieved: YES
- Used for: the definition of the *provision mathématique* as the difference between the present values of the two parties' commitments and its requirement to **include future management costs** equal to the tariff's *chargements de gestion*; the one-category rule; and the existence of a *provision d'égalisation* for group death business

(frlib-temporaire_deces-r12)=

### R12 — Code des assurances, art. R. 343-7 (provision pour risques croissants)
- Publisher: Légifrance. Version en vigueur : 10 juin 2024
- URL: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047658116
- Retrieved: YES
- Used for: the scope point that the PRC is defined for *maladie* and *invalidité* operations, **not** death — so the death-cover analogue is the R. 343-3 *provision mathématique*

(frlib-temporaire_deces-r13)=

### R13 — Institut des actuaires, "Provisions pour risques croissants — Guidelines" (assurance emprunteur working group, sub-group SGT4)
- Publisher / doc type: Institut des actuaires; professional guidance document, 43 pp.
- URL: https://www.institutdesactuaires.com/global/gene/link.php?doc_id=17428
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: the best public French treatment of how a death cover with a flat premium rate and rising mortality is reserved — "un montant de PRC est toujours constitué pendant la durée", and "la même provision de prime s'appelle PM en vie et PRC en non-vie"; the verbatim texts of A. 343-1-1 and ANC 2015-11 art. 142-3 (eight-year spreading of a basis change); the **60 % TH 00-02 / 40 % TF 00-02** unisex mix as observed market practice; technical rates of 0,5 % and 0 % in its own illustrations; the medical-selection abatement of 70 % / 50 % / 20 % over years 1–3; and the *capital initial* versus *capital restant dû* distinction that belongs to the borrower product

(frlib-temporaire_deces-r14)=

### R14 — Code général des impôts, art. 990 I (and 990 I bis)
- Publisher: Légifrance. Version date shown: 11 mars 2023
- URL: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069577/LEGISCTA000006162644/
- Retrieved: YES
- Used for: the 152 500 € per-beneficiary abattement and the 20 % / 31,25 % rates either side of 700 000 € of taxable share, and the spouse / PACS partner / sibling exemptions

(frlib-temporaire_deces-r15)=

### R15 — BOFiP, BOI-TCAS-AUT-60 (30 March 2023) — doctrine on the art. 990 I levy
- Publisher: Direction générale des finances publiques
- URL: https://bofip.impots.gouv.fr/bofip/1335-PGP.html/identifiant%3DBOI-TCAS-AUT-60-20230330
- Retrieved: YES
- Used for: **the scope statement this product needs** — the levy expressly reaches *assurance décès temporaire* and *assurance décès pure* where the beneficiary is designated *à titre gratuit*, and excludes contracts designated *à titre onéreux*, the paradigm being loan cover assigned to a lender; plus the post-70 art. 757 B rule and its 30 500 € abattement

(frlib-temporaire_deces-r16)=

### R16 — CNP Assurances, "Notice explicative : attestation sur l'honneur article 990 I du code général des impôts"
- Publisher / doc type: CNP Assurances (SA, RCS Paris 341 737 062); insurer tax-procedure notice, 2 pp., no document date printed
- URL: https://www.cnp.fr/media/fichiers/particuliers/faq/remplir-l-attestation-sur-l-honneur-etablie-en-application-de-l-article-990-i-du-code-general-des-impots
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: the levy stated in **capital** terms as an insurer applies it — 20 % between 152 500 € and 852 500 €, 31,25 % above 852 500 € — and the insurer's duty to withhold and remit, which is why the beneficiary files the *attestation sur l'honneur*

(frlib-temporaire_deces-r17)=

### R17 — Convention AERAS, version actualisée 2023
- Publisher / doc type: the State, banking and insurance federations and patient/consumer associations; inter-professional convention, 44 pp.
- URL: https://www.aeras-infos.fr/files/live/sites/aeras/files/contributed/docs/Convention%20AERAS%202023.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Used for: **the scope finding that matters most here** — AERAS applies to *prêts immobiliers*, *prêts professionnels* and *prêts à la consommation affectés ou dédiés*, and nothing in the retrieved text extends it to a standalone temporaire décès; plus the three examination levels, the age-71 and 420 000 € third-level conditions, the 17 000 € / 4-year / age-50 questionnaire waiver, the *écrêtement* income tests and the 1,4-point TEG cap, the five-year *droit à l'oubli*, and the *grille de référence* setting maximum surprimes per garantie; and the record that the *loi Lemoine* questionnaire removal is a **borrower** measure

(frlib-temporaire_deces-r18)=

### R18 — aeras-infos.fr, the convention's official site
- Publisher: signatories of the Convention AERAS
- URL: https://www.aeras-infos.fr/
- Retrieved: YES (partially — summary pages render; per-figure detail sits in the PDF at R17)
- Used for: confirmation that the 2023 version is current and carries an *avenant* signed **5 July 2024**

(frlib-temporaire_deces-r19)=

### R19 — Code général des impôts, art. 757 B (premiums paid after age 70)
- Publisher: Légifrance
- URL: **not resolved** — the article's Légifrance identifier could not be located without a web search, and no URL was guessed
- Retrieved: **NO.** Known reference only (`fetched_ok = false`)
- Used for: nothing substantive. It is cited in `product-spec.md` only to record that the product research did not reach the article, so that the 30 500 € abattement and the post-70 rule rest on [R15], [R16], [S1] and [S3] — and, at article level, on the cross-product entry [REG-R41], which **was** retrieved and closes this gap

(frlib-temporaire_deces-r20)=

### R20 — ACPR (Autorité de contrôle prudentiel et de résolution)
- Publisher: ACPR / Banque de France
- URL: https://acpr.banque-france.fr/ (and https://acpr.banque-france.fr/en)
- Retrieved: **NO — HTTP 403 Forbidden on both roots, on repeated attempts.** Known reference only (`fetched_ok = false`)
- Used for: nothing substantive. Cited in `product-spec.md` only to disclose that **no ACPR *analyse et synthèse* on prévoyance was retrieved**, and that the ACPR appears in these documents solely as the supervisory authority named in the notices [S1] [S2] [S6] [S9]

(frlib-temporaire_deces-r21)=

### R21 — France Assureurs, "Nos chiffres clés — L'assurance santé et prévoyance"
- Publisher: France Assureurs
- URL: https://www.franceassureurs.fr/nos-chiffres-cles/lassurance-sante-et-prevoyance/
- Retrieved: YES (headline figure only)
- Used for: **"40,3 Md€ Cotisations en assurance prévoyance en 2025"** — and, equally, for the disclosure that the page does **not** break the figure down by garantie, so there is no sourced size for the standalone temporaire décès segment

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product French reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R49, frozen;
research provenance in `_research/regulatory-actuarial.md`). Entries cited by the temporaire
décès documents:

- **REG-R1** — Directive 2009/138/CE (Solvabilité II). fetched_ok: **no** (EUR-Lex WAF challenge); all its article numbers are [unverified] in this library.
- **REG-R2** — Règlement délégué (UE) 2015/35. fetched_ok: **no** (same challenge) — which is why no contract-boundary rule, cost-of-capital rate or standard-formula shock here rests on a retrieved text.
- **REG-R3** — Directive (UE) 2025/2 (Solvency II review); new rules take effect 30 January 2027. fetched_ok: no.
- **REG-R4** — EIOPA Solvency II framework page: the verified carrier for the best-estimate-plus-risk-margin statement and the three-pillar structure. fetched_ok: yes.
- **REG-R5** — EIOPA risk-free interest rate term structures, published monthly. fetched_ok: yes.
- **REG-R6** — C. ass. art. R. 343-3, the eleven French life technical provisions. fetched_ok: yes.
- **REG-R10** — CMF art. L. 612-1, the ACPR as supervisor. fetched_ok: yes.
- **REG-R14** — C. ass. art. L. 331-3, the statutory participation aux bénéfices obligation. fetched_ok: yes.
- **REG-R17** — C. ass. arts. A. 132-1 / A. 132-1-1, maximum technical interest rate. fetched_ok: yes.
- **REG-R22** — Arrêté du 20 décembre 2005, homologation of TH 00-02 / TF 00-02 (non-annuity tables). fetched_ok: yes.
- **REG-R23** — C. ass. art. A. 335-1 and its Annexe: the two permitted table families, the most-prudent rule, the *méthode forfaitaire* for annually cancellable collective death contracts, and **the only retrieved *décalage d'âge* values** (TF 00-02 from −11 at ages 16–32 to 0 at 94+; TH 00-02 from −13 at ages 16–38 to −3 at 75+). fetched_ok: yes (served as the pre-2016 version).
- **REG-R24** — INSEE national mortality series: the intended base for a user-supplied replacement decrement table. The entry records that the INSEE page **states no licence or reuse conditions**; standard open-data terms are assumed there and that assumption is [unverified], so a user should confirm before redistributing derived CSVs. fetched_ok: yes.
- **REG-R29** — C. ass. arts. L. 132-5-1 / L. 132-5-2, the 30-day *renonciation*. fetched_ok: yes.
- **REG-R30** — C. ass. arts. A. 132-4 / A. 132-8, the *note d'information* and the one-page *encadré*. fetched_ok: yes.
- **REG-R31** — C. ass. arts. L. 132-21 / L. 132-22 / L. 132-23-1: the death-settlement clock (15 days to request documents, one month to pay from the complete file). fetched_ok: yes.
- **REG-R37** — France Assureurs, *Statistiques Convention AERAS 2023*: the only public French price point on rated lives (average 1,01 % of initial capital before *écrêtement*, 0,65 % after) and the death 65 % / PTIA 87 % no-surprime offer rates. fetched_ok: yes.
- **REG-R39** — Loi n° 2014-617 (loi Eckert): unclaimed life contracts transfer to the Caisse des dépôts after ten years, with revaluation continuing until deposit. fetched_ok: yes.
- **REG-R41** — CGI arts. 990 I and 757 B: **the retrieved article-level source for 757 B**, closing the gap left by [R19]. fetched_ok: yes.
- **REG-R44** — Institut des actuaires NPA 2, *Modèles actuariels* — the professional standard this library's model documentation sits under. fetched_ok: yes (NPA 4 not retrieved, [unverified]).
- **REG-R45** — IFRS 17 *Insurance Contracts*, effective 1 January 2023 with no French carve-out. fetched_ok: yes.
- **REG-R49** — France Assureurs chiffres clés: the assurance vie market scale used only as a comparator (€19,3 bn in June 2026). fetched_ok: yes.

---

## Provenance note

Extraction details — which fact was read from which document, section-level notes, and the
seventeen-item gaps-and-caveats register — live in `_research/temporaire-deces.md`. That file is
the citation ground truth for the S# and R# numbering used here. The caveats that most affect
what these product documents can claim are: **no level-premium French standalone contract was
found**, so the `constante` form is a **[std]** construction; **the published rate card [S3] is a
2019–2021 vintage** retrieved from a third-party mirror, usable for shape but not level; **the
*décalages d'âge* values annexed to the current art. A. 132-18 were not retrieved** [R4], with
the abrogated annexe's values available only through [REG-R23]; **the regulatory mortality tables
are cited, never shipped**, so every decrement in the model is a **[std]** proxy; **no French
insurer publishes a pricing basis, a *surprime* scale, a lapse rate or an expense loading**, so
every assumption in class (c) of the technical notes is **[std]**; **art. L. 132-7 changed on
20 August 2026** and no retrieved product document yet reflects it [R1]; and three official French
sources — the ACPR site [R20], the economie.gouv.fr AERAS page and the service-public fiche
(both R23) — returned errors, so **no official government-portal description of this product
appears anywhere in this file**.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-temporaire_deces-r1
[R15]: #frlib-temporaire_deces-r15
[R16]: #frlib-temporaire_deces-r16
[R19]: #frlib-temporaire_deces-r19
[R20]: #frlib-temporaire_deces-r20
[R4]: #frlib-temporaire_deces-r4
[R6]: #frlib-temporaire_deces-r6
[REG-R23]: #frlib-reg-r23
[REG-R41]: #frlib-reg-r41
[REG-R49]: #frlib-reg-r49
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
