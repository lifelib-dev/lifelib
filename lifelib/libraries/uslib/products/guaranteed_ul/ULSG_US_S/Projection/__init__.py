# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.ULSG_US_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_av()          # the worked-example anchor cell
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/guaranteed_ul/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ULSG_US_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

The readers live in the unparameterized :mod:`~.ULSG_US_S.Data` Space, reached
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
surr_charge_file        data.surr_charge_table()          surr_charge_table.csv
rop_file                data.rop_table()                  rop_table.csv
======================  ================================  ==========================

.. rubric:: Projection basis

``t`` counts **policy months**, 1-based from the start of the projection: ``t = 1`` is
the issue month of a new-business model point and the first projected month of an
in-force cell, which sits ``duration_mth_init()`` completed policy months after issue.
The technical notes index the same months by their absolute policy month number,
starting at ``duration_months + 1``, so the worked example's months 301-305 are
``t = 1`` to ``t = 5`` here, with ``duration_mth(t) = 300 + t - 1``. State variables
the notes define at ``t = 0`` -- ``AV_0``, ``SG_0``, ``L_0``, ``CumPrem_0``,
``l_0 = 1``, ``g_0 = 0`` -- are the ``t == 0`` branch of the corresponding recursion.

Within each month the notes' twelve-step monthiversary order is followed exactly:

1. status check -- a policy whose 61-day grace has expired lapses at BOM with no value
   (:func:`is_lapsed`, :func:`grace_mth`);
2. premium, its two loads and the cumulative premium (:func:`premium_pp`,
   :func:`prem_to_av_pp`, :func:`prem_to_sg_pp`, :func:`cum_prem_pp`);
3. expense charges on both accounts and the withdrawal and its fee
   (:func:`maint_fee_pp`, :func:`sg_maint_fee_pp`, :func:`wd_pp`, :func:`wd_fee_pp`)
   -- after which the account value is the notes' ``AV'(t)``,
   :func:`av_pp_at(t, "BEF_COI")<av_pp_at>`, and the shadow value its ``SG'(t)``;
4. death benefit and the GPT corridor test (:func:`db_pp`);
5. the net amount at risk on both accounts, each the death benefit discounted one
   month at *that account's* credited rate less *that account's* balance floored at
   zero (:func:`net_amt_at_risk`, :func:`sg_net_amt_at_risk`);
6. cost of insurance on both accounts (:func:`coi_pp`, :func:`sg_coi_pp`);
7. the insufficiency test: if the account value cannot carry the deduction, the
   shortfall is either **forgone by the insurer** while the guarantee stands
   (:func:`mth_deduction_forgone_pp`, :func:`is_guar_supported`) or opens the grace
   period (:func:`is_shortfall`, :func:`grace_mth`);
8. end of month: interest on the post-deduction balance of each account
   (:func:`inv_income_pp`, :func:`sg_inv_income_pp`) and loan interest accrual
   (:func:`loan_bal_pp`);
9. the in-force test ``SG - L > 0`` (:func:`is_guar_active`, :func:`sg_net_pp`) and
   the catch-up requirement it implies (:func:`catch_up_prem_pp`);
10. end of month: decrements, death first, then surrender, then return-of-premium
    exercise (:func:`pols_death`, :func:`pols_lapse`, :func:`pols_rop`).

Cash flows are **undiscounted**. Premiums and expenses fall at BOM and are weighted by
``pols_if(t)``; death claims by ``pols_if(t) * mort_rate_mth(t)``; surrender payments
by ``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``; refunds by the same
survivors times ``rop_rate(t)``. Loads, charges, interest credits and **every
shadow-account entry** are internal transfers, not cash flows: the shadow account is
notional and never payable [S2][S3], so it has per-policy cells only and no in-force
weighted counterparts.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and this library's own
:mod:`.UL_US_S` -- the chassis this product is built on -- everywhere else.
Names introduced here are the ones guaranteed UL genuinely adds: the shadow account
(``sg_*``), the guarantee tests, the grace counter, the forgone deduction and the
return-of-premium endorsement. The technical notes use compact actuarial symbols; the
mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Policy month, 1-based
duration_months            duration_mth_init               Elapsed months at start
(t - 1 in months)          duration_mth(t)                 Completed policy months
y                          policy_year(t)                  Policy year
(y - 1)                    duration(t)                     Completed policy years
issue_age                  age_at_entry                    Issue age (ANB)
x_t                        age(t)                          Attained age (ANB)
sex                        sex                             Sex, M or F
risk_class                 rate_class                      Underwriting class [S4]
(none)                     proj_len                        Last projected month
face_amount, F             sum_assured                     Initial face amount
(none)                     sum_assured_at(t)               Face amount in month t
(units)                    units(t)                        Face in $1,000 units
guarantee_age              guarantee_age                   Elected guarantee age
premium_pattern            premium_type                    LEVEL / SINGLE / TEN_PAY
annual_premium             premium_pp_ann                  Scheduled premium
premium_mode               premium_mode, premium_freq()    Payment mode, per year
(premium month)            is_premium_mth(t)               A premium falls due
phi_t                      prem_persistency(t)             Premium persistency
P_t                        premium_pp(t)                   Premium received at BOM
pi                         load_prem_rate                  Base premium load, 25%
pi^g                       load_prem_rate_sg               Shadow premium load, 8%
(1-pi) P_t                 prem_to_av_pp(t)                Net premium to the AV
(1-pi^g) P_t               prem_to_sg_pp(t)                Net premium to the shadow
CumPrem_t                  cum_prem_pp(t)                  Cumulative premiums
CumPrem_0                  cum_prem_init                   Opening cumulative premium
W_t                        wd_pp(t)                        Withdrawal
(25 fee)                   wd_fee_pp(t)                    Withdrawal fee
e_pol                      expense_pol_mth                 Per-policy charge
e_u                        expense_unit_mth                Base per-unit charge
e_u^g                      expense_unit_mth_sg             Shadow per-unit charge
rc(t)                      rider_charge_pp(t)              Rider charges (0)
(e_pol + e_u F/1000 + rc)  maint_fee_pp(t)                 Base non-COI charges
(e_u^g F/1000)             sg_maint_fee_pp(t)              Shadow non-COI charges
DB_t                       db_pp(t)                        Death benefit
kappa(x)                   corridor_factor(t)              GPT corridor factor
NAAR_t                     net_amt_at_risk(t)              Base net amount at risk
NAAR_t^g                   sg_net_amt_at_risk(t)           Shadow net amount at risk
(NAAR factors)             naar_factor, sg_naar_factor     1 + j_g, 1 + j^g
(guaranteed max scale)     coi_rate_scale()                The cell's annual COI scale
m_t^max                    coi_rate_guar(t)                Guaranteed max monthly COI
m_t                        coi_rate(t)                     Current monthly COI rate
m_t^g                      sg_coi_rate(t)                  Shadow monthly COI rate
(scale precision)          coi_rate_dp()                   Quoting precision per $1,000
COI_t                      coi_pp(t)                       Base cost of insurance
COI_t^g                    sg_coi_pp(t)                    Shadow cost of insurance
(MD)                       mth_deduction_pp(t)             Base monthly deduction
(shadow MD)                sg_deduction_pp(t)              Shadow monthly deduction
D_t                        mth_deduction_forgone_pp(t)     Deduction forgone
(deduction taken)          mth_deduction_taken_pp(t)       Deduction actually taken
AV_{t-1}                   av_pp_at(t, "BEF_PREM")         Opening account value
(after premium)            av_pp_at(t, "BEF_WD")           Before the withdrawal
(after withdrawal)         av_pp_at(t, "BEF_FEE")          Before the expense charges
AV_t'                      av_pp_at(t, "BEF_COI")          After the expense charges
AV_t''                     av_pp_at(t, "BEF_INV")          After COI, floored at zero
AV_t                       av_pp(t)                        Account value, EOM
av_init                    av_pp_init                      Opening account value
(aggregate AV)             av_at(t, timing)                Account value in force
(none)                     av_change(t)                    Change in account value
SG_t'                      sg_pp_at(t, "BEF_COI")          Shadow after the charges
SG_t''                     sg_pp_at(t, "BEF_INV")          Shadow after COI, no floor
SG_t                       sg_pp(t)                        Shadow value, EOM
sg_init                    sg_pp_init                      Opening shadow value
SG_t - L_t                 sg_net_pp(t)                    The in-force test quantity
(in-force test)            is_guar_active(t)               SG_t - L_t > 0
(step 6 test)              is_guar_supported(t)            SG_t'' - L_{t-1} > 0
C_t                        catch_up_prem_pp(t)             Catch-up premium required
j_c                        inv_return_mth(t)               Monthly credited rate
j_g                        guar_rate_mth()                 Monthly guaranteed rate
j^g                        sg_rate_mth()                   Monthly shadow rate
(interest)                 inv_income_pp(t)                Interest credited to the AV
(shadow interest)          sg_inv_income_pp(t)             Interest credited to SG
L_t                        loan_bal_pp(t)                  Loan balance
loan_init                  loan_bal_init                   Opening loan balance
SC_t                       surr_charge_pp(t)               Surrender charge scheduled
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
(AV - SC)                  csv_pp(t)                       Cash surrender value
CSV_t                      ncsv_pp(t)                      Net cash surrender value
(SC retained)              surr_charge(t)                  Surrender charge collected
g_t                        grace_mth(t)                    Months in grace
(grace trigger)            is_shortfall(t)                 The deduction attempt fails
(cure payment)             cure_premium_pp(t)              Payment curing the grace
(lapse for insufficiency)  is_lapsed(t)                    Terminated in grace
(Status column)            status(t)                       The notes' status string
rop_elected                rop_elected                     Endorsement elected [S1]
rho                        rop_ratio(t)                    ROP refund ratio
w^ROP                      rop_rate(t)                     ROP exercise rate
(ROP window)               rop_anniversary(t)              20, 25 or 0
q_t^d                      mort_rate_mth(t)                Monthly mortality rate
(annual q)                 mort_rate(t)                    Annual mortality rate
(improvement)              mort_improve_rate(t)            Annual improvement rate
(improvement factor)       mort_improve_factor(t)          Cumulative improvement
b(d)                       lapse_rate_base(t)              Base annual lapse rate
G                          lapse_rate_guar_mult()          Lifetime-guarantee factor
Phi                        lapse_rate_pattern_mult()       Premium-pattern factor
Psi_t                      lapse_rate_dyn_mult(t)          Funding-status factor
(annual w)                 lapse_rate(t)                   Total annual lapse rate
w_t                        lapse_rate_mth(t)               Monthly lapse rate
l_t                        pols_if(t)                      In force at BOM of month t
(l_0)                      pols_if_init                    In force at the outset
(deaths)                   pols_death(t)                   Deaths in month t
(surrenders)               pols_lapse(t)                   Surrenders in month t
(ROP exercises)            pols_rop(t)                     Refund exercises
(grace lapse)              pols_lapse_grace(t)             Terminations in grace
(none)                     pols_maturity(t)                Maturities: always zero
(premium income)           premiums(t)                     Premium income
(death CF)                 claims(t, "DEATH")              Death claims
(surrender CF)             claims(t, "LAPSE")              Surrender payments
(ROP CF)                   claims(t, "REFUND")             Refund payments
(withdrawal CF)            withdrawals(t)                  Withdrawal payments
(expenses)                 expenses(t)                     Insurer expenses
(none)                     premium_taxes(t)                Percent-of-premium: zero
NetCF                      net_cf(t)                       Net liability cash flow
g(P)                       guar_min_sg(prem)               min over t of SG_t(P) - L_t
SG_t(P)                    sg_pp_solve(t, prem)            Shadow value under P
P*                         no_lapse_premium()              Solved no-lapse premium
=========================  ==============================  ==========================

