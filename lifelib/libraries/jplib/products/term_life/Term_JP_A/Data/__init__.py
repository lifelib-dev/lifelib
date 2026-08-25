# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.Term_JP_A.Projection` as ``data``. :mod:`~.Term_JP_A.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/term_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_JP_A`` folder without its parent's CSVs produces a model that reads and then
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
prem_rate_file          prem_rate_table()           prem_rate_table.csv
======================  ==========================  ==============================

:func:`prem_anchor_table` is derived from :func:`prem_rate_table` rather than read from
a fifth file, so it costs no extra read.

.. rubric:: The mortality table is a proxy, and deliberately so

生保標準生命表2018（死亡保険用）(*seiho hyōjun seimeihyō 2018*, the standard mortality
table for death benefits) is published by 日本アクチュアリー会 (the Institute of
Actuaries of Japan) free and in full at a stable public URL [REG-R18][R3][R4] — anyone
can retrieve it and check a rate, which is the sharpest contrast in this repository with
the UK term model, whose CMI tables cannot be read at all without a subscription. **But
the publisher's site terms prohibit reproduction, alteration and transmission to third
parties without written consent** [REG-R21], so this library must not ship a copy of it.

``mort_table.csv`` is therefore a **[std]** construction, not the table. It is the
**canonical jplib proxy** — one construction shared by every product in this library
rather than a per-product reconstruction, so that a cell carries the same rate *and* the
same provenance wherever it is shipped. Its anchors are the union of the rates read from
the published table across the library's research passes [REG-R18], which is why more
ages are anchored than this product's own pass read [R4]; among them are the rates the
technical notes quote — male ``q30 = 0.00068``, ``q35 = 0.00077``, ``q40 = 0.00118``,
``q50 = 0.00285``, ``q60 = 0.00653``, ``q65 = 0.01015``, female ``q30 = 0.00037`` and
``q60 = 0.00363``. Every other age is log-linear in ``ln q`` between its two neighbouring
anchors, rounded to the five decimals of the published table's own granularity, with no
extrapolation anywhere. Every row says which of the two it is in its ``provenance``
column. The rows shipped here run from attained age 20 to attained age 80, the range
this product's model points can reach. The anchoring is what makes the model reproduce
the notes' worked-example rates exactly; the interpolated rows are a documented proxy
and no conclusion about Japanese mortality should be drawn from them.

Two further distinctions the file does not blur. The shipped rates are **table** rates:
:mod:`~.Term_JP_A.Projection` applies its own ``mort_be_factor`` to reach a
best-estimate basis, because 標準生命表2018 is a **valuation** table carrying an
explicit risk-theory margin sized near 2σ and capped at 130% of the unadjusted rate
[REG-R20]. And the table **includes 高度障害 inside its death rate** [REG-R20], which is
why the projection has one decrement and not two.

To swap in a company basis, replace ``mort_table.csv`` with a same-schema file, or point
``mort_table_file`` at a different name, and clear the cache. No formula changes.

.. rubric:: The premium table is mostly sourced

``prem_rate_table.csv`` is the one assumption file whose values are largely **not**
standardizations. Japanese insurers publish rate cards, so the marginal rate per
¥5,000,000 of cover and the ¥248 flat monthly element decompose exactly out of published
premiums [S2]. Four cells are published — male ages 30, 40 and 50 and female age 30, all
at a ten-year term — and each carries the arithmetic of its decomposition in its
``provenance`` column. Ages 60 and 70 are published by no carrier and the anchor cell
reaches both, so :mod:`~.Term_JP_A.Projection` extends the scale off the ``is_anchor``
row of the matching sex. The ¥248 is a **premium** component, not an expense recovery;
crediting it against maintenance expense counts it twice.
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

    Indexed by ``point_id``; ``point_id = 1`` is the anchor cell of the technical notes'
    worked example.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The **table** mortality rates by sex and age, from *mort_table.csv*.

    A **[std]** proxy for 生保標準生命表2018（死亡保険用）, anchored on the rates the
    technical notes quote and log-linearly interpolated between them; see the Space
    docstring for why the published table itself is cited rather than shipped.  The
    rates include 高度障害 [REG-R20] and carry the table's own valuation margin, which
    ``Projection.mort_be_factor`` removes.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def lapse_table():
    """The ordinary lapse rates by policy year, read from *lapse_table.csv*.

    **[std]** throughout: Japan's only published industry-wide persistency figure is the
    LIAJ's whole-market 解約・失効率 [REG-R31], which is a level and not a duration
    curve.  Policy years beyond the last row take that row.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def prem_rate_table():
    """The published premium rate cells, read from *prem_rate_table.csv*.

    Indexed by ``(sex, issue_age, term_y)``.  ``rate_per_5m`` is the marginal monthly
    rate per ¥5,000,000 of cover and ``policy_fee_m`` the flat monthly element, both
    decomposed out of published rate cards [S2].  ``is_anchor`` marks the one row per
    sex from which :mod:`~.Term_JP_A.Projection` extends the scale to unpublished ages.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / prem_rate_file,                                # noqa: F821
        index_col=["sex", "issue_age", "term_y"])


def prem_anchor_table():
    """The one ``is_anchor`` row per sex of :func:`prem_rate_table`, indexed by sex.

    Derived from the table already in memory rather than read from a file of its own, so
    it costs no extra read.  The male anchor is the published age-50 ten-year cell, the
    highest male cell any carrier publishes; the female anchor is the age-30 ten-year
    cell, the only published female cell in the source set [S2].
    """
    tbl = prem_rate_table().reset_index()
    return tbl[tbl["is_anchor"] == 1].set_index("sex")


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

prem_rate_file = "prem_rate_table.csv"

pd = ("Module", "pandas")
