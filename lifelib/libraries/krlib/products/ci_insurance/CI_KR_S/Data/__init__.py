# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.CI_KR_S.Projection` as ``data``. :mod:`~.CI_KR_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells cache;
if the readers lived there, every model point would re-read every file. Holding them in
an unparameterized Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/ci_insurance/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``CI_KR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
ci_incidence_file       ci_incidence_table()            ci_incidence_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
======================  ==============================  ==========================

.. rubric:: Every decrement in this model is a construction, and the reason is Korean

Korea publishes neither of the two tables this product needs.

**경험생명표** (*gyeongheom saengmyeongpyo*, the industry experience life table, currently
the 제10회 applied from 2024-04) is produced by 보험개발원 and is **not published in
full**: only summary statistics — 평균수명 and 기대여명 — are released [REG-R33]
[REG-R34]. The **life 참조순보험요율** is defined by 감독규정 제1-2조제1호 as the 위험률
the bureau *files* with the supervisor, not as a published table [REG-R4] [REG-R34]. The
장기손해보험 참조순보험요율 display 보험개발원 *does* publish carries an insured-cancer
발생률 grid and a 질병입원율 grid [REG-R61] — the bases ``Cancer_KR_S`` and ``Medical_KR_S``
use — and no 중대한 질병 item at all, so nothing on it reaches this model. The 산출방법서
that would carry a carrier's own 적용위험률 is a 기초서류, filed and never published
[REG-R2].

What does exist, and it is the whole public evidence base for this product, is a single
2011 상품요약서 that prints its 예정위험률 by sex at ages 20, 40 and 60 [S3]. Both
decrement files are built on it.

``mort_table.csv`` — sex, attained age 15 to ω = 110, ``mort_rate``, ``provenance``.
The male rates are a Makeham form fitted **exactly** to [S3]'s three disclosed male
anchors **in the rate itself, not in the force** — ``q(y) = A + B c^y`` — used to age 60,
and log-linear in ``q`` from there to ``q(110) = 1``; extrapolated, that fit reaches a rate of 1 at about attained age 107 and stands a
third above the shipped ramp by age 100, which is why the old-age shape is a separate
**[std]** rule rather than a continuation. The female rates are **0.5294 times the male
rates at every age below** ω, that ratio being [S3]'s own disclosed female-to-male ratio
at age 20 — the only usable female anchor, because [S3]'s female rates at 40 and 60
extract identical to the male ones and are a PDF column-merge artefact expressly marked
[unverified]; at ω both sexes carry the terminal rate of 1. The construction is known
to **understate** the female advantage: it gives a 15-to-80 death probability ratio of
0.560 against the 0.500 implied by 국가데이터처's survival to age 80 of 남 64.4% /
여 82.2% [REG-R38]. The row-by-row tags say which rows are anchors and which are fill.

``ci_incidence_table.csv`` — sex, attained age 15 to 100, ``cause``, ``ci_rate``,
``provenance``, in long form so that each cause carries its own tag. Five causes:

``cancer``, ``ami``, ``stroke``
    중대한 암, 중대한 급성심근경색증 and 중대한 뇌졸중, **[S3]** at ages 20, 40 and 60,
    log-linear in ``ln(rate)`` between and below those anchors, and above 60 on the
    40-to-60 log-slope decaying geometrically at 0.90 a year **[std]** — undamped, the
    cancer rate passes 1 before age 100.
``other``
    the five remaining 중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식, as
    10.5% of the three headline rates **[std]**: [S4]'s published 3대-to-17대 office
    premium step of 5.30% divided by the 50.6% share the CI benefit takes of the risk
    premium at male 40 on [S3]'s 보장위험별 연간보험료 disclosure.
