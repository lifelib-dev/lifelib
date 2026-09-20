# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.Immediate_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace projecting
model point 1::

    >>> Projection[1].result_cf()          # the worked-example anchor
    >>> Projection.point_id = 6            # the 상속연금형, retention as designed
    >>> Projection.point_id = 7            # the same contract, retention as ordered

``t`` counts **completed policy months from inception and is 0-based**: ``t = 0`` is the
first policy month, and the contractual policy year — the 1-based label the 약관 speaks in —
is the derived ``policy_year(t) = t // 12 + 1``. Period ``t`` runs from time ``t`` to time
``t + 1``; row ``t`` of :func:`result_cf` carries the cash flows of month ``t``; the
single premium falls at time 0 on row 0; and the annuity is payable **in arrears**, so the
payment shown on row ``t`` falls at the end of month ``t``, which is the 연금지급일 —
「미지급된 연금월액을 **매월** 연금지급일에 드립니다」. ``proj_len()`` is the **number of
projected months**, the frame's exclusive end and ``12 x proj_years()``, so the frame is
``range(proj_len())`` and the last row — the one carrying the last scheduled payment — is
``t = proj_len() - 1``.

The contract terms stay in **years**, which is how the 약관 states them, and the assumptions
stay **annual**, which is how they are filed and published: ``mort_rate(t)``,
``lapse_rate(t)``, ``decl_rate()``, ``min_guar_rate(t)`` and ``crediting_rate(t)`` are the
yearly figures, and ``mort_rate_mth``, ``lapse_rate_mth`` and ``crediting_rate_mth`` are
their uniform-force monthly companions, level inside a policy year and stepping on each
계약해당일. Twelve of each compound back to the year's figure exactly.

.. rubric:: Age basis

Every age in this model is **보험나이** (*boheom nai*, insurance age) — 만나이 at the
계약일 with a remainder under six months discarded and six months or more rounded up to a
year, incrementing on each 계약해당일. It is the age the 가입나이 band is stated in, the age
the shipped 개인연금사망률 table is indexed by, and the age the model point table carries.
It is **not** 만나이 (age last birthday), which is what the public 완전생명표 and every
Korean population statistic are published on; the six-month rule makes the two differ for
half of all issue dates, and reading a 만나이 model point against a 보험나이 table
understates the rate by about half a year of ageing on every row without raising anything.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/immediate_annuity/``, read at run time rather than stored inside the model. Each
table has a filename Reference and a reader Cells, both on
:mod:`~.Immediate_KR_S.Data`, reached here through the ``data`` Reference:

======================  ====================================  ========================
Reference               Cells                                 File
======================  ====================================  ========================
model_point_file        data.model_point_table()              model_point_table.csv
mort_table_file         data.mort_table()                     mort_table.csv
charge_table_file       data.charge_table()                   charge_table.csv
crediting_table_file    data.crediting_table()                crediting_table.csv
======================  ====================================  ========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S``, ``savings.CashValue_SE`` and
``annuallife.TradLife_A`` wherever those models have an analogue, and follow the sister
libraries' payout models wherever the products share machinery. The technical notes use
compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the cells argument)            0-based period index
(model point)              model_point()                   The selected row as a Series
(shape)                    shape()                         life / inheritance / certain
x                          age_at_entry()                  가입나이, 보험나이
x + t                      age(t)                          Attained 보험나이
(sex)                      sex()                           M or F
P                          prem_pp()                        일시납보험료, the single premium
n, g                       annuity_term()                  보험기간 / 연금지급기간, or the
                                                           보증지급기간 on the life shape
(switch)                   retention_basis()               as_designed or as_ordered
(basis id)                 crediting_basis()               Row set of crediting_table
w                          lapse_rate(t)                   Annual surrender rate **[std]**
w^m                        lapse_rate_mth(t)               Its monthly conversion
i_d                        decl_rate()                     공시이율
i_g(t)                     min_guar_rate(t)                최저보증이율, duration-stepped
i(t)                       crediting_rate(t)               Max[공시이율, 최저보증이율]
j(t)                       crediting_rate_mth(t)           Its monthly equivalent
q(x + t)                   mort_rate(t)                    개인연금사망률 at age(t)
q^m(t)                     mort_rate_mth(t)                Its monthly conversion
(load)                     acq_charge_rate()               계약체결비용
(load)                     admin_charge_rate()             계약관리비용
c                          expense_load_rate()             The two, summed
b                          risk_prem_rate()                위험보험료
(commission)               comm_rate()                     모집수수료율
(expense)                  acq_expense_rate()              Load less commission **[std]**
(charge)                   annuity_charge_rate()           0.80% of the 연금연액
(benefit)                  db_rate()                       사망보험금 as a share of P
B                          risk_prem_pp()                  보장계약 보험료
V(0)                       av_pp_init()                    Opening 계약자적립액
V(t)                       av_pp(t)                        계약자적립액 at time t
CV(t)                      cv_pp(t)                        해약환급금
(deduction)                surr_chg_pp(t)                  해약공제액, nil at every t
M                          maturity_benefit()              만기보험금
a(m, i)                    annuity_factor_certain(m, i)    Annuity-certain in arrears
s(m, i)                    accum_factor(m, i)              Accumulation of 1 a period
ae(x, g, j)                annuity_factor()                종신연금형 factor at inception
A(t)                       annuity_pp(t)                   연금월액 payable at t + 1
12 A(t)                    annuity_pp_annual(t)            The 연금연액 it makes up
R(t)                       retention_pp(t)                 만기보험금 지급재원
v(t)                       disc_factor(t)                  PV factor on the crediting path
(dispute)                  retention_shortfall_pp()        PV cost of the 주문 liability
l(t)                       lives_if(t)                     Annuitant alive at time t
(persistency)              surr_if(t)                      Not surrendered at time t
IF(t)                      pols_if(t)                      Any payment obligation open
(none)                     pols_if_init()                  Obligations in force at t = 0
d(t)                       pols_death(t)                   Deaths in period t
(surrenders)               pols_lapse(t)                   Surrenders in period t
(exits)                    pols_exit(t)                    Obligations ending in period t
F(t)                       payment_factor(t)               Weight on the payment at t + 1
(pricing)                  pricing_factor(t)               The same on the pricing basis
N                          proj_len()                      Number of projected months
N / 12                     proj_years()                    The same horizon in years
E[PREM(t)]                 premiums(t)                     Single premium income
E[ANN(t)]                  annuity_payments(t)             생존연금 outgo
E[DTH(t)]                  claims(t, "DEATH")              사망보험금
E[SUR(t)]                  claims(t, "LAPSE")              해약환급금 on surrender
E[MAT(t)]                  claims(t, "MATURITY")           만기보험금
E[COM(t)]                  commissions(t)                  모집수수료
E[EXP(t)]                  expenses(t)                     Acquisition and annuity charges
CF(t)                      liability_cf(t)                 Total gross liability outgo
(none)                     net_cf(t)                       -liability_cf(t), insurer sign
=========================  ==============================  ==========================

Four names needed care.

``pols_if`` is **not a policy count**. It is the notes' ``IF(t)``, the probability that a
**payment obligation remains** at time ``t``, which on this product is not the same thing as
the probability that the annuitant is alive. Within the 보증지급기간 the instalments are due
whether or not the annuitant lives; on the 확정기간연금형 they are due irrespective of
survival for the whole term; and on the 상속연금형 death itself triggers a payment. The name
is kept because it is what the rest of the library weights maintenance expense by and what
``result_cf()`` publishes first. :func:`lives_if` is the survival probability proper, and
the two differ on every shape.

``annuity_term`` carries three contractual quantities under one name because the arithmetic
treats them identically: the **보증지급기간** on the life shape, the **보험기간** on the
inheritance shape and the **연금지급기간** on the certain shape. What differs is what the
projection does after it, and that is the shape's business, not the term's.

``lapse_rate`` is the **annual** rate, as everywhere in this library, and
``lapse_rate_mth`` is the monthly conversion the projection applies — the same pairing the
other monthly models in ``krlib`` use, and for the same reason: the assumption is stated and
argued annually and only the grid beneath it is monthly. It is nil on the life shape as a
matter of contract, not of assumption.

