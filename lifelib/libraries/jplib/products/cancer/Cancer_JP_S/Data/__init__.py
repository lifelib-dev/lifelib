# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.Cancer_JP_S.Projection` as ``data``. :mod:`~.Cancer_JP_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/cancer/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Cancer_JP_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
incidence_table_file    incidence_table()               incidence_table.csv
sex_factor_file         sex_factor_table()              sex_factor_table.csv
survival_table_file     survival_table()                survival_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
hosp_stay_file          hosp_stay_table()               hosp_stay_table.csv
======================  ==============================  ==========================

.. rubric:: The mortality table is a construction, not a copy

``mort_table.csv`` is a **[std]** construction. 第三分野標準生命表2018 is published by
日本アクチュアリー会 at a stable public URL, free and in full, and can be retrieved and checked by
anyone — but the publisher's site terms prohibit reproduction, alteration and
transmission to third parties without written consent, so this library must not ship a
copy of it. What is shipped instead is the **library-wide [std] construction** built on
the union of the individual rates ``jplib``'s products quote and attribute — 22 anchor
rows across the two sexes, 男 q(40) = 0.00076 among them, and the terminal rows
男 q(116) = 1.00000 and 女 q(118) = 1.00000 — **graduated log-linearly (geometrically)**
between adjacent anchors, ``q(x) = q(a) (q(b)/q(a))^((x-a)/(b-a))``. That graduation
reproduces every quoted rate **exactly**, which is the property a fitted curve does not
have, and it is locally the Gompertz family the publisher itself uses at the older ages.
Every product that reads this table ships the same file, so one cell carries one value
and one provenance string library-wide; each row's ``provenance`` says whether it is an
anchor or an interpolation. **The model reproduces the quoted rates exactly and asserts
nothing else about the IAJ table.** The copy here is cut to the ages this model can
reach — male 20-116, female 20-118 — which are the issue-age range and the two terminal
ages. Drop a licensed extract in over the same schema — ``sex``, ``age``,
``mort_rate`` — and no formula changes.

``incidence_table.csv`` is the opposite case and the contrast is the point: the
age-banded 罹患率 of 全国がん登録 are public, freely downloadable and reproduced here verbatim
with their attribution in ``provenance``. What is **[std]** about the incidence basis is
only the *sex split*, which lives in ``sex_factor_table.csv`` as the two sourced ratios
the notes interpolate between.

``hosp_stay_table.csv`` carries two bases: ``all_ages``, the sourced 14.4-day mean stay
used in the base run, and ``age_band``, the sourced four-band age gradient that the
``hosp_age_gradient`` switch reads instead.
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

    Indexed by ``point_id``; ``point_id = 1`` is the technical notes' worked-example
    anchor cell.  ``premium`` is an input on this product in a stronger sense than on any
    other in the library: no carrier publishes a rate table for a cancer main contract and
    the 算出方法書 is not a published document, so every premium in the table is a **[std]**
    modelling value.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The **[std]** mortality table by sex and age, from *mort_table.csv*.

    A log-linear graduation of the 第三分野標準生命表2018 rates the library quotes and attributes,
    男 q(40) = 0.00076 among them, **not** a copy of that table; see the Space docstring for
    why the distinction is load-bearing.  Read as the valuation-basis rate, which
    ``Projection.mort_rate`` scales by ``mort_be_factor``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def incidence_table():
    """全国がん登録 first-diagnosis 罹患率 by five-year age band, from *incidence_table.csv*.

    Both sexes combined, all sites C00-C96, crude rate per 100,000, 2023 diagnoses.
    Indexed by ``band_start``; the last row is the 100+ open band.  These are sourced
    values reproduced with their attribution, in deliberate contrast to
    :func:`mort_table`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / incidence_table_file, index_col="band_start")  # noqa: F821


def sex_factor_table():
    """The two sourced male / both-sexes incidence ratios, from *sex_factor_table.csv*.

    72.92 / 132.21 at the 35-39 band midpoint 37.5 and 2,684.60 / 1,948.71 at the 70-74
    band midpoint 72.5.  ``Projection.sex_factor`` interpolates linearly in age between
    them; replacing this two-row file and the interpolation with the by-sex age-band grid
    from the same workbook is the first thing a serious user should do.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / sex_factor_file, index_col="age")              # noqa: F821


def survival_table():
    """全国がん登録 5年相対生存率 by sex, from *survival_table.csv*.

    All sites, 2018 diagnoses.  Relative survival nets out background mortality, so it
    converts into an **excess hazard added to** the baseline rather than a replacement for
    it; ``Projection.mu_ex`` does that conversion.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / survival_table_file, index_col="sex")          # noqa: F821


def lapse_table():
    """The **[std]** annual lapse rates by policy year, from *lapse_table.csv*.

    Shared unchanged with the medical chassis so the two third-sector products do not
    disagree about persistency.  The only published industry-wide figure is a
    sum-assured-weighted 解約・失効率 on a book dominated by death cover, which a がん保険 with no
    sum assured cannot enter; the shipped curve averages 5.5% over its first ten years
    against that 5.6%.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def hosp_stay_table():
    """患者調査 mean stay in days for 悪性新生物 discharges, from *hosp_stay_table.csv*.

    Two bases in one file, selected by the ``basis`` column: ``all_ages`` is the sourced
    14.4-day figure the base run uses, and ``age_band`` is the sourced four-band gradient
    that ``Projection.hosp_age_gradient`` switches to.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / hosp_stay_file)                                # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

incidence_table_file = "incidence_table.csv"

sex_factor_file = "sex_factor_table.csv"

survival_table_file = "survival_table.csv"

lapse_table_file = "lapse_table.csv"

hosp_stay_file = "hosp_stay_table.csv"

pd = ("Module", "pandas")
