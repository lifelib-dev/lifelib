# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WOL_UK_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the O50 worked-example anchor cell
    >>> Projection.point_id = 5            # the underwritten cell

``t`` counts **policy months**, 1-based. The notes index the in-force probability
``l(t)`` at the **end** of month ``t`` with ``l(0) = 1``; the library indexes
:func:`pols_if` at the **start**, so ``pols_if(t)`` is the notes' ``l(t-1)`` — which is
the column their worked-example table prints, and the weight on every cash flow of the
same ``result_cf()`` row.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/whole_of_life/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WOL_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.WOL_UK_S.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for annual rates and ``*_rate_mth`` for monthly ones, ``*_pp``
for per-policy amounts, ``claims(t, kind)`` and ``benefit_pp(t, kind)`` with an
uppercase ``kind`` string. The technical notes use compact actuarial symbols instead.
The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
cell                       cell()                          O50 or UW
entry_age                  age_at_entry()                  Entry age (ALB)
a(t)                       age(t)                          Attained age (ALB) in month t
y                          policy_year(t)                  Policy year containing month t
(none)                     duration(t)                     Completed policy years, y - 1
(none)                     duration_mth(t)                 Months elapsed at end of month t
omega                      omega_age                       Limiting age, 120
(none)                     proj_len()                      Last projected month
SA                         sum_assured()                   Sum assured at outset
SA(t)                      cover_pp(t)                     Sum assured in force in month t
P                          premium_mth()                   Monthly premium at outset
P(t)                       premium_pp(t)                   Monthly premium due in month t
T_cess                     cessation_mths()                Months to premium cessation
CumPrem(t)                 prem_cum_pp(t)                  Cumulative premiums paid
(escalation)               esc_cover_step()                Annual cover increase
(escalation)               esc_prem_step()                 Annual premium increase
(moratorium)               moratorium_mths()               O50 moratorium, 12 months
in_moratorium(t)           in_moratorium(t)                Indicator t <= moratorium
DB_na(t)                   benefit_pp(t, "NON_ACC")        Non-accidental death benefit
DB_ac(t)                   benefit_pp(t, "ACC")            Accidental death benefit
(blended)                  benefit_pp(t, "DEATH")          Expected benefit per death
PU                         benefit_pp(t, "PAID_UP")        Paid-up payout on conversion
k_adb                      adb_multiplier()                Accidental multiplier, 1 or 2
delta_acc                  acc_share                       Accidental share of deaths, 3%
delta_su                   suicide_share                   Suicide share of year-1 deaths
N_paid(t)                  payments_made(t)                Monthly payments made
N_expected                 payments_expected()             Payments expected to cessation
paid_up                    pu_eligible(t)                  Pro-rata paid-up qualifies
t*                         crossover_mth()                 Month cumulative premiums pass SA
(basis)                    mort_basis()                    population or assured
(loading)                  mort_loading()                  Anti-selection loading
q(y)                       mort_rate(t)                    Annual mortality rate applied
q_m(y)                     mort_rate_mth(t)                Monthly mortality rate
(improvement)              mort_improve_factor(t)          Improvement factor, 1 in base
w(y)                       lapse_rate(t)                   Annual lapse rate in month t
(table)                    lapse_rate_base(t)              Table lapse rate before beta
beta                       lapse_crossover_beta            Crossover lapse stress dial
w_m(y)                     lapse_rate_mth(t)               Monthly lapse rate
l(t-1)                     pols_if(t)                      Full-cover policies in force
(none)                     pols_pu(t)                      Paid-up policies in force
(none)                     pu_benefit(t)                   Paid-up cover in force
(none)                     pols_all(t)                     pols_if + pols_pu
(none)                     pols_death(t)                   Deaths on full cover
(none)                     pols_death_pu(t)                Deaths on paid-up cover
(none)                     pols_exit(t)                    Would-be lapses
(none)                     pols_convert(t)                 Would-be lapses made paid-up
(none)                     pols_lapse(t)                   Lapses that actually terminate
(none)                     pols_maturity(t)                Survivors at the limiting age
E[premium](t)              premiums(t)                     Premium income
E[death outgo](t)          claims(t, kind)                 Death outgo by kind
E[expenses](t)             expenses(t)                     Acquisition + maintenance
(commission)               commissions(t)                  Initial commission
(none)                     inflation_factor(t)             Expense inflation factor
CF(t)                      net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ==========================

