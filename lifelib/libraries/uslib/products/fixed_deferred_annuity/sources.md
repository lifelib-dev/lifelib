# Sources

Source ids, titles, publishers, URLs, access dates and retrieval markers are carried over
**verbatim** from `_research/fixed-deferred-annuity.md` (the citation ground truth for
[S#]/[R#] tags). Ids are never renumbered. Sources in the research file that are not cited
by `product-spec.md` or `technical-notes.md` are omitted (dropped here: S17, S18, S19, R3,
R10 — see the note at the end of the [R#] section). **No new sources were fetched at
drafting; nothing is marked "added at drafting".**

Access date for all citations: **2026-08-04**, except the frozen [REG-R#] entries reproduced
in full at the end of this file, whose own access dates (2026-08-03 or 2026-08-04) are
carried from `references/regulatory-and-actuarial-references.md`, and the four AP&P Manual
appendix entries **REG-R151, REG-R152, REG-R153 and REG-R157**, accessed **2026-08-06** and
added after drafting. Those four are the only post-drafting additions; nothing else in this
file changed source or status.

---

## Primary product sources [S#]

(uslib-fixed_deferred_annuity-s1)=

### S1. Athene Annuity & Life Assurance Company — "ATHENE MaxRate® Multi-Year Guarantee Annuity (MYGA) CA Version", producer fact sheet AN1007-CA (10/14)
- Publisher: Athene Annuity & Life Assurance Company (Wilmington, DE; main administrative
  office Greenville, SC). PDF hosted on iPipeline's forms repository, which distributes
  carrier-authored producer material.
- Doc type: producer product fact sheet (2 pages), "FOR PRODUCER USE ONLY"
- URL fetched: https://files.ipipeline.com/AALAC/AN1007CA.pdf
- Retrieved: YES (full text extracted)
- Note carried over: this CA version has **no** market value adjustment provision.

(uslib-fixed_deferred_annuity-s2)=

### S2. Athene Annuity & Life Assurance Company of New York — "ATHENE MaxRate® Multi-Year Guarantee Annuity (MYG)", producer fact sheet AN1007-NY (06/16)
- Publisher: Athene Annuity & Life Assurance Company of New York (Nyack, NY)
- Doc type: producer product fact sheet (4 pages), New York only
- URL fetched: https://files.ipipeline.com/AALAC/AN1007NY.pdf
- Retrieved: YES (full text extracted)
- Role in this library: source of the **symmetrically capped** MVA (adjustment, positive or
  negative, not greater than the withdrawal charge) and of the renewal 5/4/3/2/1 schedule.

(uslib-fixed_deferred_annuity-s3)=

### S3. Voya Retirement Insurance and Annuity Company — "Voya Multi-Rate Annuity (Voya MRA)" prospectus, Form 424B3, dated May 1, 2021
- Publisher: Voya Retirement Insurance and Annuity Company (Windsor, CT), filed with the SEC
- Doc type: statutory prospectus for a single purchase payment, modified guaranteed deferred
  annuity contract (39 pages incl. Appendix I on the MVA); product closed to new sales
- URL fetched: https://www.sec.gov/Archives/edgar/data/837010/000010300521000017/definitivemultirateannuity.pdf
- Retrieved: YES (full text extracted, pages 1–17 and 37–39)
- Role: uncapped geometric Treasury-based MVA; the gross-up example for a net check.

(uslib-fixed_deferred_annuity-s4)=

### S4. Nationwide Life Insurance Company — "BOA Platinum Edge", Form S-1 registration statement / prospectus dated May 1, 2023, "Flexible Purchase Payment Modified Guaranteed Annuity Contracts Supporting Guaranteed Periods"
- Publisher: Nationwide Life Insurance Company (Columbus, OH), filed with the SEC
  (filed 2023-04-07)
- Doc type: registration statement containing the full prospectus, including Appendix A with
  MVA worked examples and a sensitivity table
- URL fetched: https://www.sec.gov/Archives/edgar/data/1127203/000119312523095286/d490814ds1.htm
- Retrieved: YES (full text extracted)
- Role in this library: **arithmetic unit-test anchor** for the geometric MVA branch — the
  only retrieved source with fully worked MVA numbers.

(uslib-fixed_deferred_annuity-s5)=

### S5. Midland National Life Insurance Company — "Oak ADVantage® multi-year guarantee annuity", consumer brochure 34158Y REV 6-26
- Publisher: Midland National Life Insurance Company (West Des Moines, IA), a Sammons
  Financial Group member. Official insurer domain.
- Doc type: consumer product brochure (8 pages)
- URL fetched: https://www.midlandnational.com/documents/35453/349595425/34158Y+-+Oak+ADVantage+brochure.pdf/57b2f6a9-d3fc-65d4-c613-83f262f42fab?t=1724168079212
- Retrieved: YES (full text extracted)
- Note carried over: features flagged as offered "by current company practice" are
  explicitly **not** contractual guarantees and can be withdrawn at any time.

(uslib-fixed_deferred_annuity-s6)=

### S6. Midland National Life Insurance Company — "Oak ADVantage℠ multi-year guarantee annuity" highlight sheet 34199Y REV 11-24
- URL fetched: https://www.midlandnational.com/documents/35453/65313/34199Y+-+Oak+ADVantage+highlight+sheet.pdf/efeb0d27-884d-e0f2-535d-6430a37a58ac?t=1635796256861
- Doc type: 2-page product highlight sheet
- Retrieved: YES

(uslib-fixed_deferred_annuity-s7)=

### S7. Midland National Life Insurance Company — "Oak ADVantage® and Oak ADVantage® Care" rate sheet 32400Y REV 7-23-26 (interest rates effective July 23, 2026)
- URL fetched: https://www.midlandnational.com/documents/35453/349595419/32400Y+-+Oak+ADVantage+rate+sheet.pdf/fa83c185-49b5-ef49-afc7-fdf4da62b245?t=1726160212636
- Doc type: 1-page producer rate sheet
- Retrieved: YES
- Caveat carried over: the declared rates 5.45% / 5.60% / 5.50% are certain, but the
  text-extraction order does not unambiguously bind each rate to its guarantee period; the
  3 / 5 / 7-year mapping is **[unverified]**. (No rate from S7 is used in the product
  documents; S7 is cited only for the $50,000 minimum premium and the Care variant.)

(uslib-fixed_deferred_annuity-s8)=

### S8. Midland National Life Insurance Company — "Understanding the market value adjustment", 32340Y-2 REV 7-25 (Midland National Capital Income® fixed index annuity)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32340Y+-+Understanding+the+MVA/7446bfd5-4e75-8e71-db85-e055f63ea9de
- Doc type: 2-page consumer MVA explainer
- Retrieved: YES
- **Caveat carried over:** written for the Capital Income *fixed index* annuity, not for a
  MYGA. Cited here because it states the Sammons/Midland MVA formula, base and caps
  explicitly, and Oak ADVantage uses the same MVA family [S5] [S6]; **the numeric example
  must not be attributed to a MYGA** and is labelled as such wherever used.

(uslib-fixed_deferred_annuity-s9)=

### S9. Midland National Life Insurance Company — "Midland National Capital Income® Fixed index annuity — Annuity disclosure statement", 32372Y-5 (8-24)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32372Y+-+Capital+Income+disclosure+for+most+states/f334edb5-4545-608e-3e7b-f8558ed021b8
- Doc type: signed annuity disclosure statement (12 pages)
- Retrieved: YES
- **Caveat carried over:** FIA, not a MYGA. Cited for (a) contractually-precise MVA wording,
  (b) the nonforfeiture-floor wording and its **net-of-charges** withdrawal convention, and
  (c) the disclosure-statement structure that Model #245 [R4] drives.

(uslib-fixed_deferred_annuity-s10)=

### S10. MassMutual Ascend Life Insurance Company — "SecureGain 5 Annuity — A fixed annuity with a market value adjustment", consumer brochure B1088822NW 4/23
- Publisher: MassMutual Ascend Life Insurance Company (Cincinnati, OH), a wholly owned
  subsidiary of Massachusetts Mutual Life Insurance Company (formerly Great American Life)
- Doc type: consumer brochure (12 pages) with a product-features specification table
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/b1088822nw.pdf?sfvrsn=845c2fde_3
- Retrieved: YES (full text extracted)
- Role: the charge/liquidity anchor — 9/8/7/6/5 early withdrawal charge, 10% free
  withdrawal, extended-care and terminal-illness waivers.

(uslib-fixed_deferred_annuity-s11)=

### S11. MassMutual Ascend Life Insurance Company — "SecureGain 5" client rate flier F1089525NW-1 (rates effective 09/22/25)
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/f1089525nw-1.pdf?sfvrsn=7b719de_1
- Doc type: 2-page rate flier with disclosure footnotes
- Retrieved: YES
- Note carried over: **the single best retrieved statement of the nonforfeiture floor in a
  real product** — the GMSV definition, its 2.80% rate, the 0.25% minimum interest rate and
  the express tie to NAIC Model #805.

(uslib-fixed_deferred_annuity-s12)=

### S12. MassMutual Ascend Life Insurance Company — "How a market value adjustment works", S6075424NW 8/24
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/s6075424nw.pdf?sfvrsn=d91920de_2
- Doc type: 2-page consumer MVA explainer
- Retrieved: YES
- Role: the **asymmetric** cap design (positive capped at the early withdrawal charge,
  negative floored by the standard nonforfeiture law minimum) and the blended
  Treasury/corporate reference indices.

(uslib-fixed_deferred_annuity-s13)=

### S13. New York Life Insurance and Annuity Corporation (NYLIAC) — "Secure Term MVA Fixed Annuity II — Just the facts", client fact sheet ML25-007661 / SMRU5821693 (Exp. 03.20.2028)
- Publisher: New York Life Insurance and Annuity Corporation (a Delaware corporation),
  wholly owned subsidiary of New York Life Insurance Company. Official insurer domain
  (nylannuities.com).
- Doc type: 4-page client fact sheet with full feature table and footnotes
- URL fetched: https://www.nylannuities.com/connectedassets/final-assets/marketing-materials/fact-sheet-products/TPD_Client_FactSheet_ST_MVA_II_Generic.pdf
- Retrieved: YES (full text extracted). An earlier WebFetch of the same URL and of an
  immediateannuities.com copy returned HTTP 403; the direct Python fetch succeeded.
- Role: the **Camp B** renewal architecture (annually redeclared rates, no new surrender
  charge) and the GMIR-floored MVA. Gap carried over: the exact MVA algebra is not in the
  fact sheet — it points to a separate "Examples and Explanation" flyer, not retrieved.

(uslib-fixed_deferred_annuity-s14)=

### S14. Symetra Life Insurance Company — "Form of Section 457 Contract Data Page", Exhibit 99.4(i) to Form 485BPOS for Symetra Separate Account C (filed 2009)
- Publisher: Symetra Life Insurance Company (Bellevue, WA), filed with the SEC
- Doc type: **specimen contract data page** (bracketed values), for the Spinnaker Advisor
  Variable Annuity
- URL fetched: https://www.sec.gov/Archives/edgar/data/0000912869/000119312509093761/dex994i.htm
- Retrieved: YES (full text extracted)
- **Caveat carried over:** a VA chassis, not a standalone MYGA, and the values are bracketed
  specimen values. Cited only for the MVA on its Guaranteed Interest Period Fixed Account
  Option — the classic **declared-rate-differential** `W × (Ic − In) × Fs` design with its
  contractual duration-factor table.

(uslib-fixed_deferred_annuity-s15)=

### S15. Forethought Life Insurance Company (Global Atlantic) — "SecureFore II Fixed Annuities" product page
- Publisher: Global Atlantic / Forethought Life Insurance Company (Indianapolis, IN)
- Doc type: insurer web page (not a disclosure document)
- URL fetched: https://www.globalatlantic.com/retirement-annuities/fixed-annuities/securefore-ii
- Retrieved: YES (web page)
- Note carried over: withdrawal charge percentages, issue ages, premium minima, death
  benefit and annuitization details were **not** stated on the page.

(uslib-fixed_deferred_annuity-s16)=

### S16. Oceanview Life and Annuity Company — "Harbourview Multi-Year Guaranteed Annuity — Product Disclosure", OVLAC-MYGA-DISC Rev. 01/20
- Publisher: Oceanview Life and Annuity Company. A smaller MYGA specialist, not a "major"
  carrier — included because it is a genuine signed **MYGA product disclosure** in the Model
  #245 format, which the majors do not post publicly.
- Doc type: 2-page signed product disclosure with owner/producer signature block
- URL fetched: https://oceanviewlife.com/wp-content/uploads/2020/05/OVLAC-MYGA-DISC.pdf
- Retrieved: YES (full text extracted)

**Dropped (in the research file, not cited here):** S17 (New York Life Secure Term MVA IV
fact sheet via Fidelity — Retrieved: **NO**, HTML interstitial); S18 (American Equity
GuaranteeShield brochure — Retrieved: **NO**, DNS resolution failure); S19 (three
immediateannuities.com brochures — Retrieved: **NO**, HTTP 403). Nothing is asserted from
any of them anywhere in this library.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(uslib-fixed_deferred_annuity-r1)=

### R1. NAIC — Model #805, "Standard Nonforfeiture Law for Individual Deferred Annuities" (NAIC Model Laws, Regulations, Guidelines and Other Resources — Fall 2020)
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (all 5 pages)
- **Correction carried over:** in the retrieved Fall 2020 edition the indexed nonforfeiture
  rate floor is **15 basis points (0.15%)**, not 1%. The corridor is
  `0.15% ≤ i ≤ 3.00%` with `i = round(5-yr CMT, 1/20 of 1%) − 1.25%`. The commonly cited 1%
  floor reflects the 2003 amendment as originally adopted and is **[unverified]**.
- Same document as [REG-R42].

(uslib-fixed_deferred_annuity-r2)=

### R2. NAIC — Valuation Manual, Jan. 1, 2026 edition; VM-22: Requirements for Principle-Based Reserves For Non-Variable Annuities
- Publisher: NAIC (© 2025 NAIC). 457-page PDF; VM-22 begins at PDF page 227 (manual page 22-1)
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (downloaded and text-extracted; VM-22 sections read directly)
- Gaps carried over: VM-22 Table 6.2 (partial withdrawals) was extracted only for the
  **Qualified** column and the attained-age-80-and-over row was truncated; the mandatory
  application date "three years after the effective date" is printed as a rule, not a date,
  so 2029 is arithmetic and carries **[unverified]**.
- Same document as [REG-R36] (and the parent Valuation Manual as [REG-R3]).

(uslib-fixed_deferred_annuity-r4)=

### R4. NAIC — Model #245, "Annuity Disclosure Model Regulation" (NAIC Model Laws — Summer 2021)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-245.pdf
- Retrieved: YES (40 pages; §§1–6 read)
- **Numbering note carried over:** the NAIC Annuity Disclosure Model Regulation is **#245**,
  not #250. (#250 is the Variable Annuity Model Regulation — see [REG-R43].)
- Same document as [REG-R45].

(uslib-fixed_deferred_annuity-r5)=

### R5. NAIC — Model #275, "Suitability in Annuity Transactions Model Regulation" (NAIC Model Laws — Spring 2020; the best-interest revision)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-275.pdf
- Retrieved: YES (20 pages; §§1–6 read)
- Same document as [REG-R46].

(uslib-fixed_deferred_annuity-r6)=

### R6. 26 U.S. Code § 72 — "Annuities; certain proceeds of endowment and life insurance contracts" (Cornell Legal Information Institute)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES (full section text)
- Same statute as [REG-R55].

(uslib-fixed_deferred_annuity-r7)=

### R7. IRS — Rev. Rul. 2002-6, 2002-1 C.B. (Section 807 — Rules for Certain Reserves), used to establish AG 33's identity and effective date
- URL fetched: https://www.irs.gov/pub/irs-drop/rr-02-6.pdf
- Retrieved: YES (3 pages)
- Gap carried over at drafting: "the full text of AG 33 was not retrieved … published in the
  NAIC Accounting Practices and Procedures Manual, Appendix C, which is not freely
  accessible." **Both halves of that gap are now closed and the entry must be read with the
  corrections below.** The AP&P Manual is a **free download** and was retrieved in full; AG 33
  was read as printed at **[REG-R151]**, so its mechanics are **no longer [unverified]**.
- **Corrections this entry now carries.** What R7 sources is the *Revenue Ruling's* account of
  AG 33, and it differs from the manual's print in two respects. (a) **Title:** R7 gives
  "Determining Minimum Commissioners Annuities Reserve Valuation Method (CARVM) Reserves for
  Individual Annuity Contracts"; the manual prints **"Determining CARVM Reserves for Annuity
  Contracts With Elective Benefits"** [REG-R151]. (b) **Effective date:** R7 gives
  **December 31, 1995**; the manual prints **December 31, 1998**, with the same
  **January 1, 1981** issue-date reach [REG-R151]. Both are recorded; the AG 33 pages carry
  **no amendment history**, so the reconciliation is **unresolved** and "a later revision" is
  an inference, not a fact from either document. R7 remains the citation for the 1995 date and
  the Revenue Ruling title, and for the IRS's §807(f) treatment; it is **not** a citation for
  the current guideline's title, date or mechanics.
- See also [REG-R39] (the frozen title-only record, superseded in fact by [REG-R151]).

(uslib-fixed_deferred_annuity-r8)=

### R8. Society of Actuaries Research Institute & LIMRA — "2023-2024 Fixed-Rate Deferred Annuity Surrender Study" (public report), February 2026
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2023-24-frda-public-report.pdf
- Retrieved: YES (7 pages — the public highlights report)
- Note carried over: detailed results sit behind the Experience Studies Pro subscription and
  were **not** retrieved; only the qualitative behavioural findings and the exposure
  statistics are cited.
- Related landing page catalogued cross-product as [REG-R63].

(uslib-fixed_deferred_annuity-r9)=

### R9. Society of Actuaries — 2012 Individual Annuity Reserving Report & Table; and the 2012 IAM Basic Table on mort.soa.org
- URLs fetched: https://www.soa.org/resources/experience-studies/2011/2012-ind-annuity-reserving-rpt/
  and https://mort.soa.org/ViewTable.aspx?TableIdentity=2581
- Retrieved: YES (web page; table page)
- Related entries in the cross-product library: [REG-R59] (Model #821 + VM-M definitions),
  [REG-R60] (the 2012 IAR development report).

**Dropped (in the research file, not cited here):** R3 (NAIC "Valuation Manual (VM)-22 (A)
Subgroup" committee page — retrieved, but nothing from it is cited; VM-22 facts come from
the manual itself at R2); R10 (SOA "2015-2022 Fixed Rate Deferred Surrender Experience
Study" — Retrieved: **NO**, HTTP 404; nothing asserted from it).

---

## Cross-product regulatory references [REG-R#]

Cited with the [REG-R#] prefix to avoid collision with the product research file's own
R-numbering. **[REG-R#] resolves against a single shared numbering space running R1–R157**,
with most of the **R73–R149** block unused. The numbering is curated in
`references/regulatory-and-actuarial-references.md`. Research provenance is split across
seven files: **R1–R34** (life-origin, several of which also bind annuity models) come from
`_research/regulatory-actuarial.md`; **R35–R72** (annuity-specific) come from
`_research/regulatory-actuarial-annuities.md`, which also carries the table showing which
of R1–R34 bind annuity models and how; and **R151–R157** (the seven AP&P Manual appendix
items, read at first hand on **2026-08-06**) come from `_research/appp-ag33.md` (R151),
`appp-ag35.md` (R152), `appp-a820-a821-a822.md` (R153), `appp-a830.md` (R154) and
`appp-a585-a250-a255-a270.md` (R155–R157). **Ids are never
renumbered.** Entries cited by the two documents in this directory:

| Tag | Provenance file | Short title | Retrieval status (per that file) |
|---|---|---|---|
| REG-R2 | life | Standard Nonforfeiture Law for Life Insurance (Model #808) — cited only to record that it does **not** apply to annuities | fetched |
| REG-R16 | life | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R26 | life | ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products | fetched |
| REG-R27 | life | ASOP No. 7 — Life or Health Cash Flow Analysis | fetched |
| REG-R29 | life | ASOP No. 22 — Opinions based on asset adequacy analysis | fetched |
| REG-R32 | life | ASOP No. 56 — Modeling | fetched |
| REG-R34 | life | FASB ASU 2018-12 (LDTI) | fetched |
| REG-R36 | annuities | VM-22 — PBR for Non-Variable Annuities (same document as [R2]) | fetched (local text extraction) |
| REG-R37 | annuities | VM-V §1 — statutory maximum valuation interest rates, income annuities | fetched (local text extraction) |
| REG-R39 | annuities | Actuarial Guideline XXXIII (AG 33) | **no** — title verified via REG-R41; mechanics [unverified]. **Frozen, and superseded in fact by [REG-R151]**, which read the guideline in full |
| REG-R41 | annuities | VM-C — index of actuarial guidelines incorporated into the Valuation Manual | fetched (local text extraction) |
| REG-R42 | annuities | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) (same document as [R1]) | fetched (local text extraction) |
| REG-R43 | annuities | Variable Annuity Model Regulation (Model #250) — cited for the #245/#250 numbering correction and the §7.B fixed-account carve-out | fetched (local text extraction) |
| REG-R44 | annuities | Actuarial Guideline LIV (AG 54) — ILVA nonforfeiture; cited for the Model #805 scope boundary | fetched (local text extraction, complete) |
| REG-R45 | annuities | Annuity Disclosure Model Regulation (Model #245) (same document as [R4]) | fetched (local text extraction) |
| REG-R46 | annuities | Suitability in Annuity Transactions Model Regulation (Model #275) (same document as [R5]) | fetched (local text extraction) |
| REG-R49 | annuities | SEC Release 33-11294 — registration for index-linked and **registered MVA** annuities; Form N-4 | fetched via govinfo.gov (sec.gov PDF returned 403); compliance date [unverified] |
| REG-R55 | annuities | 26 U.S.C. §72 (same statute as [R6]) | fetched |
| REG-R56 | annuities | 26 U.S.C. §1035 — exchanges | fetched |
| REG-R59 | annuities | NAIC Model #821 + VM-M annuity mortality definitions (2012 IAM/IAR, Scale G2) | fetched (local text extraction, both) |
| REG-R60 | annuities | 2012 Individual Annuity Reserving Table — AAA/SOA development report | fetched (local text extraction) |
| REG-R61 | annuities | 2020–2024 Individual Payout Annuity Mortality Experience Study | fetched (landing page) |
| REG-R62 | annuities | Fixed Indexed Annuity Policyholder Behavior Experience Studies | fetched (both landing pages); headline shock-lapse split [unverified] |
| REG-R63 | annuities | Fixed Rate Deferred Surrender Experience Studies (2023–24, 2015–2022) | partial (verified via the SOA index REG-R65); quantitative figures [unverified] |
| REG-R64 | annuities | VA contract holder behavior and GLB utilization studies | fetched (2022–24 landing page) |
| REG-R65 | annuities | SOA Individual Annuity Experience Studies — index | fetched |
| REG-R70 | annuities | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | fetched |
| REG-R71 | annuities | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Doc. No. 207) | fetched (local text extraction) |

Note on the curated page: `references/regulatory-and-actuarial-references.md` carries
**both halves — all of R1–R72** — with the life-origin entries (R1–R34) frozen and the
annuity entries (R35–R72) merged in. Research provenance remains split between
`_research/regulatory-actuarial.md` (R1–R34) and
`_research/regulatory-actuarial-annuities.md` (R35–R72); the numbering is the same
shared space in every file and is never renumbered.

Id, title, publisher, URL, access date and fetched marker of the frozen entries reproduced
below are carried from `references/regulatory-and-actuarial-references.md`.
**No new sources were fetched at drafting.** Two formatting notes, neither of which changes
any id: headings carry the **`REG-`** prefix used throughout this section, because the shared
numbering collides with the product research file's own `R#` numbering above (this file's
`R1` is Model #805; `REG-R1` is the Standard Valuation Law); and bare `R#` references
*inside* a carried-over entry are that entry's own text and resolve against the **shared
[REG-R#] numbering**, not against the `[R#]` section above.

**Frozen entries (R1–R72) newly cited here.**

### REG-R1. Standard Valuation Law (Model #820)
- **Publisher:** National Association of Insurance Commissioners (NAIC)
- **URL:** https://content.naic.org/sites/default/files/model-law-820.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (27-page PDF retrieved and read; re-read for
  the reserves stream at §§3, 4b, 5, 5a, 6, 7, 11, 12)

### REG-R40. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve Method to Equity Indexed Annuities (AG 35)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located.** Exact title verified from
  the VM-C index (page C-2) [R41]; the authoritative text is in the **AP&P Manual Appendix C**.
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no.** Same limit as R39.
- **Frozen, and superseded in fact by [REG-R152]**, which read AG 35 in full from the AP&P
  Manual on 2026-08-06. This record is preserved unaltered as evidence of what was true at
  drafting.

**AP&P Manual appendix entries (R151–R157) cited here — added after drafting.** Id, title,
publisher, URL, access date, fetched marker and carried-forward limits below are reproduced
from `references/regulatory-and-actuarial-references.md`. Three facts stated
there apply to all of them and are carried with the entries. (a) **One physical document:** all seven
R151–R157 items are appendix items of the NAIC *Accounting Practices and Procedures Manual,
As of March 2026* — the **same 2,117-page consolidated PDF already catalogued as R73**, a
**free download** from `content.naic.org`. They take appendix-level ids so a document can
cite **A-820 ¶15** or **AG 33 *Text* 4** instead of a 2,117-page manual. This supersedes in
fact the library's earlier record of the manual as a paid publication that could not be
fetched, which is what caused AG 33 and AG 35 to be cited by title only [REG-R39] [REG-R40].
(b) **Edition line:** none of these items prints "As of March 2026" on its own pages; every
extracted page carries only the footer "© 1999-2026 National Association of Insurance
Commissioners", which is a **copyright span, not an adoption, effective or revision date**
and must never be cited as one. (c) **Licence caution, inherited from R73:** personal and
non-commercial use; redistribution or integration "into any software or other publication"
requires written NAIC permission — so the two documents in this directory **paraphrase the
mechanics and cite the block, paragraph or page**, quoting only short anchors.

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
  Rev. Rul. 2002-6 [R7] for a differently-titled instrument; **both are recorded and neither is
  presented as settled**. AG 33 contains **no formulas, symbols, tables or factors** beyond the
  7% expense allowance and the 1998–2000 phase-in percentages, and **names no other guideline
  anywhere** — not AG 35, not AG 43. Cite by block (*Background* / *Definitions* / *Text*),
  since all three restart at 1. Spurious intra-word spaces at justified-line breaks are text-layer
  artefacts and were closed up in the research file's quotations.
- **Supersedes in fact:** **R39** ("guideline text not retrieved"), which is frozen and is
  preserved unaltered above.

### REG-R152. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve Method to Equity Indexed Annuities (AG 35), as printed in the AP&P Manual
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  **Appendix C — Actuarial Guidelines**; printed pages **AG35-1 to AG35-10** = **PDF pages
  1505–1514**; same physical document as R73
- **Accessed:** 2026-08-06
- **Fetched:** yes (local text extraction; **all ten printed pages read in full**, including
  Attachment 1 — the four computational methods, Attachment 2 — the "Hedged as Required"
  criteria, and the Attachment 3 and 4 certification forms)
- **Limits carried forward from `_research/appp-ag35.md`:** the guideline prints **no
  effective, adoption or operative date, no transition, no phase-in, no grandfathering and no
  sunset** — the only temporal language in the document is "regardless of the date of issue",
  so **any date attached to AG 35 elsewhere is an inference from outside this text**. It defines
  **no term "equity indexed annuity"**, contains **no symbols and no algebraic notation** (every
  method is prose; the sole printed formula is `SP% = (1 - .03) ^ 5 = 86%`), and prints **no
  volatility, dividend yield, risk-free curve or option pricing model**. Its supersession clause
  reaches **Sections 5 and 6 of the NAIC Interest-Indexed Annuity Contracts Model Regulation**,
  an instrument **not in this library at all** and recorded as a cross-reference only. It names
  **Actuarial Guideline IX-B** three times as an alternative source of the valuation interest
  rate; **AG IX-B has not been read** and is held only as a VM-C index entry (R41). Text-layer
  artefacts noted at the point of use: a lost superscript in the Attachment 2 option-replication
  `SP%` formula, and irregular intra-word spacing throughout.
- **Cited here for a negative finding only.** AG 35's Scope is limited to "all equity indexed
  annuity contracts, regardless of the date of issue, that are subject to CARVM", so it does
  **not** reach the book-value MYGA specified in this directory. **Nothing in its four
  computational methods is used or restated here.**
- **Supersedes in fact:** **R40** ("guideline text not retrieved"), frozen and preserved
  unaltered above.

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
  alone. R110 is frozen and is preserved unaltered in
  `references/regulatory-and-actuarial-references.md`.
- **Used in this directory for** the CARVM construction (¶15) and its scope gate (¶¶13.b, 14),
  and for the SVL §4b weighting-factor machinery AG 33 points at (¶8.c). **A-820 gives no
  elective-path list** — that is AG 33's subject [REG-R151].

### REG-R157. Appendix A-255 — Modified Guaranteed Annuities
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
  **no effective date**.
- **Cited here for a boundary, not a mechanic.** A-255 ¶1 defines a Modified Guaranteed Annuity
  by asset location — underlying assets **held in a separate account** during any period when the
  contract holder can surrender — so it does **not** reach the general account, book-value MYGA
  specified in this directory, and none of its rules is applied to the MVA modelled here.

---

## Provenance note

Extraction details live in `_research/fixed-deferred-annuity.md`: that file records which
facts came from which source, including the [unverified] flags (the Model #805 1% floor, the
Midland rate-to-period mapping, AG 33's mechanics, the pre-2026 content of VM-22, the
absence of a bailout provision, the VM-22 mandatory application date), the failed fetches
(S17, S18, S19, R10), the FIA-not-MYGA caveats on S8/S9, the VA-chassis caveat on S14, and
the "current company practice" caveat on S5/S6. **One of those flags is now closed:**
**AG 33's mechanics are no longer [unverified]** — the guideline was read in full from the
AP&P Manual on 2026-08-06 [REG-R151], and with it AG 35 [REG-R152] and A-820 with A-821 and
A-822 [REG-R153]. The research file's own R7 entry, its §15 and its Gaps item 1 still carry
the pre-2026-08-06 wording and the **December 31, 1995** date; the corrected record is the R7
entry above and the AG 33 paragraphs in `product-spec.md` and `technical-notes.md`. **Every
other flag in that list stands.** The cross-product bibliographies
`_research/regulatory-actuarial.md` (R1–R34),
`_research/regulatory-actuarial-annuities.md` (R35–R72) and the AP&P Manual appendix
extractions `_research/appp-ag33.md` (R151), `appp-ag35.md` (R152),
`appp-a820-a821-a822.md` (R153) and `appp-a585-a250-a255-a270.md` (R155–R157) play the same
role for [REG-R#] tags.
Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md` are
introduced at drafting and are not attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_deferred_annuity-r1
[R2]: #uslib-fixed_deferred_annuity-r2
[R4]: #uslib-fixed_deferred_annuity-r4
[R41]: #uslib-reg-r41
[R5]: #uslib-fixed_deferred_annuity-r5
[R6]: #uslib-fixed_deferred_annuity-r6
[R7]: #uslib-fixed_deferred_annuity-r7
[REG-R151]: #uslib-reg-r151
[REG-R152]: #uslib-reg-r152
[REG-R153]: #uslib-reg-r153
[REG-R3]: #uslib-reg-r3
[REG-R36]: #uslib-reg-r36
[REG-R39]: #uslib-reg-r39
[REG-R40]: #uslib-reg-r40
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R45]: #uslib-reg-r45
[REG-R46]: #uslib-reg-r46
[REG-R55]: #uslib-reg-r55
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R63]: #uslib-reg-r63
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
