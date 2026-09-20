# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Pension_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 4            # or switch the default

``t`` counts **completed policy months since issue**, 0-based, matching the technical notes
and ``product-spec.md``. Premiums fall at ``t = 0 .. 12m - 1``; the 계약자적립액 accumulates
over ``t = 0 .. n`` where ``n = 12(m + d)``; the annuity is paid from ``t = n``; and
:func:`proj_len` is the **number of projected policy months**, twelve times
:func:`proj_years` and the exclusive end of the frame, so ``result_cf()`` runs
``t = 0 .. proj_len() - 1``. The contractual policy year is
the 1-based label ``t // 12 + 1``, and a 계약해당일 is a month-end ``12y``. ``pols_if(t)``
is the in-force count at the **start** of month ``t`` and is the weight on that same
``result_cf()`` row.

.. rubric:: Annual assumptions, a monthly grid

Every rate the sources publish is an **annual** figure and stays one — the 공시이율, the
최저보증이율 ladder, the 해지율 curve, the annuitant table, the expense inflation — and each
has a monthly companion that the roll-forward applies:
:func:`credit_rate_mth` is ``(1 + i_c)^(1/12) - 1`` and :func:`mort_rate_mth` and
:func:`lapse_rate_mth` are ``1 - (1 - q)^(1/12)``, so twelve months compound back to exactly
the tabulated annual rate. Contractual terms quoted in policy years — the 납입기간, the
거치기간, the 연금지급기간, the 보증지급기간, the 해약공제기간, the guarantee ladder, the
납입유예 — are unchanged and multiplied out by twelve where the grid needs them.

**On this product the monthly grid removes an approximation rather than adding one.** The
real contract credits interest 「납입일부터 일자계산을 하여」, from the date each instalment
is received, and the annual-step model this replaced had to collapse the twelve instalments
of a policy year into one start-of-year payment discounted by a ``prem_timing_factor`` worth
about 0.9903 of them. That cells is gone: each instalment is now credited in the month it
arrives and bears its own 계약체결비용 and 계약관리비용 there, which is the 약관's own
arithmetic. The two agree — the fund at the 연금개시일 reproduces the annual-step model's to
fourteen significant figures, which is what the timing factor was constructed to achieve —
so the gain is in the statement rather than in the number.

.. rubric:: The age basis

Every age in this model is **보험나이** (*boheom nai*, insurance age): the insured's exact
age at the 계약일 with a remainder under six months discarded and a remainder of six months
or more rounded up to a year, increasing on each policy anniversary, per 표준약관 제21조.
It is the contractual age, the age the rate basis is graduated on, and the age
``model_point_table.csv``'s ``issue_age`` and ``annuity_start_age`` are stated in.