Three names needed care.

The notes' ``l(t)`` is a single in-force probability, but the pro-rata paid-up variant
splits the population in two: policies still on **full cover**, and policies made
**paid-up** at a reduced payout. :func:`pols_if` is the first strand — the notes' ``l``,
and what the worked example prints — :func:`pols_pu` the second, and :func:`pols_all`
their sum, which is what the maintenance expense is carried on. On every model point but
one the second strand is empty and the three coincide.

``SA`` is a constant in the notes and a function of ``t`` here, because the escalating
variants move it. :func:`sum_assured` is the outset value the model point carries and
:func:`cover_pp` the amount in force in month ``t``.

``pols_maturity`` is borrowed from the term models and means something different here.
Whole of life has no maturity: the cells is the population still alive when the
projection is truncated at the limiting age, so it is a **truncation artefact** rather
than a benefit, and it pays nothing. It exists so the roll-forward closes in the last
month; a test asserts it is negligible, which is the real statement — if it were not,
the limiting age would be too low.

.. rubric:: Two cells, two bases, and why they must not be swapped

``cell = "UW"`` is underwritten guaranteed whole of life: full underwriting, level
premiums for life, the sum assured paid once on death or earlier terminal illness.
``cell = "O50"`` is over-50s guaranteed acceptance: no underwriting at all, a fixed cash
sum, a twelve-month moratorium, and premiums ceasing at the anniversary on or after the
90th birthday while cover continues.

They share this engine and **not** their mortality basis. Full underwriting restores
select experience, so the UW cell takes an assured-lives shape. Guaranteed acceptance
removes underwriting, so the O50 pool cannot be better than the population and
self-selects worse; it takes a population shape with an anti-selection loading of 120%
**[std]**. The CMI analyses non-underwritten whole of life separately from underwritten
business for exactly this reason. Feeding either cell the other's basis produces
plausible-looking but wrong margins, and the FCA's price differential between the two
designs — £71.73 against £8.10 per £1,000 of cover — is the scale of that error. The
basis is therefore derived from :func:`cell` rather than being a free parameter.

.. rubric:: The moratorium is a discontinuity, not a curve

During the O50 cell's first twelve months a **non-accidental** death returns the
premiums paid — not the cash sum, not an annualized premium — while an **accidental**
death pays the full cash sum from day one. At month 13 the full cash sum becomes payable
for any death, and expected death outgo jumps about elevenfold on the anchor cell. That
step is the signature of the product and must not be smoothed: an annual-grid
implementation has to split policy year 1 explicitly, and the notes list smoothing it as
a pitfall.

Note where the year-one outgo actually comes from. At month 1 the blended benefit is
``0.97 x £30 + 0.03 x £5,000 = £179.10``: five sixths of it is the small accidental
tail paying the full cash sum, not the premium refund. An implementation that dropped
the accidental split would understate year-one claims by about that much.

The accidental-multiplier variant doubles the accidental benefit, but **only on and after
the first anniversary** [S7] — inside the moratorium the accidental benefit is already
the full cash sum, and doubling it there, or applying the multiplier to all deaths,
overstates outgo. :func:`adb_multiplier` is applied in one place, in
``benefit_pp(t, "ACC")``, past the moratorium only.

.. rubric:: Lapse pays nothing, which is the whole economics

There is no surrender value at any duration on either cell, so a lapse produces no cash
flow at all: its entire effect is through :func:`pols_if`. Every lapse therefore
extinguishes a liability for nothing, the best estimate falls monotonically as assumed
lapses rise, and the FCA records that without the continuing-payer cross-subsidy
insurers would need to rely on lapses to remain profitable. Two consequences are wired
into the model rather than left as prose:

- **No lapse after premiums cease.** There are no premiums to stop paying once the O50
  cell reaches cessation, so :func:`lapse_rate` is zero from there. Applying a lapse
  decrement past cessation silently destroys liability, and the notes list it as a
  pitfall.
