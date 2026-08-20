# With-Profits Business (conventional and unitised) — research notes (UK)

Research for a reference liability cash-flow projection model of UK with-profits business
(conventional/traditional, unitised/accumulating, and modern smoothed-fund variants).
All facts are tagged [S#] (primary product/firm document) or [R#] (regulatory/actuarial
reference) pointing at documents actually fetched and read. Facts from general knowledge
that could not be verified against a retrieved document are tagged [unverified].
Access date for all citations: 2026-08-03.

---

## Primary sources

### S1 — Prudential Assurance Company: main PPFM
- Publisher: The Prudential Assurance Company Limited (PAC), part of M&G plc
- Title: "Principles & Practices of Financial Management (Applicable to UK with-profits policies issued by or reinsured into The Prudential Assurance Company Limited)", Version 2.3, April 2026 (44 pp)
- Doc type: PPFM
- URL: https://www.mandg.com/assets/shared/documents/en/wpgb0014.pdf
- Access date: 2026-08-03. Retrieved: YES (PDF fetched; text extracted with pypdf)
- Key facts extracted:
  - Covers all UK with-profits policies issued by or reinsured into PAC; PAC's long-term fund contains the With-Profits Sub-Fund (WPSF) and the Defined Charge Participating Sub-Fund (DCPSF); the WPSF contains the PAC Inherited Estate ("the Estate").
  - Profit sharing: WPSF policies are "90:10" — at least 90% of divisible profit to policyholders, balance to shareholder; some policies are "100:0" (100% to policyholders, 0% shareholder). Glossary defines both bases.
  - Product taxonomy (section D1–D3): conventional contracts (basic sum assured to which bonuses are added; sum assured is the minimum maturity amount before bonuses); conventional with-profits deferred annuities (basic annuity p.a. plus bonuses); accumulating with-profits = unitised with-profits (units whose value rises with declared regular bonuses, final bonus at encashment) and cash accumulation (bonuses added to contributions); with-profits annuities (With-Profits Annuity, Income Choice Annuity); PruFund (unit price grows at Expected Growth Rate, subject to adjustment); credit matched with-profits (CMWP: Prudential Guaranteed Income Plan, With-Profits Bulk Purchase Annuity — guaranteed benefit at outset, small discretionary annual bonus, fixed-income backing).
  - Two bonus types: regular (annual/reversionary) bonuses which increase guaranteed benefits, and final (terminal) bonus payable at claim. A regular bonus becomes a contractual right only once added.
  - Bonus philosophy: aim to keep a substantial proportion of pay-out values in non-guaranteed form (final bonus); pay-out values set by reference to earnings of underlying investments except where guaranteed minimums bite.
  - Target range: business managed with the aim that pay-out values for at least 90% of with-profits policies fall within 80%–120% of asset shares (1.3.10.1); ad hoc bonus declaration possible if markets move payouts outside.
  - Smoothing: same approach for accumulating and conventional; in normal circumstances most pay-out values not expected to change by more than 10% up or down year-on-year (1.3.4.2); Board may vary standard bonus smoothing limits.
  - Regular bonus practice: target rates determined by projection; gradual changes, "not expected to exceed 1% p.a."; the company retains discretion whether to declare at all and there is no limit on the amount of change if needed to protect policyholders; declared for the forthcoming bonus year; interim bonus rates apply between declaration and claim for some products; for WPSF cash accumulation products the regular bonus rate is guaranteed until the next revision date.
  - Final bonus: normally declared yearly; scales vary by product type and duration/entry year; determined by reference to asset shares of sample policies subject to smoothing; in general the same final bonus scale applies to maturity, death and surrender.
  - Surrender values — accumulating WP: pay-out value less any discontinuance charge; MVR may be applied where asset share is below the value being withdrawn and the payment falls outside any MVR-free guarantee period; MVRs vary with asset values; practice is NOT to apply MVRs that reduce surrender values below a fair reflection of the underlying asset value; on partial withdrawal, asset share is reduced pro rata to the pre-MVR policy value.
  - Surrender values — conventional WP: formula-based (parameters set to broadly target asset shares over the long term), based on sum assured, regular bonus and final bonus, adjusted for unpaid premiums; bases normally reviewed annually; deferred annuity cash claims reflect the current cost of the deferred annuity.
  - Asset share methodology (1.3.8): retrospective accumulation per policy type of premiums, investment return (incl. unrealised gains) and past excess-surplus distributions of the Estate, minus tax, charges for guarantees and smoothing, mortality/morbidity charges, shareholder profit transfers, expenses, explicit charges/commission, and payments out. Sample asset shares projected to mid bonus-year for setting final bonus rates. CMWP asset shares use a prospective method (projected guaranteed benefits and estimated future bonuses discounted back). Non-PruFund asset shares are not credited with any investment return earned on the Estate.
  - Guarantee/smoothing charges: monitored via bonus smoothing accounts held within the Estate (intended neutral over time — policyholders in each product group should neither gain nor lose from smoothing in the long run); charge may sit in the AMC (PruFund), in the customer price (CMWP), or in asset share calculation (traditional). For most traditional WP policies the total lifetime deduction is currently capped at 2% of asset shares (built up gradually); for AVCs with applications on/after 15 March 2019 the guarantee charge cap is 4% of asset shares; for With-Profits Annuity/Income Choice Annuity an annual charge (varying by entry year) is deducted from credited investment return; former SALAS policies bear no separate guarantee/smoothing charge (allowed for in 2021 merger terms).
  - Expense charges to asset shares: business sold since 1997 bears the policy-specific charges used at point of sale; an expense tariff was introduced in 2023 for business without one; the cap for many pension contracts is 1% p.a. since April 2001 (not guaranteed); excess expenses over fixed/capped charges fall to the Estate. Mortality charge = mortality rate × (death benefit − current policy value); differences vs actual claims accrue to the Estate.
  - Miscellaneous surplus: profits/losses from specified non-profit business, staff pension scheme surplus/deficits, unclaimed policies etc. allocated annually to asset shares; former SALAS policies receive a fixed 0.25% p.a. asset-share allocation per the 1997 acquisition agreement.
  - With-profits annuity smoothing: non-guaranteed income should not fall by more than the Required Smoothed Return (ICA) or Anticipated Bonus Rate (WPA) chosen at outset, should not rise by more than 12% a year (ICA) or 11% (WPA), and should not fall on the first policy anniversary.
  - Industrial Branch: some IB payouts set by reference to Ordinary Branch payout scales; for IB business issued before July 1988, payouts use IB asset shares if higher.
  - Estate: the major part of WPSF working capital; supports investment freedom, smoothing and guarantees; policyholders should have no expectation of estate distribution other than through normal smoothing/guarantee support; excess surplus may be distributed (for PruFund via unit price enhancements).
  - ELAS appendix (with-profits annuities transferred from Equitable Life Assurance Society to PAC): smoothing cap currently 11% on income rises; income should not fall by more than the combined selected ABR and any GIR in a year; asset shares built retrospectively from the initial asset share transferred, less unsmoothed annuity payments, with a longevity risk mechanism (mortality losses charged to asset shares limited to 0.5% of asset shares p.a.; profits credited limited between 0.5% and 1.04% p.a.; remainder to the Estate); charges deducted from gross credited return: max 1% p.a. for expenses (credited to the Non-Profit Sub-Fund which bears expenses) and max 0.5% p.a. for the expected cost of guarantees (credited to the Estate, hard cap 0.5%).

### S2 — Prudential Assurance Company: PruFund PPFM
- Publisher: The Prudential Assurance Company Limited (M&G plc)
- Title: "Principles & Practices of Financial Management (Applicable to PruFund UK with-profits policies issued by or reinsured into The Prudential Assurance Company Limited)", Version 2.3, April 2026 (32 pp)
- Doc type: PPFM
- URL: https://www.mandg.com/dam/pru/shared/documents/en/wpgb0010.pdf
- Access date: 2026-08-03. Retrieved: YES (PDF fetched; text extracted with pypdf)
- Key facts extracted:
  - Covers all with-profits policies investing in PruFund issued in the UK by M&G plc companies (PAC and Prudential International Assurance plc).
  - Pay-out value = units held × unit price, less policy-condition deductions, at the transaction date.
  - Unit price (before charges) changes daily at the relevant Expected Growth Rate (EGR); EGRs are annualised rates set quarterly by the Board with regard to expected long-term returns on the fund's assets.
  - Smoothing mechanism: (i) on or between investment dates, if the net asset value (NAV) per unit AND the 5-working-day rolling average NAV per unit are outside the daily smoothing limit, the unit price is adjusted to within a defined "gap after adjustment"; (ii) on an investment date, if NAV per unit is above/below the monthly/quarterly smoothing limit, the unit price is repeatedly moved by half the difference until the difference is within the limit. Each PruFund has its own daily smoothing limit, monthly/quarterly smoothing limit and gap after adjustment, stated in policy conditions.
  - Unit cancellations for switches/transfers/withdrawals may be delayed up to 28 days; the price on the final day of the delay applies.
  - Unit Price Reset: company may reset unit price to equal NAV per unit to protect the fund; smoothing may also be suspended for consecutive days (price then tracks NAV until suspension lifted).
  - Unit price enhancements may be applied to eligible PruFund funds when the Board determines excess surplus exists in the WPSF.
  - NAV (equivalent to asset share) = accumulation of premiums, investment return (incl. unrealised), past excess-surplus distributions, less tax (via net investment return for life business; pensions business gross of UK tax), guarantee and smoothing charges, mortality/morbidity where relevant, shareholder transfers where relevant, expenses, charges/commission, payments out.
  - Guarantee/smoothing charge typically included in the AMC for PruFund business; smoothing profits/losses tracked in bonus smoothing accounts within the Estate; separate accounts per product group and smoothing mechanism; intended neutral over time.
  - DCPSF: contains accumulated investment content of premiums less explicit charges for Defined Charge Participating business; policyholders bear only explicit policy charges (incl. AMC); shareholder bears expense/charge differences.

