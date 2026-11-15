# Actuarial Guideline XXXV (AG 35) — primary-source extraction from the AP&P Manual (As of March 2026)

- **Status:** Primary-source extraction, 2026-08-06. Everything below is from the guideline text as printed
  on PDF pages 1505–1514 of the manual. Nothing is inferred from secondary sources, and no statement from
  the library's existing second-hand account of AG 35 has been carried forward unless the text supports it.

---

## Source

**Exact printed title.** The guideline is headed on two lines, the second in full capitals: "Actuarial Guideline XXXV" /
"THE APPLICATION OF THE COMMISSIONERS ANNUITY RESERVE METHOD TO EQUITY INDEXED ANNUITIES" (AG35-1, PDF 1505).

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
[REG-R33] [REG-R40].

**Licence caution.** The manual is licensed for personal, non-commercial use only; redistribution or integration "into
any software or other publication" needs written NAIC permission [REG-R73], and that notice covers this appendix too.
Following the library's rule (`references/regulatory-and-actuarial-references.md`, "Licence caution"), this file
**paraphrases** AG 35 in the library's own words and cites each point by printed page (AG35-n), section, Attachment,
step or item number and PDF page. It **quotes only short phrases** — the instrument title, a defined term, an operative
trigger or applicability phrase, a date or clock rule, and the few printed misprints that the ambiguity notes turn on —
in quotation marks with their pinpoint. AG 35 prints no rate or factor tables; its one printed formula is kept, and every
other formula below is written in the library's own symbols. The four tables in this file (page map, method
taxonomy, prescribed assumptions, cross-references) are the library's own summaries, not transcriptions, and the
step-by-step blocks under "Mechanics" restate each printed step in the library's words. The certification forms of
Attachments 3 and 4 are described, not reproduced. Anyone who needs the exact printed wording should read it in the
manual at the pages given.
Revised 2026-10-25: verbatim extracts and transcribed tables replaced by paraphrase and pinpoint citations.

**Reference id.** This document is **R152** in the shared U.S. numbering. Downstream documents cite it as
**[REG-R152]** and should retire the `text not retrieved` / `[unverified]` markers that currently attach to
[REG-R40].

---

## Scope and applicability

The Scope section (AG35-1, PDF 1505) is a single sentence and is the whole of the applicability rule: the guideline
reaches every equity indexed annuity contract that is subject to CARVM, "regardless of the date of issue".

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

- *Deferred* designs give the policyholder two things: interest credited on part of the premiums at no less than a
  guaranteed minimum accumulation rate, and a share of any rise in an equity index (the Background's example is the
  S&P 500). The Background says no product is "typical" but lists features most share — a participation rate
  guaranteed for a year or longer, a cap on how much of the index rise is credited, and a policy term marking the
  period over which the current guarantees hold.
- *Immediate* designs guarantee a minimum annuitization rate and give the chance of higher periodic payments if the
  equity index grows; the design may include a participation rate, cap or term.

**AG 35 therefore covers equity indexed immediate annuities as well as deferred ones.** The library has only
ever discussed AG 35 in a deferred/FIA context. The asymmetry is preserved inside the guideline itself: the
Attachment 4 certification covers "all equity indexed annuity products" (AG35-10), while the Attachment 3
certification is confined to "all equity indexed deferred annuity products" (AG35-9) — because it certifies the
EDIM initial reserve, and EDIM is framed around a deferred contract's term.

**Transition / grandfathering:** none in the text. The nearest thing to transitional machinery is the
*Required Change in Method* rule (below), which is a compliance-failure remedy running on a one-quarter
clock, not a transition.

---

## Mechanics

### The problem AG 35 is solving, and the division of labour with AG 33

The Background states the difficulty precisely (AG35-1): the participation rate, cap and similar contract parameters
are guaranteed for a period, whereas the underlying index's growth carries no guarantee and can go either way. It is
that pairing — fixed parameters, unknown index growth — which the Background says makes applying CARVM to these
products "problematic".