- **The pro-rata paid-up variant is a different product.** Once half the expected payments
  have been made, a would-be lapse converts to a **paid-up** policy at
  ``SA x N_paid / N_expected`` instead of forfeiting everything. That converts lapse
  profit into a retained pro-rata liability and collapses most of the lapse sensitivity,
  which is why it is a variant rather than an adjustment. It is carried as a second
  population strand: :func:`pols_pu` counts the policies and :func:`pu_benefit` carries
  their aggregate cover, which is enough because paid-up policies neither lapse nor
  escalate — so the two roll forward on the same survival factor and no per-conversion
  cohort dimension is needed.

.. rubric:: The crossover

On the O50 cell cumulative premiums eventually exceed the cash sum. :func:`crossover_mth`
finds the month: on the anchor cell ``floor(5000/30) + 1 = 167`` months, thirteen years
and eleven months, which is the FCA's stylised example exactly. It is searched rather
than closed-form so that an escalating variant still resolves, and it is reported rather
than acted on — the notes' crossover-aware lapse module, which raises lapse past the
tipping point, is a pure stress dial and is off in the base run
(``lapse_crossover_beta`` is 0). Total premiums are capped at ``P x T_cess``, so a
crossover exists only where the cash sum is below that cap.

.. rubric:: Sign convention

The notes' cash flow table is income positive, which is the library-wide sign of
:func:`net_cf`, so there is no outgo-positive ``liability_cf`` companion. The notes'
worked-example table prints premium income and death outgo as separate positive columns
and omits expenses entirely "for clarity"; :func:`result_cf` carries all of them, so
``net_cf`` will not equal any column of that table.
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


def cell():
    """``O50`` (over-50s guaranteed acceptance) or ``UW`` (underwritten guaranteed).

    The two cells share this engine and not their mortality basis, their lapse table,
    their expense levels or their benefit rules.  See the Space docstring.
    """
    v = model_point()["cell"]
    if v not in ("O50", "UW"):
        raise ValueError("invalid cell")
    return v


def age_at_entry():
    """The entry age of the selected model point, **age last birthday**.

    ALB rather than the age nearest birthday every other model in this library uses:
    the underwritten cell's specimen defines entry age x as "before the (x+1)th
    birthday", which is ALB, and the over-50s documents price on "age at outset" without
    stating a basis **[std]**.  All age lookups here are on that one basis.
    """
    return int(model_point()["entry_age"])


def sex():
    """The sex (M / F) of the selected model point.

    Carried for the basis lookup.  The over-50s documents state age and smoker status as
    the rate factors and do not rate by sex, so on that cell this drives the shipped
    **[std]** proxy table and nothing contractual.
    """
    return model_point()["sex"]


def smoker():
    """The smoker status (NS / S).

    The underwritten specimen distinguishes three smoking states; they are collapsed to
    two here **[std]**.
    """
    return model_point()["smoker"]


def sum_assured():
    """SA: the sum assured or cash sum at outset.

    :func:`cover_pp` is the amount in force in a given month, which differs from this on
    the escalating variants.
    """
    return float(model_point()["sum_assured"])


def premium_mth():
    """P: the monthly premium at outset, guaranteed never to increase.

    A model point input, not a rate-table lookup: no insurer publishes whole of life
    premium rate tables, so any shipped scale would be a **[std]** snapshot calibrated
    to the handful of public quote anchors.
    """
    return float(model_point()["premium_mth"])


def escalation():
    """``level``, ``fixed_5pct`` (the UW increasing-cover variant) or ``rpi``.

    The underwritten variant raises cover 5% and premium 10% a year - two percent of
    premium for each one percent of cover - and the over-50s RPI variant raises the cash
    sum by RPI capped at 10% and the premium by 1.5 x RPI capped at 15%.
    """
    v = model_point()["escalation"]
    if v not in ("level", "fixed_5pct", "rpi"):
        raise ValueError("invalid escalation")
    return v


def cessation_mths():
    """T_cess: months from outset to premium cessation; 0 means premiums for life.

    The over-50s cells cease at the anniversary on or after the 90th birthday **[std]**
    and cover continues; the underwritten cell has no cessation at all.
    """
    return int(model_point()["cessation_months"])


def moratorium_mths():
    """The over-50s moratorium in months, 12; zero on the underwritten cell.

    The underwritten cell has a suicide clause over the same window instead, which is a
    different rule with a different denominator - see :func:`benefit_pp`.
    """
    return int(model_point()["moratorium_months"])


