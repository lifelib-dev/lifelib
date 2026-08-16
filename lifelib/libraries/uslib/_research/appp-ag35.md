# Actuarial Guideline XXXV (AG 35) — primary-source extraction from the AP&P Manual (As of March 2026)

- **Status:** Primary-source extraction, 2026-08-06. Everything below is from the guideline text as printed
  on PDF pages 1505–1514 of the manual. Nothing is inferred from secondary sources, and no statement from
  the library's existing second-hand account of AG 35 has been carried forward unless the text supports it.

---

## Source

**Exact printed title.** The guideline is headed on two lines, the second in full capitals:

> Actuarial Guideline XXXV
> THE APPLICATION OF THE COMMISSIONERS ANNUITY RESERVE METHOD TO EQUITY INDEXED ANNUITIES

Note the title says **"Commissioners Annuity Reserve Method"**, not "…Reserve Valuation Method"; the body then
uses "Commissioners Annuity Reserve Valuation Method (CARVM)" in full. The library's R40 title string matches
the print exactly and needs no change.

**Where it sits.** NAIC *Accounting Practices and Procedures Manual*, **Appendix C — Actuarial Guidelines**.
The running headers alternate "AG XXXV Appendix C" (verso) and "Appendix C AG XXXV" (recto). Internal
pagination is **AG35-1 through AG35-10**, mapping one-to-one onto **PDF pages 1505–1514**:

| Internal page | PDF page | Content |
|---|---|---|
| AG35-1 | 1505 | Background; Scope |
| AG35-2 | 1506 | Computational Methods; General Requirements; Type 1 Methods (start) |
| AG35-3 | 1507 | Type 1 Methods (cont.); Type 2 Methods; Required Change in Method; Optional Change in Method |
| AG35-4 | 1508 | Plan Type; Other Regulatory Requirements; Asset Adequacy Testing of Reserves |
| AG35-5 | 1509 | **Attachment 1** — CARVM-UMV; MVRM; MVRM using Black-Scholes Projection Method (start) |
| AG35-6 | 1510 | Attachment 1 (cont.) — BSPM; EDIM |
| AG35-7 | 1511 | **Attachment 2** — Hedged as Required Criteria: Basic; Option Replication (start) |
| AG35-8 | 1512 | Attachment 2 (cont.) — Option Replication item 5; Drafting Note |
| AG35-9 | 1513 | **Attachment 3** — Reasonableness of Assumptions Certification |
| AG35-10 | 1514 | **Attachment 4** — Reasonableness and Consistency of Assumptions Certification |

**The manual's own edition line does not appear on these pages.** The only publisher line carried on every
one of the ten pages is the footer **"© 1999-2026 National Association of Insurance Commissioners"**. The
*As of March 2026* edition designation comes from the manual's cover and front matter as recorded at
[REG-R73], not from the AG 35 pages themselves. **The "1999" in the copyright range is a copyright span, not
an adoption or effective date, and must not be cited as one.**

**Retrieval note.** Free download from `content.naic.org` (catalogue entry "APPM-2026 … Free Download"),
2,117 pages, accessed **2026-08-06**; AG 35 extracted from the local text layer. This supersedes the
library's record of the AP&P Manual as a paid publication whose Appendix C could not be read
[REG-R33][REG-R40]. The NAIC licence caution recorded at [REG-R73] (personal / non-commercial use;
redistribution or integration into software or other publication prohibited without permission) applies to
this appendix too, so this file **paraphrases the mechanics and quotes only short anchors**.

**Reference id.** This document is **R152** in the shared U.S. numbering. Downstream documents cite it as
**[REG-R152]** and should retire the `text not retrieved` / `[unverified]` markers that currently attach to
[REG-R40].

---

## Scope and applicability

The Scope section is a single sentence and is reproduced in full because it is the whole of the
applicability rule (AG35-1, PDF 1505):

> "This Actuarial Guideline applies to all equity indexed annuity contracts, regardless of the date of
> issue, that are subject to CARVM."

Three things follow, and the third is a negative finding the library needs.

1. **The trigger is the contract's character, not its issue year.** "regardless of the date of issue" makes
   AG 35 a *valuation-date* requirement reaching the whole in-force block, the same shape as VM-21/VM-22 and
   the opposite of VM-20's year-of-issue keying.
2. **There is a second, cumulative condition:** the contract must be one "that [is] subject to CARVM". A
   contract outside CARVM's scope is outside AG 35 regardless of how it is indexed.
3. **No effective date is printed anywhere in the ten extracted pages.** No adoption date, no operative
   date, no "effective for valuation dates on or after…", no transition period, no grandfathering clause, no
   phase-in, and no sunset. The only temporal language in the entire guideline is the "regardless of the
   date of issue" clause quoted above. **Any effective date attached to AG 35 elsewhere in the library would
   be an inference from outside this text and must be marked as such.**

**What "equity indexed annuity" means is not defined.** The guideline gives no definitional section. The
Background instead describes the product family narratively, and the description is worth recording because
it is the only boundary marker the text supplies (AG35-1, PDF 1505):

- *Deferred* designs "provide policyholders with a minimum guaranteed interest accumulation rate on a
  portion of all premium payments and a portion of the growth, if any, of an equity based index such as the
  S&P 500", with common features being "a participation rate guaranteed for one or more years, a cap on the
  portion of the index growth that is credited to policyholders, and a policy term which defines a time
  period for which current guarantees are applicable". The Background adds that "there is no 'typical'
  equity indexed product".
- *Immediate* designs "provide policyholders with a minimum guaranteed annuitization rate and an opportunity
  to receive larger periodic payments based on the growth, if any, in an equity index", possibly with a
  participation rate, cap or term.

**AG 35 therefore covers equity indexed immediate annuities as well as deferred ones.** The library has only
ever discussed AG 35 in a deferred/FIA context. The asymmetry is preserved inside the guideline itself: the
Attachment 4 certification covers "all equity indexed annuity products", while the Attachment 3 certification
is confined to "all equity indexed deferred annuity products" — because it certifies the EDIM initial
reserve, and EDIM is framed around a deferred contract's term.

