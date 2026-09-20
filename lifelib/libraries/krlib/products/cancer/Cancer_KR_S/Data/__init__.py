# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.Cancer_KR_S.Projection` as ``data``. :mod:`~.Cancer_KR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/cancer/``, rather than data stored inside the model. The model folder therefore
holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values -- so a diff of
the model shows logic changes only. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Cancer_KR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference and
a reader Cells:

=======================  ================================  ==========================
Reference                Cells                             File
=======================  ================================  ==========================
model_point_file         model_point_table()               model_point_table.csv
mort_table_file          mort_table()                      mort_table.csv
incidence_table_file     incidence_table()                 incidence_table.csv
tier_share_file          tier_share_table()                tier_share_table.csv
tier_table_file          tier_table()                      tier_table.csv
survival_table_file      survival_table()                  survival_table.csv
care_table_file          care_table()                      care_table.csv
lapse_table_file         lapse_table()                     lapse_table.csv
=======================  ================================  ==========================

Every file but ``model_point_table.csv`` carries a ``provenance`` column, and every cell in
it begins with a citation tag. That is not decoration on this product: the eight files sit
at three quite different levels of authority and the column is where a reader is told which.

.. rubric:: The incidence basis is sourced, and the mortality basis is not

The two decrement files are the opposite of one another, and the contrast is the single
most important fact about this model's inputs.

``incidence_table.csv`` is **published data reproduced verbatim**. 보험개발원 (the Korea
Insurance Development Institute) displays its 장기손해보험 참조순보험요율 in force from
2024-04-01, and that display carries a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid by
age and sex [R5] [REG-R61]. Its definition is the *insured* one -- invasive cancer excluding
기타피부암 (C44) and 갑상선암 (C73), classified by 원발부위 -- so it already embodies the
tier carve-out the 약관 make and the 원발부위 기준 the supervisor imposed from 2011-04-01.
Only the two rows above the published age-80 endpoint are ``[std]``, and they say so.

``mort_table.csv`` is a **[std] construction**. Korea's industry table, the 제10회
경험생명표 applied from 2024-04, is **not published in full**: 보험개발원 releases the
평균수명 and the 기대여명 and not the rates [REG-R33] [REG-R34]. There is no Korean
equivalent of the freely downloadable Japanese 標準生命表, so there is no published rate to
anchor on. What is shipped instead is a Makeham ``q(x) = 1 - exp(-(A + B c^(x+0.5)))`` whose
two free parameters are solved so that the table reproduces the **국가데이터처 생명표**'s
2024 기대여명 at ages 40 and 65 exactly -- 남 41.9 / 19.5 and 여 47.4 / 23.7 [REG-R38]. It
then returns 기대수명 at birth of 80.80 and 86.88 against the published 80.8 and 86.6, which
is a check rather than a target and is the only external validation available. Drop a
licensed extract in over the same schema -- ``sex``, ``age``, ``mort_rate`` -- and no formula
changes.

.. rubric:: Four files carry the standardizations, and each says which

``tier_share_table.csv`` splits the sourced base rate into the contract's tiers. It is
``[std]`` and it is where most of the model's judgement lives: the 특정소액암 and 유사암
shares are anchored on [R1]'s 2023 all-ages crude site rates -- 대장 63.8, 유방 58.4,
전립선 44.3, 갑상선 69.3 and 상피내암 74.7 per 100,000 against an excluding-thyroid base of
495.0 -- and then graded in age and split by sex, because those all-ages figures mix age
distributions that differ violently. The 유사암 ratio is a **floor**: [R1] does not cover
경계성종양 at all, does not identify 대장점막내암 inside 대장 D010-D012, and does not carry
기타피부암 in its top-ten table.

``survival_table.csv`` is the post-diagnosis basis, and it exists because a cancer contract
goes on paying after the diagnosis benefit. Relative survival -- 「관찰생존율을 일반인구의
기대생존율로 나누어 구한 값」 [R1] -- is a *ratio to an expected general-population
survival*, not a cohort curve and not a transition rate, so it converts into an **excess
hazard added to** the base table rather than a replacement for it. The five select years are
calibrated so that the five-year survival ratio equals the published excluding-thyroid
figure, 남 65.9% / 여 74.0% [R1]; the 특정소액암 tier is calibrated separately off [R1]'s own
site rows; and the 유사암 tier appears in **no row of the file at all**, because 갑상선
five-year relative survival is 100.2% and lifetime 갑상선 mortality risk 0.1% [R1].

``care_table.csv`` is the weakest file in the model and says so on every row. **No Korean
source publishes cancer admissions, bed-days, operations or treatment courses per diagnosed
patient.** The one published utilisation series on the 보험개발원 display is a 질병입원율 for
*all* disease [R5]. The shape is standardized on the clinical ordering the contracts' own
design implies and the level on the 180-day-per-stay cap they carry [S1] [S4] [R3].

``lapse_table.csv`` carries three segments rather than a policy-year grid, because the
functional form is prescribed rather than observed: the FSS's November 2024 ruling makes a
**로그-선형 model converging to 0.1% at 완납** the 원칙모형 for 무.저해지 business, with a
post-완납 ultimate of 0.8% [REG-R27]. **No public Korean lapse or persistency figure for
암보험 exists** [R3], so the model implements the prescribed shape and standardizes only its
starting level.

