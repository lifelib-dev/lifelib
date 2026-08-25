# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Medical_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the first policy month and
``t = proj_len() - 1`` the last. Month ``t`` is the interval from ``t`` to ``t + 1``
months after the 契約日. On the 終身 chassis the horizon is the terminal age of the
mortality table — 116 male, 118 female — and there is no maturity benefit at it; on the
定期 model point flag the horizon is the last ten-year renewal that completes before
age 80.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/medical/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Medical_JP_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Medical_JP_S.Data`, reached here through the ``data`` Reference:

=====================  ================================  ==========================
Reference              Cells                             File
=====================  ================================  ==========================
model_point_file       data.model_point_table()          model_point_table.csv
mort_table_file        data.mort_table()                 mort_table.csv
lapse_table_file       data.lapse_table()                lapse_table.csv
incidence_table_file   data.incidence_table()            incidence_table.csv
los_table_file         data.los_table()                  los_table.csv
=====================  ================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
annual rates with ``*_rate_mth`` for their monthly companions, ``*_pp`` for per-policy
amounts, ``claims(t, kind)`` with an uppercase ``kind`` string, ``pols_if_at(t, timing)``
for the within-month in-force reads. The technical notes use compact symbols instead.
The mapping is:

=========================  ==============================  ===========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ===========================
(model point row)          model_point()                   The selected model point
chassis                    chassis()                       shushin (終身) or teiki (定期)
x                          issue_age()                     契約年齢, 満年齢 at 契約日
age(t)                     age(t)                          Attained 満年齢 in month t
y(t)                       policy_year(t)                  floor(t/12) + 1
(none)                     sex()                           M or F
D                          daily_amount()                  入院給付金日額, JPY per day
L1                         limit_per_hosp()                Per-hospitalization day limit
LA                         limit_agg()                     通算 day limit, per limb
F                          min_days_floor()                Five-day minimum, 5 or 0
P                          premium_mth_pp()                Monthly office premium
(none)                     prem_period_type()              whole_life or to_65
(none)                     prem_end_month()                First month with no premium
(terminal age)             omega_age()                     Terminal age of the table
(final expiry)             expiry_age()                    定期 flag's final expiry age
proj_len                   proj_len()                      Number of projected months
(table)                    mort_rate_at_age(x)             第三分野 proxy rate at age x
(table)                    mort_rate_base(t)               第三分野 proxy rate at age(t)
mort_be_factor             mort_be_factor                  1.25 [std] best-estimate scale
q(age)                     mort_rate(t)                    Annual best-estimate mortality
q(t)                       mort_rate_mth(t)                Monthly mortality in month t
(table)                    lapse_rate(t)                   Annual lapse rate, policy year
w(t)                       lapse_rate_mth(t)               Monthly lapse in month t
w_cum(t)                   lapse_cum(t)                    Cumulative lapse proportion
lam                        sel_lapse_lambda                Anti-selective lapse loading
w_ref                      sel_lapse_ref                   Its cumulative-lapse threshold
(none)                     sel_lapse_factor(t)             Loading on *morbidity*
juryoritsu, alos           inc_rate_base(t)                受療率 -> incidence [std]
inc_rate(age)              inc_rate(t)                     Annual incidence, effective
i(t)                       inc_rate_mth(t)                 Monthly incidence
g_j                        los_days(band)                  Stay-length band day values
pi_j                       los_probs(band)                 Stay-length band probabilities
Sum pi_j g_j               d_raw(t)                        Uncapped mean stay
Sum pi_j min(g_j, L1)      d_pay_capped(t)                 Paid days after L1
d_pay                      d_pay(t)                        Days that consume the ledger
d_ben                      d_ben(t)                        Benefit days, floor included
(none)                     d_ben_free(t)                   Days outside the 通算 count
(none)                     d_ben_ltd(t)                    Days inside the 通算 count
room_dis, room_acc         room_dis(t), room_acc(t)        Days left on each limb
d_pay_dis, d_pay_acc       d_pay_dis(t), d_pay_acc(t)      Paid days after the 通算 cap
d_ben_dis, d_ben_acc       d_ben_dis(t), d_ben_acc(t)      Benefit days after the cap
A_dis(t)                   agg_days_dis(t)                 疾病 通算 ledger, days
A_acc(t)                   agg_days_acc(t)                 災害 通算 ledger, days
s_dis, s_acc               s_dis, s_acc                    Limb split of incidence [std]
term(t)                    term_rate(t)                    Benefit-driven termination
s_ih                       surg_ih_per_hosp                In-hospital surgeries per stay
s_op                       surg_op_per_hosp                Outpatient surgeries per stay
(switch)                   surg_ih_eff(t)                  In-hospital surgeries payable
m_ih, m_op                 surg_mult_ih(), surg_mult_op()  Surgery multiples of D
f_adv                      adv_freq_mth()                  Monthly 先進医療 frequency
S_adv                      adv_sev                         Mean 技術料 per 療養
pay(t)                     adv_pay_pp(t)                   Reimbursement before top-up
adv_claim(t)               adv_claim_pp(t)                 先進医療 claim per policy
V(t), LV                   adv_paid(t), adv_cap            先進医療 ledger and its cap
(rider)                    lump_count(t)                   入院一時金 通算 count ledger
waived(t)                  waived(t)                       Fraction on 保険料払込免除
waiver_inc                 waiver_inc_mth(t)               Waiver incidence, 0 in base
l(t)                       pols_if(t)                      In force at the start of t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
(none)                     pols_death(t)                   Deaths in month t
(none)                     pols_lapse(t)                   Lapses in month t
(none)                     pols_term(t)                    Benefit-driven terminations
(none)                     pols_maturity(t)                Cover ending at the scheduled end
(none)                     pols_payer(t)                   Policies actually paying
(none)                     cv_pp(t)                        解約返戻金, zero under 終身払
P l(t)(1 - waived)         premiums(t)                     Premium income
claims_hosp(t)             claims(t, "HOSP")               入院給付金 outgo
claims_surgery(t)          claims(t, "SURGERY")            手術給付金 outgo
claims_advanced(t)         claims(t, "ADVANCED")           先進医療給付金 outgo
(rider)                    claims(t, "LUMP")               入院一時金 outgo
(zero)                     claims(t, "LAPSE")              Surrender outgo, zero on 終身払
claims(t)                  claims(t)                       All benefit outgo
e(t)                       expense_maint_pp(t)             Maintenance expense per policy
ec i(t)                    claim_expenses(t)               Claim handling expense, separate
E0, e(t)                   expenses(t)                     Acquisition + maintenance only
commissions(t)             commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ===========================

Four names needed care.

The notes write ``i(t)`` for the *monthly* incidence and ``inc_rate(age)`` for the annual
one. The library convention is that a bare ``*_rate`` is annual and ``*_rate_mth`` its
monthly companion, as ``mort_rate`` / ``mort_rate_mth`` already are, so the two become
:func:`inc_rate` and :func:`inc_rate_mth` and neither can be mistaken for the other.

``d_pay`` and ``d_ben`` are **not** the same quantity and the difference is the
five-day minimum. The carriers express the floor as an *amount*, 日額 x 5, not as a
credit of five days, so it enters :func:`d_ben` and never :func:`d_pay` — and therefore
never the 通算 ledger. :func:`check_day_limits` asserts ``d_ben >= d_pay`` in every
month; a model that credited the floor to the ledger would let a two-day stay consume
five days of a lifetime limit it never used.

``term(t)`` in the notes is a 0/1 indicator, and a decrement count is a different thing
from a decrement rate. It is spelled :func:`term_rate` here, alongside
:func:`mort_rate_mth` and :func:`lapse_rate_mth`, with the count it produces at
:func:`pols_term`.

``pols_maturity`` has no symbol in the notes at all. Library-wide it is the count whose
cover ends at the **scheduled end of the contract**, whether or not anything is paid for
it; any payment would be ``claims(t, "MATURITY")``, and on this product there is none.
The 終身 chassis has no scheduled end: the projection stops where the mortality table
does and everybody has already died, so the cells is zero even in the final month. The
定期 model point flag does have one — its final ten-year renewal — and without a term
for it the in-force roll-forward would appear to lose lives with no cause in that month.
:func:`check_pols_roll_fwd` asserts

    pols_if(t) - pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_term(t)
                                + pols_maturity(t)

in every projected month. It is bookkeeping determined by the notes' own rules, not an
added assumption, and it is *not* a maturity benefit: the amount paid is nil.

.. rubric:: The day-limit machinery

Three limits act in a fixed order, and getting the order wrong is the classic
implementation failure on this product.

**1 — the per-hospitalization limit ``L1``, applied inside the stay expectation**, spell
by spell, before anything else: ``d_pay_capped = Sum_j pi_j min(g_j, L1)``. On the anchor
cell's 35-64 row that is 15.20 days against an uncapped mean of 20.20 — the 60-day cap
removes 24.75% of raw days. Capping the *mean* instead would give
``min(20.20, 60) = 20.20`` and silently remove the limit altogether.

**2 — the five-day minimum, which is an amount and not days**, so it enters
:func:`d_ben` only: ``d_ben_capped = Sum_j pi_j max(F, min(g_j, L1))``. With ``F = 5``
the 35-64 row gives 16.10 benefit days against 15.20 paid days.

**3 — the aggregate limit ``LA``, per limb, with memory.** Two ledgers, because the 通算
limit runs separately on the 疾病 and 災害 limbs, and cover ceases only when **both**
are exhausted. One combined ledger terminates the contract roughly twice as early.

The two ledgers are carried **per surviving policy** and are never weighted by
``pols_if``. This is the easiest state-variable error in the product: a ledger multiplied
by the in-force probability measures the block's consumption rather than the
individual's, and defers the limit indefinitely.

On the anchor cell's expectation ``LA`` never binds — ``agg_days_dis`` grows by about
0.709 days a year at age 40 and about 15.2 at 90 and over, reaching only single-digit
hundreds of days by the terminal age — and the ¥20,000,000 先進医療 cap is never
approached either. That is a property of the expectation, not of the product:
``E[min(Sum, LA)] != min(E[Sum], LA)``, so the deterministic ledger **understates** the
limit's bite by ignoring dispersion **[std]**. The machinery is implemented anyway
because it binds under the 三大疾病無制限 特則 and because a seriatim or stochastic run
needs it. It is **not** kept for the dependants: neither ``Cancer_JP_S`` nor ``LTC_JP_S``
inherits it — each deletes the day-limit machinery outright as a product fact of its own.
Do not delete a ledger because it reads zero.

.. rubric:: Modules that are off in the base run

Five of the notes' optional constructions are implemented and switched off on the anchor
cell, so that the base run reproduces the worked example while the machinery stays
visible and testable:

- **Anti-selective lapse**, ``inc_eff = inc (1 + lam max(0, w_cum - w_ref))`` with
  ``sel_lapse_lambda = 0``. Healthy lives lapse first, so the persisting block is
  progressively impaired on the *morbidity* basis rather than the mortality one — the
  reverse of the term assurance case. No Japanese selective-lapse evidence was retrieved.
- **保険料払込免除 (premium waiver)**, an absorbing state on the premium-paying
  population, with incidence zero unless the 特定三疾病保険料払込免除特則 is elected on
  the model point. The base contractual waiver is disability-triggered and its incidence
  is **zero in every run**: 第三分野標準生命表2018 excludes 高度障害, so the incidence
  cannot be read out of the mortality basis, and no public Japanese 高度障害 incidence
  table was retrieved. Model point 7 exercises the elected 特則 at the notes' suggested
  placeholder ``waiver_inc_mult = 0.25`` x ``mort_rate``.
- **The 三大疾病無制限 特則**, which does not merely raise the limits: it takes がん,
  心疾患 and 脳血管疾患 days out of the 通算 count entirely and removes ``L1`` for them,
  deferring the benefit-driven termination. Off on the anchor cell, elected on model
  point 4. Its one parameter, ``share_3dis``, is **[std]** and carries no observed range
  — no cause split of 入院受療率 was extracted in the research pass.
- **入院一時金特約**, ¥100,000 per hospitalization with a 通算 count limit of 50, off on
  the anchor cell and elected on model points 3 and 7.
- **The age-basis offset.** The contract ages on 満年齢 while 第三分野標準生命表2018 is
  built for 保険年齢方式, so half a year sits between the projection basis and the
  valuation basis. ``age_basis_offset = 0`` accepts the offset **[std]**; setting it to
  0.5 reads the table at ``age(t) + 0.5`` by linear interpolation. The notes require the
  mismatch be stated rather than silently absorbed, which is what the switch does.

``surg_after_limit`` is a switch too, but it is **on** in the base run because it
resolves a **contradiction between carriers** rather than an optional feature: where
surgery is performed during a stay for which 入院給付金 is no longer payable because
``L1`` is exhausted, one carrier pays at the in-hospital multiple and another pays
nothing at all. The composite pays. With the switch reversed — model point 5 — the
truncated day fraction, 24.75% of in-hospital surgeries on the anchor basis, falls
outside cover. The two positions differ by a quarter of the in-hospital surgery benefit
and are not roundable into each other.

.. rubric:: Sign convention

The notes' ``net_cf(t)`` is already **income positive** — premiums less benefits, less
acquisition and maintenance expense, less claim expense, less commission — which is the
library-wide sign of :func:`net_cf`, so unlike
the whole life and payout annuity models there is no ``liability_cf`` companion to
publish: one stream, one sign, one name.

.. rubric:: Three absences that are product facts

There is **no death benefit**: the main contract pays nothing on death, so mortality is a
pure liability-releasing decrement and no ``claims_death`` exists. There is **no
自動振替貸付 and no 契約者貸付**: with no surrender value there is nothing to lend
against, so nothing carries a policy through a missed premium and no lapse-suppression
term belongs in the recursion — importing the ``WholeLife_JP_A`` machinery here would
suppress lapses that really happen. And there is **no surrender value at all** under
終身払, at any duration, so ``claims(t, "LAPSE")`` is identically zero on the anchor cell
and the zero is published rather than dropped. :func:`cv_pp` exists only because the
65歳払済 short-pay variant acquires a small value, 10 x 日額, once the premium-paying
period completes — model point 4 — and that is the single route by which this chassis
ever has one.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
# --- Model point attributes ------------------------------------------------

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def chassis():
    """``shushin`` (終身, whole of life) or ``teiki`` (定期, ten-year renewable).

    Three of the five carriers write 終身 only, one writes 終身 and 定期 as separate
    products and one writes only a 医療保険（定期型）renewable to age 80 [S1][S4][S6]
    [S7][S9][S10].  The composite takes 終身 — the majority design, and the one that
    exercises the lifetime aggregate limit, which a ten-year term does not.
    """
    v = model_point()["chassis"]
    if v not in ("shushin", "teiki"):
        raise ValueError("invalid chassis")
    return v


def issue_age():
    """x: the 契約年齢 on a 満年齢 basis, 20 to 80 [S3][S6][S10].

    満年齢 is the attained age at the 契約日 with the fraction discarded, incremented at
    each 年単位の契約応当日 [S4][S10].
    """
    return int(model_point()["issue_age"])


def sex():
    """The sex, M or F.  A rating factor at every carrier [S6].

    The published premium scales cross over between ages 30 and 40 — female above male
    at 20 and 30, below from 40 on [S3][S8] — which is a morbidity feature, not a
    pricing artefact, and is what the **[std]** sex factors on incidence reproduce.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def daily_amount():
    """D: the 入院給付金日額, JPY per day; menu ¥3,000-¥15,000 [S6].

    The unit of account of the whole product.  This is a frequency x severity x limit
    structure, not a sum-assured structure, so ``D`` multiplies *days* and never a
    benefit amount.
    """
    return float(model_point()["daily_amount"])


def limit_per_hosp():
    """L1: the 1入院の支払限度日数, 60 or 120 days [S1][S4][S9].

    Elected at issue and **never changeable** [S4][S9], which is why it is a model point
    attribute and not a state variable.  Any code path that varies it over ``t`` models a
    contract term that does not exist.
    """
    v = int(model_point()["limit_per_hosp"])
    if v <= 0:
        raise ValueError("limit_per_hosp must be positive")
    return v


def limit_agg():
    """LA: the 通算支払限度日数, 1,095 or 1,000 days, applied **per limb** [S4][S1].

    Four carriers write 1,095 and three write 1,000 [S1][S2][S4][S6][S7][S9][S10]; the
    composite takes the majority with 1,000 as a switch.  Applying the cap separately to
    the 疾病 and 災害 limbs is the disclosed treatment at two carriers and is what this
    model implements — see :func:`agg_days_dis` and :func:`agg_days_acc`.
    """
    return float(model_point()["limit_agg"])


def prem_period_type():
    """The 保険料払込期間: ``whole_life`` (終身払) or ``to_65`` (65歳払済) [S1][S6].

    終身払 is the default because it is offered everywhere and is the design under which
    no surrender value ever arises; the 短期払 variant is the only route by which this
    chassis acquires one at all.
    """
    v = model_point()["prem_period"]
    if v not in ("whole_life", "to_65"):
        raise ValueError("invalid prem_period")
    return v


def premium_mth_pp():
    """P: the level monthly office premium per policy **[std]**.

    An **input, not a computed quantity**.  No carrier publishes a rate table by age and
    duration: the 算出方法書 is a 基礎書類 filed with the 金融庁 and is not published
    [REG-R2], which is exactly why every pricing-basis parameter in this library is
    **[std]** while every contractual parameter carries an [S#] tag.  The anchor value
    ¥2,100 sits between the two public specimen rates for this exact specification —
    ¥2,121 and ¥2,080 at age 40 male on a ¥5,000 daily amount, 60日型, 終身払 [S8][S3].

    Level and 無配当 with no insurer repricing right on the 終身 chassis [S3][S6][S8], so
    every future premium is inside the contract boundary.
    """
    return float(model_point()["premium"])


def prem_mode():
    """月払 / 半年払 / 年払.

    Inert on this grid, which is monthly because the product is: 月払 is the dominant
    retail mode and one net-direct product is 月払 only [S10].  6- or 12-month 前納 at a
    company-set discount [S4] is an immaterial modal refinement and is not modelled
    **[std scope]**.
    """
    return model_point()["prem_mode"]


def surg_mult_ih():
    """m_ih: the 手術給付金 multiple of D for surgery **in hospital**, 20 or 10 [S1][S3]."""
    return float(model_point()["surg_mult_ih"])


def surg_mult_op():
    """m_op: the 手術給付金 multiple of D for **outpatient** surgery, 5 or 0 [S1][S3].

    Zero is a real market design, not a missing value: one carrier pays a flat 10倍 in
    hospital and does not cover outpatient surgery at all [S10].
    """
    return float(model_point()["surg_mult_op"])


def min_days_5():
    """Whether the five-day minimum payment applies; **off** in the composite base.

    Two of the five carriers guarantee 「入院日数が5日以内の場合は、入院給付金日額×5」
    [S4][S6][S7] and three pay actual days [S1][S2][S9][S10].  This is a first-order
    model choice and the two cannot be averaged: against a 28.4-day national mean stay
    the floor is invisible, against a 2.4-day 白内障 stay it roughly doubles the payment.
    """
    return bool(model_point()["min_days_5"])


def adv_rider():
    """Whether the 先進医療特約 is attached [S1][S3][S5][S6][S7][S9]."""
    return bool(model_point()["adv_rider"])


def lump_rider():
    """Whether the 入院一時金特約 is attached [S1]; off in the base run.

    It matters economically because it is the market's answer to falling stay lengths:
    as the mean stay falls a per-day benefit shrinks and a per-admission benefit does
    not.
    """
    return bool(model_point()["lump_rider"])


def tokusoku_3dis():
    """Whether the 三大疾病無制限 特則 is elected [S1][S2]; off in the base run.

    Elected at issue and never cancellable.  For がん, 心疾患 and 脳血管疾患 the
    per-hospitalization limit is 無制限 and those days sit **outside** the 通算 count,
    which defers the benefit-driven termination.  Lifetime cancer incidence in Japan is
    about 61.1% for men and 50.1% for women [REG-R28], so this is a mass-market feature
    rather than a fringe option.
    """
    return bool(model_point()["tokusoku_3dis"])


def waiver_3dis():
    """Whether the 特定三疾病保険料払込免除特則 is elected [S1]; off in the base run.

    When elected, premiums are waived **for life** on a first がん diagnosis, on
    急性心筋梗塞 or on 脳卒中 under the conditions the 特則 sets [S1] — which is why
    :func:`waived` is an absorbing state rather than a two-state chain.
    """
    return bool(model_point()["waiver_3dis"])


def surg_after_limit():
    """Whether in-hospital surgery is paid once ``L1`` is exhausted; **true** in the base.

    A genuine contradiction between carriers, not a gap: one carrier pays at the
    in-hospital multiple [S4] and another pays nothing at all [S10].  The composite pays
    [S4] — the only positively stated treatment among the retrieved 約款 — and carries
    the alternative as this switch.  See :func:`surg_ih_eff`.
    """
    return bool(model_point()["surg_after_limit"])


def pols_if_init():
    """The initial in-force probability: 1.0.

    One policy at a time, projected on an expected basis, so ``pols_if`` is a
    probability rather than a count and no aggregation logic is specified.
    """
    return 1.0


# --- Structure and the projection horizon ----------------------------------

def omega_age():
    """The terminal age of the mortality basis: 116 male, 118 female [REG-R18][REG-R20].

    Read off ``mort_table.csv`` rather than hard-coded, so that replacing the table
    replaces the horizon with it.
    """
    return int(data.mort_table().loc[sex()].index.max())             # noqa: F821


def expiry_age():
    """The 定期 flag's final expiry age: the last ten-year renewal completing by 80.

    Cover renews automatically at the renewal-date age and rate scale, and the 通算
    aggregate limit and the 先進医療 cap run **across** renewals [S7][S10].  The reading
    of 「renewable to age 80」 as *the last renewal whose term completes at or before 80*
    is **[std]**.  Meaningless on the 終身 chassis, which is why it raises there.
    """
    if chassis() != "teiki":
        raise ValueError("expiry_age applies to the teiki chassis only")
    n = (teiki_expiry_age - issue_age()) // teiki_renewal_term       # noqa: F821
    if n < 1:
        raise ValueError("issue age leaves no complete renewal term")
    return issue_age() + n * teiki_renewal_term                      # noqa: F821


def proj_len():
    """The number of projected policy months.

    終身: ``12 x (omega_age() - x + 1)`` — 924 months on the anchor cell, the whole of
    life to the terminal age of the mortality basis, with no maturity benefit and no
    満期保険金 at it [S1][S6].  定期: ``12 x (expiry_age() - x)``.

    On the 定期 flag the ten-year renewal reprices, which would ordinarily close the
    contract boundary at each renewal — but where the policy is on premium waiver the
    supervisory guideline requires the reserve to be computed as though every automatic
    renewal to final expiry occurs [REG-R14].  The two treatments point in opposite
    directions; ``jplib`` projects to final expiry and records the tension rather than
    resolving it.
    """
    if chassis() == "teiki":
        return 12 * (expiry_age() - issue_age())
    return 12 * (omega_age() - issue_age() + 1)


def age(t):
    """The attained 満年齢 in policy month t: ``x + floor(t / 12)`` [S4][S10]."""
    return issue_age() + t // 12


def policy_year(t):
    """y(t): the policy year containing month t, ``floor(t / 12) + 1``."""
    return t // 12 + 1


def prem_end_month():
    """The first policy month in which no premium is payable.

    ``proj_len()`` under 終身払, so a premium falls in every projected month; under the
    65歳払済 variant the month of the 契約応当日 at age 65.
    """
    if prem_period_type() == "to_65":
        m = 12 * (prem_period_end_age - issue_age())                 # noqa: F821
        if m <= 0:
            raise ValueError("prem_period to_65 needs an issue age below 65")
        return min(m, proj_len())
    return proj_len()


# --- Mortality --------------------------------------------------------------

def mort_rate_at_age(x):
    """The **[std]** table rate at integral age ``x`` for this model point's sex.

    ``mort_table.csv`` is a documented proxy for 第三分野標準生命表2018, not a copy of
    it: the publisher's terms prohibit reproduction and transmission without written
    consent [REG-R21].  It is the library-wide canonical construction — log-linear
    between the sourced anchors and exact at every one of them, so male ``q40`` is
    exactly the 0.00076 the technical notes quote [R4][REG-R18] — and the same cell
    carries the same value in every ``jplib`` product that ships it.  Ages above the
    terminal age take the terminal rate.
    """
    a = min(int(x), omega_age())
    return float(data.mort_table().loc[(sex(), a), "mort_rate"])     # noqa: F821


def mort_rate_base(t):
    """The **valuation** table rate at the age read in policy month t.

    ``age_basis_offset`` is 0 in the base run, so the table is read at the contract's own
    満年齢 [S4][S10] even though 第三分野標準生命表2018 is constructed for a
    保険年齢方式 (nearest-birthday) basis [R5][REG-R20] — an understatement of the
    valuation age by about half a year, accepted and marked **[std]**.  Setting the
    Reference to 0.5 reads the table at ``age(t) + 0.5`` by linear interpolation between
    integral ages, which is the alternative the notes name.  Half a year sits between the
    projection basis and the valuation basis either way; the point of the switch is that
    it is stated rather than silently absorbed.
    """
    a = age(t) + age_basis_offset                                    # noqa: F821
    lo = int(a // 1)
    frac = a - lo
    if frac == 0.0:
        return mort_rate_at_age(lo)
    return (1.0 - frac) * mort_rate_at_age(lo) + frac * mort_rate_at_age(lo + 1)


def mort_rate(t):
    """The **annual best-estimate** mortality rate applying in policy month t.

    ``mort_be_factor x`` the table rate, capped at 1.  On a morbidity product the valuation
    table's margin runs the *wrong way* for a best estimate: death releases the
    liability, so 第三分野標準生命表2018 is set deliberately **below** national mortality,
    with the risk-theory adjustment bounded below at 70% and above at 85% of the
    pre-adjustment rate [R5][REG-R20].  ``mort_be_factor = 1.25`` **[std]** is the reciprocal of
    0.80, a round value inside that band and a little above its 0.775 midpoint, so the
    factor unwinds the table's stated margin and nothing more; the band's own endpoints
    would give 1.176 and 1.429.
    At age 40 male it gives 0.00095, between 第三分野標準生命表2018's 0.00076 and
    生保標準生命表2018（死亡保険用）'s 0.00118 [R4][REG-R18], which is the direction sanity
    requires.

    Using the table unadjusted would *overstate* the liability, because an understatement
    of mortality on a health product overstates it — a conservative error in the
    reserving direction, and a material one over a projection this long.
    """
    return min(1.0, mort_be_factor * mort_rate_base(t))                    # noqa: F821


def mort_rate_mth(t):
    """q(t): the monthly mortality rate, ``1 - (1 - mort_rate(t))^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


# --- Lapse ------------------------------------------------------------------

def lapse_rate(t):
    """The **annual** lapse rate in the policy year containing month t **[std]**.

    9.0 / 7.0 / 6.0 / 5.5 / 5.0 percent, 4.5% in years 6-20 and 3.0% from year 21.  The
    only published industry-wide Japanese persistency figure is 解約・失効率 5.6% p.a. on
    個人保険, measured on **opening in-force sum assured** [REG-R31] — a
    sum-assured-weighted rate on a book dominated by 定期 and 終身 death cover, which a
    医療保険 with no sum assured cannot even enter — and no Japanese durational lapse
    curve is public.  The table is anchored to that figure by construction: its first ten
    years average 5.5%.

    The step down at year 21 is **[std]** reasoning stated openly: on a contract with no
    surrender value and rising morbidity exposure, a long-duration policyholder has no
    cash incentive to lapse and a growing reason not to.  Policy years beyond the table
    take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def lapse_rate_mth(t):
    """w(t): the monthly lapse rate, ``1 - (1 - lapse_rate(t))^(1/12)`` **[std]**.

    Applied at the end of month t, **after** mortality [std order].  A lapse pays nothing
    on the 終身払 anchor: there is no surrender value at any duration, and neither
    契約者貸付 nor 自動振替貸付 is offered, so nothing carries a policy through a missed
    premium [S1][S6][S9].  The base run applies the lapse in the month the premium is
    missed and does not model the one-month 払込猶予期間 lag [S1][S4][S10]
    **[std scope]**; on an undiscounted projection that is a one-month timing effect.

    復活 (reinstatement) is available within a year at the composite [S4][S9], but a
    reinstated policy is **not** the policy that lapsed — the 責任開始期 for
    pre-existing-condition tests resets to the 復活日 and the waiting periods re-run from
    it — so it belongs in the model as a *new model point*, and lapse is treated as
    absorbing **[std scope]**.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_cum(t):
    """w_cum(t): the cumulative lapse proportion of the original cohort before month t.

    A proportion of :func:`pols_if_init`, not a running total of :func:`lapse_rate`, and
    it drives a loading on **morbidity** rather than on lapse.  Zero in the first month.
    """
    if t <= 0:
        return 0.0
    return lapse_cum(t - 1) + pols_lapse(t - 1) / pols_if_init()


def sel_lapse_factor(t):
    """The anti-selective lapse loading on **morbidity** in month t **[std]**.

    ``1 + lam max(0, w_cum(t) - w_ref)``, with ``sel_lapse_lambda = 0`` in the base run,
    where it returns 1 in every month.  Healthy lives lapse first, so the persisting
    block is progressively impaired on the *morbidity* basis rather than the mortality
    one — the reverse of the term assurance case, where the loading falls on mortality.
    No Japanese selective-lapse evidence was retrieved, so both the shape and the level
    are standardizations.
    """
    return 1.0 + sel_lapse_lambda * max(                             # noqa: F821
        0.0, lapse_cum(t) - sel_lapse_ref)                           # noqa: F821


# --- Morbidity: incidence ---------------------------------------------------

def inc_band(t):
    """The five-year 入院受療率 band containing ``age(t)``, keyed by its lower edge."""
    idx = data.incidence_table().index                               # noqa: F821
    a = age(t)
    return int(max(b for b in idx if b <= a))


def inc_rate_base(t):
    """The **annual** hospitalization incidence per life at ``age(t)`` **[std]**.

    The construction that makes this model buildable at all.  There is no published
    morbidity table in Japan — 日本アクチュアリー会 publishes the mortality basis only
    [R4][REG-R23] and every insurer's 危険発生率 is its own, unpublished [REG-R2] — so
    incidence is built from 患者調査, a 基幹統計 of 厚生労働省, in three steps:

    1. 入院受療率 is a point-in-time **prevalence** per 100,000 population, the expected
       proportion of the population in hospital on the census day [R6][REG-R26].  It is
       *not* an incidence rate, and treating it as one, or multiplying it straight by a
       daily amount, is the single commonest error in a Japanese medical model.
    2. 退院患者平均在院日数 gives the mean stay for the age band [R6][REG-R27].
    3. In a stationary population person-days in hospital per year equal admissions x
       mean stay, so the **[std]** conversion — flagged as needed by [REG-R26] itself —
       is ``inc = (juryoritsu / 100,000) x 365 / alos``.

    At age 40 that is ``0.00258 x 365 / 20.2 = 0.046619`` per year; at 90 and over it is
    0.6452 — a factor of 13.8, which is the 受療率 ratio of 24.3 damped by the
    平均在院日数 ratio 20.2 / 35.5, because a longer stay turns the same prevalence into
    fewer admissions [REG-R26][REG-R27].  Every five-year 受療率 band the model needs is
    published and is carried sourced; only the sex factor is **[std]**, because the 概況
    publishes 入院受療率 by sex for all ages and by age band for both sexes combined but
    not the age x sex cross-tabulation, which lives in an e-Stat table that was not
    downloaded [R6][R7][REG-R33].
    """
    row = data.incidence_table().loc[inc_band(t)]                    # noqa: F821
    f = float(row["inc_factor_m" if sex() == "M" else "inc_factor_f"])
    return (float(row["juryoritsu_per_100k"]) / 100000.0
            * 365.0 / float(row["alos_days"]) * f)


def inc_rate(t):
    """The **annual** effective incidence in month t: the table rate, loaded.

    Equal to :func:`inc_rate_base` in the base run, where the anti-selective lapse module
    is off.
    """
    return inc_rate_base(t) * sel_lapse_factor(t)


def inc_rate_mth(t):
    """i(t): the monthly hospitalization incidence per in-force policy.

    ``inc_rate(t) / 12`` **[std]** — uniform within the policy year, not a compounded
    twelfth, because an incidence is a count per unit time and not a probability of
    survival.
    """
    return inc_rate(t) / 12.0


# --- Morbidity: length of stay and the day limits ---------------------------

def los_band(t):
    """The broad 平均在院日数 band containing ``age(t)``, keyed by its lower edge.

    Four bands, because that is the granularity 退院患者平均在院日数 is published at,
    against the five-year bands of 受療率 — the band mapping is itself **[std]**
    [REG-R26][REG-R27].
    """
    idx = data.los_table().index                                     # noqa: F821
    a = age(t)
    return int(max(b for b, _ in idx if b <= a))


def los_days(band):
    """g_j: the stay-length day values of a length-of-stay band, ascending.

    (2, 8, 20, 45, 160) at every age **[std]**: the 2-day band stands for the day-surgery
    mode and the 160-day band for the psychiatric and neurological tail that drives the
    sourced national mean [REG-R27].
    """
    return tuple(int(d) for d in data.los_table().loc[band].index)   # noqa: F821


def los_probs(band):
    """pi_j: the probabilities of a length-of-stay band, summing to 1 **[std]**.

    Solved so that the row mean equals the sourced 平均在院日数 for that band exactly
    [REG-R27].  The *shape* is a standardization and it matters more than the mean it
    reproduces: 患者調査 publishes the stay distribution in 32 bands by age band and
    cause, but those e-Stat CSVs were not downloaded [R7][REG-R33], and the sourced
    per-cause means run from 白内障 2.4 days to 精神及び行動の障害 290.4 days — a
    distribution with the same mean and a fatter tail changes the capped expectation
    without changing the calibration target at all.
    """
    return tuple(float(p) for p in data.los_table().loc[band]["prob"])  # noqa: F821


def min_days_floor():
    """F: the five-day minimum floor in days, 5 when elected and 0 otherwise.

    It is a floor on the **amount** — 「入院給付金日額×5」 [S4][S6][S7] — so it enters
    :func:`d_ben` and never :func:`d_pay`, and therefore never the 通算 ledger.
    """
    return 5.0 if min_days_5() else 0.0


def d_raw(t):
    """Sum_j pi_j g_j: the **uncapped** mean stay in days at ``age(t)``.

    20.2 days on the anchor cell's 35-64 row, 35.5 on the 65+ row — the sourced
    平均在院日数 that :func:`los_probs` is calibrated to [REG-R27].
    """
    b = los_band(t)
    return sum(p * g for g, p in zip(los_days(b), los_probs(b)))


def d_pay_capped(t):
    """Sum_j pi_j min(g_j, L1): expected paid days per hospitalization after ``L1``.

    The per-hospitalization limit is applied **inside** the stay expectation, spell by
    spell, before anything else.  15.20 days on the anchor cell against an uncapped 20.20
    — the 60-day cap removes 24.75% of raw days, and 33.8% on the 65+ row.  Capping the
    *mean* instead would give ``min(20.20, 60) = 20.20`` and remove the limit silently.
    """
    b = los_band(t)
    return sum(p * min(g, limit_per_hosp())
               for g, p in zip(los_days(b), los_probs(b)))


def d_ben_capped(t):
    """Sum_j pi_j max(F, min(g_j, L1)): expected **benefit** days after ``L1``.

    The five-day floor enters here and nowhere else.  With ``F = 5`` the anchor's 35-64
    row gives 16.10 benefit days against 15.20 paid days: the floor adds 0.90 days of
    benefit and **zero days** to the 通算 ledger.
    """
    b = los_band(t)
    f = min_days_floor()
    return sum(p * max(f, min(g, limit_per_hosp()))
               for g, p in zip(los_days(b), los_probs(b)))


def d_ben_raw(t):
    """Sum_j pi_j max(F, g_j): expected benefit days with **no** ``L1`` at all.

    Used only by the 三大疾病無制限 特則, for which the per-hospitalization limit is
    removed [S1][S2].
    """
    b = los_band(t)
    f = min_days_floor()
    return sum(p * max(f, g) for g, p in zip(los_days(b), los_probs(b)))


def share_free():
    """The share of hospitalizations exempt from both day limits **[std]**; 0 in the base.

    Zero unless the 三大疾病無制限 特則 is elected, in which case ``share_3dis`` of
    hospitalizations — がん, 心疾患 and 脳血管疾患 — carry no ``L1`` and consume no 通算
    days [S1][S2].  ``share_3dis`` is a standardization with **no observed range**: no
    cause split of 入院受療率 was extracted in the research pass [R7][REG-R33].  It is a
    share of *spells*, not of days.
    """
    return share_3dis if tokusoku_3dis() else 0.0                    # noqa: F821


def d_pay(t):
    """d_pay: the expected days per hospitalization that **consume the 通算 ledger**.

    :func:`d_pay_capped` on the anchor cell.  Under the 三大疾病無制限 特則 the exempt
    share is removed, because those days sit outside the 通算 count entirely.
    """
    return (1.0 - share_free()) * d_pay_capped(t)


def d_ben_free(t):
    """The expected benefit days per hospitalization outside the 通算 count; 0 in the base."""
    return share_free() * d_ben_raw(t)


def d_ben_ltd(t):
    """The expected benefit days per hospitalization inside the 通算 count.

    :func:`d_ben_capped` on the anchor cell, where nothing is exempt.
    """
    return (1.0 - share_free()) * d_ben_capped(t)


def d_ben(t):
    """d_ben: the expected **benefit** days per hospitalization, before the 通算 cap.

    ``d_ben_free(t) + d_ben_ltd(t)``, which collapses to :func:`d_ben_capped` whenever
    the 三大疾病無制限 特則 is not elected.  Always at least :func:`d_pay`, which
    :func:`check_day_limits` asserts.
    """
    return d_ben_free(t) + d_ben_ltd(t)


def room_dis(t):
    """The days left on the 疾病 limb's 通算 ledger at the start of month t: ``max(0, LA - A_dis)``."""
    return max(0.0, limit_agg() - agg_days_dis(t))


def room_acc(t):
    """The days left on the 災害 limb's 通算 ledger at the start of month t: ``max(0, LA - A_acc)``."""
    return max(0.0, limit_agg() - agg_days_acc(t))


def d_pay_dis(t):
    """d_pay_dis(t) = min(d_pay(t), room_dis(t)): ledger-capped paid days, 疾病 limb."""
    return min(d_pay(t), room_dis(t))


def d_pay_acc(t):
    """d_pay_acc(t) = min(d_pay(t), room_acc(t)): ledger-capped paid days, 災害 limb."""
    return min(d_pay(t), room_acc(t))


def d_ben_dis(t):
    """The 疾病 limb's benefit days after the 通算 cap **[std proportional scaling]**.

    ``d_ben x d_pay_dis / d_pay`` on the anchor cell, exactly as the notes write it.  The
    exempt share of the 三大疾病無制限 特則 is added back unscaled, because those days do
    not depend on the ledger at all.
    """
    dp = d_pay(t)
    if dp <= 0.0:
        return d_ben_free(t)
    return d_ben_free(t) + d_ben_ltd(t) * d_pay_dis(t) / dp


def d_ben_acc(t):
    """The 災害 limb's benefit days after the 通算 cap **[std proportional scaling]**.

    The 災害 limb pays the **same** daily amount on the same length-of-stay distribution
    [S1][S4][S9][S10]; admission must begin within 180 days of the accident.  In the base
    run the split is therefore economically inert in the cash flows and structurally
    essential in the ledgers — which is precisely why there are two of them.
    """
    dp = d_pay(t)
    if dp <= 0.0:
        return d_ben_free(t)
    return d_ben_free(t) + d_ben_ltd(t) * d_pay_acc(t) / dp


def agg_days_dis(t):
    """A_dis(t): the 疾病 limb's 通算 ledger in days, **per surviving policy**.

    ``A_dis(t+1) = A_dis(t) + i(t) s_dis d_pay_dis(t)``, unweighted by ``pols_if``.
    Weighting it by the in-force probability would measure the block's consumption rather
    than the policyholder's and defer the limit forever; that is the easiest
    state-variable error in this product.

    On the anchor cell it grows by about 0.709 days a year at age 40 and reaches only
    single-digit hundreds by the terminal age, so ``LA`` never binds — a property of the
    expectation, not of the product, since ``E[min(Sum, LA)] != min(E[Sum], LA)``.
    """
    if t <= 0:
        return 0.0
    return (agg_days_dis(t - 1)
            + inc_rate_mth(t - 1) * s_dis * d_pay_dis(t - 1))        # noqa: F821


def agg_days_acc(t):
    """A_acc(t): the 災害 limb's 通算 ledger in days, **per surviving policy**.

    A separate ledger, because the 通算 limit is applied separately to the two limbs
    [S4][S1].  One combined ledger terminates the contract roughly twice as early.  The
    疾病/災害 split of incidence is **[std]** at 0.92 / 0.08: 損傷・中毒等 is 107 of the
    national 入院受療率 of 945 (11.3%) [REG-R26], and not every 損傷 admission arises from
    an 不慮の事故 with admission inside 180 days [S1][S4][S9][S10].
    """
    if t <= 0:
        return 0.0
    return (agg_days_acc(t - 1)
            + inc_rate_mth(t - 1) * s_acc * d_pay_acc(t - 1))        # noqa: F821


def term_rate(t):
    """term(t): the benefit-driven termination indicator, 0 or 1.

    Cover ceases when **both** the 疾病 and 災害 aggregate limits are exhausted [S9].
    This is a decrement a death-benefit product does not have, and it is why the
    aggregate limit is a tracked state variable rather than a cap applied at the end.
    Identically 0 on every shipped model point's expectation, which is a fact about the
    deterministic grid and not a reason to delete the machinery.
    """
    la = limit_agg()
    return 1.0 if (agg_days_dis(t) >= la and agg_days_acc(t) >= la) else 0.0


# --- 先進医療 ---------------------------------------------------------------

def adv_freq_mth():
    """f_adv: the monthly 先進医療 frequency per life **[std]**, flat across ages.

    0.00040 per life-year.  No public exposure denominator was retrieved, so it carries
    no observed range.  Zero when the rider is not attached.
    """
    return (adv_freq / 12.0) if adv_rider() else 0.0                 # noqa: F821


def adv_pay_pp(t):
    """pay(t) = min(S_adv, LV - V(t)): the 技術料 reimbursed per 療養, before the top-up.

    The 先進医療特約 reimburses the 技術料 in full, up to a lifetime aggregate of
    ¥20,000,000 — the **¥20,000,000 cap is uniform** at every carrier that publishes one
    [S1][S3][S5][S6][S7][S9], one of the few genuinely market-wide parameters in the
    product — and the rider terminates on reaching it [S1][S5].

    ``adv_sev`` = ¥150,000 is **[std]**.  The sourced anchors: in 令和5年度, 144,282
    patients received 先進医療 across 81 technologies; 先進医療A averaged about ¥67,700
    per case, while 陽子線治療 ran to about ¥2,660,000 over 824 cases and 重粒子線治療 to
    about ¥3,140,000 over 462 cases [R9].  A count-weighted mean of those three is about
    ¥92,300, but the A count is dominated by high-volume fertility technologies whose
    exposure is not this rider's, so the [std] severity sits about 1.6x above it.  The
    spread the tag stands over is a **factor of 46** between the 先進医療A average per case
    and 重粒子線治療's [R9]; no per-technology minimum was extracted, so the true spread
    is wider still.

    Eligibility is tested at the treatment date, so a technology that has left the
    厚生労働大臣's 先進医療 list pays nothing, and 患者申出療養 is a different scheme and is
    excluded [S1][S5][S6] — both scope facts, not modelled states.
    """
    return min(adv_sev, max(0.0, adv_cap - adv_paid(t)))             # noqa: F821


def adv_claim_pp(t):
    """adv_claim(t): the 先進医療 claim per in-force policy in month t.

    ``f_adv x [pay(t) + min(0.10 pay(t), 500,000)]``.  The 10% / ¥500,000 cash top-up is
    the middle of three market shapes and is **[std]** composite [S1]; the reimbursement
    limb itself is contractual.
    """
    pay = adv_pay_pp(t)
    return adv_freq_mth() * (
        pay + min(adv_topup_rate * pay, adv_topup_cap))              # noqa: F821


def adv_paid(t):
    """V(t): the 先進医療 ledger in JPY, **per surviving policy**, against ``LV``.

    ``V(t+1) = V(t) + f_adv pay(t)``.  Only the reimbursed 技術料 counts against the
    lifetime cap; the cash top-up does not.  Never approached on the expectation — about
    ¥60 a year on the anchor cell against a ¥20,000,000 cap — which is a fact about the
    deterministic grid, exactly as for the day ledgers.
    """
    if t <= 0:
        return 0.0
    return adv_paid(t - 1) + adv_freq_mth() * adv_pay_pp(t - 1)


# --- 入院一時金特約 ---------------------------------------------------------

def lump_claims_pp(t):
    """The number of 入院一時金 payments per in-force policy in month t.

    One payment per hospitalization, cause-blind, with the same 181st-day reset as the
    main contract, subject to a 通算 count limit of 50 [S1] **[std]**.  Zero unless the
    rider is attached.
    """
    if not lump_rider():
        return 0.0
    return min(inc_rate_mth(t), max(0.0, lump_max_count - lump_count(t)))  # noqa: F821


def lump_count(t):
    """The 入院一時金 通算 count ledger, **per surviving policy**, against 50 payments.

    Carried on the same basis as the day ledgers and for the same reason: a count
    weighted by the in-force probability would defer the 通算50回 limit indefinitely.
    """
    if t <= 0:
        return 0.0
    return lump_count(t - 1) + lump_claims_pp(t - 1)


# --- 保険料払込免除 ---------------------------------------------------------

def waiver_inc_mth(t):
    """The monthly 保険料払込免除 incidence **[std]**; **zero in the base run**.

    The base contractual waiver is disability-triggered — 高度障害状態 from any cause, or
    a listed 身体障害の状態 from an 不慮の事故 within 180 days [S1][S2][S10] — and its
    incidence is zero in **every** run of this model, not merely the base one, because
    第三分野標準生命表2018 **excludes 高度障害** [R5][REG-R20] so the incidence cannot be
    read out of the mortality basis, and no public Japanese 高度障害 incidence table was
    retrieved.  A model that reads it out of the table under-counts the waiver.

    Where the 特定三疾病保険料払込免除特則 is elected the module switches on at the notes'
    suggested placeholder, ``waiver_inc_mult x mort_rate(t)`` a year.  Zero after the
    premium-paying period, when there is nothing left to waive.
    """
    if not waiver_3dis() or t >= prem_end_month():
        return 0.0
    return waiver_inc_mult * mort_rate(t) / 12.0                     # noqa: F821


def waived(t):
    """The probability the policy is on 保険料払込免除 at the start of month t.

    An **absorbing** state, ``u(t+1) = u(t) + (1 - u(t)) inc(t)``: the 特則 waives
    premiums for life once triggered [S1], so there is no recovery limb.  Zero throughout
    the base run.  Mortality and lapse are assumed independent of the waiver state
    **[std]**, which is what lets the waived population be carried as a fraction of the
    in-force rather than as a separate decrement.
    """
    if t <= 0:
        return 0.0
    u = waived(t - 1)
    return u + (1.0 - u) * waiver_inc_mth(t - 1)


# --- In force ---------------------------------------------------------------

def pols_if(t):
    """l(t): the in-force probability at the **start** of policy month t.

    1 at ``t = 0``, then ``l(t+1) = l(t)(1 - q(t))(1 - w(t))(1 - term(t))``.  This is the
    weight on every cash flow of the same ``result_cf()`` row.  Zero outside
    ``0 .. proj_len() - 1``.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The in-force probability at a point inside policy month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before lapses — the notes' processing order is **mortality then
        lapse** **[std order]**, so this is the population lapses are taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state: what is left once the month's deaths, lapses and
        benefit-driven termination are taken, and zero in the final projected month
        because the cover ends there.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        if t < 0 or t >= proj_len() - 1:
            return 0.0
        return (pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
                * (1.0 - term_rate(t)))
    raise ValueError("invalid timing")


def pols_death(t):
    """Expected deaths at the end of policy month t.

    A pure liability release: the main contract pays **nothing** on death [S1][S4][S6]
    [S9][S10], so there is no ``claims_death`` anywhere in this model.  A death benefit
    column on a 医療保険 is a benefit that does not exist.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Expected lapses at the end of policy month t, taken from the survivors of mortality.

    Pays nothing on the 終身払 anchor — see :func:`cv_pp` — so on that model point this
    moves :func:`pols_if` and nothing else.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_term(t):
    """Expected benefit-driven terminations at the end of policy month t.

    Cover ceases when **both** 通算 limbs are exhausted [S9].  Zero on every shipped
    model point's expectation; see :func:`term_rate`.
    """
    return (pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
            * term_rate(t))


def pols_maturity(t):
    """Policies whose cover ends at the scheduled end of the contract.

    The library-wide meaning: the count whose cover ends because the contract reaches
    its scheduled end, whether or not anything is paid for it.  Nothing is paid here —
    the 定期 flag simply runs out at its final renewal, with no maturity value
    [S7][S10], so there is no ``claims(t, "MATURITY")`` limb — but the count is needed
    for the in-force roll-forward to close.  On the 終身 chassis there is no scheduled
    end at all and this is zero even in the final month, because the projection stops
    where the mortality table does and everybody has already died.
    """
    if t != proj_len() - 1:
        return 0.0
    return (pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
            * (1.0 - term_rate(t)))


def pols_payer(t):
    """The in-force probability actually paying premium in policy month t.

    ``l(t) (1 - waived(t))``.  Equal to :func:`pols_if` throughout the base run, where
    the waiver module is off.
    """
    return pols_if(t) * (1.0 - waived(t))


# --- Cash flows -------------------------------------------------------------

def premiums(t):
    """Premium income at the **start** of policy month t, an inflow.

    ``P l(t) (1 - waived(t))``, and zero from :func:`prem_end_month` on.  Level and
    無配当 with no repricing right on the 終身 chassis [S3][S6][S8]; on the 定期 flag the
    ten-year renewal reprices and the base run holds the issue rate flat **[std]**.
    """
    if t >= prem_end_month():
        return 0.0
    return premium_mth_pp() * pols_payer(t)


def cv_pp(t):
    """The 解約返戻金 per policy at the end of month t; **zero under 終身払** [S1][S6][S9].

    Every carrier examined writes no surrender value during the premium-paying period,
    and under 終身払 that is every duration.  Where a 短期払 is chosen a small value
    appears afterwards, standardized across two carriers at **10 x 入院給付金日額**
    [S1][S6] — the single route by which this chassis ever acquires one, and the reason
    :func:`claims` carries a ``"LAPSE"`` kind at all.
    """
    if prem_period_type() == "to_65" and t >= prem_end_month():
        return cv_mult_short_pay * daily_amount()                    # noqa: F821
    return 0.0


def surg_ih_eff(t):
    """The in-hospital surgeries per hospitalization actually payable **[std]**.

    ``s_ih`` when ``surg_after_limit`` is true — the composite's position, and the only
    positively stated treatment among the retrieved 約款 [S4].  With the switch reversed
    [S10], and surgeries assumed uniform over stay-days **[std]**, the truncated day
    fraction ``1 - d_pay_capped / d_raw`` — 24.75% on the anchor cell — of in-hospital
    surgeries falls outside cover.

    ``s_ih = 0.35`` and ``s_op = 0.15`` are **[std]**: 患者調査 crosses 推計退院患者数
    with 手術の有無, giving a public in-hospital surgery proportion, but those CSVs were
    not downloaded [R7][REG-R33].  Radiation therapy is **inside** these frequencies and
    not a separate stream: the composite folds 放射線治療 into 手術給付金 through the
    放射線治療料 limb of the trigger, subject to the 60-day lockout every carrier imposes
    [S1][S2][S6][S9][S10].  Adding a separate 放射線治療給付金 double-counts.
    """
    if surg_after_limit():
        return surg_ih_per_hosp                                      # noqa: F821
    raw = d_raw(t)
    if raw <= 0.0:
        return 0.0
    return surg_ih_per_hosp * d_pay_capped(t) / raw                  # noqa: F821


def claims(t, kind=None):
    """Benefit outgo at the **end** of policy month t, by kind; the total when omitted.

    ``"HOSP"``
        入院給付金: ``l(t) D i(t) [s_dis d_ben_dis(t) + s_acc d_ben_acc(t)]``.  A
        hospitalization *starting* in month t is resolved in full in month t **[std]** —
        its paid days, its benefit and its consumption of both day limits are all
        recognised at t — because the per-hospitalization limit is a property of the
        whole spell and a grid that split the spell would have to carry a partial-spell
        state.

    ``"SURGERY"``
        手術給付金: ``l(t) i(t) D [surg_ih_eff(t) m_ih + s_op m_op]``, unlimited in count
        [S1][S3].  ¥38,750 per hospitalization on the anchor cell.

    ``"ADVANCED"``
        先進医療給付金: ``l(t) adv_claim(t)``, reimbursement plus the [std] cash top-up.

    ``"LUMP"``
        入院一時金: ¥100,000 per hospitalization while the 通算50回 count lasts; zero
        unless the rider is attached.

    ``"LAPSE"``
        the surrender value paid on lapse — **identically zero** under 終身払, which is
        every shipped model point but one.  The kind exists so that the zero is stated
        rather than left to inference: it is the product fact, and a non-zero lapse row
        imported from a cash-value model is one of the notes' pitfalls.
    """
    if kind is None:
        return sum(claims(t, k)
                   for k in ("HOSP", "SURGERY", "ADVANCED", "LUMP", "LAPSE"))
    if kind == "HOSP":
        return (pols_if(t) * daily_amount() * inc_rate_mth(t)
                * (s_dis * d_ben_dis(t) + s_acc * d_ben_acc(t)))     # noqa: F821
    if kind == "SURGERY":
        return (pols_if(t) * inc_rate_mth(t) * daily_amount()
                * (surg_ih_eff(t) * surg_mult_ih()
                   + surg_op_per_hosp * surg_mult_op()))             # noqa: F821
    if kind == "ADVANCED":
        return pols_if(t) * adv_claim_pp(t)
    if kind == "LUMP":
        return pols_if(t) * lump_amount * lump_claims_pp(t)          # noqa: F821
    if kind == "LAPSE":
        return pols_lapse(t) * cv_pp(t)
    raise ValueError("invalid kind")


def expense_maint_pp(t):
    """e(t): the maintenance expense per policy in month t **[std]**.

    ¥250 a month inflating at 1.0% p.a. at each anniversary.  Against a ¥2,100 premium
    that is 11.9% of premium on the anchor cell, and the level premium is fixed for life
    while the expense is not — which is why the notes rate expense inflation a
    first-order lever on a product this small-premium.  No Japanese medical expense scale
    is public, so both the level and the inflation rate are standardizations.
    """
    return expense_maint * (1.0 + inflation_rate) ** (t // 12)       # noqa: F821


def claim_expenses(t):
    """ec i(t) l(t): the claim handling expense on the month's hospitalizations **[std]**.

    ¥3,000 per hospitalization event, covering the day benefit and any surgery on the
    same spell, uninflated.  A cells of its own, **outside** :func:`expenses`: it is
    deducted explicitly in :func:`net_cf` and printed as its own ``claim_expenses``
    column by :func:`result_cf`.
    """
    return expense_claim * inc_rate_mth(t) * pols_if(t)              # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense outgo in policy month t **[std]**.

    The acquisition expense of ¥20,000 per policy at ``t = 0``, then the inflating
    maintenance expense at the start of every month.  Both levels are standardizations:
    no Japanese medical expense scale is public.

    The claim handling expense is **not** in here.  It is :func:`claim_expenses`,
    deducted on its own line in :func:`net_cf` and published in its own column, so that
    ``expenses`` means acquisition + maintenance in every model in the three libraries.
    ``technical-notes.md`` prints the two separately throughout — the worked-example
    table, its three arithmetic traces and the policy-year-1 aggregate all carry both
    lines — so nothing in the notes has to be read as the combined figure.
    """
    acq = expense_acq * pols_if(t) if t == 0 else 0.0                # noqa: F821
    return acq + expense_maint_pp(t) * pols_if(t)


def commissions(t):
    """Commission outgo in policy month t **[std]**.

    1.5 x the annualized premium at ``t = 0`` — ¥37,800 on the anchor cell — then 3.0% of
    premium income from policy year 2, that is from ``t = 12``.  Both levels are
    standardizations; no Japanese commission scale is public.  With the acquisition
    expense they produce the characteristic new-business strain of ¥57,800 at ``t = 0``,
    recovered out of the margin in the early durations.
    """
    init = (comm_init_rate * 12.0 * premium_mth_pp()                 # noqa: F821
            * pols_if(t)) if t == 0 else 0.0
    renew = comm_renewal_rate * premiums(t) if t >= 12 else 0.0      # noqa: F821
    return init + renew


def net_cf(t):
    """net_cf(t): the net cash flow of policy month t, **income positive**.

    Premiums less every benefit limb, less :func:`expenses`, less
    :func:`claim_expenses`, less commission.  The notes' own
    sign, which is also the library-wide convention, so unlike the whole life and payout
    annuity models there is no outgo-positive ``liability_cf`` companion to publish.

    The shape to expect is a deep month-0 strain — ¥57,800 of acquisition expense and
    initial commission against one month's premium — and then thin positive margins that
    thin further with age: on the [std] basis annual incidence runs from 0.0466 at age 40
    to 0.6452 at 90 and over and expected paid days from 0.709 to 15.16, so the level
    premium prefunds a morbidity cost that rises steeply for the whole of life.  Year-1
    claims on the anchor cell are 21.5% of year-1 premium.
    """
    return (premiums(t)
            - claims(t, "HOSP") - claims(t, "SURGERY")
            - claims(t, "ADVANCED") - claims(t, "LUMP") - claims(t, "LAPSE")
            - expenses(t) - claim_expenses(t) - commissions(t))


# --- Checks -----------------------------------------------------------------

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - deaths - lapses - terminations - maturities``.  The
    last two terms are what makes this product's roll-forward different from a term
    assurance's: cover can cease because the 通算 limits are exhausted, and the 定期 flag
    reaches its scheduled end at the final renewal.  Without them the roll-forward would
    appear to lose lives with no cause.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_term(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_agg_days_resid(t):
    """The 通算 day-ledger residual in policy month t; zero everywhere.

    Two terms per limb.  The first restates the recursion — each ledger advances by
    exactly the month's ledger-consuming paid days, **unweighted by** ``pols_if``, which
    is the state-variable error this product invites.  The second is the one that can
    actually fail: ``max(0, A(t+1) - LA)``, the overflow above the aggregate limit, which
    is non-zero the moment the room calculation in :func:`d_pay_dis` or :func:`d_pay_acc`
    is wrong.
    """
    la = limit_agg()
    dis = (agg_days_dis(t + 1) - agg_days_dis(t)
           - inc_rate_mth(t) * s_dis * d_pay_dis(t))                 # noqa: F821
    acc = (agg_days_acc(t + 1) - agg_days_acc(t)
           - inc_rate_mth(t) * s_acc * d_pay_acc(t))                 # noqa: F821
    return (dis + acc
            + max(0.0, agg_days_dis(t + 1) - la)
            + max(0.0, agg_days_acc(t + 1) - la))


def check_agg_days():
    """True when both 通算 day ledgers roll forward and stay inside their limit."""
    return all(abs(check_agg_days_resid(t)) <= roll_fwd_tol          # noqa: F821
               for t in range(proj_len()))


def check_day_limits_resid(t):
    """The day-limit ordering residual in policy month t; zero everywhere.

    The three limits act in a fixed order and this is the identity that says so, summed
    as three non-negative violations:

    * ``max(0, d_pay_capped(t) - L1)`` — the per-hospitalization limit is applied
      **inside** the stay expectation, so no expectation may exceed it.  Capping the mean
      instead of capping each stay would show up here.
    * ``max(0, d_pay(t) - d_ben(t))`` — the five-day minimum is an **amount**, not five
      days, so benefit days are never fewer than ledger days.  A model that credited the
      floor to the 通算 ledger would fail this.
    * ``max(0, d_pay_dis(t) - room_dis(t))`` and the same on the 災害 limb — no month may
      consume more days than its ledger has left.
    """
    return (max(0.0, d_pay_capped(t) - limit_per_hosp())
            + max(0.0, d_pay(t) - d_ben(t))
            + max(0.0, d_pay_dis(t) - room_dis(t))
            + max(0.0, d_pay_acc(t) - room_acc(t)))


def check_day_limits():
    """True when the three day limits act in the notes' order in every projected month."""
    return all(abs(check_day_limits_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_adv_ledger_resid(t):
    """The 先進医療 ledger residual in policy month t; zero everywhere.

    ``V(t+1) - V(t) - f_adv pay(t)`` plus ``max(0, V(t+1) - LV)``, the overflow above the
    ¥20,000,000 lifetime cap.  Only the reimbursed 技術料 counts against the cap — a
    model that also charged the cash top-up to it would exhaust the rider early.
    """
    return (adv_paid(t + 1) - adv_paid(t) - adv_freq_mth() * adv_pay_pp(t)
            + max(0.0, adv_paid(t + 1) - adv_cap))                   # noqa: F821


def check_adv_ledger():
    """True when the 先進医療 ledger rolls forward and stays inside its cap."""
    return all(abs(check_adv_ledger_resid(t)) <= roll_fwd_tol * adv_cap  # noqa: F821
               for t in range(proj_len()))


def check_lump_ledger_resid(t):
    """The 入院一時金 count-ledger residual in policy month t; zero everywhere.

    ``count(t+1) - count(t) - claims_pp(t)`` plus the overflow above the 通算50回 limit.
    Zero by construction where the rider is not attached.
    """
    return (lump_count(t + 1) - lump_count(t) - lump_claims_pp(t)
            + max(0.0, lump_count(t + 1) - lump_max_count))          # noqa: F821


def check_lump_ledger():
    """True when the 入院一時金 count ledger rolls forward and stays inside its limit."""
    return all(abs(check_lump_ledger_resid(t)) <= roll_fwd_tol       # noqa: F821
               for t in range(proj_len()))


def check_waiver_roll_fwd_resid(t):
    """The 保険料払込免除 state residual in policy month t; zero everywhere.

    ``u(t+1) - u(t) - (1 - u(t)) inc(t)`` plus ``max(0, u(t+1) - 1)``.  The state is
    absorbing — the 特則 waives premiums for life [S1] — so a recovery limb appearing
    here would be modelling a contract term that does not exist.
    """
    u = waived(t)
    return (waived(t + 1) - u - (1.0 - u) * waiver_inc_mth(t)
            + max(0.0, waived(t + 1) - 1.0))


def check_waiver_roll_fwd():
    """True when the premium waiver state rolls forward in every projected month."""
    return all(abs(check_waiver_roll_fwd_resid(t)) <= roll_fwd_tol   # noqa: F821
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The cash flow statement residual in policy month t; zero everywhere.

    :func:`net_cf`, which adds the benefit limbs one by one exactly as ``result_cf()``
    prints them, less ``premiums - claims - expenses - claim_expenses - commissions``
    with :func:`claims` summing over its own kinds.  A benefit limb present in the total
    but missing from the printed statement, or counted twice, shows up here; so does a
    claim expense folded back into :func:`expenses` instead of standing on its own line.
    """
    return net_cf(t) - (premiums(t) - claims(t) - expenses(t)
                        - claim_expenses(t) - commissions(t))


def check_net_cf():
    """True when the printed cash flow statement adds to ``net_cf`` in every month."""
    return all(abs(check_net_cf_resid(t)) <= cash_tol                # noqa: F821
               for t in range(proj_len()))


# --- Result tables ----------------------------------------------------------

def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month in-force probability, which is the weight applied
    to every cash flow on the same row.  ``net_cf`` carries the notes' own
    income-positive sign.  ``expenses`` is acquisition + maintenance only and the claim
    handling expense stands beside it in its own ``claim_expenses`` column, which is what
    the two names mean library-wide.  ``claims_lapse`` is a column of zeros by product
    design on
    every 終身払 model point — there is no surrender value — and is published rather than
    dropped; see the Space docstring.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_hosp": [claims(t, "HOSP") for t in ts],
            "claims_surgery": [claims(t, "SURGERY") for t in ts],
            "claims_advanced": [claims(t, "ADVANCED") for t in ts],
            "claims_lump": [claims(t, "LUMP") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements and decrement rates, indexed by policy month t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_term": [pols_term(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_payer": [pols_payer(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "inc_rate": [inc_rate(t) for t in ts],
            "waived": [waived(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_days():
    """Result table of the benefit-day and rider ledgers, indexed by policy month t.

    The ledgers are **per surviving policy** and carry no ``pols_if`` weighting, so this
    table reads as one policyholder's consumption of the 通算 limits and not as the
    block's.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "d_pay": [d_pay(t) for t in ts],
            "d_ben": [d_ben(t) for t in ts],
            "agg_days_dis": [agg_days_dis(t) for t in ts],
            "agg_days_acc": [agg_days_acc(t) for t in ts],
            "adv_paid": [adv_paid(t) for t in ts],
            "lump_count": [lump_count(t) for t in ts],
            "term_rate": [term_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 1.25

age_basis_offset = 0.0

s_dis = 0.92

s_acc = 0.08

surg_ih_per_hosp = 0.35

surg_op_per_hosp = 0.15

adv_freq = 0.0004

adv_sev = 150000.0

adv_topup_rate = 0.1

adv_topup_cap = 500000.0

adv_cap = 20000000.0

lump_amount = 100000.0

lump_max_count = 50.0

share_3dis = 0.3

sel_lapse_lambda = 0.0

sel_lapse_ref = 0.2

waiver_inc_mult = 0.25

cv_mult_short_pay = 10.0

prem_period_end_age = 65

teiki_expiry_age = 80

teiki_renewal_term = 10

expense_acq = 20000.0

expense_maint = 250.0

expense_claim = 3000.0

inflation_rate = 0.01

comm_init_rate = 1.5

comm_renewal_rate = 0.03

roll_fwd_tol = 1e-10

cash_tol = 1e-06

pd = ("Module", "pandas")