``decl_rate`` is the 공시이율. The romanized name was rejected in the library's naming
review: 공시이율 is the declared crediting rate under the same definition ``delib`` settled
on for the laufende Verzinsung, and it is not the 예정이율 (pricing interest rate), which is
``prem_int_rate`` and does not appear in this model at all.

There is **no** ``prem_pp_mth``, ``pols_maturity``, ``cv_floor_ratio``, ``surr_chg_cap_pp``
or ``renewal_decline_rate`` of any kind, and the absence of each is a product fact.

.. rubric:: There is no premium term, so there is no lapse machinery of the usual kind

A single premium leaves nothing to miss, so 표준약관 제26조's 납입최고 and 제27조's 부활
cannot operate and neither is modelled. The only decrements are mortality and — on the two
shapes that permit it — voluntary surrender. On the **종신연금형 surrender is contractually
impossible**: 「종신연금이 지급개시된 이후에는 해지할 수 없습니다」, and on an immediate
annuity the annuity begins a month after inception, so the contract is irreversible from
month one. :func:`check_surr_value` asserts that the shipped life-shape model points carry a
nil rate and a nil surrender value, rather than leaving it to the table.

**No retrieved source gives a surrender rate for 즉시연금 by duration or by shape.** The
assumption on the other two shapes is therefore entirely unsourced, is **[std]**, and is
carried as a per-model-point scalar so that its effect can be isolated.

.. rubric:: The guarantee is a floor on the obligation, not a second stream

``payment_factor(t) = max(l(t + 1), 1{t + 1 <= 12g})`` on the life shape. Within the
보증지급기간 the full instalment is payable whether or not the annuitant lives, and an
additive construction — the survival probability *plus* the guarantee — would pay
``1 + l(t + 1)`` for the whole guaranteed term. :func:`check_payment_factor` asserts the
``max``, and :func:`check_guarantee_certain` asserts that the weight is exactly one for
every payment inside the guarantee.

The commutation right — 선지급, the unpaid guaranteed instalments taken as a lump sum
discounted at the 공시이율, available on death and on request once a year in whole years —
is **recorded and not exercised**. The projection pays the guaranteed instalments on their
contractual dates. That is a **[std]** simplification and it is value-neutral only because
the discount rate is the same rate that sets the annuity.

.. rubric:: The retention, and why it is a switch

On the 상속연금형 만기형 the maturity benefit is the **gross** single premium while the fund
opens at the premium net of the load, so part of each year's interest must be retained to
rebuild it. Writing ``M`` for the maturity benefit and ``s(m, i)`` for the accumulation of
₩1 a year in arrears over the remaining term,

    ``A(t) = V(t) j(t) - (M - V(t)) / s(m, j(t))``

with ``j`` the monthly crediting rate and ``m`` the remaining term in months, decomposes the
annuity exactly into interest on the fund less the **만기보험금 지급재원**.
Both terms move against the policyholder when the rate falls: the interest falls with ``i``
and the retention *rises*, because ``s`` shrinks. That retention was set out in the
산출방법서 and not in the 약관, and 금융분쟁조정위원회 조정결정 제2017-17호 held on
2017-11-14 that it could not be asserted against the policyholder; the Supreme Court
restored it for the contracts before it on 2025-10-16, and the current market states the
deduction on the face of the 약관.

Neither reading is "the" right one, so the model carries both.
``retention_basis = "as_designed"`` runs the identity above;
``retention_basis = "as_ordered"`` sets ``R(t) = 0``, so the annuity is interest on the fund
alone and the maturity benefit is met from the insurer's own resources.
:func:`retention_shortfall_pp` is what the second costs, discounted to inception on the
crediting path, and model points 6 and 7 are the same contract on the two bases.

A specification that buries the retention inside an annuity factor cannot express the
question the whole litigation was about, which is why it is an explicit term here.

.. rubric:: Two of the three shapes use no mortality in the annuity

「옵션 중 사망(생존) 위험률이 적용되는 것은 종신형에 한정된다 … 확정형과 상속형은
사망률을 사용하지 않는다」. Only :func:`annuity_factor` reads the table for pricing, and it
is defined on the life shape alone and raises on the others. Mortality still enters the
**projection** of the other two shapes, because both pay a death benefit; the distinction
between a decrement and a pricing basis is exactly the distinction the two uses draw.

.. rubric:: The 계약자적립액 on the life shape has no contractual role

:func:`av_pp` runs the 약관's own recursion — 「연금개시후에는 생존연금 발생분을 차감한
금액」 — on all three shapes. On the inheritance shape it climbs to ``M`` at maturity and on
the certain shape it exhausts to zero, and on both it is the base of the 해약환급금. On the
**life shape it is neither**: the annuity is a life annuity, the fund is not the reserve,
and the recursion runs negative at about the point where the annuitant has outlived the
factor the fund bought. Surrender is prohibited there, so :func:`cv_pp` is nil and nothing
downstream reads the negative value; :func:`check_av_terminal` accordingly asserts a
terminal value on the two shapes that have one and says so on the third.

.. rubric:: Sign convention