Korea's other age convention, **만나이** (age last birthday), is not used here for any
contractual quantity, and the difference is not cosmetic: one retrieved 약관 states the
split in terms — 「이 약관에서의 피보험자의 나이는 보험나이를 기준으로 합니다. 다만,
연금개시나이가 만 55세 이상에 해당되는지 여부의 판단은 실제 만 나이를 적용합니다」. The
two statutory tests that are on 만나이 — the 만 55세 minimum for 연금수령 and the
withholding age bands — are read off :func:`age` in this model, which is a **[std]**
simplification: 보험나이 and 만나이 differ by at most one year, and at the anchor cell both
clear 만 55세 by a decade. A model point whose 연금개시나이 sits **on** 55 is the case where
the simplification could bite, and model point 6 is that case.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/pension_savings/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Pension_KR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Pension_KR_S.Data`, reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
mort_anchor_file        data.mort_anchor_table()            mort_anchor_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
decl_rate_file          data.decl_rate_table()              decl_rate_table.csv
guar_rate_file          data.guar_rate_table()              guar_rate_table.csv
pricing_table_file      data.pricing_table()                pricing_table.csv
expense_table_file      data.expense_table()                expense_table.csv
tax_table_file          data.tax_table()                    tax_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib wherever it has an analogue — ``pols_*`` for policy counts,
plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claims(t, kind)`` with an uppercase ``kind`` string, ``pols_if_at(t, timing)`` and
``av_pp_at(t, timing)`` for the within-year reads. The technical notes use compact
actuarial symbols instead. The mapping is:

=================  ============================  =====================================
Notes symbol       Cells                         Meaning
=================  ============================  =====================================
(model point row)  model_point()                 The selected model point
x                  issue_age()                   가입나이 (보험나이) at issue
x + t//12          age(t)                        Attained 보험나이 in month t
(none)             policy_year(t)                1-based policy year label of month t
(none)             sex()                         Rating factor on the annuitant table
m                  premium_term_y()              납입기간 in years
h                  holiday_years()               납입유예 length, module
12(m + h)          prem_end_t()                  Month the premium term ends
d                  defer_gap_y()                 Gap between 납입완료 and 연금개시
n = 12(m + h + d)  annuitisation_t()             Month of the 연금개시일
Y                  annuity_start_age()           Elected 연금개시나이
x + n              annuity_age_eff()             보험나이 at the actual 연금개시일
k                  payout_term_y()               확정기간연금형 term in years
g                  guar_term_y()                 보증지급기간 of the 종신연금형
proj_years         proj_years()                  Number of projected policy years
proj_len           proj_len()                    Number of projected policy months
P                  prem_pp()                     Annual 기본보험료
P^m                prem_mth_pp()                 The monthly instalment, P / 12
P_a                addl_prem_pp()                Annual 추가납입보험료, module
P_a^m              addl_prem_mth_pp()            Its monthly instalment
alpha(t)           acq_charge_rate(t)            계약체결비용 rate on the premium
beta(t)            maint_charge_rate(t)          계약관리비용 rate on the premium
i(t)               decl_rate(t)                  공시이율, the declared rate
i_min(t)           min_guar_rate(t)              최저보증이율, the guaranteed floor
i_c(t)             credit_rate(t)                Annual rate credited, max of the two
j_c(t)             credit_rate_mth(t)            Its monthly equivalent, what the fund uses
i'                 prem_int_rate()               예정이율, a pricing rate, not a guarantee
NP(t)              prem_to_av_pp(t)              Premium credited to the fund
C(t)               charge_from_av_pp(t)          Charge taken from the fund, not a premium
AV(t)              av_pp(t)                      계약자적립액 at the start of month t
(within month)     av_pp_at(t, timing)           BEF_PREM / AFT_PREM / AFT_INT
SC(t)              surr_chg_pp(t)                해약공제액 at time t
SC_max             surr_chg_cap_pp()             표준해약공제액, the statutory cap
CV(t)              cv_pp(t)                      해약환급금 at time t
(net of loans)     cv_pp_net(t)                  해약환급금 less any 보험계약대출
DB(t)              db_pp(t)                      Death benefit: the fund, and nothing more
(net of loans)     db_pp_net(t)                  Death benefit less any 보험계약대출
G                  min_fund_pp()                 100.1% of premiums paid, the fund floor
sum P              cum_prem_pp(t)                Cumulative premiums paid to time t
F = AV(n)          annuity_fund_pp()             연금개시시점 계약자적립액, after the floor
(net)              annuity_fund_net_pp()         F plus dividend less loan
adue               annuity_due_factor()          The factor the annuity is bought at
adue(k)            annuity_due_certain_factor()  확정기간연금형 factor, 공시이율 only
adue_life          annuity_due_factor_on(table)  종신연금형 factor on a stated vintage
B                  annuity_amount_pp()           연금연액, struck once at t = n
B x 1{in payment}  annuity_pp(t)                 Instalment payable at the start of t
(dividend)         div_credit_pp(t)              계약자배당 declared in year t
(dividend)         div_acc_pp(t)                 Accumulated 계약자배당 at time t
(loan)             loan_pp(t)                    보험계약대출 balance per policy
q(x+t//12)         mort_rate(t)                  Annual best-estimate death rate
q^m(t)             mort_rate_mth(t)              Its monthly conversion, what is applied
(table)            mort_rate_base(t)             Table rate before the [std] factor
q(x) by age        mort_rate_at_age(table, x)    Table lookup keyed by attained age
(1.15)             mort_be_factor()              Best-estimate uplift on a loaded table
w(t)               lapse_rate(t)                 Annual 해지 rate of the policy year
w^m(t)             lapse_rate_mth(t)             Its monthly conversion, what is applied
l(t)               pols_if(t)                    Contracts with an obligation open
l(t)(1-q), l(t+1)  pols_if_at(t, timing)         BEF_DECR / BEF_LAPSE / AFT_DECR
L(t)               lives_if(t)                   Probability the annuitant is alive
D(t)               pols_death(t)                 Expected deaths in month t
W(t)               pols_lapse(t)                 Expected surrenders at the end of month t
(none)             pols_maturity(t)              Contracts whose last instalment is paid
P x l(t)           premiums(t)                   Premium income
DB, CV, B          claims(t, kind)               Benefit outgo by kind
ec x D(t)          claim_expenses(t)             Claim expense, its own column
E0, e(t)           expenses(t)                   Acquisition + maintenance cash expense
(none)             inflation_factor(t)           Expense inflation factor
c0, c_r            commissions(t)                Commission outgo, nil on this composite
(loan advance)     policy_loans(t)               보험계약대출 advanced, an outflow
CF(t)              net_cf(t)                     Net cash flow, income positive
(tax)              tax_credit_pp(t)              세액공제 the saver receives, not a cash flow
(tax)              surr_tax_pp(t)                16.5% 기타소득세 on a surrender at t
(tax)              annuity_tax_pp(t)             연금소득세 withheld on the instalment
(tax)              annuity_limit_pp(t)           연금수령한도, an annual figure
=================  ============================  =====================================

.. rubric:: Three names needed care

``decl_rate`` and ``credit_rate`` are not the same rate. ``decl_rate`` is the 공시이율,
the carrier's declared rate; ``credit_rate`` is what the fund is actually credited with,
the greater of the declared rate and the 최저보증이율 ladder. The floor is a guarantee on
the **credited rate**, not on the return: expenses are still deducted beneath it, which is
why :func:`charge_from_av_pp` does not consult it.

``av_pp`` and ``cv_pp`` are the 계약자적립액 and the 해약환급금, and on this composite they
are the **same number**, because the published 해약공제액 schedule the composite adopts is
zero at every duration. That is a property of the adopted schedule, not of the product: a
model point carrying the postal insurer's front-end 해지공제액 separates the two, and
:func:`check_cv_floor` asserts the regulatory identity that relates them either way.

``prem_int_rate`` is the 예정이율 (2.50%), the rate the charge and benefit structure was
priced on. It is **not** a crediting rate and **not** a guarantee — every carrier document
that discloses it says so in terms — and it appears nowhere in the fund recursion. The
retired-name register keeps it apart from ``decl_rate`` for exactly that reason.

.. rubric:: The fund is an account, and there is no mortality in it

The 계약자적립액 is a contractual balance, not a net-level-premium reserve. Charges come
off the premium, the remainder is credited at :func:`credit_rate`, and nothing else moves —
there is no survivorship release, because the death benefit **is** the fund and the insurer
carries no deferral-phase mortality risk at all. A projection that applied a
decrement-weighted death strain here would be projecting a strain of exactly zero.

Mortality enters this product in one place: :func:`annuity_due_factor_on`, the annuity
factor struck at the 연금개시일 on the annuitant basis. The same table is used as the
in-force decrement, because the *number* of policies reaching annuitisation is still needed
for the charge income and the expense; and the best-estimate uplift :func:`mort_be_factor`
is greater than 1, because the published 연금사망률 is loaded on the survival side.

.. rubric:: The monthly grid and the monthly contract

Every retrieved contract is 월납, interest accrues 「납입일부터 일자계산을 하여」, and the
annuity is paid 매월. This model steps monthly, so all three are modelled where they fall
and the annualised-premium permission of 감독규정 제7-65조제2항 is not needed:

* each instalment is credited to the 계약자적립액 in the month it arrives, at
  :func:`credit_rate_mth`, bearing its own 계약체결비용 and 계약관리비용 there;
* the annuity is paid as :func:`annuity_amount_pp` divided by twelve, in each month of the
  payout phase;
* the 연금개시일 factor is unchanged and stays annual, because it is a **pricing** quantity
  struck once: :func:`annuity_due_certain_factor` is the annuity-due payable **monthly**,
  ``(1 - v**k) / d**(12)``, and :func:`annuity_due_factor_on` subtracts the standard
  ``(f - 1) / (2f)`` correction from the annual life factor.

That last adjustment is what makes the payout formula reconstruct the published
illustration. On the anchor cell's model point the composite's factor reproduces all six
published 확정기간연금형 implied factors — 9.06 / 12.92 / 16.39 at 2.15% and
9.81 / 14.53 / 19.13 at the guaranteed rate — to three or four significant figures, and the
종신연금형 factor of 23.70 to four, at 23.7004. An annual-payment reading of the same formula
misses every one of them by about half a per cent in the wrong direction.

.. rubric:: Modules that are off in the base run

Seven of the notes' optional constructions are implemented and switched off at the anchor
cell, so the base run reproduces the worked example while the machinery stays visible and
testable. Each is a model point column, so a non-anchor point exercises it:

- **확정기간연금형**, ``payout_form = "certain"``: instalments unconditional over ``k``
  years, priced on the declared rate alone with no mortality. Model points 4, 5 and 6, at
  20, 10 and 15 years.
- **The annuitant-mortality vintage**, ``mort_vintage``: ``issue`` strikes the factor on the
  가입시점 table, which is the composite's reading of the ratchet clause; ``commencement``
  strikes it on the 연금개시시점 table; ``ratchet`` implements the clause itself, taking
  whichever vintage gives the **larger** annuity. Because successive 경험생명표 revisions
  have lightened mortality, the ratchet is **out of the money** in the base run and the
  annuitant keeps the issue-date factor. Model points 7 and 9.
- **The 100.1% minimum fund**, ``min_fund_on``: withdrawn where a payment holiday or a
  one-instalment reinstatement caused the shortfall, in which case the contract defers the
  annuity date instead. Model point 9 carries it withdrawn.
- **연금저축추가납입특약**, ``addl_prem_pp``: an additional premium bearing 계약관리비용
  only and not 계약체결비용, capped at 200% of the year's basic premiums and inside the
  ₩18,000,000 aggregate. Model point 8.
- **The front-end 해지공제액**, ``surr_chg_rate``: the postal insurer's schedule, 8.67% of
  the annual premium at year 1 running off to zero at year 5, against the composite's nil
  charge. Model point 8. :func:`check_surr_chg_cap` holds it inside 별표 14's
  표준해약공제액 on both.
- **납입유예**, ``holiday_years``: premiums suspended for ``h`` years from a **[std]**
  start year, the charges still taken from the fund, and both the premium due dates and the
  annuity date deferred by ``h``. Model point 9.
- **보험계약대출**, ``loan_on``: half the 해약환급금 drawn at policy year 15 **[std]**,
  compounding at a **[std]** 4.00% because no retrieved document gives a rate for this
  product, capped at the 해약환급금 and deducted from the death benefit, the surrender
  payment and the 연금개시 fund. Model point 9.
- **계약자배당**, ``par`` and ``div_rate``: zero declared in the base run, machinery
  retained. A declared rate credits :func:`div_credit_pp` on the fund each year, accumulates
  it at the 공시이율, and applies it at ``t = n`` as an 증액연금. ``par`` also moves 별표 14's
  coefficient from 3% to 4%. Model point 9.

**부활 and 간편부활 are not implemented [std scope].** On an annual grid a premium unpaid at
``t`` terminates the contract at ``t``: there is no partial-year 납입최고 state and no
reinstatement re-entry, so :func:`lapse_rate` here is a **net-of-부활** rate by construction
and a user substituting a gross experience rate will over-decrement. 계약이전, 의료비인출,
the six 부득이한 사유 withdrawals and 배우자 승계 are likewise out of scope: each is a real
contract term with a real tax effect, and no public frequency exists for any of them.

.. rubric:: Sign convention

:func:`net_cf` is **income positive**, which is the library-wide sign, and the technical
notes print the stream the same way round, so there is no ``liability_cf`` companion to
publish here — that absence is a fact about which orientation the notes chose, not an
omission. The shape to expect is a positive year 0, twenty-odd years of thin positive
margin as surrender outgo grows against a level premium base, and then pure outgo once the
annuity is in payment.

.. rubric:: The absences are product facts

There is no death cover above the fund, so no sum assured and no mortality strain in
deferral. There is no premium waiver: one carrier states 「보험료 납입면제 사유 : 없음」 and
no retrieved 약관 carries one. There is no maturity benefit and no maturity date, because
the contract does not mature — it annuitises. And there is no commission, because the
composite follows a direct-channel product whose published 모집수수료율 is 0.00% in every
year; :func:`commissions` is retained and returns zero, so the column states the fact
rather than hiding it.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
# --- Model point attributes ------------------------------------------------

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def sex():
    """The insured's sex, ``M`` or ``F``; a rating factor on the annuitant table.

    It is a rating factor on the **annuity** and on nothing else: the deferral phase of this
    contract carries no mortality risk, so sex changes the factor struck at the 연금개시일
    and the speed at which the in-force runs off, and no benefit amount anywhere.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the 가입나이 at issue, on **보험나이** (insurance age) [S6 제20조] [REG-R25 제21조].

    The observed envelope is 0 to (연금개시나이 - 납입기간) at most carriers and 만19세 at
    one; the shipped model points run from 25 to 50.
    """
    return int(model_point()["issue_age"])


def premium_term_y():
    """m: the 납입기간 in years, before any 납입유예.

    Menus of 5 / 10 / 15 / 20년 / 전기납 are observed; at least five years is what clears the
    statutory account-age limb of the 연금수령 test, 소득세법 시행령 제40조의2제3항제2호.
    """
    v = int(model_point()["premium_term_y"])
    if v < 5:
        raise ValueError("premium_term_y below the five-year statutory minimum")
    return v


def defer_gap_y():
    """d: the gap in years between 납입완료 and the 연금개시일.

    Zero is a valid model point and a different contract shape: the five-year gap of the
    composite is a real contractual state in which premiums have stopped, the maintenance
    charge has not, and the fund is still accumulating.
    """
    return int(model_point()["defer_gap_y"])


def annuity_start_age():
    """Y: the elected 연금개시나이, in 보험나이; 만 55 to 80 on every retrieved contract.

    Derived rather than free: it must equal ``x + m + d``, and the model rejects a model
    point where it does not, because two spellings of one date is how a projection silently
    annuitises on the wrong year.  A 납입유예 defers the *actual* start date beyond it; see
    :func:`annuity_age_eff`.
    """
    v = int(model_point()["annuity_start_age"])
    if v != issue_age() + premium_term_y() + defer_gap_y():
        raise ValueError("annuity_start_age is not issue_age + m + d")
    if v < 55 or v > 80:
        raise ValueError("annuity_start_age outside the 55-80 statutory envelope")
    return v


def prem_pp():
    """P: the annual 기본보험료, level and guaranteed for the whole 납입기간.

    ₩6,000,000 at the anchor cell — ₩500,000 a month, which is exactly the ₩6,000,000
    세액공제 ceiling, so the anchor saver sits on the corner of the tax schedule.  There is
    no review right on this chassis, so every premium is inside the contract boundary.
    """
    return float(model_point()["premium_pp"])


def addl_prem_pp():
    """P_a: the annual 추가납입보험료 under the 연금저축추가납입특약; zero in the base run.

    Capped at 200% of the year's basic premiums and, with the basic premium, inside the
    ₩18,000,000 aggregate contribution ceiling.  It bears **계약관리비용 only** — the
    additional premium is not loaded for 계약체결비용 — which is why it is a model point
    field rather than an addition to :func:`prem_pp`: merging the two would misstate the
    expense recovery.
    """
    v = float(model_point()["addl_prem_pp"])
    if v > pricing_basis("addl_prem_cap_ratio") * prem_pp():
        raise ValueError("addl_prem_pp above the 200% cap")
    if v + prem_pp() > tax_basis("contribution_ceiling"):
        raise ValueError("contribution above the statutory annual ceiling")
    return v


def payout_form():
    """The annuity form elected at the 연금개시일: ``life_guar`` or ``certain``.

    ``life_guar`` is 종신연금형 (정액형) with a 보증지급기간, computed on the 연금사망률 and
    the 공시이율; ``certain`` is 확정기간연금형, computed on the 공시이율 **alone**, whose
    instalments are paid to the count whether or not the annuitant lives.  The composite
    takes the life form with a ten-year guarantee as the base, the only guarantee period
    every retrieved life carrier offers.
    """
    v = model_point()["payout_form"]
    if v not in ("life_guar", "certain"):
        raise ValueError("invalid payout_form")
    return v


def payout_term_y():
    """k: the 확정기간연금형 term in years; 10 / 15 / 20 on the composite's menu."""
    return int(model_point()["payout_term_y"])


def guar_term_y():
    """g: the 보증지급기간 of the 종신연금형, in years; 10 on the composite, 20 observed.

    Lengthening it is cheap and readable: 10 to 20 years costs about 1.8% of the annuity for
    a 65-year-old male on the published illustration.
    """
    return int(model_point()["guar_term_y"])


def mort_vintage():
    """Which vintage of the 연금사망률 the annuity factor is struck on.

    ``issue``
        the table filed in the 산출방법서 at 가입.  This is the composite's reading and the
        base run.

    ``commencement``
        the table in force at the 연금개시일.

    ``ratchet``
        the clause every retrieved 약관 actually carries — 「연금사망률의 개정 등에 따라
        연금연액이 증가하게 되는 경우 연금개시시점의 연금사망률 … 을 기준으로」 — which is a
        **one-way ratchet in the policyholder's favour**, so the model takes whichever
        vintage produces the larger annuity.

    The reading that the base factor is the 가입시점 one is ``[derived]``, not stated by any
    retrieved document; it follows from the ratchet being one-way and from the two carriers
    that publish the 연금사망률 doing so in the 상품요약서 handed over at inception.
    """
    v = model_point()["mort_vintage"]
    if v not in ("issue", "commencement", "ratchet"):
        raise ValueError("invalid mort_vintage")
    return v


def min_fund_on():
    """Whether the 100.1%-of-premiums minimum fund applies at the 연금개시일.

    On in the base run.  It is withdrawn — and the annuity date deferred instead — where a
    payment holiday or a one-instalment reinstatement caused the shortfall, which is why it
    is a flag rather than a constant.
    """
    return bool(model_point()["min_fund_on"])


def surr_chg_rate():
    """The first-year 해약공제액 as a fraction of the annual premium; nil on the composite.

    The composite adopts a published schedule with 「해약공제액 0.0%」 at every duration, so
    the surrender value is the fund.  The alternative — the state postal insurer's ₩104,000
    on a ₩1,200,000 annual premium, 8.67%, running off to zero over four years — is a model
    point value, not a rewrite.
    """
    return float(model_point()["surr_chg_rate"])


def holiday_years():
    """h: the length of the modelled 납입유예 in years; zero in the base run.

    Up to three spells of one year is what the retrieved contracts allow.  While it runs the
    premium stops, the charges are still taken from the fund, and both the premium due dates
    and the annuity date are deferred by ``h``.
    """
    v = int(model_point()["holiday_years"])
    if v > pricing_basis("holiday_max_years"):
        raise ValueError("holiday_years above the observed maximum")
    return v


def loan_on():
    """Whether the 보험계약대출 module is on; off in the base run.

    Off because **no retrieved document gives a numeric 보험계약대출이율 for a
    연금저축보험**, so a base-run rate would be invented.  Switching it on switches on a
    [std] rate, and the model says so.
    """
    return bool(model_point()["loan_on"])


def par():
    """Whether the contract is 배당 (participating); the composite is 무배당.

    It is not a cosmetic flag.  별표 14 주5 gives a participating 연금저축보험 a
    표준해약공제액 coefficient of 4% of the 연납순보험료 and a 무배당 one 3%, so a 무배당
    composite states the **tighter** constraint, and :func:`surr_chg_cap_pp` reads this.
    """
    return bool(model_point()["par"])


def div_rate():
    """The declared 계약자배당 rate on the fund; zero in the base run.

    No retrieved carrier publishes a dividend *rate* on a 연금저축보험.  Where a dividend
    arises it is applied as an 증액연금 at the 연금개시일 rather than paid in cash, which is
    what :func:`div_acc_pp` does.
    """
    v = float(model_point()["div_rate"])
    if v and not par():
        raise ValueError("a dividend declared on a 무배당 contract")
    return v


def lapse_basis():
    """Which 해지 vector applies: ``pension`` or the ``savings`` comparison vector.

    The product's own basis cannot be borrowed from a savings contract, because a surrender
    here costs **16.5% 기타소득세** on essentially the whole payout once the contributions
    have been credited, and part of what looks like termination on an insurer's book is
    계좌이체 to a 연금저축펀드 rather than a withdrawal.  The ``savings`` vector is carried
    so the two can be run side by side, not because it is this product's basis.
    """
    v = model_point()["lapse_basis"]
    if v not in ("pension", "savings"):
        raise ValueError("invalid lapse_basis")
    return v


def rate_scenario():
    """Which 공시이율 scenario applies: ``base``, ``floor`` or ``hybrid``.

    ``base`` is the composite's level 2.15%; ``floor`` drives the declared rate below the
    guarantee at every duration, which reproduces the second column of a published
    illustration; ``hybrid`` is the one retrieved design paying a fixed 3.5% for five years.
    """
    v = model_point()["rate_scenario"]
    if v not in ("base", "floor", "hybrid"):
        raise ValueError("invalid rate_scenario")
    return v


# --- Derived model point quantities ----------------------------------------

def prem_end_t():
    """n_prem: the **month** at which the premium term ends, ``12 (m + h)``.

    A 납입유예 does not shorten the premium term, it postpones it: the same ``12 m``
    instalments are paid, ``h`` years later.
    """
    return 12 * (premium_term_y() + holiday_years())


def annuitisation_t():
    """n = 12 (m + h + d): the **month** of the 연금개시일.

    The join between the two contracts this product really is.  Almost nothing survives it:
    surrender, transfer, policy loans, contributions and the annuity-form election all stop
    there.  It is read off :func:`annuity_start_age` rather than summed from ``m`` and ``d``
    directly — the same number, but it puts the model point's own consistency check on the
    path every projection takes.  The 연금개시일 is a 계약해당일 by construction, so ``n`` is
    a multiple of twelve.
    """
    return 12 * (annuity_start_age() - issue_age() + holiday_years())


def annuity_age_eff():
    """The 보험나이 at the 연금개시일 actually reached: ``x + n / 12``.

    Equal to :func:`annuity_start_age` in the base run and later than it by ``h`` where a
    payment holiday has deferred the date.
    """
    return issue_age() + annuitisation_t() // 12


def proj_years():
    """The **number** of projected policy years, the contract's own clock.

    ``m + h + d + k`` on the 확정기간연금형 form and ``ω - x + 1`` on the 종신연금형 one,
    where the horizon is the terminal age of the annuitant table.
    """
    if payout_form() == "certain":
        return annuitisation_t() // 12 + payout_term_y()
    return omega_age(mort_table_name()) - issue_age() + 1


def proj_len():
    """The **number** of projected policy months, the exclusive end of the frame.

    ``12 proj_years()``.  ``result_cf()`` runs ``t = 0 .. proj_len() - 1``: the frame is
    ``range(proj_len())`` and the last projected index is ``proj_len() - 1``, twelve rows to
    a policy year.

    ``n + 12k`` on the 확정기간연금형 form: the contract pays exactly ``12 k`` instalments, at
    ``t = n .. n + 12k - 1``, and ends with no tail states.  On the 종신연금형 form there is
    no natural end, so the horizon is the terminal age of the annuitant table less the issue
    age, plus one policy year — the last projected policy year is the last in which anyone
    can still be alive at the start.
    """
    return 12 * proj_years()


def policy_year(t):
    """The contractual, 1-based policy year label of month t: ``t // 12 + 1``.

    Derived and never indexed by.  Every contractual term on this product is quoted in
    policy years — the 납입기간, the 거치기간, the 연금지급기간, the 보증지급기간, the
    해약공제기간, the guarantee ladder and the 세액공제 cap — and every one of them is read
    through this or multiplied out by twelve.
    """
    return t // 12 + 1


def age(t):
    """The attained 보험나이 in month t: ``x + t // 12``.

    보험나이 increases on the 계약해당일, so the floor division is the contract's own rule
    rather than an approximation of it: one age holds for the twelve months of a policy year.
    """
    return issue_age() + t // 12


# --- Assumption basis ------------------------------------------------------

def pricing_basis(item):
    """One row of the pricing, charge and module basis table, as a float.

    A single lookup helper, so every basis item is read the same way and every one of them
    carries a ``provenance`` tag in the CSV rather than sitting as an untagged constant in a
    formula.
    """
    return float(data.pricing_table().loc[item, "value"])            # noqa: F821


def expense_basis(item):
    """One row of the best-estimate cash expense and commission table, as a float."""
    return float(data.expense_table().loc[item, "value"])            # noqa: F821


def tax_basis(item):
    """One row of the 연금저축 tax parameter table, as a float.

    Nothing read through here is an insurer cash flow.  The tax layer drives the behavioural
    assumptions on this product; it does not appear in :func:`net_cf`.
    """
    return float(data.tax_table().loc[item, "value"])                # noqa: F821


def prem_freq():
    """The number of premium instalments a year; 12 on every retrieved contract."""
    return int(pricing_basis("prem_freq"))


def annuity_freq():
    """The number of annuity instalments a year; 12 in the base run.

    매월 / 매3개월 / 매6개월 are all offered, with the deferred instalments credited at the
    공시이율.  The frequency is what makes the published annuity factors reconstruct: an
    annual-payment reading of the same formula misses every one of them.
    """
    return int(pricing_basis("annuity_freq"))


def prem_int_rate():
    """i': the 예정이율, 2.50% 연복리, used to price the charge and benefit structure.

    Disclosed by three carriers and by all three at the same level.  It is **not a
    guarantee** and **not a crediting rate** — 「동 이율은 적립액 및 해약환급금을 보증하는
    이율은 아닙니다」 — and it appears nowhere in the fund recursion.  It is published because
    a reader who finds a 2.50% in the basis needs to be told which rate it is.
    """
    return pricing_basis("prem_int_rate")


def avg_decl_rate():
    """The 평균공시이율, 2.50% for 2026; a supervisory average, not a crediting rate.

    Defined at 감독규정 제1-2조제13호 and computed by the supervisor.  It enters this product
    only as a constraint: the illustration rule, the 별표 14 주6 discount inside
    :func:`surr_chg_cap_pp`, and the 평균공시이율 + 1% ceiling on reinstatement interest.
    In 2026 it sits **above** the composite's own declared rate of 2.15%.
    """
    return pricing_basis("avg_decl_rate")


def decl_rate(t):
    """i(t): the **annual** 공시이율 (declared crediting rate) applying in month t.

    A step function of policy year read from the scenario the model point selects.  It is
    **not** a market rate and must not be modelled as one: 시행세칙 별표 27 builds it from an
    external index rate and the insurer's own 운용자산이익률 with the external weight capped
    at 60%, so a Korean declared rate is majority-weighted to realised investment return and
    moves in steps of two to seven basis points.  One carrier's published thirteen-month
    history falls 57 basis points over a year without once reversing.
    """
    tbl = data.decl_rate_table().loc[rate_scenario()]                # noqa: F821
    y = t // 12
    return float(tbl.loc[max(k for k in tbl.index if k <= y), "decl_rate"])


def min_guar_rate(t):
    """i_min(t): the **annual** 최저보증이율 applying in month t.

    1.25% to five years, 1.00% to ten, 0.50% after — the modal current ladder, stepping
    **down** with elapsed duration on every retrieved contract, so the guarantee is
    strongest exactly where the fund is smallest.  The ladder tracks the product's
    판매개시일 rather than the carrier: one carrier's shelf runs two ladders side by side.
    감독규정 제7-60조제10호 makes setting one compulsory on a 금리연동형보험.
    """
    tbl = data.guar_rate_table()                                     # noqa: F821
    y = t // 12
    return float(tbl.loc[max(k for k in tbl.index if k <= y), "min_guar_rate"])


def credit_rate(t):
    """i_c(t): the **annual** rate the 계약자적립액 is credited with in month t.

    ``max(decl_rate(t), min_guar_rate(t))``.  The floor is a guarantee on the **credited
    rate**, not on the return — 「공시이율이 0.1%로 낮아지더라도 적립금은 … 최저보증이율로
    적립됩니다」 — so the charges are still deducted beneath it, which is why
    :func:`charge_from_av_pp` does not consult it.

    It is the **annual** rate the sources publish; what the fund recursion applies is
    :func:`credit_rate_mth`.
    """
    return max(decl_rate(t), min_guar_rate(t))


def credit_rate_mth(t):
    """j_c(t): the monthly equivalent of the credited rate, ``(1 + i_c)^(1/12) - 1``.

    Twelve months compound back to exactly the declared annual rate, which is what a Korean
    illustration quotes and what 시행세칙 별표 27 constructs.

    **This is the cell the conversion exists for on this product.** The real contract credits
    interest 「납입일부터 일자계산을 하여」 — from the date each instalment is received — and
    the annual-step model this replaced could only approximate that with a
    ``prem_timing_factor`` collapsing twelve instalments to one start-of-year payment worth
    about 0.9903 of them.  On a monthly grid each instalment is credited in the month it
    arrives and the factor is not needed at all.
    """
    return (1.0 + credit_rate(t)) ** (1.0 / 12.0) - 1.0


def acq_charge_rate(t):
    """alpha(t): the 계약체결비용 rate on the instalment of month t.

    1.50% of the monthly 기본보험료 for the first seven policy years and nothing after.
    Seven years is also the 해약공제기간 cap of 감독규정 제7-66조제1항제2호, and the
    composite's whole acquisition cost — 1.50% x ₩500,000 x 84 = ₩630,000 — is recovered
    inside it, which is a coherent explanation of why the source product's published
    해약공제 table is all zeros.  **The 84 are months**, and on this grid they are 84 rows.
    """
    if t < 12 * pricing_basis("acq_charge_years"):
        return pricing_basis("acq_charge_rate")
    return 0.0


def maint_charge_rate(t):
    """beta(t): the 계약관리비용 rate in month t, on the monthly 기본보험료.

    3.00% a month while premiums are being paid and 0.67% a month after 납입완료 — 「보험료
    납입 완료 후에는 월계약해당일에 계약관리비용 중 유지관련비용(납입후)을 적립액에서
    차감합니다」.  **The maintenance charge does not stop at 납입완료**, and during the gap
    between 납입완료 and 연금개시 the fund is accumulating at the declared rate and paying a
    charge with no premium arriving.
    """
    if t < prem_end_t():
        return pricing_basis("maint_charge_rate")
    return pricing_basis("maint_charge_rate_paid_up")


def mort_table_name():
    """The annuitant table the annuity factor and the in-force decrement are read from.

    ``annuitant_issue`` or ``annuitant_revised`` per :func:`mort_vintage`.  Under
    ``ratchet`` the model evaluates both and takes the vintage giving the **smaller factor**,
    which is the larger annuity, because the contractual clause only bites where the revision
    *increases* the annuity.  Since revisions have lightened mortality — the 제10회 table
    raised 평균수명 by 2.8 years for men and cut the monthly annuity on a fixed fund by about
    15% — the ratchet is out of the money and the answer is the issue vintage.
    """
    v = mort_vintage()
    if v == "issue":
        return "annuitant_issue"
    if v == "commencement":
        return "annuitant_revised"
    if payout_form() != "life_guar":
        return "annuitant_issue"
    if annuity_due_factor_on("annuitant_issue") <= annuity_due_factor_on(
            "annuitant_revised"):
        return "annuitant_issue"
    return "annuitant_revised"


def omega_age(table):
    """The terminal age of a shipped annuitant table; 120 on both vintages.

    Read from ``data.mort_anchor_table()``.  It is a **[std]** choice, not a published fact:
    no Korean industry table publishes a terminal age, because no Korean industry table is
    published at all.  ``q`` is truncated to 1 there.
    """
    return int(data.mort_anchor_table().loc[                         # noqa: F821
        (table, sex(), "omega_age"), "value"])


def mort_anchor(table, item):
    """One parameter of a shipped table's [std] construction, as a float.

    ``law_a`` / ``law_b`` / ``law_c`` are the Makeham parameters, ``age_setback`` the female
    setback, ``improve_factor`` the scaling that makes the revised vintage, and the
    ``pub_q_*`` rows the published anchor rates the law was fitted to.
    """
    return float(data.mort_anchor_table().loc[                       # noqa: F821
        (table, sex(), item), "value"])


def mort_rate_law(table, x):
    """The rate the stated [std] construction produces at attained age x.

    ``round(round(1 - exp(-(A + B c**y)), 8) * kappa, 8)`` with ``y = max(0, x - setback)``
    and ``kappa`` the vintage's improvement factor.  This is what the shipped table was
    generated from, and :func:`check_mort_law` asserts that the two still agree — so the day
    someone replaces ``mort_table.csv`` with a real basis, the check reports it rather than
    the model silently claiming a construction it no longer has.
    """
    y = max(0.0, x - mort_anchor(table, "age_setback"))
    q = round(1.0 - math.exp(-(mort_anchor(table, "law_a")           # noqa: F821
                               + mort_anchor(table, "law_b")
                               * mort_anchor(table, "law_c") ** y)), 8)
    return round(q * mort_anchor(table, "improve_factor"), 8)


def mort_rate_at_age(table, x):
    """The shipped [std] rate of ``table`` at attained age ``x``, truncated to 1 at omega.

    The single point at which the model touches its mortality input, so a filed or company
    basis drops in by replacing ``mort_table.csv`` with a same-schema file.
    """
    if x >= omega_age(table):
        return 1.0
    return float(data.mort_table().loc[(table, sex(), x), "mort_rate"])  # noqa: F821


def mort_rate_base(t):
    """The **annual** table rate applying in month t, before the best-estimate factor."""
    return mort_rate_at_age(mort_table_name(), age(t))


def mort_be_factor():
    """The best-estimate uplift on the annuitant table; 1.15 **[std]**.

    Greater than one, and the direction is the point.  The published 연금사망률 is a
    **pricing** basis for a longevity product, so it is loaded on the survival side: the
    rates are far below any plausible Korean population level, and a best-estimate death
    decrement therefore runs heavier than the table, not lighter.  The size is a
    standardization: the only direct evidence of the margin is that the two carriers who
    publish annuitant rates differ by about 9% at age 60, and 1.15 sits a little above that.
    """
    return pricing_basis("mort_be_factor")


def mort_rate(t):
    """q(x + t//12): the **annual** best-estimate mortality rate of the policy year of t.

    The table rate times :func:`mort_be_factor`, capped at 1.  It moves **no benefit amount
    in the deferral phase**, where the death payment equals the surrender payment equals the
    fund; what it moves is the number of policies that reach the 연금개시일, and hence the
    charge income and the expense.  In the payout phase it runs the 종신연금형 off.
    This is the rate the table holds; what the roll-forward applies is
    :func:`mort_rate_mth`.
    """
    return min(1.0, mort_be_factor() * mort_rate_base(t))


def mort_rate_mth(t):
    """q^m(t): the death decrement applied in month t, ``1 - (1 - q)^(1/12)`` **[std]**.

    The uniform-force conversion, so that the twelve months of a policy year compound back
    to exactly the annual rate.  At the annuitant table's terminal age ``q = 1`` admits no
    twelfth root, and the certain death is spread uniformly over the year as
    ``1 / (12 - j)`` — the UDD convention, which closes the table exactly instead of
    emptying the cohort in one month and leaving eleven rows to print.
    """
    q = mort_rate(t)
    if q >= 1.0:
        return 1.0 / (12 - t % 12)
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def lapse_rate(t):
    """w(t): the **annual** 해지 rate of the policy year month t falls in.

    Read from the model point's basis: a duration curve while premiums are due, a single flat
    rate between 납입완료 and 연금개시, and **zero once the annuity is in payment**, where a
    종신연금형 may not be surrendered at all and a 확정기간연금형 pays its instalments to the
    count.

    The vector is **[std]** and had to be argued rather than fitted: there is no public
    Korean lapse statistic for 연금저축보험 by policy year — one carrier's own disclosure
    reads 「적용안함」 on every row of its 경과기간별 중도해지율 column.  It is deliberately
    flatter than a non-qualified savings vector, because a surrender costs 16.5% 기타소득세
    on essentially the whole payout, and because part of what an insurer counts as
    termination is 계좌이체 to a 연금저축펀드, which is not a withdrawal and is not taxed.
    It is **not** the supervisory 무·저해지 lapse guidance, which is calibrated to
    순수보장성 business and does not describe a contract with a full surrender value from
    the first month.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    if t >= annuitisation_t():
        return float(tbl.loc[(lapse_basis(), "in_payment", 0), "lapse_rate"])
    if t >= prem_end_t():
        return float(tbl.loc[(lapse_basis(), "paid_up", 0), "lapse_rate"])
    seg = tbl.loc[(lapse_basis(), "premium_paying")]
    y = t // 12
    return float(seg.loc[max(k for k in seg.index if k <= y), "lapse_rate"])


def lapse_rate_mth(t):
    """w^m(t): the surrender decrement applied in month t, ``1 - (1 - w)^(1/12)`` **[std]**.

    The file holds a curve by **policy year** — the unit every Korean 해지율 disclosure is
    written in — and this is its uniform-force conversion, so twelve months compound back to
    exactly the tabulated annual rate.  Dividing by twelve would not.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


# --- The 계약자적립액 recursion -------------------------------------------------

def on_holiday(t):
    """Whether the 납입유예 is running in policy year t; false in the base run.

    While it runs no premium arrives, the charges are still taken from the fund, and both
    the premium due dates and the annuity date have been deferred by ``h``.
    """
    if holiday_years() <= 0:
        return False
    start = 12 * int(pricing_basis("holiday_start_year"))
    return start <= t < start + 12 * holiday_years()


def prem_paying(t):
    """Whether a premium instalment is due in month t.

    ``t < n_prem`` and not inside the payment holiday, so the contract still collects exactly
    ``12 m`` instalments however long the holiday.
    """
    return t < prem_end_t() and not on_holiday(t)


def prem_mth_pp():
    """G^m: the 기본보험료 instalment, ``prem_pp() / 12``.

    The model point carries the **annual** contribution, because that is the unit the
    세액공제 cap, the 별표 14 arithmetic and every carrier disclosure are written in; the
    monthly grid collects one twelfth of it in each month it is due, which is what the
    contract does — 「보험료 납입주기」 is 월납 on every retrieved contract.
    """
    return prem_pp() / 12.0


def addl_prem_mth_pp():
    """The 추가납입보험료 instalment, ``addl_prem_pp() / 12``; zero in the base run."""
    return addl_prem_pp() / 12.0


def prem_to_av_pp(t):
    """NP(t): the 순보험료 credited to the fund in month t.

    The 기본보험료 less **both** published charges, plus any 추가납입보험료 less the lighter
    charge that one bears, credited in the month the instalment arrives.
    「「계약자적립액」이란 순보험료(기본보험료에서 계약체결비용
    및 계약관리비용을 뺀 금액)를 「공시이율」로 납입일부터 일자계산을 하여 적립한
    금액」 — the charges come off the **premium**, not off the fund, while premiums are being
    paid, which is what gives an insurance-wrapper pension its negative early-duration
    return.

    **The charges are percentages of the monthly 기본보험료 and are applied to it directly.**
    The annual-step model had to apply them to a notional annual premium and then discount
    the whole by a timing factor; here each instalment bears its own charge in the month it
    arrives, which is the 약관's own arithmetic.
    """
    if not prem_paying(t):
        return 0.0
    basic = prem_mth_pp() * (1.0 - acq_charge_rate(t) - maint_charge_rate(t))
    addl = addl_prem_mth_pp() * (1.0 - pricing_basis("addl_charge_rate"))
    return basic + addl


def charge_from_av_pp(t):
    """C(t): the charge taken from the fund in month t, where no premium bears it.

    Two cases, and both are sourced.  After 납입완료 the 계약관리비용 continues at 0.67% of
    the notional monthly 기본보험료 and is deducted from the 적립액.  During a 납입유예 the
    acquisition **and** management charges are both still deducted monthly from the fund, and
    the holiday ends prematurely if the fund cannot bear them.  Zero once the annuity is in
    payment, where the charge is the 0.5% of the 연금연액 already inside the annuity factor.
    """
    if t >= annuitisation_t():
        return 0.0
    if on_holiday(t):
        rate = acq_charge_rate(t) + pricing_basis("maint_charge_rate")
    elif t >= prem_end_t():
        rate = pricing_basis("maint_charge_rate_paid_up")
    else:
        return 0.0
    return prem_mth_pp() * rate


def av_pp(t):
    """AV(t): the 계약자적립액 per policy at the start of month t, before that month's premium.

    A plain account roll-forward, a month at a time::

        AV(0)   = 0
        AV(t+1) = ( AV(t) + NP(t) - C(t) ) ( 1 + j_c(t) )

    There is **no mortality in it**: the fund is a contractual balance and the death benefit
    is the fund itself, so there is no survivorship release to credit and no death strain to
    subtract.  Zero from ``t = n + 1``, where the fund has been converted into the annuity
    and the liability is the instalment stream instead.

    The accumulation cross-check against the published illustration closes: rolling a
    published year-20 surrender value forward the five years of the gap at the declared rate
    reproduces the published fund at annuitisation to within five years of the post-payment
    maintenance charge.
    """
    if t <= 0 or t > annuitisation_t():
        return 0.0
    return av_pp_at(t - 1, "AFT_INT")


def av_pp_at(t, timing):
    """The 계약자적립액 per policy at a point inside month t.

    ``"BEF_PREM"``
        AV(t), the start of the month before anything is credited; the same number
        as :func:`av_pp`.

    ``"AFT_PREM"``
        after the month's 순보험료 is credited and any charge on the fund is taken,
        before interest.

    ``"AFT_INT"``
        after the credited rate is applied; the same number as ``AV(t+1)``.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_pp(t) - charge_from_av_pp(t)
    if timing == "AFT_INT":
        return av_pp_at(t, "AFT_PREM") * (1.0 + credit_rate_mth(t))
    raise ValueError("invalid timing")


def cum_prem_pp(t):
    """The cumulative premiums paid per policy up to the start of month t.

    Basic and additional together, because 「이미 납입한 보험료」 in the minimum-fund clause
    is the whole contribution.  It is the base of the 100.1% floor and of the 환급률 a Korean
    illustration quotes.
    """
    if t <= 0:
        return 0.0
    paid = prem_mth_pp() + addl_prem_mth_pp() if prem_paying(t - 1) else 0.0
    return cum_prem_pp(t - 1) + paid


# --- Deferral-phase benefit amounts ----------------------------------------

def surr_chg_cap_pp():
    """SC_max: the 표준해약공제액 of 별표 14, the statutory cap on the surrender charge.

    ``coeff x (P - levelled loading) x min(m, 12)``, less 주6's deduction of the acquisition
    amount loaded into the premium discounted at the 평균공시이율.  주2 caps the 저축성보험
    coefficient at a twelve-year premium term; 주3 defines the 연납순보험료 as the annual
    premium less the average loading spread evenly over the payment term capped at ten years;
    주5 replaces the general 5% with **4% for a 연금저축보험 and 3% if 무배당**, and 주4's 6%
    concession for a whole-of-life survival annuity is expressly **denied** to this product.
    The second term of 별표 14's formula — 보장성보험의 보험가입금액의 10/1000 — is nil here,
    because the contract has no 보장성 element.

    On the anchor cell this is about ₩1,420,000, some 2.8 months of 기본보험료.  The
    composite uses none of it, and that is the point: the cap binds nothing on this product,
    it bounds the design space.  :func:`check_surr_chg_cap` asserts the bound on every model
    point, including the one carrying a real front-end charge.
    """
    m = premium_term_y()
    lvl_years = min(m, pricing_basis("surr_chg_cap_level_years"))
    loading = sum(prem_mth_pp() * (acq_charge_rate(s) + maint_charge_rate(s))
                  for s in range(12 * m))
    net_prem = prem_pp() - loading / lvl_years
    coeff = (pricing_basis("surr_chg_cap_rate_par") if par()
             else pricing_basis("surr_chg_cap_rate"))
    gross = coeff * net_prem * min(m, pricing_basis("surr_chg_cap_term_cap"))
    yrs = int(min(m, pricing_basis("acq_charge_years")))
    i = avg_decl_rate()
    acq = prem_pp() * pricing_basis("acq_charge_rate")
    deduct = sum(acq / (1.0 + i) ** s for s in range(yrs))
    return max(0.0, gross - deduct)


def surr_chg_pp(t):
    """SC(t): the 해약공제액 at time t; **zero at every duration** on the composite.

    Unamortised acquisition cost — 「공제하지 못한 계약체결비용을 한꺼번에 공제하게 되는데
    이를 해약공제액(미상각 신계약비)라 함」.  The composite adopts a published schedule that
    is zero everywhere, so the surrender value is the fund.  A non-zero
    :func:`surr_chg_rate` reproduces the postal insurer's shape instead: the first-year
    amount running off linearly to zero at the fifth policy year — **a month at a time on
    this grid**, so the deduction is the balance outstanding in the month a surrender is
    actually taken rather than the balance at the last 계약해당일 before it.  Held inside
    :func:`surr_chg_cap_pp` in every case.
    """
    yrs = pricing_basis("surr_chg_years")
    base = surr_chg_rate() * prem_pp()
    dur = max(t / 12.0, 1.0)
    raw = base * max(0.0, (yrs - dur) / (yrs - 1.0))
    return min(raw, surr_chg_cap_pp())


def cv_pp(t):
    """CV(t): the 해약환급금 per policy at time t.

    ``max(0, AV(t) - SC(t))``, the floor imposed by 감독규정 제7-66조제1항제1호 — 「계약자
    적립액에서 해약공제액을 공제한 금액이 음(陰)의 값인 경우에는 이를 영(零)으로
    처리한다」 — and **zero from t = n + 1**, because a 종신연금형 may not be surrendered
    once payment has begun.  Surrender is available right up to the day before the
    연금개시일, so ``CV(n)`` is a real number and is what a lapse at ``t = n - 1`` is paid.

    On the composite ``CV(t) == AV(t)`` at every duration, which makes the surrender value
    and the death benefit the same number: the two decrements differ in their rate and not in
    their payment.
    """
    if t > annuitisation_t():
        return 0.0
    return max(0.0, av_pp(t) - surr_chg_pp(t))


def cv_pp_net(t):
    """The 해약환급금 actually paid on surrender: :func:`cv_pp` less any loan balance.

    Equal to :func:`cv_pp` in the base run, where the 보험계약대출 module is off.  A
    surrender also carries a 16.5% 기타소득세 withholding, which reduces what the
    **policyholder** receives and not what the insurer pays; see :func:`surr_tax_pp`.
    """
    return max(0.0, cv_pp(t) - loan_pp(t))


def db_pp(t):
    """DB(t): the death benefit for a death in year t - 1, paid at t — **the fund**.

    「피보험자가 연금개시전 보험기간 중 사망한 경우에는 사망 당시의 계약자적립액을 지급하여
    드리고 이 계약은 더는 효력이 없습니다」.  There is **no cover above the fund**, and that
    is a design fact rather than an omission: 감독규정 제7-60조제9호 would otherwise require a
    death benefit of at least cumulative premiums, but it exempts a contract whose premium
    term ends at 80 or below, and this one ends at 60.  Zero once the annuity is in payment,
    where death inside the guarantee pays the unpaid guaranteed instalments instead.
    """
    if t > annuitisation_t():
        return 0.0
    return av_pp(t)


def db_pp_net(t):
    """The death benefit actually paid: :func:`db_pp` less any loan principal and interest."""
    return max(0.0, db_pp(t) - loan_pp(t))


def min_fund_pp():
    """G: the guaranteed minimum 계약자적립액 at the 연금개시일, 100.1% of premiums paid.

    「연금개시시의 계약자적립액은 이미 납입한 보험료의 100.1%를 최저보증 합니다」, with two
    more carriers writing the functionally identical 「이미 납입한 보험료 + 1,000원」.  Why
    100.1% and not 100%: 감독규정 제7-60조제2호 requires a 저축성보험's survival benefits to
    **exceed** premiums paid, so a nominal tenth of one per cent discharges the definition.

    It is not decorative.  On the published illustration the guaranteed-rate basis reaches
    only 100.5% of premiums at the end of the twenty-year payment term, so on a persistently
    low-rate scenario the floor is close to binding — and it is the only element of this
    contract that behaves like an option rather than an account.  Zero where the guarantee
    has been withdrawn.
    """
    if not min_fund_on():
        return 0.0
    return pricing_basis("min_fund_ratio") * cum_prem_pp(annuitisation_t())


# --- The loan and dividend modules -----------------------------------------

def loan_pp(t):
    """The 보험계약대출 balance per policy at time t; zero in the base run.

    Half the 해약환급금 drawn at the 계약해당일 closing policy year 15 **[std]**, compounding
    at the monthly equivalent of a **[std]** 4.00%
    and capped at the 해약환급금, because a policy loan may not exceed the value securing it.
    The rate is a standardization and is marked as one: **no retrieved document gives a
    numeric 보험계약대출이율 for a 연금저축보험**, and the only published rate constraint of
    that kind in the standard conditions is the 평균공시이율 + 1% ceiling on reinstatement
    interest.  The balance is deducted from the death benefit, from the surrender payment and
    from the fund that buys the annuity, so it is recovered without a cash flow of its own.
    """
    if not loan_on() or t > annuitisation_t():
        return 0.0
    draw = 12 * int(pricing_basis("loan_draw_year"))
    if t < draw:
        return 0.0
    if t == draw:
        return pricing_basis("loan_draw_frac") * cv_pp(t)
    monthly = (1.0 + pricing_basis("loan_rate")) ** (1.0 / 12.0) - 1.0
    return min(loan_pp(t - 1) * (1.0 + monthly), cv_pp(t))


def div_credit_pp(t):
    """The 계약자배당 declared on the fund in policy year t; zero on the 무배당 composite.

    The rate is an **annual** one and a twelfth of it is credited each month.
    Five of the eight retrieved contracts are 무배당 and three are 배당, and one carrier sells
    both forms of the same product.  No retrieved carrier publishes a dividend *rate* on a
    연금저축보험, which is one of the two reasons the composite takes the non-participating
    form.
    """
    if t >= annuitisation_t():
        return 0.0
    return div_rate() / 12.0 * av_pp(t)


def div_acc_pp(t):
    """The accumulated 계약자배당 at time t, credited at the 공시이율.

    Applied at the 연금개시일 as an **증액연금** rather than paid in cash — 「보험기간 중
    발생한 배당금은 계약소멸할 때 계약자에게 지급하거나 연금 지급개시 이후에 증액연금으로
    수익자에게 지급합니다」 — so it enters :func:`annuity_fund_net_pp` and nowhere else.
    """
    if t <= 0:
        return 0.0
    monthly = (1.0 + pricing_basis("div_int_rate")) ** (1.0 / 12.0) - 1.0
    return ((div_acc_pp(t - 1) + div_credit_pp(t - 1)) * (1.0 + monthly))


# --- The annuitisation transition ------------------------------------------

def annuity_fund_pp():
    """F: the 계약자적립액 at the 연금개시일, after the 100.1% floor.

    Struck once, at ``t = n``.  This is the contractual quantity the illustration publishes
    and the one the floor applies to; the amount actually converted into an annuity is
    :func:`annuity_fund_net_pp`.
    """
    return max(av_pp(annuitisation_t()), min_fund_pp())


def annuity_fund_net_pp():
    """The amount actually converted into the annuity: F plus dividend, less any loan.

    A 보험계약대출 outstanding at the 연금개시일 is repaid out of the fund, so it reduces the
    annuity rather than producing a cash flow; an accumulated 계약자배당 is added as an
    증액연금.  Both are zero in the base run.
    """
    n = annuitisation_t()
    return max(0.0, annuity_fund_pp() + div_acc_pp(n) - loan_pp(n))


def annuity_due_certain_factor():
    """adue(k): the 확정기간연금형 factor, the annuity-due payable ``f`` times a year.

    ``(1 - v**k) / d**(f)`` at the declared rate in force at the 연금개시일 — 「연금개시시점의
    계약자적립액을 기준으로 공시이율을 적용하여 … 계약자가 선택한 확정된 연금지급기간 동안
    나누어 계산」.  **Mortality does not enter it**, and neither does survival: the
    instalments are paid to the count whether or not the annuitant lives.

    The monthly form is what makes it reconstruct the published figures.  With the 0.5%
    annuity-phase charge it reproduces all six published implied factors — 9.06 / 12.92 /
    16.39 at 2.15% and 9.81 / 14.53 / 19.13 at the guaranteed rate — to three or four
    significant figures.
    """
    i = credit_rate(annuitisation_t())
    k = payout_term_y()
    f = annuity_freq()
    if i <= 0.0:
        return float(k)
    d = i / (1.0 + i)
    df = f * (1.0 - (1.0 - d) ** (1.0 / f))
    return (1.0 - (1.0 + i) ** (-k)) / df


def annuity_due_factor_on(table):
    """adue_life: the 종신연금형 factor on a stated annuitant vintage.

    ``sum_j max(1{j < g}, jp_x) v**j`` on ``table`` at **100%** — a pricing basis, not the
    best-estimate one — less the standard ``(f - 1) / (2f)`` correction for instalments
    payable ``f`` times a year.  「연금개시시점의 계약자적립액을 기준으로 연금사망률 및
    공시이율을 적용하여 … 나누어 계산」: this is the only place mortality touches the
    contract.  On the 확정기간연금형 form it falls through to
    :func:`annuity_due_certain_factor`, so the ratchet comparison is well defined for both
    forms.

    At the anchor cell this returns 23.5815 on the issue vintage, which with the 0.5% charge
    is the **23.70** the published illustration implies — the single calibration target the
    public record offers.
    """
    if payout_form() == "certain":
        return annuity_due_certain_factor()
    i = credit_rate(annuitisation_t())
    g = guar_term_y()
    x0 = annuity_age_eff()
    om = omega_age(table)
    total = 0.0
    surv = 1.0
    j = 0
    while x0 + j <= om:
        total += max(1.0 if j < g else 0.0, surv) / (1.0 + i) ** j
        surv = surv * (1.0 - mort_rate_at_age(table, x0 + j))
        j = j + 1
    f = annuity_freq()
    return total - (f - 1.0) / (2.0 * f)


def annuity_due_factor():
    """The factor the annuity is actually bought at, on the vintage in force.

    :func:`annuity_due_certain_factor` on the 확정기간연금형 form and
    :func:`annuity_due_factor_on` at :func:`mort_table_name` on the 종신연금형 form.
    """
    if payout_form() == "certain":
        return annuity_due_certain_factor()
    return annuity_due_factor_on(mort_table_name())


def annuity_amount_pp():
    """B: the 연금연액, struck once at ``t = n`` and never recomputed.

    ``F_net / adue x (1 - 0.005)``, the 0.5% being the 연금수령기간 중의 관리비용 two carriers
    disclose.  That charge is what reconciles the composite's factor with the published
    illustrations, and it is a carrier choice rather than a market convention: a third
    carrier discloses none and its implied factors run about 0.6% the other way.

    The two forms differ by a factor of two and a half on the same fund.  At the anchor cell
    a 종신연금형 with a ten-year guarantee pays about 38% of what a ten-year
    확정기간연금형 pays, which is the number a policyholder is actually choosing between —
    and the tax code prices the choice, a 종신계약 drawing a flat 3.3% withholding against
    5.5% until 70 on a fixed-term annuity.
    """
    return (annuity_fund_net_pp() / annuity_due_factor()
            * (1.0 - pricing_basis("annuity_charge_rate")))


def annuity_pp(t):
    """The annuity **instalment** per contract payable at the start of month t.

    ``B / 12``, the 연금연액 divided into the twelve monthly instalments the contract
    actually pays — 연금지급주기 is 매월 on the base run and the factor the amount was struck
    at already carries the ``f``-times-a-year correction, so the monthly grid pays the
    instalment where the annual grid paid a year's worth at once.

    Paid in advance from the 연금개시일.  On the 확정기간연금형 form there are exactly
    ``12 k`` of them and the contract ends; on the 종신연금형 form the amount is the same for
    as long as the contract is in force, and it is :func:`pols_if` rather than the amount
    that carries the life contingency.  A death inside the 보증지급기간 does not stop the
    stream: the unpaid guaranteed instalments are paid to the beneficiary, and the base run
    assumes continuation at 100% **[std]** rather than commutation.
    """
    n = annuitisation_t()
    if t < n:
        return 0.0
    if payout_form() == "certain" and t >= n + 12 * payout_term_y():
        return 0.0
    return annuity_amount_pp() / 12.0


# --- In-force and decrements -----------------------------------------------

def pols_if_init():
    """The in-force count at issue: one policy, so every amount is per policy issued."""
    return 1.0


def pols_if(t):
    """l(t): contracts with an obligation open at the **start** of policy year t.

    :func:`pols_if_init` at ``t = 0``.  Through the deferral phase the recursion
    ``l(t+1) = l(t)(1 - q^m(t))(1 - w^m(t))``, death before lapse, a month at a time.  From
    ``t = n`` the rules
    change with the payout form: on the 확정기간연금형 the instalments are unconditional, so
    ``l`` is **flat** through the certain period and drops to zero once the last one is paid;
    on the 종신연금형 it is flat through the 보증지급기간 and then runs off on the
    best-estimate annuitant basis.

    This is the weight on every cash flow of the same ``result_cf()`` row.  It is a
    start-of-month count, so no decrement has been applied when a month opens and the first
    row is ``pols_if_init()`` exactly.
    """
    n = annuitisation_t()
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    if t <= n:
        return pols_if_at(t - 1, "AFT_DECR")
    base = pols_if(n)
    if payout_form() == "certain":
        return base if t < n + 12 * payout_term_y() else 0.0
    guaranteed = 1.0 if t - n < 12 * guar_term_y() else 0.0
    return base * max(guaranteed, lives_if(t) / lives_if(n))


def pols_if_at(t, timing):
    """The number of contracts in force at a point inside month t.

    ``"BEF_DECR"``
        l(t), the start of the month before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before surrenders — the processing order is **death before
        lapse** **[std order]**, so this is the population surrenders are taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) - pols_death(t)
    if timing == "AFT_DECR":
        if t < annuitisation_t():
            return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def lives_if(t):
    """L(t): the probability the annuitant is alive at the start of month t.

    ``L(t+1) = L(t)(1 - q^m(t))`` throughout.  Carried separately from :func:`pols_if` because
    the two measure different things: in the deferral phase a surrender removes a contract
    without removing a life, and in the payout phase a 확정기간연금형 obligation survives the
    annuitant entirely.  Collapsing the two is the most likely way to build this product
    wrongly.
    """
    if t <= 0:
        return 1.0
    return lives_if(t - 1) * (1.0 - mort_rate_mth(t - 1))


def pols_death(t):
    """D(t): expected deaths in month t, taken at the **end** of the month.

    ``l(t) q^m(t)`` in the deferral phase.  **Zero** inside a certain or guaranteed period,
    where the obligation does not depend on survival; on the 종신연금형 form after the
    guarantee it is the run-off of :func:`pols_if` itself.
    """
    n = annuitisation_t()
    if t < n:
        return pols_if(t) * mort_rate_mth(t)
    if payout_form() == "certain":
        return 0.0
    if t - n < 12 * guar_term_y() - 1:
        return 0.0
    return max(0.0, pols_if(t) - pols_if(t + 1))


def pols_lapse(t):
    """W(t): expected surrenders at the end of month t, from the survivors of mortality.

    ``l(t)(1 - q^m(t)) w^m(t)``, and zero from ``t = n``: a 종신연금형 may not be surrendered once
    payment has begun, and a 확정기간연금형 pays its instalments to the count.  Surrender is
    available right up to the day before the 연금개시일, so the decrement runs through
    ``t = n - 1`` and the contracts leaving there are paid ``CV(n)``.
    """
    if t >= annuitisation_t():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_maturity(t):
    """The count whose cover ends at the scheduled end of the contract, paid for or not.

    The library-wide meaning of the name: the contracts reaching the scheduled end, whether
    or not anything is paid for reaching it.  Here that end is the last 확정기간연금형
    instalment, so this is non-zero only at ``t = n + k - 1`` and zero on the 종신연금형 form,
    which has no fixed end.

    **There is no** ``claims(t, "MATURITY")`` **on this product**, and the absence is a
    product fact: 연금저축보험 has no maturity benefit and no maturity date, because the
    deferral phase ends by conversion into the payout phase rather than by payment.  The
    count is still needed for the in-force roll-forward to close, because the survivors of
    that year neither die nor surrender.
    """
    if payout_form() != "certain":
        return 0.0
    if t != annuitisation_t() + 12 * payout_term_y() - 1:
        return 0.0
    return pols_if(t)


# --- Cash flows ------------------------------------------------------------

def premiums(t):
    """Premium income at the start of month t, an inflow.

    The 기본보험료 and any 추가납입보험료 together, weighted by the in-force.  Level and
    guaranteed for the whole 납입기간, with no review right, and **nothing** after 납입완료 —
    neither the gap between 납입완료 and 연금개시 nor the payout phase carries a premium, and
    no contribution may be made at all once annuitisation has been requested.
    """
    if not prem_paying(t):
        return 0.0
    return (prem_mth_pp() + addl_prem_mth_pp()) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"ANNUITY"``
        the instalment paid in advance at the start of month t, to every contract with an
        obligation open.  A **living** benefit on the 종신연금형 form past the guarantee;
        unconditional inside a certain or guaranteed period, which is prepaid
        survival-contingent cover and still not a benefit death can trigger.

    ``"DEATH"``
        the 계약자적립액 paid for deaths at the end of the month, ``DB(t+1) D(t)``, net of any
        loan balance.  Zero once the annuity is in payment.

    ``"LAPSE"``
        surrender payments at the end of the month, ``CV(t+1) W(t)``, net of any loan balance.
        On the composite this is the same per-policy amount as ``"DEATH"``, because the
        surrender charge is nil: **the two decrements differ in their rate, not in their
        payment**.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("ANNUITY", "DEATH", "LAPSE"))
    if kind == "ANNUITY":
        return annuity_pp(t) * pols_if(t)
    if kind == "DEATH":
        return db_pp_net(t + 1) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp_net(t + 1) * pols_lapse(t)
    raise ValueError("invalid kind")


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)**(t // 12)`` **[std]**, pi = 2%.

    An expense basis is quoted per annum and so is the inflation assumption on it, so the
    factor steps on the **계약해당일** and is level across the twelve months of a policy year.
    """
    return (1.0 + expense_basis("inflation_rate")) ** (t // 12)


def claim_expenses(t):
    """ec D(t): the claim handling expense on the month's death claims **[std]**.

    ₩30,000 per death claim in the deferral phase and none on surrender or in payment — a
    death after the 보증지급기간 ends the contract with nothing paid, so there is no claim to
    handle.  A cells of its own, a column of its own in :func:`result_cf` and a term of its
    own in :func:`net_cf`: the library-wide meaning is that :func:`expenses` is acquisition
    and maintenance, and the expense that scales with claims is never folded into it.
    """
    if t >= annuitisation_t():
        return 0.0
    return expense_basis("expense_claim") * pols_death(t)


def expenses(t):
    """E0 and e(t): acquisition and maintenance **cash** expense in month t **[std]**.

    ₩200,000 per policy at ``t = 0``, then ₩30,000 per policy **per year** before
    annuitisation and ₩20,000 once the annuity is in payment, both inflating at 2% p.a. and
    both charged **a twelfth at a time**: the table holds the annual figures the expense
    basis is quoted in and the grid divides them, so the file did not move when the step
    did.  These are
    best-estimate cash expenses and are entirely separate from the 계약체결비용 and
    계약관리비용, which are contractual loadings living inside :func:`av_pp`.  Charging the
    loadings against the cash flow, or projecting these into the fund, double-counts expense
    in one direction and destroys the fund calibration in the other.
    """
    acq = expense_basis("expense_acq") * pols_if(t) if t == 0 else 0.0
    maint = (expense_basis("expense_maint_defer") if t < annuitisation_t()
             else expense_basis("expense_maint_payout")) / 12.0
    return acq + maint * inflation_factor(t) * pols_if(t)


def commissions(t):
    """Commission outgo in month t; **zero in every month** on this composite.

    The composite follows a direct-channel product whose published 모집수수료율 is 0.00% in
    every year, so the level monthly charge is the whole acquisition cost and there is no
    unpublished remainder.  The cells and its column are retained because a zero states the
    fact where a missing column would only hide it, and because a tied-channel or
    bancassurance variant would fill them in.
    """
    init = (expense_basis("comm_init_rate") * prem_pp() * pols_if(t)
            if t == 0 else 0.0)
    renew = (expense_basis("comm_renewal_rate") * premiums(t)
             if 12 <= t < prem_end_t() else 0.0)
    return init + renew


def policy_loans(t):
    """The 보험계약대출 advanced in month t, an outflow; zero in the base run.

    Only in the draw year.  The balance is recovered without a cash flow of its own, by
    reducing the death benefit, the surrender payment and the fund that buys the annuity.
    """
    if not loan_on():
        return 0.0
    if t != 12 * int(pricing_basis("loan_draw_year")):
        return 0.0
    return loan_pp(t) * pols_if(t)


def net_cf(t):
    """CF(t): the net cash flow of month t, **income positive**.

    Premiums less annuity instalments, death and surrender benefits, acquisition and
    maintenance expense, claim expense, commission and any loan advanced.  The technical
    notes print the stream this way round, so this model publishes no ``liability_cf``
    companion — that absence is a fact about which orientation the notes chose, not an
    omission.

    Nothing in the tax layer appears here.  The 세액공제 is a payment from the state to the
    saver and the 기타소득세 is a withholding from the saver's proceeds; neither passes
    through the insurer's account, and folding either into this line would misstate the
    liability in a way no reconciliation would catch.
    """
    return (premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
            - commissions(t) - policy_loans(t))


# --- The tax layer, which is not a cash flow -------------------------------

def tax_credit_rate():
    """The 세액공제 rate: 16.5% at the anchor cell **[std income band]**.

    12% of contributions, or 15% where 종합소득금액 is ₩45,000,000 or less, grossed up for
    the 10% 지방소득세 to the 13.2% / 16.5% every Korean consumer document quotes.  The
    grossed-up pair is **[unverified] arithmetic on a verified base**, because the 지방세법
    imposing the surtax was not retrieved.  **Relief here is a credit and not a deduction**,
    so the after-tax value of a contribution *falls* with income — the opposite of every
    other market in this repository.  The model takes the lower-income band, which is a
    standardization: a contract does not know its owner's income.
    """
    return tax_basis("credit_rate_low_income")


def tax_credit_pp(t):
    """The month's share of the 세액공제; not an insurer cash flow.

    The relief is annual — ``min(contribution, ₩6,000,000) x 16.5%``, and at the anchor
    cell's ₩6,000,000 contribution that is ₩990,000 a year or ₩792,000 in the higher-income
    band — and the **cap is a tax-year cap**, so it is applied to the year's contribution and
    a twelfth of the result is attributed to each month a premium is paid in. Twelve months
    therefore sum to exactly the year's credit. It is published because
    it is the reason the product exists and a first-order driver of persistency, and it is
    kept out of :func:`net_cf` because it is paid by the state to the policyholder.
    """
    if not prem_paying(t):
        return 0.0
    contrib = min(prem_pp() + addl_prem_pp(), tax_basis("credit_cap"))
    return contrib * tax_credit_rate() / 12.0


def surr_tax_pp(t):
    """The 16.5% 기타소득세 withheld on a surrender at time t — **not an insurer cash flow**.

    Any amount withdrawn that is not 연금수령 is 기타소득 under 소득세법 제21조제1항제21호,
    withheld at 15% and grossed up to 16.5% with the local surtax; nine independent carrier
    documents state the rate identically.  The base is the credited money and its return
    rather than the whole fund, but on a contract whose contributions were all inside the
    credit cap the charge falls on essentially the whole surrender value: one carrier's
    surrender illustration carries a 세후지급 예상액 column that is uniformly 83.5% of the
    surrender value at every duration and on both interest bases.

    This is the single most important number on the page for the lapse assumption, and it is
    **not** deducted from :func:`claims`: the insurer pays the whole surrender value and the
    withholding is taken from the policyholder's proceeds.
    """
    return tax_basis("other_income_tax_rate") * cv_pp(t)


def pension_tax_rate(t):
    """The 연금소득세 withholding rate applying to an instalment paid in policy year t.

    Banded by the pensioner's age — 5.5% under 70, 4.4% from 70 to 79, 3.3% from 80 — with a
    flat **3.3% at every age for a 종신계약**, reduced from 4% to 3% for pensions received on
    or after 2026-01-01.  The lowest applicable rate governs, so a life annuity carries a
    standing 2.2-percentage-point advantage over a fixed-term one for a 55-to-70-year-old,
    where before 2026 it was 1.1 points.  That is a dated, quantified incentive to annuitise
    for life.

    One caution travels with it: 종신계약 is defined by 소득세법 시행령 제187조의2, whose
    **operative text could not be retrieved**, so whether a guarantee period of any length is
    compatible with the status is **[unverified]**.  If a ten-year guarantee disqualified the
    contract the anchor cell's withholding would be 5.5% until 70.
    """
    if t < annuitisation_t():
        return 0.0
    if payout_form() == "life_guar":
        return tax_basis("pension_tax_rate_life")
    if age(t) >= 80:
        return tax_basis("pension_tax_rate_80plus")
    if age(t) >= 70:
        return tax_basis("pension_tax_rate_70to79")
    return tax_basis("pension_tax_rate_under70")


def annuity_tax_pp(t):
    """The 연금소득세 withheld from the instalment in year t; not an insurer cash flow.

    Private pension income of ₩15,000,000 or less in a year is 분리과세연금소득, so for most
    savers the withholding settles the liability.  At the anchor cell the annuity is well
    inside the threshold, and so is the market's average balance.
    """
    return annuity_pp(t) * pension_tax_rate(t)


def annuity_year_no(t):
    """연금수령연차: the payment-year counter the 연금수령한도 formula is indexed by.

    It runs from the tax year in which drawing first became possible — the later of 만 55세
    and five years from the 계약일 — and **not** from the year drawing actually starts.  At
    the anchor cell a contract taken out at 40 could first have drawn at 55, so by the 65
    annuity date the counter has reached 11 and the limit does not apply at all.  Read off
    :func:`age`, which is 보험나이, where the statute is on 만나이: a **[std]** simplification
    worth at most one year.
    """
    first = max(tax_basis("min_annuity_age"),
                issue_age() + tax_basis("min_account_years"))
    return max(1, int(age(t) - first + 1))


def annuity_limit_pp(t):
    """연금수령한도: the most that may be drawn in payment year t and still be 연금수령.

    ``평가액 / (11 - 연금수령연차) x 120/100``, and **where the counter reaches 11 the formula
    does not apply at all**, in which case this cells returns the whole 평가액.  Because the
    counter climbs by one each tax year the limit is a rising fraction of the balance — 12%
    in year 1, 60% in year 9, 120% in year 10, unlimited from year 11 — so in practice ten
    years is the shortest payout the tax code tolerates for a contract annuitised as early as
    it can be.

    The 평가액 is taken as the fund at the 연금개시일 throughout, a **[std]** simplification:
    the statute values the account each year, and a model that tracked a declining balance
    would give a slightly tighter limit in later years.  Anything above the limit is deemed
    연금외수령 and bears the 16.5% 기타소득세 instead.

    It is an **annual** limit, so what is compared against it is the policy year's twelve
    instalments and not one of them: see :func:`check_annuity_limit_resid`.
    """
    n = annuitisation_t()
    if t < n:
        return 0.0
    yr = annuity_year_no(t)
    base = tax_basis("limit_denominator_base")
    if yr >= base:
        return annuity_fund_net_pp()
    return annuity_fund_net_pp() / (base - yr) * tax_basis("limit_uplift")


# --- Roll-forward and ledger checks ----------------------------------------

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``l(t) - l(t+1) - deaths - surrenders - expiries``.  Expiries are non-zero only in the
    month the last 확정기간연금형 instalment is paid, where the survivors neither die nor
    surrender — the contract simply ends — so without that term the final payout month
    appears to lose contracts with no cause.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t.
    :func:`check_pols_roll_fwd_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol      # noqa: F821
               for t in range(proj_len()))


