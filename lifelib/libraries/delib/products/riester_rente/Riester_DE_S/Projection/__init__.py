# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Riester_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 11           # or switch the default

.. rubric:: Two clocks, and the argument of a cells says which

The grid is **monthly** and almost everything the contract and the AltZertG state is
annual, so the model runs on two clocks and a cells' argument names the one it is on.

``t`` counts **projection months** from the 1 January 2027 valuation date, 0-based:
``t = 0`` is the first projected month and ``t = proj_len() - 1`` the last, with
``proj_len() = 12 x proj_len_y()``.  It is the argument of the in force, the three
decrements, the claims, the expenses, the commission and the *Rente* instalments —
everything that happens **on a date**.

``k = proj_year(t) = t // 12`` counts **projection years** and is the argument of the
*Eigenbeitrag*, the Zulage and its ZfA lag, the two charges, the declared rate, both
account balances, the *Beitragsgarantie* accumulator and the conversion.  ``k`` is the
annual-step model's own ``t``, so ``result_cf_annual().loc[k]`` is that model's row ``k``.
The contractual contract year is ``duration_y(k) + 1 = duration_init() + k + 1``, which is
``k + 1`` only on a point projected from its own inception (``duration_init() == 0``);
on the anchor, whose contract has run three years, ``k = 0`` is contract year 4.  The
frame is contiguous and uniform on every
model point, including a point that commutes at *Rentenbeginn* and therefore carries zeros
to the end — a uniform frame is what lets two model points be read side by side, and
truncating a commuted point is a listed pitfall.

The decrements carry the library's two speeds: ``mort_rate(t)``, ``lapse_rate(t)`` and
``transfer_rate(t)`` are the **annual** rates of the year the month falls in, and
``mort_rate_mth``, ``lapse_rate_mth`` and ``transfer_rate_mth`` are the geometric twelfths
the recursion applies, so twelve months compound back to each annual rate exactly and
``pols_if(12k)`` is the annual-step model's ``pols_if(k)`` to the last bit.  Everything the
account does is therefore unchanged: the contribution, the Zulage, the two charges, both
balances, the guarantee accumulator, the capital at *Rentenbeginn*, the *Garantielücke* and
the commutation test are **bit-identical** on all thirteen model points.

**What the finer grid buys is the *Rente* and the split of the exits.**  The
*Rentenfaktor* is quoted in euro a **month** and the AltZertG requires a lifelong monthly
benefit; the annual-step model booked twelve instalments together at the start of each
payout year on that year's opening count, which paid a life that died in the first month of
a year for the whole of it.  ``annuity_month_pp()`` is now paid to whoever
:func:`pols_annuity_pay` says is alive that month, which takes 361,74 € off the anchor's
annuity outgo and 573,50 € off model point 12's, whose *Rentengarantiezeit* is zero.  The
*Rentengarantiezeit* itself becomes ``12m`` guaranteed **instalments**.  And the three
accumulation decrements now **compete month by month** where the annual grid ran them in
sequence at one year end — mortality first on the whole cohort, then surrender, then
transfer on what two decrements had already thinned — which moves 5,62 € off the anchor's
death outgo and 2,64 € off its surrender outgo and puts 8,30 € onto its transfers, with the
survivorship at every anniversary unchanged.

