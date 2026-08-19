# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for a UK unit-linked investment bond.

:mod:`~.ULB_UK_S` is the executable counterpart of
``products/unit_linked_bond/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-policy model point of a modern
clean-charge onshore unit-linked bond: a single premium, a death benefit of 100.1% of
the bid value of units, no surrender penalty, and the 5% a year tax-deferred withdrawal
pattern the product is sold on.

**The decomposition is the model.** UK practice splits this product into two streams and
so does this implementation:

*the unit fund* — the bid value of units, matched by the linked assets, which grows with
the fund, bears the tax provision and the fund-based charges, and is drawn down by
withdrawals and adviser charges; and

*the non-unit cash flow* — what actually accrues to the insurer: the annual management
charge and any rider charge, less expenses and the **death strain**, which is only the
0.1% uplift over the unit fund because the rest of the death benefit is funded by
cancelling the policyholder's own units.

Getting that split right is most of the work. Every benefit this contract pays —
death, surrender, withdrawal — is funded by cancelling units, so a naive gross
presentation would count the same money twice. Equally, the tax provision and the
fund-borne further costs reduce the unit fund but are **not** insurer income: booking
them as margin would overstate the insurer's year-one result by more than the annual
management charge itself.

**Spaces.** The model contains two:

:mod:`~.ULB_UK_S.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.ULB_UK_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.ULB_UK_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. Fund growth, the tax provision and the fund-based
charges accrue over the month; withdrawals, adviser charges and any rider charge are
unit cancellations at the end of it; death and surrender follow, deaths before
surrenders. Age is **age last birthday**. The projection ends at the limiting age or,
sooner, when the unit fund is exhausted — which on the deterministic base run it is,
because a 5% withdrawal against a 5% gross return net of tax and charges cannot be
sustained.

**What is sourced and what is not.** The contractual mechanics are sourced: the 100.1%
death uplift, the surrender value as the bid value of units with no penalty, the 7.5%
rolling withdrawal cap, charges accruing daily through the unit price, segmentation into
100 identical policies, and the liability cap to fund assets. Every rate is a
standardization. Per-fund charge rate cards are not published, the CMI's assured-lives
tables are restricted to Authorised Users, and no public UK bond persistency study was
retrieved, so the charge levels, the mortality basis and the whole surrender table are
placeholders. **This model is a mechanics demonstration, not a pricing or reserving
result.**

**Verification.** ``tests/test_unit_linked_bond_uk.py`` asserts the notes' worked
example to the penny — the month-by-month unit fund recursion, the year-one totals, and
the reconciliation that closes them — plus the insurer-side extraction beside it.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/unit_linked_bond/ULB_UK_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "ULB_UK_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

