# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.CI_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the first policy month, month ``t``
runs from time ``t`` to time ``t + 1``, and the contractual **policy year label is
``policy_year(t) = t // 12 + 1``**. ``proj_years() = omega_age() - age_at_entry() + 1`` is
the number of projected policy years and ``proj_len() = 12 proj_years()`` the number of
**months**, the frame's exclusive end, so the frame is ``range(proj_len())`` and the last
projected month is ``t = proj_len() - 1``. There is no
maturity date and no 만기보험금; the horizon is the terminal age of the mortality table,
every remaining life dies in the **last policy year**, and nothing is paid there but a
death benefit.

**Annual assumptions stay annual; only the grid underneath them is monthly.** Every rate
the sources tabulate — :func:`mort_rate`, :func:`mort_rate_ci`, :func:`ci_rate`,
:func:`lapse_rate`, :func:`lapse_rate_ci`, :func:`waiver_rate` — holds the **annual**
figure of the policy year the month falls in, and its ``_mth`` companion applies
``1 - (1 - q)^(1/12)``, so that the twelve months of a policy year compound back to exactly
that year's rate. The roll-forward applies the companions and nothing else. The one
decrement that is **not** converted this way is the terminal age, where ``q = 1`` admits no
root and the certain death is spread uniformly over the year as ``1 / (12 - j)``; and the
one rate that is **placed** rather than converted is the 90-day 보장개시일, which is a date
and now falls where the contract puts it — see :func:`ci_wait_factor_mth`.

**Two clocks, and every cells docstring says which one it is on.** The **month** clock is
``t`` above: decrements, policy counts, premiums, claims, expenses, and every row of
``result_cf()``, ``result_pols()`` and ``result_val()`` are indexed by it, and it runs
``0 … proj_len() - 1``. The **month-end** clock is a time-point index running
``0 … proj_len()``, 0 at issue, and carries the contract's *state* — :func:`pol_val_pp`,
:func:`cum_prem_pp`, :func:`base_benefit_pp`, :func:`surr_chg_pp`, :func:`cv_std_pp`,
:func:`cv_mult`, :func:`cv_pp`, :func:`cv_pp_ci`, :func:`resid_db_pp`,
:func:`loan_avail_pp`, :func:`loan_avail_ci_pp` and :func:`pol_loan_draw`. It is already
0-based and does **not** move with the frame. A 계약해당일 is a month-end ``d = 12 y``.
Both are written ``t``; they coincide at the
**opening** of a month, because month ``t`` opens at month-end ``t`` and closes at
month-end ``t + 1``. So a claim or a surrender arising in month ``t``, which is paid at
the **end** of it, is paid the month-end-``t + 1`` amount, and that ``+ 1`` is
written out wherever it occurs. ``V(0) = 0`` and ``SC(0) = SC_max`` are the issue-instant
values of the second clock and are real values, not padding.

A **post-CI cohort label** ``s`` is on that same month-end clock: it is the month-end at
which the acceleration was paid, so a life accelerating in month ``t`` joins cohort
``s = t + 1``. The first policy year's **reduced** claims take the **negative** labels
``-(t + 1)``, which are free precisely because no acceleration can be paid at month-end 0
and no full claim ever carries one. The monthly grid turns the annual model's single
reduced cohort into twelve, each paid off its own 기본보험금.

.. rubric:: The age basis

Ages are **보험나이** (*boheom nai*, insurance age): 만나이 at the 계약일 with a fraction
under six months discarded and six months or more rounded up, incrementing on each
계약해당일. It is the contractual age, the index of every Korean rate card, and the basis
[S3]'s disclosed 예정위험률 grid is stated on, so ``age(t) = x + t // 12`` steps it on
exactly that date and nowhere else, and one table rate holds for the twelve months of a
policy year. The one contractual exception — 계약의 무효 for an
age outside the permitted range, which is judged on 만나이 — produces no cash flow and is
not modelled. This is a **보험나이** model throughout; nothing here is on 만나이, and the
two differ by about half a year of ageing on every row.

.. rubric:: Input data

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/ci_insurance/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

Each table has a filename Reference and a reader Cells, both on :mod:`~.CI_KR_S.Data`,
reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
ci_incidence_file       data.ci_incidence_table()           ci_incidence_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string. The technical notes use compact actuarial symbols
instead. The mapping is:

=========================  ==================================  ============================
Notes symbol               Cells                               Meaning
=========================  ==================================  ============================
(none)                     model_point()                       The selected model point row
x                          age_at_entry()                      가입나이 at issue, 보험나이
x + t//12                  age(t)                              Attained age in month t
(none)                     policy_year(t)                      1-based policy year label
omega                      omega_age()                         Terminal age of the table
T_y                        proj_years()                        Number of projected years
T                          proj_len()                          Number of projected months
m                          prem_term(), prem_period()          납입기간, in years
12m                        prem_period_mths()                  납입기간, in months
(none)                     prem_end()                          Number of years a premium is due
n_CI                       ci_cover_end()                      Months of CI cover
SA                         sum_assured()                       보험가입금액
G                          premium_pp()                        Annual gross premium
G^m                        premium_mth_pp()                    Monthly gross premium
P^m                        prem_net_level_mth_pp()             Monthly net level premium
P                          prem_net_level_pp()                 12 x the monthly one
i                          prem_int_rate                       예정이율, per annum
j                          prem_int_rate_mth()                 Its monthly equivalent
a                          accel_rate()                        선지급 비율
r = 1 - a                  resid_rate()                        Residual death fraction
c                          resid_floor_mult()                  계약자적립금 floor multiple
f                          first_year_factor                   First-year 감액 factor
k                          cv_floor_ratio()                    저해지 suppression factor
q(t)                       mort_rate(t)                        Pre-CI death rate, annual
q^m(t)                     mort_rate_mth(t)                    Pre-CI death decrement
q'(t)                      mort_rate_ci(t)                     Post-CI death rate, annual
q'^m(t)                    mort_rate_ci_mth(t)                 Post-CI death decrement
(table q)                  mort_rate_at_age(y)                 Table rate at attained age y
(none)                     mort_rate_base(t)                   Pricing-basis rate, annual
(none)                     mort_rate_base_mth(t)               Pricing-basis rate, monthly
q_ci(t)                    ci_rate(t)                          The CI rate, annual
q_ci^m(t)                  ci_rate_mth(t)                      The CI decrement
(none)                     ci_rate_base(t)                     Pricing-basis CI rate
(none)                     ci_rate_mth_base(t)                 Pricing-basis CI, monthly
(by cause)                 ci_rate_at_age(y, cause)            Table rate by cause
(none)                     ci_wait_factor_mth(t)               90-day 보장개시일, by month
w(t)                       lapse_rate(t)                       Pre-CI surrender rate, annual
w^m(t)                     lapse_rate_mth(t)                   Pre-CI surrender decrement
w'(t)                      lapse_rate_ci(t)                    Post-CI surrender, annual
w'^m(t)                    lapse_rate_ci_mth(t)                Post-CI surrender decrement
(none)                     disc_factor()                       1 / (1 + i)
v^m                        disc_factor_mth()                   1 / (1 + j)
A1(t)                      epv_resid(t)                        EPV of the residual, post-CI
A0(t)                      epv_ben(t)                          EPV of all benefits, pre-CI
a-double-dot(t)            annuity_due(t)                      EPV of 1 p.a. while pre-CI
V(t)                       pol_val_pp(t)                       계약자적립액 at month-end t
cumprem(t)                 cum_prem_pp(t)                      Premiums paid by month-end t
B(t)                       base_benefit_pp(t)                  기본보험금 at month-end t
SC_max                     surr_chg_cap_pp()                   표준해약공제액
SC(t)                      surr_chg_pp(t)                      해약공제액 at month-end t
W(t)                       cv_std_pp(t)                        표준형 twin's 해약환급금 at t
CV(t)                      cv_pp(t)                            Payable value at t, pre-CI
CV'(t)                     cv_pp_ci(t)                         Payable value at t, post-CI
(none)                     cv_mult(t)                          k or 1, by month-end
a B(s)                     accel_benefit_pp(s)                 The 선지급 of cohort s
r B(s)                     resid_nominal_pp(s)                 Nominal residual of cohort s
max(rB, cV)                resid_db_pp(t, s)                   Residual death benefit at t
(sum)                      resid_db_total_pp(t)                Count x payable residual
(sum)                      resid_nom_total_pp(t)               Count x nominal residual
(weighted mean)            resid_db_avg_pp(t)                  In-force mean residual, month t
L(t)                       loan_pp(t)                          보험계약대출 balance at time t
i_L                        i_loan                              보험계약대출이율, per annum
j_L                        i_loan_mth()                        Its monthly equivalent
Delta(t)                   pol_loan_draw(t)                    Draw at month-end t
(available)                loan_avail_pp(t)                    Loan limit at t, pre-CI
(available)                loan_avail_ci_pp(t)                 Loan limit at t, post-CI
l(t)                       pols_if(t)                          In force, start of month t
l0(t)                      pols_if_pre(t)                      In force and pre-CI
l1(t)                      pols_if_ci(t)                       In force and post-CI
l1(t, s)                   pols_if_ci_at(t, s)                 Post-CI, by cohort s
(survivorship)             ci_surv(t)                          Post-CI survival to month t
lp(t)                      pols_if_pay(t)                      In force and paying
(waived)                   pols_waived(t)                      Waived on 장해 50%+
C(t)                       pols_ci(t)                          CI accelerations in month t
C(t, s)                    pols_ci_in(t, s)                    Entrants into cohort s
(entrants)                 ci_cohort_entrants(s)               Cohort s at its entry month
D(t)                       pols_death(t)                       Pre-CI deaths in month t
D'(t)                      pols_death_ci(t)                    Post-CI deaths in month t
S(t)                       pols_lapse(t)                       Pre-CI surrenders
S'(t)                      pols_lapse_ci(t)                    Post-CI surrenders
G^m lp(t)                  premiums(t)                         Premium income
(by kind)                  claims(t, kind)                     Benefit outgo by kind
ec                         claim_expenses(t)                   Claim expense
E0, e(t)                   expenses(t)                         Acquisition and maintenance
c0, c_r                    commissions(t)                      Commission outgo
CF(t)                      net_cf(t)                           Net cash flow, income positive
=========================  ==================================  ============================

.. rubric:: The acceleration, in one paragraph

On the first qualifying event the insurer pays ``a B(s)`` at the month-end ``s`` that
closes the month of the event, the contract does **not** terminate, the death benefit
becomes ``max(r B(s), c V(k))`` at every later month-end ``k``, and the premium stops. The contract's survival is a regulatory requirement and not a design
choice: 감독규정 제7-60조제8호 forbids a contract to be extinguished while the risk it
covers remains effective [REG-R16]. **The complement is exact** — ``a + r = 1``, and
:func:`check_accel_complement` asserts it cohort by cohort — so the acceleration
redistributes one sum assured across two dates and never adds cover.

.. rubric:: Two cohorts, and why the post-CI one is indexed by its entry month

:func:`pols_if_pre` and :func:`pols_if_ci` are the two states, and the second is carried
**by the month-end at which it accelerated**, :func:`pols_if_ci_at`; a life accelerating
in month ``t`` is paid at month-end ``t + 1`` and carries the label ``s = t + 1``. That
is not tidiness: the
residual a post-CI policy carries was fixed at its own acceleration date, at ``r`` times
the 기본보험금 *then*, and the 기본보험금 grows with the account and with the premiums
paid. Collapsing the cohorts
to one average residual would let a policy that accelerated at duration 3 inherit the
larger residual of one that accelerated at duration 40. 「지급사유 발생 당시」 is a date,
and on this grid it is a month rather than a policy year.

The **negative** labels are the first-year 감액 cohorts: a breast-cancer claim in the first
policy year, ``t = 0 … 11``, is paid ``a f B(t + 1)`` with ``f = 0.5`` and leaves a residual
of ``(1 - a f) B(t + 1)``, a different amount from the full-benefit cohort formed in the
same month. Its label is ``-(t + 1)``, which is available precisely because no acceleration
can be paid at month-end 0 and no full claim ever carries a negative label. The first two
are empty, because no 중대한 암 is covered before the 보장개시일. Where the model point
sets ``first_year_scope`` to ``all``, the whole of the first policy year's accelerations go
into them, which is the GI-generation design.

**The cohort dimension is twelve times longer than the annual grid's**, so the aggregates
the cash flow actually needs are carried as their own recursions — :func:`pols_if_ci`,
:func:`resid_nom_total_pp` and :func:`resid_db_total_pp` — rather than rebuilt by summing
the cohort table in every month. Every post-CI cohort runs the same two decrements, so
those aggregates are exact; the cohort loop survives inside
:func:`resid_db_total_pp` for the months in which the 105% account floor sits between the
smallest and the largest nominal residual, which is where a closed form is not available
and which is a window of a year or two on every shipped point.

.. rubric:: Processing order

Within month ``t``, in this order **[std order]**: premium, acquisition expense,
maintenance expense and commission at the start of the month; then the CI transition;
then death among those who did not accelerate; then surrender among those who neither
accelerated nor died. A life accelerating in month ``t`` receives ``a B(t + 1)`` at the end
of month ``t`` — month-end ``t + 1`` — and joins the post-CI cohort at the start of month
``t + 1``, so it is not exposed to the residual death benefit until the following month.
That one-month lag is the monthly grid's version of what was a one-**year** lag, and the
correction is material: the post-CI cohort is now exposed to its own mortality from the
month after the claim rather than from the next 계약해당일, and the post-CI in-force at the
twentieth 계약해당일 is 1.1% lower than the annual-step model reported for that reason. The
lag is still deliberate and conservative in the right direction: the 장해분류표 defers
assessment of a 중대한 뇌졸중 for **twelve months** after onset [S1 별표3], so a CI claim
and the death that may follow it are not simultaneous events on any grid.

.. rubric:: One policy value, three surrender values

There is a single ``V(t)`` in this model, :func:`pol_val_pp`, the 계약자적립액 of the
**표준형 twin** — the non-marketed comparison contract — at anniversary ``t``. The
해약환급금 is ``W(t) = max(0, V(t) - SC(t))`` and the amount actually payable is a
multiplier on it:

* ``cv_pp(t) = k W(t)`` for a pre-CI policy inside the 납입기간, ``W(t)`` after it;
* ``cv_pp_ci(t) = W(t)`` for a post-CI policy at **every** duration.

