# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.LTC_KR_S.Projection` as ``data``. :mod:`~.LTC_KR_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells cache;
if the readers lived there, every model point would re-read every file. Holding them in an
unparameterized Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/long_term_care/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so a
diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``LTC_KR_S`` folder without its parent's CSVs produces a model that reads and then fails on
first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference and
a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
prevalence_file         prevalence_table()              prevalence_table.csv
grade_share_file        grade_share_table()             grade_share_table.csv
incidence_file          incidence_table()               incidence_table.csv
dementia_file           dementia_table()                dementia_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
av_table_file           av_table()                      av_table.csv
======================  ==============================  ==========================

.. rubric:: Every decrement here is a construction, and the reason is Korean

**No Korean mortality table in this library is a published table.** 경험생명표 (*gyeongheom
saengmyeongpyo*, the industry experience life table, 제10회 applied from 2024-04) is
produced by 보험개발원 and is **not** released in full: what is published is the summary —
the 평균수명 and the 기대여명 — and not the rates [REG-R33] [REG-R34]. ``mort_table.csv`` is
therefore a **[std] Makeham-Gompertz construction**, ``q(x) = 1 - exp(-(A + B c^x))`` with
``A = 0.0003`` and ``c = 1.10``, in which ``B`` is solved so that the complete expectation
of life at 65 reproduces the published 경험생명표 65세 기대여명 — 23.7 years for men and
27.1 for women. The construction is not fitted to anything else, and it reproduces the
second published summary statistic without being asked to: it returns a 평균수명-equivalent
at issue age 40 of 86.4 (men) against the published 86.3, and 90.3 (women) against 90.7.
That agreement is a cross-check on the shape, not evidence about any insurer's experience,
and **no conclusion about Korean insured mortality should be drawn from the file**.

The morbidity basis is public administrative data, which is what makes this product
different from every other decrement in ``krlib``, and it is split over three files because
it is three different things. ``prevalence_table.csv`` carries the 연령별 인정률 of the
2024 노인장기요양보험 통계연보 by sex — a **prevalence**, a point-in-time count of people
*holding* a certification — together with the logistic fitted through it.
``grade_share_table.csv`` carries the grade composition of certified lives **by age band**,
because the severe share is U-shaped in age and a single all-ages vector mis-prices a
1~2등급 benefit by up to a factor of two. ``incidence_table.csv`` carries the one Korean
long-term-care **incidence** rate published in any retrieved document — one carrier's
disclosed 예정위험률 at ages 40, 50 and 60 — which the model uses for its sub-65 age
gradient and sex ratio and as a level cross-check, never as the level itself.
``dementia_table.csv`` carries the 2023 치매역학조사 prevalence for the optional rider.

Converting a prevalence into an incidence is done in :mod:`~.LTC_KR_S.Projection`, where it
belongs, because it needs the mortality of the care state.

``av_table.csv`` is the one file whose numbers come from a **carrier's own published
figures**: the 해약환급금 미지급형 환급률 progression at 40세, 90세만기, 20년납, 월납, from
which the model reconstructs the 계약자적립액 — the amount 감독규정 제7-63조제1항제1호 makes
payable on death from a cause the contract does not cover [REG-R17].

To swap in a company basis, replace the files with same-schema ones, or point the filename
References at different names, then clear the cache. No formula changes.
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

    Indexed by ``point_id``.  ``point_id = 1`` is the anchor cell of the technical notes'
    worked example — 男 만나이 40, 90세만기, 20년납, 월납, 1~2등급, 해약환급금 미지급형 —
    and the other eight exercise the thresholds, the terms, the surrender-value forms, the
    optional modules and the waiting-period variants.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """Healthy-life annual mortality by sex and 만나이, from *mort_table.csv*.

    A **[std] Makeham-Gompertz construction** whose one calibration anchor per sex is the
    published 제10회 경험생명표 65세 기대여명 [REG-R33]; the 경험생명표 itself is not
    published [REG-R34].  See the Space docstring.  ``Projection`` reads it directly — there
    is no best-estimate adjustment factor, because the anchor is an experience statistic and
    not a valuation margin.  The largest age present is 120, where ``mort_rate`` is 1.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def prevalence_table():
    """The certification-prevalence parameters by sex, from *prevalence_table.csv*.

    Five sourced 인정률 anchors per sex — the 2024 연령별 인정률 of the 노인장기요양보험
    통계연보, computed as (계 − 등급외) over population — and the three parameters of the
    logistic **[std]** fitted through them, ``prev_ceil``, ``prev_beta`` and ``prev_x_mid``.
    The anchors are carried for provenance; the model reads the three fitted parameters.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / prevalence_file, index_col=["sex", "param"])   # noqa: F821


