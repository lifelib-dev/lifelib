# U.S. individual annuities — regulatory and actuarial references (extends the life library)

Cross-product annotated bibliography supporting reference implementations of liability
cash flow projection models for U.S. individual annuities (fixed deferred / fixed indexed /
variable / registered index-linked / immediate / deferred income).

- Accessed: 2026-08-04 (all links checked on this date unless noted otherwise).
- Citation discipline: facts drawn from a document actually retrieved carry its [R#];
  claims from general knowledge or from search summaries only are tagged [unverified];
  failed links are flagged explicitly. No URL below is fabricated — every URL was either
  fetched successfully or is marked as not fetched.
- Retrieval note: many primary PDFs (NAIC model laws, the Valuation Manual, Academy
  papers) return raw compressed streams to the fetch tool. Where that happened the PDF
  was downloaded and its text extracted locally before reading; those entries are marked
  **fetched: yes (local text extraction)** and their annotations are first-hand.
- Domain blocks encountered on 2026-08-04: **sec.gov returns HTTP 403** to automated
  clients (press releases, `/files/rules/final/...`, `formn-4.pdf`); **federalregister.gov
  and ecfr.gov redirect to a bot-block page**; **irs.gov returned 404** on the LB&I
  directive URLs surfaced by search. Where a working alternative existed
  (govinfo.gov, law.cornell.edu, gao.gov) it was used and is cited instead.

---

## Scope and numbering note

**R1–R34 live in `regulatory-actuarial.md` and are frozen.** They are cited by existing
product documentation and must not be renumbered, restated, or re-annotated. This file
opens a continuation of the **same shared numbering space**: new entries begin at **R35**
and run sequentially to **R72**.

Several R1–R34 entries also govern annuity models. They are *not* duplicated here; the
next section lists them with a one-line note on how each binds an annuity model. Where an
annuity-specific document is a *section of* a document already catalogued (VM-21 and
VM-22 inside the Valuation Manual, R3), a new entry is created for the section because
the annuity models cite the section directly — the parent document is cross-referenced,
not restated.

---

## Existing entries (R1–R34) that also bind annuity models

| R# | Title (short) | How it applies to annuities |
|----|---------------|-----------------------------|
| R1 | Standard Valuation Law (Model #820) | The enabling statute for CARVM as well as CRVM; §5.C.2 is the hook for non-variable group annuity certificates, and §11–14 make the Valuation Manual (hence VM-21/VM-22) operative for annuities issued on/after 1/1/2017 [R3]. |
| R2 | Standard Nonforfeiture Law for Life Insurance (Model #808) | Does **not** apply to annuities — annuity nonforfeiture runs through Model #805 (R42) and, for variable/index-linked, Model #250 §7 (R43) and AG 54 (R44). Listed only to prevent mis-application. |
| R3 | Valuation Manual, Jan. 1, 2026 Edition | The parent document for VM-21 (R35), VM-22 (R36), VM-V §1 (R37), VM-C (R41) and the annuity mortality definitions in VM-M (R59). Its Introduction states annuity contracts are included in the term "life insurance contracts" unless indicated otherwise [R3]. |
| R4 | Life Insurance Illustrations Model Reg (Model #582) | Expressly **excludes annuities** [R4]; annuity illustrations are governed by Model #245 §6 (R45). Listed to prevent mis-application. |
| R5 | Universal Life Insurance Model Regulation (Model #585) | Not applicable to annuities, but the interest-indexed-UL provisions are the structural analogue of FIA crediting mechanics; useful for shared crediting-engine design. [unverified as to any direct annuity effect] |
| R6 | Model #830 ("Regulation XXX") | Life-only. No annuity application. Listed to prevent mis-application. |
| R7 | AG 38 | Life-only (ULSG). No annuity application. |
| R8–R10 | AG 49 / AG 49-A | Life-only (IUL illustrations). The FIA analogue is Model #245 §6 (R45), which caps indexed-annuity illustration crediting differently — do not reuse AG 49 logic for FIA illustrations. |
| R11–R12 | AG 48 / Model #787 | Life-only reserve financing (XXX/AXXX). No annuity application. |
| R13–R14 | IRC §7702 / §7702A | Life-only definitional tests. The annuity analogues are IRC §72 (R55), §72(s)/(u), and §817(h) for variable contracts. |
| **R15** | **IRC §817 (esp. §817(h))** | **Directly binding on variable annuities and RILAs:** a segregated-asset-account contract is not treated as an annuity unless the account is adequately diversified [R15]. Governs separate-account fund eligibility in a VA/RILA model. |
| **R16** | **IRC §807 (tax reserves)** | **Directly binding:** the tax reserve is the greater of net surrender value and 92.81% of the NAIC-prescribed method — **CARVM for annuities** — capped at the statutory reserve [R16]. The annuity statutory engine (VM-21/VM-22/CARVM) is therefore also the tax-reserve engine. See R72 for the IRS examination directive. |
| R17–R19 | 2017 CSO / 2015 VBT / ILEC | Life mortality. Annuitant mortality is a *different* and generally lighter basis — use the 2012 IAR/2012 IAM family (R59, R60) and the payout-annuity experience studies (R61), never the CSO/VBT tables, for annuitant longevity. |
| R20–R22 | Life persistency / PLT studies | Life lapse. Annuity surrender behavior is structurally different (surrender-charge-expiry shock lapse, MVA/rate-differential dynamic lapse, GLWB-suppressed surrender) — use R62–R64. |
| R23 | AAA VM-20 PBR Practice Note | Life PBR only. The VA analogue is the VM-21 practice note supplement (R66); there is no equivalent VM-22 practice note yet (see Gaps). |
| R24 | AAA Life Illustrations Practice Note | Life-only (Model #582/ASOP 24). No annuity analogue located. |
| R25 | AAA PBR Assumptions Resource Manual | Assumption-governance framework, written for life PBR but directly transferable to VM-21/VM-22 assumption setting and documentation [unverified as to explicit annuity scope]. |
| **R26** | **ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products** | **Directly binding:** its scope expressly includes fixed, indexed and variable deferred annuities [R26]. Governs redetermination of FIA caps/participation rates/spreads, declared credited rates, and VA rider charges. |
| **R27** | **ASOP No. 7 — Life or Health Cash Flow Analysis** | **Directly binding:** the general standard for the asset/liability cash flow projection an annuity model performs (disintermediation, reinvestment, MVA). |
| R28 | ASOP No. 15 — Dividends | Titled to include annuities, but relevant only to participating annuity forms — rare in the individual market. [unverified as to current market relevance] |
| **R29** | **ASOP No. 22 — AAA opinions based on asset adequacy analysis** | **Directly binding:** AG 35 expressly requires equity-indexed annuity reserves to be asset-adequacy tested [R40], and annuity blocks (SPIA, MYGA, FIA) are the classic cash-flow-testing exposures. |
| R30 | ASOP No. 24 — Illustrations Model Reg | Life-only; ASOP 24 covers Model #582 and AG 49/49-A certifications [R30], not Model #245 annuity illustrations. |
| R31 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual | Scoped to VM-20 life products. **It does not cover VM-21 or VM-22** — verified against the ASB standards list, which shows no annuity-PBR ASOP (R70/R71 context). See Gaps. |
| **R32** | **ASOP No. 56 — Modeling** | **Directly binding:** the model-governance frame for the whole annuity library (stochastic scenario models, nested valuations, hedge models). |
| **R33** | **NAIC AP&P Manual** | **Directly binding:** Appendix C is the authoritative home of AG 33, AG 35 and AG 43 (R38–R40), and Appendix A-821 holds the 2012 IAM/Scale G2 tables referenced by VM-M [R3]. |
| **R34** | **FASB ASU 2018-12 (LDTI)** | **Directly binding:** annuity GLWB/GMDB/GMIB riders and RILA index credits are the paradigm **market risk benefits** measured at fair value through earnings under LDTI; payout annuities carry a liability for future policy benefits with annually reviewed assumptions. |

---

## New entries

### 1. NAIC valuation — VM-21, VM-22, and the CARVM guideline family

#### R35. VM-21: Requirements for Principle-Based Reserves for Variable Annuities (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages 21-1 to 21-79 of the 457-page PDF; same document as R3)
- **Doc type:** valuation manual section ("NAIC Adoptions through August 13, 2025")
- **Fetched:** yes (local text extraction; Sections 1, 2, 3 and the TOC read in full) [R35]
- **Annotation:** The statutory reserve standard for variable annuities, and it **constitutes
  CARVM** for every contract in its scope [R35]. Scope covers variable deferred and variable
  immediate annuity contracts (with or without GMDB/VAGLB), group annuity contracts with
  similar guarantees, and any other contract with GMDB/VAGLB-like guarantees having no other
  explicit reserve requirement — in which case the benefit is reserved stand-alone and added
  to the base contract reserve [R35]. **Aggregate reserve = the SR + the additional standard
  projection amount + any Alternative Methodology reserve** [R35]. The **SR is CTE70** of the
  scenario reserves, where each scenario contributes the greatest present value of accumulated
  deficiency from a stochastic asset/liability projection on prudent-estimate assumptions
  [R35]. Sections 9–12 carry the modelling machinery an implementer needs: hedges under a
  Clearly Defined Hedging Strategy (§9), contract holder behavior (§10), prudent-estimate
  mortality (§11), and allocation of the aggregate reserve to the contract level (§13) [R35].
  **Effective for valuation dates on or after Jan. 1, 2020**, with an elective 36-month
  phase-in (extendable to seven years with domiciliary approval) computed as
  `Reserve = D − (B − A) × C / B` where `C = R1 − R2` is the 1/1/2020 reserve difference
  between the 2020 and 2019 Valuation Manual bases [R35]. A separate **economic scenario
  generator phase-in** over 36 months beginning Jan. 1, 2026 is available for the GOES
  requirements in VM-20 Appendix 1 as applicable in the 2026 edition [R35]. VM-21 also states
  that its projections are anticipated to be used for RBC, and that VM-21 §§4.A–4.E and the
  RBC requirements are **identical** except for the elective federal-income-tax treatment
  [R35] — the single most important architectural fact for a VA model (one projection, two
  outputs; see R47).
- **Matters for:** variable-annuity; registered-index-linked-annuity (ILVA/RILA written as
  variable annuities fall in scope via the GMDB/VAGLB and separate-account tests [R35][R69]);
  any deferred-annuity chassis carrying a VAGLB-like guarantee.

#### R36. VM-22: Requirements for Principle-Based Reserves for Non-Variable Annuities (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages 22-1 to 22-90; same document as R3)
- **Doc type:** valuation manual section
- **Fetched:** yes (local text extraction; Sections 1, 2, 3.A–3.F and the TOC read in full) [R36]
- **Annotation:** **Verified against the current Valuation Manual rather than assumed.** The
  2026 edition of VM-22 is the *principle-based* framework for non-variable annuities; it
  "constitute[s] the Commissioners Annuity Reserve Valuation Method (CARVM) and, for some
  contracts and certificates, the Commissioners Reserve Valuation Method (CRVM)" [R36].
  **Effective date: these requirements apply for valuation dates on or after January 1, 2026**
  [R36]. **Transition:** a company may elect to keep valuing business otherwise subject to
  VM-22 under VM-A/VM-C/VM-M/VM-V for business issued during the **first three years after
  the effective date**; once VM-22 PBR is elected for a block it must be continued; and
  **all applicable blocks must be on VM-22 PBR prospectively starting three years after the
  effective date** [R36] (i.e., Jan. 1, 2029 [unverified — the text states the rule as
  "three years after the effective date", it does not print the date]). Aggregate reserve =
  SR + DR for contracts passing the Single Scenario Test + reserve for contracts passing the
  exclusion test and valued under VM-A/VM-C/VM-M/VM-V [R36]; **SR = CTE70** [R36]. The
  **additional standard projection amount is disclosure-only** under VM-31, and a LATF
  referral of April 3, 2025 directs the VM-22 Subgroup to add attribution analysis and to
  reiterate that "the SPA is not a safe harbor," with language targeted at the 1/1/2027
  Valuation Manual [R36]. **Reserving Categories** (which may not be aggregated except under
  §3.F.2) are: *Payout Annuity* (SPIA, DIA, structured settlements, annuitizations of host
  contracts, supplementary contracts with scheduled payments, Model #820 §5.C.2 certificates,
  pension risk transfer); *Longevity Reinsurance*; and *Accumulation* — everything else,
  including fixed income streams from guaranteed living benefits after account exhaustion
  [R36]. Risks explicitly to be reflected include disintermediation, additional premium
  dump-ins under high guarantees in low-rate environments, annuitization risk, and GLB
  utilization risk [R36].
- **Matters for:** fixed-deferred-annuity; fixed-indexed-annuity; immediate-annuity;
  deferred-income-annuity. **Not** variable annuities (VM-21) — but note the fixed account of
  a VA and the fixed payout stream after a VA's funds are exhausted land in VM-22 categories.
- **Note on the "established scope" premise:** VM-22 was historically the home of maximum
  valuation interest rates for income annuities. In the **Jan. 1, 2026 edition that content
  is not in VM-22 — it is in VM-V Section 1 (R37)**, and VM-22 is entirely the PBR framework
  [R36][R37]. A model citing "VM-22 income annuity interest rates" against a current
  Valuation Manual is citing the wrong section.

#### R37. VM-V: Statutory Maximum Valuation Interest Rates for Formulaic Reserves, Section 1 — Income Annuities
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages V-1 to V-3+; same document as R3)
- **Doc type:** valuation manual appendix
- **Fetched:** yes (local text extraction; §1.A Purpose and Scope, §1.B Definitions read) [R37]
- **Annotation:** Defines, for SPIAs "and other similar contracts, certificates and contract
  features," the **statutory maximum valuation interest rate complying with Model #820** — the
  maximum interest assumption for CARVM (and for some contracts CRVM) on formulaic annuity
  reserves [R37]. Scope covers, for issues after Dec. 31, 2017: immediate annuities; **deferred
  income annuity contracts**; structured settlements in payout or deferred status; fixed payouts
  from settlement options or annuitizations of host contracts; supplementary contracts with
  scheduled payments; fixed income streams from **contingent deferred annuities** and from
  **guaranteed living benefits once contract funds are exhausted**; and Model #820 §5.C.2
  group annuity certificates [R37]. It applies to contracts **not passing the SET covered by
  VM-22** [R37] — i.e., VM-V is the formulaic fallback where VM-22 PBR is excluded. Interest is
  set by a "reference period" / Valuation Rate Bucket mechanic keyed to the premium
  determination date and the timing of the first life-contingent payment [R37]. Critically,
  VM-V §1 **supersedes** the interest-rate guidance in VM-A and VM-C, expressly including
  **AG IX-B** and the interest references in **AG IX-C** [R37].
- **Matters for:** immediate-annuity; deferred-income-annuity; fixed-deferred-annuity (the
  payout phase and settlement-option streams); structured settlements.

#### R38. Actuarial Guideline XLIII — CARVM for Variable Annuities (AG 43)
- **Publisher:** NAIC (this print is the VAIWG redlined working copy dated 2016-09-26, showing the 2009 text with the reform-era edits)
- **URL:** https://content.naic.org/sites/default/files/inline-files/cmte_e_va_issues_wg_related_redlined_ag43_160926.pdf
- **Doc type:** actuarial guideline text (redline; official text lives in AP&P Manual Appendix C, R33)
- **Fetched:** yes (local text extraction; TOC, Section I Background, Section IV Reserve Methodology, Section V Effective Date read) [R38]
- **Annotation:** The predecessor regime to VM-21 and **still operative for in-force**. Its
  purpose is to interpret CARVM for variable annuities and for contracts with similar
  guarantees, "codif[ying] the basic interpretation of the Commissioners Annuity Reserve
  Valuation Method (CARVM)" under the SVL [R38]. Reserve structure: the **Aggregate Reserve
  is the Standard Scenario Amount plus the excess, if any, of the Conditional Tail Expectation
  Amount over the Standard Scenario Amount** [R38] — a floor-plus-excess construct materially
  different from VM-21's SR + additional standard projection amount. The CTE Amount is
  **CTE(70)**: the average of the largest 30% of scenario greatest-present-values of
  accumulated deficiency [R38]. Twelve appendices carry the machinery (projections,
  reinsurance, standard scenario, Alternative Methodology, scenario calibration, hedging,
  certification, contract holder behavior, prudent-estimate mortality, general account
  assets) [R38]. **The Guideline affects all contracts issued on or after January 1, 1981**,
  effective Dec. 31, 2009 (the redline shows the reform-era change to 2018) [R38].
- **Relationship to VM-21 (verified):** VM-21 states that contracts subject to VM-21 **may be
  aggregated with AG 43 contracts** for performing and documenting the reserve calculation,
  and — decisively — that "through reference in AG 43, the reserve requirements in VM-21 also
  apply to those contracts issued prior to Jan. 1, 2017, that would not otherwise be
  encompassed by the scope of VM-21" [R35]. So AG 43 is **not simply superseded**: it is the
  scoping shell that pulls pre-2017 VA business onto the VM-21 calculation. If the two are
  aggregated, VM-G corporate governance applies to the combined valuation [R35].
- **Matters for:** variable-annuity (in-force cohorts issued 1981–2016); registered-index-linked-annuity in-force written on a VA chassis.

#### R39. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33)
- **Publisher:** NAIC
- **URL:** no free official standalone text located. Title and current status verified from the
  Valuation Manual's VM-C index (https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf,
  page C-1) [R41]. Authoritative text is in AP&P Manual Appendix C (R33), a paid publication.
  A related Academy proposal document is public but is *not* the guideline:
  http://actuary.org/wp-content/uploads/2017/11/AG-33_Non-Elective_Incidence_Reserve_Proposal_8-22-13.pdf (not fetched)
- **Doc type:** actuarial guideline
- **Fetched:** **no** — title and continued incorporation verified via R41; substantive
  description below is from secondary sources and is tagged accordingly
- **Annotation:** The interpretive core of formulaic CARVM for deferred annuities. CARVM sets
  the reserve as the greatest present value, over all elective benefit streams, of future
  guaranteed benefits — AG 33 specifies how to construct and value those **integrated benefit
  streams**, how elective benefits (surrender, partial withdrawal, annuitization at guaranteed
  purchase rates, nursing-home waivers) are combined with **non-elective** benefits (death,
  and other non-mortality incidence), and what the "efficient policyholder selection"
  assumption means in practice [unverified — consistent across the Academy proposal document
  and the *Journal of Actuarial Practice* treatment of AG 33/34, neither fetched]. For a model
  implementer this is the guideline that turns a deferred-annuity account-value roll-forward
  into a *set* of benefit streams and takes the maximum present value across them — the
  formulaic reserve any pre-VM-22 or VM-22-excluded fixed deferred annuity still requires.
- **Matters for:** fixed-deferred-annuity; fixed-indexed-annuity (AG 35 layers the index
  feature onto the AG 33 calculation [R40 context]); any deferred annuity valued formulaically
  under VM-A/VM-C rather than VM-22 PBR.

#### R40. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve Method to Equity Indexed Annuities (AG 35)
- **Publisher:** NAIC
- **URL:** no free official standalone text located. Exact title verified from the Valuation
  Manual's VM-C index (page C-2) [R41]. Authoritative text is in AP&P Manual Appendix C (R33).
- **Doc type:** actuarial guideline
- **Fetched:** **no** — title and continued incorporation verified via R41
- **Annotation:** The CARVM treatment of the index feature in equity-indexed (now generally
  "fixed indexed") annuities: it does not replace AG 33 but specifies how the index-linked
  benefit is brought into the AG 33 greatest-present-value calculation, offering alternative
  method families (industry shorthand "Type 1" / "Type 2"), imposing certification and
  notification requirements when a method is chosen or changed, and **requiring that
  equity-indexed annuity reserves be asset-adequacy tested** [unverified — from a practitioner
  presentation, not the guideline text]. The asset-adequacy requirement is the modelling
  consequence that matters most: an FIA block cannot rely on the formulaic reserve alone,
  so the same cash flow model must serve CARVM and ASOP 22 cash flow testing (R29).
- **Matters for:** fixed-indexed-annuity (primary); fixed-deferred-annuity with index-linked
  crediting options.

#### R41. VM-C: Appendix C — Actuarial Guidelines (index of guidelines incorporated into the Valuation Manual)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages C-1 to C-2; same document as R3)
- **Doc type:** valuation manual appendix (index only — it "references the following requirements from Appendix C of the AP&P Manual" [R41])
- **Fetched:** yes (local text extraction; complete two-page index read) [R41]
- **Annotation:** The authoritative, current list of which actuarial guidelines the Valuation
  Manual incorporates, with their exact titles — the cheapest way to verify a guideline number
  without buying the AP&P Manual. The **annuity/CARVM family** it lists: **II** (interest rate
  guarantees on active life funds under group annuity contracts); **VIII** (valuation of
  individual single premium deferred annuities); **IX** (form classification of individual
  SPIAs); **IX-A** and **IX-C** (substandard annuity mortality for impaired lives, structured
  settlements and SPIAs respectively); **IX-B** (methods under the SVL for individual SPIAs,
  associated deferred payments, some deferred annuities and structured settlements);
  **XIII** (guideline concerning CARVM); **XXXIII** (R39); **XXXV** (R40); **XL** (valuation
  rate of interest for funding agreements and GICs with bail-out provisions); **XLI**
  (projection of guaranteed nonforfeiture benefits under CARVM) [R41]. Note IX-B and IX-C are
  superseded on valuation interest rates by VM-V §1 for in-scope contracts [R37].
- **Verified negative finding:** the VM-C index contains **no AG XLIII, no AG XLIX/XLIX-A, and
  no AG LIV** [R41]. AG 43 sits in AP&P Appendix C but outside VM-C because its remaining work
  is on pre-VM contracts [R35]; AG 54 is a nonforfeiture guideline, not a valuation one [R44].
  Do not infer a guideline's non-existence from absence here, and do not infer its VM
  applicability from presence elsewhere.
- **Matters for:** fixed-deferred-annuity; fixed-indexed-annuity; immediate-annuity;
  deferred-income-annuity — the formulaic-reserve scaffolding for all of them.

---

### 2. NAIC nonforfeiture and market conduct

#### R42. Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-805.pdf
- **Doc type:** model law (print: "NAIC Model Laws, Regulations, Guidelines and Other Resources—Fall 2020")
- **Fetched:** yes (local text extraction; Sections 1–8 read in full) [R42]
- **Annotation:** The floor under every fixed deferred annuity's cash value, and the single
  most mechanically precise thing in this bibliography. The **minimum nonforfeiture amount**
  is an accumulation of **net considerations = 87.5% of gross considerations** credited in
  each contract year, at the Subsection B interest rate, **decreased by**: prior withdrawals
  and partial surrenders (accumulated at the same rates), an **annual contract charge of $50**
  (accumulated), premium tax actually paid by the company, and any indebtedness with accrued
  interest [R42]. **The indexed nonforfeiture rate (Subsection B):** the annual rate is the
  **lesser of 3% and** — the **five-year Constant Maturity Treasury Rate** reported by the
  Federal Reserve as of a date, or averaged over a period, **rounded to the nearest 1/20th of
  one percent**, specified in the contract and no longer than **15 months** before the issue
  or redetermination date, **reduced by 125 basis points**, **subject to a floor of 15 basis
  points (0.15%)** [R42]. The rate applies for an initial period and may be redetermined; the
  redetermination date, basis and period must be stated in the contract [R42]. **Subsection C
  (the FIA carve-out):** during a period in which the contract provides "substantive
  participation in an equity indexed benefit," the 125bp reduction may be increased by **up to
  an additional 100 basis points**, provided the present value of the additional reduction at
  issue and at each redetermination does not exceed the market value of the equity benefit —
  demonstrable on the commissioner's demand [R42]. **Cash surrender value** must be at least
  the present value of the accrued paid-up annuity at a rate no more than **1% higher** than
  the contract accumulation rate, and in no event less than the minimum nonforfeiture amount;
  the death benefit must be at least the cash surrender benefit [R42]. **Scope exclusions
  (Section 2):** reinsurance, employer/employee-organization group annuities under retirement
  or deferred compensation plans other than those providing IRAs/individual retirement
  annuities under IRC §408, premium deposit funds, **variable annuities**, investment
  annuities, **immediate annuities**, **deferred annuities after annuity payments have
  commenced**, reversionary annuities, and out-of-state deliveries; Sections 3–8 do not apply
  to **contingent deferred annuities**, for which the commissioner may prescribe nonforfeiture
  by regulation [R42].
- **Matters for:** fixed-deferred-annuity (primary — this *is* the guaranteed floor a model
  must track alongside account value); fixed-indexed-annuity (with the Subsection C
  additional reduction). Excluded: variable-annuity, immediate-annuity,
  deferred-income-annuity (once in payout), and registered-index-linked-annuity **provided
  it complies with AG 54** (R44).

#### R43. Variable Annuity Model Regulation (Model #250)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-250.pdf
- **Doc type:** model regulation (print: "NAIC Model Laws… — October 2007")
- **Fetched:** yes (local text extraction; TOC and Section 7 read) [R43]
- **Annotation:** **Correction to the task brief:** #250 is the **Variable Annuity Model
  Regulation**, not the Annuity Disclosure Model Regulation (that is **#245**, R45) — verified
  from both model-law prints and independently from AG 54, which cites "NAIC Model 250,
  Variable Annuity Model Regulation" [R43][R45][R44]. The regulation covers insurer
  qualification to issue variable annuities, separate accounts, contract filing, required
  contract provisions, nonforfeiture benefits, required reports, and agent qualification
  [R43]. **Section 7 is the load-bearing part for modelling.** §7.A excludes the same
  categories as Model #805 (reinsurance, qualifying group retirement plans, premium deposit
  funds, investment annuities, immediate annuities, deferred annuities in payout, reversionary
  annuities, out-of-state deliveries) [R43]. **§7.B is the boundary rule:** "To the extent
  that a variable annuity contract provides benefits that do not vary in accordance with the
  investment performance of a separate account before the annuity commencement date, the
  contract shall contain provisions that satisfy the requirements of [Model #805] and shall
  not otherwise be subject to this section" [R43] — so the **fixed account inside a VA is
  tested against Model #805**, assuming 100% of considerations allocated to the fixed account
  [R43]. §7.C requires paid-up annuity benefits on cessation of considerations, and lump-sum
  surrender provisions where offered [R43]. AG 54 (R44) exists precisely because Model #250
  defines variable annuities by reference to separate-account investment experience and
  non-unitized ILVA accounts do not automatically satisfy it [R44].
- **Matters for:** variable-annuity (primary); registered-index-linked-annuity (the exemption
  route runs through Model #250 + AG 54); the fixed account of any VA.

#### R44. Actuarial Guideline LIV — Nonforfeiture Requirements for Index-Linked Variable Annuity Products (AG 54)
- **Publisher:** NAIC (adopted by Life Actuarial (A) Task Force 12/11/2022; adopted by Life Insurance and Annuities (A) Committee 2/24/2023) [R44]
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-liv-230224.pdf
- **Doc type:** actuarial guideline text (6-page PDF including project history, © 2023 NAIC)
- **Fetched:** yes (local text extraction; **complete guideline read**) [R44]
- **Annotation:** **This is the RILA-specific NAIC guideline the brief asked me to verify —
  it exists, its number is LIV (54), and I read it end to end.** Purpose: "to specify the
  conditions under which an Index-Linked Variable Annuity (ILVA) is consistent with the
  definition of a variable annuity and exempt from Model 805 and specify nonforfeiture
  requirements consistent with variable annuities" [R44]. The NAIC deliberately adopts the
  term **ILVA** over "RILA"/"structured annuity" to signal that compliant designs are
  variable annuities first [R44]. **The mechanism a model must implement:** an ILVA account
  is not unitized, so the guideline requires **Interim Values** to be materially consistent
  with the value of a **Hypothetical Portfolio = a Fixed Income Asset Proxy + a Derivative
  Asset Proxy**, less a provision for reasonably expected or actual **Trading Costs** at the
  time the Interim Value is calculated [R44]. The Index Strategy Base must equal the Strategy
  Value at term start; the Fixed Income Asset Proxy is a hypothetical bond whose book value
  starts at (Index Strategy Base − Derivative Asset Proxy value) and, at unchanged yield,
  accretes to the Index Strategy Base at term end [R44]. Derivative Asset Proxy assumptions
  (implied volatilities, risk-free rates, dividend yields) must be consistent with observable
  market prices wherever possible, valued by Black-Scholes, Monte Carlo, or other
  market-consistent techniques [R44]. Non-Hypothetical-Portfolio methodologies are permitted
  **only** on a demonstration of material consistency across each Index Strategy / Index
  Strategy Term combination "under a reasonable number of realistic economic scenarios that
  include index changes that test crediting constraints and recognize initial option pricing
  market conditions" [R44]. An **actuarial memorandum with actuarial certifications is
  required with each ILVA product filing**, covering equity between contract holder and
  company, market-consistency of the derivative assumptions, material consistency of the
  contractual Interim Values, and the reasonableness of Trading Costs [R44]. Nonforfeiture
  benefits for in-scope Index Strategies must comply with **Model #250 Section 7 excluding
  §7.B**, with net investment return consistent with the Interim Value requirements [R44].
  **Effective for all contracts, riders, endorsements and amendments issued on or after
  July 1, 2024** [R44]. Whether an MVA is included or excluded, and any MVA formula, is left
  to the states under the equity principle — a deliberate drafting decision recorded in the
  project history [R44]. **Consequence:** an ILVA that fails this guideline is not a variable
  annuity and falls under Model #805 (R42) [R44].
- **Matters for:** registered-index-linked-annuity (primary and definitional);
  variable-annuity with buffered index strategies.

#### R45. Annuity Disclosure Model Regulation (Model #245)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-245.pdf
- **Doc type:** model regulation (print: "NAIC Model Laws… — Summer 2021")
- **Fetched:** yes (local text extraction; Sections 1 and 3 read; Section 6 and Appendix A structure confirmed from the TOC) [R45]
- **Annotation:** The annuity counterpart to Model #582 — and the correct model number is
  **#245**, not #250 (see R43). It sets minimum disclosure for annuity contracts and, in
  **Section 6, standards for annuity illustrations**, with **Appendix A providing an annuity
  illustration example**; Sections 5 (disclosure document and Buyer's Guide) and 7 (report to
  contract owners) carry the rest [R45]. **Scope (Section 3) is what a modeller must read
  first:** the regulation applies to all group and individual annuity contracts and
  certificates **except** (A) immediate and deferred annuities **containing no
  non-guaranteed elements**; (B) annuities funding ERISA plans, 401(a)/401(k)/403(b),
  414/457 governmental and church plans, and nonqualified deferred compensation
  arrangements — with a carve-back for employee-elective-contribution arrangements involving
  direct solicitation where two or more fixed annuity providers are offered; (C)
  non-registered variable annuities sold only to accredited investors/qualified purchasers in
  exempt transactions; and (D) transactions in variable annuities and other registered
  products complying with SEC and FINRA disclosure/illustration rules — though the **Buyer's
  Guide is still required in variable annuity sales** [R45]. A drafting note flags NSMIA
  preemption risk over the §3.D(1) sunset language [R45].
- **Matters for:** fixed-indexed-annuity (primary — FIA illustrations of non-guaranteed
  index credits are the live use case); fixed-deferred-annuity with non-guaranteed
  crediting; immediate-annuity and deferred-income-annuity only if they carry
  non-guaranteed elements; variable-annuity and registered-index-linked-annuity largely
  exempt via §3.D but still owe the Buyer's Guide.

#### R46. Suitability in Annuity Transactions Model Regulation (Model #275)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-275.pdf
- **Doc type:** model regulation (print: "NAIC Model Laws… — Spring 2020" — this print **is** the 2020 best-interest revision)
- **Fetched:** yes (local text extraction; TOC and Section 1 read) [R46]
- **Annotation:** The 2020 best-interest revision, adopted by the NAIC on **February 13, 2020**
  [unverified as to the exact adoption date — the print carries "Spring 2020" and the
  best-interest text, which confirms the substance]. Section 1.A states the purpose plainly:
  to require producers "to act in the best interest of the consumer when making a
  recommendation of an annuity and to require insurers to establish and maintain a system to
  supervise recommendations" [R46]. The structure is Purpose / Scope / Authority / Exemptions
  / Definitions / **Duties of Insurers and Producers (Section 6)** / Producer Training /
  Compliance Mitigation and Penalties / Recordkeeping / Effective Date, with **three
  appendices**: the Insurance Agent (Producer) Disclosure For Annuities, Consumer Refusal to
  Provide Information, and Consumer Decision to Purchase an Annuity Not Based on a
  Recommendation [R46]. Section 6 organises the best-interest obligation into four
  obligations — **care, disclosure, conflict of interest, and documentation** — aligned with
  SEC Regulation Best Interest [unverified — from NAIC and industry summaries, not read in the
  section text]. **Modelling relevance is indirect but real:** best-interest supervision
  changes exchange/1035 activity and therefore surrender and replacement assumptions, and the
  producer-disclosure appendix affects distribution cost structures. Requirements are intended
  to supplement, not replace, Model #245 disclosure [unverified].
- **Matters for:** all annuity product types at the distribution/behavior-assumption level;
  most acute for fixed-indexed-annuity and registered-index-linked-annuity sales.

---

### 3. Capital — C-3 Phase II and the VA framework reform

#### R47. C-3 RBC Instructions and Appendices (incorporating the Academy's C3 Phase II Report for variable annuities)
- **Publisher:** American Academy of Actuaries C3 Life and Annuity Capital Work Group, transmitted to the NAIC Life RBC Working Group (memo dated November 24, 2009); the instructions themselves are NAIC RBC instructions
- **URL:** https://content.naic.org/sites/default/files/inline-files/committees_e_capad_lrbc_C3_RBC_instructions_package.pdf
- **Doc type:** RBC instructions package with appendices
- **Fetched:** yes (local text extraction; transmittal memo, "Calculation of the Total Asset Requirement," "Application of the Tax Adjustment," and "Calculation of the Standard Scenario Amount" read) [R47]
- **Annotation:** The mechanics of **C-3 Phase II** market-risk RBC for variable annuities, as
  incorporated into the Life RBC instructions. **Appendix 2 directly incorporates the
  Academy's June 2005 "Recommended Approach for Setting Risk-Based Capital Requirements for
  Variable Annuities and Similar Products"** (the C3 Phase II Report); Appendix 3 incorporates
  the September 2009 C3 Phase III report for life products [R47]. **The calculation a model
  must reproduce:** (A) run stochastic scenarios on prudent best-estimate assumptions with
  calibrated fund performance distributions; (B) for each scenario compute accumulated
  statutory surplus including federal income tax and take the negative of the lowest present
  value as that scenario's asset requirement, modelling statutory reserve as equal to the
  working reserve; (C) **set the Total Asset Requirement at CTE 90 — the average of the worst
  10% of scenario asset requirements** (capital plus starting reserve); (D) **RBC = the excess
  of the Total Asset Requirement over statutory reserves**, subject to the Standard Scenario
  and the smoothing/transition rules, then combined with C1CS for covariance [R47]. A
  **Tax Adjustment** is required where modelled tax reserves are set equal to Working Reserves
  but actual tax reserves exceed them at the start of the projection, correcting the
  understatement of modelled tax expense via a factor `f` derived from the reserve ratio at
  the worst duration [R47]. The **Standard Scenario Amount** is a floor: a single prescribed
  projection of account values with specified returns and prescribed assumptions, and where it
  exceeds the stochastic result it becomes the TAR before tax adjustment [R47]. **Caveat for
  implementers:** this print states a **35% federal income tax rate** and predates both TCJA
  and the 2018–2020 VA framework reform [R47]; use it for structure, and R48 plus the current
  VM-21 (R35) and Life RBC instructions for parameters.
- **Matters for:** variable-annuity (primary); registered-index-linked-annuity written on a
  VA chassis; any contract in VM-21 scope, since VM-21 §§4.A–4.E and the RBC requirements are
  identical apart from tax treatment [R35].

#### R48. Variable Annuity Statutory Reserve and Capital Reform — QIS II Public Report and Executive Summary
- **Publisher:** Oliver Wyman, for the NAIC Variable Annuity Issues (E) Working Group (VAIWG)
- **URL (public report):** https://content.naic.org/sites/default/files/committee_related_documents/cmte_e_va_issues_wg_related_qis_ii_public_report.pdf
- **URL (executive summary):** https://content.naic.org/sites/default/files/committee_related_documents/cmte_e_va_issues_wg_related_qis_ii_executive_summary.pdf
- **Doc type:** quantitative impact study reports, both dated **February 12, 2018**
- **Fetched:** yes, both (local text extraction; background, purpose and recommendation sections read) [R48]
- **Annotation:** **These are the adopting-era analytical documents behind the 2018–2020 NAIC
  variable annuity reserve and capital framework reform** — the reform that produced the 2020
  VM-21 and the revised C-3 Phase II. History as recorded: the NAIC enacted C3 Phase II in
  2006 and AG 43 in 2009; "the complex interplay of these standards challenged VA statutory
  capital management and, in part, motivated VA writers to seek capital management solutions
  via captive reinsurers," prompting the NAIC to engage Oliver Wyman, whose preliminary report
  came September 10, 2015, followed by **QIS I** (fifteen companies, February–July 2016),
  recommendations to the VAIWG on **August 23, 2016** with redlined AG 43 and C3 Phase II
  guidance on September 26, 2016 (R38 is that redline), a 60-day exposure from September 15,
  2016, and then **QIS II** in 2017 [R48]. **Diagnosed root causes:** penalties for
  economic-based hedging (fully hedging fair value *increased* capital requirements and RBC
  ratio volatility); structural deficiencies in the Standard Scenario that prevented
  alignment with the stochastic calculation it governs; and lack of harmonization in scenario
  projection practice [R48]. **Design principles preserved:** principles-based reserving, a
  book-value statutory approach, the "time-to-worst" accumulated-deficiency measure,
  real-world capital markets scenarios, and a Standard Scenario construct to govern
  assumptions [R48]. **Key parameterisation outcome:** the C3 charge is computed as the
  difference between a higher-confidence "CTE High" amount and the statutory reserve, both on
  the same distribution of projected deficiencies; CTE High was provisionally CTE 98, and QIS
  II recommended **CTE 95 with a 25% scalar** under the alternative equity scenarios, chosen
  so that hedging would reduce a company's total funding requirement at a typical target RBC
  ratio [R48]. Equity scenario calibration was tested over a 1926–2016 window [R48].
- **Matters for:** variable-annuity (primary); registered-index-linked-annuity on a VA
  chassis. Read alongside R35 (the VM-21 phase-in that implements the reform) and R47.

---

### 4. Federal securities regulation

#### R49. Registration for Index-Linked Annuities and Registered Market Value Adjustment Annuities; Amendments to Form N-4 for Index-Linked Annuities, Registered Market Value Adjustment Annuities, and Variable Annuities; Other Technical Amendments
- **Publisher:** U.S. Securities and Exchange Commission
- **URL:** https://www.govinfo.gov/content/pkg/FR-2024-07-24/html/2024-14925.htm (89 Fed. Reg. 59978, July 24, 2024). The SEC's own PDF, https://www.sec.gov/files/rules/final/2024/33-11294.pdf, **returned HTTP 403** and was not fetched.
- **Doc type:** final rule (adopting release)
- **Fetched:** yes, via govinfo.gov [R49]; publication metadata independently corroborated by GAO's rule report, https://www.gao.gov/products/b-336553 (fetched) [R49b]
- **Annotation:** **Release Nos. 33-11294; 34-100450; IC-35273; File No. S7-16-23; RIN
  3235-AN30** [R49]. Federal Register citation **89 Fed. Reg. 59978 (July 24, 2024)**;
  **effective September 23, 2024** [R49][R49b]. **Compliance date: May 1, 2026** — initial
  registration statements for RILAs, registered MVA annuities and variable annuities filed on
  or after that date must comply with amended Form N-4, and RILAs previously registered on
  Forms S-1 or S-3 must file a Rule 485(a) post-effective amendment on Form N-4 by that date
  [unverified as to the mechanics — the date is consistently reported across filing-agent and
  law-firm summaries; the release's section II.J was not read in full]. **Statutory driver:**
  the **Registration for Index-Linked Annuities Act**, enacted as Division AA, Title I of the
  **Consolidated Appropriations Act, 2023**, which directed the Commission to adopt a new RILA
  registration form within 18 months [R49]. **What it requires:** RILA and registered MVA
  issuers must register on **Form N-4** rather than S-1/S-3; provide tailored disclosure of
  **cap rates, participation rates, buffers and floors**, contract adjustments and surrender
  charges; use layered disclosure with a **Key Information Table** in prescribed format;
  optionally use summary prospectuses for continuous offerings; pay registration fees annually
  on net issuances; and comply with Rule 156 on sales literature [R49].
- **Matters for:** registered-index-linked-annuity (primary); variable-annuity (Form N-4 was
  amended for them too); fixed-deferred-annuity written with a registered market value
  adjustment.

#### R50. Updated Disclosure Requirements and Summary Prospectus for Variable Annuity and Variable Life Insurance Contracts (Rule 498A adopting release)
- **Publisher:** U.S. Securities and Exchange Commission
- **URL:** https://www.govinfo.gov/content/pkg/FR-2020-05-01/html/2020-05526.htm (the SEC's own PDF at https://www.sec.gov/files/rules/final/2020/33-10765.pdf returned HTTP 403 and was not fetched)
- **Doc type:** final rule (adopting release)
- **Fetched:** yes, via govinfo.gov [R50]
- **Annotation:** **Release Nos. 33-10765; 34-88358; IC-33814; File No. S7-23-18; RIN
  3235-AK60**; **effective July 1, 2020**, with certain provisions effective January 1, 2022
  [R50]. Adopted **Rule 498A**, an optional layered-disclosure framework letting variable
  contract issuers satisfy prospectus delivery through an **Initial Summary Prospectus** for
  new investors and an **Updating Summary Prospectus** for existing investors, with the full
  statutory prospectus and SAI available online free and on request in paper [R50]. The
  mandatory **Key Information Table** consolidates five topics — fees and expenses, risks,
  restrictions on access, taxes, and conflicts of interest — in standardized order to allow
  cross-product comparison [R50]. Forms **N-4 and N-6** were modernized to condense summary
  information, reflect the prevalence of optional benefit riders, and require **Inline XBRL**
  tagging of specified prospectus disclosures [R50]. The Commission's rationale was that
  bundled variable contract prospectuses frequently exceed 100 pages [R50].
- **Matters for:** variable-annuity (primary); registered-index-linked-annuity (Rule 498A was
  later extended to registered non-variable annuities — see R51).

#### R51. 17 C.F.R. § 230.498A — Summary prospectuses for separate accounts offering variable annuity and variable life insurance contracts and for offering registered non-variable annuity contracts
- **Publisher:** U.S. Government (Code of Federal Regulations), via Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/cfr/text/17/230.498A
- **Doc type:** regulation (current text)
- **Fetched:** yes [R51]
- **Annotation:** The operative rule text, and the reason to cite it separately from R50: the
  **current title has been extended to "and for offering registered non-variable annuity
  contracts"** [R51], reflecting the 2024 RILA rulemaking (R49). It deems a compliant summary
  prospectus a prospectus under Securities Act §10(b) for delivery purposes [R51]. **Delivery
  obligations are satisfied when** the summary prospectus reaches the investor by the time the
  contract is delivered; the summary meets the content requirements; the registrant keeps
  current statutory prospectuses and related documents accessible on a specified website for
  at least 90 days; and paper copies are furnished on request within three business days
  [R51]. Applies to registrants on **Forms N-3, N-4 and N-6** [R51].
- **Matters for:** variable-annuity; registered-index-linked-annuity.

#### R52. SEC Form N-4 — Registration statement for separate accounts organized as unit investment trusts (as amended for RILAs and registered MVA annuities)
- **Publisher:** U.S. Securities and Exchange Commission
- **URL:** https://www.sec.gov/files/formn-4.pdf
- **Doc type:** registration form
- **Fetched:** **no — sec.gov returned HTTP 403 to the fetch tool on 2026-08-04.** The URL is
  genuine (it appears in SEC search indexing), but the form text was not retrieved.
- **Annotation:** The form itself is the disclosure schema a variable annuity or RILA product
  must populate. Its current content requirements are described first-hand in the adopting
  releases that created and amended them — **R50** for the post-2020 structure (condensed
  summary, optional benefits, Key Information Table, Inline XBRL) and **R49** for the RILA/MVA
  extension (cap rates, participation rates, buffers, floors, contract adjustments, surrender
  charges) [R49][R50]. For a modelling library the value is mainly in *reverse*: the fee table
  and Key Information Table define the charge taxonomy (mortality and expense risk charge,
  administrative charge, contract maintenance fee, optional benefit rider charges, surrender
  charges) that a VA/RILA cash flow model must expose as parameters.
- **Matters for:** variable-annuity; registered-index-linked-annuity.

#### R53. SEC Rule 151A and Annuities: Issues and Legislation (CRS Report R40656)
- **Publisher:** Congressional Research Service
- **URL:** https://www.everycrsreport.com/reports/R40656.html
- **Doc type:** other (congressional research report; secondary but authoritative on legislative history)
- **Fetched:** yes [R53]
- **Annotation:** The clean history of **why fixed indexed annuities are not registered
  securities**, which a product library needs in order to justify treating FIA and RILA as
  different regulatory animals. Rule 151A, finalized **December 17, 2008** and published
  January 16, 2009 after roughly 4,800 comments, would have classified indexed annuities as
  securities where "the amounts payable by the insurer… are more likely than not to exceed"
  the guaranteed minimums, effective January 12, 2011 [R53]. In **American Equity Investment
  Life Insurance Co. v. SEC**, the **U.S. Court of Appeals for the D.C. Circuit** held on
  July 21, 2009 that the SEC's classification was reasonable but its analysis of effects on
  efficiency, competition and capital formation inadequate, and **vacated Rule 151A on
  July 12, 2010** [R53]. **Dodd-Frank § 989J** (P.L. 111-203, signed July 21, 2010 — the
  "Harkin amendment") then directed the SEC to treat annuities meeting specified conditions
  as **exempt securities**, returning them to state insurance regulation [R53]. Net effect for
  a model library: FIAs are state-regulated non-registered products governed by Model #805
  (R42), Model #245 (R45) and AG 33/35 (R39/R40); RILAs, which expose the contract holder to
  index losses, are registered and governed additionally by R49–R52 and AG 54 (R44).
- **Matters for:** fixed-indexed-annuity (primary); registered-index-linked-annuity (by
  contrast).

#### R54. FINRA Rule 2330 — Members' Responsibilities Regarding Deferred Variable Annuities
- **Publisher:** Financial Industry Regulatory Authority
- **URL:** https://www.finra.org/rules-guidance/rulebooks/finra-rules/2330
- **Doc type:** self-regulatory organization rule (current text)
- **Fetched:** yes [R54]
- **Annotation:** Governs broker-dealer conduct in **recommended purchases and exchanges of
  deferred variable annuities and recommended initial subaccount allocations**; it does **not**
  reach reallocations among subaccounts, and excludes 401(k)/403(b)/457 tax-qualified plans
  unless an individual participant receives a personalized recommendation [R54]. Before
  recommending, a member must have a reasonable basis to believe the transaction is suitable
  under Rule 2111 and that the customer has been informed of the **surrender period and
  surrender charge** and the **potential tax penalty on redemption before age 59½** [R54]. A
  **registered principal must review and approve the application no later than seven business
  days after an OSJ receives a complete and correct application package** [R54]. Written
  supervisory procedures, surveillance for inappropriate exchange rates among associated
  persons, and documented training programs are required [R54]. **Modelling relevance:** the
  principal-review window and exchange surveillance are the proximate regulatory brake on 1035
  exchange velocity (R56) and therefore on VA replacement-driven surrender assumptions.
- **Matters for:** variable-annuity (primary); registered-index-linked-annuity (registered
  products distributed through broker-dealers) [unverified as to whether FINRA applies
  Rule 2330 to RILAs specifically — the rule text says "deferred variable annuities"].

---

### 5. Federal tax

#### R55. 26 U.S.C. § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- **Publisher:** Legal Information Institute, Cornell Law School (U.S. Code)
- **URL:** https://www.law.cornell.edu/uscode/text/26/72
- **Doc type:** statute (current text)
- **Fetched:** yes [R55]
- **Annotation:** The core annuity tax section, and the one an illustration or in-force system
  must implement. **§72(b) exclusion ratio:** the excluded portion of each annuity payment
  bears the same ratio to the payment as the **investment in the contract** bears to the
  **expected return**; the exclusion is capped at unrecovered investment [R55]. Investment in
  the contract equals premiums paid less prior excludable distributions [R55]. **§72(e)
  amounts not received as annuities:** for pre-annuity-starting-date distributions from
  deferred annuities the **LIFO / income-first rule** applies — income out first, basis second
  — in contrast to the ratable basis recovery of annuitized payments [R55]. **The aggregation
  rule:** "all annuity contracts issued by the same company to the same policyholder during
  any calendar year shall be treated as 1 annuity contract" [R55] — a real modelling
  requirement for multi-contract policyholders. **§72(q):** a **10% penalty** on the includible
  portion of distributions from non-qualified annuity contracts, with exceptions including
  age 59½, death, disability, substantially equal periodic payments, and amounts allocable to
  investment before August 14, 1982 [R55]. **§72(t)** is the parallel 10% additional tax on
  early distributions from qualified plans and IRAs [R55]. **§72(s):** the contract must
  provide that on the holder's death after annuitization the remaining interest distributes at
  least as rapidly as under the pre-death method, and on death before annuitization the entire
  interest within five years, subject to a beneficiary-life-expectancy exception [R55] — the
  provision that shapes death-benefit payout modelling. **§72(u):** contracts held by
  non-natural persons lose deferral, with the **primary annuitant** treated as the holder
  [R55].
- **Matters for:** all annuity product types — fixed-deferred-annuity,
  fixed-indexed-annuity, variable-annuity, registered-index-linked-annuity,
  immediate-annuity, deferred-income-annuity.

#### R56. 26 U.S.C. § 1035 — Certain exchanges of insurance policies
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/1035
- **Doc type:** statute (current text)
- **Fetched:** yes [R56]
- **Annotation:** Tax-free exchange relief, and the asymmetry matters. Permitted: **life →
  life, endowment, annuity, or qualified long-term care**; **endowment → endowment (with
  payments beginning no later than under the original), annuity, or qualified LTC**;
  **annuity → annuity or qualified LTC**; **qualified LTC → qualified LTC** [R56].
  **An annuity cannot be exchanged tax-free for a life insurance contract** [R56]. Relief does
  not apply to transfers having the effect of transferring property to a non-U.S. person
  [R56]. **Modelling relevance:** 1035 exchanges are the dominant source of both new-business
  premium and surrender activity in the deferred annuity market, so an exchange assumption is
  a first-class input; the annuity→life prohibition constrains which replacement flows a model
  should even contemplate. Read with FINRA Rule 2330 (R54) and Model #275 (R46), which
  together throttle exchange velocity in the registered and best-interest channels.
- **Matters for:** fixed-deferred-annuity; fixed-indexed-annuity; variable-annuity;
  registered-index-linked-annuity; immediate-annuity and deferred-income-annuity (as exchange
  destinations).

#### R57. 26 C.F.R. § 1.401(a)(9)-6 — Required minimum distributions for defined benefit plans and annuity contracts (QLAC rules)
- **Publisher:** Legal Information Institute, Cornell Law School (CFR)
- **URL:** https://www.law.cornell.edu/cfr/text/26/1.401(a)(9)-6
- **Doc type:** Treasury regulation (current text)
- **Fetched:** yes [R57]
- **Annotation:** The regulation that makes **qualifying longevity annuity contracts** possible
  and constrains their design. Distributions under a QLAC "must commence not later than a
  specified annuity starting date that is no later than the first day of the month next
  following the **85th anniversary**" of the employee's birth [R57]. The contract may not
  offer "any commutation benefit, cash surrender right, or other similar feature" after the
  required beginning date, subject to a 90-day rescission exception [R57] — i.e., a QLAC is
  modelled with **no surrender value**, which removes the entire lapse module from the
  liability. Dollar limitations are set in paragraph (q)(2) [R57] (see R58 for the current
  **$200,000** figure and the elimination of the 25%-of-account-balance limit). The regulation
  also governs annuity payments generally: distributions must be **periodic annuity payments
  for life, joint lives, or a period certain**, at **uniform intervals not exceeding one
  year**, and **nonincreasing** except as permitted [R57] — the rule that forbids most
  increasing-payment DIA designs in qualified money. Actuarial increases are required for
  employees retiring after age 70½ from April 1 following that birthday until commencement,
  using reasonable actuarial assumptions [R57].
- **Matters for:** deferred-income-annuity (primary — QLACs are DIAs in qualified money);
  immediate-annuity; fixed-deferred-annuity used as an IRA funding vehicle.

#### R58. Required Minimum Distributions — Final Regulations (T.D. 10001)
- **Publisher:** Internal Revenue Service / U.S. Treasury (Federal Register, 89 Fed. Reg., July 19, 2024)
- **URL:** https://www.govinfo.gov/content/pkg/FR-2024-07-19/html/2024-14542.htm
- **Doc type:** final rule (Treasury Decision)
- **Fetched:** yes, via govinfo.gov [R58]
- **Annotation:** **T.D. 10001; RIN 1545-BP82; published July 19, 2024; effective September 17,
  2024; applicable for calendar years beginning January 1, 2025** (with §1.402(c)-2 applying
  to distributions on or after that date) [R58]. Finalizes regulations under IRC §§401(a)(9),
  402(c), 403(b), 408, 457 and 4974, incorporating SECURE and SECURE 2.0 changes [R58].
  **The annuity-relevant content:** SECURE 2.0 **§202** directed amendments to §1.401(a)(9)-6
  that **eliminate the 25%-of-account-balance limitation on QLAC premiums**, **raise the
  dollar cap from $125,000 to $200,000** (inflation-adjusted), permit joint-and-survivor
  benefits to survive divorce under qualified-domestic-relations-order conditions, and add a
  **90-day free-look rescission** [R58]. The regulations also address **bifurcation** where an
  annuity is purchased with part of an individual account — the annuity payments satisfy
  §1.401(a)(9)-6 while the residual account satisfies §1.401(a)(9)-5 — and SECURE 2.0 **§204**
  adds an elective **partial annuitization** alternative under which the required amount is the
  excess of the total required amount for the year over the annuity amount for that year,
  aggregating the annuity contract value with the remaining account balance [R58].
- **Matters for:** deferred-income-annuity (QLAC design and pricing); immediate-annuity;
  fixed-deferred-annuity and variable-annuity held in qualified accounts (RMD-driven
  withdrawal behaviour, which is a major driver of GLWB activation timing — see R64).

---

### 6. Mortality and experience

#### R59. NAIC Model Rule (Regulation) for Recognizing a New Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities (Model #821), with the corresponding VM-M definitions
- **Publisher:** NAIC
- **URL (model):** https://content.naic.org/sites/default/files/model-law-821.pdf
- **URL (VM-M definitions):** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (VM-M §1.I–§1.M, §2.C; same document as R3)
- **Doc type:** model regulation (print: "NAIC Model Laws… — January 2013") plus valuation manual appendix
- **Fetched:** yes, both (local text extraction) [R59]
- **Annotation:** The statutory annuity mortality basis. Model #821 recognizes, for the minimum
  standard of valuation of annuity and pure endowment contracts, the **1983 Table "a"**, the
  **1983 GAM Table**, the **Annuity 2000 Mortality Table**, the **2012 Individual Annuity
  Reserving (2012 IAR) Mortality Table**, and the **1994 GAR Table**, with Appendices I–IV
  printing the **2012 IAM Period Table** (female and male, age nearest birthday) and
  **Projection Scale G2** (female and male) [R59]. **The 2012 IAR is a generational table**:
  VM-M §1.J states it contains rates q<sub>x</sub><sup>2012+n</sup> derived from combining the
  2012 IAM Period Table with Scale G2, and prints the application formula
  **q<sub>x</sub><sup>2012+n</sup> = q<sub>x</sub><sup>2012</sup> × (1 − G2<sub>x</sub>)<sup>n</sup>**,
  with the result **rounded to three decimal places per 1,000** and — a genuine implementation
  trap the manual calls out explicitly — the rounding applied **from the 2012 period rate each
  time, never by compounding an already-rounded prior-year rate** [R59]. Worked example given:
  male age 30, q<sup>2012</sup> = 0.741 → q<sup>2014</sup> = 0.741 × 0.99² = 0.7262541 → 0.726
  (not 0.727) [R59]. VM-M §2.C defines the **2012 IAM Basic Table** as the unloaded table
  underlying the Period Table, developed from the 2002 experience table projected to 2012, and
  records that the underlying **2000–2004 Payout Annuity Mortality Experience Study** covered
  immediate annuities, annuitizations and life settlement options from **16 companies**,
  **excluding substandard annuities, structured settlement annuities and variable payout
  annuities** [R59] — an exclusion that matters when the model's block includes those.
  The 2012 IAM/Scale G2 tables themselves live in **AP&P Manual Appendix A-821** [R59][R33].
- **Matters for:** immediate-annuity; deferred-income-annuity (valuation mortality);
  fixed-deferred-annuity and fixed-indexed-annuity (annuitization and GLWB payout phases);
  variable-annuity (VM-21 prescribes percentages of the 2012 IAM Basic Table with Scale G2 for
  prudent-estimate mortality on contracts with VAGLBs and roll-up GMDBs [R35]).

#### R60. 2012 Individual Annuity Reserving Table — Report of the joint American Academy of Actuaries / Society of Actuaries Payout Annuity Table Team
- **Publisher:** American Academy of Actuaries and Society of Actuaries (joint subgroup of the Life Experience Subcommittee), presented to the NAIC Life Actuarial Task Force
- **URL:** http://actuary.org/wp-content/uploads/2017/11/Payout_Annuity_Report_09-28-11.pdf (https:// redirects to http:// on the same path)
- **Doc type:** table development report, **September 2011** (chair: Mary Bahna-Nolan)
- **Fetched:** yes (local text extraction; title page, TOC, and the margin/loading sections read) [R60]
- **Annotation:** The development report behind R59 — what a modeller needs when justifying or
  stress-testing the valuation basis. LATF's charge was to produce a new annuity valuation
  mortality table "including projection scales and margins necessary to make the table suitable
  for standard valuation purposes for individual annuities"; the IAR Table is the composition
  of **three pieces**: the 2012 IAM Basic Table, the margin, and Projection Scale G2 [R60].
  **The margin, as recommended by the Team and agreed by LATF, is 10% at all ages up to and
  including 100, grading down 1% per year above age 100 until the ultimate mortality cap of
  0.40000 is invoked**, producing a zero margin at the cap [R60] — LATF concluded there was no
  compelling reason to depart from the approach or level used for the a2000 Table [R60]. The
  report also covers graduation, younger-age and older-age adjustments (Kannisto-form
  extrapolation at the oldest ages), the derivation of improvement from 2002 to 2012, and A/E
  analysis against the unloaded 2012 IAM adjusted to January 1, 2007 (the midpoint of the
  underlying experience) [R60]. Reserve-impact comparisons against the a2000 Table are
  tabulated [R60].
- **Matters for:** immediate-annuity; deferred-income-annuity; any product whose valuation
  mortality is the 2012 IAR.

#### R61. 2020–2024 Individual Payout Annuity Mortality Experience Study
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL:** https://www.soa.org/resources/experience-studies/2026/2020-24-individual-payout/
- **Doc type:** experience study report (landing page; free public report PDF plus a paid Standard Data Package)
- **Fetched:** yes (landing page) [R61]
- **Annotation:** The current annuitant-longevity experience basis. **23 parent company groups
  covering 26 individual companies, over 80% of industry sales during the study period, 3.1
  million contract-years and $33 billion of annual-income-years of exposure, and 143,190
  deaths over five years** [R61]. Results are presented against the **2012 IAM Table**, the
  prior study, and U.S. population mortality [R61] — i.e., it is directly usable as the A/E
  evidence for a prudent-estimate or best-estimate deviation from R59. Deliverables: a free
  public PDF, and a purchasable Standard Data Package with executive summary, in-depth
  analysis and interactive dashboards [R61]. Predecessor: the **2014–2019 Individual Payout
  Annuity Mortality Experience Study** (December 2022), 25 companies, ~80% of market, ~4.3
  million contract-years, ~236,000 deaths [R61][R65].
- **Matters for:** immediate-annuity (primary); deferred-income-annuity; annuitized and GLWB
  payout phases of fixed-deferred-annuity, fixed-indexed-annuity and variable-annuity.

#### R62. Fixed Indexed Annuity Policyholder Behavior Experience Studies (2021–2022, with 2019–2020 predecessor)
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL (2021–22):** https://www.soa.org/resources/experience-studies/2024/21-22-fia/
- **URL (2019–20):** https://www.soa.org/resources/experience-studies/2023/19-20-fia/
- **Doc type:** experience study reports (landing pages; free public report plus paid data package)
- **Fetched:** yes, both landing pages [R62]
- **Annotation:** The public basis for FIA surrender and withdrawal assumptions. The **2021–2022**
  study covers **12 companies, ~4.8 million contracts of surrender exposure by count, $526
  billion of contract value exposure, over 227,000 surrenders and $15.9 billion of
  withdrawals**, with comparisons "to several expected bases of policyholder behavior,
  including the current valuation standard" [R62]. The **2019–2020** study covers **17 parent
  company groupings / 20 individual companies, roughly two-thirds of industry new sales and
  assets, ~4.9 million contracts valued at $503 billion, over 195,000 surrenders and $13.7
  billion of withdrawals**, analysing withdrawal rates, surrender rates and additional premium
  deposited [R62]. **The headline finding a model must encode** is the interaction between
  surrender-charge expiry and the GLWB rider: in the year the surrender charge expires, the
  surrender rate was about **10% for contracts with a GLWB rider versus about 33% without**
  [unverified — reported consistently in LIMRA/SOA press coverage of the 2019–20 study, not
  read in the report PDF]. That is the difference between a shock-lapse assumption and a
  rider-suppressed one, and it is product-design-dependent, not a single industry number.
- **Matters for:** fixed-indexed-annuity (primary); fixed-deferred-annuity by analogy.

#### R63. Fixed Rate Deferred Surrender Experience Studies (2023–24, with 2015–2022 predecessor)
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL (2023–24):** https://www.soa.org/resources/experience-studies/2025/2023-24-fixed-rate-deferred/
- **URL (2015–2022):** https://www.soa.org/49c0c1/globalassets/assets/files/resources/experience-studies/2024/15-22-frds.pdf (report PDF, not fetched)
- **Doc type:** experience study reports
- **Fetched:** **partially** — both titles, dates and URLs verified from the SOA's Individual
  Annuity Experience Studies index (R65) [R65]; neither landing page nor report PDF fetched
  individually
- **Annotation:** The surrender basis for MYGA / fixed-rate deferred annuities, where the shock
  at surrender-charge expiry is far more violent than in FIA because there is no living-benefit
  rider anchoring the contract holder. Reported surrender rates by contract count in the year
  the surrender charge expired were roughly **51.7% for 2020 and 55.7% for 2021** [unverified —
  from trade-press coverage of the 2015–2022 study, not read in the report]. Compare with the
  ~10%/~33% FIA figures at R62 — the same event, three very different assumptions, driven by
  rider presence and rate-differential dynamics.
- **Matters for:** fixed-deferred-annuity (primary, especially multi-year guaranteed annuities).

#### R64. Variable Annuity Contract Holder Behavior and Guaranteed Living Benefit Utilization Studies (2022–2024, with the 2019–2021 and the 2013–2018 GLB utilization series)
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL (2022–24):** https://www.soa.org/resources/experience-studies/2025/2022-24-va-livingbenefit/
- **URL (2019–21):** https://www.soa.org/resources/experience-studies/2023/19-21-va/ (not fetched; verified via R65)
- **URL (2015 experience GLB utilization report PDF):** https://www.soa.org/globalassets/assets/Files/resources/research-report/2018/variable-annuity-guaranteed-utilization.pdf (not fetched)
- **Doc type:** experience study reports
- **Fetched:** yes (2022–24 landing page) [R64]; the others verified via R65
- **Annotation:** The public basis for VA and RILA behavior assumptions. The **2022–2024**
  study covers **17 companies representing approximately 48% of new premium for VAs and
  RILAs**, about **11.5 million contracts valued at $1.5 trillion**, with over **625,000
  surrender events and 4 million withdrawal transactions** ($56.7 billion of contract value
  withdrawn) [R64] — note the explicit inclusion of RILAs in the premium-share denominator,
  which is the first sign that the studies now span both chassis. **What a GLWB model needs
  from the utilization series** (from the earlier reports): roughly **79% of owners taking
  withdrawals withdrew at or near the maximum permitted amount (up to 110%)**, about **55%
  withdrew between 90% and 110% of the maximum**, most withdrawals run through **systematic
  withdrawal plans** which keep owners inside the guaranteed maximum, owners rarely add
  premium after contract year two, and **activation clusters at the RMD age** [unverified —
  these figures come from SOA/LIMRA summaries of the 2013/2015-experience utilization studies,
  not read in the report PDFs]. The RMD clustering is the reason R58 (the 2024 RMD final
  regulations) is a *behavioral* input to a GLWB model, not merely a tax one.
- **Matters for:** variable-annuity (primary); registered-index-linked-annuity;
  fixed-indexed-annuity with GLWB riders.

#### R65. SOA Individual Annuity Experience Studies — index
- **Publisher:** Society of Actuaries Research Institute
- **URL:** https://www.soa.org/research/topics/indiv-ann-exp-study-list/
- **Doc type:** other (index/navigation page)
- **Fetched:** yes (complete list read) [R65]
- **Annotation:** The authoritative index of publicly available individual annuity experience
  studies, and the cheapest way to check whether an assumption source has been superseded. It
  catalogues, by year: payout annuity mortality (2000–04, 2005–08, 2009–13, 2014–19,
  2020–24); fixed indexed annuity behavior (2013–15, 2016–18, 2019–20, 2021–22); fixed rate
  deferred surrender (2015–22, 2023–24); variable annuity contract owner behavior (2019–21)
  and the VA guaranteed living benefits utilization series (2011 through 2018 experience);
  **deferred annuity mortality (2011–2015)**; **structured settlement mortality (1997,
  2000–08, 2009–13, 2005–17)**; a **Deferred Annuity Persistency Report (2006)**; and
  "Analysis of Mortality Experience Under Variable and Fixed Individual Annuities During the
  Deferred Period" (2006) [R65]. The last two are the only public sources located for
  **deferred-period** (pre-annuitization) annuitant mortality, which is a distinct and much
  under-served assumption relative to payout mortality.
- **Matters for:** all annuity product types — assumption-source discovery and supersession
  checking.

---

### 7. Professional standards and practice notes

#### R66. Implementation of Requirements for Principle-Based Reserves for Variable Annuities — 2022 Edition of VM-21 (Practice Note Supplement)
- **Publisher:** American Academy of Actuaries, Variable Annuity Reserves & Capital Work Group of the Life Practice Council (chair: Connie Tang)
- **URL:** https://actuary.org/wp-content/uploads/2022/02/VA_PN_Supplement_Final.pdf
- **Doc type:** practice note supplement, **February 2022** (34 pages)
- **Fetched:** yes (local text extraction; title page, introduction, acronym list and full table of contents read) [R66]
- **Annotation:** The implementation companion to VM-21 (R35), written specifically for the
  **2020 revisions** to VA principle-based reserves and capital. Its eight sections are:
  **1. Transition; 2. Standard Projection** (including product/contractual conflicts);
  **3. Asset Modeling & Discount Rates; 4. Scenarios; 5. Hedging; 6. C-3 Phase 2 RBC;
  7. Disclosures; 8. Miscellaneous** [R66] — i.e., it maps almost exactly onto the decisions a
  VA cash flow model has to make. Its acronym list is itself a useful glossary (CDHS,
  Company-Specific Market Path, CTE with Prescribed Assumptions, Direct Iteration Method,
  Guarantee Actuarial Present Value, GPVAD, IMR) [R66]. **Explicitly not binding:** it "is not
  a promulgation of the Actuarial Standards Board, is not an actuarial standard of practice,
  is not binding upon any actuary" [R66]. Two cautions it states directly: readers must check
  differences between the VM-21 edition the note was written against and the edition
  applicable to the current valuation, since the Valuation Manual is a living document; and
  the note **does not cover state variations such as New York Regulation 213** [R66].
- **Matters for:** variable-annuity (primary); registered-index-linked-annuity valued under
  VM-21.

#### R67. Utilization Assumptions of Guaranteed Living Benefits for Deferred Annuities — A Resource and Discussion Guide
- **Publisher:** American Academy of Actuaries, Life Experience Committee (chair: Donna Claire)
- **URL:** https://actuary.org/wp-content/uploads/2024/05/life-paper-GLBs.pdf
- **Doc type:** resource/discussion guide, **May 2024**
- **Fetched:** yes (local text extraction; title page and front matter read) [R67]
- **Annotation:** The profession's assembled thinking on the single hardest assumption in the
  deferred annuity model — when and how intensely contract holders use a guaranteed living
  benefit. The Academy is explicit about its status: it "is not a promulgation of the
  Actuarial Standards Board, is not an actuarial standard of practice (ASOP), is not binding
  upon any actuary… This document should not be treated as guidance but rather it should be
  read and utilized as a list of considerations and resources on a particular topic" [R67].
  Treat it as a checklist of drivers (moneyness, age and RMD timing, qualified versus
  non-qualified, distribution channel, systematic withdrawal plan enrolment, rider type) to
  test a utilization assumption against, and as a bridge from the experience data in R64 to a
  prudent-estimate assumption that will satisfy VM-21 §10 (R35) or VM-22 §10 (R36).
- **Matters for:** variable-annuity; fixed-indexed-annuity with GLWB;
  registered-index-linked-annuity; fixed-deferred-annuity with living benefit riders.

#### R68. Fixed Indexed Annuities — Product Mechanics and Risk Management
- **Publisher:** American Academy of Actuaries, Life Experience and Assumptions Committee (chair: Kyle Wan)
- **URL:** https://actuary.org/wp-content/uploads/2026/02/life-FIA-policypaper.pdf
- **Doc type:** policy/issue paper, **February 2026**
- **Fetched:** yes (local text extraction; title page, table of contents and the crediting-method sections read) [R68]
- **Annotation:** The most current and most directly implementable public description of FIA
  mechanics. Contents: Introduction; **Examples of Index Crediting Methods**;
  investment strategy, ALM and **hedging considerations**; and **Reserves and Regulations**
  [R68]. It defines the crediting levers precisely — **participation rate** (the percentage of
  index return credited: 10% index return at 80% participation with a 6% cap), **cap**, and
  **spread** (a percentage deducted from the index return) — and works a full **annual
  point-to-point** example against the S&P 500 showing a 7% cap and 0% floor binding in a year
  when the normalized index rose 25% [R68]. It notes the industry shift toward **custom
  indices with built-in volatility control**, and covers averaging and monthly point-to-point
  variants [R68]. It explains the **option budget** framing — the insurer allocates a portion
  of premium to derivatives to hedge the index-linked credits — and links crediting design back
  to **nonforfeiture limits and the nonforfeiture rate** [R68], i.e., to R42.
- **Matters for:** fixed-indexed-annuity (primary); registered-index-linked-annuity (shared
  crediting vocabulary); fixed-deferred-annuity with index options.

#### R69. Index-Linked Variable Annuity (ILVA) / Registered Index-Linked Annuity (RILA) Policy Paper
- **Publisher:** American Academy of Actuaries, Index-Linked Variable Annuity Subcommittee (chair: Elizabeth Keith)
- **URL:** https://actuary.org/wp-content/uploads/2025/12/Life-PolicyPaper120225.pdf
- **Doc type:** policy paper, **December 2025**
- **Fetched:** yes (local text extraction; title page, table of contents and the interim-value sections read) [R69]
- **Annotation:** The bridge between AG 54's legal text (R44) and an actual RILA implementation.
  It describes the product family — downside protection via a **buffer, dual-direction buffer,
  or floor**, and upside parameters of **cap rate, participation rate, buffer and floor**, with
  more complex strategies adding **trigger rates, dual-direction buffers and performance
  locks**, noting that design complexity constrains the company's ability to hedge and value
  the strategy [R69]. It restates the two AG 54 guiding principles (interim values provide
  equity between contract holder and company; interim values are consistent with the
  Hypothetical Portfolio over the Index Strategy Term) and explains the consequence: a
  compliant ILVA is exempt from Model #805 and subject instead to variable annuity
  nonforfeiture under **Model #250** [R69]. It covers interim values under AG 54 **and**
  separately under the **Interstate Insurance Compact** standards, and addresses **U.S.
  statutory risk-based capital** for ILVAs [R69], plus practical valuation issues such as
  hedge-cost inference and bid/mid/ask spread treatment in Trading Costs [R69].
- **Matters for:** registered-index-linked-annuity (primary); variable-annuity with buffered
  strategies.

#### R70. ASOP No. 54 — Pricing of Life Insurance and Annuity Products
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/pricing-of-life-insurance-and-annuity-products/
- **Doc type:** actuarial standard of practice (adopted June 2018; effective December 1, 2018)
- **Fetched:** yes [R70]
- **Annotation:** **Not in R1–R34** and squarely applicable to annuity work. It applies when
  actuaries perform pricing services for life insurance and annuity products at initial
  development or when charges or benefits change for future sales, covering individual policy
  forms and group master contracts with individually-priced certificates; **it excludes the
  pricing of reinsurance contracts** [R70]. It requires the actuary to consider the principal's
  profitability criteria, risk-capital approach and risk-management policies; select
  profitability metrics (it lists IRR, ROE, profit margin, ROA, value of new business, and
  break-even year); develop or select models accommodating product design, time horizon,
  granularity, **dynamic assumptions, economic scenarios, asset returns, accounting bases,
  risk capital frameworks, taxes and risk-mitigation strategies**; set internally consistent
  assumptions with margins where credible data is lacking; perform sensitivity and stochastic
  risk evaluation; and implement governance controls including model validation and
  independent review [R70]. For an annuity reference model this is the standard that justifies
  a pricing-mode output (profit metrics, dynamic lapse, hedge cost) alongside the valuation
  outputs.
- **Matters for:** all annuity product types at the pricing layer.

#### R71. ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Revised Edition)
- **Publisher:** Actuarial Standards Board
- **URL (standard PDF, current adopted edition):** http://www.actuarialstandardsboard.org/wp-content/uploads/2023/01/asop010_207.pdf
- **Doc type:** actuarial standard of practice, **Revised Edition, adopted by the ASB December 2022, Doc. No. 207**
- **Fetched:** yes (local text extraction; title page, full table of contents, §1.1–1.4 read) [R71]
- **Annotation:** **Not in R1–R34**, and it is the professional-standards counterpart to the
  LDTI accounting standard already catalogued at R34. **Effective for actuarial services
  related to the preparation or review of insurance company GAAP financial statements
  applicable to fiscal periods ending on or after May 1, 2023** [R71]. Scope: actuarial
  services related to the preparation or review of GAAP financial statements for long-duration
  life, **annuity**, or health products, with the standard yielding to applicable law and to
  authoritative GAAP guidance (ASC, SEC Staff Accounting Bulletins) where they conflict [R71].
  Its definitions section is the working vocabulary an LDTI-capable annuity model must
  implement: **Best-Estimate Assumption, Cohort, Deferred Policy Acquisition Cost, Deferred
  Sales Inducements, GAAP Net Premiums, Liability for Future Policy Benefits, Lock-In,
  Market-Estimate Assumption, Market Risk Benefit, Net GAAP Liability, Policy Benefit
  Liability, Premium Deficiency, Risk of Adverse Deviation, and Value of Business Acquired**
  [R71]. Section 3 covers classification of contracts, features and benefits, and the
  best-estimate versus market-estimate assumption split [R71] — the classification decision
  that determines whether a GLWB is an MRB or an insurance liability.
- **Caution:** two ASB pages carry ASOP 10 exposure drafts (an April 2022 proposed revision
  page was fetched and is clearly labelled an exposure draft, not adopted [R71b:
  https://www.actuarialstandardsboard.org/asops/asop-no-10-ssun-u-s-gaap-for-long-duration-life-annuity-and-health-products/]).
  Cite the Doc. No. 207 PDF above, which states adoption on its title page.
- **Matters for:** all annuity product types on the U.S. GAAP measurement basis; most acute
  for variable-annuity and registered-index-linked-annuity (market risk benefits) and
  immediate-annuity / deferred-income-annuity (liability for future policy benefits).

#### R72. IRC Section 807 LB&I Directive Related to Principle-Based Reserves for Variable Annuity Contracts (AG 43/VM-21) and Life Insurance Contracts (VM-20) [brief]
- **Publisher:** Internal Revenue Service, Large Business & International Division
- **URL:** https://www.irs.gov/businesses/corporations/irc-section-807-large-business-and-international-lbi-directive-related-to-principle-based-reserves-for-variable-annuity-contracts-ag-43vm-21-and-life-insurance-contracts-vm-20
- **Doc type:** examination directive
- **Fetched:** **no — irs.gov returned HTTP 404 to the fetch tool on 2026-08-04** on this and on
  a companion §446 hedging-directive URL, both of which appear in irs.gov search indexing. The
  URL is reproduced as surfaced by search; treat the substance below as unverified.
- **Annotation:** Reported as **LB&I-04-0818-015, issued August 24, 2018**, instructing LB&I
  examiners not to challenge an insurance company's determination of tax reserves for variable
  annuity contracts subject to **AG 43 / VM-21** and life contracts subject to **VM-20**, where
  the company reported its 2017 tax reserves in compliance with the directive; otherwise
  regular audit procedures apply [unverified]. Relevant to a model library because it is the
  practical bridge between the statutory annuity engine (R35, R38) and the §807 tax reserve
  (R16). A companion directive on the timing of hedges of variable annuity guaranteed minimum
  benefits under IRC §446 is also indexed on irs.gov [unverified].
- **Matters for:** variable-annuity (tax reserve and hedge tax timing).

---

## Cross-reference: which entries bind which annuity product models

| Product | Binding / relevant entries |
|---------|---------------------------|
| **fixed-deferred-annuity** (incl. MYGA) | **New:** R36 (VM-22 PBR), R37 (VM-V if VM-22-excluded), R39 (AG 33 CARVM), R41 (VM-C guideline family), **R42 (Model #805 nonforfeiture — the load-bearing one)**, R45 (Model #245 if non-guaranteed elements), R46 (Model #275), R55 (IRC §72), R56 (§1035), R57–R58 (if qualified), R59 (payout mortality on annuitization), **R63 (surrender-charge-expiry shock lapse)**, R70 (ASOP 54), R71 (ASOP 10). **Existing:** R1, R3, R16, R26, R27, R29, R32, R33, R34. |
| **fixed-indexed-annuity** | **New:** R36 (VM-22 PBR — Accumulation category), R39 + **R40 (AG 33 + AG 35 index feature, and AG 35's asset-adequacy requirement)**, R41, **R42 incl. §4.C equity-index additional 100bp reduction**, **R45 (annuity illustrations — not AG 49)**, R46, **R53 (why FIAs are not registered)**, R55, R56, R57–R58, R59, **R62 (FIA behavior, GLWB-suppressed shock lapse)**, R64/R67 (if GLWB), **R68 (product mechanics and option budget)**, R70, R71. **Existing:** R1, R3, R16, R26, R27, **R29 (AG 35 requires AAT)**, R32, R33, R34. |
| **variable-annuity** | **New:** **R35 (VM-21)**, R38 (AG 43 for pre-2017 in-force and as the aggregation shell), **R43 (Model #250, incl. §7.B fixed-account carve-out to Model #805)**, R46, **R47 (C-3 Phase II RBC at CTE 90)**, R48 (the reform record), R50–R52 (Rule 498A, Form N-4), **R54 (FINRA 2330)**, R55 (§72), R56, R57–R58, R59 (VM-21 prescribes 2012 IAM Basic × Scale G2 percentages), **R64 (GLB utilization)**, R66 (VM-21 practice note), R67, R70, R71, R72. **Existing:** R1, R3, **R15 (§817(h) diversification)**, R16, R26, R27, R29, R32, R33, **R34 (MRBs)**. |
| **registered-index-linked-annuity (RILA / ILVA)** | **New:** **R44 (AG 54 — definitional)**, R35 (VM-21 where written on a VA chassis), R43 (Model #250 §7 ex §7.B, per AG 54), **R49 (SEC 2024 RILA rule, Form N-4, compliance May 1 2026)**, R51, R52, R46, R53 (by contrast with FIA), R55, R56, R64, **R69 (ILVA/RILA policy paper)**, R68 (shared crediting vocabulary), R47 (RBC), R70, R71. **Existing:** R1, R3, R15, R16, R26, R27, R29, R32, R33, R34. Note: **R42 (Model #805) does *not* apply if and only if AG 54 is satisfied** [R44]. |
| **immediate-annuity (SPIA)** | **New:** **R36 (VM-22 Payout Annuity Reserving Category)**, **R37 (VM-V §1 maximum valuation interest rate)**, R41 (AG IX, IX-B, IX-C), **R59 + R60 (2012 IAR / Model #821)**, **R61 (payout annuity mortality experience)**, R55 (§72(b) exclusion ratio), R56, R57–R58 (if qualified), R70, R71. **Existing:** R1, R3, R16, R27, R29, R32, R33, R34. Explicitly **outside** Model #805 (R42) and Model #250 §7 (R43) [R42][R43]. |
| **deferred-income-annuity (DIA / QLAC)** | **New:** **R36 (VM-22 Payout category — DIA named explicitly)**, **R37 (VM-V §1.A.2.b names DIAs)**, R41, R59 + R60, R61, R55, R56, **R57 (QLAC design: age-85 limit, no commutation/cash surrender)**, **R58 ($200,000 cap, 25% limit eliminated, free-look, divorce)**, R70, R71. **Existing:** R1, R3, R16, R27, R29, R32, R33, R34. |

---

## Gaps and caveats

**Verified findings that correct or sharpen the brief**

1. **Model number correction.** The brief named "#250" as the Annuity Disclosure Model
   Regulation. Verified against both model-law prints and AG 54's own citation: **#245 is the
   Annuity Disclosure Model Regulation (R45)** and **#250 is the Variable Annuity Model
   Regulation (R43)** [R43][R44][R45].
2. **VM-22's scope in the current edition.** The brief asked me to verify rather than assume,
   and the assumption would have been wrong: in the **Jan. 1, 2026 edition, VM-22 is entirely
   the principle-based framework for non-variable annuities**; the maximum valuation interest
   rates for income annuities are **in VM-V Section 1**, not VM-22 [R36][R37]. VM-22 PBR is
   effective for **valuation dates on or after January 1, 2026**, with a three-year elective
   transition and mandatory prospective application three years after the effective date
   [R36].
3. **A RILA-specific NAIC guideline exists and I read it.** It is **Actuarial Guideline LIV
   (AG 54), Nonforfeiture Requirements for Index-Linked Variable Annuity Products**, adopted by
   LATF 12/11/2022 and by the Life Insurance and Annuities (A) Committee 2/24/2023, effective
   for contracts issued **on or after July 1, 2024** [R44]. It is a *nonforfeiture* guideline,
   not a valuation one, and it does **not** appear in the VM-C index [R41].
4. **AG 43 is not simply superseded by VM-21.** VM-21 states that through reference in AG 43,
   VM-21's reserve requirements also apply to pre-2017 contracts outside VM-21's own scope, and
   that the two populations may be reserved as a single aggregated group [R35]. Any statement
   that AG 43 is "replaced" is wrong in a way that changes in-force model scope.
5. **There is no ASOP for principle-based reserves for annuities.** Verified against the full
   ASB standards list: **ASOP 52 is scoped to life products under VM-20**, and no VM-21 or
   VM-22 analogue exists [R70 context; ASB list fetched 2026-08-04]. The nearest professional
   guidance is the non-binding Academy practice note supplement (R66).

**What could not be verified**

- **AG 33 and AG 35 texts (R39, R40).** No free official standalone copy was located on
  content.naic.org or elsewhere; the authoritative text is in the AP&P Manual Appendix C
  (R33), a paid publication. Their **exact titles and continued incorporation** were verified
  from the Valuation Manual's VM-C index [R41], but every substantive statement about their
  mechanics in this file is tagged [unverified]. **This is the single largest hole in the
  annuity library** — formulaic CARVM for fixed and indexed deferred annuities rests on two
  guidelines I could not read.
- **SEC primary documents.** sec.gov returned **HTTP 403** on every attempt (press release
  2024-81, `/files/rules/final/2024/33-11294.pdf`, `/files/formn-4.pdf`). Release metadata and
  substance were recovered from **govinfo.gov** (R49, R50) and **GAO** (R49b), which is why
  those entries are marked fetched. **Form N-4 itself (R52) was never retrieved** — its
  requirements are described only through the adopting releases.
- **The RILA compliance date of May 1, 2026** is consistently reported by filing agents and
  law firms but I did not read section II.J of Release 33-11294, so the date carries
  [unverified] in R49 even though the effective date (September 23, 2024) is verified twice
  [R49][R49b].
- **federalregister.gov and ecfr.gov** both 302-redirect to a bot-block page; govinfo.gov and
  law.cornell.edu were substituted throughout.
- **IRS LB&I directives (R72).** irs.gov returned **HTTP 404** on both directive URLs surfaced
  by search. The control number, date and substance are [unverified].
- **A successor to the 2012 IAR valuation table could not be confirmed to exist.** The LATF
  charges page states generally that the Task Force works "with the American Academy of
  Actuaries and the Society of Actuaries… to develop new mortality tables for valuation and
  minimum nonforfeiture requirements," and lists active subgroups (VM-22, Experience Reporting,
  GOES, Longevity Risk, Variable Annuities Capital and Reserve) — **but it names no annuity
  mortality table project and no IAR replacement** [LATF page fetched 2026-08-04]. **I am not
  asserting that such a project exists.** The 2012 IAR (R59) remains the recognized valuation
  table, while the experience underneath it has moved materially — the 2020–2024 payout study
  (R61) measures against the 2012 IAM basis directly, which is the right place to look for
  evidence of drift.
- **Quantitative behavior figures.** The FIA shock-lapse split (~10% with GLWB vs ~33%
  without), the fixed-rate-deferred shock lapse (~52%/~56%), and the GLWB withdrawal-efficiency
  distribution (~79% at or near maximum) all come from press summaries and landing pages, not
  from the study PDFs, which sit behind paid data packages. They are tagged [unverified] in
  R62, R63 and R64 and should be treated as order-of-magnitude anchors, not calibration
  targets.
- **VM-22 mandatory date.** VM-22 §2.B states the rule as "three years after the effective
  date" without printing a date [R36]; Jan. 1, 2029 is arithmetic, not quotation, and is
  tagged accordingly.
- **C-3 Phase II parameters are stale in R47.** The instructions package read carries a **35%
  federal income tax rate** and predates both TCJA and the 2018–2020 reform [R47]. Its
  *structure* (CTE 90 TAR, RBC = TAR − statutory reserve, Standard Scenario floor, tax
  adjustment) is reliable; its *numbers* are not. Current parameters must come from the
  in-force Life RBC instructions, which were not located as a current standalone document.
- **Deferred-period annuitant mortality** is served publicly by only two dated sources — a
  2011–2015 deferred annuity mortality study and a 2006 analysis — both identified via the SOA
  index (R65) but neither fetched. This assumption is materially under-evidenced relative to
  payout mortality.

**Retrieval status summary**

| R# | Short name | Fetched |
|----|-----------|---------|
| R35 | VM-21 (VM 2026 ed.) | yes (local extraction) |
| R36 | VM-22 (VM 2026 ed.) | yes (local extraction) |
| R37 | VM-V §1 Income Annuities | yes (local extraction) |
| R38 | AG XLIII (VAIWG redline) | yes (local extraction) |
| R39 | AG XXXIII | no (title verified via R41) |
| R40 | AG XXXV | no (title verified via R41) |
| R41 | VM-C guideline index | yes (local extraction) |
| R42 | Model #805 | yes (local extraction) |
| R43 | Model #250 | yes (local extraction) |
| R44 | AG LIV (AG 54) | yes (local extraction, complete) |
| R45 | Model #245 | yes (local extraction) |
| R46 | Model #275 | yes (local extraction) |
| R47 | C-3 RBC instructions package | yes (local extraction) |
| R48 | Oliver Wyman QIS II (both docs) | yes (local extraction) |
| R49 | SEC Rel. 33-11294 (RILA) | yes (govinfo); sec.gov PDF 403 |
| R49b | GAO B-336553 rule report | yes |
| R50 | SEC Rel. 33-10765 (Rule 498A) | yes (govinfo); sec.gov PDF 403 |
| R51 | 17 CFR 230.498A | yes |
| R52 | SEC Form N-4 | **no (sec.gov 403)** |
| R53 | CRS R40656 (Rule 151A / §989J) | yes |
| R54 | FINRA Rule 2330 | yes |
| R55 | IRC §72 | yes |
| R56 | IRC §1035 | yes |
| R57 | Treas. Reg. §1.401(a)(9)-6 | yes |
| R58 | T.D. 10001 (RMD final regs) | yes (govinfo) |
| R59 | Model #821 + VM-M | yes (local extraction, both) |
| R60 | 2012 IAR development report | yes (local extraction) |
| R61 | 2020–24 payout annuity mortality | yes (landing page) |
| R62 | FIA behavior 2021–22 / 2019–20 | yes (both landing pages) |
| R63 | Fixed rate deferred surrender | partial (via R65 index) |
| R64 | VA behavior / GLB utilization | yes (2022–24 landing page) |
| R65 | SOA annuity experience index | yes |
| R66 | AAA VM-21 practice note supp. | yes (local extraction) |
| R67 | AAA GLB utilization guide | yes (local extraction) |
| R68 | AAA FIA product mechanics | yes (local extraction) |
| R69 | AAA ILVA/RILA policy paper | yes (local extraction) |
| R70 | ASOP 54 | yes |
| R71 | ASOP 10 (Doc. No. 207) | yes (local extraction) |
| R72 | IRS LB&I §807 directive | **no (irs.gov 404)** |
