# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean critical illness assurance (CI보험).

:mod:`~.CI_KR_S` is the executable counterpart of
``products/ci_insurance/technical-notes.md`` in the lifelib-products library. It projects
gross liability cash flows for a single-policy model point of the standardized composite
CI보험 (*CI boheom*, critical illness insurance), also sold as 중대질병보험 — a level
premium 종신보험 carrying an **acceleration clause**, under which a contractually defined
중대한 질병 pays a stated fraction of the death benefit early and the contract continues
on the balance.

**What this model exists to demonstrate is the acceleration.** One decrement produces
**two payments at two dates on one sum assured**: the 선지급 (*seonjigeup*, advance
payment) of ``accel_rate`` times the 기본보험금 at the CI date, and the residual death
benefit ``1 - accel_rate`` times the same base whenever death follows. Between them the
contract is still in force with no premium, a surrender value that has jumped to its
unsuppressed level and a reserve that has to carry the residual, so the projection runs
**two cohorts** — pre-CI and post-CI — and the post-CI one is indexed by the **month** it
accelerated in, because the residual it carries was fixed at that date and 「지급사유 발생
당시」 is a date rather than a policy year.

It states its deltas against the whole life chassis (종신보험) and does not restate it.
The 계약자적립액 recursion, the 해약환급금 built from it net of a 해약공제액 capped by the
표준해약공제액, the 저해지환급형 suppression and its step at 납입완료, the 보험계약대출 and
the 납입면제 are the chassis's and are implemented here on the chassis's terms. What is
new is the acceleration, the residual with its 105%-of-account floor, the release of the
suppression by a CI event as well as by 납입완료, and a morbidity decrement that is
several times the mortality one.

**Spaces.** The model contains two:

:mod:`~.CI_KR_S.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.CI_KR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor cell.
    It reaches the input tables through its ``data`` Reference, which resolves to the
    single :mod:`~.CI_KR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** **Monthly** steps, on 보험나이 (*boheom nai*, insurance age). The
time index ``t`` is
**0-based and counts months**: ``t = 0`` is the first policy month, month ``t`` runs from
time ``t`` to time ``t + 1``, the attained age is ``age_at_entry() + t // 12`` — 보험나이
increments on the 계약해당일, so the floor division is exact — the contractual policy year
label is ``t // 12 + 1``, and ``proj_len()`` is the **number of months**, twelve times
``proj_years()``, so the frame is
``range(proj_len())`` and ``result_cf()`` carries ``proj_len()`` rows indexed
``0 … proj_len() - 1``. The contract's *state* — the 계약자적립액, the 해약공제액, the
해약환급금, the 기본보험금, the 보험계약대출 limit — is carried on a second, **month-end**
index running ``0 … proj_len()`` with 0 at issue, which does not move with the frame; month
``t`` opens at month-end ``t`` and closes at month-end ``t + 1``, and a 계약해당일 is the
month-end ``12 y``.

**Annual assumptions stay annual.** Every rate the sources tabulate — the 적용위험률, the
CI incidence, the 해지율, the 납입면제 incidence — holds the annual figure of the policy
year the month falls in, and its ``_mth`` companion applies ``1 - (1 - q)^(1/12)`` so that
twelve months compound back to exactly that figure. Contractual terms quoted in policy
years — the 납입기간, the 해약공제기간, the CI cover period to the 100세 계약해당일, the
first-year 감액 — are unchanged and multiplied out into months where the grid needs them.
The two exceptions are named: the table's terminal age, where ``q = 1`` admits no twelfth
root and the certain death is spread uniformly over the year; and the **90-day
보장개시일**, which is a date and now falls where the contract puts it rather than being
smeared across the whole first year.

Premium, maintenance expense
and renewal commission fall at the start of the month; acquisition expense and initial
commission at issue; the CI acceleration, death claims and claim expense at the end of
the month of the event; surrenders at the end of the month, after the CI transition and
after deaths. A life accelerating in month ``t`` joins the post-CI cohort at the
start of month ``t + 1``, so the two payments are at least one step apart — a **month**
where the annual grid made it a year, which is the single largest number the conversion
moves on this product. That cohort is labelled by the month-end its acceleration was paid
at, ``t + 1``; the first policy year's reduced 감액 cohorts take the negative labels
``-(t + 1)``, one for each of the twelve months.

**What is sourced and what is not.** The contractual mechanics are sourced: the
acceleration and its exact complement, the once-only rule across the whole trigger set,
the 105% 계약자적립금 floor under the residual, the 90-day 중대한 암 보장개시일 and the
absence of a waiting period on everything else, the first-year halving for breast
cancer, the premium waiver on any CI/LTC 지급사유, the release of the 저해지 suppression
by that same event, the CI cover ending at the 100세 계약해당일 while death cover runs
종신, and the statutory 표준해약공제액 that caps the surrender charge. The quantitative
basis is not, and in Korea it structurally cannot be: the 산출방법서 is filed and never
published, 경험생명표 is released only as summary statistics, and there is exactly one
disclosed Korean CI morbidity table in public — a 2011 상품요약서 giving six rates at
three ages. **This model is a mechanics demonstration, not a pricing or reserving
result.** Replace the assumption tables with company data before drawing any conclusion
from the output.

**Mortality and morbidity.** ``mort_table.csv`` and ``ci_incidence_table.csv`` are
**[std]** constructions anchored on that one disclosed grid, with every row tagged in its
``provenance`` column. The three headline rates — 중대한 암, 중대한 급성심근경색증,
중대한 뇌졸중 — carry the source tag at ages 20, 40 and 60 and are interpolated and
extrapolated everywhere else; the remaining triggers and the 장기요양상태 limb are
standardizations throughout. See :mod:`~.CI_KR_S.Data` for what each row rests on.

**Model points.** Nine, covering both sexes, the 보험나이 15-60 issue-age envelope, the
₩10,000,000-₩200,000,000 sum-assured envelope, both acceleration fractions, all three
surrender-value forms, both first-year reduction scopes, both lapse bases, the policy
loan and the best-estimate levers. Model point 1 is the anchor cell of the worked example
in the technical notes.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/ci_insurance/CI_KR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "CI_KR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