def adb_multiplier():
    """k_adb: the accidental death multiplier past the moratorium, 1 or 2.

    The 2 is one insurer's variant and applies to **accidental** death **on and after
    the first anniversary** only.  Inside the moratorium the accidental benefit is
    already the full cash sum, so doubling it there - or applying the multiplier to all
    deaths - overstates outgo.
    """
    return 2.0 if bool(model_point()["variant_adb_2x"]) else 1.0


def pu_variant():
    """Whether the pro-rata paid-up variant applies.

    Once half the expected payments have been made, a would-be lapse converts to a
    paid-up policy instead of forfeiting everything.  Requires a premium cessation date,
    since ``N_expected`` is measured to it; the underwritten cell has none, so the
    combination raises rather than dividing by zero.
    """
    v = bool(model_point()["variant_paid_up"])
    if v and cessation_mths() <= 0:
        raise ValueError("the pro-rata paid-up value needs a premium cessation date")
    return v


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_len():
    """Projection length in months: ``12 x (omega_age - entry_age)``.

    Whole of life has no maturity date, so the horizon is a **limiting age** rather than
    a contractual one.  The shipped mortality tables reach 1 well before ``omega_age``,
    so the population is exhausted inside the projection rather than truncated by it;
    :func:`check_truncation` asserts that, because a limiting age set too low would
    silently drop liability off the end.
    """
    return 12 * (omega_age - age_at_entry())                         # noqa: F821


def duration(t):
    """Completed policy years at the start of month t: ``(t - 1) // 12``."""
    return (t - 1) // 12


def duration_mth(t):
    """Months elapsed from outset at the end of month t; equal to t.

    ``t`` is 1-based, so the identity is trivial - the cells exists so the monthly
    models in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y = floor((t-1)/12) + 1: the policy year containing month t; 1 for t = 1..12."""
    return duration(t) + 1


def age(t):
    """a(t): the attained age (ALB) in the policy year containing month t."""
    return age_at_entry() + duration(t)


def mort_basis():
    """The mortality basis the cell takes: ``population`` for O50, ``assured`` for UW.

    Derived from :func:`cell` rather than left as a free parameter, because feeding
    either cell the other's basis produces plausible-looking but wrong margins.  See the
    Space docstring.
    """
    return "population" if cell() == "O50" else "assured"


def mort_loading():
    """The anti-selection loading on the table rate: 120% for O50, 100% for UW **[std]**.

    Guaranteed acceptance removes underwriting, so the pool cannot be better than the
    population and self-selects worse.  No insurer discloses its guaranteed-acceptance
    pricing basis, so the loading is a placeholder to be calibrated - and a deliberately
    modest one, since population mortality is already heavier than insured experience.
    """
    return mort_loading_o50 if cell() == "O50" else mort_loading_uw  # noqa: F821


def mort_improve_factor(t):
    """The mortality improvement factor in month t; 1 in the base run **[std]**.

    ``(1 - improvement)^(y - 1)``.  The market-standard expression is a CMI projections
    model with a chosen long-term rate, but that model is subscriber-restricted, so a
    flat annual improvement is the **[std]** sensitivity proxy.  Improvements lengthen
    exactly the part of the liability that is pure outgo - past the crossover and past
    premium cessation - so this is not a second-order dial on this product.
    """
    return (1.0 - mort_improvement) ** (policy_year(t) - 1)          # noqa: F821


def mort_rate(t):
    """q(y): the annual mortality rate applied in the policy year containing month t.

    The cell's table rate at the attained age, times the anti-selection loading and the
    improvement factor, capped at 1.  Both shipped bases are **[std]** proxies shaped
    like the tables the notes name and are not published tables.
    """
    q = float(data.mort_table().loc[                                 # noqa: F821
        (mort_basis(), sex(), smoker(), age(t)), "mort_rate"])
    return min(1.0, q * mort_loading() * mort_improve_factor(t))


