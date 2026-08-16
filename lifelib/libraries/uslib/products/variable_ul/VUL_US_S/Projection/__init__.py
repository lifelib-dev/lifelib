# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.VUL_US_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_av()          # the worked-example anchor cell
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/variable_ul/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VUL_US_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers live in the unparameterized :mod:`~.VUL_US_S.Data` Space, reached here
through the ``data`` Reference, so each file is read once per model rather than once
per model point:

======================  ================================  ==========================
Reference (on Data)     Cells                             File
======================  ================================  ==========================
model_point_file        data.model_point_table()          model_point_table.csv
subaccount_file         data.subaccount_table()           subaccount_table.csv
scenario_file           data.scenario_table()             scenario_table.csv
coi_rates_file          data.coi_rates()                  coi_rates.csv
corridor_file           data.corridor_factors()           corridor_factors.csv
mort_table_file         data.mort_table()                 mort_table.csv
class_factor_file       data.class_factor_table()         class_factor_table.csv
lapse_table_file        data.lapse_table()                lapse_table.csv
prem_persistency_file   data.prem_persistency_table()     prem_persistency.csv
surr_charge_file        data.surr_charge_table()          surr_charge_table.csv
======================  ================================  ==========================

.. rubric:: Projection basis

``t`` counts **policy months**, 1-based: ``t = 1`` is the issue month of a new-business
model point, and for an in-force point it is the first projected month, sitting
``duration_mth_init()`` completed months after issue. State variables the notes define
at ``t = 0`` -- ``SA_i(0)``, ``FA(0)``, ``LA(0)``, ``D(0)``, ``F(0)``, ``l(0) = 1`` --
are the ``t == 0`` branch of the corresponding recursion.

Within each month the notes' monthiversary order is followed exactly:

1. advance the policy year, the attained age and the year-dependent parameters -- the
   loan tier (:func:`loan_rate_ann`), the surrender charge (:func:`surr_charge_rate`)
   and the corridor factor (:func:`corridor_factor`);
2. gross premium and its load, the net premium allocated by :func:`alloc` and
   :func:`alloc_fixed` (:func:`premium_pp`, :func:`prem_to_av_pp`);
3. withdrawal and the $25 fee, taken pro rata from the unloaned accounts, and under
   Option A the proportionate face reduction they force (:func:`wd_pp`,
   :func:`wd_fee_pp`, :func:`face_reduction_pp`, :func:`sum_assured_at`) -- after which
   the account value is :func:`av_pp_at(t, "BEF_FEE")<av_pp_at>`, the notes'
   post-premium value;
4. loan activity -- not modeled; the opening debt and collateral roll forward;
5. death benefit and the GPT corridor test (:func:`db_pp`), then the net amount at
   risk (:func:`net_amt_at_risk`), **with no one-month discount**;
6. the monthly deduction (:func:`mth_deduction_pp`), allocated across the unloaned
   accounts pro rata (:func:`mth_deduction_sa_pp`, :func:`mth_deduction_fa_pp`);
7. growth over the month: the separate-account unit-value factor
   (:func:`inv_return_mth`), fixed-option interest (:func:`fixed_return_mth`), loan
   account interest (:func:`loan_cr_rate_mth`) and debt accrual
   (:func:`loan_rate_mth`);
8. end of month: the death benefit and net amount at risk recomputed on end-of-month
   balances (:func:`db_pp_eom`, :func:`net_amt_at_risk_eom`), then the decrements,
   death before lapse (:func:`pols_death`, :func:`pols_lapse`);
9. the default test (:func:`is_default`) -- a diagnostic; see the model docstring.

Cash flows are **undiscounted**. Premiums, expenses and percent-of-premium expenses
fall at BOM and are weighted by ``pols_if(t)``; death claims by
``pols_if(t) * mort_rate_mth(t)``; surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``.

.. rubric:: Two views of the same run

The notes require two reports and warn that confusing them is "a common specification
error". :func:`result_cf` is the **gross (policyholder) view**: the insurer's liability
outflow on death is the *full death benefit less policy debt*, and the account value
seized is the *funding* of part of it. :func:`result_net` is the **net-of-account
(general-account strain) view**, derived arithmetically from the same run: the margins
collected (premium loads, monthly deductions, M&E, loan spread, surrender charges) less
the net mortality cost :func:`claims_net`, which is the net amount at risk. Projecting
``DB - AV`` as the claim understates gross benefit outgo; projecting the full death
benefit *and* separately expensing the net amount at risk double counts.
:func:`check_net_view` pins the two views to each other.

.. rubric:: Naming

Cells names follow :mod:`.UL_US_S` -- the universal-life chassis this product is
built on -- and through it lifelib's ``basiclife.BasicTerm_S`` and
``savings.CashValue_SE``: ``pols_*`` for policy counts, ``av_*`` for account values,
plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``timing`` and ``kind`` string arguments. Names are added only where variable UL has a
concept fixed universal life does not: the subaccount vector, the fixed option, the
loan account, the M&E charge, the return scenario, the funding ratio and the pricing
path. The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Policy month, 1-based
(policy year)              policy_year(t)                  Policy year, 1-based
(t - 1 in months)          duration_mth(t)                 Completed policy months
(completed years)          duration(t)                     Completed policy years
(issue age)                age_at_entry                    Issue age (ANB)
x_t                        age(t)                          Attained age (ANB)
(none)                     proj_len                        Last projected month
F_0                        sum_assured                     Initial face amount
F_t                        sum_assured_at(t)               Face after reductions
(F_0 / 1000)               units                           Initial face in $1,000s
i (subaccount index)       subaccount_ids                  The subaccount lineup
alpha_i                    alloc(i)                        Allocation to subaccount i
alpha_F                    alloc_fixed                     Allocation to fixed option
e_i                        fund_expense_ann(i)             Fund expense ratio (annual)
m                          me_rate_ann                     M&E rate (annual)
r_{i,t}                    gross_return_mth(t, i)          Gross subaccount return
(net unit-value return)    inv_return_mth(t, i)            (1+r)(1-e/12)(1-m/12) - 1
i_fix                      crediting_rate_ann(t)           Declared fixed rate
(monthly fixed rate)       fixed_return_mth(t)             (1+i_fix)^(1/12) - 1
(fixed floor)              guar_rate_ann                   1.0% fixed-option floor
i_L                        loan_rate_ann(t)                Loan rate charged
i_C                        loan_cr_rate_ann(t)             Loan rate credited
P_t                        premium_pp(t)                   Premium paid per policy
(planned)                  premium_pp_ann                  Planned annual premium
rho_t                      prem_persistency(t)             Premium persistency
rho^base_t                 prem_persistency_base(t)        Base persistency factor
gamma                      load_prem_rate                  Premium load rate
(net premium)              prem_to_av_pp(t)                Net premium to the accounts
W(t)                       wd_pp(t)                        Partial withdrawal
(withdrawal fee)           wd_fee_pp(t)                    $25 withdrawal fee
(face cut)                 face_reduction_pp(t)            Option A face reduction
SA_{i,t}                   sa_pp(t, i)                     Subaccount value, EOM
SA'_{i,t}                  sa_pp_at(t, i, "BEF_INV")       Subaccount post-deduction
FA_t                       fa_pp(t)                        Fixed-option value, EOM
LA_t                       la_pp(t)                        Loan-account collateral
D_t                        loan_bal_pp(t)                  Outstanding policy debt
AV_t                       av_pp(t)                        Total account value, EOM
AV_t (BOM)                 av_pp_at(t, "BEF_PREM")         Account value, start of month
(post-premium AV)          av_pp_at(t, "BEF_FEE")          The notes' step-5 balance
(unloaned AV)              unloaned_av_pp_at(t, timing)    Deduction allocation base
(aggregate AV)             av_at(t, timing)                Account value in force
(none)                     av_change(t)                    Change in account value
e_pol                      expense_pol_mth                 $10.00 per-policy charge
e_face                     expense_unit_mth                $0.20 per $1,000 of F_0
rc(t)                      rider_charge_pp(t)              Rider charges (0)
(e_pol + e_face U + rc)    maint_fee_pp(t)                 Non-COI monthly charges
MD_t                       mth_deduction_pp(t)             Monthly deduction
(MD share)                 mth_deduction_sa_pp(t, i)       Pro-rata share, subaccount i
(MD share)                 mth_deduction_fa_pp(t)          Pro-rata share, fixed option
c_t                        coi_rate(t)                     Current monthly COI rate
(2017 CSO max)             coi_rate_guar(t)                Guaranteed maximum COI rate
(83.34 cap)                coi_rate_cap                    Monthly COI rate cap
COI_t                      coi_pp(t)                       Cost of insurance charge
kappa_t                    corridor_factor(t)              GPT corridor factor
(corridor minimum)         db_corridor_pp(t)               kappa_t x AV
DB_t                       db_pp(t)                        Death benefit, BOM
DB_t^EOM                   db_pp_eom(t)                    Death benefit, EOM
NAAR_t                     net_amt_at_risk(t)              Net amount at risk, BOM
NAAR_t^EOM                 net_amt_at_risk_eom(t)          Net amount at risk, EOM
(M&E collected)            me_charge_pp(t, i)              M&E taken in unit values
(interest credited)        inv_income_pp(t)                Total credit to the accounts
SC_t                       surr_charge_pp(t)               Surrender charge scheduled
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
(AV - SC)                  csv_pp(t)                       Cash value before debt
CSV_t                      ncsv_pp(t)                      AV - SC - D, the notes' CSV
(SC collected)             surr_charge(t)                  sc_income
(default test)             is_default(t)                   CSV_t <= 0
(deduction shortfall)      is_shortfall(t)                 Unloaned AV cannot pay MD_t
(none)                     first_default_month()           First month in default
(none)                     first_shortfall_month()         First month short of MD_t
phi_t                      funding_ratio(t)                AV_t / AV*_t
AV*_t                      av_pricing_pp(m)                At-issue pricing path
lambda_t                   lapse_rate_dyn_mult(t)          Dynamic lapse multiplier
(SC cliff spike)           lapse_rate_sc_mult(t)           Surrender-charge cliff spike
q^d,annual                 mort_rate(t)                    Annual mortality rate
q^d_t                      mort_rate_mth(t)                Monthly mortality rate
q^w,annual                 lapse_rate(t)                   Total annual lapse rate
q^w_t                      lapse_rate_mth(t)               Monthly lapse rate
q^w,base                   lapse_rate_base(t)              Base annual lapse rate
l_t                        pols_if(t)                      In force at start of month t
(l_0)                      pols_if_init                    In force at outset
(deaths)                   pols_death(t)                   Deaths in month t
(lapses)                   pols_lapse(t)                   Lapses in month t
(none)                     pols_maturity(t)                Maturities: always zero
prem_gross                 premiums(t)                     Premium income
load_income                premium_loads(t)                Premium loads collected
md_income                  mth_deduction(t)                Monthly deductions collected
me_income                  me_charge(t)                    M&E collected
loan_spread                loan_spread(t)                  (i_L - i_C) accrual on D_t
claim_gross                claims(t, "DEATH")              Death claims, DB - debt
claim_net                  claims_net(t)                   Net GA strain, NAAR^EOM
surr_outgo                 claims(t, "LAPSE")              Surrender payments
(withdrawals)              withdrawals(t)                  Withdrawal payments
sc_income                  surr_charge(t)                  Surrender charges collected
expense                    expenses(t), premium_taxes(t)   Insurer expenses
sa_transfer                sa_transfer(t)                  Separate -> general account
av_eop                     av_at(t, "EOM")                 Account value in force, EOM
(net GA cash flow)         net_cf_ga(t)                    Net-of-account view
NetCF(t)                   net_cf(t)                       Gross liability cash flow
=========================  ==============================  ==========================