def grade_share_table():
    """The grade composition of certified lives by age band, from *grade_share_table.csv*.

    ``share_ge`` is the share of all certified lives at that 장기요양등급 **or above**, so
    ``g2`` is the 1~2등급 share — 0.146 at 65-69, 0.111 at 80-84 and 0.148 at 85 and over.
    The share is indexed by age because the severe share is **U-shaped**: high below 65,
    where only the 노인성 질병 list gets in at all, lowest around 80-84, where the marginal
    entrant is a lightly impaired person newly crossing the 51-point line, and rising again
    at 85 and over.  The grade keys are ASCII codes for the six-point statutory scale and
    the model point column ``benefit_grade`` holds one of them.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / grade_share_file, index_col=["grade", "age"])  # noqa: F821


def incidence_table():
    """The one disclosed Korean long-term-care incidence basis, from *incidence_table.csv*.

    One carrier's 예정위험률 — 요양(1등급) 발생률 and 요양(2등급) 발생률 at 만나이 40, 50 and
    60 by sex — the only Korean long-term-care incidence rate published in any retrieved
    document.  It is a *loaded pricing* rate for a select, underwritten, 180-day-waited
    population and is **not** used as the level of this model's basis; what is taken from it
    is the sub-65 age gradient and the sex ratio, and the ratio of the two is published by
    :func:`~.LTC_KR_S.Projection.disclosed_inc_ratio_at` as the calibration finding.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / incidence_file, index_col=["sex", "age"])      # noqa: F821


def dementia_table():
    """The dementia-prevalence parameters of the optional rider, from *dementia_table.csv*.

    Five sourced band prevalences from the 2023 치매역학조사 and the three parameters of the
    logistic **[std]** fitted through them, plus the two sourced 65+ sex factors.  Read only
    when ``dementia_rider`` is on, but read once per model regardless, as every table here
    is.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / dementia_file, index_col="param")              # noqa: F821


def lapse_table():
    """The lapse-vector parameters, read from *lapse_table.csv*.

    Four values: the first-year rate **[std]**, the 0.1% convergence point at 납입완료 and
    the 0.8% post-완납 ultimate rate that the 2024 계리가정 guidance sets for a 무·저해지
    form [REG-R27], and the level rate of the 표준형 comparison vector **[std]**.  The
    durational *shape* between the first year and 납입완료 is the guidance's own log-linear
    principle model and is applied in :func:`~.LTC_KR_S.Projection.lapse_rate`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="param")           # noqa: F821


def av_table():
    """The 계약자적립액 progression, read from *av_table.csv*.

    Four anchors taken from one carrier's published 해약환급금 미지급형 환급률 progression at
    40세, 주계약 1,000만원, 90세만기, 20년납, 월납 — 48.7% at 20 years, 54.4% at 30, 50.5% at
    40 and 0.0% at 50 — doubled, because that form pays 50% of the notional 기본형 value once
    the premiums are paid.  ``av_ratio`` is therefore the 계약자적립액 as a ratio to cumulative
    office premiums paid, and ``runoff_fraction`` is the fraction of the way from 납입완료 to
    maturity, which is what lets one shipped progression serve every term and paying period.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / av_table_file, index_col="runoff_fraction")    # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

prevalence_file = "prevalence_table.csv"

grade_share_file = "grade_share_table.csv"

incidence_file = "incidence_table.csv"

dementia_file = "dementia_table.csv"

lapse_table_file = "lapse_table.csv"

av_table_file = "av_table.csv"

pd = ("Module", "pandas")