The notes define ``CF(t)`` as total gross liability **outgo**, which is
:func:`liability_cf`. :func:`net_cf` is its exact negative, the library-wide
income-positive convention, so a ``result_cf()["net_cf"]`` column can be summed or compared
across every model in the library. Both are published as columns. The single premium is
genuine income at ``t = 0`` and is projected as such; there is no premium income after it.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series.

    One row of ``data.model_point_table()``, indexed by ``point_id``.  Model point 1 is the
    technical notes' worked-example anchor: 남자, 보험나이 60, 일시납 ₩100,000,000 (1억원),
    종신연금형 with a ten-year 보증지급기간 on the representative crediting basis.
    """
    return data.model_point_table().loc[point_id]                    # noqa: F821


def shape():
    """The payout shape elected at inception: ``life``, ``inheritance`` or ``certain``.

    ``life`` is 종신연금형, the annuity for life with a 보증지급기간; ``inheritance`` is
    상속연금형 만기형, interest only with the capital returned at maturity or on death; and
    ``certain`` is 확정기간연금형, the annuity-certain paid irrespective of survival.  The
    election is irrevocable, is priced into the basis and is a model point column rather
    than a rider, because the three are three different liabilities.
    """
    v = str(model_point()["shape"])
    if v not in ("life", "inheritance", "certain"):
        raise ValueError("unknown payout shape: %s" % v)
    return v


def sex():
    """The annuitant's sex, ``M`` or ``F``, the first key of the mortality table.

    Male and female are rated separately on the life shape, which is the only shape whose
    annuity reads a mortality table at all.  The other two shapes still carry the sex,
    because their death benefit is projected on the same table.
    """
    v = str(model_point()["sex"])
    if v not in ("M", "F"):
        raise ValueError("unknown sex: %s" % v)
    return v


def age_at_entry():
    """x: the 가입나이 at inception, in **보험나이**.

    The representative issue-age band is 45 to 80.  There is no deferral on an 즉시연금, so
    the 연금개시나이 equals the 가입나이 and no separate attribute is carried for it.
    """
    return int(model_point()["age_at_entry"])


def age(t):
    """x + t // 12: the attained **보험나이** in month t, the key into the mortality table.

    보험나이 increments on each 계약해당일, which on a monthly grid is every twelfth period
    boundary, so the attained age is the entry age plus the completed policy years and needs
    no rounding rule and no fractional-age interpolation of its own.
    """
    return age_at_entry() + t // 12


def policy_year(t):
    """The contractual policy year containing month t, 1-based.

    ``t // 12 + 1``: the 약관 speaks in policy years and the grid runs in months, so this is
    the label that translates between them.  「제1보험년도」 is ``t = 0 … 11``.
    """
    return t // 12 + 1


def annuity_term_mths():
    """The contractual term of :func:`annuity_term` expressed in months.

    ``12 x annuity_term()``.  The contract states the 보증지급기간, the 보험기간 and the
    연금지급기간 in whole years and the grid counts months, so every comparison against the
    term goes through this cells rather than through a bare ``12 *`` at each site.
    """
    return 12 * annuity_term()


def prem_pp():
    """P: the 일시납보험료, the single premium, per policy.

    Paid once at inception and never again: there is no premium term, no renewal premium
    and no 추가납입 on the 즉시형.  It is the base of the expense load, of the 위험보험료,
    of the commission and — on the inheritance shape — of the 만기보험금, so a change to it
    moves every quantity in the model.
    """
    return float(model_point()["prem_pp"])


def annuity_term():
    """n or g: the contractual term in whole years, in the sense the shape gives it.

    On the life shape it is the **보증지급기간**, the period over which instalments are due
    whether or not the annuitant lives; on the inheritance shape the **보험기간**, at the
    end of which the 만기보험금 falls due; and on the certain shape the **연금지급기간**,
    over which the fund is divided.  Ten years is the representative term on all three
    shapes, and it is what 97.3% of life-shape buyers and 77.6% of certain-shape buyers
    actually chose.
    """
    v = int(model_point()["annuity_term"])
    if v < 1:
        raise ValueError("annuity_term must be at least one year")
    return v


def retention_basis():
    """The 만기보험금 지급재원 switch: ``as_designed`` or ``as_ordered``.

    ``as_designed`` runs the retention the 산출방법서 specified, so the annuity is interest
    on the fund less the amount needed to rebuild it to the 만기보험금.  ``as_ordered``
    sets the retention to zero, which is the liability 금융분쟁조정위원회 조정결정
    제2017-17호 ordered and the 금융감독원 extended to the industry on 2018-03-15: interest
    on the fund with no deduction, the maturity benefit met from the insurer's own
    resources.  The switch is meaningful on the inheritance shape only and is ignored
    elsewhere.
    """
    v = str(model_point()["retention_basis"])
    if v not in ("as_designed", "as_ordered"):
        raise ValueError("unknown retention basis: %s" % v)
    return v


def crediting_basis():
    """The ``basis_id`` selecting this contract's rows of ``data.crediting_table()``.

    ``decl_2017`` is the representative basis, a 공시이율 of 2.50% over a 최저보증이율
    stepping 1.25% / 1.00% / 0.75% at five and ten years.  ``min_guar`` sets the declared
    rate to zero so that Max[공시이율, 최저보증이율] resolves to the floor at every
    duration; it is not a product a carrier sells, but it is the basis on which the anchor
    carrier publishes its 해약환급금 run, and it is what exercises the duration stepping.
    """
    return str(model_point()["crediting_basis"])


def lapse_rate(t):
    """w: the **annual** voluntary surrender rate in period t.  **[std]**

    Nil on the life shape at every duration, because a 종신연금형 cannot be surrendered once
    the annuity is in payment and on an immediate annuity that means from month one.  On
    the other two shapes **no retrieved source gives a rate of any kind**, so the
    assumption is entirely unsourced and is carried per model point rather than in a table,
    so that its effect can be isolated.

    It is nil in the final **policy year** as well, on every shape: a contract in its last
    year runs to the 만기보험금 or to the last instalment rather than being surrendered a
    moment before either, and a lapse decrement there would divert the maturity benefit into
    a surrender value of the same amount for no reason a contract states.  Holding it nil
    over the whole final year rather than the final month is what makes the monthly grid's
    in-force reproduce the annual-step model's at every 계약해당일.
    """
    if shape() == "life":
        return 0.0
    if t >= proj_len() - 12:
        return 0.0
    return float(model_point()["lapse_rate"])


def lapse_rate_mth(t):
    """w^m: the monthly surrender rate actually applied in month t.  **[std]**

    ``1 - (1 - w)^(1/12)`` on the annual rate of :func:`lapse_rate`, the uniform-force
    conversion: twelve monthly exits compound to exactly the year's annual rate, so the
    annual assumption is refined onto the grid rather than restated.  Note that it is
    **larger** than ``w / 12``, which is the convexity a naive division would give away.
    """
    w = lapse_rate(t)
    if w <= 0.0:
        return 0.0
    return 1.0 - (1.0 - w) ** (1.0 / 12.0)


def pols_if_init():
    """The obligations in force at t = 0, one per model point.

    Every shipped model point stands for a single contract, so this is 1.0 and every
    monetary cells is per policy.  It is carried explicitly so that a model point standing
    for a cohort can be scaled without touching a formula.
    """
    return float(model_point()["pols_if_init"])


def charge_basis():
    """This shape's row of ``data.charge_table()`` as a Series.

    The load, the 위험보험료, the commission and the annuity-period charge are published by
    shape, because the shapes buy different things: the life shape pays no death benefit
    once the annuity has begun and therefore carries no risk premium at all, while the two
    that keep a 10%-of-premium death benefit carry one.
    """
    return data.charge_table().loc[shape()]                          # noqa: F821


def acq_charge_rate():
    """The 계약체결비용 (*gyeyak chegyeol biyong*) as a share of the single premium.

    Deducted **once**, at inception, on every retrieved carrier.  2.20% on the
    representative basis.  Because it is taken in full at t = 0 there is no unamortised
    acquisition cost, which is why the 해약공제액 can be nil at every duration without the
    insurer giving anything away.
    """
    return float(charge_basis()["acq_charge_rate"])


def admin_charge_rate():
    """The 계약관리비용 (*gyeyak gwalli biyong*) as a share of the single premium.

    1.30% on the representative basis, and — like the acquisition charge — deducted once at
    inception rather than levied over the life of the contract.
    """
    return float(charge_basis()["admin_charge_rate"])


def expense_load_rate():
    """c: the whole one-off expense load, 계약체결비용 plus 계약관리비용.

    3.50% on the representative basis.  A single number is carried across all three shapes
    rather than the anchor carrier's 0.42-point allocation difference between them, because
    a second and entirely independent carrier's published 확정기간연금형 figures are
    reproduced within 1.4% across four terms on exactly this total.
    """
    return acq_charge_rate() + admin_charge_rate()


def risk_prem_rate():
    """b: the 위험보험료 (*wiheom boheomnyo*) as a share of the single premium.

    Nil on the life shape, which pays no death benefit once the annuity has begun, and
    1.47% on the two shapes that keep one.  Deducted once at inception with the load, so it
    reduces the opening 계약자적립액 and never appears as a projected cash flow: what it
    buys appears instead as :func:`claims` on the ``DEATH`` kind.
    """
    return float(charge_basis()["risk_prem_rate"])


def comm_rate():
    """The 모집수수료율, the first-year commission as a share of the single premium.

    2.00% at t = 0 and nil thereafter.  The rate that matters structurally is not its level
    but that it sits **below** the 계약체결비용: the acquisition charge taken from the fund
    at inception covers the commission paid out of it at the same moment, so this model has
    no acquisition strain and no deferred acquisition cost to amortise.
    """
    return float(charge_basis()["comm_rate"])


def acq_expense_rate():
    """The insurer's own acquisition and administration expense at t = 0, less commission.

    **[std]** and derived: the 3.50% load less the 2.00% commission.  Setting the expense
    equal to the charge is the composite's treatment, not a carrier's disclosure, and it is
    what makes :func:`check_premium_split` close: the single premium divides exactly into
    commission, expense, 위험보험료 and the opening 계약자적립액, with nothing left over in
    either direction.
    """
    return float(charge_basis()["acq_expense_rate"])


def annuity_charge_rate():
    """The 연금수령기간 중 비용: 0.80% of the 연금연액 each year in payment.

    Disclosed in the cost table rather than the benefit table, so the composite models it
    as an **insurer expense measured on the annuity** and does *not* net it off the
    policyholder's payment.  Whether a carrier's own 산출방법서 builds it into the annuity
    factor instead is unverified: no filed basis document for an 즉시연금 discloses the
    annuity formula.
    """
    return float(charge_basis()["annuity_charge_rate"])


def db_rate():
    """The 사망보험금 as a share of the single premium: nil, or 10%.

    Nil on the life shape after annuitisation, where the unpaid guaranteed instalments are
    the only thing that survives the annuitant.  10% of the single premium on the other two
    shapes — the near-universal Korean design — payable **in addition to** the 계약자적립액
    on the inheritance shape, and alone on the certain shape, whose remaining instalments
    continue on their own dates.
    """
    return float(charge_basis()["db_rate"])


def decl_rate():
    """i_d: the 공시이율 (*gongsi iyul*), the declared crediting rate.

    2.50% a year on the representative basis, reset on the first of each month and fixed
    for that month.  It is the **annual** rate, which is how a carrier declares it and how
    every retrieved illustration quotes it; :func:`crediting_rate_mth` is the monthly
    equivalent the fund actually rolls on.  It is a **scalar** and not a derived quantity:
    감독규정 제7-65조제3항
    makes it the product of a 공시기준이율 and a 조정률, with the 공시기준이율 a weighted
    average of an external index and the insurer's own 운용자산이익률 whose weighting the
    two carriers that publish one publish differently.  Any model that claims to derive a
    Korean declared rate is not defensible; this one exposes it.
    """
    tbl = data.crediting_table()                                     # noqa: F821
    rows = tbl[tbl["basis_id"] == crediting_basis()]
    if len(rows) == 0:
        raise ValueError("no crediting basis %s" % crediting_basis())
    values = set(round(float(v), 12) for v in rows["decl_rate"])
    if len(values) != 1:
        raise ValueError("declared rate is not uniform within a basis")
    return float(rows["decl_rate"].iloc[0])


def min_guar_rate(t):
    """i_g(t): the 최저보증이율 (*choejeo bojeung iyul*) applying in period t.

    Duration-stepped, 1.25% in policy years 1 to 5, 1.00% to year 10 and 0.75% thereafter
    on the representative schedule.  Each row of the table gives a half-open band
    ``[dur_from, dur_to)`` in completed **policy years**, and the table is left in years
    because that is how the schedule is published: month ``t`` falls in the band containing
    ``t // 12``, so the floor steps on the 계약해당일 and is level across the twelve months
    of a policy year.  That a floor exists at all is not a commercial courtesy: 감독규정
    제7-60조제10호 requires a 금리연동형보험 to set one.  Note what it is **not**: a rate on
    the fund, never a floor on the annuity, which is the substance of the whole 과소지급
    dispute.
    """
    tbl = data.crediting_table()                                     # noqa: F821
    y = t // 12
    for _, row in tbl.iterrows():
        if (str(row["basis_id"]) == crediting_basis()
                and int(row["dur_from"]) <= y < int(row["dur_to"])):
            return float(row["min_guar_rate"])
    raise ValueError("no 최저보증이율 band for basis %s at t = %s"
                     % (crediting_basis(), t))


def crediting_rate(t):
    """i(t) = Max[공시이율, 최저보증이율]: the rate credited to the fund in period t.

    The 약관's own rule, and the one the supervisor restated when it explained the disputed
    product: 「보험료에 일정한 이율을 곱하여 산출한 금액 … Max [공시이율, 최저보증이율]」.
    On the representative basis the declared rate is above the floor at every duration, so
    the rate is level and the floor is inert; on the ``min_guar`` basis it is the floor that
    binds, and it steps down at five and ten years — months 60 and 120 on this grid.  It is
    the **annual** rate; the fund rolls on :func:`crediting_rate_mth`.
    """
    return max(decl_rate(), min_guar_rate(t))


def crediting_rate_mth(t):
    """j(t) = (1 + i(t))^(1/12) - 1: the monthly rate the fund is actually credited with.

    The uniform-force conversion of the annual credited rate, so twelve months compound back
    to exactly the year's figure and the fund at every 계약해당일 is the annual-step model's.
    The conversion is the model's, not the contract's: a Korean carrier declares an annual
    공시이율 and accrues 「일자계산」 beneath it, and this is the monthly reading of that
    annual rate.
    """
    return (1.0 + crediting_rate(t)) ** (1.0 / 12.0) - 1.0


def mort_rate(t):
    """q(x + t): the 개인연금사망률 at the attained 보험나이 in period t.

    Read from the shipped **[std]** annuitant table by ``(sex, age)``.  It is used two ways
    and the difference matters: by :func:`annuity_factor` as the **pricing basis** of the
    종신연금형, which is the only shape whose annuity uses mortality at all, and by
    :func:`lives_if` as the **decrement** on every shape, because the inheritance and
    certain shapes both pay a death benefit even though neither prices one into its
    annuity.

    It is the **annual** rate the table publishes, level across the twelve months of a
    policy year and stepping on each 계약해당일; :func:`mort_rate_mth` is what the monthly
    grid applies.
    """
    return float(data.mort_table().loc[(sex(), age(t)), "mort_rate"])  # noqa: F821


def mort_rate_mth(t):
    """q^m: the monthly mortality rate applied in month t.

    ``1 - (1 - q)^(1/12)`` on the annual rate at the attained 보험나이, the uniform-force
    conversion: twelve monthly decrements compound to exactly the year's ``q``, so the
    annual table is refined onto the grid rather than restated on a monthly base no Korean
    basis publishes.  The monthly force is **larger** than ``q / 12``, which is the
    convexity a naive division would give away.

    At the limiting age the table's ``q`` is 1, which cannot be converted that way: the
    certain death is instead spread uniformly over the twelve months of that policy year,
    ``1 / (12 - t mod 12)``, so the last of the in-force leaves in the final month of the
    frame rather than all at once on the 계약해당일.
    """
    q = mort_rate(t)
    if q >= 1.0:
        return 1.0 / (12 - t % 12)
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def risk_prem_pp():
    """B: the 보장계약 보험료, the part of the single premium buying the death benefit.

    Deducted once at inception.  It is the ``B`` of the determination's own division of the
    premium — 단일 보험료 A = 보장계약 보험료 B + 사업비 C + 연금계약 순보험료 D — and it
    never becomes a projected cash flow; the benefit it buys does.
    """
    return prem_pp() * risk_prem_rate()


def av_pp_init():
    """V(0): the opening 계약자적립액, the residue D of the premium split.

    ``P x (1 - c - b)``: 96.50% of the single premium on the life shape, which carries no
    risk premium, and 95.03% on the two shapes that keep a death benefit.  The 약관 states
    the identity in words — 「연금계약적립액이란 … 연금계약순보험료(사망보장이 있는 경우
    납입하신 보험료중 보장을 위한 보험료 및 예정사업비를 차감한 금액)를 공시이율로 … 적립한
    금액」 — and :func:`check_premium_split` asserts it against the cash flows.
    """
    return prem_pp() * (1.0 - expense_load_rate() - risk_prem_rate())


def maturity_benefit():
    """M: the 만기보험금, payable on survival to the end of the 보험기간.

    **The gross single premium**, on the inheritance shape alone — 「만기보험금 : 납입
    보험료 총액」.  Nil on the other two shapes: the life shape has no maturity at all, and
    the certain shape's fund is exhausted by its own instalments.  That ``M`` exceeds
    ``V(0)`` by the whole first-day deduction is the entire mechanic of the retention, and
    of the dispute about it.
    """
    return prem_pp() if shape() == "inheritance" else 0.0


def annuity_factor_certain(m, i):
    """a(m, i): the present value of ₩1 a period in arrears for m periods at rate i.

    The 확정기간연금형's whole pricing basis, and the annuity part of the inheritance
    shape's prospective value.  On the monthly grid every caller passes a **month** count
    and a **monthly** rate, so the factor is a monthly annuity-certain and the instalment it
    produces is the 연금월액.  Returns 0 for a non-positive term, which is what makes the
    fund close to zero at the end of the certain shape's last period.
    """
    if m <= 0:
        return 0.0
    if i == 0.0:
        return float(m)
    return (1.0 - (1.0 + i) ** (-m)) / i


def accum_factor(m, i):
    """s(m, i): the accumulated value of ₩1 a period in arrears over m periods at rate i.

    The denominator of the 만기보험금 지급재원, called with a **month** count and a
    **monthly** rate.  Because ``s`` **shrinks** when the rate falls, the retention *rises*
    as the interest it is deducted from falls — which is why an annuity on the inheritance
    shape can halve while the guaranteed floor never moves.
    """
    if m <= 0:
        return 0.0
    if i == 0.0:
        return float(m)
    return ((1.0 + i) ** m - 1.0) / i


def annuity_factor():
    """ae(x, g, i): the 종신연금형 annuity factor, struck once at commencement.

    The present value of ₩1 a **month** in arrears payable while the annuitant aged x lives
    **or the 보증지급기간 of g years runs, whichever is longer**, discounted at the monthly
    crediting rate at inception and decremented on the monthly conversion of the
    개인연금사망률.  It is a ``max`` over the two and not a sum: within the guarantee the
    instalment is due whether or not the annuitant lives, and an additive construction would
    pay for both.  Because the grid is monthly the factor is a monthly annuity-due-in-arrears
    of about twelve times the annual one, and the instalment it produces is the 연금월액 the
    contract actually pays — no ``(f − 1)/(2f)`` frequency correction is needed, because the
    frequency is the grid.

    No carrier publishes a factor and no filed 산출방법서 for an 즉시연금 was retrieved, so
    every annuity factor in this library is computed by the model from a **[std]** table.
    The sum runs over exactly the periods the projection carries, so the pricing and the
    projection cannot drift apart; :func:`check_annuity_basis` asserts that they have not.

    Defined on the life shape alone, and raises elsewhere: 「확정형과 상속형은 사망률을
    사용하지 않는다」.
    """
    if shape() != "life":
        raise ValueError("only 종신연금형 converts the fund through an annuity factor")
    j = crediting_rate_mth(0)
    v = 1.0 / (1.0 + j)
    return sum(v ** (t + 1) * pricing_factor(t)
               for t in range(proj_len()))


def retention_pp(t):
    """R(t): the 만기보험금 지급재원 retained out of period t's interest.

    ``(M - V(t)) / s(m, j(t))`` on the inheritance shape under ``as_designed``, with
    ``m = 12n - t`` the remaining term **in months** and ``j`` the monthly crediting rate,
    recomputed each month so that the fund still reaches the 만기보험금 exactly at maturity
    however the rate has moved.  Zero under ``as_ordered``, and zero on the other two
    shapes, neither of which has a maturity benefit to fund.

    This is the term that was written into the 산출방법서 and not into the 약관, and the
    whole of 조정결정 제2017-17호 is about whether it is part of the contract.
    """
    if shape() != "inheritance" or retention_basis() == "as_ordered":
        return 0.0
    return ((maturity_benefit() - av_pp(t))
            / accum_factor(annuity_term_mths() - t, crediting_rate_mth(t)))


def annuity_pp(t):
    """A(t): the 연금월액 payable at the end of month t, per policy and before decrement.

    Three shapes, three constructions, all of them on the monthly grid:

    * **life** — ``V(0) / ae(x, g, j)``, struck once at commencement and level thereafter.
      The 약관 bases it on 「연금개시시의 계약자적립액」, the fund *at commencement*, and the
      annuitant-mortality ratchet is inert on an immediate annuity because there is no
      interval between issue and annuitisation for a table revision to land in.
    * **inheritance** — ``V(t) j(t) - R(t)``, a month's interest on the fund less the
      retention, recomputed every month because the annuity moves whenever the declared
      rate does.
    * **certain** — ``V(t) / a(m, j(t))``, the fund divided over the remaining term in
      months, again recomputed as the rate moves.

    This is the **연금월액**, which is what the contract actually pays — 「미지급된 연금월액을
    매월 연금지급일에 드립니다」.  The 연금연액 a Korean illustration quotes is
    :func:`annuity_pp_annual`, twelve times this figure; the monthly grid pays the monthly
    amount and needs no sub-annual correction to value it.
    """
    if shape() == "life":
        return av_pp_init() / annuity_factor()
    j = crediting_rate_mth(t)
    if shape() == "certain":
        return av_pp(t) / annuity_factor_certain(annuity_term_mths() - t, j)
    return av_pp(t) * j - retention_pp(t)


def annuity_pp_annual(t):
    """The 연금연액: twelve times the 연금월액 payable in month t.

    Published because every Korean illustration quotes the annual figure and because the
    0.80% 연금수령기간 중 비용 is disclosed on it, but it is **not** a cash flow: the grid
    pays :func:`annuity_pp` a row, and twelve of those make this.
    """
    return 12.0 * annuity_pp(t)


def av_pp(t):
    """V(t): the 계약자적립액 at time t, before period t's crediting.

    The 약관's own recursion a month at a time, ``V(t + 1) = V(t) (1 + j(t)) - A(t)`` —
    「연금개시후에는 생존연금 발생분을 차감한 금액」 — opening at :func:`av_pp_init`.

    It reaches ``M`` exactly at maturity on the inheritance shape under ``as_designed``,
    stands still at ``V(0)`` under ``as_ordered``, and exhausts to zero at the end of the
    term on the certain shape.  **On the life shape it is none of those things**: a life
    annuity's fund is not its reserve, and the recursion runs negative at about the point
    where the annuitant has outlived the factor the fund bought.  Surrender is prohibited
    there, :func:`cv_pp` is nil, and nothing downstream of this cells reads the negative
    value; it is published because the recursion is the contract's, and suppressing it
    would hide what a 종신연금형 actually does with the money.
    """
    if t == 0:
        return av_pp_init()
    return av_pp(t - 1) * (1.0 + crediting_rate_mth(t - 1)) - annuity_pp(t - 1)


def surr_chg_pp(t):
    """The 해약공제액 (*haeyak gongjeaek*), the surrender deduction: **nil at every t**.

    Published as a complete run of zeros by the anchor carrier — 「해지공제금액(만원) 0 … 0
    / 해지공제비율 0.0% … 0.0%」 — and independently confirmed by the same carrier's rate
    disclosure.  The reason is structural rather than generous: a single-premium annuity has
    no unamortised acquisition cost to recover, the cost having been taken in full at
    inception.  The statutory cap of 별표 14's 표준해약공제액 therefore binds nothing here,
    and the cells exists to say that the zero was observed rather than assumed.
    """
    return 0.0


def cv_pp(t):
    """CV(t): the 해약환급금, the 계약자적립액 less the 해약공제액, floored at zero.

    Nil at every duration on the life shape, where surrender is contractually impossible
    once the annuity is in payment and on an immediate annuity that is from month one.
    Equal to the fund on the other two shapes, because the deduction is nil.  The
    위법계약의 해지 route returns the 계약자적립액 rather than the surrender value, and on a
    product with no deduction the two coincide, so no separate cells is carried for it.
    """
    if shape() == "life":
        return 0.0
    return max(av_pp(t) - surr_chg_pp(t), 0.0)


def lives_if(t):
    """l(t): the probability the annuitant is alive at time t.

    Mortality alone, on the 개인연금사망률, opening at :func:`pols_if_init`.  It is **not**
    the payment weight and it is not :func:`pols_if`: within the 보증지급기간 the
    instalments are due whether or not the annuitant lives, and on the certain shape they
    are due for the whole term.  It drives the death benefit on the two shapes that carry
    one and the tail of the life annuity on the shape that does not.
    """
    if t == 0:
        return pols_if_init()
    return lives_if(t - 1) * (1.0 - mort_rate_mth(t - 1))


def surr_if(t):
    """The probability the contract has not been surrendered by time t.

    Identically one on the life shape, where surrender is impossible.  On the other two it
    is the running product of ``(1 - w^m)``, with the rate nil in the final policy year so
    that a contract in its last year runs to its maturity benefit or its last instalment.
    """
    if t == 0:
        return pols_if_init()
    return surr_if(t - 1) * (1.0 - lapse_rate_mth(t - 1))


def pols_if(t):
    """IF(t): the probability that a **payment obligation remains** at time t.

    This is *not* a policy count and it is not a survival probability, and the difference is
    a product fact rather than a modelling choice.  On the **life** shape the instalments
    inside the 보증지급기간 are due whether or not the annuitant lives — 「보증지급기간안에
    사망시에는 잔여보증지급기간 동안, 미지급된 연금월액을 … 드립니다」 — so the obligation
    is the *greater* of the survival probability and the indicator that the guarantee is
    still running.  On the **certain** shape it is one until the term ends or the contract
    is surrendered, death not accelerating it.  On the **inheritance** shape it is survival
    and persistency together, because death itself triggers a payment and ends the contract.

    The name is lifelib's and is kept because it is what the rest of the library weights
    expense by and what ``result_cf()`` publishes first; the meaning is the technical notes'
    ``IF(t)``.
    """
    if shape() == "life":
        guaranteed = pols_if_init() if t < annuity_term_mths() else 0.0
        return max(lives_if(t), guaranteed)
    if shape() == "certain":
        return surr_if(t)
    return lives_if(t) * surr_if(t)


def pols_death(t):
    """d(t): deaths during period t, among contracts still in force at time t.

    Deaths are placed at the **end** of the policy month, after the month's crediting and
    after the annuity due to the survivors, so the 사망보험금 is paid on the fund carried
    forward.  That is a **[std]** convention, and on a monthly grid a much cheaper one than
    it was on an annual grid: the unmodelled lag between the date of death and the period
    end is now at most a month, not at most a year.
    """
    return lives_if(t) * surr_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Surrenders during period t, taken at the end of it and after the deaths.

    Nil on the life shape, where surrender is contractually impossible.  On the certain
    shape the contract survives the annuitant, so the decrement bites on the persistency
    measure alone; on the inheritance shape only a contract that has not become a death
    claim can be surrendered, so the deaths of the period come off first.
    """
    if shape() == "life":
        return 0.0
    if shape() == "certain":
        return surr_if(t) * lapse_rate_mth(t)
    return (lives_if(t) * (1.0 - mort_rate_mth(t)) * surr_if(t)
            * lapse_rate_mth(t))


