# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Euro_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection[7].result_pb()          # the same cell on the low scenario

``t`` counts **policy months from the valuation date**, 0-based, so ``t = 0`` is the
first projected month whatever the model point's completed duration, and the frame is
``t = 0 … proj_len() - 1`` with ``proj_len() = 12 * proj_years = 480``. Month ``t`` runs
from time ``t / 12`` to time ``(t + 1) / 12``. `Versements` and `rachats partiels` fall
at the beginning of the month; the insurer's expense accrues through it; the
revalorisation and the `prélèvements sociaux` land at 31 December only; deaths and
`rachats totaux` act at the end of the month, deaths first.

Underneath that monthly grid the product carries an **annual layer**, and the two are
not the same clock. ``proj_year(t) = t // 12`` is the 0-based projection year, and
``is_anniv(t)`` — ``t % 12 == 11`` — is its 31 December, which on this model's
convention is also the policy anniversary. The attained age is
``age(t) = issue_age() + duration(t)`` with ``duration(t) = duration_init() + t // 12``
the completed policy years, and the contract's own 1-based policy year — which the lapse
table is indexed by — is ``policy_year(t) = duration(t) + 1``. For a cell issued at the
valuation date (``duration_init = 0``) that is the library's ``t // 12 + 1``. Nothing is
indexed by the policy year.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/assurance_vie_euro/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Euro_FR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Euro_FR_S.Data`, reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
fin_rate_file           data.fin_rate_table()           fin_rate_table.csv
======================  ==============================  ==========================

.. rubric:: Two clocks, and which cells carries which

A monthly grid is not a monthly product. The **crediting machinery** is a financial-year
statement — art. A132-11 and A132-12 build one `compte de participation aux résultats`
per financial year, art. A132-16 counts financial years, the `taux servi` is fixed by
the board for the closing year and credited at 31 December value date, and the levy is
withheld as that interest is inscribed — and none of it becomes monthly. What the finer
grid resolves is everything that is *not* contractually annual: the `versements libres
programmés` and `rachats partiels programmés` the contract bills monthly, the insurer's
expenses, and the decrements, which now fall in the month they happen.

So the argument of a cells says which clock it is on:

* cells that state a **financial-year account** take ``y``, the projection year —
  :func:`pm_avg_pp`, :func:`fee_pp`, :func:`expenses_pp`, the whole `compte de
  participation` block, :func:`ppb_pp` and its vintage ledger, :func:`ts_net`,
  :func:`int_credited_pp`, :func:`soc_levy_pp`, :func:`r_fin`, :func:`ref_rate`,
  :func:`prem_gross_pp`, :func:`prem_to_av_pp`, :func:`withdrawals_pp`,
  :func:`inflation_factor`;
* cells that state a **month** take ``t`` — the account and its ledgers, the in force,
  the claims, every ``result_cf()`` column, and the ``*_mth_pp`` instalments that carry
  a year's amount into its twelve months;
* the **decrement rates take ``t`` and return the year's annual rate**, which is the
  library-wide convention and is not the same thing as an annual statement.

The two-speed structure that follows is the library's convention, asserted by
``tests/test_model_conventions_fr.py``: :func:`mort_rate` and :func:`lapse_rate` are the
**annual** rates of the policy year containing month ``t`` — the vectors the technical
notes tabulate — and :func:`mort_rate_mth` and :func:`lapse_rate_mth` are the monthly
rates actually applied, ``1 - (1 - r)^(1/12)``, so that twelve of them compound back to
exactly the annual rate.

.. rubric:: Naming

Cells names follow lifelib's ``savings.CashValue_SE`` and ``basiclife.BasicTerm_S``
wherever those models have an analogue — ``av_pp_at(t, timing)`` for the within-month
account value, ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
annual rates and ``*_rate_mth`` for monthly ones, ``*_pp`` for per-policy amounts,
``*_mth_pp`` for the monthly instalment of a per-policy annual amount,
``claims(t, kind)`` with an uppercase ``kind`` string. The technical notes use compact
symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the cells argument)            Projection month, 0-based
y                          proj_year(t)                    Projection year, ``t // 12``
(none)                     duration_mth(t)                 Months elapsed at BOM, = t
(none)                     duration(t)                     Completed policy years
(none)                     is_anniv(t)                     31 December, ``t % 12 == 11``
(none)                     proj_len()                      Number of projected months
(the row)                  model_point()                   The selected model point
x                          issue_age()                     Age at `adhésion` (ALB)
x + d + y                  age(t)                          Attained age in month t
d                          duration_init()                 Completed years at valuation
d + y + 1                  policy_year(t)                  Contractual policy year, 1-based
AV(t)                      av_pp(t)                        `Épargne acquise`, start of t
(the steps)                av_pp_at(t, timing)             The balance inside month t
(fund level)               av_at(t, timing)                The same times pols_if(t)
P_g(y)                     prem_gross_pp(y)                `Versements` before charges
P(y)                       prem_to_av_pp(y)                `Versements` credited, year y
(instalment)               prem_to_av_mth_pp(t)            One twelfth of it, month t
W(y)                       withdrawals_pp(y)               `Rachats partiels`, year y
(instalment)               withdrawals_mth_pp(t)           One twelfth of it, month t
(the weights)              prem_wt_mth(k)                  Mid-month weight, sums to 0.5
B(y)                       pm_avg_pp(y)                    `Pro rata temporis` base
c, F(y)                    fee_rate(), fee_pp(y)           `Frais de gestion sur encours`
E(y)                       expenses_pp(y)                  Insurer expenses, year y
(instalment)               expenses_mth_pp(t)              One twelfth of it, month t
r(y)                       r_fin(y)                        Fund financial return
Phi(y)                     fin_acct_pp(y)                  `Compte financier` balance
T(y)                       tech_acct_pp(y)                 `Compte technique` balance
s(y)                       insurer_tech_share_pp(y)        Insurer's technical share
A(y)                       pb_acct_pp(y)                   `Compte de participation`
A+(y)                      pb_min_pp(y)                    Statutory minimum PB
s*                         ts_target()                     Target `taux servi`
(target amount)            pb_target_pp(y)                 What the target costs
Q(y)                       ppb_pp(y)                       PPB, start of year y
Q_v(y)                     ppb_vintage_pp(y, v)            The vintage ledger
(ledger total)             ppb_ledger_pp(y)                The ledger rebuilt
D(y)                       ppb_dotation_pp(y)              PPB dotation in year y
(discretionary)            ppb_discr_rel_pp(y)             Release the target wants
(the clock)                ppb_forced_pp(y)                Release the clock forces
R(y)                       ppb_release_pp(y)               max of the two
(FIFO draw)                ppb_vintage_release_pp(y, v)    Which vintage paid it
X(y)                       pb_credited_pp(y)               PB credited, gross of F(y)
(before the floor)         ts_raw(y)                       Rate that implies
g                          tmg_rate()                      `Taux minimum garanti`
(the floor's cost)         insurer_topup_pp(y)             What the TMG costs the insurer
sigma(y)                   ts_net(y)                       `Taux servi` credited
s^(y)                      ts_stat(y)                      Statutory floor rate
I(y)                       int_credited_pp(y)              Net revalorisation credited
(on the anniversary)       int_credited_mth_pp(t)          I(y) in month t, else nil
L(y)                       soc_levy_pp(y)                  `Prélèvements sociaux`
(on the anniversary)       soc_levy_mth_pp(t)              L(y) in month t, else nil
(cumulative)               soc_levy_cum_pp(t)              The levy ledger
(cumulative)               pb_cum_pp(t)                    The `effet cliquet` ledger
G(t)                       guar_floor_pp(t)                Contractual capital floor
q(y)                       mort_rate(t)                    Annual mortality rate
q_m(y)                     mort_rate_mth(t)                Monthly mortality rate
w(y)                       lapse_rate(t)                   Annual surrender rate
w_m(y)                     lapse_rate_mth(t)               Monthly surrender rate
(table)                    lapse_rate_base(t)              Base rate by policy year
(dynamic)                  lapse_dyn_add(t)                The `taux servi` gap term
l(t)                       pols_if(t)                      In force, start of month t
(none)                     pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
(none)                     pols_death(t), pols_lapse(t)    Decrements in month t
DB(t)                      db_pp(t)                        Death benefit per policy
CV(t)                      cv_pp(t)                        Surrender value per policy
(payout)                   claim_pp(t, kind)               Either of the two, by kind
(weighted)                 claims(t, kind)                 Benefit outgo
CF(t)                      liability_cf(t)                 The notes' outgo-positive flow
(none)                     net_cf(t)                       Its negative, income-positive
(none)                     result_cf_annual()              result_cf() summed into years
=========================  ==============================  ==========================

Six names needed care.

``pm_avg_pp`` is the notes' ``B(y)``, and it is not an average of anything the model
computes: it is the `pro rata temporis` base, the opening balance plus each month's
movement weighted by the fraction of the year still to run from the middle of that
month. On a level programmed schedule the twelve weights sum to exactly one half, so it
is the notes' ``AV + 0.5 P - 0.5 W`` to the last bit — **derived** on the monthly grid
rather than asserted. Calling it ``av_avg_pp`` would suggest it was read off
``av_pp_at``; it is a statement about *when* money moved, and the name says which
provision it stands in for.

``prem_wt_mth(k) = (11.5 - k) / 12`` is that weight. The mid-month convention is the
only one of the three candidates that reproduces the notes: beginning-of-month weights
``(12 - k)/12`` sum to 0.541667 and end-of-month ``(11 - k)/12`` to 0.458333, and either
would move the base by EUR 100 on the anchor cell's first year — small enough to look
like rounding and large enough to break the annual equivalence.

``ts_stat`` and ``ts_net`` are both rates **net of the management charge**, and that is
the single likeliest place to go wrong. ``pb_min_pp`` is gross of ``fee_pp`` because the
charge is a credit to the `compte technique`; the charge is subtracted **once**, on the
way from the PB amount to the rate the account actually grows by. Applying
``(1 + ts_net) (1 - fee_rate)`` afterwards would cost the policyholder 0.60% a year that
was already taken.

``ts_raw`` and ``insurer_topup_pp`` are the two halves of the notes'
``max(tmg_rate, ...)``. ``ts_raw`` is what the allocation alone produces; ``ts_net`` is
that floored at the TMG; and ``insurer_topup_pp`` is the difference in euros — what the
guarantee costs the insurer out of its own resources in a year the allocation cannot
fund it. It is nil on every model point shipped here, and see below for why no
positive-TMG cell is shipped.

``withdrawals`` is an **owner election, not a claim**. A `rachat partiel` is money the
policyholder asked for out of a balance the policyholder owns; a `rachat total` is the
same money, but it ends the contract and is a decrement, so it appears as
``claims_lapse``. Both leave the fund and both are in ``liability_cf``; keeping them
apart is what lets a reader see the difference between elective drawdown and exit.

``claims_lapse`` rather than ``claims_surr``: the column is named for the ``kind``
argument that produces it, and the decrement that produces it is the library's
``pols_lapse``.

.. rubric:: What a mid-year `dénouement` is paid

**A death or `rachat total` in a non-anniversary month is paid the `épargne acquise`
with no in-year revalorisation.** ``db_pp(t) = cv_pp(t) = av_pp(t + 1)`` is unchanged as
a formula — the claim is always struck on the balance closing the month of exit — but on
a monthly grid that balance carries the year's `taux servi` only in the anniversary
month. The other eleven months carry the contractual rule instead: the announced floor
rate `pro rata temporis`, which at ``tmg_rate() = 0``, the value every shipped model
point carries, is nil.

This is the one place the finer grid changes an answer rather than its resolution. An
annual step could only pay a March exit the following 31 December's balance, which is a
forward-looking payment at a date it is not yet due; it did so because the exit and the
crediting were the same instant, and the technical notes listed it as a pitfall, a
sensitivity and an out-of-scope item at once. The monthly grid removes the constraint,
so the model implements the contract. The documented alternative — the Afer reading, in
which the declared rate accrues `pro rata temporis` so that
``int_credited_mth_pp(t) = int_credited_pp(y) / 12`` in every month — is a variant named
in the notes, not the base; it preserves the anniversary equivalence just as exactly,
because the year's interest still sums to ``I(y)``, so only the sources decide between
them. At a **positive** TMG the in-year floor would be credited month by month and
squared up at 31 December against ``ts_net``; no such cells is shipped, because no
positive-TMG model point is (see below).

.. rubric:: What the monthly grid changes, and what it does not

Because the monthly decrement rates compound back to their annual values,
``[(1 - q_m)(1 - w_m)]^12 = (1 - q)(1 - w)``, the in force **at every anniversary** is
the annual-step recursion term for term — ``pols_if(12k)`` here is what an annual-step
model carried at its year ``k``. Because the twelve mid-month weighted
twelfths sum to exactly one half, the crediting base is the notes'
``AV + 0.5 P - 0.5 W``. And because the
`participation aux bénéfices` is a financial-year account that lands whole at 31
December, every quantity built on it — the `compte financier`, the `compte technique`,
the statutory minimum, the PPB and its vintages, the `taux servi`, the revalorisation,
the `prélèvements sociaux` and the closing `épargne acquise` — is the same number on the
two grids.

What the finer grid changes is the **cash flows**, and that is the point of it.
`Versements` and `rachats partiels` are collected in twelve instalments from a block
that decrements every month; expenses accrue on the in force of each month rather than
of the year's first day; claims fall at the end of the month of exit; and the year's
interest is weighted by the December in force rather than the January one. On the anchor
cell over forty years that is premiums -3.6%, withdrawals -4.0%, expenses -3.7%, death
claims -4.1%, surrender claims -0.5% and ``liability_cf`` -1.6% against the annual-step
model. :func:`result_cf_annual` sums the frame into projection years so the two can be
laid side by side.

.. rubric:: The crediting rule is an allocation with three levers

::

    fin_acct_pp(y)           = r_fin(y) (pm_avg_pp(y) + ppb_pp(y))
    tech_acct_pp(y)          = fee_pp(y) - expenses_pp(y)
    insurer_tech_share_pp(y) = max(0.10 max(tech_acct_pp(y), 0), 0.045 prem_gross_pp(y))
    pb_acct_pp(y)            = 0.85 fin_acct_pp(y) + tech_acct_pp(y)
                               - insurer_tech_share_pp(y)
    pb_min_pp(y)             = max(0, pb_acct_pp(y) - tmg_rate() pm_avg_pp(y))

Not one operator in this block is touched by the grid: it is a financial-year statement
indexed by ``y``, and it reproduces the annual-step model exactly.

Four points of substance, each of which is a listed pitfall.

**The 85% attaches to the financial account and the 90% to the technical account, not
the other way round.** "90% of the financial account and 85% of the technical result" is
the popular form and it is wrong.

**The insurer's technical share has two limbs and the 4.5%-of-premiums limb often
binds.** In the worked example's ``y = 5`` it is EUR 108.00 against EUR 28.43 for the
10% limb. Two model points identical but for their premium stream credit different rates,
and that is the article working as written: the premiums limb vanishes on a paid-up
contract and can exceed the whole technical result on a heavily premium-paying one.

**The PPB sits inside the financial base**, because art. A132-14 computes the financial
result on average technical provisions and the PPB is one of them. Omitting it
understates the distributable amount by ``0.85 r_fin ppb_pp`` — EUR 41.81 at
worked-example ``y = 5``. The mirror error is *accreting the vintages as well*, which
distributes the PPB's return twice: :func:`ppb_vintage_pp` changes only by releases.

**``ts_stat`` is net of the charge.** For the euro support the underwriting result is nil
— the death benefit is the account value — so ``tech_acct_pp`` is the loading result
alone.

Then the three levers::

    pb_target_pp(y)      = ts_target() pm_avg_pp(y) + fee_pp(y)
    ppb_dotation_pp(y)   = max(0, pb_min_pp(y) - pb_target_pp(y))
    ppb_discr_rel_pp(y)  = min(max(0, pb_target_pp(y) - pb_min_pp(y)), ppb_pp(y))
    ppb_forced_pp(y)     = sum of the vintages whose eight years are up
    ppb_release_pp(y)    = max(ppb_discr_rel_pp(y), ppb_forced_pp(y))
    pb_credited_pp(y)    = pb_min_pp(y) - ppb_dotation_pp(y) + ppb_release_pp(y)

The **statutory floor** is what the year's result alone obliges the insurer to credit.
The **PPB** moves the credited rate above or below it: a dotation parks this year's
excess, a release spends an earlier year's. The **TMG** is a hard floor under the result,
and because it guarantees technical interest *plus* PB together it is a floor on
``ts_net``, not a separate credit stacked on top. A dotation and a forced release can
coexist in one year — this year's excess goes in while an eight-year-old vintage comes
out — and both happen in the worked example's first three rows.

Note what a dotation year does: it credits **less** than ``ts_stat(y)``, and that is
legal, because the balance goes to the PPB and not to the insurer. The invariant is an
allocation identity, not a rate inequality, and :func:`check_pb_allocation` states it as
one.

.. rubric:: The PPB vintage ledger, and why it is a ledger

A dotation carried in financial year ``v`` must be applied to mathematical provisions or
paid to policyholders **within the eight financial years following**. The model
therefore carries :func:`ppb_vintage_pp`, a per-vintage balance released FIFO by
:func:`ppb_vintage_release_pp`, so that ``v + 8`` is a real deadline on a real balance.
A single-pot PPB with an average age satisfies the rule on average and breaches it on
every vintage; :func:`check_ppb_clock` asserts that nothing survives the year after its
deadline.

**The vintage clock is not made finer by the monthly grid**, and that is deliberate: art.
A132-16 counts *financial years*, so both the vintage index ``v`` and the balance's own
index ``y`` stay on the financial-year clock and the deadline stays a year deadline on a
year balance.

The opening balance is split into ``ppb_vintages_init`` equal vintages carried in years
``-1, -2, ... , -ppb_vintages_init``, so eight equal vintages fall due at ``y = 7, 6,
... , 0`` — a steady-state construction, and **[std]**, since no insurer publishes its
vintage profile. It matters: model point 6 carries the same EUR 4 000 in four vintages
instead of eight, and nothing is forced out until ``y = 4``.

The vintages do **not** accrete. The return on PPB assets enters the `compte financier`
through :func:`fin_acct_pp`, which is struck on ``pm_avg_pp + ppb_pp``; accreting the
vintages as well would distribute that return twice.

.. rubric:: The `effet cliquet` is not "the account never falls"

What is ratcheted is **credited PB**, not the balance. Under the `garantie nette` the
account falls by the management charge in a nil-PB year — the tables insurers publish
for exactly that case prove it — and the ratchet does not undo that.
:func:`check_cliquet` therefore asserts the ledger :func:`pb_cum_pp` is non-decreasing
and that ``int_credited_pp(y) >= 0`` and ``ts_net(y) >= tmg_rate()``, while
:func:`check_guar_floor` separately asserts the weaker contractual floor at **every
month**. The floor is compared to ``av_pp(t) + soc_levy_cum_pp(t)``, because the
published minimum surrender-value tables are stated **before** social and tax levies.

.. rubric:: Behaviour keys on the gap, not on the level

::

    lapse_dyn_add(t) = lapse_dyn_a max(0, ref_rate(y) - ts_net(y) - lapse_dyn_tol)
    lapse_rate(t)    = min(lapse_cap, lapse_rate_base(t) + lapse_dyn_add(t))
    lapse_rate_mth(t) = 1 - (1 - lapse_rate(t))^(1/12)

French surrender behaviour keys on the gap between the `taux servi` and the rate
available elsewhere, most visibly the Livret A. The gap is read **once a year**, at the
year the month falls in, so the annual rate is one rate for the whole policy year and
only :func:`lapse_rate_mth` varies within it. The term is **one-sided**: a `taux servi`
above the reference rate does not push surrenders below the base, because the base
already reflects needs-driven withdrawals. The sign of the relationship is observed — in
2025 the euro rate was 2.63% against a 2.20% Livret A average and euro supports turned to
a net inflow after five years of net outflow — but the **magnitude** has no public
calibration and ``lapse_dyn_a``, ``lapse_dyn_tol`` and ``lapse_cap`` are the most
consequential standardizations in the model. Because the credited rate and the surrender
rate move together, the model has a feedback loop the deterministic run only samples
once.

The table rate itself is keyed by :func:`policy_year`, the contract's own 1-based label,
so the duration-8 tax step is **twelve months wide**: on the anchor cell, five years in,
it covers ``t = 24 … 35``. Reading the table at ``t`` rather than at ``t // 12`` would
put the step in the third *month*, and that is the likeliest indexing error on this
grid.

.. rubric:: What is out of scope, and why

**No positive-TMG model point is shipped.** No contract in the source set publishes a
TMG — the two Suravenir notices state no guaranteed rate at all, BoursoVie names a TMG
without its value, MACSF names a board-set art. A132-3 rate without giving it, Afer names
a `Taux Plancher Garanti` without giving it — so the composite's TMG is 0.00% and every
model point carries it. The lever is implemented as the notes specify, and at
``tmg_rate() = 0`` the two things the notes call the TMG coincide: the art. A132-12
subtraction of "interest already credited to mathematical provisions", which belongs to a
`taux technique` fixed at subscription, and the floor on the year's total revalorisation,
which is what art. A132-3 actually guarantees. Above zero they are different quantities
and a model point would have to choose; the product specification is explicit that the
`taux technique` must not be substituted for the TMG, so no such cell is shipped and
``insurer_topup_pp`` is nil throughout.

Also out of scope, per the notes: the HCSF surrender-suspension power, which is precisely
what would change a mass-lapse answer, so a mass-lapse run here is a
**pre-management-action** result; the exceptional PPB `reprise` of art. A132-16-1, a
supervised recovery measure with no published trigger; `avances`, whose terms all three
insurers push into a separate document, so :func:`avance_on` validates rather than
guesses; `arbitrages` to and from the UC compartment, which is the sibling product; the
UC-holding bonus, since no contract publishes its grid; and sub-annual crediting
mechanics finer than the month, such as BoursoVie's daily compounding — an approximation
the monthly grid narrows rather than removes.

There is **no maturity decrement**: the euro support has no term, and the contract's
stated maturity, where one exists, is renewable annually without limit. The projection
simply stops at :func:`proj_len`, and the survivors there are paid nothing, because that
ending is a modelling truncation and not a contractual event.
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
    """The model point's policy identifier, for reporting."""
    return str(model_point()["policy_id"])


def sex():
    """The sex (M / F) of the model point; the mortality table is sex-distinct."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the age at `adhésion`, age last birthday **[std]**.

    No retrieved French document fixes an age basis, and it matters little here:
    mortality drives the *timing* of the `dénouement`, not the benefit amount, because
    the death benefit is the `épargne acquise` itself.
    """
    return int(model_point()["issue_age"])


def duration_init():
    """d: completed policy years at the valuation date; 0 on a new-business cell.

    The anchor cell is five years in, so the eighth policy anniversary - the tax
    threshold that drives the surrender step - falls inside the projection, in the twelve
    months ``t = 24 ... 35``.
    """
    return int(model_point()["duration_init"])


def pols_if_init():
    """l(0): policies represented by the model point; 1.0 on a single-policy cell.

    Model point 11 carries 250 instead, which is the only difference between it and the
    anchor cell: every per-policy amount is identical and every cash flow is 250 times
    as large.
    """
    return float(model_point()["pols_if_init"])


def av_pp_init():
    """AV(0): the `épargne acquise` per policy at the valuation date."""
    return float(model_point()["av_pp_init"])


def ppb_pp_init():
    """Q(0): the PPB attributed to the model point at the valuation date.

    4.0% of the account value on the anchor cell, the ACPR's end-2025 ratio for
    individual contracts.  The PPB is **collective** and is not attributed to individual
    contracts in law; attributing a per-policy share is the device that makes the
    eight-year clock visible at model-point level **[std]**.
    """
    return float(model_point()["ppb_pp_init"])


def ppb_vintages_init():
    """The number of equal open vintages the opening PPB is split across.

    Eight on the anchor cell - a steady-state construction, since a fund that has run the
    art. A132-16 clock for eight years carries roughly one eighth of its PPB in each open
    vintage - and four on model point 6, which is the same money in younger vintages and
    therefore no forced release before ``y = 4``.  **[std]**: no insurer publishes its own
    vintage profile, and this is the assumption that decides *when* the clock bites.
    """
    n = int(model_point()["ppb_vintages_init"])
    if n < 1:
        raise ValueError("ppb_vintages_init must be at least 1")
    return n


def prem_charge_rate():
    """The `frais sur versement` (entry charge) deducted from each `versement`.

    0.00% on the composite, which is what the bank-distributed and direct contracts
    charge; 0.50% on model point 9, the observed association-contract level.
    """
    return float(model_point()["prem_charge_rate"])


def wd_prog_pp():
    """The `rachat partiel programmé` elected per year, before it starts running.

    An **annual** election, billed in twelve monthly instalments: the product
    specification's minimum for a programmed partial surrender is EUR 150 a month, which
    every shipped model point clears.  :func:`withdrawals_pp` is what is actually paid in
    a year - nil before ``wd_start_year`` and capped at the balance it comes out of - and
    :func:`withdrawals_mth_pp` is the month's twelfth of it.
    """
    return float(model_point()["wd_pp"])


def wd_start_year():
    """The first **projection year** in which the programmed `rachat partiel` runs.

    A point on the annual layer's time axis, so it is 0-based like ``proj_year(t)``: 5 on
    the anchor cell means the sixth projected year, the months ``t = 60 ... 71``, and 98
    is the "never" sentinel a paid-up cell carries.  It is compared against
    ``proj_year(t)``, never against ``t``.
    """
    return int(model_point()["wd_start_year"])


def fee_rate():
    """c: the `frais de gestion sur encours`, per year of the euro-support balance.

    0.60% on the composite - a real contract rate in the middle of the observed 0.475% to
    0.80% band, and close to the ACPR's *actual* ratio of charges paid to average
    mathematical provisions, 0.63% for individual contracts in 2025.  The level is
    **[std]**; the charge itself and its 31 December pro rata temporis timing are
    sourced.
    """
    return float(model_point()["fee_rate"])


def tmg_rate():
    """g: the `taux minimum garanti`, a floor on the year's credited rate.

    0.00% on every model point shipped here.  **No public figure exists for the TMG of
    any contract in the source set**, and the nearest public anchor - the ACPR's average
    `taux technique` of 0.32% - is a different quantity, the maximum rate at which the
    insurer's commitments are discounted, and must not be substituted.  See the Space
    docstring for why no positive-TMG cell is shipped, and for what a positive TMG would
    have to do inside the year.
    """
    return float(model_point()["tmg_rate"])


def ts_target():
    """s*: the insurer's target `taux servi`, net of charges on the balance.

    2.30% on the composite: the **bottom of the band covering 50% of encours** in 2025
    (2.3% to 2.9%), which is where an unbonused contract sits when the market mean is
    2.63%.  A target, not an outcome - the model credits it only where the statutory
    floor and the PPB allow.  Model point 3 targets 2.90%, the top of that band, and
    drains its PPB in a handful of years trying to pay it.  **[std]**: no insurer's
    forward crediting policy is public.
    """
    return float(model_point()["ts_target"])


def soc_levy_rate():
    """The `prélèvements sociaux` rate, 17.2%, withheld as interest is credited."""
    return float(model_point()["soc_levy_rate"])


def guarantee_form():
    """``net`` or ``gross``: which capital guarantee the contract carries.

    ``net`` is the `garantie nette` - the floor is `versements` net of entry charges
    **less** the annual management charges - and is the modern design, the one whose
    arithmetic the published minimum surrender-value tables actually show.  ``gross``
    drops the charge term.  The retrieved documents split cleanly between the two, and
    both designs run inside one insurer and even inside one notice, so the model carries
    the choice on the model point rather than fixing it.
    """
    v = model_point()["guarantee_form"]
    if v not in ("net", "gross"):
        raise ValueError("invalid guarantee_form")
    return v


def avance_on():
    """Whether an `avance` (policy loan) is outstanding; always False here.

    Every retrieved notice pushes the `avance` terms - the rate, the ceiling, the
    duration - into a separate document that was not retrieved, so a model point electing
    one would have to invent them.  This validates rather than guessing.
    """
    v = int(model_point()["avance_on"])
    if v != 0:
        raise ValueError("avance terms are unpublished; no avance cell is supported")
    return False


def scenario_id():
    """The financial scenario the model point runs on: ``base``, ``low`` or ``high``."""
    v = str(model_point()["scenario_id"])
    if v not in tuple(data.fin_rate_table().index.levels[0]):        # noqa: F821
        raise ValueError("unknown scenario_id")
    return v


def proj_len():
    """The number of projected policy **months**: ``12 * proj_years`` = 480 **[std]**.

    The **count**, so the frame is ``t = 0 ... proj_len() - 1`` - lifelib's
    ``for t in range(proj_len())`` - and ``result_cf()`` has ``proj_len()`` rows.
    ``proj_years`` stays 40 and stays in **years**, because the horizon is an annual-layer
    fact: the euro support has no term, so it is a modelling choice rather than a contract
    fact, and ``fin_rate_table.csv`` carries exactly forty rows per scenario.  Forty years
    carries the anchor cell from attained age 60 to 99 and covers five full turns of the
    eight-year PPB clock.
    """
    return 12 * proj_years                                           # noqa: F821


def proj_year(t):
    """y: the 0-based projection year containing month t, ``t // 12``.

    The index of the model's **annual layer**.  The `compte de participation aux
    résultats`, the PPB and its vintage ledger, the declared `taux servi`, the
    revalorisation and the `prélèvements sociaux` are financial-year statements and are
    indexed by ``y``; everything that moves inside the year is indexed by the month ``t``.
    It is also the key of ``fin_rate_table.csv`` and the axis ``wd_start_year`` is stated
    on.
    """
    return t // 12


def duration_mth(t):
    """Months elapsed from the valuation date at the start of month t; equal to t.

    ``t`` is 0-based and counts from the valuation date, so the identity is trivial - the
    cells exists so the monthly models in this library share one vocabulary.  Policy time
    elapsed *before* the valuation date is carried in :func:`duration_init` and never in
    the index, which is why this is not ``12 * duration_init() + t``.
    """
    return t


def duration(t):
    """Completed policy years at the start of month t: ``duration_init + t // 12``.

    0-based, as ``duration`` is throughout lifelib.  It counts from the contract's
    inception rather than from the valuation date, because everything read off it - the
    attained age, the lapse table's eight-year tax threshold - is a fact about the
    contract and not about the frame.
    """
    return duration_init() + proj_year(t)


def is_anniv(t):
    """True in the **last month of a projection year**: ``t % 12 == 11``.

    The 31 December of year ``proj_year(t)``, which on this model's convention is also
    the policy anniversary.  It is where the whole year's revalorisation and
    `prélèvements sociaux` land, where the `frais de gestion` steps the `garantie nette`
    floor down, and where the art. A132-16 eight-year clock ticks.  The other eleven
    months of the year carry none of it.
    """
    return t % 12 == 11


def age(t):
    """The attained age in month t: ``issue_age() + duration(t)`` **[std]**.

    Age last birthday, stepping at the **policy anniversary** rather than on the
    insured's birthday, which is the library's convention.  It is constant across the
    twelve months of a policy year, so ``mort_rate`` reads one annual rate a year and
    ``mort_rate_mth`` spreads it.
    """
    return issue_age() + duration(t)


def policy_year(t):
    """The contract's 1-based policy year in month t: ``duration(t) + 1``.

    The **contractual label**, not the frame's index, and the library's 1-based
    ``policy_year`` rather than its 0-based ``duration``: during month ``t`` the contract
    is in its ``duration_init + t // 12 + 1``-th policy year, and that is equally the
    count of completed policy years at the 31 December that closes it.

    This is the index the lapse table is read by, and the reason is the tax threshold:
    the eight-year clock that switches on the reduced rate and the annual allowance runs
    from the contract's inception, not from the valuation date.  On the anchor cell, five
    completed years in, policy year 8 covers the twelve months ``t = 24 ... 35``.  It is
    derived from ``t`` and never indexed by.
    """
    return duration(t) + 1


def r_fin(y):
    """r(y): the fund's financial return rate in projection year y, from the scenario.

    A **scenario**, not a forecast.  The base path is anchored to the ACPR's observed
    `taux de rendement de l'actif` and to the reinvestment picture behind it: the 10-year
    OAT averaged 3.4% in 2025 while about 60% of fixed-coupon bonds maturing within four
    years still carried a coupon below 3%.  It dominates everything downstream - it sets
    the `compte financier`, hence the statutory floor, hence how fast the PPB drains.

    The scenario table is an **annual** path and stays one; the month reaches it through
    ``proj_year(t)``.
    """
    tbl = data.fin_rate_table().loc[scenario_id()]                   # noqa: F821
    return float(tbl.loc[min(y, int(tbl.index.max())), "r_fin"])


def ref_rate(y):
    """The market reference rate the dynamic surrender term keys off, in year y.

    2.20% throughout, the 2025 average Livret A rate.  It is carried in the scenario
    table rather than as a Reference because in a different financial scenario the rate
    available elsewhere is a different rate too.
    """
    tbl = data.fin_rate_table().loc[scenario_id()]                   # noqa: F821
    return float(tbl.loc[min(y, int(tbl.index.max())), "ref_rate"])


def prem_gross_pp(y):
    """P_g(y): the `versements libres programmés` received in year y, before charges.

    Level, and nil on a paid-up cell.  It stays an **annual** amount because it is the
    base of the **4.5%-of-premiums limb** of the insurer's technical share, which art.
    A132-11 states per financial year - so a paid-up contract and a premium-paying one
    credit different rates on identical funds.  :func:`prem_to_av_mth_pp` is what reaches
    the account in a month.
    """
    return float(model_point()["prem_gross_pp"])


def prem_to_av_pp(y):
    """P(y): the year's `versements` credited to the account, net of the entry charge."""
    return prem_gross_pp(y) * (1.0 - prem_charge_rate())


