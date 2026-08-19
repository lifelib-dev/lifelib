# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WP_UK_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's scenario A
    >>> Projection.point_id = 2            # scenario B, the down market

``t`` counts **policy years** from issue, 1-based, so an in-force model point at
duration 5 starts at ``t = proj_start() = 6`` — which is the year the notes' worked
example projects. State carried into that year (the asset share, the smoothed payout,
the unit price) is indexed at ``proj_start() - 1``.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/with_profits/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WP_UK_A`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.WP_UK_A.Data`,
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
t                          (the cells argument)            Policy year
x                          age_at_entry()                  Entry age (ANB)
x + t - 1                  age(t)                          Attained age (ANB)
duration_ifo               duration_inforce()              Completed years at valuation
(none)                     proj_start()                    First projected policy year
n                          policy_term()                   Endowment term
(none)                     proj_len()                      Last projected policy year
(none)                     fund_exhaust_year()             Year the bond's units run out
(none)                     is_forced_encashment()          Whether the run ends there
P(t)                       premium_pp(t)                   Premium received at BOY
W(t)                       wd_pp(t)                        Partial withdrawal at BOY
W_AS(t)                    wd_as_pp(t)                     Asset-share reduction for it
r(t)                       fund_return()                   Earned fund return
c_amc                      amc_rate                        Annual management charge
c_g                        guar_charge_rate(t)             Guarantee/smoothing charge
CumGC(t)                   guar_charge_cum_pp(t)           Cumulative guarantee charge
AS(t)                      asset_share(t)                  Asset share at end of year t
(the steps)                asset_share_at(t, timing)       The asset share inside year t
M(t)                       misc_surplus_pp(t)              Estate distributions; 0 in base
Q(t)                       unit_price(t)                   With-profits unit price
U(t)                       units(t)                        Units held
FV(t), G(t)                guar_benefit_pp(t)              Guaranteed benefit
(pre-MVR value)            policy_value_pp(t)              Guaranteed benefit + final bonus
b(t), b_rev(t)             bonus_rate(t)                   Declared bonus rate
b_supp                     bonus_supportable(t)            Rate the guarantee-fill implies
theta, kappa               guar_fill_target, bonus_speed   Bonus-rule parameters
CB(t)                      cost_of_bonus_pp(t)             Cost of the declared bonus
ST(t)                      shareholder_transfer_pp(t)      CB/9, the 90:10 transfer
MC(t)                      mort_charge_pp(t)               Mortality charge to the AS
DB_g(t)                    death_guar_pp(t)                Guaranteed death benefit
q(x+t-1)                   mort_rate(t)                    Mortality rate
w(t)                       surr_rate(t)                    Surrender rate, all multipliers
(table)                    surr_rate_base(t)               Table surrender rate
sigma                      smooth_cap                      Year-on-year smoothing cap
S(t)                       smoothed_payout(t)              Smoothed target payout
(cap step)                 smoothed_payout_capped(t)       After the cap, before the corridor
FB(t), TB(t)               final_bonus_pp(t)               Final or terminal bonus
MVR(t)                     mvr_pp(t)                       Market value reduction, unapplied
(applied)                  mvr_applied_pp(t)               Zero where the exit is MVR-free
(guarantee dates)          is_guarantee_date(t)            MVR-free anniversary
g_db                       death_benefit_factor            Bond death uplift, 1.01
i_sv, v_sv                 surr_disc_rate                  Endowment surrender discount
l(t)                       pols_if(t)                      In force at the start of year t
(none)                     pols_if_at(t, timing)           BEF_DECR / BEF_SURR / AFT_DECR
(none)                     pols_death(t)                   Deaths in year t
(none)                     pols_surr(t)                    Surrenders at the end of year t
(none)                     pols_maturity(t)                Maturities, or the truncation
(payouts)                  claim_pp(t, kind)               Payout per claim by kind
SM(t)                      smoothing_account(t)            Cumulative smoothing cost
(cash flows)               premiums, claims, withdrawals   Probability-weighted flows
E(t)                       expenses(t)                     Maintenance expense
ST x l                     shareholder_transfers(t)        Transfer outgo
(none)                     net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ==========================

Four names needed care.

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

There is **no** ``av_pp_at`` in this model, and that is a product statement rather than
an omission. The asset share is a *shadow* retrospective accumulation that the
policyholder never owns and is never paid; the guaranteed benefit is not a fund either.
Naming either of them the library's account value would assert something false about
the contract.

