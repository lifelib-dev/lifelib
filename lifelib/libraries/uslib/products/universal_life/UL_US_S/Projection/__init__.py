# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.UL_US_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_av()          # the worked-example anchor cell
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/universal_life/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``UL_US_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

The readers live in the unparameterized :mod:`~.UL_US_S.Data` Space, reached
here through the ``data`` Reference, so each file is read once per model rather than
once per model point:

======================  ================================  ==========================
Reference (on Data)     Cells                             File
======================  ================================  ==========================
model_point_file        data.model_point_table()          model_point_table.csv
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
at ``t = 0`` -- ``AV(0)``, ``L(0)``, ``F(0)``, ``l(0) = 1`` -- are the ``t == 0``
branch of the corresponding recursion.

Within each month the notes' monthiversary order is followed exactly:

1. amortize the surrender charge (:func:`surr_charge_rate`);
2. gross premium and its load, net premium to the account value
   (:func:`premium_pp`, :func:`prem_to_av_pp`);
3. withdrawal and withdrawal fee, and under Option A the face reduction they force
   (:func:`wd_pp`, :func:`wd_fee_pp`, :func:`sum_assured_at`) -- after which the
   account value is the notes' ``AV'(t)``, :func:`av_pp_at(t, "BEF_FEE")<av_pp_at>`;
4. death benefit and the GPT corridor test (:func:`db_pp`);
5. net amount at risk, the death benefit discounted one month at the **guaranteed**
   rate less the account value measured **before** the deduction
   (:func:`net_amt_at_risk`);
6. the monthly deduction (:func:`mth_deduction_pp`);
7. the shortfall test (:func:`is_shortfall`);
8. end of month: one month's interest on the post-deduction balance
   (:func:`inv_income_pp`) and loan interest accrual (:func:`loan_bal_pp`);
9. end of month: decrements, death before lapse (:func:`pols_death`,
   :func:`pols_lapse`).

