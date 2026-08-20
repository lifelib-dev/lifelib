# Sources

Source ids, titles, publishers, URLs, access dates, and retrieval markers are carried over
verbatim from `_research/whole-of-life.md` (the citation ground truth for [S#]/[R#] tags).
Ids are never renumbered. Sources from the research file that are not cited in
`product-spec.md` or `technical-notes.md` are omitted (dropped here: R9 — CMI Limited
website, fetched_ok: no; R10 — FCA MS24/1 Terms of Reference, not fetched; CMI-restriction
and ToR facts are cited instead from the fetched cross-product entries [REG-R22] and [R2]).
No new sources were fetched at drafting; nothing is marked "added at drafting".

Access date: 2026-08-03. (The research file's access-date field, originally recorded as
"undefined", has been corrected to 2026-08-03; see the Provenance note.) [REG-R#] sources
were accessed 2026-08-03 per `_research/regulatory-actuarial.md`.

---

## Primary product sources [S#]

(uklib-whole_of_life-s1)=

### S1. SunLife, "Guaranteed Over 50 Plan — Terms and Conditions including the Policy Summary" (PDF)
- Publisher: SunLife (distributor SunLife Limited); insurer Phoenix Life Limited trading as SunLife
- Doc type: policy conditions + policy summary (combined booklet), doc code S-G050T12.25.V3 (Nov 2025 version)
- URL: https://www.sunlife.co.uk/siteassets/documents/2025-11-guaranteed-over-50-plan-terms-and-conditions.pdf
- Fetched: YES (full 8-page text extracted)

(uklib-whole_of_life-s2)=

### S2. SunLife, "Over 50s Life Insurance" product page
- Publisher: SunLife
- Doc type: product page (marketing + parameters)
- URL: https://www.sunlife.co.uk/over-50-life-insurance/
- Fetched: YES

(uklib-whole_of_life-s3)=

### S3. SunLife, "Funeral Benefit Option" page
- Publisher: SunLife
- Doc type: product page (option description)
- URL: https://www.sunlife.co.uk/over-50-life-insurance/funeral-benefit-option/
- Fetched: YES

(uklib-whole_of_life-s4)=

### S4. Legal & General, "Over 50's Life Insurance — Policy Terms and Conditions" (PDF)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy conditions, doc code QGI11740 06/26
- URL: https://www.legalandgeneral.com/landg-assets/personal/life-cover/_resources/over-50s/documents/terms-and-conditions.pdf
- Fetched: YES (full 6-page text extracted)

(uklib-whole_of_life-s5)=

### S5. Legal & General, "Over 50s Fixed Life Insurance — Policy Summary" (PDF)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy summary (IPID-style), doc code QGI12836 11/2025
- URL: https://www.legalandgeneral.com/landg-assets/personal/life-cover/_resources/over-50s/documents/fixed-policy-summary.pdf
- Fetched: YES (full 4-page text extracted)

(uklib-whole_of_life-s6)=

### S6. Legal & General, "Over 50s Life Insurance" product page
- Publisher: Legal & General
- Doc type: product page
- URL: https://www.legalandgeneral.com/insurance/over-50-life-insurance/
- Fetched: YES

(uklib-whole_of_life-s7)=

### S7. Aviva, "Guaranteed Lifelong Protection — Plan Conditions" (PDF)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: policy conditions, doc code LD01052 11/2016 (version currently posted under aviva.co.uk over-50s path)
- URL: https://static.aviva.io/content/dam/aviva-public/gb/pdfs/personal/insurance/life/over-50s/insurance-life-over-50s-guaranteed-lifelong-protection-plan-conditions.pdf
- Fetched: YES (via direct download; WebFetch returned 403; full 6-page text extracted)
- Vintage caveat carried over: the fetched plan conditions and key features (S8) are dated
  11/2016 — the versions Aviva currently publishes at the product URLs; a newer edition may
  exist behind the quote journey.

(uklib-whole_of_life-s8)=

### S8. Aviva, "Key Features of Guaranteed Lifelong Protection" (PDF)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: key features document, doc code LD06001 11/2016
- URL: https://static.aviva.io/content/dam/aviva-public/gb/pdfs/personal/insurance/life/over-50s/insurance-life-over-50s-guaranteed-lifelong-protection-key-features.pdf
- Fetched: YES (via direct download; full 5-page text extracted)

(uklib-whole_of_life-s9)=

### S9. Royal London, "Terms & Conditions — Over 50 Life Insurance" (PDF)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: policy conditions, doc code D2COFTC
- URL: https://www.royallondon.com/siteassets/site-docs/insurance/life-insurance/over-50s-direct-terms-conditions.pdf
- Fetched: YES (full 9-page text extracted)

(uklib-whole_of_life-s10)=

### S10. Zurich, "Zurich Whole of Life — Terms and conditions" (PDF)
- Publisher: Zurich Assurance Ltd
- Doc type: policy conditions, doc code PW720491009 (08/25)
- URL: https://www.zurichintermediary.co.uk/-/media/zurich-intermediary/documents/terms-and-conditions/720491.pdf
- Fetched: YES (via direct download; full 20-page text extracted)
- Role in this library: implementation anchor for the underwritten cell (RefWOL-UW) —
  benefit/terminal illness wording, suicide clause, escalation and milestone-benefit
  mechanics, waiver of premium, lapse terms.

(uklib-whole_of_life-s11)=

### S11. Zurich, "Zurich Whole of Life — Key features" (PDF)
- Publisher: Zurich Assurance Ltd
- Doc type: key features document, doc code PW720505007 (02/25)
- URL: https://www.zurichintermediary.co.uk/-/media/zurich-intermediary/documents/key-features/720505.pdf
- Fetched: YES (via direct download; full 12-page text extracted)

(uklib-whole_of_life-s12)=

### S12. Zurich for advisers, "Whole of Life" product page
- Publisher: Zurich (zurichintermediary.co.uk)
- Doc type: adviser product page with document links
- URL: https://www.zurichintermediary.co.uk/whole-of-life
- Fetched: YES

(uklib-whole_of_life-s13)=

### S13. Royal London for advisers, "Life Cover — Product details" page (Personal Menu Plan)
- Publisher: Royal London (adviser.royallondon.com)
- Doc type: adviser product specification page
- URL: https://adviser.royallondon.com/protection/personal-protection/life-or-critical-illness-cover/detail/ (life cover detail page: https://adviser.royallondon.com/protection/personal-protection/life-cover/detail/)
- Fetched: YES (life cover detail page)

(uklib-whole_of_life-s14)=

### S14. Royal London, "Personal Menu Plan — Life Cover — Plan details" (PDF, December 2024)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: policy conditions booklet (menu plan life cover, incl. whole of life), doc code PCP8P10004
- URL: https://adviser.royallondon.com/globalassets/docs/protection/pcp8p10004-plan-details-for-the-personal-menu-plan-life-cover.pdf
- Fetched: YES (44 pages downloaded; introductory sections and structure read; clause-level
  extraction not performed — WoL parameters cited from S13 instead; carried caveat)

(uklib-whole_of_life-s15)=

### S15. ReAssure, "Keeping your reviewable whole-of-life policy on track" (PDF factsheet)
- Publisher: ReAssure Ltd (closed-book consolidator; FRN 110495)
- Doc type: customer factsheet on legacy unit-linked reviewable whole of life
- URL: https://www.reassure.co.uk/uploads/2015/12/Keeping-your-whole-of-life-policy-on-track.pdf
- Fetched: YES (full 4-page text extracted)
- Role in this library: sole source for the legacy unit-linked reviewable variation
  (maximum vs standard/balanced cover, review cycle, unit-fund surrender value).

(uklib-whole_of_life-s16)=

### S16. Vitality, "Whole of life insurance" product page
- Publisher: Vitality (VitalityLife)
- Doc type: product page
- URL: https://www.vitality.co.uk/life-insurance/life-cover/whole-life/
- Fetched: YES (via direct download; WebFetch returned 403)
- Caveat carried over: detailed plan provisions (ages, optimiser/premium-step mechanics)
  not extracted; market-role facts only.

---

## Regulatory and actuarial references [R#] (product research file numbering)

(uklib-whole_of_life-r1)=

### R1. FCA, "MS24/1: Pure Protection Market Study" (study landing page)
- Publisher: Financial Conduct Authority
- URL: https://www.fca.org.uk/publications/market-studies/ms24-1-1-market-distribution-pure-protection
- Fetched: YES

(uklib-whole_of_life-r2)=

### R2. FCA, "MS24/1 Annex 2: Value of pure protection products" (PDF)
- Publisher: Financial Conduct Authority
- URL: https://www.fca.org.uk/publication/market-studies/ms24-1-annex-2.pdf
- Fetched: YES (full text extracted; Chapter 3 is "Guaranteed acceptance over 50s")
- Role in this library: primary regulatory source for the over-50s cell — tipping-point
  example (£30/month, £5,000, 13 years 11 months), premium age caps, per-£1,000 price
  comparison (£71.73 vs £8.10), lapse-supported economics, Consumer Duty fair value framing.

(uklib-whole_of_life-r3)=

### R3. PRA Rulebook, "Technical Provisions" Part (Solvency UK)
- Publisher: Prudential Regulation Authority (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Fetched: YES (via direct download; WebFetch returned 403; rule text extracted; site viewed
  "in the present on 03/08/2026")

(uklib-whole_of_life-r4)=

### R4. PRA, "PS15/24 – Review of Solvency II: Restatement of assimilated law"
- Publisher: Bank of England / PRA
- URL: https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/review-of-solvency-ii-restatement-of-assimilated-law-policy-statement
- Fetched: YES (via direct download; WebFetch returned 403)

(uklib-whole_of_life-r5)=

### R5. Financial Services and Markets Act 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1
- Publisher: legislation.gov.uk
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- Fetched: YES

(uklib-whole_of_life-r6)=

### R6. CMI / IFoA, "'00' series tables" page
- Publisher: Institute and Faculty of Actuaries (Continuous Mortality Investigation)
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/00-series-tables
- Fetched: YES

(uklib-whole_of_life-r7)=

### R7. IFoA blog, "CMI: New '16' Series term assurance mortality and accelerated critical illness tables"
- Publisher: Institute and Faculty of Actuaries (blog.actuaries.org.uk)
- URL: https://blog.actuaries.org.uk/cmi-new-16-series-term-assurance-mortality-and-accelerated-critical-illness-tables/
- Fetched: YES

(uklib-whole_of_life-r8)=

### R8. FRC, "General Technical Actuarial Standards (TAS 100)" page
- Publisher: Financial Reporting Council
- URL: https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- Fetched: YES

Dropped (in the research file but not cited in these documents): R9 (CMI Limited website —
fetched_ok: NO, connection reset; the CMI access-model facts are cited from [REG-R22] and
[R7] instead); R10 (FCA MS24/1 Terms of Reference PDF — not fetched; the GO50 value-concern
premise is cited from [R2] instead).

---

## Cross-product regulatory references [REG-R#]

These are cited with the [REG-R#] prefix to avoid collision with the product research file's
own R-numbering. Full annotated entries (titles, publishers, URLs, retrieval markers, access
date 2026-08-03) live in `_research/regulatory-actuarial.md` (the research provenance);
the shared reference library is `references/regulatory-and-actuarial-references.md` (same
R-numbering, R1–R38 frozen). Entries cited by the two documents in this directory:

| Tag | Short title | Retrieval status (per that file) |
|---|---|---|
| REG-R1 | PRA Rulebook — Technical Provisions Part (best-estimate definition, rule 3.1; same document as [R3] above, different recorded facts) | fetched (browser) |
| REG-R3 | PRA Rulebook — Transitional Measure on Technical Provisions Part (TMTP) | fetched (browser, as-at 31/12/2024 view) |
| REG-R4 | Insurance and Reinsurance Undertakings (Prudential Requirements) (Risk Margin) Regulations 2023 (SI 2023/1346) — 4% CoC, lambda 0.9 | fetched |
| REG-R11 | FCA Handbook ICOBS — Insurance: Conduct of Business sourcebook (ICOBS 1.1) | fetched (browser) |
| REG-R12 | FCA Handbook PRIN 2A — The Consumer Duty | fetched (browser) |
| REG-R15 | ITTOIA 2005, Part 4 Chapter 9 — Gains from contracts for life insurance (chargeable events) | fetched |
| REG-R16 | HMRC Insurance Policyholder Taxation Manual (IPTM) | fetched (landing/contents) |
| REG-R17 | Finance Act 2012, Part 2 — long-term business taxation (BLAGAB / I-E; protection business excluded) | fetched |
| REG-R20 | Consumer Insurance (Disclosure and Representations) Act 2012 | fetched (contents) |
| REG-R22 | CMI main page — role and Authorised-User access model | fetched |
| REG-R24 | CMI "92" Series tables (AM92/AF92 family) | fetched |
| REG-R30 | CMI Mortality Projections Model CMI_2025 (announcement, WP211) | fetched |
| REG-R32 | ONS National life tables (UK series, 2021–2023) | fetched |
| REG-R34 | FRC TAS 200: Insurance, v2.0 | fetched (FRC page; PDF not read) |
| REG-R38 | UK Endorsement Board — IFRS 17 Insurance Contracts (UK adoption) | fetched |

---

## Provenance note

Extraction details live in `_research/whole-of-life.md`: that file records which facts
came from which source, including the [unverified] flags (L&G/Dignity funeral option,
ICOBS-vs-COBS classification at glossary level, market-share claims, qualifying-policy tax
rules), the failed fetches (R9 — connection reset; R10 — not attempted), the Aviva document
vintage caveat (11/2016 editions), the S14 clause-level-extraction caveat, and the note that
no public insurer disclosure of a guaranteed-acceptance pricing mortality basis was found.
The research file's access date, originally recorded as "undefined", has been corrected to
2026-08-03; its internal evidence (document codes up to 11/2025–06/26; R3 viewed "in the
present on 03/08/2026") is consistent with that date.
The cross-product bibliography `_research/regulatory-actuarial.md` (accessed 2026-08-03)
plays the same role for [REG-R#] tags. Standardizations marked **[std]** in `product-spec.md`
and `technical-notes.md` are introduced at drafting and are not attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uklib-whole_of_life-r2
[R3]: #uklib-whole_of_life-r3
[R7]: #uklib-whole_of_life-r7
[REG-R22]: #uklib-reg-r22
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
