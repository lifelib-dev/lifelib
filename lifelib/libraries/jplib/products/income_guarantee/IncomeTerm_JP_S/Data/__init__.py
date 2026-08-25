# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.IncomeTerm_JP_S.Projection` as ``data``. :mod:`~.IncomeTerm_JP_S.Projection`
is parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace
with its own cells cache; if the readers lived there, every model point would re-read
every file. Holding them in an unparameterized Space reads each file once no matter
how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/income_guarantee/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IncomeTerm_JP_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
rate_class_file         rate_class_table()          rate_class_table.csv
======================  ==========================  ==============================

.. rubric:: The mortality table is a construction, not a copy

``mort_table.csv`` is a **[std] construction**, not a reproduction of
生保標準生命表2018（死亡保険用）. The table is published by 日本アクチュアリー会 (the Institute of
Actuaries of Japan) at a stable public URL and anyone may go and read it, but the
publisher's site terms prohibit reproduction, alteration and transmission to third
parties without written consent, so this library may not ship a copy of it. What it
ships instead is a table whose anchor rows carry the individual rates the technical
notes quote and attribute, and whose remaining rows are log-linear interpolations in
``ln q`` between the two neighbouring anchors, rounded to 5 decimals. The anchor set
is the **union** of every anchor any ``jplib`` product reads from the table — both
sexes at ages 20, 22, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80 and 85, plus male
31-34 — so a cell carries the same value and the same ``provenance`` string in every
product that ships it. Female rates are read at the female anchors in their own right,
not built as a ratio to the male rate, and no age is extrapolated: every shipped age
lies strictly between two sourced anchors. Every row's ``provenance`` column says
which of the two kinds it is and points at the IAJ entries [REG-R18] [REG-R21].

The file is restricted to attained ages 20-89, the range this model can read on the
composite's own envelope of issue age 20-70 and expiry age 45-90. It reproduces every
rate the technical notes display, which is what makes the worked example checkable:
the sourced anchors ``q30 = 0.00068``, ``q31 = 0.00069``, ``q32 = 0.00070`` and
``q45 = 0.00177``, and the interpolations ``q44 = 0.00163``, ``q63 = 0.00851`` and
``q64 = 0.00929``. It is not a published table and no conclusion about Japanese
mortality should be drawn from it.
Keep the second distinction separate from the first, too: even the real table is a
**valuation** table carrying an explicit safety margin, so a best-estimate basis is a
**[std]** adjustment of it either way — here ``Projection.mort_be_factor`` at 0.80,
times the rate class factor read from ``rate_class_table.csv``.

To swap in a company basis, replace ``mort_table.csv`` with a same-schema file — the
columns are ``sex``, ``age``, ``mort_rate``, ``provenance`` — or point
``mort_table_file`` at a different name, then clear the cache. No formula changes.

.. rubric:: Why the rate class factors are a table and not a model point column

``technical-notes.md`` lists ``class_factor`` among the model point attributes. It is
held here instead, keyed by ``rate_class``, for two reasons: the four factors are one
**[std]** structure rather than four free numbers — a smoker/non-smoker ratio of 1.50
and a preferred/standard ratio of 0.778, with the levels pinned by the requirement
that the mix-weighted mean be 1.000, because 生保標準生命表2018 is an all-lives basis — and
a per-policy copy of a shared assumption is a place for the four points to drift
apart. ``rate_class_table.csv`` therefore carries the illustrative mix weights as
well, and ``Projection.check_class_factor_norm()`` asserts the normalization.
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

    Inputs are *external* files, not data stored inside the model, so the model
    folder is pure formulas.  The path is resolved at run time from where the model
    was read, following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*.

    Indexed by ``point_id``.  Point 1 is the anchor cell of the worked example in
    ``technical-notes.md``; the rest exercise the product's variants, its optional
    modules and its edge cases.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The 死亡保険用 table rates by sex and attained age, from *mort_table.csv*.

    A **[std]** construction anchored on the individual 生保標準生命表2018（死亡保険用）rates the
    technical notes quote, **not** a copy of the published table — see the Space
    docstring for why, and the file's own ``provenance`` column for which rows are
    anchors and which are interpolated.  Read as the *table* rate: the best-estimate
    factor and the rate class factor are applied in ``Projection.mort_rate``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def lapse_table():
    """The annual ordinary lapse rates by policy year, from *lapse_table.csv*.

    Five rows; the last applies to policy year 5 and beyond.  A **[std]** table
    reconciled to the LIAJ's FY2024 個人保険 解約・失効率 of 5.6%, carried unchanged from the
    protection chassis because nothing product-specific exists — the national
    household survey does not break 収入保障保険 out at all.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def rate_class_table():
    """The rate class mortality factors and mix weights, from *rate_class_table.csv*.

    Indexed by the ASCII ``rate_class`` code.  Four classes — 非喫煙者優良体,
    非喫煙者標準体, 喫煙者優良体, 喫煙者標準体 — whose qualification is published and *measured*
    (BMI, blood pressure, a cotinine test) but whose premium differential no carrier
    publishes, so every factor here is **[std]**.  The ``mix_weight`` column is the
    illustrative mix that normalizes the four factors to a mean of 1.000.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_class_file, index_col="rate_class")       # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

rate_class_file = "rate_class_table.csv"

pd = ("Module", "pandas")