def mort_rate_mth(t):
    """q_m(y) = 1 - (1 - q)^(1/12): the monthly mortality rate **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def esc_cover_step():
    """The annual increase in the sum assured under the escalation variant.

    5% on the underwritten increasing-cover variant, and RPI floored at 0 and capped at
    10% on the over-50s RPI variant.  Scaled by ``esc_take_up``, which is 1 in the
    base run: holders may decline an increase, with three declines removing the option,
    but a deterministic run cannot represent a take-up probability, so full take-up is
    assumed and the decline rule is not implemented.
    """
    e = escalation()
    if e == "level":
        return 0.0
    if e == "fixed_5pct":
        return esc_fixed_cover * esc_take_up                         # noqa: F821
    return min(max(rpi_rate, 0.0), esc_rpi_cover_cap) * esc_take_up  # noqa: F821


def esc_prem_step():
    """The annual increase in the premium under the escalation variant.

    10% on the underwritten variant - two percent of premium for each one percent of
    cover - and ``1.5 x RPI`` capped at 15% on the over-50s RPI variant.  Floored at 0:
    the source defines an increase only, with no decrease **[std]**.
    """
    e = escalation()
    if e == "level":
        return 0.0
    if e == "fixed_5pct":
        return esc_fixed_prem * esc_take_up                          # noqa: F821
    return min(max(esc_rpi_prem_mult * rpi_rate, 0.0),               # noqa: F821
               esc_rpi_prem_cap) * esc_take_up                       # noqa: F821


def cover_pp(t):
    """SA(t): the sum assured or cash sum in force in month t.

    Steps at policy anniversaries.  On the RPI variant the cash sum **continues to
    index after premiums cease at 90**, which is why this carries no cessation test -
    the premium step, being applied to a zero premium, stops of its own accord.
    """
    return sum_assured() * (1.0 + esc_cover_step()) ** (policy_year(t) - 1)


def premium_pp(t):
    """P(t): the monthly premium due at the beginning of month t.

    Zero once the premium cessation month has passed, and zero on a paid-up policy -
    which is carried as a separate population strand rather than as a premium of zero,
    so it does not appear here.
    """
    if cessation_mths() > 0 and t > cessation_mths():
        return 0.0
    return premium_mth() * (1.0 + esc_prem_step()) ** (policy_year(t) - 1)


def prem_cum_pp(t):
    """CumPrem(t): cumulative premiums paid per policy to the end of month t.

    The premium falls at the beginning of the month and death at the end, so a death in
    month t has had the month-t premium paid on it - which is why the moratorium refund
    at ``t = 1`` is one month's premium and not nothing.  This is the **refund base**: a
    year-one non-accidental claim pays cumulative premiums paid, not the cash sum and
    not an annualized premium.
    """
    if t <= 0:
        return 0.0
    return prem_cum_pp(t - 1) + premium_pp(t)


def in_moratorium(t):
    """Whether month t falls inside the over-50s moratorium; always False on the UW cell."""
    return t <= moratorium_mths()


def payments_made(t):
    """N_paid(t): the number of monthly payments made by the end of month t."""
    if cessation_mths() <= 0:
        return t
    return min(t, cessation_mths())


def payments_expected():
    """N_expected: the payments expected over the premium-paying period.

    The pro-rata paid-up denominator, so it is the cessation month; zero where premiums
    are payable for life, in which case the variant does not apply.
    """
    return cessation_mths()


def pu_eligible(t):
    """Whether a would-be lapse in month t converts to paid-up instead of terminating.

    The pro-rata paid-up rule: at least half the expected payments must have been made
    [S9].  Before that halfway point a lapse is a total loss and the base lapse rate
    applies; after it, forfeiture is strictly dominated, so **all** would-be lapses are
    assumed to convert **[std]**.
    """
    if not pu_variant():
        return False
    return payments_made(t) >= payments_expected() / 2.0


def crossover_mth():
    """t*: the first month in which cumulative premiums exceed the cover in force.

    ``floor(SA/P) + 1`` under level premiums - 167 months, thirteen years and eleven
    months, on the anchor cell, which is the FCA's stylised example exactly - but
    searched rather than closed-form so that an escalating variant still resolves.
    Returns 0 where the crossover never happens, which is the case whenever the cash sum
    exceeds the total premiums payable to cessation.

    Reported, not acted on: the crossover-aware lapse module that would raise lapse past
    the tipping point is a pure stress dial and is off in the base run.
    """
    last = cessation_mths() if cessation_mths() > 0 else proj_len()
    for t in range(1, last + 1):
        if prem_cum_pp(t) > cover_pp(t):
            return t
    return 0


def lapse_rate_base(t):
    """The table annual lapse rate in month t **[std]**, before the crossover stress.

    Read from the cell's own row of the lapse table; policy years beyond the table take
    its last row.  Both tables are drafting constructions - no public UK whole of life
    lapse study was retrieved - and on a product with no surrender value they are the
    single largest lever on the liability.
    """
    tbl = data.lapse_table().loc[cell()]                             # noqa: F821
    y = policy_year(t)
    return float(tbl.loc[min(y, int(tbl.index.max())), "lapse_rate"])


def lapse_rate(t):
    """w(y): the annual lapse rate applying at the end of month t.

    **Zero once premiums have ceased**: there is nothing left to stop paying, and
    applying a lapse decrement there silently destroys liability - the notes list it as
    a pitfall.  Otherwise the table rate, optionally stressed by
    ``1 + beta`` past the crossover, which is off in the base run.
    """
    if cessation_mths() > 0 and t > cessation_mths():
        return 0.0
    w = lapse_rate_base(t)
    if lapse_crossover_beta > 0.0 and prem_cum_pp(t) > cover_pp(t):  # noqa: F821
        w = w * (1.0 + lapse_crossover_beta)                         # noqa: F821
    return min(1.0, w)


def lapse_rate_mth(t):
    """w_m(y) = 1 - (1 - w)^(1/12): the monthly lapse rate **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """l(t-1): full-cover policies in force at the **start** of policy month t.

    The notes' in-force probability, and the column their worked-example table prints.
    Paid-up policies are **not** counted here: they are a separate strand,
    :func:`pols_pu`, because their benefit is a reduced amount.  On every model point
    without the pro-rata paid-up variant the two coincide with :func:`pols_all`.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return pols_if_init()
    return (pols_if(t - 1) * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1)))


def pols_pu(t):
    """Paid-up policies in force at the start of month t.

    Zero without the pro-rata paid-up variant.  Paid-up policies pay no premium, carry no
    lapse decrement and do not escalate, so they roll forward on mortality alone and take
    conversions in from the full-cover strand.
    """
    if t < 1 or t > proj_len() or not pu_variant():
        return 0.0
    if t == 1:
        return 0.0
    return pols_pu(t - 1) * (1.0 - mort_rate_mth(t - 1)) + pols_convert(t - 1)


def pu_benefit(t):
    """The aggregate paid-up cover in force at the start of month t.

    Carrying the aggregate benefit alongside the count is what removes the need for a
    per-conversion cohort dimension: the paid-up payout depends on when the policy
    converted, but every paid-up policy thereafter rolls forward on the same survival
    factor, so the sum of their payouts satisfies the same recursion as the count.
    Death outgo on the strand is then ``pu_benefit(t) x q_m(t)``.
    """
    if t < 1 or t > proj_len() or not pu_variant():
        return 0.0
    if t == 1:
        return 0.0
    return (pu_benefit(t - 1) * (1.0 - mort_rate_mth(t - 1))
            + pols_convert(t - 1) * benefit_pp(t - 1, "PAID_UP"))


def pols_all(t):
    """All policies in force at the start of month t: full cover plus paid-up.

    The weight on the maintenance expense, and the count the roll-forward closes on.
    """
    return pols_if(t) + pols_pu(t)


def pols_if_at(t, timing):
    """The number of full-cover policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement; :func:`pols_if`.

    ``"BEF_LAPSE"``
        after deaths, before lapses - the notes' processing order is
        **death before lapse** **[std]**.

    ``"AFT_DECR"``
        the notes' ``l(t)``, the end-of-month count.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        if t < 1 or t >= proj_len():
            return 0.0
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths on full cover at the end of month t, against the start-of-month in-force."""
    return pols_if(t) * mort_rate_mth(t)


def pols_death_pu(t):
    """Deaths on paid-up cover at the end of month t; zero without the pro-rata paid-up value."""
    return pols_pu(t) * mort_rate_mth(t)


def pols_exit(t):
    """Would-be lapses at the end of month t, taken from the survivors of mortality.

    What happens to them depends on :func:`pu_eligible`: they either terminate for
    nothing or convert to paid-up.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_convert(t):
    """Would-be lapses converted to paid-up at the end of month t.

    All of them once the pro-rata paid-up halfway point is passed **[std]**, none before
    it, and none at all without the variant.  A state change, not a cash flow.
    """
    return pols_exit(t) if pu_eligible(t) else 0.0