def check_av_roll_fwd_resid(t):
    """The 계약자적립액 recursion residual in month t; zero over the deferral phase.

    ``(AV(t) + NP(t) - C(t))(1 + j_c(t)) - AV(t+1)``, scaled by the fund so the tolerance
    means the same thing at every duration.  Zero by definition from ``t = n``, where there
    is no fund left to roll forward.  A model that had put a survivorship release into this
    recursion — the shape of the *Japanese* deferred annuity on the same page of this
    repository — would fail here rather than silently misstate the 연금개시 fund.
    """
    if t >= annuitisation_t():
        return 0.0
    return av_pp_at(t, "AFT_INT") - av_pp(t + 1)


def check_av_roll_fwd():
    """True when the 계약자적립액 recursion closes in every deferral month."""
    scale = max(1.0, annuity_fund_pp())
    return all(abs(check_av_roll_fwd_resid(t)) <= roll_fwd_tol * scale  # noqa: F821
               for t in range(proj_len()))


def check_cv_floor_resid(t):
    """The 해약환급금 identity residual at duration t; zero everywhere.

    ``CV(t) - max(0, AV(t) - SC(t))`` over the deferral phase, which is 감독규정
    제7-66조제1항제1호 written out: the surrender value is the 계약자적립액 net of the
    해약공제액, and where that is negative it is set to zero.
    """
    if t > annuitisation_t():
        return 0.0
    return cv_pp(t) - max(0.0, av_pp(t) - surr_chg_pp(t))


