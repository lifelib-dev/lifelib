# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.IUL_US_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_av()          # the account value roll-forward
    >>> Projection[1].result_seg()         # the segment ladder
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/indexed_ul/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IUL_US_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers live in the unparameterized :mod:`~.IUL_US_S.Data` Space, reached here
through the ``data`` Reference, so each file is read once per model rather than once
per model point:

======================  ================================  ==========================
Reference (on Data)     Cells                             File
======================  ================================  ==========================
model_point_file        data.model_point_table()          model_point_table.csv
coi_rates_file          data.coi_rates()                  coi_rates.csv
corridor_file           data.corridor_factors()           corridor_factors.csv
mort_table_file         data.mort_table()                 mort_table.csv
class_factor_file       data.class_factor_table()         class_factor_table.csv
lapse_table_file        data.lapse_table()                lapse_table.csv
surr_charge_file        data.surr_charge_table()          surr_charge_table.csv
======================  ================================  ==========================

The index path is **not** a file. The base deterministic run generates
:func:`index_level` from a level annual return, and a historical or simulated path is
substituted by overriding that one cells.

.. rubric:: Projection basis

``t`` counts **policy months**, 1-based: ``t = 1`` is the issue month of a
new-business model point, and for an in-force point it is the first projected month,
sitting ``duration_mth_init()`` completed months after issue. State variables the
notes define at their own ``t = 0`` -- ``FA(0)``, ``S(0)``, ``L(0)``, ``l(0) = 1`` --
are the ``t == 0`` branch of the corresponding recursion. The notes' own month index
is therefore :func:`duration_mth`, not ``t``.

Within each month the notes' monthiversary order is followed exactly:

1. **Anniversary resets and premium.** The attained age and the corridor factor move
   on the policy anniversary (:func:`age`, :func:`corridor_factor`); the annual
   premium is received at BOM of the first month of each policy year and its load
   deducted (:func:`premium_pp`, :func:`prem_to_av_pp`), the net premium going to the
   fixed account.
2. **Segment maturity.** A segment created twelve months earlier matures: its index
   credit is computed (:func:`index_credit_pp`) and its whole value rolls into the
   fixed account (:func:`seg_roll_pp`), from which the sweep at step 6 re-enters it
   into a new segment under the standing instruction **[std]**.
3. **Withdrawals and new loans** are sourced fixed-account-first, then pro rata across
   live segments [S3] (:func:`draw_from_fa_pp`, :func:`draw_from_seg_pp`); loan
   collateral moves into :func:`lca_pp`.
4. **Death benefit and corridor** on the post-premium, post-withdrawal account value
   (:func:`db_pp`).
5. **Net amount at risk**, the death benefit discounted one month at the
   **guaranteed** rate less the account value measured **before** the deduction
   (:func:`net_amt_at_risk`) -- the universal life base convention.
6. **Monthly deduction** (:func:`mth_deduction_pp`), sourced the same way as step 3
   (:func:`mth_deduction_from_fa_pp`, :func:`mth_deduction_from_seg_pp`), then the
   shortfall / no-lapse test (:func:`is_shortfall`).
7. **Sweep.** ``w_ix`` times the remaining fixed-account balance creates the new
   segment of this month (:func:`sweep_pp`, :func:`seg_new_pp`).
8. **Interest, EOM.** One month at the fixed-account rate on the post-sweep fixed
   balance and at the loan collateral rate on the collateral account
   (:func:`inv_income_pp`); **segments earn no interim interest** [S2]; loan interest
   accrues (:func:`loan_bal_pp`).
9. **Decrements, EOM**, death before lapse (:func:`pols_death`, :func:`pols_lapse`).

Cash flows are **undiscounted**. Premiums, expenses and premium taxes fall at BOM and
are weighted by :func:`pols_if`, the count in force at the **start** of month ``t``;
death claims by ``pols_if(t) * mort_rate_mth(t)``; surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``; and partial withdrawals by
``pols_if(t)`` again, because a withdrawal is taken at BOM on the owner's election and
is not a decrement.

.. rubric:: Naming

