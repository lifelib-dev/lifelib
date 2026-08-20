# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03; see `sources.md`).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/unit-linked-bond.md` — resolve against
`sources.md` in this directory; [REG-R#] resolves against the cross-product reference
library `references/regulatory-and-actuarial-references.md` (its own R-numbering;
research provenance in `_research/regulatory-actuarial.md`). Values marked **[std]**
are standardizations introduced for the reference implementation; each [std] table row
carries a footnote giving the rationale and the observed range across insurers.
Facts the research file could not verify are flagged [unverified]. The implementation
anchor for mechanics is a single carrier's document pair — Key Features
Document [S1] plus Policy Provisions [S2] — the most completely specified public source.

---

## Product overview and market role

The onshore unit-linked investment bond is a single-premium ("lump sum") unit-linked
whole-of-life assurance: it has no fixed term or maturity date and is designed to be
held for five to ten years or more [S1] [S4] [S5]. It is a "contract of long-term
insurance" within the meaning of the FSMA 2000 (Regulated Activities) Order 2001
[S2 §18.5], and its linked benefit design places it in RAO Class III "Linked
long-term" [R4]. Units are purely notional records of benefit entitlement — the
policyholder does not own the units or any interest in the underlying assets
[S2 §3.1.5] [S3 Part D] [S5 Q1] — and the insurer's liability is capped at the value
derived from the assets underpinning each fund, with no make-whole if an external
fund manager defaults [S2 §3.1.9] [S4] [S1].

The product is sold as a tax wrapper: no personal capital gains tax applies, and
policyholder taxation runs through the chargeable-event regime with its cumulative 5%
per-annum tax-deferred withdrawal allowance [R1] [R2] [S1] [S4] [S5]. Because the insurer
pays corporation tax on the fund under the I-E/BLAGAB regime, gains carry a basic-rate
tax credit in the policyholder's hands [R6] [S4] [S5]. The life cover element is nominal
— a death uplift of 0.1%–1% over unit value [S1] [S2] [S3] [S4] [S5] — so the contract is
economically a taxed investment account with a thin insurance wrapper.

The market has consolidated around adviser-platform providers: one carrier closed its
onshore bond to new business on 23 January 2024 (retaining all features for existing
customers) to concentrate on offshore bonds, and the closed products were under 1% of
its customer base [S7]. Current open books are platform or platform-style
"clean-charge" designs (three of the carriers surveyed [S1] [S2] [S4] [S5]);
legacy back-books carry bid-offer, establishment and early cash-in charge layers
[S3] (see Variations).

---

## Representative specification

The composite is a modern **clean-charge onshore** single-premium bond on the
anchor carrier's chassis [S1] [S2], with the explicit life-fund tax pass-through
documented on the platform products [S4] [S5].

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-premium unit-linked whole-of-life assurance bond (onshore); no maturity date | [S1] [S2] [S4] [S5] |
| Legal class | RAO Class III linked long-term; contract of long-term insurance | [R4] [S2 §18.5] |
| Governing law | England (and Wales) | [S1] [S2 §18.4] [S3] [S4] [S5] |
| Lives assured | Single or joint lives, benefits on last death; composite models single life | design [S1] [S2 §9.2] [S3] [S4] [S5]; single-life choice **[std]** (1) |
| Plan owner | Individual 18+, UK resident (trustee/corporate ownership out of scope) | [S1] [S5]; scope **[std]** (1) |
| Issue ages (life assured) | 3 months to 85 next birthday | [S1]; band choice **[std]** (2) |
| Policy segmentation | 100 identical mini-policies ("segments"), premium and units divided equally | count **[std]** (3); mechanics [S1] [S2 §2.4] |
| Minimum single premium | £10,000 (after any set-up adviser charge) | [S1] [S4] [S5] |
| Top-ups | Permitted any time, minimum £10,000; blocked if no longer UK resident; excluded from base projection | [S1]; exclusion **[std]** (4) |
| Maximum investment | £5,000,000 (general limit; more by referral) | [S1] |
| Anchor model cell | Male 65, single life, £100,000 premium, no adviser charges, 5% p.a. regular withdrawals | **[std]** (5) |

Footnotes to [std] rows:

1. All five product sets write single or joint lives on a last-death basis; one
   platform bond allows up to 10 lives assured [S4] and another accepts companies and
   trusts [S5]. The composite restricts to a single life assured who is also the sole
   owner — joint-life last-death mortality is a second-order refinement for a product
   whose death strain is 0.1% of unit value (see Contractual mechanics).
2. Observed maxima for a life assured at outset: 85 next birthday [S1]; top-ups while
   the younger life is not over 84 (legacy) [S3]; 89 [S4]; owner aged 18–90 attained
   [S5]. The anchor carrier's band [S1] is adopted, since the composite is built on
   that carrier's document pair.
3. Observed segment counts: 20 default, up to 999 on request, minimum £1,000 per
   segment when more than 20 [S1] [S2 §2.4]; 100 [S3]; 1,000 [S4]; 1,000 [S5].
   Standardized to 100 so each segment is exactly 1% of the bond (£1,000 per segment
   at the anchor model cell premium, which meets that £1,000 per-segment floor
   [S2 §2.4]), matching the legacy structure [S3] and keeping segment-level
   arithmetic transparent. Purpose in every source is tax flexibility: full
   surrender of individual segments and part surrender across all segments produce
   different chargeable-event outcomes [S1] [S4] [S5 Q12] [R1 s484/s498](#uklib-unit_linked_bond-r1) [R2].
4. Top-up minima observed: £10,000 [S1]; £1,000 [S4]; permitted, minimum not stated
   [S5]. The base projection excludes top-ups; a top-up is modeled as a new model
   point (its own premium, allowance clock and segment set) — consistent with the
   statutory per-premium allowance arithmetic [R2].
5. Pure modeling choice: £100,000 sits inside all observed premium bands; age 65
   reflects the retirement-lump-sum use case implied by the 5–10-year holding design
   [S1] [S4] [S5] [unverified as a market-demographics fact]. Withdrawals at exactly
   the 5% allowance exercise the tax-deferral machinery without triggering excess
   events [R2].

### Death benefit (sum assured)

| Parameter | Representative value | Basis |
|---|---|---|
| Sum assured | 100.1% of the bid value of units (0.1% death uplift) | [S1] [S2 "Sum Assured"] [S5]; choice **[std]** (6) |
| Unit valuation on death | Units valued on the working day notice of death is received (12:00 cut-off); number of units = units in credit at the date of death, adjusted for post-death transactions | [S1] [S2 §4.2.7, §9] |
| Adviser charges after death | Ongoing/ad hoc adviser charges paid between death and processing are reclaimed and included in the claim | [S2 §9] |
| Deferral powers | Do not apply to death benefit payment | [S1] [S2 §8] |
| On payment | Plan cancelled; no further benefits | [S2 §9.5, §10.5] |
| Return-of-premium GMDB rider | Optional at outset only; described under Riders; excluded from the base model | [S1] [S2 §5.2, §10] [S5]; exclusion **[std]** (7) |

6. Observed death uplifts: 100.1% of bid value of units [S1] [S2]; 100.1% of plan
   value, 101% for pre-3-August-2006 plans (legacy) [S3]; 101% [S4]; 100.1% of
   surrender value, 101% prior to 25 November 2024 [S5]. 100.1% is chosen — it is the
   anchor-document value [S1] [S2], shared by another currently open product [S5];
   only one platform writes 101% [S4]. The 101% variant is a one-line parameter change
   (uplift 1.0% instead of 0.1%).
7. Both optional guarantees observed (a return-of-premium death benefit
   [S1] [S2 §5.2, §10]; a capital-protected death benefit [S5]) are elected at
   outset only, cancellable but not restartable, and charged monthly. Excluded from
   the base model to keep the death strain at 0.1% of unit value; the rider module is
   specified under Riders so it can be enabled without changing the core recursion.

### Charges (clean structure; snapshot where insurer-discretionary)

| Parameter | Representative value | Basis |
|---|---|---|
| Annual management charge (AMC) | 1.00% p.a. of unit value, accrued daily through the unit price (modeled as 1/12 monthly) | mechanism [S2 §5.1.1]; level **[std]** (8) |
| Fund-level further costs | 0.10% p.a., borne within the fund (not insurer income) | existence [S1] [S2 §3.1.7]; level **[std]** (9) |
| AMC fund-size discount | Not modeled; documented option — one carrier's tiers 0.30% (<£25k) to 0.575% (£3m+), applied monthly on AUM per premium | [S1] [S2 §5.1.4]; scope **[std]** (10) |
| Life-fund tax pass-through | 20% of the gross fund investment return, deducted within the unit price (neutral pass-through to the insurer) | mechanism [S2 §3.2.1] [S3 Part E] [S4] [S5 Q15]; rate proxy **[std]** (11) |
| Bid-offer spread / allocation rate | None — single-priced units, 100% allocation | [S3 Part D single-priced default] [S4] [S5]; clean scope **[std]** (12) |
| Establishment / early cash-in charges | None in the clean design | [S4] [S5]; scope **[std]** (12) |
| Switching | Free, unlimited (right to introduce charges reserved); anti-market-timing powers reserved | [S1] [S2 §6.3.1.2] [S3] [S5 Q10, Q11] |
| Dilution levy | Reserved power, collected through unit pricing; not modeled | [S2 §3.2.6]; scope **[std]** |

8. Actual AMC percentages are per-fund and live in fund guides that were not fetched
   (research gap 5 in `_research/unit-linked-bond.md`); only one carrier's
   fund-size *discount* tier table is public [S1]. 1.00% p.a. is a round
   representative level for a managed fund net of any discount. The AMC is
   insurer-reviewable — increase provisions tied to cost/tax/regulatory changes are
   documented on the legacy booklet [S3 Part D] — so the model treats it as a
   discretionary current element (class (b) in the technical notes).
9. Fund-level "further costs" (transaction/underlying costs) are confirmed to exist
   and be borne within funds [S1] [S2 §3.1.7] but no values are published in the
   fetched documents; 0.10% p.a. is a placeholder. They reduce the unit fund but are
   not insurer margin.
10. The tier table [S1]: <£24,999: 0.30%; £25,000–£49,999: 0.35%; £50,000–£99,999:
    0.40%; £100,000–£249,999: 0.45%; £250,000–£499,999: 0.475%; £500,000–£999,999:
    0.50%; £1,000,000–£1,749,999: 0.525%; £1,750,000–£2,999,999: 0.55%; £3,000,000+:
    0.575%, computed at each Monthly Transaction Date on assets under management per
    premium [S2 §5.1.4]. Omitted from the base model (a level net AMC is assumed);
    enabling it makes the AMC margin band-dependent on fund size.
11. Onshore life funds bear corporation tax on income and gains under I-E/BLAGAB, at
    the policyholder rate (basic rate, 20% in the HMRC example) on the policyholder
    slice [R6]. The two insurer-managed fund ranges allow for tax inside the daily unit
    price [S2 §3.2.1] [S3 Part E]; the platform products levy explicit periodic tax
    charges to the policy (on income as received, on realised gains at the next bond
    charge date, an annual deemed-disposal charge, and on full surrender from
    proceeds) [S4] [S5 Q15]. The composite standardizes to a flat 20% of the gross
    fund return deducted within the unit price — a deliberate simplification of the
    I-E timing detail (see technical notes for what the proxy ignores).
12. The clean design has no initial charge, no allocation-rate machinery and no exit
    penalties: one platform's withdrawals are "at any time without penalty" [S4] and
    the other discloses charges via personalised illustration documents with no
    early-exit layer recorded [S5 Q7]. Legacy layers (bid-offer One-Off Charge,
    Early Cash-in Charges, Establishment Charge [S3]) are back-book variations only —
    see Variations across insurers.

### Withdrawals, adviser charges and surrender

| Parameter | Representative value | Basis |
|---|---|---|
| Regular withdrawals | Monthly (available frequencies monthly/3-/4-/6-/12-monthly); amount as fixed £, % of premium, or % of unit value; minimum £50 per payment; ≥ £500 must remain per fund | [S1] [S2 §7.1] |
| Product cap on regular withdrawals | In any 12 months, greater of 7.5% of plan value and 7.5% of total paid in, with ongoing adviser charges aggregated inside the cap | [S1] [S2 §7.1] |
| One-off partial withdrawal | Any time, part surrender spread across all segments; irrevocable once received | [S2 §7] |
| Segment surrender | Full surrender of one or more individual segments | [S1] [S2 §2.4.5] [S4] [S5 Q12] |
| Full surrender value | Bid value of units — no surrender penalty in the clean design | [S4]; composite scope **[std]** (13) |
| Composite withdrawal behavior (anchor cell) | Regular withdrawals of 5% of the single premium p.a., paid monthly (£416.67/month on £100,000) | **[std]** (14) |
| Tax-deferred allowance (policyholder side) | Cumulative 5% of each premium per insurance year — statutorily, allowable element = premium × y/20, y capped at 20; unused allowance carries forward; excess over the cumulative allowance is an "excess event" gain at insurance-year end | [R2] [R1 s498/s507](#uklib-unit_linked_bond-r1) [S1] [S4] [S5 Q15] |
| Adviser charges | Set-up (deducted before investment; remainder is the Premium), ongoing (periodic, by unit cancellation spread across segments), ad hoc (one-off); ongoing/ad hoc treated as withdrawals for tax and counted inside the 7.5% cap; base model carries them at zero | [S1] [S2 §12.1–12.4] [S4] [S5 Q15]; zero **[std]** (15) |
| Maximum Limit Test | Caps total ongoing + ad hoc adviser charges per policy year; re-tested on partial withdrawals and instruction changes | [S2 §12.3.2, §12.7] |
| Cooling-off | 30 days from plan documents; refund reduced by any fall in value; adviser fees not refunded | [S1] [S4] [S5 Q19] |
| Settlement frictions | Same-working-day unit cancellation before 12:00 cut-off; up to 2 working days for large deals; deferral up to 6 months (property funds) / 1 month (others); not modeled | [S2 §4.1.1, §4.4, §8] [S1] [S3]; scope **[std]** |

13. The anchor provisions confirm partial/full withdrawals at any time with no
    penalty layer in the current product [S1] [S2 §7.2–7.3]; one platform states
    "without penalty" [S4]. The other caps a one-off part surrender at 95% of value
    with £1,000 minimum remaining [S5 Q12] — remaining-balance minima are
    administrative and not modeled. Early cash-in charges exist only in the legacy
    layer [S3].
14. 5% of premium p.a. equals the statutory tax-deferred allowance exactly [R2], sits
    inside the 7.5% product cap [S2 §7.1], and is the pattern every fetched KFD uses
    to explain the wrapper [S1] [S4] [S5]. Behavioral rationale and the dynamic variant
    are in the technical notes.
15. A representative ongoing adviser charge, when the module is enabled, is 0.5% p.a.
    of unit value — the illustrative rate in the anchor cap example ("0.5% OAC ⇒
    maximum 7% withdrawals") [S1] [S2 §7.1]. The anchor cell carries all three adviser
    charges at zero so the worked example stays within the 5% allowance without
    consuming it on charges (ongoing/ad hoc adviser charges consume the allowance
    [S2 §12.1.1] [S4] [S5 Q15]).

---

## Contractual mechanics

**Premium and segmentation.** A single premium P (the payment minus any set-up
adviser charge [S1] [S2 §1, §12.2]) buys units at the bid price across the chosen
funds; premium and units are divided equally between the 100 segments (**[std]**
count; mechanics [S1] [S2 §2.4]). Each segment is an identical mini-policy that can be
assigned or fully surrendered separately [S1] [S2 §2.4].

**Units and unit pricing.** Units are notional [S2 §3.1.5]. The anchor carrier's
internally-managed funds are valued at least monthly between a maximum value (lowest
buying price of assets) and minimum value (highest selling price), net of taxes,
duties, reserves and the AMC, with the basis swinging between purchase and sale
valuation according to whether the fund is expanding or contracting; bid price ≥
minimum value / units in issue, rounded to the nearest 0.1p [S2 §3.2.1–3.2.4].
Externally-linked funds follow the external manager's prices with the same
expansion/contraction logic [S2 §3.2.3, §3.2.5]; the legacy book values funds every
business day on the same swinging-basis design [S3 Part E]; platform deals receive
forward pricing at the next dealing point [S5 Q9]. The reference model abstracts all
of this to a single daily-priced, single-priced unit fund per policy (**[std]**; see
technical notes).

**Charges.** For unit-linked funds, 1/365 of the fund's AMC is deducted daily from
fund value and reflected in the bid price [S2 §5.1.1]. Fund-level further costs are
borne within the fund [S1] [S2 §3.1.7]. Tax on the life fund's income and gains is
allowed for inside the unit price (insured funds) [S2 §3.2.1] [S3 Part E] or charged
explicitly to the policy (platform products) [S4] [S5 Q15]. With AMC rate `c`, further
costs `f`, gross fund return `g` and tax proxy rate `t_pf` (composite values 1.00%,
0.10%, scenario input, 20% — all **[std]** as tabulated above), the annual unit-fund
growth relation the composite standardizes is:

    UF_after = UF_before × (1 + g × (1 − t_pf)) × (1 − c − f) − withdrawals − adviser charges

(the exact monthly discretization, processing order and dimension checks are in the
technical notes; the same parameter values are used there).

**Death benefit.** On death of the (last) life assured the plan pays the sum assured:

    DB = 100.1% × bid value of units    [S1] [S2]; uplift choice **[std]** (6)

with units counted at the date of death and valued on the working day notice is
received [S2 §4.2.7, §9]. The insurer's death strain per claim is DB − unit fund
= 0.1% of unit value (plus any GMDB in-the-money amount if the rider is attached
[S1] [S2 §5.2, §10]). The plan then terminates [S2 §9.5].

**Withdrawals.** Regular withdrawals run monthly to annually, subject to the £50
per-payment and £500 residual minima and the 12-month cap = max(7.5% of plan value,
7.5% of total paid in), with ongoing adviser charges counted inside the cap
[S1] [S2 §7.1]. One-off partial withdrawals are part surrenders spread across all
segments; alternatively whole segments are surrendered [S2 §2.4.5, §7] [S4] [S5 Q12].
All withdrawals and adviser charges are effected by unit cancellation.

**Policyholder tax machinery (contract-external, behavior-relevant).** At each
insurance-year end a periodic calculation compares cumulative withdrawals (including
ongoing/ad hoc adviser charges [S2 §12.1.1] [S4] [S5 Q15]) with the cumulative
allowable element = Σ premiums × y/20 (y = insurance years since payment, capped at
20) — i.e. 5% of each premium per year, unused amounts carried forward, full premium
allowable after 20 years [R2] [R1 s498/s507](#uklib-unit_linked_bond-r1). Withdrawals above the cumulative
allowance create an "excess event" gain; full surrender (of the bond or a segment),
death giving rise to benefits, and assignment for consideration are chargeable events
[R1 s484](#uklib-unit_linked_bond-r1), with gain = total benefit value − (allowable deductions + previous gains)
[R1 s491–s494](#uklib-unit_linked_bond-r1). On death the bond is treated as fully cashed in immediately before
death [S5 Q15] [R1 s484](#uklib-unit_linked_bond-r1). Gains are taxed as income of the policyholder with a
basic-rate credit (onshore) [S4] [S5 Q15] [R6]; top-slicing relief (s535–s537) and
deficiency relief (s539) exist in the statute [R1] [unverified beyond section
references]. The insurer issues Chargeable Event Certificates [S5 Q15]. None of this
is an insurer cash flow — it is modeled only through policyholder behavior (see
technical notes).

**Switching and fund powers.** Switching between funds is free (charge rights
reserved) [S1] [S2 §6.3.1.2] [S3] [S5 Q11]; the insurer may refuse, limit or charge
switches on suspicion of market timing [S3] [S5 Q10], and may close, merge or rename
funds with notice [S2 §3.1.3] [S3]. Fund-count limits vary (10 [S1] [S2 §3.1.4] to
open architecture [S4] [S5]); the reference model collapses the fund menu to a single
composite fund (**[std]**).

**Cancellation.** 30-day cooling-off with refund reduced by any fall in value
[S1] [S4] [S5 Q19]. There is no paid-up mechanism — a single-premium contract carries
no premium obligation [unverified as an explicit statement; consistent with all of
S1–S5].

---

## Riders and options

**In scope (described; charged at 0 / disabled in the base model [std]):**

- **Return-of-premium guaranteed minimum death benefit (GMDB).** As written on the
  anchor documents, the option pays max(Sum Assured, GMDB) where GMDB = total
  premiums (net of set-up adviser charges) − partial/regular withdrawals −
  ongoing/ad hoc adviser charges. Monthly charge = (GMDB − Sum Assured, if positive)
  × a mortality factor depending on age at the last policy anniversary, levied by
  unit cancellation pro-rata across premiums and funds; the charge is zero while the
  option is out of the money; elected at outset only, cancellable but not
  restartable [S1] [S2 §5.2, §10]. A second currently open product carries the
  same design (greater of premiums-less-withdrawals and 100.1% of value; monthly
  charge that may exceed growth; unavailable if any life assured is over 90 at
  outset) [S5]. The mortality-factor scale is not published in the fetched documents
  — a [std] placeholder scale is given in the technical notes.

**Out of scope (listed):**

- Accidental Death Benefit — 110% of bond value on accidental death within 90 days
  (legacy layer; war/self-inflicted/aviation exclusions) [S3].
- PruFund smoothed funds inside the wrapper — Expected Growth Rate accrual, quarterly
  and daily smoothing limits, 28-day waits, quarter dates [S2 §3.3.7–3.3.10]; see the
  with-profits folder (`products/with_profits/`) for smoothing mechanics; the
  smoothing parameters themselves are published separately and change over time
  [S2 §3.3.10].
- PruFund Protected Fund guarantee (Guaranteed Minimum Fund Value at a chosen
  Guarantee Date, fixed guarantee charge, proportional reduction for unit
  cancellations) [S2 §5.3, §11].
- With-profits funds within the bond, including Market Value Reduction (MVR) on
  cash-in or switch-out — MVR never applied on death or on regular withdrawals up to
  7.5% of plan value p.a. (legacy layer) [S3].
- Capital guarantee on the trustee-owned variant (greater of net invested premiums
  less withdrawals and 101% of bond value) [S3].
- Distribution funds / natural-income options [S1] [S3].
- Discretionary investment manager (DIM) portfolios and model-portfolio rebalancing
  [S4] [S5].
- Capital redemption variant [brief]: the same bond chassis written without lives
  assured as an RAO Class VI capital redemption contract, so no death-based
  chargeable event occurs; noted as a market variant only [REG-R14 class list;
  product-level terms not in any fetched document](#uklib-reg-r14) [unverified].

---

## Variations across insurers

1. **Death uplift.** 100.1% of unit value [S1] [S2] [S5] vs 101% [S4] [S3 pre-2006
   plans; S5 pre-25/11/2024]. Chosen: 100.1% — anchor-document value, currently
   marketed norm; the difference is a factor of 10 in the (still tiny) death strain.
2. **Segment count.** 20 default / up to 999 [S1] [S2] vs 100 [S3] vs 1,000 [S4] [S5].
   Chosen: 100 **[std]** (footnote 3) — mid-range, clean percentages.
3. **Charge architecture.** Clean fund-based AMC with tiered discount [S1] [S2] or
   platform charge plus fund charges plus explicit tax charge [S4] [S5], vs the legacy
   layer stack: bid-offer "One-Off Charge" implemented as offer price above bid on
   specified funds, Early Cash-in Charges (percentage of units cashed in before the
   end of a Schedule period, per payment, never on death, regular withdrawals within
   the "regular withdrawal percentage" exempt), Establishment Charge accruing daily
   in the early years collected monthly by unit cancellation, and a daily-accruing
   Yearly Management Charge [S3 Part C/D]. Chosen: clean structure; the legacy stack
   is documented here for back-book modeling. Allocation rates and initial/capital
   units were not present in any retrieved document and remain a [unverified] legacy
   variation.
4. **Life-fund tax presentation.** Implicit in daily unit pricing [S2 §3.2.1] [S3
   Part E] vs explicit periodic "charge in respect of tax" to the policy, including
   an annual deemed-disposal charge [S4] [S5 Q15]. Chosen: implicit-in-price 20%
   proxy **[std]** (footnote 11); the explicit variant matters for platform-bond
   admin reconciliation but not for the net cash flow shape.
5. **Fund menu.** ~10 concurrent internal/mirror funds [S1] [S2 §3.1.4]; 30 (legacy)
   [S3]; open architecture with ~3,000 collectives [S5] or unrestricted plus DIM
   [S4]. Chosen: single composite fund **[std]** — fund-menu breadth affects the
   return assumption, not the liability mechanics.
6. **Withdrawal caps.** 7.5%-of-value/paid-in product cap including ongoing adviser
   charges [S1] [S2 §7.1] vs minima-only (£25 minimum, £1,000 residual [S5]; residual
   minimum [S4]). Chosen: the 7.5% cap [S2 §7.1], because it is a real constraint
   that binds the withdrawal-plus-adviser-charge total.
7. **Smoothed-fund option.** PruFund range with published smoothing mechanics
   [S2 §3.3] vs a platform's smoothed-managed fund range (quarterly switch limit)
   [S4] vs with-profits with MVR (legacy) [S3] vs none [S5]. Chosen: excluded —
   smoothing belongs to the with-profits reference product.
8. **Guarantee riders.** Return-of-premium GMDB [S1] [S2 §5.2, §10] [S5] vs none
   observed on one platform KFD [S4]. Chosen: specified as an optional module,
   disabled in the base cell.
9. **Settlement frictions.** 28-day PruFund waits, 2-working-day large-deal delay,
   6-month property deferral [S1] [S2 §4.4, §8]; suspension/deferment powers [S3] [S4];
   forward pricing and ~10-working-day payout [S5 Q9, Q16]. Chosen: ignored in the
   monthly-grid model **[std]**; they matter for liquidity risk, not expected cash
   flows.

---

## Regulatory context

**PRA / Solvency UK.** Technical provisions for the bond equal a best estimate plus a
risk margin [R5 TP 2.4](#uklib-unit_linked_bond-r5); the best estimate is the probability-weighted average of
future cash flows discounted at the relevant risk-free term structure, and the
projection must take into account *all* cash in- and out-flows required to settle the
obligations [R5 TP 3.1, 3.2](#uklib-unit_linked_bond-r5) — for unit-linked business this is the rule-level anchor
for projecting fund-based charges, expenses and death strain alongside the unit fund.
The reformed UK risk margin applies a 4% cost-of-capital rate with a 0.9 risk-tapering
factor (floor 0.25) for long-term business [R5 TP 1.2, 4A.1](#uklib-unit_linked_bond-r5) [REG-R4]. This library
projects the gross best-estimate cash flows only (see technical notes).

**FCA conduct rules.** COBS 21.3 restricts what benefits may be linked to for
natural-person policyholders: only approved indices and the permitted-links asset
list (approved/listed securities, permitted unlisted securities, permitted land
and property, loans, deposits,
scheme interests, money-market instruments, cash, permitted units, stock lending,
derivatives, and conditional permitted links), classified by economic substance
[R3] [REG-R10]. This is why every fetched product reserves fund-deferral powers
aligned to illiquid assets (6-month property deferral [S1] [S2 §8] [S3]). The Consumer
Duty applies to this retail product; its price-and-value outcome bears on charge
levels of the kind snapshotted here [REG-R12; outcome-location detail unverified](#uklib-reg-r12).

**Policyholder tax (ITTOIA 2005 Part 4 Ch. 9).** The chargeable-event regime taxes
bond gains as income: events at s484 (death giving rise to benefits, full surrender,
assignment for consideration, maturity, part-surrender excess events via s509/s514), gain
computation at s491–s494, the 5%/20-year allowance machinery per s498/s507 as applied in
IPTM3560, and top-slicing relief at s535–s537 and deficiency relief at s539 [R1] [R2]. UK-resident
individuals, personal representatives and trustees are the liable persons
[R1 s465–s467](#uklib-unit_linked_bond-r1). Gains can affect personal allowances and means-tested benefits
[S1] [S5 Q15]. All of it is policyholder-side: the model carries it as behavior, not
cash flow.

**Company tax (I-E / BLAGAB).** Onshore bonds are BLAGAB: the insurer pays
corporation tax on investment income and chargeable gains allocated to the business
minus expenses, with the policyholder slice taxed at the basic rate and a minimum
profits test protecting the shareholder slice [R6] [REG-R17]. This is the source of
the basic-rate credit on policyholder gains [R6] [S4] [S5] and of the fund-level tax
drag the composite standardizes at 20% of gross return **[std]** (footnote 11).

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-unit_linked_bond-r1
[R2]: #uklib-unit_linked_bond-r2
[R3]: #uklib-unit_linked_bond-r3
[R4]: #uklib-unit_linked_bond-r4
[R6]: #uklib-unit_linked_bond-r6
[REG-R10]: #uklib-reg-r10
[REG-R17]: #uklib-reg-r17
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