Cash flows are **undiscounted**. Premiums, expenses and premium taxes fall at BOM and
are weighted by ``pols_if(t)``; death claims by ``pols_if(t) * mort_rate_mth(t)``;
surrender payments by ``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``.
Partial withdrawals also fall at BOM and are weighted by ``pols_if(t)``, but they are
:func:`withdrawals`, a cash flow line of their own rather than a ``kind`` of
:func:`claims`.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue -- ``pols_*`` for policy counts, ``av_*`` for
account values, plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for
per-policy amounts, ``timing`` and ``kind`` string arguments. The technical notes use
compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Policy month, 1-based
y                          policy_year(t)                  Policy year, ceil(t/12)
(t - 1 in months)          duration_mth(t)                 Completed policy months
(y - 1)                    duration(t)                     Completed policy years
x / issue_age              age_at_entry                    Issue age (ANB)
x + y - 1                  age(t)                          Attained age (ANB)
(none)                     proj_len                        Last projected month
sex                        sex                             Sex, M or F
risk_class                 rate_class                      Underwriting class, one of six
F / face_amount            sum_assured                     Initial total face amount
F(t)                       sum_assured_at(t)               Total face after reductions
U                          units(t)                        Face in $1,000 units
db_option                  db_option                       Death benefit option, A or B
qual_test                  qual_test                       7702 test elected; GPT only
premium_pattern            premium_type                    LEVEL / SINGLE / TARGET
premium_mode               (not modelled)                  Monthly premiums only **[std]**
planned_premium_annual     premium_pp_ann                  Planned annual premium
av_initial / AV(0)         av_pp_init                      Opening account value
loan_balance_initial       loan_bal_init                   Opening loan balance, L(0)
policy_month_offset        duration_mth_init               Completed months at t = 1
sc_layer_table             surr_charge_id                  Surrender charge schedule ID
(schedule applies)         has_surr_charge                 Whether a schedule applies
guideline_single_premium   gsp                             GSP in the GPT limit
guideline_level_premium    glp                             GLP in the GPT limit
seven_pay_premium          seven_pay_prem                  7-pay premium, an input
GP(t)                      premium_pp(t)                   Gross premium per policy
pp(y)                      prem_persistency(t)             Paid/planned factor
pl                         load_prem_rate                  Current premium load rate
NP(t)                      prem_to_av_pp(t)                Net premium to account value
W(t)                       wd_pp(t)                        Partial withdrawal
wf                         wd_fee_pp(t)                    Withdrawal fee ($25)
(free amount)              wd_free_pp(t)                   Free allowance still available
wd_used_year               wd_used_year(t)                 Free allowance used this year
(face cut)                 face_reduction_pp(t)            Option A face reduction
AV(t)                      av_pp(t)                        Account value, end of month
AV(t-1)                    av_pp_at(t, "BEF_PREM")         Account value, start of month
(after premium)            av_pp_at(t, "BEF_WD")           Before the withdrawal
AV'(t)                     av_pp_at(t, "BEF_FEE")          After premium and withdrawal
(AV'(t) floored at 0)      av_pp_db_basis(t)               The AV' that DB and NAAR use
AV'(t) - MD(t)             av_pp_at(t, "BEF_INV")          After the monthly deduction
(aggregate AV)             av_at(t, timing)                Account value in force
(none)                     av_change(t)                    Change in account value
e_pol                      expense_pol_mth                 Per-policy charge
e_unit(y)                  expense_unit_mth_1/_2           Per-unit charge
rc(t)                      rider_charge_pp(t)              Rider charges (0)
(e_pol + e_unit U + rc)    maint_fee_pp(t)                 Non-COI monthly charges
MD(t)                      mth_deduction_pp(t)             Monthly deduction
q_coi_guar(s)              coi_rate_guar(t)                Guaranteed maximum COI rate
q_coi(s)                   coi_rate(t)                     Current COI rate
(COI charge)               coi_pp(t)                       Cost of insurance charge
NAAR(t)                    net_amt_at_risk(t)              Net amount at risk
DB(t)                      db_pp(t)                        Death benefit after corridor
cf(a)                      corridor_factor(t)              GPT corridor factor
(NAAR factor)              naar_factor                     1 + i_gm
i_guar                     guar_rate_ann                   Guaranteed annual rate
i_cr                       crediting_rate_ann(t)           Current credited annual rate
i_m                        inv_return_mth(t)               Monthly credited rate
i_gm                       guar_rate_mth                   Monthly guaranteed rate
(interest credited)        inv_income_pp(t)                Interest credited to AV
earned_rate(t)             (not modelled)                  NGE revision input, no source
L(t)                       loan_bal_pp(t)                  Policy loan balance
r_L                        loan_rate_ann                   Charged loan rate
SC(t)                      surr_charge_pp(t)               Surrender charge
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
CSV(t)                     csv_pp(t)                       Cash surrender value
NCSV(t)                    ncsv_pp(t)                      Net cash surrender value
(SC retained)              surr_charge(t)                  Surrender charge collected
CumPrem(t)                 cum_prem_pp(t)                  Cumulative premiums
(GPT limit)                gpt_limit(t)                    max(GSP, GLP x years)
(GPT test)                 gpt_ok(t)                       GPT compliance flag
(7-pay limit)              seven_pay_limit(t)              7-pay cumulative limit
(MEC flag)                 is_mec(t)                       7-pay failure flag, latched
(grace trigger)            is_shortfall(t)                 AV' - L < MD
grace_flag(t)              (not modelled)                  In-grace state; see below
(cure payment)             cure_premium_pp(t)              3 x MD plus load
q_m(t)                     mort_rate_mth(t)                Monthly mortality rate
(annual q)                 mort_rate(t)                    Annual mortality rate
w_base(y)                  lapse_rate_base(t)              Base annual lapse rate
M_sc                       lapse_rate_sc_mult(t)           SC-expiry lapse shock
M_rate(t)                  lapse_rate_dyn_mult(t)          Dynamic lapse multiplier
r_comp(t)                  comp_rate_ann(t)                Competitor new-money rate
w_annual(y,t)              lapse_rate(t)                   Total annual lapse rate
w_m(t)                     lapse_rate_mth(t)               Monthly lapse rate
l(t-1)                     pols_if(t)                      In force at start of month t
(l(0))                     pols_if_init                    In force at outset
(deaths)                   pols_death(t)                   Deaths in month t
(lapses)                   pols_lapse(t)                   Lapses in month t
(none)                     pols_maturity(t)                Maturities: always zero
(premium income)           premiums(t)                     Premium income
(death claims)             claims(t, "DEATH")              Death claims
(surrender outgo)          claims(t, "LAPSE")              Surrender payments
(withdrawal outgo)         withdrawals(t)                  Withdrawal payments
(maintenance)              expenses(t)                     Maintenance expenses
(percent of premium)       premium_taxes(t)                Premium tax / %-of-premium
NetCF(t)                   net_cf(t)                       Net liability cash flow
=========================  ==============================  ==========================

The table covers every symbol the notes define: the Model point attributes table, the
State variables table and the notation list, in that order, followed by the cash flow
rows. Three symbols have **no cells at all**, and are carried in the table as ``(not
modelled)`` so that the absence is recorded rather than silent: ``grace_flag(t)``, the
one of the notes' ten state variables with no counterpart here, because the grace
cascade is a diagnostic and no in-grace state is held (:func:`is_shortfall`);
``premium_mode``, because every premium in this model is monthly **[std]**; and
``earned_rate(t)``, the input the notes' optional NGE revision rule would need
(:func:`crediting_rate_ann`).

Eight names needed care.

The notes' ``risk_class`` is :func:`rate_class` here, and the model point table column
is ``rate_class`` too. The name is taken from ``Term_US_A``/``BasicTerm_S``, which
this library follows ahead of the notes wherever the two collide; ``rate_class`` also
avoids reading as Python's ``class``. The six classes themselves are the product
spec's, unchanged.

``l(t)`` in the notes is the in-force probability at the **end** of month ``t``, while
``pols_if(t)`` follows ``BasicTerm_S`` and is the number in force at the **start** of
month ``t``; so ``pols_if(t) = l(t-1)``, and ``pols_if(1) = l(0) = pols_if_init()``.
Every BOM cash flow is weighted by ``pols_if(t)``, which is the notes' own
``l(t-1)`` weighting.

The notes write the monthly deduction as ``MD(t)`` and split it into a per-policy
charge, a per-unit charge, rider charges and the COI charge. ``CashValue_SE`` calls the
non-COI part of an account-value deduction ``maint_fee``; that name is kept here for
:func:`maint_fee_pp`, and :func:`mth_deduction_pp` is the notes' ``MD(t)`` in full.
:func:`expenses` is something different -- the insurer's own **[std]** maintenance
expense of $75 per policy per year, a cash flow, not a charge against the account
value. The two must not be confused: ``maint_fee`` is income, ``expenses`` is outgo.

The notes' ``t`` in the surrender-charge formula ``SC(t) = max(0, (9.00 - t/12) x U)``
counts the current month, so it equals ``duration_mth(t) + 1``, not ``duration_mth(t)``.
:func:`surr_charge_rate` says so explicitly; getting it wrong shifts the whole run-off
by a month.

``q_coi`` is quoted per $1,000 of net amount at risk **per month** and ``e_unit`` per
$1,000 of face per month, so both are divided by 1,000 -- or multiplied by
:func:`units` -- before they meet a currency amount. :func:`coi_rate` is therefore not
comparable with ``CashValue_SE.coi_rate``, which is a rate per unit of account value.

``surr_charge_pp(t)`` is the surrender charge *scheduled* at month ``t``;
``surr_charge(t)`` is the amount actually *collected* from lapsing policies, which is
capped by the account value because :func:`csv_pp` is floored at zero. In the first
policy years the schedule exceeds the account value and the two differ by a lot.

The notes' cash flow table lists "Withdrawal outgo" beside "Death claims" and
"Surrender outgo", but a partial withdrawal is a payment made on the **owner's
election**, not on a contingency, so it is not a claim here: it is :func:`withdrawals`,
its own cash flow line and its own ``result_cf()`` column, and ``"WITHDRAWAL"`` is not
a ``kind`` of :func:`claims` or of :func:`claim_pp`. The consequence to hold on to is
that ``claims(t)`` with no ``kind`` is the death and surrender total *only*, so
:func:`net_cf` subtracts :func:`withdrawals` as a separate term. The per-policy amount
stays :func:`wd_pp`, which is the notes' ``W(t)``.

Finally, the notes write ``AV'(t)`` for one quantity and use it for two: the balance
the monthly deduction comes out of, and the balance the death benefit and the net
amount at risk are measured against. The two coincide until a policy in permanent
shortfall drives the account value negative -- which this model does not prevent,
because it does not terminate such a policy (:func:`is_shortfall`).
:func:`av_pp_at(t, "BEF_FEE")<av_pp_at>` is the first and stays signed;
:func:`av_pp_db_basis` is the second and is floored at zero **[std]**, so an Option B
death benefit can never fall below the face amount.
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
    """The initial total face amount F of the selected model point."""
    return float(model_point()["sum_assured"])


def db_option():
    """The death benefit option: ``"A"`` (level) or ``"B"`` (face plus account value).

    Option C (return of premium) is out of scope in the product spec.
    """
    return model_point()["db_option"]


def qual_test():
    """The IRC 7702 qualification test elected at issue; only ``"GPT"`` is modeled.

    CVAT is out of scope in the product spec, so :func:`corridor_factor` raises on
    anything else rather than silently applying GPT corridor factors.
    """
    return model_point()["qual_test"]


def premium_type():
    """The premium pattern: ``"LEVEL"``, ``"SINGLE"`` or ``"TARGET"`` **[std]**."""
    return model_point()["premium_type"]


def premium_pp_ann():
    """The planned annual premium per policy; a billing target only [S3]."""
    return float(model_point()["premium_pp_ann"])


def load_prem_rate():
    """The current premium load rate, 6% **[std]** (guaranteed maximum 9%) [S1].

    The load is itself a non-guaranteed element in the source design, which is why it
    sits in the model point table rather than in a Reference.
    """
    return float(model_point()["load_prem_rate"])


def av_pp_init():
    """AV(0): the account value per policy at the outset, 0 at issue."""
    return float(model_point()["av_pp_init"])


def loan_bal_init():
    """L(0): the policy loan balance per policy at the outset, 0 at issue."""
    return float(model_point()["loan_bal_init"])


def pols_if_init():
    """l(0): the in-force probability at the outset, 1 for a single-policy point."""
    return float(model_point()["pols_if_init"])


def duration_mth_init():
    """Completed policy months already elapsed when the projection starts.

    0 for a new-business model point, so that ``t = 1`` is the issue month; positive
    for an in-force cell.  This is the notes' ``policy_month_offset``.
    """
    return int(model_point()["duration_mth"])


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point."""
    return bool(model_point()["has_surr_charge"])


def surr_charge_id():
    """The surrender charge schedule ID, a row label of *surr_charge_table.csv*."""
    return model_point()["surr_charge_id"]


def gsp():
    """The guideline single premium (GPT compliance input) [S3]."""
    return float(model_point()["gsp"])


def glp():
    """The guideline level premium (GPT compliance input) [S3]."""
    return float(model_point()["glp"])


def seven_pay_prem():
    """The 7-pay premium (IRC 7702A compliance input) [S3]."""
    return float(model_point()["seven_pay_prem"])


def duration_mth(t):
    """Completed policy months at the beginning of policy month t.

    ``duration_mth_init() + t - 1``, so it is 0 in the issue month of a new-business
    model point.  Note the contrast with the notes' own ``t``, which counts the
    current month as well; see :func:`surr_charge_rate`.
    """
    return duration_mth_init() + t - 1


def duration(t):
    """Completed policy years at the beginning of policy month t."""
    return duration_mth(t) // 12


def policy_year(t):
    """y: the policy year containing policy month t, 1-based."""
    return duration(t) + 1


def age(t):
    """The attained age (ANB) in policy month t: ``age_at_entry() + duration(t)``.

    This is the notes' ``x + y - 1``.  Age changes on the policy anniversary, not on
    the birthday, which is the ANB convention the whole model is built on **[std]**.
    """
    return age_at_entry() + duration(t)


def proj_len():
    """Projection length in policy months.

    ``12 * (omega_age - age_at_entry() + 1) - duration_mth_init()``: the projection
    runs through the policy year in which the insured attains ``omega_age`` (120), the
    last age of *mort_table.csv*, where the annual rate is 1.0.  The contract has no
    maturity date [S2][S3]; the projection is truncated by mortality, not by the
    policy.
    """
    return 12 * (omega_age - age_at_entry() + 1) - duration_mth_init()  # noqa: F821


def crediting_rate_ann(t):
    """i_cr: the current declared annual effective credited rate, 4.00% **[std]**.

    A non-guaranteed element under ASOP 2 [R8].  The base deterministic run holds the
    snapshot scale level, as the notes prescribe.  The notes' optional revision rule
    ``i_cr(t) = max(i_guar, earned_rate(t) - spread)`` needs an earned-rate input the
    notes do not supply and is not implemented.
    """
    return crediting_rate_curr                                       # noqa: F821


def inv_return_mth(t):
    """i_m: the monthly credited rate, ``(1 + i_cr)^(1/12) - 1``.

    0.0032737 at the **[std]** 4.00% current rate.  The contract credits daily on a
    365-day year [S3]; monthly compounding is the model's discretization **[std]** --
    do not also compound daily.
    """
    return (1 + crediting_rate_ann(t)) ** (1 / 12) - 1


def guar_rate_mth():
    """i_gm: the monthly guaranteed rate, ``(1 + i_guar)^(1/12) - 1`` = 0.0016516."""
    return (1 + guar_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def naar_factor():
    """The specimen's NAAR factor, ``1 + i_gm`` = 1.0016516 **[std]** at 2% [S3].

    The death benefit is discounted one month at the **guaranteed** rate, never the
    credited rate; the specimen prints 1.0024663 = 1.03^(1/12) at its own 3%
    guarantee [S3].
    """
    return 1 + guar_rate_mth()


def loan_rate_mth():
    """The monthly charged loan rate, ``(1 + r_L)^(1/12) - 1`` at r_L = 2.75%.

    The contract accrues daily and capitalizes annually [S3]; monthly compounding is
    the model's discretization **[std]**.
    """
    return (1 + loan_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def prem_persistency(t):
    """pp(y): the fraction of the planned premium actually paid in policy year y **[std]**.

    100% in year 1, declining 2 percentage points a year to a 70% floor from year 16,
    read from *prem_persistency.csv*.  Policy years beyond the table take its last
    row.  The shape is informed qualitatively by the SOA/LIMRA UL study [R7]; the
    levels are a standardization.
    """
    tbl = data.prem_persistency_table()                              # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "prem_persistency"])


def premium_pp(t):
    """GP(t): the gross premium per policy received at BOM of policy month t.

    ``LEVEL``  planned annual premium / 12, times :func:`prem_persistency`.
    ``SINGLE`` one premium in the issue month, capped at the guideline single premium.
    ``TARGET`` as ``LEVEL`` but capped so cumulative premium stays inside the GPT
    limit **[std]**; the cap looks at ``cum_prem_pp(t - 1)``, so there is no
    circularity.

    Zero from attained age 121, when premiums are no longer accepted [S2][S3].
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    if premium_type() == "SINGLE":
        return min(premium_pp_ann(), gsp()) if duration_mth(t) == 0 else 0.0
    elif premium_type() == "LEVEL":
        return premium_pp_ann() / 12 * prem_persistency(t)
    elif premium_type() == "TARGET":
        level = premium_pp_ann() / 12 * prem_persistency(t)
        return min(level, max(0.0, gpt_limit(t) - cum_prem_pp(t - 1)))
    else:
        raise ValueError("invalid premium type")


def prem_to_av_pp(t):
    """NP(t): the net premium credited to the account value, ``GP(t) x (1 - pl)``."""
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_av(t):
    """Net premium credited to account value, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """Premium income at BOM of policy month t, weighted by the in force at BOM."""
    return premium_pp(t) * pols_if(t)


def wd_pp(t):
    """W(t): the partial withdrawal per policy at BOM of policy month t.

    Withdrawals are allowed on and after the first policy anniversary and not after
    attained age 121 [S2][S3].  The amount is the constant monthly figure in the model
    point's ``wd_pp`` column, **0 in every shipped model point**: the notes give no
    withdrawal utilization pattern, so the mechanics are implemented and the behaviour
    is left to the data **[std]**.
    """
    if duration_mth(t) < 12 * wd_first_year:                         # noqa: F821
        return 0.0
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return float(model_point()["wd_pp"])


def wd_used_year(t):
    """The free-withdrawal allowance already consumed in the current policy year.

    The notes' ``wd_used_year`` state variable, "free-withdrawal usage in current
    policy year, updated on withdrawal": reset to zero on each policy anniversary and
    increased month by month by the free part of each withdrawal taken since,
    ``min(W(t-1), wd_free_pp(t-1))``.

    This is what makes the notes' allowance an **annual** one.  Without it the 10% is
    granted afresh every month, and a policyholder withdrawing 10% of the account value
    every month takes twelve full annual allowances in a policy year and never triggers
    the Option A face reduction of :func:`face_reduction_pp`.

    Zero at ``t = 1`` for an in-force model point as well: the notes give no opening
    withdrawal-usage attribute, so the first projected policy year starts unused
    **[std]**.
    """
    if t <= 1 or duration_mth(t) % 12 == 0:
        return 0.0
    return wd_used_year(t - 1) + min(wd_pp(t - 1), wd_free_pp(t - 1))


def wd_free_pp(t):
    """The free partial withdrawal allowance still available in policy month t **[std]**.

    ``max(0, 10% of AV - wd_used_year(t))``: the allowance is 10% of the account value
    measured after the premium and before the withdrawal, less the part of it already
    taken earlier in the same policy year, and it resets on each policy anniversary --
    the notes' "free-amount rule (10% of AV per policy year)" with its ``wd_used_year``
    state (:func:`wd_used_year`).  In the first withdrawal month of a policy year
    nothing is used yet and this is the full 10%.

    The specimen's carve-out is the lesser of $10,000 and 10% of net cash surrender
    value, on the first withdrawal of each of the first 15 policy years [S3]; the
    composite simplifies to 10% of the account value, with no dollar cap and no
    15-year limit **[std]**.
    """
    allowance = wd_free_rate * av_pp_at(t, "BEF_WD")                 # noqa: F821
    return max(0.0, allowance - wd_used_year(t))


def wd_fee_pp(t):
    """wf: the $25 withdrawal fee, charged only in a month with a withdrawal [S2][S3].

    The fee is retained by the insurer, so it is account-value outgo but not a
    liability cash flow; it appears in :func:`margin_expense`, not in :func:`claims`.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def face_reduction_pp(t):
    """The total face reduction forced by a withdrawal under Option A [S3].

    Under Option A a withdrawal beyond the free amount would otherwise increase the
    net amount at risk, so the face is cut by the excess.  The free amount is whatever
    is left of the policy year's allowance (:func:`wd_free_pp`), not a fresh 10% each
    month.  Under Option B the withdrawal reduces the account value only, and this is
    zero.
    """
    if db_option() != "A" or wd_pp(t) <= 0:
        return 0.0
    return max(0.0, wd_pp(t) - wd_free_pp(t))


def sum_assured_at(t):
    """F(t): the total face amount after any withdrawal-driven reductions.

    ``F(0) = sum_assured()``; face increases, elective decreases and option changes
    are not modeled, so the only movement is the Option A withdrawal reduction.
    """
    if t == 0:
        return sum_assured()
    return max(0.0, sum_assured_at(t - 1) - face_reduction_pp(t))


def units(t):
    """U: the total face amount in $1,000 units, ``sum_assured_at(t) / 1000``.

    The per-unit charge is quoted per $1,000 of face per month, so it is multiplied by
    this.  The surrender charge is quoted per $1,000 of **initial** face, because face
    decreases do not reduce it [S3]; see :func:`surr_charge_pp`.
    """
    return sum_assured_at(t) / 1000


def corridor_factor(t):
    """cf(a): the GPT corridor factor at the attained age [S3][R2].

    250% to age 40, grading to 101% above age 93.  Ages beyond the table take its last
    row.  Only the Guideline Premium Test is modeled; CVAT is out of scope in the
    product spec, so any other ``qual_test`` raises rather than being treated as GPT.
    """
    if qual_test() != "GPT":
        raise ValueError("invalid qual_test")
    tbl = data.corridor_factors()                                    # noqa: F821
    a = min(max(age(t), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[a, "corridor_factor"])


def av_pp_db_basis(t):
    """AV'(t) floored at zero: the balance the death benefit is measured against.

    The notes' step 4 sets the Option B death benefit to ``F + AV'(t)`` and step 5
    measures the net amount at risk against the same ``AV'(t)``, both on the premise
    that ``AV'`` is a real account balance.  It stops being one as soon as a policy in
    permanent shortfall keeps being projected: the grace and lapse-for-insufficiency
    cascade is not implemented (see :func:`is_shortfall`), so nothing terminates such a
    policy and its account value runs deeply negative.  Fed to ``F + AV'`` unfloored
    that gives an Option B death benefit **below the face amount**, and in the end a
    negative one -- a death claim paid *by* the beneficiary, which no universal life
    contract can produce.

    Flooring the balance at zero here is **[std]**, and is the same floor
    :func:`csv_pp` already carries for the same reason: a negative account balance is
    an artifact of the missing termination, not a contract state.  It holds the Option
    B death benefit at or above the face amount, and it stops the net amount at risk
    from growing with the shortfall and charging COI on a fund that is not there.

    Wherever ``AV'(t) >= 0`` -- every month of model points 1 and 3, and the first 677
    of point 2's 1,032 months -- this is exactly ``av_pp_at(t, "BEF_FEE")`` and changes
    nothing, so the worked example is untouched.
    """
    return max(0.0, av_pp_at(t, "BEF_FEE"))


def db_pp(t):
    """DB(t): the death benefit per policy after the corridor test [S1][S3].

    ``max(option_db, cf(a) x AV'(t))`` where ``option_db`` is the face amount under
    Option A and face plus account value under Option B, and ``AV'(t)`` is the account
    value after premium and withdrawal and **before** the monthly deduction.  Taking
    the account value at that point is what removes the circularity the notes warn
    about: under Option B the death benefit depends on the account value and the net
    amount at risk depends on the death benefit, but with this BOM ordering neither
    depends on the deduction.

    The ``AV'(t)`` used here is :func:`av_pp_db_basis`, floored at zero **[std]**, so
    the death benefit is never less than the face amount; see that cells for why the
    floor is needed at all.
    """
    av = av_pp_db_basis(t)
    if db_option() == "A":
        opt = sum_assured_at(t)
    elif db_option() == "B":
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor(t) * av)


def net_amt_at_risk(t):
    """NAAR(t): ``DB(t) / (1 + i_gm) - AV'(t)``, floored at zero [S3].

    Two conventions here are the specimen's, not conveniences: the death benefit is
    discounted one month at the **guaranteed** rate (:func:`naar_factor`), and the
    account value is measured **before** the monthly deduction.  Using the credited
    rate in the discount, or the post-deduction account value, makes the COI charge
    implicit and requires iteration, and produces small systematic COI errors.

    The ``AV'(t)`` subtracted is :func:`av_pp_db_basis`, the same floored balance the
    death benefit is measured on, so the two sides of the subtraction stay consistent.
    """
    return max(0.0, db_pp(t) / naar_factor() - av_pp_db_basis(t))


def coi_rate_scale():
    """The guaranteed maximum monthly COI scale for this model point's cell.

    A Series indexed by policy year, per $1,000 of net amount at risk, sliced once
    from *coi_rates.csv* for this ``sex`` / ``rate_class`` / ``age_at_entry``.  The
    shipped table covers the specimen anchor cell M / StdNT / 35 only; a model point
    on any other cell needs the table extended first.
    """
    return data.coi_rates().loc[                                     # noqa: F821
        (sex(), rate_class(), age_at_entry())]["coi_rate_guar"]


def coi_rate_guar(t):
    """q_coi_guar(s): the guaranteed maximum monthly COI rate per $1,000 NAAR [S3].

    A 2001 CSO-era specimen table, log-linearly interpolated between the printed
    anchor years **[std]**; it grades to 1000/12 at attained ages 112-120 and to zero
    from attained age 121.  Policy years beyond the table take its last row.
    """
    scale = coi_rate_scale()
    y = min(policy_year(t), int(scale.index.max()))
    return float(scale[y])


def coi_rate(t):
    """q_coi(s): the current monthly COI rate, ``coi_curr_factor`` x guaranteed **[std]**.

    60% of the guaranteed maximum at every duration.  Current COI scales are not
    published -- only guaranteed maxima appear in the specimen [S3] -- so this factor
    is a pure modeling assumption and one of the two assumptions to sensitivity-test
    first.

    Note the units: this is per $1,000 of net amount at risk per **month**, so it is
    divided by 1,000 in :func:`coi_pp`.  It is not comparable with
    ``CashValue_SE.coi_rate``, which is a rate per unit of account value.
    """
    return coi_curr_factor * coi_rate_guar(t)                        # noqa: F821


def coi_pp(t):
    """The cost of insurance charge per policy, ``q_coi(y) / 1000 x NAAR(t)`` [S3].

    Zero from attained age 121, when monthly deductions cease [S2][S3].
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def coi(t):
    """Cost of insurance charges deducted from account values, for the policies in force."""
    return coi_pp(t) * pols_if(t)


def rider_charge_pp(t):
    """rc(t): rider charges, 0 in the base model **[std]**.

    The notes carry this term in the monthly deduction so that rider modules can be
    added without changing the recursion [S3].
    """
    return 0.0


def maint_fee_pp(t):
    """The non-COI part of the monthly deduction per policy [S3].

    ``e_pol + e_unit(y) x U + rc(t)``: the $7.50 per-policy administrative charge, the
    per-unit coverage charge of $0.26 per $1,000 of face per month in policy years
    1-10 and $0.156 thereafter, and rider charges.  Zero from attained age 121, when
    charges cease [S2][S3].

    The name follows ``CashValue_SE.maint_fee``: this is a *charge* against the
    account value and therefore insurer income.  It is not :func:`expenses`, which is
    the insurer's own outgo.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    if policy_year(t) <= expense_unit_step_year:                     # noqa: F821
        e_unit = expense_unit_mth_1                                  # noqa: F821
    else:
        e_unit = expense_unit_mth_2                                  # noqa: F821
    return expense_pol_mth + e_unit * units(t) + rider_charge_pp(t)  # noqa: F821


def maint_fee(t):
    """Non-COI monthly charges deducted from account values, for the policies in force."""
    return maint_fee_pp(t) * pols_if(t)


def mth_deduction_pp(t):
    """MD(t): the monthly deduction per policy, taken at BOM [S3].

    ``e_pol + e_unit(y) x U + rc(t) + q_coi(y) / 1000 x NAAR(t)``, i.e.
    :func:`maint_fee_pp` plus :func:`coi_pp`.  The deduction at the start of month t
    pays for month t's coverage: the specimen says the deduction provides coverage for
    the following policy month, which with BOM indexing is the month it is taken in.
    """
    return maint_fee_pp(t) + coi_pp(t)


def mth_deduction(t):
    """Monthly deductions taken from account values, for the policies in force."""
    return mth_deduction_pp(t) * pols_if(t)


def av_pp_at(t, timing):
    """Account value per policy at an intra-month point of policy month t.

    The BOM events change the balance in this order, and ``timing`` names the point
    just before each of them:

    ``"BEF_PREM"``
        Before the premium: the closing balance of the previous month, ``AV(t-1)``.

    ``"BEF_WD"``
        After the net premium, before the withdrawal.

    ``"BEF_FEE"``
        After the withdrawal and its fee, before the monthly deduction.  This is the
        notes' ``AV'(t)``, and the balance the death benefit, corridor test and net
        amount at risk are all measured against.

    ``"BEF_INV"``
        After the monthly deduction, before interest.  Interest is credited on this
        post-deduction balance; reversing the two overstates the account value by
        about one month's interest on the deduction every month.

    The end-of-month balance ``AV(t)`` is :func:`av_pp`.
    """
    if timing == "BEF_PREM":
        return av_pp(t - 1)
    elif timing == "BEF_WD":
        return av_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)
    elif timing == "BEF_FEE":
        return av_pp_at(t, "BEF_WD") - wd_pp(t) - wd_fee_pp(t)
    elif timing == "BEF_INV":
        return av_pp_at(t, "BEF_FEE") - mth_deduction_pp(t)
    else:
        raise ValueError("invalid timing")