Nine names needed care.

The notes' ``risk_class`` is this model's ``rate_class`` -- the name ``Term_US_A`` and
:mod:`.UL_US_S` both use for the underwriting class, and the one the model point
table column carries, so the notes' word appears nowhere in the model. It is the only
model point attribute renamed on cross-model grounds rather than for a reason internal
to this product.

``l_t`` in these notes is the in-force probability at the **beginning** of month ``t``
-- the notes weight every cash flow of month ``t`` by ``l_t`` and roll forward with
``l_{t+1} = l_t (1 - q^d)(1 - w)(1 - w^ROP)`` -- so it maps straight onto
``pols_if(t)`` with no offset. Note the contrast with the universal life chassis, whose
notes define ``l(t)`` at the **end** of month ``t``, making ``pols_if(t) = l(t-1)``
there.

The account value measured for the net amount at risk is ``AV'(t)``, which in these
notes is the balance **after the expense charges and before the cost of insurance** --
``av_pp_at(t, "BEF_COI")``. The universal life chassis measures it before the entire
monthly deduction, ``av_pp_at(t, "BEF_FEE")``. The guaranteed-UL notes flag the
difference as a deliberate deviation; it is immaterial at the modelled charge levels
but it is real, and ``"BEF_COI"`` exists so that the two models can be reconciled
without reading the formulas.

The notes' ``CSV_t = max(AV_t - SC_t - L_t, 0)`` already nets policy debt, so it is
this model's :func:`ncsv_pp`, not its :func:`csv_pp`. :func:`csv_pp` is the chassis'
``AV - SC`` floored at zero, and keeping both means the surrender-charge and the
indebtedness offsets can be read separately.

``D_t`` is the monthly deduction the insurer **forgoes** because the account value is
exhausted while the guarantee stands. It is not a receivable and must never accrue
against future premiums or account value recoveries -- treating it as one understates
the guarantee cost, which the notes list among the pitfalls.
:func:`mth_deduction_forgone_pp` therefore feeds nothing but the diagnostics, and
:func:`mth_deduction_taken_pp` -- what actually left the account -- is what the
account value roll-forward and the margins use.

The guarantee is tested twice at slightly different points, and the notes use the same
words for both. :func:`is_guar_supported` is the step-6 test ``SG''_t - L_{t-1} > 0``,
which decides whether a failed deduction is forgone or opens the grace period;
:func:`is_guar_active` is the step-9 in-force test ``SG_t - L_t > 0``, measured after
the shadow interest credit and the loan accrual. Running the second before the
deduction attempt -- the notes' "order of tests" pitfall -- shifts claim timing at
exactly the durations where the net amount at risk is the whole death benefit.

``maint_fee_pp`` is the notes' non-COI monthly *charge* against the account value and
is therefore insurer income, following ``CashValue_SE.maint_fee``. :func:`expenses` is
something different -- the insurer's own **[std]** acquisition, maintenance and claim
expense, a cash flow. The two must not be confused: ``maint_fee`` is income,
``expenses`` is outgo.

A partial withdrawal is **not a claim**. It is a payment the owner elects to take out
of a policy that stays in force, not an event that terminates one, so it is
:func:`withdrawals` and a ``withdrawals`` column of :func:`result_cf`, and ``claims(t,
"WITHDRAWAL")`` raises ``ValueError("invalid kind")``. :func:`claim_pp` keeps its
``"WITHDRAWAL"`` branch, because the per-policy amount is what :func:`withdrawals`
weights, and :func:`claims_from_av` keeps its own, because a withdrawal does release
account value; only the *claim* aggregate excludes it, and its ``kind is None`` total
must not double-count it.

:func:`coi_rate_dp` is the one place where the notes' worked example and the notes'
own rule disagree by more than rounding; see its docstring and the README.
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
    """The underwriting class of the selected model point (four NT, two tobacco) [S4]."""
    return model_point()["rate_class"]


def sum_assured():
    """F: the initial face amount of the selected model point [S4][S6]."""
    return float(model_point()["sum_assured"])


def guarantee_age():
    """The elected secondary-guarantee age, any attained age from 90 to 121 [S1][S2][S9].

    121 is the lifetime election, which is what the anchor cell carries and what
    switches :func:`lapse_rate_guar_mult` to the 0.55 multiplier [R7].
    """
    return int(model_point()["guarantee_age"])


def premium_type():
    """The premium pattern: ``"LEVEL"``, ``"SINGLE"`` or ``"TEN_PAY"`` **[std]**.

    A first-class model point attribute because funding pattern drives both the
    guarantee trajectory and observed lapse behaviour [R8].
    """
    return model_point()["premium_type"]


def premium_mode():
    """The premium mode: ``"A"``, ``"S"``, ``"Q"`` or ``"M"`` (EFT only) [S2]."""
    return model_point()["premium_mode"]


def premium_pp_ann():
    """The scheduled annual premium per policy, or the single premium for ``"SINGLE"``.

    For the anchor cell this is the notes' solved level no-lapse premium
    ``P* = 10,800`` **[std]**; :func:`no_lapse_premium` re-derives it from the shadow
    recursion rather than reading it from here.
    """
    return float(model_point()["premium_pp_ann"])


def load_prem_rate():
    """pi: the base premium expense charge, 25% of every premium, all years [S3][S7].

    Contractual here, unlike the universal life chassis where the load is a
    non-guaranteed element; it sits in the model point table for the same reason it
    does there, so that the table alone describes the policy.
    """
    return float(model_point()["load_prem_rate"])


def av_pp_init():
    """AV_0: the base account value per policy at the outset, 0 at issue."""
    return float(model_point()["av_pp_init"])


def sg_pp_init():
    """SG_0: the shadow account value per policy at the outset, 0 at issue.

    Not floored anywhere in the projection: a negative shadow balance measures the
    catch-up shortfall, and flooring it destroys :func:`catch_up_prem_pp`.
    """
    return float(model_point()["sg_pp_init"])


def loan_bal_init():
    """L_0: the policy loan balance per policy at the outset, 0 in every shipped point."""
    return float(model_point()["loan_bal_init"])


def cum_prem_init():
    """CumPrem_0: cumulative premiums already paid at the outset.

    The notes make this a model point attribute because it drives the return-of-premium
    refund [S1] and the 7-pay test [R5].  For the anchor cell it is the 25 annual
    premiums of $10,800 implied by the in-force snapshot **[std]**.
    """
    return float(model_point()["cum_prem_init"])


def pols_if_init():
    """l_0: the in-force probability at the outset, 1 for a single-policy point."""
    return float(model_point()["pols_if_init"])


