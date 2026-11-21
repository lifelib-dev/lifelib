# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. level premium term life insurance.

:mod:`~.Term_US_S` is the executable counterpart of
``products/term_life/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-life, fully underwritten level
premium term policy: level premiums for the level period, then Jump-to-ART renewal at
unchanged face amount to expiry at attained age 95, convertible to permanent cover
before ``min(end of level period, attained age 70)``, with no cash value.

**Spaces.** The model contains two:

:mod:`~.Term_US_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Term_US_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Term_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps on lifelib's 0-based time index — the clock
``basiclife/BasicTerm_S`` runs on. ``t = 0`` is the issue month and the frame runs
``t = 0, 1, ..., proj_len() - 1``, where ``proj_len() = 12 * (95 - age_at_entry())`` is
the number of policy months projected to expiry at attained age 95. Everything
contractual about the product is nevertheless annual — the guaranteed premium schedule,
the ART renewals, the shock lapse — so the policy year is derived and used as a lookup
key: ``duration(t) = t // 12`` is the completed policy years, ``policy_year(t) =
duration(t) + 1`` the contractual 1-based label, and the attained age is
``age_at_entry() + duration(t)``.

Decrements follow suit in two speeds. ``mort_rate(t)`` and ``lapse_rate(t)`` are the
**annual** rates of the policy year containing month ``t`` — the vectors the technical
notes tabulate — and ``mort_rate_mth(t)`` and ``lapse_rate_mth(t)`` are the monthly
rates actually applied, ``1 - (1 - q)^(1/12)``. The shock lapse is the documented
exception: it is not spread but falls in full at the end of the final level-period
month, ``t = 12n - 1``, immediately before the first ART premium is due.

Because the ordinary rates compound back to the annual ones and the shock sits on a
year boundary, the in-force **at every policy anniversary** is exactly what an
annual-step model would carry. The cash flows are not, and are not meant to be:
claims fall at the end of the month of death, maintenance expense accrues monthly, and
a modal premium is collected when it is contractually due — which is what the finer
grid is for. ``result_cf_annual()`` sums the frame into policy years so the two can be
read side by side.

**What is sourced and what is not.** The contractual elements are taken from a
specimen policy: the guaranteed premium schedule, the $65 policy fee inside it, the
modal factors and expiry at attained age 95. Everything behavioural and
expense-related — mortality, lapse, the shock lapse, post-level-term mortality
deterioration, conversion, commission, expenses and premium tax — is a standardization
introduced for the reference implementation, because no public source carries it.
**This model is a mechanics demonstration, not a pricing or reserving result.**
Replace the assumption tables with company data before drawing any conclusion from the
output.

**Model points.** Both points in ``model_point_table.csv`` use the anchor
configuration T10 / M / StdNT / band 1 / annual mode, because the specimen gives a
guaranteed premium scale for that cell alone. They differ only in the M(1) override,
which is what makes the divergence between the technical notes' formula and its worked
example testable. A model point on any other plan, sex, class or band requires
``premium_rates.csv`` to be extended first; a test asserts every model point in the
table actually projects.

**Verification.** Model point 1 is the anchor cell of the worked example in the
technical notes, and ``tests/test_term_life_us.py`` asserts both of its tables — the
twelve months of policy year 1 and the policy-year aggregation of years 1-12 — money
to the cent, in-force to six decimals.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/term_life/Term_US_S")
    >>> model.Projection[1].result_cf()
    >>> model.Projection[1].result_cf_annual()
"""

from modelx.serialize.jsonvalues import *

_name = "Term_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
