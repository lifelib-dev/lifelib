# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Index_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 8            # or switch the default

.. rubric:: Two clocks: a monthly frame over an annual *Indexjahr*

``t`` counts **policy months from issue**, 0-based. ``proj_len() = 12 x proj_len_y()`` is
the **exclusive end** of the frame, with ``proj_len_y() = ann_start_age - entry_age`` the
number of policy years, so ``result_cf().index[-1] == proj_len() - 1`` and the frame of an
in-force point at ``dur_init = 8`` has 228 rows while still reporting ``proj_len() = 324``.
A **new-business** point starts at ``t = 0``; an **in-force** point starts at
``t = t_start() = 12 x dur_init``, because ``t`` is counted from the policy's own inception
and not from the valuation date.

**Almost nothing on this product is monthly, and the argument of a cells says which clock
it is on.** Cells that state an **annual** construction take a 0-based policy year ``k``:
the premium and all three of its charges, the *Deckungskapital* and its § 169 Abs. 3
shadow, the whole *Indexjahr* — Cap, *Partizipationsquote*, the sum of the twelve capped
returns, the *Indexrendite* and the *Indexgutschrift* — the option budget and the safe-arm
credit, the *Höchststandsicherung* ledger, the guaranteed capital, the death benefit, the
surrender value and the maturity benefit. Cells that state a **month** take ``t``: the in
force, the two decrements, the claims, the expenses and every ``result_cf()`` column.
``duration(t) = t // 12`` is the bridge, ``policy_year(t) = duration(t) + 1`` is the
contractual 1-based label, ``age(t) = age_y(duration(t))`` steps on the **anniversary**, and
``is_anniv(t) = (t % 12 == 11)`` marks the month the annual machinery acts in.

**The one place the finer grid earns its keep is the *Indexjahr* itself.** Its twelve
monthly returns were already the mechanic and were already read month by month — but only
inside a single cells, invisible from the frame. ``index_month(t)``,
``index_return_mth(t)`` and ``index_return_capped_mth(t)`` now put them on the frame, one
row each, so the asymmetry the product turns on — capped above, **not** floored below — can
be read off month by month instead of inferred from a year's sum. What that cannot change
is the *settlement*: ``index_credit_pp(k)`` is struck at the year end and nowhere inside
it, because that is the contract.

The decrement rates keep the library's two speeds: ``mort_rate(t)`` and ``lapse_rate(t)``
return the **annual** rate of the policy year, and ``mort_rate_mth(t)`` and
``lapse_rate_mth(t)``, each ``1 - (1 - r)^(1/12)``, are what the recursion applies. Twelve
of each compound back to the year, which leaves the whole annual layer **bit-identical** to
the annual-step model this replaced, on all thirteen model points: the account, the ledger,
the guaranteed capital, every *Indexgutschrift*, the surrender value and premium income are
unchanged. What moved is the **split** of a year's exits between death and surrender, now
competing month by month rather than in one fixed annual order, and the expenses, which a
policy leaving mid-year now bears only for the months it was there.

At the end of month ``proj_len() - 1`` the accumulation contract ends: the capital falls
due at *Rentenbeginn* as ``claims(12n - 1, "MATURITY")``, and whether it is taken as a
*Kapitalabfindung* or converted at the *Rentenfaktor* changes what is **reported**, not
the cash flow. The *Rentenphase* itself is ``products/sofortrente/``.

.. rubric:: Two frames, and the third