``tier_table.csv`` is the benefit ladder itself -- 200 / 100 / 60 / 20 per cent of the
보험가입금액 -- read directly off the one retrieved 약관 that states every tier as an amount
at 보험가입금액 1,000만원 [S3 별표 1]. It also carries each tier's own 면책기간, which is
where the product's **two start dates** come from: the invasive tiers attach on the 91st day
and the 유사암 tier on the 보험계약일.
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
    following ``annuallife.TradLife_A``, so the model works from any checkout location.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*.

    Indexed by ``point_id``; ``point_id = 1`` is the technical notes' worked-example anchor
    cell, male at the 감독규정 기준연령 요건 age of 40 [REG-R9].  ``premium`` is an input on
    this product in a stronger sense than on most: no Korean carrier publishes a rate table
    for a cancer main contract, the 산출방법서 is a 기초서류 filed with the FSC and not a
    published document, and the 참조순보험요율 reaches the public only as the 보험가격지수
    ratio [REG-R22], so every premium in the table is a **[std]** modelling value.

    This is the one input file exempt from the ``provenance`` column, because a model point
    is a *configuration* -- one policy's own terms -- rather than an assumption.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The **[std]** all-cause mortality table by sex and age, from *mort_table.csv*.

    A Makeham ``q(x) = 1 - exp(-(A + B c^(x+0.5)))`` whose two free parameters reproduce the
    국가데이터처 생명표's 2024 40세 and 65세 기대여명 exactly [REG-R38], **not** a copy of
    the 제10회 경험생명표, which 보험개발원 does not publish in full [REG-R33] [REG-R34].
    See the Space docstring for why the distinction is load-bearing.  Ages 15 to 100, the
    composite's issue-age range and its 100세 만기.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def incidence_table():
    """보험개발원 「기타피부암 및 갑상선암 이외의 암 발생률」, from *incidence_table.csv*.

    The 참조순보험요율 display in force from 2024-04-01, by age and sex, on the published
    ten-year grid [R5] [REG-R61].  Indexed by ``sex`` and ``age``; ``Projection.inc_rate``
    interpolates log-linearly between the grid ages.  The two rows above 80 are **[std]**
    extrapolations and their ``provenance`` says so.  These are sourced values reproduced
    with their attribution, in deliberate contrast to :func:`mort_table`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / incidence_table_file,                          # noqa: F821
        index_col=["sex", "age"])


def tier_share_table():
    """The **[std]** tier decomposition of the base incidence rate, by sex and age.

    Three shares per row, from *tier_share_table.csv*: ``minor_share`` -- the fraction of the
    sourced base rate falling in the 특정소액암 tier, its complement being the 일반암 tier;
    ``high_share`` -- the 고액암 sub-share, which pays *in addition* rather than instead; and
    ``similar_share`` -- 유사암 incidence expressed as a ratio to the base rate, which is
    **additive** to it because the 유사암 tier is outside the base rate's own definition.
    Anchored at ages 20, 40, 60 and 80 and interpolated linearly in age.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / tier_share_file,                               # noqa: F821
        index_col=["sex", "age"])


def tier_table():
    """The benefit ladder and each tier's own 면책기간, from *tier_table.csv*.

    Four rows: ``high`` (고액암, 100% *in addition* to the general tier, so 200% in total),
    ``general`` (일반암, 100%), ``minor`` (특정소액암, 60%) and ``similar`` (유사암, 20%),
    read off the one retrieved 약관 stating every tier as an amount at 보험가입금액
    1,000만원 [S3 별표 1].  ``wait_months`` is 3 for the invasive tiers and **0** for
    유사암, which is the product's two-start-date structure; ``waives_premium`` is 1 for
    일반암 and 고액암 alone [S3 제14조제1항] [S1 제9조제1항].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / tier_table_file, index_col="tier")             # noqa: F821


def survival_table():
    """The **[std]** post-diagnosis excess hazard by sex, tier and select year.

    From *survival_table.csv*, indexed by ``sex``, ``tier`` and ``dur_year`` 1 to 5 with 6
    standing for the ultimate.  Calibrated so that ``exp(-sum of the five annual hazards)``
    reproduces the published 2019-2023 5년 상대생존율 excluding thyroid, 남 65.9% / 여 74.0%
    [R1], for the general tier, and an [R1]-derived 87.1% / 88.8% for the 특정소액암 tier.
    The 유사암 tier is absent from the file by design: 갑상선 relative survival is 100.2%
    and lifetime 갑상선 mortality risk 0.1% [R1], so a 유사암 diagnosis changes no state.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / survival_table_file,                           # noqa: F821
        index_col=["sex", "tier", "dur_year"])


def care_table():
    """The **[std]** care intensities per diagnosed life, by select year since diagnosis.

    From *care_table.csv*: cancer admissions and mean days per admission, 관혈 and 비관혈
    operations, and the annual hazard of the *first* qualifying 항암약물.방사선 treatment.
    Indexed by ``dur_year`` 1 to 5 with 6 standing for the ultimate.  Every figure is a
    standardization: no Korean source publishes treatment volume per diagnosed cancer
    patient, and the one published utilisation grid on the 보험개발원 display is a
    질병입원율 for all disease rather than for cancer [R5].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / care_table_file, index_col="dur_year")         # noqa: F821


def lapse_table():
    """The three-segment **[std]** lapse basis, from *lapse_table.csv*.

    ``first_year`` 4.6%, ``at_completion`` 0.1% and ``post_payment`` 0.8%.  Three segments
    rather than a policy-year grid because the functional form is *prescribed*: the FSS's
    November 2024 계리가정 ruling makes a 로그-선형 model converging to 0.1% at 완납 the
    원칙모형 for 무.저해지 business, with a 0.8% post-완납 ultimate [REG-R27].
    ``Projection.lapse_rate`` interpolates log-linearly between the first two and steps to
    the third at 납입완료.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="segment")         # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

incidence_table_file = "incidence_table.csv"

tier_share_file = "tier_share_table.csv"

tier_table_file = "tier_table.csv"

survival_table_file = "survival_table.csv"

care_table_file = "care_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")
