# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of :mod:`~.FIA_US_S`.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked-example anchor cell, by month
    >>> Projection[1].result_cf_annual()   # the same, summed into contract years
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/fixed_indexed_annuity/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FIA_US_S`` folder without its parent's CSVs produces a model that reads
and then fails on first evaluation.

The readers and the filename References live on the sibling
:mod:`~.FIA_US_S.Data` Space, reached here through the ``data`` Reference, so
each file is read once per model rather than once per model point:

=========================  ==================================  ==========================
Reference (on Data)        Cells                               File
=========================  ==================================  ==========================
model_point_file           data.model_point_table()            model_point_table.csv
mort_table_file            data.mort_table()                   mort_table.csv
surr_charge_file           data.surr_charge_table()            surr_charge_table.csv
rollup_file                data.rollup_table()                 rollup_table.csv
payout_rate_file           data.payout_rate_table()            payout_rate_table.csv
rate_scenario_file         data.rate_scenario()                rate_scenario.csv
withdrawal_file            data.withdrawal_table()             withdrawal_table.csv
=========================  ==================================  ==========================

.. rubric:: Projection basis

``t`` is the **month index and it is 0-based**: ``t = 0`` is the first month of a model
point projected from issue, ``duration(t) = t // 12`` is the completed contract years at
the start of month ``t``, and the contractual label is ``policy_year(t) = duration(t) + 1``.
The frame is ``t = entry_mth() … proj_len() - 1``, and ``proj_len()`` is ``12 *
policy_term()``. The grid matches :mod:`.MYGA_US_S`, :mod:`.Term_US_S` and the rest of the
library, and it is what the product assignment table records for this product.

**The monthly grid does not make the product monthly.** The technical notes make the
anniversary the single event date — "All transactions occur **at** the anniversary and are
processed as the last events of the contract year ending there" **[std]** — and that is
still true here: every contractual event is an annual event landing in the **anniversary
month**, ``is_anniv(t)``, the last month of each contract year. What the finer grid buys is
everything that is *not* a contractual event: mortality and surrender now fall in the month
they happen rather than all at the anniversary, the Model #805 floor and the fixed account
accrue month by month so a mid-year death or surrender is valued on the balance it actually
has, and maintenance expense accrues where it is incurred. Because the monthly decrement
rates compound to the annual ones and every contractual step still happens once a year,
**every state value at an anniversary is identical to the annual grid's** — account value,
benefit base, rollup base, lifetime withdrawal, Model #805 floor, phase and ``pols_if`` at
``t = 12k``. What changes is the timing and the weighting of the cash, which is the point.

Three vocabulary cells carry the split, and the whole model is written in terms of them:
:func:`duration` for anything keyed by contract year, :func:`is_anniv` for anything that
happens once a year, and :func:`year_open_mth` for the month whose closing value opens the
contract year — because on a monthly grid the previous *month* is no longer the previous
*year*, and reaching for ``t - 1`` where a year is meant is the mistake this conversion
exists to prevent.

``age(t) = age_at_entry() + duration(t)`` is the attained age **opening the contract year**
of month ``t``, so mortality over that year reads ``age(t)`` itself — the library
convention of :mod:`.Term_US_S` and :mod:`.MYGA_US_S`. Age changes on the anniversary, not
on the birthday and not monthly. The transactions at the closing anniversary are one year
older, and that age is :func:`exercise_age`, ``covered_age(t) + 1``: it is what reads the
lifetime-withdrawal percentage table and what clears the contractual minimum exercise age.

**There is no issue-instant row.** The single premium, the premium bonus and the
acquisition expense are beginning-of-month flows of month ``0`` on a new-issue model point,
whose first projected month is ``t = 0``. A model point may instead enter **in force** after
``entry_year()`` completed contract years, on balances stated in ``model_point_table.csv``
— which is what the worked example does, its anniversary-7 balances being explicitly
"illustrative ... broadly consistent with a seven-year deferral" **[std]** rather than
derived. ``entry_year()`` is an elapsed count of whole years, so ``entry_mth() = 12 *
entry_year()`` is the index of the model point's first projected month and the frame always
opens on an anniversary. Every recursion opens there on the ``*_init`` cells, read through
the opening timing (``av_pp_at(t, "BEF_INV")``, ``benefit_base_pp_at(t, "BEF_ROLLUP")``,
:func:`phase_open`, :func:`rider_in_force_open`), and ``result_cf()`` is indexed from
``entry_mth()``.

The anniversary's eight processing steps are the notes' own, all eight still annual and all
eight landing in the anniversary month, and each intermediate value is reachable through a
``timing`` argument rather than being buried inside one formula:

1. index credit and fixed interest --- :func:`index_credit_pp`,
   :func:`fixed_interest_ann_pp`
2. rider charge on the **opening** benefit base --- :func:`rider_charge_pp`
3. benefit base: rollup, stack, step-up --- :func:`rollup_pp`, :func:`stack_pp`
4. lifetime and excess withdrawal --- :func:`lw_pp_at`, :func:`wd_pp`
5. charges on the excess and the proportional reduction --- :func:`wd_reduction_rate`
6. guaranteed minimum value roll --- :func:`mgsv_pp`
7. phase transition including the depletion test --- :func:`phase`
8. decrements --- :func:`pols_if_at` at ``"AFT_DECR"``

Steps 1--3 are skipped in ``DEPLETED``, steps 1--7 in ``TERMINATED``. Step 8 is the one
that is **not** annual: it runs every month, on :func:`mort_rate_mth` and
:func:`lapse_rate_mth`. Steps 1 and 6 keep a monthly component — the fixed account accrues
at ``(1 + i_F)^(1/12) - 1`` and the Model #805 floor at ``(1 + i_nf)^(1/12)`` — while their
annual figures, :func:`fixed_interest_ann_pp` and the anniversary deduction, stay whole.

Between anniversaries the contract is quiet: no withdrawal, no rider charge, no index
credit, no rollup and no step-up. The indexed account is therefore **flat between
anniversaries**, because the annual point-to-point segment locks only at maturity and "the
credit ... cannot be lost to later declines" [S1] is a statement about a credit that has
not yet been earned. That is the sourced rule "withdrawals are not credited with index
interest in the year they are taken" [S1] carried to mid-year deaths and surrenders
**[std]**; crediting a part year would be the *daily interim value* variant the notes
exclude.

.. rubric:: Naming

Cells names follow :mod:`.MYGA_US_S` — the deferred annuity chassis this
product sits on — and through it lifelib's ``basiclife.BasicTerm_S`` and
``savings.CashValue_SE``: ``pols_*`` for policy counts, ``av_*`` for account values,
plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-contract amounts,
``*_at(t, timing)`` for a quantity read at a point inside the anniversary. The technical
notes use compact actuarial symbols instead. The mapping is:

================================================  ================================  ========================================
Notes symbol                                      Cells                             Meaning
================================================  ================================  ========================================
t                                                 (the projection index)            Month index, 0-based
(elapsed years)                                   duration(t)                       Completed contract years at month t
(elapsed months)                                  duration_mth(t)                   Completed contract months; = t
(the anniversary month)                           is_anniv(t)                       Last month of a contract year
(that month's index)                              anniv_mth(t)                      Anniversary closing month t's year
(the year's opening month)                        year_open_mth(t)                  Anniversary that opened it
(contract year)                                   policy_year(t)                    Contract year containing t; duration + 1
x                                                 age_at_entry                      Issue age (ANB)
x + duration(t)                                   age(t)                            Attained age opening month t's contract year
(younger covered life)                            covered_age(t)                    Younger covered age opening that year
x + duration(t) + 1                               exercise_age(t)                   Covered age at the closing anniversary
(none)                                            policy_term                       Contract years from issue to maturity_age
(none)                                            proj_len                          Number of projected months; 12 x policy_term
(in-force cell entry)                             entry_year                        Completed years at entry
(none)                                            entry_mth                         First projected month; 12 x entry_year
av_initial                                        av_pp_init                        AV at entry, else P x (1 + b)
bb_initial                                        benefit_base_pp_init              BB at entry, else P
mgv_initial                                       mgsv_pp_init                      MGV at entry, else 0.875 x P
(RB at entry)                                     rollup_base_pp_init               RB at entry, else P
(LW at entry)                                     lw_pp_init                        LW at entry, 0 before exercise
(pi at entry)                                     payout_rate_init                  Payout percentage locked at entry
(phase at entry)                                  phase_init                        Phase at entry
P                                                 premium_pp                        Single premium
b                                                 bonus_rate                        Premium bonus rate (7% [S5])
b/(1+b)                                           bonus_factor                      Clawback factor -- **not** b [S10]
v(t)                                              vest_rate(t)                      Vested bonus percentage [S5]
alloc_indexed/alloc_fixed                         alloc_indexed / alloc_fixed       Account allocation at issue
I(y)                                              index_level(y)                    Index level at **anniversary number** y
R(t)                                              index_return(t)                   I(y+1)/I(y) - 1 over month t's year
c                                                 cap_rate                          Declared annual cap (5.25% [S2])
c_min                                             cap_rate_min                      Guaranteed minimum cap (0.25% [S4])
c(t)                                              cap_rate_in_force()               Cap actually applied
f                                                 floor_rate                        Index credit floor (0%)
p, s, d                                           par_rate, spread_rate,            Participation rate [R1]; spread
                                                  trigger_rate                      and trigger, levels **[std]**
cr(t)                                             credit_rate(t)                    Credit rate for month t's contract year
(cr on a return)                                  credit_rate_on(r, method)         The crediting engine itself
IC(t)                                             index_credit_pp(t)                Index credit, in the anniversary month
FI(t) monthly                                     fixed_interest_pp(t)              Fixed account interest for month t
FI(t) annual                                      fixed_interest_ann_pp(t)          The contract year's, for the stack
i_F, i_F,min                                      fixed_rate, fixed_rate_min        Declared / guaranteed fixed rate
kappa                                             av_int_factor                     Share of IC reaching the AV [S3]
(IC x kappa + FI)                                 inv_income_pp(t)                  Interest credited to the AV
A(t)                                              av_indexed_pp(t)                  Indexed account balance
F(t)                                              av_fixed_pp(t)                    Fixed account balance
AV(t)                                             av_pp(t)                          Account value closing month t
AV(0), AV(1), AV(2), AV(t)                        av_pp_at(t, timing)               BEF_INV / BEF_FEE / BEF_WD / EOY in
                                                                                    order; BEF_PREM opens the month
AV(0) of the contract year                        av_pp_year_open(t)                Balance opening month t's contract year
F(0), A(0) of that year                           av_fixed_pp_year_open(t),         The fixed and indexed openings: the
                                                  av_indexed_pp_year_open(t)        credit base and the fixed-interest base
l(t) x AV(t)                                      av_at(t, timing)                  In-force weighted account value
(shortfall at exhaustion)                         av_depletion_pp(t)                Withdrawal the AV could not fund
phi                                               rider_charge_rate                 Rider charge rate (0.95% [S9])
Phi(t)                                            rider_charge_pp(t)                Rider charge amount
BB(t)                                             benefit_base_pp(t)                GLWB benefit base, closing
BB(3), BB(4)                                      benefit_base_pp_at(t, timing)     BEF_ROLLUP/BEF_STEP_UP/BEF_WD/EOY
RB(t)                                             rollup_base_pp(t)                 Rollup base
g(t)                                              rollup_rate(t)                    Guaranteed simple rollup rate [S2]
rollup(t)                                         rollup_pp(t)                      Rollup dollar increment
m                                                 stack_factor                      Stacking factor (1.50 [S8][S9])
stack(t)                                          stack_pp(t)                       Stacking credit
T_g                                               in_growth_period(t)               Benefit base still growing
(the step-up)                                     step_up_applies(t)                Whether the ratchet is tested
LW(t)                                             lw_pp(t)                          Lifetime withdrawal amount, closing
LW before/after step 5                            lw_pp_at(t, timing)               BEF_WD / EOY
pi(a, basis)                                      payout_rate(a, basis)             Payout percentage by age band [S3]
(pi locked at exercise)                           payout_rate_locked(t)             The percentage actually in force
h(a)                                              activation_rate(a)                Activation incidence, reported only
G(t)                                              wd_pp(t)                          Gross withdrawal requested
min(G, LW)                                        wd_guar_pp(t)                     Guaranteed portion
E(t)                                              wd_excess_pp(t)                   Excess above the guaranteed amount
(unpayable withdrawal)                            wd_unfunded_pp(t)                 Requested but neither funded nor
                                                                                    guaranteed, on TERMINATED
(guaranteed portion paid)                         wd_guar_paid_pp(t)                min(G, LW) less its share of it
(excess portion paid)                             wd_excess_paid_pp(t)              E(t) less its share of it
FW(t)                                             free_wd_allow(t)                  Free withdrawal amount
0.10 x AV(0)(t)                                   free_wd_base(t)                   Base of the free amount
(FW consumed)                                     wd_free_pp(t)                     Free-allowance portion of the
                                                                                    withdrawal
(FW remaining)                                    free_wd_remain(t)                 Free amount left for the excess
X(t) on a withdrawal                              wd_charge_base_pp(t)              Amount exposed to charge and MVA
X(t) on a surrender                               surr_charge_base_pp(t)            Same, at a full surrender
sc(t)                                             surr_charge_rate(t)               Surrender charge percentage [S5]
SC(t) on a withdrawal                             wd_charge_pp(t)                   Surrender charge on the excess
SC(t) on a surrender                              surr_charge_pp(t)                 Surrender charge on a surrender
CB(t) on a withdrawal                             wd_clawback_pp(t)                 Non-vested bonus recovery
CB(t) on a surrender                              surr_clawback_pp(t)               Same, at a full surrender
(the clawback formula)                            bonus_clawback_on(...)            (1-A) x [B/(1+B)] x C [S10]
MVA(t) on a withdrawal                            wd_mva_pp(t)                      Collared MVA on the excess
MVA(t) on a surrender                             mva_pp(t)                         Collared MVA on a surrender
(the MVA collar)                                  mva_pp_on(t, base, gross)         The collared MVA on any base
(the MVA rate)                                    mva_rate(t)                       [(1+i0)/(1+it)]^(n/12) - 1 [S10]
i0                                                mva_ref_yield_at_issue            Reference index at issue
i_y                                               mva_ref_yield(y)                  Reference index at **anniversary number** y
n/12                                              mva_term(t)                       Years left in the MVA period
(MVA applies at all)                              mva_in_force(t)                   Inside the MVA period
rho(t)                                            wd_reduction_rate(t)              Proportional reduction factor
(rho's formula)                                   wd_reduction_rate_on(...)         The [S9] worked construction
Wcum(t)                                           wd_cum_pp(t)                      Cumulative gross withdrawals
G - SC - CB + MVA                                 wd_payment_pp(t)                  Cash paid on the withdrawal
(pre-floor surrender value)                       surr_value_pp(t)                  AV - SC - CB + MVA
CSV(t)                                            surr_benefit_pp(t)                Surrender benefit paid
MGV(t)                                            mgsv_pp(t)                        Model #805 guaranteed minimum
i_nf                                              mgsv_rate                         Nonforfeiture accumulation rate
(the $50 charge)                                  mgsv_charge_pp(t)                 Annual contract charge, 0 **[std]**
(statutory i_nf)                                  mgsv_rate_statutory(...)          Model #805 4B/4C indexed rate
phase(t)                                          phase(t)                          Closing ACCUM/INCOME/DEPLETED/TERMINATED
(phase during the year)                           phase_open(t)                     Phase steps 1-7 are processed under
(first exercise)                                  is_exercise(t)                    The first lifetime withdrawal
rider_in_force(t)                                 rider_in_force(t)                 Rider still alive closing month t [S9]
rider_in_force(k-1)                               rider_in_force_open(t)            Rider alive opening the contract year
depletion_cause(t)                                depletion_cause(t)                Excess / charge / negative MVA flag
q(t)                                              mort_rate(t)                      Annual mortality of month t's contract year
1 - (1-q)^(1/12)                                  mort_rate_mth(t)                  The monthly rate actually applied
(A/E deviation)                                   mort_ae_factor                    Mortality A/E factor, 100% **[std]**
w(t)                                              lapse_rate(t)                     Annual surrender rate of that year
1 - (1-w)^(1/12)                                  lapse_rate_mth(t)                 The monthly rate actually applied
w_base(t)                                         lapse_rate_base(t)                Base surrender table
w_shock                                           shock_lapse_rate(t)               33% / 10% / 5% by rider state [R8]
M_money(t)                                        lapse_moneyness_factor(t)         Moneyness suppression **[std]**
l(k) at t = 12k                                   pols_if(t)                        In-force opening month t
(closing the month)                               pols_if_at(t, "AFT_DECR")         In-force at the end of month t
l(0)                                              pols_if_init                      In-force at entry
(the four readings)                               pols_if_at(t, timing)             BEF_DECR/BEF_MORT/BEF_LAPSE/AFT_DECR
l q_m                                             pols_death(t)                     Deaths in the month
l (1-q_m) w_m                                     pols_lapse(t)                     Full surrenders in the month
(none)                                            pols_maturity(t)                  Survivors at the horizon
P at t = 0                                        premiums(t)                       Premium income
min(G, LW) x l(t)                                 wd_guar(t)                        Guaranteed withdrawal outgo, paid
(E - SC - CB + MVA) l(t)                          wd_excess(t)                      Excess withdrawal outgo, paid
LW while DEPLETED                                 income_payments(t)                Post-depletion income outgo
(all three together)                              withdrawals(t)                    Total withdrawal outgo
(ledger benefit lines)                            claims(t, kind)                   Benefit outgo by kind
                                                  claim_pp(t, kind)                 Benefit per contract by kind
                                                  claims_from_av(t, kind)           Account value released by a claim
                                                  claims_over_av(t, kind)           Benefit paid above the account value
(no separate commission)                          commissions(t)                    Acquisition commission, 0 **[std]**
0.06 P; (80/12) x 1.025^(t/12)                    expenses(t)                       Acquisition and monthly maintenance
premium tax                                       premium_taxes(t)                  Premium tax, 0% **[std]**
NetCF(t)                                          net_cf(t)                         Net cash flow for the month
(the annual summary)                              result_cf_annual()                result_cf() summed into contract years
================================================  ================================  ========================================

Six names needed care.

**pols_if(t) is the notes' l(k) at the twelfth months.** Across this library
``pols_if(t)`` is the number in force at the **start** of ``t`` and is the weight carried
by that same row's cash flows — :mod:`.Term_US_S` has ``pols_if(0) == pols_if_init()`` and
``savings.CashValue_SE`` has ``pols_if(t)`` equal to ``pols_if_at(t, "BEF_MAT")``. The
notes define ``l(k)`` as the in-force probability at the *end* of contract year ``k``,
which is anniversary ``k``, which is where contract year ``k + 1`` opens: on the monthly
index that is month ``12k``, so ``pols_if(12k) = l(k)`` with
``pols_if(entry_mth()) = l(0) = 1`` for a new issue. Because the monthly rates compound to
the annual ones this equality is exact, not approximate.

**The one place the finer grid changes an answer rather than its resolution** is the weight
on the anniversary's own cash. A withdrawal, a rider charge or a surrender charge falls in
month ``12k + 11`` and is weighted by ``pols_if(12k + 11)`` — the contracts that actually
*reach* the anniversary — where the annual grid weighted it by ``l(k)``, the contracts that
entered the year. The second is an approximation the annual grid could not avoid: it pays a
full year's guaranteed withdrawal to a contract that died in month three. The
reconciliation the convention buys is unchanged, and now holds row by row on the finer
grid: the ``pols_if`` column of :func:`result_cf` is the divisor of the cash flows on its
own row — ``result_cf()["wd_guar"][t] / wd_guar_paid_pp(t)`` is ``pols_if(t)``.

**MGV is MGSV.** The Model #805 floor is called ``MGV`` in these notes, after [S10], and
``MGSV`` in ``products/fixed_deferred_annuity/``, after its own specimen. Both source
files say in terms that this is **one quantity under two labels** and must not be modeled
as two. The chassis name :func:`mgsv_pp` is used here, so the two annuity models share it.
The *recursion*, however, is **not** the chassis's: this product accretes and then deducts,
``MGV(t) = max(0, MGV(t-1) x (1 + i_nf) - G(t))``, while the chassis deducts and then
accretes, ``MGSV(t) = [MGSV(t-1) - d(t) - c(t)] x g``. The worked example pins the FIA
ordering — ``93,811.84 x 1.01 - 10,144.16 = 84,605.80`` — and the chassis notes explicitly
warn against carrying their recursions across unexamined. Same name, same concept,
different arithmetic, on purpose.

**E(t) is not the chassis's E(t).** On the chassis ``E(t)`` is the amount exposed to the
surrender charge and the MVA, and is named ``wd_excess_pp`` / ``surr_excess_pp``. Here
``E(t)`` is the notes' **excess withdrawal** — the part of a gross withdrawal above the
guaranteed lifetime amount, the quantity that permanently reduces the guarantee and, at
exhaustion, destroys it. That is the product's headline concept and it keeps the name
:func:`wd_excess_pp`. The chargeable amount, the notes' ``X(t)``, becomes
:func:`wd_charge_base_pp` on the withdrawal path and :func:`surr_charge_base_pp` on the
surrender path. Reading a chassis formula across without renaming would silently charge a
surrender charge on the wrong base.

**age(t) opens the contract year; exercise_age(t) closes it.**
``age(t) = age_at_entry() + duration(t)`` is the attained age at the anniversary that opens
month ``t``'s contract year, exactly as in :mod:`.Term_US_S` and :mod:`.MYGA_US_S`, and
:func:`mort_rate` reads it directly — the annual rate it returns is then converted for the
month by :func:`mort_rate_mth`. Every transaction, however, falls at the **closing**
anniversary, one year older, and the payout percentage depends on that age: the anchor
cell's first lifetime withdrawal, in contract year 8 from an issue age of 62, is taken at
attained age 70 and reads ``pi(70, single) = 5.20%``. :func:`exercise_age` carries that age
— ``covered_age(t) + 1`` — so the ``+ 1`` is named once rather than spelled at each use.

**M_shock is absorbed into lapse_rate_base.** The notes write
``w(t) = min(0.35, w_base(t) x M_shock(t) x M_money(t))`` but state the shock as three
*absolute* rates (33% / 10% / 5%) rather than as multipliers on the 6% ultimate. Carrying
``M_shock`` as a separate factor would require inventing a denominator, so
:func:`lapse_rate_base` returns :func:`shock_lapse_rate` in the shock year and
:func:`lapse_rate` multiplies only by :func:`lapse_moneyness_factor`. The name
``shock_lapse_rate`` follows :mod:`.Term_US_S` — but the **timing does not**, and the
contrast is worth stating. There the notes put the shock "in full at the end of the final
level-period month", a contractual date, so :mod:`.Term_US_S` drops the whole shock in that
one month. Here the notes state it as the surrender rate *of contract year 11*, a year that
carries no surrender charge in any of its months, so there is no date inside the year for
the decision to cluster on and :func:`lapse_rate_mth` spreads it like any other annual
rate. The one surrender that is not spread is the deemed full surrender at termination,
which is a contractual event and lands whole on the anniversary.

**d and c collide across the library.** ``d`` is the performance-trigger rate in these
notes, deaths in :mod:`.Term_US_S` and the floor's withdrawal deduction on the chassis;
``c`` is the declared cap here and the floor's contract charge on the chassis. The names
``trigger_rate``, :func:`pols_death`, :func:`mgsv_charge_pp` and :func:`cap_rate`
keep the four apart.

One name is reused deliberately and reads across cleanly. :func:`credit_rate` is the
chassis's declared effective annual rate ``i_cr(t)`` and here the index credit rate
``cr(t) = max(f, min(c, R(t)))``. Different formulas, but the same concept — the rate at
which interest is credited for the contract year — so the name is kept rather than split.

.. rubric:: Timing arguments

Account value, following ``CashValue_SE``'s ``av_pp_at`` and named for the processing step
each precedes:

``"BEF_PREM"``
    the balance carried into month ``t`` **before** the single premium: zero at ``t = 0``
    on a new-issue model point, and the same as ``"BEF_INV"`` everywhere else. It exists so
    that the account-value roll-forward closes on the first month too, the premium being a
    beginning-of-month flow rather than a row of its own.
``"BEF_INV"``
    the balance opening month ``t`` after the premium: ``av_pp_init()`` at the first
    projected month and ``AV(t-1)`` after it. In an anniversary month this is the notes'
    ``AV(0)`` only when the fixed allocation is zero; in general the notes' ``AV(0)`` of the
    contract year is :func:`av_pp_year_open`, eleven months earlier.
``"BEF_FEE"``
    ``AV(1)``, after the month's interest — the fixed accrual every month, plus the index
    credit in an anniversary month — and before the rider charge.
``"BEF_WD"``
    ``AV(2)``, after the rider charge, before the withdrawal. **Not floored at zero** —
    the 0% floor is on the index *credit*, not on the account value [S7].
``"EOY"``
    ``AV(t)``, after the withdrawal, floored at zero. Equal to :func:`av_pp`.

**Away from an anniversary the last three coincide**, at the opening balance plus the
month's fixed accrual, because no contractual transaction falls there.

Benefit base, named for the same steps: ``"BEF_ROLLUP"`` is the base opening the **contract
year**, ``"BEF_STEP_UP"`` is ``BB(3)`` after rollup and stack, ``"BEF_WD"`` is ``BB(4)``
after the annual step-up, and ``"EOY"`` is ``BB(t)`` after the proportional reduction. All
four steps are annual, so away from an anniversary every timing returns the opening base.
Lifetime withdrawal: ``"BEF_WD"`` is the amount payable at the contract year's anniversary,
``"EOY"`` the closing value after the same reduction; away from an anniversary both carry
the amount set at the last one, which is the income in force.

Policy counts, following the chassis: ``"BEF_DECR"`` is the count entering the month and
therefore equals :func:`pols_if` itself, ``"BEF_MORT"`` is the same (this product has no
annuitization decrement), ``"BEF_LAPSE"`` is after that month's deaths, and ``"AFT_DECR"``
is the closing count, which is also ``pols_if(t + 1)``. Both decrements are the **monthly**
rates.

Benefit ``kind`` arguments are ``"DEATH"``, ``"LAPSE"`` and ``"MATURITY"``. Any other
value of any of these raises ``ValueError``.

.. rubric:: The three phases, and why the cause of depletion matters

``ACCUM`` is deferral. ``INCOME`` starts at the first lifetime withdrawal and lasts while
an account value remains. ``DEPLETED`` is what the product is sold for: the account value
is gone, the insurer pays ``LW`` from its own funds for the rest of the covered life, no
rider charge is deducted, no index credit is computed, the surrender value and the death
benefit are zero, and **lapse is impossible**, so :func:`lapse_rate` returns zero and
``l(t+1) = l(t)(1 - q_m(t))``. ``TERMINATED`` is the same exhaustion with the guarantee
destroyed — reached when the account value is driven to zero by an excess withdrawal, a
surrender charge or a negative MVA rather than by guaranteed withdrawals and rider charges
[S1][S5][S9]. :func:`depletion_cause` carries the attribution and is evaluated *before*
the depletion test, exactly as the notes require. A model testing only ``AV <= 0`` would
either give the guarantee away after an excess withdrawal or destroy it after a legitimate
one. When the contract terminates, the survivors leave as a deemed full surrender —
:func:`lapse_rate` returns 1.0 for that contract year, and :func:`lapse_rate_mth` puts the
whole of it in the anniversary month rather than spreading it, because the contract "as
well as the rider will be considered Surrendered" [S5] on that date — so the in-force
roll-forward still closes.

The transition itself is annual and is tested only at the anniversary, which costs nothing:
the account value can reach zero only where a withdrawal or a charge is taken, and both
fall there. Between anniversaries :func:`phase` simply carries :func:`phase_open`.

**The asymmetry reaches the cash, not only the phase label.** On the exhaustion
anniversary itself the withdrawal requested exceeds what the account value can meet. In
``DEPLETED`` the insurer funds the whole shortfall, because that is the guarantee. On the
``TERMINATED`` branch it funds none of it: the balance is gone and the rider that would
have covered the rest is destroyed by the very withdrawal being paid, and [S5] treats the
contract as surrendered at that point. :func:`wd_unfunded_pp` is that unpayable part, and
:func:`wd_payment_pp`, :func:`wd_guar` and :func:`wd_excess` are all net of it. The cap is
on the *payment* only — :func:`wd_pp` still carries the amount requested, so the excess
still sets :func:`depletion_cause`, still drives ``rho`` to 1 and still takes the benefit
base to zero.

.. rubric:: pols_maturity and the projection horizon

The technical notes state no projection horizon; the ``DEPLETED`` liability is a life
annuity, so the model runs through the final month of the contract year *entered* at
attained age ``maturity_age`` = 120 **[std]**, the terminal age of the shipped mortality
table — ``proj_len() = 12 * policy_term()`` months. The survivors of the last month leave
through :func:`pols_maturity`, zero at every other ``t``, so that

    pols_if(t) - pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)

holds for every ``t``, including the last, ``t = proj_len() - 1``, where
``pols_if(proj_len())`` is zero. Under the shipped table ``q`` reaches 1.000000 at age 120,
hence a monthly rate of 1.0 in the first month of that contract year, so the projection
closes itself and the term is numerically zero; it is kept because a substituted table with
no terminal age would make it bite, and because without it the last month would appear to
lose lives with no cause. The name follows ``BasicTerm_S.pols_maturity`` and the
construction follows :mod:`.Term_US_S`.
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


def policy_id():
    """The contract identifier of the selected model point."""
    return model_point()["policy_id"]


def age_at_entry():
    """x: the issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the selected model point, M or F."""
    return model_point()["sex"]


def tax_status():
    """Tax status of the contract, NQ or Q.

    Reported only.  The base run is non-qualified **[std]**; no RMD module is
    implemented, though the notes make the RMD age a behavioural input through
    :func:`activation_rate` and the ``rmd_age`` Reference.
    """
    return model_point()["tax_status"]


def premium_pp():
    """P: the single premium per contract."""
    return float(model_point()["premium"])


def pols_if_init():
    """l(0): in-force probability at entry, 1 for a single-contract model point."""
    return float(model_point()["pols_if_init"])


def entry_year():
    """The completed contract years behind the model point when it enters the projection.

    An elapsed count of whole years, which :func:`entry_mth` turns into the index of the
    model point's **first projected month**, ``12 * entry_year()``.  ``0`` for a new issue,
    whose month ``0`` carries the premium, the acquisition expense and the notes'
    Initialisation block as its opening state and beginning-of-month flows.  A positive
    value enters the contract **in force** on balances stated in the model point table,
    which is what the worked example does: its anniversary-7 balances are described as
    illustrative and broadly consistent with a seven-year deferral **[std]**, not derived
    from one, so deriving them would mean retuning assumptions to force a match.  Every
    recursion opens here.
    """
    return int(model_point()["entry_year"])


def entry_mth():
    """The model point's first projected **month**, ``12 * entry_year()``.

    The frame is ``t = entry_mth() … proj_len() - 1``.  ``0`` for a new issue, whose month
    ``0`` carries the premium, the acquisition expense and the notes' Initialisation block
    as its opening state and beginning-of-month flows.  Elapsed time is stated in completed
    contract years, so the frame always opens on an anniversary and every recursion opens
    here.
    """
    return 12 * entry_year()


def bonus_rate():
    """b: the premium bonus rate, 7% of the single premium [S5]."""
    return float(model_point()["bonus_rate"])


def alloc_indexed():
    """The share of the account value allocated to the indexed account; 100% **[std]**."""
    return float(model_point()["alloc_indexed"])


def alloc_fixed():
    """The share allocated to the fixed account, ``1 - alloc_indexed()``."""
    return 1.0 - alloc_indexed()


def glwb_elected():
    """Whether the GLWB rider is elected at issue [S5][S9][S11]."""
    return bool(model_point()["glwb_elected"])


def glwb_basis():
    """``single`` or ``joint``.

    The joint column of the payout table is the single column less 0.50%, read on the
    younger covered person [S1][S3].  Joint-life *survivorship* is **not implemented**:
    the notes specify the joint payout percentage but no second-life mortality basis.
    """
    return model_point()["glwb_basis"]


def joint_age():
    """The issue age (ANB) of the joint covered person; the annuitant's own if blank."""
    given = model_point()["joint_age"]
    return age_at_entry() if pd.isna(given) else int(given)           # noqa: F821


def income_start_age():
    """The attained age at which the base run takes its first lifetime withdrawal.

    The deterministic run activates here rather than on the ``h(a)`` incidence table,
    which the notes say clusters at the RMD age but which cannot be applied to a single
    deterministic cell; see :func:`activation_rate`.
    """
    return int(model_point()["income_start_age"])


def utilization_intensity():
    """The fraction of ``LW`` actually withdrawn once income starts.

    1.00 in the base run **[std]**; the majority of users withdraw 95%-105% of the
    maximum [R1].  **The 1.05 case is an excess withdrawal** and routes through the
    proportional reduction of step 5, which is why efficiency and excess-withdrawal
    assumptions cannot be set independently.
    """
    return float(model_point()["utilization_intensity"])


def credit_method():
    """The crediting method: ``cap``, ``par``, ``par_cap``, ``spread`` or ``trigger``.

    All five are implemented in :func:`credit_rate_on`.  The notes' sixth variant,
    monthly sum with a monthly cap, is **not implemented**: it needs a monthly grid,
    which the notes exclude, and its floor convention is itself flagged as ambiguous
    [S4][R1].
    """
    return model_point()["credit_method"]


def cap_rate():
    """c: the declared annual cap, 5.25% [S2].

    A non-guaranteed element captured as of 07/01/2022, revisable under ASOP No. 2
    [R6][REG-R26].  Holding it constant for forty years is a strong implicit assumption;
    re-declaration against the option budget is **not implemented** because the notes
    give the target but no option-pricing function.
    """
    return float(model_point()["cap_rate"])


def stack_factor():
    """m: the stacking factor on realised dollar credits, 150% [S8][S9].

    Zero gives the pure-rollup design (a); with ``rollup_rate`` zero it gives the pure
    stacking design (b), where one carrier's 250% election credits 250% to the benefit
    base [S3][S4].
    """
    return float(model_point()["stack_factor"])


def av_int_factor():
    """kappa: the share of the index credit that reaches the account value [S3][S4].

    1.00 on the blended baseline.  0.50 is the 250% election documented at one carrier,
    which credits 250% of index interest to the benefit base but only 50% to the account
    value, deliberately starving the account value.  The stacking factor ``m`` applies to
    the **gross** index credit, not to ``kappa x IC``.
    """
    return float(model_point()["av_int_factor"])


def rollup_id():
    """The guaranteed rollup schedule, a key into *rollup_table.csv*."""
    return model_point()["rollup_id"]


def mva_ref_yield_at_issue():
    """i0: the MVA reference index level locked at issue, 3.00% **[std]**."""
    return float(model_point()["mva_ref_yield_at_issue"])


def scenario_id():
    """The index and reference-yield scenario, a key into *rate_scenario.csv*."""
    return model_point()["scenario_id"]


def wd_schedule_id():
    """The ad hoc withdrawal programme, a key into *withdrawal_table.csv*."""
    return model_point()["wd_schedule_id"]


def av_pp_init():
    """AV at entry: the stated in-force balance, else ``P x (1 + b)`` [S5].

    The bonus is credited to the **account value** at issue and earns index credits from
    day one [S5]; it does **not** enter the benefit base [S9] or the nonforfeiture base
    [S10].
    """
    given = model_point()["av_initial"]
    if pd.isna(given):                                               # noqa: F821
        return premium_pp() * (1.0 + bonus_rate())
    return float(given)


def av_fixed_pp_init():
    """F at entry: the fixed account share of :func:`av_pp_init`, allocated as premium."""
    return alloc_fixed() * av_pp_init()


def benefit_base_pp_init():
    """BB at entry: the stated in-force base, else ``P`` -- the bonus stays out [S9]."""
    if not glwb_elected():
        return 0.0
    given = model_point()["bb_initial"]
    if pd.isna(given):                                               # noqa: F821
        return premium_pp()
    return float(given)


def rollup_base_pp_init():
    """RB at entry: the stated in-force rollup base, else ``P`` [S2][S9]."""
    if not glwb_elected():
        return 0.0
    given = model_point()["rb_initial"]
    if pd.isna(given):                                               # noqa: F821
        return premium_pp()
    return float(given)


def mgsv_pp_init():
    """MGV at entry: the stated in-force floor, else 87.5% of premium [S10][R2].

    87.5% of the single premium **excluding the bonus** [S10]; the worked example's
    ``93,811.84 = 87,500 x 1.01^7`` is that value rolled forward seven years.
    """
    given = model_point()["mgv_initial"]
    if pd.isna(given):                                               # noqa: F821
        return net_consideration_ratio * premium_pp()                # noqa: F821
    return float(given)


def lw_pp_init():
    """LW at entry: zero before exercise, else the stated in-force income amount."""
    given = model_point()["lw_initial"]
    return 0.0 if pd.isna(given) else float(given)                   # noqa: F821


def payout_rate_init():
    """The payout percentage already locked at entry; zero before exercise."""
    given = model_point()["payout_rate_initial"]
    return 0.0 if pd.isna(given) else float(given)                   # noqa: F821


def phase_init():
    """The phase at entry: ``ACCUM`` unless the model point enters in force in income."""
    value = model_point()["phase_initial"]
    if value not in ("ACCUM", "INCOME", "DEPLETED", "TERMINATED"):
        raise ValueError("invalid phase_initial")
    return value


def policy_term():
    """Contract term in years **[std]**: through the year entered at ``maturity_age``.

    ``maturity_age`` = 120 is the terminal age of the mortality basis, where the annual
    rate is 1.000000, so the projection closes itself rather than being truncated: the
    last contract year is the one *entered* at that age, hence the ``+ 1``.  The notes
    state no horizon, and the ``DEPLETED`` liability is a life annuity, so stopping
    earlier would silently drop the tail the product is sold for.
    """
    return maturity_age - age_at_entry() + 1                          # noqa: F821


def proj_len():
    """The number of contract **months** projected, ``12 * policy_term()``.

    The **exclusive end** of the frame counted from ``t = 0``: ``result_cf()`` runs
    ``t = entry_mth() … proj_len() - 1``, so its last row is the final month of the
    contract year entered at attained age ``maturity_age``.
    """
    return 12 * policy_term()


def policy_year(t):
    """The contract year month ``t`` falls in: ``duration(t) + 1``, the 1-based label.

    Derived from ``t``, never indexed by.  It is the key that reads the surrender charge,
    the vesting vector and the rollup schedule, all of which the sources state by contract
    year, and it is the year whose annual decrement rates :func:`mort_rate` and
    :func:`lapse_rate` return.
    """
    return duration(t) + 1


def duration_mth(t):
    """Completed contract months at the start of month ``t``: ``t`` itself.

    The cells exists so the monthly vocabulary reads the same here as in
    :mod:`.Term_US_S` and ``savings.CashValue_SE``; an in-force model point opens the
    frame at ``entry_mth()`` rather than re-basing ``t``.
    """
    return t


def duration(t):
    """Completed contract years at the start of month ``t``, ``duration_mth(t) // 12``.

    Every contractual schedule in this product is annual, so this is what the attained
    age, the surrender charge, the vesting vector, the rollup schedule and the scenario
    tables are read at.
    """
    return duration_mth(t) // 12


def is_anniv(t):
    """True in the **last month of a contract year**, where every annual event lands.

    ``duration_mth(t) % 12 == 11``.  All eight of the notes' processing steps are
    contractually annual — the point-to-point index credit [S2][S4][S10], the rider charge
    [S9], the benefit base rollup, stack and step-up [S9], the lifetime withdrawal, the
    charges and the phase transition — so all eight happen here and nowhere else.  What
    the finer grid carries between anniversaries is the fixed-account accrual, the
    Model #805 roll, the decrements and the maintenance expense.
    """
    return duration_mth(t) % 12 == 11


def anniv_mth(t):
    """The month that **closes** the contract year of month ``t``: ``12 * duration(t) + 11``.

    Equal to ``t`` itself when :func:`is_anniv` is true.  It is where the annual
    quantities of that contract year are evaluated — which is what makes
    :func:`lapse_rate` a property of the year rather than of the month.
    """
    return 12 * duration(t) + 11


def year_open_mth(t):
    """The month whose **closing** value opens the contract year of month ``t``.

    ``12 * duration(t) - 1``, the anniversary closing the previous contract year.  It
    falls below ``entry_mth()`` in the first projected contract year, where the notes'
    Initialisation values stand in — which is the test every annual state cells makes.
    """
    return 12 * duration(t) - 1


def age(t):
    """x + duration(t): the attained age (ANB) **opening** the contract year of month t.

    The library convention of :mod:`.Term_US_S` and :mod:`.MYGA_US_S`, so :func:`mort_rate`
    reads this age directly for the contract year of mortality it covers.  Age changes on
    the anniversary, not on the birthday and not monthly.  The transactions of that
    contract year fall at its *closing* anniversary and are one year older: that age is
    :func:`exercise_age`, which is what reads the lifetime withdrawal percentage table.
    """
    return age_at_entry() + duration(t)


def covered_age(t):
    """The attained age of the covered life opening the contract year of month t.

    The annuitant's own age on a single-life basis; the **younger** covered person's on a
    joint-life basis [S1][S3].  Timed like :func:`age`, at the opening anniversary; the
    payout percentage and the minimum exercise age are read at :func:`exercise_age`.
    """
    if glwb_basis() == "joint":
        return min(age_at_entry(), joint_age()) + duration(t)
    return age(t)


def exercise_age(t):
    """``covered_age(t) + 1``: the covered age at the anniversary closing the contract year.

    All transactions occur **at** the anniversary and are processed as the last events of
    the contract year ending there **[std]**, so a lifetime withdrawal taken in the
    contract year of month ``t`` is taken one year older than the age opening it.  This is
    the age that reads the payout percentage band and that clears the contractual minimum
    exercise age of 50: the anchor cell's exercise in contract year 8, from issue age 62,
    is at attained age 70 and reads the 70-79 band.
    """
    return covered_age(t) + 1


def scenario_value(y, name):
    """Step-function lookup of column ``name`` in the model point's scenario at anniversary ``y``.

    **The argument is an anniversary number, not the frame's month index.** The ``t``
    column of *rate_scenario.csv* is an anniversary number, ``0`` at issue, and the file's
    keys are read unshifted; callers pass ``duration(t)`` for the anniversary opening the
    contract year of month ``t`` and ``duration(t) + 1`` for the one closing it.  Each row
    states the level that holds from its own anniversary until the next row of the same
    scenario, so a flat path is one row.  Anniversaries before the first row take the
    first row's level.
    """
    sub = data.rate_scenario().loc[scenario_id()]                    # noqa: F821
    keys = [i for i in sub.index if i <= y]
    key = max(keys) if keys else min(sub.index)
    return float(sub.loc[key, name])


def index_level(y):
    """I(y): the index level at anniversary ``y``.

    **Keyed by anniversary number, not by the frame's month index** — a time-point
    reading, so the return over a contract year differences this level against the next
    anniversary's.  The S&P 500 **price** index in the composite; dividends are excluded
    [S2][S6][R1].
    """
    return scenario_value(y, "index_level")


def index_return(t):
    """R(t) = I(y+1)/I(y) - 1 with ``y = duration(t)``: the return over the contract year.

    The point-to-point segment runs from the anniversary opening the contract year of
    month ``t`` to the one closing it, where it matures.  The return is a property of the
    contract year, not of the month, and is the same for every month inside it.
    """
    y = duration(t)
    prior = index_level(y)
    if prior <= 0.0:
        return 0.0
    return index_level(y + 1) / prior - 1.0


def cap_rate_in_force():
    """c(t): the annual cap actually applied.

    The declared 5.25% snapshot held level **[std]**, never below the guaranteed minimum
    cap of 0.25% [S4].  Set ``use_guaranteed_scale = True`` to run the contract on its
    guaranteed minimums instead — the notes insist the guaranteed and current scales are
    different assumption classes and "must not be mixed in the code".
    """
    if use_guaranteed_scale:                                         # noqa: F821
        return cap_rate_min                                          # noqa: F821
    return max(cap_rate_min, cap_rate())                             # noqa: F821


def fixed_rate_in_force():
    """i_F: the fixed account rate applied, 2.30% declared over a 1.00% guarantee.

    Declared [S2] and guaranteed minimum [S10]; ``use_guaranteed_scale`` switches to the
    guarantee, as for the cap.
    """
    if use_guaranteed_scale:                                         # noqa: F821
        return fixed_rate_min                                        # noqa: F821
    return max(fixed_rate_min, fixed_rate)                           # noqa: F821


def credit_rate_on(r, method):
    """cr: the credit rate for an index return ``r`` under ``method``.

    The engine the notes require, all branches floored at ``f`` = 0%:

    ``cap`` **[std]**
        ``max(f, min(c, R))`` [S2][S4][S10][R1] — the composite's baseline.
    ``par``
        ``max(f, p x R)`` [S4][S10][R1].
    ``par_cap``
        ``max(f, min(c, p x R))``, worked at [R1] as ``min(80% x 10%, 6%) = 6%`` — which
        is where ``par_rate`` = 80% comes from, and the case
        ``test_crediting_engine_reproduces_the_R1_worked_case`` asserts.
    ``spread``
        ``max(f, p x R - s)``, the index-margin form [S8][R1].
    ``trigger``
        ``d x 1{R >= 0}``, a declared rate credited whenever the return is non-negative
        [R1]; the floor applies when it is not.

    **The notes declare the two levels these last branches need nowhere, so both are
    [std].**  They print the *forms* — ``s`` an index margin, ``d`` a performance-trigger
    rate — and neither ``technical-notes.md`` nor ``product-spec.md`` states a value for
    either, unlike the cap (5.25% [S2]) and the participation rate (80% [R1]).  The
    shipped ``spread_rate`` = 2.00% **[std]** and ``trigger_rate`` = 4.50% **[std]** are
    illustrative levels chosen only to exercise the branch, and must not be read as
    sourced parameters of the composite.

    ``index_cost_rate`` is deducted from ``R`` **before** any cap or participation rate,
    which is where a volatility-controlled index's embedded servicing cost belongs
    [S2][S10]; it is 0 in the base run **[std]**.  The monthly-sum method is not
    implemented — see :func:`credit_method`.
    """
    net = r - index_cost_rate                                        # noqa: F821
    if method == "cap":
        raw = min(cap_rate_in_force(), net)
    elif method == "par":
        raw = par_rate * net                                         # noqa: F821
    elif method == "par_cap":
        raw = min(cap_rate_in_force(), par_rate * net)               # noqa: F821
    elif method == "spread":
        raw = par_rate * net - spread_rate                           # noqa: F821
    elif method == "trigger":
        raw = trigger_rate if net >= 0.0 else floor_rate             # noqa: F821
    else:
        raise ValueError("invalid credit_method")
    return max(floor_rate, raw)                                      # noqa: F821


def credit_rate(t):
    """cr(t): the credit rate the segment of month t's contract year matures at.

    A property of the contract year, like :func:`index_return`; it is applied once, at
    the anniversary where the segment matures.
    """
    return credit_rate_on(index_return(t), credit_method())


def index_credit_pp(t):
    """IC(t) = A(0) x cr(t): the index credit on the segment maturing at month t.

    One annual segment per indexed account, created at the anniversary opening the
    contract year with the balance opening it and maturing at the anniversary closing it;
    the credit locks at maturity and cannot be lost to later declines [S1], and **it is
    not earned before then** — which is why this is zero in every month but the
    anniversary, and why the indexed balance is flat between anniversaries.  That is the
    sourced rule "withdrawals are not credited with index interest in the year they are
    taken" [S1], carried to mid-year deaths and surrenders **[std]**; crediting a part
    year would be the *daily interim value* variant the notes exclude.

    The credit base is the segment's opening balance less withdrawals from that account
    during the segment — the "Interest Credit Basis" [S6] — which collapses to the opening
    balance here because every transaction happens at an anniversary **[std]**.  Zero in
    ``DEPLETED`` and ``TERMINATED``, where steps 1-3 are skipped.
    """
    if t < entry_mth() or not is_anniv(t):
        return 0.0
    if phase_open(t) in ("DEPLETED", "TERMINATED"):
        return 0.0
    return av_indexed_pp_year_open(t) * credit_rate(t)


def fixed_interest_pp(t):
    """FI(t): interest credited to the fixed account in **month** t.

    The declared rate is an annual effective one, so the month accrues at
    ``(1 + i_F)^(1/12) - 1`` and twelve of them compound back to exactly ``i_F`` — nothing
    else touches the fixed account between anniversaries, because every contractual
    transaction falls at one.  :func:`fixed_interest_ann_pp` is the annual figure the
    benefit-base stack is computed on.
    """
    if t < entry_mth():
        return 0.0
    if phase_open(t) in ("DEPLETED", "TERMINATED"):
        return 0.0
    rate = (1.0 + fixed_rate_in_force()) ** (1.0 / 12.0) - 1.0
    return av_fixed_pp_at(t, "BEF_INV") * rate


def fixed_interest_ann_pp(t):
    """FI over the contract year closing at the anniversary in month ``t``: ``F(0) x i_F``.

    On the balance **opening** that contract year.  The twelve monthly accruals of
    :func:`fixed_interest_pp` compound to exactly this, so the annual figure is computed
    directly rather than accumulated — which is what keeps the benefit-base stack, and
    through it the whole guarantee, identical to the annual grid's.
    """
    if t < entry_mth() or not is_anniv(t):
        return 0.0
    if phase_open(t) in ("DEPLETED", "TERMINATED"):
        return 0.0
    return av_fixed_pp_year_open(t) * fixed_rate_in_force()


def inv_income_pp(t):
    """Interest credited to one contract's account value in month t.

    ``kappa x IC(t) + FI(t)``: the fixed accrual every month, and the index credit only in
    the anniversary month where the segment matures.  ``kappa`` starves the account value
    in the pure-stacking design [S3]; the benefit-base stack in :func:`stack_pp` uses the
    **gross** index credit, which is the whole point of that design.
    """
    return av_int_factor() * index_credit_pp(t) + fixed_interest_pp(t)


def rider_charge_pp(t):
    """Phi(t) = phi x BB(0): the GLWB rider charge, deducted once a year [S9].

    On the **benefit base**, not the account value, and taken **after** index credits are
    added — the notes' ordering, which is why the base in the formula is the *opening*
    base.  In the worked example the base closes at 1.59 times the account value, so
    charging on the account value would understate the deduction by a growing margin.
    Deducted from the fixed account first and then proportionately across indexed
    accounts [S9].  ``phi`` is fixed for fifteen contract years and never exceeds 1.50%
    [S9]; re-declaration after that is not implemented.  **Once the account value is
    exhausted the charge stops** — there is nothing to deduct it from and income
    continues [S9].

    The charge is annual by contract [S9], so on the monthly grid it lands whole on the
    anniversary rather than being spread over the year; the monthly deduction documented
    at one carrier is a variant this composite does not adopt **[std]**.
    """
    if t < entry_mth() or not is_anniv(t):
        return 0.0
    if not rider_in_force_open(t):
        return 0.0
    if phase_open(t) in ("DEPLETED", "TERMINATED"):
        return 0.0
    return (min(rider_charge_rate, rider_charge_rate_max)             # noqa: F821
            * benefit_base_pp_at(t, "BEF_ROLLUP"))


def av_pp_at(t, timing):
    """AV per contract in **month** t, read at the point given by ``timing``.

    ``"BEF_PREM"`` is the balance carried into the month before the single premium, zero
    at ``t = 0`` on a new issue; ``"BEF_INV"`` is the balance opening the month after it,
    which is ``av_pp_init()`` at the first projected month and ``AV(t-1)`` after that;
    ``"BEF_FEE"`` is after the month's interest — the fixed accrual every month, plus the
    index credit in an anniversary month; ``"BEF_WD"`` is after the rider charge; ``"EOY"``
    is after the withdrawal.  **In a month that is not an anniversary the last three
    coincide**, at the opening balance plus the fixed accrual, because every contractual
    transaction falls at an anniversary.

    Only ``"EOY"`` is floored at zero: **the 0% floor is on the index credit, not on the
    account value** [S7], so ``"BEF_WD"`` may legitimately sit below the opening balance or
    below zero when the rider charge exceeds the credit.  Flooring it would silently remove
    the charge drag that produces depletion.
    """
    if t < entry_mth():
        return av_pp_init()
    if timing == "BEF_PREM":
        return 0.0 if t == entry_mth() == 0 else av_pp_at(t, "BEF_INV")
    opening = av_pp_init() if t == entry_mth() else av_pp(t - 1)
    if timing == "BEF_INV":
        return opening
    val = opening + inv_income_pp(t)
    if timing == "BEF_FEE":
        return val
    val = val - rider_charge_pp(t)
    if timing == "BEF_WD":
        return val
    if timing == "EOY":
        return max(0.0, val - wd_pp(t))
    raise ValueError("invalid timing")


def av_pp(t):
    """AV(t): the account value per contract closing **month** t, after all processing."""
    return av_pp_at(t, "EOY")


def av_pp_year_open(t):
    """AV(0): the account value **opening** the contract year containing month ``t``.

    The balance the annual index credit and the free withdrawal allowance are computed on:
    the closing value of the anniversary before, or the Initialisation value in the first
    projected contract year.  On an annual grid this would simply be the previous row's
    close; on the monthly grid the previous *month* is not the previous *year*, which is
    what this cells exists to keep straight.
    """
    prev = year_open_mth(t)
    return av_pp_init() if prev < entry_mth() else av_pp(prev)


def av_fixed_pp_year_open(t):
    """F(0): the fixed account balance opening the contract year containing month ``t``."""
    prev = year_open_mth(t)
    return av_fixed_pp_init() if prev < entry_mth() else av_fixed_pp(prev)


def av_indexed_pp_year_open(t):
    """A(0): the indexed balance opening the contract year — the segment's credit base."""
    return av_pp_year_open(t) - av_fixed_pp_year_open(t)


def av_fixed_pp_at(t, timing):
    """F per contract in month t; see :func:`av_pp_at` for ``timing``.

    The fixed account is the one balance that moves between anniversaries: it accrues at
    ``(1 + i_F)^(1/12) - 1`` every month.  The rider charge comes out of it **first** and
    only then proportionately across the indexed accounts [S9].  The notes give no
    allocation rule for withdrawals, so they are taken **pro rata** across the two accounts
    **[std]**; with the baseline 100% indexed allocation neither rule is visible.
    """
    if t < entry_mth():
        return av_fixed_pp_init()
    if timing == "BEF_PREM":
        return 0.0 if t == entry_mth() == 0 else av_fixed_pp_at(t, "BEF_INV")
    opening = av_fixed_pp_init() if t == entry_mth() else av_fixed_pp(t - 1)
    if timing == "BEF_INV":
        return opening
    val = opening + fixed_interest_pp(t)
    if timing == "BEF_FEE":
        return val
    val = max(0.0, val - rider_charge_pp(t))
    if timing == "BEF_WD":
        return val
    if timing == "EOY":
        total = av_pp_at(t, "BEF_WD")
        if total <= 0.0:
            return 0.0
        share = min(1.0, max(0.0, wd_pp(t) / total))
        return max(0.0, val * (1.0 - share))
    raise ValueError("invalid timing")


def av_fixed_pp(t):
    """F(t): the fixed account balance per contract closing month t."""
    return av_fixed_pp_at(t, "EOY")


def av_indexed_pp_at(t, timing):
    """A per contract in month t: ``AV - F`` at the same timing, by construction."""
    return av_pp_at(t, timing) - av_fixed_pp_at(t, timing)


def av_indexed_pp(t):
    """A(t): the indexed account balance per contract closing month t.

    Flat between anniversaries — the segment credits only at maturity — and stepped at
    each anniversary by that year's index credit net of its share of the charge and the
    withdrawal.
    """
    return av_indexed_pp_at(t, "EOY")


def av_depletion_pp(t):
    """The part of month t's withdrawal the account value could not fund.

    Zero until the account value runs out, then the shortfall between the withdrawal
    requested and the balance available to meet it.  It is the term that makes the
    account value roll-forward close across the depletion anniversary, where ``AV(t)`` is
    floored at zero.

    **It is not the same thing as an amount paid.** Whether the shortfall is a payment
    depends on which exhaustion branch the anniversary closes on: in ``DEPLETED`` the
    guarantee is alive and the insurer funds it from its own funds [S1][S3][S9][R1], on
    the ``TERMINATED`` branch there is neither balance nor promise behind it and it is
    not paid at all.  :func:`wd_unfunded_pp` carries that half, and only that half is
    kept out of the ledger.
    """
    if t < entry_mth():
        return 0.0
    return max(0.0, wd_pp(t) - av_pp_at(t, "BEF_WD"))


def surr_charge_rate(t):
    """sc(t): the surrender charge percentage of month t's contract year [S5].

    9.1, 9, 8, 7, 6, 5, 4, 3, 2, 1% over the ten-year charge period and zero thereafter;
    the last row of the table holds for every later year.  The table is keyed by the
    contractual 1-based contract year, ``policy_year(t)``, so the rate is the same in every
    month of a year.
    """
    table = data.surr_charge_table()                                 # noqa: F821
    key = min(policy_year(t), int(table.index.max()))
    return float(table.loc[key, "surr_charge_rate"])


def vest_rate(t):
    """v(t): the vested percentage of the premium bonus in month t's contract year [S5].

    0, 10, ..., 100% over eleven contract years, read at ``policy_year(t)``.  On
    **death** 100% vests immediately [S5], which is why the death benefit carries no
    clawback.
    """
    table = data.surr_charge_table()                                 # noqa: F821
    key = min(policy_year(t), int(table.index.max()))
    return float(table.loc[key, "vest_rate"])


def rollup_rate(t):
    """g(t): the guaranteed simple rollup rate of month t's contract year [S2][S9].

    Read as a step function of the contract year ``policy_year(t)`` from the model
    point's schedule: the blended baseline is 5.00% in years 1-10, 2.00% in years 11-20 and
    zero after [S2]; another documented design is a flat 3.00% over fifteen anniversaries
    [S9].
    """
    sub = data.rollup_table().loc[rollup_id()]                       # noqa: F821
    keys = [y for y in sub.index if y <= policy_year(t)]
    if not keys:
        return 0.0
    return float(sub.loc[max(keys), "rollup_rate"])


def payout_rate(a, basis):
    """pi(a, basis): the lifetime withdrawal percentage at attained age ``a`` [S3].

    Five inclusive attained-age bands; the joint column is the single column less 0.50%
    [S1][S3].  Zero below the first band, because no lifetime withdrawal is permitted
    there; the last band holds above its upper age.
    """
    if basis == "single":
        column = "payout_rate_single"
    elif basis == "joint":
        column = "payout_rate_joint"
    else:
        raise ValueError("invalid glwb_basis")
    table = data.payout_rate_table()                                 # noqa: F821
    for _, row in table.iterrows():
        if int(row["age_lo"]) <= a <= int(row["age_hi"]):
            return float(row[column])
    last = table.iloc[-1]
    return float(last[column]) if a > int(last["age_hi"]) else 0.0


def payout_rate_locked(t):
    """The payout percentage in force in the contract year of month t.

    Locked at the attained age of the **first** lifetime withdrawal, :func:`exercise_age`,
    and not re-read afterwards **[std]**.  :func:`is_exercise` is a property of the
    contract year, so the lock holds for every month of the year it is set in and is then
    carried from anniversary to anniversary.  Documented alternatives: one carrier reads
    the band from the age at the most recent anniversary, letting it step up [S3]; another
    makes it depend on both issue age and the youngest covered person's age at exercise
    [S9]; a third uses sex-distinct factors [S5].
    """
    if t < entry_mth():
        return payout_rate_init()
    if is_exercise(t):
        return payout_rate(exercise_age(t), glwb_basis())
    prev = year_open_mth(t)
    if prev < entry_mth():
        return payout_rate_init()
    return payout_rate_locked(prev)


def activation_rate(a):
    """h(a): the GLWB activation incidence at attained age ``a`` **[std]**.

    ``0`` below 60, 5% from 60 to the RMD age, 40% at it and 15% above [R1][REG-R64].
    ``rmd_age`` is a configurable Reference and **must not be hard-coded**: the statutory
    age is set by IRC 401(a)(9) as amended by SECURE 2.0 and finalized in T.D. 10001
    [REG-R57][REG-R58] and is not printed in the retrieved research material.

    **Reported only.** A single deterministic cell cannot activate a fraction of itself,
    so the base run exercises at the model point's ``income_start_age`` instead; this
    cells exists so the incidence assumption is visible and testable rather than implied.
    """
    if a < activation_age_low:                                       # noqa: F821
        return 0.0
    if a < rmd_age:                                                  # noqa: F821
        return activation_rate_early                                 # noqa: F821
    if a == rmd_age:                                                 # noqa: F821
        return activation_rate_rmd                                   # noqa: F821
    return activation_rate_late                                      # noqa: F821


def is_exercise(t):
    """True through the contract year whose closing anniversary carries the **first** LW.

    Requires an in-force rider, the ``ACCUM`` phase opening the year and an
    :func:`exercise_age` at or above both the contractual minimum of 50 [S2][S3][S9] and
    the model point's ``income_start_age``.  It depends only on the state **opening** the
    contract year, which is what lets the phase, the benefit base and the withdrawal be
    evaluated without a circular reference — and what makes it constant across the year,
    so every month of the exercise year reads the same phase and the same locked payout
    percentage.
    """
    if t < entry_mth():
        return False
    if not glwb_elected():
        return False
    prev = year_open_mth(t)
    prior = phase_init() if prev < entry_mth() else phase(prev)
    if prior != "ACCUM":
        return False
    if not rider_in_force_open(t):
        return False
    return exercise_age(t) >= max(min_income_age, income_start_age())  # noqa: F821


def phase_open(t):
    """The phase the annual steps of month t's contract year are processed under.

    The phase **opening the contract year** — ``phase_init()`` in the first projected year
    and the closing phase of the previous anniversary after that — promoted to ``INCOME``
    when the first lifetime withdrawal falls in this year.  Constant across the twelve
    months, because every one of the eight steps belongs to the year rather than to the
    month.  Steps 1-3 are skipped when this is ``DEPLETED`` and steps 1-7 when it is
    ``TERMINATED``.
    """
    if t < entry_mth():
        return phase_init()
    prev = year_open_mth(t)
    opening = phase_init() if prev < entry_mth() else phase(prev)
    if opening == "ACCUM" and is_exercise(t):
        return "INCOME"
    return opening


def depletion_cause(t):
    """True when a charge, an excess withdrawal or a negative MVA touched the AV in month t.

    The attribution test of step 5, evaluated **before** the depletion test: an account
    value run to zero by an excess withdrawal, a surrender charge or a market value
    adjustment loses the guarantee entirely, while one run to zero by guaranteed
    withdrawals and rider charges keeps it [S1][S5][S9].  One carrier's confinement and
    terminal illness waivers are themselves excess withdrawals that terminate the income
    rider [S1] — a trap if waivers are added.
    """
    if t < entry_mth():
        return False
    return (wd_excess_pp(t) > 0.0 or wd_charge_pp(t) > 0.0
            or wd_mva_pp(t) < 0.0)


def phase(t):
    """The phase closing month t, after step 7's transition at the anniversary.

    Step 7 is annual and the account value can only reach zero at an anniversary — nothing
    between them takes a withdrawal or a charge — so away from one this simply carries
    :func:`phase_open`, and the transition is tested at the anniversary itself.

    ``ACCUM -> INCOME`` at the first lifetime withdrawal;
    ``INCOME -> DEPLETED`` when the account value reaches zero with no
    :func:`depletion_cause`, which is where the economic value of the guarantee sits;
    ``INCOME -> TERMINATED`` when it reaches zero *with* one; and
    ``any -> TERMINATED`` when the benefit base reaches zero [S9].  An account value
    exhausted in ``ACCUM`` terminates rather than depletes **[std]**: the notes define
    the depleted state only out of ``INCOME``, and before exercise there is no ``LW`` to
    pay.
    """
    if t < entry_mth():
        return phase_init()
    opening = phase_open(t)
    if opening == "TERMINATED":
        return "TERMINATED"
    if opening == "DEPLETED":
        return "DEPLETED"
    if not is_anniv(t):
        return opening
    if glwb_elected() and benefit_base_pp(t) <= 0.0:
        return "TERMINATED"
    if av_pp(t) <= 0.0:
        if opening == "INCOME" and not depletion_cause(t):
            return "DEPLETED"
        return "TERMINATED"
    return opening


def rider_in_force_open(t):
    """Whether the GLWB rider is alive **opening** the contract year of month t.

    ``glwb_elected()`` in the first projected contract year — an in-force model point
    enters on the rider state its row states — and :func:`rider_in_force` at the previous
    anniversary after that.  Kept as a cells of its own, like :func:`phase_open`, because
    four formulas need the opening rider state and none of them may reach for a closing
    one.
    """
    if t < entry_mth():
        return bool(glwb_elected())
    prev = year_open_mth(t)
    if prev < entry_mth():
        return bool(glwb_elected())
    return rider_in_force(prev)


def rider_in_force(t):
    """Whether the GLWB rider is still alive at the end of month t [S9].

    It terminates on the earliest of death of the covered person, the benefit base
    reduced to zero, termination of the base contract, assignment, owner cancellation on
    or after the earliest cancellation date, or a change in a covered person — with no
    refund of past charges [S9].  Death is a decrement here, and cancellation and
    assignment are not modelled, so what survives is the base-reaching-zero and
    contract-termination legs.
    """
    if t < entry_mth():
        return bool(glwb_elected())
    if not glwb_elected():
        return False
    if not rider_in_force_open(t):
        return False
    if phase(t) == "TERMINATED":
        return False
    return benefit_base_pp(t) > 0.0


def in_growth_period(t):
    """T_g: whether the benefit base still rolls up and stacks in month t's contract year.

    To the earlier of the first lifetime withdrawal and contract year 20 [S1][S2].  The
    year of exercise itself is still inside the window — the worked example credits both
    the rollup and the stack in contract year 8, the year income starts — which is why the
    test is on the phase *opening* the year.
    """
    if t < entry_mth():
        return False
    if not glwb_elected():
        return False
    if policy_year(t) > growth_period_max:                           # noqa: F821
        return False
    prev = year_open_mth(t)
    return (phase_init() if prev < entry_mth() else phase(prev)) == "ACCUM"


def step_up_applies(t):
    """Whether the annual step-up ``BB <- max(BB, AV)`` is tested at month t.

    Annual by construction, so it is tested only at the anniversary.

    **A [std] generalisation.** No retrieved document describes an automatic annual
    ratchet during deferral; documented instead are an at-exercise step-up to the
    contract value [S5], an annual benefit amount computed on the greater of base and
    account value at exercise [S9], and a never-decreasing income amount once withdrawals
    begin [S3].  ``step_up_mode = "at_exercise"`` reduces the model to those designs;
    ``"annual"`` is the superset and the baseline.  Under the blended baseline it rarely
    binds — a dollar of credit adds $1 to the account value and $1.50 to the base — but
    *rarely is not never*: on a new issue the bonus opens contract year 1 with an account
    value of ``107,000`` against a benefit base of ``100,000``, so a first contract year
    with a zero index credit gives an account value of ``106,050`` against a base of
    ``105,000`` and the step-up binds.
    """
    if not is_anniv(t):
        return False
    if not glwb_elected():
        return False
    if phase_open(t) in ("DEPLETED", "TERMINATED"):
        return False
    if step_up_mode == "annual":                                     # noqa: F821
        return True
    elif step_up_mode == "at_exercise":                              # noqa: F821
        return is_exercise(t)
    else:
        raise ValueError("invalid step_up_mode")


def rollup_pp(t):
    """rollup(t) = g(t) x RB(0): the guaranteed rollup increment, once a year.

    **A flat dollar increment, not simple interest on the grown base.** One carrier
    computes it on premium less withdrawals [S2] and another on the adjusted *initial*
    base [S9]; the latter's fifteen-year table confirms a constant $3,000 a year on a
    $100,000 adjusted initial base [S9].  Compounding it inflates the base and every
    downstream charge and payment.
    """
    if not is_anniv(t) or not in_growth_period(t):
        return 0.0
    prev = year_open_mth(t)
    opening = (rollup_base_pp_init() if prev < entry_mth()
               else rollup_base_pp(prev))
    return rollup_rate(t) * opening


def stack_pp(t):
    """stack(t) = m x max(0, IC(t) + FI(t)): the stacking credit at the anniversary.

    On **realised dollar credits**, net of any strategy fee (zero here) and floored at
    zero [S8][S9] — one specimen's separately named stacking credit.  The gross index
    credit is used, so the pure stacking design can credit 250% to the base while
    ``kappa`` sends only 50% to the account value [S3][S4].  ``FI`` here is the **annual**
    fixed interest of the contract year, :func:`fixed_interest_ann_pp`, not the
    anniversary month's own accrual.
    """
    if not is_anniv(t) or not in_growth_period(t):
        return 0.0
    return stack_factor() * max(0.0, index_credit_pp(t) + fixed_interest_ann_pp(t))


def benefit_base_pp_at(t, timing):
    """BB per contract in month t, read at the point given by ``timing``.

    ``"BEF_ROLLUP"`` is the base **opening the contract year** — ``benefit_base_pp_init()``
    in the first projected year and the base at the previous anniversary after it;
    ``"BEF_STEP_UP"`` is after the rollup and the stack; ``"BEF_WD"`` is after the annual
    step-up and is the base the lifetime withdrawal is computed on; ``"EOY"`` is after
    step 5's proportional reduction.  All four steps are annual, so away from an
    anniversary every timing returns the opening base and the benefit base is flat.

    The base is **notional**: it has no cash value, cannot be withdrawn and cannot be taken
    as a lump sum [S1][S9].
    """
    if t < entry_mth():
        return benefit_base_pp_init()
    if not glwb_elected() or not rider_in_force_open(t):
        return 0.0
    prev = year_open_mth(t)
    opening = (benefit_base_pp_init() if prev < entry_mth()
               else benefit_base_pp(prev))
    if timing == "BEF_ROLLUP":
        return opening
    val = opening + rollup_pp(t) + stack_pp(t)
    if timing == "BEF_STEP_UP":
        return val
    if step_up_applies(t):
        val = max(val, av_pp_at(t, "BEF_WD"))
    if timing == "BEF_WD":
        return val
    if timing == "EOY":
        return val * (1.0 - wd_reduction_rate(t))
    raise ValueError("invalid timing")


def benefit_base_pp(t):
    """BB(t): the GLWB benefit base per contract closing month t."""
    return benefit_base_pp_at(t, "EOY")


def rollup_base_pp(t):
    """RB(t): the rollup base closing month t.

    Reduced in the same proportion as the benefit base under the baseline **[std]**
    convention [S9], and only at an anniversary, where the reduction happens.  Set
    ``rb_wd_convention = "dollar"`` for the alternative documented at another carrier,
    ``RB(t) = max(0, RB(0) - G(t))`` — "Premium minus Withdrawals" [S2].
    """
    if t < entry_mth():
        return rollup_base_pp_init()
    prev = year_open_mth(t)
    opening = (rollup_base_pp_init() if prev < entry_mth()
               else rollup_base_pp(prev))
    if rb_wd_convention == "pro_rata":                               # noqa: F821
        return opening * (1.0 - wd_reduction_rate(t))
    elif rb_wd_convention == "dollar":                               # noqa: F821
        return max(0.0, opening - wd_pp(t))
    else:
        raise ValueError("invalid rb_wd_convention")


def lw_pp_at(t, timing):
    """LW per contract in month t, read at the point given by ``timing``.

    ``"BEF_WD"`` is the amount payable at this contract year's anniversary, after step 4's
    ratchet; ``"EOY"`` is the closing value, after step 5's proportional reduction.  The
    ratchet is annual, so away from an anniversary this carries the amount set at the last
    one — the income in force, which is what a mid-year reading of the rider state means.

    At exercise ``LW = pi x BB(4)``; afterwards the ratchet ``LW = max(LW(0), pi x BB(4))``
    applies so income never decreases [S3].  Unused ``LW`` does **not** carry forward [S9];
    one carrier is the exception, accumulating the shortfall without interest [S3].  In
    ``DEPLETED`` the amount is simply carried: there is no base to recompute it from.
    """
    if t < entry_mth():
        return lw_pp_init()
    if timing not in ("BEF_WD", "EOY"):
        raise ValueError("invalid timing")
    prev = year_open_mth(t)
    prior = lw_pp_init() if prev < entry_mth() else lw_pp(prev)
    opening = phase_open(t)
    if not is_anniv(t):
        return 0.0 if opening == "TERMINATED" else prior
    if opening == "TERMINATED":
        val = 0.0
    elif opening == "DEPLETED":
        val = prior
    elif opening == "INCOME":
        candidate = payout_rate_locked(t) * benefit_base_pp_at(t, "BEF_WD")
        val = candidate if is_exercise(t) else max(prior, candidate)
    else:
        val = 0.0
    if timing == "BEF_WD":
        return val
    return val * (1.0 - wd_reduction_rate(t))


def lw_pp(t):
    """LW(t): the lifetime withdrawal amount per contract closing month t."""
    return lw_pp_at(t, "EOY")


def wd_scheduled_pp(t):
    """The ad hoc gross withdrawal scheduled at the anniversary of month t's year, else zero.

    Read from *withdrawal_table.csv*, which is **not** a step function: a contract year
    with no row takes nothing.  **Its key column is an elapsed contract year count, not the
    frame's month index** — a row keyed ``y`` is a withdrawal at the anniversary closing
    contract year ``y + 1`` — so it is read at ``duration(t)`` and the file is unchanged by
    the move to a monthly grid.  Lifetime withdrawals are generated by the rider, not
    scheduled here.
    """
    if not is_anniv(t):
        return 0.0
    table = data.withdrawal_table()                                  # noqa: F821
    key = (wd_schedule_id(), duration(t))
    return float(table.loc[key, "wd_amount"]) if key in table.index else 0.0


def wd_pp(t):
    """G(t): the gross withdrawal taken at the anniversary in month t.

    Zero in every other month: both the lifetime withdrawal and the ad hoc schedule are
    contractually annual, so the finer grid moves no cash between anniversaries.  In
    ``INCOME``, ``utilization_intensity() x LW`` plus any scheduled ad hoc amount; in
    ``DEPLETED``, exactly ``LW``, paid by the insurer from its own funds; in ``ACCUM``,
    only the scheduled amount.  Gross by construction: a contract promising a stated net
    check would need a gross-up solve, which is not implemented.
    """
    if t < entry_mth() or not is_anniv(t):
        return 0.0
    opening = phase_open(t)
    if opening == "TERMINATED":
        return 0.0
    if opening == "DEPLETED":
        return lw_pp_at(t, "BEF_WD")
    if opening == "INCOME":
        return utilization_intensity() * lw_pp_at(t, "BEF_WD") + wd_scheduled_pp(t)
    return wd_scheduled_pp(t)


def wd_guar_pp(t):
    """min(G(t), LW(t)): the guaranteed portion of month t's withdrawal.

    A withdrawal is applied **first** against the guaranteed annual amount; that portion
    reduces the account value dollar for dollar and leaves the benefit base and the
    income amount unchanged [S9].
    """
    return min(wd_pp(t), lw_pp_at(t, "BEF_WD"))


def wd_excess_pp(t):
    """E(t) = max(0, G(t) - LW(t)): the **excess withdrawal** in month t.

    The quantity that permanently reduces the guarantee, and that destroys it entirely if
    it exhausts the account value [S1][S5][S9].  Note this is *not* the chassis's
    ``wd_excess_pp``, which is the amount exposed to the surrender charge; that is
    :func:`wd_charge_base_pp` here.  Before exercise ``LW`` is zero, so the whole
    withdrawal is an excess.
    """
    return max(0.0, wd_pp(t) - lw_pp_at(t, "BEF_WD"))


def wd_unfunded_pp(t):
    """The part of G(t) that neither the account value nor the guarantee pays.

    ``G(t) - min(G(t), max(0, AV(2)(t)))`` in a month whose closing phase is
    ``TERMINATED``; zero everywhere else.  **The two exhaustion branches are not
    symmetric, and this is where they part.**  In ``DEPLETED`` the account value is gone
    but the guarantee is alive, so the insurer pays ``LW`` from its own funds for the
    rest of the covered life [S1][S3][S9][R1] and nothing is unfunded.  On the
    ``TERMINATED`` branch the account value is driven to zero by an excess withdrawal, a
    surrender charge or a negative MVA, and "an account value run to zero by an excess
    withdrawal loses the guarantee entirely" [S1][S5][S9] — [S5] is explicit that the
    contract "as well as the rider will be considered Surrendered".  Beyond the account
    value there is then nothing to pay from: no balance and no promise.  Paying the
    requested amount in full would honour the guarantee in the very year the withdrawal
    destroys it, which is the trap the notes' attribution test exists to avoid.

    The notes write step 4 as ``AV(5)(t) = AV(2)(t) - G(t)`` with no cap because they
    write it for the funded case.  The cap here is on the **payment**, not on the
    withdrawal: :func:`wd_pp` still carries the amount requested, so the excess still
    sets :func:`depletion_cause` and still drives ``rho`` to 1 and the benefit base to
    zero.  Only :func:`wd_payment_pp` and the three ledger lines are reduced.
    """
    if t < entry_mth():
        return 0.0
    if phase(t) != "TERMINATED":
        return 0.0
    return wd_pp(t) - min(wd_pp(t), max(0.0, av_pp_at(t, "BEF_WD")))


def wd_guar_paid_pp(t):
    """The guaranteed portion of month t's withdrawal that is actually paid.

    ``min(G, LW)`` less whatever of :func:`wd_unfunded_pp` the excess could not absorb.
    The account value funds the withdrawal in the order the notes compose it — the first
    ``LW`` dollars are the guaranteed portion and the remainder is the excess [S9] — so
    an under-funded withdrawal leaves the **excess** unpaid first and eats into the
    guaranteed portion only after that **[std]**, the notes being silent on a withdrawal
    the account value cannot fund.  Equal to :func:`wd_guar_pp` in every month except a
    terminating anniversary.
    """
    return max(0.0, wd_guar_pp(t) - max(0.0, wd_unfunded_pp(t) - wd_excess_pp(t)))


def wd_excess_paid_pp(t):
    """The excess portion of month t's withdrawal that is actually paid.

    ``max(0, E(t) - wd_unfunded_pp(t))``: the excess is the first thing an under-funded
    withdrawal loses, being the part with no promise behind it.  Equal to
    :func:`wd_excess_pp` in every month except a terminating anniversary.
    """
    return max(0.0, wd_excess_pp(t) - wd_unfunded_pp(t))


def wd_cum_pp(t):
    """Wcum(t): cumulative gross withdrawals from entry to the end of month t.

    A running total over months, though only the anniversary months add to it.
    """
    if t < entry_mth():
        return 0.0
    prior = 0.0 if t == entry_mth() else wd_cum_pp(t - 1)
    return prior + wd_pp(t)


def free_wd_base(t):
    """The base of the free withdrawal amount: the AV opening the contract year of month t.

    10% of the account value at the anniversary that **opens** the contract year, available
    from contract year 1 and with no carry-forward [S1][S3][S5][S6][S9][S10]; the
    combination is **[std]**.  Fixing the base at a *known* prior value is what lets the
    chargeable amount be evaluated without a fixed point, and it is what makes the
    allowance a property of the contract year rather than of the month.
    """
    return av_pp_year_open(t)


def free_wd_allow(t):
    """FW(t) = 0.10 x AV(0): the free withdrawal amount for month t's contract year."""
    return free_wd_rate * free_wd_base(t)                            # noqa: F821


def wd_free_pp(t):
    """The free-allowance portion of the anniversary's withdrawal: the part of FW(t) it uses.

    The chassis name for this quantity (``MYGA_US_S``, ``UL_US_S``,
    ``RILA_US_S``), so the library spells the free-allowance portion
    of a withdrawal one way everywhere.  Zero away from the anniversary, where no
    withdrawal is taken and the whole allowance therefore remains against a mid-year
    surrender.

    **A [std] choice the notes flag as open.** [S9] says only that withdrawals up to the
    annual benefit amount carry no charge "even if greater than the Free Withdrawal
    Amount"; it does not say whether they *exhaust* it.  The convention here — the
    guaranteed amount consumes the free amount — is the insurer-favourable reading and is
    what the worked example uses, leaving ``12,800.00 - 10,144.16 = 2,655.84`` against
    the surrender.  The alternative leaves the whole ``FW(t)`` available against the
    excess.
    """
    if t < entry_mth() or not is_anniv(t):
        return 0.0
    if phase_open(t) == "INCOME":
        return min(free_wd_allow(t), lw_pp_at(t, "BEF_WD"))
    return min(free_wd_allow(t), wd_pp(t))


def free_wd_remain(t):
    """The free withdrawal amount left after the contract year's guaranteed withdrawal.

    The whole allowance away from an anniversary, where no withdrawal has been taken yet —
    which is what a mid-year surrender is charged against.
    """
    return free_wd_allow(t) - wd_free_pp(t)


def wd_charge_base_pp(t):
    """X(t): the part of month t's withdrawal exposed to charge, clawback and MVA.

    ``max(0, G(t) - FW(t))`` before exercise and ``max(0, E(t) - remaining free)`` after
    it **[std]** — withdrawals up to ``LW`` carry no surrender charge, no MVA and no
    bonus clawback **even when ``LW`` exceeds the free withdrawal amount** [S9].  Zero
    once the account value is gone: post-depletion income is not a chargeable withdrawal.
    """
    if t < entry_mth():
        return 0.0
    opening = phase_open(t)
    if opening in ("DEPLETED", "TERMINATED"):
        return 0.0
    if opening == "INCOME":
        return max(0.0, wd_excess_pp(t) - free_wd_remain(t))
    return max(0.0, wd_pp(t) - free_wd_allow(t))


def surr_charge_base_pp(t):
    """X(t) at a **full surrender** in month t: ``AV(t)`` less the free amount left.

    The chassis calls this ``surr_excess_pp``; renamed here only for symmetry with
    :func:`wd_charge_base_pp`, because ``E(t)`` already names a different quantity in
    these notes.  The construction is the chassis's and the source is the same [S10].
    """
    if t < entry_mth():
        return 0.0
    if phase(t) == "DEPLETED":
        return 0.0
    return max(0.0, av_pp(t) - free_wd_remain(t))


def bonus_factor():
    """b/(1+b): the factor that strips the bonus out of a bonus-inclusive account value.

    **The clawback factor is b/(1+b), not b** [S10] — the account value already contains
    the bonus, so using ``b`` over-recovers by ``(1+b)``.
    """
    return bonus_rate() / (1.0 + bonus_rate())


def bonus_clawback_on(base, vested, bonus):
    """CB = (1 - A) x [B/(1+B)] x C: the non-vested bonus recovery [S10].

    ``A`` is the vested percentage for the contract year, ``B`` the bonus percentage and
    ``C`` the gross withdrawal less the free withdrawal amount.  Worked verbatim at
    [S10]: contract year 5, bonus 16%, gross $100,000, free $7,000 gives
    ``0.70 x 0.1379 x 93,000 = 8,979``.  Written as a function of its three arguments so
    that arithmetic is testable directly.
    """
    return (1.0 - vested) * (bonus / (1.0 + bonus)) * base


def mva_ref_yield(y):
    """i_y: the MVA reference index level at anniversary ``y``, from the scenario table.

    **Keyed by anniversary number**, like :func:`index_level`, so the level in force at a
    transaction closing the contract year of month ``t`` is
    ``mva_ref_yield(duration(t) + 1)``.  A declared investment-grade corporate bond yield
    index; generic here **[std]**, and named as Barclay's US Credit Index in the
    linear-form products [S6][S7].
    """
    return scenario_value(y, "mva_ref_yield")


def mva_term(t):
    """n/12: the years remaining in the MVA period at the end of month t.

    The MVA period is the ten-year surrender charge period [S7][S10], and the notes state
    the term in **months** — which is what the monthly grid can now say exactly:
    ``surr_charge_period - (t + 1)/12``, a transaction in month ``t`` being settled at its
    end.  At the worked example's anniversary 8 — month 95, the close of contract year 8 —
    that is ``10 - 96/12 = 2`` years, the ``n = 24`` months the notes quote, so every
    anniversary value is the annual grid's; a surrender six months earlier now carries the
    30 months it actually has instead of being rounded to the anniversary.  The remaining
    term reaches zero at anniversary 10, so a transaction carries a live adjustment through
    contract year 9 and none in contract year 10.
    """
    return max(0.0, surr_charge_period - (t + 1) / 12.0)             # noqa: F821


def mva_in_force(t):
    """Whether an MVA applies to a transaction in month t.

    ``MVA = 0`` outside the MVA period and on the death benefit [S5][S6][S7][S10]; the
    second is handled where the death benefit is valued.
    """
    return mva_term(t) > 0.0


def mva_rate(t):
    """The market value adjustment rate, ``[(1+i0)/(1+it)]^(n/12) - 1`` [S10].

    Signed, and **negative when the reference yield has risen** [S10].  This is the
    ratio-of-yield-factors family, which is naturally bounded; the linear family
    ``(i0 - it) x T`` adopted by the fixed-deferred chassis [S6][S7] is unbounded and
    must be collared separately.  The FIA composite **restates** the MVA rather than
    inheriting it, which is why the chassis's ``mva_family`` switch is absent here.

    The reference yield is read at the anniversary **closing** the contract year of month
    ``t``, ``duration(t) + 1``, which is the transaction date the adjustment applies at.
    """
    if not mva_in_force(t):
        return 0.0
    return ((1.0 + mva_ref_yield_at_issue())
            / (1.0 + mva_ref_yield(duration(t) + 1))) ** mva_term(t) - 1.0


def mva_pp_on(t, base, gross):
    """The collared MVA on a currency ``base`` withdrawn as ``gross`` in month t.

    ``|MVA| <= max(0, G - SC - CB - MGV)`` [S10], so a negative MVA combined with the
    surrender charge and the clawback can never push the proceeds below the guaranteed
    minimum value, and the maximum positive adjustment cannot exceed the maximum negative
    one.  In the worked example's surrender trace the limit is
    ``max(0, 122,865.84 - 5,965.56 - 84,605.80) = 32,294.48`` and the raw
    ``-1,158.64`` sits well inside it.

    **The notes are silent on how a surrender-value collar applies to a partial
    withdrawal, and both readings are shipped.** The limit is stated on the *gross
    withdrawal*, and its stated purpose is that the adjustment "never reduces the
    surrender value below the guaranteed minimum value" — a full-surrender concept, and
    the only case the worked example demonstrates.  Read literally, a partial withdrawal
    smaller than the floor gives a non-positive limit and therefore **no adjustment at
    all**.  ``mva_collar_basis`` selects:

    ``"gross"`` **[std] default**
        the notes' literal text, ``reference = G(t)``.
    ``"surrender_value"``
        the test applied to the contract rather than to the payment,
        ``reference = AV(t)``, so a partial withdrawal carries the adjustment its rate
        produces up to what the remaining floor allows.

    **The two are identical on the surrender path**, where ``G(t) = AV(t)``, so the
    worked example reproduces under either; they differ only where the notes say nothing.
    """
    raw = mva_rate(t) * base
    if mva_collar_basis == "gross":                                  # noqa: F821
        reference = gross
    elif mva_collar_basis == "surrender_value":                      # noqa: F821
        reference = av_pp(t)
    else:
        raise ValueError("invalid mva_collar_basis")
    limit = max(0.0, reference - surr_charge_rate(t) * base
                - bonus_clawback_on(base, vest_rate(t), bonus_rate())
                - mgsv_pp(t))
    return max(-limit, min(limit, raw))


def wd_charge_pp(t):
    """SC(t) on month t's withdrawal: ``sc(t) x X(t)`` [S5][S10]."""
    return surr_charge_rate(t) * wd_charge_base_pp(t)


def wd_clawback_pp(t):
    """CB(t) on month t's withdrawal [S10]."""
    return bonus_clawback_on(wd_charge_base_pp(t), vest_rate(t), bonus_rate())


def wd_mva_pp(t):
    """MVA(t) on month t's withdrawal, collared [S10]."""
    return mva_pp_on(t, wd_charge_base_pp(t), wd_pp(t))


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``G - unfunded - SC - CB + MVA``.

    The surrender charge and the clawback are **internal transfers** within the account
    value, not fee income: the account value falls by the *gross* ``G(t)`` while the
    holder receives this.  Reporting them as income while also projecting the account
    value net of them double-counts.

    :func:`wd_unfunded_pp` is zero in every month except a terminating anniversary, where
    it strips out the part of the request the account value could not fund and the
    destroyed guarantee does not cover.  On the ``DEPLETED`` branch it stays zero and the
    whole of ``LW`` is paid, which is the guarantee.
    """
    return (wd_pp(t) - wd_unfunded_pp(t) - wd_charge_pp(t)
            - wd_clawback_pp(t) + wd_mva_pp(t))


def wd_reduction_rate_on(av, lw, gross):
    """rho for a gross withdrawal of ``gross`` against ``av`` with guaranteed amount ``lw``.

    ``E / (AV - LW)``, the post-exercise construction stated verbatim at [S9]: account
    value $100,000, base $200,000, annual benefit amount $10,000, withdrawal $28,000
    gives denominator $90,000, excess $18,000, reduction 20%, base to $160,000 and
    benefit amount to $8,000.  Passing ``lw = 0`` gives the pre-exercise form
    ``G / AV`` [S1][S3][S5][S9] — **the two denominators differ by exactly LW**, which is
    the pitfall the notes name.  ``rho = 1`` when the denominator is non-positive: the
    base goes to zero and the rider terminates [S9].
    """
    excess = max(0.0, gross - lw)
    if excess <= 0.0:
        return 0.0
    denom = av - lw
    if denom <= 0.0:
        return 1.0
    return min(1.0, excess / denom)


def wd_reduction_rate(t):
    """rho(t): the proportional reduction applied to BB, LW and RB in month t.

    Pre-exercise the denominator is the gross account value after the rider charge;
    post-exercise it is that value **net of the guaranteed amount** [S9].  Zero when
    there is no excess: a withdrawal inside ``LW`` leaves the guarantee untouched.
    """
    if t < entry_mth():
        return 0.0
    opening = phase_open(t)
    if opening in ("DEPLETED", "TERMINATED"):
        return 0.0
    if opening == "INCOME":
        return wd_reduction_rate_on(av_pp_at(t, "BEF_WD"),
                                    lw_pp_at(t, "BEF_WD"), wd_pp(t))
    return wd_reduction_rate_on(av_pp_at(t, "BEF_WD"), 0.0, wd_pp(t))


def surr_charge_pp(t):
    """SC(t) on a full surrender in month t."""
    return surr_charge_rate(t) * surr_charge_base_pp(t)


def surr_clawback_pp(t):
    """CB(t) on a full surrender closing month t [S10]."""
    return bonus_clawback_on(surr_charge_base_pp(t), vest_rate(t), bonus_rate())


def mva_pp(t):
    """MVA(t) on a full surrender closing month t, collared [S10]."""
    return mva_pp_on(t, surr_charge_base_pp(t), av_pp(t))


def surr_value_pp(t):
    """The surrender value before the nonforfeiture floor, ``AV - SC - CB + MVA``.

    The composition order is **account value, then charge and clawback and MVA computed
    on the pre-deduction excess, then the floor** — the chassis's order, and the one
    contractual element the FIA notes inherit rather than restate.
    """
    if phase(t) == "DEPLETED":
        return 0.0
    return (av_pp(t) - surr_charge_pp(t) - surr_clawback_pp(t) + mva_pp(t))


def surr_benefit_pp(t):
    """CSV(t) = max(AV - SC - CB + MVA, MGV): the surrender benefit paid [S1][S6][S10].

    Zero in ``DEPLETED``: there is no account value and no surrender value [S1][S9].  A
    binding floor is **not** a separate cash flow — it raises the benefit, and
    ``MGV - SV`` is a reconciliation quantity only.
    """
    if phase(t) == "DEPLETED":
        return 0.0
    return max(surr_value_pp(t), mgsv_pp(t))


def mgsv_charge_pp(t):
    """The annual contract charge deducted from the Model #805 floor, at the anniversary.

    Model #805 4.A permits $50 a year, accumulated at the nonforfeiture rate, together
    with premium tax actually paid and indebtedness [R2].  All are zero here **[std]**
    because no retrieved product declares an actual annual policy fee, which makes the
    modeled floor slightly conservative.
    """
    if t < entry_mth() or not is_anniv(t):
        return 0.0
    return mgsv_annual_charge                                        # noqa: F821


def mgsv_pp(t):
    """MGV(t): the Model #805 guaranteed minimum value closing **month** t.

    The floor accretes every month at ``(1 + i_nf)^(1/12) - 1``, so twelve months compound
    to exactly the annual nonforfeiture rate and the anniversary values are the annual
    grid's; the withdrawal is deducted at the anniversary, where it is taken.  **Accrete,
    then deduct** — the worked example pins the ordering at
    ``93,811.84 x 1.01 - 10,144.16 = 84,605.80``.  The fixed-deferred chassis deducts and
    *then* accretes; the two are different arithmetic on the same concept, which is exactly
    what that file warns against carrying across.

    Accruing monthly rather than once at the anniversary is what makes the floor mean
    something for a mid-year death or surrender, which is where it most often binds.  The
    opening value is ``0.875 x P`` excluding the bonus at issue [S10][R2].
    ``rider_charge_from_mgsv`` switches on the treatment documented at two carriers, one
    deducting the rider charge from the floor and the other its allocation charge
    [S1][S2][S3][S4]; the composite does not **[std]**.
    """
    if t < entry_mth():
        return mgsv_pp_init()
    opening = mgsv_pp_init() if t == entry_mth() else mgsv_pp(t - 1)
    accrued = opening * (1.0 + mgsv_rate) ** (1.0 / 12.0)            # noqa: F821
    if not is_anniv(t):
        return max(0.0, accrued)
    charge = rider_charge_pp(t) if rider_charge_from_mgsv else 0.0    # noqa: F821
    return max(0.0, accrued - wd_pp(t) - mgsv_charge_pp(t) - charge)


def mgsv_rate_statutory(cmt5, option_cost):
    """The Model #805 4.B/4.C indexed nonforfeiture rate [R2][R3].

    ``max(0.0015, min(0.03, round(CMT5 to 1/20 of 1%) - 0.0125 - delta))`` where
    ``delta`` is the equity-index reduction of 4.C: available only when the annualized
    option cost of the **guaranteed** index features is at least 25 basis points, and
    then equal to ``min(100 bp, option cost)``, certified annually [R3].

    Two traps the notes name.  **The 4.B floor is 15 basis points, not 1%** — the
    composite's 1.00% is a **[std]** pick inside the 0.15%-3% corridor, not the statutory
    floor.  And whether the 15 bp floor survives the 4.C reduction is not stated in the
    retrieved text [unverified]; the specimen contract language, "the interest rates will
    range between 0.15% and 3%", suggests it does [S10], which is the reading
    implemented.  The statute *defines the minimum*: the contract rate must satisfy
    ``mgsv_rate >= mgsv_rate_statutory(...)``, which is what
    :func:`mgsv_rate_is_compliant` tests, not the reverse inequality.
    """
    delta = (min(mgsv_stat_delta_max, option_cost)                   # noqa: F821
             if option_cost >= mgsv_stat_delta_gate else 0.0)        # noqa: F821
    rounded = math.floor(cmt5 / mgsv_stat_step + 0.5) * mgsv_stat_step  # noqa: F821
    return max(mgsv_stat_floor,                                      # noqa: F821
               min(mgsv_stat_cap,                                    # noqa: F821
                   rounded - mgsv_stat_spread - delta))              # noqa: F821


def mgsv_rate_is_compliant(cmt5, option_cost):
    """True when the contract nonforfeiture rate meets the statutory minimum [R2][R3]."""
    return mgsv_rate >= mgsv_rate_statutory(cmt5, option_cost)       # noqa: F821


def mort_rate(t):
    """q(t): the **annual** mortality rate of the contract year containing month t.

    Read at ``age(t)``, the attained age opening that contract year — the library
    convention of :mod:`.Term_US_S` and :mod:`.MYGA_US_S`.  The rate actually applied to a
    month is :func:`mort_rate_mth`; this cells stays annual so the table is read the way
    it is published and so the assumption is visible at the frequency it is set at.

    The shipped table is the same illustrative Makeham annuitant curve as
    ``products/fixed_deferred_annuity`` **[std]**, *not* a published basis.  The prescribed
    basis is the 2012 IAM Basic / 2012 IAR generational family with Projection Scale G2,
    ``q_x^(2012+n) = q_x^(2012) x (1 - G2_x)^n``, rounding applied from the 2012 period
    rate each time and never by compounding an already rounded rate [REG-R59][REG-R60]; it
    may not be redistributed here, so swap it in by repointing ``Data.mort_table_file``.
    Generational projection is **not implemented** for the same reason.  ``mort_ae_factor``
    carries the A/E deviation, 100% **[std]** against the 2020-2024 payout experience study
    [REG-R61]; the spelling is the library's shared one, so the A/E factor reads the same
    in every model that has one.
    """
    base = float(data.mort_table().loc[(age(t), sex()), "mort_rate"])  # noqa: F821
    return min(1.0, mort_ae_factor * base)                           # noqa: F821


def mort_rate_mth(t):
    """The monthly mortality rate, ``1 - (1 - q)^(1/12)``.

    The uniform-force conversion the library uses everywhere: twelve of these compound to
    exactly the annual rate of the contract year, so the anniversary in-force numbers are
    the annual grid's and only their distribution through the year changes.  Dividing by
    twelve instead would overstate the decrement, and the error grows with the rate.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def shock_lapse_rate(t):
    """w_shock: the surrender rate in the year the surrender charge expires [R8].

    **The single most important behavioral fact in the product.** 33% without a GLWB
    rider against 10% with one in force but not activated, and 5% **[std]** once it is
    activated, extrapolated from the finding that contracts with GLWBs lapse less than
    those without and that activated GLWBs lapse least [R1][R8].  Applying a plain
    fixed-deferred shock lapse — roughly 52%-56% for fixed-rate deferred annuities
    [REG-R63, unverified] — to an FIA with an in-force rider materially understates the
    tail the product is sold for.
    """
    if not glwb_elected() or not rider_in_force_open(t):
        return shock_lapse_no_rider                                  # noqa: F821
    if phase_open(t) == "ACCUM":
        return shock_lapse_rider_idle                                # noqa: F821
    return shock_lapse_rider_active                                  # noqa: F821


def lapse_rate_base(t):
    """w_base(t): the base annual surrender rate of month t's contract year **[std]**.

    2% in years 1-3, 3% in 4-6, 4% in 7-9, 5% in year 10, the shock in the year the
    surrender charge expires, and 6% thereafter — the shape [R1] describes: low early,
    rising through the charge period, spiking at expiry, then falling back but staying
    above pre-shock levels.  The notes' separate ``M_shock`` multiplier is absorbed here,
    because the shock is stated as an absolute rate rather than as a factor on the
    ultimate; see the Space docstring.
    """
    year = policy_year(t)
    if year == surr_charge_period + 1:                               # noqa: F821
        return shock_lapse_rate(t)
    if year <= 3:
        return lapse_base_early                                      # noqa: F821
    if year <= 6:
        return lapse_base_mid                                        # noqa: F821
    if year <= 9:
        return lapse_base_late                                       # noqa: F821
    if year <= surr_charge_period:                                   # noqa: F821
        return lapse_base_final                                      # noqa: F821
    return lapse_base_ult                                            # noqa: F821


def lapse_moneyness_factor(t):
    """M_money(t) = clamp(1 - 0.6 max(0, BB/AV - 1), 0.2, 1.0) **[std]**.

    Surrender is suppressed when the guarantee is in the money, because a rational
    surrender destroys a guarantee worth ``BB - AV`` in benefit-base terms.  The observed
    direction is documented [R1][R8]; the functional form is not.

    Evaluated on the state **closing the contract year**, at :func:`anniv_mth`, so the
    factor is a property of the year like the base rate it multiplies.  Reading it month
    by month would let the fixed-account accrual drift the ratio within the year and make
    the annual surrender assumption depend on where in the year it is sampled.
    """
    a = anniv_mth(t)
    av = av_pp(a)
    if av <= 0.0:
        return lapse_money_floor                                     # noqa: F821
    ratio = benefit_base_pp(a) / av
    return min(1.0, max(lapse_money_floor,                           # noqa: F821
                        1.0 - lapse_money_slope * max(0.0, ratio - 1.0)))  # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** surrender rate of the contract year containing month t.

    ``min(0.35, w_base(t) x M_money(t))``, and **zero in DEPLETED** — with no account
    value there is nothing to surrender, so lapse is impossible [S1][S9] and leaving the
    decrement on would silently truncate the most expensive part of the liability.  In
    the contract year the contract terminates, the survivors leave as a deemed full
    surrender [S5][S9], so this returns 1.0 there and the in-force roll-forward closes.

    Evaluated on the phase **closing** the contract year, at :func:`anniv_mth`, so it is
    one rate for the whole year; :func:`lapse_rate_mth` is what a month actually applies.
    """
    if t < entry_mth():
        return 0.0
    a = anniv_mth(t)
    if phase_open(a) == "TERMINATED":
        return 0.0
    closing = phase(a)
    if closing == "TERMINATED":
        return 1.0
    if closing == "DEPLETED":
        return 0.0
    return min(lapse_rate_max,                                       # noqa: F821
               lapse_rate_base(t) * lapse_moneyness_factor(t))


def lapse_rate_mth(t):
    """The monthly surrender rate, ``1 - (1 - w)^(1/12)``.

    The same uniform-force conversion as :func:`mort_rate_mth`, so twelve months compound
    to exactly the contract year's annual rate — including the shock in the year the
    surrender charge expires, which **is** spread.  That is deliberate and is the opposite
    of :mod:`.Term_US_S`, where the notes state the shock as a rate "applied in full at
    the end of the final level-period month": here the notes state it as the surrender
    rate *of contract year 11*, a year that carries no surrender charge in any month, so
    there is no contractual date inside it for the decision to cluster on.

    The one rate that is **not** spread is the deemed full surrender at termination.  That
    is a contractual event, not a behavioral assumption: the contract "as well as the
    rider will be considered Surrendered" [S5] at the anniversary the account value is
    destroyed, so the survivors leave in that month and not before.
    """
    w = lapse_rate(t)
    if w >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - w) ** (1.0 / 12.0)


def pols_if(t):
    """The in-force probability at the **start** of month t.

    The library convention, set by :mod:`.Term_US_S` and ``savings.CashValue_SE``: this is
    the count entering the month, before its decrements, and it is the weight carried by
    every cash flow reported on the same row of :func:`result_cf`.  At an anniversary month
    ``12k + 11`` it is the count that reaches the anniversary and therefore the weight the
    year's withdrawal and charges carry — on the annual grid that weight was the count
    entering the year, which is the one place the finer grid changes the answer rather than
    only the resolution.

    ``pols_if(entry_mth()) = pols_if_init()``, the recursion runs
    ``pols_if(t + 1) = pols_if(t)(1 - q_m(t))(1 - w_m(t))`` with death before surrender
    **[std]**, and it is zero from ``proj_len()`` on, where the survivors of the last
    projected month have left through :func:`pols_maturity`.  Because the monthly rates
    compound to the annual ones, ``pols_if(12k)`` is exactly the annual-grid model's
    ``pols_if(k)``: the notes' ``l(k)``.
    """
    if t <= entry_mth():
        return pols_if_init()
    if t >= proj_len():
        return 0.0
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """In-force in month t read at the point given by ``timing``.

    ``"BEF_DECR"`` and ``"BEF_MORT"`` are both the count entering the month, which is
    :func:`pols_if` itself — this product has no annuitization decrement, so the chassis's
    two timings coincide.  ``"BEF_LAPSE"`` is after deaths, and ``"AFT_DECR"`` is the count
    at the *end* of month t and therefore ``pols_if(t + 1)``.  Both decrements are the
    **monthly** rates.
    """
    if t < entry_mth():
        return pols_if_init()
    pols = pols_if(t)
    if timing in ("BEF_DECR", "BEF_MORT"):
        return pols
    pols = pols * (1.0 - mort_rate_mth(t))
    if timing == "BEF_LAPSE":
        return pols
    pols = pols * (1.0 - lapse_rate_mth(t))
    if timing == "AFT_DECR":
        return pols
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in month t, on the monthly mortality rate."""
    return (0.0 if t < entry_mth()
            else pols_if_at(t, "BEF_MORT") * mort_rate_mth(t))


def pols_lapse(t):
    """Full surrenders in month t, on the survivors of that month's mortality."""
    return (0.0 if t < entry_mth()
            else pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t))


def pols_maturity(t):
    """Survivors leaving at the projection horizon, non-zero only at ``proj_len() - 1``.

    Not a decrement — the horizon runs out — but needed for the in-force roll-forward to
    close.  Numerically zero under the shipped mortality table, whose annual rate reaches
    1.000000 at age 120, hence a monthly rate of 1.0, so the projection closes itself; see
    the Space docstring.
    """
    return pols_if_at(t, "AFT_DECR") if t == proj_len() - 1 else 0.0


def pols_decr(t, kind):
    """The number of contracts leaving in month t by benefit ``kind``."""
    if kind == "DEATH":
        return pols_death(t)
    elif kind == "LAPSE":
        return pols_lapse(t)
    elif kind == "MATURITY":
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def claim_pp(t, kind):
    """The benefit paid per contract at the end of month t by ``kind``.

    ``"DEATH"`` is ``max(AV(t), MGV(t))`` with 100% bonus vesting, no surrender charge
    and no MVA [S1][S2][S5][S10], and is never below the cash surrender benefit [R2 6].
    Note the FIA composite **restates** this rather than inheriting the chassis's full
    account value floored at the surrender benefit.  ``"LAPSE"`` is the surrender benefit.
    ``"MATURITY"`` is the account value floored at the guaranteed minimum at the horizon.
    All three are **zero in DEPLETED**: there is no account value, no surrender value and
    no death benefit, and the only exit is death [S1][S9].
    """
    if phase(t) == "DEPLETED":
        return 0.0
    if kind == "DEATH":
        return max(av_pp(t), mgsv_pp(t))
    elif kind == "LAPSE":
        return surr_benefit_pp(t)
    elif kind == "MATURITY":
        return max(av_pp(t), mgsv_pp(t))
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The account value released per contract by a claim of ``kind``.

    ``AV(t)`` for all three kinds; the difference from :func:`claim_pp` is
    :func:`claims_over_av`, positive when the Model #805 floor binds and negative when
    the surrender charge and a negative MVA bite.
    """
    if kind in ("DEATH", "LAPSE", "MATURITY"):
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def premiums(t):
    """Premium income: the single premium, at the **start** of month 0 on a new issue.

    There is no issue-instant row, so the premium is a beginning-of-month flow of the
    first projected month rather than a row of its own.  An in-force model point paid its
    premium before the projection starts, so this is zero throughout for it — as are the
    acquisition expense and the premium tax that key off it.
    """
    if t == 0 and entry_mth() == 0:
        return premium_pp() * pols_if_init()
    return 0.0


def prem_to_av_pp(t):
    """Premium and bonus credited to the account value per contract, at issue only."""
    return av_pp_init() if (t == 0 and entry_mth() == 0) else 0.0


def prem_to_av(t):
    """Premium and bonus credited to the block's account value, at issue only."""
    return prem_to_av_pp(t) * pols_if_init() if t == 0 else 0.0


def wd_guar(t):
    """Guaranteed withdrawal outgo in month t, weighted by ``pols_if(t)``.

    The count entering the month, which is the in-force number reported on the same row of
    :func:`result_cf`; at an anniversary that is the count which **reaches** it.
    On :func:`wd_guar_paid_pp`, not on the amount requested, so a terminating anniversary
    cannot pay a guaranteed withdrawal the account value could not fund and the destroyed
    rider no longer covers.  Zero in ``DEPLETED``, where the same payment is reported as
    :func:`income_payments` so the two lines partition the total rather than overlap.
    """
    if t < entry_mth() or phase_open(t) == "DEPLETED":
        return 0.0
    return wd_guar_paid_pp(t) * pols_if(t)


def wd_excess(t):
    """Excess withdrawal outgo in month t: ``E - unfunded - SC - CB + MVA``.

    Weighted by ``pols_if(t)``, the count entering the month, and on
    :func:`wd_excess_paid_pp`: the excess is the first part of an under-funded withdrawal to
    go unpaid.
    """
    if t < entry_mth():
        return 0.0
    net = (wd_excess_paid_pp(t) - wd_charge_pp(t) - wd_clawback_pp(t) + wd_mva_pp(t))
    return net * pols_if(t)


def income_payments(t):
    """Post-depletion income outgo: ``LW`` at the anniversary while ``phase = DEPLETED``.

    **This is the guarantee.** There is no account value behind it, no rider charge is
    deducted, and it runs for the rest of the covered life [S1][S3][S9][R1].

    Annual like every other withdrawal, so it falls in the anniversary month and is
    weighted by the contracts that **reach** it.  Paying it in each of the twelve months
    would multiply the guarantee twelvefold and break the partition
    ``withdrawals = wd_guar + wd_excess + income_payments`` that :func:`result_cf`
    documents.
    """
    if t < entry_mth() or not is_anniv(t):
        return 0.0
    if phase_open(t) != "DEPLETED":
        return 0.0
    return lw_pp_at(t, "BEF_WD") * pols_if(t)


def withdrawals(t):
    """Total withdrawal outgo in month t, ``wd_payment_pp(t) x pols_if(t)``.

    Equal to :func:`wd_guar` + :func:`wd_excess` + :func:`income_payments` in every
    month, the three lines partitioning it by the notes' ledger categories.  All
    four are published by :func:`result_cf`, so **summing every column of that frame
    double-counts the withdrawal**; the ledger identity is on the total, and the split is
    there because the notes report the three categories separately.
    """
    return 0.0 if t < entry_mth() else wd_payment_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, for one ``kind`` or, with ``kind=None``, all three."""
    if kind is None:
        return (claims(t, "DEATH") + claims(t, "LAPSE") + claims(t, "MATURITY"))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The account value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind=None):
    """Benefit paid less the account value released, ``claims - claims_from_av``.

    Signed and a reconciliation quantity only: positive exactly when the Model #805 floor
    binds, negative when the surrender charge, the clawback and a negative MVA bite.  A
    binding floor does not add a top-up cash flow — it raises the benefit.
    """
    if kind is None:
        return (claims_over_av(t, "DEATH") + claims_over_av(t, "LAPSE")
                + claims_over_av(t, "MATURITY"))
    return claims(t, kind) - claims_from_av(t, kind)


def commissions(t):
    """Acquisition commission, **zero [std]**.

    The technical notes fold the whole acquisition cost into a single 6.0%-of-premium
    acquisition *expense* and give no separate commission, so ``comm_rate_acq`` is 0 and
    this line exists for shape only.  It is kept rather than dropped because every model
    in the library carries the same cash flow vocabulary.
    """
    return comm_rate_acq * premiums(t)                               # noqa: F821


def premium_taxes(t):
    """Premium tax on the single premium, 0% on the composite state basis **[std]**."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in month t, ``1.025^(t/12)``.

    A fractional power of the annual rate, so twelve months of it compound to exactly one
    year of inflation and the factor at each anniversary is the annual grid's.
    """
    return (1.0 + inflation_rate) ** (t / 12.0)                      # noqa: F821


def expenses(t):
    """Insurer expenses: acquisition at issue and inflating maintenance monthly **[std]**.

    6.0% of the single premium in month 0 on a new issue, and $80 per contract per year
    inflating at 2.5% — **one twelfth of it a month**, weighted by the in-force at the
    start of the month.  Spreading the maintenance charge is the point of the finer grid
    for this line: it is an insurer cost accruing continuously, not a contractual event
    tied to the anniversary, so it now falls where it is incurred and is weighted by
    survivors who have not yet left.  ``premiums(t)`` is zero everywhere but the first
    month, so the acquisition term simply drops out elsewhere.  Both are standardizations:
    no retrieved document discloses FIA acquisition cost or per-contract maintenance.
    """
    if t < entry_mth() or t >= proj_len():
        return 0.0
    return (expense_acq_rate * premiums(t)                           # noqa: F821
            + expense_maint / 12.0 * inflation_factor(t) * pols_if(t))  # noqa: F821


def net_cf(t):
    """Net cash flow in month t.

    The index credit, the rider charge, the surrender charge, the bonus clawback and the
    movement of the Model #805 floor are **internal accounting entries**: they drive the
    account value, the benefit base and the benefit *amount* but are never ledger lines
    of their own.  Only amounts paid to or received from the contract holder, and the
    insurer's own expenses, appear here.
    """
    return (premiums(t) - withdrawals(t) - claims(t)
            - commissions(t) - expenses(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted account value in month t; see :func:`av_pp_at`.

    Every timing inside the month carries ``pols_if(t)`` — the count entering it — because
    all processing happens before the decrements.  ``"EOY"`` carries the count *leaving*
    the month, ``pols_if(t + 1)``: zero at the horizon, where :func:`pols_maturity` has
    taken the survivors out.
    """
    if t < entry_mth():
        return 0.0
    if timing in ("BEF_PREM", "BEF_INV", "BEF_FEE", "BEF_WD"):
        return av_pp_at(t, timing) * pols_if(t)
    if timing == "EOY":
        return av_pp(t) * pols_if(t + 1)
    raise ValueError("invalid timing")


def inv_income(t):
    """Interest credited to the whole block in month t."""
    return 0.0 if t < entry_mth() else inv_income_pp(t) * pols_if(t)


def rider_charges(t):
    """Rider charges deducted from the whole block's account value in month t."""
    return 0.0 if t < entry_mth() else rider_charge_pp(t) * pols_if(t)


def wd_from_av(t):
    """The account value released by month t's withdrawals, gross of charge and MVA."""
    return 0.0 if t < entry_mth() else wd_pp(t) * pols_if(t)


def av_depletion(t):
    """The block's withdrawal outgo the account value could not fund in month t."""
    return 0.0 if t < entry_mth() else av_depletion_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's account value over month t.

    Closing less **opening**, the opening being read at ``"BEF_PREM"`` so that the single
    premium of a new issue's month 0 is a movement rather than part of the balance brought
    in.  Away from the first month ``av_at(t, "BEF_PREM")`` is exactly the previous
    month's closing value.
    """
    return av_at(t, "EOY") - av_at(t, "BEF_PREM")


def check_av_roll_fwd_resid(t):
    """Account value roll-forward residual for month t; the signed float.

    ``AV(t) - AV(0)(t) = premium in + interest credited - rider charges - withdrawals
    + the part of a withdrawal the account value could not fund - the account value
    released by each claim kind``.  The cash *paid* on a surrender may differ from the
    account value released — by the charge, the clawback, the MVA and any binding
    Model #805 floor — and that difference is :func:`claims_over_av`, deliberately not
    part of this identity.  It closes month by month on the finer grid, where the interest
    term is the month's accrual and the claim terms are that month's exits.

    The per-``t`` residual is kept because it is what a debugging session wants when
    :func:`check_av_roll_fwd` returns ``False``; the boolean is defined in terms of it.
    """
    if t < entry_mth():
        return 0.0
    expected = (prem_to_av(t) + inv_income(t) - rider_charges(t) - wd_from_av(t)
                + av_depletion(t)
                - claims_from_av(t, "DEATH") - claims_from_av(t, "LAPSE")
                - claims_from_av(t, "MATURITY"))
    return av_change(t) - expected


def check_av_roll_fwd():
    """Check the account value roll-forward: ``True`` when it closes at every projected t.

    No argument and a bool, following ``savings.CashValue_SE`` and the rest of this
    library, so one test can call the same check across every model.  The signed residual
    for a single month is :func:`check_av_roll_fwd_resid`.

    The tolerance is absolute and loose enough for an account value of order $100,000
    accumulated over a century of months; it is not a modelling assumption.
    """
    res = []
    for t in range(entry_mth(), proj_len()):
        res.append(math.isclose(check_av_roll_fwd_resid(t), 0.0,      # noqa: F821
                                abs_tol=1e-6))
    return all(res)


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual for month t; the signed float.

    ``pols_if(t) - pols_if(t+1) = deaths + surrenders + horizon exits``.  Zero to floating
    point for every ``t``, including the last, ``t = proj_len() - 1``, where
    ``pols_if(proj_len())`` is zero and :func:`pols_maturity` carries the survivors out.
    """
    if t < entry_mth():
        return 0.0
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """Check the in-force roll-forward: ``True`` when it closes at every projected t.

    No argument and a bool, as for :func:`check_av_roll_fwd`; the signed residual for a
    single month is :func:`check_pols_roll_fwd_resid`.
    """
    res = []
    for t in range(entry_mth(), proj_len()):
        res.append(math.isclose(check_pols_roll_fwd_resid(t), 0.0,    # noqa: F821
                                abs_tol=1e-12))
    return all(res)


def result_cf():
    """Result table of cashflows, indexed by the **month** ``t`` from ``entry_mth()``.

    The frame runs ``t = entry_mth() … proj_len() - 1``, one row per projected month and
    **no issue-instant row**: the first row of a new-issue model point carries the premium
    and the acquisition expense as beginning-of-month flows alongside that month's own
    activity.  :func:`result_cf_annual` sums it into contract years.

    ``pols_if`` is the in-force count at the **start** of month ``t``, which is the weight
    every cash flow on the same row carries — dividing a row's cash flow by its
    per-contract amount returns this column exactly.  Every withdrawal and benefit driven
    by the contract falls in an anniversary month, so those columns are zero in eleven
    rows out of twelve; deaths, surrenders and maintenance expense fall in every row.

    ``withdrawals`` is the library-wide column for partial withdrawal payments and is the
    total; the three columns after it — ``wd_guar``, ``wd_excess`` and
    ``income_payments`` — partition that total into the notes' own ledger categories.
    **They are published alongside it, not instead of it, so summing every column of the
    frame double-counts the withdrawal.**  ``net_cf`` is income-positive, as everywhere
    in this library.
    """
    ts = list(range(entry_mth(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "wd_guar": [wd_guar(t) for t in ts],
            "wd_excess": [wd_excess(t) for t in ts],
            "income_payments": [income_payments(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "commissions": [commissions(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, indexed by the month t.

    ``pols_if`` opens the row and ``pols_if_aft_decr`` closes it, and the two decrement
    columns are the **monthly** rates actually applied; the annual rates they are converted
    from are :func:`mort_rate` and :func:`lapse_rate`, constant across each contract year.
    The closing column is the opening figure of the next row in every month but the last,
    where :func:`pols_maturity` takes the survivors out and the projection stops.  The
    identity ``check_pols_roll_fwd_resid`` asserts is therefore
    ``pols_if(t) - pols_if(t+1) = pols_death + pols_lapse + pols_maturity``.
    """
    ts = list(range(entry_mth(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, "AFT_DECR") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the per-contract account value and surrender trace, indexed by month.

    The first eight columns walk the worked example's account value rows, now month by
    month: ``fixed_interest_pp`` accrues in every row, ``index_credit_pp``,
    ``rider_charge_pp`` and ``wd_pp`` only in anniversary rows.  The rest are the surrender
    trace, available in **every month** rather than only at the anniversaries the notes
    tabulate — which is the reading a mid-year surrender needs.
    """
    ts = list(range(entry_mth(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_inv": [av_pp_at(t, "BEF_INV") for t in ts],
            "credit_rate": [credit_rate(t) for t in ts],
            "index_credit_pp": [index_credit_pp(t) for t in ts],
            "fixed_interest_pp": [fixed_interest_pp(t) for t in ts],
            "rider_charge_pp": [rider_charge_pp(t) for t in ts],
            "av_pp_bef_wd": [av_pp_at(t, "BEF_WD") for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "mgsv_pp": [mgsv_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "surr_clawback_pp": [surr_clawback_pp(t) for t in ts],
            "mva_pp": [mva_pp(t) for t in ts],
            "surr_benefit_pp": [surr_benefit_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_glwb():
    """Result table of the GLWB rider state per contract, indexed by the month t.

    The benefit base is **notional** — no cash value, not withdrawable, not payable as a
    lump sum [S1][S9] — so none of these columns is a cash flow.  They are the drivers of
    the rider charge, the lifetime withdrawal and, in the end, the post-depletion income.
    Every one of them is annual: the rider state is flat between anniversaries and steps at
    each one, so the rows of interest are the anniversary rows ``t = 12k + 11``.
    """
    ts = list(range(entry_mth(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "phase": [phase(t) for t in ts],
            "rollup_pp": [rollup_pp(t) for t in ts],
            "stack_pp": [stack_pp(t) for t in ts],
            "bb_pp_bef_step_up": [benefit_base_pp_at(t, "BEF_STEP_UP") for t in ts],
            "benefit_base_pp": [benefit_base_pp(t) for t in ts],
            "rollup_base_pp": [rollup_base_pp(t) for t in ts],
            "lw_pp": [lw_pp(t) for t in ts],
            "free_wd_allow": [free_wd_allow(t) for t in ts],
            "wd_guar_pp": [wd_guar_pp(t) for t in ts],
            "wd_excess_pp": [wd_excess_pp(t) for t in ts],
            "wd_unfunded_pp": [wd_unfunded_pp(t) for t in ts],
            "wd_reduction_rate": [wd_reduction_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into contract years, indexed by ``policy_year``.

    Every cash flow column is the total of its twelve months; ``pols_if`` is the count at
    the **start** of the contract year, ``pols_if(12 * duration)``, which is the number the
    annual-step model carried on the same row.

    Against the annual grid this agrees exactly on ``pols_if``, ``premiums``,
    ``commissions`` and ``premium_taxes``, the last three being the single premium and two
    rates on it.  It does **not** agree on the withdrawal columns, the claims or the
    expenses, and so not on ``net_cf``: a withdrawal taken at the anniversary is now
    weighted by the contracts that **reach** it rather than by those that entered the year,
    claims fall in the month of exit, and maintenance expense accrues monthly.  That gap is
    the point of the finer grid — see the Space docstring.
    """
    df = result_cf()
    years = pd.Index([duration(t) + 1 for t in df.index],            # noqa: F821
                     name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out



# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

maturity_age = 120

net_consideration_ratio = 0.875

floor_rate = 0.0

cap_rate_min = 0.0025

fixed_rate = 0.023

fixed_rate_min = 0.01

par_rate = 0.8

spread_rate = 0.02

trigger_rate = 0.045

index_cost_rate = 0.0

use_guaranteed_scale = False

rider_charge_rate = 0.0095

rider_charge_rate_max = 0.015

rider_charge_from_mgsv = False

growth_period_max = 20

step_up_mode = "annual"

rb_wd_convention = "pro_rata"

mva_collar_basis = "gross"

min_income_age = 50

free_wd_rate = 0.1

surr_charge_period = 10

mgsv_rate = 0.01

mgsv_annual_charge = 0.0

mgsv_stat_step = 0.0005

mgsv_stat_spread = 0.0125

mgsv_stat_cap = 0.03

mgsv_stat_floor = 0.0015

mgsv_stat_delta_max = 0.01

mgsv_stat_delta_gate = 0.0025

mort_ae_factor = 1.0

lapse_base_early = 0.02

lapse_base_mid = 0.03

lapse_base_late = 0.04

lapse_base_final = 0.05

lapse_base_ult = 0.06

shock_lapse_no_rider = 0.33

shock_lapse_rider_idle = 0.1

shock_lapse_rider_active = 0.05

lapse_money_slope = 0.6

lapse_money_floor = 0.2

lapse_rate_max = 0.35

rmd_age = 73

activation_age_low = 60

activation_rate_early = 0.05

activation_rate_rmd = 0.4

activation_rate_late = 0.15

comm_rate_acq = 0.0

expense_acq_rate = 0.06

expense_maint = 80.0

inflation_rate = 0.025

premium_tax_rate = 0.0

math = ("Module", "math")

pd = ("Module", "pandas")