def inv_income_pp(t):
    """Interest credited to the account value per policy at EOM of policy month t.

    The unloaned part of the post-deduction balance earns the current monthly rate and
    the loaned part earns the guaranteed monthly rate [S2][S3]::

        (AV'(t) - MD(t) - L(t-1)) x i_m + L(t-1) x i_gm

    which is the notes' step 8 rearranged.  The loaned portion is taken as the opening
    loan balance exactly, as the notes write it, without capping it at the account
    value.
    """
    loaned = loan_bal_pp(t - 1)
    unloaned = av_pp_at(t, "BEF_INV") - loaned
    return unloaned * inv_return_mth(t) + loaned * guar_rate_mth()


def av_pp(t):
    """AV(t): the account value per policy at the end of policy month t.

    ``AV(0) = av_pp_init()``; thereafter the post-deduction balance plus one month's
    interest.  With no loans and no withdrawals this collapses to the notes' core
    recursion ``AV(t) = [AV(t-1) + NP(t) - MD(t)] x (1 + i_m)``, which reproduces the
    contractual policy-date rule that the account value equals the net premium less
    the first monthly deduction [S3].
    """
    if t == 0:
        return av_pp_init()
    return av_pp_at(t, "BEF_INV") + inv_income_pp(t)


def loan_bal_pp(t):
    """L(t): the policy loan balance per policy at the end of policy month t.

    ``L(0) = loan_bal_init()``; thereafter ``L(t-1) x (1 + r_L)^(1/12)``.  Interest
    accrues daily and is capitalized annually under the contract [S3]; monthly
    compounding is the model's discretization **[std]**.  New loans and repayments are
    not modeled -- the notes give no utilization pattern -- so this only rolls the
    model point's opening balance forward.
    """
    if t == 0:
        return loan_bal_init()
    return loan_bal_pp(t - 1) * (1 + loan_rate_mth())


