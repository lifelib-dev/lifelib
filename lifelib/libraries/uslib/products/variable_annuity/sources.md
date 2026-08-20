# Sources

Source ids, titles, publishers, URLs, access dates and fetched/not-fetched markers are
carried over **verbatim** from `_research/variable-annuity.md`, the citation ground
truth for the [S#]/[R#] tags used in `product-spec.md` and `technical-notes.md`. **Ids are
never renumbered.** Sources present in the research file but not cited in either document
are dropped; **none were dropped here — all of S1–S8 and R1–R13 are cited.** No new
sources were fetched at drafting, so nothing below is marked "added at drafting".

Access date for all citations: **2026-08-04**, except the four **AP&P Manual appendix
entries R151, R153, R156 and R157**, accessed **2026-08-06** and added to this directory
afterwards.

Retrieval note carried over from the research file: `sec.gov` and `efts.sec.gov` return
HTTP 403 to a plain fetch. All SEC documents below were retrieved with an explicit declared
User-Agent (SEC's stated requirement for programmatic access) and read in full as text.
Every document marked "Retrieved: YES" was actually downloaded and read.

---

## Primary product sources [S#]

(uslib-variable_annuity-s1)=

### S1. Jackson National Life Insurance Company — Perspective II® Flexible Premium Variable and Fixed Deferred Annuity — statutory prospectus dated April 28, 2025
- Publisher: Jackson National Life Insurance Company, through Jackson National
  Separate Account – I (CIK 0000927730)
- Doc type: SEC Form N-4 statutory prospectus, filed as Form 485BPOS
  (accession 0000927730-25-000086), ~4.9 MB HTML
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773025000086/ck0000927730-20250422.htm
- Retrieved: YES (converted to ~1.28 MB plain text and read in relevant part)
- Role in this library: **implementation anchor.** Full GLWB/GMDB algebra (GWB, GAWA,
  Bonus Base, step-up, GWB adjustment, excess-withdrawal proportional reduction), the
  charge-increase/opt-out mechanic, the contract-value-zero regime, and Appendices F–J of
  historical rate tables.

(uslib-variable_annuity-s2)=

### S2. Jackson National Life Insurance Company — Perspective II® Initial Summary Prospectus (Summary Prospectus for New Investors), April 28, 2025
- Publisher: same as S1; filed as exhibit EX-99.(o)(1) to the S1 registration statement
- Doc type: Rule 498A Initial Summary Prospectus (~16 pages)
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773025000086/jnlpiiafter6-24x19initials.htm
- Retrieved: YES (full text read)
- Role in this library: the base contract charge stack, withdrawal charge schedule,
  contract maintenance charge, fund expense range and premium limits.

(uslib-variable_annuity-s3)=

### S3. Jackson National Life Insurance Company — Rate Sheet Prospectus Supplement dated April 27, 2026 (Perspective II)
- Publisher: same as S1; SEC Form 497 (accession 0000927730-26-000157)
- Doc type: rate sheet prospectus supplement (6 pages) — the document that carries
  the *currently offered* rider charges, GAWA percentages, bonus percentages, GWB
  adjustment percentages and GMDB roll-up percentages
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773026000157/jnlpiiafter6-24x19rateshee.htm
- Retrieved: YES (full text read)
- Role in this library: the **dated current parameter set** (rate-sheet date 2026-04-27) for
  the representative GLWB and GMDB elections.

(uslib-variable_annuity-s4)=

### S4. American General Life Insurance Company (Corebridge Financial) — Polaris Advisory Variable Annuity — prospectus dated May 1, 2026
- Publisher: American General Life Insurance Company, Variable Separate Account
  (CIK 0000729522); SEC Form 485BPOS, accession 0001193125-26-186414
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526186414/d79162d485bpos.htm
- Retrieved: YES (~732 KB plain text; fee table, living-benefit and death-benefit
  sections, Appendix C fee formula and Appendix H examples read)
- Role in this library: the **VIX-linked non-discretionary rider fee formula** variant, the
  Secure Value Account investment requirement, the daily-step-up design, and the cited fact
  that the rider fee stops when contract value falls to zero.

(uslib-variable_annuity-s5)=

### S5. American General Life Insurance Company (Corebridge) — Rate Sheet Prospectus Supplement dated May 1, 2026 (Polaris Advisory)
- Doc type: SEC Form 497, accession 0001193125-26-164551 (3 pages)
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526164551/d113668d497.htm
- Retrieved: YES (full text read)
- Role in this library: cited for the rate-sheet mechanism (current withdrawal and income
  percentages reset by Form 497 filing with a 10-day advance-filing commitment).

(uslib-variable_annuity-s6)=

### S6. American General Life Insurance Company (Corebridge) — Polaris Choice IV — prospectus dated May 1, 2026
- Doc type: SEC Form 485BPOS, accession 0001193125-26-173379
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526173379/d97533d485bpos.htm
- Retrieved: YES (~503 KB plain text; fee table, penalty-free withdrawal, nursing
  home waiver, purchase-payment and issue-age rules read)
- Carried-over note: "This contract is no longer available for purchase by new
  contract Owners." [S6] — it is a recently-sold, currently-in-force design.
- Role in this library: the commission-share charge/withdrawal-charge trade-off, the
  ±0.25%-per-quarter VIX fee band for the commission class, and the GLWB RMD relief rule.

(uslib-variable_annuity-s7)=

### S7. Equitable Financial Life Insurance Company / Equitable Financial Life Insurance Company of America — Retirement Cornerstone® Series — prospectus dated May 1, 2026
- Publisher: Separate Account No. 70 (CIK 0001537470) and Equitable America
  Variable Account No. 70A; SEC Form 485BPOS, accession 0001193125-26-169230
- URL fetched: https://www.sec.gov/Archives/edgar/data/1537470/000119312526169230/d120089d485bpos.htm
- Retrieved: YES (~1.45 MB plain text; definitions, benefits, GIB mechanics,
  charges and expenses sections read)
- Role in this library: the **unbundled daily charge components** (the source of the 0.30%
  administrative component in the representative charge decomposition), the
  **Treasury-formula roll-up rate** variant (10-year CMT + 1.00%, floored 4%, capped 8%),
  the bifurcated account architecture, and the annual (not quarterly) rider charge
  frequency exception.

(uslib-variable_annuity-s8)=

### S8. The Lincoln National Life Insurance Company — Lincoln ChoicePlus℠ product suite / Lincoln ChoicePlus Assurance℠ — Form N-4 post-effective amendment filed April 23, 2026 (prospectuses and rate sheets dated May 1, 2026)
- Publisher: Lincoln Life Variable Annuity Account N (CIK 0001048606); SEC Form
  485BPOS, accession 0001104659-26-047599 (~20 MB HTML bundling several rate-sheet
  supplements and prospectuses)
- URL fetched: https://www.sec.gov/Archives/edgar/data/1048606/000110465926047599/tm265235d1_485bpos.htm
- Retrieved: YES (~2.68 MB plain text; the three Lincoln ProtectedPay®/4LATER®/
  i4LIFE® rate sheets, the Key Information and Fee Tables, the ProtectedPay
  Enhancement/Account Value Step-up mechanics, and Appendix C discontinued-rider
  charges were read)
- Role in this library: the **step-up-triggered fee reset** variant with its reversing
  opt-out and the no-opt-out $100,000-premium trigger; the **two-table post-depletion
  payout** variant; the explicit enhancement-vs-step-up mutual-exclusivity rule that
  settles the [std] bonus/step-up ordering; and the GMDB-priced-into-M&E design.
- Carried-over caveat: Lincoln share-class attribution is ambiguous — the accession bundles
  several rate sheets and prospectuses, and the fee table read cannot be attributed with
  certainty to a single named product among the ChoicePlus Assurance share classes.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(uslib-variable_annuity-r1)=

### R1. NAIC — Valuation Manual, Jan. 1, 2026 Edition — **VM-21: Requirements for Principle-Based Reserves for Variable Annuities**
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457-page PDF downloaded; VM-21 occupies PDF pages 142–226,
  manual pages 21-1 through 21-76; Sections 1, 2, 3, 4, 6, 7, 10 read)

(uslib-variable_annuity-r2)=

### R2. NAIC / Oliver Wyman — "Variable Annuity Statutory Reserve and Capital Reform — QIS II Executive Summary", February 12, 2018
- Publisher: NAIC Variable Annuities Issues (E) Working Group (report by Oliver Wyman)
- URL fetched: https://content.naic.org/sites/default/files/committee_related_documents/cmte_e_va_issues_wg_related_qis_ii_executive_summary.pdf
- Retrieved: YES (13-page PDF; background and QIS I/QIS II overview read)

(uslib-variable_annuity-r3)=

### R3. NAIC — Life Risk-Based Capital instructions, **LR027 Interest Rate Risk and Market Risk** (C-3 Phase II for VAs)
- Publisher: NAIC Capital Adequacy (E) Task Force
- URL fetched: https://content.naic.org/sites/default/files/inline-files/LR027%20mod%20for%20vol%20res%202020.pdf
- Retrieved: YES (5-page PDF; full 7-step process, CTE(98) definition, RBC formula,
  phase-in and smoothing read)

(uslib-variable_annuity-r4)=

### R4. American Academy of Actuaries — "Implementation of Requirements for Principle-Based Reserves for Variable Annuities – 2022 Edition of VM-21" (Practice Note Supplement), February 2022
- Publisher: Variable Annuity Reserves & Capital Work Group, Life Practice Council, AAA
- URL fetched: https://actuary.org/wp-content/uploads/2022/02/VA_PN_Supplement_Final.pdf
- Retrieved: YES (34-page PDF; introduction, acronym list, background, C-3 Phase 2
  Q&A and disclosures Q&A read)

(uslib-variable_annuity-r5)=

### R5. American Academy of Actuaries — "Utilization Assumptions of Guaranteed Living Benefits for Deferred Annuities: A Resource and Discussion Guide", May 2024
- Publisher: Life Experience Committee, AAA (Donna Claire, chair)
- URL fetched: https://actuary.org/sites/default/files/2024-05/life-paper-GLBs.pdf
  (note: `www.actuary.org` 301-redirects to `actuary.org`; the redirect target was
  fetched directly)
- Retrieved: YES (18-page PDF, read in full including both sample utilization tables)
- Carried-over caveat: the sample utilization tables are built for a **non-qualified FIA**,
  not a VA, and must be applied with care.

(uslib-variable_annuity-r6)=

### R6. U.S. Securities and Exchange Commission — **Form N-4** (reference copy, version effective September 23, 2024)
- URL fetched: https://www.sec.gov/files/formn-4.pdf
- Retrieved: YES (65-page PDF; general instructions and item index read)
- Note: this product research file retrieved Form N-4 successfully with a declared
  User-Agent; the cross-product entry [REG-R52] records a **failed** fetch of the same URL
  (HTTP 403). Prefer [R6] for first-hand Form N-4 facts.

(uslib-variable_annuity-r7)=

### R7. SEC Rule 498A, 17 CFR 230.498A — summary prospectuses for variable annuity and variable life contracts
- URL fetched: https://www.law.cornell.edu/cfr/text/17/230.498A
- Retrieved: YES

(uslib-variable_annuity-r8)=

### R8. FINRA Rule 2330 — Members' Responsibilities Regarding Deferred Variable Annuities
- URL fetched: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2330
- Retrieved: YES

(uslib-variable_annuity-r9)=

### R9. Internal Revenue Code § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES

(uslib-variable_annuity-r10)=

### R10. Treas. Reg. § 1.817-5 — Diversification requirements for variable annuity, endowment, and life insurance contracts
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.817-5
- Retrieved: YES

(uslib-variable_annuity-r11)=

### R11. Actuarial Standards Board — ASOP No. 52, "Principle-Based Reserves for Life Products under the NAIC Valuation Manual"
- URL fetched: http://www.actuarialstandardsboard.org/asops/principle-based-reserves-life-products-naic-valuation-manual/
- Retrieved: YES
- Carried-over caveat: the retrieved text scopes ASOP 52 to policies "subject to **VM-20**
  requirements". Treat any claim that "ASOP 52 governs VM-21" as [unverified].

(uslib-variable_annuity-r12)=

### R12. Actuarial Standards Board — Standards of Practice index (titles and effective dates for ASOP Nos. 22, 52, 56)
- URL fetched: http://www.actuarialstandardsboard.org/standards-of-practice/
- Retrieved: YES

(uslib-variable_annuity-r13)=

### R13. Society of Actuaries Research Institute & LIMRA — "2022–2024 Variable Annuity Guaranteed Living Benefit / Contract Holder Behavior Study"
- URL fetched: https://www.soa.org/resources/experience-studies/2025/2022-24-va-livingbenefit/
- Retrieved: YES (landing page only — the detailed report is a paid data package)

---

## Cross-product regulatory references [REG-R#]

These are cited with the **[REG-R#]** prefix to avoid collision with the product research
file's own R-numbering. They resolve against a **single shared numbering space running
R1–R157**, curated at `references/regulatory-and-actuarial-references.md`, with most
of the **R73–R149** block **unused**:

- **R1–R34** — research provenance `_research/regulatory-actuarial.md` (the original
  life bibliography; several entries also bind annuity models, and that file's companion
  table records how each one applies).
- **R35–R72** — research provenance `_research/regulatory-actuarial-annuities.md` (the
  annuity continuation of the same space; it opens at R35 precisely because R1–R34 are
  frozen and must not be renumbered).
- **R151–R157** — the seven NAIC *Accounting Practices and Procedures Manual* appendix items
  read at first hand on **2026-08-06**: `_research/appp-ag33.md` (R151),
  `_research/appp-ag35.md` (R152), `_research/appp-a820-a821-a822.md` (R153),
  `_research/appp-a830.md` (R154) and `_research/appp-a585-a250-a255-a270.md` (R155,
  R156, R157). **R150** is the NAIC principle-based reserving topic page and is not cited
  here. Four of the seven are cited in this directory — **R151, R153, R156 and R157** — and
  their entries are reproduced below from
  `references/regulatory-and-actuarial-references.md`.

Entries cited by the two documents in this directory:

| Tag | Short title | Research file | Retrieval status (per that file) |
|---|---|---|---|
| REG-R15 | 26 U.S.C. §817 (esp. §817(h)) — variable contract diversification | regulatory-actuarial.md | fetched |
| REG-R16 | 26 U.S.C. §807 — tax reserves | regulatory-actuarial.md | fetched |
| REG-R26 | ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products | regulatory-actuarial.md | fetched |
| REG-R27 | ASOP No. 7 — Life or Health Cash Flow Analysis | regulatory-actuarial.md | fetched |
| REG-R29 | ASOP No. 22 — Opinions Based on Asset Adequacy Analysis | regulatory-actuarial.md | fetched |
| REG-R31 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual | regulatory-actuarial.md | fetched |
| REG-R32 | ASOP No. 56 — Modeling | regulatory-actuarial.md | fetched |
| REG-R34 | FASB ASU 2018-12 (LDTI) — market risk benefits | regulatory-actuarial.md | **no (fasb.org 403)** — substance corroborated only from secondary summaries and carried as [unverified] in that file |
| REG-R35 | VM-21 — PBR for Variable Annuities (Valuation Manual, Jan. 1, 2026 ed.) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R36 | VM-22 — PBR for Non-Variable Annuities (Jan. 1, 2026 ed.) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R37 | VM-V §1 — Income Annuities, maximum valuation interest rates | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R38 | Actuarial Guideline XLIII (AG 43) — CARVM for Variable Annuities (VAIWG redline) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R42 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R43 | Variable Annuity Model Regulation (Model #250) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R44 | Actuarial Guideline LIV (AG 54) — ILVA nonforfeiture | regulatory-actuarial-annuities.md | yes (local text extraction, complete) |
| REG-R45 | Annuity Disclosure Model Regulation (Model **#245**) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R46 | Suitability in Annuity Transactions Model Regulation (Model #275) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R47 | C-3 RBC Instructions and Appendices (C-3 Phase II for VAs) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R48 | Oliver Wyman / VAIWG — QIS II Public Report and Executive Summary | regulatory-actuarial-annuities.md | yes (local text extraction, both) |
| REG-R50 | SEC Release 33-10765 — Rule 498A adopting release | regulatory-actuarial-annuities.md | yes (via govinfo); sec.gov PDF 403 |
| REG-R51 | 17 C.F.R. §230.498A (current text, extended to registered non-variable annuities) | regulatory-actuarial-annuities.md | fetched |
| REG-R52 | SEC Form N-4 | regulatory-actuarial-annuities.md | **no (sec.gov 403)** — but fetched first-hand as [R6] above |
| REG-R54 | FINRA Rule 2330 | regulatory-actuarial-annuities.md | fetched (same rule as [R8] above) |
| REG-R55 | 26 U.S.C. §72 — Annuities | regulatory-actuarial-annuities.md | fetched (same statute as [R9] above) |
| REG-R56 | 26 U.S.C. §1035 — Certain exchanges of insurance policies | regulatory-actuarial-annuities.md | fetched |
| REG-R57 | 26 C.F.R. §1.401(a)(9)-6 — RMDs for annuity contracts (QLAC rules) | regulatory-actuarial-annuities.md | fetched |
| REG-R58 | T.D. 10001 — RMD final regulations (July 19, 2024) | regulatory-actuarial-annuities.md | yes (via govinfo) |
| REG-R59 | Model #821 + VM-M — 2012 IAM / 2012 IAR / Scale G2 annuity mortality | regulatory-actuarial-annuities.md | yes (local text extraction, both) |
| REG-R61 | 2020–2024 Individual Payout Annuity Mortality Experience Study | regulatory-actuarial-annuities.md | yes (landing page) |
| REG-R62 | FIA Policyholder Behavior Experience Studies (2021–22, 2019–20) | regulatory-actuarial-annuities.md | yes (both landing pages) |
| REG-R64 | VA Contract Holder Behavior / GLB Utilization Studies (2022–24 and predecessors) | regulatory-actuarial-annuities.md | yes (2022–24 landing page; same landing page as [R13] above) |
| REG-R66 | AAA — VM-21 Practice Note Supplement (Feb. 2022) | regulatory-actuarial-annuities.md | yes (local text extraction; same document as [R4] above) |
| REG-R67 | AAA — Utilization Assumptions of Guaranteed Living Benefits (May 2024) | regulatory-actuarial-annuities.md | yes (local text extraction; same document as [R5] above) |
| REG-R70 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | regulatory-actuarial-annuities.md | fetched |
| REG-R71 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R72 | IRS LB&I §807 directive (AG 43/VM-21 tax reserves) | regulatory-actuarial-annuities.md | **no (irs.gov 404)** — substance [unverified] |

Note on overlaps: [R1]/[REG-R35], [R4]/[REG-R66], [R5]/[REG-R67], [R8]/[REG-R54],
[R9]/[REG-R55], [R11]/[REG-R31] and [R13]/[REG-R64] are the **same documents** reached
through two numbering spaces. Where a fact was extracted first-hand in the product research
file, the [R#] tag is used; where the fact comes from the cross-product annotation, the
[REG-R#] tag is used. Both are given where both apply.

### AP&P Manual appendix entries (R151–R157) newly cited here

Added on **2026-08-06**, when AG 33 and the Appendix A items were read at first hand and the
findings written into `technical-notes.md` (*Known modeling pitfalls*, *Valuation and reserve
pointers*) and `product-spec.md` (*Regulatory context*). Ids, titles, publishers, URLs, access
dates, fetched markers and every carried-forward limit are reproduced from
`references/regulatory-and-actuarial-references.md`; **nothing is renumbered and no flag is
upgraded**. Only the four items this directory actually cites are reproduced — R152 (AG 35),
R154 (A-830) and R155 (A-585) are not cited here and are not carried over. Cross-references
*inside* these entries to ids not reproduced here — **R73** (the AP&P Manual *As of March
2026*), **R33**, **R39**, **R110**, **R101/R102**, **R1** and **R6** — resolve in
`references/regulatory-and-actuarial-references.md`.

**One physical document behind R151–R157.** All seven are appendix items of the NAIC
*Accounting Practices and Procedures Manual, As of March 2026* — the **same 2,117-page
consolidated PDF already catalogued as R73**, a **free download** from `content.naic.org`
(catalogue entry "APPM-2026 … Free Download" on https://content.naic.org/publications;
file https://content.naic.org/sites/default/files/publication-app-manual.pdf). They take
appendix-level ids rather than being folded into R73 so a document can cite **A-820 ¶15** or
**AG 33 *Text* 4** instead of a 2,117-page manual. Each was read by **local text extraction**
from that download. **This supersedes, for these items, the library's earlier record of the
manual as a paid publication that could not be fetched** [REG-R33 — frozen and preserved
unaltered in `references/regulatory-and-actuarial-references.md`](#uslib-reg-r33).

**Edition line, stated once for all seven.** None of these items prints "As of March 2026" on
its own pages. Every extracted page carries only the footer **"© 1999-2026 National
Association of Insurance Commissioners"**, which is a **copyright span, not an adoption,
effective or revision date** for any of these instruments and must never be cited as one. The
"As of March 2026" designation is the manual's own front matter, recorded at R73. The **AP&P
Manual licence** applies unchanged to all of R151–R157: personal and
non-commercial use, no integration "into any software or other publication" without written
NAIC permission, so these items are paraphrased with a paragraph cite and quoted only in short
anchors.

**A-270 (Variable Life Insurance)** was extracted alongside R155 at printed pages A270-1 to
A270-3 = **PDF pages 1097–1099**, but the extraction **assigned it no reference id**. Nothing
in this directory is cited from it, and its guaranteed-minimum-death-benefit reserve
construction is therefore outside the library.

#### REG-R151. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33), as printed in the AP&P Manual
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  **Appendix C — Actuarial Guidelines**; printed pages **AG33-1 to AG33-8** = **PDF pages
  1496–1503**; same physical document as R73
- **Accessed:** 2026-08-06
- **Fetched:** yes (local text extraction; **all eight printed pages read in full** —
  *Background Information*, *Purpose*, *Definitions*, *Text* 1–7 and *Effective Date*)
- **Limits carried forward from `_research/appp-ag33.md`:** the running heads confirm
  Appendix C, but these pages carry **no volume statement** — the **Volume II** placement is
  R73's record, not theirs. They carry **no amendment history, no adoption note and no
  revision log**, so the guideline's printed *Effective Date* of **31 December 1998** cannot be
  reconciled here against the **31 December 1995** date the library carries from IRS
  Rev. Rul. 2002-6 for a differently-titled instrument; **both are recorded and neither is
  presented as settled**. AG 33 contains **no formulas, symbols, tables or factors** beyond the
  7% expense allowance and the 1998–2000 phase-in percentages, and **names no other guideline
  anywhere** — not AG 35, not AG 43. Cite by block (*Background* / *Definitions* / *Text*),
  since all three restart at 1. Spurious intra-word spaces at justified-line breaks are text-layer
  artefacts and were closed up in the research file's quotations.
- **Supersedes in fact:** **R39** ("guideline text not retrieved"), which is frozen and is
  preserved unaltered in `references/regulatory-and-actuarial-references.md`.
- **Note for this directory:** cited for scope, the precedence clause, the elective/non-elective
  classification and the prohibition on experience-based elective incidence — **not** for any
  parameter of this model. AG 33 **never mentions separate accounts, variable annuities, the
  Valuation Manual or PBR**, so its displacement by AG 43/VM-21 rests on its general precedence
  clause and is marked **[std, derived]** where it is relied on.

#### REG-R153. Appendix A-820 — Minimum Life and Annuity Reserve Standards (with Appendix A-821, Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities, and Appendix A-822, Asset Adequacy Analysis Requirements)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  **Volume I, Appendix A — Excerpts of NAIC Model Laws**; **A-820** printed A820-1 to A820-13 =
  **PDF pages 1186–1198**, **A-821** printed A821-1 to A821-6 = **PDF pages 1199–1204**,
  **A-822** printed A822-1 = **PDF page 1205**; same physical document as R73
- **Accessed:** 2026-08-06
- **Fetched:** yes (local text extraction; **A-820 ¶¶1–28 read in full**, **A-821 read in full**
  including the 2012 IAM Period Table and Projection Scale G2 printed at its Appendices I–IV,
  and **A-822's four paragraphs read in full**)
- **Limits carried forward from `_research/appp-a820-a821-a822.md`:** **"As of March 2026"
  is not printed on PDF pp. 1186–1205** — cite the copyright footer for what those pages print.
  **A-821 prints only** the 2012 IAM Period Table and Projection Scale G2; the **1994 GAR** table
  and its `AA_x` factors, the **Annuity 2000** table and **1983 Table "a"** are named and **not
  printed**, so A-821 ¶16 is not computable from library sources, and **no standard is printed for
  individual annuities issued before 1 January 2001**. A-820 **names its life mortality tables
  without printing them** and the **2017 CSO is nowhere in its text**. Three text-layer repairs are
  recorded in the research file rather than hidden: the **lost fraction bar at ¶7.a.i(a)** (the term
  is `(W/2)·(R2 − .09)`), the lost `R1`/`R2` subscripts, and the **¶8.c weighting-factor tables,
  which were reassembled by column position** from a scrambled layer. Two internal oddities are
  recorded as printed and **not reconciled**: **¶22's empty window** and **¶7's "effective date of
  the Codification"**, a threshold whose date A-820 never prints. **Naming trap:** AP&P
  **Appendix A-822 is not NAIC Model #822** (R101/R102) — A-820's own header does not list Model
  #820 while A-822's does.
- **Supersedes in fact:** the A-820 half of **R110**'s limit ("A-820 and A-830 as printed in the
  AP&P Manual were not retrieved"), and, for the paragraphs it carries, the reliance on R1 and R6
  alone. R110 is frozen and is preserved unaltered.
- **Note for this directory:** cited **only** as the destination of A-250 ¶3's delegation and for
  the fact that its ¶15 is the CARVM construction. **No A-820 mechanic, rate, weighting factor or
  mortality table is stated anywhere in this directory** — this product's reserve is VM-21's.

#### REG-R156. Appendix A-250 — Variable Annuities
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  **Volume I, Appendix A — Excerpts of NAIC Model Laws**; printed page **A250-1** = **PDF page
  1095**; same physical document as R73
- **Accessed:** 2026-08-06
- **Fetched:** yes (local text extraction; **the whole item read in full** — three paragraphs,
  seven printed lines of substance)
- **Limit, and it is the point of the entry:** A-250 is **a pointer, not a reserve method**. It
  gives a definition, a separate-account asset-coverage requirement, and a delegation of the
  reserve itself to **Appendix A-820** "in accordance with actuarial procedures that recognize the
  variable nature of the benefits provided and any mortality guarantees". It contains **no
  formula, no symbol, no factor, no table, no CARVM adaptation, no elective-benefit path rule, no
  interim-value rule and not the word CARVM**, and prints **no effective date**. It is cited in
  this directory for that **verified negative finding** as much as for anything it supplies.
- **Note for this directory:** its header names only the **Standard Valuation Law (#820)** and
  **SSAP No. 56—Separate Accounts** — **it does not name Model #250**, so every Model #250
  statement in `product-spec.md` continues to rest on [REG-R43] and not on this print. All three
  of its paragraphs sit under the heading "Definitions"; there is no "Valuation Requirements"
  heading in the item, which is recorded as printed and does not change the effect of ¶3.

#### REG-R157. Appendix A-255 — Modified Guaranteed Annuities
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  **Volume I, Appendix A — Excerpts of NAIC Model Laws**; printed page **A255-1** = **PDF page
  1096**; same physical document as R73
- **Accessed:** 2026-08-06
- **Fetched:** yes (local text extraction; **the whole item read in full** — seven paragraphs)
- **Limit:** like A-250, A-255 delegates the reserve method itself to **Appendix A-820**; what it
  adds is three operative rules — the separate account liability must be at least the surrender
  value produced by **the contract's own market-value-adjustment formula**, a shortfall against the
  market value of the separate account assets must be made good by a transfer into that account,
  and any additional reserve needed to cover future guaranteed benefits must be established.
  **No MVA formula and no parameters for one are printed** — the formula is the contract's. Like
  A-250 it contains **no formula, symbol, factor or table**, does **not mention CARVM**, and prints
  **no effective date**. Its ¶1 definition is separately load-bearing as the test VM-21 §2.A.2 uses
  to exclude contracts falling under VM-A item A-255 (R35); **that exclusion is VM-21's text, not
  A-255's**.
- **Note for this directory:** the representative contract has **no fixed account and no MVA** —
  the Roll-up GMDB election removes the Fixed Account Options [S1] — so A-255 is cited only in the
  MVA-variant pitfall in `technical-notes.md`, and cited there for what it does **not** print.

---

## Provenance note

Extraction details live in `_research/variable-annuity.md`: that file records which fact
came from which source, its [unverified] flags, and its "Gaps and caveats" section — in
particular that **no closed-form MVA factor** was found in any of the four prospectuses
read; that **guaranteed annuity purchase rate tables** were not obtained; that the SOA/LIMRA
behavior study detail is **paywalled**, leaving the VM-21 §6.C prescribed tables [R1] and
the AAA sample tables [R5] as the only public numeric behavior anchors; that **rate sheets
are volatile by design**; that fund expense ranges carry lagging as-of dates; and that
**GMAB mechanics, RILA buffer/floor structures and New York Regulation 213** are outside
its scope.

`_research/regulatory-actuarial-annuities.md` plays the same role for the R35–R72 half of
the [REG-R#] space, including its own verified corrections carried into these documents:
Model **#245** (not #250) is the Annuity Disclosure Model Regulation; the Model #805 indexed
nonforfeiture rate floor is **15 basis points**, not 1%; VM-22 in the 2026 edition is
entirely the PBR framework with income-annuity valuation rates in VM-V §1; AG 43 is **not**
simply superseded by VM-21; and **there is no ASOP for principle-based reserves for
annuities**. `_research/regulatory-actuarial.md` plays that role for R1–R34.

`_research/appp-ag33.md` (R151) and `_research/appp-a585-a250-a255-a270.md` (R155–R157,
plus the unnumbered A-270) are the ground truth for the AP&P Manual appendix material added on
2026-08-06, and `_research/appp-a820-a821-a822.md` for R153. Their two findings that bear on
this product are both **negatives, and are cited as such**: **A-250 supplies no reserve method
for a variable annuity**, only a definition, a per-account asset-coverage floor and a delegation
to A-820; and **A-255 prints no market-value-adjustment formula**, the formula being the
contract's. Neither the ¶16 guaranteed-minimum-death-benefit reserve construction of **A-270**
nor anything else in that item is used anywhere in this directory, A-270 having **no reference
id**.

Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md` are
introduced at drafting and are not attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-variable_annuity-r1
[R11]: #uslib-variable_annuity-r11
[R13]: #uslib-variable_annuity-r13
[R4]: #uslib-variable_annuity-r4
[R5]: #uslib-variable_annuity-r5
[R6]: #uslib-variable_annuity-r6
[R8]: #uslib-variable_annuity-r8
[R9]: #uslib-variable_annuity-r9
[REG-R31]: #uslib-reg-r31
[REG-R35]: #uslib-reg-r35
[REG-R43]: #uslib-reg-r43
[REG-R52]: #uslib-reg-r52
[REG-R54]: #uslib-reg-r54
[REG-R55]: #uslib-reg-r55
[REG-R64]: #uslib-reg-r64
[REG-R66]: #uslib-reg-r66
[REG-R67]: #uslib-reg-r67
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