def pols_exit(t):
    """The obligations ending during period t, however they end.

    Built independently of :func:`pols_if` so that the two can be compared, which is what
    :func:`check_pols_roll_fwd` does.  On the certain and inheritance shapes it is the
    decrements themselves.  On the **life** shape it is neither, and the difference is the
    guarantee: a death inside the 보증지급기간 does not end the obligation, so nothing exits
    at all until the guarantee expires, and then everyone who died inside it exits at once.
    That step is the shape's characteristic feature and an implementation that decremented
    the obligation on death would smooth it away.
    """
    if shape() == "life":
        g = annuity_term_mths()
        if t < g - 1:
            return 0.0
        if t == g - 1:
            return pols_if_init() - lives_if(g)
        return pols_death(t)
    if shape() == "certain":
        return pols_lapse(t)
    return pols_death(t) + pols_lapse(t)


def payment_factor(t):
    """F(t): the weight on the 생존연금 payable at the end of period t.

    On the **life** shape ``max(l(t + 1), 1{t + 1 <= g})``: the instalment is paid if the
    annuitant is alive at the payment date **or** the guarantee is still running.  The
    ``max`` is what makes the 보증지급기간 a floor on the obligation rather than a second
    stream; an additive form would pay ``1 + l(t + 1)`` for the whole guaranteed term.

    On the **certain** shape it is the persistency measure alone, survival being irrelevant
    — 「가입자의 생존여부에 관계없이 연금급여를 지급한다」.  On the **inheritance** shape it
    is in-force survival to the payment date, the 생존연금 being payable 「살아있을 때」,
    with the death benefit taking the place of the payment for those who die.
    """
    if shape() == "life":
        guaranteed = pols_if_init() if t + 1 <= annuity_term_mths() else 0.0
        return max(lives_if(t + 1), guaranteed)
    if shape() == "certain":
        return surr_if(t)
    return pols_if(t) * (1.0 - mort_rate_mth(t))