def pols_lapse(t):
    """Lapses that actually terminate the policy at the end of month t.

    **Pays nothing.** There is no surrender value at any duration on either cell, so
    this moves :func:`pols_if` and produces no cash flow whatever - which is the
    arithmetic meaning of a lapse-supported product.
    """
    return pols_exit(t) - pols_convert(t)


def pols_maturity(t):
    """Policies still in force when the projection is truncated at the limiting age.

    Not a maturity - whole of life has none - and not a benefit: it pays nothing.  It is
    the truncation residual, non-zero only in the last projected month, and it exists so
    that the roll-forward closes there.  :func:`check_truncation` asserts it is
    negligible, which is the substantive statement: a limiting age set too low would
    drop liability off the end of the projection instead.
    """
    if t != proj_len():
        return 0.0
    return (pols_all(t) - pols_death(t) - pols_death_pu(t) - pols_lapse(t))


def benefit_pp(t, kind):
    """The benefit amount per policy in month t, by kind.

    ``"NON_ACC"``
        the non-accidental death benefit.  On the O50 cell it is
        ``CumPrem(t)`` inside the moratorium and the cash sum after it; on
        the UW cell it is the sum assured, with the suicide refund handled
        under ``"DEATH"``.

    ``"ACC"``
        the accidental death benefit: the full cash sum from day one, and
        ``k_adb`` times it past the moratorium.  On the UW cell there is no
        accidental split, so this is the sum assured.

    ``"DEATH"``
        the expected benefit per death on the full-cover strand, blending the
        two above by the accidental share on O50, and the sum assured with
        the suicide refund by the suicide share inside the first twelve
        months on UW.  This is what :func:`claims` multiplies by.

    ``"PAID_UP"``
        the pro-rata paid-up payout for a policy converting in month t,
        ``SA x N_paid / N_expected``.  Zero without the variant.
    """
    if kind == "NON_ACC":
        if cell() == "O50" and in_moratorium(t):
            return prem_cum_pp(t)
        return cover_pp(t)
    if kind == "ACC":
        if cell() != "O50":
            return cover_pp(t)
        if in_moratorium(t):
            return cover_pp(t)
        return adb_multiplier() * cover_pp(t)
    if kind == "DEATH":
        if cell() == "O50":
            return ((1.0 - acc_share) * benefit_pp(t, "NON_ACC")     # noqa: F821
                    + acc_share * benefit_pp(t, "ACC"))              # noqa: F821
        if t <= suicide_mths:                                        # noqa: F821
            return ((1.0 - suicide_share) * cover_pp(t)              # noqa: F821
                    + suicide_share * prem_cum_pp(t))                # noqa: F821
        return cover_pp(t)
    if kind == "PAID_UP":
        if not pu_variant():
            return 0.0
        return cover_pp(t) * payments_made(t) / payments_expected()
    raise ValueError("invalid kind")


