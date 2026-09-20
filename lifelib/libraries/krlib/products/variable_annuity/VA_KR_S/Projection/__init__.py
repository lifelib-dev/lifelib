# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.VA_KR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 4            # or switch the default

``t`` counts **projection months**, 0-based: ``t = 0`` is the month containing the
계약일 and the first 기본보험료, and ``t = proj_len() - 1`` the last month before attained
age ``omega_age``. ``proj_len()`` is the **number** of projected months, so the frame is
``range(proj_len())`` and the policy year containing month ``t`` is ``t // 12 + 1``.

Two dates cut the projection in two. ``pay_months()`` ends the premium-paying period,
and the monthly deduction **steps up** there rather than down,
because the 계약관리비용 for the period after 납입완료 was collected inside the premium
and is now drawn back out of the fund. ``t_ann()`` is the 연금개시나이 계약해당일: the
특별계정 exists for ``t < t_ann()`` and is empty afterwards, the whole 계약자적립액
having moved to the 일반계정 [S6].

.. rubric:: The age basis

Every age in this model is **보험나이** (*boheom nai*, insurance age): 만나이 with
fractions of six months or more rounded up, incrementing on the **policy anniversary**
and not on the birthday, under 표준약관 제21조 [REG-R25]. It is the contractual age, the
index of every Korean rate card, and the basis the 경험생명표 is graduated on, so the
model point ages and both mortality bases are on one basis and no shift is applied.
Reading a 만나이 model point against this table would understate the rate by about half
a year of ageing on every row. The one place Korean practice uses 만나이 instead is the
가입나이 envelope, 만15세–70세 [S1] [S2], which is an issue rule rather than a
projection quantity.

.. rubric:: Input data

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/variable_annuity/``, read at run time rather than stored inside the model.
Each table has a filename Reference and a reader Cells, both on :mod:`~.VA_KR_S.Data`,
reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
fund_file               data.fund_table()                   fund_table.csv
charge_file             data.charge_table()                 charge_table.csv
risk_prem_file          data.risk_prem_table()              risk_prem_table.csv
return_scenario_file    data.return_scenario()              return_scenario.csv
crediting_file          data.crediting_table()              crediting_table.csv
======================  ==================================  ==========================

.. rubric:: Symbol map

The technical notes use compact actuarial symbols; the cells use lifelib names. For a
reader holding the notes beside the model that mapping is the most useful thing in the
file. Notes symbol to cells:

=========================  ==============================  ============================
Notes symbol               Cells                           Meaning
=========================  ==============================  ============================
(row label)                model_point()                   The selected model point row
t                          (the index of result_cf)        Projection month, 0-based
x                          age_at_entry()                  가입나이, 보험나이
x + floor(t/12)            age(t)                          Attained 보험나이 in month t
(none)                     sex()                           M or F
n_p                        pay_term()                      납입기간, in years
12 n_p                     pay_months()                    납입기간, in months
y                          annuity_age()                   연금개시나이, 보험나이
T                          t_ann()                         Month of the 연금개시 계약해당일
m                          defer_years()                   연금개시 전 보험기간, in years
t = 0..N-1                 proj_len()                      Number of projected months, N
omega                      omega_age                       Terminal age of the table, 120
(switch)                   gmab_flag()                     1 보증형, 0 미보증형
(none)                     fund_set()                      Allocation set, on the ladder
(none)                     scenario_id()                   Return path identifier
P                          basic_prem_pp()                 기본보험료, monthly
12 P                       prem_ann_pp()                   Annualized 기본보험료
12 P n_p                   prem_total_pp()                 보험료총액 over 납입기간
P(t)                       premium_mth_pp(t)               기본보험료 payable in month t
A(t)                       addl_prem_pp(t)                 추가납입보험료 in month t
(sum)                      prem_pp(t)                      Total premium in month t
alpha                      acq_charge_pp(t)                계약체결비용
beta_1                     maint_charge_in_pp(t)           계약관리비용, 납입기간 이내
beta_2                     maint_charge_after_pp(t)        계약관리비용, 납입기간 이후
gamma                      other_charge_pp(t)              기타비용
(sum)                      prem_charge_pp(t)               Deducted at premium payment
1 - l                      prem_alloc_ratio(t)             특별계정 투입 ratio, 91.33%
P_sa(t)                    prem_to_av_pp(t)                특별계정 투입보험료
r(x)                       risk_prem_rate(x)               위험보험료 rate by 보험나이
R(t)                       risk_prem_pp(t)                 위험보험료
c_d                        gmdb_charge_pp(t)               최저사망보험금 보증비용
c_a                        gmab_charge_asset_pp(t)         GMAB 보증비용, asset part
c_p                        gmab_charge_prem_pp(t)          GMAB 보증비용, premium part
(sum)                      gmab_charge_pp(t)               최저연금적립금 보증비용
B(t)                       gmab_prem_base_pp(t)            보험료총액, the c_p base
D(t)                       mth_deduct_pp(t)                월공제액
f_j                        fund_mgmt_fee(j)                특별계정 운용보수, fund j
w_j                        fund_alloc(j)                   Allocation to fund j
i_j                        gross_return(j)                 Gross asset return, fund j
F_j(t)                     fund_pp(t, j)                   Fund j balance, end of month
(within-month)             fund_pp_at(t, j, timing)        BEF_PREM / BEF_DEDUCT / ...
AV(t)                      av_pp(t)                        계약자적립액, end of month
(within-month)             av_pp_at(t, timing)             The same, inside the month
I(t)                       inv_income_pp(t)                Gross separate-account return
M(t)                       mgmt_fee_pp(t)                  특별계정 운용보수 taken
(none)                     bond_weight(t)                  채권형 share of the account
b_min                      bond_floor()                    Mandatory 채권형 minimum
(none)                     derisk_amount_pp(t)             Pre-annuitisation de-risking
W(t)                       wd_pp(t)                        중도인출금
(cumulative)               wd_cum_pp(t)                    중도인출 to date
K_d(t)                     prem_paid_pp(t)                 이미 납입한 보험료
DB(t)                      db_pp(t)                        사망보험금, 연금개시 전
(top-up)                   gmdb_claim_pp(t)                GMDB guarantee claim
C                          surr_chg_pp(t)                  해약공제액
C_max                      surr_chg_cap_pp()               표준해약공제액, 별표 14
CV(t)                      cv_pp(t)                        해약환급금
AV(T)                      av_ann_pp()                     계약자적립액 at 연금개시
K(T)                       gmab_base_pp()                  최저연금적립금 strike
(payoff)                   gmab_claim_pp()                 GMAB intrinsic value at T
(fund)                     annuity_fund_pp()               연금재원
i_c                        annuity_int_rate()              공시이율 at annuitisation
(ladder)                   credit_rate(k)                  Max[공시이율, 최저보증이율]
k p_y                      ann_surv(k)                     연금사망률 survivorship
a-due                      annuity_factor()                종신연금 10년 보증기간부
Y                          annuity_ann_pp()                연금 연액, gross
(charge)                   annuity_charge_pp()             연금수령기간 중 계약관리비용
Y_net                      annuity_net_pp()                연금 연액 actually paid
q(x)                       mort_rate_at_age(x)             보험사망률 at 보험나이 x
q_a(x)                     ann_mort_rate_at_age(x)         연금사망률 at 보험나이 x
q(t)                       mort_rate(t)                    Annual death rate in month t
(monthly)                  mort_rate_mth(t)                Monthly death rate
w(t)                       lapse_rate(t)                   Annual 해지율
(monthly)                  lapse_rate_mth(t)               Monthly 해지율
l(t)                       pols_if(t)                      In force, start of month t
(within-month)             pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / ...
d(t)                       pols_death(t)                   Expected deaths
s(t)                       pols_lapse(t)                   Expected 해지
(horizon)                  pols_maturity(t)                Survivors at omega_age
l(T)                       pols_annuitised()               Count reaching 연금개시
(obligation)               pols_annuity_oblig(t)           Payments due in month t
(income)                   premiums(t)                     영업보험료 received
(outgo)                    claims(t, kind)                 Benefit outgo by kind
(released)                 claims_from_av(t, kind)         The 특별계정 part of it
(outgo)                    withdrawals(t)                  중도인출금 paid
(outgo)                    expenses(t)                     Insurer's own expenses
(outgo)                    commissions(t)                  모집수수료
(transfer)                 prem_to_av(t)                   일반계정 to 특별계정
(transfer)                 av_charges(t)                   특별계정 to 일반계정, monthly
(transfer)                 surr_charges(t)                 해약공제액 retained
(transfer)                 av_transfer(t)                  연금재원 moved at 연금개시
(memo)                     gmdb_claims(t)                  GMDB strain on the 일반계정
(memo)                     gmab_claims(t)                  GMAB strain at T
CF(t)                      net_cf(t)                       Net cash flow, income positive
CF_g(t)                    net_cf_gen(t)                   The 일반계정 ledger
CF_s(t)                    net_cf_sep(t)                   The 특별계정 ledger
=========================  ==============================  ============================

.. rubric:: The two deduction points, and why they are not one

Confusing them is the commonest way to get a Korean variable model wrong, and the
conditions are explicit [S7 제2조]: 「월공제액이라 함은 해당월의 위험보험료,
계약관리비용(납입기간 종료 후 유지관련비용), 최저사망적립금 보증비용 및 … 보증비용의
합계액을 말합니다. … 다만, 계약체결비용, 계약관리비용(납입기간 중 유지관련비용),
계약관리비용(기타비용)은 보험료를 납입할 때 공제하며 …」.

So :func:`prem_charge_pp` is taken **out of the premium in the 일반계정** and never
enters the fund, while :func:`mth_deduct_pp` is taken **out of the 계약자적립액** by
cancelling units on the 월계약해당일, and :func:`mgmt_fee_pp` is different again — it is
deducted inside the 기준가격 [S7 제43조제2호], which is why it is written as a factor on
the growth rather than as a unit cancellation. The identity [R2] is::

    특별계정 투입보험료 = 납입보험료 − (계약체결비용 + 납입 중 계약유지비용 + 기타비용)
                        = 순보험료 + 납입 후 계약유지비용

and the second line is the one that matters: the 계약관리비용 for the period **after**
납입완료 is collected during the premium period and carried inside the account value,
then drawn back out month by month once premiums stop. On the anchor cell that is
₩273,990 of every ₩300,000 reaching the fund — **91.33%**, inside the 91.3%–91.5%
three carriers publish on this cell [S1] [S2] [S6] — and :func:`check_prem_alloc`
asserts it.

.. rubric:: The premium-based guarantee charge deserves its own paragraph

