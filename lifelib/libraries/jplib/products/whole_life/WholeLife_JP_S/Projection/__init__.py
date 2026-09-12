# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WholeLife_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` is the **0-based policy-month index**: ``t = 0`` is the first policy month, month
``t`` runs from time ``t`` to time ``t + 1``, the frame is ``range(proj_len())`` with
``proj_len() = 12 (omega_age() - age_at_entry()) + 1``, so the last index is
``proj_len() - 1``. The contractual policy year is the 1-based label
``policy_year(t) = 1 + t // 12``, derived and never indexed by, and
``duration(t) = t // 12`` is the count of completed policy years.

Values carry a **second index, and it is still the anniversary in years**:
``d = 0 … proj_years()`` with ``d = 0`` at issue. :func:`pol_val_pp`, :func:`cv_pp`,
:func:`surr_charge_pp`, :func:`reserve_pp`, :func:`loan_pp` and their companions are
values *at* a 年単位の契約応当日 and not flows of a period, and **none of their numbers
moved when ``t`` became a month**. The month ``t`` opens inside the policy year running
from anniversary ``duration(t)`` to ``duration(t) + 1`` and is settled net of the loan
balance at the first of those.

There is no maturity date and no 満期保険金; the horizon is the terminal age of the
mortality table, every remaining life dies in the terminal policy year, and nothing is
paid there but the death benefit. **There are no tail states.** The frame stops in the
**first month** of that terminal year, which is the ``+ 1`` in ``proj_len()``: the table's
rate at ``omega`` is 1 and so is its monthly equivalent, so the cohort clears there and
the eleven months after it would be rows of zeros.

.. rubric:: The monthly grid: what moved and what did not

The contract is quoted in years and valued at anniversaries, so the monthly step is finer
than the guarantees rather than finer than the product. Three things therefore stayed
annual on purpose, and four moved.

**Annual, because the contract is.** The **policy value construction** —
:func:`epv_death`, :func:`annuity_due`, :func:`prem_net_level_pp`, :func:`prosp_val_pp`,
:func:`reserve_pp` — is built from annual actuarial functions and calibrated to one
carrier's published **annual** surrender-value run, so re-deriving it monthly would move a
number that was fitted rather than assumed. The **loan balances** compound once a year
because the 約款 states a 年利 capitalised at the 契約応当日. And the **APL continuation
test** is the question the insurer asks when a premium goes unpaid, which happens once a
year; its cohort index ``s`` is accordingly a policy year and not a month.

**Monthly, because the experience is.** Mortality and ordinary surrender are rates per
unit time and are taken to the month on the effective convention
``r_m = 1 - (1 - r)^(1/12)``, so twelve of them compound back to the annual rate exactly
and survivorship at the anniversaries is identical to the annual-grid model's. The
**premium**, being 年払, now falls in one month out of twelve instead of being smeared
across a year — which is what a 年払 contract actually looks like. **Maintenance expense**
is a twelfth of the annual amount each month, inflating once a policy year. And the
**cliff** is one month wide.

