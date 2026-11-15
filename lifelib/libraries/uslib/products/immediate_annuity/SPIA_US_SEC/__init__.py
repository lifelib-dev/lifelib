# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. single premium immediate annuities.

:mod:`~.SPIA_US_SEC` projects the contracts :mod:`~.SPIA_US_S` projects — a single premium
immediate annuity in payment: scheduled instalments to the annuitant and, on a joint
contract, to the surviving annuitant at a survivor percentage; a certain-period or refund
guarantee; a cash-refund lump sum on death; optional commutation of the certain portion;
and maintenance expense — from a **valuation date** rather than from the annuity date. A
model point may be a contract already in payment at that date, one whose annuity date is
that date, or one commencing in the ten years after it, as in lifelib's
``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S`` the same way. Its
formulas are the executable counterpart of
``products/immediate_annuity/technical-notes.md``, and
``products/immediate_annuity/model-sec.md`` explains what running in force changes.
There is no premium income in the projection, no account value, no cash surrender value
and **no lapse decrement** — mortality is the only decrement, a position VM-22 makes
prescriptively for this reserving category [R2][REG-R36].

This product is the **payout chassis** of the library: the same survival-indexed
payment engine serves deferred income annuities, annuitizations of deferred-annuity
account values and supplementary contracts, which VM-22 places with SPIAs in a single
Payout Annuity Reserving Category [R2].

**Spaces.** The model contains two:

:mod:`~.SPIA_US_SEC.Data`
    Reads the three assumption CSVs it shares with :mod:`~.SPIA_US_S` and its own model
    point table, and holds their filename References. It takes no parameters, so each
    file is read **once per model**.

:mod:`~.SPIA_US_SEC.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.SPIA_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every contract. In ``Data`` they are
evaluated once, however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the valuation
date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the valuation month
for every model point, however long the contract has been in payment, and the frame runs
``t = 0, 1, ..., proj_len() - 1``, where ``proj_len()`` counts the months from the
valuation date to the notes' stop rule. ``duration_mth(t)`` counts the months elapsed from
the annuity date, ``duration_mth_init() + t`` from the model point's ``duration_mth`` at
``t = 0``, and the contract runs on it: the policy year ``duration_mth(t) // 12 + 1``, the
attained ages, the payment months, the COLA anniversaries, the certain period, the
commutation months and the surrender-charge year. Survival is indexed by a **time point**
on the valuation clock, ``lives_if(t, life)`` *at* time ``t``, the start of month ``t``,
and the instalments scheduled to date by a time point on the policy clock,
``cum_annuity_pp(k)`` *before* the time ``k`` months after the annuity date. The annuity
date is collapsed onto the issue date, as in :mod:`~.SPIA_US_S`, so a contract issued
before its annuity date is modelled as an annuity commencing later, without the
pre-income period.

The stop rule is :mod:`~.SPIA_US_S`'s, on the policy clock: the notes' age stop on the
**youngest** covered life, or the end of the effective certain period if that is later.
On the anchor cell's 65/62 pair it is policy month 696: the younger life is 119 in the last
projected month, policy month 695, and a contract in payment ``d`` months has ``696 - d``
months left to project. The notes'
other stop test, ``IF(t) < 1e-6``, is not subsumed: model point 21, the anchor cell on
the table basis in its last month, carries ``pols_if(0) = 3.41e-06``. A test pins the
figure.

The monthly processing order follows the notes: the COLA increase applies at the start
of policy month ``12(y-1)`` for ``y >= 2``; mortality is decremented at **end of month**;
the instalment falls at the end of the month on arrears timing (the default) and at the
start on advance timing, with survival measured at the payment point in both cases; the
cash-refund lump sum, any commutation and the maintenance expense accrue in the same
month. All cash flows are **undiscounted** — reserves and discounting are a separate
layer, and the only discounting in the model is contractual, inside the commuted value.
Expense inflation alone runs on ``t``, so the maintenance charge is in valuation-date
dollars. Mortality improvement is calendar-dated, through ``annuity_year + duration(t)``,
so it stays on the policy clock: a contract reads the improvement of its own calendar
years whatever the valuation date. On a point commencing at ``t = 0`` the two clocks
coincide, and the model computes what :mod:`~.SPIA_US_S` computes, except that
``pols_if_init()`` is the count already in payment at the valuation date, 0 for such a
point, whose contracts enter as new business at ``t = 0``.

A contract in payment carries an **opening state** beside its count and its policy clock:
each covered life's probability of being alive at the valuation date, 1 or 0 on a real
record, so that a joint contract may carry one life already dead; the commutation fraction
it has taken; and the 10-year CMT's change from its annuity date to the valuation date,
which moves its commutation discount rate, the Reference ``cmt10_shift`` being the change
made at that date, on the one path every point shares, which a contract commencing later
has not seen. The certain months left follow from ``duration_mth``, and the payments to
date, which a refund nets, are a deterministic schedule summed from the annuity date.

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
computation and generates no insurer cash flow; the pre-income period between issue and
a later annuity date; and every valuation layer — CARVM, VM-22 CTE70, the 2012 IAR
valuation table with its no-compound-rounding rule.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.SPIA_US_S` and
its model point table, and the tests regenerate it and compare, so no row is typed by
hand. Points 1 to 15 are the twins of :mod:`~.SPIA_US_S`'s fifteen points, each commencing
at the valuation date, so the worked example's anchor cell and its traces and pitfall
cases are here as there. Points 16 to 21 are S points restated in payment at an S month,
each opened with the state S carries into that month: the anchor cell at month 14, the
month after its joint annuitant's death; the cash refund at month 13, its death month,
which pays the refund at ``t = 0``; the 10-year certain point at month 120, where its
deferred reduction begins; the certain floor with both lives dead, at month 30; the
commuting point on the table basis at month 24, its second anniversary, with two
fractional lives; and the anchor cell on the table basis at month 695, its last. Point 22
is the anchor cell on the table basis commencing 13 months after the valuation date. Each
row keeps :mod:`~.SPIA_US_S`'s annuity year, so the rows are test cases standing at
different calendar dates at their common ``t = 0``; a real block carries each contract's
actual annuity year. A test asserts that every point in the table projects.

**Verification.** On the fifteen twins every cell this model shares with
:mod:`~.SPIA_US_S` agrees with it at every argument the S model evaluates in its sweep,
``pols_if_init``, ``model_point`` and ``result_pols`` excepted, so the worked example
``tests/test_immediate_annuity_us.py`` asserts — every row of the notes' table under both
triggers, and the traces below it — holds here too, with no number restated.
``tests/test_immediate_annuity_us_sec.py`` splices: an S point restated in payment at
month ``d``, opened with S's own state there, continues the S projection from ``d`` on,
cell by cell, at months around the deaths, the anniversaries and commutations, the end of
the certain period and the last month of the frame, over S's points and variants of them,
in a copy of S's table never committed, that reach what S's own points cannot. And an
annuity commencing ``k`` months late is the S projection ``k`` months on.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/immediate_annuity/SPIA_US_SEC")
    >>> model.Projection[16].result_cf()
    >>> model.Projection[16].result_pols()
"""

from modelx.serialize.jsonvalues import *

_name = "SPIA_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