def check_cv_floor():
    """True when the 해약환급금 is the fund net of the deduction, floored at zero, throughout.

    The regulatory identity, asserted rather than assumed.  On the composite it also says
    something stronger, which the residual makes visible: with a nil 해약공제액 the surrender
    value **is** the fund, so death and surrender pay the same amount at every duration.
    """
    scale = max(1.0, annuity_fund_pp())
    return all(abs(check_cv_floor_resid(t)) <= roll_fwd_tol * scale   # noqa: F821
               for t in range(proj_len()))


def check_surr_chg_cap_resid(t):
    """The 표준해약공제액 headroom at duration t; negative is the breach.

    ``SC_max - SC(t)``.  Published unsigned rather than clipped so that the headroom is
    readable off it — on the composite it is the whole cap at every duration, because the
    surrender charge is nil.
    """
    return surr_chg_cap_pp() - surr_chg_pp(t)


def check_surr_chg_cap():
    """True when the 해약공제액 never exceeds 별표 14's 표준해약공제액 at any duration.

    The statutory bound of 감독규정 제7-66조 and 별표 14, which singles this product out for
    the tightest coefficient in the schedule — 3% of the 연납순보험료 for a 무배당
    연금저축보험 against 5% for a general 저축성보험, with 주4's 6% concession expressly
    denied.  The composite sits far inside it, and so does the model point carrying the
    postal insurer's front-end charge.
    """
    return all(check_surr_chg_cap_resid(t) >= -roll_fwd_tol * max(    # noqa: F821
        1.0, prem_pp()) for t in range(proj_len()))