**Transition / grandfathering:** none in the text. The nearest thing to transitional machinery is the
*Required Change in Method* rule (below), which is a compliance-failure remedy running on a one-quarter
clock, not a transition.

---

## Mechanics

### The problem AG 35 is solving, and the division of labour with AG 33

The Background states the difficulty precisely: contract parameters such as participation rate and cap are
guaranteed for a period, but "growth of the underlying index is not. Index growth may be positive or
negative. This combination of guaranteed parameters and unknown equity index growth makes the application of
CARVM to these products problematic" (AG35-1).

The guideline then quotes CARVM from the Standard Valuation Law — and the quotation is a useful independent
check on the library's own rendition at `us/regulatory/technical-notes.md`, "Formulaic reserves". As printed
(AG35-1, the ellipsis is the guideline's own):

> "the greatest of the respective excesses of the present value, at the date of valuation, of the future
> guaranteed benefits, including guaranteed nonforfeiture benefits, … over the present value, at the date of
> valuation, of any future valuation considerations derived from future gross considerations, required by the
> terms of such contract, that become payable prior to the end of such respective contract year. The future
> guaranteed benefits shall be determined by using the mortality table, if any, and the interest rate, or
> rates, specified in such contracts for determining guaranteed benefits."

**The single most important structural fact for an implementer: AG 35 does not perform the CARVM
maximisation.** Every one of the four computational recipes in Attachment 1 ends with the same Step 4 —
"Now a CARVM calculation can be performed. The CARVM calculation should be in accordance with Actuarial
Guideline XXXIII and any other applicable regulations or Actuarial Guidelines." AG 35's job is to convert an
*unknown future index path* into *deterministic guaranteed benefit amounts* at each duration; AG 33 then
takes the greatest present value across elective paths. The library's existing statement that AG 35 "does not
replace AG 33 but specifies how the index-linked benefit is brought into the AG 33 calculation" is
**confirmed by the text**, and the confirming sentence is Step 4 of each method.

### The method taxonomy

The guideline defines two classes and names four calculations (AG35-2, PDF 1506):

| Class | Method | Condition on use |
|---|---|---|
| **Type 1** | **EDIM** — Enhanced Discounted Intrinsic Method | Deemed consistent with CARVM **only if** the applicable "Hedged as Required" criteria (Attachment 2) are met, with quarterly appointed-actuary certification |
| **Type 2** | **CARVM with UMV** — CARVM with Updated Market Values | No hedging condition; requires the Attachment 4 assumption certification |
| **Type 2** | **MVRM** — Market Value Reserve Method | No hedging condition; requires the Attachment 4 assumption certification |
| **Type 2 (adaptation)** | **BSPM** — Black-Scholes Projection Method | "an acceptable adaptation of the MVRM"; recognised, not a separate class |

"Type 1" and "Type 2" are **the guideline's own printed terminology**, used as section headings
("Type 1 Methods", "Type 2 Methods") and in the Required/Optional Change in Method rules.

**The method set is closed for two of the four.** "Variations from the MVRM and EDIM as described in
Attachment 1, are not acceptable interpretations of CARVM" (AG35-2). The BSPM is the one sanctioned
variation, and it is a variation on the MVRM specifically. The text says nothing about variations on
CARVM-UMV.

### The "term", the single dominant benefit, and which methods need it

MVRM, BSPM and EDIM are all "based on a future value" and therefore need a horizon; "Determination of the
'term' is an essential component of both computational methods" (AG35-2, referring to MVRM and EDIM). The
guideline sets three cumulative conditions on their use (AG35-2, paraphrased; the numbering is the
guideline's):

1. **Single dominant benefit test.** The policy form must feature "a single dominant benefit which is the
   most likely benefit to be provided under the policy form", determined "based on a consideration of product
   features such as the pattern of guaranteed participation rates, surrender charges, vesting rates, spread
   deductions, and marketing/advertising material". Note the last item: *marketing and advertising material
   is a prescribed input to a statutory reserve determination.*
2. **Terminal point.** "The point in time associated with the single dominant benefit most likely to be
   provided under the contract is used as the terminal point of the current term" — both for applying the
   computational method and for complying with the "Hedged as Required" criteria where applicable.
3. **Prior demonstration.** The appointed actuary must have demonstrated compliance with (1) and (2) "to the
   satisfaction of the regulatory officials in each state in which the insurer is required to submit a
   statutory financial statement", **prior to** using MVRM or EDIM.

The same "term" then fixes the **time horizon for present value calculations** under both Type 1 methods
(AG35-3) and the MVRM/BSPM (AG35-3), and fixes the "current term" used to test "equivalence of
characteristics" under the Hedged as Required criteria (AG35-2).

**CARVM-UMV is exempt from all of this.** The General Requirements section names only "The EDIM, MVRM and the
BSPM adaptation of the MVRM"; CARVM-UMV needs no term, no single dominant benefit, and no prior regulator
demonstration. This is a first-order model-design consequence: CARVM-UMV requires an option valuation on a
full *duration × benefit* grid, while MVRM/EDIM require one term election and one index path.

### Attachment 1 — the four constructions

Symbol definitions are the library's, introduced to make the steps executable; the guideline itself uses
prose throughout and defines **no symbols at all**.

Let `t` index durations, `b` index the benefits available at a duration, `T` be the end of the "term",
`i_v` be the applicable valuation interest rate, `I(t)` the index level, `AV(t)` the account value, and
`F(t,b)` the **guaranteed floor** of benefit `b` at `t`.

#### CARVM-UMV (Type 2)

```
Step 1  For each duration t and each benefit b at which an index-based benefit is available:
        O(t,b) = market value of the call option that EXACTLY hedges the floor of that benefit, i.e. the
                 option whose payoff exactly equals  [ benefit b available at t, reflecting all relevant
                 contract features ]  −  F(t,b)
        O(t,b) is valued "using an appropriate option pricing technique, such as Black-Scholes or a
        stochastic scenario method"
Step 2  Accumulate each option market value forward at the applicable valuation interest rate to the point
        in time at which that option would expire:
        A(t,b) = O(t,b) · (1 + i_v)^(expiry − valuation date)
Step 3  Future guaranteed benefit at each time point:
        GB(t,b) = F(t,b) + A(t,b)
Step 4  Perform the CARVM calculation on {GB(t,b)}, in accordance with AG XXXIII and any other applicable
        regulations or Actuarial Guidelines.
```

The index enters as an **addition to the guaranteed benefit stream**, benefit by benefit — not as a separate
reserve component. `i_v` "should be consistent with the requirements of any applicable Actuarial Guidelines
or regulations, such as **Actuarial Guideline XXXIII or Actuarial Guideline IX-B**".

#### MVRM (Type 2)

```
Step 1  Solve for the projected index level at the end of the term, I(T), such that the benefit at T equals
              contract guarantee at T
            + current market value of the call option(s) that would FULLY hedge the index-based benefit,
              accumulated at the appropriate valuation interest rate
        "This calculation should be performed assuming equal annual percentage increases in the index."
        The call options used are those "with maturity dates coterminous with the setting of participation
        rates, spread, or any other method of determining index-based benefits."
Step 2  From the current index level I(0) and the projected I(T), calculate the implied compound constant
        growth rate g:
              g = ( I(T) / I(0) )^(1/T) − 1
        and use g to project I(t) at intermediate anniversaries:  I(t) = I(0)·(1 + g)^t
Step 3  Determine all annuity benefits from the projected index levels.
Step 4  Perform the CARVM calculation, in accordance with AG XXXIII and any other applicable regulations or
        Actuarial Guidelines.
```

The index enters as a **single deterministic index path**, calibrated so that the end-of-term benefit
reproduces guarantee-plus-accumulated-option-value. The "equal annual percentage increases" instruction is
what makes it a constant compound growth rate rather than any other shape, and the `g` expression above is
the library's arithmetic restatement of that instruction — **the guideline prints no formula.**

#### MVRM using the Black-Scholes Projection Method (recognised adaptation)

Purpose, verbatim in substance: an adaptation "to accommodate products for which the participation rate,
spread, or any other benefit determination method is redetermined during the term (particularly annually)"
(AG35-5/6) — i.e. the annual-reset and annual-ratchet designs, which are the dominant modern FIA chassis.

```
Step 1  For each successive period p within the term, over which the benefit determination is guaranteed:
          c(p) = cost of a FULL hedging call option, expressed as a PERCENTAGE OF THE ACCOUNT VALUE, for
                 the period the benefit determination is guaranteed
          accumulate c(p) to the end of that period at the RISK-FREE INTEREST RATE
          use the accumulated percentage cost as the PROJECTED GROWTH RATE OF THE ACCOUNT VALUE during p
        Repeat for each successive period "giving recognition to the benefit guarantees, forward interest
        rates, forward index volatility, and index dividend levels."
Step 2  Determine the index level that would produce the projected account level on each anniversary, on
        the basis of the participation rate, spread, or other benefit determination method used.
        (i.e. INVERT the crediting formula: AV projected first, index level backed out second)
Step 3  Determine all annuity benefits from the index levels.
Step 4  Perform the CARVM calculation, in accordance with AG XXXIII and any other applicable regulations or
        Actuarial Guidelines.
```

**Two differences from the base MVRM that an implementer will get wrong if not flagged.** (a) BSPM
accumulates the option cost at the **risk-free interest rate**, whereas CARVM-UMV Step 2, MVRM Step 1 and
EDIM Step 3 all use the **valuation interest rate**. The guideline uses "risk-free" only here. (b) BSPM
projects the **account value** first and derives the index level from it (Step 2 inverts the crediting
formula); MVRM projects the **index** first and derives benefits from it. The direction of the mapping is
reversed.

#### EDIM (Type 1)

```
Reserve = Fixed Component + Equity Component                                              (Step 4)

Fixed Component
  Step 1  at issue    :  FC(0) = the formula reserve produced by EITHER CARVM-UMV OR MVRM
          at end of term: FC(T) = the FLOOR of the benefit actually being hedged
  Step 2  intermediate values: solve for the interest rate j that accumulates FC(0) to FC(T):
              FC(0)·(1 + j)^T = FC(T)      ⇒      FC(t) = FC(0)·(1 + j)^t
          where the terminal floor may be a WEIGHTED BLEND of benefit floors — see the worked example below

Equity Component
  Step 3  EC(t) = discounted intrinsic value of the options
              = [ intrinsic value of the options at the valuation date ] · (1 + i_v)^−(T − t)
          i.e. take the intrinsic value AT THE VALUATION DATE and discount at the valuation rate for the
          number of years from the valuation date to the end of the term.
```

`i_v` again "should be consistent with the requirements of any applicable Actuarial Guidelines or
regulations, such as Actuarial Guideline XXXIII or Actuarial Guideline IX-B" (AG35-6).

Note what EDIM is doing: the equity element is measured at **intrinsic value only**, not market value — no
time value — and is then discounted rather than projected. That is what makes it "Discounted Intrinsic", and
it is why the method is available only to an insurer that is actually hedged (the time value the reserve
omits is assumed to be carried by the hedge). The `(1 + j)` accumulation of the Fixed Component is the
"enhancement".

**The guideline's own worked example (EDIM Step 2, AG35-6)** — the only worked illustration in the whole
document, and it is qualitative:

> "assume you purchase options assuming that 90% of policyholders will surrender at maturity, and that 10%
> of policyholders will annuitize at maturity. The Fixed Component is the sum of (1) 90% of the Fixed
> Component that grows to the floor of the surrender benefit; and (2) 10% of the Fixed Component that grows
> to the floor of the annuitization benefit."

Restated: `FC(t) = 0.90 · FC_surr(t) + 0.10 · FC_ann(t)`, where each sub-component runs its own Step 2
accumulation from its own share of `FC(0)` to its own terminal floor. **The 90/10 split is illustrative and
is tied to the option-purchase assumption, not prescribed.** The general rule the example encodes is that
the terminal floor is a *mixture over the maturity benefit options actually assumed when the hedge was
bought*.

**EDIM's initial-reserve floor.** EDIM does not generate its own `FC(0)`; the guideline plugs the hole
explicitly (AG35-3): the initial reserve under EDIM "must be set at least equal to the initial reserve
produced by either CARVM with UMV, or the MVRM with assumptions used to compute any necessary option market
values reasonable as of the date of issue of the policy", with the Attachment 3 certification as to
reasonableness. **So a Type 1 shop must still be able to run at least one Type 2 method at issue.** A model
build cannot implement EDIM alone.

### Prescribed assumptions for the index element — and what is *not* prescribed

| Element | What the guideline prescribes |
|---|---|
| Option pricing model | **Not prescribed.** "an appropriate option pricing technique, such as Black-Scholes or a stochastic scenario method" — permissive examples only (AG35-5) |
| Volatility | **No level prescribed.** Named only as an input to BSPM: "forward index volatility" (AG35-6) |
| Dividend yield | **No level prescribed.** Named only as "index dividend levels" in BSPM (AG35-6) |
| Interest rates for projecting/accumulating option values | The **valuation interest rate** for CARVM-UMV Step 2, MVRM Step 1 and EDIM Step 3; the **risk-free interest rate** for BSPM Step 1. Forward interest rates are a named BSPM input |
| Which valuation interest rate | Must be "consistent with the requirements of any applicable Actuarial Guidelines or regulations, such as **Actuarial Guideline XXXIII or Actuarial Guideline IX-B**" — stated three times, once per method that needs it |
| Index path shape (MVRM) | **Prescribed: "equal annual percentage increases in the index"** — a constant compound growth rate, not a stochastic set and not a scenario ensemble |
| Option maturities (MVRM) | **Prescribed:** "those with maturity dates coterminous with the setting of participation rates, spread, or any other method of determining index-based benefits" |
| Option strike / payoff (CARVM-UMV) | **Prescribed by identity:** the option must "exactly hedge" the floor, its payoff exactly equalling benefit-minus-floor, "reflecting all relevant contract features" |
| Mortality and decrements in the reserve | **Not addressed.** AG 35 hands this to CARVM/AG 33 at Step 4. The 3%-per-year elective decrement in Attachment 2 is a *hedge-sizing* limit, not a reserve assumption |
| Assumption discipline generally | Enforced **by certification, not by prescription** — Attachment 3 (reasonableness at issue, EDIM) and Attachment 4 (reasonableness at valuation + consistency with hedge asset statement values) |

### Plan Type and the maximum valuation interest rate

A section the library carries nowhere, and directly implementable (AG35-4, PDF 1508). Either method class
"requires a determination of Plan Type for purposes of determining the maximum valuation interest rate", and:

- Design features unique to equity indexed annuities — **"an equity enhanced surrender values, vesting
  schedules, or participation rate"** (sic; see artefacts) — **may not** be used to determine the Plan Type of
  a policy form. "Only those design features specifically identified in Section 4b. Paragraph C of the NAIC
  Model SVL may be used to assign a Plan Type to a policy form."
- The Plan Type A and B definitions in the Model SVL include the phrase "with an adjustment to reflect
  changes in interest rates or asset values since receipt of the funds by the insurance company…". AG 35
  rules that **"The reference to 'change in … asset values' does not include changes in policy values due to
  changes in the equity index underlying the policy form."**

The practical effect: an FIA's index-linked features are invisible to the Plan Type A/B/C table at
[REG-R1 §4b.C(1)(c)] that `us/regulatory/technical-notes.md` already carries. Plan Type is decided on the
contract's *withdrawal and adjustment* features alone, and the equity kicker cannot be used to argue a
contract into an adjusted-value Plan Type.

### Certification, disclosure and change-of-method rules

**Type 1 (AG35-2/3).** The insurer must comply with the applicable Hedged as Required criteria **and**
provide a certification of compliance, signed by the appointed actuary, "with each annual and quarterly
statutory financial statement filed with the appropriate insurance regulatory official in each state in which
the insurer does business". Attachment 2 states the same obligation as "the appointed actuary needs to
certify quarterly". Separately, an EDIM user files the **Attachment 3** certification on initial-reserve
assumptions, also with each quarterly and annual statement.

**Type 2 (AG35-3).** No hedging condition. But the **Attachment 4** certification, signed by the appointed
actuary, is filed with each annual and quarterly statement in each state, covering (1) reasonableness of the
option-value assumptions "in light of current relevant economic conditions as of the date of valuation" and
(2) consistency of those assumptions "with the comparable assumptions used to determine the statement value
of any derivative instruments used to hedge the equity indexed based obligations embedded in the equity
indexed annuities subject to this certification". **This is a reserve-to-asset consistency requirement**: the
option assumptions inside the reserve must line up with the option assumptions used to carry the hedge assets
on the balance sheet.

**Required Change in Method (AG35-3)** — the compliance-failure ratchet, and the only clock in the document:

```
Type 1 user fails the applicable Hedged as Required criteria
  → the required actuarial certification MUST DISCLOSE the failure
  → if the reason is not corrected within ONE QUARTERLY FINANCIAL REPORTING of the initial disclosure,
    the insurer MUST use a Type 2 computational method for that block
  → to resume Type 1: demonstrate to the domiciliary commissioner's satisfaction that the criteria are being
    met, obtain the domiciliary commissioner's approval, and notify the regulatory official in each state in
    which the insurer does business subject to the change
```

**Optional Change in Method (AG35-3).** Either direction, with domiciliary-commissioner approval and prior
notification to all other states in which the insurer writes the block. A **Type 2 → Type 1** request "must
be accompanied with a demonstration of compliance with the applicable 'Hedged as Required' criteria".

### Attachment 2 — Hedged as Required criteria (the Type 1 gate)

Two alternative sets; the appointed actuary certifies quarterly to one of them.

**"Basic" — for an insurer using long dated options to hedge the embedded equity risk** (the Background at
AG35-1 states this is the intended split).

1. **Equivalence of characteristics** between the option contracts held and the options embedded in the
   products, "with respect to specific contract features such as: Index, averaging features, option type,
   strike price, term, etc."
2. **Hedge sizing at issue.** "The amount of hedge purchased, at or near the contract issuance, must be
   greater than or equal to a Specified Percentage of the product's account value, at contract issuance."
   The Specified Percentage varies **by the length of the option guarantee**, and the guideline is explicit
   that on an annual-ratchet product with a multi-year policy term but one-year participation-rate
   guarantees, **"the 'term' for this purpose is 1 year"**. It "allows the company to assume no more than
   **3% per year** of elective benefit decrements, unless the Commissioner agrees to a higher limit". Worked
   example as printed: "for a five-year point-to-point product, the Specified Percentage would be:
   **SP% = (1 - .03) ^ 5 = 86%**". Generalising the example (the guideline prints no general formula):
   `SP% = (1 − d)^n` with `d ≤ 0.03` and `n` = length of the option guarantee in years; `0.97^5 = 0.8587`.
3. A **specific plan** for hedging risks associated with interim death benefits, early surrenders, etc.
4. A **system in place** to monitor the effectiveness of the hedging strategy.
5. A **stated maximum tolerance** for differences between expected and actual hedge performance.

**"Option Replication" — for an insurer using an option replication strategy** (dynamic hedging).

1. Same equivalence-of-characteristics requirement, between "the target of an option replication strategy
   employed" and the embedded options.
2. **Quarterly notional test**, and note it is *ongoing* where the Basic version is *at issue*: "At the end
   of each quarter, the notional amount of the target of the option replication strategy must be greater than
   or equal to the sum of the Specified Percentages of each contract's account value." Here the Specified
   Percentage "varies by the length of the **remaining** option guarantee", same 1-year rule for annual
   ratchet, same 3%-per-year elective decrement cap. Printed example: a point-to-point contract with five
   years remaining takes `SP% = (1 - .03)^5 = 86%` (the superscript is lost in the text layer — see
   artefacts). **Additional allowance not present in the Basic criteria:** "Appropriate assumptions for
   non-elective decrements such as mortality may be added to the assumption for elective decrements."
3. Same specific-plan requirement.
4. Same monitoring-system requirement.
5. **Stated maximum tolerance, with prescribed minimum quantitative requirements** — the only numeric
   compliance thresholds in the guideline (AG35-8, PDF 1512):

```
Compliance evaluation = a RETROSPECTIVE CORRELATION TEST, performed AT LEAST WEEKLY.

  D = ( change in the market value of the HEDGE PORTFOLIO from the beginning of the calendar quarter )
    − ( change in the market value of the OPTIONS EMBEDDED IN THE LIABILITY PORTFOLIO over the same period )
  V = beginning-of-period market value of the options embedded in the liabilities

  Maximum permitted |D|  =  10% of V

  10% < |D| < 25%, occurring for a SECOND TIME during a quarter
      → notify the Commissioner of Insurance in EACH STATE in which the insurer is licensed
      → the notification must state the dollar amount of reserves being hedged by the option replication
        strategy

  |D| > 25% at ANY of the weekly intervals
      → notify the Commissioner in each state in which licensed
      → the notification must state the dollar amount of reserves being hedged AND the IMPACT ON SURPLUS OF
        REPORTING THE RESERVES BASED ON THE CARVM-UMV

  |D| > 35% at ANY POINT IN TIME during the quarter
      → the insurer is DEEMED TO BE OUT OF COMPLIANCE with the "Hedged as Required" criteria
      → notify the Commissioner in each state in which licensed
      → the notification must state the dollar amount of reserves being hedged AND the impact on surplus of
        reporting the reserves based on the CARVM-UMV
```

Note the escalation is not uniform in its trigger language: the 10–25% band triggers on the **second**
occurrence *during a quarter*; the 25% band triggers at **any** weekly interval; the 35% band triggers at
**any point in time** during the quarter, which is wider than the weekly observation grid the test otherwise
runs on. Note also that **CARVM-UMV is the guideline's implicit reference method** — it is what the insurer
must quantify the surplus impact against when the hedge drifts, and it is one of the two permitted bases for
the EDIM initial reserve.

**Drafting Note on over-hedging (AG35-8).** The requirements above address the case where the actual hedge
*underperforms*. An insurer's ability to over-hedge "may be constrained by other components of a state's
regulatory framework including the state's investment article and regulations concerning the use of
derivative instruments". Over-hedged means "that at a particular point in time, the hedge portfolio exceeds
the portfolio of liabilities being hedged". **If over-hedged, "the excess hedging instruments are excluded
from the measurements required in Item 5"** — i.e. the correlation test is run on the matched portion only,
and over-hedging cannot be used to mask a correlation failure.

### Other regulatory requirements, and asset adequacy

**Supersession (AG35-4).** "The guidance provided in this Actuarial Guideline concerning statutory minimum
formula reserves for equity indexed annuity products supersedes the valuation guidance in **Sections 5 and 6
of the NAIC Interest-Indexed Annuity Contracts Model Regulation**." That model regulation is **not in this
library and its text was not supplied**; recorded here as a cross-reference only. Note the supersession is
scoped — it reaches "the valuation guidance in Sections 5 and 6", not the model regulation as a whole.

**Asset Adequacy Testing of Reserves (AG35-4), in full — it is one sentence:**

> "To the extent required by law, regulation, or regulatory requirements, reserves established for equity
> indexed annuity policies must be tested for adequacy using appropriate methods and assumptions."

**Read the opening clause.** This is a *conditional* provision that defers to whatever other law imposes the
requirement; it is not a free-standing AG 35 mandate. See "What this settles for the library" below — this is
the extraction's single most consequential correction.

---

## What this settles for the library

### Confirmed

- **The exact title at [REG-R40].** "Actuarial Guideline XXXV — The Application of the Commissioners Annuity
  Reserve Method to Equity Indexed Annuities" matches the print. The VM-C-index verification recorded at
  [REG-R41] was correct. No change needed to the title string anywhere.
- **AG 35 layers on AG 33 rather than replacing it** — `references/regulatory-and-actuarial-references.md`
  R39/R40 annotations, `products/fixed_indexed_annuity/product-spec.md` §"Statutory valuation", and
  `us/regulatory/statutory-accounting-and-capital.md` line 219. Confirmed by Step 4 of all four methods.
- **AG 35 does not reach a book-value MYGA** — `products/fixed_deferred_annuity/technical-notes.md` line
  639. Confirmed on primary authority: Scope is limited to "equity indexed annuity contracts … subject to
  CARVM", and a MYGA is not index-linked. The claim can drop from inference to text.
- **Certification and notification requirements attach to method choice and method change** — R40 annotation.
  Confirmed and now specified: quarterly + annual certifications, Attachments 3 and 4, the one-quarter
  correction clock, domiciliary-commissioner approval plus all-states notification on any change.
- **CARVM as rendered in `us/regulatory/technical-notes.md` lines 75–78.** AG 35's Background quotes the SVL
  definition and it matches the library's construction on both traps the library flags — guaranteed
  nonforfeiture benefits are *included* in the benefit leg, and the considerations deducted are those payable
  *before* the end of the contract year in question.

### Contradicted or materially qualified — four corrections

1. **"Type 1" / "Type 2" are not industry shorthand.** [REG-R40]'s annotation says AG 35 offers "alternative
   method families (industry shorthand 'Type 1' / 'Type 2')". They are **the guideline's own section headings
   and defined terms**. Delete "industry shorthand" and the surrounding hedging. Same for
   `_research/fixed-indexed-annuity.md` line 973.

2. **The asset adequacy requirement is conditional, and the library states it unconditionally.** Three places
   assert that AG 35 *requires* equity-indexed annuity reserves to be asset-adequacy tested:
   - `references/regulatory-and-actuarial-references.md` line 194 — "binding in part because AG 35
     expressly requires equity-indexed annuity reserves to be asset-adequacy tested";
   - the [REG-R40] annotation — "**requiring that equity-indexed annuity reserves be asset-adequacy tested**
     [unverified — from a practitioner presentation, not the guideline text]";
   - `products/fixed_indexed_annuity/technical-notes.md` line 694 — "AG 35 is reported to require
     equity-indexed annuity reserves to be asset-adequacy tested … [unverified]";
   - and `_research/regulatory-actuarial-annuities.md` line 64 in the same terms.

   The text is **"To the extent required by law, regulation, or regulatory requirements, reserves … must be
   tested for adequacy using appropriate methods and assumptions."** AG 35 **presupposes** the obligation and
   points at it; it does not create one. The *modelling* conclusion the library draws — that an FIA block
   cannot rely on the formulaic reserve alone and the same cash flow model must serve CARVM and ASOP 22 —
   survives intact, but its authority is **SVL §6.B and VM-30** [REG-R1][REG-R100], with AG 35 as
   corroboration rather than as the source. Rewrite the three sentences to say AG 35 *directs that reserves
   be tested to the extent other law requires it*, and re-anchor the binding force on [REG-R100].

3. **AG 35 covers immediate as well as deferred equity indexed annuities.** Every library mention treats AG 35
   as an FIA (deferred accumulation) item. The Background devotes a paragraph to equity indexed *immediate*
   annuity products with a minimum guaranteed annuitization rate. The `products/immediate_annuity/` and
   `products/deferred_income_annuity/` files should at minimum record that AG 35 reaches an index-linked
   payout design, even though the library's representative SPIA and DIA are not index-linked.

4. **The retrievability caveats are now wrong for AG 35.** All of the following state or imply that the AG 35
   text could not be obtained and must be cited second-hand, and all should be revised to cite **[REG-R152]**:
   - `README.md` lines 104, 155, 185;
   - `references/regulatory-and-actuarial-references.md` lines 833–834, 1009–1024 (the R40 entry), 1741,
     3243;
   - `us/regulatory/statutory-accounting-and-capital.md` lines 29, 218–219, 225–228, 243–244, 640, 698;
   - `us/regulatory/technical-notes.md` lines 80 and 453 ("AG 33 and AG 35 are the interpretive layers and
     **their texts were not retrieved**" / "the interpretive guidance — AG 33 and AG 35 — was **not
     retrievable**");
   - `us/regulatory/sources.md` lines 664, 717 ff.;
   - `products/fixed_indexed_annuity/technical-notes.md` lines 567–570, 605, 694, 720, 740;
   - `products/fixed_indexed_annuity/product-spec.md` lines 520–521 and `sources.md` lines 230–233, 266,
     271;
   - `products/registered_index_linked_annuity/technical-notes.md` line 677 and `sources.md` lines 293–294;
   - `products/fixed_deferred_annuity/technical-notes.md` line 639 and `sources.md` line 313;
   - `_research/fixed-indexed-annuity.md` lines 972–975, 1321–1327, 1811, 1989.

   **AG 33 is a separate document and this extraction says nothing about it** — every joint "AG 33 and AG 35
   were not retrieved" sentence must be split, not deleted.

### Now answerable where the library previously had a hole

- **`products/fixed_indexed_annuity/technical-notes.md` line 605** — "How the index feature itself enters
  is **AG 35's subject and unretrieved** … expose both bases rather than choosing in code." The answer is now
  available and the "expose both bases" instruction turns out to be *right for the wrong reason*: AG 35 does
  not choose between a guaranteed-basis and a declared-basis roll-forward. It supplies **four** distinct
  constructions, and the choice among them is a company election gated on hedging (Type 1) or on
  certification (Type 2), reversible only with regulator approval. The model must be able to run at least
  **CARVM-UMV or MVRM** in all cases, because EDIM's initial reserve is defined by reference to one of them.
- **Plan Type** (`us/regulatory/technical-notes.md`, "Valuation interest rate"). The library carries the
  SVL §4b.C(1)(c) Plan Type A/B/C table but has no rule for how an indexed contract is classified. AG 35
  supplies it: index-linked features are excluded from the Plan Type determination, and index-driven policy
  value changes are not the "changes in … asset values" of the Plan Type A/B definitions.
- **The valuation-rate cross-reference chain.** AG 35 points the valuation interest rate at **AG XXXIII or
  AG IX-B**. [REG-R41] already records AG IX-B in the VM-C index but the library never connects it to
  indexed annuities. An FIA CARVM run has to resolve AG IX-B, not just AG 33.
- **Interim death benefits and early surrenders** are named as hedge-plan obligations (Attachment 2 items 3
  in both criteria sets) — a concrete tie between the library's FIA elective-path enumeration and the
  hedging condition.

### Left open — do not resolve from this text

- **RILA / ILVA.** `products/registered_index_linked_annuity/technical-notes.md` line 677 calls AG 35
  "equity-indexed CARVM" and says the RILA interim-value interaction is "precisely the interaction those
  unread guidelines would govern". **AG 35 does not settle this.** It defines no term "equity indexed
  annuity"; its Background describes designs carrying "a minimum guaranteed interest accumulation rate on a
  portion of all premium payments", which a buffer/floor RILA generally does not have; and it says nothing
  about separate accounts, registered products, index-linked variable annuities, or AG 54. The Scope's second
  limb — "that are subject to CARVM" — is also unresolved for a RILA in the library. **Record the guideline
  as neither including nor excluding RILA**, and keep the RILA CARVM caveat, narrowing it from "AG 35 was not
  retrieved" to "AG 35 was retrieved and does not address this design".
- **Interaction with VM-22 / the Valuation Manual.** The extracted text makes **no mention** of the Valuation
  Manual, VM-22, principle-based reserving, or any post-2000 development. It cannot tell you whether AG 35
  continues to bind an FIA valued under VM-22, nor whether moving off AG 35 is a change in valuation basis.
  [REG-R41] establishes only that VM-C continues to incorporate AG XXXV.
- **Whether AG 35 or AG 33 controls where they conflict.** AG 35 defers to AG XXXIII at Step 4 of every
  method but sets its own rules on term, Plan Type and benefit construction. No precedence clause is printed.

---

## Quotable anchors

Verbatim, with PDF page. Intra-word spaces introduced by the PDF text layer have been closed; nothing else is
altered. Ellipses marked `…` are the guideline's own.

1. **Scope, entire** — "This Actuarial Guideline applies to all equity indexed annuity contracts, regardless
   of the date of issue, that are subject to CARVM." (PDF 1505)
2. **The problem** — "This combination of guaranteed parameters and unknown equity index growth makes the
   application of CARVM to these products problematic." (PDF 1505)
3. **Method taxonomy** — "The following computational method is considered a Type 1 method: the Enhanced
   Discounted Intrinsic Method (EDIM)." (PDF 1506)
4. **Closed method set** — "Variations from the MVRM and EDIM as described in Attachment 1, are not
   acceptable interpretations of CARVM. The BSPM is considered an acceptable adaptation of the MVRM."
   (PDF 1506)
5. **Term determination** — "The point in time associated with the single dominant benefit most likely to be
   provided under the contract is used as the terminal point of the current term…" (PDF 1506)
6. **EDIM initial reserve floor** — "the initial reserve under EDIM must be set at least equal to the initial
   reserve produced by either CARVM with UMV, or the MVRM…" (PDF 1507)
7. **Required change** — "If the reason for failing the 'Hedged as Required' criteria is not corrected within
   one quarterly financial reporting of the initial disclosure … the insurer must use a Type 2 computational
   method…" (PDF 1507)
8. **Plan Type exclusion** — "The reference to 'change in … asset values' does not include changes in policy
   values due to changes in the equity index underlying the policy form." (PDF 1508)
9. **Supersession** — "…supersedes the valuation guidance in Sections 5 and 6 of the NAIC Interest-Indexed
   Annuity Contracts Model Regulation." (PDF 1508)
10. **Asset adequacy, conditional** — "To the extent required by law, regulation, or regulatory requirements,
    reserves established for equity indexed annuity policies must be tested for adequacy using appropriate
    methods and assumptions." (PDF 1508)
11. **CARVM-UMV option identity** — "The appropriate call option is one that exactly hedges the floor of the
    benefit at that point in time." (PDF 1509)
12. **MVRM index path** — "This calculation should be performed assuming equal annual percentage increases in
    the index." (PDF 1509)
13. **BSPM rate** — "accumulate the percentage to the end of that period at the risk-free interest rate, and
    use the accumulated percentage cost as the projected growth rate of the account value during the period."
    (PDF 1509–1510)
14. **EDIM equity component** — "The Equity Component is equal to the discounted intrinsic value of the
    options." (PDF 1510)
15. **Specified Percentage** — "for a five-year point-to-point product, the Specified Percentage would be:
    SP% = (1 - .03) ^ 5 = 86%." (PDF 1511)
16. **Correlation tolerance** — "The maximum dollar amount of difference permitted between these two changes
    is 10% of the beginning of period market value of the options embedded in the liabilities." (PDF 1512)
17. **Over-hedge exclusion** — "If over-hedged, the excess hedging instruments are excluded from the
    measurements required in Item 5 of the Hedged as Required Criteria." (PDF 1512)
18. **Attachment 4 consistency limb** — assumptions must be "consistent with the comparable assumptions used
    to determine the statement value of any derivative instruments used to hedge the equity indexed based
    obligations…" (PDF 1514)

---

## Gaps and caveats

### What the document does not address

- **No effective date, adoption date, operative date, transition, phase-in, grandfathering or sunset.** The
  only temporal language is "regardless of the date of issue". Anything dated attached to AG 35 in this
  library must come from outside this text and be marked as such. The `© 1999-2026` footer is a copyright
  span.
- **No definition of "equity indexed annuity."** No treatment of RILA / ILVA, index-linked separate account
  contracts, buffers, floors, or registered products. No mention of AG 54 or of separate accounts at all.
- **No mention of the Valuation Manual, VM-22, VM-21, or principle-based reserving** in any form.
- **No numerical reserve example.** The EDIM 90/10 illustration is the only worked passage and is
  arithmetically qualitative. No factor tables, no rate tables, no parameter values other than the 3%
  decrement cap and the 10%/25%/35% correlation thresholds.
- **No prescribed volatility, dividend yield, risk-free curve, or option pricing model.** Assumption
  discipline is delegated entirely to appointed-actuary certification.
- **No symbols, no algebraic notation.** Every method is prose. The formula renderings in "Mechanics" above
  are the library's restatement of prose steps and are labelled as such; only `SP% = (1 - .03) ^ 5 = 86%` is
  printed as a formula in the guideline.
- **No printed certification form for Hedged as Required compliance.** The Type 1 section requires "a
  certification as to compliance with the criteria" signed by the appointed actuary, but the only two forms
  printed are Attachment 3 (EDIM initial-reserve reasonableness) and Attachment 4 (Type 2 reasonableness and
  consistency). There is no Attachment for the HaR certification itself.
- **No precedence rule** where AG 35 and AG 33 might conflict.
- **No guidance on aggregation, grouping, or seriatim requirements**; no reinsurance treatment; no tax
  treatment; no interaction with AVR/IMR or the derivative accounting in SSAP No. 86.

### Cross-references to material not supplied

Recorded as references only; **their content is not asserted here**.

| Cross-reference | Where | Library status |
|---|---|---|
| **Actuarial Guideline XXXIII** (AG 33) | Step 4 of all four methods; the valuation-rate consistency clause | [REG-R39], text not read by this pass |
| **Actuarial Guideline IX-B** | The valuation-rate consistency clause, three times | Indexed at [REG-R41] only; text not retrieved |
| **NAIC Model Standard Valuation Law, Section 4b, Paragraph C** | Plan Type determination | [REG-R1]; the A/B/C table is carried at `us/regulatory/technical-notes.md` |
| **NAIC Model SVL, Plan Type A and B definitions** | The "changes in interest rates or asset values" phrase | [REG-R1] |
| **NAIC Interest-Indexed Annuity Contracts Model Regulation, Sections 5 and 6** | Supersession clause | **Not in this library at all.** No R-number, no text |
| **Standard Valuation Law** generally, and the CARVM definition it carries | Background | [REG-R1] |

### Ambiguities in the text as printed

- **AG35-2:** "Type 1 computational methods are deemed to be consistent with CARVM if the applicable 'Hedged
  as Required' are met." — the word **criteria** is missing after the quoted phrase. The Background one page
  earlier uses "'Hedged as Required' criteria" in full, so the reading is unambiguous, but the omission is in
  the print (or the text layer) and is noted for fidelity.
- **AG35-2:** "Determination of the 'term' is an essential component of **both** computational methods" —
  "both" refers to MVRM and EDIM, which are the two discussed in the preceding two sentences; but the
  paragraph's opening sentence names "The MVRM and EDIM computational methods", and the *following* paragraph
  extends the conditions to three methods (EDIM, MVRM, BSPM). Whether BSPM independently requires a term
  determination is not stated; it inherits the requirement through the three numbered conditions, which do
  name it.
- **AG35-4:** "Design features unique to equity indexed annuities … should **not used** to determine the Plan
  Type" — the word **be** is missing. Meaning is clear.
- **AG35-4:** "such as **an** equity enhanced surrender values, vesting schedules, or participation rate" —
  the article disagrees in number with the plural noun. Cosmetic.
- **The escalation triggers in Attachment 2 item 5 are not stated on a uniform basis** — "for a second time
  during a quarter" for the 10–25% band, "at any of the weekly intervals" for the 25% band, "at any point in
  time during the quarter" for the 35% band. The last is broader than the weekly test grid the paragraph
  otherwise establishes, and the guideline does not say how a between-observation breach is detected.
- **Attachment 3 timing tension.** The certification concerns assumptions "reasonable in light of the
  relevant economic conditions prevalent **at the time of issue** of each policy", yet it "must be filed in
  conjunction with **each** quarterly and annual statutory financial statement". The certification is
  therefore re-filed every quarter about a fixed historical fact. Not an error, but implementers should not
  read it as a re-measurement obligation.
- **Attachment 3 vs Attachment 4 scope mismatch.** Attachment 3 covers "equity indexed **deferred** annuity
  products"; Attachment 4 covers "all equity indexed annuity products". Consistent with EDIM being framed on
  a deferred contract's term, but the guideline does not say what an EDIM user with an equity indexed
  *immediate* annuity certifies.

### Extraction artefacts in the supplied text layer

The PDF text layer is irregular and the following were observed and corrected in this file; they are recorded
so a future reader comparing against a fresh extraction is not surprised.

- **Lost superscript.** Attachment 2, Option Replication item 2 (PDF 1511) renders as
  `SP% = (1 - .03)` / newline / `5 = 86%`. The exponent 5 has dropped out of line. The Basic criteria one
  item earlier print the same formula intact as `SP% = (1 - .03) ^ 5 = 86%`, and `0.97^5 = 0.8587 ≈ 86%`
  confirms the reading. **No guessing was required, but the raw text is misleading on first read.**
- **Irregular intra-word spaces throughout**, from justified two-column-era typesetting: "Actuarial Guide
  line", "th e", "pr oduct", "i ndex", "re serve", "co mputational", "hedgi ng", "to lerance", "in terest",
  "prov ide", "disco unted", "charac teristics", "notifica tion", "financ ial", "the insure r does business",
  "Actuarial Guideli ne"-type breaks. These are cosmetic and were closed silently in the quotations above.
- **Bullet glyphs lost.** The three escalation clauses in Attachment 2 item 5 (PDF 1512) are bulleted in the
  original; the text layer renders the bullets as leading whitespace. The three-clause structure is
  unambiguous from the text.
- **Signature blocks** in Attachments 3 and 4 render as runs of underscores with parenthetical labels; they
  carry no content.
- **Running headers and the copyright footer are interleaved with body text** at every page boundary, which
  is why the page-marker structure of the supplied file matters for citation.
- **No content appears to be missing.** The ten pages run continuously AG35-1 → AG35-10, each section closes
  before the next opens, and both certification attachments terminate in signature blocks. There is no
  evidence of a truncated table or dropped paragraph.
