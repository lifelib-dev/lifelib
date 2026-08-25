# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The three input CSVs are read here, **once per model**, and referenced from
:mod:`~.WholeLife_JP_A.Projection` as ``data``. :mod:`~.WholeLife_JP_A.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/whole_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WholeLife_JP_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
======================  ==========================  ==============================

.. rubric:: The mortality table is a construction, and the reason is the licence

生保標準生命表2018（死亡保険用）is published by 日本アクチュアリー会 in full, free, at a stable
public URL — the sharp contrast with the UK library, whose CMI tables cannot be read at
all without a subscription. Anyone can retrieve it and check a rate. But the publisher's
site terms prohibit reproduction, alteration and transmission to third parties without
prior written consent, so this library must not ship a copy of the file.

``mort_table.csv`` is therefore a **[std] construction**, and its ``provenance`` column
says so row by row, ANCHOR row by ANCHOR row. It is the **canonical jplib death table**:
one file, built once from the union of every anchor any product in this library sources,
and shipped identically by every product that needs it, so that a rate quoted in two
products carries the same number *and* the same provenance in both. This product ships
the age range it reads, 15 to ω.

Two kinds of row, and the provenance string names which is which. An **ANCHOR** row is a
rate **quoted and attributed** to the IAJ table [REG-R18]; an **INTERPOLATED** row is
filled by **log-linear interpolation in ln q between the two neighbouring anchors,
evaluated in double precision and rounded to five decimal places**. There is no
extrapolation anywhere: both sexes run from an age-0 anchor to a terminal anchor, so
every interpolated age lies strictly between two sourced ones. Over the range shipped
here, 27 of the 95 male rows and 24 of the 99 female rows are anchors; the remaining 68
and 75 are the standardization. **The interpolated rows are not IAJ values** and no
conclusion about Japanese insured mortality should be drawn from them.

How far an interpolated row sits from the rate the IAJ actually publishes is **not
known** and is not asserted anywhere: this library reads the anchors and constructs the
rest, so it has nothing to measure the fill against. What is known is where the fill is
thinnest — between age 90 and ω the anchors are five and then four years apart while
``q`` is turning over, which is the widest gap in the file. A user who has downloaded the
IAJ PDF replaces ``mort_table.csv`` with a same-schema file and changes no formula.

The other two files are standardizations end to end. No Japanese carrier publishes a
lapse or surrender curve by duration — the only public benchmark is an amount-weighted,
all-product industry 解約・失効率 — and none publishes an expense basis at all, the
予定事業費率 being named in the 保険契約者保護機構 boilerplate and never quantified. The
expense and commission levels are Projection References rather than a table, because
each is a single scalar.
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

    Indexed by ``point_id``.  Point 1 is the technical notes' worked-example anchor
    cell; the other nine exercise the product's variants, its optional modules and its
    edge cases.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The mortality rates by sex and attained age, from *mort_table.csv*.

    A **[std]** construction anchored on quoted rates of 生保標準生命表2018（死亡保険用）,
    not a copy of the published table; see the Space docstring.  The rate includes
    高度障害, which the published table already carries inside the death rate, so a
    projection using it must not add a separate disability decrement.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def lapse_table():
    """The base voluntary surrender rates by policy year, from *lapse_table.csv*.

    Three rows: policy years 1 and 2, then a level tail read for every later year.  The
    surrender surge at 払込満了 is **not** in this table — it is the model point's
    ``lapse_spike``, held apart so that it can be switched off and its effect read
    directly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")