def pricing_factor(t):
    """The weight the **pricing** basis puts on the payment at the end of period t.

    The same construction as :func:`payment_factor` on the life shape, because the pricing
    basis and the projection run on one mortality table here and there is no lapse
    assumption to separate them; and one on the other two shapes, whose annuities carry no
    mortality at all.  The two are written separately rather than one calling the other, so
    that :func:`check_annuity_basis` compares two constructions instead of one with itself.
    """
    if shape() == "life":
        guaranteed = 1.0 if t + 1 <= annuity_term_mths() else 0.0
        return max(lives_if(t + 1) / pols_if_init(), guaranteed)
    return 1.0


def disc_factor(t):
    """The present value at inception of ₩1 at time t, on the crediting-rate path.

    Discounting at Max[공시이율, 최저보증이율] period by period, so that a stepping floor is
    handled without assuming a level rate.  This is **not** a valuation rate and this model
    computes no discounted result: it exists for the pricing identity
    :func:`check_annuity_basis` and for :func:`retention_shortfall_pp`, both of which are
    statements about the contract's own basis rather than about value.  Every
    ``technical-notes.md`` in this library specifies *gross* liability cash flows and leaves
    discounting, the 책임준비금, the IFRS 17 CSM and the K-ICS 요구자본 to a layer that
    consumes them.
    """
    if t <= 0:
        return 1.0
    return disc_factor(t - 1) / (1.0 + crediting_rate_mth(t - 1))