### S3 — Prudential PPFM Summary of changes
- Publisher: The Prudential Assurance Company Limited (M&G plc)
- Title: "Principles and Practices of Financial Management — Summary of changes" (8 pp; covers versions to v2.3 April 2026)
- Doc type: PPFM change log
- URL: https://www.mandg.com/dam/pru/shared/documents/en/wpgg10116.pdf
- Access date: 2026-08-03. Retrieved: YES
- Key facts: main PPFM first published 2004; v2.3 (April 2026) added description of new Credit Matched With-Profits business, clarified risk-sharing between policyholders and shareholder, smoothing/guarantee charge operation, and OB/IB bonus process.

### S4 — Phoenix Life Limited PPFM
- Publisher: Phoenix Life Limited (Phoenix Group)
- Title: "Phoenix Life Limited — Principles and Practices of Financial Management", July 2026 (443 pp)
- Doc type: PPFM
- URL: https://library.phoenixlife.co.uk/ppfm-pll.pdf
- Access date: 2026-08-03. Retrieved: YES (PDF fetched; text extracted with pypdf)
- Key facts extracted:
  - PLL's long-term fund is internally segregated into 18 funds, including: 90% With-Profits Fund, 100% With-Profits Fund, Alba WPF, Britannic WPF, Britannic Industrial Branch Fund, Phoenix WPF, Scottish Mutual WPF, SPI WPF, SAL WPF, Pearl WPF, SERP Fund, London Life WPF, National Provident Life WPF, Heritage WPF, UK Smoothed Managed With-Profits Fund, and others. Policies originally issued by Standard Life Assurance Limited have separate PPFM documents.
  - Key concepts (section 4): conventional (traditional) life policy benefit at maturity/death = guaranteed sum assured + annual bonuses added at annual declarations (increasing guaranteed benefit) + any final bonus; some endowments carry an additional death-only sum assured or guaranteed minimum death benefit not eligible for bonuses. Pension policies: guaranteed basic annuity or cash for annuity purchase + annual + final bonus; death benefit generally non-participating. If premiums cease: surrender value/transfer value, or paid-up with reduced benefits (future bonuses may or may not accrue), else lapse without value.
  - Unitised WP: proportion of each premium less charges buys with-profits units; annual bonus delivered either by unit price increasing at the daily equivalent of the current annual bonus rate, or by allocation of bonus units. Claim benefit = value of units + bonus units + any final bonus. Guaranteed minimum death benefit (where present) financed by monthly unit cancellation on the sum at risk. On surrender, unit and bonus-unit values may be reduced by an MVR; MVR calculated by reference to underlying fair value, in some cases allowing for smoothing. Single-premium bonds: whole-of-life; some have guarantee dates at which encashment is MVR-free.
  - Asset shares: calculated for specimen policies/groups; premiums accumulated at earned investment returns less expenses, mortality/morbidity costs, cost of guarantees, cost of capital, shareholder distributions and tax; used to guide payouts and bonus declarations; asset shares can fall and can be above or below guaranteed benefits.
  - Target payout ratios (typical across funds): long-term target maturity payout ratio 100% of asset share; target range 80%–120% of asset share before the effects of smoothing (stated for e.g. SAL fund 8.7.1, Britannic 9.7.11, Scottish Mutual 12.7.12); surrenders also targeted at 100% with an 80%–120% range in most funds; some Bradford WPF policies target 100%.
  - 90% WPF: parameters of surrender bases reviewed so the majority of specimen-policy surrender values fall within 80%–120% of asset share before smoothing; values above range possible near maturity when guarantees exceed asset share.
  - MVR practice (90% WPF and generally): for unitised policies an MVR applies where the determined proportion of asset share (after any guarantee charge) falls short of the value of units; the MVR will not exceed the shortfall; MVRs reviewed periodically — normally an investment return variation of up to 10% since last review is tolerated before an additional MVR review; MVRs not applied at maturity or death (Alba 8.6.12); with-profits bonds in the Phoenix WPF: no (or limited) MVR on encashment at the 10th policy anniversary (date varies by tranche); some policies allow small regular encashments MVR-free.
  - Alba WPF (from 2023 Scheme): maturity payouts targeted at 100% of asset shares (after guarantee charges for fully participating classes); guarantee charges applied only to the extent needed to eliminate a fund deficit, capped at 10% of asset shares unless liabilities (after the 10% charge) exceed assets by more than £92m, with an absolute cap of 25% of asset shares; previously applied guarantee charges are reversed when experience recovers; surrender payouts targeted at 100% of asset shares after guarantee charge.
  - Scottish Mutual WPF adverse-conditions ladder (12.12.8): (a) remove future planned asset-share enhancements; (b) remove past enhancements (to restore an estate of at least 0.5% of aggregate asset shares); (c) charge asset shares — max 1.0% of asset shares in one year; once cumulative charges reach 5.0% the maximum falls to 0.5% per year; cumulative cap 7.0% where policyholders bear all costs; (d) internal loan from Non-Profit Fund/Shareholder Fund. Recovery applied in reverse order.
  - Guaranteed annuity options (GAOs): present in several funds (e.g. Scottish Mutual deferred annuities, retirement annuity contracts; some unit-linked GAO risk from former Scottish Provident business); GAO liabilities backed by fixed-interest assets; interest-rate risk from GAOs explicitly identified as a business risk borne by the funds.
  - Final bonus and MVR interaction: in the Phoenix WPF final bonus and MVR do not apply simultaneously to any policy class (11.6.2); in some other funds (e.g. former funds within Britannic) final bonus and MVR may apply at the same time.

### S5 — Aviva Life & Pensions UK Limited PPFM (Old & New WPSF)
- Publisher: Aviva Life & Pensions UK Limited
- Title: "Principles and Practices of Financial Management (PPFM) for Aviva Life & Pensions UK Limited Old With-Profits Sub-Fund and New With-Profits Sub-Fund", 1 January 2026 (50 pp)
- Doc type: PPFM
- URL: https://static.aviva.io/content/dam/document-library/adviser/general/gn16214c.pdf
- Access date: 2026-08-03. Retrieved: YES (direct WebFetch returned HTTP 403; successfully downloaded with a browser user-agent and text-extracted)
- Key facts extracted:
  - Covers with-profits business of the Old WPSF and New WPSF (split created by the 1 October 2009 Reattribution Scheme of the CGNU Life and CULAC inherited estates; the Reattributed Inherited Estate External Support Account (RIEESA) supports the New WPSF; Aviva agreed to waive rights to withdraw/reduce that support).
  - Maturity payouts: managed so payouts for maturing policies average 100% of asset shares; maturity and surrender payouts for a group of policies should normally fall within 80%–120% of asset shares.
  - Smoothing (maturities): change in payout limited to the smoothing limit percentage when final bonus rates change — 5% if the payout at current final bonus rates lies within the target payout range, 7.5% if outside it; in normal circumstances the maximum amount of smoothing in one year is 15%; if solvency is threatened, larger limits or suspension of smoothing possible. Cost of smoothing intended broadly neutral long-term; no specific overall limit on accumulated smoothing cost beyond maintaining regulatory solvency.
  - Smoothing account: excess/deficit of smoothed payouts over asset shares is charged/credited to a smoothing account; at each calendar year-end the balance is recycled to asset shares through an addition/deduction to credited investment return, with the maximum deduction currently 2.5% of asset shares.
  - Unitised WP smoothing managed principally per year of unit purchase (single-premium basis).
  - Surrenders: target average payout 100% of asset shares less any protective deductions; standard actuarial formulae may be used where asset shares unavailable (e.g. whole life); surrender bases reviewed when underlying market indicators move 5% from the last review; no formal smoothing on surrenders.
  - MVR: may be applied to unitised WP whenever needed to protect the Sub-Fund from losses on unit cancellation, where asset share is less than the value credited via bonuses, subject to policy conditions; the MVR reduces final bonus first, then unit face value; an MVR never applies on death and at certain other policy-condition dates (MVR-free guarantee dates); MVRs target post-MVR payouts of 100% of asset share; individual policy payouts may fall within 90%–110% of asset share due to short-term market fluctuation; MVR rates rebalanced when market indicators move 5%; MVRs set by calendar year of unit purchase (pensions) or month (life).
  - Conventional asset shares = accumulation of premiums with actual investment returns (actual annual returns net of dealing costs), less expenses/charges (in line with 1 October 2009 basis; regulatory fees, audit fees and mis-selling costs are NOT charged to asset shares — borne by inherited estate; industry levies currently not charged), less mortality/risk costs, less shareholder transfers — shareholders currently receive 10% of distributed surplus, charged to asset shares; less any contribution for capital/guarantees/glide-path/smoothing. With-Profits Annuities: gross annuity instalments deducted; outset charge for the minimum floor guarantee.
  - Unitised WP asset shares: per-unit-allocation asset shares; AMC applied as a percentage of asset share; for certain pre-December 2000 UWP business the total charge to asset shares for selling/administering plus shareholder share of declared profits is restricted to 1% p.a. with effect from 6 April 2001; some products carry an annual charge of 0.7% of units for the first 10 years to help meet guarantee costs.
  - Special distributions: qualifying policies' asset shares were enhanced on 1 Jan 2008, 1 Jan 2009, 1 Jan 2010 (three tranches of Special Bonus connected to the reattribution).
  - Investment strategy: equity backing ratio (EBR) benchmark set against a "Theoretical EBR" for aggregate asset shares with a tolerance of 5% (up to 10% where beneficial); benchmark EBR subject to an upper limit of 75%; New/Old WPSF equivalent policies get the same credited return and same MVRs.