def prem_to_av_mth_pp(t):
    """The `versement` credited at the beginning of month t: ``P(y) / 12``.

    The contract bills `versements libres programmés` monthly - the product
    specification's minimum is EUR 50 a month - so the year's amount is collected in
    twelve equal instalments rather than as one lump.  This is one of the two places the
    finer grid changes a cash flow rather than its resolution: the second to twelfth
    instalments are paid by fewer policies than an annual grid charged the whole year's
    premium to.
    """
    return prem_to_av_pp(proj_year(t)) / 12.0


def withdrawals_pp(y):
    """W(y): the `rachat partiel` paid during year y, per policy.

    Nil before ``wd_start_year``, then the programmed annual amount.  Capped at the
    balance it comes out of - a physical constraint rather than a product rule, but an
    uncapped level election against a fund being run down eventually drives the account
    negative and every number downstream of it stays plausible enough to read past.  The
    cap is struck **once a year, on the year-open balance**, so that a within-year
    feedback from the balance into the crediting base is not introduced; it binds on no
    shipped model point.

    This is an **owner election, not a claim**.  The money leaves the fund and is in
    ``liability_cf``, but it comes out of a balance the policyholder owns and it does not
    end the contract; a `rachat total` does, and appears as ``claims_lapse``.
    """
    if y < wd_start_year():
        return 0.0
    return min(wd_prog_pp(), max(0.0, av_pp(12 * y) + prem_to_av_pp(y)))