Cells names follow :mod:`~.UL_US_S` -- the chassis these notes defer to -- and
through it lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``: ``pols_*``
for policy counts, ``av_*`` for account values, plural nouns for cash flows, ``*_rate``
for rates, ``*_pp`` for per-policy amounts, ``timing`` and ``kind`` string arguments.
Every concept shared with the chassis carries the chassis name. The names that are new
are the ones the indexed crediting engine needs: the fixed (holding) account, the
segment ladder, the crediting formula, and the no-lapse guarantee test.

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Policy month, 1-based
(notes' own t)             duration_mth(t)                 Completed policy months
y                          policy_year(t)                  Policy year, 1-based
(y - 1)                    duration(t)                     Completed policy years
(issue age)                age_at_entry                    Issue age (ANB)
Sex                        sex                             Sex, M or F
Risk class                 rate_class                      Underwriting class, spec Table 1
DB option                  db_option                       Death benefit option, A or B
Tax test                   qual_test                       IRC 7702 test; only GPT modeled
Premium mode               premium_mode                    ANNUAL **[std]** or MONTHLY
x                          age(t)                          Attained age (ANB)
(none)                     proj_len                        Last projected month
F                          sum_assured                     Initial face amount
F(t)                       sum_assured_at(t)               Face after reductions
F/1000                     units(t)                        Face in $1,000 units
P_t                        premium_pp(t)                   Gross premium per policy
(planned)                  premium_pp_ann                  Planned annual premium
(persistency)              prem_persistency(t)             Paid/planned factor 0.98^(y-1)
l_prem                     load_prem_rate()                Premium load rate
NP_t                       prem_to_av_pp(t)                Net premium to the accounts
W_t                        wd_pp(t)                        Partial withdrawal, gross of fee
(the $25 fee)              wd_fee_pp(t)                    Withdrawal fee
B_t                        loan_new_pp(t)                  New standard loan
W_t + B_t                  draw_pp(t)                      The whole step-3 draw
W^FA_t + B^FA_t            draw_from_fa_pp(t)              Step-3 draw sourced from FA
W^seg_{k,t} + B^seg_{k,t}  draw_from_seg_pp(t)             Step-3 draw sourced from segments
(segment k's share)        seg_wd_pp(t, m)                 Segment m's part of that draw
(cumulative)               seg_wd_cum_pp(t, m)             Draws out of segment m to date
FA_t                       fa_pp(t)                        Fixed (holding) account
(FA intra-month)           fa_pp_at(t, timing)             Fixed account by timing
S_{k,t}                    seg_bal_pp(t, m)                Balance of the segment born at m
Sweep_t                    sweep_pp(t)                     Sweep into a new segment
S_{k,m_k}                  seg_new_pp(m)                   Segment balance at creation
(sum of segments)          seg_bal_tot_pp(t)               All live segment balances
(active pool)              seg_bal_active_pp(t)            Segments available to a draw
(pro-rata share)           seg_share(t, m)                 Segment m's share of that pool
(segment count)            seg_count(t)                    Live segments, at most 12
w_ix                       index_alloc_rate()              Indexed allocation share
I(t)                       index_level(t)                  Index level at monthiversary t
r_k                        index_change(i_0, i_1)          Point-to-point index change
(index path)               index_return_ann                Level annual index return **[std]**
c                          index_cap_at(t)                 Cap in force
p                          index_par                       Participation rate
f                          index_floor                     Floor
cr_k                       index_credit_rate(r)            max(f, min(c, p x r))
(credit base)              seg_credit_base(...)            Balance the credit applies to
Credit_k                   index_credit(...)               Index credit, engine form
(matured value)            seg_matured_value(...)          Value rolling into the next segment
(the segment's r)          seg_return(t)                   Index change of the segment maturing at t
(credit at t)              index_credit_pp(t)              Credit added at BOM of month t
Roll^FA_t                  seg_roll_pp(t)                  Matured value rolled into FA
LCA_t                      lca_pp(t)                       Loan collateral account
Existing loan balance      loan_bal_init                   L(0), the opening loan balance
L_t                        loan_bal_pp(t)                  Loan principal plus interest
i_L^c                      loan_rate_ann                   Loan charged rate
i_L^e                      loan_credit_rate_ann(t)         Collateral credited rate
AV_t                       av_pp(t)                        Account value, end of month
AV_{t-1}                   av_pp_at(t, "BEF_PREM")         Account value, start of month
(after premium)            av_pp_at(t, "BEF_CREDIT")       Before the maturity credit
(after credit)             av_pp_at(t, "BEF_WD")           Before the withdrawal
AV'_t                      av_pp_at(t, "BEF_FEE")          After premium and withdrawal
AV'_t - MD_t               av_pp_at(t, "BEF_INV")          After the monthly deduction
(aggregate AV)             av_at(t, timing)                Account value in force
(none)                     av_change(t)                    Change in account value
i_fix                      fixed_rate_ann(t)               Fixed-account annual rate
i_g                        guar_rate_ann                   Guaranteed annual rate
(i_fix monthly)            inv_return_mth(t)               Monthly fixed-account rate
(i_g monthly)              guar_rate_mth()                 Monthly guaranteed rate
v_g                        naar_factor()                   1 + i_gm; DB is divided by it
(interest credited)        inv_income_pp(t)                Interest on FA and LCA
e_pol                      expense_pol_mth_at(t)           Monthly policy fee
e_unit                     expense_unit_mth_at(t)          Per-unit charge per $1,000
(none)                     rider_charge_pp(t)              Rider charges (0)
(e_pol + e_unit + rc)      maint_fee_pp(t)                 Non-COI monthly charges
coi_t                      coi_rate(t)                     Current monthly COI rate
(guaranteed COI)           coi_rate_guar(t)                Guaranteed maximum COI rate
COI_t                      coi_pp(t)                       Cost of insurance charge
NAAR_t                     net_amt_at_risk(t)              Net amount at risk
MD_t                       mth_deduction_pp(t)             Monthly deduction
MD^FA_t                    mth_deduction_from_fa_pp(t)     Deduction sourced from FA
MD^seg_{k,t}               mth_deduction_from_seg_pp(t)    Deduction sourced from segments
(segment k's share)        seg_ded_pp(t, m)                Segment m's part of the deduction
(cumulative)               seg_ded_cum_pp(t, m)            Deductions charged to segment m
DB_t                       db_pp(t)                        Death benefit after corridor
kappa_x                    corridor_factor(t)              IRC 7702(d) corridor factor
SC_t                       surr_charge_pp(t)               Surrender charge scheduled
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
(AV - SC)                  csv_pp(t)                       Cash value before loan
CSV_t                      ncsv_pp(t)                      Cash surrender value, loan netted
(SC retained)              surr_charge(t)                  Surrender charge collected
CumP_t                     cum_prem_net_pp(t)              Premiums less withdrawals and loans
(GPT/7-pay base)           cum_prem_pp(t)                  Premiums less withdrawals
CumMNLP_t                  cum_mnlp_pp(t)                  Cumulative no-lapse premium
(MNLP rate)                mnlp_rate()                     No-lapse premium per $1,000 p.a.
(MNLP monthly)             mnlp_pp_mth()                   Monthly no-lapse premium
(no-lapse period)          nlg_period_years()              Length of the no-lapse period
(no-lapse test)            nlg_test_ok(t)                  CumP >= CumMNLP
(NLG status)               nlg_in_effect(t)                In period and test passing
(NLG expiry shock)         nlg_expiry_shock(t)             25% shock at expiry **[std]**
(grace trigger)            is_shortfall(t)                 CSV cannot cover MD, NLG failed
(GPT limit)                gpt_limit(t)                    max(GSP, GLP x years)
(GPT test)                 gpt_ok(t)                       GPT compliance flag
(7-pay limit)              seven_pay_limit(t)              7-pay cumulative limit
(MEC flag)                 is_mec(t)                       7-pay failure flag
q^d_t                      mort_rate_mth(t)                Monthly mortality rate
(annual q)                 mort_rate(t)                    Annual mortality rate
(base lapse)               lapse_rate_base(t)              Base annual lapse rate
(SC-expiry spike)          lapse_rate_sc_mult(t)           Year-11 shock multiplier
r_cred,t                   cred_rate_ann(t)                Trailing credited rate
r_alt                      comp_rate_ann(t)                Competitor / market rate
(dynamic multiplier)       lapse_rate_dyn_mult(t)          Dynamic lapse multiplier
q^w_t                      lapse_rate_mth(t)               Monthly lapse rate
(annual w)                 lapse_rate(t)                   Total annual lapse rate
l_t                        pols_if(t)                      In force at start of month t
(l_0)                      pols_if_init                    In force at outset
(deaths)                   pols_death(t)                   Deaths in month t
(lapses)                   pols_lapse(t)                   Lapses in month t
(none)                     pols_maturity(t)                Maturities: always zero
(premium income)           premiums(t)                     Premium income
DB_t - L_t                 claims(t, "DEATH")              Death claims
CSV_t                      claims(t, "LAPSE")              Surrender payments
W_t - fee                  withdrawals(t)                  Withdrawal payments
E_t                        expenses(t)                     Insurer's own expenses
(premium tax)              premium_taxes(t)                Premium tax
(net loan cash flows)      net_loan_cf(t)                  Loan advances and repayments
CF_t                       net_cf(t)                       Net liability cash flow
=========================  ==============================  ==========================

Seven names needed care.

**A withdrawal is not a claim.** The notes write the withdrawal outflow as its own term
of ``CF_t``, alongside the death and surrender legs, and the library follows that: the
payment is :func:`withdrawals`, published in a ``withdrawals`` column, and
``"WITHDRAWAL"`` is **not** a ``kind`` that :func:`claims` accepts -- it would otherwise
sit in the ``kind is None`` total and be double-counted against the standalone cells.
The per-policy amount is still :func:`claim_pp` ``(t, "WITHDRAWAL")``, because that is
where the ``W_t - $25 fee`` rule lives and :func:`withdrawals` weights it by
:func:`pols_if`: a withdrawal is taken at BOM by policies still in force, not by a
decrement. Surrenders keep the ``"LAPSE"`` kind and are published as ``claims_lapse``,
so the column name matches the kind that produces it.

**The notes' ``t`` is not this model's ``t``.** The notes index policy months from
``t = 0`` at issue; here ``t`` is 1-based, so the notes' index is
:func:`duration_mth`. Every ``mod 12`` test -- the anniversary premium, the segment
maturity -- is written against ``duration_mth(t)``, and the surrender charge run-off
uses ``duration_mth(t) + 1`` because the notes' schedule counts the current month.

**The notes' ``CSV_t`` is :func:`ncsv_pp`, not :func:`csv_pp`.** The notes define
``CSV_t = AV_t - SC_t - L_t``, with the loan already netted. The chassis and
``CashValue_SE`` split that into :func:`csv_pp` (``AV - SC``) and :func:`ncsv_pp`
(``CSV - L``). The chassis names are kept, and the notes' symbol maps to the second.

**The withdrawal fee is inside ``W_t``, not on top of it.** These notes say ``W_t`` is
"gross of $25 fee" and that the "withdrawal outflow = W_t - $25 fee". The account is
therefore debited ``W_t``, the policyholder receives ``W_t - 25`` and the insurer keeps
the fee. The universal life chassis reads its own notes the other way -- there the fee
is charged *on top* of the withdrawal -- so :func:`av_pp_at` deliberately differs from
the chassis at ``"BEF_FEE"``.

**The death claim nets ``L_t``, not ``L(t-1)``.** These notes write
``death claim outflow = DB_t - L_t``; decrements are end-of-month events, after the
loan has accrued, so :func:`claim_pp` uses :func:`loan_bal_pp` at ``t``. The chassis
uses the opening balance because its own notes write ``L(t-1)``.

**``maint_fee`` is income, ``expenses`` is outgo.** As on the chassis,
:func:`maint_fee_pp` is the non-COI part of the monthly deduction -- a charge *against
the account value* -- while :func:`expenses` is the insurer's own $75 a year plus $150
at issue **[std]**. Confusing them double-counts.

**The two cumulative premium accumulators are different.** :func:`cum_prem_net_pp` is
the notes' ``CumP_t``, premiums less withdrawals **and loans**, which is what the
no-lapse test compares against ``CumMNLP_t``. :func:`cum_prem_pp` is premiums less
withdrawals only, which is the base of the guideline premium and 7-pay tests. Using one
for the other quietly changes both answers.

.. rubric:: The segment ladder

A segment is created at every monthiversary from the sweep and matures twelve months
later, so between step 2 and step 7 of any month eleven segments are live and after the
sweep twelve are -- the "up to 12 concurrent segments" of [S3][S4]. Segments are indexed
by their creation month ``m``: :func:`seg_bal_pp` ``(t, m)`` is the balance at the end
of month ``t`` of the segment born at ``m``, and is zero outside ``m <= t <= m + 11``.

Two properties of this arrangement are worth stating because the notes list both as
pitfalls.

Each segment carries **its own index start level** ``I(m)``, so twelve segments a year
mature at twelve different point-to-point returns. Collapsing them into one annual
segment mis-times credits and distorts mid-segment surrender values [S3];
:func:`check_seg_ladder` and model point 3 (indexed allocation 0%) exist so the
difference is visible rather than assumed.

Deductions and withdrawals are sourced from the fixed account first and then **pro rata
across live segments** on their remaining balances **[std]**. Because a pro-rata draw
leaves the proportions unchanged, one set of shares (:func:`seg_share`) serves both the
step-3 draw and the step-6 deduction. The two claims on the pool are **ordered, not
parallel**: the step-6 deduction is capped against what the step-3 draw leaves behind,
so their sum can never exceed the pool, no segment balance can go negative, and no
segment can pay a negative index credit at maturity. Capping both against the same
pre-draw pool is the easy mistake, and :func:`check_seg_ladder` now asserts against it.
The credit base under the baseline convention
is exactly the remaining balance -- amounts that left the segment mid-term earn no index
credit [S3]. The alternative convention the notes price, Transamerica's
adjusted-beginning-value with half-weighted deductions [S3], is the ``"ADJ_BEGIN"``
argument of :func:`seg_credit_base`, and both are asserted against the worked example.
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
    """The issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the selected model point."""
    return model_point()["sex"]


def rate_class():
    """The underwriting class of the selected model point (spec Table 1) [S3]."""
    return model_point()["rate_class"]


def sum_assured():
    """F: the initial face amount of the selected model point."""
    return float(model_point()["sum_assured"])


def db_option():
    """The death benefit option: ``"A"`` (level) or ``"B"`` (face plus account value).

    The Graded and Return of Premium options are minority designs excluded from the
    baseline by the product spec (F3).
    """
    return model_point()["db_option"]


def qual_test():
    """The IRC 7702 qualification test elected at issue; only ``"GPT"`` is modeled.

    GPT is the baseline (spec F4) because the Overloan Protection Rider attaches only
    to GPT non-MEC policies [S3]; CVAT is documented as a variation, so
    :func:`corridor_factor` raises on anything else rather than silently applying GPT
    corridor factors.
    """
    return model_point()["qual_test"]


def premium_type():
    """The premium pattern: ``"LEVEL"``, ``"SINGLE"`` or ``"TARGET"`` **[std]**."""
    return model_point()["premium_type"]


def premium_mode():
    """The premium mode: ``"ANNUAL"`` **[std]** baseline, or ``"MONTHLY"``.

    The notes fix the baseline at annual premiums paid at BOM of policy month 1 of
    each policy year **[std]**; monthly mode is carried so the chassis' level-pay
    pattern remains reachable.
    """
    return model_point()["premium_mode"]


def premium_pp_ann():
    """The planned annual premium per policy; a billing target only, premiums are flexible."""
    return float(model_point()["premium_pp_ann"])


def index_alloc_rate():
    """w_ix: the share of the sweepable fixed-account balance moved to the indexed account.

    100% in the baseline **[std]**.  A model point at 0% never creates a segment and
    accumulates entirely at the fixed-account rate, which is the control run for the
    segment ladder.
    """
    return float(model_point()["index_alloc_rate"])


def av_pp_init():
    """AV(0): the account value per policy at the outset, 0 at issue.

    For an in-force model point the whole opening balance is placed in the fixed
    account net of any loan collateral **[std]**: the notes give no opening segment
    ladder, so a projection from an in-force cell starts with no live segments and
    rebuilds the ladder over its first twelve months.
    """
    return float(model_point()["av_pp_init"])


def loan_bal_init():
    """L(0): the policy loan balance per policy at the outset, 0 at issue."""
    return float(model_point()["loan_bal_init"])


def pols_if_init():
    """l(0): the in-force probability at the outset, 1 for a single-policy point."""
    return float(model_point()["pols_if_init"])


def duration_mth_init():
    """Completed policy months already elapsed when the projection starts.

    0 for a new-business model point, so that ``t = 1`` is the issue month; positive
    for an in-force cell.  This is the notes' issue-date / duration offset attribute.
    """
    return int(model_point()["duration_mth"])


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point."""
    return bool(model_point()["has_surr_charge"])


def surr_charge_id():
    """The surrender charge schedule ID, a row label of *surr_charge_table.csv*."""
    return model_point()["surr_charge_id"]


def wd_first_year():
    """The first policy year in which a withdrawal may be taken.

    2 in the shipped points: withdrawals are allowed after the free-look period [S3]
    and the model takes that as the first anniversary **[std]**.
    """
    return int(model_point()["wd_first_year"])


def loan_first_year():
    """The first policy year in which the distribution-scenario loan is drawn.

    The notes' loan utilization module borrows a level amount annually from a start
    age, e.g. 65 **[std]**; 21 for issue age 45 is that age expressed as a policy year.
    """
    return int(model_point()["loan_first_year"])


def mnlp_rate():
    """The minimum monthly no-lapse premium rate per $1,000 of face, annualized [S3].

    20.80 for M / Non-Tobacco / 45 / band 1 [S3].  The 250,000 example face is a
    higher band whose rate is not public, so the band-1 rate stands in **[std]**.
    """
    return float(model_point()["mnlp_rate"])


def gsp():
    """The guideline single premium (GPT compliance input) **[std]** placeholder.

    No retrieved source gives guideline premiums for this composite, so the shipped
    value is a plausible placeholder, not a computed IRC 7702 figure.
    """
    return float(model_point()["gsp"])


def glp():
    """The guideline level premium (GPT compliance input) **[std]** placeholder."""
    return float(model_point()["glp"])


def seven_pay_prem():
    """The 7-pay premium (IRC 7702A compliance input) **[std]** placeholder [R5]."""
    return float(model_point()["seven_pay_prem"])


def duration_mth(t):
    """The notes' own month index: completed policy months at the beginning of month t.

    ``duration_mth_init() + t - 1``, so it is 0 in the issue month of a new-business
    model point.  Anniversary events test ``duration_mth(t) % 12 == 0``.
    """
    return duration_mth_init() + t - 1


def duration(t):
    """Completed policy years at the beginning of policy month t."""
    return duration_mth(t) // 12


def policy_year(t):
    """y: the policy year containing policy month t, 1-based."""
    return duration(t) + 1


def age(t):
    """The attained age (ANB) in policy month t: ``age_at_entry() + duration(t)``.

    Attained age increments on the policy anniversary, not on the birthday, which is
    the ANB convention the whole model is built on **[std]** (spec Table 1, F1).
    """
    return age_at_entry() + duration(t)


def proj_len():
    """Projection length in policy months.

    ``12 * (maturity_age - age_at_entry()) - duration_mth_init()``: the projection runs
    to attained age 121 **[std]**, the notes' [unverified] maturity inference (spec
    F5).  The contract itself is described as continuing in force with no further
    charges at 121, so the horizon truncates the run rather than terminating the
    policy; :func:`pols_maturity` is identically zero.
    """
    return 12 * (maturity_age - age_at_entry()) - duration_mth_init()  # noqa: F821


def is_guaranteed_basis():
    """Whether the run uses class (a) contractual guarantees only.

    ``basis`` is ``"CURRENT"`` in the base run, so the current non-guaranteed scales
    apply.  Setting it to ``"GUARANTEED"`` switches the fixed-account rate to 1.00%,
    the cap to 2.00%, the premium load to 8%, the policy fee to $15, the per-unit
    charge to $0.40 in all years and the COI scale to its guaranteed maximum -- the
    notes' "guaranteed-basis projections use only this class".  Key sensitivity 1 in
    the notes is exactly how far apart the two runs are.
    """
    if basis == "CURRENT":                                           # noqa: F821
        return False
    elif basis == "GUARANTEED":                                      # noqa: F821
        return True
    else:
        raise ValueError("invalid basis")


def load_prem_rate():
    """l_prem: the premium load rate, 5% current **[std]** / 8% guaranteed **[std]** (F12).

    The current rate sits in the model point table because the load is itself a
    non-guaranteed element re-declarable under ASOP 2 [REG-R26].
    """
    if is_guaranteed_basis():
        return load_prem_rate_guar                                   # noqa: F821
    return float(model_point()["load_prem_rate"])


def fixed_rate_ann(t):
    """i_fix: the fixed (holding) account annual effective rate.

    4.50% current [S2], 1.00% guaranteed [S2].  A non-guaranteed element; the base
    deterministic run holds the snapshot level, as the notes prescribe.
    """
    if is_guaranteed_basis():
        return guar_rate_ann                                         # noqa: F821
    return fixed_rate_curr                                           # noqa: F821


def inv_return_mth(t):
    """The monthly fixed-account rate, ``(1 + i_fix)^(1/12) - 1`` **[std]** conversion.

    0.0036748 at the 4.50% current rate [S2].  The name follows ``CashValue_SE``; only
    the fixed account and the loan collateral account earn it -- segments earn no
    interim interest at all, which is what the 0% floor design buys [S2].
    """
    return (1 + fixed_rate_ann(t)) ** (1 / 12) - 1


def guar_rate_mth():
    """i_gm: the monthly guaranteed rate, ``(1 + i_g)^(1/12) - 1`` at i_g = 1.00% [S2]."""
    return (1 + guar_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def naar_factor():
    """``1 + i_gm``; ``v_g = 1 / naar_factor()`` is the notes' one-month discount.

    The death benefit is discounted one month at the **guaranteed** rate, never the
    credited or index rate -- the universal life base convention, carried over
    unchanged.  1.0008295 at the 1.00% guarantee [S2].
    """
    return 1 + guar_rate_mth()


def loan_rate_mth():
    """The monthly charged loan rate, ``(1 + i_L^c)^(1/12) - 1`` at 3.00% **[std]** (F18)."""
    return (1 + loan_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def loan_credit_rate_ann(t):
    """i_L^e: the rate credited on loan collateral, 2.00% years 1-10, 3.00% after **[std]**.

    The standardization keeps the universal carrier pattern of a ~1% net loan spread
    early grading to a 0% "wash" from year 11 [S3][S5][S7] (F18).
    """
    if policy_year(t) <= loan_credit_step_year:                      # noqa: F821
        return loan_credit_rate_ann_1                                # noqa: F821
    return loan_credit_rate_ann_2                                    # noqa: F821


def loan_credit_rate_mth(t):
    """The monthly loan collateral credited rate, ``(1 + i_L^e)^(1/12) - 1``."""
    return (1 + loan_credit_rate_ann(t)) ** (1 / 12) - 1


def index_cap_at(t):
    """c: the cap in force, 10.00% current [S2] / 2.00% guaranteed [S2] (F8).

    The current cap is a **snapshot**: observed 10.00%-13.75% across carriers and print
    dates [S2][S3][S4][S5][S7], and re-declared at every segment start [S3][S4].  The
    base run holds it level; a cap re-declaration module driven by an option budget is
    described in the notes but not implemented, because the notes supply neither an
    option pricing model nor a net investment earnings rate path.
    """
    if is_guaranteed_basis():
        return index_cap_guar                                        # noqa: F821
    return index_cap_curr                                            # noqa: F821


def index_level(t):
    """I(t): the S&P 500 price-return index level at monthiversary t [S2][S3].

    The base deterministic run grows the index at a level ``index_return_ann`` a year:
    ``index_level_init * (1 + index_return_ann)^(duration_mth(t) / 12)``, so every
    segment matures at the same point-to-point return.  6.40% is the carrier-published
    1988-2023 lookback for the 10%-cap account [S2].

    **This cells is the single point of substitution.**  Override it with a historical
    or simulated path and the whole segment ladder follows: the notes' stochastic
    module (real-world lognormal, mu = 6.0%, sigma = 16% **[std]**) is a driver around
    the model, not a formula inside it.  Remember what the notes say about the level
    rate: AG 49-A bounds what may be *illustrated*, not what will be *credited*
    [R1][R6], and because the cap truncates the right tail while the floor only offsets
    the left, a deterministic run at the illustrated rate overstates credits against a
    stochastic mean at matched expected index growth.
    """
    return index_level_init * (1 + index_return_ann) ** (duration_mth(t) / 12)  # noqa: F821


def index_change(index_start, index_end):
    """r = I(m+12) / I(m) - 1: the point-to-point index change over a segment term.

    Price return, dividends excluded [S2][S3].  Takes the two index levels rather than
    a month so that the worked example's own levels -- 4,500.00 to 5,040.00 in
    scenario A, to 3,825.00 in scenario B -- can be put through the same formula the
    projection uses.
    """
    return index_end / index_start - 1


def index_credit_rate(index_return, cap=None):
    """cr_k = max(f, min(c, p x r)): the credited rate for one segment [S2][S3][R1].

    Floor 0%, participation 100%, cap per :func:`index_cap_at` [S2].  ``cap`` defaults
    to the cap in force, which the base run holds level, so the default is read at
    ``t = 1``; pass ``index_cap_guar`` for the guaranteed-basis credit -- the notes
    price both on the worked example, at 10.00% and 2.00%.

    This is where the two-sided truncation lives: the cap binds on the way up, the
    floor on the way down, and the historical frequency of a 0% credit for a single
    index allocation was 12.55%-23.81% in a carrier's 2005-2017 issue-date study [S8].
    """
    c = index_cap_at(1) if cap is None else cap
    return max(index_floor, min(c, index_par * index_return))        # noqa: F821


def seg_credit_base(seg_bal_init, seg_deductions, conv=None):
    """The segment balance the index credit is applied to.

    ``"REMAINING"`` **[std]**, the baseline
        ``seg_bal_init - seg_deductions``: the actual balance left at maturity, so
        amounts withdrawn, borrowed or deducted mid-segment earn no index credit
        (withdrawal and loan forfeiture [S3]; extension to deductions **[std]**).

    ``"ADJ_BEGIN"``, the documented variation
        ``seg_bal_init - seg_deductions / 2``: Transamerica's contractual adjusted
        beginning value, which subtracts withdrawals and loan transfers in full but
        **one half** of the monthly deductions taken during the segment [S3].  Pass
        ``seg_bal_init`` already net of withdrawals and loan transfers, as
        :func:`index_credit_pp` does.

    The notes list picking one and keeping the death benefit, cash value and credit
    formulas consistent with it among the modeling pitfalls; ``seg_credit_base_conv``
    is the Reference that records the choice.
    """
    k = seg_credit_base_conv if conv is None else conv               # noqa: F821
    if k == "REMAINING":
        return seg_bal_init - seg_deductions
    elif k == "ADJ_BEGIN":
        return seg_bal_init - seg_deductions / 2
    else:
        raise ValueError("invalid credit base")


def index_credit(seg_bal_init, seg_deductions, index_return, conv=None, cap=None):
    """Credit_k = cr_k x credit base: the index credit paid at a segment's maturity.

    The engine form, taking the segment's opening balance (net of any withdrawals and
    loan transfers), the deductions charged to it over its term, and its
    point-to-point index change.  :func:`index_credit_pp` is the projection's caller.
    """
    return (index_credit_rate(index_return, cap)
            * seg_credit_base(seg_bal_init, seg_deductions, conv))


def seg_matured_value(seg_bal_init, seg_deductions, index_return, conv=None, cap=None):
    """The matured segment value: remaining balance plus the index credit.

    ``S_{k,m+12} x (1 + cr_k)`` under the baseline credit base, which is the value that
    rolls into the fixed account and is swept back into a new segment under the
    standing allocation instruction **[std]** (spec F11).
    """
    return (seg_bal_init - seg_deductions
            + index_credit(seg_bal_init, seg_deductions, index_return, conv, cap))


def prem_persistency(t):
    """The fraction of the planned premium actually paid in policy year y **[std]**.

    ``0.98^(y - 1)``: the notes give premium persistency in closed form rather than as
    a table, compounding at 98% a year.  Premium persistency is *the* behavior
    dimension unique to flexible-premium products; the 2015-2021 LIMRA/SOA UL study is
    the recommended public calibration base [REG-R21] and the level here is a
    placeholder.

    The funding-stop state the notes pair with this factor -- probability 1% a year,
    after which the policy runs charge-only -- is a **second account value path** the
    notes do not say how to blend with the first, and is not implemented.
    """
    return prem_persistency_rate ** (policy_year(t) - 1)             # noqa: F821


def premium_pp(t):
    """P_t: the gross premium per policy received at BOM of policy month t.

    Annual mode **[std]**: the whole planned premium falls at BOM of the first month
    of each policy year, ``duration_mth(t) % 12 == 0``, and every other month is zero.

    ``LEVEL``  planned annual premium times :func:`prem_persistency`.
    ``SINGLE`` one premium in the issue month, capped at the guideline single premium.
    ``TARGET`` as ``LEVEL`` but capped so cumulative premium stays inside the guideline
    premium limit **[std]**; the cap looks at ``cum_prem_pp(t - 1)``, so there is no
    circularity.

    Zero from attained age 121, when charges cease and premiums are no longer accepted
    (spec F5) -- inert in practice, because the projection horizon is that age.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    if premium_type() == "SINGLE":
        return min(premium_pp_ann(), gsp()) if duration_mth(t) == 0 else 0.0
    if premium_mode() == "ANNUAL":
        if duration_mth(t) % 12 != 0:
            return 0.0
        gross = premium_pp_ann() * prem_persistency(t)
    elif premium_mode() == "MONTHLY":
        gross = premium_pp_ann() / 12 * prem_persistency(t)
    else:
        raise ValueError("invalid premium mode")
    if premium_type() == "LEVEL":
        return gross
    elif premium_type() == "TARGET":
        return min(gross, max(0.0, gpt_limit(t) - cum_prem_pp(t - 1)))
    else:
        raise ValueError("invalid premium type")


def prem_to_av_pp(t):
    """NP_t = P_t (1 - l_prem): the net premium, credited to the fixed account.

    The fixed account doubles as the interim / holding account: net premium sits there
    at the declared fixed rate until the next monthiversary sweep moves it into a
    segment [S1] **[std]** (spec F10).
    """
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_av(t):
    """Net premium credited to account values, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """Premium income at BOM of policy month t, weighted by the in force at BOM."""
    return premium_pp(t) * pols_if(t)


def wd_pp(t):
    """W_t: the partial withdrawal per policy at BOM of month t, **gross of the fee**.

    A constant monthly amount from :func:`wd_first_year`, taken from the model point's
    ``wd_pp`` column and **0 in the baseline** [std]: the notes give no withdrawal
    utilization pattern, so the mechanics are implemented and the behaviour is left to
    the data.  Model point 4 switches it on.

    The account is debited ``W_t``; the policyholder receives ``W_t - 25`` and the
    insurer keeps the $25 fee [S3].  This differs from the universal life chassis,
    where the fee is charged on top of the withdrawal -- these notes write the
    withdrawal outflow as ``W_t - $25 fee``, so the fee is inside ``W_t`` here.
    """
    if policy_year(t) < wd_first_year():
        return 0.0
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return float(model_point()["wd_pp"])


def wd_fee_pp(t):
    """The $25 withdrawal fee, charged only in a month with a withdrawal [S3].

    Retained by the insurer, so it is part of :func:`margin_expense`, not of
    :func:`claims`.  It is not an extra debit to the account value: it comes out of
    ``W_t``.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def loan_new_pp(t):
    """B_t: a new standard loan taken at BOM of policy month t **[std]**.

    The notes' distribution-scenario module borrows a level amount annually from a
    start age [S3]; here that is ``loan_new_pp_ann`` from the first month of policy
    year :func:`loan_first_year`.  **Zero in the baseline** -- the notes set loan
    utilization to none -- and switched on by model point 4.

    Participating (indexed) loans are a documented variation, not modeled: the baseline
    uses standard loans only **[std]** (F18), which decouples loan modeling from index
    scenarios.
    """
    if policy_year(t) < loan_first_year():
        return 0.0
    if duration_mth(t) % 12 != 0:
        return 0.0
    return float(model_point()["loan_new_pp_ann"])


def face_reduction_pp(t):
    """The face reduction a withdrawal forces under Option A, dollar for dollar **[std]**.

    Standard universal life practice, stated in the product spec but not explicit in
    the retrieved brochures.  Under Option B the withdrawal reduces the account value
    only and this is zero.
    """
    if db_option() != "A" or wd_pp(t) <= 0:
        return 0.0
    return min(wd_pp(t), sum_assured_at(t - 1))


def sum_assured_at(t):
    """F(t): the face amount after any withdrawal-driven reductions.

    ``F(0) = sum_assured()``; face increases, elective decreases and option changes are
    not modeled, so the only movement is the Option A withdrawal reduction.
    """
    if t == 0:
        return sum_assured()
    return max(0.0, sum_assured_at(t - 1) - face_reduction_pp(t))


def units(t):
    """The face amount in $1,000 units, ``sum_assured_at(t) / 1000``.

    The per-unit charge is quoted per $1,000 of face per month, so it multiplies this.
    The surrender charge is quoted per $1,000 of **initial** face, because face
    decreases do not reduce it [S3]; see :func:`surr_charge_pp`.
    """
    return sum_assured_at(t) / 1000


def corridor_factor(t):
    """kappa_x: the IRC 7702(d) corridor factor at the attained age [R4].

    250% at ages 0-40 grading to 100% at 90-95.  Ages beyond the table take its last
    row.  Only the Guideline Premium Test is modeled (spec F4), so any other
    ``qual_test`` raises rather than being treated as GPT.

    High funding drives the corridor rather than the face amount, which raises the
    death benefit, the net amount at risk and hence the cost of insurance: the notes
    list omitting this among the pitfalls, because it overstates late-duration account
    values and understates charges.
    """
    if qual_test() != "GPT":
        raise ValueError("invalid qual_test")
    tbl = data.corridor_factors()                                    # noqa: F821
    a = min(max(age(t), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[a, "corridor_factor"])


def db_pp(t):
    """DB_t: the death benefit per policy after the corridor test [S3][R4].

    ``max(option_db, kappa_x x AV'_t)`` where ``option_db`` is the face amount under
    Option A and face plus account value under Option B, and ``AV'_t`` is the account
    value after premium, the maturity credit and any withdrawal, and **before** the
    monthly deduction.  Measuring the account value at that point is what removes the
    circularity: under Option B the death benefit depends on the account value and the
    net amount at risk on the death benefit, but with this ordering neither depends on
    the deduction.

    During a segment the death benefit reflects the segment balance **without**
    unrealized index credit [S3]: with a 0% floor design segments simply carry no
    interim interest, so nothing extra is needed here.
    """
    av = av_pp_at(t, "BEF_FEE")
    if db_option() == "A":
        opt = sum_assured_at(t)
    elif db_option() == "B":
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor(t) * av)


def net_amt_at_risk(t):
    """NAAR_t = max(0, DB_t x v_g - AV'_t), the universal life base convention.

    The death benefit is discounted one month at the **guaranteed** rate
    (:func:`naar_factor`) and the account value is measured **before** the monthly
    deduction.  Using the credited or index rate in the discount, or the
    post-deduction account value, makes the cost of insurance implicit and requires
    iteration, and produces small systematic errors.
    """
    return max(0.0, db_pp(t) / naar_factor() - av_pp_at(t, "BEF_FEE"))


def coi_rate_scale():
    """The guaranteed maximum monthly COI scale for this model point's cell.

    A Series indexed by policy year, per $1,000 of net amount at risk, sliced once
    from *coi_rates.csv* for this ``sex`` / ``rate_class`` / ``age_at_entry``.  The
    shipped table covers the notes' anchor cell M / NT / 45 only; a model point on any
    other cell needs the table extended first.
    """
    return data.coi_rates().loc[                                     # noqa: F821
        (sex(), rate_class(), age_at_entry())]["coi_rate_guar"]


def coi_rate_guar(t):
    """The guaranteed maximum monthly COI rate per $1,000 of net amount at risk.

    The notes set the guaranteed basis at 2017 CSO ANB smoker-distinct ultimate
    **[std]**/[REG-R17].  That table is licensed and is not reproduced here: the
    shipped scale is illustrative **[std]**, of realistic magnitude and shape, and is
    swapped by replacing *coi_rates.csv*.  Policy years beyond the table take its last
    row.
    """
    scale = coi_rate_scale()
    y = min(policy_year(t), int(scale.index.max()))
    return float(scale[y])


def coi_rate(t):
    """coi_t: the monthly COI rate in force, per $1,000 of net amount at risk.

    ``coi_curr_factor`` (65% **[std]**) times the guaranteed maximum on the current
    basis; the guaranteed maximum itself on the guaranteed basis.  Carrier COI tables
    are not public [S3] and re-rating is governed by ASOP 2 [REG-R26], so the ratio is
    a pure modeling assumption and one of the notes' dominant sensitivities.

    Note the units: per $1,000 of net amount at risk per **month**, so it is divided by
    1,000 in :func:`coi_pp`.  It is not comparable with ``CashValue_SE.coi_rate``,
    which is a rate per unit of account value.
    """
    if is_guaranteed_basis():
        return coi_rate_guar(t)
    return coi_curr_factor * coi_rate_guar(t)                        # noqa: F821


def coi_pp(t):
    """COI_t = coi_t x NAAR_t / 1000: the cost of insurance charge per policy."""
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def coi(t):
    """Cost of insurance charges deducted from account values, for the policies in force."""
    return coi_pp(t) * pols_if(t)


def rider_charge_pp(t):
    """Rider charges, 0 in the baseline **[std]**.

    The notes carry this term in the monthly deduction so rider modules can be added
    without changing the recursion; every rider in the product spec is out of the
    baseline.
    """
    return 0.0


def expense_pol_mth_at(t):
    """e_pol: the monthly policy fee, $10 current [S3][S5] / $15 guaranteed **[std]** (F13)."""
    if is_guaranteed_basis():
        return expense_pol_mth_guar                                  # noqa: F821
    return expense_pol_mth                                           # noqa: F821


def expense_unit_mth_at(t):
    """e_unit: the per-unit charge per $1,000 of face per month (F14).

    $0.30 in policy years 1-10 and nothing thereafter on the current basis; $0.40 in
    **all** years on the guaranteed basis.  The structure -- charged for the first ten
    years currently, guaranteed for all years -- is sourced [S3][S5]; the dollar scales
    live in policy data pages and are not public, so the levels are **[std]**.
    """
    if is_guaranteed_basis():
        return expense_unit_mth_guar                                 # noqa: F821
    if policy_year(t) <= expense_unit_step_year:                     # noqa: F821
        return expense_unit_mth_1                                    # noqa: F821
    return expense_unit_mth_2                                        # noqa: F821


def maint_fee_pp(t):
    """The non-COI part of the monthly deduction per policy.

    ``e_pol + e_unit x F/1000 + rider charges``.  The name follows
    ``CashValue_SE.maint_fee``: this is a *charge* against the account value and
    therefore insurer income.  It is not :func:`expenses`, which is the insurer's own
    outgo.
    """
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return (expense_pol_mth_at(t) + expense_unit_mth_at(t) * units(t)
            + rider_charge_pp(t))


def maint_fee(t):
    """Non-COI monthly charges deducted from account values, for the policies in force."""
    return maint_fee_pp(t) * pols_if(t)


def mth_deduction_pp(t):
    """MD_t = e_pol + e_unit x F/1000 x 1{yr<=10} + coi_t x NAAR_t / 1000.

    :func:`maint_fee_pp` plus :func:`coi_pp`, taken at BOM.  The deduction at the start
    of month t pays for month t's coverage.
    """
    return maint_fee_pp(t) + coi_pp(t)


def mth_deduction(t):
    """Monthly deductions taken from account values, for the policies in force."""
    return mth_deduction_pp(t) * pols_if(t)


def draw_pp(t):
    """The total amount leaving the fixed account and segments at step 3 of month t.

    The withdrawal (gross of its fee) plus the collateral for any new standard loan.
    The loan collateral does not leave the *account value* -- it moves into
    :func:`lca_pp` -- but it does leave the fixed account and the segments, and it is
    sourced by the same rule [S3].
    """
    return wd_pp(t) + loan_new_pp(t)


def draw_from_seg_pp(t):
    """The part of the step-3 draw sourced pro rata from live segments [S3].

    Only what the fixed account cannot cover, and never more than the live segments
    hold.  Being step 3 it has the **first** claim on the pool; the step-6 deduction
    is capped against what is left after it (:func:`mth_deduction_from_seg_pp`).
    Amounts leaving a segment mid-term earn no index credit [S3], which under the
    baseline credit base happens automatically.
    """
    short = draw_pp(t) - max(0.0, fa_pp_at(t, "BEF_WD"))
    if short <= 0:
        return 0.0
    return min(short, max(0.0, seg_bal_active_pp(t)))


def draw_from_fa_pp(t):
    """The part of the step-3 draw sourced from the fixed account, taken first [S3].

    Defined as the residual so that the two sources always sum to :func:`draw_pp`
    exactly; if neither the fixed account nor the segments can cover it, the fixed
    account carries the excess and goes negative rather than the draw being silently
    truncated.
    """
    return draw_pp(t) - draw_from_seg_pp(t)


def mth_deduction_from_seg_pp(t):
    """The part of the monthly deduction sourced pro rata from live segments **[std]**.

    The notes' sourcing convention: fixed account first, shortfall pro rata across
    active segments.  Never more than the segments still hold **after** the step-3
    draw, which is why the cap is ``seg_bal_active_pp(t) - draw_from_seg_pp(t)`` and
    not the pool :func:`draw_from_seg_pp` was itself capped against: the withdrawal
    and the new loan collateral come out of the same segments earlier in the same
    month, so capping both against the pre-draw pool would let the two together take
    more than the segments hold.  That drives a segment balance negative and, twelve
    months later, pays a **negative** index credit on it -- a breach of the 0% floor
    of ``cr_k = max(f, min(c, p x r))`` [S2][R1].  :func:`check_seg_ladder` asserts
    both consequences away.

    Whatever the segments cannot cover stays with :func:`mth_deduction_from_fa_pp`,
    so the fixed account carries the excess and goes negative rather than the
    deduction being silently truncated -- the notes charge ``MD_t`` in full and hand
    an uncovered deduction to the grace/lapse cascade, which is not implemented.

    Carrier practice differs -- Transamerica instead half-weights in-segment
    deductions in its credit base [S3] -- and the notes list picking one and keeping
    the formulas consistent among the modeling pitfalls; see :func:`seg_credit_base`.
    """
    short = mth_deduction_pp(t) - max(0.0, fa_pp_at(t, "BEF_FEE"))
    if short <= 0:
        return 0.0
    return min(short, max(0.0, seg_bal_active_pp(t) - draw_from_seg_pp(t)))


def mth_deduction_from_fa_pp(t):
    """The part of the monthly deduction sourced from the fixed account, taken first.

    The residual, so the two sources always sum to :func:`mth_deduction_pp`.
    """
    return mth_deduction_pp(t) - mth_deduction_from_seg_pp(t)


def seg_bal_active_pp(t):
    """The live segment balances available to a draw at BOM of month t.

    The segments born at ``t - 11 ... t - 1``, valued at the end of month ``t - 1``.
    The segment born at ``t - 12`` is **not** in the pool: it matured at step 2 of this
    month and its value is already in the fixed account.  The segment born at ``t``
    does not exist yet -- it is created by the sweep at step 7.
    """
    lo = max(1, t - seg_term_mth + 1)                                # noqa: F821
    return sum(seg_bal_pp(t - 1, m) for m in range(lo, t))


def seg_share(t, m):
    """Segment m's pro-rata share of a draw at BOM of month t.

    Its opening balance over the live pool.  Because a pro-rata draw leaves the
    proportions unchanged, the same shares serve the step-3 draw and the step-6
    deduction even though they are taken at different points in the month.
    """
    pool = seg_bal_active_pp(t)
    if pool <= 0:
        return 0.0
    return seg_bal_pp(t - 1, m) / pool


def seg_wd_pp(t, m):
    """Segment m's contribution to the step-3 draw of month t."""
    return draw_from_seg_pp(t) * seg_share(t, m)


def seg_ded_pp(t, m):
    """Segment m's contribution to the monthly deduction of month t."""
    return mth_deduction_from_seg_pp(t) * seg_share(t, m)


def sweep_pp(t):
    """Sweep_t = w_ix x FA balance after steps 1-6 **[std]** (spec F10).

    The monthiversary sweep, which creates this month's segment.  Carrier practice
    varies -- Pacific Life sweeps on the 15th [S1], Transamerica on the first day of a
    policy month [S3] -- and the baseline standardizes on the monthiversary so segment
    dates align with monthly processing.  Nationwide's charge-holdback in the fixed
    strategy [S5] is a documented variation and is not modeled.
    """
    return index_alloc_rate() * max(0.0, fa_pp_at(t, "BEF_SWEEP"))


def seg_new_pp(m):
    """S_{k,m_k}: the balance of the segment created at month m, from the sweep."""
    return sweep_pp(m)


def seg_bal_pp(t, m):
    """S_{k,t}: the balance at the end of month t of the segment created at month m.

    ``S_{k,t+1} = S_{k,t} - MD^seg - W^seg - B^seg``, with **no interim interest**: the
    0% floor design credits nothing during the segment term [S2], in contrast with
    Transamerica's in-segment 0.75% [S3], which is a different guarantee and must not
    be mixed with a 0% annual floor.

    Zero outside ``m <= t <= m + 11``.  A segment created at ``m`` is live through the
    end of month ``m + 11`` and matures at step 2 of month ``m + 12``, before that
    month's deduction -- so it bears eleven in-segment deductions.  The worked example
    stipulates twelve; see the README.
    """
    if m < 1 or t < m or t > m + seg_term_mth - 1:                   # noqa: F821
        return 0.0
    if t == m:
        return seg_new_pp(m)
    return seg_bal_pp(t - 1, m) - seg_wd_pp(t, m) - seg_ded_pp(t, m)


def seg_ded_cum_pp(t, m):
    """Deductions charged to segment m from its creation through the end of month t."""
    if m < 1 or t <= m or t > m + seg_term_mth - 1:                  # noqa: F821
        return 0.0
    return seg_ded_cum_pp(t - 1, m) + seg_ded_pp(t, m)


def seg_wd_cum_pp(t, m):
    """Withdrawals and loan transfers out of segment m through the end of month t."""
    if m < 1 or t <= m or t > m + seg_term_mth - 1:                  # noqa: F821
        return 0.0
    return seg_wd_cum_pp(t - 1, m) + seg_wd_pp(t, m)


def seg_bal_tot_pp(t):
    """The sum of every live segment balance at the end of month t."""
    lo = max(1, t - seg_term_mth + 1)                                # noqa: F821
    return sum(seg_bal_pp(t, m) for m in range(lo, t + 1))


def seg_count(t):
    """The number of segments with a positive balance at the end of month t.

    At most ``seg_term_mth`` (12), the contractual maximum [S3][S4]; zero throughout
    for a model point with ``index_alloc_rate() == 0``.
    """
    lo = max(1, t - seg_term_mth + 1)                                # noqa: F821
    return sum(1 for m in range(lo, t + 1) if seg_bal_pp(t, m) > 0)


def seg_return(t):
    """r_k for the segment maturing at month t: its own point-to-point index change.

    ``index_change(I(t - 12), I(t))``.  Each segment carries its own index start level,
    which is the whole point of a monthly ladder: collapsing twelve segments into one
    annual segment mis-times credits and distorts mid-segment surrender values [S3].
    """
    return index_change(index_level(t - seg_term_mth), index_level(t))  # noqa: F821


def index_credit_pp(t):
    """The index credit added to the account value at BOM of month t.

    The segment created at ``t - 12`` matures now: its credit is
    :func:`index_credit` of its opening balance net of withdrawals and loan transfers,
    the deductions charged to it, and its own point-to-point return.  Zero in the first
    twelve months, and in every month for a model point that never creates a segment.
    """
    m = t - seg_term_mth                                             # noqa: F821
    if m < 1:
        return 0.0
    init = seg_new_pp(m) - seg_wd_cum_pp(t - 1, m)
    return index_credit(init, seg_ded_cum_pp(t - 1, m), seg_return(t))


def index_credits(t):
    """Index credits added to account values, for the policies in force."""
    return index_credit_pp(t) * pols_if(t)


def seg_roll_pp(t):
    """Roll^FA_t: the matured segment value rolled into the fixed account at step 2.

    Remaining balance plus index credit.  Under the standing allocation instruction it
    is swept straight back into a new segment at step 7 **[std]** (spec F11); routing
    it through the fixed account is what makes it available to pay this month's
    deduction first, which is the notes' own sourcing rule.
    """
    m = t - seg_term_mth                                             # noqa: F821
    if m < 1:
        return 0.0
    return seg_bal_pp(t - 1, m) + index_credit_pp(t)


def fa_pp_at(t, timing):
    """FA: the fixed (holding) account balance at an intra-month point of month t.

    The notes' recursion
    ``FA_{t+1} = [FA_t + NP_t - MD^FA - W^FA - B^FA - Sweep + Roll^FA] x (1+i_fix)^(1/12)``
    unrolled, with ``timing`` naming the point just before each event:

    ``"BEF_PREM"``
        The closing balance of the previous month, ``FA_t``.

    ``"BEF_CREDIT"``
        After the net premium, before the maturing segment rolls in.

    ``"BEF_WD"``
        After the roll, before the withdrawal and any new loan collateral.

    ``"BEF_FEE"``
        After the draw, before the monthly deduction.

    ``"BEF_SWEEP"``
        After the deduction, before the sweep.  This is the balance the sweep takes
        ``w_ix`` of.

    ``"BEF_INV"``
        After the sweep, before interest.  Interest is credited on this balance;
        reversing the two overstates the account value by about one month's interest on
        the deduction, every month.
    """
    if timing == "BEF_PREM":
        return fa_pp(t - 1)
    elif timing == "BEF_CREDIT":
        return fa_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)
    elif timing == "BEF_WD":
        return fa_pp_at(t, "BEF_CREDIT") + seg_roll_pp(t)
    elif timing == "BEF_FEE":
        return fa_pp_at(t, "BEF_WD") - draw_from_fa_pp(t)
    elif timing == "BEF_SWEEP":
        return fa_pp_at(t, "BEF_FEE") - mth_deduction_from_fa_pp(t)
    elif timing == "BEF_INV":
        return fa_pp_at(t, "BEF_SWEEP") - sweep_pp(t)
    else:
        raise ValueError("invalid timing")


def fa_pp(t):
    """FA_t: the fixed (holding) account balance at the end of policy month t.

    ``FA(0)`` is the model point's opening account value less its loan collateral: the
    notes give no opening segment ladder, so an in-force cell starts with everything in
    the holding account **[std]**.  Thereafter the post-sweep balance plus one month's
    interest at the fixed-account rate.
    """
    if t == 0:
        return av_pp_init() - loan_bal_init()
    return fa_pp_at(t, "BEF_INV") * (1 + inv_return_mth(t))


def lca_pp_at(t, timing):
    """LCA: the loan collateral account at an intra-month point of month t.

    ``"BEF_PREM"`` is the closing balance of the previous month; ``"BEF_INV"`` adds the
    collateral for any new loan taken at step 3, which is the balance one month's
    interest is credited on.
    """
    if timing == "BEF_PREM":
        return lca_pp(t - 1)
    elif timing == "BEF_INV":
        return lca_pp_at(t, "BEF_PREM") + loan_new_pp(t)
    else:
        raise ValueError("invalid timing")


def lca_pp(t):
    """LCA_t: the loan collateral account at the end of policy month t.

    Standard loans move loaned value out of the fixed account and the segments into a
    collateral account credited at :func:`loan_credit_rate_ann` while the loan itself
    accrues at the charged rate; the collateral remains part of the account value, so a
    loan advance does not reduce ``AV`` -- it reduces the cash surrender value through
    ``- L_t``.  ``LCA(0)`` is set equal to the model point's opening loan **[std]**.
    """
    if t == 0:
        return loan_bal_init()
    return lca_pp_at(t, "BEF_INV") * (1 + loan_credit_rate_mth(t))


def loan_bal_pp(t):
    """L_t: the policy loan balance at the end of policy month t.

    ``L_{t+1} = (L_t + B_t) (1 + i_L^c)^(1/12)``, the notes' own recursion: new loans
    from step 3 are added to principal and the whole balance accrues at the charged
    rate.  Repayments are not modeled -- the notes give no repayment pattern.
    """
    if t == 0:
        return loan_bal_init()
    return (loan_bal_pp(t - 1) + loan_new_pp(t)) * (1 + loan_rate_mth())


def inv_income_pp(t):
    """Interest credited to the account value per policy at EOM of policy month t.

    The post-sweep fixed-account balance at the fixed-account monthly rate plus the
    loan collateral account at the collateral credited rate.  **Segments contribute
    nothing**: they earn no interim interest under a 0% floor design [S2], and their
    whole return arrives as :func:`index_credit_pp` at maturity.  Keeping the two apart
    is what stops the floor being confused with an in-segment guarantee, which the notes
    list among the pitfalls.
    """
    return (fa_pp_at(t, "BEF_INV") * inv_return_mth(t)
            + lca_pp_at(t, "BEF_INV") * loan_credit_rate_mth(t))


def inv_income(t):
    """Interest credited to account values, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month's interest.
    """
    return inv_income_pp(t) * pols_if(t)


def av_pp_at(t, timing):
    """AV: the account value per policy at an intra-month point of policy month t.

    The account value is the fixed account plus every live segment plus the loan
    collateral account; ``timing`` names the point just before each BOM event:

    ``"BEF_PREM"``
        Before the premium: the closing balance of the previous month, ``AV_{t-1}``.

    ``"BEF_CREDIT"``
        After the net premium, before the maturing segment's index credit.

    ``"BEF_WD"``
        After the index credit, before the withdrawal.  The roll of the matured segment
        into the fixed account is internal and does not change this total.

    ``"BEF_FEE"``
        After the withdrawal, before the monthly deduction.  This is the notes'
        ``AV'_t``, the balance the death benefit, the corridor test and the net amount
        at risk are all measured against.  A new loan does not change it: the collateral
        moves within the account value.

    ``"BEF_INV"``
        After the monthly deduction, before interest.

    The end-of-month balance ``AV_t`` is :func:`av_pp`, and
    :func:`check_av_components` asserts that it still equals the sum of its three
    parts.
    """
    if timing == "BEF_PREM":
        return av_pp(t - 1)
    elif timing == "BEF_CREDIT":
        return av_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)
    elif timing == "BEF_WD":
        return av_pp_at(t, "BEF_CREDIT") + index_credit_pp(t)
    elif timing == "BEF_FEE":
        return av_pp_at(t, "BEF_WD") - wd_pp(t)
    elif timing == "BEF_INV":
        return av_pp_at(t, "BEF_FEE") - mth_deduction_pp(t)
    else:
        raise ValueError("invalid timing")


