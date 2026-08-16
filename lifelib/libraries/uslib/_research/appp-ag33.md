# Actuarial Guideline XXXIII (AG 33) — primary-source extraction from the AP&P Manual (As of March 2026)

- **Status:** Primary-source extraction, 2026-08-06. Everything below comes from the eight extracted
  pages of the guideline itself unless explicitly flagged otherwise. Where this note compares the
  guideline against what the library already says, the library side carries its own [REG-R#].
- **Reference id assigned to the document read here: R151.** This is a *new* entry, not a
  replacement of R39. R39 is the pre-existing "AG 33, title-only, not fetched" record; R151 is the
  guideline **as printed in the AP&P Manual, As of March 2026**, read in full. R39's annotation
  needs the corrections in "What this settles for the library" below.

---

## Source

**Exact printed title.** The guideline's opening page prints the designation and the title on
separate lines, both as shown:

> Actuarial Guideline XXXIII
>
> DETERMINING CARVM RESERVES
> FOR ANNUITY CONTRACTS WITH ELECTIVE BENEFITS

(PDF p. 1496 / printed page AG33-1. The title is set in two lines as printed; it reads as the single
title "Determining CARVM Reserves for Annuity Contracts With Elective Benefits".)

**Where it sits.** The running heads on every page after the first alternate between
`AG XXXIII    Appendix C` (verso, PDF pp. 1497, 1499, 1501, 1503) and `Appendix C    AG XXXIII`
(recto, PDF pp. 1498, 1500, 1502), so the guideline sits in **Appendix C — Actuarial Guidelines**.
The library's existing record that Appendix C is carried in **Volume II** of the manual comes from
the statutory-accounting research stream [REG-R73], **not** from these pages: the extracted pages
carry no volume statement.

**Printed pagination.** Printed page numbers run **AG33-1 through AG33-8**, corresponding to **PDF
pages 1496–1503** of the manual.

**Edition and copyright line.** Every one of the eight pages carries the footer

> © 1999-2026 National Association of Insurance Commissioners

The **"As of March 2026"** edition line is the manual's own, taken from the retrieval of the whole
volume [REG-R73]; **it does not appear on the extracted AG 33 pages**, which show only the copyright
footer above. The `1999-2026` copyright range is a range on the *manual*, not evidence about AG 33's
own adoption or amendment history — the extracted pages contain **no amendment history, no adoption
note and no revision log** (see "Gaps and caveats", which matters for the effective-date correction
below).

**Retrieval note.** The NAIC *Accounting Practices and Procedures Manual, As of March 2026* is a
**free download from content.naic.org**; it was retrieved in full (2,117 pages) and accessed
**2026-08-06**. This supersedes the library's earlier record of the manual as a paid publication
that could not be fetched [REG-R33], which is what caused AG 33 to be cited by title only [REG-R39].
The AP&P licence terms recorded elsewhere in the library (personal, non-commercial, no integration
into software or other publication without permission) are unaffected by the price and still apply
[REG-R73].

**Structure as printed** (use these headings when citing; the guideline numbers its sections
independently inside each of three blocks, so "Section 2" is ambiguous without the block name):

| Block | Sections |
|---|---|
| **Background Information** (pp. AG33-1 to AG33-2) | 1 Introduction; 2 Annuitization Benefits; 3 Application of Incidence Rates in CARVM; 4 Integrated Benefit Stream Approach; 5 Valuation Interest Rates |
| **Purpose** (p. AG33-3) | unnumbered, three sentences |
| **Definitions** (pp. AG33-3 to AG33-4) | 1 Elective and Non-Elective Benefits in CARVM; 2 Elective and Non-Elective Incidence Rates in CARVM; 3 Integrated Benefit Stream |
| **Text** (pp. AG33-4 to AG33-8) | 1 Greatest Present Value; 2 Examples of Integrated Benefit Streams That Must Be Considered (A Cash Value Streams, B Annuitization Streams, C Other Elective Benefit Streams); 3 Determination of Valuation Interest Rates; 4 Determination of Guarantee Duration and Plan Type (A, B, C, plus the GLIB example); 5 Change in Fund Basis; 6 Purchase Rates; 7 Practical Considerations |
| **Effective Date** (p. AG33-8) | unnumbered, one paragraph |

The *Background Information* block is explanatory: it states the problem each *Text* section then
resolves. Nothing in Background imposes a requirement on its own; the operative requirements are in
*Purpose*, *Definitions*, *Text* and *Effective Date*.

---

## Scope and applicability

### The applicability sentence, verbatim

> This Actuarial Guideline shall apply to all annuity contracts subject to CARVM, where any elective
> benefits (as defined below) are available to the contract owner under the terms of the contract.

(p. AG33-3 / PDF p. 1498, *Purpose*.)

Three things follow that the library needs, and each is load-bearing:

1. **The trigger is the presence of elective benefits, not the product type.** There is no product
   list, no account-value threshold, no premium threshold and no size test anywhere in the
   guideline. A contract subject to CARVM with **no** elective benefit is outside the applicability
   sentence — and the *Definitions* block expressly contemplates such a contract, classing as
   non-elective the "benefits payable under either a deferred or immediate annuity contract (with or
   without life contingencies), where no benefit options are available under the terms of the
   contract" (p. AG33-3).
2. **"All annuity contracts subject to CARVM"** — the scope rides on CARVM's own scope, which AG 33
   does not restate by SVL section number (see "Interaction with the Standard Valuation Law" below).
3. It is an **interpretation, not a new method.** Verbatim:

> The purpose of this Actuarial Guideline is to codify the basic interpretation of CARVM and does
> not constitute a change of method or basis from any previously used method, by clarifying the
> assumptions and methodologies which will comply with the intent of the SVL.

(p. AG33-3.) The library already records — from IRS Rev. Rul. 2002-6 — that the IRS declined to
follow this characterisation for tax purposes under IRC §807(f); that ruling is a separate document
and nothing here confirms or disturbs it.

### Carve-out for separate life or health riders, verbatim

> However, life or health insurance riders attached to an annuity contract, where all components of
> the rider (e.g., premiums, benefits, contract charges, accumulation values and other components)
> are separate and distinct from the components of the annuity contract, should be treated as a
> separate life or health insurance contract not subject to this Actuarial Guideline.

(p. AG33-3.) The test is **separateness of all components**, not the rider's label. Note the mirror
statement in Background 1: the SVL's annuity standards reach "any annuity riders or endorsements,
and any or all components of which, such as premiums, benefits, contract charges, primary or
secondary accumulation values or other components" (p. AG33-1). So a rider whose components are
entangled with the annuity's stays inside AG 33; only a fully self-contained life/health rider
leaves.

### Precedence over AG 33, verbatim

> While this Actuarial Guideline applies to all annuity contracts subject to CARVM, in the event an
> actuarial guideline or regulation dealing with reserves is developed for a specific annuity
> product design, the product specific actuarial guideline or regulation will take precedence over
> the Actuarial Guideline.

(p. AG33-3.) This is the general-versus-specific rule and it settles the *direction* of the AG 33 /
AG 35 and AG 33 / AG 43 relationships without naming either: a product-specific guideline wins. AG
33 **names no other guideline anywhere in the extracted text** — not AG 35, not AG 43, not AG IX,
not AG XIII.

### Effective date and grade-in, verbatim and in full

> This guideline shall be effective on December 31, 1998, affecting all contracts issued on or after
> January 1, 1981. A company may request a grade-in period for contracts issued prior to December
> 31, 1998 from the domiciliary commissioner upon satisfactory demonstration that the method and
> level of current reserves held for such contracts are adequate in the aggregate. This phase-in
> will require establishment of no less than 33 1/3% of the additional reserves resulting from the
> application of this guideline on December 31, 1998, no less than 66 2/3% on December 31, 1999, and
> 100% by December 31, 2000.