def check_min_fund_resid(t):
    """The 100.1% minimum-fund headroom at ``t = n``; negative is the breach, zero elsewhere.

    ``F - G``, the fund at the 연금개시일 less 100.1% of premiums paid.  Zero at every other
    duration, and zero throughout where the guarantee has been withdrawn.
    """
    if t != annuitisation_t() or not min_fund_on():
        return 0.0
    return annuity_fund_pp() - min_fund_pp()


def check_min_fund():
    """True when the fund at the 연금개시일 is at least 100.1% of premiums paid.

    The one guarantee that bites before annuitisation, and it bites at one date.  It is a
    **survival** guarantee: a death claim in deferral is not floored at premiums paid on this
    composite, so the floor is payable only to a policy that reaches the 연금개시일 in force.
    """
    return all(check_min_fund_resid(t) >= -roll_fwd_tol * max(        # noqa: F821
        1.0, cum_prem_pp(annuitisation_t()))
        for t in range(proj_len()))


def check_annuity_total_resid(t):
    """The guaranteed-instalment residual in policy year t; zero everywhere.

    The instalment actually payable per contract less ``B / 12``, over the certain period of
    the 확정기간연금형 or the 보증지급기간 of the 종신연금형.  Zero outside that window.
    """
    n = annuitisation_t()
    guaranteed = 12 * (payout_term_y() if payout_form() == "certain"
                       else guar_term_y())
    if t < n or t >= n + guaranteed:
        return 0.0
    return annuity_pp(t) - annuity_amount_pp() / 12.0


