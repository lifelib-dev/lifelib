# Sources

Source ids, titles, publishers, URLs, access dates and retrieval markers are carried over
verbatim from `_research/deferred-income-annuity.md` (the citation ground truth for
[S#]/[R#] tags). **Ids are never renumbered.** Sources in the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted (dropped here: **S7**, NYL
official fact sheet, failed fetch; **S10**, Brighthouse QLAC brochure, failed fetch;
**R17**, IRS PLR 201515001, retrieved but found not relevant to DIAs and unused in the
research file itself). **No new sources were fetched at drafting; nothing is marked
"added at drafting."**

**Added 2026-08-06 — three cross-product entries.** **REG-R151** (AG 33), **REG-R153**
(A-820 with A-821 and A-822) and **REG-R154** (A-830) were added after the NAIC *Accounting
Practices and Procedures Manual, As of March 2026* was found to be a **free download** rather
than the paid publication this library had recorded, and were read in full from it. Their
metadata is carried from `references/regulatory-and-actuarial-references.md`,
the citation ground truth for R150–R157. **Nothing is renumbered:** the frozen **REG-R39** ("AG 33 text not retrieved")
and **REG-R110** ("A-820 and A-830 were not retrieved") entries below are preserved exactly as
written and carry **appended** supersession notes rather than edits. **REG-R39 is now cited by
neither document in this directory and is retained anyway**, on the principle that a superseded
record is evidence, not clutter — the same treatment
`references/regulatory-and-actuarial-references.md` gives it.

Access date for all citations: **2026-08-04**, except **REG-R151**, **REG-R153** and
**REG-R154**, accessed **2026-08-06**.

---

## Primary product sources [S#]

(uslib-deferred_income_annuity-s1)=

### S1. New York Life Insurance and Annuity Corporation (NYLIAC) — "New York Life Guaranteed Future Income Annuity II — Product Overview"
- Publisher: NYLIAC (a Delaware corporation), subsidiary of New York Life Insurance
  Company, 51 Madison Avenue, New York, NY 10010. Document distributed by Fidelity
  Insurance Agency, Inc. (authorized distributor); item numbers `969689.8.0`,
  `NYL-DIA-0626`, `49695-20`; © 2026 FMR LLC.
- Doc type: consumer product overview / fact sheet (4 pages). Current vintage (June 2026
  revision code).
- URL fetched: https://communications.fidelity.com/fili/dia/nyl/docs/new_york_life_dfia_factsheet.pdf
- Retrieved: **YES** (full 4-page PDF text extracted)
- Policy form: `ICC11–P101` in most jurisdictions; `211-P101` in some states; state
  variations apply.

(uslib-deferred_income_annuity-s2)=

### S2. Massachusetts Mutual Life Insurance Company — "MassMutual RetireEase Choice — A Flexible Premium Deferred Income Annuity" (client guide)
- Publisher: Massachusetts Mutual Life Insurance Company, Springfield, MA. Document code
  `AN4325 219  CRN202011-221296`; © 2019 MassMutual. PDF hosted on a third-party content
  CDN (`static.contentres.com`), but the document itself is MassMutual's own 32-page
  client guide.
- Doc type: detailed client/product guide (32 pages) — the most contractually granular DIA
  document retrieved.
- URL fetched: https://s3.amazonaws.com/static.contentres.com/media/documents/cda42ab0-617b-4977-94dc-221106c82e4f.pdf
- Retrieved: **YES** (all 32 pages text extracted)
- Contract forms: `FPDIA12` and `ICC12-FPDIA12` (in certain states, including North
  Carolina).
- **VINTAGE CAVEAT carried over:** this guide is from 2019 and predates SECURE 1.0/2.0.
  Its QLAC figures ($130,000 limit, 25%-of-balance limit, RMD age 70½) are **superseded**
  — see [R1] [R2] [R3]. Its *product mechanics* remain the most detailed DIA description
  retrieved and are cited as such. This is the **archetype** for the representative design.

(uslib-deferred_income_annuity-s3)=

### S3. The Guardian Insurance & Annuity Company, Inc. (GIAC) — "Guardian SecureFuture Income Annuity® — A flexible premium deferred income annuity"
- Publisher: The Guardian Insurance & Annuity Company, Inc. (GIAC), a Delaware
  corporation, 7 Hanover Square, New York, NY 10004; wholly owned subsidiary of The
  Guardian Life Insurance Company of America. Document codes
  `641695.4.0 GSFIA-DIA-0118`, `1/15/2018`, `1.956733.103` (Fidelity-distributed version).
  PDF retrieved from a third-party mirror (`qlacs.net`) after the Fidelity-hosted copy
  failed.
- Doc type: consumer fact sheet / brochure (4 pages).
- URL fetched: https://www.qlacs.net/assets/guardian_dia_factsheet.pdf
- Retrieved: **YES** (all 4 pages text extracted)
- **VINTAGE CAVEAT carried over:** January 2018 document; references "the required minimum
  distribution (RMD) age of **70½**" throughout — superseded by SECURE 1.0/2.0. Product
  mechanics still cited; age references flagged.

(uslib-deferred_income_annuity-s4)=

### S4. Pacific Life Insurance Company / Pacific Life & Annuity Company — "PACIFIC SECURE INCOME® — A Fixed, Deferred Income Annuity" (fact sheet)
- Publisher: Pacific Life Insurance Company (all states except New York) and Pacific Life
  & Annuity Company (all states). Document codes `24-299C`, `FAC0560-01`, `2/26 E1127`.
  Official Pacific Life domain.
- Doc type: producer/consumer fact sheet (6 pages). **Current vintage (Feb 2026)** — the
  most up-to-date primary source retrieved.
- URL fetched: https://www.annuities.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/fact-sheets/pacific-secure-income-fact-sheet.pdf
- Retrieved: **YES** (all 6 pages text extracted)
- Role in this library: the **extended case** (commutation of the present value of
  remaining guaranteed payments; the unbundled "Life Only with 100% Return of Purchase
  Payments Death Benefit" option) and the independent corroboration of the 2026 QLAC
  premium limit.

(uslib-deferred_income_annuity-s5)=

### S5. Pacific Life — "Pacific Secure Income — Client Guide"
- Publisher: Pacific Life. Document codes `24-300A`, `FAC0555-2401`, `11/24 E1127`.
- Doc type: client guide (16 pages).
- URL fetched: https://www.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/guide/pacific-secure-income-client-guide.pdf
- Retrieved: **YES** (16 pages text extracted)
- Note carried over: the guide does **not** disclose the interest-rate-adjustment charge
  formula used for withdrawals — the basis for the [std]/[unverified] commutation
  construction in `technical-notes.md`.

(uslib-deferred_income_annuity-s6)=

### S6. Fidelity Investments — "Compare Deferred Income Annuities" (cross-insurer comparison table)
- Publisher: Fidelity Brokerage Services / Fidelity Insurance Agency (distributor
  comparison of third-party insurer products).
- Doc type: web comparison table (secondary/aggregator, but sourced from the insurers'
  filed product parameters and useful as a cross-check).
- URL fetched: https://www.fidelity.com/annuities/deferred-fixed-income-annuities/compare
- Retrieved: **YES**
- Caveat carried over: this is a **distributor aggregation**. Where it conflicts with an
  insurer's own document, the insurer document governs; where it is the only source (USAA
  Life, Western & Southern), rows are flagged as lower-confidence.

(uslib-deferred_income_annuity-s8)=

### S8. MassMutual — official RetireEase Choice guide on compass.massmutual.com (FAILED FETCH)
- URL attempted: https://compass.massmutual.com/api/public/assets/file/bltd738363f5d003651
- Retrieved: **NO** — request timed out (60s). A current-vintage MassMutual DIA guide was
  therefore **not** obtained; [S2] is the 2019 edition. Cited only as the reason for the
  vintage caveat on the archetype.

(uslib-deferred_income_annuity-s9)=

### S9. Fidelity communications-hosted insurer fact sheets (PARTIAL FAILURE)
- URLs attempted: https://communications.fidelity.com/fili/docs/guardian-dia-factsheet.pdf
  and https://communications.fidelity.com/fili/docs/usaa-dia-factsheet.pdf
- Retrieved: **NO** — both returned an HTML interstitial rather than PDF bytes when
  fetched directly. Guardian content was obtained from a mirror [S3]; **no USAA Life
  primary document was retrieved** (USAA parameters come only from [S6]). Cited only as
  the reason the Guardian minimum-deferral conflict could not be resolved.

(uslib-deferred_income_annuity-s11)=

### S11. Guardian brochure on immediateannuities.com (FAILED FETCH)
- URL attempted: https://www.immediateannuities.com/annuity-brochures/guardian-securefuture-income-annuity.pdf
- Retrieved: **NO** — HTTP 403 Forbidden. Cited only as the second failed route to a
  current Guardian primary document.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(uslib-deferred_income_annuity-r1)=

### R1. 26 CFR § 1.401(a)(9)-6(q) — Qualifying longevity annuity contract (current text)
- Publisher: U.S. Government (eCFR, current edition), Treasury/IRS.
- Doc type: codified Treasury Regulation.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.401(a)(9)-6
  (renders 26 CFR 1.401(a)(9)-6; human-readable equivalent
  https://www.ecfr.gov/current/title-26/section-1.401(a)(9)-6)
- Retrieved: **YES** (full section text extracted)
- Credit line carried over: `[T.D. 9130, 69 FR 33293, June 15, 2004; … T.D. 9673, 79 FR
  37639, July 2, 2014; … T.D. 10001, 89 FR 58907, July 19, 2024]` — the paragraph (q)
  QLAC rules were **restructured from the old "A-17" Q&A format into paragraph (q)** by
  the July 2024 final regulations [R6].

(uslib-deferred_income_annuity-r2)=

### R2. SECURE 2.0 Act of 2022, § 202 ("Qualifying Longevity Annuity Contracts") — Division T of Pub. L. 117-328
- Publisher: U.S. Government Publishing Office (govinfo), enrolled text of Public Law
  117-328 (Consolidated Appropriations Act, 2023), Division T = SECURE 2.0 Act of 2022.
  Statutory note codified at 26 U.S.C. 401 note; text at 136 Stat. 5331–5332.
- Doc type: enacted federal statute.
- URL fetched: https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm
- Retrieved: **YES** (full text downloaded; § 202 located and read)
- Caveat carried over: SECURE 2.0's **enactment date (December 29, 2022) is [unverified]**
  — the statutory text says only "the date of the enactment of this Act". The derived
  base-period quarter (July 1, 2022) *is* confirmed directly by the codified regulation
  [R1 (q)(4)(ii)(A)(1)](#uslib-deferred_income_annuity-r1).

(uslib-deferred_income_annuity-r3)=

### R3. IRS Notice 2025-67 — "2026 Amounts Relating to Retirement Plans and IRAs, as Adjusted for Changes in Cost-of-Living"
- Publisher: Internal Revenue Service (irs.gov); published in Internal Revenue Bulletin
  2025-49.
- Doc type: IRS notice (annual COLA).
- URL fetched: https://www.irs.gov/pub/irs-drop/n-25-67.pdf
- Retrieved: **YES**
- Fact carried over verbatim: "The limitation on premiums paid for a qualifying longevity
  annuity contract under § 1.401(a)(9)-6(q)(2)(ii) remains $210,000."

(uslib-deferred_income_annuity-r4)=

### R4. 26 CFR § 1.401(a)(9)-5(b)(4) — Exclusion of QLAC value from the account balance
- Publisher: eCFR (current edition), Treasury/IRS.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.401(a)(9)-5
- Retrieved: **YES**
- Credit line: `[… T.D. 9673, 79 FR 37639, July 2, 2014; T.D. 9930, 85 FR 72477, Nov. 12,
  2020; T.D. 10001, 89 FR 58907, July 19, 2024]`.

(uslib-deferred_income_annuity-r5)=

### R5. 26 CFR § 1.408-8(h) — QLACs in the IRA context
- Publisher: eCFR (current edition), Treasury/IRS.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.408-8
- Retrieved: **YES**
- Credit line: `[… T.D. 9673, 79 FR 37642, July 2, 2014; T.D. 10001, 89 FR 58948,
  July 19, 2024]`. Applicability: for RMDs for calendar years beginning on or after
  January 1, 2025.

(uslib-deferred_income_annuity-r6)=

### R6. T.D. 10001 — "Required Minimum Distributions", final regulations (Federal Register)
- Publisher: Treasury Department / Internal Revenue Service.
- Doc type: final rule.
- URL fetched (metadata via Federal Register API):
  https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions
- Retrieved: **YES** (metadata; **full preamble not read** — carried-over caveat: any
  statement about *why* Treasury drafted a particular QLAC provision would be
  unsupported). Document number **2024-14542**; citation **89 FR 58886**; published
  **July 19, 2024**; **effective September 17, 2024**.

(uslib-deferred_income_annuity-r7)=

### R7. T.D. 9673 — "Longevity Annuity Contracts", final regulations (the original 2014 QLAC rule)
- Publisher: Treasury Department / Internal Revenue Service.
- URL fetched (metadata via Federal Register API):
  https://www.federalregister.gov/documents/2014/07/02/2014-15524/longevity-annuity-contracts
- Retrieved: **YES** (metadata). Document number **2014-15524**; citation **79 FR 37633**;
  published **July 2, 2014**.

(uslib-deferred_income_annuity-r8)=

### R8. Internal Revenue Code § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- Publisher: Cornell Legal Information Institute (LII) rendering of 26 U.S.C. § 72.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: **YES** (key subsections read; full section is long)

(uslib-deferred_income_annuity-r9)=

### R9. NAIC — Valuation Manual, January 1, 2026 edition
- Publisher: National Association of Insurance Commissioners.
- Doc type: statutory valuation manual (457 pages).
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: **YES** (full 457-page text extracted and searched directly)
- Sections used: VM-01 (DIA definition); VM-22 §§2.B, 3.A, 3.F.1.a and the Section 6
  standard-projection tables (mortality, Table 6.8, maintenance expense Table 6.1, lapse,
  annuitization); VM-M §1.J (2012 IAR); VM-V §1 (income annuities, Valuation Rate Buckets,
  premium determination date, prescribed portfolio).
- Caveats carried over: **VM-22 Table 6.8 was captured only through attained age 79**; the
  **seven-basis-point expense provision was truncated at a page break**, so the exact
  present-value base for contracts without an account value is not quoted.

(uslib-deferred_income_annuity-r10)=

### R10. NAIC — Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805), Fall 2020 edition
- Publisher: National Association of Insurance Commissioners.
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: **YES** (all 5 pages)
- Caveat carried over: **Section 4.B (the nonforfeiture interest rate definition) and the
  balance of Section 4.A(1)(c)–(d) were not captured** in this extract; the well-known
  "5-year CMT minus 125 bp" formulation and its floor are therefore **[unverified] in this
  file**. The cross-product entry [REG-R42] read Sections 1–8 in full and settles the
  floor at **15 basis points**, which is the figure used in `product-spec.md`.

(uslib-deferred_income_annuity-r11)=

### R11. NAIC — Annuity Disclosure Model Regulation (Model #245)
- Publisher: National Association of Insurance Commissioners (© 2015 edition of the model
  text within the Fall compendium).
- URL fetched: https://content.naic.org/sites/default/files/model-law-245.pdf
- Retrieved: **YES** (40 pages)
- Caveat carried over: the Section 3.A characterisation (a non-participating DIA has no
  non-guaranteed elements and is therefore exempt) is a direct reading of the retrieved
  text; **whether individual states apply it the same way to DIAs was not verified**.

(uslib-deferred_income_annuity-r12)=

### R12. NAIC — Variable Annuity Model Regulation (Model #250)
- Publisher: National Association of Insurance Commissioners (October 2007 edition).
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: **YES**
- Role: identifies the mis-numbering — **Model #250 is the Variable Annuity Model
  Regulation**, not an annuity disclosure regulation, and does not apply to a
  general-account DIA. The disclosure model is **#245** [R11].

(uslib-deferred_income_annuity-r13)=

### R13. IIPRC — "Individual Deferred Paid-Up Non-Variable Annuity Contract Standards (Commonly Marketed as Deferred Income Annuities or Longevity Annuities)", IIPRC-A02-I-LONG
- Publisher: Interstate Insurance Product Regulation Commission (Insurance Compact).
- Doc type: adopted uniform product standard (26 pages). **The single most contractually
  precise DIA reference retrieved**, and the contractual-language authority throughout
  this library, no DIA specimen contract having been located.
- URL fetched: https://www.insurancecompact.org/sites/default/files/2022-12/171120_ind_def_pu_non_var_ann_long_stds.pdf
  (record page: https://www.insurancecompact.org/standards/record-adopted-standards/individual-deferred-paid-non-variable-annuity-contract-standards)
- Retrieved: **YES** (all 26 pages)
- Dates: **Adopted August 5, 2017; Effective November 20, 2017**; amends standards
  originally adopted October 17, 2010; amendments apply only to new filings received after
  the effective date.

(uslib-deferred_income_annuity-r14)=

### R14. American Academy of Actuaries / SOA Payout Annuity Table Team — "Payout Annuity Report" (September 28, 2011)
- Publisher: American Academy of Actuaries (report prepared by the Joint Academy/SOA
  Payout Annuity Table Team at the request of the NAIC Life Actuarial (A) Task Force).
- URL fetched: https://www.actuary.org/wp-content/uploads/2017/11/Payout_Annuity_Report_09-28-11.pdf
- Retrieved: **YES** (36 pages)

(uslib-deferred_income_annuity-r15)=

### R15. SOA Research Institute & LIMRA — "2020-24 Payout Annuity Experience Study" (Study Highlights), © 2026
- Publisher: Society of Actuaries Research Institute (with LIMRA).
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2020-24-payout-annuity-exp-study.pdf
- Retrieved: **YES** (5-page Study Highlights document; the full results are behind the SOA
  "Experience Studies Pro" subscription)
- Fact of first importance here, carried over verbatim: "The study includes immediate
  annuities, **deferred income annuities**, settlement options, and annuitizations of life
  insurance and annuity death claims."
- Caveat carried over: **no A/E ratios or DIA-specific mortality results are quoted** —
  only the highlights were retrieved.

(uslib-deferred_income_annuity-r16)=

### R16. SOA — "2012 Individual Annuity Reserving Report & Table" (resource page)
- Publisher: Society of Actuaries.
- URL fetched: https://www.soa.org/resources/experience-studies/2011/2012-ind-annuity-reserving-rpt/
- Retrieved: **YES** (page content; no date stated on the page for the report itself)
- Role here: it identifies **http://mort.soa.org/** as the machine-readable source for the
  2012 IAM Period, 2012 IAM Basic and Scale G2 tables. Caveat carried over: **those
  numerical tables were not downloaded**, which is why the worked example in
  `technical-notes.md` uses illustrative **[std]** survival and annuity factors rather
  than table lookups.

---

## Cross-product regulatory references [REG-R#]

These are cited with the **[REG-R#]** prefix to avoid collision with the product research
file's own R-numbering. They resolve against the curated page
`references/regulatory-and-actuarial-references.md`, whose **shared numbering space runs
R1–R157 and is one space, not several**, with **most of the R73–R149 block unused** (the
gaps are not losses and must not be back-filled):

- **R1–R34** are of life origin; research provenance `_research/regulatory-actuarial.md`.
  Several of them also bind annuity models and are listed as such in the annuity
  bibliography's "Existing entries (R1–R34) that also bind annuity models" table.
- **R35–R72** are annuity-specific; research provenance
  `_research/regulatory-actuarial-annuities.md`, which opens the continuation of the
  same numbering space at R35.
- **R150–R157** are the AP&P Manual appendix and actuarial-guideline prints read on
  2026-08-06; per-entry bibliography at
  `references/regulatory-and-actuarial-references.md`, research provenance
  `_research/appp-ag33.md` (R151), `_research/appp-a820-a821-a822.md` (R153) and
  `_research/appp-a830.md` (R154). Cited here by `technical-notes.md` and by the
  "Regulatory context" paragraphs of `product-spec.md`; the three entries are reproduced
  below.

Entries cited by the two documents in this directory (retrieval status as recorded in the
originating research file, access date 2026-08-04):

| Tag | Short title | Half | Retrieval status |
|---|---|---|---|
| REG-R16 | 26 U.S.C. § 807 — tax reserves | R1–R34 (life file) | fetched |
| REG-R26 | ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products | R1–R34 | fetched |
| REG-R27 | ASOP No. 7 — Life or Health Cash Flow Analysis | R1–R34 | fetched |
| REG-R29 | ASOP No. 22 — Opinions Based on Asset Adequacy Analysis | R1–R34 | fetched |
| REG-R31 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual (cited to show it does **not** cover VM-22) | R1–R34 | fetched |
| REG-R32 | ASOP No. 56 — Modeling | R1–R34 | fetched |
| REG-R34 | FASB ASU 2018-12 (LDTI) | R1–R34 | fetched |
| REG-R35 | VM-21 — PBR for Variable Annuities (cited to show it does **not** apply) | R35–R72 (annuity file) | fetched (local text extraction) |
| REG-R36 | VM-22 — PBR for Non-Variable Annuities | R35–R72 | fetched (local text extraction) |
| REG-R37 | VM-V Section 1 — Income Annuities (statutory maximum valuation interest rates) | R35–R72 | fetched (local text extraction) |
| REG-R41 | VM-C — Appendix C index of incorporated actuarial guidelines | R35–R72 | fetched (local text extraction) |
| REG-R42 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) — full Sections 1–8, source of the **15 bp** floor correction | R35–R72 | fetched (local text extraction) |
| REG-R43 | Variable Annuity Model Regulation (Model #250) — the numbering correction | R35–R72 | fetched (local text extraction) |
| REG-R44 | Actuarial Guideline LIV (AG 54) — cited only to name the "interim value" concept a DIA does not have | R35–R72 | fetched (local text extraction, complete) |
| REG-R45 | Annuity Disclosure Model Regulation (Model #245) | R35–R72 | fetched (local text extraction) |
| REG-R46 | Suitability in Annuity Transactions Model Regulation (Model #275) | R35–R72 | fetched (local text extraction) |
| REG-R49 | SEC Release 33-11294 — registration for index-linked and registered MVA annuities (contrast case) | R35–R72 | fetched via govinfo; sec.gov PDF returned 403 |
| REG-R52 | SEC Form N-4 (contrast case) | R35–R72 | **not fetched** (sec.gov 403) |
| REG-R53 | CRS Report R40656 — SEC Rule 151A and Annuities (why fixed annuities are not registered securities) | R35–R72 | fetched |
| REG-R55 | 26 U.S.C. § 72 — Annuities (same statute as [R8] above) | R35–R72 | fetched |
| REG-R56 | 26 U.S.C. § 1035 — exchanges | R35–R72 | fetched |
| REG-R57 | 26 C.F.R. § 1.401(a)(9)-6 — QLAC rules (same regulation as [R1] above, LII rendering) | R35–R72 | fetched |
| REG-R58 | T.D. 10001 — RMD final regulations implementing SECURE 2.0 § 202 (same T.D. as [R6] above, govinfo full text) | R35–R72 | fetched via govinfo |
| REG-R59 | Model #821 + VM-M §§1.I–1.M, 2.C — annuity valuation mortality (2012 IAR, 2012 IAM Period/Basic, Scale G2) | R35–R72 | fetched (local text extraction, both) |
| REG-R60 | 2012 IAR development report (Payout Annuity Table Team; same report as [R14] above) | R35–R72 | fetched (local text extraction) |
| REG-R61 | 2020–2024 Individual Payout Annuity Mortality Experience Study (landing page; highlights PDF fetched as [R15] above) | R35–R72 | fetched (landing page) |
| REG-R65 | SOA Individual Annuity Experience Studies index — the only route to the **deferred-period** mortality sources (2011–2015 deferred annuity mortality; 2006 deferred-period analysis) | R35–R72 | fetched |
| REG-R70 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | R35–R72 | fetched |
| REG-R71 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Doc. No. 207) | R35–R72 | fetched (local text extraction) |

Cross-product note carried over from the annuity bibliography — **the numbers below are
cross-product numbers, i.e. [REG-R#] in this directory, not the product-local [R#] above**:
for the deferred-income-annuity product the binding new entries are **R36, R37, R41, R59,
R60, R61, R55, R56, R57, R58, R70, R71**, plus the existing entries **R1, R3, R16, R27,
R29, R32, R33, R34** [`_research/regulatory-actuarial-annuities.md`, cross-reference
table]. (Cross-product R1, R3, R33 are cited by neither document in this directory, so
they carry no [REG-R#] row in the table above.)

### Superseded entries kept as frozen records

The two entries below are preserved exactly as written and carry **appended** supersession
notes rather than edits; ids, titles, publishers, URLs, access dates and fetched markers are
carried from `references/regulatory-and-actuarial-references.md`. **Nothing is
renumbered and nothing is re-worded.** Read every heading as a cross-product id, i.e. `[REG-R#]`
in this directory, never the product-local `[R#]` of the section above.

### REG-R39. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located.** Title and current status
  verified from the Valuation Manual's VM-C index (page C-1) [R41]; the authoritative text is
  in the **AP&P Manual Appendix C**.
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no.** Neither document in this directory quotes AG 33 mechanics, and both say
  so at the point of use.
- **Superseded in fact by R151** (below), the guideline as printed in the AP&P Manual and read
  in full on 2026-08-06. The three lines above are preserved verbatim as the record of what was
  true when they were written; the statement that neither document quotes AG 33 mechanics
  **no longer holds** — `product-spec.md`'s *Formulaic CARVM — Appendix A-820 and Actuarial
  Guideline XXXIII* paragraph now does. R39 is frozen and is not edited.

### REG-R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages A-1 to A-2; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; the complete two-page index read)
- **Limit carried forward:** VM-A is an **index, not a text**. The requirements it indexes —
  above all **A-820** (minimum life and annuity reserve standards) and **A-830** (valuation of
  life insurance policies) — live in AP&P Appendix A and **were not retrieved**, because the
  reserves stream worked under R33's "paid publication" assumption. Formulaic CRVM detail in
  this directory therefore rests on the Standard Valuation Law itself (R1) and Model #830 (R6).
- **Superseded in fact for the two items this directory relies on**, the sentence above being
  preserved verbatim as the record of what was true when it was written. **A-820 is now R153 and
  A-830 is now R154**, both read in full from the same free *As of March 2026* download on
  2026-08-06. **A-270, A-791, A-812, A-815, VM-A-814 and A-817 are still unretrieved**, and
  A-270 — although extracted alongside A-585 — has **no reference id assigned** and is therefore
  not citable. R110 is frozen and is not edited.

### Entries added 2026-08-06 from the AP&P Manual appendix and guideline prints

Ids, titles, publishers, URLs, access dates, fetched markers and carried-forward limits below are
reproduced from `references/regulatory-and-actuarial-references.md`, including the
internal cross-references they make to ids not listed in this directory (R1, R5, R6, R33, R39,
R41, R73, R101, R102, R110), which resolve against that shared reference page. **Nothing is
renumbered and nothing is re-worded.** Read every heading as a cross-product id, i.e. `[REG-R#]`
here, never the product-local `[R#]`.

**One physical document behind R151–R157.** All seven are appendix items of the NAIC
*Accounting Practices and Procedures Manual, As of March 2026* — the **same 2,117-page
consolidated PDF already catalogued as R73**, a **free download** from `content.naic.org`
(catalogue entry "APPM-2026 … Free Download" on https://content.naic.org/publications;
file https://content.naic.org/sites/default/files/publication-app-manual.pdf). They take
appendix-level ids rather than being folded into R73 so a document can cite **A-820 ¶15** or
**AG 33 *Text* 4** instead of a 2,117-page manual. Each was read by **local text extraction**
from that download. Only **R151, R153 and R154** are cited in this directory; R152 (AG 35),
R155 (A-585), R156 (A-250) and R157 (A-255) reach no DIA and carry no row here.

**Edition line.** None of these items prints "As of March 2026" on its own pages. Every extracted
page carries only the footer **"© 1999-2026 National Association of Insurance Commissioners"**,
which is a **copyright span, not an adoption, effective or revision date** for any of these
instruments and must never be cited as one. The "As of March 2026" designation is the manual's own
front matter, recorded at R73.

**Licence caution, inherited from R73.** Personal and non-commercial use; redistribution or
integration "into any software or other publication" requires written NAIC permission. Both
documents in this directory **paraphrase the mechanics and cite the paragraph, section or block**,
and quote only short anchors.

**A-270 (Variable Life Insurance)** was extracted alongside A-585 at printed pages A270-1 to
A270-3 = **PDF pages 1097–1099**, but the extraction **assigned it no reference id**. It is
referred to descriptively where it comes up at all and is **never cited as a [REG-R#]**.

### REG-R151. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33), as printed in the AP&P Manual
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
  preserved unaltered above.

### REG-R153. Appendix A-820 — Minimum Life and Annuity Reserve Standards (with Appendix A-821, Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities, and Appendix A-822, Asset Adequacy Analysis Requirements)
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
  alone. R110 is frozen and is preserved unaltered above.

### REG-R154. Appendix A-830 — Valuation of Life Insurance Policies (Including the Introduction and Use of New Select Mortality Factors)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  **Volume I, Appendix A — Excerpts of NAIC Model Laws**; printed pages **A830-1 to A830-27** =
  **PDF pages 1206–1232** — operative text A830-1 to A830-14 (PDF 1206–1219), the Attachment
  heading and explanatory note at A830-15 (PDF 1220), and the six select-mortality-factor tables
  at A830-16 to A830-27 (PDF 1221–1232); same physical document as R73
- **Accessed:** 2026-08-06
- **Fetched:** yes (local text extraction; **¶¶1–32 and the Attachment read in full**; the six
  factor tables transcribed programmatically, each parsing to 71 issue-age rows × 20 duration
  columns)
- **Limits carried forward from `_research/appp-a830.md`:** the appendix is a **flat sequence
  of paragraphs ¶¶1–32 plus an unnumbered Attachment and has no Sections at all**, so a
  "Model 830 Section 7" citation **does not resolve** against this print — the ULSG material is at
  **¶¶29–32** — and the words **"Model #830" and "Regulation XXX" appear nowhere** in it. It prints
  **no calendar effective date for itself**: "the effective date of this appendix" is an unresolved
  placeholder used **eleven times**, and the only calendar dates printed anywhere are the
  **1 January 2004** cutover to the 2001 CSO. There is **no worked numerical example** in it, **no
  AG 38 content**, **no prescribed X value**, and **no annuity content**. Its ¶17 X-factor
  cross-reference is **garbled in the print** and is flagged rather than resolved, as is ¶32.b's
  unnamed "other appendices governing universal life plans". **The transcribed factor tables were
  not checked against an independent copy** and are not reproduced in this directory.
- **Supersedes in fact:** the A-830 half of **R110**'s limit, and the second-hand reliance on
  Model #830 (R6) for the segmented/unitary construction. R6 and R110 are frozen and unaltered.
- **Why a life-side appendix is cited in a DIA directory:** for its **verified negative**. A-830
  carries **no annuity content**, which is what makes the Exhibit 5 deficiency-reserve line with
  its Actuarial Guideline I / A-830 apparatus a life-side item rather than a DIA item. That is the
  only use made of it here.

---

## Provenance note

Extraction details live in `_research/deferred-income-annuity.md`: that file records
which facts came from which source, the [unverified] flags, the failed fetches (S7–S11),
the source-vintage caveats (MassMutual 2019 [S2] [S8], Guardian January 2018 [S3] [S9] [S11],
with NYL June 2026 [S1] and Pacific Life February 2026 [S4] the current-vintage primary
sources — the research file's own S4 header calls it "the most up-to-date primary source
retrieved", which its S1 header (June 2026 revision code) does not support), the distributor-mirror
hosting caveat for [S1] and [S3], and the four **regulatory corrections** this library
follows rather than repeating the common misconceptions:

1. **Model #250 is the Variable Annuity Model Regulation, not the Annuity Disclosure Model
   Regulation** — the disclosure model is **#245** [R11] [R12] [REG-R43] [REG-R45].
2. **The QLAC rules live in Treas. Reg. § 1.401(a)(9)-6(q), not in "A-17"** — T.D. 10001
   restructured them out of the Q&A format on July 19, 2024 [R1] [R6] [REG-R58].
3. **The 25%-of-account-balance QLAC premium limit no longer exists** — SECURE 2.0 § 202
   directed its elimination and the codified text has only a dollar limitation
   [R1] [R2] [REG-R58].
4. **The Model #805 indexed nonforfeiture rate floor is 15 basis points, not 1%** — the DIA
   research file's own extract did not capture Section 4.B and therefore left the "floored
   at 1%" formulation [unverified] [R10]; the fully fetched text in the cross-product
   bibliography settles it at 0.15% [REG-R42].
5. **AG 33's printed title is "Determining CARVM Reserves for Annuity Contracts With Elective
   Benefits", and its printed effective date is December 31, 1998** — not the title or the
   December 31, 1995 date the library carries elsewhere from IRS Rev. Rul. 2002-6. The AP&P
   print's *Effective Date* block reaches "all contracts issued on or after January 1, 1981",
   which both records agree on; **the date conflict itself is unresolved** — the extracted pages
   carry no amendment history — and this directory records both rather than swapping one for the
   other [REG-R151]. Two related mis-statements the library declines to repeat: **nursing home
   benefits are non-elective** under AG 33's *Definitions* 1, and **"efficient policyholder
   selection" is not AG 33's language** and appears nowhere in the guideline [REG-R151].

The cross-product bibliographies `_research/regulatory-actuarial.md` (R1–R34) and
`_research/regulatory-actuarial-annuities.md` (R35–R72) play the same role for
[REG-R#] tags; for **REG-R151, REG-R153 and REG-R154** the research provenance is
`_research/appp-ag33.md`, `_research/appp-a820-a821-a822.md` and
`_research/appp-a830.md` respectively, and where one of those files and a document in
this directory disagree, **the research file governs**. Income-phase mechanics are specified in
`products/immediate_annuity/`, whose research provenance is
`_research/immediate-annuity.md`. Standardizations marked **[std]** in
`product-spec.md` and `technical-notes.md` are introduced at drafting and are not
attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-deferred_income_annuity-r1
[R10]: #uslib-deferred_income_annuity-r10
[R11]: #uslib-deferred_income_annuity-r11
[R12]: #uslib-deferred_income_annuity-r12
[R14]: #uslib-deferred_income_annuity-r14
[R15]: #uslib-deferred_income_annuity-r15
[R2]: #uslib-deferred_income_annuity-r2
[R3]: #uslib-deferred_income_annuity-r3
[R41]: #uslib-reg-r41
[R6]: #uslib-deferred_income_annuity-r6
[R8]: #uslib-deferred_income_annuity-r8
[REG-R151]: #uslib-reg-r151
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R45]: #uslib-reg-r45
[REG-R58]: #uslib-reg-r58
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
