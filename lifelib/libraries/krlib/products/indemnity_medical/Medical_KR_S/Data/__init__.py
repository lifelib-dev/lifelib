# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.Medical_KR_S.Projection` as ``data``. :mod:`~.Medical_KR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/indemnity_medical/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Medical_KR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ============================  ==========================
Reference               Cells                         File
======================  ============================  ==========================
model_point_file        model_point_table()           model_point_table.csv
mort_table_file         mort_table()                  mort_table.csv
lapse_table_file        lapse_table()                 lapse_table.csv
utilisation_table_file  utilisation_table()           utilisation_table.csv
severity_table_file     severity_table()              severity_table.csv
claim_shape_file        claim_shape_table()           claim_shape_table.csv
oop_ceiling_file        oop_ceiling_table()           oop_ceiling_table.csv
======================  ============================  ==========================

.. rubric:: Every one of these files is a [std] construction, and that is a finding

보험개발원 (Korea Insurance Development Institute) is the statutory 보험요율 산출기관
under 보험업법 제176조, and the 장기손해보험 참조순보험요율 it publishes covers
일반상해, 교통상해, 질병 사망률, 후유장해, 입원율, 암 발생률, 비용손해, 재물손해 and
배상책임 — **실손의료보험 is not among them**. The 산출방법서, where an insurer's
예정위험률 and 예정사업비율 actually live, is a 기초서류 filed under 보험업법 제5조제3호
and 제127조 and is not published. There is therefore **no public Korean
indemnity-medical morbidity or severity basis at all**: this is a positive finding about
what Korea publishes, not an unfetched document, and it is the exact boundary at which
this model marks its basis [std].

What the supervisor does publish, annually and in quantity, is *aggregate* experience:
in-force counts by generation, premium income, claims split 급여/비급여, 경과손해율
overall and by generation against a stated break-even of about 85%, claims by treatment
category and by provider class, per-policy claim amounts by generation, a twelve-band
claim-size distribution by generation, the 65% zero-claim mass and the top-decile
concentration, the NHIS coverage ratios by provider class and age band, and the
본인부담상한제 threshold table. Every table below is anchored on those, and every row
says which.

``mort_table.csv``
    A [std] Makeham construction, ``q(x) = 1 - exp(-(A + B c^x))`` above age 15 with a
    log-linear child schedule below it, fitted to the four summary statistics
    국가데이터처 publishes — 기대수명 at birth, 기대여명 at 40 and at 65, and survival to
    age 80. It is **not** a transcription: 제10회 경험생명표, the industry table applied
    from 2024-04, is not published in full, and the single-year 완전생명표 qx tables live
    behind KOSIS and were not downloaded. The direction of prudence runs the *wrong way*
    here: on a one-year indemnity contract death **releases** the liability, so an
    over-statement of mortality is anti-conservative, the reverse of every protection
    product in this library.

``lapse_table.csv``
    A [std] annual lapse schedule by policy year. No 실손-specific persistency table
    exists in public. The ultimate rate is anchored on the only 실손-specific figure
    there is — the 1-3세대 in-force block fell 3.3% in 2025 — which blends lapse, death
    and conversion, so the 2.0% ultimate is what is left of it once mortality and the
    renewal decline are taken out. The first-year rate is set against an [unverified]
    장기손해보험 13회차 유지율 of about 86%, from a news summary rather than a retrieved
    disclosure. There is **nothing to break the fall** on this contract: with no
    surrender value there is no 보험료 자동대출납입, so a missed premium really does
    lapse the policy.

``utilisation_table.csv``
    Annual claim **frequencies** per policy by sex and five-year age band — admissions,
    급여 and 비급여 outpatient visits, and the three 3대비급여 act counts — plus the mean
    length of stay that the room-differential daily-average cap needs. These are
    frequencies of events **giving rise to a paid claim**, averaged over the whole
    population including the roughly 65% of insureds who claim nothing in a year, which
    is why they look low against national utilisation. The level is *solved*: the
    age-40 male row is set so that the anchor cell's first policy year reproduces the
    published 4세대 2022 급여 and 비급여 loss ratios on the published 2021 new-business
    premium anchor. The age curves and the sex factors are [std] shapes following the
    NHIS coverage ratios by age band. Pregnancy and childbirth are **excluded from
    cover**, so there is deliberately no maternity bump in the female rows.

``severity_table.csv``
    A discrete cost distribution per event for each of eight streams. A single mean is
    unusable on this product: the deductible is ``max(flat floor, percentage)``, which is
    a flat amount below a crossing point and a percentage above it, so the payment is a
    kinked function of cost and the **shape** of the cost distribution decides the claim.
    The 건강보험심사평가원 price survey found 도수치료 quoted anywhere between ₩5,000 and
    ₩600,000 across Seoul hospitals; that dispersion is the product's structural problem
    and a mean would erase it.

