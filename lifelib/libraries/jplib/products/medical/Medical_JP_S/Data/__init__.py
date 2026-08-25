# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.Medical_JP_S.Projection` as ``data``. :mod:`~.Medical_JP_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/medical/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Medical_JP_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=====================  ===========================  ==========================
Reference              Cells                        File
=====================  ===========================  ==========================
model_point_file       model_point_table()          model_point_table.csv
mort_table_file        mort_table()                 mort_table.csv
lapse_table_file       lapse_table()                lapse_table.csv
incidence_table_file   incidence_table()            incidence_table.csv
los_table_file         los_table()                  los_table.csv
=====================  ===========================  ==========================

.. rubric:: The mortality table is a proxy, and deliberately so

第三分野標準生命表2018 is public, free and machine-readable at a stable 日本アクチュアリー会
URL — the sharp contrast with ``uklib``, which had to proxy subscriber-only CMI tables.
Anyone can retrieve it and check a rate. But the publisher's site terms prohibit
reproduction, alteration and transmission to third parties without written consent, so
this library does **not** ship a copy of it.

``mort_table.csv`` is therefore a **[std] construction**, and it is the **library-wide
canonical one**: the same file, value for value and provenance string for provenance
string, ships in every ``jplib`` product that reads a third-sector rate, so a cell cannot
disagree with itself across products. It is built on the union of the rates the research
pass actually read out of 第三分野標準生命表2018 — 22 sourced anchors, male and female,
age 0 to the terminal age — with **piecewise log-linear (geometric) graduation** between
adjacent anchors: for ``a <= x <= b``, ``q(x) = q(a) (q(b)/q(a))^((x-a)/(b-a))``. That
reproduces every anchor **exactly** by construction, so nothing sourced is disturbed, and
it is locally the Gompertz family the publisher's own table follows. The terminal age
anchor — 116 male, 118 female, ``q = 1`` — is what closes the projection horizon. Every
row says so in its ``provenance`` column, which points at the IAJ entries rather than
reproducing them: an anchor row records the quoted rate, an interpolated row records the
two anchors it sits between. No conclusion about Japanese third-sector mortality should
be drawn from it.

Two further things the ``provenance`` columns record, because they change what the
numbers mean. The table is a **valuation** table whose margin runs the *wrong way* for a
best estimate on a morbidity product — death releases the liability, so the table is set
deliberately below national mortality — which is why ``Projection.mort_be_factor`` scales it
**up**. And 第三分野標準生命表2018 **excludes 高度障害**, so a severe-disability state
cannot be read out of it and the premium waiver module carries its own incidence.

.. rubric:: The morbidity tables are constructions on public statistics

There is no published morbidity table in Japan: 日本アクチュアリー会 publishes the
mortality basis only, and every insurer's 危険発生率 sits in its unpublished 算出方法書.
``incidence_table.csv`` and ``los_table.csv`` are built from 患者調査, a 基幹統計 of
厚生労働省:

``incidence_table.csv``
    入院受療率 per 100,000 by five-year age band and 退院患者平均在院日数 by the four
    broad bands each statistic is published at. 受療率 is a point-in-time
    **prevalence**, not an incidence, and the conversion
    ``inc = (juryoritsu / 100,000) x 365 / alos`` is an explicit **[std]** step —
    treating the published figure as a claim frequency is the commonest error in a
    Japanese medical model. The 概況 prints 入院受療率 for every five-year band, so all
    fifteen bands the model needs carry its citation and none is interpolated. The sex
    factors are **[std]**: the age x sex cross-tabulation lives in an e-Stat table that
    was not downloaded.

``los_table.csv``
    A five-band discrete length-of-stay distribution per broad age band, with the
    probabilities in each row solved so that the row mean **equals** the sourced
    平均在院日数 for that band exactly. The shape is **[std]** — the 32-band e-Stat grids
    were not downloaded — and it matters more than the mean it reproduces, because the
    60-day limit bites on the tail and not on the mean.

To swap in a company basis, replace the CSVs with same-schema files, or point the
``*_file`` References at different names, and clear the cache. No formula changes.
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

    Indexed by ``point_id``.  ``point_id = 1`` is the technical notes' worked-example
    anchor cell; the others exercise the product's 型 elections, its riders, its 特則
    and its edge ages.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The **[std]** mortality construction by sex and age, from *mort_table.csv*.

    Not a copy of 第三分野標準生命表2018, whose publisher's terms forbid redistribution:
    the library-wide canonical **[std]** construction, log-linear between the sourced
    anchors and exact at every one of them, including the male ``q40`` the technical
    notes quote and the real table's terminal ages.  See the Space docstring.  Read as
    the *valuation* rate; ``Projection.mort_be_factor`` turns it into a best estimate.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def lapse_table():
    """The **[std]** annual lapse rates by policy year, from *lapse_table.csv*.

    Anchored by construction to the only published industry-wide Japanese persistency
    figure, 解約・失効率 5.6% p.a. on 個人保険 — which is measured on opening in-force
    *sum assured*, a basis a 医療保険 with no sum assured cannot even enter.  Policy
    years beyond the last row take that row.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def incidence_table():
    """入院受療率 and 平均在院日数 by age band, from *incidence_table.csv*.

    Indexed by ``age_start``, the lower edge of the five-year band.  ``alos_days``
    repeats the broad-band 平均在院日数 that the five-year band falls in, because that
    is the granularity each statistic is published at **[std]**.  ``inc_factor_m`` and
    ``inc_factor_f`` are the **[std]** sex factors on incidence.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / incidence_table_file, index_col="age_start")   # noqa: F821


def los_table():
    """The **[std]** length-of-stay distribution, from *los_table.csv*.

    Five ``stay_days`` bands per broad age band, keyed by ``band_start``, with ``prob``
    solved so the row mean equals the sourced 平均在院日数 for that band.  A single mean
    is not usable on this product: the sourced per-cause means run from 2.4 days to
    290.4, and a 60-day cap bites at one end and never at the other.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / los_table_file,                                # noqa: F821
        index_col=["band_start", "stay_days"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

incidence_table_file = "incidence_table.csv"

los_table_file = "los_table.csv"

pd = ("Module", "pandas")
