# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.Child_KR_S.Projection` as ``data``. :mod:`~.Child_KR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/child/``, rather than data stored inside the model. The model folder therefore
holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so a diff of
the model shows logic changes only. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Child_KR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
incidence_file          incidence_table()               incidence_table.csv
basis_file              basis_table()                   basis_table.csv
neonatal_file           neonatal_table()                neonatal_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
av_table_file           av_table()                      av_table.csv
======================  ==============================  ==========================

.. rubric:: The data position for this product is the worst in the library

**No Korean mortality table in this library is a published table.** 경험생명표
(*gyeongheom saengmyeongpyo*, the industry experience life table, 제10회 applied from
2024-04) is produced by 보험개발원 and is **not** released in full: what is published is
the summary — the 평균수명 and the 기대여명 — and not the rates [REG-R33] [REG-R34].
``mort_table.csv`` is therefore a **[std] construction**, log-linear between anchor ages
shaped on the 통계청 완전생명표 age pattern [REG-R38] [REG-R39], carrying the infant
peak, the childhood trough at about age 10 and the adolescent turn that a child policy is
exposed to for its first two decades. It is used for the insured child **and** for the
계약자, whose death is the second of the two waiver triggers.

**The morbidity position is worse, though not for the reason a first reading suggests.**
Each carrier's own 적용위험률 lives in the 산출방법서, an undisclosed 기초서류 [REG-R2],
and the bureau's 참조순보험요율 is filed under 보험업법 제176조제4항 with no general
obligation to publish [REG-R4]. But 제176조제9항 lets the bureau publish 순보험요율 산출
자료 where policyholder protection requires it, and for **장기손해보험** it does: a dated
display carrying 「기타피부암 및 갑상선암 이외의 암 발생률」, 질병입원율 and 후유장해 by
age and sex, whose age grid reaches **연령 0 and 10** [REG-R61]. **This product's research
pass never opened it** — the ``cancer`` and ``indemnity_medical`` passes did — and
**nothing on child incidence was retrieved** from 보험개발원, 국가암정보센터 or 통계청 in
this pass. Every rate in ``incidence_table.csv`` is therefore a **[std] construction**
whose provenance cell names the authority its shape rests on: the 국가암등록통계 연령별
발생률 [REG-R40], the two grids of the 참조순보험요율 display [REG-R61], and the
국민건강보험 진료비 실태조사 [REG-R41]. It is [std] because it was never reconciled to that
display, not because no display exists, and a later pass should re-base the rows off it —
noting that a 참조순보험요율 is a **net premium rate, not a best estimate** [REG-R61]. The one exception is
the row that anchors the whole file: **일반상해 후유장해 발생률(3~100%), 기본계약, 5세,
상해 1급 — 남자 0.0001823, 여자 0.0001163** [S1], the only observation of a Korean child
morbidity rate anywhere in the research, and the point the basic contract's decrement is
calibrated on.

``basis_table.csv`` carries the scalar [std] parameters that turn an incidence into a
cost — the mean 장해지급률, the surgery rates given a diagnosis, the liability severity,
the per-stay cap factor, the 50%-severity share that fires the waiver, the 계약자's
disability-to-mortality ratio, the 누수사고 share of the liability cost, the foetal-loss
rate and the broad-definition factor. ``neonatal_table.csv`` carries the 태아 module: nine
limbs, each with a frequency, an amount (fixed or a ratio to the module's 가입금액), an
expected number of units and a timing — ``birth`` for the 태아보장기간 limbs paid at
birth, ``block`` for the 1년만기 신생아 block. Two of them are **day-capped rather than
amount-capped**, which is why the module's cost is a length-of-stay question.

``lapse_table.csv`` carries three bases: the 2024 계리가정 guideline's 원칙모형
[REG-R27], the 적용해지율 one carrier actually discloses [S1], and a level comparison
vector. ``av_table.csv`` carries the published 표준형 환급률 progression of a current
상품요약서 [S2] as a ``build`` curve indexed by duration in years, and a ``taper`` curve
indexed by the fraction of the term run off, calibrated to reproduce the published 16.0%
at 95 years and 0.0% at 만기 — so that one shipped progression serves every 보험기간.

To swap in a company basis, replace the files with same-schema ones, or point the
filename References at different names, then clear the cache. No formula changes.
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
    worked example — a **태아가입** contract, priced male, 계약나이 0 at the 계약일, birth
    at policy month 5, 100세만기 20년납 월납, 표준형, with both premium waivers on and the
    계약자 male 만 33 — and the other nine exercise the sexes, the issue-age and term
    envelopes, the three surrender-value forms, the optional modules and the switches.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """Annual mortality by sex and 만나이, from *mort_table.csv*.

    A **[std] construction**, log-linear between anchor ages shaped on the Korean
    완전생명표 age pattern [REG-R38] [REG-R39]; the 제10회 경험생명표 is published only as
    summary statistics [REG-R33] [REG-R34].  It serves two lives: the insured child, whose
    mortality begins at birth and not at the 계약일, and the 계약자, whose death is one of
    the two triggers of the premium waiver.  The largest age present is 120, where the
    rate is 1.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"]).sort_index()


def incidence_table():
    """Annual incidence by cause, sex and pivot 만나이, from *incidence_table.csv*.

    Eleven causes — ``disability``, ``disease_disab``, ``cancer``, ``minor_cancer``,
    ``cerebral``, ``cardiac``, ``fracture``, ``burn``, ``hosp_acc``, ``hosp_dis`` and
    ``liability`` — at fourteen pivot ages from 0 to 100, interpolated log-linearly in
    :func:`~.Child_KR_S.Projection.inc_rate_at`.  The two ``hosp_*`` causes are expected
    **days** per policy year rather than event frequencies, before the 1~180일 per-stay
    cap; every other cause is an annual event frequency.

    **Every rate here is a [std] construction and the provenance column says which
    authority its shape rests on**, save the two rows that are not: 일반상해 후유장해
    발생률(3~100%) at 5세, 상해 1급 — 남자 0.0001823, 여자 0.0001163 [S1] — the only
    published Korean child morbidity rate in the whole research file.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / incidence_file,                                # noqa: F821
        index_col=["cause", "sex", "age"]).sort_index()