def av_pp(t):
    """AV_t: the account value per policy at the end of policy month t.

    ``AV(0) = av_pp_init()``; thereafter the post-deduction balance plus one month's
    interest.  Interest is credited on the *post-deduction* balance, as on the
    universal life chassis; the index credit is not part of it -- that arrives at BOM
    when a segment matures.
    """
    if t == 0:
        return av_pp_init()
    return av_pp_at(t, "BEF_INV") + inv_income_pp(t)


def av_at(t, timing):
    """Account value in force at an intra-month point of policy month t.

    :func:`av_pp_at` times the number of policies in force, which is constant through
    the month because decrements are end-of-month events.  ``timing`` takes the same
    values as :func:`av_pp_at`, plus ``"EOM"`` for the closing balance before
    decrements.
    """
    if timing == "EOM":
        return av_pp(t) * pols_if(t)
    return av_pp_at(t, timing) * pols_if(t)


def av_change(t):
    """Change in the account value in force over policy month t.

    ``av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")``, following ``CashValue_SE``.
    """
    return av_at(t + 1, "BEF_PREM") - av_at(t, "BEF_PREM")


def surr_charge_rate(t):
    """SC per $1,000 of initial face in policy month t **[std]** scale (F17).

    ``max(0, sc_init - (sc_init / runoff_years) x m / 12)`` where ``m`` is the notes'
    own month index ``duration_mth(t) + 1`` -- the current month counts.  With the
    shipped schedule of $25.00 per $1,000 running off over 10 years this is $24.79 in
    the issue month, declining linearly to zero in the last month of policy year 10.
    The ten-year period is sourced [S1][S5][S7]; the dollar scale is not public and is
    a placeholder of realistic magnitude.
    """
    if not has_surr_charge():
        return 0.0
    row = data.surr_charge_table().loc[surr_charge_id()]             # noqa: F821
    init = float(row["sc_per_1000_init"])
    yrs = float(row["runoff_years"])
    m = duration_mth(t) + 1
    return max(0.0, init - (init / yrs) * (m / 12))