def retention_shortfall_pp():
    """What the 조정결정's liability costs the insurer, at inception, per policy.

    ``(M - V(0)) x v(n)`` on the inheritance shape under ``as_ordered``, and zero
    everywhere else.  Under ``as_designed`` the contract funds its own 만기보험금 out of the
    retention and the shortfall is nil; under ``as_ordered`` the annuity is interest on the
    fund alone, the fund stands still at ``V(0)``, and the whole first-day deduction has to
    be found again at maturity from the insurer's own resources.

    Model points 6 and 7 are the same contract on the two bases, so the difference between
    their cash flow statements is the quantity that was litigated from 2017 to 2025.
    """
    if shape() == "inheritance" and retention_basis() == "as_ordered":
        return ((maturity_benefit() - av_pp_init())
                * disc_factor(annuity_term_mths()))
    return 0.0


def proj_years():
    """The projection horizon in **whole policy years**.

    On the inheritance and certain shapes the contract ends at a stated term, so the horizon
    is that term.  On the life shape the projection runs to the limiting age of the shipped
    table, at which ``qx`` is 1, so the obligation is exhausted rather than truncated:
    ``ω - x + 1`` years.  Where the 보증지급기간 outlives the annuitant's limiting age —
    which it cannot on any shipped model point but can at a high enough issue age — the
    guarantee sets the horizon instead.
    """
    if shape() == "life":
        return max(annuity_term(), omega_age - age_at_entry() + 1)   # noqa: F821
    return annuity_term()


def proj_len():
    """N: the **number of projected months**, the frame's exclusive end.

    ``12 x proj_years()``.  ``result_cf()`` runs ``t = 0 .. proj_len() - 1`` and the frame is
    ``range(proj_len())``, so the last projected month is ``proj_len() - 1`` and
    ``len(result_cf())`` is ``proj_len()`` itself — 612 rows, ``t = 0`` to ``t = 611``, on
    the worked-example anchor.

    On the inheritance and certain shapes the last row carries the payment falling at time
    ``12n`` with the 만기보험금 beside it where there is one.  On the life shape the last row
    is the final month of the limiting age's policy year, where the monthly conversion of
    ``qx = 1`` pays out the last of the in-force.
    """
    return 12 * proj_years()


def premiums(t):
    """E[PREM(t)]: the 일시납보험료, income at t = 0 and nothing thereafter.

    The single premium is genuine income to the insurer and is projected as such, which is
    what makes the absence of acquisition strain visible in the statement rather than only
    in prose: at t = 0 the premium less the commission and the acquisition expense is
    exactly the opening 계약자적립액 plus the 위험보험료 retained against the death benefit.
    There is no renewal premium, no 추가납입 and no premium term.
    """
    return prem_pp() * pols_if_init() if t == 0 else 0.0


def annuity_payments(t):
    """E[ANN(t)]: the expected 생존연금 outgo at the end of period t.

    The 연금연액 weighted by :func:`payment_factor`.  On the life shape the weight is one
    for every payment inside the 보증지급기간 whether or not the annuitant lives, which is
    why the first ten rows of the anchor model point carry the full annuity.
    """
    return annuity_pp(t) * payment_factor(t)


def claims(t, kind):
    """E[CLAIM(t, kind)]: the expected benefit outgo of period t of one kind.

    ``"DEATH"``
        The 사망보험금.  Nil on the life shape, which pays none once the annuity has begun —
        the unpaid guaranteed instalments are what survives the annuitant, and they are in
        :func:`annuity_payments`.  On the inheritance shape it is 10% of the single premium
        **plus the 계약자적립액 at death**, the fund being the one carried forward at the end
        of the period.  On the certain shape it is the 10% alone: the remaining instalments
        fall due on their own dates and are already in the annuity stream.
    ``"LAPSE"``
        The 해약환급금 paid on voluntary surrender, at the fund carried forward because the
        deduction is nil.  Nil on the life shape, where surrender is impossible.
    ``"MATURITY"``
        The 만기보험금, on the inheritance shape at the end of its last period, weighted by
        the probability of reaching it alive and in force.

    The cells stays and the ``claims`` **column** does not: a cash flow statement must not
    publish its own subtotal beside its parts, so ``result_cf()`` carries the three kinds
    split out and they sum, with the annuity and the outgo above, to ``net_cf``.
    """
    if kind == "DEATH":
        if shape() == "life":
            return 0.0
        if shape() == "inheritance":
            return pols_death(t) * (db_rate() * prem_pp() + av_pp(t + 1))
        return pols_death(t) * db_rate() * prem_pp()
    if kind == "LAPSE":
        return pols_lapse(t) * cv_pp(t + 1)
    if kind == "MATURITY":
        if shape() == "inheritance" and t == proj_len() - 1:
            return pols_if(t + 1) * maturity_benefit()
        return 0.0
    raise ValueError("unknown claim kind: %s" % kind)