def av_at(t, timing):
    """Account value in force at an intra-month point of policy month t.

    :func:`av_pp_at` times the number of policies in force, which is constant through
    the month because decrements are end-of-month events.  ``timing`` takes the same
    values as :func:`av_pp_at`, plus ``"EOM"`` for the closing balance before
    decrements.
    """
    if timing == "EOM":
        return av_pp(t) * pols_if(t)
    return av_pp_at(t, timing) * pols_if(t)


def inv_income(t):
    """Interest credited to account values, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month's interest.
    """
    return inv_income_pp(t) * pols_if(t)


def av_change(t):
    """Change in the account value in force over policy month t.

    ``av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")``, following ``CashValue_SE``.
    """
    return av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")


def surr_charge_rate(t):
    """SC per $1,000 of initial face in policy month t **[std amount; mechanics [S3]]**.

    ``max(0, sc_init - (sc_init / runoff_years) x m / 12)`` where ``m`` is the notes'
    own month index ``duration_mth(t) + 1`` -- the current month counts.  With the
    shipped schedule of $9.00 per $1,000 running off over 9 years this is the notes'
    ``max(0, 9.00 - t/12)``: $8.916667 in the issue month, zero from the last month of
    policy year 9 onward.  Reading the notes' ``t`` as ``duration_mth(t)`` instead
    would shift the entire run-off by a month.
    """
    if not has_surr_charge():
        return 0.0
    row = data.surr_charge_table().loc[surr_charge_id()]             # noqa: F821
    init = float(row["sc_per_1000_init"])
    yrs = float(row["runoff_years"])
    m = duration_mth(t) + 1
    return max(0.0, init - (init / yrs) * (m / 12))


