# Sources

Source ids, titles, publishers, doc types, URLs, access dates and retrieval markers are
carried over **verbatim** from `_research/immediate-annuity.md` (the citation ground truth
for [S#]/[R#] tags). Ids are never renumbered. Sources in the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted — **none were dropped: every
S1–S11 and R1–R11 entry is cited.** No new sources were fetched at drafting; nothing is
marked "added at drafting".

Access date for all citations: **2026-08-04**, except the AP&P Manual appendix items
**REG-R151, REG-R152 and REG-R153**, added on **2026-08-06** and listed in their own section
below.

---

## Primary product sources [S#]

(uslib-immediate_annuity-s1)=

### S1. Massachusetts Mutual Life Insurance Company — "MassMutual RetireEase — A Single Premium Immediate Annuity" (AN1500 526 / MM202905-316012)
- Publisher: Massachusetts Mutual Life Insurance Company (official document served from
  MassMutual's own `compass.massmutual.com` asset service)
- Doc type: consumer product brochure with a formal "Product Highlights" spec section
  (8 pages, © 2026)
- URL fetched: https://compass.massmutual.com/api/public/assets/file/bltd6a32711c1c02d16
- Retrieved: YES (full PDF, text layer extracted; surrender-charge chart re-extracted with
  text-position coordinates to confirm the year→rate mapping)
- Product: MassMutual RetireEase, contract form **#SPIA05; SPIA05 (NC)**
- Role in this library: design anchor — issue ages and age basis, premium limits, the full
  joint-life option inventory with both reduction triggers, the 1–4% Inflation Protector
  COLA, and the **only published SPIA surrender-charge schedule** located in this research.

(uslib-immediate_annuity-s2)=

### S2. Pacific Life Insurance Company — "Pacific Income Provider — A Single-Premium, Immediate Fixed Annuity" fact sheet (FAC0719-00 11/25, item 25-555)
- Publisher: Pacific Life Insurance Company (official; `annuities.pacificlife.com`)
- Doc type: product fact sheet / spec sheet (4 pages)
- URL fetched: https://www.annuities.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/fact-sheets/pacific-income-provider-fact-sheet.pdf
- Retrieved: YES (full PDF read)
- Product: **Pacific Income Provider**, contract form series **ICC10:30-1181, 30-1181OR**
- Role in this library: design anchor — the cleanest published statement of the
  reduce-on-either-death versus reduce-on-primary-death distinction.

(uslib-immediate_annuity-s3)=

### S3. Pacific Life Insurance Company — "Pacific Income Provider — A Single-Premium, Immediate Fixed Annuity" client guide (FAC0718-0224)
- Publisher: Pacific Life Insurance Company (official; `pacificlife.com`)
- Doc type: consumer client guide (16 pages, Feb 2024 version)
- URL fetched: https://www.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/guide/pacific-income-provider-client-guide.pdf
- Retrieved: YES (full PDF read)
- Role: narrative confirmation of the joint-life trigger distinction; the cash-refund
  definition; and the only insurer hypothetical income illustrations located (explicitly
  "For illustrative purposes only").

(uslib-immediate_annuity-s4)=

### S4. Integrity Life Insurance Company / National Integrity Life Insurance Company (Western & Southern Financial Group) — "IncomeSource® Series Product Summary" (CF-51-0075-2406)
- Publisher: Western & Southern Financial Group (official; `westernsouthern.com`)
- Doc type: distributor/producer product summary (2 pages)
- URL fetched: https://www.westernsouthern.com/-/media/files/distributors/toolkits/incomesource-product-summary.pdf
- Retrieved: YES (full PDF read)
- Product: **IncomeSource** SPIA, contract series **ICC16 ENT-01 1701** / **ENT-01 1701 NY**;
  Deceased Commutation Rider **ICC09 ER.02 0901**; Living Commutation Rider **ICC09 ER.01
  0901**

(uslib-immediate_annuity-s5)=

### S5. New York Life Insurance and Annuity Corporation (NYLIAC) — "Just the facts about the New York Life Guaranteed Lifetime Income Annuity II" (1222A.1125 / ML25-006013 / SMRU5817113, exp. 06.27.2028)
- Publisher: New York Life (official; `nylannuities.com`)
- Doc type: client fact sheet / spec sheet (5 pages)
- URL fetched: https://www.nylannuities.com/connectedassets/final-assets/marketing-materials/fact-sheet-products/TPD_Client_FactSheet_GLI_II_Generic.pdf
- Retrieved: YES via direct HTTP with a browser user-agent. (Note: the same URL returned
  **HTTP 403** through the WebFetch tool; recorded as a tool-specific failure, not a dead
  link.)
- Product: **New York Life Guaranteed Lifetime Income Annuity II**, policy form
  **ICC11-P103** (may be **211-P103**)

(uslib-immediate_annuity-s6)=

### S6. Nationwide Life Insurance Company — "INCOME Promise® — A Single-premium Immediate Fixed Annuity" (NFS-0133-C (05/04))
- Publisher: Nationwide Life Insurance Company (PDF hosted on Nationwide's
  retirement-plans site `nrsforu.com`)
- Doc type: consumer brochure with a spec page (8 pages)
- URL fetched: https://www.nrsforu.com/BOA/media/pdf/NFS-0133.pdf
- Retrieved: YES (full PDF read). **Caveat carried over: this is a 2004-vintage document**
  (contracts APO-4834, APO-4834-37, APO-4834-43; Oklahoma APO-4834-36) — retained because it
  documents an older but very typical SPIA option set and terminology.

(uslib-immediate_annuity-s7)=

### S7. TIAA-CREF Life Insurance Company — "Single Premium Immediate Annuities" prospectus (Rule 497(c) filing, Registration No. 333-46414, dated May 1, 2008)
- Publisher: TIAA-CREF Life Insurance Company, filed with the SEC
- Doc type: **registered product prospectus** (SEC EDGAR)
- URL fetched: https://www.sec.gov/Archives/edgar/data/1067490/000119312508102441/d497.htm
- Retrieved: YES (full HTML, 256 KB of text). **Caveats carried over: 2008 filing**, used for
  its contractual precision on immediate-annuity mechanics, not as a currently-sold product
  spec; and these are single premium immediate **variable** annuity contracts with a
  fixed-account option, **not a pure fixed SPIA**.

(uslib-immediate_annuity-s8)=

### S8. Mutual of Omaha / United of Omaha Life Insurance Company — producer product overview (form 135880, updated 9-17)
- Publisher: Mutual of Omaha Insurance Company (official producer site)
- Doc type: producer portfolio overview (16 pages); **for producer use only**
- URL fetched: https://producer.mutualofomaha.com/enterprise/wcm/connect/14033a75-36a8-4542-b987-a96fa72cc5b3/135880.pdf?MOD=AJPERES&ContentCache=NONE
- Retrieved: YES (full PDF read). **Caveat carried over: dated 9-2017**; the current
  Ultra-Income brochure 404s and the product page host does not resolve, so the 6% COLA and
  "age rating" facts should be re-verified before being relied on.

(uslib-immediate_annuity-s9)=

### S9. LifeAnnuities.us — "Best SPIA Rates — July 2026: Top Payouts by Age"
- Publisher: LifeAnnuities.us (**commercial annuity-quote / lead-generation site — NOT an
  insurer, regulator, or actuarial body**)
- Doc type: rate-survey web page
- URL fetched: https://lifeannuities.us/rates/best-spia-rates/
- Retrieved: YES (HTML)
- **Reliability: LOW.** Carried over verbatim: recorded solely as a rate anchor of last
  resort because no insurer- or regulator-published payout-rate table could be retrieved.
  Numbers are indicative order-of-magnitude only and **must not be used as authoritative
  pricing**.

(uslib-immediate_annuity-s10)=

### S10. New York Life — "Annuity rates" page (weekly payout-rate publication)
- Publisher: New York Life (official; `nylannuities.com`)
- Doc type: rates web page
- URL fetched: https://www.nylannuities.com/resources/rates
- Retrieved: **PARTIAL** — page HTML retrieved successfully, but the rate tables are loaded
  client-side via JavaScript and rendered as "Loading…" in the static HTML, so **no numeric
  rates could be extracted**. Only the methodology text is cited.

(uslib-immediate_annuity-s11)=

### S11. The Guardian Life Insurance Company of America — "Single Premium Immediate Annuity (SPIA)" educational page (last updated January 29, 2026)
- Publisher: Guardian Life (official; `guardianlife.com`)
- Doc type: consumer education page (not a product spec sheet)
- URL fetched: https://www.guardianlife.com/annuities/income/single-premium-immediate-spia
- Retrieved: YES (HTML). Low specification content; cited only for the market-size datapoint,
  the timing framing, the premium/annuity-tax note, the 10%-penalty note and the mention of
  participating (dividend-paying) SPIA designs.

### Failed / unusable fetches (carried over for completeness; contents NOT used)

- `https://www.immediateannuities.com/annuity-brochures/massmutual-retireease.pdf` — **HTTP 403**.
- `https://www.immediateannuities.com/annuity-rates/by-age.html` — **HTTP 403** (both WebFetch and direct HTTP).
- `https://legacy.mutualofomaha.com/documents/annuities/lc3146.pdf` (Ultra-Income brochure) — **HTTP 404**.
- `https://webprod3.mutualofomaha.com/annuities/plan-details/ultra-income.php` — **DNS resolution failure**.
- `https://communications.fidelity.com/fili/spia/nyl/docs/new_york_life_lifetime_spia_factsheet.pdf` — HTTP 200 but the PDF has **no extractable text layer** (image-only); no facts taken.
- `https://communications.fidelity.com/fili/docs/ws-spia-factsheet.pdf` — returned a **230-byte stub**, not the document.
- `https://www.nylannuities.com/connectedassets/.../TPD_Client_FactSheet_GLI_II_Generic.pdf` via **WebFetch** — HTTP 403 (succeeded via direct HTTP; see S5).

---

## Regulatory and actuarial references [R#] (product research file numbering)

These [R#] ids are **product-local** to `_research/immediate-annuity.md` and are
independent of the cross-product [REG-R#] space below.

(uslib-immediate_annuity-r1)=

### R1. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-V: Statutory Maximum Valuation Interest Rates for Formulaic Reserves**, Section 1 "Income Annuities"
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457-page PDF; VM-V Section 1 at PDF pages 447–457)
- Note carried over: the maximum-valuation-interest-rate machinery for income annuities
  historically labelled VM-22 now sits in **VM-V**; VM-22 has been redefined as the
  principle-based reserve framework for non-variable annuities (R2).

(uslib-immediate_annuity-r2)=

### R2. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-22: Requirements for Principle-Based Reserves for Non-Variable Annuities**, and Section II "Reserve Requirements" Subsection 2
- Publisher: NAIC. Same URL as R1 (PDF pages 5, 16–21, 227–318)
- Retrieved: YES
- Contains the Payout Annuity Reserving Category definition, the prescribed Standard
  Projection mortality formula and **Table 6.8** (payout-annuity `F_x` factors, reproduced in
  full in the research file), and the age-basis conversion formula.

(uslib-immediate_annuity-r3)=

### R3. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-M Appendix M — Mortality Tables**, §1.J (2012 IAR) and §2.C (2012 IAM Basic)
- Publisher: NAIC. Same URL as R1 (PDF pages 445–446)
- Retrieved: YES
- Source of the generational application formula, the three-decimals-per-1,000 rounding rule
  and its worked example, and the definition of the 2012 IAM Basic table.

(uslib-immediate_annuity-r4)=

### R4. NAIC — **Model #821**, *Model Rule (Regulation) for Recognizing a New Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities* (January 2013 publication; recommended effective date 1/1/2014)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-821.pdf
- Retrieved: YES (5 pages)

(uslib-immediate_annuity-r5)=

### R5. NAIC — **Model #805**, *Standard Nonforfeiture Law for Individual Deferred Annuities* (Fall 2020 publication)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (5 pages)
- Carries the **verified** §2.A finding that immediate annuities are exempt.

(uslib-immediate_annuity-r6)=

### R6. **26 U.S.C. § 72** — Annuities; certain proceeds of endowment and life insurance contracts
- Publisher: Legal Information Institute, Cornell Law School (mirror of the U.S. Code)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES (via WebFetch)

(uslib-immediate_annuity-r7)=

### R7. IRS — **Publication 939, *General Rule for Pensions and Annuities*** (Rev. 12-2025)
- Publisher: Internal Revenue Service
- URL fetched: https://www.irs.gov/pub/irs-pdf/p939.pdf
- Retrieved: YES (85 pages)
- Source of the exclusion-ratio computation steps, the age-nearest convention, the
  expected-return rules by payout form, and the refund-feature adjustment worked example.

(uslib-immediate_annuity-r8)=

### R8. **Treas. Reg. § 1.401(a)(9)-6** — Required minimum distributions for defined benefit plans and annuity contracts
- Publisher: Legal Information Institute, Cornell Law School (mirror of 26 CFR)
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.401%28a%29%289%29-6
- Retrieved: YES (via WebFetch)

(uslib-immediate_annuity-r9)=

### R9. SOA Research Institute & LIMRA — **2020-2024 Individual Payout Annuity Mortality Experience Study** (study highlights, © 2026)
- Publisher: Society of Actuaries Research Institute (Individual Annuity Experience
  Committee) with LIMRA
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2020-24-payout-annuity-exp-study.pdf
- Retrieved: YES (5-page public "Study Highlights"; the detailed report and dashboards are
  behind the paid Experience Studies Pro package — **not retrieved**)

(uslib-immediate_annuity-r10)=

### R10. **26 U.S.C. § 130** — Certain personal injury liability assignments (structured settlements)
- Publisher: Legal Information Institute, Cornell Law School
- URL fetched: https://www.law.cornell.edu/uscode/text/26/130
- Retrieved: YES (via WebFetch)
- Cited only to distinguish structured settlements (no commutation permissible at all) from
  the retail SPIA in scope here.

(uslib-immediate_annuity-r11)=

### R11. Wisconsin Office of the Commissioner of Insurance — **PI-214, *Consumer's Guide to Understanding Annuities*** (R 09/2025)
- Publisher: State of Wisconsin OCI
- URL fetched: https://oci.wi.gov/Documents/Consumers/PI-214.pdf
- Retrieved: YES
- Cited only for the regulator's plain-language framing of the income-start window.

---

## Cross-product regulatory references [REG-R#]

Cited with the [REG-R#] prefix to avoid collision with the product research file's own
R-numbering above. The curated library is
`references/regulatory-and-actuarial-references.md`. **[REG-R#] is one shared numbering
space running R1–R157**, with most of the **R73–R149** block **unused**: entries **R1–R34**
originate in `_research/regulatory-actuarial.md` (the life-origin bibliography, several
of whose entries also bind annuity models) and entries **R35–R72** in
`_research/regulatory-actuarial-annuities.md` (the annuity-specific continuation, which
opens at R35 and explicitly freezes R1–R34). Entries cited by the two documents in this
directory:

| Tag | Half | Short title | Retrieval status (per the research file) |
|---|---|---|---|
| REG-R1 | R1–R34 | Standard Valuation Law (Model #820) | fetched |
| REG-R3 | R1–R34 | NAIC Valuation Manual, Jan. 1, 2026 edition (parent document) | fetched |
| REG-R16 | R1–R34 | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R27 | R1–R34 | ASOP No. 7 — Life or Health Cash Flow Analysis | fetched |
| REG-R29 | R1–R34 | ASOP No. 22 — opinions based on asset adequacy analysis | fetched |
| REG-R31 | R1–R34 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual (cited for its *non*-applicability to annuities) | fetched |
| REG-R32 | R1–R34 | ASOP No. 56 — Modeling | fetched |
| REG-R33 | R1–R34 | NAIC AP&P Manual **catalogue page**, which recorded the manual itself as a **paid publication, not fetched**. **Superseded in fact** by REG-R73 (the *As of March 2026* edition is a free download, retrieved in full) and, for Appendix A-821 and its printed 2012 IAM / Scale G2 tables, by **REG-R153** | catalogue page fetched; the manual was **not** fetched under this entry |
| REG-R34 | R1–R34 | FASB ASU 2018-12 (LDTI) | fetched |
| REG-R36 | R35–R72 | VM-22: PBR for Non-Variable Annuities (Valuation Manual, 2026 ed.) | yes (local text extraction) |
| REG-R37 | R35–R72 | VM-V §1 — Income Annuities (Valuation Manual, 2026 ed.) | yes (local text extraction) |
| REG-R41 | R35–R72 | VM-C Appendix C — index of incorporated actuarial guidelines (AG IX, IX-A, IX-B, IX-C) | yes (local text extraction) |
| REG-R42 | R35–R72 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) — same document as [R5] above | yes (local text extraction) |
| REG-R43 | R35–R72 | Variable Annuity Model Regulation (Model #250) — §7.A immediate-annuity exclusion | yes (local text extraction) |
| REG-R45 | R35–R72 | Annuity Disclosure Model Regulation (Model **#245**) | yes (local text extraction) |
| REG-R46 | R35–R72 | Suitability in Annuity Transactions Model Regulation (Model #275) | yes (local text extraction) |
| REG-R55 | R35–R72 | 26 U.S.C. §72 (same statute as [R6] above) | yes |
| REG-R56 | R35–R72 | 26 U.S.C. §1035 — exchanges | yes |
| REG-R57 | R35–R72 | 26 C.F.R. §1.401(a)(9)-6 (same regulation as [R8] above) | yes |
| REG-R58 | R35–R72 | RMD Final Regulations (T.D. 10001) | yes (govinfo) |
| REG-R59 | R35–R72 | Model #821 + VM-M annuity mortality definitions (same documents as [R3] [R4] above) | yes (local text extraction, both) |
| REG-R60 | R35–R72 | 2012 IAR development report (AAA/SOA Payout Annuity Table Team, Sept 2011) | yes (local text extraction) |
| REG-R61 | R35–R72 | 2020–2024 Individual Payout Annuity Mortality Experience Study (landing page; the highlights PDF is [R9] above) | yes (landing page) |
| REG-R70 | R35–R72 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | yes |
| REG-R71 | R35–R72 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity and Health Products (Doc. No. 207) | yes (local text extraction) |

Verified at drafting: the curated page `references/regulatory-and-actuarial-references.md`
carries every entry of the R1–R157 numbering still in use, so every [REG-R#] tag above and
below resolves there. The "Half" column records which research file each entry's annotation
originates in, because the halves were compiled separately and R1–R34 are frozen against
renumbering.

### Superseded entries retained as records

Id, title, publisher, URL, access date and fetched marker are carried from
`references/regulatory-and-actuarial-references.md`. **Ids are never renumbered.** One
frozen R1–R72 entry — **R39** — appears here because it had not previously been cited by this
directory; after the 2026-08-06 AP&P appendix pass **neither document cites R39 any longer**,
and it is retained rather than deleted because a superseded record is evidence (see the
supersession bullet on the entry itself, and REG-R151 in the section that follows). Access
date for every entry below: **2026-08-04**.

#### REG-R39. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located.** Title and current status
  verified from the Valuation Manual's VM-C index (page C-1) [REG-R41]; the authoritative text
  is in the **AP&P Manual Appendix C**.
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no.** No AG 33 mechanic is quoted anywhere in this library, and every
  document that touches it says so at the point of use.
- **Superseded in fact by [REG-R151], 2026-08-06.** The four lines above are preserved
  verbatim as the record of what was true when they were written. The AP&P Manual proved to
  be a **free download**, AG 33 was read in full at Appendix C, printed pages AG33-1 to
  AG33-8, and **R151 is the citable entry**. R39 is frozen and is never renumbered or
  rewritten; do not cite it for guideline mechanics.

#### REG-R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages A-1 to A-2; same document as [REG-R3])
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; the complete two-page index read)
- **Limit carried forward:** VM-A is an **index, not a text**. The requirements it indexes —
  above all **A-820** and **A-830** — live in AP&P Appendix A and **were not retrieved**.
- **Superseded in fact for A-820, 2026-08-06**, the sentence above being preserved verbatim as
  the record of what was true when it was written. **A-820 (with A-821 and A-822) is now
  [REG-R153]**, read in full from the free *As of March 2026* download. **A-830 is [REG-R154]**
  in the cross-product library but is not cited by this directory (it is life-insurance
  valuation and has **no annuity content**). VM-A remains an index; R110 is frozen and
  unaltered.

### Entries added at this pass — AP&P Manual appendix items read at first hand

Cited by the `## Regulatory context` and `## Riders and options` sections of
`product-spec.md` (**REG-R151** and **REG-R153**) and by the `## Model scope and conventions`,
`## Assumption inputs`, `## Policyholder behavior modeling` and `## Valuation and reserve
pointers` sections of `technical-notes.md` (**REG-R151** and **REG-R153**).
Id, title, publisher,
URL, access date, fetched marker and every carried-forward limit are reproduced
from `references/regulatory-and-actuarial-references.md` (which carries them from
the extraction files `_research/appp-ag33.md`, `_research/appp-ag35.md` and
`_research/appp-a820-a821-a822.md`). **Ids are never renumbered.** Access date for every
entry below: **2026-08-06**.

**One physical document behind R151–R157.** All seven are appendix items of the NAIC
*Accounting Practices and Procedures Manual, As of March 2026* — the **same 2,117-page
consolidated PDF already catalogued as R73**, a **free download** from `content.naic.org`
(catalogue entry "APPM-2026 … Free Download" on https://content.naic.org/publications;
file https://content.naic.org/sites/default/files/publication-app-manual.pdf). They take
appendix-level ids rather than being folded into R73 so a document can cite **A-820 ¶15** or
**AG 33 *Text* 4** instead of a 2,117-page manual. Each was read by **local text extraction**
from that download. **This directory cites two of the seven — R151 and R153** (R152, AG 35,
is retained below for its scope fact alone). R154
(A-830, life valuation, no annuity content), R155 (A-585, universal life), R156 (A-250) and
R157 (A-255) bear on other products and are not cited here.

**Edition line, stated once.** None of these items prints "As of March 2026" on its own
pages. Every extracted page carries only the footer **"© 1999-2026 National Association of
Insurance Commissioners"**, which is a **copyright span, not an adoption, effective or
revision date** for any of these instruments and must never be cited as one.

**Licence caution, inherited from R73.** Personal and non-commercial use; redistribution or
integration "into any software or other publication" requires written NAIC permission. Both
documents in this directory **paraphrase the mechanics and cite the paragraph, section or
block**, and quote only short anchors.

**A-270 (Variable Life Insurance)** was extracted alongside R155 but the extraction **assigned
it no reference id**. It is not cited anywhere in this directory and is **not citable as
[REG-R#]**.

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
  preserved unaltered above.
- **Product note, this directory only:** AG 33 **never cites SVL §5a by number** — its only
  numbered SVL cross-references are to §4b and §4b.C(1)(c)(vi). Where this directory maps AG 33
  onto §5a, that mapping is **the library's own, made on content**, and is labelled as such at
  the point of use.

#### REG-R152. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve Method to Equity Indexed Annuities (AG 35), as printed in the AP&P Manual
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
  rate; **AG IX-B has not been read** and is held only as a VM-C index entry (REG-R41).
- **Supersedes in fact:** **R40** ("guideline text not retrieved"), frozen and unaltered.
- **Why this entry is retained:** for a **scope fact only** — AG 35 reaches equity indexed
  *immediate* annuities, not deferred ones alone. The composite specified here is a **fixed**
  SPIA, so no AG 35 mechanic is applied to it and none is reproduced.

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
  **Appendix A-822 is not NAIC Model #822** — A-820's own header does not list Model
  #820 while A-822's does.
- **Supersedes in fact:** the A-820 half of **REG-R110**'s limit ("A-820 and A-830 as printed in
  the AP&P Manual were not retrieved"), and, for the paragraphs it carries, the reliance on
  REG-R1 alone. R110 is frozen and is preserved unaltered above.
- **Product note, this directory only:** the paragraphs cited here are **¶6** (the CARVM triple),
  **¶¶7.a.i(b), 8.b, 9.b** (the SPIA valuation rate, W = .80), **¶¶13.b, 14, 15** (CARVM and its
  scope gate), **¶¶16–18** (minimum reserve, optional higher standard, appointed-actuary
  reserves), **¶19** (deficiency reserves), **A-821 ¶¶10–12, 15** with Appendices I–IV (annuity
  mortality and the printed 2012 IAM / Scale G2 tables), and **A-822 ¶¶3–4** (the asset adequacy
  additional reserve).

---

## Provenance note

Extraction details live in `_research/immediate-annuity.md`: that file records which facts
came from which source, including every [unverified] flag, the failed/partial fetches (S10 and
the block above), the low-reliability marking on S9, the vintage caveats on S6/S7/S8, and the
research gaps this specification inherits — no specimen contract retrieved; **no published
payout-factor tables or guaranteed annuity purchase rates**; **no published commutation /
interest-rate-adjustment formula from any fixed SPIA issuer**; the 2012 IAM Period, 2012 IAM
Basic and Scale G2 numerical tables not retrieved (they live in Appendices 1–4 of AP&P Manual
Appendix A-821); NAIC-published VM-V rate inputs (Weight Tables 1–4, Table X spreads, VM-20
Table A) not retrieved; the paywalled detail of the SOA payout annuity study; and unresearched
state premium tax rates. The cross-product bibliographies
`_research/regulatory-actuarial.md` (R1–R34) and
`_research/regulatory-actuarial-annuities.md` (R35–R72) play the same role for
[REG-R#] tags; where one of them and a document in this directory disagree, **the research
file governs**. Standardizations marked **[std]** in `product-spec.md` and
`technical-notes.md` are introduced at drafting and are not attributable to any source.

**Correction to this note, 2026-08-06 (AP&P appendix pass).** Two of the research gaps listed
above have moved, and the pass's own bibliographies are
`_research/appp-ag33.md`, `_research/appp-ag35.md` and
`_research/appp-a820-a821-a822.md`, which govern R151–R153 the same way.

- **Closed.** The **2012 IAM Period Table and Projection Scale G2** *have* now been retrieved —
  A-821 prints both in full at its Appendices I–IV and they are transcribed in the research
  file [REG-R153]. The AP&P Manual is a **free download**, not the paid publication recorded at
  REG-R33. AG 33's text is retrieved [REG-R151], superseding REG-R39.
- **Still open, and narrowed rather than removed.** The **2012 IAM Basic** table — the
  best-estimate base — is **still not retrieved**; A-821 prints the *loaded* Period Table only.
  A-821 prints **no valuation standard for individual annuities issued before 1/1/2001**, and
  names but does not print the **1994 GAR**, **Annuity 2000** and **1983 Table "a"** tables. The
  VM-V rate inputs, the SOA study detail, the payout-factor and commutation gaps and the state
  premium tax rates are **untouched by this pass**.
- **[unverified] flags.** Two were closed by primary text at this pass and are named where they
  closed: that AG 33 mechanics were unavailable, and that A-820's mechanics were second-hand.
  **Everything else stays [unverified]**, including the commutation discount basis (assumption
  note (ii)), the absence of a PBR ASOP for annuities, and the SEC-registration conclusion.
  **AG 33's own effective date is a new [unverified] item opened by this pass**, not a closed
  one: the manual prints 31 December 1998, the library carried 31 December 1995 from IRS
  Rev. Rul. 2002-6 under a different title, and the extracted pages carry no amendment history
  to reconcile them [REG-R151].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #uslib-immediate_annuity-r3
[R4]: #uslib-immediate_annuity-r4
[R5]: #uslib-immediate_annuity-r5
[R6]: #uslib-immediate_annuity-r6
[R8]: #uslib-immediate_annuity-r8
[R9]: #uslib-immediate_annuity-r9
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R154]: #uslib-reg-r154
[REG-R3]: #uslib-reg-r3
[REG-R41]: #uslib-reg-r41
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
