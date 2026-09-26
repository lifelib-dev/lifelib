# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German selbstaendige Berufsunfaehigkeitsversicherung.

:mod:`~.BU_DE_S` is the executable counterpart of
``products/berufsunfaehigkeit/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows, undiscounted, for a single-policy
model point of a German standalone occupational-disability contract — a monthly
*BU-Rente* while the insured is *berufsunfaehig*, a *Beitragsbefreiung* for the same
period, and nothing at all otherwise — on a **monthly** grid over ``t = 0 ...
proj_len() - 1``.

Three things make this the German BU model rather than a translated disability rider.

**It is a four-ledger multi-state chain with a return arc.** *aktiv* (paying premium,
exposed to inception, active-lives mortality and lapse) becomes *leistungspflichtig*
(receiving the *BU-Rente*, premium-free, exposed to reactivation and to disabled-lives
mortality), which on a *Nachpruefung* termination becomes a **three-month run-off** in
which the annuity is still paid, and only then returns to *aktiv*. Death and lapse are
the only absorbing exits, so inception, recovery and reactivation are internal transfers
and must not appear in the closure identity. The run-off is § 174 VVG in arithmetic: the
insurer stays liable to the end of the third month after the notice reaches the
policyholder, so a recovery does not release the liability in the month it happens.
:func:`~.BU_DE_S.Projection.check_runoff_roll_fwd` and
:func:`~.BU_DE_S.Projection.check_dis_roll_fwd` assert both ledgers close.

**The premium is quoted as two numbers.** The *Bruttobeitrag* is the contractually
guaranteed maximum, struck on *Rechnungsgrundlagen erster Ordnung*; the *Zahlbeitrag*
actually charged is ``beitragsverrechnung`` times it, the anticipated *Ueberschuss*
credited in advance under § 153 VVG through § 176. Both are published —
:func:`~.BU_DE_S.Projection.premiums` is the gross stream and
:func:`~.BU_DE_S.Projection.surplus_credit` the credit returned out of it — because a
model carrying only one of them either assumes the credit is permanent or overstates
collected premium by ``1 / 0.70 - 1``. No German BU rate card exists in this library's
source corpus, so the *Bruttobeitrag* is **derived** by an equivalence on a stated
first-order basis rather than read from a table.

**The premium is weighted by the premium-paying count, not by the in-force count.**
``pols_prem(t)`` is ``pols_actv(t)`` plus the disabled cohorts still inside the
*Karenzzeit*: charging premium to lives in claim silently deletes the
*Beitragsbefreiung*, which is core cover and not an option.

**Spaces.** The model contains two:

:mod:`~.BU_DE_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.BU_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the worked example's anchor cell. It reaches
    the input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.BU_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed
there would re-read every file for every policy. In ``Data`` they are evaluated once,
however many policies are projected.

Input data is **external**: plain CSVs in the model folder's parent directory, read at
run time rather than stored inside the model. The model folder holds nothing but
formulas — no ``_data/``, no IOSpec, no embedded values — so the model and its inputs
must travel together, and a diff of the model shows logic changes only.

**Projection basis.** Monthly steps, matching the *BU-Rente* paid monthly in advance and
the retail monthly premium. ``t`` is the policy month, **0-based**: ``t = 0`` is the
first projected month — the month of inception for a new-business point, the valuation
month for an in-force one — and ``proj_len()`` is the **number** of projected months, the
exclusive end of the frame, so ``result_cf()`` runs ``t = 0 ... proj_len() - 1`` and ends
there — 444 rows on the anchor cell. Premium, the surplus
credit, administration expense, the *BU-Rente* and the claim-maintenance cost fall at
the **start** of the month; every state transition and the claim-assessment cost at the
**end** of it.

**What is sourced and what is not.** The mechanics are the established German ones and
each carries the instrument it must be checked against: the *Berufsunfaehigkeit*
definition and its 50 % / six-month concretisation, the *Anerkenntnis* and *Nachpruefung*
frame with its three-month run-off, the *Beitragsbefreiung*, the *Brutto* / *Zahlbeitrag*
pair, the unisex rule, and the absence of any death, maturity or surrender benefit.
**Every level is a standardization.** The DAV 1997 family (inception, reactivation and
disabled-lives mortality) and DAV 2008 T are the property of the Deutsche
Aktuarvereinigung, are not public and are **not redistributed here** — they are cited by
name and the model ships anchored ``[std]`` proxies instead. No German insurer publishes
a BU charge structure, lapse rate or rate card, and a pure risk contract carries no
*Effektivkosten* disclosure, so the charges and the premium are ``[std]`` too.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the decrement, charge and premium bases with company data before drawing any conclusion
from the output.

**Model points.** Thirteen, covering both premium forms, all four payment frequencies,
an in-force active policy, an in-force policy already in claim, a *Karenzzeit*, an
*Endalter* of 60, a *Leistungsendalter* below the *Versicherungsdauer*, the *AU-Klausel*
switched on, a *Risikozuschlag*, a point with both escalation options off, and a premium
override. Model point 1 is the anchor cell of the worked example in the technical notes,
and model points 2 and 3 are one-attribute neighbours of it so that the unisex invariance
and the occupational loading can be measured against it rather than inferred.

**Verification.** ``tests/test_berufsunfaehigkeit_de.py`` asserts the notes' worked
example to the cent and ``pols_if`` to six decimals, the derived annual *Bruttobeitrag*,
and one test per listed modeling pitfall. ``tests/test_model_conventions_de.py`` asserts
the house style, including delib's two rulings: every model publishes
:func:`~.BU_DE_S.Projection.check_net_cf`, and every input CSV but the model point table
carries a populated ``provenance`` column.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/berufsunfaehigkeit/BU_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "BU_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
