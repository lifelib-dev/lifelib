# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. participating whole life insurance.

:mod:`~.WholeLife_US_A` is the executable counterpart of
``products/whole_life/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for the two standardized composite designs those
notes specify: ``RefWL-Par``, a participating level-premium whole life policy with a
guaranteed cash value schedule that endows at attained age 100, an annual
three-factor dividend and paid-up additions; and ``RefWL-FE``, the non-participating
simplified-issue final-expense variant with an explicit policy fee and, on the graded
plan, a return-of-premium death benefit in policy years 1-2.

**Spaces.** The model contains two:

:mod:`~.WholeLife_US_A.Data`
    Reads the six input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.WholeLife_US_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.WholeLife_US_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Annual steps on policy years. Policy year ``t`` counts **years**,
not months, because every cash flow driver in this product — the level annual premium,
the annual dividend declaration and the anniversary capitalization of loan interest —
is annual, and there is no account value requiring monthiversary processing. ``t`` runs
``proj_start()`` .. ``proj_len()``, where ``proj_len() = 100 - age_at_entry()`` is the
anniversary at attained age 100 and ``proj_start() = duration_inforce() + 1`` lets an
in-force model point start mid-life. The **value** state variables carry the notes'
end-of-year subscript: ``cv_pp(t)``, ``pua_face(t)``, ``div_accum(t)`` and
``loan_bal(t)`` are all **as at the anniversary ending policy year t**, and the notes'
``t = 0`` initializations (``PUAF_0 = puaf_inforce``, ``DA_0 = 0``,
``L_0 = loan_inforce``) are the ``t <= duration_inforce()`` branch of each recursion.

The **policy count** is the one exception, and deliberately so. ``pols_if(t)`` is the
number in force at the **start** of policy year t — the notes' ``l_{t-1}``, ``l_0 = 1``
at issue — because that is the weight every cash flow on the same ``result_cf()`` row
is computed over, and because it is what ``pols_if`` means in every other model in this
library. The notes' end-of-year ``l_t`` is ``pols_if_at(t, "AFT_DECR")``, which is
``pols_if(t + 1)``.

Within a policy year the order is the notes': premium, PUA rider premium, premium tax
and expenses at the **beginning** of the year; then, at the **end**, deaths, loan
interest capitalization, the dividend credit, surrenders, and — in the final year only
— maturity. Deaths are therefore valued on the *prior* anniversary's paid-up additions
(``claim_pp(t, "DEATH")`` carries ``pua_face(t - 1)``) while surrenders are valued on
the current one, including the dividend just credited.

The net flow is published under **both** signs, because these notes print ``NetCF_t``
with outgo positive while the rest of the library is income-positive.
``liability_cf(t)`` carries the notes' formula verbatim — premium income with a minus
sign, so a positive value is money leaving the insurer — and
``net_cf(t) = -liability_cf(t)`` carries the income-positive convention every model in
``products/`` shares, so the column can be summed or compared across products. Both are
columns of ``result_cf()``. Nothing is silently flipped and nothing is lost.

**What is sourced and what is not.** Very little of this product is public. The
contractual skeleton is sourced: the 4.00% guarantee interest rate, endowment of the
guaranteed cash value at face at age 100, the fixed 6.00% loan rate with direct
recognition, the union of dividend options with paid-up additions as the default, and
— for the final-expense variant — the per-$1,000 premium rates, the $36 policy fee and
the 110%-of-premiums graded death benefit. Everything else is a standardization
introduced for the reference implementation and marked **[std]**: the 6.00% dividend
interest rate snapshot, the three-factor dividend parametrization, the 0.70 experience
factor that produces both the scale and the best-estimate mortality, the $25 expense
margin, the lapse schedules, expenses, premium tax, the 10% PUA-rider load, the 2x
term-blend target, and every shipped table — the guarantee mortality, the net single
premiums, the nonforfeiture net level premiums and the guaranteed cash value schedules
are all illustrative curves calibrated to the worked example's anchors, **not** the
2017 CSO / 4% tables the notes name, which are licensed and may not be shipped here.
**This model is a mechanics demonstration, not a pricing or reserving result.**
Replace the assumption tables with company data before drawing any conclusion from the
output.

Those four tables are pinned to their worked-example anchors *independently*, which is
a documented divergence from the notes rather than an oversight: the notes' first
"known modeling pitfall" says to regenerate every guarantee-basis quantity from one
2017 CSO / 4% source, and the worked example's own steps 3 and 10 make that impossible
— ``NP_g = 13.00`` and ``NSP_55 = 0.42`` cannot both hold on any single mortality table
at 4%. The arithmetic is in the ``Projection`` docstring, in the model README and in a
test. What the shipped tables *do* preserve are the two endpoints whose failure the
pitfall is about: the net single premium is exactly 1 at attained age 100 and the cash
value schedule is exactly face in the final policy year, so neither block leaks at
maturity.

**Not implemented.** The notes describe, and this model deliberately omits: the
reduced paid-up and extended term nonforfeiture options and the automatic premium loan
(the notes name them but give no projection formula); partial surrender of paid-up
additions; terminal dividends and dividends credited at death; the monthly modal
premium refinement; the variable/adjustable loan rate regimes; the age 100-121 tail
beyond the **[std]** truncation; and any Sect. 7702 / 7702A policing — ``mec_flag()``
flags a model point that would need the test rather than performing it, exactly as the
notes prescribe. State variations are not modeled.

**Model points.** ``model_point_table.csv`` carries fourteen points. Point 1 is the
worked example's anchor cell, and it is an **in-force** point: the notes walk through
policy year 10 of a male 45, $100,000, $1,800-premium policy that already holds
$4,100 of paid-up additions, which is exactly ``duration_inforce = 9`` and
``puaf_inforce = 4100``. Points 2-10 are the same policy issued as new business under
each dividend option and each in-scope rider, plus the limited-pay and female cells;
points 11-13 are the final-expense variant on the sourced rate table; point 14 is the
term blend again, this time with no rider premium funding it, so that the shortfall
branch of the one-year-term cap is exercised as well as the funded branch. A test
asserts that every point in the table projects.

**Verification.** ``tests/test_whole_life_us.py`` asserts all fifteen steps of the
worked example on model point 1 — the guaranteed cash values, the net level premium,
both mortality bases, all three dividend margins, the dividend, the net single premium,
the paid-up additions purchased and in force, their cash value, the death benefit and
the surrender value — to the cent, together with the in-force and paid-up-additions
roll-forwards, one test per pitfall the notes list, the size of the guarantee-basis
divergence above, and the identity that every dividend credited is delivered under each
of the four dividend options.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/whole_life/WholeLife_US_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "WholeLife_US_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