:func:`gmab_charge_prem_pp` is 0.30% a year of the **보험료총액** — 「이미 납입한
보험료(특약보험료 제외) 및 추후 납입할 기본보험료 합계」, the whole premium the
policyholder has undertaken to pay, past *and* future — levied 「납입기간(최대 7년)
동안」 [S1]. On the anchor cell that is ₩9,000 a month against a first-year account
value of ₩3,216,621: **over 3% a year of the fund at outset**, falling below
0.5% by year seven. A model that treats guarantee charges as basis points on the account
value misstates the early-duration cash flow of this contract by an order of magnitude,
which is why the asset and premium components are separate cells with separate bases.

.. rubric:: The guarantees, and what one path says about them

:func:`gmdb_claim_pp` is ``max(0, 이미 납입한 보험료 − 계약자적립액)`` and is a real
expected cash flow on this path, because the mortality decrement is a probability
applied to a deterministic account value. :func:`gmab_claim_pp` is
``max(0, K(T) − AV(T))`` at the **single** date ``T``, paid only on survival **and**
persistency to it: the GMAB is void on surrender, on lapse, on death before
annuitisation and on 조기연금개시 [S1] [S6] [S7 제50조제3항] [R1]. A model that treated
it as a floor on the account at every duration would overstate its cost by the whole of
the pre-annuitisation exit probability, which on a seven-year persistency below 30% [R1]
is most of it.

On one path both figures are **intrinsic values**, and by Jensen's inequality each is a
lower bound on the expected cost. The base run's account is above the strike at
annuitisation, so it reports a GMAB cost of exactly zero while collecting the full
guarantee charge; model point 4 runs the mandated −1.00% return, on which it is not. The
gap between :func:`gmab_charges` collected and :func:`gmab_claims` incurred is a
**single-path residual and not a profit**, and the statutory 보증준비금 — a CTE(70) over
a thousand scenarios, or a standard factor, whichever is greater [REG-R10] [REG-R26]
[R1] — is not computable from this run and is not published by it.

.. rubric:: Which account, and how the model proves it

Every transfer in :func:`net_cf_gen` and :func:`net_cf_sep` is one of the movements
감독규정 제5-7조 permits between the two accounts [REG-R15]: premium receipt and benefit
payment, transfer to the general account of the amounts needed for risk cover and for
acquisition, maintenance and administration, management fees, and the 연금재원 moved at
연금개시. Each appears in both ledgers with opposite signs, so their sum is the
whole-contract external cash flow :func:`net_cf` and nothing else.
:func:`check_net_cf` asserts exactly that, and it is the identity this product's cash
flow statement turns on.

.. rubric:: Model points

``model_point_table.csv`` carries ten contracts. Point **1** is the anchor: 남자 보험나이
40, 기본보험료 ₩300,000 월납, 10년납, 연금개시나이 60, 보증형, 채권형 50% / 주식형 50%
— the illustration point three independent carriers publish [S1] [S2] [S6], and the only
cell at which the composite's parameters can be checked against published
surrender-value tables. Point **2** is the same cell female. Point **3** is the
**미보증형**, with the GMAB and its two charge components both removed [S4] [S5]. Points
**4** and **5** are the anchor on the other two mandated illustration returns, −1.00%
and 3.75% [R2], point 4 being the only shipped cell on which the GMAB finishes in the
money. Point **6** is a 5년납 contract with a ten-year 연금개시 전 보험기간, which is the
**<12년** rung of the mandatory 채권형 ladder at 80% [S1], and whose surrender charge is
cut by the 표준해약공제액 cap [REG-R20]. Point **7** sits exactly on the **=12년** rung
at 70%. Point **8** exercises **추가납입** at 100% of the basic premium, which grows the
GMDB base and the GMAB strike without a loading [S1] and — because 보험료총액 is defined
on premiums *paid* as well as payable — grows the premium-based guarantee charge with
it. Point **9** exercises **중도인출**, 10% of the 해약환급금 once a year from the
eleventh 계약해당일 (``t = 132``, the start of the twelfth policy year), which re-bases
both guarantees proportionally [S2]
[S7 제51조제8항]: without that adjustment a policyholder could withdraw the fund and keep
the strike [R1]. Point **10** is the issue envelope — 가입나이 70, 연금개시나이 80,
기본보험료 at the ₩1,000,000 per 구좌 maximum [S1] [S2] [S9] — on the ``min_guar``
crediting basis, so the 최저보증이율 ladder rather than the 공시이율 sets the annuity
factor.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point, a row of ``data.model_point_table()``."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The contract's identifier, carried through to the printed output."""
    return model_point()["policy_id"]


def sex():
    """The insured's sex, ``M`` or ``F``: the rating factor of both mortality bases."""
    return model_point()["sex"]


def age_at_entry():
    """가입나이 (*gaibnai*, issue age) in **보험나이**, at the 계약일.

    The retrieved envelope is 만15세–70세 [S1] [S2]; the shipped points run 35 to 70.
    """
    return int(model_point()["age_at_entry"])


def basic_prem_pp():
    """기본보험료 (*gibon boheomnyo*), the level monthly basic premium per contract.

    Every front-end charge on this product is a rate on **this** amount rather than on
    the premium actually paid, which is why 추가납입보험료 attracts no loading [S1]. The
    observed minimum runs ₩50,000 to ₩500,000 by carrier and the maximum is ₩1,000,000
    per 구좌 [S1] [S2] [S9].
    """
    return float(model_point()["basic_prem_pp"])


def pay_term():
    """납입기간 (*nabip gigan*), the premium-paying term in whole years.

    Retrieved terms are 5 / 7 / 10 / 12 / 15 / 20년납 [S1] [S2].
    """
    return int(model_point()["pay_term"])


def annuity_age():
    """연금개시나이 (*yeongeum gaesi nai*) in **보험나이**, the annuitisation age.

    The retrieved envelope is 45–80 [S1] [S5] [S6] [S9]. The 연금개시 전 보험기간 runs
    from the 계약일 to the day before the 연금개시나이 계약해당일 [S4] [S5] [S7].
    """
    return int(model_point()["annuity_age"])


def gmab_flag():
    """1 on the 보증형 (GMAB elected), 0 on the 미보증형.

    The 최저연금적립금보증 has been elective since April 2016 [R2], so the same chassis
    has to support both forms; the charge and the guarantee are switched together,
    because a 미보증형 pays neither [S4] [S5].
    """
    return int(model_point()["gmab"])


def fund_set():
    """The 특별계정 allocation set, a key of ``data.fund_table()``.

    The three sets sit on the three rungs of the mandatory 채권형 ladder — ``bond80_eq20``
    for a 연금개시 전 보험기간 under twelve years, ``bond70_eq30`` at exactly twelve and
    ``bond50_eq50`` above it [S1] [R1] — so a model point's allocation sits **on** its
    constraint rather than slack of it.
    """
    return model_point()["fund_set"]


def scenario_id():
    """The deterministic return path, a key of ``data.return_scenario()``.

    ``base`` is the 2026 평균공시이율 of 2.50% net of the blended 운용보수 [REG-R48];
    ``low`` and ``high`` are the other two returns a Korean variable illustration must
    show, −1.00% and 3.75% [R2].
    """
    return model_point()["scenario_id"]


def crediting_basis():
    """The payout-phase crediting basis, a key of ``data.crediting_table()``."""
    return model_point()["crediting_basis"]


def addl_prem_ratio():
    """추가납입보험료 as a multiple of the 기본보험료, paid monthly; 0 switches it off.

    Capped cumulatively at 200% of the basic premium paid and payable, universally
    across the retrieved contracts [S1] [S2] [S4] [S5] [S6] [S7] [S10], and attracting
    **no loading** [S1].
    """
    return float(model_point()["addl_prem_ratio"])


def wd_ratio():
    """중도인출 as a fraction of the 해약환급금, once a policy year; 0 switches it off."""
    return float(model_point()["wd_ratio"])


def wd_start_year():
    """The number of completed policy years after which the first 중도인출 is taken.

    An **elapsed count**, not a 1-based policy-year label: the first withdrawal falls on
    the ``wd_start_year``-th 계약해당일, ``t = 12 * wd_start_year()``. With 11 on model
    point 9 that is ``t = 132``, the start of the twelfth policy year. 0 with the module
    off.

    The contract permits twelve withdrawals a policy year from one month after the
    계약일 [S1]; the model takes at most one a year, on the 계약해당일 **[std]**.
    """
    return int(model_point()["wd_start_year"])


def pols_if_init():
    """The number of contracts in force at ``t = 0``: 1, the model point being one 구좌.

    Korean variable annuities are written in 구좌 (*gujwa*), repeatable units of the
    basic premium, with the withdrawal residual floor and the maximum basic premium both
    expressed per 구좌 [S1] [S2] [S10]. One 구좌 keeps the model point one contract.
    """
    return float(model_point()["pols_if_init"])


def pay_months():
    """납입기간 in months, ``12 * pay_term()``, and the month the deduction steps up."""
    return 12 * pay_term()


def t_ann():
    """``T``, the projection month of the 연금개시나이 계약해당일.

    ``(annuity_age() - age_at_entry()) * 12``. The 특별계정 exists for ``t < t_ann()``;
    at ``t_ann()`` the whole 계약자적립액, floored at the GMAB where one was bought, is
    transferred to the 일반계정 and run at the 공시이율 [S6].
    """
    return (annuity_age() - age_at_entry()) * 12


def defer_years():
    """연금개시 전 보험기간 in whole years — the band of the mandatory 채권형 ladder."""
    return annuity_age() - age_at_entry()


def proj_len():
    """The **number** of projected months, ``N`` — the frame's exclusive end.

    The frame is ``range(proj_len())``, so ``t`` runs ``0 … proj_len() - 1`` and
    ``len(result_cf()) == proj_len()``. The contract is a 종신연금형 and has no maturity,
    so the horizon is the terminal age of the shipped mortality table: the projection
    runs while ``age(t) < omega_age``, which is ``(omega_age - age_at_entry()) * 12``
    months. The survivors at that horizon leave through :func:`pols_maturity` with no
    payment, so the in-force roll-forward closes and the truncation is visible rather
    than absorbed.
    """
    return (omega_age - age_at_entry()) * 12                         # noqa: F821


def age(t):
    """Attained **보험나이** at the start of projection month ``t``.

    ``age_at_entry() + t // 12``: 보험나이 increments on the **policy anniversary**, not
    on the birthday [REG-R25 제21조].
    """
    return age_at_entry() + t // 12


def policy_year(t):
    """The policy year containing month ``t``, 1-based: ``t // 12 + 1``."""
    return t // 12 + 1


def yrs_completed(t):
    """Completed whole policy years at the **end** of month ``t``: ``(t + 1) // 12``.

    This is the ``t`` of the 해약공제 scale, whose published rows are labelled 경과
    완성 연수 [S2].
    """
    return (t + 1) // 12