def check_annuity_total():
    """True when the undiscounted guaranteed instalments sum to k B, or g B on the life form.

    A 확정기간연금형 pays exactly ``12 k`` instalments regardless of survival and a 종신연금형
    at least ``12 g`` of them, summing to ``k B`` and ``g B``, and the contract warns that the guaranteed total may come to **less**
    than the fund at annuitisation.  A model that had decremented the guaranteed period by
    mortality, or that had recomputed ``B`` after the 연금개시일, would fail here.
    """
    n = annuitisation_t()
    years = (payout_term_y() if payout_form() == "certain" else guar_term_y())
    total = sum(annuity_pp(t) for t in range(n, n + 12 * years))
    scale = max(1.0, annuity_amount_pp())
    return (all(abs(check_annuity_total_resid(t)) <= roll_fwd_tol * scale  # noqa: F821
                for t in range(proj_len()))
            and abs(total - years * annuity_amount_pp())
            <= roll_fwd_tol * scale * years * 12)


def check_annuity_limit_resid(t):
    """The 연금수령한도 headroom in payment year t; negative would mean 연금외수령.

    ``limit(t)`` less the **policy year's** twelve instalments, read at each anniversary of
    the 연금개시일 and zero in the eleven months between: the 연금수령한도 is an annual
    figure and comparing it with one instalment would understate the draw twelvefold.  Zero
    outside the payout phase.  It is published because the constraint
    is real even where it does not bind: every retrieved contract makes the default election
    the tax-recognised maximum — 「연금액은 관련 세법에서 정한 바에 따라 연금소득으로
    인정받을 수 있는 범위 이내로 합니다」 — so the contract itself enforces it.
    """
    if t < annuitisation_t() or t % 12 != annuitisation_t() % 12:
        return 0.0
    drawn = sum(annuity_pp(u) for u in range(t, min(t + 12, proj_len())))
    return annuity_limit_pp(t) - drawn


