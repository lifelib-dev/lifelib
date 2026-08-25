# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.Endowment_JP_A.Projection` as ``data``. :mod:`~.Endowment_JP_A.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/endowment/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Endowment_JP_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ===============================  ==========================
Reference                 Cells                            File
========================  ===============================  ==========================
model_point_file          model_point_table()              model_point_table.csv
mort_table_file           mort_table()                     mort_table.csv
lapse_table_file          lapse_table()                    lapse_table.csv
benefit_schedule_file     benefit_schedule_table()         benefit_schedule_table.csv
========================  ===============================  ==========================

.. rubric:: The mortality table is a construction, not a copy

``mort_table.csv`` is a **[std] construction**. 生保標準生命表2018（死亡保険用）
(*seiho hyōjun seimeihyō 2018*, the standard mortality table for death cover) is
published by 日本アクチュアリー会 (the Institute of Actuaries of Japan) at a stable public
URL, free and in full, so anyone can retrieve it and check a rate — but the publisher's
site terms prohibit reproduction, alteration and transmission to third parties without
written consent. This library therefore **cites** the table by URL, **quotes** the
individual rates its worked example needs, and **ships** a table whose ``provenance``
column points at the IAJ entry row by row: an ANCHOR row is a rate read from the IAJ
table and quoted under attribution, an INTERPOLATED row is the log-linear fill in
``ln q`` between the two neighbouring anchors, rounded to five decimals, which is the
published table's own granularity. Nothing here is a copy of the IAJ file and nothing
here should be read as one.

The file is the **library-wide canonical construction**, identical row for row in every
jplib product that ships it, so one cell carries one value and one provenance string
wherever it appears. Both sexes are built the same way from their own sourced anchors:
there is no ratio, no sex multiplier and no derivation of one sex from the other. It is
restricted to attained ages 0 to 60, which is every age these nine model points reach —
the oldest, the 養老保険 anchor cell, matures at attained age 60.

Two further distinctions survive that one. The shipped rates trace a **valuation** table
carrying an explicit safety margin sized to roughly a 2-sigma level, not best-estimate
experience, so a best-estimate basis is a further **[std]** adjustment of it — which is
what ``Projection.mort_be_factor`` is for, and why it is 1.00 in the base run. And the
table is read at 満年齢 (*mannenrei*, attained age) while the published table is built on a
nearest-birthday basis, an understatement of up to half a year of age that the technical
notes name rather than hide.

To swap in a company basis, replace ``mort_table.csv`` with a same-schema file, or point
``mort_table_file`` at a different name, then clear the cache. No formula changes: the
lookup already carries the sex and attained age the tables need, and it is used for both
lives — the 被保険者 (*hihokensha*, the insured) and, on the education cell, the 契約者
whose death triggers the waiver.
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

    Indexed by ``point_id``.  ``point_id = 1`` is the 養老保険 anchor cell of the
    technical notes' worked example and ``point_id = 2`` its 学資保険 cell.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The mortality rates by sex and attained age, from *mort_table.csv*.

    A **[std]** construction anchored to 生保標準生命表2018（死亡保険用）and never a copy of
    it; see the Space docstring for what that means and why.  Read at 満年齢 attained age
    for both lives — the insured and, on the education cell, the policyholder whose
    death triggers the waiver.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def lapse_table():
    """Surrender and premium-default rates by policy year, from *lapse_table.csv*.

    Two columns.  ``lapse_rate`` is the voluntary surrender rate, 4 / 3 / 2 percent with
    the last row applying to every later year **[std]**; ``default_rate`` is the
    premium-default rate that feeds the automatic premium loan module, which is off in
    the base run because every shipped base model point carries ``apl_default_mult = 0``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def benefit_schedule_table():
    """The staged 学資金 schedules, read from *benefit_schedule_table.csv*.

    Indexed by ``schedule_id``, one row per payment, each row giving the policy year and
    the payment as a fraction of 基準保険金額.  The schedule is **data, not formula**:
    observed designs run from a single payment of 100% to four payments of 100% each, so
    an implementation that hard-codes a shape is modelling one carrier.  The maturity
    benefit is not a row here — it is always present on both cells and is held
    separately, so that a schedule with no rows at all still matures.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / benefit_schedule_file,                         # noqa: F821
        index_col="schedule_id")


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

benefit_schedule_file = "benefit_schedule_table.csv"

pd = ("Module", "pandas")