Eight names needed care.

``l_t`` in the notes is the in-force probability at the **start** of month ``t`` and
``l_{t+1} = l_t (1 - q^d_t)(1 - q^w_t)`` is its roll-forward; ``pols_if(t)`` follows
``BasicTerm_S`` and is the number in force at the start of month ``t``, so the two
coincide and ``pols_if(1) = l_0 = pols_if_init()``. Every BOM cash flow is weighted by
``pols_if(t)``.

The notes' ``AV_{t+1}`` is an **end-of-month** balance, not the next month's opening
event: ``av_pp(t)`` is the notes' ``AV_{t+1}`` and ``av_pp_at(t, "BEF_PREM")`` is the
notes' ``AV_t``. The same shift applies to ``D_{t+1}``, which is ``loan_bal_pp(t)``.
This is why the notes write the death claim as ``DB_t^EOM - D_{t+1}``: both are
end-of-month quantities of month ``t``.

The notes use ``m`` for the M&E rate and also index the pricing path by policy month.
``me_rate_ann`` names the rate; the pricing-path cells take an argument ``m`` counting
policy months **from issue**, which is ``duration_mth(t) + 1`` at projection month
``t`` -- not ``t`` itself, which restarts at 1 for an in-force model point.

The notes call ``AV_t - SC_t - D_t`` the cash surrender value ``CSV_t``. The chassis
name for that quantity, net of policy debt, is ``ncsv_pp``; ``csv_pp`` is the
intermediate ``AV_t - SC_t`` before debt. Both are kept so the chassis reads across,
and the symbol table above records which is which.

``coi_rate`` is quoted per $1,000 of net amount at risk **per month** and
``expense_unit_mth`` per $1,000 of face per month, so both are divided by 1,000 -- or
multiplied by :func:`units` -- before they meet a currency amount. :func:`coi_rate` is
therefore not comparable with ``CashValue_SE.coi_rate``, which is a rate per unit of
account value.

:func:`units` takes **no** ``t``. Both the $0.20 monthly charge and the surrender
charge are quoted on ``F_0``, the *initial* face [S2], where the fixed-UL chassis
charges its per-unit fee on the current face and so writes ``units(t)``. Using the
current face here would silently reduce both charges after an Option A withdrawal.

:func:`maint_fee_pp` is the non-COI part of the *monthly deduction* -- a charge against
the account value, and therefore insurer income. :func:`expenses` is something
different: the insurer's own **[std]** maintenance outgo of $75 per policy per year.
The two must not be confused. Note also that the variable-UL notes specify a flat $75 a
year where the fixed-UL chassis inflates it at 2.5%, so ``inflation_rate`` is **0.0**
here; the cells is kept so the two models read alike.

A partial withdrawal is **not a claim**: it is a payment the owner elects, not an event
that terminates coverage, so it is :func:`withdrawals` in its own ``withdrawals`` column
and :func:`claims` neither accepts ``"WITHDRAWAL"`` nor counts it in the ``kind is None``
total.  The per-policy amount is still reached through
:func:`claim_pp(t, "WITHDRAWAL")<claim_pp>`, which is where the rule that the $25 fee is
not part of the payment is written down, and :func:`withdrawals` weights it by
:func:`pols_if` -- a withdrawal is taken at the monthiversary by policies still in force,
where a death claim is weighted by :func:`pols_death` and a surrender by
:func:`pols_lapse`.
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


def age_at_entry():
    """The issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the selected model point."""
    return model_point()["sex"]


def rate_class():
    """The underwriting class of the selected model point (one of six)."""
    return model_point()["rate_class"]


def sum_assured():
    """F_0: the initial face amount of the selected model point.

    Both the $0.20 per $1,000 monthly charge and the surrender charge are quoted on
    this, the *initial* face, not on :func:`sum_assured_at`.
    """
    return float(model_point()["sum_assured"])


def db_option():
    """The death benefit option: ``"A"`` (level) or ``"B"`` (face plus account value).

    Option C (return of premium) is observed at one insurer only and is out of scope
    in the product spec.
    """
    return model_point()["db_option"]


def qual_test():
    """The IRC 7702 qualification test elected at issue; only ``"GPT"`` is modeled.

    CVAT is a documented variation, out of scope in the baseline, so
    :func:`corridor_factor` raises on anything else rather than silently applying GPT
    corridor factors.
    """
    return model_point()["qual_test"]


def premium_type():
    """The premium pattern: ``"LEVEL"`` or ``"SINGLE"`` **[std]**.

    The notes do not enforce guideline premium or 7-pay limits in the baseline --
    premiums are assumed within limits -- so there is no cap on either pattern and no
    ``TARGET`` pattern.
    """
    return model_point()["premium_type"]


def premium_pp_ann():
    """The planned annualized premium per policy; flexible in amount and timing [S1]."""
    return float(model_point()["premium_pp_ann"])


def load_prem_rate():
    """gamma: the current premium load rate, 4.0% flat **[std]** (guaranteed max 6.0% [S2]).

    The load is a non-guaranteed element under ASOP 2 [R11], which is why it sits in
    the model point table rather than in a Reference.
    """
    return float(model_point()["load_prem_rate"])


def subaccount_ids():
    """The separate-account subaccount lineup, from *subaccount_table.csv*.

    Two subaccounts -- equity and bond -- a **[std]** collapse of the observed menus.
    Extending the lineup means adding a row here *and* the matching ``sa_pp_init_*``
    and ``alloc_*`` columns to the model point table.
    """
    return list(data.subaccount_table().index)                       # noqa: F821


def alloc(i):
    """alpha_i: the share of each net premium allocated to subaccount i."""
    return float(model_point()["alloc_" + str(i)])


def alloc_fixed():
    """alpha_F: the share of each net premium allocated to the fixed option."""
    return float(model_point()["alloc_fixed"])


def fund_expense_ann(i):
    """e_i: the annual fund operating expense ratio of subaccount i **[std]**.

    0.75% equity and 0.55% bond, chosen inside the observed lineup ranges
    (0.29%-1.18% [S1], 0.55%-2.88% gross [S2], 0.46%-2.54% [S3], 0.08%-1.93% [S4]).
    Borne through the unit value, so it reduces the policyholder's return and is *not*
    insurer income.
    """
    return float(data.subaccount_table().loc[i, "fund_expense_ann"])  # noqa: F821


def sa_pp_init(i):
    """SA_i(0): the value of subaccount i per policy at the outset, 0 at issue."""
    return float(model_point()["sa_pp_init_" + str(i)])


def fa_pp_init():
    """FA(0): the fixed-option value per policy at the outset, 0 at issue."""
    return float(model_point()["fa_pp_init"])


def loan_bal_init():
    """D(0): the outstanding policy debt per policy at the outset, 0 at issue.

    The loan-account collateral LA(0) is taken equal to it **[std]**: a loan moves
    value from the investment options into a general-account loan account [S3], so at
    the outset the two balances coincide and only their accrual rates differ.
    """
    return float(model_point()["loan_bal_init"])


def av_pp_init():
    """AV(0): the total account value per policy at the outset.

    ``sum(SA_i(0)) + FA(0) + LA(0)`` -- the loan account is part of the account value
    [S1][S2][S3][S4], the debt is not.
    """
    return (sum(sa_pp_init(i) for i in subaccount_ids())
            + fa_pp_init() + loan_bal_init())


def pols_if_init():
    """l_0: the in-force probability at the outset, 1 for a single-policy point."""
    return float(model_point()["pols_if_init"])


