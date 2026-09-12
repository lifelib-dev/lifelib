# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WP_UK_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's scenario A
    >>> Projection.point_id = 2            # scenario B, the down market

``t`` counts **policy months** from issue and is **0-based**, as everywhere in lifelib:
``t = 0`` is the issue month, month ``t`` runs from time ``t`` to time ``t + 1``, and
the contractual policy year containing it is the 1-based label
``policy_year(t) = t // 12 + 1``. An in-force model point opens the frame at
``t = proj_start() = 12 x duration_inforce()``, the elapsed months — so the worked
example's bond, in force at duration 5, is projected from ``t = 60``, the first month of
its sixth policy year. The state carried into that month (the asset share, the smoothed
payout, the unit price, the guaranteed benefit) is its **opening** value, read through
``asset_share_at(t, "BEF_PREM")`` and the ``*_open`` cells rather than through a row
below the frame. The frame is ``range(proj_start(), proj_len())``: ``proj_len()`` is
the number of policy months projected from issue, so the last month is
``proj_len() - 1``.

.. rubric:: A monthly grid with an annual discretion cycle

This is the one thing to hold on to about this model. The notes' rationale for an annual
grid was that **bonus declarations are annual** — they are the governing act of
discretion, and a declaration permanently hardens the guarantee. That is a fact about
the product, not about the grid, and it survives the move to monthly steps intact: the
declaration still fires once a policy year, in the twelfth month,
:func:`is_declaration_month`. Everything continuous runs monthly around it — the fund
return, the charges, the mortality charge, the decrements, the smoothed payout, the
final bonus and the market value reduction — and everything discretionary stays where
the contract puts it.

So :func:`unit_price` and :func:`guar_benefit_pp` are **step functions** of the policy
year, flat for eleven months and stepping in the twelfth; :func:`cost_of_bonus_pp` and
:func:`shareholder_transfer_pp` are nil in eleven months out of twelve;
:func:`bonus_rate` is the **annual** rate declared for the policy year the month falls
in, and the ±1% gradual-change discipline is applied once a year to it rather than
twelve times. :func:`check_declaration_is_annual` asserts all of that, because the way
this conversion goes wrong quietly is by compounding an annual bonus rate monthly: the
model still runs, the roll-forwards still close, and the guarantee is an order of
magnitude too large a decade later.

The annual rates the assumptions are quoted in — the fund return, the annual management
charge, the guarantee charge, mortality, surrender, expense inflation and the ±10%
smoothing cap — are converted with the effective ``(1 + r)^(1/12)`` and
``1 - (1 - r)^(1/12)`` forms **[std]**, so twelve months compound back to the annual
figure exactly and the basis does not move with the grid.

