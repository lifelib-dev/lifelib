# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German Pflegerentenversicherung.

:mod:`~.Pflege_DE_S` is the executable counterpart of
``products/pflegerentenversicherung/technical-notes.md`` in the lifelib-products library.
It projects gross best-estimate liability cash flows, undiscounted, for a single-policy
model point of a German private long-term-care annuity — a *Pflegerente* graded by the
five *Pflegegrade* of §§ 14, 15 SGB XI, with full *Beitragsbefreiung im Leistungsfall*,
on a **monthly** grid running to a terminal age of 110.

Three things make this the *Pflegerente* model rather than a translated disability one.

**The benefit is a multi-state ledger, not a single decrement.** The state space is
{aktiv, PG1 … PG5, storno, tot}. A life enters care at a grade drawn from
``inc_share``, deteriorates towards PG5, recovers towards PG1 and out to aktiv, and dies
from every state at a grade-increasing multiple of active-life mortality. The paying
state therefore has **three** exits, not one: death, a *Herabstufung* to a lower insured
grade, and a *Herabstufung* out of the insured grades altogether, on which the annuity
stops and the *Beitrag* revives. A model that treats "in claim" as one state exited only
by death overstates the liability; one that treats every downgrade as a termination
understates it. ``check_states()`` and ``check_waiver()`` assert the ledger and the
premium split that hangs off it, on every model point.

**Grade and mortality are correlated, and the highest-paying state is the shortest-lived.**
``mort_mult`` is a multiple on the **force** of active mortality — 1.5 at PG1 rising to
9.0 at PG5 — so the annuity in payment runs three to five years, not the fifteen to
twenty a healthy-life annuity would at the same age. Pricing this benefit on an annuity
table would be prudent in exactly the wrong direction. The consequence for the code is
that the annuity is weighted on ``esc_pg(t, g)`` grade by grade and never on an average
benefit percentage applied to an average survival curve.

**The premium is a priced quantity and the projection is not.** Where ``premium_mth``
is ``0.0`` on the model point, the level monthly *Beitrag* is struck by equivalence on
the **first-order** (*erster Ordnung*) bases — every rate carrying its prudence margin,
the sexes blended 50 / 50 because sex may not enter a German premium, and **no lapse** —
discounted at the *Rechnungszins*. That engine is the ``tar_*`` cells, it is the only
place a discount rate appears, and ``check_prem_equiv()`` closes it from the tariff
ledgers rather than from the closed form.

**Spaces.** The model contains two:

:mod:`~.Pflege_DE_S.Data`
    Reads the nine input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Pflege_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the worked example's anchor cell. It reaches the
    input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.Pflege_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: plain CSVs in the model folder's parent directory, read at
run time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, which are the contract's own grid rather than a
refinement of an annual one: the *Pflegerente* is a monthly annuity, the *Beitrag* a
monthly instalment, and the *Pflegegrad* can change in any month. ``t`` is the policy
month index, 0-based; the frame starts at ``duration_mth_init()`` — ``0`` for new
business, the elapsed duration for an in-force point — and runs to ``proj_len() - 1``,
where ``proj_len() = 12 * (omega_age - age_at_entry)`` is the **number of projected
months**, the exclusive end of the frame. The *Beitrag*, the *Pflegerente*
and the per-policy expenses fall at the **start** of the month; transitions act over the
month; surrender and death benefits fall at the **end** of it.

**What is sourced and what is not.** The contractual mechanics are cited: the statutory
*Pflegegrad* trigger, the *Beitragsbefreiung*, the level guaranteed *Beitrag* adjustable
only on the narrow § 163 VVG route, the 1,00 % *Höchstrechnungszins* of the DeckRV, the
25 ‰ *Höchstzillmersatz*, the § 169 VVG *Rückkaufswert* and *Stornoabzug* rules, and the
unisex pricing constraint. **Every biometric rate, every charge, every lapse rate and the
premium itself is a standardization.** No *Bedingungswerk*, *Produktinformationsblatt*,
*Tarifblatt* or premium quotation for any German *Pflegerentenversicherung* was retrieved
for this library, and DAV 2008 P — the German market's standard multi-state
*Pflegetafel* — is the property of the Deutsche Aktuarvereinigung, is not public and is
**not redistributed here**; it is cited by name and the shipped tables are ``[std]``
proxies anchored so the worked example reproduces exactly, never calibrations of it.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the decrement, expense and surrender tables with company data before drawing any
conclusion from the output.

**Model points.** Fourteen, covering both *Leistungsstaffeln*, all five payment modes
including the *Einmalbeitrag*, a shortened *Beitragszahlungsdauer*, a *Wartezeit* with a
*Karenzzeit*, a *Leistungsdynamik*, a *Beitragsrückgewähr*, a supplied premium with a
*Stornoabzug*, two in-force points — one of them already in claim — and both ends of the
observed entry-age band. Model point 1 is the anchor cell of the worked example in the
technical notes.

**Verification.** ``tests/test_pflegerentenversicherung_de.py`` asserts the notes' worked
example to the cent and ``pols_if`` to six decimals, the equivalence premium and the
actuarial values behind it, and one test per listed modeling pitfall.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/pflegerentenversicherung/Pflege_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Pflege_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