def duration_mth_init():
    """Completed policy months already elapsed when the projection starts.

    0 for a new-business model point, so that ``t = 1`` is the issue month; positive
    for an in-force cell.  This is the notes' ``duration_inforce``.
    """
    return int(model_point()["duration_mth"])


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point.

    False models the low-load / no-load archetype [S3], a documented variation.
    """
    return bool(model_point()["has_surr_charge"])


def surr_charge_id():
    """The surrender charge schedule ID, a row label of *surr_charge_table.csv*."""
    return model_point()["surr_charge_id"]


def scenario_id():
    """The return scenario ID, a row label of *scenario_table.csv*.

    The separate-account return path is the dominant assumption for this product, so
    it is a model point attribute rather than a Reference: different cells can be run
    on different paths in one model.
    """
    return model_point()["scenario_id"]


def duration_mth(t):
    """Completed policy months at the beginning of policy month t.

    ``duration_mth_init() + t - 1``, so it is 0 in the issue month of a new-business
    model point.  The pricing-path cells index policy months from issue as
    ``duration_mth(t) + 1``; see :func:`funding_ratio`.
    """
    return duration_mth_init() + t - 1


def duration(t):
    """Completed policy years at the beginning of policy month t."""
    return duration_mth(t) // 12


def policy_year(t):
    """The policy year containing policy month t, 1-based."""
    return duration(t) + 1


def age(t):
    """x_t: the attained age (ANB) in policy month t, ``age_at_entry() + duration(t)``.

    Age advances on the policy anniversary, not on the birthday, which is the ANB
    convention the whole model is built on **[std]**.
    """
    return age_at_entry() + duration(t)


def proj_len():
    """Projection length in policy months.

    ``12 * (omega_age - age_at_entry() + 1) - duration_mth_init()``: the projection
    runs through the policy year in which the insured attains ``omega_age`` (121), the
    last age of *mort_table.csv*, where the annual rate is 1.0.  The contract has no
    maturity date [S1][S2][S4], so the projection is truncated by mortality **[std]**,
    not by the policy.  Ending at 121 rather than 120 is deliberate: it is the age at
    which premiums and monthly deductions cease while the asset charges continue, and
    the notes list missing that regime switch among the modeling pitfalls.
    """
    return 12 * (omega_age - age_at_entry() + 1) - duration_mth_init()  # noqa: F821


def units():
    """U: the **initial** face amount in $1,000 units, ``sum_assured() / 1000``.

    Takes no ``t``.  The $0.20 monthly charge is quoted per $1,000 of ``F_0`` [S2] and
    the surrender charge per $1,000 of initial face **[std]**, so neither follows
    :func:`sum_assured_at`.  The fixed-UL chassis charges its per-unit fee on the
    *current* face and therefore writes ``units(t)``; copying that here would silently
    shrink both charges after an Option A withdrawal.
    """
    return sum_assured() / 1000


def gross_return_mth(t, i):
    """r_{i,t}: the **gross** monthly return of subaccount i, a scenario input.

    Read from *scenario_table.csv* for this model point's :func:`scenario_id`.  Months
    beyond the end of a scenario take its last row, so a two-row scenario is a level
    path with one distinguished opening month -- which is exactly the shipped ``WE``
    scenario, whose month 1 is the worked example's (+1.00% equity, -0.50% bond).

    Gross means before the fund expense ratio and before the M&E charge; both are
    applied in :func:`inv_return_mth`.  A stochastic set is more rows in this table,
    not a formula change.
    """
    tbl = data.scenario_table().loc[(scenario_id(), i)]              # noqa: F821
    m = min(t, int(tbl.index.max()))
    return float(tbl.loc[m, "gross_return_mth"])


def inv_return_mth(t, i):
    """The net monthly unit-value return of subaccount i.

    ``(1 + r_{i,t}) (1 - e_i/12) (1 - m/12) - 1``.  In the contract the fund expenses
    and (at one insurer [S1]) the M&E charge accrue daily inside the unit value; the
    monthly product form is a **[std]** approximation, and insurers that deduct M&E
    monthly [S2][S3][S4] are captured by the same factor.

    The M&E charge is applied **here and only here**.  Applying it again as a monthly
    deduction would double count it across insurer conventions -- the notes list that
    among the modeling pitfalls, and this model picks the unit-value factor.
    """
    return ((1 + gross_return_mth(t, i))
            * (1 - fund_expense_ann(i) / 12)
            * (1 - me_rate_ann / 12) - 1)                            # noqa: F821


def crediting_rate_ann(t):
    """i_fix: the declared annual effective rate on the fixed option, 1.0% **[std]**.

    Floored at the contractual guaranteed minimum ``guar_rate_ann`` of 1.0% [S1].
    Declared rates are non-guaranteed and are not published, so the baseline holds the
    declared rate at the floor; in practice it would move with general-account yields.
    """
    return max(guar_rate_ann, crediting_rate_curr)                   # noqa: F821


def fixed_return_mth(t):
    """The monthly fixed-option rate, ``(1 + i_fix)^(1/12) - 1``.

    The contract credits daily [S1]; monthly compounding is the model's discretization
    **[std]** -- do not also compound daily.
    """
    return (1 + crediting_rate_ann(t)) ** (1 / 12) - 1


def loan_rate_ann(t):
    """i_L: the annual effective rate charged on policy debt [S1].

    2.0% in policy years 1-9 (the standard loan), 1.05% from the 10th anniversary (the
    preferred loan).  Against the 1.0% credited to the loan account this is a net
    spread of 1.0% falling to 0.05%.
    """
    if policy_year(t) < loan_pref_year:                              # noqa: F821
        return loan_rate_ann_std                                     # noqa: F821
    return loan_rate_ann_pref                                        # noqa: F821


def loan_rate_mth(t):
    """The monthly charged loan rate, ``(1 + i_L)^(1/12) - 1``.

    Contractually the interest is due each anniversary and capitalized if unpaid [S1];
    monthly compounding is the model's discretization **[std]**.
    """
    return (1 + loan_rate_ann(t)) ** (1 / 12) - 1


def loan_cr_rate_ann(t):
    """i_C: the annual effective rate credited to the loan account, 1.0% [S1].

    Loaned value earns this, not fund returns -- the notes list ignoring that among
    the modeling pitfalls.
    """
    return loan_cr_rate_ann_lvl                                      # noqa: F821


def loan_cr_rate_mth(t):
    """The monthly loan-account credited rate, ``(1 + i_C)^(1/12) - 1`` **[std]**."""
    return (1 + loan_cr_rate_ann(t)) ** (1 / 12) - 1


def pricing_return_mth():
    """The monthly gross subaccount return on the notes' at-issue pricing path.

    ``(1 + 6%)^(1/12) - 1`` **[std]**: the level gross return the notes specify for
    ``AV*``, the denominator of the funding ratio.  Independent of the projection's own
    return scenario, which is the point -- the funding ratio compares the realized path
    against a fixed pricing path.
    """
    return (1 + pricing_return_ann) ** (1 / 12) - 1                  # noqa: F821


def age_pricing(m):
    """The attained age (ANB) in policy month m of the pricing path, counted from issue."""
    return age_at_entry() + (m - 1) // 12


def policy_year_pricing(m):
    """The policy year containing policy month m of the pricing path, 1-based."""
    return (m - 1) // 12 + 1


def prem_pricing_pp(m):
    """The premium paid in policy month m on the pricing path: the *planned* premium.

    The pricing path is funded at ``rho = 1`` by construction -- it is the benchmark
    the realized funding level is measured against -- so premium persistency does not
    enter it.  Zero from attained age 121.
    """
    if age_pricing(m) >= charges_cease_age:                          # noqa: F821
        return 0.0
    if premium_type() == "SINGLE":
        return premium_pp_ann() if m == 1 else 0.0
    elif premium_type() == "LEVEL":
        return premium_pp_ann() / 12
    else:
        raise ValueError("invalid premium type")


def sa_pricing_pp_at(m, i, timing):
    """Pricing-path subaccount value at an intra-month point of policy month m.

    ``"BEF_PREM"`` the closing balance of month ``m - 1``; ``"BEF_FEE"`` after the net
    premium; ``"BEF_INV"`` after this subaccount's pro-rata share of the monthly
    deduction.  There are no withdrawals and no loans on the pricing path, so the
    ``"BEF_WD"`` point of :func:`sa_pp_at` has no counterpart.
    """
    if timing == "BEF_PREM":
        return sa_pricing_pp(m - 1, i)
    elif timing == "BEF_FEE":
        return (sa_pricing_pp_at(m, i, "BEF_PREM")
                + alloc(i) * (1 - load_prem_rate()) * prem_pricing_pp(m))
    elif timing == "BEF_INV":
        den = av_pricing_pp_at(m, "BEF_FEE")
        bef = sa_pricing_pp_at(m, i, "BEF_FEE")
        share = bef / den if den > 0 else alloc(i)
        return bef - mth_deduction_pricing_pp(m) * share
    else:
        raise ValueError("invalid timing")


def sa_pricing_pp(m, i):
    """SA*_i: the pricing-path value of subaccount i at the end of policy month m.

    ``SA*_i(0) = 0``: the path starts at issue with no account value, whatever the
    model point's own opening balances are.  Growth uses the level pricing return
    rather than the projection's scenario, with the same fund expense and M&E factors.
    """
    if m == 0:
        return 0.0
    return (sa_pricing_pp_at(m, i, "BEF_INV")
            * (1 + pricing_return_mth())
            * (1 - fund_expense_ann(i) / 12)
            * (1 - me_rate_ann / 12))                                # noqa: F821


def fa_pricing_pp_at(m, timing):
    """Pricing-path fixed-option value at an intra-month point of policy month m."""
    if timing == "BEF_PREM":
        return fa_pricing_pp(m - 1)
    elif timing == "BEF_FEE":
        return (fa_pricing_pp_at(m, "BEF_PREM")
                + alloc_fixed() * (1 - load_prem_rate()) * prem_pricing_pp(m))
    elif timing == "BEF_INV":
        den = av_pricing_pp_at(m, "BEF_FEE")
        bef = fa_pricing_pp_at(m, "BEF_FEE")
        share = bef / den if den > 0 else alloc_fixed()
        return bef - mth_deduction_pricing_pp(m) * share
    else:
        raise ValueError("invalid timing")


def fa_pricing_pp(m):
    """FA*: the pricing-path fixed-option value at the end of policy month m."""
    if m == 0:
        return 0.0
    return fa_pricing_pp_at(m, "BEF_INV") * (1 + fixed_return_mth(m))


def av_pricing_pp_at(m, timing):
    """Pricing-path total account value at an intra-month point of policy month m."""
    return (sum(sa_pricing_pp_at(m, i, timing) for i in subaccount_ids())
            + fa_pricing_pp_at(m, timing))


def av_pricing_pp(m):
    """AV*_m: the account value the notes' pricing path reaches by policy month m.

    "The account value projected at issue under the pricing path (level 6% gross
    subaccount return, current charges, planned premiums)" **[std]**.  It is the
    denominator of :func:`funding_ratio`, and it is a genuine second recursion: no
    decrements, no loans, no withdrawals, ``rho = 1``, starting from zero at issue.
    """
    if m == 0:
        return 0.0
    return (sum(sa_pricing_pp(m, i) for i in subaccount_ids()) + fa_pricing_pp(m))


def db_pricing_pp(m):
    """The pricing-path death benefit in policy month m, after the corridor test.

    Uses :func:`corridor_factor_at` at the pricing path's own attained age rather than
    :func:`corridor_factor`, whose month-1 pin belongs to the projection and not to
    this benchmark.
    """
    av = av_pricing_pp_at(m, "BEF_FEE")
    if db_option() == "A":
        opt = sum_assured()
    elif db_option() == "B":
        opt = sum_assured() + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor_at(age_pricing(m)) * av)


def naar_pricing_pp(m):
    """The pricing-path net amount at risk, ``max(0, DB* - AV*')``, undiscounted [S2]."""
    return max(0.0, db_pricing_pp(m) - av_pricing_pp_at(m, "BEF_FEE"))


def mth_deduction_pricing_pp(m):
    """The pricing-path monthly deduction: current charges, as the notes specify.

    ``e_pol + e_face x U + c x NAAR*/1000``, zero from attained age 121.  The current
    COI scale comes from :func:`coi_rate_at`, the rule, never from a model point's
    month-1 pin: the pricing path is a seventy-year benchmark and a single disclosed
    rate is not a scale.
    """
    if age_pricing(m) >= charges_cease_age:                          # noqa: F821
        return 0.0
    return (expense_pol_mth + expense_unit_mth * units()             # noqa: F821
            + coi_rate_at(policy_year_pricing(m)) / 1000 * naar_pricing_pp(m))


def funding_ratio(t):
    """phi_t: the funding ratio ``AV_t / AV*_t`` **[std]**.

    Both sides are measured at the **start** of policy month t, before the premium, so
    the dynamic multipliers that consume it cannot depend on the premium they help
    determine.  ``phi_t < 1`` is a performance or funding shortfall.

    Returns 1.0 -- no dynamic effect -- when the behavior module is off, and also when
    the pricing path has not accumulated anything yet, which is the issue month of a
    new-business point.
    """
    if not dyn_behavior_on:                                          # noqa: F821
        return 1.0
    star = av_pricing_pp(duration_mth(t))
    if star <= 0:
        return 1.0
    return av_pp_at(t, "BEF_PREM") / star


def prem_persistency_base(t):
    """rho^base_t: the base fraction of the planned premium paid in policy year y **[std]**.

    1.00 in year 1 grading to 0.85 in year 5 and 0.80 thereafter, read from
    *prem_persistency.csv*; policy years beyond the table take its last row.  The
    levels come from the UL premium persistency study [REG-R21] applied to VUL by
    analogy -- no VUL-specific study was retrieved, which the notes flag.
    """
    tbl = data.prem_persistency_table()                              # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "prem_persistency"])


def prem_persistency(t):
    """rho_t: the fraction of the planned premium actually paid **[std]**.

    ``rho^base_t x min(1.3, max(0.7, phi_t^-0.25))``: a funding shortfall induces
    catch-up funding by retained policyholders, strong performance induces premium
    holidays -- the signature flexible-premium behavior the UL studies measure
    [REG-R21].

    **1.0 when the behavior module is off**, which is the default.  The base
    deterministic run therefore pays the planned premium in full, which is what the
    notes' worked example does ("planned premium $500/month paid"); switching
    ``dyn_behavior_on`` on brings in both the base persistency scale and the funding
    adjustment.  ``Term_US_A`` switches conversion off for the same reason.
    """
    if not dyn_behavior_on:                                          # noqa: F821
        return 1.0
    phi = funding_ratio(t)
    if phi <= 0:
        adj = prem_pers_cap                                          # noqa: F821
    else:
        adj = min(prem_pers_cap,                                     # noqa: F821
                  max(prem_pers_floor, phi ** (-prem_pers_delta)))   # noqa: F821
    return prem_persistency_base(t) * adj


def premium_pp(t):
    """P_t: the gross premium per policy paid at the monthiversary of month t.

    ``LEVEL``  the planned annual premium / 12, times :func:`prem_persistency`.
    ``SINGLE`` one premium in the issue month.

    Zero from attained age 121, when premiums are no longer accepted [S1][S2][S4].
    Guideline premium and 7-pay limits are not enforced in the baseline; premiums are
    assumed within limits **[std]**.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    if premium_type() == "SINGLE":
        return premium_pp_ann() if duration_mth(t) == 0 else 0.0
    elif premium_type() == "LEVEL":
        return premium_pp_ann() / 12 * prem_persistency(t)
    else:
        raise ValueError("invalid premium type")


def prem_to_av_pp(t):
    """The net premium credited to the accounts, ``P_t x (1 - gamma)``.

    Split by :func:`alloc` and :func:`alloc_fixed`.  The net premium is a pass-through
    into the policyholder's accounts; the load is insurer revenue.
    """
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_av(t):
    """Net premium credited to the accounts, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """prem_gross: premium income at BOM of policy month t, weighted by the in force.

    The **full** premium, not the load: the net premium is a pass-through into the
    accounts and shows up again as an account release when a claim is paid.
    """
    return premium_pp(t) * pols_if(t)


def premium_loads(t):
    """load_income: the premium load the insurer keeps, ``gamma x P_t x l_t``."""
    return load_prem_rate() * premium_pp(t) * pols_if(t)


def wd_pp(t):
    """W(t): the partial withdrawal per policy at the monthiversary of month t.

    The constant monthly figure in the model point's ``wd_pp`` column, **0 in every
    shipped model point**: the notes make withdrawals explicitly none in the baseline,
    so the mechanics are implemented and the behavior is left to the data **[std]**.
    Not taken after attained age 121.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return float(model_point()["wd_pp"])


def wd_fee_pp(t):
    """The $25 withdrawal fee, charged only in a month with a withdrawal [S1].

    Retained by the insurer, so it is account-value outgo but not a liability cash
    flow; it appears in :func:`margin_expense`, not in :func:`claims`.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def wd_sa_pp(t, i):
    """The part of the withdrawal and its fee taken from subaccount i.

    Pro rata over the **unloaned** accounts, on balances measured after the premium
    **[std]**; the loan account is collateral and is not available.  The denominator is
    guarded exactly as :func:`mth_deduction_sa_pp` guards it, and for the same reason.
    """
    den = unloaned_av_pp_at(t, "BEF_WD")
    share = sa_pp_at(t, i, "BEF_WD") / den if den > 0 else alloc(i)
    return (wd_pp(t) + wd_fee_pp(t)) * share


def wd_fa_pp(t):
    """The part of the withdrawal and its fee taken from the fixed option."""
    den = unloaned_av_pp_at(t, "BEF_WD")
    share = fa_pp_at(t, "BEF_WD") / den if den > 0 else alloc_fixed()
    return (wd_pp(t) + wd_fee_pp(t)) * share


def face_reduction_pp(t):
    """The face reduction a withdrawal forces under Option A [S1][S2].

    **Proportionate**: the face is cut in the same proportion as the withdrawal bears
    to the account value, ``F x W / AV``.  Note the contrast with the fixed-UL chassis,
    which instead cuts the face by the excess of the withdrawal over a free amount --
    the variable-UL notes say proportionate, and that is what is implemented here.
    Under Option B the withdrawal reduces the account value only, and this is zero.
    """
    if db_option() != "A" or wd_pp(t) <= 0:
        return 0.0
    av = av_pp_at(t, "BEF_WD")
    if av <= 0:
        return 0.0
    return sum_assured_at(t - 1) * wd_pp(t) / av


def sum_assured_at(t):
    """F_t: the face amount after any withdrawal-driven reductions.

    ``F_0 = sum_assured()``; face increases, elective decreases and option changes are
    not modeled, so the only movement is the Option A withdrawal reduction.
    """
    if t == 0:
        return sum_assured()
    return max(0.0, sum_assured_at(t - 1) - face_reduction_pp(t))


def unloaned_av_pp_at(t, timing):
    """The unloaned account value: subaccounts plus the fixed option, excluding LA.

    This is the base the withdrawal and the monthly deduction are allocated over
    **[std]** -- the loan account is collateral for the debt and is not drawn on.
    ``timing`` takes the :func:`av_pp_at` values other than ``"BEF_PREM"``.
    """
    return (sum(sa_pp_at(t, i, timing) for i in subaccount_ids())
            + fa_pp_at(t, timing))


def corridor_factor_at(a):
    """kappa: the GPT corridor factor at attained age a [S2][R3].

    250% to age 40, 215% at 45, 185% at 50, 150% at 55, 130% at 60, then **grading
    linearly to 100% at attained age 95** and level at 100% from there on.  The quoted
    quinquennial factors are sourced; every age between them is **linear interpolation
    [std]**, carried in ``corridor_factors.csv`` to six decimals.

    The notes write the tail as "to 100% at 90-95", which does not say which end of
    that range reaches 100%; the product spec's footnote 11 does -- *"The reference
    model linearly interpolates between the quoted ages and grades to 100% at 95"* --
    so the last quoted age (130% at 60) is joined to 100% at 95, not to 100% at 90.
    The two readings differ over attained ages 61-94: at age 90 this table gives
    ``kappa = 1.042857`` where grading to 90 would give 1.00, and a corridor of exactly
    1.00 would collapse the net amount at risk to zero on an Option A policy funded
    above its face.

    Ages outside the table take its first or last row.  Interpolating is what keeps the
    death benefit continuous: stepping between quinquennial factors would make it jump
    on every fifth anniversary, which the notes list among the modeling pitfalls.
    """
    tbl = data.corridor_factors()                                    # noqa: F821
    a = min(max(a, int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[a, "corridor_factor"])


def corridor_factor(t):
    """kappa_t: the corridor factor in policy month t, at the **attained** age.

    Only the Guideline Premium Test is modeled; CVAT is a documented variation, so any
    other ``qual_test`` raises rather than being treated as GPT.

    A model point may pin the factor **in the projection's first month** through the
    ``corridor_override_m1`` column.  Model point 1 does, at 2.15, because the notes'
    worked example sits in policy year 3 -- attained age 47, where the rule gives
    2.03 -- but quotes ``kappa(45) = 215%``, the **issue**-age factor.  The pin
    reproduces the worked example's corridor product exactly.

    The pin is deliberately confined to ``t == 1``, the one month the worked example
    describes.  It is a *lookup* that the notes performed at the wrong age, not a
    parameter of the contract; holding an issue-age corridor factor across the
    seventy-seven years this projection runs would misstate every later month and is no
    reading of the notes at all.  Model point 2 is the same cell with the pin blank, so
    the rule applies from the first month too, and a test holds the gap open in both
    directions.
    """
    if qual_test() != "GPT":
        raise ValueError("invalid qual_test")
    o = model_point()["corridor_override_m1"]
    if t == 1 and not pd.isna(o):                                    # noqa: F821
        return float(o)
    return corridor_factor_at(age(t))


def db_corridor_pp(t):
    """The corridor minimum death benefit, ``kappa_t x AV'(t)``.

    Named because the worked example displays it: at the anchor cell it is
    ``2.15 x 50,480 = 108,532.00``, which loses to the $500,000 face.  The corridor
    binds only on heavily funded, older cells.
    """
    return corridor_factor(t) * av_pp_at(t, "BEF_FEE")


def db_pp(t):
    """DB_t: the death benefit per policy at the monthiversary, after the corridor test.

    Option A ``max(F_t, kappa_t x AV'(t))``; Option B ``max(F_t + AV'(t),
    kappa_t x AV'(t))``, where ``AV'(t)`` is the account value after premium and
    withdrawal and **before** the monthly deduction [S2][R3].  Measuring the account
    value at that point is what removes the circularity: under Option B the death
    benefit depends on the account value and the net amount at risk depends on the
    death benefit, but with this ordering neither depends on the deduction.
    """
    av = av_pp_at(t, "BEF_FEE")
    if db_option() == "A":
        opt = sum_assured_at(t)
    elif db_option() == "B":
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, db_corridor_pp(t))


def net_amt_at_risk(t):
    """NAAR_t: ``max(0, DB_t - AV'(t))`` [S2]; floor **[std]**.

    **No one-month discount.**  This is the single sourced deviation from the
    fixed-UL chassis, which divides the death benefit by ``1 + i_gm`` first: the VUL
    prospectuses define the net amount at risk as death benefit less account value
    outright [S2], so there is no ``naar_factor`` in this model.  Carrying the chassis
    recursion across unexamined would understate the net amount at risk, and with it
    the cost of insurance, by about one month's guaranteed interest on the death
    benefit every month.

    The floor at zero is a standardization: the corridor keeps ``DB >= AV`` in normal
    operation, and forgetting the floor is on the notes' pitfall list.
    """
    return max(0.0, db_pp(t) - av_pp_at(t, "BEF_FEE"))


def coi_rate_scale():
    """The guaranteed maximum monthly COI scale for this model point's cell.

    A Series indexed by policy year, per $1,000 of net amount at risk, sliced once
    from *coi_rates.csv* for this ``sex`` / ``rate_class`` / ``age_at_entry``.  The
    shipped table covers the notes' anchor cell M / StdNT / 45 only; a model point on
    any other cell needs the table extended first.
    """
    return data.coi_rates().loc[                                     # noqa: F821
        (sex(), rate_class(), age_at_entry())]["coi_rate_guar"]


def coi_rate_guar_at(y):
    """The guaranteed maximum monthly COI rate per $1,000 NAAR in policy year y.

    An illustrative **[std]** stand-in for the licensed 2017 CSO sex-distinct
    smoker/nonsmoker ultimate ANB table the notes require [S2][S4][R12], anchored on
    the one disclosed guaranteed point -- male 45 standard non-tobacco, policy year 1
    = $0.22 [S4].  Capped at ``coi_rate_cap`` ($83.34, observed $83.33-$83.34 across
    filings), the monthly rate that fully consumes the net amount at risk near attained
    age 120 [S1][S2][S3][S4].  Policy years beyond the table take its last row.
    """
    scale = coi_rate_scale()
    y = min(y, int(scale.index.max()))
    return min(float(scale[y]), coi_rate_cap)                        # noqa: F821


def coi_rate_guar(t):
    """The guaranteed maximum monthly COI rate in policy month t."""
    return coi_rate_guar_at(policy_year(t))


def coi_rate_at(y):
    """c: the current monthly COI rate per $1,000 NAAR in policy year y **[std]**.

    ``coi_curr_factor`` (50%) of the guaranteed maximum -- the notes' stated default
    placeholder for the current scale -- bounded above by the guaranteed maximum and by
    the $83.34 cap [S2][S4][R12].  Current COI tables are not publicly disclosed; only
    minima, maxima and representative points appear in prospectuses, so this factor is
    a pure modeling assumption and the notes rank it the second most important
    assumption in the model.

    Note the units: per $1,000 of net amount at risk per **month**, so it is divided by
    1,000 in :func:`coi_pp`.  It is not comparable with ``CashValue_SE.coi_rate``,
    which is a rate per unit of account value.
    """
    rate = coi_curr_factor * coi_rate_guar_at(y)                     # noqa: F821
    return min(rate, coi_rate_guar_at(y), coi_rate_cap)              # noqa: F821


def coi_rate(t):
    """c_t: the current monthly COI rate in policy month t.

    A model point may pin the rate **in the projection's first month** through the
    ``coi_rate_override_m1`` column.  Model point 1 does, at 0.04: that is the year-1
    current rate disclosed for this cell [S4], which the notes' worked example applies
    in policy year 3, and it is 18% of the year-1 guaranteed $0.22 rather than the 50%
    the placeholder assumes.  The notes acknowledge the gap themselves -- "disclosed
    year-1 current/guaranteed ratios are much lower (select effect)" -- so the
    placeholder is conservative early and the select-to-ultimate shape matters.

    As with :func:`corridor_factor`, the pin is confined to ``t == 1``: a single
    disclosed point is not a scale, and holding $0.04 flat for seventy-seven years
    would leave a policy paying almost nothing for its insurance at age 100.  Model
    point 2 is the same cell with the pin blank and takes the placeholder from the
    first month, and a test holds the gap open in both directions.
    """
    o = model_point()["coi_rate_override_m1"]
    if t == 1 and not pd.isna(o):                                    # noqa: F821
        return min(float(o), coi_rate_guar(t), coi_rate_cap)         # noqa: F821
    return coi_rate_at(policy_year(t))


def coi_pp(t):
    """COI_t: the cost of insurance charge per policy, ``c_t / 1000 x NAAR_t``.

    Zero from attained age 121, when monthly deductions cease [S1][S2][S4].

    The rate here is the **current COI scale** -- insurer revenue, a non-guaranteed
    element under ASOP 2 [R11].  It is not the death decrement: that is
    :func:`mort_rate`, best-estimate experience.  The notes are emphatic that the two
    must never be conflated, and they are deliberately different tables here.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def coi(t):
    """Cost of insurance charges deducted from account values, for the policies in force."""
    return coi_pp(t) * pols_if(t)


def rider_charge_pp(t):
    """rc(t): rider charges, 0 in the baseline **[std]**.

    The no-lapse guarantee and overloan protection riders are documented variations
    that the notes exclude from the baseline; this term is carried in the monthly
    deduction so a rider module can be added without changing the recursion.
    """
    return 0.0


def maint_fee_pp(t):
    """The non-COI part of the monthly deduction per policy.

    ``e_pol + e_face x U + rc(t)``: the $10.00 per-policy administrative charge
    [S2][S4] and the $0.20 per $1,000 of **initial** face charge [S2], both level in
    all years, plus rider charges.  Zero from attained age 121, when deductions cease
    [S1][S2][S4].

    The name follows ``CashValue_SE.maint_fee``: this is a *charge* against the account
    value and therefore insurer income.  It is not :func:`expenses`, which is the
    insurer's own outgo.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return (expense_pol_mth + expense_unit_mth * units()             # noqa: F821
            + rider_charge_pp(t))