def duration_mth_init():
    """Completed policy months already elapsed when the projection starts.

    0 for a new-business model point, so that ``t = 1`` is the issue month; 300 for
    the notes' worked-example cell, whose months 301-305 are ``t = 1`` to ``t = 5``.
    This is the notes' ``duration_months``.
    """
    return int(model_point()["duration_mth"])


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point."""
    return bool(model_point()["has_surr_charge"])


def surr_charge_id():
    """The surrender charge schedule ID, a row label of *surr_charge_table.csv*."""
    return model_point()["surr_charge_id"]


def rop_elected():
    """Whether the return-of-premium endorsement applies [S1].

    Built into the representative contract, so it is on for every point but the one
    that switches it off to isolate the guarantee mechanics.
    """
    return bool(model_point()["rop_elected"])


def coi_rate_dp():
    """Decimal places the declared COI scales are quoted to per $1,000; -1 = exact.

    **The one place where the notes' rule and the notes' worked example disagree by
    more than rounding.**  The rule is that the current scale is 65% and the shadow
    scale 55% of the guaranteed maximum, which at the worked example's
    ``m^max = 8.615`` gives 5.59975 and 4.73825.  The worked example is computed with
    5.60 and 4.74 -- the same figures rounded to the cent per $1,000, which is how the
    notes quote them -- and the difference is about $0.12 a month of base deduction and
    $0.65 of shadow deduction, an order of magnitude more than the cent-level rounding
    that explains the rest of that table.

    Rather than pick one, the model ships both.  A model point that leaves this column
    blank takes the rule at full precision; the worked-example anchor sets it to 2 and
    holds both declared scales to the cent per $1,000, which is a perfectly ordinary
    way for an admin system to carry a rate table and reproduces the notes' table.
    """
    o = model_point()["coi_rate_dp"]
    return -1 if pd.isna(o) else int(o)                              # noqa: F821


def duration_mth(t):
    """Completed policy months at the beginning of policy month t.

    ``duration_mth_init() + t - 1``, so it is 0 in the issue month of a new-business
    model point and 300 in the first month of the notes' worked example.  Note the
    contrast with the notes' own month index, which counts the current month as well;
    see :func:`surr_charge_rate`.
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

    Age advances on the policy anniversary, not on the birthday, which is the ANB
    convention the whole model is built on **[std]**.  Mixing an ALB basis into the
    COI or mortality lookups shifts both by up to half a year of mortality, which the
    notes list among the pitfalls.
    """
    return age_at_entry() + duration(t)


def proj_len():
    """Projection length in policy months.

    ``12 * (charges_cease_age - age_at_entry()) - duration_mth_init()``, the notes'
    maximum projection length: the projection runs to attained age 121, where premiums
    and all charges cease.  Coverage continues past that point under the contract
    [S7], but the illustrative mortality table reaches 1.0 at attained age 120, so
    nothing survives the horizon.
    """
    return 12 * (charges_cease_age - age_at_entry()) - duration_mth_init()  # noqa: F821


def sum_assured_at(t):
    """F(t): the face amount in policy month t.

    Level: face increases are not permitted [S2] and elective decreases, option
    changes and the face reduction some designs attach to a withdrawal are not
    modelled -- the notes' withdrawal reduces the account and shadow balances only.
    The cells is kept so the chassis' shape is unchanged and a design with face
    movement can specialise it.
    """
    return sum_assured()


def units(t):
    """U: the face amount in $1,000 units, ``sum_assured_at(t) / 1000``.

    Both per-unit charges are quoted per $1,000 of **initial** face per month, and the
    surrender charge per $1,000 of initial face; with a level face they coincide.
    """
    return sum_assured_at(t) / 1000


def crediting_rate_ann(t):
    """i^c: the current declared annual effective credited rate, 3.50% **[std]**.

    A non-guaranteed element declared at insurer discretion within the guaranteed
    bounds and governed by ASOP 2 [REG-R26].  The base run holds the snapshot scale
    level, as the notes prescribe; re-rating is out of scope.
    """
    return crediting_rate_curr                                       # noqa: F821


def inv_return_mth(t):
    """j_c: the monthly credited rate, ``(1 + i^c)^(1/12) - 1``, floored at j_g.

    0.0028709 at the **[std]** 3.50% current rate, matching the notes.  The floor is
    the contractual 2.0% guaranteed minimum [S3][S5][S7]; it does not bind at the
    snapshot scale.
    """
    return max((1 + crediting_rate_ann(t)) ** (1 / 12) - 1, guar_rate_mth())


def guar_rate_mth():
    """j_g: the monthly guaranteed rate, ``(1 + i_guar)^(1/12) - 1`` = 0.0016516."""
    return (1 + guar_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def sg_rate_mth():
    """j^g: the monthly shadow credited rate, ``(1 + i^g)^(1/12) - 1`` = 0.0044717.

    5.5% annual effective **[std]**, comfortably below the AG 38 8E cap of a
    Moody's-composite-yield index plus 3% that classifies a Design #1 shadow account
    [R1], and well above the 2.0% base guarantee -- which is what makes the guarantee
    outlive the cash value.
    """
    return (1 + sg_rate_ann) ** (1 / 12) - 1                         # noqa: F821


def naar_factor():
    """The base NAAR factor, ``1 + j_g`` = 1.0016516.

    The death benefit is discounted one month at the **guaranteed** rate, never the
    credited rate.  Using the undiscounted death benefit instead changes the cost of
    insurance by about 0.17% a month at the 2% guarantee, which the notes list first
    among the pitfalls; the same convention must hold on both accounts.
    """
    return 1 + guar_rate_mth()


def sg_naar_factor():
    """The shadow NAAR factor, ``1 + j^g`` = 1.0044717 **[std]**.

    The shadow account discounts the death benefit at *its own* credited rate, which
    is what the notes' step 4 writes, so the two accounts see different net amounts at
    risk even before their balances diverge.
    """
    return 1 + sg_rate_mth()


def loan_rate_mth():
    """The monthly charged loan rate, ``(1 + r_L)^(1/12) - 1`` at r_L = 5.0% [S4].

    Charged in arrears and guaranteed; monthly accrual is the model's discretization
    **[std]**.
    """
    return (1 + loan_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def loan_cr_rate_mth():
    """The monthly rate credited on the loaned account value, 3.0% annual [S4].

    Guaranteed, and 200 basis points below the charged rate -- the contractual loan
    spread.
    """
    return (1 + loan_cr_rate_ann) ** (1 / 12) - 1                    # noqa: F821


def premium_freq():
    """Scheduled premium payments per policy year, from :func:`premium_mode` [S2].

    Annual 1, semi-annual 2, quarterly 4, monthly (EFT only) 12.  Non-annual modes
    carry modal factors in the source design; no carrier publishes them, so the
    scheduled annual premium is divided evenly **[std]** and every shipped model point
    is annual.
    """
    m = premium_mode()
    if m == "A":
        return 1
    elif m == "S":
        return 2
    elif m == "Q":
        return 4
    elif m == "M":
        return 12
    else:
        raise ValueError("invalid premium mode")


def is_premium_mth(t):
    """Whether a scheduled premium falls due at BOM of policy month t.

    ``LEVEL``    every ``12 / premium_freq()`` months from issue.
    ``SINGLE``   the issue month only.
    ``TEN_PAY``  as ``LEVEL``, for the first ``ten_pay_years`` policy years **[std]**.
    """
    pt = premium_type()
    if pt == "SINGLE":
        return duration_mth(t) == 0
    elif pt == "TEN_PAY":
        if duration(t) >= ten_pay_years:                             # noqa: F821
            return False
    elif pt != "LEVEL":
        raise ValueError("invalid premium type")
    return duration_mth(t) % (12 // premium_freq()) == 0


def prem_persistency(t):
    """phi_t: the probability the scheduled premium is actually paid **[std]**.

    98% a year for a level payer, 100% for single-pay and ten-pay, which is what the
    notes prescribe; a missed premium is never made up, so it permanently lowers the
    shadow trajectory, and catch-up behaviour is not modelled in the base run.

    The model point may override it, and the worked-example anchor overrides it to
    1.00.  That is not a tuning: the notes' worked example is a contract-mechanics
    view with the behavioural assumptions suppressed, and premium persistency is a
    class (c) behavioural assumption.  The notes are also not self-consistent about
    where phi belongs -- their cash flow list writes premium income as
    ``l_t phi_t P_t`` while their step 2 credits ``(1 - pi) P_t`` to the account, which
    would hand the account value more than the insurer received.  This model applies
    phi once, to the premium actually received, so the account value, the shadow
    account, the cumulative premium and the premium income all move together.
    """
    o = model_point()["prem_persistency_override"]
    if not pd.isna(o):                                               # noqa: F821
        return float(o)
    return prem_persistency_ann if premium_type() == "LEVEL" else 1.0  # noqa: F821


def premium_pp(t):
    """P_t: the premium received per policy at BOM of policy month t.

    The scheduled premium in a premium month times :func:`prem_persistency`, zero
    otherwise, and zero from attained age 121 when premiums are no longer accepted
    [S7].  Premiums are flexible in amount and timing after the first [S2][S4]; the
    model projects the scheduled pattern, which is what the guarantee was solved on.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    if not is_premium_mth(t):
        return 0.0
    if premium_type() == "SINGLE":
        return premium_pp_ann() * prem_persistency(t)
    return premium_pp_ann() / premium_freq() * prem_persistency(t)


def prem_to_av_pp(t):
    """The net premium credited to the base account value, ``(1 - pi) P_t`` [S3][S7]."""
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_sg_pp(t):
    """The net premium credited to the shadow account, ``(1 - pi^g) P_t`` **[std]**.

    The shadow load of 8% sits near the 7% market-wide load allowance AG 38 8B uses
    [R1] and far below the 25% base load, which is the whole point: the shadow account
    must credit premiums more generously than the real one for the guarantee to
    outlast the cash value.
    """
    return premium_pp(t) * (1 - load_prem_rate_sg)                   # noqa: F821