All four are on the month-end clock, so a surrender arising in month ``t`` — paid at the
end of it — is paid ``cv_pp(t + 1)``.

**The suppression therefore has two exits, not one: 납입완료 and a CI/LTC 지급사유.** The
second is contractual — [S2] conditions the suppression on 「CI/LTC보험금 지급사유가
발생하지 않은 경우」 and [S4] on 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」 —
and it is the CI-specific delta on the chassis, whose cliff is a deterministic function of
duration. Here it is at ``min(m, t_CI)``, a **random** date correlated with the product's
own decrement. :func:`check_cv_carve_out` asserts the consequence the carve-out exists to
produce: a CI claimant is never worse off on surrender than an unaccelerated policyholder
at the same duration.

The same carve-out **doubles the policy loan** at the acceleration date, because the loan
is computed off the payable value: compare :func:`loan_avail_pp` with
:func:`loan_avail_ci_pp` at any duration inside the 납입기간.

.. rubric:: The pricing basis, and what it deliberately leaves out

:func:`pol_val_pp` is a prospective net level premium reserve on the 예정이율 and the
shipped tables, solved from :func:`epv_ben` and :func:`annuity_due` and asserted by
:func:`check_pol_val_roll_fwd`. Two simplifications are **[std]** and are stated rather
than hidden. The pricing recursion values benefits at ``SA`` and the residual at
``r SA``, ignoring both floors on the 기본보험금 and the 105% floor under the residual;
pricing the second one in would make ``V`` self-referential, since the floor is a multiple
of ``V`` itself. And the reserve is computed on the **pricing** decrements, not the
best-estimate ones, which is what makes the identity testable at all. The floors are
benefit-payment rules and are applied in full in the cash-flow projection, where
:func:`check_resid_floor` asserts them.

The gross premium is a model point input. On the anchor cell it is **sourced**: ₩306,740
a month is published for exactly that cell, the model point column carries twelve times it,
and :func:`premium_mth_pp` divides it back — so the monthly grid collects the published
rate itself and no modal loading is invented in either direction. On the other cells it is
the annual-step model's own ``prem_net_level_pp()`` grossed up
by the loading the anchor implies, times the published 저해지-to-기본환급형 form factor
**[std]**. The relativity that falls out is a check rather than an input: the model prices
the 80% form at 1.079 times the 50% form at male 40, against the 1.085 [S4] publishes.

.. rubric:: 예정위험률 are not a best estimate

``mort_be_factor`` and ``ci_be_factor`` are 1.00 on every model point but one, so the base
run is a **valuation-basis run**. [S3]'s rates are 예정위험률 carrying a 안전할증 whose
regulatory cap was 30% in the early 2000s, 50% from 2015 and removed in 2017 [R1]; no
retrieved source sizes the margin against current Korean insured experience, so any
best-estimate basis derived from them is a standardization and model point 9 is where it
is exercised.

.. rubric:: Modules that are off in the base run

* **보험계약대출**, ``pol_loan_util`` at 0, drawn on model point 7 at duration 12 — the
  계약해당일 ``d = 144``, inside the 납입기간, so the suppressed base binds and the doubling
  at a CI event is visible.
* **The 표준형 lapse basis**, ``lapse_basis`` at ``table``. The suppressed forms run the
  **로그-선형 원칙모형** of the IFRS17 주요 계리가정 가이드라인 instead, converging to
  0.1% at 납입완료 with a 0.8% post-완납 ultimate [REG-R27]. No separate 완납 surrender
  spike is imposed: the eightfold step at 납입완료 is produced by the guideline's own
  shape.
* **The all-trigger first-year 감액**, ``first_year_scope`` at ``all``, on model point 4.
* **The best-estimate levers**, on model point 9, which also carries the 110% residual
  floor multiple [S3] publishes instead of 105%.

.. rubric:: What is not modelled, and is named so that it is not mistaken for absent