def maint_fee(t):
    """Non-COI monthly charges deducted from account values, for the policies in force."""
    return maint_fee_pp(t) * pols_if(t)


def mth_deduction_pp(t):
    """MD_t: the monthly deduction per policy, taken at the monthiversary.

    ``COI_t + e_pol + e_face x F_0/1000``, i.e. :func:`maint_fee_pp` plus
    :func:`coi_pp`.  The M&E charge is **not** part of it -- that is collected inside
    the unit values by :func:`inv_return_mth`, and taking it in both places is on the
    notes' pitfall list.
    """
    return maint_fee_pp(t) + coi_pp(t)


def mth_deduction(t):
    """md_income: monthly deductions collected, for the policies in force."""
    return mth_deduction_pp(t) * pols_if(t)


def mth_deduction_sa_pp(t, i):
    """The monthly deduction's pro-rata share taken from subaccount i **[std]**.

    ``MD_t x SA_i / sum(unloaned)``, on balances measured after the premium and the
    withdrawal.  The loan account is excluded because it is collateral.

    The denominator is guarded -- the notes list an unguarded one among the modeling
    pitfalls -- and the guard falls back to the **premium allocation** shares
    ``alpha_i`` **[std]**.  That keeps the full deduction applied, so the account value
    roll-forward stays exact, and it matters only once the unloaned balance has run to
    zero or below, which is well past the month :func:`is_shortfall` first fires.  The
    notes would have defaulted the policy there; the grace cascade is not implemented,
    so the arithmetic simply continues, as it does on the fixed-UL chassis.  Whatever
    fallback is chosen, the shares sum to one, which is what the identity needs.
    """
    den = unloaned_av_pp_at(t, "BEF_FEE")
    share = sa_pp_at(t, i, "BEF_FEE") / den if den > 0 else alloc(i)
    return mth_deduction_pp(t) * share