(p. AG33-8 / PDF p. 1503. This is the entire *Effective Date* block; there is nothing else.)

**This contradicts the date the library currently carries.** The library records AG 33 as "effective
December 31, **1995**, for all contracts issued on or after January 1, 1981", sourced from IRS
Rev. Rul. 2002-6, and under the title "Determining Minimum Commissioners Annuities Reserve Valuation
Method (CARVM) Reserves for Individual Annuity Contracts". The manual as of March 2026 prints a
**different effective date (December 31, 1998)** and a **different title**. Both differences are
facts about the two documents; the extracted pages give **no** amendment history, so the obvious
reading — that the guideline was revised after 1995 and the manual prints the revised text and its
own effective date — is an **inference, not something this source states**. Record it as: the
current printed text says 1998; Rev. Rul. 2002-6 said 1995 of a differently-titled instrument; the
reconciliation is unsourced. The library must stop presenting the 1995 date and the old title as the
current guideline's.

**Grade-in mechanics worth noting for a model.** The phase-in is (a) **by request**, to the
**domiciliary** commissioner, (b) conditioned on demonstrating existing reserves "are adequate in
the aggregate", (c) applied to **the additional reserves resulting from the application of this
guideline**, not to the whole reserve, and (d) fully run off by December 31, 2000 — so it has **no
live effect on any current valuation** and matters only to historical reconstruction. Note also the
literal wording "contracts issued prior to December 31, **1998**" for eligibility, against an
effective date of that same day; the guideline does not resolve contracts issued exactly on
December 31, 1998.

**No other dates appear in the guideline.** There is no sunset, no re-effective date, no
transition onto VM-22 or VM-21, and no cross-reference to the Valuation Manual operative date.

---

## Mechanics

### 0. Notation used in this section

AG 33 contains **no algebra whatsoever** — no formulas, no symbols, no tables and no numeric
factors except the 7% expense allowance in *Text* 6 and the phase-in percentages in *Effective
Date*. Any symbolic restatement below is the library's own notation, marked **[std, restatement]**,
and is placed next to the guideline's own words so the two can be told apart.

### 1. The two benefit categories — the classification every contract must pass through

Verbatim, the mandatory sorting step (p. AG33-3):

> For purposes of determining reserves under CARVM, each benefit available under the annuity
> contract must be placed into one of the two categories defined as follows:

**Non-Elective Benefits**, verbatim:

> Benefits that are payable to contract owners or beneficiaries only after the occurrence of a
> contingent or scheduled event independent of a contract owner's election of an option specified in
> the contract, including (but not limited to) death benefits, accidental death benefits, disability
> benefits, nursing home benefits, and benefits payable under either a deferred or immediate annuity
> contract (with or without life contingencies), where no benefit options are available under the
> terms of the contract.

**Elective Benefits**, verbatim:

> Benefits that do not fall under the non-elective benefits category (i.e., benefit options that may
> be freely elected under the terms of the contract). Elective benefits include (but are not limited
> to) full surrenders, partial withdrawals, and full and partial annuitizations.

So the taxonomy is a **complement**: elective is defined as "not non-elective". The enumerated lists
are both non-exhaustive ("including (but not limited to)").

**The judgement clause**, verbatim (p. AG33-3):

> In some cases it may not be clear whether some benefits are elective or non-elective. The presence
> of certain types of non-elective benefits may affect other non-elective benefits and/or elective
> benefits. The Valuation Actuary should use judgment in making these determinations by considering
> factors such as the degree to which contract owner actions would be influenced by the availability
> of each benefit in the contract.

Note the criterion: **influence on contract owner behaviour**, not the accounting or product
label. This is the guideline's only stated tie-breaker.

For an implementer this is a **per-benefit flag on the product definition**, set once, driving
everything downstream: which incidence assumption is legal (section 2 below), whether the benefit
enters stream `A` or stream `B` of the integrated benefit stream (section 3), and which Plan
Type / guarantee duration rule sets its valuation rate (section 6).

### 2. Incidence assumptions — completely different rules on the two sides

**Non-elective side**, verbatim (p. AG33-3):

> For non-elective benefits, incidence rates from tables prescribed by the SVL should be applied to
> determine the payment of non-elective benefits and to discount, for survivorship, all benefit
> payments included in an Integrated Benefit Stream, as defined below. If no incidence tables are
> prescribed by the SVL, then company or industry experience (with margins for conservatism) may be
> used, as appropriate. Annuity mortality tables prescribed by the SVL should be used to determine
> all mortality based benefits under the contract (including, but not limited to, annuitizations and
> death benefits) and to discount other types of benefit payments for survivorship.

Three separate rules are packed in there and should be implemented separately:

- **(2a) Prescribed table where one exists.** Non-elective incidence uses the SVL-prescribed table.
- **(2b) Fallback where none exists.** "Company or industry experience (**with margins for
  conservatism**)". The guideline does not quantify the margin. Nursing home and disability
  incidence normally fall here.
- **(2c) Survivorship discounting is universal.** The **SVL-prescribed annuity mortality table**
  discounts *every* payment in *every* integrated benefit stream for survivorship — including the
  purely elective surrender and withdrawal streams. A cash-value stream is **not** valued on a
  mortality-free basis under AG 33.

**A hard cut-off on non-mortality non-elective incidence**, verbatim (p. AG33-4):

> Actuarial judgment should be used as to the appropriateness of applying any non-elective incidence
> rates other than mortality. For non-elective waiver-of-surrender-charge benefits other than
> mortality-based benefits and for similar non-elective benefits, incidence rates greater than zero
> are not to be applied at any time in the projection after the earlier of: (a) the end of the
> surrender charge period applicable immediately after the first premium is paid; and (b) when the
> projected cash value has been depleted.

**[std, restatement]** For a non-mortality non-elective waiver-type benefit, incidence
`ι(t) = 0` for all `t > T`, where

```
T = min( SCP1 , T_depletion )
SCP1        = end of the surrender charge period applicable immediately after the FIRST premium is paid
T_depletion = first projection time at which the projected cash value has been depleted
```

Two implementation traps in that one sentence. **SCP1 is fixed at first premium** — a later premium
that restarts or extends a surrender charge schedule does **not** extend `T`. And the rule is
**earlier of**, so a contract whose cash value depletes inside the surrender charge period cuts off
at depletion. This is the guideline's most mechanical, least ambiguous instruction and is trivially
codeable.

**Elective side**, verbatim (p. AG33-4):

> For elective benefits, incidence rates should not be based on tables reflecting past company
> experience, industry experience or other expectations. Instead, every potential guaranteed
> elective benefit stream required to be reserved by CARVM must be considered in the determination
> of integrated benefit streams as defined below. This is accomplished by considering trial sets of
> guaranteed elective benefit incidence rates, either through numerical testing or analytical means,
> to determine which trial set produces the "greatest present value" as described in Text paragraph
> 1 below. Theoretically, this means that all possible elective benefit incidence rates between 0%
> and 100% should be considered. However, in practice, such a greatest present value will typically
> occur by assuming an incidence rate of either 0% or 100%.

This is the **prohibition** the library has been missing: **experience-based lapse, withdrawal and
annuitization assumptions are illegal in a CARVM valuation**. The elective assumption is not an
assumption at all — it is a **decision variable maximised over**. The "typically 0% or 100%"
sentence is the guideline's own practical observation, phrased as a typicality, **not** as a
permission to restrict the search: the requirement remains that all rates between 0% and 100% be
considered, tempered only by *Text* 7 (below), which requires the actuary to **consider**, not
necessarily **test**, every stream.

### 3. The integrated benefit stream — the object being valued

Verbatim (p. AG33-4):