### S6 — Royal London Main Fund PPFM
- Publisher: The Royal London Mutual Insurance Society Limited
- Title: "Principles and Practices of Financial Management (PPFM) — Royal London Main Fund", Version 17.7, 1 January 2026 (61 pp)
- Doc type: PPFM
- URL: https://www.royallondon.com/siteassets/site-docs/about-us/corporate-goverance/ppfm/rl-ppfm-january-2026.pdf
- Access date: 2026-08-03. Retrieved: YES (downloaded and text-extracted)
- Key facts extracted:
  - Mutual insurer; eligible policies share in profits through "ProfitShare" — each year the directors determine profits from the Estate available for distribution; the amount may be zero.
  - ProfitShare application: conventional and unitised WP policies — extra regular bonus plus an enhancement to asset shares; unit-linked with-profits policies — additional units (regular bonus). For CWP/UWP policies started before 31 December 2021, the ProfitShare rate is 8× the rate applied to unit-linked WP policies; directors can change the multiple (independent actuarial advice required if below 6 or above 10); regulators told in advance of changes for pre-2022 policies.
  - Product types: conventional WP (asset share tracks policy value; asset share increased by ProfitShare; used to set final bonuses); unitised WP (same); unit-linked WP (bonus units added; not eligible for final bonuses; no asset shares or smoothing applied); deposit administration.
  - Target ranges: maturity payouts as % of asset share — for most conventional WP policies 80% to 130%; for most unitised WP policies 75% to 125%. Surrender payouts: conventional 80%–130%; unitised 75%–125% of asset share (with guaranteed benefits considered where no MVR applies).
  - Asset shares: premiums accumulated with actual investment return earned on assets backing WP policies, less expenses/charges (which may be related to asset share size or per-policy), risk-benefit charges, charges for guarantees (may be a direct charge or a reduction of credited return; some policies bear no guarantee charge), plus/minus cost or benefit of smoothing, tax (with correction of actual-vs-charged differences), and enhancements (temporary or permanent).
  - Smoothing: aims to limit year-on-year changes in maturity payouts of similar policies; formula moves payouts toward asset shares (larger correction the further payouts are from asset shares); no maximum amounts for smoothing increases/reductions; overall aim is that positive and negative smoothing roughly balance (cost-neutral over time); surrender benefits not usually smoothed except where formula includes final bonus.
  - MVR: for unitised WP and deposit administration; applied in challenging markets when asset share falls below guaranteed benefits plus final bonus; MVR scales usually set as the difference between asset shares and guarantees + final bonus; because final bonus rates are smoothed, an MVR may persist after markets improve until asset shares catch up; MVR applies only where allowable under policy conditions (not on contractual claim events).
  - Estate: if the Estate becomes too low, ProfitShare may be reduced/zeroed and charges to asset shares introduced/increased to restore it.

### S7 — NFU Mutual PPFM
- Publisher: NFU Mutual (The National Farmers Union Mutual Insurance Society Limited)
- Title: "Principles and Practices of Financial Management (PPFM)" (25 pp; undated current edition from NFU Mutual website)
- Doc type: PPFM
- URL: https://www.nfumutual.co.uk/globalassets/investments/with-profits/principles-practices-financial-management-ppfm.pdf
- Access date: 2026-08-03. Retrieved: YES (downloaded and text-extracted)
- Key facts extracted:
  - Mutual; the long-term business fund remains open — "no minimum scale of new business of a with-profits type required to justify the long-term fund remaining open to new business"; new business volumes controlled only if capital strain threatens solvency; maximum volumes may be set for products with significant guarantees.
  - Payout target: aggregate payouts of 100% of asset share over the longer term, subject to smoothing limits. Maturity payout ranges as % of underlying asset share: conventional (life and pension) 75% to 125%; unitised with-profits 85% to 111%; With-Profits Trustee Investment Plans 80% to 120%. Smoothing will not produce payouts above 120% (or 111% unitised) nor below 80% (85% unitised) of the underlying asset share.
  - Annual (regular) bonus: in normal circumstances, traditional WP annual bonus rates will not change by more than 1% compound from the previous year's value; for unitised WP the limits are 1.25% or 1.5% depending on product type as specified in policy literature; interim bonus rates set annually as best estimate of the next declaration.
  - Smoothing: payouts for policies of the same class with the same duration should not differ by more than 15% from one year to the next; surrender/transfer bases smoothed less than claims; With-Profits Trustee Investment Plan terminal bonus and MVR rates set against projected asset shares with a 3-month comparison; resulting MVRs of less than 3% are set to 0%.
  - MVR (unitised): triggered when the asset share is below 90% of the value of the with-profits units (including interim annual bonuses); for asset shares between 85% and 90% of unit value, the MVR is smoothed in linearly; below 85%, the full reduction to asset share is applied; the MVR is reduced linearly from 100% effect 3 years before the selected retirement date to 0% at the selected retirement date (MVR-free at retirement).
  - Asset shares: shadow-fund concept per class/generation; annual credited return may be the actual smoothed return of the fund; charges either direct to asset share or via reduced credited return; explicit tax allowance in aggregate; mortality/risk charges to asset shares.
  - Investment strategy: wide diversified spread (equities, gilts, fixed interest, property, alternatives incl. infrastructure/commodities), subject to guarantee levels and regulatory capital; different bonus series may have different backing assets depending on guarantee levels; CAB (cash accumulation) business backed mainly by floating-rate notes, CDs and cash.

### S8 — Prudential conventional with-profits customer guide
- Publisher: The Prudential Assurance Company Limited (M&G plc)
- Title: "Your Plan — a guide to how we manage the Fund (Conventional With-Profits Plans: endowment assurance, whole-of-life, and pension plans expressed as yearly income)" (8 pp)
- Doc type: consumer-facing with-profits guide (customer-friendly PPFM companion)
- URL: https://www.mandg.com/assets/shared/documents/en/wpgb0028.pdf
- Access date: 2026-08-03. Retrieved: YES
- Key facts extracted:
  - Two bonus types: regular bonus (not guaranteed to be added each year) and final bonus expected at claim; additional final bonus may apply to pension plans at certain retirement dates.
  - Concepts of "unsmoothed value" (the asset-share-based amount) vs "smoothed value" (the amount actually paid after smoothing).
  - Smoothing: payouts on maturity at normal retirement date will average 100% of the unsmoothed value; the difference between smoothed and unsmoothed values of a typical plan will rarely be more than 20% (bonus rates for all plans reconsidered if a high number exceed 20%); payouts normally limited to ±10% change year-on-year.
  - Shareholders receive up to 10% of distributed profit; remaining 90% to planholders via bonuses.
  - Final bonus rates on death for assurance plans equal the final bonus for maturing endowments (same duration basis).
  - Guarantees: sum assured plus attached bonuses guaranteed at maturity (and death); guarantee costs and smoothing costs are charged and can affect bonus rates.

### S9 — Prudential PruFund customer guide (smoothing parameter table)
- Publisher: The Prudential Assurance Company Limited (M&G plc)
- Title: "Your With-Profits Plan — a guide to how we manage the Fund (PruFund range of funds)" (8 pp)
- Doc type: consumer-facing with-profits guide
- URL: https://www.mandg.com/assets/shared/documents/en/wpgb0031.pdf
- Access date: 2026-08-03. Retrieved: YES
- Key facts extracted:
  - Daily process: gap between smoothed price and unsmoothed (NAV) price checked daily using spot and 5-day measures; if gap ≥ Daily Smoothing Limit, price adjusted immediately to the Gap After Adjustment; on quarter dates, if gap ≥ Quarterly Smoothing Limit, gap halved repeatedly until below the limit.
  - Current smoothing limits (Daily / Quarterly / Gap After Adjustment, as % of unsmoothed price):
    - PruFund Growth, Growth Pension/ISA, Protected Growth (+Pension), Growth & Income: 5.0% / 10.0% / 2.5%
    - PruFund Cautious, Cautious Pension/ISA, Protected Cautious (+Pension): 4.0% / 8.0% / 2.0%
    - PruFund Risk Managed 1 & 2 (+Pension/ISA): 4.0% / 8.0% / 2.0%
    - PruFund Risk Managed 3, 4, 5 (+Pension/ISA): 5.0% / 10.0% / 2.5%
  - Limits can vary by fund and may change.

### S10 — Prudential Investment Plan: Key Features Document
- Publisher: The Prudential Assurance Company Limited (M&G plc)
- Title: "Key Features of the Prudential Investment Plan" (16 pp)
- Doc type: key features document (currently marketed single-premium investment bond investing in PruFund and unit-linked funds)
- URL: https://www.mandg.com/dam/pru/shared/documents/en/pipk10011.pdf
- Access date: 2026-08-03. Retrieved: YES
- Key facts extracted:
  - Single or joint lives assured; minimum age of any life assured 3 months; maximum age at outset 85 (next birthday).
  - Minimum initial investment £10,000 (after adviser set-up charges); top-ups minimum £10,000; general maximum £5 million (higher by agreement).
  - Death benefit: 100.1% of the bid value of units (basic); optional Return of Premium Death Benefit guarantees the payout on death is at least premiums paid (monthly charge, taken only when the guaranteed minimum death benefit exceeds the basic 100.1% fund value benefit); this option cannot be added later.
  - PruFund guarantees: optional capital guarantees at start (see "PruFund range of funds: Guarantee Options" leaflet); annual guarantee charge taken by unit cancellation throughout the guaranteed term.
  - Withdrawals: regular and partial withdrawals allowed; up to 5% p.a. of the initial investment for up to 20 years is tax-deferred; each regular withdrawal must be over £50; at least £500 must remain invested in a fund; PruFund cancellations may be delayed up to 28 days (price at day 28 applies).
  - Charges: annual management charge with fund-size discount tiers — below £24,999: 0.30%; £25,000–£49,999: 0.35%; £50,000–£99,999: 0.40%; £100,000–£249,999: 0.45%; £250,000–£499,999: 0.475%; £500,000–£999,999: 0.50%; £1,000,000–£1,749,999: 0.525%; £1,750,000–£2,999,999: 0.55%; £3,000,000+: 0.575% (discount table); guarantee charges additional; adviser charges may be facilitated (as % of plan value or of premium).

