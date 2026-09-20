# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Term_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy months** and is **0-based**: ``t = 0`` is the first policy month,
period ``t`` runs from time ``t`` to time ``t + 1``, the attained 보험나이 is
``age_at_entry() + t // 12``, the contractual policy year is the derived 1-based label
``t // 12 + 1`` and is never indexed by, and ``proj_len()`` is the *number* of projected
periods, so the frame is ``t = 0, 1, ..., proj_len() - 1`` — lifelib's own
``for t in range(proj_len())``.  A 20년만기 contract projects 240 rows.
On the representative 순수보장형 there is nothing after it —
no 만기보험금, no 해약환급금 at any duration, no run-off and no tail state of any kind
[S1] [S2 제33조제2항] [S12]. On the 만기환급형 variant the last year pays 100% of the
premiums paid and the contract ends there [S1] [S12].

.. rubric:: The age basis

Every age in this model is **보험나이** (*boheom nai*, insurance age): 만나이 with
fractions of six months or more rounded up, incrementing on the **policy anniversary**
and not on the birthday [S2 제22조] [REG-R25 제21조]. It is the contractual age, the index
of every Korean rate card, and the basis the 경험생명표 is graduated on, so the model
point ages, the premium table and the mortality table are all on one basis and no shift
is applied. The one place Korean practice uses 만나이 instead is the 상법 제732조
voidness test for a life under 만 15 [S2 제22조제1항 단서], which is an issue rule and not
a projection quantity. Reading a 만나이 model point against this table would understate
the rate by about half a year of ageing on every row.

.. rubric:: Where the horizon ends

This is a product question rather than a convention, and on a Korean term policy it is
the contract-boundary question in disguise.

A **비갱신형** (*bi-gaengsinhyeong*, non-renewable) contract has one 보험기간, one premium
and no repricing [S1] [S12], so ``proj_len() = policy_term()``.

