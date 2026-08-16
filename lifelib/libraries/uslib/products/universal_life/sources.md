# Sources

Source ids, titles, publishers, URLs, access dates, and retrieval markers are carried
over verbatim from `_research/universal-life.md` (the citation ground truth for
[S#]/[R#] tags). Ids are never renumbered. Sources from the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted (dropped here: R9).
No new sources were fetched at drafting; nothing is marked "added at drafting".

Access date for all citations: 2026-08-03 — except the superseded-but-kept
**REG-R110** entry, accessed **2026-08-04**, and the post-drafting entries
**REG-R150 and REG-R153–REG-R155**, accessed **2026-08-06**.

---

## Primary product sources [S#]

(uslib-universal_life-s1)=

### S1. Symetra Life Insurance Company — "Symetra CAUL Universal Life Insurance — Fact Sheet" (LIM-1286 10/23)
- Publisher: Symetra Life Insurance Company (document distributed via Financial
  Markets Inc., an authorized distributor; PDF is the insurer's own fact sheet)
- Doc type: consumer/product fact sheet (2 pages)
- URL fetched: https://www.fmiagent.com/wp-content/uploads/2024-05-22_Symetra_CAUL_Product_Highlights_LIM-1286_10-23.pdf
- Retrieved: YES (full PDF read)

(uslib-universal_life-s2)=

### S2. Protective Life Insurance Company — "Protective Advantage Choice UL — Producer Guide" (PLAG.3459 (01.15))
- Publisher: Protective Life Insurance Company (distributed via MRW Financial,
  an authorized distributor; PDF is the insurer's producer guide)
- Doc type: producer/agent guide (8 pages)
- URL fetched: https://www.mrwfinancial.com/wp-content/uploads/Advantage-Choice-UL.pdf
- Retrieved: YES (full PDF read)

(uslib-universal_life-s3)=

### S3. Pacific Life Insurance Company — Sample (specimen) policy "Versa-Flex PRO" — FLEXIBLE PREMIUM ADJUSTABLE LIFE INSURANCE, policy form P08VP1 (8/08)
- Publisher: Pacific Life Insurance Company (official sample policy on
  pacificlife.com)
- Doc type: specimen policy (full contract, 19+ pages incl. policy specifications
  for a Male 35 Standard Nonsmoker, $100,000 basic coverage + riders, policy date
  Nov 1, 2007)
- URL fetched: https://www.pacificlife.com/content/dam/paclife/lid/public/sample-policies/Sample_Policy_VF%20PRO%20II.pdf
- Retrieved: YES (full PDF read)
- Role in this library: implementation anchor for monthly-deduction mechanics,
  GPT corridor table, guaranteed maximum COI table, surrender charge amortization,
  loan/withdrawal/grace/reinstatement provisions.

(uslib-universal_life-s4)=

### S4. Nationwide Life and Annuity Insurance Company — "Nationwide No-Lapse Guarantee UL II" producer presentation (FLM-1167AO.3 (06/22))
- Publisher: Nationwide (distributed via Krause Agency portal mirror)
- Doc type: producer marketing deck / product highlights (19 slides)
- URL fetched: https://portal.krauseagency.com/wp-content/uploads/2025/02/Nationwide-No-Lapse-Guarantee-Universal-Life.pdf
- Retrieved: YES (full PDF read)
- Role in this library: contrast case (guaranteed UL) for the current-assumption
  design; cited for market-role and out-of-scope rider/guarantee context.

(uslib-universal_life-s5)=

### S5. Symetra — CAUL product page, symetra.com (FAILED FETCH)
- URL attempted: https://www.symetra.com/IndividualsFamilies/Products/LifeInsurance/PermanentLifeInsurance/SymetraCAULUniversalLife/
- Retrieved: NO — HTTP 403 Forbidden. Current declared crediting rates
  (symetra.com/liferates) therefore not captured. Nothing cited from this source
  except the fact of the failed fetch (used to document why current-scale
  assumptions are [std]).

---

## Regulatory and actuarial references [R#] (product research file numbering)

(uslib-universal_life-r1)=

### R1. NAIC — Universal Life Insurance Model Regulation (Model 585), January 2001 reprint
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-585.pdf
- Retrieved: YES (full PDF read, 14 pages)

(uslib-universal_life-r2)=

### R2. IRC §7702 — Life insurance contract defined
- Publisher: Legal Information Institute, Cornell Law School (U.S. Code)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702
- Retrieved: YES (fetched and summarized)
- Caveat carried over: the fetch was summarized by an automated reader; exact
  subsection text should be re-verified before quoting in a formal document.

(uslib-universal_life-r3)=

### R3. IRC §7702A — Modified endowment contract defined
- Publisher: Legal Information Institute, Cornell Law School (U.S. Code)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702A
- Retrieved: YES (fetched and summarized)

(uslib-universal_life-r4)=

### R4. Society of Actuaries — 2017 Commissioners Standard Ordinary (CSO) Tables (resource page)
- Publisher: Society of Actuaries
- URL fetched: https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/
- Retrieved: YES (page fetched; it is chiefly a download index)
- Caveat carried over: 2017 CSO adoption-timeline and usage claims (mandatory from
  2020-01-01; UL guaranteed COI cap; terminal age 121) come from search-result
  context, not a fetched primary document, and remain [unverified].

(uslib-universal_life-r5)=

### R5. NAIC — Principle-Based Reserving (insurance topic page; gateway to Valuation Manual / VM-20)
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/insurance-topics/principle-based-reserving
- Retrieved: YES

(uslib-universal_life-r6)=

### R6. American Academy of Actuaries — Life Illustrations Practice Note (September 2021 update)
- Publisher: American Academy of Actuaries, Life Illustrations Work Group
- URL fetched: https://actuary.org/wp-content/uploads/2021/09/Life_Illustrations_Practice_Note_Update.pdf
- Retrieved: YES (fetched and summarized)

(uslib-universal_life-r7)=

### R7. SOA Research Institute & LIMRA — "2015-2021 Universal Life Premium Persistency and Lapse Rate Experience Study" (July 2024, revised December 2024) — Study Highlights
- Publisher: Society of Actuaries Research Institute and LIMRA
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/experience-studies/2024/15-21-ulpp-ulls.pdf
- Retrieved: YES (full highlights PDF read)
- Note carried over: detailed tables are behind the paid Experience Studies Pro
  package (not retrieved).

(uslib-universal_life-r8)=

### R8. Actuarial Standards Board — ASOP No. 2 (Revised Edition, Doc. No. 204): "Nonguaranteed Elements for Life Insurance and Annuity Products" (adopted September 2021)
- Publisher: Actuarial Standards Board
- URL fetched: https://www.actuarialstandardsboard.org/wp-content/uploads/2021/12/asop002_204-2.pdf
- Retrieved: YES (full PDF read)

(uslib-universal_life-r10)=

### R10. IIPRC (Interstate Insurance Product Regulation Commission) — Standards for Individual Flexible Premium Adjustable Life Insurance Policies (5-year review revision, 2014)
- Publisher: Interstate Insurance Product Regulation Commission
  (insurancecompact.org)
- URL: https://www.insurancecompact.org/sites/default/files/2023-08/140815-iiprc-l-09-i-5-yr-rev.pdf
- Retrieved: PARTIAL — PDF binary was downloaded but its text was not read;
  NO facts are cited from it. Cited in this library only as a located reference
  for the uniform product standards under which multi-state UL forms (e.g., the
  "ICC14"-prefixed Symetra form in [S1]) are filed.

Dropped (in the research file but not cited in these documents): R9 (NAIC Valuation
Manual, located but not fetched in the product research; Valuation Manual facts are
cited instead from the fetched cross-product entry [REG-R3] below).

---

## Cross-product regulatory references [REG-R#]

These are cited with the [REG-R#] prefix to avoid collision with the product research
file's own R-numbering. Full annotated entries (titles, publishers, URLs, retrieval
markers, access date 2026-08-03) live in `_research/regulatory-actuarial.md`;
the shared reference library is
`references/regulatory-and-actuarial-references.md` (same R-numbering, which now runs
**R1–R157**, with most of the **R73–R149** block unused; R1–R34 originate in
`_research/regulatory-actuarial.md` and R35–R72 — annuity-specific entries not
cited here — in `_research/regulatory-actuarial-annuities.md`; R150–R157 are the
post-drafting entries — the NAIC PBR topic page and the seven AP&P Manual appendix
items read at first hand on 2026-08-06, of which this directory cites **R153 (A-820,
with A-821 and A-822)**, **R154 (A-830)** and **R155 (A-585)**).
Entries cited by the two documents in this directory:

| Tag | Short title | Retrieval status (per that file) |
|---|---|---|
| REG-R3 | NAIC Valuation Manual, Jan. 1, 2026 edition (VM-01/02/20/31, VM-M/G/C/V) | fetched (cover, adoption history, full TOC read) |
| REG-R5 | NAIC Universal Life Insurance Model Regulation (Model #585) | fetched (same document as [R1] above) |
| REG-R6 | NAIC Valuation of Life Insurance Policies Model Regulation (Model #830, "XXX") | fetched |
| REG-R7 | Actuarial Guideline XXXVIII (AG 38), 2012 text incl. 8D/8E | fetched |
| REG-R13 | 26 U.S.C. §7702 (same statute as [R2] above) | fetched |
| REG-R14 | 26 U.S.C. §7702A (same statute as [R3] above) | fetched |
| REG-R16 | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R17 | 2017 CSO tables (SOA landing page; same page as [R4] above) | fetched (landing page) |
| REG-R18 | 2015 Valuation Basic Table (VBT) — SOA landing page | fetched (landing page) |
| REG-R19 | ILEC 2012–2019 Individual Life Mortality Experience Report (landing page) | fetched (landing page) |
| REG-R20 | LIMRA/SOA U.S. Individual Life Persistency Update (2009–2013) | fetched (landing page) |
| REG-R21 | LIMRA/SOA 2015–2021 UL Premium Persistency and Lapse/Surrender Study (landing page; highlights PDF fetched as [R7] above) | fetched (landing page) |
| REG-R23 | AAA — Life PBR Under VM-20 Practice Note (April 2020) | fetched |
| REG-R26 | ASOP No. 2 — Nonguaranteed Elements (same standard as [R8] above) | fetched |
| REG-R27 | ASOP No. 7 — Life or Health Cash Flow Analysis (rev. Dec 2025) | fetched |
| REG-R31 | ASOP No. 52 — Principle-Based Reserves for Life Products under the NAIC Valuation Manual | fetched |
| REG-R32 | ASOP No. 56 — Modeling | fetched |

Two entries are kept below in full annotated form rather than as table rows.
**REG-R110** is a superseded-but-kept record — the supersession notes of **REG-R153**
and **REG-R154** preserve it unaltered; **REG-R150** is a post-drafting entry from the
2026-08-06 pass. Id, title, publisher, URL, access date and fetched marker are carried
from `references/regulatory-and-actuarial-references.md`.
**Ids are never renumbered.**

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
- **Superseded in fact for five of the items it indexes**, the sentence above being preserved
  verbatim as the record of what was true when it was written. **A-820 is now R153, A-830 is
  R154, A-585 is R155, A-250 is R156 and A-255 is R157**, all read in full from the same free
  *As of March 2026* download as R73. **A-270, A-791, A-812, A-815, VM-A-814 and A-817 are
  still unretrieved**, and A-270, although extracted alongside R155, has **no reference id
  assigned** and is therefore not citable.

### REG-R150. NAIC — Principle-Based Reserving (insurance topic page)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/insurance-topics/principle-based-reserving
- **Accessed:** 2026-08-06 · **Fetched:** yes (page shows "Last Updated: 8/1/2025")
- **Note:** the shared-library entry for **this file's local [R5]** — the same document,
  now addressable from the cross-product bibliography. Cited for two verbatim statements:
  *"Effective Jan. 1, 2017, the Valuation Manual became operative"* and *"PBR which became
  an accreditation standard Jan. 1, 2020."* Do not confuse with **[REG-R5]**, which is the
  Universal Life Insurance Model Regulation (Model #585) — a different document that this
  file also cites.

### Entries added for the AP&P Manual appendix reading (2026-08-06)

Newly cited by the "Valuation and reserve pointers" section of `technical-notes.md`
and by the "Regulatory context" section of `product-spec.md`. Id, title, publisher,
URL, access date, fetched marker and limits are carried from
`references/regulatory-and-actuarial-references.md`. **Ids are never renumbered.**

**One physical document behind them.** R153, R154 and R155 are appendix items of the NAIC
*Accounting Practices and Procedures Manual, As of March 2026* — the same 2,117-page
consolidated PDF catalogued as **R73** (the manual itself; its entry lives in
`references/regulatory-and-actuarial-references.md` and is not reproduced here), a
**free download** from `content.naic.org`. They take
appendix-level ids so a document can cite **A-585 ¶8.c** or **A-820 ¶11** instead of a
2,117-page manual. **Edition line:** none of these items prints "As of March 2026" on its own
pages; every extracted page carries only the footer "© 1999-2026 National Association of
Insurance Commissioners", which is a **copyright span, not an adoption, effective or revision
date**, and must never be cited as one. **Licence caution inherited from R73:** personal and
non-commercial use; redistribution or integration "into any software or other publication"
requires written NAIC permission — the two documents in this directory paraphrase the
mechanics, cite the paragraph, and quote only short anchors. **A-270** (variable life) was
extracted alongside A-585 but was **assigned no reference id**; it is referred to
descriptively where the variable-UL sibling is discussed and **nothing is cited from it**.

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

### REG-R155. Appendix A-585 — Universal Life Insurance
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  **Volume I, Appendix A — Excerpts of NAIC Model Laws**; printed pages **A585-1 to A585-4** =
  **PDF pages 1102–1105**; same physical document as R73
- **Accessed:** 2026-08-06
- **Fetched:** yes (local text extraction; **¶¶1–13 and all three footnotes read in full**)
- **Limits carried forward from `_research/appp-a585-a250-a255-a270.md`:** the item's own
  "Relevant NAIC Model Laws/Regulations" line names only the **Standard Valuation Law (#820)** —
  **it does not name Model #585 anywhere**, so "A-585 *is* Model #585 §5" is unsupported by this
  print, and **Model #585 (R5) was not re-read against it**. A-585 carries the **valuation half
  only**: no nonforfeiture provisions, no mandatory policy provisions, no annual-report
  requirements and no separate interest-indexed UL section. It prints **no effective date** and
  **no number of any kind** — every rate, table and factor is delegated to A-820 (¶¶8.j, 10) — and
  its **¶8.f pointer to "paragraph 9 of Appendix A-820" does not resolve** against the A-820 print
  read at R153, where ¶9 is the reference-interest-rate paragraph. The fraction bars in ¶¶8.a.ii,
  8.f and 13 are **lost in the text layer**, so those denominators are **inferred from layout**,
  not read from a bar character.

---

## Provenance note

Extraction details live in `_research/universal-life.md`: that file records which
facts came from which source, including the [unverified] flags, the failed/partial
fetches (S5, R10), the mirror-hosting caveat for S1/S2/S4 (fetched from
authorized-distributor mirrors carrying the insurers' own form numbers), and the
vintage caveat that parameter levels are era-representative while mechanics are
stable. The cross-product bibliography `_research/regulatory-actuarial.md` plays
the same role for [REG-R#] tags — except for the AP&P appendix entries, whose provenance
files are `_research/appp-a820-a821-a822.md` (R153), `_research/appp-a830.md` (R154)
and `_research/appp-a585-a250-a255-a270.md` (R155, and A-270 unnumbered). Those files
record every text-layer artefact repaired and every reading **inferred from layout rather
than read**; where one of them and a document in this directory disagree, **the research
file governs**. Standardizations marked **[std]** in
`product-spec.md` and `technical-notes.md` are introduced at drafting and are not
attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-universal_life-r1
[R2]: #uslib-universal_life-r2
[R3]: #uslib-universal_life-r3
[R4]: #uslib-universal_life-r4
[R5]: #uslib-universal_life-r5
[R7]: #uslib-universal_life-r7
[R8]: #uslib-universal_life-r8
[REG-R3]: #uslib-reg-r3
[REG-R5]: #uslib-reg-r5
[S1]: #uslib-universal_life-s1
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