### S11 — Prudential Investment Plan: Policy Provisions
- Publisher: The Prudential Assurance Company Limited (M&G plc)
- Title: "Policy Provisions — Prudential Investment Plan" (40 pp)
- Doc type: policy conditions (contractual)
- URL: https://www.pru.co.uk/pdf/INVM11630.pdf (301-redirects to https://www.mandg.com/dam/pru/shared/documents/en/INVM11630.pdf)
- Access date: 2026-08-03. Retrieved: YES
- Key facts extracted (contractual formulation of PruFund smoothing):
  - Defined terms: "Daily Smoothing Limit", "Quarterly Smoothing Limit", "Gap After Adjustment" (all expressed as percentages of the Unit Price), "Expected Growth Rate" (rate, which can be negative, applied daily to increase Unit Prices).
  - PruFund Growth Fund unit price was set at 100p per unit on 25 November 2004 (other funds seeded later, e.g. 25 August 2009).
  - Quarter-date rule: if NAV per unit exceeds/falls below the Unit Price by the Quarterly Smoothing Limit or more, the Unit Price is increased/reduced (by half the difference, repeatedly) until within the limit; daily rule: if both spot NAV and 5-day measure breach the Daily Smoothing Limit, price adjusted to the Gap After Adjustment.
  - Unit Price Reset provision: price may be set equal to NAV per unit on a working day to protect the fund, thereafter growing at EGR; smoothing suspension provision: price tracks NAV until suspension lifted.
  - Holding accounts (e.g. Protected Growth Account) grow at their own EGR pending automated unit purchase; holding-account prices are not subject to unit price reset.
  - Death benefit: 100.1% of the bid value of units credited to the Plan.

### S12 — Shepherds Friendly Investment ISA guide (open with-profits product)
- Publisher: The Shepherds Friendly Society Limited
- Title: "Investment ISA — Important Information Guide" (April 2025 edition, 24 pp)
- Doc type: consumer product guide / key information (with-profits stocks & shares ISA currently open to new business)
- URL: https://shepherdsfriendly.blob.core.windows.net/wp-media/2025/05/Investment-ISA-IIG-Final-170425.pdf
- Access date: 2026-08-03. Retrieved: YES
- Key facts extracted:
  - Insurance-based stocks & shares ISA invested in the Society's With-Profits Fund; open to anyone aged 18 or over; annual ISA subscription limit £20,000 (government limit).
  - Minimum contributions: £30 per month (may be reduced to a £10/month minimum later); minimum initial lump sum £100; further lump sums from £10.
  - Bonuses: added quarterly (normally); amounts vary and no bonus is guaranteed; a final bonus may be added at exit (not guaranteed).
  - Guarantee: a 101% guarantee applies to net money paid in (e.g. after investing £100 and withdrawing £20, the guarantee applies to the remaining £80).
  - MVR: a Market Value Reduction may be applied when the With-Profits Fund's value is falling, reducing withdrawal values.
  - Withdrawals: minimum £100, no charges; no explicit product charges disclosed (costs implicitly borne before bonus declaration).

### S13 — M&G/Prudential PPFM document index page
- Publisher: M&G plc (Prudential customer site)
- Title: "Financial Management of With-Profits Fund" (PPFM landing page)
- Doc type: document index (HTML)
- URL: https://www.mandg.com/pru/customer/en-gb/funds/ppfm
- Access date: 2026-08-03. Retrieved: YES
- Key facts: lists the full PPFM (wpgb0014.pdf), PruFund PPFM (wpgb0010.pdf), PPFM compliance report + With-Profits Actuary report (wpgb10005.pdf), summary of changes, With-Profits Committee terms of reference, and 19 consumer with-profits guides split by product family (PruFund pricing series D/E/F/S, unitised & cash accumulation, SALAS/SAL unitised, conventional, SALAS conventional, Income Choice Annuity, With-Profits Annuity, Equitable Life annuities, international bonds, Guaranteed Income Plan, asset mix leaflet) — evidence that firms publish per-product-family bonus/smoothing guides.

### S14 — Royal London PPFM index page
- Publisher: The Royal London Mutual Insurance Society Limited
- Title: "Principles and Practices of Financial Management (PPFM)" (governance page)
- Doc type: document index (HTML)
- URL: https://www.royallondon.com/about-us/how-we-are-run/governance-and-leadership-teams/corporate-governance/ppfm/
- Access date: 2026-08-03. Retrieved: YES
- Key facts: current documents are the Royal London Main Fund PPFM (January 2026) plus three separate RLCIS PPFMs (OB & IB Fund; With-Profits Pension Fund; With-Profits Stakeholder Fund, all January 2026 editions); nine RL customer guides and ten RLCIS guides by policy type; directors' PPFM compliance reports and With-Profits Committee terms of reference are also published.

### S15 — Scottish Widows / Clerical Medical PPFM — NOT RETRIEVED
- Publisher: Scottish Widows Limited (Lloyds Banking Group)
- Title: "The Clerical Medical With Profits Fund Principles and Practices of Financial Management" (EX1813); also "Report on Principles and Practices of Financial Management (PPFM) for 2025" (e1287)
- Doc type: PPFM / PPFM compliance report
- URL: https://adviser.scottishwidows.co.uk/assets/literature/docs/EX1813.pdf ; https://adviser.scottishwidows.co.uk/assets/literature/docs/e1287.pdf
- Access date: 2026-08-03. Retrieved: NO — the adviser.scottishwidows.co.uk site returned an error page ("Something went wrong") to automated fetches (bot protection); contents NOT verified and not used for any tagged fact. Search results indicate Scottish Widows runs two with-profits funds (Scottish Widows With Profits Fund and Clerical Medical With Profits Fund), each with its own PPFM, but this could not be confirmed from the documents themselves.

---

## Regulatory and actuarial references

### R1 — FCA COBS 20.2 "Treating with-profits policyholders fairly"
- Publisher: Financial Conduct Authority (FCA Handbook)
- Title: COBS 20.2 (as displayed 03/08/2026; last updated 26/06/2026)
- URL: https://www.handbook.fca.org.uk/handbook/COBS/20/2.html
- Access date: 2026-08-03. Retrieved: YES (full chapter text read via browser; site serves a JS shell to plain fetches)
- Key content:
  - COBS 20.2.1G: with-profits business involves discretion and conflicts (shareholders vs policyholders, between generations, with/without guarantees); policyholders have an interest in the whole with-profits fund.
  - Target ranges (COBS 20.2.3R–20.2.5R): unless maturity payments cannot reasonably be compared with asset shares, a firm must set a target range for maturity payments on all policies or each group; each target range must be expressed as a percentage of unsmoothed asset share and must include 100% of unsmoothed asset share; the firm must aim for each maturity payment to fall within the range. Unsmoothed asset share may be policy-specific or derived from specimen policies; for Solvency II firms it is calculated applying PRA Rulebook Valuation/Technical Provisions/Surplus Funds methods, including amounts added from inherited-estate distributions.
  - COBS 20.2.6R: a maturity payment may fall outside the target range if the firm has good reason to believe at least 90% of maturity payments in the group have fallen or will fall within the range.
  - Surrender values: a surrender target range top-end may be lower than the maturity range top-end (guidance before COBS 20.2.16R).
  - MVR restriction (COBS 20.2.16R): a firm must not, so far as reasonably practicable, apply a market value reduction to the face value of units of an accumulating with-profits policy unless the value of the units exceeds the underlying asset value, and the MVR is no greater than necessary to reflect that difference; COBS 20.2.16AR: exit volumes may be considered subject to that limit.
  - Distributions (COBS 20.2.17R): the amount distributed to policyholders from a with-profits fund must be not less than the "required percentage" of the total distributed; COBS 20.2.17AR: adjustments (e.g. MVRs, retrospective bonus reductions) reducing policyholder distributions below the required percentage require a proportionate reduction in shareholder transfers; COBS 20.2.17BG treats bonus reductions as "negative distributions"; COBS 20.2.17CR: no distribution unless the with-profits fund surplus is not eliminated (Solvency II firms) / regulatory surplus retained (non-SII firms); COBS 20.2.18R–19AR: restrictions and FCA-notification minima for distributions to non-policyholders.
  - Excess surplus (COBS 20.2.21R): at least annually (every 3 years for non-directive friendly societies), and on any reattribution, the governing body must determine whether each with-profits fund has an excess surplus; if retention would breach Principle 6/Consumer Duty, a distribution should be made.
  - New business (COBS 20.2.28R and guidance): firms must not write new business unless on terms unlikely to adversely affect existing with-profits policyholders' interests; attention at pricing/re-pricing; increments on existing policies are generally not "new business".
  - Closure/run-off (COBS 20.2.53R et seq.): on ceasing to effect a material volume of new with-profits business a firm must submit a run-off plan to the appropriate regulator within three months; content per SUP App 2.15; plan reviewed/updated periodically.
- Note: the precise Glossary definition of "required percentage" was not separately captured; PAC's own PPFM states its WPSF operates with at least 90% to policyholders [S1]. That 90:10 is the typical proprietary-fund basis is otherwise [unverified].

