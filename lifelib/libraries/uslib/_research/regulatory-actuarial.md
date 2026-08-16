# Regulatory and Actuarial Reference Library — U.S. Individual Life Insurance

Cross-product annotated bibliography supporting reference implementations of liability
cash flow projection models (term / whole life / UL / IUL / VUL / ULSG).

- Accessed: 2026-08-03 (all links checked on this date unless noted otherwise).
- Citation discipline: facts drawn from a document actually retrieved carry its [R#];
  claims from general knowledge are tagged [unverified]; failed or unverified links are
  flagged explicitly. No URL below is fabricated — every URL was either fetched
  successfully or is marked as not fetched.
- Note on NAIC documents: NAIC model law PDFs on content.naic.org fetch cleanly, but
  several content.naic.org HTML topic pages (e.g., CIPR topic pages) return HTTP 403 to
  automated clients; where that happened it is noted.

---

## 1. NAIC — Valuation, Nonforfeiture, Illustrations, and Actuarial Guidelines

### R1. Standard Valuation Law (Model #820)
- **Publisher:** National Association of Insurance Commissioners (NAIC)
- **URL:** https://content.naic.org/sites/default/files/model-law-820.pdf
- **Doc type:** model law (official NAIC model text, print incorporating the 2009 amendments; header "NAIC Model Laws, Regulations, Guidelines and Other Resources—July 2010")
- **Fetched:** yes (27-page PDF retrieved and read) [R1]
- **Annotation:** The enabling statute for statutory reserve valuation. Contains the
  classic formulaic-reserve machinery (minimum standard by calendar year of issue,
  Commissioners Reserve Valuation Method for life insurance and endowment benefits,
  minimum reserves, deficiency-reserve treatment when valuation net premium exceeds
  gross premium) plus, as amended in 2009, the sections that create principle-based
  reserving: Section 11 (Valuation Manual applies to policies issued on/after the VM
  operative date), Section 12 (requirements of a principle-based valuation), Section 13
  (experience reporting) and Section 14 (confidentiality) [R1]. The VM operative date
  was January 1, 2017 [unverified — widely documented but not stated in this print].
- **Matters for:** all products (term, WL, UL, IUL, VUL, ULSG) — it is the legal root of
  every statutory reserve a projection model must reproduce.

### R2. Standard Nonforfeiture Law for Life Insurance (Model #808)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-808.pdf
- **Doc type:** model law (print: "Model Laws…—January 2014")
- **Fetched:** yes (13-page PDF retrieved and read) [R2]
- **Annotation:** Sets the minimum cash surrender values and paid-up nonforfeiture
  benefits: the 60-day default/election mechanics, computation of cash surrender value
  and paid-up benefits, the adjusted-premium method (ordinary and industrial variants,
  and the nonforfeiture net level premium method), treatment of indeterminate premium
  plans, and the required smooth progression of cash values by duration [R2]. This 2014
  print ties its definitions to the "operative date of the valuation manual" under the
  2009 SVL amendments [R2]. Minimum nonforfeiture mortality/interest for new issues now
  comes through VM-02 of the Valuation Manual [R3].
- **Matters for:** whole life primarily (guaranteed CSV scale); term (why long-term
  guaranteed-premium term may generate nonforfeiture values); UL/IUL/VUL nonforfeiture
  is governed via Model #585's UL-specific adaptation (R6).

### R3. Valuation Manual, Jan. 1, 2026 Edition (VM-01, VM-02, VM-20, VM-31, VM-M, VM-G, VM-C, VM-V, …)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- **Doc type:** valuation manual, current edition (457-page PDF; "NAIC Adoptions through August 13, 2025"; initially adopted Dec. 2, 2012 with amendment adoptions each year through Aug. 13, 2025)
- **Fetched:** yes (retrieved; cover, adoption history, and full table of contents read) [R3]
- **Annotation:** The operative rulebook for statutory valuation of new business. The
  2026 edition contains: VM-01 (definitions), VM-02 (minimum nonforfeiture mortality and
  interest), VM-20 (Requirements for Principle-Based Reserves for Life Products — the
  net premium reserve floor plus stochastic and deterministic reserves; the section a
  life PBR model implements), VM-21 (variable annuities), VM-22 (non-variable
  annuities), VM-25/VM-26 (health, credit), VM-30 (actuarial opinion & memorandum),
  VM-31 (PBR Actuarial Report Requirements for Business Subject to a Principle-Based
  Reserve — the disclosure/report the model output must feed), VM-50/VM-51 (experience
  reporting), and appendices VM-A (requirements), VM-C (actuarial guidelines,
  incorporated as an appendix), VM-G (corporate governance for PBR), VM-M (mortality
  tables) and VM-V (statutory maximum valuation interest rates for formulaic reserves)
  [R3]. **Caution:** the task brief lists "VM-05" (the model SVL as reproduced in the
  VM); the Jan. 1, 2026 edition's table of contents contains **no VM-05 section** — a
  full-text search of the PDF finds no "VM-05" at all [R3]. Earlier editions (e.g.,
  2016) did reproduce the SVL as VM-05 [unverified]; use Model #820 (R1) directly for
  the statute.
- **Matters for:** all products for valuation; VM-20 specifically for term, WL, UL, IUL,
  VUL, ULSG issued on/after the operative date (with exclusions/exemptions defined in
  II. Reserve Requirements) [R3].

### R4. Life Insurance Illustrations Model Regulation (Model #582)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-582.pdf
- **Doc type:** model regulation (print: April 2001)
- **Fetched:** yes (14-page PDF retrieved and read) [R4]
- **Annotation:** Governs sales illustrations: applies to all group and individual life
  policies **except** variable life, annuities, credit life, and policies with
  illustrated death benefits of $10,000 or less [R4]. Prescribes basic/supplemental
  illustration formats, general rules and prohibitions, delivery and record retention,
  annual reports to policy owners, and annual certifications by an illustration actuary
  [R4]. The disciplined current scale, and the self-support and lapse-support tests the
  illustration actuary certifies, are the modeling-relevant machinery (the tests are
  defined in the regulation's standards and in ASOP 24, R31) [R4][unverified as to
  section numbering detail]. IUL-specific rate limits are layered on by AG 49/49-A
  (R8–R10).
- **Matters for:** WL (dividend illustrations), UL, IUL (via AG 49 family), term with
  non-guaranteed elements; explicitly **not** VUL [R4].

### R5. Universal Life Insurance Model Regulation (Model #585)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-585.pdf
- **Doc type:** model regulation (print: January 2001)
- **Fetched:** yes (14-page PDF retrieved and read) [R5]
- **Annotation:** Adapts the life-insurance regulatory framework to flexible-premium
  designs: definitions (flexible vs. fixed premium UL, interest-indexed UL), valuation
  (Section 5), nonforfeiture (Section 6), mandatory policy provisions, disclosure, the
  periodic (annual) statement to policyowners, and extra requirements for
  interest-indexed UL policies [R5]. The regulation's drafting notes state it applies to
  individual UL except variable UL [R5 per NAIC search summary; scope section read].
  This is where UL-pattern mechanics a model must honor (account value roll-forward
  disclosure, maturity/nonforfeiture treatment) get their regulatory definition.
- **Matters for:** UL, IUL (as interest-indexed UL), ULSG chassis; background for VUL
  (which is carved out and regulated under variable-products rules and federal
  securities law).

### R6. Valuation of Life Insurance Policies Model Regulation (Model #830, "Regulation XXX")
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-830.pdf
- **Doc type:** model regulation (print: October 2009; regulation adopted March 1999 [R7])
- **Fetched:** yes (35-page PDF retrieved and read) [R6]
- **Annotation:** The pre-PBR reserve regime for term and secondary-guarantee UL, still
  operative for in-force blocks issued before PBR: tables of select mortality factors
  and rules for their use; Section 6 minimum valuation standards for plans with
  guaranteed nonlevel gross premiums or nonlevel benefits (level-term segmentation —
  the "XXX" term reserves); and Section 7 minimum standards for flexible/fixed-premium
  UL with provisions (secondary guarantees) keeping the policy in force ("AXXX"
  reserves) [R6]. Basic reserves under this regulation constitute CRVM for the policies
  in scope [R6]. The XXX/AXXX conservatism is what drove captive reserve financing,
  hence AG 48 (R11) and Model #787 (R12).
- **Matters for:** term (level-premium term reserves), ULSG (with AG 38); in-force
  models for pre-2017 cohorts especially.

### R7. Actuarial Guideline XXXVIII — The Application of the Valuation of Life Insurance Policies Model Regulation (AG 38)
- **Publisher:** NAIC (PDF circulated with the NAIC CIPR newsletter, December 2012)
- **URL:** https://content.naic.org/sites/default/files/inline-files/cipr_ag38_121212.pdf
- **Doc type:** actuarial guideline text (13-page PDF, © 2012 NAIC, including Sections 8D and 8E)
- **Fetched:** yes (retrieved and read; confirmed it contains the 2012 revision sections 8D/8E and the pre-July-2005 / pre-2013 / post-2013 issue-date splits) [R7]
- **Annotation:** Interprets Model #830 for products designed around it — especially
  ULSG with shadow accounts — on the principle that "reserves need to be established
  for the guarantees provided by a policy" and that designs disguising guarantees must
  be reserved like typical designs with similar guarantees [R7]. Enumerates product
  designs and the reserving approach for each; the 2012 revisions (8D/8E) set separate
  standards for pre-2013 in-force ULSG versus post-2013 issues [R7]. Original guideline
  created 2003, revised 2005 and 2012 [unverified — consistent with the 2012 text but
  history stated from secondary sources]. Official current text lives in the NAIC
  Accounting Practices & Procedures Manual Appendix C / VM-C [R3][unverified as to AP&P
  pagination]. The NAIC CIPR topic page for AG 38 returned HTTP 403 to automated fetch.
- **Matters for:** ULSG above all; also shadow-account IUL/UL with no-lapse guarantees;
  in-force valuation models.

### R8. Actuarial Guideline XLIX (AG 49, original 2015; amended 2016)
- **Publisher:** NAIC
- **URL:** none verified — no official standalone copy of the *original* AG 49 text was located on content.naic.org (only a 2019 exposure redline: https://content.naic.org/sites/default/files/inline-files/AG%2049%20-%202019%20edits%20-%201st%20exposure.pdf, not fetched)
- **Doc type:** actuarial guideline (official text in AP&P Manual Appendix C / VM-C)
- **Fetched:** no (link failure disclosed; see R9/R10 for fetched successors and history)
- **Annotation:** First uniform limits on illustrated crediting rates for IUL under
  Model #582: a Benchmark Index Account (BIA) whose lookback average caps the
  illustrated scale, limits on illustrated policy-loan leverage, and disciplined
  current scale earned-rate limits [R9][R10]. Adopted 2015, applying to policies sold
  on/after Sept. 1, 2015 [R9 per SOA article; date detail unverified]. Superseded for
  new sales by AG 49-A for policies sold on/after Dec. 14, 2020 [R10].
- **Matters for:** IUL illustrations (and inforce illustrations of pre-2021 IUL sales).

### R9. "Actuarial Guideline XLIX (AG49): Past, Present and Future" (SOA Product Matters!, June 2023)
- **Publisher:** Society of Actuaries, Product Development Section newsletter
- **URL:** https://www.soa.org/sections/product-dev/product-dev-newsletter/2023/june/pm-2023-06-hoffer/
- **Doc type:** other (practitioner article; secondary source for the AG 49 lineage)
- **Fetched:** yes [R9]
- **Annotation:** Traces the three rounds of IUL illustration guidance: AG 49 (2015)
  capping illustrated index credits via the benchmark account; AG 49-A (2020)
  eliminating illustrated leverage from multipliers and fixed bonuses (charges funding
  enhancements must offset illustrated benefit equally); and the 2023 "quick fix"
  (industry shorthand "AG 49-B") stopping volatility-controlled-index hedge-cost
  savings from funding bonuses that out-illustrate the benchmark [R9]. Useful modeling
  context for why IUL illustrated-scale logic is version-dependent by sale date.
- **Matters for:** IUL.

### R10. Actuarial Guideline XLIX-A — The Application of the Life Illustrations Model Regulation to Policies with Index-Based Interest Sold On or After December 14, 2020 (as revised; the "AG 49-B" changes)
- **Publisher:** NAIC (adopted by LATF 12/11/2022; adopted by Life Insurance and Annuities (A) Committee 2/24/2023)
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-xlix-a-230224.pdf
- **Doc type:** actuarial guideline text (6-page PDF, © 2023 NAIC)
- **Fetched:** yes (retrieved and read) [R10]
- **Annotation:** The operative IUL illustration guideline: caps the illustrated annual
  rate of index credits by reference to the Benchmark Index Account, limits illustrated
  policy loan leverage, and requires side-by-side alternate-scale illustration and
  added disclosures [R10]. This print embeds the 2023 revisions — tighter limits for
  non-BIA index accounts apply to policies sold on or after May 1, 2023 (the change the
  industry calls "AG 49-B") [R10]. Formally the NAIC adopted these as revisions to AG
  49-A rather than as a separately numbered guideline [R9][R10]; treat "AG 49-B" as a
  colloquial label [R9].
- **Matters for:** IUL (all new-business and in-force illustrations for policies sold
  on/after Dec. 14, 2020).

### R11. Actuarial Guideline XLVIII — Actuarial Opinion and Memorandum Requirements for the Reinsurance of Policies Required to be Valued under Sections 6 and 7 of the NAIC Valuation of Life Insurance Policies Model Regulation (AG 48) [brief]
- **Publisher:** NAIC (LATF adoption 12/1/2016 revision print)
- **URL:** https://content.naic.org/sites/default/files/inline-files/committees_ex_pbr_implementation_tf_related_actuarial_guideline_ag48.pdf
- **Doc type:** actuarial guideline text (12-page PDF)
- **Fetched:** yes (retrieved and read) [R11]
- **Annotation:** Response to XXX/AXXX captive reserve financing: the appointed actuary
  must issue a **qualified** opinion if the ceding insurer (or its holding-company
  system) has a XXX/AXXX reserve financing arrangement that doesn't hold the Required
  Level of Primary Security, computed by the prescribed Actuarial Method, in qualifying
  Primary Security assets [R11]. Original AG 48 effective Jan. 1, 2015 [R11]. Sunsets
  operationally into Model #787 (R12) as states adopt it [unverified].
- **Matters for:** term and ULSG blocks that are reinsured for reserve financing —
  relevant to a model's reinsurance/collateral module, not to base cash flows.

### R12. Term and Universal Life Insurance Reserve Financing Model Regulation (Model #787) [brief]
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-787.pdf
- **Doc type:** model regulation (print: Model Regulation Service, 1st Quarter 2017)
- **Fetched:** yes (10-page PDF retrieved and read) [R12]
- **Annotation:** Codifies the AG 48 framework as a regulation under the Credit for
  Reinsurance Model Law: uniform national standards for reserve-financing reinsurance
  of policies with guaranteed nonlevel gross premiums/benefits (XXX term) and ULSG
  (AXXX), requiring Primary Security and Other Security in prescribed forms/amounts,
  with an Actuarial Method for the required level, remediation mechanics, and an
  anti-avoidance prohibition [R12].
- **Matters for:** term, ULSG (reinsurance/reserve-financing side).

---

## 2. Federal Tax — Product Qualification and Insurer Tax

Historical note [unverified, brief]: the definitional regime arrived in stages — TEFRA
(1982) first imposed temporary corridor/guideline rules for flexible-premium contracts
(former IRC 101(f)); DEFRA (1984) enacted IRC 7702 for all life contracts; TAMRA (1988)
added IRC 7702A's MEC/7-pay regime to curb single-premium tax shelters. The 2021
Consolidated Appropriations Act change is verified at [R13].

### R13. 26 U.S.C. § 7702 — Life insurance contract defined
- **Publisher:** Legal Information Institute, Cornell Law School (U.S. Code)
- **URL:** https://www.law.cornell.edu/uscode/text/26/7702
- **Doc type:** statute (current text)
- **Fetched:** yes [R13]
- **Annotation:** Federal definition of life insurance: a contract must pass either the
  cash value accumulation test (CVAT — CSV may not exceed the net single premium for
  future benefits) or the guideline premium test plus cash value corridor (GPT/CVC)
  [R13]. Subsection (f)(11), added by the Consolidated Appropriations Act, 2021,
  replaces the fixed 4%/6% assumptions with the "insurance interest rate" — the lesser
  of the § 7702 valuation interest rate and the § 7702 applicable federal interest
  rate, with a 2% transition rate for 2021 issues [R13]. A product model needs CVAT/GPT
  logic to police premium limits, corridor death benefits, and funding patterns.
- **Matters for:** all cash-value products (WL, UL, IUL, VUL, ULSG); term to a lesser
  degree (definitional compliance is trivial without cash value) [unverified].

### R14. 26 U.S.C. § 7702A — Modified endowment contract defined
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/7702A
- **Doc type:** statute (current text)
- **Fetched:** yes [R14]
- **Annotation:** A contract entered into after June 20, 1988 is a MEC if cumulative
  premiums in the first seven contract years exceed the 7-pay net level premiums, or if
  received in exchange for a MEC [R14]. Material changes restart the 7-pay test
  (with a cash-value adjustment); benefit reductions within the first seven years apply
  retroactively; there are exclusions (e.g., death benefit increases funded by the
  lowest-level death benefit premiums, reinstatement within 90 days) [R14]. MEC status
  changes distribution taxation (LIFO + penalty) [unverified], so illustration/inforce
  systems test it continuously.
- **Matters for:** WL (paid-up additions riders), UL, IUL, VUL funding-pattern logic.

### R15. 26 U.S.C. § 817 — Treatment of variable contracts (esp. § 817(h) diversification) [brief]
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/817
- **Doc type:** statute (current text)
- **Fetched:** yes [R15]
- **Annotation:** § 817(h): a variable contract based on a segregated asset account is
  not treated as life insurance/annuity unless the account is "adequately diversified"
  per Treasury regulations; safe harbor if it satisfies § 851(b)(3) with no more than
  55% in one issuer or group of related issuers; look-through rules for insurance-
  dedicated funds; Treasury securities special rule [R15]. For a VUL model this is
  background (fund eligibility), not cash flow mechanics.
- **Matters for:** VUL (and variable annuities).

### R16. 26 U.S.C. § 807 — Rules for certain reserves (tax reserves)
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/807
- **Doc type:** statute (current text)
- **Fetched:** yes [R16]
- **Annotation:** Post-TCJA (tax years beginning after Dec. 31, 2017), the life
  insurance tax reserve is the greater of the contract's net surrender value and
  92.81% of the reserve computed under the NAIC-prescribed method (CRVM for life,
  CARVM for annuities) — capped at the statutory reserve [R16]. Discounting uses the
  highest rates permitted by the NAIC as of the determination date; § 807(e)(6)
  requires reserve reporting [R16]. This is why a statutory VM-20/CRVM engine is also
  the natural source for tax reserves (see category 6).
- **Matters for:** all products — tax-reserve output of a projection model.

---

## 3. Mortality / Experience Tables and Studies

### R17. 2017 Commissioners Standard Ordinary (CSO) Tables
- **Publisher:** Society of Actuaries (developed jointly with the American Academy of Actuaries for NAIC adoption [unverified])
- **URL:** https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/
- **Doc type:** valuation mortality tables + development report (landing page; "Report on the 2017 CSO and 2017 CSO Preferred Structure Table Development" PDF linked from the page at https://www.soa.org/globalassets/assets/files/research/exp-study/research-2017-cso-report.pdf — report PDF itself not separately fetched)
- **Fetched:** yes (landing page) [R17]
- **Annotation:** The statutory valuation/nonforfeiture mortality basis for new issues:
  loaded and unloaded composite, smoker-distinct, and preferred-structure tables, plus
  gender-blended and ultimate variants, each in ANB/ALB forms [R17]. Prescribed via
  VM-20/VM-M for NPR and used in nonforfeiture calculations for post-2017 issues
  [R3][unverified as to exact VM-M table numbers]. Developed from ILEC experience
  showing significant mortality improvement over the 2001 CSO basis and adding a
  preferred structure [search summary; development detail in the linked report].
- **Matters for:** all products' statutory reserve/nonforfeiture assumptions (term, WL,
  UL, IUL, VUL, ULSG).

### R18. 2015 Valuation Basic Table (VBT) — Report and Tables
- **Publisher:** Society of Actuaries
- **URL:** https://www.soa.org/resources/experience-studies/2015/2015-valuation-basic-tables/
- **Doc type:** experience (unloaded) mortality tables + development report (report updated Sept. 2018; report PDF linked from the page at https://www.soa.org/globalassets/assets/Files/resources/experience-studies/2018/2015-vbt-report.pdf — not separately fetched)
- **Fetched:** yes (landing page) [R18]
- **Annotation:** The industry experience basis underlying the 2017 CSO: primary tables
  (male/female, smoker/nonsmoker, composite; ANB/ALB), 10 nonsmoker and 4 smoker
  Relative Risk (RR) tables for preferred-class fit, with preferred wear-off and
  mortality-improvement factors in appendices [R18]. Built on the 2009–2013 ILEC
  individual life experience [R18]. In VM-20, company prudent-estimate mortality is
  credibility-blended toward industry tables of this family [R3][unverified as to
  current VM-prescribed VBT vintage].
- **Matters for:** all products — the anchor for best-estimate/prudent-estimate
  mortality in PBR and pricing models.

### R19. 2019 Individual Life Insurance Mortality Experience Report (ILEC, observation years 2012–2019)
- **Publisher:** Society of Actuaries Research Institute — Individual Life Experience Committee (ILEC)
- **URL:** https://www.soa.org/resources/research-reports/2024/ilec-mort-2012-19
- **Doc type:** experience study report (published Oct. 2024; main report PDF linked from the page at https://www.soa.org/globalassets/assets/files/resources/research-report/2024/ilec-mort-main.pdf — not separately fetched)
- **Fetched:** yes (landing page) [R19]
- **Annotation:** Latest full ILEC mortality study: actual-to-expected experience for
  2012–2019 against standard industry tables, with trends by key policy
  characteristics, plus underlying data as pivot tables, text files, and Tableau
  dashboards [R19]. Data collection shifted from MIB (2012–17) to the NAIC as
  statistical agent (2018 on) [R19]. The A/E basis includes the 2015 VBT [search
  summary; stated expected basis 2015 VBT RR100 — noted on the report itself, not the
  landing page].
- **Matters for:** all products — mortality assumption setting and VM-20 experience
  justification.

### R20. U.S. Individual Life Insurance Persistency Update (LIMRA/SOA, observation years 2009–2013)
- **Publisher:** LIMRA and Society of Actuaries (joint study)
- **URL:** https://www.soa.org/resources/research-reports/2019/2009-13-us-ind-life-persistency-update/
- **Doc type:** experience study report + Excel lapse-rate tables
- **Fetched:** yes (landing page) [R20]
- **Annotation:** Lapse experience for whole life, term, UL, and VUL plans issued
  1918–2012, from 16 companies, with analysis by major policy/product factors,
  joint-life plans, and a detailed look at UL with secondary guarantees [R20]. The
  standard public source for base lapse assumptions by product, duration, premium mode,
  size band [R20][unverified as to full factor list]. Successor UL-focused study is
  R21; older editions (2003–04 through 2007–09) remain on soa.org.
- **Matters for:** term, WL, UL, VUL, ULSG lapse/persistency assumptions.

### R21. 2015–2021 Universal Life Premium Persistency and Lapse/Surrender Experience Study
- **Publisher:** LIMRA and SOA Research Institute (joint)
- **URL:** https://www.soa.org/resources/experience-studies/2024/15-21-ulpp-ulls/
- **Doc type:** experience study report
- **Fetched:** yes (landing page) [R21]
- **Annotation:** Two-part flexible-premium UL study for calendar years 2015–2021:
  premium persistency (14 companies, ~50% of flexible-premium UL new-sales share,
  11.9M policy-years, ~$4.0T face exposure) and lapse/surrender (24 companies, ~80% of
  market, ~33.5M policy-years, 1.3M lapse terminations) [R21]. Directly relevant to
  modeling flexible-premium payment behavior — the assumption unique to UL-type
  products — and modern surrender bases. The landing page does not break out IUL/VUL
  separately [R21].
- **Matters for:** UL, IUL, ULSG (premium persistency + lapse); VUL by analogy.

### R22. U.S. Post-Level Term Lapse and Mortality Experience Report (2021)
- **Publisher:** Society of Actuaries (research by SCOR: Bradfield, Covington, Reppert, Tomas)
- **URL:** https://www.soa.org/resources/experience-studies/2021/us-post-level-term-lapse-mortality/
- **Doc type:** experience study report + Tableau dashboards
- **Fetched:** yes (landing page) [R22]
- **Annotation:** The current study of shock lapse at the end of the level premium
  period, post-level-term (PLT) lapse, and PLT mortality deterioration —
  anti-selection that dominates late-duration term cash flows [R22]. Updates the 2010
  ("Lapse and Mortality Experience of Post-Level Premium Period Term Plans") and 2014
  PLT studies; a predictive-modeling companion report exists, and an ILEC/LIMRA update
  covering 2009–2024 experience is in progress (data request issued 2025) [R22][search
  summaries]. Essential for term models with post-level premium structures
  (jump-to-ART, graded).
- **Matters for:** term (post-level period); reinsurance pricing of term.

---

## 4. American Academy of Actuaries — Practice Notes

### R23. Life Principle-Based Reserves (PBR) Under VM-20 — Practice Note (April 2020)
- **Publisher:** American Academy of Actuaries, Life Principle-Based Approach Practice Note Work Group (Life Valuation Committee)
- **URL:** https://www.actuary.org/sites/default/files/2020-04/VM-20_PN_2020_Version_0.pdf (301-redirects to http://actuary.org/…; same path)
- **Doc type:** practice note (115-page PDF)
- **Fetched:** yes (retrieved and read; title page and front matter verified) [R23]
- **Annotation:** Q&A-format guidance on implementing VM-20: scope/exemptions, the net
  premium reserve, deterministic and stochastic reserves, prudent-estimate assumption
  setting (mortality credibility, lapse, premium persistency), asset modeling and
  reinvestment, exclusion tests, and reporting interplay with VM-31 [R23 front matter;
  topic list partly [unverified] — not every chapter was read]. Explicitly not an ASB
  promulgation and not binding [R23]. Updates the 2017 edition for VM changes since the
  12/31/2019 valuation [search summary].
- **Matters for:** term, WL, UL, IUL, VUL, ULSG under VM-20 — the implementation
  companion to R3/ASOP 52.

### R24. Life Insurance Illustrations: Application of the NAIC Life Insurance Illustrations Model Regulation and ASOP No. 24 — Practice Note (September 2021)
- **Publisher:** American Academy of Actuaries, Life Illustrations Work Group
- **URL:** https://actuary.org/wp-content/uploads/2021/09/Life_Illustrations_Practice_Note_Update.pdf
- **Doc type:** practice note (137-page PDF)
- **Fetched:** yes (retrieved and read; title page verified) [R24]
- **Annotation:** Practitioner Q&A on illustration-actuary work under Model #582 and
  ASOP 24: disciplined current scale development, self-support and lapse-support
  testing, certification practice, and application to indexed products under the AG 49
  family [R24 title/front matter; detailed topic list partly [unverified]]. The
  companion to R4/R31 for building illustration logic into product models.
- **Matters for:** WL (dividends as illustrated NGEs), UL, IUL, term with NGEs; not VUL
  (outside Model #582 scope [R4]).

### R25. Life Principle-Based Reserves (PBR) Assumptions Resource Manual (January 2019)
- **Publisher:** American Academy of Actuaries, PBR Assumptions Resource Manual Work Group (Life Practice Council)
- **URL:** https://www.actuary.org/sites/default/files/files/publications/PBR_Assumptions_Resource_Manual_012919.pdf (301-redirects to http://actuary.org/…; same path)
- **Doc type:** practice resource (86-page PDF)
- **Fetched:** yes (retrieved and read; title page verified) [R25]
- **Annotation:** "An actuary's step-by-step sample framework for setting, updating,
  and governing life insurance assumptions for PBR and other valuation frameworks"
  [R25] — assumption governance, documentation, and update-cycle patterns that a model
  library's assumption architecture can mirror. Non-binding, non-ASB [R25].
- **Matters for:** all VM-20 products; especially ULSG/term assumption governance.
- **Note on UL practice notes:** no current standalone Academy "universal life"
  practice note was located on actuary.org (search performed 2026-08-03); UL-specific
  practice content lives in R23–R25, ASOP 2 (R26), and the illustration materials. The
  Academy's practice-note index is at https://actuary.org/practice-notes/ (not
  fetched).

---

## 5. Actuarial Standards of Practice (ASB) — current numbers/titles verified against the ASB standards list (fetched 2026-08-03)

### R26. ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/asop-no-2-nonguaranteed-elements-for-life-insurance-and-annuity-products/
- **Doc type:** actuarial standard of practice (adopted Sept. 2021; effective June 1, 2022)
- **Fetched:** yes [R26]
- **Annotation:** Governs determination (and support of illustration) of NGEs — credited
  rates, COI charges, expense loads, indeterminate premiums — for individual life and
  annuity forms where NGEs vary at insurer discretion, including UL, indeterminate-
  premium life, and fixed/indexed/variable deferred annuities [R26]. Excludes
  dividends (ASOP 15) and illustrations under ASOP 24 [R26]. Defines the
  determination-policy/framework discipline a model's NGE re-rating logic should
  reflect.
- **Matters for:** UL, IUL, VUL (charges/credits), indeterminate-premium term; WL NGEs
  other than dividends.

### R27. ASOP No. 7 — Life or Health Cash Flow Analysis (revision adopted December 2025; effective June 1, 2026)
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/life-or-health-cash-flow-analysis/
- **Doc type:** actuarial standard of practice
- **Fetched:** yes [R27]
- **Annotation:** The revised cash-flow-analysis standard (successor to "Analysis of
  Life, Health, or Property/Casualty Insurer Cash Flows"; P/C moved to ASOP 20) [R27].
  Applies to actuaries analyzing life/health cash flow risks — the general standard for
  asset/liability cash flow projection work of exactly the kind a reference model
  performs [R27]. Pairs with ASOP 22 for opinions and ASOP 56 for model governance.
- **Matters for:** all products.

### R28. ASOP No. 15 — Dividends for Individual Participating Life Insurance, Annuities, and Disability Insurance
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/dividends-individual-participating-life-insurance-annuities-disability-insurance/
- **Doc type:** actuarial standard of practice (adopted March 2006; effective Aug. 1, 2006)
- **Fetched:** yes [R28]
- **Annotation:** Guidance on establishing/modifying dividend frameworks and
  determining/illustrating dividends for individual participating business (stock,
  mutual, fraternal), including participating riders [R28]. Excludes divisible-surplus
  aggregate determination and ASOP-24 illustration compliance [R28]. The
  contribution-principle mechanics behind a par WL model's dividend module.
- **Matters for:** participating whole life (and par riders on other products).

### R29. ASOP No. 22 — Statements of Actuarial Opinion Based on Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/asop-no-22-statements-of-actuarial-opinion-based-on-asset-adequacy-analysis-for-life-insurance-annuity-or-health-insurance-reserves-and-other-liabilities/
- **Doc type:** actuarial standard of practice (adopted Sept. 2021; effective June 1, 2022)
- **Fetched:** yes [R29]
- **Annotation:** Standard for the appointed actuary's asset adequacy opinion under the
  SVL/VM-30 framework (and analogous law) [R29]. Cash flow testing is the dominant
  technique [unverified — the standard admits multiple methods]; a liability projection
  model that will feed AAT/CFT must satisfy this standard's analysis and documentation
  expectations, alongside ASOP 7 and ASOP 56.
- **Matters for:** all products at the company/block level (ULSG and long-duration
  guarantees are typical stress points [unverified]).

### R30. ASOP No. 24 — NAIC Life Insurance Illustrations Model Regulation (revision adopted September 2024; effective December 1, 2024)
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/asop-24-naic-life-insurance-illustrations-model-regulation-024-217/
- **Doc type:** actuarial standard of practice (Doc. No. 217; PDF: https://www.actuarialstandardsboard.org/wp-content/uploads/2024/09/asop024_217.pdf — PDF not separately fetched)
- **Fetched:** yes (standard's page) [R30]
- **Annotation:** Applies when actuaries certify that illustrated scales comply with
  Model #582 or with AG 49/AG 49-A [R30]. Covers illustrated-scale work only;
  currently-payable-scale determination belongs to ASOP 2/15 [R30]. The Dec. 2024
  revision is the current edition — note it postdates and reflects the indexed-product
  guidelines [R30].
- **Matters for:** WL, UL, IUL, illustrated term; not VUL [R4].

### R31. ASOP No. 52 — Principle-Based Reserves for Life Products under the NAIC Valuation Manual
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/principle-based-reserves-life-products-naic-valuation-manual/
- **Doc type:** actuarial standard of practice (adopted Sept. 2017; effective Dec. 31, 2017)
- **Fetched:** yes [R31]
- **Annotation:** Standard for actuaries calculating or reviewing VM-20 reserves;
  extends to any actuary participating in the principle-based methodology [R31].
  Notably, if the standard conflicts with the operative Valuation Manual, "the
  provisions of the Valuation Manual shall govern" [R31]. Sets expectations on
  assumptions, margins, model granularity, and documentation that flow into VM-31
  reporting.
- **Matters for:** all VM-20 products: term, WL, UL, IUL, VUL, ULSG.

### R32. ASOP No. 56 — Modeling
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/modeling-3/
- **Doc type:** actuarial standard of practice (adopted Dec. 2019; effective Oct. 1, 2020)
- **Fetched:** yes [R32]
- **Annotation:** Cross-practice standard for designing, developing, selecting,
  modifying, using, reviewing, or evaluating models where reliance on model output has
  a material effect [R32]. The governing standard for the reference implementation
  itself: intended purpose, model risk mitigation, validation/testing, reliance on
  others' models and data, documentation [R32 scope; component list partly
  [unverified]].
- **Matters for:** all products — the model-governance frame for the whole library.

---

## 6. Accounting Frames — Why One Cash Flow Model Serves Several Bases [brief]

### R33. NAIC Accounting Practices and Procedures Manual (statutory basis)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/publications
- **Doc type:** other (annual manual; listed on the NAIC publications page — manual itself is a paid publication)
- **Fetched:** yes (publications page describing the manual) [R33]
- **Annotation (statutory):** The AP&P Manual "includes all statutory accounting
  guidance that has been adopted by the NAIC as of March of the current year,"
  including appendices with excerpts of applicable model laws, working-group
  interpretations, **actuarial guidelines** (Appendix C — where AG 38/48/49 officially
  live), and financial-reporting implementation guidance; updated annually [R33].
  Statutory accounting is conservative, solvency-oriented, and the frame in which
  Models 820/830, the VM, and the AGs operate; a liability model's statutory outputs
  (reserves, nonforfeiture floors) plug into this basis.
- **Matters for:** all products (statutory reporting).

### R34. FASB ASU No. 2018-12 — Financial Services—Insurance (Topic 944): Targeted Improvements to the Accounting for Long-Duration Contracts (LDTI)
- **Publisher:** Financial Accounting Standards Board
- **URL:** https://www.fasb.org (fasb.org blocked automated fetch — both https://www.fasb.org/insurance and a direct document URL returned HTTP 403; no working deep link is cited to avoid fabricating one. An accessible third-party full text is PwC Viewpoint: https://viewpoint.pwc.com/dt/us/en/fasb_financial_accou/asus_fulltext/2018/asu_201812financial_/asu_201812financial__US/asu_201812financial__US.html — fetch failed with redirect loop, likely auth-gated.)
- **Doc type:** other (accounting standards update)
- **Fetched:** no (title, scope, and effective dates corroborated across multiple secondary sources: BDO, Deloitte, KPMG, PwC summaries via search)
- **Annotation (U.S. GAAP / LDTI):** ASU 2018-12 rewrote GAAP for long-duration
  contracts: liability for future policy benefits with annually reviewed cash flow
  assumptions and discounting at an upper-medium-grade (single-A) rate through OCI,
  market risk benefits at fair value, simplified DAC amortization, and greatly expanded
  disclosures [unverified — consistent across the cited summaries]. Effective for
  large SEC filers Jan. 1, 2023 (2025 for others) [search summaries]. A GAAP valuation
  run needs the same projected cash flows as statutory, but different assumption
  update/locking, discounting, and amortization overlays — a key reason to separate
  cash flow projection from measurement in model architecture.
- **Matters for:** term, WL (traditional LFPB), UL/IUL/VUL/ULSG (universal-life-type
  contracts, additional liabilities/SOP 03-1-style features, MRBs) [unverified].

### Tax reserves (cross-reference R16)
- **Annotation (tax):** IRC § 807 defines tax reserves off the NAIC-prescribed method:
  greater of net surrender value and 92.81% of the CRVM/VM-computed reserve, capped at
  statutory, discounted at NAIC-permitted rates [R16]. So the same statutory engine,
  with a scalar haircut and cap logic, produces the tax basis; DEFRA/TEFRA/TAMRA-era
  definitional rules (category 2) decide whether the *contract* is life insurance at
  all. Together, statutory (R33), GAAP LDTI (R34), and tax (R16) explain why a single
  liability cash flow projection typically feeds at least three measurement wrappers.

---

## Summary of retrieval status

| R# | Short name | Fetched |
|----|------------|---------|
| R1 | Model 820 SVL | yes |
| R2 | Model 808 SNFL | yes |
| R3 | Valuation Manual 2026 (VM-01/02/20/31, VM-C/M/G/V; no VM-05) | yes |
| R4 | Model 582 Illustrations | yes |
| R5 | Model 585 UL Model Reg | yes |
| R6 | Model 830 XXX | yes |
| R7 | AG 38 (2012 text incl. 8D/8E) | yes |
| R8 | AG 49 original | no (no official standalone URL located) |
| R9 | SOA AG49 history article | yes |
| R10 | AG 49-A as revised 2023 ("49-B") | yes |
| R11 | AG 48 (2016 revision) | yes |
| R12 | Model 787 | yes |
| R13 | IRC 7702 | yes |
| R14 | IRC 7702A | yes |
| R15 | IRC 817 | yes |
| R16 | IRC 807 | yes |
| R17 | 2017 CSO (landing) | yes |
| R18 | 2015 VBT (landing) | yes |
| R19 | ILEC 2012–19 report (landing) | yes |
| R20 | 2009–13 persistency (landing) | yes |
| R21 | 2015–21 UL persistency (landing) | yes |
| R22 | PLT 2021 study (landing) | yes |
| R23 | AAA VM-20 practice note | yes |
| R24 | AAA illustrations practice note | yes |
| R25 | AAA PBR assumptions manual | yes |
| R26 | ASOP 2 | yes |
| R27 | ASOP 7 | yes |
| R28 | ASOP 15 | yes |
| R29 | ASOP 22 | yes |
| R30 | ASOP 24 | yes |
| R31 | ASOP 52 | yes |
| R32 | ASOP 56 | yes |
| R33 | NAIC AP&P Manual (publications page) | yes |
| R34 | FASB ASU 2018-12 | no (fasb.org 403) |