def surr_charge_pp(t):
    """SC_t: the surrender charge scheduled per policy in policy month t.

    Quoted on the **initial** face amount, because face decreases do not reduce the
    surrender charge [S3][S7].  This is the schedule, not the amount collected: see
    :func:`surr_charge`.
    """
    return surr_charge_rate(t) * sum_assured() / 1000


def csv_pp(t):
    """``AV_t - SC_t``, floored at zero: the cash value before the loan is netted.

    The floor is **[std]**: the notes write the cash surrender value without one, but a
    negative value would be a payment *from* the policyholder.  In the early policy
    years the scheduled surrender charge exceeds the account value and the floor binds,
    so the charge actually collected is the whole account value.

    The notes' own ``CSV_t`` -- which already nets the loan -- is :func:`ncsv_pp`.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """CSV_t = AV_t - SC_t - L_t: the cash surrender value, floored at zero.

    This is what a surrendering policyholder is paid, and the notes' surrender outflow.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """Surrender charge actually collected from the policies lapsing in month t.

    ``(AV_t - csv_pp(t)) x pols_lapse(t)``, so it is capped by the account value where
    the :func:`csv_pp` floor binds.  Insurer income, and part of
    :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def cum_prem_pp(t):
    """Cumulative premiums less withdrawals: the base of the GPT and 7-pay tests.

    ``CumPrem(0) = 0`` even for an in-force model point, because the notes give no
    opening accumulator **[std]**, so the compliance flags are only meaningful for
    points projected from issue.  The statutory "less a portion of withdrawals" is
    taken as the whole withdrawal **[std]**.
    """
    if t == 0:
        return 0.0
    return cum_prem_pp(t - 1) + premium_pp(t) - wd_pp(t)


