# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.PA_UK_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked-example scenario
    >>> Projection.point_id = 2            # the same contract, probability-weighted

``t`` counts **months from the annuity start date**, 1-based: ``t = 1`` is the first
projected month and ``t = 0`` is the month-zero state used as the base case of every
recursion (``lives_if(0, life) = 1``, ``cum_annuity_pp(0, kind) = 0``).

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/pension_annuity/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``PA_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.PA_UK_S.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and follow :mod:`.SPIA_US_S` — this library's
U.S. payout chassis — wherever the two products share machinery, so that the same
concept has the same name on both sides of the Atlantic. The technical notes use
compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the cells argument)            Month from the start date
y = ceil(t/12)             policy_year(t)                  Policy year containing month t
(none)                     duration(t)                     Completed policy years, y - 1
(none)                     duration_mth(t)                 Months elapsed at end of month t
P                          purchase_price()                Purchase price
x_a, x_d                   age_at_entry(life)              Entry ages (ALB), life 1 or 2
(none)                     age(t, life)                    Attained age (ALB)
(none)                     sex(life)                       Sex of each covered life
theta_a, theta_d           rating_factor(life)             Enhanced/impaired multiplier
delta                      dependant_pct()                 Dependant's percentage
(dependant_present)        is_joint()                      Contract covers a dependant
overlap                    overlap()                       Dependant runs during guarantee
A(1)                       annual_income_init()            Starting annualized income
A(y)                       annual_income(y)                Annualized income in year y
g                          escalation_rate()               Fixed escalation rate
escalation_type            escalation_type()               level / fixed / rpi_catchup / lpi5
I(k)                       rpi_index(k)                    RPI reference level at anniv. k
peak                       rpi_peak(k)                     Running peak of the index
m                          payment_freq()                  Payments per year
timing                     payment_timing()                arrears or advance
T                          is_payment_mth(t)               Month t is a payment date
(payment point)            payment_surv_mth(t)             Month survival is measured at
inst(t)                    annuity_pp(t)                   Scheduled instalment
n                          guarantee_mths()                Guarantee period in months
C(t) = 1{t <= n}           certain_floor(t)                Annuity-certain floor indicator
l_a(t), l_d(t)             lives_if(t, life)               Survival probability
d_a(t), d_d(t)             lives_death(t, life)            Death density
d_last(t)                  lives_death_last(t)             Last-death density
(none)                     lives_if_last(t)                At least one covered life alive
max(C, l_a)                payment_factor(t)               Annuitant payment factor
(none)                     payment_factor_life(t)          l_a alone, before the floor
w(t)                       overlap_gate(t)                 Dependant-stream availability
delta(1-l_a)l_d w          dependant_factor(t)             Dependant payment factor
G(t)                       cum_annuity_pp(t, kind)         Cumulative scheduled instalments
v                          vp_pct()                        Value-protection percentage
vp_basis                   vp_basis()                      first_death or last_survivor
VPbal(t)                   vp_balance(t)                   Value-protection balance
h(t)                       mths_since_payment(t)           Complete months since last payment
proportion                 proportion()                    Proportionate final payment
(none)                     next_payment_mth(t)             The next scheduled payment month
q_x (table)                mort_rate_base(t, life)         Base-table annual rate
alpha                      annuitant_adj                   Population-to-annuitant factor
f(x)                       improve_rate(t, life)           Improvement rate at the age
(1-f)^(c-c0)               improve_factor(t, life)         Cumulative improvement factor
q_rated                    mort_rate(t, life)              Annual rate after all factors
q_m                        mort_rate_mth(t, life)          Monthly rate 1-(1-q)^(1/12)
(none)                     mort_basis()                    table or scenario run **[std]**
(none)                     death_mth(life)                 Scenario month of death **[std]**
omega                      omega_age                       Limiting age, 115
(stopping rule)            horizon_mths()                  Months to the age stop rule
(none)                     proj_len()                      Last projected month
(none)                     calendar_year(t)                Calendar year containing month t
IF(t)                      pols_if(t)                      Any payment obligation open
(none)                     pols_if_init()                  Contracts in force at t = 0
E[ANN(t)]                  annuity_payments(t)             Expected annuity outgo
E[VP(t)]                   claims(t, "VP")                 Value-protection lump sum
E[PROP(t)]                 claims(t, "PROP")               Proportionate final payment
E[EXP(t)]                  expenses(t)                     Maintenance expense
c_e, pi                    expense_maint, inflation_rate   Expense level and inflation
CF(t)                      liability_cf(t)                 Total gross liability outgo
(none)                     net_cf(t)                       -liability_cf(t), insurer sign
=========================  ==============================  ==========================

Four names needed care.