def premiums(t):
    """E[premium](t): premium income at the beginning of month t, an inflow.

    Carried on the full-cover strand only: paid-up policies pay nothing, and neither do
    over-50s policies past cessation, where :func:`premium_pp` is already zero.
    """
    return premium_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Death outgo in month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        outgo on the full-cover strand, ``deaths x benefit_pp(t, "DEATH")``.

    ``"DEATH_PU"``
        outgo on the paid-up strand, ``pu_benefit(t) x q_m(t)`` - the
        aggregate paid-up cover times the monthly mortality rate, which is
        why the strand carries a benefit total as well as a count.

    ``"LAPSE"``
        zero, always.  There is no surrender value at any time on either
        cell; the kind exists so the zero is stated rather than inferred.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "DEATH_PU", "LAPSE"))
    if kind == "DEATH":
        return pols_death(t) * benefit_pp(t, "DEATH")
    if kind == "DEATH_PU":
        return pu_benefit(t) * mort_rate_mth(t)
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def expense_acq_pp():
    """The acquisition expense per policy at issue **[std]**: £150 on O50, £300 on UW."""
    return expense_acq_o50 if cell() == "O50" else expense_acq_uw    # noqa: F821


def expense_maint_pp():
    """The annual maintenance expense per policy **[std]**: £30 on O50, £50 on UW.

    Premiums are level and small - £30 a month on the anchor cell - while this inflates,
    so the expense margin erodes mechanically over a twenty-year-plus horizon.  A
    per-policy expense error compounds accordingly.
    """
    return expense_maint_o50 if cell() == "O50" else expense_maint_uw  # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y - 1)`` **[std]**.

    Steps on policy anniversaries, not monthly, which is how the notes write it.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**.

    The acquisition charge falls once, at issue.  Maintenance is carried on
    :func:`pols_all`, so a paid-up policy still costs money to administer even though it
    pays no premium - which is part of why the pro-rata paid-up variant is expensive.
    """
    acq = expense_acq_pp() * pols_if(t) if t == 1 else 0.0
    return acq + expense_maint_pp() / 12.0 * inflation_factor(t) * pols_all(t)


def commissions(t):
    """Initial commission in month t **[std]**: a share of the first year's premiums.

    The existence of commission is sourced - an intermediary is "paid by commission as a
    percentage of total annual premium" - and the level is a standardization.
    """
    if policy_year(t) > 1:
        return 0.0
    return comm_init_rate * premiums(t)                              # noqa: F821


def net_cf(t):
    """CF(t): the net cash flow of month t, **income positive**.

    Premiums less death outgo, expenses and commission.  The notes' own sign and the
    library-wide one, so there is no outgo-positive ``liability_cf`` companion.

    Note that the notes' worked-example table prints premium income and death outgo as
    separate positive columns and omits expenses "for clarity", so ``net_cf`` will not
    equal any column of that table.  Lapse contributes nothing at all: it moves
    :func:`pols_if` and pays no cash.
    """
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_all(t) - pols_all(t+1)`` less deaths from both strands, lapses that actually
    terminate, and the truncation residual in the last month.  Conversions to paid-up
    are absent because they move policies *between* strands rather than out of the
    population - which is the point of running the check on the total.
    """
    return (pols_all(t) - pols_all(t + 1)
            - pols_death(t) - pols_death_pu(t) - pols_lapse(t)
            - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives
    the signed residual of the month that failed.  The tolerance scales with
    ``pols_if_init()``, since the residual accumulates rounding on that many policies.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(1, proj_len() + 1))