def cum_prem_net_pp(t):
    """CumP_t: cumulative premiums less withdrawals **and loans**, for the no-lapse test.

    The notes define the no-lapse accumulator this way and the guideline premium
    accumulator differently; :func:`cum_prem_pp` is the other one.  Using one for the
    other quietly changes both answers.
    """
    if t == 0:
        return 0.0
    return cum_prem_net_pp(t - 1) + premium_pp(t) - wd_pp(t) - loan_new_pp(t)


def nlg_period_years():
    """The length of the no-lapse period in policy years, by issue age [S3] (spec F6).

    0-45: 20 years; 46-60: to attained age 65; 61+: 5 years.  Comparators differ --
    Nationwide 20 years for issue ages 0-55, ``75 - issue age`` for 56-69, 5 years for
    70+ [S5] -- and the Transamerica structure is the one the baseline follows.
    """
    x = age_at_entry()
    if x <= 45:
        return 20
    elif x <= 60:
        return max(0, 65 - x)
    return 5


def mnlp_pp_mth():
    """The minimum monthly no-lapse premium per policy [S3].

    ``mnlp_rate x F / 1000 / 12``: the annual rate per $1,000 of face spread evenly
    over the year.
    """
    return mnlp_rate() * sum_assured() / 1000 / 12


def cum_mnlp_pp(t):
    """CumMNLP_t: the cumulative minimum no-lapse premium through policy month t."""
    return mnlp_pp_mth() * (duration_mth(t) + 1)


