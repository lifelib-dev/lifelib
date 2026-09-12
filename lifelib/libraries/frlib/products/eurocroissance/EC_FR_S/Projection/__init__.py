# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.EC_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_provisions()   # the worked example, Chassis A
    >>> Projection.point_id = 2             # Chassis B, same asset path

.. rubric:: The time index

``t`` counts **policy months**, 0-based, the clock ``basiclife.BasicTerm_S`` and the five
monthly models of this library run on: ``t = 0`` is the issue month, month ``t`` runs
from time ``t`` to time ``t + 1``, and the frame is
``range(proj_start(), proj_len())`` with ``proj_len() = 12 x policy_term()`` the
**number** of policy months projected — 120 on the worked example's ten-year term. Its
last row, ``proj_len() - 1``, is the month that ends at the *échéance*. A new-business
cell opens at ``proj_start() = 0``, where the initial *versement* net of the entry charge
creates the rights and the two provisions are first struck — that is the **opening
state** of month 0, reached as ``own_assets_at(0, "BOM")`` and its siblings, and not a row
of its own. An in-force cell opens at ``proj_start() = 12 x duration_ifo``: elapsed time
is recorded in whole policy years, so the frame always opens in the **first month of a
policy year** (shipped point 7 at ``t = 48``), where the extract's assets, parts and
guaranteed amount are seeded and the *provision mathématique* is re-derived rather than
read.

Everything contractual about this product is nevertheless on an **annual** cycle, so the
policy year is derived and used as a lookup key throughout: ``duration(t) = t // 12`` is
the completed policy years at the start of month ``t``, ``policy_year(t) = duration(t) +
1`` is the contractual 1-based label, and the attained age is ``age(t) = issue_age() +
duration(t)``, stepping on the anniversary rather than on the birthday. The **anniversary**
is the last month of a policy year, ``is_anniv(t)``, ``t ≡ 11 (mod 12)``. The frame is
indexed by ``t``; the policy year is never indexed by.

A handful of cells are indexed by a **month boundary** ``m`` rather than by a month:
``m = 0`` at issue and ``m = 12 n`` at the *échéance*, and :func:`rem_term`,
:func:`tec_rate`, :func:`i_pm` and :func:`disc_factor` are of that kind, so month ``t``
reads them at ``t`` for its opening and at ``t + 1`` for its end-of-month striking.
``rem_term(m) = (proj_len() - m) / 12`` is the remaining term in **years**, fractional
between anniversaries.

.. rubric:: Two speeds: annual assumptions on a monthly grid

The two-speed structure that follows is the library's convention, asserted by
``tests/test_model_conventions_fr.py``. ``mort_rate(t)``, ``lapse_rate(t)``,
``wd_rate(t)`` and ``asset_return(t)`` are the **annual** rates of the policy year
containing month ``t`` — the vectors the technical notes tabulate — and
``mort_rate_mth(t)``, ``lapse_rate_mth(t)``, ``wd_rate_mth(t)`` and
``asset_return_mth(t)`` are the rates actually applied in the month:
``1 - (1 - q)^(1/12)`` for a decrement and ``(1 + r)^(1/12) - 1`` for a return, so twelve
compound back to exactly the annual figure.

A monthly grid is not a monthly product. Every **contractual** mechanic stays where the
contract puts it: the R. 134-3 base 4° parts levy and a scheduled *versement* in the
**first month of a policy year**; the striking of the *compte de participation aux
résultats* and with it the base 5° performance levy, a free *versement* and the R. 134-12
*apport d'actifs* **on the anniversary**. What the finer grid adds is what A. 134-5
already required and the annual grid could not express: the **intermediate re-striking of
the diversification provision in every month in which the participation account is not
struck**, a **forward** part value for an exit, mortality and *rachat* falling in the
month they happen, and maintenance expense accruing where it is incurred.

.. rubric:: Anniversary equivalence, and the three places it does not hold

Because the monthly decrements and the monthly return compound back to the annual ones,
because the twelve monthly ``invest_income`` sum to the year's ``A_a r`` where no cash
moves inside the year, and because the parts levy and the top-up land at the same instant
on both grids, **every anniversary-dated value is what the annual-step model this one
replaced carried on the corresponding row** — ``own_assets``, ``pm``, ``prov_div``,
``parts``, ``part_value``, ``mg``, ``cum_prem_net``, ``insurer_contribution``, ``pgt``,
``pcdd``, ``provision_value``, ``surrender_value``, ``death_value``, ``death_payout``,
``maturity_value``, ``conversion_headroom``, ``gate_revalue_ok``, ``parts_levy`` and
``perf_levy`` at ``t = 12k + 11``, and ``pols_if`` at ``t = 12k``. Measured against a
pre-conversion snapshot of all eleven shipped model points, the largest absolute
difference is **1.3e-10 EUR** on figures of order 10,000.

Three things do not reproduce, and each is the point of the exercise rather than a defect:

* the **cash flows**, which now fall where they happen — a claim at the end of the month
  of exit rather than of the year, a *versement* in its own month;
* :func:`expenses`, where maintenance now accrues at one twelfth a month on the month's
  own provision and in-force, and the annual grid's extra opening-striking charge is gone:
  -0.2% to -1.3% over a whole projection on the shipped cells, and +0.9% on point 9, whose
  annual *versements* step the provision up at the start of each of its first five years;
* on a cell with ``wd_factor > 0`` — shipped point 5 alone — the **asset-fed** values, because
  :func:`wd_rate_mth` spreads the *rachat partiel* instead of taking it all at the start of
  the year, so more capital earns return early: ``own_assets`` at the anniversaries runs
  0.21 to 3.05 EUR above the annual model's, at most 0.031%, ``part_value`` at maturity is
  25.097 against 25.0768, and total *rachats* are 0.23% higher. What still matches exactly
  there is everything whose run-down is purely multiplicative — ``mg``, ``cum_prem_net``,
  ``pm``, ``parts`` and ``pols_if`` — because ``(1 - w_pm)^12 = 1 - w_p``.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/eurocroissance/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``EC_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.EC_FR_S.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