.. rubric:: The asset share is a state variable, not a cash flow

::

    AS(t) = [AS(t-1) + P(t) - W_AS(t)] (1 + r(t)) (1 - c_amc - c_g) - ST(t) - MC(t) + M(t)

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
therefore never falls — ``b(t) >= 0`` is a contractual floor, not a modelling choice —
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
    S_cap = clamp(S_raw, (1-sigma) S(t-1), (1+sigma) S(t-1))
    S(t)  = clamp(S_cap, 0.80 AS(t), 1.20 AS(t))

The year-on-year cap is applied **first** and the target corridor **second**, and the
order matters: the cap is what stops a market shock reaching payouts in one step, and
the corridor is what stops the cap holding a payout indefinitely away from the asset
share. In the notes' down scenario the cap binds at ``-10%`` and the corridor then does
not, which is exactly the pattern the two rules are designed to produce.

The corridor implements the 80-120% target range at model-point level. The regulatory
test is a *portfolio* property — a proportion of policies within the range — and a
single-policy model cannot express it, so the deterministic corridor is a **[std]**
reading of it.

Two things the cap cannot say. It is skipped in the first projected year of a
new-business cell, where ``S(t-1) = 0`` would clamp the payout to nil. And on a
**premium-paying** policy it is only loosely meaningful: a firm's ±10% discipline is a
*like-for-like* comparison between successive maturity cohorts — this year's payout on a
25-year endowment against last year's — not a comparison of one policy's own payout
across its own durations. A regular-premium asset share grows far faster than 10% a year
in early durations because premiums, not investment return, dominate it, so the cap
binds throughout and the corridor floor is what actually sets the payout. On the
endowment cell shipped here that persists to about duration 14, after which the asset
share is large enough that the cap stops binding and the payout converges to it: 80% of
the asset share at duration 1, 100.0% at maturity. The single-premium bond the worked
example uses has no such problem, which is why the notes can state the cap plainly.

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

Three multipliers sit on the base surrender rate, all **[std]** and all rationalized
from the incentive structure rather than measured:

- an **MVR deterrent** of 0.6 while an MVR would be applied — an active MVR penalizes
  exit;
- a **guarantee-date spike** of 2.5 in a guarantee-date year, applied **only when the
  guarantee is in the money** (``GB > AS``), because MVR-free encashment is worth
  exercising precisely then and worth nothing otherwise; and
- a **guarantee-imminent suppression** of 0.8 in the year before a guarantee date,
  policyholders waiting for the MVR-free window.

The second is the one that matters. Anti-selective exit when guarantees are in the money
is the dominant behavioural risk on with-profits business, and dynamic assumptions of
this kind are a regulatory expectation for the best estimate rather than an optional
refinement.

The MVR deterrent applies on the bond chassis only, because there is no MVR on the other
one. That falls out of :func:`mvr_applied_pp` rather than being coded as a special case.

.. rubric:: A withdrawal election is not unconditional

The MVR-free allowance is 5% of the original premium a year, and the withdrawing cell
takes the whole of it every year. Against a fund whose growth is only the declared
bonus, that exhausts the fund: the shipped cell cancels its last unit in policy year 34.
:func:`wd_pp` therefore caps the withdrawal at the unit fund it comes out of, and
:func:`proj_len` stops the projection the year before exhaustion, where
:func:`is_forced_encashment` marks the ending as a real contractual event and the
survivors are paid ``FV + FB`` rather than nothing. :func:`check_fund_nonneg` asserts the
result, because the failure mode here is silent: an uncapped election turns the unit
holding negative and every number downstream of it stays plausible enough to read past.

.. rubric:: What is out of scope, and why

The **smoothed-fund (PruFund-style) chassis** is not implemented. Its mechanics are
daily and quarterly — a 5% daily and 10% quarterly smoothing limit with a 2.5% gap
trigger — and an annual grid smooths away the very limits that define the design.
Implementing it here would produce something that ran and meant nothing, so
:func:`chassis` accepts the two chassis the annual grid can carry and says so.

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
    are daily and quarterly, and an annual grid smooths away the very mechanics that
    define it.  See the Space docstring.
    """
    v = model_point()["chassis"]
    if v not in ("UWP_bond", "CWP_endowment"):
        raise ValueError("invalid chassis; SF_prufund is out of scope on an annual grid")
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
    """Completed policy years at the valuation date; 0 on a new-business cell.

    The worked example is an in-force bond at duration 5, so its projection starts in
    policy year 6 and the state it carries in is indexed at year 5.
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
    """The first projected policy year: ``duration_inforce() + 1``."""
    return duration_inforce() + 1


