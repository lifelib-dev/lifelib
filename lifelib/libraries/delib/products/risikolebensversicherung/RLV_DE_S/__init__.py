# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German Risikolebensversicherung.

:mod:`~.RLV_DE_S` is the executable counterpart of
``products/risikolebensversicherung/technical-notes.md`` in the lifelib-products
library. It projects gross best-estimate liability cash flows for a single-policy model
point of a German standalone term assurance — the *Versicherungssumme* paid as a
*Todesfallleistung* on death inside the *Versicherungsdauer*, and **nothing at all**
otherwise — on a **monthly** grid, undiscounted.

Three things make this the German model rather than a translated French or British one.

**The customer is not billed the premium the contract guarantees.** The tariff premium
is the *Bruttobeitrag*, struck on prudent first-order *Rechnungsgrundlagen*, and it is
the maximum the policyholder can ever be required to pay. What is billed is the
*Zahlbeitrag*: the *Bruttobeitrag* less a declared *Beitragsverrechnung*, which is how
§ 153 VVG's surplus entitlement is delivered on a product with no account to credit. The
MindZV obliges the insurer to allocate at least 90 % of the *Risikoergebnis* to
policyholders, and on a term product the *Risikoergebnis* is essentially the whole
technical result, so the spread is wide: on the worked example's anchor cell the
*Beitragsverrechnungssatz* comes out at 0.4253 and the billed premium at 57,5 % of the
guaranteed one. The model therefore publishes **two premium streams** — ``prem_gross``,
the guaranteed one, and ``premiums``, the billed one that enters ``net_cf`` — and
``prem_rebate`` between them. A model carrying one premium stream cannot represent this
product, and the *Beitragsverrechnungssatz* is **derived** from the surplus mechanic
rather than assumed, because that is what it is in the real contract.

**The tariff is unisex and the projection is not.** Sex may not enter a German premium
for contracts concluded from 21 December 2012, while the DAV 2008 T tables the tariff is
built on remain sex-distinct, so every German term tariff is a blend at a mixing ratio
the carrier chooses. ``mort_rate_tar`` prices on a 50/50 blend and ``mort_rate``
projects on the policy's own sex, so the cross-subsidy appears in the cash flows instead
of in the price: model points 1 and 2 differ only in ``sex``, pay the same premium to the
last cent, and have claim totals differing by a factor near two.

**There is no cash value anywhere.** § 169 Abs. 1 VVG confines the surrender-value duty
to a life insurance whose insured event is certain to occur, which a term assurance's is
not, and § 165's paid-up right collapses into the same nil through the minimum-benefit
test. So the model has no account value, no ``av_pp_at``, no surrender cells and no
paid-up state, and ``claims(t, "LAPSE")`` and ``claims(t, "MATURITY")`` are structurally
zero at every ``t``. ``check_no_cash_value()`` asserts it on every model point rather than
leaving it to prose. What is *not* true is that nothing accumulates: a level premium
charged against a rising death rate builds a small *Deckungskapital* that peaks near the
middle of the term and runs off to exactly zero at expiry, and ``res_pp_at`` publishes it
as a **pricing diagnostic**. Concluding from "no *Sparanteil*" that there is no reserve is
the modelling error this product invites, and ``check_res_roll_fwd()`` is what catches it.

**Spaces.** The model contains two:

:mod:`~.RLV_DE_S.Data`
    Reads the six input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.RLV_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.RLV_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps. The time index ``t`` is **0-based** and counts policy
**months** from issue: ``proj_len() = 12 x policy_term`` is the number of projected months
and the frame's exclusive end, a new-business point opens at ``t = 0`` and an in-force
point at ``t = 12 x duration_y``, so the frame is ``t = 12 duration_y … proj_len() - 1``.
The **product is annual and stays annual**: ``duration(t) = t // 12`` and
``policy_year(t) = duration(t) + 1`` are derived and never indexed by, and everything the
contract puts on the anniversary stays there — ``age(t) = issue_age + duration(t)``, the
*Versicherungssumme* schedule, the § 161 three-year window, the *Beitragszahlungsdauer*
and the whole first-order equivalence, whose *Bruttobeitrag*, *Nettoprämie*,
*Beitragsverrechnungssatz* and *Deckungskapital* are unmoved by the conversion. What the
finer grid resolves is the timing: ``mort_rate`` and ``lapse_rate`` are the policy year's
**annual** rates and ``mort_rate_mth`` and ``lapse_rate_mth`` the monthly rates derived
from them at ``1 - (1 - r)^(1/12)``, so twelve of each compound back to the year's rate
and ``pols_if`` at every anniversary is the annual-step model's own figure.

A *Zahlbeitrag* **instalment** on the *Zahlweise*'s own cycle, its collection cost and the
renewal commission on it fall at the start of the month; a twelfth of the sum-related
admin charge accrues each month on the opening in-force; acquisition cost and initial
commission fall in month 0 and never on an in-force point, where they are sunk; death
claims and the claim expense at the end of the month of death; lapses at the end of the
month, after the death decrement; the expiry at the end of the last month
``t = proj_len() - 1``, paying nothing. ``result_cf_annual()`` sums the monthly frame into
policy years, which is the view the technical notes' worked example is stated on.

**What is sourced and what is not.** The contractual mechanics are sourced, if only ever
through inherited corroboration: the guaranteed *Bruttobeitrag* and the non-guaranteed
*Zahlbeitrag*, the MindZV's 90 % minimum allocation from the *Risikoergebnis*, the
three-year *Selbsttötung* window of § 161 VVG and its substitution of a *Rückkaufswert*
that is nil here, the absence of any surrender or paid-up value, the unisex rule, and the
*Höchstrechnungszins* and *Höchstzillmersatz* the tariff is bounded by. **Every price,
charge, margin and behavioural level is a standardization.** No German insurer publishes a
mortality table, a *Sicherheitszuschlag*, an expense loading, a commission scale, a lapse
rate or a *Beitragsverrechnungssatz* for this product, and the DAV 2008 T tables — DAV
2008 T NR and DAV 2008 T R — are the property of the Deutsche Aktuarvereinigung, are not
public, and are cited by name rather than redistributed here. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the decrement and rate tables
with company data, and the charge parameters with a real tariff's, before drawing any
conclusion from the output.

**Model points.** Fourteen, covering both premium forms, all four *Zahlweisen*, all three
*Versicherungssumme* shapes, an in-force point opening at ``t = 12``, a
*Nachversicherungsgarantie* with two increments, *verbundene Leben*, a *Risikozuschlag* on
an impaired smoker, the § 153-excluded non-participating tariff, an *abgekürzte
Beitragszahlungsdauer*, and two boundary cells at the ends of the issue-age and term
envelopes. Model point 1 is the anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_risikolebensversicherung_de.py`` asserts every row of the
notes' twenty-five-year worked example to the cent — on ``result_cf_annual()`` — and the
twelve months of policy year 1 on the monthly frame beside it, ``pols_if`` to six
decimals, the *Bruttobeitrag* 1 275,411882 € and the *Beitragsverrechnungssatz*
0,42527476 behind it, and one test per listed modeling pitfall.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/risikolebensversicherung/RLV_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "RLV_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
