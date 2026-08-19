# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.ULB_UK_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked-example anchor cell
    >>> Projection.point_id = 2            # the accumulation cell, no withdrawals

``t`` counts **policy months**, 1-based. The notes index the unit fund ``UF(t)`` at the
**end** of month ``t`` with ``UF(0) = P``; the library indexes :func:`av_pp` at the
**start**, so ``av_pp(t)`` is the notes' ``UF(t-1)`` — the column their worked-example
table prints first — and the notes' ``UF(t)`` is ``av_pp_at(t, "AFT_WD")``, which equals
``av_pp(t + 1)``.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/unit_linked_bond/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ULB_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.ULB_UK_S.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
surr_table_file         data.surr_table()               surr_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``savings.CashValue_SE`` and ``basiclife.BasicTerm_S``
wherever those models have an analogue, and the account-value vocabulary the U.S. models
in this library settled on — ``av_pp_at(t, timing)`` for the fund read at a point inside
the month, ``check_av_roll_fwd`` for its identity. The technical notes use compact
symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the cells argument)            Policy month
y = ceil(t/12)             policy_year(t)                  Policy year containing month t
a                          age(t)                          Attained age (ALB)
(none)                     duration(t)                     Completed policy years, y - 1
(none)                     duration_mth(t)                 Months elapsed at end of month t
P                          premium()                       Single premium
UF(t-1)                    av_pp(t)                        Unit fund at the start of month t
UF_g(t), UF'(t), UF(t)     av_pp_at(t, timing)             The fund inside month t
(per segment)              av_per_segment_pp(t)            The fund divided by the segments
g                          fund_return                     Annual gross fund return
g_m                        fund_return_mth()               Its monthly equivalent
G$(t)                      fund_growth_pp(t)               Gross return credited in month t
t_pf                       tax_provision_rate()            Tax provision rate
TX(t)                      tax_provision_pp(t)             Tax provision deducted
c, c_m                     amc_rate(), amc_rate_mth()      Annual management charge
AMC$(t)                    amc_pp(t)                       AMC collected in month t
f, f_m                     further_costs_rate()            Fund-borne further costs
FC$(t)                     further_costs_pp(t)             Further costs borne in month t
u                          db_uplift()                     Death-benefit uplift, 1.001
W(t)                       wd_pp(t)                        Withdrawal cancelled at EOM
(cap)                      wd_cap_pp(t)                    Rolling 12-month withdrawal cap
(pattern)                  wd_pattern()                    none / allowance_5pct / custom
AC(t)                      adviser_charge_pp(t)            Ongoing adviser charge
GC(t)                      gmdb_charge_pp(t)               GMDB rider charge
G(t)                       gmdb_guarantee_pp(t)            GMDB guaranteed amount
gmdb_flag                  gmdb_flag()                     Rider elected
DS(t)                      death_strain_pp(t)              Non-unit cost per death
q_a, q_m(t)                mort_rate(t), mort_rate_mth(t)  Mortality rates
w_base(y)                  surr_rate_base(t)               Table surrender rate
M_perf(t)                  perf_factor(t)                  Performance lapse multiplier
M_allow(y)                 allow_factor(t)                 Allowance-exhaustion step
w_ann(y,t), w_m(t)         surr_rate(t), surr_rate_mth(t)  Surrender rates applied
l(t-1)                     pols_if(t)                      In force at the start of month t
l(t)                       pols_if_at(t, timing)           BEF_DECR / BEF_SURR / AFT_DECR
(none)                     pols_death(t)                   Deaths in month t
(none)                     pols_surr(t)                    Surrenders at the end of month t
(none)                     pols_maturity(t)                In force when the projection ends
CumWD(n)                   wd_cum_pp(t)                    Cumulative withdrawals + charges
CumAllow(n)                allowance_cum_pp(t)             Cumulative 5% allowable element
ExcessGain(n)              excess_gain_pp(t)               Excess-event gain, policyholder side
E(t)                       expenses(t)                     Acquisition + maintenance
(none)                     inflation_factor(t)             Expense inflation factor
(unit cancellations)       claims(t, kind)                 Gross benefit outgo by kind
(none)                     unit_releases(t)                Units cancelled to fund benefits
(none)                     withdrawals(t)                  Withdrawal outgo
AMC$ x l                   amc_charges(t)                  AMC margin collected
FC$ x l                    further_costs(t)                Further costs, a pass-through
TX x l                     tax_provisions(t)               Tax provision, a pass-through
NUCF(t)                    net_cf(t)                       Non-unit cash flow, income positive
=========================  ==============================  ==========================

Four names needed care.

``UF`` is the unit fund, and the library calls a policyholder-owned fund
:func:`av_pp_at`. The house name wins, because one concept must not carry two names
across the library — but the docstrings and the ``result_cf`` columns keep the unit
vocabulary the product is actually discussed in, and ``av_pp(t)`` is documented
everywhere as the notes' ``UF(t-1)``.