def mth_deduction_fa_pp(t):
    """The monthly deduction's pro-rata share taken from the fixed option **[std]**."""
    den = unloaned_av_pp_at(t, "BEF_FEE")
    share = fa_pp_at(t, "BEF_FEE") / den if den > 0 else alloc_fixed()
    return mth_deduction_pp(t) * share


def sa_pp_at(t, i, timing):
    """Subaccount i's value per policy at an intra-month point of policy month t.

    The events change the balance in this order, and ``timing`` names the point just
    before each of them:

    ``"BEF_PREM"``
        Before the premium: the closing balance of the previous month.

    ``"BEF_WD"``
        After this subaccount's share ``alpha_i`` of the net premium.

    ``"BEF_FEE"``
        After the withdrawal and its fee, before the monthly deduction.  Summed across
        the accounts this is the notes' post-premium value ``AV'``, the balance the
        death benefit, corridor test and net amount at risk are all measured against.

    ``"BEF_INV"``
        After the monthly deduction, before growth.  Growth applies to this
        post-deduction balance; reversing the two overstates the account value by about
        one month's return on the deduction every month.

    ``"BEF_ME"``
        After the gross return and the fund expense, before the M&E charge.  This is
        the balance the M&E charge is taken from, so it is what :func:`me_charge_pp`
        measures.

    The end-of-month balance is :func:`sa_pp`.
    """
    if timing == "BEF_PREM":
        return sa_pp(t - 1, i)
    elif timing == "BEF_WD":
        return sa_pp_at(t, i, "BEF_PREM") + alloc(i) * prem_to_av_pp(t)
    elif timing == "BEF_FEE":
        return sa_pp_at(t, i, "BEF_WD") - wd_sa_pp(t, i)
    elif timing == "BEF_INV":
        return sa_pp_at(t, i, "BEF_FEE") - mth_deduction_sa_pp(t, i)
    elif timing == "BEF_ME":
        return (sa_pp_at(t, i, "BEF_INV") * (1 + gross_return_mth(t, i))
                * (1 - fund_expense_ann(i) / 12))
    else:
        raise ValueError("invalid timing")


def sa_pp(t, i):
    """SA_{i,t}: subaccount i's value per policy at the end of policy month t.

    ``SA_i(0) = sa_pp_init(i)``; thereafter the post-deduction balance times the
    unit-value factor ``(1 + r)(1 - e_i/12)(1 - m/12)``, which is
    ``1 + inv_return_mth(t, i)``.  Separate-account assets: the policyholder bears the
    investment experience and the insurer's general account does not.
    """
    if t == 0:
        return sa_pp_init(i)
    return sa_pp_at(t, i, "BEF_ME") * (1 - me_rate_ann / 12)         # noqa: F821


def fa_pp_at(t, timing):
    """The fixed-option value per policy at an intra-month point of policy month t.

    ``timing`` takes the same values as :func:`sa_pp_at` except ``"BEF_ME"``: the
    fixed option is a general-account balance and bears neither fund expenses nor the
    M&E charge.
    """
    if timing == "BEF_PREM":
        return fa_pp(t - 1)
    elif timing == "BEF_WD":
        return fa_pp_at(t, "BEF_PREM") + alloc_fixed() * prem_to_av_pp(t)
    elif timing == "BEF_FEE":
        return fa_pp_at(t, "BEF_WD") - wd_fa_pp(t)
    elif timing in ("BEF_INV", "BEF_ME"):
        return fa_pp_at(t, "BEF_FEE") - mth_deduction_fa_pp(t)
    else:
        raise ValueError("invalid timing")


def fa_pp(t):
    """FA_t: the fixed-option value per policy at the end of policy month t.

    ``FA(0) = fa_pp_init()``; thereafter ``FA'(t) x (1 + i_fix)^(1/12)`` at the
    declared rate, floored at the contractual 1.0% [S1].  A general-account liability,
    unlike the subaccounts.
    """
    if t == 0:
        return fa_pp_init()
    return fa_pp_at(t, "BEF_INV") * (1 + fixed_return_mth(t))


