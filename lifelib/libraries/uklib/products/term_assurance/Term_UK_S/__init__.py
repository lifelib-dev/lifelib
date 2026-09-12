# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for UK guaranteed-premium term assurance.

:mod:`~.Term_UK_S` is the executable counterpart of
``products/term_assurance/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of
UK term assurance in the three benefit shapes the representative product offers —
**level**, **decreasing** at a client-selected schedule rate, and **family income
benefit** — with terminal illness inside the death decrement, an optional RPI
indexation option, and **no tail states of any kind**: cover ceases at the end of the
term with no maturity value, no renewal and no conversion.

That last point is the structural difference from :mod:`.Term_US_S`, the U.S. model in
the same library. A U.S. level premium term policy jumps to ART rates at the end of
the level period and runs on to attained age 95; a UK policy simply stops. There is no
post-level-term phase, no shock lapse, no jump ratio and no mortality deterioration
factor here, and importing them would materially misstate UK term liabilities.

**Spaces.** The model contains two:

:mod:`~.Term_UK_S.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Term_UK_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Term_UK_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. The time index ``t`` is 0-based and counts policy
months from issue: ``t = 0`` is the issue month, the policy year containing month ``t``
is ``t // 12 + 1``, and the frame runs ``t = 0, 1, ..., proj_len() - 1``, where
``proj_len() = term_mths() = 12 x policy_term()`` is the number of policy months; an
in-force model point opens at ``t = 12 x duration_inforce()``. Premiums, maintenance
expense and renewal commission fall at the start of the month; death and terminal
illness claims and their claim expense at the end; lapses act on the survivors of
mortality, death before lapse. Acquisition expense and initial commission fall at
issue, in ``t = 0``.

The notes take an annual grid as their base and name a monthly one as the arbiter of
its two approximations — the mid-year benefit balance of the decreasing shape and the
annual-in-advance premium, which they call an offsetting pair. This model is that
monthly grid, so neither approximation is here: the decreasing benefit is the exact
schedule balance of the month the claim falls in, the premium is the contractual
monthly one and stops the month the policy leaves, and family income benefit
instalments are counted one by one rather than rounded to six in the year of death and
twelve thereafter. ``premium_mode`` is live rather than inert — an annual payer is
charged twelve months' premium in the first month of each policy year — and the waiver
rider's 26-week deferred period is carried as six months between incidence and the
first waived premium. The assumption tables stay in the annual units they are quoted
in, converted month by month with ``1 - (1 - r)^(1/12)``, the notes' own convention.

**What is sourced and what is not.** The contractual mechanics are sourced: the
decreasing-shape amortization, the family income benefit as an annuity-certain to the
end of the term, terminal illness as a 100% acceleration rather than an extra benefit,
the absence of any surrender value, and the indexation option's cover and premium
caps. Everything quantitative is a standardization introduced for the reference
implementation. No UK insurer publishes premium rate tables — pricing is quote-driven,
and only the £5/month minimum is public — and the current CMI "16" Series assured
lives tables are subscriber-restricted, so both the premium and the mortality basis
shipped here are constructed. **This model is a mechanics demonstration, not a pricing
or reserving result.** Replace the assumption tables with company data, and the
mortality basis with licensed tables, before drawing any conclusion from the output.

**Model points.** Eight, covering all three benefit shapes, both mortality bases, the
indexation option, a joint first-death policy, waiver of premium, family income
benefit commutation, and one policy already in force at duration 5. Model point 1 is
the anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_term_assurance_uk.py`` asserts the notes' worked-example
rows and their policy-year totals to the penny and the in-force column to six decimals,
the anniversary identity that ties ``pols_if(12y)`` to an annual-grid roll-forward of
the same table, the ``B(60) = £134,588`` decreasing-schedule anchor, and the family
income benefit ledger against an independent rebuild.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/term_assurance/Term_UK_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Term_UK_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

