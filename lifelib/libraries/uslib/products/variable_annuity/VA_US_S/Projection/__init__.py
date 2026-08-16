# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of :mod:`~.VA_US_S`.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the anchor cell
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/variable_annuity/``, read at run time rather than stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VA_US_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

The readers and the filename References live on the sibling
:mod:`~.VA_US_S.Data` Space, reached here through the ``data`` Reference, so
each file is read once per model rather than once per model point:

=========================  ==============================  ==========================
Reference (on Data)        Cells                           File
=========================  ==============================  ==========================
model_point_file           data.model_point_table()        model_point_table.csv
mort_table_file            data.mort_table()               mort_table.csv
fund_file                  data.fund_table()               fund_table.csv
return_scenario_file       data.return_scenario()          return_scenario.csv
rate_scenario_file         data.rate_scenario()            rate_scenario.csv
gawa_pct_file              data.gawa_pct_table()           gawa_pct_table.csv
cdsc_file                  data.cdsc_table()               cdsc_table.csv
transaction_file           data.transaction_table()        transaction_table.csv
=========================  ==============================  ==========================

.. rubric:: Projection basis

``t`` counts **projection months**, 1-based, with ``t = 0`` the entry instant carrying
the single premium and the initial branch of every recursion. The *policy* month is
``duration_mth(t) = duration_mth_init() + t``: for an at-issue cell the two coincide,
and for an in-force cell — the worked example's carried state is one — ``t = 1`` is
policy month ``duration_mth_init() + 1``. Every calendar test (Contract Anniversary,
Contract Quarterly Anniversary, contract year, attained age) is written on
``duration_mth(t)``, never on ``t``.

``policy_year(t) = ceil(duration_mth(t) / 12)`` is the contract year ``y``,
``contract_quarter(t) = ceil(duration_mth(t) / 3)`` the contract quarter ``k``. Contract
Anniversaries fall at the **end** of months ``duration_mth ≡ 0 (mod 12)`` and Contract
Quarterly Anniversaries at the end of months ``duration_mth ≡ 0 (mod 3)`` **[std]**.
The attained age is ``a(t) = x + y − 1``.

Within a month the technical notes' processing order is followed exactly. At the
beginning of the month (BOM): if the contract is already depleted, run the
post-depletion routine and skip everything else; otherwise take the premium, which buys
units at the prior unit value per ``alloc[i]`` and raises ``GWB``, ``BB``, ``NP``,
``RP``, ``RB``, ``GAWA`` and ``ADJ``; then take the withdrawal, which fixes the GAWA% if
it is the first one, splits into excess and non-excess portions, computes the withdrawal
charge, cancels units pro rata and updates ``GWB``, ``GAWA`` and ``BB``. Then unit values
grow over the month. At the end of the month (EOM): the two rider fees are assessed at a
Contract Quarterly Anniversary and the annual contract fee at a Contract Anniversary,
both by pro-rata unit cancellation; then, at a Contract Anniversary only, the seven
guarantee events in the notes' order — GMDB withdrawal adjustment, GMDB roll-up, GLWB
bonus, step-up, GWB Adjustment Date test, the non-For-Life ``GAWA = GWB`` floor, and the
$10,000,000 cap; then the depletion test; then decrements, **death first, then
surrender** **[std]**.

**Undiscounted.** Like every model in this library, this one projects *gross liability
cash flows* only. Reserves and discounting are a separate layer: the notes' *Valuation
and reserve pointers* section cites VM-21's CTE70 stochastic reserve, C-3 Phase II's
CTE(98), VM-22/VM-V §1 for the post-depletion stream and IRC §807, rather than
reproducing any of them.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and :mod:`.MYGA_US_S` — the deferred
annuity chassis of this library — wherever the two products share a concept:
``pols_*`` for policy counts, ``av_*`` for account values, plural nouns for cash flows,
``*_rate`` for rates, ``*_pp`` for per-contract amounts, ``*_at(t, timing)`` for a
quantity read at a point inside the month. The technical notes use compact actuarial
symbols instead. The mapping is:

===================================================  ===========================================  =============================================
Notes symbol                                         Cells                                        Meaning
===================================================  ===========================================  =============================================
t                                                    duration_mth(t)                              Elapsed policy months
(months elapsed at entry)                            duration_mth_init()                          0 at issue; the in-force cell's own
y = ceil(t/12)                                       policy_year(t)                               Contract year containing month t
y - 1                                                duration(t)                                  Completed contract years
k = ceil(t/3)                                        contract_quarter(t)                          Contract quarter containing month t
x, issue_age                                         age_at_entry                                 Issue age (ANB)
a(t) = x + y - 1                                     age(t)                                       Attained age during month t
(a at the anniversary)                               age_at_anniv(t)                              Attained age just after the anniversary
(none)                                               policy_term                                  Years from issue to omega_age
(none)                                               proj_len                                     Last projection month
av_initial                                           av_pp_init()                                 AV carried into t = 0 (in-force cell)
gwb_initial                                          gwb_pp_init()                                GWB carried into t = 0
bb_initial                                           bb_pp_init()                                 Bonus Base carried into t = 0
rb_initial                                           rb_pp_init()                                 GMDB Benefit Base carried into t = 0
(none)                                               gawa_pp_init()                               GAWA carried into t = 0
(none)                                               gawa_pct_init()                              GAWA% already locked at t = 0
(none)                                               np_pp_init()                                 Cumulative Net Premiums at t = 0
(none)                                               rp_pp_init()                                 Remaining Premium at t = 0
(none)                                               adj_pp_init()                                GWB Adjustment at t = 0
(none)                                               bonus_end_init()                             Contract year the Bonus Period ends, at t = 0
glwb_stepup_basis                                    stepup_basis()                               annual_CV or highest_quarterly_CV
i                                                    sub_ids                                      Subaccount indices
alloc[i]                                             alloc(i)                                     Allocation of net premium to subaccount i
e_i                                                  fund_expense_rate(i)                         Annual fund expense ratio
r_i(t)                                               inv_return_mth(t, i)                         Gross monthly fund return (scenario input)
m, alpha                                             asset_charge_me, asset_charge_admin          M&E and administrative asset charge
(the growth factor)                                  unit_growth(t, i)                            (1+r_i)(1-e_i/12)(1-(m+a)/12)
V_i(t)                                               (inside unit_growth)                         Unit value; see the note below
U_i(t)                                               (implicit)                                   Units; see the note below
SA_i(t)                                              sa_pp(t, i)                                  Subaccount value at end of month t
SA_i at a point in the month sa_pp_at(t, i, timing)  BEF_PREM / BEF_WD / BEF_INV / BEF_FEE / EOM
AV(t)                                                av_pp(t)                                     Contract value at end of month t
AV at a point in the month                           av_pp_at(t, timing)                          Same timings, summed over subaccounts
l x AV(t)                                            av_at(t, timing)                             In-force weighted contract value
w_i(t)                                               sa_weight(t, i)                              Value weight, the pro-rata deduction key
(gross fund return)                                  gross_inv_income_pp(t)                       Return before any charge
(fund's own expense)                                 fund_expense_pp(t)                           Paid to the funds, not insurer revenue
(M&E + admin)                                        asset_charge_pp(t)                           Collected inside the unit value
(net of both)                                        inv_income_pp(t)                             Change in AV from investment over month t
P(t)                                                 premium_pp(t)                                Gross premium at BOM of month t
P(t)(1 - tau)                                        prem_to_av_pp(t)                             Net premium buying units
tau                                                  premium_tax_rate                             Premium tax rate
W(t)                                                 wd_pp(t)                                     Gross withdrawal, inclusive of charges
(W before the AV cap)                                wd_pp_due(t)                                 Withdrawal requested before capping at AV
(scheduled part of W)                                wd_scheduled_pp(t)                           Withdrawal from transaction_table.csv
(utilization part of W)                              wd_glwb_pp(t)                                wd_intensity x L(t) once activated
L(t)                                                 wd_limit_pp(t)                               Annual withdrawal limit max(GAWA, RMD)
SumW_y                                               sum_wd_pp(t)                                 Withdrawals to date in the contract year
E(t)                                                 wd_excess_pp(t)                              Excess portion of W(t)
N(t)                                                 wd_nonexcess_pp(t)                           Non-excess portion of W(t)
CV_pre                                               cv_pre_excess_pp(t)                          AV after N has been deducted
(1 - E/CV_pre)                                       excess_factor(t)                             The pro-rata factor for the excess
(charge-free amount)                                 free_wd_allow(t)                             max(earnings, 10% of RP)
(unused allowance)                                   free_wd_avail(t)                             Allowance left in the contract year
(allowance consumed)                                 wd_free_pp(t)                                Allowance used by month t's withdrawal
(allowance used to date)                             free_wd_used_cum_pp(t)                       Allowance used in the contract year so far
(exempt part of W)                                   wd_exempt_pp(t)                              Portion of W bearing no charge
(chargeable part of W)                               wd_chargeable_pp(t)                          Portion of W bearing the CDSC
c(t)                                                 wd_charge_pp(t)                              CDSC on the withdrawal
W(t) - c(t)                                          wd_payment_pp(t)                             Cash paid on the withdrawal
CDSC scale                                           surr_charge_rate(t)                          CDSC % by completed years since receipt
(surrender chargeable base)                          surr_chargeable_pp(t)                        Remaining Premium withdrawn on surrender
(CDSC on surrender)                                  surr_charge_pp(t)                            Charge on a full surrender
AV(t) - CDSC                                         surr_benefit_pp(t)                           Surrender proceeds
RP(t)                                                rp_pp(t)                                     Remaining Premium, the CDSC basis
(premium portion withdrawn)                          rp_reduction_pp(t)                           Reduction of RP by a withdrawal
NP(t)                                                np_pp(t)                                     Cumulative Net Premiums
GWB(t)                                               gwb_pp(t)                                    Guaranteed Withdrawal Balance
GWB at a point in the month                          gwb_pp_at(t, timing)                         BEF_PREM / BEF_WD / BEF_ANNIV
(GWB after the bonus)                                gwb_pp_aft_bonus(t)                          Anniversary sub-step 3
(GWB after the step-up)                              gwb_pp_aft_stepup(t)                         Anniversary sub-step 4
b x BB                                               bonus_pp(t)                                  GLWB bonus credited at the anniversary
BB(t)                                                bb_pp(t)                                     Bonus Base
BB before the anniversary                            bb_pp_bef_anniv(t)                           Bonus Base the bonus is computed on
bonus_end(t)                                         bonus_end(t)                                 Contract year the Bonus Period ends
(the step-up basis)                                  stepup_base_pp(t)                            Annual CV or highest quarterly CV
(step-up occurred)                                   is_stepup(t)                                 True at a step-up anniversary
GAWA(t)                                              gawa_pp(t)                                   Guaranteed Annual Withdrawal Amount
GAWA in the month                                    gawa_pp_at(t, timing)                        BEF_PREM / BEF_WD / BEF_ANNIV
g(a)                                                 gawa_pct_at_age(a)                           GAWA% at attained age a
gawa_pct_fixed                                       gawa_pct_fixed(t)                            GAWA% locked at the first withdrawal
ADJ(t)                                               adj_pp(t)                                    GWB Adjustment amount
s                                                    gwb_adj_pct                                  GWB Adjustment percentage, 105%
(the Adjustment Date)                                is_gwb_adj_date(t)                           Later of anniv on/after 70 and the 12th
RB(t)                                                rb_pp(t)                                     GMDB Benefit Base
RB in the month                                      rb_pp_at(t, timing)                          BEF_PREM / BEF_WD / BEF_ANNIV
rho                                                  rollup_rate(t)                               GMDB roll-up percentage in force
(the year's d-f-d allowance) gmdb_allow_pp(t)        rho x RB at the prior anniversary
(d-f-d part of a withdrawal) gmdb_wd_dfd_pp(t)       Dollar-for-dollar portion
(excess part)                                        gmdb_wd_excess_pp(t)                         Portion above the allowance
(accrued d-f-d)                                      gmdb_dfd_acc_pp(t)                           Accrued to the end of the contract year
(accrued pro-rata factor)                            gmdb_factor_acc(t)                           Accrued to the end of the contract year
DB(t)                                                db_pp(t)                                     Gross death benefit max(AV, NP, RB)
max(NP, RB)                                          gmdb_guarantee_pp(t)                         The floor under DB; ``basic`` elects RB alone
GuaranteeClaim                                       gmdb_claim_pp(t)                             Net general-account strain on death
phi_G                                                phi_glwb(t)                                  GLWB charge rate in force
phi_D                                                phi_gmdb(t)                                  GMDB charge rate in force
Fee_G                                                fee_glwb_pp(t)                               Quarterly GLWB fee, on the GWB
Fee_D                                                fee_gmdb_pp(t)                               Quarterly GMDB fee, on the RB
f_c                                                  maint_fee_pp(t)                              Annual contract fee, $35 waived at $50k
(total unit cancellation)                            charge_pp(t)                                 Fee_G + Fee_D + f_c actually collected
(fee reset formula)                                  fee_rate_vix_raw(phi0, vix2)                 The VIX-squared fee formula [S4][S6]
(fee reset clipping)                                 fee_rate_vix_clip(prior, raw)                Band and corridor clipping [S4]
forlife_flag                                         forlife_flag()                               For Life Guarantee in effect
depleted_flag(t)                                     depleted_flag(t)                             AV has reached zero with the GLWB alive
(post-depletion payment)                             glwb_payment_pp(t)                           Insurer-funded GAWA payment
phase(t)                                             phase(t)                                     ACCUM / DEPLETED / EXPIRED
M_G(t)                                               moneyness_glwb(t)                            GWB / AV
M_D(t)                                               moneyness_gmdb(t)                            max(NP, RB) / AV
lambda(M)                                            lapse_itm_mult(m)                            The VM-21 7.B.1 multiplier
lambda*(t)                                           lapse_dyn_mult(t)                            min of the two, per VM-21 6.C.6
kappa(t)                                             lapse_wd_factor(t)                           0.60 in a withdrawal year
q^w_base(y)                                          lapse_rate_base(t)                           VM-21 Table 6.3 under-50%-ITM column
q^w_annual(t)                                        lapse_rate(t)                                Annual total surrender rate
q^w(t)                                               lapse_rate_mth(t)                            Monthly total surrender rate
q^d(t)                                               mort_rate_mth(t)                             Monthly mortality rate
(annual q_x)                                         mort_rate(t)                                 Annual mortality at the attained age
l(t-1)                                               pols_if(t)                                   In-force at the START of month t
l(t)                                                 pols_if_at(t, "AFT_DECR")                    In-force at the end of month t
l(0)                                                 pols_if_init                                 In-force at entry
l(t-1), ...                                          pols_if_at(t, timing)                        BEF_DECR / BEF_LAPSE / AFT_DECR
l(t-1) q^d                                           pols_death(t)                                Deaths
l(t-1)(1-q^d) q^w                                    pols_lapse(t)                                Full surrenders
(none)                                               pols_maturity(t)                             Survivors at the projection horizon
Premium income                                       premiums(t)                                  Premium cash flow
Charge income - M&E/admin                            asset_charges(t)                             Asset charge cash flow
Charge income - rider fees                           fees_glwb(t), fees_gmdb(t)                   Rider fee cash flow
Charge income - contract fee maint_fees(t)           Contract fee cash flow
Charge income - CDSC                                 wd_charges(t)                                CDSC on withdrawals (memo; see below)
Withdrawal proceeds                                  withdrawals(t)                               W(t) - c(t), weighted
Post-depletion GLWB payments glwb_payments(t)        GAWA paid after depletion
Death benefit (gross)                                claims(t, "DEATH")                           DB(t) x deaths
Death benefit (net strain)                           gmdb_claims(t)                               GuaranteeClaim x deaths (memo)
Surrender proceeds                                   claims(t, "LAPSE")                           surr_benefit_pp(t) x surrenders
(horizon benefit)                                    claims(t, "MATURITY")                        Survivors at proj_len()
Maintenance expense                                  expenses(t)                                  VM-21 6.C.2 prescribed expense
(acquisition)                                        commissions(t)                               0 in the base run [std]
(none)                                               net_cf(t)                                    The notes' ledger, summed
(none)                                               net_cf_ga(t)                                 General-account view (memo)
===================================================  ===========================================  =============================================

Model point attributes the notes and the model name identically — ``sex``,
``designated_lives``, ``tax_status``, ``premium_single``, ``premium_tax_rate``,
``glwb_option``, ``gmdb_option``, ``cdsc_schedule`` and the ``rate_sheet_date``
Reference — are not repeated in the table above; ``issue_date`` is not carried at all,
the model working in policy months throughout.

Nine names needed care.

``pols_if(t)`` is the count in force at the **start** of month ``t`` — the notes'
``l(t-1)`` — and is the weight applied to that same row's cash flows, so
``premiums(t) / premium_pp(t)`` is exactly ``pols_if(t)`` and the printed in-force column
reconciles with the row it sits on. That is the library-wide convention, set by
:mod:`.Term_US_A` and by ``savings.CashValue_SE``. The notes' own end-of-month ``l(t)``
has not gone anywhere: it is :func:`pols_if_at` ``(t, "AFT_DECR")``, and the roll-forward
is written across it.

``lapse_rate(t)`` is the **annual** total surrender rate and :func:`lapse_rate_mth` the
monthly one, matching the ``mort_rate`` / ``mort_rate_mth`` pair. Both spellings of the
notes' ``q^w`` are present and the suffix is the only thing that tells them apart, so
read the suffix.

``wd_free_pp(t)`` is the portion of a withdrawal covered by the **free-withdrawal
allowance**, which is what the same name means on the deferred annuity chassis
(:mod:`.MYGA_US_S`, ``min(W, FW)``). On this product a second exemption
stacks on top of it — no CDSC applies to cumulative withdrawals within ``L`` [S1] — and
the union of the two is :func:`wd_exempt_pp`, the portion of ``W(t)`` bearing no charge
at all. The two differ by exactly :func:`wd_nonexcess_pp`, and it is
:func:`wd_exempt_pp`, not :func:`wd_free_pp`, that complements
:func:`wd_chargeable_pp`. The year-to-date cumulative is
:func:`free_wd_used_cum_pp`, named for what it is rather than sharing the ``wd_*`` stem.

``E(t)`` is the **guarantee** excess here — the portion of a withdrawal above the GLWB
annual limit — and :func:`wd_excess_pp` carries that meaning. In
:mod:`.MYGA_US_S` the same cells name means the portion of a withdrawal above
the free allowance, i.e. the *charge* base. On this product those are two different
quantities and both exist: the charge base is :func:`wd_chargeable_pp`. Reading
``wd_excess_pp`` across the two models without checking is the single easiest mistake to
make in this library.

``E(t)`` in :mod:`.Term_US_A` is expenses, which here is :func:`expenses` as usual. ``M``
is the in-the-moneyness ratio here and the market value adjustment in
:mod:`.MYGA_US_S`; a VA separate account has no MVA at all, so there is no
collision in the model, only in the reader's memory. ``c(t)`` is the CDSC here and the
Model #805 contract charge in :mod:`.MYGA_US_S`; it becomes
:func:`wd_charge_pp`. ``g`` is the GAWA% here and the monthly nonforfeiture factor there;
it becomes :func:`gawa_pct_at_age`. And ``b`` is the GLWB bonus percentage here and the
MVA distribution yield there.

Two cells the chassis has that this model deliberately does **not**: ``mgsv_pp`` and
``surr_value_pp``. NAIC Model #805 expressly excludes variable annuities and reaches a VA
only through its *fixed* account under Model #250 §7.B [REG-R42][REG-R43], and this
contract has no fixed account because electing the Roll-up GMDB removes the Fixed Account
Options [S1]. There is therefore no minimum guaranteed surrender value and no pre-floor
surrender value to distinguish: :func:`surr_benefit_pp` is simply ``AV(t)`` less the
CDSC. Carrying the chassis' floor across would be the error the chassis file itself warns
against.

.. rubric:: The unit ledger

The notes write the account value as ``AV = Σ_i U_i V_i`` and require charges assessed
*per unit of value* (fund expense, M&E, administrative asset charge) to live **inside**
``V_i``, while charges assessed *per contract or on a benefit base* (the annual contract
fee, the two rider fees) are collected by **cancelling units**, leaving ``V_i``
untouched: ``ΔU_i = C · w_i(t) / V_i(t)``, so ``ΔAV = C``.

The model carries the *product* ``SA_i = U_i V_i`` rather than the two factors, because
with no transfers between subaccounts the two are never needed apart, and every quantity
the notes print is a subaccount **value**. The distinction the ledger exists to enforce
survives intact: a per-unit charge multiplies ``sa_pp`` through :func:`unit_growth`,
while a unit cancellation multiplies it by ``(1 − C / AV)`` — which is exactly pro-rata
deduction, and which therefore leaves every ``w_i`` unchanged.

That property is necessary for the notes' 60/40 anchor cell to still sit at exactly
60/40 twenty-six months later, but it is **not sufficient**, and it would be a bad
lesson to take away on its own: unequal growth moves the weights whatever the charges
do. What closes the gap is the illustrative ``base`` path, reverse-engineered so that
the two subaccounts grow at the same rate *net of fund expense* (see the ``provenance``
column of *return_scenario.csv*) — with equal net growth and pro-rata cancellation the
weights cannot move at all. The worked-example month itself is the counter-example:
``r_1`` = +1.20% against ``r_2`` = −0.30% takes ``w_1`` from 0.600000 at BOM 27 to
:func:`sa_weight` ``(27, 1)`` = 0.603519 by the time the fees are read, one month later.

.. rubric:: Timing arguments

Account and subaccount values, following ``CashValue_SE``'s ``av_pp_at``:

``"BEF_PREM"``
    ``AV(t-1)``, at the start of month ``t`` before the premium.
``"BEF_WD"``
    after the premium has bought units, before the withdrawal.
``"BEF_INV"``
    ``AV'(t)``, after the withdrawal, before unit value growth.
``"BEF_FEE"``
    after growth, before the rider fees and the contract fee. This is the point at which
    the notes read the pro-rata key ``w_i``.
``"EOM"``
    ``AV(t)``, after every charge. Equal to :func:`av_pp`.

Guarantee bases (``gwb_pp_at``, ``gawa_pp_at``, ``rb_pp_at``) take ``"BEF_PREM"``,
``"BEF_WD"`` and ``"BEF_ANNIV"``; their end-of-month value, after the anniversary
guarantee events, is the plain cells (:func:`gwb_pp`, :func:`gawa_pp`, :func:`rb_pp`).

Policy counts, following ``CashValue_SE``'s ``pols_if_at``:

``"BEF_DECR"``
    ``l(t-1)``, in force at the start of month ``t``. Equal to :func:`pols_if` ``(t)``.
``"BEF_LAPSE"``
    after deaths, ``l(t-1)(1 - q^d(t))``.
``"AFT_DECR"``
    after surrenders, ``l(t)`` — the notes' end-of-month count, and equal to
    :func:`pols_if` ``(t + 1)`` except in the horizon month, where the survivors leave as
    :func:`pols_maturity` instead.

Benefit ``kind`` arguments are ``"DEATH"``, ``"LAPSE"`` and ``"MATURITY"``. Any other
value of any of these raises ``ValueError``.

.. rubric:: pols_maturity and the projection horizon

The technical notes state no projection horizon, and this contract does not supply one:
once the account value is exhausted the For Life Guarantee is a **pure life-contingent
annuity at GAWA**, which the notes rank sixth in their sensitivity list precisely because
the mortality basis then becomes the whole story. The model therefore runs to attained
age ``omega_age`` = 120 **[std]**, the terminal age of the mortality table, and
``pols_maturity(t)`` carries the survivors out at that month — zero everywhere else — so
that

    pols_if(t) - pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)

holds for every ``t``, including the last, where the block would otherwise appear to lose
lives with no cause. The identity is written on start-of-month counts because that is
what :func:`pols_if` carries; ``pols_if(proj_len() + 1)`` is zero, every survivor of the
horizon month having left as :func:`pols_maturity`. The name follows
``BasicTerm_S.pols_maturity`` and the construction follows :mod:`.Term_US_A` and
:mod:`.MYGA_US_S`. It is bookkeeping determined by the horizon, not an added
assumption.

The contract's own Latest Income Date — the Contract Anniversary at owner age 95 [S2] —
is **not** implemented as a forced annuitization; see the model docstring's list of what
is not implemented.
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


def policy_id():
    """The contract identifier of the selected model point."""
    return model_point()["policy_id"]


def age_at_entry():
    """x: the issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the Designated Life, M or F."""
    return model_point()["sex"]


def designated_lives():
    """``single`` or ``joint``.

    Reported only: the joint-life Flex GMWB is out of scope in the product spec, so the
    GAWA% grid and the For Life test are the single-life ones **[std]**.
    """
    return model_point()["designated_lives"]


def tax_status():
    """``NQ`` or ``Q``.

    Reported only. The base run is non-qualified **[std]**, which keeps the RMD term of
    ``L = max(GAWA, RMD)`` disclosed but inactive; no RMD module is implemented.
    """
    return model_point()["tax_status"]


def pols_if_init():
    """l(0): in-force probability at entry, 1 for a single-contract model point."""
    return float(model_point()["pols_if_init"])


def premium_tax_rate():
    """tau: premium tax deducted from the purchase payment, 0% **[std]**, 0-3.5% [S2].

    Set to zero so that GWB at issue equals gross premium and the worked example is
    checkable; premium tax is contractually deducted from the amounts that initialize the
    guarantee bases [S1].
    """
    return float(model_point()["premium_tax_rate"])


def premium_single():
    """The single purchase payment stated on the model point, paid at ``t = 0``."""
    return float(model_point()["premium"])


def fund_set():
    """The key into *fund_table.csv* naming this contract's subaccount allocation."""
    return model_point()["fund_set"]


def sub_ids():
    """The subaccount indices of the model point's allocation set, in file order.

    Two subaccounts **[std]** — the minimum that exercises pro-rata charge allocation and
    unit accounting. Real contracts offer far more; Corebridge lists 76 across 12 asset
    classes [S4].
    """
    return list(data.fund_table().loc[fund_set()].index)              # noqa: F821


def alloc(i):
    """alloc[i]: the share of net premium allocated to subaccount i, no rebalancing."""
    return float(data.fund_table().loc[(fund_set(), i), "alloc"])     # noqa: F821


def fund_expense_rate(i):
    """e_i: the annual fund expense ratio of subaccount i, paid to the fund [S2]."""
    return float(data.fund_table().loc[(fund_set(), i), "fund_expense"])  # noqa: F821


def glwb_option():
    """The GLWB election, and the key into the GAWA% grid; ``single_core`` [S3]."""
    return model_point()["glwb_option"]


def stepup_basis():
    """``annual_CV`` or ``highest_quarterly_CV`` [S1][S3].

    ``annual_CV`` is the representative election: the step-up test uses the Contract
    Value at the anniversary. ``highest_quarterly_CV`` uses the highest contract value
    over the four most recent Contract Quarterly Anniversaries; the source also adjusts
    each of those for subsequent premiums and withdrawals under the same
    dollar-for-dollar / proportional rule, which is **not implemented** — see the model
    docstring.
    """
    return model_point()["glwb_stepup_basis"]


def gmdb_option():
    """``rollup``, ``HQAV`` or ``basic``.

    ``rollup`` is the representative election: ``RB(t) = RB(t-1)(1 + rho)`` at each
    anniversary to the age cutoff, with a dollar-for-dollar withdrawal allowance applied
    at Contract Year end [S1][S3]. ``HQAV`` is the annual ratchet ``max(RB, AV)`` at each
    anniversary with proportional withdrawal treatment [S1][S4][S7]. ``basic`` is the
    included no-charge proportional return of premium [S1][S2]; on that election the base
    *is* the return of premium, so :func:`np_pp` is not floored under it as well — see
    :func:`gmdb_guarantee_pp`. The notes' fourth form, ``combination``, is **not
    implemented** — see the model docstring.
    """
    return model_point()["gmdb_option"]


def cdsc_schedule():
    """The key into *cdsc_table.csv* naming this contract's withdrawal charge scale."""
    return model_point()["cdsc_schedule"]


def fee_reset_rule():
    """``none``, ``quinquennial`` or ``vix``.

    ``none`` is the base run **[std]**: the insurer does not increase the rider charge
    and the owner does not opt out. ``quinquennial`` applies the maximum single increase
    of +0.25% at each fifth Contract Anniversary up to the guaranteed maximum [S1].
    ``vix`` applies the Corebridge non-discretionary VIX-squared formula [S4][S6].
    """
    return model_point()["fee_reset_rule"]


def rollup_rule():
    """``fixed`` or ``cmt_linked``.

    ``fixed`` is the base run **[std]**: 6.00% at election ages up to 69 and 5.00% from
    70 [S3]. ``cmt_linked`` is the Equitable formula rate, a 20-day average 10-year CMT
    plus 1.00% (1.50% before the first withdrawal), rounded to 0.10%, floored at 4% and
    capped at 8% [S7].
    """
    return model_point()["rollup_rule"]


def wd_start_age():
    """The attained age at which GLWB withdrawals begin; 70 in the base run **[std]**.

    Zero means the contract never withdraws. The base-run value rests on the finding that
    activation clusters at the RMD age [REG-R64 **[unverified]**][REG-R57][REG-R58]. The
    prescribed alternative is VM-21's Withdrawal Delay Cohort Method, which is **not
    implemented**.
    """
    return int(model_point()["wd_start_age"])


def wd_intensity():
    """The fraction of the annual limit withdrawn once activated; 100% **[std]**.

    100% matches VM-21 §6.C.3's Guarantee Actuarial Present Value construction [R1]. The
    prescribed partial-withdrawal assumption is 90% for lifetime GMWBs and 70% for
    non-lifetime ones [R1].
    """
    return float(model_point()["wd_intensity"])


def scenario_id():
    """The scenario the model point runs on, a key into the two scenario tables."""
    return model_point()["scenario_id"]


def txn_id():
    """The scheduled transaction programme, a key into *transaction_table.csv*."""
    return model_point()["txn_id"]


def duration_mth_init():
    """Policy months already elapsed at ``t = 0``; 0 for an at-issue cell.

    An in-force cell enters mid-contract, so ``t = 1`` is policy month
    ``duration_mth_init() + 1``. The worked example's carried state is entered this way
    on model point 2.
    """
    return int(model_point()["duration_mth_init"])


def is_inforce():
    """True when the model point enters mid-contract rather than at issue."""
    return duration_mth_init() > 0


def av_pp_init():
    """AV carried into ``t = 0``; 0 at issue, the in-force cell's contract value else.

    An in-force contract value is split across subaccounts by ``alloc[i]`` **[std]**: the
    notes give an ``av_initial`` model point attribute but no subaccount split, and the
    worked example's carried state is exactly at its 60/40 target allocation.
    """
    return float(model_point()["av_init"])


def gwb_pp_init():
    """GWB carried into ``t = 0``; 0 at issue, where the premium creates it [S1]."""
    return float(model_point()["gwb_init"])


def gawa_pp_init():
    """GAWA carried into ``t = 0``; 0 until the first withdrawal fixes it [S1]."""
    return float(model_point()["gawa_init"])


def gawa_pct_init():
    """The GAWA% already locked at ``t = 0``; 0 when no withdrawal has been taken."""
    return float(model_point()["gawa_pct_init"])


def has_wd_init():
    """Whether a withdrawal had already been taken before ``t = 0``.

    Inferred from ``gawa_pct_init``, which is non-zero exactly when the GAWA% has been
    locked, so an in-force cell needs no separate flag column.
    """
    return gawa_pct_init() > 0.0


def bb_pp_init():
    """Bonus Base carried into ``t = 0``; it initializes at GWB [S1]."""
    return float(model_point()["bb_init"])


def rb_pp_init():
    """GMDB Benefit Base carried into ``t = 0``."""
    return float(model_point()["rb_init"])


def np_pp_init():
    """Cumulative Net Premiums carried into ``t = 0``."""
    return float(model_point()["np_init"])


def rp_pp_init():
    """Remaining Premium carried into ``t = 0``; the CDSC basis [S2]."""
    return float(model_point()["rp_init"])


def adj_pp_init():
    """GWB Adjustment carried into ``t = 0``; 105% of net premium at issue [S3]."""
    return float(model_point()["adj_init"])


def bonus_end_init():
    """The contract year the Bonus Period ends, carried into ``t = 0``.

    Zero on an at-issue cell, where it is set to ``bonus_period_years`` = 10 [S1].
    """
    return int(model_point()["bonus_end_init"])


def policy_term():
    """Contract term in years: entry age to ``omega_age`` **[std]**."""
    return omega_age - age_at_entry()                                 # noqa: F821


def proj_len():
    """Projection length in months from ``t = 0``, net of months already elapsed."""
    return 12 * policy_term() - duration_mth_init()


def duration_mth(t):
    """The policy month at projection month t: ``duration_mth_init() + t``."""
    return duration_mth_init() + t


def policy_year(t):
    """y(t) = ceil(policy month / 12): the contract year; 0 at issue."""
    return (duration_mth(t) + 11) // 12


def duration(t):
    """Completed contract years at month t, ``policy_year(t) - 1``, floored at 0."""
    return max(0, policy_year(t) - 1)


def age(t):
    """a(t) = x + y - 1: the attained age (ANB) during month t."""
    return age_at_entry() + duration(t)


def age_at_anniv(t):
    """The attained age just after the Contract Anniversary at the end of month t.

    ``x + y``, one more than :func:`age`, and the age the GMDB growth cutoff and the
    Bonus Period restart cutoff are stated against [S1].
    """
    return age_at_entry() + policy_year(t)


def contract_quarter(t):
    """k(t) = ceil(policy month / 3): the contract quarter containing month t."""
    return (duration_mth(t) + 2) // 3


def is_anniv(t):
    """True at the end of a Contract Anniversary month, ``policy month = 0 (mod 12)``."""
    return t >= 1 and t <= proj_len() and duration_mth(t) % 12 == 0


def is_quarterly_anniv(t):
    """True at a Contract Quarterly Anniversary, ``policy month = 0 (mod 3)`` **[std]**."""
    return t >= 1 and t <= proj_len() and duration_mth(t) % 3 == 0


def is_year_start(t):
    """True in the first month of a contract year, where SumW_y resets [S1]."""
    return t >= 1 and (duration_mth(t) - 1) % 12 == 0


def t_of_month(m):
    """The projection index t of policy month m; negative before the entry instant."""
    return m - duration_mth_init()


def phase(t):
    """ACCUM, DEPLETED or EXPIRED at month t."""
    if t > proj_len():
        return "EXPIRED"
    return "DEPLETED" if depleted_flag(t) else "ACCUM"


def inv_return_mth(t, i):
    """r_i(t): the gross monthly fund return of subaccount i, a scenario input.

    Read from *return_scenario.csv* as a step function of the **policy** month, so a flat
    path is one row per subaccount. VM-21 requires each variable subaccount to be mapped
    to a crafted proxy fund, normally a linear combination of recognized market indices
    [R1]; the model takes the return series as an input rather than hard-coding one.
    """
    sub = data.return_scenario().loc[(scenario_id(), i)]              # noqa: F821
    months = [m for m in sub.index if m <= max(duration_mth(t), 0)]
    return float(sub.loc[max(months), "gross_return"])


def scenario_rate(t, name):
    """Step-function lookup of column ``name`` in the model point's rate scenario.

    Each row of *rate_scenario.csv* states the level that holds from its own policy month
    until the next row of the same scenario, so a flat path is one row.
    """
    sub = data.rate_scenario().loc[scenario_id()]                     # noqa: F821
    months = [m for m in sub.index if m <= max(duration_mth(t), 0)]
    return float(sub.loc[max(months), name])


def vix_sq(k):
    """The quarterly average of daily VIX-squared for contract quarter k [S4][S6].

    Read at the last month of the quarter. Used only by the ``vix`` fee reset rule.
    """
    return scenario_rate(t_of_month(3 * k), "vix_sq")


def cmt10(t):
    """The 20-day average 10-year Constant Maturity Treasury rate at month t [S7].

    Used only by the ``cmt_linked`` roll-up rule.
    """
    return scenario_rate(t, "cmt10")


def unit_growth(t, i):
    """The monthly unit value factor of subaccount i.

    ``(1 + r_i(t)) x (1 - e_i/12) x (1 - (m + alpha)/12)`` — a monthly discretization of
    a daily accrual **[std]** [S2]. The fund's own expense and the base contract asset
    charge live **inside** the unit value; charges assessed per contract or on a benefit
    base do not, and are collected by cancelling units instead. Do not additionally
    compound daily: pick one discretization and document it, because reconciling to an
    admin system requires knowing which was used.
    """
    return ((1.0 + inv_return_mth(t, i))
            * (1.0 - fund_expense_rate(i) / 12.0)
            * (1.0 - (asset_charge_me + asset_charge_admin) / 12.0))  # noqa: F821


def sa_pp_at(t, i, timing):
    """SA_i at month t read at the point given by ``timing``; see the Space docstring.

    A withdrawal and a unit cancellation both scale the subaccount by
    ``(1 - amount / AV)`` — pro-rata deduction — so neither moves the value weights.
    """
    if t < 0:
        return 0.0
    if t == 0:
        return alloc(i) * (av_pp_init() + prem_to_av_pp(0))
    if depleted_flag(t - 1) or t > proj_len():
        return 0.0
    sa = sa_pp(t - 1, i)
    if timing == "BEF_PREM":
        return sa
    sa = sa + alloc(i) * prem_to_av_pp(t)
    if timing == "BEF_WD":
        return sa
    base = av_pp_at(t, "BEF_WD")
    sa = sa * (1.0 - wd_pp(t) / base) if base > 0.0 else 0.0
    if timing == "BEF_INV":
        return sa
    sa = sa * unit_growth(t, i)
    if timing == "BEF_FEE":
        return sa
    base = av_pp_at(t, "BEF_FEE")
    sa = sa * (1.0 - charge_pp(t) / base) if base > 0.0 else 0.0
    if timing == "EOM":
        return sa
    raise ValueError("invalid timing")


def sa_pp(t, i):
    """SA_i(t): the value of subaccount i per contract at the end of month t."""
    return sa_pp_at(t, i, "EOM")


def av_pp_at(t, timing):
    """AV at month t read at the point given by ``timing``: the sum over subaccounts."""
    return sum(sa_pp_at(t, i, timing) for i in sub_ids())


def av_pp(t):
    """AV(t): the contract value per contract at the end of month t."""
    return av_pp_at(t, "EOM")


def sa_weight(t, i):
    """w_i(t): the value weight of subaccount i, the pro-rata deduction key [S2].

    Read at ``BEF_FEE``, where the notes read it: after the month's growth and before the
    charges that cancel units.
    """
    base = av_pp_at(t, "BEF_FEE")
    return sa_pp_at(t, i, "BEF_FEE") / base if base > 0.0 else 0.0


def gross_inv_income_pp(t):
    """The gross fund return over month t, before any charge."""
    if t < 1 or depleted_flag(t - 1):
        return 0.0
    return sum(sa_pp_at(t, i, "BEF_INV") * inv_return_mth(t, i) for i in sub_ids())


def fund_expense_pp(t):
    """The funds' own expense collected inside the unit value.

    ``Σ_i SA_i(1 + r_i) e_i/12``. **Not insurer revenue** — it is paid to the underlying
    funds — so it never enters :func:`charge_income` or :func:`net_cf`.
    """
    if t < 1 or depleted_flag(t - 1):
        return 0.0
    return sum(sa_pp_at(t, i, "BEF_INV") * (1.0 + inv_return_mth(t, i))
               * fund_expense_rate(i) / 12.0 for i in sub_ids())


def asset_charge_pp(t):
    """The M&E and administrative asset charge collected inside the unit value.

    ``Σ_i SA_i^{pre-charge}(t) (m + alpha)/12`` where the pre-charge value is net of the
    fund's own expense, which is deducted first inside :func:`unit_growth`. This is
    insurer charge income.
    """
    if t < 1 or depleted_flag(t - 1):
        return 0.0
    rate = (asset_charge_me + asset_charge_admin) / 12.0             # noqa: F821
    return sum(sa_pp_at(t, i, "BEF_INV") * (1.0 + inv_return_mth(t, i))
               * (1.0 - fund_expense_rate(i) / 12.0) * rate for i in sub_ids())


def inv_income_pp(t):
    """The change in AV over month t from investment, net of both per-unit charges.

    ``AV(BEF_FEE) - AV(BEF_INV)``, and identically
    ``gross_inv_income_pp - fund_expense_pp - asset_charge_pp``.
    """
    if t < 1:
        return 0.0
    return av_pp_at(t, "BEF_FEE") - av_pp_at(t, "BEF_INV")


def prem_scheduled_pp(t):
    """The gross premium scheduled for month t in *transaction_table.csv*, else zero."""
    if t < 1:
        return 0.0
    table = data.transaction_table()                                 # noqa: F821
    key = (txn_id(), duration_mth(t))
    return float(table.loc[key, "prem_amount"]) if key in table.index else 0.0


def premium_pp(t):
    """P(t): the gross premium paid at BOM of month t.

    The model point's single purchase payment at ``t = 0``, plus anything scheduled in
    *transaction_table.csv*. The chassis is flexible-premium [S1][S2] and premium receipt
    is retained as an active term in every guarantee-base recursion, so a subsequent
    payment is a data change rather than a formula change.
    """
    if t == 0:
        return premium_single() + prem_scheduled_pp(t)
    if t < 0 or t > proj_len() or depleted_flag(t - 1):
        return 0.0
    return prem_scheduled_pp(t)


def prem_to_av_pp(t):
    """P(t)(1 - tau): the net premium that buys units and raises the guarantee bases.

    The per-contract counterpart of :func:`prem_to_av`, and the name every
    account-value model in this library uses for the premium credited to the account
    value. Not to be confused with ``WholeLife_US_A.premium_net_pp``, which is a *gross*
    premium net of the dividend offset — a different concept entirely.
    """
    return premium_pp(t) * (1.0 - premium_tax_rate())


def wd_scheduled_pp(t):
    """The gross withdrawal scheduled for month t in *transaction_table.csv*, else zero."""
    if t < 1:
        return 0.0
    table = data.transaction_table()                                 # noqa: F821
    key = (txn_id(), duration_mth(t))
    return float(table.loc[key, "wd_amount"]) if key in table.index else 0.0


def is_wd_month(t):
    """True when the GLWB utilization withdrawal falls in month t.

    Base run **[std]**: the contract activates in the first month of the contract year in
    which the attained age reaches :func:`wd_start_age`, and withdraws in the first month
    of every contract year thereafter. ``wd_start_age = 0`` never withdraws.
    """
    if t < 1 or t > proj_len() or wd_start_age() <= 0:
        return False
    if depleted_flag(t - 1) or not is_year_start(t):
        return False
    return age(t) >= wd_start_age()


def is_wd_taken(t):
    """True when any withdrawal is taken in month t, before its amount is known.

    Stated as a predicate rather than ``wd_pp(t) > 0`` so that the first-withdrawal test
    can run *before* the GAWA% is fixed, which is what the amount itself depends on.
    """
    if t < 1 or t > proj_len() or depleted_flag(t - 1):
        return False
    return wd_scheduled_pp(t) > 0.0 or is_wd_month(t)


def has_wd_by(t):
    """True when a withdrawal has been taken at or before month t."""
    if t < 1:
        return has_wd_init()
    return has_wd_by(t - 1) or is_wd_taken(t)


def is_first_wd(t):
    """True in the month of the contract's first withdrawal.

    The notes are explicit that this test must run **before** the annual limit ``L`` is
    formed: a first withdrawal tested against ``GAWA = 0`` would score entirely as excess
    and wreck both benefit bases [S1].
    """
    return is_wd_taken(t) and not has_wd_by(t - 1)


def is_wd_year(t):
    """True when any withdrawal falls in the contract year containing month t.

    Drives the VM-21 withdrawal-year surrender factor ``kappa`` [R1] and the rule that
    *any* withdrawal in a Contract Year kills that year's bonus [S1].
    """
    first = t_of_month(12 * (policy_year(t) - 1) + 1)
    return any(is_wd_taken(u) for u in range(max(1, first),
                                             min(first + 12, proj_len() + 1)))


def gawa_pct_at_age(a):
    """g(a): the GAWA% for attained age a, from *gawa_pct_table.csv* [S3]."""
    grid = data.gawa_pct_table().loc[glwb_option()]                  # noqa: F821
    bands = [b for b in grid.index if b <= a]
    if not bands:
        return 0.0
    return float(grid.loc[max(bands), "gawa_pct"])


def wd_limit_pp(t):
    """L(t) = max(GAWA, RMD): the annual withdrawal limit governing month t [S1].

    At the first withdrawal the GAWA is fixed on the **pre-withdrawal** GWB, so the limit
    is formed from that. The RMD term is disclosed but inactive: the base run is
    non-qualified and no RMD module is implemented.
    """
    if is_first_wd(t):
        return gawa_pct_at_age(age(t)) * gwb_pp_at(t, "BEF_WD")
    return gawa_pp_at(t, "BEF_WD")


def wd_glwb_pp(t):
    """The GLWB utilization withdrawal: ``wd_intensity x L(t)`` once activated **[std]**."""
    return wd_intensity() * wd_limit_pp(t) if is_wd_month(t) else 0.0


def wd_pp_due(t):
    """The gross withdrawal requested at BOM of month t, before capping at AV.

    Scheduled withdrawals **add to** the utilization withdrawal, which is how a model
    point exercises the excess algebra without disturbing the base run.
    """
    if t < 1 or t > proj_len() or depleted_flag(t - 1):
        return 0.0
    return wd_scheduled_pp(t) + wd_glwb_pp(t)


def wd_pp(t):
    """W(t): the gross amount removed from the contract value at BOM of month t.

    Measured **inclusive of withdrawal charges, MVAs, advisory fees and every other
    charge** for all guarantee calculations [S1]; using net proceeds would understate the
    benefit-base reduction. Capped at the available contract value **[std]**.
    """
    return min(wd_pp_due(t), av_pp_at(t, "BEF_WD"))


def sum_wd_pp(t):
    """SumW_y: cumulative withdrawals in the current contract year, including W(t) [S1]."""
    if t < 1:
        return 0.0
    prev = 0.0 if is_year_start(t) else sum_wd_pp(t - 1)
    return prev + wd_pp(t)


def wd_excess_pp(t):
    """E(t) = min(W, SumW_y - L) if SumW_y > L else 0: the excess withdrawal [S1].

    This is the **guarantee** excess, not the charge base — see the Space docstring's
    note on the divergence from :mod:`.MYGA_US_S`.
    """
    if wd_pp(t) <= 0.0:
        return 0.0
    over = sum_wd_pp(t) - wd_limit_pp(t)
    return min(wd_pp(t), over) if over > 0.0 else 0.0


def wd_nonexcess_pp(t):
    """N(t) = W(t) - E(t): the guaranteed portion of the withdrawal [S1]."""
    return wd_pp(t) - wd_excess_pp(t)


def cv_pre_excess_pp(t):
    """CV_pre: the contract value after the non-excess portion has been deducted [S1].

    The order is decisive: the non-excess portion reduces the base dollar-for-dollar
    **first**, and the proportional factor for the excess is computed against the
    contract value *after* that reduction. Reversing it changes both GWB and GAWA.
    """
    return av_pp_at(t, "BEF_WD") - wd_nonexcess_pp(t)


def excess_factor(t):
    """``1 - E(t)/CV_pre``: the pro-rata factor applied to GWB, GAWA and BB [S1]."""
    base = cv_pre_excess_pp(t)
    if base <= 0.0:
        return 0.0
    return max(0.0, 1.0 - wd_excess_pp(t) / base)


def free_wd_allow(t):
    """The charge-free amount at month t: earnings first, then 10% of Remaining Premium.

    The notes state it as ``max(0, AV - RP)`` plus ``max(0, 0.10 RP - earnings)``, which
    is ``max(earnings, 0.10 x RP)`` [S1]. Aged-out premium is free too, which the CDSC
    scale delivers by reaching 0.0% at seven completed years [S2].
    """
    rp = rp_pp(t - 1) + premium_pp(t) if t >= 1 else rp_pp_init()
    earnings = max(0.0, av_pp_at(t, "BEF_WD") - rp)
    return max(earnings, free_wd_rate * rp)                          # noqa: F821


def free_wd_avail(t):
    """The free-withdrawal allowance still unused in the contract year at BOM of month t."""
    if t < 1:
        return 0.0
    used = 0.0 if is_year_start(t) else free_wd_used_cum_pp(t - 1)
    return max(0.0, free_wd_allow(t) - used)


def wd_free_pp(t):
    """The free-allowance portion of month t's withdrawal: ``min(FW, E(t))``.

    The chassis name for the same thing — :mod:`.MYGA_US_S` has
    ``min(W, FW)`` — differing only in that here the allowance is applied to the
    *guarantee excess* rather than to the whole withdrawal, because the non-excess
    portion is already exempt from the CDSC under the within-``L`` rule [S1]. The
    portion of ``W(t)`` bearing no charge *at all* is therefore the wider
    :func:`wd_exempt_pp`, not this cells.
    """
    return min(free_wd_avail(t), wd_excess_pp(t))


def free_wd_used_cum_pp(t):
    """The free allowance consumed so far in the contract year, including month t.

    The year-to-date cumulative of :func:`wd_free_pp`, reset at each contract year
    start; it is what :func:`free_wd_avail` and :func:`surr_free_pp` net off.
    """
    if t < 1:
        return 0.0
    prev = 0.0 if is_year_start(t) else free_wd_used_cum_pp(t - 1)
    return prev + wd_free_pp(t)


def wd_exempt_pp(t):
    """The portion of W(t) bearing no withdrawal charge at all.

    Two exemptions stack: **no CDSC applies to cumulative withdrawals within L** [S1],
    which covers the non-excess portion outright, and the free-withdrawal allowance
    covers part of what is left. So this is identically
    ``wd_nonexcess_pp(t) + wd_free_pp(t)``, and it — not :func:`wd_free_pp` — is what
    complements :func:`wd_chargeable_pp`.
    """
    return min(wd_pp(t), wd_nonexcess_pp(t) + free_wd_avail(t))


def wd_chargeable_pp(t):
    """The portion of W(t) exposed to the CDSC: ``max(0, E(t) - free allowance)``."""
    return wd_pp(t) - wd_exempt_pp(t)


def surr_charge_rate(t):
    """The CDSC rate at month t, read off the **contract duration** [S2].

    The scale runs 8.5% down to 0.0% at seven completed years and is read from
    *cdsc_table.csv*, keyed by :func:`duration`.

    The notes key it on *completed years since receipt of the premium being withdrawn*
    [S2], which coincides with the contract duration only while the contract is single
    premium. It is **not implemented** by premium tranche: :func:`rp_pp` carries Remaining
    Premium as one undifferentiated pool, so a subsequent premium does not restart its
    own charge clock — model point 4 pays a second premium at policy month 73 and is read
    at that contract's 6-completed-year band rather than at the new tranche's 8.5%. Named
    in the model docstring's and the README's *not implemented* lists and pinned by a
    test; splitting the pool needs a withdrawal-ordering rule across tranches that no
    retrieved source states.
    """
    grid = data.cdsc_table().loc[cdsc_schedule()]                    # noqa: F821
    years = min(duration(t), int(grid.index.max()))
    return float(grid.loc[years, "surr_charge_rate"])


def wd_charge_pp(t):
    """c(t): the withdrawal charge on month t's withdrawal [S2]."""
    return surr_charge_rate(t) * wd_chargeable_pp(t)


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``W(t) - c(t)``."""
    return wd_pp(t) - wd_charge_pp(t)


def surr_free_pp(t):
    """The charge-free amount left for a full surrender at the end of month t."""
    rp = rp_pp(t)
    earnings = max(0.0, av_pp(t) - rp)
    allow = max(earnings, free_wd_rate * rp)                         # noqa: F821
    return max(0.0, allow - free_wd_used_cum_pp(t))


def surr_chargeable_pp(t):
    """The Remaining Premium withdrawn on a full surrender, net of the free amount [S2]."""
    return min(rp_pp(t), max(0.0, av_pp(t) - surr_free_pp(t)))


def surr_charge_pp(t):
    """The CDSC on a full surrender at the end of month t."""
    return surr_charge_rate(t) * surr_chargeable_pp(t)


def surr_benefit_pp(t):
    """Surrender proceeds: ``AV(t)`` less the CDSC.

    There is **no nonforfeiture floor** under this value. NAIC Model #805 expressly
    excludes variable annuities and reaches a VA only through its fixed account under
    Model #250 §7.B [REG-R42][REG-R43], and electing the Roll-up GMDB removes the Fixed
    Account Options [S1]. Contrast :mod:`.MYGA_US_S`, where
    ``max(SV, MGSV)`` is the whole point.
    """
    return av_pp(t) - surr_charge_pp(t)


def phi_glwb(t):
    """phi_G: the annual GLWB rider charge rate in force in month t.

    1.25% of the GWB currently [S3], guaranteed maximum 3.00% **[std]** within an
    observed 1.20%-3.00% band by option and vintage [S1]. ``fee_reset_rule`` selects the
    reset mechanism; the base run does not increase the charge and the owner does not opt
    out **[std]**, because opting out forfeits bonus, step-up and GWB Adjustment and
    blocks future premium [S1], so a rational opt-out is a joint decision rather than an
    independent lapse-style rate.
    """
    rule = fee_reset_rule()
    if rule == "none":
        return phi_glwb_curr                                         # noqa: F821
    elif rule == "quinquennial":
        steps = duration(t) // fee_reset_years                       # noqa: F821
        return min(phi_glwb_max,                                     # noqa: F821
                   phi_glwb_curr + fee_increase_max * steps)         # noqa: F821
    elif rule == "vix":
        return phi_glwb_vix(contract_quarter(t))
    else:
        raise ValueError("invalid fee_reset_rule")


def fee_rate_vix_raw(phi_0, vix_sq_avg):
    """The unclipped VIX-squared fee formula [S4][S6].

    ``phi_0 + 0.05% x [ QuarterlyAverage(daily VIX^2) / 33 - 10 ]``. The disclosed
    examples are an initial 1.45% with a quarterly average of 204.42 giving 1.26%, and
    602.30 giving an unclipped 1.86%.
    """
    return phi_0 + vix_fee_coef * (vix_sq_avg / vix_divisor - vix_offset)  # noqa: F821


def fee_rate_vix_clip(prior, raw):
    """Clip a VIX-formula rate to the movement band and the absolute corridor [S4].

    The band is +/-0.40% annualized against the prior quarter's rate (advisory class) and
    the corridor is [0.60%, 2.50%]. The second disclosed example clips to 1.82% against a
    prior rate of 1.42%.
    """
    lo = max(vix_corridor_lo, prior - vix_band)                      # noqa: F821
    hi = min(vix_corridor_hi, prior + vix_band)                      # noqa: F821
    return min(hi, max(lo, raw))


def phi_glwb_vix(k):
    """The VIX-formula GLWB charge rate in contract quarter k [S4][S6]."""
    if k <= 1:
        return phi_glwb_curr                                         # noqa: F821
    prior = phi_glwb_vix(k - 1)
    return fee_rate_vix_clip(
        prior, fee_rate_vix_raw(phi_glwb_curr, vix_sq(k)))           # noqa: F821


def phi_gmdb(t):
    """phi_D: the annual GMDB rider charge rate in force in month t.

    0.90% of the GMDB Benefit Base currently, guaranteed maximum 1.80% [S2][S3]. The
    ``basic`` death benefit is included at no charge [S1][S2], so the rate is zero there.
    """
    return 0.0 if gmdb_option() == "basic" else phi_gmdb_curr        # noqa: F821


def rollup_pct():
    """rho at election: 6.00% at age 69 or younger, 5.00% from 70 [S3]."""
    if age_at_entry() >= rollup_age_split:                           # noqa: F821
        return rollup_pct_old                                        # noqa: F821
    return rollup_pct_young                                          # noqa: F821


def rollup_rate(t):
    """rho(t): the GMDB roll-up percentage credited at the anniversary ending month t.

    ``fixed`` is the base run [S3]. ``cmt_linked`` is the Equitable formula rate: the
    10-year CMT plus 1.00%, or 1.50% before the first withdrawal, rounded to 0.10%,
    floored at 4% and capped at 8% [S7].
    """
    if rollup_rule() == "fixed":
        return rollup_pct()
    elif rollup_rule() == "cmt_linked":
        spread = cmt_spread if has_wd_by(t) else cmt_spread_predraw  # noqa: F821
        raw = cmt10(t) + spread
        step = cmt_round_step                                        # noqa: F821
        rounded = math.floor(raw / step + 0.5) * step                # noqa: F821
        return max(cmt_floor, min(cmt_cap, rounded))                 # noqa: F821
    else:
        raise ValueError("invalid rollup_rule")


def fee_glwb_pp_due(t):
    """Fee_G = (phi_G/4) x GWB at a Contract Quarterly Anniversary [S1][S3].

    The base is the **benefit base, not the account value** — putting the rider fee on
    account value is the most common and most consequential error on this product. The
    fee therefore rises as markets fall, until the account reaches zero, at which point
    it stops [S4].
    """
    if t < 1 or depleted_flag(t - 1) or not is_quarterly_anniv(t):
        return 0.0
    return (phi_glwb(t) / 4.0) * gwb_pp_at(t, "BEF_ANNIV")


def fee_gmdb_pp_due(t):
    """Fee_D = (phi_D/4) x RB at a Contract Quarterly Anniversary [S2][S3].

    The charge base is the GMDB Benefit Base; the quarterly frequency aligns it with the
    GLWB fee **[std]**, the research file recording quarterly for the GMWB family only.
    """
    if t < 1 or depleted_flag(t - 1) or not is_quarterly_anniv(t):
        return 0.0
    return (phi_gmdb(t) / 4.0) * rb_pp_at(t, "BEF_ANNIV")


def maint_fee_pp_due(t):
    """f_c: the $35 annual contract fee, waived at a contract value of $50,000 or more.

    Assessed at the Contract Anniversary and deducted proportionally across investment
    divisions [S2]. The waiver is tested on the contract value after the rider fees
    **[std]**, the notes placing the contract fee after them in the processing order.
    """
    if t < 1 or depleted_flag(t - 1) or not is_anniv(t):
        return 0.0
    after_riders = (av_pp_at(t, "BEF_FEE")
                    - fee_glwb_pp_due(t) - fee_gmdb_pp_due(t))
    return 0.0 if after_riders >= maint_fee_waiver_av else maint_fee  # noqa: F821


def charge_pp_due(t):
    """The total unit cancellation due at EOM before capping at the contract value."""
    return fee_glwb_pp_due(t) + fee_gmdb_pp_due(t) + maint_fee_pp_due(t)


def charge_scale(t):
    """The fraction of the charges due that the contract value can actually pay **[std]**.

    Charges are collected only up to the available contract value; the shortfall is not
    carried forward. This binds in at most one month per contract, the one in which the
    account is exhausted, and it is what makes :func:`check_av_roll_fwd` close there.
    """
    due = charge_pp_due(t)
    if due <= 0.0:
        return 0.0
    return min(1.0, av_pp_at(t, "BEF_FEE") / due)


def fee_glwb_pp(t):
    """The GLWB rider fee actually collected in month t."""
    return fee_glwb_pp_due(t) * charge_scale(t)


def fee_gmdb_pp(t):
    """The GMDB rider fee actually collected in month t."""
    return fee_gmdb_pp_due(t) * charge_scale(t)


def maint_fee_pp(t):
    """The annual contract fee actually collected in month t."""
    return maint_fee_pp_due(t) * charge_scale(t)


def charge_pp(t):
    """The total unit cancellation at EOM of month t: the two rider fees and f_c."""
    return charge_pp_due(t) * charge_scale(t)


def charge_income_pp(t):
    """Insurer charge income per contract in month t.

    The asset charge collected inside the unit value plus the charges collected by unit
    cancellation. The funds' own expense is **not** included — it is paid to the funds.
    """
    return asset_charge_pp(t) + charge_pp(t)


def gwb_pp_at(t, timing):
    """GWB at month t read at ``BEF_PREM``, ``BEF_WD`` or ``BEF_ANNIV`` [S1]."""
    if t < 1:
        return gwb_pp_init()
    if depleted_flag(t - 1):
        return gwb_pp(t - 1)
    g = gwb_pp(t - 1)
    if timing == "BEF_PREM":
        return g
    g = min(gwb_cap, g + prem_to_av_pp(t))                           # noqa: F821
    if timing == "BEF_WD":
        return g
    if wd_pp(t) > 0.0:
        if sum_wd_pp(t) <= wd_limit_pp(t):
            g = max(g - wd_pp(t), 0.0)
        else:
            g = max((g - wd_nonexcess_pp(t)) * excess_factor(t), 0.0)
    if timing == "BEF_ANNIV":
        return g
    raise ValueError("invalid timing")


def bb_pp_bef_anniv(t):
    """The Bonus Base carried into the anniversary events of month t [S1].

    Increased by net premium, set to ``min(GWB_after, BB_before)`` on an excess
    withdrawal, and otherwise unaffected by withdrawals. Applying the bonus does not
    change it.
    """
    if t < 1:
        return bb_pp_init()
    if depleted_flag(t - 1):
        return bb_pp(t - 1)
    b = min(gwb_cap, bb_pp(t - 1) + prem_to_av_pp(t))                # noqa: F821
    if wd_pp(t) > 0.0 and sum_wd_pp(t) > wd_limit_pp(t):
        b = min(gwb_pp_at(t, "BEF_ANNIV"), b)
    return b


def bonus_pp(t):
    """The GLWB bonus credited at the Contract Anniversary ending month t.

    ``b x BB`` if **no withdrawal was taken in the contract year** and the year is within
    the Bonus Period [S1]. *Any* withdrawal kills the whole year's bonus, including an
    automatic withdrawal or an RMD; pro-rating it for a partial year is wrong.
    """
    if not is_anniv(t) or depleted_flag(t - 1):
        return 0.0
    if policy_year(t) > bonus_end(t - 1) or is_wd_year(t):
        return 0.0
    return bonus_pct * bb_pp_bef_anniv(t)                            # noqa: F821


def gwb_pp_aft_bonus(t):
    """GWB after anniversary sub-step 3, the GLWB bonus."""
    return gwb_pp_at(t, "BEF_ANNIV") + bonus_pp(t)


def stepup_base_pp(t):
    """The contract value the step-up test is made against [S1][S3].

    ``annual_CV``: the Contract Value at the anniversary. ``highest_quarterly_CV``: the
    highest contract value over the four most recent Contract Quarterly Anniversaries.
    """
    basis = stepup_basis()
    if basis == "annual_CV":
        return av_pp(t)
    elif basis == "highest_quarterly_CV":
        return max(av_pp(t - 3 * j) for j in range(0, 4) if t - 3 * j >= 0)
    else:
        raise ValueError("invalid stepup_basis")


def is_stepup(t):
    """True when the anniversary step-up fires: the contract value exceeds the GWB [S1]."""
    return is_anniv(t) and stepup_base_pp(t) > gwb_pp_aft_bonus(t)


def gwb_pp_aft_stepup(t):
    """GWB after anniversary sub-step 4, the step-up.

    The **[std]** order — bonus first, then step-up — gives
    ``max(GWB_old + bonus, AV)``; the reverse gives ``max(GWB_old, AV) + bonus``, which
    is strictly more generous. The research file does not settle the interaction, and the
    choice made here follows the one design in the set that states it explicitly [S8].
    Treat the alternative as a first-order sensitivity, not a rounding issue.
    """
    return max(gwb_pp_aft_bonus(t), stepup_base_pp(t)) if is_anniv(t) else gwb_pp_aft_bonus(t)


def gwb_adj_year():
    """The contract year of the GWB Adjustment Date [S1].

    The later of the anniversary on or after the Designated Life's 70th birthday and the
    12th Contract Anniversary.
    """
    return max(gwb_adj_min_year, gwb_adj_age - age_at_entry())       # noqa: F821


def is_gwb_adj_date(t):
    """True at the Contract Anniversary that is the GWB Adjustment Date."""
    return is_anniv(t) and policy_year(t) == gwb_adj_year()


def adj_pp_bef_anniv(t):
    """ADJ carried into the anniversary events of month t [S1][S3].

    Initialized at 105% of net premium at endorsement, increased by ``s x P(1-tau)`` for
    premiums before the first anniversary after endorsement and by ``P(1-tau)`` for later
    ones, and **voided without value** by any earlier partial withdrawal.
    """
    if t < 1:
        return adj_pp_init()
    if has_wd_by(t):
        return 0.0
    rate = gwb_adj_pct if duration_mth(t) <= 12 else 1.0             # noqa: F821
    return adj_pp(t - 1) + rate * prem_to_av_pp(t)


def adj_pp(t):
    """ADJ(t): the GWB Adjustment amount at the end of month t; 0 once it terminates."""
    if t < 0:
        return 0.0
    if t == 0:
        return adj_pp_init() + gwb_adj_pct * prem_to_av_pp(0)        # noqa: F821
    if is_gwb_adj_date(t) or policy_year(t) > gwb_adj_year():
        return 0.0
    return adj_pp_bef_anniv(t)


def gwb_pp(t):
    """GWB(t): the Guaranteed Withdrawal Balance at the end of month t [S1].

    Anniversary sub-steps 5 to 7 finish here: the GWB Adjustment Date test, which raises
    the GWB to the Adjustment only if no withdrawal has ever been taken, and the
    $10,000,000 cap. In the depleted state the balance is run down by each payment when
    the For Life Guarantee is not in effect, and is left alone when it is.
    """
    if t < 0:
        return 0.0
    if t == 0:
        return min(gwb_cap, gwb_pp_init() + prem_to_av_pp(0))        # noqa: F821
    if depleted_flag(t - 1):
        g = gwb_pp(t - 1)
        return g if forlife_flag() else max(0.0, g - glwb_payment_pp(t))
    g = gwb_pp_aft_stepup(t)
    if is_gwb_adj_date(t) and not has_wd_by(t):
        g = max(g, adj_pp_bef_anniv(t))
    return min(gwb_cap, g)                                           # noqa: F821


def bb_pp(t):
    """BB(t): the Bonus Base at the end of month t [S1].

    A step-up sets it to ``max(GWB_after_step-up, BB_before)``; the bonus itself never
    changes it.
    """
    if t < 0:
        return 0.0
    if t == 0:
        return min(gwb_cap, bb_pp_init() + prem_to_av_pp(0))         # noqa: F821
    if depleted_flag(t - 1):
        return bb_pp(t - 1)
    b = bb_pp_bef_anniv(t)
    if is_stepup(t):
        b = max(gwb_pp_aft_stepup(t), b)
    return min(gwb_cap, b)                                           # noqa: F821


def bonus_end(t):
    """The contract year in which the Bonus Period ends [S1].

    Ten Contract Years from the endorsement effective date, **restarting** on each
    Bonus-Base-increasing step-up occurring on or before the anniversary following the
    Designated Life's 80th birthday. A hard-coded 10-year window from issue materially
    understates the guarantee in rising markets.
    """
    if t <= 0:
        return bonus_end_init() if is_inforce() else bonus_period_years  # noqa: F821
    prev = bonus_end(t - 1)
    if (is_stepup(t) and age_at_anniv(t) <= bonus_restart_age        # noqa: F821
            and gwb_pp_aft_stepup(t) > bb_pp_bef_anniv(t)):
        return policy_year(t) + bonus_period_years                   # noqa: F821
    return prev


def gawa_pct_fixed(t):
    """The GAWA% locked at the first withdrawal; 0 until then [S1].

    If the contract value reaches zero with the percentage not yet fixed, it is fixed at
    the percentage for the attained age at that moment [S1].
    """
    if t < 0:
        return 0.0
    if t == 0:
        return gawa_pct_init()
    prev = gawa_pct_fixed(t - 1)
    if prev > 0.0:
        return prev
    if is_first_wd(t) or depleted_flag(t):
        return gawa_pct_at_age(age(t))
    return 0.0


def gawa_pp_at(t, timing):
    """GAWA at month t read at ``BEF_PREM``, ``BEF_WD`` or ``BEF_ANNIV`` [S1]."""
    if t < 1:
        return gawa_pp_init()
    if depleted_flag(t - 1):
        return gawa_pp(t - 1)
    g = gawa_pp(t - 1)
    if timing == "BEF_PREM":
        return g
    if has_wd_by(t - 1) and prem_to_av_pp(t) > 0.0:
        g = g + gawa_pct_fixed(t - 1) * prem_to_av_pp(t)
    if timing == "BEF_WD":
        return g
    if is_first_wd(t):
        g = gawa_pct_at_age(age(t)) * gwb_pp_at(t, "BEF_WD")
    if wd_pp(t) > 0.0 and sum_wd_pp(t) > wd_limit_pp(t):
        g = min(g * excess_factor(t), gwb_pp_at(t, "BEF_ANNIV"))
    if timing == "BEF_ANNIV":
        return g
    raise ValueError("invalid timing")


def gawa_pp(t):
    """GAWA(t): the Guaranteed Annual Withdrawal Amount at the end of month t [S1].

    After the first withdrawal, both the bonus and the step-up raise it to
    ``max(g x GWB, GAWA)``. If the For Life Guarantee is not in effect and ``GWB < GAWA``
    at a Contract Year end, GAWA is set equal to GWB.
    """
    if t < 0:
        return 0.0
    if t == 0:
        return gawa_pp_init()
    if depleted_flag(t - 1):
        return gawa_pp(t - 1)
    g = gawa_pp_at(t, "BEF_ANNIV")
    if is_anniv(t):
        pct = gawa_pct_fixed(t)
        if has_wd_by(t) and pct > 0.0:
            if bonus_pp(t) > 0.0:
                g = max(pct * gwb_pp_aft_bonus(t), g)
            if is_stepup(t):
                g = max(pct * gwb_pp_aft_stepup(t), g)
        if not forlife_flag() and gwb_pp(t) < g:
            g = gwb_pp(t)
    if g <= 0.0 and depleted_flag(t) and gawa_pct_fixed(t) > 0.0:
        g = gawa_pct_fixed(t) * gwb_pp(t)
    return g


def np_pp(t):
    """NP(t): cumulative Net Premiums, a floor under the death benefit [S1].

    Updated by premium only, as the notes' state table has it: it is never reduced for a
    withdrawal. Under the ``rollup`` and ``HQAV`` elections it is therefore an unreduced
    floor beneath ``DB``. Under ``gmdb_option = "basic"`` the elected form is itself the
    proportional return of premium — carried on :func:`rb_pp`, which *does* fall with a
    withdrawal — and this cells is not layered over it, or the election would have no
    effect at all. See :func:`gmdb_guarantee_pp`.
    """
    if t < 0:
        return 0.0
    if t == 0:
        return np_pp_init() + prem_to_av_pp(0)
    if depleted_flag(t - 1):
        return np_pp(t - 1)
    return np_pp(t - 1) + prem_to_av_pp(t)


def rp_reduction_pp(t):
    """The premium portion of month t's withdrawal, earnings coming out first **[std]**.

    The sources state that Remaining Premium falls by "withdrawals of premium including
    withdrawal charges" [S2] and that earnings come out free first [S1], but give no
    algebra; this is the reading that makes the two consistent.
    """
    if t < 1 or wd_pp(t) <= 0.0:
        return 0.0
    rp = rp_pp(t - 1) + premium_pp(t)
    earnings = max(0.0, av_pp_at(t, "BEF_WD") - rp)
    return min(rp, max(0.0, wd_pp(t) - earnings))


def rp_pp(t):
    """RP(t): Remaining Premium, the basis the CDSC is charged on [S2]."""
    if t < 0:
        return 0.0
    if t == 0:
        return rp_pp_init() + premium_pp(0)
    if depleted_flag(t - 1):
        return rp_pp(t - 1)
    return max(0.0, rp_pp(t - 1) + premium_pp(t) - rp_reduction_pp(t))


def rb_prior_anniv_pp(t):
    """RB at the Contract Anniversary preceding month t, the d-f-d allowance base [S1]."""
    u = t_of_month(12 * (policy_year(t) - 1))
    return rb_pp(max(0, u))


def gmdb_allow_pp(t):
    """The contract year's dollar-for-dollar GMDB withdrawal allowance [S1].

    ``rho x RB`` at the previous anniversary. Withdrawals inside it reduce the Benefit
    Base dollar for dollar; anything above it reduces it proportionally.
    """
    return rollup_rate(t) * rb_prior_anniv_pp(t)


def gmdb_wd_dfd_pp(t):
    """The dollar-for-dollar portion of month t's withdrawal against the allowance [S1]."""
    if t < 1 or wd_pp(t) <= 0.0 or gmdb_option() != "rollup":
        return 0.0
    used = 0.0 if is_year_start(t) else gmdb_dfd_acc_pp(t - 1)
    return min(wd_pp(t), max(0.0, gmdb_allow_pp(t) - used))


def gmdb_wd_excess_pp(t):
    """The portion of month t's withdrawal above the GMDB d-f-d allowance [S1]."""
    if t < 1 or gmdb_option() != "rollup":
        return 0.0
    return wd_pp(t) - gmdb_wd_dfd_pp(t)


def gmdb_wd_factor(t):
    """The proportional factor month t's excess GMDB withdrawal accrues **[std]**.

    The notes say the adjustment above the allowance is "proportional to the contract
    value reduction from the excess" but leave the base unstated. The model measures it
    the same way the GLWB does: against the contract value after the dollar-for-dollar
    portion has been deducted.
    """
    if gmdb_wd_excess_pp(t) <= 0.0:
        return 1.0
    base = av_pp_at(t, "BEF_WD") - gmdb_wd_dfd_pp(t)
    if base <= 0.0:
        return 0.0
    return max(0.0, 1.0 - gmdb_wd_excess_pp(t) / base)


def gmdb_dfd_acc_pp(t):
    """The dollar-for-dollar reduction accrued so far in the contract year [S1].

    **GMDB withdrawal adjustments are applied at Contract Year end**, not at the
    withdrawal; applying them immediately changes the base the roll-up compounds on.
    """
    if t < 1:
        return 0.0
    prev = 0.0 if is_year_start(t) else gmdb_dfd_acc_pp(t - 1)
    return prev + gmdb_wd_dfd_pp(t)


def gmdb_factor_acc(t):
    """The proportional factor accrued so far in the contract year **[std]**."""
    if t < 1:
        return 1.0
    prev = 1.0 if is_year_start(t) else gmdb_factor_acc(t - 1)
    return prev * gmdb_wd_factor(t)


def rb_pp_at(t, timing):
    """RB at month t read at ``BEF_PREM``, ``BEF_WD`` or ``BEF_ANNIV``.

    The ``rollup`` form accrues its withdrawal adjustment and applies it at the Contract
    Year end; the ``HQAV`` and ``basic`` forms reduce the base proportionally at the
    withdrawal itself [S1].
    """
    if t < 1:
        return rb_pp_init()
    if depleted_flag(t - 1):
        return rb_pp(t - 1)
    r = rb_pp(t - 1)
    if timing == "BEF_PREM":
        return r
    r = r + prem_to_av_pp(t)
    if timing == "BEF_WD":
        return r
    if wd_pp(t) > 0.0 and gmdb_option() != "rollup":
        base = av_pp_at(t, "BEF_WD")
        r = r * max(0.0, 1.0 - wd_pp(t) / base) if base > 0.0 else 0.0
    if timing == "BEF_ANNIV":
        return r
    raise ValueError("invalid timing")


def rb_pp(t):
    """RB(t): the GMDB Benefit Base at the end of month t.

    Growth cutoffs are **age-based, not duration-based**: roll-up and ratchet growth stop
    at the Contract Anniversary preceding the oldest Covered Life's 81st birthday [S1],
    so an issue-age-60 cell gets 20 roll-up credits and an issue-age-75 cell gets 5.
    """
    if t < 0:
        return 0.0
    if t == 0:
        return rb_pp_init() + prem_to_av_pp(0)
    if depleted_flag(t - 1):
        return rb_pp(t - 1)
    r = rb_pp_at(t, "BEF_ANNIV")
    if not is_anniv(t):
        return r
    option = gmdb_option()
    if option == "rollup":
        r = max(0.0, (r - gmdb_dfd_acc_pp(t)) * gmdb_factor_acc(t))
        if age_at_anniv(t) <= gmdb_growth_cutoff_age:                # noqa: F821
            r = r * (1.0 + rollup_rate(t))
    elif option == "HQAV":
        if age_at_anniv(t) <= gmdb_growth_cutoff_age:                # noqa: F821
            r = max(r, av_pp(t))
    elif option == "basic":
        pass
    else:
        raise ValueError("invalid gmdb_option")
    return r


def gmdb_guarantee_pp(t):
    """The guarantee actually floored under the death benefit [S1].

    ``max(NP(t), RB(t))`` under the ``rollup`` and ``HQAV`` elections, exactly as the
    notes' ``DB = max(AV, NP, RB)`` reads: there ``NP`` is the *included* return of
    premium and ``RB`` the separately elected base, and the two are different guarantees.

    Under ``basic`` they are the **same** guarantee — the elected form *is* the return of
    premium — and the notes' two tables then contradict each other. The GMDB form table
    reduces it ``G <- G x (1 - W/AV_pre)``, "proportional, **not** dollar-for-dollar",
    while the state table updates ``NP`` by premium alone. Layering the unreduced ``NP``
    over the reduced base would make the emphasized rule unreachable and the election a
    dead switch, so on that election the elected form governs alone **[std]**. The
    README section *The basic GMDB election and the unreduced NP floor* sets out the
    conflict and the choice; :func:`np_pp` still carries cumulative net premiums, and a
    test pins the difference on model point 9.
    """
    if gmdb_option() == "basic":
        return rb_pp(t)
    return max(np_pp(t), rb_pp(t))


def db_pp(t):
    """DB(t) = max(AV(t), NP(t), RB(t)): the **gross** death benefit outflow [S1].

    Zero once the contract value has reached zero with the GLWB in force: all other
    endorsements terminate without value and **no death benefit is payable on subsequent
    death** [S1].
    """
    if depleted_flag(t):
        return 0.0
    return max(av_pp(t), gmdb_guarantee_pp(t))


def gmdb_claim_pp(t):
    """``max(0, max(NP, RB) - AV)``: the **net general-account strain** on death [S1].

    Project ``DB(t)`` as the outflow and derive this as the strain — never the reverse,
    never both. Projecting only the guarantee excess understates gross benefit outgo and
    breaks reconciliation with statutory exhibits; projecting both double counts.
    """
    if depleted_flag(t):
        return 0.0
    return max(0.0, gmdb_guarantee_pp(t) - av_pp(t))


def forlife_flag():
    """Whether the For Life Guarantee is in effect from issue [S1].

    True when the Designated Life is 59 1/2 or older. On an age-nearest-birthday basis an
    ANB of 60 is exactly an actual age of 59 1/2 or more, so the test is
    ``age_at_entry() >= 60`` with no approximation **[std]**.
    """
    return age_at_entry() >= forlife_age                             # noqa: F821


def depleted_flag(t):
    """True once the contract value has reached zero with the GLWB in force [S1].

    Absorbing: once set it never clears. The threshold is half a cent **[std]** — the
    charge cap in :func:`charge_scale` and the withdrawal cap in :func:`wd_pp` both drive
    the account to exactly zero, so the threshold only guards floating point.
    """
    if t < 0:
        return False
    if t > 0 and depleted_flag(t - 1):
        return True
    return av_pp(t) <= av_depletion_threshold                        # noqa: F821


def glwb_payment_pp(t):
    """The insurer-funded GLWB payment in month t once the contract is depleted [S1].

    With the For Life Guarantee in effect, GAWA is paid for the life of the Designated
    Life. Without it, payments continue until the earlier of death and GWB depletion, the
    final one truncated to the remaining GWB. The notes place the routine at BOM and the
    payment "at each Contract Anniversary"; the model pays it at the BOM of the first
    month of each contract year **[std]**, the instant just after the anniversary, which
    keeps it on the same clock as the pre-depletion withdrawals.
    """
    if t < 1 or t > proj_len() or not depleted_flag(t - 1):
        return 0.0
    if not is_year_start(t):
        return 0.0
    amount = gawa_pp(t - 1)
    return amount if forlife_flag() else min(amount, gwb_pp(t - 1))


def mort_rate(t):
    """The annual mortality rate at the attained age and sex, from *mort_table.csv*.

    The shipped table is an illustrative annuitant curve **[std]**, *not* a published
    basis. The prescribed basis is the 2012 IAM **Basic** Table improved to December 31,
    2017 on Projection Scale G2, generational, with no further improvement in the
    projection [R1][REG-R59]; it may not be redistributed here, so swap it in by
    repointing ``Data.mort_table_file``. **Do not use CSO or VBT life tables** —
    annuitant mortality is a different and generally lighter basis [REG-R59].
    """
    table = data.mort_table()                                        # noqa: F821
    top = max(a for a, s in table.index)
    return float(table.loc[(min(age(t), top), sex()), "mort_rate"])


def mort_rate_mth(t):
    """q^d(t): the monthly mortality rate, ``1 - (1 - q_x)^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """q^w_base(y): VM-21 Table 6.3's "under 50% ITM" column **[std]** [R1].

    4.0% p.a. during the surrender-charge period (contract years 1 to 7 here [S2]),
    25.0% in the first year after it, 15.0% thereafter.
    """
    year = policy_year(t)
    if year <= surr_charge_years:                                    # noqa: F821
        return lapse_rate_sc                                         # noqa: F821
    elif year == surr_charge_years + 1:                              # noqa: F821
        return lapse_rate_shock                                      # noqa: F821
    return lapse_rate_ult                                            # noqa: F821


def moneyness_glwb(t):
    """M_G(t) = GWB(t) / AV(t): the living-benefit in-the-moneyness ratio [R1]."""
    return gwb_pp(t) / av_pp(t) if av_pp(t) > 0.0 else 0.0


def moneyness_gmdb(t):
    """M_D(t) = max(NP(t), RB(t)) / AV(t): the death-benefit moneyness ratio [R1].

    Measured on the guarantee actually floored under ``DB``, not on ``RB`` alone.
    """
    return gmdb_guarantee_pp(t) / av_pp(t) if av_pp(t) > 0.0 else 0.0


def lapse_itm_mult(m):
    """lambda(M): the VM-21 §7.B.1 Alternative Methodology multiplier [R1].

    ``min[U, max(L, 1 - Mult (M - D))]`` with U = 1.00, L = 0.50, Mult = 1.25, D = 1.10 —
    the only closed-form dynamic lapse formula the Valuation Manual publishes for VAs.
    Note that it floors suppression at 50% while Table 6.3's own ITM grading implies an
    84% suppression; compose one or the other, never both.
    """
    raw = 1.0 - lapse_itm_mult_coef * (m - lapse_itm_threshold)      # noqa: F821
    return min(lapse_itm_upper, max(lapse_itm_lower, raw))           # noqa: F821


def lapse_dyn_mult(t):
    """lambda*(t) = min(lambda(M_G), lambda(M_D)) [R1].

    The contract carries both a VAGLB and a GMDB, and VM-21 §6.C.6 directs that such
    contracts use the **lower** of the two ITM-based rates.
    """
    return min(lapse_itm_mult(moneyness_glwb(t)),
               lapse_itm_mult(moneyness_gmdb(t)))


def lapse_wd_factor(t):
    """kappa(t): 0.60 in any contract year with a projected withdrawal, else 1.00 [R1]."""
    return lapse_wd_year_factor if is_wd_year(t) else 1.0            # noqa: F821


def lapse_rate(t):
    """q^w_annual(t) = min[1, base x lambda* x kappa] **[std] composition** [R1].

    The **annual** total surrender rate; :func:`lapse_rate_mth` is the monthly one, the
    pair matching :func:`mort_rate` / :func:`mort_rate_mth`. Zero whenever the contract
    value is zero: the prescribed surrender assumption for a GMWB contract at ``AV = 0``
    is 0% [R1]. This is the single most important behavioural assumption on the product,
    because it determines how many deeply in-the-money contracts persist to become
    claims.
    """
    if av_pp(t) <= 0.0:
        return 0.0
    return min(1.0, lapse_rate_base(t) * lapse_dyn_mult(t) * lapse_wd_factor(t))


def lapse_rate_mth(t):
    """q^w(t): the monthly surrender rate, ``1 - (1 - q^w_annual)^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """The in-force probability at the **start** of projection month t.

    The notes' ``l(t-1)``, and the weight applied to month ``t``'s cash flows, so that
    the ``pols_if`` column of :func:`result_cf` reconciles with the row it sits on:
    ``premiums(t) / premium_pp(t)`` is exactly ``pols_if(t)``. This is the library-wide
    convention, set by :mod:`.Term_US_A` and by ``savings.CashValue_SE``.

    The notes' own end-of-month ``l(t)`` is :func:`pols_if_at` ``(t, "AFT_DECR")``. The
    two coincide — ``pols_if(t + 1) == pols_if_at(t, "AFT_DECR")`` — everywhere but the
    horizon month, where the survivors leave as :func:`pols_maturity` and nothing is in
    force at the start of the month after it.
    """
    if t <= 0:
        return pols_if_init()
    if t > proj_len():
        return 0.0
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """In-force at month t read at ``BEF_DECR``, ``BEF_LAPSE`` or ``AFT_DECR``.

    The order is the notes' ``l(t) = l(t-1)(1 - q^d(t))(1 - q^w(t))`` — **death first,
    then surrender** **[std]**. ``"BEF_DECR"`` is :func:`pols_if` ``(t)`` and
    ``"AFT_DECR"`` is the notes' ``l(t)``, the end-of-month count.
    """
    if t < 1:
        return pols_if_init()
    pols = pols_if(t)
    if timing == "BEF_DECR":
        return pols
    pols = pols * (1.0 - mort_rate_mth(t))
    if timing == "BEF_LAPSE":
        return pols
    pols = pols * (1.0 - lapse_rate_mth(t))
    if timing == "AFT_DECR":
        return pols
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in month t, on the contracts in force at the start of it."""
    return 0.0 if t < 1 else pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Full surrenders in month t, on the survivors of mortality."""
    return 0.0 if t < 1 else pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_maturity(t):
    """Survivors carried out at the projection horizon; zero in every other month.

    Not a decrement — the projection runs out — but needed for the in-force roll-forward
    to close; see the Space docstring.
    """
    return pols_if_at(t, "AFT_DECR") if t == proj_len() else 0.0


def pols_decr(t, kind):
    """The number of contracts leaving in month t by benefit ``kind``."""
    if kind == "DEATH":
        return pols_death(t)
    elif kind == "LAPSE":
        return pols_lapse(t)
    elif kind == "MATURITY":
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def claim_pp(t, kind):
    """The benefit paid per contract in month t by ``kind``.

    ``"DEATH"`` is the gross death benefit :func:`db_pp`. ``"LAPSE"`` is the surrender
    proceeds :func:`surr_benefit_pp`. ``"MATURITY"`` is the surrender value of the
    survivors at the projection horizon.
    """
    if kind == "DEATH":
        return db_pp(t)
    elif kind == "LAPSE":
        return surr_benefit_pp(t)
    elif kind == "MATURITY":
        return surr_benefit_pp(t)
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The contract value released per contract by a claim of ``kind``.

    Always ``AV(t)``: the separate account gives up the account value, and whatever the
    guarantee adds on top is general-account money, reported as :func:`claims_over_av`.
    """
    if kind in ("DEATH", "LAPSE", "MATURITY"):
        return av_pp(t)
    raise ValueError("invalid kind")


def premiums(t):
    """Premium income in month t, weighted by the contracts in force at the start of it.

    ``pols_if(0)`` is ``pols_if_init()``, so the entry instant needs no special case.
    """
    return 0.0 if t < 0 else premium_pp(t) * pols_if(t)


def prem_to_av(t):
    """Net premium credited to the block's contract value in month t."""
    return 0.0 if t < 0 else prem_to_av_pp(t) * pols_if(t)


def asset_charges(t):
    """Charge income from the M&E and administrative asset charge, in-force weighted."""
    return 0.0 if t < 1 else asset_charge_pp(t) * pols_if(t)


def fees_glwb(t):
    """Charge income from the GLWB rider fee, in-force weighted."""
    return 0.0 if t < 1 else fee_glwb_pp(t) * pols_if(t)


def fees_gmdb(t):
    """Charge income from the GMDB rider fee, in-force weighted."""
    return 0.0 if t < 1 else fee_gmdb_pp(t) * pols_if(t)


def maint_fees(t):
    """Charge income from the annual contract fee, in-force weighted."""
    return 0.0 if t < 1 else maint_fee_pp(t) * pols_if(t)


def wd_charges(t):
    """The CDSC collected on withdrawals, in-force weighted — a **memo line**.

    The notes' ledger lists the withdrawal charge twice: once as charge income ``c(t)``
    and once as a deduction inside withdrawal proceeds ``W(t) - c(t)``. Counting both
    double-counts it. :func:`withdrawals` carries the net proceeds into :func:`net_cf`
    and this line reports the charge separately.
    """
    return 0.0 if t < 1 else wd_charge_pp(t) * pols_if(t)


def charge_income(t):
    """Total insurer charge income in month t, excluding the double-counted CDSC."""
    return asset_charges(t) + fees_glwb(t) + fees_gmdb(t) + maint_fees(t)


def withdrawals(t):
    """Withdrawal proceeds ``W(t) - c(t)``, weighted by :func:`pols_if` ``(t)``."""
    return 0.0 if t < 1 else wd_payment_pp(t) * pols_if(t)


def glwb_payments(t):
    """Insurer-funded post-depletion GLWB payments, weighted by ``pols_if(t)``."""
    return 0.0 if t < 1 else glwb_payment_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, for one ``kind`` or, with ``kind=None``, all three."""
    if kind is None:
        return (claims(t, "DEATH") + claims(t, "LAPSE")
                + claims(t, "MATURITY"))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The contract value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind=None):
    """Benefit paid less the contract value released, ``claims - claims_from_av``.

    On death this is exactly the GMDB guarantee claim — the general-account strain. On a
    surrender it is negative by the withdrawal charge, which the separate account keeps.
    A reconciliation quantity, never a ledger line of its own.
    """
    if kind is None:
        return (claims_over_av(t, "DEATH") + claims_over_av(t, "LAPSE")
                + claims_over_av(t, "MATURITY"))
    return claims(t, kind) - claims_from_av(t, kind)


def gmdb_claims(t):
    """The net general-account strain on death, ``GuaranteeClaim x deaths`` — a memo."""
    return 0.0 if t < 1 else gmdb_claim_pp(t) * pols_death(t)


def commissions(t):
    """Acquisition commission; **0 in the base run [std]**, the notes not modelling it."""
    return comm_rate_acq * premiums(t)                               # noqa: F821


def premium_taxes(t):
    """Premium tax deducted from the purchase payment, 0% **[std]** [S2]."""
    return premium_tax_rate() * premiums(t)


def inflation_factor(t):
    """The VM-21 §6.C.2 expense inflation factor for the contract year containing t.

    ``1.025^(valuation year - 2015 + completed contract years)`` [R1].
    """
    return (1.0 + inflation_rate) ** (                               # noqa: F821
        valuation_year - expense_base_year + duration(t))            # noqa: F821


def expenses(t):
    """VM-21 §6.C.2 prescribed maintenance expense [R1].

    ``[100 x 1.025^(valuation year - 2015)]/12`` per contract per month, inflating 2.5%
    a year, **plus 7 basis points of projected account value** for a company-administered
    block. Acquisition expense is not modelled in the base run **[std]**.
    """
    if t == 0:
        return expense_acq * pols_if(0)                              # noqa: F821
    if t < 0 or t > proj_len():
        return 0.0
    per_contract = (expense_maint / 12.0) * inflation_factor(t)      # noqa: F821
    per_av = (expense_av_rate / 12.0) * av_pp(t)                     # noqa: F821
    return (per_contract + per_av) * pols_if(t)


def net_cf(t):
    """The technical notes' cash flow ledger, summed with the notes' own signs.

    Premium income and every charge income line are positive; the gross death benefit,
    surrender and horizon proceeds, withdrawal proceeds, post-depletion GLWB payments and
    maintenance expense are negative. Note what this **is not**: because a VA's separate
    account is legally segregated, this line mixes separate-account movements (premium
    in, benefits out) with transfers into the general account (the charges), and it omits
    investment return entirely, so it does not reconcile to the account value.
    :func:`net_cf_ga` is the insurer's own view; :func:`check_av_roll_fwd` is the
    account-value identity.
    """
    return (premiums(t) + charge_income(t)
            - withdrawals(t) - glwb_payments(t) - claims(t)
            - expenses(t) - commissions(t) - premium_taxes(t))


def net_cf_ga(t):
    """The general-account view: charge income less guarantee strain and expenses.

    The notes require both the gross death benefit and the net general-account strain and
    say they are not interchangeable. This line assembles the net one: charge income,
    less the GMDB guarantee claim, less insurer-funded post-depletion GLWB payments, less
    expenses, commissions and premium tax. It is the memo, not the ledger.
    """
    return (charge_income(t) - gmdb_claims(t) - glwb_payments(t)
            - expenses(t) - commissions(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted contract value at month t; see :func:`av_pp_at`.

    Every timing inside the month is weighted by the contracts in force at the start of
    it, :func:`pols_if` ``(t)``. ``"EOM"`` is weighted by ``pols_if(t + 1)`` — the count
    still in force once the month's decrements have gone — which is zero in the horizon
    month, where the survivors leave as :func:`pols_maturity` and their contract value
    is released through :func:`claims_from_av`.
    """
    if t < 0:
        return 0.0
    if timing == "EOM":
        return av_pp(t) * pols_if(t + 1)
    return av_pp_at(t, timing) * pols_if(t)


def inv_income(t):
    """Investment income credited to the block's contract value in month t."""
    return 0.0 if t < 1 else inv_income_pp(t) * pols_if(t)


def wd_from_av(t):
    """The contract value released by month t's withdrawals, gross of the charge."""
    return 0.0 if t < 1 else wd_pp(t) * pols_if(t)


def charges_from_av(t):
    """The contract value cancelled by month t's per-contract and benefit-base charges."""
    return 0.0 if t < 1 else charge_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's contract value over month t."""
    return av_at(t, "EOM") - av_at(t - 1, "EOM")


def check_av_roll_fwd_resid(t):
    """Contract value roll-forward residual; zero to floating point for every t >= 1.

    ``AV(t) - AV(t-1) = net premium in - withdrawals out + investment income net of the
    per-unit charges - the charges collected by unit cancellation - the contract value
    released by each claim kind``. The cash *paid* on a death may exceed the contract
    value released; that excess is :func:`claims_over_av` and is not part of this
    identity. ``t = 0`` is the entry instant and is excluded.

    The signed residual, for a debugging session that wants to know *where* the identity
    fails; :func:`check_av_roll_fwd` is the library-wide boolean over all ``t``.
    """
    if t < 1:
        return 0.0
    expected = (prem_to_av(t) - wd_from_av(t) + inv_income(t)
                - charges_from_av(t)
                - claims_from_av(t, "DEATH") - claims_from_av(t, "LAPSE")
                - claims_from_av(t, "MATURITY"))
    return av_change(t) - expected


def check_av_roll_fwd():
    """True when the contract value roll-forward closes at **every** projected month.

    No argument and a ``bool`` return, following ``savings.CashValue_SE`` and the
    library-wide convention, so one test can call the same check across every model.
    The per-month signed residual is :func:`check_av_roll_fwd_resid`; the tolerance is
    1e-6 of a currency unit on a contract value of order 1e5.
    """
    return all(abs(check_av_roll_fwd_resid(t)) < 1e-6
               for t in range(1, proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual; zero to floating point for every t >= 1.

    ``pols_if(t) - pols_if(t+1) = deaths + surrenders + horizon survivors``, written on
    the start-of-month counts :func:`pols_if` carries. In the horizon month
    ``pols_if(t+1)`` is zero and :func:`pols_maturity` absorbs the survivors.
    """
    if t < 1:
        return 0.0
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes at **every** projected month.

    No argument and a ``bool`` return; :func:`check_pols_roll_fwd_resid` is the signed
    per-month residual. In-force is a probability of order 1, so the tolerance is 1e-12.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) < 1e-12
               for t in range(1, proj_len() + 1))


def check_charge_split_resid(t):
    """Residual of the investment identity; zero to floating point for every t >= 1.

    ``gross fund return = fund expense + asset charge + the change in AV from
    investment``. It is the guard against the charge-base confusion the notes call the
    most consequential error on this product: M&E and admin are on **account value**, the
    rider fees on **benefit bases**, the contract fee **per contract** and the CDSC on
    **Remaining Premium** — four bases in one stack.
    """
    if t < 1:
        return 0.0
    return (gross_inv_income_pp(t) - fund_expense_pp(t)
            - asset_charge_pp(t) - inv_income_pp(t))


def check_charge_split():
    """True when the investment identity closes at **every** projected month.

    No argument and a ``bool`` return; :func:`check_charge_split_resid` is the signed
    per-month residual, measured per contract, so the tolerance is 1e-8.
    """
    return all(abs(check_charge_split_resid(t)) < 1e-8
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by projection month t from 0 to ``proj_len()``.

    ``t = 0`` carries the purchase payment, as the notes' ledger indexes it. The
    ``pols_if`` column is the count in force at the **start** of each month and is the
    weight carried by every cash flow on that row, so the two reconcile.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "asset_charges": [asset_charges(t) for t in ts],
            "fees_glwb": [fees_glwb(t) for t in ts],
            "fees_gmdb": [fees_gmdb(t) for t in ts],
            "maint_fees": [maint_fees(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "glwb_payments": [glwb_payments(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, indexed by projection month t.

    ``pols_if`` opens the month, the three decrement columns take contracts out of it,
    and ``pols_if_aft_decr`` — the notes' ``l(t)`` — closes it. Rows therefore read
    across: ``pols_if - pols_death - pols_lapse - pols_maturity`` is the next row's
    ``pols_if``.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, "AFT_DECR") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of per-contract subaccount and contract values, indexed by t.

    One ``sa_pp_<i>`` column per subaccount, then the worked example's own columns: the
    contract value before the charges, the three charges, and the end-of-month value.
    """
    ts = list(range(0, proj_len() + 1))
    cols = {}
    for i in sub_ids():
        cols["sa_pp_%s" % i] = [sa_pp(t, i) for t in ts]
    cols["av_pp_bef_fee"] = [av_pp_at(t, "BEF_FEE") for t in ts]
    cols["fee_glwb_pp"] = [fee_glwb_pp(t) for t in ts]
    cols["fee_gmdb_pp"] = [fee_gmdb_pp(t) for t in ts]
    cols["maint_fee_pp"] = [maint_fee_pp(t) for t in ts]
    cols["asset_charge_pp"] = [asset_charge_pp(t) for t in ts]
    cols["fund_expense_pp"] = [fund_expense_pp(t) for t in ts]
    cols["av_pp"] = [av_pp(t) for t in ts]
    cols["surr_benefit_pp"] = [surr_benefit_pp(t) for t in ts]
    return pd.DataFrame(cols, index=pd.Index(ts, name="t"))          # noqa: F821


def result_bases():
    """Result table of the guarantee bases and moneyness ratios, indexed by t."""
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "gwb_pp": [gwb_pp(t) for t in ts],
            "gawa_pp": [gawa_pp(t) for t in ts],
            "bb_pp": [bb_pp(t) for t in ts],
            "rb_pp": [rb_pp(t) for t in ts],
            "np_pp": [np_pp(t) for t in ts],
            "rp_pp": [rp_pp(t) for t in ts],
            "adj_pp": [adj_pp(t) for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "gmdb_claim_pp": [gmdb_claim_pp(t) for t in ts],
            "moneyness_glwb": [moneyness_glwb(t) for t in ts],
            "moneyness_gmdb": [moneyness_gmdb(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

rate_sheet_date = "2026-04-27"

asset_charge_me = 0.01

asset_charge_admin = 0.003

phi_glwb_curr = 0.0125

phi_glwb_max = 0.03

phi_gmdb_curr = 0.009

phi_gmdb_max = 0.018

fee_increase_max = 0.0025

fee_reset_years = 5

maint_fee = 35.0

maint_fee_waiver_av = 50000.0

free_wd_rate = 0.1

surr_charge_years = 7

bonus_pct = 0.06

bonus_period_years = 10

bonus_restart_age = 81

gwb_cap = 10000000.0

gwb_adj_pct = 1.05

gwb_adj_age = 70

gwb_adj_min_year = 12

rollup_pct_young = 0.06

rollup_pct_old = 0.05

rollup_age_split = 70

gmdb_growth_cutoff_age = 80

forlife_age = 60

av_depletion_threshold = 0.005

lapse_rate_sc = 0.04

lapse_rate_shock = 0.25

lapse_rate_ult = 0.15

lapse_itm_upper = 1.0

lapse_itm_lower = 0.5

lapse_itm_mult_coef = 1.25

lapse_itm_threshold = 1.1

lapse_wd_year_factor = 0.6

vix_fee_coef = 0.0005

vix_divisor = 33.0

vix_offset = 10.0

vix_band = 0.004

vix_corridor_lo = 0.006

vix_corridor_hi = 0.025

cmt_spread = 0.01

cmt_spread_predraw = 0.015

cmt_round_step = 0.001

cmt_floor = 0.04

cmt_cap = 0.08

expense_maint = 100.0

expense_base_year = 2015

valuation_year = 2026

expense_av_rate = 0.0007

inflation_rate = 0.025

expense_acq = 0.0

comm_rate_acq = 0.0

math = ("Module", "math")

pd = ("Module", "pandas")