def fund_exhaust_year():
    """The first projected year in which the bond's unit fund is exhausted; 0 if never.

    A level withdrawal election runs the unit holding down, and against a fund whose
    growth is only the declared bonus it eventually cancels the last unit.  This locates
    that year so :func:`proj_len` can stop there.  Zero on the endowment chassis and on
    any bond cell taking no withdrawals, which is the ordinary case.
    """
    if not is_unitised() or wd_rate() <= 0.0:
        return 0
    for t in range(proj_start(), omega_age - age_at_entry() + 1):    # noqa: F821
        if units(t) <= 1e-9:
            return t
    return 0


def proj_len():
    """The last projected policy year.

    The endowment's term, or the whole-of-life bond's limiting age - cut short where a
    withdrawal election has exhausted the unit fund, since a bond with no units is not a
    bond.
    """
    if not is_unitised():
        return policy_term()
    horizon = omega_age - age_at_entry()                             # noqa: F821
    exhaust = fund_exhaust_year()
    if exhaust:
        return min(horizon, exhaust - 1)
    return horizon


def is_forced_encashment():
    """Whether the bond's projection ends because the unit fund has been exhausted.

    It changes what the survivors at the end of the projection are paid.  A fund-
    exhaustion ending is a **real contractual event** - the last units are cancelled and
    the bond is encashed - so the survivors are paid out.  A limiting-age ending is a
    modelling truncation, and paying anything there would invent a claim.
    """
    return (is_unitised() and fund_exhaust_year() > 0
            and proj_len() == fund_exhaust_year() - 1)


def age(t):
    """The attained age (ANB) in policy year t: ``x + t - 1``."""
    return age_at_entry() + t - 1


def is_guarantee_date(t):
    """Whether policy year t ends on a contractual guarantee date.

    An exit there is MVR-free and pays the full guaranteed benefit plus final bonus,
    which is the option the guarantee-date surrender spike is exercising.
    """
    return t in guarantee_years()


def premium_pp(t):
    """P(t): the premium received at the start of policy year t.

    The regular premium on the endowment chassis, plus the single premium in policy year
    1 - which an in-force cell never reaches, so it is not double counted.
    """
    p = premium_regular_pp()
    if t == 1:
        p += premium_single_pp()
    return p


def wd_pp(t):
    """W(t): the partial withdrawal paid at the start of policy year t.

    Taken as a fraction of the **original** premium, which is how the MVR-free allowance
    is expressed, and zero in the base run.  Within the allowance it is MVR-free.

    Capped at the unit fund it is cancelled out of, ``FV(t-1)``.  The cap is a physical
    constraint rather than a product rule: a level withdrawal against a fund that is
    being run down eventually exhausts it, and an uncapped election drives the unit
    holding - and with it the guaranteed benefit - negative.  Note what the cap is
    measured against: the *unit* fund, not the pre-MVR policy value, because a partial
    withdrawal cancels units and the final bonus is only paid on full encashment.  The
    residual final bonus reaches the policyholder in the encashment that
    :func:`is_forced_encashment` marks.
    """
    w = wd_rate() * premium_single_pp()
    if w <= 0.0:
        return 0.0
    return min(w, max(0.0, guar_benefit_pp(t - 1)))


def wd_as_pp(t):
    """W_AS(t): the asset-share reduction for the year's withdrawal.

    Pro rata to the **pre-MVR policy value**, so a withdrawal takes the same proportion
    of the asset share as it takes of what the policy is worth - not the same cash
    amount.  Zero where nothing is withdrawn or the policy value is nil.
    """
    w = wd_pp(t)
    if w <= 0.0:
        return 0.0
    pv = policy_value_pp(t - 1)
    if pv <= 0.0:
        return 0.0
    return asset_share(t - 1) * w / pv


def guar_charge_rate(t):
    """c_g: the guarantee and smoothing charge on the asset share in year t **[std]**.

    0.10% a year, and it **stops** once cumulative deductions reach the lifetime cap of
    2% of the asset share.  The cap test is measured on the previous year's asset share
    rather than the year's own, which is what keeps the charge from depending on the
    balance it is being deducted from.

    Note what the cap is a fraction *of*.  The notes set it against the **current** asset
    share, not against a level struck once at first breach, so on a fund that keeps
    growing the threshold grows with it: the charge stops the year the cumulative
    overtakes it and resumes the year after, when the larger asset share has moved the
    threshold back above.  That is the rule as written; a cap frozen at first breach
    would be a different rule and a materially different charge.
    """
    prev_as = asset_share(t - 1)
    if prev_as > 0.0 and guar_charge_cum_pp(t - 1) >= guar_charge_cap * prev_as:  # noqa: F821
        return 0.0
    return guar_charge_rate_base                                     # noqa: F821


