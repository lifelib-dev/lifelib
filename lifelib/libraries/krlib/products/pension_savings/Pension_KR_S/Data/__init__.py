# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The nine input CSVs are read here, **once per model**, and referenced from
:mod:`~.Pension_KR_S.Projection` as ``data``. :mod:`~.Pension_KR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/pension_savings/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so a
diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Pension_KR_S`` folder without its parent's CSVs produces a model that reads and then
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
decl_rate_file          decl_rate_table()               decl_rate_table.csv
guar_rate_file          guar_rate_table()               guar_rate_table.csv
pricing_table_file      pricing_table()                 pricing_table.csv
expense_table_file      expense_table()                 expense_table.csv
tax_table_file          tax_table()                     tax_table.csv
======================  ==============================  ==========================

.. rubric:: The mortality table is a construction, not a copy

**No Korean industry mortality table is public.** 경험생명표 (*gyeongheom saengmyeongpyo*,
the experience life table), currently the 제10회 applied to new business from 2024-04, is
produced by 보험개발원 (Korea Insurance Development Institute) under the statutory office
of 보험요율산출기관, 보험업법 제176조, which carries **no publication obligation**. What is
released is the summary — 평균수명 남 86.3세 / 여 90.7세 and 65세 기대여명 남 23.7년 / 여
27.1년 on the 제10회 — and not the rates.

So :func:`mort_table` reads a **[std] construction** on the *annuitant* basis, and it must
not be shared with ``WholeLife_KR_S``: one table is loaded for survival and the other for
death, and using either for both is wrong in a known direction.

The construction has three parts, all recorded in :func:`mort_anchor_table` and asserted by
``Projection.check_mort_law``:

* a Makeham law ``mu(x) = A + B c**y`` with ``y = max(0, x - setback)``,
  ``q(x) = 1 - exp(-mu(x))``, fitted jointly to the six annuitant rates two carriers publish
  in their 상품요약서 — 「연금사망률」 and 「개인연금사망률」 at ages 40 to 80 — and to the
  annuity factors the one published annuitisation illustration implies, at **two** interest
  bases;
* the female table is the male law **set back four years**, the whole-year setback closest to
  the published 65세 기대여명 gap of 3.4 years between the sexes; it does not reproduce that
  gap — the fitted tables differ by 3.66 years at 65;
* a second vintage, ``annuitant_revised``, is the issue vintage times 0.85 — a one-step
  lightening of the order the 제9회 → 제10회 revision produced — which is what the
  연금사망률 ratchet clause in every retrieved 약관 switches to when it is in the money.

**The fit honours the annuity factors and misses the rates, and the file says so rather than
smoothing it away.** The two published life-annuity implied factors are recovered to four
significant figures (23.7004 against 23.7000 and 31.1799 against 31.1768, inside the rounding
of the published 만원 amounts). The published *rates* are not: the fitted male rates run
about 1.30 times the published anchor at 70 and 0.72 times it at 80, and the female rates,
being a setback rather than an independent fit, run 1.9 to 2.8 times the published female
rates over ages 50 to 70. A three-parameter law cannot honour both, and the annuity factor is
what the payout phase depends on. Every row of both files carries a ``provenance`` column
saying which part of the construction it came from, and that the file is not a copy of a
보험개발원 table.

To swap in a company or filed basis, replace ``mort_table.csv`` with a same-schema file, or
point ``mort_table_file`` at a different name, then clear the cache. No formula changes:
the lookup already carries the table name and the sex. ``Projection.check_mort_law`` will
then report the shipped rates as no longer equal to the stated law, which is the correct
answer once the table is a real one.
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

    Indexed by ``point_id``.  Point 1 is the technical notes' worked-example anchor cell:
    male, 보험나이 40 at issue, 기본보험료 ₩500,000 a month for twenty years to 60, annuity
    from 65 as a 종신연금형 with a ten-year guarantee.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The [std] annuitant mortality rates by table, sex and age, from *mort_table.csv*.

    Two vintages live in the file under the ``table`` key: ``annuitant_issue``, the basis
    filed in the 산출방법서 at 가입, and ``annuitant_revised``, the lighter table a
    경험생명표 revision would produce.  Neither is a copy of a 보험개발원 table; both are
    constructions on the Makeham law recorded in :func:`mort_anchor_table`.  See the Space
    docstring.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["table", "sex", "age"]).sort_index()


def mort_anchor_table():
    """The law parameters, the terminal age and the published anchor rates, by table and sex.

    Read from *mort_anchor_table.csv*, indexed by ``table``, ``sex`` and ``item``.  The
    ``law_a`` / ``law_b`` / ``law_c`` / ``age_setback`` / ``improve_factor`` rows are what
    ``Projection.check_mort_law`` re-derives the shipped rates from; ``omega_age`` is the
    terminal age; and the ``pub_q_*`` rows are the six annuitant rates two carriers publish
    in their statutory product summaries — the only Korean annuitant mortality figures in
    this library's input set, quoted rather than transcribed from a table nobody may read.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_anchor_file,                              # noqa: F821
        index_col=["table", "sex", "item"]).sort_index()


def lapse_table():
    """The [std] 해지 (surrender and lapse) rates by basis, segment and duration.

    Read from *lapse_table.csv*.  Two bases: ``pension``, the product's own vector, and
    ``savings``, the steeper comparison vector of a non-qualified savings contract, carried
    so the two can be run side by side.  Three segments in each: ``premium_paying`` carries
    a duration curve keyed by ``from_year``, the first **0-based** policy year index ``t``
    it applies from — ``from_year = 0`` is the first projected year — ``paid_up`` the single
    rate applying between 납입완료 and 연금개시, and ``in_payment`` the zero that must apply
    once the annuity has started.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file,                              # noqa: F821
        index_col=["basis", "segment", "from_year"]).sort_index()


def decl_rate_table():
    """The 공시이율 (declared crediting rate) scenarios, from *decl_rate_table.csv*.

    Indexed by ``scenario`` and ``from_year`` — the **0-based** policy year index ``t`` the
    step applies from — so a scenario is a step function of policy year rather than a
    scalar.  ``base`` is the composite's level 2.15%; ``floor`` drives
    the declared rate below the guarantee at every duration, which is what the second column
    of a published illustration shows; ``hybrid`` is the one retrieved design that pays a
    fixed 3.5% for five years before reverting.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / decl_rate_file,                                # noqa: F821
        index_col=["scenario", "from_year"]).sort_index()


def guar_rate_table():
    """The 최저보증이율 ladder, from *guar_rate_table.csv*, keyed by elapsed policy years.

    ``from_year`` is the 0-based policy year index ``t`` the step applies from, so the first
    band is keyed ``0``.

    The floor steps **down** with duration — 1.25% to five years, 1.00% to ten, 0.50%
    after — which is the opposite of intuition and matters: the guarantee is strongest
    exactly where the fund is smallest.  A 금리연동형보험 must set one at all, under
    감독규정 제7-60조제10호.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / guar_rate_file, index_col="from_year")         # noqa: F821


def pricing_table():
    """The pricing, charge and module basis, one row per item, from *pricing_table.csv*.

    The two published charge percentages and their periods, the annuity-phase charge, the
    100.1% minimum-fund ratio, the payment and annuity frequencies, the 표준해약공제액
    coefficients of 별표 14, the best-estimate mortality factor and the loan, holiday and
    dividend parameters.  Every row carries its source tag or its **[std]** rationale in the
    ``provenance`` column.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / pricing_table_file, index_col="item")          # noqa: F821


def expense_table():
    """The best-estimate cash expense and commission levels, from *expense_table.csv*.

    These are **cash flows**.  They are entirely separate from the 계약체결비용 and
    계약관리비용 of :func:`pricing_table`, which are contractual loadings deducted inside
    the 계약자적립액; mixing the two double-counts expense in one direction and destroys the
    fund calibration in the other.  The commission rows are zero because the composite
    follows a direct-channel product whose published 모집수수료율 is 0.00% in every year.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / expense_table_file, index_col="item")          # noqa: F821


def tax_table():
    """The 연금저축 tax parameters, from *tax_table.csv*, one row per item.

    The 세액공제 rates and cap, the ₩18,000,000 contribution ceiling, the 16.5%
    기타소득세 on a 연금외수령, the 연금소득 withholding bands including the 3.3%
    종신계약 rate in force from 2026-01-01, the ₩15,000,000 aggregation threshold and the
    three limbs of the statutory 연금수령 test.  **None of these is an insurer cash flow**
    and none of them enters :func:`~.Pension_KR_S.Projection.net_cf`; they are carried
    because they are what drives the lapse and annuitisation-election assumptions.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / tax_table_file, index_col="item")              # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

mort_anchor_file = "mort_anchor_table.csv"

lapse_table_file = "lapse_table.csv"

decl_rate_file = "decl_rate_table.csv"

guar_rate_file = "guar_rate_table.csv"

pricing_table_file = "pricing_table.csv"

expense_table_file = "expense_table.csv"

tax_table_file = "tax_table.csv"

pd = ("Module", "pandas")