def nlg_test_ok(t):
    """The cumulative-premium no-lapse test: ``CumP_t >= CumMNLP_t`` [S3][S4]."""
    return cum_prem_net_pp(t) >= cum_mnlp_pp(t)


def nlg_in_effect(t):
    """Whether the no-lapse guarantee is in effect: inside the period and test passing.

    While it is, the policy cannot lapse for insufficiency even with no cash surrender
    value [S3][S4], which is why :func:`lapse_rate` suppresses voluntary lapse in that
    state as well **[std]**.
    """
    return policy_year(t) <= nlg_period_years() and nlg_test_ok(t)


def nlg_expiry_shock(t):
    """Whether the 25% no-lapse-expiry shock lapse applies in policy month t **[std]**.

    The notes apply a 25% shock lapse to *underfunded* policies on no-lapse expiry;
    "underfunded" is taken as a non-positive cash surrender value **[std]**, and the
    shock is confined to the first policy year after the no-lapse period ends.
    """
    return policy_year(t) == nlg_period_years() + 1 and ncsv_pp(t) <= 0


def is_shortfall(t):
    """The grace trigger: the cash surrender value cannot cover the monthly deduction.

    ``AV'_t - SC_t - L_{t-1} < MD_t`` **and** the no-lapse test fails [S3][S4].  A
    diagnostic.  The grace and lapse-for-insufficiency cascade (61 days, modeled as
    lapse at ``t + 2`` months if unfunded **[std]**) is **not implemented**: the notes
    leave the in-grace account value treatment and the cash flow of a cure payment
    undetermined, so no policy is terminated for insufficiency here.
    """
    csv = av_pp_at(t, "BEF_FEE") - surr_charge_pp(t) - loan_bal_pp(t - 1)
    return csv < mth_deduction_pp(t) and not nlg_in_effect(t)


