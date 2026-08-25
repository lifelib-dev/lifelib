# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.Annuity_JP_A.Projection` as ``data``. :mod:`~.Annuity_JP_A.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/individual_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Annuity_JP_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
mort_anchor_file        mort_anchor_table()             mort_anchor_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
pricing_table_file      pricing_table()                 pricing_table.csv
expense_table_file      expense_table()                 expense_table.csv
commute_factor_file     commute_factor_table()          commute_factor_table.csv
======================  ==============================  ==========================

.. rubric:: The mortality tables are constructions, not copies

生保標準生命表2018（死亡保険用）and 生保標準生命表2007（年金開始後用）are published by 日本アクチュアリー会 at
stable public URLs, free and in full — anyone can retrieve them and check a rate. But the
publisher's site terms prohibit reproduction, alteration and transmission to third
parties without written consent, so **this library ships no copy of either table**.

What :func:`mort_table` reads is a **[std] construction**, and the two tables in it are
constructed differently because their anchor sets are.

死亡保険用 is the **canonical jplib table**: one file, shared by every product in the library
that reads 生保標準生命表2018（死亡保険用）, so that the same cell carries the same value and the
same provenance everywhere. Its anchor rows are rates read from the IAJ table and quoted
under attribution [REG-R18]; every other age is graduated **log-linearly in age between the
two neighbouring anchors** — linear in ``ln q`` — evaluated in full double precision and
rounded to five decimal places. Nothing is extrapolated: both sexes run from an age-0
anchor to a terminal anchor, so every graduated age lies strictly between two sourced ones.
Both sexes carry their own sourced anchors; there is no age setback.

年金開始後用 is a Makeham law ``mu(x) = A + B c**x``, ``q(x) = 1 - exp(-mu(x))`` fitted to the
three published male spot rates in :func:`mort_anchor_table`, with the female rows a
**four-year age setback [std]** — the setback the published terminal ages imply, 126 against
122. Only male spot rates were retrieved for that table.

Every row of both files carries a ``provenance`` column saying which construction it came
from, which rows are sourced anchors, and that the file is not a copy of an IAJ file.

To swap in a licensed or company basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache. No formula
changes: the lookup already carries the table name and the sex the Japanese tables need.
``Projection.check_mort_graduation`` will then report the shipped rates as no longer equal
to the stated graduation, which is the correct answer once the table is a real one.
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

    Indexed by ``point_id``.  Point 1 is the technical notes' worked-example anchor cell.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The [std] mortality rates by table, sex and age, from *mort_table.csv*.

    Two tables live in the file under the ``table`` key: ``death_cover_2018`` for the
    deferral phase and ``annuity_payout_2007`` for the annuity in payment.  Neither is a
    copy of a 日本アクチュアリー会 file; both are constructions anchored to the quoted rates in
    :func:`mort_anchor_table` — 死亡保険用 graduated log-linearly, 年金開始後用 on a Makeham law.
    See the Space docstring.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["table", "sex", "age"]).sort_index()


def mort_anchor_table():
    """The published spot rates each construction is anchored to, and its omega age.

    Read from *mort_anchor_table.csv*: the sourced ages of the canonical 死亡保険用 table, and
    three spot rates per sex on 年金開始後用.  These are the only published mortality figures in
    the library's input set: rates quoted and attributed, which the IAJ's terms permit — as
    opposed to a copy of the table, which they do not.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_anchor_file,                              # noqa: F821
        index_col=["table", "sex"]).sort_index()


def lapse_table():
    """The [std] 解約・失効 rates by phase segment, read from *lapse_table.csv*.

    Three segments: ``premium_paying`` carries a duration curve keyed by the first policy
    year it applies from, ``defer_gap`` the single rate applying through the 据置期間, and
    ``pre_annuitisation`` the zero that must apply from ``t = n - 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file,                              # noqa: F821
        index_col=["segment", "from_year"]).sort_index()


def pricing_table():
    """The pricing and module basis, one row per item, from *pricing_table.csv*.

    The two 予定利率, the 予定事業費率 and 年金支払開始時費用, the 解約控除 shape, the two
    best-estimate mortality factors, the 基本年金額 rounding step and the loan, dividend and
    dynamic-lapse parameters.  Every row carries its source tag or its **[std]** rationale
    in the ``provenance`` column.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / pricing_table_file, index_col="item")          # noqa: F821


def expense_table():
    """The best-estimate cash expense and commission levels, from *expense_table.csv*.

    These are cash flows.  They are entirely separate from the 予定事業費率 in
    :func:`pricing_table`, which is a pricing loading living inside the fund; mixing the
    two double-counts expense in one direction and destroys the calibration in the other.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / expense_table_file, index_col="item")          # noqa: F821


def commute_factor_table():
    """The published 年金の一括払 factors by remaining instalments.

    Read from *commute_factor_table.csv*: one carrier's table, verbatim over 1-14
    remaining instalments.  It implies about 0.40% p.a., which is not the composite's
    payout 予定利率 of 0.65%; the mismatch is a property of the composite and the reason
    base-run commutation take-up is zero.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / commute_factor_file,                           # noqa: F821
        index_col="remaining_years")


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

mort_anchor_file = "mort_anchor_table.csv"

lapse_table_file = "lapse_table.csv"

pricing_table_file = "pricing_table.csv"

expense_table_file = "expense_table.csv"

commute_factor_file = "commute_factor_table.csv"

pd = ("Module", "pandas")