### R2 — FCA COBS 20.3 "Principles and Practices of Financial Management"
- Publisher: FCA Handbook
- Title: COBS 20.3 (as displayed 03/08/2026; last updated 01/01/2016)
- URL: https://www.handbook.fca.org.uk/handbook/COBS/20/3.html
- Access date: 2026-08-03. Retrieved: YES (full text via browser)
- Key content:
  - COBS 20.3.1R: a firm must establish and maintain the PPFM according to which its with-profits business is conducted (separate PPFM per fund if appropriate) and retain each version for five years; principles = enduring statements of standards/business model; practices = sufficiently detailed for a knowledgeable observer to understand the material risks and rewards; change controls (justification by governing body; error-correction/clarity/immaterial changes allowed).
  - COBS 20.3.4R/20.3.6R: PPFM must cover, in a prescribed table: (1) amount payable under a with-profits policy — methods, bonus-rate approach, smoothing approach (smoothing policy per policy type, limits on total cost of smoothing, limits on payment changes between periods); (2) investment strategy (matching, credit/liquidity/volatility, strategic assets, new instrument controls); (3) business risk (procedures, limits, allocation of profits/losses to payouts); (4) charges and expenses (application, apportionment); (5) management of inherited estate and its uses; (6) volumes of new business and arrangements on stopping new business; (7) equity between the with-profits fund and shareholders.
  - COBS 20.3.5R: PPFM must cover anything with a significant impact including scheme constraints, shareholder support commitments, support asset terms.
  - COBS 20.3.8G guidance table: target ranges for maturity payments, frequency of bonus resets, maximum amount by which annual bonuses would alter on reset, interim bonus approach, final bonus/MVR interaction, whether smoothing is intended to be neutral over time, preferred size of estate, profit-sharing basis, etc.

### R3 — FCA COBS 20.4 "Communications with with-profits policyholders"
- Publisher: FCA Handbook
- Title: COBS 20.4 (as displayed 03/08/2026; last updated 01/01/2021)
- URL: https://www.handbook.fca.org.uk/handbook/COBS/20/4.html
- Access date: 2026-08-03. Retrieved: YES (full text via browser)
- Key content: COBS 20.4.1R: PPFM must be provided on request (free to with-profits policyholders) and prominently signposted if on the website. COBS 20.4.2R: written notice of proposed changes to with-profits principles three months in advance; changes to practices within a reasonable time (exceptions for error/clarity/immaterial). COBS 20.4.7R: annual report to with-profits policyholders on PPFM compliance and exercise of discretion, addressing competing interests between classes and generations; with-profits actuary's annual policyholder report (SUP 4.3.16AR(4)) and any independent-judgement statement annexed (20.4.8G); report available within six months of financial year end (20.4.10G). (Earlier consumer-friendly PPFM rules no longer appear in the current chapter text; firms nevertheless still publish customer-facing fund guides [S8][S9][S13][S14].)

### R4 — FCA COBS 20.5 "With-profits governance"
- Publisher: FCA Handbook
- Title: COBS 20.5 (as displayed 03/08/2026; last updated 26/06/2026)
- URL: https://www.handbook.fca.org.uk/handbook/COBS/20/5.html
- Access date: 2026-08-03. Retrieved: YES (full text via browser)
- Key content: COBS 20.5.1R: for each with-profits fund a firm must appoint a with-profits committee (WPC) or (for smaller/simpler funds) an advisory arrangement, with published terms of reference. COBS 20.5.3R minimum ToR: assess/report/advise the governing body on fund management vs PPFM, PPFM compliance, conflicts (incl. shareholders), surplus and excess surplus identification and distribution policy, how bonus rates, smoothing and MVRs have been calculated and applied, relative interests of policyholders with and without valuable guarantees, communications, run-off plans, costs, support assets; WPC needs ≥3 members, quorum at least half and ≥2; advises on with-profits actuary appointment and assesses the WPA annually. COBS 20.5.4G: WPC expected to meet at least quarterly. COBS 20.5.5R: governing body must obtain and give due regard to WPC input, explain departures, notify FCA on request of WPC.

### R5 — FCA SUP 4.3 "Appointment of actuaries" (actuarial function and with-profits actuary function)
- Publisher: FCA Handbook
- Title: SUP 4.3 (as displayed 03/08/2026; last updated 07/03/2016)
- URL: https://www.handbook.fca.org.uk/handbook/SUP/4/3.html
- Access date: 2026-08-03. Retrieved: YES (full text via browser)
- Key content:
  - Actuaries appointed under PRA rules (s340 FSMA / PRA Conditions Governing Business 6) must be Fellows of the IFoA with appropriate practising certificates (SUP 4.3.9R/4.3.10G); with-profits actuary must not be chairman/CEO or a member of the governing body (SUP 4.3.12AR).
  - Actuarial function (SUP 4.3.13R): advise management on risks to meeting long-term liabilities and capital needs; monitor and escalate concerns; advise on methods/assumptions for actuarial investigations; perform and report on them.
  - With-profits actuary function (SUP 4.3.16AR): advise management on key aspects of the discretion exercised over with-profits business; for Solvency II firms, advise the governing body whether the assumptions used to calculate the future discretionary benefits within the technical provisions are consistent with the firm's PPFM (16A(2A)); report at least annually to the governing body on the discretion exercised; make an annual written report addressed to with-profits policyholders accompanying the COBS 20.4.7R report; advise on data/systems; advise on any actuarial investigation to determine with-profits fund surplus.
  - SUP 4.3.16BG: WPA advice/report should cover bonus rates at maturity/death/annual declarations, investment policy vs product disclosures, surrender value methodology (including market value adjusters), new business plans and premium rates, expense allocation, investment fees, PPFM changes, and communications.
  - SUP 4.3.17R: firm must resource and inform the WPA, request advice on material changes, pay due regard, allow direct access to the board, and manage WPA conflicts.

### R6 — PRA Rulebook: With-Profits Part
- Publisher: Prudential Regulation Authority (PRA Rulebook, Solvency II firms sector)
- Title: With-Profits Part (viewed in force 03/08/2026)
- URL: https://www.prarulebook.co.uk/pra-rules/with-profits
- Access date: 2026-08-03. Retrieved: YES (full text via browser; plain fetch returns 403)
- Key content: applies to UK Solvency II firms carrying on with-profits insurance business (not Holloway sickness policies) (1.1–1.2). Rule 2.1: a firm must hold assets in each with-profits fund of a value sufficient to cover the with-profits policy liabilities of the business written in or transferred into that fund (ring-fencing of the WP fund). Rule 3.1: the strategy for distribution of discretionary benefits of each with-profits fund must be affordable and sustainable and must not reasonably be expected to adversely affect the firm's safety and soundness or benefit security of all policyholders. Rule 4.1: support arrangements (external capital support to a WP fund) must have fully documented terms including repayment terms and restrictions.

### R7 — PRA Rulebook: Technical Provisions Part (Solvency UK; treatment of future discretionary benefits, risk margin)
- Publisher: PRA Rulebook (Solvency II firms sector)
- Title: Technical Provisions Part (viewed in force 03/08/2026)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Access date: 2026-08-03. Retrieved: YES (full text via browser)
- Key content:
  - Technical provisions = best estimate + risk margin (2.4); best estimate = probability-weighted average of future cash-flows discounted at the relevant risk-free term structure, gross of reinsurance (3.1); all cash in/out-flows to settle obligations over their lifetime (3.2).
  - Future discretionary benefits: rule 9.1(3) — technical provisions must take into account all payments to policyholders which firms expect to make, "whether or not those payments are contractually guaranteed, unless those payments fall within Surplus Funds 2.1". This is the Solvency UK basis for including FDB (future regular/final bonuses consistent with the PPFM) in the BEL, with the surplus-funds carve-out for the unallocated estate. Rule 9.2: value of financial guarantees and contractual options must be included; option-exercise (lapse/surrender) assumptions must be realistic and dynamic.
  - Post-2023/24 reform risk margin (rules 1.2, 4A.1): cost-of-capital rate reduced to 4% (per regulation 7B of the IRPR Regulations); risk margin formula RM = CoC × Σt SCR(t)·max(λ^t, λ_floor)/(1+r(t+1))^(t+1) with risk tapering factor λ = 0.9 for long-term business (floor 0.25) — the "Solvency UK" modified cost-of-capital with taper.
  - The former matching adjustment chapters (6, 7) are deleted (30/06/2024) — MA now governed by separate reformed provisions; volatility adjustment requires a s138BA FSMA permission (8.1). TMTP exists as a defined transitional measure (referenced at 4B.1(13)(d) alongside MA/VA as items the risk-margin reference undertaking must not apply).
- Note: with-profits BEL modelling therefore requires stochastic/market-consistent valuation of guarantees (9.2) plus FDB projection consistent with PPFM discretion (9.1(3) with SUP 4.3.16A(2A) [R5] tying FDB assumptions to the PPFM).

### R8 — PRA Rulebook: Surplus Funds Part (regulatory codification of asset-share methodology)
- Publisher: PRA Rulebook (Solvency II firms sector)
- Title: Surplus Funds Part (viewed in force 03/08/2026)
- URL: https://www.prarulebook.co.uk/pra-rules/surplus-funds
- Access date: 2026-08-03. Retrieved: YES (full text via browser)
- Key content:
  - Applies to UK Solvency II firms with with-profits business. Rule 2.1: surplus funds are not treated as insurance obligations in technical provisions (they are own funds — the estate).
  - Rule 3.1: surplus funds = with-profits assets − with-profits policy liabilities − tax/costs on future shareholder transfers − other attributable liabilities − value of future shareholder transfers.
  - Rule 3.3 (retrospective valuation — regulatory asset share definition): with-profits policy liabilities (other than future policy-related liabilities) are the aggregate retrospective value per policy of: premiums received; investment income and value changes; permanent enhancements; past miscellaneous surplus/deficit allocated; expenses/deductions; past deductions for cost of guarantees and smoothing, options, life cover; partial benefits paid; attributable tax; reinsurance amounts; past shareholder transfers (deducting implicit allowance for future shareholder transfers).
  - Rule 3.4/3.5 (prospective alternative where retrospective is inappropriate/impracticable): NPV of future premiums, expenses, planned deductions for guarantees/smoothing/options/life cover, benefits (all guaranteed benefits incl. guaranteed surrender and paid-up values; declared bonuses to which the policyholder is contractually entitled; future discretionary additions consistent with what the retrospective calculation would have produced), reinsurance and tax.
  - Rule 4.1: valuations must be consistent with technical provisions methodology.