``G(t)`` is used for two different accumulations in the notes: the *state variable*
table defines it as cumulative gross instalments **scheduled**, which is what the worked
example's G column prints, while the value-protection section says it accumulates
instalments "while the annuitant is alive" on the first-death basis and "the
dependant's instalments too" on the last-survivor one. Those are different objects
whenever the dependant's stream is running, so :func:`cum_annuity_pp` takes a ``kind``:
``"ANNUITANT"`` is the deterministic as-if-alive annuitant schedule that the first-death
value-protection balance nets against, and ``"ALL"`` adds the expected dependant
instalments and is the notes' printed column.

``l`` and ``L`` differ in the notes only by case, as in ``SPIA_US_S``: survival
probability against the payment factor. They become :func:`lives_if` and
:func:`payment_factor_life`, with :func:`payment_factor` the certain-floored version.

``w(t)`` is the overlap gate, not a lapse rate — there is no lapse on this product at
all. It is spelled :func:`overlap_gate` so that nothing in the model reads as a
decrement that is not one.

``pols_if`` is not a policy count in the usual sense. It is the notes' ``IF(t)``, the
probability that *any* payment obligation remains — guarantee certain, annuitant alive,
or dependant stream in payment — and it exists to carry the maintenance expense. The
name is kept because it is what the rest of the library calls the expense weight.

.. rubric:: Two mortality bases: table and scenario

The notes' worked example is not a probability-weighted run. It is a **scenario**: "the
annuitant dies in month 17; the dependant survives throughout", evaluated at
``l_a = 0`` from month 17 and ``l_d = 1`` throughout. The rest of the notes projects on
an expected basis. Both readings are shipped, and which one applies is a model point
column — the same device :mod:`.SPIA_US_S` uses for the same reason:

``mort_basis = "table"``
    ``lives_if`` runs the generational recursion off the shipped mortality table and
    improvement scale. Model points 2, 5, 6, 7 and 8; point 2 is the worked
    configuration on this basis and is the run to read for a realistic cash flow shape.

``mort_basis = "scenario"`` **[std]**
    ``lives_if(t, life)`` is the deterministic step function ``1{t < death_mth(life)}``,
    with a blank ``death_mth`` meaning the life survives the whole projection. Model
    points 1, 3, 4, 9 and 10, which reproduce the worked example and its variants
    exactly.

The scenario switch is a **[std]** modelling device, not a product feature; it exists
because the notes' verification anchor is a scenario and retuning assumptions to force a
probability-weighted run onto it would be dishonest.

.. rubric:: The guarantee is a floor, not a second stream

``payment_factor(t) = max(certain_floor(t), payment_factor_life(t))`` is the notes'
first-listed pitfall written as one line. During the guarantee period the full
instalment is payable regardless of survival, escalating as if the annuitant were alive;
an additive construction would pay ``1 + l_a`` and silently double the guarantee.

The guarantee and value protection **never coexist** in the representative design — the
contract offers one or the other, and :func:`check_guarantee_xor` asserts no model point
carries both. An engine supporting the combinable variant would have to net guarantee
payments off the value-protection balance or the death benefit is paid twice.

.. rubric:: The overlap gate

``overlap = False`` is the representative default and means the dependant's stream
starts only at the **end of the guarantee period**, not at the annuitant's death.
Applying the dependant's percentage from the death date silently converts every
without-overlap policy into the more expensive with-overlap form, which is the notes'
second-listed pitfall. Model points 3 and 4 are the same contract on either side of that
switch, and their cash flows differ from month 18 to month 120.

.. rubric:: Escalation, and the one path-dependent option

Four bases. ``level`` and ``fixed`` are self-explanatory; ``lpi5`` is RPI floored at
zero and capped at 5%; ``rpi_catchup`` is a **ratchet**: income is indexed to the
*running peak* of the RPI reference index, so a fall in the index freezes income rather
than reducing it, and later rises only bite once the index passes its previous peak.
:func:`rpi_peak` carries that state across anniversaries. Resetting it each year turns
the catch-up into a plain zero floor and overstates indexed income after a
deflation-recovery path.

Under the deterministic 3% RPI assumption **[std]** the index is monotone, so the
ratchet never binds and ``rpi_catchup`` degenerates to fixed 3% — model points 6 and 2
agree by construction. That is not an accident to be tidied away but the honest
consequence of a deterministic inflation path: the zero floor, the ratchet and the LPI
cap are all **inflation options**, and a deterministic path values them at intrinsic
only. A market-consistent value needs stochastic inflation.

Escalation applies on the **anniversary**, not on payment dates: the year-2 rate does
not reach the ``t = 12`` arrears instalment, which accrued in year 1.

.. rubric:: Value protection, and where the balance is measured

``VP(t) = d(t) x max(0, v P - G(t-1))``, the death benefit measured against instalments
**already paid**. Two timing rules matter and both are the notes' pitfalls:

- on **arrears** timing the balance is ``G(t-1)``, because the instalment due at the end
  of the death month is never paid;