중도인출 and 추가납입 are arguments of the 기본보험금 definition [S1 별표1 주7] and are
held at **zero** rather than dropped. 부활 and the 90-day 중대한 암 보장개시일 it restarts,
the 예정위험률 revision right that takes effect as a **benefit reduction** rather than a
lapse, the 가지급제도, 감액, 연금전환 (which appears in no retrieved CI 약관) and the
multi-pay CI generation are all outside this model. So is any 요구자본: the projection
produces gross liability cash flows and leaves the 책임준비금, the IFRS 17 CSM and the
K-ICS 장해ㆍ질병위험액 to a layer that consumes them.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — premiums less claims, expenses and commission —
which is the notes' own sign and the library-wide one, so there is no outgo-positive
``liability_cf`` companion to publish.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def sex():
    """The sex of the insured, M or F; the two are rated and tabulated separately.

    The sex effect on this product runs in **opposite directions** on price and on
    incidence, and a reader must not infer one from the other.  Female premium is
    0.808-0.872 of male across the published grid [S4], while at age 40 the three headline CI
    rates sum to 1.10 times the male ones [S3] — the excess being breast and thyroid
    cancer, which is exactly the exposure that broke the 2002 pricing [R1].  The
    reconciliation is that the premium is dominated by the death benefit, by old-age CI
    incidence where the female rates are far below the male ones, and by the savings
    element, which is sex-neutral.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def age_at_entry():
    """x: the 가입나이 at issue on **보험나이**, 15 to 60.

    보험나이 (*boheom nai*, insurance age) is 만나이 at the 계약일 with a fraction under
    six months discarded and six months or more rounded up, incrementing on each
    계약해당일 [S1 제26조] [REG-R25 제21조].  The 15-60 envelope is invariant across every
    CI source retrieved [S3] [S4] [R13] and is five years below the whole life chassis's
    15-65 ceiling.
    """
    return int(model_point()["issue_age"])


def sum_assured():
    """SA: the 보험가입금액 at issue, level for life.

    The envelope is ₩10,000,000 to ₩200,000,000, and the underwriting cap binds the
    **accelerated** exposure rather than the face amount: [S3] publishes 2,000만-1억
    5,000만원 on the 50% form against 1,000만-9,000만원 on the 80% form, so
    0.5 x 1억5,000만 and 0.8 x 9,000만 are within 4% of each other [S3].  중도인출 and
    추가납입 are held at zero **[std]**, so ``SA`` is also the 기본사망보험금 of
    [S1 별표1 주7].
    """
    return float(model_point()["sum_assured"])


def pols_if_init():
    """The number of policies in force at the start of the first projected year.

    1 on every shipped model point: these are single-policy cells, as everywhere in this
    library.  It is read from the model point rather than hard-coded so that a user can
    project a block by scaling one row.
    """
    return float(model_point()["pols_if_init"])


def prem_term():
    """m: the 납입기간 in years, as entered on the model point.

    20년납 on the anchor, which is the term every published Korean CI rate card and every
    해약환급금 illustration in the source set is quoted on [S3] [S4], and which puts
    납입완료 at attained age 60 — well inside the CI cover period, so the surrender-value
    step and the acceleration can be observed separately.  The menu runs 5 to 30년납 in
    fives and 55 to 80세납, with 5년납 and 10년납 offered on the 기본환급형 only [S4].
    """
    return int(model_point()["prem_term"])


def prem_period():
    """m: the effective 납입기간, and the duration at which the suppression would end.

    Identical to :func:`prem_term` on every shipped point; the cells exists because the
    chassis admits a 종신납 form on which the suppressed period runs for life, and a model
    reading ``prem_term`` directly would silently mis-place the step if one were added.
    """
    return prem_term() if prem_term() > 0 else proj_years()


def prem_period_mths():
    """12 m: the 납입기간 in **months**, the unit the monthly grid steps in.

    The paying months are ``t = 0 … prem_period_mths() - 1`` and 납입완료 falls at the
    계약해당일 ``d = prem_period_mths()``.  The 납입기간 itself is a contractual term quoted
    in **years** and did not change when the grid did: this cells multiplies it out and is
    the only place the projection needs the product.
    """
    return 12 * prem_period()


def prem_end():
    """The **number** of policy years in which a premium is actually due.

    ``prem_period()``, so the paying months are ``t = 0 … prem_period_mths() - 1`` and
    납입완료 falls at the 계약해당일 ``d = prem_period_mths()``.  Nothing else about the
    contract stops there: maintenance expense,
    death cover, CI cover to 100세 and the account value all continue, which is the
    structural point of a whole-life chassis and the reason a projection truncated at
    납입완료 misses the majority of the liability.
    """
    return prem_period()


def premium_pp():
    """G: the level annual gross premium per policy, payable in advance in years 0 to m - 1.

    Level and guaranteed for the whole of 납입기간, subject only to the statutory
    예정위험률 revision right from five years — which, where it bites, is applied by
    **reducing the benefit or the sum assured** rather than by raising the premium [S3],
    so its exercise would show up as benefit erosion and not as a decrement.  There is no
    renewal mechanic on the main contract.

    On the anchor cell the value is **sourced**: ₩306,740 a month is published for 남 40,
    80% 선지급형, 17대보장형, 해지환급금이 적은 유형, 1억원, 20년납, 월납, net of the
    고액계약할인, and the annual figure is twelve times it **[std]** — no carrier publishes
    an annual-mode scale, so the modal discount a real 연납 rate would carry is not applied
    and the annual premium is slightly overstated [S4].  On the other cells it is this
    model's own :func:`prem_net_level_pp` grossed up by the 1.2400 loading the anchor
    implies, times the 저해지-to-기본환급형 form factor of 1.10224 published for one
    identical cell [S4], with 0.937 for the 무해지 form **[std]**.
    """
    return float(model_point()["premium_annual"])


def premium_mth_pp():
    """G^m: the level **monthly** gross premium, the instalment the projection collects.

    ``premium_pp() / 12``, which on the anchor cell returns the published ₩306,740 a month
    exactly — the figure the model point column was built from as twelve times it [S4].
    The annual column survives because a Korean commission scale and a 보험료지수 are
    written in annual units and :func:`commissions` reads it; the monthly grid collects
    this.  No modal loading is applied in either direction **[std]**: no carrier publishes
    an annual-mode scale, so the division returns the published monthly rate and invents
    nothing.
    """
    return premium_pp() / 12.0


def accel_rate():
    """a: the 선지급 비율, the fraction of the 기본보험금 the CI benefit pays.

    0.80 on the composite, 0.50 as a model point flag; both appear together in every
    complete 약관 retrieved [S1] [S2] [S3] [S4] [S5] [S6].  **Paid once only across the
    whole trigger set** — eight 중대한 질병, four 중대한 수술, 중대한 화상 및 부식 and
    장기요양상태 — so ``ci_rate`` is a first-event rate and not a sum of marginal
    incidences [S1 별표1] [R1].

    80% is the composite's choice for three reasons stated in ``product-spec.md``, of
    which the modelling one is that the residual's 105%-of-account floor actually binds
    inside a normal projection on this form: at the anchor cell ``r SA`` is ₩20,000,000
    and the floor takes over as soon as ``V(t)`` passes ₩19,050,000.  On the 50% form the
    same test needs ₩47,600,000 and is reached far later.  The 100% 선지급플러스형 is
    excluded because it is not a pure acceleration: it extinguishes the death benefit and
    replaces it with a separately funded 유족위로금 [S4].
    """
    a = float(model_point()["accel_rate"])
    if not 0.0 < a < 1.0:
        raise ValueError("accel_rate must lie strictly between 0 and 1")
    return a


def resid_rate():
    """r = 1 - a: the residual death fraction, the exact complement of the acceleration.

    ``80 + 20 = 100`` and ``40 + 60 = 100`` exactly [S1] [S2].  **The acceleration never
    adds cover**, and keeping ``r`` as the arithmetic complement rather than as a second
    model point column is what makes that unfalsifiable here;
    :func:`check_accel_complement` asserts it against the 기본보험금 cohort by cohort.
    """
    return 1.0 - accel_rate()


def resid_floor_mult():
    """c: the 계약자적립금 multiple flooring the post-CI death benefit.

    1.05 at [S1 별표1 주8], 1.10 at [S3]'s older universal version of the same product, so
    it is a carrier and vintage parameter and is carried as one rather than hard-coded.
    The clause reads 「CI/LTC보험금 지급사유 발생당시의 기본보험금의 20%와 … 계약자적립금의
    105% 중 큰 금액」, which is why the residual is a **growing** quantity and not the
    stated complement: on a long-surviving post-CI policy the account overtakes the nominal
    and the floor becomes the benefit.
    """
    return float(model_point()["resid_floor_mult"])


def cv_floor_ratio():
    """k: the 저해지환급형 suppression factor applied to the 표준형 twin's 해약환급금.

    1.00 표준형 / 기본환급형, 0.50 저해지환급형, 0.00 무해지환급형.  [S2] states both
    grades it offers in terms — 「'30% 저해지환급형'의 경우 '기본형' 해지환급금의 30%…
    '50% 저해지환급형'의 경우 … 50%」 — and 0.50 is taken because it is the modal fraction
    on the chassis and one of the two grades this carrier offers on the CI product itself
    **[std]**.  [S4] rebrands the same mechanic as 해지환급금이 적은 유형 and prices it
    9-12% below the 기본환급형.

    The suppression is a **regulatory dispensation** rather than a contractual gimmick:
    감독규정 제7-66조제4항 permits an insurer to pay less than the 별표-14 floor only where
    the premium was calculated on a 최적해지율, which is why the lapse assumption on this
    product is a supervisory matter [REG-R19] [REG-R27].
    """
    k = float(model_point()["cv_floor_ratio"])
    if not 0.0 <= k <= 1.0:
        raise ValueError("invalid cv_floor_ratio")
    return k


def first_year_scope():
    """The scope of the first-year 감액: ``breast`` (the composite) or ``all``.

    Two designs are in the sources and they differ in **scope, not in depth** — both
    halve.  [S1] and [S2] reduce only for breast cancer and only in the first policy year,
    so an 80% form pays 40% and the death benefit's complement rises to 60% [S1 별표1]
    [S2 별표1].  [S4]'s GI product halves **every** trigger in the first year, carving back
    only a 중대한 화상 및 부식 claim on the 17대보장형 [S4].

    The composite takes the breast-cancer design because it is the CI-generation design in
    both complete 약관 retrieved and because it is the only one with an identifiable
    experience rationale: it is the lineal descendant of the 180-day breast-cancer 부담보
    imposed across the market from 2008 after the female claim excess of 2003-2005 [R1].
    The modelling consequence is real — it requires the 중대한 암 incidence to be split
    into a breast component and the rest, which :func:`breast_share` supplies.
    """
    v = model_point()["first_year_scope"]
    if v not in ("breast", "all"):
        raise ValueError("invalid first_year_scope")
    return v


def breast_share():
    """The share of 중대한 암 incidence attributable to breast cancer **[std]**.

    0.268 for females and 0.005 for males, calibrated on the national cancer registry
    [REG-R40]: 유방 29,871 cases in 2023 against female cases of 137,487 less the 19.0%
    of the female burden that is 갑상선, which 중대한 암 excludes as C73 — so
    29,871 / 111,364 = 0.268.  Male breast cancer is under 1% of breast cases and is
    carried at 0.005 rather than nil so that the male first-year 감액 is present and
    negligible rather than absent and unexplained.

    The registry publishes incidence on **만나이** while this model runs on 보험나이; the
    quantity used here is a *share* of one age's incidence, which is first-order
    insensitive to the half-year shift, and no adjustment is made **[std]**.
    """
    return breast_share_f if sex() == "F" else breast_share_m        # noqa: F821


def lapse_basis():
    """The surrender basis: ``log_linear`` (the 원칙모형) or ``table`` (the 표준형 curve).

    The IFRS17 주요 계리가정 가이드라인 of 2024-11-07 adopts a **로그-선형 모형** as the
    원칙모형 for 무·저해지 lapse rates, converging to 0.1% at 납입완료 with a 0.8%
    post-완납 ultimate; departure is permitted only on disclosure, against the principle
    model, of the CSM, best-estimate liability, K-ICS and net-income differences
    [REG-R27] [R3].  The suppressed model points run it; the 기본환급형 points run the
    표준형 duration curve in ``lapse_table.csv``.  **Carrying both is the comparison the
    guideline requires an insurer to disclose**, and it is the reason the table survives
    on a product whose representative form does not use it.

    The problem the supervisor named bites here with particular force: with no experience
    on 무·저해지 business, insurers assumed high lapse right up to 완납, which flatters
    profitability, and the resulting switching raised observed 표준형 lapse, which was fed
    back into the 무해지 assumption — 「악순환」 [REG-R27].
    """
    v = model_point()["lapse_basis"]
    if v not in ("log_linear", "table"):
        raise ValueError("invalid lapse_basis")
    return v


def mort_be_factor():
    """The multiplier turning the shipped valuation mortality into the projection basis.

    1.00 on every model point but 9, so the base run is a **valuation-basis run and not a
    best estimate**: [S3]'s rates are 예정위험률 carrying a 안전할증 whose regulatory cap
    was 30% in the early 2000s, 50% from the 2015 로드맵 and removed from 2017, and no
    retrieved source sizes the margin against current Korean insured experience [R1].
    Claims move proportionately with it; the terminal rate is held at 1 whatever it is set
    to, because ``omega_age`` is the horizon of the table and a structural property of the
    projection rather than an experience assumption.
    """
    return float(model_point()["mort_adj"])


def ci_be_factor():
    """The same lever on the CI decrement; 1.00 on every model point but 9 **[std]**.

    Held apart from :func:`mort_be_factor` because the two margins are not the same size
    and there is no reason to move them together: the mortality basis is a life table and
    the CI basis is a morbidity table built on six disclosed numbers, and the second is by
    far the weaker of the two.  0.75 on model point 9, removing a quarter of the rate as a
    stated **[std]** unwinding of the 안전할증 [R1].
    """
    return float(model_point()["ci_adj"])


def mort_ci_factor():
    """The multiplier on mortality after a CI event **[std]**; 3.00 in the base run.

    **The CI and death decrements are not independent competing risks**, and the product
    is built on the fact that they are not.  There is no survival period anywhere in a
    Korean CI contract — the supervisor refused the overseas 30-day requirement on
    consumer-protection grounds, holding that requiring survival would create disputes
    where the insured died [R1] — so the CI rate already includes lives who die of the CI
    cause, and a fraction of what would be a death claim on an ordinary 종신보험 is a CI
    claim here followed shortly by a residual death claim.

    No Korean post-CI mortality is published.  3.00 is a standardization whose rationale
    is the registry's own survival data: five-year relative survival across all cancers
    excluding thyroid is 69.6% against a general population at 100% by construction
    [REG-R40], and the CI trigger set is deliberately the severe tail of each disease.
    It is a model point column so that the sensitivity can be read directly, and model
    point 9 runs it at 2.00.
    """
    return float(model_point()["mort_ci_factor"])


def waiver_rate(t):
    """The **annual** 납입면제 rate on the **장해 50%+** limb alone **[std]**.

    [S1] waives all future 기본보험료 on either a 장해지급률 of 50% or more from one
    accident or one non-accidental cause, **or** any CI/LTC 지급사유 [S1 별표1 주4].
    Because the second limb fires with essentially every CI claim, the waiver is **not an
    independent decrement on the CI limb** and is not modelled as one: it is implicit in
    the post-CI cohort, which pays no premium at all.  What is left is the first limb, a
    real if second-order decrement on the same 장해분류표 percentage scale the chassis uses
    [REG-R25].

    0.03% a year during the 납입기간 on every shipped point but 9, which runs 0.05%
    **[std]**; no Korean disability inception rate at the 50% 장해지급률 threshold is
    published.  A waived policy stays pre-CI, keeps its full death cover
    and — the chassis's **"waived premiums count as paid"** rule — continues to accrue
    surrender value on the full premium scale, so the waiver is the only route to the
    저해지 step without funding it.  Zero once no premium is due, that is from
    ``t = prem_period_mths()``.  Its monthly companion is :func:`waiver_rate_mth`.
    """
    if t < 0 or t >= prem_period_mths():
        return 0.0
    return float(model_point()["waiver_rate"])


def pol_loan_util():
    """The fraction of the available 보험계약대출 drawn; 0 in the base run **[std]**.

    There is no public Korean take-up data of any kind, so the level is a model point
    input and the contractual limit in :func:`loan_avail_pp` binds it whatever it is set
    to.  Model point 7 draws half the available amount at duration 12, inside the
    납입기간, where the base is the **suppressed** value — which is the configuration in
    which the CI carve-out's doubling of the limit is visible.
    """
    return float(model_point()["pol_loan_util"])


def pol_loan_year():
    """The **anniversary** at which the 보험계약대출 is drawn; 0 for no draw.

    An elapsed count of completed policy years — duration 12 on model point 7 — and so
    already 0-based: it is a point on the anniversary clock, not an index into the frame,
    and it did not move when the frame did.
    """
    return int(model_point()["pol_loan_year"])


def omega_age():
    """omega: the terminal age of the mortality table, the first age at which q = 1.

    110 on the shipped construction, for both sexes **[std]**.  The 제10회 경험생명표's
    terminal age is not published — 보험개발원 releases only 평균수명 and 기대여명
    [REG-R33] [REG-R34] — so the horizon is a stated property of the constructed table and
    not a transcription.  It is a hard model parameter and not a rounding: projecting a
    whole-life contract to 100 truncates the liability and projecting to 120 invents one.
    """
    tbl = data.mort_table().loc[sex()]                               # noqa: F821
    return int(tbl.index[tbl["mort_rate"] >= 1.0][0])


def proj_years():
    """T_y = omega - x + 1: the **number** of projected policy years.

    The contract's own clock.  The projection steps in months and carries ``12 T_y`` of
    them; this cells is what every quantity quoted in policy years — the 납입기간, the
    해약공제기간, the CI cover period — is measured against.
    """
    return omega_age() - age_at_entry() + 1


def proj_len():
    """T = 12 T_y: the **number** of projected policy **months**.

    The frame's exclusive end, not its last index: :func:`result_cf` carries ``proj_len()``
    rows indexed ``0 … proj_len() - 1`` and the frame is ``range(proj_len())``, twelve rows
    to a policy year.

    There is no maturity date and no 만기보험금, so the horizon is the table's and not the
    contract's.  Every remaining life dies in the last policy **year** — the table's rate is
    1 there and :func:`mort_rate_mth` spreads that certain death evenly over its twelve
    months — and ``pols_if(T)`` is zero; there are no tail states.  **CI cover ends
    earlier**, at the 100세 계약해당일 — see :func:`ci_cover_end` — so the projection carries
    a long stretch on which the death benefit is the only cover left.
    """
    return 12 * proj_years()


def policy_year(t):
    """The contractual, 1-based policy year label of month t: ``t // 12 + 1``.

    Derived and never indexed by.  The 계약해당일 closing policy year ``y`` is the month-end
    ``d = 12 y``, and everything the contract quotes in policy years — the 납입기간, the
    해약공제기간, the lapse table's rows, the CI cover period — is read through this.
    """
    return t // 12 + 1


def age(t):
    """x + t // 12: the attained 보험나이 in month t, which is 0-based.

    보험나이 increments on the **계약해당일** and not on the birthday [REG-R25 제21조], so
    the floor division is exact rather than an approximation: one table rate holds for the
    twelve months of a policy year, which is what the contract says.
    """
    return age_at_entry() + t // 12


def ci_cover_end():
    """n_CI: the **number** of policy months in which the CI benefit is covered.

    The death benefit is 종신 but **CI/LTC cover ends at the 100세 계약해당일**, so the
    last covered month is ``t = n_CI - 1`` and ``n_CI = 12 (100 - x)``.  This
    is the post-2008 design and is the one a contract written today has: the 2002 product
    put the acceleration inside a 제1보험기간 running to the 80세 계약해당일 and paid 100%
    of the death benefit thereafter [S6] [R1], and that legacy split is named in
    ``product-spec.md`` and deliberately not modelled, because a second discontinuity at
    80 would collide with the 저해지 step in any model point trying to isolate either.
    """
    return 12 * max(0, ci_cover_end_age - age_at_entry())            # noqa: F821


def mort_rate_at_age(y):
    """The shipped table's mortality rate at attained age y, before any adjustment.

    Read from ``mort_table.csv``, a **[std]** construction anchored on the 예정 경험
    사망률 one Korean CI 상품요약서 discloses at ages 20, 40 and 60 [S3]; see
    :mod:`~.CI_KR_S.Data`.  This is the rate the pricing recursions use unadjusted:
    ``mort_be_factor`` is a lever on the *decrement*, not a change to the 산출방법서 basis.
    """
    return float(data.mort_table().loc[(sex(), y), "mort_rate"])     # noqa: F821


def mort_rate_base(t):
    """The **annual** pricing-basis mortality rate in month t, at attained age ``age(t)``.

    One table rate holds for the twelve months of a policy year, because 보험나이 steps on
    the 계약해당일.
    """
    return mort_rate_at_age(age(t))


def mort_rate_base_mth(t):
    """The monthly pricing-basis mortality rate in month t.

    ``1 - (1 - q)^(1/12)`` on :func:`mort_rate_base`, so twelve months compound back to
    exactly the year's tabulated rate, and ``1 / (12 - t mod 12)`` in the terminal policy
    year where ``q = 1`` — see :func:`mort_rate_mth` for why.
    """
    q = mort_rate_base(t)
    if q >= 1.0:
        return 1.0 / (12 - t % 12)
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def mort_rate(t):
    """q(t): the **annual** death rate of the **pre-CI** cohort in the policy year of t.

    The table rate times :func:`mort_be_factor`, capped at 1 and held at 1 at the table's
    terminal age whatever the factor is set to.  This is the rate the sources tabulate;
    what the roll-forward applies is :func:`mort_rate_mth`.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate_base(t) * mort_be_factor())