A **갱신형** (*gaengsinhyeong*, renewable) contract renews automatically and negative-
option — unless the policyholder objects 15 days before expiry — with **no 고지, no
underwriting and no health condition**, at attained 보험나이 on the whole 기초율 then in
force, on a new product code, until it reaches the **renewal ceiling of 보험나이 80**
[S6] [S9] [S15]. So the 보험기간 of the contract in force is one cycle and the horizon of
the cash flows the contract generates is the ceiling: ``proj_len() = renew_ceiling() -
age_at_entry()``, and a ten-year cycle issued at 40 is projected for forty years across
four priced cycles. ``contract_boundary = current_term`` truncates instead at the end of
the cycle in force, which is the short reading of the boundary. Model points 3 and 4 are
the same cell on the two readings.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/term_life/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_KR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Term_KR_S.Data`, reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
rate_class_file         data.rate_class_table()             rate_class_table.csv
prem_rate_file          data.prem_rate_table()              prem_rate_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind``
string, ``pols_if_at(t, timing)`` for the within-year in-force reads. The technical notes
use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ============================
Notes symbol               Cells                           Meaning
=========================  ==============================  ============================
(row label)                model_point()                   The selected model point row
t                          (the index of result_cf)        Policy month index, 0-based
y(t)                       policy_year(t)                  Policy year label, t // 12 + 1
x                          age_at_entry()                  가입나이, 보험나이
x + floor(t/12)            age(t)                          Attained 보험나이 at time t
(none)                     sex()                           Rating factor, M or F
(none)                     renewal_type()                  gaengsin or bi_gaengsin
(none)                     rate_class()                    표준체 / 비흡연자 / 건강체 ...
(none)                     maturity_form()                 pure or rop (만기환급형)
n                          policy_term()                   보험기간, in years
n_p                        pay_term()                      납입기간, in years
w_r                        renew_ceiling()                 보험나이 renewal stops
(horizon)                  horizon_ceiling()               Years from entry to w_r
N_y                        proj_years()                    Horizon in policy years
N                          proj_len()                      Projected months, 12 N_y;
                                                           the frame is t = 0..N-1
(none)                     contract_boundary()             ceiling or current_term
k                          term_index(t)                   Renewal index, 1 in the first
x_k                        term_start_age(k)               보험나이 at cycle k start
m_k                        term_len(k)                     Length of cycle k, truncated
m_k^p                      term_pay_years(k)               Paying years inside cycle k
SA                         sum_assured()                   보험가입금액, level
i_p                        prem_int_rate                   적용이율, 2.50%
g                          pay_factor(k)                   Shortened-pay uplift
r(sex, x, m)               prem_rate_mth(t)                Rate per 100,000,000 of cover
qbar(x, m)                 mort_table_mean(x, m)           Mean table rate over m years
P_m(k)                     premium_mth_pp(t)               Monthly office premium, the
                                                           month's actual premium income
P_a(k)                     prem_pp(t)                      Annualized premium, 12 P_m
(none)                     prem_payable(t)                 1 inside the 납입기간, else 0
(none)                     cum_prem_pp(t)                  Premiums paid to date, per pol
(table)                    mort_rate_at_age(x)             표준체 table rate at an age
(table)                    acc_mort_rate_at_age(x)         예정 재해사망률 at an age
(class)                    class_mort_ratio()              Rate-class mortality ratio
(class)                    class_prem_ratio()              Rate-class premium ratio
(basis)                    mort_rate_base(t)               Class table rate in period t
(margin removal)           mort_be_factor                  Best-estimate factor, 0.85
q(t)                       mort_rate(t)                    Annual death rate at age(t)
q^m(t)                     mort_rate_mth(t)                Monthly death decrement
a_q(t)                     acc_mort_share(t)               Accidental share of q(t)
w(t)                       lapse_rate(t)                   Annual ordinary lapse rate
w^m(t)                     lapse_rate_mth(t)               Monthly lapse decrement
d(t)                       renewal_decline_rate(t)         Renewal-decline rate
d_0                        renewal_decline_base            Flat decline rate, 20%
beta, d_max                renewal_decline_beta, _max      Decline elasticity module
l(t)                       pols_if(t)                      In force at time t, l(0) = 1
(within-year)              pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / ...
D(t)                       pols_death(t)                   Expected death claims
(none)                     pols_lapse(t)                   Ordinary lapses
(none)                     pols_decline(t)                 Renewal declines
(none)                     pols_maturity(t)                Cover ending at the horizon
lap(t)                     pols_lapse_pool(t)              Reinstatable population
rho                        reinstate_rate                  Reinstatement rate
(window)                   reinstate_window                36 months [S2 제28조]
(none)                     pols_reinstate(t)               부활 into l(t+1)
(none)                     pols_lapse_expire(t)            Pool leavers, window expired
u(t)                       wop_waived_frac(t)              Fraction premium-waived
(none)                     pols_waived(t)                  Policies with premiums waived
(none)                     pols_payer(t)                   Policies paying premium
A                          accel_amount()                  선지급 accelerated amount
i_s                        accel_disc_rate                 평균공시이율, 2.50%
a(t)                       accel_share(t)                  Acceleration take-up
(payout formula)           accel_payout_pp(t)              Discounted acceleration
P_a x l                    premiums(t)                     Premium income
SA x D(t)                  claims(t, kind)                 Benefit outgo by kind
ec                         expense_claim                   Claim expense per claim
ec x D(t)                  claim_expenses(t)               Claim expense outgo
E0                         expense_acq                     Acquisition expense
e(t)                       expenses(t)                     Acquisition + maintenance
c0                         comm_init_pp()                  Initial commission per policy
c_r                        comm_renewal_rate               Renewal commission rate
(none)                     comm_new_term(t)                Commission at a 갱신
(none)                     commissions(t)                  Commission outgo
CF(t)                      net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ============================

Four names needed care.

``d(t)`` is spelled :func:`renewal_decline_rate` and never any variant of ``lapse``, and
never ``renew_rate``, which reads as its complement. It is a different event at a
different time from a different population.

``q(t)`` is the decrement and ``qbar(x, m)`` is a mean of **table** rates used by the
premium scale. Those are different quantities on different bases — one is best-estimate
and one is not — so :func:`mort_rate` is the decrement and :func:`mort_table_mean`
averages :func:`mort_rate_at_age`, which reads the table unadjusted. Feeding the
best-estimate rate into the premium extension would move a premium scale by an assumption
that has nothing to do with pricing.

``P_m(k)`` is indexed by the *renewal cycle* in the notes and by the period index here.
:func:`premium_mth_pp` takes ``t`` and resolves the cycle through :func:`term_index`,
which keeps every cash flow line indexed the same way. The premium is nonetheless level
within a 보험기간, and :func:`check_prem_level` asserts it. On a monthly grid it is also
the **cash flow itself**: 월납 is the base frequency and the only one on seven of the
retrieved products [S1] [S6] [S8] [S9] [S12] [S17] [S18], so the month's premium income is
the month's premium and no annualization convention stands between the rate card and the
statement. ``P_a = 12 P_m`` survives as a reporting quantity and as the base of the
commission scale, not as a cash flow.

``lap(t)`` is spelled :func:`pols_lapse_pool` because it is a **stock**, the lapsed lives
still inside the three-year 부활 window, whereas :func:`pols_lapse` is the year's **flow**
into it.

.. rubric:: 갱신 reprices, and it also resets things a 更新 does not

At a renewal boundary the premium is recomputed at attained 보험나이 on the whole 기초율
then in force — 적용이율, 계약체결비용, 계약관리비용 and 위험률, each named in the
carriers' own words [S9] [S15] — and the renewal is issued on a **new product code**
[S9] [S15]. What carries and what does not is the crux of the boundary question, and the
Korean answer is mixed:

- ``pols_if`` is continuous across the boundary. There is no reset to 1: a renewal
  reprices the contract, it does not re-issue it to a new life.
- **A premium waiver already running does not survive the renewal.** 흥국생명, verbatim:
  「다만, 새로이 갱신되는 계약에서는 갱신 전 보험료 납입면제 사유로 인한 보험료 납입면제를
  적용하지 않고, 보험료를 계속 납입하여야 합니다」 [S6]. A disabled life resumes paying.
  This is a material cash-flow rule with no ``jplib`` counterpart, and it is the sharpest
  single piece of evidence that a Korean renewal really is a fresh contract.
  :func:`wop_waived_frac` therefore resets to zero in the first period of every renewed
  cycle, and :func:`check_waiver_reset` asserts it.
- **The suicide and contestability clocks do not restart.** They run from the original
  보장개시일 and restart only on 부활 [S2 제6조·제28조]. Neither is monetized in the base
  run; both are stated here because a model that treated each renewed cycle as a fresh
  policy would get persistency, the strain pattern and both clocks wrong at once.
- No acquisition expense and, in the base run, no commission is paid at a renewal
  (``comm_new_term_rate`` is 0). That is a choice, not a fact — a Korean renewal is a new
  product code, which is an argument the other way — and switching it on changes the sign
  of the cash flow in the earlier repriced years, where the commission on the new premium
  is larger than the year's whole margin.

Truncation at the ceiling shortens the **cycle**, not the horizon: 「갱신일부터 최종
갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 갱신일부터 갱신계약의 보험기간
종료일까지 이 계약의 보험기간으로 합니다」 [S6]. That is :func:`term_len`.

.. rubric:: Renewal decline is not lapse

:func:`renewal_decline_rate` is non-zero **only** in the last month of a cycle, and the
exits it produces are taken **after** mortality and **after** ordinary lapse. The ordering
is not cosmetic: reversing it applies the decline to lives that died or lapsed during that
month and understates the exposure of the renewed cohort. On a monthly grid the decline is
also visibly the discrete event it is — one row of 240 carries it, where an annual grid put
it in the same period as a year of continuous lapse.

The rate is **[std] 20%** and is published nowhere in Korea for any product — the
disclosure requires the price path and not the persistency path [S7] [S16]. It is argued
from three directions. The option is negative and the notice is 15 days, so inertia
dominates and the rate must sit well below a positive-election rate. The step is large
and disclosed in advance — 2.33x at the first renewal on the published path [S7] — so an
insurer expecting no reaction would not need to print the projection. And the nearest
Korean supervisory calibration of a behavioural jump at a discrete contractual event is
the FSS's floor of **at least 30% additional lapse** where a 단기납 종신보험's refund
ratio peaks [REG-R27]; a renewal offers the policyholder no cash and no maturing option,
only a higher price, so 20% sits deliberately below that floor. An arguable range is
roughly 5% to 40%, and ``renewal_decline_max`` is set at the top of it.

Zero in the final projected month, where cover ends at the ceiling rather than renewing,
and zero on a 비갱신형 point.

.. rubric:: One decrement, one benefit — and the disability benefit Korea does not have

A Korean term policy pays the 보험가입금액 on death within the 보험기간 and nothing else,
and payment terminates the contract immediately and automatically [S2 제4조·제23조].
There is **no Korean analogue of the Japanese 高度障害保険金**, so unlike ``Term_JP_S``
this model carries no competing benefit on one sum assured. What the 장해 (*janghae*,
disability) state does instead is **switch the premium off** — the 보험료 납입면제 on a
장해지급률 of 50% or more from any cause, in the 주계약 at no separate premium [S1]
[S2 제5조] [S6] [S8] [S9] [S10] [S11] [S12] — so the state space is: in force paying, in
force premium-waived, dead, lapsed, and on a 갱신형 declined at renewal.

The waiver is **cause-neutral**: sickness qualifies equally with accident, so the waiver
incidence is a general disability incidence and **must not** be scaled off
:func:`mort_rate`. No Korean document publishes a 50%-plus 장해 incidence and the
참조순보험요율 behind it is not public [REG-R4] [R19], so ``wop_inc_rate`` is an
**arbitrary placeholder** and the module is off on eight of the ten shipped model points.

.. rubric:: Lapse pays nothing, and there is no policy loan

On the representative 전기납 무해지 contract the 약관 pays **nothing at any duration**:
「보험료 납입기간이 보험기간과 동일한 계약 … 의 경우에는 보험기간 중 계약이 해지될 경우
해약환급금을 지급하지 않습니다」 [S2 제33조제2항]. 한화생명's published 해약환급금 예시
for the same shape shows 환급률 0.0% at all eleven durations printed, for both sexes [S1].
So an ordinary lapse is a pure decrement: it moves :func:`pols_if` and pays nothing.
``claims(t, "LAPSE")`` exists and returns zero, and ``result_cf()`` carries the zero
column, because the 표준형 comparator does have a value and a reader must not infer one
from the product class.

On a **shortened-pay** 무해지 contract a value does arise after 납입완료 — 50% of the
표준형's [S1] [S2 제33조제2항] [S12] — and this model does not compute it. The 표준형
해약환급금 is the 순보험료식 계약자적립액 less the 해약공제액, which is the savings
chassis's quantity and belongs to ``WholeLife_KR_S``; projecting it here would duplicate
that machinery in the one product that exists to demonstrate the decrement recursion
without it. What the shortened-pay model point does exercise is the **lapse-rate step**
at 납입완료 — the 적용해지율 falls to 0.1% and then steps to the 0.8% ultimate
[REG-R27] — and the premium ceasing. Model point 5 is that point, and the omitted
surrender value is recorded here rather than left to be discovered.

There is likewise **no 보험계약대출 and no 자동대출납입 in fact**. Both are granted by the
약관 [S2 제26조·제34조] and both are inoperative, there being no surrender value to lend
against — a point the supervisor made in terms of the 무해지 form generally [REG-R28].
납입최고 (14 days), then 실효, then 부활-or-not is the whole persistency machinery here,
which is part of why this is the right chassis to specify first.

.. rubric:: The premium chassis, and where it stops being sourced

Korean rate cards are published and the anchor cell is published twice, so the level is
sourced where ``jplib``'s and ``uklib``'s are not::

    P_m(k) = r(form, sex, x_k, m_k) * c_p(class, sex) * g(k) * SA / 100,000,000
    x_k    = x + (k - 1) * n
    m_k    = min(n, w_r - x_k)
    P_a(k) = 12 * P_m(k)

rounded to the nearest 10 won before annualization, which is the granularity the anchor
carrier quotes [S12]. **No flat policy element can be separated out**: unlike ``jplib``'s
オリックス生命 grid, every Korean grid retrieved fixes the sum assured and varies age, sex,
rate class or product form instead [S1] [S8] [S11] [S12] [S14], so the office premium is
treated as proportional in the sum assured and the approximation is recorded rather than
hidden. One consequence is visible in the data: female premiums run at 52-56% of male
across the six direct writers on the same cell and from 47% to 90% across the eleven
face-to-face and simplified-issue rows [S4] -- consistent with a flat per-policy loading
on a small risk premium, but not proof of one, the two bands overlapping at the bottom.

``g(k)`` is the **[std]** shortened-pay uplift, ``a-due(m_k) / a-due(m_k^p)`` at the
적용이율 of 2.50% [S1] [S12]. No Korean document retrieved publishes a shortened-pay
premium for a term contract at all, so an equivalence had to be chosen; a certain annuity
rather than a life annuity is a simplification that overstates the uplift slightly, by
the mortality that would have been shed between the two periods.

``P_a = 12 P_m`` is a **reporting** quantity on this grid and no longer a cash flow
convention: the monthly step collects ``P_m`` in the month it falls due, so the half-year
of interest an annual grid used to gain -- 1.136% of a year's premium at the 적용이율,
the mean deferral of the twelve payments being 5.5/12 of a year -- is not gained here.
``P_a`` survives because the rate card is quoted monthly and read annually, and because
the commission scale is written on an annualized premium.

.. rubric:: Modules that are off in the base run

Five optional constructions are implemented and switched off on the anchor cell, so that
the base run reproduces the worked example while the machinery stays visible and
testable. All five are model point columns:

- **보험료 납입면제** (``waiver``), the premium waiver on a 50%-plus 장해지급률 from any
  cause. On for model points 3 and 4, which are 갱신형, so that the waiver **not**
  surviving the renewal is exercised and not merely asserted [S6].
- **선지급서비스특약** (``accel``), the accelerated death benefit on a 12-month
  prognosis, discounted at the 평균공시이율, capped at 50% of the sum assured aggregated
  to 50,000,000 won, with up to 10,000,000 won payable in full [S2 제3조·제4조]. On for
  model points 7 and 9 — one where the cap does not bind and one where it does. At the
  anchor's 100,000,000 won the cap is **exactly reached and reduces nothing**, which
  :func:`accel_cap_binds` reports with a strict inequality.
- **부활** (``reinstatement``), the lapsed-but-reinstatable population and its three-year
  window [S2 제28조]. On for model point 8. The window is sourced and expressly covers a
  policy with no surrender value — 「해약환급금이 없는 경우를 포함합니다」 — so a 무해지
  policy is **always** eligible; the rate beside it is an arbitrary placeholder.
- **재해사망 uplift** (``acc_death``), the product 형 paying 2x the sum assured on
  재해사망 and 1x otherwise [S6] [S10]. On for model point 10. It is modelled as a split
  of the existing decrement using the published 예정 재해사망률, never as a second
  decrement.
- **Contract boundary** (``contract_boundary``), ``current_term`` truncating at the end
  of the cycle in force. ``ceiling`` on model point 3, ``current_term`` on model point 4.

Two further switches are References rather than columns: the **renewal-decline
elasticity** ``d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta)`` with ``beta = 0`` giving the
flat 20%, and **commission at a 갱신** with ``comm_new_term_rate = 0``.

.. rubric:: Sign convention and the timing of the monthly step

:func:`net_cf` is **income positive** — premiums less claims, claim expense, expenses and
commission — which is the library-wide sign, so there is no outgo-positive
``liability_cf`` companion to publish: one stream, one sign, one name.

Premiums are monthly in advance, claims fall at the end of the month of death, and the
decrements act inside the month they belong to. The annual grid this model was first
written on carried a matched pair of offsetting distortions — a whole year's premium
collected from lives that died or lapsed in the year, against a death benefit paid a year
late — and the monthly step removes both rather than netting them: the residual timing
error is now half a month either way instead of half a year.

.. rubric:: What is not modelled, and why

**감액** (a reduction in the sum assured) changes ``SA`` and ``P_a`` together and pays
nothing on this form, so it is a model point re-parameterization rather than a decrement
**[std scope]** [S2] [S12]. **증액** is not available at all; a new contract with fresh
underwriting is required [S1] [S12]. **청약철회** is out of scope: the projection begins
with cover in force and the 15-day statutory population already out [S2 제18조]
[REG-R51]. The **위법계약의 해지** — which returns the whole 계약자적립액 with no
surrender charge [S2 제30조의2] [REG-R25 제29조의2], and so is worth the entire value on
a form whose ordinary surrender pays nothing — is not modelled, no incidence of
mis-selling findings being published; it is stated because a Korean model treating the
surrender value as uniformly nil would be wrong about a real if small cash flow. The
**rate class is a state and not a parameter**: a Korean class rider tracks smoking status
for the life of the contract and moves in **both** directions, with a 정산차액 recovered
or the 보험가입금액 reduced in the ratio of the two premiums [S2 건강체서비스특약Ⅱ
제4조] [S11] [S12]. This model does not carry the transition, and a model that later needs
it will need a transition and not a relabelling. And the **claim timetable** — 3영업일,
10영업일 where investigation is needed, 30영업일 outside — is contractual and real, but no
Korean document publishes the mix of claims falling into the three bands, so the
composite pays at the projection step in which the claim arises and says so [S2 제9조].
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
    """The sex (M / F) of the 피보험자, a rating factor of every Korean rate card [S4]."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def age_at_entry():
    """x: the 가입나이 (issue age) in **보험나이** [S2 제22조] [REG-R25 제21조].

    만나이 with fractions of six months or more rounded up, incrementing on the policy
    anniversary and not on the birthday, so the whole model is on one age basis and no
    shift is applied anywhere.  The composite's envelope is 만19세 to 보험나이 65
    [S1] [S6] [S9] [S11] [S12]; the mixed basis in that sentence is the documents' own,
    a minimum written 만19세 being 만나이 and a maximum written 65세 being 보험나이.
    """
    return int(model_point()["issue_age"])


def renewal_type():
    """``gaengsin`` for a 갱신형 contract, ``bi_gaengsin`` for a 비갱신형 one.

    The single most consequential model point attribute.  A 갱신형 contract renews
    automatically at attained 보험나이 to the ceiling with no 고지 and no underwriting
    [S6] [S9] [S15]; a 비갱신형 contract has one 보험기간, one premium and no repricing
    [S1] [S12], and applying the renewal machinery to it invents cover it does not have.
    비갱신형 is the base because it is the market: only three of the 45 disclosed
    products renew and only two carriers sell a renewable term at all [S4].
    """
    v = model_point()["renewal_type"]
    if v not in ("gaengsin", "bi_gaengsin"):
        raise ValueError("invalid renewal_type: expected gaengsin or bi_gaengsin")
    return v


def rate_class():
    """The underwriting class: 표준체 / 비흡연자 / 건강체 / 슈퍼건강체.

    Spelled ``standard`` / ``nonsmoker`` / ``preferred`` / ``super_preferred`` so that
    ``run.py`` stays ASCII.  Observed class counts run from one to four [S15] [S11]
    [S12]; the base run is 표준체 because a class structure multiplies the premium basis
    without changing a contractual mechanic.  It is parameterized rather than dropped
    because **Korea publishes the mortality behind it** — two carriers print a full
    예정 경험사망률 table per class [S11] [S12] — which no other library here can do.

    The class is a **state and not a parameter** in the contract: the rider tracks
    smoking status for the life of the policy and moves in both directions [S2
    건강체서비스특약Ⅱ 제4조].  This model does not carry the transition.
    """
    v = model_point()["rate_class"]
    if v not in ("standard", "nonsmoker", "preferred", "super_preferred"):
        raise ValueError("invalid rate_class")
    return v


def maturity_form():
    """``pure`` for the 순수보장형, ``rop`` for the 만기환급형 [S1] [S8] [S12].

    The 순수보장형 has no 만기보험금 at all and passes the 보장성보험 test by
    construction [REG-R9].  The 만기환급형 returns exactly 100% of 「이미 납입한 주계약
    보험료」 at maturity, computed **as if any waived premiums had been paid** [S1] [S12],
    and passes the same test by design; 감독규정 제7-60조제9호 is part of why it returns
    exactly 100% and not less [REG-R16].  It costs 9.42x the 순수보장형 at male 40 and
    10.90x at female 40 [S12], which is what a savings contract with a small amount of
    insurance stapled to it looks like.
    """
    v = model_point()["maturity_form"]
    if v not in ("pure", "rop"):
        raise ValueError("invalid maturity_form: expected pure or rop")
    return v


def policy_term():
    """n: the 보험기간 in years — the *priced* term, not the projection horizon.

    Read from ``term_y`` on a 년만기 point and implied by ``expiry_age`` on a 세만기 one;
    every carrier offering a menu offers both shapes and the 세만기 ceiling has crept
    from 80세 to 90세 and 100세 [S1] [S9] [S12] [S17].  On a 갱신형 contract this is the
    length of one **cycle** and the horizon is :func:`horizon_ceiling`, which is longer.
    """
    v = int(model_point()["term_y"])
    if v > 0:
        return v
    return int(model_point()["expiry_age"]) - age_at_entry()


def pay_term():
    """n_p: the 납입기간, in years from issue, over which premium is payable.

    ``0`` in the model point table means **전기납** (*jeongi-nap*, whole-term pay), which
    is the disclosure's basis [S5] and available at every carrier, and which on this
    chassis means paying for the whole projection — so the payment period never ends
    before the cover does and the post-완납 machinery never fires [S2 제33조제2항].
    Shortened pay is carried because **it is the only way the 무해지 form's post-완납
    step-up can arise at all**, and with it the 0.8% ultimate lapse rate [REG-R27].
    """
    v = int(model_point()["pay_term_y"])
    return proj_years() if v <= 0 else v


def renew_ceiling():
    """w_r: the 보험나이 at which renewal stops, 80 on the composite [S6].

    Observed ceilings are 80세 [S6], five years' total cover [S15] and the main
    contract's expiry [S9]; the composite takes 흥국생명's, which is the only one that
    supports a multi-cycle projection.  Inert on a 비갱신형 point.
    """
    return int(model_point()["renew_ceiling"])


def sum_assured():
    """SA: the 보험가입금액, level for the whole term and unchanged through a 갱신.

    Paid on death within the 보험기간 and on nothing else; payment terminates the
    contract [S2 제4조·제23조].  The composite's envelope is 30,000,000 to 500,000,000
    won in 10,000,000 won units [S6] [S9] [S11] [S12] [S14]; 체증형 (escalating) is
    corporate-only and 체감형 (decreasing) is a disclosure category with no retail
    product in it [S4] [S18].
    """
    return float(model_point()["sum_assured"])


def premium_mode():
    """The 납입주기 — **월납** (monthly) in the base run [S1] [S6] [S8] [S9] [S12].

    Monthly is available at every carrier retrieved, is the only frequency on seven of the
    retrieved products, is the disclosure's basis [S5] and is half of the 감독규정
    기준연령 요건 [REG-R9].  It is the projection's own step, so the mode is no longer a
    convention the grid has to absorb: the month's premium income is ``premium_mth_pp``,
    collected in the month it falls due.  A non-월납 mode would need its own
    ``prem_mode_months`` schedule and is not shipped, every retrieved rate card being
    quoted monthly.
    """
    return model_point()["premium_mode"]


def contract_boundary():
    """``ceiling`` or ``current_term``: how far the liability is projected.

    A Korean 갱신형 reprices the *entire* 기초율 at renewal, 위험률 included, and the
    carriers say so in terms [S9] [S15]; the renewal is issued on a new product code
    [S9] [S15]; and a waiver already running is extinguished [S6].  Against that, the
    renewal is **guaranteed-issue** — no 고지, no underwriting, no health condition [S6]
    [S9] [S15] — so the repricing is at portfolio level and cannot reflect the risks of
    the particular policyholder, which is the test that keeps a renewal inside the
    boundary.  Nothing retrieved settles it [REG-R60], so the model does not rule: it
    projects to the ceiling in the base run **[std]** and carries the truncation as a
    switch.  Naming the convention is part of reporting the number.
    """
    v = model_point()["contract_boundary"]
    if v not in ("ceiling", "current_term"):
        raise ValueError("invalid contract_boundary")
    return v


def acc_death():
    """Whether the 재해사망 uplift module is on; false in the base run [S6] [S10].

    Two of nine carriers sell it, and both sell it as a **product 형 rather than a
    rider**, paying twice the 보험가입금액 on 재해사망 and once otherwise.  It is cheap:
    on the shipped table the 예정 재해사망률 [S6] is about a third of the all-cause rate
    [S12] at male 20 and about a tenth of it at male 60, so a doubled benefit costs a
    fraction of the base risk premium — which is why it is bundled into the base price
    rather than priced separately.  One structural asymmetry is worth recording: 흥국생명
    does not sell its 기본형 to women at all, so a female life there must buy the
    보장추가형 and the disclosure prints 0 won in the 기본형 female column [S4] [S6].
    """
    return bool(model_point()["acc_death"])


def waiver():
    """Whether the 보험료 납입면제 module is on; false in the base run.

    The trigger is identical at eight carriers in identical words: a 장해지급률 summing
    to **50% or more** from 「동일한 재해 또는 재해이외의 동일한 원인」, waiving 「차회
    이후의 보험료 납입」 with no refund of past premiums, the contract continuing in
    force [S1] [S2 제5조제1항] [S6] [S8] [S9] [S10] [S11] [S12].  It is **cause-neutral**,
    so the incidence is a general disability incidence and not a scaled accident rate,
    and the 장해지급률 is a percentage scale rather than a binary trigger [REG-R25 부표
    3].  On for model points 3 and 4, which are 갱신형, so that the waiver not surviving
    a renewal is exercised [S6].
    """
    return bool(model_point()["waiver"])


def accel():
    """Whether the 선지급서비스특약 module is on; false in the base run [S2] [S12].

    A 제도성특약 attached as standard at every carrier whose full document set was
    retrieved, carrying no separate premium in any of them — that it is genuinely free is
    **[unverified]**, no document stating a nil 특약보험료, but the discount in the
    payment formula supplies the economic reason it can be.  Against Japan's
    リビング・ニーズ特約 the Korean trigger is **12 months rather than six**, the cap is
    **half the sum assured to 50,000,000 won** rather than the whole benefit, and there
    is **no bar on payment near expiry at all**.
    """
    return bool(model_point()["accel"])


def reinstatement():
    """Whether the 부활 module is on; false in the base run [S2 제28조].

    부활 is available for **three years** from the termination date provided the
    surrender value was not drawn — expressly 「해약환급금이 없는 경우를 포함합니다」, so
    a 무해지 policy is **always** eligible — with arrears at 「평균공시이율+1% 범위 내」.
    Reinstatement re-runs the 계약 전 알릴 의무 and **restarts the two-year suicide
    window**, where a 갱신 does not [S2 제6조·제28조].  Off by default because
    ``reinstate_rate`` is an arbitrary placeholder with a material persistency effect: no
    Korean document publishes a reinstatement rate.  What *is* published, and is
    therefore not [std], is the window.
    """
    return bool(model_point()["reinstatement"])


def horizon_ceiling():
    """The number of policy **years** from entry to the renewal ceiling.

    ``renew_ceiling() - age_at_entry()`` on a 갱신형 point, because the contract renews
    until it gets there [S6]; the term itself on a 비갱신형 point, which never renews
    [S1] [S12].
    """
    if renewal_type() == "gaengsin":
        return renew_ceiling() - age_at_entry()
    return policy_term()


def proj_years():
    """N_y: the number of projected policy **years** — :func:`horizon_ceiling`, or the cycle.

    The horizon in the unit the contract states it in.  ``contract_boundary =
    current_term`` truncates at the end of the 보험기간 in force, which for a policy
    projected from issue is ``policy_term()``.  On a 비갱신형 point the two coincide.  A
    model that can project to the ceiling can always be truncated to one cycle; the
    reverse is not true, which is why the long reading is the base.

    Kept separate from :func:`proj_len` because the contract is written in years —
    보험기간, 납입기간 and the 보험나이 80 ceiling are all annual quantities — while the
    projection steps in months.  Everything that reads a contractual term in years reads
    this; everything that indexes the grid reads :func:`proj_len`.
    """
    if contract_boundary() == "current_term":
        return min(horizon_ceiling(), policy_term())
    return horizon_ceiling()


def proj_len():
    """N: the **number** of projected policy months, ``12 x proj_years()``.

    The exclusive end of the frame: the projection covers ``t = 0, 1, ..., proj_len() - 1``
    and ``result_cf()`` has ``proj_len()`` rows.  240 on the anchor cell — a 20년만기
    contract projected month by month.

    There is no terminal row beyond the months of cover.  The 순수보장형 pays nothing at
    the horizon and the 만기환급형's 만기보험금 falls in the last month of cover along with
    :func:`pols_maturity`, so nothing is left over to need an instant of its own.
    """
    return 12 * proj_years()


def age(t):
    """x + floor(t / 12): the attained **보험나이** in policy month t.

    보험나이 increments on the **policy anniversary** and not on the birthday
    [S2 제22조], and a monthly grid anchored at issue steps its anniversaries exactly
    twelve months apart, so ``t // 12`` is the number of anniversaries passed and the
    alignment is exact rather than approximate.  ``t`` is 0-based, so ``age(0)`` is the
    가입나이 itself and the attained age advances at ``t = 12, 24, ...``.
    """
    return age_at_entry() + t // 12


def policy_year(t):
    """y(t): the contractual policy year containing month t, ``t // 12 + 1``.

    The **1-based** contractual label, derived from the 0-based month index and never the
    index itself.  Month ``t = 0`` falls in policy year 1.  It is what the 납입기간, the
    보험기간 and the disclosed 적용해지율 vector are written in, so :func:`lapse_rate`
    and :func:`prem_payable` read it rather than counting months by hand.
    """
    return t // 12 + 1


def term_index(t):
    """k: the renewal index — 1 in the original 보험기간, 2 after the first 갱신.

    ``1 + floor(t / n)`` on a 갱신형 point; always 1 on a 비갱신형 one, which never
    renews [S1] [S12].  **The premium is a function of k and not of t**, which is the
    state variable a Korean protection model needs: a model that indexes the premium by
    policy year cannot represent a 갱신형, and one that carries a single level premium
    across a renewal boundary silently converts a 갱신형 into a 비갱신형 at the wrong
    price.
    """
    if renewal_type() != "gaengsin":
        return 1
    return 1 + (t // 12) // policy_term()


def term_start_age(k):
    """x_k: the attained 보험나이 at which cycle k starts, ``x + (k - 1) n``.

    ``k`` is the contractual 1-based cycle label, not the 0-based time index: cycle 1 is
    the original 보험기간 and starts at ``t = 0``, cycle ``k`` starts at ``t = (k - 1) n``.
    """
    if renewal_type() != "gaengsin":
        return age_at_entry()
    return age_at_entry() + (k - 1) * policy_term()


def term_len(k):
    """m_k: the length of cycle k in years, ``min(n, w_r - x_k)``.

    The ceiling **truncates rather than refuses**: 「갱신일부터 최종 갱신계약의 보험기간
    종료일까지가 10년미만일 경우에는 갱신일부터 갱신계약의 보험기간 종료일까지 이 계약의
    보험기간으로 합니다」 [S6].  The truncated cycle is priced over its own shorter
    length, which is why this feeds :func:`prem_rate_mth`.
    """
    if renewal_type() != "gaengsin":
        return policy_term()
    return min(policy_term(), renew_ceiling() - term_start_age(k))


def term_pay_years(k):
    """m_k^p: the years of premium payment falling inside cycle k.

    Equal to :func:`term_len` on a 전기납 contract and on every cycle of a 갱신형 one,
    and shorter on a 비갱신형 contract bought with a shortened 납입기간.  Zero once the
    납입기간 has run out, which cannot happen on the shipped points but is defined so the
    premium formula stays total.
    """
    start = (k - 1) * policy_term() if renewal_type() == "gaengsin" else 0
    return max(0, min(start + term_len(k), pay_term()) - start)


def class_mort_ratio():
    """The rate class's mortality relativity to 표준체, from *rate_class_table.csv*.

    1.000 / 0.828 / 0.723 / 0.583 at male 40 and 1.000 / 0.956 / 0.907 / 0.856 at female
    40, computed from the anchor carrier's own class-by-class 예정 경험사망률 [S12].  A
    second carrier's full table gives 0.597 and 0.861 at the same two cells [S11], so the
    relativity is a market feature rather than one carrier's design.  Held flat across
    ages **[std]**: the disclosures are at ages 20, 40 and 60 and the ratios move little
    between them.
    """
    return float(data.rate_class_table().loc[                        # noqa: F821
        (rate_class(), sex()), "mort_ratio"])


def class_prem_ratio():
    """The rate class's premium relativity to 표준체, from *rate_class_table.csv*.

    1.000 / 0.865 / 0.763 / 0.586 at male 40 and 1.000 / 0.964 / 0.890 / 0.846 at female
    40, from the published premium grid [S12].  It sits **above** the mortality ratio in
    the three male classes and in the female 비흡연자, which is what a loading that does
    not scale with the risk does, and marginally **below** it at female 건강체 (0.890
    against 0.907) and female 슈퍼건강체 (0.846 against 0.856).  Nothing retrieved
    explains the reversal, so the two ratios are carried as separate columns and neither
    is derived from the other.
    """
    return float(data.rate_class_table().loc[                        # noqa: F821
        (rate_class(), sex()), "prem_ratio"])


def mort_rate_at_age(x):
    """The **표준체 table** mortality rate at attained 보험나이 x, unadjusted.

    A **[std]** construction of the 예정 경험사망률 basis: a Makeham law fitted exactly
    to the anchor carrier's three disclosed rates [S12] and tilted above age 60 so that
    the shipped table reproduces the 제10회 경험생명표's published 65세 기대여명 exactly
    [REG-R33]; see :mod:`~.Term_KR_S.Data`.  This is a *pricing* rate with its margin
    still in it, and it is read directly by the premium scale and only through
    :func:`mort_rate_base` by the decrement.
    """
    return float(data.mort_table().loc[(sex(), int(x)), "mort_rate"])  # noqa: F821


def acc_mort_rate_at_age(x):
    """The **예정 재해사망률** (accidental-death rate) at attained 보험나이 x [S6].

    Published by two carriers, who agree to three significant figures at age 20 and to
    within 10% everywhere [S6] [S10] — strong evidence that both take the 보험개발원
    참조 재해사망률 almost unadjusted, where the all-cause rates are heavily adjusted and
    differ by a factor of 1.77 at male 40.  Used only to split the death decrement for
    the 재해사망 uplift variant, never as a decrement of its own.
    """
    return float(data.mort_table().loc[                              # noqa: F821
        (sex(), int(x)), "acc_mort_rate"])


def mort_table_mean(x, m):
    """qbar(x, m): the mean **표준체 table** rate over ages x .. x + m - 1.

    The shape parameter of the **[std]** premium extension.  Deliberately built on the
    table rate rather than on :func:`mort_rate`: a premium scale is not a best-estimate
    quantity, and feeding the best-estimate factor in would move a published rate card by
    an assumption that has nothing to do with pricing.
    """
    return sum(mort_rate_at_age(a)
               for a in range(int(x), int(x) + int(m))) / float(m)


def mort_rate_base(t):
    """The class-adjusted **table** rate at the attained age of period t.

    ``mort_rate_at_age(age(t)) * class_mort_ratio()``.  Still a pricing rate; the
    best-estimate factor is applied by :func:`mort_rate`.  No age-basis shift is applied
    anywhere in this model, both the model point and the table being on 보험나이
    [S2 제22조].
    """
    return mort_rate_at_age(age(t)) * class_mort_ratio()


def mort_rate(t):
    """q(t): the **annual** best-estimate death rate at the attained age of month t.

    ``mort_be_factor`` times the class-adjusted table rate, capped at 1.  **One decrement
    carrying one benefit**: a Korean term policy pays the 보험가입금액 on death and
    nothing else, and payment terminates the contract [S2 제4조·제23조].  There is no
    Korean analogue of the Japanese 高度障害保険金, so unlike ``Term_JP_S`` there is no
    competing benefit to double-count; what the 장해 state does instead is switch the
    premium off, which is :func:`wop_waived_frac`.

    ``mort_be_factor = 0.85`` **[std]** is this model's largest single lever and its
    least evidenced number.  The shipped table is a carrier's 예정 경험사망률, which is a
    *pricing* rate carrying a margin over experience that **no public Korean document
    sizes** — the 산출방법서 in which it would be justified is a 기초서류 filed with the
    FSC and never published [REG-R2].  What can be bracketed is the scale and not the
    margin: seven carriers' disclosures at male 40 run from 0.000480 to 0.000850, a
    factor of 1.77 around the anchor's 0.000650 [S1] [S6] [S8] [S10] [S11] [S12] [S17],
    so the cheapest carrier prices at 0.74x the anchor before any margin is removed.  A
    round 0.85 sits between that and unity and the technical notes carry the sensitivity.
    """
    return min(1.0, mort_be_factor * mort_rate_base(t))              # noqa: F821


def mort_rate_mth(t):
    """q^m(t): the monthly death decrement, ``1 - (1 - q(t))^(1/12)`` **[std]**.

    The uniform-force conversion of the annual best-estimate rate of the policy year month
    ``t`` falls in, which is the conversion every monthly model in this library uses.  The
    annual rate is the quantity the sources publish — every Korean 예정 경험사망률
    disclosure is annual [S12] [S11] [S6] — so the annual rate is the one the model reads
    and the monthly rate is derived from it, never the other way round.

    It is the decrement :func:`pols_death` and :func:`pols_if_at` actually apply.  The
    twelve monthly rates inside a policy year are equal, the annual table rate stepping
    only at each 계약해당일: 보험나이 increments on the anniversary [S2 제22조], so a
    within-year interpolation of the table would be modelling an age the contract does not
    recognize.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def acc_mort_share(t):
    """a_q(t): the accidental share of period t's death decrement [S6] [S10].

    ``acc_mort_rate_at_age / mort_rate_at_age`` on the **표준체 table** basis, so that
    the ratio is not disturbed by the class relativity or the best-estimate factor —
    neither of which has anything to say about the cause of death.  Capped at 1.  It runs
    around 0.35 at age 20 and 0.10 at age 60 on the shipped table, which is the right
    order for a doubled-benefit variant to be cheap enough to bundle into the base price
    rather than price separately.  Reported on every model point; it enters the cash
    flows only where :func:`acc_death` is on.
    """
    return min(1.0, acc_mort_rate_at_age(age(t)) / mort_rate_at_age(age(t)))


def lapse_rate(t):
    """w(t): the ordinary lapse rate applied at the end of period t.

    The **shape is supervisory and not chosen**: the 2024 IFRS17 계리가정 가이드라인 makes
    a **로그-선형 model converging to 0.1%** the 원칙모형 for 무·저해지 business, permits
    only 선형-로그 and 로그-로그 as exceptions and on onerous disclosure conditions, and
    sets a post-완납 ultimate of **0.8%** [REG-R27].  The **endpoints are disclosed**:
    「납입기간 이내에 대하여 경과기간별로 연 0.1%~4.6%, 납입기간 이후에 대하여 경과기간별로
    연 0.7%~1.6%」 at the anchor carrier [S12] and 「연 0.1%~8.4%, 납입기간 이후 연 0.8%」
    at another [S1].  So::

        w(t) = 0.046 * (0.001 / 0.046) ** (t / (n_p - 1))   for t <  n_p
        w(t) = 0.008                                        for t >= n_p

    times ``lapse_be_factor``, read at the **0-based policy year** ``y = policy_year(t) -
    1`` rather than at the month index: the vector is published by 경과기간 in years, so
    the 4.6% upper endpoint covers the whole of the first projected year and the 0.1%
    convergence point the whole of the last paying one.  :func:`lapse_rate_mth` is the
    decrement actually applied.  Two **[std]** steps remain and both are recorded rather
    than absorbed.  Both disclosed ranges are on a **10년납** basis and the composite is
    전기납 over twenty years, so the same endpoints are **stretched over the
    representative's own 납입기간** — which flattens the curve and is why model point 5,
    at 10년납, is the one that reproduces the disclosed shape at its disclosed length.
    And the 적용해지율 is a **pricing** rate for the 무해지 form, deliberately low by
    regulatory design [REG-R19 제7-66조제4항], and is **not** a best-estimate.  Nothing
    retrieved discloses a best-estimate term lapse rate; the only Korean experience datum
    available is a whole-life one, a 저해지 단기납 종신보험 running a 37회차 유지율 of
    50.2% against an assumed 71.5% [R18].  The **direction** of that error is the reason
    ``lapse_be_factor`` exists as a switch and is 1.0 **[std]** in the base run, with the
    sensitivity carried in the technical notes rather than a point estimate dressed as a
    fact.

    A lapse pays nothing on this form: there is no 해약환급금 at any duration
    [S1] [S2 제33조제2항] [S12].
    """
    tbl = data.lapse_table()                                         # noqa: F821
    start = float(tbl.loc["in_payment_start", "lapse_rate"])
    end = float(tbl.loc["in_payment_end", "lapse_rate"])
    post = float(tbl.loc["post_payment", "lapse_rate"])
    n_p = pay_term()
    y = policy_year(t) - 1
    if y >= n_p:
        rate = post
    elif n_p <= 1:
        rate = end
    else:
        rate = start * (end / start) ** (y / (n_p - 1.0))
    return lapse_be_factor * rate                                    # noqa: F821


def lapse_rate_mth(t):
    """w^m(t): the monthly lapse rate, ``1 - (1 - w(t))^(1/12)`` **[std]**.

    The 적용해지율 the supervisor's 원칙모형 prescribes is an **annual** rate by
    duration — 「경과기간별로 연 0.1%~4.6%」 [S12] [REG-R27] — so the annual vector is
    what the model reads and the monthly rate is its uniform-force conversion, level
    inside a policy year and stepping at each 계약해당일.  This is the rate
    :func:`pols_lapse` and :func:`pols_if_at` apply.

    A lapse still pays nothing on this form [S1] [S2 제33조제2항] [S12]; what the monthly
    grid changes is *when* the exposure leaves, not what leaves with it.  Twelve monthly
    exits compound to the year's annual rate exactly, so the year-end in-force is
    unchanged and the mid-year exposure carrying premium and mortality is not — which is
    the whole reason to step monthly.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def renewal_decline_rate(t):
    """d(t): the renewal-decline rate — non-zero **only** in a boundary period **[std]**.

    A boundary period is the **last month** of a cycle that is not the last of the
    projection: with ``t`` 0-based that is ``(t + 1) % 12n == 0`` and ``t < proj_len() -
    1``, so a ten-year cycle declines at ``t = 119, 239, 359`` and the repriced premium
    takes effect at ``t = 120, 240, 360``.

    At each 갱신 date a fraction of the surviving in-force leaves rather than accept the
    repriced contract.  It is **not** ordinary lapse: ordinary lapse is continuous,
    spread through the year and driven by affordability and by competing products,
    whereas this is discrete, concentrated on a single date, and driven by the size of
    the repricing step — a step the policyholder was warned about in the 상품요약서 and
    which, on the published path, is 2.33x at the first renewal and 3.6x at the third
    [S7].  Folding it into :func:`lapse_rate` makes the boundary invisible.

    ``renewal_decline_base = 0.20`` is published nowhere in Korea for any product, and
    that is a real gap rather than a research failure: the 예상 갱신보험료 예시 the
    disclosure requires shows the **price** path and not the persistency path [S7] [S16].
    See the Space docstring for the three-way argument behind the 20% and the 5%-to-40%
    arguable range.

    Zero on a 비갱신형 point, which never renews [S1] [S12], and zero in the final
    projected year, where cover ends at the ceiling rather than renewing.  The optional
    elasticity ``d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta)`` responds to the premium
    jump; ``renewal_decline_beta = 0`` in the base run gives the flat rate.
    """
    if renewal_type() != "gaengsin":
        return 0.0
    if (t + 1) % (12 * policy_term()) != 0 or t >= proj_len() - 1:
        return 0.0
    jump = prem_pp(t + 1) / prem_pp(t)
    return min(renewal_decline_max,                                  # noqa: F821
               renewal_decline_base * jump ** renewal_decline_beta)  # noqa: F821


def pay_factor(k):
    """g(k): the **[std]** shortened-pay uplift on the premium of cycle k.

    ``a-due(m_k) / a-due(m_k^p)`` at the 적용이율, the ratio of an annuity-certain-due
    over the cover period to one over the paying period — the level premium that pays for
    the same cover over fewer years.  1.0 on a 전기납 contract, and 1.78 on a 20-year
    term bought 10년납.

    **[std]** because no Korean document retrieved publishes a shortened-pay premium for
    a term contract at all: every published grid is 전기납 or fixes the 납입기간 equal to
    the 보험기간 [S1] [S8] [S11] [S12].  A certain annuity rather than a life annuity is
    a simplification that overstates the uplift slightly, by the mortality that would
    have been shed between the two periods; at the ages this composite issues at, that is
    a fraction of a percent.
    """
    m, m_p = term_len(k), term_pay_years(k)
    if m_p <= 0 or m_p >= m:
        return 1.0
    v = 1.0 / (1.0 + prem_int_rate)                                  # noqa: F821
    return ((1.0 - v ** m) / (1.0 - v ** m_p))


def prem_rate_mth(t):
    """r(form, sex, x_k, m_k): the monthly 표준체 rate per 100,000,000 won of cover.

    The **published cell** where one exists — the anchor carrier's 20-year grid at ages
    30, 40 and 50 for both sexes and both maturity forms [S12], and the 갱신형 ladder at
    ages 40, 50, 60 and 70 on a ten-year cycle [S6] [S7] — and otherwise the **[std]**
    extension off the ``is_anchor`` row of the matching form and sex::

        r(form, sex, x, m) = r_anchor * qbar(x, m) / qbar(x_a, m_a)

    The anchor is the age-40 20-year cell, which for the 순수보장형 is simultaneously the
    감독규정 기준연령 요건 [REG-R9] and the disclosure's 대표계약 [S5], and whose 15,080
    won appears independently in the carrier's own grid and in the cross-carrier
    disclosure, agreeing to the won [S12] [S4].

    The 10-year rows and the 20-year rows are **different carriers**, and the model never
    mixes them: the shipped 갱신형 points reach published cells only.  That the two are
    at the same level is checkable — the 흥국생명 비갱신형 20-year premium on the
    disclosure basis is 15,000 won against the anchor's 15,080 [S4].
    """
    k = term_index(t)
    x_k, m_k = term_start_age(k), term_len(k)
    tbl = data.prem_rate_table()                                     # noqa: F821
    key = (maturity_form(), sex(), int(x_k), int(m_k))
    if key in tbl.index:
        return float(tbl.loc[key, "prem_mth_per_100m"])
    anchor = data.prem_anchor_table().loc[                           # noqa: F821
        (maturity_form(), sex())]
    return (float(anchor["prem_mth_per_100m"])
            * mort_table_mean(x_k, m_k)
            / mort_table_mean(int(anchor["issue_age"]), int(anchor["term_y"])))


def premium_mth_pp(t):
    """P_m: the monthly 영업보험료 (office premium) per policy in period t.

    ``r * c_p * g * SA / 100,000,000``, rounded half up to the nearest **10 won**, which
    is the granularity the anchor carrier quotes [S12].  Level within the 보험기간 and
    recomputed at each 갱신 at attained 보험나이 on the whole 기초율 then in force [S9]
    [S15] — it is **not** guaranteed beyond the current cycle, which is what makes
    :func:`contract_boundary` a question rather than a detail.

    **No flat policy element is separated out.** Every Korean rate card retrieved fixes
    the sum assured and varies age, sex, rate class or product form instead [S1] [S8]
    [S11] [S12] [S14], so the per-mille rate and any per-policy fee cannot be decomposed
    and the premium is treated as proportional in the sum assured.  On the anchor cell
    this reproduces the published 15,080 won exactly [S12] [S4].

    No 단체취급 discount (1.5%-5% for an affinity group of five or more), 고액할인,
    걷기할인형 or 선납 discount is applied: all four are documented and none has a
    published rate that could be applied without inventing the number that matters
    [S1] [S8] [S9] [S10] [S12].
    """
    raw = (prem_rate_mth(t) * class_prem_ratio() * pay_factor(term_index(t))
           * sum_assured() / 100000000.0)
    return float(int(raw / 10.0 + 0.5) * 10)


def prem_pp(t):
    """P_a: the annualized 영업보험료 per policy in period t, ``12 P_m``.

    The annualization is **[std]**: 월납 is the base frequency and the only one on seven of
    the retrieved products, from five carriers [S1] [S6] [S8] [S9] [S12] [S17] [S18], and no
    carrier
    publishes a mode discount, so no allowance is made for the timing difference.  The
    simplification is conservative in the insurer's favour by half a year's interest on the
    whole premium -- 1.136% of a year's premium at the 적용이율, the mean deferral of the
    twelve payments being 5.5/12 of a year.  On the anchor cell
    ``P_a = 12 x 15,080 = 180,960``.
    """
    return 12.0 * premium_mth_pp(t)


def prem_payable(t):
    """1 while period t falls inside the 납입기간, 0 after 납입완료.

    With ``t`` 0-based the 납입기간 of ``n_p`` years is ``t < n_p``, the last paying
    period being ``t = n_p - 1``.  On a 전기납 contract this is 1 for the whole
    projection, which is why the representative form has no post-완납 period at all and
    hence no surrender-value step-up [S2 제33조제2항].
    """
    return 1.0 if t < 12 * pay_term() else 0.0


def cum_prem_pp(t):
    """Scheduled premiums paid per policy to the end of month t, ``t + 1`` months' worth.

    The 만기환급형's maturity benefit is 100% of 「이미 납입한 주계약 보험료」 computed
    **as if any waived premiums had been paid** [S1] [S12], so this is the scheduled
    premium and not the collected one, and :func:`wop_waived_frac` does not enter it.
    That is exactly why the waived state is a real state and not a cash-flow adjustment.
    """
    n = min(int(t) + 1, 12 * pay_term())
    return sum(premium_mth_pp(s) for s in range(n))


def pols_if_init():
    """l(0) = 1: the model point is one policy, projected on an expected basis.

    Survivorship multiplies the per-policy cash flows; no aggregation logic is specified
    in the technical notes and none is implemented.
    """
    return 1.0


def pols_if(t):
    """l(t): the in-force probability at time t, the **start** of period t.

    ``pols_if_init()`` at ``t = 0``, then the roll-forward
    ``l(t+1) = l(t)(1 - q)(1 - w)(1 - d) + reinstatements - maturities``.  This is the
    weight on every cash flow of the same ``result_cf()`` row.

    It is **continuous across a renewal boundary**: a 갱신 reprices the contract, it does
    not re-issue it [S6] [S9] [S15], so there is no reset to 1 and no new cohort — even
    though the renewal is issued on a new product code, which is one of the facts that
    pulls the other way on the contract-boundary question.  Defined one step beyond the
    frame and zero at ``proj_len()``, the time at which the horizon is reached:
    everything still in force there leaves through :func:`pols_maturity`, whether or not
    anything is paid for it.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return (pols_if_at(t - 1, "AFT_DECR") + pols_reinstate(t - 1)
            - pols_maturity(t - 1))


def pols_if_at(t, timing):
    """The number of policies in force at a point inside period t.

    The processing order is death, then ordinary lapse, then the renewal decline, and
    each timing reads the population the next decrement is taken from:

    ``"BEF_DECR"``
        l(t), the start of the period, before any decrement; the same number as
        :func:`pols_if` and the weight on that period's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before ordinary lapse.

    ``"BEF_DECLINE"``
        after ordinary lapse, before the renewal decline.  Equal to ``"AFT_DECR"`` in
        every period that is not a renewal boundary.

    ``"AFT_DECR"``
        after all three decrements — the end-of-period state, before any 부활
        reinstatement is added back and before the horizon's :func:`pols_maturity`
        removes the remainder.

    The order is load-bearing and the specification is explicit about it: applying the
    renewal decline before mortality and ordinary lapse would apply it to lives that died
    or lapsed during the boundary month and overstate the exposure of the renewed cohort.

    Zero outside ``0 .. proj_len() - 1``: the cover has not started or has ended.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "BEF_DECLINE":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_DECLINE") * (1.0 - renewal_decline_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t) = l(t) q(t): expected death claims in period t.

    One decrement carrying one benefit.  A court 실종선고 and a 관공서 disaster
    notification count as death and are inside this rate [S2 제5조제2항]; a withdrawal of
    life-sustaining treatment expressly does not affect the cause of death or the payment
    [S2 제5조제3항].  The three 면책 limbs — suicide within two years of the 보장개시일,
    and intentional killing by the 보험수익자 or the 계약자 — are not monetized: no
    Korean document publishes their incidence, and gross negligence is **not** an
    exclusion, 상법 제732조의2 preserving the benefit [REG-R50] [R4].
    """
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_lapse(t):
    """Ordinary lapses at the end of period t, from the survivors of mortality.

    Pays nothing on this form [S1] [S2 제33조제2항] [S12], so this moves :func:`pols_if`
    and nothing else.  With the 부활 module on, these lives flow into
    :func:`pols_lapse_pool` rather than leaving for good.  The machinery behind the rate
    is short and is the whole of it: 납입최고(독촉)기간 of **14일** from a written,
    recorded-telephone or electronic demand, termination the day after it ends, and a
    claim arising before termination still paid [S2 제27조] [REG-R25 제26조].
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_decline(t):
    """Renewal declines at the end of a boundary period, after ordinary lapse.

    Zero in every period that is not a 갱신 boundary and zero on a 비갱신형 point.  Nothing
    is paid: the policyholder who declines simply lets the cover end, and on the 갱신형
    the reserve has already unwound to zero within the cycle — 흥국생명's ten-year
    renewable shows 환급률 0.0% at 10년 [S6].
    """
    return pols_if_at(t, "BEF_DECLINE") * renewal_decline_rate(t)


def pols_maturity(t):
    """Policies whose cover ends at the horizon, in the last period ``proj_len() - 1`` only.

    The count whose cover ends at the scheduled end of the contract, whether or not
    anything is paid for it — nothing on the 순수보장형, which expires with no maturity
    value and a surrender value that has already run to zero [S1] [S8] [S12], and 100% of
    the premiums paid on the 만기환급형 [S1] [S12].  Reinstatements arriving in the final
    period are inside it, so that a contract revived under 부활 and then reaching maturity
    is treated consistently.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_if_at(t, "AFT_DECR") + pols_reinstate(t)


def reinstate_rate_eff():
    """rho: the 부활 reinstatement rate actually applied — zero unless the module is on.

    Keeping the effective rate in one cells is what lets :func:`pols_lapse_pool` and
    :func:`check_lapse_pool` carry the same ledger in both positions of the switch: with
    the module off the pool still tracks the lapsed-but-reinstatable population, and
    nothing is reinstated out of it.
    """
    if not reinstatement():
        return 0.0
    return 1.0 - (1.0 - reinstate_rate) ** (1.0 / 12.0)              # noqa: F821


def pols_lapse_pool(t):
    """lap(t): lapsed lives still inside the three-year 부활 window at time t.

    A **stock**, where :func:`pols_lapse` is the flow into it.  Tracked by vintage rather
    than as one blanket balance, because the window runs from each life's own 해지 and a
    single indicator would drop a whole cohort months early or late::

        lap(t) = sum over s in [t - W, t - 1] of pols_lapse(s) (1 - rho)^(t - 1 - s)

    with ``W = reinstate_window = 36`` months — the three years the 약관 gives
    [S2 제28조], counted on the projection's own step so that the window closes on the
    month it actually closes on rather than at the next anniversary.  Renewal declines
    never enter it: a declined 갱신 is an expiry and not a 해지, and there is nothing to
    reinstate.
    """
    rho = reinstate_rate_eff()
    return sum(pols_lapse(s) * (1.0 - rho) ** (t - 1 - s)
               for s in range(max(0, t - reinstate_window), t))      # noqa: F821


def pols_reinstate(t):
    """Reinstatements out of the pool into ``pols_if(t + 1)``: ``lap(t) rho``.

    부활 is available for **three years** from the termination date and expressly covers
    a policy with no surrender value — 「해약환급금이 없는 경우를 포함합니다」 — so a
    무해지 policy is always eligible [S2 제28조].  The arrears, which bear interest at
    「평균공시이율+1% 범위 내에서 회사가 정하는 이율」, are **not monetized**: they settle
    premiums for years in which this projection collected none, so recognizing them would
    need a missed-premium ledger **[std scope]**.  Reinstatement re-runs the 계약 전 알릴
    의무 and **restarts the two-year suicide window**, where a 갱신 does not [S2
    제6조·제28조].  Zero in the base run.
    """
    return pols_lapse_pool(t) * reinstate_rate_eff()


def pols_lapse_expire(t):
    """Lives leaving the pool in period t because their three-year window has run out.

    The vintage that lapsed in period ``t - W``, net of the reinstatements taken out of it
    along the way.  They are gone for good: after the window there is no 부활
    [S2 제28조].
    """
    s = t - reinstate_window                                         # noqa: F821
    if s < 0:
        return 0.0
    return pols_lapse(s) * (1.0 - reinstate_rate_eff()) ** reinstate_window  # noqa: F821


def wop_waived_frac(t):
    """u(t): the fraction of in-force policies with premiums waived at time t.

    A two-state incidence chain **[std]**, ``u(t+1) = u(t)(1 - rec) + (1 - u(t)) inc``,
    starting from ``u(0) = 0``.  Two Korean rules shape it and both are sourced.

    **It resets at every 갱신**, so it is zero again at ``t = (k - 1) n``, the first
    period of cycle k.  흥국생명, verbatim: 「다만, 새로이 갱신되는 계약에서는
    갱신 전 보험료 납입면제 사유로 인한 보험료 납입면제를 적용하지 않고, 보험료를 계속
    납입하여야 합니다」 [S6].  A disabled life must resume paying at the renewal date.
    :func:`check_waiver_reset` asserts it, and model points 3 and 4 exercise it.

    **It is zero after 납입완료**, there being no premium left to waive [S2 제5조제1항].

    ``wop_inc_rate = 0.0008`` is an **arbitrary placeholder**.  The trigger is a
    장해지급률 summing to **50% or more** from any cause, additive across body parts,
    determined at 180 days with a two-year look-back [S2 제5조]; it is **cause-neutral**,
    so it is a general disability incidence and **must not** be scaled off
    :func:`mort_rate`, which would be a false derivation dressed as one.  No Korean
    document publishes a 50%-plus 장해 incidence and the 참조순보험요율 behind it is not
    public [REG-R4] [R19], so the module is off on eight of the ten shipped points and no
    conclusion should be drawn from its level.

    Entering the waived state also **forfeits the 무해지 post-완납 step-up**
    [S2 제33조제2항 단서] [S12] — a value effect this model does not carry, the 표준형
    계약자적립액 belonging to ``WholeLife_KR_S``.
    """
    if not waiver() or t <= 0 or t >= 12 * pay_term():
        return 0.0
    if term_index(t) != term_index(t - 1):
        return 0.0
    u = wop_waived_frac(t - 1)
    return u * (1.0 - wop_rec_rate_mth()) + (1.0 - u) * wop_inc_rate_mth()


def wop_inc_rate_mth():
    """The monthly 납입면제 incidence, ``1 - (1 - wop_inc_rate)^(1/12)`` **[std]**.

    ``wop_inc_rate`` is stated as an annual incidence, because that is the unit a 장해
    incidence would be published in if Korea published one; the monthly grid needs the
    monthly equivalent and derives it here rather than restating the placeholder in a unit
    no source would ever use.  The level itself is arbitrary and the module is off on
    eight of the ten shipped points — see :func:`wop_waived_frac`.
    """
    return 1.0 - (1.0 - wop_inc_rate) ** (1.0 / 12.0)                # noqa: F821


def wop_rec_rate_mth():
    """The monthly recovery rate out of the waived state, from ``wop_rec_rate`` **[std]**.

    Zero in the base run: the 약해지급률 trigger is assessed at 180 days with a two-year
    look-back and the 약관 provides no re-assessment that puts a waived life back on
    premium [S2 제5조], so recovery is carried as a switch at zero rather than as a
    modelled transition.
    """
    return 1.0 - (1.0 - wop_rec_rate) ** (1.0 / 12.0)                # noqa: F821


def pols_waived(t):
    """In-force policies whose premiums are waived in period t; zero in the base run.

    Mortality and lapse are assumed independent of the waiver state **[std]**, which is
    what lets the waived population be carried as a fraction of the in-force rather than
    as its own decrement.  That assumption is more comfortable here than it would be on a
    disability product: the waiver is a *premium* mechanic on a contract whose only
    benefit is death, so the waived lives are still the same lives on the same cover.
    """
    return pols_if_at(t, "BEF_DECR") * wop_waived_frac(t) * prem_payable(t)


def pols_payer(t):
    """In-force policies actually paying premium in period t.

    ``l(t)`` inside the 납입기간, less the waived fraction; zero after 납입완료.  Equal to
    :func:`pols_if` while premiums are payable unless the 납입면제 module is on.
    """
    return pols_if_at(t, "BEF_DECR") * prem_payable(t) - pols_waived(t)


def accel_cap_binds():
    """Whether the 선지급 cap would **reduce** a single-contract acceleration.

    ``0.5 SA > 50,000,000``, a **strict** inequality.  The 약관 is 「주계약 사망보험금액의
    50% 이내에서 피보험자별로 통산하여 최고 5,000만원까지 … 다만, 1,000만원까지는 주계약
    사망보험금액의 100% 이내」 [S2 제4조].  At the anchor's 100,000,000 won of cover the
    50% limb gives exactly 50,000,000 and the aggregate cap is **exactly reached and
    reduces nothing**, so the cap is visible at the anchor rather than only at large model
    points and a model reporting it as binding there has a strict-versus-weak inequality
    error.  Model point 9, at 200,000,000 won, is where it genuinely binds.
    """
    return bool(sum_assured() > accel_full_limit                     # noqa: F821
                and accel_share_max * sum_assured() > accel_cap)     # noqa: F821


def accel_amount():
    """A: the accelerated amount under 선지급서비스특약; zero unless the module is on.

    ``SA`` where the sum assured is within the 10,000,000 won full-payment window, and
    ``min(0.5 SA, 50,000,000)`` above it [S2 제4조].  Against Japan's リビング・ニーズ特約
    the Korean cap is **tighter** — half the sum assured to 50,000,000 won rather than
    the whole benefit — while the trigger is **looser**, 12 months rather than six, and
    there is no bar near expiry at all.
    """
    if not accel():
        return 0.0
    sa = sum_assured()
    if sa <= accel_full_limit:                                       # noqa: F821
        return sa
    return min(accel_share_max * sa, accel_cap)                      # noqa: F821


def accel_available(t):
    """Whether an acceleration can be claimed in period t.

    True in **every** projected period where the module is on.  Unlike Japan's rider, which
    is barred within a year of a non-renewable expiry, the Korean 선지급서비스특약 has no
    bar near expiry in any retrieved 약관 [S2 제3조·제4조] [S10] [S12] [S17].  The one
    observed narrowing is a carrier that shortens the prognosis to six months
    specifically for 정기보험 [S17].
    """
    return accel() and 0 <= t < proj_len()


def accel_share(t):
    """a(t): the share of period t's decrement arriving as an acceleration **[std]**.

    Modelled as a **split of the existing death decrement** rather than as an additional
    incidence: an acceleration is a re-timing and re-pricing of the death benefit, not a
    second claim, and a separate incidence on top would double-count it.  Payment reduces
    the 보험가입금액 from the payment date, no surrender value arises on the reduction,
    and there is one payment per contract [S2 제4조].

    ``accel_take_up = 0.10`` is an **arbitrary placeholder**, and the honest defence of it
    is not a rationale but the switch: no retrieved document gives an acceleration take-up
    for any Korean carrier and nothing in the sources bounds it.  A round tenth was chosen
    because it is visibly round — a number no reader can mistake for an estimate.
    """
    return accel_take_up if accel_available(t) else 0.0              # noqa: F821


def accel_payout_pp(t):
    """The 선지급 payment per accelerated claim in period t.

    The accelerated amount **discounted over the remaining life expectancy at the
    평균공시이율**, less the similarly discounted premiums that would have fallen due on
    it and less any outstanding 보험계약대출, which is nil on this form [S2 제4조제6항]
    [S2 제34조]::

        payout = A v^(m/12) - m P_m (A / SA) v^(m/24)

    with ``m = accel_prognosis_months = 12`` [S2 제3조] and ``v`` at
    ``accel_disc_rate``.  The discount is the economic reason the rider can be offered
    without a separate premium, and it is the sharpest contrast with a UK terminal-illness
    benefit, which is undiscounted.

    ``accel_disc_rate = 0.025`` is the **2026 평균공시이율** [S12], which the 약관 uses
    for instalment settlement and for this discount [S2 제10조].  That it equals the
    composite's 적용이율 is a coincidence of level and not an identity of concept: there
    is no 공시이율 and no 최저보증이율 on a Korean protection product, and the
    disclosure's guarantee columns are empty for every 정기보험 row [S4].
    """
    a = accel_amount()
    if a <= 0.0:
        return 0.0
    yrs = accel_prognosis_months / 12.0                              # noqa: F821
    v = 1.0 / (1.0 + accel_disc_rate)                                # noqa: F821
    prem = (accel_prognosis_months * premium_mth_pp(t)               # noqa: F821
            * a / sum_assured() * prem_payable(t))
    return a * v ** yrs - prem * v ** (yrs / 2.0)


def premiums(t):
    """Premium income at the start of period t (at time t), an inflow.

    ``P_a(k(t))`` on the policies actually paying — :func:`pols_payer`, which is
    :func:`pols_if` inside the 납입기간 unless the 납입면제 module is on, and zero after
    납입완료.  **Monthly in advance**: the month's income is one month's office premium on
    the lives in force when the month opens, which is what the contract collects and what
    the rate card quotes.  The annual grid's matched pair of offsetting errors — a year's
    premium taken from lives that exited during the year, against a death benefit paid a
    year late — is gone rather than netted, and no half-year adjustment belongs on top of
    this one.
    """
    return premium_mth_pp(t) * pols_payer(t)


def claims(t, kind=None):
    """Benefit outgo in period t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the 보험가입금액 on the period's death claims, net of the share arriving as an
        acceleration: ``SA (1 - a(t)) D(t)`` [S2 제4조].

    ``"ACC_DEATH"``
        the **second** sum assured on the accidental subset, on the 재해사망 uplift
        variant only: ``SA a_q(t) (1 - a(t)) D(t)`` [S6] [S10].  Zero elsewhere.  It is a
        split of the existing decrement, never a second decrement: 재해 is defined by
        별표3 재해분류표 as 「한국표준질병·사인분류상의 (S00~Y84)에 해당하는 우발적인
        외래의 사고」 plus a 제1급감염병, with a closed carve-out list [S2 별표3].

    ``"ACCEL"``
        the discounted 선지급서비스특약 acceleration on the share ``a(t)`` of the same
        decrement.  Zero in the base run.

    ``"MATURITY"``
        the 만기보험금 of the 만기환급형 variant: 100% of the premiums paid, computed as
        if any waived premiums had been paid, on the policies reaching the horizon [S1]
        [S12].  Zero on the 순수보장형, which has no maturity value at all [S1] [S8]
        [S12].

    ``"LAPSE"``
        zero, always.  On a 전기납 무해지 contract the 약관 pays nothing at any duration
        [S1] [S2 제33조제2항] [S12], and 한화생명's published 해약환급금 예시 shows
        환급률 0.0% at all eleven durations printed for both sexes [S1].  The kind exists
        so that the zero is **stated** rather than inferred: the 표준형 comparator does
        have a value, reaching 46% of premiums paid by duration six [S10], and a
        shortened-pay 무해지 contract pays 50% of it after 납입완료 [S1] [S12] — a value
        this chassis deliberately does not compute, the 계약자적립액 belonging to
        ``WholeLife_KR_S``.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("DEATH", "ACC_DEATH", "ACCEL", "MATURITY", "LAPSE"))
    if kind == "DEATH":
        return sum_assured() * (1.0 - accel_share(t)) * pols_death(t)
    if kind == "ACC_DEATH":
        if not acc_death():
            return 0.0
        return (sum_assured() * acc_mort_share(t)
                * (1.0 - accel_share(t)) * pols_death(t))
    if kind == "ACCEL":
        return accel_payout_pp(t) * accel_share(t) * pols_death(t)
    if kind == "MATURITY":
        if maturity_form() != "rop":
            return 0.0
        return cum_prem_pp(t) * pols_maturity(t)
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def claim_expenses(t):
    """ec D(t): the claim handling expense on period t's death claims **[std]**.

    300,000 won per claim, uninflated, on the whole death decrement whether the benefit
    is paid as a death claim or accelerated.  No Korean document publishes a claim
    handling cost; the level is a standardization and the notes carry it as such.  A
    maturity payment carries no claim expense here, being a scheduled settlement rather
    than an investigated claim — the 약관's 3영업일 / 10영업일 / 30영업일 timetable
    applies to 보험금 지급사유 [S2 제9조].  Kept out of :func:`expenses` because the
    notes' worked example prints the two as separate columns.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^floor(t/12)`` **[std]**.

    1.0 through the whole of the first policy year, then stepping at each 계약해당일: an
    expense basis is reset annually and inflating it monthly would claim a precision the
    assumption does not have.

    ``inflation_rate = 0.02``.  No Korean insurer publishes an expense inflation
    assumption; 2% is a round central choice and the notes carry it as a standardization.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def expenses(t):
    """E0 and e(t): acquisition and inflating maintenance expense in period t **[std]**.

    120,000 won per policy at issue — that is, in the first projected period ``t = 0`` —
    then 2,000 won per policy per **month** — the same 24,000 a year — inflating at
    2.0% a year, stepping at each 계약해당일 rather than monthly, both at the start of the
    period.  **No Korean carrier publishes either level**:
    every 상품요약서 defines 계약체결비용 and 계약관리비용 in the same words — 「보험회사가
    보험계약의 체결, 유지 및 관리 등에 필요한 경비로 사용하기 위하여 보험료 중 일정비율을
    책정한 것」 — and not one publishes a rate [S1] [S6] [S8] [S10] [S11] [S12].

    Two public handles bound the standardization.  The **보험가격지수** is the product's
    total premium as a percentage of a 참조순보험료 총액 plus an industry-average
    평균사업비 총액, and it is 88.1 male / 85.5 female at the anchor [S4] [S1]; its
    dispersion across the 45 disclosed products, 51.6% to 239.1%, bounds what an expense
    assumption may plausibly be.  And the **표준해약공제액** of 별표 14 caps the
    recoverable acquisition cost by formula [REG-R20]; at the anchor its sum-assured limb
    alone is 100,000,000 x 10/1000 = 1,000,000 won, which is 5.5 years' gross premium, so
    the statutory cap is very far from binding on this product and is not computed here.
    The constraint that actually shapes a Korean term surrender value is 제7-66조제1항제2호's
    **해약공제기간, capped at seven years** [REG-R19] — and this contract has no surrender
    value for it to shape.

    **No acquisition expense is charged at a 갱신.** That is a choice rather than a fact:
    a Korean renewal is issued on a new product code [S9] [S15], which is an argument the
    other way, and ``comm_new_term_rate`` is the switch that carries it.
    """
    acq = expense_acq * pols_if_at(t, "BEF_DECR") if t == 0 else 0.0  # noqa: F821
    return acq + (expense_maint * inflation_factor(t)                # noqa: F821
                  * pols_if_at(t, "BEF_DECR"))


def comm_init_pp():
    """c0: initial commission per policy issued **[std]**, 60% of ``P_a`` at ``t = 0``.

    Paid upfront at issue, in the first projected month ``t = 0``, and computed on the
    **annualized** premium because that is the unit a commission scale is written in.  With
    the acquisition expense this is 228,576 won of first-month outgo against 15,080 won of
    first-month premium on the anchor cell, which is the deep new business strain the
    protection shape starts from — and which a monthly grid shows as the single-row cliff
    it is rather than spread against a year of premium.  No Korean document in the source
    set discloses a commission scale — the 모집수수료 reforms bound the *first-year*
    share of premium rather than publishing a level [REG-R29] — so both this and
    ``comm_renewal_rate`` are levels chosen for the reference implementation.
    """
    return comm_init_rate * prem_pp(0)                               # noqa: F821


def comm_new_term(t):
    """Commission paid at a 갱신 **[std]**; zero in the base run.

    The base run pays no acquisition commission on a renewed cycle.  That is a choice and
    not a fact, and the Korean evidence cuts both ways: a 갱신 takes no 고지 and no
    underwriting [S6] [S9] [S15], which is an argument that it is not new business, while
    the renewal is issued on a **new product code** — 푸본현대생명 prints 주계약 최초계약
    ``LO01011`` and 갱신계약 ``LO01012`` separately [S15], and 삼성생명 states 「갱신형특약은
    매 갱신시마다 갱신시점의 상품코드를 적용합니다」 [S9] — which is an argument that it
    is.  Set ``comm_new_term_rate`` to switch it on; it then falls in the first **month** of
    each cycle after the first — ``t = 12 (k - 1) n`` for cycle ``k > 1`` — and on the
    shipped 갱신형 anchor at a first-year rate it turns the opening months of each repriced
    cycle sharply negative.
    """
    if comm_new_term_rate <= 0.0 or term_index(t) <= 1:              # noqa: F821
        return 0.0
    if t != (term_index(t) - 1) * 12 * policy_term():
        return 0.0
    return comm_new_term_rate * prem_pp(t) * pols_if_at(              # noqa: F821
        t, "BEF_DECR")


def commissions(t):
    """Commission outgo in period t **[std]**.

    The initial commission in the first month ``t = 0``, then 3% of premium income from
    the start of policy year 2 — ``t = 12`` — while premiums are payable, plus any
    commission at a 갱신 (off in the base run).  The renewal commission rides on
    :func:`premiums`, so it stops when the 납입면제 stops the premium and when the
    납입기간 ends.  No
    clawback on early lapse is modelled: no Korean clawback rule appears in the retrieved
    set, so a clawback would be an invention rather than a standardization of something
    observed.
    """
    init = comm_init_pp() * pols_if_at(0, "BEF_DECR") if t == 0 else 0.0
    renew = comm_renewal_rate * premiums(t) if t >= 12 else 0.0      # noqa: F821
    return init + renew + comm_new_term(t)


def net_cf(t):
    """CF(t): the net cash flow of period t, **income positive**.

    Premiums less claims, claim expense, maintenance and acquisition expense and
    commission.  This is the library-wide sign, so there is no outgo-positive
    ``liability_cf`` companion to publish.

    Lapse and the renewal decline contribute no term: they act only through
    :func:`pols_if`, there being no surrender value to pay [S2 제33조제2항].  The shape to
    expect on the anchor cell is a deep strain at ``t = 0``, then thin positive margins that
    decay as the level premium falls behind the rising mortality cost, and on a 갱신형
    point a saw-tooth: a negative period immediately before each renewal and a jump back
    into surplus the period after, as the premium resets to attained age.
    """
    return (premiums(t) - claims(t) - claim_expenses(t)
            - expenses(t) - commissions(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in period t; zero everywhere.

    ``l(t) - l(t+1) - D(t) - lapses - declines - maturities + reinstatements``, with the
    부활 inflow and the horizon's maturity outflow carried as their own terms so that the
    same residual closes in both positions of every switch.  Non-zero would mean the
    decrements and the roll-forward have drifted apart — most easily by applying the
    renewal decline to the wrong population, since it is taken **after** mortality and
    **after** ordinary lapse.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_decline(t) - pols_maturity(t) + pols_reinstate(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected period.

    The library-wide form of a roll-forward check: no argument, one bool over
    ``t = 0 .. proj_len() - 1``, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the period that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_lapse_pool_resid(t):
    """The 부활 pool roll-forward residual in period t; zero everywhere.

    ``lap(t) - lap(t+1) - reinstatements - window expiries + lapses``.  The pool is a
    stock with one inflow (:func:`pols_lapse`) and two outflows (:func:`pols_reinstate`
    and :func:`pols_lapse_expire`), and the vintage bookkeeping of the three-year window
    is exactly where an implementation drops or double-counts a cohort.  Closes with the
    module off as well as on, since the pool is tracked either way.
    """
    return (pols_lapse_pool(t) - pols_lapse_pool(t + 1)
            - pols_reinstate(t) - pols_lapse_expire(t) + pols_lapse(t))


def check_lapse_pool():
    """True when the 부활 pool ledger closes in every projected period."""
    return all(abs(check_lapse_pool_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_pols_payer_resid(t):
    """The premium-paying population residual in period t; zero everywhere.

    ``l(t) x prem_payable(t) - payers - waived``.  The 납입면제 module carries the waived
    lives as a fraction of the in-force rather than as a separate decrement, which is only
    legitimate while payers and waived lives partition the population that owes a premium
    at all.  The ``prem_payable`` factor is what makes the identity survive 납입완료 on a
    shortened-pay point, where nobody owes a premium and both parts are zero.
    """
    return (pols_if_at(t, "BEF_DECR") * prem_payable(t)
            - pols_payer(t) - pols_waived(t))


def check_pols_payer():
    """True when payers and waived lives partition the premium-owing in-force."""
    return all(abs(check_pols_payer_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_prem_level_resid(t):
    """The premium-level residual in period t; zero everywhere.

    ``P_a(t) - P_a(t-1)`` inside a 보험기간, and zero by definition in the first period of
    a cycle.  The premium is level within the 보험기간 and changes **only** at a 갱신 [S1]
    [S9] [S12] [S15]; there is no premium review within a term and no insurer discretion
    over the level.  A residual here means the premium is drifting with the policy year,
    which is what happens if the rate lookup is keyed on attained age rather than on the
    cycle's entry age — the single most likely way to convert a 갱신형 into something that
    is neither form.
    """
    if t <= 0 or term_index(t) != term_index(t - 1):
        return 0.0
    return prem_pp(t) - prem_pp(t - 1)


def check_prem_level():
    """True when the premium is level within every 보험기간 of the projection."""
    return all(abs(check_prem_level_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_decline_timing():
    """True when the renewal decline falls on renewal boundaries and nowhere else.

    The decline rate must be non-zero in exactly those months that end a 갱신 cycle short
    of the horizon — ``(t + 1) % 12n == 0`` with ``t < proj_len() - 1`` on the 0-based
    index — and zero in every other month, including the last one ``t = proj_len() - 1``,
    where cover ends at the ceiling rather than renewing, and every period of a 비갱신형 point, which
    never renews [S1] [S12].  This is the check that catches the decline being modelled
    as a lapse loading: a rate that is non-zero in a non-boundary period has stopped being
    a renewal decline whatever it is called.
    """
    for t in range(proj_len()):
        boundary = (renewal_type() == "gaengsin"
                    and (t + 1) % (12 * policy_term()) == 0 and t < proj_len() - 1)
        if boundary != (renewal_decline_rate(t) > 0.0):
            return False
    return True


def check_waiver_reset():
    """True when no premium waiver survives a 갱신 into the next cycle.

    「다만, 새로이 갱신되는 계약에서는 갱신 전 보험료 납입면제 사유로 인한 보험료 납입면제를
    적용하지 않고, 보험료를 계속 납입하여야 합니다」 [S6].  The waived fraction must
    therefore be zero in the first month of every cycle, not merely at ``t = 0``.  On a
    비갱신형 point the check reduces to ``u(0) = 0`` and on a point with the module off it
    is vacuous; model points 3 and 4 are where it bites, and where a model that carried
    the waiver across the boundary would be caught collecting no premium from a population
    the contract says must resume paying.
    """
    for t in range(proj_len()):
        if t == 0 or term_index(t) != term_index(t - 1):
            if abs(wop_waived_frac(t)) > roll_fwd_tol:               # noqa: F821
                return False
    return True


def check_net_cf_resid(t):
    """The published cash flow statement's ledger residual in period t; zero.

    :func:`net_cf` less the sum of the **columns of** ``result_cf()``, so a reader adding
    up the printed statement gets the printed total.  It is the check that catches a
    benefit kind that exists in :func:`claims` but was never given a column — which would
    leave the statement silently short of outgo it is charging.
    """
    row = result_cf().loc[t]
    return float(row["net_cf"] - (
        row["premiums"] - row["claims_death"] - row["claims_acc_death"]
        - row["claims_accel"] - row["claims_maturity"] - row["claims_lapse"]
        - row["claim_expenses"] - row["expenses"] - row["commissions"]))


def check_net_cf():
    """True when the published cash flow statement adds up in every projected period.

    Tested against ``cash_tol``, not the ``roll_fwd_tol`` the decrement checks use.  The
    wider tolerance is a property of what is compared: the other checks close an identity
    between cells evaluated in one expression, where the residual is a unit or two in the
    last place of a count near 1.0, while this one re-reads won amounts of order 1e7 back
    out of the ``result_cf()`` DataFrame, so the round trip through column construction
    leaves float64 rounding in absolute won.  ``cash_tol = 1e-6`` is well above that noise
    and far below one won, which is the smallest error a reader adding up the printed
    statement could observe.
    """
    return all(abs(check_net_cf_resid(t)) <= cash_tol                # noqa: F821
               for t in range(proj_len()))


def result_cf():
    """Result table of cashflows, indexed by the 0-based period index t.

    ``t = 0`` is the first policy month and the frame runs to ``proj_len() - 1``, so the
    table has ``proj_len()`` rows and the contractual policy year of row ``t`` is
    ``policy_year(t) = t // 12 + 1``.
    ``pols_if`` is the start-of-period count, which is the weight applied to every cash flow
    on the same row.  ``net_cf`` is income positive.  ``claims_lapse`` is a column of
    zeros by product design — there is no 해약환급금 at any duration on the representative
    form — and is published rather than dropped; see :func:`claims`.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_acc_death": [claims(t, "ACC_DEATH") for t in ts],
            "claims_accel": [claims(t, "ACCEL") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts, decrement rates and the premium, indexed by t.

    Same 0-based monthly frame as :func:`result_cf`: ``t = 0 .. proj_len() - 1``.
    Both the annual rates and the monthly decrements derived from them are printed, because
    the annual rate is the sourced quantity and the monthly one is what the projection
    applies; a reader checking a disclosure checks the first and a reader checking the
    roll-forward checks the second.
    The renewal machinery is only legible next to the decrements it drives, so
    ``term_index`` and ``prem_pp`` are printed here with ``renewal_decline_rate``: a
    boundary month is the row where the decline rate is non-zero and the premium changes
    on the next row.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_decline": [pols_decline(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_reinstate": [pols_reinstate(t) for t in ts],
            "pols_lapse_pool": [pols_lapse_pool(t) for t in ts],
            "pols_payer": [pols_payer(t) for t in ts],
            "pols_waived": [pols_waived(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "renewal_decline_rate": [renewal_decline_rate(t) for t in ts],
            "term_index": [term_index(t) for t in ts],
            "prem_pp": [prem_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 0.85

lapse_be_factor = 1.0

prem_int_rate = 0.025

renewal_decline_base = 0.2

renewal_decline_beta = 0.0

renewal_decline_max = 0.4

expense_acq = 120000.0

expense_maint = 2000.0

expense_claim = 300000.0

inflation_rate = 0.02

comm_init_rate = 0.6

comm_renewal_rate = 0.03

comm_new_term_rate = 0.0

accel_cap = 50000000.0

accel_full_limit = 10000000.0

accel_share_max = 0.5

accel_disc_rate = 0.025

accel_prognosis_months = 12

accel_take_up = 0.1

wop_inc_rate = 0.0008

wop_rec_rate = 0.0

reinstate_rate = 0.1

reinstate_window = 36

roll_fwd_tol = 1e-12

cash_tol = 1e-06

pd = ("Module", "pandas")