def basis_table():
    """The scalar [std] parameters of the benefit basis, from *basis_table.csv*.

    Thirteen values, each with its own provenance: the mean 장해지급률 on an accident and
    on a disease impairment, the three surgery rates given a diagnosis, the liability
    severity, the per-stay cap factor on the hospital-cash limbs, the share of 3~100%
    impairments reaching the 50% waiver threshold, the 계약자's disability-to-mortality
    ratio, the 누수사고 share of the liability cost, the foetal-loss rate, the
    broad-definition factor on the two adult-disease limbs, and the 순보험료 share used in
    the 표준해약공제액 computation.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / basis_file, index_col="param")                 # noqa: F821


def neonatal_table():
    """The 태아 module's nine limbs, from *neonatal_table.csv*.

    Each row carries a ``timing`` — ``birth`` for a 태아보장기간 limb paid at birth,
    ``block`` for a limb of the 1년만기 신생아 block — a frequency per birth, a fixed
    ``amount``, an ``amount_ratio`` to the module's own 가입금액, and the expected number
    of ``units``.  The incubator and perinatal-cash limbs are **day-capped rather than
    amount-capped**, so their ``units`` are expected paid days after the contractual
    deduction and inside the cap, which is why the module's cost is a length-of-stay
    question rather than an amount question.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / neonatal_file, index_col="item")               # noqa: F821


def lapse_table():
    """The three lapse bases, from *lapse_table.csv*.

    Each basis carries a first-year rate, the rate reached at 납입완료 and the ultimate
    rate afterwards; the durational shape between the first two is applied in
    :func:`~.Child_KR_S.Projection.lapse_rate`.  ``loglinear`` is the 2024 계리가정
    guideline's 원칙모형 [REG-R27] [R11], ``disclosed`` the 적용해지율 one carrier
    publishes for its suppressed forms [S1], and ``flat`` a level comparison vector.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="lapse_basis")     # noqa: F821


def av_table():
    """The 해약환급금 progression, read from *av_table.csv*.

    Two curves in one file, keyed by the ``curve`` column.  ``build`` is the published
    표준형 환급률 grid of a current 상품요약서 — 0.0% at 1 year, 45.6% at 3, 62.5% at 5,
    73.7% at 10, 78.3% at 15, 82.6% at 20, 101.2% at 30, 122.5% at 40, 144.1% at 50 and
    158.9% at 60 [S2] — indexed by duration in years and held flat beyond 60. ``taper``
    is the terminal collapse, indexed by the fraction of the 보험기간 run off and
    calibrated so that a 100세만기 contract reproduces the published 16.0% at 95 years and
    pays nothing at 만기.  Splitting the progression in two is what lets one shipped grid
    serve every 보험기간 without re-basing the published figures.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / av_table_file,                                 # noqa: F821
        index_col=["curve", "key"]).sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

incidence_file = "incidence_table.csv"

basis_file = "basis_table.csv"

neonatal_file = "neonatal_table.csv"

lapse_table_file = "lapse_table.csv"

av_table_file = "av_table.csv"

pd = ("Module", "pandas")