def fund_ids():
    """The 특별계정 fund identifiers of this contract's allocation set, in order."""
    return tuple(int(i) for i in
                 data.fund_table().loc[fund_set()].index)            # noqa: F821


def fund_alloc(j):
    """The share of the 특별계정 투입보험료 allocated to fund ``j``, fixed at issue.

    Selection at issue is up to three funds including a 채권형, in 5% steps [S1] [S5].
    There is no rebalancing in the base run, so the realised mix drifts away from this
    allocation and the drift is itself a modelled quantity — which is what the automatic
    de-risking rules exist to control.
    """
    return float(data.fund_table().at[(fund_set(), j), "alloc"])     # noqa: F821


def fund_mgmt_fee(j):
    """특별계정 운용보수 of fund ``j``, per annum: 채권형 0.40%, 주식형 0.60% [S2].

    Deducted **daily**, at rate/365, out of net assets before the 기준가격 is struck
    [S7 제43조제2호] — so it lives inside the unit price and not in the 월공제액. The
    model takes it monthly at rate/12 **[std]**, the monthly grid having no daily step.
    """
    return float(data.fund_table().at[(fund_set(), j), "mgmt_fee"])  # noqa: F821


def fund_is_bond(j):
    """True when fund ``j`` is the 채권형, the fund the mandatory floor is measured on."""
    return data.fund_table().at[(fund_set(), j),                     # noqa: F821
                                "asset_class"] == "bond"


def bond_floor():
    """The mandatory minimum 채권형 weight for this contract's 연금개시 전 보험기간.

    The same ladder appears at two carriers eight years apart — 12년 미만 ≥80%, 12년
    ≥70%, 12년 초과 ≥50% — and it binds both the premium allocation and the account mix,
    surviving every later 펀드변경 [S1] [R1].
    """
    if defer_years() < 12:
        return bond_floor_short                                      # noqa: F821
    elif defer_years() == 12:
        return bond_floor_mid                                        # noqa: F821
    return bond_floor_long                                           # noqa: F821


def gross_return(j):
    """The annual **gross** separate-account asset return of fund ``j``, constant.

    Gross of the 운용보수, which :func:`fund_mgmt_fee` then takes inside the 기준가격, so
    the management fee is a modelled cash flow rather than an assumption. **Every return
    assumption on this product is [std]**: the only realised Korean figures retrieved are
    the top of a cross-sectional distribution in a trade article [R10] and one live fund
    panel at 904.24원 against the statutory 1,000.00 opening price after fourteen years
    [S11], and no volatility, correlation or time series was retrieved at all.
    """
    return float(data.return_scenario().at[                          # noqa: F821
        (scenario_id(), j), "gross_return"])


def fund_growth(j):
    """One month's growth factor on fund ``j``: gross return, then the 운용보수.

    ``(1 + i_j) ** (1/12) * (1 - f_j / 12)``. The two are written as separate factors
    because they happen at different places — the return accrues on the assets, the fee
    is taken out of net assets before the 기준가격 is struck [S7 제43조제2호].
    """
    return (1.0 + gross_return(j)) ** (1.0 / 12.0) * (
        1.0 - fund_mgmt_fee(j) / 12.0)


def charge_rate(line):
    """One row of the 수수료 안내표: ``data.charge_table()``'s ``value`` for ``line``.

    The lines are the ones a savings-type variable contract must publish — 계약체결비용,
    계약관리비용, 위험보험료, 보증비용, 특별계정운용비용, 해약공제비용 and the
    연금수령기간 중 비용 — plus the commission scale and the insurer's own unit expenses
    [R2].
    """
    return float(data.charge_table().at[line, "value"])              # noqa: F821


def loading_rate():
    """부가보험료 as a fraction of the 기본보험료: 5.17% + 3.50% + 0.00% = **8.67%**.

    The complement, 91.33%, is the 특별계정 투입 ratio, and it is also the 부가보험료 that
    별표 14 excludes in computing the 연납순보험료 for the 표준해약공제액 cap [REG-R20].
    """
    return (charge_rate("acq_charge") + charge_rate("maint_charge_in")
            + charge_rate("other_charge"))


def prem_ann_pp():
    """The annualized 기본보험료, ``12 * basic_prem_pp()``."""
    return 12.0 * basic_prem_pp()


def prem_total_pp():
    """보험료총액 as contracted: the whole 기본보험료 payable over the 납입기간.

    ``12 * pay_term() * basic_prem_pp()`` — ₩36,000,000 (3,600만원) on the anchor cell.
    """
    return prem_ann_pp() * pay_term()


def premium_mth_pp(t):
    """기본보험료 payable in month ``t``, level and in advance."""
    if t < min(pay_months(), t_ann()):
        return basic_prem_pp()
    return 0.0


def addl_prem_pp(t):
    """추가납입보험료 paid in month ``t``, subject to the cumulative 200% cap.

    Permitted to 200% of the basic premium paid and payable, cumulative, with **no
    loading** [S1] — the single largest lever a policyholder has over this product's
    cost, and the reason the front-loaded 계약체결비용 is levied on the 기본보험료 alone.
    Off unless the model point sets :func:`addl_prem_ratio`.
    """
    if addl_prem_ratio() <= 0.0 or t >= min(pay_months(), t_ann()):
        return 0.0
    paid = addl_prem_ratio() * basic_prem_pp() * t
    room = addl_prem_cap_ratio * prem_total_pp() - paid              # noqa: F821
    return max(0.0, min(addl_prem_ratio() * basic_prem_pp(), room))


def prem_pp(t):
    """Total premium per contract in month ``t``: 기본보험료 plus 추가납입보험료."""
    return premium_mth_pp(t) + addl_prem_pp(t)


def acq_charge_pp(t):
    """계약체결비용 (*gyeyak chegyeol biyong*), 5.17% of the 기본보험료 [S2].

    Deducted from the premium **in the 일반계정** before it reaches the fund, for ten
    years from the 계약일 and nil thereafter [S2]. A charge on a premium cannot outlive
    the premium, so the model levies it for the shorter of ten years and the 납입기간
    **[std]**; the two coincide on [S2]'s own 10년납 contract. ₩15,510 a month on the
    anchor cell.
    """
    if t < min(pay_months(), 12 * acq_charge_years, t_ann()):        # noqa: F821
        return charge_rate("acq_charge") * basic_prem_pp()
    return 0.0


def maint_charge_in_pp(t):
    """계약관리비용 inside the 납입기간, 3.50% of the 기본보험료 [S2].

    Deducted from the premium, in the 일반계정. ₩10,500 a month on the anchor cell.
    """
    if t < min(pay_months(), t_ann()):
        return charge_rate("maint_charge_in") * basic_prem_pp()
    return 0.0


def other_charge_pp(t):
    """기타비용, nil in the base run **[std]**.

    [R2]'s cash-flow identity names it and [S7 제2조] confirms it is deducted at premium
    payment, but no retrieved 상품요약서 quantifies it. Held at zero so the premium
    allocation reproduces the observed 91.33% exactly; the line is kept because the
    identity needs it.
    """
    if t < min(pay_months(), t_ann()):
        return charge_rate("other_charge") * basic_prem_pp()
    return 0.0


def prem_charge_pp(t):
    """The whole deduction taken **at premium payment**, in the 일반계정 [S7 제2조].

    계약체결비용 + 납입 중 계약관리비용 + 기타비용. It never enters the 특별계정, which is
    the first of the product's two deduction points and the one a model most easily
    conflates with the second.
    """
    return acq_charge_pp(t) + maint_charge_in_pp(t) + other_charge_pp(t)


def prem_alloc_ratio(t):
    """특별계정 투입보험료 as a fraction of the 기본보험료 in month ``t``.

    **91.33%** while both front-end charges run, rising to 100% once the 계약체결비용
    stops [R2]. Three carriers' first-year illustrations put the realised ratio at 91.3%,
    91.3% and 91.4% on the anchor cell [S1] [S2] [S6], and the textbook publishes 90.0%
    for a 10년납 as the flat-by-age industry figure [R2].
    """
    if premium_mth_pp(t) <= 0.0:
        return 0.0
    return (premium_mth_pp(t) - prem_charge_pp(t)) / basic_prem_pp()


def prem_to_av_pp(t):
    """특별계정 투입보험료: what actually reaches the fund and buys 좌 in month ``t``.

    ``납입보험료 − (계약체결비용 + 납입 중 계약유지비용 + 기타비용) = 순보험료 + 납입 후
    계약유지비용`` [R2]. The second reading is the one that matters: the 계약관리비용 for
    the period after 납입완료 is collected here and carried inside the account value,
    then drawn back out by :func:`maint_charge_after_pp` once premiums stop. 추가납입
    보험료 attracts no loading and enters in full [S1].
    """
    if t >= t_ann():
        return 0.0
    return premium_mth_pp(t) - prem_charge_pp(t) + addl_prem_pp(t)


def risk_prem_rate(x):
    """위험보험료 rate at attained 보험나이 ``x``, a fraction of the 기본보험료.

    A banded lookup on ``data.risk_prem_table()``: the applicable row is the highest
    ``age_from`` at or below ``x``. The published band is 0.004%–0.011% — ₩12 to ₩32 a
    month on the anchor cell [S2] [S4] — and it is that small because the risk premium
    buys only the 고도재해장해급여금 and, on the retrieved contracts, no basic death
    cover at all, which is why the textbook can call the natural premium immaterial and
    the premium allocation flat by age [R2]. The **scale across the band is [std]**.
    """
    tbl = data.risk_prem_table()                                     # noqa: F821
    rows = tbl[tbl["age_from"] <= x]
    return float(rows.iloc[-1]["rate"])


def risk_prem_pp(t):
    """위험보험료 (*wiheom boheomnyo*) in month ``t``, part of the 월공제액.

    ₩24 a month on the anchor cell at issue. It buys the 고도재해장해급여금 of
    ₩10,000,000 per 구좌 [S1] [S2], which this model **charges for and never pays**: no
    장해 incidence rate on this contract's basis was retrieved, the 참조순보험요율 display
    being a 장기손해보험 one that does not reach the life side [REG-R34] [REG-R61]. The
    omission is named in the model docstring rather than hidden.
    """
    if t >= t_ann():
        return 0.0
    return risk_prem_rate(age(t)) * basic_prem_pp()


def maint_charge_after_pp(t):
    """계약관리비용 after 납입완료, 1.33% of the 기본보험료 [S2].

    Taken from the 계약자적립액 on the 월계약해당일 [S7 제2조] — ₩3,990 a month on the
    anchor cell, where the document prints ₩4,000. This is the step the Korean expense
    stack is most often modelled wrong at: at 납입완료 the monthly deduction **rises**,
    with no premium arriving to offset it, and the cumulative separate-account
    contribution of [S2]'s own illustration falls from ₩32,877,360 at ten years to
    ₩32,393,520 at twenty.
    """
    if pay_months() <= t < t_ann():
        return charge_rate("maint_charge_after") * basic_prem_pp()
    return 0.0