def surr_charge_pp(t):
    """SC(t): the surrender charge scheduled per policy in policy month t.

    Quoted on the **initial** face amount, because face decreases do not reduce the
    surrender charge [S3].  This is the schedule, not the amount collected: see
    :func:`surr_charge`.
    """
    return surr_charge_rate(t) * sum_assured() / 1000


def csv_pp(t):
    """CSV(t): the cash surrender value per policy, ``AV(t) - SC(t)``, floored at zero.

    The floor is **[std]**: the notes write ``CSV = AV - SC`` without one, but a
    negative cash surrender value would be a payment *from* the policyholder.  In the
    early policy years the scheduled surrender charge exceeds the account value and
    the floor binds, so the charge actually collected is the whole account value.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """NCSV(t): the net cash surrender value, ``CSV(t) - L(t)``, floored at zero.

    This is what a surrendering policyholder is paid, and the notes' surrender outgo.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """Surrender charge actually collected from the policies lapsing in month t.

    ``(AV(t) - CSV(t)) x pols_lapse(t)``, so it is capped by the account value where
    the :func:`csv_pp` floor binds.  Insurer income, and part of
    :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def is_shortfall(t):
    """The grace trigger: ``AV'(t) - L(t-1) < MD(t)`` on a monthiversary [S2][S3].

    A diagnostic.  The full grace and lapse-for-insufficiency cascade is **not
    implemented**: the notes leave the in-grace account value treatment (deductions
    accrue as due and unpaid) and the cash flow of a cure payment undetermined, so no
    policy is terminated for insufficiency here.

    It is not inert.  Of the three shipped model points:

    * point 1, the worked-example anchor, is never in shortfall in any of its 1,032
      months -- ``$150`` a month comfortably covers the ``$39.54`` month-1 deduction,
      and the account value grows from there;
    * point 3, the in-force cell, is never in shortfall in any of its 912 months;
    * point 2, the Option B cell, **is** in shortfall from month 677 (policy year 57,
      attained age 91) to the end of the projection, 356 months.  Level $150 premiums
      stop covering a COI charge on a ~$100,000 net amount at risk at those ages.

    Because nothing terminates point 2, its deductions keep coming out of an account
    value that is already empty and it ends the projection about $1.84m overdrawn.
    That is an artifact of the missing cascade, and it is why the death benefit is
    measured on the floored :func:`av_pp_db_basis` rather than on a signed ``AV'``.
    Treat cash flows for a model point in shortfall as **not meaningful** past the
    trigger month; the README says so too.
    """
    return av_pp_at(t, "BEF_FEE") - loan_bal_pp(t - 1) < mth_deduction_pp(t)