``G`` is used twice in the notes: ``G$(t)`` is the gross fund return credited in the
month and ``G(t)`` the GMDB guaranteed amount. They become :func:`fund_growth_pp` and
:func:`gmdb_guarantee_pp`; nothing here is called ``G``.

``net_cf`` on this product is the **non-unit** cash flow, not a gross liability total.
That is not a departure from the library convention but the consequence of the product:
every benefit is funded by cancelling the policyholder's own units, so a gross
presentation adds the same money to both sides. The gross flows are still published —
``claims_death``, ``claims_surrender``, ``withdrawals`` and ``unit_releases`` are
``result_cf`` columns — and :func:`check_unit_funding` asserts that they net exactly
against the fund.

``pols_maturity`` is borrowed from the term models and, as in ``WOL_UK_S``, means
something different: a bond has no maturity date, so this is the population still in
force when the projection ends. It pays nothing and exists only so the roll-forward
closes in the last month.

.. rubric:: The unit fund recursion, and the order the charges come in

Per policy, within month ``t``::

    UF_g(t) = UF(t-1) x (1 + g_m(1 - t_pf))          growth, net of the tax provision
    UF'(t)  = UF_g(t) x (1 - c_m - f_m)              AMC and further costs
    UF(t)   = UF'(t) - W(t) - AC(t) - GC(t)          unit cancellations at end of month

The **order matters and is a listed pitfall**. The annual management charge accrues
daily through the unit price, so it is levied on the post-growth, pre-cancellation fund.
Charging it on ``UF(t-1)`` instead, or after the withdrawal, moves the margin by about
half a month's growth or withdrawal — small in one month and systematic over decades.
:func:`av_pp_at` exposes all three points so the ordering is inspectable rather than
buried in one expression.

.. rubric:: What is margin and what is a pass-through

Only two of the four amounts that leave the unit fund are insurer income:

============================  ==============  ===================================
Amount                        Insurer income  Why
============================  ==============  ===================================
AMC                           **yes**         the charge for managing the contract
GMDB rider charge             **yes**         the price of the guarantee
Further costs                 no              fund-borne expenses, paid on to the fund
Tax provision                 no              collected in-price, paid on as tax
Adviser charges               no              post-RDR pass-throughs facilitated by
                                              cancelling units
============================  ==============  ===================================

Booking the pass-throughs as margin is the notes' second-listed pitfall and would
overstate the year-one non-unit result by more than the AMC itself — the tax provision
alone is about 97% of the AMC on the anchor cell, and the further costs another 10%.
:func:`further_costs` and :func:`tax_provisions` are therefore published as their own
``result_cf`` columns and are **not** in :func:`net_cf`, so the exclusion is visible.

.. rubric:: The death strain is the uplift, not the death benefit

The sum assured is ``u x UF``, of which ``UF`` is funded by cancelling the policyholder's
own units. The non-unit cost per death is therefore only

    DS(t) = (u - 1) UF(t) + max(0, G(t) - u UF(t)) 1{gmdb}

— a tenth of a percent of the fund on the composite, plus any in-the-money guarantee.
The uplift is a **parameter and never a literal**: 100.1% against 101% is a tenfold
difference in death strain, which the notes list as a pitfall and model point 5
exercises.

.. rubric:: The 5% allowance is policyholder tax machinery, not a product feature

:func:`allowance_cum_pp` and :func:`excess_gain_pp` track the cumulative 5% tax-deferred
allowance and the excess-event gain it produces when exceeded. **Neither generates an
insurer cash flow.** The allowance never caps what can be withdrawn — the *product* cap
is the rolling 7.5% of :func:`wd_cap_pp` — and treating it as a product feature is a
listed pitfall. It is carried because it drives behaviour: the allowance-exhaustion step
in :func:`allow_factor` raises surrender from policy year 21, once twenty years of
allowance have been drawn.

.. rubric:: The fund runs out, and the projection ends there

A 5% withdrawal against a 5% gross return is not sustainable once the tax provision and
the charges are taken: the fund drifts down and, on the deterministic base run, reaches
zero inside the annuitant's lifetime. :func:`wd_pp` caps the withdrawal at what the fund
can pay, so the fund never goes negative, and :func:`proj_len` ends the projection at
:func:`fund_exhaust_mth` — a bond with no units has no liability, no margin and nothing
left to project. That is a product fact worth seeing rather than an artefact to hide:
the anchor cell's fund is exhausted around policy year 30, and every margin the insurer
was counting on stops there.

.. rubric:: Behaviour is the whole valuation

