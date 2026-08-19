# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/critical-illness.md` and resolved against
`sources.md` in this directory — were extracted from the cited document. [REG-R#] tags
resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, distinct
from the product research file's R#; research provenance in
`_research/regulatory-actuarial.md`). Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a footnote
giving the rationale and the observed range across insurers. Facts the research file
could not verify are flagged [unverified].

**Base-chassis rule.** The representative product is an *accelerated* critical illness
benefit built on the level, guaranteed-premium term assurance chassis specified in
`products/term_assurance/` (companion product folder). Term-chassis provisions —
premium guarantee mechanics, terminal illness benefit, the first-year suicide clause on
the life element, grace and lapse, indexation (increasing cover) mechanics, and the
guaranteed insurability / life-change options — are cross-referenced there and only the
CI-specific deltas are restated here.

---

## Product overview and market role

UK Critical Illness Cover (CIC) pays a lump sum ("sum assured") on the diagnosis of a
defined critical illness. It is sold in two structures: (a) **accelerated** — combined
with life cover so the sum assured pays on the earlier of death, terminal illness, or
critical illness (offered as a combined life-and-critical-illness benefit [S11], and as
a single life-or-critical-illness menu benefit [S8]; joint-life cover on a first-event
basis [S11]); and (b) **standalone** — CI only, with no death benefit (the carrier that
supplies the combined benefit also sells a standalone CIC paying only on a defined
critical illness [S11]; another carrier's CI product is a standalone contract [S4]). A
further carrier sells CIC as a policy contractually separate from its life cover but
distributed with it [S1]. The policy ends when
the full (main) CI benefit is paid [S1] [S4] [S11]; lower-severity "additional payment"
conditions and children's claims pay capped partial amounts *without* reducing the sum
assured or ending the policy [S1] [S3] [S4] [S8] [S11].

The right to call a product "Critical Illness Cover" is governed by the ABI's *Guide to
Minimum Standards for Critical Illness Cover*, which "sets out the minimum standards
that insurers must meet to call their product Critical Illness Cover" [R2]; the
2021/22 review (guide dated 16 September 2022 [unverified — R1 not fetched], with
April 2023 clarifications) changed the Alzheimer's, cancer and heart-attack model
definitions, with insurer compliance required for new policies by 31 January 2024
[R2] [R3]. Insurer wordings visibly implement these model definitions [S1] [S11].
Market context: "On average, critical illness insurance policies only cover 75
conditions (Defaqto, 2026)" [S9]; most insurers now sell a core product plus an
enhanced tier (a two-tier menu [S3]; standard vs upgraded [S4] [S5]; a 1X/2X/3X
ladder [S9]).

The structural outlier is one carrier's **severity-graded design**: instead of a
full-payment conditions list, each condition is severity-graded and pays a percentage
of the cover amount — historically 5% (Severity G) to 100% (Severity A) [S10], and
25%–100% per claim on the current standard plan (114 conditions; upgradable to 174
conditions with total claims up to 3x the cover amount) [S9] — with payments reducing a
depletable "plan account" unless a protected-cover option reinstates cover [S10]. This
design is documented under *Variations across insurers* and excluded from the baseline.

These are pure protection contracts: the fetched policy documents describe cancellation
with no payment other than the cooling-off refund [S1] [S4] [S5]; no surrender value or
paid-up value exists [unverified as an explicit statement; consistent with all fetched
terms]. There is no asset share, bonus, or MVR mechanics anywhere in this product.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Accelerated CI: level term assurance + CI, sum assured paid on first event (death / terminal illness / critical illness), policy then ends | [S1] [S8] [S11]; composite **[std]** (1) |
| Standalone variant | Same chassis minus the death benefit (see Contractual mechanics) | [S4] [S11] |
| Benefit shape | Level lump sum (decreasing and family-income shapes out of scope) | [S4] [S7]; scope **[std]** (2) |
| Life basis | Single life (joint life first event as a variant) | [S11]; scope **[std]** (3) |
| Premium type | Guaranteed, level | [S1]; choice **[std]** (4) |
| Entry ages | 18–64 | 18 [S2] [S5] [S11]; 64 [S5]; composite **[std]** (5) |
| Maximum age at policy end | 75th birthday | [S2] [S5]; composite **[std]** (6) |
| Policy term | 5–50 years | [S2] [S5]; composite **[std]** (7) |
| Sum assured | No contractual minimum (minimum-premium driven); anchor cell £100,000 | no-minimum [S2]; anchor **[std]** (8) |
| Residency at application | UK resident, ≥183 days in the last tax year | [S1] |
| Anchor model cell | Male 40, non-smoker, £100,000 sum assured, 25-year term, accelerated, level guaranteed premium | **[std]** (8) |

Footnotes to [std] rows:

1. The dominant market design (four of the five carriers surveyed): one full payment on
   a defined-conditions list which ends the policy, plus non-depleting additional
   payments [S1] [S4] [S11] [S6]. Chosen over the severity-graded account design
   [S9] [S10], which is the documented alternative.
2. One carrier also offers "family income cover" paying equal monthly instalments to the
   end of term [S4]; another offers lump sum or regular payments (decreasing cover
   lump-sum only) [S7]. Level lump sum is the simplest common denominator.
3. Joint-life policies pay on a first-event basis [S11] and carry separation options
   ([S1] [S4] [S11], see Riders). Single life keeps the reference decrement model
   one-life.
4. Retail CIC premiums are now typically guaranteed [S1]; reviewable variants persist
   (one carrier offers both, 5-yearly reviews with "no limits on how much your premium
   can change" [S4] [S5]; another offers both [S7] [S8]; a third's intermediary-channel
   booklet is reviewable with 5-yearly reviews and ±5% tolerance [S3]). Guaranteed
   premiums are the modeling default; the reviewable variant is a module (see technical
   notes).
5. Observed minimum entry age 18 across three carriers [S2] [S5] [S11]. Observed
   maximum entry: 64 (one carrier [S5]; another's non-level options [S2]), 67 (the same
   carrier's life+CIC level option [S2]), 69 [S11]. 64 is the modal value.
6. Observed maximum age at policy end: 74 [S11], 75 (one carrier [S2]; another on
   guaranteed premiums [S5]), 90 (the same carrier's reviewable premiums) [S5]. 75
   matches the guaranteed-premium mainstream.
7. Observed terms: min 5 years (one carrier on guaranteed premiums [S5], and a second
   [S11]; 6 years on that first carrier's reviewable variant [S5]; 2 years for
   life-level-with-CIC at a third and 5 otherwise [S2]); max 50 years (two carriers)
   [S2] [S5], 40 [S11].
8. No insurer publishes CI rate cards (research-file gap), and explicit sum assured
   caps appear only as adviser-page maxima (£2m–£3m depending on TPD basis [S2]).
   £100,000 / male 40 / 25 years is a pure modeling anchor; the level guaranteed
   premium attached to it in the technical notes (£55/month) is a **[std]**
   placeholder, not a quoted rate.

### Benefits

| Parameter | Representative value | Basis |
|---|---|---|
| Main benefit | Sum assured, once, on the first of: death, terminal illness, or diagnosis of a listed critical illness (with survival period); policy ends on payment | [S1] [S4] [S8] [S11] |
| Survival period | 14 days from diagnosis; payable even if survival completes after the policy end date | [S1]; pick **[std]** (9) |
| Full-payment conditions | ~40 ABI-aligned definitions including TPD; concrete reference list = one carrier's retail list (~37 definitions) | list [S1]; count **[std]** (10) |
| TPD definition | Own occupation before 70th birthday, or Specified Work Tasks (unable ever again to do 3 of 6 tasks); TPD cover drops off at age 70 with a premium reduction | [S1]; mirrored at a second carrier [S4] |
| Additional-payment conditions | 2 conditions (carcinoma in situ of the breast treated by surgery; low-grade prostate cancer), each paying the lower of 25% of sum assured and £25,000; does not reduce the sum assured or end the policy; one claim per condition per life [S11] | [S1] [S4] [S5] [S11]; calibration **[std]** (11) |
| Children's cover | Automatic; lower of 50% of sum assured and £25,000 per child; max 2 children's claims per policy; child aged 30 days to 18th birthday (21 if in full-time education) | [S1]; calibration **[std]** (12) |
| Child funeral benefit | £4,000 (max 2 children) | [S1]; range £4,000–£10,000 [S4] [S6] [S8] [S11] |
| Diagnosis standard | Diagnosis by a (UK) consultant of appropriate specialism | [S1] [S4] |
| Claim-validity residence | Claims payable while the life insured resides in EU, Australia, Canada, Channel Islands, Isle of Man, New Zealand, UK, USA (insurer discretion elsewhere) | [S1] [S3] |

9. Observed survival periods: 14 days (one retail wording, including children; and the
   severity-graded plan) [S1] [S10]; 10 days (main, additional and children's benefits
   at another carrier [S4] [S5]; additional/children's at a further carrier [S8]; and
   the same retail carrier's intermediary children's cover [S3]). The ABI-typical
   survival period is 14 days [unverified — R1 not fetched]. 14 days chosen as the
   value in [S1] [S10] and the [unverified] ABI-typical figure.
10. Observed full-payment counts: 33 (standard tier, incl. terminal illness) [S5], ~37
    (a retail list, incl. TPD) [S1], 39 (incl. terminal illness) [S11], 46 [S6];
    enhanced tiers add ~15–20 more [S3] [S4] [S5]. "~40 incl. TPD" is the composite;
    the model treats the list as a single aggregate incidence basis, so the count is
    documentation, not a parameter.
11. Observed additional-payment calibrations: 2 conditions at lower of 25%/£25,000
    (three carriers: a retail wording [S1]; a standard tier [S4] [S5]; and a third
    allowing one claim per condition per life [S11]) → ~22 conditions at lower of
    50%/£30,000 (an enhanced tier [S3]) → 32 conditions at 50% up to £35,000
    ([S6] [S8]) → 26 conditions at lower of 100%/£30,000 (an upgraded tier [S4] [S5]).
    The core-tier calibration (2 conditions, 25%/£25,000) is adopted.
12. Observed children's cover: lower of 50%/£25,000, max 2 children, ages 30 days–18
    (21 FTE), £50,000 max per child across policies [S1]; lower of £25,000/50%
    standard or flat £25,000 upgraded, to 18 (21 FTE) or birth–22 upgraded [S4];
    50% capped £30,000–£50,000 to age 22/23 [S6] [S8]; optional, lower of £25,000/50%
    to 22nd birthday [S11]. Automatic inclusion is the pattern at three of the four
    carriers [S1] [S4] [S7]; the retail calibration in [S1] is adopted.

### Premiums and policy administration

| Parameter | Representative value | Basis |
|---|---|---|
| Premium guarantee | Guaranteed: rates fixed at outset for the full term | [S1]; choice **[std]** (see footnote 4) |
| Premium frequency | Monthly or annual | [S1] [S4] |
| Grace period | 60 days; then cancellation without refund | [S1] [S4]; pick **[std]** (13) |
| Cooling-off | 30 days with full premium refund; thereafter no refund on monthly premiums | [S1] [S4] [S5] |
| Indexation (increasing cover option) | Per term chassis composite: sum assured up by RPI (no increase if RPI ≤ 0%, capped 10% p.a.); premium up by RPI x 1.5 capped 15% p.a.; declining 3 years in a row removes the option (one carrier's own wording floors increases at RPI < 1% [S1]) | term-assurance chassis composite; [S1]; another similar (RPI or fixed 3%/5%) [S4] |
| Guaranteed insurability (life events) | Per term chassis: increase on marriage/mortgage/birth etc., capped at the lower of 100% of original cover and £200,000; eldest life under 55 | [S1] [S4]; ≤54 with the same cap at a third carrier [S11] |
| Waiver of premium | Optional rider, out of model scope: premiums waived after a 26-week deferred period of incapacity | [S1]; elsewhere a deferred period stopping at 71 [S4] |
| Surrender / paid-up value | None; lapse yields no payment | [S1] [S4] [S5]; absence of surrender value [unverified as explicit statement] |
| Misrepresentation remedy | Proportionate reduction: new cover = premium charged x original cover / higher premium | [S1] |
| FSCS protection | 100% of claim value, continuity preferred | [S1] |

13. Observed grace: 60 days (two retail wordings) [S1] [S4]; 30 days (an intermediary
    wording) [S3]. 60 days adopted as the retail mainstream.

---

## Contractual mechanics

Notation: `SA` = sum assured; `P` = level guaranteed premium (per frequency);
subscripted benefit amounts as below. The same symbols and values are used in
`technical-notes.md`.

**First-event main benefit (accelerated).** The policy pays `SA` exactly once, on the
first of: (i) death of the life assured; (ii) terminal illness (per the term chassis);
(iii) diagnosis of a listed critical illness or undergoing a listed medical procedure,
provided the life assured survives 14 days from diagnosis [S1]. The 14-day survival
condition is satisfied even if the 14th day falls after the policy end date, so long as
diagnosis occurred in-term [S1]. Payment of the main benefit terminates the policy
[S1] [S4] [S11]. Because death within the survival period itself triggers the death
benefit for the same `SA`, the survival period is cash-flow-neutral in the accelerated
design (it only reclassifies the claim); it is economically binding only in the
standalone variant.

**Additional-payment benefit (non-depleting).** For each of the 2 listed lower-severity
conditions, one claim per condition per life:

    B_AP = min(0.25 x SA, GBP 25,000)                    [S1][S4][S11]

Payment of `B_AP` does not reduce `SA`, does not end the policy, and does not change
the premium [S1] [S3] [S4] [S8] [S11].

**Children's cover (non-depleting).** Each eligible child (30 days to 18th birthday, 21
if in full-time education) is covered for the listed full-payment conditions on the
same definitions, with a 14-day child survival period [S1]:

    B_child = min(0.50 x SA, GBP 25,000)   (max 2 children's claims per policy)  [S1]

plus a child funeral benefit of £4,000 on death of a child (max 2 children) [S1].
Children's claims do not reduce `SA` or end the policy [S1] [S4] [S8] [S11]. Exclusions:
conditions present at birth; symptoms before cover start; death within the survival
period; TPD [S1].

**Standalone variant.** Identical chassis minus the death and terminal-illness
benefits: the sum assured pays only on a defined critical illness (plus survival
period) [S11] [S4]. Death of the life assured within the survival period, or death
without a prior CI diagnosis, ends the policy with no payment [S4] [S11] (a
premium-refund-on-death feature exists in some designs [S4] [S11 — recorded jointly in
the research file] and is excluded from the composite **[std]**); the survival period
is therefore a real benefit-reducing decrement in this variant (see technical notes).
All other provisions (additional payments, children's cover, premiums, options) are
unchanged [S4] [S11].

**Premiums, grace and lapse.** Premiums are level and guaranteed for the term [S1]. If
a premium is unpaid, cover continues for a 60-day grace period; if still unpaid the
policy is cancelled without refund and without value [S1] [S4]. There is no surrender
value at any time [S1] [S4] [S5] [unverified as explicit statement]; cancellation inside
the 30-day cooling-off period refunds premiums in full [S1] [S4] [S5].

**Exclusions.** CI policies carry few blanket exclusions; exclusions are embedded per
definition (e.g., cancers below staging thresholds; myocardial injury without
infarction; TIA) [S1] [S3]. Case-specific exclusions appear in the policy schedule
[S1]. The first-year suicide/self-inflicted-death clause applies to the life insurance
element (term chassis) [S1] [S3].

**Misrepresentation.** Claims can be declined for misrepresentation; the proportionate
remedy reduces cover to

    SA' = SA x (premium charged / premium that should have been charged)   [S1]

consistent with the CIDRA 2012 graduated-remedy regime for careless consumer
misrepresentation [REG-R20].

**Headline definitions (ABI-aligned).** The composite adopts the 2022/23 ABI
minimum-standard parameters as implemented in the reference retail wording
[S1] [R2] [R3]: cancer requires positive histological diagnosis of a malignant tumour
with invasion, with staging floors (prostate Gleason ≥7 or ≥ cT2bN0M0; urothelial ≥
T1N0M0; thyroid ≥ T2N0M0; NETs WHO Grade ≥2; GIST AFIP/Miettinen-Lasota moderate/high
risk or UICC/TNM8 stage ≥II) [S1] [R3]; heart attack requires new ECG/imaging changes
plus characteristic troponin rise, excluding myocardial injury without infarction
[S1] [R2]; stroke requires death of brain tissue with deficit lasting ≥24 hours,
excluding TIA [S1]; dementia (including Alzheimer's) of specified severity with MCI
excluded [S1] [R2].

---

## Riders and options

**In scope (modeled or embedded in the base contract):**

- **TPD** — embedded as one of the full-payment conditions (own occupation before 70 /
  Specified Work Tasks 3-of-6); drops off at age 70 with a premium reduction [S1].
  In the model it is part of the aggregate CI incidence basis, not a separate decrement.
- **Additional-payment conditions** — modeled as a non-terminating frequency loading
  (see technical notes) [S1] [S4] [S11].
- **Children's cover** — automatic; modeled as a non-terminating frequency loading
  [S1] [S4].
- **Indexation (increasing cover)** and **guaranteed insurability option** — contract
  features per the term chassis [S1] [S4] [S11]; described, but the base model point is
  level cover with no exercises **[std]**.

**Out of scope (listed for completeness):** waiver of premium [S1] [S4]; family income
benefit shape [S4] [S7]; extra-care cover (cover amount + £50,000 on CI with
severe permanent disability / ADL failure) [S4]; fracture cover (£2,000–£6,000
schedule) [S4] [S11]; global treatment (overseas treatment, 3-year renewals) [S4] [S5];
hospital benefit (£100/night from 8th night) [S4]; joint-life separation options and
replacement cover after a joint-life claim [S1] [S4] [S11]; enhanced condition tiers at
two carriers [S3] [S4] [S5]; an advanced-surgery benefit (payment on joining an NHS
waiting list) [S6]; and the severity-graded plan's severity mechanics, its
claim-uplift, cancer-relapse, dementia and frailty add-ons, and its children's
severity cover [S9] [S10].

---

## Variations across insurers

1. **Payment architecture.** Dominant design (four of the five carriers surveyed): one
   full payment on a 33–46-condition list ending the policy, plus capped non-depleting
   additional payments [S1] [S4] [S11] [S6]. The fifth replaces this with a severity scale
   (historically A–G, 100% down to 5%; currently 25%–100% standard) and multiple claims
   against a depletable or protected plan account [S9] [S10]. Representative choice:
   the dominant design — it is what four of five fetched insurers sell, and it keeps
   the reference model single-decrement for the main benefit.
2. **Additional-payment calibration.** 25% capped £25,000 (three carriers' core tiers)
   → 50% capped £30,000–£35,000 (an enhanced tier, and a fourth carrier) → 100% capped
   £30,000 (an upgraded tier) [S1] [S3] [S4] [S8] [S11]. Chosen: 25%/£25,000 — the core-tier
   calibration common to three insurers.
3. **Two-tier menus.** Core + enhanced tier is now standard (a two-tier menu [S3];
   standard vs upgraded [S4] [S5]; "three levels" at a third carrier per its 2024
   relaunch [unverified — media page not fetched]; a 1X/2X/3X ladder [S9]). Enhanced
   tiers add ~15–20 full-payment conditions and expand partial payments [S3] [S4] [S5].
   Chosen: core tier only; enhanced tiers change the incidence basis, not the
   mechanics.
4. **Survival period.** 14 days (a retail wording and the severity-graded plan) vs 10
   days (two other carriers, and the same retail carrier's intermediary children's
   cover) [S1] [S4] [S8] [S10] [S3]. Chosen: 14 days (footnote 9).
5. **Children's cover.** Always a capped percentage (50%) with per-child and
   per-policy limits; caps £25,000–£50,000; enhanced tiers add congenital-onset
   conditions, pregnancy complications and conversion options [S1] [S3] [S4] [S6] [S8] [S11].
   One carrier makes it optional; three others include it automatically
   [S11] [S1] [S4] [S7]. Chosen: automatic, 50%/£25,000, 2-claim limit (the retail
   calibration in [S1]).
6. **Premium guarantee.** Retail CIC premiums typically guaranteed; reviewable
   variants persist with 5-yearly reviews — unlimited changes at one carrier, ±5%
   tolerance in another's intermediary variant [S1] [S3] [S4] [S5] [S7]. Chosen:
   guaranteed, with the reviewable design documented as a technical-notes module.
7. **Accelerated vs standalone.** Both are sold; the accelerated form is packaged with
   life cover as the mainstream retail proposition [S1] [S8] [S11], while another
   carrier's CI product is a standalone contract [S4]. Chosen: accelerated as base
   (it exercises the combined decrement), standalone as the documented variant with a
   one-line model delta.

---

## Regulatory context

**Prudential — PRA / Solvency UK.** CI business is valued under the PRA Rulebook's
Technical Provisions Part: technical provisions = best estimate + risk margin (rule
2.4), where the best estimate is the probability-weighted average of future cash flows
discounted on the relevant risk-free term structure, gross of reinsurance, including
all cash in- and out-flows required to settle the obligations (rules 3.1–3.2)
[R7] [REG-R1]. The reformed risk margin (rules effective 31/12/2024) uses the
cost-of-capital method with CoC = 4% and a risk-tapering factor λ = 0.9 (floor 0.25)
for long-term business [R7] [REG-R4]. Lapse/surrender assumptions must be realistic and
reflect dependence on future conditions, and obligations are segmented into homogeneous
risk groups (9.1–9.2, 10.1) [R7]. The matching adjustment now sits in its own Rulebook
Part [R7] and is in practice irrelevant to CI term business [unverified].

**Conduct — FCA.** CIC is a non-investment insurance contract, so conduct rules sit in
ICOBS, which applies to distribution and to effecting and carrying out such contracts
(ICOBS 1.1.1R) [R5] [REG-R11]; the "pure protection contract" glossary mapping is
[unverified]. The Consumer Duty (PRIN 2A) requires firms to deliver good outcomes,
including fair value, on retail protection business [R6] [REG-R12]; in-force dates 31
July 2023 (open) / 31 July 2024 (closed) [unverified]. Consumer misrepresentation
remedies follow CIDRA 2012's graduated regime (deliberate/reckless vs careless)
[REG-R20], which the contractual proportionate-remedy formula implements [S1].

**Industry self-regulation — ABI minimum standards.** The ABI Guide (2022, with April
2023 clarifications) sets the minimum condition definitions required to use the CIC
label; the 2021/22 review broadened Alzheimer's to all dementia (with MCI exclusion),
clarified cancer exclusions and excluded myocardial injury from heart attack, with
compliance required for new policies by 31 January 2024 [R2] [R3]. The Guide itself
could not be fetched (Cloudflare challenge) [R1]; its content is triangulated from
[R2] [R3] and implementing wordings [S1] [S11].

**Authorisation classes.** Accelerated CI written with life cover falls in long-term
Class I (life and annuity); standalone CI is typically written as long-term Class IV
(permanent health: defined benefits for incapacity from accident or sickness, of
indefinite duration or running to retirement age, with restricted insurer cancellation
rights) or general classes 1–2 for short-term forms [R4] [REG-R14 for the class
definitions; the mapping of CI products to classes](#uklib-reg-r14) [unverified].

**Tax.** Under FA 2012 Part 2, protection business written post-2012 is non-BLAGAB
long-term business taxed on trade profits (BLAGAB I-E applies to investment life
business, not these contracts) [REG-R17]. At the policyholder level the reference retail
policy is written to remain a qualifying policy compatible with para 19(3) Schedule 15
ICTA 1988 and "cannot be issued or assigned into a trust" [S1]; other insurers' plans
are commonly placed in trust [unverified]. FSCS protects 100% of claim value, with
continuity of cover preferred [S1].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-critical_illness-r1
[R2]: #uklib-critical_illness-r2
[R3]: #uklib-critical_illness-r3
[R4]: #uklib-critical_illness-r4
[R5]: #uklib-critical_illness-r5
[R6]: #uklib-critical_illness-r6
[R7]: #uklib-critical_illness-r7
[REG-R1]: #uklib-reg-r1
[REG-R11]: #uklib-reg-r11
[REG-R12]: #uklib-reg-r12
[REG-R17]: #uklib-reg-r17
[REG-R20]: #uklib-reg-r20
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
