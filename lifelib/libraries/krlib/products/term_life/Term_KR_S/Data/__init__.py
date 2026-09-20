# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.Term_KR_S.Projection` as ``data``. :mod:`~.Term_KR_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/term_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_KR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
rate_class_file         rate_class_table()              rate_class_table.csv
prem_rate_file          prem_rate_table()               prem_rate_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
======================  ==============================  ==========================

:func:`prem_anchor_table` is derived from :func:`prem_rate_table` rather than read from a
sixth file, so it costs no extra read.

.. rubric:: The mortality table is a construction, and there was no alternative

The industry table is the **경험생명표** (*gyeongheom saengmyeongpyo*, experience life
table), prepared by 보험개발원 every five years from life-insurance policyholder
statistics; the current edition is the **제10회**, applied to new business from April
2024. **It is not published.** What 보험개발원 releases is the summary — 평균수명 남
86.3 / 여 90.7 and 65세 기대여명 남 23.7 / 여 27.1 — and not the rates [REG-R33]
[REG-R34]; and even those four numbers reach this library through a **trade newspaper**,
the 보험개발원 announcement itself not being retrievable, so the tilt target of step 2
below is second-hand. The 참조순보험요율 behind each carrier's own basis is not public either
[REG-R4] [R19] [R20]. This is the sharpest contrast in this repository with ``jplib``,
whose 標準生命表2018 is a free public PDF with ``qx`` by single year of age.

What *is* public is (i) the carriers' **예정 경험사망률** disclosures, which the
상품요약서 must print at ages 20, 40 and 60, and (ii) the 국가데이터처 완전생명표 summary
[REG-R38]. ``mort_table.csv`` is built from both and is **[std]** throughout:

1. A **Makeham law** ``q(x) = A + B c^x`` is fitted *exactly* to the anchor carrier's
   three disclosed rates per sex — male 0.000280 / 0.000650 / 0.003390 and female
   0.000200 / 0.000430 / 0.001390 at ages 20 / 40 / 60 [S12]. Three anchors, three
   parameters, so the fit is an interpolation and not a regression, and the shipped rows
   at those three ages are the disclosed rates to the digit.
2. Above age 60 the fitted law is tilted by ``k^(x - 60)``, one free parameter per sex,
   solved so that the **complete expectation of life at 65 on the shipped table is
   exactly the published 경험생명표 figure** — 23.7 years male and 27.1 female [REG-R33].
   The solved tilts are k = 1.00989 (male) and k = 1.05928 (female), so the correction is
   small and upward: an unconstrained Makeham extrapolation of the three disclosed rates
   leaves slightly too much life at 65.
3. The resulting table sits **4.2 years (male) and 3.4 years (female) above** the public
   완전생명표's own 65세 기대여명 of 19.5 and 23.7 [REG-R38]. That gap is underwriting
   selection, and a constructed Korean table that does not reproduce it is not an
   insured-lives table. Reproducing it is the one external check available.

The rows run from age 19 — below the composite's 만19세 minimum issue age — to age 120,
the terminal age of the expectation calculation, so that step 2 can be checked from the
shipped file rather than taken on trust. Every row says in its ``provenance`` column
whether it is an anchor or a fitted value.

Two distinctions the file does not blur. The shipped ``mort_rate`` is a **pricing** rate:
it is a carrier's 예정 경험사망률, which carries a margin over experience that no public
document sizes, so :mod:`~.Term_KR_S.Projection` applies its own ``mort_be_factor`` to
reach a best-estimate basis. And ``mort_rate`` is the **표준체** rate; the rate-class
relativities live in ``rate_class_table.csv``.

``acc_mort_rate`` is the **예정 재해사망률**, the accidental-death rate, from a different
carrier [S6]. Pairing the two is defensible in a way that pairing two all-cause tables
would not be: the two carriers that publish accidental rates agree to three significant
figures at age 20 and to within 10% everywhere [S6] [S10], which is strong evidence that
both take the 보험개발원 참조 재해사망률 almost unadjusted, where the all-cause rates are
heavily adjusted and differ by a factor of 1.77 at male 40. It is used only to split the
existing death decrement for the 재해사망 uplift variant, never as a decrement of its
own.

.. rubric:: The premium table is mostly sourced

``prem_rate_table.csv`` is the one assumption file whose values are largely **not**
standardizations, and this is the respect in which Korea is better documented than any
other market in this repository. The 생명보험협회 공시실 publishes a statutory
상품비교공시 pricing 45 정기보험 products on one prescribed 대표계약 basis [S4] [S5], and
each product's 상품요약서 prints its own premium grid. Twenty cells are shipped: six
순수보장형 20-year cells and six 만기환급형 20-year cells from the anchor carrier [S12],
and eight 10-year cells that are the 갱신형 ladder of the one carrier that publishes a
mandatory 예상 갱신보험료 예시 [S6] [S7]. All are monthly premiums per 100,000,000 won of
cover on a 표준체 basis. One asymmetry inside those eight: 흥국생명 does not sell its
1형(기본형) to women, so the four female rows are on 2형(보장추가형) and carry a 재해사망
보험금 the male rows do not [S4] [S6]. They are shipped for completeness, the row
provenance says so, and no shipped model point reads one.

The ``is_anchor`` rows — male and female age 40, 20-year term, one per maturity form —
are where :mod:`~.Term_KR_S.Projection` extends the scale to unpublished cells, by the
ratio of mean table mortality over the term. The male 순수보장형 anchor is the cell that
is simultaneously the 감독규정 기준연령 요건 [REG-R9] and the disclosure's 대표계약 [S5],
and its 15,080 won appears independently in the carrier's own grid and in the
cross-carrier disclosure, agreeing to the won [S12] [S4].