def mort_rate_mth(t):
    """q^m(t): the death decrement applied to the **pre-CI** cohort in month t.

    ``1 - (1 - q(t))^(1/12)`` **[std]**, the uniform-force conversion, so that the twelve
    months of a policy year compound back to exactly the annual rate the table holds.
    Dividing by twelve would not, and on a rate that rises by two orders of magnitude
    across the horizon the difference is not a rounding.

    At the table's terminal age ``q = 1`` and no compounding is available: the conversion
    would kill the whole surviving cohort in the first month and leave eleven empty rows.
    The certain death is therefore spread **uniformly** over the year as ``1 / (12 - j)``
    in its ``j``-th month, which is the UDD convention and closes the table exactly.
    """
    q = mort_rate(t)
    if q >= 1.0:
        return 1.0 / (12 - t % 12)
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def mort_rate_ci_base(t):
    """The **annual** pricing-basis mortality of a **post-CI** life in the policy year of t.

    The table rate times :func:`mort_ci_factor`.  It is what :func:`epv_resid` values the
    residual on, so the reserve carries the same excess mortality the projection does; a
    pricing basis that valued the residual on ordinary mortality would hold too little
    against it.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate_base(t) * mort_ci_factor())


def mort_rate_ci_base_mth(t):
    """The monthly pricing-basis mortality of a post-CI life in month t.

    ``1 - (1 - q')^(1/12)``, and the terminal-year UDD spread of :func:`mort_rate_mth`.
    """
    q = mort_rate_ci_base(t)
    if q >= 1.0:
        return 1.0 / (12 - t % 12)
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def mort_rate_ci(t):
    """q'(t): the **annual** death rate of the **post-CI** cohort in the policy year of t.

    :func:`mort_rate` times :func:`mort_ci_factor`, capped at 1.  The post-CI cohort is
    the only place in this model where the correlation between the two decrements appears
    as a number, and it is the reason the residual death benefit is paid earlier than an
    ordinary 종신보험's would be.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate(t) * mort_ci_factor())


def mort_rate_ci_mth(t):
    """q'^m(t): the death decrement applied to the **post-CI** cohort in month t.

    ``1 - (1 - q'(t))^(1/12)`` **[std]**, with the terminal-year UDD spread of
    :func:`mort_rate_mth`.  **The excess mortality is applied to the annual probability and
    then converted, not to the converted one**: a factor of three on a monthly force is not
    a factor of three on the year, and the 3.00 that stands behind this number is a
    statement about a year's survival [REG-R40].
    """
    q = mort_rate_ci(t)
    if q >= 1.0:
        return 1.0 / (12 - t % 12)
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def ci_rate_at_age(y, cause):
    """The shipped incidence rate at attained age y for one of the five modelled causes.

    ``cancer``, ``ami`` and ``stroke`` are 중대한 암, 중대한 급성심근경색증 and 중대한
    뇌졸중, sourced at ages 20, 40 and 60 [S3] and constructed elsewhere; ``other`` covers
    the five remaining 중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식; ``ltc``
    is 장기요양상태 on 노인장기요양 1·2등급.  See :mod:`~.CI_KR_S.Data` for what each rests
    on.  Zero above the last tabulated age.
    """
    if y > ci_cover_end_age:                                         # noqa: F821
        return 0.0
    return float(data.ci_incidence_table().loc[                      # noqa: F821
        (sex(), y, cause), "ci_rate"])


def ci_wait_factor():
    """The first-year proration for the 90-day 보장개시일 **[std]**.

    ``1 - 90/365 = 0.7534``.  The 중대한 암 보장개시일 is 「계약일(부활일)부터 그 날을
    포함하여 90일이 지난날의 다음날」 [S1 제7조] [S1 별표1 주1] and is **invariant across
    every document retrieved** [S1] [S2] [S3] [S4]; 장기요양상태 carries the same 90 days,
    waived where the state arises directly from a 재해 [S1 별표1 주2].  Everything else —
    the other seven 중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식 — is covered
    **from the 계약일** with no waiting period at all [S1] [S2 별표1 주1].

    ``1 - 90/365`` is the **first policy year's** aggregate exposure for the two causes
    that carry the wait, and it is what the twelve monthly factors of
    :func:`ci_wait_factor_mth` add up to.  It is published because it is the number an
    annual-step model would use for the whole of the first year, and because the two
    figures agreeing is the check that the monthly placement of the wait did not change
    its size.

    Neither form models the two consumer protections that ride on the wait — the right to
    cancel and recover the premiums where 중대한 암 is diagnosed before the 보장개시일, and
    the five-year revival of cover for a pre-inception cancer [S1 제7조⑤⑥].
    """
    return 1.0 - ci_wait_days / 365.0                                # noqa: F821


def ci_wait_factor_mth(t):
    """The fraction of month t that falls **after** the 90-day 보장개시일.

    ``clamp(((t + 1) * 365/12 - 90) / (365/12), 0, 1)`` on a mean month of 365/12 days:
    **zero in months 0 and 1**, 0.0411 in month 2, and 1 from month 3 on.  That is the
    substantive gain of the monthly grid on this decrement — the 보장개시일 is a **date**,
    「계약일(부활일)부터 그 날을 포함하여 90일이 지난날의 다음날」 [S1 제7조] [S1 별표1 주1],
    and an annual grid could only smear it across the whole first year as a 0.7534
    proration on the assumption that incidence is uniform within it.  The monthly grid puts
    the cover where the contract puts it: none for the first two months, a twenty-fifth of
    the third, and all of it thereafter.

    The twelve factors sum to ``12 * (1 - 90/365) = 9.0411`` months of exposure, so the
    first policy year carries exactly the 275 days of cover the contract gives it and the
    conversion moves the wait without resizing it.  The wait is invariant across every
    document retrieved [S1] [S2] [S3] [S4]; 장기요양상태 carries the same 90 days, waived
    where the state arises directly from a 재해 [S1 별표1 주2].  Everything else — the other
    seven 중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식 — is covered **from the
    계약일** with no waiting period at all [S1] [S2 별표1 주1], so this factor is applied to
    the 중대한 암 and 장기요양 limbs only.
    """
    if t < 0:
        return 0.0
    days = 365.0 / 12.0
    return min(1.0, max(0.0, ((t + 1) * days - ci_wait_days) / days))  # noqa: F821


def ci_wait_share(t):
    """The share of the month's tabulated CI incidence that carries the 90-day wait.

    ``(cancer + ltc) / total`` at the attained age of month t — the two causes whose
    보장개시일 is 90 days after the 계약일 [S1 별표1 주1] [S1 별표1 주2], over the five-cause
    first-event total.  Used only to apply :func:`ci_wait_factor_mth` to the part of the
    decrement it belongs to; zero where there is no cover at all.
    """
    if t < 0 or t >= ci_cover_end():
        return 0.0
    y = age(t)
    total = 0.0
    for cause in ("cancer", "ami", "stroke", "other", "ltc"):
        total = total + ci_rate_at_age(y, cause)
    if total <= 0.0:
        return 0.0
    return (ci_rate_at_age(y, "cancer") + ci_rate_at_age(y, "ltc")) / total


def ci_rate_base(t):
    """The **annual** pricing-basis CI decrement of the policy year of month t.

    The five causes summed at the attained age, capped at 1, and **zero from**
    ``t = ci_cover_end()``.  This is the rate the source tabulates, **before** the 90-day
    보장개시일 is applied: the wait is a date inside the first policy year and belongs to
    the monthly rate, :func:`ci_rate_mth_base`, and not to the year's tabulated figure.
    Summing is
    legitimate here only because the shipped rates are themselves first-event rates across
    the competing-risk set: the benefit is payable once only across every trigger
    [S1 별표1], and Korea's supervisor required the overlap between CI causes to be
    reflected in the filed rate rather than ignored for rate stability as overseas practice
    does — 「CI 질병들 간 중복해서 발생할 수 있는 확률을 최대한 반영한 최종 위험률로
    검증받고 사용하였다」 [R1].  A table built by adding published site-specific incidences
    would be wrong in exactly the direction the regulation addresses.
    """
    if t < 0 or t >= ci_cover_end():
        return 0.0
    y = age(t)
    total = 0.0
    for cause in ("cancer", "ami", "stroke", "other", "ltc"):
        total = total + ci_rate_at_age(y, cause)
    return min(1.0, total)


def ci_rate_mth_base(t):
    """The monthly pricing-basis CI decrement in month t, wait applied where it falls.

    ``[1 - (1 - q_ci)^(1/12)]`` on the year's first-event total, so twelve months compound
    back to exactly the tabulated annual rate, times the month's cover factor

        ``1 - (1 - ci_wait_factor_mth(t)) * ci_wait_share(t)``

    which removes the 중대한 암 and 장기요양 limbs from the two months the 보장개시일 has
    not yet passed and 96% of them from the third.  Everything else is covered from the
    계약일 and is never withheld.

    Converting the **summed** first-event rate rather than each cause separately is the
    same choice the annual rate makes and for the same reason: the benefit is payable once
    only across the whole trigger set [S1 별표1] and the filed rate already carries the
    overlap between causes [R1].
    """
    if t < 0 or t >= ci_cover_end():
        return 0.0
    q = ci_rate_base(t)
    if q >= 1.0:
        return 1.0
    mth = 1.0 - (1.0 - q) ** (1.0 / 12.0)
    return mth * (1.0 - (1.0 - ci_wait_factor_mth(t)) * ci_wait_share(t))


def ci_rate(t):
    """q_ci(t): the **annual** CI rate of the policy year of month t.

    :func:`ci_rate_base` times :func:`ci_be_factor`, capped at 1.  **Morbidity dominates
    mortality on this chassis**: on [S3]'s own disclosure the three headline rates sum to
    3.70 times the death rate at male 40 and 6.70 times it at male 60, which is why a
    projection of this product is a morbidity projection with a mortality tail rather than
    the reverse, and why the CI benefit takes about half the risk premium at a 50%
    acceleration despite paying only half the sum assured [S3].
    """
    return min(1.0, ci_rate_base(t) * ci_be_factor())


def ci_rate_mth(t):
    """q_ci^m(t): the CI decrement applied in month t.

    :func:`ci_rate_mth_base` times :func:`ci_be_factor`, capped at 1.  It is zero in the
    first two months of the contract for the 중대한 암 and 장기요양 limbs and positive for
    the rest from the 계약일, which is what the 약관 says and what an annual grid cannot
    express.
    """
    return min(1.0, ci_rate_mth_base(t) * ci_be_factor())


def ci_reduced_share(t):
    """The share of month t's CI claims paid at the reduced first-year rate.

    Zero in every month but the twelve of the **first policy year**, ``t = 0 … 11`` — the
    감액 runs for a policy year and not for a projection step, so the monthly grid carries
    it over twelve rows where the annual grid carried it over one.  Inside that year it is
    1 where ``first_year_scope`` is ``all``, and otherwise the breast-cancer share of that
    **month's** own CI decrement — :func:`breast_share` times the 중대한 암 component after
    the month's 보장개시일 factor, over :func:`ci_rate_mth_base`.  So it is zero in the
    first two months, where no 중대한 암 is covered at all, and the reduced cohorts formed
    there are empty.

    Splitting the decrement rather than averaging the benefit is what lets the two kinds of
    first-year cohort carry different residuals, which they must: a reduced claim leaves
    ``(1 - a f) B(d)`` and a full one leaves ``r B(d)``, both at the month-end ``d`` the
    claim is paid at.
    """
    if t < 0 or t >= 12 or first_year_factor >= 1.0:                 # noqa: F821
        return 0.0
    if first_year_scope() == "all":
        return 1.0
    base = ci_rate_mth_base(t)
    if base <= 0.0:
        return 0.0
    q = ci_rate_base(t)
    if q >= 1.0:
        return 0.0
    y = age(t)
    total = 0.0
    for cause in ("cancer", "ami", "stroke", "other", "ltc"):
        total = total + ci_rate_at_age(y, cause)
    if total <= 0.0:
        return 0.0
    mth = 1.0 - (1.0 - q) ** (1.0 / 12.0)
    cancer = (mth * ci_rate_at_age(y, "cancer") / total
              * ci_wait_factor_mth(t))
    return min(1.0, breast_share() * cancer / base)


def lapse_rate_base(t):
    """The **annual** 표준형 surrender rate of the policy year of month t, from the table.

    The file is keyed by the **contractual, 1-based ``policy_year`` label**, so month ``t``
    is read at row ``policy_year(t)`` and the file itself is untouched by the grid; rows
    past the last are the level tail.  A published 해지율 is an annual figure and stays
    one: the conversion to a month happens in :func:`lapse_rate_mth` and nowhere else.

    9% / 7% / 5.5% / 4.5% / 3.8% / 3.2% and a 2.8% tail, all **[std]**.  **No CI lapse
    experience of any kind was retrieved** — [R1] gives one cession ratio and no lapse data
    at all — so the curve is bounded rather than fitted: Korean 상품요약서 publish the
    적용해지율 used in pricing in envelope form, and one carrier's protection product
    discloses 0%-13.4% during the payment period against 1%-10% at another.  The tail sits
    far above the 0.8% post-완납 ultimate the supervisor's 원칙모형 sets, and that gap is
    the subject of [REG-R27].
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(max(policy_year(t), 1), int(tbl.index.max())),
                         "lapse_rate"])


def lapse_rate_ult():
    """The post-납입완료 ultimate surrender rate of whichever basis is in force.

    0.8% on the 로그-선형 원칙모형, which the IFRS17 주요 계리가정 가이드라인 sets as the
    post-완납 rate for 무·저해지 business [REG-R27]; the table's own tail otherwise, read at
    the first month after 납입완료.  Annual, like everything in the table.
    """
    if lapse_basis() == "log_linear":
        return lapse_post_paidup                                     # noqa: F821
    return lapse_rate_base(prem_period_mths())


def lapse_rate(t):
    """w(t): the **annual** surrender rate of the **pre-CI** cohort in the policy year of t.

    This is the rate the sources tabulate and the supervisor sets; its monthly companion is
    :func:`lapse_rate_mth`, and the pair is the library-wide convention on every monthly
    model.  On the ``log_linear`` basis it is the guideline's 원칙모형 — geometric decay
    from a first-year 10% **[std]** in policy year 1 to the 0.1% the guideline sets at
    납입완료, reached in the last paying year, then the 0.8% post-완납 ultimate from
    ``t = 12m`` [REG-R27].  On the ``table`` basis it is :func:`lapse_rate_base` unchanged.
    **The decay runs on the policy year and not on the month**, so the rate is level across
    the twelve rows of a policy year, which is how the guideline states it.

    **No separate 완납 surrender spike is imposed.**  The eightfold step from 0.1% to 0.8%
    at 납입완료 is produced by the guideline's own shape, and the contractual step in
    :func:`cv_pp` that provokes a real surge is a different object from the behavioural
    assumption about it; conflating the two is how a spike gets counted twice.

    A surrender is not a pure decrement here: it pays :func:`cv_pp` net of any loan, and
    that value is **suppressed** during the 납입기간, which is precisely why early
    surrender on this form is assumed low.
    """
    if lapse_basis() != "log_linear":
        return min(1.0, lapse_rate_base(t))
    m = prem_end()
    y = policy_year(t) - 1
    if y >= m:
        return lapse_post_paidup                                     # noqa: F821
    if m <= 1:
        return lapse_ll_target                                       # noqa: F821
    lam = math.log(lapse_ll_first / lapse_ll_target) / (m - 1)       # noqa: F821
    return min(1.0, lapse_ll_first * math.exp(-lam * y))             # noqa: F821


def lapse_rate_mth(t):
    """w^m(t): the surrender decrement applied to the **pre-CI** cohort in month t.

    ``1 - (1 - w(t))^(1/12)`` **[std]**, so that the twelve months of a policy year
    compound back to exactly the annual rate the table or the guideline states.  On the
    ``log_linear`` basis the vector spans two orders of magnitude — 10% to 0.1% — and
    dividing by twelve instead of compounding would understate the early months by 4.9% of
    the rate and overstate the late ones; only the compounding convention reproduces the
    supervisor's own annual figure at every 계약해당일.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_rate_ci(t):
    """w'(t): the **annual** voluntary surrender rate of the **post-CI** cohort.

    The ultimate rate of the basis in force times ``lapse_ci_factor`` **[std]**, level in
    t.  A post-CI policy is premium-waived, so it is in the paid-up state by construction
    and the paying-period curve does not describe it whichever basis is chosen.

    The factor is 0.50 and its **direction is genuinely ambiguous**, which is why it is a
    lever rather than a finding.  A CI claimant has no premium to fund and may value the
    residual cover highly, which argues for less surrender; but the carve-out has just
    doubled the cash available, which argues for more.  Nothing in any retrieved document
    bears on it.
    """
    return min(1.0, lapse_ci_factor * lapse_rate_ult())              # noqa: F821


def lapse_rate_ci_mth(t):
    """w'^m(t): the surrender decrement applied to the **post-CI** cohort in month t.

    ``1 - (1 - w'(t))^(1/12)``, level in t like the annual rate it converts.
    """
    return 1.0 - (1.0 - lapse_rate_ci(t)) ** (1.0 / 12.0)


def waiver_rate_mth(t):
    """u^m(t): the 장해 50%+ 납입면제 incidence applied in month t.

    ``1 - (1 - u(t))^(1/12)`` on :func:`waiver_rate`, so twelve compound back to the annual
    figure the model point carries.  The monthly grid also puts the transition in the month
    of the 장해 rather than at the next 계약해당일, which is when the 약관 stops the
    premium.
    """
    return 1.0 - (1.0 - waiver_rate(t)) ** (1.0 / 12.0)


def prem_int_rate_mth():
    """j: the monthly equivalent of the 예정이율, ``(1 + i)^(1/12) - 1``.

    Twelve of these compound back to exactly ``1 + i``, so the pricing basis is the same
    basis the annual-step model used and only the step changed.
    """
    return (1.0 + prem_int_rate) ** (1.0 / 12.0) - 1.0               # noqa: F821


def i_loan_mth():
    """j_L: the monthly equivalent of the 보험계약대출이율, ``(1 + i_L)^(1/12) - 1``.

    The 약관 quotes 보험계약대출이율 as an annual rate — 예정이율 + 1.5% = 4.00% on this
    chassis — so the monthly roll runs on its twelfth root and twelve months compound back
    to exactly the quoted figure.
    """
    return (1.0 + i_loan) ** (1.0 / 12.0) - 1.0                      # noqa: F821


def disc_factor_mth():
    """v^m = 1 / (1 + j): the **monthly** discount factor of the 예정이율.

    What every EPV in this model discounts on, the pricing recursions having moved to the
    month with the projection.  :func:`disc_factor` survives beside it as the annual figure
    the 예정이율 is quoted as.
    """
    return 1.0 / (1.0 + prem_int_rate_mth())


def disc_factor():
    """v = 1 / (1 + i): the annual discount factor of the 예정이율.

    2.50% flat, inherited unchanged from the whole life chassis and **[std]**.  No
    CI-specific pricing rate later than 2011 was retrieved and the two that exist bracket
    it from too far away to be useful — 연복리 4.0% on a January 2011 CI product [S3] and
    about 2.75% on a 2019 종신 illustration basis [S4] — while the chassis reads six values
    off 2021-2025 carrier documents spanning 2.25%-2.75% and takes the mid-point, which is
    also the 2026 평균공시이율 [REG-R48].  A library whose CI product and whose whole-life
    product discounted on different rates would make the cost of the acceleration
    impossible to read off the difference between them.

    Note that **예정이율 is not a regulatory term in Korea**: a full-text search of the
    감독규정 returns no occurrence, and the regulation speaks only of the 계약자적립액
    적용이율 and of the 금리연동형 / 금리확정형 distinction [REG-R9] [REG-R48].  Interest
    matters less here than on the chassis, because a CI benefit is paid a decade or more
    before the death benefit it accelerates and the liability is correspondingly shorter.
    """
    return 1.0 / (1.0 + prem_int_rate)                               # noqa: F821


def epv_resid(t):
    """A1(t): the EPV at the start of **month** t of the residual, for a post-CI life.

    ``v^m [q'^m r SA + (1 - q'^m) A1(t + 1)]`` on the pricing basis, with ``A1(T) = 0``.
    It values the residual at its **nominal** ``r SA`` and ignores the 105% account floor
    **[std]**: the floor is a multiple of ``V`` and ``V`` is built out of this quantity, so
    pricing it in would make the reserve self-referential.  The projection applies the
    floor in full, and :func:`check_resid_floor` asserts it there.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    q = mort_rate_ci_base_mth(t)
    return disc_factor_mth() * (q * resid_rate() * sum_assured()
                                + (1.0 - q) * epv_resid(t + 1))


def epv_ben(t):
    """A0(t): the EPV at the start of **month** t of every future benefit, pre-CI.

    The two-state recursion this whole product reduces to, a month at a time::

        A0(t) = v^m [ q_ci^m a SA + (1 - q_ci^m) q^m SA
                      + q_ci^m A1(t + 1) + (1 - q_ci^m)(1 - q^m) A0(t + 1) ]

    **The acceleration is a timing effect and nothing else.**  Because ``a + r = 1``
    exactly, a life that accelerates and then dies pays the same total as a life that
    simply dies; the CI event moves ``a SA`` of it forward by the years between the two
    events.  At the anchor cell that is worth 24.4% of the net premium against the same
    contract with no acceleration, and it is the whole actuarial content of the product.

    ``A0(T) = 0`` is the base case, at ``T = proj_len()``.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    qc = ci_rate_mth_base(t)
    qd = mort_rate_base_mth(t)
    return disc_factor_mth() * (
        qc * accel_rate() * sum_assured()
        + (1.0 - qc) * qd * sum_assured()
        + qc * epv_resid(t + 1)
        + (1.0 - qc) * (1.0 - qd) * epv_ben(t + 1))


def annuity_due(t):
    """The EPV at the start of **month** t of 1 a month while pre-CI and premium due.

    ``1 + v^m (1 - q_ci^m)(1 - q^m) a(t + 1)`` for ``t < 12m``, zero from ``t = 12m``, so
    it is measured in **months** of premium and ``A0 / a`` is a monthly net premium.
    **The CI decrement is in the annuity as well as in the benefit**, because any CI/LTC
    지급사유 waives all future 기본보험료 [S1 별표1 주4]: a premium stream that ran on
    through the post-CI state would over-fund the contract by the whole of the waiver.
    """
    if t < 0 or t >= prem_period_mths():
        return 0.0
    return 1.0 + disc_factor_mth() * (1.0 - ci_rate_mth_base(t)) * (
        1.0 - mort_rate_base_mth(t)) * annuity_due(t + 1)


def prem_net_level_mth_pp():
    """P^m: the **monthly** net level premium on the pricing basis, ``A0(0) / a(0)``.

    The quantity the account is built out of, and the one the monthly equivalence
    ``P^m a^m(0) = A0^m(0)`` solves for.  A **pricing** quantity that never becomes a cash
    flow: what is collected is :func:`premium_mth_pp`.
    """
    return epv_ben(0) / annuity_due(0)


def prem_net_level_pp():
    """P: the annualised net level premium, ``12 P^m``.

    Published so that the loading can be read against the **annual** gross the model point
    carries: on the anchor it is ₩3,051,133.35 against a gross of ₩3,680,880, a loading of
    20.6% — which sits close to, and is a different quantity from, the 보험료지수 of 130.1%
    [S3] publishes for the same form, that ratio being against the 표준순보험료 computed on
    the supervisor's prescribed rates rather than on this model's.  Both sides of that
    ratio are twelve times a monthly figure, so the comparison is the like-for-like one.

    **It is 2.78% above the annual-equivalence premium the annual-step model solved for**,
    and that is the ordinary modal effect of paying monthly in advance rather than once a
    year: eleven of the twelve instalments arrive later and are exposed to the year's
    decrements before they do.  The model point file's own premiums were derived from the
    annual-step figure and are unchanged — they are inputs, not outputs — so the loading
    the anchor now implies is 20.6% where it was 24.0%.

    It is **not** an annual-equivalence premium and is not used as one: nothing in the
    model solves ``P a(0) = A0(0)`` on an annual grid any more.  Nor is it the 연납순보험료
    that enters the 표준해약공제액; that is :func:`surr_chg_cap_pp`, which follows the
    chassis in taking 80% of the gross premium **[std]** so that the statutory cap can be
    reproduced from published quantities alone.
    """
    return 12.0 * prem_net_level_mth_pp()


def pol_val_pp(t):
    """V(t): the 계약자적립액 at **month-end** t, prospective and net level premium.

    On the month-end clock: ``t = 0`` is the issue instant and ``t = T`` the horizon, so
    this cells is defined for ``t = 0 … proj_len()`` and does not move with the frame.  The
    account that month ``t`` opens with is ``V(t)`` and the one it closes with is
    ``V(t + 1)``.  A 계약해당일 is ``t = 12 y``.

    ``A0(t) - P^m a(t)``, zero at ``t = 0`` — by the definition of ``P^m`` — and at
    ``t = T``.
    It is the account of
    the **표준형 twin** — the non-marketed comparison contract priced with the lapse
    assumption switched off — and there is exactly one of it in this model: the suppression
    is a haircut on this value, the post-CI carve-out lifts the haircut off this value, and
    the 기본보험금 and residual floors read off this value.  **CV(t) is therefore
    independent of the sold form's own premium**, which is the whole of the 환급률
    arithmetic that sells the 저해지 form.

    The recursion it satisfies is asserted by :func:`check_pol_val_roll_fwd`.  [S3] words
    the same identity in a CI product's own terms — 「보험료 계산시 적용한 위험률로 산출한
    순보험료식 책임준비금에서 미상각신계약비(해지공제액)를 공제한 금액을 해지환급금으로
    지급합니다」 — and [S1]'s 약관 sends the calculation to the 산출방법서, which is filed
    and unpublished [REG-R2].
    """
    if t <= 0:
        return 0.0
    return epv_ben(t) - prem_net_level_mth_pp() * annuity_due(t)


def cum_prem_pp(t):
    """cumprem(t): gross premiums paid per policy by **month-end** t.

    ``G^m min(t, 12m)``, the instalments falling at the month-ends ``0 … 12m - 1``.  This
    is one of the three limbs of the 기본보험금, and the monthly grid is what makes it a
    true running total: 이미 납입한 보험료 grows twelve times a year, not once.  **Waived
    premiums count as paid** — the chassis's rule, carried over
    — so a policy on the 장해 50%+ waiver reaches the same cumulative figure without
    funding it.
    """
    return premium_mth_pp() * min(t, prem_period_mths())


def base_benefit_pp(t):
    """B(t): the 기본보험금 at **month-end** t, the base every percentage applies to.

    On the month-end clock, so a claim arising in month ``t`` — paid at the end of it — is
    paid off ``B(t + 1)``.

    ``max(기본사망보험금, 이미 납입한 보험료, c V(t))`` with 기본사망보험금 =
    보험가입금액 - 중도인출금액 + 추가납입보험료 [S1 별표1 주7], the last two held at zero
    **[std]** — named rather than dropped, because a model that ignores them must say it
    holds them at zero rather than silently leaving them out of the definition.

    **At the anchor cell neither floor binds within the 납입기간**, and it is worth saying
    so plainly so that the model is not read as being built around a clause that never
    fires: cumulative premiums at 납입완료 are ₩73,617,600 against a face of
    ₩100,000,000, and ``c V(t)`` reaches the face only when ``V`` passes ₩95,238,095.  The
    floors bind where a Korean designer would want them to — a short-pay or high-premium
    cell, and a very old attained age.  The floor on the **residual** is a different matter
    and binds early: see :func:`resid_db_pp`.

    The premiums-paid limb is the contractual form of a supervisory design rule, 감독규정
    제7-60조제9호, which requires the death benefit to be at least cumulative premiums paid
    except where the payment period ends at age 80 or below [REG-R16] — and on the anchor
    cell 납입완료 falls at attained age 60, so the exception applies and the rule does not
    strictly bite.
    """
    return max(sum_assured(), cum_prem_pp(t),
               resid_floor_mult() * pol_val_pp(t))


def surr_chg_cap_pp():
    """SC_max: the statutory 표준해약공제액, the cap on the surrender charge.

    ``연납순보험료 x 5% x 해약공제계수 + 보험가입금액 x 10/1000`` [REG-R20], the
    해약공제계수 being the 보험기간 capped at 20 years for a 보장성보험 — so on a 종신
    contract it is **one year's net premium plus 1% of the sum assured**.  The
    연납순보험료 is taken as 80% of the gross **[std]**, the chassis's ratio, so that the
    cap can be reproduced from published quantities rather than from this model's own
    pricing basis.

    At the anchor that is ₩2,944,704 + ₩1,000,000 = **₩3,944,704**.  Cross-check: the
    FSC's 보장성보험 rule of thumb of 13 times the monthly premium gives ₩3,987,620, which
    agrees within 1.1% [REG-R29].  The 보험가입금액 that enters the formula is the
    **pre-acceleration** death benefit, by 감독규정 [별표 15] 제3호 read with 제8호
    [REG-R21]: a CI contract covers death from any cause, so 일반사망 applies directly and
    the figure is ₩100,000,000 and not the ₩20,000,000 residual — a clean instance of the
    acceleration form buying this product a simpler regulatory position than a standalone
    진단비 product, which must build a notional 보험가입금액 instead.
    """
    return (net_prem_ratio * premium_pp() * surr_chg_rate            # noqa: F821
            * surr_chg_coef_cap                                      # noqa: F821
            + surr_chg_sa_rate * sum_assured())                      # noqa: F821


def surr_chg_period_mths():
    """12 n_sc: the 해약공제기간 in **months**.

    The 납입기간 or the 신계약비 부가기간 **capped at 7 years** [REG-R19
    제7-66조제1항제2호], multiplied out.  The period is a contractual term quoted in years
    and did not change when the grid did.
    """
    return 12 * min(prem_period(), surr_chg_years_cap)               # noqa: F821


def surr_chg_pp(t):
    """SC(t): the 해약공제액 (미상각신계약비) outstanding at **month-end** t.

    On the month-end clock, ``t = 0`` at issue where the whole cap is outstanding, so a
    surrender arising in month ``t`` bears ``SC(t + 1)``.

    The cap running off in a straight line over the 해약공제기간, now in **84 monthly steps
    rather than seven annual ones** on the anchor's 20년납 contract, so the balance
    deducted is the balance outstanding in the month the surrender is actually taken.  The
    charge is gone by the month-end ``d = 84``, **thirteen years before 납입완료** and, on
    most lives, before any CI event — which is why the step in :func:`cv_pp` at 납입완료 is
    not a surrender-charge effect and cannot be explained as one.  The straight-line
    run-off is **[std]**: the amortisation schedule lives in the unpublished 산출방법서.
    """
    n = surr_chg_period_mths()
    if n <= 0 or t >= n:
        return 0.0
    return surr_chg_cap_pp() * (n - t) / n


def cv_std_pp(t):
    """W(t): the 표준형 twin's 해약환급금 at **anniversary** t, floored at zero.

    ``max(0, V(t) - SC(t))``.  The 미경과보험료 that 감독규정 제7-66조제5항 adds on
    termination is not modelled **[std]**: premiums are paid monthly in advance on the
    month-end grid, so at most one instalment is ever unexpired and the monthly step is the
    finest the composite's own premium mode makes available.
    """
    return max(0.0, pol_val_pp(t) - surr_chg_pp(t))


def cv_mult(t):
    """The multiplier on W(t) at **month-end** t: k inside the 납입기간, 1 from 납입완료.

    A **step, not a ramp**, at the 계약해당일 ``d = 12m``.  A surrender occurring in the
    last paying **month** — ``t = 12m - 1`` — is paid at the end of it, that is at
    ``d = 12m``, on the full value **[std ordering]**; the suppressed value applies to the
    month-ends 1 to ``12m - 1``.  The monthly grid is what makes the step checkable as a
    step: the two month-ends either side of it are one month apart, so a doubling between
    them is visibly a single-row event and not an artefact of comparing two balances a year
    apart.  Both quantities exist at every duration and the model publishes both,
    :func:`cv_pp` and :func:`cv_pp_ci`.
    """
    return 1.0 if t >= prem_period_mths() else cv_floor_ratio()


def cv_pp(t):
    """CV(t): the 해약환급금 payable on a **pre-CI** surrender at **anniversary** t.

    ``cv_mult(t) W(t)``.  On the 무해지 form (``k = 0``) this is nil throughout the
    납입기간, and the FSS's finding that such a contract cannot support a policy loan at
    all during the payment period [REG-R28] [REG-R25 제33조] follows arithmetically —
    which is one reason the composite's representative form is 저해지 rather than 무해지.
    """
    return cv_mult(t) * cv_std_pp(t)


def cv_pp_ci(t):
    """CV'(t): the 해약환급금 payable on a **post-CI** surrender at anniversary t.

    ``W(t)``, the full 표준형 value, at **every** duration, before and after 납입완료
    [S2] [S4].  This is the CI-specific delta on the chassis and it is contractual: [S2]
    conditions the suppression on 「제7조 … 제2호의 CI/LTC보험금 지급사유가 발생하지 않은
    경우」 and [S4] on 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」.

    Three consequences follow and each is a modelling requirement.  The surrender strain
    on the post-CI cohort is materially larger than on the pre-CI cohort at the same
    duration, so a projection running one surrender-value scale over one aggregate policy
    count understates outgo.  The policy loan available jumps at the same date.  And the
    premium stops at the same date, so from ``t_CI`` the contract pays nothing, holds a
    full-value surrender right and owes only the residual — which is what makes the post-CI
    state a genuinely different liability rather than a scaled-down version of the pre-CI
    one.

    There is an accounting asymmetry worth naming: the 해약환급금준비금 appropriation test
    measures the IFRS 17 잔여보장요소 against the surrender value computed under 제7-66조
    제1항, on the unsuppressed basis, **even for the 제4항 products that may contractually
    pay less** [REG-R11].  So this carve-out doubles the contractual value from one day to
    the next and changes the reserve it is measured against not at all.
    """
    return cv_std_pp(t)


def ci_cohort_ids(t):
    """The post-CI cohort labels that can carry policies at the start of month t.

    ``[-1 .. -min(t, 12)] + [1 .. t]``.  A cohort is labelled by the **month-end at which
    its acceleration was paid**, so a life accelerating in month ``u`` is paid at
    ``u + 1`` and carries the label ``u + 1``.  The **negative** labels are the first-year
    감액 cohorts: a reduced claim paid at the month-end ``d`` carries the label ``-d``,
    which is free precisely because nothing can be accelerated at month-end 0 and no full
    claim ever carries a negative label.

    **The monthly grid turns one reduced cohort into twelve.**  On an annual grid the whole
    of the first policy year's reduced claims were paid at one anniversary and carried one
    residual; here they are paid at twelve month-ends, each off its own 기본보험금, and the
    first two are empty because no 중대한 암 is covered before the 보장개시일.  Entrants
    join at the start of the month after they accelerate, so no label ``> t`` can be
    populated at t.
    """
    return ([-s for s in range(1, min(max(t, 0), 12) + 1)]
            + list(range(1, max(t, 0) + 1)))


def accel_benefit_pp(s):
    """a B(s): the 선지급 CI/LTC보험금 paid to cohort s, per policy.

    ``a B(s)`` for a full claim paid at the month-end ``s``, and ``a f B(-s)`` for a
    first-year reduced claim, whose label is the negative of the month-end it was paid at;
    ``f = 0.5``, so 40% of the 기본보험금 instead of 80% on the composite, 25% instead of
    50% on the 50% form [S1 별표1] [S2 별표1].  Paid at the
    end of the **month** of the event, **once only** across the whole trigger set, and
    **not** netted against any policy loan: the contract continues and the loan stays
    outstanding against the residual.
    """
    if s < 0:
        return accel_rate() * first_year_factor * base_benefit_pp(-s)  # noqa: F821
    return accel_rate() * base_benefit_pp(s)


def resid_nominal_pp(s):
    """r B(s): the nominal residual death benefit cohort s carries, per policy.

    The exact complement of what was paid — ``(1 - a) B(s)``, and ``(1 - a f) B(-s)`` for a
    first-year reduced cohort, so 60% where 40% was accelerated [S1] [S2].  It is
    fixed at the acceleration **month** and does not move afterwards; what moves is the
    floor beneath it, :func:`resid_db_pp`.  The monthly grid is what makes 「지급사유 발생
    당시의 기본보험금」 a month rather than a policy year.
    """
    if s < 0:
        return (1.0 - accel_rate() * first_year_factor) * base_benefit_pp(-s)  # noqa: F821
    return resid_rate() * base_benefit_pp(s)


def resid_db_pp(t, s):
    """The death benefit payable at **month-end** t to a policy in cohort s.

    Both indices are on the month-end clock, so a post-CI death in month ``t`` is paid
    ``resid_db_pp(t + 1, s)``.

    ``max(r B(s), c V(t))`` — 「CI/LTC보험금 지급사유 발생당시의 기본보험금의 20%와
    CI/LTC보험금 지급사유 발생 후 계약자적립금의 105% 중 큰 금액」 [S1 별표1 주8].  **The
    residual is not a constant**, and on the 80% form the floor binds early and stays
    bound: at the anchor cell ``r B`` is ₩20,000,000 and the account passes ₩19,050,000
    well inside the 납입기간, so for most of the contract's life the residual death benefit
    **is the account value and not the stated complement**.  A model that hard-codes 20% of
    the sum assured understates the post-CI liability by a growing margin, and that
    asymmetry is one of the three reasons the composite takes the 80% fraction.
    """
    return max(resid_nominal_pp(s), resid_floor_mult() * pol_val_pp(t))


def resid_nom_min_pp(t):
    """The smallest nominal residual carried by any cohort live at the start of month t.

    A running minimum over the cohorts formed so far, and one of the two bounds that let
    :func:`resid_db_total_pp` close in one line in the months where the 105% account floor
    is either below every cohort's nominal or above all of them.  Infinite — represented as
    the largest nominal plus one won — while no cohort exists.
    """
    if t <= 0:
        return 0.0
    prev = resid_nom_min_pp(t - 1) if t > 1 else 0.0
    here = resid_nominal_pp(t)
    if t <= 12 and ci_reduced_share(t - 1) > 0.0:
        here = min(here, resid_nominal_pp(-t))
    if t == 1:
        return here
    return min(prev, here)


def resid_nom_max_pp(t):
    """The largest nominal residual carried by any cohort live at the start of month t.

    The companion running maximum to :func:`resid_nom_min_pp`.
    """
    if t <= 0:
        return 0.0
    prev = resid_nom_max_pp(t - 1) if t > 1 else 0.0
    here = resid_nominal_pp(t)
    if t <= 12 and ci_reduced_share(t - 1) > 0.0:
        here = max(here, resid_nominal_pp(-t))
    if t == 1:
        return here
    return max(prev, here)


def resid_nom_total_pp(t):
    """Sum over the post-CI cohorts of count times **nominal** residual, at month t.

    ``sum(l1(t, s) r B(s))``, carried as its own O(T) recursion rather than rebuilt from
    the cohort table every month: every post-CI cohort carries the same two decrements, so
    the aggregate rolls forward exactly as a single cohort would, and the month's entrants
    are added at their own nominal.

    This is the conversion's one piece of new machinery and it is there for a reason.  The
    cohort dimension is the acceleration **month**, so the (month, cohort) table is twelve
    times longer and a hundred and forty-four times larger than the annual grid's; summing
    it row by row in every month is quadratic work for an answer that is almost always
    available in closed form.  See :func:`resid_db_total_pp`.
    """
    if t <= 0:
        return 0.0
    prev = resid_nom_total_pp(t - 1) * (1.0 - mort_rate_ci_mth(t - 1)) * (
        1.0 - lapse_rate_ci_mth(t - 1))
    entrants = 0.0
    for s in (t, -t):
        entrants = entrants + pols_ci_in(t - 1, s) * resid_nominal_pp(s)
    return prev + entrants


def resid_db_total_pp(t):
    """Sum over the post-CI cohorts of count times **payable** residual, at month t.

    ``sum(l1(t, s) max(r B(s), c V(t + 1)))`` — the amounts payable at the month-end that
    closes month ``t``, which is where a post-CI death in it is paid.  It is what
    :func:`claims` weights ``"DEATH_CI"`` by and what :func:`resid_db_avg_pp` averages.

    Three cases, and the first two are exact one-liners:

    * the floor is **below every** cohort's nominal — then the payable residual is the
      nominal for all of them and the answer is :func:`resid_nom_total_pp`;
    * the floor is **at or above every** nominal — then it is the floor for all of them
      and the answer is the floor times the count;
    * otherwise the cohorts straddle the floor and the sum is taken cohort by cohort.

    On every shipped model point the third case covers a window of a year or two — the
    months in which ``1.05 V`` crosses the narrow band the nominals occupy — so the cohort
    loop runs where it is needed and nowhere else, and the result is the same number a
    row-by-row sum would give in every month.
    """
    n = pols_if_ci(t)
    if n <= 0.0:
        return 0.0
    floor = resid_floor_mult() * pol_val_pp(t + 1)
    if floor <= resid_nom_min_pp(t):
        return resid_nom_total_pp(t)
    if floor >= resid_nom_max_pp(t):
        return floor * n
    return sum(pols_if_ci_at(t, s) * resid_db_pp(t + 1, s)
               for s in ci_cohort_ids(t))


def resid_db_avg_pp(t):
    """The in-force-weighted mean residual death benefit over the cohorts, in month t.

    The weights are the post-CI counts at the **start** of month ``t`` and the amounts are
    the benefits payable at its **end**, the month-end ``t + 1``, which is the pairing
    :func:`claims` uses for ``"DEATH_CI"``.

    A reporting quantity only; no cash flow uses it.  It is published because the spread
    between it and ``r SA`` is the clearest single reading of how far the 105% floor has
    taken over the residual.
    """
    n = pols_if_ci(t)
    if n <= 0.0:
        return 0.0
    return resid_db_total_pp(t) / n


def loan_avail_pp(t):
    """The 보험계약대출 available at month-end t to a **pre-CI** policy.

    80% of the *payable* 해약환급금 [REG-R25 제33조], which during the 납입기간 is the
    **suppressed** value.  The chassis argues the 80% limit against published Korean ranges
    of 「해약환급금의 50% ~ 85%」 and 「50 ~ 80%이내」 and this product inherits it.
    """
    return loan_cap_rate * cv_pp(t)                                  # noqa: F821


def loan_avail_ci_pp(t):
    """The 보험계약대출 available at month-end t to a **post-CI** policy.

    The same 80% of the payable value, which after a CI event is the **full** 표준형 value
    — so on the composite's ``k = 0.50`` form **the available loan doubles the moment a
    CI/LTC 지급사유 arises**, at the same duration and with no other change to the
    contract.  Nothing in the retrieved documents restricts the loan after a CI payment, so
    the post-acceleration contract carries a full-value loan facility against a sum assured
    that is now a fifth of its original size; whether any carrier restricts it further is
    **[unverified]**.  Published as its own cells so that the doubling can be read directly
    rather than inferred.
    """
    return loan_cap_rate * cv_pp_ci(t)                               # noqa: F821


def pol_loan_draw(t):
    """Delta(t): the 보험계약대출 drawn at **month-end** t, per policy; nil in the base run.

    ``pol_loan_year`` is a contractual duration in **policy years** — duration 12 on model
    point 7 — and did not change when the grid did: the draw falls at the 계약해당일
    ``d = 12 * pol_loan_year()``, which is the same date it always was, now located to the
    month.
    """
    if pol_loan_year() <= 0 or t != 12 * pol_loan_year():
        return 0.0
    return pol_loan_util() * loan_avail_pp(t)


def loan_pp(t):
    """L(t): the 보험계약대출 balance at time t, the opening balance of month t.

    ``L(0) = 0`` and ``L(t) = (L(t - 1) + Delta(t))(1 + j_L)`` on the **monthly**
    equivalent of ``i_L = 예정이율 + 1.5% = 4.00%``, the chassis's rate, so twelve months
    compound back to exactly the annual figure the 약관 quotes; ``Delta`` is
    :func:`pol_loan_draw` on the month-end clock, so a draw is booked with one month's
    interest in the month it is taken **[std]** —
    this model's own arithmetic, and identically immaterial in the base run, where nothing
    is drawn.  It is the balance the benefits of month ``t`` are netted down by.
    One balance per policy, carried unchanged across the CI
    transition — a policy that borrowed before accelerating still owes it afterwards — and
    deducted from every terminal payment, floored at zero.  The 보험계약대출 is a modelled
    state and not a decrement: no policy leaves because of it here, and a loan that
    outgrows the benefit simply reduces the payment to nil.
    """
    if t <= 0:
        return 0.0
    return (loan_pp(t - 1) + pol_loan_draw(t)) * (1.0 + i_loan_mth())


def pols_if_pre(t):
    """l0(t): policies in force and **pre-CI** at the start of month t.

    Decremented in the month by the CI transition first, then death among those who did not
    accelerate, then surrender among those who neither accelerated nor died, so
    ``l0(t + 1) = l0(t)(1 - q_ci^m)(1 - q^m)(1 - w^m)``, with ``l0(0) = pols_if_init()``.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return (pols_if_pre(t - 1) - pols_ci(t - 1) - pols_death(t - 1)
            - pols_lapse(t - 1))


def pols_waived(t):
    """Policies in force, pre-CI and on the **장해 50%+** premium waiver at the start of t.

    A subset of :func:`pols_if_pre`, not a separate state: a waived policy keeps its full
    death cover, stays exposed to the CI decrement and continues to accrue surrender value
    on the full premium scale.  What it stops doing is paying, so it is subtracted from
    :func:`pols_if_pay` and from the renewal commission that follows the cash.  The waiver
    on the CI limb is not counted here — it is implicit in the post-CI cohort, which pays
    nothing at all.  Nil in the first month, ``t = 0``: nobody has yet been on the waiver.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return 0.0
    u = t - 1
    entered = (pols_waived(u)
               + (pols_if_pre(u) - pols_waived(u)) * waiver_rate_mth(u))
    return entered * (1.0 - ci_rate_mth(u)) * (1.0 - mort_rate_mth(u)) * (
        1.0 - lapse_rate_mth(u))


def pols_if_pay(t):
    """lp(t): policies in force, pre-CI and actually paying a premium in month t.

    ``l0(t)`` less the waived subset, and nil once no premium is due.  **The post-CI cohort
    never appears here**: any CI/LTC 지급사유 waives all future 기본보험료 [S1 별표1 주4],
    so the residual death benefit is funded entirely out of the reserve standing at the
    acceleration date — which [S4] states in terms, computing the post-waiver reserve on
    the post-acceleration basis 「「선지급 진단보험금」 발생 이후 기준의 책임준비금을 계산」.
    """
    if t < 0 or t >= prem_period_mths():
        return 0.0
    return pols_if_pre(t) - pols_waived(t)


def pols_ci(t):
    """C(t): CI/LTC accelerations in month t, taken from the pre-CI cohort.

    ``l0(t) q_ci^m(t)``.  This is a **state transition and not an exit**: the contract
    continues, which 감독규정 제7-60조제8호 requires — a contract must not be extinguished
    while the risk it covers remains effective [REG-R16] — so these policies reappear in
    :func:`pols_if_ci` at the start of the next month and stay in :func:`pols_if`
    throughout.
    """
    return pols_if_pre(t) * ci_rate_mth(t)


def pols_ci_in(t, s):
    """C(t, s): accelerations in month t entering post-CI cohort s.

    Cohort ``t + 1`` — the month-end at which the month's claims are paid — takes the
    full-benefit claims of month ``t``; cohort ``-(t + 1)`` takes the reduced ones, and is
    empty outside the twelve months of the first policy year.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if s < 0:
        if t >= 12 or s != -(t + 1):
            return 0.0
        return pols_ci(t) * ci_reduced_share(t)
    return pols_ci(t) * (1.0 - ci_reduced_share(t)) if s == t + 1 else 0.0


def ci_cohort_entrants(s):
    """The policies that entered post-CI cohort s, at the month-end ``abs(s)`` it is named for.

    A cohort has exactly **one** entry month by construction — it is labelled by the
    month-end its acceleration was paid at — which is what lets :func:`pols_if_ci_at` be a
    closed form rather than a recursion in ``t``.
    """
    if s == 0:
        return 0.0
    return pols_ci_in(abs(s) - 1, s)


def ci_surv(t):
    """The post-CI survivorship from issue to the start of month t, ignoring entry.

    ``prod (1 - q'^m(u))(1 - w'^m(u))`` over ``u < t``, with ``ci_surv(0) = 1``.  Every
    post-CI cohort carries the same two decrements, so a cohort's in-force at ``t`` is its
    entry count times the ratio of this factor at ``t`` to its value at the entry month —
    which is :func:`pols_if_ci_at`, in closed form and without a recursion per cohort.
    """
    if t <= 0:
        return 1.0
    u = t - 1
    return ci_surv(u) * (1.0 - mort_rate_ci_mth(u)) * (1.0 - lapse_rate_ci_mth(u))


def pols_if_ci_at(t, s):
    """l1(t, s): policies in force and post-CI at the start of month t, from cohort s.

    Entrants join at the start of the month **after** they accelerate, and are then
    decremented by post-CI mortality and post-CI surrender.  Kept by cohort because the
    residual is a cohort property: see :func:`resid_nominal_pp`.  Nil at ``t = 0``, and
    defined one step past the frame at ``t = proj_len()``, the terminal month-end, where
    the roll-forward checks read it.

    Written as ``entrants(s) x ci_surv(t) / ci_surv(abs(s))`` rather than as a recursion in
    ``t``.  The two are the same number; the closed form is what keeps a cohort dimension
    twelve times longer than the annual grid's from turning every read of it into a chain
    of monthly steps.
    """
    if t <= 0 or t > proj_len():
        return 0.0
    d = abs(s)
    if d <= 0 or d > t:
        return 0.0
    base = ci_surv(d)
    if base <= 0.0:
        return 0.0
    return ci_cohort_entrants(s) * ci_surv(t) / base


def pols_if_ci(t):
    """l1(t): policies in force and post-CI at the start of month t, all cohorts.

    Carried as its own recursion — the month's entrants plus last month's survivors — and
    not as a sum over the cohort table.  Every post-CI cohort runs the same two decrements,
    so the aggregate rolls forward exactly as the sum of the cohorts does, and the identity
    is what :func:`check_ci_state_roll_fwd` asserts.
    """
    if t <= 0 or t > proj_len():
        return 0.0
    u = t - 1
    return (pols_ci(u) + pols_if_ci(u) * (1.0 - mort_rate_ci_mth(u))
            * (1.0 - lapse_rate_ci_mth(u)))


def pols_if(t):
    """l(t): the total number of policies in force at the **start** of policy year t.

    Pre-CI plus post-CI.  A CI claimant's contract is still in force — that is the whole
    point of an acceleration — so both states are counted here, and this is the weight on
    every maintenance-expense figure of the same ``result_cf()`` row.  It is
    :func:`pols_if_init` in the first month, ``t = 0``, and 0 at ``proj_len()``,
    because the table terminates and every remaining life dies in the final policy year.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    return pols_if_pre(t) + pols_if_ci(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before anything happens; the same number
        as :func:`pols_if`.

    ``"BEF_LAPSE"``
        after the CI transition and after deaths, before surrenders — the
        processing order is **CI, then death, then lapse** **[std order]**, so
        this is the population surrenders are taken from.

    ``"AFT_DECR"``
        l(t + 1), the end-of-month state, and zero at ``proj_len() - 1`` because
        the table's terminal rate is 1 and nobody survives the final policy year.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return (pols_if_pre(t) * (1.0 - ci_rate_mth(t))
                * (1.0 - mort_rate_mth(t))
                + pols_ci(t)
                + pols_if_ci(t) * (1.0 - mort_rate_ci_mth(t)))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t): expected deaths of **pre-CI** policies in month t, at the end of it.

    Taken from the survivors of the CI transition.  These policies never received an
    acceleration, so they are paid the whole 기본보험금 [S1].
    """
    return pols_if_pre(t) * (1.0 - ci_rate_mth(t)) * mort_rate_mth(t)


def pols_death_ci(t):
    """D'(t): expected deaths of **post-CI** policies in month t, at the end of it.

    On :func:`mort_rate_ci_mth`, which carries the excess mortality a 중대한 질병 event
    implies.  Each cohort is paid its own residual, so the aggregate count here is a
    reporting figure and the benefit is weighted by :func:`resid_db_total_pp` in
    :func:`claims`.
    """
    return pols_if_ci(t) * mort_rate_ci_mth(t)


def pols_lapse(t):
    """S(t): expected surrenders of **pre-CI** policies at the end of month t.

    Taken from the survivors of the CI transition and of mortality — **CI, then death,
    then lapse** **[std order]** — and paid :func:`cv_pp` net of any loan, which inside
    the 납입기간 is the *suppressed* value.
    """
    return (pols_if_pre(t) * (1.0 - ci_rate_mth(t)) * (1.0 - mort_rate_mth(t))
            * lapse_rate_mth(t))


def pols_lapse_ci(t):
    """S'(t): expected surrenders of **post-CI** policies at the end of month t.

    Paid :func:`cv_pp_ci`, the **full** 표준형 value, at every duration.  The surrender
    strain on this cohort is therefore materially larger than on the pre-CI cohort at the
    same duration, which is the modelling consequence of the carve-out.
    """
    return pols_if_ci(t) * (1.0 - mort_rate_ci_mth(t)) * lapse_rate_ci_mth(t)


def premiums(t):
    """Premium income at the start of month t, an inflow.

    ``G^m lp(t)``, carried on the paying cohort alone: the post-CI cohort pays nothing
    because any CI/LTC 지급사유 waives the premium, and the 장해 50%+ waived subset pays
    nothing either.  Zero from ``t = prem_period_mths()``; **nothing else about the
    contract stops there.**

    There is no 자동대출납입 behind the 납입최고 in any retrieved Korean 약관 — a
    conventional Korean contract is 해지 the day after a 14-day demand period ends
    [REG-R25 제26조] — so Korean lapse is behavioural rather than funded, and a model that
    imported the Japanese automatic-premium-loan machinery onto this chassis would remove a
    decrement the contract has.
    """
    return premium_mth_pp() * pols_if_pay(t)


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    Every payment here falls at the **end** of month ``t``, which is the month-end
    ``t + 1``, so every amount is read off the month-end clock one step ahead of the row:
    ``B(t + 1)``, ``CV(t + 1)``, ``W(t + 1)``, ``resid_db_pp(t + 1, s)``.  The loan netted
    off is ``loan_pp(t)``, the balance the month opened with.

    ``"CI"``
        the 선지급 CI/LTC보험금, ``a B(t + 1)`` on the full-benefit claims —
        cohort ``t + 1`` — and ``a f B(t + 1)`` on the first-year reduced ones,
        cohort ``-(t + 1)``, paid at the end of the **month** of the event and
        **not** netted against any policy loan, because the contract continues
        and the loan does with it.

    ``"DEATH"``
        the 사망보험금 of a policy with no prior CI payment, ``B(t + 1)`` net of
        any loan, floored at zero.

    ``"DEATH_CI"``
        the residual death benefit, ``max(r B(s), c V(t + 1))`` net of any loan,
        summed cohort by cohort because each carries its own nominal.

    ``"LAPSE"``
        the 해약환급금 on a pre-CI surrender, ``CV(t + 1)`` net of any loan.

    ``"LAPSE_CI"``
        the 해약환급금 on a post-CI surrender, the **full** ``W(t + 1)`` net of
        any loan — the carve-out, at every duration.

    Every one of these is floored at zero: a loan can outgrow the surrender value and,
    given long enough, the residual, and none of them may produce a negative payment.
    """
    if kind is None:
        return (claims(t, "CI") + claims(t, "DEATH") + claims(t, "DEATH_CI")
                + claims(t, "LAPSE") + claims(t, "LAPSE_CI"))
    if kind == "CI":
        return sum(pols_ci_in(t, s) * accel_benefit_pp(s)
                   for s in (t + 1, -(t + 1)))
    if kind == "DEATH":
        return max(0.0, base_benefit_pp(t + 1) - loan_pp(t)) * pols_death(t)
    if kind == "DEATH_CI":
        n = pols_if_ci(t)
        if n <= 0.0:
            return 0.0
        loan = loan_pp(t)
        floor = resid_floor_mult() * pol_val_pp(t + 1)
        low = min(resid_nom_min_pp(t), floor)
        if loan <= low:
            return mort_rate_ci_mth(t) * (resid_db_total_pp(t) - loan * n)
        if loan >= max(resid_nom_max_pp(t), floor):
            return 0.0
        return sum(pols_if_ci_at(t, s) * mort_rate_ci_mth(t)
                   * max(0.0, resid_db_pp(t + 1, s) - loan)
                   for s in ci_cohort_ids(t))
    if kind == "LAPSE":
        return max(0.0, cv_pp(t + 1) - loan_pp(t)) * pols_lapse(t)
    if kind == "LAPSE_CI":
        return max(0.0, cv_pp_ci(t + 1) - loan_pp(t)) * pols_lapse_ci(t)
    raise ValueError("invalid kind")