def withdrawals_mth_pp(t):
    """The `rachat partiel` paid at the beginning of month t: ``W(y) / 12``.

    A `rachat partiel programmé` is billed monthly - the product specification's minimum
    is EUR 150 a month - so the year's election is paid in twelve equal instalments, from
    the block in force in each of those months.
    """
    return withdrawals_pp(proj_year(t)) / 12.0


def prem_wt_mth(k):
    """The crediting-base weight of a movement in month k of the year: ``(11.5 - k)/12``.

    The fraction of the financial year still to run from the **middle** of month ``k``,
    which is where a movement spread evenly through that month sits on average.  Each
    instalment is one twelfth of the year's amount, so the twelve weighted twelfths sum
    to exactly ``72/144 = 0.5`` of it - which is what turns the notes'
    ``B = AV + 0.5 P - 0.5 W`` from a **[std]** assertion into an arithmetic consequence
    of "spread evenly through the year".

    The two neighbouring conventions do not: beginning-of-month weights ``(12 - k)/12``
    give 0.541667 and end-of-month ``(11 - k)/12`` give 0.458333, either of which moves
    the anchor cell's first-year base by EUR 100 and its interest by EUR 2.79 - small
    enough to look like rounding and large enough to break the anniversary equivalence.
    """
    return (11.5 - k) / 12.0


