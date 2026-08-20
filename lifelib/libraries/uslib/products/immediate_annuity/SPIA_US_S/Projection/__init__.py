# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.SPIA_US_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked-example anchor cell
    >>> Projection.point_id = 8            # or switch the default

``t`` counts **policy months from the annuity date**, 1-based: ``t = 1`` is the first
projected month and ``t = 0`` is the month-zero state used as the base case of every
recursion (``lives_if(0, life) = 1``, ``cum_annuity_pp(0) = 0``,
``commute_frac_cum(1) = 0``).

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/immediate_annuity/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``SPIA_US_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.SPIA_US_S.Data`:

========================  ==================================  ======================
Reference                 Cells                               File
========================  ==================================  ======================
model_point_file          data.model_point_table()            model_point_table.csv
mort_table_file           data.mort_table()                   mort_table.csv
improvement_scale_file    data.improvement_scale()            improvement_scale.csv
surr_charge_file          data.surr_charge_table()            surr_charge_table.csv
========================  ==================================  ======================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for contract counts, plural nouns
for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claims(t, kind)`` with an uppercase ``kind`` string, ``result_cf()`` for the cash flow
table. The technical notes use compact actuarial symbols instead. The mapping is:

=========================  =================================  =========================
Notes symbol               Cells                              Meaning
=========================  =================================  =========================
t                          (the cells argument)               Month from the annuity date
y(t) = ceil(t/12)          policy_year(t)                     Policy year containing month t
(none)                     duration(t)                        Completed policy years, y(t)-1
(none)                     duration_mth(t)                    Months elapsed at end of month t
m                          payment_freq()                     Payments per year
timing                     payment_timing()                   arrears (default) or advance
T                          is_payment_mth(t)                  Month t is a payment date
(payment point)            payment_surv_mth(t)                Month survival is measured at
P                          premium_pp()                       Single premium
tau                        premium_tax_rate()                 State premium tax rate
P_net                      premium_net_pp()                   P(1 - tau), the amount annuitized
B(y)                       annual_income(y)                   Unreduced annualized income
inst(t)                    annuity_pp(t)                      Instalment per contract payable
(inst, untrimmed)          annuity_pp_sched(t)                Scheduled instalment before trim
g                          cola_rate()                        Fixed compound COLA rate
delta                      survivor_pct()                     Survivor percentage
trig                       reduction_trigger()                either / primary
form                       form()                             Payout form, one of five
n                          certain_mths()                     Elected certain months
n_R                        certain_mths_refund()              Derived installment-refund months
n_eff                      certain_mths_eff()                 Effective certain months by form
joint                      is_joint()                         Contract covers two lives
x1, x2                     age_at_entry(life)                 Issue ages (ANB), life = 1 or 2
(none)                     age(t, life)                       Attained age (ANB)
(none)                     sex(life)                          Sex of each covered life
l_i(t)                     lives_if(t, life)                  Survival probability to end of t
d_i(t)                     lives_death(t, life)               Death density
l_last(t)                  lives_if_last(t)                   At least one covered life alive
d_last(t), d_term(t)       lives_death_last(t)                Last-death density
L(t)                       payment_factor_life(t)             Life-contingent payment factor
C(t)                       certain_floor(t)                   Certain floor 1{t <= n_eff}
Phi(t)                     payment_factor(t)                  max(C(t), L(t))
G(t)                       cum_annuity_pp(t)                  Cumulative scheduled instalments
IF(t)                      pols_if(t)                         Contracts with an obligation open
(none)                     pols_if_init()                     Contracts in force at t = 0
(none)                     annuity_year()                     Calendar year of the annuity date
(none)                     calendar_year(t)                   Calendar year containing month t
q_x (table)                mort_rate_base(t, life)            Base-table annual mortality rate
G2_x                       improvement_rate(t, life)          Generational improvement rate
AE                         mort_ae_factor                     A/E factor, 1.084 **[std]**
theta                      rating_factor()                    Substandard multiplier
q_rated(x, cal)            mort_rate(t, life)                 Annual rate after AE and theta
q_m(t)                     mort_rate_mth(t, life)             Monthly rate 1-(1-q)^(1/12)
(none)                     mort_basis()                       table or scenario run **[std]**
(none)                     death_mth(life)                    Scenario month of death **[std]**
omega                      omega_age                          Limiting age, 120
(stopping rule)            horizon_mths()                     Months to the age stop rule
(none)                     proj_len()                         Last projected month
(inst after commutation)   annuity_pp_paid(t)                 inst(t)*(1 - theta_cum*C)
E[ANN(t)]                  annuity_payments(t)                Expected annuity outgo
E[CR(t)]                   claims(t, "REFUND")                Cash-refund lump sum
(per contract)             claim_pp(t, kind)                  Refund amount per contract
E[COMM(t)]                 commutations(t)                    Commutation paid to the owner
E[EXP(t)]                  expenses(t)                        Maintenance expense
CF(t)                      liability_cf(t)                    Total gross liability outgo
(none)                     net_cf(t)                          -liability_cf(t), insurer sign
commutation_enabled        commutation_enabled()              Contract has the withdrawal right
(same name)                issue_state_excludes_withdrawal()  Oregon bars the withdrawal
qualified                  qualified()                        Qualified money; inert here
(none)                     commute_elig(t)                    Withdrawal allowed in month t
CV(t)                      commuted_value(t)                  Commuted value of certain tail
j(t)                       commute_disc_rate(t)               Commutation discount rate
j0                         commute_disc_rate_base             Base commutation rate, 4.00%
CMT10(t) - CMT10(0)        cmt10_shift                        10-yr CMT change since issue
sc(y)                      surr_charge_rate(y)                Surrender charge rate
sc(y) x W                  surr_charge(t)                     Surrender charge retained
W                          commute_amount(t)                  Gross withdrawal requested
theta_cum(t)               commute_frac_cum(t)                Cumulative commutation fraction
u(y)                       commute_util_rate(y)               Commutation utilization **[std]**
c_e                        expense_maint                      Maintenance expense p.a.
pi                         inflation_rate                     Expense inflation
=========================  =================================  =========================

Every attribute of the notes' *Model point attributes* table has a row above, and so do
the model's own additions, which the notes give no symbol but which drive the
generational basis, the verification anchor and the commutation eligibility test:
``pols_if_init``, ``annuity_year``, ``calendar_year``, ``mort_basis``, ``death_mth`` and
``commute_elig``. Only the outputs and diagnostics are left out — :func:`result_cf`,
:func:`result_pols`, :func:`check_lives_roll_fwd` / :func:`check_lives_roll_fwd_resid`
and :func:`check_payment_factor` / :func:`check_payment_factor_resid` — because they are
not quantities the notes define. Most model point attributes keep the
notes' own name; ``issue_state_excludes_withdrawal`` is one of them and is entered as
``(same name)`` only because it is too wide for the first column.

Five names in that table needed care.

``l`` and ``L`` differ in the notes only by case — survival probability versus the
life-contingent payment factor — so they become ``lives_if`` and
``payment_factor_life``. Likewise ``G(t)``, cumulative instalments, collides with
``G2_x``, the improvement scale: ``cum_annuity_pp`` and ``improvement_rate``. And
``theta`` is used twice, once as the substandard mortality multiplier and once as
``theta_cum``, the cumulative commutation fraction: ``rating_factor`` and
``commute_frac_cum``.

``d_term(t)`` is not a separate quantity. The notes define it as ``d_1`` on a
single-life contract and ``d_last`` on a joint one; because :func:`lives_if_last`
returns ``l_1`` when the contract is single-life, ``lives_death_last`` *is* ``d_term``
in both cases and no second cells is needed.

``CF(t)`` needs one sentence of warning. The notes define
``CF(t) = E[ANN] + E[CR] + E[COMM] + E[EXP]``, an outgo-positive total, and that is
:func:`liability_cf`. But the **CF column of the worked-example table is the annuity
instalment alone** — at ``t = 1`` it shows 500.00, not the 505.00 that the definition
gives once the $5.00 monthly maintenance expense is added. The worked example is
therefore asserted against :func:`annuity_payments`, and :func:`net_cf` carries the
house sign convention of ``Term_US_A`` (income less outgo, so ``-liability_cf``). Both
signs are published as columns of :func:`result_cf`, the notes' outgo-positive total
under ``liability_cf`` and the library-wide income-positive one under ``net_cf``.

The two self-checks follow the library convention: :func:`check_lives_roll_fwd` and
:func:`check_payment_factor` take **no argument and return a bool** covering every
projected month, so one test can call the same no-arg check across every model in the
library. The signed per-month residual — the more useful object once a check fails —
stays available as :func:`check_lives_roll_fwd_resid` and
:func:`check_payment_factor_resid`, and each boolean is implemented in terms of its own
residual.

.. rubric:: Two mortality bases: table and scenario

The notes' worked example is not a probability-weighted run. It is a **scenario**: "the
joint (secondary) annuitant dies during month 14; the primary survives throughout",
evaluated at ``l_1 = 1``, ``l_2 = 0``. The notes' *Model points* section, by contrast,
projects "on an expected (probability-weighted) basis". Both readings are shipped, and
which one applies is a model point column:

``mort_basis = "table"``
    ``lives_if`` runs the notes' generational recursion off the shipped mortality and
    improvement tables. Model points 7, 8, 9, 12 and 15; point 8 is the anchor cell on
    this basis and is the run to read for a realistic cash flow shape.

``mort_basis = "scenario"`` **[std]**
    ``lives_if(t, life)`` is the deterministic step function
    ``1{t < death_mth(life)}``, with a blank ``death_mth`` meaning the life survives the
    whole projection. Model points 1-6, 10, 11, 13 and 14, which reproduce the worked
    example and its traces exactly.

The scenario switch is a **[std]** modelling device, not a product feature; it exists
because the notes' verification anchor is a scenario and retuning assumptions to force a
probability-weighted run onto it would be dishonest.

.. rubric:: The certain period is a floor, not a second stream

``payment_factor(t) = max(certain_floor(t), payment_factor_life(t))`` is the single most
important line in the model and the notes' first listed pitfall. During the certain
period the full, *unreduced* instalment is payable regardless of survival; an additive
construction would pay ``1 + L`` and silently double the guarantee. The ``max`` also
reproduces, with no extra logic, one carrier's rule that a survivor reduction inside a
certain period is deferred to the end of that period [S5] — see model point 5, where the
reduction to ``delta`` begins at ``t = 121`` and not at the month-14 death.

.. rubric:: ``certain_only``, where the notes' expense formula outlives the contract

The notes carry the maintenance expense on ``IF(t) = max(C(t), l_alive(t))`` and, in the
same table, describe it as paid *"while any payment obligation remains"*. The two agree
on the four life-contingent forms. They do not agree on ``certain_only``, where the notes
also set ``L(t) = 0``: the last instalment falls at ``n_eff`` and nothing is owed
afterwards, but ``l_alive`` is a survival probability, not a payment factor, and stays
positive for the annuitant's whole remaining lifetime. Read literally the formula keeps
billing a contract that ended years earlier. :func:`pols_if` follows the prose and drops
the life-contingent leg on ``certain_only`` — the one form with no life contingency in it
— so ``IF(t) = C(t)`` there and ``max(C(t), l_alive(t))`` on every other form. Model
point 15 exercises it; no other form and no other model point moves.

.. rubric:: Survival-measurement and refund-balance timing

Two timing conventions move the liability by one payment period each and are wired to
the same switch, ``timing``:

- an **arrears** instalment falling at the end of month ``t`` requires survival to the
  end of month ``t``; an **advance** instalment falls at the *start* of month ``t``,
  which is the end of month ``t - 1``, so survival is measured at ``t - 1`` whatever the
  frequency. That is :func:`payment_surv_mth`. The notes write the advance point as
  ``t - 12/m``, one full payment period earlier — but that measures from the **arrears**
  month of the same instalment, which falls one payment period later than the advance
  month. :func:`is_payment_mth` indexes an advance instalment by the month it falls *in*
  (``t = 1, 4, 7, …`` at ``m = 4``), so ``t - 1`` is the reading that holds at every
  frequency; the two agree at ``m = 12``, the only frequency the notes spell out.
- the cash-refund balance nets instalments *already paid*: ``G(t-1)`` on arrears, but
  ``G(t)`` in an advance payment month, because an instalment paid at the start of the
  month of death has been paid. That is :func:`claim_pp`.

Deaths are decremented at end of month, so a survivor reduction takes effect **from the
instalment due at the end of the month of death** — which is why the worked example's
trigger split bites at ``t = 14`` and not at ``t = 15``.
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


def premium_pp():
    """P: the single premium of the selected model point.

    A pricing input at t = 0, not a projected cash flow: the projection carries no
    premium income.  It enters the projection only through the refund forms, where the
    guarantee is measured against it.
    """
    return float(model_point()["premium"])


def premium_tax_rate():
    """tau: the state premium tax rate deducted before income is determined **[std]**.

    Zero in the base run; no source quantifies a rate [S6][S7][S11].
    """
    return float(model_point()["premium_tax_rate"])


def premium_net_pp():
    """P_net = P(1 - tau), the amount annuitized [S6][S7][S11].

    Reported for completeness.  Because ``B(1)`` is exogenous - no insurer publishes
    payout factors, so the model does not derive income from premium - nothing in the
    projection consumes it.
    """
    return premium_pp() * (1.0 - premium_tax_rate())


def pols_if_init():
    """Initial number of contracts in force; 1.0 on a single-contract model point."""
    return float(model_point()["pols_if_init"])


def form():
    """The payout form: one of the five forms of [S1][S2][S4][S5].

    life_only, life_certain, cash_refund, installment_refund, certain_only.
    """
    v = model_point()["form"]
    if v not in ("life_only", "life_certain", "cash_refund",
                 "installment_refund", "certain_only"):
        raise ValueError("invalid form")
    return v


def is_joint():
    """True when the contract covers two annuitants."""
    return bool(model_point()["joint"])


def age_at_entry(life):
    """x_i: issue age (ANB) of the primary (life = 1) or joint (life = 2) annuitant.

    Age nearest birthday **[std]**: one carrier defines contract age as ANB [S1] and the
    2012 IAM/IAR family is tabulated ANB [R2][R9].
    """
    if life == 1:
        return int(model_point()["primary_age"])
    if life == 2:
        return int(model_point()["joint_age"])
    raise ValueError("invalid life")


def sex(life):
    """Sex (M / F) of the primary (life = 1) or joint (life = 2) annuitant."""
    if life == 1:
        return model_point()["primary_sex"]
    if life == 2:
        return model_point()["joint_sex"]
    raise ValueError("invalid life")


def survivor_pct():
    """delta: the survivor percentage, in {0.50, 2/3, 0.75, 1.00} [S1][S2][S5][S6][S7]."""
    return float(model_point()["survivor_pct"])


def reduction_trigger():
    """trig: whether the reduction is triggered by *either* death or the *primary*'s.

    A switch, not a parameter: the two conventions coincide on the primary's death and
    differ only on the secondary's [S1][S2][S3][S7].
    """
    v = model_point()["reduction_trigger"]
    if v not in ("either", "primary"):
        raise ValueError("invalid reduction_trigger")
    return v


def certain_mths():
    """n: the elected certain period in months, 0 or 60-360 [S1][S2][S4][S5]."""
    return int(model_point()["certain_months"])


def payment_freq():
    """m: payments per year, in {12, 4, 2, 1} [S1][S2]."""
    v = int(model_point()["frequency"])
    if v not in (12, 4, 2, 1):
        raise ValueError("invalid frequency")
    return v


def payment_timing():
    """Whether instalments fall in *arrears* (the **[std]** default) or in *advance*.

    No product document states the convention; VM-V's prescribed weight-table cash flow
    model assumes payments at the end of each period, so arrears is the default [R1].
    """
    v = model_point()["timing"]
    if v not in ("arrears", "advance"):
        raise ValueError("invalid timing")
    return v


def cola_rate():
    """g: the fixed compound COLA rate, in {0, .01, .02, .03, .04} [S1][S5]."""
    return float(model_point()["cola_rate"])


def commutation_enabled():
    """Whether the contract carries the certain-portion commutation right [S1]."""
    return bool(model_point()["commutation_enabled"])


def issue_state_excludes_withdrawal():
    """True where the issue state bars the withdrawal feature (Oregon) [S1][S2]."""
    return bool(model_point()["issue_state_excludes_withdrawal"])


def qualified():
    """True for qualified money.  Informational: the RMD overlay is not implemented."""
    return bool(model_point()["qualified"])


def rating_factor():
    """theta: the substandard mortality multiplier **[std]**; 1.0 in the base run.

    ``q_rated = min(1, theta * q_be)``, the reference model's carrier for anti-selection
    at outset and for rated ages [S8][R1][REG-R41].
    """
    return float(model_point()["rating_factor"])


def annuity_year():
    """The calendar year of the annuity date **[std]**; the generational anchor.

    The improvement exponent is ``calendar_year(t) - mort_table_year``, so this is what
    makes the mortality basis generational rather than period.
    """
    return int(model_point()["annuity_year"])


def mort_basis():
    """Whether the run is probability-weighted (*table*) or deterministic (*scenario*).

    *table* runs the notes' generational recursion off the shipped tables; *scenario*
    **[std]** replaces it with the step function ``1{t < death_mth(life)}`` so the notes'
    worked example - which is a scenario, not an expectation - reproduces exactly.  See
    the Space docstring.
    """
    v = model_point()["mort_basis"]
    if v not in ("table", "scenario"):
        raise ValueError("invalid mort_basis")
    return v


def death_mth(life):
    """The scenario month of death of ``life``; 0 if the life survives throughout.

    Read only when ``mort_basis() == "scenario"``.  A blank cell in the model point table
    means the life never dies in the scenario and is returned as 0, since ``t`` is 1-based
    and a death in month 0 is not a projectable event.  A death "during month 14" is
    decremented at the end of month 14, so ``lives_if(t, life)`` is 0 from ``t = 14``.
    """
    v = model_point()["death_mth_1" if life == 1 else "death_mth_2"]
    return 0 if pd.isna(v) else int(v)                               # noqa: F821


def duration_mth(t):
    """Months elapsed from the annuity date at the end of month t; equal to t.

    ``t`` is 1-based here, unlike ``CashValue_SE``'s 0-based months, so the identity is
    trivial - the cells exists so the monthly models share one vocabulary.
    """
    return t


def duration(t):
    """Completed policy years at the start of month t: ``(t - 1) // 12``."""
    return (t - 1) // 12


def policy_year(t):
    """y(t) = ceil(t/12): the policy year containing month t; 1 for t = 1..12."""
    return duration(t) + 1


def calendar_year(t):
    """The calendar year of the policy year containing month t."""
    return annuity_year() + duration(t)


def age(t, life):
    """The attained age (ANB) of ``life`` in the policy year containing month t."""
    return age_at_entry(life) + duration(t)


def horizon_mths():
    """Last month at which some covered life has not yet passed the limiting age.

    ``12*(omega_age - min x_i)``: the notes stop once ``t/12 + x_i > omega`` for every
    covered life, and stopping on the primary's age alone would truncate a younger joint
    annuitant's tail.  It is *not* the month in which the youngest life attains the
    limiting age, which is one month later - see :func:`proj_len`.
    """
    ages = [age_at_entry(1)]
    if is_joint():
        ages.append(age_at_entry(2))
    return 12 * (omega_age - min(ages))                              # noqa: F821


def proj_len():
    """Projection length in months: the mortality horizon, or the certain period if longer.

    :func:`horizon_mths` implements the notes' age stop rule literally - stop once
    ``t/12 + x_i > omega`` for every covered life - so the last projected month is
    ``12*(omega_age - min x_i)``.  Under the ANB age convention, where :func:`age`
    advances on each policy anniversary, the youngest life's attained age in that month is
    ``omega_age - 1``: the projection stops **one month before** any life attains
    ``omega_age``, and the ``q = 1`` row of the shipped tables is never reached inside it.

    The notes' other stop test, ``IF(t) < 1e-6``, is therefore **not** subsumed - on model
    point 8 the projection ends at ``pols_if(696) = 3.41e-06``, above that threshold, and
    a test pins the figure.  The age rule is the one implemented, because it keeps
    ``proj_len()`` independent of the projection it bounds; what it truncates is a tail of
    3.41e-06 of a contract, and one further month would take it to zero.
    """
    return max(horizon_mths(), certain_mths_eff())


def is_payment_mth(t):
    """Whether month t is a payment date.

    Arrears: ``T = {12k/m}``, so t = 3, 6, 9, ... at m = 4.  Advance: the k-th instalment
    falls one full payment period earlier, at the start of month ``12(k-1)/m + 1``, so
    t = 1, 4, 7, ...  At m = 12 every month is a payment month on either convention.
    """
    if t < 1:
        return False
    step = 12 // payment_freq()
    if payment_timing() == "arrears":
        return t % step == 0
    return (t - 1) % step == 0


def payment_surv_mth(t):
    """The month at which survival is measured for the instalment falling in month t.

    Arrears: the end of month t.  Advance: the end of month ``t - 1``, because an advance
    instalment falls at the *start* of month t, whatever the frequency; 0 for the first
    instalment, where ``lives_if`` is 1.  Using end-of-period survival for advance
    payments understates the liability by about one period's mortality per payment.

    The notes put the advance point at ``t - 12/m``, "one full payment period earlier".
    That measures from the **arrears** month of the same instalment, which falls one
    payment period *after* the advance month; :func:`is_payment_mth` indexes an advance
    instalment by the month it falls in, so the two readings coincide only at m = 12.
    At m = 4 the second instalment falls at the start of month 4 and requires survival to
    the end of month 3 - not to the end of month 1, which would pay it to a life the
    projection has already recorded as dead.
    """
    if payment_timing() == "arrears":
        return t
    return t - 1


def annual_income(y):
    """B(y): the unreduced annualized income in policy year y.

    ``B(y) = B(y-1)(1 + g)`` on each anniversary of the annuity date [S1][S4], compound
    and irrevocable.  Escalation applies to the **unreduced** level and continues after a
    survivor reduction, because the contract reduces payments to delta of the *current*
    income payment [S2].  One carrier instead starts the first increase one year after the
    first income payment [S5]; that one-period difference is a **[std]** convention choice
    not taken here.  ``B(1)`` is exogenous - no insurer publishes payout factors, so the
    model does not derive it from the premium.
    """
    if y <= 1:
        return float(model_point()["annual_income"])
    return annual_income(y - 1) * (1.0 + cola_rate())


def annuity_pp_sched(t):
    """The scheduled unreduced instalment per contract in month t, before any trim.

    ``inst(t) = B(y(t))/m`` on payment dates and 0 elsewhere.
    """
    if not is_payment_mth(t):
        return 0.0
    return annual_income(policy_year(t)) / payment_freq()


def cum_annuity_pp(t):
    """G(t): cumulative scheduled instalments per contract through month t.

    A **deterministic** as-if-alive schedule: instalments payable while any covered life
    is alive follow the deterministic escalation path, so the refund balance needs no
    path simulation.  On a joint contract with a survivor reduction the cash refund is
    offered only at delta = 100% [S5], so the unreduced schedule is the paid schedule.
    """
    if t <= 0:
        return 0.0
    return cum_annuity_pp(t - 1) + annuity_pp_sched(t)


def certain_mths_refund():
    """n_R: the certain period derived by an installment refund [S1][S4][S5][S6].

    ``n_R = min{t in T : G(t) >= P}`` - payments continue until cumulative payments equal
    the premium.  Under a level path this closes to ``(12/m) * ceil(m*P/B(1))``, which is
    the published rule "guaranteed payment period = premium paid / annualized income
    benefit amount" rounded up to a payment date [S5]; the anchor check is
    ``P/B(1) = 100,000/6,000 = 16.667 years = 200 months``.  Searched rather than closed
    so a COLA path (which the anchor carrier does not offer with this form [S1]) still
    resolves.
    Capped at :func:`horizon_mths` if the premium is never recovered.
    """
    step = 12 // payment_freq()
    last = horizon_mths()
    t = step if payment_timing() == "arrears" else 1
    while t <= last:
        if cum_annuity_pp(t) >= premium_pp():
            return t
        t += step
    return last


def certain_mths_eff():
    """n_eff: the effective certain period in months, by form.

    ``n`` for life_certain and certain_only [S1][S2][S4][S5]; ``n_R`` for
    installment_refund [S1][S5]; 0 for life_only and cash_refund [S1][S2].
    """
    f = form()
    if f in ("life_certain", "certain_only"):
        return certain_mths()
    if f == "installment_refund":
        return certain_mths_refund()
    return 0


def annuity_pp(t):
    """inst(t): the instalment per contract actually payable in month t.

    Equal to :func:`annuity_pp_sched` except on installment_refund, where the notes trim
    the final instalment at ``n_R`` to ``P - G(n_R - 12/m)`` **[std]** so cumulative
    payments land exactly on the premium.  The trim is a no-op whenever ``P`` is an exact
    multiple of the instalment, which is the shipped anchor's case.
    """
    if form() != "installment_refund":
        return annuity_pp_sched(t)
    if t != certain_mths_refund():
        return annuity_pp_sched(t)
    step = 12 // payment_freq()
    return max(0.0, premium_pp() - cum_annuity_pp(t - step))


def mort_rate_base(t, life):
    """The base-table annual mortality rate for ``life`` in the policy year containing t.

    The shipped table is an illustrative **[std]** annuitant table, *not* the 2012 IAM
    Basic table the notes prescribe: licensed tables may not be embedded, and the Basic
    table is in any case not printed in any source this library holds.  Rates at and
    above the limiting age are 1.
    """
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    return float(data.mort_table().loc[(x, sex(life)), "mort_rate"])  # noqa: F821


def improvement_rate(t, life):
    """G2_x: the generational improvement rate for ``life`` in the year containing t.

    The shipped scale is an illustrative **[std]** stand-in for Projection Scale G2.
    Scaling this table is the notes' first-listed sensitivity - Scale G2 is fixed and
    dated, and 2020-2024 experience says it has over-projected [R9].
    """
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 0.0
    return float(                                                    # noqa: F821
        data.improvement_scale().loc[(x, sex(life)), "improvement_rate"])


def mort_rate(t, life):
    """q_rated: the annual mortality rate applied to ``life`` in the year containing t.

    The notes' construction, in order::

        q_base(x, 2012+k) = q_x(table) * (1 - G2_x)^k
        q_be              = min(1, AE * q_base),      AE = 1.084 **[std]**
        q_rated           = min(1, theta * q_be),     theta = 1 in base

    ``k = calendar_year(t) - mort_table_year``, so the basis is **generational**: each
    attained age in each future calendar year uses its own improved rate.  The A/E factor
    belongs on the *projected* basis, matching the study's measurement convention - on
    the unprojected table the study's own answer is 99.6% [R9], and applying 1.084 there
    misstates the mortality level by about 8%.
    """
    k = calendar_year(t) - mort_table_year                           # noqa: F821
    q_base = mort_rate_base(t, life) * (1.0 - improvement_rate(t, life)) ** k
    q_be = min(1.0, mort_ae_factor * q_base)                         # noqa: F821
    return min(1.0, rating_factor() * q_be)


def mort_rate_mth(t, life):
    """q_m(t) = 1 - (1 - q_rated)^(1/12): the monthly mortality rate **[std]**."""
    return 1.0 - (1.0 - mort_rate(t, life)) ** (1.0 / 12.0)


def lives_if(t, life):
    """l_i(t): the probability that ``life`` is alive at the end of month t.

    ``l_i(0) = 1``.  On the *table* basis ``l_i(t) = l_i(t-1)(1 - q_m(t))``, deaths being
    decremented at end of month.  On the *scenario* basis **[std]** the survival path is
    the step function ``1{t < death_mth(life)}``, with ``death_mth = 0`` meaning the life
    survives the whole projection - which is what the notes' worked example specifies.
    Returns 0 for life = 2 on a single-life contract.
    """
    if life == 2 and not is_joint():
        return 0.0
    if t <= 0:
        return 1.0
    if mort_basis() == "scenario":
        d = death_mth(life)
        return 0.0 if (d > 0 and t >= d) else 1.0
    return lives_if(t - 1, life) * (1.0 - mort_rate_mth(t, life))


def lives_death(t, life):
    """d_i(t) = l_i(t-1) - l_i(t): the death density of ``life`` in month t."""
    return lives_if(t - 1, life) - lives_if(t, life)


def lives_if_last(t):
    """l_last(t): the probability that at least one covered life is alive at end of t.

    ``l_1 + l_2 - l_1*l_2`` on a joint contract, under **joint-life independence
    [std]** - the SOA/LIMRA payout study is explicit that its data cannot inform the
    assumption, since it gives no recognition to a living secondary annuitant [R9].
    On a single-life contract this is ``l_1``, which is why no separate ``l_alive`` cells
    is needed.
    """
    l1 = lives_if(t, 1)
    if not is_joint():
        return l1
    l2 = lives_if(t, 2)
    return l1 + l2 - l1 * l2


def lives_death_last(t):
    """d_last(t) = l_last(t-1) - l_last(t): the last-death density in month t.

    This is also the notes' ``d_term(t)``, the death that terminates the income stream:
    ``d_1`` on a single-life contract and ``d_last`` on a joint one, which
    :func:`lives_if_last` already collapses into one expression.
    """
    return lives_if_last(t - 1) - lives_if_last(t)


def certain_floor(t):
    """C(t) = 1{t <= n_eff}: the annuity-certain floor indicator."""
    return 1.0 if t <= certain_mths_eff() else 0.0


def payment_factor_life(t):
    """L(t): the life-contingent payment factor for the instalment falling in month t.

    Survival is measured at :func:`payment_surv_mth`, not at t.  By form and trigger::

        single life:           L = l_1
        joint, trig = either:  L = l_1*l_2 + delta*(l_1 + l_2 - 2*l_1*l_2)
        joint, trig = primary: L = l_1 + delta*(1 - l_1)*l_2
        certain_only:          L = 0

    The *either* form pays the full instalment while **both** are alive and delta while
    **exactly one** is - the second bracket is P(at least one alive) - P(both alive)
    [S2][S3].  The *primary* form pays in full while the primary lives whatever the joint
    annuitant's status, and delta only when the primary is dead and the joint annuitant
    alive [S2][S3][S5].  The two coincide on the primary's death and differ only on the
    secondary's, which is why the trigger is a switch and not a footnote.
    """
    if form() == "certain_only":
        return 0.0
    s = payment_surv_mth(t)
    l1 = lives_if(s, 1)
    if not is_joint():
        return l1
    l2 = lives_if(s, 2)
    d = survivor_pct()
    trig = reduction_trigger()
    if trig == "either":
        return l1 * l2 + d * (l1 + l2 - 2.0 * l1 * l2)
    return l1 + d * (1.0 - l1) * l2


def payment_factor(t):
    """Phi(t) = max(C(t), L(t)): the master payment factor.

    The ``max`` makes the certain period an annuity-**certain floor** rather than an
    additional stream: during the certain period the full unreduced instalment is paid
    regardless of survival, and the ``max`` prevents paying ``1 + L``.  An additive
    construction silently doubles the guarantee - the notes' first-listed pitfall.
    Because the floor pays the *unreduced* instalment, it also reproduces one carrier's
    rule that a survivor reduction inside a certain period is deferred to the end of that
    period, with no extra flag [S5].
    """
    return max(certain_floor(t), payment_factor_life(t))


def pols_if(t):
    """IF(t): contracts with a payment obligation still open at month t.

    ``pols_if_init * max(C(t), l_alive(t))`` **[std]** - the in-force measure the notes
    use to carry the maintenance expense, which runs while *any* payment obligation
    remains, whether that obligation is life-contingent or certain.

    One divergence from the notes' literal formula, on ``certain_only`` only.  That form
    has ``L(t) = 0``, so the last instalment falls at ``n_eff`` and nothing is owed after
    it; but ``l_alive`` is a survival probability rather than a payment factor and stays
    positive for the annuitant's remaining lifetime, so the unqualified ``max`` would keep
    accruing the maintenance expense on a contract that has ended - contradicting the
    same table's "while any payment obligation remains".  The life-contingent leg is
    therefore dropped on ``certain_only``, the one form with no life contingency in it,
    and ``IF(t) = C(t)`` there.  Every other form is unaffected.  See model point 15.
    """
    alive = 0.0 if form() == "certain_only" else lives_if_last(t)
    return pols_if_init() * max(certain_floor(t), alive)


def commute_util_rate(y):
    """u(y): the deterministic commutation utilization in contract year y **[std]**.

    Zero in the base run, so the payment engine is exercised in isolation: no public data
    on SPIA commutation take-up exists.  The notes' rate-driven alternative
    ``u(y, t) = min(u_max, u_base(y) * max(0, 1 + kappa*[CMT10(0) - CMT10(t)]))`` is not
    implemented - it is a pure shape assumption calibrated to nothing.  Both
    constructions are best-estimate objects and are **barred from a CARVM run**:
    commutation is an elective benefit under AG 33, whose incidence rates must be
    maximised over rather than assumed [REG-R151].
    """
    return 0.0 if y < 2 else commute_util_base                       # noqa: F821


def commute_elig(t):
    """Whether a commutation may be taken in month t [S1].

    All of: the contract carries the right; the issue state is not Oregon; the form has a
    certain period; the contract year is 2 or later; and this is the first month of that
    contract year, which enforces "one withdrawal per contract year".
    """
    if not commutation_enabled():
        return False
    if issue_state_excludes_withdrawal():
        return False
    n_eff = certain_mths_eff()
    if n_eff <= 0 or t > n_eff:
        return False
    y = policy_year(t)
    if y < 2:
        return False
    return t == 12 * (y - 1) + 1


def commute_disc_rate(t):
    """j(t): the commutation discount rate **[std] [unverified]**.

    ``j(t) = j0 + [CMT10(t) - CMT10(0)]`` with ``j0 = 4.00%``.  **No fixed SPIA issuer
    publishes a commutation discount formula**: one carrier gives only the cap [S1], a
    second only "an interest-rate adjustment will apply" [S2], a third only the 10-year
    CMT as the driver [S5]; the 4% comes from a fourth's *variable* contract [S7].
    ``cmt10_shift`` is a flat scalar here - a CMT path would be another input table - so
    the rate is level.  Any run with commutation enabled inherits an unsupported
    assumption; flag it in output.
    """
    return commute_disc_rate_base + cmt10_shift                      # noqa: F821


def commuted_value(t):
    """CV(t): the commuted value of the remaining certain instalments [S1].

    ``CV(t) = sum over s in T, t < s <= n_eff of inst(s) * (1 - theta_cum(t)) * v(t, s)``
    with, per the ``commute_disc_convention`` Reference::

        compound (default **[std]**):  v = (1 + j)^(-(s-t)/12)
        simple   (per [S7]):           v = max(0, 1 - j*(s-t)/12)

    Only the certain tail is discounted; the life-contingent payments after the certain
    period are untouched by a commutation [S1][S2][S5].
    """
    n_eff = certain_mths_eff()
    if t >= n_eff:
        return 0.0
    j = commute_disc_rate(t)
    conv = commute_disc_convention                                   # noqa: F821
    total = 0.0
    for s in range(t + 1, n_eff + 1):
        inst = annuity_pp_sched(s)
        if inst == 0.0:
            continue
        yrs = (s - t) / 12.0
        if conv == "compound":
            v = (1.0 + j) ** (-yrs)
        elif conv == "simple":
            v = max(0.0, 1.0 - j * yrs)
        else:
            raise ValueError("invalid commute_disc_convention")
        total += inst * v
    return total * (1.0 - commute_frac_cum(t))


def commute_amount(t):
    """W: the gross withdrawal taken in month t [S1]; zero in the base run.

    ``W = u(y) * CV(t)``, then constrained by the published limits: at least $5,000, at
    most ``CV(t)``, and leaving every remaining guaranteed payment at or above $100.  The
    residual floor is applied as a **cap** on W rather than a rejection, so a large
    requested utilization degrades to the largest admissible withdrawal; if that is below
    the $5,000 minimum, nothing is withdrawn.
    """
    if not commute_elig(t):
        return 0.0
    cv = commuted_value(t)
    if cv <= 0.0:
        return 0.0
    th = commute_frac_cum(t)
    n_eff = certain_mths_eff()
    insts = [annuity_pp_sched(s) for s in range(t + 1, n_eff + 1)]
    insts = [i for i in insts if i > 0.0]
    if not insts:
        return 0.0
    th_max = 1.0 - commute_min_payment / min(insts)                  # noqa: F821
    if th_max <= th:
        return 0.0
    w_max = cv * (th_max - th) / (1.0 - th)
    w = min(commute_util_rate(policy_year(t)) * cv, cv, w_max)
    return w if w >= commute_min_amount else 0.0                     # noqa: F821


def commute_frac_cum(t):
    """theta_cum(t): the cumulative commutation fraction applying in month t.

    Measured *before* any withdrawal taken in month t, because the notes' processing
    order records the instalment (step 3) before the commutation (step 5)::

        theta_cum(t+) = theta_cum(t) + (1 - theta_cum(t)) * W / CV(t)

    This is one carrier's pro-rata rule: future income payments through the end of the
    guaranteed period are reduced by the withdrawal percentage elected, with full payments
    resuming for life at the end of that period [S5][S2].  It applies to certain-period
    instalments **only** - applying it to the life-contingent tail contradicts every
    retrieved contract [S1][S2][S5], which is why :func:`annuity_payments` multiplies it
    by ``C(t)``.
    """
    if t <= 1:
        return 0.0
    prev = commute_frac_cum(t - 1)
    cv = commuted_value(t - 1)
    w = commute_amount(t - 1)
    if cv <= 0.0 or w <= 0.0:
        return prev
    return prev + (1.0 - prev) * w / cv


def surr_charge_rate(y):
    """sc(y): the surrender charge on a commutation in contract year y [S1].

    8% in year 2 grading to 1% in year 9 and 0% from year 10 - the only published SPIA
    surrender-charge schedule found.  Contract years below and above the table's range
    take its first and last rows; year 1 is barred from withdrawing at all, so its rate
    is never reached through :func:`commute_amount`.
    """
    tbl = data.surr_charge_table()                                   # noqa: F821
    lo, hi = int(tbl.index.min()), int(tbl.index.max())
    return float(tbl.loc[min(max(int(y), lo), hi), "surr_charge_rate"])


def surr_charge(t):
    """The surrender charge retained by the insurer on a commutation in month t [S1]."""
    return pols_if_init() * commute_amount(t) * surr_charge_rate(policy_year(t))


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y(t) - 1)`` **[std]**."""
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def annuity_pp_paid(t):
    """The instalment per contract after any prior commutation, before survival weighting.

    ``inst(t) * (1 - theta_cum(t)*C(t))``: a commutation reduces certain-period
    instalments only.
    """
    return annuity_pp(t) * (1.0 - commute_frac_cum(t) * certain_floor(t))


def annuity_payments(t):
    """E[ANN(t)]: expected annuity outgo in month t.

    ``inst(t) * Phi(t) * (1 - theta_cum(t)*C(t))``, scaled by ``pols_if_init``.  This is
    the column the notes' worked-example table labels "CF": at t = 1 it is 500.00, the
    instalment alone, with the maintenance expense carried separately in
    :func:`liability_cf`.
    """
    return pols_if_init() * annuity_pp_paid(t) * payment_factor(t)


def claim_pp(t, kind):
    """The claim amount per contract in month t, by ``kind``.

    ``"REFUND"`` - the cash refund lump sum ``max(0, P - G)``, zero on any form other
    than cash_refund [S1][S3][S5].  The balance is measured at ``G(t-1)`` on arrears,
    implementing "instalments already paid" for a mid-month death; in an **advance**
    payment month the instalment paid at the *start* of the death month has been paid, so
    ``G(t)`` is used or the lump sum is overstated by one instalment.
    """
    if kind != "REFUND":
        raise ValueError("invalid kind")
    if form() != "cash_refund":
        return 0.0
    paid_to = t if (payment_timing() == "advance" and is_payment_mth(t)) else t - 1
    return max(0.0, premium_pp() - cum_annuity_pp(paid_to))


def claims(t, kind=None):
    """Expected claim outgo in month t; ``kind=None`` totals every kind.

    The only kind on this product is ``"REFUND"``.  It is weighted by
    :func:`lives_death_last`, the notes' ``d_term`` - the death that terminates the income
    stream, which is the primary's on a single-life contract and the last death on a
    joint one (a cash refund on a joint contract is offered only at delta = 100% [S5]).
    """
    if kind is None:
        return claims(t, "REFUND")
    return pols_if_init() * lives_death_last(t) * claim_pp(t, kind)


def commutations(t):
    """E[COMM(t)]: the commutation payment made to the owner in month t [S1].

    ``W * (1 - sc(y))`` - the withdrawal net of its surrender charge.  Zero in the base
    run, where utilization is zero.
    """
    return pols_if_init() * commute_amount(t) * (1.0 - surr_charge_rate(policy_year(t)))


def expenses(t):
    """E[EXP(t)]: maintenance expense in month t **[std]**.

    ``(c_e / 12) * (1 + pi)^(y(t)-1) * IF(t)``: $60 per contract p.a. inflating at 2.5%,
    paid monthly while any payment obligation remains.  No insurer publishes expense
    assumptions; the "zero fees" statement [S1] refers to charges to the policyholder, not
    to the insurer's cost.  Acquisition cost is out of scope - the premium is single and
    the cost is priced in.
    """
    return expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821


def liability_cf(t):
    """CF(t): total gross liability outgo in month t, the notes' cash flow definition.

    ``E[ANN] + E[CR] + E[COMM] + E[EXP]``.  **Outgo positive**, the notes' own sign, and
    the sum of the cash flow columns of :func:`result_cf`.  There is no premium income
    in the projection - the single premium at t = 0 is a pricing input - and no surrender
    outgo, because the contract has no cash value at any time [S1][S4][S5].  Note that
    the worked-example table's "CF" column is :func:`annuity_payments`, not this.

    Both signs are published, here and in :func:`net_cf`, so that the notes' stream
    survives verbatim under the name the notes give it while the library-wide
    income-positive convention is available under the name every other model uses.
    """
    return annuity_payments(t) + claims(t) + commutations(t) + expenses(t)


def net_cf(t):
    """Net cash flow to the insurer in month t: income less outgo, so ``-liability_cf``.

    **Income positive**, the sign convention of ``Term_US_A.net_cf``, kept even though
    this product has no projected income so that every model's ``net_cf`` can be compared
    or summed across the library.  :func:`liability_cf` carries the opposite, outgo-positive
    sign of the technical notes; both are published as columns of :func:`result_cf` rather
    than one being made to stand for the other.
    """
    return -liability_cf(t)


def check_lives_roll_fwd_resid(t):
    """Residual between :func:`lives_if` and an independently rebuilt survival path.

    Deliberately **not** the telescoping identity ``l_i(t-1) - d_i(t) - l_i(t)``:
    :func:`lives_death` is *defined* as that difference, so the identity is identically
    zero whatever :func:`lives_if` returns and constrains nothing.  Each life's survival
    is rebuilt here from the assumptions instead, with no reference to the recursion -
    on the *table* basis as the running product ``prod_{s=1..t} (1 - q_m(s, i))``, which
    a misindexed or mis-based recursion breaks - and the residual is the sum of the
    per-life differences.

    On the *scenario* basis ``lives_if`` is closed form, so there is no recursion to
    close and that leg only restates the step function; the substantive check is the
    table one.  On a joint contract the last-survivor identity
    ``l_last(t) - [l_1 + l_2 - l_1*l_2]`` is added.  That term *is* zero by construction,
    like :func:`check_payment_factor_resid`, and exists to catch a future redefinition of
    :func:`lives_if_last` that broke the independence construction.
    """
    res = 0.0
    scenario = mort_basis() == "scenario"
    for i in (1, 2):
        if i == 2 and not is_joint():
            continue
        if scenario:
            d = death_mth(i)
            built = 0.0 if (d > 0 and t >= d) else 1.0
        else:
            built = 1.0
            for s in range(1, t + 1):
                built *= 1.0 - mort_rate_mth(s, i)
        res += built - lives_if(t, i)
    if is_joint():
        l1, l2 = lives_if(t, 1), lives_if(t, 2)
        res += lives_if_last(t) - (l1 + l2 - l1 * l2)
    return res


def check_lives_roll_fwd():
    """Whether the survival recursion closes at **every** projected month.

    Takes no argument and returns a ``bool``, the library-wide shape of a ``check_*``
    cells, so one test can call the same check across every model.  It is
    ``all(abs(check_lives_roll_fwd_resid(t)) < 1e-10)`` over ``t = 1 ... proj_len()``;
    the signed residual of a failing month is the more useful object when it does fail,
    and stays available as :func:`check_lives_roll_fwd_resid`.

    The tolerance is absolute, not relative: the residual is a difference of survival
    probabilities that is zero when the model is right, and ``math.isclose(x, 0.0)``
    is False for every nonzero ``x`` at the default relative tolerance.
    """
    return all(abs(check_lives_roll_fwd_resid(t)) < 1e-10
               for t in range(1, proj_len() + 1))


def check_payment_factor_resid(t):
    """``Phi(t) - max(C(t), L(t))``: the certain-period double-count guard.

    Zero by construction.  It is asserted anyway because an additive floor - ``C + L``
    instead of ``max(C, L)`` - is the notes' first-listed pitfall and would show up here
    as ``min(C, L)``.
    """
    return payment_factor(t) - max(certain_floor(t), payment_factor_life(t))


def check_payment_factor():
    """Whether the master payment factor is the certain floor at **every** projected month.

    No argument, returns a ``bool``, implemented as
    ``all(abs(check_payment_factor_resid(t)) < 1e-10)`` over ``t = 1 ... proj_len()``.
    See :func:`check_payment_factor_resid` for what the residual catches and why a
    quantity that is zero by construction is checked at all.
    """
    return all(abs(check_payment_factor_resid(t)) < 1e-10
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by month t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "claims": [claims(t) for t in ts],
            "commutations": [commutations(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of survival probabilities and payment factors, indexed by month t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "lives_if_1": [lives_if(t, 1) for t in ts],
            "lives_if_2": [lives_if(t, 2) for t in ts],
            "lives_if_last": [lives_if_last(t) for t in ts],
            "lives_death_last": [lives_death_last(t) for t in ts],
            "certain_floor": [certain_floor(t) for t in ts],
            "payment_factor_life": [payment_factor_life(t) for t in ts],
            "payment_factor": [payment_factor(t) for t in ts],
            "pols_if": [pols_if(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_table_year = 2012

mort_ae_factor = 1.084

expense_maint = 60.0

inflation_rate = 0.025

commute_util_base = 0.0

commute_disc_rate_base = 0.04

cmt10_shift = 0.0

commute_disc_convention = "compound"

commute_min_amount = 5000.0

commute_min_payment = 100.0

pd = ("Module", "pandas")