def cure_premium_pp(t):
    """The payment required to cure a grace: ``3 x MD(t)`` grossed up for the load [S3].

    The specimen requires at least three times the monthly deduction due plus the
    premium load, so the gross payment is ``3 x MD / (1 - pl)``.  A diagnostic; see
    :func:`is_shortfall`.
    """
    return 3 * mth_deduction_pp(t) / (1 - load_prem_rate())


def cum_prem_pp(t):
    """CumPrem(t): cumulative premiums less withdrawals, for the GPT and 7-pay tests.

    ``CumPrem(0) = 0`` even for an in-force model point, because the notes give no
    opening cumulative-premium attribute **[std]**; the GPT and 7-pay flags are
    therefore only meaningful for points projected from issue.  The notes' "less a
    portion of withdrawals" is taken as the whole withdrawal **[std]**.
    """
    if t == 0:
        return 0.0
    return cum_prem_pp(t - 1) + premium_pp(t) - wd_pp(t)


def gpt_limit(t):
    """The guideline premium limit, ``max(GSP, GLP x policy years elapsed)`` [S3][R2]."""
    return max(gsp(), glp() * policy_year(t))


def gpt_ok(t):
    """Whether cumulative premium is still inside the guideline premium limit.

    A compliance side-calculation with no cash flow of its own: a refused premium
    simply never enters the model [S3][R2][R3].
    """
    return cum_prem_pp(t) <= gpt_limit(t)


def seven_pay_limit(t):
    """The 7-pay limit, ``seven_pay_prem x min(7, policy years elapsed)`` [R3][REG-R14]."""
    return seven_pay_prem() * min(7, policy_year(t))


def is_mec(t):
    """Whether the 7-pay test has failed by policy month t -- once true, true for good.

    ``CumPrem(t) > 7-pay limit`` in any of the first seven policy years, **latched**:
    the flag stays set for the rest of the projection.  The latch is not decoration.
    Under IRC 7702A the contract *is* a modified endowment contract once the 7-pay test
    fails, permanently and for every later year [R3][REG-R14]; and the in-year test
    itself stops applying in policy year 8, so an unlatched flag would quietly switch
    itself off exactly when the failure becomes permanent.  The notes ask the base
    model to "flag (does not project) 7-pay failures", which a flag that turns itself
    off does not do.

    A flag, not a cash flow: MEC status changes policyholder taxation, not insurer
    liability cash flows, and modeling it as a charge or refund would distort premium
    income [S3][R2][R3].
    """
    if policy_year(t) <= 7 and cum_prem_pp(t) > seven_pay_limit(t):
        return True
    return t > 1 and is_mec(t - 1)