def pm_avg_pp(y):
    """B(y): the crediting base of year y, `pro rata temporis` **[std]**.

    ``AV(12y)`` plus each of the year's twelve monthly movements weighted by
    :func:`prem_wt_mth`.  The PB is allocated "weighted by the time the sums were present
    on the fund during the year", so a payment made evenly through the year earns half a
    year's interest; crediting on the closing balance instead would give a full year's
    interest on a December payment.  The same base carries the management charge, which
    is what reproduces the published minimum surrender-value tables.

    On the level programmed schedules shipped here the twelve weighted twelfths collapse
    to the notes' ``AV + 0.5 P - 0.5 W`` exactly.  It can reach zero only if a withdrawal
    election has emptied the account, in which case every rate below is nil rather than
    undefined.
    """
    return av_pp(12 * y) + sum(
        prem_wt_mth(k) * (prem_to_av_mth_pp(12 * y + k)
                          - withdrawals_mth_pp(12 * y + k))
        for k in range(12))


def fee_pp(y):
    """F(y): the `frais de gestion sur encours` charged in year y, ``c B(y)``.

    Levied **whole at 31 December value date** on the average balance: the sourced "pro
    rata temporis" in that charge is about the *base*, which :func:`pm_avg_pp` already
    carries, not about the date.  It is never a cash flow - it is a credit to the `compte
    technique` - and it is **inside** :func:`ts_net`, not a further deduction from it.
    The one place it is visible monthly is :func:`guar_floor_pp`, where the `garantie
    nette` floor steps down once a year, on the anniversary.
    """
    return fee_rate() * pm_avg_pp(y)


def inflation_factor(y):
    """The expense inflation factor in projection year y: ``(1 + pi)^y`` **[std]**.

    Unity in the first projected year, ``y = 0``.  It steps **on the anniversary, not
    monthly**, which is the house rule in this library (``ADE_FR_S``, ``Obseques_FR_S``
    and ``Dep_FR_S`` all do the same) and which keeps the year's expense - and therefore
    the `compte technique` and the `taux servi` - identical to the annual-step model's.
    """
    return (1.0 + expense_inflation) ** y                            # noqa: F821


def expenses_pp(y):
    """E(y): the insurer's expenses in year y, per policy **[std]**.

    EUR 24 a policy a year inflating at 1.5%, plus 0.35% of the average balance.  Actual
    unit expenses are not public.  The proportional part is sized so that the loading
    margin leaves the statutory `compte technique` small relative to the `compte
    financier`, which is what the market outturn implies: a 0.63% average charge rate
    against a 2.8% asset return and a 2.63% credited rate leaves little technical margin
    once distribution costs on encours are paid.  The fixed/proportional split is a
    modelling choice, and it is why a small-balance model point credits materially less:
    the fixed part dominates its `compte technique`.

    This is the **year's** amount and the one the `compte technique` needs;
    :func:`expenses_mth_pp` is the month's twelfth of it, which is the reported cash flow.
    """
    return (expense_prop_rate * pm_avg_pp(y)                         # noqa: F821
            + expense_maint * inflation_factor(y))                   # noqa: F821


def expenses_mth_pp(t):
    """The insurer's expense incurred in month t, per policy: ``E(y) / 12``.

    One twelfth of the annual charge accrues each month, so a policy that runs a full
    year carries the same expense as it did on the annual grid - but it is now borne by
    the in force of **each month** rather than of the year's first day, which is what
    makes a decrementing block cost less.  The amount entering the `compte technique`
    stays the year's total, so the `taux servi` does not move.
    """
    return expenses_pp(proj_year(t)) / 12.0


