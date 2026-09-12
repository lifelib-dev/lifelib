# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for a French multisupport contract, UC leg.

:mod:`~.UC_FR_S` is the executable counterpart of
``products/assurance_vie_uc/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-policy model point of a standardized
`contrat d'assurance vie multisupport`: a single premium split between one composite
`unités de compte` support and one `fonds en euros`, a management charge levied monthly
by cancelling units, and an optional age-rated `garantie plancher` — a floor death
benefit charged on the `capital sous risque`.

**The decomposition is the model.** French practice splits this contract exactly as UK
practice splits a unit-linked bond, and so does this implementation:

*the unit leg* — a **count** of units valued at an exogenous liquidation value. Art.
A. 132-5 requires every contract to state that the insurer commits on the number of
units and not on their value, so the count is the state variable, every charge is a unit
cancellation, and — while the plancher premium is taken from the euro support — the count
is a deterministic, market-independent sequence; and

*the non-unit cash flow* — what accrues to the insurer: the premium charge, the UC
management charge, the arbitrage fee and the plancher premium, less expenses and the
plancher **death strain**, which is exactly the `capital sous risque` and nothing else,
because the whole of the account value is funded by cancelling units and by the euro
balance.

**The garantie plancher is the insurance content.** Its charge base is the net amount at
risk, not the account value: on the anchor cell at ``t = 11`` the correct charge is 27.18 €
and the charge on the account value would be 126.35 €, a factor of 4.6. The net amount at
risk is floored at zero, so the rider costs nothing while the units are above the floor
and the strain never turns into a rebate; it is capped at 300,000 €, and the cap applies
to the risk rather than to the benefit. :func:`~.UC_FR_S.Projection.check_nar_bounds` and
:func:`~.UC_FR_S.Projection.check_unit_roll_fwd` assert both.

**The euro leg is a pointer.** It enters as an allocation share carrying an annual
credited rate net of its own management charge, because that is all the UC leg needs it
for — the euro balance sizes the `capital sous risque` and is the first source the
plancher premium is levied from. `Taux minimum garanti`, `participation aux bénéfices`,
the `provision pour participation aux bénéfices` and the `effet cliquet` belong to
``products/assurance_vie_euro/`` and model ``Euro_FR_S``, and are neither restated nor
re-implemented here. Reading ``net_cf`` as the contract's total margin is therefore a
modeling error: it is the UC leg plus the rider, and the euro leg's margin must be added
from outside.

**Spaces.** The model contains two:

:mod:`~.UC_FR_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.UC_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.UC_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, ``t`` counting policy months from issue and
**0-based**: ``t = 0`` is the issue month, period ``t`` runs from time ``t`` to time
``t + 1``, and the frame is ``t = 0 … proj_len() − 1``, so ``result_cf()`` has
``proj_len()`` rows. A contractual policy year is the 1-based label ``t // 12 + 1``.
Within month ``t``: the liquidation value moves and the euro leg accrues; the management
charge is taken on the units held at the **start** of the month; arbitrages and
withdrawals settle; the `capital sous risque` is observed; the plancher premium is levied;
decrements act at the end of the month, deaths before surrenders. The balances **at
issue** are not a row of the frame — they are the ``*_init`` cells, read into month 0
through the opening cells ``units_open``, ``unit_price_open``, ``av_euro_open_pp`` and
``av_pp_at(t, "OPENING")``. Age is **age last birthday** and the tariff steps at each
policy anniversary. The projection runs for the model point's own ``proj_len`` months —
the contract is whole of life and has no maturity date.

**What is sourced and what is not.** The contractual mechanics are sourced: the unit
count as the thing guaranteed, the death benefit as the account value plus the `capital
sous risque`, the 300,000 € cap with the excess reducing the floor, cessation at attained
age 75, the charge on the net amount at risk by attained age, the levy from the euro
support first, the pro-rata split of a partial surrender, the surrender value as the
account value with no exit charge, the `prélèvements sociaux` at 17.2% levied on the UC
leg only at `dénouement`, and the Spirica tariff itself. Every **rate** is a
standardization. No insurer publishes the mortality table, the age definition, the
loading or the margin behind a plancher tariff, no French persistency or arbitrage study
was retrieved, and no unit-return assumption is published, so the mortality basis, the
surrender table, the charge levels and the return scenarios are placeholders. **This
model is a mechanics demonstration, not a pricing or reserving result.**

**Verification.** ``tests/test_assurance_vie_uc_fr.py`` asserts the notes' worked example
to the centime — the month-by-month unit count, account values, floor and net amount at
risk, the four `plancher_basis` variants on the same path, the settlement arithmetic of
the partial surrender, and the insurer-side extraction beside it — plus one test for each
modeling pitfall the notes list.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/assurance_vie_uc/UC_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "UC_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