def class_factor():
    """The underwriting-class multiplier on the base mortality table **[std]**."""
    return float(data.class_factor_table().loc[rate_class(), "factor"])  # noqa: F821


def mort_rate(t):
    """The annual best-estimate mortality rate in policy month t.

    Base table times :func:`class_factor` times the A/E factor, which is 100% in the
    base run **[std]** with no mortality improvement.  The shipped table is a small
    illustrative one **[std]**, *not* the 2015 VBT the notes recommend -- that family
    is licensed and may not be reproduced here.  Ages beyond the table take its last
    row, where the rate is 1.0.
    """
    tbl = data.mort_table()                                          # noqa: F821
    a = min(max(age(t), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[a, "mort_rate"]) * class_factor() * mort_ae_factor  # noqa: F821


def mort_rate_mth(t):
    """q_m(t): the monthly mortality rate, ``1 - (1 - q)^(1/12)``."""
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """w_base(y): the base annual lapse rate by policy year **[std]**.

    6% in year 1, 5% in year 2, 4% in years 3-10, 3% thereafter, read from
    *lapse_table.csv*; policy years beyond the table take its last row.  The shape is
    informed qualitatively by the SOA/LIMRA UL persistency studies [R7][REG-R20],
    whose detailed tables are behind a paid package, so the levels are a
    standardization.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate_ann"])


def lapse_shock_year():
    """The policy year of the surrender-charge-expiry lapse shock.

    The first policy year with no surrender charge, i.e. the run-off length plus one,
    derived from *surr_charge_table.csv* rather than hard-coded, so a different
    schedule moves the shock with it.  Zero when the model point carries no surrender
    charge, which no policy year can equal.
    """
    if not has_surr_charge():
        return 0
    return int(data.surr_charge_table().loc[surr_charge_id(), "runoff_years"]) + 1  # noqa: F821


def lapse_rate_sc_mult(t):
    """M_sc: the surrender-charge-expiry lapse shock multiplier, 2.0 **[std]**.

    Applied in :func:`lapse_shock_year` only.  The surrender charge suppresses
    surrender while it is positive and its expiry is a known industry shock point;
    product-specific studies are proprietary, so the size is a shape assumption.
    """
    return lapse_shock_mult if policy_year(t) == lapse_shock_year() else 1.0  # noqa: F821


def comp_rate_ann(t):
    """r_comp(t): the competitor / market new-money rate driving dynamic lapse **[std]**.

    The base deterministic run sets it equal to the current credited rate, exactly as
    the notes prescribe, so :func:`lapse_rate_dyn_mult` is 1.  Override this cells to
    switch interest-sensitive lapse on.
    """
    return crediting_rate_ann(t)


def lapse_rate_dyn_mult(t):
    """M_rate(t): the interest-sensitive lapse multiplier **[std]**.

    ``min(3.0, 1 + 5 x max(0, r_comp(t) - i_cr(t) - 0.01))``: no effect until the
    competitor rate exceeds the credited rate by more than 100 basis points.  Equal to
    1 throughout the base run.
    """
    excess = max(0.0, comp_rate_ann(t) - crediting_rate_ann(t) - lapse_dyn_threshold)  # noqa: F821
    return min(lapse_dyn_cap, 1 + lapse_dyn_slope * excess)          # noqa: F821


def lapse_rate(t):
    """w_annual(y, t): the total annual lapse rate **[std]**.

    ``min(0.35, w_base(y) x M_sc(y) x M_rate(t))`` -- the base rate, the
    surrender-charge-expiry shock and the dynamic multiplier, capped **[std]**.
    """
    rate = lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_rate_dyn_mult(t)
    return min(lapse_rate_cap, rate)                                 # noqa: F821


def lapse_rate_mth(t):
    """w_m(t): the monthly lapse rate, ``1 - (1 - w_annual)^(1/12)``."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """Number of policies in force at the beginning of policy month t.

    This is the notes' ``l(t-1)``: decrements are end-of-month events, so the number
    in force is constant through the month and every BOM cash flow is weighted by it.
    ``pols_if(1) = l(0) = pols_if_init()``.
    """
    if t == 1:
        return pols_if_init()
    return pols_if(t - 1) - pols_death(t - 1) - pols_lapse(t - 1)


def pols_if_at(t, timing):
    """Number of policies in force at time t, by ``timing``.

    All three ``CashValue_SE`` timings coincide for this product, and all equal
    :func:`pols_if`: there is no new business inside a projection, and the contract
    has no maturity date, so nothing changes the policy count between BOM and the
    end-of-month decrements.  The cells exists so that products built on this chassis
    which *do* have a maturity or new business can specialize it without moving every
    caller.
    """
    if timing in ("BEF_MAT", "BEF_NB", "BEF_DECR"):
        return pols_if(t)
    else:
        raise ValueError("invalid timing")


def pols_death(t):
    """Number of deaths at the end of policy month t, ``pols_if(t) x q_m(t)``."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Number of lapses at the end of policy month t.

    ``pols_if(t) x (1 - q_m(t)) x w_m(t)``: death is applied before lapse **[std
    order]**, matching the notes' ``l(t) = l(t-1)(1 - q_m)(1 - w_m)``.
    """
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    Universal life has no maturity date -- at attained age 121 charges cease, premiums
    stop and coverage continues for life [S2][S3].  The cells is kept so the in-force
    roll-forward identity has the same shape as in the term and annuity models of this
    library, where it is not zero.
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``"DEATH"``
        ``DB(t) - L(t-1)``: the death benefit less policy debt [S3].  Due and unpaid
        deductions during grace would also be subtracted, but the grace cascade is not
        implemented.

    ``"LAPSE"``
        ``NCSV(t)``, the net cash surrender value.

    A partial withdrawal is **not** a claim -- it is a payment on the owner's election
    rather than on a contingency -- so ``"WITHDRAWAL"`` is not a ``kind`` here.  Its
    per-policy amount is :func:`wd_pp` and its cash flow is :func:`withdrawals`; the
    $25 fee is retained by the insurer and is not part of the payment.
    """
    if kind == "DEATH":
        return db_pp(t) - loan_bal_pp(t - 1)
    elif kind == "LAPSE":
        return ncsv_pp(t)
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim paid out of the account value, by ``kind``.

    Death and lapse both release the end-of-month account value ``AV(t)``, because
    decrements follow the interest credit.  ``"MATURITY"`` is zero: the contract has
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

    ``(claim_pp(t, "DEATH") - AV(t)) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin.
    """
    return (claim_pp(t, "DEATH") - av_pp(t)) * pols_death(t)


def claims(t, kind=None):
    """Claim outgo in policy month t, optionally by ``kind``.

    ``kind`` is ``"DEATH"`` or ``"LAPSE"``, or ``None`` for the total.  Death claims
    are weighted by :func:`pols_death` and surrenders by :func:`pols_lapse`, both
    end-of-month events.

    Partial withdrawals are **not** here, neither as a ``kind`` nor in the ``None``
    total: a withdrawal is a payment on the owner's election rather than a claim, and
    is :func:`withdrawals`.  So ``claims(t)`` is the death and surrender total only,
    and :func:`net_cf` subtracts the withdrawal row separately.
    """
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    elif kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    elif kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    else:
        raise ValueError("invalid kind")


def withdrawals(t):
    """Partial withdrawal payments at BOM of policy month t.

    ``W(t) x pols_if(t)``: a withdrawal is taken at the beginning of the month by the
    policies still in force, so it is weighted by :func:`pols_if` and not by a
    decrement.

    It is a cash flow line of its own -- the ``withdrawals`` column of
    :func:`result_cf` -- and not a ``kind`` of :func:`claims`, because a withdrawal is
    a payment the owner elects rather than a claim on a contingency.  The $25
    withdrawal fee is retained by the insurer and is not part of the payment; see
    :func:`wd_fees`.

    Zero in every shipped model point: the mechanics are implemented and the
    utilization is left to the data **[std]**, as :func:`wd_pp` explains.
    """
    return wd_pp(t) * pols_if(t)


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force.

    Account-value outgo but not a liability cash flow, so this appears in
    :func:`margin_expense` and not in :func:`claims`.
    """
    return wd_fee_pp(t) * pols_if(t)


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(y - 1)`` **[std]**.

    Expenses inflate by policy year, not by month, which is how the notes write the
    $75 per policy per year maintenance expense.
    """
    return (1 + inflation_rate) ** (policy_year(t) - 1)              # noqa: F821


def expenses(t):
    """The insurer's own expenses in policy month t **[std]**.

    ``expense_maint / 12`` inflating at 2.5% a year, plus ``expense_acq`` in the issue
    month.  The notes specify no acquisition expense for this product -- the higher
    per-unit charge in policy years 1-10 is the contractual acquisition-cost recovery,
    which is income, not outgo -- so ``expense_acq`` is zero and the term is carried
    only so products built on this chassis can switch it on.

    Not to be confused with :func:`maint_fee`, which is the charge *against the
    account value*.
    """
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    return (acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821


def premium_taxes(t):
    """Premium tax and other percent-of-premium expense, 2.5% of premium **[std]**."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``load x GP + withdrawal fees + maint_fee + surrender charges - expenses
    - premium taxes``.  Follows ``CashValue_SE.margin_expense``; see
    :func:`check_margin` for the identity it takes part in.
    """
    return (load_prem_rate() * premium_pp(t) * pols_if(t)
            + wd_fees(t)
            + maint_fee(t)
            + surr_charge(t)
            - expenses(t)
            - premium_taxes(t))


def margin_mortality(t):
    """Mortality margin: :func:`coi` net of :func:`claims_over_av`."""
    return coi(t) - claims_over_av(t)


def net_cf(t):
    """Net liability cash flow in policy month t, **undiscounted**.

    ``premiums - death claims - surrender payments - withdrawals - expenses
    - premium taxes``, **income-positive** as in every model of this library.
    :func:`claims` carries the death and surrender rows only, so the withdrawal row is
    subtracted as its own term.  Like the rest of this library the model projects
    *gross liability cash flows*: there is no discounting and no change in account
    value in this figure, because reserves are a separate layer that consumes these
    flows.  Investment income on the account value is a credit to the policyholder,
    not an insurer cash flow, so it does not appear either -- see :func:`check_margin`
    for how it reconciles.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - premium_taxes(t))


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

    This pins the notes' processing order, in particular that interest is credited on
    the *post-deduction* balance and that decrements come after the credit.
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
    ``CashValue_SE``, whose ``net_cf`` already nets the change in account value and
    the investment income; the loan term is the debt extinguished against the account
    value when a policy with a loan surrenders.  The identity holds while neither the
    :func:`csv_pp` nor the :func:`ncsv_pp` floor binds against a policy loan, which is
    the case for every shipped model point.
    """
    res = []
    for t in range(1, proj_len() + 1):
        rhs = (margin_expense(t) + margin_mortality(t)
               + av_change(t) - inv_income(t)
               + loan_bal_pp(t) * pols_lapse(t))
        res.append(math.isclose(net_cf(t), rhs,                      # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-9))
    return all(res)


def result_cf():
    """Result table of cashflows, a DataFrame indexed by policy month ``t``.

    The surrender column is ``claims_lapse``, matching the ``"LAPSE"`` ``kind`` that
    produces it, and partial withdrawals sit in their own ``withdrawals`` column rather
    than among the claims.  The cash flow columns sum to ``net_cf`` under the
    income-positive sign convention: ``premiums`` less every other flow.
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
    """Result table of policy decrements, a DataFrame indexed by policy month ``t``."""
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

    The columns are the columns of the worked example in the technical notes, in the
    notes' own order: ``AV(t-1)``, ``NP``, ``AV'``, ``DB``, ``NAAR``, ``COI``, ``MD``,
    ``AV' - MD``, interest, ``AV(t)``, followed by the surrender and loan values.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_prem": [av_pp_at(t, "BEF_PREM") for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "av_pp_bef_fee": [av_pp_at(t, "BEF_FEE") for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "net_amt_at_risk": [net_amt_at_risk(t) for t in ts],
            "coi_pp": [coi_pp(t) for t in ts],
            "mth_deduction_pp": [mth_deduction_pp(t) for t in ts],
            "av_pp_bef_inv": [av_pp_at(t, "BEF_INV") for t in ts],
            "inv_income_pp": [inv_income_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "ncsv_pp": [ncsv_pp(t) for t in ts],
            "loan_bal_pp": [loan_bal_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

charges_cease_age = 121

guar_rate_ann = 0.02

crediting_rate_curr = 0.04

coi_curr_factor = 0.6

expense_pol_mth = 7.5

expense_unit_mth_1 = 0.26

expense_unit_mth_2 = 0.156

expense_unit_step_year = 10

loan_rate_ann = 0.0275

wd_fee = 25.0

wd_free_rate = 0.1

wd_first_year = 1

mort_ae_factor = 1.0

lapse_shock_mult = 2.0

lapse_dyn_slope = 5.0

lapse_dyn_threshold = 0.01

lapse_dyn_cap = 3.0

lapse_rate_cap = 0.35

expense_acq = 0.0

expense_maint = 75.0

inflation_rate = 0.025

premium_tax_rate = 0.025

pd = ("Module", "pandas")

math = ("Module", "math")