def fin_acct_pp(y):
    """Phi(y): the `compte financier` balance, ``r(y) (B(y) + Q(y))``.

    **The PPB is inside the base.**  Art. A132-14 computes the financial result on
    average technical provisions and the PPB is one of them, so PPB assets earn inside
    this account.  Omitting it understates the distributable amount by
    ``0.85 r_fin ppb_pp``.  The mirror error is accreting the vintage balances as well,
    which would distribute the same return twice; :func:`ppb_vintage_pp` changes only by
    releases.
    """
    return r_fin(y) * (pm_avg_pp(y) + ppb_pp(y))


def tech_acct_pp(y):
    """T(y): the `compte technique` balance, ``F(y) - E(y)``.

    For the euro support the underwriting result is nil - the death benefit is the
    `épargne acquise` and nothing more - so this is the loading result alone.
    """
    return fee_pp(y) - expenses_pp(y)


def insurer_tech_share_pp(y):
    """s(y): the insurer's share of the technical account, art. A132-11.

    ``max(0.10 max(T(y), 0), 0.045 P_g(y))``: **the greater of** 10% of the credit
    balance and 4.5% of annual premiums.  The second limb is the one implementations
    drop, and with a small technical result and a live premium stream it takes the larger
    bite - EUR 108.00 against EUR 28.43 at the worked example's ``y = 5``.  It vanishes on
    a paid-up contract, leaving the insurer only 10% of the technical result, and it can
    exceed the whole technical result on a heavily premium-paying one, which is the
    article working as written.
    """
    return max(0.10 * max(tech_acct_pp(y), 0.0),
               0.045 * prem_gross_pp(y))


def pb_acct_pp(y):
    """A(y): the `compte de participation aux résultats`, art. A132-11.

    ``0.85 Phi(y) + T(y) - s(y)``.  **The 85% attaches to the financial account** and the
    90% - what is left after the 10% limb - to the technical account, not the other way
    round.  A contract with a contractual PB percentage, 90% at Suravenir Rendement or
    100% on Afer's `Fonds Garanti`, would replace the first term with that percentage of
    the ring-fenced fund's net financial profits; the composite keeps the insurer's
    discretion and floors it at the statutory minimum.
    """
    return (0.85 * fin_acct_pp(y) + tech_acct_pp(y)
            - insurer_tech_share_pp(y))


def pb_min_pp(y):
    """A+(y): the statutory minimum `participation aux bénéfices`, art. A132-12.

    The credit balance of the participation account, less interest already credited to
    mathematical provisions, floored at zero.  With ``tmg_rate() = 0`` on every model
    point shipped here the subtraction is nil and this is ``max(0, pb_acct_pp(y))``.
    """
    return max(0.0, pb_acct_pp(y) - tmg_rate() * pm_avg_pp(y))


def ts_stat(y):
    """s^(y): the statutory floor rate, ``(A+(y) - F(y)) / B(y)``.

    What the year's result alone obliges the insurer to credit, expressed as a rate the
    account grows by - so **net of the management charge**, which is subtracted once here
    because ``pb_min_pp`` is gross of it.

    Note that ``ts_net(y) >= ts_stat(y)`` is **not** an invariant.  A dotation year
    credits less than this and that is legal: the balance goes to the PPB, not to the
    insurer.  It happens to hold on every row of the worked example only because the
    forced release always exceeds the dotation there.
    """
    if pm_avg_pp(y) <= 0.0:
        return 0.0
    return (pb_min_pp(y) - fee_pp(y)) / pm_avg_pp(y)


def pb_target_pp(y):
    """What crediting the target `taux servi` would cost, ``s* B(y) + F(y)``.

    Gross of the management charge, because ``pb_min_pp`` is, so that the two are
    comparable and the dotation and discretionary release fall out of their difference.
    """
    return ts_target() * pm_avg_pp(y) + fee_pp(y)


def ppb_pp(y):
    """Q(y): the PPB attributed to the model point at the start of year y.

    ``Q(y+1) = Q(y) + D(y) - R(y)``.  Bounded below by zero, and it never has to be
    floored: both candidate releases are bounded by the balance, so the recursion cannot
    take it negative.  A negative PPB is not a permitted state, and the exceptional
    `reprise` of art. A132-16-1 - available only on a negative technical account **and**
    an uncovered SCR, under an ACPR-approved recovery plan - is a supervised recovery
    measure, not a projection lever.

    This is the aggregate balance, and it is a **financial-year** balance: art. A132-16
    counts financial years, so the monthly grid leaves it alone.  :func:`ppb_ledger_pp`
    rebuilds the same number from the vintage ledger, and :func:`check_ppb_roll_fwd`
    asserts the two agree - which is the point of keeping them separate.
    """
    if y == 0:
        return ppb_pp_init()
    return ppb_pp(y - 1) + ppb_dotation_pp(y - 1) - ppb_release_pp(y - 1)


def ppb_vintage_first():
    """The oldest vintage index the ledger carries: ``-ppb_vintages_init()``.

    The vintage index runs on the same 0-based **projection-year** clock as ``y``: a
    dotation in year ``v`` opens vintage ``v``, and the opening balance's vintages sit in
    the years before the frame.  Eight equal opening vintages are carried in years -1, -2,
    ... , -8 and fall due at ``y = 7, 6, ... , 0``.
    """
    return -ppb_vintages_init()


def ppb_vintage_pp(y, v):
    """Q_v(y): the remaining balance of the vintage carried in year v, at the start of y.

    Both indices are **financial years**, which is what art. A132-16 counts: the monthly
    grid does not reach into this ledger.  The opening vintages are seeded equal.  A
    vintage opened by a dotation in year ``v`` carries ``D(v)`` at the start of year
    ``v + 1`` and is drawn down by :func:`ppb_vintage_release_pp` thereafter.

    It **changes only by releases**.  The return on PPB assets is earned inside the
    `compte financier`, which is struck on ``pm_avg_pp + ppb_pp``; accreting the vintages
    as well would distribute that return twice.
    """
    if v < ppb_vintage_first() or v >= y:
        return 0.0
    if y == 0:
        return ppb_pp_init() / ppb_vintages_init()
    if v == y - 1:
        return ppb_dotation_pp(y - 1)
    return ppb_vintage_pp(y - 1, v) - ppb_vintage_release_pp(y - 1, v)


def ppb_vintage_release_pp(y, v):
    """How much of year y's release is drawn from the vintage carried in year v.

    **FIFO, oldest vintage first.**  The statute prescribes no release order, but FIFO is
    the only order that satisfies the eight-year constraint without slack, and it is what
    makes the ledger testable: releasing LIFO would let an old vintage age past its
    deadline behind a young one that keeps being spent.
    """
    if v < ppb_vintage_first() or v >= y:
        return 0.0
    drawn = sum(ppb_vintage_release_pp(y, u)
                for u in range(ppb_vintage_first(), v))
    return min(max(0.0, ppb_release_pp(y) - drawn), ppb_vintage_pp(y, v))


def ppb_ledger_pp(y):
    """The PPB rebuilt from the vintage ledger: the sum of the open vintages.

    Computed independently of :func:`ppb_pp`, which runs its own aggregate recursion, so
    that :func:`check_ppb_roll_fwd` compares two things rather than restating one.
    """
    return sum(ppb_vintage_pp(y, v)
               for v in range(ppb_vintage_first(), max(y, 0)))


def ppb_dotation_pp(y):
    """D(y): the dotation carried to the PPB in year y, ``max(0, A+(y) - target)``.

    The excess of the year's statutory minimum over what the target `taux servi` costs.
    It opens vintage ``y``, whose eight-year clock starts running now.  No insurer
    publishes its dotation policy; only the outer bounds are public **[std]**.
    """
    return max(0.0, pb_min_pp(y) - pb_target_pp(y))


def ppb_discr_rel_pp(y):
    """The release the target `taux servi` wants, capped at the PPB balance.

    ``min(max(0, target - A+(y)), Q(y))``: what the insurer would choose to spend to
    reach its target.  When the PPB is exhausted this is nil and the model credits
    ``ts_stat(y)`` - which is exactly what happens from ``y = 8`` of the worked example,
    and the step down is a model result, not a market forecast.
    """
    return min(max(0.0, pb_target_pp(y) - pb_min_pp(y)), ppb_pp(y))


def ppb_forced_pp(y):
    """The release the eight-year clock forces in year y.

    The sum of every vintage carried in a year ``v`` with ``v + 8 <= y``: sums carried to
    the PPB must be applied to mathematical provisions or paid to policyholders within
    the eight financial **years** following the one they were carried in.  This is a
    **deadline**, and it can exceed what the insurer would have chosen to release - which
    is the whole reason the ledger is per vintage.
    """
    return sum(ppb_vintage_pp(y, v)
               for v in range(ppb_vintage_first(), y - 7))


def ppb_release_pp(y):
    """R(y): the PPB released in year y, ``max(discretionary, forced)``.

    A dotation and a forced release can coexist in one year - this year's excess goes in
    while an eight-year-old vintage comes out - and both happen in the worked example's
    first three rows.  Where the forced release wins, the credited rate goes **above** the
    target: ``y = 5`` of the worked example wants EUR 426.99 and must release EUR 500.00.
    """
    return max(ppb_discr_rel_pp(y), ppb_forced_pp(y))


def pb_credited_pp(y):
    """X(y): the `participation aux bénéfices` credited in year y, gross of F(y).

    ``A+(y) - D(y) + R(y)``.  The whole of the year's statutory minimum is allocated -
    credited, or carried to the PPB - and nothing of it is lost: that identity, not a
    rate inequality, is what :func:`check_pb_allocation` asserts.
    """
    return pb_min_pp(y) - ppb_dotation_pp(y) + ppb_release_pp(y)


def ts_raw(y):
    """The credited rate the allocation alone produces, before the TMG floor.

    ``(X(y) - F(y)) / B(y)``.  The management charge is subtracted **once**, here, on the
    way from a PB amount to the rate the account actually grows by; the charge is a credit
    to the `compte technique` and is already inside ``X(y)``.
    """
    if pm_avg_pp(y) <= 0.0:
        return 0.0
    return (pb_credited_pp(y) - fee_pp(y)) / pm_avg_pp(y)


