# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.Rente_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked-example scenario
    >>> Projection.point_id = 2            # the same contract, probability-weighted

``t`` counts **months from the effective date**, 0-based: ``t = 0`` is the first
projected month — the first whole civil month of service, at the end of which the first
*arrérage* falls due — and the frame is ``t = 0, 1, …, proj_len() - 1``. Month t runs
from time t to time t + 1, so ``duration(t) = t // 12`` completed policy years have run
at its start and ``policy_year(t) = t // 12 + 1``.

Survival is carried on the **time-point** clock rather than on the period one:
``lives_if(k, life)`` is the probability that a life is alive **at time k**, with
``k = 0`` at the effective date and ``lives_if(0, life) = 1``. Month t therefore opens
at ``lives_if(t, life)`` and closes at ``lives_if(t + 1, life)`` — which is what
:func:`payment_surv_mth` selects between — and nothing is indexed before time 0.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/rente_viagere/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Rente_FR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Rente_FR_S.Data`, reached here through the ``data`` Reference:

======================  ====================================  ========================
Reference               Cells                                 File
======================  ====================================  ========================
model_point_file        data.model_point_table()              model_point_table.csv
mort_table_file         data.mort_table()                     mort_table.csv
reversion_coeff_file    data.reversion_coeff_table()          reversion_coeff_table.csv
======================  ====================================  ========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and follow :mod:`.PA_UK_S` and :mod:`.SPIA_US_S`
— this library's UK and US payout chassis — wherever the three products share machinery,
so that the same concept has the same name whichever country's model a reader opens. The
technical notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the cells argument)            Month from the effective date,
                                                           0-based
(none)                     duration(t)                     Completed policy years
(none)                     duration_mth(t)                 Months elapsed at start of month t
(none)                     policy_year(t)                  Policy year containing month t
C                          purchase_price()                *Capital constitutif*
Y0, M0                     effective_year(),               Calendar year and civil month
                           effective_month()               of the effective date
k(t)                       cal_year_index(t)               Completed 31 Decembers
(none)                     calendar_year(t)                Calendar year of month t
(none)                     civil_month(t)                  Civil month of month t
x_a0, x_r0                 age_at_entry(life)              Entry ages (ALB), life 1 or 2
x_a(t), x_r(t)             age(t, life)                    Attained age (ALB)
g_a, g_r                   birth_year(life)                *Millésimes*
(none)                     sex(life)                       M, F or mix
rho                        annuity_rate()                  *Taux de rente*
kappa                      option_coeff()                  Definitive option coefficient
(reversion table)          reversion_coeff()               *Réversion* coefficient [S6]
(guarantee)                guarantee_coeff()               *Annuités garanties* coefficient
delta                      reversion_pct()                 *Taux de réversion*
n                          guarantee_mths()                *Annuités garanties*, in months
i                          technical_rate()                *Taux technique*
m                          payment_freq()                  Payments per year
timing                     payment_timing()                arrears or advance
T                          is_payment_mth(t)               Month t is a payment date
(payment point)            payment_surv_mth(t)             Time survival is measured at
nu                         revalo_rate                     Revalorisation rate
R(t)                       revalo_factor(t)                Cumulative revalorisation index
Pi(t)                      palier_factor(t)                *Palier* step multiplier
A0                         annual_income_init()            Gross annual *rente* at conversion
A(t)                       annual_income(t)                Gross annual *rente* in force
A(t)/m                     annuity_pp(t)                   Scheduled *arrérage*
h(t)                       mths_since_payment(t)           Complete months since last payment
(prorata)                  prorata_pp(t)                   Accrued *prorata d'arrérages*
q(s, g, x)                 mort_rate_at_age(...)           Generational table lookup
q(t, life)                 mort_rate(t, life)              Annual rate applied to a life
q_mth                      mort_rate_mth(t, life)          Monthly rate 1-(1-q)^(1/12)
theta                      portfolio_male_share            **[std]** portfolio mix
(none)                     mort_basis()                    table or scenario run **[std]**
(none)                     death_mth(life)                 Scenario month of death **[std]**
l_a(t), l_r(t)             lives_if(t, life)               Survival probability to time t
d_a(t), d_r(t)             lives_death(t, life)            Death density of month t
gamma(t)                   certain_floor(t)                Annuity-certain floor indicator
max(gamma, l_a)            payment_factor(t)               Annuitant stream's factor
(none)                     payment_factor_life(t)          l_a alone, before the floor
delta(1-l_a)l_r            reversion_factor(t)             *Réversion* stream's factor
(prorata factor)           prorata_factor(t)               Death-settlement factor
G(t)                       cum_annuity_pp(t, kind)         Cumulative gross *arrérages*
(tariff factor)            annuity_factor(table_sex)       Annuity factor at conversion
(none)                     taux_rente_tariff()             *Taux de rente* the table implies
(none)                     taux_rente_own_table()          The same on the life's own table
(none)                     unisex_gap()                    Cost of the unisex rule
omega                      omega_age                       Limiting age, 120
(stopping rule)            horizon_mths()                  Months to the age stop rule
(none)                     proj_len()                      Projection length in months
IF(t)                      pols_if(t)                      Any payment obligation open
(none)                     pols_if_init()                  Contracts in force at outset
E[ANN(t)]                  annuity_payments(t)             Expected *arrérages* outgo
E[PRO(t)]                  claims(t, "PRORATA")            *Prorata d'arrérages* on death
E[FRA(t)]                  arrerage_charges(t)             *Frais d'arrérages* retained
E[EXP(t)]                  expenses(t)                     Maintenance expense
c_e, pi                    expense_maint, inflation_rate   Expense level and inflation
CF(t)                      liability_cf(t)                 Total gross liability outgo
(none)                     net_cf(t)                       -liability_cf(t), insurer sign
=========================  ==============================  ==========================

Five names needed care.

``kappa`` is one symbol for two different coefficients. The notes carry it as a model
point attribute; here it is **derived**, because both of its values are derivable and a
derived coefficient cannot drift out of step with the table that implies it.
:func:`reversion_coeff` reads the published [S6] age-difference table shipped as a CSV,
and :func:`guarantee_coeff` computes the certain-period loading off the tariff table.
:func:`option_coeff` is the one the conversion applies, and it is 1 when no option is
elected.

``q`` is used for two different objects: the **tariff** rate, which is the more prudent
single table for every life, and the **best-estimate** rate, which is the life's own
table. They are separate objects here — :func:`mort_rate_at_age` takes the table as an
argument, :func:`mort_rate` is the best estimate for a covered life, and
:func:`annuity_factor` takes the table it is priced on. Collapsing them destroys the
unisex mechanic; see below.

``l`` denotes two different survival paths as well. :func:`lives_if` is the *projection*
path of a covered life on the best-estimate basis, and it honours the scenario switch;
:func:`tariff_lives` is the annuitant's survival on a *pricing* table, and it does not.
They are different objects and the model keeps them apart.

``pols_if`` is not a policy count in the usual sense. It is the notes' ``IF(t)``, the
probability that *any* payment obligation remains — the guarantee certain, the annuitant
alive, or the reversion stream in payment — and it exists to carry the maintenance
expense. The name is kept because it is what the rest of the library calls the expense
weight.

There is **no** ``lapse_rate``, ``improve_factor``, ``improve_rate``, ``surr_charge`` or
``av_pp_at`` of any kind, and the absence of each is deliberate; see below.

.. rubric:: The table is generational, so there is no improvement scale

``mort_rate(t, life)`` is a **pure table lookup**::

    q(t, life) = mort_rate_at_age(sex(life), birth_year(life), age(t, life))

with no factor of any kind applied on top of it and no calendar-year argument. TGH05 and
TGF05 are prospective generation tables: ``q(sex, generation, age)`` already gives the
rate the life will experience at that age, in calendar year ``generation + age``. The
trend is inside the table. An improvement scale on top of it — which the UK sibling
needs, because its ONS base table is a *period* table — would double-count the trend, so
this model has no ``improve_factor`` cells and must not acquire one.

The *millésime* is a model point attribute and is **never derived from the projection
year**. A period-table implementation reads the rate for age 66 in calendar year 2027 and
walks diagonally across generations; a generational one reads ``(g = 1961, x = 66)``
whatever the projection year. Two model points with the same entry age and different
*millésimes* must therefore give different rates at the same attained age, and the tests
assert exactly that.

.. rubric:: The tariff table and the best-estimate table are different objects

The Code forces the single table applied to all lives to be the more prudent of the two,
which for an annuity is the female table; the shipped ``tariff_table_sex`` is ``"F"``.
The projection meanwhile decrements each life on its **own** table, or on a **[std]**
portfolio blend at ``portfolio_male_share`` where the model point carries ``mix``. For a
male annuitant the two differ by construction, and the gap — :func:`unisex_gap`, about
13% of income on the shipped anchor — is the systematic technical surplus that the
eight-year profit-sharing rule requires to flow back to policyholders, which in this
model it does through the revalorisation rate ``nu``. Pricing a male life on the female
table *and* projecting him on it makes the prudence margin invisible; projecting him on
the male table without crediting the surplus back shows a permanent retained profit the
rule does not allow.

.. rubric:: Two mortality bases: table and scenario

The notes' worked example is not a probability-weighted run. It is a **scenario**: "the
annuitant dies in month 25 — the 26th month of service — and the reversionary survives
throughout", evaluated at ``l_a = 0`` from time 26 and ``l_r = 1`` throughout. The rest
of the notes projects on an expected basis. Both readings are shipped, and which one applies is a model point
column — the same device :mod:`.PA_UK_S` and :mod:`.SPIA_US_S` use for the same reason:

``mort_basis = "table"``
    ``lives_if`` runs the monthly recursion off the shipped generational table. Model
    points 2, 4, 5, 7, 8, 9, 10 and 11; point 2 is the worked configuration on this basis
    and is the run to read for a realistic cash flow shape.

``mort_basis = "scenario"`` **[std]**
    ``lives_if(t, life)`` is the deterministic step function ``1{t <= death_mth(life)}``
    — survival to time t, so a life dying in month ``d`` is alive at time ``d``, the
    start of that month, and gone from time ``d + 1`` — with a blank or negative
    ``death_mth`` meaning the life survives the whole projection. Model points 1, 3
    and 6, which reproduce the worked example and its variants exactly.

The scenario switch is a **[std]** modelling device, not a product feature; it exists
because the notes' verification anchor is a scenario and retuning assumptions to force a
probability-weighted run onto it would be dishonest. It never reaches the *pricing*
side: :func:`tariff_lives` and :func:`annuity_factor` always run off the table.

.. rubric:: Revalorisation is a calendar event, and it is pro-rated once

``revalo_factor`` steps at each **31 December**, never on a policy anniversary, and the
uplift reaches instalments payable from the following 1 January. The first step is
pro-rated ``nu x (13 - M0)/12`` for the part-year of service, which degenerates to the
full ``nu`` for a 1 January effective date. Both halves are notes' pitfalls: an
anniversary convention holds the annuity at its initial level for twelve months instead
of nine on the worked configuration and shifts every later step by three months, and
dropping the pro-rata overstates the annuity for the whole of its remaining life, because
``R(t)`` is a running product. ``nu`` is floored at zero, which is the only contractual
bound any retrieved document states.

The *frais sur encours de rentes* appear in **no** recursion here, by design: they bite on
the *provision mathématique* and reduce the profit-sharing base — hence ``nu`` — and never
an instalment. Netting them off an instalment would cut the annuitant's income, which no
retrieved contract does.

.. rubric:: The guarantee is a floor, the reversion is a second stream

``payment_factor(t) = max(certain_floor(t), payment_factor_life(t))`` makes the *annuités
garanties* an annuity-**certain floor** rather than a second stream: while the guarantee
runs the full instalment is payable regardless of survival, and an additive construction
would pay ``1 + l_a``. The *réversion* is genuinely a second stream, gated on
``(1 - l_a(t))`` — the annuitant's survival to the **start** of month t — and **not** on
``(1 - l_a(t + 1))``, its survival to the end: the survivor's first instalment falls in
the month *after* the month of death, immediately after the *prorata d'arrérages* has
settled it. Gating on the end of the month pays the reversion and the *prorata* in the
same month, so the month of death is paid ``1 + delta`` times.

The two options are **not cumulative**; :func:`check_options_xor` asserts no model point
carries both, and :func:`option_coeff` raises if one does.

.. rubric:: The month of death is paid in full

``prorata_pp(t)`` is the accrued instalment settled on death. With
``h(t) = t mod (12/m)`` complete months since the last payment date it is
``((h(t) + 1)/(12/m)) x A(t)/m``, so at ``m = 12`` it is exactly **one full instalment** —
the French rule is that instalments cease from the 1st day of the month *following* the
death — and at ``m = 4`` a death in the first month of a quarter settles one third of the
quarterly instalment. The ``(1 - gamma(t))`` gate suppresses it while the guarantee runs,
the full instalment being payable there already, and the second term of
:func:`prorata_factor` is the symmetric settlement on the reversionary's own death. There
is no "with or without proportion" election in France: the *prorata* is the rule. On the
unobserved ``advance`` variant nothing has accrued unpaid at death, so the *prorata* is
zero **[std]**.

.. rubric:: The taux technique is not a discount rate

``i`` reaches the projection **only through** ``rho``: it prices the annuity at
conversion, through :func:`annuity_factor`, and thereafter functions as a lifetime
minimum guaranteed return. It appears in no cash flow recursion and is not a valuation
rate. The best estimate discounts at the risk-free term structure, which this library
does not compute at all — every ``technical-notes.md`` in it specifies *gross* liability
cash flows and leaves discounting and reserves to a layer that consumes them.

.. rubric:: There is no policyholder behaviour to model

No lapse decrement, no dynamic behaviour formulas, no surrender value at any duration, no
alteration of options and no premium flexibility. That is a cited product feature — the
Code gives a *rente viagère* in payment no surrender value at all — and it is why this
model has no ``lapse_rate`` of any kind. The one election that survives conversion is not
a cash flow but an admission test: below the statutory commutation threshold the insurer
may pay a capital instead, with the annuitant's agreement, so there is no annuity to
project, and :func:`check_commutation_floor` rejects such a model point rather than
projecting it. Behaviour otherwise enters the *basis*, not the projection: voluntary
annuitants self-select for longevity, which is already inside an annuitant-experience
table, and the unisex tariff deters male annuitants, which is the direction of
``portfolio_male_share`` sitting below one half.

.. rubric:: Sign convention

The notes define ``CF(t)`` as total gross liability **outgo**, which is
:func:`liability_cf`. :func:`net_cf` is its negative, the library-wide income-positive
convention, so a ``result_cf()["net_cf"]`` column can be summed or compared across every
model in the library. Both are published as columns rather than one being made to stand
for the other. There is no premium income in the projection at all: the *capital
constitutif* is a pricing input at the effective date, not a projected cash flow. The one
component that runs the other way is :func:`arrerage_charges`, which the insurer
**retains** out of each *quittance*: it is published as a positive column and
**subtracted** in :func:`liability_cf`.
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


def purchase_price():
    """C: the *capital constitutif* actually applied to the annuity.

    For a wrapper exit this is the *valeur atteinte* net of social and tax levies, with
    any entry charge taken before the model starts.  A pricing input at the effective
    date, not a projected cash flow: the projection carries no premium income.  It enters
    the projection only through :func:`annual_income_init`.
    """
    return float(model_point()["purchase_price"])


def effective_year():
    """Y0: the calendar year of the effective date.

    The model carries the calendar and not merely the duration, because revalorisation
    and expense inflation step at 31 December.
    """
    return int(model_point()["effective_year"])


def effective_month():
    """M0: the civil month of the effective date, 1 for January.

    The annuity always takes effect on the 1st day of a civil month, so the effective
    date needs no day part.  M0 fixes the length of the first partial calendar year,
    13 - M0 months, over which the first revalorisation is pro-rated.
    """
    v = int(model_point()["effective_month"])
    if not 1 <= v <= 12:
        raise ValueError("invalid effective_month")
    return v


def age_at_entry(life):
    """x(0): the entry age of the annuitant (``life = 1``) or reversionary (``life = 2``).

    **Age last birthday** at the effective date, chosen to index the shipped
    single-year-of-age generational table **[std]**.  It is not derived from the
    *millésime* and does not derive it: the two are separate attributes, because a table
    keyed on year of birth and an age keyed on birthday do not determine one another
    inside a calendar year.
    """
    if life == 1:
        return int(model_point()["annuitant_age"])
    if life == 2 and reversion_pct() > 0.0:
        return int(model_point()["reversion_age"])
    raise ValueError("invalid life")


def birth_year(life):
    """g: the *millésime* of ``life``, the generational table's key.

    **Never derived from the projection year.**  The table is generational, so the rate
    a life experiences at an attained age depends on the year it was born and on nothing
    else about the calendar.
    """
    if life == 1:
        return int(model_point()["annuitant_birth_year"])
    if life == 2 and reversion_pct() > 0.0:
        return int(model_point()["reversion_birth_year"])
    raise ValueError("invalid life")


def sex(life):
    """The best-estimate table of ``life``: ``M``, ``F`` or ``mix``.

    ``mix`` is the **[std]** portfolio blend of assumption (vi), for a model point that
    stands for a cohort rather than a person.  This selects the **best-estimate** table
    only; the tariff is ``tariff_table_sex`` for every life, whatever this returns.
    """
    if life == 1:
        v = model_point()["annuitant_sex"]
    elif life == 2 and reversion_pct() > 0.0:
        v = model_point()["reversion_sex"]
    else:
        raise ValueError("invalid life")
    if v not in ("M", "F", "mix"):
        raise ValueError("invalid sex")
    return v


def annuity_rate():
    """rho: the *taux de rente* struck at conversion, per unit of capital per annum.

    A model point attribute, because it is what a real *barème* quotes and no French
    insurer publishes one.  Every shipped model point carries the rate the shipped tariff
    table implies at its own age, *millésime* and *taux technique*, rounded to six
    decimals; :func:`check_taux_rente` asserts that agreement, and
    :func:`taux_rente_tariff` is the derivation.
    """
    return float(model_point()["annuity_rate"])


def reversion_pct():
    """delta: the *taux de réversion*; 0 where no *réversion* is elected.

    The survivor receives delta times the *rente atteinte* at death, for life, from the
    1st day of the month following it.  Mutually exclusive with the *annuités garanties*
    in the representative design.
    """
    v = model_point()["reversion_pct"]
    return 0.0 if pd.isna(v) else float(v)                           # noqa: F821


def guarantee_mths():
    """n: the *annuités garanties* in months, 0 or 60 to 300 in 60-month steps.

    Instalments are certain for n months to the designated beneficiaries, at the same
    amount and rising with the same revalorisation index.  No lump-sum commutation of the
    remaining term is offered.
    """
    return 12 * int(model_point()["guarantee_years"])


def palier_scheme():
    """The *rente par paliers* scheme: ``none``, ``inc1``, ``inc2``, ``dec1`` or ``dec2``.

    A *rente par paliers* is a level-within-step function of duration, not an escalation:
    nothing compounds and the steps are contractual percentages of the initial level.
    """
    v = model_point()["palier_scheme"]
    if v not in ("none", "inc1", "inc2", "dec1", "dec2"):
        raise ValueError("invalid palier_scheme")
    return v


def palier_step_years():
    """S: the length of the first *palier* step in years, 5 or 10; 0 when none.

    The second step is "d'une durée égale" to the first, which is why one number
    parameterizes both.
    """
    v = int(model_point()["palier_step_years"])
    if palier_scheme() == "none":
        return 0
    if v not in (5, 10):
        raise ValueError("invalid palier_step_years")
    return v


def payment_freq():
    """m: payments per year, in {12, 4, 2, 1}."""
    v = int(model_point()["payment_freq"])
    if v not in (12, 4, 2, 1):
        raise ValueError("invalid payment_freq")
    return v


def payment_timing():
    """Whether instalments fall in *arrears* (*terme échu*) or in *advance*.

    Every retrieved French carrier pays *terme échu*; ``advance`` is retained as an
    unobserved model variant only.  Arrears instalments require survival at the end of
    the payment month and advance instalments at the start of it; using end-of-period
    survival for advance payments understates the liability by roughly one period's
    mortality per payment, which is material at annuitant ages.
    """
    v = model_point()["payment_timing"]
    if v not in ("arrears", "advance"):
        raise ValueError("invalid payment_timing")
    return v


def arrerage_charge_rate():
    """f: the *frais d'arrérages* retained out of each gross *quittance*.

    A percentage of the payment, deducted per *quittance d'arrérages* and not off the
    annualised *rente*.  At a flat percentage the two coincide; at a per-instalment cap or
    a flat per-instalment fee they do not, and the payment frequency then changes the
    total.  Ranges from 0.00% to 3% across the retrieved carriers.
    """
    return float(model_point()["arrerage_charge_rate"])


def technical_rate():
    """i: the *taux technique* the *taux de rente* was struck on.

    It reaches the projection **only through** rho, by way of :func:`annuity_factor`, and
    appears in no cash flow recursion.  It is **not** a discount rate: the best estimate
    discounts at the risk-free term structure, and reusing i for that produces neither a
    price nor a reserve.  It is carried so a reader can see which rate rho was struck on.
    """
    return float(model_point()["technical_rate"])


def mort_basis():
    """Whether the run is probability-weighted (*table*) or deterministic (*scenario*).

    *table* runs the monthly recursion off the shipped generational table; *scenario*
    **[std]** replaces it with the step function ``1{t <= death_mth(life)}`` so the notes'
    worked example - which is a scenario, not an expectation - reproduces exactly.  It
    never reaches the pricing side.  See the Space docstring.
    """
    v = model_point()["mort_basis"]
    if v not in ("table", "scenario"):
        raise ValueError("invalid mort_basis")
    return v


def death_mth(life):
    """The scenario month of death of ``life``; -1 if the life survives throughout.

    Read only when ``mort_basis() == "scenario"``.  The month index is on the projection
    frame's own 0-based clock, so the shipped worked example dies in month 25, the 26th
    month of service.  A blank cell in the model point table means the life never dies in
    the scenario and is returned as -1, a value no month can take: with ``t`` 0-based,
    month 0 is a projectable event and cannot double as the sentinel.  A death in month d
    is decremented at the end of that month, so ``lives_if(t, life)`` - survival to time t
    - is 0 from ``t = d + 1`` and the *arrérage* of month d is nevertheless due in full,
    as the *prorata*.
    """
    v = model_point()["death_mth_1" if life == 1 else "death_mth_2"]
    return -1 if pd.isna(v) else int(v)                              # noqa: F821


def pols_if_init():
    """Initial number of contracts in force; 1.0 on a single-contract model point."""
    return float(model_point()["pols_if_init"])


def duration(t):
    """Completed policy years at the start of month t: ``duration_mth(t) // 12``.

    0-based, as ``duration`` is throughout lifelib: 0 through the first policy year.
    """
    return duration_mth(t) // 12


def duration_mth(t):
    """Months elapsed from the effective date at the start of month t; equal to t.

    ``t`` is 0-based and counted from the effective date, so the identity is trivial - the
    cells exists so the monthly models in this library share one vocabulary, and so that
    ``duration(t) = duration_mth(t) // 12`` reads as lifelib writes it.
    """
    return t


def policy_year(t):
    """The policy year containing month t; 1 for t = 0..11.

    Nothing in this product happens on a policy anniversary: the *paliers* and the
    attained ages step on 12-month multiples of the effective date, and revalorisation
    and expense inflation step at 31 December.  The cells exists for the shared
    vocabulary and for the *palier* boundaries.
    """
    return duration(t) + 1


def age(t, life):
    """The attained age (ALB) of ``life`` in month t: ``x(0) + t // 12`` **[std]**.

    Age increments on each 12-month multiple of the effective date, not on a birthday:
    the model point carries an age last birthday at the effective date and a *millésime*,
    and neither fixes the birthday within the year.
    """
    return age_at_entry(life) + duration(t)


def calendar_year(t):
    """The calendar year containing month t.

    Derived from the effective date's year and civil month, ``Y0 + (M0 + t - 1) // 12``,
    ``t`` being 0-based so that month 0 is the civil month of the effective date itself.
    It is **not** an argument to any mortality lookup: the table is generational.
    """
    return effective_year() + (effective_month() + t - 1) // 12


def civil_month(t):
    """The civil month containing month t, 1 for January."""
    return (effective_month() + t - 1) % 12 + 1


def cal_year_index(t):
    """k(t): completed 31 Decembers strictly before the start of month t.

    The annuity is in service for ``13 - M0`` months of its first calendar year - months
    ``t = 0 .. 12 - M0`` on the 0-based clock - so ``k(t) = 0`` while ``t < 13 - M0`` and
    ``1 + (t - (13 - M0)) // 12`` afterwards.  It counts 31 Decembers **strictly before**
    month t, because the uplift credited at 31 December reaches instalments payable from
    the following 1 January.  :func:`check_calendar_index` asserts that this agrees with
    the calendar the model carries independently, ``calendar_year(t) - Y0``.
    """
    first = 13 - effective_month()
    if t < first:
        return 0
    return 1 + (t - first) // 12


def mort_rate_at_age(table_sex, gen, x):
    """q(s, g, x): the annual mortality rate of the shipped generational table.

    A **pure table lookup** keyed on sex, *millésime* and attained age - no improvement
    factor, no rating factor, no calendar-year argument.  Rates at and above the limiting
    age are 1.  ``table_sex = "mix"`` returns the **[std]** portfolio blend
    ``theta q(M) + (1 - theta) q(F)``, which is a best-estimate device for a model point
    standing for a cohort and is never a tariff basis.
    """
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    if table_sex == "mix":
        return (portfolio_male_share * mort_rate_at_age("M", gen, x)  # noqa: F821
                + (1.0 - portfolio_male_share)                       # noqa: F821
                * mort_rate_at_age("F", gen, x))
    if table_sex not in ("M", "F"):
        raise ValueError("invalid table_sex")
    return float(data.mort_table().loc[(table_sex, gen, x), "mort_rate"])  # noqa: F821


def mort_rate(t, life):
    """q: the annual best-estimate mortality rate applied to ``life`` in month t.

    ``mort_rate_at_age(sex(life), birth_year(life), age(t, life))`` and nothing else.  The
    table is generational, so the trend is inside it and there is no improvement scale to
    apply on top; the projection year does not enter.  This is the **best-estimate**
    rate, not the tariff rate - see :func:`annuity_factor`.
    """
    return mort_rate_at_age(sex(life), birth_year(life), age(t, life))


def mort_rate_mth(t, life):
    """q_m = 1 - (1 - q)^(1/12): the monthly mortality rate **[std]**.

    Uniform force within the year of age, which is the standard reading of an annual
    table on a monthly grid and is strictly below the annual rate wherever that is
    positive.
    """
    return 1.0 - (1.0 - mort_rate(t, life)) ** (1.0 / 12.0)


def lives_if(t, life):
    """l(t): the probability that ``life`` is alive at **time** t, t = 0 at the outset.

    A **time-point** cells, not a period one: ``l(0) = 1`` at the effective date, month t
    opens at ``l(t)`` and closes at ``l(t + 1)``, and no index is ever negative.  On the
    *table* basis ``l(t) = l(t-1)(1 - q_m(t-1))``, the rate of month ``t - 1`` decrementing
    over that month.  On the *scenario* basis **[std]** the survival path is the step
    function ``1{t <= death_mth(life)}``, with a negative ``death_mth`` meaning the life
    survives the whole projection - which is what the notes' worked example specifies.
    Returns 0 for life = 2 where no *réversion* is elected.
    """
    if life == 2 and reversion_pct() <= 0.0:
        return 0.0
    if t <= 0:
        return 1.0
    if mort_basis() == "scenario":
        d = death_mth(life)
        return 0.0 if (d >= 0 and t > d) else 1.0
    return lives_if(t - 1, life) * (1.0 - mort_rate_mth(t - 1, life))


def lives_death(t, life):
    """d(t) = l(t) - l(t+1): the death density of ``life`` in month t.

    A period quantity built from the two time points month t runs between: the deaths of
    month t are decremented at its end.
    """
    return lives_if(t, life) - lives_if(t + 1, life)


def tariff_horizon_mths():
    """The months the tariff annuity factor runs over: ``12 (omega - x_a0)``.

    The annuitant's own horizon, not the projection's: an annuity factor is a property of
    the life being priced.
    """
    return 12 * (omega_age - age_at_entry(1))                        # noqa: F821


def tariff_lives(t, table_sex):
    """The annuitant's survival to **time** t on a **pricing** table, t = 0 at conversion.

    A different object from :func:`lives_if`: it runs on whichever table it is asked for,
    it always runs off the table, and it ignores the scenario switch entirely - a
    scenario is a statement about one realisation, and pricing is not.  Like
    :func:`lives_if` it is a time-point cells, and the step from ``t - 1`` to ``t`` takes
    the rate of month ``t - 1``, at the attained age ``age(t - 1, 1)``.
    """
    if t <= 0:
        return 1.0
    q = mort_rate_at_age(table_sex, birth_year(1), age(t - 1, 1))
    return tariff_lives(t - 1, table_sex) * (1.0 - (1.0 - (1.0 - q) ** (1.0 / 12.0)))


def annuity_factor(table_sex):
    """The annuity factor at conversion on ``table_sex``, per unit of annual *rente*.

    ``sum(l(t) v^t) / 12`` over the annuitant's horizon, monthly in arrears, with
    ``v = (1 + i)^(-1/12)`` at the *taux technique*.  This is the **only** place i
    enters the model, and it enters the pricing side, not a cash flow.  At the shipped
    zero *taux technique* the factor is the residual life expectancy of the table.

    The sum runs over the **payment times** ``t = 1 .. 12(omega - x_a0)`` on the pricing
    clock - the instants an arrears instalment falls due, counted from conversion - and
    not over the projection frame's month indices, so it does not move with the frame.
    """
    v = (1.0 + technical_rate()) ** (-1.0 / 12.0)
    return sum(tariff_lives(t, table_sex) * v ** t
               for t in range(1, tariff_horizon_mths() + 1)) / 12.0


def taux_rente_tariff():
    """The *taux de rente* the tariff table implies: ``1 / (a x (1 + loading))``.

    Struck on ``tariff_table_sex`` for **every** life, whatever the annuitant's own sex,
    because the Code requires the single table applied to all lives to be the more
    prudent one.  ``rate_loading`` is the **[std]** margin between the pure factor and the
    quoted rate, at a level no source publishes.  The shipped mortality proxy is anchored
    so that this reproduces the technical notes' placeholder rho exactly at the worked
    configuration's age and *millésime*.
    """
    return 1.0 / (annuity_factor(tariff_table_sex)                   # noqa: F821
                  * (1.0 + rate_loading))                            # noqa: F821


def taux_rente_own_table():
    """The *taux de rente* the annuitant's **own** table would imply.

    The counterfactual the unisex rule forbids.  It is not used in any cash flow; it
    exists so that :func:`unisex_gap` can be read off the model rather than asserted.
    """
    return 1.0 / (annuity_factor(sex(1)) * (1.0 + rate_loading))     # noqa: F821


def unisex_gap():
    """The income a life gives up to the unisex rule, as a fraction of what it receives.

    ``taux_rente_own_table() / rho - 1``.  Positive for a male annuitant - about 13% on
    the shipped anchor - and it is the systematic technical surplus the eight-year
    profit-sharing rule requires to flow back to policyholders, which in this model it
    does through the revalorisation rate.  Negative or zero for a female annuitant, whose
    own table *is* the tariff table.
    """
    return taux_rente_own_table() / annuity_rate() - 1.0


def certain_excess_years():
    """The years of annuity factor the *annuités garanties* add, on the tariff table.

    ``sum((1 - l(t)) v^t) / 12`` over the guaranteed months: the certain-period annuity
    factor exceeds the life factor by exactly the payments made to beneficiaries after a
    death inside the term.  Zero where no guarantee is elected.  Like
    :func:`annuity_factor` this is a pricing sum over payment times ``t = 1 .. n`` and
    not over the projection frame.
    """
    n = guarantee_mths()
    if n <= 0:
        return 0.0
    v = (1.0 + technical_rate()) ** (-1.0 / 12.0)
    return sum((1.0 - tariff_lives(t, tariff_table_sex)) * v ** t    # noqa: F821
               for t in range(1, n + 1)) / 12.0


def guarantee_coeff():
    """The definitive coefficient the *annuités garanties* cost, ``a / (a + excess)``.

    **[std]**: no retrieved document publishes the cost of *annuités garanties*, so it is
    derived here from the tariff table by the only construction the notes give - the
    certain-period factor exceeds the life factor by the payments made after a death
    inside the term.  Derived rather than carried as a model point column so that it
    cannot drift out of step with the table that implies it, and so that a 25-year term
    costs more than a 5-year one, which a single published figure cannot express.
    Substituting a licensed mortality basis therefore moves this coefficient too.
    """
    if guarantee_mths() <= 0:
        return 1.0
    a = annuity_factor(tariff_table_sex)                             # noqa: F821
    return a / (a + certain_excess_years())


def reversion_coeff():
    """The definitive *réversion* coefficient, from the published [S6] table.

    Keyed on the *taux de réversion* and on the difference in *millésime* between the
    reversionary and the annuitant, a positive difference meaning the reversionary is the
    younger life.  The three published columns are 60%, 80% and 100%; a *taux de
    réversion* off that grid has no retrieved coefficient and raises rather than being
    guessed at.  The reduction is **definitive** and applies to the annuitant's own
    annuity once, at conversion: it does not also scale the reversion stream, which is
    delta times the *already reduced* annuity reached at death, and it is not released if
    the reversionary predeceases the annuitant.
    """
    if reversion_pct() <= 0.0:
        return 1.0
    d = birth_year(2) - birth_year(1)
    tbl = data.reversion_coeff_table()                               # noqa: F821
    hit = tbl[((tbl["reversion_pct"] - reversion_pct()).abs() < 1e-9)
              & (tbl["gen_diff_lo"] <= d) & (d <= tbl["gen_diff_hi"])]
    if len(hit) != 1:
        raise ValueError("no published reversion coefficient for this model point")
    return float(hit["reversion_coeff"].iloc[0])


def option_coeff():
    """kappa: the definitive coefficient the elected option costs; 1 with no option.

    The *réversion* coefficient where a *réversion* is elected and the **[std]**
    guarantee coefficient where *annuités garanties* are.  The options are **not
    cumulative**, so exactly one of them may be non-trivial and a model point carrying
    both raises rather than compounding two coefficients.
    """
    if reversion_pct() > 0.0 and guarantee_mths() > 0:
        raise ValueError("reversion and annuites garanties are not cumulative")
    if reversion_pct() > 0.0:
        return reversion_coeff()
    if guarantee_mths() > 0:
        return guarantee_coeff()
    return 1.0


def annual_income_init():
    """A0 = C rho kappa: the gross annual *rente* at conversion.

    Derived, not carried: rho and kappa are the two quantities a real *barème* computes,
    and the model shows the arithmetic rather than taking its answer as an input.
    """
    return purchase_price() * annuity_rate() * option_coeff()


def revalo_factor(t):
    """R(t): the cumulative revalorisation index in month t; R = 1 while k(t) = 0.

    Steps at each **31 December** and reaches instalments payable from the following
    1 January, never on a policy anniversary.  The first step is pro-rated
    ``nu (13 - M0)/12`` for the part-year of service, which degenerates to the full nu
    for a 1 January effective date.  The uplift is floored at zero, the only contractual
    bound any retrieved document states, so R is non-decreasing.  The ``k(t) = 0`` branch
    is the base case of the recursion: it holds over the whole first partial calendar
    year, which always contains month 0, so no month before the first is ever read.
    """
    k = cal_year_index(t)
    if k == 0:
        return 1.0
    if k == cal_year_index(t - 1):
        return revalo_factor(t - 1)
    if k == 1:
        step = revalo_rate * (13 - effective_month()) / 12.0         # noqa: F821
    else:
        step = revalo_rate                                           # noqa: F821
    return revalo_factor(t - 1) * (1.0 + max(0.0, step))


def palier_factor(t):
    """Pi(t): the *rente par paliers* step multiplier; 1 where no scheme is elected.

    A step function of **duration**, not an escalation: nothing compounds, and the steps
    are contractual percentages of the initial level.  The first step runs 12S months -
    ``t = 0 .. 12S - 1`` - and the second, where the scheme has three levels, an equal
    further 12S months.
    """
    scheme = palier_scheme()
    if scheme == "none":
        return 1.0
    if scheme == "inc1":
        steps = (1.0, 2.0)
    elif scheme == "inc2":
        steps = (1.0, 1.25, 1.50)
    elif scheme == "dec1":
        steps = (1.0, 0.50)
    else:
        steps = (1.0, 0.75, 0.50)
    s = 12 * palier_step_years()
    if t < s:
        return steps[0]
    if len(steps) == 2 or t < 2 * s:
        return steps[1]
    return steps[2]


def annual_income(t):
    """A(t) = A0 R(t) Pi(t): the gross annualised *rente* in force in month t.

    **Deterministic** given the assumption set: the annuity level does not depend on
    survival, only the payment factors do.  The *frais sur encours de rentes* are not
    netted from it - they bite on the *provision mathématique* and reduce the
    profit-sharing base, hence nu, and never an instalment.
    """
    return annual_income_init() * revalo_factor(t) * palier_factor(t)


def is_payment_mth(t):
    """Whether month t is a payment date.

    Arrears (*terme échu*): the k-th instalment falls at the end of month
    ``12k/m - 1``, so ``t = 2, 5, 8, ...`` at m = 4.  Advance: it falls one full payment
    period earlier, at the start of month ``12(k-1)/m``, so t = 0, 3, 6, ...  At m = 12
    every month is a payment month on either convention.
    """
    if t < 0:
        return False
    step = 12 // payment_freq()
    if payment_timing() == "arrears":
        return (t + 1) % step == 0
    return t % step == 0


def payment_surv_mth(t):
    """The **time** at which survival is measured for the instalment falling in month t.

    An index into :func:`lives_if`, which is a time-point cells.  Arrears: the end of
    month t, time ``t + 1``.  Advance: the start of month t, time ``t``, because an
    advance instalment falls at the start of the month; 0 for the first instalment, where
    ``lives_if`` is 1.
    """
    return t + 1 if payment_timing() == "arrears" else t


def annuity_pp(t):
    """A(t)/m: the scheduled *arrérage* per contract in month t, zero outside T.

    This is the annuitant's instalment.  The reversionary's is delta times it, on the
    *rente atteinte* - the same schedule - which is what "delta of the annuity reached at
    death" reduces to under a schedule that does not depend on survival.
    """
    if not is_payment_mth(t):
        return 0.0
    return annual_income(t) / payment_freq()


def mths_since_payment(t):
    """h(t) = t mod (12/m): complete months since the last payment date, at the start of t.

    The accrual base of the *prorata d'arrérages*.  At m = 12 it is 0 for every t, so the
    *prorata* is a whole instalment; at m = 4 a death in the first month of a quarter
    gives h = 0 and settles one third of the quarterly instalment, the second month h = 1
    and two thirds.
    """
    return t % (12 // payment_freq())


def prorata_pp(t):
    """The *prorata d'arrérages* accrued and unpaid at a death in month t.

    ``((h(t) + 1)/(12/m)) A(t)/m``: the arrears that have accrued up to and including the
    month of death, which belong to the heirs.  At m = 12 that is exactly **one full
    instalment**, the French rule being that instalments cease from the 1st day of the
    month *following* the death.  Zero on the unobserved ``advance`` variant **[std]**,
    where the instalment covering the month of death was already paid at its start and
    nothing has accrued unpaid.
    """
    if payment_timing() != "arrears":
        return 0.0
    step = 12.0 / payment_freq()
    return (mths_since_payment(t) + 1) / step * annual_income(t) / payment_freq()


def certain_floor(t):
    """gamma(t) = 1{t < n}: the annuity-certain floor of the *annuités garanties*.

    The guarantee covers the n months ``t = 0 .. n - 1`` and is spent from month n.
    """
    return 1.0 if t < guarantee_mths() else 0.0


def payment_factor_life(t):
    """l_a measured at the payment point: the annuitant's survival factor alone."""
    return lives_if(payment_surv_mth(t), 1)


def payment_factor(t):
    """max(gamma(t), l_a): the annuitant stream's payment factor.

    The ``max`` makes the *annuités garanties* an annuity-**certain floor** rather than a
    second stream: while the guarantee runs the full instalment is payable regardless of
    survival, and an additive form would pay ``1 + l_a`` for the whole term.
    """
    return max(certain_floor(t), payment_factor_life(t))


def reversion_factor(t):
    """delta (1 - l_a(t)) l_r: the *réversion* stream's payment factor.

    The gate is ``(1 - l_a(t))``, the annuitant's survival to the **start** of month t,
    and **not** ``(1 - l_a(t + 1))``, its survival to the end: the survivor's first
    instalment falls in the month *after* the month of death, immediately after the
    *prorata d'arrérages* has settled it.  The only source that dates the reversion start
    gives it as the 1st day of the "month **or** quarter" following death, so a one-month
    gate at every payment frequency is a **[std]** reading of its monthly limb - exact at
    m = 12, and up to a quarter early on a quarterly contract.  No shipped model point
    combines a *réversion* with m < 12.  The survivor's own survival is measured at the
    payment point.  Zero where no *réversion* is elected.
    """
    if reversion_pct() <= 0.0:
        return 0.0
    return (reversion_pct() * (1.0 - lives_if(t, 1))
            * lives_if(payment_surv_mth(t), 2))


def prorata_factor(t):
    """The probability-weight of a *prorata d'arrérages* settlement in month t.

    ``d_a(t)(1 - gamma(t)) + delta (1 - l_a(t)) d_r(t)``: the annuitant's own death,
    suppressed while the *annuités garanties* run because the full instalment is already
    payable there, plus the symmetric settlement on the reversionary's death once the
    reversion stream is running - gated, like :func:`reversion_factor`, on the
    annuitant's survival to the **start** of month t.
    """
    res = lives_death(t, 1) * (1.0 - certain_floor(t))
    if reversion_pct() > 0.0:
        res += (reversion_pct() * (1.0 - lives_if(t, 1))
                * lives_death(t, 2))
    return res


def cum_annuity_pp(t, kind):
    """G(t): cumulative gross *arrérages* per contract through month t.

    ``"ANNUITANT"``
        the **deterministic as-if-alive** annuitant schedule, which needs no
        path simulation precisely because it ignores survival.  It is the
        *rente* the contract promises, and it is what a reader should compare
        a *barème* against.

    ``"ALL"``
        the expected total actually paid across both streams, including the
        *prorata* settled on death.  On a probability-weighted run it is an
        *expectation* rather than a path; in a scenario run the two coincide
        for a surviving annuitant.

    Month 0 is the first projected month, so the accumulation opens there rather than
    carrying a month-zero row: ``G(0)`` is what month 0 itself pays.
    """
    prev = 0.0 if t <= 0 else cum_annuity_pp(t - 1, kind)
    if kind == "ANNUITANT":
        return prev + annuity_pp(t)
    if kind == "ALL":
        paid = (annuity_pp(t) * (payment_factor(t) + reversion_factor(t))
                + prorata_pp(t) * prorata_factor(t))
        return prev + paid
    raise ValueError("invalid kind")


def horizon_mths():
    """The number of months over which some covered life is still below the limiting age.

    ``12 (omega - min x_i)``: the notes stop once ``t/12 + x_i > omega`` for every covered
    life, so the months projected are ``t = 0 .. 12(omega - min x_i) - 1``, the last of
    them the last month of age ``omega - 1`` for the youngest life.  Stopping on the
    annuitant's age alone would truncate a younger reversionary's tail.
    """
    ages = [age_at_entry(1)]
    if reversion_pct() > 0.0:
        ages.append(age_at_entry(2))
    return 12 * (omega_age - min(ages))                              # noqa: F821


def proj_len():
    """Projection length in months: the mortality horizon, or the guarantee if longer.

    The **number of months projected**, so the frame is ``range(proj_len())`` and its last
    index is ``proj_len() - 1``.
    """
    return max(horizon_mths(), guarantee_mths())


def annuity_payments(t):
    """E[ANN(t)]: expected *arrérages* outgo in month t.

    ``A(t)/m x [max(gamma, l_a) + delta (1 - l_a) l_r]``, scaled by ``pols_if_init``: the
    annuitant stream with its certain floor, plus the *réversion* stream.
    """
    return (pols_if_init() * annuity_pp(t)
            * (payment_factor(t) + reversion_factor(t)))


def claims(t, kind=None):
    """Expected death-settlement outgo in month t, by kind; the total when kind is omitted.

    ``"PRORATA"``
        the *prorata d'arrérages*: the arrears accrued and unpaid at a death,
        which belong to the heirs.  At m = 12 that is a whole instalment, so
        losing it understates the outgo by one full *arrérage* per death.  It
        is the **only** death benefit this product has: the representative
        design is *capital aliéné*, with no death capital and no refund of any
        part of the *capital constitutif*.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("PRORATA",))
    if kind == "PRORATA":
        return pols_if_init() * prorata_pp(t) * prorata_factor(t)
    raise ValueError("invalid kind")


def arrerage_charges(t):
    """E[FRA(t)]: the *frais d'arrérages* the insurer retains in month t.

    ``f x (E[ANN(t)] + E[PRO(t)])`` - per *quittance*, on every payment including the
    *prorata* settled on death, and **not** on the annualised *rente*.  Published as a
    positive column and **subtracted** in :func:`liability_cf`, because the insurer keeps
    it: it is the one component of this statement that runs the other way.
    """
    return arrerage_charge_rate() * (annuity_payments(t) + claims(t, "PRORATA"))


def pols_if(t):
    """IF(t): the probability that any payment obligation remains in month t.

    ``min(1, max(gamma(t), l_a(t+1)) + 1{delta>0}(1 - l_a(t)) l_r(t+1))`` **[std]** - the
    guarantee certain, the annuitant alive, or the reversion stream in payment.  Survival
    is read at the **end** of month t, the point the arrears instalment is measured at,
    and the reversion leg is gated on the annuitant's survival to its start.  This is
    the weight the maintenance expense is carried on, which is why it keeps the library's
    name for the expense weight even though it is not a policy count.

    Note the one-month gap the notes' own formula produces: in the month of an
    annuitant's death the annuitant leg is already 0 and the reversion leg has not yet
    opened, so no maintenance expense is accrued in that month even though the *prorata*
    is being settled in it.  The formula is implemented as the notes write it rather than
    smoothed, and the gap is one month of a EUR 30 a year expense.
    """
    la = lives_if(t + 1, 1)
    obligation = max(certain_floor(t), la)
    if reversion_pct() > 0.0:
        obligation += (1.0 - lives_if(t, 1)) * lives_if(t + 1, 2)
    return pols_if_init() * min(1.0, obligation)


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^k(t)`` **[std]**.

    It steps at each 31 December like the revalorisation index, but **without** the
    first-year pro-rating: an expense base is restated at a full year's inflation
    whenever the calendar year turns, whereas the pro-rating of the revalorisation is a
    contractual rule about a *rente* in service for part of a year.
    """
    return (1.0 + inflation_rate) ** cal_year_index(t)               # noqa: F821


def expenses(t):
    """E[EXP(t)]: maintenance expense in month t **[std]**.

    ``(c_e / 12)(1 + pi)^k IF(t)``: a round placeholder for in-payment administration,
    paid monthly while any payment obligation remains.  No French insurer publishes
    expense assumptions.  Note that at the composite's 3% *frais d'arrérages* the charge
    on the worked configuration is about EUR 150 a year against this EUR 30, so the French
    charging structure recovers far more than in-payment administration and the balance
    funds distribution and margin.  Acquisition cost is out of scope: the premium is
    single and the cost is priced in.
    """
    return expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821


def liability_cf(t):
    """CF(t): total gross liability outgo in month t, the notes' cash flow definition.

    ``E[ANN] + E[PRO] - E[FRA] + E[EXP]``.  **Outgo positive**, the notes' own sign.  The
    *frais d'arrérages* carry a minus because the insurer retains them out of the
    payment.  There is no premium income in the projection - the *capital constitutif* is
    a pricing input at the effective date - no surrender outgo, because the contract has
    no surrender value at any duration, and no death capital, the representative design
    being *capital aliéné*.
    """
    return (annuity_payments(t) + claims(t) - arrerage_charges(t)
            + expenses(t))


def net_cf(t):
    """Net cash flow to the insurer in month t: income less outgo, so ``-liability_cf``.

    **Income positive**, the sign convention every model in this library carries, kept
    even though this product has no projected income so that every model's ``net_cf`` can
    be compared or summed across the library.  :func:`liability_cf` carries the opposite,
    outgo-positive sign of the technical notes; both are published as columns of
    :func:`result_cf` rather than one being made to stand for the other.
    """
    return -liability_cf(t)


def check_lives_roll_fwd_resid(t):
    """Residual between :func:`lives_if` and an independently rebuilt survival path.

    Deliberately **not** the telescoping identity ``l(t) - d(t) - l(t + 1)``:
    :func:`lives_death` is *defined* as that difference, so the identity is identically
    zero whatever :func:`lives_if` returns and constrains nothing.  Each life's survival
    is rebuilt here from the assumptions instead, with no reference to the recursion - on
    the *table* basis as the **annual** form ``prod (1 - q_x)`` over the completed years
    of age and ``(1 - q)^(rest/12)`` over the part-year, which the monthly recursion must
    telescope to.  A recursion that reads the age one month early or late, or that indexes
    the table by the projection year instead of the *millésime*, breaks it.  ``t`` is a
    **time**, as in :func:`lives_if`: the survival rebuilt here is the one to time t.
    """
    res = 0.0
    scenario = mort_basis() == "scenario"
    for life in (1, 2):
        if life == 2 and reversion_pct() <= 0.0:
            continue
        if scenario:
            d = death_mth(life)
            built = 0.0 if (d >= 0 and t > d) else 1.0
        else:
            built = 1.0
            full = t // 12
            rest = t - 12 * full
            for j in range(full):
                built *= 1.0 - mort_rate_at_age(
                    sex(life), birth_year(life), age_at_entry(life) + j)
            if rest:
                q = mort_rate_at_age(
                    sex(life), birth_year(life), age_at_entry(life) + full)
                built *= (1.0 - q) ** (rest / 12.0)
        res += built - lives_if(t, life)
    return res


def check_lives_roll_fwd():
    """Whether the survival recursion closes at **every** projected month.

    Takes no argument and returns a ``bool``, the library-wide shape of a ``check_*``
    cells, so one test can call the same check across every model.  The signed residual
    of a failing month stays available as :func:`check_lives_roll_fwd_resid`.  It sweeps
    the **time points** the frame reads, ``t = 0 .. proj_len()``: the last projected
    month, ``proj_len() - 1``, closes at time ``proj_len()``.
    """
    return bool(all(abs(check_lives_roll_fwd_resid(t)) < 1e-10
                    for t in range(proj_len() + 1)))


def check_revalo_roll_fwd_resid(t):
    """Residual between :func:`revalo_factor` and its closed form.

    The recursion steps whenever ``k(t)`` advances; the closed form is
    ``(1 + nu (13 - M0)/12)(1 + nu)^(k - 1)`` for ``k >= 1`` and 1 for ``k = 0``.  The two
    are independent constructions of the same index, and the residual catches both of the
    notes' revalorisation pitfalls: a step taken on the policy anniversary instead of at
    31 December moves ``k`` by ``13 - M0`` months, and dropping the first-year pro-rating
    scales every later month by ``(1 + nu)/(1 + nu (13 - M0)/12)`` for the whole of the
    annuity's remaining life, because R is a running product.
    """
    k = cal_year_index(t)
    if k == 0:
        built = 1.0
    else:
        first = max(0.0, revalo_rate * (13 - effective_month()) / 12.0)  # noqa: F821
        built = ((1.0 + first)
                 * (1.0 + max(0.0, revalo_rate)) ** (k - 1))         # noqa: F821
    return built - revalo_factor(t)


def check_revalo_roll_fwd():
    """Whether the revalorisation index closes against its closed form at every month."""
    return bool(all(abs(check_revalo_roll_fwd_resid(t)) < 1e-12
                    for t in range(proj_len())))


def check_cum_annuity_roll_fwd_resid(t):
    """Residual between :func:`cum_annuity_pp` on ``"ANNUITANT"`` and a direct sum.

    The recursion is rebuilt here as an explicit sum of the scheduled instalments over
    the payment months up to t, with no reference to the accumulation.  A cumulation that
    starts at the wrong month, double-counts a payment month, or reads ``annuity_pp`` at
    ``t - 1`` shows up here; the telescoping form would not, because it is the recursion
    written twice.  The first payment month is ``12/m - 1`` in arrears and month 0 in
    advance.
    """
    step = 12 // payment_freq()
    start = step - 1 if payment_timing() == "arrears" else 0
    built = sum(annuity_pp(s) for s in range(start, t + 1, step))
    return built - cum_annuity_pp(t, "ANNUITANT")


def check_cum_annuity_roll_fwd():
    """Whether the cumulative *arrérages* schedule closes at every projected month."""
    return bool(all(abs(check_cum_annuity_roll_fwd_resid(t)) < 1e-8
                    for t in range(proj_len())))


def check_calendar_index_resid(t):
    """``k(t) - (calendar_year(t) - Y0)``: two constructions of the same count.

    :func:`cal_year_index` counts the 31 Decembers from the length of the first partial
    calendar year, ``13 - M0``; :func:`calendar_year` steps the year from the civil month
    of the effective date.  They are independent and must agree at every month.  An
    implementation that counts anniversaries instead of 31 Decembers disagrees from the
    first turn of the year.
    """
    return cal_year_index(t) - (calendar_year(t) - effective_year())


def check_calendar_index():
    """Whether the calendar index agrees with the calendar at every projected month."""
    return bool(all(check_calendar_index_resid(t) == 0
                    for t in range(proj_len())))


def check_payment_factor_resid(t):
    """``payment_factor(t) - max(gamma(t), l_a)``: the guarantee double-count guard.

    Zero by construction, and asserted anyway: an additive floor - ``gamma + l_a`` instead
    of ``max(gamma, l_a)`` - is a listed pitfall and would pay ``1 + l_a`` for the whole
    guaranteed term.  It would show up here as ``min(gamma, l_a)``.
    """
    return payment_factor(t) - max(certain_floor(t), payment_factor_life(t))


def check_payment_factor():
    """Whether the guarantee stays a floor rather than a second stream, at every month."""
    return bool(all(abs(check_payment_factor_resid(t)) < 1e-12
                    for t in range(proj_len())))


def check_revalo_floor():
    """Whether the revalorisation index is non-decreasing at every month.

    The contractual floor on the uplift is zero in every retrieved formulation, so a
    *rente* in payment can rise and can stand still but can never fall.  A negative
    ``revalo_rate`` fed into the model must therefore leave the annuity where it was
    rather than cutting it.  The sweep starts at month 1, month 0 having no predecessor.
    """
    return bool(all(revalo_factor(t) >= revalo_factor(t - 1) - 1e-15
                    for t in range(1, proj_len())))


def check_options_xor():
    """Whether the contract carries at most one of a *réversion* and *annuités garanties*.

    The representative design offers one or the other, never both, and the coefficients
    are definitive reductions of the same annuity: compounding two of them would price an
    option pair no retrieved carrier sells.
    """
    return not (reversion_pct() > 0.0 and guarantee_mths() > 0)


def check_commutation_floor():
    """Whether the gross *quittance* clears the statutory commutation threshold.

    ``A0 Pi(0) / m > 110 x (12/m)``: below it the insurer may, with the annuitant's
    agreement, pay a capital instead, so there is no annuity to project.  This is an
    **admission test**, not a cash flow - the one policyholder election that survives
    conversion - and a model point that fails it is a defect in the table rather than a
    projection with a small answer.
    """
    gross = annual_income_init() * palier_factor(0) / payment_freq()
    return bool(gross > commutation_floor * (12.0 / payment_freq()))  # noqa: F821


def check_taux_rente():
    """Whether the carried *taux de rente* agrees with the one the tariff table implies.

    The shipped mortality proxy is anchored so that ``taux_rente_tariff()`` reproduces the
    technical notes' placeholder rho exactly at the worked configuration, and every other
    model point carries the rate the same construction gives at its own age, *millésime*
    and *taux technique*, rounded to six decimals.  The check ties the model point table
    to the mortality table: editing one without the other fails here rather than silently
    pricing on a basis the projection does not use.
    """
    return bool(abs(taux_rente_tariff() - annuity_rate()) < 1e-6)


def result_cf():
    """Result table of cashflows, indexed by month t.

    ``pols_if`` is the probability any payment obligation remains, which is the expense
    weight rather than a policy count.  ``arrerage_charges`` is the one column the
    insurer **retains**: it is positive here and subtracted in ``liability_cf``.  Both
    signs of the net flow are published: ``net_cf`` is income-positive, the library-wide
    convention, and ``liability_cf`` is the technical notes' outgo-positive ``CF(t)``.

    The index is the 0-based month, ``t = 0 .. proj_len() - 1``.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "claims_prorata": [claims(t, "PRORATA") for t in ts],
            "arrerage_charges": [arrerage_charges(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of survival probabilities and payment factors, indexed by month t.

    ``lives_if_1`` and ``lives_if_2`` are the survival probabilities to the **end** of
    month t, ``lives_if(t + 1, life)``: :func:`lives_if` is a time-point cells and this is
    a table of periods, so the row carries the closing value, which is also the point an
    arrears instalment is measured at.  The index is ``t = 0 .. proj_len() - 1``.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "lives_if_1": [lives_if(t + 1, 1) for t in ts],
            "lives_if_2": [lives_if(t + 1, 2) for t in ts],
            "revalo_factor": [revalo_factor(t) for t in ts],
            "palier_factor": [palier_factor(t) for t in ts],
            "annual_income": [annual_income(t) for t in ts],
            "certain_floor": [certain_floor(t) for t in ts],
            "payment_factor": [payment_factor(t) for t in ts],
            "reversion_factor": [reversion_factor(t) for t in ts],
            "prorata_factor": [prorata_factor(t) for t in ts],
            "annuity_pp": [annuity_pp(t) for t in ts],
            "cum_annuity_all": [cum_annuity_pp(t, "ALL") for t in ts],
            "pols_if": [pols_if(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

tariff_table_sex = "F"

portfolio_male_share = 0.45

rate_loading = 0.0227

revalo_rate = 0.015

commutation_floor = 110.0

expense_maint = 30.0

inflation_rate = 0.015

pd = ("Module", "pandas")