### R9 — FSMA 2000 (Regulated Activities) Order 2001, Schedule 1 Part II (classes of long-term insurance business)
- Publisher: legislation.gov.uk (UK Statutory Instrument 2001/544)
- Title: RAO Schedule 1 Part II — Contracts of long-term insurance
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1/part/II
- Access date: 2026-08-03. Retrieved: YES
- Key content: Class I "Life and annuity" (contracts on human life / annuities on human life, excluding Class III) — conventional with-profits assurances and annuities fall here; Class III "Linked long term" (life/annuity contracts whose benefits are wholly or partly determined by reference to the value of, or income from, property or index fluctuations) — unitised/accumulating with-profits and PruFund-style contracts are typically written under Class I and/or III depending on structure ([unverified] as to per-product allocation); Classes II (marriage/birth), IV (permanent health), V (tontines), VI (capital redemption), VII (pension fund management), VIII/IX (collective/social insurance) also defined.

### R10 — CMI mortality and morbidity tables page
- Publisher: Continuous Mortality Investigation (CMI Limited / IFoA)
- Title: "CMI mortality and morbidity tables" (actuaries.org.uk)
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables
- Access date: 2026-08-03. Retrieved: YES
- Key content: CMI publishes assured-lives and annuitant table series — '80, '92, '00, '08, and '16 series for insurance business (term assurance and annuities), and S1/S2/S3/S4 series for self-administered pension schemes; morbidity series (critical illness AC04, '08, '16; income protection IP06/IP11 etc.). Access restriction: "Tables issued after 1 March 2013 are only available to organisations that subscribe to the CMI" — the older '92 series (e.g. AM92/AF92 used widely in historical with-profits work — table naming [R10], usage claim [unverified]) predates that restriction but full data are still distributed via CMI/IFoA channels. The CMI Mortality Projections Model (CMI_20xx series) is referenced through working papers rather than this page ([unverified] beyond page content).

### R11 — FRC Technical Actuarial Standards (TAS 200; TAS 100)
- Publisher: Financial Reporting Council
- Title: "Insurance Technical Actuarial Standard (TAS 200)" library page
- URL: https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-200/
- Access date: 2026-08-03. Retrieved: YES (TAS 200 page; the general actuarial-standards landing URL tried first returned 404)
- Key content: TAS 200: Insurance v2.0 published 20 September 2024, effective 1 January 2025; contains requirements for technical actuarial work in relation to insurance; mandatory for IFoA members. TAS 100 (general standard applying to all technical actuarial work) exists with its own library page https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/ (identified via search; that page itself not separately fetched — treat details of TAS 100 content as [unverified]). TAS 200 v2.0 revisions address Consumer Duty implications, insurance transformations, audit and assumption setting (per FRC news summary retrieved in search results).

### R12 — IFoA APS L1: Duties and Responsibilities of Life Assurance Actuaries
- Publisher: Institute and Faculty of Actuaries
- Title: "APS L1: Duties and Responsibilities of Life Assurance Actuaries", Version 4.0, effective 2 April 2024 (8 pp)
- URL: https://actuaries.org.uk/media/04ujhlcm/aps-l1-version-4-0.pdf
- Access date: 2026-08-03. Retrieved: YES (PDF fetched and text-extracted)
- Key content: covers Chief Actuary (Life), Small Insurer Chief Actuary, With-Profits Actuary and Appropriate Actuary roles. With-Profits Actuaries must hold a With-Profits Actuary Practising Certificate (3.1); restrictions on accepting appointment for only some with-profits funds (3.2–3.3); where the roles of Chief Actuary and With-Profits Actuary are combined, conflict-management provisions apply (5.1–5.2); where asset share calculation is not the WPA's direct responsibility, the WPA must still ensure appropriate oversight (5.6); Chief Actuary/WPA must request access to information (5.7); cross-references FCA COBS 20.3 (PPFM) in its definitions/appendix.

### R13 — IFoA SA2 resources page (canonical with-profits actuarial literature)
- Publisher: Institute and Faculty of Actuaries
- Title: "Resources for SA2" (Life Insurance specialist syllabus resources)
- URL: https://actuaries.org.uk/qualify/curriculum/life-insurance/resources-for-sa2/
- Access date: 2026-08-03. Retrieved: YES
- Key content — canonical papers listed with citations (papers themselves not fetched; titles/DOIs as listed on the page):
  - Needleman, P.D. & Roff, T.A. (1995), "Asset shares and their use in the financial management of a with-profits fund", British Actuarial Journal 1(4): 603–688, doi:10.1017/S1357321700001276 — the standard asset-share methodology reference.
  - Hibbert, A.J. & Turnbull, C.J. (2003), "Measuring and managing the economic risks and costs of with-profits business", BAJ 9(4): 725–786, doi:10.1017/S1357321700004347 — market-consistent valuation of with-profits guarantees/smoothing.
  - Hare, D.J.P. et al. (2000), "A market-based approach to pricing with-profits guarantees", BAJ 6(1): 143–213, doi:10.1017/S1357321700000842.
  - O'Brien, C.D. (2012), "Equity between with-profits policyholders and shareholders", BAJ 17(2): 435–474, doi:10.1017/S1357321712000074.

---

## Extracted specifications

### 1. Product forms and benefit structure
- Conventional (traditional) with-profits assurance: premium buys a basic sum assured (minimum maturity amount); regular/annual/reversionary bonuses are added at annual declarations and increase the guaranteed benefit once added; a final/terminal bonus may be added at claim (death, maturity, retirement) [S1][S4][S8]. Conventional deferred annuities carry a basic annuity p.a. plus bonuses [S1][S4].
- Death benefit on conventional endowments = sum assured + attached bonuses + any final bonus; some endowments carry an extra death-only sum assured or guaranteed minimum death benefit not participating in bonuses [S4].
- Bonus addition forms: regular bonus increases guaranteed benefits; a regular bonus becomes a contractual right only when added [S1]. Interim bonus rates cover claims between declarations [S1][S7]. Pension final bonus can increase the annuity or the cash available to buy one [S4].
- Simple vs compound bonus structure: the retrieved PPFMs describe bonus additions generically; explicit super-compound/compound classification per product was not found in the retrieved texts [unverified — commonly, UK conventional bonuses are compound (rate applied to sum assured + attaching bonuses) or super-compound (separate rates on sum assured and on bonuses)].
- Unitised (accumulating) with-profits: a proportion of each premium (less charges) buys with-profits units; annual bonus is delivered either by increasing the unit price at the daily equivalent of the declared annual rate, or by adding bonus units [S4]; claim value = unit value (+ bonus units) + any final bonus [S4]; cash accumulation variant adds bonuses directly to contributions [S1].
- MVR: on surrender/transfer outside guarantee dates, unit values (including final bonus) may be reduced by a market value reduction when the underlying asset share is below the face value of units [S1][S4][S5][S6][S7]; never on death [S5], not at maturity/death [S4-Alba], restricted by COBS 20.2.16R to the asset-value shortfall [R1].
- MVR-free points observed: contractual guarantee dates (product-specific) [S1][S4][S5]; 10th policy anniversary for certain with-profits bonds [S4]; selected retirement date with a 3-year linear taper to zero [S7]; death always [S5].
- Smoothed-fund (modern) variant — PruFund: no explicit bonuses; unit price rises daily at a published Expected Growth Rate (set quarterly) with rule-based unit price adjustments when the smoothed price diverges from the unsmoothed NAV beyond specified limits; optional capital guarantees at extra charge [S1][S2][S9][S10][S11].
- Credit matched with-profits (new PAC business type, 2026): guaranteed income/lump sum set at outset, small discretionary annual bonus, fixed-income backed, prospective asset shares [S1][S3].
- With-profits annuities: annuity income linked to fund performance via bonuses; income falls limited by the anticipated bonus rate chosen at outset; rises capped (11–12% p.a. at PAC) [S1].

### 2. Eligibility, premium and size parameters (currently sold products)
- Prudential Investment Plan (PruFund bond, on sale): lives assured aged 3 months to 85 (next birthday) at outset; minimum investment £10,000 (after set-up adviser charge); top-ups min £10,000; standard maximum £5m; death benefit 100.1% of unit bid value; optional return-of-premium death guarantee (charged monthly only while in the money); withdrawals ≥£50 each, ≥£500 must remain per fund; 5% p.a. tax-deferred withdrawal allowance for up to 20 years; unit cancellation may be deferred 28 days [S10][S11].
- Shepherds Friendly Investment ISA (with-profits ISA, open): age 18+; £30/month minimum (may drop to £10/month); £100 minimum lump sum (£10 top-ups); £20,000 p.a. ISA limit; quarterly bonuses (not guaranteed) plus possible final bonus; 101% guarantee on net money paid in; MVR possible; withdrawals min £100, no explicit charges [S12].
- Closed conventional business parameters (issue ages/premium ranges of endowments etc.) are not stated in PPFMs; they sit in original policy conditions which insurers do not generally republish [gap — see Gaps].