Every margin line is proportional to the unit fund **and** to persistency, and a
surrender costs nothing at the point of exit — the surrender value is the bid value of
units, cancelled — while truncating the entire future AMC stream. Two dynamic overlays
sit on the base table, both **[std]** and both inert in the deterministic base run:

- :func:`perf_factor`, ``min(2, 1 + 2 max(0, g_ref - R_12m))``, raising surrender after
  poor performance. The base run has ``R_12m = g_ref`` by construction, so it is 1;
  ``return_shock`` moves the trailing return without disturbing the fund path, which
  is what makes the multiplier testable in isolation.
- :func:`allow_factor`, a step to 1.5 from policy year 21, when the tax allowance is
  spent.

There is no interest-sensitive dynamic lapse and no paid-up state: the product is single
premium, so there is no premium obligation to stop.
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
    """The issue age of the selected model point, **age last birthday**.

    ALB is chosen to index directly into the single-year-of-age table used as the
    **[std]** mortality proxy.  The anchor documents quote contractual age limits next
    birthday; the difference is immaterial to a product whose death strain is a tenth of
    a percent of the fund.
    """
    return int(model_point()["age_at_entry"])


def sex():
    """The sex (M / F) of the selected model point."""
    return model_point()["sex"]


def lives():
    """``single``.  Joint last-death bonds are out of scope in this composite."""
    v = model_point()["lives"]
    if v != "single":
        raise ValueError("invalid lives")
    return v


def premium():
    """P: the single premium, net of any set-up adviser charge.

    Top-ups are excluded from the base projection: a top-up is a new model point with
    its own premium, allowance clock and segments **[std]**.
    """
    return float(model_point()["premium"])


def n_segments():
    """The number of identical segments the bond is written in; 100 **[std]**.

    Per-segment values are bond values divided by this.  Modelling at bond level is
    exact only while all segments stay identical - a segment surrender breaks the
    symmetry - and the composite keeps bond-level modelling and notes the approximation.
    """
    return int(model_point()["n_segments"])


def db_uplift():
    """u: the death benefit as a multiple of the bid value of units; 1.001.

    A **parameter and never a literal**: 100.1% against 101% is a tenfold difference in
    death strain, which is the whole non-unit cost of mortality on this product.  Model
    point 5 is the anchor cell at 101% and exists to make that visible.
    """
    return float(model_point()["db_uplift"])


def amc_rate():
    """c: the annual management charge, 1.00% **[std]**.

    A snapshot of a discretionary element: per-fund charge rate cards are not published,
    and the insurer's provisions allow the charge to be increased.  It is the insurer's
    only material income line, so its level sets the whole result.
    """
    return float(model_point()["amc_rate"])


def further_costs_rate():
    """f: the fund-borne further costs, 0.10% **[std]**.

    Reduces the unit fund and is **not** insurer income - it is paid on as a fund
    expense.  Booking it as margin is a listed pitfall.
    """
    return float(model_point()["further_costs_rate"])


def tax_provision_rate():
    """t_pf: the life-fund tax provision taken in-price, 20% of gross return **[std]**.

    Collected through the unit price and paid on as corporation tax, so it is neutral to
    the insurer's margin in this model.  The real I-E position has timing differences -
    income as received, realised gains at the next charge date, an annual deemed
    disposal, settlement on full surrender - and base differences including expense
    relief and the minimum profits test, all of which create insurer-side tax strain or
    float that this proxy does not capture.
    """
    return float(model_point()["tax_provision_rate"])


def wd_pattern():
    """``none``, ``allowance_5pct`` or ``custom``: the regular withdrawal pattern.

    ``allowance_5pct`` is the anchor: 5% of premium a year, taken monthly.  That is the
    pattern every fetched key features document leads with, it sits inside the 7.5%
    product cap, and adviser charges consume the same tax allowance - so rational
    take-up gravitates to 5% inclusive of charges.
    """
    v = model_point()["wd_pattern"]
    if v not in ("none", "allowance_5pct", "custom"):
        raise ValueError("invalid wd_pattern")
    return v


def wd_rate():
    """The annual regular withdrawal as a fraction of the premium.

    Zero on ``none``, 5% on ``allowance_5pct``, and the model point's own rate on
    ``custom``.
    """
    p = wd_pattern()
    if p == "none":
        return 0.0
    if p == "allowance_5pct":
        return wd_allowance_rate                                     # noqa: F821
    return float(model_point()["wd_rate_custom"])


def oac_rate():
    """The ongoing adviser charge as an annual rate on the unit value; 0 in the base run.

    Post-RDR adviser charges are **pass-throughs** facilitated by cancelling units: they
    reduce the fund and consume the policyholder's tax allowance, and they add nothing to
    the insurer's non-unit cash flow.  Treating them as income is a listed pitfall.
    """
    return float(model_point()["oac_rate"])