def ts_net(y):
    """sigma(y): the `taux servi` credited for year y, ``max(g, ts_raw(y))``.

    A **net** rate in the ACPR's sense - net of charges on the balance and before social
    levies - and the `frais de gestion sur encours` is *inside* it.  Applying
    ``(1 + ts_net) (1 - fee_rate)`` afterwards would cost the policyholder 0.60% a year
    that was already taken, which is the likeliest implementation error on this product.

    It is a **rate for the financial year**, fixed by the board for the closing year and
    credited at 31 December value date, so it takes the year index and not the month's.
    The TMG enters as a floor rather than as a separate credit, because it guarantees
    technical interest *plus* PB together.
    """
    return max(tmg_rate(), ts_raw(y))


def insurer_topup_pp(y):
    """What the TMG floor costs the insurer out of its own resources in year y.

    ``(sigma(y) - ts_raw(y)) B(y)``: the amount the allocation could not fund and the
    guarantee obliges the insurer to add.  Nil on every model point shipped here, because
    every one carries ``tmg_rate() = 0``; it is published so that the floor's cost is a
    number rather than an invisible adjustment, and so that
    :func:`check_pb_allocation` can close exactly when it is not nil.
    """
    return (ts_net(y) - ts_raw(y)) * pm_avg_pp(y)


def int_credited_pp(y):
    """I(y): the net revalorisation credited at 31 December, ``sigma(y) B(y)``.

    The amount the contract's value actually rises by in the financial year, and the base
    of the `prélèvements sociaux`.  :func:`int_credited_mth_pp` is where it lands.
    """
    return ts_net(y) * pm_avg_pp(y)


def int_credited_mth_pp(t):
    """The revalorisation credited in month t: ``I(y)`` at 31 December, nil otherwise.

    The `participation aux bénéfices` is fixed for the **closing financial year** and
    credited at 31 December value date, so the whole of the year's interest arrives in
    one month and eleven months of twelve carry none of it.  That is what an annual
    contractual event looks like on a finer grid, and it is why a mid-year exit is paid
    the account value without the year's `taux servi` - see the Space docstring.
    """
    return int_credited_pp(proj_year(t)) if is_anniv(t) else 0.0


def soc_levy_pp(y):
    """L(y): the `prélèvements sociaux` withheld in year y, ``0.172 max(I(y), 0)``.

    Taken **as the interest is credited**, every year, whether or not anything is
    withdrawn, because the rights are expressed in euros; only the UC part is deferred to
    `dénouement`.  Levying it only at surrender is the commonest foreign-model error on
    this product, and levying it on the *account* rather than on the year's interest is
    the next one: 17.2% of EUR 100 000 is EUR 17 200, while 17.2% of the worked example's
    first year's interest - ``y = 0``, EUR 2 827.60 - is EUR 486.35.

    The base is the interest actually inscribed on the contract, i.e. **net** of the
    management charge, which is **[std]**: art. L136-7 fixes the timing but not the base,
    and no retrieved product document says which it is.
    """
    return soc_levy_rate() * max(int_credited_pp(y), 0.0)


def soc_levy_mth_pp(t):
    """The `prélèvements sociaux` withheld in month t: ``L(y)`` at 31 December, else nil.

    Art. L136-7 II charges the products "lors de leur inscription au bon ou contrat", and
    the inscription is the 31 December crediting, so the levy lands in the same month as
    the interest it is struck on and never before it.  Spreading the levy without
    spreading the interest would tax interest not yet credited.
    """
    return soc_levy_pp(proj_year(t)) if is_anniv(t) else 0.0


def soc_levy_cum_pp(t):
    """Cumulative `prélèvements sociaux` deducted before the start of month t.

    Non-decreasing, and it moves only in the month after an anniversary.  It is added
    back to the account in :func:`check_guar_floor`, because the published minimum
    surrender-value tables are stated **before** social and tax levies.
    """
    if t == 0:
        return 0.0
    return soc_levy_cum_pp(t - 1) + soc_levy_mth_pp(t - 1)


def pb_cum_pp(t):
    """The `effet cliquet` ledger: PB credited since the valuation date, before month t.

    Non-decreasing by construction, since credited PB is definitively acquired and cannot
    be called back.  It steps once a year, in the month after the 31 December that
    credited the PB.  What is ratcheted is **this**, not the account balance - see
    :func:`check_cliquet`.
    """
    if t == 0:
        return 0.0
    prev_y = proj_year(t - 1)
    step = max(pb_credited_pp(prev_y), 0.0) if is_anniv(t - 1) else 0.0
    return pb_cum_pp(t - 1) + step


def av_pp_at(t, timing):
    """The `épargne acquise` per policy at a point inside month t.

    ``"BEF_PREM"``
        the opening balance, ``AV(t)``; the same number as :func:`av_pp`.

    ``"AFT_PREM"``
        after the month's `versement`, credited net of the entry charge.

    ``"AFT_WD"``
        after the month's `rachat partiel`.

    ``"AFT_INT"``
        after the 31 December revalorisation - which is nil in eleven months of twelve,
        so in those months this equals ``"AFT_WD"``.  **The `frais de gestion`
        is inside** ``I(y)``, not a further deduction from this balance.

    The `prélèvements sociaux` are withheld after this last point, and
    ``av_pp(t + 1) = av_pp_at(t, "AFT_INT") - soc_levy_mth_pp(t)``.  The levy is not given
    a timing string of its own because it is not a movement on the contract in the same
    sense: it is a tax the insurer withholds and remits, and keeping it out of the timing
    ladder is what keeps it out of ``net_cf``.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_mth_pp(t)
    if timing == "AFT_WD":
        return av_pp_at(t, "AFT_PREM") - withdrawals_mth_pp(t)
    if timing == "AFT_INT":
        return av_pp_at(t, "AFT_WD") + int_credited_mth_pp(t)
    raise ValueError("invalid timing")


def av_pp(t):
    """AV(t): the `épargne acquise` per policy at the start of month t.

    ``AV(t+1) = AV(t) + P_m(t) - W_m(t) + I_m(t) - L_m(t)``, where the last two terms are
    nil except in the anniversary month.  The social levy is **inside** this recursion,
    because it is money that genuinely leaves the contract; a model that defers it to
    surrender overstates the account and every benefit measured on it.
    """
    if t == 0:
        return av_pp_init()
    return av_pp_at(t - 1, "AFT_INT") - soc_levy_mth_pp(t - 1)


def av_at(t, timing):
    """The fund-level `épargne acquise` at a point inside month t: per policy times l(t).

    Every aggregate in this model is the per-policy amount times the start-of-month in
    force, which is what makes :func:`check_av_roll_fwd` an exact identity: claims are
    struck on ``av_pp(t + 1)``, the same balance the survivors carry forward.
    """
    return av_pp_at(t, timing) * pols_if(t)


def av(t):
    """The fund-level `épargne acquise` at the start of month t."""
    return av_pp(t) * pols_if(t)


def guar_floor_pp(t):
    """G(t): the contractual capital guarantee floor at the start of month t.

    ``G(t+1) = G(t) + P_m(t) - W_m(t) - F(y) 1{31 December}`` on the `garantie nette`,
    which is the composite's form: `versements` net of entry charges, **less** the
    **annual** management charges - so the charge term steps once a year, on the
    anniversary, which is what "less the annual management charges" says.  The ``gross``
    variant drops the charge term.

    For an in-force cell the premium history before the valuation date is not carried on
    the model point, so the floor is seeded at ``av_pp_init()`` **[std]** - deliberately
    conservative, since the true floor on a five-year-old contract sits below its account
    value by the interest already credited.
    """
    if t == 0:
        return av_pp_init()
    prev = (guar_floor_pp(t - 1) + prem_to_av_mth_pp(t - 1)
            - withdrawals_mth_pp(t - 1))
    if guarantee_form() == "net" and is_anniv(t - 1):
        prev = prev - fee_pp(proj_year(t - 1))
    return prev


def mort_rate(t):
    """q(y): the **annual** best-estimate mortality rate of the policy year of month t.

    The shipped table rate at ``age(t)`` times ``mort_be_factor``, and it is the rate the
    technical notes tabulate - one rate for the twelve months of a policy year.
    :func:`mort_rate_mth` is the rate actually applied in the month.  Both are
    placeholders: the statutory tables annexed to the arrêté du 1er août 2006 are cited in
    the documents but not redistributed here, so the table is an INSEE-shaped population
    proxy and the factor a crude allowance for population mortality being heavier than
    insured experience.  The two together give the notes' placeholder ``q = 0.0060`` at
    male age 60 exactly **[std]**.

    Mortality here is a **timing** assumption, not an amount assumption: the death
    benefit is the `épargne acquise`, so the basis affects only *when* the account is
    released - far less than in any protection product.
    """
    x = min(age(t), omega_age)                                       # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def mort_rate_mth(t):
    """q_m = 1 - (1 - q)^(1/12): the monthly mortality rate applied in month t **[std]**.

    Derived **geometrically** from the policy year's annual rate and not by dividing by
    twelve, which is what makes twelve months compound back to exactly that rate.  No
    retrieved French source states a conversion convention for any decrement, so the
    constant-force conversion is a standardization - and it is the one that makes the
    monthly grid reproduce the annual-step model at every anniversary.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The table **annual** surrender rate at the contractual policy year **[std]**.

    4% at durations 1-7, **8% at duration 8**, 5% at durations 9 and beyond; durations
    past the table take its last row.  The duration-8 step is the tax threshold, not a
    behavioural guess.  The key is :func:`policy_year`, the 1-based contractual label,
    which is what ``lapse_table.csv``'s ``policy_duration`` column is stated on - so the
    step is **twelve months wide**, ``t = 24 ... 35`` on the anchor cell.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())),
                         "lapse_rate_base"])


def lapse_dyn_add(t):
    """The dynamic surrender addition for the policy year of month t **[std]**.

    ``a max(0, ref_rate(y) - ts_net(y) - tol)``: additive in the gap between the market
    reference rate and the `taux servi`, both of which are **annual** quantities read at
    ``proj_year(t)``, so the addition is one number for the whole policy year rather than
    drifting month by month.  **One-sided** - a `taux servi` above the reference rate does
    not push surrenders below the base, because the base already reflects needs-driven
    withdrawals.  A two-sided variant is a scenario switch, not the base.

    ``a`` and ``tol`` have no public calibration and are the largest unanchored numbers
    in this model.
    """
    y = proj_year(t)
    return lapse_dyn_a * max(0.0, ref_rate(y) - ts_net(y)            # noqa: F821
                             - lapse_dyn_tol)                        # noqa: F821


