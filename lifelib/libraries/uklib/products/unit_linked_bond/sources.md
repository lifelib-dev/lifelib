# Sources

Source ids, titles, publishers, URLs, access dates, and retrieval markers are carried
over verbatim from `_research/unit-linked-bond.md` (the citation ground truth for
[S#]/[R#] tags). Ids are never renumbered. Sources from the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted (dropped here: S6, S8).
No new sources were fetched at drafting; nothing is marked "added at drafting".

Access date: 2026-08-03. (The research file's global access-date field was originally
recorded as "undefined" and has since been corrected; its retrieval notes date the session
to 03/08/2026 — see the [R5] entry, "viewed as at 03/08/2026". The drafting date of the two
documents in this directory is 2026-08-03.)
Cross-product [REG-R#] entries carry their own access date, 2026-08-03, per
`_research/regulatory-actuarial.md`.

---

## Primary product sources [S#]

(uklib-unit_linked_bond-s1)=

### S1. Prudential (M&G plc) — "Key Features of the Prudential Investment Plan"
- Publisher: The Prudential Assurance Company Limited ("Pru, part of M&G plc"),
  reg. no. 15454, FCA ref 139793
- Doc type: Key Features Document (KFD). Doc code PIPK10011 10/2025_WEB
- URL: https://www.mandg.com/dam/pru/shared/documents/en/pipk10011.pdf
- Retrieved: YES (full PDF read, 16 pp)
- Role in this library: implementation anchor (with S2) — currently marketed
  single-premium onshore investment bond.

(uklib-unit_linked_bond-s2)=

### S2. Prudential (M&G plc) — "Policy Provisions — Prudential Investment Plan"
- Publisher: The Prudential Assurance Company Limited
- Doc type: Policy conditions (full contract terms). Doc code INVM11630 11/2025_WEB
- URL: https://www.mandg.com/dam/pru/shared/documents/en/invm11630.pdf
- Retrieved: YES (full PDF read, 40 pp — definitions, unit pricing, charges,
  withdrawals, death benefit, PruFund smoothing, adviser charging, guarantee
  mechanics)
- Role in this library: implementation anchor (with S1) for unit pricing, charge,
  withdrawal, adviser-charging, death-benefit and GMDB mechanics.

(uklib-unit_linked_bond-s3)=

### S3. Aviva — "Investment and Trustee Bond Plan Booklet — The details of your Investment Bond"
- Publisher: Aviva Life & Pensions UK Limited, reg. no. 3253947, FCA firm ref 185896
- Doc type: Policy conditions / plan booklet (full plan terms; covers Investment Bond
  and Trustee Bond). Doc code AIBPO HL59005 05/2023
- URL: https://static.aviva.io/content/dam/document-library/adviser/ecm/hl59005c.pdf
- Retrieved: YES (full PDF read, 15 pp). Note: static.aviva.io returns HTTP 403 to
  plain fetchers; retrieved with a browser user-agent.
- Role in this library: legacy-charge layer (bid-offer "One-Off Charge", Early
  Cash-in Charges, Establishment Charge), with-profits/MVR variation, 100-segment
  structure, Accidental Death Benefit.

(uklib-unit_linked_bond-s4)=

### S4. Aviva — "Onshore Bond Key Features" (Aviva Wealth platform)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: Key Features Document. Doc code LF20017 06/2026 (companion T&Cs are
  LF30029)
- URL: https://static.aviva.io/content/dam/document-library/adviser/general/lf20017c.pdf
- Retrieved: YES (full PDF read, 8 pp)
- Role in this library: current adviser-platform onshore bond — modern "clean"
  open-architecture design; explicit charge in respect of tax; 101% death benefit
  variant.

(uklib-unit_linked_bond-s5)=

### S5. Quilter — "Key Features of the Collective Investment Bond"
- Publisher: Quilter Life & Pensions Limited, reg. no. 04163431, PRA/FCA ref 207977
- Doc type: Key Features Document. Doc code QIP 18193/205/14009, approved May 2026
- URL: https://www.quilter.com/siteassets/documents/platform/kfd/18193_cib_kfd.pdf
- Retrieved: YES (full PDF read, 16 pp)
- Role in this library: current platform onshore bond (open architecture, ~3,000
  funds); explicit life-fund tax pass-through; Capital Protected Death Benefit
  rider; chargeable-event statements.

(uklib-unit_linked_bond-s7)=

### S7. Canada Life — "Canada Life announces closure of onshore bond and personal pension to focus investment on offshore bonds"
- Publisher: Canada Life UK (canadalife.co.uk)
- Doc type: Other (news announcement; market-context evidence)
- URL: https://www.canadalife.co.uk/news/canada-life-announces-closure-of-onshore-bond-and-personal-pension-to-focus-investment-on-offshore-bonds/
- Retrieved: YES
- Role in this library: market-consolidation context (Select Account closed to new
  business 23 January 2024; existing customers unaffected; <1% of customer base).

Dropped (in the research file but not cited in these documents): S6 (Quilter CIB
Terms and Conditions — PDF downloaded but not parsed in the research session; no
facts citable), S8 (Aviva legacy Investment Bond KFD HL59015 — downloaded but not
read).

---

## Regulatory and actuarial references [R#] (product research file numbering)

(uklib-unit_linked_bond-r1)=

### R1. ITTOIA 2005, Part 4 Chapter 9 — "Gains from contracts for life insurance etc."
- Publisher: legislation.gov.uk (UK statute)
- URL: https://www.legislation.gov.uk/ukpga/2005/5/part/4/chapter/9
- Retrieved: YES (chapter structure and key sections: s461 ff. charge, s465–s467
  liable persons, s484 chargeable events, s491–s494 gain computation, s498/s500/s507
  part-surrender periodic calculations, s535–s537 top-slicing, s539 deficiency
  relief)
- Caveat carried over: top-slicing and deficiency-relief mechanics were not
  extracted beyond section references — [unverified] where used.

(uklib-unit_linked_bond-r2)=

### R2. HMRC Insurance Policyholder Taxation Manual IPTM3560
- Publisher: GOV.UK (HMRC internal manual)
- Title: "IPTM3560 — Calculating gains: part surrenders and part assignments:
  'periodic calculations' and 'excess events': calculation method"
- URL: https://www.gov.uk/hmrc-internal-manuals/insurance-policyholder-taxation-manual/iptm3560
- Retrieved: YES (allowable element = premium × y/20, y capped at 20 — the 5% p.a.
  cumulative tax-deferred allowance machinery)

(uklib-unit_linked_bond-r3)=

### R3. FCA Handbook COBS 21.3 — "Further rules for firms engaged in linked long-term insurance business"
- Publisher: FCA (handbook.fca.org.uk)
- URL: https://www.handbook.fca.org.uk/handbook/COBS/21/3.html
- Retrieved: YES (rendered via browser; the site is JavaScript-only) — permitted-links
  asset list, approved indices, economic-substance classification, conditional
  permitted links.

(uklib-unit_linked_bond-r4)=

### R4. FSMA 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1 Part II
- Publisher: legislation.gov.uk
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- Retrieved: YES (long-term insurance classes; Class III "Linked long-term"
  definition)

(uklib-unit_linked_bond-r5)=

### R5. PRA Rulebook (Solvency II firms) — Technical Provisions Part
- Publisher: Bank of England / PRA (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Retrieved: YES (page HTML downloaded and text-extracted; viewed as at 03/08/2026)
  — TP 2.1–2.5, TP 3.1–3.2 best estimate, TP 4A.1 reformed risk margin (CoC 4%,
  λ = 0.9, floor 0.25).

(uklib-unit_linked_bond-r6)=

### R6. HMRC Life Assurance Manual LAM01160 (I-E / BLAGAB)
- Publisher: GOV.UK (HMRC internal manual)
- Title: "LAM01160 — ... key concepts: simplified example of the I-E calculation"
- URL: https://www.gov.uk/hmrc-internal-manuals/life-assurance/lam01160
- Retrieved: YES (I-E base, policyholder rate = basic rate 20% in the example,
  minimum profits test, basic-rate credit rationale)

(uklib-unit_linked_bond-r7)=

### R7. FRC — TAS 100 "General Technical Actuarial Standards"
- Publisher: Financial Reporting Council (frc.org.uk)
- URL: https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- Retrieved: YES (v2.0, published 3 March 2023, effective 1 July 2023; Principle 5
  Models)

(uklib-unit_linked_bond-r8)=

### R8. IFoA — Continuous Mortality Investigation page
- Publisher: Institute and Faculty of Actuaries (actuaries.org.uk)
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation
- Retrieved: YES (CMI role and subscription/Authorised User access model; specific
  assured-lives table series names not stated on the fetched page — [unverified]
  where referenced)

(uklib-unit_linked_bond-r9)=

### R9. IFoA historical sessional papers on unit-linked reserving
- Publisher: Institute and Faculty of Actuaries (actuaries.org.uk document archive)
- Example URLs: https://www.actuaries.org.uk/documents/category-b-unit-linked-policies
  (A. F. Wilson, "Category B unit-linked policies");
  https://www.actuaries.org.uk/system/files/documents/pdf/0311-0367.pdf
- Retrieved: NO (fetched_ok = false; the archive PDFs are scanned images — text could
  not be extracted). Listed as known references for the unit vs non-unit ("sterling")
  reserve decomposition, which therefore stays tagged [unverified] wherever used in
  these documents.

---

## Cross-product regulatory references [REG-R#]

These are cited with the [REG-R#] prefix to avoid collision with the product research
file's own R-numbering. Full annotated entries (titles, publishers, URLs, retrieval
markers, access date 2026-08-03) live in `_research/regulatory-actuarial.md`; the
shared reference library is `references/regulatory-and-actuarial-references.md`
(same R-numbering, R1–R38 frozen). Entries cited by the two documents in this
directory:

| Tag | Short title | Retrieval status (per that file) |
|---|---|---|
| REG-R4 | Insurance and Reinsurance Undertakings (Prudential Requirements) (Risk Margin) Regulations 2023 (SI 2023/1346) — CoC 6%→4%, λ 0.9 / floor 0.25 | fetched |
| REG-R10 | FCA Handbook COBS 21.3 — permitted links (same rules as [R3] above) | fetched (browser) |
| REG-R12 | FCA Handbook PRIN 2A — the Consumer Duty | fetched (PRIN 2A.1 read; price-and-value outcome location [unverified]) |
| REG-R14 | FSMA 2000 (Regulated Activities) Order 2001, Sch. 1 Pt II (same instrument as [R4] above; Class VI capital redemption in the verified class list) | fetched |
| REG-R17 | Finance Act 2012, Part 2 — BLAGAB definition (s57) and I-E charge (s68) | fetched |
| REG-R24 | CMI "92" Series tables (AM92/AF92 family) — canonical teaching assured-lives tables | fetched |
| REG-R30 | CMI Mortality Projections Model CMI_2025 (WP211 announcement) — subscriber-restricted; "CMI_20xx with long-term rate p% [std]" convention | fetched |
| REG-R32 | ONS National life tables (UK series) — freely downloadable qx under OGL; population heavier than insured experience | fetched |
| REG-R33 | FRC TAS 100 v2.0 (same standard as [R7] above) | fetched (FRC page; PDF not read) |
| REG-R34 | FRC TAS 200: Insurance, v2.0 — published 20 September 2024, effective 1 January 2025 | fetched (FRC page; PDF not read) |
| REG-R38 | UK Endorsement Board — IFRS 17 (UK adoption 16 May 2022, effective 1 January 2023); VFA mechanics [unverified] per that file's narrative | fetched |

---

## Provenance note

Extraction details live in `_research/unit-linked-bond.md`: that file records
which facts came from which source, the [unverified] flags (including the unit vs
non-unit "sterling" reserve terminology [R9], the CMI assured-lives table names [R8],
and legacy allocation-rate/initial-unit mechanics), the not-parsed downloads (S6,
S8), the browser-user-agent workaround for static.aviva.io (S3), and the research
gaps (per-fund AMC rate cards, PruFund smoothing parameter values, Quilter
segment-level terms). The cross-product bibliography
`_research/regulatory-actuarial.md` plays the same role for [REG-R#] tags.
Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md` are
introduced at drafting and are not attributable to any source.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #uklib-unit_linked_bond-r3
[R4]: #uklib-unit_linked_bond-r4
[R5]: #uklib-unit_linked_bond-r5
[R7]: #uklib-unit_linked_bond-r7
[R8]: #uklib-unit_linked_bond-r8
[R9]: #uklib-unit_linked_bond-r9
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