def la_pp(t):
    """LA_t: the loan-account collateral per policy at the end of policy month t [S3].

    ``LA(0) = loan_bal_init()`` **[std]** -- a loan moves value out of the investment
    options into a general-account loan account, so collateral and debt coincide at the
    outset.  Thereafter it earns the credited loan rate ``i_C``, **not** fund returns,
    which is why it is held apart from the subaccounts and excluded from the pro-rata
    deduction base.  It is part of the account value; the debt is not.

    New loans and repayments are not modeled -- the notes give no utilization pattern
    -- so this only rolls the model point's opening collateral forward.
    """
    if t == 0:
        return loan_bal_init()
    return la_pp(t - 1) * (1 + loan_cr_rate_mth(t))


def loan_bal_pp(t):
    """D_t: the outstanding policy debt per policy at the end of policy month t.

    ``D(0) = loan_bal_init()``; thereafter ``D(t-1) x (1 + i_L)^(1/12)``, the charged
    rate, monthly **[std]** where the contract charges interest annually in arrears and
    capitalizes it if unpaid [S1].  Debt reduces both the death benefit and the
    surrender value; it grows faster than the collateral in :func:`la_pp`, and the
    difference is the insurer's :func:`loan_spread`.

    Note the notes' indexing: their ``D_{t+1}`` is this end-of-month balance of month
    ``t``, which is why the death claim is ``DB_t^EOM - D_{t+1}``.
    """
    if t == 0:
        return loan_bal_init()
    return loan_bal_pp(t - 1) * (1 + loan_rate_mth(t))


def loan_spread(t):
    """loan_spread: the insurer's margin on policy debt, for the policies in force.

    ``l_t x D(t-1) x [(1 + i_L)^(1/12) - (1 + i_C)^(1/12)]`` -- one month of the
    charged rate less one month of the credited rate on the opening debt.  1.0% a year
    in policy years 1-9 and 0.05% from the 10th [S1].
    """
    return (loan_bal_pp(t - 1)
            * (loan_rate_mth(t) - loan_cr_rate_mth(t)) * pols_if(t))


def av_pp_at(t, timing):
    """AV per policy at an intra-month point of policy month t.

    ``sum(SA_i) + FA + LA``.  The loan account does not move intra-month -- it accrues
    only at end of month -- so it enters at its opening balance whatever the
    ``timing``, which takes the :func:`sa_pp_at` values.  An unknown ``timing`` raises
    from :func:`sa_pp_at`.
    """
    if timing == "BEF_PREM":
        return av_pp(t - 1)
    return unloaned_av_pp_at(t, timing) + la_pp(t - 1)


def av_pp(t):
    """AV_t: the total account value per policy at the end of policy month t.

    ``sum(SA_i) + FA + LA`` [S1][S2][S3][S4].  ``AV(0) = av_pp_init()`` by
    construction, since each component starts at its own opening balance.
    """
    return (sum(sa_pp(t, i) for i in subaccount_ids())
            + fa_pp(t) + la_pp(t))


def av_at(t, timing):
    """Account value in force at an intra-month point of policy month t.

    :func:`av_pp_at` times the number of policies in force, which is constant through
    the month because decrements are end-of-month events.  ``timing`` takes the same
    values as :func:`av_pp_at`, plus ``"EOM"`` for the closing balance before
    decrements -- the notes' ``av_eop`` reconciliation column.
    """
    if timing == "EOM":
        return av_pp(t) * pols_if(t)
    return av_pp_at(t, timing) * pols_if(t)


def av_change(t):
    """Change in the account value in force over policy month t.

    ``av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")``, following ``CashValue_SE``.
    """
    return av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")


def me_charge_pp(t, i=None):
    """me_income per policy: the M&E risk charge collected inside the unit values.

    ``SA_i (after the gross return and the fund expense) x m / 12`` for subaccount
    ``i``, or the total over the lineup when ``i`` is ``None``.  0.45% a year current
    [S1], under a 0.60% guaranteed ceiling **[std]**.

    This is insurer revenue taken from separate-account assets, and it is the only
    charge in this model that is *not* an explicit deduction -- which is why it has to
    be reported separately for the net-of-account view to reconcile.  It continues
    after attained age 121, when the monthly deduction stops [S1][S2][S4].
    """
    if i is None:
        return sum(me_charge_pp(t, j) for j in subaccount_ids())
    return sa_pp_at(t, i, "BEF_ME") * me_rate_ann / 12               # noqa: F821


def me_charge(t):
    """me_income: the M&E risk charge collected, for the policies in force."""
    return me_charge_pp(t) * pols_if(t)


def inv_income_pp(t):
    """The total investment credit to the accounts per policy over policy month t.

    The subaccount growth **net** of fund expenses and the M&E charge, plus the
    fixed-option interest, plus the loan-account interest.  Because it is net, the
    insurer's M&E revenue is *not* in it: :func:`me_charge_pp` reports that separately
    and :func:`check_net_view` puts the two back together.
    """
    return (sum(sa_pp(t, i) - sa_pp_at(t, i, "BEF_INV")
                for i in subaccount_ids())
            + fa_pp(t) - fa_pp_at(t, "BEF_INV")
            + la_pp(t) - la_pp(t - 1))


def inv_income(t):
    """Investment credit to the accounts, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month of it.
    """
    return inv_income_pp(t) * pols_if(t)


def db_pp_eom(t):
    """DB_t^EOM: the death benefit recomputed on end-of-month balances **[std]**.

    The notes weight the death claim by ``l_t q^d_t`` at end of month and recompute the
    option and corridor formula on the end-of-month account value, so a death in month
    ``t`` is paid on ``DB_t^EOM``, not on the monthiversary figure that priced the
    month's cost of insurance.
    """
    av = av_pp(t)
    if db_option() == "A":
        opt = sum_assured_at(t)
    elif db_option() == "B":
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor(t) * av)


def net_amt_at_risk_eom(t):
    """NAAR_t^EOM: ``max(0, DB_t^EOM - AV_t)``, the net general-account strain.

    This, not the death benefit, is what the insurer's own funds have to find when a
    policy dies: the account value is seized to fund the rest.  It is the notes'
    ``claim_net`` before survivorship weighting -- and it is emphatically **not** the
    claim cash flow; see :func:`claims`.
    """
    return max(0.0, db_pp_eom(t) - av_pp(t))


def surr_charge_rate(t):
    """SC per $1,000 of initial face in policy year y **[std]**.

    ``sc_init x (runoff_years + 1 - y) / runoff_years``, floored at zero: $18.00 per
    $1,000 in policy year 1, declining **by policy year** to zero at the end of policy
    year 14.  In policy year 3 that is ``18.00 x 12/14 = 15.428571``, the factor the
    worked example quotes.

    Note the contrast with the fixed-UL chassis, whose surrender charge amortizes every
    *month*.  The variable-UL notes step it by policy year, and the worked example pins
    the step: carrying the chassis's monthly run-off across would give
    ``18 x (1 - 25/168)`` here instead.
    """
    if not has_surr_charge():
        return 0.0
    row = data.surr_charge_table().loc[surr_charge_id()]             # noqa: F821
    init = float(row["sc_per_1000_init"])
    yrs = int(row["runoff_years"])
    return max(0.0, init * (yrs + 1 - policy_year(t)) / yrs)


def surr_charge_pp(t):
    """SC_t: the surrender charge scheduled per policy in policy month t.

    Quoted on the **initial** face amount [S1][S2].  This is the schedule; the amount
    actually collected is :func:`surr_charge`, which is capped by the account value.
    """
    return surr_charge_rate(t) * units()


def csv_pp(t):
    """``AV_t - SC_t``: the cash value before policy debt, floored at zero **[std]**.

    The chassis name for this intermediate.  The floor is a standardization -- a
    negative cash value would be a payment *from* the policyholder -- and it binds in
    the early policy years, where the scheduled surrender charge exceeds the account
    value, so the charge actually collected is the whole account value.  The notes'
    own ``CSV_t`` is net of debt: that is :func:`ncsv_pp`.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """CSV_t: the cash surrender value, ``AV_t - SC_t - D_t``, floored at zero [S1].

    What a surrendering policyholder is paid, and the notes' surrender outgo.  Note
    the notes' indexing: their ``AV_{t+1} - SC_t - D_{t+1}`` is this end-of-month
    quantity of month ``t``.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """sc_income: surrender charges collected from the policies lapsing in month t.

    ``(AV_t - csv_pp(t)) x pols_lapse(t)``, so it is capped by the account value where
    the :func:`csv_pp` floor binds.  Insurer income, and part of
    :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def is_default(t):
    """The notes' default test: ``AV_t - SC_t - D_t <= 0`` at the end of month t [S1].

    The contractual trigger for grace, and the same test as the excess-debt default
    (debt at or above fund less surrender charge) [S1].  It is a **diagnostic only**:
    the notes lapse a defaulted policy "at the next monthiversary if not cured" without
    defining the cure test, the in-grace deduction accrual or the death benefit during
    grace, so the grace cascade is not implemented and no policy is terminated for
    insufficiency here.

    Read literally the test is true from **issue** on any front-loaded design: in
    policy year 1 the scheduled $18 per $1,000 surrender charge is far larger than the
    account value a first premium buys, so ``AV - SC`` is negative on a perfectly
    healthy new policy.  That is what model point 3 shows.  The test is reported as the
    notes write it, and :func:`is_shortfall` is the companion diagnostic that answers
    the question the default rule is really asking.
    """
    return av_pp(t) - surr_charge_pp(t) - loan_bal_pp(t) <= 0


def is_shortfall(t):
    """The deduction-shortfall test: the unloaned accounts cannot pay ``MD_t``.

    ``unloaned_av_pp_at(t, "BEF_FEE") < mth_deduction_pp(t)``.  The fixed-UL chassis
    makes this its grace trigger, and it is the point at which the account genuinely
    stops being able to carry the contract, as opposed to the notes' literal
    surrender-charge test in :func:`is_default`.  A diagnostic; nothing terminates.
    """
    return unloaned_av_pp_at(t, "BEF_FEE") < mth_deduction_pp(t)


def first_default_month():
    """The first policy month in which :func:`is_default` is true, or 0 if never.

    On a front-loaded model point this is usually month 1; see :func:`is_default`.
    """
    for t in range(1, proj_len() + 1):
        if is_default(t):
            return t
    return 0


def first_shortfall_month():
    """The first policy month in which :func:`is_shortfall` is true, or 0 if never.

    The month past which the projection is arithmetic rather than a description of a
    live contract: the notes' default rule would have terminated the policy at the
    following monthiversary, and that cascade is not implemented.  A level-premium cell
    whose cost of insurance eventually outruns its premium reaches this point at some
    late duration; run it to see where.
    """
    for t in range(1, proj_len() + 1):
        if is_shortfall(t):
            return t
    return 0


def class_factor():
    """The underwriting-class multiplier on the base mortality table **[std]**."""
    return float(data.class_factor_table().loc[rate_class(), "factor"])  # noqa: F821


def mort_rate(t):
    """q^d,annual: the annual best-estimate mortality rate in policy month t.

    Base table times :func:`class_factor` times the A/E factor, 100% in the base run
    **[std]** with no mortality improvement.  The shipped table is a small illustrative
    one **[std]**, *not* the 2015 VBT calibrated to ILEC experience the notes recommend
    [REG-R18][REG-R19] -- that family is licensed and may not be reproduced here.  Ages
    beyond the table take its last row, where the rate is 1.0.

    This is the **death decrement**, best-estimate experience.  It is not
    :func:`coi_rate`, the current COI scale, which is a revenue item.  Conflating them
    is the first entry on the notes' list of modeling pitfalls, and the two tables
    shipped here are deliberately different.
    """
    tbl = data.mort_table()                                          # noqa: F821
    a = min(max(age(t), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[a, "mort_rate"]) * class_factor() * mort_ae_factor  # noqa: F821


def mort_rate_mth(t):
    """q^d_t: the monthly mortality rate, ``1 - (1 - q^d,annual)^(1/12)`` **[std]**."""
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """q^w,base: the base annual lapse rate by policy year **[std]**.

    6% in year 1, 5% in year 2, 4% in years 3-10, 3% thereafter, read from
    *lapse_table.csv*; policy years beyond the table take its last row.  The levels
    come from the LIMRA/SOA UL persistency and lapse studies [REG-R20][REG-R21] applied
    to VUL **by analogy** -- VUL is not broken out separately in them, which the notes
    flag -- and the detailed tables are behind a paid package, so the numbers are a
    standardization.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate_ann"])