def guar_charge_pp(t):
    """The guarantee and smoothing charge actually deducted in year t."""
    return guar_charge_rate(t) * asset_share_at(t, "AFT_RETURN")


def guar_charge_cum_pp(t):
    """CumGC(t): cumulative guarantee and smoothing deductions to the end of year t."""
    if t < proj_start():
        return 0.0
    return guar_charge_cum_pp(t - 1) + guar_charge_pp(t)


def misc_surplus_pp(t):
    """M(t): estate distributions credited to the asset share; zero in the base run.

    Miscellaneous surplus and estate distributions are allocated annually where a firm
    operates them; the base model allocates none.
    """
    return misc_surplus_rate * asset_share(t - 1)                    # noqa: F821


def asset_share_at(t, timing):
    """The asset share at a point inside policy year t.

    ``"BEF_RETURN"``
        ``AS(t-1) + P(t) - W_AS(t)``, after the start-of-year premium and
        withdrawal.

    ``"AFT_RETURN"``
        after the year's fund return.

    ``"AFT_CHARGE"``
        after the annual management charge and the guarantee charge.

    ``"AFT_ST"``
        after the shareholder transfer, which is charged to asset shares.
        **This is the balance the mortality charge's sum at risk is
        measured against.**

    ``"AFT_MC"``
        after the mortality charge and any estate distribution; the
        year-end asset share, and the same number as :func:`asset_share`.

    The steps are exposed individually because their order is contractual discipline
    rather than arithmetic convenience.
    """
    if timing == "BEF_RETURN":
        return asset_share(t - 1) + premium_pp(t) - wd_as_pp(t)
    if timing == "AFT_RETURN":
        return asset_share_at(t, "BEF_RETURN") * (1.0 + fund_return())
    if timing == "AFT_CHARGE":
        return (asset_share_at(t, "AFT_RETURN")
                * (1.0 - amc_rate - guar_charge_rate(t)))            # noqa: F821
    if timing == "AFT_ST":
        return asset_share_at(t, "AFT_CHARGE") - shareholder_transfer_pp(t)
    if timing == "AFT_MC":
        return (asset_share_at(t, "AFT_ST") - mort_charge_pp(t)
                + misc_surplus_pp(t))
    raise ValueError("invalid timing")


def asset_share(t):
    """AS(t): the asset share at the end of policy year t.

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
    """
    if t < proj_start() - 1:
        return 0.0
    if t == proj_start() - 1:
        return asset_share_init()
    return max(0.0, asset_share_at(t, "AFT_MC"))


def unit_price(t):
    """Q(t): the with-profits unit price at the end of policy year t.

    ``Q(t) = Q(t-1)(1 + b(t))``, and it **never decreases** - the non-negative bonus is
    a contractual floor, which is what makes a declaration irreversible.  Constant on
    the endowment chassis, where the guarantee is carried as an amount rather than a
    price.
    """
    if t < proj_start() - 1:
        return unit_price_init()
    if t == proj_start() - 1:
        return unit_price_init()
    return unit_price(t - 1) * (1.0 + bonus_rate(t))


def units(t):
    """U(t): the units held at the end of policy year t.

    Bought with the year's premium at the previous price and cancelled to fund the
    year's withdrawal.  Constant in the base run, where the bond is single premium and
    nothing is withdrawn.  Nil on the endowment chassis, which carries its guarantee as
    an amount rather than as units at a price.
    """
    if not is_unitised():
        return 0.0
    if t <= proj_start() - 1:
        return units_init()
    q = unit_price(t - 1)
    if q <= 0.0:
        return units(t - 1)
    return (units(t - 1) + prem_alloc_rate * premium_pp(t) / q       # noqa: F821
            - wd_pp(t) / q)