``claim_shape_table.csv``
    The distribution of a policy's **annual rated 비급여 claim** across ten buckets, as a
    share and a representative amount. This is the input the experience-rating loop runs
    on, and it is the one table whose *dispersion* matters more than its mean: the
    요율 상대도 band is decided by where a policy's annual claim falls against fixed
    money thresholds, so the band mix is a property of the distribution and not of the
    average. Bucket 0 carries the 72.9% of contracts assessed with no rated claim, and
    the four positive groups are calibrated so that at the anchor cell's first-year
    claim level the band mix reproduces the published commencement distribution
    72.9 / 25.3 / 0.8 / 0.7 / 0.3 exactly — which is what makes the solved band-1
    relativity come out at the specification's 0.9575.

``oop_ceiling_table.csv``
    The 본인부담상한제 annual ceiling by NHI-contribution decile, 2026 scale. This is the
    only table here that is a **transcription of a published number** rather than a
    construction, and it is the single most important interaction in the product: the
    NHIS refunds the excess of a member's annual statutory co-payment over the ceiling,
    and the 표준약관 excludes the refundable amount from cover twice over, so the 급여
    half of the claim is truncated — and truncated differently by income.

To swap in a company basis, replace the CSVs with same-schema files, or point the
``*_file`` References at different names, and clear the cache. No formula changes.
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

    Indexed by ``point_id``.  ``point_id = 1`` is the technical notes' worked-example
    anchor cell — male, 만나이 40 at issue, all five 보장종목 held, ₩50,000,000 a year
    per 보장종목 and the ₩11,982 monthly office premium the 2021 launch release prints
    for that exact life.  The others exercise the 보장종목 elections, the
    보험가입금액 menu, the optional modules and the edge ages.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The **[std]** mortality construction by sex and age, from *mort_table.csv*.

    Not a copy of 제10회 경험생명표, which 보험개발원 does not publish in full: a Makeham
    construction fitted to the four summary statistics 국가데이터처 does publish.  Read
    as an annual rate of mortality at 만나이 ``age``.  On this product death is a
    liability *release*, so the usual direction of prudence is inverted — see the Space
    docstring.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def lapse_table():
    """The **[std]** annual lapse rates by policy year, from *lapse_table.csv*.

    Policy years beyond the last row take that row.  Non-payment lapse only: the
    policyholder's separate right to decline the annual renewal is a different decrement
    and carries its own rate, ``Projection.renewal_decline_rate``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def utilisation_table():
    """The **[std]** annual claim frequencies by sex and age band, from
    *utilisation_table.csv*.

    Indexed by ``sex`` and ``age_start``, the lower edge of the five-year band.  The
    columns are the frequencies of events giving rise to a **paid** claim, per policy per
    year, averaged over a population most of which claims nothing: ``adm_rate``,
    ``visit_rate_ge``, ``visit_rate_np``, ``act_rate_physio``, ``act_rate_inject`` and
    ``act_rate_mri``, plus ``los_days``, the mean length of stay the 상급병실료
    daily-average cap is applied against.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / utilisation_table_file,                        # noqa: F821
        index_col=["sex", "age_start"])


def severity_table():
    """The **[std]** discrete cost distribution per event, from *severity_table.csv*.

    Indexed by ``stream`` and ``point``.  Eight streams: ``ge_in`` and ``ge_out`` are the
    급여 본인부담금 per admission and per visit, ``np_in`` and ``np_room`` the 비급여
    cost per admission excluding and comprising the 상급병실료 차액, ``np_out`` the
    비급여 cost per visit, and ``physio``, ``inject`` and ``mri`` the per-act cost of the
    three 3대비급여 classes.  The deductible is a kinked function of cost, so the shape
    of each distribution, not its mean, decides the claim.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / severity_table_file,                           # noqa: F821
        index_col=["stream", "point"])


def claim_shape_table():
    """The **[std]** distribution of a policy's annual rated 비급여 claim, from
    *claim_shape_table.csv*.

    Indexed by ``bucket``.  ``share`` is the proportion of contracts in the bucket and
    ``claim_amount`` the representative annual rated 비급여 claim of a contract in it, in
    KRW at the anchor cell's first-year level; the model reads the amounts as multiples
    of the table's own mean and rescales them to whatever claim level it is projecting.
    Bucket 0 is the no-claim mass that becomes 1단계.  This is the table the
    비급여 할인·할증 loop runs on.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / claim_shape_file, index_col="bucket")          # noqa: F821


def oop_ceiling_table():
    """The 본인부담상한제 annual ceiling by NHI-contribution decile, from
    *oop_ceiling_table.csv*.

    Indexed by ``decile``, 1 to 10, on the 2026 scale.  The NHIS refunds a member's
    annual 본인일부부담금 above this amount, and the 표준약관 excludes anything so
    refundable from cover outright, so this is the level at which the 급여 half of the
    insured loss stops accruing.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / oop_ceiling_file, index_col="decile")          # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

utilisation_table_file = "utilisation_table.csv"

severity_table_file = "severity_table.csv"

claim_shape_file = "claim_shape_table.csv"

oop_ceiling_file = "oop_ceiling_table.csv"

pd = ("Module", "pandas")
