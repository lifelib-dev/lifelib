# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German fondsgebundene Rentenversicherung.

:mod:`~.FRV_DE_S` is the executable counterpart of
``products/fondsgebundene_rentenversicherung/technical-notes.md`` in the lifelib-products
library. It projects gross best-estimate liability cash flows for a single-policy model
point of a German **unit-linked deferred private annuity** — Schicht 3, single life,
one fund, no *Beitragsgarantie* — over the ***Aufschubzeit* only**, on a **monthly**
grid. At the end of month ``proj_len() - 1``, the frame's last, the units are cancelled,
the *Fondsguthaben* is converted at the *Rentenfaktor*, and the contract leaves this
model: the payout phase belongs to ``products/sofortrente/``.

Three things make this the unit-linked model rather than a translated general-account
one.

**The insurer guarantees the number of units, not their value.** There is no
*Rechnungszins* in the accumulation phase, no *Deckungskapital*, no *Zinsüberschuss* and
— because the *Anlagestock* holds the covering assets in the very units the liability is
denominated in — **no investment-mismatch term anywhere in the model**. The state
variable is :func:`~.FRV_DE_S.Projection.units_pp`; euro are derived from it and a unit
price. Every charge is either withheld from the *Beitrag* before units are bought or
levied by cancelling units that already exist, and which of the two it is decides what
happens when premiums stop.

**``net_cf`` is the non-unit stream, and that is the model's single most important
convention.** Every benefit paid before *Rentenbeginn* — the death benefit up to the
fund, the *Rückkaufswert*, the *Teilentnahme*, the capital released at *Rentenbeginn* —
is funded by cancelling the policyholder's own units, so a gross presentation would
count the same money twice. ``net_cf(t)`` is therefore *charges collected, less insurer
expenses, less the death strain*. The gross flows are published beside it —
``premiums``, ``prem_to_av``, ``claims_death``, ``claims_lapse``, ``claims_maturity``,
``withdrawals``, ``av_releases`` are all ``result_cf()`` columns — and
``check_benefit_funding()`` asserts that they net exactly, so the exclusion is visible in
the frame rather than merely asserted in prose.

**Two mortality bases at once.** The *Risikobeitrag* the tariff charges is priced on a
**death** table (DAV 2008 T, first order); the projection decrements on the
**second-order** best estimate. The wedge between them is the *Risikoergebnis*, and with
the shipped flat ``mort_be_factor = 0.75`` it is exactly 25 % of the *Risikobeitrag*
collected. A model that uses one basis for both makes the risk result identically zero
and deletes the mechanic. The *Rentenfaktor* rests on a third basis again — an annuity
table, DAV 2004 R — which is why no cells reads both tables.

**Spaces.** The model contains two:

:mod:`~.FRV_DE_S.Data`
    Reads the six input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.FRV_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.FRV_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps, which the contract forces rather than the modeller
choosing: the dominant premium frequency is monthly, the *kapitalbezogenen
Verwaltungskosten* and the *Risikobeitrag* are levied monthly by unit cancellation, and
the *Abschluss- und Vertriebskosten* instalment runs for exactly **60 months**. An
annual grid cannot place the month-60 cliff, and that cliff is the characteristic shape
of a German unit-linked contract's early values. ``t`` is the **0-based** policy month
counted from the contract's own inception — ``t = 0`` is the inception month — so
``t = 60`` means the same thing on every model point. The frame is
``range(proj_start(), proj_len())`` with ``proj_start() = duration_init_m`` and
``proj_len() = 12 x (annuity_age - entry_age)``, the **number** of policy months and so
the frame's exclusive end; an in-force model point simply opens partway through it. The
contractual policy year is the 1-based label ``t // 12 + 1``.

**What is sourced and what is not.** The mechanics are common ground in German practice:
the *Beitragsverrechnung* order, the five-year spreading of the acquisition charge, the
*Beitragsrückgewähr* death benefit and its net amount at risk, the *Zeitwert*
*Rückkaufswert*, the ``max(guaranteed, current)`` *Rentenfaktor* rule, and the survival
of the fund-based charges into a *beitragsfrei* contract. The **levels** are almost
entirely standardizations: **no charge rate, no *Rentenfaktor*, no lapse rate and no
expense loading was established at any carrier**, and no document cited in this library
was retrieved. The one anchor in the whole charge stack is the *Höchstzillmersatz* of
25 ‰ of the *Beitragssumme*, and the shipped tariff takes the cap rather than a guessed
interior point. The DAV tables — DAV 2008 T for the risk charge, DAV 2004 R behind the
*Rentenfaktor* — are the property of the Deutsche Aktuarvereinigung, are not public and
are **not redistributed here**: they are cited by name and stood in for by anchored
**[std]** proxies. **This model is a mechanics demonstration, not a pricing, reserving
or disclosure result.** Nothing it produces may be quoted as an *Effektivkostenquote* or
compared with a PRIIPs performance scenario, and its charge levels must be replaced with
a real tariff before any quantitative use.

**Model points.** Thirteen, covering both premium forms, all four payment frequencies,
an in-force cell opening at duration 96, a *beitragsfrei* cell on a zero-return fund, a
*Zuzahlung* and a *Teilentnahme*, a *Beitragsdynamik*, a *Nettotarif* on an ETF, a
two-year premium term inside a twelve-year deferment on a stress path, a cell with a
non-zero *Stornoabzug*, and a *Rentenbeginn* at 70 where the current *Rentenfaktor*
exceeds the guaranteed one so the ``max()`` bites. Model point 1 is the anchor cell of
the worked example in the technical notes.

**Verification.** ``tests/test_fondsgebundene_rentenversicherung_de.py`` asserts the
notes' worked example to the cent and ``pols_if`` to six decimals, and one test per
listed modeling pitfall. Seven ``check_*()`` cells travel with the model itself.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/fondsgebundene_rentenversicherung/FRV_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "FRV_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