def gmdb_charge_pp(t):
    """최저사망보험금 보증비용, 연 0.07% of the 계약자적립액, monthly [S1].

    Deducted from the 특별계정 in the 월공제액 and held in the 일반계정 as
    최저사망보험금 보증준비금, out of which the shortfall on a death below premiums paid
    is met [R2]. Compulsory: 감독규정 제7-60조제7호 requires 변액보험 to set a
    최저사망보험금 [REG-R16], and all 36 products in the 2017 industry census carried one
    [R1].
    """
    if t >= t_ann():
        return 0.0
    return charge_rate("gmdb_charge") / 12.0 * av_pp_at(t, "BEF_DEDUCT")


def gmab_prem_base_pp(t):
    """보험료총액, the base of the premium component of the GMAB charge.

    「이미 납입한 보험료(특약보험료 제외) 및 추후 납입할 기본보험료 합계」 [S1] — the
    whole premium the policyholder has undertaken to pay, past *and* future. With no
    추가납입 it is the constant :func:`prem_total_pp`, ₩36,000,000 on the anchor cell;
    with 추가납입 it grows, because a paid additional premium is 이미 납입한 보험료. Note
    the asymmetry that creates: the charge base and the guarantee strike both grow, but
    the strike keeps growing after the charge has stopped at seven years.
    """
    return prem_total_pp() + addl_prem_ratio() * basic_prem_pp() * min(
        t, min(pay_months(), t_ann()))


def gmab_charge_asset_pp(t):
    """최저연금적립금 보증비용, asset component: 연 0.25% of the 계약자적립액 [S1]."""
    if t >= t_ann() or gmab_flag() == 0:
        return 0.0
    return charge_rate("gmab_charge_asset") / 12.0 * av_pp_at(t, "BEF_DEDUCT")


def gmab_charge_prem_pp(t):
    """최저연금적립금 보증비용, premium component: 연 0.30% of 보험료총액 [S1].

    Levied 「납입기간(최대 7년) 동안」 — for the shorter of the 납입기간 and seven years —
    and **not** on the fund. ₩9,000 a month on the anchor cell, which is over 3% a year
    of the first-year account value and below 0.5% by year seven.
    """
    if gmab_flag() == 0:
        return 0.0
    if t >= min(pay_months(), 12 * gmab_charge_years, t_ann()):      # noqa: F821
        return 0.0
    return charge_rate("gmab_charge_prem") / 12.0 * gmab_prem_base_pp(t)


def gmab_charge_pp(t):
    """최저연금적립금 보증비용 in month ``t``: the asset and premium components together."""
    return gmab_charge_asset_pp(t) + gmab_charge_prem_pp(t)


def mth_deduct_pp(t):
    """월공제액 (*wolgongjeaek*) — the second deduction point, taken from the fund.

    위험보험료 + 납입 후 계약관리비용 + 최저사망보험금 보증비용 + 최저연금적립금 보증비용,
    cancelled out of the 계약자적립액 on the 월계약해당일 [S7 제2조]. Capped at the
    available account value **[std]**: the contract meets an unpayable deduction by
    ending the premium holiday or lapsing [S1], neither of which this model represents.
    """
    if t >= t_ann():
        return 0.0
    raw = (risk_prem_pp(t) + maint_charge_after_pp(t)
           + gmdb_charge_pp(t) + gmab_charge_pp(t))
    return min(raw, max(0.0, av_pp_at(t, "BEF_DEDUCT")))


def wd_pp(t):
    """중도인출금 (*jungdo inchul*) taken in month ``t``, per contract.

    Off unless the model point sets :func:`wd_ratio`. Taken once a policy year on the
    계약해당일 **[std]** against a contract permitting twelve a year [S1], and bounded by
    every published limit: at most 50% of the 해약환급금, a residual 계약자적립액 of at
    least ₩5,000,000 per 구좌 — the anchor carrier's figure [S1], matched by [S5]; [S2]
    publishes ₩3,000,000 — and cumulative withdrawals inside the first ten years no
    greater than the premiums actually paid — the last of these a **tax** rule showing
    through into the policy conditions, since it is what keeps the 소득세법 시행령 제25조
    ten-year exemption open [S1] [S2] [S5] [REG-R58]. No fee is charged [S1] [S2] [S9].
    """
    if wd_ratio() <= 0.0 or t >= t_ann() or t < 12 * wd_start_year():
        return 0.0
    if t % 12 != 0 or t == 0:        # a 계약해당일, not the 계약일 itself
        return 0.0
    base = av_pp_at(t, "BEF_DEDUCT") - mth_deduct_pp(t)
    if base <= 0.0:
        return 0.0
    cv = max(0.0, base - surr_chg_pp(t))
    caps = [wd_ratio() * cv,
            wd_max_cv_ratio * cv,                                    # noqa: F821
            max(0.0, base - wd_min_residual_pp)]                     # noqa: F821
    if t < 12 * wd_cum_cap_years:                                    # noqa: F821
        caps.append(max(0.0, prem_paid_gross_pp(t) - wd_cum_pp(t - 1)))
    return max(0.0, min(caps))


def wd_cum_pp(t):
    """Cumulative 중도인출금 taken to the end of month ``t``, per contract.

    Nil before the first month: the accumulation opens at zero in ``t = 0``.
    """
    return (wd_cum_pp(t - 1) if t > 0 else 0.0) + wd_pp(t)


def prem_paid_gross_pp(t):
    """Premiums actually paid to the end of month ``t``, **before** any withdrawal reduction.

    The base of the ten-year cumulative withdrawal limit [S1] [S2] [S5], which is stated
    on 「실제 납입한 보험료 총액」 and so is not the reduced guarantee base
    :func:`prem_paid_pp`. Nil before the first month: the accumulation opens at zero in
    ``t = 0``, the 계약일 premium being ``prem_pp(0)``.
    """
    return (prem_paid_gross_pp(t - 1) if t > 0 else 0.0) + prem_pp(t)


def fund_pp_at(t, j, timing):
    """The balance of fund ``j`` inside month ``t``, per contract, at ``timing``.

    ``BEF_PREM`` opens the month; ``BEF_DEDUCT`` has taken the 특별계정 투입보험료 in at
    the fixed allocation; ``AFT_DEDUCT`` has cancelled the 월공제액 and any 중도인출 pro
    rata across the funds; ``AFT_DERISK`` has applied the mandatory pre-annuitisation
    reallocation. :func:`fund_pp` then grows this last one over the month.

    The account **opens at nil in month 0**: there is no 특별계정 balance before the first
    premium, so ``BEF_PREM`` is ``0`` at ``t = 0`` and ``fund_pp(t - 1, j)`` thereafter.
    """
    if t >= t_ann():
        return 0.0
    if timing == "BEF_PREM":
        return 0.0 if t == 0 else fund_pp(t - 1, j)
    if timing == "BEF_DEDUCT":
        return fund_pp_at(t, j, "BEF_PREM") + prem_to_av_pp(t) * fund_alloc(j)
    if timing == "AFT_DEDUCT":
        total = av_pp_at(t, "BEF_DEDUCT")
        out = mth_deduct_pp(t) + wd_pp(t)
        if total <= 0.0:
            return fund_pp_at(t, j, "BEF_DEDUCT")
        share = fund_pp_at(t, j, "BEF_DEDUCT") / total
        return fund_pp_at(t, j, "BEF_DEDUCT") - out * share
    if timing == "AFT_DERISK":
        total = av_pp_at(t, "AFT_DEDUCT")
        bond = sum(fund_pp_at(t, k, "AFT_DEDUCT")
                   for k in fund_ids() if fund_is_bond(k))
        target = derisk_bond_target * total                          # noqa: F821
        if derisk_amount_pp(t) <= 0.0:
            return fund_pp_at(t, j, "AFT_DEDUCT")
        if fund_is_bond(j):
            return fund_pp_at(t, j, "AFT_DEDUCT") + derisk_amount_pp(t) * (
                fund_pp_at(t, j, "AFT_DEDUCT") / bond if bond > 0.0
                else 1.0 / len([k for k in fund_ids() if fund_is_bond(k)]))
        risky = total - bond
        if risky <= 0.0:
            return fund_pp_at(t, j, "AFT_DEDUCT")
        return fund_pp_at(t, j, "AFT_DEDUCT") * (
            1.0 - derisk_amount_pp(t) / risky)
    raise ValueError("unknown timing %r" % timing)


def derisk_amount_pp(t):
    """The amount moved into the 채권형 by the mandatory pre-annuitisation de-risking.

    「「연금지급개시일 − 3년」시점부터 매년 연계약해당일에 … 채권형 … 계약자적립액의
    합계가 펀드 전체 계약자적립액의 80% 미만인 경우 … 자동 조정됩니다」 [S1]. Applied at
    the three annual 계약해당일 inside the window, after the 월공제액 and before the
    month's growth **[std]**. Unlike 펀드자동재배분 and 펀드자동전환옵션, which the base
    run leaves off because a single deterministic path cannot distinguish them from a
    different fixed allocation, this one is **not optional and is on**.
    """
    if t >= t_ann() or t % 12 != 0 or t == 0:   # a 계약해당일, not the 계약일 itself
        return 0.0
    if not (0 < t_ann() - t <= 12 * derisk_lead_years):              # noqa: F821
        return 0.0
    total = av_pp_at(t, "AFT_DEDUCT")
    bond = sum(fund_pp_at(t, k, "AFT_DEDUCT")
               for k in fund_ids() if fund_is_bond(k))
    return max(0.0, derisk_bond_target * total - bond)               # noqa: F821


def fund_pp(t, j):
    """The balance of fund ``j`` at the **end** of month ``t``, per contract.

    ``AFT_DERISK`` grown by :func:`fund_growth`, which carries the gross asset return and
    the 운용보수 together, the fee being deducted inside the 기준가격 [S7 제43조제2호].
    Zero from ``t_ann()``, the 특별계정 having been emptied into the 일반계정 [S6].
    """
    if t >= t_ann():
        return 0.0
    return fund_pp_at(t, j, "AFT_DERISK") * fund_growth(j)


def av_pp_at(t, timing):
    """계약자적립액 inside month ``t``, per contract: the funds summed at ``timing``."""
    return sum(fund_pp_at(t, j, timing) for j in fund_ids())