def gmdb_flag():
    """Whether the return-of-premium death benefit rider is elected; false in the base.

    With it, the death strain stops being negligible and becomes market-contingent, and
    the rider's charge scale is unpublished - so the **[std]** cost-of-insurance form
    used here is a guess.  Enable it only with its own sensitivity set.
    """
    return bool(model_point()["gmdb_flag"])


def av_init_pp():
    """The unit fund at outset; the premium on a new-business cell."""
    return float(model_point()["uf_init"])


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def duration(t):
    """Completed policy years at the start of month t: ``(t - 1) // 12``."""
    return (t - 1) // 12


def duration_mth(t):
    """Months elapsed from issue at the end of month t; equal to t.

    ``t`` is 1-based, so the identity is trivial - the cells exists so the monthly
    models in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y = ceil(t/12): the policy year containing month t; 1 for t = 1..12.

    Also the **insurance year** the tax allowance is tracked against.
    """
    return duration(t) + 1


def age(t):
    """a: the attained age (ALB) in the policy year containing month t."""
    return age_at_entry() + duration(t)


def horizon_mths():
    """The mortality horizon: ``12 x (omega_age - age_at_entry)``."""
    return 12 * (omega_age - age_at_entry())                         # noqa: F821


def fund_exhaust_mth():
    """The first month at which the unit fund has been drawn to nothing.

    ``horizon_mths() + 1`` if it never is.  A 5% withdrawal against a 5% gross return is
    not sustainable once the tax provision and the charges are taken, so on the
    deterministic base run the anchor cell's fund does run out - around policy year 30 -
    and every margin the insurer was counting on stops there.  Searched rather than
    solved, so that any withdrawal pattern and charge basis resolves.
    """
    last = horizon_mths()
    for t in range(1, last + 1):
        if av_pp(t) <= 0.0:
            return t
    return last + 1


def proj_len():
    """Projection length in months: the mortality horizon, or the fund exhausting first.

    A bond has no maturity date, so the horizon is a limiting age - but a bond with no
    units has no liability, no margin and nothing left to project, so the projection also
    ends when the fund does.
    """
    return min(horizon_mths(), fund_exhaust_mth() - 1)


def fund_return_mth():
    """g_m = (1 + g)^(1/12) - 1: the monthly gross fund return **[std]**.

    Deterministic in the base run.  The insurer's margin is proportional to the unit
    fund, so the liability model inherits full market beta on the margin stream: a 20%
    market fall cuts the margin base by about a fifth and, through
    :func:`perf_factor`, raises surrender at the same time.
    """
    return (1.0 + fund_return) ** (1.0 / 12.0) - 1.0                 # noqa: F821


def amc_rate_mth():
    """c_m = c/12: the monthly annual management charge **[std 1/12 accrual]**."""
    return amc_rate() / 12.0


def further_costs_rate_mth():
    """f_m = f/12: the monthly further costs **[std 1/12 accrual]**."""
    return further_costs_rate() / 12.0