- on **advance** timing an instalment paid at the *start* of the death month **has**
  been paid, so in an advance payment month the balance is ``G(t)`` — netting it, or the
  lump sum is overstated by one instalment.

On the ``first_death`` basis the death that triggers it is the annuitant's and the
balance nets the annuitant's schedule alone. On ``last_survivor`` it is the last death,
and the balance nets both streams — which, on a probability-weighted run, makes the
balance an *expected* cumulative payment rather than a path-specific one. That
approximation is stated here rather than hidden: it is exact in a scenario run, which is
the basis the shipped ``last_survivor`` model point uses.

The contractual bound ``v + delta <= 1`` on the first-death basis is asserted by
:func:`check_vp_bound`; the worked configuration sits exactly on it.

.. rubric:: There is no policyholder behaviour to model

No lapse decrement, no dynamic behaviour formulas, no surrender value at any time, no
alteration of options and no premium flexibility. That is a cited product feature and
the reason the liability is matching-adjustment eligible, and it is why this model has no
``lapse_rate`` of any kind. Behaviour enters only at outset, outside the projection, as
basis-selection effects: voluntary annuitants self-select for longevity, which is the
direction of the ``annuitant_adj`` factor below 1, and the enhanced-annuity market
leaves standard-terms lives healthier on average, which is carried through
:func:`rating_factor` rather than through any dynamic.

.. rubric:: Sign convention

The notes define ``CF(t)`` as total gross liability **outgo**, which is
:func:`liability_cf`. :func:`net_cf` is its negative, the library-wide income-positive
convention, so a ``result_cf()["net_cf"]`` column can be summed or compared across every
model in the library. Both are published as columns rather than one being made to stand
for the other. There is no premium income in the projection at all: the purchase price
is a pricing input at ``t = 0``, not a projected cash flow.
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
    """P: the amount applied to the annuity after any lump sum and adviser charges.

    A pricing input at t = 0, not a projected cash flow: the projection carries no
    premium income.  It enters the projection only through value protection, where the
    guarantee is measured against it.
    """
    return float(model_point()["purchase_price"])


def age_at_entry(life):
    """x: the entry age of the annuitant (``life = 1``) or dependant (``life = 2``).

    **Age last birthday**, chosen to index the shipped single-year-of-age proxy table
    **[std]**.
    """
    if life == 1:
        return int(model_point()["annuitant_age"])
    if life == 2 and is_joint():
        return int(model_point()["dependant_age"])
    raise ValueError("invalid life")


def sex(life):
    """The sex (M / F) of the annuitant or dependant."""
    if life == 1:
        return model_point()["annuitant_sex"]
    if life == 2 and is_joint():
        return model_point()["dependant_sex"]
    raise ValueError("invalid life")


def rating_factor(life):
    """theta: the enhanced or impaired mortality multiplier **[std]**; 1.0 standard.

    ``q_rated = min(1, theta x q)``, the simplest overlay that reprices longevity
    without touching contract mechanics.  Insurers' real rating structures - postcode
    and condition-specific factors - are not public, and a rated-age offset is the
    equivalent form.  Whole-market enhanced quoting is mandated at the point of sale, so
    lives remaining on standard terms are healthier on average; the model carries that
    through this multiplier rather than through any behavioural dynamic.
    """
    if life == 1:
        return float(model_point()["rating_multiplier"])
    if life == 2 and is_joint():
        return float(model_point()["dependant_rating"])
    raise ValueError("invalid life")


def is_joint():
    """True when the contract carries a dependant's income."""
    return bool(model_point()["dependant_present"])


def dependant_pct():
    """delta: the dependant's percentage of the income; zero on a single-life contract."""
    v = float(model_point()["dependant_pct"])
    if not is_joint():
        return 0.0
    return v


def overlap():
    """Whether the dependant's stream runs *during* the remaining guarantee period.

    ``False`` is the representative default and means the stream starts at the end of
    the guarantee, not at the annuitant's death.  See :func:`overlap_gate`.
    """
    return bool(model_point()["overlap"])


def annual_income_init():
    """A(1): the starting annualized income.

    A pricing input taken from a quote: no insurer publishes an annuity rate card, so
    the model does not derive income from the purchase price and nothing in the
    projection consumes ``P`` except value protection.
    """
    return float(model_point()["annual_income"])


def payment_freq():
    """m: payments per year, in {12, 4, 2, 1}."""
    v = int(model_point()["frequency"])
    if v not in (12, 4, 2, 1):
        raise ValueError("invalid frequency")
    return v


def payment_timing():
    """Whether instalments fall in *arrears* or in *advance*.

    Arrears instalments require survival at the end of the payment month; advance
    instalments at the start of it.  Using end-of-period survival for advance payments
    understates the liability by roughly one period's mortality per payment, which is
    material at high ages.
    """
    v = model_point()["timing"]
    if v not in ("arrears", "advance"):
        raise ValueError("invalid timing")
    return v