def av_pp(t):
    """계약자적립액 (*gyeyakja jeongnibaek*) at the **end** of month ``t``, per contract.

    「납입보험료에서 월공제액 및 인출금액 등을 공제한 금액을 특별계정의 운용실적을
    반영하여 계산한 금액」, which 「특별계정의 평가 등에 따라 매일 변동할 수 있습니다」
    [S7 제2조] [S4] [S5]. On the monthly grid::

        AV(t) = [ AV(t-1) + P_sa(t) - D(t) - W(t) ] x (1+i)^(1/12) x (1 - f/12)

    fund by fund. The exact form sits in the **산출방법서**, a filed 기초서류 that is not
    public [REG-R18 제7-64조], so this recursion is a **[std]** construction consistent
    with, and not derived from, the retrieved documents — and that limit applies equally
    to the surrender value and the annuity amount. It is the hard boundary on how far a
    public-source reconstruction of a Korean variable annuity can go.
    """
    if t >= t_ann():
        return 0.0
    return sum(fund_pp(t, j) for j in fund_ids())


def bond_weight(t):
    """The 채권형 share of the 계약자적립액 at the end of month ``t``.

    Compared against :func:`bond_floor` by :func:`check_bond_floor`. With no rebalancing
    it drifts, and on the shipped scenarios it drifts **upwards**, the 채권형 carrying
    the lower 운용보수 on the same gross asset return.
    """
    if t >= t_ann() or av_pp(t) <= 0.0:
        return 1.0
    return sum(fund_pp(t, j) for j in fund_ids() if fund_is_bond(j)) / av_pp(t)


def inv_income_pp(t):
    """Gross separate-account investment return credited over month ``t``, per contract.

    Before the 운용보수. Not a liability cash flow and not a column of
    :func:`result_cf`: it is the asset-side quantity the account roll-forward needs, and
    this library projects gross liability cash flows only.
    """
    if t >= t_ann():
        return 0.0
    return sum(fund_pp_at(t, j, "AFT_DERISK")
               * ((1.0 + gross_return(j)) ** (1.0 / 12.0) - 1.0)
               for j in fund_ids())


def mgmt_fee_pp(t):
    """특별계정 운용보수 taken over month ``t``, per contract — 0.50% a year blended.

    Taken out of net assets before the 기준가격 is struck [S7 제43조제2호] and transferred
    to the 일반계정 [REG-R15 제5-7조], so it is insurer income even though the
    policyholder never sees a deduction: the unit price is simply lower. Note that the
    disclosed 투자수익률 is already net of it — [S6]'s illustration shows a gross-to-net
    gap of 0.01pp on a product with no guarantee charge, far too small to contain a
    management fee, while [S1]'s gap of 0.32pp is exactly its two account-based guarantee
    charges.
    """
    if t >= t_ann():
        return 0.0
    return sum(fund_pp_at(t, j, "AFT_DERISK")
               * (1.0 + gross_return(j)) ** (1.0 / 12.0)
               * fund_mgmt_fee(j) / 12.0
               for j in fund_ids())


def fund_expense_pp(t):
    """증권거래비용 and 기초펀드 보수·비용, **nil in the base run** [std].

    Borne directly by separate-account assets under 자본시장법 제188조 [S7 제44조] and
    paid to third parties rather than to the insurer, which is why it is a cash flow of
    its own rather than a charge. Both lines are **ex-post estimates of actual spend**
    and not contractual rates — [S2] states its figures are estimated from FY2023 — so
    setting them to zero keeps the modelled charges contractual. Observed 0.00%–0.79%
    and 0.01%–0.45% [S2] [S4]: the omission understates the drag by up to about half a
    percentage point a year.
    """
    if t >= t_ann():
        return 0.0
    return charge_rate("fund_expense") / 12.0 * av_pp_at(t, "AFT_DERISK")


def prem_paid_pp(t):
    """이미 납입한 보험료 at the end of month ``t`` — the strike of **both** guarantees.

    기본보험료 plus 추가납입보험료 actually paid, excluding 특약보험료 [S1] [S4]
    [S7 제2조], reduced **proportionally** by any 중도인출 [S2] [S7 제51조제8항]::

        이미 납입한 보험료 (after) = (before)
            x (중도인출 전 계약자적립액 − 중도인출금액) ÷ (중도인출 전 계약자적립액)

    Without that adjustment a policyholder could withdraw the fund and keep the strike,
    and [R1] is explicit that it is a guarantee-risk mitigant rather than a convenience:
    「중도인출금은 최저보증한도에서 차감된다」.

    The strike opens at nil in month 0, the 계약일 premium being ``prem_pp(0)``.
    """
    base = (prem_paid_pp(t - 1) if t > 0 else 0.0) + prem_pp(t)
    if wd_pp(t) <= 0.0:
        return base
    av_bef = av_pp_at(t, "BEF_DEDUCT") - mth_deduct_pp(t)
    if av_bef <= 0.0:
        return base
    return base * (av_bef - wd_pp(t)) / av_bef


def db_pp(t):
    """사망보험금 payable on a death in month ``t``, per contract, 연금개시 전.

    ``Max(계약자적립액, 이미 납입한 보험료)`` — the account value with premiums paid as a
    floor and **no 기본사망보험금 at all** on the representative design [S1] [S4] [S10]
    [R2]. The GMDB ceases at 연금개시, 「일반적으로 연금개시 후 보장은 소멸됨」 [R2], so
    this is zero from ``t_ann()``.
    """
    if t >= t_ann():
        return 0.0
    return max(av_pp(t), prem_paid_pp(t))


def gmdb_claim_pp(t):
    """The GMDB guarantee claim per death: ``max(0, 이미 납입한 보험료 − 계약자적립액)``.

    The insurer's own cost, met **out of the 일반계정** 보증준비금 rather than out of the
    fund [R2]. On this path it is a real expected cash flow, the mortality decrement
    being a probability applied to a deterministic account value; across paths it is the
    intrinsic value of a strip of puts and a lower bound on their expected cost.
    """
    if t >= t_ann():
        return 0.0
    return max(0.0, prem_paid_pp(t) - av_pp(t))


def surr_chg_cap_pp():
    """표준해약공제액 — the statutory ceiling on the surrender charge, 별표 14 [REG-R20].

    ``5% x 연납순보험료 x 해약공제계수``, the coefficient being the 납입기간 capped at 12
    and the 연납순보험료 excluding the level-spread 부가보험료 [REG-R19 제7-66조제1항제3호]
    [REG-R20]. **₩1,643,940 on the anchor cell**, against which the representative
    ₩830,000 is 50.5%. Note 6 to 별표 14 further requires the acquisition cost loaded onto
    the premium to be discounted at the 평균공시이율 and subtracted from the cap; no
    retrieved document works that netting and the exact residual cap is **[unverified]**
    [REG-R21], so the model applies the gross cap and it binds on three shipped points.
    """
    return (charge_rate("surr_charge_cap") * prem_ann_pp()
            * (1.0 - loading_rate()) * min(pay_term(), 12))


def surr_chg_pp(t):
    """해약공제액 (*haeyak gongjeaek*) applying to a surrender at the end of month ``t``.

    ``C x (n − k) ÷ n`` in completed whole years ``k``, nil from ``n``, with ``n`` the
    해약공제기간 — the 납입기간 capped at **seven years**, which is statutory
    [REG-R19 제7-66조제1항제2호]. The run-off is linear in the **amount**, not in the
    ratio: all three retrieved scales fit that function exactly [S2] [S4] [S5], and the
    published ratio falls far faster only because its denominator is growing. ``C`` is
    [S2]'s ₩830,000 on the anchor cell, capped at :func:`surr_chg_cap_pp`.

    The charge **is** the unamortised 계약체결비용 [R2], which is why the composite takes
    its acquisition cost and its surrender charge from one carrier: pairing [S2]'s 5.17%
    with [S5]'s ₩1,077,000 would recover more on surrender than was ever loaded.
    """
    if t >= t_ann():
        return 0.0
    n = min(pay_term(), surr_chg_years)                              # noqa: F821
    k = yrs_completed(t)
    if k >= n:
        return 0.0
    level = min(charge_rate("surr_charge") * prem_ann_pp(), surr_chg_cap_pp())
    return level * (n - k) / n


def cv_pp(t):
    """해약환급금 (*haeyak hwanreupgeum*) on a surrender at the end of month ``t``.

    ``max(0, 계약자적립액 − 해약공제액)``, the zero floor being statutory — 「계약자적립액
    에서 해약공제액을 공제한 금액이 음(陰)의 값인 경우에는 이를 영(零)으로 처리한다」
    [REG-R19 제7-66조제1항제1호]. **There is no guarantee on it at any duration**
    [S1] [S6] [S7 제50조제3항] [S8] [S10], and on the representative scale it is zero for
    roughly the first four months. 변액보험 is also barred from the 무해지/저해지환급형
    forms by 제7-66조제4항제1호 [REG-R19], so the cliff-shaped curve that dominates this
    library's protection products cannot appear here.
    """
    if t >= t_ann():
        return 0.0
    return max(0.0, av_pp(t) - surr_chg_pp(t))


def av_ann_pp():
    """계약자적립액 at the 연금개시나이 계약해당일, per contract: ``av_pp(t_ann() - 1)``."""
    return av_pp(t_ann() - 1)


def gmab_base_pp():
    """``K(T)``, the 최저연금적립금 strike: 이미 납입한 보험료 at annuitisation.

    Premium refund at **100%**, the textbook identity 「연금개시시 계약자적립금(최저보증
    포함) = Max(기납입보험료, 연금개시시 계약자적립금)」 [R2] and the level of the only
    retrieved charged-GMAB contract [S1]. Three other rules are in the market — step-up,
    ratchet and roll-up — and [R1]'s fifteen-year worked comparison shows that **the
    guarantee design, not the guarantee level, drives the option cost**; they are
    specified in ``product-spec.md`` and not run.
    """
    return prem_paid_pp(t_ann() - 1)


def gmab_claim_pp():
    """``max(0, K(T) − AV(T))`` — the GMAB payoff per contract reaching annuitisation.

    A **European option struck on one date**. It is not payable on surrender, not payable
    on death before annuitisation and forfeited on 조기연금개시 [S1] [S6]
    [S7 제50조제3항] [S8] [S10] [R1] — 「만기 전에 사망 또는 해약이 발생하는 경우 이
    보증은 성립하지 않으며」 — so it is weighted by :func:`pols_annuitised`, which carries
    every decrement that occurred before ``T``.

    On one path this is the option's intrinsic value at maturity and **not its value**:
    zero on the base and high scenarios, positive on the low one. Read it with the model
    docstring's warning beside it.
    """
    if gmab_flag() == 0:
        return 0.0
    return max(0.0, gmab_base_pp() - av_ann_pp())


def annuity_fund_pp():
    """연금재원 per contract: the 계약자적립액 at ``T``, floored at the GMAB.

    Transferred **from the 특별계정 to the 일반계정** — 「연금개시시점부터 계약자적립액
    모두에 대하여 특별계정에서 일반계정으로 자동전환하여 공시이율로 운용합니다」 [S6] —
    with the guarantee top-up added from the 일반계정 보증준비금.
    """
    return av_ann_pp() + gmab_claim_pp()