Two things the monthly grid genuinely says better than the annual one, and both are
about the **guarantee date**. First, a guarantee date is a date: an exit in that month
is MVR-free and an exit in the other eleven months of the same policy year is not, which
:func:`mvr_applied_pp` can now express. Second, the anti-selective encashment that
follows from it is a dated exercise rather than a year-long elevation of the surrender
rate, which is :func:`guarantee_exercise`. That second change moves an assumption's
shape and not merely its frequency, and its docstring says so.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/with_profits/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WP_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.WP_UK_S.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` and ``claim_pp(t, kind)``
with an uppercase ``kind`` string. The technical notes use compact symbols instead. The
mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
chassis                    chassis()                       UWP_bond or CWP_endowment
t                          (the cells argument)            Policy month index, 0-based
t // 12 + 1                policy_year(t)                  Contractual policy year label
(none)                     duration(t)                     Completed policy years, t // 12
(none)                     duration_mth(t)                 Months elapsed since issue, = t
(none)                     is_declaration_month(t)         The twelfth month of a policy year
(none)                     declaration_month(t)            That month, for the year holding t
x                          age_at_entry()                  Entry age (ANB)
x + duration(t)            age(t)                          Attained age (ANB)
duration_ifo               duration_inforce()              Completed years at valuation
(none)                     proj_start()                    First projected t, = 12 x duration_ifo
n                          policy_term()                   Endowment term in years
(none)                     proj_len()                      Policy months from issue, exclusive end
(none)                     fund_exhaust_mth()              Month the bond's units run out
(none)                     is_forced_encashment()          Whether the run ends there
P(t)                       premium_pp(t)                   Premium received at BOM
W(t)                       wd_pp(t)                        Partial withdrawal at BOM
W_AS(t)                    wd_as_pp(t)                     Asset-share reduction for it
r                          fund_return()                   Earned fund return, annual
r_m                        fund_return_mth()               The same, monthly
c_amc                      amc_rate                        Annual management charge
(monthly)                  amc_rate_mth()                  The same, monthly
c_g                        guar_charge_rate(t)             Guarantee/smoothing charge, annual
(monthly)                  guar_charge_rate_mth(t)         The same, monthly
CumGC(t)                   guar_charge_cum_pp(t)           Cumulative guarantee charge
AS(t)                      asset_share(t)                  Asset share at the end of month t
(the steps)                asset_share_at(t, timing)       The asset share inside month t
AS(t-1)                    asset_share_at(t, "BEF_PREM")   The balance month t opens with
M(t)                       misc_surplus_pp(t)              Estate distributions; 0 in base
Q(t)                       unit_price(t)                   With-profits unit price
U(t)                       units(t)                        Units held
FV(t), G(t)                guar_benefit_pp(t)              Guaranteed benefit
FV(t-1), G(t-1)            guar_benefit_open(t)            The guarantee month t opens with
(pre-MVR value)            policy_value_pp(t)              Guaranteed benefit + final bonus
(opening value)            policy_value_open(t)            The pre-MVR value at its open
b, b_rev                   bonus_rate(t)                   Declared annual bonus rate
b_supp                     bonus_supportable(t)            Rate the guarantee-fill implies
theta, kappa               guar_fill_target, bonus_speed   Bonus-rule parameters
CB(t)                      cost_of_bonus_pp(t)             Cost of the declared bonus
ST(t)                      shareholder_transfer_pp(t)      CB/9, the 90:10 transfer
MC(t)                      mort_charge_pp(t)               Mortality charge to the AS
DB_g(t)                    death_guar_pp(t)                Guaranteed death benefit
q(x+t)                     mort_rate(t)                    Annual mortality rate
q_m(t)                     mort_rate_mth(t)                Monthly mortality rate
w(t)                       surr_rate(t)                    Annual ordinary surrender rate
w_m(t)                     surr_rate_mth(t)                Monthly rate, exercise included
(table)                    surr_rate_base(t)               Table annual surrender rate
(spike)                    guarantee_exercise(t)           MVR-free encashment on the date
sigma                      smooth_cap                      Year-on-year smoothing cap
(monthly bounds)           smooth_cap_dn_mth(), _up_mth()  Its twelfth roots
S(t)                       smoothed_payout(t)              Smoothed target payout
S(t-1)                     smoothed_payout_open(t)         The payout month t opens with
(cap step)                 smoothed_payout_capped(t)       After the cap, before the corridor
FB(t), TB(t)               final_bonus_pp(t)               Final or terminal bonus
MVR(t)                     mvr_pp(t)                       Market value reduction, unapplied
(applied)                  mvr_applied_pp(t)               Zero where the exit is MVR-free
(guarantee dates)          is_guarantee_date(t)            MVR-free anniversary month
g_db                       death_benefit_factor            Bond death uplift, 1.01
i_sv, v_sv                 surr_disc_rate                  Endowment surrender discount
l(t)                       pols_if(t)                      In force at the start of month t
(none)                     pols_if_at(t, timing)           BEF_DECR / BEF_SURR / AFT_DECR
(none)                     pols_death(t)                   Deaths in month t
(none)                     pols_surr(t)                    Surrenders at the end of month t
(none)                     pols_maturity(t)                Maturities, or the truncation
(payouts)                  claim_pp(t, kind)               Payout per claim by kind
SM(t)                      smoothing_account(t)            Cumulative smoothing cost
(cash flows)               premiums, claims, withdrawals   Probability-weighted flows
E(t)                       expenses(t)                     Maintenance expense
ST x l                     shareholder_transfers(t)        Transfer outgo
(none)                     net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ==========================

Six names needed care.

``G`` is the guaranteed benefit on the endowment chassis and ``FV`` the unit face value
on the bond chassis, but every rule that consumes them — the bonus cost, the mortality
charge sum at risk, the final bonus, the MVR — treats them identically. They are
therefore **one cells**, :func:`guar_benefit_pp`, and the chassis decides how it rolls
forward. Keeping two names would have duplicated five rules to no purpose.

``MVR`` is computed whether or not it applies: :func:`mvr_pp` is the *scale* and
:func:`mvr_applied_pp` is what an exit actually bears, which is zero on death and on a
guarantee date. Both are needed, because the behavioural deterrent keys off the scale
being positive while the payout keys off what is applied.

``FB`` and ``TB`` are the same quantity — the non-guaranteed top-up from the smoothed
payout to the guaranteed benefit — under two names, one per chassis. They are
:func:`final_bonus_pp` here.

``q(t)`` and ``w(t)`` are the **annual** mortality and surrender rates, as the tables
quote them, with :func:`mort_rate_mth` and :func:`surr_rate_mth` carrying the monthly
conversions. That is the library-wide split — a bare ``*_rate`` is annual everywhere and
only ``*_rate_mth`` is monthly — and it is what keeps the assumption basis stated in the
units it was set in. The same goes for ``fund_return`` against
:func:`fund_return_mth` and ``amc_rate`` against :func:`amc_rate_mth`.

``guarantee_spike``, the annual grid's 2.5x multiplier on a guarantee-date *year*, is
:func:`guarantee_exercise` here: a one-off encashment rate in the guarantee-date
*month*. The rename is not cosmetic — it is a multiplier on a rate becoming a rate of
its own, because the monthly grid can put the exercise in the month the MVR-free window
is actually open.

There is **no** ``av_pp_at`` in this model, and that is a product statement rather than
an omission. The asset share is a *shadow* retrospective accumulation that the
policyholder never owns and is never paid; the guaranteed benefit is not a fund either.
Naming either of them the library's account value would assert something false about
the contract.

.. rubric:: The asset share is a state variable, not a cash flow

::

    AS(t) = [AS(t-1) + P(t) - W_AS(t)] (1 + r_m) (1 - c_amc_m - c_g_m) - ST(t) - MC(t) + M(t)

Every item in it is a recorded deduction from or addition to a retrospective
accumulation, and none of them is a policy cash flow. The policy's actual flows are
premiums, claims, withdrawals, expenses and the shareholder transfer; the asset share
reaches them only through the bonus, smoothing and MVR rules, and the difference between
what is paid and what the asset share says is absorbed by the estate. That difference is
tracked in :func:`smoothing_account`, which the base model accumulates without recycling.

:func:`asset_share_at` exposes the recursion one step at a time — ``BEF_RETURN``,
``AFT_RETURN``, ``AFT_CHARGE``, ``AFT_ST``, ``AFT_MC`` — because the order is
contractual discipline rather than arithmetic convenience: the shareholder transfer is
charged to asset shares *after* the charges and *before* the mortality charge, and the
mortality charge's sum at risk is measured on the balance after the transfer.

.. rubric:: The bonus hardens, and that is what makes guarantees expensive

A declared regular bonus increases the guaranteed benefit permanently. The unit price
therefore never falls — ``b >= 0`` is a contractual floor, not a modelling choice —
and every declaration converts non-guaranteed final bonus into guaranteed benefit
without changing the target payout. That is the whole tension the discretion manages,
and it is why ``guar_fill_target`` and ``bonus_speed`` are genuine modelling
choices with no public calibration rather than parameters someone measured.

The base projection holds the model point's snapshot rate level, as the notes specify.
:func:`bonus_supportable` and the smoothed setting rule are implemented and switched off
behind ``bonus_rule_on``, so the revision module is available for scenario work
without disturbing the reproduction of the worked example.

.. rubric:: Smoothing: the cap, then the corridor

::

    S_raw = AS(t)
    S_cap = clamp(S_raw, (1-sigma)^(1/12) S(t-1), (1+sigma)^(1/12) S(t-1))
    S(t)  = clamp(S_cap, 0.80 AS(t), 1.20 AS(t))

The cap is applied **first** and the target corridor **second**, and the order matters:
the cap is what stops a market shock reaching payouts in one step, and the corridor is
what stops the cap holding a payout indefinitely away from the asset share. In the
notes' down scenario the cap binds in every month and the corridor then does not, which
is exactly the pattern the two rules are designed to produce.

The cap is the notes' **year-on-year** ±10% discipline, taken to its twelfth root so
that twelve capped months move the payout by exactly ±10% over the policy year. That is
the conversion that keeps the rule's meaning: a flat ±10% per month would be twelve
times as loose, and a ±10% applied only at anniversaries would leave the eleven
intervening payouts unsmoothed. The notes' down scenario reaches the same closing payout
on this grid as on an annual one for exactly that reason.

The corridor implements the 80-120% target range at model-point level. The regulatory
test is a *portfolio* property — a proportion of policies within the range — and a
single-policy model cannot express it, so the deterministic corridor is a **[std]**
reading of it.

Two things the cap cannot say. It is skipped in the first projected month of a
new-business cell, where the opening payout ``S`` is nil and the cap would clamp the
payout to nil with it. And on a
**premium-paying** policy it is only loosely meaningful: a firm's ±10% discipline is a
*like-for-like* comparison between successive maturity cohorts — this year's payout on a
25-year endowment against last year's — not a comparison of one policy's own payout
across its own durations. A regular-premium asset share grows far faster than 10% a year
in early durations because premiums, not investment return, dominate it, so the cap's
upper bound binds and the corridor floor is what actually sets the payout: exactly 80% of
the asset share for most of the first dozen policy years on the endowment cell shipped
here - ``t = 0`` is the one month where the cap is skipped, so the payout there is the
asset share itself. Later the corridor floor stops binding and the capped path alone
carries the payout up towards the asset share at maturity. The single-premium bond
the worked example uses has no such problem, which is why the notes can state the cap
plainly.

.. rubric:: Final bonus and MVR are never simultaneous

``FB > 0`` requires ``S > FV`` and ``MVR > 0`` requires ``S < FV``, so the two cannot
both be positive. :func:`check_fb_mvr_exclusive` asserts it, because an implementation
that computed them independently could produce both and would then pay a final bonus and
deduct a market value reduction on the same exit.

The MVR also carries a **contractual bound**: it may not exceed the excess of the unit
value over the underlying asset value, which is ``max(0, FV - AS)``.
:func:`check_mvr_bound` asserts that too. In the notes' down scenario the bound is
2,704.05 and the MVR actually applied is 1,328.04 — comfortably inside it, which is the
point of checking rather than assuming.

The MVR is **unitised only**. It is an adjustment to a *unit* value, and the notes
define it for the unitised chassis alone; a conventional endowment has no units to
reduce. Applying the same arithmetic there would be arithmetically harmless — it happens
to collapse the surrender payout onto the asset share — but it would report a £19,575
"market value reduction" in policy year 1 of a 25-year endowment, which is not a thing
that exists. :func:`mvr_pp` returns zero on that chassis and :func:`claim_pp` sets the
surrender value on a surrender basis instead.

.. rubric:: What a deterministic run cannot do

This is a deterministic single-scenario projection, and it **materially understates the
cost of guarantees**, because guarantee cost is convex in the fund return: the average
of the cost over scenarios exceeds the cost at the average scenario. The ``c_g`` charge
in the asset share recursion is a *charging* proxy — a deduction firms make — and not a
valuation of anything. What this model produces is exactly the per-scenario cash flow
vector a market-consistent stochastic valuation consumes; the stochastic layer is out of
scope and is the reason the notes list a deterministic base run as the central model
risk.

.. rubric:: Behaviour, where the anti-selection lives

Three behavioural adjustments sit on the base surrender rate, all **[std]** and all
rationalized from the incentive structure rather than measured:

- an **MVR deterrent** of 0.6 on the annual rate while an MVR would be applied — an
  active MVR penalizes exit;
- a **guarantee-imminent suppression** of 0.8 on the annual rate in the twelve months
  before a guarantee date, policyholders waiting for the MVR-free window; and
- a **guarantee-date encashment** of 7.5% of the survivors of the guarantee-date
  **month**, applied **only when the guarantee is in the money** (``GB > AS``), because
  MVR-free encashment is worth exercising precisely then and worth nothing otherwise.

The third is the one that matters. Anti-selective exit when guarantees are in the money
is the dominant behavioural risk on with-profits business, and dynamic assumptions of
this kind are a regulatory expectation for the best estimate rather than an optional
refinement. It is also the one place where this grid changes an assumption's shape
rather than its frequency: on an annual grid it could only be a multiplier on the whole
guarantee-date year's surrender rate, which spreads MVR-free exits across eleven months
in which the window is shut. :func:`guarantee_exercise` puts it in the month the option
is open, at a rate chosen so that the guarantee-date year still sheds roughly what the
annual grid's 2.5x spike shed.

The MVR deterrent applies on the bond chassis only, because there is no MVR on the other
one. That falls out of :func:`mvr_applied_pp` rather than being coded as a special case.

.. rubric:: A withdrawal election is not unconditional

The MVR-free allowance is 5% of the original premium a year, and the withdrawing cell
takes the whole of it — a twelfth each month. Against a fund whose growth is only the
declared bonus, that exhausts the fund. :func:`wd_pp` therefore caps the withdrawal at
the unit fund it comes out of, and :func:`proj_len` stops the projection the month
before exhaustion, where
:func:`is_forced_encashment` marks the ending as a real contractual event and the
survivors are paid ``FV + FB`` rather than nothing. :func:`check_fund_nonneg` asserts the
result, because the failure mode here is silent: an uncapped election turns the unit
holding negative and every number downstream of it stays plausible enough to read past.

.. rubric:: What is out of scope, and why

The **smoothed-fund (PruFund-style) chassis** is not implemented. Its mechanics are
daily and quarterly — a 5% daily and 10% quarterly smoothing limit with a 2.5% gap
trigger — and a monthly grid still smooths away the limits that define the design: a
daily limit needs a daily step, and a trigger that fires and unwinds between two monthly
points is invisible to this projection. Moving from an annual grid to a monthly one
narrows that gap without closing it, so the exclusion stands rather than being quietly
relaxed. Implementing it here would produce something that ran and meant nothing, so
:func:`chassis` accepts the two chassis this grid can carry and says so.

Also out of scope, per the notes: paid-up conversion on the endowment chassis, the
guaranteed annuity option module on legacy pension cells (long interest-rate
optionality that needs the stochastic layer to mean anything), estate reattributions and
special bonuses, and the fund-level excess of actual expenses over capped charges, which
a single-policy model cannot see.
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


def chassis():
    """``UWP_bond`` (unitised) or ``CWP_endowment`` (conventional).

    The smoothed-fund chassis of the notes is **not implemented**: its smoothing limits
    are a 5% *daily* and a 10% quarterly movement with a 2.5% gap trigger, and a monthly
    grid can express none of them - a daily limit needs a daily step, and a trigger that
    fires between two monthly points is invisible to this projection.  See the Space
    docstring.
    """
    v = model_point()["chassis"]
    if v not in ("UWP_bond", "CWP_endowment"):
        raise ValueError(
            "invalid chassis; SF_prufund is out of scope on a monthly grid")
    return v


def is_unitised():
    """True on the unitised bond chassis, where the guaranteed benefit is a unit value."""
    return chassis() == "UWP_bond"


def age_at_entry():
    """x: the entry age of the model point, age nearest birthday **[std]**."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex (M / F) of the model point."""
    return model_point()["sex"]


def duration_inforce():
    """Completed policy **years** at the valuation date; 0 on a new-business cell.

    A policy attribute, carried on the model point in the unit a contract speaks in;
    :func:`proj_start` converts it to the grid's months.  The worked example is an
    in-force bond at duration 5, so its projection opens at ``t = 60`` - the first month
    of its sixth policy year - with the carried-in state as that month's opening
    balances.
    """
    return int(model_point()["duration_inforce"])


def premium_single_pp():
    """The single premium of the bond chassis; a pricing input on an in-force cell."""
    return float(model_point()["premium_single"])


def premium_regular_pp():
    """The regular annual premium of the endowment chassis."""
    return float(model_point()["premium_regular"])


def sum_assured():
    """The basic sum assured of the endowment chassis; the guarantee floor at outset."""
    return float(model_point()["sum_assured"])


def attaching_bonus():
    """Reversionary bonuses already attaching at the valuation date (endowment chassis)."""
    return float(model_point()["attaching_bonus"])


def policy_term():
    """n: the endowment term in years; 0 on the whole-of-life bond chassis."""
    return int(model_point()["policy_term"])


def units_init():
    """U: the units held at the valuation date (bond chassis)."""
    return float(model_point()["units"])


def unit_price_init():
    """Q: the with-profits unit price at the valuation date (bond chassis).

    On the anchor cell it is ``1.02^5 = 1.104081`` - five declarations at 2% on a unit
    seeded at £1.0000.
    """
    return float(model_point()["unit_price_init"])


def asset_share_init():
    """AS: the asset share carried into the projection.

    A retrospective accumulation, and the model point's most important number: it is
    what the payout machinery is measured against, and nobody is ever paid it.
    """
    return float(model_point()["asset_share_init"])


def smoothed_payout_init():
    """S: the smoothed payout carried in; the benchmark the year-on-year cap works from.

    On the anchor cell it is £29,500 against an asset share of £30,000 - the payout is
    already a little below the asset share, which is what the smoothing cap does after a
    good year.
    """
    return float(model_point()["smoothed_payout_init"])


def guarantee_years():
    """The policy anniversaries at which an exit is MVR-free, as a tuple of years.

    Read from a semicolon-separated model point column, empty on the endowment chassis.
    """
    v = model_point()["guarantee_dates"]
    if pd.isna(v):                                                   # noqa: F821
        return ()
    return tuple(int(float(s)) for s in str(v).split(";") if str(s).strip())


def wd_rate():
    """The partial withdrawal taken each year, as a fraction of the original premium.

    Zero in the base run; the MVR-free allowance is 5% a year, and a withdrawing cell
    takes the whole of it.
    """
    return float(model_point()["wd_rate"])


def tax_basis():
    """``life_net`` or ``pension_gross``.

    The fund return is quoted net of life-fund tax on a ``life_net`` cell and gross on a
    pension one; asset shares are accumulated on the basis that applies to the policy.
    The distinction is carried on the model point and is applied by supplying the return
    already on the right basis, rather than by grossing up inside the model.
    """
    v = model_point()["tax_basis"]
    if v not in ("life_net", "pension_gross"):
        raise ValueError("invalid tax_basis")
    return v


def fund_return():
    """r: the earned fund return, on the model point's tax basis **[std]**.

    A **scenario level** rather than a best estimate: the notes' worked example is a
    one-year, two-scenario comparison, and the shipped scenario cells hold their own
    return for the whole projection, so the first projected year reproduces the notes
    exactly and the remainder shows what that scenario implies if sustained.

    Asset shares, final bonuses and MVR incidence all key off this one number, and a
    deterministic run understates guarantee cost because the cost is convex in it.

    Read the down cell's tail for what it is.  A single year at -15% is a market shock;
    sixty consecutive years at -15% is not a scenario anyone would value against, and the
    cell duly exhausts its asset share and leaves the guarantee entirely estate-funded.
    That end of the projection is a demonstration of the machinery under stress, not a
    result.
    """
    return float(model_point()["fund_return"])


def bonus_rate_init():
    """The declared regular or reversionary bonus rate the model point carries.

    2.00% on the bond chassis and 1.50% compound on the endowment, both **[std]**:
    declarations are not published in firms' principles and practices documents.
    """
    return float(model_point()["bonus_rate"])


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_start():
    """The first projected month: ``12 x duration_inforce()``, the elapsed months.

    ``t`` is 0-based, so a cell in force at duration 5 opens its frame at ``t = 60`` -
    the first month of the sixth policy year - and a new-business cell opens it at
    ``t = 0``.  Because the conversion is a whole number of years, the frame always
    opens on a policy anniversary, which is what keeps the declaration months aligned
    with the contract.
    """
    return 12 * duration_inforce()


def fund_exhaust_mth():
    """The first projected month in which the bond's unit fund is exhausted; 0 if never.

    A level withdrawal election runs the unit holding down, and against a fund whose
    growth is only the declared bonus it eventually cancels the last unit.  This locates
    that month so :func:`proj_len` can stop before it.  Zero on the endowment chassis
    and on any bond cell taking no withdrawals, which is the ordinary case.

    Zero is safe as the "never" sentinel even though ``t = 0`` is a real month: the
    withdrawal is capped at the fund it is cancelled out of, so a bond written at
    ``t = 0`` still holds the units its single premium bought at the end of it.
    """
    if not is_unitised() or wd_rate() <= 0.0:
        return 0
    for t in range(proj_start(), 12 * (omega_age - age_at_entry())):  # noqa: F821
        if units(t) <= 1e-9:
            return t
    return 0


def proj_len():
    """The number of policy months projected from issue: the frame's exclusive end.

    The frame is ``range(proj_start(), proj_len())``, so the last projected month is
    ``proj_len() - 1``.  It is twelve times the endowment's term, or twelve times the
    whole-of-life bond's limiting age - cut short where a withdrawal election has
    exhausted the unit fund, since a bond with no units is not a bond.
    """
    if not is_unitised():
        return 12 * policy_term()
    horizon = 12 * (omega_age - age_at_entry())                      # noqa: F821
    exhaust = fund_exhaust_mth()
    if exhaust:
        return min(horizon, exhaust)
    return horizon


def is_forced_encashment():
    """Whether the bond's projection ends because the unit fund has been exhausted.

    It changes what the survivors at the end of the projection are paid.  A fund-
    exhaustion ending is a **real contractual event** - the last units are cancelled and
    the bond is encashed - so the survivors are paid out.  A limiting-age ending is a
    modelling truncation, and paying anything there would invent a claim.
    """
    return (is_unitised() and fund_exhaust_mth() > 0
            and proj_len() == fund_exhaust_mth())


def duration(t):
    """Completed policy years at the start of month t: ``t // 12``; 0 in the first year."""
    return t // 12


def duration_mth(t):
    """Months elapsed from issue at the start of month t; equal to t.

    ``t`` is 0-based and counts from issue, so the identity is trivial - the cells
    exists so the monthly models in this library share one vocabulary.
    """
    return t


def age(t):
    """The attained age (ANB) during month t: ``x + duration(t)``.

    Advances on the policy anniversary rather than monthly, which is what an
    age-nearest-birthday basis means and how the mortality table is entered.
    """
    return age_at_entry() + duration(t)


def policy_year(t):
    """The contractual policy year containing month t: the 1-based label ``t // 12 + 1``.

    ``t`` is the 0-based month index; the policy year is the 1-based label a contract
    speaks in, and it is what the guarantee dates, the declaration cycle and the lapse
    table are keyed by.  Derived here rather than indexed by, so that no schedule is
    read a row out.
    """
    return duration(t) + 1


def is_declaration_month(t):
    """Whether month t ends on a policy anniversary, and so carries a declaration.

    ``(t + 1) mod 12 = 0``.  The bonus declaration is the governing discretion cycle and
    it is **annual**: firms declare once a year, and a declaration permanently hardens
    the guarantee.  So the grid runs monthly and the declaration does not - it fires in
    the twelfth month of each policy year and nowhere else, which is what keeps this a
    change of grid rather than a change of product.
    """
    return (t + 1) % 12 == 0


def declaration_month(t):
    """The month whose end carries the declaration for the policy year containing t.

    ``12 x duration(t) + 11``.  Every month of a policy year reads the rate declared at
    that month, so a declared rate is a property of the policy year rather than of the
    month.
    """
    return 12 * duration(t) + 11


def is_guarantee_date(t):
    """Whether month t ends on a contractual guarantee date.

    A guarantee date is an anniversary, so it falls at the end of a declaration month
    whose ``policy_year(t)`` is one of the guarantee years.  An exit there is MVR-free
    and pays the full guaranteed benefit plus final bonus, which is the option
    :func:`guarantee_exercise` is exercising.  In the other eleven months of the same
    policy year the window is shut and an exit bears the market value reduction like any
    other - a distinction an annual grid could not draw.
    """
    return is_declaration_month(t) and policy_year(t) in guarantee_years()


def premium_pp(t):
    """P(t): the premium received at the start of month t.

    A twelfth of the annual regular premium on the endowment chassis - the model point
    carries the premium per year, the unit a policy document states it in, and it is
    collected monthly by direct debit **[std]** - plus the single premium in the issue
    month, ``t = 0``, which an in-force cell never reaches, so it is not double counted.
    """
    p = premium_regular_pp() / 12.0
    if t == 0:
        p += premium_single_pp()
    return p


def wd_pp(t):
    """W(t): the partial withdrawal paid at the start of month t.

    A twelfth of the annual election, which is taken as a fraction of the **original**
    premium - the form the MVR-free allowance is expressed in - and zero in the base
    run.  Within the allowance it is MVR-free.  Taking the year's allowance in twelve
    instalments rather than one is the ordinary way a bond's withdrawal facility is
    operated, and it is what the monthly grid lets the model say.

    Capped at the unit fund it is cancelled out of, the opening ``FV`` of the period.
    The cap is a physical
    constraint rather than a product rule: a level withdrawal against a fund that is
    being run down eventually exhausts it, and an uncapped election drives the unit
    holding - and with it the guaranteed benefit - negative.  Note what the cap is
    measured against: the *unit* fund, not the pre-MVR policy value, because a partial
    withdrawal cancels units and the final bonus is only paid on full encashment.  The
    residual final bonus reaches the policyholder in the encashment that
    :func:`is_forced_encashment` marks.
    """
    w = wd_rate() * premium_single_pp() / 12.0
    if w <= 0.0:
        return 0.0
    return min(w, max(0.0, guar_benefit_open(t)))


def wd_as_pp(t):
    """W_AS(t): the asset-share reduction for the month's withdrawal.

    Pro rata to the **pre-MVR policy value** the month opens with, so a withdrawal
    takes the same proportion of the asset share as it takes of what the policy is worth
    - not the same cash amount.  Zero where nothing is withdrawn or the policy value is
    nil.
    """
    w = wd_pp(t)
    if w <= 0.0:
        return 0.0
    pv = policy_value_open(t)
    if pv <= 0.0:
        return 0.0
    return asset_share_at(t, "BEF_PREM") * w / pv


def guar_charge_rate(t):
    """c_g: the **annual** guarantee and smoothing charge on the asset share **[std]**.

    0.10% a year, and it **stops** once cumulative deductions reach the lifetime cap of
    2% of the asset share.  The cap test is measured on the balance the month opens
    with rather than on its own closing one, which is what keeps the charge from
    depending on the balance it is being deducted from; on this grid it is tested every
    month rather than once a year, so the charge switches off the month the cumulative
    overtakes the threshold instead of at the following anniversary.

    Note what the cap is a fraction *of*.  The notes set it against the **current** asset
    share, not against a level struck once at first breach, so on a fund that keeps
    growing the threshold grows with it: the charge stops the year the cumulative
    overtakes it and resumes the year after, when the larger asset share has moved the
    threshold back above.  That is the rule as written; a cap frozen at first breach
    would be a different rule and a materially different charge.
    """
    prev_as = asset_share_at(t, "BEF_PREM")
    prev_cum = guar_charge_cum_pp(t - 1) if t > proj_start() else 0.0
    if prev_as > 0.0 and prev_cum >= guar_charge_cap * prev_as:      # noqa: F821
        return 0.0
    return guar_charge_rate_base                                     # noqa: F821


def guar_charge_rate_mth(t):
    """c_g monthly: ``1 - (1 - c_g)^(1/12)`` **[std]**.

    The effective conversion, so twelve months of the charge compound back to the annual
    rate the notes quote.  Zero in a month the lifetime cap has switched the charge off.
    """
    return 1.0 - (1.0 - guar_charge_rate(t)) ** (1.0 / 12.0)


def amc_rate_mth():
    """c_amc monthly: ``1 - (1 - c_amc)^(1/12)`` **[std]**.

    The same effective conversion as the guarantee charge, and for the same reason: the
    annual management charge is quoted per year and must not be restated in monthly
    units, or the basis moves with the grid.
    """
    return 1.0 - (1.0 - amc_rate) ** (1.0 / 12.0)                    # noqa: F821


def guar_charge_pp(t):
    """The guarantee and smoothing charge actually deducted in month t."""
    return guar_charge_rate_mth(t) * asset_share_at(t, "AFT_RETURN")


def guar_charge_cum_pp(t):
    """CumGC(t): cumulative guarantee and smoothing deductions to the end of month t.

    Nil before the first projected month, so the accumulation opens at zero rather
    than reading a row below the frame.
    """
    if t < proj_start():
        return 0.0
    prev = guar_charge_cum_pp(t - 1) if t > proj_start() else 0.0
    return prev + guar_charge_pp(t)


def misc_surplus_pp(t):
    """M(t): estate distributions credited to the asset share; zero in the base run.

    Miscellaneous surplus and estate distributions are allocated annually where a firm
    operates them; the base model allocates none, so the rate is a monthly one only in
    the sense that nil is nil at any frequency.
    """
    return misc_surplus_rate * asset_share_at(t, "BEF_PREM")         # noqa: F821


def fund_return_mth():
    """r_m = (1 + r)^(1/12) - 1: the monthly earned fund return **[std]**.

    The effective conversion of the scenario's annual return, so twelve months of it
    compound back to the annual figure exactly.  A nominal ``r/12`` would not, and on a
    -15% scenario the gap is not small.
    """
    return (1.0 + fund_return()) ** (1.0 / 12.0) - 1.0


def asset_share_at(t, timing):
    """The asset share at a point inside month t.

    ``"BEF_PREM"``
        the balance the month **opens** with: ``AS(t-1)``, or the
        carried-in :func:`asset_share_init` in the first projected
        month.  Everything that needs the opening asset share reads it
        here, so no cells indexes a row below the frame.

    ``"BEF_RETURN"``
        the opening balance plus the start-of-month premium, less the
        withdrawal: ``AS(t-1) + P(t) - W_AS(t)``.

    ``"AFT_RETURN"``
        after the month's fund return.

    ``"AFT_CHARGE"``
        after the annual management charge and the guarantee charge, both
        at their monthly equivalents.

    ``"AFT_ST"``
        after the shareholder transfer, which is charged to asset shares.
        It is nil in eleven months out of twelve, because a transfer
        arises only on a declaration.  **This is the balance the mortality
        charge's sum at risk is measured against.**

    ``"AFT_MC"``
        after the mortality charge and any estate distribution; the
        closing asset share of the month, and the same number as
        :func:`asset_share`.

    The steps are exposed individually because their order is contractual discipline
    rather than arithmetic convenience, and the order survives the change of grid
    unchanged: return, then charges, then the transfer, then the mortality charge on the
    balance the transfer left.
    """
    if timing == "BEF_PREM":
        if t <= proj_start():
            return asset_share_init()
        return asset_share(t - 1)
    if timing == "BEF_RETURN":
        return asset_share_at(t, "BEF_PREM") + premium_pp(t) - wd_as_pp(t)
    if timing == "AFT_RETURN":
        return asset_share_at(t, "BEF_RETURN") * (1.0 + fund_return_mth())
    if timing == "AFT_CHARGE":
        return (asset_share_at(t, "AFT_RETURN")
                * (1.0 - amc_rate_mth() - guar_charge_rate_mth(t)))
    if timing == "AFT_ST":
        return asset_share_at(t, "AFT_CHARGE") - shareholder_transfer_pp(t)
    if timing == "AFT_MC":
        return (asset_share_at(t, "AFT_ST") - mort_charge_pp(t)
                + misc_surplus_pp(t))
    raise ValueError("invalid timing")


def asset_share(t):
    """AS(t): the asset share at the end of month t.

    A **shadow retrospective accumulation**: nobody owns it and nobody is paid it.  It
    drives claim amounts only through the bonus, smoothing and MVR machinery, and the
    difference between what is paid and what it says is absorbed by the estate.

    **Floored at zero.**  The charges and the mortality charge are deductions that do not
    stop when the balance runs out, so a sustained adverse scenario - the shipped down
    cell holds its -15% for the whole projection - drives the raw recursion negative.
    A negative asset share would make the payout *target* negative and invert the
    corridor, whose bounds are ``0.80 AS`` and ``1.20 AS``.  What a nil asset share
    actually means is that the fund backing the policy is exhausted and the guarantee is
    being met entirely by the estate, which is what :func:`smoothing_account` then
    records.

    Nil before the frame opens: the carried-in balance is the *opening* value of the
    first projected period, ``asset_share_at(t, "BEF_PREM")``, not a row of its own.
    """
    if t < proj_start():
        return 0.0
    return max(0.0, asset_share_at(t, "AFT_MC"))


def unit_price(t):
    """Q(t): the with-profits unit price at the end of month t.

    ``Q(t) = Q(t-1)(1 + b)`` in a **declaration month** and ``Q(t) = Q(t-1)`` in the
    other eleven: the price is a step function of the policy year, because the
    declaration that moves it is an annual act of discretion.  It **never decreases** -
    the non-negative bonus is a contractual floor, which is what makes a declaration
    irreversible.  Constant on the endowment chassis, where the guarantee is carried as
    an amount rather than a price.  The first projected month opens at the carried-in
    price, and because the frame opens on an anniversary that price is the one the
    previous declaration left.
    """
    if t < proj_start():
        return unit_price_init()
    q = unit_price_init() if t == proj_start() else unit_price(t - 1)
    return q * (1.0 + bonus_rate(t)) if is_declaration_month(t) else q


def units(t):
    """U(t): the units held at the end of month t.

    Bought with the month's premium at the price it opens with and cancelled to fund
    the month's withdrawal.  Constant in the base run, where the bond is single premium
    and nothing is withdrawn.  Nil on the endowment chassis, which carries its guarantee
    as an amount rather than as units at a price.
    """
    if not is_unitised():
        return 0.0
    if t < proj_start():
        return units_init()
    u = units_init() if t == proj_start() else units(t - 1)
    q = unit_price_init() if t == proj_start() else unit_price(t - 1)
    if q <= 0.0:
        return u
    return u + prem_alloc_rate * premium_pp(t) / q - wd_pp(t) / q    # noqa: F821


def guar_benefit_pp(t):
    """The guaranteed benefit at the end of month t.

    The unit face value ``U(t) Q(t)`` on the bond chassis, and the sum assured plus
    attaching reversionary bonuses on the endowment, where ``G(t) = G(t-1)(1 + b)`` in a
    declaration month and ``G(t) = G(t-1)`` in the other eleven.  Two contractual forms,
    one cells: every rule that consumes it - the bonus cost, the mortality charge's sum
    at risk, the final bonus, the MVR - treats them identically, so keeping two names
    would duplicate five rules to no purpose.
    """
    if is_unitised():
        return units(t) * unit_price(t)
    if t < proj_start():
        return sum_assured() + attaching_bonus()
    g = guar_benefit_open(t)
    return g * (1.0 + bonus_rate(t)) if is_declaration_month(t) else g


def guar_benefit_open(t):
    """The guaranteed benefit month t **opens** with: ``FV(t-1)`` or ``G(t-1)``.

    The carried-in guarantee in the first projected month - the unit face value the
    model point holds on the bond chassis, the sum assured plus attaching reversionary
    bonuses on the endowment - and the previous month's closing value after that.  A
    declaration is measured against the value its own month opens with, and the
    withdrawal is capped at it.
    """
    if t > proj_start():
        return guar_benefit_pp(t - 1)
    if is_unitised():
        return units_init() * unit_price_init()
    return sum_assured() + attaching_bonus()


def policy_value_pp(t):
    """The pre-MVR policy value at the end of month t: guarantee plus final bonus.

    What an MVR is measured against.
    """
    return guar_benefit_pp(t) + final_bonus_pp(t)


def policy_value_open(t):
    """The pre-MVR policy value month t **opens** with.

    The same guarantee-plus-final-bonus sum as :func:`policy_value_pp`, on the values
    the month opens with, and what a start-of-month withdrawal is taken pro rata to.
    """
    return guar_benefit_open(t) + max(
        0.0, smoothed_payout_open(t) - guar_benefit_open(t))


def bonus_supportable(t):
    """b_supp: the level bonus rate that fills the guarantee to the target **[std]**.

    Project the asset share to the horizon at the expected net return, take
    ``guar_fill_target`` of it, and solve for the level rate that grows the current
    guaranteed benefit to that amount::

        b_supp = [theta AS_proj / GB(t)]^(1/m) - 1

    with ``m`` the remaining endowment term in **years** - the term less the policy year
    the declaration closes, ``policy_term() - policy_year(t)`` - or the bond's
    bonus-setting horizon.  Future premiums are accumulated to the horizon at the same
    net return.  Everything in the rule is annual, because the rate it sets is: the grid
    is monthly but the discretion cycle is not.  Read only at a declaration month, and
    only when ``bonus_rule_on`` is set.
    """
    m = (bonus_horizon if is_unitised()                              # noqa: F821
         else max(1, policy_term() - policy_year(t)))
    r_e = fund_return() - amc_rate - guar_charge_rate(t)             # noqa: F821
    proj = asset_share_at(t, "BEF_PREM") * (1.0 + r_e) ** m
    p = premium_regular_pp()
    if p > 0.0:
        if abs(r_e) < 1e-12:
            proj += p * m
        else:
            proj += p * (1.0 + r_e) * ((1.0 + r_e) ** m - 1.0) / r_e
    gb = guar_benefit_open(t)
    if gb <= 0.0 or proj <= 0.0:
        return 0.0
    return (guar_fill_target * proj / gb) ** (1.0 / m) - 1.0         # noqa: F821


def bonus_rate(t):
    """b: the annual regular or reversionary bonus rate for the policy year holding t.

    A declared rate is a property of the **policy year**, not of the month, so every
    month of a year reads the rate set at that year's :func:`declaration_month`.  The
    base projection holds the model point's snapshot rate level, which is what the notes
    do.  With ``bonus_rule_on`` set, the smoothed setting rule applies once a year
    instead::

        b(y) = max(0, b(y-1) + clamp(kappa (b_supp - b(y-1)), -1%, +1%))

    The floor at zero is contractual - a declared bonus can be nil but never negative -
    and the plus or minus one percent is the gradual-change discipline firms state in
    their principles and practices, which is a discipline **per declaration** and would
    be a different rule applied twelve times a year.
    """
    if not bonus_rule_on:                                            # noqa: F821
        return bonus_rate_init()
    d = declaration_month(t)
    if t != d:
        return bonus_rate(d)
    if duration(t) <= duration(proj_start()):
        return bonus_rate_init()
    prev = bonus_rate(d - 12)
    step = bonus_speed * (bonus_supportable(d) - prev)               # noqa: F821
    step = max(-bonus_change_cap, min(bonus_change_cap, step))       # noqa: F821
    return max(0.0, prev + step)


def cost_of_bonus_pp(t):
    """CB(t): the cost of the bonus declared at the end of month t **[std]**.

    Zero in every month but a declaration month, because a cost arises only where a
    declaration does.  On the bond chassis it is the face-value uplift the declaration
    delivers, ``b FV`` on the face value the declaration month opened with.  On the
    endowment it is the declared addition to the guarantee discounted to the declaration
    date at the surrender-basis rate, over the ``policy_term() - policy_year(t)`` years
    still to run, since the addition is not payable until maturity; the survivorship
    discount is omitted **[std]**.
    """
    if not is_declaration_month(t):
        return 0.0
    if is_unitised():
        return bonus_rate(t) * guar_benefit_open(t)
    delta = guar_benefit_pp(t) - guar_benefit_open(t)
    years = max(0, policy_term() - policy_year(t))
    return delta / (1.0 + surr_disc_rate) ** years                   # noqa: F821


def shareholder_transfer_pp(t):
    """ST(t) = CB(t)/9: the 90:10 shareholder transfer, charged to the asset share.

    One ninth of the cost of bonus, so that shareholders receive a tenth of each
    distribution and policyholders nine tenths.  It is a real cash outflow from the fund
    and is reported as its own line, not netted into anything.  Like the cost it is
    taken from, it falls in the declaration month and is nil in the other eleven.
    """
    return cost_of_bonus_pp(t) / shareholder_transfer_divisor        # noqa: F821


def mort_rate(t):
    """q(x + duration(t)): the **annual** best-estimate mortality rate **[std]**.

    The shipped table rate times ``mort_be_factor``, entered at an attained age that
    advances on the policy anniversary, so the rate is level across a policy year.  Both
    are placeholders: CMI tables issued after March 2013 are subscriber-restricted, so
    the table is an ONS-shaped proxy and the factor a crude allowance for population
    mortality being heavier than insured experience.  :func:`mort_rate_mth` is what the
    projection decrements and charges by.
    """
    x = min(age(t), omega_age)                                       # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def mort_rate_mth(t):
    """q_m(t) = 1 - (1 - q)^(1/12): the monthly mortality rate **[std]**.

    Twelve months compound back to the table's annual rate exactly, so the in-force at
    each anniversary is what an annual-step roll-forward of the same table would give.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def death_guar_pp(t):
    """DB_g(t): the **guaranteed** death benefit, the mortality charge's sum-at-risk top.

    ``g_db x FV(t)`` on the bond chassis, where the death benefit carries a 101% uplift,
    and ``G(t)`` on the endowment.  Only the guaranteed element enters the sum at risk
    **[std]**: the final bonus is not guaranteed, so charging for it would charge the
    asset share for a benefit the fund has not promised.
    """
    if is_unitised():
        return death_benefit_factor * guar_benefit_pp(t)             # noqa: F821
    return guar_benefit_pp(t)


def mort_charge_pp(t):
    """MC(t): the mortality charge deducted from the asset share in month t.

    ``q_m x max(0, DB_g(t) - AS_after_ST)``: the **monthly** mortality rate times the
    sum at risk, measured on the balance **after** the shareholder transfer.  Differences
    between charged and actual mortality accrue to the estate, which is why this is a
    charge rather than a claim.  In the eleven months before a declaration the sum at
    risk is measured against the guarantee as it then stands; the declaration month's
    charge is the first to carry the hardened one.
    """
    return mort_rate_mth(t) * max(0.0, death_guar_pp(t)
                                  - asset_share_at(t, "AFT_ST"))


def smooth_cap_dn_mth():
    """The monthly floor factor of the smoothing cap: ``(1 - sigma)^(1/12)`` **[std]**.

    The notes' cap is a **year-on-year** discipline: a payout may not move more than
    ``sigma`` from one year to the next.  Twelve of these compound to exactly
    ``1 - sigma``, so the annual discipline survives the change of grid intact while the
    payout itself is recomputed every month.  Converting the cap instead to a flat
    ``sigma`` per month would loosen it twelvefold and stop it being the notes' rule.
    """
    return (1.0 - smooth_cap) ** (1.0 / 12.0)                        # noqa: F821


def smooth_cap_up_mth():
    """The monthly ceiling factor of the smoothing cap: ``(1 + sigma)^(1/12)`` **[std]**."""
    return (1.0 + smooth_cap) ** (1.0 / 12.0)                        # noqa: F821


def smoothed_payout_capped(t):
    """S_cap: the asset share after the month-on-month smoothing cap, before the corridor.

    ``clamp(AS(t), (1 - sigma)^(1/12) S(t-1), (1 + sigma)^(1/12) S(t-1))`` at
    ``sigma = 10%``.  This is what stops a market shock reaching payouts in one step,
    and it is applied **before** the corridor.  Twelve capped months compound to the
    notes' ``+/- 10%`` year-on-year band exactly, so a payout that is capped every month
    of a policy year has moved by exactly ``sigma`` over it - which is what the notes'
    down scenario does.

    The cap is **skipped where there is no previous payout** to compare against - the
    first month of a new-business cell, where the opening ``S`` is nil and the cap
    would otherwise clamp the payout to nil and leave the corridor to do all the work.
    See the Space docstring on what the cap can and cannot say about a premium-paying
    policy.
    """
    prev = smoothed_payout_open(t)
    if prev <= 0.0:
        return asset_share(t)
    lo = smooth_cap_dn_mth() * prev
    hi = smooth_cap_up_mth() * prev
    return max(lo, min(hi, asset_share(t)))


def smoothed_payout(t):
    """S(t): the smoothed target payout at the end of month t.

    The capped value, then clamped into the target corridor of 80% to 120% of the asset
    share.  The corridor is what stops the cap holding a payout indefinitely away from
    the asset share; the order - cap first, corridor second - is what produces the
    pattern the two rules are designed for.

    The regulatory target-range test is a *portfolio* property, a proportion of policies
    within the range, which a single-policy model cannot express; the deterministic
    corridor is a **[std]** reading of it.
    """
    if t < proj_start():
        return smoothed_payout_init()
    as_t = asset_share(t)
    lo = corridor_lo * as_t                                          # noqa: F821
    hi = corridor_hi * as_t                                          # noqa: F821
    return max(lo, min(hi, smoothed_payout_capped(t)))


def smoothed_payout_open(t):
    """S(t-1): the smoothed payout month t **opens** with.

    The carried-in benchmark in the first projected month - nil on a new-business
    cell, which is what switches the cap off there - and the previous month's closing
    payout after that.
    """
    if t > proj_start():
        return smoothed_payout(t - 1)
    return smoothed_payout_init()


def final_bonus_pp(t):
    """FB(t) or TB(t): the final or terminal bonus, ``max(0, S(t) - GB(t))``.

    The non-guaranteed top-up from the guaranteed benefit to the smoothed payout, and
    the form the discretion keeps a substantial proportion of the payout in - precisely
    because it is the part that has not hardened.
    """
    return max(0.0, smoothed_payout(t) - guar_benefit_pp(t))


def mvr_pp(t):
    """MVR(t): the market value reduction **scale** at the end of month t.

    ``min(max(0, FV - S), max(0, FV - AS))``.  The first argument recovers the shortfall
    of the smoothed payout below the unit face value; the second is the contractual
    bound - the reduction may not exceed the excess of the unit value over the
    underlying asset value.

    This is the scale, not what an exit bears: :func:`mvr_applied_pp` is zero where the
    exit is MVR-free.  Both are needed, because the behavioural deterrent keys off the
    scale being positive while the payout keys off what is applied.

    **Unitised chassis only.**  A market value reduction is a unit-linked-style
    adjustment to a *unit* value, and the notes define it for the unitised chassis
    alone; a conventional endowment has no units to reduce, and its surrender value is
    set on a surrender basis instead - see :func:`claim_pp`.  Returning zero here rather
    than applying the same arithmetic keeps the result table honest: on a conventional
    policy the face value is a maturity guarantee decades away, so ``FV - S`` is a large
    number that means nothing.
    """
    if not is_unitised():
        return 0.0
    gb = guar_benefit_pp(t)
    return min(max(0.0, gb - smoothed_payout(t)),
               max(0.0, gb - asset_share(t)))


def mvr_applied_pp(t):
    """The market value reduction an exit at the end of month t actually bears.

    Zero in a guarantee-date **month**, where the contract promises the full guaranteed
    benefit without reduction, and zero on death.  In the other eleven months of a
    guarantee year the window is shut and the reduction applies in full: the monthly
    grid can say when the option is open, where an annual one could only treat the whole
    year as the date.  The death case is handled in :func:`claim_pp` rather than here,
    because only the surrender payout reads this.  Zero throughout on the endowment
    chassis, which has no units to reduce.
    """
    if is_guarantee_date(t):
        return 0.0
    return mvr_pp(t)


def claim_pp(t, kind):
    """The payout per claim at the end of month t, by kind.

    ``"DEATH"``
        ``g_db (FV + FB)`` on the bond chassis - the 101% uplift applies to
        the whole payout - and ``G + TB`` on the endowment.  **Never
        MVR'd**: an MVR is not applied on death on either chassis.

    ``"SURRENDER"``
        ``FV + FB - MVR_applied`` on the bond chassis, the non-guaranteed
        exit.  On the endowment chassis there is no MVR, and the surrender
        value targets the smoothed payout - the asset share under the
        smoothing discipline - capped at the prospective value ``G + TB``,
        which is what the policy would be worth if it ran to maturity.
        Early surrender values are therefore well below the guaranteed
        maturity benefit, as they are on a real conventional policy.

    ``"GUARANTEE"``
        ``GB + FB``, what a guarantee-date exit pays.  Computed at every
        ``t`` so the two can be compared, but paid only in a month where
        :func:`is_guarantee_date` - in those months it equals the
        surrender payout, because the MVR is not applied.  The endowment
        chassis has no guarantee dates, so this is informational there.

    ``"MATURITY"``
        ``G + TB`` at the end of the endowment term, the last projected
        month ``proj_len() - 1``.  On the bond chassis, which is whole of
        life, this is zero unless the projection ends in a **forced
        encashment** - the withdrawal election has cancelled the last unit
        - in which case the survivors are paid ``FV + FB``, the residual
        final bonus included.  A limiting-age ending pays nothing, because
        it is a modelling truncation rather than a contractual event.
    """
    base = guar_benefit_pp(t) + final_bonus_pp(t)
    if kind == "DEATH":
        return death_benefit_factor * base if is_unitised() else base  # noqa: F821
    if kind == "SURRENDER":
        if not is_unitised():
            return max(0.0, min(smoothed_payout(t), base))
        return base - mvr_applied_pp(t)
    if kind == "GUARANTEE":
        return base
    if kind == "MATURITY":
        if t != proj_len() - 1:
            return 0.0
        if is_unitised() and not is_forced_encashment():
            return 0.0
        return base
    raise ValueError("invalid kind")


def smoothing_cost_pp(t, kind):
    """The excess of a payout over the asset share, borne by the estate.

    Positive where the smoothing or a guarantee has paid more than the policy earned,
    negative where it has paid less.  Intended broadly neutral over time; the base model
    accumulates the balance in :func:`smoothing_account` without recycling it.
    """
    return claim_pp(t, kind) - asset_share(t)


def surr_rate_base(t):
    """The table **annual** surrender rate applying in month t **[std]**.

    Read from the chassis's own row of the lapse table, whose key is the **contractual
    policy year** - a 1-based label, so month t reads row ``policy_year(t)``; policy
    years beyond the table take its last row.  A drafting construction: no public UK
    with-profits lapse experience was retrieved.
    """
    tbl = data.lapse_table().loc[chassis()]                          # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def mvr_deterrent(t):
    """0.6 while an MVR would be applied, 1 otherwise **[std]**.

    An active market value reduction penalizes exit, and firms may consider exit volumes
    when setting reductions inside the contractual bound.
    """
    return mvr_deterrent_factor if mvr_applied_pp(t) > 0.0 else 1.0  # noqa: F821


def guarantee_exercise(t):
    """The one-off MVR-free encashment taken in a guarantee-date month **[std]**.

    ``guarantee_exercise_rate`` of the survivors of that month, and only **when the
    guarantee is in the money** (``GB > AS``); zero everywhere else.  The gate matters:
    MVR-free encashment is worth exercising precisely when the guaranteed benefit
    exceeds the asset share and worth nothing otherwise, so exercising unconditionally
    would invent anti-selection where there is none.  This is the dominant behavioural
    risk on with-profits business.

    This is where the monthly grid changes the *shape* of an assumption rather than only
    its frequency, and deliberately.  The annual grid could only express the exercise as
    a 2.5x multiplier on the whole guarantee-date **year**'s surrender rate, which
    spreads MVR-free exits across eleven months in which the window is shut.  Here the
    exercise falls in the month the option is actually open, at a rate **[std]** set so
    that a guarantee-date year still sheds about the same proportion of lives as the
    annual grid's spike did.  Neither number is measured: no public UK with-profits
    experience was retrieved, and the whole construction is rationalized from the
    incentive structure.
    """
    if is_guarantee_date(t) and guar_benefit_pp(t) > asset_share(t):
        return guarantee_exercise_rate                               # noqa: F821
    return 0.0


def guarantee_imminent(t):
    """0.8 in the twelve months before a guarantee date **[std]**: policyholders wait.

    The run-up, not the calendar year: any month from which the next guarantee date is
    between one and twelve months away.  On the annual grid this was the single period
    before a guarantee-date period, which is the same window counted in years.
    """
    if any(0 < 12 * g - 1 - t <= 12 for g in guarantee_years()):
        return guarantee_imminent_factor                             # noqa: F821
    return 1.0


def surr_rate(t):
    """w(t): the **annual** ordinary surrender rate applying in month t.

    The table rate times the two diffuse behavioural multipliers - the MVR deterrent and
    the guarantee-imminent suppression - capped at 1.  The guarantee-date exercise is
    *not* in here: it is a dated one-off rather than a rate per year, and it enters
    through :func:`surr_rate_mth`.
    """
    return min(1.0, surr_rate_base(t) * mvr_deterrent(t)
               * guarantee_imminent(t))


def surr_rate_mth(t):
    """w_m(t): the monthly surrender rate, exercise included.

    ``1 - (1 - w_ord_m)(1 - exercise)`` where ``w_ord_m = 1 - (1 - w(t))^(1/12)``: the
    ordinary monthly rate, and then in a guarantee-date month the MVR-free encashment
    taken by whoever is left after it.  Twelve ordinary months compound back to the
    annual table rate exactly; the exercise is over and above that, and falls in one
    month a decade.
    """
    ordinary = 1.0 - (1.0 - surr_rate(t)) ** (1.0 / 12.0)
    return min(1.0, 1.0 - (1.0 - ordinary) * (1.0 - guarantee_exercise(t)))


def pols_if(t):
    """l(t): the number of policies in force at the **start** of month t.

    ``pols_if(proj_start()) == pols_if_init()``, and it is the weight on every flow of
    that same ``result_cf()`` row.  Zero outside the frame.
    """
    if t < proj_start() or t >= proj_len():
        return 0.0
    if t == proj_start():
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement; :func:`pols_if`.

    ``"BEF_SURR"``
        after deaths, before surrenders - the processing order is death
        before surrender **[std]**.

    ``"AFT_DECR"``
        the end-of-month count, and zero in the last projected month
        ``proj_len() - 1``, where the endowment matures and the bond
        projection is truncated.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_SURR":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        if t < proj_start() or t >= proj_len() - 1:
            return 0.0
        return pols_if_at(t, "BEF_SURR") * (1.0 - surr_rate_mth(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in month t, against the in force at its start."""
    return pols_if(t) * mort_rate_mth(t)


def pols_surr(t):
    """Surrenders at the end of month t, from the survivors of mortality.

    Carries the guarantee-date encashment as well as the ordinary rate, so the exits of
    a guarantee-date month are visibly larger than its neighbours' - which is the point
    of dating the exercise rather than spreading it.
    """
    return pols_if_at(t, "BEF_SURR") * surr_rate_mth(t)


def pols_maturity(t):
    """Survivors at the end of the projection: maturities, or the bond's truncation.

    On the endowment chassis these are genuine maturities and are paid.  On the bond
    chassis they are paid where the projection ends in a forced encashment and pay
    nothing where it ends at the limiting age - see :func:`is_forced_encashment`.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_if(t) - pols_death(t) - pols_surr(t)


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^duration(t)`` **[std]**.

    Steps on the policy anniversary rather than monthly: the expense assumption is
    quoted per year and inflates per year.  One through the first policy year.
    """
    return (1.0 + inflation_rate) ** duration(t)                     # noqa: F821


def premiums(t):
    """Premium income at the start of month t, an inflow."""
    return premium_pp(t) * pols_if(t)


def withdrawals(t):
    """Partial withdrawals paid at the start of month t.

    An owner election rather than a claim, which is why it has its own name and column.
    """
    return wd_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"DEATH"``, ``"SURRENDER"`` and ``"MATURITY"`` weight :func:`claim_pp` by the
    corresponding decrement.  ``"GUARANTEE"`` is not a separate outgo: a guarantee-date
    exit *is* a surrender, paid MVR-free, so it is already inside the surrender line.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "SURRENDER", "MATURITY"))
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    if kind == "SURRENDER":
        return claim_pp(t, "SURRENDER") * pols_surr(t)
    if kind == "MATURITY":
        return claim_pp(t, "MATURITY") * pols_maturity(t)
    raise ValueError("invalid kind")


def expenses(t):
    """E(t): the maintenance expense in month t **[std]**.

    £30 a policy a year - a twelfth of it each month - inflating at 3% on each
    anniversary.  Where a fund's actual expenses exceed the capped charge taken from
    asset shares, the excess falls to the estate - a fund-level flow a single-policy
    model cannot see.
    """
    return (expense_maint / 12.0                                     # noqa: F821
            * inflation_factor(t) * pols_if(t))


def shareholder_transfers(t):
    """The 90:10 shareholder transfer paid out of the fund in month t.

    The transfer on the month's declared bonus - nil except in a declaration month -
    weighted by the in force, plus a ninth of the final bonus actually paid on the
    month's claims, which arises whenever a claim does.  The same 90:10 split applied at
    the point the non-guaranteed part is handed over.
    """
    on_declaration = shareholder_transfer_pp(t) * pols_if(t)
    exits = pols_death(t) + pols_surr(t) + pols_maturity(t)
    on_final_bonus = (final_bonus_pp(t) * exits
                      / shareholder_transfer_divisor)                # noqa: F821
    return on_declaration + on_final_bonus


def smoothing_cost(t):
    """The estate's smoothing and guarantee cost on the month's exits.

    Each exiting policy is paid its smoothed payout while the asset share it earned is
    released; the difference falls on the estate.  Positive in a month when guarantees
    or smoothing pay more than the policies earned - which on a guarantee-date month is
    both the largest exit and the deepest shortfall at once.
    """
    return (smoothing_cost_pp(t, "DEATH") * pols_death(t)
            + smoothing_cost_pp(t, "SURRENDER") * pols_surr(t)
            + smoothing_cost_pp(t, "MATURITY") * pols_maturity(t))


def smoothing_account(t):
    """SM(t): the cumulative smoothing and guarantee cost borne by the estate.

    Intended broadly neutral over time.  The base model tracks the balance without
    recycling it into credited returns; one insurer operates that recycling, feeding it
    back subject to a maximum annual deduction from asset shares [S5].

    The balance opens at zero in the first projected month rather than reading a row
    below the frame.
    """
    if t < proj_start():
        return 0.0
    prev = smoothing_account(t - 1) if t > proj_start() else 0.0
    return prev + smoothing_cost(t)


def net_cf(t):
    """The net cash flow of month t, **income positive**.

    Premiums less claims, withdrawals, expenses and shareholder transfers.  The asset
    share appears nowhere in it: it is a state variable, not a cash flow, and the
    payouts it drives are already in ``claims``.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - shareholder_transfers(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere."""
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_surr(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month."""
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(proj_start(), proj_len()))


def check_asset_share_roll_fwd_resid(t):
    """The asset share recursion residual in month t; zero everywhere.

    ``AS(t) - max(0, {[AS(t-1) + P - W_AS](1 + r_m)(1 - c_amc_m - c_g_m) - ST - MC
    + M})``, rebuilt in one expression rather than through :func:`asset_share_at`, so
    that a mis-ordered step - a shareholder transfer taken before the charges, say, or a
    mortality charge measured on the wrong balance - shows up here.  Every rate in it is
    the monthly equivalent, which is the other thing the check pins down: a stray annual
    rate left in the recursion would fail here rather than quietly overcharging the
    asset share twelvefold.  The outer ``max(0, ...)`` is the zero floor
    :func:`asset_share` applies; the check still validates the ordering in every month
    the floor is not binding, which is every month of every cell shipped here except the
    tail of the sustained down scenario.
    """
    built = ((asset_share_at(t, "BEF_PREM") + premium_pp(t) - wd_as_pp(t))
             * (1.0 + fund_return_mth())
             * (1.0 - amc_rate_mth() - guar_charge_rate_mth(t))
             - shareholder_transfer_pp(t) - mort_charge_pp(t)
             + misc_surplus_pp(t))
    return asset_share(t) - max(0.0, built)


def check_asset_share_roll_fwd():
    """True when the asset share recursion closes in every projected month."""
    return all(abs(check_asset_share_roll_fwd_resid(t)) <= 1e-8
               for t in range(proj_start(), proj_len()))


def check_fb_mvr_exclusive():
    """True when no month carries both a final bonus and a market value reduction.

    ``FB > 0`` requires ``S > GB`` and ``MVR > 0`` requires ``S < GB``, so the two
    cannot both be positive.  An implementation that computed them independently could
    produce both, and would then pay a final bonus and deduct a reduction on the same
    exit.
    """
    return all(min(final_bonus_pp(t), mvr_pp(t)) <= 1e-9
               for t in range(proj_start(), proj_len()))


def check_mvr_bound():
    """True when the market value reduction stays inside its contractual bound.

    It may not exceed the excess of the unit value over the underlying asset value,
    ``max(0, GB - AS)``.  The bound is a conduct rule, not a modelling nicety.
    """
    return all(mvr_pp(t) <= max(0.0, guar_benefit_pp(t) - asset_share(t)) + 1e-9
               for t in range(proj_start(), proj_len()))


def check_fund_nonneg():
    """True when the unit holding and the asset share stay non-negative throughout.

    This is the way a with-profits projection goes wrong quietly.  A level withdrawal
    election runs the unit fund down; uncapped, the unit holding turns negative and the
    guaranteed benefit turns negative with it, and every downstream number - the bonus
    cost, the mortality charge's sum at risk, the smoothed payout - stays plausible
    enough to read past.  :func:`wd_pp` caps the withdrawal at the fund and
    :func:`proj_len` stops at exhaustion; this asserts that they worked.
    """
    return all(units(t) >= -1e-9 and asset_share(t) >= -1e-9
               for t in range(proj_start(), proj_len()))


def check_payout_corridor():
    """True when the smoothed payout stays inside the 80-120% target corridor.

    Deterministic at model-point level; the regulatory test is a portfolio property that
    a single-policy model cannot express.
    """
    for t in range(proj_start(), proj_len()):
        as_t = asset_share(t)
        if as_t <= 0.0:
            continue
        ratio = smoothed_payout(t) / as_t
        if ratio < corridor_lo - 1e-9 or ratio > corridor_hi + 1e-9:  # noqa: F821
            return False
    return True


def check_declaration_is_annual():
    """True when the declared bonus moves the guarantee only in declaration months.

    The grid is monthly and the discretion cycle is not: a declaration hardens the
    guarantee once a policy year, at its anniversary, and nothing declares in the other
    eleven months.  The failure this guards against is compounding the *annual* bonus
    rate twelve times a year, which produces a model that still runs, whose roll-forwards
    still close, and whose guarantee is an order of magnitude too large a decade later.

    What is asserted is the quantity a declaration actually moves.  On the bond chassis
    that is the **unit price**, not the face value: a withdrawal cancels units every
    month, so the face value falls between declarations for a reason that has nothing to
    do with discretion.  On the endowment chassis, which holds no units, it is the
    guaranteed benefit itself.  Either way the cost of bonus and the shareholder transfer
    it feeds must be nil outside a declaration month.

    Tolerances are relative to the quantity, since these are money amounts and a price
    rather than probabilities.
    """
    for t in range(proj_start(), proj_len()):
        if is_declaration_month(t):
            continue
        if is_unitised():
            opening = unit_price(t - 1) if t > proj_start() else unit_price_init()
            moved = unit_price(t)
        else:
            opening = guar_benefit_open(t)
            moved = guar_benefit_pp(t)
        if abs(moved - opening) > 1e-9 * max(abs(opening), 1.0):
            return False
        if cost_of_bonus_pp(t) != 0.0 or shareholder_transfer_pp(t) != 0.0:
            return False
    return True


def result_cf():
    """Result table of cashflows, indexed by the 0-based month t.

    The frame is ``range(proj_start(), proj_len())``, so the first row is the first
    projected month and the last is ``proj_len() - 1``.

    ``pols_if`` is the start-of-month count that weights every flow on the row.  The
    asset share is published beside them as ``asset_share`` because it is what the
    payouts are measured against - but it is a state variable, not a cash flow, and it
    is not part of ``net_cf``.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "asset_share": [asset_share(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_surrender": [claims(t, "SURRENDER") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "shareholder_transfers": [shareholder_transfers(t) for t in ts],
            "smoothing_cost": [smoothing_cost(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_payout():
    """Result table of the payout machinery, indexed by the 0-based month t.

    The asset share against the guaranteed benefit and the smoothed payout, and the
    final bonus and market value reduction the gap between them produces.  Every column
    is an end-of-month value, on the same frame as :func:`result_cf`.  ``bonus_rate`` is
    the **annual** rate declared for the policy year the month falls in, so it repeats
    across twelve rows and steps once a year; ``cost_of_bonus_pp`` and
    ``shareholder_transfer_pp`` beside it are nil in eleven of those twelve.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "asset_share": [asset_share(t) for t in ts],
            "guar_benefit_pp": [guar_benefit_pp(t) for t in ts],
            "smoothed_payout": [smoothed_payout(t) for t in ts],
            "final_bonus_pp": [final_bonus_pp(t) for t in ts],
            "mvr_pp": [mvr_pp(t) for t in ts],
            "mvr_applied_pp": [mvr_applied_pp(t) for t in ts],
            "claim_death": [claim_pp(t, "DEATH") for t in ts],
            "claim_surrender": [claim_pp(t, "SURRENDER") for t in ts],
            "claim_guarantee": [claim_pp(t, "GUARANTEE") for t in ts],
            "bonus_rate": [bonus_rate(t) for t in ts],
            "cost_of_bonus_pp": [cost_of_bonus_pp(t) for t in ts],
            "shareholder_transfer_pp": [shareholder_transfer_pp(t) for t in ts],
            "mort_charge_pp": [mort_charge_pp(t) for t in ts],
            "smoothing_account": [smoothing_account(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_be_factor = 0.6

amc_rate = 0.01

guar_charge_rate_base = 0.001

guar_charge_cap = 0.02

misc_surplus_rate = 0.0

prem_alloc_rate = 1.0

death_benefit_factor = 1.01

shareholder_transfer_divisor = 9.0

surr_disc_rate = 0.04

smooth_cap = 0.1

corridor_lo = 0.8

corridor_hi = 1.2

bonus_rule_on = False

guar_fill_target = 0.8

bonus_speed = 0.5

bonus_change_cap = 0.01

bonus_horizon = 10

mvr_deterrent_factor = 0.6

guarantee_exercise_rate = 0.075

guarantee_imminent_factor = 0.8

expense_maint = 30.0

inflation_rate = 0.03

pd = ("Module", "pandas")