def claims_death(t):
    """E[DTH(t)]: :func:`claims` on the ``DEATH`` kind, as a statement column."""
    return claims(t, "DEATH")


def claims_lapse(t):
    """E[SUR(t)]: :func:`claims` on the ``LAPSE`` kind, as a statement column.

    Named for the decrement rather than for the 해약환급금, because ``claims_surr`` was
    retired across the library in favour of the name matching the ``kind`` argument that
    produces it.
    """
    return claims(t, "LAPSE")


def claims_maturity(t):
    """E[MAT(t)]: :func:`claims` on the ``MATURITY`` kind, as a statement column."""
    return claims(t, "MATURITY")


def commissions(t):
    """E[COM(t)]: the 모집수수료 paid at inception and nil in every later year.

    2.00% of the single premium at t = 0.  Every retrieved figure for this product is a
    first-year-only rate on a bancassurance sale, which is what the very low level is
    consistent with and with nothing else in Korean retail life insurance.
    """
    return prem_pp() * comm_rate() * pols_if_init() if t == 0 else 0.0


def expenses(t):
    """E[EXP(t)]: the insurer's own expense outgo in period t.

    Two components and they do not overlap.  At t = 0 the acquisition and administration
    expense, taken as the load less the commission so that the charge deducted from the
    fund exactly meets the outgo.  In every month including the first, the
    연금수령기간 중 비용 of 0.80% of the 연금연액, incurred when a payment is made and
    therefore carried at the payment's own weight — on the monthly grid that is 0.80% of the
    **연금월액** each month, which over twelve months is exactly the 0.80% of the 연금연액
    the cost table discloses.

    There is no maintenance expense per policy and no expense inflation in this model.  The
    one recurring charge any retrieved 즉시연금 document publishes is measured on the
    annuity, not per policy and not per 만원 of fund, and inventing a per-policy expense
    beside it would be a number with no source at all.
    """
    charge = annuity_charge_rate() * annuity_pp(t) * payment_factor(t)
    if t == 0:
        return charge + prem_pp() * acq_expense_rate() * pols_if_init()
    return charge


def net_cf(t):
    """Net cash flow of period t, **income positive**: premium less every outgo.

    The library-wide orientation, so that a ``result_cf()["net_cf"]`` column can be summed
    or compared across every model here without checking which product it came from.  The
    technical notes' own ``CF(t)`` is outgo-positive and is published verbatim as
    :func:`liability_cf`, which is this cells' exact negative.
    """
    return (premiums(t)
            - annuity_payments(t)
            - claims(t, "DEATH")
            - claims(t, "LAPSE")
            - claims(t, "MATURITY")
            - commissions(t)
            - expenses(t))


def liability_cf(t):
    """CF(t): total gross liability **outgo** in period t, the technical notes' orientation.

    The exact negative of :func:`net_cf`.  Both are published as columns rather than one
    being made to stand for the other, so that a reader holding the notes beside the model
    reads the same sign in both.
    """
    return -net_cf(t)


def check_net_cf_resid(t):
    """The ledger residual of row t: the statement's own parts, less ``net_cf``.

    Rebuilt from ``result_cf()``'s published columns rather than from the formulas, so that
    a component missing from the statement fails here rather than being reconciled only in
    prose.  The identity is the product's: premium income at inception, less the 생존연금,
    the 사망보험금, the 해약환급금, the 만기보험금, the 모집수수료 and the expenses.  There
    is no premium term to reconcile and no acquisition cost to amortise, which is what makes
    this the shortest ledger in the library.
    """
    row = result_cf().loc[t]
    built = row["premiums"] - (row["annuity_payments"]
                               + row["claims_death"]
                               + row["claims_lapse"]
                               + row["claims_maturity"]
                               + row["commissions"]
                               + row["expenses"])
    return built - row["net_cf"]


def check_net_cf():
    """Whether the cash flow statement reconciles to ``net_cf`` at every projected period."""
    tol = val_tol * prem_pp()                                        # noqa: F821
    return bool(all(abs(check_net_cf_resid(t)) < tol
                    for t in range(proj_len())))


def check_pols_roll_fwd_resid(t):
    """``IF(t) - exits(t) - IF(t + 1)``: the obligation roll-forward residual.

    :func:`pols_exit` is built from the decrements and the guarantee rather than from
    :func:`pols_if`, so the two are independent constructions.  On the life shape the check
    has real content: an implementation that decremented the obligation on every death
    would show a residual for every period inside the 보증지급기간, because a death there
    does not end the obligation, and would then miss the step at the end of it.
    """
    return pols_if(t) - pols_exit(t) - pols_if(t + 1)


def check_pols_roll_fwd():
    """Whether the payment obligation rolls forward on its own decrements at every t."""
    return bool(all(abs(check_pols_roll_fwd_resid(t)) < roll_fwd_tol  # noqa: F821
                    for t in range(proj_len())))


def check_lives_roll_fwd_resid(t):
    """``prod(1 - q) - l(t)``: the survival curve against a direct product.

    :func:`lives_if` is a one-step recursion; this rebuilds the same probability as an
    explicit product of ``(1 - q)`` over the attained ages, with no reference to the
    recursion.  An off-by-one in the age indexing — reading ``q`` at the attained age at the
    *end* of the period rather than the start — shows up here from the first period.
    """
    built = pols_if_init()
    for s in range(0, t):
        built *= (1.0 - mort_rate_mth(s))
    return built - lives_if(t)


def check_lives_roll_fwd():
    """Whether the annuitant's survival curve closes against a direct product at every t."""
    return bool(all(abs(check_lives_roll_fwd_resid(t)) < roll_fwd_tol  # noqa: F821
                    for t in range(proj_len() + 1)))


def check_av_roll_fwd_resid(t):
    """The 계약자적립액 against its per-shape closed form, one step back.

    Each branch is a genuinely different derivation of the same fund and not the recursion
    written twice:

    * **inheritance, as designed** — ``V(t) = V(t-1) + (M - V(t-1)) / s(m, i)``, the
      algebraic reduction of ``V(1 + i) - A`` once the retention is substituted, which is
      the form the fund's convergence to ``M`` is visible in;
    * **inheritance, as ordered** — ``V(t) = V(t-1)``, the fund standing still because the
      annuity is exactly the interest;
    * **certain** — ``V(t) = V(t-1) a(m-1, i) / a(m, i)``, the annuity-certain's own
      run-off, which exhausts to zero at the last period without being told to;
    * **life** — ``V(0) (1 + i)^t - A s(t, i)``, the retrospective closed form at the level
      rate :func:`check_rate_level` guarantees the shape carries.
    """
    if t == 0:
        return av_pp_init() - av_pp(0)
    j = crediting_rate_mth(t - 1)
    if shape() == "life":
        j0 = crediting_rate_mth(0)
        built = (av_pp_init() * (1.0 + j0) ** t
                 - annuity_pp(0) * accum_factor(t, j0))
    elif shape() == "certain":
        m = annuity_term_mths() - (t - 1)
        built = (av_pp(t - 1) * annuity_factor_certain(m - 1, j)
                 / annuity_factor_certain(m, j))
    elif retention_basis() == "as_ordered":
        built = av_pp(t - 1)
    else:
        m = annuity_term_mths() - (t - 1)
        built = av_pp(t - 1) + ((maturity_benefit() - av_pp(t - 1))
                                / accum_factor(m, j))
    return built - av_pp(t)


def check_av_roll_fwd():
    """Whether the 계약자적립액 recursion closes against its closed form at every t."""
    tol = val_tol * prem_pp()                                        # noqa: F821
    return bool(all(abs(check_av_roll_fwd_resid(t)) < tol
                    for t in range(proj_len() + 1)))