def decl_rate(k):
    """공시이율 declared in the ``k``-th completed year of the 연금수령기간.

    Re-declared monthly off a published 공시기준이율 [REG-R18] [REG-R24]; the base run
    holds it at the 2026 평균공시이율 of 2.50% [REG-R48] **[std]**.
    """
    tbl = data.crediting_table()                                     # noqa: F821
    rows = tbl[(tbl["basis"] == crediting_basis()) & (tbl["dur_from"] <= k)]
    return float(rows.iloc[-1]["decl_rate"])


def min_guar_rate(k):
    """최저보증이율 in the ``k``-th completed year: 1.00% / 0.75% / 0.50% [S1]."""
    tbl = data.crediting_table()                                     # noqa: F821
    rows = tbl[(tbl["basis"] == crediting_basis()) & (tbl["dur_from"] <= k)]
    return float(rows.iloc[-1]["min_guar_rate"])


def credit_rate(k):
    """``Max[공시이율, 최저보증이율]`` in the ``k``-th completed year of the payout phase."""
    return max(decl_rate(k), min_guar_rate(k))


def annuity_int_rate():
    """The interest rate the annuity is struck at: :func:`credit_rate` at duration 0.

    「연금사망률 및 공시이율을 적용하여 산출방법서에 따라」 [S1] [S2] [S5], the rates in
    force **at annuitisation**. The contract then moves the annuity with the 공시이율 as
    it is re-declared [S5]; this model holds it **level** **[std]** and says so.
    """
    return credit_rate(0)


def ann_mort_rate_at_age(x):
    """연금사망률 at 보험나이 ``x`` — the annuitant basis, from ``data.mort_table()``.

    A **[std]** Makeham curve fitted so its complete expectation of life at 65 **rounds
    to** the 제10회 경험생명표 65세 기대여명, 23.7 years male and 27.1 female [REG-R33];
    the fitted values are 23.663 and 27.060. The
    실제 table is not published [REG-R34]. The contract lets the insurer re-strike this
    basis at annuitisation but **only in the policyholder's favour** [S1] [S2] [S5];
    that one-way ratchet is not modelled.
    """
    return float(data.mort_table().at[(sex(), x), "ann_mort_rate"])  # noqa: F821


def mort_rate_at_age(x):
    """보험사망률 at 보험나이 ``x`` — the insurance basis, from ``data.mort_table()``.

    The :func:`ann_mort_rate_at_age` curve at ``mu / 0.80`` **[std]**: Korea prices
    annuities on a separate and lighter 연금생명표, and neither table is public
    [REG-R34]. This is the basis of the death decrement and therefore of the GMDB cost.
    """
    return float(data.mort_table().at[(sex(), x), "mort_rate"])      # noqa: F821


def mort_rate(t):
    """The annual death rate applying in month ``t``, on the basis then in force.

    보험사망률 through the 연금개시 전 보험기간, 연금사망률 afterwards: the two periods are
    priced on different tables in Korea and the model does not pretend otherwise.
    """
    if t < t_ann():
        return mort_rate_at_age(age(t))
    return ann_mort_rate_at_age(age(t))


