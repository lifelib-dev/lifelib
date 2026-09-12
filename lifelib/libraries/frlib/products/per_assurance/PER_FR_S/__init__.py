# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the French PER individuel assurantiel.

:mod:`~.PER_FR_S` is the executable counterpart of
``products/per_assurance/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single-policy model points on the
composite *plan d'épargne retraite* those notes specify: a compartment-1 PER assurantiel
with a *fonds en euros* support and a *unités de compte* bucket, run on the *gestion
pilotée par horizon* glide path, with an entry loading, separate euro and UC management
charges, an arbitrage charge on the annual rebalancing, a *garantie plancher* death
floor, and a settlement at the declared horizon split between *capital* and *rente
viagère*.

**Accumulation with a two-way exit.** That sentence is the product. The plan is
**blocked** until the L. 224-1 maturity, so there is no surrender right and no
``lapse_rate`` anywhere in this model. What leaves the book instead are two distinct
statutory exits, and they are not the same thing: a *déblocage anticipé* under one of the
seven L. 224-4 cases, which pays the **whole** account value and bears no charge, and a
**transfer out** to another PER, which pays a transfer value net of a 1% indemnity for
the first five years from the first *versement*. Modelling either as a lapse, or both
with one decrement, attaches the wrong payment formula to half the exits.

**Spaces.** The model contains two:

:mod:`~.PER_FR_S.Data`
    Reads the five input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.PER_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.PER_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**The glide path is an input table, not a formula.** ``allocation_grid.csv`` is keyed by
(*allocation_profile*, *years_to_horizon*) and gives the target euro share, so the four
regulatory profiles, and any insurer ladder finer than the four regulatory bands, are a
table edit rather than a code change. That is the product's dominant financial lever and
it is the one thing a reader of this model will want to change first.

**Projection basis.** Monthly steps, on plan months. ``t`` counts **plan months** from
the valuation date and is **0-based**: ``t = 0`` is the first projected month and the
frame is ``t = 0, 1, …, proj_len() - 1``, where ``proj_len() = 12 x proj_years()`` is the
number of projected months and ``proj_years() = retirement_age - age_init()`` the declared
horizon in years. An in-force cell opens the frame at ``t = 0`` like any other; its
history is carried in ``duration_ifo``, not in a frame offset. Everything contractual
about the plan is nevertheless annual, so the plan year is derived and used as a lookup
key: ``duration(t) = duration_ifo + t // 12`` are the completed *ancienneté* years,
``plan_year(t) = duration(t) + 1`` the 1-based label the *ancienneté* schedules are
written in, ``years_to_horizon(t) = proj_years() - t // 12`` the key into the glide path,
and the attained age ``age_init() + t // 12``, which steps at the anniversary.

The annual events land whole on their own month of the plan year, and there are two such
months rather than one. In the month that **opens** a plan year, ``t % 12 == 0``, the
*versement* arrives and the balance is rebalanced to the glide-path target. In the month
that **closes** it, ``t % 12 == 11``, the management charge is taken on the post-crediting
balance — and at ``t = proj_len() - 1``, the horizon anniversary, the survivors settle.
Every month in between, investment return is credited to both supports and the decrements
death, early release and transfer out fall at the end, in that order.

Decrements and returns follow suit in two speeds. ``mort_rate(t)``,
``early_release_rate(t)`` and ``transfer_out_rate(t)`` are the **annual** rates of the
plan year containing month ``t`` — the vectors the technical notes tabulate — and
``mort_rate_mth(t)``, ``early_release_rate_mth(t)`` and ``transfer_out_rate_mth(t)`` are
the monthly rates actually applied, ``1 - (1 - q)^(1/12)``; the two credited returns take
the same treatment in interest form, ``(1 + r)^(1/12) - 1``. The management charge is the
documented exception: it is **not** spread, because the *garantie plancher* base
accumulates a sum of charges rather than a product of factors and twelve monthly charges
do not add to the annual one.

Because the monthly rates and factors compound back to the annual ones and the charge sits
at the year boundary, every anniversary state and the whole settlement are exactly what an
annual-step model would carry — verified to 1.8e-14 relative across all twelve model
points. The cash flows are not, and are not meant to be: claims fall at the end of the
month of exit and are valued on the balance held then, maintenance expense accrues
monthly on a decrementing block, and the split between the three decrements moves while
their total does not. That is what the finer grid is for. ``result_cf_annual()`` sums the
frame into plan years and ``result_state_annual()`` reads it at the two months that
determine each of its columns, so the two grids can be read side by side.

**What is sourced and what is not.** The mechanics are sourced: the *blocage* and the
seven early-release cases, the 1%/five-year transfer indemnity, the 0% maximum technical
rate, the regulatory de-risking grid, the euro capital floor stated net of loading and
net of charges, death closing the plan, the exit menu and the compartment-3 annuity-only
rule, and the €110 monthly commutation threshold. Every **rate** is a standardization:
the charge levels are contractual *maxima* rather than levels, no insurer publishes an
annuity rate card, TH 00-02 / TF 00-02 and TGH05 / TGF05 are cited but not shipped, and
no public French experience exists for PER early-release, transfer or annuitisation
behaviour. **This model is a mechanics demonstration, not a pricing or reserving
result.**

**Where the annuity goes.** A liquidating plan that does not commute hands
``annuity_conversion`` to ``Rente_FR_S``, and the annuity's own reserve, its 0.80% p.a.
charge, reversion, *annuités garanties* and revaluation are specified in
``products/rente_viagere/technical-notes.md``. This model commutes to a stated amount and
records what it hands over; it does not re-implement the payout chassis.

**Verification.** ``tests/test_per_assurance_fr.py`` asserts the notes' worked example
row by row to the cent — the glide-path band crossings, the arbitrage charge and which
support pays it, the two supports' crediting and charging, the *garantie plancher* base,
the three decrements, and the settlement with its commutation identity — and, on the
monthly grid, the month-by-month table of the first plan year, the constant-force rate
conversions, and that every plan-year state reproduces the annual-step model exactly.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/per_assurance/PER_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "PER_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