def check_annuity_limit():
    """True when no instalment exceeds the 연금수령한도 of 소득세법 시행령 제40조의2제4항.

    At the anchor cell the constraint does not bind at all, because the 연금수령연차 has
    reached 11 by the 연금개시일 and the formula is disapplied.  Where it does bind — a
    contract annuitising at 55 — the limit is 12% of the 평가액 in the first payment year, and
    a payout term shorter than about ten years would breach it.  A breach is not an error in
    the model, it is a contract that has stopped being 연금수령 and started being 연금외수령
    at 16.5%, which is why it is worth a check rather than a comment.
    """
    return all(check_annuity_limit_resid(t) >= -roll_fwd_tol * max(   # noqa: F821
        1.0, annuity_amount_pp()) for t in range(proj_len()))


def check_mort_law_resid(t):
    """The shipped-rate residual against the stated [std] construction at ``age(t)``.

    ``q_shipped(x+t) - q_law(x+t)``.  Zero on the shipped file by construction, and non-zero
    the moment ``mort_table.csv`` is replaced with a real basis — which is the correct answer
    then, and the reason the check exists.
    """
    table = mort_table_name()
    x = age(t)
    if x >= omega_age(table):
        return 0.0
    return mort_rate_at_age(table, x) - mort_rate_law(table, x)


