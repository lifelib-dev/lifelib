# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The three input CSVs are read here, **once per model**, and referenced from
:mod:`~.WholeLife_KR_S.Projection` as ``data``. :mod:`~.WholeLife_KR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/whole_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so a
diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WholeLife_KR_S`` folder without its parent's CSVs produces a model that reads and then
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

.. rubric:: The mortality table is a construction, and the reason is that Korea publishes
   no table at all

The industry table is the **제10회 경험생명표** (*gyeongheom saengmyeongpyo*, experience
life table), produced by 보험개발원 and applied to new business from April 2024. It is
**not published in full**: what is released is the summary — 평균수명 and 기대여명 — and
not the rates, and even those were retrieved for this library only through a trade
newspaper [REG-R33] [REG-R34]. The 참조순보험요율 the bureau files with the FSC are
likewise never published. There is therefore **no published Korean insured mortality rate
to anchor a proxy on**, which is the sharp contrast with ``jplib``, where the 生保標準生命表
is free to read and only its redistribution is restricted.

``mort_table.csv`` is accordingly a **[std] construction** and its ``provenance`` column
says so row by row. Three kinds of row:

**ANCHOR** rows at 보험나이 20, 40 and 60 take the mean of the only two Korean insured
mortality rates in the public domain at those ages — the sample 적용위험률 grids that
하나생명 [S2] and KDB생명 [S8] print in their 상품요약서. The two rates are sourced; taking
their mean is the standardization. They differ by up to 24% — 18%–24% at five of the six
published cells and not at all at 여 20세, where both print 0.00018 — so they **bracket**
rather than fix a Korean insured mortality level.

**CONSTRUCTED** rows below age 60 are log-linear in ``ln q`` between those anchors, and
above age 60 follow a Gompertz in ``ln q`` with a quadratic deceleration term whose two
parameters are solved so that the table's 65세 기대여명 is 23.7 years (male) and 27.1
(female) — the 국가데이터처 완전생명표 figures of 19.5 and 23.7 [REG-R38] plus the gap to
the reported 제10회 경험생명표 figures [REG-R33] — and so that ``q`` reaches 1 at the
standardized terminal age ω = 115.

**The TERMINAL row** sets ``q = 1`` at ω = 115, which closes the table. The 제10회
terminal age is not public either.

Two independent checks on the construction are worth recording because neither was used to
fit it. The resulting 평균수명 at birth is **85.4 years (male)** and **90.4 (female)**
against the 86.3 and 90.7 reported for the 제10회 [REG-R33]; and the age-40 male rate of
0.00085 sits between the two disclosed carrier rates by construction while the age-60
female rate of 0.001935 reproduces the same bracket. **No row of this file is a
경험생명표 value and the table must never be presented as one.** One conversion is stated
rather than performed: the public statistics behind the calibration are on **만나이** while
this product rates on **보험나이**, and no public mapping between the two exists.

The lapse file is a standardization end to end. ``lapse_table.csv`` holds the two bases
the November 2024 계리가정 decision puts side by side — the log-linear 원칙모형 converging
on 0.1% at 납입완료 with an 0.8% ultimate rate [REG-R27], and a level comparison basis —
as three parameters each rather than a rate per policy year, because the convergence point
is 납입완료 and that is a model point attribute rather than a fixed duration. The expense,
commission and interest levels are Projection References rather than a table, because each
is a single scalar.
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

    Indexed by ``point_id``.  Point 1 is the technical notes' worked-example anchor cell —
    남자, 보험나이 40세, 보험가입금액 1억원, 종신, 20년납, 저해지환급형 ``k = 0.50`` — and
    the other nine exercise the product's variants, its optional modules and the edges of
    its issue-age and sum-assured envelopes.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The mortality rates by sex and attained 보험나이, from *mort_table.csv*.

    A **[std]** construction anchored on the two carriers' disclosed 적용위험률 grids [S2]
    [S8] and calibrated to the insured 65세 기대여명 implied by [REG-R38] and [REG-R33];
    **not** the 제10회 경험생명표, which is not published in full.  See the Space
    docstring.  The rate is a death rate alone: Korea puts no 고도장해 benefit on this
    chassis, so a projection using it must not add a disability decrement — the disability
    trigger on a Korean 종신보험 waives the premium instead, and that is a separate state.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def lapse_table():
    """The lapse-rate parameters by basis, from *lapse_table.csv*.

    Two rows, indexed by ``lapse_basis``.  ``loglinear`` is the FSS 원칙모형 of the
    November 2024 계리가정 decision — a log-linear decay from a first-year rate to 0.1% at
    납입완료, then an 0.8% ultimate rate [REG-R27].  ``flat`` is the level comparison basis
    the same guidance obliges an insurer to disclose against it.  The columns are
    parameters rather than a rate per policy year because the convergence point is
    납입완료, which differs by model point.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="lapse_basis")     # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")