def claim_expenses(t):
    """The claim handling expense on the month's claim events **[std]**.

    ₩300,000 per event, uninflated, on CI accelerations and on both kinds of death.  **A
    CI claim is charged the same as a death claim**, which is a standardization and
    probably a generous one: the whole dispute record of this product is about
    adjudicating the 중대한 definitions, and an accelerated claim on a 중대한 뇌졸중
    requires a 장해 assessment deferred twelve months after onset [S1 별표3].  No Korean
    carrier publishes an expense basis of any kind — [S1] names the components as
    계약체결비용 and 계약관리비용 and never quantifies them — so every expense level here is
    a standardization, bounded above by the 표준해약공제액 [REG-R20] and by the 보험료지수
    of 130.1% [S3].  Published as its own ``claim_expenses`` column and deducted explicitly
    in :func:`net_cf`; it is **not** inside :func:`expenses`.
    """
    return expense_claim * (pols_ci(t) + pols_death(t)               # noqa: F821
                            + pols_death_ci(t))


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(t // 12)`` **[std]**, 1 at t = 0.

    1.0% a year, stepping on the **계약해당일** and level across the twelve months of a
    policy year — an expense basis is quoted per annum and an inflation assumption with it.
    Over a seventy-year whole-life horizon 1% compounds to 2.0 and 3% to
    7.9, so importing a Western inflation assumption here produces a different product
    rather than a stressed one.  There is no published Korean expense basis to anchor
    either figure.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def expenses(t):
    """E0 and e(t) in month t: **acquisition and maintenance only** **[std]**.

    ₩500,000 per policy at issue, then ₩5,000 per policy per **month** inflating at 1% a
    year, both at the start of the month.  Maintenance is carried on :func:`pols_if`, the
    **total** in force, so a post-CI policy costs the same to administer as a pre-CI one;
    it continues **for life** and not to 납입완료, which is the structural point of this
    chassis.  There is no separate surrender expense; it is folded into maintenance
    **[std]**.  The claim handling expense is not here: it is :func:`claim_expenses`,
    deducted separately and published in its own column.
    """
    acq = expense_acq * pols_if(0) if t == 0 else 0.0                # noqa: F821
    maint = expense_maint * inflation_factor(t) * pols_if(t)         # noqa: F821
    return acq + maint


def commissions(t):
    """Commission outgo in month t **[std]**.

    80% of the **annual** premium in month 0, then 3% of premium income in the months of
    policy years 2 to m — ``t = 12 … 12m - 1``, every paying month but the twelve of the
    first policy year.  The initial commission is computed on the annual premium because
    that is the unit a Korean commission scale is written in: the **1,200% rule** of the
    2019 사업비 reform caps first-year 모집수수료 at twelve times the **monthly** premium,
    which is one annual premium [REG-R29], and the 80% here sits under it and just under
    the 표준해약공제액 of ₩3,944,704, the statutory bound on what a surrender may be made
    to repay.  Renewal commission follows the premium **actually collected in cash**, so
    neither the waived subset nor the post-CI cohort produces any, and none is paid after
    납입완료.
    """
    init = (comm_init_rate * premium_pp() * pols_if(0)               # noqa: F821
            if t == 0 else 0.0)
    renew = (comm_renewal_rate * premiums(t)                         # noqa: F821
             if 12 <= t < prem_period_mths() else 0.0)
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of month t, **income positive**.

    Premiums less the five kinds of benefit, claim expense, acquisition and maintenance
    expense and commission.  The notes' own sign, which is also the library-wide
    convention, so there is no outgo-positive ``liability_cf`` companion to publish.

    The shape to expect is a deep new business strain in the first **month** ``t = 0``,
    where the whole acquisition expense and the whole first-year commission fall against
    one instalment of premium, a long positive stretch
    while the premium runs against a CI decrement that is still small, a steepening drain
    as the incidence curve turns over from the fifties, a negative step at 납입완료 where
    the premium stops and the suppression lifts, and then a run-off in which the whole of
    the outgo is claims and maintenance against no income at all.  **The acceleration
    front-loads that outgo**: on the anchor cell the CI benefit is paid a decade or more
    before the death benefit it accelerates.
    """
    return (premiums(t) - claims(t) - claim_expenses(t) - expenses(t)
            - commissions(t))


def check_pols_roll_fwd_resid(t):
    """The total in-force roll-forward residual in month t; zero everywhere.

    ``l(t) - l(t + 1)`` less deaths and surrenders in **both** states.  The CI
    acceleration is deliberately absent from this identity: it is a transition and not an
    exit, and a model in which it reduced the in-force count would be modelling a
    standalone 진단비 benefit rather than an acceleration.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_death_ci(t)
            - pols_lapse(t) - pols_lapse_ci(t))


