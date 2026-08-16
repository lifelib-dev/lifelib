# Product Specification

**Status:** Draft, 2026-08-03. This is a **standardized composite specification** for reference
modeling — it does not reproduce any single insurer's product. Facts tagged [S#] and [R#] are
sourced from the product research notes (`_research/term-life.md`); facts tagged [REG-R#]
are sourced from the cross-product reference library
(`references/regulatory-and-actuarial-references.md`; research provenance in
`_research/regulatory-actuarial.md` for R1–R34 and in `_research/appp-a820-a821-a822.md` and
`_research/appp-a830.md` for the AP&P Manual appendix items cited here, same R-numbering). Values marked **[std]** are standardizations
introduced for the reference implementation; each **[std]** entry carries a footnote with the
rationale and the observed range across insurers. Facts the research notes flag as
[unverified] remain flagged here.

---

## Product overview and market role

Level premium term life insurance provides a guaranteed level death benefit for a fixed
initial "level term period" (commonly 10 to 40 years), during which gross premiums are
guaranteed not to change. After the level period the policy is renewable annually, without
evidence of insurability, at annually increasing premiums until expiry at attained age 95
[S2] [S3] [S5] [S6]. The policy accumulates no cash value, pays no dividends
(non-participating), and grants no policy loans [S3] [S6]. Most carriers also make the policy
convertible: the owner may exchange it for a permanent policy without new underwriting during
a contractually bounded conversion window [S2] [S3] [S6].

Term is the commodity protection product of the U.S. individual life market. Pricing at the
competitive cell examined in the research (Female 40, $1,000,000, best non-tobacco class,
20-year term) is tightly clustered — the top seven carriers were within $4 per year of each
other (≈$477–$480 annually) [S4]. The 20-year level term plan carries the highest in-force
exposure among level term types in the SOA/LIMRA 2015–2022 lapse study [R6]. For liability
modeling, the economically dominant feature is the post-level-term (PLT) transition: the
premium jump at the end of the level period triggers a shock lapse of 27%–96% and first-year
PLT mortality deterioration of 154%–1,066% of level-period mortality for Jump-to-ART designs
[R4], so the small surviving PLT block is heavily anti-selected.

---

## Representative specification

### Plan structure

| Parameter | Representative value | Basis |
|---|---|---|
| Product type | Individual level premium term; renewable and convertible; level death benefit | [S2] [S3] [S6] |
| Level term periods modeled | 10 / 20 / 30 years; **base cell = 20-year** | **[std]** (fn 1) |
| Coverage expiry | Attained age 95 (renewal ceases; policy expires without value) | [S2] [S3] [S5] [S6] |
| Age basis | Age nearest birthday (ANB); attained age = issue age + completed policy years | [S2] [S3] [S5] [S6] |
| Issue ages (non-tobacco) | 10-yr: 18–75; 20-yr: 18–70; 30-yr: 18–55 | **[std]** (fn 2) |
| Issue ages (tobacco) | Cap 5 years lower than non-tobacco cap per plan; floor 18 | **[std]** (fn 2) |
| Minimum face amount | $100,000 | [S1] [S2] [S3] [S5] [S6] |
| Maximum face amount | None modeled (band 4 is open-ended) | **[std]** (fn 3) |
| Participation / values | Non-participating; no cash value; no policy loans | [S3] [S6] |
| Free look | 30 days | [S6] |

**Footnotes**

1. **[std] Level period menu.** Observed menus: 10/15/20/25/30/35/40 (Protective [S1];
   Banner [S2]); 10/15/20/30 (Lincoln [S3]); 10/15/20/25/30 (Pacific Life [S4]); 18 periods
   including every year 15–30 (Corebridge [S5]). The 10/15/20/30 menu is the classic core
   (it is Lincoln's entire menu [S3]); the reference library models 10/20/30 and takes 20-year as the base cell because
   20-year term has the highest in-force exposure industry-wide [R6].
2. **[std] Issue ages.** Observed: Protective 20-yr NT 18–70 (tobacco 18–62), 10-yr 18–80,
   30-yr 18–58 [S1]; Banner 10-yr 20–75, 20-yr NT 20–70 (tobacco 20–65), 30-yr 20–55 [S2];
   Lincoln 10/15/20-yr 18–60, 30-yr NT 18–55 [S3]; Corebridge 10-yr 20–80, 20-yr 20–70,
   30-yr 20–55 [S5]. The representative grid uses minimum age 18 (Protective/Lincoln) and
   NT caps 75/70/55 — modal for the 20- and 30-year plans; the 10-year cap adopts Banner's
   75 [S2], between Lincoln's 60 [S3] and the Protective/Corebridge 80 [S1] [S5]; the
   tobacco cap reduction of 5 years approximates the observed
   pattern (Protective 20-yr −8 yrs, Banner 20-yr −5 yrs) without a per-plan table.
3. **[std] Maximum face.** Protective states no set maximum [S1]; Lincoln caps at
   $1,000,000 reflecting its accelerated/online underwriting program [S3]; Banner bands run
   to $10,000,001+ [S2]. The reference model imposes no maximum; underwriting-program caps
   are a distribution feature, not a liability mechanic.

### Rate classes and banding

| Parameter | Representative value | Basis |
|---|---|---|
| Rate classes | 4: Preferred Plus NT / Preferred NT / Standard NT / Standard Tobacco | **[std]** (fn 4) |
| Substandard ratings | Not modeled | **[std]** (fn 5) |
| Premium rate bands (by face) | 4: $100,000–249,999 / $250,000–499,999 / $500,000–999,999 / $1,000,000+ | [S5] boundaries; 4-band choice **[std]** (fn 6) |
| Per-$1,000 rate behavior | Rate per $1,000 decreases by band, constant within band | [S2] [S3] [S5] |

4. **[std] Rate classes.** Observed counts: 4 (Protective: Select Preferred, Preferred,
   Non-Tobacco, Tobacco [S1]), 5 (Lincoln [S3]), 6 (Banner [S2]), 8 (Corebridge [S5]). The
   common skeleton is preferred-plus/preferred/standard × tobacco with table ratings layered
   on a standard-type class [S2] [S3] [S5]. Four classes (three NT tiers + one tobacco) keep
   the model-point dimensionality small while preserving the preferred-structure mortality
   split that the 2015 VBT relative-risk tables support [REG-R18].
5. **[std] Substandard.** Observed: table ratings to Table D (Lincoln;
   flat extras to $5/1,000) [S3], Table H/D by issue age (Corebridge, on Special rates)
   [S5], ratings applied to Standard Plus rates (Banner) [S2]. Excluded from the reference
   model as a volume-minor complication; a flat mortality multiple can emulate it.
6. **[std] Bands.** Observed band counts: 3 (Lincoln [S3]), 4 (Corebridge [S5]), 7 (William
   Penn [S2]), 10 (Banner [S2]). Four bands with the Corebridge boundaries [S5] are chosen
   as the median-complexity structure that still exhibits the band-reversal lapse dynamics
   noted in the experience studies [R6].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium guarantee | Gross premiums fully guaranteed for all policy years (level period + ART tail); printed in policy specifications at issue | [S3] [S6] |
| Premium structure | Banded per-$1,000 rate × (face/1,000) + annual policy fee | [S2] [S3] [S5] [S6] |
| Annual policy fee | $65, fully guaranteed, level all years, non-commissionable | $65: [S6]; non-commissionable **[std]** (fn 7) |
| Modal factors (× annual premium) | Semi-annual 0.52; quarterly 0.27; monthly 0.08333 | [S6] (fn 8) |
| Level-period rate anchor 1 | M35 / Standard NT / $100,000 / 10-yr: $140/yr guaranteed (= $0.75 per $1,000 + $65 fee) | [S6] |
| Level-period rate anchor 2 | F40 / best NT class / $1,000,000 / 20-yr: ≈ $477/yr (≈ $0.41–$0.48 per $1,000 + fee) | [S4] |
| Full guaranteed rate table | Synthesized by the implementation, calibrated to the two anchors and the ART tail below | **[std]** (fn 9) |

7. **[std] Policy fee.** Observed: $90 Banner / $80 William Penn [S2]; $80–$90 by band,
   non-commissionable (Lincoln) [S3]; $74 band 1 (commissionable) / $64 bands 2–4
   (non-commissionable) (Corebridge) [S5]; $65 included in scheduled premium (Pacific Life
   specimen) [S6]. $65 is adopted because it keeps the specimen premium anchor internally
   consistent ($140 = $0.75 × 100 + $65) [S6]; non-commissionable follows the majority of
   observed fee treatments [S3] [S5].
8. Modal factors vary narrowly across carriers: Banner 0.51/0.26/0.085 [S2], Lincoln
   0.515/0.262/0.0875 [S3], Corebridge 0.52/0.265/0.0845 [S5], Pacific Life specimen
   0.52/0.27/0.08333 [S6]. The specimen set is used for consistency with the premium anchor.
9. **[std] Rate table.** No carrier publishes full per-$1,000 rate tables by
   age/class/band/duration in the retrieved documents; only the two cells above were
   verified (research notes, "Gaps and caveats"). The reference implementation therefore
   ships a synthesized guaranteed table constrained to reproduce both anchors and the ART
   tail anchor points below.

### Post-level term (PLT)

| Parameter | Representative value | Basis |
|---|---|---|
| PLT design | **Jump-to-ART**: face amount unchanged; premium jumps at end of level period, then increases annually to expiry at 95 | [S2] [S6]; most common U.S. structure [R4] |
| Guaranteed ART tail anchor (M35/$100k/10-yr, fee included) | Yr 11: $764; yr 12: $830; yr 15: $992; yr 20: $1,526; yr 30: $4,250; yr 40: $10,946; yr 50: $30,965; yr 60 (age 95): $74,780 | [S6] |
| Initial premium jump at anchor | $764 / $140 ≈ 5.46× (increase ≈ 446%, fee included) | [S6]-derived |
| Implied per-$1,000 ART rates (fee $65 removed) | Yr 11: $6.99; yr 12: $7.65; yr 15: $9.27; yr 20: $14.61; yr 30: $41.85; yr 40: $108.81; yr 50: $309.00; yr 60: $747.15 | [S6]-derived |
| Current PLT scale | Equal to guaranteed scale (no separate current scale modeled) | **[std]** (fn 10) |

10. **[std] Current PLT scale.** Graded PLT structures (smaller initial jump, premiums
    grading up annually) have become popular, in some cases implemented by re-rating
    in-force blocks [R4]; Lincoln instead decreases face and holds premium level for three
    years [S3], and Corebridge decreases face with premium initially near level [S5]. The
    reference product charges the guaranteed Jump-to-ART scale because it is the
    SOA-documented most common structure [R4] and because the specimen contract provides a
    complete verified guaranteed schedule for it [S6].

### Conversion

| Parameter | Representative value | Basis |
|---|---|---|
| Conversion right | To a permanent plan the insurer makes available, without evidence of insurability, same or most-comparable rate class | [S2] [S3] [S6] |
| Conversion window | Any time before min(end of level term period, policy anniversary at attained age 70) | [S2] [S3] (fn 11) |
| Conversion credit | One annual term premium, applied to the new policy's initial premium, if conversion occurs after policy year 1 | [S6] |
| Partial conversion | Allowed once; converted portion ≥ $250,000; remainder ≥ minimum face | [S6] |
| New policy face | Cannot exceed the term face | [S6] |
| Carry-overs | Suicide/contestable periods measured from original issue date | [S6] |
| Restriction | Not allowed while waiver-of-premium disability benefits apply (rider out of scope) | [S6] |

11. Window per Banner (level period or attained age 70, whichever first; 5 years if issued
    at 66+ — the 66+ carve-out is not modeled) [S2] and Lincoln (earlier of level period
    and attained age 70) [S3]. The Pacific Life specimen instead prints an explicit
    Conversion Period End Date (sample: 5 years on a 10-year plan) [S6]; Protective's
    longer rider-extended windows (8/13/18 years, to age 70) are [unverified]. The
    min(level period, age 70) rule is the modal contractual pattern [S2] [S3].

### Policy administration provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Grace period | 31 days; policy in force during grace; premium to end of policy month deducted from proceeds on death in grace | [S3] [S6] [S7] |
| Reinstatement | Within 3 years of lapse; evidence of insurability; overdue premiums with 6.00% compound interest | [S6] (fn 12) |
| Incontestability | 2 years from issue (separately from reinstatement) | [S1] [S2] [S6] |
| Suicide exclusion | 2 years; proceeds limited to premiums paid | [S2] [S6] (fn 13) |
| Misstatement of age/sex | Benefits adjusted to what premiums would have purchased at correct age/sex | [S1] [S6] |
| Requested face decrease | Once, after 5th policy year, up to 50% of face; new premium = ((a − b) × c) + b where b = policy fee (fee not scaled) | [S6] |
| Face increases | Not allowed after issue | [S3] |
| Termination | Earliest of death, expiry (age 95), conversion, lapse, successful contest, owner request; pro-rata premium refund beyond month of termination | [S6] |

12. Lincoln allows 5 years (and 15 days after the 46-day post-due-date window without
    evidence) [S3]; the specimen's 3-year/6% rule [S6] is adopted as it is complete
    contract language. Reinstatement is administratively real but not modeled as a
    decrement reversal in the base reference model (see technical notes).
13. 1-year suicide period in CO, MO, ND for Banner [S2]; state variations are out of scope
    for the composite.

### Death benefit

| Parameter | Representative value | Basis |
|---|---|---|
| Death benefit | Level face amount, guaranteed, all years (level period and ART tail) | [S1] [S2] [S6] |
| Proceeds formula | Face + rider benefits + pro-rata refund of premium paid beyond the month of death − premiums due and unpaid | [S6] |
| Delayed-claim interest | Interest payable on delayed claims (10% after 31 days in specimen) | [S6] |
| Settlement options | Lump sum default; guaranteed income options (≥2% interest; specimen uses Annuity 2000 female −5 yrs for life incomes) — not modeled | [S6]; exclusion **[std]** (fn 14) |

14. **[std] Settlement options.** Guaranteed purchase-rate income options [S6] and
    Protective's Income Provider Option installment endorsement [S7] exist but have
    negligible take-up impact on gross liability cash flows relative to lump sums; the
    reference model pays all death claims as lump sums.

---

## Contractual mechanics

### Premium provisions

The gross premium for each policy year is guaranteed at issue and printed in the policy
specifications for every year from issue to expiry at attained age 95 — level for the level
term period, then annually increasing (ART pattern) [S3] [S6]. The annual premium decomposes
as

```
AnnPrem(t) = rate_per_1000(x+t−1, class, band, plan, t) × Face/1000 + PolicyFee
```

with `PolicyFee = $65` level in all years [S6] (fee treatment per fn 7). During the level
period `rate_per_1000` is constant in `t`; after the level period it follows the guaranteed
ART scale [S2] [S6]. Modal premiums are `ModalFactor × AnnPrem` with factors 0.52 / 0.27 /
0.08333 (semi-annual / quarterly / monthly) [S6]; modal loadings are therefore implicit
(e.g. 12 × 0.08333 ≈ 1.000 in the specimen, but 12 × 0.085 = 1.02 at Banner [S2]).

There are no non-guaranteed premium elements in the representative product: no dividends,
no current-vs-guaranteed premium distinction [S3] [S6] (see fn 10 for the PLT scale choice).

### Death benefit provisions

The death benefit is the level face amount in all years, including the ART tail
[S1] [S2] [S6] (the Corebridge and Lincoln face-decrease PLT variants are documented under
"Variations" and not modeled [S3] [S5]). Proceeds on death equal face plus any rider
benefits, plus a pro-rata refund of premium paid beyond the policy month of death, minus due
and unpaid premium [S6]. If death occurs in the grace period, the premium to the end of the
policy month is deducted from proceeds [S3] [S6].

### Account / cash value mechanics

None. The policy accumulates no account value or cash surrender value, is non-participating,
and terminates without value on lapse or expiry [S3] [S6]. There are consequently no charges,
credits, loans, or withdrawals: Lincoln explicitly lists "Loans: N/A" [S3]. Long-duration
guaranteed-premium term can in principle generate nonforfeiture values under the Standard
Nonforfeiture Law [REG-R2]; the representative product is assumed to develop none **[std]**
(consistent with all retrieved product documents, none of which shows a cash value schedule
[S1] [S2] [S3] [S5] [S6]).

### Grace, lapse, reinstatement

If a premium is unpaid at its due date, a 31-day grace period begins during which the policy
remains in force [S3] [S6] [S7]. If the premium remains unpaid at the end of grace, the policy
lapses without value [S6]. Reinstatement is available within 3 years of lapse upon evidence
of insurability and payment of overdue premiums accumulated at 6.00% compound interest [S6].

### Renewal, conversion, maturity

- **Renewal.** At the end of the level term period, coverage continues automatically
  (no evidence of insurability) on the guaranteed ART scale, renewing annually to attained
  age 95, at which point the policy expires without value [S2] [S3] [S5] [S6].
- **Conversion.** At any time before min(end of level period, attained age 70) the owner may
  convert all or part (once, ≥$250,000 converted, remainder ≥ minimum face) of the face to a
  permanent policy without evidence of insurability, at attained-age premium rates for the
  same or most-comparable class; a conversion credit of one annual term premium is applied
  to the new policy's initial premium when conversion occurs after policy year 1
  [S2] [S3] [S6]. Conversion terminates the term policy (or reduces it, on partial
  conversion) [S6].
- **Maturity.** There is no maturity value; expiry at attained age 95 ends coverage [S6].

---

## Riders

### In scope

- **Accelerated Death Benefit (terminal illness) — included at no premium.** Included
  automatically on all policies at Banner (ICC10-ADB) [S2] and on Corebridge plans
  (accelerate up to the lesser of 50% of the specified amount and a scheduled maximum;
  eligibility on a 24-month prognosis (12 in NY); one-time administrative fee up to $500;
  payment reduces the death benefit) [S5]. Lincoln's version (R879) accelerates up to 50% of
  death benefit, max $250,000, discounted with interest under a lien approach [S3]; Pacific
  Life's forms are R16LYTIR / specimen R12TTI [S4] [S6]. **Modeling treatment [std]:** the
  rider is carried in the specification for completeness but modeled as cash-flow-neutral —
  an acceleration is approximately an actuarially discounted prepayment of an imminent death
  claim, and the rider carries no premium.

### Out of scope

Listed for completeness; none is modeled in the reference implementation:

- Waiver of premium (disability) [S2] [S3] [S5] [S6]
- Children's level term rider [S2] [S3] [S5]
- Additional-insured / layered term riders (e.g. Banner AIR 10/15/20-year) [S2]
- Accidental death benefit [S5]
- Conversion-extension riders with chronic-illness benefits (Protective Conversion
  Choice(SM) / ExtendCare(SM)) [S1] [S7]
- Income/settlement endorsements (Protective Income Provider Option [S7]; guaranteed income
  benefit plans [S6])
- Return-of-premium (ROP) term variants — no fetched insurer source documents one; the only
  verified ROP-related fact is VM-20's special NPR lapse treatment for policies with an
  endowment benefit [R2]; ROP products' existence is otherwise [unverified]
- Risk class improvement / re-qualification feature (Pacific Life: after 2nd anniversary to
  age 70, fee up to $100) [S6]

---

## Variations across insurers

1. **Term period menus.** 10–40 years including 35/40-year plans (Protective [S1], Banner
   [S2]); 10/15/20/30 only (Lincoln [S3]); every year 15–30 plus 10 and 35 (Corebridge
   [S5]); 10–30 in 5-year steps (Pacific Life [S4]). Representative choice 10/20/30 with a
   20-year base cell: a subset of the classic 10/15/20/30 core menu (Lincoln's exact
   lineup [S3]) weighted by in-force exposure [R6].
2. **PLT design — the largest structural variation.** (a) Jump-to-ART with face unchanged
   (Banner [S2], Pacific Life [S6]); (b) automatic face decrease with premium held level 3
   years then ART (Lincoln — explicitly a design to avoid premium sticker-shock and
   antiselective termination [S3]); (c) immediate face decrease with premium initially
   near-level then increasing (Corebridge [S5]); (d) graded PLT premium scales, sometimes
   applied retroactively to in-force blocks [R4]. Jump-to-ART is chosen because the SOA
   found it the most common U.S. structure [R4] and the full guaranteed schedule is
   verified [S6]; it also produces the strongest anti-selection dynamics, which the model
   must be able to represent.
3. **Rate classes.** 4 (Protective [S1]) to 8 (Corebridge [S5]); representative 4 **[std]**
   (fn 4).
4. **Policy fees and bands.** Fees $64–$90, commissionable or not [S2] [S3] [S5] [S6]; bands 3
   to 10 [S2] [S3] [S5]. Representative $65 fee / 4 bands (fns 6–7).
5. **Issue ages.** Minimum 18 (Protective, Lincoln [S1] [S3]) or 20 (Banner, Corebridge
   [S2] [S5]); maximum 80 on 10-year plans (Protective, Corebridge [S1] [S5]) but 60 at
   Lincoln's digital program [S3]. Representative grid per fn 2.
6. **Conversion.** All carriers convert without evidence, typically bounded by the level
   period and attained age 70, but: Banner grants 5 years at issue ages 66+ [S2]; Lincoln
   guarantees full-portfolio access for the first 7 years of the conversion period via
   amendment [S3]; Pacific Life prints an explicit Conversion Period End Date and pays a
   conversion credit of about one annual premium [S6]; Protective sells an optional rider
   lengthening the window with a chronic-illness benefit [S1] [S7], with numeric windows
   (8/13/18 years) [unverified]; Corebridge's month-based limits (96th/120th month) are
   [unverified]. Representative: min(level period, age 70) window + one-premium credit
   (fn 11).
7. **Pricing dispersion.** At the F40/$1M/best-NT/20-year cell the top 7 carriers sit
   within $4/yr (≈$477–$480) and the widest outlier is 54% higher [S4] — supporting a
   single representative rate scale calibrated to the cluster.

---

## Regulatory context

- **Standard Valuation Law (NAIC Model #820) [REG-R1], as codified in the AP&P Manual at
  Appendix A-820 [REG-R153].** The legal root of statutory reserving: minimum standards by
  calendar year of issue, CRVM (¶11), the deficiency-reserve rule (¶¶19–20), and the
  principle-based-valuation provisions delegating to the Valuation Manual (¶¶23–28)
  [REG-R1] [REG-R153]. **The appendix print has now been read in full and it settles two things
  this entry previously left open.** (i) The **VM operative date is no longer [unverified]**:
  ¶3 applies the PBR paragraphs to all policies and contracts "issued on or after the
  January 1, 2017, operative date of the Valuation Manual", and ¶4 provides that they "shall
  not apply" to earlier issues [REG-R153 ¶¶3–4](#uslib-reg-r153). (ii) The deficiency-reserve rule is **not an
  additive quantity but a floor**: where the gross premium charged in any contract year is less
  than the valuation net premium computed by the method actually used but on the **minimum**
  standards of mortality and interest, the minimum reserve is the greater of the reserve on the
  basis actually used and the reserve on the minimum standards with the **actual gross premium
  substituted for the valuation net premium in the deficient contract years only**
  [REG-R153 ¶19](#uslib-reg-r153). A-830 defines a *separate* deficiency quantity for the policies it reaches —
  see the next entry. One verified negative worth carrying: **the 2017 CSO is nowhere in
  A-820's printed text**, which names the 2001 CSO for issues from 1 January 2004 and the 1980
  CSO before that; the 2017 CSO reaches post-2017 issues through the Valuation Manual under
  ¶23 [REG-R153 ¶¶5, 23](#uslib-reg-r153).

- **Valuation of Life Insurance Policies — AP&P Appendix A-830 [REG-R154], the manual's
  print of the regulation known outside it as Model #830, "Regulation XXX" [R1] [REG-R6].** The
  pre-PBR reserve regime for level premium term, still operative for in-force blocks issued
  before PBR [REG-R6] [REG-R154]. **Cite it by paragraph:** the appendix is a flat sequence
  ¶¶1–32 plus an unnumbered Attachment, has **no Sections at all**, and the strings "Model #830"
  and "Regulation XXX" appear **nowhere in it** [REG-R154]. By its own ¶2 the method it defines
  **constitutes CRVM** for the policies it reaches, so it replaces rather than supplements the
  A-820 ¶11 construction [REG-R154 ¶2](#uslib-reg-r154) [REG-R153 ¶11](#uslib-reg-r153). Basic reserves for policies with
  guaranteed nonlevel gross premiums are the **greater of segmented and unitary** reserves under
  the contract segmentation method (¶21), which segments on the ratio of guaranteed gross
  premiums **per thousand of face amount, "ignoring policy fees only if level for the premium
  paying period"**, against the ratio of valuation mortality rates, with a company-elective ±1%
  tolerance on the mortality ratio, floored at 1 and elected **per policy year** (¶5) — the
  library's earlier second-hand statement of this construction is confirmed and the
  "per thousand of face amount" wording is exact [REG-R154 ¶¶5, 21](#uslib-reg-r154). Deficiency reserves are
  **quantity A less the basic reserve**, A being a full recalculation of the basic reserve with
  the **guaranteed** gross premium substituted for the net premium duration by duration wherever
  the gross is the smaller — a one-sided substitution, keyed to the guaranteed premium
  "determined at issue" and not to premium collected — mitigated by X-factor select mortality
  subject to a **two-limb** test (an aggregate present-value limb *and* a year-by-year floor over
  the first five years after the valuation date) and, whenever X falls below 100% at any duration
  for any policy, an annual actuarial opinion and memorandum under the **A-822** asset adequacy
  requirements [REG-R154 ¶¶7, 17, 22](#uslib-reg-r154). **The valuation basis is date-split, not 1980 CSO flat:**
  1980 CSO with elective select factors applies **before 1 January 2004**, and **from 1 January
  2004 the 2001 CSO Mortality Table is the minimum standard** for basic reserves, deficiency
  reserves and the tabular cost of insurance; the complete pre-2004 branch is retained in the
  print for valuing older issues [REG-R154 ¶¶16, 17, 23](#uslib-reg-r154). A level dollar policy fee after year 1
  may be excluded from the guaranteed gross premium wherever a calculation uses it — confirmed —
  with the asymmetry that for **deficiency** reserves the fee **may** be put back in even where it
  was excluded from the basic reserve [REG-R154 ¶19](#uslib-reg-r154). **A-830 prints no calendar effective date
  for itself**: "the effective date of this appendix" is an unresolved placeholder used eleven
  times, so **no date for when XXX first bit may be attributed to [REG-R154]** — the only calendar
  dates it prints are the 1 January 2004 cutover above. The XXX conservatism drove captive reserve
  financing, hence AG 48 [REG-R11] and Model #787 [REG-R12].

- **Valuation Manual / VM-20 [R2] [REG-R3].** For new issues, the minimum reserve is the
  seriatim net premium reserve (NPR) plus any excess of the modeled deterministic (DR) and
  stochastic (SR) reserves; the deterministic exclusion test no longer applies to term
  [R2]. Term NPR uses the 2017 CSO per VM-M, prescribed NPR interest, and prescribed
  lapses: 6%/yr during level periods of 5+ years (10% if <5 years), a prescribed shock
  lapse of 25%–80% at the end of the level period depending on segment lengths and the
  premium increase per $1,000 including the policy fee (70% jumping to ART with <400%
  increase; 80% with ≥400%), and 0% after the final premium [R2]. For the representative
  product the anchor jump is ≈446% including fee [S6]-derived, so the prescribed NPR shock
  is 80% [R2]. PLT profits may not be capitalized: for post-2017 issues the DR must assume
  100% lapse at the end of the level term when PV(PLT inflows) > PV(PLT outflows); PLT
  losses must be reflected; SR and pre-2017 blocks grade PLT profits toward zero where
  experience lacks credibility [R2].

- **2017 CSO tables [R3] [REG-R17].** The statutory valuation and nonforfeiture mortality
  family for new issues: composite, smoker-distinct, and preferred-structure versions,
  loaded/unloaded, ANB/ALB [R3] [REG-R17]. The reference model uses the ANB smoker-distinct
  loaded tables for guaranteed-basis calculations **[std]** (choice among [R3] variants). That
  **[std]** is **not** upgraded by the appendix prints now read: **neither A-820 nor A-830 names
  the 2017 CSO anywhere**, and neither prints any mortality table it does name — A-820 reaches
  the 2017 CSO only through its ¶5.a forward reference to tables "adopted subsequently by the
  NAIC" and, in practice, through the Valuation Manual under ¶23 [REG-R153 ¶¶5, 23](#uslib-reg-r153) [REG-R154].

- **Standard Nonforfeiture Law (Model #808) [REG-R2].** Sets minimum cash surrender values
  via the adjusted-premium method; relevant to term chiefly as the reason long-duration
  guaranteed-premium term *may* generate nonforfeiture values [REG-R2]. The representative
  product assumes none arise (see Account/cash value mechanics).

- **Reserve financing: AG 48 [REG-R11] and Model #787 [REG-R12].** XXX term reserve
  financing through captives requires prescribed Primary Security levels computed by the
  Actuarial Method, on pain of a qualified actuarial opinion [REG-R11], codified as a
  regulation in Model #787 [REG-R12]. Relevant to a reinsurance/collateral module, not to
  base liability cash flows [REG-R11].

- **IRC §7702 [R5] [REG-R13].** Federal definition of life insurance (CVAT, or guideline
  premium test plus cash value corridor with applicable percentages 250% at ages 0–40
  grading to 100% at 90–95) [R5]. Level premium term with no cash value satisfies these
  tests trivially, and §7702A MEC status is not normally implicated [R5 — analytical note
  flagged [unverified] in the research](#uslib-term_life-r5). No §7702 testing machinery is needed in the term
  reference model.

- **IRC §807 tax reserves [REG-R16].** Post-TCJA, the tax reserve is the greater of net
  surrender value and 92.81% of the NAIC-method reserve, capped at the statutory reserve
  [REG-R16]. For term (no surrender value) this is 92.81% of the CRVM/VM-20 quantity capped
  at statutory — a scalar wrapper on the statutory engine [REG-R16].

- **Interstate compact.** The specimen contract is issued under IIPRC (Interstate Insurance
  Product Regulation Commission) standards [S6]; state variations (policy forms, suicide
  periods, NY entities such as William Penn and US Life) apply to essentially all
  parameters [S2] [S5] and are out of scope for the composite.

---

*Companion documents: `technical-notes.md` (model mechanics), `sources.md` (citations).*

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-term_life-r1
[R2]: #uslib-term_life-r2
[R3]: #uslib-term_life-r3
[R4]: #uslib-term_life-r4
[R5]: #uslib-term_life-r5
[R6]: #uslib-term_life-r6
[REG-R1]: #uslib-reg-r1
[REG-R11]: #uslib-reg-r11
[REG-R12]: #uslib-reg-r12
[REG-R13]: #uslib-reg-r13
[REG-R153]: #uslib-reg-r153
[REG-R154]: #uslib-reg-r154
[REG-R16]: #uslib-reg-r16
[REG-R17]: #uslib-reg-r17
[REG-R18]: #uslib-reg-r18
[REG-R2]: #uslib-reg-r2
[REG-R3]: #uslib-reg-r3
[REG-R6]: #uslib-reg-r6
[S1]: #uslib-term_life-s1
[S2]: #uslib-term_life-s2
[S3]: #uslib-term_life-s3
[S4]: #uslib-term_life-s4
[S5]: #uslib-term_life-s5
[S6]: #uslib-term_life-s6
[S7]: #uslib-term_life-s7
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