def proportion():
    """Whether a proportionate final payment is made for the accrued part-period.

    Arrears only.  Without it - the representative default - nothing is paid for the
    final partial period, which is the more common contractual design.
    """
    v = bool(model_point()["proportion"])
    if v and payment_timing() != "arrears":
        raise ValueError("proportion applies to arrears payments only")
    return v


def escalation_type():
    """``level``, ``fixed``, ``rpi_catchup`` or ``lpi5``.

    ``lpi5`` is RPI floored at zero and capped at 5%; ``rpi_catchup`` is a ratchet on
    the running peak of the RPI reference index.  See the Space docstring.
    """
    v = model_point()["escalation_type"]
    if v not in ("level", "fixed", "rpi_catchup", "lpi5"):
        raise ValueError("invalid escalation_type")
    return v


def escalation_rate():
    """g: the fixed escalation rate, at most 10%; read only on the ``fixed`` basis."""
    v = float(model_point()["escalation_rate"])
    if v > esc_fixed_cap:                                            # noqa: F821
        raise ValueError("fixed escalation exceeds the contractual cap")
    return v


def guarantee_mths():
    """n: the guarantee period in months, 0 or 12-360.

    Instalments are certain for n months, escalating as if the annuitant were alive.
    Mutually exclusive with value protection in the representative design.
    """
    return int(model_point()["guarantee_months"])


def vp_pct():
    """v: the value-protection percentage of the purchase price; 0 if not elected."""
    return float(model_point()["vp_pct"])


def vp_basis():
    """Whether value protection pays on the ``first_death`` or the ``last_survivor``.

    On the first-death basis the trigger is the annuitant's death and the balance nets
    the annuitant's instalments; on the last-survivor basis it is the last death and the
    balance nets both streams.  See the Space docstring for the approximation the second
    basis carries in a probability-weighted run.
    """
    v = model_point()["vp_basis"]
    if v not in ("first_death", "last_survivor"):
        raise ValueError("invalid vp_basis")
    return v


def mort_basis():
    """Whether the run is probability-weighted (*table*) or deterministic (*scenario*).

    *table* runs the generational recursion off the shipped table and improvement scale;
    *scenario* **[std]** replaces it with the step function ``1{t < death_mth(life)}`` so
    the notes' worked example - which is a scenario, not an expectation - reproduces
    exactly.  See the Space docstring.
    """
    v = model_point()["mort_basis"]
    if v not in ("table", "scenario"):
        raise ValueError("invalid mort_basis")
    return v


def death_mth(life):
    """The scenario month of death of ``life``; 0 if the life survives throughout.

    Read only when ``mort_basis() == "scenario"``.  A blank cell in the model point
    table means the life never dies in the scenario and is returned as 0, since ``t`` is
    1-based and a death in month 0 is not a projectable event.  A death "in month 17" is
    decremented at the end of month 17, so ``lives_if(t, life)`` is 0 from ``t = 17``.
    """
    v = model_point()["death_mth_1" if life == 1 else "death_mth_2"]
    return 0 if pd.isna(v) else int(v)                               # noqa: F821


def start_year():
    """The calendar year of the annuity start date; the improvement-scale anchor.

    The improvement exponent is ``calendar_year(t) - mort_table_year``, so this is what
    makes the mortality basis generational rather than period.
    """
    return int(model_point()["start_year"])


def pols_if_init():
    """Initial number of contracts in force; 1.0 on a single-contract model point."""
    return float(model_point()["pols_if_init"])


def duration(t):
    """Completed policy years at the start of month t: ``(t - 1) // 12``."""
    return (t - 1) // 12


def duration_mth(t):
    """Months elapsed from the start date at the end of month t; equal to t.

    ``t`` is 1-based, so the identity is trivial - the cells exists so the monthly
    models in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y = ceil(t/12): the policy year containing month t; 1 for t = 1..12."""
    return duration(t) + 1


def age(t, life):
    """The attained age (ALB) of ``life`` in the policy year containing month t."""
    return age_at_entry(life) + duration(t)


def calendar_year(t):
    """The calendar year of the policy year containing month t."""
    return start_year() + duration(t)


def horizon_mths():
    """The last month at which some covered life has not yet passed the limiting age.

    ``12 x (omega_age - min x_i)``: the notes stop once ``t/12 + x_i > omega`` for every
    covered life, and stopping on the annuitant's age alone would truncate a younger
    dependant's tail.  The notes' other stop test, ``IF(t) < 1e-6``, is not implemented,
    because a stopping rule that depends on the projection it bounds is harder to reason
    about than one that does not.
    """
    ages = [age_at_entry(1)]
    if is_joint():
        ages.append(age_at_entry(2))
    return 12 * (omega_age - min(ages))                              # noqa: F821


