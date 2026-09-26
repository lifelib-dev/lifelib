# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German kapitalbildende Lebensversicherung.

:mod:`~.KLV_DE_S` is the executable counterpart of
``products/kapitallebensversicherung/technical-notes.md`` in the lifelib-products
library. It projects gross best-estimate liability cash flows, **undiscounted**, for a
single-policy model point of the classic German endowment — the *gemischte Versicherung
auf den Todes- und Erlebensfall*, which pays a guaranteed *Erlebensfallleistung* at the
*Ablauf* if the insured is then alive and a guaranteed *Todesfallleistung* on earlier
death, both increased by the *Überschussbeteiligung* — on a **monthly** grid, over a
product whose every contractual mechanic stays on the **annual** clock it is written on.

This is the *Überschussbeteiligung* chassis the other nine delib products reuse in
modified form, and three things make it the German model rather than a translated one.

**The surplus rate multiplies a reserve, not a sum insured and not a premium.** The
declared *laufende Verzinsung* **is** the *Garantieverzinsung* plus the *laufende
Zinsüberschussbeteiligung*, so a declared 2,70 % on a 1,00 % guarantee is a **1,70 pp**
credit and never 2,70 pp on top of 1,00 pp: ``zins_ueberschuss_rate(t) = max(0,
decl_rate(t) - rechnungszins())``, applied to ``max(res_pp_at(t, "AFT_INT"), 0)``. Both
``max`` are load-bearing. A *gezillmerte Deckungskapital* is **negative at issue**, so a
positive rate on an un-floored base would credit a negative surplus; and on the ``nil``
scenario the declared rate falls below the guarantee, which the reserve still meets in
full, so the credit is zero rather than negative. How long the base stays negative is a
parameter question rather than a structural one: at the post-2015 25 ‰ ceiling over a
long *Beitragszahlungsdauer* the first Zillmer premium more than repays the zillmered
cost, and the floor is inert on every shipped model point; at the pre-2015 40 ‰ ceiling it
is not.

**There are three reserves and the product needs all three.** ``res_zill_pp`` is the
*gezillmerte Deckungskapital* the insurer holds, negative at issue and equal to
``-alpha_cost`` there; ``res_min_pp`` is the § 169 Abs. 3 VVG floor obtained by spreading
the acquisition cost evenly over the first five contract years, and on a long *gezillmert*
contract it **normally binds**; ``res_guar_pp`` is their maximum and is what the customer
actually gets. Publishing only the first understates the surrender value at essentially
every duration; publishing only the second loses the quantity the *Deckungsrückstellung*
and the *beitragsfreie Versicherungssumme* are built on.

**Making the contract paid-up is not a lapse.** § 165 VVG converts the contract to a
reduced *beitragsfreie Versicherungssumme* bought with the § 169 value — the policy stays
in ``pols_if`` — **unless** the resulting sum falls below the agreed
*Mindestversicherungsleistung*, in which case the statute obliges the insurer to pay the
§ 169 value instead and the election becomes a surrender. Model points 11 and 12 exercise
the two branches.

**Spaces.** The model contains two:

:mod:`~.KLV_DE_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.KLV_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the worked example's anchor cell. It reaches the
    input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.KLV_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, over an annual product. ``t`` is the policy **month**,
0-based and counted from issue, and the frame runs ``t = t_start() ... proj_len() - 1``
contiguously with ``t_start() = 12 x duration_init()`` and ``proj_len() = 12 x
policy_term()`` — the frame's exclusive end, with the *Ablauf* at the end of the last month.
There is no ``t = proj_len()`` row.

**The model carries two clocks and the argument of a cells says which.** Cells that state an
**annual account** take ``k``, the 0-based policy year: the whole pricing block, all three
reserves, the § 169 value, the paid-up purchase and every part of the
*Überschussbeteiligung*. Cells that state a **month** take ``t``: the in force, the claims,
the premium instalments and every ``result_cf()`` column. ``duration(t) = t // 12`` is the
bridge, ``policy_year(t) = duration(t) + 1`` the contractual 1-based label, and
``is_anniv(t) = (t % 12 == 11)`` the month the annual machinery acts in. The decrement rates
take ``t`` and return the **year's** annual rate; ``mort_rate_mth`` and ``lapse_rate_mth``
are what the recursion applies, at ``1 - (1 - r)^(1/12)``, so twelve of each compound back to
the year's rate and ``pols_if`` at every anniversary is what an annual-step model carries.
That is what leaves the whole annual layer — every reserve, every declared credit, every
ledger balance and the *Bruttobeitrag* itself — **bit-identical** to the annual-step model
this replaced.

A *Beitrag* **instalment** on the *Zahlweise*'s own cycle and a twelfth of the maintenance
expense fall at the beginning of the month; the guaranteed *Deckungskapital* rolls forward
over the **policy year** at the *Rechnungszins*; the surplus is declared and credited at the
**anniversary** on that year's closing reserve; death, maturity and surrender fall at the end
of the **month**, surrender after the mortality decrement, and each is paid the balances
standing at the end of that month — the year's own closing figures in an anniversary month,
and the ones struck at the **last** anniversary in the other eleven.

**What is sourced and what is not.** The contractual mechanics are sourced: the surplus
rate as a percentage of the *Deckungskapital* at the allocation date and the allocation at
the *Bilanzstichtag*; the *Rückkaufswert* as the *Deckungskapital* on the
*Rechnungsgrundlagen der Prämienkalkulation* struck at the end of the current
*Versicherungsperiode* and floored by the five-year spreading; the *Stornoabzug* biting on
the guaranteed value alone; the *Beitragsfreistellung* test of § 165 VVG; the § 161 VVG
substitution of the *Rückkaufswert* for the sum insured on a suicide inside three years;
the cessation of premiums on death; and both DeckRV cohort ceilings. **Every behavioural
and experience assumption is a standardization**: no German insurer publishes a mortality
basis, an expense loading, a commission scale, a terminal-bonus rate or a lapse rate for
this product, and the DAV tables — DAV 2008 T here — are the property of the Deutsche
Aktuarvereinigung, are not public and are cited by name rather than redistributed.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the decrement, surplus and expense tables with company data before drawing any conclusion
from the output.

**Model points.** Fourteen, covering both premium forms, all four payment frequencies with
the *echte* and *unechte* readings of a sub-annual one, all three *Überschussverwendung*
systems, an in-force 2012 cohort on a 1,75 % guarantee opening at ``t = 168``, a successful
and a failing *Beitragsfreistellung*, a non-*gezillmert* tariff, and a short unequal-sums
contract at a *Risikozuschlag* on the ``nil`` surplus scenario. Model point 1 is the
anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_kapitallebensversicherung_de.py`` asserts every row of the
notes' twenty-five-year worked example to the cent — on ``result_cf_annual()`` — and the
twelve months of policy year 1 on the monthly frame beside it, ``pols_if`` to six decimals,
and one test per listed modeling pitfall. Ten ``check_*()`` cells close on every model point,
among them ``check_net_cf()`` — this library's first ruling — and ``check_res_roll_fwd()``,
the Fackler recursion that proves the premium, the first-order mortality, the interest and
the prospective reserve formula are mutually consistent.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/kapitallebensversicherung/KLV_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "KLV_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