def gpt_limit(t):
    """The guideline premium limit, ``max(GSP, GLP x policy years elapsed)`` [R4]."""
    return max(gsp(), glp() * policy_year(t))


def gpt_ok(t):
    """Whether cumulative premium is still inside the guideline premium limit.

    A compliance side-calculation with no cash flow of its own: a refused premium
    simply never enters the model.
    """
    return cum_prem_pp(t) <= gpt_limit(t)


def seven_pay_limit(t):
    """The 7-pay limit, ``seven_pay_prem x min(7, policy years elapsed)`` [R5]."""
    return seven_pay_prem() * min(7, policy_year(t))


def is_mec(t):
    """Whether the 7-pay test has failed by policy month t [R5].

    A flag, not a cash flow: MEC status changes policyholder taxation, not insurer
    liability cash flows.
    """
    return policy_year(t) <= 7 and cum_prem_pp(t) > seven_pay_limit(t)


def class_factor():
    """The underwriting-class multiplier on the base mortality table **[std]**."""
    return float(data.class_factor_table().loc[rate_class(), "factor"])  # noqa: F821


def mort_rate(t):
    """The annual best-estimate mortality rate in policy month t.

    Base table times :func:`class_factor` times the A/E factor, 100% in the base run
    **[std]** with no mortality improvement.  The notes recommend 2015 VBT
    sex/smoker-distinct ANB validated against ILEC 2012-2019 [REG-R18][REG-R19]; those
    tables are licensed, so the shipped table is a small illustrative one **[std]**.
    Ages beyond the table take its last row, where the rate is 1.0.
    """
    tbl = data.mort_table()                                          # noqa: F821
    a = min(max(age(t), int(tbl.index.min())), int(tbl.index.max()))
    return float(tbl.loc[a, "mort_rate"]) * class_factor() * mort_ae_factor  # noqa: F821


def mort_rate_mth(t):
    """q^d_t: the monthly mortality rate, ``1 - (1 - q)^(1/12)`` **[std]** conversion."""
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """The base annual lapse rate by policy year **[std]**.

    6% in policy years 1-10, 4% thereafter, read from *lapse_table.csv*; policy years
    beyond the table take its last row.  The levels are placeholders to be calibrated
    to the LIMRA/SOA persistency studies [REG-R20][REG-R21], whose detailed tables are
    behind a paid package.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate_ann"])


def lapse_shock_year():
    """The policy year of the surrender-charge-expiry lapse spike.

    The first policy year with no surrender charge -- the run-off length plus one,
    which is 11 for the shipped ten-year schedule -- derived from
    *surr_charge_table.csv* rather than hard-coded, so a different schedule moves the
    spike with it.  Zero when the model point carries no surrender charge, which no
    policy year can equal.
    """
    if not has_surr_charge():
        return 0
    return int(data.surr_charge_table().loc[surr_charge_id(), "runoff_years"]) + 1  # noqa: F821


def lapse_rate_sc_mult(t):
    """The surrender-charge-expiry spike multiplier, 2.0 in policy year 11 **[std]**.

    The ten-year surrender charge period [S1][S5][S7] creates a cliff in surrender
    economics; the size of the spike is a shape assumption, and UL lapse and surrender
    experience by duration is available in [REG-R21] for calibration.
    """
    return lapse_shock_mult if policy_year(t) == lapse_shock_year() else 1.0  # noqa: F821


def cred_rate_ann(t):
    """r_cred,t: the policy's trailing credited rate, driving dynamic lapse **[std]**.

    The credited rate of the segment that matured this month once the ladder is
    running, and the fixed-account rate before that or when nothing is allocated to the
    indexed account.  The notes say only "the policy's trailing credited rate"; this is
    the reading the model uses.
    """
    if index_alloc_rate() <= 0 or t <= seg_term_mth:                 # noqa: F821
        return fixed_rate_ann(t)
    return index_credit_rate(seg_return(t))


def comp_rate_ann(t):
    """r_alt: the competitor / market alternative rate **[std]**.

    The base deterministic run sets it equal to the trailing credited rate, so
    :func:`lapse_rate_dyn_mult` is exactly 1.  Override this cells to switch dynamic
    lapse on.  The rationale the notes give is real: caps are non-guaranteed elements
    and uncompetitive re-declarations -- caps on one product fell from 13.75% to 12.00%
    between two print dates [S3][S4] -- plausibly drive excess lapse.
    """
    return cred_rate_ann(t)


def lapse_rate_dyn_mult(t):
    """The dynamic lapse multiplier **[std]**.

    ``min(2.0, max(0.5, 1 + 3.0 x (r_alt - r_cred,t)))``: a competitive credited rate
    halves lapse at the floor and an uncompetitive one doubles it at the cap.  Equal to
    1 throughout the base run.
    """
    raw = 1 + lapse_dyn_slope * (comp_rate_ann(t) - cred_rate_ann(t))  # noqa: F821
    return min(lapse_dyn_cap, max(lapse_dyn_floor, raw))             # noqa: F821


def lapse_rate(t):
    """The total annual lapse rate **[std]**.

    Base rate times the surrender-charge-expiry spike times the dynamic multiplier,
    with two no-lapse-guarantee overrides the notes specify:

    * while the guarantee is in effect and the cash surrender value is non-positive,
      lapse is **suppressed** -- policyholders paying no-lapse-premium-level premiums
      persist;
    * in the first policy year after the no-lapse period ends, an underfunded policy
      takes a 25% shock lapse.

    ``lapse_rate_cap`` is 1.0: these notes give no cap, unlike the universal life
    chassis, so the Reference is present for symmetry and inert.
    """
    if nlg_in_effect(t) and ncsv_pp(t) <= 0:
        return 0.0
    if nlg_expiry_shock(t):
        return nlg_shock_lapse                                       # noqa: F821
    rate = lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_rate_dyn_mult(t)
    return min(lapse_rate_cap, rate)                                 # noqa: F821


def lapse_rate_mth(t):
    """q^w_t: the monthly lapse rate, ``1 - (1 - w)^(1/12)`` **[std]** conversion."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """l_t: the number of policies in force at the beginning of policy month t.

    Decrements are end-of-month events, so the number in force is constant through the
    month and every BOM cash flow is weighted by it.  ``pols_if(1) = pols_if_init()``.
    """
    if t == 1:
        return pols_if_init()
    return pols_if(t - 1) - pols_death(t - 1) - pols_lapse(t - 1)


def pols_if_at(t, timing):
    """Number of policies in force at time t, by ``timing``.

    All three ``CashValue_SE`` timings coincide for this product and equal
    :func:`pols_if`: there is no new business inside a projection, and the contract has
    no maturity that terminates coverage.
    """
    if timing in ("BEF_MAT", "BEF_NB", "BEF_DECR"):
        return pols_if(t)
    else:
        raise ValueError("invalid timing")


def pols_death(t):
    """Number of deaths at the end of policy month t, ``pols_if(t) x q^d_t``."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Number of lapses at the end of policy month t.

    ``pols_if(t) x (1 - q^d_t) x q^w_t``: death is applied before lapse **[std]**.
    """
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    At attained age 121 the policy is described as continuing in force with no further
    charges [unverified] (spec F5), so the projection horizon truncates the run rather
    than terminating the contract.  The cells is kept so the in-force roll-forward
    identity has the same shape as in the term and annuity models of this library,
    where it is not zero.
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``"DEATH"``
        ``DB_t - L_t``, the death benefit less policy debt.  The loan is taken at its
        end-of-month value because decrements follow the loan accrual, which is how
        these notes write it.

    ``"LAPSE"``
        ``CSV_t``, the cash surrender value with the surrender charge and the loan
        already netted -- :func:`ncsv_pp`.

    ``"WITHDRAWAL"``
        ``W_t - $25 fee``: the withdrawal is gross of the fee and the insurer keeps it.
        This kind survives here, where :func:`claims` no longer accepts it, because the
        per-policy rule has to live somewhere; :func:`withdrawals` is its only caller.
    """
    if kind == "DEATH":
        return max(0.0, db_pp(t) - loan_bal_pp(t))
    elif kind == "LAPSE":
        return ncsv_pp(t)
    elif kind == "WITHDRAWAL":
        return max(0.0, wd_pp(t) - wd_fee_pp(t))
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim released out of the account value, by ``kind``.

    Death and lapse both release the end-of-month account value ``AV_t``, because
    decrements follow the interest credit.  ``"MATURITY"`` is zero: the contract does
    not mature within the projection.
    """
    if kind == "DEATH":
        return av_pp(t) * pols_death(t)
    elif kind == "LAPSE":
        return av_pp(t) * pols_lapse(t)
    elif kind == "MATURITY":
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_over_av(t):
    """Death claims in excess of the account value released.

    ``(claim_pp(t, "DEATH") - AV_t) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin.
    """
    return (claim_pp(t, "DEATH") - av_pp(t)) * pols_death(t)


def claims(t, kind=None):
    """Claim outgo in policy month t, optionally by ``kind``.

    ``kind`` is ``"DEATH"`` or ``"LAPSE"``, or ``None`` for the total.  Death claims are
    weighted by :func:`pols_death` and surrenders by :func:`pols_lapse`, both
    end-of-month events.

    ``"WITHDRAWAL"`` is deliberately **not** accepted: a partial withdrawal is a payment
    on the owner's election rather than a claim, so it is the standalone cells
    :func:`withdrawals` and its own ``result_cf()`` column.  Keeping it out of the
    ``kind is None`` total is what stops it being counted twice.
    """
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    elif kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    elif kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    else:
        raise ValueError("invalid kind")


def withdrawals(t):
    """Partial withdrawal payments in policy month t: ``(W_t - $25 fee) x l_t``.

    Weighted by :func:`pols_if`, because a withdrawal is taken at BOM by policies still
    in force -- it is not a decrement.  The per-policy amount is
    :func:`claim_pp` ``(t, "WITHDRAWAL")``, so the fee-inside-``W_t`` rule is stated
    once; the fee itself stays with the insurer as :func:`wd_fees`.

    A withdrawal is not a claim, and this cells is why :func:`claims` does not take a
    ``"WITHDRAWAL"`` kind.
    """
    return claim_pp(t, "WITHDRAWAL") * pols_if(t)


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force.

    Taken out of the withdrawal, so this is the difference between what leaves the
    account value and what the policyholder receives; it appears in
    :func:`margin_expense`, not in :func:`claims`.
    """
    return wd_fee_pp(t) * pols_if(t)