def proj_len():
    """Projection length in months: the mortality horizon, or the guarantee if longer."""
    return max(horizon_mths(), guarantee_mths())


def is_payment_mth(t):
    """Whether month t is a payment date.

    Arrears: ``t = 3, 6, 9, ...`` at m = 4.  Advance: the k-th instalment falls one full
    payment period earlier, at the start of month ``12(k-1)/m + 1``, so t = 1, 4, 7, ...
    At m = 12 every month is a payment month on either convention.
    """
    if t < 1:
        return False
    step = 12 // payment_freq()
    if payment_timing() == "arrears":
        return t % step == 0
    return (t - 1) % step == 0


def payment_surv_mth(t):
    """The month at which survival is measured for the instalment falling in month t.

    Arrears: the end of month t.  Advance: the end of month ``t - 1``, because an
    advance instalment falls at the *start* of month t; 0 for the first instalment,
    where ``lives_if`` is 1.  Using end-of-period survival for advance payments
    understates the liability by about one period's mortality per payment.
    """
    return t if payment_timing() == "arrears" else t - 1


def rpi_index(k):
    """I(k): the RPI reference level at anniversary k **[std]**; I(0) = 1.

    A deterministic ``(1 + rpi_rate)^k`` path.  A deterministic path cannot value the
    zero floor, the catch-up ratchet or the LPI cap - all of them inflation options -
    and values them at intrinsic only; a market-consistent value needs stochastic
    inflation.
    """
    return (1.0 + rpi_rate) ** k                                     # noqa: F821


def rpi_peak(k):
    """The running maximum of the RPI reference index through anniversary k.

    The catch-up ratchet's state, and it is **path-dependent**: it must persist across
    anniversaries.  Resetting it each year turns the catch-up into a plain zero floor
    and overstates indexed income after a deflation-recovery path.
    """
    if k <= 0:
        return rpi_index(0)
    return max(rpi_peak(k - 1), rpi_index(k))


def annual_income(y):
    """A(y): the annualized income in policy year y, on the annuitant's scale.

    Escalation applies at the start of the month containing the policy anniversary, so
    the first increase reaches ``t = 13`` and not the ``t = 12`` arrears instalment,
    which accrued in year 1.  By basis::

        level:        A(y) = A(1)
        fixed:        A(y) = A(y-1)(1 + g)
        lpi5:         A(y) = A(y-1)(1 + min(0.05, max(0, RPI)))
        rpi_catchup:  A(y) = A(1) x peak(y-1) / I(0)

    The catch-up form is the closed version of the ratchet pseudocode: income is indexed
    to the running peak of the reference index.
    """
    if y <= 1:
        return annual_income_init()
    e = escalation_type()
    if e == "level":
        return annual_income_init()
    if e == "fixed":
        return annual_income(y - 1) * (1.0 + escalation_rate())
    if e == "lpi5":
        step = min(esc_lpi_cap, max(0.0, rpi_rate))                  # noqa: F821
        return annual_income(y - 1) * (1.0 + step)
    return annual_income_init() * rpi_peak(y - 1) / rpi_index(0)


def annuity_pp(t):
    """inst(t) = A(y(t))/m: the scheduled instalment per contract in month t.

    Zero outside payment months.  This is the *annuitant's* instalment; the dependant's
    is ``delta`` times it, on the same escalated income, which is what the contractual
    "percentage of the higher of income at death and at guarantee end" reduces to under
    a non-decreasing escalation path.
    """
    if not is_payment_mth(t):
        return 0.0
    return annual_income(policy_year(t)) / payment_freq()


def next_payment_mth(t):
    """The next scheduled payment month at or after month t; used by the proportion rule."""
    step = 12 // payment_freq()
    s = t
    while s <= proj_len() + step:
        if is_payment_mth(s):
            return s
        s += 1
    return 0