:func:`result_cf` is the **monthly** cash flow statement and carries the five flows that
cross the contract boundary. :func:`result_cf_annual` sums it into policy years.
:func:`result_index` is the **annual state** behind both — the *Indexjahr*, the three
credits, the account, the ledger and the guaranteed capital — indexed by the 1-based
``policy_year``. The account movements live there and not in the cash flow statement:
they move once a year, and a statement whose columns do not all sum to its bottom line is
one a reader has to know which columns to skip.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/indexpolice/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Index_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Index_DE_S.Data`, reached here through the ``data`` Reference:

=====================  =================================  ==========================
Reference              Cells                              File
=====================  =================================  ==========================
model_point_file       data.model_point_table()           model_point_table.csv
index_return_file      data.index_return_table()          index_return_table.csv
index_param_file       data.index_param_table()           index_param_table.csv
surplus_rate_file      data.surplus_rate_table()          surplus_rate_table.csv
election_file          data.election_table()              election_table.csv
mort_file              data.mort_table()                  mort_table.csv
lapse_file             data.lapse_table()                 lapse_table.csv
freq_load_file         data.freq_load_table()             freq_load_table.csv
=====================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_pp`` and
``av_pp_at(t, timing)`` for the account value and its within-year reads, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string. The technical notes use compact actuarial symbols
instead. The mapping is:

=========================  ==============================  ===========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ===========================
(none)                     model_point()                   The selected model point row
n = ann_start - entry      proj_len_y()                    Number of projected policy
                                                           years; last one is n - 1
12 n                       proj_len()                      Exclusive end, in months
t0 = 12 dur_init           t_start()                       First projected month
k0 = dur_init              k_start()                       First projected policy year
(none)                     duration_mth(t)                 Elapsed policy months, = t
k(t)                       duration(t)                     0-based policy year of month t
t + 1 (contractual)        policy_year(t)                  1-based policy year label
(none)                     is_anniv(t)                     Last month of a policy year
m(t)                       index_month(t)                  Month of the Indexjahr, 1-12
x(k)                       age_y(k)                        Attained age in policy year k
x(t)                       age(t)                          The same, read at a month
l(t)                       pols_if(t)                      In force at the start of month t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / AFT_DEATH /
                                                           AFT_LAPSE
(year end)                 pols_surv_year_end(k)           Survivors the Indexjahr credit
                                                           is given to
q_d(t)                     mort_rate(t)                    Annual death rate
q^m_d(t)                   mort_rate_mth(t)                The monthly rate applied
w_l(t)                     lapse_rate(t)                   Annual surrender rate applied
w^m_l(t)                   lapse_rate_mth(t)               The monthly rate applied
(table)                    lapse_rate_base(t)              The table rate before the
                                                           terminal-year override
phi                        freq_load()                     Ratenzahlungszuschlag
P_b(k)                     prem_base_pp(k)                 Annual-mode premium due
P(k)                       prem_gross_pp(k)                Premium actually collected
(none)                     prem_due(t)                     Whether P falls due in month t
BS                         prem_sum()                      Beitragssumme
alpha(k)                   prem_charge_acq_pp(k)           Acquisition charge, tariff
alpha_5(k)                 prem_charge_acq_min_pp(k)       The same on the 5-year spread
beta P(k)                  prem_charge_adm_pp(k)           Premium administration charge
P+(k)                      prem_to_av_pp(k)                Premium credited to the account
Pi(k)                      prem_paid_pp(k)                 Cumulative annual-mode premium
A(k)                       av_pp(k)                        Deckungskapital at the start
(within year)              av_pp_at(k, timing)             BEF_PREM / AFT_PREM /
                                                           AFT_CHARGE / AFT_GUAR /
                                                           AFT_CREDIT
gamma, F(k)                exp_av_rate, av_charge_pp(k)    Reserve charge rate; amount
i_g, I(k)                  guar_rate(), guar_int_pp(k)     Rechnungszins; guaranteed
                                                           interest
(shadow)                   av_min_pp(k), av_min_pp_at(..)  The 169 Abs. 3 account
G(k)                       index_base_pp(k)                Participating capital of the
                                                           Indexjahr
b(k)                       surplus_rate(k)                 Declared Ueberschussanteilsatz
w(k)                       elect_index(k)                  Fraction elected to the index
B(k)                       opt_budget_pp(k)                Option budget, spent
U(k)                       surplus_credit_pp(k)            Safe-arm credit
r(k,m)                     index_return(k, m)              The month's index return
r(t)                       index_return_mth(t)             The same, read at a month
C(k), q(k)                 index_cap(k), index_quote(k)    Monthly Cap; Partizipationsquote
min(r, C)                  index_return_capped(k, m)       Capped above, not floored below
min(r, C)                  index_return_capped_mth(t)      The same, read at a month
S(k)                       index_sum(k)                    Sum of the twelve capped months
Y(k)                       index_return_year(k)            Compounded raw year return
rho(k)                     index_credit_rate(k)            The Indexrendite
X(k)                       index_credit_pp(k)              The Indexgutschrift
(diagnostic)               index_budget_ratio()            Credits over budget
K(k)                       credit_cum_pp(k)                Hoechststandsicherung ledger
guar_level Pi(k)           guar_floor_pp(k)                The Beitragsgarantie
Gamma(k)                   guar_cap_pp(k)                  Guaranteed capital
D(k)                       db_pp(k)                        Death benefit
V(k)                       cv_pp(k)                        Surrender value
(169 Abs. 3)               min_surr_pp(k)                  Minimum surrender value
(Stornoabzug)              surr_charge_pp(k)               Surrender charge
M(n-1)                     mat_pp(k)                       Benefit at Rentenbeginn
claims_death, ...          claims(t, kind)                 Benefit outgo by kind
(released)                 av_released(k)                  Account taken out by the exits
E(t)                       expenses(t)                     Insurer expense outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ===========================

.. rubric:: Charges and expenses are two different things

A **charge** is a deduction from the policyholder's *Deckungskapital*
(``prem_charge_acq_pp``, ``prem_charge_adm_pp``, ``av_charge_pp``); an **expense** is the
insurer's own cash outgo and appears in ``net_cf`` (``exp_acq_pp``, ``exp_maint_pp``).
They are of the same order here by construction, so the *Kostenüberschuss* is small. The
model does **not** close the MindZV loop — it does not compute a cost result, return half
of it to the policyholder and raise the declared rate — so changing an expense assumption
changes ``net_cf`` without changing what the policyholder receives. That is a stated
limitation of the reference implementation, not an oversight.

.. rubric:: The two steps that define the product

**Step 2 of the annual processing order:** the participating base is struck on the
**opening** balance, ``index_base_pp(k) = av_pp(k)``, *before* the year's premium. That
is why a new-business point credits nothing in its first year ``k = 0`` however well the
index does, and it is a **[std]** reading — whether the base is the whole *Deckungskapital*, an
index-participating sub-account or the accumulated *Überschussguthaben* alone was not
established, and a different reading rescales every credit in the model.

**Step 12:** the credit lands at the **end of the *Indexjahr*** and goes to the
**survivors**, :func:`pols_surv_year_end` — the opening cohort of the year less every death
and every surrender in any of its twelve months — while the premium, the charges and the
guaranteed interest are struck on the year's opening in-force ``pols_if(12k)``. The
decrementing lives paid the premium and earned the guaranteed interest before they left;
they did not see the *Indexjahr* out. ``av_released(k)`` is the account those exits carry
out of the fund, and it exists as a cells precisely so that ``check_av_roll_fwd()`` is exact
rather than approximate.

The asymmetry that follows is the product's own rule, and a model that pays two exits at
the same instant the same amount has lost it: death and surrender are struck on
``av_pp_at(k, "AFT_GUAR")``, the account **before** the year's credits, because a
mid-year exit forfeits the running *Indexjahr* **[std]**; the maturity is struck on
``av_pp(n)``, **including** them, because that contract ran the *Indexjahr* to its
end, and it is then floored at the *Beitragsgarantie* plus the whole locked-in ledger.

**The monthly grid dates that forfeiture.** On the annual grid every exit fell at a year
end and the forfeiture was a statement about an amount; here a surrender in month 7 of an
*Indexjahr* is a row of the frame, and the incentive the product carries — to surrender
just **after** a year closes rather than just before — is visible in the projection rather
than only in prose. What the grid does **not** do is pro-rate the payoff: no carrier
convention for that was established, so the forfeiture stays a **[std]** all-or-nothing
rule and the monthly grid says exactly when it bites.

.. rubric:: What is deliberately not here

No unit account, unit price or fund value — the capital is in the *Sicherungsvermögen*
and the surrender value is a reserve. No *Beitragsfreistellung* sub-population: German
lapse is a three-way decrement and this model carries surrender only. No *Dynamik*, no
*Zuzahlungen*, no *Rentengarantiezeit*, no *Schlussüberschussanteil* and no
*Bewertungsreserven* share. No dynamic surrender: on this contract the account cannot
fall from the index, so the usual driver is absent, and the driver that *is* present — a
run of zero *Indexjahre* — has no published calibration, so inventing one would put a
large unevidenced number at the centre of the result. No discounting, no
*Deckungsrückstellung*, no *Zinszusatzreserve*, no technical provisions and no tax.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# --- the model point ---------------------------------------------------------

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point; reporting only."""
    return model_point()["policy_id"]


def sex():
    """``"M"`` or ``"F"``: the row of the best-estimate mortality table to read.

    **Never a rating factor.** Sex may not enter a premium, a charge or a benefit in a
    contract written after 21 December 2012, and none of them depends on it here; it
    selects a decrement only.  Because the death benefit of this product is the account
    value with a floor rather than a sum at risk, mortality is a **timing** assumption and
    the choice moves the result very little.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def entry_age():
    """*Eintrittsalter*: age last birthday at inception, the origin of ``age(t)``."""
    return int(model_point()["entry_age"])


def dur_init():
    """Completed policy years at the valuation date; 0 for new business.

    The frame starts at ``t_start() = dur_init()``, because ``t`` is the policy's own
    elapsed duration and both are 0-based counts of completed years.  An in-force point
    brings its state with it — ``av_pp_init``,
    ``guar_locked_init``, ``prem_paid_init`` — rather than having it re-derived, which is
    what makes the in-force cells independent evidence about the recursion rather than a
    replay of it.
    """
    return int(model_point()["dur_init"])


def pols_if_init():
    """Policies in force at ``t_start()``: 1.0, a single-policy model point.

    Named rather than written as a literal because it is the scale of the roll-forward
    tolerances and the quantity ``result_cf()``'s first ``pols_if`` value must equal.
    """
    return float(model_point()["pols_if_init"])


def ann_start_age():
    """Attained age at *Rentenbeginn*, the end of the accumulation phase."""
    return int(model_point()["ann_start_age"])


def prem_form():
    """``"level"`` (*laufender Beitrag*) or ``"single"`` (*Einmalbeitrag*)."""
    v = model_point()["prem_form"]
    if v not in ("level", "single"):
        raise ValueError("invalid prem_form")
    return v


def prem_freq():
    """The payment frequency: annual, half_yearly, quarterly or monthly.

    It selects the *Ratenzahlungszuschlag* in :func:`freq_load` and does nothing else.
    """
    v = model_point()["prem_freq"]
    if v not in ("annual", "half_yearly", "quarterly", "monthly"):
        raise ValueError("invalid prem_freq")
    return v


def prem_term_y():
    """*Beitragszahlungsdauer* in policy years; 1 on a single premium."""
    return int(model_point()["prem_term_y"])


def av_pp_init():
    """The *Deckungskapital* per policy at ``t_start()``; 0 for new business."""
    return float(model_point()["av_pp_init"])


def guar_locked_init():
    """The *Höchststandsicherung* ledger already accumulated at ``t_start()``.

    Every credit — index or safe-arm — made before the valuation date.  Zero for new
    business.  It is carried separately from :func:`av_pp_init` because the two answer
    different questions: the account says what the policy is worth, the ledger says how
    much of it can never be lost.
    """
    return float(model_point()["guar_locked_init"])


def prem_paid_init():
    """Annual-mode premiums already paid at ``t_start()``; the base of the guarantee so far."""
    return float(model_point()["prem_paid_init"])


def guar_level():
    """*Garantieniveau*: the *Beitragsgarantie* as a fraction of the *Beitragssumme*.

    The wrapper sets the floor, not the index module: a *Schicht 3* contract may be sold
    at 60 %, 80 %, 90 % or 100 %, while a *Riester* contract must guarantee 100 % of
    contributions and allowances by statute.  Every euro of guarantee not promised is a
    euro that can back risk assets and therefore a larger option budget — a feedback this
    model does **not** carry, so the *Garantieniveau* sensitivity it reports is only the
    maturity-floor effect.
    """
    return float(model_point()["guar_level"])


def guar_rate():
    """``i_g``: the contract's *Rechnungszins*, a **cohort** fact and not today's rate.

    The *Höchstrechnungszins* history the shipped points span — 1.00 % for 2025-2026,
    0.90 % for a 2017-2021 cohort, 0.25 % for 2022-2024 — is why a book of this product
    cannot be projected on one rate.  At 0.25 % the rate equals the reserve charge and the
    account falls in a year that credits nothing, which is model point 13.
    """
    return float(model_point()["guar_rate"])


def payoff_form():
    """``"cap"`` (the monthly Cap design) or ``"quote"`` (the *Partizipationsquote*).

    The two designs are **not** interchangeable and fail differently: the Cap gives away
    the large monthly moves and is hurt by volatility even in a year that ends well, while
    the *Quote* gives away a constant fraction in every state.  Model points 1 and 2 run
    them on the identical index path so the difference is visible rather than argued.
    """
    v = model_point()["payoff_form"]
    if v not in ("cap", "quote"):
        raise ValueError("invalid payoff_form")
    return v


def index_id():
    """The key into *index_return_table.csv* and *index_param_table.csv*."""
    return model_point()["index_id"]


def elect_id():
    """The key into *election_table.csv*: this policy's *Wahlrecht* path."""
    return model_point()["elect_id"]


def death_min_rate():
    """The *Mindesttodesfallschutz* floor on the death benefit, as a fraction of ``BS``.

    0.50 on the shipped points that carry it: the standard formulation of the condition
    that a contract concluded from 1 April 2009 must satisfy for the favourable
    half-income treatment of a *Kapitalabfindung*.  It is a floor on the benefit and never
    a sum at risk added to it.
    """
    return float(model_point()["death_min_rate"])


def ann_option():
    """``"annuity"`` or ``"cash"``: how the terminal capital is **reported**.

    It changes :func:`ann_monthly_pp` and nothing else.  The *Kapitalwahlrecht* is a
    configuration of the model point, not a take-up rate: modelling it as a rate would
    stand in for a tax comparison this model does not perform.
    """
    v = model_point()["ann_option"]
    if v not in ("annuity", "cash"):
        raise ValueError("invalid ann_option")
    return v


def surr_charge_on():
    """1 if the contractual *Stornoabzug* applies to this policy, 0 if not.

    A *Stornoabzug* is effective only if it is agreed, appropriate **and quantified in the
    contract**, so a tariff without the clause is a real configuration and not a special
    case.
    """
    return int(model_point()["surr_charge_on"])


# --- the frame ---------------------------------------------------------------

def k_start():
    """``k0``: the first projected **policy year**, ``dur_init()`` — the elapsed years.

    New business starts at 0; an in-force point starts partway through its own term, at
    the count of policy years it has already completed.  Every annual construction in this
    model — the premium and its charges, the account, the *Indexjahr*, the
    *Höchststandsicherung* ledger, the death benefit and the surrender value — is defined
    from here.
    """
    return dur_init()


def t_start():
    """``t0``: the frame's first **month**, ``12 x k_start()``.

    ``dur_init`` is an elapsed count of policy **years**, so the conversion is a
    multiplication and no model point column changed.  The frame's *start* is a product fact
    and is not fixed per model, which is why the conventions suite asserts contiguity and
    the last index rather than the first.
    """
    return 12 * k_start()


def proj_len_y():
    """``n``: the **number of projected policy years**, ``ann_start_age() - entry_age()``.

    Policy year ``n - 1`` is the last and ends at *Rentenbeginn*, at time ``n``, when the
    capital falls due.  There is no policy year ``n``: the whole surviving cohort has
    matured, while ``av_pp(n)`` and ``guar_cap_pp(n)`` are defined, being the time-``n``
    per-policy amounts the maturity benefit is struck on.
    """
    return ann_start_age() - entry_age()


def proj_len():
    """The **exclusive end** of the frame, counted in policy **months**: ``12 x proj_len_y()``.

    The library's reading of ``proj_len()`` and lifelib's own: ``result_cf()`` covers
    ``t = t_start() ... proj_len() - 1``, so ``result_cf().index[-1] == proj_len() - 1``.
    It is **not** the row count of an in-force point — one at ``dur_init = 8`` publishes
    228 rows and still reports 324.
    """
    return 12 * proj_len_y()


def duration_mth(t):
    """The number of **complete policy months** elapsed at the start of month t: ``t`` itself.

    Published rather than inlined because it is the name the rest of the library uses for
    the elapsed-month count, and because a model whose frame starts partway through a
    contract must say once, in one place, that ``t`` is counted from **inception** and not
    from the frame's own start.
    """
    return t


def duration(t):
    """``k(t)``: the **0-based policy year** month t falls in, ``duration_mth(t) // 12``.

    The bridge between the two clocks.  Everything annual on this product — the premium,
    the account, the whole *Indexjahr*, the ledger, the guarantee, the death benefit and
    the surrender value — takes this ``k``; the in force, the decrements, the claims and
    the expenses take ``t``.
    """
    return duration_mth(t) // 12


def is_anniv(t):
    """Whether month t is the **last** month of its policy year: ``t % 12 == 11``.

    The month the annual machinery acts in: the *Indexjahr* closes, the *Indexgutschrift*
    is struck and locked in, the safe-arm credit is made and the account rolls to its next
    opening balance.
    """
    return t % 12 == 11


def policy_year(t):
    """The **contractual, 1-based** policy year of month t: ``duration(t) + 1``.

    Derived and never indexed by; the input tables that are keyed by duration are keyed on
    the 0-based ``duration(t)`` instead, which is what they were already keyed on.
    """
    return duration(t) + 1


def index_month(t):
    """``m(t)``: which month of its *Indexjahr* month t is, **1-based**: ``t % 12 + 1``.

    The *Indexjahr* is aligned with the policy year **[std]**, so month 1 opens on the
    anniversary and month 12 closes on the next one.  This is the column of
    *index_return_table.csv* that month t reads — see :func:`index_return_mth` — and it is
    the one thing the annual grid could not name: the twelve capped returns were a sum
    computed inside a single row, and they are now twelve rows of the frame.
    """
    return duration_mth(t) % 12 + 1


def age_y(k):
    """``x(k)``: the attained age in policy year k, ``entry_age() + k``."""
    return entry_age() + k


def age(t):
    """``x(t)``: the attained age in month t, ``age_y(duration(t))``.

    Age last birthday **stepping on the policy anniversary**, the basis the delib registry
    fixes for the whole library: the monthly grid does not refine it, and a model that
    stepped the age monthly would read a mortality rate the table does not publish.
    """
    return age_y(duration(t))


# --- the premium and its charges ---------------------------------------------

def prem_sum():
    """``BS``: the *Beitragssumme*, on the **annual-mode** premium.

    ``prem_gross_pp x prem_term_y`` on the level form and the single premium itself on the
    single form — the premiums payable over the whole contract, counted from issue and not
    from ``t_start()``, because a *Beitragssumme* is a contract fact that an in-force
    point brings with it.

    The *Ratenzahlungszuschlag* does **not** enter it.  A frequency surcharge is the price
    of paying in instalments, not more insurance bought, so it may not inflate the
    acquisition charge or the *Mindesttodesfallschutz* floor: on model point 4 the premium
    collected is 2,520.00 EUR a year while ``prem_sum()`` is 2,400.00 x 32 = 76,800.00 EUR.
    Getting that wrong is a numbered pitfall.
    """
    if prem_form() == "single":
        return float(model_point()["prem_gross_pp"])
    return float(model_point()["prem_gross_pp"]) * prem_term_y()


def freq_load():
    """``phi``: the *Ratenzahlungszuschlag* multiplier for this policy's payment frequency.

    1.000 annual, 1.020 half-yearly, 1.030 quarterly, 1.050 monthly **[std]** — the market
    convention, no carrier tariff having been established.  It multiplies the premium
    **collected** and nothing else; see :func:`prem_sum`.
    """
    return float(data.freq_load_table().loc[                         # noqa: F821
        prem_freq(), "freq_load"])


def prem_base_pp(k):
    """``P_b(k)``: the annual-mode premium due in period k, per policy.

    The level form pays ``prem_gross_pp`` in the first ``prem_term_y()`` policy years,
    i.e. at ``k < prem_term_y()``, which may be shorter than the projection — model point
    13 stops paying after policy year 12 (``k = 11``) and runs to policy year 22.  The
    single form pays the whole premium in the first projected period and nothing
    afterwards.
    """
    if k < k_start() or k >= proj_len_y():
        return 0.0
    if prem_form() == "single":
        return float(model_point()["prem_gross_pp"]) if k == k_start() else 0.0
    return float(model_point()["prem_gross_pp"]) if k < prem_term_y() else 0.0


def prem_gross_pp(k):
    """``P(k)``: the premium actually collected in period k, ``P_b(k) x phi``.

    Annual in advance, at the start of the policy year.  This is the amount that reaches
    :func:`premiums` and out of which the contractual charges are taken; the amount that
    drives the *Beitragssumme* is :func:`prem_base_pp`.
    """
    return prem_base_pp(k) * freq_load()


def prem_charge_acq_pp(k):
    """``alpha(k)``: the acquisition charge deducted from the premium in period k.

    ``min(acq_cost_rate, zill_cap_rate) x BS`` spread evenly over the first
    ``min(zill_years, prem_term_y())`` premium-paying years, i.e. over ``k < spread`` —
    2.5 % of the *Beitragssumme* at the DeckRV *Höchstzillmersatz* of 25 per mille, over
    five years, so 324.00 EUR a year on the anchor's 64,800.00 EUR.  On a single premium
    it is taken in full in the first projected period, there being only one premium to
    take it from.

    This is a **charge**, a deduction from the policyholder's account.  The insurer's own
    acquisition **expense** is :func:`exp_acq_pp`, falls in one lump at inception, and is
    the *Zillmer* strain the five-year recovery works off.
    """
    if k < k_start() or k >= proj_len_y():
        return 0.0
    charge = min(acq_cost_rate, zill_cap_rate) * prem_sum()          # noqa: F821
    if prem_form() == "single":
        return charge if k == k_start() else 0.0
    spread = min(zill_years, prem_term_y())                          # noqa: F821
    return charge / spread if k < spread else 0.0


def prem_charge_acq_min_pp(k):
    """``alpha_5(k)``: the same charge on the **five-year** spread of § 169 Abs. 3 VVG.

    Acquisition and distribution costs must be spread over at least the first five years
    for the purpose of the *Mindestrückkaufswert*, whatever the tariff does — so this
    profile is written with the literal 5 and not with ``zill_years``, which is a tariff
    parameter and not a statutory one.  With ``zill_years = 5`` the two coincide exactly
    and the floor is a no-op, which is the point: delib's charge profile is already at the
    statutory floor.  Set ``zill_years = 1`` and the floor bites.

    A single premium is taken once, so there is no second premium over which to spread
    anything and the two profiles coincide there by construction rather than by parameter.
    """
    if k < k_start() or k >= proj_len_y():
        return 0.0
    charge = min(acq_cost_rate, zill_cap_rate) * prem_sum()          # noqa: F821
    if prem_form() == "single":
        return charge if k == k_start() else 0.0
    spread = min(5, prem_term_y())
    return charge / spread if k < spread else 0.0


def prem_charge_adm_pp(k):
    """``beta P(k)``: the premium-based administration charge, 3 % of the premium collected.

    *Verwaltungskosten* taken as the premium is credited.  **[std]**: no German insurer
    publishes a charge level for this product.
    """
    return exp_prem_rate * prem_gross_pp(k)                          # noqa: F821


def prem_to_av_pp(k):
    """``P+(k)``: the part of the premium credited to the account.

    ``P(k) - alpha(k) - beta P(k)``.  On the anchor's first five years that is
    ``2,400.00 - 324.00 - 72.00 = 2,004.00 EUR``, and 2,328.00 EUR thereafter.  Negative
    values are possible in principle on a tariff whose charges exceed the premium; none of
    the shipped points is one.
    """
    return prem_gross_pp(k) - prem_charge_acq_pp(k) - prem_charge_adm_pp(k)


def prem_to_av(k):
    """The premium credited to the account at fund level: ``P+(k) x l(k)``.

    Struck on the **opening** in-force of the policy year, ``pols_if(12k)``, because the
    lives that decrement during the year have already paid the year's premium in advance.
    """
    return prem_to_av_pp(k) * pols_if(12 * k)


def prem_paid_pp(k):
    """``Pi(k)``: cumulative annual-mode premiums paid to time k, the start of period k.

    Starts at ``prem_paid_init()`` and adds ``P_b(k)`` each year, so ``Pi(n)`` — the value
    at *Rentenbeginn* — is the whole *Beitragssumme* for a policy that pays throughout.  Non-decreasing by
    construction, which is half of why :func:`guar_cap_pp` is monotone.
    """
    if k <= k_start():
        return prem_paid_init()
    return prem_paid_pp(k - 1) + prem_base_pp(k - 1)


def prem_due(t):
    """Whether the year's premium falls due at the **beginning** of month t.

    ``duration_mth(t) % 12 == 0`` — the first month of each policy year and no other.  The
    *Beitrag* of this tariff is payable in advance for the *Versicherungsperiode*, which is
    the year (§ 12 Abs. 1 VVG), and the *Indexjahr* the whole product turns on is struck on
    the balance standing at the anniversary: splitting the premium without splitting the
    *Indexjahr* would credit a policy with a year it did not pay for.  The
    *Ratenzahlungszuschlag* :func:`freq_load` is what a sub-annual *Zahlweise* costs, and it
    remains the whole of what the *Zahlweise* does here.
    """
    return duration_mth(t) % 12 == 0


def premiums(t):
    """Premium income in **month** t, an inflow: ``P(k) x l(t)``, or zero.

    Non-zero only where :func:`prem_due` makes the year's premium payable, so the count is
    the in-force at the **start of the policy year** and premium income is **bit-identical**
    to the annual-step model this replaced.  Not further multiplied by ``(1 - q_d)``:
    decrements fall at the **end** of a month, so a life that dies in the first month of a
    policy year has paid that year's premium.
    """
    return prem_gross_pp(duration(t)) * pols_if(t) if prem_due(t) else 0.0


# --- the surplus, the election and the option budget -------------------------

def surplus_rate(k):
    """``b(k)``: the declared *Überschussanteilsatz* for period k.

    2.50 % a year of ``G(k)``, level over the projection **[std]**.  **This rate is the
    option budget.**  The insurer earns a return on the *Sicherungsvermögen*, the MindZV
    forces at least 90 % of the excess over the guarantee into the policyholders' share,
    the insurer declares a rate out of that, and a contract in the index arm has the
    declared amount spent on options instead of credited as interest.  An Indexpolice
    therefore has **exactly the same risk budget** as a classic contract of the same
    vintage and spends it differently.

    Holding it level is the strongest single simplification in this model: in reality the
    rate moves with the investment result, and the feedback from the *Garantieniveau*
    through the asset mix to the declared rate is not modelled at all.
    """
    return float(data.surplus_rate_table().loc[k, "surplus_rate"])   # noqa: F821


def elect_index(k):
    """``w(k)``: the fraction of year k's declared surplus directed to the index arm.

    The *Wahlrecht*, read from this policy's election path.  A fraction in [0, 1] rather
    than a flag, because some tariffs permit a partial election and all-or-nothing is then
    the special case ``w in {0, 1}``.  It is a **behavioural** assumption and not a
    contractual one: whether real policyholders revisit the election at all is not
    established, and ``always_index`` is a modelling choice made so that the base run
    demonstrates the index mechanic rather than a claim about behaviour.
    """
    return float(data.election_table().loc[                          # noqa: F821
        (elect_id(), k), "w"])


def index_base_pp(k):
    """``G(k)``: the participating capital of *Indexjahr* k — the **opening** balance.

    ``av_pp(k)``, struck **before** the year's premium and before the year's charges.
    Two consequences, both intended: a new-business point credits nothing in its first
    period ``k = 0`` however well the index does, because the base is zero; and a premium
    paid during a year participates only from the following one.

    Whether the base is the whole *Deckungskapital*, a defined index-participating
    sub-account or the accumulated *Überschussguthaben* alone **was not established** for
    any carrier.  delib takes the whole capital **[std]**.  This is the largest
    unquantified uncertainty in the product file: a different reading rescales every credit
    in the model, and it is a documentary gap rather than a modelling choice.
    """
    return av_pp(k)


def opt_budget_pp(k):
    """``B(k)``: the option budget of *Indexjahr* k, ``w(k) b(k) G(k)``.

    The money the insurer spends buying the option package that replicates the promised
    payoff.  It is **spent, not credited**: if the *Indexjahr* ends at or below zero it has
    bought options that expired worthless, and that — the opportunity cost of one year's
    surplus — is the whole of the policyholder's downside.
    """
    return elect_index(k) * surplus_rate(k) * index_base_pp(k)


def surplus_credit_pp(k):
    """``U(k)``: the safe-arm credit of year k, ``(1 - w(k)) b(k) G(k)``.

    The part of the declared surplus **not** elected to the index arm, credited to the
    account as interest and guaranteed from the moment it is credited.  Zero throughout on
    the anchor, which elects the index arm in every year; the whole of the surplus on model
    point 11, which reduces the contract to a *klassische Rentenversicherung*.
    """
    return (1.0 - elect_index(k)) * surplus_rate(k) * index_base_pp(k)


def pols_surv_year_end(k):
    """The policies surviving to the **end of policy year k**, before any maturity.

    ``pols_if_at(12k + 11, "AFT_LAPSE")``: the opening cohort of the year less every death
    and every surrender in any of its twelve months.  This is the population the
    *Indexgutschrift* and the safe-arm credit are given to, because both are struck at the
    end of the *Indexjahr* and a life that left during it was not there for the payoff.

    On the annual grid this was ``pols_if_at(k, "AFT_LAPSE")`` and it is the same number:
    the two decrements compound geometrically, so the count at an anniversary is unchanged.
    What the monthly grid adds is that the lives which forfeited the year's credit are now
    dated — and the forfeiture is a month's event rather than a year-end lump.
    """
    return pols_if_at(12 * k + 11, "AFT_LAPSE")


def pols_death_year(k):
    """The deaths of policy year k, summed over its twelve months."""
    return sum(pols_death(t) for t in range(12 * k, 12 * k + 12))


def pols_lapse_year(k):
    """The surrenders of policy year k, summed over its twelve months."""
    return sum(pols_lapse(t) for t in range(12 * k, 12 * k + 12))


def surplus_credit(k):
    """The safe-arm credit at fund level: ``U(k) x pols_surv_year_end(k)``.

    On the **survivors**, not on the opening in-force: like the index credit, it is struck
    at the end of the *Indexjahr*, and the lives that died or surrendered during the year
    were not there for it.
    """
    return surplus_credit_pp(k) * pols_surv_year_end(k)


# --- the Indexjahr -----------------------------------------------------------

def index_return(k, m):
    """``r(k, m)``: the index return of month m of *Indexjahr* k, as a decimal.

    Read from row ``(index_id(), k)`` of *index_return_table.csv*, column ``m01`` ...
    ``m12``.  The *Indexjahr* is aligned with the policy year **[std]**: the contractual
    *Indexstichtag* need not fall on the policy anniversary, no carrier's convention was
    established, and an annual-grid model has no other defensible alignment.
    """
    return float(data.index_return_table().loc[                      # noqa: F821
        (index_id(), k), "m%02d" % m])


def index_return_mth(t):
    """``r(t)``: the index return of **month t**, read on the monthly frame.

    ``index_return(duration(t), index_month(t))`` — the same number the annual grid summed
    inside a single row, now addressable as a row of the frame.  It is what the monthly grid
    buys on this product: the *Indexjahr*'s twelve months **are** the mechanic, and until now
    they were invisible outside one cells.
    """
    return index_return(duration(t), index_month(t))


def index_return_capped_mth(t):
    """``min(r(t), C(k))``: month t's return **capped above and not floored below**.

    The monthly view of :func:`index_return_capped`, so that the asymmetry the product turns
    on can be read off the frame month by month rather than inferred from a year's sum.
    Twelve of these sum to :func:`index_sum`, which is the contract's formula and is what
    the test module asserts.
    """
    return index_return_capped(duration(t), index_month(t))


def index_cap(k):
    """``C(k)``: the monthly Cap of *Indexjahr* k.

    3.00 % on the equity path **[std]**, the midpoint of an argued 1.5-5.0 % band that no
    carrier document could confirm; 6.00 % on the low-volatility house path, which is
    cheaper to buy options on.  The Cap is fixed before the *Indexjahr* begins and is then
    binding for its whole length.

    **It is not a marketing parameter but the solution of a pricing equation**: given the
    option budget, the index's implied volatility and dividend yield and the risk-free
    rate, there is exactly one Cap at which the twelve-month capped-sum payoff costs the
    budget.  That is why caps move from year to year with no change in the contract, and it
    is why the Cap and :func:`surplus_rate` may not be chosen independently — see
    :func:`index_budget_ratio`.
    """
    return float(data.index_param_table().loc[                       # noqa: F821
        (index_id(), k), "cap"])


def index_quote(k):
    """``q(k)``: the *Partizipationsquote* of *Indexjahr* k, used by the ``quote`` design.

    60 % on the equity path and 100 % on the house path **[std]**.  A participation rate
    near or above 100 % on a volatility-targeted index is not generosity: it is what the
    same budget buys when the underlying is engineered to be cheap, and it moves the
    give-up from somewhere the purchaser can see to somewhere they cannot.
    """
    return float(data.index_param_table().loc[                       # noqa: F821
        (index_id(), k), "quote"])


def index_return_capped(k, m):
    """``min(r(k, m), C(k))``: the month's return **capped above and not floored below**.

    The asymmetry is the product, and it must never be softened.  A month in which the
    index rises 8 % contributes ``C``; a month in which it falls 8 % contributes the whole
    -8 %.  An implementation that floors the month at zero credits something in every year
    with an up-month in it, and gets the research file's Example B — where the sum is
    -2.60 % and the correct credit is nothing — spectacularly wrong.
    """
    return min(index_return(k, m), index_cap(k))


def index_sum(k):
    """``S(k)``: the **sum** of the twelve capped monthly returns of *Indexjahr* k.

    Summed, not compounded.  Summation is close to compounding for small numbers and is
    not the same thing, and the contractual formula is a sum: on the research file's
    Example A the twelve capped returns sum to exactly **+8.90 %** while compounding the
    same twelve gives 8.9599 %, an error small enough to look like rounding and large
    enough to be wrong at every duration.
    """
    return sum(index_return_capped(k, m) for m in range(1, 13))


def index_return_year(k):
    """``Y(k)``: the compounded **raw** index return of the year, ``prod(1 + r) - 1``.

    The uncapped, unfloored movement of the index itself.  It drives the
    *Partizipationsquote* design and is otherwise a diagnostic — and the diagnostic that
    matters most, because on the research file's Example B ``Y(9) = +6.4402 %`` while the
    Cap design credits **zero**.  The index rose and the credit was nothing; that is the
    feature the product is most criticised for and the one most often misdescribed.
    """
    out = 1.0
    for m in range(1, 13):
        out = out * (1.0 + index_return(k, m))
    return out - 1.0


def index_credit_rate(k):
    """``rho(k)``: the *Indexrendite* of *Indexjahr* k — the rate the credit is struck at.

    ``max(S(k), 0)`` in the Cap design, ``max(q(k) Y(k), 0)`` in the *Partizipationsquote*
    design.  **The floor is on the year, not on the month**, and in the Cap design it is on
    the *sum of capped returns* and not on the compounded raw return: applying it to ``Y``
    instead is a numbered pitfall that credits 6.44 % where the contract credits nothing.

    Never negative: the worst imaginable *Indexjahr* credits zero and leaves the capital
    untouched.  That floor is what makes this a life-insurance product rather than a bet,
    and it is the only reason the arm has a positive expectation at all — with a 3 % cap on
    a 17 %-volatility index the expected value of a *capped month* is negative.
    """
    if payoff_form() == "quote":
        return max(index_quote(k) * index_return_year(k), 0.0)
    return max(index_sum(k), 0.0)


def index_credit_pp(k):
    """``X(k)``: the *Indexgutschrift* per policy, ``rho(k) w(k) G(k)``.

    Credited at the end of the *Indexjahr* and **locked in**: once made it is permanently
    part of the guaranteed capital, earns the guaranteed rate thereafter like any other
    part of the *Deckungskapital*, and enters the base of every later *Indexjahr*.  That is
    the *Höchststandsicherung*, and it is what makes a year-by-year floor add up to a
    path-independent guarantee.

    Zero in the first period of a new-business point even when ``index_credit_rate(0)`` is
    positive, because ``G(0) = 0``.
    """
    if k < k_start() or k >= proj_len_y():
        return 0.0
    return index_credit_rate(k) * elect_index(k) * index_base_pp(k)


def index_credit(k):
    """The *Indexgutschrift* at fund level: ``X(k) x pols_surv_year_end(k)``.

    On the **survivors** of both decrements.  A life that died or surrendered during the
    *Indexjahr* forfeits it **[std]**: the payoff exists only at the year end, and whether
    a carrier pro-rates it, refunds the unspent option budget or simply keeps it was not
    established.  Crediting the year to the lives that left is a numbered pitfall and is
    caught by :func:`check_av_roll_fwd`.
    """
    return index_credit_pp(k) * pols_surv_year_end(k)


def index_budget_ratio():
    """Total index credits over total option budget, per policy, over the projection.

    The diagnostic that answers the one question the shipped parameters cannot: **are the
    Cap and the declared surplus rate mutually consistent?**  They are not free parameters
    — the Cap is the level at which the option strip costs the budget — so on a long
    enough path the credits should average the budget and this ratio should sit near 1.

    A value far from 1 means the pair is off, and it says which way: **above 1** the model
    is handing the policyholder more than the budget could buy, **below 1** it is charging
    for options it does not deliver.  On a single deterministic path the ratio is also
    sampling noise, so read it as an order-of-magnitude check and not as a calibration.
    Returns 0.0 where nothing was elected to the index arm, there being no budget to
    compare against.
    """
    budget = sum(opt_budget_pp(t) for t in range(k_start(), proj_len_y()))
    if budget <= 0.0:
        return 0.0
    credits = sum(index_credit_pp(t) for t in range(k_start(), proj_len_y()))
    return credits / budget


# --- the account -------------------------------------------------------------

def av_pp(k):
    """``A(k)``: the *Deckungskapital* per policy at time k, the **start** of period k.

    ``av_pp_init()`` at ``k_start()``, then ``av_pp_at(k - 1, "AFT_CREDIT")``.  Defined at
    ``k = proj_len_y()``, *Rentenbeginn*, where it is the balance the maturity benefit is
    struck on.

    **Not monotone, and it must not be asserted to be.**  What ratchets is the ledger of
    credits, not the balance: with the reserve charge at or above the guaranteed rate the
    account falls in a year that credits nothing, which is exactly model point 13's 0.25 %
    cohort once its premiums stop.  Testing the lock-in as "the account never falls" is a
    numbered pitfall.
    """
    if k < k_start() or k > proj_len_y():
        return 0.0
    if k == k_start():
        return av_pp_init()
    return av_pp_at(k - 1, "AFT_CREDIT")


def av_pp_at(k, timing):
    """The *Deckungskapital* per policy at a point inside period k.

    ``"BEF_PREM"``
        ``A(k)``, the opening balance — and the base ``G(k)`` the *Indexjahr*
        is struck on.

    ``"AFT_PREM"``
        after the premium net of its charges has been credited.

    ``"AFT_CHARGE"``
        after the reserve charge ``gamma`` on the post-premium balance.

    ``"AFT_GUAR"``
        after the guaranteed interest ``i_g``.  **This is the balance every
        exit is measured on**: a death or a surrender takes the account
        before the year's index and safe-arm credits, because a mid-year
        exit forfeits the running *Indexjahr* **[std]**.

    ``"AFT_CREDIT"``
        after the *Indexgutschrift* and the safe-arm credit, i.e. ``A(k + 1)``.
        The maturity benefit is struck here and the two other exits are not,
        which is the product's own asymmetry and not a rounding of it.
    """
    if timing == "BEF_PREM":
        return av_pp(k)
    if timing == "AFT_PREM":
        return av_pp(k) + prem_to_av_pp(k)
    if timing == "AFT_CHARGE":
        return av_pp_at(k, "AFT_PREM") - av_charge_pp(k)
    if timing == "AFT_GUAR":
        return av_pp_at(k, "AFT_CHARGE") + guar_int_pp(k)
    if timing == "AFT_CREDIT":
        return (av_pp_at(k, "AFT_GUAR")
                + index_credit_pp(k) + surplus_credit_pp(k))
    raise ValueError("invalid timing")


def av_charge_pp(k):
    """``F(k)``: the reserve charge of period k, ``gamma`` on the post-premium balance.

    0.25 % a year of ``av_pp_at(k, "AFT_PREM")`` **[std]** — *Verwaltungskosten* taken
    from the account rather than from the premium.  A **charge**, not an expense: it
    reduces the policyholder's *Deckungskapital* and does not appear in ``net_cf``.
    """
    return exp_av_rate * av_pp_at(k, "AFT_PREM")                     # noqa: F821


def av_charge(k):
    """The reserve charge at fund level: ``F(k) x l(12k)``, on the year's opening in-force."""
    return av_charge_pp(k) * pols_if(12 * k)


def guar_int_pp(k):
    """``I(k)``: the guaranteed interest of period k, ``i_g`` on the post-charge balance.

    The *Rechnungszins* of the policy's own cohort.  This is the **only** interest an
    Indexpolice credits in the index arm: the declared surplus is not added on top of it,
    it is spent.  A model that credits the guarantee *and* the declared rate *and* the
    index payoff has spent the same money three times.
    """
    return guar_rate() * av_pp_at(k, "AFT_CHARGE")


def guar_int(k):
    """The guaranteed interest at fund level: ``I(k) x l(k)``.

    On the **opening** in-force of the policy year, because the decrementing lives earned
    the year's guaranteed interest before they left — their benefit is struck on
    ``av_pp_at(k, "AFT_GUAR")``, which includes it.  That is the one thing the monthly grid
    deliberately does **not** refine: the *Rechnungszins* of this tariff is credited per
    *Versicherungsjahr*, and pro-rating it would be a crediting rule no wording states.
    """
    return guar_int_pp(k) * pols_if(12 * k)


def av_at(k, timing):
    """The account at fund level at a within-year point: ``av_pp_at(k, timing) x l(k)``.

    Struck on the year's opening in-force at every timing, so that the difference between
    two timings is a movement of the same population.  The count changes through the year,
    and that change is carried by :func:`av_released` rather than by re-weighting the
    balance.
    """
    return av_pp_at(k, timing) * pols_if(12 * k)


def av(k):
    """The *Deckungskapital* at fund level at time k: ``A(k) x pols_if(12k)``.

    Zero at ``k = proj_len_y()``, the whole surviving cohort having matured — which is
    why :func:`check_av_roll_fwd` closes in the final year only if the maturity is
    accounted for in :func:`av_released`.

    A **balance**, not a cash flow.  It is published in :func:`result_index` because a
    reader cannot follow this product without it, and it is **not** summed into ``net_cf``.
    """
    return av_pp(k) * pols_if(12 * k)


def av_released(k):
    """The account the year's exits carry **out of the fund** in period k.

    ``av_pp_at(k, "AFT_GUAR") x (deaths + surrenders of policy year k) + av_pp(k + 1) x
    maturities``: deaths and surrenders take the balance before the year's credits,
    maturities take it after them.  The exits are counted over the **whole policy year**,
    whatever months inside it they fell in, because the balance they carry out is an annual
    construction — the account of this tariff is defined at anniversaries and nowhere
    between them.

    This is deliberately **not** what the exits are *paid*.  The death floor pays more
    than the account releases, the *Stornoabzug* pays less, and the *Beitragsgarantie* at
    *Rentenbeginn* pays more.  Those three differences are insurer money and they belong in
    ``net_cf``, not in the account roll-forward — which is exactly what makes
    :func:`check_av_roll_fwd` an exact identity rather than an approximate one.
    """
    return (av_pp_at(k, "AFT_GUAR") * (pols_death_year(k) + pols_lapse_year(k))
            + av_pp(k + 1) * pols_maturity(12 * (k + 1) - 1))


# --- the § 169 Abs. 3 shadow account -----------------------------------------

def av_min_pp(k):
    """The shadow *Deckungskapital* on the statutory five-year acquisition-cost spread.

    The same recursion as :func:`av_pp` with :func:`prem_charge_acq_min_pp` in place of the
    tariff charge — the credits are identical, so only the acquisition profile differs.  It
    exists to produce :func:`min_surr_pp`, the § 169 Abs. 3 VVG floor under the surrender
    value, and it is a *shadow*: it is not the reserve, it is not published in the cash
    flow statement, and it never touches a death or a maturity benefit.

    An in-force point starts it at ``av_pp_init()`` for want of a second opening state in
    the model point table.  That understates the floor for a policy whose first five years
    are behind it, and it is a stated simplification rather than a claim.
    """
    if k < k_start() or k > proj_len_y():
        return 0.0
    if k == k_start():
        return av_pp_init()
    return av_min_pp_at(k - 1, "AFT_CREDIT")


def av_min_pp_at(k, timing):
    """The shadow account at a point inside period k; timings as :func:`av_pp_at`.

    Identical in structure, so that a reader comparing the two accounts is comparing one
    number — the acquisition charge — and not two recursions.
    """
    if timing == "BEF_PREM":
        return av_min_pp(k)
    if timing == "AFT_PREM":
        return (av_min_pp(k) + prem_gross_pp(k) - prem_charge_acq_min_pp(k)
                - prem_charge_adm_pp(k))
    if timing == "AFT_CHARGE":
        return av_min_pp_at(k, "AFT_PREM") * (1.0 - exp_av_rate)     # noqa: F821
    if timing == "AFT_GUAR":
        return av_min_pp_at(k, "AFT_CHARGE") * (1.0 + guar_rate())
    if timing == "AFT_CREDIT":
        return (av_min_pp_at(k, "AFT_GUAR")
                + index_credit_pp(k) + surplus_credit_pp(k))
    raise ValueError("invalid timing")


# --- the Höchststandsicherung ledger and the guarantee -----------------------

def credit_cum_pp(k):
    """``K(k)``: the *Höchststandsicherung* ledger — every credit ever made, cumulated.

    ``guar_locked_init()`` at ``k_start()``, then ``K(k) = K(k - 1) + X(k - 1) +
    U(k - 1)``.  Both index and safe-arm credits enter it, because both are guaranteed
    from the moment they are credited.  Monotone non-decreasing by construction, credits
    being non-negative.

    This is the quantity that makes the annual floor add up to something: a plain maturity
    guarantee lets the insurer recover a bad year with a good one, while here every
    credited amount is permanent, so **the cost of the guarantee rises with every good
    year**.  It is also what the *Deckungsrückstellung* means by "profit shares already
    allocated".
    """
    if k <= k_start():
        return guar_locked_init()
    return credit_cum_pp(k - 1) + index_credit_pp(k - 1) + surplus_credit_pp(k - 1)


def guar_floor_pp(k):
    """The *Beitragsgarantie* accrued to time k, the start of period k.

    ``guar_level() x prem_paid_pp(k)`` — a fraction of the premiums **actually paid so
    far**, so it grows with the premium stream and is complete only once the last premium
    is in.  On the anchor it reaches ``0.90 x 64,800.00 = 58,320.00 EUR`` at
    ``k = proj_len_y()``.
    """
    return guar_level() * prem_paid_pp(k)


def guar_cap_pp(k):
    """``Gamma(k)``: the guaranteed capital, ``guar_floor_pp(k) + credit_cum_pp(k)``.

    The *Beitragsgarantie* plus every locked-in credit — the second term dominating after
    a few good years.

    **It is owed at *Rentenbeginn* and at no earlier date.**  That is what *Neue Klassik*
    means, and it is the reason the insurer can hold a materially riskier asset mix behind
    it and generate the surplus that becomes the option budget.  A model that reserves this
    product as though it guaranteed ``i_g`` on the reserve at every balance date overstates
    the guarantee; a model that lets ``guar_cap_pp`` into a death or surrender benefit has
    made the same mistake in the cash flows.  ``av_pp(k) < guar_cap_pp(k)`` at intermediate
    ``k`` is permitted and is ordinary.
    """
    return guar_floor_pp(k) + credit_cum_pp(k)


# --- decrements --------------------------------------------------------------

def mort_rate(t):
    """``q_d(t)``: the **annual** death rate at the attained age of month t.

    A **[std]** Gompertz proxy anchored at ``qx(M, 40) = 0.001200``; DAV 2008 T and DAV
    2004 R are proprietary and are cited by name rather than shipped.  Mortality here is a
    **timing** assumption: the death benefit is the account value with a floor, not a sum
    at risk, so the rate decides when capital leaves and hardly at all how much.

    The **annual** rate, flat across a policy year because the attained age steps on the
    anniversary; :func:`mort_rate_mth` is what the monthly recursion applies.
    """
    return float(data.mort_table().loc[(sex(), age(t)), "qx"])       # noqa: F821


def mort_rate_mth(t):
    """``q^m_d(t)``: the **monthly** death rate, ``1 - (1 - q_d(t))^(1/12)``.

    A **geometric** twelfth and never ``q_d(t) / 12``: twelve of it compound back to the
    year's rate exactly, which is what leaves ``pols_if`` at every anniversary equal to the
    annual-step model's and with it the whole account, the *Höchststandsicherung* ledger and
    every *Indexgutschrift*.  Dividing by twelve would undershoot and leave a cohort that
    never quite runs off.
    """
    q = mort_rate(t)
    if q >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The table surrender rate for period t, **before** the terminal-year override.

    5 % in policy years 1-2 (``k = 0, 1``), 3 % in policy years 3-11, **6 % in policy year
    12** (``k = 11``), 2 % from policy year 13 **[std]**; the table is keyed on the 0-based
    policy year, so the lookup goes through ``duration(t)`` and the twelve months of a year
    all read the same row.  The year-12 step is the § 20 Abs. 1 Nr. 6 EStG threshold, at which only half the
    *Unterschiedsbetrag* becomes taxable and at the personal rate rather than by final
    withholding — the strongest single driver of German surrender behaviour, and the reason
    a rate flat in duration is a numbered pitfall.  The mean over the anchor's 27 years is
    about 2.6 %, inside the market-wide GDV band; no index-specific rate exists at all.
    """
    return float(data.lapse_table().loc[duration(t), "lapse_rate"])  # noqa: F821


def lapse_rate(t):
    """``w_l(t)``: the surrender rate actually applied in period t.

    :func:`lapse_rate_base` except **through the whole final policy year**,
    ``duration(t) == proj_len_y() - 1``, where it is **0** **[std]**: that year ends at
    *Rentenbeginn*, and the whole surviving cohort is booked as a maturity.

    Unlike a term product, where the two paid the same nothing, **here they pay different
    amounts** — a surrender carries the *Stornoabzug* and forfeits the running *Indexjahr*,
    a maturity carries neither and takes the *Beitragsgarantie* floor — so this convention
    moves real money and is a modelling decision rather than bookkeeping.  It is the
    library's convention, shared with ``KLV_DE_S`` and ``RLV_DE_S``, and the monthly grid
    does **not** change it: a within-final-year surrender is now expressible, but no source
    establishes one, and the zero keeps the final-year cohort a single population with a
    single benefit.
    """
    if duration(t) == proj_len_y() - 1:
        return 0.0
    return lapse_rate_base(t)


def lapse_rate_mth(t):
    """``w^m_l(t)``: the **monthly** surrender rate, ``1 - (1 - w_l(t))^(1/12)``.

    A geometric twelfth, for the same reason as :func:`mort_rate_mth`: twelve of it compound
    back to the year's rate, so every anniversary count is the annual-step model's and every
    *Indexgutschrift* is struck on the same population it was.
    """
    w = lapse_rate(t)
    if w >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - w) ** (1.0 / 12.0)


def pols_if(t):
    """``l(t)``: policies in force at time t, the **start** of period t.

    ``pols_if_init()`` at ``t_start()``, then ``pols_if_at(t - 1, "AFT_LAPSE")``, **month by
    month**.  This is the weight on every cash flow of the same ``result_cf()`` row, which is
    what makes it a start-of-month count: no decrement has been applied when a month opens,
    so the frame opens at ``pols_if_init()`` exactly.

    ``pols_if(12k)`` at an anniversary is **bit-identical to the annual-step model's**
    ``pols_if(k)``, because both decrements compound geometrically and the order inside a
    month is the annual model's order inside a year: deaths first, surrenders on the
    survivors of them.  What the finer grid changes is the **split** of a year's exits
    between the two, not their total.

    ``pols_if(proj_len())`` is **zero**, not the surviving cohort: at the end of the last
    month the survivors mature and leave through :func:`pols_maturity`.  Zero outside
    ``t_start() .. proj_len()``.
    """
    if t < t_start() or t > proj_len():
        return 0.0
    if t == t_start():
        return pols_if_init()
    if t == proj_len():
        return 0.0
    return pols_if_at(t - 1, "AFT_LAPSE")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside period t.

    ``"BEF_DECR"``
        ``l(t)``, the start of the month, before any decrement — the same
        number as :func:`pols_if` and the weight on that month's cash flows.

    ``"AFT_DEATH"``
        after the month's deaths, before surrenders.  Death and surrender are
        **sequential and not competing** here: the surrender rate is applied
        to the survivors of death **[std]**, which is the annual model's own
        order taken a twelfth at a time.

    ``"AFT_LAPSE"``
        after both, so ``l(t + 1)`` before any maturity.  Read at the last
        month of a policy year it is :func:`pols_surv_year_end`, the
        population the *Indexjahr* credit is given to; in the final policy
        year the surrender rate is zero, so that is the maturing cohort.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DEATH":
        return pols_if(t) - pols_death(t)
    if timing == "AFT_LAPSE":
        return pols_if_at(t, "AFT_DEATH") - pols_lapse(t)
    raise ValueError("invalid timing")


def pols_death(t):
    """``l(t) q^m_d(t)``: expected deaths in **month** t, claimed at the end of it."""
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Expected surrenders in **month** t, taken from the survivors of the month's deaths.

    Zero through the final policy year, where the survivors leave as maturities instead.
    A surrender in any month of policy year ``k`` is paid ``cv_pp(k)`` and forfeits that
    year's *Indexgutschrift* — the payoff exists only at the *Indexjahr* end — which is the
    behavioural asymmetry the annual grid could state but not date.
    """
    return pols_if_at(t, "AFT_DEATH") * lapse_rate_mth(t)


def pols_maturity(t):
    """The cohort reaching *Rentenbeginn*: the survivors of both decrements at the last month.

    Zero in every other month.  The name is the library's — a count whose cover ends
    at the scheduled end of the contract, whether or not anything is paid for it — and here
    something very much is paid for it.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_if_at(t, "AFT_LAPSE")


# --- benefits ----------------------------------------------------------------

def db_pp(k):
    """``D(k)``: the death benefit per policy in period k.

    ``max(av_pp_at(k, "AFT_GUAR"), death_min_rate() x BS)`` — the account **before** the
    year's index and safe-arm credits, floored at the *Mindesttodesfallschutz* fraction of
    the *Beitragssumme*.

    Two things this is not.  It is **not** a sum at risk: the standard *Todesfallleistung*
    in the *Aufschubphase* of a German deferred annuity is a return of the accumulated
    capital, which is why the *Risikoüberschuss* is small, underwriting is light and the
    three-year suicide exclusion is close to inoperative.  And it carries **no pro-rata
    index credit**: the payoff exists only at the *Indexjahr* end **[std]**, so a death in
    month 7 forfeits it.
    """
    return max(av_pp_at(k, "AFT_GUAR"), death_min_rate() * prem_sum())


def min_surr_pp(k):
    """The § 169 Abs. 3 VVG *Mindestrückkaufswert* per policy in period k.

    ``av_min_pp_at(k, "AFT_GUAR")``: the account with acquisition costs spread evenly over
    the first five contract years, so that an early surrender value cannot be extinguished
    by front-loaded costs.  A floor under the tariff value, not a value in its own right.

    It is a different rule from the DeckRV *Höchstzillmersatz* with a different function —
    the DeckRV governs what may be **reserved**, § 169 VVG what must be **paid** — and
    conflating the two is a numbered pitfall.  With ``zill_years = 5`` they coincide and
    this floor is a no-op.
    """
    return av_min_pp_at(k, "AFT_GUAR")


def surr_charge_pp(k):
    """The *Stornoabzug* deducted from the surrender value in period k.

    2 % of the floored base **[std]**, applied only where the model point carries
    ``surr_charge_on = 1``.  A *Stornoabzug* is effective only if it is agreed, appropriate
    and **quantified in the contract**; one carrier's retrieved structure in the sibling
    research was a 5 % base deduction plus a capital-market-dependent component, and the
    observed band runs from 0 % to 20 %, so 2 % is a deliberately mild **[std]**.
    """
    return (storno_rate * surr_charge_on()                           # noqa: F821
            * max(av_pp_at(k, "AFT_GUAR"), min_surr_pp(k)))


def cv_pp(k):
    """``V(k)``: the surrender value per policy in period k.

    ``max(av_pp_at(k, "AFT_GUAR"), min_surr_pp(k)) - surr_charge_pp(k)``.  A
    **general-account reserve**, not a unit value: locked-in index credits are inside it,
    because by then they are guaranteed capital, while the running *Indexjahr* is not,
    because its payoff is determined only at the year end.

    A behavioural incentive the annual grid quietly assumes away: with no credit in the
    year of exit the product rewards surrendering just **after** an *Indexjahr* ends and
    penalises surrendering just before one, and an annual grid with exits at the year end
    silently gives every surrender the favourable date.
    """
    return max(av_pp_at(k, "AFT_GUAR"), min_surr_pp(k)) - surr_charge_pp(k)


def mat_pp(k):
    """``M(n - 1)``: the benefit per policy at *Rentenbeginn*; zero in every other period.

    ``max(av_pp(n), guar_cap_pp(n))`` — the time-``n`` account **including** the final
    *Indexjahr*'s credits, floored at the *Beitragsgarantie* plus the whole locked-in
    ledger.  It is a flow of the last policy year ``k = n - 1``, whose end is time ``n``,
    paid in the frame's last **month**.  This is the one date at which the guarantee is
    owed, and the only benefit in the model that sees it.

    On the anchor the floor does not bind; on model point 9, whose 100 % guarantee is
    written against a flat index path, it does — and a model with no floor and a model with
    a floor that never binds look identical on every other point.
    """
    if k != proj_len_y() - 1:
        return 0.0
    return max(av_pp(proj_len_y()), guar_cap_pp(proj_len_y()))


def claims(t, kind=None):
    """Benefit outgo in **month** t, by kind; the total when kind is omitted.

    The **counts are monthly and the amounts are annual**, which is the shape of this
    conversion in one cells: a claim is recognised in the month it happens, and what it is
    paid is the policy year's own amount — because the account this product pays out of is
    defined at anniversaries and the *Indexjahr* is settled only at the year end.

    ``"DEATH"``
        ``D(k) x pols_death(t)``, the account before the year's credits with
        the *Mindesttodesfallschutz* floor.

    ``"LAPSE"``
        ``V(k) x pols_lapse(t)``, the § 169 Abs. 3-floored reserve less the
        *Stornoabzug*.  Zero through the final policy year by construction.

    ``"MATURITY"``
        ``M(n - 1) x pols_maturity(12n - 1)``, the capital falling due at
        *Rentenbeginn*, and zero in every other month.

    All three fall at the **end** of the month.  Two exits at the same instant take
    different amounts — the maturity includes the year's *Indexjahr* and the other two do
    not — and that is the product's own rule.
    """
    if kind is None:
        return sum(claims(t, j) for j in ("DEATH", "LAPSE", "MATURITY"))
    if kind == "DEATH":
        return db_pp(duration(t)) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp(duration(t)) * pols_lapse(t)
    if kind == "MATURITY":
        return mat_pp(duration(t)) * pols_maturity(t)
    raise ValueError("invalid kind")


def rentenfaktor():
    """The *Rentenfaktor* applied at *Rentenbeginn*: the **greater** of the two.

    ``max(rentenfaktor_guar, rentenfaktor_curr)`` — a guarantee with upside, the chassis
    rule of the German deferred annuity.  The two are set equal in the base run **[std]**
    so that the max-of-two rule is exercised by a test rather than by the base path.
    """
    return max(rentenfaktor_guar, rentenfaktor_curr)                 # noqa: F821


def ann_monthly_pp():
    """The monthly *Leibrente* the terminal capital buys, per policy; **reported, not paid**.

    ``M(n - 1) / 10,000 x rentenfaktor()`` where the *Kapitalwahlrecht* is not exercised, and
    0.00 where it is.  It is not a cash flow of this model: the *Rentenphase* is a separate
    contract state and a separate model.

    **Neither this number nor the factor behind it is authoritative.**  The factor is a
    **[std]** 25.00 EUR per 10,000 EUR and the mortality it is quoted against is a **[std]**
    period-table proxy, while the real basis is DAV 2004 R, generational in age *and*
    calendar year.  A period proxy priced at a 40-year-old's annuitisation twenty-seven
    years out understates the liability by a margin that dwarfs every other assumption here,
    which is why the model **reports** an annuity and does not compute one.
    """
    if ann_option() != "annuity":
        return 0.0
    return mat_pp(proj_len_y() - 1) / 10000.0 * rentenfaktor()


# --- expenses and the cash flow statement ------------------------------------

def exp_acq_pp(t):
    """The insurer's acquisition expense per policy: 2.5 % of ``BS`` at inception **[std]**.

    Incurred **in full at ``t_start()``** and only for a new-business point — an in-force
    point's acquisition expense was paid before the valuation date.  This is the *Zillmer*
    strain: the insurer pays it at once and recovers it through
    :func:`prem_charge_acq_pp` over five years, and setting the expense equal to the charge
    is what makes the strain visible in ``net_cf`` rather than assumed away.
    """
    if t != t_start() or dur_init() != 0:
        return 0.0
    return acq_expense_rate * prem_sum()                             # noqa: F821


def exp_maint_pp(k):
    """Maintenance expense per policy: 36.00 EUR a year inflating at 1.5 % **[std]**.

    *Stückkosten*, ``exp_fixed_pp x (1 + exp_infl)^k``, inflated from **issue** and not
    from the valuation date — ``k`` is the elapsed policy years, so an in-force point
    carries the inflation its duration has already accumulated.  It is the **year's**
    amount; :func:`expenses` charges a twelfth of it each month, and the inflation factor
    steps on the anniversary because it compounds in policy years.
    """
    return exp_fixed_pp * (1.0 + exp_infl) ** k                      # noqa: F821


def expenses(t):
    """Total insurer expense outgo in **month** t, at the start of it.

    ``(exp_acq_pp(t) + exp_maint_pp(duration(t)) / 12) x l(t)``.  The maintenance level is a
    twelfth of the year's amount rather than a monthly amount of its own, so a year of it on
    a closed cohort is exactly the annual-step model's charge; what the finer grid buys is
    that a policy leaving mid-year bears administration only for the months it was there.
    No claim expense is modelled: no source gives one and it would be immaterial beside a
    benefit that is the account value.

    An **expense**, not a charge: this is the insurer's own cash going out, and it is the
    only expense line in ``net_cf``.  The deductions from the policyholder's account —
    ``prem_charge_acq_pp``, ``prem_charge_adm_pp``, ``av_charge_pp`` — are charges and
    appear nowhere in this cells.
    """
    return (exp_acq_pp(t) + exp_maint_pp(duration(t)) / 12.0) * pols_if(t)


def net_cf(t):
    """The net liability cash flow of period t, **income positive**.

    Premiums less death, surrender and *Rentenbeginn* benefits less expenses — the
    library's sign convention, applied to every model in it.

    The shape to expect is a large first-**month** strain, the acquisition expense falling
    in one lump against the year's premium, then thin positive months while the account
    builds, then a very large negative final month when the whole surviving cohort's capital
    falls due at once.  ``guar_int``, ``surplus_credit``, ``index_credit`` and ``av`` are
    reported beside it and are **not** in it: they are movements of the policyholder's
    account, and they reach the insurer's cash flow only later, through a benefit.
    """
    return (premiums(t) - claims(t, "DEATH") - claims(t, "LAPSE")
            - claims(t, "MATURITY") - expenses(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column beside ``net_cf`` so the sign convention is verifiable
    in the frame rather than only in prose.
    """
    return -net_cf(t)


# --- the published identities ------------------------------------------------

def check_net_cf_resid(t):
    """The cash flow statement's reconciliation residual in **month** t; zero everywhere.

    ``net_cf(t) - [ premiums(t) - claims(t) - expenses(t) ]``, with ``claims(t)`` the
    kind-less total.  :func:`net_cf` names the three kinds one by one while this identity
    takes the total, so the two agree only if the ``claims(t, kind)`` dispatch and the cash
    flow statement carry the **same** list of kinds.

    What it catches is therefore a benefit that exists in the model and not in the
    statement — a fourth kind added to :func:`claims` and forgotten in :func:`net_cf` — and,
    read against ``result_cf()``, the pitfall this product invites above all: adding
    ``guar_int``, ``surplus_credit`` or ``index_credit`` into ``net_cf``.  Those are
    movements of the policyholder's account, not the insurer's cash, and any of them
    entering here would leave a residual the size of the credit.

    delib requires this cells of every model in the library: no model's headline number may
    be reconciled only in prose.
    """
    return net_cf(t) - (premiums(t) - claims(t) - expenses(t))


def check_net_cf():
    """True when the cash flow statement reconciles in every projected month.

    The library-wide form: no argument, one bool over all ``t``;
    :func:`check_net_cf_resid` gives the signed residual of the month that failed.
    """
    return bool(all(abs(check_net_cf_resid(t)) <= roll_fwd_tol       # noqa: F821
                    * max(abs(premiums(t)), abs(claims(t)),
                          abs(expenses(t)), 1.0)
                    for t in range(t_start(), proj_len())))


def check_av_roll_fwd_resid(k):
    """The account roll-forward residual at fund level in policy **year** k; zero everywhere.

    ``av(k + 1) - [ av(k) + prem_to_av(k) - av_charge(k) + guar_int(k) + surplus_credit(k)
    + index_credit(k) - av_released(k) ]``.

    This is the identity the product is most easily got wrong on, because every term is
    struck on a **different population**.  The premium, the charge and the guaranteed
    interest are on the opening in-force, the two credits are on the survivors of both
    decrements, and ``av_released`` carries the balance the exits took with them — at
    ``AFT_GUAR`` for a death or a surrender and at ``AFT_CREDIT`` for a maturity.  Give the
    *Indexjahr* credit to ``pols_if(12k)`` instead of to :func:`pols_surv_year_end` and
    the residual is exactly the credit the leavers should not have had.

    **It is an annual identity and it is stated annually**, one residual per policy year
    rather than one per month: the account of this tariff is defined at anniversaries and
    the *Indexjahr* is settled only at the year end, so a monthly residual for it would
    first have had to invent a monthly account.  That is the error the two-clock split
    exists to make impossible.

    It closes in the final policy year too, where ``av(n)`` is zero and the whole
    balance leaves through the maturity term of :func:`av_released`.
    """
    return av(k + 1) - (av(k) + prem_to_av(k) - av_charge(k) + guar_int(k)
                        + surplus_credit(k) + index_credit(k) - av_released(k))


def check_av_roll_fwd():
    """True when the account roll-forward closes in every projected policy year.

    Tolerance is relative to the balance, the account running to five figures while the
    residual should be zero to machine precision.
    """
    return bool(all(abs(check_av_roll_fwd_resid(k)) <= roll_fwd_tol  # noqa: F821
                    * max(abs(av(k)), 1.0)
                    for k in range(k_start(), proj_len_y())))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in **month** t; zero everywhere.

    ``pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t) - pols_maturity(t)``.
    The recursion applies the two rates in sequence while the three exits are formed
    separately, so the two agree by algebra when — and only when — every one of them is
    read at the same ``t``.  What it catches is a **misindexed recursion**: rolling forward
    with ``w^m_l(t - 1)`` or ``q^m_d(t + 1)``, or applying the surrender rate to the opening
    in-force instead of to the survivors of death.

    In the last month ``pols_if(12n)`` is zero, ``pols_lapse`` is zero and the
    survivors leave through ``pols_maturity``, so the identity closes there as well — and
    that is the month in which an implementation that lets the cohort simply vanish, or that
    double-counts it as both a lapse and a maturity, fails.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the decrements roll forward **and** close over the whole projection.

    Two conditions, not one: the per-year residual above is zero at every ``t``, and the
    three exits summed over the projection account for the whole opening cohort,
    ``sum(deaths + surrenders + maturities) == pols_if_init()``.  The second is the
    stronger statement — it is built by direct summation over the exit cells, with no
    reference to the recursion that produced ``pols_if`` — and it is what catches a life
    that leaves twice or never leaves at all.
    """
    ts = range(t_start(), proj_len())
    closure = sum(pols_death(t) + pols_lapse(t) + pols_maturity(t)
                  for t in ts) - pols_if_init()
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return bool(abs(closure) <= tol
                and all(abs(check_pols_roll_fwd_resid(t)) <= tol for t in ts))


def check_surplus_alloc_resid(k):
    """The surplus-allocation residual in policy **year** k; zero everywhere.

    ``opt_budget_pp(k) + surplus_credit_pp(k) - surplus_rate(k) x index_base_pp(k)``.

    **This is the product's whole economics in one line.**  The year's declared surplus is
    either spent on the option package or credited as interest — never both, and never
    neither.  An implementation that credits the declared rate *and* runs the index
    participation has spent one budget twice, and the result looks entirely plausible until
    this residual is taken: it is exactly the surplus that was double-counted.
    """
    return (opt_budget_pp(k) + surplus_credit_pp(k)
            - surplus_rate(k) * index_base_pp(k))


def check_surplus_alloc():
    """True when the declared surplus is allocated exactly once in every policy year."""
    return bool(all(abs(check_surplus_alloc_resid(k)) <= roll_fwd_tol  # noqa: F821
                    * max(abs(index_base_pp(k)), 1.0)
                    for k in range(k_start(), proj_len_y())))


def check_lock_in_resid(k):
    """The *Höchststandsicherung* violation in policy **year** k; zero when the ratchet holds.

    The sum of three one-sided terms, each zero unless it is breached: the fall in
    ``guar_cap_pp`` from ``k`` to ``k + 1``, a negative *Indexgutschrift*, and a negative
    safe-arm credit.  Negative when the lock-in fails, and its size is the size of the
    breach.

    What it must **not** be is a statement about the account balance.  It is the *credits*
    that ratchet, not ``av_pp``: with the reserve charge at or above the guaranteed rate
    the balance falls in a year that credits nothing, which is ordinary and is model point
    13.  Writing this check on ``av_pp`` would make a correct implementation fail and a
    wrong one — one that let a bad *Indexjahr* claw back a credit — pass.
    """
    return (min(0.0, guar_cap_pp(k + 1) - guar_cap_pp(k))
            + min(0.0, index_credit_pp(k))
            + min(0.0, surplus_credit_pp(k)))


def check_lock_in():
    """True when the guaranteed capital is monotone and no credit is negative."""
    return bool(all(abs(check_lock_in_resid(k)) <= roll_fwd_tol      # noqa: F821
                    * max(abs(guar_cap_pp(k)), 1.0)
                    for k in range(k_start(), proj_len_y())))


def check_index_credit_resid(k):
    """The payoff-bound violation in policy **year** k; zero when the *Indexrendite* is in range.

    ``0 <= rho(k) <= 12 C(k)`` in the Cap design — the year cannot credit less than nothing
    and cannot credit more than twelve capped months — and ``0 <= rho(k) <= q(k) max(Y(k),
    0)`` in the *Partizipationsquote* design.  Returns the sum of the two one-sided
    breaches, so it is zero when both hold and negative otherwise.

    It is the arithmetic guard on the payoff formula itself.  An implementation that floors
    each month at zero stays inside the upper bound and is still wrong, which is why the
    Example B assertions in the product's own test module sit beside this check rather than
    being replaced by it; but one that compounds the capped returns, or that applies the
    Cap to the annual return instead of the monthly one, or that forgets the floor
    altogether, breaks a bound here.
    """
    if payoff_form() == "quote":
        upper = index_quote(k) * max(index_return_year(k), 0.0)
    else:
        upper = 12.0 * index_cap(k)
    return (min(0.0, index_credit_rate(k))
            + min(0.0, upper - index_credit_rate(k)))


def check_index_credit():
    """True when the *Indexrendite* is inside its contractual bounds in every policy year."""
    return bool(all(abs(check_index_credit_resid(k)) <= roll_fwd_tol  # noqa: F821
                    for k in range(k_start(), proj_len_y())))


# --- the result table --------------------------------------------------------

def result_cf():
    """Result table of **monthly** cash flows, indexed by the 0-based policy month t.

    The frame runs ``t = t_start() ... proj_len() - 1``, contiguous, and stops: month
    ``proj_len() - 1`` is the last month of the last policy year and ends at
    *Rentenbeginn*, where the capital falls due as ``claims_maturity``.

    ``pols_if`` is the start-of-month count and the weight on every cash flow of the same
    row, so the first row's value is ``pols_if_init()`` exactly.  ``premiums``,
    ``claims_death``, ``claims_lapse``, ``claims_maturity`` and ``expenses`` are the cash
    flow statement and sum to ``net_cf``; ``liability_cf`` is ``net_cf`` outgo-positive,
    published so the sign convention is verifiable in the frame.

    **The account movements are not here.**  ``guar_int``, ``surplus_credit``,
    ``index_credit`` and ``av`` move once a policy year — the *Indexjahr* is settled at its
    end and nowhere inside it — so they live in :func:`result_index` with the rest of the
    annual state.  They are credits to the policyholder's account that reach the insurer's
    cash flow only later, through a benefit, and summing them into ``net_cf`` is a numbered
    pitfall that :func:`check_net_cf` catches.  :func:`result_cf_annual` sums this frame
    into policy years.
    """
    ts = list(range(t_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by the 1-based ``policy_year``.

    A **regrouping of the monthly frame and never a second projection**: every cash flow
    column is the sum of that policy year's twelve months while ``pols_if`` is the count at
    the year's **start**, which is the only reading under which a count and a flow can share
    a row.  This is the view the technical notes' worked example is stated on.
    """
    df = result_cf()
    years = pd.Index([duration(t) + 1 for t in df.index],            # noqa: F821
                     name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


def result_index():
    """The **annual** state behind the monthly cash flows, indexed by the 1-based policy year.

    Everything on this product that happens once a year, on the anniversary: the *Indexjahr*
    — its Cap, the sum of its twelve capped returns, its raw compounded return and the
    *Indexrendite* the credit is struck at — the option budget and the safe-arm credit
    beside it, the three credits at fund level, the account, the *Höchststandsicherung*
    ledger and the guaranteed capital, and the two per-policy amounts an exit is paid.

    Nothing here changed when the grid did: the account and the *Indexjahr* are annual
    constructions weighted at anniversary counts, so this table is row for row the one the
    annual-step model published.  The twelve monthly returns behind ``index_sum`` are now
    readable off the monthly frame through :func:`index_return_mth` and
    :func:`index_return_capped_mth`.
    """
    ks = list(range(k_start(), proj_len_y()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(12 * k) for k in ks],
            "index_cap": [index_cap(k) for k in ks],
            "index_sum": [index_sum(k) for k in ks],
            "index_return_year": [index_return_year(k) for k in ks],
            "index_credit_rate": [index_credit_rate(k) for k in ks],
            "opt_budget_pp": [opt_budget_pp(k) for k in ks],
            "index_credit_pp": [index_credit_pp(k) for k in ks],
            "surplus_credit_pp": [surplus_credit_pp(k) for k in ks],
            "guar_int": [guar_int(k) for k in ks],
            "surplus_credit": [surplus_credit(k) for k in ks],
            "index_credit": [index_credit(k) for k in ks],
            "av_pp": [av_pp(k) for k in ks],
            "av": [av(k) for k in ks],
            "credit_cum_pp": [credit_cum_pp(k) for k in ks],
            "guar_cap_pp": [guar_cap_pp(k) for k in ks],
            "db_pp": [db_pp(k) for k in ks],
            "cv_pp": [cv_pp(k) for k in ks],
        },
        index=pd.Index([k + 1 for k in ks], name="policy_year"),     # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

acq_cost_rate = 0.025

acq_expense_rate = 0.025

zill_years = 5

zill_cap_rate = 0.025

exp_prem_rate = 0.03

exp_av_rate = 0.0025

exp_fixed_pp = 36.0

exp_infl = 0.015

storno_rate = 0.02

rentenfaktor_guar = 25.0

rentenfaktor_curr = 25.0

roll_fwd_tol = 1e-08

pd = ("Module", "pandas")