def lapse_rate(t):
    """w(y): the **annual** `rachat total` rate of the policy year containing month t.

    The base rate plus the dynamic addition, capped - the rate the technical notes
    tabulate, and the one :func:`lapse_rate_mth` converts for the month.  The cap is what
    stops a wide `taux servi` gap producing a surrender rate no fund could meet in an
    orderly way - and a mass-lapse run here is a **pre-management-action** number, because
    the HCSF's power to freeze surrenders for up to six consecutive months is precisely
    what would change the answer and is not modelled.
    """
    return min(lapse_cap, lapse_rate_base(t) + lapse_dyn_add(t))     # noqa: F821


def lapse_rate_mth(t):
    """w_m = 1 - (1 - w)^(1/12): the monthly `rachat total` rate in month t **[std]**.

    The same constant-force conversion :func:`mort_rate_mth` takes, on the policy year's
    annual rate, so twelve months of it compound back to exactly that rate.  There is no
    shock or contractual surrender date inside a policy year on this product - the
    duration-8 tax threshold is itself a policy-year boundary - so nothing about the
    surrender decrement clusters on a month, and the whole of the year's rate is spread.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """l(t): the number of policies in force at the **start** of month t."""
    if t == 0:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement; :func:`pols_if`.

    ``"BEF_LAPSE"``
        after deaths, before `rachats totaux` - the processing order is
        death before surrender **[std]**.

    ``"AFT_DECR"``
        the end-of-month count.

    Both decrements act at the **end of every month**, on the monthly rates, and after
    whatever crediting that month carried - which is the year's revalorisation in the
    anniversary month and nothing in the other eleven.  So an exit takes the balance its
    month actually closes on: see the Space docstring on what a mid-year `dénouement` is
    paid.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths at the end of month t, against the start-of-month in force."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """`Rachats totaux` at the end of month t, from the survivors of mortality."""
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def db_pp(t):
    """DB(t): the death benefit per policy, the `épargne acquise` and nothing more.

    ``av_pp(t + 1)``: the balance closing the month of death, because the decrement acts
    at the end of the month after whatever that month credited.  In the anniversary month
    that is the whole year's `taux servi`; in the other eleven it is no in-year interest
    at all, which is the contractual floor rate `pro rata temporis` at a nil TMG.  There
    is **no additional death guarantee** on the euro support - the optional riders price
    the *UC* capital at risk - and adding an uplift here is a listed pitfall.
    """
    return av_pp(t + 1)


def cv_pp(t):
    """CV(t): the surrender value per policy, with **no penalty**.

    The same balance as the death benefit, closing the month of exit.  The `frais de
    rachat` is 0.00% on every retrieved contract, and settlement is two months by statute
    and thirty days by contract.
    """
    return av_pp(t + 1)


def claim_pp(t, kind):
    """The payout per claim in month t, by kind.

    ``"DEATH"``
        :func:`db_pp` - the `épargne acquise`, no uplift.

    ``"LAPSE"``
        :func:`cv_pp` - the same amount, no penalty.

    They are equal, and that equality is the product statement: on the euro support the
    death benefit *is* the surrender value.  Both are computed so that an implementation
    which quietly added a death uplift or a surrender charge would show up as a
    difference rather than disappear into a shared cells.

    There is no ``"MATURITY"``: the euro support has no term.
    """
    if kind == "DEATH":
        return db_pp(t)
    if kind == "LAPSE":
        return cv_pp(t)
    raise ValueError("invalid kind")


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"DEATH"`` and ``"LAPSE"`` weight :func:`claim_pp` by the corresponding decrement.
    `Rachats partiels` are **not** here: they are an owner election and live in
    :func:`withdrawals`.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE"))
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    if kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    raise ValueError("invalid kind")


def premiums(t):
    """`Versements` credited to the fund in month t, an inflow.

    The month's instalment weighted by the in force **of that month**, which is why a
    decrementing block pays less over a year than an annual grid charged it.
    """
    return prem_to_av_mth_pp(t) * pols_if(t)


def withdrawals(t):
    """`Rachats partiels` paid in month t - an owner election, not a claim."""
    return withdrawals_mth_pp(t) * pols_if(t)


def expenses(t):
    """The insurer's expenses in month t, weighted by the in force of that month."""
    return expenses_mth_pp(t) * pols_if(t)


def int_credited(t):
    """The revalorisation credited to the fund in month t; nil but at 31 December.

    A **state movement**, reported beside the flows and not summed into
    :func:`liability_cf`: it moves the liability, it does not settle it.  At fund level it
    is weighted by the in force of the **anniversary** month, the policies that actually
    reach the crediting date.
    """
    return int_credited_mth_pp(t) * pols_if(t)


def soc_levy(t):
    """The `prélèvements sociaux` withheld in month t; nil but at 31 December.

    Reported in its own column and **excluded from** :func:`net_cf`, because it is a
    policyholder tax the insurer withholds and remits to the State - neither a benefit nor
    an insurer expense.  A fund-level asset projection adds it back as an outflow in one
    step.
    """
    return soc_levy_mth_pp(t) * pols_if(t)


def liability_cf(t):
    """CF(t): the notes' **outgo-positive** liability cash flow in month t.

    ``claims_death + claims_lapse + withdrawals + expenses - premiums``.  The
    revalorisation and the social levy are not in it: the first is a state movement and
    the second is a tax.
    """
    return (claims(t, "DEATH") + claims(t, "LAPSE") + withdrawals(t)
            + expenses(t) - premiums(t))


def net_cf(t):
    """The net cash flow of month t, **income positive**: ``-liability_cf(t)``.

    The library's sign convention.  Both orientations are published so that neither the
    notes' reader nor the library's has to negate anything in their head.
    """
    return -liability_cf(t)


def check_av_roll_fwd_resid(t):
    """The fund-level `épargne acquise` roll-forward residual in month t; zero everywhere.

    ``av(t) + premiums - withdrawals + int_credited - soc_levy - claims_death
    - claims_lapse - av(t+1)``, rebuilt from the reported cash flows rather than from the
    per-policy recursion.
    """
    return (av(t) + premiums(t) - withdrawals(t) + int_credited(t)
            - soc_levy(t) - claims(t, "DEATH") - claims(t, "LAPSE")
            - av(t + 1))


def check_av_roll_fwd():
    """True when the fund-level account roll-forward closes in every projected **month**.

    This is the check that catches a **misindexed recursion**.  The identity is exact only
    because claims are struck on ``av_pp(t + 1)`` - the same balance the survivors carry
    forward - and only because both decrements act after whatever the month credited.
    Strike the claims on ``av_pp(t)`` instead, or apply a decrement before the
    anniversary month's revalorisation, and the residual is that month's interest on the
    exiting policies: a number small enough to look like rounding and large enough to be
    wrong.
    """
    scale = max(av_pp_init() * pols_if_init(), 1.0)
    return all(abs(check_av_roll_fwd_resid(t)) <= 1e-9 * scale
               for t in range(proj_len()))


def check_ppb_roll_fwd_resid(y):
    """The PPB residual in projection year y: the ledger tie plus the roll-forward.

    Both terms are zero when the model is right.  They are reported as one signed number
    and asserted separately in :func:`check_ppb_roll_fwd`, so that a cancellation between
    them cannot pass.
    """
    roll = (ppb_pp(y + 1) - ppb_pp(y) - ppb_dotation_pp(y)
            + ppb_release_pp(y))
    tie = ppb_ledger_pp(y) - ppb_pp(y)
    return roll + tie


def check_ppb_roll_fwd():
    """True when the PPB balance and its vintage ledger agree, every **financial year**.

    Two independent statements, asserted separately.  The **balance** runs its own
    recursion ``Q(y+1) = Q(y) + D(y) - R(y)``; the **ledger** is the sum of the per-vintage
    balances, each rolled forward by its own FIFO draw.  Nothing forces them to agree, and
    a release that drew more or less than the aggregate said - the ordinary consequence of
    an off-by-one in the FIFO loop - breaks the tie while leaving both numbers plausible.
    The PPB is also asserted non-negative here.

    The range is ``proj_years``, not ``proj_len()``: this is a financial-year statement
    and restating it at 480 months would cost twelve times as much for the same answer.
    """
    for y in range(proj_years):                                      # noqa: F821
        if ppb_pp(y) < -1e-9:
            return False
        if abs(ppb_ledger_pp(y) - ppb_pp(y)) > 1e-8:
            return False
        if abs(ppb_pp(y + 1) - ppb_pp(y) - ppb_dotation_pp(y)
               + ppb_release_pp(y)) > 1e-8:
            return False
    return True


def check_ppb_clock_resid(y):
    """What is left at the start of year y in vintages whose eight years are up; zero.

    A vintage carried in year ``v`` must be exhausted by the end of year ``v + 8``, so at
    the start of year ``y`` nothing may survive in any vintage with ``v <= y - 9``.  Note
    the index: a vintage with ``v = y - 8`` is due *during* year y and is still standing at
    its start - that is what :func:`ppb_forced_pp` is about to take out.
    """
    return sum(ppb_vintage_pp(y, v)
               for v in range(ppb_vintage_first(), y - 8))


def check_ppb_clock():
    """True when no PPB vintage survives the year after its eight-year deadline.

    This is the check that catches a **LIFO release**.  Releasing newest-first meets the
    aggregate PPB recursion exactly and satisfies :func:`check_ppb_roll_fwd`, while
    letting an old vintage sit past its statutory deadline behind young ones that keep
    being spent - a breach that is invisible in the balance and obvious in the ledger.
    The clock counts financial years, so the sweep does too.
    """
    return all(abs(check_ppb_clock_resid(y)) <= 1e-8
               for y in range(proj_years))                           # noqa: F821


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere."""
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected **month**.

    Rebuilt from the decrements rather than from :func:`pols_if_at`, so that the
    processing order - deaths first, then surrenders on the survivors - is asserted
    rather than assumed.  Applying both decrements to the start-of-month count instead
    understates the exits by ``q_m w_m l(t)`` a month.
    """
    scale = max(pols_if_init(), 1.0)
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * scale
               for t in range(proj_len()))


