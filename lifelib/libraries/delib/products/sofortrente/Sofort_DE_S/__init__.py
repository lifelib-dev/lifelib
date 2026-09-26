# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German sofortbeginnende Rentenversicherung.

:mod:`~.Sofort_DE_S` is the executable counterpart of
``products/sofortrente/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single model point of a German
*sofortbeginnende private Rentenversicherung* — the immediate payout annuity bought
outright with one *Einmalbeitrag* — on a **monthly** grid, undiscounted. One payment in
at inception; a stream of instalments out until death, floored by a *Rentengarantiezeit*
or a *Kapitalrückgewähr*, lifted by a declared *Überschussrente*, and extended past the
annuitant's death by a *Hinterbliebenenrente* where one was bought.

Three things make this the payout model rather than a shortened accumulation one.

**There is no behavioural assumption in it at all.** Once the *Rentenbezug* has begun the
policyholder has no right of termination, no *Rückkaufswert*, no *Beitragsfreistellung*
and no capital option (§ 168 Abs. 3 VVG, with § 169 displaced and § 165 inapplicable), so
the model carries no lapse rate, no paid-up state, no surrender cells and no account
value. The only decrement is death. That is a statutory fact about the product, not a
modeling simplification, and it makes this the one model in the library whose answer
depends purely on the mortality basis and the surplus assumption.

**The Rentengarantiezeit is a certain floor, not a second stream.** Inside the guarantee
period the instalment is payable whether the annuitant is alive or not, so the payment
weight is ``max(certain_floor(t), lives_if(t))`` and never ``certain_floor(t) +
lives_if(t)``; the additive reading pays ``1 + l`` for the whole guarantee and nearly
doubles the first ten years' outgo. The survivor's leg carries a ``(1 - certain_floor)``
gate for the same reason. :func:`~.Sofort_DE_S.Projection.check_guarantee_certain` and
:func:`~.Sofort_DE_S.Projection.check_payment_factor` assert both, on every model point.

**The mortality surface is generational and the tariff is unisex.** ``q`` is read at
``(attained age, birth cohort)`` rather than at ``(attained age, projection year)``, so
two annuitants of the same age and different cohorts are priced on different mortality;
and the tariff annuity factor is struck on a blended unisex basis while the projection
decrements on the model point's own sex, because German new business has been unisex
since 21 December 2012. The first-order margin reaches the improvement **trend** as well
as the level, which is what prudence means for an annuity.

**Spaces.** The model contains two:

:mod:`~.Sofort_DE_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Sofort_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Sofort_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many points are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, ``t`` counted in complete months from
*Vertragsbeginn*, on a **0-based** frame: a new-business point opens at ``t = 0``, which
is both the month the *Einmalbeitrag* arrives and — under the representative *vorschüssig*
convention — the month the first instalment is paid. An in-force point opens at
``t = duration_mth_init()``, the months it has already run. ``proj_len()`` is the
**exclusive end** of the frame — the frame is ``range(t_start(), proj_len())``, its last
month index is ``proj_len() - 1`` and it carries ``proj_len() - t_start()`` rows — taken
as the maximum of the annuitant's survival horizon, the guarantee period's own end and
the second life's horizon where a survivor's annuity is in force.

**What is sourced and what is not.** The mechanics are sourced: the conversion of the
*Einmalbeitrag* at a factor struck once at inception on DAV 2004 R and a *Rechnungszins*
at or below the *Höchstrechnungszins*; the *Rentengarantiezeit* as a tariff-level feature;
the *Kapitalrückgewähr* as the *Einmalbeitrag* less the instalments already paid; the
*Hinterbliebenenrente* as a rider on a second life; the statutory *Überschussbeteiligung*
continuing through the payout phase; and the absence of any surrender or paid-up value.
**Every level is a standardization.** No search was run for this product — the session's
search budget was exhausted before it began — so no annuity rate, no charge, no surplus
declaration and no portfolio mix was established at any carrier for any year. DAV 2004 R
and DAV 2004 R-Bestand are the property of the Deutsche Aktuarvereinigung, are not public
and are **not redistributed here**: they are cited by name and a documented [std] proxy
ships in their place. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the decrement, charge and surplus tables with company data
before drawing any conclusion from the output.

**Model points.** Fourteen, covering the plain *Leibrente*, each death-benefit option in
turn, a joint-life cell with a younger second life, all four payment frequencies, both
payment timings, all four *Überschussverwendung* forms, a five-year *Aufschubzeit*, an
in-force point carrying an annuity struck in 2012 on a 1,75 % tariff, a pre-2025
*Höchstrechnungszins* vintage, both ends of the issue-age envelope and a cell with the
*Überschussrente* switched off. Model point 1 is the anchor cell of the worked example in
the technical notes.

**Verification.** ``tests/test_sofortrente_de.py`` asserts the notes' worked example — the
anchor cell's cash flows to the cent and its probabilities to six decimals — the derived
guaranteed instalment and the annuity factor behind it, and one test per listed modeling
pitfall.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/sofortrente/Sofort_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Sofort_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
