# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for UK pension annuities.

:mod:`~.PA_UK_S` is the executable counterpart of
``products/pension_annuity/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single UK pension annuity in
payment: instalments to the annuitant and to a dependant, guarantee-period payments,
value-protection lump sums and maintenance expense.

**Mortality is the model.** After outset the contract has no premiums, no surrender
value, no account value and no policyholder options at all. The only decrements are
deaths; the only stochastic drivers are longevity and, on the indexed options,
inflation. That is not an omission — it is the design property that makes the liability
eligible for the Solvency UK matching adjustment, whose conditions effectively require
this shape.

The U.S. counterpart in the same library is :mod:`.SPIA_US_S`, and the two share the
payout chassis: a life-contingent instalment stream, a certain-period **floor** rather
than a second stream, a refund-style death benefit measured against instalments already
paid, and survival measured at the payment point rather than at the end of the month.
Where they part is the UK-specific machinery: a **dependant's stream** at a stated
percentage with an overlap rule, **escalation** on four bases including a
path-dependent RPI ratchet, and **value protection** in place of a cash refund — plus
the absence of anything resembling SPIA's commutation right, because a UK pension
annuity has no surrender value at any time.

**Spaces.** The model contains two:

:mod:`~.PA_UK_S.Data`
    Reads the two input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.PA_UK_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.PA_UK_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every contract. In ``Data`` they are
evaluated once, however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps from the annuity start date. Escalation applies at
the start of the month containing the policy anniversary, first at ``t = 13``; arrears
instalments require survival at the end of the payment month and advance instalments at
the start of it; deaths are decremented at end of month. Age is **age last birthday**.
The limiting age is 115, and the projection stops one month before the youngest covered
life would reach it — stopping on the annuitant's age alone would truncate a younger
dependant's tail.

**What is sourced and what is not.** The contractual mechanics are sourced: the
instalment formula, the four escalation bases and the RPI catch-up ratchet, the
dependant's percentage and the overlap rule, the guarantee period as an annuity-certain
floor, value protection and its exclusivity with the guarantee, the ``v + delta <= 1``
bound, and the absence of any surrender value. Every rate is a standardization. The
SAPS and PMA16/PFA16 annuitant tables are restricted to CMI Authorised Users and the
CMI projections model software with them, so the mortality basis shipped here is a
**[std]** proxy — an ONS-shaped population table with a flat annuitant adjustment and a
deterministic improvement scale — and no insurer publishes an annuity rate card, so the
starting income is a model point input. **This model is a mechanics demonstration, not
a pricing or reserving result.** Replace the basis with licensed tables before drawing
any conclusion from the output.

**Verification.** ``tests/test_pension_annuity_uk.py`` asserts the notes' worked
example row by row to the penny, including the £43,209.50 value-protection lump sum on
the month-17 death and the dependant's stream starting at the next payment date.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/pension_annuity/PA_UK_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "PA_UK_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