def check_truncation():
    """True when the population left at the limiting age is negligible.

    Whole of life has no maturity date, so the projection ends at a limiting age rather
    than at a contractual one, and anything still in force there is liability dropped
    off the end.  The shipped mortality tables reach 1 well before ``omega_age``, so the
    residual should be vanishing; if it is not, the limiting age is too low and the
    model is understating the tail rather than merely rounding it.
    """
    return pols_maturity(proj_len()) <= 1e-9 * max(pols_if_init(), 1.0)


def result_cf():
    """Result table of cashflows, indexed by policy month t.

    ``pols_if`` is the full-cover count at the start of the month, which is the weight
    on premium income and on full-cover death outgo; ``pols_pu`` is the paid-up strand,
    empty on every model point without the pro-rata paid-up variant.  ``claims_lapse`` is
    a column of zeros by product design - there is no surrender value - and is published
    rather than dropped.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_pu": [pols_pu(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_death_pu": [claims(t, "DEATH_PU") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts, benefits and rates, indexed by policy month t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_pu": [pols_pu(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_convert": [pols_convert(t) for t in ts],
            "prem_cum_pp": [prem_cum_pp(t) for t in ts],
            "cover_pp": [cover_pp(t) for t in ts],
            "benefit_death_pp": [benefit_pp(t, "DEATH") for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_loading_o50 = 1.2

mort_loading_uw = 1.0

mort_improvement = 0.0

acc_share = 0.03

suicide_share = 0.01

suicide_mths = 12

rpi_rate = 0.03

esc_fixed_cover = 0.05

esc_fixed_prem = 0.1

esc_rpi_cover_cap = 0.1

esc_rpi_prem_mult = 1.5

esc_rpi_prem_cap = 0.15

esc_take_up = 1.0

lapse_crossover_beta = 0.0

expense_acq_o50 = 150.0

expense_acq_uw = 300.0

expense_maint_o50 = 30.0

expense_maint_uw = 50.0

inflation_rate = 0.03

comm_init_rate = 0.25

pd = ("Module", "pandas")