def check_av_terminal():
    """Whether the fund ends where the contract says it must.

    Zero at the end of the 연금지급기간 on the certain shape, because the instalments have
    exhausted it; the 만기보험금 on the inheritance shape under ``as_designed``, because the
    retention was sized to rebuild it; and ``V(0)`` unchanged under ``as_ordered``, because
    the annuity was exactly the interest and nothing was retained — which is the whole
    reason the maturity benefit then has to come from somewhere else.

    True on the life shape without a test, and deliberately: a life annuity's fund has no
    contractual terminal value.  The pricing identity :func:`check_annuity_basis` is what
    holds that shape to its basis instead.
    """
    tol = val_tol * prem_pp()                                        # noqa: F821
    v = av_pp(proj_len())
    if shape() == "certain":
        return bool(abs(v) < tol)
    if shape() == "inheritance":
        target = (maturity_benefit() if retention_basis() == "as_designed"
                  else av_pp_init())
        return bool(abs(v - target) < tol)
    return True


def check_annuity_basis_resid():
    """The opening fund against the present value of everything it was struck to buy.

    ``sum A(t) x pricing_factor(t) x v(t + 1)``, plus the discounted 만기보험금 on the
    inheritance shape, less ``V(0)`` and less :func:`retention_shortfall_pp`.  Discounting
    runs on the crediting-rate path, so a stepping floor is handled without assuming a level
    rate.

    It ties the projection to the pricing across all three shapes at once.  Under
    ``as_ordered`` the identity does **not** close on ``V(0)`` alone, and it should not: the
    excess is precisely the shortfall the determination left the insurer to fund, which is
    why that term appears on the right-hand side rather than being tolerated away.
    """
    built = sum(annuity_pp(t) * pricing_factor(t) * disc_factor(t + 1)
                for t in range(proj_len()))
    if shape() == "inheritance":
        built += maturity_benefit() * disc_factor(annuity_term_mths())
    return built - av_pp_init() - retention_shortfall_pp()


def check_annuity_basis():
    """Whether the annuity the model projects is the annuity the fund actually bought."""
    return bool(abs(check_annuity_basis_resid()) < val_tol * prem_pp())  # noqa: F821


def check_premium_split():
    """Whether the single premium divides exactly as the 약관 says it does.

    ``A = B + C + D``: the 보장계약 보험료, the 사업비 and the 연금계약 순보험료 that becomes
    the opening 계약자적립액, with the 사업비 split here into the commission actually paid
    out and the expense actually incurred.  Nothing is left over in either direction, which
    is the statement that this product has **no acquisition strain**: the charge taken from
    the fund at inception is exactly the outgo at inception.
    """
    built = (prem_pp() * comm_rate()
             + prem_pp() * acq_expense_rate()
             + risk_prem_pp()
             + av_pp_init())
    return bool(abs(prem_pp() - built) < val_tol * prem_pp())        # noqa: F821


def check_rate_level():
    """Whether the crediting rate is level wherever the model relies on it being so.

    Required on the **life** shape and asserted there.  The 종신연금형 factor is struck once
    at commencement — 「연금개시시의 계약자적립액을 기준으로 … 산출」 — and this model does
    not recompute it, so a life-shape model point whose floor stepped above the declared
    rate part-way through would be projected on a basis the model never priced.  The
    representative declared rate of 2.50% is above every step of the floor, so the condition
    holds on every shipped life-shape point; a model point that broke it would fail here
    rather than silently.

    True on the other two shapes, whose annuities are recomputed every year and which
    therefore carry a stepping rate correctly; model point 8 is the one that does.
    """
    if shape() != "life":
        return True
    i0 = crediting_rate(0)
    return bool(all(abs(crediting_rate(t) - i0) < 1e-15
                    for t in range(proj_len())))


def check_guarantee_certain():
    """Whether every payment inside the 보증지급기간 is weighted at exactly one.

    「종신연금형의 경우 연금지급 개시 후 보증지급기간안에 사망시에는 잔여보증지급기간 동안,
    미지급된 연금월액을 매월 연금지급일에 드립니다」.  The guaranteed instalments are due
    whether or not the annuitant lives, so their weight is the whole obligation and not a
    survival probability, and this is the assertion that the ``max`` in
    :func:`payment_factor` is doing its job rather than being shadowed by a product.

    True on the other two shapes, neither of which has a 보증지급기간: the certain shape's
    whole term is certain and the inheritance shape's annuity is conditional on survival
    throughout.
    """
    if shape() != "life":
        return True
    return bool(all(abs(payment_factor(t) - pols_if_init()) < roll_fwd_tol  # noqa: F821
                    for t in range(0, annuity_term_mths())))


def check_payment_factor_resid(t):
    """``F(t)`` against a second construction of the same weight, per shape.

    On the life shape the ``max`` of the survival probability and the guarantee indicator;
    on the certain shape the obligation itself, mortality being irrelevant to it; and on the
    inheritance shape the obligation less the period's deaths, routed through
    :func:`pols_death` rather than through the mortality rate directly.  A shape that
    started weighting its certain payments by survival, or its survival payments by the
    guarantee, shows up here.
    """
    if shape() == "life":
        guaranteed = pols_if_init() if t + 1 <= annuity_term_mths() else 0.0
        built = max(lives_if(t + 1), guaranteed)
    elif shape() == "certain":
        built = pols_if(t)
    else:
        built = pols_if(t) - pols_death(t)
    return built - payment_factor(t)


def check_payment_factor():
    """Whether the payment weight matches its second construction at every period."""
    return bool(all(abs(check_payment_factor_resid(t)) < roll_fwd_tol  # noqa: F821
                    for t in range(proj_len())))


def check_surr_value():
    """Whether the surrender machinery matches the contract on each shape.

    On the **life** shape: the rate is nil at every duration and the 해약환급금 is nil at
    every duration, because 「종신연금이 지급개시된 이후에는 해지할 수 없습니다」 and on an
    immediate annuity that is from month one.  A life-shape model point carrying a surrender
    rate is a defect in the table, and this is where it fails.

    On the other two shapes: the 해약환급금 is the 계약자적립액 exactly, because the
    해약공제액 is nil at every duration on every retrieved carrier — the published run is a
    run of zeros — and the statutory 표준해약공제액 cap therefore binds nothing here.
    """
    tol = val_tol * prem_pp()                                        # noqa: F821
    if shape() == "life":
        return bool(all(lapse_rate(t) == 0.0 and cv_pp(t) == 0.0
                        for t in range(proj_len())))
    return bool(all(abs(cv_pp(t) - max(av_pp(t), 0.0)) < tol
                    for t in range(proj_len() + 1)))


def result_cf():
    """Result table of cash flows, indexed by the 0-based period index t.

    Row ``t`` carries period ``t``, which runs from time ``t`` to time ``t + 1``: the single
    premium falls at time 0 on row 0, and the annuity shown on row ``t`` falls at time
    ``t + 1``, in arrears on the 계약해당일.  The frame is ``range(proj_len())``, so the
    table has ``proj_len()`` rows indexed ``0 .. proj_len() - 1``.

    ``pols_if`` is the probability that a **payment obligation remains**, which on this
    product is not the probability that the annuitant is alive; see :func:`pols_if`.  The
    three ``claims_*`` columns are the split of :func:`claims` and there is deliberately no
    ``claims`` column beside them, so that the columns sum to ``net_cf``.  Both signs of the
    net flow are published: ``net_cf`` is income-positive, the library-wide convention, and
    ``liability_cf`` is the technical notes' outgo-positive ``CF(t)``.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "commissions": [commissions(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of the fund, the annuity and the decrements, indexed by the same t.

    The companion to :func:`result_cf`: everything the cash flow statement is built out of
    and nothing that is a cash flow itself.  ``av_pp`` and ``cv_pp`` are shown at the
    **start** of the period, as ``pols_if`` is, so a row reads as the state the period opens
    in and the flows that period produces.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "lives_if": [lives_if(t) for t in ts],
            "surr_if": [surr_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "payment_factor": [payment_factor(t) for t in ts],
            "crediting_rate": [crediting_rate(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "annuity_pp": [annuity_pp(t) for t in ts],
            "retention_pp": [retention_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 110

roll_fwd_tol = 1e-10

val_tol = 1e-12

pd = ("Module", "pandas")