def check_pols_roll_fwd():
    """True when the total in-force roll-forward closes in every projected month."""
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_ci_state_roll_fwd_resid(t):
    """The two-state transition residual in month t; zero everywhere.

    Two identities added: the pre-CI cohort loses exactly its accelerations, deaths and
    surrenders, and the post-CI cohort gains exactly the accelerations and loses exactly
    its own deaths and surrenders.  This is the check that catches a policy accelerating
    out of one state and not arriving in the other, which the total roll-forward above
    cannot see.
    """
    pre = (pols_if_pre(t) - pols_if_pre(t + 1) - pols_ci(t)
           - pols_death(t) - pols_lapse(t))
    post = (pols_if_ci(t + 1) - pols_if_ci(t) - pols_ci(t)
            + pols_death_ci(t) + pols_lapse_ci(t))
    return pre + post


def check_ci_state_roll_fwd():
    """True when both cohorts roll forward and the transition between them balances."""
    return all(abs(check_ci_state_roll_fwd_resid(t)) <= roll_fwd_tol  # noqa: F821
               for t in range(proj_len()))


def check_decrement_sum_resid(t):
    """The cumulative-decrement residual at month t; zero everywhere.

    ``l(0)`` less every exit up to and including month t less ``l(t + 1)``.  At
    ``t = T - 1``
    it is the statement that the decrements sum to 1: because the table terminates, every
    policy leaves by a death or a surrender in one of the two states and there is no
    residual population and no tail state anywhere in this model.
    """
    exits = sum(pols_death(u) + pols_death_ci(u) + pols_lapse(u)
                + pols_lapse_ci(u) for u in range(t + 1))
    return pols_if(0) - exits - pols_if(t + 1)