### 3. Bonus setting mechanics
- Regular bonus rates: set from projections of asset shares and guaranteed benefits, targeting a substantial final-bonus proportion of total payout [S1][S6][S7]; PAC: gradual changes "not expected to exceed 1% p.a.", full discretion to declare zero, no hard limit when protection requires [S1]; NFU Mutual: annual bonus rate changes limited (normal circumstances) to 1% compound year-on-year for traditional business, 1.25% or 1.5% for unitised depending on product [S7]; declared annually with interim rates between declarations [S1][S7]; PAC cash accumulation regular bonus guaranteed to next revision date [S1].
- Final bonus rates: normally reviewed/declared yearly (more often after large market moves) [S1][S4]; set by reference to (projected) specimen-policy asset shares subject to smoothing [S1][S4][S5][S7]; Aviva revisits final bonus scales when asset shares have moved 15%+ since rates were last set [S5]; in general at PAC the same final bonus scale applies to maturity, death and surrender [S1].
- Mutual distribution (Royal London): annual discretionary "ProfitShare" from the Estate (may be zero), applied as extra regular bonus + asset share enhancement (CWP/UWP) or bonus units (unit-linked WP); CWP/UWP rate = 8× UL rate, multiple variable 6–10 without independent advice [S6].
- Shareholder transfers: PAC WPSF ≥90% of divisible profit to policyholders (90:10; some 100:0 classes) [S1]; Aviva shareholders currently receive 10% of distributed surplus, charged to asset shares with caps/restrictions for certain tranches [S5]; consumer statement "up to 10% of any profit" to shareholders [S8]; COBS 20.2.17R "required percentage" floor with proportionate shareholder adjustment [R1].

### 4. Asset share methodology (the projection model core)
- Universal structure (retrospective accumulation), per firm practice and regulatory codification:
  - Income: premiums; actual investment return on the backing asset pool (incl. unrealised gains/losses); allocated miscellaneous surplus; past estate/excess-surplus distributions and enhancements [S1][S2][S4][S5][S6][S7][R8].
  - Outgo: expenses or expense charges (possibly capped/tariffed); commission; tax (life business; pensions gross) ; mortality/morbidity risk charges (rate × sum at risk); charges for cost of guarantees and smoothing; shareholder transfers (proprietary firms); payments out (withdrawals, partial surrenders, gross annuity instalments for WP annuities) [S1][S2][S5][S6][S7][R8].
  - PRA Surplus Funds 3.3 gives the same item list as the regulatory definition of retrospective with-profits policy liabilities [R8]; prospective alternative (3.4–3.5) where retrospective impracticable [R8]; PAC uses prospective asset shares for CMWP [S1].
- Specimen/sample policies: asset shares computed for specimen policies or groups, taken as representative; per-policy calculation not required [S1][S4][S5][R1 (COBS 20.2.5R(2))].
- Investment return credited: actual return on the relevant asset pool; asset shares are NOT credited with return earned on the Estate [S1][S2]; equivalent policies in Aviva Old/New WPSF receive identical credited returns [S5]; NFU Mutual may credit a smoothed actual return [S7].
- Expense charge examples: PAC post-1997 = point-of-sale policy charges, 2023 expense tariff otherwise, 1% p.a. cap on many pensions since April 2001 [S1]; Aviva 1% p.a. cap for certain pre-Dec-2000 UWP from 6 April 2001; 0.7% p.a. unit charge for first 10 years on certain products (guarantee cost) [S5]; Aviva excludes regulatory/audit/mis-selling costs from asset shares (borne by estate) [S5].
- Mortality charges: PAC charge = mortality rate × (death benefit − policy value), actual-vs-charged differences to Estate [S1]; Phoenix GMDB funded by monthly unit cancellation on sum at risk [S4].
- Tax: charged to life asset shares consistently with fund taxation (I-E style with relief on expenses); pension business gross; PAC assumed-vs-actual differences borne by Estate [S1][S2].

### 5. Target payout ranges and smoothing (comparison table)

| Firm / fund | Maturity target | Target range (% of asset share) | Smoothing limits |
|---|---|---|---|
| FCA baseline | must include 100% of unsmoothed asset share [R1] | firm-set; ≥90% of payouts in range [R1 COBS 20.2.6R] | PPFM must state limits [R2] |
| PAC WPSF | asset-share based | 80–120%, aim ≥90% of policies within [S1] | payouts normally change ≤10% y/y [S1]; smoothed vs unsmoothed rarely >20% apart [S8] |
| Aviva Old/New WPSF | average 100% of asset shares [S5] | 80–120% (group payouts) [S5] | 5% limit (within range) / 7.5% (outside); max 15% smoothing in one year; smoothing account recycled ≤2.5% of asset shares p.a. [S5] |
| Royal London Main Fund | asset-share guided [S6] | conventional 80–130%; unitised 75–125% [S6] | formulaic pull-to-asset-share; no fixed maximum change [S6] |
| NFU Mutual | 100% aggregate long-term [S7] | conventional 75–125%; unitised 85–111%; WP Trustee Inv Plan 80–120% [S7] | same-class payouts differ ≤15% y/y; hard floor/cap at range edges [S7] |
| Phoenix PLL (typical fund) | 100% of asset share [S4] | 80–120% before smoothing (maturity & surrender) [S4] | fund-specific; MVR review buffer 10% return variation [S4] |
- Smoothing cost neutrality: intended neutral over time at PAC (bonus smoothing accounts within Estate) [S1][S2], Aviva (no overall accumulated-cost limit beyond solvency) [S5], Royal London (positive/negative balance out) [S6]; COBS 20.3.8G expects the PPFM to state whether smoothing is intended to be neutral [R2].

### 6. Surrender, paid-up and alteration terms
- Accumulating/unitised surrender = smoothed value less any discontinuance charge, less MVR if applicable [S1][S5]; conventional surrender = formula on sum assured + bonuses + final bonus with parameters targeting asset shares over the long term, reviewed at least annually (PAC) or on 5% market moves (Aviva) [S1][S5]; surrender payouts progress smoothly into maturity values [S1].
- COBS permits a surrender target-range top-end below the maturity range top-end [R1].
- Paid-up policies: benefits reduced; future bonuses may or may not accrue depending on policy terms; lapse without value if criteria unmet [S4]; asset shares may not be a fair payout guide for altered/paid-up policies (handled separately) [S6].
- Deferred annuity cash claims reflect the current cost of the deferred annuity [S1].

### 7. PruFund-style smoothed fund mechanics (modern variation, currently sold)
- Unit price grows daily at the Expected Growth Rate (EGR), an annualised rate set quarterly by the PAC Board from expected long-term returns [S2][S11].
- Daily adjustment: if spot NAV/unit AND 5-working-day rolling average NAV/unit differ from the smoothed price by ≥ the Daily Smoothing Limit, price is immediately adjusted to within the Gap After Adjustment [S2][S9][S11].
- Quarterly adjustment: on each quarter date, while |NAV − price| ≥ Quarterly Smoothing Limit, the price is moved by half the difference (repeatedly) [S2][S9][S11].
- Current parameters: growth-type funds 5.0% daily / 10.0% quarterly / 2.5% gap; cautious and Risk Managed 1–2 funds 4.0% / 8.0% / 2.0%; Risk Managed 3–5 5.0% / 10.0% / 2.5% [S9].
- Protective machinery: unit price reset to NAV; suspension of smoothing (price tracks NAV); 28-day deferral of unit cancellation on switches/transfers/withdrawals [S2][S10][S11]; PruFund Growth seeded at 100p on 25 Nov 2004 [S11].
- Excess surplus distribution to eligible PruFund policies is delivered as unit price enhancements [S1][S2].
- Optional guarantees: minimum fund value at chosen guarantee dates for extra annual charge (unit cancellation), per Guarantee Options leaflet [S10].

### 8. Guarantees and guarantee charging
- Guarantee benefit forms: sum assured + attached regular bonuses guaranteed at death/maturity only (conventional) [S1][S4][S8]; unitised guarantee that unit face value (incl. added bonuses) is payable at contractual guarantee dates/death (MVR-free points) [S4][S5]; guaranteed minimum death benefits [S4]; PruFund optional guarantees [S10]; with-profits annuity income floors [S1][S5].
- Guaranteed annuity options (GAOs): present in Phoenix funds (Scottish Mutual deferred annuities and retirement annuities; former Scottish Provident unit-linked GAO risk); GAO liabilities backed by fixed-interest assets; GAO interest-rate risk identified as a fund business risk [S4]. Historical market significance (Equitable Life closure 2000 after House of Lords ruling on GAO costs) [unverified].
- Explicit guarantee charges: PAC traditional WP lifetime cap 2% of asset shares (4% for post-Mar-2019 AVCs); WPA/ICA annual charge by entry year; ELAS annuities ≤0.5% p.a. [S1]; Phoenix Alba fund: charges only if fund in deficit, cap 10% of asset shares (25% absolute; £92m deficit test), reversible [S4]; Scottish Mutual fund: deficit ladder max 1.0% p.a., 0.5% p.a. after 5.0% cumulative, 7.0% lifetime cap, estate floor 0.5% of asset shares [S4]; Aviva outset charge for WPA floor guarantee; 0.7%×10yr unit charge on certain products [S5]; Royal London: guarantee charge via asset share deduction or reduced credited return; some policies uncharged [S6].
- Regulatory valuation: guarantees and options must be valued in the BEL with realistic dynamic policyholder behaviour [R7]; FDB included in BEL unless within surplus funds [R7][R8]; WPA must confirm FDB assumptions are consistent with the PPFM [R5].

### 9. Estate (inherited estate) management
- Definition/purpose: excess of WP fund assets over asset shares and other liabilities; provides working capital, investment freedom, smoothing and guarantee support (PAC Estate) [S1]; regulatory surplus funds = own funds, excluded from technical provisions [R8].
- Usage constraints: PAC policyholders should expect no distribution from the Estate beyond normal smoothing/guarantee support; FSA-era constraints on new business support acknowledged [S1]; excess surplus determination at least annually required by COBS 20.2.21R with distribution if retention breaches fairness [R1]; distribution strategy must be affordable/sustainable (PRA With-Profits 3.1) [R6].
- Estate levels as management triggers: Phoenix SM fund targets estate ≥0.5% of aggregate asset shares in its deficit ladder; estates kept within target ranges by adjusting target payout ratios [S4]; Royal London can cut ProfitShare and charge asset shares to restore the Estate [S6].
- Reattribution precedent: Aviva 1 Oct 2009 Reattribution Scheme of CGNU/CULAC inherited estates; RIEESA supports New WPSF; Special Bonus tranches added to qualifying asset shares 1 Jan 2008/2009/2010; support cannot be withdrawn [S5].
- Excess surplus distribution mechanisms: PAC via ad hoc/additional bonus or PruFund unit price enhancements [S1][S2].

