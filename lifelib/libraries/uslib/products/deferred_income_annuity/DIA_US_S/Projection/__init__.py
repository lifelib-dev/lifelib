# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.DIA_US_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_annual()      # the worked-example anchor cell
    >>> Projection.point_id = 8            # or switch the default

.. rubric:: t counts months from issue, and it is 0-based

``t = 0, 1, 2, …, proj_len()`` are **policy months from issue**, indexed exactly as the
technical notes index them. ``t = 0`` is the issue month and a real projected month, not
a recursion base case: the first premium is received at its start, deaths occur during
it, and the maintenance expense accrues in it. This is a deliberate departure from the
1-based ``t`` of :mod:`.Term_US_A` and :mod:`.SPIA_US_S`, and the reason is that
the notes' ``T`` is a **month index** in the 0-based scheme — the anchor cell's income
start month is ``T = 240`` and its premiums fall at months 0 and 60. Renumbering to a
1-based grid would make ``T = 240`` mean the 241st month and quietly move every option
window, premium date and payment date by one.

Two consequences to hold on to:

- ``lives_if(t, life)`` is the probability of being alive at the **start** of month
  ``t`` — equivalently, of having survived ``t`` elapsed months, ``lives_if(0) = 1``.
  That is the *same* function of elapsed time as ``SPIA_US_S.lives_if``, so the
  name carries its meaning across unchanged.
- ``lives_death(t, life) = lives_if(t) - lives_if(t + 1)`` — deaths **during** month
  ``t``. In the 1-based chassis the same quantity is ``l(t-1) - l(t)``, because month
  ``t`` spans elapsed ``[t-1, t)`` there and ``[t, t+1)`` here.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/deferred_income_annuity/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only, and an input can
be edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``DIA_US_S`` folder without its parent's CSVs produces a model that reads
and then fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.DIA_US_S.Data`:

========================  ==================================  ======================
Reference                 Cells                               File
========================  ==================================  ======================
model_point_file          data.model_point_table()            model_point_table.csv
premium_schedule_file     data.premium_schedule_table()       premium_schedule.csv
mort_table_file           data.mort_table()                   mort_table.csv
improvement_scale_file    data.improvement_scale()            improvement_scale.csv
payout_factor_file        data.payout_factor_table()          payout_factor_table.csv
rop_factor_file           data.rop_factor_table()             rop_factor_table.csv
========================  ==================================  ======================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and — for everything in the income phase — they
follow :mod:`.SPIA_US_S` **exactly**, because the payout phase of a DIA *is* a
single premium immediate annuity. The technical notes use compact actuarial symbols
instead. The mapping is:

=========================  ==============================  =========================
Notes symbol               Cells                           Meaning
=========================  ==============================  =========================
t                          (the cells argument)            Policy month from issue
y = floor(t/12) + 1        policy_year(t)                  Policy year containing t
(none)                     duration(t)                     Completed policy years
(none)                     duration_mth(t)                 Months elapsed at start of t
x, x_2                     age_at_entry(life)              Issue ages (ANB), life 1 or 2
x(t)                       age(t, life)                    Attained age (ANB)
(none)                     sex(life)                       Sex of each covered life
(none)                     is_joint()                      Two covered lives
market_type                market_type()                   NQ / TradIRA / RothIRA / QLAC
f                          income_form()                   LO / LO_ROP / CR / IR / PC
(f, payout part)           payout_form()                   The payout stream f implies
db_form                    db_form()                       ROP or NONE in deferral
n                          certain_period()                Elected certain period, years
T                          income_start_mth()              Income start month in force
(T at issue)               income_start_mth_init()         Income start month at issue
(T for a premium at t)     income_start_mth_at(t)          Start month a premium is priced to
m                          payment_freq()                  Payments per year
pay_timing                 payment_timing()                arrears / advance
c                          cola_rate()                     Fixed compound COLA rate
(1+c)^floor((t-T)/12)      cola_factor(t)                  COLA escalation factor
delta / survivor_pct       survivor_pct()                  Survivor percentage
reduction_trigger          reduction_trigger()             either / primary
P_k                        premium_pp(t)                   Premium paid in month t
(the schedule)             premium_by_mth()                {month: premium} mapping
CP(t)                      cum_premium_pp(t)               Cumulative premiums, eq (7)
B(t)                       annual_income(t)                Guaranteed annual income, eq (8)
l(t)                       lives_if(t, life)               Survival to the start of month t
q(t)                       mort_rate_mth(t, life)          Monthly death probability
(annual q)                 mort_rate(t, life)              Annual rate after improvement
q_x (table)                mort_rate_base(t, life)         Base-table annual rate
2012 (in q_x^(2012+n))     mort_table_year                 Base year of the shipped table
G2_x                       improvement_rate(t, life)       Generational improvement rate
(A/E)                      mort_ae_factor                  A/E factor, 1.00 **[std]**
omega                      omega_age                       Limiting age, 120
(d_i)                      lives_death(t, life)            Deaths during month t
l_last(t)                  lives_if_last(t)                At least one life alive
d_last(t)                  lives_death_last(t)             Last-death density
(in force)                 pols_if(t)                      Contracts in force
i_p, v                     pricing_rate                    Pricing interest rate, 4.75%
v^d                        pricing_disc_factor(yrs)        Pricing discount factor
L                          expense_load                    Expense and profit load, 6.0%
d_k = (T - t_k)/12         deferral_yrs(t)                 Deferral of a premium at t
_d p_x                     surv_to_income_start(t)         Survival over the deferral
a^(m)_y(f; i)              annuity_factor(...)             Payout APV, eq (2) generalized
(same, at T)               payout_factor()                 Payout factor in force
(same, computed)           payout_factor_calc()            Payout factor by eq (2)
A_rop(x, d; i)             rop_factor(t)                   ROP factor in force, eq (3)
(same, computed)           rop_factor_calc(t)              ROP factor by the mid-band rule
a_def(x, d, f; i)          annuity_factor_def(t)           Deferred APV, eq (1)
pr(x, d, f)                purchase_rate(t)                Purchase rate, eq (4)
n_g (pricing)              guarantee_mths_pricing()        n_g in the kernel, eq (5)
("three iterations")       pricing_iters                   Fixed points taken on eq (5)
n_g (realized)             guarantee_yrs()                 CP(T)/B(T), eq (5)
n_R                        certain_mths_refund()           Derived refund period, months
n_eff                      certain_mths_eff()              Effective certain months
C(t)                       certain_floor(t)                Certain-floor indicator
L(t), L_pay(t)             payment_factor_life(t)          Life-contingent payment factor
Phi(t)                     payment_factor(t)               max(C(t), L(t))
inst(t)                    annuity_pp_sched(t)             Scheduled instalment
(inst as payable)          annuity_pp(t)                   Instalment after a blackout
(inst after commutation)   annuity_pp_paid(t)              inst * (1 - theta_cum * C)
G(t)                       cum_annuity_pp(t)               Cumulative scheduled instalments
RG(t)                      refund_balance(t)               Remaining refund balance
phase(t)                   phase(t)                        DEFERRAL / PAYOUT / TERMINATED
(t >= T)                   is_payout(t)                    In the income phase
T (payment dates)          is_payment_mth(t)               Month t is a payment date
(payment point)            payment_surv_mth(t)             Elapsed month survival is at
Baa(t_e)                   baa_yield                       Moody's Baa yield at t_e
s_adj                      adjust_spread                   Repricing spread, 100 bp
i_e                        repricing_rate()                Start-date repricing rate, eq (10)
B'/B                       adjust_income_factor()          Repricing factor, eq (11)
t_e                        adjust_mth()                    Start-date exercise month
T'                         adjust_start_mth()              New income start month
t_a                        accel_mth()                     Acceleration exercise month
n_a                        accel_months                    Payments accelerated, 6
Cost(t_a)                  accel_cost()                    Acceleration cost, eq (12)
accel_blackout(t)          accel_blackout(t)               Payments suspended
(Phi, frozen at t_a)       accel_payment_factor(t)         Weight on an accelerated payment
t_c                        commute_mth()                   Commutation exercise month
r_ref(t) - r_ref(0)        ref_rate_shift                  Reference-rate rise since issue
i_c(t)                     commute_disc_rate(t)            Commutation rate, eq (13)
m_c                        commute_margin                  Commutation margin, 50 bp
CV(t)                      commuted_value(t)               Commuted value, eq (14)
theta_cum(t)               commute_frac_cum(t)             Cumulative commuted fraction
(l_last(t_c))              commute_weight(t)               Cohort a commutation extinguishes
E[COMM(t)]                 commutations(t)                 Commutation paid to the owner
Limit(year)                qlac_premium_limit              QLAC premium limit, $210,000
qlac_room(t)               qlac_room(t)                    Remaining QLAC premium room
(age 85 outside date)      qlac_max_start_age              Latest QLAC income start age
(QLAC conditions)          qlac_flags()                    QLAC compliance failures
(premium income)           premiums(t)                     l(t) * premium paid at t
(deferral DB)              claims(t, "DEATH")              Return of CP(t) on death
(refund benefit)           claims(t, "REFUND")             Cash-refund lump sum
(per contract)             claim_pp(t, kind)               Claim amount per contract
E[income]                  annuity_payments(t)             Expected income outgo
e, g                       expense_maint, inflation_rate   Maintenance expense and escalation
E[EXP(t)]                  expenses(t)                     Maintenance expense
(total outgo)              liability_outgo(t)              Gross liability outgo
(none)                     liability_cf(t)                 Net stream, outgo positive
(none)                     net_cf(t)                       Premiums less outgo
=========================  ==============================  =========================

Seven names in that table needed care.

``l`` and ``L`` differ in the notes only by case — the survival probability versus the
life-contingent payment factor — so they become ``lives_if`` and
``payment_factor_life``, exactly as in :mod:`.SPIA_US_S`. ``L`` is *also* the
expense and profit load in equation (4); that one is the Reference ``expense_load``.

``B`` is the guaranteed **annual** income and ``B(t)/m`` is one instalment; the notes
never name the instalment, so it takes the chassis name ``annuity_pp_sched``. Note that
``annual_income(t)`` is indexed by **month**, not by policy year as in
:mod:`.SPIA_US_S`, because a DIA's income level changes when a *premium* is paid
and premiums fall on months.

``n_g`` is two different quantities in the notes and they must not be conflated.
:func:`guarantee_mths_pricing` is the guarantee period fed into the pricing kernel by
equation (5) — a fixed point, since ``n_g = CP(T)/B`` and ``B`` depends on ``n_g``.
:func:`guarantee_yrs` is the realized value once ``B`` is known, the 3.3891 years the
worked example quotes. And :func:`certain_mths_eff` — the *projection's* certain floor —
is **zero on a cash-refund contract**, because a cash refund is a lump sum at death, not
a stream of guaranteed payments. Equation (5) is a pricing approximation for both refund
forms; only installment refund actually pays a certain stream.

``theta`` appears **nowhere** in the DIA notes.  ``theta_cum``, the cumulative commuted
fraction, is inherited from the immediate-annuity notes that these notes incorporate by
reference for the whole income phase; the DIA notes write equations (13) and (14) with
no symbol for the fraction at all.  The cells keeps the chassis name,
:func:`commute_frac_cum`, so that the two models read alike.

Two cohort weights carry no notes symbol because the notes have no need of one: a SPIA
is already in payment and its whole model point reaches the income phase together.
:func:`surv_to_payout` is ``l_last(T)``, the cohort that ever reaches the income phase
and therefore the only cohort a guarantee period can pay; :func:`commute_weight` is
``l_last(t_c)``, the sub-cohort still alive to exercise a commutation and therefore the
only cohort whose guarantee a commutation can extinguish.  They are the same idea
applied at two dates, and getting either of them wrong moves the guaranteed leg without
moving anything else.

``CP(T)`` is the DIA-specific change to the payout chassis and the notes' own listed
pitfall: **the refund base is cumulative premiums, not the initial premium.** Where
``SPIA_US_S`` writes ``premium_pp()``, this model writes
``cum_premium_pp(income_start_mth())``.

The self-checks follow the library-wide ``check_*`` convention, which is
``CashValue_SE.check_av_roll_fwd()``'s: each check takes **no argument and returns a
bool** covering every projected ``t``, so one test can call the same name across every
model in the library, and each carries a companion ``check_*_resid(t)`` returning the
signed float residual at a single ``t`` for the debugging session that follows a failure.
The bool is defined in terms of the residual, never the other way round.
:func:`check_lives_roll_fwd`, :func:`check_income_roll_fwd`,
:func:`check_payment_factor` and :func:`check_commutation_value` are the four here; there
is no ``check_av_roll_fwd``, because there is no account value to roll forward.

.. rubric:: Two pricing bases: tabulated and computed

The notes' worked example is priced off illustrative factors it states outright —
``a^(12)_80(cash refund, female; 4.75%) = 8.60``, ``A_rop(60, 20) = 0.157900``,
``A_rop(65, 15) = 0.180200`` — declaring them "mutually consistent illustrative values,
**not** table lookups". Both readings are shipped, and which one applies is a model point
column:

``factor_basis = "table"``
    :func:`payout_factor` and :func:`rop_factor` read the shipped factor tables, and
    :func:`annuity_factor_def` is the notes' equation (1) literally,
    ``v^d * _d p_x * a^(m)``. Model points 1, 2 and 4. This is the basis that
    reproduces the worked example. It is single-life only: equation (1) factorizes the
    deferral survival out of the payout APV, which a joint status does not permit.

``factor_basis = "formula"``
    :func:`payout_factor_calc` computes equation (2) and :func:`rop_factor_calc` the
    notes' mid-band approximation of equation (3), both off the shipped mortality table,
    and :func:`annuity_factor_def` values the whole deferred stream in one pass so joint
    forms work. Model points 3 and 5 onwards.

The shipped mortality table is **[std]**, built so that the two bases agree where the
notes say they should: its rates over ages 60-84 are band-constant values reproducing
the notes' five-year survival anchors exactly, and the geometric continuation past age
85 is calibrated so that equation (2) at the income start age returns 8.600 — the notes'
own illustrative payout factor. Where they then *disagree* is ``A_rop(60, 20)``; see
below.

.. rubric:: The A_rop(60, 20) divergence is shipped, not resolved

The notes say ``A_rop`` was "computed from the same survival anchors with a mid-band
death-timing approximation". Run that recipe and the twenty-year factor comes out at
**0.161605**, not the **0.157900** the notes print, while the fifteen-year factor comes
out at **0.180241** against a printed **0.180200** — agreement to four decimal places.
One of the two is arithmetically consistent with the stated recipe and the other is not.
Rather than choose, the model ships both: model point 1 takes the printed factors from
``rop_factor_table.csv`` and reproduces the worked example, model point 3 is otherwise
identical and computes them. A test pins the gap open.

.. rubric:: The purchase-rate rounding is a [std] convention, and it is worth 3.6 cents

The worked example computes ``B_1 = 100,000 x 0.321765 = $32,176.50`` from a purchase
rate printed to six decimals. At full precision ``pr_1 = 0.3217647`` and the same
premium buys ``$32,176.47``; over both slices the difference is 3.6 cents on a
``$44,259.65`` income. The model point column ``purchase_rate_dp`` carries the
convention — 6 on point 1, blank (full precision) on point 2 — so the worked example
reproduces to the cent without the rounding being hidden.

.. rubric:: The certain period is a floor, not a second stream

``payment_factor(t) = max(certain_floor(t), payment_factor_life(t))`` is inherited from
the payout chassis and is the notes' first-listed payout pitfall. During the certain
period the full, *unreduced* instalment is payable regardless of survival; an additive
construction would pay ``1 + L`` and silently double the guarantee. The ``max`` also
reproduces, with no extra logic, the rule that a survivor reduction falling inside a
guarantee period is deferred to the end of that period.

.. rubric:: There is no lapse decrement, and adding one is a defect

"Lapse and surrender: exactly zero, at all durations. Not conservatism — there is no
surrender benefit to elect [R9][R13]. A nonzero lapse assumption in a DIA model is a
defect, not a margin." There is no ``lapse_rate``, no ``pols_lapse``, no surrender cash
flow row and no account value roll-forward in this model, and none should be added:
the liability is a schedule of income slices keyed on (premium, purchase date, income
start date, income option), not a balance.
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


def age_at_entry(life):
    """x: issue age (ANB) of the primary (life = 1) or joint (life = 2) annuitant.

    Age nearest birthday **[std]**: the archetype guide states contract issue age on an
    ANB basis [S2], prescribed VM-22 payout mortality is ANB [R9], and the 2012 IAM
    Basic and Period tables were developed ANB [R15][REG-R59].
    """
    if life == 1:
        return int(model_point()["issue_age"])
    if life == 2:
        return int(model_point()["joint_age"])
    raise ValueError("invalid life")


def sex(life):
    """Sex (M / F) of the primary (life = 1) or joint (life = 2) annuitant."""
    if life == 1:
        return model_point()["sex"]
    if life == 2:
        return model_point()["joint_sex"]
    raise ValueError("invalid life")


def is_joint():
    """True when the contract covers two annuitants [S2][S4]."""
    return bool(model_point()["joint"])


def survivor_pct():
    """delta: the survivor percentage, in {0.50, 2/3, 0.75, 1.00} [S1][S2][S4]."""
    return float(model_point()["survivor_pct"])


def reduction_trigger():
    """trig: whether the reduction is triggered by *either* death or the *primary*'s.

    A switch, not a parameter: the two conventions coincide on the primary's death and
    differ only on the secondary's [S1][S2][S4].
    """
    v = model_point()["reduction_trigger"]
    if v not in ("either", "primary"):
        raise ValueError("invalid reduction_trigger")
    return v


def market_type():
    """The tax wrapper: NQ, TradIRA, RothIRA or QLAC [S2][S4]."""
    v = model_point()["market_type"]
    if v not in ("NQ", "TradIRA", "RothIRA", "QLAC"):
        raise ValueError("invalid market_type")
    return v


def is_qlac():
    """True when the contract is intended to be a QLAC [R1 (q)(1)(vi)]."""
    return market_type() == "QLAC"


def income_form():
    """f: the income option elected at issue and immutable thereafter [S1][S2][S4].

    ``LO`` life only; ``LO_ROP`` life only with a 100% return-of-purchase-payments death
    benefit in deferral, the unbundled extended-case variant [S4]; ``CR`` life with cash
    refund; ``IR`` life with installment refund; ``PC`` life with period certain.
    """
    v = model_point()["income_form"]
    if v not in ("LO", "LO_ROP", "CR", "IR", "PC"):
        raise ValueError("invalid income_form")
    return v


def payout_form():
    """The payout stream the elected form implies: LO, CR, IR or PC.

    ``LO_ROP`` collapses to ``LO`` here because its return of premium is a *deferral*
    death benefit carried by :func:`db_form`; after the income start date it is a pure
    life annuity [S4].  The unbundling of the death benefit from the payout form is the
    product spec's chosen parameterization, so that the two mortality exposures move
    independently.
    """
    f = income_form()
    return "LO" if f in ("LO", "LO_ROP") else f


def db_form():
    """The deferral-phase death benefit: ``ROP`` or ``NONE``.

    100% of cumulative premiums, no interest, lump sum, on every option except Life Only
    and Joint Life Only [S1][S2][S3][S4][R13 SS3.I(1)(a)].  This is the product's central
    pricing fork: setting it to ``NONE`` removes ``A_rop`` from the numerator of equation
    (4) and buys strictly more income for the same premium.
    """
    v = model_point()["db_form"]
    if v not in ("ROP", "NONE"):
        raise ValueError("invalid db_form")
    return v


def certain_period():
    """n: the elected certain period in years, 10-30 on PC forms [S2]; 0 otherwise."""
    return int(model_point()["certain_period"])


def payment_freq():
    """m: payments per year, in {12, 4, 2, 1}; fixed at issue [S1][S2]."""
    v = int(model_point()["frequency"])
    if v not in (12, 4, 2, 1):
        raise ValueError("invalid frequency")
    return v


def payment_timing():
    """Whether instalments fall in *arrears* (the **[std]** default) or in *advance*.

    No retrieved DIA document states the convention; arrears matches
    ``products/immediate_annuity/product-spec.md`` so that one payout chassis serves
    both products.
    """
    v = model_point()["timing"]
    if v not in ("arrears", "advance"):
        raise ValueError("invalid timing")
    return v


def cola_rate():
    """c: the fixed compound annual increase, 0 or 1%-4%, elected at issue [S2][S3][S4].

    Every observed option is a fixed compound escalator applied on each anniversary of
    the income start date, **not** a CPI adjustment - the notes list treating it as
    index-linked among the product's pitfalls.
    """
    return float(model_point()["cola_rate"])


def issue_year():
    """The calendar year of issue **[std]**; the anchor of the generational projection.

    The improvement exponent is ``calendar_year(t) - mort_table_year``.  The chassis
    calls its counterpart ``annuity_year`` because a SPIA's annuity date *is* its issue
    date; here the two are twenty years apart, so the generational anchor has to be
    named for the one that matters.
    """
    return int(model_point()["issue_year"])


def pols_if_init():
    """Initial number of contracts in force; 1.0 on a single-contract model point."""
    return float(model_point()["pols_if_init"])


def mort_basis():
    """Whether mortality is the notes' *anchor* curve or the *generational* projection.

    *anchor* **[std]**: the shipped table is used as a period table, which is what
    reproduces the worked example - its survival anchors are a single non-generational
    curve.  *generational*: the notes' prescribed construction
    ``q^(2012+k) = q^(2012) * (1 - G2_x)^k`` [R9][REG-R59] is applied with the shipped
    illustrative improvement scale.  Both are shipped because the notes prescribe the
    second and verify against the first.
    """
    v = model_point()["mort_basis"]
    if v not in ("anchor", "generational"):
        raise ValueError("invalid mort_basis")
    return v


def factor_basis():
    """Whether the pricing factors are *table* lookups or *formula* computations.

    *table*: :func:`payout_factor` and :func:`rop_factor` read the notes' illustrative
    factors and :func:`annuity_factor_def` is equation (1) literally - the basis that
    reproduces the worked example, single-life only.  *formula*: both are computed from
    the shipped mortality table by equations (2) and (3).  See the Space docstring.
    """
    v = model_point()["factor_basis"]
    if v not in ("table", "formula"):
        raise ValueError("invalid factor_basis")
    return v


def purchase_rate_dp():
    """Decimal places the purchase rate is rounded to, or None for full precision.

    **[std]**.  The worked example computes ``B`` from a six-decimal purchase rate;
    carrying full precision instead moves the anchor cell's annual income by 3.6 cents.
    Blank on the model point returns -1, meaning no rounding: modelx forbids a cells
    returning ``None``, so every "not set" on this Space is a negative sentinel.
    """
    v = model_point()["purchase_rate_dp"]
    return -1 if pd.isna(v) else int(v)                              # noqa: F821


def other_qlac_premium():
    """Premiums paid to any other contract intended to be a QLAC [R1 (q)(2)(ii)(B)].

    The QLAC dollar limit is reduced by premiums paid to any other QLAC under any
    401(a), 403(a), 403(b), 408 or governmental 457(b) arrangement; the issuer may rely
    on the owner's written representation [R5 (h)(2)].
    """
    return float(model_point()["other_qlac_premium"])


def premium_schedule():
    """The selected contract's premium slices, ordered by payment month.

    A DIA is a flexible-premium contract - "any number of premiums during the deferral
    period" [S2][S3][S4][R13] - so the schedule is a separate long table rather than a
    fixed set of model point columns.
    """
    tbl = data.premium_schedule_table()                              # noqa: F821
    return tbl[tbl["point_id"] == point_id].sort_values("premium_mth")  # noqa: F821


def premium_by_mth():
    """The premium schedule collapsed to a ``{month: amount}`` mapping.

    Built once per contract so that :func:`premium_pp` is a dictionary lookup rather
    than a DataFrame filter in every one of the projected months.
    """
    out = {}
    for _, r in premium_schedule().iterrows():
        k = int(r["premium_mth"])
        out[k] = out.get(k, 0.0) + float(r["premium_amt"])
    return out


def premium_pp(t):
    """P_k: the premium per contract paid at the **start** of month t; 0 if none falls."""
    return premium_by_mth().get(t, 0.0)


def cum_premium_pp(t):
    """CP(t): cumulative premiums paid per contract, equation (7).

    ``CP(t) = CP(t-1) + sum of P_k at t``, ``CP(-1) = 0``.  This is both the deferral
    death benefit base and - at ``t = T`` - the refund base.  **For a flexible-premium
    DIA the refund base is CP(T), not the initial premium**, which is one of the notes'
    listed pitfalls [S2][S4].
    """
    if t < 0:
        return 0.0
    return cum_premium_pp(t - 1) + premium_pp(t)


def duration_mth(t):
    """Months elapsed from issue at the start of month t; equal to t.

    ``t`` is 0-based here, so the identity is trivial - the cells exists so that the
    monthly models share one vocabulary.
    """
    return t


def duration(t):
    """Completed policy years at the start of month t: ``t // 12``."""
    return t // 12


def policy_year(t):
    """y = floor(t/12) + 1: the policy year containing month t; 1 for t = 0..11."""
    return duration(t) + 1


def calendar_year(t):
    """The calendar year of the policy year containing month t."""
    return issue_year() + duration(t)


def age(t, life):
    """x(t) = x + floor(t/12): the attained age (ANB) of ``life`` in month t."""
    return age_at_entry(life) + duration(t)


def horizon_mths():
    """Months from issue to the limiting age of the *youngest* covered life.

    ``t/12 + x_i > omega_age`` for every covered life is the payout chassis' stop rule;
    stopping on the primary's age alone would truncate a younger joint annuitant's tail.
    """
    ages = [age_at_entry(1)]
    if is_joint():
        ages.append(age_at_entry(2))
    return 12 * (omega_age - min(ages))                              # noqa: F821


def proj_len():
    """The last projected month index: ``t`` runs 0, 1, ..., ``proj_len()``.

    The mortality horizon, or the end of the guarantee period if that is later.  Both
    are age- or contract-driven rather than derived from the projection they bound, so
    ``proj_len()`` never depends on the survival path.
    """
    return max(horizon_mths() - 1,
               income_start_mth() + certain_mths_eff() - 1)


def income_start_mth_init():
    """T at issue: the income start month elected at issue, ``13 <= T <= 360`` [S2][S4].

    ``T`` is a month index, so the income start date is the **start** of month ``T``,
    exactly ``T/12`` years after issue.  Under arrears the first instalment falls one
    payment period later - at ``m = 12``, at the end of month ``T``.
    """
    return int(model_point()["income_start_mth"])


def adjust_mth():
    """t_e: the month a start-date adjustment is exercised; -1 if it never is.

    One-time, deferral only, excluded on Life Only and Joint Life Only [S1][S3][S4].
    The **incidence** of the exercise - the notes' 1.5% p.a. take-up with its 60/40
    direction split, rate multipliers and health-selection overlay - is a cohort-
    splitting behavioural construction and is **not implemented**; the exercise is
    named deterministically on the model point instead, and is off by default.
    """
    v = model_point()["adjust_mth"]
    return -1 if pd.isna(v) else int(v)                              # noqa: F821


def adjust_start_mth():
    """T': the new income start month after an adjustment; -1 if there is none.

    ``|T' - T| <= 60`` months, ``T'`` at least 13 months after the last premium, and
    inside the maximum deferral and the maximum income start age [S1][S2][S3][S4].
    """
    v = model_point()["adjust_start_mth"]
    return -1 if pd.isna(v) else int(v)                              # noqa: F821


def income_start_mth():
    """T in force: the adjusted start month if one is exercised, else the elected one."""
    return income_start_mth_init() if adjust_mth() < 0 else adjust_start_mth()


def income_start_mth_at(t):
    """The income start month a premium paid in month t is priced to.

    A premium bought before the adjustment was priced to the original date; one bought
    after it is priced to the new date [R13 SS3.B(1)(b)].
    """
    a = adjust_mth()
    if a < 0 or t < a:
        return income_start_mth_init()
    return adjust_start_mth()


def repricing_rate():
    """i_e = Baa(t_e) - s_adj: the rate a start-date adjustment is repriced at, eq (10).

    The disclosed recipe keys on Moody's Seasoned Baa Corporate Bond Yield at the
    request date less a contractual interest-rate-change adjustment [S1][S2]; the
    adjustment is named but never quantified in any retrieved source, so the 100 bp
    spread is **[std]**.  The base run sets ``baa_yield`` so that ``i_e = i_p`` - no rate
    movement since issue - because the notes supply no Baa value **[std]**.
    """
    return baa_yield - adjust_spread                                 # noqa: F821


def accel_mth():
    """t_a: the month payment acceleration is exercised; -1 if it never is.

    Payout phase, attained age 59 1/2 or over, nonqualified, monthly frequency
    [S1][S2][S3][S4].  The notes' 2% p.a. take-up among eligible contracts is a
    cohort-splitting construction and is **not implemented**; the exercise is named
    deterministically on the model point and is off by default.
    """
    v = model_point()["accel_mth"]
    return -1 if pd.isna(v) else int(v)                              # noqa: F821


def commute_mth():
    """t_c: the month a commutation is exercised; -1 if never (extended case only).

    Offered by one of the four composite sources [S4][S5] and prohibited on a QLAC after
    the required beginning date [R1 (q)(1)(iv)].  The notes' 1.5% p.a. take-up is not
    implemented, for the same reason as the other two options.
    """
    v = model_point()["commute_mth"]
    return -1 if pd.isna(v) else int(v)                              # noqa: F821


def commute_frac():
    """The fraction of the remaining guaranteed payments commuted; up to 100% [S4][R13]."""
    v = model_point()["commute_frac"]
    return 0.0 if pd.isna(v) else float(v)                           # noqa: F821


def mort_rate_base(t, life):
    """The base-table annual mortality rate for ``life`` in the year containing month t.

    The shipped table is an illustrative **[std]** annuitant table, *not* the 2012 IAM
    Basic table the notes prescribe: licensed tables may not be embedded, and the Basic
    table is in any case printed in no source this library holds - A-821 prints the
    loaded Period Table only [REG-R153].  Its rates over ages 60-84 are band-constant
    values that reproduce the notes' five-year survival anchors exactly.  Rates at and
    above the limiting age are 1.
    """
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    return float(data.mort_table().loc[(x, sex(life)), "mort_rate"])  # noqa: F821


def improvement_rate(t, life):
    """G2_x: the generational improvement rate for ``life`` in the year containing t.

    The shipped scale is an illustrative **[std]** stand-in for Projection Scale G2 and
    is read only when ``mort_basis() == "generational"``.  Scaling it is the notes' first
    listed sensitivity: Scale G2 is fixed and dated, and the 2020-2024 payout experience
    study says it has over-projected improvement [R15][REG-R61].
    """
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 0.0
    return float(                                                    # noqa: F821
        data.improvement_scale().loc[(x, sex(life)), "improvement_rate"])


def mort_rate(t, life):
    """The annual mortality rate applied to ``life`` in the year containing month t.

    On the *generational* basis the notes' construction
    ``q_x^(2012+k) = q_x^(2012) * (1 - G2_x)^k`` [R9][REG-R59], with
    ``k = calendar_year(t) - mort_table_year``, so each attained age in each future
    calendar year uses its own improved rate.  On the *anchor* basis the table is used
    unprojected, which is what the worked example's survival curve is.
    ``mort_ae_factor`` is the experience A/E overlay, **[std]** at 1.00 - the notes set
    the deferral-phase A/E at 1.00 and give no number for the payout phase, the 2020-2024
    study being cited without a factor [R15][REG-R61].
    """
    q = mort_rate_base(t, life)
    if mort_basis() == "generational":
        k = calendar_year(t) - mort_table_year                       # noqa: F821
        q = q * (1.0 - improvement_rate(t, life)) ** k
    return min(1.0, mort_ae_factor * q)                              # noqa: F821


def mort_rate_mth(t, life):
    """q(t) = 1 - (1 - q_annual)^(1/12): the probability of death during month t **[std]**."""
    return 1.0 - (1.0 - mort_rate(t, life)) ** (1.0 / 12.0)


def lives_if(t, life):
    """l(t): the probability that ``life`` is alive at the **start** of month t.

    ``l(0) = 1`` and ``l(t+1) = l(t) * (1 - q(t))``, equation (9) - the only decrement
    in the product.  There is no lapse and no annuitization decrement: VM-22's
    standard-projection lapse section is "not applicable" to contracts with no account
    value or surrender benefit, and annuitization is prescribed at 0% [R9].
    Returns 0 for ``life = 2`` on a single-life contract.
    """
    if life == 2 and not is_joint():
        return 0.0
    if t <= 0:
        return 1.0
    return lives_if(t - 1, life) * (1.0 - mort_rate_mth(t - 1, life))


def lives_death(t, life):
    """d(t) = l(t) - l(t+1): the deaths of ``life`` **during** month t.

    Note the index.  Month ``t`` spans elapsed months ``[t, t+1)`` on this 0-based grid,
    so the density is a forward difference; the 1-based chassis writes the same quantity
    as ``l(t-1) - l(t)``.
    """
    return lives_if(t, life) - lives_if(t + 1, life)


def lives_if_last(t):
    """l_last(t): the probability at least one covered life is alive at the start of t.

    ``l_1 + l_2 - l_1*l_2`` on a joint contract, under **joint-life independence
    [std]**; ``l_1`` on a single-life contract, which is why no separate ``l_alive``
    cells is needed.
    """
    l1 = lives_if(t, 1)
    if not is_joint():
        return l1
    l2 = lives_if(t, 2)
    return l1 + l2 - l1 * l2


def lives_death_last(t):
    """d_last(t) = l_last(t) - l_last(t+1): the last-death density in month t.

    Also the death that terminates the income stream and triggers the refund, and - on
    a joint contract, where the first death leaves the contract running on the option
    chosen at issue [S2] - the death that triggers the deferral death benefit.
    """
    return lives_if_last(t) - lives_if_last(t + 1)


def pols_if(t):
    """Contracts in force at the start of month t: ``pols_if_init * l_last(t)``.

    The notes weight the maintenance expense by ``l(t)`` alone.  The payout chassis
    instead uses ``max(C(t), l_alive(t))``, so that a certain-period obligation running
    on after the last death still carries expense; the two notes files differ here and
    this model follows its own.  They coincide on every form without a certain floor,
    the anchor cell included.
    """
    return pols_if_init() * lives_if_last(t)


def pricing_disc_factor(yrs):
    """v^yrs on the pricing interest rate i_p **[std]**.

    Contractual, not a valuation discount: this is the kernel that turns a premium into
    guaranteed income.  No DIA source discloses a pricing rate - the Compact relieves
    the insurer of disclosing the deferral-period basis altogether [R13 SS1.B(1)(a)] -
    so 4.75% is a modeling assumption, readable as a long-duration general-account
    portfolio yield net of default costs.
    """
    return (1.0 + pricing_rate) ** (-yrs)                            # noqa: F821


def deferral_yrs(t):
    """d_k = (T - t)/12: the remaining deferral in years of a premium paid in month t."""
    return (income_start_mth_at(t) - t) / 12.0


def surv_to_income_start(t):
    """_d p_x(t): survival of the primary life from month t to the income start month.

    A ratio on the single survival curve anchored at issue, which is how the notes
    derive ``_15p_65 = _20p_60 / _5p_60 = 0.715000/0.975000 = 0.733333``.
    """
    base = lives_if(t, 1)
    if base <= 0.0:
        return 0.0
    return lives_if(income_start_mth_at(t), 1) / base


def annuity_factor(start_mth, guar_mths, int_rate, from_mth):
    """The APV at month ``from_mth`` of $1 per annum of income beginning at ``start_mth``.

    Equation (2) generalized.  The k-th instalment is certain while ``k * 12/m`` does not
    exceed ``guar_mths`` and life-contingent after that, the payment factor being the
    same ``max(C, L)`` the projection uses, with the survival probabilities taken
    **conditional on being alive at** ``from_mth``::

        a = sum over k of (1/m) * v^((s_k - from_mth)/12) * max(C_k, L_k)

    Called with ``from_mth = start_mth`` it is ``a^(m)_y(f; i)``, the payout factor at
    the income start age; called with ``from_mth = t`` it is ``a_def(x(t), d, f; i)``
    directly, which is what makes the joint forms work.  Equation (15)'s expansion
    ``a_def^(both) + s * sum_i a_def^(only i)`` is algebraically this sum with the
    *either* trigger, so no separate joint kernel is needed.  The convertible variant,
    equation (16), is **not implemented**; the base is non-convertible **[std]**.

    The certain instalments are weighted by the probability that the income phase is
    reached at all - see :func:`surv_to_payout`.  Without that weight the deferred
    factor would treat a guarantee period as payable to an annuitant who died in the
    deferral, and equation (1)'s ``v^d * _d p_x * a^(m)`` would not be recovered.
    """
    v = 1.0 / (1.0 + int_rate)
    m = payment_freq()
    step = 12 // m
    adv = payment_timing() == "advance"
    l1f = lives_if(from_mth, 1)
    if l1f <= 0.0:
        return 0.0
    jt = is_joint()
    l2f = lives_if(from_mth, 2) if jt else 1.0
    dlt = survivor_pct()
    trig = reduction_trigger()
    q1 = lives_if(start_mth, 1) / l1f
    if jt and l2f > 0.0:
        q2 = lives_if(start_mth, 2) / l2f
        p_start = q1 + q2 - q1 * q2
    else:
        p_start = q1
    last = horizon_mths()
    total = 0.0
    k = 1
    while True:
        off = (k - 1) * step if adv else k * step
        s = start_mth + off
        if s > last:
            break
        cert = p_start if k * step <= guar_mths else 0.0
        p1 = lives_if(s, 1) / l1f
        if jt and l2f > 0.0:
            p2 = lives_if(s, 2) / l2f
            if trig == "either":
                lf = p1 * p2 + dlt * (p1 + p2 - 2.0 * p1 * p2)
            else:
                lf = p1 + dlt * (1.0 - p1) * p2
        else:
            lf = p1
        total += (1.0 / m) * v ** ((s - from_mth) / 12.0) * max(cert, lf)
        k += 1
    return total


def guarantee_mths_pricing():
    """n_g in months as fed into the pricing kernel, equation (5).

    ``n_g = CP(T) / B`` puts ``B`` on both sides, and the notes' listed pitfall is
    "failing to iterate leaves a systematic bias in the derived guarantee period and
    hence in the income".  Resolved here by fixed-point iteration from a life-only
    start, the notes' own prescription ("three iterations from a life-only start are
    ample") - ``pricing_iters`` carries the count.  The equation (5) approximation is
    used for **both** refund forms **[std]**; the exact cash-refund factor of equation
    (6) is not implemented.
    """
    f = payout_form()
    if f == "PC":
        return float(12 * certain_period())
    if f == "LO":
        return 0.0
    cp = sum(premium_by_mth().values())
    n = 0.0
    for _ in range(pricing_iters):                                   # noqa: F821
        inc = 0.0
        for tk, pk in premium_by_mth().items():
            a = annuity_factor(income_start_mth_at(tk), n, pricing_rate, tk)  # noqa: F821
            if a > 0.0:
                inc += pk * ((1.0 - expense_load) - rop_factor(tk)) / a  # noqa: F821
        if inc <= 0.0:
            return 0.0
        n = 12.0 * cp / inc
    return n


def payout_factor_calc():
    """a^(m) at the income start age computed from the shipped table, equation (2)."""
    t = income_start_mth()
    return annuity_factor(t, guarantee_mths_pricing(), pricing_rate, t)  # noqa: F821


def payout_factor():
    """a^(m)_{x+d}(f; i_p): the payout annuity factor in force.

    On the *table* basis the notes' illustrative value - 8.60 for the anchor cell's
    ``a^(12)_80(cash refund, female; 4.75%)`` - read from *payout_factor_table.csv*
    **[std]**; on the *formula* basis :func:`payout_factor_calc`.  No insurer publishes
    payout factors for this product and the Compact does not require the basis to be
    disclosed at all [R13 SS1.B(1)(a)].
    """
    if factor_basis() == "formula":
        return payout_factor_calc()
    key = (age(income_start_mth(), 1), sex(1), payout_form())
    return float(data.payout_factor_table().loc[key, "payout_factor"])  # noqa: F821


def rop_factor_calc(t):
    """A_rop for a premium paid in month t, by the notes' mid-band approximation.

    Equation (3) is a monthly sum; the notes state their illustrative factors were
    "computed from the same survival anchors with a mid-band death-timing
    approximation", which is what this implements: deaths in each five-year band of the
    deferral, discounted from the midpoint of the band.  Zero when the contract carries
    no deferral death benefit, which is the ``1{db_form = ROP}`` indicator of (4).

    **The exposure is the last-death curve** ``l_last``, not the primary life's.
    Equation (3) is written on a single life ``x`` and the notes never restate it for a
    joint contract, but the benefit this factor has to pay for is the one
    :func:`claims` projects, and on a joint contract that attaches to the **last** death
    - "if one annuitant dies in deferral the contract continues on the option chosen at
    issue" [S2], so the return of premium falls due only when the contract ends.
    Pricing the primary life's death density instead would charge for an exposure 2.5
    times the one projected (0.161605 against 0.064105 on the joint model point) and
    understate the income the premium buys by about 12.5% - the notes' own listed
    pitfall that the deferral death benefit's cost "belongs in the purchase rate (4)
    *and* in the projected cash flows", read as requiring the *same* benefit in both.
    On a single-life contract ``l_last`` **is** the primary curve, so this changes
    nothing on the worked example.
    """
    if db_form() != "ROP":
        return 0.0
    end = income_start_mth_at(t)
    base = lives_if_last(t)
    if base <= 0.0:
        return 0.0
    total = 0.0
    lo = t
    while lo < end:
        hi = min(lo + 60, end)
        s0 = lives_if_last(lo) / base
        s1 = lives_if_last(hi) / base
        mid = ((lo - t) + (hi - t)) / 24.0
        total += (s0 - s1) * pricing_disc_factor(mid)
        lo = hi
    return total


def rop_factor(t):
    """A_rop(x(t), d; i_p): the return-of-premium factor for a premium paid in month t.

    On the *table* basis the notes' illustrative values from *rop_factor_table.csv*
    **[std]**; on the *formula* basis :func:`rop_factor_calc`.  The two disagree on the
    twenty-year slice - 0.157900 printed against 0.161605 computed - while agreeing to
    four decimals on the fifteen-year slice; both readings are shipped and a test pins
    the gap open.  See the Space docstring.
    """
    if db_form() != "ROP":
        return 0.0
    if factor_basis() == "formula":
        return rop_factor_calc(t)
    key = (age(t, 1), sex(1), int(round(deferral_yrs(t))))
    return float(data.rop_factor_table().loc[key, "rop_factor"])     # noqa: F821


def annuity_factor_def(t):
    """a_def(x(t), d, f; i_p): the APV at month t of $1 p.a. of income from T, eq (1).

    On the *table* basis, equation (1) literally, ``v^d * _d p_x * a^(m)``.  That
    factorization is single-life only - a joint status does not separate into a deferral
    survival times a payout APV - so a joint model point must use the *formula* basis,
    where the whole deferred stream is valued in one pass by :func:`annuity_factor`.
    """
    if factor_basis() == "table":
        if is_joint():
            raise ValueError("factor_basis 'table' is single-life only")
        return (pricing_disc_factor(deferral_yrs(t))
                * surv_to_income_start(t) * payout_factor())
    return annuity_factor(income_start_mth_at(t), guarantee_mths_pricing(),
                          pricing_rate, t)                           # noqa: F821


def purchase_rate(t):
    """pr(x(t), d, f): annual income bought per $1 of premium paid in month t, eq (4).

    ``pr = [ (1 - L) - 1{ROP} * A_rop ] / a_def`` - the equivalence principle applied
    **per premium**, which is the core of the product: income is additive across slices,
    each priced at the annuitant's attained age and the remaining deferral **at its own
    payment date** [R13 SS3.B(1)(b)][S3].  Nothing accumulates and there is no balance to
    roll forward.  The whole kernel is **[std]**: no purchase-rate table was obtained
    and none is published.  ``purchase_rate_dp`` rounds the result, 6 on the worked
    example's model point; see the Space docstring.
    """
    a = annuity_factor_def(t)
    if a <= 0.0:
        return 0.0
    pr = ((1.0 - expense_load) - rop_factor(t)) / a                  # noqa: F821
    dp = purchase_rate_dp()
    return pr if dp < 0 else round(pr, dp)


def adjust_income_factor():
    """B'/B on a start-date adjustment, equation (11).

    Actuarial equivalence at the exercise month **[std]**::

        B' = B(t_e) * a_def(x(t_e), (T - t_e)/12, f; i_e)
                    / a_def(x(t_e), (T' - t_e)/12, f; i_e)

    ``a_def`` decreases in the deferral, so deferring the date raises the payment and
    advancing it lowers it, matching the extended case's statement [S4][S5].  Two
    refinements the disclosed recipe does not mention are **flagged rather than
    modeled**, as the notes require: the return-of-premium exposure changes with the
    deferral length, and ``CP`` is unchanged so the derived guarantee period shifts.
    """
    a = adjust_mth()
    if a < 0:
        return 1.0
    i = repricing_rate()
    n = guarantee_mths_pricing()
    old = annuity_factor(income_start_mth_init(), n, i, a)
    new = annuity_factor(adjust_start_mth(), n, i, a)
    if new <= 0.0:
        return 1.0
    return old / new


def annual_income(t):
    """B(t): the guaranteed annual income purchased to date, before COLA, equation (8).

    ``B(t) = B(t-1) + sum of P_k * pr(x(t_k), (T - t_k)/12, f)``, ``B(-1) = 0``, plus
    the repricing factor of equation (11) in the month a start-date adjustment is
    exercised.  Income is **additive across slices** and each slice is fully guaranteed
    from the moment its premium is paid [R13 SS3.H(1)].
    """
    if t < 0:
        return 0.0
    b = annual_income(t - 1)
    if t == adjust_mth():
        b = b * adjust_income_factor()
    p = premium_pp(t)
    if p:
        b = b + p * purchase_rate(t)
    return b


def guarantee_yrs():
    """n_g realized: the derived guarantee period in years, equation (5).

    ``CP(T) / B(T)`` on the refund forms - 150,000/44,259.65 = 3.3891 years on the
    anchor cell, so its cash-refund guarantee is exhausted during the fourth payment
    year, at attained age about 83.4.  The elected period on a PC form, zero on a life
    only form.  Distinct from :func:`guarantee_mths_pricing`, which is the fixed point
    the *kernel* uses before ``B`` is known.
    """
    f = payout_form()
    if f == "PC":
        return float(certain_period())
    if f == "LO":
        return 0.0
    t = income_start_mth()
    b = annual_income(t)
    return 0.0 if b <= 0.0 else cum_premium_pp(t) / b


def is_payout(t):
    """Whether month t is in the income phase, ``t >= T``.

    Deaths in months ``t < T`` are deferral-phase deaths attracting the return of
    premium; deaths in months ``t >= T`` are payout-phase deaths attracting the form's
    refund benefit.
    """
    return t >= income_start_mth()


def phase(t):
    """DEFERRAL, PAYOUT or TERMINATED in month t."""
    if t > proj_len():
        return "TERMINATED"
    return "PAYOUT" if is_payout(t) else "DEFERRAL"


def is_payment_mth(t):
    """Whether an instalment falls in month t.

    Arrears: the k-th instalment falls at the **end** of month ``T + k*(12/m) - 1``, so
    the first lands at the end of month ``T`` when ``m = 12`` - one payment period after
    the income start date, which is why policy year 21 of the anchor cell carries the
    first twelve payments.  Advance: the k-th falls at the **start** of month
    ``T + (k-1)*(12/m)``, one full payment period earlier.
    """
    if not is_payout(t):
        return False
    step = 12 // payment_freq()
    off = t - income_start_mth()
    if payment_timing() == "arrears":
        return (off + 1) % step == 0
    return off % step == 0


def payment_surv_mth(t):
    """The elapsed month at which survival is measured for the instalment falling in t.

    Arrears: the end of month t, which on this 0-based grid is elapsed month ``t + 1``.
    Advance: the start of month t, elapsed month ``t``.  Using end-of-period survival
    for advance payments understates the liability by about one period's mortality per
    payment.
    """
    return t + 1 if payment_timing() == "arrears" else t


def cola_factor(t):
    """(1+c)^floor((t-T)/12): the COLA escalation applying in month t.

    Fixed compound, on each anniversary of the income start date, elected at issue and
    irrevocable [S2][S3][S4].  One in the deferral and in the first payout year.
    """
    d = t - income_start_mth()
    if d < 0:
        return 1.0
    return (1.0 + cola_rate()) ** (d // 12)


def annuity_pp_sched(t):
    """inst(t) = B(t)/m * (1+c)^floor((t-T)/12): the scheduled instalment per contract.

    Zero outside payment months.  Scheduled, not paid: an acceleration blackout or a
    commutation may suppress it.
    """
    if not is_payment_mth(t):
        return 0.0
    return annual_income(t) / payment_freq() * cola_factor(t)


def cum_annuity_pp(t):
    """G(t): cumulative scheduled instalments per contract through the end of month t.

    A **deterministic** as-if-alive schedule - instalments payable while any covered
    life is alive follow the deterministic escalation path - so the refund balance needs
    no path simulation.
    """
    if t < 0:
        return 0.0
    return cum_annuity_pp(t - 1) + annuity_pp_sched(t)


def certain_mths_refund():
    """n_R: the certain period an installment refund derives, in months.

    Payments "continue in the same amount and frequency until they equal the purchase
    payments" [S2], so ``n_R`` is the offset of the first payment month at which
    cumulative instalments reach ``CP(T)``.  Searched rather than closed so that a COLA
    path still resolves, and bounded by the mortality horizon so that it never depends
    on :func:`proj_len`, which depends on it.  **[std]**: the month grid rounds the
    guarantee **up** to a whole instalment rather than trimming the last one, which is
    what the notes' "exactly a certain-and-life annuity with n_g = CP(T)/B" framing
    implies; the payout chassis trims instead.
    """
    t0 = income_start_mth()
    cp = cum_premium_pp(t0)
    step = 12 // payment_freq()
    t = t0 if payment_timing() == "advance" else t0 + step - 1
    last = horizon_mths()
    while t <= last:
        if cum_annuity_pp(t) >= cp:
            return t - t0 + 1
        t += step
    return max(0, last - t0)


def certain_mths_eff():
    """n_eff: the effective certain period in months, by payout form.

    ``12 * n`` on a period certain form; ``n_R`` on installment refund; **zero on cash
    refund and life only**.  A cash refund is a lump-sum shortfall paid at death, not a
    stream of guaranteed payments - equation (5) treats it as certain-and-life for
    *pricing* only, and carrying that into the projection would pay the guarantee twice.
    """
    f = payout_form()
    if f == "PC":
        return 12 * certain_period()
    if f == "IR":
        return certain_mths_refund()
    return 0


def certain_floor(t):
    """C(t) = 1{the instalment in month t falls inside the guarantee period}."""
    if not is_payout(t):
        return 0.0
    return 1.0 if (t - income_start_mth()) < certain_mths_eff() else 0.0


def payment_factor_life(t):
    """L(t): the life-contingent payment factor for the instalment falling in month t.

    Survival is measured at :func:`payment_surv_mth`, not at t.  By form and trigger::

        single life:           L = l_1
        joint, trig = either:  L = l_1*l_2 + delta*(l_1 + l_2 - 2*l_1*l_2)
        joint, trig = primary: L = l_1 + delta*(1 - l_1)*l_2

    The *either* form pays the full instalment while **both** are alive and delta while
    **exactly one** is; the *primary* form pays in full while the primary lives whatever
    the joint annuitant's status.  The two coincide on the primary's death and differ
    only on the secondary's, which is why the trigger is a switch and not a footnote.
    Zero before the income start date.
    """
    if not is_payout(t):
        return 0.0
    s = payment_surv_mth(t)
    l1 = lives_if(s, 1)
    if not is_joint():
        return l1
    l2 = lives_if(s, 2)
    d = survivor_pct()
    if reduction_trigger() == "either":
        return l1 * l2 + d * (l1 + l2 - 2.0 * l1 * l2)
    return l1 + d * (1.0 - l1) * l2


def surv_to_payout():
    """l_last(T): the probability that the income phase is ever reached.

    **The one place the payout chassis cannot be carried across unexamined.**  A SPIA
    is already in payment, so ``SPIA_US_S`` weights its certain floor by
    nothing: ``C(t)`` is a bare indicator.  A DIA's guarantee period only begins if the
    contract reaches the income start date - an annuitant who dies in the deferral
    receives the return-of-premium benefit and no instalment is ever paid - so on an
    expected basis the certain instalments carry this factor.  Without it a period
    certain or installment refund contract would pay its guarantee with probability
    one and overstate the liability by the whole deferral mortality.  The DIA notes
    inherit ``L_pay`` and its "certain inside a guarantee period" wording from the
    immediate-annuity notes without adjusting for the deferral; this is that
    adjustment, and it is the same weight equation (1) applies through ``_d p_x``.
    """
    return lives_if_last(income_start_mth())


def payment_factor(t):
    """Phi(t) = max(C(t) * l_last(T), L(t)): the master payment factor.

    The ``max`` makes the certain period an annuity-**certain floor** rather than an
    additional stream: during the guarantee the full unreduced instalment is payable
    regardless of survival *after the income start date*, and the ``max`` prevents
    paying ``1 + L``.  An additive construction silently doubles the guarantee - the
    payout chassis' first-listed pitfall - and, because the floor pays the *unreduced*
    instalment, it also reproduces with no extra flag the rule that a survivor reduction
    inside a guarantee period is deferred to the end of that period [S1][S3].  The
    ``l_last(T)`` weight on the floor is the DIA's own; see :func:`surv_to_payout`.
    """
    return max(certain_floor(t) * surv_to_payout(), payment_factor_life(t))


def refund_balance(t):
    """RG(t) = max(0, CP(T) - income scheduled through the end of month t-1).

    The ``t-1`` is the arrears convention: an instalment due at the end of the death
    month has not been paid, so a death between ``T`` and ``T + 1/m`` yields a cash
    refund of the **full** ``CP(T)``.  On advance timing an instalment paid at the
    *start* of the death month **has** been paid, so the balance is measured at ``t``
    there or the lump sum is overstated by one instalment.
    """
    t0 = income_start_mth()
    if t < t0:
        return 0.0
    adv = payment_timing() == "advance" and is_payment_mth(t)
    return max(0.0, cum_premium_pp(t0) - cum_annuity_pp(t if adv else t - 1))


def accel_blackout(t):
    """Whether payments are suspended in month t by a payment acceleration.

    Six monthly payments are made in one sum at ``t_a`` and no payment is made for the
    following five months [S1][S4].  The feature is expressly "not a liquidity feature"
    [S2] - a timing shift, not a withdrawal - and modelling it as a withdrawal is one of
    the notes' listed pitfalls.
    """
    a = accel_mth()
    if a < 0:
        return False
    return a < t <= a + accel_months - 1                             # noqa: F821


def accel_cost():
    """Cost(t_a): the economic cost of a payment acceleration, equation (12).

    ``(B/m) * sum over j = 1..n_a-1 of [ 1 - v^(j/m) * _{j/m} p_x(t_a) ]``.  Accelerated
    payments are made **unconditionally**, so the insurer forgoes the survivorship and
    interest discount on payments 2 through ``n_a``.  Small but real, and the reason the
    feature is capped in uses and gated at age 59 1/2 - the gate itself being driven by
    the IRC SS72(q) 10% additional tax [R8][REG-R55].  Reported, not added to the cash
    flows: the cost is already implicit in paying them early through
    :func:`accel_payment_factor`.  Only the **mortality** element of it surfaces in the
    projected cash flows, because they are undiscounted - on the anchor configuration
    435.11 per exercising contract here against 153.52 of extra lifetime income outgo,
    the difference being the interest term ``v^(j/m)`` that an undiscounted projection
    has nowhere to put.
    """
    a = accel_mth()
    if a < 0:
        return 0.0
    base = lives_if(a, 1)
    if base <= 0.0:
        return 0.0
    inst = annual_income(a) / payment_freq() * cola_factor(a)
    total = 0.0
    for j in range(1, accel_months):                                 # noqa: F821
        sp = lives_if(a + j, 1) / base
        total += 1.0 - pricing_disc_factor(j / 12.0) * sp
    return inst * total


def accel_payment_factor(t):
    """Phi for an instalment scheduled in month t but paid in the acceleration lump sum.

    The six instalments are paid **in one sum** at ``t_a`` [S1][S4], so the five that are
    pulled forward are paid **unconditionally**: their survivorship is frozen at the date
    the lump sum falls - ``payment_factor_life(t_a)``, the same weight the first
    instalment of the block carries - instead of being measured at their own scheduled
    dates.  That frozen weight *is* the mortality element equation (12) prices; the
    interest element of (12) does not appear in an undiscounted projection.

    A **guaranteed** instalment is untouched.  Its weight is already
    ``C(t) * l_last(T)``, independent of survival after the income start date, so
    accelerating it forgoes no survivorship - which is why the ``max`` is taken against
    the certain floor exactly as :func:`payment_factor` does, and why equation (12)'s
    cost is zero inside a guarantee period and strictly positive outside it.  Zero when
    no acceleration is exercised.
    """
    a = accel_mth()
    if a < 0:
        return 0.0
    return max(certain_floor(t) * surv_to_payout(), payment_factor_life(a))


def commute_frac_cum(t):
    """theta_cum(t): the cumulative commuted fraction applying in month t.

    Zero before the exercise month and ``commute_frac`` from it, the exercise falling at
    the **start** of the month and so reaching that month's own instalment - the notes'
    processing order puts option exercises ahead of the income payment.  It multiplies
    ``C(t)`` in :func:`annuity_pp_paid`, so it reaches guaranteed instalments only: if
    the annuitant is alive when the would-be guarantee period ends, income **resumes
    until death**, the life-contingent tail not being commuted [S4].  Applying it to
    that tail contradicts every retrieved contract.
    """
    c = commute_mth()
    if c < 0 or t < c:
        return 0.0
    return commute_frac()


def commute_weight(t):
    """l_last(t_c): the expected size of the cohort a commutation extinguishes in month t.

    **The one weight the payout chassis has no need for, and the mirror image of**
    :func:`surv_to_payout`.  A commutation is exercised by an owner who is *alive* at
    ``t_c`` [S4], so it can only extinguish the guaranteed instalments of the
    ``l_last(t_c)`` sub-cohort.  The rest of the cohort that reached the income phase -
    ``l_last(T) - l_last(t_c)``, contracts whose annuitant died between ``T`` and ``t_c``
    - keeps its guarantee running to the beneficiary and is unaffected.  On the shipped
    commutation model point those two weights are ``0.715000`` and ``0.680338``, and
    ``l_last(t_c)`` is the one this model applies: applying the
    commutation to all of the first would cancel 4.85% more guaranteed liability than
    the commuted value pays for.

    Zero outside a guarantee period, before the exercise month, and on a contract that
    never commutes.  Bounded above by :func:`payment_factor` because ``t_c >= T``, so
    the surviving expected instalment is never negative.
    """
    c = commute_mth()
    if c < 0 or t < c or certain_floor(t) == 0.0:
        return 0.0
    return lives_if_last(c)


def commute_disc_rate(t):
    """i_c(t) = i_p + max(0, r_ref(t) - r_ref(0)) + m_c: the commutation rate, eq (13).

    One-sided by construction - it rises with rates and does not fall - implementing the
    Compact's stated intent that the adjustment "reduce interest risk in the event of
    rising interest rate after issue" and its required disclosure that "the higher the
    interest rate the lower the commuted value" [R13 SS3.F(7)].  **The actual contractual
    formula is not published anywhere** [S4][S5], so this is **[std]** and
    **[unverified]**; ``ref_rate_shift`` is a flat scalar because a reference-rate path
    would be another input table.
    """
    return pricing_rate + max(0.0, ref_rate_shift) + commute_margin  # noqa: F821


def commuted_value(t):
    """CV(t): the commuted value of the remaining guaranteed payments, equation (14).

    ``sum over j in J_g(t) of (B/m) * (1 + i_c(t))^(-(j - t)/12)``, where ``J_g`` is the
    set of remaining **guaranteed** payment months.  Zero on a form with no guaranteed
    stream: a cash refund is a lump sum at death, not a schedule of payments, so there
    is nothing to commute.  Non-zero only in the exercise month.
    """
    c = commute_mth()
    if c < 0 or t != c:
        return 0.0
    n_eff = certain_mths_eff()
    if n_eff <= 0:
        return 0.0
    end = income_start_mth() + n_eff
    i = commute_disc_rate(t)
    total = 0.0
    for s in range(max(t, income_start_mth()), end):
        inst = annuity_pp_sched(s)
        if inst:
            total += inst * (1.0 + i) ** (-(s - t) / 12.0)
    return total * commute_frac()


def commutations(t):
    """E[COMM(t)]: the commutation payment made to the owner in month t.

    ``CV(t) * l_last(t)``: the commuted value is paid to the cohort alive to exercise,
    which is the **same** ``l_last(t_c)`` weight :func:`commute_weight` removes from the
    guaranteed instalments.  The two must agree, and :func:`check_commutation_value`
    asserts that they do - discounted at ``i_c``, the value paid out equals the value
    suppressed.  Zero in the base run - commutation exists only in the extended case
    [S4][S5] - and prohibited on a QLAC after the required beginning date other than a
    rescission period not exceeding 90 days [R1 (q)(1)(iv)][R2 SS202(a)(4)].
    """
    return pols_if_init() * lives_if_last(t) * commuted_value(t)


def annuity_pp(t):
    """The instalment per contract payable in month t, before commutation and survival.

    Equal to :func:`annuity_pp_sched` except during an acceleration blackout, where the
    payment has already been made in one sum at the exercise month.
    """
    if accel_blackout(t):
        return 0.0
    return annuity_pp_sched(t)


def annuity_pp_paid(t):
    """inst(t) * (1 - theta_cum(t) * C(t)): the instalment a **commuting** contract gets.

    A commutation reduces guaranteed instalments only; the life-contingent payments
    after the guarantee period are untouched, which is what makes the tail resume.  Per
    contract, and only for a contract that actually commuted - which is a sub-cohort,
    not the whole model point, so :func:`annuity_payments` applies it through
    :func:`commute_weight` rather than to the expected instalment as a whole.
    """
    return annuity_pp(t) * (1.0 - commute_frac_cum(t) * certain_floor(t))


def annuity_payments(t):
    """E[income] in month t: the instalment weighted over the cohorts entitled to it.

    Two cohort splits sit on top of the chassis' ``inst(t) * Phi(t)``, and both are
    weights rather than per-contract adjustments::

        E[income](t) = pols * [ inst(t) * (Phi(t) - w_c(t))          not commuted
                              + inst_paid(t) * w_c(t) ]              commuted

    ``w_c(t)`` is :func:`commute_weight`, the ``l_last(t_c)`` sub-cohort that was alive
    to exercise the commutation; ``inst_paid`` is that sub-cohort's reduced instalment.
    Multiplying ``inst_paid`` by the whole of ``Phi`` instead - the obvious reading of
    the chassis formula - would cancel the guarantee of contracts whose annuitant died
    between ``T`` and ``t_c`` and could not have commuted.

    In the exercise month of a payment acceleration the following ``n_a - 1``
    instalments are added at :func:`accel_payment_factor`, the survivorship frozen at
    the lump sum's own date - they are paid whether or not the annuitant survives to
    their scheduled dates, which is precisely the mortality element equation (12)
    measures - and the months they would have fallen in pay nothing.
    """
    w = commute_weight(t)
    total = pols_if_init() * (annuity_pp(t) * (payment_factor(t) - w)
                              + annuity_pp_paid(t) * w)
    a = accel_mth()
    if a >= 0 and t == a:
        for j in range(1, accel_months):                             # noqa: F821
            total += (pols_if_init() * annuity_pp_sched(a + j)
                      * accel_payment_factor(a + j))
    return total


def claim_pp(t, kind):
    """The claim amount per contract in month t, by ``kind``.

    ``"DEATH"`` - the deferral death benefit, 100% of cumulative premiums paid without
    interest as a lump sum at the end of the month of death
    [S1][S2][S3][S4][R13 SS3.I(1)(a)], zero once the income phase starts and zero on a
    no-death-benefit form.  ``"REFUND"`` - the cash-refund shortfall
    :func:`refund_balance`, zero on any form other than cash refund, because installment
    refund and period certain deliver their guarantee as continued payments through the
    certain floor rather than as a lump sum.
    """
    if kind == "DEATH":
        if is_payout(t) or db_form() != "ROP":
            return 0.0
        return cum_premium_pp(t)
    if kind == "REFUND":
        if not is_payout(t) or payout_form() != "CR":
            return 0.0
        return refund_balance(t)
    raise ValueError("invalid kind")


def claims(t, kind=None):
    """Expected claim outgo in month t; ``kind=None`` totals every kind.

    Weighted by :func:`lives_death_last`, the death that ends the contract: on a joint
    contract the first death leaves the contract running on the option chosen at issue
    [S2], so both the deferral death benefit and the refund attach to the last death.
    The two kinds are mutually exclusive by construction - ``"DEATH"`` is zero from the
    income start month and ``"REFUND"`` is zero before it.
    """
    if kind is None:
        return claims(t, "DEATH") + claims(t, "REFUND")
    return pols_if_init() * lives_death_last(t) * claim_pp(t, kind)


def premiums(t):
    """Premium income in month t: ``l(t) * sum of P_k at t``, received at the start.

    Deterministic schedule with no attrition **[std]**: DIA subsequent premiums are
    wholly discretionary and no source publishes a distribution of them.  Dump-in risk
    differs structurally from a fixed deferred annuity's - each premium is priced at
    *then-current* rates, so there is no rate guarantee to select against unless the
    contract guarantees paid-up rates for future premiums [R13 SS1.B(1)(h)], which is off
    in the base **[std]**.
    """
    return pols_if_init() * premium_pp(t) * lives_if_last(t)


def inflation_factor(t):
    """The expense escalation factor in month t: ``(1 + g)^(y(t) - 1)``."""
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """E[EXP(t)] = (e/12) * (1+g)^(y-1) * l(t): maintenance expense in month t.

    $50 per contract per year escalated at 2.5%: VM-22 prescribes exactly that for
    individual Payout Annuity Reserving Category contracts, plus 7 basis points on a
    present-value base for contracts without an account value [R9]; adopting the
    prescribed figure as the best estimate is **[std]**, and the 7 bp element is not
    implemented because this model computes no present-value base.
    """
    return expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821


def liability_outgo(t):
    """Total gross liability outgo in month t, outgo positive.

    Income payments, death and refund benefits, any commutation, and maintenance
    expense.  **There is no surrender cash flow row, and none should be added** - the
    contract has no cash surrender value at any time before the income start date and
    none after [S1][S2][R13 SS3.P].
    """
    return annuity_payments(t) + claims(t) + commutations(t) + expenses(t)


def liability_cf(t):
    """The net liability cash flow in month t, **outgo positive**: ``-net_cf(t)``.

    Across this library ``liability_cf`` is the net stream carried under the sign the
    notes that print one use, and ``net_cf`` is the same stream income-positive; the
    invariant ``net_cf(t) == -liability_cf(t)`` holds in every model that publishes both,
    and a conventions test asserts it.

    The distinction that matters here: the notes' purpose statement projects "premiums in;
    deferral death benefits, income..." , so premium income belongs in the net stream.
    That makes this product differ from the :mod:`~.SPIA_US_S` payout chassis it
    otherwise follows, where the single premium is a pricing input and never a projected
    cash flow, so there gross outgo and the net stream coincide.  The gross outgo alone is
    :func:`liability_outgo`.
    """
    return liability_outgo(t) - premiums(t)


def net_cf(t):
    """Net cash flow to the insurer in month t: premium income less liability outgo.

    The sign convention of ``Term_US_A.net_cf``.  Unlike the immediate-annuity chassis
    this product **does** carry premium income in the projection, because premiums are
    flexible and fall throughout the deferral - so premium income nets here, and
    :func:`liability_cf` is this stream negated rather than the gross outgo
    :func:`liability_outgo`.
    """
    return premiums(t) - liability_outgo(t)


def qlac_room(t):
    """qlac_room(t) = Limit - CP(t) - premiums paid to any other intended QLAC.

    $200,000 as enacted, indexed with a base period of the calendar quarter beginning
    July 1 2022 and increments rounded to the next lowest multiple of $10,000;
    **$210,000 for 2026** [R1 (q)(2)(ii), (q)(4)(ii)(A)][R2 SS202(a)(2)][R3][S4].  There
    is **no percentage-of-account-balance limit**: SECURE 2.0 SS202(a)(1) directed its
    elimination and the codified text has no percentage test, so a 25% rule, a $125,000
    or $130,000 cap and an RMD age of 70 1/2 are all superseded arithmetic.
    """
    return qlac_premium_limit - cum_premium_pp(t) - other_qlac_premium()  # noqa: F821


def qlac_flags():
    """The QLAC conditions this contract fails; an empty list when it complies.

    The overlay generates **no cash flows of its own** - it caps premiums, restricts
    forms, constrains ``T``, disables features and raises compliance flags.  Loss of
    QLAC status changes the owner's RMD position, not the insurer's liability cash
    flows.  An excess premium ends QLAC status on the date paid unless returned by the
    end of the following calendar year; any other failure voids status retroactively to
    purchase [R1 (q)(4)(i)(B), (q)(4)(iii)(A)].  Empty on a contract that is not a QLAC.
    """
    if not is_qlac():
        return []
    out = []
    if qlac_room(proj_len()) < 0.0:
        out.append("premium limit exceeded")
    if age(income_start_mth(), 1) > qlac_max_start_age:              # noqa: F821
        out.append("income start after the age limit")
    if cola_rate() > 0.0:
        out.append("cost-of-living adjustment on a QLAC")
    if commute_mth() >= 0:
        out.append("commutation on a QLAC")
    if accel_mth() >= 0:
        out.append("payment acceleration on a QLAC")
    if payout_form() not in ("LO", "CR"):
        out.append("income form not permitted on a QLAC")
    return out


def check_lives_roll_fwd_resid(t):
    """Roll-forward residual in month t, over both lives, plus the last-survivor identity.

    ``sum_i [ l_i(t) - d_i(t) - l_i(t+1) ]`` and, on a joint contract,
    ``l_last(t) - [l_1 + l_2 - l_1*l_2]``.  Zero to floating point; non-zero if the
    independence construction and the per-life recursion ever disagree.  The signed float
    at a single ``t``, for the debugging session that follows a
    :func:`check_lives_roll_fwd` failure.
    """
    res = 0.0
    for i in (1, 2):
        res += lives_if(t, i) - lives_death(t, i) - lives_if(t + 1, i)
    if is_joint():
        l1, l2 = lives_if(t, 1), lives_if(t, 2)
        res += lives_if_last(t) - (l1 + l2 - l1 * l2)
    return res


def check_lives_roll_fwd():
    """``True`` when the in-force roll-forward closes in every projected month.

    No argument and a bool, the library-wide ``check_*`` shape taken from
    ``CashValue_SE.check_av_roll_fwd()``: one call covers ``t = 0 .. proj_len()``, so the
    same name can be asserted across every model in the library.
    :func:`check_lives_roll_fwd_resid` carries the signed residual at a single ``t``.
    Mortality is the only decrement here, so a failure means the last-survivor
    construction and the per-life recursion have come apart.
    """
    return all(abs(check_lives_roll_fwd_resid(t)) < 1e-12
               for t in range(0, proj_len() + 1))


def check_income_roll_fwd_resid(t):
    """``B(t) - B(t-1)*adj - P_k*pr`` in month t: the income roll-forward residual, eq (8).

    Zero to floating point.  Non-zero would mean income appearing from somewhere other
    than a premium slice or the one permitted repricing - and **nothing else can move
    it**: there is no credited rate, no index, no charge and no balance in this product.
    The signed float at a single ``t``; :func:`check_income_roll_fwd` is the bool.
    """
    prev = annual_income(t - 1)
    if t == adjust_mth():
        prev = prev * adjust_income_factor()
    bought = premium_pp(t) * purchase_rate(t) if premium_pp(t) else 0.0
    return annual_income(t) - prev - bought


def check_income_roll_fwd():
    """``True`` when income moves only by a premium slice or the permitted repricing.

    No argument and a bool over every projected ``t``, the library-wide ``check_*`` shape;
    :func:`check_income_roll_fwd_resid` returns the signed residual at one ``t``.  The
    tolerance is absolute rather than relative because ``B`` is a currency amount that
    only ever steps, never accrues.
    """
    return all(abs(check_income_roll_fwd_resid(t)) < 1e-9
               for t in range(0, proj_len() + 1))


def check_payment_factor_resid(t):
    """``Phi(t) - max(C(t)*l_last(T), L(t))`` in month t: the double-count residual.

    Zero by construction.  Computed anyway because an additive floor - ``C + L`` instead
    of ``max(C, L)`` - is the payout chassis' first-listed pitfall and would show up
    here as ``min(C, L)``.  :func:`check_payment_factor` is the bool over every ``t``.
    """
    return payment_factor(t) - max(certain_floor(t) * surv_to_payout(),
                                   payment_factor_life(t))


def check_payment_factor():
    """``True`` when Phi is the max of the two legs, never their sum, in every month.

    No argument and a bool, the library-wide ``check_*`` shape.  The comparison is exact
    rather than tolerant: the identity is arithmetical, so any residual at all is a
    defect and not a rounding artefact.
    """
    return all(check_payment_factor_resid(t) == 0.0
               for t in range(0, proj_len() + 1))


def check_commutation_value_resid(t):
    """``PV_ic(instalments suppressed) - commutations(t)`` in month t: the exchange residual.

    A commutation is an exchange, not a benefit: the owner gives up guaranteed
    instalments and receives their present value at ``i_c``.  On an expected basis the
    two legs must therefore carry the *same* cohort weight, and this residual is what
    catches it if they do not.

    The suppressed leg is read out of :func:`annuity_payments` itself rather than
    re-derived - what the projection would have paid, ``inst(s) * Phi(s)``, less what it
    does pay - so weighting the suppression by ``l_last(T)`` while paying the commuted
    value to ``l_last(t_c)`` shows up here as a leak equal to the difference: 6,898.37 on
    the shipped commutation model point.  The acceleration block is added back before the
    comparison so that the two options do not contaminate each other, though the
    contract's own six-month interlocks make that combination unreachable [S4].  Zero to
    floating point at the exercise month, and zero everywhere else because both legs are.
    :func:`check_commutation_value` is the bool over every ``t``.
    """
    c = commute_mth()
    if c < 0 or t != c:
        return 0.0
    a = accel_mth()
    i = commute_disc_rate(t)
    total = 0.0
    for s in range(t, income_start_mth() + certain_mths_eff()):
        paid = annuity_payments(s)
        if s == a:
            for j in range(1, accel_months):                          # noqa: F821
                paid -= (pols_if_init() * annuity_pp_sched(s + j)
                         * accel_payment_factor(s + j))
        supp = pols_if_init() * annuity_pp(s) * payment_factor(s) - paid
        total += supp * (1.0 + i) ** (-(s - t) / 12.0)
    return total - commutations(t)


def check_commutation_value():
    """``True`` when the commutation exchange closes in every projected month.

    No argument and a bool, the library-wide ``check_*`` shape;
    :func:`check_commutation_value_resid` returns the signed leak at one ``t``.
    Trivially ``True`` on a contract that never commutes, which is the base run - the
    residual is identically zero away from the exercise month.
    """
    return all(abs(check_commutation_value_resid(t)) < 1e-6
               for t in range(0, proj_len() + 1))


def lives_if_ann(y):
    """l at the **end** of policy year y: ``lives_if_last(12*y)``.

    The annual display's survival column.  Policy year ``y`` spans months
    ``12(y-1) .. 12y-1``, so surviving it means being alive at the start of month
    ``12y``.
    """
    return lives_if_last(12 * y)


def claims_ann(y, kind=None):
    """Expected claim outgo over policy year y; the notes' ``E[DB]`` when kind="DEATH".

    The monthly cash flows summed over the twelve months of the year.  Because ``CP`` is
    constant through a year whose premium falls at its start, this collapses to
    ``(l(y-1) - l(y)) * CP(y)`` on the annual grid - which is exactly how the worked
    example computes it.
    """
    return sum(claims(t, kind) for t in range(12 * (y - 1), 12 * y))


def annuity_payments_ann(y):
    """The notes' ``E[income]``: expected income at the end of policy year y.

    An **annual-payment display approximation**, not the sum of the year's monthly
    instalments: one year's income ``B`` escalated for COLA and weighted by survival to
    the end of the year.  The model runs monthly; this cells exists so that the notes'
    annual display table can be reproduced and asserted directly.  Zero in a policy year
    that ends before the income start month.
    """
    last = 12 * y - 1
    if last < income_start_mth():
        return 0.0
    return (pols_if_init() * annual_income(last) * cola_factor(last)
            * lives_if_ann(y))


def result_cf():
    """Result table of monthly cashflows, indexed by policy month t from 0."""
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
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
    ts = list(range(0, proj_len() + 1))
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


def result_annual():
    """The technical notes' annual display table, indexed by policy year.

    One row per policy year with the columns the worked example prints: the attained age
    at the start of the year, the premium received at its start, ``CP``, ``B``, the
    survival probability at the end of the year, the expected deferral death benefit
    paid during it, and the expected income at its end on the annual-payment display
    approximation.  The projection itself is monthly; this is the display grid.
    """
    ys = list(range(1, (proj_len() + 1) // 12 + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "age": [age(12 * (y - 1), 1) for y in ys],
            "premium_pp": [sum(premium_pp(t) for t in range(12 * (y - 1), 12 * y))
                           for y in ys],
            "cum_premium_pp": [cum_premium_pp(12 * y - 1) for y in ys],
            "annual_income": [annual_income(12 * y - 1) for y in ys],
            "lives_if": [lives_if_ann(y) for y in ys],
            "claims_death": [claims_ann(y, "DEATH") for y in ys],
            "claims_refund": [claims_ann(y, "REFUND") for y in ys],
            "annuity_payments": [annuity_payments_ann(y) for y in ys],
        },
        index=pd.Index(ys, name="policy_year"),                      # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_table_year = 2012

mort_ae_factor = 1.0

pricing_rate = 0.0475

expense_load = 0.06

pricing_iters = 3

expense_maint = 50.0

inflation_rate = 0.025

baa_yield = 0.0575

adjust_spread = 0.01

accel_months = 6

commute_margin = 0.005

ref_rate_shift = 0.0

qlac_premium_limit = 210000.0

qlac_max_start_age = 85

pd = ("Module", "pandas")