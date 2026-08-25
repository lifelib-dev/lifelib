# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.LTC_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the first policy month and
``t = proj_len() - 1`` the last. Cover is whole of life, so the last month is the last
month of the mortality table's terminal age — 116 for males, 118 for females — and
``proj_len() = 12 * (omega_age() - issue_age() + 1)``. There is no maturity and no
maturity benefit; what ends the projection is the table, not the contract.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/nursing_care/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``LTC_JP_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.LTC_JP_S.Data`, reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
prevalence_file         data.prevalence_table()         prevalence_table.csv
grade_share_file        data.grade_share_table()        grade_share_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
annual rates with ``*_rate_mth`` for their monthly counterparts, ``*_pp`` for
per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind`` string,
``pols_if_at(t, timing)`` for the within-month in-force reads. The technical notes use
compact actuarial symbols instead. The mapping is:

======================  =================================  ================================
Notes symbol            Cells                              Meaning
======================  =================================  ================================
t                       (the cells argument)               Policy month, 0-based
x                       issue_age()                        Issue age, 満年齢
age(t)                  age(t)                             Attained age, x + floor(t/12)
y(t)                    policy_year(t)                     Policy year, floor(t/12) + 1
(none)                  omega_age()                        Terminal age of the table
(none)                  proj_len()                         Number of projected months
(none)                  model_point()                      The selected model point row
A_L                     lump_amount()                      介護一時金額
A_N                     annuity_amount()                   基準介護年金額 per instalment
n_A                     annuity_max()                      Maximum annuity instalments
G_L, G_N, G_W           grade_lump(), grade_annuity(),     Benefit and waiver thresholds
                        grade_waiver()
s_W, s_L, s_N           grade_share(grade)                 Grade shares of the certified
prev(x)                 prev_rate(t)                       All-grade prevalence
prev'(x)                prev_slope(t)                      Its derivative in age
prev_G(x)               prev_grade(t, grade)               Grade-G prevalence
beta, x_mid, prev_ceil  prev_param(name)                   Logistic parameters
k                       care_mort_mult                     Care-state mortality multiple
f_age(x)                f_age(t)                           Sub-65 特定疾病 gate
i_W, i_L, i_N           inc_rate_w(t), inc_rate_l(t),      Annual entry rates
                        inc_rate_n(t)
i_W_m, i_L_m, i_N_m     inc_rate_w_mth(t), and so on       Monthly entry rates
(table)                 mort_rate_base(t)                  Table rate before mort_be_factor
(none)                  mort_rate(t)                       Best-estimate annual mortality
q_H(t)                  mort_rate_mth(t)                   Monthly healthy mortality
(none)                  mort_rate_care(t)                  Annual care-state mortality
q_C(t)                  mort_rate_care_mth(t)              Monthly care-state mortality
(table)                 lapse_rate(t)                      Annual lapse rate
w(t)                    lapse_rate_mth(t)                  Monthly lapse rate
w_cum(t)                lapse_cum(t)                       Cumulative lapse proportion
lam, w_ref              sel_lapse_lambda(), sel_lapse_ref  Anti-selective lapse module
rec_rate                rec_rate(), rec_rate_mth()         Recovery out of the care state
act(t)                  pols_act(t)                        Active, premium-paying lives
care_w(t)               care_w(t)                          Entered G_W: waiver running
care_l(t)               care_l(t)                          Entered G_L: lump sum paid
care_n(t)               care_n(t)                          Entered G_N: annuity running
pols_if(t)              pols_if(t)                         act(t) + care_w(t)
(none)                  pols_if_at(t, timing)              BEF_DECR, BEF_LAPSE, AFT_DECR
n_W, n_L, n_N           pols_entry_w(t), and so on         Expected entrants of the month
(none)                  pols_death(t)                      Deaths of the month
(none)                  pols_lapse(t)                      Lapses of the month
term(t)                 pols_term(t)                       Lives extinguished by the cap
S_C(s, t)               care_surv(s, t)                    Care-state survival, s to t
ann_count(t)            ann_count(t)                       Instalments due in month t
(rider)                 pols_entry_dem(t)                  認知症一時金特約 first diagnoses
P                       premium_mth_pp()                   Monthly office premium
P x act(t)              premiums(t)                        Premium income
A_L n_L, A_N ann_count  claims(t, kind)                    Benefit outgo by kind
ec                      claim_expenses(t)                  Claim handling expense
e(t), E0                expenses(t)                        Maintenance and acquisition
(none)                  inflation_factor(t)                Expense inflation factor
c0                      comm_init_pp()                     Initial commission per policy
c_r                     comm_renewal_rate                  Renewal commission rate
c0, c_r x premiums      commissions(t)                     Commission outgo
net_cf(t)               net_cf(t)                          Net cash flow, income positive
======================  =================================  ================================

Three names needed care.

The notes write ``act(t)`` for the active population. It is spelled :func:`pols_act`
here, because ``act`` next to ``care_w`` reads as an abbreviation of "actual" rather
than as a policy count, and because every other policy-count cells in the library
starts ``pols_``. The three care ledgers keep the notes' own names, since ``care_w``,
``care_l`` and ``care_n`` are already the right shape.

The notes use ``i_G`` for both the annual entry rate and, with an ``_m`` subscript, the
monthly one. The library convention is that a bare ``*_rate`` is annual and
``*_rate_mth`` is monthly, so :func:`inc_rate_l` is the annual rate and
:func:`inc_rate_l_mth` the monthly one, matching ``mort_rate`` / ``mort_rate_mth`` and
``lapse_rate`` / ``lapse_rate_mth`` exactly.

``term(t)`` is spelled :func:`pols_term`. It is a policy count, not a term of the
contract, and the bare word in a life model reads as the policy term — which this
product does not have, being whole of life.

.. rubric:: The three-state chain, and why the ledgers are nested rather than disjoint

Healthy, in care, dead, with the care state absorbing in the base run. The three care
ledgers are **cumulative first-entry counters** riding on one survival ledger, not
three disjoint compartments:

    care_n(t) <= care_l(t) <= care_w(t) <= pols_if(t)   at every t

so they must never be added together. :func:`check_nesting` asserts the ordering.
:func:`pols_entry_w` is drawn from :func:`pols_act` alone, because a life already
certified at ``G_W`` cannot enter it again; :func:`pols_entry_l` and
:func:`pols_entry_n` are drawn from **everyone in force who has not yet reached that
grade**, which includes lives already in a lower care grade, because progression up the
ladder is the dominant route into the higher grades rather than direct entry from
health.

Only :func:`care_w` is a component of :func:`pols_if`. ``pols_if(t) = pols_act(t) +
care_w(t)`` is the definition, and :func:`check_pols_roll_fwd` closes it against the
month's decrements: deaths of the active population at ``q_H``, deaths of the care
population at ``q_C``, lapses of the active population only, and the benefit-driven
termination.

.. rubric:: Premium rides on pols_act, and lapse applies to pols_act

Two of the notes' pitfalls, and they are the same fact seen twice. The waiver fires at
``G_W`` = 要介護1, one grade below the lump sum and two below the annuity, so there is a
real band of lives for whom the contract has stopped collecting premium and has not yet
paid anything. Charging premium to the whole in-force block overstates lifetime premium
income by about 5.9% on the anchor cell — the 5.5% the waiver takes out of the
in-force-weighted total, read against the smaller correct base. And with the premium waived and no 解約返戻金 to
surrender for, a life on waiver has nothing to lapse: applying lapse to
:func:`pols_if` rather than to :func:`pols_act` destroys the annuity liability it took
thirty years to build. The ``whole_life`` 自動振替貸付 machinery must not be inherited
here — there is no surrender value to lend against, so a missed premium lapses the
contract outright.

.. rubric:: 認定率 is a prevalence, and the conversion has two terms

What the government publishes is a **point-in-time count of certified persons**, not a
flow of new certifications. Multiplying it — or its 要介護2以上 share — by a benefit
amount as if it were an annual claim frequency is the single commonest error in a
Japanese nursing-care model. In an illness-death model with no recovery the conversion
is an identity rather than an approximation:

    i_G(x) = prev_G'(x) / (1 - prev_G(x)) + prev_G(x) (mu_C(x) - mu_H(x))

and **the second term is not a refinement**. A rising prevalence understates incidence
because the certified population is simultaneously being drained by its own excess
mortality. Dropping it — which is what happens if the care-state mortality multiple is
set to 1 "because there is no impaired-life table" — cuts lifetime lump-sum claims on
the anchor cell by about 31%. :func:`inc_rate` carries both terms and
:func:`prev_slope` is the analytic derivative of the logistic, not a difference
quotient.

The dimensional check that catches the error: ``prev`` and ``prev_G`` are dimensionless
**proportions of a population**, ``beta`` carries units of 1/year, and both terms of the
identity are therefore rates per year and can be added. A version of the formula that
adds a prevalence to a rate is the commonest way to get this wrong.

.. rubric:: The step in incidence at exactly age 65 belongs there

Below 65 the public limb fires only where the care state arises from one of the 16
特定疾病, and the company-basis limb that partly fills the hole is restricted to lives
満65歳未満. :func:`f_age` is the resulting gate: 0.20 below 65 with the company-basis
limb on, 0.05 with it off, 1.00 at 65 and over. Entry into 要介護2以上 jumps about 6.1x
between age 64 and age 65 on the shipped basis. A smooth curve through 65 misprices
every issue age in the lower half of the 40-79 issue range, which is most of it.

.. rubric:: The annuity ledger, in advance, capped, and computed as a partial product

Instalments fall on the annual anniversaries of the 介護年金支払基準日, so the cohort
entering in month ``s`` is paid in months ``s, s+12, ..., s+12(n_A - 1)`` while it
survives. The ``j = 0`` term of :func:`ann_count` is :func:`pols_entry_n` itself:
**payment in advance, on the entry date**. Deferring the first instalment by a year
removes roughly a tenth of the annuity liability and misdates all of it.

:func:`care_surv` is computed as a **partial product** over the months from ``s`` to
``t``, never as a ratio of cumulative products: the care-state mortality rate reaches 1
at the terminal age, so a cumulative product underflows to zero and the ratio form
divides by zero exactly where the tail of this liability lives.

The cap **binds**, unlike every limit on the ``medical`` chassis: on the anchor cell
entrants take about 4.6 instalments on average and about 15% of them reach the tenth.
:func:`pols_term` is the cohort taking its last permitted instalment; it is removed
from ``care_n``, ``care_l``, ``care_w`` and hence from ``pols_if``, which is the
retroactive extinction of the contract expressed on a monthly grid.

.. rubric:: Modules that are off in the base run

Four of the notes' optional constructions are implemented and switched off on the
anchor cell, so that the base run reproduces the worked example while the machinery
stays visible and testable. Each is exercised by a shipped model point.

- **The state-tested annuity and its recovery decrement.** Under ``annuity_test =
  "state"`` an instalment additionally requires the care state to persist, so the
  annuity cohort carries ``(1 - rec_rate_mth())`` alongside ``(1 - q_C)`` and
  :func:`care_n` loses recoveries — which lets a recovered life re-enter and start
  again from instalment 1 on a **new** 介護年金支払基準日, because
  :func:`pols_entry_n` draws from ``pols_if - care_n``. The switch is a **no-op unless
  ``rec_rate`` is moved off zero**, which is why the two must be tested together;
  model point 5 carries the switch and the notes' suggested 5% p.a. placeholder
  together. Recovery is deliberately scoped to the annuity: the lump sum, once paid,
  cannot be unpaid, and the waiver ledger is left alone **[std scope]**. The known limit
  of that scoping: ``rec_rate`` is the rate of falling below ``G_N`` = 要介護3, not of
  returning to health, so a recovered life keeps its 保険料払込免除 for the rest of the
  contract and never resumes premium. For the modelled step that is right, ``G_W`` =
  要介護1 being two grades lower; recovery below ``G_W`` is not modelled at all, because no
  source publishes a between-grade transition matrix. Premium income under that switch is
  a **lower bound**. See :func:`rec_rate`.
- **Anti-selective lapse.** ``inc_eff = inc_rate x [1 + lam max(0, w_cum - w_ref)]``
  with ``lam = 0`` on every point but 8. Healthy lives lapse first, so the persisting
  block is progressively impaired on the *incidence* basis rather than on mortality —
  which is the opposite direction from a death-benefit product, and the reason the
  loading sits on :func:`inc_rate_mth`.
- **The 認知症一時金特約.** ``dementia_rider`` is false on every point but 6. There is no
  published dementia incidence basis in any retrieved source, so the rider's incidence
  is a **[std] placeholder**: ``dementia_share`` of the entry rate into the lump-sum
  grade, after a ``dementia_wait_mths`` 認知症診断責任開始期. The MCI limb and the dementia
  limb are both once-only and the composite pays both to any life reaching dementia, so
  they are carried as one event at the dementia date paying ``(1 + mci_fraction) x
  dementia_amount`` **[std]** — which gets the amount right and dates the 10% MCI limb
  late.
- **The 1-year 不担保期間** of the simplified-underwriting design, ``waiting_1y``, true
  only on point 7. A state arising inside the 不担保期間 is excluded for good rather than
  deferred, so the waiting period zeroes the entry rates rather than the claims.

Note what the waiting period is **not**. "180日" names two different mechanisms in this
market and a model must not implement one of them twice: a 不担保期間 or a
認知症診断責任開始期 means cover has not started, while the 180-day (90-day for dementia)
test inside the company-basis trigger means the care state must have *persisted*. The
composite has the second and not the first on the care benefits, and the composite's
claim date is the month the trigger is **met**, not the month it is notified — a
certification takes effect retroactively to the application date, so a
notification-dated projection is up to a month late.

.. rubric:: Sign convention, and the zeros that are product facts

The notes' ``net_cf(t)`` is already **income positive** — premiums less claims,
expenses and commission — which is the library-wide sign of :func:`net_cf`, so there is
no outgo-positive ``liability_cf`` companion to publish: one stream, one sign, one name.

``claims(t, "LAPSE")`` exists and returns zero, and ``result_cf()`` carries the zero
column, because there is no 解約返戻金 at any duration and the notes list a non-zero lapse
row as a pitfall imported from products that have one. A column of zeros states the
product fact where a missing column would only hide it. There is deliberately **no**
``claims_death`` and **no** ``cv_pp``: the contract pays nothing on death and has no
surrender value, and inventing either would misstate the liability in a direction the
notes name.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# --- the model point ---

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point."""
    return str(model_point()["policy_id"])


def issue_age():
    """x: the 契約年齢, the attained age at the 契約日 with the fraction discarded.

    満年齢 (*man-nenrei*), incremented at each 年単位の契約応当日, which is the basis every
    carrier in the composite states [S1].  The shipped table is built for a
    保険年齢方式 (nearest-birthday) basis, so reading it at 満年齢 understates the
    valuation age by about half a year; the base run accepts the offset **[std]**,
    exactly as the third-sector chassis does.
    """
    return int(model_point()["issue_age"])


def sex():
    """The sex (M / F) of the insured, a rating factor and a mortality table key."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def lump_amount():
    """A_L: the 介護一時金額, paid once per contract on first entry into ``grade_lump``.

    Paying it does **not** terminate the contract [S1] [S4] [S7] [S12].
    """
    return float(model_point()["lump_amount"])


def annuity_amount():
    """A_N: the 基準介護年金額, one annual 介護年金 instalment [S1] [S7] [S8] [S10]."""
    return float(model_point()["annuity_amount"])


def grade_lump():
    """G_L: the certification grade at or above which the lump sum is paid.

    要介護2以上 on the composite, the modal single threshold across the seven carriers
    and the one whose public base rate is best evidenced **[std]**.
    """
    return str(model_point()["grade_lump"])


def grade_annuity():
    """G_N: the certification grade at or above which the 介護年金 starts.

    要介護3以上 on the composite, one grade above the lump sum, which is the tiering
    three carriers use **[std]**.
    """
    return str(model_point()["grade_annuity"])


def grade_waiver():
    """G_W: the certification grade at or above which 保険料払込免除 starts.

    要介護1以上 on the composite — the lowest observed threshold, and **strictly below**
    both benefit thresholds [S1] [S8] **[std]**.  That ordering is the product fact the
    model has to get right: it creates a band of lives paying nothing and receiving
    nothing.
    """
    return str(model_point()["grade_waiver"])


def annuity_max():
    """n_A: the maximum number of 介護年金 instalments before the contract is
    extinguished.

    Ten on the composite: simultaneously one carrier's hard cap [S1] and one of
    another's published terms [S7], so the cap is evidenced from both sides **[std]**.
    """
    return int(model_point()["annuity_max"])


def annuity_test():
    """The annuity metering basis: ``survival`` or ``state``.

    ``survival``
        each instalment needs only that the insured be alive on the payment date, and
        recovery does not stop it — four carriers against one [S4] [S7] [S10] [S12],
        which is what the composite takes **[std]**.

    ``state``
        the instalment additionally requires the care state to persist, and a life that
        re-qualifies after a lapse of the state gets a **new** 介護年金支払基準日 and starts
        again from instalment 1 [S1] [S2].  This is the only consumer of
        :func:`rec_rate`.
    """
    v = model_point()["annuity_test"]
    if v not in ("survival", "state"):
        raise ValueError("invalid annuity_test")
    return v


def company_limb():
    """True where the 約款-defined company-basis trigger limb is written [S1] [S2].

    A dependency state persisting 180 days (90 where dementia-defined), with the
    insured 満65歳未満 at diagnosis.  It is not modelled as a separate decrement — its
    only effect here is on :func:`f_age`, because it is what partly backfills the
    sub-65 restriction on the public limb.
    """
    return bool(model_point()["company_limb"])


def dementia_rider():
    """True where the 認知症一時金特約 is attached.  Off on the anchor cell."""
    return bool(model_point()["dementia_rider"])


def dementia_amount():
    """The 認知症診断一時金 amount of the rider, paid once per contract [S4] [S5] [S7]."""
    return float(model_point()["dementia_amount"])


def mci_fraction():
    """The 軽度認知障害 (MCI) limb as a fraction of :func:`dementia_amount`.

    10% at both carriers that publish one [S7] [S13] — one of the few genuinely
    market-wide parameters in this product.  See the Space docstring for why the two
    limbs are carried as one event.
    """
    return float(model_point()["mci_fraction"])


def waiting_1y():
    """True where the 1-year 不担保期間 of the simplified-underwriting design applies.

    Off on the composite, which is fully underwritten [S1] [S7] [S11]; carried as a
    model point flag because it is the explicit price of three-question simplified
    underwriting at one carrier [S7].
    """
    return bool(model_point()["waiting_1y"])


def waiting_mths():
    """The 不担保期間 in months: 12 where :func:`waiting_1y`, otherwise 0.

    A state arising inside the 不担保期間 is excluded for good rather than deferred, so
    this zeroes the entry rates in :func:`inc_rate_mth` rather than the claims **[std]**.
    """
    return 12 if waiting_1y() else 0


def sel_lapse_lambda():
    """lam: the anti-selective lapse loading on *incidence*, zero in the base run.

    A model point column rather than a Space Reference, so that one shipped point can
    exercise the module while the rest of the table stays on the notes' base basis.
    No Japanese selective-lapse evidence was retrieved; the level is a **[std]**
    placeholder identical to the third-sector chassis's.
    """
    return float(model_point()["sel_lapse_lambda"])


def rec_rate():
    """The annual rate of falling **below the annuity grade** ``G_N``; zero in the base run.

    Not a recovery-to-health rate.  It is applied to :func:`care_n` alone, so a life that
    recovers leaves the annuity ledger and may re-qualify on a new 介護年金支払基準日, but
    **keeps its 保険料払込免除 for the rest of the contract**: it stays in :func:`care_w`,
    never re-enters :func:`pols_act`, never resumes premium and is never again exposed to
    lapse.

    For the step modelled that is right — ``G_W`` = 要介護1 is two grades below ``G_N`` =
    要介護3, so a 要介護3 -> 要介護2 downgrade stops a state-tested annuity and leaves the
    waiver running [S1] [S2] [S8].  Recovery *below* ``G_W``, which would end the waiver
    and restore the premium, is **not modelled**: no retrieved source publishes a
    transition matrix between grades and one rate cannot carry two thresholds, so the
    model implements the threshold it can evidence and names the other as a gap
    **[std scope]**.  Under ``annuity_test = "state"`` with a non-zero rate, premium
    income is therefore a **lower** bound and the waived band an upper bound: :func:`pols_act`
    is bit-identical to the ``rec_rate`` = 0 run while :func:`care_n` is materially smaller.
    The only route by which recovery reaches :func:`care_w` is the ten-payment cap, which it
    moves **upward** — a recovered life takes no tenth instalment, so :func:`pols_term`
    extinguishes fewer contracts.

    The care state is absorbing in the base run.  That is forced by the sources and it
    is a real simplification, not a harmless one — the statute provides for the grade to
    move up *or down* at 要介護更新認定 [R1] and a carrier's own FAQ addresses recovery
    [S3] — so it is carried as a **named input set to zero** rather than omitted.

    Consumed **only** by the ``state`` annuity test: on the composite's survival-tested
    annuity a recovery does not stop payment [S7] and a paid lump sum cannot be unpaid
    [S1], so recovery has nothing to act on.  Returning zero on the survival test is
    what makes that explicit.
    """
    return float(model_point()["rec_rate"]) if annuity_test() == "state" else 0.0


def rec_rate_mth():
    """The monthly recovery rate, ``1 - (1 - rec_rate())^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - rec_rate()) ** (1.0 / 12.0)


def premium_mth_pp():
    """P: the level monthly office premium per policy, a model point **input**.

    Not a computed quantity.  No carrier publishes 予定発生率, 予定利率 or 予定死亡率 for
    this product, the regulator confirms there is nothing standard to publish for
    第三分野 business [R10], and the 算出方法書 is a 基礎書類 filed with the 金融庁 and is not
    public [REG-R2].  The anchor cell's ¥11,500 is the rounded sum of two published
    specimen rates at male 60, 月払, 終身/終身払 [S6] [S8] **[std]**.
    """
    return float(model_point()["premium"])


def prem_mode():
    """The 払込回数: monthly on the composite, which is why the grid is monthly [S1]."""
    return str(model_point()["prem_mode"])


def prem_period_type():
    """The 保険料払込期間 as a **category**: 終身払 (whole of life) on every carrier here.

    Named ``*_type`` because it returns a category and not a duration: the library-wide
    ``prem_period`` is a number of the model's own grid units, and this product has no
    such number — 終身払 runs to the terminal age of the table, which is what
    :func:`proj_len` computes.  The model point column keeps the name ``prem_period``.
    """
    v = model_point()["prem_period"]
    if v != "whole_life":
        raise ValueError("only 終身払 is in scope")
    return v


# --- the timeline ---

def omega_age():
    """The terminal age of the mortality table for this life's sex.

    Read from the shipped table rather than hard-coded: 116 for males and 118 for
    females on 第三分野標準生命表2018 [REG-R18] [REG-R20], and whatever a replacement table
    carries after that.  The table's last row for a sex has ``mort_rate = 1``.
    """
    tbl = data.mort_table()                                          # noqa: F821
    return int(max(a for (s, a) in tbl.index if s == sex()))


def proj_len():
    """The number of projected policy months, ``12 (omega_age() - issue_age() + 1)``.

    684 for the anchor cell.  Cover and premiums are both whole of life [S1] [S4] [S7]
    [S8] [S10] [S11], so nothing but the table ends the projection: there is no
    maturity, no maturity benefit and no renewal.
    """
    return 12 * (omega_age() - issue_age() + 1)


def age(t):
    """age(t): the attained 満年齢 in policy month t, ``x + floor(t / 12)``."""
    return issue_age() + t // 12


def policy_year(t):
    """y(t): the policy year of month t, ``floor(t / 12) + 1``, 1-based."""
    return t // 12 + 1


# --- mortality ---

def mort_rate_base(t):
    """The mortality table rate at ``age(t)``, before ``mort_be_factor``.

    A **[std]** construction in the shape of 第三分野標準生命表2018 — quoted anchors joined by
    a log-linear graduation — rather than a copy of it; see :mod:`~.LTC_JP_S.Data`.
    """
    return float(data.mort_table().loc[(sex(), age(t)), "mort_rate"])  # noqa: F821


def mort_rate(t):
    """The best-estimate annual mortality of a healthy life at ``age(t)``.

    ``mort_be_factor x q_third_sector(age, sex)``, capped at 1.  The table is a **valuation**
    table whose margin runs the wrong way for a best estimate on a living-benefit
    product: it is graduated from a national life table rather than insured experience,
    it excludes 高度障害, and its risk-theory adjustment is bounded 70% below and 85%
    above the unadjusted rate [R9] [REG-R20].  ``mort_be_factor = 1.25`` is the reciprocal of
    0.80, a round value inside that sourced band — it unwinds the table's stated margin
    and nothing more **[std]** — and is identical to the third-sector chassis's, because
    it is the same table read for the same reason.
    """
    return min(1.0, mort_be_factor * mort_rate_base(t))                    # noqa: F821


def mort_rate_mth(t):
    """q_H(t): monthly healthy mortality, ``1 - (1 - mort_rate(t))^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def mort_rate_care(t):
    """The annual mortality of a life in the care state at ``age(t)``.

    ``k x mort_rate(t)`` with ``k = care_mort_mult = 2.75``, capped at 1.  No
    impaired-life table for the 要介護 state exists in any retrieved source, so the
    multiple is anchored on two sourced numbers instead: 平均余命 at age 75 on
    第23回完全生命表 is 12.54 years for a male [R13] [REG-R24], and the only quantified
    duration of care in any retrieved source is a household survey's average of 55.0
    months [R14].  On a constant-force approximation life expectancy is the reciprocal
    of the force, so 12.54 / 4.583 = 2.74, rounded to 2.75 **[std]**.  Both inputs are
    biased and the biases are named rather than netted; there is no observed range.

    On the shipped table ``k x mort_rate`` first exceeds 1 at male age 105 and female age
    111, so the cap binds from there, where the surviving block is negligible **[std]**.

    ``k`` is **not** only a post-onset assumption: it is also the second term of the
    incidence identity in :func:`inc_rate`, and dropping it cuts lifetime lump-sum
    claims on the anchor cell by about 31%.  That coupling is the least obvious property
    of this model.
    """
    return min(1.0, care_mort_mult * mort_rate(t))                   # noqa: F821


def mort_rate_care_mth(t):
    """q_C(t): monthly care-state mortality, from :func:`mort_rate_care` **[std]**."""
    return 1.0 - (1.0 - mort_rate_care(t)) ** (1.0 / 12.0)


# --- lapse ---

def lapse_rate(t):
    """The annual lapse rate in the policy year of month t, from *lapse_table.csv*.

    The policy year is capped at the last year in the table, which carries the terminal
    rate — a whole-of-life projection would otherwise run off the end of it.  The only
    published industry-wide persistency figure in Japan is a 5.6% p.a. 解約・失効率 on
    個人保険 measured on opening in-force sum assured [REG-R31], and no Japanese
    durational curve is public, so the shape is a **[std]** standardization anchored to
    that single number.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(max(tbl.index)))
    return float(tbl.loc[y, "lapse_rate"])


def lapse_rate_mth(t):
    """w(t): the monthly lapse rate, ``1 - (1 - lapse_rate(t))^(1/12)`` **[std]**.

    Applied to :func:`pols_act` only — see the Space docstring.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_cum(t):
    """w_cum(t): the proportion of the original cohort lapsed before month t.

    A proportion of the *original* cohort, not a running total of :func:`lapse_rate`,
    and it drives a loading on **incidence** rather than on mortality — see
    :func:`sel_lapse_factor`.
    """
    if t <= 0:
        return 0.0
    return lapse_cum(t - 1) + pols_lapse(t - 1)


def sel_lapse_factor(t):
    """The anti-selective lapse loading on incidence; 1.0 in the base run.

    ``1 + lam max(0, w_cum(t) - w_ref)`` with ``w_ref = sel_lapse_ref = 0.20`` and
    ``lam = sel_lapse_lambda()`` **[std]**.  Healthy lives lapse first, so the persisting
    block is progressively impaired on the *incidence* basis — the opposite direction
    from a death-benefit product, where the same mechanism loads mortality.  No Japanese
    selective-lapse evidence was retrieved.
    """
    return 1.0 + sel_lapse_lambda() * max(0.0, lapse_cum(t) - sel_lapse_ref)  # noqa: F821


# --- the morbidity basis ---

def prev_param(name):
    """One parameter of the certification prevalence logistic, from the input table.

    ``prev_ceil``, ``prev_beta`` and ``prev_x_mid`` are the fitted **[std]**
    parameters; the file also carries the two sourced 認定率 anchors they were pinned to,
    4.3% at ages 65-74 and 31.1% at 75 and over [R4] [R5] [REG-R30].
    """
    return float(data.prevalence_table().loc[name, "value"])         # noqa: F821


def grade_share(grade):
    """s_G: the share of all certified persons at ``grade`` **or above**.

    0.715 at 要介護1以上, 0.508 at 要介護2以上 and 0.340 at 要介護3以上, from the published
    grade composition [R4] [REG-R30].  Holding the shares constant across ages is a
    standardization with a known direction of error: severity composition worsens with
    age, so the model **understates** 要介護3以上 prevalence at old ages and overstates it
    at young ones.  The published composition is a single all-ages figure, so no
    observed range exists **[std]**.
    """
    return float(data.grade_share_table().loc[grade, "share_ge"])    # noqa: F821


def prev_rate(t):
    """prev(x): the all-grade certification prevalence at ``age(t)``.

    A logistic in attained age **[std]**,
    ``prev_ceil / (1 + exp(-beta (x - x_mid)))``, pinned to the two sourced 認定率 at
    representative ages 70 and 82 [R4] [R5] [REG-R30].  Only two age-banded rates were
    retrieved; the five-year-band rates that a finer basis wants sit in an unfetched
    e-Stat release of the same statistic [REG-R33].

    Read the fitted tail as an upper bound on the gradient: because ``prev`` is convex
    over the 75+ band, pinning at the population mean age assigns the band average to
    too young an age and therefore **overstates** ``beta``.

    **Nothing above age 82 is sourced, and that is where the claims are.**  The logistic
    has three parameters and two anchors, so one degree of freedom is unidentified — and
    the free one, ``prev_ceil`` = 0.95 **[std]**, is the one that sets the tail.
    ``prev(90) = 0.662`` and ``prev(100) = 0.894`` are extrapolations, not fitted values,
    and 40.2% of the anchor cell's lifetime benefit outgo (74.7% at issue age 79) falls
    at attained age 83 or over.  That makes the tail a first-order model risk rather than
    a detail of the fit; ``technical-notes.md`` carries the sensitivity and the shipped
    tests pin both rates.
    """
    ceil = prev_param("prev_ceil")
    beta = prev_param("prev_beta")
    x_mid = prev_param("prev_x_mid")
    return ceil / (1.0 + math.exp(-beta * (age(t) - x_mid)))         # noqa: F821


def prev_slope(t):
    """prev'(x): the derivative of :func:`prev_rate` in age, a rate per year.

    The **analytic** derivative of the logistic,
    ``beta prev (1 - prev / prev_ceil)``, not a difference quotient: it is one of the
    two terms of the incidence identity and a numerical derivative would put noise
    straight into the claim rate.
    """
    ceil = prev_param("prev_ceil")
    beta = prev_param("prev_beta")
    p = prev_rate(t)
    return beta * p * (1.0 - p / ceil)


def prev_grade(t, grade):
    """prev_G(x): the prevalence of certification at ``grade`` or above at ``age(t)``.

    ``s_G x prev(x)`` — a dimensionless **proportion of a population**, never a rate.
    """
    return grade_share(grade) * prev_rate(t)


def f_age(t):
    """f_age(x): the sub-65 特定疾病 gate on the entry rates **[std]**.

    Below 65 the public limb fires only where the care state arises from one of the 16
    特定疾病 listed in 介護保険法施行令 第2条 [R1] [R3], and the company-basis limb that partly
    fills the hole is restricted to lives 満65歳未満 [S1] [S4] [S12].  So the gate is
    0.20 below 65 with the company limb written and 0.05 without it, 1.00 at 65 and
    over.

    ``f_sub65 = 0.20`` is a standardization with a weak anchor and is named as such:
    第2号被保険者 are 1.85% of all certified persons [R4], but the 第2号被保険者 denominator
    was not retrieved so no rate can be computed, and the factor is set well above 1.85%
    because the company-basis limb backfills part of the restriction.  There is **no
    observed range**.  The gate produces a step of about 6.1x in incidence between age
    64 and age 65, which is a real feature of the product and not an artefact to smooth
    away.
    """
    if age(t) >= sub65_age:                                          # noqa: F821
        return 1.0
    return f_sub65 if company_limb() else f_sub65_no_limb            # noqa: F821


def inc_rate(t, grade):
    """i_G(x): the annual rate of first entry into ``grade`` or above at ``age(t)``.

    The two-term prevalence-to-incidence identity, gated below 65:

        i_G(x) = f_age(x) [ prev_G'(x) / (1 - prev_G(x))
                            + prev_G(x) (mu_C(x) - mu_H(x)) ]

    with ``mu_C - mu_H = (k - 1) mort_rate(x)``.  **The second term is not a
    refinement**: a rising prevalence understates incidence because the certified
    population is being drained by its own excess mortality, and on the anchor basis the
    mortality term is 5.8% of ``i_L`` at age 60 and a much larger share at the ages
    where claims actually happen.

    The conversion rests on a **stationary-population assumption [std]**: the
    cross-sectional 認定率 by age is read as the prevalence path a cohort will follow.
    Certified persons have grown roughly 2.8-fold in the 23 years since the scheme began
    [R16], so the cross-section is *not* a cohort path; the assumption is stated rather
    than hidden.
    """
    pg = prev_grade(t, grade)
    slope_term = grade_share(grade) * prev_slope(t) / (1.0 - pg)
    mort_term = pg * (care_mort_mult - 1.0) * mort_rate(t)           # noqa: F821
    return f_age(t) * (slope_term + mort_term)


def inc_rate_mth(t, grade):
    """The monthly rate of first entry into ``grade`` or above, ``i_G(x) / 12`` **[std]**.

    Uniform within the policy year, exactly as the third-sector chassis treats its
    incidence.  Loaded by :func:`sel_lapse_factor`, which is 1.0 in the base run, and
    zero inside the 不担保期間 of :func:`waiting_mths`.
    """
    if t < waiting_mths():
        return 0.0
    return inc_rate(t, grade) / 12.0 * sel_lapse_factor(t)


def inc_rate_w(t):
    """i_W: the annual rate of entry into the waiver grade ``G_W`` at ``age(t)``."""
    return inc_rate(t, grade_waiver())


def inc_rate_l(t):
    """i_L: the annual rate of entry into the lump-sum grade ``G_L`` at ``age(t)``."""
    return inc_rate(t, grade_lump())


def inc_rate_n(t):
    """i_N: the annual rate of entry into the annuity grade ``G_N`` at ``age(t)``."""
    return inc_rate(t, grade_annuity())


def inc_rate_w_mth(t):
    """i_W_m: the monthly rate of entry into the waiver grade in month t."""
    return inc_rate_mth(t, grade_waiver())


def inc_rate_l_mth(t):
    """i_L_m: the monthly rate of entry into the lump-sum grade in month t."""
    return inc_rate_mth(t, grade_lump())


def inc_rate_n_mth(t):
    """i_N_m: the monthly rate of entry into the annuity grade in month t."""
    return inc_rate_mth(t, grade_annuity())


# --- the three-state chain ---

def pols_act(t):
    """act(t): the **active** population at the start of month t.

    In force and not yet certified at ``G_W``: the premium-paying and lapse-exposed
    population.  ``act(0) = 1``, then

        act(t+1) = ( act(t) - n_W(t) ) (1 - q_H(t)) (1 - w(t))

    Care-state lives are not here: they carry mortality only.
    """
    if t <= 0:
        return 1.0 if t == 0 else 0.0
    prev_t = t - 1
    return ((pols_act(prev_t) - pols_entry_w(prev_t))
            * (1.0 - mort_rate_mth(prev_t))
            * (1.0 - lapse_rate_mth(prev_t)))


def care_w(t):
    """care_w(t): in force and entered ``G_W`` — waiver running, premium zero.

    ``care_w(0) = 0``, then

        care_w(t+1) = ( care_w(t) + n_W(t) ) (1 - q_C(t)) - term(t)

    Lapse is suspended for these lives: with the premium waived and treated as paid on
    each 払込期月の契約応当日 [S1] [S2] there is no premium to miss, and with no 解約返戻金
    there is nothing to surrender for.

    :func:`rec_rate` does **not** act on this ledger, under either annuity test.  It is
    the rate of falling below ``G_N``, two grades above ``G_W``, so a life it moves keeps
    its waiver for life; see :func:`rec_rate` for why the second threshold is not
    modelled and which way that biases premium income.
    """
    if t <= 0:
        return 0.0
    prev_t = t - 1
    return ((care_w(prev_t) + pols_entry_w(prev_t))
            * (1.0 - mort_rate_care_mth(prev_t))
            - pols_term(prev_t))


def care_l(t):
    """care_l(t): in force and entered ``G_L`` — the lump sum has been paid.

    A cumulative first-entry counter, not a compartment: it is nested inside
    :func:`care_w`, never added to it.
    """
    if t <= 0:
        return 0.0
    prev_t = t - 1
    return ((care_l(prev_t) + pols_entry_l(prev_t))
            * (1.0 - mort_rate_care_mth(prev_t))
            - pols_term(prev_t))


def care_n(t):
    """care_n(t): in force and entered ``G_N`` — the 介護年金 is in payment.

    Carries the recovery decrement under the ``state`` annuity test and nothing extra
    under the ``survival`` test, so that a recovered life falls back into the pool
    :func:`pols_entry_n` draws from and can re-qualify on a **new** 介護年金支払基準日.
    """
    if t <= 0:
        return 0.0
    prev_t = t - 1
    return ((care_n(prev_t) + pols_entry_n(prev_t))
            * (1.0 - mort_rate_care_mth(prev_t))
            * (1.0 - rec_rate_mth())
            - pols_term(prev_t))


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy month t.

    ``pols_act(t) + care_w(t)``: alive, not lapsed and not extinguished by the annuity
    cap, whether or not the premium is being waived.  ``pols_if(0) = 1``.  This is the
    weight on every cash flow of the same ``result_cf()`` row.  Zero from
    ``proj_len()`` on.
    """
    if t < 0 or t > proj_len():
        return 0.0
    return pols_act(t) + care_w(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after care incidence and mortality, before lapse — the notes' processing order
        is incidence, then mortality, then lapse **[std order]** — so this is the
        population lapses are taken from, plus the care lives that are not exposed to
        them.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state, after lapse and after the benefit-driven
        termination.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return ((pols_act(t) - pols_entry_w(t)) * (1.0 - mort_rate_mth(t))
                + (care_w(t) + pols_entry_w(t)) * (1.0 - mort_rate_care_mth(t)))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_entry_w(t):
    """n_W(t): expected entrants into ``G_W`` in month t, from the active population.

    ``act(t) i_W_m(t)``.  Drawn from :func:`pols_act` alone, because a life already
    certified at ``G_W`` cannot enter it again.
    """
    return pols_act(t) * inc_rate_w_mth(t)


def pols_entry_l(t):
    """n_L(t): expected entrants into ``G_L`` in month t.

    ``(pols_if(t) - care_l(t)) i_L_m(t)``.  Drawn from **everyone in force who has not
    yet reached that grade**, which includes lives already on waiver: progression up the
    ladder is the dominant route into the higher grades, not direct entry from health.
    """
    return (pols_if(t) - care_l(t)) * inc_rate_l_mth(t)


def pols_entry_n(t):
    """n_N(t): expected entrants into ``G_N`` in month t, and the annuity cohort of t.

    ``(pols_if(t) - care_n(t)) i_N_m(t)``.  This cohort is paid its first instalment
    **immediately**, in the month of entry: see :func:`ann_count`.
    """
    return (pols_if(t) - care_n(t)) * inc_rate_n_mth(t)


def pols_death(t):
    """Expected deaths in month t, across both the active and the care populations.

    Active lives carry ``q_H``, care lives ``q_C``, both applied after the month's care
    incidence.  Death pays **nothing**: the contract terminates with no 死亡保険金 [S1]
    [S11], which is why there is no ``claims_death`` cells anywhere in this model.
    """
    return ((pols_act(t) - pols_entry_w(t)) * mort_rate_mth(t)
            + (care_w(t) + pols_entry_w(t)) * mort_rate_care_mth(t))


def pols_lapse(t):
    """Lapses at the end of month t, from the survivors of mortality in ``pols_act``.

    Pays **nothing** — there is no 解約返戻金 at any duration [S1] [S2] [S7] [S8] — so
    this moves :func:`pols_if` and nothing else.  Lives on waiver are not exposed.
    """
    return ((pols_act(t) - pols_entry_w(t)) * (1.0 - mort_rate_mth(t))
            * lapse_rate_mth(t))


def pols_term(t):
    """term(t): lives extinguished by taking their last permitted annuity instalment.

    The cohort that entered ``G_N`` in month ``t - 12 (n_A - 1)`` and has survived to
    ``t``.  It is removed from :func:`care_n`, :func:`care_l`, :func:`care_w` and hence
    from :func:`pols_if` — the retroactive extinction of the contract on the tenth
    instalment [S1], expressed on a monthly grid.

    On the anchor cell the cap **binds**: about 15% of entrants reach the tenth
    instalment.  Do not carry the ``medical`` chassis's intuition across, where the 通算
    day ledger never binds on the expectation.
    """
    s = t - 12 * (annuity_max() - 1)
    if s < 0:
        return 0.0
    return pols_entry_n(s) * care_surv(s, t)


def care_surv(s, t):
    """S_C(s, t): survival in the care state from month s to month t.

    The **partial product** of ``(1 - q_C(u))`` over ``u = s ... t-1``, times
    ``(1 - rec_rate_mth())`` per month under the ``state`` annuity test.  Computed as a
    partial product and never as a ratio ``SC(t) / SC(s)`` of cumulative products:
    ``q_C`` reaches 1 at the terminal age, so a cumulative product underflows to zero
    and the ratio form divides by zero exactly where the tail of this liability lives.
    """
    if t <= s:
        return 1.0
    return (care_surv(s, t - 1)
            * (1.0 - mort_rate_care_mth(t - 1))
            * (1.0 - rec_rate_mth()))


def ann_count(t):
    """The expected number of 介護年金 instalments falling due in month t.

    Instalments fall on the annual anniversaries of the 介護年金支払基準日, so the cohort
    entering in month ``s`` is paid in months ``s, s+12, ..., s+12(n_A - 1)`` while it
    survives [S1] [S7]:

        ann_count(t) = sum over j = 0 ... n_A-1 of  n_N(t - 12j) S_C(t - 12j, t)

    The ``j = 0`` term is :func:`pols_entry_n` itself: **payment in advance, on the
    entry date**.  Deferring the first instalment by a year would remove roughly a tenth
    of the annuity liability and misdate all of it.
    """
    total = 0.0
    for j in range(annuity_max()):
        s = t - 12 * j
        if s < 0:
            continue
        total += pols_entry_n(s) * care_surv(s, t)
    return total


# --- the dementia rider, off in the base run ---

def dem_inc_rate_mth(t):
    """The monthly rate of a first 器質性認知症 diagnosis under the rider **[std]**.

    ``dementia_share`` of the entry rate into the lump-sum grade, zero before the
    ``dementia_wait_mths`` 認知症診断責任開始期 [S4] [S5] and zero when the rider is not
    attached.  **No published dementia incidence basis appears in any retrieved
    source**, so both the share and the waiting period are placeholders in the shape of
    such a basis, exactly as the reference libraries treat an unsourced rider incidence.
    There is no observed range.
    """
    if not dementia_rider() or t < dementia_wait_mths:               # noqa: F821
        return 0.0
    return dementia_share * inc_rate_l_mth(t)                        # noqa: F821


def care_dem(t):
    """In force and already paid the rider's 認知症 benefit; a first-event counter.

    Once only per contract [S4] [S5] [S7] [S13].  Carried on the care-state mortality
    basis, like the three care ledgers, and held at or below :func:`pols_if` so that
    :func:`pols_entry_dem` always draws from a non-negative pool: the rider's incidence
    is unrelated to the annuity cohort that drives :func:`pols_term`, so the ledger has
    no other claim on the terminated lives **[std]**.
    """
    if t <= 0 or not dementia_rider():
        return 0.0
    prev_t = t - 1
    carried = ((care_dem(prev_t) + pols_entry_dem(prev_t))
               * (1.0 - mort_rate_care_mth(prev_t)))
    return min(pols_if(t), carried)


def pols_entry_dem(t):
    """Expected first 認知症 diagnoses under the rider in month t.

    ``(pols_if(t) - care_dem(t)) x dem_inc_rate_mth(t)``.  Zero on every model point
    but 6.
    """
    return (pols_if(t) - care_dem(t)) * dem_inc_rate_mth(t)


# --- cash flows ---

def premiums(t):
    """Premium income at the start of month t: ``P x pols_act(t)``.

    **Not** ``P x pols_if(t)``.  The waiver fires two grades below the annuity and one
    below the lump sum, so a band of lives pays nothing and receives nothing; charging
    premium to the whole in-force block overstates lifetime premium income by about 5.9%
    on the anchor cell, and at age 85 the band on waiver is about 30% of the block.
    """
    return premium_mth_pp() * pols_act(t)


def claims(t, kind=None):
    """Benefit outgo at the end of month t, by ``kind``.

    ``"LUMP"``
        ``A_L n_L(t)``: the 介護一時金, once per contract on first entry into ``G_L``.
        Paying it does not terminate the contract [S1] [S4] [S7] [S12].

    ``"ANNUITY"``
        A **living** benefit, paid on survival in the certified care state and stopped by
        death: ``A_N ann_count(t)``, the 介護年金, in advance, capped at ``n_A``
        instalments.  The column name ``claims_annuity`` describes the benefit's *form*,
        a stream of instalments, not its contingency; in ``IncomeTerm_JP_S`` the same
        name is a **death** benefit, so the contingency is stated here rather than
        inferred from the name.
        Where the annuity triggers before the lump sum has been paid, the unpaid lump
        sum is paid together with the first instalment [S1]; on the expectation the
        nesting of the ledgers already delivers that, since ``care_n <= care_l``.

    ``"DEMENTIA"``
        the 認知症一時金特約, ``(1 + mci_fraction) x dementia_amount`` per first
        diagnosis.  Zero unless the rider is attached; see the Space docstring for why
        the MCI limb and the dementia limb are carried as one event.

    ``"LAPSE"``
        identically **zero**, and published rather than dropped.  There is no 解約返戻金
        at any duration [S1] [S2] [S7] [S8], so a lapse pays nothing — the zero is the
        product fact.

    With no ``kind`` the total of the three benefit limbs.
    """
    if kind is None:
        return (claims(t, "LUMP") + claims(t, "ANNUITY")
                + claims(t, "DEMENTIA"))
    if kind == "LUMP":
        return lump_amount() * pols_entry_l(t)
    if kind == "ANNUITY":
        return annuity_amount() * ann_count(t)
    if kind == "DEMENTIA":
        return (1.0 + mci_fraction()) * dementia_amount() * pols_entry_dem(t)
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def claim_expenses(t):
    """ec x (n_L(t) + ann_count(t)): the claim-handling expense of month t **[std]**.

    ¥5,000 per claim event — the lump sum, and **each** annuity instalment — raised from
    the third-sector chassis's ¥3,000 because a care claim requires verification of a
    municipal certification the insurer does not control, or adjudication of a 180-day
    persistence test against a 約款 definition the carrier itself says differs from the
    public standard [S1] [S2], and every annuity instalment carries an annual survival
    check [S1] [S7].  Uninflated.  The rider's diagnoses are charged the same fee, which
    leaves the figure identical to the notes' whenever the rider is off.
    """
    return expense_claim * (pols_entry_l(t) + ann_count(t)           # noqa: F821
                            + pols_entry_dem(t))


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^floor(t/12)`` **[std]**.

    1.0% p.a. flat, stepping at each 年単位の契約応当日 rather than monthly.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def expenses(t):
    """E0 and e(t): **acquisition and maintenance** expense in month t **[std]**.

    ¥20,000 acquisition per policy at ``t = 0``, then ¥250 per policy per month
    inflating at 1.0% p.a.  Maintenance is charged on :func:`pols_if`, **including lives
    on waiver**: the policy is still administered when nobody is paying for it.

    The claim-handling expense is **not** here.  It is a separate cells,
    :func:`claim_expenses`, deducted on its own line in :func:`net_cf` and published in
    its own ``claim_expenses`` column of :func:`result_cf`, which is what ``expenses``
    means everywhere in this library.  ``technical-notes.md`` prints the two **combined**
    in its worked-example ``expenses`` column and in its year-1 total — so the notes'
    ¥20,250.09 at ``t = 0`` is ``expenses(0) + claim_expenses(0)``, and the notes say so
    at the table.
    """
    acq = expense_acq if t == 0 else 0.0                             # noqa: F821
    return acq + expense_maint * inflation_factor(t) * pols_if(t)    # noqa: F821


def comm_init_pp():
    """c0: initial commission per policy issued, ``1.5 x 12 P`` **[std]**.

    ¥207,000 on the anchor cell, paid upfront at ``t = 0``.  With the acquisition
    expense this is what produces the deep new business strain of the worked example's
    first row.
    """
    return comm_init_rate * 12.0 * premium_mth_pp()                      # noqa: F821


def commissions(t):
    """Commission outgo in month t **[std]**.

    The initial commission at ``t = 0``, then 3.0% of premium income from policy year 2
    — that is, from ``t = 12``.  Both levels are standardizations inherited from the
    third-sector chassis.  Renewal commission rides on :func:`premiums`, so it stops
    when the waiver stops the premium.
    """
    init = comm_init_pp() if t == 0 else 0.0
    renew = comm_renewal_rate * premiums(t) if t >= 12 else 0.0      # noqa: F821
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**.

    Premiums less the lump sum, the annuity, the rider, acquisition and maintenance
    expense, the claim-handling expense — deducted on its own line, because
    :func:`expenses` no longer carries it — and commission.  The notes' own sign, which
    is also the library-wide convention, so there is no outgo-positive ``liability_cf``
    companion to publish.

    The shape to expect is a deep month-0 strain, upfront commission and acquisition
    expense against a single month's premium, then thin positive margins for
    twenty-five years, then a long negative tail: this product prefunds a cost that
    essentially does not arise until the block is old, which is what makes the **lapse
    assumption, not the incidence basis, the dominant lever**.
    """
    return (premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
            - commissions(t))


# --- checks ---

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - deaths - lapses - terminations``.  The three
    decrements are the only ways a life leaves this contract: there is no maturity, and
    recovery is scoped to the annuity ledger, so nothing else may move
    :func:`pols_if`.  A lapse applied to the care population, or a termination not
    removed from ``care_w``, shows up here.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_term(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    No argument, one bool over all t, the library-wide shape of a ``check_*`` cells;
    :func:`check_pols_roll_fwd_resid` gives the signed residual of the month that
    failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_nesting_resid(t):
    """The smallest slack in the ledger ordering at month t; non-negative everywhere.

    ``min(pols_if - care_w, care_w - care_l, care_l - care_n)``.  The three care
    ledgers are marginal first-entry distributions riding on one survival ledger, so
    the ordering ``care_n <= care_l <= care_w <= pols_if`` is what makes them
    meaningful — and a negative value here would mean a life had started the annuity
    before its lump sum was paid, which the contract forbids.
    """
    return min(pols_if(t) - care_w(t),
               care_w(t) - care_l(t),
               care_l(t) - care_n(t))


def check_nesting():
    """True when the three care ledgers stay nested inside the in-force in every month.

    The notes' ``check_nesting()``: it asserts the **ordering**, never a sum, because
    the ledgers must never be added together.
    """
    return all(check_nesting_resid(t) >= -roll_fwd_tol               # noqa: F821
               for t in range(proj_len() + 1))


def check_ann_ledger_resid(t):
    """The annuity ledger residual in month t; zero everywhere.

    :func:`ann_count` less an independent rebuild that scans **every** month ``s`` in
    the window ``t - 12 n_A < s <= t`` and keeps those on an annual anniversary of the
    entry month, rather than stepping back in twelves.  A ledger that paid the first
    instalment a year late, that ran past the cap, or that used a ratio form of
    :func:`care_surv` would show up here.
    """
    built = 0.0
    for s in range(max(0, t - 12 * annuity_max() + 1), t + 1):
        if (t - s) % 12 == 0:
            built += pols_entry_n(s) * care_surv(s, t)
    return ann_count(t) - built


def check_ann_ledger():
    """True when the annuity ledger closes in every projected month."""
    return all(abs(check_ann_ledger_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The residual between :func:`net_cf` and the published components; zero everywhere.

    ``net_cf`` less ``premiums - claims_lump - claims_annuity - claims_dementia -
    claims_lapse - expenses - claim_expenses - commissions``, which are exactly the
    columns of :func:`result_cf`.  A cash flow that exists in ``net_cf`` but not in the
    statement, or the reverse, shows up here — and so would a claim expense left folded
    into ``expenses`` and then deducted twice.
    """
    return net_cf(t) - (premiums(t)
                        - claims(t, "LUMP") - claims(t, "ANNUITY")
                        - claims(t, "DEMENTIA") - claims(t, "LAPSE")
                        - expenses(t) - claim_expenses(t) - commissions(t))


def check_net_cf():
    """True when the cash flow statement re-adds to :func:`net_cf` in every month."""
    return all(abs(check_net_cf_resid(t)) <= 1e-6
               for t in range(proj_len()))


# --- result tables ---

def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``claims_annuity`` is a **living** benefit: the 介護年金 is paid while the insured
    survives in a certified care state at ``grade_annuity()``, and death stops it.  The
    name describes the benefit's form, a stream of instalments, and the same name carries
    a **death** benefit in ``IncomeTerm_JP_S``, so which contingency it is paid on is
    stated and not left to the name.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash
    flow on the same row, and ``pols_act`` is the part of it that is actually paying
    premium.  ``net_cf`` carries the notes' own income-positive sign.  ``claims_lapse``
    is a column of zeros by product design — there is no surrender value — and is
    published rather than dropped; see the Space docstring.  There is no ``claims_death``
    column, because the contract pays nothing on death.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_act": [pols_act(t) for t in ts],
            "care_w": [care_w(t) for t in ts],
            "care_l": [care_l(t) for t in ts],
            "care_n": [care_n(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_lump": [claims(t, "LUMP") for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_dementia": [claims(t, "DEMENTIA") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy month t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_act": [pols_act(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_term": [pols_term(t) for t in ts],
            "pols_entry_w": [pols_entry_w(t) for t in ts],
            "pols_entry_l": [pols_entry_l(t) for t in ts],
            "pols_entry_n": [pols_entry_n(t) for t in ts],
            "ann_count": [ann_count(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "inc_rate_l": [inc_rate_l(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 1.25

care_mort_mult = 2.75

sub65_age = 65

f_sub65 = 0.20

f_sub65_no_limb = 0.05

sel_lapse_ref = 0.20

dementia_share = 0.35

dementia_wait_mths = 6

expense_acq = 20000.0

expense_maint = 250.0

expense_claim = 5000.0

inflation_rate = 0.01

comm_init_rate = 1.5

comm_renewal_rate = 0.03

roll_fwd_tol = 1e-12

math = ("Module", "math")

pd = ("Module", "pandas")