``ltc``
    장기요양상태 on 노인장기요양 1·2등급, nil below 65 and 0.12% at 65 growing 14% a year
    **[std]** — a placeholder for the construction ``LTC_KR_S`` owns, scaled so the 65+
    mean is of the order implied by [REG-R42]'s 154,688 1·2등급 인정자 at an assumed
    three-year mean duration. **This product's own source set retrieved no inception
    rate; the library's did** — ``LTC_KR_S`` sources a disclosed 요양 1·2등급 발생률 grid
    at ages 40, 50 and 60 by sex, whose male 1·2등급 rate at 60 is 0.000530, about 2.5%
    of this model's CI rate there. Holding this limb at nil below 65, and not modelling
    the 노인성 질병 route below 65 [REG-R55] at all, understates the CI decrement at
    insured ages by that order.

**These are 예정위험률, not best estimate.** [R1] records the margin regime around them —
안전할증 on the 기초발생률 capped at 30% in the early 2000s, raised to 50% in 2015 and
uncapped from 2017 — so the base run is a **valuation-basis run**. ``mort_be_factor`` and
``ci_be_factor`` are the levers that turn it into a best estimate and they are 1.00 on
every model point but one.

``lapse_table.csv`` — policy year, ``lapse_rate``, ``provenance``. The 표준형 comparison
curve, three rows short of a decade with a level tail. **No CI lapse experience of any
kind was retrieved** [R1], so the curve is **[std]**, bounded only by the 적용해지율
envelopes Korean 상품요약서 publish. The suppressed forms do not use it: they run the
**로그-선형 원칙모형** the IFRS17 주요 계리가정 가이드라인 prescribes for 무·저해지
business, converging to 0.1% at 납입완료 with a 0.8% post-완납 ultimate [REG-R27], which
is a formula rather than a table and lives in ``Projection``. Carrying both is the
comparison the guideline itself requires an insurer to disclose.

``model_point_table.csv`` is the exception to all of this: it is a configuration rather
than an assumption, and carries no ``provenance`` column.
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
    cell; the other eight exercise the product's variants, its optional modules and the
    two ends of its issue-age and sum-assured envelopes.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The mortality rates by sex and attained age, from *mort_table.csv*.

    A **[std]** construction anchored on the 예정 경험 사망률 disclosed at three ages by
    one Korean CI 상품요약서 [S3]; not the 경험생명표, which 보험개발원 does not publish
    in full [REG-R33].  Indexed by ``(sex, age)`` with a single ``mort_rate`` column and
    a ``provenance`` column saying, row by row, whether the rate is an anchor, a fit, a
    ramp or the terminal age.  ω is the first age at which the rate reaches 1.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def ci_incidence_table():
    """The CI incidence rates by sex, attained age and cause, from *ci_incidence_table.csv*.

    Long form — one row per ``(sex, age, cause)`` — so that each cause carries its own
    provenance tag, which matters because they do not rest on the same thing: the three
    headline causes are [S3] at three ages and **[std]** everywhere else, while ``other``
    and ``ltc`` are standardizations throughout.

    **These are first-event rates across a competing-risk set, not marginal incidences.**
    The benefit is payable once only across every trigger, and Korea's supervisor
    required the overlap between CI causes to be reflected in the filed rate rather than
    ignored for rate stability as overseas practice does [R1].  Summing published
    site-specific incidences instead would be wrong in the direction the regulation
    specifically addresses.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / ci_incidence_file,                             # noqa: F821
        index_col=["sex", "age", "cause"])


def lapse_table():
    """The 표준형 voluntary surrender rates by policy year, from *lapse_table.csv*.

    The ``policy_year`` key is the **contractual, 1-based label**, not the model's 0-based
    time index: the projection's period ``t`` reads row ``t + 1``, so the file is unaffected
    by the frame's indexing.  Six duration rows and a level tail read for every later year.
    Used only where the
    model point sets ``lapse_basis`` to ``table``; the suppressed forms run the
    로그-선형 원칙모형 of [REG-R27] instead, which is a formula and lives in
    :mod:`~.CI_KR_S.Projection`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

ci_incidence_file = "ci_incidence_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")