def check_mort_law():
    """True when every rate the projection reads is the one the stated construction produces.

    The library ships no Korean mortality table because none is published, so what it ships
    instead is a **construction plus its recipe**.  This is the cells that keeps the two
    honest: the Makeham parameters, the female setback and the vintage improvement factor all
    live in ``mort_anchor_table.csv``, and a rate that no longer follows from them is either
    a hand edit or a real table.
    """
    return all(abs(check_mort_law_resid(t)) <= 1e-15
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The cash flow ledger residual in month t; zero everywhere.

    :func:`net_cf` less the sum of the columns ``result_cf()`` publishes.  It is the check
    that the published statement and the projected total are the same object, which is the
    one identity a reader of the output cannot verify for themselves.
    """
    return (net_cf(t) - premiums(t) + claims(t, "ANNUITY") + claims(t, "DEATH")
            + claims(t, "LAPSE") + expenses(t) + claim_expenses(t)
            + commissions(t) + policy_loans(t))


def check_net_cf():
    """True when the published cash flow columns add up to :func:`net_cf` in every month."""
    scale = max(1.0, prem_pp())
    return all(abs(check_net_cf_resid(t)) <= roll_fwd_tol * scale     # noqa: F821
               for t in range(proj_len()))


# --- Results ---------------------------------------------------------------

def result_cf():
    """Result table of cash flows, indexed by the 0-based month t.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash flow on
    the same row.  ``net_cf`` carries the library's income-positive sign, so the deferral
    rows are positive and the payout rows are large negatives.  ``commissions`` and
    ``policy_loans`` are columns of zeros in the base run and are published rather than
    dropped, because a zero states that the module is off where a missing column would only
    hide it.

    There is deliberately **no** ``claims`` column: the statement publishes the ``claims_*``
    split so its columns sum to ``net_cf``, and the ``claims(t, kind)`` cells stays.  There is
    no tax column either — see :func:`result_tax`, and :func:`net_cf` for why.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "policy_loans": [policy_loans(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force, decrements and per-policy amounts, indexed by t.

    The companion to :func:`result_cf`: the two in-force measures side by side, the decrements
    that move them — the **monthly** conversions actually applied, whose annual parents are
    ``mort_rate`` and ``lapse_rate`` — and the fund, surrender value and death benefit that
    price them.  ``credit_rate`` is published as the **annual** declared rate, because that
    is the figure a Korean illustration quotes; the fund rolls on
    ``credit_rate_mth``.  Reading
    ``av_pp``, ``cv_pp`` and ``cum_prem_pp`` in one table is the quickest way to see the
    환급률 a Korean illustration quotes and the duration at which it passes 100%.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "lives_if": [lives_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "credit_rate": [credit_rate(t) for t in ts],
            "cum_prem_pp": [cum_prem_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "loan_pp": [loan_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_tax():
    """Result table of the tax layer, indexed by t — **none of it an insurer cash flow**.

    The 세액공제 the saver receives on the way in, the 16.5% 기타소득세 they would bear on a
    surrender at each duration, and the 연금소득세 withheld from each instalment beside the
    연금수령한도 that decides whether the instalment is 연금수령 at all.  It is a separate
    frame from :func:`result_cf` for a reason: adding any of these to the cash flow statement
    would make its columns stop summing to :func:`net_cf`, and would put money that never
    passes through the insurer's account into the liability.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "tax_credit_pp": [tax_credit_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "surr_tax_pp": [surr_tax_pp(t) for t in ts],
            "annuity_pp": [annuity_pp(t) for t in ts],
            "pension_tax_rate": [pension_tax_rate(t) for t in ts],
            "annuity_tax_pp": [annuity_tax_pp(t) for t in ts],
            "annuity_year_no": [annuity_year_no(t) for t in ts],
            "annuity_limit_pp": [annuity_limit_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

roll_fwd_tol = 1e-10

math = ("Module", "math")

pd = ("Module", "pandas")