> An integrated benefit stream is one potential blend of guaranteed elective and non-elective
> benefits available under the contract, determined as the combination of A and B, where:
>
> A equals one potential stream of one or more types of guaranteed elective benefits available under
> the terms of the contract, based upon a chosen set of elective benefit incidence rates; and
>
> B equals the stream of all guaranteed non-elective benefits provided under the terms of the
> contract, recognizing the guaranteed elective benefit stream under consideration in A above, and
> the non-elective incidence rates defined in 2. above.
>
> Both A and B above should be discounted for survivorship, based on the non-elective incidence
> rates defined in 2. above.

Read the structure carefully, because it is asymmetric and the asymmetry is the whole point:

- **A varies; B is determined by A.** There is exactly one `B` per `A`. `B` is not a separate
  candidate stream to be maximised over — it is the non-elective stream *conditional on* the elective
  path already chosen ("recognizing the guaranteed elective benefit stream under consideration in A
  above"). So a projected death benefit must be computed **on the account value that the chosen
  elective path leaves behind**, not on a standalone roll-forward.
- **The search space is over elective incidence sets only.** One integrated benefit stream = one
  chosen set of elective incidence rates.
- **A is a blend across benefit types**, not one benefit type at a time: "one or more types of
  guaranteed elective benefits".
- **Survivorship discounting applies to both legs**, on the non-elective incidence rates.

**[std, restatement]** For a candidate elective incidence set `e` (a vector over benefit types and
times) at valuation date τ:

```
IBS(e)  = A(e) ⊕ B(e)                       one integrated benefit stream
A(e)    = guaranteed ELECTIVE benefit payments implied by e
B(e)    = guaranteed NON-ELECTIVE benefit payments, computed on the contract state that A(e) leaves,
          using the SVL-prescribed non-elective incidence rates
both legs survivorship-discounted on the SVL-prescribed annuity mortality
```

### 4. The greatest present value — the reserve itself

Verbatim, *Text* 1 in full (p. AG33-4):

> All guaranteed benefits potentially available under the terms of the contract must be considered
> in the valuation process and analysis and the ultimate policy reserve held must be sufficient to
> fund the greatest present value of all potential integrated benefit streams, reflecting all
> guaranteed elective and non-elective benefits available to the contract owner. Each integrated
> benefit stream available under the contract must be individually valued and the ultimate reserve
> established must be the greatest of the present values of these values, based on valuation
> interest rate(s) as defined in Section 3 below.

Note the plural in "valuation interest **rate(s)**" and its cross-reference to *Text* 3 — a single
integrated benefit stream can be discounted at **more than one rate**, one per benefit component.
That is the single most important structural fact in the guideline for a model, and section 6 below
makes it explicit.

**[std, restatement]**, in the notation of `us/regulatory/technical-notes.md`:

```
V_CARVM(τ) = max over e of  PV( IBS(e) )
PV( IBS(e) ) = Σ over payments p in A(e) ⊕ B(e) of
                   payment(p) · survivorship(p) · v_{rate(p)}(time(p))
rate(p) = the valuation interest rate for the BENEFIT COMPONENT that payment p belongs to,
          per Text 3 and Text 4 (contract-level parameters A,B,C; benefit-level D,E)
```

The guideline states the maximisation over **streams**; it does **not** restate the SVL's
"end of each respective contract year" indexing, nor does it mention the deduction of future
valuation considerations. Both remain governed by the SVL text itself [REG-R1 §5a.B]; AG 33's
Background 1 paraphrases the deduction but the *Text* block never returns to it. **This is a real
seam** — see "Gaps and caveats".

### 5. The three mandatory stream families

*Text* 2, "Examples of Integrated Benefit Streams That Must Be Considered" (p. AG33-5). The heading
says "Examples" but the body says "mandatory" twice; treat A and B as required and C as a catch-all.

**A. Cash Value Streams** — verbatim:

> One mandatory set of integrated benefit streams for a deferred annuity with cash settlement values
> which must always be considered is any possible blend of future guaranteed partial withdrawals and
> full surrenders available under the contract, as specified in the SVL, accumulated at the
> guaranteed credited interest rate(s) and discounted at the valuation rate(s) of interest defined in
> section 3 below, with appropriate recognition of all guaranteed non-elective benefits available
> under the contract.

**The accumulate-at-guaranteed / discount-at-valuation split is stated explicitly here.** This
directly confirms the construction the library already uses in
`us/regulatory/technical-notes.md`, "Formulaic reserves", Worked example 2 (roll the account
forward at the guaranteed credited rate, discount at the valuation rate). Note also **"any possible
blend of ... partial withdrawals and full surrenders"** — the elective search space is not
"surrender at each duration k"; it is every combination of partial withdrawal amounts and timings
followed by a surrender.

**B. Annuitization Streams** — verbatim:

> A second mandatory set of integrated benefit streams that must be considered is any possible blend
> of future guaranteed full or partial annuitization elections, as specified in the SVL, available to
> the contract owner at each election date required by CARVM, with appropriate recognition of all
> guaranteed non-elective benefits available under the terms of the contract. In determining the
> integrated benefit streams to value the annuitization option, the guaranteed purchase rates
> contained in the contract, as well as any other contract provisions, excluding any current purchase
> rates which may be applicable, are applied to the accumulation fund.

Three operative points: **guaranteed purchase rates** (not current) drive the annuitization stream;
they are applied to the **accumulation fund** (defined term — see below); and **partial**
annuitizations are in scope, so the search space includes streams that annuitize part of the fund and
leave the rest to be surrendered or withdrawn.

**"Accumulation fund" is a defined term**, given in Background 2 (p. AG33-1), verbatim:

> For purposes of this Actuarial Guideline, "accumulation fund" is defined as the policy value which
> is used to purchase an annuity option under the terms of the contract.

The definitional point Background 2 is making is that this value **may exceed the cash value**:
"Varying forms of contracts provide that the cash value available to the contract owner is less than
the amount available to purchase an annuitization option under the terms of the contract." A model
that carries only one account value cannot value the annuitization stream correctly; it needs the
**annuitization basis** as a separate state variable.

**C. Other Elective Benefit Streams** — verbatim:

> In addition to the cash value and annuitization streams described above, all other possible
> guaranteed elective benefits available under the contract, including blends of more than one type
> of guaranteed elective benefit, must be considered in a manner consistent with the mandatory cash
> value and annuitization streams, with appropriate recognition of all guaranteed non-elective
> benefits available under the contract.

This is the residual clause that pulls in guaranteed living-benefit elections, elective enhanced
withdrawal provisions, elective commutation and the like. **"Blends of more than one type"** is
stated a third time; it is plainly not an oversight.

### 6. Valuation interest rates — contract-level vs benefit-level parameters

*Text* 3 (pp. AG33-5 to AG33-6). Verbatim:

> Section 4b of the SVL determines valuation rates for an annuity contract based on the following
> Parameters:
>
> A. The basis of valuation (issue year or change in fund);
>
> B. Whether or not the annuity provides for cash settlement options;
>
> C. Whether interest is guaranteed on premiums received more than 12 months following issue (or the
> valuation date for change in fund basis);
>
> D. The guarantee duration; and
>
> E. The Plan Type.
>
> Parameters A, B and C above should be determined at a contract level. Additional requirements
> regarding the change in fund basis of valuation are set forth in Section 5 below. Parameters D and
> E should be determined at a benefit level, as set forth in Section 4 below.

and the definition of the two levels, verbatim:

> Under a contract level determination, parameters are set based on the characteristics of the
> contract as a whole. Under a benefit level determination, parameters are set based on the
> characteristics of each benefit, resulting in potentially different valuation rates for each
> benefit type comprising the integrated benefit stream.

**This is the answer to "how do elective and non-elective benefits take different valuation rates".**
The split is not elective-vs-non-elective as such; it is:

| SVL §4b parameter | Level | Consequence |
|---|---|---|
| A — issue year vs change in fund | **contract** | one basis for the whole contract, and (per *Text* 5) it must be applied consistently to every portion of every integrated benefit stream |
| B — cash settlement options present | **contract** | one answer per contract |
| C — interest guaranteed on premiums received >12 months after issue | **contract** | one answer per contract |
| D — guarantee duration | **benefit** | varies by benefit component *and*, for annuitization, by assumed annuitization date |
| E — Plan Type | **benefit** | A / B / C determined per benefit component |

So the rate varies **within** an integrated benefit stream, by benefit component and by payment. The
library's existing SVL §4b Plan Type A/B/C weighting-factor table and change-in-fund increments in
`us/regulatory/technical-notes.md`, "Formulaic reserves", are the machinery AG 33 is pointing at
[REG-R1 §4b.C(1)(c)]; AG 33 supplies **which** row and column each benefit takes, and supplies no
factors of its own.

### 7. Determining guarantee duration and Plan Type per benefit — *Text* 4

Verbatim lead-in (p. AG33-6):

> Guarantee duration and Plan Type are based upon the specific characteristics of each individual
> benefit type that comprise the integrated benefit stream, as follows:

**A. Surrender and partial withdrawal portions** — verbatim:

> For portions of the integrated benefit stream attributable to full surrender and partial withdrawal
> benefits, the Plan Type should be based upon the withdrawal characteristics of the benefit, as
> stated in the contract. This may result in a Plan Type A, B or C under the 1980 amendments of the
> SVL. The guarantee duration is the number of years for which interest rates are guaranteed in
> excess of the calendar year statutory valuation interest rate for life insurance policies with
> guarantee duration in excess of twenty (20) years.

Note the **guarantee duration definition** here is *not* "the length of the rate guarantee"; it is
the number of years the credited guarantee **exceeds the calendar-year life valuation rate for
guarantee durations over 20 years**. That is a comparison against an external published rate and has
to be recomputed by calendar year of issue.

**B. Full and partial annuitization portions** — verbatim:

> For portions of the integrated benefit stream attributable to full and partial annuitization
> benefits, the determination of the valuation interest rate involves the use of the appropriate Plan
> Type and weighting factor as determined by the SVL, with the guarantee duration as the number of
> years from the original date of issue or date of purchase, to the date the annuitization is assumed
> to commence. If the underlying assumption is that the contract owner may withdraw funds only as an
> immediate life annuity or as installments over 5 years or more, this will generally result in a Plan
> Type A, under the 1980 amendments of the SVL, with the valuation interest rate changing as different
> assumed annuitization dates determine guarantee durations which will fall into different guarantee
> duration bands under the SVL. An assumed annuitization option which has a non-life contingent payout
> period of less than five (5) years shall be considered a Plan Type C, with the valuation interest
> rate changing as different assumed annuitization dates determine guarantee durations which will fall
> into different guarantee duration bands under the SVL.

So for annuitization: **guarantee duration = years from original issue (or purchase) to the assumed
annuitization commencement date**, which means **the valuation rate is a function of the candidate
election date** and changes as the candidate moves across SVL guarantee-duration bands. Plan Type is
**A** for life annuities and non-life payouts of **5 years or more**, and **C** for non-life payouts
of **less than 5 years** — the latter stated with "shall", the former with "will generally".

**C. Non-elective portions** — verbatim:

> For portions of the integrated benefit stream attributable to non-elective benefits, since the
> underlying assumption is that no withdrawal is permitted, Plan Type A should generally be used, with
> a guarantee duration determined as the number of years from issue or purchase to the date
> non-elective benefits may first be paid. In most cases, the guarantee duration should be less than
> five years, since non-elective benefit coverage usually begins immediately after issue, with benefits
> payable commencing in the first contract year.

**Per-payment application, and the anti-abuse rider** — verbatim:

> For benefit types incorporating multiple payments, paragraphs 4(A), 4(B), and 4(C) above should be
> applied to each separate payment according to the withdrawal, annuitization, or non-elective benefit
> characteristics of the contract and payment provisions at the time each payment is to be made. If a
> portion of the integrated benefit stream is part of an immediate life annuity or a series of
> installments over five (5) years or more, but can be changed directly or indirectly by exercise of
> contract owner withdrawal options, then it would be inappropriate to apply paragraph 4(B) to that
> portion of the integrated benefit stream, since the contractholder may withdraw funds other than as a
> life annuity or in installments of five (5) years or more.

**Read that as a rule about rate-shopping**: you cannot claim the (usually more favourable) Plan Type
A annuitization treatment for a payment stream that the owner can still get at by withdrawal. The
test is "**can be changed directly or indirectly**".

### 8. The worked example the guideline carries — the GLIB decomposition

*Text* 4 closes with the guideline's only extended example (p. AG33-7). It is not numeric; it is a
worked **classification**. Verbatim setup:

> For example, a Guaranteed Lifetime Income Benefit (GLIB) is a guarantee to the owner of a fixed
> deferred annuity contract, whether traditional or indexed to an external referent such as an equity
> index, that the owner can have a defined income for life in an amount determined by formula, while
> the owner retains traditional rights (such as withdrawal) to the other values provided by the
> underlying deferred annuity and while such values continue to exist. Income benefits are typically
> deducted from one or more of the annuity's defined values to the extent such values remain positive.
> Once the GLIB is elected, the contract owner may have rights to stop and restart the income benefit
> and may also request full or partial surrender of any remaining annuity value, though doing so may
> negatively impact or eliminate subsequent guaranteed income benefits. Thus, applying 4(A) and 4(B)
> above, the GLIB benefit stream is seen to be composed of two portions to determine the Plan Type and
> guarantee duration, as follows:

**First portion**, verbatim:

> The first portion consists of the series of defined payments to the extent that the payments, or any
> fraction thereof, are withdrawals that reduce or deplete the annuity's defined values. Applying
> paragraph 4(A) to this portion would result in Plan Type A, Plan Type B, or Plan Type C, by following
> the definitions of such contained within the Standard Valuation Law and reflecting the specific
> contract provisions, especially with regard to withdrawal. Paragraph 4(A) would also apply to any
> residual withdrawals that can be made following election of the GLIB benefit.

**Second portion**, verbatim:

> The second portion is a life annuity without option to take or receive additional amounts under the
> contract, and consists of the payments not included in the above portion. Applying paragraph 4(B),
> Plan Type A would generally apply to this segment with the guarantee duration determined using the
> period from contract issue to commencement of payments in this second portion.

**What an implementer takes from this.** A GLWB/GLIB income stream is **split at the point of account
exhaustion**, and the two halves get different valuation rates:

| Portion | What it is | Rule | Plan Type | Guarantee duration |
|---|---|---|---|---|
| 1 | Guaranteed income payments *while and to the extent they reduce the annuity's defined values* — i.e. the pre-exhaustion payments — plus any residual withdrawals after GLIB election | 4(A) | A, B or C, per SVL definitions and the contract's withdrawal provisions | the *Text* 4(A) excess-guarantee measure |
| 2 | The payments not in portion 1 — a life annuity "without option to take or receive additional amounts", i.e. the post-exhaustion payments | 4(B) | **A generally** | **contract issue → commencement of the portion-2 payments** |

Note that the guideline reaches this split for a fixed deferred annuity "**whether traditional or
indexed to an external referent such as an equity index**" — the printed text of AG 33 therefore
contemplates **indexed** contracts directly, on its own terms, without invoking AG 35.

### 9. Change in fund basis — *Text* 5

Verbatim (p. AG33-7):

> As indicated by section 4b.C.(1)(c)(vi) of the SVL, a company may elect to value annuity contracts
> with cash settlement options on either an issue year basis or on a change in fund basis. Annuity
> contracts with no cash settlement options must be valued on an issue year basis. The issue year
> basis or change in fund basis should be determined for the contract as a whole, and thus must be
> consistently applied to all portions of all integrated benefit streams available under the annuity
> contract. The election of issue year or change in fund basis must be made at the issuance of the
> contract and must not change during the term of the contract without the prior written approval of
> the commissioner.

Four rules: **no cash settlement options ⇒ issue year basis, mandatorily**; the basis is a
**contract-level** attribute; it must be applied **consistently to every portion of every stream**;
and it is **elected at issue and locked**, changeable only with the commissioner's **prior written**
approval. In a model this is a per-contract immutable flag set at issue, of the same character as the
life-contract / deposit-type classification the library already records as set at inception and
unchangeable [REG-R78 ¶5].

The cross-reference is to **SVL section 4b.C.(1)(c)(vi)**; AG 33 does not reproduce that provision's
content, and this note does not supply it.

### 10. Purchase rates and the 7% expense-allowance floor — *Text* 6

This is the guideline's only numeric parameter. Verbatim (pp. AG33-7 to AG33-8):

> Contracts may provide, as contractual guarantees, the use of preferential purchase rates to those
> listed in the contract. As an example, a contract may provide that the company will offer, at the
> time of annuitization, the rates offered to new purchasers of immediate annuities if such rates will
> provide a higher annuity benefit than would result from the contractually guaranteed rates provided
> in the contract. This creates a contract guarantee which must be valued under CARVM. Ignoring this
> benefit in determining reserves will produce reserves less than the statutory formula reserves
> required under CARVM. Valuation of this benefit, however, is complicated by the fact that the
> company does not currently know what the exact rate will be at the time of the settlement election.
> In order to determine conservative statutory formula reserves, if use of future unknown rates are
> guaranteed, the company shall establish reserves not less than the contract's accumulation fund
> value, on the valuation date, reduced by an "expense allowance" not to exceed 7% of such fund. This
> section does not require the calculation of a reserve for the annuitization of business based upon
> current purchase rates pursuant to the "annuitization streams" described in Paragraph 2.B. above.

and the parallel rule for payout-period excess amounts, verbatim:

> Likewise for contracts which provide for additional amounts during the payout period over those
> guaranteed at the commencement of the annuity payments, the reserve during the deferred period shall
> not be less than the contract's accumulation fund reduced by an expense allowance not to exceed 7% of
> such fund.

**[std, restatement]** Where either trigger applies, an additional **floor** attaches:

```
V(τ) ≥ AF(τ) · (1 − EA),     EA ≤ 0.07                     ("expense allowance" not to exceed 7%)
AF(τ) = the contract's accumulation fund value at the valuation date
        (= the policy value used to purchase an annuity option — Background 2 definition)
```

Trigger 1: the contract guarantees the use of **future unknown rates** (e.g. "the better of guaranteed
and then-current purchase rates"). Trigger 2: the contract provides for **additional amounts during
the payout period** over those guaranteed at commencement, in which case the floor applies **during
the deferred period**.

Four cautions:

1. **`EA` is a cap, not a value.** "not to exceed 7%" — 7% is the maximum allowance, so
   `AF·0.93` is the **lowest** permitted floor. The guideline does not prescribe how to set `EA`
   below the cap.
2. **It is a floor on the reserve, not a substitute for the greatest-present-value calculation.**
   The final sentence of the first paragraph is explicit that the section "does not require the
   calculation of a reserve for the annuitization of business based upon current purchase rates
   pursuant to the 'annuitization streams' described in Paragraph 2.B." — i.e. you do **not** have to
   build current-rate annuitization streams; you take this floor instead.
3. **The base is the accumulation fund, not the cash value.** Where they differ (Background 2's
   whole point), the floor is on the larger.
4. **This floor can bind on ordinary MYGA/FIA designs** with "better of current or guaranteed
   purchase rates" language, which is common. It is the first genuinely mechanical CARVM constraint
   the library can now state for a deferred annuity.

### 11. Practical considerations and the "consider, not test" standard — *Text* 7

Verbatim (p. AG33-8):

> However, in practice there may be other acceptable methods of applying CARVM which are substantially
> consistent with the methods described in this Actuarial Guideline. Such methods may also be used,
> with prior regulatory approval.

and:

> Additionally, in applying this Actuarial Guideline there may theoretically be an infinite number of
> contract owner options that are possible under the contract. However, it may not be practical,
> possible or even appropriate to test every conceivable combination of potential integrated benefit
> streams theoretically available under the contract. This Actuarial Guideline requires that the
> actuary consider, not necessarily test, all potential integrated benefit streams to determine to what
> extent each contract owner option has a material impact on the reserve. In practice, the actuary may
> be able to eliminate some potential integrated benefit streams by analytical methods. The actuary may
> also be able to demonstrate the reserve adequacy of certain approximations. For example, in certain
> situations it may be shown that a CARVM reserve ignoring non-elective benefits, plus an "add-on"
> reserve for non-elective benefits, is a reasonable approximation for the theoretically correct CARVM
> reserve.

**"Consider, not necessarily test"** is the sanctioned escape from combinatorial explosion, and it is
conditioned on a **materiality** determination per contract-owner option and on the actuary being able
to eliminate streams **analytically** or to **demonstrate** the adequacy of an approximation. The
guideline names one such approximation by way of example: **CARVM ignoring non-elective benefits, plus
an "add-on" reserve for non-elective benefits**. That is precisely the decomposition many production
models actually implement, and the guideline blesses it **as an approximation requiring
demonstration**, not as an alternative method. Note separately that *substantially consistent
alternative methods* require **prior regulatory approval**.

### 12. Interaction with the Standard Valuation Law, including §5a

Stated plainly, because the library has an open question here:

- **AG 33 never cites SVL §5a by number.** The only numbered SVL cross-references in the entire
  guideline are **"Section 4b of the SVL"** (*Text* 3), **"section 4b.C.(1)(c)(vi) of the SVL"**
  (*Text* 5), and generic references to "the SVL", "the 1980 revisions to the SVL" and "the 1980
  amendments of the SVL".
- **It restates CARVM's definition rather than citing it.** Background 1, verbatim: "The SVL defined
  methodology for annuity contracts, the commissioners annuity reserve valuation method (CARVM),
  requires that reserves be the greatest of the respective excesses of the present values, at the date
  of valuation, of the future guaranteed benefits, including guaranteed nonforfeiture benefits,
  provided for by such contracts at the end of each respective contract year, over the present value,
  at the date of valuation, of any future valuation considerations derived from future gross
  considerations, required by the terms of such contracts, that become payable prior to the end of such
  respective contract year." That is the §5a construction the library already implements
  [REG-R1 §5a.B]; the mapping to "§5a" is the library's, made on content, and is sound — but it is not
  AG 33's own citation.
- **The division of labour is therefore:** §5a supplies the *greatest-of-excesses over contract-year
  ends* skeleton and the deduction of future valuation considerations; §4b supplies the *rates*; AG 33
  supplies (i) what the candidate benefit streams are, (ii) what may and may not be assumed about
  incidence, (iii) at what level each §4b parameter is determined, and (iv) two floors (the 7% expense
  allowance cases).
- **AG 33 adds a purpose statement to §5a's function**, Background 1, verbatim: "Such reserves are
  established to adequately fund all guaranteed contract obligations, including those obligations which
  are optional to the contract owner and which may not have yet been elected." That sentence is the
  justification for the whole elective-path enumeration and is worth quoting when explaining why the
  model must enumerate paths.
- **AG 33 also states the SVL's own silences**, which is useful for knowing what AG 33 is *for*:
  the SVL "is not explicit as to whether incidence tables prescribed under the SVL may be used"
  (Background 3); "is not explicit regarding whether or how blends of more than one type of benefit
  must be considered under CARVM" (Background 4); and "is not explicit as to how valuation interest
  rates should be determined" for multi-benefit annuities and for death and nursing home benefits
  (Background 5).

### 13. The discontinuity problem AG 33 identifies but does not solve

Background 2 (p. AG33-2) names a reserve-pattern problem an implementer will hit and should expect:

> Frequently there are significant discontinuities in the reserves, both upward and downward, at the
> time a settlement option is elected, between the reserve held immediately prior to the settlement as
> compared to the reserve required for the greatest actuarial present value of the annuitization option
> elected.

with two stated causes: the difference between the **SPIA valuation rate available at election** and
the **rate based on the original SPDA's date of issue**; and the difference between the **guaranteed
purchase rate used for reserve development** and the **rate actually used at election**. AG 33 raises
this in Background and **never resolves it in the Text block** — it is diagnosis, not remedy. A model
that jumps at annuitization is exhibiting a documented feature, not necessarily a bug.

---

## What this settles for the library

### Confirmed — claims the library already makes that the primary text supports

1. **The greatest-present-value-over-elective-paths construction, with per-path enumeration as the
   implementation obligation.** `us/regulatory/technical-notes.md`, "Formulaic reserves": "The
   implementation obligation is **path enumeration** — one benefit stream per elective path; missing a
   path can only understate the reserve." Confirmed, and strengthened: AG 33 requires blends across
   benefit types, not merely one path per benefit type (*Text* 2.C, three separate statements).
2. **Worked example 2's construction.** "accumulated at the guaranteed credited interest rate(s) and
   discounted at the valuation rate(s) of interest" (*Text* 2.A) is exactly what the library's SPDA
   worked example does. The example remains **[std]** in its parameter values, but its *method* is now
   primary-sourced.
3. **The required model output "Guaranteed benefit streams by elective path ... per contract, one
   stream per path"** in `us/regulatory/technical-notes.md`, "Required model outputs". Confirmed, and
   needs extending: each stream also needs its **non-elective** leg computed *conditional on* that
   elective path, and a **per-payment benefit-component tag** so the right valuation rate can be
   applied.
4. **Annuitization at guaranteed purchase rates.** R39's annotation says the elective set includes
   "annuitization at guaranteed purchase rates". Confirmed verbatim at *Text* 2.B, with "excluding any
   current purchase rates which may be applicable" — and with the *Text* 6 floor as the price of that
   exclusion.
5. **That AG 33 is an interpretation of CARVM rather than a separate method.** Confirmed verbatim in
   *Purpose*.
6. **AG 33's scope is elective-benefit annuity contracts.** The title the library has been citing
   ("...for Annuity Contracts With Elective Benefits", carried at R39 and in
   `us/regulatory/sources.md`) matches the printed title exactly. **R39's title is right**; it is the
   *fixed-deferred-annuity* stream's alternative title that is wrong (see below).

### Contradicted — claims the library must change

7. **The effective date is wrong.** `products/fixed_deferred_annuity/product-spec.md` (~line 534),
   `_research/fixed-deferred-annuity.md` (R7 entry, §15 and Gaps item 1) and
   `products/fixed_deferred_annuity/sources.md` (R7) all state AG 33 is "effective **December 31,
   1995** for all contracts issued on or after January 1, 1981", sourced from IRS Rev. Rul. 2002-6.
   **The manual as of March 2026 prints "December 31, 1998"**, with the same 1/1/1981 issue-date
   reach. The issue-date reach is confirmed; the effective date is not. Do not silently swap the date
   — record both, note that Rev. Rul. 2002-6 was describing a differently-titled instrument, and flag
   that no amendment history is available in the extracted pages.
8. **The title carried by the fixed-deferred-annuity stream is not the printed title.**
   "Determining Minimum Commissioners Annuities Reserve Valuation Method (CARVM) Reserves for
   Individual Annuity Contracts" is the Rev. Rul. 2002-6 title. The manual prints **"Determining CARVM
   Reserves for Annuity Contracts With Elective Benefits"**. Same correction sites as item 7.
9. **Nursing home benefits are NON-elective, not elective.** R39's annotation in
   `references/regulatory-and-actuarial-references.md` (~line 999) lists the elective set as "full
   surrenders, partial withdrawals, annuitization at guaranteed purchase rates, **nursing-home
   waivers**", contrasted with "non-elective (death, and other non-mortality incidence)". AG 33's
   *Definitions* 1 places **"nursing home benefits"** expressly in the **non-elective** list, and
   treats "non-elective waiver-of-surrender-charge benefits" as non-elective with the *Text*-level
   cut-off rule at *Definitions* 2. Correct R39.
10. **"Efficient policyholder selection" is not the guideline's standard and should not be attributed
    to it.** R39 says the guideline defines what "the 'efficient policyholder selection' assumption
    means in practice [unverified]". That phrase **does not appear in AG 33**. The actual standard is:
    experience-based elective incidence is **prohibited**; trial sets are maximised over; all rates
    0%–100% are theoretically in scope; the greatest present value "will typically occur by assuming an
    incidence rate of either 0% or 100%"; and the actuary must **consider, not necessarily test**, all
    streams. Replace the gloss with the guideline's own construction.
11. **"AG 33 text not retrieved" caveats are now obsolete** and must be replaced with citations to
    R151 wherever they appear. The full list found: `README.md` (lines ~103, ~155, ~185);
    `us/regulatory/statutory-accounting-and-capital.md` (lines ~29, ~218, ~219, ~225–228, ~243–244,
    ~640 matrix row, ~698); `us/regulatory/technical-notes.md` (lines ~9, ~80, ~453);
    `us/regulatory/sources.md` (~line 664, and the R39 entry at ~708–714);
    `references/regulatory-and-actuarial-references.md` (R39 entry ~986–1007, gaps at ~1741 and
    ~3243, and the "single largest hole" statement in section 14);
    `products/fixed_deferred_annuity/{product-spec.md, sources.md, technical-notes.md}`;
    `products/fixed_indexed_annuity/{product-spec.md, technical-notes.md, sources.md}`;
    `products/deferred_income_annuity/{sources.md, technical-notes.md}`;
    `products/registered_index_linked_annuity/technical-notes.md` (~lines 675–680);
    `_research/{fixed-deferred-annuity.md, fixed-indexed-annuity.md, statutory-reserves.md,
    statutory-accounting.md, regulatory-actuarial-annuities.md, risk-based-capital.md}`.
    **AG 35 remains unretrieved** — every AG 35 caveat stands.
12. **"A RILA CARVM run rests on the SVL text alone" is no longer true.**
    `us/regulatory/statutory-accounting-and-capital.md` (~lines 225–227) and
    `products/registered_index_linked_annuity/technical-notes.md` (~lines 675–680) both say this.
    AG 33 applies to **all** annuity contracts subject to CARVM with elective benefits, with no
    product carve-out and no separate-account exception, so a RILA with elective benefits is inside AG
    33 and gets its stream construction, its incidence rules, its benefit-level rate determination and
    (where the purchase-rate language is present) its 7% floor. The remaining RILA gap is A-250, A-255
    and AG 35, not AG 33.
13. **The AG 33 / AG 35 precedence direction is now sourced.** The library says AG 35 "does not
    replace AG 33 but specifies how the index-linked benefit is brought into the AG 33
    greatest-present-value calculation" [R39/R40 annotations, marked unverified]. AG 33's own
    precedence clause supports the general principle — "the product specific actuarial guideline or
    regulation will take precedence" — but **AG 33 never names AG 35**, so the specific AG 33/AG 35
    relationship stays inferential. Upgrade the *principle*, not the *pairing*.
14. **The `us/regulatory/statutory-accounting-and-capital.md` applicability matrix row "Formulaic
    CARVM — SVL §5a, AG 33/AG 35" marks `x` for all six annuity products.** For AG 33 that is right
    for the five deferred/indexed/RILA/variable products but **overstated for a no-option SPIA**: AG
    33's non-elective definition expressly covers "benefits payable under either a deferred or
    immediate annuity contract (with or without life contingencies), **where no benefit options are
    available**", and the applicability sentence requires that "any elective benefits ... are
    available". A pure life-only SPIA with no commutation, no acceleration and no elective option is
    **outside AG 33** — CARVM still applies, AG 33 does not. Mark it `(x)` or split the row.

### Opened up / newly answerable — questions the library flagged that this text now reaches

15. **The DIA elective paths.** `products/deferred_income_annuity/technical-notes.md` (~line 563)
    says "**AG 33 ... was not retrieved** ... no mechanic for those paths is stated here" for the
    ±5-year start-date adjustment, acceleration and commutation. Those are **elective benefits** under
    *Definitions* 1 (options freely elected under the contract), so: the DIA is in AG 33's scope; the
    three timing options are maximised over as trial sets rather than assumed from experience; the
    valuation rate for the annuitization portion is set by **guarantee duration = issue to assumed
    commencement**, which *changes with the elected start date*, so the ±5-year adjustment moves the
    contract across SVL guarantee-duration bands; and each payment is classified per *Text* 4's
    per-payment rule. A commutation right is precisely the *Text* 4 "can be changed directly or
    indirectly by exercise of contract owner withdrawal options" case, which **bars** 4(B) treatment
    for the affected payments.
16. **The FIA GLB income stream after account exhaustion.** The library records that VM-22's
    Accumulation category "expressly covers the post-exhaustion GLB income stream"
    [REG-R36] but had no formulaic counterpart. AG 33's **GLIB example** is that counterpart: the
    pre-exhaustion payments take 4(A) (Plan Type A/B/C by withdrawal characteristics) and the
    post-exhaustion life annuity takes 4(B) (Plan Type A generally, guarantee duration from **contract
    issue** to commencement of the post-exhaustion payments). This is directly usable in
    `products/fixed_indexed_annuity/technical-notes.md`.
17. **Whether valuation rates differ by benefit within one CARVM reserve.**
    `_research/fixed-deferred-annuity.md` Gaps item 1 lists "separate valuation interest rates for
    elective vs non-elective benefits" as unverified. **Answered, with a correction to the framing:**
    the split is not elective/non-elective, it is **contract-level parameters (A, B, C) versus
    benefit-level parameters (D guarantee duration, E Plan Type)**, producing "potentially different
    valuation rates for each benefit type comprising the integrated benefit stream".
18. **A concrete numeric CARVM constraint for deferred annuities.** The **7% expense-allowance floor**
    (*Text* 6) is now available and belongs in `us/regulatory/technical-notes.md`, "Formulaic
    reserves", next to the CARVM construction. It bites on any contract guaranteeing better-of current
    purchase rates, or additional payout-period amounts.
19. **A sanctioned approximation.** "CARVM reserve ignoring non-elective benefits, plus an 'add-on'
    reserve for non-elective benefits" is named in *Text* 7 as an example of a demonstrable
    approximation. The library's implementation-notes section can cite this rather than presenting the
    decomposition as an engineering shortcut.
20. **Immutable per-contract flags.** The issue-year / change-in-fund election joins the
    life-contract/deposit-type classification as a flag **set at issue and locked** (commissioner's
    prior written approval to change). Both belong in the same place in the model's contract record.
21. **Reserve discontinuity at annuitization is a documented phenomenon** (Background 2), which the
    library's validation checks can note rather than treat as a reconciliation failure.

### Still not settled by this document

22. Whether an elective move from CARVM onto VM-22 is a change in valuation basis — AG 33 says
    nothing about VM-22 and predates it.
23. AG 35's mechanics, Type 1 / Type 2, certification, and the asset-adequacy-testing requirement for
    equity-indexed annuities — **all still [unverified]**; AG 33 does not mention AG 35 or
    asset adequacy at all.
24. A-820, A-830, A-250, A-255, A-585, A-791 and AG I — all still unread.

---

## Quotable anchors

**Quotation convention.** The PDF text layer inserts spurious spaces inside words at justified-line
breaks (e.g. the source file renders *Definitions* 1's heading as `Elective and Non-Elec tive Benefits
in CARVM`). In the quotations below **those intra-word spaces have been closed up and nothing else
has been changed** — no words added, removed or reordered, no punctuation altered, no capitalisation
changed. Anyone re-verifying against the PDF should expect the broken spacing.

| # | Quotation | Page |
|---|---|---|
| 1 | "This Actuarial Guideline shall apply to all annuity contracts subject to CARVM, where any elective benefits (as defined below) are available to the contract owner under the terms of the contract." | AG33-3 / PDF 1498 |
| 2 | "The purpose of this Actuarial Guideline is to codify the basic interpretation of CARVM and does not constitute a change of method or basis from any previously used method" | AG33-3 / PDF 1498 |
| 3 | "in the event an actuarial guideline or regulation dealing with reserves is developed for a specific annuity product design, the product specific actuarial guideline or regulation will take precedence over the Actuarial Guideline." | AG33-3 / PDF 1498 |
| 4 | "This guideline shall be effective on December 31, 1998, affecting all contracts issued on or after January 1, 1981." | AG33-8 / PDF 1503 |
| 5 | "no less than 33 1/3% of the additional reserves resulting from the application of this guideline on December 31, 1998, no less than 66 2/3% on December 31, 1999, and 100% by December 31, 2000." | AG33-8 / PDF 1503 |
| 6 | "each benefit available under the annuity contract must be placed into one of the two categories" | AG33-3 / PDF 1498 |
| 7 | "including (but not limited to) death benefits, accidental death benefits, disability benefits, nursing home benefits, and benefits payable under either a deferred or immediate annuity contract (with or without life contingencies), where no benefit options are available under the terms of the contract." | AG33-3 / PDF 1498 |
| 8 | "Elective benefits include (but are not limited to) full surrenders, partial withdrawals, and full and partial annuitizations." | AG33-3 / PDF 1498 |
| 9 | "For elective benefits, incidence rates should not be based on tables reflecting past company experience, industry experience or other expectations." | AG33-4 / PDF 1499 |
| 10 | "all possible elective benefit incidence rates between 0% and 100% should be considered. However, in practice, such a greatest present value will typically occur by assuming an incidence rate of either 0% or 100%." | AG33-4 / PDF 1499 |
| 11 | "incidence rates greater than zero are not to be applied at any time in the projection after the earlier of: (a) the end of the surrender charge period applicable immediately after the first premium is paid; and (b) when the projected cash value has been depleted." | AG33-4 / PDF 1499 |
| 12 | "An integrated benefit stream is one potential blend of guaranteed elective and non-elective benefits available under the contract" | AG33-4 / PDF 1499 |
| 13 | "the ultimate reserve established must be the greatest of the present values of these values, based on valuation interest rate(s) as defined in Section 3 below." | AG33-4 / PDF 1499 |
| 14 | "accumulated at the guaranteed credited interest rate(s) and discounted at the valuation rate(s) of interest defined in section 3 below" | AG33-5 / PDF 1500 |
| 15 | "the guaranteed purchase rates contained in the contract, as well as any other contract provisions, excluding any current purchase rates which may be applicable, are applied to the accumulation fund." | AG33-5 / PDF 1500 |
| 16 | "Parameters A, B and C above should be determined at a contract level. … Parameters D and E should be determined at a benefit level" | AG33-5 / PDF 1500 |
| 17 | "resulting in potentially different valuation rates for each benefit type comprising the integrated benefit stream." | AG33-6 / PDF 1501 |
| 18 | "the guarantee duration as the number of years from the original date of issue or date of purchase, to the date the annuitization is assumed to commence." | AG33-6 / PDF 1501 |
| 19 | "An assumed annuitization option which has a non-life contingent payout period of less than five (5) years shall be considered a Plan Type C" | AG33-6 / PDF 1501 |
| 20 | "the company shall establish reserves not less than the contract's accumulation fund value, on the valuation date, reduced by an 'expense allowance' not to exceed 7% of such fund." | AG33-8 / PDF 1503 |
| 21 | "This Actuarial Guideline requires that the actuary consider, not necessarily test, all potential integrated benefit streams to determine to what extent each contract owner option has a material impact on the reserve." | AG33-8 / PDF 1503 |
| 22 | "a CARVM reserve ignoring non-elective benefits, plus an 'add-on' reserve for non-elective benefits, is a reasonable approximation for the theoretically correct CARVM reserve." | AG33-8 / PDF 1503 |
| 23 | "Such reserves are established to adequately fund all guaranteed contract obligations, including those obligations which are optional to the contract owner and which may not have yet been elected." | AG33-1 / PDF 1496 |
| 24 | "'accumulation fund' is defined as the policy value which is used to purchase an annuity option under the terms of the contract." | AG33-1 / PDF 1496 |
| 25 | "The election of issue year or change in fund basis must be made at the issuance of the contract and must not change during the term of the contract without the prior written approval of the commissioner." | AG33-7 / PDF 1502 |

---

## Gaps and caveats

### What AG 33 does not address

1. **No formulas, no symbols, no tables, no factors** except the **7%** expense-allowance cap and the
   **33 1/3 / 66 2/3 / 100%** phase-in percentages. Every rate, weighting factor and mortality table
   comes from the SVL, which AG 33 points at without reproducing. Anyone expecting AG 33 to contain a
   CARVM formula will not find one.
2. **The "end of each respective contract year" indexing and the deduction of future valuation
   considerations appear only in the Background paraphrase of the SVL, never in the operative Text
   block.** *Text* 1 speaks of maximising over integrated benefit streams; it does not say how the
   stream maximisation composes with §5a's per-contract-year-end excess. In practice the two are
   reconciled by treating each contract-year-end election as one of the elective paths, but **AG 33
   does not say that** and this note will not assert it.
3. **No asset adequacy requirement**, no mention of cash flow testing, no mention of ASOP 22 or of
   VM-30. The AG 35 asset-adequacy requirement the library records is *not* an AG 33 requirement.
4. **No mention of the Valuation Manual, VM-21, VM-22, VM-A, VM-C or PBR** in any form. The guideline
   predates them and the printed text has not been updated to reference them.
5. **No mention of AG 35, AG 43 or any other guideline by name**, and no mention of separate accounts,
   variable annuities, index credits, index crediting methods, MVAs, or SEC registration.
6. **No treatment of the deficiency-reserve interaction**, no mention of Model #805/#808 nonforfeiture
   or of the surrender-value-in-excess-of-reserve item.
7. **No quantification of the "margins for conservatism"** required where no SVL incidence table is
   prescribed (*Definitions* 2), and no guidance on how to set the expense allowance below the 7% cap
   (*Text* 6).
8. **No guidance on aggregation, model points, or grouping.** CARVM under AG 33 reads as seriatim
   throughout ("each benefit available under the annuity contract", "the contract") but the guideline
   never says so.
9. **No amendment history or revision log.** The extracted pages carry only the manual's
   `© 1999-2026` footer. There is nothing in them from which to date the GLIB paragraphs, which are
   plainly later than 1998 in subject matter (GLIBs and indexed annuities are not 1998 products). The
   guideline as printed therefore contains **material of unstated vintage under a 1998 effective-date
   line**, and this note cannot resolve when the GLIB text was added or whether it carries its own
   effective date elsewhere in the manual.

### Cross-references made to material not supplied

10. **SVL Section 4b** — the valuation-rate machinery. AG 33 lists its five parameters but reproduces
    none of the rate formula, weighting factors, Plan Type definitions or guarantee-duration bands.
    The library already carries these from the SVL itself [REG-R1 §4b].
11. **SVL section 4b.C.(1)(c)(vi)** — the issue-year / change-in-fund election. Content not
    reproduced in AG 33 and not verified here.
12. **"The 1980 amendments of the SVL" / "the 1980 revisions to the SVL"** — the source of Plan Types
    A, B and C and of the dynamic valuation-rate formula. Referenced, not reproduced.
13. **"the calendar year statutory valuation interest rate for life insurance policies with guarantee
    duration in excess of twenty (20) years"** — an externally published series that *Text* 4(A) uses
    to define guarantee duration for withdrawal benefits. AG 33 gives no values and no citation.
14. **"tables prescribed by the SVL"** for non-elective incidence, and **"annuity mortality tables
    prescribed by the SVL"** for mortality-based benefits and survivorship discounting. Not identified
    by name or year in AG 33.
15. **"a product specific actuarial guideline or regulation"** — the precedence clause names no
    instrument.

### Ambiguities in the text itself

16. **"Section 3" and "Section 4" cross-references inside *Text* are to the *Text* block's own
    sections**, not to SVL sections — *Text* 1 says "Section 3 below" and *Text* 3 says "Section 4
    below", and both resolve inside the guideline. But *Text* 3's first line says "Section 4b of the
    SVL", and *Text* 4's sub-paragraphs are cited as "paragraphs 4(A), 4(B), and 4(C)". Citing AG 33
    without naming the block (*Background* / *Definitions* / *Text*) will produce collisions, since all
    three blocks restart at 1.
17. **"Examples of Integrated Benefit Streams That Must Be Considered"** — the heading says examples,
    the body says "mandatory set" (twice) and "must be considered". A and B are requirements
    notwithstanding the heading.
18. **"will generally result in a Plan Type A" (4B, life annuities) versus "shall be considered a
    Plan Type C" (non-life payouts under 5 years)** — one permissive, one mandatory, in adjacent
    sentences. The asymmetry appears deliberate but is not explained.
19. **The grade-in eligibility wording** says "contracts issued prior to December 31, 1998" against
    an effective date of December 31, 1998; contracts issued exactly on that date are not addressed.
    Moot now, but note it if reconstructing history.
20. **"Elective benefits" is defined as the complement of non-elective**, so any classification
    dispute is really a dispute about the non-elective definition. The only tie-breaker offered is the
    behavioural-influence judgement clause.
21. **The *Text* 6 first paragraph's closing sentence** — "This section does not require the
    calculation of a reserve for the annuitization of business based upon current purchase rates
    pursuant to the 'annuitization streams' described in Paragraph 2.B. above" — is a relief from
    building current-rate streams, granted in the same breath as the 7% floor. It is clear on its face
    but easy to read backwards; note it is a *narrowing* of the *Text* 2.B obligation, not a widening.

### Extraction artefacts

22. **Spurious intra-word spaces at justified-line breaks**, throughout, in the PDF text layer.
    Examples as they appear in the source file: `bene fits`, `cons iderations`, `st atutory`,
    `cont ract`, `acc umulation`, `disconti nuities`, `gr eatest`, `offeri ng`, `Non-Elec tive`,
    `su rvivorship`, `excludi ng`, `guaran tee`, `spec ific`, `additi onal`, `clarificat ion`,
    `potent ial`, `add- on`, `satisfacto ry`, `adeq uate`, `referen t`, `righ ts`, `ea ch`,
    `de termination`. These are **artefacts of the text layer, not typographical errors in the
    manual**. All quotations above have them closed up, per the convention stated in "Quotable
    anchors".
23. **Irregular line breaks** — the extraction breaks lines at the PDF's typeset line ends, so
    sentences span several source lines. No sentence was found to be truncated or lost.
24. **No superscripts, footnotes, tables, figures or formulas appear in these eight pages**, so no
    superscript loss could be detected; the guideline contains none of those elements to begin with.
25. **Nothing in the extracted range appears garbled beyond the spacing artefact.** The eight pages
    are contiguous (PDF 1496–1503), each carries its printed page number (AG33-1 … AG33-8) and its
    copyright footer, and the text runs continuously from the title through the Effective Date
    paragraph. **The guideline is complete as extracted** — the Effective Date block ends the
    document, and AG33-8 is its last page.
26. **The manual's edition line, table of contents, Appendix C front matter and any Volume statement
    were not in the extracted range**, so the placement facts in "Source" above rest on the running
    heads plus the library's existing record of the manual [REG-R73].
