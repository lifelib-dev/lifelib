# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for French individual assurance dépendance.

:mod:`~.Dep_FR_S` is the executable counterpart of
``products/dependance/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows for a single-policy model point of individual
*assurance dépendance*: a lifetime monthly *rente* payable in arrears while a recognised
state of dependence persists, a one-off *capital d'équipement*, the premiums refunded
when dependence arises inside the *carence*, and expenses. Premiums are *viagères* and
cease on recognition; there is no surrender value, no death benefit and no maturity.

**This is a five-ledger multiple-state model.** The health chain is
*autonome* → *dépendance partielle* / *dépendance totale* → *décès*, and a fifth
in-force but paid-up ledger, *réduite*, is reached only by lapse from eight years of
premiums. Two features of that structure carry the product:

**State-dependent mortality.** A dependent life's mortality is far heavier than a healthy
life's at the same age, and modelling it flat is this product's first error. The model
applies proportional hazards on the force — ``mort_partial_mult`` 1.75 and
``mort_total_mult`` 4.27 — so at attained age 85 the annual rates are 0.06179 healthy,
0.10562 in *partielle* and 0.23841 in *totale*. Flattening them while leaving the
incidence basis unchanged raises lifetime claims by 159.7%. ``mort_total_mult`` is
calibrated rather than picked: it is the value at which
:func:`~.Dep_FR_S.Projection.sojourn_total` returns 2.9989 years from exact age 84,
against the "about three years" the CCSF reports for heavy dependents.

**The *carence* and the *franchise* are different things and both are modelled.** The
*carence* runs from inception, is cause-specific (0 / 12 / 36 months by accident,
illness, neurological or psychiatric illness), blocks the benefit **and terminates the
membership with a full refund of premiums**. The *franchise* runs from recognition, is
three months, and only delays payment. Removing the first raises lifetime claims by
3.99%, removing the second by 7.09% — different sizes, and different signs of error if
either is applied in the other's place.

The third structural feature is the *mise en réduction*: a policyholder who stops paying
after eight full years keeps a **reduced *rente totale*** for life instead of nothing.
Treating that lapse as an exit understates lifetime claims by 4.57% and drops a ledger
that peaks at 8.27% of the original policy.

**Spaces.** The model contains two:

:mod:`~.Dep_FR_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Dep_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Dep_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, matching the *rente mensuelle à terme échu* and the
monthly premium. Policy month ``t`` is **0-based** and runs 0, 1, ...,
``proj_len() - 1``, where ``proj_len() = 12 (110 - entry_age)`` is the **number of
projected months**, 480 for the base cell — cover is *viagère* with no age limit, so what
ends the projection is a **[std]** terminal age of 110, not the contract. Premium and
expenses fall at the start of the month, benefits and transitions at the end of it, and
the two *revalorisations* and any tariff revision at the start of months 12, 24, ...

**Model points come in four kinds.** ``status = autonomous`` cells start the whole
population in the autonomous ledger; ``status = partial`` and ``status = total`` cells
start it in a dependent ledger at a stated claim duration; ``status = reduced`` cells
start it paid-up on a reduced guarantee. An in-force portfolio needs all four.

**What is sourced and what is not.** The contractual mechanics are sourced: the two-state
trigger and its AVQ and AGGIR grids, the *rente partielle* at half the *rente totale*,
the *capital d'équipement* paid once per membership, the 0 / 12 / 36-month *carence* by
cause with termination and refund, the three-month *franchise*, premium *exonération*
from recognition, the eight-year *mise en réduction* and the CNP *barème* behind it, the
absence of any surrender value, and the two separate indexations. **Every rate is a
standardization.** No French LTC incidence or continuance table is public: the shipped
prevalence curve is a **[std]** logistic fitted to two sourced DREES APA rates, the
severity shares that turn public GIR prevalence into insured prevalence are **[std]**,
the state-mortality multiples are **[std]**, the mortality proxy is a Gompertz shaped
like a French population table and is **not** TH 00-02 / TF 00-02 or TGH05 / TGF05, and
the lapse table has one indirect anchor. **This model is a mechanics demonstration, not
a pricing or reserving result.** Replace the basis with portfolio experience before
drawing any conclusion from the output.

**Verification.** ``tests/test_dependance_fr.py`` asserts the notes' sixteen-month worked
example to the precision the notes display, the policy-year-1 aggregates, the lifetime
totals, and one test for each modelling pitfall the notes name.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/dependance/Dep_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Dep_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