def mths_since_payment(t):
    """h(t): complete months elapsed since the last payment date, measured at t - 1.

    The accrual base of the proportionate final payment.  On the worked configuration a
    death in month 17 with quarterly arrears payments at months 3, 6, ... gives h = 1:
    one complete month since the month-15 instalment.
    """
    step = 12 // payment_freq()
    if t <= 1:
        return 0
    last = ((t - 1) // step) * step
    return max(0, (t - 1) - last)


def mort_rate_base(t, life):
    """The base-table annual mortality rate for ``life`` in the year containing month t.

    Population mortality, times the **[std]** annuitant adjustment that stands in for
    the difference between a population table and the licensed annuitant tables.  Rates
    at and above the limiting age are 1.
    """
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    return float(data.mort_table().loc[                              # noqa: F821
        (sex(life), x), "mort_rate"]) * annuitant_adj                # noqa: F821


def improve_rate(t, life):
    """f(x): the annual mortality improvement rate at ``life``'s attained age **[std]**.

    A flat rate to age 90, tapering linearly to zero at 110 and zero above it.  This
    stands in for the CMI Mortality Projections Model, whose software is restricted, and
    it **materially understates** the age-period-cohort structure of the real model - it
    exists only so the reference implementation is runnable without CMI access.  The
    choice of long-term improvement rate is the single most sensitive judgment in UK
    annuity valuation, and the CMI model carries no default recommendation for it.
    """
    x = age(t, life)
    if x <= improve_flat_age:                                        # noqa: F821
        return improve_rate_base                                     # noqa: F821
    if x >= improve_taper_age:                                       # noqa: F821
        return 0.0
    span = improve_taper_age - improve_flat_age                      # noqa: F821
    return improve_rate_base * (improve_taper_age - x) / span        # noqa: F821


def improve_factor(t, life):
    """(1 - f(x))^(c - c0): the cumulative improvement factor for ``life`` in month t.

    ``c`` is the calendar year containing month t and ``c0`` the base table's data
    mid-year, so the basis is **generational**: each attained age in each future
    calendar year carries its own improved rate.
    """
    k = calendar_year(t) - mort_table_year                           # noqa: F821
    return (1.0 - improve_rate(t, life)) ** k


def mort_rate(t, life):
    """q_rated: the annual mortality rate applied to ``life`` in the year containing t.

    The notes' construction, in order::

        q_base  = ONS-shaped table rate x alpha
        q_imp   = q_base x (1 - f(x))^(c - c0)
        q_rated = min(1, theta x q_imp)

    Every one of the three factors is a standardization: the table is a population
    proxy, the improvement scale a stand-in for a restricted model, and the rating
    multiplier the simplest form of an unpublished structure.  The liability is a
    life-contingent stream with no offsetting decrements, so the level of this rate is
    the single largest lever on it.
    """
    q = mort_rate_base(t, life) * improve_factor(t, life)
    return min(1.0, rating_factor(life) * q)


def mort_rate_mth(t, life):
    """q_m = 1 - (1 - q_rated)^(1/12): the monthly mortality rate **[std]**."""
    return 1.0 - (1.0 - mort_rate(t, life)) ** (1.0 / 12.0)


def lives_if(t, life):
    """l(t): the probability that ``life`` is alive at the end of month t.

    ``l(0) = 1``.  On the *table* basis ``l(t) = l(t-1)(1 - q_m(t))``, deaths being
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
    """d(t) = l(t-1) - l(t): the death density of ``life`` in month t."""
    return lives_if(t - 1, life) - lives_if(t, life)


def lives_if_last(t):
    """The probability that at least one covered life is alive at the end of month t.

    ``l_a + l_d - l_a l_d`` under **joint-life independence [std]**, which ignores
    broken-heart dependence and common lifestyle factors and so modestly overstates the
    expected dependant stream.  On a single-life contract this is ``l_a``.
    """
    la = lives_if(t, 1)
    if not is_joint():
        return la
    ld = lives_if(t, 2)
    return la + ld - la * ld


def lives_death_last(t):
    """d_last(t): the last-death density in month t, the last-survivor VP trigger."""
    return lives_if_last(t - 1) - lives_if_last(t)


def certain_floor(t):
    """C(t) = 1{t <= n}: the annuity-certain floor indicator of the guarantee period."""
    return 1.0 if t <= guarantee_mths() else 0.0


def payment_factor_life(t):
    """l_a measured at the payment point: the annuitant's survival factor alone.

    Survival is measured at :func:`payment_surv_mth`, not at t - the end of the payment
    month on arrears and the start of it on advance.
    """
    return lives_if(payment_surv_mth(t), 1)


def payment_factor(t):
    """max(C(t), l_a): the annuitant stream's payment factor.

    The ``max`` makes the guarantee period an annuity-**certain floor** rather than an
    additional stream: during the guarantee the full instalment is payable regardless of
    survival, escalating as if the annuitant were alive, and the ``max`` prevents paying
    ``1 + l_a``.  An additive construction silently doubles the guarantee, which is the
    notes' first-listed pitfall.
    """
    return max(certain_floor(t), payment_factor_life(t))


def overlap_gate(t):
    """w(t): whether the dependant's stream is available in month t.

    1 with overlap, or once the guarantee period has run; 0 inside the guarantee without
    overlap.  **Not** a decrement of any kind - there is no lapse on this product -
    which is why it is not called a rate.  Applying the dependant's percentage from the
    death date on a without-overlap contract silently converts it into the more
    expensive with-overlap form.
    """
    if overlap() or t > guarantee_mths():
        return 1.0
    return 0.0


def dependant_factor(t):
    """delta (1 - l_a) l_d w(t): the dependant stream's payment factor.

    The dependant is paid when the annuitant is dead and the dependant alive, gated by
    the overlap rule, both survivals measured at the payment point.  Zero on a
    single-life contract.
    """
    if not is_joint():
        return 0.0
    s = payment_surv_mth(t)
    return (dependant_pct() * (1.0 - lives_if(s, 1)) * lives_if(s, 2)
            * overlap_gate(t))


def cum_annuity_pp(t, kind):
    """G(t): cumulative scheduled instalments per contract through month t.

    ``"ANNUITANT"``
        the **deterministic as-if-alive** annuitant schedule.  This is what
        the first-death value-protection balance nets against, and it needs
        no path simulation precisely because it ignores survival.

    ``"ALL"``
        the same plus the expected dependant instalments, which is the
        column the notes' worked-example table prints and the balance the
        last-survivor basis nets against.  On a probability-weighted run it
        is an *expected* cumulative payment rather than a path-specific one;
        in a scenario run the two coincide.
    """
    if t <= 0:
        return 0.0
    if kind == "ANNUITANT":
        return cum_annuity_pp(t - 1, kind) + annuity_pp(t)
    if kind == "ALL":
        paid = annuity_pp(t) * (payment_factor(t) + dependant_factor(t))
        return cum_annuity_pp(t - 1, kind) + paid
    raise ValueError("invalid kind")


def vp_balance(t):
    """VPbal(t) = max(0, v P - G(t)): the value-protection balance after month t.

    Nets the schedule the elected basis applies to: the annuitant's alone on
    ``first_death``, both streams on ``last_survivor``.  Zero when value protection is
    not elected.
    """
    if vp_pct() <= 0.0:
        return 0.0
    kind = "ANNUITANT" if vp_basis() == "first_death" else "ALL"
    return max(0.0, vp_pct() * purchase_price() - cum_annuity_pp(t, kind))


def annuity_payments(t):
    """E[ANN(t)]: expected annuity outgo in month t.

    ``inst(t) x [max(C(t), l_a) + delta (1 - l_a) l_d w(t)]``, scaled by
    ``pols_if_init``: the annuitant stream with its guarantee floor, plus the
    dependant's stream.
    """
    return pols_if_init() * annuity_pp(t) * (payment_factor(t) + dependant_factor(t))


def claims(t, kind=None):
    """Expected lump-sum outgo in month t, by kind; the total when kind is omitted.

    ``"VP"``
        the value-protection lump sum, ``d(t) x VPbal``.  The trigger is the
        annuitant's death on the ``first_death`` basis and the last death on
        ``last_survivor``.  The balance is measured at ``t - 1`` on arrears
        timing, because the instalment due at the end of the death month is
        never paid; in an **advance** payment month it is measured at ``t``,
        because an instalment paid at the start of the death month has been paid
        and netting it is what keeps the lump sum from being overstated by one
        instalment.

    ``"PROP"``
        the proportionate final payment on an arrears contract that elects it:
        ``d_a(t) x (h(t) + 0.5)/(12/m) x inst(next(t))``, a **[std]** half-month
        accrual for the part-period between the last payment date and the death.
        Zero on the representative default, where nothing is paid for the final
        partial period.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("VP", "PROP"))
    if kind == "VP":
        if vp_pct() <= 0.0:
            return 0.0
        density = (lives_death(t, 1) if vp_basis() == "first_death"
                   else lives_death_last(t))
        measured_at = (t if (payment_timing() == "advance" and is_payment_mth(t))
                       else t - 1)
        return pols_if_init() * density * vp_balance(measured_at)
    if kind == "PROP":
        if not proportion():
            return 0.0
        nxt = next_payment_mth(t)
        if nxt == 0:
            return 0.0
        accrual = (mths_since_payment(t) + 0.5) / (12.0 / payment_freq())
        return pols_if_init() * lives_death(t, 1) * accrual * annuity_pp(nxt)
    raise ValueError("invalid kind")


