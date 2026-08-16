# Sources

Source ids, titles, publishers, URLs, access dates, and fetched/not-fetched markers are
carried over **verbatim** from `_research/registered-index-linked-annuity.md` (the
citation ground truth for [S#]/[R#] tags). Ids are never renumbered. Sources from the
research file that are not cited in `product-spec.md` or `technical-notes.md` are omitted
— **none were dropped**: all of S1–S6 and R1–R6 are cited. **No new source was fetched at
drafting**; the only entries added afterwards are the **AP&P Manual appendix items
R151–R157**, read on 2026-08-06 and listed in their own block at the end of the [REG-R#]
section.

Access date for all citations: **2026-08-04** (cross-product entries R1–R34 carry their
own access date of 2026-08-03, and the AP&P appendix entries **R151–R157** carry
**2026-08-06** — see the [REG-R#] section).

---

## Primary product sources [S#]

(uslib-registered_index_linked_annuity-s1)=

### S1. Brighthouse Life Insurance Company of NY — "Brighthouse Shield Level Select 6-Year Annuity", Form S-3 registration statement
- Publisher: Brighthouse Life Insurance Company of NY ("BLNY"), CIK 0001167609
- Doc type: Securities Act registration statement / statutory prospectus (Form S-3, the
  pre-2024 RILA registration form). Filed 2019-02-06, accession 0001193125-19-030795.
- URL fetched: https://www.sec.gov/Archives/edgar/data/1167609/000119312519030795/d695141ds3.htm
- Retrieved: YES (full document downloaded and read; note sec.gov rejects generic fetchers
  with HTTP 403 — a declared User-Agent is required)
- Product: Brighthouse Shield Level Select 6-Year Annuity — "an individual single premium
  deferred index-linked separate account annuity contract". New York version only.
  Separate Account: Brighthouse Separate Account SA II.
- Role in this library: documents the **older, pro-rata "accrued rate" interim value
  design**, retained as the legacy contrast module and first implementation target; also
  the source for issue rules, free-withdrawal and withdrawal-charge mechanics, the
  return-of-premium death benefit, the Transfer Period, and the Cap/Step crediting
  worked examples.

(uslib-registered_index_linked_annuity-s2)=

### S2. Brighthouse Life Insurance Company — "Brighthouse Shield Level II 6-Year Annuity", Rule 424(b)(3) prospectus
- Publisher: Brighthouse Life Insurance Company ("BLIC"), CIK 0000733076
- Doc type: statutory prospectus filed under Rule 424(b)(3), filed 2024-07-26, accession
  0001193125-24-180915
- URL fetched: https://www.sec.gov/Archives/edgar/data/733076/000119312524180915/d747348d424b3.htm
- Retrieved: YES (full document downloaded and read)
- Product: Brighthouse Shield Level II 6-Year Annuity — individual single premium deferred
  index-linked separate account annuity contract.
- Role in this library: **the mechanics anchor**. Appendix F "Interim Value of Shield
  Options" carries the complete Fixed Income Asset Proxy / Derivative Asset Proxy algebra,
  the per-crediting-type replicating option portfolios, and the worked proportional
  Investment Amount reduction on withdrawal.

(uslib-registered_index_linked_annuity-s3)=

### S3. Pruco Life Insurance Company — "PRUDENTIAL FlexGuard — Flexible Premium Deferred Index-Linked and Variable Annuity ('B Series')", prospectus supplement
- Publisher: Pruco Life Insurance Company (Prudential)
- Doc type: prospectus supplement dated September 14, 2022 to the prospectus dated
  August 15, 2022, containing full amended-and-restated text of the index-strategy
  sections, the Interim Value discussion, and Appendix B (57 pages)
- URL fetched: https://www.prudential.com/content/dam/us/sites/pru-com/pru/opt2/annuities/annuity-prospectuses/S3-flex-guard-prosp-B-plaz.pdf
- Retrieved: YES (full PDF text extracted and read)
- Product: Prudential FlexGuard indexed variable annuity, B Series — a *combination*
  contract offering index strategies alongside variable investment subaccounts.
- Caveat carried over: this is a 2022 supplement, not the current prospectus. Numbers are
  as of that document; **do not treat as current pricing.** FlexGuard has since been
  re-registered on Form N-4 under the 2024 rule [R1], so strategy menus, buffers and rates
  will have changed.

(uslib-registered_index_linked_annuity-s4)=

### S4. Equitable Financial Life Insurance Company — "Structured Capital Strategies PLUS 26", Form N-4 registration statement
- Publisher: Equitable Financial Life Insurance Company, CIK 0002039145 (a parallel,
  essentially identical filing exists for Equitable Financial Life Insurance Company of
  America, CIK 0002038891)
- Doc type: Form N-4 registration statement (the post-2024 RILA form), filed 2026-06-18,
  accession 0001193125-26-275133
- URL fetched: https://www.sec.gov/Archives/edgar/data/2039145/000119312526275133/d59590dn4.htm
- Retrieved: YES (full document downloaded and read)
- Product: Structured Capital Strategies PLUS (SCS PLUS 26) — index-linked annuity with a
  Structured Investment Option (SIO) of "Segments" plus a Guaranteed Interest Option
  (GIO). Non-unitized Separate Account No. 68 (NY) / 68A and 68E (AZ).
- Role in this library: the richest **segment-type menu** publicly documented (Standard,
  Annual Lock, Step Up, Dual Direction, Dual Step Up, Optimal Mix) with the exact Segment
  Rate of Return decision table for each, and the most detailed **Segment Interim Value**
  description including the Cap Calculation Factor and the implied-volatility
  interpolation procedure.

(uslib-registered_index_linked_annuity-s5)=

### S5. Allianz Life Insurance Company of North America / Allianz Life Variable Account B — "Allianz Index Advantage+ Select Income Annuity", Form N-4 initial registration statement
- Publisher: Allianz Life Insurance Company of North America (CIK 0000072499) / Allianz
  Life Variable Account B (CIK 0000836346)
- Doc type: Form N-4 initial registration statement, filed 2025-07-22, accession
  0000836346-25-000047
- URL fetched: https://www.sec.gov/Archives/edgar/data/836346/000083634625000047/iaplusselectincomn4july2025.htm
- Retrieved: YES (full document downloaded and read)
- Product: Allianz Index Advantage+ Select Income Annuity.
- Role in this library: the structurally different presentation — a **"Daily Adjustment"**
  applied to an "Index Option Base" rather than a self-contained interim value — and the
  only retrieved source offering both **buffer** and **floor** crediting side by side
  (Index Guard Strategy = −10% Floor). Appendix C gives the Proxy Value formula for each
  of six crediting methods.
- Caveat carried over: this is an *initial* N-4 filing; several fee-table cells are marked
  "[To be updated by amendment]" and the prospectus date is "[December XX, 2025]". **Fee
  figures from this document are preliminary** and should be re-verified against the
  effective prospectus.

(uslib-registered_index_linked_annuity-s6)=

### S6. Lincoln Life & Annuity Company of New York — "Lincoln Level Advantage 2 B-Share Index-Linked Annuity", Form N-4/A
- Publisher: Lincoln Life & Annuity Company of New York, CIK 0001022095
- Doc type: Form N-4/A (pre-effective amendment), filed 2026-04-16, accession
  0001104659-26-044336. Includes the SAI text with the Interim Value appendix and worked
  examples.
- URL fetched: https://www.sec.gov/Archives/edgar/data/1022095/000110465926044336/tm265270d1_n4a.htm
- Retrieved: YES (full document downloaded and read)
- Product: Lincoln Level Advantage 2 B-Share (and Advisory) Index-Linked Annuity Contracts.
- Role in this library: a **third algebraic form of the fixed income asset proxy** and a
  full grid of **worked Interim Value numeric examples** across index moves of
  −30%/−10%/+20%/+40% for 1-year and 6-year terms and for cap, trigger and dual-trigger
  accounts — the best available regression test vectors.

### Failed / blocked retrievals (carried over; **not** sources, and nothing is cited from them)
- Brighthouse "Understanding Interim Value" educational PDF —
  https://www.brighthousefinancial.com/content/dam/brighthouse-financial/public/pdfs/shield/Shield-Interim-Value-Educational-Resource.pdf
  — HTTP 403. fetched_ok = false.
- Brighthouse Shield current rate page —
  https://www.brighthousefinancial.com/products/annuities/shield-annuities/shield-rates/
  — HTTP 403. fetched_ok = false. **No current declared cap/step/edge rates captured** —
  this is why every declared-rate value in `product-spec.md` is **[std]**.
- Equitable performance cap rate page —
  https://equitable.com/annuities/variable-annuities/performance-cap-rates
  — request rejected by WAF. fetched_ok = false.
- Federal Register HTML of the RILA adopting release — redirects off-host to
  unblock.federalregister.gov. fetched_ok = false; the SEC PDF (R1) was used instead and
  is authoritative.

---

## Regulatory and actuarial references [R#] (product research file numbering)

These are the local R-numbers used inside
`_research/registered-index-linked-annuity.md`. They are **independent of** the shared
[REG-R#] space; several documents appear in both (noted per entry).

(uslib-registered_index_linked_annuity-r1)=

### R1. U.S. Securities and Exchange Commission — Final rule, "Registration for Index-Linked Annuities and Registered Market Value Adjustment Annuities; Amendments to Form N-4 …; Other Technical Amendments"
- Publisher: SEC
- Release Nos. 33-11294; 34-100450; IC-35273; File No. S7-16-23; RIN 3235-AN30. 17 CFR
  Parts 230, 232, 239, 274. 467 pages (conformed to Federal Register version).
- URL fetched: https://www.sec.gov/files/rules/final/2024/33-11294.pdf
- Retrieved: YES (full PDF; introduction and effective/compliance-date sections read in
  detail)
- Cross-reference: the same rulemaking is catalogued at **[REG-R49]**, which was fetched
  via govinfo.gov (89 Fed. Reg. 59978) because sec.gov returned HTTP 403 there, and which
  flags the **May 1, 2026 compliance date as [unverified]** (section II.J not read).
  Both documents in this directory carry that [unverified] flag.

(uslib-registered_index_linked_annuity-r2)=

### R2. NAIC — Actuarial Guideline LIV, "Nonforfeiture Requirements for Index-Linked Variable Annuity Products" (AG 54)
- Publisher: National Association of Insurance Commissioners
- Doc type: adopted actuarial guideline plus project history (6 pages)
- URL fetched: https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-liv-230224.pdf
- Retrieved: YES (full text read)
- Adoption trail printed on the document: adopted by Life Actuarial (A) Task Force
  12/11/2022; adopted by Life Insurance and Annuities (A) Committee 2/24/2023. NAIC
  Executive (EX) Committee and Plenary adoption is **[unverified]** — not stamped on the
  retrieved document. The July 1, 2024 effective date **is** stated in the retrieved text.
- Cross-reference: the same guideline is **[REG-R44]**.

(uslib-registered_index_linked_annuity-r3)=

### R3. NAIC — Valuation Manual, Jan. 1, 2026 edition, VM-21 "Requirements for Principle-Based Reserves for Variable Annuities"
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457 pages; VM-21 Sections 1 and 2 read in detail)
- Cross-reference: **[REG-R35]** (VM-21 as a section) and **[REG-R3]** (the parent
  Valuation Manual).

(uslib-registered_index_linked_annuity-r4)=

### R4. NAIC — Model #250, "Variable Annuity Model Regulation"
- Publisher: NAIC (October 2007 edition of the NAIC Model Laws compilation)
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: YES (13 pages; Sections 2, 3 and 7 read)
- Cross-reference: **[REG-R43]**. Note the model-number correction recorded there and in
  `product-spec.md`: **#250 is the Variable Annuity Model Regulation; the Annuity
  Disclosure Model Regulation is #245** ([REG-R45]).

(uslib-registered_index_linked_annuity-r5)=

### R5. Actuarial Standards Board — ASOP No. 2, "Nonguaranteed Elements for Life Insurance and Annuity Products" (Doc. No. 204)
- Publisher: Actuarial Standards Board
- URL fetched: http://www.actuarialstandardsboard.org/wp-content/uploads/2021/12/asop002_204-2.pdf
- Retrieved: YES (33 pages; Sections 1 and 2 read)
- Note carried over: the title has changed from the older "Nonguaranteed Charges or
  Benefits for Life Insurance Policies and Annuity Contracts".
- Cross-reference: **[REG-R26]**.

(uslib-registered_index_linked_annuity-r6)=

### R6. American Academy of Actuaries — "Index-Linked Variable Annuity (ILVA) / Registered Index-Linked Annuity (RILA)" policy paper
- Publisher: American Academy of Actuaries, Life Practice Council
- Doc type: policy paper, 26 pages, dated December 2025 (file name Life-PolicyPaper120225.pdf)
- URL fetched: https://actuary.org/wp-content/uploads/2025/12/Life-PolicyPaper120225.pdf
- Retrieved: YES (full PDF text extracted and read)
- Role in this library: the **fully worked numeric hypothetical-portfolio interim value
  example** (6-year, 10% buffer, Black-Scholes inputs disclosed), the survey of common
  ILVA product features used to calibrate the composite, and the open-source Excel Lambda
  library reproducing the AG 54 calculation.
- Cross-reference: **[REG-R69]**.
- Caveat carried over: the Interstate Compact standard IIPRC-03-I-ILVA is quoted **only
  second-hand** through this paper; the Compact standard itself was not retrieved
  [unverified].

---

## Cross-product regulatory references [REG-R#]

[REG-R#] tags resolve against the **single shared numbering space, which now runs R1–R157**,
curated at `references/regulatory-and-actuarial-references.md`, with most of the
**R73–R149** block unused. The gaps are not losses and must not be back-filled. Ids are
never renumbered. It is one space in three blocks:

- **R1–R34** — life-origin entries, several of which also bind annuity models. Research
  provenance: `_research/regulatory-actuarial.md`. Access date **2026-08-03**.
- **R35–R72** — annuity-specific entries. Research provenance:
  `_research/regulatory-actuarial-annuities.md`, which also carries the table of which
  R1–R34 entries bind annuity models. Access date **2026-08-04**.
- **R151–R157** — the seven AP&P Manual appendix items read at first hand on **2026-08-06**,
  after this directory was drafted. Research provenance: `_research/appp-ag33.md`,
  `_research/appp-ag35.md`, `_research/appp-a820-a821-a822.md`,
  `_research/appp-a830.md` and `_research/appp-a585-a250-a255-a270.md`; the per-entry
  bibliography is `references/regulatory-and-actuarial-references.md`. Five of the seven
  are cited here and are listed in their own block below. Access date **2026-08-06**.

Entries cited by the two documents in this directory:

| Tag | Half | Short title | Retrieval status (per the research files) |
|---|---|---|---|
| REG-R15 | R1–R34 | 26 U.S.C. §817 (esp. §817(h) diversification) | fetched |
| REG-R16 | R1–R34 | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R26 | R1–R34 | ASOP No. 2 — Nonguaranteed Elements (same standard as [R5] above) | fetched |
| REG-R27 | R1–R34 | ASOP No. 7 — Life or Health Cash Flow Analysis (rev. Dec 2025) | fetched |
| REG-R29 | R1–R34 | ASOP No. 22 — Opinions based on asset adequacy analysis | fetched |
| REG-R31 | R1–R34 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual | fetched (cited only to record that it does **not** cover VM-21/VM-22) |
| REG-R32 | R1–R34 | ASOP No. 56 — Modeling | fetched |
| REG-R34 | R1–R34 | FASB ASU 2018-12 (LDTI; market risk benefits) | fasb.org blocked (HTTP 403); annotated from an accessible third-party full text |
| REG-R35 | R35–R72 | VM-21, Valuation Manual Jan. 1, 2026 ed. (same document as [R3] above) | yes (local text extraction; §§1–3 and TOC read) |
| REG-R38 | R35–R72 | Actuarial Guideline XLIII (AG 43), VAIWG redline | yes (local text extraction) |
| REG-R42 | R35–R72 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) | yes (local text extraction; §§1–8 read in full) |
| REG-R43 | R35–R72 | Variable Annuity Model Regulation (Model #250) (same document as [R4] above) | yes (local text extraction; TOC and §7 read) |
| REG-R44 | R35–R72 | Actuarial Guideline LIV (AG 54) (same document as [R2] above) | yes (local text extraction; **complete guideline read**) |
| REG-R45 | R35–R72 | Annuity Disclosure Model Regulation (Model #245) | yes (local text extraction; §§1 and 3 read) |
| REG-R46 | R35–R72 | Suitability in Annuity Transactions Model Regulation (Model #275) | yes (local text extraction; TOC and §1 read) |
| REG-R47 | R35–R72 | C-3 RBC Instructions and Appendices (C-3 Phase II) | yes (local text extraction) |
| REG-R48 | R35–R72 | Oliver Wyman QIS II public report and executive summary (VA framework reform) | yes, both (local text extraction) |
| REG-R49 | R35–R72 | SEC Release 33-11294 — RILA registration / Form N-4 (same rulemaking as [R1] above) | yes, via govinfo.gov (89 Fed. Reg. 59978); **sec.gov PDF returned HTTP 403 there**; compliance date May 1, 2026 flagged [unverified] |
| REG-R49b | R35–R72 | GAO rule report B-336553 (corroborates R49 publication metadata) | yes |
| REG-R51 | R35–R72 | 17 C.F.R. §230.498A — summary prospectuses, extended to registered non-variable annuities | yes |
| REG-R52 | R35–R72 | SEC Form N-4 | **no — sec.gov returned HTTP 403**; content described only through the adopting releases |
| REG-R53 | R35–R72 | CRS Report R40656 — SEC Rule 151A and annuities (why FIAs are not registered) | yes |
| REG-R54 | R35–R72 | FINRA Rule 2330 — deferred variable annuities | yes; **[unverified]** whether FINRA applies it to RILAs specifically |
| REG-R55 | R35–R72 | 26 U.S.C. §72 — Annuities | yes |
| REG-R56 | R35–R72 | 26 U.S.C. §1035 — exchanges | yes |
| REG-R58 | R35–R72 | T.D. 10001 — RMD final regulations (2024) | yes, via govinfo.gov |
| REG-R59 | R35–R72 | Model #821 + VM-M annuity mortality definitions (2012 IAM / IAR, Scale G2) | yes, both (local text extraction) |
| REG-R60 | R35–R72 | 2012 Individual Annuity Reserving Table — Academy/SOA Payout Annuity Table Team report (source of the 10% margin loaded into the Period / IAR table) | yes (local text extraction; margin/loading sections read) |
| REG-R61 | R35–R72 | 2020–2024 Individual Payout Annuity Mortality Experience Study | yes (landing page; full report PDF and paid data package not retrieved) |
| REG-R62 | R35–R72 | FIA policyholder behavior experience studies (2021–22, 2019–20) | yes (both landing pages); the ~10%/~33% shock-lapse split is **[unverified]** |
| REG-R63 | R35–R72 | Fixed rate deferred surrender experience studies (2023–24, 2015–22) | partial (verified via the SOA index R65); the ~52%/~56% figures are **[unverified]** |
| REG-R64 | R35–R72 | VA / RILA contract holder behavior and GLB utilization studies (2022–24) | yes (2022–24 landing page); detailed tables behind a paid data package |
| REG-R65 | R35–R72 | SOA Individual Annuity Experience Studies — index | yes (complete list read) |
| REG-R66 | R35–R72 | AAA VM-21 practice note supplement (Feb 2022) | yes (local text extraction) |
| REG-R69 | R35–R72 | AAA ILVA / RILA policy paper (same document as [R6] above; listed as the cross-reference for [R6], which is the tag actually used in the two documents) | yes (local text extraction) |
| REG-R70 | R35–R72 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | yes |
| REG-R71 | R35–R72 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Doc. No. 207) | yes (local text extraction) |

### Frozen entries not previously cited here

Id, title, publisher, URL, access date and fetched marker are carried from
`references/regulatory-and-actuarial-references.md`, together with the retrieval limits
and [unverified] flags that bear on how the entry may be used. **Ids are never renumbered.**
No new source was fetched at drafting.

**R1. Standard Valuation Law (Model #820)** — Publisher: National Association of Insurance
Commissioners (NAIC) · URL: https://content.naic.org/sites/default/files/model-law-820.pdf ·
Accessed: 2026-08-03 · Fetched: yes (27-page PDF retrieved and read; re-read for the reserves
stream at §§3, 4b, 5, 5a, 6, 7, 11, 12).

**R39. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With
Elective Benefits (AG 33)** — Publisher: NAIC · URL: none — **no free official standalone text
was located**; title and current status verified from the Valuation Manual's VM-C index
(page C-1); the authoritative text is in the **AP&P Manual Appendix C** · Accessed: 2026-08-04
(search date; guideline text not retrieved) · **Fetched: no.** AG 33 mechanics are quoted
nowhere in this library.

**R40. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve Method
to Equity Indexed Annuities (AG 35)** — Publisher: NAIC · URL: none — **no free official
standalone text was located**; exact title verified from the VM-C index (page C-2); the
authoritative text is in the **AP&P Manual Appendix C** · Accessed: 2026-08-04 (search date;
guideline text not retrieved) · **Fetched: no.** Same limit as R39.

**R39 and R40 are retained although neither document in this directory cites them any
longer.** They are the "AG 33 / AG 35 text not retrieved" records, **superseded in fact** by
**R151** and **R152** in the AP&P appendix block below. Their wording is frozen and is not
edited: a superseded record is evidence, not clutter — the same treatment R33 received when
R73 superseded it. Read them as history, never as a live limit.

**R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)** — Publisher:
NAIC · URL: same document as R3, pages A-1 to A-2 · Accessed: 2026-08-04 · Fetched: yes (local
text extraction; the complete two-page index read). **Limit carried forward:** VM-A is an
**index, not a text**. The requirements it indexes — including **A-250** (variable annuities)
and **A-255** (modified guaranteed annuities), and above all A-820 and A-830 — live in AP&P
Appendix A and **were not retrieved**.

**R110's limit is frozen and is superseded in fact for three of the items it names.** A-820,
A-250 and A-255 have since been read in full and carry their own ids — **R153**, **R156** and
**R157** in the AP&P appendix block below. R110 remains the authority for the VM-A *index*
itself and for the items still unread; its "were not retrieved" wording is preserved
unaltered and must not be read as current for A-820, A-250 or A-255.

### AP&P Manual appendix entries (R151–R157), read 2026-08-06

**Added after drafting — the only entries in this file that were.** All are appendix items of
the NAIC *Accounting Practices and Procedures Manual, As of March 2026*: the **same
2,117-page consolidated PDF already catalogued as R73**, a **free download** from
`content.naic.org` (catalogue entry "APPM-2026 … Free Download" on
https://content.naic.org/publications; file
https://content.naic.org/sites/default/files/publication-app-manual.pdf). They take
appendix-level ids rather than being folded into R73 so a document can cite **A-820 ¶15** or
**AG 33 *Text* 4** instead of a 2,117-page manual. Each was read by **local text extraction**
from that download. Id, title, publisher, URL, access date, fetched marker and every
retrieval limit below are carried from
`references/regulatory-and-actuarial-references.md`.
**Ids are never renumbered.** Only the five cited by the two documents in this directory are
listed: **R154** (A-830, valuation of life insurance policies) and **R155** (A-585, universal
life) are life-side items neither document cites.

**Edition line, stated once for all five.** None of these items prints "As of March 2026" on
its own pages. Every extracted page carries only the footer **"© 1999-2026 National
Association of Insurance Commissioners"**, which is a **copyright span, not an adoption,
effective or revision date** for any of these instruments and must never be cited as one. The
"As of March 2026" designation is the manual's own front matter, recorded at R73.

**Licence caution, inherited from R73 and applying to all five.** Personal and non-commercial
use; redistribution or integration "into any software or other publication" requires written
NAIC permission. Both documents in this directory **paraphrase the mechanics and cite the
paragraph, section or page**, and quote only short anchors.

**A-270 (Variable Life Insurance)** was extracted alongside R155 at printed pages A270-1 to
A270-3 = **PDF pages 1097–1099**, but the extraction **assigned it no reference id**. Nothing
in this directory is cited from it and **it must not be given one here**; any reference to it
stays descriptive.

**R151. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With
Elective Benefits (AG 33), as printed in the AP&P Manual** — Publisher: NAIC · URL:
https://content.naic.org/sites/default/files/publication-app-manual.pdf — **Appendix C —
Actuarial Guidelines**; printed pages **AG33-1 to AG33-8** = **PDF pages 1496–1503**; same
physical document as R73 · Accessed: 2026-08-06 · Fetched: yes (local text extraction; **all
eight printed pages read in full** — *Background Information*, *Purpose*, *Definitions*,
*Text* 1–7 and *Effective Date*). **Limits carried forward from
`_research/appp-ag33.md`:** the running heads confirm Appendix C, but these pages carry
**no volume statement** — the **Volume II** placement is R73's record, not theirs. They carry
**no amendment history, no adoption note and no revision log**, so the guideline's printed
*Effective Date* of **31 December 1998** cannot be reconciled here against the **31 December
1995** date the library carries from IRS Rev. Rul. 2002-6 for a differently-titled
instrument; **both are recorded and neither is presented as settled**. AG 33 contains **no
formulas, symbols, tables or factors** beyond the 7% expense allowance and the 1998–2000
phase-in percentages, and **names no other guideline anywhere** — not AG 35, not AG 43, so
the AG 33 / AG 43 / VM-21 precedence reading in `technical-notes.md` is the library's
inference. It **never cites SVL §5a by number**: the mapping to §5a is the library's own,
made on content. Cite by block (*Background* / *Definitions* / *Text*), since all three
restart at 1. Spurious intra-word spaces at justified-line breaks are text-layer artefacts
and were closed up in the research file's quotations. **Supersedes in fact:** **R39**
("guideline text not retrieved"), which is frozen and preserved unaltered above.

**R152. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve
Method to Equity Indexed Annuities (AG 35), as printed in the AP&P Manual** — Publisher: NAIC
· URL: https://content.naic.org/sites/default/files/publication-app-manual.pdf — **Appendix C
— Actuarial Guidelines**; printed pages **AG35-1 to AG35-10** = **PDF pages 1505–1514**; same
physical document as R73 · Accessed: 2026-08-06 · Fetched: yes (local text extraction; **all
ten printed pages read in full**, including Attachment 1 — the four computational methods,
Attachment 2 — the "Hedged as Required" criteria, and the Attachment 3 and 4 certification
forms). **Limits carried forward from `_research/appp-ag35.md`:** the guideline prints
**no effective, adoption or operative date, no transition, no phase-in, no grandfathering and
no sunset** — the only temporal language in the document is "regardless of the date of
issue", so **any date attached to AG 35 elsewhere is an inference from outside this text**. It
defines **no term "equity indexed annuity"**, contains **no symbols and no algebraic
notation** (every method is prose; the sole printed formula is `SP% = (1 - .03) ^ 5 = 86%`),
and prints **no volatility, dividend yield, risk-free curve or option pricing model**. Its
supersession clause reaches **Sections 5 and 6 of the NAIC Interest-Indexed Annuity Contracts
Model Regulation**, an instrument **not in this library at all** and recorded as a
cross-reference only. It names **Actuarial Guideline IX-B** three times as an alternative
source of the valuation interest rate; **AG IX-B has not been read**. **Product-specific
limit, and it is why this entry matters here:** AG 35 says nothing about separate accounts,
registered products, index-linked variable annuities, buffers, floors or AG 54, and is
recorded as **neither including nor excluding RILA**. **Supersedes in fact:** **R40**
("guideline text not retrieved"), frozen and preserved unaltered above.

**R153. Appendix A-820 — Minimum Life and Annuity Reserve Standards (with Appendix A-821,
Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities, and
Appendix A-822, Asset Adequacy Analysis Requirements)** — Publisher: NAIC · URL:
https://content.naic.org/sites/default/files/publication-app-manual.pdf — **Volume I,
Appendix A — Excerpts of NAIC Model Laws**; **A-820** printed A820-1 to A820-13 = **PDF pages
1186–1198**, **A-821** printed A821-1 to A821-6 = **PDF pages 1199–1204**, **A-822** printed
A822-1 = **PDF page 1205**; same physical document as R73 · Accessed: 2026-08-06 · Fetched:
yes (local text extraction; **A-820 ¶¶1–28 read in full**, **A-821 read in full** including
the 2012 IAM Period Table and Projection Scale G2 printed at its Appendices I–IV, and
**A-822's four paragraphs read in full**). **Limits carried forward from
`_research/appp-a820-a821-a822.md`:** **"As of March 2026" is not printed on PDF
pp. 1186–1205** — cite the copyright footer for what those pages print. **A-821 prints only**
the 2012 IAM Period Table and Projection Scale G2; the **1994 GAR** table and its `AA_x`
factors, the **Annuity 2000** table and **1983 Table "a"** are named and **not printed**, so
A-821 ¶16 is not computable from library sources, and **no standard is printed for individual
annuities issued before 1 January 2001**. A-820 **names its life mortality tables without
printing them** and the **2017 CSO is nowhere in its text**. Three text-layer repairs are
recorded in the research file rather than hidden: the **lost fraction bar at ¶7.a.i(a)** (the
term is `(W/2)·(R2 − .09)`), the lost `R1`/`R2` subscripts, and the **¶8.c weighting-factor
tables, which were reassembled by column position** from a scrambled layer. Two internal
oddities are recorded as printed and **not reconciled**: **¶22's empty window** and **¶7's
"effective date of the Codification"**, a threshold whose date A-820 never prints. **Naming
trap:** AP&P **Appendix A-822 is not NAIC Model #822**. **Cited here** only for ¶15 (the
CARVM print) and ¶¶7–10 (the valuation-rate machinery SSAP No. 56 ¶30 points at). **Supersedes
in fact:** the A-820 half of **R110**'s limit.

**R156. Appendix A-250 — Variable Annuities** — Publisher: NAIC · URL:
https://content.naic.org/sites/default/files/publication-app-manual.pdf — **Volume I,
Appendix A — Excerpts of NAIC Model Laws**; printed page **A250-1** = **PDF page 1095**; same
physical document as R73 · Accessed: 2026-08-06 · Fetched: yes (local text extraction; **the
whole item read in full** — three paragraphs, seven printed lines of substance). **Limit, and
it is the point of the entry:** A-250 is **a pointer, not a reserve method**. It gives a
definition, a separate-account asset-coverage requirement, and a delegation of the reserve
itself to **Appendix A-820** "in accordance with actuarial procedures that recognize the
variable nature of the benefits provided and any mortality guarantees". It contains **no
formula, no symbol, no factor, no table, no CARVM adaptation, no elective-benefit path rule,
no interim-value rule and not the word CARVM**, and prints **no effective date**. It is cited
by `technical-notes.md` for that **verified negative finding** as much as for anything it
supplies. **Supersedes in fact:** the A-250 half of **R110**'s limit.

**R157. Appendix A-255 — Modified Guaranteed Annuities** — Publisher: NAIC · URL:
https://content.naic.org/sites/default/files/publication-app-manual.pdf — **Volume I,
Appendix A — Excerpts of NAIC Model Laws**; printed page **A255-1** = **PDF page 1096**; same
physical document as R73 · Accessed: 2026-08-06 · Fetched: yes (local text extraction; **the
whole item read in full** — seven paragraphs). **Limit:** like A-250, A-255 delegates the
reserve method itself to **Appendix A-820**; what it adds is three operative rules — the
separate account liability must be at least the surrender value produced by **the contract's
own market-value-adjustment formula**, a shortfall against the market value of the separate
account assets must be made good by a transfer into that account, and any additional reserve
needed to cover future guaranteed benefits must be established. **No MVA formula and no
parameters for one are printed** — the formula is the contract's. Like A-250 it contains **no
formula, symbol, factor or table**, does **not mention CARVM**, and prints **no effective
date**. Its ¶1 definition is separately load-bearing for this product as the test VM-21
§2.A.2 uses to disapply VM-21 to contracts falling under VM-A item A-255 [REG-R35]; **that
exclusion is VM-21's text, not A-255's**, and A-255 supplies only the definition.
**Supersedes in fact:** the A-255 half of **R110**'s limit.

---

Corrections carried forward from the research files and made explicit in
`product-spec.md`, rather than repeating the common misstatements:

1. **Model #805's indexed nonforfeiture rate floor is 15 basis points (0.15%), not 1%** —
   the rate is the lesser of 3% and the five-year CMT (rounded to the nearest 1/20 of one
   percent) reduced by 125 basis points, subject to that 15 bp floor [REG-R42].
2. **The Annuity Disclosure Model Regulation is #245, not #250** — #250 is the Variable
   Annuity Model Regulation, verified from both model-law prints and from AG 54's own
   citation [REG-R43] [REG-R44] [REG-R45].
3. **Model #805 does not apply to a RILA if and only if AG 54 is satisfied**
   [REG-R42] [REG-R44].
4. **VM-21 does not automatically apply to a RILA**: §2.A.3 excludes separate-account
   contracts that guarantee an index and offer no GMDB/VAGLB [R3] [REG-R35].
5. **AG 43 is not simply superseded by VM-21** — through reference in AG 43, VM-21's
   requirements reach pre-2017 contracts outside VM-21's own scope [REG-R35] [REG-R38].
6. **VM-22 is not the RILA reserve standard** and, in the Jan. 1, 2026 edition, no longer
   holds the income-annuity maximum valuation interest rates (those are in VM-V §1) — see
   the VM-22 and VM-V entries in `_research/regulatory-actuarial-annuities.md`. Noted
   here only to prevent mis-application; neither entry is cited by the documents in this
   directory and neither is listed in the table above.
7. **"A RILA CARVM run rests on the SVL text alone, and A-250/A-255 are the closest
   formulaic items but were not read" is superseded.** All three have been read.
   **AG 33 applies** — to all annuity contracts subject to CARVM where elective benefits are
   available, with no product list, no separate-account exception and no threshold
   [REG-R151] — so the interpretive layer is now first-hand and the run rests on the SVL text
   *as read through AG 33*. **AG 35 was retrieved and does not address this design**; record
   it as neither including nor excluding RILA [REG-R152]. **A-250 and A-255 are not reserve
   methods at all** — one printed page each, each delegating the reserve to A-820, and between
   them containing no formula, symbol, factor, table, elective-path rule, interim-value rule
   or the word CARVM [REG-R156] [REG-R157]. Calling them "the closest formulaic items" is
   defensible only as *nearest by subject matter*. **A verified negative is a result**; what
   stays open is narrower — no retrieved document says how an Interim Value becomes "the
   future guaranteed benefit" of §5a.
8. **AG 33's printed effective date is December 31, 1998, not the December 31, 1995 the
   library carries from IRS Rev. Rul. 2002-6**, and the guideline's printed title is
   *Determining CARVM Reserves for Annuity Contracts With Elective Benefits* — which is the
   title R39 already carries correctly. The **January 1, 1981 issue reach is confirmed** and
   is the limb that binds every in-force RILA; the effective date is not. The extracted pages
   carry **no amendment history**, so "a later revision" is an inference, not a fact: **both
   dates are recorded and the reconciliation is unresolved** [REG-R151]. Related cautions
   from the same print: AG 33 contains **no formulas, tables or factors** beyond the 7%
   expense-allowance cap and the 33⅓ / 66⅔ / 100% grade-in, it **never cites SVL §5a by
   number** (the §5a mapping is the library's own, made on content), and **"efficient
   policyholder selection" is not its language and appears nowhere in it** — the actual
   construction is that experience-based elective incidence is prohibited, trial sets are
   maximised over, and the actuary must *"consider, not necessarily test"* all potential
   integrated benefit streams [REG-R151].

---

## Provenance note

Extraction details live in `_research/registered-index-linked-annuity.md`: that file
records which facts came from which source, the [unverified] flags, the per-insurer
interim-value algebra, the failed/blocked retrievals listed above, and the twelve
documented gaps — most consequentially that **no current declared rate sheet was
retrievable** (gap 1), that **annuity purchase rate tables were not found** (gap 2), that
**Trading Costs are required by AG 54 but quantified nowhere** (gap 8), and that **no
specimen contract or policy form was located for any of these products** (gap 7), so all
product facts come from prospectuses rather than from the contracts themselves. The
cross-product bibliographies `_research/regulatory-actuarial.md` (R1–R34) and
`_research/regulatory-actuarial-annuities.md` (R35–R72) play the same role for
[REG-R#] tags, as do `_research/appp-ag33.md` (R151), `_research/appp-ag35.md` (R152),
`_research/appp-a820-a821-a822.md` (R153) and
`_research/appp-a585-a250-a255-a270.md` (R156, R157 — and A-270, which carries **no
reference id** and must not be given one) for the AP&P Manual appendix items — those files
govern where they and any document in this directory disagree. Standardizations marked
**[std]** in `product-spec.md` and
`technical-notes.md` — including the entire declared-rate snapshot, the trading-cost
factor, the market-data assumptions used in the worked example, and every behavioral
assumption — are introduced at drafting and are not attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-registered_index_linked_annuity-r1
[R2]: #uslib-registered_index_linked_annuity-r2
[R3]: #uslib-registered_index_linked_annuity-r3
[R4]: #uslib-registered_index_linked_annuity-r4
[R5]: #uslib-registered_index_linked_annuity-r5
[R6]: #uslib-registered_index_linked_annuity-r6
[REG-R151]: #uslib-reg-r151
[REG-R152]: #uslib-reg-r152
[REG-R156]: #uslib-reg-r156
[REG-R157]: #uslib-reg-r157
[REG-R26]: #uslib-reg-r26
[REG-R3]: #uslib-reg-r3
[REG-R35]: #uslib-reg-r35
[REG-R38]: #uslib-reg-r38
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R44]: #uslib-reg-r44
[REG-R45]: #uslib-reg-r45
[REG-R49]: #uslib-reg-r49
[REG-R69]: #uslib-reg-r69
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