### 10. Investment strategy parameters
- Aviva: benchmark equity backing ratio managed against a theoretical EBR with 5% tolerance (10% max), EBR ceiling 75% [S5].
- PAC: WPSF invests across equities, property, fixed income incl. corporate debt (M&G managed); higher fixed-income matching for guarantee-heavy blocks (CMWP fully fixed-income backed) [S1].
- NFU Mutual: diversified equities/gilts/fixed interest/property/alternatives; bonus series may have different asset mixes depending on guarantee levels; CAB business in floating-rate notes/CDs/cash [S7].
- Phoenix: GAO liabilities backed by fixed interest; Alba equity exposure historically nil, some equities from 2017, property c.15% reduced over time [S4].
- COBS 20.3.6R(2) requires the PPFM to describe matching, credit/liquidity quality, strategic assets and new-instrument controls [R2].

### 11. New business status
- Open to new with-profits business (verified examples): PAC PruFund range (currently marketed, e.g. Prudential Investment Plan) [S10][S13]; PAC Credit Matched WP (Guaranteed Income Plan, WP BPA — new product type added v2.3 2026) [S1][S3]; NFU Mutual (open fund; no minimum new-business scale required) [S7]; Royal London (ProfitShare on unit-linked WP; business sold/switched on or after 31 Dec 2021 referenced) [S6]; Shepherds Friendly (with-profits ISA open) [S12].
- Closed/legacy: Phoenix Life's funds are run-off consolidations of many acquired offices (Britannic, Pearl, London Life, NPL, Scottish Mutual, SPI etc.) [S4]; Provident Mutual closed to new business 1995 (within Aviva) [S5]; most conventional with-profits funds in the UK market are closed to new business [unverified as a market-wide statement].
- Regulatory consequence of closure: run-off plan to the regulator within three months (COBS 20.2.53R) [R1].

### 12. Solvency and reporting treatment (for the liability model)
- BEL includes guaranteed benefits + FDB (future regular and final bonuses expected under PPFM discretion), except amounts qualifying as surplus funds [R7][R8]; guarantees/options valued market-consistently with dynamic lapse/exercise [R7].
- Risk margin: post-reform cost-of-capital method, CoC 4%, taper λ=0.9 (floor 0.25) for long-term business [R7]. TMTP: transitional measure on technical provisions still defined in the regime (excluded from risk-margin reference undertaking) [R7] — [brief; detailed TMTP rules not fetched].
- WP fund ring-fencing: assets covering WP liabilities must be held within each with-profits fund [R6]; support arrangements documented [R6].
- Governance inputs to discretion: With-Profits Committee review of bonus rates, smoothing, MVRs [R4]; With-Profits Actuary annual reports and FDB/PPFM consistency advice [R5]; PPFM as the public statement of the discretion model [R2]; annual PPFM-compliance report to policyholders [R3].

---

## Variations across insurers

1. Chassis split. Three distinct liability chassis coexist: (a) conventional WP — sum assured + declared bonus stack with formulaic surrender values [S1][S4][S8]; (b) unitised WP — unit account with bonus-driven unit price growth (or bonus units), MVR machinery and MVR-free dates [S4][S5][S6][S7]; (c) smoothed unit funds (PruFund) — EGR + rule-based price adjustment with no bonus declarations [S2][S9][S11]. A reference implementation should treat (a) and (b) as the core historical designs and (c) as the modern open-business design.

2. Target ranges. All firms target 100% of asset share on average, but ranges differ: 80–120% (PAC, Aviva, Phoenix) is the most common; Royal London uses 80–130% (conventional) / 75–125% (unitised); NFU Mutual uses 75–125% / 85–111% / 80–120% by product. The 80–120% band with a ≥90%-of-policies test is the representative design and matches the COBS structure (range must include 100% of unsmoothed asset share; 90% compliance test) [S1][S4][S5][S6][S7][R1].

3. Smoothing formulation varies more than any other feature: year-on-year payout change caps (PAC 10%; NFUM 15%; Aviva 5%/7.5% stepped with a 15% annual max), explicit smoothing accounts recycled to asset shares (Aviva, capped 2.5% p.a.; PAC bonus smoothing accounts in the Estate), or pure formulaic pull-to-asset-share with no stated cap (Royal London). For a representative model, a payout-change cap plus a smoothing account with long-run neutrality is the most transferable abstraction [S1][S5][S6][S7].

4. MVR triggers: asset share below face value of units (PAC, Aviva, Phoenix — shortfall-capped per COBS 20.2.16R), explicit numeric trigger/taper (NFU Mutual: <90% of unit value, taper 85–90%, retirement taper), or smoothing-account-negative triggers (parts of Phoenix Alba). MVR-free events are universal: death, contractual guarantee dates; frequently 10th anniversary (bonds) and selected retirement date [S1][S4][S5][S6][S7][R1].

5. Ownership/distribution: proprietary 90:10 funds (PAC WPSF, Aviva — shareholder transfer charged to asset shares) vs mutuals (Royal London ProfitShare with an 8× CWP/UWP-to-UL multiple; NFU Mutual with no shareholders) vs defined-charge structures (PAC DCPSF, 100:0 with explicit charges only). The 90:10 proprietary fund is the representative historical design; DCPSF/PruFund AMC-charged structures represent the modern design [S1][S2][S5][S6][S7].

6. Guarantee charging: lifetime caps as % of asset share (PAC 2%/4%), annual deduction from credited return (PAC WP annuities, RL option), conditional deficit-triggered charges with caps (Phoenix Alba 10%/25%; Scottish Mutual 1% p.a./7% lifetime), or premium-priced (CMWP). A model should expose the guarantee charge as a configurable deduction from the asset-share credited return with an optional lifetime cap [S1][S4][S6].

7. Estate handling ranges from pure working capital with no distribution expectation (PAC) to active distribution mechanisms (Aviva reattribution + special bonuses; RL annual ProfitShare; PAC excess-surplus unit enhancements) and estate-floor management triggers (Phoenix 0.5% of asset shares) [S1][S4][S5][S6].

Most representative single design for a reference conventional model: a closed proprietary 90:10 fund, asset shares built retrospectively per Surplus Funds 3.3 items, annual + final bonus with a 80–120% maturity target range (≥90% of policies), ±10% y/y payout smoothing, formulaic surrender targeting asset shares, guarantee charge ≤2% lifetime, estate as residual [S1][R1][R8]. Most representative unitised design: premium buys units, annual bonus via unit price growth, final bonus on claim, MVR = max(0, unit face value − asset share) outside MVR-free dates (death/guarantee dates/retirement), AMC ~1% p.a. capped legacy pensions [S1][S4][S5][R1]. Modern open design: PruFund-style EGR smoothing with the S9 parameter table.

---

## Gaps and caveats

1. Scottish Widows / Clerical Medical PPFMs could not be retrieved (adviser site bot-blocks automated fetches; error pages returned) — recorded as S15 with fetched_ok=false. No Scottish Widows-specific parameters are cited anywhere in these notes.
2. Aviva documents on static.aviva.io reject default fetchers (HTTP 403) but download with a browser user-agent; the file used (gn16214c.pdf, 1 Jan 2026) was fully retrieved and read.
3. Current declared bonus rates (annual/final bonus percentage declarations, current EGRs) were not collected — they live in annual bonus declarations, EGR announcements and per-product guides, not the PPFMs; the PruFund smoothing-limit table [S9] is the exception. A model calibration pass would need the current bonus declaration documents.
4. Conventional with-profits policy conditions (original endowment/whole-life wording with premium tables, issue-age limits, alteration clauses) are not published for closed books; PPFMs describe their management but not their original contract parameters. The retrieved KFD/policy-conditions pair (S10/S11) is for the modern PruFund bond; Shepherds Friendly (S12) covers an open with-profits ISA. Issue-age/premium specifics for conventional products remain a gap.
5. Simple vs compound vs super-compound bonus classification per product was not confirmed in any retrieved document and is flagged [unverified] where mentioned.
6. Equitable Life / GAO history (closure to new business in 2000 following the House of Lords Hyman ruling) is provided as [unverified] context; however the continuing existence of GAO exposure in current funds is verified via S4 (Phoenix) and the transfer of ELAS with-profits annuities to PAC is verified via S1.
7. CMI: table names and the post-1 March 2013 subscriber-only restriction are verified [R10]; the actual qx tables are not publicly retrievable and were not obtained; use of AM92/AF92 in historical with-profits valuation is [unverified] convention.
8. FCA Glossary definition of "required percentage" (COBS 20.2.17R) was not captured (glossary page IDs unstable); the 90% floor for PAC is instead evidenced from its PPFM [S1].
9. TAS 100 content details were not fetched (landing page only identified); TAS 200 v2.0 metadata verified [R11]. IFoA with-profits working party papers: canonical papers identified with full citations via the SA2 resources page [R13] but the papers themselves (paywalled BAJ) were not fetched.
10. TMTP treated briefly: its existence in the reformed regime is verified only via the risk-margin reference-undertaking exclusion list [R7]; detailed TMTP rules were not fetched.
11. The market-wide statement that most conventional/unitised WP funds are closed to new business is [unverified] in aggregate, though supported by examples (Phoenix consolidation funds S4; Provident Mutual S5) and counterexamples of open business are verified (S1/S3 CMWP, S7, S10, S12).
12. PDF text extraction (pypdf) introduces occasional ligature/spacing artifacts; all quoted numbers were checked in context, but page-perfect quotations should be re-verified against the PDFs before publication-grade use.