def mort_rate(t):
    """q_a: the annual best-estimate mortality rate at the attained age **[std]**.

    The shipped table rate times ``mort_be_factor``, a crude allowance for
    population mortality being heavier than insured-lives experience.  Nearly irrelevant
    to this product unless the guaranteed minimum death benefit rider is enabled.
    """
    x = min(age(t), omega_age)                                       # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def mort_rate_mth(t):
    """q_m = 1 - (1 - q_a)^(1/12): the monthly mortality rate **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def surr_rate_base(t):
    """w_base(y): the table annual full-surrender rate in month t **[std]**.

    2 / 3 / 5 / 8 / 10 percent by band.  Policy years beyond the table take its last row.
    """
    tbl = data.surr_table()                                          # noqa: F821
    y = policy_year(t)
    return float(tbl.loc[min(y, int(tbl.index.max())), "surr_rate"])


def return_12m(t):
    """R_12m: the trailing twelve-month gross fund return driving the lapse multiplier.

    ``fund_return + return_shock`` **[std]**.  The base run leaves the shock at zero, so
    the trailing return equals the reference and the multiplier is 1.  Keeping the shock
    separate from ``fund_return`` is deliberate: it moves the *behavioural* driver
    without disturbing the fund path, which is what makes the multiplier testable in
    isolation.  A stochastic or scenario projection would replace this with a path.
    """
    return fund_return + return_shock                                # noqa: F821


def perf_factor(t):
    """M_perf(t) = min(2, 1 + 2 max(0, g_ref - R_12m)): the performance lapse multiplier.

    Poor recent performance raises surrender **[std]**; 1 in the deterministic base run.
    """
    shortfall = max(0.0, fund_return - return_12m(t))                # noqa: F821
    return min(perf_factor_cap, 1.0 + perf_factor_slope * shortfall)  # noqa: F821


def allow_factor(t):
    """M_allow(y): the allowance-exhaustion step, 1.5 from policy year 21 **[std]**.

    After twenty insurance years the cumulative 5% allowance is fully drawn under the
    anchor withdrawal pattern, and continued withdrawals then generate immediate
    excess-event gains - which pushes policyholders towards full surrender or
    advice-driven restructuring.
    """
    return allow_step if policy_year(t) > allowance_years else 1.0   # noqa: F821


def surr_rate(t):
    """w_ann: the annual full-surrender rate applied in month t.

    ``min(cap, w_base x M_perf x M_allow)``.  A surrender costs the insurer nothing at
    the point of exit - the surrender value is the bid value of units, cancelled, with no
    penalty - but truncates the entire future charge stream, which is why persistency
    rather than mortality dominates this product's value.
    """
    return min(surr_rate_cap,                                        # noqa: F821
               surr_rate_base(t) * perf_factor(t) * allow_factor(t))


def surr_rate_mth(t):
    """w_m = 1 - (1 - w_ann)^(1/12): the monthly surrender rate **[std]**."""
    return 1.0 - (1.0 - surr_rate(t)) ** (1.0 / 12.0)


def av_pp(t):
    """UF(t-1): the unit fund per policy at the **start** of policy month t.

    The bid value of units, and the column the notes' worked-example table prints first.
    ``av_init_pp()`` at ``t = 1``, then the end-of-month value of the previous month.
    Floored at zero: :func:`wd_pp` caps the withdrawal at what the fund can pay, so the
    fund is drawn to nothing rather than through it.
    """
    if t <= 1:
        return av_init_pp()
    return av_pp_at(t - 1, "AFT_WD")


def av_pp_at(t, timing):
    """The unit fund per policy at a point inside policy month t.

    ``"BEF_GROWTH"``
        UF(t-1), the start of the month; the same as :func:`av_pp`.

    ``"AFT_GROWTH"``
        UF_g(t), after the gross return and the tax provision taken in
        price.

    ``"AFT_CHARGE"``
        UF'(t), after the annual management charge and the further costs.
        **This is the base the AMC is levied on**, not ``UF(t-1)`` and not
        the post-withdrawal fund: the charge accrues daily through the
        unit price, so it sits on the post-growth, pre-cancellation fund.

    ``"AFT_WD"``
        UF(t), after the end-of-month unit cancellations - withdrawal,
        adviser charge and rider charge.  Equals ``av_pp(t + 1)``.

    All four points are exposed so that the charge ordering is inspectable rather than
    buried in one expression; charging on the wrong one moves the margin by about half a
    month's growth or withdrawal, which is small monthly and systematic over decades.
    """
    if timing == "BEF_GROWTH":
        return av_pp(t)
    if timing == "AFT_GROWTH":
        return av_pp(t) + fund_growth_pp(t) - tax_provision_pp(t)
    if timing == "AFT_CHARGE":
        return av_pp_at(t, "AFT_GROWTH") - amc_pp(t) - further_costs_pp(t)
    if timing == "AFT_WD":
        return max(0.0, av_pp_at(t, "AFT_CHARGE")
                   - wd_pp(t) - adviser_charge_pp(t) - gmdb_charge_pp(t))
    raise ValueError("invalid timing")


def av_per_segment_pp(t):
    """The unit fund per segment at the start of month t: the bond value over 100.

    Reported only.  A policyholder's tax outcome depends on whether whole segments are
    cashed or a part-surrender is taken across all of them, but the insurer's cash flow
    is identical either way - both cancel the same unit value.
    """
    return av_pp(t) / n_segments()


def fund_growth_pp(t):
    """G$(t) = g_m x UF(t-1): the gross fund return credited in month t."""
    return fund_return_mth() * av_pp(t)


def tax_provision_pp(t):
    """TX(t) = t_pf x G$(t): the tax provision taken in the unit price.

    A **pass-through**, not insurer income: it reduces the unit fund and is paid on as
    corporation tax.  On the anchor cell it is about 97% of the AMC, so counting it as
    margin roughly doubles the year-one non-unit result.
    """
    return tax_provision_rate() * fund_growth_pp(t)


def amc_pp(t):
    """AMC$(t) = c_m x UF_g(t): the annual management charge collected in month t.

    Levied on the post-growth, pre-cancellation fund, because it accrues daily through
    the unit price.  The insurer's only material income line on this product.
    """
    return amc_rate_mth() * av_pp_at(t, "AFT_GROWTH")


def further_costs_pp(t):
    """FC$(t) = f_m x UF_g(t): the fund-borne further costs in month t.

    A **pass-through**, not insurer income.
    """
    return further_costs_rate_mth() * av_pp_at(t, "AFT_GROWTH")


def wd_cap_pp(t):
    """The rolling twelve-month withdrawal cap: ``max(7.5% of UF, 7.5% of premium)``.

    The **product** cap, and the only thing that actually limits what can be withdrawn -
    the 5% tax allowance does not.  Measured against the fund after charges and against
    the premium, whichever is larger, and it includes the ongoing adviser charge.
    """
    return wd_cap_rate * max(                                        # noqa: F821
        av_pp_at(t, "AFT_CHARGE"), premium())


def wd_pp(t):
    """W(t): the regular withdrawal cancelled at the end of month t.

    ``wd_rate x P / 12``, then capped twice: by the product's rolling twelve-month limit
    - a twelfth of it each month, and **net of the ongoing adviser charge**, which counts
    against the same limit - and by what the fund can actually pay after the adviser and
    rider charges.  The second cap is what stops the fund going negative, and it is why
    the projection can end with the fund at exactly zero rather than through it.
    """
    scheduled = wd_rate() * premium() / 12.0
    ac = adviser_charge_pp(t)
    gc = gmdb_charge_pp(t)
    room = max(0.0, wd_cap_pp(t) / 12.0 - ac)
    available = max(0.0, av_pp_at(t, "AFT_CHARGE") - ac - gc)
    return min(scheduled, room, available)


def adviser_charge_pp(t):
    """AC(t): the ongoing adviser charge cancelled at the end of month t.

    ``oac_rate/12`` of the fund after charges.  A **pass-through**: it reduces the unit
    fund and consumes the policyholder's tax allowance, and it is not insurer income.
    """
    return oac_rate() / 12.0 * av_pp_at(t, "AFT_CHARGE")


def gmdb_guarantee_pp(t):
    """G(t): the guaranteed minimum death benefit, if the rider is elected.

    ``premium - cumulative withdrawals - adviser charges``: a return-of-premium
    guarantee that erodes as the policyholder draws the fund down.  Zero without the
    rider.

    Measured **before** the current month's cancellations, at ``wd_cum_pp(t - 1)``.
    That is the only reading that resolves: the rider charge is itself a cancellation
    alongside the withdrawal, so a guarantee net of the same month's withdrawal would
    make the charge depend on a withdrawal that depends on the charge.  Taking the
    start-of-month guarantee breaks the loop and matches the contractual sense, in which
    the amount guaranteed is what is on the record when the month begins.
    """
    if not gmdb_flag():
        return 0.0
    return max(0.0, premium() - wd_cum_pp(t - 1))


def gmdb_charge_pp(t):
    """GC(t): the rider charge cancelled at the end of month t **[std]**.

    ``q_m x max(0, G(t) - u UF'(t))``, a cost-of-insurance form on the in-the-money part
    of the guarantee.  The real charge scale is unpublished, so this is a guess with the
    right shape and no authority.  Insurer income, unlike the other cancellations.
    """
    if not gmdb_flag():
        return 0.0
    naar = max(0.0, gmdb_guarantee_pp(t)
               - db_uplift() * av_pp_at(t, "AFT_CHARGE"))
    return mort_rate_mth(t) * naar


def death_strain_pp(t):
    """DS(t): the **non-unit** cost per death in month t.

    ``(u - 1) UF(t) + max(0, G(t) - u UF(t)) 1{gmdb}``.  The sum assured is ``u x UF``,
    of which ``UF`` is funded by cancelling the policyholder's own units, so the
    insurer's cost is only the uplift - a tenth of a percent of the fund on the composite
    - plus any in-the-money guarantee.
    """
    uf = av_pp_at(t, "AFT_WD")
    strain = (db_uplift() - 1.0) * uf
    if gmdb_flag():
        strain += max(0.0, gmdb_guarantee_pp(t) - db_uplift() * uf)
    return strain


def wd_cum_pp(t):
    """CumWD: cumulative withdrawals and adviser charges to the end of month t.

    The allowance-relevant total: ongoing and ad hoc adviser charges consume the same 5%
    tax allowance as withdrawals do.
    """
    if t <= 0:
        return 0.0
    return wd_cum_pp(t - 1) + wd_pp(t) + adviser_charge_pp(t)


def allowance_cum_pp(t):
    """CumAllow: the cumulative 5% allowable element, ``P x min(y, 20) x 5%``.

    **Policyholder tax machinery, not a product feature.**  It never caps what can be
    withdrawn - the product cap is :func:`wd_cap_pp` - and it generates no insurer cash
    flow.  It is carried because it drives behaviour through :func:`allow_factor`.
    """
    y = policy_year(t)
    return premium() * min(y, allowance_years) * wd_allowance_rate    # noqa: F821


def excess_gain_pp(t):
    """ExcessGain: the excess-event gain at the insurance-year end, if any.

    ``max(0, CumWD - CumAllow)``, cumulative rather than per-year, so the running total
    is the gain reported to date.  **No insurer cash flow**: chargeable events are
    settled between the policyholder and HMRC, with the insurer issuing certificates.
    """
    return max(0.0, wd_cum_pp(t) - allowance_cum_pp(t))


def pols_if(t):
    """l(t-1): the number of policies in force at the **start** of policy month t.

    ``pols_if_init()`` at ``t = 1``, then the notes' recursion
    ``l(t) = l(t-1)(1 - q_m)(1 - w_m)``, deaths before surrenders **[std]**.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement; :func:`pols_if`.

    ``"BEF_SURR"``
        after deaths, before surrenders - the processing order is **death
        before surrender** **[std]**.

    ``"AFT_DECR"``
        the notes' ``l(t)``, the end-of-month count, and zero in the last
        projected month.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_SURR":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        if t < 1 or t >= proj_len():
            return 0.0
        return pols_if_at(t, "BEF_SURR") * (1.0 - surr_rate_mth(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in policy month t, against the start-of-month in-force."""
    return pols_if(t) * mort_rate_mth(t)


def pols_surr(t):
    """Full surrenders at the end of policy month t, from the survivors of mortality."""
    return pols_if_at(t, "BEF_SURR") * surr_rate_mth(t)


def pols_maturity(t):
    """Policies still in force when the projection ends; zero in every other month.

    A bond has no maturity date, so this is either the population left at the limiting
    age or - on the base run - the population still holding a bond whose fund has just
    been drawn to nothing.  It pays nothing, and it exists so the roll-forward closes.
    """
    if t != proj_len():
        return 0.0
    return pols_if(t) - pols_death(t) - pols_surr(t)


def claims(t, kind=None):
    """Gross benefit outgo in policy month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``u x UF(t)`` per death - the full sum assured, of which all but
        the uplift is funded by cancelling the policyholder's own units -
        or the guaranteed amount where the rider is elected and in the
        money, ``max(u x UF(t), G(t))``.

    ``"SURRENDER"``
        ``UF(t)`` per surrender: the bid value of units, with no penalty.

    These are **gross** flows.  They are published so the reader can see the whole
    picture, but they are not in :func:`net_cf`, because :func:`unit_releases` cancels
    them against the fund - all except the death strain.  See the Space docstring.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "SURRENDER"))
    uf = av_pp_at(t, "AFT_WD")
    if kind == "DEATH":
        benefit = db_uplift() * uf
        if gmdb_flag():
            benefit = max(benefit, gmdb_guarantee_pp(t))
        return benefit * pols_death(t)
    if kind == "SURRENDER":
        return uf * pols_surr(t)
    raise ValueError("invalid kind")


def withdrawals(t):
    """Withdrawal and adviser-charge outgo in month t, funded by cancelling units.

    An owner election rather than a claim, which is why it has its own name and its own
    ``result_cf`` column.
    """
    return (wd_pp(t) + adviser_charge_pp(t)) * pols_if(t)


def unit_releases(t):
    """The unit fund cancelled to fund the month's death and surrender benefits.

    ``UF(t) x (deaths + surrenders)``.  The gross benefit outgo less this is exactly the
    death strain, which is the only part the insurer funds from its own resources.
    """
    return av_pp_at(t, "AFT_WD") * (pols_death(t) + pols_surr(t))


def amc_charges(t):
    """The annual management charge collected in month t; **insurer income**."""
    return amc_pp(t) * pols_if(t)


def gmdb_charges(t):
    """The rider charge collected in month t; **insurer income**, zero in the base run."""
    return gmdb_charge_pp(t) * pols_if(t)


def further_costs(t):
    """The fund-borne further costs in month t; a **pass-through**, not income.

    Published as its own column so that its exclusion from :func:`net_cf` is visible
    rather than merely asserted.
    """
    return further_costs_pp(t) * pols_if(t)


def tax_provisions(t):
    """The tax provision taken in the unit price in month t; a **pass-through**.

    About 97% of the annual management charge on the anchor cell, which is the measure of
    how badly counting it as margin would mislead.
    """
    return tax_provision_pp(t) * pols_if(t)


def death_strain(t):
    """The non-unit cost of the month's deaths: the uplift, plus any in-the-money GMDB."""
    return death_strain_pp(t) * pols_death(t)


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y - 1)`` **[std]**."""
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**.

    £300 per policy at issue, then £60 per policy a year inflating at 2.5%.  The margin
    is proportional to the fund while the expense inflates, so a small-fund cell goes
    margin-negative late in life - which the anchor cell does, as its fund is drawn down.
    """
    acq = expense_acq * pols_if(t) if t == 1 else 0.0                # noqa: F821
    return acq + expense_maint / 12.0 * inflation_factor(t) * pols_if(t)  # noqa: F821


