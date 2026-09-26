# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.Sofort_DE_S.Projection` as ``data``. :mod:`~.Sofort_DE_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many points
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/sofortrente/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so a
diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Sofort_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

============================  ==============================  ================================
Reference                     Cells                           File
============================  ==============================  ================================
model_point_file              model_point_table()             model_point_table.csv
mort_table_file               mort_table()                    mort_table.csv
improvement_file              improvement_table()             improvement_table.csv
surplus_scale_file            surplus_scale_table()           surplus_scale_table.csv
hoechstrechnungszins_file     hoechstrechnungszins_table()    hoechstrechnungszins_table.csv
============================  ==============================  ================================

Every file but ``model_point_table.csv`` carries a final ``provenance`` column, one tag
per row, per the library's second ruling. A model point is a *configuration* rather than
an assumption, and that is the only exemption.

.. rubric:: The decrement tables are a [std] proxy, and here is its anchor

**DAV 2004 R and DAV 2004 R-Bestand are the property of the Deutsche Aktuarvereinigung,
are not public, and are not redistributed here.** They are cited by name in
``sources.md`` and ``mort_table.csv`` ships a constructed proxy in their place, in four
series — ``{FIRST, SECOND} x {M, F}`` — over attained ages 50 to 120:

    q_base(x) = 1 - exp( -( A + B c^x (c - 1) / ln c ) ),   A = 0.0002, B = 1.5e-5, c = 1.10
    FIRST/M   = 1.250000 x q_base(x)          SECOND/M = 1.20 x FIRST/M
    FIRST/F   = 0.795455 x q_base(x)          SECOND/F = 1.20 x FIRST/F

``q_base`` is the Gompertz-Makeham law the research file constructs and prints, with life
expectancy 24,29 years at 65 and ``q(65) = 0.00789``, ``q(75) = 0.02001``,
``q(85) = 0.05078`` — a **prudent annuitant** shape of the right order for a German
first-order basis, and **not** DAV 2004 R.

**The anchor is the unisex blend.** The two sex factors are chosen so that the
``mix_male = 0.45`` blend of the FIRST series reproduces ``q_base(x)`` itself:
``0.45 x 1.250000 + 0.55 x 0.795455 = 1.00000025``, the exact factor for the female
series being ``0.4375 / 0.55 = 0.79545454...`` and 0.795455 its six-decimal rounding. The
blend therefore reproduces the research file's own law to 2.5e-7 relative at every age,
which is four orders of magnitude inside the tolerance any published figure is quoted to,
and every annuity factor printed in ``_research/sofortrente.md`` can be traced into this
model. Age 120 is the closing row: all four series are set to 1.0 there, so the survival
path reaches zero inside the ``omega_age = 121`` horizon.

``improvement_table.csv`` carries the second half of the surface — a *Trendfunktion*
proxy ``lambda_SECOND(x) = 0.0150`` to age 70, tapering linearly to zero at 105, with
``lambda_FIRST = 1.25 x lambda_SECOND`` — and the model builds
``q(x, sex, cohort, basis) = q_table x (1 - lambda)^(cohort + x - mort_base_year)`` with
``mort_base_year = 2025``, so the shipped tables are the period tables of calendar year
2025 and the exponent is the calendar year the life attains age ``x``, less 2025. The
exponent is **negative** for a cohort attaining an age before 2025 — an in-force point
issued in 2012 reads pre-2025 mortality — and is not floored.

**What a replacement must preserve.** Three things, and a substitution that keeps only
the first is not a substitution for this table. (i) The **generational structure**: a
``q(x, cohort)`` surface, not a period table, because a period proxy applied to a
forty-year annuity understates the liability by a margin that dwarfs every other
assumption. (ii) The **first-order margin in both dimensions**: lighter mortality
(``SECOND = 1.20 x FIRST``) *and* a stronger improvement trend
(``lambda_FIRST = 1.25 x lambda_SECOND``), because prudence in an annuity table must reach
the rate of improvement as well as its level. (iii) The **age-adjustment convention** —
here, integer attained age last birthday with the closing row at 120 — since a table
supplied with an *Altersverschiebung* must have it applied before it is read here.
Replacing the level alone leaves the wedge between the two bases wrong, and that wedge is
the systematic *Risikoüberschuss* this product's *Überschussrente* is largely financed
from.

The other two assumption files are levels, not tables. ``surplus_scale_table.csv`` gives
the opening *Überschussrente* share and its annual growth for each of the four
*Überschussverwendung* forms, all [std]: no *Überschussanteilsatz* was established at any
carrier for any year. ``hoechstrechnungszins_table.csv`` is the statutory rate history a
model point's tariff rate is checked against, by the contract's own vintage — a German
in-force book is a stack of cohorts and each carries its own cap.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_dir():
    """The directory holding the input CSVs: the model folder's parent.

    Inputs are *external* files, not data stored inside the model, so the model folder is
    pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*.

    Fourteen points, indexed by ``point_id``.  The only input file without a
    ``provenance`` column: a model point is a configuration rather than an assumption, and
    its columns are one contract's own terms.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The annual death rates by basis, sex and attained age, from *mort_table.csv*.

    Indexed by ``(basis, sex, age)`` with ``basis`` in ``{FIRST, SECOND}`` and ``sex`` in
    ``{M, F}``.  The unisex series the tariff is struck on is **computed** from these two
    at ``mix_male``; it is deliberately not a row, because no real sex-distinct table
    carries one.

    A **[std]** proxy, not DAV 2004 R; see the Space docstring for what it is, what its
    anchor is and what a replacement must preserve.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["basis", "sex", "age"])


def improvement_table():
    """The annual mortality improvement rates, from *improvement_table.csv*.

    Indexed by ``(basis, age)``.  This is the *Trendfunktion* of a generational table:
    the improvement lives **inside** the mortality surface, keyed by birth cohort, rather
    than being applied on top of a period rate keyed to the projection year.  A **[std]**
    proxy; DAV 2004 R's own trend is not public.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / improvement_file,                              # noqa: F821
        index_col=["basis", "age"])


def surplus_scale_table():
    """The *Überschussverwendung* scale by form, from *surplus_scale_table.csv*.

    Indexed by ``surplus_form``.  ``surplus_init_pct`` is the *Überschussrente* at outset
    as a fraction of the *garantierte Rente* and ``surplus_growth`` its annual increase,
    for the four forms ``none`` / ``konstant`` / ``teildynamisch`` / ``volldynamisch``.

    Every figure is **[std]**.  No *Überschussanteilsatz* was established for this product
    at any carrier for any year; what the corpus establishes is the *shape* — the constant
    form highest at outset and flat in intention only, the volldynamic form lowest at
    outset and rising with each declaration.  The four forms are **not** calibrated to
    equal present value here, and a user who needs them to be must do that calibration.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surplus_scale_file, index_col="surplus_form")  # noqa: F821


def hoechstrechnungszins_table():
    """The statutory *Höchstrechnungszins* history, from *hoechstrechnungszins_table.csv*.

    Indexed by ``year_from``, with ``year_to`` closing each band and ``max_rate`` the cap
    in force.  A contract's cap is the one in force at its own *Vertragsbeginn* and stays
    with it for life, so an in-force model point is checked against its vintage rather
    than against today's rate.  The cap is an upper bound and not the tariff rate: a
    carrier may price below it, and one in the corpus is observed doing so.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / hoechstrechnungszins_file, index_col="year_from")   # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

improvement_file = "improvement_table.csv"

surplus_scale_file = "surplus_scale_table.csv"

hoechstrechnungszins_file = "hoechstrechnungszins_table.csv"

pd = ("Module", "pandas")