def pols_if(t):
    """IF(t): the probability that any payment obligation remains in month t.

    ``min(1, max(C(t), l_a(t)) + 1{delta>0}(1 - l_a(t)) l_d(t))`` **[std]** - guarantee
    certain, annuitant alive, or dependant stream in payment.  This is the weight the
    maintenance expense is carried on, which is why it keeps the library's name for the
    expense weight even though it is not a policy count.
    """
    la = lives_if(t, 1)
    obligation = max(certain_floor(t), la)
    if dependant_pct() > 0.0:
        obligation += (1.0 - la) * lives_if(t, 2)
    return pols_if_init() * min(1.0, obligation)


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y - 1)`` **[std]**."""
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """E[EXP(t)]: maintenance expense in month t **[std]**.

    ``(c_e / 12)(1 + pi)^(y-1) IF(t)``: a round placeholder for in-payment
    administration, paid monthly while any payment obligation remains.  No insurer
    publishes expense assumptions - charges are priced into the annuity rate - and
    acquisition cost is out of scope, the premium being single and the cost priced in.
    Second-order against the instalments, but the in-payment term is thirty years or
    more, so the inflation assumption compounds.
    """
    return expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821


def liability_cf(t):
    """CF(t): total gross liability outgo in month t, the notes' cash flow definition.

    ``E[ANN] + E[PROP] + E[VP] + E[EXP]``.  **Outgo positive**, the notes' own sign.
    There is no premium income in the projection - the purchase price at t = 0 is a
    pricing input - and no surrender outgo, because the contract has no surrender value
    at any time.
    """
    return annuity_payments(t) + claims(t) + expenses(t)


def net_cf(t):
    """Net cash flow to the insurer in month t: income less outgo, so ``-liability_cf``.

    **Income positive**, the sign convention every model in this library carries, kept
    even though this product has no projected income so that every model's ``net_cf``
    can be compared or summed across the library.  :func:`liability_cf` carries the
    opposite, outgo-positive sign of the technical notes; both are published as columns
    of :func:`result_cf` rather than one being made to stand for the other.
    """
    return -liability_cf(t)


def check_lives_roll_fwd_resid(t):
    """Residual between :func:`lives_if` and an independently rebuilt survival path.

    Deliberately **not** the telescoping identity ``l(t-1) - d(t) - l(t)``:
    :func:`lives_death` is *defined* as that difference, so the identity is identically
    zero whatever :func:`lives_if` returns and constrains nothing.  Each life's survival
    is rebuilt here from the assumptions instead, with no reference to the recursion - on
    the *table* basis as the running product ``prod (1 - q_m(s))``, which a misindexed or
    mis-based recursion breaks - and the residual is the sum of the per-life differences.
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
    return res


