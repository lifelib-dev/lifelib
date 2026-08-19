# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. single premium immediate annuities.

:mod:`~.SPIA_US_S` is the executable counterpart of
``products/immediate_annuity/technical-notes.md`` in the lifelib-products library.
It projects gross liability cash flows for a single SPIA already in payment: scheduled
instalments to the annuitant and, on a joint contract, to the surviving annuitant at a
survivor percentage; a certain-period or refund guarantee; a cash-refund lump sum on
death; optional commutation of the certain portion; and maintenance expense. There is
no premium income in the projection, no account value, no cash surrender value and
**no lapse decrement** — mortality is the only decrement, a position VM-22 makes
prescriptively for this reserving category [R2][REG-R36].

This product is the **payout chassis** of the library: the same survival-indexed
payment engine serves deferred income annuities, annuitizations of deferred-annuity
account values and supplementary contracts, which VM-22 places with SPIAs in a single
Payout Annuity Reserving Category [R2].

**Spaces.** The model contains two:

:mod:`~.SPIA_US_S.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.SPIA_US_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.SPIA_US_S.Data`
    Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every contract. In ``Data`` they are
evaluated once, however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. ``t`` counts **policy months from the annuity
date**, ``t = 1, 2, ..., proj_len()``, matching the technical notes' own index; the
annuity date is collapsed onto the issue date, so there is no deferral period. Note
the contrast with lifelib's ``CashValue_SE``, whose months are 0-based: here the
month-zero state (``lives_if(0, life) = 1``, ``cum_annuity_pp(0) = 0``) is the ``t <= 0``
branch of each recursion, and every projected month is ``t >= 1``.
``proj_len()`` runs to the notes' age stop rule on the **youngest** covered life, or
to the end of the effective certain period if that is later — stopping on the primary's
age alone would truncate a younger joint annuitant's tail. The age rule ends the
projection one month *before* any life attains the limiting age ω = 120 (696 months on
the anchor cell's 65/62 pair, where the younger life is then 119), so the notes' other
stop test, ``IF(t) < 1e-6``, is not subsumed: model point 8 finishes at
``pols_if(696) = 3.41e-06``. A test pins the figure.

The monthly processing order follows the notes: the COLA increase applies at the start
of month ``12(y-1)+1`` for ``y >= 2``; mortality is decremented at **end of month**;
the instalment falls at the end of the month on arrears timing (the default) and at the
start on advance timing, with survival measured at the payment point in both cases; the
cash-refund lump sum, any commutation and the maintenance expense accrue in the same
month. All cash flows are **undiscounted** — reserves and discounting are a separate
layer, and the only discounting in the model is contractual, inside the commuted value.

**What is sourced and what is not.** The contractual elements come from the composite's
product documents: the five payout forms and the two survivor-reduction triggers, the
fixed compound COLA menu, the cash-refund and installment-refund definitions, one
carrier's ``premium / annualized income`` rule for the derived refund period, and the only
published SPIA surrender-charge schedule, 8% in contract year 2 grading to 0% from
year 10 [S1][S2][S3][S5]. Everything else is a standardization introduced for the
reference implementation, because no public source carries it: the initial income level
``B(1)`` (no insurer publishes payout factors, so it is exogenous and unverifiable),
the mortality and improvement tables shipped here, the A/E factor of 1.084, the
commutation discount basis (**[std]** *and* **[unverified]**), the $60 p.a. maintenance
expense inflating at 2.5%, and the joint-life independence assumption.
**This model is a mechanics demonstration, not a pricing or reserving result.**

Not implemented, and named here so the omission is visible: the qualified-money overlay
(RMD limits on the certain period, the MDIB survivor cap, the post-death distribution
period — the ``qualified`` column is inert); the rate-driven dynamic commutation take-up
``u(y, t)``, of which only the deterministic ``u(y)`` construction is built; a 10-year
CMT path (``cmt10_shift`` is a flat scalar); the ALB/ANB conversion VM-22 supplies for
valuation-rate bucketing; the exclusion-ratio tax split, which is a policyholder
computation and generates no insurer cash flow; and every valuation layer — CARVM,
VM-22 CTE70, the 2012 IAR valuation table with its no-compound-rounding rule.

**Model points.** ``model_point_table.csv`` carries fifteen contracts on the same anchor
configuration — $100,000 premium, $6,000 p.a. initial income, joint primary male ANB 65
and joint annuitant female ANB 62, monthly in arrears, 3% compound COLA, survivor
percentage 2/3 — differing only in what the notes' worked example and its "Known
modeling pitfalls" list vary: the reduction trigger, which life dies, the payout form,
arrears against advance timing, the payment frequency, the income level behind the
derived refund period, and whether the run is a deterministic **scenario** or a
probability-weighted **table** run.
Points 1 and 2 are the two columns of the worked-example table; points 3–6, 10, 11 and 13
are its traces and the pitfall cases; points 7, 8, 9 and 12 project on the shipped
mortality tables, point 8 being the anchor cell on that basis. Two points exist to hold
open a case the notes leave under-specified and would otherwise go untested: point 14 is
**quarterly in advance**, the frequency at which the notes' ``t - 12/m`` survival point
and their own advance payment schedule disagree, and point 15 is the **certain_only**
form, where the notes' expense formula ``IF(t) = max(C, l_alive)`` outlives the contract
that their own prose ends at ``n_eff``. Both divergences are resolved in
:mod:`~.SPIA_US_S.Projection`'s docstring and pinned by tests. A test asserts
every model point projects.

**Verification.** ``tests/test_immediate_annuity_us.py`` asserts every row and column of
the notes' worked-example table — both trigger columns at ``t`` = 1, 12, 13, 14, 15, 24
and 25, to the cent — plus each of the five traces below it: the reversed death on which
the two triggers coincide, the COLA continuing after the survivor reduction, the 10-year
certain period deferring the reduction to ``t = 121``, the cash-refund lump sum of
$93,485.00 on a death in month 14, and the derived installment-refund period of 200
months.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/immediate_annuity/SPIA_US_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "SPIA_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