def mort_rate_mth(t):
    """The monthly death rate in month ``t``: ``1 - (1 - mort_rate(t)) ** (1/12)``.

    A uniform-force split of the annual rate **[std]**.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate(t):
    """The **annual** 해지율 in the policy year containing month ``t``.

    Zero from ``t_ann()``: the representative payout form is a 종신연금형 and no
    retrieved document allows a surrender of it **[std]**. The scale is calibrated so
    the seven-year persistency is 28.9%, against the only published Korean figure for
    this product — 「변액보험의 7년 평균 유지율은 30% 미만으로 알려져 있다」, second-hand
    inside [R1] and reported from a 2016 금융감독원 release that was not retrieved.

    **Lapse here is static and exogenous, and it is neither in reality.** [R1] states the
    market and reserving convention plainly — 「동적해지율이란 최저보증 발생률(In-the-
    moneyness)에 따라 해지율을 달리 적용하는 방법으로 … 최저보증 발생률이 높을수록
    해지율을 감소시키고」 — but **no retrieved document publishes a functional form or a
    single parameter**, so any dynamic-lapse formula here would be a [std] construction
    and the base run does not attempt one.
    """
    if t >= t_ann():
        return 0.0
    tbl = data.lapse_table()                                         # noqa: F821
    rows = tbl[tbl["dur_from"] <= policy_year(t)]
    return float(rows.iloc[-1]["lapse_rate"])


def lapse_rate_mth(t):
    """The monthly 해지율 in month ``t``: ``1 - (1 - lapse_rate(t)) ** (1/12)``."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """Contracts in force at the **start** of month ``t``.

    ``pols_if(0) = pols_if_init()``, and this is the weight carried by every cash flow on
    the same ``result_cf()`` row, so the exposure column and the cash flows beside it
    reconcile. It is a genuine policy count on both sides of annuitisation — contracts
    before ``t_ann()``, living annuitants after it. The end-of-month count is
    ``pols_if_at(t, "AFT_DECR")``.
    """
    if t == 0:
        return pols_if_init()
    return (pols_if(t - 1) - pols_death(t - 1)
            - pols_lapse(t - 1) - pols_maturity(t - 1))


def pols_death(t):
    """Expected deaths during month ``t``, taken **first** among the decrements [std]."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Expected 해지 during month ``t``, taken on the survivors of the month's deaths."""
    return (pols_if(t) - pols_death(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Survivors carried out at the horizon, so the roll-forward closes.

    A 종신연금형 has no maturity and pays nothing here: the projection stops at attained
    age ``omega_age`` and this cells makes the truncation visible rather than absorbing
    it into the last row's decrements. Non-zero only in the last row,
    ``t = proj_len() - 1``.
    """
    if t == proj_len() - 1:
        return pols_if(t) - pols_death(t) - pols_lapse(t)
    return 0.0


def pols_if_at(t, timing):
    """The in-force count inside month ``t``: ``BEF_DECR`` / ``BEF_LAPSE`` / ``AFT_DECR``."""
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) - pols_death(t)
    if timing == "AFT_DECR":
        return pols_if(t) - pols_death(t) - pols_lapse(t) - pols_maturity(t)
    raise ValueError("unknown timing %r" % timing)


def pols_annuitised():
    """The count reaching the 연금개시나이 계약해당일, ``pols_if(t_ann())``.

    This is the indicator the GMAB payoff is weighted by, and it carries **every**
    decrement — mortality *and* lapse — that occurred before ``T``.
    """
    return pols_if(t_ann())


def is_annuity_month(t):
    """True in a month an annuity instalment falls due: ``T``, ``T+12``, ``T+24``, ...

    The annuity is paid **annually in advance** on the 연금개시 계약해당일 **[std]**,
    which is the granularity the 연금 연액 and the 0.5% 연금수령기간 중 계약관리비용 are
    published on [S4].
    """
    return t >= t_ann() and (t - t_ann()) % 12 == 0


def pols_annuity_oblig(t):
    """The count an instalment is owed to in month ``t``.

    Inside the 10-year 보증기간 that is every contract that annuitised, whether the
    annuitant is alive or not: 「사망하더라도 남은 보증기간의 연금은 지급됩니다」, the
    remaining instalments falling due on their dates or commutable at the 공시이율
    [S2] [S5]. After it, the survivors only — 「보증기간 후 사망시 계약은 소멸」 [S1] [S5].
    The step down at the end of the 보증기간 is real and is visible in the output.
    """
    if not is_annuity_month(t):
        return 0.0
    if t - t_ann() < 12 * guar_period_years:                         # noqa: F821
        return pols_annuitised()
    return pols_if(t)


def ann_surv(k):
    """``k p_y`` — survival from 연금개시나이 to ``k`` years later, on the 연금사망률."""
    if k <= 0:
        return 1.0
    return ann_surv(k - 1) * (1.0 - ann_mort_rate_at_age(annuity_age() + k - 1))


def annuity_factor():
    """The 종신연금형 10년 보증기간부 annuity-due factor at :func:`annuity_int_rate`.

    ``sum(v**k for k in 0..9) + sum(v**k * k_p_y for k in 10..omega)``: the first ten
    instalments are certain and the rest life-contingent. The menu is uniform across
    carriers — 보증기간 of 10 / 15 / 20 years, to age 100, or 기대여명보증, in 정액형 or
    체증형 [S1] [S2] [S5] — and the composite takes the ten-year level form because it is
    the modal election, the only one exercising both longevity and a guarantee period,
    and the form the 소득세법 종신형 연금보험 route is written around, that route
    requiring the guarantee period to sit within the published 기대여명 연수 [REG-R58].
    The sum is truncated at ``omega_age`` for consistency with the projection horizon.
    """
    v = 1.0 / (1.0 + annuity_int_rate())
    last = omega_age - annuity_age() - 1                             # noqa: F821
    total = 0.0
    for k in range(0, last + 1):
        if k < guar_period_years:                                    # noqa: F821
            total = total + v ** k
        else:
            total = total + v ** k * ann_surv(k)
    return total


def annuity_ann_pp():
    """연금 연액 (*yeongeum yeonaek*), gross: ``annuity_fund_pp() / annuity_factor()``."""
    return annuity_fund_pp() / annuity_factor()


def annuity_charge_pp():
    """연금수령기간 중 계약관리비용: **연금 연액의 0.5%**, netted off each payment [S4].

    Two forms are published — this proportional one [S4] and 구좌당 매월 min(영업보험료의
    3.5%, ₩4,000) [S2]. The composite takes the proportional form **[std]** because it is
    scale-free and needs no reference to a premium that has stopped being paid.
    """
    return charge_rate("annuity_charge") * annuity_ann_pp()


def annuity_net_pp():
    """The annuity instalment actually paid, 연금 연액 net of the payout-phase charge."""
    return annuity_ann_pp() - annuity_charge_pp()


def premiums(t):
    """영업보험료 received in month ``t``: 기본보험료 plus 추가납입보험료, in force weighted.

    Received into the **일반계정**, out of which the front-end charges are retained and
    the remainder transferred to the 특별계정 [S7 제2조] [R2].
    """
    return prem_pp(t) * pols_if(t)


def claim_pp(t, kind):
    """Benefit per contract for one ``kind``: ``DEATH``, ``LAPSE``, ``ANNUITY``, ``MATURITY``."""
    if kind == "DEATH":
        return db_pp(t)
    if kind == "LAPSE":
        return cv_pp(t)
    if kind == "ANNUITY":
        return annuity_net_pp() if is_annuity_month(t) else 0.0
    if kind == "MATURITY":
        return 0.0
    raise ValueError("unknown kind %r" % kind)


def pols_decr(t, kind):
    """The count a benefit of ``kind`` is paid on in month ``t``."""
    if kind == "DEATH":
        return pols_death(t)
    if kind == "LAPSE":
        return pols_lapse(t)
    if kind == "ANNUITY":
        return pols_annuity_oblig(t)
    if kind == "MATURITY":
        return pols_maturity(t)
    raise ValueError("unknown kind %r" % kind)


def claims(t, kind=None):
    """Benefit outgo in month ``t``, for one ``kind`` or, with ``kind=None``, all four.

    ``DEATH`` is the 사망보험금 including its GMDB top-up; ``LAPSE`` the 해약환급금;
    ``ANNUITY`` the instalment net of the payout-phase charge; ``MATURITY`` is
    structurally nil, a 종신연금형 paying nothing at the horizon. The **column** ``claims``
    is deliberately absent from :func:`result_cf`, which publishes the split lines so that
    they sum to :func:`net_cf`.
    """
    if kind is None:
        return (claims(t, "DEATH") + claims(t, "LAPSE")
                + claims(t, "ANNUITY") + claims(t, "MATURITY"))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The part of a benefit of ``kind`` released **out of the 특별계정** in month ``t``.

    On death that is the 계약자적립액 alone, the guarantee top-up coming from the
    일반계정 보증준비금 [R2]; on a 해지 it is the whole account value, of which the
    policyholder receives the 해약환급금 and the insurer retains the 해약공제액.
    """
    if kind in ("DEATH", "LAPSE"):
        return av_pp(t) * pols_decr(t, kind)
    return 0.0


def withdrawals(t):
    """중도인출금 paid to the policyholder in month ``t``, out of the 특별계정."""
    return wd_pp(t) * pols_if(t)


def fund_expenses(t):
    """증권거래비용 and 기초펀드 보수 borne by separate-account assets — nil [std]."""
    return fund_expense_pp(t) * pols_if(t)


def expenses(t):
    """The insurer's **own** expenses in month ``t`` — not the charges it collects.

    ₩300,000 per contract at issue and ₩3,000 per contract per month thereafter,
    both **[std]** and both held level with no inflation [std]. No Korean carrier
    publishes a unit cost: the 사업비 disclosure is of *charges*, not of costs [R2] [S12],
    so the acquisition and maintenance charges above are sourced and these are not.
    """
    unit = charge_rate("expense_maint")
    if t == 0:
        unit = unit + charge_rate("expense_acq")
    return unit * pols_if(t)


def comm_rate(y):
    """모집수수료율 in policy year ``y``, a fraction of 보험료총액; nil after year five.

    1.34% / 0.41% / 0.28% / 0.25% / 0.11%, the 2017 census **mean** for a 월납 변액연금
    [R1 <표 Ⅴ-3>]. The five sum to 2.39% of the premiums the policyholder will pay, against
    the mean *total* of 2.11% the same table reports: a mean of contract totals is not the
    sum of per-year means, and the model runs the per-year scale. The observed
    range is wide — 0.63%–2.38% in year one and 1.10%–3.13% in total — and **channel is a
    first-order parameter**: the one variable annuity [R1] found buyable directly online
    carried no acquisition commission at all, and bancassurance and online 계약체결비용
    were capped at 50% of the tied-agent level from 2016. The composite is a
    전속설계사 contract **[std]** and says so.
    """
    if 1 <= y <= 5:
        return charge_rate("comm_yr%d" % y)
    return 0.0


def commissions(t):
    """모집수수료 paid in month ``t``, one twelfth of the policy year's rate [std]."""
    return comm_rate(policy_year(t)) / 12.0 * prem_total_pp() * pols_if(t)


def prem_to_av(t):
    """특별계정 투입보험료 transferred 일반계정 → 특별계정 in month ``t``, in force weighted.

    One of the transfers 감독규정 제5-7조 permits between the two accounts [REG-R15]. It
    is **internal**: it appears in both account ledgers with opposite signs and cancels
    out of :func:`net_cf`.
    """
    return prem_to_av_pp(t) * pols_if(t)


def av_charges(t):
    """월공제액 and 특별계정 운용보수 transferred 특별계정 → 일반계정 in month ``t``.

    The 월공제액 by cancelling units on the 월계약해당일, the 운용보수 daily inside the
    기준가격 [S7 제2조] [S7 제43조제2호]; both are 「위험보장에 필요한 금액」 and
    「사업비」 transfers under 감독규정 제5-7조 [REG-R15], and the two guarantee components
    of the 월공제액 are held in the 일반계정 as 보증준비금 [R2]. Internal.
    """
    return (mth_deduct_pp(t) + mgmt_fee_pp(t)) * pols_if(t)


def surr_charges(t):
    """해약공제액 retained by the insurer on the month's 해지, 특별계정 → 일반계정.

    ``min(해약공제액, 계약자적립액)``, the statutory zero floor on the 해약환급금 meaning
    the insurer never recovers more than the account holds [REG-R19]. Internal.
    """
    return min(surr_chg_pp(t), max(0.0, av_pp(t))) * pols_lapse(t)


def av_transfer(t):
    """연금재원 moved 특별계정 → 일반계정 at ``t_ann()``, in force weighted.

    「연금개시시점부터 계약자적립액 모두에 대하여 특별계정에서 일반계정으로 자동전환하여
    공시이율로 운용합니다」 [S6]. The account-value part only: the GMAB top-up beside it is
    a movement **within** the 일반계정, from the 보증준비금 to the 연금재원, and so appears
    in neither ledger. Internal.
    """
    if t != t_ann():
        return 0.0
    return av_pp(t - 1) * pols_if(t)


def prem_charges(t):
    """계약체결비용, 납입 중 계약관리비용 and 기타비용 retained in the 일반계정 — a memo.

    Never a transfer: this money reaches the 일반계정 with the premium and simply does not
    leave it [S7 제2조].
    """
    return prem_charge_pp(t) * pols_if(t)


def annuity_charges(t):
    """연금수령기간 중 계약관리비용 retained in month ``t`` — a memo.

    Netted off the instalment [S4], so it never leaves the 일반계정 and appears in no
    ledger; :func:`claims` already carries the payment net of it.
    """
    if not is_annuity_month(t):
        return 0.0
    return annuity_charge_pp() * pols_annuity_oblig(t)


def gmdb_charges(t):
    """최저사망보험금 보증비용 collected in month ``t`` — a memo on the guarantee."""
    return gmdb_charge_pp(t) * pols_if(t)


def gmab_charges(t):
    """최저연금적립금 보증비용 collected in month ``t`` — a memo on the guarantee.

    Compare it with :func:`gmab_claims`, and read the difference as what it is: **a
    single-path residual, not a profit**. On the base scenario the GMAB finishes out of
    the money and the whole charge is collected against an intrinsic cost of zero.
    """
    return gmab_charge_pp(t) * pols_if(t)


def gmdb_claims(t):
    """The GMDB strain on the 일반계정 in month ``t``: top-up times deaths."""
    return gmdb_claim_pp(t) * pols_death(t)


def gmab_claims(t):
    """The GMAB strain at ``t_ann()``: intrinsic payoff times the count annuitising.

    A movement inside the 일반계정 — 보증준비금 to 연금재원 — so it does not appear in
    :func:`net_cf`. Its cash-flow consequence is a **larger annuity for the rest of the
    projection**, which is where a reader should look for it.
    """
    if t != t_ann():
        return 0.0
    return gmab_claim_pp() * pols_annuitised()


def charge_income(t):
    """Every charge line collected in month ``t``, summed — a memo, never a ledger line.

    계약체결비용 + 계약관리비용 + 위험보험료 + 두 보증비용 + 특별계정 운용보수 +
    해약공제액 + 연금수령기간 중 계약관리비용. It is a memo because most of it is an
    **internal transfer** rather than an external cash flow: adding it to
    :func:`premiums` would count the same money twice.
    """
    return (prem_charges(t) + av_charges(t) + surr_charges(t)
            + annuity_charges(t))


def net_cf(t):
    """Net cash flow in month ``t``, **income positive**: income less outgo.

    The **whole-contract external** cash flow — what crosses the boundary of the insurer,
    on either side of the 특별계정 / 일반계정 line::

        premiums − 사망보험금 − 해약환급금 − 연금 − 중도인출금
                 − 특별계정 third-party costs − expenses − commissions

    Every internal transfer is absent by construction, which is what makes the columns of
    :func:`result_cf` sum to this line. Investment return is absent too: this library
    projects **gross liability cash flows** and leaves the asset side, discounting, the
    책임준비금, the IFRS 17 CSM and the K-ICS 요구자본 to a separate layer that consumes
    them. :func:`net_cf_gen` and :func:`net_cf_sep` decompose this line by account and
    :func:`check_net_cf` asserts that they add back to it.
    """
    return (premiums(t) - claims(t) - withdrawals(t) - fund_expenses(t)
            - expenses(t) - commissions(t))


def net_cf_sep(t):
    """The **특별계정** ledger in month ``t``, income positive.

    In: the 특별계정 투입보험료. Out: the 월공제액 and 운용보수 transferred to the
    일반계정, the 해약공제액 retained there, the 계약자적립액 released on a death or a
    해지, the 중도인출금, the 연금재원 moved at 연금개시, and the third-party costs borne
    directly by separate-account assets under 자본시장법 제188조 [S7 제44조]. Investment
    return is excluded, as in :func:`net_cf`.
    """
    return (prem_to_av(t) - av_charges(t) - surr_charges(t)
            - claims_from_av(t, "DEATH") - claims(t, "LAPSE")
            - withdrawals(t) - av_transfer(t) - fund_expenses(t))


def net_cf_gen(t):
    """The **일반계정** ledger in month ``t``, income positive.

    In: the whole 영업보험료, the transfers received from the 특별계정, and the 연금재원 at
    연금개시. Out: the 특별계정 투입보험료 transferred away, the GMDB top-up met from the
    보증준비금, the annuity instalments, and the insurer's own expenses and commission.
    The GMAB top-up does not appear: it is a movement **within** this account.
    """
    return (premiums(t) + av_charges(t) + surr_charges(t) + av_transfer(t)
            - prem_to_av(t) - gmdb_claims(t) - claims(t, "ANNUITY")
            - claims(t, "MATURITY") - expenses(t) - commissions(t))


def check_net_cf_resid(t):
    """Residual of the account-boundary identity in month ``t``; zero to floating point.

    ``net_cf(t) − net_cf_gen(t) − net_cf_sep(t)``. Every transfer 감독규정 제5-7조 permits
    between the two accounts [REG-R15] appears in the two ledgers with opposite signs, so
    their sum must be the whole-contract external cash flow and nothing else. This is the
    identity a 변액연금보험 has to cross the 특별계정 / 일반계정 boundary to state, and a
    model that cannot state it has not represented the boundary.
    """
    return net_cf(t) - net_cf_gen(t) - net_cf_sep(t)


def check_net_cf():
    """True when the cash flow statement reconciles at **every** projected month.

    No argument and a ``bool`` return; :func:`check_net_cf_resid` is the signed per-month
    residual. The tolerance is relative to the size of the month's gross flows, cash
    flows on this product running to eight figures in KRW.
    """
    return all(abs(check_net_cf_resid(t))
               <= val_tol * max(1.0, abs(net_cf_gen(t)) + abs(net_cf_sep(t)))  # noqa: F821
               for t in range(0, proj_len()))


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual in month ``t``; zero to floating point.

    ``pols_if(t) − pols_if(t+1) = deaths + 해지 + horizon survivors``, written on the
    start-of-month counts :func:`pols_if` carries. In the horizon month ``pols_if(t+1)``
    is zero and :func:`pols_maturity` absorbs the survivors.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes at **every** projected month.

    No argument and a ``bool`` return; :func:`check_pols_roll_fwd_resid` is the signed
    per-month residual. In force is a probability of order 1, so the tolerance is
    ``roll_fwd_tol``.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) < roll_fwd_tol      # noqa: F821
               for t in range(0, proj_len()))