**One convention is new and one ruling changed.** The new convention is
:func:`pol_val_at_m`, which reads the surrender value **between** anniversaries by linear
interpolation in elapsed months **[std]** — the 算出方法書 that would state the real rule
is unpublished, and the anniversary values it interpolates are untouched. The changed
ruling is :func:`cv_mult_at_m`: the annual grid had to pay every surrender in policy year
``m`` the **post-step** value, because the step and the grid landed on the same year; here
the suppression ends at the month the contract ends it, so eleven months of policy year
``m`` move to the pre-step side and the 15% surge moves to the month **after** the last
premium, where the step actually is. That is the largest single difference between the two
runs of this product.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/whole_life/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.WholeLife_JP_S.Data`, reached here through the ``data`` Reference:

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
with an uppercase ``kind`` string, ``pols_if_at(t, timing)`` for the within-month
in-force reads, ``cv_pp`` rather than ``av_pp`` because this is a cash surrender value
and not an account value. The technical notes use compact actuarial symbols instead. The
mapping is:

=========================  ===================================  ============================
Notes symbol               Cells                                Meaning
=========================  ===================================  ============================
(none)                     model_point()                        The selected model point row
x                          age_at_entry()                       契約年齢 at issue, 満年齢
x + floor(t/12)            age(t)                               Attained age in month t
floor(t/12)                duration(t)                          Completed policy years
y(t) = 1 + floor(t/12)     policy_year(t)                       Contractual policy year
omega                      omega_age()                          Terminal age of the table
T_y                        proj_years()                         Policy years, the span of d
T                          proj_len()                           Number of months projected
m                          prem_term(), prem_period()           保険料払込期間; 0 is 終身払
12m                        prem_period_months()                 払込満了, in policy months
(none)                     prem_end()                           Last policy year a premium is due
SA                         sum_assured(), sum_assured_at(t)     保険金額 at issue, in month t
P                          premium_pp()                         Annual premium
k                          low_cv_rate()                        解約払戻金支払割合
q(t)                       mort_rate(t)                         Mortality incl. 高度障害, annual
q_m(t)                     mort_rate_mth(t)                     The same, per month
(table q)                  mort_rate_at_age(y)                  Table rate at attained age y
(none)                     mort_rate_base(t)                    Table rate in month t, annual
(none)                     mort_be_factor()                     Multiplier on the table rate
w(t)                       lapse_rate(t)                        Surrender rate, annual
w_m(t)                     lapse_rate_mth(t)                    The same, per month
(table w)                  lapse_rate_base(t)                   Before the dynamic factor
s                          lapse_spike()                        Cliff surge, the parameter
s(t)                       lapse_spike_rate(t)                  The surge, in its one month
beta                       lapse_beta                           Dynamic-surrender slope
w_dyn(t) / w(t)            lapse_dyn_factor(t)                  Dynamic-surrender multiplier
cumprem(d)                 cum_prem_pp(d)                       Premiums paid by anniversary d
cumprem at month u         cum_prem_pp_m(u)                     The same, by elapsed month
u(t)                       default_rate(t)                      Premium-default rate
(none)                     apl_active()                         Whether any cohort can exist
l(t)                       pols_if(t)                           In force at the start of month t
(within-month)             pols_if_at(t, timing)                BEF_DECR/BEF_LAPSE/BEF_SPIKE/...
(paying cohort)            pols_if_pay(t)                       In force and paying premium
lp(t)                      pols_pay_bef_decr(t)                 Payers after the default exit
(none)                     pols_default(t)                      Movers into the APL state
D(t)                       pols_death(t)                        Expected deaths in month t
S(t)                       pols_lapse(t)                        Expected surrenders in month t
(ordinary part)            pols_lapse_base(t)                   Surrenders before the surge
(cliff part)               pols_lapse_spike(t)                  The surge itself
(cumulative)               pols_exit_cum(t)                     Every exit to month t
(APL failure)              pols_apl_exit(t)                     Exits on APL exhaustion
(loan excess)              pols_loan_exit(t)                    Exits on loan excess
i_cv                       i_cv                                 Cash-value basis rate
i_std                      i_std                                Reference valuation rate
i_L                        i_loan                               APL / 契約者貸付 rate
alpha                      acq_dedn_rate                        Acquisition-deduction rate
(none)                     disc_factor(), disc_factor_std()     1 / (1 + i)
A(y)                       epv_death(y)                         Whole-life EPV of 1 at age y
a-double-dot(y, n)         annuity_due(y, n)                    n-year annuity-due at age y
A*(y), a*(y, n)            epv_death_std(y), annuity_due_std    The same on i_std
pi                         prem_net_level_pp()                  Net level premium on i_cv
pi*                        prem_net_level_std_pp()              Net level premium on i_std
W(d)                       prosp_val_pp(d)                      Prospective policy value
SC(d)                      surr_charge_pp(d)                    解約控除
V(d)                       pol_val_pp(d)                        Ordinary surrender value
V at month u               pol_val_at_m(u)                      The same, interpolated [std]
CV(d)                      cv_pp(d)                             Payable 解約返戻金
CV at month u              cv_at_m(u)                           The same, at elapsed month u
k V(d)                     cv_pp_susp(d)                        Suppressed value at every d
k V at month u             cv_susp_at_m(u)                      The same, at elapsed month u
(none)                     cv_mult(d)                           1 or k, by anniversary
(none)                     cv_mult_at_m(u)                      1 or k, by elapsed month
(reserve)                  reserve_pp(d)                        平準純保険料式 reserve
L(d)                       loan_pp(d)                           Main-cohort balance at d
L(d) by cohort             loan_apl_pp(d, s)                    APL balance by entry year s
A(d)                       apl_advance_due(d)                   Premium advanced at d
(trigger)                  apl_fires(d, s)                      APL continuation test
CV*(d)                     apl_test_val(d)                      Value the APL test runs on
CV* at month u             apl_test_val_m(u)                    The same, at elapsed month u
(exhaustion)               apl_fail_year(s)                     Anniversary the cohort ends at
(exhaustion)               apl_fail_month(s)                    The same, as a month
(advances)                 apl_advances(s)                      Number of advances made
(loan excess)              loan_fail_year(), loan_fail_month()  Where the loan outgrows CV
(none)                     pol_loan_year()                      Policy year the 契約者貸付 is drawn
(none)                     pua_sum_assured()                    払済保険金額 after conversion
P lp(t)                    premiums(t)                          Premium income, once a year
(SA - L)D, (CV - L)S       claims(t, kind)                      Benefit outgo by kind
ec D(t)                    claim_expenses(t)                    Claim expense
E0, e_m(t)                 expenses(t)                          Acquisition and maintenance
(none)                     inflation_factor(t)                  Expense inflation factor
c0, c_r                    commissions(t)                       Commission outgo
(dividend)                 dividends(t)                         5年ごと利差配当 outgo
CF(t)                      net_cf(t)                            Net cash flow, income positive
=========================  ===================================  ============================

Six names needed care.

The notes write ``V(d)`` for the ordinary, unsuppressed surrender value and ``CV(d)`` for
the amount actually payable. :func:`pol_val_pp` is ``V`` and :func:`cv_pp` is ``CV``, and
:func:`cv_pp_susp` is the third quantity the notes need at the anniversary ``d = m``:
``k V(d)`` at *every* duration, which is both the value an instant before the step and
the value the clawed-back APL cohort keeps for life. All three are one policy value times
one multiplier — there is no second reserve run anywhere in this model.

``L`` is one symbol in the notes but two objects here. :func:`loan_pp` is the
契約者貸付 balance of the premium-paying cohort; :func:`loan_apl_pp` is the automatic
premium loan balance of a cohort indexed by the **anniversary** ``s`` it defaulted at.
They are kept apart because the APL exhausts at a duration that depends on ``s``, so
collapsing the cohorts to an average balance would let early entrants ride on late
entrants' headroom.

Every ``*_at_m`` cells is the **monthly reading of an annual contractual quantity**, and
the suffix is the warning: ``cv_pp(d)`` is the 解約返戻金 the contract defines at an
anniversary, and ``cv_at_m(u)`` is what this model pays someone who surrenders between
two. They agree wherever the contract has an opinion. Where they differ —
:func:`cv_mult_at_m` inside the last year of the 保険料払込期間 — the difference is the
subject of its own docstring rather than a rounding.

``lapse_rate`` no longer carries the cliff surge. :func:`lapse_spike_rate` does, and it is
a **one-off proportion in one month**, not a rate: converting it to a monthly equivalent
would spread one decision, taken on a date, over a year in which the thing that provokes
it has not yet happened.

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

``CV(d) = k V(d)`` for ``d < m`` and ``CV(d) = V(d)`` for ``d >= m``, with ``k = 0.70``
where the suppressed form is elected. The transition at the anniversary ``d = m`` is a
**step**: the ratio ``cv_pp(m) / (low_cv_rate() * pol_val_pp(m))`` is exactly ``1 / k``,
and anything between is an interpolation the contract does not have. Both quantities exist
at ``d = m`` and the model publishes both, :func:`cv_pp` and :func:`cv_pp_susp`.

**On this grid the step is at the month the contract puts it.** A surrender at elapsed
month ``12m - 1`` is still inside the 保険料払込期間 and is paid ``k V``; one at ``12 m`` is
not and is paid ``V``. The annual grid could not draw that line — the step and its own
step were the same size — so it ruled **[std ordering]** that the whole of policy year
``m`` was paid the post-step value, and put the behavioural surge there too. Here eleven
of those twelve months are on the pre-step side and the surge is in the month after the
last premium, beside the step that causes it. Nothing about the contract changed; the grid
stopped rounding it.

On a 終身払 point (``prem_term = 0``) the suppressed period runs for life and the step
never happens, which is why one shipped model point is written that way: it is the one
configuration in which the product's signature mechanic is absent by construction.

.. rubric:: Lapse is a funded event

Where the premium is unpaid and there is a surrender value, the insurer **lends the
premium against that value and applies it to the premium**, and the contract continues.
So a premium default is not a lapse: :func:`default_rate` moves policies out of the
paying cohort into an APL state, and only the failure of the continuation test

    apl_test_val(t + 1) >= loan_apl_pp(t, s) + premium_pp() * (1 + i_loan)

terminates them — the value at the anniversary the advanced premium would carry the
contract to, against the balance at the anniversary the test is made at. The test runs on the **suppressed** value, which is the whole
point: on the anchor cell a default at ``s = 1`` (policy year 2) buys one advance at
``k = 0.70`` and thirteen at ``k = 1.00``. Running it on ``V`` overstates the headroom by
more than a decade of in force.

**The advance is not cash income.** No cash reaches the insurer, so an APL cohort
produces no :func:`premiums` entry and no renewal commission; a loan asset is created and
shows up only as growth in :func:`loan_apl_pp` and as a deduction from every later benefit.
:func:`net_cf` is unchanged by an advance in the month it is made — which, the premium
being 年払, is an anniversary month and no other.

**The clawback survives the step.** A cohort carried through the low period by unrepaid
advances has by definition not paid those premiums, so **[std]** its value stays at
``k V(d)`` for ever and never steps up at ``m``. ``apl_clawback`` switches that off, and
the difference is sixteen years of in force on the anchor cell.

.. rubric:: Modules that are off in the base run

Six of the notes' optional constructions are implemented and switched off, so that the
base run reproduces the worked example while the machinery stays visible and testable:

- **Premium default and the APL**, ``default_rate`` at 0 on the base points and 1% per
  premium in policy years 1 to ``m`` — the anniversary months ``t = 0, 12, …, 12(m - 1)``
  — on model points 5 and 6, which run it on the suppressed and the ordinary form
  respectively. It is applied once per premium and never converted to a monthly rate: a
  default is the failure to pay one premium on one date.
- **契約者貸付**, ``pol_loan_util`` at 0, with model point 7 drawing the contractual
  maximum at the anniversary ``d = 39``, which opens policy year 40, and reaching the
  loan-excess termination at an anniversary decades later, with the benefit floored at
  zero. The 9/10-while-paying and
  8/10-once-paid-up caps are contractual and always applied.
- **Dynamic surrender on the 払戻率**, ``w_dyn = w min(3, max(1, 1 + beta (CV/cumprem -
  1)))`` with ``lapse_beta = 2``, off unless the model point sets ``dyn_lapse``. Model
  point 8 turns it on **and** sets the cliff spike to zero, so the spike is produced
  endogenously instead of imposed — a cross-check on the 15% **[std]** choice rather than
  a replacement for it.
- **The cliff spike itself**, ``lapse_spike``, 15% **[std]** on every point but 8, taken
  as a one-off in the single month after the last premium. It is a behavioural assumption
  and nothing in any retrieved document quantifies it; the step in ``CV`` that provokes it
  is contractual, and the two must not be confused.
- **払済保険 conversion**, ``pua_year``, 0 except on model point 4. The contract stops
  paying premiums, the sum assured is replaced by ``(CV - L) / A(x + d)`` on the same
  single-premium basis, and the suppression switches off for the future — but the
  conversion is made on the suppressed value, so the resulting 払済保険金額 is permanently
  smaller.
- **5年ごと利差配当**, ``dividend_type``, ``none`` except on model point 9. The composite is
  無配当; the participating variant declares a dividend out of investment margin every
  fifth year — in the last month of it — here as ``div_spread`` times five years of the
  policy value **[std]**,
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

    reserve_pp(d) - pol_val_pp(d) = surr_charge_pp(d)

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
    """m: the effective 保険料払込期間 **in years**, ``proj_years()`` on a 終身払 contract.

    The suppressed period is identical to the premium-paying period, so this is also the
    anniversary at which :func:`cv_pp` steps up where it steps up at all.  It stays in
    years on the monthly grid because the contract states it in years: ``m`` is a
    contractual term, and the month it converts to is ``12 m``, which is
    :func:`prem_period_months`.
    """
    return prem_term() if prem_term() > 0 else proj_years()


def prem_period_months():
    """12 m: the 保険料払込期間 in policy **months** — the month 払込満了 falls at.

    The instant the 低解約返戻金型 suppression ends and the surrender value steps up by
    ``1 / k``.  On the annual grid that step had to be smeared over the whole of policy
    year ``m``; here it is the single month the contract puts it in.
    """
    return 12 * prem_period()


def prem_end():
    """The last policy year in which a premium is actually due.

    ``prem_period()`` normally; one year less than ``pua_year()`` where a 払済保険
    conversion is elected, because the contract stops paying at the conversion.
    """
    if pua_year() > 0:
        return min(prem_period(), pua_year() - 1)
    return prem_period()


def premium_pp():
    """P: the level annual premium per policy, payable in advance in policy years 1 to m.

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
    """u(t): the premium-default rate in policy month t; **0 in the base run**.

    A decrement out of the premium-paying cohort into the APL state, **not** a lapse:
    a policy does not lapse while the cash value can carry the premium.  Zero where the
    APL is not elected, and zero once no premium is due — the last premium falls at the
    anniversary opening policy year ``prem_end()``.

    **It is non-zero only in a premium due month**, and on the monthly grid that is a
    statement the model can make.  A premium default is the failure to pay a *particular*
    premium on a *particular* date, not a hazard running through the year, so the annual
    rate is applied once, at the anniversary the premium falls due, and never converted to
    a monthly equivalent.  The annual grid could not tell the two readings apart.
    """
    if not apl_elected() or t < 0 or t % 12 != 0 or policy_year(t) > prem_end():
        return 0.0
    return float(model_point()["default_rate"])


def apl_active():
    """Whether any policy can ever enter the APL state on this model point.

    ``apl_elected()`` and a positive ``default_rate`` column.  It exists to keep
    :func:`apl_entry_years` empty on the eight model points that never default, which is
    exact — no cohort can be non-empty without it — and which matters on the monthly grid
    in a way it did not on the annual one: the cohort sums run over the whole frame, so a
    model point with no APL at all would otherwise pay for twelve times as many empty
    summands as before.
    """
    return apl_elected() and float(model_point()["default_rate"]) > 0.0


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
    """Whether the contract is on the 払済保険 basis in policy month t.

    The election takes effect from policy year ``pua_year()``, i.e. from the month
    ``12 (pua_year() - 1)``; the anniversary it is made at is ``pua_year() - 1``.
    """
    return pua_year() > 0 and policy_year(t) >= pua_year()


def omega_age():
    """omega: the terminal age of the mortality table, the first age at which q = 1.

    109 for males and 113 for females on 生保標準生命表2018（死亡保険用）.  It is a hard model
    parameter and not a rounding: projecting a whole life contract to 100, a U.S. habit,
    truncates the liability, and projecting to 120 invents one.
    """
    tbl = data.mort_table().loc[sex()]                               # noqa: F821
    return int(tbl.index[tbl["mort_rate"] >= 1.0][0])


def proj_years():
    """T_y = omega - x + 1: the number of policy **years** the contract can run.

    The span of the **anniversary** index ``d``, which stays in years on this grid because
    every contractual value in the product — the surrender value, the 解約控除, the
    reserve, the 保険料払込期間 — is defined at an anniversary and quoted by policy year.
    ``d`` therefore runs ``0 .. proj_years()`` and none of its numbers moved when ``t``
    became a month.
    """
    return omega_age() - age_at_entry() + 1


def proj_len():
    """T: the **number** of policy **months** projected, ``12 (omega - x) + 1``.

    The exclusive end of the frame, counted from ``t = 0``: ``result_cf()`` covers
    ``t = 0, ..., proj_len() - 1`` and ``len(result_cf()) == proj_len()``.  There is no
    maturity date, so the horizon is the table's, not the contract's.

    The ``+ 1`` is the terminal month and is the whole of the terminal policy year that
    this model needs.  The table's rate at ``omega`` is 1, so its monthly equivalent
    ``1 - (1 - 1)^(1/12)`` is also 1: every life still in force at the start of the
    terminal policy year dies in its **first** month, and the eleven months after it would
    be rows of zeros.  The frame stops at the month the cohort clears — ``pols_if(T)`` is
    zero, nothing is paid at the horizon but the death benefit, and there are no tail
    states.
    """
    return 12 * (omega_age() - age_at_entry()) + 1


def duration(t):
    """The number of **completed** policy years at the start of policy month t, ``t // 12``.

    The bridge between the monthly projection index and the annual anniversary index
    ``d``: month ``t`` opens inside policy year ``duration(t) + 1``, which runs from
    anniversary ``duration(t)`` to anniversary ``duration(t) + 1``.
    """
    return t // 12


def policy_year(t):
    """y(t) = 1 + t // 12: the contractual policy year of month t, a 1-based label.

    Months ``t = 0 .. 11`` are policy year 1.  The label exists because the contract's own
    schedules are quoted in policy years — the 保険料払込期間 ``m``, the ``policy_year``
    column of ``lapse_table.csv``, ``pua_year`` and ``pol_loan_year`` — and it is
    **derived, never indexed by**: every cells of this model is indexed by the 0-based
    month ``t`` or by the anniversary ``d``.
    """
    return 1 + duration(t)


def age(t):
    """x + floor(t / 12): the attained age during policy month t.

    The 契約年齢 holds for the twelve months ``t = 0 .. 11``, and the rating age
    increments at each 年単位の契約応当日 rather than at the birthday, so stepping it on the
    anniversary is what the contract does.
    """
    return age_at_entry() + duration(t)


def mort_rate_at_age(y):
    """The shipped table's mortality rate at attained age y, before ``mort_be_factor``.

    Read from ``mort_table.csv``, a **[std]** construction anchored on quoted rates of
    生保標準生命表2018（死亡保険用）rather than a copy of it; see :mod:`~.WholeLife_JP_S.Data`.
    The rate already **includes 高度障害**, so a projection using it must not add a
    separate disability decrement.  This is the rate the contractual cash-value
    construction uses, unadjusted: ``mort_be_factor`` is a best-estimate lever on the
    *decrement*, not a change to the 算出方法書 basis.
    """
    return float(data.mort_table().loc[(sex(), y), "mort_rate"])     # noqa: F821


def mort_rate_base(t):
    """The **annual** table mortality rate in month t, at attained age ``age(t)``.

    Level across the twelve months of a policy year, because the table is graduated by
    整数年齢 and the rating age steps on the anniversary.
    """
    return mort_rate_at_age(age(t))


def mort_rate(t):
    """q(t): the **annual** mortality rate in policy month t, 高度障害 included.

    The table rate times :func:`mort_be_factor`, capped at 1.  At the table's terminal age the
    rate is held at 1 whatever ``mort_be_factor`` is: ``omega_age`` is the horizon of the table
    and a structural property of the projection, not an experience assumption, and
    scaling it would leave lives alive past the end of the table.

    This is the annual rate the table is stated on and the notes quote;
    :func:`mort_rate_mth` is the decrement actually applied to the month.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate_base(t) * mort_be_factor())


def mort_rate_mth(t):
    """q_m(t): the monthly mortality decrement, ``1 - (1 - q(t))^(1/12)`` **[std]**.

    The **effective** convention, not a nominal ``q / 12``: twelve months of it compound
    back to the annual rate exactly, so survivorship at the anniversaries is the same as
    the annual-grid model produced and every difference between the two runs is a timing
    difference rather than a change of basis.

    At the terminal age ``q = 1`` and this is 1 as well, which is why the frame ends in
    the first month of the terminal policy year: the cohort clears there and cannot be
    spread over a year that no longer exists.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The base **annual** voluntary surrender rate in month t **[std]**.

    ``lapse_table.csv`` is keyed by the **contractual** ``policy_year``, a 1-based label,
    so the lookup goes through :func:`policy_year`: period ``t`` reads row ``t + 1``.
    4% / 3% / 2%, with the last row of ``lapse_table.csv`` read for every later year.
    The shape is reasoned, not fitted: a 低解約返戻金型 owner who surrenders during the low
    period takes a 30% haircut on a value that is already below cumulative premiums, so
    early surrender is strongly suppressed.  No carrier publishes a lapse curve by
    duration; the only public benchmark is an amount-weighted, all-product industry
    解約・失効率 of 5.6%, used here as a sanity ceiling and nothing more.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(max(policy_year(t), 1),
                             int(tbl.index.max())), "lapse_rate"])


def cum_prem_pp(d):
    """cumprem(d): premiums paid per policy by the anniversary d.

    ``P min(d, prem_end())`` — the premiums falling due at times ``0 … d - 1``.  An
    anniversary quantity, like the surrender value it is compared with: the denominator
    of the 払戻率 the dynamic-surrender module keys off, and the quantity the product is
    sold on, since the 低解約返戻金型 value crosses 100% of it shortly after 払込満了.
    """
    return premium_pp() * min(d, prem_end())


def cum_prem_pp_m(u):
    """cumprem at **elapsed month u**: premiums paid per policy by that instant.

    The premium is annual and falls at the anniversaries ``0, 12, 24, …``, so the count
    paid by elapsed month ``u`` is ``ceil(u / 12)`` capped at ``prem_end()`` — and it is a
    **step** function of ``u``, not a smooth accrual, because that is what paying once a
    year is. It agrees with :func:`cum_prem_pp` at every anniversary.
    """
    return premium_pp() * min(-(-u // 12), prem_end())


def lapse_dyn_factor(t):
    """The dynamic-surrender multiplier on the lapse rate **[std]**; 1 in the base run.

    ``min(3, max(1, 1 + beta max(0, CV/cumprem - 1)))``, read at the **end of month t**,
    which is where the surrender is paid.  On the monthly grid the ratio is therefore a
    monthly series rather than an annual one, and the surge it produces on model point 8
    builds over the months around 払込満了 instead of arriving in one annual step.  The
    economically natural driver on a savings-shaped contract is the ratio of the value to
    the premiums paid, and on the anchor cell that ratio crosses 1 exactly at the cliff —
    so with the module on and ``lapse_spike`` at zero the surge at 払込満了 is produced
    endogenously instead of imposed.  There is no public calibration evidence for the
    form or for ``beta``.
    """
    if not dyn_lapse():
        return 1.0
    cp = cum_prem_pp_m(t + 1)
    if cp <= 0.0:
        return 1.0
    return min(lapse_dyn_cap,                                        # noqa: F821
               max(1.0, 1.0 + lapse_beta * max(0.0, cv_at_m(t + 1) / cp - 1.0)))  # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** voluntary surrender rate of the policy year containing month t.

    The table rate times the dynamic multiplier, capped at 1.  A surrender is not a pure
    decrement here: it pays :func:`cv_at_m` net of any loan.

    **The cliff spike is no longer inside it.**  On the annual grid the 15% surge at
    払込満了 had to be added to this rate, because the year was the finest thing there was;
    here it is :func:`lapse_spike_rate`, a one-off proportion of the survivors of the
    single month the step happens in.  The two are different kinds of quantity — one is a
    rate per unit time that converts to a month, the other is a decision taken on a date
    that does not — and keeping them apart is the same ruling this library makes for the
    renewal decline in ``Term_JP_S``.
    """
    return min(1.0, lapse_rate_base(t) * lapse_dyn_factor(t))


def lapse_rate_mth(t):
    """w_m(t): the monthly ordinary surrender rate, ``1 - (1 - w(t))^(1/12)`` **[std]**.

    The same effective convention as :func:`mort_rate_mth`, so the twelve months of a
    policy year compound back to the annual table rate.  It excludes the cliff spike,
    which is :func:`lapse_spike_rate`.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_spike_rate(t):
    """s: the one-off surrender surge at 払込満了 **[std]**, 15% in the base run.

    Non-zero in exactly one month of the whole projection — ``t = prem_period_months()``, the
    first month **after** the last premium, which is the month the 解約返戻金 steps up by
    ``1 / k``.  Zero on a 終身払 contract, which has no 払込満了 and therefore no step, and
    zero once the contract is on the 払済保険 basis.

    **It is not annualized and never converted to a monthly rate.**  The step in
    :func:`cv_at_m` is contractual and instantaneous; the surge in surrenders at the step
    is a behavioural response to it, taken by owners who have been waiting for the step,
    and it is a proportion of the people standing there rather than a hazard running
    through a year.  The annual grid had to spread it over the twelve months of policy
    year ``m`` **and** pay those surrenders the post-step value, which put the surge a year
    before the event that causes it; here the surge and the step are in the same month.

    Nothing in any retrieved document quantifies it.  It is held as its own cells so that
    setting ``lapse_spike`` to zero and re-running reads its effect directly, which is the
    right way to challenge it — and model point 8 does exactly that, replacing it with the
    endogenous dynamic-surrender module.
    """
    if prem_term() <= 0 or is_paid_up(t) or t != prem_period_months():
        return 0.0
    return min(1.0, lapse_spike())


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


def prosp_val_base_pp(d):
    """W(d) on the premium-paying construction, before any 払済保険 conversion.

    ``SA A(x + d) - pi a(x + d, max(m - d, 0))``: the prospective net level premium
    policy value **at anniversary d**, ``d = 0`` at issue, which is the end of period
    ``d - 1`` and the start of period ``d``.  ``W(0) = 0`` by construction and
    ``W(T) = 0`` because the table terminates.
    """
    return (sum_assured() * epv_death(age_at_entry() + d)
            - prem_net_level_pp() * annuity_due(
                age_at_entry() + d, max(prem_period() - d, 0)))


def pua_sum_assured():
    """The 払済保険金額 the contract converts to, or 0 where no conversion is elected.

    ``(CV(p - 1) - L(p - 1)) / A(x + p - 1)`` at the conversion anniversary
    ``d = p - 1``, on the insurer's own single-premium net basis.  The conversion is made
    on the **suppressed** value, so a 低解約返戻金型 contract converted during the low
    period carries a permanently smaller paid-up sum assured than the same contract
    converted after 払込満了.
    """
    p = pua_year()
    if p <= 0:
        return 0.0
    return (max(0.0, cv_base_pp(p - 1) - loan_pp(p - 1))
            / epv_death(age_at_entry() + p - 1))


def sum_assured_at(t):
    """The sum assured in force in period t: ``SA``, or the 払済保険金額 after conversion."""
    return pua_sum_assured() if is_paid_up(t) else sum_assured()


def prosp_val_pp(d):
    """W(d): the prospective policy value at anniversary d, conversion included.

    The premium-paying construction until the 払済保険 election, then the single-premium
    value ``pua_sum_assured() A(x + d)`` of the reduced paid-up contract.  The change of
    basis at the conversion anniversary ``pua_year() - 1`` is a contractual re-basing,
    not a roll-forward step, and :func:`check_pol_val_roll_fwd` excludes the one period
    that rolls into it for exactly that reason.
    """
    if pua_year() > 0 and d >= pua_year() - 1:
        return pua_sum_assured() * epv_death(age_at_entry() + d)
    return prosp_val_base_pp(d)


def surr_charge_base_pp(d):
    """SC(d) on the premium-paying construction: the 解約控除 grading to zero at m.

    ``alpha SA max(0, m - d) / m`` **[std]**, an initial deduction of 0.90% of the sum
    assured grading linearly to nothing at 払込満了, the anniversary ``d = m``.  On a 終身払
    contract the grading has no end date, so the deduction is held flat at ``alpha SA``
    for life — the limit of the same formula as m goes to infinity.
    """
    if prem_term() == 0:
        return acq_dedn_rate * sum_assured()                         # noqa: F821
    m = prem_period()
    return acq_dedn_rate * sum_assured() * max(0, m - d) / m         # noqa: F821


def surr_charge_pp(d):
    """SC(d): the 解約控除 embedded in the surrender value at anniversary d.

    Zero once the contract is on the 払済保険 basis: the deduction was taken at the
    conversion, and the paid-up contract is a single-premium contract with none left to
    take.
    """
    if pua_year() > 0 and d >= pua_year() - 1:
        return 0.0
    return surr_charge_base_pp(d)


def pol_val_pp(d):
    """V(d): the ordinary, **unsuppressed** surrender value at anniversary d.

    ``max(0, W(d) - SC(d))``.  The floor is not decoration: ``W - SC`` is negative in
    principle at ``d = 0``, the issue instant, and none of this model's amounts may
    produce a negative payment.  This is the one policy value from which the suppressed
    value, the 払済保険 conversion amount, the 契約者貸付 limit and the APL headroom are all
    derived.
    """
    return max(0.0, prosp_val_pp(d) - surr_charge_pp(d))


def pol_val_base_pp(d):
    """V(d) on the premium-paying construction, before any 払済保険 conversion.

    Needed by :func:`pua_sum_assured`, which values the conversion on the pre-conversion
    surrender value and would otherwise be circular.
    """
    return max(0.0, prosp_val_base_pp(d) - surr_charge_base_pp(d))


def cv_mult(d):
    """The 解約払戻金支払割合 applying at anniversary d: ``k`` before the step, 1 after it.

    ``k`` for ``d < m`` and 1 for ``d >= m``, and the transition is a **step**.  A
    surrender occurring in policy year m — period ``m - 1`` — is paid at anniversary m on
    the full value **[std ordering]**; the suppressed value applies to anniversaries 1 to
    m - 1.  Always 1 on the ordinary form and from the anniversary the contract is paid
    up at, and always ``k`` on a 終身払 contract, where the suppressed period runs for
    life.  The paid-up test is written on the anniversary rather than through
    :func:`is_paid_up`, which is indexed by the period: the suppression switches off from
    anniversary ``pua_year()``, the conversion itself being made at ``pua_year() - 1`` on
    the suppressed value.
    """
    if not low_cv() or (pua_year() > 0 and d >= pua_year()):
        return 1.0
    if prem_term() == 0:
        return low_cv_rate()
    return low_cv_rate() if d < prem_period() else 1.0


def cv_base_pp(d):
    """CV(d) on the premium-paying construction, before any 払済保険 conversion."""
    if not low_cv():
        mult = 1.0
    elif prem_term() == 0 or d < prem_period():
        mult = low_cv_rate()
    else:
        mult = 1.0
    return mult * pol_val_base_pp(d)


def cv_pp(d):
    """CV(d): the 解約返戻金 actually payable at anniversary d, per policy.

    ``cv_mult(d) V(d)``.  Everything derived from the surrender value is suppressed with
    it — the 払済保険金額, the 契約者貸付 limit and the APL headroom are all computed off this
    number rather than off ``V``.
    """
    return cv_mult(d) * pol_val_pp(d)


def pol_val_at_m(u):
    """V at **elapsed month u**: the ordinary surrender value between anniversaries **[std]**.

    ``V(d)`` at every anniversary — ``u = 12 d`` reproduces :func:`pol_val_pp` exactly —
    and **linear in the elapsed months** between two anniversaries::

        V(u) = (1 - f) V(d) + f V(d + 1),   d = u // 12,  f = (u mod 12) / 12

    The within-year rule is the one thing the monthly grid needs that the annual grid did
    not, and it is a **[std]**: the 算出方法書 that would state it is a 基礎書類 filed with
    the 金融庁 and is not published, so no source settles whether a real carrier grades its
    解約返戻金 linearly in elapsed months, on a 経過月数 table of its own, or on the
    retrospective value. Linear interpolation is the market's ordinary convention for a
    value quoted by policy year and is the least assuming of the three.

    What it deliberately does **not** touch is the calibration. ``i_cv`` was derived by
    fitting this construction to one carrier's complete published surrender-value run,
    which is an **annual** table; the anniversary values are unchanged here, so the fit is
    the same fit and the interpolation adds a convention rather than moving a number.
    """
    d, r = u // 12, u % 12
    if r == 0:
        return pol_val_pp(d)
    f = r / 12.0
    return (1.0 - f) * pol_val_pp(d) + f * pol_val_pp(d + 1)


def cv_mult_at_m(u):
    """The 解約払戻金支払割合 applying at elapsed month u: ``k`` before 払込満了, 1 from it.

    The monthly statement of :func:`cv_mult`, and it is where the monthly grid changes an
    answer rather than merely refining one. The annual grid had to rule that a surrender
    anywhere in policy year ``m`` was paid at anniversary ``m`` on the **full** value — a
    **[std ordering]** forced by the step and the grid landing on the same year. Here the
    suppression ends at the month the contract ends it, ``u = 12 m``: a surrender at
    elapsed month ``12m - 1`` is inside the 保険料払込期間 and is paid ``k V``, and one at
    ``12 m`` is not and is paid ``V``. Eleven months of policy year ``m`` move from the
    post-step to the pre-step side, and on the anchor cell that is the largest single
    difference between the two grids.
    """
    if not low_cv() or (pua_year() > 0 and u >= 12 * pua_year()):
        return 1.0
    if prem_term() == 0:
        return low_cv_rate()
    return low_cv_rate() if u < prem_period_months() else 1.0


def cv_at_m(u):
    """CV at elapsed month u: the 解約返戻金 actually payable, per policy.

    ``cv_mult_at_m(u) pol_val_at_m(u)``.  This is what a surrender in month ``t`` is paid,
    read at ``u = t + 1`` because the surrender falls at the end of the month.  It agrees
    with :func:`cv_pp` at every anniversary except inside the 保険料払込期間's last year,
    where the two disagree **by design** — see :func:`cv_mult_at_m`.
    """
    return cv_mult_at_m(u) * pol_val_at_m(u)


def cv_susp_at_m(u):
    """k V at elapsed month u: the suppressed value between anniversaries.

    The monthly companion of :func:`cv_pp_susp`, and the value a clawed-back APL cohort is
    settled on when it surrenders between anniversaries.
    """
    return low_cv_rate() * pol_val_at_m(u)


def cv_pp_susp(d):
    """k V(d): the suppressed value at **every** anniversary, step or no step.

    Two things at once, and the notes need both.  It is the value an instant before the
    step at ``d = m`` — the published pre-step figure — against which
    :func:`cv_pp` an instant after must stand in the exact ratio ``1 / k``.  And it is
    the value a **clawed-back** APL cohort keeps for life, because a cohort carried
    through the low period by unrepaid advances has not paid the low-period premiums and
    the suppressed basis therefore continues to apply after the period ends.
    """
    return low_cv_rate() * pol_val_pp(d)


def reserve_pp(d):
    """The 平準純保険料式 policy reserve at anniversary d — a reference quantity only.

    Accumulated net level premium with **no Zillmer adjustment**, on ``i_std`` and the
    same table, which is what 平成8年大蔵省告示第48号 prescribes for a level-premium 終身保険
    with a fixed 予定利率.  **It never produces a cash flow.**  It exists so that
    ``reserve_pp - pol_val_pp = surr_charge_pp`` can be asserted, and that identity holds
    only because ``i_std`` defaults to ``i_cv``; ``reserve_pp >= pol_val_pp >= cv_pp`` is
    not an invariant and is not asserted anywhere.
    """
    if pua_year() > 0 and d >= pua_year() - 1:
        return pua_sum_assured() * epv_death_std(age_at_entry() + d)
    return (sum_assured() * epv_death_std(age_at_entry() + d)
            - prem_net_level_std_pp() * annuity_due_std(
                age_at_entry() + d, max(prem_period() - d, 0)))


def loan_cap_rate(d):
    """The contractual 契約者貸付 limit at anniversary d: 9/10 while paying, 8/10 once 払込済.

    Stated identically at three carriers, with the existing balance deducted first.  It
    binds :func:`pol_loan_util` whatever that is set to.  Indexed by the **anniversary**,
    like the loan balance and the value it is a fraction of: a 契約者貸付 is drawn at an
    anniversary and the 約款 compounds it once a year.
    """
    return (loan_cap_pay if d + 1 <= prem_end()                      # noqa: F821
            else loan_cap_paidup)                                    # noqa: F821


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


def pol_loan_draw(d):
    """The 契約者貸付 drawn at anniversary d; zero in the base run.

    A single drawdown at the anniversary opening policy year :func:`pol_loan_year` —
    ``d = pol_loan_year() - 1`` **[std]** — of the elected fraction of the value there,
    capped by :func:`loan_cap_rate`.  There is no public take-up data of any kind, so both
    the timing and the level are standardizations; a revolving facility would be another
    input table.
    """
    if (pol_loan_util() <= 0.0 or pol_loan_year() <= 0
            or d != pol_loan_year() - 1):
        return 0.0
    return min(pol_loan_util(), loan_cap_rate(d)) * cv_pp(d)


def loan_pp(d):
    """L(d): the 契約者貸付 principal and interest of the paying cohort at anniversary d.

    ``L(d + 1) = (L(d) + draw(d)) (1 + i_L)``, compound, with interest capitalised into
    principal, and ``L(0) = 0``.  Identically zero in the base run, where every benefit is
    therefore gross.

    **It stays an annual quantity on the monthly grid, and that is the contract's own
    convention, not an approximation.**  The 約款 states the loan rate as a 年利 and
    capitalises it at the 年単位の契約応当日, so the balance genuinely does not move between
    anniversaries.  A benefit falling in month ``t`` is settled net of ``loan_pp`` read at
    ``duration(t)``, the anniversary that opened the policy year — which is the balance
    actually outstanding.
    """
    if d <= 0:
        return 0.0
    return (loan_pp(d - 1) + pol_loan_draw(d - 1)) * (1.0 + i_loan)   # noqa: F821


def loan_fail_year():
    """The **anniversary** d at which the loan outgrows the value, or ``proj_years()``.

    The 約款's loan-excess termination: where loan and interest exceed the surrender
    value the insurer notifies for a top-up and, unpaid, the contract lapses.  The balance
    at anniversary ``d`` is tested against the value at that same instant — the amount
    actually available to settle it — and the notice-and-top-up period is not modelled
    **[std]**.  ``proj_years()``, one past the last anniversary, is the never-reached
    sentinel; a zero balance cannot exceed a non-negative value, so the base run never
    reaches it.  The termination takes effect in the month ``12 d``, which is
    :func:`loan_fail_month`.

    The test stays annual because both sides of it are: the balance moves once a year and
    the notice it triggers is served at the anniversary.
    """
    for d in range(proj_years()):
        if loan_pp(d) > cv_pp(d):
            return d
    return proj_years()


def loan_fail_month():
    """The policy month the loan-excess termination takes effect in, ``12 loan_fail_year()``.

    ``proj_len()`` where it never happens, so that a comparison against ``t`` is safe over
    the whole frame.
    """
    d = loan_fail_year()
    return proj_len() if d >= proj_years() else 12 * d


def apl_advance_due(d):
    """A(d): the premium the APL would advance at anniversary d, zero once none is due.

    Once ``d + 1 > prem_end()`` no premium is due, so the balance rolls up on interest
    alone against a value that is still growing — which is why exhaustion after 払込満了
    takes decades rather than years.  Indexed by the anniversary the premium falls at,
    because an annual premium falls at an anniversary and nowhere else.
    """
    return premium_pp() if 0 <= d and d + 1 <= prem_end() else 0.0


def apl_test_val(d):
    """CV*(d): the surrender value the APL continuation test is run against, at anniversary d.

    The value computed **as if the premium had been paid**: the test made at anniversary
    ``d`` reads ``apl_test_val(d + 1)``, the value at the anniversary the advanced premium
    would carry the contract to **[std]**.  With the clawback on — the correct treatment,
    since a cohort carried by advances has not paid its low-period premiums — that is the
    **suppressed** value at every duration; with it off the value steps up at m like any
    other.  Running the test on ``V`` instead of on ``k V`` overstates the headroom by more
    than a decade of in force.
    """
    return cv_pp_susp(d) if apl_clawback else cv_pp(d)               # noqa: F821


def apl_test_val_m(u):
    """CV* at elapsed month u: the same quantity between anniversaries.

    What an APL cohort surrendering mid-year is settled on.  It is the *test* value and
    not :func:`cv_at_m` because the clawback applies to the settlement for the same reason
    it applies to the test: a cohort carried through the low period by unrepaid advances
    has not paid those premiums, so the suppressed basis continues to apply to it.
    """
    return cv_susp_at_m(u) if apl_clawback else cv_at_m(u)           # noqa: F821


def apl_fires(d, s):
    """Whether the APL continuation test passes at anniversary d for the cohort entering at s.

    ``CV*(d + 1) >= L(d, s) + P (1 + i_L)`` while a premium is due, and
    ``CV*(d + 1) >= L(d, s)`` once none is — the value at the **next** anniversary against
    the balance at this one.  Stated the same way at three carriers.  In the first policy
    year the value cannot carry a premium on either form, so a default at ``s = 0``
    terminates at once.

    **Both indices are anniversaries, and they stay anniversaries on the monthly grid.**
    An APL advance settles a premium, a premium falls once a year, and the test is what
    the insurer runs when it does; there is no monthly version of the question.  ``s`` is
    accordingly the *policy year* the cohort defaulted in — the 0-based anniversary
    ``d = s``, month ``12 s`` — and not the month.
    """
    if d < s or d >= proj_years():
        return False
    adv = apl_advance_due(d)
    return apl_test_val(d + 1) >= loan_apl_pp(d, s) + adv * (1.0 + i_loan)  # noqa: F821


def loan_apl_pp(d, s):
    """L(d, s): the APL balance at anniversary d of the cohort entering at anniversary s.

    ``L(d + 1, s) = (L(d, s) + A(d)) (1 + i_L)``, with the advance made only where the
    test fired.  Indexed by the entry anniversary and **not** collapsed to a cohort
    average: the APL exhausts at a duration that depends on when the loan started, so an
    average balance would let early entrants ride on late entrants' headroom and would
    move the termination by decades.

    Annual like :func:`loan_pp` and for the same contractual reason — 年利, capitalised at
    the 契約応当日 — so a benefit in month ``t`` is settled net of ``loan_apl_pp`` read at
    ``duration(t)``.
    """
    if d <= s:
        return 0.0
    prev = loan_apl_pp(d - 1, s)
    adv = apl_advance_due(d - 1) if apl_fires(d - 1, s) else 0.0
    return (prev + adv) * (1.0 + i_loan)                             # noqa: F821


def apl_fail_year(s):
    """The anniversary d at which the APL cohort entering at anniversary s exhausts.

    ``proj_years()`` where it never does, one past the last anniversary.  The cohort
    leaves at the **start** of the policy year that anniversary opens — the month
    :func:`apl_fail_month` — and the policyholder may claim the surrender value net of the
    loan, floored at zero because the loan can exceed the value.
    """
    for d in range(s, proj_years()):
        if not apl_fires(d, s):
            return d
    return proj_years()


def apl_fail_month(s):
    """The policy month the APL cohort entering at anniversary s terminates in.

    ``12 apl_fail_year(s)``, or ``proj_len()`` where the cohort never exhausts, so that a
    comparison against ``t`` is safe over the whole frame.
    """
    d = apl_fail_year(s)
    return proj_len() if d >= proj_years() else 12 * d


def apl_advances(s):
    """The number of premium advances the APL makes for the cohort entering at anniversary s.

    The single most instructive number the module produces: on the anchor cell a default
    at ``s = 1`` — policy year 2 — buys **one** advance on the suppressed form and
    **thirteen** on the ordinary one, from the same default at the same duration on the
    same underlying policy value.
    """
    return sum(1 for d in range(s, min(apl_fail_year(s), prem_end()))
               if apl_fires(d, s))


def pols_default(t):
    """Policies moving out of the paying cohort into the APL state at the start of month t.

    ``pols_if_pay(t) u(t)``, and non-zero only in a premium due month, because
    :func:`default_rate` is.  Zero in the base run, and zero in the month a loan-excess
    termination takes the whole paying cohort.
    """
    if default_rate(t) <= 0.0 or t == loan_fail_month():
        return 0.0
    return pols_if_pay(t) * default_rate(t)


def pols_pay_bef_decr(t):
    """The paying cohort exposed to the month-t decrements, after defaults and loan exit."""
    if t == loan_fail_month():
        return 0.0
    return pols_if_pay(t) - pols_default(t)


def pols_if_pay(t):
    """The premium-paying cohort in force at the **start** of policy month t.

    ``pols_if_pay(0) = 1`` and
    ``pols_if_pay(t + 1) = pols_pay_bef_decr(t)(1 - q_m)(1 - w_m)(1 - s)``, the monthly
    decrements plus the one-off cliff spike in the month it fires.  Equal to
    :func:`pols_if` in the base run, where no policy ever enters the APL state.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return 1.0
    return (pols_pay_bef_decr(t - 1) * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1))
            * (1.0 - lapse_spike_rate(t - 1)))


def pols_apl_in(t, s):
    """The APL cohort entering at anniversary s, carried into month t before its test.

    ``pols_default(12 s)`` in the entry month, then decremented **monthly** by mortality
    and voluntary surrender like any other in-force policy, and zero from the month after
    the cohort exhausts.  The cohort index ``s`` is the entry *anniversary* and ``t`` the
    month: the population moves every month, the loan and its test move once a year.
    """
    if t < 12 * s or t >= proj_len():
        return 0.0
    if pols_default(12 * s) == 0.0:
        return 0.0
    if t == 12 * s:
        return pols_default(t)
    if apl_fail_month(s) <= t - 1:
        return 0.0
    return (pols_apl_in(t - 1, s) * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1))
            * (1.0 - lapse_spike_rate(t - 1)))


def pols_if_apl(t, s):
    """The APL cohort of entry anniversary s exposed to the month-t decrements.

    The carried amount, or zero in and after the month the cohort exhausts: an exhausted
    cohort leaves at the **start** of that month and does not experience its deaths or
    surrenders.
    """
    n = pols_apl_in(t, s)
    if n == 0.0:
        return 0.0
    return 0.0 if apl_fail_month(s) <= t else n


def pols_apl_exit_at(t, s):
    """The APL cohort of entry anniversary s terminating at the start of month t."""
    n = pols_apl_in(t, s)
    if n == 0.0:
        return 0.0
    return n if apl_fail_month(s) == t else 0.0


def apl_entry_years(t):
    """The entry anniversaries of every APL cohort that can be in force in month t.

    ``0 … min(duration(t), prem_end() - 1)``: no cohort can enter before the first
    anniversary, and none after the last anniversary a premium is due,
    ``prem_end() - 1``.  Empty where :func:`apl_active` is False, which is exact — no
    cohort can be non-empty there — and keeps eight of the ten model points from summing
    over an entry list twelve times longer than the annual grid's.
    """
    if not apl_active():
        return range(0)
    return range(min(duration(t), prem_end() - 1) + 1)


def pols_apl_carried(t):
    """The APL cohorts carried into month t from an **earlier** entry anniversary.

    Kept apart from the entrants of month t, which are still inside :func:`pols_if_pay` at
    the start of the month and would otherwise be counted twice.  A cohort entering at
    anniversary ``s`` enters in month ``12 s``, so the cohorts carried in are those with
    ``12 s < t``.
    """
    if not apl_active() or t <= 0:
        return 0.0
    return sum(pols_apl_in(t, s)
               for s in range(min((t - 1) // 12, prem_end() - 1) + 1))


def pols_apl(t):
    """The APL cohorts exposed to the month-t decrements, summed over entry anniversaries."""
    return sum(pols_if_apl(t, s) for s in apl_entry_years(t))


def pols_apl_exit(t):
    """Policies terminating at the start of month t because the APL exhausted."""
    return sum(pols_apl_exit_at(t, s) for s in apl_entry_years(t))


def pols_loan_exit(t):
    """Policies terminating at the start of month t on loan-excess; zero in the base run."""
    return pols_if_pay(t) if t == loan_fail_month() else 0.0


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy month t.

    The premium-paying cohort plus every APL cohort carried in from an earlier month.
    This is the weight on every cash flow of the same ``result_cf()`` row.  It is 1 in
    the first month, ``t = 0``, on a single-policy model point and 0 at ``proj_len()``,
    one past the frame, because the table terminates and every remaining life dies in the
    final month.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    return pols_if_pay(t) + pols_apl_carried(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before anything happens; the same number
        as :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after the APL and loan-excess terminations and after deaths, before
        surrenders — the notes' processing order is **death before lapse**
        **[std order]**, so this is the population surrenders are taken from.

    ``"BEF_SPIKE"``
        after ordinary surrender, before the one-off cliff surge.  Equal to
        ``"AFT_DECR"`` in every month but the one 払込満了 falls in.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state, and zero at ``proj_len() - 1`` because
        the table's terminal rate is 1 and nobody survives the final month.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return (pols_pay_bef_decr(t) + pols_apl(t)) * (1.0 - mort_rate_mth(t))
    if timing == "BEF_SPIKE":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_SPIKE") * (1.0 - lapse_spike_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t): expected death and 高度障害 claims in month t, at the end of the month.

    One decrement covering both benefits at one amount: the shipped table already
    includes 高度障害 inside the death rate, so adding a separate disability decrement
    would double-count.  The リビング・ニーズ rider is an acceleration that **reduces** the
    sum assured by what it pays, so it is not an addition either and its incidence is
    zero in the base run **[std]**.
    """
    return (pols_pay_bef_decr(t) + pols_apl(t)) * mort_rate_mth(t)


def pols_lapse_base(t):
    """The ordinary voluntary surrenders at the end of month t, before the cliff surge.

    Taken from the survivors of mortality — death before lapse **[std order]**.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_lapse_spike(t):
    """The cliff surge: surrenders taken at 払込満了 by owners who waited for the step.

    Non-zero in one month of the whole projection, and zero on every contract that has no
    払込満了.  It is published beside :func:`pols_lapse_base` rather than folded into it
    because it is the thing the product is about, and on the annual grid it could not be
    seen apart from a year of ordinary surrender.
    """
    return pols_if_at(t, "BEF_SPIKE") * lapse_spike_rate(t)


def pols_lapse(t):
    """S(t): total expected voluntary surrenders at the end of month t.

    Ordinary surrenders plus the cliff surge, both paid on the surrender value at the end
    of the month — ``cv_at_m(t + 1)`` — net of any loan.  The surge falls in the month
    **after** the last premium, which is where the value steps up, so it is paid on the
    post-step value while the eleven months before it are paid on the suppressed one.
    """
    return pols_lapse_base(t) + pols_lapse_spike(t)


def premiums(t):
    """Premium income at the start of policy month t, an inflow.

    **The premium is annual (年払), so it falls in one month out of twelve** — the
    anniversary months ``t = 0, 12, 24, …`` — and is zero in the other eleven.  That is
    the single most visible change the monthly grid makes to this product's statement: the
    stream is a sawtooth of one large inflow a year against maintenance expense every
    month, which is what a 年払 contract actually looks like and what the annual grid could
    not show.

    Carried on :func:`pols_pay_bef_decr`, never on the APL cohorts: **an APL advance is
    not cash income.**  No cash reaches the insurer, a loan asset is created instead, and
    booking the advanced premium as income while also netting the loan off the later
    claim would count it twice.  ``net_cf`` is unchanged by an advance in the month it is
    made.  Zero once ``policy_year(t) > prem_end()``; nothing else about the contract
    stops there.
    """
    if t % 12 != 0 or policy_year(t) > prem_end():
        return 0.0
    return premium_pp() * pols_pay_bef_decr(t)


def claims(t, kind=None):
    """Benefit outgo in period t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the 死亡保険金 / 高度障害保険金 paid at the end of the period of death,
        ``(SA - L) D(t)`` floored at zero, cohort by cohort because each APL
        cohort carries its own balance.

    ``"LAPSE"``
        the 解約返戻金 paid on voluntary surrender, ``(CV(t + 1) - L) S(t)``
        floored at zero — the value at the **end of the month**, interpolated
        between anniversaries by :func:`cv_at_m` — **plus** the residual value
        paid where an APL cohort exhausts or a loan outgrows the value, which is
        settled at the **start** of the month it happens in, on the anniversary
        that opens it, net of the balance that broke the test.  Both the
        ordinary surrenders and the 払込満了 cliff surge are in this line and
        both are paid the same way.

    Every one of these is floored at zero: a loan can outgrow both the surrender value
    and, given long enough, the sum assured, and none of them may produce a negative
    payment.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    d = duration(t)
    if kind == "DEATH":
        pay = max(0.0, sum_assured_at(t) - loan_pp(d)) * (
            pols_pay_bef_decr(t) * mort_rate_mth(t))
        apl = sum(max(0.0, sum_assured_at(t) - loan_apl_pp(d, s))
                  * pols_if_apl(t, s) * mort_rate_mth(t)
                  for s in apl_entry_years(t) if pols_if_apl(t, s) != 0.0)
        return pay + apl
    if kind == "LAPSE":
        surv = 1.0 - mort_rate_mth(t)
        exit_rate = 1.0 - (1.0 - lapse_rate_mth(t)) * (1.0 - lapse_spike_rate(t))
        pay = max(0.0, cv_at_m(t + 1) - loan_pp(d)) * (
            pols_pay_bef_decr(t) * surv * exit_rate)
        apl = sum(max(0.0, apl_test_val_m(t + 1) - loan_apl_pp(d, s))
                  * pols_if_apl(t, s) * surv * exit_rate
                  for s in apl_entry_years(t) if pols_if_apl(t, s) != 0.0)
        exhausted = sum(max(0.0, apl_test_val(d) - loan_apl_pp(d, s))
                        * pols_apl_exit_at(t, s)
                        for s in apl_entry_years(t)
                        if pols_apl_exit_at(t, s) != 0.0)
        excess = max(0.0, cv_pp(d) - loan_pp(d)) * pols_loan_exit(t)
        return pay + apl + exhausted + excess
    raise ValueError("invalid kind")


def claim_expenses(t):
    """ec D(t): the claim handling expense on the month's death claims **[std]**.

    ¥20,000 per claim, uninflated.  No carrier publishes an expense basis of any kind —
    the 予定事業費率 is named in the 保険契約者保護機構 boilerplate and never quantified — so
    every expense level in this model is a standardization.  Published as its own
    ``claim_expenses`` column in :func:`result_cf` and deducted explicitly in
    :func:`net_cf`; it is **not** inside :func:`expenses`.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y(t) - 1)``, 1 in year 1 **[std]**.

    **Annual steps inside the monthly grid**: maintenance inflates once a policy year, at
    the anniversary, not once a month.  A 1.0% p.a. assumption is an annual observation and
    compounding it monthly would assert a within-year expense profile no source supports.

    1.0% p.a. is deliberately below the 3% a UK or U.S. model would carry: over an
    eighty-year whole-life horizon 1% compounds to 2.19 and 3% to 10.33, so importing a
    Western inflation assumption here produces a different product rather than a stressed
    one.  There is no published Japanese expense basis to anchor either figure.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """E0 and e_m(t) in month t: **acquisition and maintenance only** **[std]**.

    ¥50,000 per policy at issue — the acquisition charge falls in the first row of the
    frame — then ¥8,000 per policy per year taken as ``8,000 / 12`` a month and inflating
    at 1% a year, both at the start of the month.  The claim handling expense is **not**
    here: it is :func:`claim_expenses`, deducted separately in :func:`net_cf` and published
    in its own ``result_cf()`` column, which is how the notes' worked-example table prints
    it too.  Maintenance continues
    **for life**, not to 払込満了: that is the structural point of this product, a contract
    on which premiums stop after m years and obligations do not — and on the monthly grid
    that point is visible every month rather than once a year.  There is no separate
    surrender expense; it is folded into maintenance **[std]**.
    """
    acq = expense_acq * pols_if(t) if t == 0 else 0.0                # noqa: F821
    maint = expense_maint / 12.0 * inflation_factor(t) * pols_if(t)  # noqa: F821
    return acq + maint


def commissions(t):
    """Commission outgo in policy month t **[std]**.

    90% of the annual premium at issue, then 3% of premium income in policy years 2 to
    ``prem_end()``.  Both levels are standardizations; no Japanese carrier publishes a
    commission scale.  Renewal commission follows the premium **actually collected in
    cash**, so it falls in the same anniversary month the premium does and is zero in the
    eleven months between; an APL cohort produces none **[std]**; and none is paid after
    払込満了 — a projection that keeps charging it there is charging commission on a premium
    nobody pays.
    """
    init = comm_init_rate * premium_pp() * pols_if(t) if t == 0 else 0.0  # noqa: F821
    renew = (comm_renewal_rate * premiums(t)                         # noqa: F821
             if 2 <= policy_year(t) <= prem_end() else 0.0)
    return init + renew


def dividends(t):
    """The 5年ごと利差配当 declared at the end of every fifth policy year **[std]**; 0 in base.

    Fires in the **last month** of every fifth policy year — ``t = 59, 119, 179, …`` — and
    is declared on the policy value at the anniversary that closes it,
    ``d = policy_year(t)``.  ``div_spread`` times ``div_period`` years of that value, on
    the policies surviving mortality.  A declaration is an event at a date, so it falls in
    one month and is not spread; the annual grid put it in a year, which was the same thing
    said less precisely.  The composite is 無配当 and this column is zero on every model
    point but one.  The declaration basis is a 三利源 calculation inside the unpublished
    算出方法書 and no carrier publishes it, so both the spread and the once-in-five-years
    timing are standardizations — the timing is the only part of it that is sourced, from
    the product name itself.
    """
    if (dividend_type() != "five_year" or (t + 1) % 12 != 0
            or policy_year(t) % div_period != 0):                    # noqa: F821
        return 0.0
    return (div_spread * div_period * pol_val_pp(policy_year(t))     # noqa: F821
            * pols_if_at(t, "BEF_LAPSE"))


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**.

    Premiums less death and 高度障害 claims, surrender benefits, :func:`claim_expenses`,
    maintenance and acquisition expense, commission and any dividend.  The notes' own
    sign, which is also the library-wide convention, so there is no outgo-positive
    ``liability_cf`` companion to publish.

    The shape to expect is a deep new business strain in the first month, then a sawtooth
    while the premium runs — one large inflow at each anniversary against maintenance and
    claims every month — then a single violent negative **month** at 払込満了 where the
    surrender value steps up by ``1 / k`` and the surrender surge lands on it, and finally
    a run-off of claims and expenses against no premium at all.  **The cliff is the
    largest single feature of this stream, and on this grid it is one month wide rather
    than one year.**  That is the clearest thing the monthly step buys on this product:
    the annual grid could say the cliff cost a year and could not say what a month of it
    looked like.
    """
    return (premiums(t) - claims(t) - claim_expenses(t) - expenses(t)
            - commissions(t) - dividends(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy month t; zero everywhere.

    ``l(t) - l(t+1)`` less deaths, surrenders, APL exhaustions and loan-excess
    terminations.  The last two are zero in the base run and are what makes the identity
    close when the modules are on: a policy that leaves because its loan outgrew its
    value has left for a reason that is neither a death nor a surrender.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_apl_exit(t) - pols_loan_exit(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def pols_exit_cum(t):
    """Every exit of every kind from ``t = 0`` to month t inclusive, per policy issued.

    A running total, defined recursively rather than re-summed at each ``t``.  On the
    annual grid :func:`check_decrement_sum_resid` re-added the whole history on every row,
    which cost 80 squared additions over a run; twelve times as many rows makes that 144
    times as much work, so the cumulative total is carried instead.  The quantity is the
    same one.
    """
    if t < 0:
        return 0.0
    return (pols_exit_cum(t - 1) + pols_death(t) + pols_lapse(t)
            + pols_apl_exit(t) + pols_loan_exit(t))


def check_decrement_sum_resid(t):
    """The cumulative-decrement residual at month t; zero everywhere.

    ``l(0)`` less every exit up to and including month t less ``l(t+1)``.  At
    ``t = T - 1`` it is the notes' statement that the decrements sum to 1: because the
    table terminates, every policy leaves by one of them and ``l(T) = 0``, so there is no
    residual population and no tail state anywhere in this model.
    """
    return pols_if(0) - pols_exit_cum(t) - pols_if(t + 1)


def check_decrement_sum():
    """True when every policy issued leaves by a modelled decrement, in every month."""
    return all(abs(check_decrement_sum_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_pol_val_roll_fwd_resid(d):
    """The policy-value recursion residual across the policy year opening at anniversary d.

    ``(W(d) + pi 1{premium due}) (1 + i_cv) - [q SA + (1 - q) W(d+1)]`` on the table
    rate — the roll from one anniversary to the next.  It is the retrospective form of the
    same prospective value and is what catches a mis-set ``prem_period`` or a discount
    factor applied on the wrong side.  It is defined as zero for the year that rolls
    **into** the 払済保険 conversion anniversary ``pua_year() - 1``, i.e. at
    ``d = pua_year() - 2``, where the value is re-based by the election rather than rolled
    forward.

    **Annual, and it must stay annual.**  The policy value is constructed from annual
    actuarial functions on an annual basis and is defined at anniversaries; rolling it
    monthly would be checking an interpolation convention rather than the construction.
    The monthly reading of the same value is :func:`pol_val_at_m`, which agrees with this
    one at every anniversary by definition.
    """
    if pua_year() > 0 and d == pua_year() - 2:
        return 0.0
    pi = (prem_net_level_pp()
          if (d + 1 <= prem_period() and not (pua_year() > 0 and d + 1 >= pua_year()))
          else 0.0)
    q = mort_rate_at_age(age_at_entry() + d)
    sa = (pua_sum_assured() if (pua_year() > 0 and d + 1 >= pua_year())
          else sum_assured())
    return ((prosp_val_pp(d) + pi) * (1.0 + i_cv)                    # noqa: F821
            - q * sa - (1.0 - q) * prosp_val_pp(d + 1))


def check_pol_val_roll_fwd():
    """True when the policy value rolls forward on its own basis in every policy year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_pol_val_roll_fwd_resid(d)) <= tol
               for d in range(proj_years()))


def check_reserve_identity_resid(d):
    """The 責任準備金-to-解約返戻金 residual at anniversary d; zero everywhere.

    ``reserve_pp(d) - pol_val_pp(d) - SC(d)``, with the deduction floored at the reserve
    itself because the surrender value cannot go below zero.  The whole difference
    between the two quantities is the 解約控除, which is precisely what 平準純保険料式
    forbids the reserve to carry.  Zero **by definition** when the two basis rates
    differ: the identity is a consequence of ``i_std = i_cv`` and is not asserted
    otherwise, because with a 標準利率 below the pricing basis the reserve exceeds the cash
    value by far more than the 解約控除.
    """
    if i_std != i_cv:                                                # noqa: F821
        return 0.0
    return (reserve_pp(d) - pol_val_pp(d)
            - min(surr_charge_pp(d), max(0.0, reserve_pp(d))))


def check_reserve_identity():
    """True when the reserve exceeds the surrender value by exactly the 解約控除.

    Swept over every anniversary of the run, ``d = 0 … proj_years()``, issue and horizon
    included: this is a statement about a value at a point in time, not about a period.
    """
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_reserve_identity_resid(d)) <= tol
               for d in range(proj_years() + 1))


def check_loan_roll_fwd_resid(d):
    """The loan roll-forward residual across the policy year opening at anniversary d.

    The 契約者貸付 balance and every APL cohort balance, each rolled
    ``L(d + 1) = (L(d) + advance) (1 + i_L)`` and compared with the balance the model
    actually carries.  Identically zero in the base run, where there is no loan at all;
    non-trivial the moment either module is switched on, which is the point of it.

    Annual, like the balances themselves: the 約款 states a 年利 and capitalises it at the
    契約応当日, so there is nothing to roll between anniversaries.
    """
    resid = (loan_pp(d + 1)
             - (loan_pp(d) + pol_loan_draw(d)) * (1.0 + i_loan))     # noqa: F821
    for s in apl_entry_years(12 * d):
        if pols_apl_in(12 * d, s) == 0.0 or apl_fail_year(s) <= d:
            continue
        adv = apl_advance_due(d) if apl_fires(d, s) else 0.0
        resid += (loan_apl_pp(d + 1, s)
                  - (loan_apl_pp(d, s) + adv) * (1.0 + i_loan))      # noqa: F821
    return resid


def check_loan_roll_fwd():
    """True when every loan balance accumulates at ``i_loan`` in every policy year.

    Stops one year short of the end because the residual reads ``loan_pp(d + 1)``.
    """
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_loan_roll_fwd_resid(d)) <= tol
               for d in range(proj_years() - 1))


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in policy month t; zero everywhere.

    :func:`net_cf` less the published ``result_cf()`` columns of the same row.  It closes
    the loop between the total benefit outgo and the two kinds that make it up, so a
    third kind added to :func:`claims` and left out of its total shows up here rather
    than silently vanishing from the statement.
    """
    return (net_cf(t) - premiums(t) + claims(t, "DEATH") + claims(t, "LAPSE")
            + claim_expenses(t) + expenses(t) + commissions(t) + dividends(t))


def check_net_cf():
    """True when the net cash flow equals the sum of its published columns, every month."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(proj_len()))


def result_cf():
    """Result table of cash flows, indexed by the 0-based policy **month** t.

    The frame runs ``t = 0 … proj_len() - 1``, twelve rows to the policy year, and
    ``df.groupby(df.index // 12).sum()`` reads it back as the annual statement.
    ``pols_if`` is the start-of-month count, which is the weight applied to every cash
    flow on the same row.  ``net_cf`` carries the notes' own income-positive sign.
    ``expenses`` is acquisition and maintenance; the claim handling expense is beside it
    in ``claim_expenses``, as it is in every model in the three libraries.
    ``dividends`` is a column of zeros on the 無配当 composite and is published rather
    than dropped, because the participating variant is a real product in the source set.
    """
    ts = list(range(proj_len()))
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
    """Result table of policy counts and decrement rates, indexed by the policy month t.

    Both the annual rates and the monthly decrements are published: ``mort_rate`` and
    ``lapse_rate`` are the annual rates the assumption tables are stated on and the notes
    quote, ``mort_rate_mth`` and ``lapse_rate_mth`` the rates actually applied to the
    month, and ``lapse_spike_rate`` the one-off cliff surge, which is neither — it is
    non-zero in exactly one row of the whole table.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_if_pay": [pols_if_pay(t) for t in ts],
            "pols_apl": [pols_apl(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_lapse_spike": [pols_lapse_spike(t) for t in ts],
            "pols_apl_exit": [pols_apl_exit(t) for t in ts],
            "pols_loan_exit": [pols_loan_exit(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "lapse_spike_rate": [lapse_spike_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """Result table of the policy value, the surrender value and the reserve, by anniversary d.

    **Indexed by the anniversary, not by the month**, because that is what these
    quantities are: the contractual value construction is annual, defined at the
    年単位の契約応当日, and it did not move when the cash flow statement went monthly.  The
    frame is ``d = 0 … proj_years()``, issue and horizon included.

    ``cv_pp`` is the amount payable at the anniversary and ``cv_pp_susp`` the suppressed
    value at every anniversary, so the step at 払込満了 and the value an instant before it
    read off the same table.  ``reserve_pp`` is a reference quantity and produces no cash
    flow.  The value a surrender **between** anniversaries is paid on is
    :func:`cv_at_m`, which interpolates these columns.
    """
    ds = list(range(proj_years() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "prosp_val_pp": [prosp_val_pp(d) for d in ds],
            "surr_charge_pp": [surr_charge_pp(d) for d in ds],
            "pol_val_pp": [pol_val_pp(d) for d in ds],
            "cv_pp": [cv_pp(d) for d in ds],
            "cv_pp_susp": [cv_pp_susp(d) for d in ds],
            "reserve_pp": [reserve_pp(d) for d in ds],
            "loan_pp": [loan_pp(d) for d in ds],
        },
        index=pd.Index(ds, name="d"),                                # noqa: F821
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
