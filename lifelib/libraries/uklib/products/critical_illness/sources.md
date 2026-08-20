# Sources

Source ids, titles, publishers, URLs, access dates, and retrieval markers are carried
over verbatim from `_research/critical-illness.md` (the citation ground truth for
[S#]/[R#] tags). Ids are never renumbered. Sources from the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted (dropped here: R11).
No new sources were fetched at drafting; nothing is marked "added at drafting".

Access date for all citations: 2026-08-03.

---

## Primary product sources [S#]

(uklib-critical_illness-s1)=

### S1. Legal & General — "Life Insurance / Critical Illness Cover — Policy Terms and Conditions" (QGI14872 — 2026/07)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy conditions (combined booklet: Life Insurance PB QGI12849 +
  Critical Illness Cover PB)
- URL: https://www.legalandgeneral.com/asset/499546/globalassets/personal/life-cover/_resources/documents/qgi14872.pdf
- Fetched: YES (PDF, 47 pp., full text extracted)
- Role in this library: current direct (D2C) retail product; primary wording anchor
  for the composite (conditions list, survival period, additional payments,
  children's cover, options, exclusions, misrepresentation remedy).

(uklib-critical_illness-s2)=

### S2. Legal & General — adviser Critical Illness Cover product page
- Publisher: Legal & General
- Doc type: technical guide / adviser product page
- URL: https://www.legalandgeneral.com/adviser/protection/products/personal-protection/critical-illness-cover/
- Fetched: YES (HTML, summarised by fetch tool — product limits)
- Caveat carried over: the adviser-page numbers (max sums assured £2m/£3m, min term
  2 years for some options) come from a fetch-tool summary of a JS-heavy page;
  plausible but not verified against a second document.

(uklib-critical_illness-s3)=

### S3. Legal & General — "Critical Illness Cover and Critical Illness Extra with Life Insurance — Policy Booklet" (QGI14162)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy conditions (intermediary "My Life" variant; reviewable premiums)
- URL: https://am.landg.com/asset/4a07ae/globalassets/adviser/files/protection/my-life/landg/policy-booklet/cic-two/cic-two-policybooklet08.pdf
- Fetched: YES (PDF, 42 pp., full text extracted)
- Caveat carried over: the two L&G booklets differ (retail QGI14872 guaranteed-premium
  vs intermediary QGI14162 reviewable-premium, 10- vs 14-day child survival); facts
  are cited to the correct variant.

(uklib-critical_illness-s4)=

### S4. Aviva — "Critical Illness+ — Policy Conditions" (AL51002, 04/2025)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: policy conditions
- URL: https://static.aviva.io/content/dam/document-library/adviser/individualprotection/al51002c.pdf
- Fetched: YES (PDF, 47 pp., full text extracted; WebFetch was 403 — retrieved via
  direct HTTPS GET)

(uklib-critical_illness-s5)=

### S5. Aviva — "Policy Summary of Critical Illness+" (AL51001, 04/2025)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: key features document / policy summary
- URL: https://static.aviva.io/content/dam/document-library/adviser/individualprotection/al51001c.pdf
- Fetched: YES (PDF, 28 pp., full text extracted)

(uklib-critical_illness-s6)=

### S6. Royal London — "Critical Illness Cover at a glance" (SAP8P10029/14, June 2025)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: adviser sales aid / product summary
- URL: https://adviser.royallondon.com/globalassets/docs/protection/SAP8P10029-critical-illness-cover-at-a-glance.pdf
- Fetched: YES (PDF, 2 pp., full text extracted)

(uklib-critical_illness-s7)=

### S7. Royal London — adviser page "Details of Critical Illness Cover"
- Publisher: Royal London
- Doc type: adviser product page
- URL: https://adviser.royallondon.com/protection/personal-protection/critical-illness-cover/detail/
- Fetched: YES (HTML, summarised by fetch tool)

(uklib-critical_illness-s8)=

### S8. Royal London — "Personal Menu Plan — Life or Critical Illness Cover — Plan details" (PCP8P10010, July 2025)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: policy conditions (plan details, 84 pp.)
- URL: https://adviser.royallondon.com/globalassets/docs/protection/pcp8p10010-plan-details-for-the-personal-menu-plan-life-or-critical-illness-cover.pdf
- Fetched: YES (PDF, 84 pp., full text extracted)
- Caveat carried over: definitions-focused; Royal London entry ages/term/sum limits
  were not found in the fetched plan details.

(uklib-critical_illness-s9)=

### S9. Vitality — "Serious Illness Cover" public product page
- Publisher: Vitality (VitalityLife)
- Doc type: product page (marketing but with concrete plan facts)
- URL: https://www.vitality.co.uk/life-insurance/serious-illness-cover/
- Fetched: YES (via browser; vitality.co.uk blocks non-browser fetches)

(uklib-critical_illness-s10)=

### S10. VitalityLife — "VitalityLife Essentials Plan Summary" (mirror hosted by LifeQuote)
- Publisher: VitalityLife (document); mirror host: LifeQuote (lifequote.co.uk)
- Doc type: key features document / plan summary
- URL: https://www.lifequote.co.uk/cdrom/KFDocsProps/VitalityLife/VitalityLife%20KFD.pdf
- Fetched: YES (PDF, 16 pp., full text extracted)
- CAUTION carried over: third-party mirror, undated — describes an earlier generation
  of the product (Primary/Comprehensive severity structure) than the current 1X/2X/3X
  presentation on S9. Treated as the design reference for the severity mechanics.

(uklib-critical_illness-s11)=

### S11. Zurich — "Key features of the Zurich Life Protection policy" (NP720500009, 02/2025)
- Publisher: Zurich Assurance Ltd
- Doc type: key features document
- URL: https://www.zurich.co.uk/-/media/documents/life-insurance/720500.pdf
- Fetched: YES (PDF, 16 pp., full text extracted)
- Caveat carried over: KFD only; Zurich's full policy terms, its survival period and
  the 2024 "three levels" proposition are unverified.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(uklib-critical_illness-r1)=

### R1. ABI — "Guide to Minimum Standards for Critical Illness Cover" (16 September 2022; April 2023 clarifications)
- Publisher: Association of British Insurers
- URL: https://www.abi.org.uk/globalassets/files/publications/public/protection/abi-guide-to-minimum-standards-for-critical-illness-cover-2023.pdf
- Fetched: NO (abi.org.uk sits behind a Cloudflare challenge that blocked all fetch
  routes tried). Retained as the load-bearing known reference; its content is
  triangulated from R2, R3 and insurer documents that visibly implement it (S1
  wordings; S11 states its KFD follows the ABI Statement of Best Practice for
  Critical Illness Cover, March 2023). Nothing is cited to R1 as verified.

(uklib-critical_illness-r2)=

### R2. Unum — "Definition changes for ABI minimum standards 2023"
- Publisher: Unum Limited
- URL: https://www.unum.co.uk/docs/Definition-changes-critical-illness-cover.pdf
- Fetched: YES (PDF, 3 pp., full text extracted)

(uklib-critical_illness-r3)=

### R3. SCOR — "Revision of the Minimum Standards for Critical Illness Review 2022"
- Publisher: SCOR (UK)
- URL: https://www.scor.com/en/article/news-uk/revision-minimum-standards-critical-illness-review-2022
- Fetched: YES (HTML)

(uklib-critical_illness-r4)=

### R4. FSMA 2000 (Regulated Activities) Order 2001, Schedule 1 (SI 2001/544)
- Publisher: legislation.gov.uk
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- Fetched: YES

(uklib-critical_illness-r5)=

### R5. FCA Handbook, ICOBS 1.1 (general application rule)
- Publisher: FCA (handbook.fca.org.uk)
- URL: https://www.handbook.fca.org.uk/handbook/ICOBS/1/1.html
- Fetched: YES (via browser; page as of 03/08/2026)

(uklib-critical_illness-r6)=

### R6. FCA — Consumer Duty firms page
- Publisher: FCA
- URL: https://www.fca.org.uk/firms/consumer-duty
- Fetched: YES (HTML; landing page only)

(uklib-critical_illness-r7)=

### R7. PRA Rulebook — Technical Provisions Part (Solvency UK)
- Publisher: PRA (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Fetched: YES (via browser; Rulebook "in the present" on 03/08/2026)

(uklib-critical_illness-r8)=

### R8. IFoA/CMI — "Critical illness investigation" page
- Publisher: Institute and Faculty of Actuaries — Continuous Mortality Investigation
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/critical-illness-investigation
- Fetched: YES (HTML)

(uklib-critical_illness-r9)=

### R9. CMI Working Paper 167 — "Accelerated critical illness experience by cause of claim, 2017–2020"
- Publisher: IFoA/CMI
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-working-papers/assurances/cmi-working-paper-167
- Fetched: YES (HTML)
- Note carried over: WP167 and chart data are publicly downloadable; full CMI
  tables/datasets are generally restricted to authorised users [unverified — access
  limits not stated on the fetched pages].

(uklib-critical_illness-r10)=

### R10. FRC — TAS 100 (General Actuarial Standards) v2.0
- Publisher: Financial Reporting Council
- URL: https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- Fetched: YES (HTML)

Dropped (in the research file but not cited in these documents): R11 (Bank of England
Solvency II implementation / Solvency UK page — 403 to all fetch routes tried; the
reformed rule state is evidenced directly from the Rulebook text in R7 instead).

---

## Cross-product regulatory references [REG-R#]

These are cited with the [REG-R#] prefix to avoid collision with the product research
file's own R-numbering. Full annotated entries (titles, publishers, URLs, retrieval
markers, access date 2026-08-03) live in `_research/regulatory-actuarial.md`
(provenance); the shared reference library is
`references/regulatory-and-actuarial-references.md` (same R-numbering, R1–R38
frozen). Entries cited by the two documents in this directory:

| Tag | Short title | Retrieval status (per that file) |
|---|---|---|
| REG-R1 | PRA Rulebook — Technical Provisions Part | fetched (browser) |
| REG-R4 | Insurance and Reinsurance Undertakings (Prudential Requirements) (Risk Margin) Regulations 2023 (SI 2023/1346) | fetched |
| REG-R11 | FCA Handbook ICOBS (ICOBS 1.1 read) | fetched (browser) |
| REG-R12 | FCA Handbook PRIN 2A — The Consumer Duty | fetched (browser) |
| REG-R14 | FSMA 2000 (Regulated Activities) Order 2001, Sch. 1 Part II | fetched |
| REG-R17 | Finance Act 2012, Part 2 (BLAGAB / protection trade basis) | fetched |
| REG-R20 | Consumer Insurance (Disclosure and Representations) Act 2012 | fetched (contents) |
| REG-R22 | CMI main page (role and Authorised-User access model) | fetched |
| REG-R26 | CMI "16" Series term assurance mortality and accelerated CI tables (IFoA blog announcement) | fetched |
| REG-R30 | CMI Mortality Projections Model CMI_2025 (announcement, WP211) | fetched |
| REG-R32 | ONS National life tables (UK series) | fetched |
| REG-R33 | FRC TAS 100 v2.0 (same standard as [R10] above) | fetched (FRC page) |
| REG-R34 | FRC TAS 200: Insurance, v2.0 | fetched (FRC page) |
| REG-R38 | UK Endorsement Board — IFRS 17 (UK adoption) | fetched |

---

## Provenance note

Extraction details live in `_research/critical-illness.md`: that file records which
facts came from which source, including the [unverified] flags, the failed fetch of
the ABI Guide (R1), the Vitality access limitations and the S10 mirror caution, the
fetch-tool-summary caveat on S2, the L&G retail-vs-intermediary variant split
(S1 vs S3), and the gaps (no public CI premium rate cards; AC04/16-Series table values
not obtained; Royal London underwriting limits; Zurich full terms). The cross-product
bibliography `_research/regulatory-actuarial.md` plays the same role for [REG-R#]
tags. Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md`
are introduced at drafting and are not attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #uklib-critical_illness-r10
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