def check_decrement_sum():
    """True when every policy issued leaves by a modelled decrement, in every month."""
    return all(abs(check_decrement_sum_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_pol_val_roll_fwd_resid(t):
    """The 계약자적립액 recursion residual over month t; zero everywhere.

    ``(V(t) + P^m 1{t < 12m})(1 + j)`` less ``q_ci^m [a SA + A1(t+1)] + (1 - q_ci^m) q^m SA
    + (1 - q_ci^m)(1 - q^m) V(t + 1)`` on the pricing decrements — the retrospective form
    of the same prospective value, rolling the account the month **opens** with, ``V(t)``,
    into the one it **closes** with, ``V(t + 1)``.  It is what catches a mis-set 납입기간, a
    discount factor applied on the wrong side, a CI decrement left out of the premium
    annuity but present in the benefit, or an annual rate used where its monthly conversion
    belongs.
    """
    pi = prem_net_level_mth_pp() if t < prem_period_mths() else 0.0
    qc = ci_rate_mth_base(t)
    qd = mort_rate_base_mth(t)
    return ((pol_val_pp(t) + pi) * (1.0 + prem_int_rate_mth())
            - qc * (accel_rate() * sum_assured() + epv_resid(t + 1))
            - (1.0 - qc) * qd * sum_assured()
            - (1.0 - qc) * (1.0 - qd) * pol_val_pp(t + 1))


def check_pol_val_roll_fwd():
    """True when the 계약자적립액 rolls forward on its own basis in every month."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_pol_val_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_accel_complement_resid(t):
    """The complement residual for every cohort formed in month t; zero everywhere.

    **The identity this product exists to demonstrate**: what is accelerated and what is
    left add to exactly the 기본보험금 that was in force when the claim arose,
    ``a B + r B = B`` and ``a f B + (1 - a f) B = B``, so the acceleration is a
    redistribution of one sum assured across two dates and never adds cover [S1] [S2].
    Exactly two cohorts can be formed in a month — the full one ``t + 1`` and the reduced
    one ``-(t + 1)`` — so the check reads those two and no others, and a model point whose
    first policy year carries reduced claims checks both arithmetics.
    """
    resid = 0.0
    for s in (t + 1, -(t + 1)):
        if pols_ci_in(t, s) == 0.0:
            continue
        base = base_benefit_pp(abs(s))
        resid = resid + (accel_benefit_pp(s) + resid_nominal_pp(s) - base)
    return resid


def check_accel_complement():
    """True when the acceleration and its residual sum to the 기본보험금, every cohort."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_accel_complement_resid(t)) <= tol
               for t in range(proj_len()))


def check_resid_floor_resid(t):
    """The residual-floor residual for month t; zero everywhere.

    Read at the month-end ``t + 1``, the end of the month, which is where a post-CI death
    in month ``t`` is paid.  The post-CI death benefit must be at or above **both** of its
    limbs — the nominal complement fixed at the acceleration month and 105% of the account
    now — so the two shortfalls, each floored above at zero, must vanish.  A one-sided
    ``max`` written the wrong way round, or a floor read off the wrong month's account,
    shows up here and nowhere else.

    It is asserted in two forms, because the cohort dimension is now the acceleration
    **month** and a full cohort-by-cohort sweep of every month would be quadratic.  In
    every month the **aggregate** form is checked — the total payable residual against the
    total nominal and against the floor times the count, which is the same statement summed
    — and at every **계약해당일** the sweep is taken cohort by cohort as well, so every
    cohort ever formed is read against both of its limbs at twelve-month intervals and the
    first-year reduced cohorts are read at the first of them.
    """
    floor = resid_floor_mult() * pol_val_pp(t + 1)
    resid = (min(0.0, resid_db_total_pp(t) - resid_nom_total_pp(t))
             + min(0.0, resid_db_total_pp(t) - floor * pols_if_ci(t)))
    if t % 12 == 0:
        for s in ci_cohort_ids(t):
            db = resid_db_pp(t + 1, s)
            resid = resid + min(0.0, db - resid_nominal_pp(s))
            resid = resid + min(0.0, db - floor)
    return resid


def check_resid_floor():
    """True when the residual death benefit is the maximum of its two limbs, every month."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_resid_floor_resid(t)) <= tol
               for t in range(proj_len()))


def check_cv_carve_out_resid(t):
    """The carve-out residual at **month-end** t; zero everywhere.

    On the month-end clock, so :func:`check_cv_carve_out` sweeps ``0 … proj_len()``
    rather than the frame.

    ``min(0, CV'(t) - CV(t))``.  The consumer-protection design the carve-out exists to
    produce is that **a CI claimant is never worse off on surrender than an unaccelerated
    policyholder at the same duration** [S2] [S4], and this is that statement as an
    inequality with a signed residual.  It is not tautological: it fails the moment the
    suppression is applied to the post-CI cohort, which is the natural mistake to make when
    one surrender-value scale is run over one aggregate policy count.
    """
    return min(0.0, cv_pp_ci(t) - cv_pp(t))


def check_cv_carve_out():
    """True when the post-CI surrender value is never below the pre-CI one."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_cv_carve_out_resid(t)) <= tol
               for t in range(proj_len() + 1))


def check_loan_roll_fwd_resid(t):
    """The 보험계약대출 roll-forward residual over month t; zero everywhere.

    ``L(t + 1) - (L(t) + Delta(t + 1))(1 + j_L)``, the balance the month closes with
    against the one it opened with and the draw taken at its closing month-end.
    Identically zero in the base run, where there is no loan at all; non-trivial the moment
    the module is switched on, which is the point of it.
    """
    return (loan_pp(t + 1)
            - (loan_pp(t) + pol_loan_draw(t + 1)) * (1.0 + i_loan_mth()))


def check_loan_roll_fwd():
    """True when the loan balance accumulates at ``j_L`` in every month."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_loan_roll_fwd_resid(t)) <= tol
               for t in range(proj_len() - 1))


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in month t; zero everywhere.

    :func:`net_cf` less the published ``result_cf()`` columns of the same row.  It closes
    the loop between the total benefit outgo and the five kinds that make it up, so a
    sixth kind added to :func:`claims` and left out of the statement shows up here rather
    than silently vanishing from it.
    """
    return (net_cf(t) - premiums(t) + claims(t, "CI") + claims(t, "DEATH")
            + claims(t, "DEATH_CI") + claims(t, "LAPSE")
            + claims(t, "LAPSE_CI") + claim_expenses(t) + expenses(t)
            + commissions(t))


def check_net_cf():
    """True when the net cash flow equals the sum of its published columns, every month."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(proj_len()))


def result_cf():
    """Result table of cash flows, indexed by the 0-based month t.

    ``pols_if`` is the start-of-month count of policies in force in **both** states, which
    is the weight on the maintenance expense of the same row; the decrement-weighted
    figures are in ``result_pols()``.  ``net_cf`` carries the notes' own income-positive
    sign.  ``expenses`` is acquisition and maintenance; the claim handling expense is
    beside it in ``claim_expenses``, as in every model in the sister libraries.  The five
    ``claims_*`` columns are published rather than their total, so that the columns sum to
    ``net_cf`` and the acceleration can be read apart from the death benefit it
    accelerates.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_ci": [claims(t, "CI") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_death_ci": [claims(t, "DEATH_CI") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_lapse_ci": [claims(t, "LAPSE_CI") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by the month t.

    The two states side by side, so that the migration from ``pols_if_pre`` to
    ``pols_if_ci`` — which is the product — can be read directly.  The three rate columns
    are the **monthly** decrements actually applied; their annual parents are
    ``mort_rate``, ``ci_rate`` and ``lapse_rate``, which hold the figures the sources
    tabulate.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_if_pre": [pols_if_pre(t) for t in ts],
            "pols_if_ci": [pols_if_ci(t) for t in ts],
            "pols_if_pay": [pols_if_pay(t) for t in ts],
            "pols_ci": [pols_ci(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_death_ci": [pols_death_ci(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_lapse_ci": [pols_lapse_ci(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "ci_rate_mth": [ci_rate_mth(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """Result table of the account, the surrender values and the benefit levels, by t.

    Indexed by the **month** ``t``, like ``result_cf()``, and every state column is the
    value at the month-end that **closes** that month, ``t + 1`` — the amount a claim or
    a surrender arising in the row's own month is actually paid.  So row ``t = 0`` carries
    ``V(1)``, the account at the first month-end, and the issue-instant values
    ``V(0) = 0`` and ``SC(0) = SC_max`` are one step off the top of the table, reachable
    from the cells themselves.  ``accel_benefit_pp`` and ``resid_nominal_pp`` are read at
    the cohort label ``t + 1``, which is the full-benefit cohort the row's own
    accelerations form; ``loan_pp`` is the balance the row opens with, as in ``claims()``.

    ``cv_pp`` is the amount payable before a CI event and ``cv_pp_ci`` the amount payable
    after one, so the carve-out and the step at 납입완료 can be read off the same table.
    ``resid_db_avg_pp`` against ``resid_nominal_pp`` at any duration shows how far the 105%
    account floor has taken over the residual.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pol_val_pp": [pol_val_pp(t + 1) for t in ts],
            "surr_chg_pp": [surr_chg_pp(t + 1) for t in ts],
            "cv_std_pp": [cv_std_pp(t + 1) for t in ts],
            "cv_pp": [cv_pp(t + 1) for t in ts],
            "cv_pp_ci": [cv_pp_ci(t + 1) for t in ts],
            "base_benefit_pp": [base_benefit_pp(t + 1) for t in ts],
            "accel_benefit_pp": [accel_benefit_pp(t + 1) for t in ts],
            "resid_nominal_pp": [resid_nominal_pp(t + 1) for t in ts],
            "resid_db_avg_pp": [resid_db_avg_pp(t) for t in ts],
            "loan_pp": [loan_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

prem_int_rate = 0.025

i_loan = 0.04

loan_cap_rate = 0.8

net_prem_ratio = 0.8

surr_chg_rate = 0.05

surr_chg_coef_cap = 20

surr_chg_sa_rate = 0.01

surr_chg_years_cap = 7

ci_cover_end_age = 100

ci_wait_days = 90

first_year_factor = 0.5

breast_share_m = 0.005

breast_share_f = 0.268

lapse_ll_first = 0.1

lapse_ll_target = 0.001

lapse_post_paidup = 0.008

lapse_ci_factor = 0.5

expense_acq = 500000.0

expense_maint = 5000.0

expense_claim = 300000.0

inflation_rate = 0.01

comm_init_rate = 0.8

comm_renewal_rate = 0.03

roll_fwd_tol = 1e-10

val_tol = 1e-08

math = ("Module", "math")

pd = ("Module", "pandas")