The Background then restates the Standard Valuation Law's definition of CARVM, and the restatement is a useful
independent check on the library's own rendition at `us/regulatory/technical-notes.md`, "Formulaic reserves"
(AG35-1; the guideline's quotation carries its own ellipsis). In the library's words: for each contract year `k`, take
the present value at the valuation date of the future guaranteed benefits — guaranteed nonforfeiture benefits
*included* — less the present value at the valuation date of those future valuation considerations, derived from the
gross considerations the contract requires, that fall due *before* the end of year `k`; the reserve is the greatest
of these excesses. The guaranteed benefits themselves are to be determined on the mortality table (where there is
one) and the interest rate or rates that the contract specifies for determining them. In symbols (the library's):

```
CARVM reserve = max over k of [ PV_val( future guaranteed benefits for year k, incl. nonforfeiture )
                                − PV_val( valuation considerations payable before the end of contract year k ) ]
```

The year-`k` label is the library's. The guideline's quotation shows the "respective contract year" only on the
considerations side; the words that tie each benefit set to its contract year sit inside the guideline's ellipsis,
so the full SVL text [REG-R1] is the authority for that part.

**The single most important structural fact for an implementer: AG 35 does not perform the CARVM
maximisation.** Three of the four computational recipes in Attachment 1 — CARVM-UMV, the MVRM and the BSPM —
close with an identical Step 4: only at that point is a CARVM calculation run, and it should follow AG XXXIII
together with any other regulation or Actuarial Guideline that applies (AG35-5, AG35-6). The fourth, EDIM, ends
differently: its Step 4 simply adds the Fixed and Equity Components, and it reaches CARVM only through its
starting Fixed Component, which is the CARVM-UMV or MVRM formula reserve (EDIM Steps 1 and 4, AG35-6). For the
three Type 2 constructions, AG 35's job is to convert an *unknown future index path* into *deterministic
guaranteed benefit amounts* at each duration; AG 33 then takes the greatest present value across elective paths.
The library's existing statement that AG 35 "does not
replace AG 33 but specifies how the index-linked benefit is brought into the AG 33 calculation" is
**confirmed by the text**, and the confirming sentence is Step 4 of CARVM-UMV, the MVRM and the BSPM (EDIM is tied
to AG 33 through its initial Fixed Component).

### The method taxonomy

The guideline defines two classes and names four calculations (AG35-2, PDF 1506):

| Class | Method | Condition on use |
|---|---|---|
| **Type 1** | **EDIM** — Enhanced Discounted Intrinsic Method | Deemed consistent with CARVM **if** the applicable "Hedged as Required" criteria (Attachment 2) are met and the appointed actuary certifies compliance with each quarterly and annual statement; an uncured failure forces a switch to Type 2 (Required Change in Method, AG35-3) |
| **Type 2** | **CARVM with UMV** — CARVM with Updated Market Values | No hedging condition; requires the Attachment 4 assumption certification |
| **Type 2** | **MVRM** — Market Value Reserve Method | No hedging condition; requires the Attachment 4 assumption certification |
| **Type 2 (adaptation)** | **BSPM** — Black-Scholes Projection Method | "an acceptable adaptation of the MVRM"; recognised, not a separate class |

"Type 1" and "Type 2" are **the guideline's own printed terminology**, used as section headings
("Type 1 Methods", "Type 2 Methods") and in the Required/Optional Change in Method rules.

**The method set is closed for two of the four.** The guideline rules out any departure from the MVRM and EDIM as
Attachment 1 describes them: such variations are not acceptable readings of CARVM (AG35-2). The BSPM is the one
sanctioned variation, and it is a variation on the MVRM specifically. The text says nothing about variations on
CARVM-UMV.

### The "term", the single dominant benefit, and which methods need it

The MVRM and EDIM are both "based on a future value" (and the BSPM, as an MVRM adaptation, with them), so they need
a horizon; the guideline calls fixing the "term" an essential part of both the MVRM and the EDIM (AG35-2). It sets
three cumulative conditions on their use (AG35-2, paraphrased; the numbering is the guideline's):

1. **Single dominant benefit test.** The policy form's design must feature "a single dominant benefit" — the benefit
   the form is most likely to pay. It is identified by weighing product features; the guideline's examples are
   surrender charges, vesting rates, spread deductions, how the guaranteed participation rates run over time, and
   marketing/advertising material. Note the last item: *marketing and advertising material is a prescribed input to
   a statutory reserve determination.*
2. **Terminal point.** The timing of that most-likely single dominant benefit marks the end of the current term —
   both for running the computational method and, where they apply, for testing the "Hedged as Required" criteria.
3. **Prior demonstration.** **Before** the MVRM or EDIM is used, the appointed actuary must have shown that (1) and
   (2) are met, to the satisfaction of the regulators of every state in which the insurer has to file a statutory
   financial statement.

The same "term" then fixes the **time horizon for present value calculations** both for a Type 1 method
(AG35-3) and for the MVRM/BSPM (AG35-3), and fixes the current term of an equity indexed deferred annuity
policy for the "equivalence of characteristics" test under the Hedged as Required criteria (AG35-2/3).

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
        O(t,b) is valued by a suitable option pricing technique; the guideline's examples are Black-Scholes
        and a stochastic scenario method
Step 2  Roll each option value up at the valuation interest rate to that option's own expiry date:
        A(t,b) = O(t,b) · (1 + i_v)^(expiry − valuation date)
Step 3  Future guaranteed benefit at each time point:
        GB(t,b) = F(t,b) + A(t,b)
Step 4  Perform the CARVM calculation on {GB(t,b)}, following AG XXXIII and any other regulation or
        Actuarial Guideline that applies.
```

The index enters as an **addition to the guaranteed benefit stream**, benefit by benefit — not as a separate
reserve component. `i_v` should be consistent with whatever Actuarial Guidelines or regulations apply, the guideline's
named examples being **AG XXXIII and AG IX-B** (CARVM-UMV Step 2, AG35-5).

#### MVRM (Type 2)

```
Step 1  Solve for the projected index level at the end of the term, I(T), such that the benefit at T equals
              contract guarantee at T
            + today's market value of the call option(s) giving a FULL hedge of the index-linked benefit,
              rolled up at the valuation interest rate
        The index is assumed to rise by "equal annual percentage increases".
        The options are those whose maturities coincide ("coterminous") with the dates on which the
        participation rate, spread or other index-benefit basis is set; i_v as for CARVM-UMV (AG XXXIII or
        AG IX-B named as examples); the "term" is the one fixed under the General Requirements.
Step 2  From the current index level I(0) and the projected I(T), calculate the implied compound constant
        growth rate g:
              g = ( I(T) / I(0) )^(1/T) − 1
        and use g to project I(t) at intermediate anniversaries:  I(t) = I(0)·(1 + g)^t
Step 3  Read every annuity benefit off the projected index levels.
Step 4  Perform the CARVM calculation, following AG XXXIII and any other regulation or Actuarial Guideline
        that applies.
```

The index enters as a **single deterministic index path**, calibrated so that the end-of-term benefit
reproduces guarantee-plus-accumulated-option-value. The "equal annual percentage increases" instruction is
what makes it a constant compound growth rate rather than any other shape, and the `g` expression above is
the library's arithmetic restatement of that instruction — **the guideline prints no formula.**

#### MVRM using the Black-Scholes Projection Method (recognised adaptation)

Purpose (AG35-5): the guideline presents it as an adaptation of the basic MVRM for designs that re-set the
participation rate, spread or other crediting basis within the term, especially where the reset is annual — i.e.
the annual-reset and annual-ratchet designs, which are the dominant modern FIA chassis.

```
Step 1  For each successive period p within the term over which the crediting basis is guaranteed:
          c(p) = price of a call option giving a FULL hedge over p, stated as a FRACTION OF ACCOUNT VALUE
          roll c(p) up to the end of p at the RISK-FREE rate (r_f, the library's symbol)
          the rolled-up cost becomes the ASSUMED ACCOUNT-VALUE GROWTH RATE for p:
              AV(end of p) = AV(start of p) · ( 1 + c(p)·(1 + r_f)^len(p) )
        Repeat period by period across the term, reflecting forward interest rates, forward index
        volatility, index dividend levels and the benefit guarantees.
Step 2  On each anniversary, back out the index level that would deliver the projected account value under
        the contract's participation rate, spread or other crediting basis.
        (i.e. INVERT the crediting formula: AV projected first, index level backed out second)
Step 3  Read every annuity benefit off those index levels.
Step 4  Perform the CARVM calculation, following AG XXXIII and any other regulation or Actuarial Guideline
        that applies.
```

The `AV(end of p)` line is the library's arithmetic reading of BSPM Step 1 (AG35-5/6); the guideline states the
step in prose only.

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
  Step 1  at issue    :  FC(0) = formula reserve from EITHER CARVM-UMV OR MVRM
          at end of term: FC(T) = FLOOR of the benefit the insurer is in fact hedging
  Step 2  intermediate values: solve for the interest rate j that accumulates FC(0) to FC(T):
              FC(0)·(1 + j)^T = FC(T)      ⇒      FC(t) = FC(0)·(1 + j)^t
          where the terminal floor may be a WEIGHTED BLEND of benefit floors — see the worked example below

Equity Component
  Step 3  EC(t) = discounted intrinsic value of the options
              = [ intrinsic value of the options at the valuation date ] · (1 + i_v)^−(T − t)
          i.e. measure intrinsic value AS AT THE VALUATION DATE, then discount it at the valuation rate over
          the years still to run until the end of the term.
```

As in the other two methods, `i_v` should be consistent with the applicable Actuarial Guidelines or regulations, with
AG XXXIII and AG IX-B again the named examples (EDIM Step 3, AG35-6).

Note what EDIM is doing: the equity element is measured at **intrinsic value only**, not market value — no
time value — and is then discounted rather than projected. That is what makes it "Discounted Intrinsic", and
it is why the method is available only to an insurer that is actually hedged (the time value the reserve
omits is assumed to be carried by the hedge). The `(1 + j)` accumulation of the Fixed Component is the
"enhancement".

**The guideline's own worked example (EDIM Step 2, AG35-6)** — the only worked illustration of a reserve
calculation in the document (the Attachment 2 Specified Percentage examples size the hedge, not the reserve), and it
is qualitative. It supposes the options were bought on the assumption that, at maturity, 90% of
policyholders surrender and 10% annuitize. The Fixed Component is then built from two pieces: a 90% share of a Fixed
Component growing to the surrender benefit's floor, plus a 10% share of one growing to the annuitization benefit's
floor.

Restated: `FC(t) = 0.90 · FC_surr(t) + 0.10 · FC_ann(t)`, where each sub-component runs its own Step 2
accumulation from its own share of `FC(0)` to its own terminal floor. **The 90/10 split is illustrative and
is tied to the option-purchase assumption, not prescribed.** The general rule the example encodes is that
the terminal floor is a *mixture over the maturity benefit options actually assumed when the hedge was
bought*.

**EDIM's initial-reserve floor.** EDIM does not generate its own `FC(0)`; the guideline plugs the hole
explicitly (AG35-3): for statutory minimum formula reserve purposes, the initial EDIM reserve must be at least
the initial reserve from CARVM with UMV or from the MVRM, with whatever option market values those need
computed on assumptions that were reasonable at the policy's issue date; the insurer must certify that
reasonableness under Attachment 3. **So a Type 1 shop must still be able to run at least one Type 2 method at
issue.** A model build cannot implement EDIM alone.

### Prescribed assumptions for the index element — and what is *not* prescribed

| Element | What the guideline prescribes |
|---|---|
| Option pricing model | **Not prescribed.** CARVM-UMV Step 1 asks only for a suitable pricing technique and offers Black-Scholes or a stochastic scenario method as examples — permissive only (AG35-5) |
| Volatility | **No level prescribed.** Named only as an input to BSPM: "forward index volatility" (AG35-6) |
| Dividend yield | **No level prescribed.** Named only as "index dividend levels" in BSPM (AG35-6) |
| Interest rates for projecting/accumulating option values | The **valuation interest rate** for CARVM-UMV Step 2, MVRM Step 1 and EDIM Step 3; the **risk-free interest rate** for BSPM Step 1. Forward interest rates are a named BSPM input |
| Which valuation interest rate | Should be consistent with the Actuarial Guidelines or regulations that apply, **AG XXXIII and AG IX-B** being the named examples — stated three times, in CARVM-UMV Step 2, MVRM Step 1 and EDIM Step 3 (AG35-5/6) |
| Index path shape (MVRM) | **Prescribed: "equal annual percentage increases in the index"** — a constant compound growth rate, not a stochastic set and not a scenario ensemble (MVRM Step 1, AG35-5) |
| Option maturities (MVRM) | **Prescribed:** maturities must be "coterminous" with the dates on which the participation rate, spread or other index-benefit basis is set (AG35-5) |
| Option strike / payoff (CARVM-UMV) | **Prescribed by identity:** the option is the one that "exactly hedges" the floor, its payoff exactly equalling benefit-minus-floor, "reflecting all relevant contract features" (AG35-5) |
| Mortality and decrements in the reserve | **Not addressed.** AG 35 hands this to CARVM/AG 33 at Step 4. The 3%-per-year elective decrement in Attachment 2 is a *hedge-sizing* limit, not a reserve assumption |
| Assumption discipline generally | Enforced **by certification, not by prescription** — Attachment 3 (reasonableness at issue, EDIM) and Attachment 4 (reasonableness at valuation + consistency with hedge asset statement values) |

### Plan Type and the maximum valuation interest rate

A section the library carries nowhere, and directly implementable (AG35-4, PDF 1508). Whichever method class is used,
the insurer must determine the policy form's Plan Type, because Plan Type is what sets the maximum valuation interest
rate. Then:

- Design features peculiar to equity indexed annuities — the guideline's examples are equity-enhanced surrender
  values, vesting schedules and the participation rate (its wording is ungrammatical; see "Ambiguities in the text as
  printed") — **should not** be used to determine the Plan Type of a policy form. A Plan Type may be assigned only
  on the design features that the NAIC Model SVL itself identifies in Section 4b, Paragraph C.
- The Model SVL's Plan Type A and B definitions speak of an adjustment reflecting changes "in interest rates or asset
  values" since the insurer received the funds. AG 35 rules that the **"asset values" limb does not extend to policy
  value changes caused by movements in the equity index** underlying the policy form.

The practical effect: an FIA's index-linked features are invisible to the Plan Type A/B/C table at
[REG-R1 §4b.C(1)(c)] that `us/regulatory/technical-notes.md` already carries. Plan Type is decided on the
contract's *withdrawal and adjustment* features alone, and the equity kicker cannot be used to argue a
contract into an adjusted-value Plan Type.

### Certification, disclosure and change-of-method rules

**Type 1 (AG35-2/3).** A Type 1 method is deemed consistent with CARVM where the insurer using it complies with
the applicable Hedged as Required criteria **and** provides a certification of compliance, signed by the appointed
actuary, to go with every annual and quarterly statutory statement it files with the insurance regulator of each
state where it does business. Attachment 2 puts
the same duty as a quarterly certification by the appointed actuary (AG35-7). Separately, an EDIM user must file
the **Attachment 3** certification on initial-reserve assumptions, also with each quarterly and annual statement
(AG35-9).

**Type 2 (AG35-3).** No hedging condition. But the **Attachment 4** certification, signed by the appointed
actuary, must be filed with each annual and quarterly statement in each state (AG35-3, AG35-10). It certifies that
the option-value assumptions are (1) reasonable given the economic conditions current at the valuation date, and
(2) consistent with the corresponding assumptions used to set the statement value of any derivatives that hedge
the equity-index obligations embedded in the annuities it covers. **This is a reserve-to-asset consistency
requirement**: the option assumptions inside the reserve must line up with the option assumptions used to carry
the hedge assets on the balance sheet.

**Required Change in Method (AG35-3)** — the compliance-failure ratchet, and the only clock in the document:

```
Type 1 user fails the applicable Hedged as Required criteria for a block
  → the actuarial certification has to REPORT the failure
  → if the cause is still uncorrected "within one quarterly financial reporting" after that first
    disclosure, the insurer MUST switch the block to a Type 2 method for its minimum formula reserves
  → to resume Type 1: show the domiciliary commissioner, to the commissioner's satisfaction, that the
    criteria are met again; obtain that commissioner's approval; and notify the appropriate regulator of
    each state where the insurer does business "subject to the change" of method
```

**Optional Change in Method (AG35-3).** Either direction, with domiciliary-commissioner approval and prior
notification to all other states in which the insurer writes the block. A **Type 2 → Type 1** request to the
domiciliary commissioner has to come with a demonstration that the applicable Hedged as Required criteria are met.

### Attachment 2 — Hedged as Required criteria (the Type 1 gate)

Two alternative sets; the appointed actuary certifies quarterly to one of them.

**"Basic" — for an insurer using long dated options to hedge the embedded equity risk** (the Background at
AG35-1 states this is the intended split).

1. **Equivalence of characteristics** between the option contracts held and the options embedded in the
   products, judged on contract features — the guideline's list runs index, averaging, option type, strike, term
   and so on (AG35-7).
2. **Hedge sizing at issue.** The hedge bought at or around issue must be at least a Specified Percentage of the
   contract's account value at issue. The Specified Percentage varies **by the length of the option guarantee**,
   and the guideline is explicit that on an annual-ratchet product with a multi-year policy term but one-year
   participation-rate guarantees, **"the 'term' for this purpose is 1 year"**. The percentage may build in elective
   benefit decrements of **up to 3% a year**; a higher allowance needs the Commissioner's agreement. The printed
   worked example is a five-year point-to-point product: **`SP% = (1 - .03) ^ 5 = 86%`** (AG35-7, PDF 1511).
   Generalising the example (the guideline prints no general formula): `SP% = (1 − d)^n` with `d ≤ 0.03` and
   `n` = length of the option guarantee in years; `0.97^5 = 0.8587`.
3. A **specific plan** for hedging the risks that interim death benefits, early surrenders and the like create.
4. A **system in place** to monitor the effectiveness of the hedging strategy.
5. A **stated maximum tolerance** for differences between expected and actual hedge performance.

**"Option Replication" — for an insurer using an option replication strategy** (dynamic hedging).

1. Same equivalence-of-characteristics requirement, here between the replication strategy's target ("the target of
   an option replication strategy") and the options embedded in the liabilities.
2. **Quarterly notional test**, and note it is *ongoing* where the Basic version is *at issue*: at every quarter-end
   the replication target's notional amount must be at least the sum, over contracts, of each contract's Specified
   Percentage of its account value (AG35-7). Here the Specified Percentage depends on the option guarantee period
   still **remaining**, with the same 1-year rule for annual ratchet and the same 3%-a-year elective decrement cap.
   Printed example: a point-to-point contract with five years to run takes `SP% = (1 - .03)^5 = 86%` (the
   superscript is lost in the text layer — see artefacts). **Additional allowance not present in the Basic
   criteria:** the insurer may add suitable assumptions for non-elective decrements, mortality for instance, on top
   of the elective decrement assumption.
3. Same specific-plan requirement.
4. Same monitoring-system requirement.
5. **Stated maximum tolerance, with prescribed minimum quantitative requirements** — the only numeric
   compliance thresholds in the guideline (AG35-8, PDF 1512). The layout below is the library's:

```
Compliance evaluation = a RETROSPECTIVE CORRELATION TEST, run AT LEAST WEEKLY.

  D = ( change since the start of the calendar quarter in the market value of the HEDGE PORTFOLIO )
    − ( change over the same span in the market value of the OPTIONS EMBEDDED IN THE LIABILITIES )
  V = market value, at the start of the period, of the liability-embedded options

  Maximum permitted |D|  =  10% of V

  10% < |D| < 25%, for the SECOND TIME in a quarter
      → notify the insurance commissioner of EVERY STATE where the insurer holds a licence
      → the notice gives the dollar amount of reserves hedged under the replication strategy

  |D| > 25% at ANY weekly observation
      → notify the commissioner of every licensing state
      → the notice gives the hedged reserve amount AND the SURPLUS EFFECT of reporting reserves on a
        CARVM-UMV basis

  |D| > 35% at ANY POINT IN TIME in the quarter
      → the insurer is "deemed to be out of compliance", i.e. it has failed the Hedged as Required test
      → notify the commissioner of every licensing state
      → the notice gives the hedged reserve amount AND the surplus effect of a CARVM-UMV reserve basis
```

Note the escalation is not uniform in its trigger language: the 10–25% band triggers on the **second**
occurrence *during a quarter*; the 25% band triggers at **any** weekly interval; the 35% band triggers at
**any point in time** during the quarter, which is wider than the weekly observation grid the test otherwise
runs on. Note also that **CARVM-UMV is the guideline's implicit reference method** — it is what the insurer
must quantify the surplus impact against when the hedge drifts, and it is one of the two permitted bases for
the EDIM initial reserve.

**Drafting Note on over-hedging (AG35-8).** The requirements above address the case where the actual hedge
*underperforms* what was expected. The Note observes that other parts of a state's regulatory framework — its
investment article and its rules on derivative use — may limit how far an insurer can over-hedge. It treats an
insurer as over-hedged when, at a given moment, the hedge portfolio is larger than the liability portfolio it hedges,
and **directs that the surplus hedging instruments be left out of the Item 5 measurements** — i.e. the correlation
test is run on the matched portion only, and over-hedging cannot be used to mask a correlation failure.

### Other regulatory requirements, and asset adequacy

**Supersession (AG35-4).** For statutory minimum formula reserves on equity indexed annuity products, AG 35's
guidance displaces the valuation guidance contained in **Sections 5 and 6 of the NAIC Interest-Indexed Annuity
Contracts Model Regulation**. That model regulation is **not in this library and its text was not supplied**;
recorded here as a cross-reference only. Note the supersession is scoped — it reaches "the valuation guidance" in
those two sections, not the model regulation as a whole.

**Asset Adequacy Testing of Reserves (AG35-4).** The section is a single sentence. It opens with a condition — "To
the extent required by law, regulation, or regulatory requirements" — and only then requires that reserves held for
equity indexed annuity policies undergo adequacy testing on appropriate methods and assumptions.

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
  `us/regulatory/statutory-accounting-and-capital.md` line 219. Confirmed by Step 4 of CARVM-UMV, the MVRM and the
  BSPM, and for EDIM by its Step 1, which takes the initial Fixed Component from the CARVM-UMV or MVRM formula
  reserve.
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

   The text (AG35-4, PDF 1508) makes the testing duty conditional: it applies **"To the extent required by
   law, regulation, or regulatory requirements"**. AG 35 **presupposes** the obligation and points at it; it
   does not create one. The *modelling* conclusion the library draws — that an FIA block
   cannot rely on the formulaic reserve alone and the same cash flow model must serve CARVM and ASOP 22 —
   survives intact, but its authority is **SVL §6.B and VM-30** [REG-R1] [REG-R100], with AG 35 as
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
  annuity"; its Background describes designs that credit part of the premiums at a guaranteed minimum
  interest accumulation rate, which a buffer/floor RILA generally does not have; and it says nothing about
  separate accounts, registered products, index-linked variable annuities, or AG 54. The Scope's second
  limb — "that are subject to CARVM" — is also unresolved for a RILA in the library. **Record the guideline
  as neither including nor excluding RILA**, and keep the RILA CARVM caveat, narrowing it from "AG 35 was not
  retrieved" to "AG 35 was retrieved and does not address this design".
- **Interaction with VM-22 / the Valuation Manual.** The extracted text makes **no mention** of the Valuation
  Manual, VM-22, principle-based reserving, or any post-2000 development. It cannot tell you whether AG 35
  continues to bind an FIA valued under VM-22, nor whether moving off AG 35 is a change in valuation basis.
  [REG-R41] establishes only that VM-C continues to incorporate AG XXXV.
- **Whether AG 35 or AG 33 controls where they conflict.** AG 35 defers to AG XXXIII at Step 4 of CARVM-UMV, the
  MVRM and the BSPM (and, through the initial Fixed Component, for EDIM) but sets its own rules on term, Plan Type
  and benefit construction. No precedence clause is printed.

---

## Citation anchors

Each entry gives the pinpoint (printed page, section, Attachment, step or item, and PDF page) and a one-line
paraphrase; words in quotation marks are short key phrases from the print, with intra-word text-layer spaces
closed, and an ellipsis inside quotation marks is the guideline's own. The entry numbers are this file's own and
are kept stable.

1. **Scope** — AG35-1, *Scope*, PDF 1505: applies to every equity indexed annuity contract subject to CARVM,
   "regardless of the date of issue".
2. **The problem** — AG35-1, *Background*, PDF 1505: guaranteed contract parameters combined with unknown index growth
   make CARVM "problematic" for these products.
3. **Method taxonomy** — AG35-2, *Computational Methods*, PDF 1506: EDIM is the sole Type 1 method; CARVM with UMV and
   the MVRM are Type 2; the BSPM is a recognised adaptation of the MVRM.
4. **Closed method set** — AG35-2, *General Requirements*, PDF 1506: departures from the MVRM and EDIM as Attachment 1
   describes them are not acceptable readings of CARVM; the BSPM is accepted as an MVRM adaptation.
5. **Term determination** — AG35-2, *General Requirements* condition 2, PDF 1506: the timing of the "single dominant
   benefit" most likely to be provided ends the current term.
6. **EDIM initial reserve floor** — AG35-3, *Type 1 Methods*, PDF 1507: the initial EDIM reserve must be at least
   the initial reserve under CARVM with UMV or the MVRM, on option assumptions reasonable at issue.
7. **Required change** — AG35-3, *Required Change in Method*, PDF 1507: a Hedged as Required failure not cured
   "within one quarterly financial reporting" of its first disclosure forces a Type 2 method.
8. **Plan Type exclusion** — AG35-4, *Plan Type*, PDF 1508: policy value changes driven by the equity index are not a
   "change in … asset values" for the SVL's Plan Type A/B definitions.
9. **Supersession** — AG35-4, *Other Regulatory Requirements*, PDF 1508: AG 35's formula-reserve guidance supersedes
   the valuation guidance contained in Sections 5 and 6 of the NAIC Interest-Indexed Annuity Contracts Model
   Regulation.
10. **Asset adequacy, conditional** — AG35-4, *Asset Adequacy Testing of Reserves*, PDF 1508: reserves are to be
    adequacy-tested, but only "To the extent required by law, regulation, or regulatory requirements".
11. **CARVM-UMV option identity** — AG35-5, Attachment 1, CARVM-UMV Step 1, PDF 1509: the call option valued is the
    one that "exactly hedges the floor" of the benefit at that time.
12. **MVRM index path** — AG35-5, Attachment 1, MVRM Step 1, PDF 1509: the projection assumes "equal annual
    percentage increases" in the index.
13. **BSPM rate** — AG35-5/6, Attachment 1, BSPM Step 1, PDF 1509–1510: the period's option cost, as a percentage of
    account value, is rolled up at the "risk-free interest rate" and used as the account value's projected growth.
14. **EDIM equity component** — AG35-6, Attachment 1, EDIM Step 3, PDF 1510: the Equity Component is the "discounted
    intrinsic value" of the options.
15. **Specified Percentage** — AG35-7, Attachment 2, Basic item 2, PDF 1511: the five-year point-to-point example,
    printed as `SP% = (1 - .03) ^ 5 = 86%`.
16. **Correlation tolerance** — AG35-8, Attachment 2, Option Replication item 5, PDF 1512: the two market-value
    changes may differ by at most 10% of the liability-embedded options' market value at the start of the period.
17. **Over-hedge exclusion** — AG35-8, Attachment 2, Drafting Note, PDF 1512: excess hedging instruments are left
    out of the Item 5 measurements.
18. **Attachment 4 consistency limb** — AG35-10, Attachment 4 item 2, PDF 1514: option-value assumptions must be
    consistent with the comparable assumptions behind the statement value of any hedging derivatives.

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
| **Actuarial Guideline XXXIII** (AG 33) | Step 4 of CARVM-UMV, MVRM and BSPM; the valuation-rate consistency clause | [REG-R39], text not read by this pass |
| **Actuarial Guideline IX-B** | The valuation-rate consistency clause, three times | Indexed at [REG-R41] only; text not retrieved |
| **NAIC Model Standard Valuation Law, Section 4b, Paragraph C** | Plan Type determination | [REG-R1]; the A/B/C table is carried at `us/regulatory/technical-notes.md` |
| **NAIC Model SVL, Plan Type A and B definitions** | The "changes in interest rates or asset values" phrase | [REG-R1] |
| **NAIC Interest-Indexed Annuity Contracts Model Regulation, Sections 5 and 6** | Supersession clause | **Not in this library at all.** No R-number, no text |
| **Standard Valuation Law** generally, and the CARVM definition it carries | Background | [REG-R1] |

### Ambiguities in the text as printed

- **AG35-2, *Computational Methods*:** the sentence making Type 1 methods consistent with CARVM ends "if the
  applicable 'Hedged as Required' are met" — the word **criteria** is missing after the quoted phrase. The
  Background one page earlier uses "'Hedged as Required' criteria" in full, so the reading is unambiguous, but the
  omission is in the print (or the text layer) and is noted for fidelity.
- **AG35-2, *General Requirements*:** the sentence calling the "term" determination essential refers to "**both**
  computational methods" — "both" means MVRM and EDIM, the two discussed in the preceding sentences, and the
  paragraph's opening sentence names "The MVRM and EDIM computational methods"; but the *following* paragraph
  extends the conditions to three methods (EDIM, MVRM, BSPM). Whether BSPM independently requires a term
  determination is not stated; it inherits the requirement through the three numbered conditions, which do
  name it.
- **AG35-4, *Plan Type*:** the bar on equity-indexed design features reads "should **not used** to determine" the
  Plan Type — the word **be** is missing. Meaning is clear.
- **AG35-4, *Plan Type*:** the examples are introduced as "such as **an** equity enhanced surrender values" — the
  article disagrees in number with the plural noun. Cosmetic.
- **The escalation triggers in Attachment 2 item 5 are not stated on a uniform basis** — "for a second time
  during a quarter" for the 10–25% band, "at any of the weekly intervals" for the 25% band, "at any point in
  time during the quarter" for the 35% band. The last is broader than the weekly test grid the paragraph
  otherwise establishes, and the guideline does not say how a between-observation breach is detected.
- **Attachment 3 timing tension (AG35-9, PDF 1513).** The certification says the assumptions were reasonable
  given economic conditions "**at the time of issue**" of each policy, yet it is to be filed with **each**
  quarterly and annual statutory financial statement. The certification is therefore re-filed every quarter
  about a fixed historical fact. Not an error, but implementers should not read it as a re-measurement
  obligation.
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
  "Actuarial Guideli ne"-type breaks. These are cosmetic and were closed silently in the short quotations above.
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