**Two phases in one projection.** ``k_conv() = rentenbeginn_age - age(0)`` is the
conversion year and ``t_conv() = 12 x k_conv()`` the conversion month. ``is_accum(t)``
holds for ``t < t_conv()`` and ``is_payout(t)`` for
``t >= t_conv()``, with ``is_accum_y(k)`` and ``is_payout_y(k)`` the annual readings. The
accumulation recursions stop at ``k_conv()``; the lifelong annuity
runs from ``t_conv()`` to ``proj_len() - 1``. A model that stops at *Rentenbeginn* has not
modelled the benefit the AltZertG requires.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/riester_rente/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Riester_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Riester_DE_S.Data`, reached here through the ``data`` Reference:

=========================  =====================================  ==========================
Reference                  Cells                                  File
=========================  =====================================  ==========================
model_point_file           data.model_point_table()               model_point_table.csv
mort_accum_file            data.mort_table_accum()                mort_table_accum.csv
annuity_mort_file          data.annuity_mort_table()              annuity_mort_table.csv
lapse_file                 data.lapse_table()                     lapse_table.csv
zulage_file                data.zulage_schedule()                 zulage_schedule.csv
income_file                data.income_schedule()                 income_schedule.csv
surplus_file               data.surplus_scenario()                surplus_scenario.csv
freq_loading_file          data.freq_loading()                    freq_loading.csv
=========================  =====================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string, ``pols_if_at(t, timing)`` and
``av_total_pp_at(t, timing)`` for the within-year reads, ``prem_to_av_pp`` for the part of
the contribution credited to the account. This model publishes **no** ``av_pp``: delib
spells the *principal* account balance ``av_pp`` and the *verzinsliche Ansammlung* beside
it ``av_sur_pp`` (``RV_DE_S``, the chassis this model inherits the two-balance recursion
from), and the quantity this product's benefits are struck on is neither of them but their
**sum**, so it is named apart as ``av_total_pp``. The technical notes use compact actuarial
symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
(none)                     model_point()                   The selected model point row
n = omega - x(0) + 1       proj_len_y()                    Number of projected years
12 n                       proj_len()                      Number of projected months
k = t // 12                proj_year(t)                    Projection year of month t
(none)                     is_anniv(t)                     Last month of a projection year
(none)                     prem_due(t)                     Month the contribution falls due
T                          k_conv()                        The conversion year
12 T                       t_conv()                        The conversion month
x(k)                       age_y(k)                        Attained age in year k
x(t)                       age(t)                          The same, read from a month
d(k)                       duration_y(k)                   Contract years done at start k
d(t)                       duration(t)                     The same, read from a month
(none)                     duration_mth(t)                 Contract months done
(none)                     contract_year(t)                Contractual 1-based label
tau(k)                     calendar_year_y(k)              Calendar year of year k
tau(t)                     calendar_year(t)                The same, read from a month
(phase)                    is_accum(t), is_payout(t)       Accumulation / payout flag
(phase)                    is_accum_y(k), is_payout_y(k)   The same, on the annual clock
l(t)                       pols_if(t)                      In force at the START of month t
l(0)                       pols_if_init()                  Opening policy count
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / AFT_DECR
q(t)                       mort_rate(t)                    ANNUAL death rate of the year
q_mth(t)                   mort_rate_mth(t)                Its geometric twelfth
(table)                    mort_rate_at_age(x)             Accumulation table rate at x
q(x, tau)                  annuity_mort_rate(x, tau)       Generational annuitant rate
w(t)                       lapse_rate(t)                   ANNUAL surrender rate
w_mth(t)                   lapse_rate_mth(t)               Its geometric twelfth
theta(t)                   transfer_rate(t)                ANNUAL Anbieterwechsel rate
theta_mth(t)               transfer_rate_mth(t)            Its geometric twelfth
(none)                     pols_death(t)                   Expected deaths in month t
(none)                     pols_lapse(t)                   Expected surrenders in month t
(none)                     pols_transfer(t)                Expected transfers out in month t
l(T)                       pols_conv()                     Policies reaching Rentenbeginn
(none)                     pols_annuity_pay(t)             Policies paid an instalment
Y(k)                       income_ref(k)                   Previous year's earnings
Z*(k)                      zulage_entitlement_pp(k)        Full Sec. 84/85 entitlement
Zhat(k)                    zulage_granted_pp(k)            After the Sec. 86 Kuerzung
Z(k)                       zulage_pp(k)                    Zulage CREDITED in year k
(none)                     zulage_cum_pp(k)                Cumulative Zulagen credited
M(k)                       mindesteigenbeitrag_pp(k)       The Sec. 86 minimum
E(k)                       eigenbeitrag_pp(k)              Own contribution, before phi
E(k) phi                   eigenbeitrag_paid_pp(k)         Own contribution, as paid
phi                        prem_freq_load()                Ratenzuschlag multiplier
C(k)                       contrib_total_pp(k)             Total contribution received
K_a(k)                     acq_charge_pp(k)                Acquisition charge
K_v(k)                     admin_charge_pp(k)              Administration charge
S(k)                       prem_to_av_pp(k)                Sparbeitrag; MAY BE NEGATIVE
D(k)                       dk_pp(k)                        Deckungskapital
U(k)                       surplus_acct_pp(k)              Ueberschussguthaben
A(k) = D(k) + U(k)         av_total_pp(k)                  Account value per policy; D + U
A(k), A(k)+S(k), A(k+1)    av_total_pp_at(k, timing)       BEF_PREM / AFT_PREM / AFT_INT
A(k) l(12k)                av_total_at(k, timing)          The same, aggregated
i                          rechnungszins()                 Guaranteed rate
j(k)                       decl_rate(k)                    Declared rate; INCLUDES i
i (D+S)                    int_guar_pp(k)                  Guaranteed interest
(j-i)(D+S) + j U           int_surplus_pp(k)               Declared surplus above it
(none)                     int_credited_pp(k)              Their sum
G(k)                       guar_pp(k)                      Beitragsgarantie accumulator
kappa(k)                   guar_carve_out_pp(k)            Biometric carve-out, 20 % cap
(none)                     garantieluecke_pp(k)            Running shortfall; DIAGNOSTIC
(none)                     pool_gefoerdert_pp(k)           Cumulative subsidised contribs
(none)                     pool_ungefoerdert_pp(k)         Cumulative unsubsidised ones
(none)                     slueb_pp()                      Schlussueberschussanteil
(none)                     bewres_pp()                     Bewertungsreserven share
(none)                     account_conv_pp()               Account at Rentenbeginn
V                          capital_conv_pp()               Conversion capital
Lambda                     garantieluecke_conv_pp()        Garantieluecke the insurer funds
a-double-dot               ann_factor()                    First-order annuity-due factor
R_c                        rentenfaktor_curr()             Current Rentenfaktor
R_g                        rentenfaktor_guar()             Guaranteed Rentenfaktor
R                          rentenfaktor_applied()          max(R_g, R_c)
(none)                     annuity_month_pp()              Monthly instalment per policy
(none)                     is_kleinbetrag()                The commutation test
(none)                     teilkapital_pp()                Teilkapitalauszahlung
(none)                     annuity_capital_pp()            Capital left to annuitise
(none)                     commutation_pp()                Kleinbetragsrenten-Abfindung
a(k)                       annuity_pp(k)                   Annual annuity, 12 instalments
(none)                     db_pp(k)                        Death benefit, gross
(none)                     cv_pp(k)                        Rueckkaufswert, gross
(none)                     transfer_value_pp(k)            Anbieterwechsel transfer value
(none)                     exit_charge_pp(t)               Stornoabzug + transfer charge
(none)                     premiums(t)                     Eigenbeitrag income
(none)                     zulagen(t)                      Zulage income, SEPARATE column
(none)                     int_credited(k)                 Interest credited, REPORTED
(none)                     claims(t, kind)                 Benefit outgo by kind
(none)                     expenses(t)                     Expense outgo
(none)                     commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ==========================

Six names needed care.

``Z*(t)``, ``Zhat(t)`` and ``Z(t)`` are three different quantities and the product turns
on the difference. :func:`zulage_entitlement_pp` is the full § 84/85 entitlement of
contribution year ``k``; :func:`zulage_granted_pp` is that entitlement after the § 86
**proportional** Kürzung, which reduces the subsidy in the ratio of the contribution paid
to the *Mindesteigenbeitrag* rather than withdrawing it; and :func:`zulage_pp` is the cash
**credited** in year ``k``, which the ZfA pays one year in arrear, so it is
``zulage_granted_pp(k - 1)``. Those are **two different lags** — the entitlement looks
back one *calendar* year for income, the cash one *projection* year — and collapsing them
into one is the first listed pitfall. Both are **annual** lags and the monthly grid does not
touch them: the ZfA determines an entitlement per contribution year and pays the provider
once in the following one, which is why :func:`zulagen` is non-zero in one month of twelve.
Note also that ``zulage_pp(k_conv())`` is **not**
zero: the final contribution year's Zulage lands in the conversion year and must be
credited, guaranteed and converted before the guarantee is tested.

``C(k)`` in the notes is the contribution *credited*; :func:`contrib_total_pp` here is the
cash actually **received**, ``eigenbeitrag_paid_pp(k) + zulage_pp(k) + contrib_extra_pp``,
and the *Ratenzuschlag* it carries is deducted back out inside :func:`admin_charge_pp`,
whose percentage base is the **unloaded** ``E + Z + extra``. The notes write ``S = C - K_a
- K_v`` with an unloaded ``C`` and a ``K_v`` that already carries ``E(phi - 1)``, which
deducts the loading twice. The arrangement here deducts it exactly once, which is what
makes :func:`prem_to_av_pp`, :func:`guar_pp` and every benefit **invariant to the payment
frequency** while :func:`premiums` rises by ``E(k)(phi - 1)`` — the property the notes'
pitfall 11 asserts.  It is also why the contribution keeps the **annual** grid on a monthly
frame: φ prices a fractionated mode by loading the amount rather than by moving the
contribution year, so :func:`prem_due` puts the whole year's contribution in the first month
of a projection year whatever ``prem_freq`` says, and a model that both split the cash into
instalments *and* kept φ would charge for the deferral twice.

``S(k)`` **may be negative**, and that is the point of model point 10. The acquisition
charge runs for its five contract years whether or not contributions are paid, so on a
*beitragsfrei* contract the *Sparbeitrag* is negative and the *Deckungskapital* falls.

``D`` and ``U`` are **guarantee accounting, not two investment strategies.** The whole
account grows at the declared ``j(t)``; ``D`` is carved out of it as the part the
*Rechnungszins* guarantees, and ``U`` is the *verzinsliche Ansammlung* of the excess. The
German arithmetic error this prevents is adding the declared *laufende Verzinsung* **to**
the *Rechnungszins*: ``j`` already includes ``i``.

``G(k)`` is an accumulator of **contributions**, never of interest, and it is compared
with the account **exactly once**, at ``k_conv()``. :func:`garantieluecke_pp` is published
at every ``k`` because it is positive in the early durations of any charged contract and a
reader should see that, but it is a **diagnostic**: :func:`db_pp`, :func:`cv_pp` and
:func:`transfer_value_pp` are *not* floored at it, and flooring them is a listed pitfall.

``pols_annuity_pay(t)`` is the whole of the *Rentengarantiezeit*. During the guarantee
period the instalment is paid on ``pols_conv()`` rather than on ``pols_if(t)``, because
payments continue to beneficiaries; afterwards it is paid on the survivors. On this grid the
window is ``12m`` guaranteed **instalments**, which is what the contract says. The guarantee
period changes **who is paid**, never **how much**, so :func:`annuity_pp` does not read
``rentengarantie_years`` at all — and what is paid is :func:`annuity_month_pp`, one
instalment a month, :func:`annuity_pp` being the annual reporting figure it sums to.

.. rubric:: The Zulage is a contribution, not a benefit

It is paid by the *Zentrale Zulagenstelle für Altersvermögen* to the **provider**, credited
to the contract, counted in the *Beitragsgarantie*, invested, and taxed at the end like
any other contribution. It never reaches the saver's bank account. So :func:`zulagen` is a
positive income column of :func:`result_cf`, published **beside** :func:`premiums` and
never folded into it: the separation is the single most important reporting decision in
this model, because a statement that folds the two cannot answer the one question the
product is about. The § 10a *Sonderausgabenabzug* and the *Günstigerprüfung* top-up are
**not** modelled and have no cells, because they are a personal tax matter between the
saver and the tax office and never touch the contract.

.. rubric:: Benefits are gross of the Rückzahlungsbetrag

On a *Kündigung* the provider withholds every Zulage credited and every § 10a relief
granted and remits them to the ZfA. That is a **tax collection, not a reduction in the
insurer's obligation**, so :func:`cv_pp` and :func:`db_pp` are published gross and netting
the *Rückzahlungsbetrag* out of them would understate the outgo. :func:`zulage_cum_pp`
publishes the reclaimable Zulage limb as a diagnostic; the § 10a limb depends on the
saver's marginal rate and cannot be computed from contract data at all, so no cells
attempts it.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — contributions and Zulagen in, benefits, expenses
and commission out — which is the notes' own orientation and the library-wide sign.
:func:`liability_cf` publishes the same stream outgo-positive, ``liability_cf(t) =
-net_cf(t)`` exactly, so a Solvency II best estimate is ``sum v(t) liability_cf(t)`` over
whatever discount curve the valuation layer supplies. Both are columns of
:func:`result_cf`, so the identity is verifiable in the frame rather than only in prose.

``int_credited`` is **reported, not summed into** ``net_cf``: it is money moving inside the
account, not across the insurer's boundary. On the monthly grid it is not a column of
:func:`result_cf` at all — it moves once a *Versicherungsjahr*, like the two balances it
moves between, so it lives in :func:`result_acct` with them.

.. rubric:: What is deliberately not here

No unit-linked fund and no rebalancing algorithm — that chassis is
``products/fondsgebundene_rentenversicherung/``. No *Auszahlungsplan mit Restverrentung*.
No Wohn-Riester in either limb: no *Eigenheimbetrag* withdrawal decrement, no certified
*Darlehen*, no *Wohnförderkonto*, the last because it is a notional tax-bookkeeping account
carrying no cash flow at all. No *Berufsunfähigkeits-Zusatzversicherung* liability — only
the guarantee carve-out its premium creates. No *Versorgungsausgleich*, no surplus in
payment, no policyholder tax of any kind, and no apportionment of investment return between
the subsidised and unsubsidised contribution pools, which a real *Leistungsmitteilung*
must perform. And no *Beitragsfreistellung* **decrement**: it is the dominant exit in the
real German book and it is represented here as a per-model-point switch (``bfs_year``),
because a paid-up policy and a premium-paying one have different account values and
different guarantee accumulators from the moment they diverge, and a scalar
single-model-point projection cannot carry two of each without doubling every recursion.
Model point 10 shows the mechanic on one policy; a book projection needs the cohort split.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
#
# === the model point


def model_point():
    """The selected model point as a Series, indexed by ``point_id``."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def sex():
    """The saver's sex, M or F.  **Reporting only — it must not enter any rate.**

    Riester tariffs have been **unisex** since a 2006 vintage, six years before the
    general unisex rule, so neither the contribution, the decrements nor the
    *Rentenfaktor* may read this cells.  It is carried because the administration records
    it and because its *absence* from every formula is the assertion worth making.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """The attained age at which the contract was concluded, age last birthday.

    With :func:`duration_init` it fixes ``age(0) = issue_age() + duration_init()``, the
    attained age at the valuation date.  It does not otherwise enter the projection: no
    rate in this model is struck at issue.
    """
    return int(model_point()["issue_age"])


def duration_init():
    """Completed contract years at the valuation date; 0 for a point projected from issue.

    It drives three things and each of them matters.  ``duration(t) = duration_init() +
    t`` selects the *Stornoabzug* band and the acquisition-charge window, so an in-force
    point picks up the charge only for the contract years it has left; the expense
    inflation factor runs on contract duration rather than projection year; and the
    acquisition expense and initial commission fall only where ``duration_init() == 0``,
    because on an in-force point they are in the past.
    """
    return int(model_point()["duration_init"])


def pols_if_init():
    """The number of policies the model point represents at the start of period ``t = 0``.

    ``result_cf()``'s first ``pols_if`` value equals this exactly, because no decrement has
    been applied when the first period opens.
    """
    return float(model_point()["pols_if_init"])


def rentenbeginn_age():
    """The attained age at which the payout phase begins.

    Bounded below by the completed 62nd year for a contract concluded from 1 January 2012
    (the completed 60th before that), which is a certification condition of the AltZertG
    rather than a tariff term.  Model point 13 sits at the floor.
    """
    return int(model_point()["rentenbeginn_age"])


def rechnungszins():
    """i: the tariff's guaranteed rate of interest.

    At or below the *Höchstrechnungszins* of the contract's vintage — 0,25 % for the
    2024-vintage anchor, 0,90 % on the older model point 3.  It caps the *reserving* rate
    rather than the rate a policy may guarantee, so a tariff may guarantee less; using the
    cap of the vintage is the highest defensible value and therefore makes the
    *Beitragsgarantie* cheapest.  It is a **model point** attribute rather than a library
    constant because the *Zinszusatzreserve* on the older Riester vintages turns on it.
    """
    return float(model_point()["rechnungszins"])


def beitragssumme():
    """The *Beitragssumme* fixed at conclusion, in euros.

    The base of the acquisition charge and of the initial commission, and nothing else.
    On the ``mindest`` contribution form it is a contractual figure rather than the sum
    the projection actually collects, because the § 86 minimum moves with income.
    """
    return float(model_point()["beitragssumme"])


def contrib_form():
    """The contribution form: ``mindest`` or ``fixed``.

    ``mindest`` recomputes the § 86 *Mindesteigenbeitrag* every year from the previous
    calendar year's earnings, so the contribution rises with income and steps down when a
    *Kinderzulage* stops.  ``fixed`` is a level contractual contribution, which is what a
    *mittelbar* eligible spouse paying the 60 € *Sockelbeitrag* has, and what a saver
    contributing at the § 10a ceiling has.
    """
    v = model_point()["contrib_form"]
    if v not in ("mindest", "fixed"):
        raise ValueError("invalid contrib_form")
    return v


def contrib_fixed_pp():
    """The level own contribution under the ``fixed`` form, per policy per year; 0 otherwise."""
    return float(model_point()["contrib_fixed_pp"])


def contrib_ratio():
    """The fraction of the *Mindesteigenbeitrag* actually paid, on the ``mindest`` form.

    1.00 pays the minimum in full and draws the full Zulagen.  Below 1.00 the § 86 Kürzung
    reduces the **subsidy** in the same proportion — it is not a lapse, not a premium
    holiday and not a cliff edge.  Model point 7 sits at 0.50 and draws exactly half.
    """
    return float(model_point()["contrib_ratio"])


def contrib_extra_pp():
    """Unsubsidised contribution above the § 10a ceiling, per policy per year.

    It enters the account **and** the *Beitragsgarantie*, because the guarantee is on the
    *Altersvorsorgebeiträge* paid in and does not distinguish the pools, but it draws no
    Zulage and it does not enlarge the entitlement.  A single Riester contract can
    therefore carry two tax regimes at once, which is why
    :func:`pool_gefoerdert_pp` and :func:`pool_ungefoerdert_pp` are tracked separately.
    """
    return float(model_point()["contrib_extra_pp"])


def rider_prem_pp():
    """Contribution applied to a biometric rider, per policy per year.

    **Not a cash flow of this model.**  The rider's own liability lives in
    ``products/berufsunfaehigkeit/``; what it does here is create the guarantee carve-out
    of :func:`guar_carve_out_pp`, capped at 20 % of total contributions, which is the
    reason a Riester contract can carry a *Berufsunfähigkeits-Zusatzversicherung* without
    the *Beitragsgarantie* having to reproduce its premiums.
    """
    return float(model_point()["rider_prem_pp"])


def income_id():
    """The key into *income_schedule.csv* naming this policy's earnings path."""
    return model_point()["income_id"]


def income_init():
    """Contribution-liable earnings in the calendar year **before** the projection starts.

    The reference income for ``t = 0``, because the § 86 base is the *previous* year's
    earnings.  Zero for a *mittelbar zulageberechtigt* spouse, whose *Mindesteigenbeitrag*
    is then the 60 € *Sockelbeitrag* floor.
    """
    return float(model_point()["income_init"])


def zulage_id():
    """The key into *zulage_schedule.csv* naming this policy's entitlement drivers."""
    return model_point()["zulage_id"]


def zulage_init_pp():
    """The Zulage credited in period ``t = 0``, earned in the contribution year before it.

    This column exists **only** because the ZfA pays in arrear, so an in-force point opens
    owing one Zulage.  On model point 6 it carries the once-in-a-lifetime 200 €
    *Berufseinsteiger-Bonus* alongside the *Grundzulage*; on a point projected from its own
    inception it is zero, because there is no earlier contribution year.
    """
    return float(model_point()["zulage_init_pp"])


def prem_freq():
    """The payment frequency: annual, half_yearly, quarterly or monthly."""
    v = model_point()["prem_freq"]
    if v not in ("annual", "half_yearly", "quarterly", "monthly"):
        raise ValueError("invalid prem_freq")
    return v


def prem_freq_load():
    """phi: the *Ratenzuschlag* multiplier for this policy's payment frequency.

    Read from *freq_loading.csv*.  A **charge**: the saver pays ``E(t) x phi`` and only
    ``E(t)`` reaches the *Sparbeitrag* base and the *Beitragsgarantie*, so the loading
    enlarges :func:`premiums` and leaves :func:`prem_to_av_pp`, :func:`guar_pp` and every
    benefit untouched.
    """
    return float(data.freq_loading().at[prem_freq(), "load"])        # noqa: F821


def bfs_year():
    """The period index ``t`` from which contributions stop (*Beitragsfreistellung*).

    A **0-based point on the projection's own time axis**, so it is compared directly with
    ``t``; the sentinel for a contract that never goes paid-up is ``-1``, because ``0`` is
    now the first projected period and would mean "paid-up from the outset".

    A **state change, not a termination**: ``pols_if`` is continuous across it, the account
    keeps rolling, the guarantee accumulator freezes once the last Zulage has landed, and
    the acquisition charge keeps biting for its five contract years — which is what drives
    :func:`prem_to_av_pp` negative on model point 10.
    """
    return int(model_point()["bfs_year"])


def dk_pp_init():
    """D(0): the *Deckungskapital* per policy at the valuation date, in euros."""
    return float(model_point()["dk_pp_init"])


def surplus_pp_init():
    """U(0): the *Überschussguthaben* per policy at the valuation date, in euros."""
    return float(model_point()["surplus_pp_init"])


def guar_pp_init():
    """G(0): the *Beitragsgarantie* accumulator per policy at the valuation date.

    The *Altersvorsorgebeiträge* credited before the projection opens — the saver's own
    contributions and the Zulagen actually credited, not the entitlements earned.  On the
    anchor it is **above** the account, so the cell opens with a positive
    :func:`garantieluecke_pp`, which is the normal state of a charged contract in its early
    durations and affects no benefit.
    """
    return float(model_point()["guar_pp_init"])


def teilkapital_share():
    """The elected *Teilkapitalauszahlung*, as a share of the conversion capital.

    Zero to the statutory 0.30.  A lump sum above the cap would be *schädliche Verwendung*
    of the excess; the model does not police the cap, it takes the elected share as a
    contract term and the model point table stays inside it.  There is **no** lump sum on a
    commuted contract: a *Kleinbetragsrenten-Abfindung* is the whole capital in one payment.
    """
    return float(model_point()["teilkapital_share"])


def rentenfaktor_guar():
    """R_g: the guaranteed *Rentenfaktor*, euros of monthly annuity per 10 000 € of capital.

    Struck at inception and contractual thereafter.  It is an **independent contract term**
    rather than a function of the model's own annuity basis, so it and
    :func:`rentenfaktor_curr` can disagree; :func:`rentenfaktor_applied` says which wins.
    """
    return float(model_point()["rentenfaktor_guar"])


def rentengarantie_years():
    """The *Rentengarantiezeit* in years from *Rentenbeginn*; 0 for a pure lifelong annuity.

    It changes **who is paid** — payments continue to beneficiaries — and never **how
    much**.  :func:`annuity_pp` does not read it.
    """
    return int(model_point()["rentengarantie_years"])


def scenario_id():
    """The key into *surplus_scenario.csv* naming this policy's declared-rate path."""
    return model_point()["scenario_id"]


# === the time axis and the two phases


def proj_len_y():
    """n: the **number of projected years**, ``omega_age - age(0) + 1``.

    The annual coordinate of the projection, and the one the contract is written in: the
    contribution, the Zulage, the two charges, the declared rate, both account balances, the
    *Beitragsgarantie* accumulator and the conversion are all annual.  ``k = 0 ...
    proj_len_y() - 1`` indexes exactly the rows the annual-step model this replaced
    projected, which is what makes the two comparable row by row.
    """
    return omega_age - age(0) + 1                                    # noqa: F821


def proj_len():
    """The **number of projected months**, ``12 x proj_len_y()``.

    The frame is ``range(proj_len())``, 0-based, so the last projected index is
    ``proj_len() - 1`` and ``result_cf()`` has exactly ``proj_len()`` rows.  The projection
    runs to the end of the mortality table so that the lifelong annuity is projected to
    exhaustion and the decrement closure identity is exact: in the last projected year the
    attained age is ``omega_age`` and ``mort_rate`` is 1, and :func:`mort_rate_mth` places
    that certainty in the year's **last month**.
    """
    return 12 * proj_len_y()


def k_conv():
    """T: the conversion **year**, ``rentenbeginn_age - age(0)``.

    The boundary between the two phases and the single moment at which the
    *Beitragsgarantie* is tested.  ``is_accum_y(k)`` holds strictly before it; the conversion
    year itself is the first payout year, because the first annuity instalment falls at
    *Rentenbeginn* and the account is extinguished there.
    """
    return rentenbeginn_age() - age(0)


def t_conv():
    """The conversion **month**, ``12 x k_conv()``.

    The last accumulation month is ``t_conv() - 1``; the *Teilkapitalauszahlung*, the
    *Abfindung* and the first monthly annuity instalment are all paid at ``t = t_conv()``.
    """
    return 12 * k_conv()


def proj_year(t):
    """k(t): the 0-based **projection year** month t falls in, ``t // 12``.

    The bridge between the model's two clocks.  ``t`` counts projection **months** from the
    valuation date and is the argument of the in force, the three decrements, the claims,
    the expenses, the commission and the *Rente* instalments; ``k`` counts projection
    **years** and is the argument of everything the contract and the AltZertG state per
    year — the *Eigenbeitrag*, the Zulage and its lag, the two charges, the declared rate,
    both account balances, the *Beitragsgarantie* accumulator and the conversion.

    ``k`` is the annual-step model's own ``t``: ``result_cf_annual().loc[k]`` is that
    model's row ``k``.
    """
    return t // 12


def is_anniv(t):
    """True in the **last** month of a projection year, ``t % 12 == 11``.

    Where everything contractually annual falls: the interest credit, the roll-forward of
    both accounts and of the guarantee accumulator, and the certainty that the terminal year
    kills the last survivor.
    """
    return t % 12 == 11


def prem_due(t):
    """True in the month the year's contribution and Zulage fall due, ``t % 12 == 0``.

    The *Eigenbeitrag*, the unsubsidised contribution and the ZfA's Zulage payment are all
    **annual** events and all fall in the first month of a projection year.  The
    *Ratenzuschlag* is why a fractionated payment mode needs no finer grid than this: a
    German tariff prices monthly or quarterly payment by **loading the amount** through
    :func:`prem_freq_load`, not by moving the contribution year, and the account the
    contribution is credited to is struck per year.  The Zulage is not fractionated at all —
    the ZfA pays the provider once a year.
    """
    return t % 12 == 0


def age_y(k):
    """x(k): attained age last birthday in projection year k.

    ``issue_age() + duration_init() + k``, so ``age_y(0)`` is the attained age at the
    valuation date.  Every rate in the model is indexed by this and never by sex.
    """
    return issue_age() + duration_init() + k


def age(t):
    """x(t): attained age in projection month t, ``age_y(proj_year(t))``.

    The age **steps on the anniversary** and not monthly, so the twelve months of a
    projection year share one annual death rate and one generational annuity rate.
    """
    return age_y(proj_year(t))


def duration_y(k):
    """d(k): completed contract years at the start of projection year k, ``duration_init() + k``.

    The **contract** clock rather than the projection clock, and **0-based**, as lifelib's
    ``duration`` is and as ``Basis_DE_S`` and ``KLV_DE_S`` define it: a point projected from
    its own inception opens at ``duration_y(0) = 0``.  The contractual band label is the
    1-based ``duration_y(k) + 1`` — contract year ``k`` is ``duration_y(k) = k - 1`` — and
    that is the key of *lapse_table.csv*, so the surrender and transfer bands are read at
    ``duration_y(k) + 1``.  It also gates the five-year acquisition charge and drives the
    expense inflation factor, so an in-force point inherits the charge window its contract
    has actually used up.
    """
    return duration_init() + k


def duration(t):
    """d(t): completed contract years at the start of projection month t.

    ``duration_y(proj_year(t))``.  It steps on the anniversary, so the twelve months of a
    projection year share one contract duration and therefore one row of *lapse_table.csv*.
    """
    return duration_y(proj_year(t))


def duration_mth(t):
    """Completed contract **months** at the start of projection month t.

    ``12 x duration_init() + t``.  It is what distinguishes two model points at the same
    projection month, and ``duration(t) = duration_mth(t) // 12`` states in code that the
    contract duration is the contract month divided down.
    """
    return 12 * duration_init() + t


def contract_year(t):
    """The contractual **1-based** contract year label of month t, ``duration(t) + 1``.

    The key of *lapse_table.csv*, published so that a reader never has to decide which of
    the two a table's index means.
    """
    return duration(t) + 1


def calendar_year_y(k):
    """tau(k): the calendar year of projection year k, ``2027 + k``.

    The projection opens at the **1 January 2027** valuation date on every model point, so
    the calendar axis is common across the table.  It enters only the generational annuity
    basis, where ``annuity_mort_rate(x, tau)`` needs both arguments.
    """
    return valuation_year + k                                        # noqa: F821


def calendar_year(t):
    """tau(t): the calendar year of month t, ``calendar_year_y(proj_year(t))``.

    It steps on the policy anniversary rather than on 1 January, which is the convention the
    attained age follows and the one the annual-step model necessarily used.
    """
    return calendar_year_y(proj_year(t))


def is_accum_y(k):
    """True while the contract is accumulating in projection year k: ``k < k_conv()``.

    Contributions, the Zulage credit, the charges, the interest credit and the surrender
    and transfer decrements all live here.  The Zulage credit is the one item that also
    runs **at** ``k_conv()``: the final contribution year's subsidy lands in the conversion
    year, and dropping it silently removes a full year's subsidy from both the account and
    the guarantee.
    """
    return k < k_conv()


def is_accum(t):
    """True while the contract is accumulating in month t: ``t < t_conv()``.

    The monthly reading of :func:`is_accum_y`, and the one the decrements and the claims
    use.  The last accumulation month is ``t_conv() - 1``.
    """
    return t < t_conv()


def is_payout_y(k):
    """True from *Rentenbeginn* onward in projection years: ``k >= k_conv()``."""
    return k >= k_conv()


def is_payout(t):
    """True from *Rentenbeginn* onward: ``t >= t_conv()``.

    The conversion month is the first payout month: the lump sum, the commutation and the
    first monthly annuity instalment are all paid at ``t = t_conv()``.
    """
    return t >= t_conv()


def mort_rate_at_age(x):
    """The accumulation-phase table death rate at attained age x.

    A **[std]** proxy for DAV 2008 T, read from *mort_table_accum.csv* and carrying no
    improvement dimension.  Forced to 1 at ``omega_age`` so the closure identity is exact
    there whatever the table says.
    """
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    return float(data.mort_table_accum().at[x, "qx"])                # noqa: F821


def annuity_mort_rate(x, tau):
    """q(x, tau): the **generational** annuitant death rate at age x in calendar year tau.

    ``qx_base(x) x (1 - improvement(x))^(tau - annuity_base_year)`` from
    *annuity_mort_table.csv*, a **[std]** proxy for DAV 2004 R.  It depends on **both**
    arguments, and that is the property a replacement may not drop: a twenty-year-deferred
    annuitisation happens on the mortality of its own conversion year, and a period-table
    proxy understates it by a margin that dwarfs every other assumption here.  Strictly
    decreasing in ``tau`` below ``omega_age``, where it is forced to 1.
    """
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    tab = data.annuity_mort_table()                                  # noqa: F821
    qb = float(tab.at[x, "qx_base"])
    im = float(tab.at[x, "improvement"])
    return qb * (1.0 - im) ** (tau - annuity_base_year)              # noqa: F821


def mort_rate(t):
    """q(t): the **annual** death rate of the year month t falls in, best-estimate basis.

    The basis **switches at ``t_conv()``**, and the two adjustments run in opposite
    directions because the direction of prudence forks by product.  In accumulation the
    rate is ``mort_rate_at_age(x(t)) x mort_be_factor`` with the factor at 0.80: a
    first-order *death* table assumes mortality higher than expected, so the best estimate
    sits below it.  In payout it is ``annuity_mort_rate(x(t), tau(t)) x
    annuity_mort_be_factor`` with the factor at 1.15: a first-order *annuity* table assumes
    mortality lower than expected, so the best estimate sits above it.  Using one table for
    both phases, or one factor in both directions, is a listed pitfall.

    This is the library's two-speed convention: ``mort_rate`` is the **annual** rate and
    :func:`mort_rate_mth` is what the recursion applies.  The age and the calendar year step
    on the anniversary, so the twelve months of a projection year share one annual rate.
    """
    if age(t) >= omega_age:                                          # noqa: F821
        return 1.0
    if is_accum(t):
        return min(1.0, mort_rate_at_age(age(t)) * mort_be_factor)   # noqa: F821
    return min(1.0, annuity_mort_rate(age(t), calendar_year(t))
               * annuity_mort_be_factor)                             # noqa: F821


def mort_rate_mth(t):
    """The **monthly** death rate applied in month t, ``1 - (1 - mort_rate(t))^(1/12)``.

    The geometric twelfth, so twelve months compound back to the year's annual rate exactly
    and the survivorship at every anniversary is the annual-step model's to the last bit.
    ``mort_rate(t) / 12`` would not close, and the residue it leaves grows with the rate —
    largest exactly where this product's cash flows are, in the tail of a lifelong annuity.

    A rate of **1 is a certainty and is not twelfth-rooted**: at the terminal age the whole
    cohort dies in the year's last month, so the annuity is paid for the whole of that year
    and ``pols_if(proj_len())`` is still zero.
    """
    q = mort_rate(t)
    if q >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def lapse_rate(t):
    """w(t): the **annual** surrender rate of the year month t falls in, by duration.

    Read from *lapse_table.csv* at ``contract_year(t)``, so the twelve months of a
    projection year share one band.  Zero from ``t_conv()``: a contract in payment cannot be
    surrendered.  The level is deliberately small — a *Kündigung* is *schädliche Verwendung*,
    repaying every Zulage and every § 10a relief and taxing the accumulated growth, against a
    surrender value already below the contributions paid in the early years — so the German
    market's description of a Riester contract as economically unsurrenderable is stated
    numerically rather than only in prose.
    """
    if not is_accum(t):
        return 0.0
    return float(data.lapse_table().at[contract_year(t),              # noqa: F821
                                       "lapse_rate"])


def lapse_rate_mth(t):
    """The **monthly** surrender rate applied in month t, the geometric twelfth of ``w(t)``.

    ``1 - (1 - lapse_rate(t))^(1/12)``, so twelve months compound back to the band's annual
    rate exactly and a *Kündigung* is now **dated**: a saver who surrenders in the fourth
    month of a contract year does so in month four of the frame, not at the year end.
    """
    w = lapse_rate(t)
    if w <= 0.0:
        return 0.0
    if w >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - w) ** (1.0 / 12.0)


def transfer_rate(t):
    """theta(t): the **annual** *Anbieterwechsel* rate of the year, from *lapse_table.csv*.

    Set **above** :func:`lapse_rate` at every duration.  The statutory *Wechselrecht* moves
    the capital to another certified contract with no subsidy consequence at all, so it
    dominates surrender for any saver who wants out of the provider but not out of the
    system.  Zero from ``t_conv()``.
    """
    if not is_accum(t):
        return 0.0
    return float(data.lapse_table().at[contract_year(t),              # noqa: F821
                                       "transfer_rate"])


def transfer_rate_mth(t):
    """The **monthly** *Anbieterwechsel* rate applied in month t, the geometric twelfth."""
    th = transfer_rate(t)
    if th <= 0.0:
        return 0.0
    if th >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - th) ** (1.0 / 12.0)


def pols_if(t):
    """l(t): policies in force at the **START** of month t.

    ``pols_if_init()`` at ``t = 0``, then the decrements of the previous month.  This is the
    weight on every cash flow of the same :func:`result_cf` row; end-of-month state is
    reached through :func:`pols_if_at`.  ``pols_if(proj_len())`` — one index beyond the
    frame — is defined and is zero, because ``mort_rate`` is 1 in the terminal year and
    :func:`mort_rate_mth` puts that certainty in its last month; it is read by
    :func:`check_pols_roll_fwd` and by nothing else.

    Because the three monthly rates are geometric twelfths, ``pols_if(12k)`` is the
    annual-step model's ``pols_if(k)`` to the last bit.  What the finer grid changes is not
    the survivorship but the **split** of a year's exits between the three decrements, which
    now compete month by month instead of running in sequence inside one year end.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """Policies in force at a point inside month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement — the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state.  In accumulation that is mortality first, then
        surrender on the survivors of mortality, then transfer on the survivors of both, a
        stated **[std]** ordering — applied now within each **month** rather than once at a
        year end.  In the conversion month of a **commuted** contract it is zero: the
        *Kleinbetragsrenten-Abfindung* discharges the contract outright.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DECR":
        if t < 0 or t >= proj_len():
            return 0.0
        if t == t_conv() and is_kleinbetrag():
            return 0.0
        return (pols_if(t) - pols_death(t) - pols_lapse(t)
                - pols_transfer(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """l(t) q_mth(t): expected deaths in month t, at the end of the month.

    In accumulation the claim is the account value — the **annual** one, struck at the end
    of the contract year, so the month decides when the account is released and not how
    much.  In payout the account is already extinguished, so a death moves :func:`pols_if`
    and pays nothing except through the *Rentengarantiezeit*, which pays the **survivors'
    beneficiaries** rather than the estate.  Zero in the conversion month of a commuted
    contract, where the whole population leaves through the *Abfindung* instead.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == t_conv() and is_kleinbetrag():
        return 0.0
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Expected surrenders in month t, on the survivors of that month's mortality.

    A *Kündigung*: *schädliche Verwendung*, paying :func:`cv_pp` gross of the
    *Rückzahlungsbetrag* the provider withholds and remits.  Zero from ``t_conv()``.
    """
    if not is_accum(t) or t < 0:
        return 0.0
    return pols_if(t) * (1.0 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_transfer(t):
    """Expected *Anbieterwechsel* exits in month t, on the survivors of both prior decrements.

    A **separate decrement from surrender**, not a variant of it: the transfer moves the
    capital to another certified contract at full value less a flat charge, with no
    *Stornoabzug* and no subsidy consequence.  Collapsing the two is a listed pitfall.

    On the monthly grid the three decrements **compete**: in the annual model they ran in
    sequence inside one year end, so mortality took the whole cohort as its base and the
    transfer took what two decrements had already thinned.  Month by month each takes only
    the month's share, which moves exits from the first decrement toward the last while the
    survivorship at every anniversary is unchanged.
    """
    if not is_accum(t) or t < 0:
        return 0.0
    return (pols_if(t) * (1.0 - mort_rate_mth(t)) * (1.0 - lapse_rate_mth(t))
            * transfer_rate_mth(t))


def pols_conv():
    """l(T): the policies that reach *Rentenbeginn* and convert, ``pols_if(t_conv())``.

    Struck once.  It is the count the lump sum, the commutation and — during the
    *Rentengarantiezeit* — the monthly annuity instalment are paid on.
    """
    return pols_if(t_conv())


def pols_annuity_pay(t):
    """The policies a monthly annuity instalment is actually paid on in month t.

    ``pols_conv()`` while ``0 <= t - t_conv() < 12 x rentengarantie_years``, because during
    the *Rentengarantiezeit* the instalment continues to a deceased annuitant's
    beneficiaries; ``pols_if(t)`` afterwards.  Zero before *Rentenbeginn* and zero on a
    commuted contract, which pays no annuity at all.

    On this grid the guarantee window is what the contract says it is — ``12m`` guaranteed
    monthly **instalments** — where the annual grid could only offer ``m`` payments of a
    whole year's annuity each.
    """
    if not is_payout(t) or t >= proj_len() or is_kleinbetrag():
        return 0.0
    if t - t_conv() < 12 * rentengarantie_years():
        return pols_conv()
    return pols_if(t)


def income_ref(k):
    """Y(k): the contribution-liable earnings the § 86 minimum of period k is struck on.

    The **previous calendar year's** earnings — ``income_init()`` at ``k = 0``, otherwise
    ``income(k - 1)`` from *income_schedule.csv*.  This is the first of the model's two
    lags and it is a **calendar** lag; the second, the ZfA payment lag in
    :func:`zulage_pp`, is a **projection** lag.  They are different lags and collapsing
    them into one is the first listed pitfall.  Zero once contributions have ceased.
    """
    if not is_accum_y(k):
        return 0.0
    if k == 0:
        return income_init()
    return float(data.income_schedule().at[(income_id(), k - 1), "income"])  # noqa: F821


def zulage_entitlement_pp(k):
    """Z*(k): the full § 84/85 *Altersvorsorgezulage* entitlement of contribution year k.

    ``grundzulage x unmittelbar + kinderzulage_pre2008 x n_pre + kinderzulage_post2008 x
    n_post + bonus x berufseinsteiger_bonus``, with the drivers read from
    *zulage_schedule.csv*.  The two *Kinderzulage* rates are a permanent **birth-cohort**
    split rather than a transitional rule, so a contract can draw both at once — model
    point 3 draws 175 + 185 + 300 = 660,00 € — and using a single rate is a listed pitfall.
    Zero once contributions have ceased.
    """
    if not is_accum_y(k):
        return 0.0
    row = data.zulage_schedule().loc[(zulage_id(), k)]               # noqa: F821
    return (grundzulage * float(row["unmittelbar"])                  # noqa: F821
            + kinderzulage_pre2008 * float(row["n_kinder_pre2008"])  # noqa: F821
            + kinderzulage_post2008 * float(row["n_kinder_post2008"])  # noqa: F821
            + berufseinsteiger_bonus * float(row["bonus"]))          # noqa: F821


def mindesteigenbeitrag_pp(k):
    """M(k): the § 86 *Mindesteigenbeitrag* of contribution year k.

    ``max(sockelbeitrag, min(mindest_rate x Y(k), foerder_ceiling) - Z*(k))``: 4 % of the
    previous calendar year's contribution-liable earnings, capped at the 2 100 €
    *Sonderausgaben* ceiling, **less** the full entitlement, and floored at the 60 €
    *Sockelbeitrag*.  The floor is what makes the product's economics extraordinary at low
    incomes: on model point 4, 60,00 € of own money draws 775,00 € of Zulagen.  Zero once
    contributions have ceased, which is also the guard that keeps
    :func:`zulage_granted_pp` from dividing by zero.
    """
    if not is_accum_y(k):
        return 0.0
    return max(sockelbeitrag,                                        # noqa: F821
               min(mindest_rate * income_ref(k), foerder_ceiling)    # noqa: F821
               - zulage_entitlement_pp(k))


def eigenbeitrag_pp(k):
    """E(k): the saver's own contribution in period k, **before** the *Ratenzuschlag*.

    ``contrib_ratio() x M(k)`` on the ``mindest`` form and ``contrib_fixed_pp()`` on the
    ``fixed`` one.  Zero from ``bfs_year()`` where that is set, and zero from ``k_conv()``:
    the last contribution year is ``k_conv() - 1``.  This is the amount that reaches the
    *Sparbeitrag* base and the *Beitragsgarantie*; :func:`eigenbeitrag_paid_pp` is what the
    saver actually hands over.
    """
    if not is_accum_y(k):
        return 0.0
    if bfs_year() >= 0 and k >= bfs_year():
        return 0.0
    if contrib_form() == "fixed":
        return contrib_fixed_pp()
    return contrib_ratio() * mindesteigenbeitrag_pp(k)


def eigenbeitrag_paid_pp(k):
    """E(k) phi: the own contribution the saver actually pays, after the *Ratenzuschlag*.

    The loading is a charge, so this is larger than :func:`eigenbeitrag_pp` on any
    non-annual frequency while nothing that touches the account or the guarantee changes.
    """
    return eigenbeitrag_pp(k) * prem_freq_load()


def zulage_granted_pp(k):
    """Zhat(k): the entitlement of contribution year k after the § 86 Kürzung.

    ``Z*(k) x min(1, E(k) / M(k))``.  The sanction for underpaying is **proportional, not a
    cliff edge**: a saver paying half the *Mindesteigenbeitrag* draws half the Zulagen
    rather than none.  Model point 7 sits at exactly that.  Zero where the minimum is zero,
    which is the case once contributions have ceased.
    """
    m = mindesteigenbeitrag_pp(k)
    if m <= 0.0:
        return 0.0
    return zulage_entitlement_pp(k) * min(1.0, eigenbeitrag_pp(k) / m)


def zulage_pp(k):
    """Z(k): the Zulage actually **credited** to the contract in period k.

    ``zulage_init_pp()`` at ``k = 0`` and ``zulage_granted_pp(k - 1)`` thereafter, because the
    ZfA determines the entitlement of a contribution year and pays the provider in the
    following one.  This is the **second** of the model's two lags and it is a *projection*
    lag, not the calendar lag of :func:`income_ref`.

    ``zulage_pp(k_conv())`` is **non-zero**: contributions stop at ``k_conv() - 1`` and the
    Zulage they earned lands in the conversion year, where it must be credited, guaranteed
    and converted before the *Beitragsgarantie* is tested.  It is zero only after that.
    """
    if k < 0 or k > k_conv():
        return 0.0
    if k == 0:
        return zulage_init_pp()
    return zulage_granted_pp(k - zulage_lag)             # noqa: F821


def zulage_cum_pp(k):
    """Cumulative Zulagen credited up to and including period k.

    The ZfA-reclaimable limb of the *Rückzahlungsbetrag* that a *Kündigung* triggers, and a
    **diagnostic only**: it is never netted from a benefit, because the withholding is a
    tax collection the provider performs on the state's behalf and not a reduction in the
    insurer's obligation.  The § 10a limb of the same *Rückzahlungsbetrag* depends on the
    saver's marginal rate and cannot be computed from contract data at all, so no cells
    attempts it.
    """
    if k < 0:
        return 0.0
    if k == 0:
        return zulage_pp(0)
    return zulage_cum_pp(k - 1) + zulage_pp(k)


# === contributions, charges and the Sparbeitrag


def contrib_total_pp(k):
    """C(k): the total contribution **received** in period k, per policy.

    ``eigenbeitrag_paid_pp(k) + zulage_pp(k) + contrib_extra_pp()`` while contributions
    run.  It carries the *Ratenzuschlag*, which :func:`admin_charge_pp` deducts straight
    back out, so the loading is taken exactly once and :func:`prem_to_av_pp` is invariant
    to the payment frequency.  The unsubsidised limb stops with the subsidised one, at
    ``bfs_year()`` or at ``k_conv()``.
    """
    return (eigenbeitrag_paid_pp(k) + zulage_pp(k)
            + (contrib_extra_pp() if (is_accum_y(k) and not
                                      (bfs_year() >= 0 and k >= bfs_year()))
               else 0.0))


def acq_charge_pp(k):
    """K_a(k): the acquisition charge deducted in period k, per policy.

    ``acq_charge_rate x beitragssumme() / acq_charge_years`` in contract years 1 to 5 and
    zero afterwards.  The AltZertG requires acquisition and distribution costs to be spread
    over **at least five years**, which is a materially tighter constraint on *Zillmerung*
    than anything the VVG imposes on a Schicht-3 contract.  The charge runs for its five
    contract years **whether or not contributions are paid**, so on a *beitragsfrei*
    contract it drives :func:`prem_to_av_pp` negative; stopping it at *Beitragsfreistellung*
    is a listed pitfall.
    """
    if k > k_conv() or duration_y(k) >= acq_charge_years:              # noqa: F821
        return 0.0
    return acq_charge_rate * beitragssumme() / acq_charge_years      # noqa: F821


def admin_charge_pp(k):
    """K_v(k): the administration charge deducted in period k, per policy.

    ``admin_charge_prem_rate`` of the contribution credited — **Zulagen included**, which
    is a standardization the German corpus does not settle and which matters most on
    exactly the low-income cells the product was designed for — plus a fixed
    ``admin_charge_fixed`` a year, plus the *Ratenzuschlag* ``E(k)(phi - 1)`` that
    :func:`contrib_total_pp` collected.  The percentage base is the **unloaded**
    contribution, so the loading is neither charged twice nor credited.
    """
    if k > k_conv():
        return 0.0
    base = (eigenbeitrag_pp(k) + zulage_pp(k)
            + (contrib_extra_pp() if (is_accum_y(k) and not
                                      (bfs_year() >= 0 and k >= bfs_year()))
               else 0.0))
    return (admin_charge_prem_rate * base + admin_charge_fixed       # noqa: F821
            + eigenbeitrag_pp(k) * (prem_freq_load() - 1.0))


def prem_to_av_pp(k):
    """S(k): the *Sparbeitrag* — the part of the contribution credited to the account.

    ``contrib_total_pp(k) - acq_charge_pp(k) - admin_charge_pp(k)``.  **It may be
    negative**: the fixed administration charge and the five-year acquisition charge
    continue on a *beitragsfrei* contract with no contribution to meet them, so the
    *Deckungskapital* falls.  That is the mechanic model point 10 exists to show, and it is
    a property of the German cost-spreading rule rather than a modelling artefact.
    """
    if k > k_conv():
        return 0.0
    return contrib_total_pp(k) - acq_charge_pp(k) - admin_charge_pp(k)


# === the account: two balances, one credited rate


def decl_rate(k):
    """j(k): the declared *laufende Verzinsung* of period k, from *surplus_scenario.csv*.

    It **includes** the *Rechnungszins*: ``j - i`` is the *laufende
    Zinsüberschussbeteiligung* and adding the two together is the German arithmetic error
    this model is built to make visible.  Zero from ``k_conv()``, where the account is
    extinguished.  The largest single lever in the model and the least supported — no
    declared rate at any carrier was established, so ``base`` is a round number and ``low``
    is a stress rather than a forecast.
    """
    if not is_accum_y(k):
        return 0.0
    return float(data.surplus_scenario().at[(scenario_id(), k),      # noqa: F821
                                            "decl_rate"])


def int_guar_pp(k):
    """The guaranteed interest credited at the end of period k, ``i x (D(k) + S(k))``.

    Credited on the *Deckungskapital* **plus the year's Sparbeitrag**, so a contribution
    earns a full year's interest in the year it is paid: contributions fall at the start of
    the year and interest at the end of it.
    """
    if not is_accum_y(k):
        return 0.0
    return rechnungszins() * (dk_pp(k) + prem_to_av_pp(k))


def int_surplus_pp(k):
    """The declared surplus above the guaranteed rate, credited at the end of period k.

    ``(j(k) - i) x (D(k) + S(k)) + j(k) x U(k)``.  The *Überschussguthaben* bears the
    **whole** declared rate, because it carries no guarantee to carve out of it; the
    *Deckungskapital* bears only the excess here, having already been credited ``i`` in
    :func:`int_guar_pp`.  Setting ``j = i`` makes the first term vanish, which is the
    check that the two rates are not being added.
    """
    if not is_accum_y(k):
        return 0.0
    return ((decl_rate(k) - rechnungszins())
            * (dk_pp(k) + prem_to_av_pp(k))
            + decl_rate(k) * surplus_acct_pp(k))


def int_credited_pp(k):
    """The total interest credited to the account in period k, per policy.

    ``int_guar_pp(k) + int_surplus_pp(k)``, which equals ``j(k) x (D(k) + S(k) + U(k))``
    exactly — the whole account grows at the declared rate and the split between the two
    legs is guarantee accounting rather than two investment strategies.
    """
    return int_guar_pp(k) + int_surplus_pp(k)


def dk_pp(k):
    """D(k): the *Deckungskapital* per policy at the **start** of period k.

    ``(D(k-1) + S(k-1)) x (1 + i)``: the part of the account the *Rechnungszins*
    guarantees.  Extinguished from ``k_conv() + 1``, where the capital has become an
    annuity.
    """
    if k < 0 or k > k_conv():
        return 0.0
    if k == 0:
        return dk_pp_init()
    return (dk_pp(k - 1) + prem_to_av_pp(k - 1)) * (1.0 + rechnungszins())


def surplus_acct_pp(k):
    """U(k): the *Überschussguthaben* per policy at the start of period k.

    *Verzinsliche Ansammlung*: the declared surplus accrues in a second account beside the
    *Deckungskapital* and bears the declared rate.  Extinguished from ``k_conv() + 1``.
    """
    if k < 0 or k > k_conv():
        return 0.0
    if k == 0:
        return surplus_pp_init()
    return surplus_acct_pp(k - 1) + int_surplus_pp(k - 1)


def av_total_pp(k):
    """A(k) = D(k) + U(k): the total account value per policy at the start of period k.

    The death benefit, the base of the *Rückkaufswert* and of the transfer value, and the
    quantity the *Beitragsgarantie* is compared with at *Rentenbeginn*.  **Zero for
    ``k > k_conv()``**: the account is extinguished at conversion, which is why a death in
    the payout phase pays nothing outside the *Rentengarantiezeit*.

    **Named ``av_total_pp`` and not ``av_pp``.**  Across delib ``av_pp`` is the *principal*
    balance alone — the *Deckungskapital* on ``RV_DE_S``, ``Index_DE_S`` and ``Basis_DE_S``,
    the *Fondsguthaben* on ``FRV_DE_S`` — with the *verzinsliche Ansammlung* beside it as
    ``av_sur_pp``.  This model's two balances are :func:`dk_pp` and :func:`surplus_acct_pp`,
    and what the benefits are struck on is their **sum**, which is a third quantity: giving
    it the name ``av_pp`` would make ``result_cf()``'s account column mean one thing here
    and another on the model this one inherits the recursion from.
    """
    return dk_pp(k) + surplus_acct_pp(k)


def av_total_pp_at(k, timing):
    """The account value per policy at a point inside period k.

    ``"BEF_PREM"``
        A(k), before the year's contribution is credited.

    ``"AFT_PREM"``
        A(k) + S(k), after the *Sparbeitrag* and before interest — the base the year's
        interest is credited on.

    ``"AFT_INT"``
        A(k+1), after interest and before the decrements act.  This is what a death,
        surrender or transfer benefit of period k is struck on, because the decrements act
        at the end of the year after crediting and an exiting policy takes the full year's
        interest.
    """
    if timing == "BEF_PREM":
        return av_total_pp(k)
    if timing == "AFT_PREM":
        return av_total_pp(k) + prem_to_av_pp(k)
    if timing == "AFT_INT":
        return av_total_pp(k + 1)
    raise ValueError("invalid timing")


def av_total_at(k, timing):
    """The aggregate account value inside projection year k.

    ``av_total_pp_at(k, timing) x pols_if(12k)``, weighted on the count at the **start of
    the year**, which is where the contribution is credited and what the account's own
    roll-forward is stated on.  The per-policy balances are annual — one contribution, two
    charges and one interest credit a year — so this is too.
    """
    return av_total_pp_at(k, timing) * pols_if(12 * k)


def guar_carve_out_pp(k):
    """kappa(k): the biometric-rider carve-out from the guarantee in period k.

    ``min(rider_prem_pp(), 0.20 x (E + Z + extra + rider))``.  Contributions used to insure
    reduced earning capacity or a survivor's benefit are excluded from the
    *Beitragserhaltungszusage*, but only up to a share of total contributions, so raising
    ``rider_prem_pp`` past the cap does **not** shrink the guarantee any further.  Model
    point 9 sits exactly at the cap: 400,00 € of rider premium on a 1 200,00 € contribution
    carves out 240,00 € and no more.
    """
    if not is_accum_y(k):
        return 0.0
    extra = (contrib_extra_pp()
             if not (bfs_year() >= 0 and k >= bfs_year()) else 0.0)
    total = eigenbeitrag_pp(k) + zulage_pp(k) + extra + rider_prem_pp()
    return min(rider_prem_pp(), guar_carve_out_cap * total)          # noqa: F821


def guar_pp(k):
    """G(k): the *Beitragsgarantie* accumulator per policy at the start of period k.

    ``G(k+1) = G(k) + E(k) + Z(k) + contrib_extra_pp - kappa(k)`` while ``k <= k_conv()``,
    frozen thereafter.  Three things this encodes.  It counts **Zulagen credited**, in the
    year they are credited, not entitlements in the year they are earned.  It counts
    **unsubsidised** contributions too, because the undertaking is on the
    *Altersvorsorgebeiträge* paid in and does not distinguish the pools.  And it never
    counts interest: the guarantee is nominal.
    """
    if k < 0:
        return 0.0
    if k == 0:
        return guar_pp_init()
    if k - 1 > k_conv():
        return guar_pp(k - 1)
    extra = (contrib_extra_pp() if (is_accum_y(k - 1) and not
                                    (bfs_year() >= 0 and k - 1 >= bfs_year()))
             else 0.0)
    return (guar_pp(k - 1) + eigenbeitrag_pp(k - 1) + zulage_pp(k - 1)
            + extra - guar_carve_out_pp(k - 1))


def garantieluecke_pp(k):
    """The running *Garantielücke*, ``max(0, G(k) - A(k))``.  **A diagnostic.**

    Positive in the early durations of any charged contract — the anchor opens at
    358,94 € — and normally closing later as interest accrues.  The *Beitragsgarantie* is
    tested **once**, at *Rentenbeginn*, so this number affects **no** benefit: flooring
    :func:`db_pp`, :func:`cv_pp` or :func:`transfer_value_pp` at the guarantee is a listed
    pitfall and would misstate every early-duration exit.  It is published so that a reader
    sees the fact rather than infers it.
    """
    return max(0.0, guar_pp(k) - av_total_pp(k))


def pool_gefoerdert_pp(k):
    """Cumulative **subsidised** contributions credited up to period k, per policy.

    The saver's own contribution plus the Zulagen — the money whose benefit is taxed in
    full under § 22 Nr. 5 with no *Ertragsanteil*.  **Contributions only**: the model does
    not apportion investment return between the two pools, which a real
    *Leistungsmitteilung* must do, and says so rather than pretending otherwise.
    """
    if k < 0:
        return 0.0
    add = eigenbeitrag_pp(k) + zulage_pp(k)
    return add if k == 0 else pool_gefoerdert_pp(k - 1) + add


def pool_ungefoerdert_pp(k):
    """Cumulative **unsubsidised** contributions credited up to period k, per policy.

    Money paid into the same contract above the § 10a ceiling.  It enters the account and
    the *Beitragsgarantie* but draws no Zulage, and its benefit falls under the ordinary
    private-annuity rules rather than § 22 Nr. 5 — so a single Riester contract can carry
    two tax regimes at once and the provider must track the pools for the life of the
    contract.  Model point 8 is the cell that exercises it.
    """
    if k < 0:
        return 0.0
    add = (contrib_extra_pp() if (is_accum_y(k) and not
                                  (bfs_year() >= 0 and k >= bfs_year())) else 0.0)
    return add if k == 0 else pool_ungefoerdert_pp(k - 1) + add


# === conversion at Rentenbeginn


def slueb_pp():
    """The *Schlussüberschussanteil* declared at *Rentenbeginn*, per policy.

    ``slueb_rate`` of the contributions credited over the life of the contract, which is
    ``guar_pp(k_conv() + 1)`` where no rider carve-out ran before the valuation date — the
    guarantee accumulator is exactly that sum, opening balance included.  It is **counted
    toward the guarantee**, which is the provider-favourable reading of a question the
    German corpus does not settle; excluding it, and the *Bewertungsreserven* share with
    it, raises the projected guarantee cost by their whole amount.
    """
    return slueb_rate * guar_pp(k_conv() + 1)                        # noqa: F821


def bewres_pp():
    """The *Bewertungsreserven* share allocated at *Rentenbeginn*, per policy.

    ``bewres_rate`` of the account at conversion — the individual entitlement to the
    *hälftige* participation in unrealised gains that § 153 Abs. 3 VVG gives on
    termination.  Like the *Schlussüberschussanteil* it is counted toward the guarantee
    here, and the level is a standardization.
    """
    T = k_conv()
    return bewres_rate * (dk_pp(T) + prem_to_av_pp(T)                # noqa: F821
                          + surplus_acct_pp(T))


def account_conv_pp():
    """The account available at *Rentenbeginn* before the guarantee is applied, per policy.

    ``D(T) + S(T) + U(T) + slueb_pp() + bewres_pp()``.  ``S(T)`` is there because the final
    contribution year's Zulage is credited **in** the conversion year; no interest is
    credited in the conversion year, because the account is converted at the start of it.
    """
    T = k_conv()
    return (dk_pp(T) + prem_to_av_pp(T) + surplus_acct_pp(T)
            + slueb_pp() + bewres_pp())


def capital_conv_pp():
    """V: the capital actually converted at *Rentenbeginn*, per policy.

    ``max(account_conv_pp(), guar_pp(k_conv() + 1))`` — the *Beitragserhaltungszusage*
    applied, once, at the only moment the AltZertG requires it.  Where the account falls
    short the insurer makes up the difference out of its own funds; that difference is
    :func:`garantieluecke_conv_pp`.
    """
    return max(account_conv_pp(), guar_pp(k_conv() + 1))


def garantieluecke_conv_pp():
    """Lambda: the *Garantielücke* the insurer funds at *Rentenbeginn*, per policy.

    ``max(0, guar_pp(k_conv() + 1) - account_conv_pp())``.  **The product's signature
    output**: it is the realised cost of the 100 % *Beitragsgarantie* on this path, and it
    is a *declared-rate* question rather than a *Rechnungszins* question — model point 11
    is the anchor on a 0,50 % declared rate and exists to make that visible.  The
    deterministic path reports it on one scenario; a time-value-of-options-and-guarantees
    calculation would re-evaluate the crediting rule per stochastic scenario, and the two
    scenarios shipped are a sensitivity rather than a distribution.
    """
    return max(0.0, guar_pp(k_conv() + 1) - account_conv_pp())


def ann_factor():
    """a-double-dot: the annuity-due factor at *Rentenbeginn* on the **first-order** basis.

    ``sum_{k>=0} v^k x kp(x(T), tau(T)) - 11/24`` at ``annuity_rechnungszins``, with
    survivorship on the generational annuitant table at factor **1.00** — the basis the
    market's *Rentenfaktor* is struck on — and the Woolhouse ``-11/24`` correction, which
    converts the annual-due factor to a monthly-due one.  The projection's own
    survivorship, by contrast, runs on the **second-order** basis at
    ``annuity_mort_be_factor``; the wedge between the two is the *Risikoüberschuss* in
    payment, which this model does not distribute.

    On the anchor — age 67 in calendar 2044 — it is 20,87222879, and that is the number a
    substitute annuity table must reproduce for the notes' worked example to close.
    """
    v = 1.0 / (1.0 + annuity_rechnungszins)                          # noqa: F821
    x0, tau0 = age_y(k_conv()), calendar_year_y(k_conv())
    total, kp, k = 0.0, 1.0, 0
    while kp > 0.0 and x0 + k <= omega_age:                          # noqa: F821
        total += v ** k * kp
        kp *= 1.0 - annuity_mort_rate(x0 + k, tau0 + k)
        k += 1
    return total - woolhouse                                        # noqa: F821


def rentenfaktor_curr():
    """R_c: the current *Rentenfaktor* implied by the model's own annuity basis.

    ``(1 - rentenfaktor_margin) x 10 000 / (12 x ann_factor())``.  The whole payout-phase
    loading — the *Sicherheitsabschlag* and the administration margin — sits in this one
    deduction rather than being taken partly here and partly out of each instalment, which
    would double-count; the insurer's real payout administration is instead an explicit
    expense cash flow.  On the anchor it is 27,947822, **below** the guaranteed 29,00, so
    the guarantee binds.
    """
    return ((1.0 - rentenfaktor_margin) * 10000.0                    # noqa: F821
            / (12.0 * ann_factor()))


def rentenfaktor_applied():
    """R: the *Rentenfaktor* actually applied, ``max(rentenfaktor_guar(), rentenfaktor_curr())``.

    The German market's own construction: the guaranteed factor is a floor struck at
    inception, and a provider whose current basis has become more generous applies the
    better one.  The two are **independent** — one is a contract term, the other a function
    of the shipped annuity table — so the model states which is authoritative when they
    disagree instead of leaving it to be inferred.
    """
    return max(rentenfaktor_guar(), rentenfaktor_curr())


def annuity_month_pp():
    """The monthly annuity instalment per policy, in euros.

    ``annuity_capital_pp() / 10 000 x rentenfaktor_applied()`` — the *Rentenfaktor* is
    quoted per 10 000 € of capital, which is the German market's convention and the reason
    a factor of 29,00 is a monthly and not an annual amount.  Zero on a commuted contract.
    """
    return annuity_capital_pp() / 10000.0 * rentenfaktor_applied()


def is_kleinbetrag():
    """True where the annuity is small enough to be commuted as a *Kleinbetragsrente*.

    The provider may pay the whole capital as an *Abfindung*, without *schädliche
    Verwendung*, where the monthly annuity would not exceed 1 % of the monthly
    *Bezugsgröße* of § 18 SGB IV.  Two standardizations sit here and both are stated rather
    than buried.  The test is applied to the annuity **actually payable after the elected
    lump sum**, which is the reading that trips *less* often; and the threshold is held
    **flat in nominal terms**, while the *Bezugsgröße* is reset annually — on a
    seventeen-year deferral that **understates** the commutation rate, and the direction of
    the error is said out loud.

    The commutation is **computed, not assumed**: the model tests the annuity it has
    actually produced, so the commutation rate on a book is an output rather than an input.
    Given how much of the German Riester book runs at the *Sockelbeitrag*, that is the right
    way round.
    """
    test = ((1.0 - min(teilkapital_share(), teilkapital_cap))         # noqa: F821
            * capital_conv_pp() / 10000.0
            * rentenfaktor_applied())
    return bool(test <= kleinbetrag_threshold_mth)                   # noqa: F821


def teilkapital_pp():
    """The *Teilkapitalauszahlung* paid at *Rentenbeginn*, per policy.

    ``min(teilkapital_share(), teilkapital_cap) x capital_conv_pp()``: the elected share,
    clamped at the statutory 30 %, taken as a lump sum without losing the subsidy.  A larger
    election would be *schädliche Verwendung* of the excess rather than a bigger lump sum,
    so the model caps it rather than modelling the sanction.  **Zero on a commuted
    contract**: an *Abfindung* is the whole capital in one payment, so there is no lump sum
    beside it.
    """
    if is_kleinbetrag():
        return 0.0
    return min(teilkapital_share(), teilkapital_cap) * capital_conv_pp()  # noqa: F821


def annuity_capital_pp():
    """The capital left to annuitise after the elected lump sum, per policy.

    ``capital_conv_pp() - teilkapital_pp()``, and zero on a commuted contract.  The AltZertG
    requires the remainder after the lump sum to buy a **lifelong** benefit with constant or
    rising payments; a falling annuity is not certifiable and a pure drawdown with no
    lifelong element is not either.
    """
    if is_kleinbetrag():
        return 0.0
    return capital_conv_pp() - teilkapital_pp()


def commutation_pp():
    """The *Kleinbetragsrenten-Abfindung* paid at *Rentenbeginn*, per policy.

    The **whole** conversion capital where :func:`is_kleinbetrag` holds, and zero
    otherwise.  It is *förderunschädlich* — no Zulage is repaid — and since 2018 it is taxed
    under the *Fünftelregelung* of § 34 EStG, which is context rather than a cash flow here
    because this model publishes gross liability flows.
    """
    return capital_conv_pp() if is_kleinbetrag() else 0.0


def annuity_pp(k):
    """a(k): the **annual** annuity per policy in payout year k — twelve monthly instalments.

    ``12 x annuity_month_pp()``, level for life.  It does **not** read
    :func:`rentengarantie_years`: the guarantee period changes who is paid and never how
    much, and a model point with no guarantee period pays the *same* annuity to a smaller
    count.  Zero before *Rentenbeginn* and zero on a commuted contract.

    This is a reporting figure and is nobody's payment: the *Rentenfaktor* is quoted in euro
    a **month**, and :func:`annuity_month_pp` is the instalment that is actually paid.
    """
    if not is_payout_y(k) or k >= proj_len_y() or is_kleinbetrag():
        return 0.0
    return 12.0 * annuity_month_pp()


def db_pp(k):
    """The death benefit per policy in period k, **gross** of the *Rückzahlungsbetrag*.

    The account value after the year's interest, ``av_total_pp_at(k, "AFT_INT")``, so there
    is no sum at risk and no *Risikobeitrag* anywhere in the accumulation.  Zero in payout, the
    account having become an annuity.  It is **not** floored at :func:`guar_pp`: the
    *Beitragsgarantie* is tested at *Rentenbeginn* and nowhere else.  On death without a
    transfer to a surviving spouse's own certified contract the provider withholds the
    Zulagen and the § 10a relief and remits them, but that is a tax collection and netting
    it here would understate the insurer's outgo.
    """
    if not is_accum_y(k):
        return 0.0
    return av_total_pp_at(k, "AFT_INT")


def cv_pp(k):
    """The *Rückkaufswert* per policy in period k, gross of the *Rückzahlungsbetrag*.

    ``av_total_pp_at(k, "AFT_INT") x (1 - stornoabzug_rate)``.  The statutory floor is the
    *Deckungskapital* computed on at least five-year cost spreading, which is satisfied by
    construction here because the acquisition charge is spread over exactly five years.
    Not floored at the guarantee.
    """
    if not is_accum_y(k):
        return 0.0
    return av_total_pp_at(k, "AFT_INT") * (1.0 - stornoabzug_rate)         # noqa: F821


def transfer_value_pp(k):
    """The *Anbieterwechsel* transfer value per policy in period k.

    ``max(0, av_total_pp_at(k, "AFT_INT") - transfer_charge)``: the full account less a flat
    charge, with **no** *Stornoabzug*.  That is the whole economic difference between a
    transfer and a surrender, and collapsing the two into one decrement is a listed
    pitfall — it would apply a percentage charge where a flat one belongs and, far worse,
    would attribute the *schädliche Verwendung* consequences of a *Kündigung* to an exit
    that has none.
    """
    if not is_accum_y(k):
        return 0.0
    return max(0.0, av_total_pp_at(k, "AFT_INT") - transfer_charge)        # noqa: F821


def exit_charge_pp(t):
    """The charge the insurer retains on the month's exits — an **aggregate**, not per policy.

    ``stornoabzug_rate x A(k+1) x pols_lapse(t) + min(transfer_charge, A(k+1)) x
    pols_transfer(t)``, with ``A(k+1)`` the **annual** end-of-year account value every exit
    of that contract year is struck on.  It is the residue that keeps the account
    roll-forward exact: the account released by an exiting policy either leaves as a benefit
    or stays with the insurer as this charge, and :func:`check_av_roll_fwd` closes only when
    both are counted.  The name keeps the ``_pp`` suffix of the notes' own symbol table.
    """
    if not is_accum(t):
        return 0.0
    a = av_total_pp_at(proj_year(t), "AFT_INT")
    return (stornoabzug_rate * a * pols_lapse(t)                     # noqa: F821
            + min(transfer_charge, a) * pols_transfer(t))            # noqa: F821


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total over all six kinds when kind is omitted.

    Every kind is paid in the **month** it falls; the per-policy amounts behind three of
    them are **annual**, struck at the end of the contract year, because that is where the
    account is struck.  So the month decides when a benefit is paid and not how much, and a
    contract year's exits release exactly what the annual-step model released.

    ``"DEATH"``
        the account value paid at the end of the month of death, gross of the
        *Rückzahlungsbetrag*.  Zero in payout.

    ``"LAPSE"``
        the *Rückkaufswert* on a *Kündigung*, net of the *Stornoabzug* and gross of the
        *Rückzahlungsbetrag*.

    ``"TRANSFER"``
        the *Anbieterwechsel* transfer value, a **separate** decrement from surrender with
        no *Stornoabzug* and no subsidy consequence.

    ``"LUMPSUM"``
        the *Teilkapitalauszahlung* at *Rentenbeginn*, on ``pols_conv()``, in the
        conversion **month** only.

    ``"COMMUTATION"``
        the *Kleinbetragsrenten-Abfindung* at *Rentenbeginn*, on ``pols_conv()``, in the
        conversion month only.  A contract pays this **or** a lump sum and an annuity, never
        both.

    ``"ANNUITY"``
        **one** monthly instalment, on ``pols_annuity_pay(t)`` — which is ``pols_conv()``
        inside the *Rentengarantiezeit* and ``pols_if(t)`` afterwards.  The annual-step model
        booked twelve of them together at the start of each payout year on that year's
        opening count, which paid a life that died in the first month of a year for the whole
        of it; that approximation is gone.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "TRANSFER",
                                          "LUMPSUM", "COMMUTATION", "ANNUITY"))
    k = proj_year(t)
    if kind == "DEATH":
        return db_pp(k) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp(k) * pols_lapse(t)
    if kind == "TRANSFER":
        return transfer_value_pp(k) * pols_transfer(t)
    if kind == "LUMPSUM":
        return teilkapital_pp() * pols_conv() if t == t_conv() else 0.0
    if kind == "COMMUTATION":
        return commutation_pp() * pols_conv() if t == t_conv() else 0.0
    if kind == "ANNUITY":
        return annuity_month_pp() * pols_annuity_pay(t)
    raise ValueError("invalid kind")


def premiums(t):
    """The saver's own contribution income in month t, an inflow.

    ``(eigenbeitrag_paid_pp(k) + contrib_extra_pp) x l(t)`` in the month the year's
    contribution falls due and zero in the other eleven: the *Eigenbeitrag* **after**
    the *Ratenzuschlag*, plus any unsubsidised contribution.  It excludes the Zulagen,
    which are :func:`zulagen`, and it excludes ``rider_prem_pp``, which is the biometric
    rider's premium and belongs to the rider's own liability rather than to this one.

    **The contribution keeps the annual grid, and the *Ratenzuschlag* is the reason.** A
    fractionated payment mode is priced by loading the amount — that is what
    :func:`prem_freq_load` is — rather than by moving the contribution year, and the account
    the contribution is credited to is struck per year.  The weight is therefore the count
    at the start of the projection year, which is the annual-step model's own ``l(k)``, and
    this column sums over a year to that model's premium income exactly.
    """
    if not prem_due(t):
        return 0.0
    k = proj_year(t)
    extra = (contrib_extra_pp() if (is_accum_y(k) and not
                                    (bfs_year() >= 0 and k >= bfs_year())) else 0.0)
    return (eigenbeitrag_paid_pp(k) + extra) * pols_if(t)


def zulagen(t):
    """The state *Zulage* income in month t, an inflow: ``zulage_pp(k) x l(t)``, once a year.

    **A contribution with a different payer**, published in its own column and never folded
    into :func:`premiums`.  It is paid by the ZfA to the provider, credited to the
    contract, counted in the *Beitragsgarantie* and invested; it never reaches the saver's
    bank account and it never appears with a negative sign.  On the low-income model points
    it is the **majority** of the contribution, which is the whole economics of the product
    and is invisible in a statement that nets it against the premium.

    The ZfA pays the provider **once a year**, so this is not fractionated on any payment
    mode and falls in the same month as the *Eigenbeitrag*.  ``zulage_pp(k_conv())`` is
    non-zero, so the conversion month carries the last contribution year's subsidy.
    """
    if not prem_due(t):
        return 0.0
    return zulage_pp(proj_year(t)) * pols_if(t)


def int_credited(k):
    """Interest credited to the account in projection year k: ``int_credited_pp(k) x l(12k)``.

    **Reported, not summed into** :func:`net_cf`: it is money moving inside the account,
    not across the insurer's boundary — and on the monthly grid it is not a column of
    :func:`result_cf` at all, because it moves once a *Versicherungsjahr* and belongs with
    the two balances in :func:`result_acct`.  It is published because the account
    roll-forward is unreadable without it and because the guarantee's cost is entirely a
    question of how it compares with the contributions the guarantee accumulates.
    """
    return int_credited_pp(k) * pols_if(12 * k)


def expenses(t):
    """Total expense outgo in month t, excluding commission.

    Four components, all **[std]** because no German insurer publishes a unit cost.  The
    acquisition expense ``expense_acq + expense_acq_rate x beitragssumme()`` at issue, only
    on a point with ``duration_init() == 0``.  A **twelfth** of the annual per-policy
    maintenance ``expense_maint``, inflating at ``expense_infl`` on **contract** duration and
    stepping on the anniversary, on the in-force, in accumulation only.  A twelfth of
    ``expense_annuity`` per annuitant actually paid, in payout.  And ``expense_claim`` per
    death, surrender or transfer, which is a per-**event** cost and so falls whole in the
    month of the event.  The maintenance figure carries the
    Zulage administration — the *Dauerzulageantrag*, the annual data exchange with the ZfA
    and the *Leistungsmitteilung* — which is a real and product-specific cost.

    A policy that exits in the fourth month of a contract year now bears four twelfths of
    that year's maintenance rather than the whole of it.
    """
    total = 0.0
    if t == 0 and duration_init() == 0:
        total += (expense_acq + expense_acq_rate                     # noqa: F821
                  * beitragssumme()) * pols_if(0)
    if is_accum(t):
        total += (expense_maint / 12.0                                # noqa: F821
                  * (1.0 + expense_infl) ** duration(t)              # noqa: F821
                  * pols_if(t))
    total += expense_annuity / 12.0 * pols_annuity_pay(t)            # noqa: F821
    total += expense_claim * (pols_death(t) + pols_lapse(t)          # noqa: F821
                              + pols_transfer(t))
    return total


def commissions(t):
    """Commission outgo in month t **[std]**, published beside :func:`expenses`.

    ``comm_rate_init x beitragssumme()`` at issue on a point written at the valuation date,
    otherwise ``comm_rate_renew`` of the contributions credited — the *Eigenbeitrag* and
    the Zulagen alike, because the provider is remunerated on what it administers.  The
    renewal commission is a percentage of a contribution, so it falls in the month the
    contribution does and in no other.  The initial rate sits at the *Höchstzillmersatz*;
    **the cash leaves at issue while the charge is recovered over five years**, and that gap
    is the new-business strain the insurer carries.  Zero from *Rentenbeginn*.  It is a
    **separate** column from :func:`expenses` and :func:`net_cf` subtracts each exactly once.
    """
    if t == 0 and duration_init() == 0:
        return comm_rate_init * beitragssumme() * pols_if(0)         # noqa: F821
    if not is_accum(t) or not prem_due(t):
        return 0.0
    k = proj_year(t)
    return comm_rate_renew * (eigenbeitrag_pp(k) + zulage_pp(k)) * pols_if(t)  # noqa: F821


def net_cf(t):
    """The net liability cash flow of month t, **income positive**.

    Contributions and Zulagen in, the six kinds of benefit out, expenses and commission
    out.  ``int_credited`` is **not** in it: interest moves money inside the account rather
    than across the insurer's boundary, and it is not even a column of this frame.  The
    notes' own sign and the library-wide one.

    The shape to expect on the monthly frame is a saw-tooth: the whole year's contribution
    and Zulage land in the first month of a projection year and nothing else does, so that
    month is strongly positive and the other eleven carry a twelfth of the maintenance
    expense and the month's exits.  Summed into years by :func:`result_cf_annual` the
    familiar shape returns: a modest positive in accumulation, a very large negative in the
    conversion year as the *Teilkapitalauszahlung* or the *Abfindung* leaves in one payment,
    then a long thin negative tail of monthly annuity instalments.
    """
    return (premiums(t) + zulagen(t)
            - claims(t, "DEATH") - claims(t, "LAPSE") - claims(t, "TRANSFER")
            - claims(t, "LUMPSUM") - claims(t, "COMMUTATION")
            - claims(t, "ANNUITY")
            - expenses(t) - commissions(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column beside :func:`net_cf` so the sign convention is
    verifiable in the frame rather than only in prose.
    """
    return -net_cf(t)


# === the check identities


def check_net_cf_resid(t):
    """The cash flow statement's own reconciliation residual in month t; zero everywhere.

    ``net_cf`` **as published in** :func:`result_cf`, less that same frame's own
    ``premiums + zulagen`` less its six ``claims_*`` columns less ``expenses`` less
    ``commissions`` — every term read **from the frame** rather than from the cells behind
    it, which is what makes this a reconciliation of what the model publishes rather than a
    restatement of :func:`net_cf`'s own expression.

    What it catches is a column that is in the frame but not in the total, or in the total
    twice: dropping ``zulagen`` from the sum, folding ``commissions`` into ``expenses`` and
    subtracting both, or a ``claims_*`` column that has drifted from the kind behind it.
    ``pols_if`` and ``pols_annuity_pay`` are counts and are excluded by construction; the
    interest credit is on the annual clock and is not a column of this frame at all, which
    removes the most tempting way to break the identity.
    """
    row = result_cf().loc[t]
    rebuilt = (row["premiums"] + row["zulagen"]
               - row["claims_death"] - row["claims_lapse"] - row["claims_transfer"]
               - row["claims_lumpsum"] - row["claims_commutation"]
               - row["claims_annuity"]
               - row["expenses"] - row["commissions"])
    return float(row["net_cf"] - rebuilt)


def check_net_cf():
    """True when the cash flow statement reconciles in every projected **month**.

    **delib's first ruling**: every model in this library publishes the identity that
    reconstructs ``net_cf(t)`` from its statement's own published parts, so that the
    headline number of a cash flow model is not the one quantity nothing checks.  No
    argument, one bool over all ``t``; :func:`check_net_cf_resid` gives the signed residual
    of the month that failed.
    """
    return all(abs(check_net_cf_resid(t)) <= roll_fwd_tol            # noqa: F821
               * max(1.0, guar_pp(k_conv() + 1))
               for t in range(proj_len()))


def check_av_roll_fwd_resid(k):
    """The aggregate account roll-forward residual in projection **year** k; zero everywhere.

    The account is an annual construction — one contribution, two charges and one interest
    credit a *Versicherungsjahr* — so its roll-forward is stated per year and this residual
    takes ``k``, not ``t``.  While ``k < k_conv()``: the account at the start of ``k + 1``
    less the account at the start of ``k``, the year's *Sparbeitrag* and the year's credited
    interest, plus the year's three exit benefits and the charge the insurer retained on
    them — each summed over the year's twelve months, because that is where the exits now
    fall.  Every euro that
    leaves the account either becomes a benefit or stays with the insurer as
    :func:`exit_charge_pp`, and omitting the second is the way this identity usually fails
    — the *Stornoabzug* and the transfer charge look like income rather than like account
    released.

    It closes **whatever the split** of the year's exits between death, surrender and
    transfer, because all three release the same annual end-of-year account value; that is
    what lets the monthly grid move the split without touching the account.

    From ``k_conv()`` the identity becomes the assertion that the account is **gone**: the
    residual is ``av_total_pp(k + 1)``, which is zero because conversion extinguishes it.
    """
    if k >= k_conv():
        return av_total_pp(k + 1)
    months = range(12 * k, 12 * k + 12)
    out = sum(claims(t, "DEATH") + claims(t, "LAPSE") + claims(t, "TRANSFER")
              + exit_charge_pp(t) for t in months)
    return (av_total_at(k + 1, "BEF_PREM")
            - (av_total_at(k, "BEF_PREM") + prem_to_av_pp(k) * pols_if(12 * k)
               + int_credited(k) - out))


def check_av_roll_fwd():
    """True when the account rolls forward exactly in every projected year."""
    return all(abs(check_av_roll_fwd_resid(k)) <= roll_fwd_tol       # noqa: F821
               * max(1.0, guar_pp(k_conv() + 1))
               for k in range(proj_len_y()))


def check_guar_roll_fwd_resid(k):
    """The *Beitragsgarantie* accumulator's roll-forward residual in year k; zero everywhere.

    ``G(k+1) - G(k) - E(k) - Z(k) - contrib_extra + kappa(k)`` while ``k <= k_conv()``, and
    ``G(k+1) - G(k)`` afterwards, where the accumulator is frozen.  It catches the three
    ways this accumulator is usually built wrong: adding the entitlement of year ``k``
    rather than the Zulage **credited** in it, adding interest to a guarantee that is
    nominal, and dropping the unsubsidised contribution, which the undertaking covers
    because it is on the *Altersvorsorgebeiträge* paid in and does not distinguish the
    pools.

    Stated per projection **year**, because the accumulator counts contributions and a
    contribution is an annual event; the guarantee is nominal and never accrues, so there is
    nothing for a month to do here.
    """
    if k > k_conv():
        return guar_pp(k + 1) - guar_pp(k)
    extra = (contrib_extra_pp() if (is_accum_y(k) and not
                                    (bfs_year() >= 0 and k >= bfs_year())) else 0.0)
    return (guar_pp(k + 1) - guar_pp(k) - eigenbeitrag_pp(k)
            - zulage_pp(k) - extra + guar_carve_out_pp(k))


def check_guar_roll_fwd():
    """True when the guarantee accumulator rolls forward and the 20 % carve-out cap holds.

    Two conditions, because the second is the one a rider premium breaks silently:
    ``guar_carve_out_pp(k)`` must never exceed ``guar_carve_out_cap`` times the total
    contribution including the rider premium, so raising ``rider_prem_pp`` past the cap
    cannot shrink the guarantee further.  Both are stated per projection **year**: the
    accumulator counts contributions, and a contribution is an annual event.
    """
    ok = all(abs(check_guar_roll_fwd_resid(k)) <= roll_fwd_tol       # noqa: F821
             * max(1.0, guar_pp(k_conv() + 1))
             for k in range(proj_len_y()))
    cap = all(guar_carve_out_pp(k) <= guar_carve_out_cap             # noqa: F821
              * (eigenbeitrag_pp(k) + zulage_pp(k) + contrib_extra_pp()
                 + rider_prem_pp()) + roll_fwd_tol                   # noqa: F821
              for k in range(k_conv()))
    return bool(ok and cap)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``l(t) - l(t+1) - pols_death(t) - pols_lapse(t) - pols_transfer(t)``, less the whole
    converting cohort in the conversion month of a **commuted** contract, where the
    *Kleinbetragsrenten-Abfindung* discharges the contract outright and the population
    leaves through an exit that is not a decrement.  What it catches is a misindexed
    recursion — rolling forward with ``w(t-1)`` or ``q(t+1)`` — a transfer decrement
    that moves ``pols_if`` without being counted, which is how collapsing transfer into
    surrender usually shows up, and a recursion that applied the **annual** rate where the
    monthly one belongs, which would project twelve years of decrement in one.
    """
    commuted = (pols_conv() if (t == t_conv() and is_kleinbetrag()) else 0.0)
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_transfer(t) - commuted)


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes and the whole cohort is accounted for.

    Two conditions.  The per-period recursion above, and the **closure identity**: the
    deaths, surrenders, transfers and any commuted cohort summed over the whole projection,
    plus ``pols_if(proj_len())`` — the one index beyond the frame — equal ``pols_if_init()``.
    The second is built by
    direct summation over the exit cells with no reference to the recursion that produced
    ``pols_if``, so it catches a wrong starting cohort and an exit counted in two places,
    which the telescoping first condition cannot.  ``mort_rate`` is 1 at ``omega_age``, so
    the survivor term is exactly zero and the identity is exact rather than approximate.
    """
    n = proj_len()
    step = all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               * max(pols_if_init(), 1.0)
               for t in range(n))
    exits = sum(pols_death(s) + pols_lapse(s) + pols_transfer(s)
                for s in range(n))
    if is_kleinbetrag():
        exits += pols_conv()
    closure = abs(exits + pols_if(n) - pols_if_init()) <= (
        roll_fwd_tol * max(pols_if_init(), 1.0))                     # noqa: F821
    return bool(step and closure)


def check_conversion_resid(k):
    """The total absolute conversion residual, reported at ``k = k_conv()`` and zero elsewhere.

    Four identities are summed, all of them at the conversion year, because conversion is
    a single event rather than a recursion.  First, the guarantee is applied:
    ``capital_conv_pp() = max(account_conv_pp(), guar_pp(k_conv() + 1))``.  Second, the
    capital is fully disposed of: ``capital_conv_pp() = teilkapital_pp() +
    annuity_capital_pp() + commutation_pp()``, so a commuted contract pays no lump sum
    beside the *Abfindung* and an annuitised one pays no *Abfindung* beside the annuity.
    Third, the current *Rentenfaktor* and the annuity factor are consistent by
    construction: ``rentenfaktor_curr() x 12 x ann_factor() = (1 - rentenfaktor_margin) x
    10 000``, which is the identity that catches a Woolhouse correction applied twice, a
    factor struck on the second-order basis, or a margin taken both in the factor and in the
    instalment.  Fourth, the instalment is the **monthly** one the factor quotes:
    ``12 x annuity_month_pp() = annuity_pp(k)``, so an annual amount cannot reach a monthly
    frame by accident.

    Unlike the other residuals this one is an absolute total rather than a signed
    difference, because the components have different units and there is nothing a
    signed sum of them would mean.  It is annual because the conversion is struck on a
    balance the contract defines per year; the instalments it buys are monthly.
    """
    if k != k_conv():
        return 0.0
    r1 = capital_conv_pp() - max(account_conv_pp(), guar_pp(k_conv() + 1))
    r2 = capital_conv_pp() - (teilkapital_pp() + annuity_capital_pp()
                              + commutation_pp())
    r3 = (rentenfaktor_curr() * 12.0 * ann_factor()
          - (1.0 - rentenfaktor_margin) * 10000.0)                   # noqa: F821
    r4 = 12.0 * annuity_month_pp() - annuity_pp(k)
    return abs(r1) + abs(r2) + abs(r3) + abs(r4)


def check_conversion():
    """True when the conversion at *Rentenbeginn* closes on all four identities."""
    return all(check_conversion_resid(k) <= roll_fwd_tol             # noqa: F821
               * max(1.0, guar_pp(k_conv() + 1))
               for k in range(proj_len_y()))


def check_zulage_lag_resid(k):
    """The Zulage-lag residual in projection year k; zero everywhere.

    ``zulage_pp(k)`` less what the ZfA lag says it must be: ``zulage_init_pp()`` at
    ``k = 0``, ``zulage_granted_pp(k - 1)`` for ``1 <= k <= k_conv()``, and zero after the
    conversion year.  It is the mechanical form of the first listed pitfall — collapsing
    the calendar lag on income and the payment lag on cash into one offset — and of the
    second, dropping the final contribution year's Zulage, which the ``k = k_conv()`` case
    pins down.

    Annual, because the ZfA determines an entitlement per contribution **year** and pays the
    provider once in the following one; the finer grid gives the payment a month, not a
    different lag.
    """
    if k == 0:
        return zulage_pp(0) - zulage_init_pp()
    if k <= k_conv():
        return zulage_pp(k) - zulage_granted_pp(k - 1)
    return zulage_pp(k)


def check_zulage_lag():
    """True when the Zulage is credited one projection year after it is earned, everywhere."""
    return all(abs(check_zulage_lag_resid(k)) <= roll_fwd_tol        # noqa: F821
               * max(1.0, guar_pp(k_conv() + 1))
               for k in range(proj_len_y()))


def result_cf():
    """Result table of cash flows, indexed by projection **month** t, ``0 ... proj_len() - 1``.

    ``pols_if`` is the **start**-of-month count, which is the weight applied to every cash
    flow on the same row, and its first value is ``pols_if_init()`` exactly.
    ``pols_annuity_pay`` is beside it because during the *Rentengarantiezeit* the two
    differ and the annuity is paid on the second.  ``premiums`` and ``zulagen`` are
    **separate** income columns — the Zulage is a contribution with a different payer, and
    folding it into the premium destroys the one number this product is about — and both are
    non-zero in the first month of a projection year and in no other.  The
    six ``claims_*`` columns are the split of ``claims(t, kind)``; there is no bare
    ``claims`` subtotal column, because a statement must not publish a subtotal beside its
    own parts.  ``liability_cf`` is ``net_cf`` outgo-positive.

    **The interest credit is not a column here.**  It moves once a *Versicherungsjahr*, like
    the two balances it moves between, so it lives in :func:`result_acct` with them; a state
    movement in a monthly cash flow statement invites exactly the summation that is a
    category error.  :func:`result_cf_annual` is this frame summed into projection years,
    which is the view the technical notes print.

    The frame is uniform across model points and carries ``proj_len()`` rows on every one
    of them, including a contract commuted at *Rentenbeginn*, which then carries zeros to
    the end rather than being truncated.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_annuity_pay": [pols_annuity_pay(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "zulagen": [zulagen(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_transfer": [claims(t, "TRANSFER") for t in ts],
            "claims_lumpsum": [claims(t, "LUMPSUM") for t in ts],
            "claims_commutation": [claims(t, "COMMUTATION") for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into projection years, indexed by k.

    The twelve cash flow columns are **summed** over each projection year's months and the
    two counts are taken at the year's **start**, which is what they are everywhere else in
    the model.  It is a regrouping of the monthly frame and not a second projection: no
    cells is evaluated on a different basis to produce it.

    Indexed by the projection year ``k``, which is the annual-step model's own ``t``, so
    ``result_cf_annual().loc[k]`` is that model's row ``k`` and the two can be read side by
    side.  The contribution, the Zulage and the commission reproduce it exactly; the split
    of a year's exits between death, surrender and transfer does not, because the three now
    compete month by month, and the annuity and the expenses do not, because both are now
    paid as the months pass.
    """
    ks = list(range(proj_len_y()))
    flows = ["premiums", "zulagen", "claims_death", "claims_lapse", "claims_transfer",
             "claims_lumpsum", "claims_commutation", "claims_annuity", "expenses",
             "commissions", "net_cf", "liability_cf"]
    df = result_cf()
    out = {"pols_if": [pols_if(12 * k) for k in ks],
           "pols_annuity_pay": [pols_annuity_pay(12 * k) for k in ks]}
    for col in flows:
        out[col] = [float(df[col].iloc[12 * k:12 * k + 12].sum()) for k in ks]
    return pd.DataFrame(out, index=pd.Index(ks, name="k"))           # noqa: F821


def result_acct():
    """Result table of the two state variables and the subsidy chain, indexed by year k.

    The model's **annual** view: the account and the guarantee side by side with the
    contribution that drives both, so a reader can follow the *Garantielücke* opening and
    closing.  Every quantity here moves once a *Versicherungsjahr* — one contribution, one
    Zulage, two charges, one interest credit — which is why it is indexed by ``k`` and why
    the interest credit lives here rather than in the monthly cash flow statement.

    ``age`` and ``contract_year`` are published beside them so the annual frame can be read
    without converting; ``mort_rate`` is the year's annual rate and ``mort_rate_mth`` the
    twelfth the recursion applies, printed together because confusing the two is the easiest
    way to break a monthly model of an annual product.  Not part of the cash flow statement
    and not asserted by the conventions suite; it is the frame the technical notes' worked
    example reads its per-policy columns from.
    """
    ks = list(range(proj_len_y()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "age": [age_y(k) for k in ks],
            "contract_year": [duration_y(k) + 1 for k in ks],
            "pols_if": [pols_if(12 * k) for k in ks],
            "mort_rate": [mort_rate(12 * k) for k in ks],
            "mort_rate_mth": [mort_rate_mth(12 * k) for k in ks],
            "income_ref": [income_ref(k) for k in ks],
            "zulage_entitlement_pp": [zulage_entitlement_pp(k) for k in ks],
            "zulage_pp": [zulage_pp(k) for k in ks],
            "mindesteigenbeitrag_pp": [mindesteigenbeitrag_pp(k) for k in ks],
            "eigenbeitrag_pp": [eigenbeitrag_pp(k) for k in ks],
            "acq_charge_pp": [acq_charge_pp(k) for k in ks],
            "admin_charge_pp": [admin_charge_pp(k) for k in ks],
            "prem_to_av_pp": [prem_to_av_pp(k) for k in ks],
            "int_credited_pp": [int_credited_pp(k) for k in ks],
            "int_credited": [int_credited(k) for k in ks],
            "dk_pp": [dk_pp(k) for k in ks],
            "surplus_acct_pp": [surplus_acct_pp(k) for k in ks],
            "av_total_pp": [av_total_pp(k) for k in ks],
            "guar_pp": [guar_pp(k) for k in ks],
            "garantieluecke_pp": [garantieluecke_pp(k) for k in ks],
        },
        index=pd.Index(ks, name="k"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

valuation_year = 2027

omega_age = 110

grundzulage = 175.0

kinderzulage_pre2008 = 185.0

kinderzulage_post2008 = 300.0

berufseinsteiger_bonus = 200.0

mindest_rate = 0.04

foerder_ceiling = 2100.0

sockelbeitrag = 60.0

zulage_lag = 1

acq_charge_rate = 0.025

acq_charge_years = 5

admin_charge_prem_rate = 0.04

admin_charge_fixed = 12.0

guar_carve_out_cap = 0.2

slueb_rate = 0.02

bewres_rate = 0.01

teilkapital_cap = 0.3

kleinbetrag_threshold_mth = 39.55

rentenfaktor_margin = 0.3

annuity_rechnungszins = 0.01

woolhouse = 0.4583333333333333

mort_be_factor = 0.8

annuity_mort_be_factor = 1.15

annuity_base_year = 2027

stornoabzug_rate = 0.02

transfer_charge = 50.0

expense_maint = 30.0

expense_infl = 0.02

expense_annuity = 24.0

expense_claim = 80.0

expense_acq = 150.0

expense_acq_rate = 0.02

comm_rate_init = 0.025

comm_rate_renew = 0.015

roll_fwd_tol = 1e-09

pd = ("Module", "pandas")