def guar_benefit_pp(t):
    """The guaranteed benefit at the end of policy year t.

    The unit face value ``U(t) Q(t)`` on the bond chassis, and the sum assured plus
    attaching reversionary bonuses ``G(t) = G(t-1)(1 + b(t))`` on the endowment.  Two
    contractual forms, one cells: every rule that consumes it - the bonus cost, the
    mortality charge's sum at risk, the final bonus, the MVR - treats them identically,
    so keeping two names would duplicate five rules to no purpose.
    """
    if is_unitised():
        return units(t) * unit_price(t)
    if t <= proj_start() - 1:
        return sum_assured() + attaching_bonus()
    return guar_benefit_pp(t - 1) * (1.0 + bonus_rate(t))


def policy_value_pp(t):
    """The pre-MVR policy value: the guaranteed benefit plus any final bonus.

    What a withdrawal is taken pro rata to, and what an MVR is measured against.
    """
    return guar_benefit_pp(t) + final_bonus_pp(t)


def bonus_supportable(t):
    """b_supp: the level bonus rate that fills the guarantee to the target **[std]**.

    Project the asset share to the horizon at the expected net return, take
    ``guar_fill_target`` of it, and solve for the level rate that grows the current
    guaranteed benefit to that amount::

        b_supp = [theta AS_proj / GB(t)]^(1/m) - 1

    with ``m`` the remaining endowment term or the bond's bonus-setting horizon.  Future
    premiums are accumulated to the horizon at the same net return.  Read only when
    ``bonus_rule_on`` is set.
    """
    m = (bonus_horizon if is_unitised()                              # noqa: F821
         else max(1, policy_term() - t))
    r_e = fund_return() - amc_rate - guar_charge_rate(t)             # noqa: F821
    proj = asset_share(t - 1) * (1.0 + r_e) ** m
    p = premium_regular_pp()
    if p > 0.0:
        if abs(r_e) < 1e-12:
            proj += p * m
        else:
            proj += p * (1.0 + r_e) * ((1.0 + r_e) ** m - 1.0) / r_e
    gb = guar_benefit_pp(t - 1)
    if gb <= 0.0 or proj <= 0.0:
        return 0.0
    return (guar_fill_target * proj / gb) ** (1.0 / m) - 1.0         # noqa: F821


def bonus_rate(t):
    """b(t): the regular or reversionary bonus rate declared for policy year t.

    The model point's snapshot rate, held level, which is what the notes' base
    projection does.  With ``bonus_rule_on`` set, the smoothed setting rule applies
    instead::

        b(t) = max(0, b(t-1) + clamp(kappa (b_supp - b(t-1)), -1%, +1%))

    The floor at zero is contractual - a declared bonus can be nil but never negative -
    and the plus or minus one percent is the gradual-change discipline firms state in
    their principles and practices.
    """
    if not bonus_rule_on:                                            # noqa: F821
        return bonus_rate_init()
    if t <= proj_start():
        return bonus_rate_init()
    prev = bonus_rate(t - 1)
    step = bonus_speed * (bonus_supportable(t) - prev)               # noqa: F821
    step = max(-bonus_change_cap, min(bonus_change_cap, step))       # noqa: F821
    return max(0.0, prev + step)


def cost_of_bonus_pp(t):
    """CB(t): the cost of the bonus declared in policy year t **[std]**.

    On the bond chassis it is the face-value uplift the declaration delivers,
    ``b(t) FV(t-1)``.  On the endowment it is the declared addition to the guarantee
    discounted to the declaration date at the surrender-basis rate, since the addition
    is not payable until maturity; the survivorship discount is omitted **[std]**.
    """
    if is_unitised():
        return bonus_rate(t) * guar_benefit_pp(t - 1)
    delta = guar_benefit_pp(t) - guar_benefit_pp(t - 1)
    years = max(0, policy_term() - t)
    return delta / (1.0 + surr_disc_rate) ** years                   # noqa: F821


def shareholder_transfer_pp(t):
    """ST(t) = CB(t)/9: the 90:10 shareholder transfer, charged to the asset share.

    One ninth of the cost of bonus, so that shareholders receive a tenth of each
    distribution and policyholders nine tenths.  It is a real cash outflow from the fund
    and is reported as its own line, not netted into anything.
    """
    return cost_of_bonus_pp(t) / shareholder_transfer_divisor        # noqa: F821


def mort_rate(t):
    """q(x+t-1): the annual best-estimate mortality rate in policy year t **[std]**.

    The shipped table rate times ``mort_be_factor``.  Both are placeholders: CMI
    tables issued after March 2013 are subscriber-restricted, so the table is an
    ONS-shaped proxy and the factor a crude allowance for population mortality being
    heavier than insured experience.
    """
    x = min(age(t), omega_age)                                       # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


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
    """MC(t): the mortality charge deducted from the asset share in policy year t.

    ``q x max(0, DB_g(t) - AS_after_ST)``: the mortality rate times the sum at risk,
    measured on the balance **after** the shareholder transfer.  Differences between
    charged and actual mortality accrue to the estate, which is why this is a charge
    rather than a claim.
    """
    return mort_rate(t) * max(0.0, death_guar_pp(t)
                              - asset_share_at(t, "AFT_ST"))