def check_decrements_compound_resid(t):
    """How far twelve monthly decrements miss the policy year's annual ones, in month t.

    ``[(1 - q_m)(1 - w_m)]^12 - (1 - q)(1 - w)``: zero to floating point, because both
    monthly rates are the constant-force conversion of the annual rate of the policy year
    containing month ``t``.
    """
    survive_mth = (1.0 - mort_rate_mth(t)) * (1.0 - lapse_rate_mth(t))
    survive_ann = (1.0 - mort_rate(t)) * (1.0 - lapse_rate(t))
    return survive_mth ** 12 - survive_ann


def check_decrements_compound():
    """True when twelve monthly decrements compound back to the annual ones, every year.

    The conversion itself, asserted directly rather than only through its consequence:
    it is what makes ``pols_if(12k)`` on this grid equal the annual-step model's
    ``pols_if(k)``, and therefore what makes every anniversary quantity reconcile.  It is
    checked at each year's first month, because the annual rates are properties of the
    policy year and do not move inside it.
    """
    return all(abs(check_decrements_compound_resid(t)) <= 1e-12
               for t in range(0, proj_len(), 12))


def check_pb_allocation_resid(y):
    """The allocation residual in projection year y; zero everywhere.

    ``I(y) + F(y) + D(y) - R(y) - A+(y) - topup(y)``: the whole of the year's statutory
    minimum is either credited or carried to the PPB, plus whatever an earlier year's
    vintage released, plus whatever the TMG obliged the insurer to add.
    """
    return (int_credited_pp(y) + fee_pp(y) + ppb_dotation_pp(y)
            - ppb_release_pp(y) - pb_min_pp(y) - insurer_topup_pp(y))


def check_pb_allocation():
    """True when the year's statutory minimum PB is fully accounted for, every year.

    **This residual is zero by construction in a correct implementation**, since
    ``pb_credited_pp`` is defined as ``A+(y) - D(y) + R(y)`` and ``int_credited_pp`` is
    that less the charge.  What it catches is the ways of getting there that are not
    correct, because the identity is stated in terms of the *rate* round trip rather than
    of the amounts: deducting the management charge a second time inside ``ts_net``,
    striking the rate on the closing balance instead of the `pro rata temporis` base,
    stacking the TMG on top of the allocation instead of flooring it, or dropping a
    dotation on the floor. Each of those leaves every printed number plausible and this
    residual non-zero.

    Note what the invariant is **not**.  ``ts_net(y) >= ts_stat(y)`` is not an invariant:
    a dotation year credits less than the statutory floor rate and that is legal, because
    the balance goes to the PPB and not to the insurer.
    """
    scale = max(av_pp_init(), 1.0)
    return all(abs(check_pb_allocation_resid(y)) <= 1e-9 * scale
               for y in range(proj_years))                           # noqa: F821


def check_cliquet_resid(y):
    """The `effet cliquet` residual in projection year y; zero everywhere.

    Three violations rolled into one signed number, each of which can only push it above
    zero: a break in the cumulative-PB ratchet over the year, negative credited interest,
    and a credited rate below the TMG.  The ratchet is read at the year's boundaries,
    ``pb_cum_pp(12(y+1))`` against ``pb_cum_pp(12y)``, because the ledger steps once a
    year.
    """
    ratchet = (pb_cum_pp(12 * (y + 1)) - pb_cum_pp(12 * y)
               - max(pb_credited_pp(y), 0.0))
    return (ratchet - min(0.0, int_credited_pp(y))
            - min(0.0, ts_net(y) - tmg_rate()) * pm_avg_pp(y))


def check_cliquet():
    """True when credited PB is never negative and the ratchet never falls.

    Credited `participation aux bénéfices` is definitively acquired and cannot be called
    back, so the credited interest can never be negative.  **In this implementation the
    non-negativity is enforced by construction**, by the ``max(tmg_rate(), ...)`` in
    :func:`ts_net`, so that half of the residual cannot move; the check is published
    because the constraint is a contractual fact about the product and a re-implementation
    that let a bad year claw back interest - by netting the management charge against the
    revalorisation, say, or by carrying a negative ``pb_acct_pp`` through to the account -
    would break it. The ratchet half is not by construction: it compares two independent
    recursions.

    What this does **not** say is that the account never falls.  Under the `garantie
    nette` the balance falls by the management charge in a nil-PB year, and the tables
    insurers publish for exactly that case prove it.  Testing the cliquet as "``av_pp`` is
    non-decreasing" is a listed pitfall; :func:`check_guar_floor` is the weaker and
    correct statement about the balance.
    """
    return all(abs(check_cliquet_resid(y)) <= 1e-8
               for y in range(proj_years))                           # noqa: F821


def check_guar_floor_resid(t):
    """The capital-guarantee shortfall in month t; zero when the floor holds.

    ``max(0, G(t) - (AV(t) + cumulative levies))``.  The floor is compared to the account
    **before** cumulative social levies, because the published minimum surrender-value
    tables are stated before social and tax levies.
    """
    return max(0.0, guar_floor_pp(t)
               - (av_pp(t) + soc_levy_cum_pp(t)))


def check_guar_floor():
    """True when the contractual capital floor is met in every projected **month**.

    A genuine inequality rather than an identity: nothing in the recursions enforces it,
    and on a path with a `taux servi` at or near zero for long enough the `garantie nette`
    floor and the account converge and then cross.  The monthly grid makes this a stronger
    statement than the annual one was - the floor steps down at the anniversary while the
    account only catches up at the same date, so the tightest month of each year is now
    looked at.  On the shipped scenarios it never binds, and knowing that it does not bind
    is the reason to check it.
    """
    return all(check_guar_floor_resid(t) <= 1e-6
               for t in range(proj_len()))


def result_cf():
    """Result table of cash flows, one row per **month**, ``t = 0 ... proj_len() - 1``.

    ``pols_if`` is the start-of-month count that weights every flow on the row.
    ``int_credited`` and ``soc_levy`` are published beside the flows and are **not** in
    ``net_cf``: the first is a state movement and the second is a policyholder tax the
    insurer remits, and both are nil in eleven months of twelve.  ``net_cf`` is
    income-positive; ``liability_cf`` is the notes' outgo-positive orientation, verbatim.
    :func:`result_cf_annual` sums the same frame into projection years.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "int_credited": [int_credited(t) for t in ts],
            "soc_levy": [soc_levy(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into projection years, indexed by ``y``.

    Every cash flow column is the total of its twelve months; ``pols_if`` is the count at
    the **start** of the projection year, ``pols_if(12y)``, which is the number the
    annual-step model this replaced carried on the same row.  It is the monthly frame
    regrouped, never a second projection.

    ``pols_if`` is the one column the two grids still agree on, because the monthly
    decrement rates compound back to the annual ones.  The flows do not agree and are not
    meant to: `versements` and `rachats partiels` are now collected from a block that
    decrements every month, expenses accrue on the in force of each month, claims fall at
    the end of the month of exit, and the year's revalorisation is weighted by the
    December in force.  That gap is the point of the finer grid.
    """
    df = result_cf()
    years = pd.Index([proj_year(t) for t in df.index], name="y")     # noqa: F821
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


def result_pb():
    """The crediting machinery, per policy, indexed by the projection year y, 0-based.

    The two tables of the notes' worked example side by side: the `compte de
    participation aux résultats` and the statutory floor rate it implies, the PPB
    dotation, release and balance, the `taux servi` actually credited, and the
    `épargne acquise` the whole apparatus moves.  Every column is a **financial-year**
    quantity, so this table has ``proj_years`` rows however fine the grid underneath it
    is, and every figure in it is the one the annual-step model produced.

    **One column is offset by a year.**  The ``ppb_pp`` column is ``ppb_pp(y + 1)``, the
    PPB at the **end** of year ``y`` - the notes' Table 1 header, which is literally
    ``ppb_pp(y+1)``, because the reader wants the balance the year's dotation and release
    leave behind.  ``av_pp`` and ``guar_floor_pp`` on the same row are the **start**-of-year
    values ``av_pp(12y)`` and ``guar_floor_pp(12y)``.  So on the anchor cell the ``y = 0``
    row shows ``ppb_pp`` 3 637.06 while the cells ``ppb_pp(0)`` is the 4 000.00 carried in.
    """
    ys = list(range(proj_years))                                     # noqa: F821
    return pd.DataFrame(                                             # noqa: F821
        {
            "r_fin": [r_fin(y) for y in ys],
            "pm_avg_pp": [pm_avg_pp(y) for y in ys],
            "fin_acct_pp": [fin_acct_pp(y) for y in ys],
            "tech_acct_pp": [tech_acct_pp(y) for y in ys],
            "insurer_tech_share_pp": [insurer_tech_share_pp(y) for y in ys],
            "pb_min_pp": [pb_min_pp(y) for y in ys],
            "ts_stat": [ts_stat(y) for y in ys],
            "ppb_dotation_pp": [ppb_dotation_pp(y) for y in ys],
            "ppb_release_pp": [ppb_release_pp(y) for y in ys],
            # End of year y, unlike av_pp / guar_floor_pp below - see the docstring.
            "ppb_pp": [ppb_pp(y + 1) for y in ys],
            "ts_net": [ts_net(y) for y in ys],
            "av_pp": [av_pp(12 * y) for y in ys],
            "int_credited_pp": [int_credited_pp(y) for y in ys],
            "soc_levy_pp": [soc_levy_pp(y) for y in ys],
            "guar_floor_pp": [guar_floor_pp(12 * y) for y in ys],
        },
        index=pd.Index(ys, name="y"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

proj_years = 40

omega_age = 120

mort_be_factor = 0.8

expense_maint = 24.0

expense_inflation = 0.015

expense_prop_rate = 0.0035

lapse_dyn_a = 4.0

lapse_dyn_tol = 0.0025

lapse_cap = 0.3

pd = ("Module", "pandas")
