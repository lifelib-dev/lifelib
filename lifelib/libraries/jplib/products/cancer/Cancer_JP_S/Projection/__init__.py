# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Cancer_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the month beginning at the 契約日 and
``t = proj_len() - 1`` the last month of cover. Cover is whole of life, so
``proj_len() = 12 x (omega_age() - issue_age() + 1)`` — 924 months on the anchor cell.
There is no maturity benefit, no 満期保険金 and **no benefit-driven termination**: paying the
diagnosis lump sum neither ends nor exhausts the contract, and with no day limits the
inpatient benefit cannot exhaust it either. The decrements are death and lapse, and
nothing else.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/cancer/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Cancer_JP_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Cancer_JP_S.Data`, reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
incidence_table_file    data.incidence_table()              incidence_table.csv
sex_factor_file         data.sex_factor_table()             sex_factor_table.csv
survival_table_file     data.survival_table()               survival_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
hosp_stay_file          data.hosp_stay_table()              hosp_stay_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
annual rates and ``*_rate_mth`` for their monthly counterparts, ``claims(t, kind)`` with
an uppercase ``kind`` string. The technical notes use compact symbols instead. The
mapping is:

=========================  ==================================  ========================
Notes symbol               Cells                               Meaning
=========================  ==================================  ========================
(model point row)          model_point()                       The selected model point
t                          (the cells argument)                Policy month, 0-based
x                          issue_age()                         契約年齢 (満年齢) at issue
age(t)                     age(t)                              Attained age x + t//12
y(t)                       policy_year(t)                      Policy year, 1-based
(terminal age)             omega_age()                         116 male / 118 female
(horizon)                  proj_len()                          Months projected
W                          wait_months()                       Waiting period in months
cover(t)                   cover(t)                            1 from t >= W, else 0
A                          base_amount()                       基本給付金額
DB                         diag_benefit()                      がん診断一時金, 100 x A
u                          insitu_pct()                        上皮内新生物 grading of DB
D                          daily_amount()                      がん入院給付金日額
m_s                        surg_mult()                         Surgery multiple of A
B_tr                       treat_benefit()                     がん治療給付金 per month
K                          treat_cap()                         Lifetime cap in months
(outpatient rate)          outp_daily()                        がん通院給付金日額
C                          cycle_months()                      Repeat cycle in months
(payment period)           prem_period_type()                  終身払 or 65歳払済
P                          premium_mth_pp()                    Monthly office premium
(band rate)                inc_rate_both(t)                    罹患率 of the age band
f_male(a)                  sex_factor(a)                       Male / both-sexes factor
inc_rate(age, sex)         inc_rate(t)                         Annual first-diagnosis rate
i(t)                       inc_rate_mth(t)                     Monthly incidence
iz(t)                      insitu_rate_mth(t)                  Monthly 上皮内新生物 incidence
(table rate)               mort_rate_at_age(a)                 第三分野2018 proxy at age a
mort_rate(age)             mort_rate(t)                        Annual best-estimate q
q(t)                       mort_rate_mth(t)                    Monthly q, never diagnosed
S5                         surv_5y()                           5年相対生存率
mu_ex                      mu_ex()                             Annual excess hazard
q_c(t)                     mort_rate_canc_mth(t)               Monthly q, diagnosed
(table)                    lapse_rate(t)                       Annual lapse rate
w(t)                       lapse_rate_mth(t)                   Monthly lapse, healthy
w_c(t)                     lapse_rate_canc_mth(t)              Monthly lapse, diagnosed
w_cum(t)                   lapse_cum(t)                        Cumulative lapse share
lam                        sel_lapse_lambda                    Anti-selective loading
r                          relapse_rate_mth(t)                 Monthly relapse hazard
sc(t)                      surv_canc(t)                        Diagnosed survival factor
(void rule)                void_prob()                         In-window voidness
(initial exposure)         pols_if_init()                         In force at t = 0
pols_healthy(t)            pols_healthy(t)                     Never diagnosed
pols_locked(t)             pols_locked(t)                      Diagnosed, cycle running
pols_open(t)               pols_open(t)                        Diagnosed, cycle expired
pols_cancer(t)             pols_cancer(t)                      locked + open
pols_if(t)                 pols_if(t)                          healthy + cancer
(intra-month timing)       pols_if_at(t, timing)               In force at a named point
diag_first(t)              diag_first(t)                       First diagnoses
diag_rep(t)                diag_rep(t)                          Repeat triggers
trig(t)                    trig(t)                             All payment triggers
unlock(t)                  unlock(t)                           Cycle expiries arriving
insitu_ev(t)               insitu_ev(t)                        上皮内新生物 diagnoses
Z(t)                       insitu_avail(t)                     Once-only tier unused
(consumed)                 insitu_used(t)                      Once-only tier consumed
(decrement)                pols_death(t)                       Deaths, both states
(decrement)                pols_lapse(t)                       Lapses, both states
h                          hosp_rate_mth(t)                    Monthly admissions
L                          hosp_stay_days(t)                   Mean stay in days
s_h, s_z                   surg_per_hosp, surg_per_insitu      Surgeries per event
p_tr                       treat_prob                          Qualifying-month chance
M(t)                       treat_months(t)                     Treatment-month ledger
(capped draw)              paid_months(t)                      Months paid in month t
o                          outp_days                           Outpatient days per year
f_a                        adv_freq_mth()                      Monthly 先進医療 frequency
S_a                        adv_sev                             Mean 技術料
LV                         adv_cap                             先進医療 lifetime cap
V(t)                       adv_paid(t)                         先進医療 ledger
pay(t)                     adv_pay(t)                          先進医療 draw in month t
P x pols_healthy           premiums(t)                         Premium income
(claim lines)              claims(t, kind)                     Benefit outgo by kind
e(t)                       maint_expenses(t)                   Maintenance expense
ec_d, ec_h                 claim_expenses(t)                   Claim handling expense
E0, e(t)                   expenses(t)                         Acquisition + maintenance
(commission)               commissions(t)                      Commission outgo
net_cf(t)                  net_cf(t)                           Net cash flow, income +
=========================  ==================================  ========================

Five names needed care.

``pols_if_at(t, timing)`` carries the library-wide ``"BEF_DECR"`` / ``"BEF_LAPSE"`` /
``"AFT_DECR"`` vocabulary, and ``"BEF_LAPSE"`` is the sum over the **two states**, each
decremented on its own mortality basis — a blended rate on ``pols_if`` does not
reproduce it. What the vocabulary cannot show here is the movement that defines the
product: the three timings are *decrement* timings, and a first diagnosis is not a
decrement. :func:`diag_first` moves a life from :func:`pols_healthy` to
:func:`pols_cancer` before the decrement, changing which benefits and which premium the
life carries while leaving ``pols_if`` identical at all three points. Read
:func:`pols_healthy`, :func:`pols_cancer` and :func:`diag_first` for the state movement;
``pols_if_at`` answers only how many lives are left, never which state they are in.

``pols_open`` is the population **eligible for a repeat payment**, not the population in
payment. The two-year cycle is a *clock keyed to an event* — the previous payment trigger
— so the flow out of ``pols_locked`` is a **24-month delay**, not a rate:
:func:`unlock` is the trigger cohort of month ``t - C`` carried forward on diagnosed
decrements alone. This clock is emphatically **not** the 180-day one-hospitalization
memory of the medical chassis: different length, different trigger, different
consequence, and sharing one clock between the two products breaks both.

``insitu_ev`` is a *second benefit tier*, not a discount on the first. It attaches to
:func:`pols_healthy` alone, carries its own once-only ledger :func:`insitu_avail`, does
not move the life into the diagnosed state, does not start the two-year cycle and does
not trigger the premium waiver. Implementing it as ``insitu_pct x claims_diag`` inside
the main diagnosis benefit gets the amount right and the cap, the cycle and the waiver
all wrong.

``treat_months`` and ``adv_paid`` are ledgers **per diagnosed life**, not per block. They
measure what an individual has consumed against the 60-month and ¥20,000,000 caps, so
they are carried as a cohort average diluted by new entrants — and only by
:func:`diag_first`, because a repeat trigger is an already-diagnosed life whose ledgers
continue. Weighting them by ``pols_cancer`` would measure the block's consumption and
defer the cap forever; diluting them with :func:`diag_rep` would reset a ledger that
should keep running.

``claims(t, "LAPSE")`` exists and returns zero. There is no surrender value at any
duration under 終身払, so a lapse is a pure decrement that pays nothing; a column of zeros
states the product fact where a missing column would only hide it. There is no
``claims_death`` at all, because the composite carries no death benefit — mortality is a
pure liability-releasing decrement.

.. rubric:: Three states, and why two will not do

The medical chassis projects one in-force population and reads a hospitalisation
incidence off it. Here the diagnosis benefit repeats on a two-year cycle, the inpatient
benefit has no day limit and the treatment benefit pays by the month, so all three run on
**how long the insured lives after diagnosis**. The model therefore carries
:func:`pols_healthy`, :func:`pols_locked` and :func:`pols_open`, and needs a survival
basis as well as an incidence basis. The single roll-forward that ties them together is

    pols_cancer(t+1) = ( pols_cancer(t) + diag_first(t) ) x sc(t)

which :func:`check_cancer_roll_fwd` asserts against the separate ``locked`` / ``open``
recursions in every projected month.

.. rubric:: The waiting period is a hard zero

:func:`cover` multiplies **every** cancer benefit, the incidence transition and the
in-situ transition. In months 0, 1 and 2 the model pays nothing, transitions nobody, and
collects the premium. It is a hard zero, not a reduced rate: a model that starts the
incidence at ``t = 0`` pays three months of benefit that no contract in the retrieved set
pays, and one that suppresses the premium along with the benefit is a different product.

.. rubric:: Premiums ride on pols_healthy, claims on pols_cancer

The waiver fires on the same first invasive diagnosis that starts every benefit, so the
premium stream is carried by the never-diagnosed sub-population alone and the two weights
are disjoint. Multiplying the premium by ``pols_if`` is the single largest arithmetic
error available in this product, and it is invisible in the first three months because
the two are equal. :func:`pols_payer` is where the choice is made, and it is a *product*
choice: on the ``waiver_trigger = "none"`` and ``"disability"`` designs the diagnosed keep
paying and can lapse, which is why :func:`lapse_rate_canc_mth` is not simply zero.

.. rubric:: Dimensions

``D x hosp_stay_days`` is JPY per admission, so the inpatient benefit is
``D x L x h x pols_cancer``. ``B_tr`` is JPY per **month**, so the treatment benefit is
``B_tr x p_tr x pols_cancer`` directly — **no day count enters it at all**, and inserting
one is the commonest way to break this product. The medical chassis's benefit is
``日額 x days`` and this product's central benefit is ``月額 x months``; the two have
different dimensions and cannot share a formula.

.. rubric:: Modules that are off in the base run

Eight of the notes' optional constructions are implemented and held at an inert base
value, so that the base run reproduces the worked example while the machinery stays
visible and testable:

- **The validity adjustment**, ``void_adjust``. A diagnosis inside the 90-day window makes
  the contract **void**, not lapsed: the policy was never in force, so the premium already
  collected comes back with the future benefit. :func:`void_prob` is that probability —
  0.037% of policies at the anchor cell — and switching ``void_adjust`` on scales
  :func:`pols_if_init` down by it, which releases premium and benefit together at outset.
  The acquisition expense and initial commission are *not* scaled: they were incurred.
- **Anti-selective lapse**, ``inc_eff = inc_rate (1 + lam max(0, w_cum - w_ref))``, with
  ``sel_lapse_lambda = 0``. Healthy lives lapse first, so the persisting never-diagnosed
  block is progressively impaired on the *incidence* basis. On this product the effect is
  amplified by the waiver: the healthiest lives are also the only ones still paying. No
  Japanese evidence was retrieved.
- **Conditioned repeats**, the ``repeat_conditioned`` model-point flag. Two of the three
  sourced two-year designs require the insured to be under treatment for the second and
  later payments; the flag multiplies the relapse hazard by ``treat_prob``, so the two
  designs differ by an order of magnitude, not by a rounding. False on the anchor cell,
  true on model point 3.
- **The age gradient on the mean stay**, ``hosp_age_gradient``. The 14.4-day all-ages
  figure and the 35-64 / 65+ / 75+ gradient are both sourced, but the gradient is
  published on four broad bands and the incidence on twenty-one narrow ones, so the base
  run takes the all-ages figure.
- **The 保険年齢 age offset**, ``mort_age_offset``. 第三分野標準生命表2018 is constructed for use on a
  nearest-birthday basis, so reading it at 満年齢 understates the valuation age by about half
  a year. Set the offset to 0.5 to read at ``age(t) + 0.5``, interpolating between rows.
- **A cancer-free mortality baseline**, ``net_of_cancer``. The never-diagnosed carry a
  population table that already contains cancer deaths and the diagnosed carry them again
  as an excess hazard. At the anchor age the double count is 1% of the excess hazard; at
  80 it is not. ``cancer_death_share = 0.28`` is a **[std]** placeholder with no observed
  range — no document in this product's source set gives 悪性新生物's share of all-cause
  Japanese mortality — so the switch demonstrates the capability rather than a calibration.
- **Repricing at renewal**, ``renew_reprice_rate``, on the 10年更新 定期 chassis flag. The
  renewal reprices at then-current rates, which would ordinarily close the contract
  boundary at each renewal; the base run holds the issue rate flat and records the tension
  rather than resolving it. Model point 3 carries the flag with the rate at zero.
- **The diagnosed lapse loading**, ``lapse_canc_factor = 1.0``. It scales the diagnosed
  lapse rate off the healthy one, and its base value is inert rather than off: wherever
  the waiver fires a diagnosed life has no premium to miss and no surrender value to take,
  so :func:`lapse_rate_canc_mth` returns zero whatever the factor is. It reaches a cash
  flow only on the ``waiver_trigger = "none"`` and ``"disability"`` designs — model point
  7.

Two further constructions the notes name are deliberately **not** implemented, and the
absence is stated rather than left to inference. A duration-banded excess hazard needs
cohort tracking by time since diagnosis that the three-state model does not carry, and
the grace-period lag and 復活 are modelled as a new model point rather than as a negative
lapse, because the 90-day waiting period **re-runs from the 復活日**.

.. rubric:: One divergence from the technical notes

The notes carry ``disch_rider`` as a model point attribute but their cash-flow section
does not define the がん退院一時金 benefit, so :func:`claims` ``(t, "DISCHARGE")`` supplies a
**[std]** formula built from ``product-spec.md`` instead: ``disch_mult x A`` per
qualifying discharge, on the ``disch_qual_share`` of admissions whose stay reaches the
contractual ten days. The 30-day re-payment bar is not modelled — at 0.0208 admissions
per diagnosed life-month the overlap is second-order. The rider is off on every model
point but 8, so the base run and the worked example are untouched by it; see
``model.md``.

.. rubric:: Sign convention

The notes' ``net_cf(t)`` is already **income positive** — premiums less claims, expenses
and commission — which is the library-wide sign of :func:`net_cf`, so there is no
outgo-positive ``liability_cf`` companion to publish: one stream, one sign, one name.

.. rubric:: What the shape of the answer is

Year-1 claims are 3.47% of year-1 premium at the anchor cell, against 21.5% on the medical
chassis at the same age and expense scale, and the gap is the product rather than an
error: the first quarter pays nothing, the diagnosed population starts empty and is still
0.11% of the in-force after twelve months, and cancer incidence at 40 is a factor of 32
below the medical chassis's hospitalisation incidence. This is a product whose cost is
almost entirely in front of it — the sourced incidence curve rises by a factor of 11.3
from the 40-44 band to the 85-89 band — so a ten-year projection sees almost none of the
liability the contract actually carries.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# ===== Cells: the model point =====


def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point."""
    return str(model_point()["policy_id"])


def chassis():
    """The cover chassis: ``shushin`` (終身) or ``teiki`` (10年更新 定期).

    終身 is the composite because four of the seven retrieved carriers write it, against a
    ten-year renewable term at two and a five-year one at the expense carrier.  The 定期
    flag carries automatic renewal with benefit history, waiver history and 責任開始期
    continuous across the renewal, so the projection horizon is unchanged; what the
    renewal really does is reprice, and that is the ``renew_reprice_rate`` switch.
    """
    v = model_point()["chassis"]
    if v not in ("shushin", "teiki"):
        raise ValueError("invalid chassis")
    return v


def issue_age():
    """x: the 契約年齢 at issue, on a 満年齢 basis, in the composite's 20-75 range.

    満年齢 is the attained age at the 契約日 with the fraction discarded, incremented at each
    年単位の契約応当日.  第三分野標準生命表2018 is constructed for use on a 保険年齢方式
    (nearest-birthday) basis, so reading it at 満年齢 understates the valuation age by about
    half a year; the base run accepts the offset **[std]** and ``mort_age_offset`` is the
    switch that removes it.
    """
    v = int(model_point()["issue_age"])
    if not 20 <= v <= 75:
        raise ValueError("issue_age outside the composite's 20-75 range")
    return v


def sex():
    """The sex (M / F) of the insured.

    A unisex basis would be materially wrong at every age on this product, because the
    male and female incidence curves cross: female incidence is nearly three times male at
    35-39 and half of it at 70-74.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def base_amount():
    """A: the 基本給付金額, the amount every benefit in the composite is a multiple of.

    The only published course menu is ¥5,000 and ¥10,000; ¥10,000 is the composite default
    because it is the amount at which the published multiples and the published ¥1,000,000
    headline diagnosis benefit are mutually consistent.
    """
    return float(model_point()["base_amount"])


def diag_benefit():
    """DB: the がん診断一時金, 100 x A = ¥1,000,000 on the anchor cell.

    Payable on the first diagnosis of an 悪性新生物 on or after the がん責任開始日 and again on each
    fresh 再発 / 転移 / 新生 once the cycle has expired, with **no lifetime cap** and no
    termination on payment.
    """
    return float(model_point()["diag_benefit"])


def cycle_months():
    """C: the repeat cycle in months, measured from the **previous payment trigger**.

    At most one diagnosis payment in any two years.  The three sourced two-year designs
    measure the clock from the trigger date, from the first day of the calendar month of
    the previous payment, and from the start date of the last hospitalisation; only the
    first needs no second date carried alongside, and it is the one modelled.
    """
    return int(model_point()["cycle_months"])


def insitu_pct():
    """u: the 上皮内新生物 grading of the diagnosis benefit, in {1.00, 0.50, 0.10}.

    The three sourced treatments of in-situ disease — full rate, half rate and 10% — are a
    single model-point parameter.  Whatever the grading, the benefit is payable **once**,
    on its own cap, is not payable after a full-rate benefit, and does not trigger the
    premium waiver.
    """
    return float(model_point()["insitu_pct"])


def daily_amount():
    """D: the がん入院給付金日額, equal to A in the composite.

    Paid per day of a cancer hospitalisation with **no per-hospitalization day limit and
    no 通算 lifetime limit** — the structural difference from the medical chassis, whose 60
    or 120-day and 1,095-day ledgers dominate its model.
    """
    return float(model_point()["daily_amount"])


def surg_mult():
    """m_s: the がん手術給付金 as a multiple of A, 20 on the composite.

    Unlimited count; simultaneous procedures count as one.  Payable in full on 上皮内新生物 as
    well, which is why :func:`claims` ``(t, "SURGERY")`` has two limbs.
    """
    return float(model_point()["surg_mult"])


def treat_benefit():
    """B_tr: the がん治療給付金 per qualifying **calendar month**, 10 x A on the composite.

    An indicator per month, not a count and not a duration: a prescription covering two
    months pays one month, and two triggers in one month pay once.  Any formula in which a
    day count reaches this benefit is wrong by construction.
    """
    return float(model_point()["treat_benefit"])


def treat_cap():
    """K: the lifetime cap on the monthly treatment benefit, in months.

    60 at the two carriers that write the benefit.  At ``treat_prob`` and the diagnosed
    state duration implied by the survival basis, a life diagnosed at the anchor age
    accumulates an expected 12.98 qualifying months against it, so the cap binds for a
    long-course minority — which is what a 60-month cap is for, and why
    :func:`treat_months` cannot be dropped as immaterial.
    """
    return int(model_point()["treat_cap"])


def outp_daily():
    """The がん通院給付金日額, equal to A in the composite.

    Treatment-linked — attendance *for* surgery, radiation, thermal therapy or non-oral
    chemotherapy, not attendance for follow-up — and with no day limit.  Not payable for a
    day of attendance during a stay for which the inpatient benefit is paid.
    """
    return float(model_point()["outp_daily"])


def wait_months():
    """W: the 90-day waiting period expressed on the monthly grid, 3 months.

    がん責任開始日 is the 91st day counting the 責任開始日 as day 1 at five carriers; two write three
    calendar months instead.  On a monthly grid these are the same boundary **[std]** and
    the model does not claim a precision it does not have.
    """
    return int(model_point()["wait_months"])


def prem_period_type():
    """The premium-paying period **as a category**: ``whole_life`` (終身払) or ``to_65``.

    Named ``prem_period_type`` and not ``prem_period`` because the library reserves
    ``prem_period`` for a **duration in the model's own grid unit**; this returns one of
    two labels.  The model point column keeps the name ``prem_period``.

    終身払 is the composite default and is the design under which **no surrender value ever
    arises** on any retrieved contract; the 短期払 variant is the only route by which this
    chassis acquires a surrender value at all, which the model does not carry either way.
    """
    v = model_point()["prem_period"]
    if v not in ("whole_life", "to_65"):
        raise ValueError("invalid prem_period")
    return v


def premium_mth_pp():
    """P: the level **monthly** office premium per policy **[std]**.

    ``premium_mth_pp`` and not ``premium_pp``: the library spells a monthly per-policy
    premium ``premium_mth_pp`` and an annual one ``premium_pp``, and this product's grid
    step is the payment interval, so the figure here is a month's premium.

    An input, not a computed quantity, and on this product that is a stronger statement
    than on any other in the library.  No carrier publishes a rate table for a cancer main
    contract, the 算出方法書 is a 基礎書類 filed with the 金融庁 and is not published, and for
    third-sector business there is additionally no standard incidence table and no
    reference pure premium to fall back on.  The single retrieved price point is a
    ten-year term at twice the composite's benefit amounts on a 2013 calculation basis;
    the anchor's ¥3,000 is a round modelling figure in that neighbourhood and no result in
    this library depends on its being a market rate.
    """
    return float(model_point()["premium"])


def prem_mode():
    """The premium frequency; 月払 (monthly) throughout the composite.

    Carried because the product documentation distinguishes 月払 / 半年払 / 年払, and inert on
    a monthly grid whose step *is* the payment interval.  It is also why the 90-day waiting
    period lands exactly on a grid boundary.
    """
    return model_point()["prem_mode"]


def waiver_trigger():
    """The 保険料払込免除 trigger: ``cancer_diag``, ``disability`` or ``none``.

    ``cancer_diag`` is the composite: the waiver fires on the first 悪性新生物 diagnosis on or
    after the がん責任開始日, and 上皮内新生物 does not trigger it.  The consequence runs through the
    whole model — premiums ride on :func:`pols_healthy`, and a diagnosed life has no
    premium to miss and no surrender value to take, so it cannot lapse.  On the other two
    designs both of those reverse; see :func:`pols_payer` and
    :func:`lapse_rate_canc_mth`.  The disability incidence itself is out of scope
    **[std scope]**: no basis for it appears in this product's source set.
    """
    v = model_point()["waiver_trigger"]
    if v not in ("cancer_diag", "disability", "none"):
        raise ValueError("invalid waiver_trigger")
    return v


def adv_rider():
    """Whether the がん先進医療特約 is attached.

    A reimbursement of the 技術料 in full against a ¥20,000,000 lifetime cap, with a 10% cash
    top-up capped at ¥500,000 per 療養; the rider terminates when the cap is reached, which
    :func:`adv_pay` implements as a draw against :func:`adv_paid`.
    """
    return bool(model_point()["adv_rider"])


def disch_rider():
    """Whether the がん退院一時金 rider is attached; false on the base run's anchor cell.

    ¥100,000 on discharge from a covered stay of ten or more consecutive days.  The
    technical notes carry the flag but not a formula for it, so the benefit is a **[std]**
    construction here; see the Space docstring and ``model.md``.
    """
    return bool(model_point()["disch_rider"])


def repeat_conditioned():
    """Whether second and later diagnosis payments require the insured to be in treatment.

    False in the composite, which does not condition the repeat.  Two of the three sourced
    two-year designs do condition it — on being under treatment at one carrier and
    hospitalised at another — and the switch multiplies the relapse hazard by
    ``treat_prob``, so the two designs differ by an order of magnitude.
    """
    return bool(model_point()["repeat_conditioned"])


# ===== Cells: the projection frame =====


def omega_age():
    """The terminal age of 第三分野標準生命表2018: 116 male, 118 female.

    The horizon of a whole-of-life projection, and the last age the shipped table carries:
    both terminal rates are sourced ``q = 1.00000`` rows quoted from that table, so the
    projection ends where the published table ends rather than where a fitted curve
    happens to close.
    """
    return omega_age_male if sex() == "M" else omega_age_female      # noqa: F821


def proj_len():
    """The projection length in policy months: ``12 x (omega_age - x + 1)``.

    924 months on the anchor cell.  Cover is whole of life with no maturity benefit and no
    benefit-driven termination, so the horizon is the mortality table's and nothing
    shortens it — including the 定期 chassis flag, whose renewal is automatic.
    """
    return 12 * (omega_age() - issue_age() + 1)


def age(t):
    """age(t): the attained 満年齢 in policy month t, ``x + t // 12``."""
    return issue_age() + t // 12


def policy_year(t):
    """y(t): the policy year containing month t, ``t // 12 + 1``."""
    return t // 12 + 1


def cover(t):
    """cover(t): 1 from the がん責任開始日, 0 inside the 90-day waiting period.

    A **hard zero**, not a reduced rate.  It multiplies every cancer benefit, the incidence
    transition and the in-situ transition, so in months 0, 1 and 2 the model pays nothing
    and transitions nobody — while still collecting the premium, because five of the six
    carriers that state it charge from inception.
    """
    return 1.0 if t >= wait_months() else 0.0


# ===== Cells: decrement and incidence bases =====


def mort_rate_at_age(a):
    """The shipped **[std]** mortality table rate at age ``a``, which may be fractional.

    A construction **graduated between the individual 第三分野標準生命表2018 rates the library
    quotes and attributes** — 男 q(40) = 0.00076 among them — and **not** a copy of that
    table; see the :mod:`~.Cancer_JP_S.Data` docstring.  Every quoted rate is reproduced
    exactly at its own age; the ages between them are log-linear interpolations.  A
    fractional age is linearly interpolated between the two bracketing rows, which is what
    ``mort_age_offset`` needs.
    """
    tbl = data.mort_table()                                          # noqa: F821
    top = int(tbl.loc[sex()].index.max())
    lo = min(int(a), top)
    q0 = float(tbl.loc[(sex(), lo), "mort_rate"])
    frac = a - lo
    if frac <= 0.0 or lo >= top:
        return q0
    q1 = float(tbl.loc[(sex(), lo + 1), "mort_rate"])
    return q0 + frac * (q1 - q0)


def mort_rate(t):
    """The annual best-estimate mortality of a never-diagnosed life in month t.

    ``mort_be_factor x q_third_sector(age(t), sex)``, capped at 1.  第三分野標準生命表2018 is a
    **valuation** table whose margin runs the wrong way for a best estimate on a morbidity
    product: death releases the liability, so the table sits deliberately below national
    mortality, with a risk-theory adjustment bounded at 70% below and 85% above the
    unadjusted rate.  ``mort_be_factor = 1.25`` **[std]** is the reciprocal of 0.80, a
    round value inside that sourced band, so the factor unwinds the table's stated margin
    and nothing more.  The same factor must be used here and on the medical chassis.  The
    cap binds at the terminal age alone, where the shipped table already carries the
    sourced ``q = 1.00000``.

    With ``net_of_cancer`` on, the rate is additionally netted of the **[std]** cancer share
    of deaths, so that the cancer mortality inside the table's own rates is not carried
    twice once the diagnosed excess hazard is added.
    """
    q = min(1.0, mort_be_factor * mort_rate_at_age(age(t) + mort_age_offset))   # noqa: F821
    if net_of_cancer:                                                # noqa: F821
        q = q * (1.0 - cancer_death_share)                           # noqa: F821
    return q


def mort_rate_mth(t):
    """q(t): the monthly mortality of a never-diagnosed life, ``1 - (1 - q_ann)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def surv_5y():
    """S5: the 5年相対生存率 of the insured's sex, all sites, 2018 diagnoses.

    63.17% male and 66.84% female.  **Relative** survival, which already nets out
    background mortality — multiplying survivorship by it would double-count the
    background; it converts instead into an excess hazard, which is what :func:`mu_ex`
    does.
    """
    return float(data.survival_table().loc[sex(), "surv_5y"])        # noqa: F821


def mu_ex():
    """mu_ex: the annual excess hazard of a diagnosed life, ``-ln(S5) / 5`` **[std]**.

    0.0918681 per year for a male.  Held **flat for the whole diagnosed lifetime**
    **[std]**, which overstates late-duration mortality — real relative-survival curves
    flatten as the cured fraction emerges — and therefore *understates* the repeating
    diagnosis benefit and the unlimited inpatient benefit, which are precisely the
    long-survivor benefits.  A duration-banded hazard would need cohort tracking by time
    since diagnosis that this three-state model does not carry, and it moves the liability
    in one direction only: up.
    """
    return -math.log(surv_5y()) / 5.0                                # noqa: F821


def mort_rate_canc_mth(t):
    """q_c(t): the monthly mortality of a diagnosed life.

    ``1 - (1 - q(t)) exp(-mu_ex / 12)`` — the baseline **plus** an excess hazard, not a
    replacement for it.  0.0077050451 at the anchor cell's first year, which implies a mean
    diagnosed-state duration of 129.79 months and is what every one of the five care
    benefits is integrated over.
    """
    return 1.0 - (1.0 - mort_rate_mth(t)) * math.exp(-mu_ex() / 12.0)   # noqa: F821


def lapse_rate(t):
    """The annual lapse rate applying in policy year ``y(t)`` **[std]**.

    9 / 7 / 6 / 5.5 / 5 percent then a 4.5% plateau and a 3% ultimate, shared unchanged
    with the medical chassis so that the two third-sector products do not disagree about
    persistency.  The only published industry-wide figure is a 5.6% 解約・失効率 measured on
    opening in-force **sum assured**, on a book dominated by death cover, which a がん保険
    with no sum assured cannot enter; the shipped curve averages 5.5% over its first ten
    years against it.  Policy years beyond the table take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())), "lapse_rate"])


def lapse_rate_mth(t):
    """w(t): the monthly lapse rate of a never-diagnosed life **[std]**.

    ``1 - (1 - lapse_rate)^(1/12)``, applied after mortality at the end of the month.  A
    lapse pays nothing: the composite is 無解約払戻金型 at every duration under 終身払, and with
    no surrender value neither 契約者貸付 nor 自動振替貸付 can operate, so a missed premium really
    does lapse the policy.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_rate_canc_mth(t):
    """w_c(t): the monthly lapse rate of a **diagnosed** life; zero in the base run.

    A product fact, not a refinement.  The waiver fires on the first 悪性新生物 diagnosis, so a
    diagnosed life has no premium to miss, and there is no surrender value to cash in — so
    there is no mechanism by which a diagnosed policy leaves the book other than death.
    Applying the healthy lapse rate to the diagnosed state deletes exactly the claimants
    the product exists to pay.  On the disability-trigger and no-waiver designs the premium
    does not stop, and the rate becomes the healthy one scaled by ``lapse_canc_factor``.
    """
    if waiver_trigger() == "cancer_diag":
        return 0.0
    return lapse_rate_mth(t) * lapse_canc_factor                     # noqa: F821


def lapse_cum(t):
    """w_cum(t): the cumulative lapse proportion of the never-diagnosed cohort before t.

    A proportion of :func:`pols_if_init`, not a running total of :func:`lapse_rate_mth`, and
    it drives a loading on **incidence** rather than on lapse.  Zero at ``t = 0``.
    """
    if t <= 0:
        return 0.0
    lapsed = (pols_healthy(t - 1) - diag_first(t - 1)) * (
        1.0 - mort_rate_mth(t - 1)) * lapse_rate_mth(t - 1)
    return lapse_cum(t - 1) + lapsed / pols_if_init()


def sel_lapse_factor(t):
    """The anti-selective lapse loading on incidence in month t **[std]**; 1 in the base run.

    ``1 + lam max(0, w_cum(t) - w_ref)``.  Healthy lives lapse first, so the persisting
    never-diagnosed block is progressively impaired on the incidence basis.  Off in the
    base run (``sel_lapse_lambda = 0``); no Japanese evidence for the loading was
    retrieved.
    """
    return 1.0 + sel_lapse_lambda * max(                             # noqa: F821
        0.0, lapse_cum(t) - sel_lapse_ref)                           # noqa: F821


def inc_band_at_age(a):
    """The five-year 全国がん登録 age band containing age ``a``, as its starting age.

    The registry publishes by five-year band, so the incidence **steps** and does not
    glide.  Interpolating within a band is a choice, not a correction, and it would have to
    be the same choice in the model and in the CSV's ``provenance`` column.  The last row
    is the 100+ open band.
    """
    tbl = data.incidence_table()                                     # noqa: F821
    b = 5 * (int(a) // 5)
    return min(max(b, int(tbl.index.min())), int(tbl.index.max()))


def inc_rate_both(t):
    """The both-sexes 罹患率 of the age band containing ``age(t)``, per policy per year.

    All sites C00-C96, crude rate, 2023 diagnoses, converted from the published per-100,000
    figure.  220.28 per 100,000 at the anchor cell's 40-44 band.  This is the one
    assumption in the model that is genuinely sourced.
    """
    tbl = data.incidence_table()                                     # noqa: F821
    return float(tbl.loc[inc_band_at_age(age(t)), "rate_per_100k"]) / 100000.0


def sex_factor(a):
    """f_male(a): the male / both-sexes incidence factor at age ``a`` **[std]**.

    Linear in age between the two sourced ratios, 0.551547 at the 35-39 band midpoint 37.5
    and 1.377629 at the 70-74 band midpoint 72.5, and read at the **band midpoint** — so
    ``f_male(42.5) = 0.669559`` serves the whole 40-44 band.  The female limb is
    ``2 - f_male``, which is what makes the construction sum to twice the both-sexes rate.

    The factor is clamped to ``[0, 2]`` **[std]**, because outside that interval one limb
    of the construction goes negative and a negative incidence is not a rate.  The clamp
    binds only on the 100+ band: the linear form reaches 2 at age 98.87, so at the 102.5
    midpoint it would give a female rate of -0.086 x the band rate.

    Two properties of the construction are validation targets rather than claims.
    ``f_male = 1`` at age 56.5, against a sourced crossover somewhere between about 25 and
    about 55.  And the female limb does not reproduce the sourced female rates exactly —
    -1.2% at 35-39 and -6.1% at 70-74 — because the band rate is a population-weighted
    average rather than the arithmetic mean the ``2 - f_male`` form assumes.  The error is
    small at the anchor age and material in the tail, and it disappears the moment the
    by-sex grid from the same workbook replaces the construction.
    """
    tbl = data.sex_factor_table()                                    # noqa: F821
    a0, a1 = float(tbl.index.min()), float(tbl.index.max())
    f0 = float(tbl.loc[a0, "f_male"])
    f1 = float(tbl.loc[a1, "f_male"])
    return min(2.0, max(0.0, f0 + (f1 - f0) * (a - a0) / (a1 - a0)))


def inc_rate(t):
    """The annual first-diagnosis incidence per never-diagnosed policy in month t.

    The band rate times the sex limb, times the anti-selective lapse loading.
    0.00147490 per year on the anchor cell.  For third-sector business the regulator states
    flatly that no standard incidence table and no reference pure premium exist and that
    insurers must build the rate for each 支払事由 from public data and their own experience —
    and for cancer the public data is excellent, which is why only the sex split here is
    **[std]**.
    """
    both = inc_rate_both(t)
    f = sex_factor(inc_band_at_age(age(t)) + 2.5)
    limb = f if sex() == "M" else 2.0 - f
    return both * limb * sel_lapse_factor(t)


def inc_rate_mth(t):
    """i(t): the monthly first-diagnosis incidence, ``inc_rate(t) / 12`` **[std]**.

    Uniform within the band year; 0.000122909 per month on the anchor cell.
    """
    return inc_rate(t) / 12.0


def insitu_rate(t):
    """The annual 上皮内新生物 incidence per never-diagnosed policy.

    ``insitu_share x inc_rate(t)``.  The registry publishes paired rows with and without
    上皮内がん — 993,469 invasive against 1,114,642 including in situ — an increment of 121,173
    cases, 12.2% of the invasive count.  The 12.2% is sourced; its **age-invariance** is
    **[std]** and is very likely wrong in a knowable direction, since in-situ detection is
    screening-driven and concentrated at the screened ages.
    """
    return insitu_share * inc_rate(t)                                # noqa: F821


def insitu_rate_mth(t):
    """iz(t): the monthly 上皮内新生物 incidence, 0.0000149949 on the anchor cell."""
    return insitu_rate(t) / 12.0


def relapse_rate_mth(t):
    """r: the monthly relapse hazard once the cycle is open **[std]**.

    ``rel_rate / 12`` = 0.005, with the deeming rule — a continuing hospitalisation at cycle
    expiry is a fresh trigger — folded into it.  The largest single **[std]** lever in the
    product, and there is no public source for it and no observed range.  The calibration
    target is stated so it can be argued with: at the anchor cell's decrement rates held
    flat a diagnosed life survives the 24-month lock with probability 0.830575, then wins
    the race between relapse and exit with probability 0.393544, giving 0.326868 per cycle
    and an expected 1.485593 diagnosis payments per diagnosed life.

    With ``repeat_conditioned`` the hazard is multiplied by ``treat_prob``, the conditional
    probability of being in treatment on the **[std]** basis.
    """
    r = rel_rate / 12.0                                              # noqa: F821
    return r * treat_prob if repeat_conditioned() else r             # noqa: F821


# ===== Cells: the three states =====


def void_prob():
    """The probability of a diagnosis inside the 90-day window; zero in the base run.

    ``1 - (1 - i(0))^W`` = 0.000368681 at the anchor cell, 0.037% of policies.  A diagnosis
    inside the window makes the contract **void**, not merely unpayable — a
    de-recognition, not a decrement: the policy was never in force, so it releases the
    premium already collected as well as the future benefit, and it belongs in a validity
    adjustment at outset rather than in the lapse column.  ``void_adjust`` is off in the
    base run and the omission is quantified here rather than waved at.
    """
    if not void_adjust:                                              # noqa: F821
        return 0.0
    return 1.0 - (1.0 - inc_rate_mth(0)) ** wait_months()


def pols_if_init():
    """The exposure in force at ``t = 0``: one policy, less any validity adjustment.

    The acquisition expense and the initial commission are deliberately **not** scaled by
    it: they were incurred whether or not the contract turns out to have been void.
    """
    return 1.0 - void_prob()


def pols_healthy(t):
    """In force at the start of month t and **never diagnosed with an 悪性新生物**.

    ``(pols_healthy(t) - diag_first(t)) (1 - q(t)) (1 - w(t))``.  A life diagnosed in month
    t leaves this state before the decrement and takes the **diagnosed** mortality in its
    month of diagnosis **[std]**.  An in-situ diagnosis does *not* move the life out: it is
    a second benefit tier, not a state change.

    This is the population the premium rides on, and the population lapse applies to.
    """
    if t <= 0:
        return pols_if_init() if t == 0 else 0.0
    survivors = pols_healthy(t - 1) - diag_first(t - 1)
    return survivors * (1.0 - mort_rate_mth(t - 1)) * (1.0 - lapse_rate_mth(t - 1))


def surv_canc(t):
    """sc(t): the survival factor of a diagnosed life over month t.

    ``(1 - q_c(t)) (1 - w_c(t))``, and in the base run ``w_c = 0``, so it is pure
    mortality: a diagnosed policy leaves the book only by death.
    """
    return (1.0 - mort_rate_canc_mth(t)) * (1.0 - lapse_rate_canc_mth(t))


def unlock(t):
    """The trigger cohort whose two-year cycle expires at the start of month t.

    ``trig(t - C)`` carried forward on diagnosed decrements alone.  The cycle is a
    **delay**, not a rate, and the delay is implemented on the trigger history: a life
    triggered in month ``s`` enters ``locked``, survives C months of diagnosed decrements
    and arrives in ``open`` in month ``s + C``.  Zero before ``t = C``, and in fact zero
    before ``t = C + W`` because nothing can trigger inside the waiting period.
    """
    s = t - cycle_months()
    if s < 0:
        return 0.0
    cohort = trig(s)
    if cohort == 0.0:
        return 0.0
    factor = 1.0
    for v in range(s, t):
        factor = factor * surv_canc(v)
    return cohort * factor


def pols_locked(t):
    """In force, diagnosed, and **within C months of the last payment trigger**.

    ``(pols_locked(t) + trig(t)) sc(t) - unlock(t+1)``.  A life that has just been paid
    cannot be paid again for C months; this is where it waits.
    """
    if t <= 0:
        return 0.0
    return (pols_locked(t - 1) + trig(t - 1)) * surv_canc(t - 1) - unlock(t)


def pols_open(t):
    """In force, diagnosed, cycle expired, **eligible for a repeat payment**.

    ``(pols_open(t) - diag_rep(t)) sc(t) + unlock(t+1)``.  Eligible, not in payment: a
    fresh 再発 / 転移 / 新生 is what converts eligibility into a payment, at the relapse hazard,
    without limit and with no termination on payment.
    """
    if t <= 0:
        return 0.0
    return (pols_open(t - 1) - diag_rep(t - 1)) * surv_canc(t - 1) + unlock(t)


def pols_cancer(t):
    """The diagnosed in-force population, ``pols_locked(t) + pols_open(t)``.

    The weight on all five care benefits.  0.11% of the in-force after twelve months at the
    anchor cell, and drawing ¥16,035 a month per life while it lasts.
    """
    return pols_locked(t) + pols_open(t)


def pols_if(t):
    """The total in force at the **start** of month t, healthy plus diagnosed.

    The weight on the maintenance expense — a waived policy is still serviced — but *not*
    on the premium, which rides on :func:`pols_healthy` alone.
    """
    return pols_healthy(t) + pols_cancer(t)


def pols_if_at(t, timing):
    """The in-force count at a named point inside month t.

    The library-wide timing vocabulary, over the total book:

    ``"BEF_DECR"``
        the start-of-month count, :func:`pols_if` — the weight on the
        ``result_cf()`` row of the same ``t``.

    ``"BEF_LAPSE"``
        after mortality and before lapse, **summed over the two states**, each
        decremented on its own basis: the never-diagnosed survivors of
        :func:`mort_rate_mth` plus the diagnosed survivors of
        :func:`mort_rate_canc_mth`.  A single blended rate applied to
        :func:`pols_if` does not reproduce it.

    ``"AFT_DECR"``
        after both decrements, which is :func:`pols_if` of ``t + 1``.

    What the vocabulary **cannot** show on this model is the movement that defines
    the product.  The three timings are decrement timings, and the first diagnosis is
    not a decrement: :func:`diag_first` moves a life from :func:`pols_healthy` to
    :func:`pols_cancer` **before** the decrement, changing which benefits and which
    premium the life carries while leaving ``pols_if`` untouched at every one of the
    three points.  Read :func:`pols_healthy`, :func:`pols_cancer` and
    :func:`diag_first` — all three published as columns of :func:`result_cf` and
    :func:`result_pols` — for the state movement; ``pols_if_at`` answers only how many
    lives are left, never which state they are in.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return ((pols_healthy(t) - diag_first(t)) * (1.0 - mort_rate_mth(t))
                + (pols_cancer(t) + diag_first(t))
                * (1.0 - mort_rate_canc_mth(t)))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def diag_first(t):
    """First 悪性新生物 diagnoses in month t: ``pols_healthy(t) i(t) cover(t)``.

    The event that starts every benefit stream and simultaneously stops the premium, which
    is what makes premium and claims anti-correlated by construction on this product.
    """
    return pols_healthy(t) * inc_rate_mth(t) * cover(t)


def diag_rep(t):
    """Repeat diagnosis triggers in month t: ``pols_open(t) r cover(t)``.

    A fresh 再発, 転移 or new primary on a life whose two-year cycle has expired.  There is no
    lifetime cap on the count.
    """
    return pols_open(t) * relapse_rate_mth(t) * cover(t)


def trig(t):
    """All diagnosis payment triggers in month t, first and repeat.

    The quantity the two-year clock restarts from, which is why :func:`unlock` reads the
    trigger history rather than the first-diagnosis history.
    """
    return diag_first(t) + diag_rep(t)


def insitu_avail(t):
    """Z(t): the probability the once-only 上皮内新生物 benefit is still unused.

    ``Z(t+1) = Z(t) (1 - iz(t) cover(t))``, from ``Z(0) = 1``.  A separate ledger rather
    than a flag on the diagnosis benefit, because the tier has its own cap, does not start
    the two-year cycle and does not trigger the waiver.
    """
    if t <= 0:
        return 1.0 if t == 0 else 0.0
    return insitu_avail(t - 1) * (
        1.0 - insitu_rate_mth(t - 1) * cover(t - 1))


def insitu_used(t):
    """The once-only 上皮内新生物 tier consumed per never-diagnosed policy before month t.

    Accumulated straight off the published claim line, ``insitu_ev(s) / pols_healthy(s)``,
    with no reference to the :func:`insitu_avail` recursion.  It exists so that
    :func:`check_insitu_ledger` can assert that the benefit paid and the availability
    remaining still sum to one.
    """
    if t <= 0:
        return 0.0
    healthy = pols_healthy(t - 1)
    used = insitu_ev(t - 1) / healthy if healthy > 0.0 else 0.0
    return insitu_used(t - 1) + used


def insitu_ev(t):
    """上皮内新生物 diagnoses in month t: ``pols_healthy(t) Z(t) iz(t) cover(t)``.

    Attaches to the never-diagnosed alone, because the tier is not payable once a full-rate
    benefit has been paid.  It generates the reduced lump sum and the surgery benefit and
    **nothing continuing** **[std]**: no inpatient, no treatment months, no outpatient days
    and no state change.  The rationale is a data fact rather than a convenience — the
    sourced 推計患者数 and 平均在院日数 figures are for 悪性新生物 and do not measure in-situ exposure —
    and the direction of the error is stated: it understates the in-situ tier.
    """
    return pols_healthy(t) * insitu_avail(t) * insitu_rate_mth(t) * cover(t)


def pols_death(t):
    """Deaths at the end of month t, from both states.

    Mortality is a pure liability-releasing decrement here: the composite carries **no
    death benefit**, so there is no ``claims_death`` anywhere in the model.  A life
    diagnosed in month t is already in the diagnosed state for this purpose.
    """
    healthy = (pols_healthy(t) - diag_first(t)) * mort_rate_mth(t)
    cancer = (pols_cancer(t) + diag_first(t)) * mort_rate_canc_mth(t)
    return healthy + cancer


def pols_lapse(t):
    """Lapses at the end of month t, taken from the survivors of mortality.

    Zero out of the diagnosed state in the base run.  A lapse pays nothing — there is no
    surrender value at any duration under 終身払 — so this moves :func:`pols_if` and nothing
    else, and ``claims(t, "LAPSE")`` is identically zero.
    """
    healthy = ((pols_healthy(t) - diag_first(t)) * (1.0 - mort_rate_mth(t))
               * lapse_rate_mth(t))
    cancer = ((pols_cancer(t) + diag_first(t)) * (1.0 - mort_rate_canc_mth(t))
              * lapse_rate_canc_mth(t))
    return healthy + cancer


# ===== Cells: the care-benefit bases and their ledgers =====


def hosp_stay_days(t):
    """L: the mean cancer hospitalisation in days.

    14.4 days for 悪性新生物 discharges against 28.4 for all conditions, all ages, from 患者調査.
    With ``hosp_age_gradient`` on, the sourced four-band gradient — 10.7 at 35-64, 15.5 at
    65+, 17.6 at 75+ — is read instead; the base run takes the all-ages figure **[std]**
    because the gradient is published on four broad bands and the incidence on twenty-one
    narrow ones.
    """
    tbl = data.hosp_stay_table()                                     # noqa: F821
    basis = "age_band" if hosp_age_gradient else "all_ages"          # noqa: F821
    rows = tbl[(tbl["basis"] == basis) & (tbl["age_from"] <= age(t))]
    return float(rows.sort_values("age_from")["days"].iloc[-1])


def hosp_rate_mth(t):
    """h: monthly cancer admissions per diagnosed life, ``hosp_rate / 12`` **[std]**.

    The annual 0.25 is derived from two sourced counts on a trick that needs no population
    figure, because the population cancels: 2,689,653 cancer admissions a year — 106,100
    inpatients times 365 over a 14.4-day mean stay — against 993,469 new diagnoses a year
    gives 2.707020 admissions per diagnosed person over a cancer lifetime, and spreading
    that over the 10.815-year mean diagnosed-state duration gives 0.250293.  At 14.4 days
    each it is **38.98 inpatient days per diagnosed person**, the single most useful number
    for sanity-checking an implementation.

    The constant hazard makes the inpatient benefit **proportional to survival**, which is
    the product's actual economics under an unlimited-day design; it does not front-load
    admissions onto the diagnosis month, which real cancer treatment does.
    """
    return hosp_rate / 12.0                                          # noqa: F821


def paid_months(t):
    """The qualifying treatment months paid in month t, ``min(p_tr, K - M(t))``.

    An indicator per month, not a count and not a duration.  ``treat_prob = 0.10``
    **[std]** — 1.2 qualifying months per diagnosed life-year — has no public source and no
    observed range; the only calibration anchor is the cap itself, against which a life
    diagnosed at the anchor age accumulates an expected 12.98 months.
    """
    return min(treat_prob, max(0.0, treat_cap() - treat_months(t)))  # noqa: F821


def treat_months(t):
    """M(t): the treatment-month ledger, **per diagnosed life**, against the cap K.

    ``M(t+1) = (M(t) + paid_months(t)) pols_cancer(t) / (pols_cancer(t) + diag_first(t))``
    — a cohort average diluted by new entrants, and only by first diagnoses, because a
    repeat trigger is an already-diagnosed life whose ledger continues.  Zero while
    ``pols_cancer`` is zero.

    The direction of the approximation is stated rather than discovered:
    ``E[min(sum, K)] != min(E[sum], K)``, so a deterministic average **understates** the
    cap's bite.  Here that matters more than on the medical chassis, because the 60-month
    cap is reached by a real minority rather than never.  ``M(12) = 0.4002`` at the anchor
    cell — small, and not therefore deletable.
    """
    if t <= 0:
        return 0.0
    entering = pols_cancer(t - 1) + diag_first(t - 1)
    if entering <= 0.0:
        return 0.0
    return ((treat_months(t - 1) + paid_months(t - 1))
            * pols_cancer(t - 1) / entering)


def adv_freq_mth():
    """f_a: the monthly 先進医療 療養 frequency per diagnosed life, ``adv_freq / 12`` **[std]**.

    0.012 療養 per diagnosed life-year, with no observed range.  The medical chassis carries
    the sourced 先進医療 cost anchors; this product's own source set does not, so neither the
    frequency nor the severity can be tagged here.
    """
    return adv_freq / 12.0                                           # noqa: F821


def adv_pay(t):
    """pay(t): the 技術料 reimbursable per 療養 in month t, ``min(S_a, LV - V(t))``.

    ``adv_sev`` = ¥600,000 **[std]**, set well above the medical chassis's population-wide
    figure because a cancer-only trigger selects for particle-beam therapy, which is the
    expensive end of the 先進医療 list; the direction is defensible and the level is not
    sourced.  The draw falls to zero when the ¥20,000,000 lifetime cap is reached, which is
    how the rider's termination on the cap is implemented.  Zero without the rider.
    """
    if not adv_rider():
        return 0.0
    return min(adv_sev, max(0.0, adv_cap - adv_paid(t)))             # noqa: F821


def adv_paid(t):
    """V(t): the 先進医療 技術料 ledger, **per diagnosed life**, against the ¥20,000,000 cap.

    Diluted by new entrants on the same cohort-average basis as :func:`treat_months`, and
    accumulating the 技術料 only — the 10% cash top-up is a benefit, not a draw against the
    cap.  ``V(12) = ¥2,401.31`` at the anchor cell.
    """
    if t <= 0:
        return 0.0
    entering = pols_cancer(t - 1) + diag_first(t - 1)
    if entering <= 0.0:
        return 0.0
    return ((adv_paid(t - 1) + adv_freq_mth() * adv_pay(t - 1))
            * pols_cancer(t - 1) / entering)


# ===== Cells: cash flows =====


def pols_payer(t):
    """The in-force policies actually paying premium at the start of month t.

    :func:`pols_healthy` on the composite, because the waiver fires on the first invasive
    diagnosis; :func:`pols_if` on the disability-trigger and no-waiver designs, where a
    cancer diagnosis does not stop the premium.  Weighting the premium by ``pols_if`` on
    the composite overstates income by exactly the waived population.
    """
    if waiver_trigger() == "cancer_diag":
        return pols_healthy(t)
    return pols_if(t)


def premium_factor(t):
    """The repricing factor on the 10年更新 定期 chassis flag **[std]**; 1 in the base run.

    The renewal recomputes the premium at then-current rates, which would ordinarily close
    the Solvency contract boundary at each renewal.  ``jplib`` projects the flag to final
    expiry at a flat rate and records the tension rather than resolving it; set
    ``renew_reprice_rate`` above zero to step the premium at each renewal instead.
    """
    if chassis() != "teiki" or renew_reprice_rate == 0.0:            # noqa: F821
        return 1.0
    return (1.0 + renew_reprice_rate) ** (t // renewal_months)       # noqa: F821


def prem_payable(t):
    """Whether a premium falls due in month t: 1 during the premium-paying period, else 0.

    終身払 pays for life.  65歳払済 stops at the 年単位の契約応当日 on which the insured attains 65,
    after which the cover continues unpaid — and so does the maintenance expense, which is
    what makes expense inflation a first-order lever on a short-pay design.
    """
    if prem_period_type() == "to_65" and age(t) >= 65:
        return 0.0
    return 1.0


def premiums(t):
    """Premium income at the start of month t, an inflow.

    ``P x pols_payer(t)``.  On the composite that is ``P x pols_healthy(t)``: the waiver
    fires on the first invasive diagnosis, so the diagnosed pay nothing.  The premium is
    still charged throughout the 90-day waiting period — five of the six carriers that
    state it charge from inception, and the one that does not says explicitly that its
    three free months are not a discount.
    """
    return premium_mth_pp() * premium_factor(t) * pols_payer(t) * prem_payable(t)


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"DIAG"``
        the がん診断一時金, ``DB x trig(t)`` — first diagnoses and repeats alike,
        with no lifetime cap and no termination on payment.

    ``"INSITU"``
        the 上皮内新生物 tier, ``u x DB x insitu_ev(t)``: a second benefit at a
        second rate on its own once-only cap, not a discount on the first.

    ``"HOSP"``
        the がん入院給付金, ``D x L x h x pols_cancer(t)``, with **no
        per-hospitalization and no 通算 day limit**.

    ``"SURGERY"``
        the がん手術給付金, ``m_s x A`` times two limbs: surgeries on the diagnosed
        state at ``s_h`` per admission, and ``s_z`` surgeries recognised in the
        month of an in-situ diagnosis, since in-situ disease is by definition
        managed by local excision and the composite pays the benefit in full.

    ``"TREAT"``
        the がん治療給付金, ``B_tr x paid_months(t) x pols_cancer(t)`` — JPY per
        **month** times months, with no day count anywhere in it.

    ``"OUTPATIENT"``
        the がん通院給付金, ``A x o x pols_cancer(t)``.  ``outp_days = 1.10``
        **[std]** per diagnosed life-year derives from 186,400 cancer
        outpatients on the survey day at 250 **[std]** operating days a year —
        46.91 visits per diagnosed person — of which a **25% [std]** share is
        treatment-linked and so qualifying.  Both the 250 and the 25% are
        unsourced and between them they are a factor-of-four uncertainty.

    ``"ADVANCED"``
        the 先進医療給付金, ``f_a (pay + min(10% pay, 500,000)) x pols_cancer(t)``.

    ``"DISCHARGE"``
        the がん退院一時金, zero unless the rider is attached; a **[std]**
        construction, since the technical notes carry the flag but not the
        formula.  See the Space docstring.

    ``"LAPSE"``
        zero, always.  There is no surrender value at any duration under 終身払;
        the kind exists so that the zero is stated rather than left to
        inference.

    At the anchor cell's parameters the five care benefits are fixed yen amounts per
    diagnosed life-month and the five numbers are worth memorising as an implementation
    check: ¥3,000.00 inpatient, ¥1,458.33 surgery, ¥10,000.00 treatment, ¥916.67
    outpatient and ¥660.00 advanced medicine — ¥16,035.00 in total.
    """
    if kind is None:
        return sum(claims(t, k) for k in (
            "DIAG", "INSITU", "HOSP", "SURGERY", "TREAT", "OUTPATIENT",
            "ADVANCED", "DISCHARGE", "LAPSE"))
    if kind == "DIAG":
        return diag_benefit() * trig(t)
    if kind == "INSITU":
        return insitu_pct() * diag_benefit() * insitu_ev(t)
    if kind == "HOSP":
        return (daily_amount() * hosp_stay_days(t) * hosp_rate_mth(t)
                * pols_cancer(t))
    if kind == "SURGERY":
        return surg_mult() * base_amount() * (
            surg_per_hosp * hosp_rate_mth(t) * pols_cancer(t)        # noqa: F821
            + surg_per_insitu * insitu_ev(t))                        # noqa: F821
    if kind == "TREAT":
        return treat_benefit() * paid_months(t) * pols_cancer(t)
    if kind == "OUTPATIENT":
        return outp_daily() * (outp_days / 12.0) * pols_cancer(t)    # noqa: F821
    if kind == "ADVANCED":
        pay = adv_pay(t)
        top_up = min(adv_topup_rate * pay, adv_topup_cap)            # noqa: F821
        return adv_freq_mth() * (pay + top_up) * pols_cancer(t)
    if kind == "DISCHARGE":
        if not disch_rider():
            return 0.0
        return (disch_mult * base_amount() * disch_qual_share        # noqa: F821
                * hosp_rate_mth(t) * pols_cancer(t))
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + pi)^(t // 12)`` **[std]**.

    1.0% p.a. flat, stepping at each 年単位の契約応当日 rather than gliding monthly.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def maint_expenses(t):
    """e(t): the maintenance expense at the start of month t **[std]**.

    ¥250 per policy per month inflating at 1% p.a., on :func:`pols_if` — a waived policy is
    still serviced, so the expense runs on the diagnosed population with no premium against
    it.  ¥250 against a ¥3,000 premium is 8.3% of premium, the premium is fixed for life
    and the expense is not, which is why the notes rate expense inflation a first-order
    lever despite its size.
    """
    return expense_maint * inflation_factor(t) * pols_if(t)          # noqa: F821


def claim_expenses(t):
    """The claim handling expense at the end of month t **[std]**.

    ¥5,000 per diagnosis trigger — invasive or in-situ — and ¥3,000 per cancer admission.
    A cells of its own, deducted explicitly in :func:`net_cf` and published as its own
    ``claim_expenses`` column of :func:`result_cf`; it is **not** inside :func:`expenses`.
    Keeping it separate is what lets a reader see the policy-servicing cost and the
    claim-handling cost move independently, which on this product they do: the first rides
    on :func:`pols_if` and the second on the diagnosis and admission counts.
    """
    return (expense_claim_diag * (trig(t) + insitu_ev(t))            # noqa: F821
            + expense_claim_hosp * hosp_rate_mth(t) * pols_cancer(t))  # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**; **not** claim handling.

    ¥20,000 per policy at ``t = 0``, then the inflating maintenance expense.  The claim
    handling expense is :func:`claim_expenses`, a separate cells with a column of its own —
    the library-wide split, so that ``expenses`` means the same thing in every model.  No
    Japanese cancer expense scale is public; the levels are carried from the medical
    chassis and scaled to this product's premium.

    ``technical-notes.md``'s month-by-month traces print the two in **one arithmetic
    line** — ``250 x pols_if + 5,000 x diagnoses + 3,000 x admissions`` — because the
    notes narrate the month's expense as a single sum.  The worked-example table and the
    policy-year-1 aggregate carry the two as separate rows, matching the two columns
    published here; the notes' combined figure is their sum.
    """
    acq = expense_acq if t == 0 else 0.0                             # noqa: F821
    return maint_expenses(t) + acq


def commissions(t):
    """Commission outgo in month t **[std]**.

    1.5 times the annualized premium at ``t = 0`` — ¥54,000 on the anchor cell — then 3.0%
    of premium income from policy year 2.  No Japanese commission scale is public either.
    With the acquisition expense this is ¥74,000 of cost at outset against a ¥3,000 monthly
    premium: the product's cost is almost entirely in front of it.
    """
    init = comm_init_rate * 12.0 * premium_mth_pp() if t == 0 else 0.0   # noqa: F821
    renew = (comm_renewal_rate * premiums(t)                         # noqa: F821
             if t >= comm_renewal_start else 0.0)                    # noqa: F821
    return init + renew


def net_cf(t):
    """The net cash flow of month t, **income positive**.

    Premiums less every benefit line, less :func:`expenses` (acquisition and maintenance),
    less :func:`claim_expenses` **deducted explicitly**, less commission.  The notes' own
    sign, which is also the library-wide convention, so there is no outgo-positive
    ``liability_cf`` companion to publish.

    Note the asymmetry that defines this product's cash-flow signature: premiums are
    weighted by :func:`pols_healthy` and claims by :func:`pols_cancer`, and the two are
    disjoint.  Every error in incidence therefore hits both sides of the cash flow at once,
    roughly doubling its effect here.
    """
    return (premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
            - commissions(t))


# ===== Cells: roll-forward and ledger checks =====


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - deaths - lapses``.  There is no maturity term and no
    benefit-driven termination to add: the contract does not end and cannot exhaust, so a
    life leaves only by dying or lapsing.  A first diagnosis cancels out of this identity
    because it moves a life between states rather than out of the book.
    """
    return pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so one
    test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the month that failed.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                       # noqa: F821
    return all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_cancer_roll_fwd_resid(t):
    """The diagnosed-state roll-forward residual in month t; zero everywhere.

    ``pols_cancer(t+1) - (pols_cancer(t) + diag_first(t)) sc(t)``.  The ``locked`` and
    ``open`` recursions each carry an ``unlock`` term of opposite sign, so their sum must
    collapse to this one line; a sign slip or an off-by-one in the delay shows up here and
    nowhere else in the in-force figures.
    """
    return pols_cancer(t + 1) - (
        pols_cancer(t) + diag_first(t)) * surv_canc(t)


def check_cancer_roll_fwd():
    """True when the diagnosed-state roll-forward closes in every projected month."""
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                       # noqa: F821
    return all(abs(check_cancer_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_cycle_ledger_resid(t):
    """The two-year cycle ledger residual in month t; zero everywhere.

    :func:`pols_locked` less an independent rebuild of the same figure — the triggers of
    the previous ``C - 1`` months, each carried forward on diagnosed decrements — summed
    straight off the trigger vector with no reference to the :func:`unlock` recursion.  A
    cycle implemented as a rate rather than as a delay, or one released a month early or
    late, shows up here.
    """
    built = 0.0
    factor = 1.0
    for s in range(t - 1, max(t - cycle_months(), -1), -1):
        factor = factor * surv_canc(s)
        built = built + trig(s) * factor
    return pols_locked(t) - built


def check_cycle_ledger():
    """True when the two-year cycle ledger closes in every projected month."""
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                       # noqa: F821
    return all(abs(check_cycle_ledger_resid(t)) <= tol
               for t in range(proj_len()))


def check_insitu_ledger_resid(t):
    """The once-only 上皮内新生物 ledger residual in month t; zero everywhere.

    ``insitu_avail(t) + insitu_used(t) - 1``.  :func:`insitu_used` is accumulated off the
    published claim line rather than off the ledger recursion, so the identity fails if the
    benefit is paid at a rate the ledger is not decremented by — which is what implementing
    the tier as a share of the main diagnosis benefit would do.
    """
    return insitu_avail(t) + insitu_used(t) - 1.0


def check_insitu_ledger():
    """True when the once-only 上皮内新生物 ledger closes in every month it is observable in.

    The identity is read off the claim line, so it says nothing once the never-diagnosed
    population is exhausted: at the terminal age the best-estimate mortality reaches
    exactly 1, ``pols_healthy`` becomes zero and no in-situ benefit is paid, while
    :func:`insitu_avail` — a probability conditional on being never diagnosed and in force
    — keeps running against nobody.  Those months carry no information and are excluded
    rather than papered over.
    """
    return all(abs(check_insitu_ledger_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()) if pols_healthy(t) > 0.0)


def check_treat_cap_resid(t):
    """The treatment-month ledger's excursion outside ``[0, K]`` in month t; zero everywhere.

    Positive when the month's draw would carry the ledger past the 60-month cap, negative
    if the ledger ever went below zero.  This is the identity the cap exists to enforce, and
    it is the one a per-block rather than per-life ledger would break by deferring the cap
    forever.
    """
    ledger = treat_months(t)
    return (max(0.0, ledger + paid_months(t) - treat_cap())
            + min(0.0, ledger))


def check_treat_cap():
    """True when the treatment-month ledger stays inside its cap in every month."""
    return all(abs(check_treat_cap_resid(t)) <= roll_fwd_tol         # noqa: F821
               for t in range(proj_len()))


def check_adv_cap_resid(t):
    """The 先進医療 ledger's excursion outside ``[0, LV]`` in month t; zero everywhere.

    The rider terminates when the ¥20,000,000 lifetime cap is reached, so the ledger plus
    the month's draw must never pass it.
    """
    ledger = adv_paid(t)
    return (max(0.0, ledger + adv_freq_mth() * adv_pay(t) - adv_cap)  # noqa: F821
            + min(0.0, ledger))


def check_adv_cap():
    """True when the 先進医療 ledger stays inside its cap in every month."""
    return all(abs(check_adv_cap_resid(t)) <= roll_fwd_tol * adv_cap  # noqa: F821
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in month t; zero everywhere.

    Rebuilds ``net_cf`` from the columns of :func:`result_cf` rather than from
    :func:`net_cf`, so a column wired to the wrong cells, a benefit line dropped from the
    table or a double-counted claim expense shows up as a non-zero residual in the very
    table a reader is looking at.

    The benefit side is every column whose name begins ``claims_``, taken as a group
    rather than enumerated: :func:`result_cf` publishes the nine splits and **no bare
    ``claims`` subtotal beside them**, so the columns of the table sum to ``net_cf``
    without a reader having to know which of them to skip.  A benefit line added to the
    table and not to :func:`net_cf` is caught by the same sweep.
    """
    row = result_cf().loc[t]
    outgo = sum(row[c] for c in row.index if str(c).startswith("claims_"))
    return (row["premiums"] - outgo - row["expenses"] - row["claim_expenses"]
            - row["commissions"] - row["net_cf"])


def check_net_cf():
    """True when the published cash-flow statement adds up in every projected month."""
    tol = roll_fwd_tol * max(premium_mth_pp(), 1.0)                      # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(proj_len()))


# ===== Cells: result tables =====


def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month count and the weight on the maintenance expense of
    the same row — but *not* on ``premiums``, which is carried by ``pols_healthy``, nor on
    the seven benefit lines, five of which are carried by ``pols_cancer``.  Publishing the
    three counts side by side is what makes that asymmetry visible in the table itself.

    ``expenses`` is acquisition plus maintenance and ``claim_expenses`` is the claim
    handling cost, in two columns rather than one: the library-wide split, and on this
    product the two move on different weights.

    ``net_cf`` carries the notes' own income-positive sign.  ``claims_lapse`` is a column
    of zeros by product design — there is no surrender value — and is published rather than
    dropped; ``claims_discharge`` is zero unless the がん退院一時金 rider is attached.  There is
    no ``claims_death`` column at all, because the composite has no death benefit.

    The nine benefit lines are published as splits and **no bare ``claims`` subtotal is
    published beside them**.  The table's columns therefore add to ``net_cf`` as they
    stand: premiums less every ``claims_*`` column, less ``expenses``, ``claim_expenses``
    and ``commissions``.  A subtotal column sitting among its own components would break
    that, since a reader summing the row would double the whole benefit side.  The
    :func:`claims` cells still returns the total when its ``kind`` argument is omitted;
    it is the *column* that is not published.  :func:`check_net_cf` asserts the identity
    off this table in every projected month.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_healthy": [pols_healthy(t) for t in ts],
            "pols_cancer": [pols_cancer(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_diag": [claims(t, "DIAG") for t in ts],
            "claims_insitu": [claims(t, "INSITU") for t in ts],
            "claims_hosp": [claims(t, "HOSP") for t in ts],
            "claims_surgery": [claims(t, "SURGERY") for t in ts],
            "claims_treat": [claims(t, "TREAT") for t in ts],
            "claims_outpatient": [claims(t, "OUTPATIENT") for t in ts],
            "claims_advanced": [claims(t, "ADVANCED") for t in ts],
            "claims_discharge": [claims(t, "DISCHARGE") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts, decrement rates and ledgers, indexed by month t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_healthy": [pols_healthy(t) for t in ts],
            "pols_locked": [pols_locked(t) for t in ts],
            "pols_open": [pols_open(t) for t in ts],
            "pols_cancer": [pols_cancer(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "diag_first": [diag_first(t) for t in ts],
            "diag_rep": [diag_rep(t) for t in ts],
            "insitu_ev": [insitu_ev(t) for t in ts],
            "insitu_avail": [insitu_avail(t) for t in ts],
            "treat_months": [treat_months(t) for t in ts],
            "adv_paid": [adv_paid(t) for t in ts],
            "inc_rate": [inc_rate(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age_male = 116

omega_age_female = 118

mort_be_factor = 1.25

mort_age_offset = 0.0

net_of_cancer = False

cancer_death_share = 0.28

insitu_share = 0.122

rel_rate = 0.06

hosp_rate = 0.25

hosp_age_gradient = False

surg_per_hosp = 0.35

surg_per_insitu = 0.80

treat_prob = 0.10

outp_days = 1.10

adv_freq = 0.012

adv_sev = 600000.0

adv_cap = 20000000.0

adv_topup_rate = 0.10

adv_topup_cap = 500000.0

disch_mult = 10.0

disch_qual_share = 0.60

expense_acq = 20000.0

expense_maint = 250.0

expense_claim_diag = 5000.0

expense_claim_hosp = 3000.0

inflation_rate = 0.01

comm_init_rate = 1.5

comm_renewal_rate = 0.03

comm_renewal_start = 12

sel_lapse_lambda = 0.0

sel_lapse_ref = 0.20

lapse_canc_factor = 1.0

void_adjust = False

renew_reprice_rate = 0.0

renewal_months = 120

roll_fwd_tol = 1e-10

math = ("Module", "math")

pd = ("Module", "pandas")