def smoothed_payout_capped(t):
    """S_cap: the asset share after the year-on-year smoothing cap, before the corridor.

    ``clamp(AS(t), (1 - sigma) S(t-1), (1 + sigma) S(t-1))`` at ``sigma = 10%``.  This is
    what stops a market shock reaching payouts in one step, and it is applied **before**
    the corridor.

    The cap is **skipped where there is no previous payout** to compare against - the
    first year of a new-business cell, where ``S(t-1) = 0`` would otherwise clamp the
    payout to nil and leave the corridor to do all the work.  See the Space docstring on
    what the cap can and cannot say about a premium-paying policy.
    """
    prev = smoothed_payout(t - 1)
    if prev <= 0.0:
        return asset_share(t)
    lo = (1.0 - smooth_cap) * prev                                   # noqa: F821
    hi = (1.0 + smooth_cap) * prev                                   # noqa: F821
    return max(lo, min(hi, asset_share(t)))


def smoothed_payout(t):
    """S(t): the smoothed target payout at the end of policy year t.

    The capped value, then clamped into the target corridor of 80% to 120% of the asset
    share.  The corridor is what stops the cap holding a payout indefinitely away from
    the asset share; the order - cap first, corridor second - is what produces the
    pattern the two rules are designed for.

    The regulatory target-range test is a *portfolio* property, a proportion of policies
    within the range, which a single-policy model cannot express; the deterministic
    corridor is a **[std]** reading of it.
    """
    if t <= proj_start() - 1:
        return smoothed_payout_init()
    as_t = asset_share(t)
    lo = corridor_lo * as_t                                          # noqa: F821
    hi = corridor_hi * as_t                                          # noqa: F821
    return max(lo, min(hi, smoothed_payout_capped(t)))


def final_bonus_pp(t):
    """FB(t) or TB(t): the final or terminal bonus, ``max(0, S(t) - GB(t))``.

    The non-guaranteed top-up from the guaranteed benefit to the smoothed payout, and
    the form the discretion keeps a substantial proportion of the payout in - precisely
    because it is the part that has not hardened.
    """
    return max(0.0, smoothed_payout(t) - guar_benefit_pp(t))


def mvr_pp(t):
    """MVR(t): the market value reduction **scale** in policy year t.

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
    """The market value reduction an exit in policy year t actually bears.

    Zero on a guarantee date, where the contract promises the full guaranteed benefit
    without reduction, and zero on death.  The death case is handled in
    :func:`claim_pp` rather than here, because only the surrender payout reads this.
    Zero throughout on the endowment chassis, which has no units to reduce.
    """
    if is_guarantee_date(t):
        return 0.0
    return mvr_pp(t)


def claim_pp(t, kind):
    """The payout per claim in policy year t, by kind.

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
        ``t`` so the two can be compared, but paid only where
        :func:`is_guarantee_date` - on those years it equals the surrender
        payout, because the MVR is not applied.  The endowment chassis has
        no guarantee dates, so this is informational there.

    ``"MATURITY"``
        ``G(n) + TB(n)`` at the end of the endowment term.  On the bond
        chassis, which is whole of life, this is zero unless the projection
        ends in a **forced encashment** - the withdrawal election has
        cancelled the last unit - in which case the survivors are paid
        ``FV + FB``, the residual final bonus included.  A limiting-age
        ending pays nothing, because it is a modelling truncation rather
        than a contractual event.
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
        if t != proj_len():
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
    """The table annual surrender rate in policy year t **[std]**.

    Read from the chassis's own row of the lapse table; policy years beyond the table
    take its last row.  A drafting construction: no public UK with-profits lapse
    experience was retrieved.
    """
    tbl = data.lapse_table().loc[chassis()]                          # noqa: F821
    return float(tbl.loc[min(t, int(tbl.index.max())), "lapse_rate"])


def mvr_deterrent(t):
    """0.6 while an MVR would be applied, 1 otherwise **[std]**.

    An active market value reduction penalizes exit, and firms may consider exit volumes
    when setting reductions inside the contractual bound.
    """
    return mvr_deterrent_factor if mvr_applied_pp(t) > 0.0 else 1.0  # noqa: F821


