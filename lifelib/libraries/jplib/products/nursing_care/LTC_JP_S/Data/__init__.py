# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.LTC_JP_S.Projection` as ``data``. :mod:`~.LTC_JP_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/nursing_care/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``LTC_JP_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
prevalence_file         prevalence_table()              prevalence_table.csv
grade_share_file        grade_share_table()             grade_share_table.csv
======================  ==============================  ==========================

.. rubric:: The mortality table is a construction, not a copy

第三分野標準生命表2018 (*dai-san bun'ya hyōjun seimeihyō 2018*, the third-sector standard
table) is published by 日本アクチュアリー会 at a stable public URL, free and in full, so
anyone can retrieve it and check a rate — a real contrast with the CMI tables ``uklib``
has to work around. **But the publisher's site terms prohibit reproduction, alteration
and transmission to third parties**, so this library must not ship a copy of it. What
``mort_table.csv`` holds is a **[std] construction** built on the rates the library
quotes and attributes: eighteen **anchor** rows — nine per sex, at ages 40, 60, 65, 75,
80, 85, 90, 115 and the terminal age for males, and 40, 60, 65, 70, 75, 80, 85, 90 and
the terminal age for females — each carrying a rate quoted from 第三分野標準生命表2018
[REG-R18] [REG-R20], and between adjacent anchors a **piecewise log-linear (geometric)
graduation**,

    q(x) = q(a) (q(b) / q(a)) ** ((x - a) / (b - a))    for a <= x <= b

The graduation reproduces **every anchor exactly by construction**, so nothing sourced
is disturbed by the fitting, and it is locally the Gompertz family, which is the family
the publisher's own table follows over this age range. Above the last female anchor at
90 the female curve is continued at the male age-90-to-115 log-slope and closed on the
sourced female terminal rate. The file is restricted to ages 40 and over, which is the
whole of this product's issue-age range, and ``q = 1`` at the terminal ages 116 (male)
and 118 (female).

The same construction, at the same values, is shipped by every ``jplib`` product that
reads this table, so a cell carries the same rate **and the same provenance string**
wherever it appears. Every row carries that account in its ``provenance`` column, and
no conclusion about Japanese insured mortality should be drawn from the file.

Two further distinctions the ``provenance`` column keeps separate. First, even the real
table is a **valuation** table carrying an explicit safety margin — its risk-theory
adjustment is bounded 70% below and 85% above the unadjusted rate — so a best-estimate
basis is a **[std]** adjustment of it either way; that adjustment lives in
``Projection.mort_be_factor``, not in this file. Second, no impaired-life table for the 要介護
state exists in any retrieved source, so the care-state mortality multiple is likewise
a **[std]** Reference on ``Projection`` rather than a shipped table.

The morbidity basis is public, which is unique in this library, and is split over two
files rather than one. ``prevalence_table.csv`` carries the 認定率 (*nintei-ritsu*,
certification rate) the government publishes by broad age band, together with the
logistic that interpolates it; ``grade_share_table.csv`` carries the grade composition
of certified persons. Both are **prevalences** — a point-in-time count of certified
persons — and the conversion of a prevalence into an incidence is done in
:mod:`~.LTC_JP_S.Projection`, where it belongs, because it needs the mortality basis.

To swap in a company basis, replace the files with same-schema ones, or point the
filename References at different names, then clear the cache. No formula changes.
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

    Inputs are *external* files, not data stored inside the model, so the model folder
    is pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*.

    Indexed by ``point_id``.  ``point_id = 1`` is the anchor cell of the technical
    notes' worked example; the other seven exercise the product's variants, its
    optional modules and its edge cases.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The mortality rates by sex and attained age, from *mort_table.csv*.

    A **[std] construction** in the shape of 第三分野標準生命表2018 — quoted anchors joined
    by a log-linear graduation — never a copy of the published table; see the Space
    docstring.  The rate here is the *table* rate; ``Projection`` applies
    ``mort_be_factor`` to it to reach a best estimate.  The largest age present for a
    sex is that sex's terminal age, which is what ``Projection.omega_age()`` reads.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def lapse_table():
    """The annual lapse rates by policy year, read from *lapse_table.csv*.

    The last row is the terminal rate: ``Projection.lapse_rate`` caps the policy year
    at the largest year in the table, so a whole-of-life projection does not run off
    the end of it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def prevalence_table():
    """The certification prevalence parameters, read from *prevalence_table.csv*.

    Two sourced 認定率 anchors — 4.3% at ages 65-74 and 31.1% at 75 and over — and the
    three parameters of the logistic **[std]** fitted through them,
    ``prev_ceil``, ``prev_beta`` and ``prev_x_mid``.  The anchors are carried for
    provenance; the model reads the three fitted parameters.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / prevalence_file, index_col="param")            # noqa: F821


def grade_share_table():
    """The grade composition of certified persons, from *grade_share_table.csv*.

    ``share_ge`` is the share of all certified persons at that 要介護/要支援 grade **or
    above**, so ``care2`` is 0.508 and ``care3`` is 0.340.  The grade keys are ASCII
    codes for the seven-point certification scale; the model point columns
    ``grade_lump``, ``grade_annuity`` and ``grade_waiver`` hold them.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / grade_share_file, index_col="grade")           # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

prevalence_file = "prevalence_table.csv"

grade_share_file = "grade_share_table.csv"

pd = ("Module", "pandas")
