# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WholeLife_JP_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **policy years**, 1-based: ``t = 1`` is the first policy year and
``t = proj_len() = omega_age() - age_at_entry() + 1`` the last. There is no maturity
date and no 満期保険金; the horizon is the terminal age of the mortality table, every
remaining life dies in year ``proj_len()``, and nothing is paid there but the death
benefit. **There are no tail states.**

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/whole_life/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.WholeLife_JP_A.Data`, reached here through the ``data`` Reference:

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
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string, ``pols_if_at(t, timing)`` for the within-year
in-force reads, ``cv_pp`` rather than ``av_pp`` because this is a cash surrender value
and not an account value. The technical notes use compact actuarial symbols instead. The
mapping is:

=========================  ==================================  ============================
Notes symbol               Cells                               Meaning
=========================  ==================================  ============================
(none)                     model_point()                       The selected model point row
x                          age_at_entry()                      契約年齢 at issue, 満年齢
x + t - 1                  age(t)                              Attained age in year t
omega                      omega_age()                         Terminal age of the table
T                          proj_len()                          Projection length in years
m                          prem_term(), prem_period()          保険料払込期間; 0 is 終身払
(none)                     prem_end()                          Last year a premium is due
SA                         sum_assured(), sum_assured_at(t)     保険金額 at issue, in year t
P                          premium_pp()                        Annual premium
k                          low_cv_rate()                       解約払戻金支払割合
q(t)                       mort_rate(t)                        Mortality incl. 高度障害
(table q)                  mort_rate_at_age(y)                 Table rate at attained age y
(none)                     mort_rate_base(t)                   Table rate in policy year t
(none)                     mort_be_factor()                    Multiplier on the table rate
w(t)                       lapse_rate(t)                       Voluntary surrender rate
(table w)                  lapse_rate_base(t)                  Before spike and dynamics
s                          lapse_spike()                       Cliff spike applied at t = m
beta                       lapse_beta                          Dynamic-surrender slope
w_dyn(t) / w(t)            lapse_dyn_factor(t)                 Dynamic-surrender multiplier
cumprem(t)                 cum_prem_pp(t)                      Premiums paid to year t
u(t)                       default_rate(t)                     Premium-default rate
l(t)                       pols_if(t)                          In force at start of year t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)               BEF_DECR/BEF_LAPSE/AFT_DECR
(paying cohort)            pols_if_pay(t)                      In force and paying premium
lp(t)                      pols_pay_bef_decr(t)                Payers after the default exit
(none)                     pols_default(t)                     Movers into the APL state
D(t)                       pols_death(t)                       Expected deaths in year t
S(t)                       pols_lapse(t)                       Expected surrenders in year t
(APL failure)              pols_apl_exit(t)                    Exits on APL exhaustion
(loan excess)              pols_loan_exit(t)                   Exits on loan excess
i_cv                       i_cv                                Cash-value basis rate
i_std                      i_std                               Reference valuation rate
i_L                        i_loan                              APL / 契約者貸付 rate
alpha                      acq_dedn_rate                       Acquisition-deduction rate
(none)                     disc_factor(), disc_factor_std()    1 / (1 + i)
A(y)                       epv_death(y)                        Whole-life EPV of 1 at age y
a-double-dot(y, n)         annuity_due(y, n)                   n-year annuity-due at age y
A*(y), a*(y, n)            epv_death_std(y), annuity_due_std   The same on i_std
pi                         prem_net_level_pp()                 Net level premium on i_cv
pi*                        prem_net_level_std_pp()             Net level premium on i_std
W(t)                       prosp_val_pp(t)                     Prospective policy value
SC(t)                      surr_charge_pp(t)                   解約控除
V(t)                       pol_val_pp(t)                       Ordinary surrender value
CV(t)                      cv_pp(t)                            Payable 解約返戻金
k V(t)                     cv_pp_susp(t)                       Suppressed value at every t
(none)                     cv_mult(t)                          1 or k, by policy year
(reserve)                  reserve_pp(t)                       平準純保険料式 reserve
L(t)                       loan_pp(t)                          Main-cohort loan balance
L(t) by cohort             loan_apl_pp(t, s)                   APL balance by entry year s
A(t)                       apl_advance_due(t)                  Premium advanced in year t
(trigger)                  apl_fires(t, s)                     APL continuation test
CV*(t)                     apl_test_val(t)                     Value the APL test runs on
(exhaustion)               apl_fail_year(s)                    Year the cohort exhausts
(advances)                 apl_advances(s)                     Number of advances made
(none)                     pol_loan_year()                     Year the 契約者貸付 is drawn
(none)                     pua_sum_assured()                   払済保険金額 after conversion
P lp(t)                    premiums(t)                         Premium income
(SA - L)D, (CV - L)S       claims(t, kind)                     Benefit outgo by kind
ec D(t)                    claim_expenses(t)                   Claim expense
E0, e(t)                   expenses(t)                         Acquisition and maintenance
(none)                     inflation_factor(t)                 Expense inflation factor
c0, c_r                    commissions(t)                      Commission outgo
(dividend)                 dividends(t)                        5年ごと利差配当 outgo
CF(t)                      net_cf(t)                           Net cash flow, income positive
=========================  ==================================  ============================

Four names needed care.

The notes write ``V(t)`` for the ordinary, unsuppressed surrender value and ``CV(t)`` for
the amount actually payable. :func:`pol_val_pp` is ``V`` and :func:`cv_pp` is ``CV``, and
:func:`cv_pp_susp` is the third quantity the notes need at ``t = m``: ``k V(t)`` at
*every* duration, which is both the value an instant before the step and the value the
clawed-back APL cohort keeps for life. All three are one policy value times one
multiplier — there is no second reserve run anywhere in this model.

``L(t)`` is one symbol in the notes but two objects here. :func:`loan_pp` is the
契約者貸付 balance of the premium-paying cohort; :func:`loan_apl_pp` is the automatic
premium loan balance of a cohort indexed by the year ``s`` it defaulted in. They are kept
apart because the APL exhausts at a duration that depends on ``s``, so collapsing the
cohorts to an average balance would let early entrants ride on late entrants' headroom.

``expenses`` is **acquisition plus maintenance only**. The claim handling expense is
:func:`claim_expenses`, a separate cells, deducted explicitly in :func:`net_cf` and
published as its own ``claim_expenses`` column in :func:`result_cf`, exactly as the notes'
worked-example table prints it. This is the settled meaning across the three libraries, so
an ``expenses`` column means the same thing in all of them.

``mort_be_factor`` is the cells; ``mort_adj`` is the **model-point column** it reads. The
cells name is the library-wide one for the multiplier that turns the shipped valuation
table into the projection basis, and the column keeps the spelling it ships with, so a
CSV written against an earlier revision still loads.

.. rubric:: The 低解約返戻金型 cliff is a step, not a ramp

``CV(t) = k V(t)`` for ``t < m`` and ``CV(t) = V(t)`` for ``t >= m``, with ``k = 0.70``
where the suppressed form is elected. The transition at ``t = m`` is a **step**: the
ratio ``cv_pp(m) / (low_cv_rate() * pol_val_pp(m))`` is exactly ``1 / k``, and anything
between is an interpolation the contract does not have. A surrender occurring in policy
year ``m`` is paid at the end of that year on the **full** value **[std ordering]**; the
suppressed value applies to years 1 to ``m - 1``. Both quantities exist at ``t = m`` and
the model publishes both, :func:`cv_pp` and :func:`cv_pp_susp`.

On a 終身払 point (``prem_term = 0``) the suppressed period runs for life and the step
never happens, which is why one shipped model point is written that way: it is the one
configuration in which the product's signature mechanic is absent by construction.

.. rubric:: Lapse is a funded event

Where the premium is unpaid and there is a surrender value, the insurer **lends the
premium against that value and applies it to the premium**, and the contract continues.
So a premium default is not a lapse: :func:`default_rate` moves policies out of the
paying cohort into an APL state, and only the failure of the continuation test

    apl_test_val(t) >= loan_apl_pp(t, s) + premium_pp() * (1 + i_loan)

terminates them. The test runs on the **suppressed** value, which is the whole point: on
the anchor cell a default at ``t = 2`` buys one advance at ``k = 0.70`` and thirteen at
``k = 1.00``. Running it on ``V`` overstates the headroom by more than a decade of in
force.

**The advance is not cash income.** No cash reaches the insurer, so an APL year produces
no :func:`premiums` entry and no renewal commission; a loan asset is created and shows up
only as growth in :func:`loan_apl_pp` and as a deduction from every later benefit.
:func:`net_cf` is unchanged by an advance in the year it is made.

**The clawback survives the step.** A cohort carried through the low period by unrepaid
advances has by definition not paid those premiums, so **[std]** its value stays at
``k V(t)`` for ever and never steps up at ``m``. ``apl_clawback`` switches that off, and
the difference is sixteen years of in force on the anchor cell.

.. rubric:: Modules that are off in the base run

Six of the notes' optional constructions are implemented and switched off, so that the
base run reproduces the worked example while the machinery stays visible and testable:

- **Premium default and the APL**, ``default_rate`` at 0 on the base points and 1% p.a.
  for ``1 <= t <= m`` on model points 5 and 6, which run it on the suppressed and the
  ordinary form respectively.
- **契約者貸付**, ``pol_loan_util`` at 0, with model point 7 drawing the contractual
  maximum at the fortieth anniversary and reaching the loan-excess termination in year
  53 with the benefit floored at zero. The 9/10-while-paying and 8/10-once-paid-up caps
  are contractual and always applied.
- **Dynamic surrender on the 払戻率**, ``w_dyn = w min(3, max(1, 1 + beta (CV/cumprem -
  1)))`` with ``lapse_beta = 2``, off unless the model point sets ``dyn_lapse``. Model
  point 8 turns it on **and** sets the cliff spike to zero, so the spike is produced
  endogenously instead of imposed — a cross-check on the 15% **[std]** choice rather than
  a replacement for it.
- **The cliff spike itself**, ``lapse_spike``, 15% **[std]** on every point but 8. It is a
  behavioural assumption and nothing in any retrieved document quantifies it; the step in
  ``CV`` that provokes it is contractual, and the two must not be confused.
- **払済保険 conversion**, ``pua_year``, 0 except on model point 4. The contract stops
  paying premiums, the sum assured is replaced by ``(CV - L) / A(x + t)`` on the same
  single-premium basis, and the suppression switches off for the future — but the
  conversion is made on the suppressed value, so the resulting 払済保険金額 is permanently
  smaller.
- **5年ごと利差配当**, ``dividend_type``, ``none`` except on model point 9. The composite is
  無配当; the participating variant declares a dividend out of investment margin every
  fifth year, here as ``div_spread`` times five years of the policy value **[std]**,
  because the declaration basis lives in the unpublished 算出方法書 and no carrier
  publishes it.

``mort_be_factor`` is the last lever, 1.00 on every point but 9. At 1.00 the base run is a
**valuation-table run, not a best estimate**: 生保標準生命表2018（死亡保険用）carries a
roughly-2σ prudential margin and an eight-year improvement allowance already inside it,
and no retrieved source sizes either against current insured experience. Claims move
proportionately with ``mort_be_factor``; the terminal rate is held at 1 whatever it is set to,
because ``omega_age`` is the table's horizon and not an experience assumption.

.. rubric:: 責任準備金 is not 解約返戻金

:func:`reserve_pp` is the 平準純保険料式 policy reserve, on ``i_std`` and the same table,
and it **never produces a cash flow**. It exists so that the notes' identity

    reserve_pp(t) - pol_val_pp(t) = surr_charge_pp(t)

can be asserted — which it can only because ``i_std`` defaults to ``i_cv``. When the two
basis rates differ the ordering can fail outright: with a 標準利率 below the pricing basis
the statutory reserve exceeds the cash value by far more than the 解約控除, and in a deep
逆ざや the reserve can exceed even the sum assured. ``reserve_pp >= pol_val_pp >= cv_pp``
is **not** a model invariant and :func:`check_reserve_identity` does not assert it.

.. rubric:: Sign convention

The notes' ``CF(t)`` is already **income positive** — premiums less claims, expenses and
commission — which is the library-wide sign of :func:`net_cf`, so there is no
``liability_cf`` companion to publish: one stream, one sign, one name.
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


def sex():
    """The sex of the insured, M or F; the two are rated and tabulated separately."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def age_at_entry():
    """x: the 契約年齢 at issue, 15 to 80.

    満年齢 (*man-nenrei*, attained age) with the fractional year discarded at 契約日; the
    rating age then increments on each 年単位の契約応当日 rather than on the birthday, so a
    projection stepped on anniversaries steps it correctly by construction.  **The
    mortality table does not share this basis**: 生保標準生命表2018（死亡保険用）is built for
    a 保険年齢 (nearest-birthday) basis, and the table is read here at the 満年齢 attained
    age with no adjustment **[std]**, because no public mapping between the two exists.
    The resulting bias understates mortality by up to half a year of age.
    """
    return int(model_point()["issue_age"])


def sum_assured():
    """SA: the 保険金額 at issue, level for life.

    One amount pays two benefits — 死亡保険金 on death and 高度障害保険金 on the disability
    state defined in the 約款's 別表 — and paying the second extinguishes the contract.
    They are one decrement on one amount, never two.
    """
    return float(model_point()["sum_assured"])


def prem_term():
    """m: the 保険料払込期間 in years as entered, with **0 denoting 終身払**.

    On a 終身払 contract there is no 払込満了 date, the 低解約払戻期間 runs for life and the
    cliff never occurs.  Use :func:`prem_period` for the effective number of years.
    """
    return int(model_point()["prem_term"])


def prem_period():
    """m: the effective 保険料払込期間, ``proj_len()`` on a 終身払 contract.

    The suppressed period is identical to the premium-paying period, so this is also the
    duration at which :func:`cv_pp` steps up where it steps up at all.
    """
    return prem_term() if prem_term() > 0 else proj_len()


def prem_end():
    """The last policy year in which a premium is actually due.

    ``prem_period()`` normally; one year less than ``pua_year()`` where a 払済保険
    conversion is elected, because the contract stops paying at the conversion.
    """
    if pua_year() > 0:
        return min(prem_period(), pua_year() - 1)
    return prem_period()


def premium_pp():
    """P: the level annual premium per policy, payable in advance in years 1 to m.

    Level and guaranteed for the whole of 保険料払込期間 with no unilateral repricing
    right, which puts every year of it inside any defensible contract boundary.  On the
    anchor cell the value is **sourced**: ¥14,580 a month is published for exactly that
    cell, and the annual figure is 12 times it **[std]** — no carrier publishes an
    annual-mode scale, so the modal discount a real 年払 rate would carry is not applied
    and the annual premium is slightly overstated.  On the other cells it is a **[std]**
    scaling of the anchor's published-premium-to-``prem_net_level_pp()`` ratio, divided
    by 0.837 on the ordinary form, that being the one carrier's published ratio between
    its suppressed and its ordinary scale for one identical cell.
    """
    return float(model_point()["premium_annual"])


def low_cv():
    """Whether the 低解約返戻金型 form is elected.

    A model point flag rather than a modelling switch: the suppressed and ordinary forms
    are separately priced products, and the suppression buys a materially cheaper
    premium in exchange for a 30% haircut on the value during the premium-paying period.
    """
    return bool(model_point()["low_cv"])


def low_cv_rate():
    """k: the 解約払戻金支払割合, 0.70 during the 低解約払戻期間 and 1.00 on the ordinary form.

    Stated identically at four carriers.  It is a **multiplier on one common policy
    value**, not a second reserve basis: at duration 40, well past 払込満了, the suppressed
    and the ordinary product have identical surrender values.
    """
    k = float(model_point()["low_cv_rate"])
    if not low_cv() and k != 1.0:
        raise ValueError("low_cv_rate must be 1.0 when low_cv is not elected")
    if not 0.0 < k <= 1.0:
        raise ValueError("invalid low_cv_rate")
    return k


def apl_elected():
    """Whether the 自動振替貸付 is elected; the default at four of the seven carriers.

    Election varies more than any other feature in the source set — opt-out at four,
    opt-in at one, absent at two — so this is a genuine product variable.  The
    supervisory guideline requires the facility to be at the policyholder's election with
    prompt notice, which is why it is a flag with a default and never an unconditional
    no-lapse rule.
    """
    return bool(model_point()["apl_elected"])


def default_rate(t):
    """u(t): the premium-default rate in policy year t; **0 in the base run**.

    A decrement out of the premium-paying cohort into the APL state, **not** a lapse:
    a policy does not lapse while the cash value can carry the premium.  Zero where the
    APL is not elected, and zero once no premium is due.
    """
    if not apl_elected() or t < 1 or t > prem_end():
        return 0.0
    return float(model_point()["default_rate"])


def pol_loan_util():
    """The fraction of :func:`cv_pp` drawn as a 契約者貸付; 0 in the base run.

    There is no public take-up data of any kind, so the level is a **[std]** model point
    input.  The contractual caps in :func:`loan_cap_rate` bind it whatever it is set to.
    """
    return float(model_point()["pol_loan_util"])


def dividend_type():
    """The participation basis: ``none`` (the composite) or ``five_year``.

    無配当 is the composite default because it is the largest single group in the source
    set and because a dividend is an insurer-discretionary element rather than a
    contractual one.  ``five_year`` is the 5年ごと利差配当 variant, declared out of
    investment margin every fifth policy year; see :func:`dividends`.
    """
    v = model_point()["dividend_type"]
    if v not in ("none", "five_year"):
        raise ValueError("invalid dividend_type")
    return v


def lapse_spike():
    """s: the extra surrender rate applied in policy year m **[std]**, 15% in the base run.

    The step in :func:`cv_pp` at 払込満了 is contractual; the surge in surrenders at the
    step is a behavioural assumption and nothing in any retrieved document quantifies it.
    It is held as its own parameter so that setting it to zero and re-running reads its
    effect directly, which is the right way to challenge it.
    """
    return float(model_point()["lapse_spike"])


def dyn_lapse():
    """Whether the dynamic-surrender module is on; off in the base run."""
    return bool(model_point()["dyn_lapse"])


def mort_be_factor():
    """The multiplier on the table mortality rate; **1.00 in the base run**.

    1.00 is a choice, not a default: it means the base run is a **valuation-table run,
    not a best estimate**.  生保標準生命表2018（死亡保険用）carries a roughly-2σ prudential
    margin and a built-in eight-year improvement allowance, but no retrieved source sizes
    either against current insured experience, so no defensible single haircut exists.
    A production basis would sit below 1.00 and would move claims proportionately.

    Read from the model point's ``mort_adj`` column, which keeps that spelling; the
    cells carries the library-wide name for the factor.
    """
    return float(model_point()["mort_adj"])


def pua_year():
    """The policy year at which 払済保険 is elected, or 0 for no conversion.

    Off on every model point but one.  The conversion is made at the anniversary
    ``pua_year() - 1``, so the earliest meaningful value is 2.
    """
    v = int(model_point()["pua_year"])
    if v == 1:
        raise ValueError("pua_year must be 0 or at least 2")
    return v


def is_paid_up(t):
    """Whether the contract is on the 払済保険 basis in policy year t."""
    return pua_year() > 0 and t >= pua_year()


def omega_age():
    """omega: the terminal age of the mortality table, the first age at which q = 1.

    109 for males and 113 for females on 生保標準生命表2018（死亡保険用）.  It is a hard model
    parameter and not a rounding: projecting a whole life contract to 100, a U.S. habit,
    truncates the liability, and projecting to 120 invents one.
    """
    tbl = data.mort_table().loc[sex()]                               # noqa: F821
    return int(tbl.index[tbl["mort_rate"] >= 1.0][0])


def proj_len():
    """T = omega - x + 1: the projection length in policy years.

    There is no maturity date, so the horizon is the table's, not the contract's.  Every
    remaining life dies in year T and ``pols_if(T + 1)`` is zero; nothing is paid at the
    horizon other than the death benefit and there are no tail states.
    """
    return omega_age() - age_at_entry() + 1


def age(t):
    """x + t - 1: the attained age at the start of policy year t."""
    return age_at_entry() + t - 1


def mort_rate_at_age(y):
    """The shipped table's mortality rate at attained age y, before ``mort_be_factor``.

    Read from ``mort_table.csv``, a **[std]** construction anchored on quoted rates of
    生保標準生命表2018（死亡保険用）rather than a copy of it; see :mod:`~.WholeLife_JP_A.Data`.
    The rate already **includes 高度障害**, so a projection using it must not add a
    separate disability decrement.  This is the rate the contractual cash-value
    construction uses, unadjusted: ``mort_be_factor`` is a best-estimate lever on the
    *decrement*, not a change to the 算出方法書 basis.
    """
    return float(data.mort_table().loc[(sex(), y), "mort_rate"])     # noqa: F821


def mort_rate_base(t):
    """The table mortality rate in policy year t, at attained age ``age(t)``."""
    return mort_rate_at_age(age(t))


def mort_rate(t):
    """q(t): the mortality decrement applied in policy year t, 高度障害 included.

    The table rate times :func:`mort_be_factor`, capped at 1.  At the table's terminal age the
    rate is held at 1 whatever ``mort_be_factor`` is: ``omega_age`` is the horizon of the table
    and a structural property of the projection, not an experience assumption, and
    scaling it would leave lives alive past the end of the table.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate_base(t) * mort_be_factor())


def lapse_rate_base(t):
    """The base voluntary surrender rate in policy year t **[std]**.

    4% / 3% / 2%, with the last row of ``lapse_table.csv`` read for every later year.
    The shape is reasoned, not fitted: a 低解約返戻金型 owner who surrenders during the low
    period takes a 30% haircut on a value that is already below cumulative premiums, so
    early surrender is strongly suppressed.  No carrier publishes a lapse curve by
    duration; the only public benchmark is an amount-weighted, all-product industry
    解約・失効率 of 5.6%, used here as a sanity ceiling and nothing more.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(max(t, 1), int(tbl.index.max())), "lapse_rate"])


def cum_prem_pp(t):
    """cumprem(t): premiums paid per policy by the end of policy year t.

    ``P min(t, prem_end())``.  The denominator of the 払戻率 the dynamic-surrender module
    keys off, and the quantity the product is sold on: the 低解約返戻金型 value crosses
    100% of it shortly after 払込満了.
    """
    return premium_pp() * min(t, prem_end())


def lapse_dyn_factor(t):
    """The dynamic-surrender multiplier on the lapse rate **[std]**; 1 in the base run.

    ``min(3, max(1, 1 + beta max(0, CV(t)/cumprem(t) - 1)))``.  The economically natural
    driver on a savings-shaped contract is the ratio of the value to the premiums paid,
    and on the anchor cell that ratio crosses 1 exactly at the cliff — so with the module
    on and ``lapse_spike`` at zero the surge at 払込満了 is produced endogenously instead
    of imposed.  There is no public calibration evidence for the form or for ``beta``.
    """
    if not dyn_lapse():
        return 1.0
    cp = cum_prem_pp(t)
    if cp <= 0.0:
        return 1.0
    return min(lapse_dyn_cap,                                        # noqa: F821
               max(1.0, 1.0 + lapse_beta * max(0.0, cv_pp(t) / cp - 1.0)))  # noqa: F821


def lapse_rate(t):
    """w(t): the annual voluntary surrender rate applied at the end of policy year t.

    The table rate, plus :func:`lapse_spike` in the year the suppression ends, times the
    dynamic multiplier, capped at 1.  This is the **annual** rate; there is no monthly
    companion on an annual-grid model.  A surrender is not a pure decrement here: it pays
    :func:`cv_pp` net of any loan.
    """
    base = lapse_rate_base(t)
    if prem_term() > 0 and t == prem_period() and not is_paid_up(t):
        base = base + lapse_spike()
    return min(1.0, base * lapse_dyn_factor(t))


def disc_factor():
    """v = 1 / (1 + i_cv): the discount factor of the cash-value basis.

    ``i_cv`` is **[std]** and derived rather than asserted.  The 予定利率, 予定死亡率 and
    予定事業費率 live in the filed but unpublished 算出方法書, so the library constructs the
    policy value in closed form and calibrates it to one carrier's complete published
    surrender-value run.  The calibrated rate lands below the 予定利率 that carrier
    disclosed fifteen years earlier, which is informative rather than embarrassing.
    """
    return 1.0 / (1.0 + i_cv)                                        # noqa: F821


def disc_factor_std():
    """v* = 1 / (1 + i_std): the discount factor of the reference valuation basis.

    ``i_std`` stands for the 標準利率, whose current numeric value could not be
    established from any retrieved official document — the 安全率係数 table for the annual
    case is printed as an omitted table in the retrieved redline.  It therefore defaults
    to ``i_cv`` **[std]**, which is what makes the reserve identity exactly testable.
    """
    return 1.0 / (1.0 + i_std)                                       # noqa: F821


def epv_death(y):
    """A(y): the expected present value at age y of 1 payable at the end of the year of death.

    On ``i_cv`` and the shipped table, unadjusted by ``mort_be_factor``.  Recursive:
    ``A(y) = v [q(y) + (1 - q(y)) A(y + 1)]``, with ``A(omega + 1) = 0`` and
    ``q(omega) = 1``, so ``A(omega) = v`` and the recursion terminates at the table.
    """
    if y > omega_age():
        return 0.0
    q = mort_rate_at_age(y)
    return disc_factor() * (q + (1.0 - q) * epv_death(y + 1))


def annuity_due(y, n):
    """a-double-dot(y, n): the n-year annuity-due of 1 per year at age y, on ``i_cv``.

    ``1 + v p(y) a(y + 1, n - 1)``, zero for ``n <= 0``.  Measured in years of premium,
    so ``SA A(x) / a(x, m)`` is an amount per year.
    """
    if n <= 0:
        return 0.0
    return 1.0 + disc_factor() * (1.0 - mort_rate_at_age(y)) * annuity_due(y + 1, n - 1)


def epv_death_std(y):
    """A*(y): :func:`epv_death` on the reference valuation rate ``i_std``."""
    if y > omega_age():
        return 0.0
    q = mort_rate_at_age(y)
    return disc_factor_std() * (q + (1.0 - q) * epv_death_std(y + 1))


def annuity_due_std(y, n):
    """a*(y, n): :func:`annuity_due` on the reference valuation rate ``i_std``."""
    if n <= 0:
        return 0.0
    return (1.0 + disc_factor_std() * (1.0 - mort_rate_at_age(y))
            * annuity_due_std(y + 1, n - 1))


def prem_net_level_pp():
    """pi = SA A(x) / a(x, m): the net level premium of the cash-value construction.

    **This is not the priced net premium and must not be read as one.**  On the anchor
    cell it comes out *above* the gross premium, which would be a negative expense
    loading and no real product carries one: the construction uses the valuation table's
    margin-loaded q as a stand-in for the insurer's unpublished 予定死亡率, and
    :func:`surr_charge_pp` absorbs the difference.  It reproduces the contractual
    **value**; it is not a pricing model.
    """
    return sum_assured() * epv_death(age_at_entry()) / annuity_due(
        age_at_entry(), prem_period())


def prem_net_level_std_pp():
    """pi*: the net level premium of the 平準純保険料式 reserve, on ``i_std``."""
    return sum_assured() * epv_death_std(age_at_entry()) / annuity_due_std(
        age_at_entry(), prem_period())


def prosp_val_base_pp(t):
    """W(t) on the premium-paying construction, before any 払済保険 conversion.

    ``SA A(x + t) - pi a(x + t, max(m - t, 0))``: the prospective net level premium
    policy value at anniversary t, which is the end of policy year t.  ``W(0) = 0`` by
    construction and ``W(T) = 0`` because the table terminates.
    """
    return (sum_assured() * epv_death(age_at_entry() + t)
            - prem_net_level_pp() * annuity_due(
                age_at_entry() + t, max(prem_period() - t, 0)))


def pua_sum_assured():
    """The 払済保険金額 the contract converts to, or 0 where no conversion is elected.

    ``(CV(p - 1) - L(p)) / A(x + p - 1)`` at the conversion anniversary, on the insurer's
    own single-premium net basis.  The conversion is made on the **suppressed** value, so
    a 低解約返戻金型 contract converted during the low period carries a permanently smaller
    paid-up sum assured than the same contract converted after 払込満了.
    """
    p = pua_year()
    if p <= 0:
        return 0.0
    return max(0.0, cv_base_pp(p - 1) - loan_pp(p)) / epv_death(age_at_entry() + p - 1)


def sum_assured_at(t):
    """The sum assured in force in policy year t: ``SA``, or the 払済保険金額 after conversion."""
    return pua_sum_assured() if is_paid_up(t) else sum_assured()


def prosp_val_pp(t):
    """W(t): the prospective policy value at anniversary t, conversion included.

    The premium-paying construction until the 払済保険 election, then the single-premium
    value ``pua_sum_assured() A(x + t)`` of the reduced paid-up contract.  The change of
    basis at the conversion anniversary is a contractual re-basing, not a roll-forward
    step, and :func:`check_pol_val_roll_fwd` excludes that one year for exactly that
    reason.
    """
    if pua_year() > 0 and t >= pua_year() - 1:
        return pua_sum_assured() * epv_death(age_at_entry() + t)
    return prosp_val_base_pp(t)


def surr_charge_base_pp(t):
    """SC(t) on the premium-paying construction: the 解約控除 grading to zero at m.

    ``alpha SA max(0, m - t) / m`` **[std]**, an initial deduction of 0.90% of the sum
    assured grading linearly to nothing at 払込満了.  On a 終身払 contract the grading has
    no end date, so the deduction is held flat at ``alpha SA`` for life — the limit of
    the same formula as m goes to infinity.
    """
    if prem_term() == 0:
        return acq_dedn_rate * sum_assured()                         # noqa: F821
    m = prem_period()
    return acq_dedn_rate * sum_assured() * max(0, m - t) / m         # noqa: F821


def surr_charge_pp(t):
    """SC(t): the 解約控除 embedded in the surrender value at anniversary t.

    Zero once the contract is on the 払済保険 basis: the deduction was taken at the
    conversion, and the paid-up contract is a single-premium contract with none left to
    take.
    """
    if pua_year() > 0 and t >= pua_year() - 1:
        return 0.0
    return surr_charge_base_pp(t)


def pol_val_pp(t):
    """V(t): the ordinary, **unsuppressed** surrender value at anniversary t.

    ``max(0, W(t) - SC(t))``.  The floor is not decoration: ``W - SC`` is negative in
    principle at ``t = 0`` and none of this model's amounts may produce a negative
    payment.  This is the one policy value from which the suppressed value, the 払済保険
    conversion amount, the 契約者貸付 limit and the APL headroom are all derived.
    """
    return max(0.0, prosp_val_pp(t) - surr_charge_pp(t))


def pol_val_base_pp(t):
    """V(t) on the premium-paying construction, before any 払済保険 conversion.

    Needed by :func:`pua_sum_assured`, which values the conversion on the pre-conversion
    surrender value and would otherwise be circular.
    """
    return max(0.0, prosp_val_base_pp(t) - surr_charge_base_pp(t))


def cv_mult(t):
    """The 解約払戻金支払割合 applying at anniversary t: ``k`` before the step, 1 after it.

    ``k`` for ``t < m`` and 1 for ``t >= m``, and the transition is a **step**.  A
    surrender occurring in policy year m is paid on the full value **[std ordering]**;
    the suppressed value applies to years 1 to m - 1.  Always 1 on the ordinary form and
    once the contract is paid up, and always ``k`` on a 終身払 contract, where the
    suppressed period runs for life.
    """
    if not low_cv() or is_paid_up(t):
        return 1.0
    if prem_term() == 0:
        return low_cv_rate()
    return low_cv_rate() if t < prem_period() else 1.0


def cv_base_pp(t):
    """CV(t) on the premium-paying construction, before any 払済保険 conversion."""
    if not low_cv():
        mult = 1.0
    elif prem_term() == 0 or t < prem_period():
        mult = low_cv_rate()
    else:
        mult = 1.0
    return mult * pol_val_base_pp(t)


def cv_pp(t):
    """CV(t): the 解約返戻金 actually payable at anniversary t, per policy.

    ``cv_mult(t) V(t)``.  Everything derived from the surrender value is suppressed with
    it — the 払済保険金額, the 契約者貸付 limit and the APL headroom are all computed off this
    number rather than off ``V``.
    """
    return cv_mult(t) * pol_val_pp(t)


def cv_pp_susp(t):
    """k V(t): the suppressed value at **every** anniversary, step or no step.

    Two things at once, and the notes need both.  It is the value an instant before the
    step at ``t = m`` — the published pre-step figure — against which
    :func:`cv_pp` an instant after must stand in the exact ratio ``1 / k``.  And it is
    the value a **clawed-back** APL cohort keeps for life, because a cohort carried
    through the low period by unrepaid advances has not paid the low-period premiums and
    the suppressed basis therefore continues to apply after the period ends.
    """
    return low_cv_rate() * pol_val_pp(t)


def reserve_pp(t):
    """The 平準純保険料式 policy reserve at anniversary t — a reference quantity only.

    Accumulated net level premium with **no Zillmer adjustment**, on ``i_std`` and the
    same table, which is what 平成8年大蔵省告示第48号 prescribes for a level-premium 終身保険
    with a fixed 予定利率.  **It never produces a cash flow.**  It exists so that
    ``reserve_pp - pol_val_pp = surr_charge_pp`` can be asserted, and that identity holds
    only because ``i_std`` defaults to ``i_cv``; ``reserve_pp >= pol_val_pp >= cv_pp`` is
    not an invariant and is not asserted anywhere.
    """
    if pua_year() > 0 and t >= pua_year() - 1:
        return pua_sum_assured() * epv_death_std(age_at_entry() + t)
    return (sum_assured() * epv_death_std(age_at_entry() + t)
            - prem_net_level_std_pp() * annuity_due_std(
                age_at_entry() + t, max(prem_period() - t, 0)))


def loan_cap_rate(t):
    """The contractual 契約者貸付 limit in policy year t: 9/10 while paying, 8/10 once 払込済.

    Stated identically at three carriers, with the existing balance deducted first.  It
    binds :func:`pol_loan_util` whatever that is set to.
    """
    return loan_cap_pay if t <= prem_end() else loan_cap_paidup      # noqa: F821


def pol_loan_year():
    """The policy year at which the 契約者貸付 is drawn, or 0 for no drawdown.

    A model point column rather than a fixed Reference, because *when* the loan is taken
    decides whether the contract survives it: a small early draw is outgrown by the value,
    while a draw of the contractual maximum late in the run compounds at ``i_loan``
    against a value growing at ``i_cv`` and reaches the loan-excess termination.
    """
    v = int(model_point()["pol_loan_year"])
    if v == 1:
        raise ValueError("pol_loan_year must be 0 or at least 2")
    return v


def pol_loan_draw(t):
    """The 契約者貸付 drawn at the start of policy year t; zero in the base run.

    A single drawdown at :func:`pol_loan_year` **[std]** of the elected fraction of the
    value at the previous anniversary, capped by :func:`loan_cap_rate`.  There is no
    public take-up data of any kind, so both the timing and the level are
    standardizations; a revolving facility would be another input table.
    """
    if pol_loan_util() <= 0.0 or pol_loan_year() <= 0 or t != pol_loan_year():
        return 0.0
    return min(pol_loan_util(), loan_cap_rate(t)) * cv_pp(t - 1)


def loan_pp(t):
    """L(t): the 契約者貸付 principal and interest of the paying cohort at the start of year t.

    ``L(t + 1) = (L(t) + draw(t)) (1 + i_L)``, compound, with interest capitalised into
    principal.  Identically zero in the base run, where every benefit is therefore gross.
    """
    if t <= 1:
        return 0.0
    return (loan_pp(t - 1) + pol_loan_draw(t - 1)) * (1.0 + i_loan)   # noqa: F821


def loan_fail_year():
    """The policy year in which the loan outgrows the value, or ``proj_len() + 1``.

    The 約款's loan-excess termination: where loan and interest exceed the surrender
    value the insurer notifies for a top-up and, unpaid, the contract lapses.  The
    balance at the start of year t is tested against the value at the **previous**
    anniversary — the amount actually available to settle it — and the
    notice-and-top-up period is not modelled **[std]**.  Never reached where no loan is
    drawn, because a zero balance cannot exceed a non-negative value.
    """
    for t in range(1, proj_len() + 1):
        if loan_pp(t) > cv_pp(t - 1):
            return t
    return proj_len() + 1


def apl_advance_due(t):
    """A(t): the premium the APL would advance in policy year t, zero once none is due.

    Once ``t > prem_end()`` no premium is due, so the balance rolls up on interest alone
    against a value that is still growing — which is why exhaustion after 払込満了 takes
    decades rather than years.
    """
    return premium_pp() if 1 <= t <= prem_end() else 0.0


def apl_test_val(t):
    """CV*(t): the surrender value the APL continuation test is run against.

    The value computed **as if the premium had been paid**, which on the annual grid is
    the value at the end of year t **[std]**.  With the clawback on — the correct
    treatment, since a cohort carried by advances has not paid its low-period premiums —
    that is the **suppressed** value at every duration; with it off the value steps up at
    m like any other.  Running the test on ``V`` instead of on ``k V`` overstates the
    headroom by more than a decade of in force.
    """
    return cv_pp_susp(t) if apl_clawback else cv_pp(t)               # noqa: F821


def apl_fires(t, s):
    """Whether the APL continuation test passes in year t for the cohort defaulting in year s.

    ``CV*(t) >= L(t, s) + P (1 + i_L)`` while a premium is due, and ``CV*(t) >= L(t, s)``
    once none is.  Stated the same way at three carriers.  In policy year 1 the value
    cannot carry a premium on either form, so a default at ``s = 1`` terminates at once.
    """
    if t < s or t > proj_len():
        return False
    adv = apl_advance_due(t)
    return apl_test_val(t) >= loan_apl_pp(t, s) + adv * (1.0 + i_loan)  # noqa: F821


def loan_apl_pp(t, s):
    """L(t, s): the APL balance at the start of year t of the cohort defaulting in year s.

    ``L(t + 1, s) = (L(t, s) + A(t)) (1 + i_L)``, with the advance made only where the
    test fired.  Indexed by the entry year and **not** collapsed to a cohort average: the
    APL exhausts at a duration that depends on when the loan started, so an average
    balance would let early entrants ride on late entrants' headroom and would move the
    termination year by decades.
    """
    if t <= s:
        return 0.0
    prev = loan_apl_pp(t - 1, s)
    adv = apl_advance_due(t - 1) if apl_fires(t - 1, s) else 0.0
    return (prev + adv) * (1.0 + i_loan)                             # noqa: F821


def apl_fail_year(s):
    """The policy year in which the APL cohort entering in year s exhausts.

    ``proj_len() + 1`` where it never does.  The cohort leaves at the **start** of that
    year and the policyholder may claim the surrender value net of the loan, floored at
    zero because the loan can exceed the value.
    """
    for t in range(s, proj_len() + 1):
        if not apl_fires(t, s):
            return t
    return proj_len() + 1


def apl_advances(s):
    """The number of premium advances the APL makes for the cohort entering in year s.

    The single most instructive number the module produces: on the anchor cell a default
    at ``s = 2`` buys **one** advance on the suppressed form and **thirteen** on the
    ordinary one, from the same default at the same duration on the same underlying
    policy value.
    """
    return sum(1 for t in range(s, min(apl_fail_year(s), prem_end() + 1))
               if apl_fires(t, s))


def pols_default(t):
    """Policies moving out of the paying cohort into the APL state at the start of year t.

    ``pols_if_pay(t) u(t)``.  Zero in the base run, and zero in the year a loan-excess
    termination takes the whole paying cohort.
    """
    if default_rate(t) <= 0.0 or t == loan_fail_year():
        return 0.0
    return pols_if_pay(t) * default_rate(t)


def pols_pay_bef_decr(t):
    """The paying cohort exposed to the year-t decrements, after defaults and loan exit."""
    if t == loan_fail_year():
        return 0.0
    return pols_if_pay(t) - pols_default(t)


def pols_if_pay(t):
    """The premium-paying cohort in force at the **start** of policy year t.

    ``pols_if_pay(1) = 1`` and ``pols_if_pay(t + 1) = pols_pay_bef_decr(t)(1 - q)(1 - w)``.
    Equal to :func:`pols_if` in the base run, where no policy ever enters the APL state.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return 1.0
    return (pols_pay_bef_decr(t - 1) * (1.0 - mort_rate(t - 1))
            * (1.0 - lapse_rate(t - 1)))


def pols_apl_in(t, s):
    """The APL cohort of entry year s carried into the start of year t, before the year-t test.

    ``pols_default(s)`` in the entry year, then decremented by mortality and voluntary
    surrender like any other in-force policy, and zero from the year after it exhausts.
    """
    if t < s or t > proj_len():
        return 0.0
    if pols_default(s) == 0.0:
        return 0.0
    if t == s:
        return pols_default(s)
    if apl_fail_year(s) <= t - 1:
        return 0.0
    return (pols_apl_in(t - 1, s) * (1.0 - mort_rate(t - 1))
            * (1.0 - lapse_rate(t - 1)))


def pols_if_apl(t, s):
    """The APL cohort of entry year s exposed to the year-t decrements.

    The carried amount, or zero in and after the year the cohort exhausts: an exhausted
    cohort leaves at the **start** of the year and does not experience that year's deaths
    or surrenders.
    """
    n = pols_apl_in(t, s)
    if n == 0.0:
        return 0.0
    return 0.0 if apl_fail_year(s) <= t else n


def pols_apl_exit_at(t, s):
    """The APL cohort of entry year s terminating at the start of year t on exhaustion."""
    n = pols_apl_in(t, s)
    if n == 0.0:
        return 0.0
    return n if apl_fail_year(s) == t else 0.0


def apl_entry_years(t):
    """The entry years of every APL cohort that can be in force in policy year t."""
    return range(1, min(t, prem_end()) + 1)


def pols_apl_carried(t):
    """The APL cohorts carried into policy year t from an **earlier** entry year.

    Kept apart from the entrants of year t, which are still inside
    :func:`pols_if_pay` at the start of the year and would otherwise be counted twice.
    """
    return sum(pols_apl_in(t, s) for s in range(1, min(t - 1, prem_end()) + 1))


def pols_apl(t):
    """The APL cohorts exposed to the year-t decrements, summed over entry years."""
    return sum(pols_if_apl(t, s) for s in apl_entry_years(t))


def pols_apl_exit(t):
    """Policies terminating at the start of policy year t because the APL exhausted."""
    return sum(pols_apl_exit_at(t, s) for s in apl_entry_years(t))


def pols_loan_exit(t):
    """Policies terminating at the start of policy year t on loan-excess; zero in the base run."""
    return pols_if_pay(t) if t == loan_fail_year() else 0.0


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy year t.

    The premium-paying cohort plus every APL cohort carried in from an earlier year.
    This is the weight on every cash flow of the same ``result_cf()`` row.  It is 1 in
    the first policy year on a single-policy model point and 0 at ``proj_len() + 1``,
    because the table terminates and every remaining life dies in the final year.
    """
    if t < 1 or t > proj_len():
        return 0.0
    return pols_if_pay(t) + pols_apl_carried(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        l(t), the start of the year, before anything happens; the same number
        as :func:`pols_if` and the weight on that year's cash flows.

    ``"BEF_LAPSE"``
        after the APL and loan-excess terminations and after deaths, before
        surrenders — the notes' processing order is **death before lapse**
        **[std order]**, so this is the population surrenders are taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-year state, and zero at ``proj_len()`` because the
        table's terminal rate is 1 and nobody survives the final year.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return (pols_pay_bef_decr(t) + pols_apl(t)) * (1.0 - mort_rate(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t): expected death and 高度障害 claims in policy year t, at the end of the year.

    One decrement covering both benefits at one amount: the shipped table already
    includes 高度障害 inside the death rate, so adding a separate disability decrement
    would double-count.  The リビング・ニーズ rider is an acceleration that **reduces** the
    sum assured by what it pays, so it is not an addition either and its incidence is
    zero in the base run **[std]**.
    """
    return (pols_pay_bef_decr(t) + pols_apl(t)) * mort_rate(t)


def pols_lapse(t):
    """S(t): expected voluntary surrenders at the end of policy year t.

    Taken from the survivors of mortality — death before lapse **[std order]** — and paid
    on the surrender value at that anniversary, net of any loan.  A surrender in policy
    year m is paid on the **full** value; the suppressed value applies to years 1 to
    m - 1.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate(t)


def premiums(t):
    """Premium income at the start of policy year t, an inflow.

    Carried on :func:`pols_pay_bef_decr`, never on the APL cohorts: **an APL advance is
    not cash income.**  No cash reaches the insurer, a loan asset is created instead, and
    booking the advanced premium as income while also netting the loan off the later
    claim would count it twice.  ``net_cf`` is unchanged by an advance in the year it is
    made.  Zero from ``prem_end() + 1``; nothing else about the contract stops there.
    """
    return premium_pp() * pols_pay_bef_decr(t) if t <= prem_end() else 0.0


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the 死亡保険金 / 高度障害保険金 paid at the end of the year of death,
        ``(SA - L) D(t)`` floored at zero, cohort by cohort because each APL
        cohort carries its own balance.

    ``"LAPSE"``
        the 解約返戻金 paid on voluntary surrender, ``(CV(t) - L) S(t)`` floored
        at zero, **plus** the residual value paid where an APL cohort exhausts
        or a loan outgrows the value, which is settled on the previous
        anniversary's value net of the balance that broke the test.

    Every one of these is floored at zero: a loan can outgrow both the surrender value
    and, given long enough, the sum assured, and none of them may produce a negative
    payment.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    if kind == "DEATH":
        pay = max(0.0, sum_assured_at(t) - loan_pp(t)) * (
            pols_pay_bef_decr(t) * mort_rate(t))
        apl = sum(max(0.0, sum_assured_at(t) - loan_apl_pp(t, s))
                  * pols_if_apl(t, s) * mort_rate(t)
                  for s in apl_entry_years(t) if pols_if_apl(t, s) != 0.0)
        return pay + apl
    if kind == "LAPSE":
        surv = 1.0 - mort_rate(t)
        pay = max(0.0, cv_pp(t) - loan_pp(t)) * (
            pols_pay_bef_decr(t) * surv * lapse_rate(t))
        apl = sum(max(0.0, apl_test_val(t) - loan_apl_pp(t, s))
                  * pols_if_apl(t, s) * surv * lapse_rate(t)
                  for s in apl_entry_years(t) if pols_if_apl(t, s) != 0.0)
        exhausted = sum(max(0.0, apl_test_val(t - 1) - loan_apl_pp(t, s))
                        * pols_apl_exit_at(t, s)
                        for s in apl_entry_years(t)
                        if pols_apl_exit_at(t, s) != 0.0)
        excess = max(0.0, cv_pp(t - 1) - loan_pp(t)) * pols_loan_exit(t)
        return pay + apl + exhausted + excess
    raise ValueError("invalid kind")


def claim_expenses(t):
    """ec D(t): the claim handling expense on the year's death claims **[std]**.

    ¥20,000 per claim, uninflated.  No carrier publishes an expense basis of any kind —
    the 予定事業費率 is named in the 保険契約者保護機構 boilerplate and never quantified — so
    every expense level in this model is a standardization.  Published as its own
    ``claim_expenses`` column in :func:`result_cf` and deducted explicitly in
    :func:`net_cf`; it is **not** inside :func:`expenses`.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + pi)^(t-1)`` **[std]**.

    1.0% p.a., deliberately below the 3% a UK or U.S. model would carry: over an
    eighty-year whole-life horizon 1% compounds to 2.19 and 3% to 10.33, so importing a
    Western inflation assumption here produces a different product rather than a stressed
    one.  There is no published Japanese expense basis to anchor either figure.
    """
    return (1.0 + inflation_rate) ** (t - 1)                         # noqa: F821


def expenses(t):
    """E0 and e(t) in policy year t: **acquisition and maintenance only** **[std]**.

    ¥50,000 per policy at issue, then ¥8,000 per policy per year inflating at 1%, both at
    the start of the year.  The claim handling expense is **not** here: it is
    :func:`claim_expenses`, deducted separately in :func:`net_cf` and published in its own
    ``result_cf()`` column, which is how the notes' worked-example table prints it too.
    Maintenance continues
    **for life**, not to 払込満了: that is the structural point of this product, a contract
    on which premiums stop after m years and obligations do not.  There is no separate
    surrender expense; it is folded into maintenance **[std]**.
    """
    acq = expense_acq * pols_if(t) if t == 1 else 0.0                # noqa: F821
    maint = expense_maint * inflation_factor(t) * pols_if(t)         # noqa: F821
    return acq + maint


def commissions(t):
    """Commission outgo in policy year t **[std]**.

    90% of the annual premium at issue, then 3% of premium income in years 2 to
    ``prem_end()``.  Both levels are standardizations; no Japanese carrier publishes a
    commission scale.  Renewal commission follows the premium **actually collected in
    cash**, so an APL cohort produces none **[std]**, and none is paid after 払込満了 — a
    projection that keeps charging it there is charging commission on a premium nobody
    pays.
    """
    init = comm_init_rate * premium_pp() * pols_if(t) if t == 1 else 0.0  # noqa: F821
    renew = comm_renewal_rate * premiums(t) if 2 <= t <= prem_end() else 0.0  # noqa: F821
    return init + renew


def dividends(t):
    """The 5年ごと利差配当 declared at the end of every fifth policy year **[std]**; 0 in base.

    ``div_spread`` times ``div_period`` years of the policy value, on the policies
    surviving mortality.  The composite is 無配当 and this column is zero on every model
    point but one.  The declaration basis is a 三利源 calculation inside the unpublished
    算出方法書 and no carrier publishes it, so both the spread and the once-in-five-years
    timing are standardizations — the timing is the only part of it that is sourced, from
    the product name itself.
    """
    if dividend_type() != "five_year" or t % div_period != 0:        # noqa: F821
        return 0.0
    return (div_spread * div_period * pol_val_pp(t)                  # noqa: F821
            * pols_if_at(t, "BEF_LAPSE"))


def net_cf(t):
    """CF(t): the net cash flow of policy year t, **income positive**.

    Premiums less death and 高度障害 claims, surrender benefits, :func:`claim_expenses`,
    maintenance and acquisition expense, commission and any dividend.  The notes' own
    sign, which is also the library-wide convention, so there is no outgo-positive
    ``liability_cf`` companion to publish.

    The shape to expect is a deep new business strain in year 1, then a long positive
    stretch while the premium runs, then a single violent negative year at 払込満了 where
    the surrender value steps up by ``1 / k`` and the surrender assumption spikes with
    it, and finally a run-off of claims and expenses against no premium at all.  **The
    cliff is the largest single feature of this stream and it is one year wide.**
    """
    return (premiums(t) - claims(t) - claim_expenses(t) - expenses(t)
            - commissions(t) - dividends(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``l(t) - l(t+1)`` less deaths, surrenders, APL exhaustions and loan-excess
    terminations.  The last two are zero in the base run and are what makes the identity
    close when the modules are on: a policy that leaves because its loan outgrew its
    value has left for a reason that is neither a death nor a surrender.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_apl_exit(t) - pols_loan_exit(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy year.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the year that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_decrement_sum_resid(t):
    """The cumulative-decrement residual at policy year t; zero everywhere.

    ``l(1)`` less every exit up to and including year t less ``l(t+1)``.  At ``t = T`` it
    is the notes' statement that the decrements sum to 1: because the table terminates,
    every policy leaves by one of them and ``l(T + 1) = 0``, so there is no residual
    population and no tail state anywhere in this model.
    """
    exits = sum(pols_death(u) + pols_lapse(u) + pols_apl_exit(u) + pols_loan_exit(u)
                for u in range(1, t + 1))
    return pols_if(1) - exits - pols_if(t + 1)


def check_decrement_sum():
    """True when every policy issued leaves by a modelled decrement, in every year."""
    return all(abs(check_decrement_sum_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_pol_val_roll_fwd_resid(t):
    """The policy-value recursion residual at anniversary t; zero everywhere.

    ``(W(t-1) + pi 1{premium due}) (1 + i_cv) - [q SA + (1 - q) W(t)]`` on the table rate,
    which is the retrospective form of the same prospective value and is what catches a
    mis-set ``prem_period`` or a discount factor applied on the wrong side.  It is
    defined as zero at the 払済保険 conversion anniversary, where the value is re-based by
    the election rather than rolled forward.
    """
    if pua_year() > 0 and t == pua_year() - 1:
        return 0.0
    pi = prem_net_level_pp() if (t <= prem_period() and not is_paid_up(t)) else 0.0
    q = mort_rate_at_age(age(t))
    return ((prosp_val_pp(t - 1) + pi) * (1.0 + i_cv)                # noqa: F821
            - q * sum_assured_at(t) - (1.0 - q) * prosp_val_pp(t))


def check_pol_val_roll_fwd():
    """True when the policy value rolls forward on its own basis in every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_pol_val_roll_fwd_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_reserve_identity_resid(t):
    """The 責任準備金-to-解約返戻金 residual at anniversary t; zero everywhere.

    ``reserve_pp(t) - pol_val_pp(t) - SC(t)``, with the deduction floored at the reserve
    itself because the surrender value cannot go below zero.  The whole difference
    between the two quantities is the 解約控除, which is precisely what 平準純保険料式
    forbids the reserve to carry.  Zero **by definition** when the two basis rates
    differ: the identity is a consequence of ``i_std = i_cv`` and is not asserted
    otherwise, because with a 標準利率 below the pricing basis the reserve exceeds the cash
    value by far more than the 解約控除.
    """
    if i_std != i_cv:                                                # noqa: F821
        return 0.0
    return (reserve_pp(t) - pol_val_pp(t)
            - min(surr_charge_pp(t), max(0.0, reserve_pp(t))))


def check_reserve_identity():
    """True when the reserve exceeds the surrender value by exactly the 解約控除."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_reserve_identity_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_loan_roll_fwd_resid(t):
    """The loan roll-forward residual in policy year t; zero everywhere.

    The 契約者貸付 balance and every APL cohort balance, each rolled
    ``L(t + 1) = (L(t) + advance) (1 + i_L)`` and compared with the balance the model
    actually carries.  Identically zero in the base run, where there is no loan at all;
    non-trivial the moment either module is switched on, which is the point of it.
    """
    resid = (loan_pp(t + 1)
             - (loan_pp(t) + pol_loan_draw(t)) * (1.0 + i_loan))     # noqa: F821
    for s in apl_entry_years(t):
        if pols_apl_in(t, s) == 0.0 or apl_fail_year(s) <= t:
            continue
        adv = apl_advance_due(t) if apl_fires(t, s) else 0.0
        resid += (loan_apl_pp(t + 1, s)
                  - (loan_apl_pp(t, s) + adv) * (1.0 + i_loan))      # noqa: F821
    return resid


def check_loan_roll_fwd():
    """True when every loan balance accumulates at ``i_loan`` in every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_loan_roll_fwd_resid(t)) <= tol
               for t in range(1, proj_len()))


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in policy year t; zero everywhere.

    :func:`net_cf` less the published ``result_cf()`` columns of the same row.  It closes
    the loop between the total benefit outgo and the two kinds that make it up, so a
    third kind added to :func:`claims` and left out of its total shows up here rather
    than silently vanishing from the statement.
    """
    return (net_cf(t) - premiums(t) + claims(t, "DEATH") + claims(t, "LAPSE")
            + claim_expenses(t) + expenses(t) + commissions(t) + dividends(t))


def check_net_cf():
    """True when the net cash flow equals the sum of its published columns, every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cash flows, indexed by policy year t.

    ``pols_if`` is the start-of-year count, which is the weight applied to every cash
    flow on the same row.  ``net_cf`` carries the notes' own income-positive sign.
    ``expenses`` is acquisition and maintenance; the claim handling expense is beside it
    in ``claim_expenses``, as it is in every model in the three libraries.
    ``dividends`` is a column of zeros on the 無配当 composite and is published rather
    than dropped, because the participating variant is a real product in the source set.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "dividends": [dividends(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy year t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_if_pay": [pols_if_pay(t) for t in ts],
            "pols_apl": [pols_apl(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_apl_exit": [pols_apl_exit(t) for t in ts],
            "pols_loan_exit": [pols_loan_exit(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """Result table of the policy value, the surrender value and the reserve, by t.

    ``cv_pp`` is the amount payable and ``cv_pp_susp`` the suppressed value at every
    anniversary, so the step at 払込満了 and the value an instant before it can be read off
    the same table.  ``reserve_pp`` is a reference quantity and produces no cash flow.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "prosp_val_pp": [prosp_val_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "pol_val_pp": [pol_val_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "cv_pp_susp": [cv_pp_susp(t) for t in ts],
            "reserve_pp": [reserve_pp(t) for t in ts],
            "loan_pp": [loan_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

i_cv = 0.01468

i_std = 0.01468

i_loan = 0.0275

acq_dedn_rate = 0.0090

lapse_beta = 2.0

lapse_dyn_cap = 3.0

expense_acq = 50000.0

expense_maint = 8000.0

expense_claim = 20000.0

inflation_rate = 0.01

comm_init_rate = 0.90

comm_renewal_rate = 0.03

apl_clawback = True

loan_cap_pay = 0.9

loan_cap_paidup = 0.8

div_spread = 0.0025

div_period = 5

roll_fwd_tol = 1e-10

val_tol = 1e-8

pd = ("Module", "pandas")