def prem_to_av(t):
    """Net premium credited to base account values, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """Premium income at BOM of policy month t, weighted by the in force at BOM."""
    return premium_pp(t) * pols_if(t)


def cum_prem_pp(t):
    """CumPrem_t: cumulative premiums paid per policy.

    ``CumPrem_0 = cum_prem_init()``; thereafter ``CumPrem_{t-1} + P_t``, exactly as the
    notes write it.  Withdrawals do **not** reduce it here -- that is the
    cumulative-premium-test variation's ``CumPrem^net``, not this one -- and it drives
    the return-of-premium refund [S1].
    """
    if t == 0:
        return cum_prem_init()
    return cum_prem_pp(t - 1) + premium_pp(t)


def wd_pp(t):
    """W_t: the partial withdrawal per policy at BOM of policy month t.

    Available after policy year 1 and not after attained age 121 [S2][S3][S4][S7].  The
    amount is the constant monthly figure in the model point's ``wd_pp`` column,
    **0 in every shipped model point**: the notes set utilisation to zero in the base
    model and give no pattern, so the mechanics are implemented and the behaviour is
    left to the data **[std]**.  A withdrawal reduces the account value by the amount
    plus the fee and the shadow account dollar-for-dollar, with no fee [S4].
    """
    if duration_mth(t) < 12 * wd_first_year:                         # noqa: F821
        return 0.0
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return float(model_point()["wd_pp"])


def wd_fee_pp(t):
    """The $25 withdrawal fee, charged only in a month with a withdrawal [S2][S3][S4][S7].

    Retained by the insurer, so it is account-value outgo but not a liability cash
    flow; it appears in :func:`margin_expense`, not in :func:`claims`.  It is charged
    against the base account only, never the shadow account.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force."""
    return wd_fee_pp(t) * pols_if(t)


def corridor_factor(t):
    """kappa(x_t): the GPT corridor factor at the attained age [R4][REG-R13].

    The IRC 7702(d)(2) applicable percentages, every row of them: 250% to attained age
    40, then decreasing by a ratable portion for each full year through the statute's
    breakpoints -- 215% at 45, 185% at 50, 150% at 55, 130% at 60, 120% at 65, 115% at
    70, 105% from 75 to 90 -- and 100% from attained age 95 on, which is the statute's
    last row.  Ages beyond the table take its last row.  Because guaranteed UL account
    values are deliberately thin the corridor never binds in any shipped model point --
    but it is the reason the death benefit is a ``max`` rather than the face amount.
    """
    tbl = data.corridor_factors()                                    # noqa: F821
    a = min(max(age(t), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[a, "corridor_factor"])


def db_pp(t):
    """DB_t: the death benefit per policy, ``max(F, kappa(x_t) max(AV'_t, 0))`` [S2][S4].

    Level death benefit option only, the guarantee-focused segment's design [S2][S4].
    ``AV'_t`` is the account value after the premium, the withdrawal and the expense
    charges and **before** the cost of insurance, and it is floored at zero so an
    exhausted account cannot pull the death benefit below the face amount.
    """
    return max(sum_assured_at(t),
               corridor_factor(t) * max(av_pp_at(t, "BEF_COI"), 0.0))


def net_amt_at_risk(t):
    """NAAR_t: ``max(DB_t / (1 + j_g) - max(AV'_t, 0), 0)`` [S3].

    Two conventions here are the product's, not conveniences: the death benefit is
    discounted one month at the **guaranteed** rate (:func:`naar_factor`), and the
    account value is measured after the expense charges and before the cost of
    insurance.  The account input is floored at zero so that a deficit -- the
    guarantee-support regime, where the account is exhausted and the insurer is
    funding the deduction -- never inflates the net amount at risk above the
    discounted death benefit.  In that regime the cost of insurance is charged on
    essentially the whole face amount, which is what dominates late-duration
    guaranteed UL cash flows.
    """
    return max(0.0, db_pp(t) / naar_factor() - max(av_pp_at(t, "BEF_COI"), 0.0))


def sg_net_amt_at_risk(t):
    """NAAR_t^g: the shadow net amount at risk, ``max(DB_t / (1 + j^g) - max(SG'_t, 0), 0)``.

    The same construction as :func:`net_amt_at_risk` on the shadow parameter set
    **[std]**, discounting at the shadow credited rate and flooring the shadow balance
    at zero so that catch-up territory -- a negative shadow account -- does not inflate
    the shadow cost of insurance.
    """
    return max(0.0, db_pp(t) / sg_naar_factor()
               - max(sg_pp_at(t, "BEF_COI"), 0.0))


def coi_rate_scale():
    """The guaranteed maximum annual COI scale for this model point's cell.

    A Series indexed by **attained** age, per $1,000 of net amount at risk, sliced
    once from *coi_rates.csv* for this ``sex`` and ``rate_class``.  The shipped table
    covers the anchor cell M / StdNT over attained ages 45-121 only; a model point on
    any other cell, or a younger attained age, needs the table extended first.
    """
    return data.coi_rates().loc[(sex(), rate_class())]["coi_rate_guar_ann"]  # noqa: F821


def coi_rate_guar(t):
    """m_t^max: the guaranteed maximum **monthly** COI rate per $1,000 of NAAR.

    The annual rate from *coi_rates.csv* divided by twelve -- the notes' simple-twelfth
    conversion, fixed **[std]**.  It differs materially from
    ``1 - (1 - q)^(1/12)`` at ages 85 and over, where q exceeds 0.10, and the notes are
    explicit that the two must not be mixed.  Model 585 requires the guaranteed maxima
    to be stated in the policy [R3]; carriers do not publish them, so the shipped
    scale is illustrative **[std]**, not the 2017 CSO table [REG-R17].
    """
    scale = coi_rate_scale()
    a = min(age(t), int(scale.index.max()))
    return float(scale[a]) / 12


def coi_rate(t):
    """m_t: the current monthly COI rate, 65% of the guaranteed maximum **[std]**.

    Current COI scales are not published by any carrier, so the factor is a pure
    modelling assumption and one of the first things to sensitivity-test.  The scale
    is held to :func:`coi_rate_dp` decimals per $1,000, which reconciles the notes'
    worked example with the notes' own factor rule -- see :func:`coi_rate_dp`.
    """
    r = coi_curr_factor * coi_rate_guar(t)                           # noqa: F821
    dp = coi_rate_dp()
    return r if dp < 0 else round(r, dp)


def sg_coi_rate(t):
    """m_t^g: the shadow monthly COI rate, 55% of the guaranteed maximum **[std]**.

    Kept below the current base rate of 65% so the shadow account depletes more slowly
    than the real one, which is the defining behaviour of the product [S2][S7].
    Rounded like :func:`coi_rate`.
    """
    r = coi_sg_factor * coi_rate_guar(t)                             # noqa: F821
    dp = coi_rate_dp()
    return r if dp < 0 else round(r, dp)


def coi_pp(t):
    """COI_t: the base cost of insurance charge, ``m_t NAAR_t / 1000``.

    Zero from attained age 121, when all charges cease [S3][S7].
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def sg_coi_pp(t):
    """COI_t^g: the shadow cost of insurance charge, ``m_t^g NAAR_t^g / 1000`` **[std]**.

    Notional: it never leaves the insurer and is not a cash flow.  Zero from attained
    age 121, when the shadow charges cease with the base ones **[std]**.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return sg_coi_rate(t) / 1000 * sg_net_amt_at_risk(t)


def rider_charge_pp(t):
    """Rider charges deducted monthly, 0 in the base model **[std]**.

    Rider charges are one of the sourced monthly charge categories [S2][S3][S4][S7][S9],
    but neither rider in scope carries one: the terminal illness accelerated benefit
    takes no premium [S2][S9], and the return-of-premium endorsement is built into the
    representative contract rather than charged for [S1].  The term is carried, as it is
    on the universal life chassis, so that a rider module can be added without changing
    the recursion.
    """
    return 0.0


def maint_fee_pp(t):
    """The non-COI part of the base monthly deduction, ``e_pol + e_u U + rc`` [S3][S7].

    The $5.50 per-policy administrative charge [S3][S7], the $0.20 per $1,000 of initial
    face per month coverage charge **[std]** and rider charges.  Zero from attained age
    121, when charges cease [S3][S7].

    The name follows ``CashValue_SE.maint_fee``: this is a *charge* against the account
    value and therefore insurer income.  It is not :func:`expenses`, which is the
    insurer's own outgo.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return (expense_pol_mth + expense_unit_mth * units(t)            # noqa: F821
            + rider_charge_pp(t))


def sg_maint_fee_pp(t):
    """The non-COI part of the shadow monthly deduction, ``e_u^g U`` **[std]**.

    $0.05 per $1,000 of initial face per month and **no per-policy charge** -- the
    simplest representative choice, since no carrier publishes shadow parameters and
    AG 38 8E only describes shadow accounts as carrying expense charges [R1].
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return expense_unit_mth_sg * units(t)                            # noqa: F821


def mth_deduction_pp(t):
    """MD_t: the full base monthly deduction scheduled at BOM, ``maint_fee + COI``.

    This is what the worked example's "Base deductions" column shows.  What actually
    leaves the account is :func:`mth_deduction_taken_pp`; the remainder is
    :func:`mth_deduction_forgone_pp`.
    """
    return maint_fee_pp(t) + coi_pp(t)


def sg_deduction_pp(t):
    """The full shadow monthly deduction, ``sg_maint_fee_pp + sg_coi_pp`` **[std]**.

    The worked example's "Shdw deductions" column.  The shadow account is never
    floored, so it is always taken in full -- there is no shadow analogue of the
    forgone deduction.
    """
    return sg_maint_fee_pp(t) + sg_coi_pp(t)


def maint_fee_taken_pp(t):
    """The part of :func:`maint_fee_pp` the account value could actually carry.

    The expense charges are deducted before the cost of insurance, so they are met
    first out of the balance standing after the premium and the withdrawal.
    """
    return min(maint_fee_pp(t), max(av_pp_at(t, "BEF_FEE"), 0.0))


def coi_taken_pp(t):
    """The part of :func:`coi_pp` the account value could actually carry.

    The cost of insurance is deducted last, so it absorbs the shortfall first: this is
    the term that goes unpaid in the guarantee-support regime.
    """
    return min(coi_pp(t), max(av_pp_at(t, "BEF_COI"), 0.0))


def mth_deduction_taken_pp(t):
    """The monthly deduction actually taken from the account value in month t."""
    return maint_fee_taken_pp(t) + coi_taken_pp(t)


def mth_deduction_forgone_pp(t):
    """D_t: the monthly deduction forgone because the account value is exhausted.

    ``MD_t - (what the account could carry)``, which equals the notes' ``-AV''_t``
    whenever the balance before the charges is non-negative.  While the guarantee
    stands (:func:`is_guar_supported`) the insurer simply funds it and coverage
    continues with the account value at zero; when the guarantee has failed the same
    shortfall opens the grace period instead.

    **It is not a receivable.**  It must never accrue against future premiums or
    account value recoveries -- the notes list that among the pitfalls, because
    treating it as one understates the guarantee cost.  Nothing in the projection
    reads this cells except the diagnostics and :func:`cure_premium_pp`.

    It reports the shortfall whenever there is one, which includes the grace months and
    the months after a lapse -- where the notes' ``D_t`` is not defined at all, the
    shortfall being their *required grace payment* instead, and where the zero floor
    above it is this model's own **[std]** extension (:func:`av_pp_at`).  Read it beside
    :func:`is_guar_supported`, not on its own.
    """
    return mth_deduction_pp(t) - mth_deduction_taken_pp(t)


def maint_fee(t):
    """Non-COI monthly charges actually deducted from account values, in force."""
    return maint_fee_taken_pp(t) * pols_if(t)


def coi(t):
    """Cost of insurance charges actually deducted from account values, in force."""
    return coi_taken_pp(t) * pols_if(t)


def mth_deduction(t):
    """Monthly deductions actually taken from account values, in force."""
    return mth_deduction_taken_pp(t) * pols_if(t)


def mth_deduction_forgone(t):
    """Monthly deductions forgone because the account value is exhausted, in force.

    While :func:`is_guar_supported` holds this is the running cost of the "negative
    account economics" regime the notes describe: the insurer is paying for coverage on
    a policy whose account value is zero.  In the grace months it is not -- there the
    shortfall is the notes' *required grace payment* on a policy about to terminate --
    so :func:`result_guar` prints it beside ``is_guar_active``.  After the lapse
    ``pols_if(t)`` is zero and so is this, whatever the per-policy cells say.
    """
    return mth_deduction_forgone_pp(t) * pols_if(t)


def av_pp_at(t, timing):
    """Base account value per policy at an intra-month point of policy month t.

    The BOM events change the balance in this order, and ``timing`` names the point
    just before each of them:

    ``"BEF_PREM"``
        Before the premium: the closing balance of the previous month, ``AV_{t-1}``.

    ``"BEF_WD"``
        After the net premium, before the withdrawal.

    ``"BEF_FEE"``
        After the withdrawal and its fee, before the expense charges.

    ``"BEF_COI"``
        After the expense charges, before the cost of insurance.  **This is the notes'
        ``AV'(t)``**, and the balance the death benefit, the corridor test and the net
        amount at risk are all measured against.  The universal life chassis measures
        them one step earlier, at ``"BEF_FEE"``; the guaranteed-UL notes flag the
        difference as a deliberate deviation.

    ``"BEF_INV"``
        After the cost of insurance and **after the zero floor**, before interest.
        Interest is credited on this post-deduction balance; reversing the two
        overstates the account value by about one month's interest on the deduction
        every month.  The floor is what the guarantee buys: the account value stops at
        zero and the shortfall becomes :func:`mth_deduction_forgone_pp` rather than a
        negative balance.

        **Documented deviation [std].**  The notes floor the account value at zero
        *only while the guarantee is active* -- their step 6 sets ``AV''_t = 0`` in the
        guarantee branch and gives the grace branch no account-value recursion at all.
        This model applies the floor unconditionally, in the grace months and after a
        lapse as well.  A negative balance would break the account-value roll-forward,
        which closes on the deduction actually *taken*, and nothing is taken from an
        exhausted account.  No cash flow moves either way -- a policy in grace
        surrenders for nothing by construction and ``pols_if(t)`` is zero once it has
        lapsed -- but the per-policy account-value cells do keep running after the
        lapse, where they describe no policy.  See :func:`mth_deduction_forgone` and
        the README section "The forgone deduction is the product".

    The end-of-month balance ``AV_t`` is :func:`av_pp`.
    """
    if timing == "BEF_PREM":
        return av_pp(t - 1)
    elif timing == "BEF_WD":
        return av_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)
    elif timing == "BEF_FEE":
        return av_pp_at(t, "BEF_WD") - wd_pp(t) - wd_fee_pp(t)
    elif timing == "BEF_COI":
        return av_pp_at(t, "BEF_FEE") - maint_fee_pp(t)
    elif timing == "BEF_INV":
        return max(0.0, av_pp_at(t, "BEF_COI") - coi_pp(t))
    else:
        raise ValueError("invalid timing")


def inv_income_pp(t):
    """Interest credited to the base account value at EOM of policy month t.

    The unloaned part of the post-deduction balance earns the current monthly rate and
    the loaned part the guaranteed loaned rate of 3.0% [S4]::

        (AV''_t - L_{t-1}) x j_c + L_{t-1} x loan_cr_rate_mth()

    With the account value exhausted the credit is zero, which is why the worked
    example shows no interest from month 304.
    """
    loaned = loan_bal_pp(t - 1)
    unloaned = av_pp_at(t, "BEF_INV") - loaned
    return unloaned * inv_return_mth(t) + loaned * loan_cr_rate_mth()


def av_pp(t):
    """AV_t: the base account value per policy at the end of policy month t.

    ``AV_0 = av_pp_init()``; thereafter the floored post-deduction balance plus one
    month's interest.  An exhausted account never goes negative and the shortfall is
    recorded as :func:`mth_deduction_forgone_pp` instead.

    Floored at zero *throughout* -- in grace and after a lapse as well as under a live
    guarantee.  The notes floor it "only while the guarantee is active"; applying the
    floor unconditionally is a **[std]** deviation that moves no cash flow but does
    leave this cells running after the policy has gone.  :func:`av_pp_at` sets out why.
    """
    if t == 0:
        return av_pp_init()
    return av_pp_at(t, "BEF_INV") + inv_income_pp(t)


def av_at(t, timing):
    """Base account value in force at an intra-month point of policy month t.

    :func:`av_pp_at` times the number of policies in force, which is constant through
    the month because decrements are end-of-month events.  ``timing`` takes the same
    values as :func:`av_pp_at`, plus ``"EOM"`` for the closing balance before
    decrements.
    """
    if timing == "EOM":
        return av_pp(t) * pols_if(t)
    return av_pp_at(t, timing) * pols_if(t)


def inv_income(t):
    """Interest credited to base account values, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month's interest.
    """
    return inv_income_pp(t) * pols_if(t)


def av_change(t):
    """Change in the base account value in force over policy month t.

    ``av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")``, following ``CashValue_SE``.
    """
    return av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")


def loan_bal_pp(t):
    """L_t: the policy loan balance per policy at the end of policy month t.

    ``L_0 = loan_bal_init()``; thereafter ``L_{t-1} x (1 + r_L)^(1/12)`` at the
    guaranteed 5.0% charged in arrears [S4], accrued monthly **[std]**.  New loans and
    repayments are not modelled -- the notes give no utilisation pattern -- so this
    only rolls the model point's opening balance forward.  Indebtedness is deducted
    from the guarantee in-force test (:func:`sg_net_pp`), from death proceeds and from
    the surrender value; the shadow account itself is not reduced by it [S4][S2].
    """
    if t == 0:
        return loan_bal_init()
    return loan_bal_pp(t - 1) * (1 + loan_rate_mth())


def sg_pp_at(t, timing):
    """Shadow account value per policy at an intra-month point of policy month t.

    The same timings as :func:`av_pp_at`, on the shadow parameter set:

    ``"BEF_PREM"``
        The closing shadow balance of the previous month, ``SG_{t-1}``.

    ``"BEF_WD"``
        After the shadow net premium ``(1 - pi^g) P_t``, before the withdrawal.

    ``"BEF_FEE"``
        After the withdrawal, which reduces the shadow account dollar-for-dollar and
        carries **no fee** [S4] **[std]**, before the per-unit charge.

    ``"BEF_COI"``
        After the shadow per-unit charge, before the shadow cost of insurance.  **This
        is the notes' ``SG'(t)``.**

    ``"BEF_INV"``
        After the shadow cost of insurance, before interest.  This is the notes'
        ``SG''(t)`` and it is **not floored**: a negative shadow balance is the
        catch-up shortfall, and flooring it destroys :func:`catch_up_prem_pp` and
        misprices restoration.
    """
    if timing == "BEF_PREM":
        return sg_pp(t - 1)
    elif timing == "BEF_WD":
        return sg_pp_at(t, "BEF_PREM") + prem_to_sg_pp(t)
    elif timing == "BEF_FEE":
        return sg_pp_at(t, "BEF_WD") - wd_pp(t)
    elif timing == "BEF_COI":
        return sg_pp_at(t, "BEF_FEE") - sg_maint_fee_pp(t)
    elif timing == "BEF_INV":
        return sg_pp_at(t, "BEF_COI") - sg_coi_pp(t)
    else:
        raise ValueError("invalid timing")


def sg_inv_income_pp(t):
    """Interest credited to the shadow account at EOM, ``SG''_t x j^g`` **[std]**.

    Credited on the post-deduction shadow balance with no floor and no loaned/unloaned
    split: the shadow account is notional and carries no loan of its own.
    """
    return sg_pp_at(t, "BEF_INV") * sg_rate_mth()


def sg_pp(t):
    """SG_t: the shadow account value per policy at the end of policy month t.

    ``SG_0 = sg_pp_init()``; thereafter ``SG''_t x (1 + j^g)``.  Notional throughout:
    it exists only to run the in-force test and is never payable [S2][S3].
    """
    if t == 0:
        return sg_pp_init()
    return sg_pp_at(t, "BEF_INV") + sg_inv_income_pp(t)


def sg_net_pp(t):
    """SG_t - L_t: the shadow account net of indebtedness, the in-force test quantity.

    Indebtedness is deducted from the guarantee measure rather than from the shadow
    account itself [S4][S2].  The mainstream design; the harshest observed alternative
    voids the guarantee outright on any loan [S5].
    """
    return sg_pp(t) - loan_bal_pp(t)


def is_guar_active(t):
    """The step-9 in-force test: ``SG_t - L_t > 0`` [S4][S2][S9].

    Measured at EOM, after the shadow interest credit and the loan accrual.  While it
    holds the policy cannot lapse however exhausted the real account value is; when it
    fails, an exhausted account opens the grace period.  Strictly greater than zero, as
    the notes require: a ``>= 0`` target on a monthly grid can leave the guarantee
    failing on the final monthiversary.
    """
    return sg_net_pp(t) > 0


def is_guar_supported(t):
    """The step-6 test: ``SG''_t - L_{t-1} > 0``, measured before the interest credits.

    This is the one that decides what happens to a failed deduction -- forgone by the
    insurer, or grace.  It is deliberately a different measurement point from
    :func:`is_guar_active`, and it is evaluated **after** the full monthly deduction
    attempt: testing before the deduction lets a policy lapse a month early or late and
    shifts claim timing at exactly the durations where the net amount at risk is the
    whole death benefit.
    """
    return sg_pp_at(t, "BEF_INV") - loan_bal_pp(t - 1) > 0


def catch_up_prem_pp(t):
    """C_t: the premium that would restore the guarantee, ``max(0, -(SG_t - L_t)) / (1 - pi^g)``.

    The negative net shadow balance grossed up for the shadow premium load **[std]**;
    paying it brings ``SG - L`` back to zero and the guarantee with it [S7][R1 ex. 7].
    A diagnostic only: the notes state expressly that catch-up behaviour is not
    modelled in the base run, so no policy ever pays it.  This is why the shadow
    account must never be floored at zero.
    """
    return max(0.0, -sg_net_pp(t)) / (1 - load_prem_rate_sg)         # noqa: F821


def surr_charge_rate(t):
    """SC per $1,000 of initial face in policy month t **[std]**.

    ``max(0, sc_init - (sc_init / runoff_years) x m / 12)`` where ``m`` is the notes'
    own month index ``duration_mth(t) + 1`` -- the current month counts.  With the
    shipped 15-year schedule at $18 per $1,000 this is the spec's
    ``18 x max(0, (180 - m) / 180)``: $17.90 in the issue month, zero from the last
    month of policy year 15.  Reading the notes' month index as ``duration_mth(t)``
    would shift the entire run-off by a month.
    """
    if not has_surr_charge():
        return 0.0
    row = data.surr_charge_table().loc[surr_charge_id()]              # noqa: F821
    init = float(row["sc_per_1000_init"])
    yrs = float(row["runoff_years"])
    m = duration_mth(t) + 1
    return max(0.0, init - (init / yrs) * (m / 12))


def surr_charge_pp(t):
    """SC_t: the surrender charge scheduled per policy in policy month t.

    Quoted on the **initial** face amount.  This is the schedule, not the amount
    collected: see :func:`surr_charge`.
    """
    return surr_charge_rate(t) * sum_assured() / 1000


def csv_pp(t):
    """The cash surrender value per policy, ``AV_t - SC_t``, floored at zero.

    The floor is **[std]**: a negative cash surrender value would be a payment *from*
    the policyholder.  On this product it binds for years -- guaranteed UL account
    values are deliberately thin and the 15-year surrender charge starts at $9,000 on
    a $500,000 face.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """CSV_t in the notes: the net cash surrender value, ``max(AV_t - SC_t - L_t, 0)``.

    What a surrendering policyholder is paid, and the notes' surrender outgo.  The
    notes' symbol ``CSV_t`` already nets indebtedness, so it is this cells and not
    :func:`csv_pp`; the chassis keeps the two apart so the surrender-charge and the
    debt offsets can be read separately.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """Surrender charge actually collected from the policies surrendering in month t.

    ``(AV_t - CSV_t) x pols_lapse(t)``, so it is capped by the account value where the
    :func:`csv_pp` floor binds -- which on this product is most of the first fifteen
    years.  Insurer income, and part of :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def is_shortfall(t):
    """Whether the monthly deduction attempt failed: ``AV'_t - COI_t < 0``.

    The notes' step 6 condition, evaluated **after** the full deduction attempt.  On
    its own it says nothing about lapse: while :func:`is_guar_supported` holds the
    shortfall is forgone by the insurer and coverage continues; only when the guarantee
    has failed as well does it open the grace period.
    """
    return av_pp_at(t, "BEF_COI") - coi_pp(t) < 0


def cure_premium_pp(t):
    """The payment that would cure a grace: the deduction shortfall, grossed up.

    ``D_t / (1 - pi)`` **[std]** -- the notes define the required grace payment as the
    amount curing the deduction shortfall, and a premium reaches the account value net
    of the load.  A diagnostic: the notes give no cure probability, so a policy that
    enters grace always lapses when the 61 days expire.
    """
    return mth_deduction_forgone_pp(t) / (1 - load_prem_rate())


def grace_mth(t):
    """g_t: months elapsed in the grace period, 0 when not in grace [S7].

    The counter advances only when the deduction attempt failed **and** the guarantee
    is not supporting the policy; a failed deduction under an active guarantee is
    forgone and never opens a grace.  ``g_0 = 0``.
    """
    if t < 1:
        return 0
    if is_lapsed(t):
        return 0
    if not is_shortfall(t) or is_guar_supported(t):
        return 0
    return grace_mth(t - 1) + 1


def is_lapsed(t):
    """Whether the policy has terminated for insufficiency at or before BOM of month t.

    The 61-day grace period [S7] is taken as ``grace_months`` = 2 policy months
    **[std]**; when it expires without the required payment the policy lapses at BOM
    with no value -- the cash surrender value is zero in grace by construction.  Lapse
    for insufficiency requires all three of the notes' conditions: the deduction
    attempt failed, ``SG - L <= 0``, and the grace expired uncured.
    """
    if t <= 1:
        return False
    return is_lapsed(t - 1) or grace_mth(t - 1) >= grace_months      # noqa: F821


def status(t):
    """The worked example's Status column, in ASCII.

    ``"IN FORCE"``
        the account value is carrying the policy;
    ``"IN FORCE - GUARANTEE"``
        the account value is exhausted and the guarantee is
        carrying it -- the notes' "in force - guarantee";
    ``"GRACE"``
        the deduction failed with no guarantee behind it;
    ``"LAPSED"``
        the grace expired uncured.
    """
    if is_lapsed(t):
        return "LAPSED"
    if grace_mth(t) > 0:
        return "GRACE"
    if av_pp(t) <= 0:
        return "IN FORCE - GUARANTEE"
    return "IN FORCE"


def rop_anniversary(t):
    """The return-of-premium anniversary whose window contains month t, or 0 [S1].

    The endorsement is exercisable during the 60 days following policy anniversaries
    20 and 25 [S1][S3][S4].  On a monthly grid the window is taken as the anniversary
    month itself **[std]**, so the exercise rate is applied once rather than spread
    over two monthiversaries.
    """
    if not rop_elected():
        return 0
    if duration_mth(t) % 12 != 0:
        return 0
    y = duration(t)
    return y if y in data.rop_table().index else 0                   # noqa: F821


def rop_ratio(t):
    """rho: the fraction of cumulative premiums refunded in the window, 50% or 100% [S1]."""
    a = rop_anniversary(t)
    if a == 0:
        return 0.0
    return float(data.rop_table().loc[a, "refund_ratio"])             # noqa: F821


def rop_rate(t):
    """w^ROP: the fraction of eligible in-force exercising in the window **[std]**.

    5% at the year-20 window and 10% at the year-25 window.  No public exercise study
    exists; the rationale for keeping them modest is that the 100% refund dominates
    the cash surrender value on a thin-account product, but exercising forfeits a
    now-cheap guarantee.  Mis-setting them distorts years 20-26 of the cash flows.
    """
    a = rop_anniversary(t)
    if a == 0:
        return 0.0
    return float(data.rop_table().loc[a, "exercise_rate"])            # noqa: F821


def class_factor():
    """The underwriting-class multiplier on the best-estimate mortality table **[std]**."""
    return float(data.class_factor_table().loc[rate_class(), "factor"])  # noqa: F821


def mort_improve_rate(t):
    """The annual mortality improvement rate at the attained age in month t **[std]**.

    1.0% a year to attained age 85, grading linearly to 0% at attained age 95 and zero
    thereafter.  Improvement compounds, so at the late attained ages where the net
    amount at risk is the whole death benefit it is one of the two assumptions that
    move the claims most.
    """
    a = age(t)
    if a <= mort_improve_full_age:                                   # noqa: F821
        return mort_improve_rate_init                                # noqa: F821
    if a >= mort_improve_end_age:                                    # noqa: F821
        return 0.0
    return mort_improve_rate_init * (                                # noqa: F821
        (mort_improve_end_age - a)                                   # noqa: F821
        / (mort_improve_end_age - mort_improve_full_age))            # noqa: F821


def mort_improve_factor(t):
    """The cumulative mortality improvement factor at policy month t **[std]**.

    1.0 in the first projected year, then one further year of improvement on each
    anniversary of the projection start, for at most ``mort_improve_max_years`` = 20
    years as the notes prescribe.  Improvement is applied on projection anniversaries
    **[std]**; for every shipped model point those coincide with policy
    anniversaries.
    """
    k = (t - 1) // 12
    if k <= 0:
        return 1.0
    if k > mort_improve_max_years:                                   # noqa: F821
        return mort_improve_factor(12 * mort_improve_max_years + 1)  # noqa: F821
    return mort_improve_factor(t - 12) * (1 - mort_improve_rate(t - 12))


def mort_rate(t):
    """The annual best-estimate mortality rate in policy month t.

    Base table x :func:`class_factor` x the A/E factor, which is 100% in the base run
    **[std]**, x :func:`mort_improve_factor`, capped at 1.0.  The shipped table is a
    small illustrative one **[std]**, *not* the 2015 VBT the notes recommend -- that
    family is licensed and may not be reproduced here.  Ages beyond the table take its
    last row, where the rate is 1.0; the cap is what keeps a class factor above 1 from
    pushing the terminal rate past certainty.
    """
    tbl = data.mort_table()                                          # noqa: F821
    a = min(max(age(t), int(tbl.index.min())), int(tbl.index.max()))
    return min(1.0, float(tbl.loc[a, "mort_rate"]) * class_factor()
               * mort_ae_factor * mort_improve_factor(t))            # noqa: F821


def mort_rate_mth(t):
    """q_t^d: the monthly best-estimate mortality rate, ``1 - (1 - q)^(1/12)``.

    Note that the **experience** decrement uses the compound conversion while the
    contractual COI rate uses the simple twelfth (:func:`coi_rate_guar`).  The notes
    prescribe exactly that split; the two must not be interchanged.
    """
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """b(d): the base annual lapse rate by policy year **[std]**.

    4.0%, 3.0%, 2.5%, then 2.0% in years 4-5, 1.5% in 6-10, 1.0% in 11-20 and 0.75%
    thereafter, read from *lapse_table.csv*; policy years beyond the table take its
    last row.  The shape is anchored to the public highlights of the SOA/LIMRA UL
    persistency and lapse studies [R7][REG-R20][REG-R21], whose detailed tables sit in
    a paid data package, so the levels are a standardization.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate_ann"])


def lapse_rate_guar_mult():
    """G: the guarantee-duration lapse multiplier, 0.55 for a lifetime election.

    Lifetime secondary-guarantee lapse rates run 45% below non-lifetime rates on both
    count and amount bases in the 2015-2021 industry experience [R7]; the level is
    derived from that finding and the flat duration shape is **[std]**.  This is the
    first-order assumption for a lapse-supported product: every lapse of a funded
    guarantee releases the insurer from a deeply in-the-money claim.
    """
    if guarantee_age() >= lifetime_guarantee_age:                    # noqa: F821
        return lapse_guar_mult                                       # noqa: F821
    return 1.0


def lapse_rate_pattern_mult():
    """Phi: the premium-pattern lapse multiplier **[std]**.

    Single-pay 0.6, ten-pay 0.8, level 1.0, in the direction [R8] reports -- higher
    lapses for level-pay, lower for single-pay.
    """
    pt = premium_type()
    if pt == "SINGLE":
        return lapse_pattern_mult_single                             # noqa: F821
    elif pt == "TEN_PAY":
        return lapse_pattern_mult_ten_pay                            # noqa: F821
    elif pt == "LEVEL":
        return 1.0
    else:
        raise ValueError("invalid premium type")


def lapse_rate_dyn_mult(t):
    """Psi_t: the funding-status dynamic lapse factor **[std]**.

    ``1.0``
        guarantee active and the account value still positive;
    ``0.6``
        guarantee active and the account value exhausted -- the policy is deep in
        the money to the policyholder, the regime [R8]'s tail scenarios keep 40%
        of policies in after 31 years;
    ``2.0``
        the guarantee has terminated and the policy is surviving on its account
        value alone -- a shock.  Where the account value has gone too the policy
        is already in grace and about to lapse, so the rate is academic there.

    Dynamic lapse is used by 63% of surveyed ULSG writers, and lapse and tail
    investment returns are rated the most critical ULSG assumptions [R8]; the formula
    itself is a standardization.
    """
    if not is_guar_active(t):
        return lapse_dyn_mult_guar_failed                            # noqa: F821
    if av_pp(t) > 0:
        return 1.0
    return lapse_dyn_mult_guar_only                                  # noqa: F821


def lapse_rate(t):
    """The total annual lapse rate, ``min(0.5, max(0.003, b(d) G Phi Psi_t))`` **[std]**.

    The 0.3% annual floor is applied after the dynamic factor, as the notes write it,
    and the 50% cap wraps the result; the two cannot conflict.
    """
    rate = (lapse_rate_base(t) * lapse_rate_guar_mult()
            * lapse_rate_pattern_mult() * lapse_rate_dyn_mult(t))
    return min(lapse_rate_cap, max(lapse_rate_floor, rate))          # noqa: F821


def lapse_rate_mth(t):
    """w_t: the monthly lapse rate, ``1 - (1 - w_annual)^(1/12)``."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """l_t: the number of policies in force at the beginning of policy month t.

    Decrements are end-of-month events, so the number in force is constant through the
    month and every BOM cash flow is weighted by it.  ``pols_if(1) = l_0 =
    pols_if_init()``.  A policy whose grace has expired is out at BOM with no value,
    which is why :func:`is_lapsed` is tested first.
    """
    if t == 1:
        return pols_if_init()
    if is_lapsed(t):
        return 0.0
    return (pols_if(t - 1) - pols_death(t - 1) - pols_lapse(t - 1)
            - pols_rop(t - 1) - pols_lapse_grace(t - 1))


def pols_if_at(t, timing):
    """Number of policies in force at time t, by ``timing``.

    All three ``CashValue_SE`` timings coincide for this product, and all equal
    :func:`pols_if`: there is no new business inside a projection and the contract has
    no maturity date, so nothing changes the policy count between BOM and the
    end-of-month decrements.
    """
    if timing in ("BEF_MAT", "BEF_NB", "BEF_DECR"):
        return pols_if(t)
    else:
        raise ValueError("invalid timing")


def pols_death(t):
    """Number of deaths at the end of policy month t, ``l_t x q_t^d``."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Number of surrenders at the end of policy month t.

    ``l_t (1 - q_t^d) w_t``: death is applied before lapse, which is the notes'
    ordering.
    """
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_rop(t):
    """Number of return-of-premium exercises at the end of policy month t.

    ``l_t (1 - q_t^d)(1 - w_t) w_t^ROP``, matching the notes'
    ``l_{t+1} = l_t (1 - q^d)(1 - w)(1 - w^ROP)``.  Exercise is a full surrender
    [S1][S3], so an exercising policy leaves with the refund and nothing else.
    """
    return (pols_if(t) * (1 - mort_rate_mth(t))
            * (1 - lapse_rate_mth(t)) * rop_rate(t))


def pols_lapse_grace(t):
    """Number of policies terminating for insufficiency at the end of policy month t.

    Non-zero only in the month before the grace period expires, when every remaining
    policy is out.  This is not a rate-based decrement: it is the contractual
    termination of a policy whose account value failed and whose guarantee had already
    gone, and it is needed for the in-force roll-forward to close.  The policies leave
    with no value, so it generates no claim -- the cash surrender value is zero in
    grace by construction.
    """
    if is_lapsed(t) or not is_lapsed(t + 1):
        return 0.0
    return pols_if(t) - pols_death(t) - pols_lapse(t) - pols_rop(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    Guaranteed UL has no maturity date -- at attained age 121 premiums and charges
    cease and coverage continues [S7].  The cells is kept so the in-force roll-forward
    identity has the same shape as in the term and annuity models of this library,
    where it is not zero.
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``"DEATH"``
        ``DB_t - L_t``: the death benefit less outstanding indebtedness, standard UL
        treatment **[std]**.

    ``"LAPSE"``
        :func:`ncsv_pp`, the notes' ``CSV_t = max(AV_t - SC_t - L_t, 0)``.

    ``"REFUND"``
        ``min(rho CumPrem_t, 0.40 F) - L_t``, floored at zero [S1]: the
        return-of-premium refund, capped at 40% of the face amount and net of debt.
        On the anchor cell the cap binds -- 25 years of $10,800 premiums is $270,000
        against a $200,000 cap -- which is exactly why the cap exists.

    ``"WITHDRAWAL"``
        ``W_t``.  The $25 fee is retained by the insurer and is not part of the
        payment.  A withdrawal is not a claim -- the aggregate cash flow is
        :func:`withdrawals`, not ``claims(t, "WITHDRAWAL")``, which raises -- but the
        per-policy amount keeps its branch here because :func:`withdrawals` weights it.

    ``"GRACE"``
        Zero: a policy terminating in grace terminates without value [S7].
    """
    if kind == "DEATH":
        return db_pp(t) - loan_bal_pp(t)
    elif kind == "LAPSE":
        return ncsv_pp(t)
    elif kind == "REFUND":
        return max(0.0, min(rop_ratio(t) * cum_prem_pp(t),
                            rop_cap_rate * sum_assured_at(t))        # noqa: F821
                   - loan_bal_pp(t))
    elif kind == "WITHDRAWAL":
        return wd_pp(t)
    elif kind == "GRACE":
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim released from the account value, by ``kind``.

    Death, surrender and refund all release the end-of-month account value ``AV_t``,
    because decrements follow the interest credit; so does a policy terminating in
    grace, though its account value is zero by construction.  ``"MATURITY"`` is zero:
    the contract has no maturity date.

    ``"WITHDRAWAL"`` keeps its branch even though a withdrawal is not a claim: it is
    taken at BOM out of the account values of the policies still in force, and it is
    the same figure as :func:`withdrawals`.
    """
    if kind == "DEATH":
        return av_pp(t) * pols_death(t)
    elif kind == "LAPSE":
        return av_pp(t) * pols_lapse(t)
    elif kind == "REFUND":
        return av_pp(t) * pols_rop(t)
    elif kind == "GRACE":
        return av_pp(t) * pols_lapse_grace(t)
    elif kind == "WITHDRAWAL":
        return withdrawals(t)
    elif kind == "MATURITY":
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_over_av(t):
    """Death claims in excess of the account value released.

    ``(claim_pp(t, "DEATH") - AV_t) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin -- and in the guarantee-support regime, where
    the account value is zero and the charge is forgone, it is the whole face amount
    with no charge behind it.
    """
    return (claim_pp(t, "DEATH") - av_pp(t)) * pols_death(t)


def claims(t, kind=None):
    """Claim outgo in policy month t, optionally by ``kind``.

    ``kind`` is ``"DEATH"``, ``"LAPSE"``, ``"REFUND"``, ``"GRACE"``, or ``None`` for
    the total.  Death claims are weighted by :func:`pols_death`, surrenders by
    :func:`pols_lapse` and refunds by :func:`pols_rop`, all end-of-month events.

    ``"WITHDRAWAL"`` is deliberately **not** a claim kind and raises: a partial
    withdrawal is a payment on the owner's election out of a policy that stays in
    force, so it is :func:`withdrawals`.  Keeping it out of this cells is what keeps
    the ``kind is None`` total from double-counting it against the ``withdrawals``
    column of :func:`result_cf`.
    """
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    elif kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    elif kind == "REFUND":
        return claim_pp(t, "REFUND") * pols_rop(t)
    elif kind == "GRACE":
        return 0.0
    elif kind is None:
        return sum(claims(t, k) for k in
                   ("DEATH", "LAPSE", "REFUND", "GRACE"))
    else:
        raise ValueError("invalid kind")


def withdrawals(t):
    """Partial withdrawal payments in policy month t, for the policies in force.

    ``W_t x l_t``.  Withdrawals are taken at BOM by policies still in force, so the
    weight is :func:`pols_if` and not a decrement.  A withdrawal is a payment on the
    owner's election, not a claim, which is why it is a cells and a ``result_cf()``
    column of its own rather than a ``kind`` of :func:`claims`.  The $25 fee is
    retained by the insurer and is :func:`wd_fees`, not part of this payment.

    Zero in every shipped model point: the notes set withdrawal utilisation to zero in
    the base model and give no pattern, so the mechanics are implemented and the
    behaviour is left to the data **[std]**.
    """
    return claim_pp(t, "WITHDRAWAL") * pols_if(t)


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(y - 1)`` **[std]**.

    Expenses inflate by policy year, not by month, which is how the notes write the
    $75 per policy per year maintenance expense.
    """
    return (1 + inflation_rate) ** (policy_year(t) - 1)              # noqa: F821


def expenses(t):
    """The insurer's own expenses in policy month t **[std]**.

    Acquisition in policy year 1 -- $300 a policy in the issue month plus 90% of every
    first-year premium, which is the notes' combined commission and issue allowance --
    maintenance of $75 a policy a year inflating at 2.5%, spread evenly over the
    months, and $300 of claim expense per death.

    Not to be confused with :func:`maint_fee`, which is the *charge against the
    account value*.
    """
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    if policy_year(t) == 1:
        acq = acq + expense_acq_prem_rate * premium_pp(t)            # noqa: F821
    return ((acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821
            + expense_claim * pols_death(t))                         # noqa: F821


def premium_taxes(t):
    """Percent-of-premium expense, **zero** on this product.

    The universal life chassis carries a 2.5% premium tax; the guaranteed-UL notes'
    expense list has no percent-of-premium item at all -- the commission sits inside
    the acquisition expense instead -- so the rate is zero and the cells is kept only
    so ``result_cf()`` has the chassis' shape.  Adding a tax here would be an
    unsourced assumption.
    """
    return premium_tax_rate * premiums(t)                            # noqa: F821


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``pi x GP + withdrawal fees + the deduction's non-COI part actually taken
    + surrender charges collected + the account value left behind by a policy
    terminating in grace - expenses - premium taxes``.  The last of those is zero by
    construction, because the account value is exhausted before a grace can begin; it
    is carried so :func:`check_margin` closes without a special case.
    """
    return (load_prem_rate() * premiums(t)
            + wd_fees(t)
            + maint_fee(t)
            + surr_charge(t)
            + claims_from_av(t, "GRACE")
            - expenses(t)
            - premium_taxes(t))


def margin_mortality(t):
    """Mortality margin: :func:`coi` net of :func:`claims_over_av`.

    Deeply negative once the account value is exhausted: the cost of insurance is
    forgone while the death benefit is still the whole face amount.  That is the
    "negative account economics" regime the notes describe, and it is what dominates
    late-duration guaranteed UL liability cash flows.
    """
    return coi(t) - claims_over_av(t)


def margin_rop(t):
    """Return-of-premium margin: the account value released less the refund paid.

    ``(AV_t - claim_pp(t, "REFUND")) x pols_rop(t)``.  Large and negative on a
    thin-account product, which is the point of the endorsement: it is an option
    against the insurer whose cost depends on cumulative premiums against the reserve
    released.
    """
    return (av_pp(t) - claim_pp(t, "REFUND")) * pols_rop(t)


def net_cf(t):
    """Net liability cash flow in policy month t, **undiscounted**.

    ``premiums - death claims - surrender payments - refunds - withdrawal payments
    - expenses - premium taxes``.  Income-positive, as in every model of this library.
    Withdrawals are subtracted here as :func:`withdrawals` rather than through
    :func:`claims`, which no longer carries them.

    Like the rest of this library the model projects *gross liability cash flows*:
    there is no discounting and no change in account value in this figure, because
    reserves are a separate layer that consumes these flows.  Loads, charges, interest
    credits and every shadow-account entry are internal transfers and do not appear --
    see :func:`check_margin` for how they reconcile.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - premium_taxes(t))


def solve_len():
    """The number of months the funding-premium solve has to keep the guarantee alive.

    ``12 x (guarantee_age() - age_at_entry()) - duration_mth_init()``, the notes'
    stopping time.  A shorter guarantee age solves the same way with the earlier
    stopping time.
    """
    return 12 * (guarantee_age() - age_at_entry()) - duration_mth_init()


def sg_pp_solve(t, prem):
    """SG_t(P): the shadow account under a hypothetical premium scale ``prem``.

    ``prem`` is the annual premium for a level or ten-pay pattern and the single
    premium for a single-pay one; the payment months are the model point's own, so
    single-pay and n-pay premiums solve over their premium vectors exactly as the
    notes prescribe.

    A self-contained replay of the shadow recursion with **decrements off and premium
    persistency off** -- the solve is contractual, not behavioural, as the notes say --
    and with the death benefit held at the face amount.  The notes justify the latter
    by capping the search domain at the guideline premium limitation [R4], inside which
    the corridor does not bind for this thin-account design.

    It shares :func:`sg_coi_rate` and :func:`units` with the projection, so the COI
    lookups are cached across bisection iterates.
    """
    if t == 0:
        return sg_pp_init()
    p = prem / premium_freq() if is_premium_mth(t) else 0.0
    sgp = (sg_pp_solve(t - 1, prem) + (1 - load_prem_rate_sg) * p    # noqa: F821
           - sg_maint_fee_pp(t))
    naar = max(0.0, sum_assured_at(t) / sg_naar_factor() - max(sgp, 0.0))
    return (sgp - sg_coi_rate(t) / 1000 * naar) * (1 + sg_rate_mth())


def guar_min_sg(prem):
    """g(P): the smallest value of ``SG_t(P) - L_t`` over the guarantee period.

    Monotone non-decreasing in P on the notes' search domain, which is what makes
    bisection safe.  Evaluated in increasing ``t`` so the shadow recursion never
    recurses deeply.
    """
    return min(sg_pp_solve(t, prem) - loan_bal_pp(t)
               for t in range(1, solve_len() + 1))


def no_lapse_premium():
    """P*: the smallest premium on this model point's pattern for which ``g(P) > 0``.

    The notes' funding-premium solve.  The bracket starts at zero and doubles the
    upper end until the guarantee is funded, then bisects to ``solve_tol`` = $0.01 of
    annual premium **[std]**.  The target is ``g(P) > 0`` strictly: a ``>= 0`` target
    on a monthly grid can leave the guarantee failing on the final monthiversary.

    A side calculation -- nothing in the projection depends on it.  For the
    new-business level-pay cell it returns about $10,800, which is the figure the notes
    calibrated the **[std]** shadow parametrization to produce; the illustrative COI
    curve shipped with the model is fitted so that it does.  On the in-force anchor it
    answers a different question -- the level premium needed **from the projection
    start**, given the opening shadow balance -- and returns far more, because the
    notes' opening shadow value is not the balance a fully funded policy would carry
    at duration 300.
    """
    lo = 0.0
    hi = max(premium_pp_ann(), 1.0)
    for _ in range(solve_max_doublings):                             # noqa: F821
        if guar_min_sg(hi) > 0:
            break
        hi = hi * 2
    else:
        raise ValueError("no_lapse_premium: no funding premium found")
    while hi - lo > solve_tol:                                       # noqa: F821
        mid = (lo + hi) / 2
        if guar_min_sg(mid) > 0:
            hi = mid
        else:
            lo = mid
    return hi


def check_av_roll_fwd():
    """Check the base account value roll-forward.

    Returns ``True`` when, for every projected month, the opening account value in
    force of month ``t + 1`` equals::

        av_at(t, "BEF_PREM")
            + prem_to_av(t)
            - withdrawals(t) - wd_fees(t)
            - mth_deduction(t)
            + inv_income(t)
            - claims_from_av(t, "DEATH") - claims_from_av(t, "LAPSE")
            - claims_from_av(t, "REFUND") - claims_from_av(t, "GRACE")

    This pins the notes' processing order: that interest is credited on the
    *post-deduction* balance, that decrements come after the credit, and that what
    leaves the account is the deduction actually taken and not the deduction
    scheduled.
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
              - claims_from_av(t, "LAPSE")
              - claims_from_av(t, "REFUND")
              - claims_from_av(t, "GRACE"))
        res.append(math.isclose(av_at(t + 1, "BEF_PREM"), av,        # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-9))
    return all(res)


def check_sg_roll_fwd():
    """Check the shadow account roll-forward, per policy.

    Returns ``True`` when, for every projected month::

        sg_pp(t) == sg_pp(t - 1) + prem_to_sg_pp(t) - wd_pp(t)
                    - sg_deduction_pp(t) + sg_inv_income_pp(t)

    The shadow account is notional and carries no decrements, so this is a per-policy
    identity with no in-force weighting.  It is the check that the shadow account is
    never floored: if a zero floor crept in, this would fail the moment the balance
    went negative.
    """
    res = []
    for t in range(1, proj_len() + 1):
        sg = (sg_pp(t - 1) + prem_to_sg_pp(t) - wd_pp(t)
              - sg_deduction_pp(t) + sg_inv_income_pp(t))
        res.append(math.isclose(sg_pp(t), sg, rel_tol=1e-9, abs_tol=1e-9))  # noqa: F821
    return all(res)


def check_margin():
    """Check the net cash flow against the expense, mortality and refund margins.

    Returns ``True`` when, for every projected month::

        net_cf(t) == margin_expense(t) + margin_mortality(t) + margin_rop(t)
                     + av_change(t) - inv_income(t)
                     + loan_bal_pp(t) * pols_lapse(t)

    The last three terms are what separates a *gross liability cash flow* model from
    ``CashValue_SE``, whose ``net_cf`` already nets the change in account value and the
    investment income; the loan term is the debt extinguished against the account value
    when a policy with a loan surrenders.  The identity holds while neither the
    :func:`csv_pp` nor the :func:`ncsv_pp` floor binds against a policy loan, which is
    the case for every shipped model point.
    """
    res = []
    for t in range(1, proj_len() + 1):
        rhs = (margin_expense(t) + margin_mortality(t) + margin_rop(t)
               + av_change(t) - inv_income(t)
               + loan_bal_pp(t) * pols_lapse(t))
        res.append(math.isclose(net_cf(t), rhs,                       # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-9))
    return all(res)


def result_cf():
    """Result table of cashflows, a DataFrame indexed by policy month ``t``.

    ``pols_if`` is the in-force weight applied to that same row's cash flows -- the
    number in force at the **start** of the month -- and the remaining columns are
    income-positive under ``net_cf``: ``premiums - claims_death - claims_lapse
    - claims_rop - withdrawals - expenses - premium_taxes``.  The surrender column is
    ``claims_lapse``, matching the ``"LAPSE"`` kind that produces it, and withdrawals
    are their own column rather than a claim.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_rop": [claims(t, "REFUND") for t in ts],
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
            "pols_rop": [pols_rop(t) for t in ts],
            "pols_lapse_grace": [pols_lapse_grace(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the two account values, per policy.

    The columns are the columns of the worked example in the technical notes, in the
    notes' own order -- premium, net premium to each account, the deductions on each,
    the interest credited to each, the two closing balances -- followed by the forgone
    deduction, which the notes write inline in the deductions cell, and the status.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "premium_pp": [premium_pp(t) for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "mth_deduction_pp": [mth_deduction_pp(t) for t in ts],
            "inv_income_pp": [inv_income_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "prem_to_sg_pp": [prem_to_sg_pp(t) for t in ts],
            "sg_deduction_pp": [sg_deduction_pp(t) for t in ts],
            "sg_inv_income_pp": [sg_inv_income_pp(t) for t in ts],
            "sg_pp": [sg_pp(t) for t in ts],
            "forgone_pp": [mth_deduction_forgone_pp(t) for t in ts],
            "status": [status(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_guar():
    """Result table of the guarantee diagnostics, a DataFrame indexed by ``t``.

    The net amount at risk and cost of insurance on each account, the deduction the
    insurer forgoes across the policies in force -- the running cost of the guarantee --
    the shadow account net of debt, whether the guarantee is active, the catch-up
    premium that would restore it and the grace counter.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "net_amt_at_risk": [net_amt_at_risk(t) for t in ts],
            "coi_pp": [coi_pp(t) for t in ts],
            "mth_deduction_forgone": [mth_deduction_forgone(t) for t in ts],
            "sg_net_amt_at_risk": [sg_net_amt_at_risk(t) for t in ts],
            "sg_coi_pp": [sg_coi_pp(t) for t in ts],
            "sg_net_pp": [sg_net_pp(t) for t in ts],
            "is_guar_active": [is_guar_active(t) for t in ts],
            "catch_up_prem_pp": [catch_up_prem_pp(t) for t in ts],
            "grace_mth": [grace_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

charges_cease_age = 121

lifetime_guarantee_age = 121

guar_rate_ann = 0.02

crediting_rate_curr = 0.035

sg_rate_ann = 0.055

coi_curr_factor = 0.65

coi_sg_factor = 0.55

load_prem_rate_sg = 0.08

expense_pol_mth = 5.5

expense_unit_mth = 0.2

expense_unit_mth_sg = 0.05

loan_rate_ann = 0.05

loan_cr_rate_ann = 0.03

wd_fee = 25.0

wd_first_year = 1

ten_pay_years = 10

prem_persistency_ann = 0.98

grace_months = 2

rop_cap_rate = 0.4

mort_ae_factor = 1.0

mort_improve_rate_init = 0.01

mort_improve_full_age = 85

mort_improve_end_age = 95

mort_improve_max_years = 20

lapse_guar_mult = 0.55

lapse_pattern_mult_single = 0.6

lapse_pattern_mult_ten_pay = 0.8

lapse_dyn_mult_guar_only = 0.6

lapse_dyn_mult_guar_failed = 2.0

lapse_rate_floor = 0.003

lapse_rate_cap = 0.5

expense_acq = 300.0

expense_acq_prem_rate = 0.9

expense_maint = 75.0

expense_claim = 300.0

inflation_rate = 0.025

premium_tax_rate = 0.0

solve_tol = 0.01

solve_max_doublings = 40

pd = ("Module", "pandas")

math = ("Module", "math")