def net_cf(t):
    """NUCF(t): the **non-unit** cash flow of month t, income positive.

    ``AMC + rider charge - expenses - death strain``.  Not a gross liability total, and
    that is a product fact rather than a departure: every benefit is funded by cancelling
    the policyholder's own units, so a gross presentation would add the same money to
    both sides.  The tax provision, the further costs and the adviser charges are
    excluded because they are pass-throughs - the notes' second-listed pitfall is
    counting them as margin.

    The result is a fund-based margin stream: proportional to the unit fund and to
    persistency, with mortality contributing about a tenth of a percent of the fund times
    the mortality rate.  Behaviour, not mortality, dominates the value.
    """
    return amc_charges(t) + gmdb_charges(t) - expenses(t) - death_strain(t)


def check_av_roll_fwd_resid(t):
    """The unit fund roll-forward residual in month t; zero everywhere.

    ``UF(t) - [UF(t-1) + growth - tax - AMC - further costs - W - AC - GC]``, per policy.
    This is the identity the charge ordering has to satisfy, and it is checked rather
    than assumed because the ordering is the model's most consequential convention.
    Skipped once the fund has been drawn to nothing, where the withdrawal cap breaks the
    equality by design.
    """
    uf_end = av_pp_at(t, "AFT_WD")
    if uf_end <= 0.0:
        return 0.0
    built = (av_pp(t) + fund_growth_pp(t) - tax_provision_pp(t)
             - amc_pp(t) - further_costs_pp(t)
             - wd_pp(t) - adviser_charge_pp(t) - gmdb_charge_pp(t))
    return uf_end - built