def guarantee_spike(t):
    """2.5 in a guarantee-date year **when the guarantee is in the money** **[std]**.

    The gate matters: MVR-free encashment is worth exercising precisely when the
    guaranteed benefit exceeds the asset share and worth nothing otherwise, so applying
    the spike unconditionally would invent anti-selection where there is none.  This is
    the dominant behavioural risk on with-profits business.
    """
    if is_guarantee_date(t) and guar_benefit_pp(t) > asset_share(t):
        return guarantee_spike_factor                                # noqa: F821
    return 1.0


def guarantee_imminent(t):
    """0.8 in the year before a guarantee date **[std]**: policyholders wait for it."""
    return (guarantee_imminent_factor if is_guarantee_date(t + 1)    # noqa: F821
            else 1.0)


def surr_rate(t):
    """w(t): the annual surrender rate applied at the end of policy year t.

    The table rate times all three behavioural multipliers, capped at 1.
    """
    return min(1.0, surr_rate_base(t) * mvr_deterrent(t)
               * guarantee_spike(t) * guarantee_imminent(t))


def pols_if(t):
    """l(t-1): the number of policies in force at the **start** of policy year t."""
    if t < proj_start() or t > proj_len():
        return 0.0
    if t == proj_start():
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        the start of the year, before any decrement; :func:`pols_if`.

    ``"BEF_SURR"``
        after deaths, before surrenders - the processing order is death
        before surrender **[std]**.

    ``"AFT_DECR"``
        the end-of-year count, and zero in the final projected year, where
        the endowment matures and the bond projection is truncated.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_SURR":
        return pols_if(t) * (1.0 - mort_rate(t))
    if timing == "AFT_DECR":
        if t < proj_start() or t >= proj_len():
            return 0.0
        return pols_if_at(t, "BEF_SURR") * (1.0 - surr_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in policy year t, against the start-of-year in force."""
    return pols_if(t) * mort_rate(t)


def pols_surr(t):
    """Surrenders at the end of policy year t, from the survivors of mortality."""
    return pols_if_at(t, "BEF_SURR") * surr_rate(t)


def pols_maturity(t):
    """Survivors at the end of the projection: maturities, or the bond's truncation.

    On the endowment chassis these are genuine maturities and are paid.  On the bond
    chassis they are paid where the projection ends in a forced encashment and pay
    nothing where it ends at the limiting age - see :func:`is_forced_encashment`.
    """
    if t != proj_len():
        return 0.0
    return pols_if(t) - pols_death(t) - pols_surr(t)


def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + pi)^(t-1)`` **[std]**."""
    return (1.0 + inflation_rate) ** (t - 1)                         # noqa: F821


def premiums(t):
    """Premium income at the start of policy year t, an inflow."""
    return premium_pp(t) * pols_if(t)


def withdrawals(t):
    """Partial withdrawals paid at the start of policy year t.

    An owner election rather than a claim, which is why it has its own name and column.
    """
    return wd_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

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
    """E(t): the maintenance expense in policy year t **[std]**.

    £30 a policy a year inflating at 3%.  Where a fund's actual expenses exceed the
    capped charge taken from asset shares, the excess falls to the estate - a fund-level
    flow a single-policy model cannot see.
    """
    return expense_maint * inflation_factor(t) * pols_if(t)          # noqa: F821


def shareholder_transfers(t):
    """The 90:10 shareholder transfer paid out of the fund in policy year t.

    The transfer on the year's declared bonus, weighted by the in force, plus a ninth of
    the final bonus actually paid on the year's claims - the same 90:10 split applied at
    the point the non-guaranteed part is handed over.
    """
    on_declaration = shareholder_transfer_pp(t) * pols_if(t)
    exits = pols_death(t) + pols_surr(t) + pols_maturity(t)
    on_final_bonus = (final_bonus_pp(t) * exits
                      / shareholder_transfer_divisor)                # noqa: F821
    return on_declaration + on_final_bonus


def smoothing_cost(t):
    """The estate's smoothing and guarantee cost on the year's exits.

    Each exiting policy is paid its smoothed payout while the asset share it earned is
    released; the difference falls on the estate.  Positive in a year when guarantees or
    smoothing pay more than the policies earned.
    """
    return (smoothing_cost_pp(t, "DEATH") * pols_death(t)
            + smoothing_cost_pp(t, "SURRENDER") * pols_surr(t)
            + smoothing_cost_pp(t, "MATURITY") * pols_maturity(t))


def smoothing_account(t):
    """SM(t): the cumulative smoothing and guarantee cost borne by the estate.

    Intended broadly neutral over time.  The base model tracks the balance without
    recycling it into credited returns; one insurer operates that recycling, feeding it
    back subject to a maximum annual deduction from asset shares [S5].
    """
    if t < proj_start():
        return 0.0
    return smoothing_account(t - 1) + smoothing_cost(t)


def net_cf(t):
    """The net cash flow of policy year t, **income positive**.

    Premiums less claims, withdrawals, expenses and shareholder transfers.  The asset
    share appears nowhere in it: it is a state variable, not a cash flow, and the
    payouts it drives are already in ``claims``.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - shareholder_transfers(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere."""
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_surr(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected year."""
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(proj_start(), proj_len() + 1))


def check_asset_share_roll_fwd_resid(t):
    """The asset share recursion residual in policy year t; zero everywhere.

    ``AS(t) - max(0, {[AS(t-1) + P - W_AS](1 + r)(1 - c_amc - c_g) - ST - MC + M})``,
    rebuilt in one expression rather than through :func:`asset_share_at`, so that a
    mis-ordered step - a shareholder transfer taken before the charges, say, or a
    mortality charge measured on the wrong balance - shows up here.  The outer
    ``max(0, ...)`` is the zero floor :func:`asset_share` applies; the check still
    validates the ordering in every year the floor is not binding, which is every year of
    every cell shipped here except the tail of the sustained down scenario.
    """
    built = ((asset_share(t - 1) + premium_pp(t) - wd_as_pp(t))
             * (1.0 + fund_return())
             * (1.0 - amc_rate - guar_charge_rate(t))                # noqa: F821
             - shareholder_transfer_pp(t) - mort_charge_pp(t)
             + misc_surplus_pp(t))
    return asset_share(t) - max(0.0, built)


def check_asset_share_roll_fwd():
    """True when the asset share recursion closes in every projected year."""
    return all(abs(check_asset_share_roll_fwd_resid(t)) <= 1e-8
               for t in range(proj_start(), proj_len() + 1))


def check_fb_mvr_exclusive():
    """True when no year carries both a final bonus and a market value reduction.

    ``FB > 0`` requires ``S > GB`` and ``MVR > 0`` requires ``S < GB``, so the two
    cannot both be positive.  An implementation that computed them independently could
    produce both, and would then pay a final bonus and deduct a reduction on the same
    exit.
    """
    return all(min(final_bonus_pp(t), mvr_pp(t)) <= 1e-9
               for t in range(proj_start(), proj_len() + 1))


def check_mvr_bound():
    """True when the market value reduction stays inside its contractual bound.

    It may not exceed the excess of the unit value over the underlying asset value,
    ``max(0, GB - AS)``.  The bound is a conduct rule, not a modelling nicety.
    """
    return all(mvr_pp(t) <= max(0.0, guar_benefit_pp(t) - asset_share(t)) + 1e-9
               for t in range(proj_start(), proj_len() + 1))


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
               for t in range(proj_start(), proj_len() + 1))


def check_payout_corridor():
    """True when the smoothed payout stays inside the 80-120% target corridor.

    Deterministic at model-point level; the regulatory test is a portfolio property that
    a single-policy model cannot express.
    """
    for t in range(proj_start(), proj_len() + 1):
        as_t = asset_share(t)
        if as_t <= 0.0:
            continue
        ratio = smoothed_payout(t) / as_t
        if ratio < corridor_lo - 1e-9 or ratio > corridor_hi + 1e-9:  # noqa: F821
            return False
    return True


def result_cf():
    """Result table of cashflows, indexed by policy year t.

    ``pols_if`` is the start-of-year count that weights every flow on the row.  The
    asset share is published beside them as ``asset_share`` because it is what the
    payouts are measured against - but it is a state variable, not a cash flow, and it
    is not part of ``net_cf``.
    """
    ts = list(range(proj_start(), proj_len() + 1))
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
    """Result table of the payout machinery, indexed by policy year t.

    The asset share against the guaranteed benefit and the smoothed payout, and the
    final bonus and market value reduction the gap between them produces.
    """
    ts = list(range(proj_start(), proj_len() + 1))
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

guarantee_spike_factor = 2.5

guarantee_imminent_factor = 0.8

expense_maint = 30.0

inflation_rate = 0.03

pd = ("Module", "pandas")