def check_lives_roll_fwd():
    """Whether the survival recursion closes at **every** projected month.

    Takes no argument and returns a ``bool``, the library-wide shape of a ``check_*``
    cells, so one test can call the same check across every model.  The signed residual
    of a failing month stays available as :func:`check_lives_roll_fwd_resid`.
    """
    return all(abs(check_lives_roll_fwd_resid(t)) < 1e-10
               for t in range(1, proj_len() + 1))


def check_payment_factor_resid(t):
    """``payment_factor(t) - max(C(t), l_a)``: the guarantee double-count guard.

    Zero by construction.  It is asserted anyway because an additive floor - ``C + l_a``
    instead of ``max(C, l_a)`` - is the notes' first-listed pitfall and would show up
    here as ``min(C, l_a)``.
    """
    return payment_factor(t) - max(certain_floor(t), payment_factor_life(t))


def check_payment_factor():
    """Whether the guarantee stays a floor rather than a second stream, at every month."""
    return all(abs(check_payment_factor_resid(t)) < 1e-10
               for t in range(1, proj_len() + 1))


def check_guarantee_xor():
    """Whether the contract carries at most one of a guarantee period and value protection.

    The representative design offers one or the other, never both.  An engine supporting
    the combinable variant would have to net guarantee payments off the value-protection
    balance, or the death benefit is paid twice - so the exclusivity is asserted rather
    than assumed.
    """
    return not (guarantee_mths() > 0 and vp_pct() > 0.0)


def check_vp_bound():
    """Whether ``v + delta <= 1`` on the first-death value-protection basis.

    A contractual bound, and the worked configuration sits exactly on it.  It does not
    apply on the last-survivor basis, where the two benefits cannot both be triggered by
    the same death.
    """
    if vp_pct() <= 0.0 or vp_basis() != "first_death":
        return True
    return vp_pct() + dependant_pct() <= 1.0 + 1e-12


def result_cf():
    """Result table of cashflows, indexed by month t.

    ``pols_if`` is the probability any payment obligation remains, which is the expense
    weight rather than a policy count.  Both signs of the net flow are published:
    ``net_cf`` is income-positive, the library-wide convention, and ``liability_cf`` is
    the technical notes' outgo-positive ``CF(t)``.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "claims_vp": [claims(t, "VP") for t in ts],
            "claims_prop": [claims(t, "PROP") for t in ts],
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
            "certain_floor": [certain_floor(t) for t in ts],
            "payment_factor": [payment_factor(t) for t in ts],
            "dependant_factor": [dependant_factor(t) for t in ts],
            "annuity_pp": [annuity_pp(t) for t in ts],
            "cum_annuity_all": [cum_annuity_pp(t, "ALL") for t in ts],
            "vp_balance": [vp_balance(t) for t in ts],
            "pols_if": [pols_if(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 115

mort_table_year = 2023

annuitant_adj = 0.8

improve_rate_base = 0.0125

improve_flat_age = 90

improve_taper_age = 110

rpi_rate = 0.03

esc_fixed_cap = 0.1

esc_lpi_cap = 0.05

expense_maint = 30.0

inflation_rate = 0.03

pd = ("Module", "pandas")