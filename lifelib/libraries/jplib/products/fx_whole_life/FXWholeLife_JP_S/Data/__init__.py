# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.FXWholeLife_JP_S.Projection` as ``data``. :mod:`~.FXWholeLife_JP_S.Projection`
is parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace
with its own cells cache; if the readers lived there, every model point would re-read
every file. Holding them in an unparameterized Space reads each file once no matter how
many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/fx_whole_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FXWholeLife_JP_S`` folder without its parent's CSVs produces a model that reads and
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
charge_table_file       charge_table()              charge_table.csv
fx_path_file            fx_path_table()             fx_path_table.csv
======================  ==========================  ==============================

.. rubric:: The mortality table is a construction, not a copy

``mort_table.csv`` is a **[std]** construction. 生保標準生命表2018（死亡保険用）is published free
at a stable public URL by 日本アクチュアリー会 and anyone can go and read it, but that
publisher's site terms prohibit reproduction and transmission to third parties, so this
library must not ship a copy of it. What it ships instead is the **one canonical jplib
proxy**: a single table built once, for the whole library, by log-linear interpolation
in ``ln q`` between the individual rates the library's nine products quote from the
published table, rounded to that table's own five decimal places. Every row's
``provenance`` column says which of the two it is — an ANCHOR row read from the IAJ
table and quoted under attribution, or an INTERPOLATED **[std]** value — so the same
attained age carries the same rate *and* the same provenance in every product that
ships it. This file is that canonical table restricted to the attained ages this
product's model points can reach: ages 18 to the terminal age of each sex. The rates
are identical to the other products' at every shared cell and must not diverge. It is
**not** the published table, and no conclusion about Japanese insured-lives mortality
should be drawn from it.

The table is also a **valuation** table carrying an explicit margin sized to about 2σ,
not best-estimate experience, so a best-estimate basis is a **[std]** adjustment of it
either way. That adjustment lives on ``Projection`` as ``mort_be_factor`` and moves the
*decrement* only; the cost-of-insurance charge reads the table unadjusted, because the
charge basis is a pricing element the insurer sets and the decrement is an experience
assumption. To swap in a licensed or company basis, replace ``mort_table.csv`` with a
same-schema file, or point ``mort_table_file`` at a different name, and clear the
cache. No formula changes.

.. rubric:: The other four tables

``model_point_table.csv`` is indexed by ``point_id``; point 1 is the technical notes'
worked-example anchor cell. ``lapse_table.csv`` is indexed by shape and policy year,
because the two shapes are two behavioural regimes an order of magnitude apart — a
four-year cumulative exit of 60.90% on the single-premium shape against roughly 25% on
the level-premium one. ``charge_table.csv`` holds the shape's whole parameter set: the
back-solved charge stack, the 解約控除 scale, the 低解約返戻金割合 ramp, the three constants of
the 市場価格調整 reconstruction and the two 特別積立金 rates, each row tagged in its
``provenance`` column with the source it came from or with the fit that produced it.
``fx_path_table.csv`` is an optional monthly-anniversary FX path by policy year, read
only where a model point sets ``fx_path``; the base run holds the rate flat at the
model point's own ``fx_ttm``.
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

    Indexed by ``point_id``.  ``point_id = 1`` is the technical notes' worked-example
    anchor cell: male, 契約年齢 40, LEVEL shape, 基本保険金額 US$100,000, 60歳払込満了,
    月払保険料 US$239.60, 積立利率 at the guaranteed floor of 3.00%.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The mortality rates by sex and attained age, from *mort_table.csv*.

    The canonical jplib **[std]** proxy for 生保標準生命表2018（死亡保険用）, anchored to the
    individual rates the library quotes from it and never a copy of that table; see the
    Space docstring.  Includes 高度障害, which the published table's death rate already
    carries, so 高度障害 is not a second decrement anywhere in this model.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def lapse_table():
    """The annual surrender rates by shape and policy year, from *lapse_table.csv*.

    Two curves, because the two shapes are two behavioural regimes: the SINGLE curve
    is calibrated to a published four-year exit statistic, the LEVEL curve has no
    public anchor at all and is a **[std]** judgement.  Policy years beyond the last
    row take that row.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file,                              # noqa: F821
        index_col=["shape", "policy_year"])


def charge_table():
    """The shape's charge, surrender and MVA parameters, from *charge_table.csv*.

    Indexed by shape and item name.  Holds the back-solved 契約初期費用 and 維持費率, the
    解約控除 scale, the 低解約返戻金割合 ramp, the three constants of the 市場価格調整
    reconstruction and the two 特別積立金 rates, each with its own provenance.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / charge_table_file,                             # noqa: F821
        index_col=["shape", "item"])


def fx_path_table():
    """The optional TTM path by policy year, from *fx_path_table.csv*.

    Read only where a model point sets ``fx_path``; the base run holds the reference
    TTM flat at the model point's own ``fx_ttm``, because this library models
    contractual cash flows and not an FX view.  Policy years beyond the last row take
    that row.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / fx_path_file, index_col="policy_year")         # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

charge_table_file = "charge_table.csv"

fx_path_file = "fx_path_table.csv"

pd = ("Module", "pandas")