def check_av_roll_fwd():
    """True when the unit fund roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call the same check across every account-value model in the library.
    """
    return all(abs(check_av_roll_fwd_resid(t)) <= 1e-8
               for t in range(1, proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - deaths - surrenders - the final-month residual``.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_surr(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month."""
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(1, proj_len() + 1))


def check_unit_funding_resid(t):
    """How much of the month's benefit outgo the unit fund does **not** fund.

    ``claims(t) - unit_releases(t) - death_strain(t)``, which is zero: the death benefit
    is the unit fund plus the uplift, the surrender benefit is the unit fund exactly, and
    the uplift is precisely the death strain.  A model that funded benefits twice - once
    from the fund and once from the insurer - would show it here.
    """
    return claims(t) - unit_releases(t) - death_strain(t)


def check_unit_funding():
    """True when every benefit is funded by unit cancellation plus the death strain."""
    return all(abs(check_unit_funding_resid(t)) <= 1e-8
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by policy month t.

    ``av_pp`` is the unit fund at the start of the month, and ``pols_if`` the in-force
    count that weights every flow on the row.  ``net_cf`` is the **non-unit** stream -
    what accrues to the insurer - while ``claims_death``, ``claims_surrender``,
    ``withdrawals`` and ``unit_releases`` show the gross picture they net against.
    ``further_costs`` and ``tax_provisions`` are published precisely because they are
    **not** in ``net_cf``: they leave the unit fund and are paid on.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "amc_charges": [amc_charges(t) for t in ts],
            "gmdb_charges": [gmdb_charges(t) for t in ts],
            "further_costs": [further_costs(t) for t in ts],
            "tax_provisions": [tax_provisions(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_surrender": [claims(t, "SURRENDER") for t in ts],
            "unit_releases": [unit_releases(t) for t in ts],
            "death_strain": [death_strain(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_uf():
    """Result table of the unit fund recursion, indexed by policy month t.

    The notes' worked-example table, column for column: the fund at the start of the
    month, the gross return, the tax provision, the charges, the withdrawal, and the fund
    at the end.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp": [av_pp(t) for t in ts],
            "fund_growth_pp": [fund_growth_pp(t) for t in ts],
            "tax_provision_pp": [tax_provision_pp(t) for t in ts],
            "amc_pp": [amc_pp(t) for t in ts],
            "further_costs_pp": [further_costs_pp(t) for t in ts],
            "adviser_charge_pp": [adviser_charge_pp(t) for t in ts],
            "gmdb_charge_pp": [gmdb_charge_pp(t) for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "av_pp_end": [av_pp_at(t, "AFT_WD") for t in ts],
            "wd_cum_pp": [wd_cum_pp(t) for t in ts],
            "allowance_cum_pp": [allowance_cum_pp(t) for t in ts],
            "excess_gain_pp": [excess_gain_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_be_factor = 0.8

fund_return = 0.05

return_shock = 0.0

perf_factor_slope = 2.0

perf_factor_cap = 2.0

surr_rate_cap = 0.35

allow_step = 1.5

allowance_years = 20

wd_allowance_rate = 0.05

wd_cap_rate = 0.075

expense_acq = 300.0

expense_maint = 60.0

inflation_rate = 0.025

pd = ("Module", "pandas")