scenario_table_file     data.scenario_table()           scenario_table.csv
tec_curve_file          data.tec_curve()                tec_curve.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
**annual** rates and ``*_rate_mth`` for the monthly ones derived from them, ``*_pp`` for
per-policy amounts, ``claims(t, kind)`` and ``claim_pp(t, kind)``
with an uppercase ``kind`` string, and the ``duration_mth`` / ``duration`` /
``policy_year`` triple the other monthly models of this library carry. The technical
notes use compact symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
engagement_modality        chassis()                       euro_and_parts or parts_only
(the 1° test)              is_euro_leg()                   True on Chassis A
t                          (the cells argument)            Policy month, 0-based
m                          (the cells argument)            Month boundary, m = 0 at issue
(none)                     duration_mth(t)                 Months elapsed at BOM, = t
dur(t)                     duration(t)                     Completed policy years, t // 12
y                          policy_year(t)                  Policy year of month t, dur + 1
(the anniversary)          is_anniv(t)                     True where t % 12 == 11
(the anniversary)          anniv_mth(t)                    Month that ends that policy year
n - m/12                   rem_term(m)                     Remaining term in years, at m
x                          issue_age()                     Entry age (âge atteint)
x + dur(t)                 age(t)                          Age entering the policy year
x + dur(t) + 1             age_anniv(t)                    Age attained at the anniversary
duration_ifo               duration_inforce()              Completed years at valuation
(none)                     proj_start()                    First projected month, 12 x above
n                          policy_term()                   Years to the échéance
(none)                     proj_len()                      Months projected, = 12 n
g                          guarantee_rate()                Share of net versements guaranteed
P_0                        premium_initial_pp(t)           Initial versement, opening state
P_net,0                    prem_init_after_charge()        Net of the R. 134-3 1° charge
P(t)                       premium_gross_pp(t)             Scheduled versement, BOM of a year
P_net(t)                   prem_after_charge_pp(t)               Net of the R. 134-3 1° charge
(free versement)           premium_top_up_gross_pp(t)      Free versement, on the anniversary
(free versement, net)      premium_top_up_net_pp(t)        Net of the entry charge
f_e                        entry_charge_rate()             Entry charge, base 1°
f_p                        parts_charge_rate()             Parts levy p.a., base 4°
f_perf                     perf_charge_rate()              Performance levy, base 5°
f_x                        exit_charge_rate()              Exit charge, base 6°
(indemnity)                surrender_indemnity(t)          R. 132-5-3 indemnity, capped
mg(t)                      mg(t)                           Guaranteed amount at n
(the steps)                mg_at(t, timing)                mg inside month t
(versement split, BOM)     parts_added_bom(t)              Parts a BOM versement buys
(versement split, anniv)   parts_added_top_up(t)           Parts the free versement buys
(cumulative net premiums)  cum_prem_net(t)                 Death-floor base
(opening)                  cum_prem_net_at(t, "BOM")       Its opening value
TEC(rem)                   tec_rate(m)                     Interpolated TEC at boundary m
i_pm(m)                    i_pm(m)                         90% of TEC, floored at zero
(discount factor)          disc_factor(m)                  (1 + i_pm(m))^-rem_term(m)
r(t)                       asset_return(t)                 Annual asset return of the year
r_m(t)                     asset_return_mth(t)             (1 + r)^(1/12) - 1, the month's
A(t)                       own_assets(t)                   Account assets, excluding C(t)
(the steps)                own_assets_at(t, timing)        The asset roll inside month t
pm(t)                      pm(t)                           Provision mathématique
(opening, pre-versement)   pm_at(t, timing)                PM opening and at the striking
pd(t)                      prov_div(t)                     Provision de diversification
(opening, pre-versement)   prov_div_at(t, timing)          PD opening and at the striking
N(t)                       parts(t)                        Number of parts
(the steps)                parts_at(t, timing)             Parts inside month t
u(t)                       part_value(t)                   Valeur de la part
(opening, pre-versement)   part_value_at(t, timing)        u opening and at the striking
u_min                      min_part_value()                Contractual floor on u
L(t)                       parts_levy(t)                   Levy at the BOM of a year, base 4°
I(t)                       invest_income(t)                Financial performance of month t
(year to date)             invest_income_ytd(t)            I accumulated since the year opened
F(t)                       perf_levy(t)                    Anniversary levy, base 5°
(entry)                    entry_charge(t)                 Base 1° charge on a versement
C(t)                       insurer_contribution(t)         L. 134-3 outstanding contribution
G(t)                       pgt(t)                          Provision pour garantie à terme
D(t)                       pcdd(t)                         Provision collective de div. différée
(apport d'actifs)          apport(t)                       R. 134-12 contribution to the PCDD
(A. 134-3 tests)           gate_revalue_ok(t)              Whether a revaluation is permitted
(A. 134-4 headroom)        conversion_headroom(t)          Parts convertible into PM
(surrender base)           provision_value(t)              pm(t) + pd(t)
(opening)                  provision_value_at(t, "BOM")    Its opening value
surrender_value(t)         surrender_value(t)              R. 134-5 value
death_value(t)             death_value(t)                  The current provision value
death_payout(t)            death_payout(t)                 After any garantie décès plancher
rider_claim(t)             rider_claim_pp(t)               The floor's cost, outside the account
maturity_value(n)          maturity_value(t)               R. 134-6 amount
(payouts)                  claim_pp(t, kind)               Payout per claim by kind
q(x+dur(t)+1)              mort_rate(t)                    Annual mortality rate
q_m(t)                     mort_rate_mth(t)                The monthly rate actually applied
w(t)                       lapse_rate(t)                   Annual full surrender rate
w_m(t)                     lapse_rate_mth(t)               The monthly rate actually applied
(table)                    lapse_rate_base(t)              Table full surrender rate
(partial rachat)           wd_rate(t)                      Annual partial surrender rate
w_pm(t)                    wd_rate_mth(t)                  The monthly rate actually applied
(partial rachat)           wd_pp(t)                        Partial surrender paid
(partial rachat, gross)    wd_gross_pp(t)                  Taken from the provision
(none)                     pols_if(t)                      In force at the **start** of month t
l(t)                       pols_if_at(t, "AFT_DECR")       In force at the **end** of month t
(none)                     pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
(none)                     pols_death(t)                   Deaths in month t
(none)                     pols_lapse(t)                   Full surrenders in month t
(none)                     pols_maturity(t)                Survivors reaching the échéance
(cash flows)               premiums, claims, withdrawals   Probability-weighted flows
E(t)                       expenses(t)                     Acquisition and maintenance
charges_taken(t)           charges_taken(t)                Insurer income, reported apart
CF(t)                      liability_cf(t)                 The notes' outgo-positive stream
(none)                     net_cf(t)                       Its negative, income positive
(none)                     model_point()                   The selected row as a Series
(none)                     result_cf_annual()              result_cf() summed into years
=========================  ==============================  ==========================

:func:`result_cf_annual` is the frame **regrouped**, never a second projection: every cash
flow column is the total of its twelve months and ``pols_if`` is the count entering the
policy year.  It exists so the annual-step model this one replaced can be laid beside this
one row for row — ``pols_if`` and ``premiums`` agree on it exactly, and ``expenses`` and
the claim columns deliberately do not.

Nine names needed care.

``pols_if`` is the count at the **start** of month t — the exposure every cash flow
on that same :func:`result_cf` row is weighted by — so ``result_cf()["pols_if"].iloc[0]``
is ``pols_if_init()`` on every model point.  This model first published the notes' own
``l(t)``, the count at the **end** of the period, under that name, which put the exposure
column one period ahead of the flows beside it: a reader dividing ``claims_death`` by that
row's ``pols_if`` to recover a per-policy payout got a stale answer, and nothing
raised.  The end-of-period quantity survives unchanged and unrenamed in substance — it is
now reached as **``pols_if_at(t, "AFT_DECR")``**, the ``CashValue_SE`` timing form this
library uses for every other intra-period state — and every number in :func:`result_cf`
except the ``pols_if`` column is what it was before the change.  The notes, ``model.md``
and the test module index ``l(t)`` the same way.

The ``*_at(t, timing)`` cells open on **``"BOM"``**, the beginning of the month.  It was
``"BOY"`` while the step was a policy year and moved with the grid; the retired spelling
raises rather than being silently accepted, which is the cheapest guard against a
half-finished conversion.  The other timings — ``"AFT_LEVY"``, ``"AFT_EXIT"``,
``"AFT_PREM"``, ``"AFT_RETURN"``, ``"AFT_PERF"``, ``"AFT_STRIKE"``, ``"AFT_TOP_UP"``,
``"BEF_DECR"``, ``"BEF_LAPSE"``, ``"AFT_DECR"`` — are unchanged, because they name a step
of the recursion rather than a length of time.

``parts_added_bom`` and ``parts_added_top_up`` are the two *versement* splits, named for
**where they land** rather than for BOY and EOY.  They are two different rules, not one
rule at two times: the first prices at the opening part value and splits at
``disc_factor(t)``, the second prices at the part value just struck and splits at
``disc_factor(t + 1)``.

``age`` is the age **entering** the policy year of month t and ``age_anniv`` the age
attained at the anniversary that closes it.  The mortality assumption is read at
``age_anniv``, which is the notes' ``q(x + t + 1)``: the age rule belongs to the annual
assumption and moving it to the entering age would shift every decrement by a year of age
and break the anniversary equivalence outright.  ``age`` is published anyway, because the
library's monthly vocabulary expects it and because the *âge atteint* convention is stated
on it.

``pm_ifo`` appears in the notes' model point attribute table but is **not** an input the
projection reads. The *provision mathématique* is re-struck from ``mg`` and the current
``i_pm`` every month, so an in-force cell that supplied one would be asserting a number
the rule already determines. The column is shipped and :func:`check_pm_restruck` compares
it against the re-strike — which is how a reader discovers that an extract was built by
accumulating the PM instead.

``lapse_rate`` is the **full** surrender (*rachat total*) and ``wd_rate`` the **partial**
one (*rachat partiel*). They are different events with different consequences: a full
surrender removes the policy, a partial one runs the guarantee, the parts and the assets
down pro rata and leaves the contract in force. Sharing one name would have merged a
decrement with an owner election.

``wd_gross_pp`` and ``wd_pp`` differ by the base 6° exit charge — what leaves the
provision and what reaches the saver. Both are needed, because the provision run-down
keys off the gross amount and the cash flow off the net one.

``provision_value`` is ``pm + pd``, the base of R. 134-5 and R. 134-6. It is the same
expression on both chassis because ``pm`` is identically zero on Chassis B, so the
surrender and death rules are one formula rather than two.

``pd`` is the one notes symbol this model could not keep. ``pd`` is **pandas** in every
model in this library, and shadowing it inside the one Space that has to build a
DataFrame is not worth a two-letter symmetry, so the *provision de diversification* is
:func:`prov_div` here while the *provision mathématique* keeps :func:`pm`, whose symbol
was free. The displayed formulas below stay in the notes' notation; the table above is
what maps them.

There is **no** ``av_pp_at`` in this model. A eurocroissance engagement is not an account
value: the saver's rights are a number of *parts* whose value is common to every
engagement of the auxiliary account, plus — on Chassis A — a share of a *provision
mathématique* that is a discounted promise rather than a fund. Naming either of them the
library's account value would assert something false about the contract.

.. rubric:: The provision mathématique is re-struck, never accumulated

::

    pm(t) = mg(t) (1 + i_pm(t+1))^-rem_term(t+1)   Chassis A
    pm(t) = 0                                      Chassis B

``pm(t)`` is the closing PM of month t, struck at its month end — boundary ``t + 1``,
where the remaining term is the **fractional** ``(12n - t - 1)/12`` years. ``i_pm(m)`` is
90% of the TEC, floored at zero
(A. 134-1), read here at the **remaining** maturity — a **[std]** reading of the
article's index maturity, which :func:`tec_rate` sets out. It is **not** the A. 132-1
maximum technical rate and not the
A. 132-3 guaranteed rate ceiling, which are different and stricter objects. Rolling ``pm(t-1)`` forward at
last year's rate would silently remove the **rate effect**: in the notes' worked example
that is +587.44 of the +824.18 move over policy year 6, ``t`` = 59 to ``t`` = 71, against
a time effect of only +236.74.

**The monthly re-strike is a decision, and it is [std].** R. 134-2 defines the PM as the
guaranteed amount discounted at the A. 134-1 rate, a definition with a value at every
instant; A. 134-5 requires the diversification provision to be re-struck at an
intermediate value at least monthly, which on Chassis A is impossible without a PM for the
residual to be taken against. Holding the PM flat between strikings would make it a step
function and push a year of time effect onto the anniversary, so the intermediate part
value would be wrong in exactly the direction A. 134-5 exists to prevent. It is the same
article being read at a finer frequency as the ``n - k`` remaining-term reading, and it is
recorded in the same paragraph of the notes. It also makes
:func:`check_guarantee_funding` hold **month by month** rather than only at anniversaries.

The finer grid splits the policy-year-6 move in two, which the annual grid could not: the
PM accretes from 10,541.34 at ``t`` = 60 to 10,738.63 at ``t`` = 70 at the unchanged 2.25%
— the **time effect** — and jumps to 11,346.00 at ``t`` = 71, where the TEC curve is
re-published at 1.00% — the **rate effect**, +607.37 in one month. The year-on-year
+236.74 / +587.44 decomposition is unchanged.

At the *échéance* the discount factor is 1, so ``pm(12n-1) = mg(12n-1)`` identically and
the Chassis A guarantee is pre-funded by construction. :func:`check_guarantee_funding`
asserts it at every ``t``, and it is the model's headline check.

.. rubric:: The monthly re-striking and the annual participation account

::

    L(t) = f_p pd_open(t) 1{t % 12 == 0}  A_a = A_open(t) - L(t) - W(t) + P_net(t)
    I(t) = A_a r_m(t)                     F(t) = f_perf max(I_ytd(t), 0) 1{is_anniv(t)}
    A(t) = A_a + I(t) - F(t)              N(t) = N_open(t)(1 - f_p 1{BOM})(1 - w_pm) + ...
    pd(t) = max(A(t) - pm(t), N(t) u_min)  u(t) = pd(t)/N(t)
    C(t)  = max(pm(t) + pd(t) - A(t), 0)

``A_open(t)`` is ``own_assets_at(t, "BOM")`` and its siblings: ``A(t-1)`` in every month
but the first projected one, and in that one the state the initial *versement* — or the
in-force extract — creates. That is where the issue instant lives; it is not a row of the
frame.

Two of the six R. 134-3 bases keep an annual rhythm inside this monthly recursion, and
for two different reasons. The base 4° levy ``L(t)`` falls in the **first month of each
policy year** because ``product-spec.md`` states it taken there on the opening part value:
it is a contract term, not an assumption, and spreading it would change the cash it takes
even though the parts count would compound back. The base 5° levy ``F(t)`` falls **on the
anniversary** on the year's accumulated performance ``I_ytd`` because R. 134-3 5° is a levy
on the balance of the participation account and R. 134-4 strikes that account at least
annually; a monthly levy would tax a positive month inside a losing year, which the
asymmetric ``max(., 0)`` exists not to do, and would have taken money in policy year 6. A
policy exiting between anniversaries therefore pays no performance levy for the part year,
which is what the article's annual striking implies.

The diversification provision takes the **residual** and stops at the parts' contractual
floor. Where the floor binds, the two provisions together exceed the assets, and the
excess is exactly ``C(t)`` — the contribution the insurer must make under L. 134-3 to
complete the representation. The **surrender value therefore exceeds the account's own
assets by exactly ``C(t)``** while the contribution is outstanding: at the anniversary of
the notes' policy-year-6 shock, month ``t`` = 71, 12,384.73 paid against assets of
10,250.65. The monthly grid says when that starts, which the annual grid could not: the
part-value floor **first binds in month 66**, and the contribution starts there at 141.96
and climbs to 2,134.08 by the anniversary.

``C(t)`` carries **no return to the savers**: :func:`own_assets` rolls forward from
``A(t-1)``, not from ``pm(t-1) + prov_div(t-1)``. Rolling the topped-up balance forward would
manufacture investment return out of the insurer's capital, and the shipped worked
example is the case that catches it — the policy-year-7 asset roll, month ``t`` = 72,
starts from 10,250.65 and not from 12,384.73.

.. rubric:: The Chassis B surrender value is not guaranteed

This is the single most important product fact. Before the *échéance* a 2° engagement
pays ``parts × part value`` and **nothing else** (R. 134-5). The guarantee bites only at
the *échéance* — the end of the last projected month, ``t = proj_len() - 1`` — and only
there does :func:`maturity_value` take ``max(parts × u, mg)``. At the anniversary of the
notes' policy-year-6 shock, month ``t`` = 71, Chassis B surrenders for **9,899.22** —
84.18% of
net *versements* against a guarantee of 11,760.00. An implementation that floors the
surrender value at the guarantee, or at the discounted guarantee, is modelling a contract
that does not exist. :func:`check_own_funds_not_paid` asserts that no benefit before the
term exceeds the two provisions.

The monthly grid makes the same point sharper, and honours A. 134-5 in doing so: a saver
surrendering in **month 65** receives **11,430.63**, the striking of the month the request
falls in, and not the 9,899.22 the anniversary reports. That is the *forward* part value
the article requires, and delivering it is the one place this conversion **removes** a
documented simplification rather than adding one.

The shortfall against the guarantee is carried instead as the *provision pour garantie à
terme*, :func:`pgt` — the insurer's own funds, computed per auxiliary account on the
A. 132-18 tables at a rate at most 90% of the TEC, counting **no cash flows other than
guarantee maturities and mortality**. It sits outside the participation account, it is
not part of any benefit, and a model must not "improve" its deliberately narrow basis by
adding lapses or expenses to it. Of the article's two admitted drivers this model
implements only the guarantee maturity: :func:`pgt` applies **no survival factor**, a
prudent **[std]** simplification that the cells docstring quantifies. Struck monthly like
everything else, it shows the provision being constituted: on the worked example's
Chassis B it **first becomes positive in month 68**, at 61.48, and reaches 1,446.78 by the
anniversary at month 71.

.. rubric:: The death benefit is not the maturity guarantee

Chapter IV of the regulatory part contains no death valuation article. The death benefit
is the **current provision value**, and any *garantie décès plancher* is a complementary
guarantee provisioned **outside** the auxiliary account (R. 134-7). :func:`death_payout`
therefore floors the payout at cumulative net *versements* where the model point elects
the rider, and :func:`rider_claim_pp` reports the difference separately — 1,860.78 on the
notes' policy-year-6 Chassis B death at month ``t`` = 71, which is not the account's money.

.. rubric:: The charge bases are not interchangeable

R. 134-3 permits six bases and no others, and base 3° — a levy on the *encours* of the
diversification provision — is available only in an auxiliary account holding **no** 1°
engagements. No base permits a levy on the *provision mathématique* at all. The recurring
charge here is therefore base 4°, a levy **in number of parts**: :func:`parts_levy` is
``f_p × prov_div_at(t, "BOM")`` in the first month of each policy year, and
:func:`parts_at` cancels ``f_p`` of the parts there and nothing in the other eleven
months. On the worked example's Chassis A that is **15.64** opening policy year 1,
``t`` = 0. An *encours*
levy on ``pm + pd`` would have been 78.40 — five times as much, and unlawful in a 1°
account.

.. rubric:: Behaviour, and what is not modelled

All dynamic shapes are **[std]**: no eurocroissance lapse experience is public and the
product is too small and too young to have any. Three overlays sit on the base full
surrender rate:

- a **guarantee-imminent suppression** of 0.5 over every month of the two policy years
  before the *échéance* on Chassis B, and only while the guarantee is in the money — a
  saver who surrenders in that state gives up the entire guarantee, which is the strongest
  exit deterrent the product creates. The in-the-money test is read on the **current
  month's** striking, which is what the behavioural statement says and which on every
  shipped model point agrees with the anniversary reading in every month;
- a **duration-8 spike** of 1.5 over policy year 8 where ``n > 8``, because the
  assurance-vie annual *abattement* becomes available at eight years; and
- a **lock-up**, where ``lock_up_years > 0`` bars surrender entirely, the L. 132-23
  hardship exits not being separately modelled.

All three are multipliers on the **annual** rate, applied before the monthly conversion,
so each grades once a year as the behaviour it stands for does and not once a month. The
non-surrender period and the *échéance*-year exclusion are likewise read on
``duration(t)``, not on the month, so the monthly grid opens no month the annual grid
closed.

Out of scope, and held at zero or absent by design: the PCDD **piloting rule** (run the
fund at 30 bp above the insurer's own euro fund and carry the rest to the PCDD) and the
PCDD's release back into the participation account — :func:`pcdd` accumulates the
R. 134-12 *apport d'actifs* and nothing else; the conversion of parts into PM under
A. 134-4, whose headroom :func:`conversion_headroom` computes without exercising; the
revaluation of guarantees out of the participation account, whose two A. 134-3 gates
:func:`gate_revalue_ok` tests without exercising; the *rente viagère* option at the
*échéance*, which :func:`annuity_option_flag` rejects by name; and the statutory
arbitrage into an SRI ≤ 2 support that A. 134-6 makes the maturity default.

.. rubric:: What a single-policy model cannot say

The part value, the PCDD, the PGT and the *apport d'actifs* are all **account-level**
quantities. The part value in particular is common to every engagement of an auxiliary
account, so savers with different maturities and different guarantee levels in one
account earn the same rate and differentiation is possible only through the number of
parts. A per-policy model can only approximate that, and the *mémoire* records that
pooling two maturity cohorts in one account produces **no** mutualisation benefit at all.
Model points 1 and 2 are two separate accounts on the same asset path, and their part
values duly diverge; two engagements of one account would not.

The deterministic single scenario is the other limit. The maturity guarantee is a put on
the auxiliary account, its cost is convex in the asset shock and in the level of rates,
and a deterministic run understates it. What this model produces is exactly the
per-scenario cash flow vector a market-consistent stochastic valuation consumes.
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


def chassis():
    """``euro_and_parts`` (1° engagement) or ``parts_only`` (2° engagement).

    L. 134-1 defines exactly these two modalities, and R. 134-2 to R. 134-6 give each of
    them its own provision structure, surrender value and maturity amount.  A value
    outside the pair is a data error and raises rather than defaulting to one of them.
    """
    v = model_point()["engagement_modality"]
    if v not in ("euro_and_parts", "parts_only"):
        raise ValueError("invalid engagement_modality: " + str(v))
    return v


def is_euro_leg():
    """True on Chassis A, the 1° engagement that carries a *provision mathématique*.

    On Chassis B ``pm`` is identically zero, the whole engagement is expressed in parts,
    and the guarantee is carried by the insurer's own funds until the *échéance*.
    """
    return chassis() == "euro_and_parts"


def issue_age():
    """x: the entry age of the model point, *âge atteint* (age last birthday) **[std]**.

    A. 335-1 applies the homologated tables with the annexed *décalages d'âge* rather than
    fixing a model age basis, so the basis is a standardization.
    """
    return int(model_point()["issue_age"])


def sex():
    """The sex (M / F) of the model point.

    A. 132-18 requires the mortality basis to be by sex, so the decrement table is
    sex-distinct even though the tariff itself may not be.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex: " + str(v))
    return v


def policy_term():
    """n: the years from issue to the *échéance*, at which the guarantee is payable.

    The retrieved market range is 8 to 40 years; the worked example uses 10.
    """
    return int(model_point()["policy_term"])


def duration_inforce():
    """Completed policy years at the valuation date; 0 on a new-business cell.

    An in-force cell is seeded from its extract's assets, parts and guaranteed amount and
    carries no accumulated *provision mathématique* — see :func:`pm_init`.
    """
    return int(model_point()["duration_ifo"])


def guarantee_rate():
    """g: the share of cumulative net *versements* guaranteed at the *échéance*.

    100% in the worked example; the retrieved market range is 80% to 100%, chosen by the
    saver.  This is the product's single largest dial: it sets how much of the account is
    locked into the guaranteed leg and therefore how much of it can bear risk.
    """
    return float(model_point()["guarantee_rate"])


def premium_gross_init():
    """The initial gross *versement* paid at issue; nil on an in-force cell."""
    return float(model_point()["premium_gross"])


def premium_regular_pp():
    """The scheduled annual gross *versement* paid at the start of each policy year.

    Zero on a single-*versement* cell, which is the ordinary eurocroissance shape.
    """
    return float(model_point()["premium_regular"])


def premium_regular_years():
    """The number of policy years over which the scheduled *versement* is paid."""
    return int(model_point()["premium_regular_years"])


def premium_top_up_pp():
    """The free additional gross *versement*, paid at the **end** of a stated policy year.

    The worked example's is €2 000.00 at the end of policy year 3, and it is what makes
    the *versement* split rule visible: paid immediately after the year's striking, it
    buys parts at the part value just struck and raises the guaranteed amount by ``g``
    times its net amount.
    """
    return float(model_point()["premium_top_up"])


def premium_top_up_year():
    """The policy year at whose end the free additional *versement* is paid; 0 if none."""
    return int(model_point()["premium_top_up_t"])


def entry_charge_rate():
    """f_e: the entry charge on each *versement*, R. 134-3 base 1° **[std]**.

    2.00% in the reference configuration; 4.50% is the only published maximum retrieved
    for any eurocroissance support.  It is deducted **before** rights are created, which
    is why the guarantee is a percentage of *net* *versements* — see :func:`mg`.
    """
    return float(model_point()["entry_charge_rate"])


def parts_charge_rate():
    """f_p: the recurring levy in number of parts p.a., R. 134-3 base 4° **[std]**.

    0.80% p.a., taken at the start of the policy year on the opening part value.  Base 4°
    is a levy **in number of parts**, not on an *encours*: R. 134-3 3° permits an encours
    levy only in an auxiliary account holding no 1° engagements, and no base permits any
    levy on the *provision mathématique*.
    """
    return float(model_point()["parts_charge_rate"])


def perf_charge_rate():
    """f_perf: the levy on positive financial performance, R. 134-3 base 5° **[std]**.

    10% of the policy year's positive financial-management performance, taken on the
    anniversary, and nothing at all on a negative one — which is why the worked example's
    policy-year-6 performance levy, at month ``t`` = 71, is zero.
    """
    return float(model_point()["perf_charge_rate"])


def exit_charge_rate():
    """f_x: the exit charge on amounts leaving the account, R. 134-3 base 6° **[std]**.

    Zero in the reference configuration — the code permits it and neither retrieved
    insurer shows one.
    """
    return float(model_point()["exit_charge_rate"])


def surrender_indemnity_rate():
    """The *indemnité de rachat* rate on a full surrender **[std]**.

    Zero in the reference configuration.  R. 132-5-3 caps it at 5% of the present value of
    the mutual engagements and **permits** the contract to charge none at all once it has
    been in force more than ten years — a permission, not a prohibition.
    :func:`surrender_indemnity` takes that permission up unconditionally **[std]**.
    """
    return float(model_point()["surrender_indemnity_rate"])


def part_value_init():
    """u(0): the *valeur de la part* at the auxiliary account's inception.

    €10.0000 in the reference configuration.  It is a denomination rather than an
    assumption: what matters is the ratio of the part value to its floor, since that is
    how far the diversification provision can fall before the floor binds.
    """
    return float(model_point()["part_value_init"])


def min_part_value():
    """u_min: the contractual minimum *valeur de la part*, R. 134-1 **[std]**.

    €5.0000 in the reference configuration, and nowhere published for any insurer.  A
    debit balance on the participation account may reduce the part value only **within the
    limit of its minimum** (R. 134-4), so this level sets the floor of the diversification
    provision — and therefore both the Chassis A maturity payout and the point at which
    the insurer must start contributing assets.  Without it the worked example's Chassis A
    ``prov_div`` would go to **-1,095.35** at the anniversary of policy year 6, ``t`` = 71.
    """
    return float(model_point()["min_part_value"])


def lock_up_years():
    """The non-surrender period in years; capped at ``min(n, 8)`` by R. 134-5.

    Zero in the reference configuration.  The L. 132-23 hardship exits are not separately
    modelled **[std]**.
    """
    v = int(model_point()["lock_up_years"])
    if v > min(policy_term(), lock_up_cap):                          # noqa: F821
        raise ValueError("lock_up_years exceeds the R. 134-5 cap")
    return v


def death_floor_flag():
    """Whether the model point carries a *garantie décès plancher*.

    A complementary guarantee provisioned **outside** the auxiliary account (R. 134-7),
    floored at cumulative net *versements*.  It is not the maturity guarantee and does not
    become payable because the saver died before the *échéance*.
    """
    return bool(model_point()["death_floor_flag"])


def annuity_option_flag():
    """Whether the model point elects conversion into a *rente viagère* at the *échéance*.

    R. 134-6 permits it, and it is **out of scope** here: an annuity conversion needs the
    TGH05 / TGF05 generational tables, which are cited by arrêté and never shipped, and a
    projection that continues past the *échéance*.  No shipped model point elects it, and
    a cell that did raises rather than being paid a lump sum in silence.
    """
    v = bool(model_point()["annuity_option_flag"])
    if v:
        raise ValueError("the rente viagère option at the échéance is out of scope")
    return v


def wd_factor():
    """The multiplier on the table partial-surrender rate; 0 switches *rachats partiels* off.

    The worked example takes none, which is what lets its provision path be read as the
    cash flow path.
    """
    return float(model_point()["wd_factor"])


def apport_rate():
    """The R. 134-12 *apport d'actifs*, as a fraction of the diversification provision.

    Capped at 10% by the article.  It enters the auxiliary account at realisation value
    and **endows the PCDD**; it is never credited to the savers' diversification
    provision, and switching it on changes no policyholder value by one cent.
    """
    return float(model_point()["apport_rate"])


def apport_year():
    """The policy year at whose end the *apport d'actifs* is made; 0 if none."""
    return int(model_point()["apport_t"])


def decrement_basis():
    """``table`` or ``none``: whether mortality and full surrender are applied.

    ``none`` is not a modelling shortcut but the worked example's stated configuration:
    with ``mort_rate = 0`` and ``lapse_rate = 0`` the in-force probability stays at 1 and
    the per-policy provision path **is** the cash flow path, which is what makes the
    notes' two tables readable as provisions rather than as expected values.
    """
    v = model_point()["decrement_basis"]
    if v not in ("table", "none"):
        raise ValueError("invalid decrement_basis: " + str(v))
    return v


def scenario():
    """The asset-return path and TEC curve the model point runs on.

    Both the return and the discount curve are drawn from the same scenario name, because
    the two move together: the policy-year-6 double shock in the worked example — months
    ``t`` = 60 to 71, equities down and rates down at once — is what makes the rebalancing
    visible, and pairing an equity fall with an unchanged curve would understate the
    *provision mathématique* by the whole rate effect.
    """
    return model_point()["scenario"]


def own_assets_init():
    """A: the auxiliary-account assets attributable to the policy at the valuation date.

    At realisation value (R. 134-8) and **excluding** any outstanding insurer
    contribution, which is not the savers' money.  Zero on a new-business cell, where
    :func:`own_assets` seeds from the initial net *versement* instead.
    """
    return float(model_point()["own_assets_ifo"])


def parts_init():
    """N: the number of *parts de provision de diversification* at the valuation date."""
    return float(model_point()["parts_ifo"])


def mg_init():
    """mg: the guaranteed amount payable at the *échéance*, at the valuation date."""
    return float(model_point()["mg_ifo"])


def pm_init():
    """The *provision mathématique* the in-force extract reports; **not** an input.

    It is read by :func:`check_pm_restruck` alone.  R. 134-2 makes the PM the guaranteed
    amount discounted at the *current* A. 134-1 rate, so an extract cannot supply it and
    a projection cannot roll it forward — it is re-derived every year, and comparing the
    two is how a reader discovers an extract built by accumulation.
    """
    return float(model_point()["pm_ifo"])


def cum_prem_net_init():
    """The cumulative net *versements* at the valuation date: the death-floor base."""
    return float(model_point()["cum_prem_net_ifo"])


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_start():
    """The first projected **month**: ``12 x duration_inforce()``.

    Zero on a new-business cell, where month ``t = 0`` is the issue month and opens on the
    initial *versement*, which creates the rights and strikes both provisions.  On an
    in-force cell ``duration_ifo`` is the completed policy **years** at the valuation
    date — an elapsed count, already 0-based — so twelve times it is the first month of
    the policy year the extract opens.  Shipped point 7 has ``duration_ifo = 4`` and
    therefore opens at ``t = 48``.  Elapsed time is recorded in whole policy years, so
    **the frame always opens in the first month of a policy year**.
    """
    return 12 * duration_inforce()


def proj_len():
    """The **number** of policy months projected: ``12 x policy_term()``.

    The exclusive end of the frame, so the frame is ``range(proj_start(), proj_len())``
    and the last projected month is ``proj_len() - 1``, the month that ends at the
    *échéance*.  120 on the worked example's ten-year term.  The projection stops there
    because that is where the contract's guarantee is discharged.  A model point electing
    the *rente viagère* option would have to run past it, which is why
    :func:`annuity_option_flag` rejects one.

    :func:`policy_term` stays in **years**, because the contract states the *échéance* in
    years; the 12 lives here and in :func:`proj_start`.
    """
    return 12 * policy_term()


def duration_mth(t):
    """Months elapsed from issue at the start of month t; equal to ``t``.

    ``t`` is 0-based and counts from the contract's inception even on an in-force cell,
    whose frame simply opens later at ``proj_start()``, so the identity is trivial - the
    cells exists so the monthly models in this library share one vocabulary.
    """
    return t


def duration(t):
    """Completed policy years at the start of month t: ``duration_mth(t) // 12``.

    0-based, as ``duration`` is throughout lifelib: 0 through the first policy year.  It
    is what the *versement* schedule, the lock-up, the surrender indemnity and the
    last-policy-year exclusions are read on, all of which the contract states in years.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y: the contractual policy year containing month t; 1 for t = 0..11.

    The 1-based label ``duration(t) + 1``, derived from the 0-based ``t`` and **never
    indexed by**.  It is what ``lapse_table.csv`` is keyed by - both the *rachat total*
    and the *rachat partiel* columns - and what ``premium_top_up_t`` and ``apport_t``
    name.
    """
    return duration(t) + 1


def is_anniv(t):
    """True in the **last month of a policy year**, ``duration_mth(t) % 12 == 11``.

    The policy anniversary, and the date every *contractually* annual event of this
    product lands on: the striking of the *compte de participation aux résultats* and with
    it the R. 134-3 base 5 deg performance levy, the free *versement*, and the R. 134-12
    *apport d'actifs*.  The base 4 deg parts levy is the exception and falls at the
    **opening** of the policy year, ``duration_mth(t) % 12 == 0``, because
    ``product-spec.md`` states it taken at the start of each policy year.
    """
    return duration_mth(t) % 12 == 11


def anniv_mth(t):
    """The month index of the anniversary that **ends** the policy year containing t.

    ``12 x duration(t) + 11``, which is ``t`` itself where :func:`is_anniv` is true.  It
    is what a reader lays beside the annual-step model this one replaced: the anniversary
    month's closing values are that model's row for the same policy year.
    """
    return 12 * duration(t) + 11


def rem_term(m):
    """The remaining term to the *échéance*, in **years**, at month boundary ``m``.

    ``(proj_len() - m) / 12``, and **fractional** between anniversaries: A. 134-1's index
    maturity really does shorten continuously, so the maturity the TEC curve is
    interpolated at and the exponent the guarantee is discounted over both move month by
    month.  Zero at ``m = proj_len()``, the *échéance*, where the discount factor is 1.

    A **month boundary** rather than a month: month ``t`` opens at ``m = t`` and is struck
    at ``m = t + 1``, which is the argument :func:`disc_factor` is read at for the
    striking.
    """
    return (proj_len() - m) / 12.0


def age(t):
    """x + dur(t): the attained age (*âge atteint*) **entering** the policy year of month t.

    Age steps on the policy **anniversary**, not on the birthday and not monthly, which is
    the *âge atteint* convention the whole model is built on **[std]**.  The decrement is
    read one year later, at :func:`age_anniv`, because the annual mortality assumption
    this model converts is the rate of the age attained at the year's end - see
    :func:`mort_rate`.
    """
    return issue_age() + duration(t)


def age_anniv(t):
    """x + dur(t) + 1: the age attained at the anniversary that **closes** the policy year.

    The age :func:`mort_rate` reads the notes' ``q(x + t + 1)`` at.  Keeping the annual
    assumption on the end-of-year age rather than moving it to the entering age is what
    makes the in-force at every anniversary reproduce the annual-step model exactly; the
    age rule is part of the assumption, and the finer grid changes only when within the
    year the decrement falls.
    """
    return issue_age() + duration(t) + 1


def asset_return(t):
    """r(t): the **annual** gross asset return of the policy year containing month t **[std]**.

    Net of asset management fees, which is the basis the notes quote it on.  A **scenario**
    level rather than a best estimate: the guarantee is a put on the account and its cost
    is convex in this number, so a deterministic run understates it.

    The **annual** return of the policy year containing month t;
    :func:`asset_return_mth` is the return actually credited in the month.
    ``scenario_table.csv`` is keyed by the elapsed **year end** at which the return is
    credited, so the policy year of month t, which ends at ``duration(t) + 1`` years after
    issue, reads row ``duration(t) + 1``; its row 0 is the inception placeholder and is
    never read.  The last row is held beyond the table.
    """
    tbl = data.scenario_table()                                      # noqa: F821
    y = min(duration(t) + 1, int(tbl.index.get_level_values("year").max()))
    return float(tbl.loc[(scenario(), y), "asset_return"])


def asset_return_mth(t):
    """r_m(t) = ``(1 + r(t))^(1/12) - 1``: the return credited in month t **[std]**.

    Derived **geometrically** from the policy year's annual return and not by dividing by
    twelve, so that twelve months of it compound back to exactly that return - which is
    what makes the account assets at every anniversary identical to the annual-step
    model's.  On the worked example's path 4.00% a year is 0.327374% a month, -25.00% is
    -2.368842% and 6.00% is 0.486755%.

    The conversion is **[std]**: no retrieved French source states a within-year shape for
    a scenario return, and a constant force is the only shape that leaves the annual
    figure intact.
    """
    return (1.0 + asset_return(t)) ** (1.0 / 12.0) - 1.0


def tec_rate(m):
    """The *taux de l'échéance constante* at month boundary m, at maturity ``rem_term(m)``.

    A **month boundary**: ``m = 0`` at issue and ``m = 12 n`` at the *échéance*, and month
    ``t`` reads ``tec_rate(t)`` for its opening and ``tec_rate(t + 1)`` for its end-of-month
    striking.

    The curve is read in two speeds, and the split is the point.  ``tec_curve.csv``
    publishes **one curve per elapsed year**, so the row is ``m // 12`` — the **most
    recently published** curve, which is what A. 134-1's *dernier TEC publié* says
    **[std]**; interpolating a curve level between published years would invent data the
    file does not contain.  The remaining maturity, by contrast, shortens continuously, so
    the interpolation across maturities runs at the **fractional** ``rem_term(m)``.  The
    consequence is that the *provision mathématique*'s **time effect accrues month by
    month and its rate effect lands whole on the anniversary**.

    From A. 134-1: linear interpolation between the two bracketing maturities of the
    published curve, the longest rate held beyond the end of the curve, and the shortest
    held below its start — which is what ``k = n`` reaches, where the discount factor is 1
    and the rate is immaterial.  The method choice is irreversible per auxiliary account
    under the article; this model uses method 1°, the per-engagement one, throughout.

    **The index maturity is [std].**  The article as retrieved fixes it as the holder's
    guarantee maturity (method 1°) or the auxiliary account's 1°-engagement duration
    (method 2°), and says nothing about how that maturity is re-read at valuation dates
    after inception.  This model takes the **remaining** term ``n - k``, the horizon the
    guarantee is actually discounted over; holding ``n`` fixed at the original term would
    discount a one-year promise at a ten-year constant-maturity rate on the *échéance*.
    ``technical-notes.md`` states the reading and is the source of truth for it;
    ``product-spec.md`` states the article as retrieved.  The two readings differ only on a
    sloped curve, which is what shipped model point 10 exercises.
    """
    tbl = data.tec_curve()                                           # noqa: F821
    y = min(m // 12, int(tbl.index.get_level_values("year").max()))
    curve = tbl.loc[(scenario(), y), "tec_rate"]
    ms = [int(v) for v in curve.index]
    mat = rem_term(m)
    if mat <= ms[0]:
        return float(curve.iloc[0])
    if mat >= ms[-1]:
        return float(curve.iloc[-1])
    for lo, hi in zip(ms[:-1], ms[1:]):
        if lo <= mat <= hi:
            r_lo, r_hi = float(curve.loc[lo]), float(curve.loc[hi])
            return r_lo + (r_hi - r_lo) * (mat - lo) / (hi - lo)
    raise ValueError("no bracketing maturity for " + str(mat))


def i_pm(m):
    """The A. 134-1 discount rate for the *provision mathématique*: 90% of the TEC, floored.

    ``max(0, 0.90 x TEC(rem_term(m)))`` at month boundary m, the 90% haircut and the zero
    floor from the article and the remaining-maturity reading of ``n`` **[std]** — see
    :func:`tec_rate`.  A **month boundary**, like the curve it reads: month t is struck at
    ``i_pm(t + 1)``.  This is
    **not** the A. 132-1 maximum technical rate and
    **not** the A. 132-3 guaranteed-rate ceiling; those are different and stricter objects
    that apply to a tariff, while this one is a valuation ceiling for a provision the saver
    has no right to withdraw at.  The zero floor matters where the curve is negative: a
    model that let ``i_pm`` go negative would report a *provision mathématique* larger than
    the guarantee it discounts.
    """
    return max(0.0, tec_haircut * tec_rate(m))                       # noqa: F821


def disc_factor(m):
    """``(1 + i_pm(m))^-rem_term(m)``: the factor that turns the guarantee into the PM.

    A **month boundary**, like the rate it is built from: a beginning-of-month *versement*
    splits at ``disc_factor(t)`` and the end-of-month striking of month t discounts at
    ``disc_factor(t + 1)``.  The exponent is the **fractional** remaining term in years,
    so the PM is re-struck at an intermediate value in every month, which is what
    A. 134-5 requires and an annual grid could not express **[std]**.  It is one at
    ``m = proj_len()``, the *échéance*, by construction, which is the whole point — see
    :func:`check_guarantee_funding`.
    """
    return (1.0 + i_pm(m)) ** -rem_term(m)


def premium_initial_pp(t):
    """The initial gross *versement*, paid at the contract's inception.

    It falls at the very start of the first projected month on a new-business cell — month
    0, the issue month — where it creates the rights, and is nil on an in-force cell, whose
    *versement* was paid before the valuation date.

    It is the first projected **month's opening state** rather than a step in its roll
    forward: ``own_assets_at(t, "BOM")``, ``mg_at(t, "BOM")`` and their siblings already
    carry it net of the entry charge, which is why ``own_assets_at(t, "AFT_PREM")`` adds
    only the *scheduled* *versement*.  It is nonetheless a cash flow of month t, so it is in
    :func:`total_premium_pp` and reaches :func:`premiums`, :func:`entry_charge` and
    :func:`expenses` from there.
    """
    if t == proj_start() and duration_inforce() == 0:
        return premium_gross_init()
    return 0.0


def prem_init_after_charge():
    """The initial *versement* net of the R. 134-3 1° entry charge.

    The account's opening balance on a new-business cell, and ``g`` times it is the
    opening guaranteed amount — see :func:`mg`.
    """
    return premium_gross_init() * (1.0 - entry_charge_rate())


def premium_gross_pp(t):
    """P(t): the scheduled gross *versement*, received in the **first month** of a policy year.

    A **contractual annual term**, so it lands whole on the policy-year opening rather
    than being spread: ``product-spec.md`` gives no modal factor and no retrieved
    eurocroissance document shows one, so there is no *fractionnement* to collect it on.
    A ``premium_mode`` column with sourced modal factors is the natural extension, and is
    exactly what ``WholeLife_US_S`` added when its own sources published the factors.

    Payable in the months where ``duration_mth(t) % 12 == 0`` for
    ``premium_regular_years()`` policy years from the first projected one, so the last is
    the first month of policy year ``duration_inforce() + premium_regular_years()``.  On
    shipped point 9 that is months 0, 12, 24, 36 and 48.  The initial *versement* is
    **not** here: it is the opening state of the first projected month,
    :func:`premium_initial_pp`.
    """
    if (duration_mth(t) % 12 == 0
            and duration(t) < duration_inforce() + premium_regular_years()):
        return premium_regular_pp()
    return 0.0


def prem_after_charge_pp(t):
    """P_net(t): the beginning-of-month scheduled *versement* net of the R. 134-3 1° charge.

    **This is the base of the guarantee.**  The guarantee is a percentage of *versements*
    net of the entry charge, so a 2.00% charge on €12 000.00 of gross *versements* leaves
    a guaranteed amount of 11,760.00 and not 12,000.00.
    """
    return premium_gross_pp(t) * (1.0 - entry_charge_rate())


def premium_top_up_gross_pp(t):
    """The free additional gross *versement*, paid on the **anniversary** of a policy year.

    ``premium_top_up_t`` is the contractual **policy year** at whose end it falls, so on
    the monthly grid the test is ``is_anniv(t) and policy_year(t) ==
    premium_top_up_year()`` — the single month ``t = 12 x premium_top_up_year() - 1``, 35
    on the worked example.  Zero is the "no top-up" sentinel and matches no month.

    It stays whole on the anniversary because it is a discrete **contractual act** and
    because the split rule prices it on the striking it immediately follows,
    ``disc_factor(t + 1)`` and ``part_value_at(t, "AFT_STRIKE")``; on the anniversary that
    striking is the participation account's own.  A mid-year variant would need a
    ``premium_top_up_month`` column the composite has no basis to populate.
    """
    if (t >= proj_start() and is_anniv(t)
            and policy_year(t) == premium_top_up_year()):
        return premium_top_up_pp()
    return 0.0


def premium_top_up_net_pp(t):
    """The free additional *versement* net of the entry charge."""
    return premium_top_up_gross_pp(t) * (1.0 - entry_charge_rate())


def total_premium_pp(t):
    """Every gross *versement* of month t: the initial one, the scheduled one and any free one."""
    return (premium_initial_pp(t) + premium_gross_pp(t)
            + premium_top_up_gross_pp(t))


def entry_charge(t):
    """The R. 134-3 1° charge taken from the year's *versements*: insurer income."""
    return entry_charge_rate() * total_premium_pp(t)


def parts_added_bom(t):
    """The parts a beginning-of-month *versement* buys, at the **opening** part value.

    The *versement* splits under R. 134-2: ``g P_net`` discounted at the ``i_pm`` of the
    month's own opening — the ``m = t`` boundary — goes to the *provision mathématique*
    and the remainder buys parts at the opening part value.  On Chassis B nothing goes to
    the PM, so the whole net *versement* buys parts.
    """
    p = prem_after_charge_pp(t)
    if p <= 0.0 or t < proj_start():
        return 0.0
    u = part_value_at(t, "BOM")
    if u <= 0.0:
        return 0.0
    pm_add = guarantee_rate() * p * disc_factor(t) if is_euro_leg() else 0.0
    return (p - pm_add) / u


def parts_added_top_up(t):
    """The parts a free *versement* buys on the anniversary, at the part value **just struck**.

    Paid immediately after the month's striking, so it is priced on ``u(t)`` before the
    top-up rather than on the opening value, and split at the striking's own
    ``disc_factor(t + 1)``.  In the worked example the top-up on the anniversary that
    closes policy year 3 — month ``t`` = 35 — pays 1 960.00 net, which splits into
    ``1 960.00 x 1.0225^-7 = 1,677.31`` of PM and 282.69 of diversification provision,
    buying ``282.69 / 12.8688 = 21.9672`` parts on Chassis A — and the whole 1 960.00
    buying ``1 960.00 / 11.1193 = 176.2694`` parts on Chassis B.
    """
    p = premium_top_up_net_pp(t)
    if p <= 0.0:
        return 0.0
    u = part_value_at(t, "AFT_STRIKE")
    if u <= 0.0:
        return 0.0
    pm_add = guarantee_rate() * p * disc_factor(t + 1) if is_euro_leg() else 0.0
    return (p - pm_add) / u


def wd_rate_base(t):
    """The table annual partial-surrender rate of the policy year containing month t **[std]**.

    6% of the provision in policy years 1-2 and 3% thereafter; the *mémoire* observes 6%
    then 2%-4%.  ``lapse_table.csv`` is keyed by the contractual **policy year**, read here
    at ``policy_year(t)``; policy years beyond the table take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "wd_rate"])


def wd_rate(t):
    """w_p(t): the **annual** *rachat partiel* rate of the policy year containing month t.

    The rate the technical notes tabulate; :func:`wd_rate_mth` is the rate actually applied
    in the month.  Nil while the decrements are switched off, inside a non-surrender
    period — policy years 1 to ``lock_up_years``, so ``duration(t) < lock_up_years()`` —
    and **in the whole of the last policy year**, which ends at the *échéance*, where the
    contract is discharged in full instead.  That last exclusion is on
    ``duration(t) >= policy_term() - 1`` and not on the final month: the annual grid never
    let a *rachat* out of the *échéance* year, and restating the test on the month would
    quietly move a year of exits.

    Expressed as a fraction of the provision rather than as a cash amount, because a
    partial surrender takes the same proportion of every element of the engagement — the
    parts, the guaranteed amount and the death-floor base all run down pro rata with it.
    """
    if decrement_basis() == "none" or wd_factor() <= 0.0:
        return 0.0
    if (t < proj_start() or duration(t) < lock_up_years()
            or duration(t) >= policy_term() - 1):
        return 0.0
    return min(1.0, wd_factor() * wd_rate_base(t))


def wd_rate_mth(t):
    """w_pm = ``1 - (1 - w_p)^(1/12)``: the *rachat partiel* rate applied in month t **[std]**.

    Derived **geometrically** and not by dividing by twelve, so that twelve months of it
    run the engagement down by exactly the annual factor ``1 - w_p``: 6.00% a year is
    0.514301% a month.  That is what keeps :func:`mg`, :func:`cum_prem_net` and
    :func:`parts` — whose run-down is purely multiplicative — identical to the annual-step
    model at every anniversary.

    **Spreading is a decision, and it is the one that costs exact equivalence.**  The
    sourced basis is a rate on *average encours* [R13], a partial surrender is an owner
    election that can be made in any month, and A. 134-5 prices such an exit on the next
    intermediate value, which the monthly grid now strikes.  What it costs is that the
    exit cash leaves in twelve instalments rather than one, so more capital earns return
    early: on shipped point 5, the only cell with ``wd_factor > 0``, the anniversary
    ``own_assets`` run 0.21 to 3.05 EUR above the annual model's, at most 0.031%, and
    total *rachats* over fifteen years are 0.23% higher.  Gating it to the first month of
    the policy year at the full annual rate would restore bit-exactness and lose the
    realism; the technical notes record the choice.
    """
    return 1.0 - (1.0 - wd_rate(t)) ** (1.0 / 12.0)


def wd_gross_pp(t):
    """W(t): the amount a *rachat partiel* takes out of the provision, before the exit charge.

    Taken at the beginning of month t, so it is a fraction of the **opening** provisions,
    at the month's own rate :func:`wd_rate_mth`.
    """
    if t < proj_start():
        return 0.0
    return wd_rate_mth(t) * provision_value_at(t, "BOM")


def wd_pp(t):
    """The *rachat partiel* actually paid to the saver, net of the base 6° exit charge.

    An **owner election**, not a claim: the contract stays in force and the engagement
    continues on the reduced parts and the reduced guarantee.  It has its own cash flow
    column for that reason.
    """
    return wd_gross_pp(t) * (1.0 - exit_charge_rate())


def mg_at(t, timing):
    """mg at a point inside month t.

    ``"BOM"``
        the opening guaranteed amount: ``mg(t - 1)`` in every month but
        the first projected one, and in that one ``g`` times the initial
        net *versement* on a new-business cell or the extract's
        ``mg_ifo`` on an in-force one.  This is where the issue instant
        lives.

    ``"AFT_EXIT"``
        after a *rachat partiel* has run the guarantee down pro rata, at
        the month's own :func:`wd_rate_mth`.

    ``"AFT_PREM"``
        after a beginning-of-month scheduled *versement* has raised it by
        ``g P_net``.  This is the amount the month-end striking discounts.

    ``"AFT_TOP_UP"``
        after any free *versement* on the anniversary; the closing
        guaranteed amount, and the same number as :func:`mg`.
    """
    if timing == "BOM":
        if t > proj_start():
            return mg(t - 1)
        if duration_inforce() > 0:
            return mg_init()
        return guarantee_rate() * prem_init_after_charge()
    if timing == "AFT_EXIT":
        return mg_at(t, "BOM") * (1.0 - wd_rate_mth(t))
    if timing == "AFT_PREM":
        return mg_at(t, "AFT_EXIT") + guarantee_rate() * prem_after_charge_pp(t)
    if timing == "AFT_TOP_UP":
        return (mg_at(t, "AFT_PREM")
                + guarantee_rate() * premium_top_up_net_pp(t))
    raise ValueError("invalid timing: " + str(timing))


def mg(t):
    """mg(t): the amount guaranteed at the *échéance*, as at the end of month t.

    ``g`` times cumulative *versements* **net of the R. 134-3 1° entry charge**, run down
    pro rata to any *rachat partiel*.  It is constant between *versements* in a
    single-policy expected-value projection: full surrenders and deaths remove the policy
    rather than the guarantee, so they reach the cash flows through ``pols_if`` instead.
    """
    if t < proj_start():
        return 0.0
    return mg_at(t, "AFT_TOP_UP")


def cum_prem_net_at(t, timing):
    """The cumulative net *versements* at a point inside month t.

    ``"BOM"``
        the opening base: ``cum_prem_net(t - 1)`` in every month but the
        first projected one, and in that one the initial net *versement*
        on a new-business cell or the extract's ``cum_prem_net_ifo`` on
        an in-force one.
    """
    if timing == "BOM":
        if t > proj_start():
            return cum_prem_net(t - 1)
        if duration_inforce() > 0:
            return cum_prem_net_init()
        return prem_init_after_charge()
    raise ValueError("invalid timing: " + str(timing))


def cum_prem_net(t):
    """The cumulative net *versements* at the end of month t: the death-floor base.

    Equal to ``mg(t) / g`` here, and kept separate because they are different objects: the
    guaranteed amount is a contractual promise at a stated term and this is the base of a
    complementary death guarantee provisioned outside the account.  They coincide only
    because ``g`` is constant.
    """
    if t < proj_start():
        return 0.0
    return (cum_prem_net_at(t, "BOM") * (1.0 - wd_rate_mth(t))
            + prem_after_charge_pp(t) + premium_top_up_net_pp(t))


def parts_levy(t):
    """L(t): the R. 134-3 base 4° levy, taken in the **first month of the policy year**.

    ``f_p x prov_div_at(t, "BOM")`` in the months where ``duration_mth(t) % 12 == 0``, and
    nil in the other eleven — a levy **in number of parts**, valued at the opening part
    value.  It is a **contractual annual term** and not an assumption: ``product-spec.md``
    states it "0.80% p.a. of parts, taken at the start of each policy year on the opening
    part value", so it lands whole where the contract puts it.  Spreading it at
    ``(1 - f_p)^(1/12)`` would leave the parts count unchanged over a year but would
    change the **cash**, because the levy is valued on the then-current ``prov_div``.

    Base 3°, a levy on the *encours* of the diversification provision, is available only
    in an auxiliary account holding **no** 1° engagements, and no base permits a levy on
    the *provision mathématique* at all.  On the worked example's Chassis A the levy
    opening policy year 1 — month ``t`` = 0 — is 15.64; an encours levy on ``pm + pd``
    would have been 78.40.
    """
    if t < proj_start() or duration_mth(t) % 12 != 0:
        return 0.0
    return parts_charge_rate() * prov_div_at(t, "BOM")


def invest_income(t):
    """I(t): the **month's** financial performance, on the balance after its opening steps.

    ``own_assets_at(t, "AFT_PREM") x r_m(t)``.  Twelve of these compound the account up by
    exactly the policy year's annual return, and — where no cash moves inside the year —
    they **sum** to the annual model's ``A_a r``, which is what makes the anniversary
    performance levy reproduce it.
    """
    return own_assets_at(t, "AFT_PREM") * asset_return_mth(t)


def invest_income_ytd(t):
    """The financial performance accumulated since the policy year opened, through month t.

    ``I(t)`` in the first month of the policy year and ``I(t) + invest_income_ytd(t - 1)``
    in the other eleven, so it resets on every ``duration_mth(t) % 12 == 0``.  It exists
    because the R. 134-3 base 5° levy is struck **once a year** on the *compte de
    participation aux résultats*, so the levy needs the year's balance and not the month's.
    """
    if t < proj_start():
        return 0.0
    v = invest_income(t)
    if duration_mth(t) % 12 != 0:
        v += invest_income_ytd(t - 1)
    return v


def perf_levy(t):
    """F(t): the R. 134-3 base 5° levy on **positive** financial performance, on the anniversary.

    ``f_perf x max(invest_income_ytd(t), 0)`` where :func:`is_anniv`, and nil in the other
    eleven months.  It is an event of the **striking**, not of the month: R. 134-3 5° is a
    levy on the balance of the *compte de participation aux résultats*, R. 134-4 strikes
    that account at least annually, and R. 134-12 III fixes affectations to the striking
    dates.  A monthly levy would also be a different charge — it would tax a positive
    month inside a losing year, which the asymmetric ``max(., 0)`` exists not to do, and
    would have taken money in the worked example's policy year 6.

    Nothing at all in a year of negative performance, which is why the worked example's
    performance levy on the anniversary closing policy year 6, month ``t`` = 71, is zero on
    both chassis.  A policy exiting between anniversaries pays no performance levy for the
    part year, which is what the article's annual striking implies.
    """
    if t < proj_start() or not is_anniv(t):
        return 0.0
    return perf_charge_rate() * max(invest_income_ytd(t), 0.0)


def own_assets_at(t, timing):
    """The account assets at a point inside month t.

    ``"BOM"``
        the opening assets: ``A(t-1)`` in every month but the first
        projected one, and in that one the initial *versement* net of the
        entry charge on a new-business cell or ``own_assets_ifo`` on an
        in-force one.  This is where the issue instant lives — it is not a
        row of the frame.

    ``"AFT_LEVY"``
        less the base 4° parts levy, which falls only in the first month
        of a policy year.

    ``"AFT_EXIT"``
        less any *rachat partiel*, taken gross of the exit charge because
        the charge stays in the account.

    ``"AFT_PREM"``
        plus a beginning-of-month scheduled *versement* net of the entry
        charge.  **This is the balance the month's return accrues on.**

    ``"AFT_RETURN"``
        after the month's asset return, at :func:`asset_return_mth`.

    ``"AFT_PERF"``
        after the base 5° performance levy, which is nil except on the
        anniversary; the balance the two provisions are struck against.

    ``"AFT_TOP_UP"``
        plus any free *versement* on the anniversary; the closing assets,
        and the same number as :func:`own_assets`.

    The steps are exposed individually because their order is fixed by R. 134-4 and
    R. 134-12 III — asset affectations completing the representation are made on the dates
    the participation account is struck, after its balance has been allocated — rather
    than being arithmetic convenience.
    """
    if timing == "BOM":
        if t > proj_start():
            return own_assets(t - 1)
        if duration_inforce() > 0:
            return own_assets_init()
        return prem_init_after_charge()
    if timing == "AFT_LEVY":
        return own_assets_at(t, "BOM") - parts_levy(t)
    if timing == "AFT_EXIT":
        return own_assets_at(t, "AFT_LEVY") - wd_gross_pp(t)
    if timing == "AFT_PREM":
        return own_assets_at(t, "AFT_EXIT") + prem_after_charge_pp(t)
    if timing == "AFT_RETURN":
        return own_assets_at(t, "AFT_PREM") * (1.0 + asset_return_mth(t))
    if timing == "AFT_PERF":
        return own_assets_at(t, "AFT_RETURN") - perf_levy(t)
    if timing == "AFT_TOP_UP":
        return own_assets_at(t, "AFT_PERF") + premium_top_up_net_pp(t)
    raise ValueError("invalid timing: " + str(timing))


def own_assets(t):
    """A(t): the auxiliary-account assets attributable to the policy at the end of month t.

    At realisation value (R. 134-8) and **excluding** any outstanding L. 134-3
    contribution, which is the insurer's capital and not the savers' money.  That
    exclusion is the point of the cells: :func:`own_assets_at` rolls forward from ``A(t-1)``
    and never from ``pm(t-1) + prov_div(t-1)``, so the contribution earns nothing for the savers.
    In the worked example the policy-year-7 roll — month ``t`` = 72 — starts from
    10,250.65, not from the 12,384.73 the contract would have surrendered for.
    """
    if t < proj_start():
        return 0.0
    return own_assets_at(t, "AFT_TOP_UP")


def parts_at(t, timing):
    """The number of parts at a point inside month t.

    ``"BOM"``
        the opening count: ``N(t-1)`` in every month but the first
        projected one, and in that one the parts the initial net
        *versement* buys at ``part_value_init()`` on a new-business cell,
        or ``parts_ifo`` on an in-force one.

    ``"AFT_LEVY"``
        ``N_open(t)(1 - f_p)`` in the first month of a policy year, where
        the base 4° levy falls, and ``N_open(t)`` unchanged in the other
        eleven.  The levy cancels parts rather than reducing their value.

    ``"AFT_EXIT"``
        after a *rachat partiel* has cancelled its pro-rata share, at the
        month's own :func:`wd_rate_mth`.

    ``"AFT_PREM"``
        plus the parts a beginning-of-month *versement* bought.
        **This is the count the month-end striking divides by.**

    ``"AFT_TOP_UP"``
        plus the parts a free *versement* bought on the anniversary at the
        just struck part value; the closing count, and the same number as
        :func:`parts`.
    """
    if timing == "BOM":
        if t > proj_start():
            return parts(t - 1)
        if duration_inforce() > 0:
            return parts_init()
        u = part_value_init()
        return prov_div_at(t, "BOM") / u if u > 0.0 else 0.0
    if timing == "AFT_LEVY":
        if duration_mth(t) % 12 != 0:
            return parts_at(t, "BOM")
        return parts_at(t, "BOM") * (1.0 - parts_charge_rate())
    if timing == "AFT_EXIT":
        return parts_at(t, "AFT_LEVY") * (1.0 - wd_rate_mth(t))
    if timing == "AFT_PREM":
        return parts_at(t, "AFT_EXIT") + parts_added_bom(t)
    if timing == "AFT_TOP_UP":
        return parts_at(t, "AFT_PREM") + parts_added_top_up(t)
    raise ValueError("invalid timing: " + str(timing))


def parts(t):
    """N(t): the number of *parts de provision de diversification* at the end of month t.

    The saver's rights are expressed in a **number of parts**, and R. 134-2 makes the
    insurer's commitment the number and not the value.  On the worked example the count
    closes on ``212.8127 x 0.992^7 = 201.1774``: seven years of the base 4° levy and
    nothing else.
    """
    if t < proj_start():
        return 0.0
    return parts_at(t, "AFT_TOP_UP")


def pm_at(t, timing):
    """The *provision mathématique* inside month t: opening, and at the month-end striking.

    ``"BOM"``
        the opening PM: ``pm(t-1)`` in every month but the first projected
        one, and in that one the opening guaranteed amount discounted at
        the boundary-``t`` rate.  On an in-force cell this is the number
        :func:`check_pm_restruck` compares against the extract's ``pm_ifo``.

    ``"AFT_STRIKE"``
        the guaranteed amount as it stands after the month's opening
        steps, discounted at the rate of the month-end striking,
        ``i_pm(t + 1)``.  In eleven months of twelve this is A. 134-5's
        *valeur intermédiaire*; in the twelfth it is the striking of the
        participation account itself.

    ``"AFT_TOP_UP"``
        the same after any free *versement* on the anniversary; the closing
        PM, and the same number as :func:`pm`.

    Identically zero on Chassis B, where the guarantee is not provisioned inside the
    account at all.
    """
    if not is_euro_leg():
        return 0.0
    if timing == "BOM":
        if t > proj_start():
            return pm(t - 1)
        return mg_at(t, "BOM") * disc_factor(t)
    if timing == "AFT_STRIKE":
        return mg_at(t, "AFT_PREM") * disc_factor(t + 1)
    if timing == "AFT_TOP_UP":
        return mg_at(t, "AFT_TOP_UP") * disc_factor(t + 1)
    raise ValueError("invalid timing: " + str(timing))


def pm(t):
    """pm(t): the *provision mathématique* at the end of month t.

    ``mg(t) (1 + i_pm(t+1))^-rem_term(t+1)`` on Chassis A and identically zero on
    Chassis B (R. 134-2) — the closing guaranteed amount discounted from the *échéance*
    back to the month's end, boundary ``t + 1``, over a **fractional** number of years.
    **Re-struck every month, never accumulated.**  Rolling ``pm(t-1)`` forward at last
    year's rate removes the rate effect: in the worked example that is +587.44 of the
    +824.18 move over policy year 6, ``t`` = 59 to ``t`` = 71, against a time effect of
    +236.74.

    The monthly re-strike splits that move in two, which the annual grid could not: the PM
    accretes from 10,541.34 at ``t`` = 60 to 10,738.63 at ``t`` = 70 at the unchanged
    2.25% — the **time effect** — and jumps to 11,346.00 at ``t`` = 71, where the TEC is
    re-published at 1.00% — the **rate effect**, +607.37 in one month.

    In the last projected month the discount factor is 1, so ``pm`` equals ``mg``
    identically and the Chassis A guarantee is pre-funded by construction.
    """
    if t < proj_start() or not is_euro_leg():
        return 0.0
    return pm_at(t, "AFT_TOP_UP")


def prov_div_at(t, timing):
    """The *provision de diversification* inside month t: opening, and at the striking.

    The **residual** of the account's assets over the *provision mathématique*, floored at
    the parts' minimum value: R. 134-4 permits a debit balance to reduce the part value
    only within the limit of its minimum.  Where the floor binds the two provisions
    together exceed the assets, and the excess is exactly the L. 134-3 contribution.

    ``"BOM"`` is the opening provision — ``prov_div(t-1)`` in every month but the first
    projected one, and in that one the residual the initial *versement*, or the in-force
    extract, leaves over the opening PM.  It is the base of the parts levy in the months
    that carry one.
    """
    if timing == "BOM":
        if t > proj_start():
            return prov_div(t - 1)
        if duration_inforce() > 0:
            return max(own_assets_at(t, "BOM") - pm_at(t, "BOM"),
                       parts_init() * min_part_value())
        return max(own_assets_at(t, "BOM") - pm_at(t, "BOM"), 0.0)
    if timing == "AFT_STRIKE":
        return max(own_assets_at(t, "AFT_PERF") - pm_at(t, "AFT_STRIKE"),
                   parts_at(t, "AFT_PREM") * min_part_value())
    if timing == "AFT_TOP_UP":
        return max(own_assets_at(t, "AFT_TOP_UP") - pm_at(t, "AFT_TOP_UP"),
                   parts_at(t, "AFT_TOP_UP") * min_part_value())
    raise ValueError("invalid timing: " + str(timing))


def prov_div(t):
    """prov_div(t): the *provision de diversification* at the end of month t.

    The savers' individualised rights (R. 343-3 9°), and the only part of the engagement
    that bears investment risk.  On the worked example's policy-year-6 shock, at the
    anniversary month ``t`` = 71, the raw residual on Chassis A is
    ``10,250.65 - 11,346.00 = -1,095.35`` and the floor binds instead at
    ``207.7460 x 5.0000 = 1,038.73``.  The monthly grid shows where that starts: the floor
    **first binds in month 66**, not at the anniversary.
    """
    if t < proj_start():
        return 0.0
    return prov_div_at(t, "AFT_TOP_UP")


def part_value_at(t, timing):
    """The *valeur de la part* inside month t: opening, and at the month-end striking.

    ``"BOM"`` is the opening value — ``u(t-1)`` in every month but the first projected one,
    and in that one ``part_value_init()`` on a new-business cell (the initial *versement*
    buys parts at it) or the extract's ``pd / N`` on an in-force one.  It is what a
    beginning-of-month *versement* buys parts at.  ``"AFT_STRIKE"`` is what a free
    *versement* on the anniversary buys parts at.
    """
    if timing == "BOM":
        if t > proj_start():
            return part_value(t - 1)
        n_t = parts_at(t, "BOM")
        return prov_div_at(t, "BOM") / n_t if n_t > 0.0 else part_value_init()
    if timing == "AFT_STRIKE":
        n_t = parts_at(t, "AFT_PREM")
        return prov_div_at(t, "AFT_STRIKE") / n_t if n_t > 0.0 else 0.0
    if timing == "AFT_TOP_UP":
        n_t = parts_at(t, "AFT_TOP_UP")
        return prov_div_at(t, "AFT_TOP_UP") / n_t if n_t > 0.0 else 0.0
    raise ValueError("invalid timing: " + str(timing))


def part_value(t):
    """u(t): the *valeur de la part* at the end of month t, ``prov_div(t) / N(t)``.

    Struck **every month**: in the eleven months of a policy year in which the
    participation account is not struck this is the *valeur intermédiaire* A. 134-5
    requires, and it is what an exit falling in the month is priced on.

    **Common to every engagement of the auxiliary account** (R. 134-2), so savers with
    different maturities and different guarantee levels in one account earn the same rate;
    differentiation is possible only through the number of parts or through a
    differentiated PCDD distribution.  A per-policy model can only approximate that — the
    shipped model points are separate accounts, and their part values diverge as separate
    accounts' would.
    """
    if t < proj_start():
        return 0.0
    return part_value_at(t, "AFT_TOP_UP")


def provision_value(t):
    """``pm(t) + prov_div(t)``: the base of the R. 134-5 and R. 134-6 values.

    One expression on both chassis, because ``pm`` is identically zero on Chassis B.  It
    equals ``pm(t) + N(t) u(t)``, which is how the articles write it.
    """
    return pm(t) + prov_div(t)


def provision_value_at(t, timing):
    """``pm + prov_div`` at a point inside month t.

    ``"BOM"``
        the opening provisions — the base a beginning-of-month *rachat
        partiel* takes its pro-rata share of.
    """
    if timing == "BOM":
        return pm_at(t, "BOM") + prov_div_at(t, "BOM")
    raise ValueError("invalid timing: " + str(timing))


def insurer_contribution(t):
    """C(t): the outstanding L. 134-3 contribution completing the representation.

    ``max(pm(t) + prov_div(t) - A(t), 0)``, and nil on Chassis B, where the shortfall against the
    guarantee is carried as a PGT instead.  It is the insurer's capital: it carries **no
    return to the savers** and is releasable as soon as the account's own assets cover the
    two provisions.  The surrender value exceeds the account's own assets by exactly this
    amount while it is outstanding — 2,134.08 at the anniversary month ``t`` = 71 of the
    worked example's policy-year-6 shock.

    Struck monthly, which is where the finer grid earns its keep on this cell: the
    contribution **starts at 141.96 in month 66**, the month the part-value floor first
    binds, and climbs to 2,134.08 by the anniversary.  The annual grid could only report
    the anniversary figure.
    """
    if not is_euro_leg():
        return 0.0
    return max(provision_value(t) - own_assets(t), 0.0)


def apport(t):
    """The R. 134-12 *apport d'actifs*, made on the **anniversary** of a stated policy year.

    Capped at 10% of the diversification provision by the article.  It enters the account
    at realisation value and **endows the PCDD**; it is never credited to ``prov_div``, so it
    changes no policyholder value by one cent.  ``apport_t`` is the contractual **policy
    year** at whose end it falls, so the test is ``is_anniv(t) and policy_year(t) ==
    apport_year()`` — the single month ``t = 12 x apport_year() - 1``; zero is the "no
    *apport*" sentinel and matches no month.  It stays on the anniversary because
    R. 134-12 III fixes asset affectations to the dates the participation account is
    struck.  On the worked example's Chassis B a statutory-maximum *apport* on the
    anniversary closing policy year 6 — month ``t`` = 71 — is 989.92 and cuts the PGT from
    1,446.78 to 456.86.
    """
    if (t < proj_start()
            or not (is_anniv(t) and policy_year(t) == apport_year())):
        return 0.0
    return min(apport_rate(), apport_cap) * prov_div(t)                    # noqa: F821


def pcdd(t):
    """D(t): the *provision collective de diversification différée* (R. 343-3 10°).

    Collective, with no individual rights, and released into the participation account
    within fifteen years (A. 132-16) — against eight for a euro fund's *provision pour
    participation aux bénéfices*.  This model accumulates the *apport d'actifs* into it and
    nothing else: the *mémoire*'s piloting rule, which runs the fund at 30 bp above the
    insurer's own euro fund and carries the rest here, is a fund-level discretion a
    single-policy model cannot express, and holding it at zero **understates the smoothing
    the real product delivers**.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        return apport(t)
    return pcdd(t - 1) + apport(t)


def pgt(t):
    """G(t): the *provision pour garantie à terme* (A. 134-2, R. 343-3 11°).

    ``max(mg(t) (1 + i_pm(t+1))^-rem_term(t+1) - prov_div(t) - D(t), 0)`` on Chassis B and
    nil on Chassis A, struck at the end of every month.
    Funded from the **insurer's own funds** and held **outside** the participation account,
    on a deliberately narrow basis: the A. 132-18 mortality tables at a rate at most 90% of
    the TEC, counting **no cash flows other than guarantee maturities and mortality**.  A
    model must not "improve" that basis by adding lapses or expenses to it, and must not
    let the provision reach a benefit or feed the profit-sharing computation.

    **Mortality, one of the article's two admitted drivers, is not implemented [std].**  The
    present value above applies no survival factor, so it is the amount for a guarantee
    certain to be reached: prudent, since it overstates the provision, and invisible on the
    worked example, where ``mort_rate`` is zero.  It is live on the decrement-bearing cells —
    on model point 6 at the anniversary closing policy year 7, month ``t`` = 83, this
    returns 2,739.35
    against 2,477.36 with the five-year
    survival factor 0.972660 the shipped table gives.  In a single-policy model the decrement
    reaches the projection through ``pols_if`` in :func:`result_cf` instead; a fund-level
    implementation should carry the survival factor inside the present value, summed over the
    account's 2° engagements.

    On the worked example's Chassis B the monthly striking shows the provision being
    constituted: the PGT **first becomes positive in month 68**, at 61.48, and reaches
    1,446.78 by the anniversary at month 71.
    """
    if is_euro_leg():
        return 0.0
    return max(mg(t) * disc_factor(t + 1) - prov_div(t) - pcdd(t), 0.0)


def gate_revalue_ok(t):
    """Whether both A. 134-3 tests permit revaluing the guarantees out of the account.

    Test 1: the diversification provision exceeds 1.5 times the excess of the guaranteed
    amounts over the *provision mathématique*.  Test 2: the diversification provision less
    the parts at their minimum value exceeds 10% of the *provision mathématique*.  **Both**
    must pass.  Informational here — the reference credit-balance route raises the part
    value instead — but computed, because a model that revalued guarantees without testing
    the gates would be exercising a discretion the article does not allow.  Evaluated on
    the **month's own** striking, so it is answered every month rather than once a year.
    On the worked example both pass at ``t`` = 59, the anniversary closing policy year 5,
    and the second fails at ``t`` = 71, where the part-value floor has taken the headroom
    to nil.
    """
    if not is_euro_leg():
        return False
    t1 = prov_div(t) > revalue_gate1_factor * max(mg(t) - pm(t), 0.0)      # noqa: F821
    t2 = (prov_div(t) - parts(t) * min_part_value()
          > revalue_gate2_factor * pm(t))                            # noqa: F821
    return bool(t1 and t2)


def conversion_headroom(t):
    """The parts convertible into *provision mathématique* under A. 134-4.

    The article requires the diversification provision, net of the conversion and of the
    parts at their minimum value, to remain at least 15% of the resulting PM, and imposes
    a five-year cooling period besides.  Solving ``pd - C - N u_min = 0.15 (pm + C)`` gives
    ``C = (pd - N u_min - 0.15 pm) / 1.15`` — 474.52 on the worked example at ``t`` = 59.
    Computed, never exercised: the conversion is out of scope, and the 0.50% *frais de
    conversion* the market shows would take 2.37 of that.
    """
    if not is_euro_leg():
        return 0.0
    room = (prov_div(t) - parts(t) * min_part_value()
            - conv_headroom_rate * pm(t))                            # noqa: F821
    return max(room / (1.0 + conv_headroom_rate), 0.0)               # noqa: F821


def surrender_indemnity(t):
    """The R. 132-5-3 *indemnité de rachat* applying to a full surrender in month t.

    The article caps the indemnity at 5% of the present value of the mutual engagements
    (20% or 10% in narrow unlisted-asset cases) and **permits** the contract to provide for
    no indemnity at all once it has been in force more than ten years.  That is a
    permission, not a prohibition: the article does not forbid an indemnity beyond ten
    years.  The reference contract charges none at any duration, and this model returns zero
    once ``indemnity_max_years`` policy years have elapsed — from ``duration(t) =
    indemnity_max_years`` on, the eleventh policy year, month ``t = 120`` on a longer
    term — unconditionally, which is the permission taken up **[std]** rather than the
    article applied.  The test is on the completed policy **years**, because that is the
    unit R. 132-5-3 states.
    """
    if duration(t) >= indemnity_max_years:                           # noqa: F821
        return 0.0
    return min(surrender_indemnity_rate(), indemnity_cap)            # noqa: F821


def surrender_value(t):
    """The R. 134-5 *valeur de rachat* at the end of month t.

    ``pm(t) + N(t) u(t)`` on Chassis A and ``N(t) u(t)`` on Chassis B, less the base 6°
    exit charge and any surrender indemnity.

    **There is no guarantee in it before the *échéance*.**  On the worked example's
    policy-year-6 shock, at the anniversary month ``t`` = 71,
    Chassis A surrenders for 12,384.73 — 105.31% of net *versements*, because its
    *provision mathématique* has already been marked up by the fall in rates — while
    Chassis B surrenders for 9,899.22, **84.18%**, against a guarantee of 11,760.00 that
    does not apply.  A model that floors this at ``g`` times premiums, or at the discounted
    guarantee, is modelling a contract that does not exist.

    A surrender is priced on the **forward** part value A. 134-5 requires — the striking
    of the month in which the request falls, which is the next striking or intermediate
    value after it.  The monthly grid delivers that rather than standardizing it away: a
    Chassis B saver surrendering in month 65 receives **11,430.63**, not the 9,899.22 the
    anniversary striking at month 71 reports.
    """
    return (provision_value(t) * (1.0 - exit_charge_rate())
            * (1.0 - surrender_indemnity(t)))


def death_value(t):
    """The current provision value, which is what a death before the *échéance* pays.

    Chapter IV contains **no death valuation article**, so the death benefit is the value
    of the engagement and the maturity guarantee does not apply.  No exit charge: the base
    6° charge is on amounts the saver elects to take out.
    """
    return provision_value(t)


def death_payout(t):
    """The death benefit actually paid, after any *garantie décès plancher*.

    ``max(death_value(t), cum_prem_net(t))`` where the model point carries the rider.  The
    floor is a **complementary guarantee provisioned outside the auxiliary account**
    (R. 134-7), not the maturity guarantee arriving early: it happens to equal ``mg`` here
    only because ``g`` is 100%, and at ``g`` = 80% the two would differ.
    """
    if death_floor_flag():
        return max(death_value(t), cum_prem_net(t))
    return death_value(t)


def rider_claim_pp(t):
    """The part of the death benefit the *garantie décès plancher* funds, per claim.

    ``death_payout(t) - death_value(t)`` — 1,860.78 on the worked example's policy-year-6
    Chassis B death, month ``t`` = 71.  Reported apart from the auxiliary-account columns
    because it is not the account's money: R. 134-7 puts complementary guarantees outside it.
    """
    return death_payout(t) - death_value(t)


def maturity_value(t):
    """The R. 134-6 amount payable at the *échéance*; nil at every other t.

    The *échéance* is the end of the **last projected month**, ``t = proj_len() - 1``, and
    it really is one month rather than a policy year — which is why this test stays on the
    month while the *rachat* exclusions in :func:`lapse_rate` and :func:`wd_rate` moved to
    the policy year.
    ``pm + N u`` there on Chassis A — **more** than the guarantee whenever the parts
    retain any value, 12,765.89 against 11,760.00 in the worked example — and
    ``max(N u, mg)`` on Chassis B.  The ``max`` exists **only in that last month** and
    **only on Chassis B**; applying it earlier, or on Chassis A at all, invents a guarantee
    the contract does not give.

    The statutory default at the *échéance* is in fact an arbitrage into an SRI <= 2
    support unless the holder decides otherwise (A. 134-6); this model pays the amount out
    and stops, and a "roll into a low-risk support" variant is the natural extension.
    """
    if t != proj_len() - 1:
        return 0.0
    if is_euro_leg():
        return provision_value(t)
    return max(provision_value(t), mg(t))


def claim_pp(t, kind):
    """The payout per claim in month t, by kind.

    ``"DEATH"``
        :func:`death_payout` — the current provision value, floored at
        cumulative net *versements* where the rider is carried.

    ``"LAPSE"``
        :func:`surrender_value` — the R. 134-5 value, with **no**
        guarantee before the *échéance*.

    ``"MATURITY"``
        :func:`maturity_value` in the last projected month and nil
        elsewhere.
    """
    if kind == "DEATH":
        return death_payout(t)
    if kind == "LAPSE":
        return surrender_value(t)
    if kind == "MATURITY":
        return maturity_value(t)
    raise ValueError("invalid kind: " + str(kind))


def mort_rate(t):
    """q(x + dur(t) + 1): the **annual** mortality rate of the policy year of month t **[std]**.

    The rate the technical notes tabulate; :func:`mort_rate_mth` is the rate actually
    applied in the month.  Read at :func:`age_anniv`, the *âge atteint* at the **end** of
    the policy year, which is the notes' own ``q(x + t + 1)`` restated on the monthly
    grid: the age rule belongs to the annual assumption, and the finer grid changes only
    where within the year the decrement falls.  The shipped table rate times
    ``mort_be_factor``.  Both are
    placeholders: the
    homologated tables TH 00-02 / TF 00-02 are cited by arrêté and never shipped, A. 132-18
    permits an insurer's own certified table besides, and the proxy is INSEE-shaped
    population mortality with a factor for insured lives being lighter than the population.
    Nil where the model point switches the decrements off, which is the worked example's
    configuration.
    """
    if decrement_basis() == "none" or t < proj_start():
        return 0.0
    x = min(age_anniv(t), omega_age)                                 # noqa: F821
    return min(1.0, float(data.mort_table().loc[                     # noqa: F821
        (sex(), x), "mort_rate"]) * mort_be_factor)                  # noqa: F821


def mort_rate_mth(t):
    """q_m = ``1 - (1 - q)^(1/12)``: the monthly mortality rate applied in month t **[std]**.

    Derived **geometrically** and not by dividing by twelve, which is what makes
    ``(1 - q_m)^12 = 1 - q`` hold exactly - so twelve months of it leave the in-force at
    the anniversary identical to the annual-step model's.  On shipped point 6 the annual
    0.00243005 becomes 0.00020273 a month, and twelve of those compound back to
    0.00243005.

    The conversion carries **[std]** because no retrieved French source states a
    conversion convention for any decrement.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The table annual full-surrender (*rachat total*) rate of the policy year of month t **[std]**.

    2.5% p.a. level; the *mémoire* observes 2%-3%.  ``lapse_table.csv`` is keyed by the
    contractual **policy year**, read here at ``policy_year(t)``; policy years beyond the
    table take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def guarantee_imminent(t):
    """0.5 in the two policy years before the *échéance* on Chassis B, while the guarantee bites.

    The policy year of month t is ``policy_year(t)``, so the years still to run at its
    close are ``n - policy_year(t)`` and the suppression applies over **every month** of a
    policy year where that is at most ``guarantee_imminent_years``.  On shipped point 6
    that is months 108 to 143.

    The in-the-money test is read on the **current month's** striking rather than on the
    anniversary's, because the behavioural statement is that a saver deciding to surrender
    looks at whether ``N u < mg`` now.  It is a faithful reading rather than a free one:
    on every shipped model point the two readings agree in every month, the gate's state
    being slow-moving relative to a month.

    The gate matters.  A saver who surrenders a 2° engagement gives up the **entire**
    guarantee (R. 134-5), so the deterrent exists precisely while ``N u < mg`` and is worth
    nothing otherwise; applying it unconditionally would invent behaviour where there is
    none.  This is the strongest exit deterrent the product creates, and it is **[std]** —
    no eurocroissance lapse experience is public.
    """
    if (is_euro_leg()
            or policy_term() - policy_year(t) > guarantee_imminent_years):  # noqa: F821
        return 1.0
    if parts(t) * part_value(t) < mg(t):
        return guarantee_imminent_factor                             # noqa: F821
    return 1.0


def duration8_spike(t):
    """1.5 over policy year 8 — every month with ``policy_year(t) == 8`` — where ``n > 8`` **[std]**.

    The assurance-vie annual *abattement* becomes available at eight years, so surrender
    incentive spikes there — and only where the contract still has years to run, since a
    contract maturing at eight has no such choice to make.  It is a multiplier on the
    **annual** rate, applied before the monthly conversion, so it grades once a year as
    the behaviour it stands for does and not once a month.
    """
    if (policy_year(t) == duration8_year                             # noqa: F821
            and policy_term() > duration8_year):                     # noqa: F821
        return duration8_factor                                      # noqa: F821
    return 1.0


def lapse_rate(t):
    """w(t): the **annual** full-surrender rate of the policy year containing month t.

    The rate the technical notes tabulate — the table rate times both behavioural
    overlays, capped at 1; :func:`lapse_rate_mth` is the rate actually applied at the end
    of the month.  Nil while the decrements are switched off, inside a non-surrender
    period — policy years 1 to ``lock_up_years``, so ``duration(t) < lock_up_years()`` —
    and over **the whole of the last policy year**, which ends at the *échéance*, where the
    survivors take the maturity amount instead — the base run assumes 100% of them do,
    as the *mémoire* also assumes.

    That last exclusion is ``duration(t) >= policy_term() - 1`` and **not** the last month.
    The annual grid never let a survivor lapse out of the *échéance* year; restating the
    test as ``t >= proj_len() - 1`` would open eleven months of it and move the whole
    maturity claim, which is the single most likely place for the conversion to introduce
    a silent error.
    """
    if decrement_basis() == "none":
        return 0.0
    if (t < proj_start() or duration(t) < lock_up_years()
            or duration(t) >= policy_term() - 1):
        return 0.0
    return min(1.0, lapse_rate_base(t) * guarantee_imminent(t)
               * duration8_spike(t))


def lapse_rate_mth(t):
    """w_m = ``1 - (1 - w)^(1/12)``: the full-surrender rate applied at the end of month t **[std]**.

    Derived **geometrically** from the policy year's annual rate, so ``(1 - w_m)^12 =
    1 - w`` exactly and the in-force at every anniversary is the annual-step model's.  The
    same conversion :func:`mort_rate_mth` takes, and **[std]** for the same reason: no
    retrieved French source states one.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement — and the exposure
        every cash flow of the month is weighted by; :func:`pols_if`.

    ``"BEF_LAPSE"``
        after deaths, before surrenders: the processing order is death
        before surrender **[std]**.

    ``"AFT_DECR"``
        the notes' ``l(t)``: the end-of-month count, and zero in the last
        projected month, where the survivors mature.  This is the timing
        the end-of-month quantity is reached through, because the bare
        name ``pols_if`` belongs to the start-of-month count.

    Both decrements are applied at their **monthly** rates, so a death or a surrender
    falls in the month it happens rather than at the anniversary — and twelve months of
    them compound back to exactly the policy year's annual factors, which is why
    ``pols_if(12k)`` is what the annual-step model carried for policy year ``k + 1``.
    """
    if timing == "BEF_DECR":
        if t < proj_start():
            return 0.0
        if t == proj_start():
            return pols_if_init()
        return pols_if_at(t - 1, "AFT_DECR")
    if timing == "BEF_LAPSE":
        return pols_if_at(t, "BEF_DECR") * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        if t >= proj_len() - 1:
            return 0.0
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing: " + str(timing))


def pols_if(t):
    """The number of policies in force at the **start** of month t.

    This is the library's shared vocabulary: ``pols_if(t)`` is the exposure at the start of
    month t and the weight on that same :func:`result_cf` row's cash flows, so the opening
    row is ``pols_if_init()`` exactly — no decrement has been applied when a month opens.

    ``pols_if(12k)`` is the count the annual-step model this one replaced carried on its
    row for policy year ``k + 1``, to floating point, because the monthly decrements
    compound back to the annual ones.

    The notes' ``l(t)`` is the **end**-of-month count, nil on the last projected row
    because everyone has matured by the end of it.  That quantity is
    unchanged and is reached as ``pols_if_at(t, "AFT_DECR")``; it is no longer published
    under this name, because doing so put the exposure column one period ahead of the flows
    printed beside it.
    """
    if t < proj_start() or t >= proj_len():
        return 0.0
    return pols_if_at(t, "BEF_DECR")


def pols_death(t):
    """Deaths in month t, against the start-of-month in force, at ``mort_rate_mth``."""
    if t < proj_start():
        return 0.0
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_lapse(t):
    """Full surrenders at the end of month t, from the survivors of that month's mortality."""
    if t < proj_start():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_maturity(t):
    """Survivors reaching the *échéance*; nil outside the last projected month.

    The base run assumes 100% of them take the maturity amount **[std]**, as the *mémoire*
    also assumes; it notes that modelling annuitisation or reinvestment instead could
    amplify or damp its results.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_if_at(t, "BEF_LAPSE")


def premiums(t):
    """*Versement* income in month t, an inflow.

    The initial *versement* where the month is the first projected one, a scheduled
    *versement* in a month that opens a policy year and a free one on an anniversary,
    gross of the
    entry charge — the charge is reported as insurer income in :func:`charges_taken`
    rather than netted out of the premium line.
    """
    return total_premium_pp(t) * pols_if_at(t, "BEF_DECR")


def withdrawals(t):
    """*Rachats partiels* paid at the beginning of month t.

    An **owner election** rather than a claim, which is why it has its own name and column:
    the contract stays in force and continues on the reduced parts and reduced guarantee.
    """
    return wd_pp(t) * pols_if_at(t, "BEF_DECR")


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    Deaths and surrenders are now settled in the **month they happen**, priced on that
    month's own striking, rather than at the anniversary — which is what the finer grid
    was for, and why the claim columns do not reproduce the annual-step model.

    ``"DEATH"``, ``"LAPSE"`` and ``"MATURITY"`` weight :func:`claim_pp` by the
    corresponding decrement.  The death line **includes** the *garantie décès plancher*'s
    contribution, which :func:`rider_claims` reports separately; it is a decomposition of
    this column and not a fourth kind.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "MATURITY"))
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    if kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    if kind == "MATURITY":
        return claim_pp(t, "MATURITY") * pols_maturity(t)
    raise ValueError("invalid kind: " + str(kind))


def rider_claims(t):
    """The *garantie décès plancher*'s share of the month's death outgo.

    A memo line: it is **already inside** ``claims_death``, and it is published apart
    because R. 134-7 puts complementary guarantees outside the auxiliary account, so it is
    not paid out of the savers' provisions.
    """
    return rider_claim_pp(t) * pols_death(t)


def expenses(t):
    """E(t): the insurer's own expenses in month t **[std]**.

    Acquisition at 5% of *versements* plus an acquisition commission of 2% of the initial
    one, and maintenance at 0.20% p.a. of the two provisions.  All three levels come from
    the published *mémoire*, which is the only complete public parameterisation of this
    product.  They are the insurer's costs, not charges to the saver: the charges the
    contract permits are the six R. 134-3 bases, reported in :func:`charges_taken`.

    The acquisition components fall in the month their *versement* does and are weighted
    by the start-of-month exposure like every other flow.  **Maintenance accrues at one
    twelfth a month**, ``0.20% / 12`` of the month's own striking of the two provisions,
    weighted by the count on the books at it, ``pols_if_at(t, "AFT_DECR")``.

    This is the one place the conversion changes an answer rather than its resolution, and
    it changes it in two ways.  Twelve monthly accruals cover exactly the year the annual
    grid charged for once at its year end, so the extra opening-striking charge the annual
    model needed — ``n + 1`` point-in-time charges to cover ``n`` years of service — is
    **gone**; and the charge is now borne by the in-force and the provision of each month
    rather than of the anniversary, so a decrementing block carries less of it and a block
    whose provision grows through the year carries less again.  Over a whole projection
    that is -0.2% to -1.3% on the shipped cells, and +0.9% on point 9, whose five annual
    *versements* step the provision up in the first month of each of its first five policy
    years.
    """
    acq = expense_acq_rate * total_premium_pp(t)                     # noqa: F821
    if t == proj_start() and duration_inforce() == 0:
        acq += expense_comm_rate * premium_gross_init()              # noqa: F821
    maint = (expense_maint_rate / 12.0 * provision_value(t)          # noqa: F821
             * pols_if_at(t, "AFT_DECR"))
    return acq * pols_if_at(t, "BEF_DECR") + maint


def charges_taken(t):
    """The R. 134-3 charges the insurer takes in month t: income, reported apart.

    The base 4° parts levy, the base 5° performance levy, the base 1° entry charge and the
    base 6° exit charge together with any surrender indemnity.  They are **not** in
    ``net_cf``: they are transfers inside the account from the savers' provisions to the
    insurer, and the benefits they reduce are already net of them.  Publishing them beside
    the flows is what makes the charge structure auditable against R. 134-3.
    """
    inside = (parts_levy(t) + perf_levy(t) + entry_charge(t)
              + (wd_gross_pp(t) - wd_pp(t)))
    on_surr = (provision_value(t) - surrender_value(t)) * pols_lapse(t)
    return inside * pols_if_at(t, "BEF_DECR") + on_surr


def liability_cf(t):
    """CF(t): the month's liability cash flow, **outgo positive**, as the notes print it.

    Claims and *rachats partiels* and expenses out, *versements* in.  The two provisions
    appear nowhere in it — they are state variables, not cash flows — and neither do the
    insurer's own-funds items, which are capital rather than benefit.
    """
    return (claims(t) + withdrawals(t) + expenses(t) - premiums(t))


def net_cf(t):
    """The net cash flow of month t, **income positive**: ``-liability_cf(t)``.

    The library's sign convention, so that ``result_cf()["net_cf"]`` can be compared and
    summed across products without checking which one it came from.
    """
    return -liability_cf(t)


def check_assets_roll_fwd_resid(t):
    """The account-asset recursion residual in month t; zero everywhere.

    ``A(t) - {[A_open(t) - L(t) - W(t) + P_net(t)](1 + r_m) - F(t) + top-up}``, rebuilt in
    **one expression** rather than through :func:`own_assets_at`, so that a mis-ordered
    step shows up here: a parts levy taken after the return instead of before it, a
    *versement* credited after the return rather than at the beginning of the month, or a
    performance levy struck on the wrong balance.  The opening quantities are the ``"BOM"``
    timings, so the check is live in the first projected month too, where they carry the
    initial *versement* or the in-force extract.

    Two of the three charges now enter by **name** rather than being rebuilt from their
    rates, and that is the conversion showing through: the base 4° levy falls only in the
    first month of a policy year and the base 5° levy only on the anniversary, on the
    year's accumulated performance, so neither can be reconstructed from a month's own
    balance.  What the check still rebuilds independently is the order and the base, and
    the companion identity ``invest_income(t) == base x asset_return_mth(t)`` — asserted
    in ``tests/test_eurocroissance_fr.py`` — pins the balance the return accrues on.
    """
    if t < proj_start():
        return 0.0
    base = (own_assets_at(t, "BOM")
            - parts_levy(t)
            - wd_rate_mth(t) * provision_value_at(t, "BOM")
            + prem_after_charge_pp(t))
    built = (base * (1.0 + asset_return_mth(t))
             - perf_levy(t)
             + premium_top_up_net_pp(t))
    return own_assets(t) - built


def check_assets_roll_fwd():
    """True when the account-asset recursion closes in every projected month."""
    return all(abs(check_assets_roll_fwd_resid(t)) <= roll_fwd_tol   # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_parts_roll_fwd_resid(t):
    """The parts recursion residual in month t; zero everywhere.

    ``N(t) - {N_open(t)(1 - f_p 1{BOM of a policy year})(1 - w_pm) + parts bought at BOM
    + parts bought at the top-up}``, rebuilt in one expression.  The base 4° levy cancels
    parts rather than reducing their value, so a levy applied to the part value instead of
    to the count would leave the count unchanged and show up here; so would a *versement*
    priced at the wrong striking, or a levy taken in a month that carries none.  On the
    worked example the count closes on ``212.8127 x 0.992^7 = 201.1774``.
    """
    if t < proj_start():
        return 0.0
    levy = ((1.0 - parts_charge_rate()) if duration_mth(t) % 12 == 0 else 1.0)
    built = (parts_at(t, "BOM") * levy * (1.0 - wd_rate_mth(t))
             + parts_added_bom(t) + parts_added_top_up(t))
    return parts(t) - built


def check_parts_roll_fwd():
    """True when the parts recursion closes in every projected month."""
    return all(abs(check_parts_roll_fwd_resid(t)) <= roll_fwd_tol    # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_guarantee_roll_fwd_resid(t):
    """The guaranteed-amount recursion residual in month t; zero everywhere.

    ``mg(t) - {mg_open(t)(1 - w_pm) + g x net versements of the month}``, rebuilt in
    one expression.  It is the check that catches the guarantee being computed on **gross**
    *versements*: with a 2.00% entry charge, ``mg`` after the worked example's top-up on
    the anniversary closing policy year 3 is 11,760.00 and not 12,000.00, and a model that
    used the gross figure would fail here in the month the top-up is paid rather than
    silently over-guaranteeing for seven years.
    """
    if t < proj_start():
        return 0.0
    built = (mg_at(t, "BOM") * (1.0 - wd_rate_mth(t))
             + guarantee_rate() * (prem_after_charge_pp(t) + premium_top_up_net_pp(t)))
    return mg(t) - built


def check_guarantee_roll_fwd():
    """True when the guaranteed-amount recursion closes in every projected month."""
    return all(abs(check_guarantee_roll_fwd_resid(t)) <= roll_fwd_tol  # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    The month opens at ``pols_if(t)`` and closes at ``pols_if_at(t, "AFT_DECR")``, the
    notes' ``l(t)``; the difference is the month's deaths, full surrenders and maturities.
    """
    if t < proj_start():
        return 0.0
    return (pols_if(t) - pols_if_at(t, "AFT_DECR") - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month."""
    return all(abs(check_pols_roll_fwd_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_guarantee_funding_resid(t):
    """``pm(t)`` accumulated to the *échéance* less the guaranteed amount; zero on Chassis A.

    This is the model's headline identity: the *provision mathématique* accumulated at the
    regulated rate reaches the guarantee **exactly** at the *échéance*, so
    ``pm(t)(1 + i_pm(t+1))^rem_term(t+1) = mg(t)`` at every t — month t closes at boundary
    ``t + 1``, which is ``(T - t - 1)/12`` **years** short of the *échéance* — and the two
    coincide in the last projected month.  On the monthly grid it holds month by month and
    not only at anniversaries, which is one of the reasons the PM is re-struck at a
    fractional remaining term rather than held flat between strikings.

    It is zero by construction under R. 134-2's re-strike rule, and that is the point of
    publishing it: an implementation that **accumulates** the PM instead — rolling
    ``pm(t-1)`` forward at last year's rate — breaks it the first year the rate moves.  On
    the worked example's path ``pm(59) x 1.0225 = 10,758.56`` against the 11,346.00 the
    re-strike gives, and the 587.44 difference is the rate effect it has silently dropped.

    Identically zero on Chassis B, where **both sides are nil**: a 2° engagement funds
    nothing inside the account against its guarantee, which is exactly why an early
    *rachat* there can pay less than the guaranteed amount.  The Chassis B funding
    statement is :func:`check_pgt_covers_guarantee` instead.
    """
    if not is_euro_leg():
        return 0.0
    return pm(t) * (1.0 + i_pm(t + 1)) ** rem_term(t + 1) - mg(t)


def check_guarantee_funding():
    """True when the *provision mathématique* funds the guarantee exactly, at every t."""
    return all(abs(check_guarantee_funding_resid(t)) <= funding_tol  # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_pgt_covers_guarantee_resid(t):
    """``pd + G + D`` less the discounted guarantee on Chassis B; non-negative in every month.

    A. 134-2 makes the PGT the shortfall of the diversification provision and the PCDD
    against the discounted guarantees, floored at zero, so the three together always cover
    it — exactly where the PGT is positive and with a surplus where it is not.  It is the
    Chassis B counterpart of :func:`check_guarantee_funding`, and what it asserts is that
    the guarantee is funded **somewhere**: on the savers' side before a shock, and out of
    the insurer's own funds after one.

    Identically zero on Chassis A, which constitutes no PGT: there the L. 134-3
    contribution plays the analogous role and :func:`insurer_contribution` carries it.
    """
    if is_euro_leg():
        return 0.0
    return prov_div(t) + pgt(t) + pcdd(t) - mg(t) * disc_factor(t + 1)


def check_pgt_covers_guarantee():
    """True when the diversification provision and the own-funds provisions cover the guarantee."""
    return all(check_pgt_covers_guarantee_resid(t) >= -funding_tol   # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_part_value_floor_resid(t):
    """``u(t) - u_min``: how far the part value sits above its contractual floor.

    Non-negative everywhere.  R. 134-4 permits a debit balance on the participation account
    to reduce the part value only **within the limit of its minimum**, and an implementation
    that omits the floor takes the worked example's Chassis A diversification provision to
    **-1,095.35** at the anniversary of policy year 6, ``t`` = 71 — a negative provision,
    and with it a
    negative surrender value that every downstream number stays plausible enough to read
    past.
    """
    return part_value(t) - min_part_value()


def check_part_value_floor():
    """True when the part value stays at or above its contractual minimum, every month."""
    return all(check_part_value_floor_resid(t) >= -floor_tol         # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_own_funds_not_paid_resid(t):
    """The excess of the month's largest benefit over the two provisions; non-positive.

    Before the *échéance* every benefit is bounded by ``pm(t) + prov_div(t)``: the surrender value
    is that less charges and the death value is exactly it, the *garantie décès plancher*
    being funded outside the account and excluded here.  Neither the L. 134-3 contribution
    nor the PGT may reach a policyholder, and on the shipped Chassis B cells the PGT is
    positive for four consecutive years, so the check is live rather than decorative: an
    implementation that floored the Chassis B surrender value at the guarantee would pay
    11,760.00 against a bound of 9,899.22 and fail here.

    The residual is zero in the **last projected month**, the one that ends at the
    *échéance*, and that is not a gap.  The maturity guarantee on
    Chassis B legitimately exceeds the account's provisions, and paying it out of the PGT
    is precisely what the PGT was constituted for.
    """
    if t >= proj_len() - 1:
        return 0.0
    return max(surrender_value(t), death_value(t)) - provision_value(t)


def check_own_funds_not_paid():
    """True when no benefit before the *échéance* exceeds the savers' two provisions."""
    return all(check_own_funds_not_paid_resid(t) <= funding_tol      # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_pm_restruck_resid(t):
    """The in-force extract's *provision mathématique* against the re-strike; zero.

    R. 134-2 makes the PM the guaranteed amount discounted at the **current** A. 134-1 rate,
    so an extract cannot supply it independently: this compares what the extract reports
    against what the rule requires, at the valuation date.

    Zero by construction on a new-business cell, where there is no extract to check, and on
    Chassis B, which has no PM at all.  On the in-force cell it is a live cross-check, and
    what it catches is an extract built by **accumulating** the PM from issue rather than
    re-striking it — the same error :func:`check_guarantee_funding` catches inside the
    projection, arriving from the data side instead.

    The comparison is against ``pm_at(t, "BOM")``, the **opening** PM of the first
    projected month — the extract's own valuation date — and not against that month's
    closing PM.  ``proj_start()`` is a month now, 48 on shipped point 7, and
    ``disc_factor(48)`` discounts over ``rem_term(48) = 6`` years, so the re-strike lands
    on the extract's 8,575.24 exactly as it did on the annual grid.
    """
    if (t != proj_start() or duration_inforce() == 0 or not is_euro_leg()):
        return 0.0
    return pm_at(t, "BOM") - pm_init()


def check_pm_restruck():
    """True when a shipped in-force *provision mathématique* agrees with R. 134-2."""
    return all(abs(check_pm_restruck_resid(t)) <= inforce_tol        # noqa: F821
               for t in range(proj_start(), proj_len()))


def result_cf():
    """Result table of cashflows, indexed by the 0-based policy **month** t.

    The frame is ``range(proj_start(), proj_len())``: one row per projected policy month —
    120 on the worked example and 72 on the in-force point 7 — the first of which carries
    the initial *versement* and the acquisition costs it draws.

    ``pols_if`` is the **start**-of-month count, which is the exposure the flows on that
    same row are weighted by; the notes' end-of-month ``l(t)`` is
    ``pols_if_at(t, "AFT_DECR")``
    and is not published here.  ``charges_taken`` and ``rider_claims`` are
    memo lines outside ``net_cf`` — the first is a transfer inside the account from the
    savers to the insurer, and the second is already inside ``claims_death``.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "charges_taken": [charges_taken(t) for t in ts],
            "rider_claims": [rider_claims(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by ``policy_year``.

    Every cash flow column is the total of its twelve months; ``pols_if`` is the count at
    the **start** of the policy year, ``pols_if(12 x (policy_year - 1))``, which is the
    number the annual-step model this one replaced carried on the same row.  It is the
    monthly frame **regrouped, never a second projection**, which is what lets the notes'
    annual figures be laid beside the monthly ones and the difference read off.

    Laid beside the annual-step model this one replaced, the columns split three ways.
    ``pols_if`` and ``premiums`` agree **exactly on every shipped model point**: the
    opening in-force is what the monthly decrements compound back to, and a *versement*
    is collected in a month the contract names and weighted by the in-force of that month
    under either grid.  ``withdrawals`` agrees on every cell that takes no *rachat
    partiel*, which is all of them but point 5.  ``charges_taken`` agrees wherever the
    decrements are switched off (points 1-4); elsewhere its surrender-indemnity term is
    weighted by the month of exit and moves with the claims.

    The rest do **not** agree, and are not meant to.  ``expenses`` moves because
    maintenance now accrues at one twelfth a month on the month's own provision and
    in-force and the annual grid's extra opening-striking charge is gone — the largest
    single-year gap on the shipped cells is 33.28 EUR, on point 9.  The ``claims_*``
    columns move because a claim now falls at the end of the month of exit rather than of
    the year.  ``liability_cf`` and ``net_cf`` inherit both.  That gap is the point of the
    finer grid.

    The frame opens on the policy year the model point's first projected month opens, so
    an in-force cell is indexed from ``duration_inforce() + 1`` rather than from 1.
    """
    df = result_cf()
    years = pd.Index(                                                # noqa: F821
        [duration(t) + 1 for t in df.index], name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


def result_provisions():
    """Result table of the provision machinery, indexed by the 0-based policy **month** t.

    Every column is a **closing** value of month t, or a rate applied within it.  The
    account's assets against the two provisions, the parts and their value, and the
    insurer's own-funds items beside them — reported, and never in a benefit.  The notes'
    two worked-example tables are the **anniversary** rows of this frame,
    ``t = 11, 23, ..., 119``, whose opening state is ``own_assets_at(t, "BOM")`` and its
    siblings rather than a row of the frame.  The other eleven rows of each policy year
    are the A. 134-5 intermediate valuations, which the annual grid could not report at
    all.

    ``i_pm`` is the rate the month's provisions are **struck at**: ``i_pm(t + 1)``, the
    A. 134-1 rate at the month-end boundary, since :func:`i_pm` is indexed by a month
    boundary.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "i_pm": [i_pm(t + 1) for t in ts],
            "asset_return": [asset_return(t) for t in ts],
            "parts_levy": [parts_levy(t) for t in ts],
            "perf_levy": [perf_levy(t) for t in ts],
            "own_assets": [own_assets(t) for t in ts],
            "mg": [mg(t) for t in ts],
            "pm": [pm(t) for t in ts],
            "prov_div": [prov_div(t) for t in ts],
            "parts": [parts(t) for t in ts],
            "part_value": [part_value(t) for t in ts],
            "insurer_contribution": [insurer_contribution(t) for t in ts],
            "pgt": [pgt(t) for t in ts],
            "pcdd": [pcdd(t) for t in ts],
            "surrender_value": [surrender_value(t) for t in ts],
            "death_payout": [death_payout(t) for t in ts],
            "maturity_value": [maturity_value(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

omega_age = 120

mort_be_factor = 0.8

tec_haircut = 0.9

lock_up_cap = 8

indemnity_cap = 0.05

indemnity_max_years = 10

apport_cap = 0.1

conv_headroom_rate = 0.15

revalue_gate1_factor = 1.5

revalue_gate2_factor = 0.1

guarantee_imminent_factor = 0.5

guarantee_imminent_years = 2

duration8_year = 8

duration8_factor = 1.5

expense_acq_rate = 0.05

expense_comm_rate = 0.02

expense_maint_rate = 0.002

roll_fwd_tol = 1e-08

funding_tol = 1e-07

floor_tol = 1e-09

inforce_tol = 0.005

pd = ("Module", "pandas")
