# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection of :mod:`~.VA_KR_S`.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.VA_KR_S.Projection` as ``data``. :mod:`~.VA_KR_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many contracts are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/variable_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and a table can be swapped
without touching a formula. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VA_KR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
lapse_table_file           lapse_table()                   lapse_table.csv
fund_file                  fund_table()                    fund_table.csv
charge_file                charge_table()                  charge_table.csv
risk_prem_file             risk_prem_table()               risk_prem_table.csv
return_scenario_file       return_scenario()               return_scenario.csv
crediting_file             crediting_table()               crediting_table.csv
=========================  ==============================  ==========================

Three of them carry a compound key — ``mort_table`` by ``(sex, age)``, ``fund_table`` by
``(fund_set, fund_id)`` and ``return_scenario`` by ``(scenario_id, fund_id)`` — and
three are read **without** an index because the lookup is a band test on a half-open
interval rather than a key lookup: ``lapse_table`` on completed policy years,
``risk_prem_table`` on attained 보험나이, ``crediting_table`` on completed years since
annuitisation.

``charge_table`` is the 상품요약서's own **수수료 안내표**, one row per charge line, and
it is a table rather than a block of scalar References for a reason: the five lines this
product turns on — 계약체결비용, 계약관리비용, 위험보험료, 최저보증비용 and 특별계정
운용보수 — are deducted from **different bases at different times and land in different
accounts**, and the ``base``, ``timing`` and ``account`` columns carry that beside each
rate so a reader can see it without reading a formula.

Every file but ``model_point_table.csv`` carries a ``provenance`` column and every cell
in it begins with a citation tag. That is the library's rule, and here it is
load-bearing rather than decorative: **no Korean mortality table in this library is a
transcription**, the 제10회 경험생명표 not being published in full [REG-R33] [REG-R34],
and every return assumption on this product is a standardization as well. The rows say
which authority each number stands on.
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

    Ten contracts indexed by ``point_id``.  Point 1 is the technical notes' anchor cell:
    남자 보험나이 40, 기본보험료 ₩300,000 월납, 10년납, 연금개시나이 60, 보증형,
    채권형 50% / 주식형 50%.  This is the only file exempt from the provenance rule, a
    model point being a configuration rather than an assumption.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """Annual mortality by sex and attained 보험나이, from *mort_table.csv*.

    Two bases on one file.  ``mort_rate`` is the 보험사망률 used for the death decrement
    of the 연금개시 전 보험기간, against which the GMDB is written; ``ann_mort_rate`` is
    the 연금사망률 (연금생명표) proxy used for the annuity factor and for the payout
    phase.  Both are **[std]** Makeham constructions: the annuity basis is fitted so its
    complete expectation of life at 65 **rounds to** the 제10회 경험생명표 65세 기대여명
    of 23.7 years male and 27.1 female [REG-R33] — the fitted values are 23.663 and
    27.060 — and the insurance basis is that curve at ``mu / 0.80``.  The 경험생명표 qx
    table is **not published** [REG-R34]; this file must never be presented as it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def lapse_table():
    """The annual 해지율 scale by completed policy year, from *lapse_table.csv*.

    Read **without** an index: the lookup is a band test, each row giving the rate that
    holds from ``dur_from`` completed policy years until the next row.  The scale is
    calibrated so the seven-year persistency is 28.9%, against the only published Korean
    figure for this product — 「변액보험의 7년 평균 유지율은 30% 미만」, itself
    second-hand inside [R1].
    """
    return pd.read_csv(input_dir() / lapse_table_file)               # noqa: F821


def fund_table():
    """The 특별계정 fund menu and its allocations, from *fund_table.csv*.

    Indexed by ``(fund_set, fund_id)``.  Two funds — 채권형 and 주식형 — are the minimum
    that exercises a pro-rata allocation, a per-fund 운용보수 and the mandatory bond
    floor at once; real Korean menus run from 5 to 51 funds [S4] [S10].  The three sets
    shipped sit exactly on the three rungs of the mandatory 채권형 ladder [S1] [R1],
    ``asset_class`` naming which fund the floor is measured on.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / fund_file, index_col=["fund_set", "fund_id"])  # noqa: F821


def charge_table():
    """The 상품요약서 fee stack, one row per charge line, from *charge_table.csv*.

    Indexed by ``line``.  ``value`` is a rate or an amount and the ``base`` column says
    which; ``timing`` says when it is taken and ``account`` which side of the 특별계정 /
    일반계정 boundary it lands on.  The commission scale and the insurer's own unit
    expenses live here too, so that every parameter with a provenance is in a file that
    carries one.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / charge_file, index_col="line")                 # noqa: F821


def risk_prem_table():
    """The 위험보험료 scale by attained 보험나이 band, from *risk_prem_table.csv*.

    Read **without** an index, the lookup being a band test on ``age_from``.  The rate
    is a fraction of the 기본보험료 and the applicable row is the highest ``age_from`` at
    or below the attained age.  The published band is 0.004%–0.011% (₩12–₩32 a month on
    the anchor cell) [S2] [S4]; the grading across it by age is **[std]**.
    """
    return pd.read_csv(input_dir() / risk_prem_file)                 # noqa: F821


def return_scenario():
    """The deterministic gross asset returns, from *return_scenario.csv*.

    Indexed by ``(scenario_id, fund_id)``: one annual **gross** separate-account asset
    return per fund, held constant for the whole projection.  Gross, not net — the
    특별계정 운용보수 of :func:`fund_table` is deducted inside the 기준가격 afterwards, so
    the management fee is a modelled cash flow rather than an assumption.  Three
    scenarios are shipped, the base one and the two other returns a Korean variable
    illustration must show [R2] [REG-R48].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / return_scenario_file,                          # noqa: F821
        index_col=["scenario_id", "fund_id"])


def crediting_table():
    """The payout-phase 공시이율 and 최저보증이율 ladder, from *crediting_table.csv*.

    Read **without** an index, the lookup being a band test on completed years since
    annuitisation.  Two bases are shipped: ``decl_2026``, on which the declared rate is
    the 2026 평균공시이율 of 2.50% [REG-R48] and the 최저보증이율 floor of 1.00% / 0.75% /
    0.50% [S1] never binds, and ``min_guar``, on which the declared rate is nil so that
    ``Max[공시이율, 최저보증이율]`` resolves to the floor and the ladder is exercised by a
    shipped model point.
    """
    return pd.read_csv(input_dir() / crediting_file)                 # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

fund_file = "fund_table.csv"

charge_file = "charge_table.csv"

risk_prem_file = "risk_prem_table.csv"

return_scenario_file = "return_scenario.csv"

crediting_file = "crediting_table.csv"

pd = ("Module", "pandas")