The 10-year rows and the 20-year rows come from **different carriers**, and the model
never mixes them: the shipped 갱신형 model points reach published cells only, and the
extension for an unpublished cell runs off the 20-year anchor. That the two carriers are
at the same level is checkable — on the disclosure basis the 흥국생명 비갱신형 20-year
premium is 15,000 won against the anchor's 15,080 [S4] — which is why the composite can
carry both.

.. rubric:: The lapse file holds three endpoints, not a curve

``lapse_table.csv`` is three rows because the Korean lapse basis is disclosed as three
numbers and a prescribed shape, not as a table. The 적용해지율 (*jeogyong haejiyul*, the
pricing lapse rate) is published in the 상품요약서 wherever a 무해지 form is sold —
「납입기간 이내에 대하여 경과기간별로 연 0.1%~4.6%, 납입기간 이후에 대하여 경과기간별로
연 0.7%~1.6%」 at the anchor carrier [S12], 「연 0.1%~8.4%, 납입기간 이후 연 0.8%」 at
another [S1] — and the **shape** between those endpoints is supervisory rather than
chosen: the 2024 IFRS17 계리가정 가이드라인 makes a 로그-선형 model converging to 0.1%
the 원칙모형 for 무·저해지 business and sets a post-완납 ultimate of 0.8% [REG-R27]. The
chain from supervisory guideline to disclosed pricing parameter runs end to end, which is
unique in this repository, so the file ships the endpoints and ``Projection.lapse_rate``
interpolates the prescribed shape between them.  One qualification travels with it: the
guideline's values are verified from the 보도자료 and its 별첨 was never converted from
HWP, so the functional form is **[unverified]** at instrument level [REG-R27].

To swap in a company basis, replace a CSV with a same-schema file, or point its ``*_file``
Reference at a different name, and clear the cache. No formula changes.
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

    Indexed by ``point_id``; ``point_id = 1`` is the anchor cell of the technical notes'
    worked example — male, 보험나이 40, 20년만기 전기납, 1억원, 표준체, 순수보장형
    해약환급금 미지급형 — which is both the 감독규정 기준연령 요건 [REG-R9] and the
    disclosure's 대표계약 [S5].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The **표준체 pricing** mortality rates by sex and age, from *mort_table.csv*.

    ``mort_rate`` is a **[std]** construction of the 예정 경험사망률 basis: a Makeham law
    fitted exactly to one carrier's three disclosed rates [S12] and tilted above age 60
    so that the table reproduces the 제10회 경험생명표's published 65세 기대여명 exactly
    [REG-R33].  The industry table itself is not published [REG-R34].  These are pricing
    rates carrying a margin over experience, which ``Projection.mort_be_factor`` removes,
    and 표준체 rates, which ``rate_class_table`` scales.

    ``acc_mort_rate`` is the 예정 재해사망률 [S6], used only to split the death decrement
    for the 재해사망 uplift variant.  See the Space docstring for why the two columns may
    come from different carriers.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def rate_class_table():
    """The rate-class relativities by class and sex, from *rate_class_table.csv*.

    Both columns are computed from one carrier's disclosures at age 40 [S12].
    ``mort_ratio`` is the ratio of the class's 예정 경험사망률 to the 표준체 rate;
    ``prem_ratio`` the same ratio taken on the published premium grid.  They differ, and
    not always in the same direction: 0.583 against 0.586 at male 40, where the premium
    ratio sits above the mortality one as a loading that does not scale with the risk
    implies, but 0.856 against 0.846 at female 40, where it sits **below**.  Nothing
    retrieved explains the reversal, so both columns are shipped and neither is derived
    from the other.

    Korea is the only market in this repository that publishes the mortality behind its
    preferred classes, so these are sourced ratios rather than a standardization.  Held
    flat across ages **[std]**: the disclosures are at three ages and the ratios move
    little between them.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_class_file,                               # noqa: F821
        index_col=["rate_class", "sex"])


def prem_rate_table():
    """The published premium cells, read from *prem_rate_table.csv*.

    Indexed by ``(form, sex, issue_age, term_y)``.  ``prem_mth_per_100m`` is the monthly
    office premium per 100,000,000 won of cover on a 표준체 basis; ``is_anchor`` marks the
    one row per form and sex from which ``Projection.prem_rate_mth`` extends the scale
    to unpublished cells.  Twelve rows are the anchor carrier's 20-year grid [S12] and
    eight are the 갱신형 ladder of the carrier that publishes an 예상 갱신보험료 예시
    [S6] [S7].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / prem_rate_file,                                # noqa: F821
        index_col=["form", "sex", "issue_age", "term_y"])


def prem_anchor_table():
    """The ``is_anchor`` rows of :func:`prem_rate_table`, indexed by form and sex.

    Derived from the table already in memory rather than read from a file of its own, so
    it costs no extra read.  Each anchor is the age-40 20-year cell of its maturity form,
    which for the 순수보장형 is the doubly prescribed cell [REG-R9] [S5].
    """
    tbl = prem_rate_table().reset_index()
    return tbl[tbl["is_anchor"] == 1].set_index(["form", "sex"])


def lapse_table():
    """The three disclosed 적용해지율 endpoints, read from *lapse_table.csv*.

    Indexed by ``segment``: ``in_payment_start`` (4.6% in the first policy year, ``t = 0``),
    ``in_payment_end`` (0.1% at 납입완료) and ``post_payment`` (0.8% thereafter).  The
    endpoints are disclosed [S12] [S1] and the log-linear shape between them is
    prescribed [REG-R27]; ``Projection.lapse_rate`` builds the curve.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="segment")         # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

rate_class_file = "rate_class_table.csv"

prem_rate_file = "prem_rate_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")
