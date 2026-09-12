# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for French eurocroissance business.

:mod:`~.EC_FR_S` is the executable counterpart of
``products/eurocroissance/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single-policy model points on the
two composite chassis those notes specify — **Chassis A**, the 1° engagement carrying a
*provision mathématique* alongside *parts de provision de diversification*, and
**Chassis B**, the 2° engagement carrying parts only with a capital guarantee that bites
at the *échéance* and nowhere before it.

**Two provisions, two state variables, and one rebalancing a year — on a monthly grid.**
That sentence is the model. The *provision mathématique* is the guaranteed amount discounted at the
A. 134-1 rate; the *provision de diversification* takes whatever the account's assets
leave over, floored at the parts' minimum value. Neither is a cash flow. The policy's
cash flows are *versements* in and surrender, death and maturity claims out; the two
provisions reach them only through the R. 134-5 surrender and R. 134-6 maturity
formulas.

**The provision mathématique is re-struck, never accumulated.** ``pm(t)`` is ``mg(t)``
discounted at the *current* rate — ``i_pm(t + 1)``, the rate of the month's own end-of-month
striking, over the fractional remaining term — so it lands on the guarantee exactly at the
*échéance* whatever the path of rates: in the last projected month the two are
identically equal. That is what makes
the Chassis A guarantee pre-funded by construction, and it is why an in-force model point
carries no accumulated PM — the model re-derives it, and
``Projection.check_pm_restruck`` asserts the shipped extract agrees.

**The Chassis B surrender value is not guaranteed.** Before the *échéance* a 2°
engagement pays ``parts × part value`` and nothing else. At the anniversary of the notes'
policy-year-6 shock — month ``t`` = 71 — that
is 9,899.22 against a guarantee of 11,760.00 — 84.18% of net *versements*. A model that
floors it is modelling a contract that does not exist, and that is this product's central
error. The monthly grid prices an exit on the striking of the month it falls in, as
A. 134-5 requires, so a surrender in month 65 pays 11,430.63 instead.

**The insurer's own funds never reach a policyholder before the term.** The L. 134-3
contribution completing the representation and the *provision pour garantie à terme* are
computed, reported and kept out of every benefit column;
``Projection.check_own_funds_not_paid`` asserts it.

**Spaces.** The model contains two:

:mod:`~.EC_FR_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.EC_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.EC_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, because A. 134-5 requires the diversification
provision to be re-struck at an intermediate value **at least monthly** and prices an exit
on a *forward* part value — the next striking after the request — which an annual grid can
only standardize away. ``t`` counts **policy months** from issue and is **0-based**: month
``t`` runs from time ``t`` to time ``t + 1``, so ``t = 0`` is the issue month. The frame is
``range(proj_start(), proj_len())`` — ``proj_len() = 12 × policy_term()`` is the number of
months projected, the last row is ``proj_len() - 1``, and that row ends at the *échéance*.
An in-force cell opens at ``proj_start() = 12 × duration_ifo``, always the first month of a
policy year. The initial *versement* is not a row of its own: it creates the rights and
strikes both provisions as the **opening state** of the first projected month, reached as
``own_assets_at(t, "BOM")`` and its siblings. The contractual policy year is the derived
1-based label ``policy_year(t) = t // 12 + 1``, and it is what the *rachat* table, the
*versement* schedule, the lock-up and the *apport* are keyed by. Age is *âge atteint* and
steps on the anniversary.

Assumptions stay annual and the grid underneath them gets finer. ``mort_rate(t)``,
``lapse_rate(t)``, ``wd_rate(t)`` and ``asset_return(t)`` are the **annual** figures the
technical notes tabulate; ``mort_rate_mth(t)``, ``lapse_rate_mth(t)``, ``wd_rate_mth(t)``
and ``asset_return_mth(t)`` are what the month applies, ``1 - (1 - q)^(1/12)`` and
``(1 + r)^(1/12) - 1``, so twelve compound back to exactly the annual figure. Contractual
terms stay where the contract puts them: the base 4° parts levy and a scheduled
*versement* in the **first month of a policy year**; the striking of the *compte de
participation aux résultats*, the base 5° performance levy on the year's accumulated
performance, the insurer's asset affectations and any free *versement* **on the
anniversary**, in that order. Both provisions are re-struck **every month**; the asset
return accrues over the month; decrements and claims follow at its end.

**What reconciles, and what does not.** Because the monthly rates compound back to the
annual ones and every contractual event sits on a year boundary, every anniversary-dated
value — the assets, both provisions, the parts and their value, the guaranteed amount, the
insurer's own-funds items and every exit value — is exactly what the annual-step model this
one replaced carried on the same row, to 1.3e-10 EUR across all eleven shipped model
points, and ``pols_if(12k)`` is its opening in-force. The **cash flows** are not and are
not meant to be: a claim falls at the end of the month of exit, maintenance expense accrues
at one twelfth a month on the in-force and the provision of each month rather than of the
anniversary, and on the one cell that takes *rachats partiels* the exit cash leaves in
twelve instalments. Those timing differences are the reason for the finer grid, and
``technical-notes.md`` quantifies each of them.

**What is sourced and what is not.** The mechanics are sourced, and unusually completely
so: eurocroissance is a statutory construct, and arts. L. 134-1 to L. 134-5,
R. 134-1 to R. 134-12 and A. 134-1 to A. 134-7 of the Code des assurances fix the
provision definitions, the six permitted charge bases, the surrender and maturity values,
the minimum part value, the 90%-of-TEC discount ceiling and the PGT. Every *rate* is a
standardization: no *notice d'information*, *conditions générales* or PRIIPs *document
d'information clé* for any eurocroissance support was retrieved, the regulatory mortality
tables are cited but never shipped, and no eurocroissance lapse experience is public.
**This model is a mechanics demonstration, not a pricing or reserving result.**

**Verification.** ``tests/test_eurocroissance_fr.py`` asserts both chassis of the notes'
worked example row by row to the cent at the anniversary months — the asset roll, the
parts levy and its base, the performance levy, the re-strike of the PM and its rate/time
decomposition, the minimum part value, the insurer's contribution, the PGT, the
policy-year-3 *versement* split, and every exit value the two chassis pay — and the
monthly claims the conversion added: that twelve monthly rates compound back to the annual
ones, that no contractual event moves between anniversaries, and that the intermediate
value is struck in every month.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/eurocroissance/EC_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "EC_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