def check_av_roll_fwd_resid(t):
    """계약자적립액 roll-forward residual in month ``t``, per contract.

    ``AV(t) − AV(t−1) = 특별계정 투입보험료 − 월공제액 − 중도인출금 + gross investment
    return − 특별계정 운용보수 − the 연금재원 transferred at 연금개시``. The mandatory
    de-risking does not appear because it conserves the total; it moves money between
    funds, not out of the account.

    Defined on **every** month of the frame including ``t = 0``, whose opening balance is
    nil: the first row carries the single premium, the 계약체결비용 and the whole first
    month's charge stack, and the identity closes on it.
    """
    opening = av_pp(t - 1) if t > 0 else 0.0
    transfer = opening if t == t_ann() else 0.0
    expected = (opening + prem_to_av_pp(t) - mth_deduct_pp(t) - wd_pp(t)
                + inv_income_pp(t) - mgmt_fee_pp(t) - transfer)
    return av_pp(t) - expected


def check_av_roll_fwd():
    """True when the account recursion closes at **every** projected month.

    No argument and a ``bool`` return; :func:`check_av_roll_fwd_resid` is the signed
    per-month residual, measured per contract on a balance of order 1e7 in KRW, so the
    tolerance is relative.
    """
    return all(abs(check_av_roll_fwd_resid(t))
               <= val_tol * max(1.0, abs(av_pp(t)))                  # noqa: F821
               for t in range(0, proj_len()))


def check_charge_split_resid(t):
    """Residual of the separate-account investment identity in month ``t``, per contract.

    ``gross asset return = 특별계정 운용보수 + the change in the 계약자적립액 from
    investment``. It is the guard against the charge-base confusion this product is most
    often modelled wrong at: the 운용보수 is inside the 기준가격, the 월공제액 cancels
    units, the 계약체결비용 never enters the fund at all, and the premium component of the
    GMAB charge is on a base that is not the fund — four bases in one stack.
    """
    if t >= t_ann():
        return 0.0
    return (inv_income_pp(t) - mgmt_fee_pp(t)
            - (av_pp(t) - av_pp_at(t, "AFT_DERISK")))


def check_charge_split():
    """True when the separate-account investment identity closes at every month."""
    return all(abs(check_charge_split_resid(t))
               <= val_tol * max(1.0, abs(av_pp(t)))                  # noqa: F821
               for t in range(0, proj_len()))


def check_gmdb_floor_resid(t):
    """Residual of the GMDB decomposition in month ``t``, per contract.

    ``사망보험금 = 계약자적립액 + max(0, 이미 납입한 보험료 − 계약자적립액)``, i.e. the
    benefit splits exactly into the part released from the 특별계정 and the part met from
    the 일반계정 보증준비금 [R2]. That split is what makes the two account ledgers add
    back to :func:`net_cf`.
    """
    if t >= t_ann():
        return 0.0
    return db_pp(t) - av_pp(t) - gmdb_claim_pp(t)


def check_gmdb_floor():
    """True when the death benefit splits cleanly into fund and guarantee at every month."""
    return all(abs(check_gmdb_floor_resid(t))
               <= val_tol * max(1.0, abs(db_pp(t)))                  # noqa: F821
               for t in range(0, proj_len()))


def check_bond_floor_resid(t):
    """Shortfall of the 채권형 weight below the mandatory floor in month ``t``; zero when met.

    Negative if the ladder is breached. The floor 「채권형 최저편입비율」 binds both the
    premium allocation and the account mix and survives every later 펀드변경 [S1] [R1],
    and the insurer has a direct financial interest in it beyond the policyholder's: the
    별표 24 보증준비금 standard factor is indexed to 주식비중한도, 「기초서류상 최대
    주식투자 비중을 적용함」, so a lower equity cap is a lower reserve floor [R1] [REG-R26].
    """
    if t >= t_ann():
        return 0.0
    return min(0.0, bond_weight(t) - bond_floor())


def check_bond_floor():
    """True when the 채권형 weight meets the mandatory ladder at every projected month."""
    return all(abs(check_bond_floor_resid(t)) < roll_fwd_tol         # noqa: F821
               for t in range(0, proj_len()))


def check_surr_chg_cap_resid(t):
    """Excess of the 해약공제액 over the 표준해약공제액 in month ``t``; zero when compliant.

    감독규정 제7-66조제1항제3호 requires the 해약공제액 to be the 표준해약공제액 of
    별표 14 [REG-R19] [REG-R20], and 제1항제2호 caps the 해약공제기간 at seven years where
    the 납입기간 is seven years or more. The cap binds on three shipped model points, all
    5년납, whose level charge scaled from the anchor cell would otherwise exceed it.
    """
    if t >= t_ann():
        return 0.0
    return max(0.0, surr_chg_pp(t) - surr_chg_cap_pp())


def check_surr_chg_cap():
    """True when the surrender charge is inside the statutory cap at every month."""
    return all(abs(check_surr_chg_cap_resid(t)) < val_tol            # noqa: F821
               for t in range(0, proj_len()))


def check_prem_alloc_resid(t):
    """Residual of the premium-allocation identity in month ``t``, per contract.

    While both front-end charges run, the 기본보험료 reaching the 특별계정 is exactly
    ``1 − 부가보험료율`` of it — **91.33%** on the composite, inside the 91.3%–91.5% three
    carriers publish on the anchor cell [S1] [S2] [S6] and inside [R1]'s industry band of
    「납입보험료의 5~15%를 … 차감한 후 85~95%만 투자」. 추가납입보험료 is subtracted first,
    because it carries no loading [S1] and so is not part of that ratio.
    """
    if premium_mth_pp(t) <= 0.0:
        return 0.0
    reached = prem_to_av_pp(t) - addl_prem_pp(t)
    expected = basic_prem_pp() * (1.0 - loading_rate())
    if t >= 12 * acq_charge_years:                                   # noqa: F821
        expected = basic_prem_pp() * (
            1.0 - loading_rate() + charge_rate("acq_charge"))
    return reached - expected


def check_prem_alloc():
    """True when the premium allocation matches the published fee stack at every month."""
    return all(abs(check_prem_alloc_resid(t)) < val_tol              # noqa: F821
               for t in range(0, proj_len()))


def result_cf():
    """The cash flow statement: one row per projection month, indexed by ``t``.

    ``pols_if`` opens each row and is the count in force at the **start** of the month,
    so it is the weight carried by every cash flow beside it. The remaining columns are
    the whole-contract external cash flows and they **sum to** ``net_cf``: income less
    outgo, income positive. There is no ``claims`` column — the split lines are published
    instead, so the columns add up without a reader having to know which to skip.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "fund_expenses": [fund_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """In-force movements, indexed by ``t``.

    Rows read across: ``pols_if − pols_death − pols_lapse − pols_maturity`` is the next
    row's ``pols_if``, which is what :func:`check_pols_roll_fwd` asserts.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, "AFT_DECR") for t in ts],
            "pols_annuity_oblig": [pols_annuity_oblig(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """The 계약자적립액 recursion, per contract, indexed by ``t``.

    The columns are the account roll-forward in the order the month applies them, then
    the quantities the guarantees are struck on. Reading a row left to right is reading
    :func:`check_av_roll_fwd_resid`.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_deduct": [av_pp_at(t, "BEF_DEDUCT") for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "mth_deduct_pp": [mth_deduct_pp(t) for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "inv_income_pp": [inv_income_pp(t) for t in ts],
            "mgmt_fee_pp": [mgmt_fee_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "bond_weight": [bond_weight(t) for t in ts],
            "surr_chg_pp": [surr_chg_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "prem_paid_pp": [prem_paid_pp(t) for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "gmdb_claim_pp": [gmdb_claim_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_charges():
    """The 상품요약서 fee stack as separate lines, per contract, indexed by ``t``.

    Five of these are the lines the task of modelling this product turns on, and they are
    separate columns because they are **deducted from different bases at different times
    and land in different accounts**: 계약체결비용 and 납입 중 계약관리비용 out of the
    premium in the 일반계정; 위험보험료, 납입 후 계약관리비용 and both guarantee
    components out of the 계약자적립액 on the 월계약해당일; 특별계정 운용보수 inside the
    기준가격. Collapsing them into one charge is the error the columns exist to prevent.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "acq_charge_pp": [acq_charge_pp(t) for t in ts],
            "maint_charge_in_pp": [maint_charge_in_pp(t) for t in ts],
            "other_charge_pp": [other_charge_pp(t) for t in ts],
            "risk_prem_pp": [risk_prem_pp(t) for t in ts],
            "maint_charge_after_pp": [maint_charge_after_pp(t) for t in ts],
            "gmdb_charge_pp": [gmdb_charge_pp(t) for t in ts],
            "gmab_charge_asset_pp": [gmab_charge_asset_pp(t) for t in ts],
            "gmab_charge_prem_pp": [gmab_charge_prem_pp(t) for t in ts],
            "mgmt_fee_pp": [mgmt_fee_pp(t) for t in ts],
            "fund_expense_pp": [fund_expense_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

acq_charge_years = 10

gmab_charge_years = 7

surr_chg_years = 7

guar_period_years = 10

derisk_lead_years = 3

derisk_bond_target = 0.80

bond_floor_short = 0.80

bond_floor_mid = 0.70

bond_floor_long = 0.50

addl_prem_cap_ratio = 2.0

wd_max_cv_ratio = 0.5

wd_min_residual_pp = 5000000.0

wd_cum_cap_years = 10

roll_fwd_tol = 1e-10

val_tol = 1e-8

pd = ("Module", "pandas")