def lapse_shock_month():
    """The policy month of the surrender-charge cliff, counted from issue.

    ``12 x runoff_years + 1``: the first month in which the surrender charge is zero,
    which for the shipped fourteen-year schedule is policy month 169.  Derived from
    *surr_charge_table.csv* rather than hard-coded, so a different schedule moves the
    cliff with it.  Zero when the model point carries no surrender charge, which no
    policy month can equal.
    """
    if not has_surr_charge():
        return 0
    yrs = int(data.surr_charge_table().loc[surr_charge_id(), "runoff_years"])  # noqa: F821
    return 12 * yrs + 1


def lapse_rate_sc_mult(t):
    """The surrender-charge cliff spike multiplier **[std]**.

    Applied in :func:`lapse_shock_month` alone -- the notes make it a *one-month* spike
    "in the month after SC_t reaches zero", not a whole shock year as on the fixed-UL
    chassis.  The notes call the spike optional and its magnitude an input, so
    ``lapse_shock_mult`` ships at 1.0, i.e. off; set it to 2.0 to switch it on.
    """
    if not has_surr_charge():
        return 1.0
    if duration_mth(t) + 1 == lapse_shock_month():
        return lapse_shock_mult                                      # noqa: F821
    return 1.0


def lapse_rate_dyn_mult(t):
    """lambda_t: the dynamic lapse multiplier **[std]**.

    ``min(2.0, max(0.5, 1 + beta (1 - phi_t)))`` with ``beta = 0.5``: a performance
    shortfall raises the premium needed to sustain coverage and pushes marginal
    policyholders to lapse, while overfunded policies are stickier.  The bounds stop
    extreme extrapolation.  No public VUL dynamic-behavior study was retrieved, so the
    form is standardized with the notes' rationale.

    **1.0 when the behavior module is off**, which is the default -- see
    :func:`prem_persistency`.
    """
    if not dyn_behavior_on:                                          # noqa: F821
        return 1.0
    raw = 1 + lapse_dyn_beta * (1 - funding_ratio(t))                # noqa: F821
    return min(lapse_dyn_cap, max(lapse_dyn_floor, raw))             # noqa: F821


def lapse_rate(t):
    """q^w,annual: the total annual lapse rate **[std]**.

    ``q^w,base x cliff spike x lambda_t``.  The notes set no cap on the product, unlike
    the fixed-UL chassis's 35% **[std]** cap, and none is imposed: the dynamic
    multiplier is already bounded at 2.0.
    """
    return lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_rate_dyn_mult(t)


def lapse_rate_mth(t):
    """q^w_t: the monthly lapse rate, ``1 - (1 - q^w,annual)^(1/12)`` **[std]**."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """l_t: the number of policies in force at the beginning of policy month t.

    Decrements are end-of-month events, so the number in force is constant through the
    month and every BOM cash flow is weighted by it.  ``pols_if(1) = l_0 =
    pols_if_init()`` and ``l_{t+1} = l_t (1 - q^d_t)(1 - q^w_t)``, which is the
    subtraction below.
    """
    if t == 1:
        return pols_if_init()
    return pols_if(t - 1) - pols_death(t - 1) - pols_lapse(t - 1)


def pols_if_at(t, timing):
    """Number of policies in force at time t, by ``timing``.

    All three ``CashValue_SE`` timings coincide for this product and all equal
    :func:`pols_if`: there is no new business inside a projection and the contract has
    no maturity date, so nothing changes the policy count between BOM and the
    end-of-month decrements.
    """
    if timing in ("BEF_MAT", "BEF_NB", "BEF_DECR"):
        return pols_if(t)
    else:
        raise ValueError("invalid timing")


def pols_death(t):
    """Number of deaths at the end of policy month t, ``l_t x q^d_t``."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Number of surrenders at the end of policy month t.

    ``l_t x (1 - q^d_t) x q^w_t``: death is applied before lapse **[std order]**,
    matching the notes' ``l_{t+1} = l_t (1 - q^d_t)(1 - q^w_t)``.
    """
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    Variable universal life has no maturity date -- at attained age 121 premiums and
    monthly deductions cease, the asset charges continue, and coverage runs to death or
    surrender [S1][S2][S4].  The cells is kept so the in-force roll-forward identity
    has the same shape as in the term and annuity models of this library, where it is
    not zero.
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``"DEATH"``
        ``DB_t^EOM - D_t``: the **full death benefit** less outstanding policy debt
        [S1][S3].  Not ``DB - AV``.  The notes carry an explicit warning here: the
        insurer's liability outflow is the whole death benefit, and seizing the account
        value is the *funding* of part of it.  ``DB - AV`` is the net
        general-account strain, reported separately as :func:`claims_net`.

    ``"LAPSE"``
        ``ncsv_pp(t)``, the cash surrender value net of debt and the surrender charge.

    ``"WITHDRAWAL"``
        ``W(t)``.  The $25 fee is retained by the insurer and is not part of the
        payment.  A withdrawal is a payment on the owner's election rather than a
        claim, so it is *not* one of the ``kind`` values :func:`claims` accepts; this
        branch is the per-policy amount :func:`withdrawals` weights by
        :func:`pols_if`.
    """
    if kind == "DEATH":
        return db_pp_eom(t) - loan_bal_pp(t)
    elif kind == "LAPSE":
        return ncsv_pp(t)
    elif kind == "WITHDRAWAL":
        return wd_pp(t)
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim funded by releasing the account value, by ``kind``.

    Death and surrender both release the end-of-month account value ``AV_t``, because
    decrements follow the investment credit.  ``"MATURITY"`` is zero: the contract has
    no maturity date.
    """
    if kind == "DEATH":
        return av_pp(t) * pols_death(t)
    elif kind == "LAPSE":
        return av_pp(t) * pols_lapse(t)
    elif kind == "MATURITY":
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_over_av(t):
    """Death claims in excess of the account value released.

    ``(claim_pp(t, "DEATH") - AV_t) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin.  It differs from :func:`claims_net` by the
    debt extinguished on death, which the account release also covers.
    """
    return (claim_pp(t, "DEATH") - av_pp(t)) * pols_death(t)


def claims(t, kind=None):
    """Claim outgo in policy month t, optionally by ``kind`` -- the **gross view**.

    ``kind`` is ``"DEATH"`` or ``"LAPSE"``, or ``None`` for the total.  Death claims
    are weighted by :func:`pols_death` and surrenders by :func:`pols_lapse`, both
    end-of-month events.

    Partial withdrawals are **not** claims and are **not** in the ``kind is None``
    total: a withdrawal is a payment on the owner's election rather than an event that
    terminates coverage, and it is reported by :func:`withdrawals` in its own column.
    ``"WITHDRAWAL"`` therefore raises here, while remaining a valid ``kind`` of
    :func:`claim_pp`, which carries the per-policy amount.

    ``claims(t, "DEATH")`` is the notes' ``claim_gross``.  Projecting the net amount at
    risk here instead understates gross benefit outgo and breaks reconciliation with
    statutory exhibits; projecting the full death benefit here *and* separately
    expensing the net amount at risk double counts.  The general-account view is
    derived from the same run in :func:`result_net`.
    """
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    elif kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    elif kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    else:
        raise ValueError("invalid kind")


def claims_net(t):
    """claim_net: the net general-account cost of the deaths in policy month t.

    ``l_t x q^d_t x NAAR_t^EOM`` -- the death benefit less the account value seized to
    fund it.  A **derived report**, not a cash flow: it belongs to the net-of-account
    view in :func:`result_net`, never to :func:`result_cf`.
    """
    return net_amt_at_risk_eom(t) * pols_death(t)


def withdrawals(t):
    """Partial withdrawal payments in policy month t, for the policies in force.

    ``claim_pp(t, "WITHDRAWAL") x l_t`` -- the withdrawal is taken at the monthiversary
    by policies still in force, so it is weighted by :func:`pols_if` and not by a
    decrement.  Zero in every shipped model point, which is the notes' baseline.

    A payment on the owner's election, not a claim: it terminates nothing and it is
    reported in its own ``withdrawals`` column of :func:`result_cf`, outside
    :func:`claims` and outside the ``kind is None`` claim total.  The $25 fee is
    retained by the insurer and is :func:`wd_fees`, not part of this payment.
    """
    return claim_pp(t, "WITHDRAWAL") * pols_if(t)


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force.

    Account-value outgo but not a liability cash flow, so this appears in
    :func:`margin_expense` and not in :func:`claims`.
    """
    return wd_fee_pp(t) * pols_if(t)