def net_loan_cf(t):
    """Net loan cash flow in policy month t: advances out, repayments in.

    A loan advance is cash the insurer pays out while the account value is unchanged --
    the collateral moves inside it -- so it is a liability cash flow of its own.
    Repayments are not modeled: the notes give no repayment pattern.
    """
    return -loan_new_pp(t) * pols_if(t)


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(y - 1)``.

    ``inflation_rate`` is **0** in the base run: these notes give per-policy
    maintenance and per-issue expenses as flat placeholders with no inflation
    assumption, unlike the universal life chassis.  The cells is kept so the chassis'
    shape survives and an inflation assumption can be switched on with one Reference.
    """
    return (1 + inflation_rate) ** (policy_year(t) - 1)              # noqa: F821


def expenses(t):
    """E_t: the insurer's own expenses in policy month t **[std]**.

    ``$75`` a policy a year spread monthly, plus ``$150`` at issue.  Placeholders: the
    notes have no public source for insurer expenses and say to calibrate to company
    studies.

    Not to be confused with :func:`maint_fee`, which is the charge *against the account
    value* -- income, not outgo.
    """
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    return (acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821


def premium_taxes(t):
    """Premium tax, 2.0% of premium **[std]** placeholder."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``load x P + withdrawal fees + maint_fee + surrender charges - expenses
    - premium taxes``.  Follows ``CashValue_SE.margin_expense``; see
    :func:`check_margin` for the identity it takes part in.
    """
    return (load_prem_rate() * premium_pp(t) * pols_if(t)
            + wd_fees(t)
            + maint_fee(t)
            + surr_charge(t)
            - expenses(t)
            - premium_taxes(t))


def margin_mortality(t):
    """Mortality margin: :func:`coi` net of :func:`claims_over_av`."""
    return coi(t) - claims_over_av(t)


def net_cf(t):
    """CF_t: the net liability cash flow in policy month t, **undiscounted**.

    ``premiums - claims - withdrawals - expenses - premium taxes + net loan cash
    flows``, which is the notes' own sign convention (inflow positive) and the
    library-wide one.  :func:`claims` is the death and surrender legs only, so
    :func:`withdrawals` is a term of its own here rather than part of the claim total.
    Policy charges -- the premium load, the monthly deduction, the surrender charge, the
    withdrawal fee -- are internal transfers within the account value, not cash flows;
    they emerge in profit as the margins.  Index credits and fixed-account interest are
    credits to the policyholder, not insurer cash flows, so they do not appear either --
    see :func:`check_margin` for how it all reconciles.
    """
    return (premiums(t) - claims(t) - withdrawals(t) - expenses(t)
            - premium_taxes(t) + net_loan_cf(t))


def check_av_components():
    """Check that the account value is still the sum of its three parts.

    Returns ``True`` when, for every projected month,
    ``av_pp(t) == fa_pp(t) + seg_bal_tot_pp(t) + lca_pp(t)``.  :func:`av_pp` is built
    from the notes' aggregate recursion while the fixed account, the segment ladder and
    the loan collateral account are each built from their own; this is the test that
    the two constructions have not drifted, and it is the strongest single check on the
    segment bookkeeping.
    """
    res = []
    for t in range(1, proj_len() + 1):
        parts = fa_pp(t) + seg_bal_tot_pp(t) + lca_pp(t)
        res.append(math.isclose(av_pp(t), parts,                     # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-8))
    return all(res)


def check_av_roll_fwd():
    """Check the account value roll-forward.

    Returns ``True`` when, for every projected month, the opening account value in
    force of month ``t + 1`` equals::

        av_at(t, "BEF_PREM")
            + prem_to_av(t)
            + index_credits(t)
            - withdrawals(t)
            - wd_fees(t)
            - mth_deduction(t)
            + inv_income(t)
            - claims_from_av(t, "DEATH")
            - claims_from_av(t, "LAPSE")

    This pins the notes' processing order: the index credit arrives at BOM when a
    segment matures, interest is credited on the *post-deduction* balance, decrements
    come after both, and the withdrawal fee leaves the account value alongside the
    withdrawal itself.
    """
    res = []
    for t in range(1, proj_len() + 1):
        av = (av_at(t, "BEF_PREM")
              + prem_to_av(t)
              + index_credits(t)
              - withdrawals(t)
              - wd_fees(t)
              - mth_deduction(t)
              + inv_income(t)
              - claims_from_av(t, "DEATH")
              - claims_from_av(t, "LAPSE"))
        res.append(math.isclose(av_at(t + 1, "BEF_PREM"), av,        # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-8))
    return all(res)


def check_seg_ladder():
    """Check the segment ladder bookkeeping.

    Returns ``True`` when, for every projected month, all four of the following hold:

    * at most ``seg_term_mth`` segments are live;
    * every segment that matured accounted for its creation balance exactly,
      ``seg_new_pp(m) == seg_bal_pp(m + 11, m) + deductions + withdrawals`` -- nothing
      may appear in or vanish from a segment except a deduction, a withdrawal or a loan
      transfer, because segments earn no interim interest;
    * **every live segment balance is non-negative**;
    * **every index credit is non-negative**.

    The last two are the 0% floor of ``cr_k = max(f, min(c, p x r))`` [S2][R1] stated as
    an invariant.  The accounting identity above closes even on a negative balance, and
    :func:`seg_count` counts only positive ones, so without these two an over-sourced
    draw could take a segment below zero and pay a negative credit on it at maturity
    without any check firing -- see :func:`mth_deduction_from_seg_pp`.
    """
    res = []
    for t in range(1, proj_len() + 1):
        res.append(seg_count(t) <= seg_term_mth)                     # noqa: F821
        res.append(index_credit_pp(t) >= -1e-8)
        lo = max(1, t - seg_term_mth + 1)                            # noqa: F821
        for k in range(lo, t + 1):
            res.append(seg_bal_pp(t, k) >= -1e-8)
        m = t - seg_term_mth                                         # noqa: F821
        if m >= 1:
            closed = (seg_bal_pp(t - 1, m) + seg_ded_cum_pp(t - 1, m)
                      + seg_wd_cum_pp(t - 1, m))
            res.append(math.isclose(seg_new_pp(m), closed,           # noqa: F821
                                    rel_tol=1e-9, abs_tol=1e-8))
    return all(res)


def check_margin():
    """Check the net cash flow against the expense and mortality margins.

    Returns ``True`` when, for every projected month::

        net_cf(t) == margin_expense(t) + margin_mortality(t)
                     + av_change(t) - inv_income(t) - index_credits(t)
                     + loan_bal_pp(t) * pols_lapse(t)
                     + net_loan_cf(t)

    The terms after the two margins are what separates a *gross liability cash flow*
    model from ``CashValue_SE``, whose ``net_cf`` already nets the change in account
    value and the investment income.  ``index_credits`` joins ``inv_income`` because
    the indexed account's whole return arrives at maturity rather than monthly; the
    loan terms are the debt extinguished against the account value when a policy with a
    loan surrenders, and the advance itself.  The identity holds while neither the
    :func:`csv_pp` nor the :func:`ncsv_pp` floor binds against a policy loan.
    """
    res = []
    for t in range(1, proj_len() + 1):
        rhs = (margin_expense(t) + margin_mortality(t)
               + av_change(t) - inv_income(t) - index_credits(t)
               + loan_bal_pp(t) * pols_lapse(t)
               + net_loan_cf(t))
        res.append(math.isclose(net_cf(t), rhs,                      # noqa: F821
                                rel_tol=1e-9, abs_tol=1e-8))
    return all(res)


def result_cf():
    """Result table of cashflows, a DataFrame indexed by policy month ``t``.

    ``pols_if`` is the number in force at the **start** of month ``t`` and is the weight
    on that same row's cash flows.  The cash flow columns are income-positive and sum to
    ``net_cf``: ``premiums - claims_death - claims_lapse - withdrawals - expenses
    - premium_taxes + net_loan_cf``.  The surrender column is ``claims_lapse``, matching
    the ``"LAPSE"`` kind that produces it, and withdrawals are their own column because
    they are not claims.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_loan_cf": [net_loan_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy decrements, a DataFrame indexed by policy month ``t``."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the per-policy account value roll-forward.

    The columns follow the notes' processing order: opening account value, net
    premium, the index credit of any maturing segment, the account value before the
    deduction, the death benefit, the net amount at risk, the cost of insurance, the
    monthly deduction, the post-deduction balance, the interest credited, the closing
    account value, and then the surrender and loan values.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_prem": [av_pp_at(t, "BEF_PREM") for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "index_credit_pp": [index_credit_pp(t) for t in ts],
            "av_pp_bef_fee": [av_pp_at(t, "BEF_FEE") for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "net_amt_at_risk": [net_amt_at_risk(t) for t in ts],
            "coi_pp": [coi_pp(t) for t in ts],
            "mth_deduction_pp": [mth_deduction_pp(t) for t in ts],
            "av_pp_bef_inv": [av_pp_at(t, "BEF_INV") for t in ts],
            "inv_income_pp": [inv_income_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "ncsv_pp": [ncsv_pp(t) for t in ts],
            "loan_bal_pp": [loan_bal_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_seg():
    """Result table of the indexed segment ladder, a DataFrame indexed by ``t``.

    The index level, the fixed (holding) account, the sweep that creates this month's
    segment, the total and count of live segments, the credit paid by the segment
    maturing this month and the return that produced it.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "index_level": [index_level(t) for t in ts],
            "fa_pp": [fa_pp(t) for t in ts],
            "sweep_pp": [sweep_pp(t) for t in ts],
            "seg_bal_tot_pp": [seg_bal_tot_pp(t) for t in ts],
            "seg_count": [seg_count(t) for t in ts],
            "index_credit_pp": [index_credit_pp(t) for t in ts],
            "seg_return": [seg_return(t) if t > seg_term_mth else 0.0  # noqa: F821
                           for t in ts],
            "lca_pp": [lca_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

basis = "CURRENT"

maturity_age = 121

omega_age = 120

charges_cease_age = 121

guar_rate_ann = 0.01

fixed_rate_curr = 0.045

index_cap_curr = 0.1

index_cap_guar = 0.02

index_par = 1.0

index_floor = 0.0

index_return_ann = 0.064

index_level_init = 4500.0

seg_term_mth = 12

seg_credit_base_conv = "REMAINING"

load_prem_rate_guar = 0.08

expense_pol_mth = 10.0

expense_pol_mth_guar = 15.0

expense_unit_mth_1 = 0.3

expense_unit_mth_2 = 0.0

expense_unit_mth_guar = 0.4

expense_unit_step_year = 10

coi_curr_factor = 0.65

loan_rate_ann = 0.03

loan_credit_rate_ann_1 = 0.02

loan_credit_rate_ann_2 = 0.03

loan_credit_step_year = 10

wd_fee = 25.0

prem_persistency_rate = 0.98

mort_ae_factor = 1.0

lapse_shock_mult = 2.0

lapse_dyn_slope = 3.0

lapse_dyn_cap = 2.0

lapse_dyn_floor = 0.5

lapse_rate_cap = 1.0

nlg_shock_lapse = 0.25

expense_acq = 150.0

expense_maint = 75.0

inflation_rate = 0.0

premium_tax_rate = 0.02

pd = ("Module", "pandas")

math = ("Module", "math")