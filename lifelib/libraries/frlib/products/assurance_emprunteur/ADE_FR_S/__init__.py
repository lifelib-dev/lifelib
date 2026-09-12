# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for French assurance emprunteur (ADE).

:mod:`~.ADE_FR_S` is the executable counterpart of
``products/assurance_emprunteur/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of
*assurance des emprunteurs* — the death, PTIA, ITT and IPT cover a French borrower buys
alongside a mortgage — on a **monthly** grid, for **one insured head on one fixed-rate
amortising loan**.

**This is the most intricate model in the library**, and the reason is that four separate
mechanisms have to run at once.

The **loan** is deterministic and the model computes it. Nothing is read from an
*échéancier*: given ``capital_initial``, ``loan_rate_annual`` and ``loan_term_months``,
:func:`~.ADE_FR_S.Projection.echeance` is the level instalment and
:func:`~.ADE_FR_S.Projection.crd` the *capital restant dû* at every month.
:func:`~.ADE_FR_S.Projection.check_crd` asserts the amortisation closes both ways — the
annuity form against the roll-forward ``crd(k) = crd(k-1) (1 + i) - ech``, and
``crd(T) = 0`` at the final instalment. ``crd`` is the only thing linking the loan to the
insurance: the death and PTIA benefits of month ``t`` are ``crd(t + 1) x quotite``, the
balance at the end of that month.

The **state space is four-state** — healthy, ITT (*incapacité temporaire totale*), IPT
(*invalidité permanente et totale*) and dead — which is the ``income_protection`` /
``IP_UK_S`` three-state chassis with a fourth state and a duration-triggered forced
transition. The in-claim population is **two-dimensional**: ITT termination rates depend
on how long the claim has run, so the model carries ``l_itt(t, z)`` cohort by cohort, and
at the 1 095-day cap the surviving cohort is **assessed** rather than advanced — 35 % of
it passes to IPT and the rest returns to healthy. Collapsing the duration dimension, or
letting cohort 36 advance to cohort 37, are the notes' two most costly pitfalls.

The **guarantees end at different ages.** Décès runs to 85, PTIA and ITT/IPT to 70 in the
base cell, and the loan over 240 months — so a cover can stop while the loan, and the
premium, run on. At the first month where the ITT/IPT cover has ceased, any claim in
payment is **moved** into healthy rather than deleted: those lives are alive, still death
covered, and still paying. The premium is *nivelé* and does not fall.

*Résiliation* — the loi Lemoine substitution decrement — is a **real lapse** out of
healthy, low in year 1 and three times higher from year 2, and it pays nothing: this
product has no surrender value and no maturity benefit.

**Spaces.** The model contains two:

:mod:`~.ADE_FR_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.ADE_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.ADE_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps, matching the monthly *échéance* that the incapacity
benefit replaces. Policy month ``t`` is **0-based**: ``t = 0`` is the first projected
month and the frame is ``t = 0, 1, ..., proj_len() - 1``, where
``proj_len() = loan_term_months`` is the number of months projected. The contractual
policy year is the 1-based label ``t // 12 + 1``. Premiums fall at the beginning of the
month and are paid by lives in healthy only — premiums are waived in claim. The
instalment, the transitions and all benefit fall at the end of the month, so month ``t``
opens on the loan balance ``crd(t)`` and closes on ``crd(t + 1)`` — ``crd`` keeps its own
0-based time-point index, ``crd(0) = capital_initial`` at adhesion — and a claim
incepting at end of month ``t`` is first paid at end of month ``t + 1``. All cover and
any claim in payment terminate at the loan's contractual expiry with no value.

**Model points come in three kinds.** ``status = healthy`` cells start the whole
population in healthy; ``status = itt`` cells start it in an ITT cohort at a stated claim
duration and ``status = ipt`` cells in IPT, and those two are the disabled-life annuities
a claims-in-payment reserve is quoted as. An in-force portfolio needs all three.

**What is sourced and what is not.** The contractual mechanics are sourced: the two
premium bases, the two indemnity bases, the *franchise* menu, the 1 095-day ITT cap, the
66 % *barème croisé* IPT threshold, the cover-end ages, waiver of premium in claim, the
level *nivelé* premium, cancellation *à tout moment*, and expiry without value. **Every
rate is a standardization.** No French decrement, incidence or termination table for this
product was retrieved — insurer rate cards are proprietary and the homologated TH 00-02 /
TF 00-02 tables are cited by name but are not redistributable — so the mortality, PTIA,
ITT inception, ITT termination, IPT mortality, *résiliation* and CRD premium tables
shipped here are **[std]** proxies built from INSEE-shaped population data and carry no
authority. **This model is a mechanics demonstration, not a pricing or reserving
result.** Replace the basis with licensed tables before drawing any conclusion from the
output.

**Verification.** ``tests/test_assurance_emprunteur_fr.py`` asserts the notes' fifteen
month worked example to the cent, its column sums, the loan spine, the ITT cohort
survival through the 1 095-day cap, the present values over the full 240 months, and one
test per modelling pitfall the notes name.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/assurance_emprunteur/ADE_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "ADE_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