def sa_transfer(t):
    """sa_transfer: separate-account value released to the general account (memo).

    On death the subaccount values move separate account to general account; on
    surrender the separate account liquidates to fund the cash surrender value.  The
    fixed option and the loan account release internally and are not part of this.  A
    memo column for reconciliation, not a liability cash flow.
    """
    return (sum(sa_pp(t, i) for i in subaccount_ids())
            * (pols_death(t) + pols_lapse(t)))


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(y - 1)``.

    ``inflation_rate`` is **0.0** here: the variable-UL notes specify a flat $75 per
    policy per year maintenance expense **[std]** with no inflation, where the fixed-UL
    chassis inflates its own at 2.5%.  The cells is kept so the two models read alike
    and so an inflation assumption can be switched on with one Reference.
    """
    return (1 + inflation_rate) ** (policy_year(t) - 1)              # noqa: F821


def expenses(t):
    """The insurer's own maintenance expenses in policy month t **[std]**.

    ``expense_maint / 12`` per policy in force, $75 a year, plus ``expense_acq`` in the
    issue month.  The notes specify no acquisition expense for this product -- the
    premium load and the surrender charge are the contractual acquisition-cost
    recovery, which is income, not outgo -- so ``expense_acq`` is zero and the term is
    carried only so a user can switch it on.

    Not to be confused with :func:`maint_fee`, which is the charge *against the account
    value*.  Internal expense assumptions are not public, so both figures are
    placeholders.
    """
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    return (acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821


def premium_taxes(t):
    """The percent-of-premium collection expense, 2% of premium **[std]**.

    The chassis name; for this product the notes call it a premium collection expense
    rather than a premium tax, but it is the same percent-of-premium line.
    """
    return premium_tax_rate * premiums(t)                            # noqa: F821


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``premium loads + withdrawal fees + maint_fee + surrender charges - expenses
    - premium taxes``.  Follows ``CashValue_SE.margin_expense``.  The M&E charge is
    *not* in it -- it is an asset-based charge on separate-account assets, reported by
    :func:`me_charge` and reconciled in :func:`check_net_view`.
    """
    return (premium_loads(t)
            + wd_fees(t)
            + maint_fee(t)
            + surr_charge(t)
            - expenses(t)
            - premium_taxes(t))


def margin_mortality(t):
    """Mortality margin: :func:`coi` net of :func:`claims_over_av`.

    The gap between the cost of insurance *charged* on the current COI scale and the
    cost of the deaths that actually occur on best-estimate mortality -- the two bases
    the notes insist must never be conflated, meeting here and only here.
    """
    return coi(t) - claims_over_av(t)


def net_cf(t):
    """NetCF(t): net liability cash flow in policy month t, **undiscounted**.

    ``premiums - claims (death and surrender) - withdrawals - expenses - premium
    taxes``: the **gross (policyholder) view**, which the notes make the reference
    model's primary projection.  Withdrawals are a separate term because they are not
    claims -- :func:`claims` no longer carries them -- and dropping them here would
    lose an outgo the account value has already released.  Like the rest of this
    library the model
    projects gross liability cash flows: there is no discounting and no change in
    account value in this figure, because reserves are a separate layer that consumes
    these flows.  Investment credit on the account value is the policyholder's, not an
    insurer cash flow, so it does not appear either -- see :func:`check_margin` and
    :func:`check_net_view` for how it reconciles.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - premium_taxes(t))


def net_cf_ga(t):
    """The net-of-account (general-account strain) view of policy month t.

    ``load_income + md_income + me_income + loan_spread + sc_income - claim_net
    - expense``, the notes' reconciliation identity.  A **derived report** from the
    same run as :func:`net_cf`, not a second projection: :func:`check_net_view` shows
    the gross view reproduces it once the account pass-throughs are added back.
    """
    return (premium_loads(t) + mth_deduction(t) + me_charge(t)
            + loan_spread(t) + surr_charge(t)
            - claims_net(t) - expenses(t) - premium_taxes(t))


def check_av_roll_fwd():
    """Check the account value roll-forward.

    Returns ``True`` when, for every projected month, the opening account value in
    force of month ``t + 1`` equals::

        av_at(t, "BEF_PREM")
            + prem_to_av(t)
            - withdrawals(t)
            - wd_fees(t)
            - mth_deduction(t)
            + inv_income(t)
            - claims_from_av(t, "DEATH")
            - claims_from_av(t, "LAPSE")

    This pins the notes' processing order: that the deduction comes out before growth,
    that growth applies to the post-deduction balance, that the M&E charge is inside
    the investment credit rather than a second deduction, and that the decrements come
    after the credit.
    """
    res = []
    for t in range(1, proj_len() + 1):
        av = (av_at(t, "BEF_PREM")
              + prem_to_av(t)
              - withdrawals(t)
              - wd_fees(t)
              - mth_deduction(t)
              + inv_income(t)
              - claims_from_av(t, "DEATH")
              - claims_from_av(t, "LAPSE"))
        res.append(math.isclose(av_at(t + 1, "BEF_PREM"), av,        # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-9))
    return all(res)


def check_margin():
    """Check the net cash flow against the expense and mortality margins.

    Returns ``True`` when, for every projected month::

        net_cf(t) == margin_expense(t) + margin_mortality(t)
                     + av_change(t) - inv_income(t)
                     + loan_bal_pp(t) * pols_lapse(t)

    The last three terms are what separates a *gross liability cash flow* model from
    ``CashValue_SE``, whose ``net_cf`` already nets the change in account value and the
    investment credit; the loan term is the debt extinguished against the account value
    when a policy with a loan surrenders.  The identity holds while neither the
    :func:`csv_pp` nor the :func:`ncsv_pp` floor binds against a policy loan -- the
    early-duration months of a new-business point have the surrender charge above the
    account value, but they carry no debt, so it holds for every shipped model point.
    """
    res = []
    for t in range(1, proj_len() + 1):
        rhs = (margin_expense(t) + margin_mortality(t)
               + av_change(t) - inv_income(t)
               + loan_bal_pp(t) * pols_lapse(t))
        res.append(math.isclose(net_cf(t), rhs,                      # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-9))
    return all(res)


def check_net_view():
    """Check the gross view against the net-of-account view.

    Returns ``True`` when, for every projected month::

        net_cf(t) == net_cf_ga(t)
                     + av_change(t) - inv_income(t) + wd_fees(t)
                     - me_charge(t) - loan_spread(t)
                     + loan_bal_pp(t) * (pols_death(t) + pols_lapse(t))

    which is the notes' "the gross view must reproduce it after adding back the account
    pass-throughs".  Reading the correction terms: ``av_change - inv_income`` is the
    net premium in and the account releases out; ``- me_charge`` and ``- loan_spread``
    remove the two margins the gross view never sees because they are collected inside
    the accounts; the debt term is the policy debt extinguished against the account
    value on death and on surrender.

    Same floor caveat as :func:`check_margin`.
    """
    res = []
    for t in range(1, proj_len() + 1):
        rhs = (net_cf_ga(t)
               + av_change(t) - inv_income(t) + wd_fees(t)
               - me_charge(t) - loan_spread(t)
               + loan_bal_pp(t) * (pols_death(t) + pols_lapse(t)))
        res.append(math.isclose(net_cf(t), rhs,                      # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-9))
    return all(res)


def result_cf():
    """Result table of the gross-view cash flows, indexed by policy month ``t``.

    The surrender column is ``claims_lapse``, matching the ``"LAPSE"`` kind that
    produces it, and partial withdrawals sit in their own ``withdrawals`` column rather
    than among the claims.  The cash flow columns net to ``net_cf`` under the library's
    income-positive sign; ``pols_if`` is a policy count, not a cash flow.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy decrements, indexed by policy month ``t``."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the per-policy account value roll-forward.

    The columns follow the worked example in the technical notes: the two subaccount
    balances at the start of the month, the net premium, the post-premium account
    value, the death benefit and net amount at risk it is measured against, the cost of
    insurance and the monthly deduction, the post-deduction balance, the two
    end-of-month subaccount balances and the total, then the M&E collected, the
    surrender charge, the cash surrender value and the end-of-month death benefit and
    net amount at risk.
    """
    ts = list(range(1, proj_len() + 1))
    ids = subaccount_ids()
    out = {}
    for i in ids:
        out["sa{}_bef_prem".format(i)] = [sa_pp_at(t, i, "BEF_PREM") for t in ts]
    out["fa_bef_prem"] = [fa_pp_at(t, "BEF_PREM") for t in ts]
    out["prem_to_av_pp"] = [prem_to_av_pp(t) for t in ts]
    out["av_pp_bef_fee"] = [av_pp_at(t, "BEF_FEE") for t in ts]
    out["db_pp"] = [db_pp(t) for t in ts]
    out["net_amt_at_risk"] = [net_amt_at_risk(t) for t in ts]
    out["coi_pp"] = [coi_pp(t) for t in ts]
    out["mth_deduction_pp"] = [mth_deduction_pp(t) for t in ts]
    out["av_pp_bef_inv"] = [av_pp_at(t, "BEF_INV") for t in ts]
    for i in ids:
        out["sa{}_pp".format(i)] = [sa_pp(t, i) for t in ts]
    out["fa_pp"] = [fa_pp(t) for t in ts]
    out["av_pp"] = [av_pp(t) for t in ts]
    out["me_charge_pp"] = [me_charge_pp(t) for t in ts]
    out["surr_charge_pp"] = [surr_charge_pp(t) for t in ts]
    out["ncsv_pp"] = [ncsv_pp(t) for t in ts]
    out["loan_bal_pp"] = [loan_bal_pp(t) for t in ts]
    out["db_pp_eom"] = [db_pp_eom(t) for t in ts]
    out["net_amt_at_risk_eom"] = [net_amt_at_risk_eom(t) for t in ts]
    return pd.DataFrame(out, index=pd.Index(ts, name="t"))           # noqa: F821


def result_net():
    """Result table of the net-of-account (general-account strain) view.

    The notes' derived report: the margins the insurer collects, the net mortality
    cost, and the memo columns for reconciliation.  Column names are the notes' own.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "prem_gross": [premiums(t) for t in ts],
            "load_income": [premium_loads(t) for t in ts],
            "md_income": [mth_deduction(t) for t in ts],
            "me_income": [me_charge(t) for t in ts],
            "loan_spread": [loan_spread(t) for t in ts],
            "claim_gross": [claims(t, "DEATH") for t in ts],
            "claim_net": [claims_net(t) for t in ts],
            "surr_outgo": [claims(t, "LAPSE") for t in ts],
            "sc_income": [surr_charge(t) for t in ts],
            "expense": [expenses(t) + premium_taxes(t) for t in ts],
            "sa_transfer": [sa_transfer(t) for t in ts],
            "av_eop": [av_at(t, "EOM") for t in ts],
            "naar": [net_amt_at_risk_eom(t) for t in ts],
            "pols_if": [pols_if(t) for t in ts],
            "net_cf_ga": [net_cf_ga(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 121

charges_cease_age = 121

expense_pol_mth = 10.0

expense_unit_mth = 0.2

me_rate_ann = 0.0045

coi_curr_factor = 0.5

coi_rate_cap = 83.34

guar_rate_ann = 0.01

crediting_rate_curr = 0.01

loan_rate_ann_std = 0.02

loan_rate_ann_pref = 0.0105

loan_cr_rate_ann_lvl = 0.01

loan_pref_year = 10

wd_fee = 25.0

mort_ae_factor = 1.0

lapse_shock_mult = 1.0

dyn_behavior_on = False

pricing_return_ann = 0.06

lapse_dyn_beta = 0.5

lapse_dyn_floor = 0.5

lapse_dyn_cap = 2.0

prem_pers_delta = 0.25

prem_pers_floor = 0.7

prem_pers_cap = 1.3

expense_acq = 0.0

expense_maint = 75.0

inflation_rate = 0.0

premium_tax_rate = 0.02

pd = ("Module", "pandas")

math = ("Module", "math")