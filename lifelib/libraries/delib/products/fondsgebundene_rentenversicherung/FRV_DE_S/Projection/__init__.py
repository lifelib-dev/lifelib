# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.FRV_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 7            # or switch the default

``t`` counts **policy months from the contract's own inception** and is **0-based**:
``t = 0`` is the inception month, so ``t = 60`` means the same thing on every model point —
the first month after the acquisition-charge instalment ends. The frame runs
``t = proj_start() ... proj_len() - 1`` with ``proj_start() = duration_init_m`` — 0 for new
business, 96 for the in-force cell — and ``proj_len() = 12 x (annuity_age - entry_age)``,
which is the **number** of policy months from inception and so the frame's **exclusive
end**. There is nothing after ``t = proj_len() - 1``: the end of that month is
*Rentenbeginn*, the units are cancelled, the *Fondsguthaben* is converted at the
*Rentenfaktor* and the contract leaves this model. The contractual policy year is the
1-based label ``policy_year(t) = t // 12 + 1``, derived and never indexed by.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/fondsgebundene_rentenversicherung/``, read at run time rather than stored
inside the model. The model folder therefore holds nothing but formulas — no ``_data/``,
no IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FRV_DE_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.FRV_DE_S.Data`, reached here through the ``data`` Reference:

========================  =================================  ==========================
Reference                 Cells                              File
========================  =================================  ==========================
model_point_file          data.model_point_table()           model_point_table.csv
mort_file                 data.mort_table()                  mort_table.csv
lapse_file                data.lapse_table()                 lapse_table.csv
charge_file               data.charge_table()                charge_table.csv
fund_scenario_file        data.fund_scenario_table()         fund_scenario_table.csv
rentenfaktor_file         data.rentenfaktor_table()          rentenfaktor_table.csv
========================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_*`` for the
account value, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase
``kind`` string, ``av_pp_at(t, timing)`` and ``pols_if_at(t, timing)`` for the
within-month reads. Three German terms of art keep their German form in the cells names
too — ``beitragssumme``, ``stornoabzug``, ``rentenfaktor`` — because each names a
quantity with a statutory or contractual definition and no English equivalent that would
not mislead. ``expenses`` is the insurer's own outgo **excluding commission** and
``commissions`` is its own cells and its own :func:`result_cf` column, which is what
``expenses`` means on every delib model that has a commission to publish. The technical
notes use compact actuarial symbols. The mapping is:

=========================  ===============================  =========================
Notes symbol               Cells                            Meaning
=========================  ===============================  =========================
(none)                     model_point()                    The selected model point row
t0                         proj_start()                     duration_init_m (0-based)
n                          proj_len()                       Policy months from inception;
                                                            the frame's exclusive end
y(t)                       policy_year(t)                   t // 12 + 1 (1-based label)
x(t)                       age(t)                           Attained age in month t
S                          beitragssumme()                  Sum of premiums payable
B(t)                       prem_pp(t)                       Gross Beitrag due in month t
Z(t)                       topup_pp(t)                      Zuzahlung in month t
d(t)                       dynamik_factor(t)                Beitragsdynamik factor
alpha(t)                   charge_acq_pp(t)                 Acquisition instalment
(ledger)                   cum_charge_acq_pp(t)             Acquisition charge to date
beta B(t)                  charge_admin_prem_pp(t)          Premium-based admin charge
A(t)                       prem_to_av_pp(t)                 Anlagebeitrag - what buys units
C(t)                       cum_prem_pp(t)                   Cumulative gross premiums paid
p(t)                       unit_price(t)                    Anteilspreis at the END of t
p_open(t)                  unit_price_open(t)               Anteilspreis at the START of t
i(t)                       fund_return_net_mth(t)           Monthly return net of the TER
(scenario)                 fund_return_gross_ann(t)         Gross annual return
(scenario)                 fund_ter_ann(t)                  Fund TER, netted off the return
u(t)                       units_pp(t)                      Units at the START of month t
du(t)                      units_bought_pp(t)               Units bought with A(t)
(cancellations)            units_cancelled_pp(t)            Units cancelled for charges
F(t)                       av_pp(t)                         Fondsguthaben, u(t) p_open(t)
F_tau(t)                   av_pp_at(t, timing)              BEF_CHARGE / AFT_CHARGE /
                                                            AFT_WD / BEF_DECR
(in force)                 av_at(t, timing)                 av_pp_at(t, timing) pols_if(t)
gamma_m                    gamma_rate_mth()                 gamma_rate_ann() / 12
gamma_m F(t)               charge_admin_fund_pp(t)          Fund-based admin charge
SK                         charge_policy_fee_pp(t)          Stueckkosten
W(t)                       withdrawals_pp(t)                Teilentnahme
D(t)                       db_floor_pp(t)                   Guaranteed minimum death benefit
K(t)                       nar_pp(t)                        Riskiertes Kapital
(none)                     db_pp(t)                         What a death claim actually pays
q_I(t)                     mort_rate_tariff_mth(t)          First-order monthly death rate
q(t)                       mort_rate_mth(t)                 Second-order monthly death rate
f                          mort_be_factor                   0.75; q(t) = f q_I(t)
(table)                    lapse_rate_base(t)               Table lapse rate
(tax)                      lapse_tax_step(t)                x 2.5 in the threshold year
w(t)                       lapse_rate_mth(t)                Monthly lapse rate; w(n-1) = 0
l(t)                       pols_if(t)                       In force at the START of month t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)            BEF_DECR / AFT_DEATH / AFT_DECR
sigma                      stornoabzug_rate()               Stornoabzug rate
R_g, R_c, R                rentenfaktor_guar(),             Euro of monthly annuity per
                           rentenfaktor_curr(),             10 000 EUR of Fondsguthaben
                           rentenfaktor_applied()
(none)                     av_maturity_pp()                 Fondsguthaben at Rentenbeginn
(none)                     annuity_mth_pp()                 The monthly annuity it buys
net_cf(t)                  net_cf(t)                        Non-unit cash flow, income positive
liability_cf(t)            liability_cf(t)                  The same stream, outgo positive
=========================  ===============================  =========================

.. rubric:: net_cf is the non-unit stream

This is the convention everything else hangs on. Every benefit this contract pays before
*Rentenbeginn* is funded by cancelling the policyholder's **own** units, so a gross
presentation would count the same money twice::

    net_cf(t) = charge_acq(t) + charge_admin_prem(t) + charge_admin_fund(t)
                + charge_policy_fee(t) + charge_risk(t) + stornoabzug(t)
                - expenses(t) - commissions(t) - death_strain(t)

Charges in, expenses, commission and the death strain out. ``expenses`` **excludes**
commission, which is :func:`commissions` and its own :func:`result_cf` column: that is the
library-wide split, stated on ``KLV_DE_S``, ``Basis_DE_S``, ``Riester_DE_S`` and
``RLV_DE_S`` too, and the opposite of the frlib chassis, where commission sits inside the
expense total. Whichever convention a model takes, taking both at once double-counts the
commission.

The **death strain** is the whole of the insurer's cost per death: the death benefit is
observed *before* that month's *Risikobeitrag*, so what the insurer funds out of its own
pocket is exactly the *riskiertes Kapital* ``nar_pp(t)`` and nothing else. Everything that
moves through the unit fund — ``premiums``, ``prem_to_av``, ``claims_death``, ``claims_lapse``,
``claims_maturity``, ``withdrawals``, ``av_releases`` — is published as a
:func:`result_cf` column and is **excluded** from ``net_cf``, and
:func:`check_benefit_funding` asserts that those columns net exactly::

    claims_death + claims_lapse + claims_maturity + withdrawals + stornoabzug
        = av_releases + death_strain

Booking the whole *Fondsguthaben* as an insurer outgo is the first-order failure mode of
a unit-linked liability model, and it is the reason the gross columns are published
rather than dropped: a reader can see what was excluded.

The fund's **TER** is a third category again. It never leaves the *Anteilspreis*, so it
appears nowhere in the ledger and is netted off the assumed gross return instead.
Charging it explicitly double-counts; ignoring it overstates the policyholder's return.

.. rubric:: Withheld from the premium, or cancelled out of the fund

The *Beitragsverrechnung* withholds the acquisition instalment and the premium-based
administration charge **before** units are bought::

    A(t) = B(t) + Z(t) - alpha(t) - beta B(t)        then  du(t) = A(t) / p_open(t)

while the fund-based administration charge, the *Stückkosten* and the *Risikobeitrag* are
levied **after** the month's return, by cancelling units that already exist. The
distinction is not cosmetic and it is the model's most easily-hidden error: a model that
nets the fund-based charge out of the *Beitrag* gives the right answer while premiums are
paid and the wrong answer the moment they stop. Model point 7 goes *beitragsfrei* at
``t = 120`` on a zero-return fund; from there ``premiums(t)`` is zero while
``charge_admin_fund(t)`` and ``charge_policy_fee(t)`` continue, and the fund decays. That
decay is the product fact § 165 VVG makes possible, not a modelling artefact.

:func:`check_units_roll_fwd` and :func:`check_av_roll_fwd` look redundant and are not.
The unit identity has **no price term at all** — ``u(t+1) = u(t) + du(t) - cancelled(t)``
— so it fails if a charge is taken in euro without cancelling the matching units. The
account identity carries the return and fails if the price is applied at the wrong point
in the month. An implementation can pass either one alone.

.. rubric:: Two mortality bases, and the wedge between them

The *Risikobeitrag* is priced on a **death** table, the first-order DAV 2008 T proxy in
``mort_table.csv``, read through :func:`mort_rate_tariff_at_age`. The projection
decrements on the **second-order** best estimate, ``mort_be_factor = 0.75`` times it. The
difference is the *Risikoergebnis*, and because the factor is flat it is exactly
``(1 - 0.75) = 25 %`` of the *Risikobeitrag* collected — a closed-form check a reader can
do with a calculator, and the reason the ratio is flat rather than age-varying. A model
that uses one basis for both makes the risk result identically zero and deletes the
mechanic.

The conversion guarantee rests on a **third** basis, an annuity table (DAV 2004 R),
reached through :func:`rentenfaktor_guar` and ``rentenfaktor_table.csv``. **No cells
reads both files**, which is the arithmetic form of the statement that a German
fondsgebundene contract carries two mortality bases at once.

The two monthly conversions are deliberately different, and mixing them is a listed
pitfall. Mortality is split **linearly**, ``mort_rate_mth = mort_rate / 12``, because the
tariff's own *Risikobeitrag* is ``q(x)/12`` times the *riskiertes Kapital* and the charge
and the decrement must rest on the same split or the model manufactures a risk result out
of a rounding convention. Lapse is split **geometrically**, ``1 - (1 - lapse_rate)^(1/12)``,
because nothing is priced off it and the annual rate is the observable to reproduce. The
fund **return** is compounded geometrically for the same reason the lapse rate is: it is
an effective annual rate, while a German tariff's charge rates are nominal.

.. rubric:: The acquisition charge, its window, and the in-force cell

``charge_acq_total() = alpha_rate x beitragssumme()`` — 2.50 % of the sum of premiums
**payable**, which is the *Höchstzillmersatz* — spread in equal instalments over
``acq_window_months() = min(alpha_spread_months, 12 x prem_term_y)`` months at the
policy's own premium frequency. On the anchor cell that is 1 800,00 € over 60 monthly
instalments of 30,00 €, which is **15 % of each of the first 60 premiums, ``t = 0 ... 59``,
and nothing from ``t = 60``**. On model point 12, whose premium term is two years, the
window is 24 months
and the instalment count is 24, not 60; on the quarterly, half-yearly and annual cells it
is 20, 10 and 5 instalments of the corresponding size.

``beitragssumme()`` is the sum of premiums **payable at the initial level**. It does not
shrink when a contract lapses or goes *beitragsfrei*, and it does not grow with a
*Beitragsdynamik* increment — a real tariff re-zillmers each accepted increment over its
own sixty months, and an increment cannot be assumed at inception. The bias that leaves,
an understated acquisition charge on a dynamic contract, is stated rather than hidden.

An **in-force** model point opens after the window has closed. Model point 6 starts at
``t = 96``, so ``charge_acq(t)`` is zero at every projected month **and**
``commissions(96)`` carries no *Abschlussprovision*: the acquisition commission and the
issue expense fall at ``t = 0`` and only there, and ``t = 0`` is not in that model point's
frame. That is the whole of the difference between an in-force cell and a new-business one
on this chassis.

.. rubric:: The Beitragsrückgewähr, and why cum_prem_pp is a state variable

On the composite death benefit the floor is the **premiums paid**, so the net amount at
risk is ``max(C(t) - F(t), 0)`` — positive early and after a market fall, vanishing once
the fund overtakes the premiums paid. That makes ``cum_prem_pp`` a genuine state variable
of this product rather than a reporting convenience, and it makes the risk charge a
quantity that has to be recomputed every month. ``C(t)`` is the premiums **paid**, gross:
on the anchor cell ``cum_prem_pp(59) = 12 000,00 €`` against ``sum of prem_to_av_pp`` over
the same months of 9 720,00 €, so reading the floor off the premiums *invested* would
understate the death benefit by 19 %.

The floor is chosen by ``db_form``: ``fund`` gives no floor and therefore no
*Risikobeitrag* at all (model points 2 and 13); ``prem_return`` is the composite;
``pct_fund`` is a multiple of the fund, so the net amount at risk grows with it; and
``sum_assured`` is a fixed *garantierte Mindesttodesfallleistung*, which on a decaying
paid-up fund makes the risk charge grow without limit — model point 7 exists to show
that. The floor at zero in :func:`nar_pp` is not decoration: without it the contract
would pay the insurer a negative charge in every month the fund is above the floor and
the death strain would turn negative, silently booking the fund's growth as insurance
profit.

.. rubric:: The Rückkaufswert is the Fondsguthaben

§ 169 VVG sends a fondsgebundene contract to the *Zeitwert*, and on a pure unit-linked
contract with no insurer-given guarantee the *Zeitwert* **is** the *Fondsguthaben*. There
is no discounting, no *Rechnungszins*, no mortality basis, no *Zillmerung* residue and no
second-basis *Mindestrückkaufswert* anywhere in this model — the protection for the
policyholder sits earlier, in the sixty-month spreading of the acquisition charge, which
is why the surrender value is positive from the first month. A *Stornoabzug* is
permissible only if agreed, quantified and appropriate, and **never for unamortised
acquisition costs**: ``stornoabzug_pp(t)`` is therefore a flat rate on the
*Fondsguthaben* and is deliberately **not** a function of
``charge_acq_total() - cum_charge_acq_pp(t)``. Only ``std_high`` carries a non-zero rate,
and only model point 5 uses it.

.. rubric:: The last month, and the age at Rentenbeginn

``lapse_rate_mth(proj_len() - 1) = 0``. The end of the last projected month is
*Rentenbeginn*, so a surrender and an annuitisation are the same event releasing the same
*Fondsguthaben*, and the whole surviving cohort is booked as ``pols_maturity``. No cash
flow moves either way; the convention only decides the split between the lapse total and
the maturity count, and it is what the closure identity reproduces. It is frlib's
convention on ``TD_FR_S`` and delib adopts it.

``age(proj_len() - 1) = annuity_age - 1``, because the annuity begins at the **end** of
that month. The *Rentenfaktor* is read at ``annuity_age`` and not at ``age(proj_len() -
1)``: on
the anchor cell 25.00 at 67, not the 24.45 an off-by-one would fetch at 66. The rule
applied is ``max(guaranteed, current)`` — a guarantee **with upside**, so a model that
applies only the guaranteed factor understates the benefit whenever the current tariff is
richer. On ``std_2026`` the two are equal, so the ``max()`` is exercised without injecting
an unsourced uplift; model point 13 carries ``rich_current``, where the current factor is
12 % higher and the ``max()`` visibly bites.

.. rubric:: The reduction in yield

:func:`reduction_in_yield` is the product's defining metric, because on a contract with
no *Rechnungszins* the charge stack **is** the economics. It is the reference gross return
less the internal rate of return the policyholder's own money actually earns, computed on
a **single persisting contract** — no survivorship, no lapse — because a reduction in
yield is a statement about one policy.

**It is a delib-defined measure and it is not the statutory *Effektivkostenquote***. The
German figure is aligned to the total-cost-indicator method of the PRIIPs RTS over a
specified recommended holding period, and this model implements neither. Any level it
produces is arithmetic on this library's own [std] charge stack and **must never be
quoted as a market figure**.

.. rubric:: Modules that are off in the base run

Three constructions are implemented and switched off, so the base run reproduces the
worked example while the machinery stays visible and testable:

- **Dynamic lapse**, ``lapse_dyn_beta = 0``, with 0.15 as the reference value.
  ``lapse_dyn_add(t) = beta x max(0, 1 - av_pp(t)/cum_prem_pp(t))`` raises the lapse rate
  while the contract is under water against the premiums paid. Unit-linked lapse is
  market-sensitive precisely because the exit is at fund value on short notice. Switched
  on it bites hardest on model point 12, whose stress path leaves the fund far below the
  premiums paid for years.
- **The *Ablaufmanagement* glide**, off unless ``ablauf_flag``. A linear ramp of the
  **gross** return from the scenario's rate to ``mmkt_return_ann = 1.50 %`` over the last
  ``glide_months = 60`` months. With one fund and a deterministic return, a reallocation
  and a change of assumed return are the same thing, so this is the honest representation
  of what is known — and nothing about a real *Ablaufmanagement* was established, not
  whether it is opt-in, not the ramp length, not the destination.
- **The *Überschussbeteiligung*.** A unit-linked contract's surplus arises from the risk
  and cost results only, and the model computes the risk result but credits none of it
  back. The omission biases the projected *Fondsguthaben* **downward**, which is the
  honest direction for a charge demonstration.

*Beitragsfreistellung* is a fourth case and is different in kind: it is a **model point
election**, ``pup_month``, and not a cohort decrement. A paid-up policy's fund and its
*Beitragsrückgewähr* base both depend on the month it went paid-up, so a cohort-level
paid-up rate would need one sub-cohort per month — a two-dimensional recursion over 360
months for a second-order effect. The model reproduces the mechanic exactly on one cell
rather than approximately on all of them, and the [std] 1 % p.a. paid-up rate a cohort
implementation would use is recorded and not implemented. Omitting it biases the
projected charge income **upward**.

.. rubric:: Sign convention

:func:`net_cf` is **income positive**, which is the library-wide sign and the notes' own
orientation. :func:`liability_cf` publishes the same stream outgo-positive,
``liability_cf(t) = -net_cf(t)`` exactly, so a best-estimate non-unit liability is
``sum v(t) liability_cf(t)`` over whatever discount curve the valuation layer supplies,
with the unit liability added at market value. Both are columns of :func:`result_cf`, so
the identity is verifiable in the frame rather than only in prose.

The shape to expect is a large negative ``net_cf`` in the inception month ``t = 0`` — on
the anchor cell -1 966,22 €, because the 2.50 % acquisition commission and the issue
expense both fall
there while the acquisition charge that funds them arrives over sixty months — then a
thin positive margin that grows with the fund as the *kapitalbezogene* charge compounds
against it.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# ----------------------------------------  the model point

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the selected model point."""
    return model_point()["policy_id"]


def sex():
    """The insured's sex, M or F.  **Reporting only — it must not enter pricing.**

    German life tariffs are unisex for contracts written from 21 December 2012, so
    neither :func:`mort_rate_tariff_at_age` nor :func:`rentenfaktor_guar` reads this
    cells: both are indexed by age alone.  It is carried because a *Standmitteilung*
    reports it and because a reserving basis may still be sex-specific even where the
    tariff may not be.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def entry_age():
    """Age last birthday at inception.

    The age basis steps at each policy anniversary, so ``age(t) = entry_age() +
    policy_year(t) - 1 = entry_age() + t // 12`` and the attained age in the last projected
    month, ``t = proj_len() - 1``, is ``annuity_age() - 1``.
    """
    return int(model_point()["entry_age"])


def duration_init_m():
    """Policy months already elapsed at the valuation date; 0 for new business.

    An **elapsed count**, so it is 0-based by nature and ``proj_start() ==
    duration_init_m()`` exactly.  It fixes :func:`proj_start`, and through it everything
    that keys off the policy month counted from inception — the acquisition window above
    all.  Model point 6 opens at duration 96, past the window, and is the cell that shows
    what that costs an insurer: nothing, because the charge and the commission it funded
    are both behind it.
    """
    return int(model_point()["duration_init_m"])


def pols_if_init():
    """Policies in force at the projection's opening: the weight the model point carries.

    ``pols_if(proj_start()) == pols_if_init()`` exactly, which is the library's
    start-of-period convention asserted in the conventions suite.
    """
    return float(model_point()["pols_if_init"])


def annuity_age():
    """Age at *Rentenbeginn*.

    It fixes :func:`proj_len` and it is the row read from ``rentenfaktor_table.csv`` —
    **not** ``age(proj_len() - 1)``, which is one lower because the annuity begins at the
    end of the last projected month.
    """
    return int(model_point()["annuity_age"])


def prem_form():
    """The premium form: ``laufend`` (recurring) or ``einmal`` (single).

    The two differ in more than the number of instalments.  A *Einmalbeitrag* has no
    *Beitragssumme* to zillmer against and no five-year spreading to obey, so its
    acquisition charge is the *Zuzahlungskosten* rate levied once on receipt, which is
    what :func:`charge_acq_total` returns for it.
    """
    v = model_point()["prem_form"]
    if v not in ("laufend", "einmal"):
        raise ValueError("invalid prem_form")
    return v


def prem_pp_base():
    """The *Beitrag* the policy states, per instalment, at the initial level.

    It **already contains** whatever *Ratenzahlungszuschlag* the tariff applied for paying
    more often than annually, so nothing in this model loads it again — re-applying the
    fractionation loading is a listed pitfall.  :func:`prem_pp` is what is actually due in
    a given month, after the frequency, the premium term, any *Beitragsfreistellung* and
    any *Beitragsdynamik*.
    """
    return float(model_point()["prem_pp"])


def prem_mode_months():
    """Payment frequency in months: 1, 3, 6 or 12.

    It decides both which months carry a premium and how many acquisition instalments the
    sixty-month window holds — 60 monthly, 20 quarterly, 10 half-yearly, 5 annual.
    """
    v = int(model_point()["prem_mode_months"])
    if v not in (1, 3, 6, 12):
        raise ValueError("invalid prem_mode_months")
    return v


def prem_term_y():
    """Premium-paying term in years; 0 on a single premium.

    It caps both the premium stream and the acquisition window: a two-year premium term
    spreads the acquisition charge over 24 months, not 60.
    """
    return int(model_point()["prem_term_y"])


def dynamik_rate():
    """*Beitragsdynamik*: the contractual annual premium increase; 0 when off.

    **[std]** at 3 % on the one model point that carries it — no carrier's dynamic step
    was established.  It raises the premium and therefore the *Anlagebeitrag*, but it does
    **not** raise :func:`beitragssumme`, because a real tariff re-zillmers each accepted
    increment over its own sixty months and an increment cannot be assumed at inception.
    """
    return float(model_point()["dynamik_rate"])


def pup_month():
    """The 0-based policy month from which the contract is *beitragsfrei*; 0 = never.

    The column carries a point on the frame's own time axis, so it moved with the frame:
    model point 7 goes paid-up at ``t = 120``.  **Zero is the "never" sentinel**, not the
    inception month — a contract *beitragsfrei* from inception is not a contract, so
    nothing is lost by spending the value that way.

    *Beitragsfreistellung* is a **model point election** on this chassis, not a cohort
    decrement, and the reason is in the Space docstring.  From ``pup_month`` the premium
    and the charges withheld from it stop, while the fund-based charges, the *Stückkosten*
    and the *Risikobeitrag* continue by unit cancellation — which is why a paid-up
    unit-linked contract decays.
    """
    return int(model_point()["pup_month"])


def db_form():
    """The *Todesfallleistung* shape: ``fund``, ``prem_return``, ``pct_fund`` or ``sum_assured``.

    The four shapes German insurers use, in ascending order of the risk they impose:
    the fund itself (no net amount at risk, no *Risikobeitrag* at all), *Beitragsrückgewähr*
    (the composite, and the only shape with any corroboration in this library's corpus), a
    percentage of the fund, and a fixed *garantierte Mindesttodesfallleistung*.
    """
    v = model_point()["db_form"]
    if v not in ("fund", "prem_return", "pct_fund", "sum_assured"):
        raise ValueError("invalid db_form")
    return v


def db_pct():
    """The multiple of the *Fondsguthaben* used by the ``pct_fund`` death benefit.

    **[std]** at 1.10 on the two model points that carry it, chosen to give a positive net
    amount at risk that grows with the fund rather than vanishing as the
    *Beitragsrückgewähr* one does.  Commonly quoted market values are 100 %, 105 % and
    110 %; none was established.
    """
    return float(model_point()["db_pct"])


def sum_assured():
    """The *garantierte Mindesttodesfallleistung* used by the ``sum_assured`` death benefit.

    **[std]** at 40 000 EUR on the one model point that carries it, chosen large enough
    that the net amount at risk stays positive over a decaying paid-up fund.  This is the
    shape that turns the contract into a savings-plus-term-cover package and the one whose
    risk charge grows without limit as the fund falls.
    """
    return float(model_point()["sum_assured"])


def charge_id():
    """The key into ``charge_table.csv`` naming this policy's charge scale."""
    return model_point()["charge_id"]


def scenario_id():
    """The key into ``fund_scenario_table.csv`` naming this policy's return path."""
    return model_point()["scenario_id"]


def rentenfaktor_id():
    """The key into ``rentenfaktor_table.csv`` naming this policy's conversion factors."""
    return model_point()["rentenfaktor_id"]


def unit_price_init():
    """The *Anteilspreis* at the projection's opening, ``unit_price_open(proj_start())``.

    100.00 EUR on every new-business cell, which makes the unit counts readable; 118.40 on
    the in-force cell, where it is the price a *Standmitteilung* would report.
    """
    return float(model_point()["unit_price_init"])


def units_init():
    """*Anteileinheiten* held at the projection's opening.

    Zero on new business.  On the in-force cell, 190.0 units at 118.40 EUR — a
    *Fondsguthaben* of 22 496,00 EUR against 24 000,00 EUR of premiums paid, so the cell
    opens with a positive net amount at risk and a live *Risikobeitrag*.
    """
    return float(model_point()["units_init"])


def cum_prem_init():
    """Gross premiums paid before the valuation date — the *Beitragsrückgewähr* base.

    Seeds :func:`cum_prem_pp`.  Nonzero only on the in-force cell, where getting it wrong
    would silently mis-state the death benefit for the whole remaining term.
    """
    return float(model_point()["cum_prem_init"])


def topup_month():
    """The 0-based policy month of a *Zuzahlung*; 0 = none.

    A point on the frame's time axis, so it moved with the frame: model point 9 tops up at
    ``t = 120``.  **Zero is the "none" sentinel** rather than the inception month, a
    *Zuzahlung* at inception being indistinguishable from a larger first *Beitrag*.
    """
    return int(model_point()["topup_month"])


def topup_amount():
    """The *Zuzahlung* — an additional single premium into an existing contract.

    It buys units like a premium, pays its own *Zuzahlungskosten* and no
    *beitragsbezogene* charge, and raises the *Beitragsrückgewähr* base.  It does **not**
    raise :func:`beitragssumme`, for the same reason a *Beitragsdynamik* increment does
    not.
    """
    return float(model_point()["topup_amount"])


def wd_month():
    """The 0-based policy month of a *Teilentnahme*; 0 = none.

    A point on the frame's time axis, so it moved with the frame: model point 9 withdraws
    at ``t = 240``.  **Zero is the "none" sentinel** rather than the inception month.
    """
    return int(model_point()["wd_month"])


def wd_amount():
    """The *Teilentnahme* — a partial withdrawal during the *Aufschubzeit*.

    An owner election, not a claim, so it is published as :func:`withdrawals` and never as
    ``claims_wd``.  It is a partial surrender with a partial surrender's tax consequences,
    and it is settled by cancelling units at the closing *Anteilspreis*.
    """
    return float(model_point()["wd_amount"])


def ablauf_flag():
    """Whether *Ablaufmanagement* — the de-risking glide before *Rentenbeginn* — is on.

    Represented as a linear ramp of the **gross** return down to ``mmkt_return_ann`` over
    the last ``glide_months`` months.  With one fund and a deterministic return that is
    arithmetically the same thing as a reallocation, and it is the honest representation
    of what is known: no ramp length, destination or opt-in rule was established.
    """
    return bool(model_point()["ablauf_flag"])


def kapitalwahl():
    """Whether the *Kapitalwahlrecht* is elected at *Rentenbeginn*.

    A **reporting** split only, and deliberately so.  Both routes release the same
    *Fondsguthaben* from this model — the annuity is published, not projected — so the
    flag changes no cash flow.  It is carried because the two tax regimes genuinely
    differ and because take-up is the largest behavioural unknown in the product; **no
    take-up rate was established**, so the base run annuitises and this is an election
    rather than an assumption.
    """
    return bool(model_point()["kapitalwahl"])


# ----------------------------------------  the frame

def proj_start():
    """The first projected policy month, ``duration_init_m()`` — 0-based.

    0 for new business, 96 for the in-force cell: ``t`` counts policy months from the
    contract's own inception with ``t = 0`` the inception month, so the elapsed-month count
    **is** the first projected index and needs no ``+ 1``.  Because the origin is inception
    rather than the valuation date, a single :func:`charge_acq_pp` rule serves the
    new-business and the in-force cell without a duration offset.
    """
    return duration_init_m()


def proj_len():
    """The **number** of projected policy months from inception,
    ``12 x (annuity_age() - entry_age())``.

    The library's reading of ``proj_len()``: a period **count**, so it is the frame's
    **exclusive** end.  ``result_cf()`` covers ``t = proj_start() ... proj_len() - 1`` and
    ``result_cf().index[-1] == proj_len() - 1`` on every model point.  The end of month
    ``proj_len() - 1`` is *Rentenbeginn*; there is no ``t = proj_len()`` row.
    """
    return 12 * (annuity_age() - entry_age())


def policy_year(t):
    """The policy year containing month t, ``t // 12 + 1``.

    The **contractual** label, and 1-based by contract: policy year 1 is ``t = 0 ... 11``.
    It is derived from ``t`` and never indexed by, and it is the key into the annual tables
    — ``lapse_table.csv`` and ``fund_scenario_table.csv`` — whose own ``policy_year``
    column is that same 1-based label.
    """
    return t // 12 + 1


def age(t):
    """Attained age in month t, ``entry_age() + policy_year(t) - 1 = entry_age() + t // 12``.

    At ``t = proj_len() - 1`` this is ``annuity_age() - 1``, because the annuity begins at
    the **end** of that month.  Reading the *Rentenfaktor* off this cells instead of off
    :func:`annuity_age` is a listed pitfall and would fetch 24.45 in place of 25.00 on the
    anchor cell.
    """
    return entry_age() + policy_year(t) - 1


# ----------------------------------------  the charge scale

def charge_row():
    """The row of ``charge_table.csv`` for this policy's ``charge_id``."""
    return data.charge_table().loc[charge_id()]                      # noqa: F821


def alpha_rate():
    """*Abschluss- und Vertriebskosten* rate on the *Beitragssumme*.

    2.50 % on ``std_gross`` — **the *Höchstzillmersatz* itself**, and the only number in
    the whole charge stack with any corroboration.  The composite takes the cap rather
    than a guessed interior point, on the ground that a reference implementation should
    demonstrate the binding constraint.  Zero on the *Nettotarif*.
    """
    return float(charge_row()["alpha_rate"])


def alpha_spread_months():
    """Months over which the acquisition charge is spread — 60 on every shipped tariff.

    § 169 VVG requires the *angesetzte Abschluss- und Vertriebskosten* to be spread evenly
    over the first five contract years, and a unit-linked tariff implements that inside
    the *Beitragsverrechnung*: only one sixtieth may be withheld per month, so units are
    bought from the start and the surrender value is positive from the first month.
    """
    return int(charge_row()["alpha_spread_months"])


def beta_rate():
    """*Beitragsbezogene Verwaltungskosten*: the rate on each gross *Beitrag*.

    Withheld from the premium before units are bought, for the whole premium-paying term,
    and it stops when premiums stop.  **[std]** at 4.00 % on the composite against an
    argued range of 2 % to 10 %; no carrier level was established.
    """
    return float(charge_row()["beta_rate"])


def gamma_rate_ann():
    """*Kapitalbezogene Verwaltungskosten* (*Gammakosten*): the annual rate on the fund.

    **[std]** at 0.30 % p.a. against an argued range of 0.10 % to 1.20 %.  This is the
    charge that continues after premiums stop, the one that makes a paid-up unit-linked
    policy decay, and — because it compounds against the whole accumulated fund — the
    dominant component of the reduction in yield on a long contract.
    """
    return float(charge_row()["gamma_rate_ann"])


def gamma_rate_mth():
    """The monthly *Gammakosten* rate, ``gamma_rate_ann() / 12``.

    Divided, not compounded, because a German tariff quotes a **nominal** monthly charge
    rate.  The fund *return* on the same contract is compounded geometrically because it
    is an effective annual rate.  That asymmetry is deliberate; collapsing it is a listed
    pitfall.  On the composite, ``0.0030 / 12 = 0.00025``.
    """
    return gamma_rate_ann() / 12.0


def policy_fee_mth():
    """*Stückkosten*: the fixed euro charge per policy per month.

    **[std]** at 3.00 EUR against an argued range of 0 to 5 EUR.  A euro amount rather
    than a rate, which is why it is the charge that can consume a small paid-up
    *Fondsguthaben* — the reason insurers set a minimum fund below which
    *Beitragsfreistellung* is refused.
    """
    return float(charge_row()["policy_fee_mth"])


def zuzahlung_charge_rate():
    """*Zuzahlungskosten*: the acquisition charge on a *Zuzahlung* or a *Einmalbeitrag*.

    **[std]** at 2.50 % on the composite.  A *Zuzahlung* pays this and **no**
    *beitragsbezogene* charge — it is not a regular *Beitrag* — and on a single-premium
    contract this rate is the whole of the acquisition charge, levied once on receipt.
    """
    return float(charge_row()["zuzahlung_charge_rate"])


def stornoabzug_rate():
    """*Stornoabzug*: the deduction from the *Rückkaufswert* on surrender.

    Permissible only if *vereinbart*, *beziffert* and *angemessen*, and **never for
    unamortised acquisition costs** — a deduction of that kind is ineffective under
    § 169 VVG, which is why :func:`stornoabzug_pp` is a flat rate on the *Fondsguthaben*
    and deliberately not a function of the unrecovered acquisition charge.  **[std]** at
    zero on the composite, because many unit-linked tariffs have none at all and a
    non-zero one would be an unsourced number attached to a contested clause; 2.00 % on
    ``std_high``, the only shipped tariff that carries one.
    """
    return float(charge_row()["stornoabzug_rate"])


# ----------------------------------------  premium and the Beitragsverrechnung

def dynamik_factor(t):
    """The *Beitragsdynamik* multiplier in month t, ``(1 + dynamik_rate())^(y(t) - 1)``.

    Steps at each policy anniversary, so it is 1.0 for the whole of policy year 1,
    ``t = 0 ... 11``.  Off
    (identically 1.0) on twelve of the thirteen model points.
    """
    return (1.0 + dynamik_rate()) ** (policy_year(t) - 1)


def prem_pp(t):
    """The gross *Beitrag* per policy due in month t; zero in a month with no instalment.

    A premium falls when the frequency says so, the premium term has not expired and the
    contract is not yet *beitragsfrei*.  On a single-premium contract the whole
    *Einmalbeitrag* falls at ``proj_start()`` and nothing after it.

    The amount is :func:`prem_pp_base` times the *Beitragsdynamik* factor and nothing
    else: the stated instalment already contains any *Ratenzahlungszuschlag*, so loading
    it again would charge the fractionation twice.
    """
    if prem_form() == "einmal":
        return prem_pp_base() if t == proj_start() else 0.0
    if t >= 12 * prem_term_y():
        return 0.0
    if pup_month() > 0 and t >= pup_month():
        return 0.0
    if (t - proj_start()) % prem_mode_months() != 0:
        return 0.0
    return prem_pp_base() * dynamik_factor(t)


def topup_pp(t):
    """The *Zuzahlung* per policy in month t; zero in every other month."""
    if topup_month() > 0 and t == topup_month():
        return topup_amount()
    return 0.0


def beitragssumme():
    """The *Beitragssumme*: the sum of premiums **payable**, at the **initial** level.

    ``prem_pp_base() x (12 / prem_mode_months()) x prem_term_y()`` on a recurring-premium
    contract — 200.00 x 12 x 30 = 72 000,00 EUR on the anchor cell — and the
    *Einmalbeitrag* itself on a single-premium one.

    It is the base of the acquisition charge and it is **invariant**: it does not shrink
    when the contract lapses or goes *beitragsfrei*, and it does not grow with a
    *Beitragsdynamik* increment or a *Zuzahlung*.  Letting it follow the premiums actually
    paid is a listed pitfall — it would make the acquisition charge a function of the
    lapse assumption, which is both wrong and circular.
    """
    if prem_form() == "einmal":
        return prem_pp_base()
    return prem_pp_base() * (12.0 / prem_mode_months()) * prem_term_y()


def acq_window_months():
    """The months over which the acquisition charge is spread, ``min(60, 12 x term)``.

    The five-year statutory spread, cut short where the premium term is shorter than five
    years: model point 12 pays for two years, so its window is 24 months and not 60.  Zero
    on a single-premium contract, whose acquisition charge is a one-off.
    """
    if prem_form() == "einmal":
        return 0
    return min(alpha_spread_months(), 12 * prem_term_y())


def acq_instalments():
    """The number of acquisition instalments: the window divided by the premium frequency.

    60 on the anchor cell, 20 quarterly, 10 half-yearly, 5 annual, 24 on the two-year
    premium term, and 1 on a single premium.  The count matters because the instalment is
    ``charge_acq_total() / acq_instalments()``, so spreading a shortened window over sixty
    months would understate every instalment and leave the ledger short at the end.
    """
    if prem_form() == "einmal":
        return 1
    return acq_window_months() // prem_mode_months()


def charge_acq_total():
    """The whole *Abschluss- und Vertriebskosten* charge, before any *Zuzahlungskosten*.

    ``alpha_rate() x beitragssumme()`` on a recurring-premium contract — 2.50 % of
    72 000,00 = **1 800,00 EUR** on the anchor cell — and
    ``zuzahlung_charge_rate() x prem_pp_base()`` on a single-premium one, where there is
    no *Beitragssumme* to zillmer against and no five-year spread to obey.
    """
    if prem_form() == "einmal":
        return zuzahlung_charge_rate() * prem_pp_base()
    return alpha_rate() * beitragssumme()


def charge_acq_pp(t):
    """The acquisition charge withheld from month t's premium, per policy.

    One instalment of ``charge_acq_total() / acq_instalments()`` on each premium date
    inside the window, nothing after it, plus the *Zuzahlungskosten* on any *Zuzahlung*
    falling in the month.  On the anchor cell that is **30,00 EUR for t = 0 ... 59 and
    0,00 from t = 60** — 15 % of each of the first sixty premiums, then a cliff.  That
    cliff is the characteristic shape of a German unit-linked contract's early values and
    it is the reason this model runs monthly.

    An in-force model point opening after the window sees zero at every projected month,
    which is correct: the charge and the commission it funded are both behind it.
    """
    reg = 0.0
    if prem_form() == "einmal":
        if t == proj_start():
            reg = charge_acq_total()
    elif t < acq_window_months() and prem_pp(t) > 0.0:
        reg = charge_acq_total() / acq_instalments()
    return reg + zuzahlung_charge_rate() * topup_pp(t)


def cum_charge_acq_pp(t):
    """Cumulative acquisition charge withheld to and including month t, per policy.

    The ledger :func:`check_acq_charge` closes against an independently counted
    expectation.  It opens at ``charge_acq_pp(proj_start())`` in the frame's first month,
    so on an in-force model point it measures the charge taken **inside the projection**
    and not the charge the contract has already paid.  The seed sits in the first month
    itself rather than at ``proj_start() - 1``, which on a new-business cell would be
    ``t = -1``.
    """
    if t < proj_start():
        return 0.0
    if t == proj_start():
        return charge_acq_pp(t)
    return cum_charge_acq_pp(t - 1) + charge_acq_pp(t)


def charge_admin_prem_pp(t):
    """*Beitragsbezogene Verwaltungskosten* withheld from month t's premium, per policy.

    ``beta_rate() x prem_pp(t)`` — 4.00 % of 200.00 = **8,00 EUR** on the anchor cell,
    every month a premium falls and none in between.  Charged on the regular *Beitrag*
    only: a *Zuzahlung* pays its own charge and no second one.
    """
    return beta_rate() * prem_pp(t)


def prem_to_av_pp(t):
    """The *Anlagebeitrag*: what is left of the month's money to buy units, per policy.

    ``B(t) + Z(t) - alpha(t) - beta B(t)``.  On the anchor cell **162,00 EUR while the
    acquisition instalment runs (t < 60) and 192,00 EUR after it** — the step at ``t = 60``
    is the whole point of the sixty-month window.
    """
    return (prem_pp(t) + topup_pp(t)
            - charge_acq_pp(t) - charge_admin_prem_pp(t))


def cum_prem_pp(t):
    """Cumulative **gross** premiums paid to and including month t, per policy.

    The *Beitragsrückgewähr* base, seeded at :func:`cum_prem_init`.  It is the premiums
    **paid**, not the premiums invested: on the anchor cell ``cum_prem_pp(59) =
    12 000,00 EUR`` against 9 720,00 EUR actually put into units, so reading the death
    benefit off the invested amount would understate it by 19 %.  A *Zuzahlung* counts.

    The seed is added **inside** the frame's first month rather than read from
    ``cum_prem_pp(proj_start() - 1)``, which on a new-business cell would be ``t = -1``.
    """
    if t < proj_start():
        return cum_prem_init()
    if t == proj_start():
        return cum_prem_init() + prem_pp(t) + topup_pp(t)
    return cum_prem_pp(t - 1) + prem_pp(t) + topup_pp(t)


# ----------------------------------------  the fund

def fund_return_gross_ann(t):
    """The assumed **gross** annual fund return in month t, before the TER.

    Read from ``fund_scenario_table.csv`` by ``(scenario_id, policy_year)``.  **[std]**
    and a scenario rather than a forecast: nothing in this product's corpus supplies a
    return, and PRIIPs deliberately does not — its scenarios are derived from an
    underlying's own return history, so nothing here may be compared with one.

    Where ``ablauf_flag`` is set, the *Ablaufmanagement* glide overrides it in the last
    ``glide_months`` months with a linear ramp down to ``mmkt_return_ann``, reaching the
    money-market rate exactly in the final month.
    """
    base = data.fund_scenario_table().loc[                           # noqa: F821
        (scenario_id(), policy_year(t)), "gross_return_ann"]
    base = float(base)
    if not ablauf_flag():
        return base
    remaining = (proj_len() - 1) - t
    if remaining >= glide_months:                                    # noqa: F821
        return base
    step = (glide_months - remaining) / float(glide_months)          # noqa: F821
    return base + (mmkt_return_ann - base) * step                    # noqa: F821


def fund_ter_ann(t):
    """The fund's *TER* (*Gesamtkostenquote*) in month t, as an annual rate.

    **A return item, never a policy charge.**  It is borne inside the *Anteilspreis* and
    accrues to the fund manager, so it appears in no ``charge_*`` cells and in no
    :func:`result_cf` column: the model nets it off the gross return instead.  Charging it
    explicitly double-counts the fund's costs; ignoring it overstates the policyholder's
    return.  0.45 % p.a. on the active composite fund, 0.15 % on the ETF.
    """
    return float(data.fund_scenario_table().loc[                     # noqa: F821
        (scenario_id(), policy_year(t)), "ter_ann"])


def fund_return_net_ann(t):
    """The annual fund return net of the TER, ``gross - ter``.

    4.55 % p.a. on the base path — 5.00 % gross less a 0.45 % TER.  Netting rather than
    compounding the two is the [std] convention and is immaterial at these levels.
    """
    return fund_return_gross_ann(t) - fund_ter_ann(t)


def fund_return_net_mth(t):
    """The monthly fund return, ``(1 + fund_return_net_ann(t))^(1/12) - 1``.

    Compounded **geometrically**, because the annual rate is an effective rate and twelve
    monthly steps must reproduce it.  The charge rates on the same contract are divided by
    twelve instead, because a German tariff quotes them nominally.  On the base path
    ``(1.0455)^(1/12) - 1 = 0.00371482 per month``.
    """
    return (1.0 + fund_return_net_ann(t)) ** (1.0 / 12.0) - 1.0


def unit_price_open(t):
    """The *Anteilspreis* at the **start** of policy month t.

    ``unit_price_init()`` in the frame's first month and ``unit_price(t - 1)`` in every
    month after it.  It is a cells of its own rather than a ``unit_price(t - 1)`` written
    at every call site because on a new-business cell ``proj_start()`` is 0, and nothing in
    a 0-based frame may be indexed at ``t = -1``.  Units bought out of month t's premium
    are bought at this price; everything cancelled during the month is cancelled at
    :func:`unit_price`.
    """
    if t <= proj_start():
        return unit_price_init()
    return unit_price(t - 1)


def unit_price(t):
    """The *Anteilspreis* at the **end** of policy month t.

    ``unit_price_open(t) x (1 + fund_return_net_mth(t))``, seeded by
    ``unit_price_open(proj_start()) = unit_price_init()``.  The whole of the fund's own
    cost lives in this recursion and nowhere else.
    """
    return unit_price_open(t) * (1.0 + fund_return_net_mth(t))


def units_pp(t):
    """*Anteileinheiten* held per policy at the **start** of month t.

    **The state variable of the product**: what the insurer guarantees is the number of
    units, not their value, so the recursion is carried in units and euro are derived.
    ``units_pp(proj_start()) = units_init()``; thereafter the closing fund of month
    ``t - 1`` divided by that month's closing price.
    """
    if t <= proj_start():
        return units_init()
    return av_pp_at(t - 1, "BEF_DECR") / unit_price(t - 1)


def units_bought_pp(t):
    """Units bought in month t with the *Anlagebeitrag*, at the **opening** price.

    ``prem_to_av_pp(t) / unit_price_open(t)``.  Premium is in advance, so the month's
    investment return accrues on the units it buys.
    """
    return prem_to_av_pp(t) / unit_price_open(t)


def units_cancelled_pp(t):
    """Units cancelled in month t for charges and any *Teilentnahme*, at the closing price.

    The fund-based administration charge, the *Stückkosten*, the *Teilentnahme* and the
    *Risikobeitrag*, all divided by ``unit_price(t)``.  Together with
    :func:`units_bought_pp` this closes :func:`check_units_roll_fwd`, an identity with
    **no price term in it at all** — which is exactly why it catches a charge taken in
    euro without the matching units being cancelled.
    """
    return (charge_admin_fund_pp(t) + charge_policy_fee_pp(t)
            + withdrawals_pp(t) + charge_risk_pp(t)) / unit_price(t)


def av_pp(t):
    """The *Fondsguthaben* per policy at the **start** of month t, before the premium.

    ``units_pp(t) x unit_price_open(t)``.  The within-month balances are
    :func:`av_pp_at`; the closing fund of the surviving cohort is ``av_pp(t + 1) x
    pols_if(t + 1)`` and not any of them.
    """
    return units_pp(t) * unit_price_open(t)


def av_pp_at(t, timing):
    """The *Fondsguthaben* per policy at a named point inside month t.

    The four points of the monthly processing order, in order:

    ``"BEF_CHARGE"``
        after the premium has bought units and the month's return has accrued.
    ``"AFT_CHARGE"``
        less the fund-based administration charge and the *Stückkosten*.
    ``"AFT_WD"``
        less any *Teilentnahme*.  This is the balance the net amount at risk is measured
        against, so it is the fund the *Risikobeitrag* prices.
    ``"BEF_DECR"``
        less the *Risikobeitrag*.  The closing balance: what a death, a surrender or an
        annuitisation releases, and what rolls into ``units_pp(t + 1)``.

    The ``min(.., remaining)`` floors inside the charges are **[std] safeguards**, not
    tariff terms; none of the thirteen shipped model points triggers one, and a contract
    that did would in practice have had its cover terminated.
    """
    if timing == "BEF_CHARGE":
        return (units_pp(t) + units_bought_pp(t)) * unit_price(t)
    elif timing == "AFT_CHARGE":
        return (av_pp_at(t, "BEF_CHARGE") - charge_admin_fund_pp(t)
                - charge_policy_fee_pp(t))
    elif timing == "AFT_WD":
        return av_pp_at(t, "AFT_CHARGE") - withdrawals_pp(t)
    elif timing == "BEF_DECR":
        return av_pp_at(t, "AFT_WD") - charge_risk_pp(t)
    else:
        raise ValueError("invalid timing")


def av_at(t, timing):
    """The in-force *Fondsguthaben* at a named point inside month t.

    ``av_pp_at(t, timing) x pols_if(t)`` — the per-policy balance weighted by the
    start-of-month exposure, which is the weight every cash flow on that
    :func:`result_cf` row carries.  For the fund the **survivors** carry into month
    ``t + 1``, read ``av_pp(t + 1) x pols_if(t + 1)`` instead: the decrements have acted
    by then and this cells has not applied them.
    """
    return av_pp_at(t, timing) * pols_if(t)


# ----------------------------------------  the charges taken out of the fund

def charge_admin_fund_pp(t):
    """*Kapitalbezogene Verwaltungskosten* in month t, per policy.

    ``gamma_rate_mth() x av_pp_at(t, "BEF_CHARGE")`` — taken by **cancelling units**, on
    the fund as it stands after the premium and the month's return.  It continues when
    premiums stop, which is what makes a paid-up unit-linked contract decay; a model that
    netted it out of the *Beitrag* instead would be right until ``t = 120`` on model
    point 7 and wrong from then on.
    """
    return gamma_rate_mth() * av_pp_at(t, "BEF_CHARGE")


def charge_policy_fee_pp(t):
    """*Stückkosten* in month t, per policy, floored at the remaining balance.

    A flat euro amount taken by cancelling units, independent of the premium and of the
    fund, so on a small decayed *Fondsguthaben* it is the charge that bites hardest.  The
    floor at the remaining balance is a **[std]** safeguard against a negative fund and is
    triggered by no shipped model point.
    """
    return min(policy_fee_mth(),
               av_pp_at(t, "BEF_CHARGE") - charge_admin_fund_pp(t))


def charge_risk_pp(t):
    """The *Risikobeitrag* in month t, per policy: the price of the death cover.

    ``mort_rate_tariff_mth(t) x nar_pp(t)``, floored at the remaining balance, taken by
    cancelling units.  Priced on the **first-order death table** — never on the annuity
    table behind the *Rentenfaktor*, and never on the projection's own best-estimate
    decrement, because the difference between the two is the *Risikoergebnis*.

    It is recomputed every month because both the death benefit and the *Fondsguthaben*
    move.  On the ``fund`` death-benefit shape it is identically zero, there being no net
    amount at risk to price.
    """
    return min(mort_rate_tariff_mth(t) * nar_pp(t), av_pp_at(t, "AFT_WD"))


def stornoabzug_pp(t):
    """The *Stornoabzug* per surrendering policy in month t.

    ``stornoabzug_rate() x av_pp_at(t, "BEF_DECR")`` — a flat rate on the *Fondsguthaben*,
    and deliberately **not** a function of the unrecovered acquisition charge: § 169 VVG
    makes a deduction for *noch nicht getilgte Abschluss- und Vertriebskosten* ineffective,
    which is precisely what stops an insurer recovering through the deduction what the
    five-year spreading denies it.  Zero on every shipped tariff but ``std_high``.
    """
    return stornoabzug_rate() * av_pp_at(t, "BEF_DECR")


def withdrawals_pp(t):
    """The *Teilentnahme* per policy in month t, floored at the balance available.

    An **owner election**, not a claim, which is why it is published under this name and
    never as ``claims_wd``.  It is settled by cancelling units at the closing
    *Anteilspreis*, after the fund-based charges and before the net amount at risk is
    measured — so a withdrawal raises the net amount at risk on a *Beitragsrückgewähr*
    contract and therefore the following months' *Risikobeitrag*.
    """
    if wd_month() > 0 and t == wd_month():
        return min(wd_amount(), av_pp_at(t, "AFT_CHARGE"))
    return 0.0


# ----------------------------------------  the death benefit

def db_floor_pp(t):
    """The guaranteed minimum *Todesfallleistung* in month t, per policy.

    The floor the fund is compared against, by ``db_form``:

    ``fund``
        0.00 — the benefit is the *Fondsguthaben* itself, so there is nothing to
        guarantee and no *Risikobeitrag*.
    ``prem_return``
        the *Beitragsrückgewähr*: ``cum_prem_pp(t)``, the gross premiums paid.  The
        composite, and the only shape with corroboration anywhere in this corpus.
    ``pct_fund``
        ``db_pct()`` times the *Fondsguthaben*, so the floor and the net amount at risk
        both grow with the fund.
    ``sum_assured``
        a fixed *garantierte Mindesttodesfallleistung*, independent of the fund.
    """
    form = db_form()
    if form == "fund":
        return 0.0
    elif form == "prem_return":
        return cum_prem_pp(t)
    elif form == "pct_fund":
        return db_pct() * av_pp_at(t, "AFT_WD")
    return sum_assured()


def nar_pp(t):
    """The *riskiertes Kapital* in month t: ``max(db_floor_pp(t) - fund, 0)``.

    Measured against ``av_pp_at(t, "AFT_WD")`` — the fund **before** that month's
    *Risikobeitrag* — so the insurer's non-unit cost per death is exactly this amount and
    nothing else.

    **The floor at zero is load-bearing.**  Without it the contract would pay the insurer
    a negative charge in every month the fund is above the guarantee and
    :func:`death_strain` would turn negative, which books the fund's growth as insurance
    profit.  On the *Beitragsrückgewähr* shape this quantity is positive early, vanishes
    once the fund overtakes the premiums paid, and returns after a market fall.
    """
    return max(db_floor_pp(t) - av_pp_at(t, "AFT_WD"), 0.0)


def db_pp(t):
    """The *Todesfallleistung* actually paid on a death in month t, per policy.

    ``av_pp_at(t, "BEF_DECR") + nar_pp(t)``: the closing *Fondsguthaben* the death
    releases, plus the net amount at risk the insurer funds.  Splitting it that way rather
    than writing ``max(floor, fund)`` is what keeps the unit and non-unit sides apart —
    the first term is the policyholder's own money and the second is the insurer's.
    """
    return av_pp_at(t, "BEF_DECR") + nar_pp(t)


# ----------------------------------------  decrements

def mort_rate_tariff_at_age(x):
    """The **first-order** annual death rate at attained age x, from ``mort_table.csv``.

    The tariff's own basis — a DAV 2008 T proxy, ``0.00080 x 1.10^(x - 37)`` — and the
    price of the death cover.  This cells and :func:`rentenfaktor_guar` are the model's
    two mortality reads, and **no cells reads both**: a German fondsgebundene contract
    prices its death charge on a death table and its conversion guarantee on an annuity
    table, and using one for both misprices one of them.
    """
    return float(data.mort_table().loc[x, "qx_tariff"])              # noqa: F821


def mort_rate_at_age(x):
    """The **second-order** annual death rate at attained age x, the projection's decrement.

    ``mort_be_factor x mort_rate_tariff_at_age(x)`` with a flat ``mort_be_factor = 0.75``.
    Flat is crude and is stated as such; what it buys is that the *Risikoergebnis* is
    exactly 25 % of the *Risikobeitrag* collected, which a reader can verify with a
    calculator.  What a replacement basis must preserve is the **direction**: a first-order
    death table carries its margin **above** best estimate.
    """
    return mort_be_factor * mort_rate_tariff_at_age(x)               # noqa: F821


def mort_rate_tariff(t):
    """The first-order annual death rate in month t, at ``age(t)``.

    0.00080 in policy year 1 of the anchor cell, whose entry age is the proxy's anchor
    age.
    """
    return mort_rate_tariff_at_age(age(t))


def mort_rate_tariff_mth(t):
    """The first-order **monthly** death rate, ``mort_rate_tariff(t) / 12``.

    Split **linearly**, not geometrically, because the tariff's *Risikobeitrag* is
    ``q(x)/12`` times the *riskiertes Kapital* and the charge and the decrement must rest
    on the same split.  At q = 0.00080 the two splits differ by 0.04 % — a difference that
    would land entirely in the risk result, which is exactly the quantity the model is
    trying to measure.
    """
    return mort_rate_tariff(t) / 12.0


def mort_rate(t):
    """The best-estimate **annual** death rate in month t, at ``age(t)``.

    0.00060 in policy year 1 of the anchor cell: 0.75 x 0.00080.
    """
    return mort_rate_at_age(age(t))


def mort_rate_mth(t):
    """The best-estimate **monthly** death rate, ``mort_rate(t) / 12``.

    The projection's decrement, and 0.00005 in policy year 1 of the anchor cell.  Split
    the same way as the tariff rate, for the reason given in
    :func:`mort_rate_tariff_mth`.
    """
    return mort_rate(t) / 12.0


def lapse_rate_base(t):
    """The table annual lapse rate for the policy year containing month t.

    **[std]** throughout — no German unit-linked *Stornoquote* was established anywhere.
    6 % in years 1 to 5, 3 % in 6 to 10, 2 % in 11 and 12, 3 % from 13.  The
    front-loading is a structural inference: the acquisition charge is being taken, the
    value is furthest below the premiums paid, and § 168 VVG makes the exit
    near-frictionless.
    """
    return float(data.lapse_table().loc[policy_year(t), "lapse_rate"])   # noqa: F821


def lapse_tax_step(t):
    """The tax-threshold multiplier on the lapse rate in month t: 2.5, or 1.0.

    Under § 20 Abs. 1 Nr. 6 EStG only **half** the *Unterschiedsbetrag* is taxable where
    the contract has run at least **twelve years** and payment falls after completion of
    the **62nd year of life**.  Surrenders are suppressed as the threshold approaches and
    spike once both limbs are met, so the multiplier applies for the twelve months of the
    policy year ``max(13, 62 - entry_age() + 1)``.

    **Keying the spike on duration alone is wrong**, and is a listed pitfall: the anchor
    cell passes duration 12 at age 48, fourteen years before the tax benefit exists, so
    its step falls in policy year 26 — ``t = 300`` to ``311``, where the base 3.0 % becomes
    7.5 %.  On model point 12 the step never fires, because the projection ends at
    ``t = 143`` and the step year begins at ``t = 144``.
    """
    step_year = max(13, 62 - entry_age() + 1)
    return 2.5 if policy_year(t) == step_year else 1.0


def lapse_dyn_add(t):
    """The dynamic-lapse addition in month t; **zero in the base run**.

    ``lapse_dyn_beta x max(0, 1 - av_pp(t) / cum_prem_pp(t))`` — the rate rises while the
    contract is under water against the premiums paid.  Unit-linked lapse is
    market-sensitive precisely because the exit is at fund value on short notice, and the
    feedback it introduces is real: a falling fund raises lapse, which removes the
    policies whose charges would have recovered the acquisition cost.

    ``lapse_dyn_beta = 0`` in the base run and 0.15 is the reference value.  No German
    calibration evidence for a coefficient of any size exists in this corpus.
    """
    if lapse_dyn_beta == 0.0:                                        # noqa: F821
        return 0.0
    if cum_prem_pp(t) <= 0.0:
        return 0.0
    return lapse_dyn_beta * max(0.0, 1.0 - av_pp(t) / cum_prem_pp(t))  # noqa: F821


def lapse_rate(t):
    """The **annual** lapse rate applied in month t.

    ``min(lapse_cap, lapse_rate_base(t) x lapse_tax_step(t) + lapse_dyn_add(t))`` with a
    **[std]** cap of 40 %.  Annual by the library's convention; the monthly rate the
    projection actually uses is :func:`lapse_rate_mth`.
    """
    return min(lapse_cap,                                            # noqa: F821
               lapse_rate_base(t) * lapse_tax_step(t) + lapse_dyn_add(t))


def lapse_rate_mth(t):
    """The **monthly** lapse rate, ``1 - (1 - lapse_rate(t))^(1/12)``; zero in the last month.

    Split **geometrically**, unlike the mortality rate, because nothing is priced off the
    lapse rate and the annual rate is the observable that twelve monthly steps must
    reproduce: 0.514301 % at 6 % p.a. and 0.253505 % at 3 %.

    ``lapse_rate_mth(proj_len() - 1) = 0`` **[std]**: the end of the last projected month
    is *Rentenbeginn*, so a surrender and an annuitisation are the same event releasing the
    same *Fondsguthaben*, and the whole surviving cohort is booked as
    :func:`pols_maturity`.  No cash flow moves either way; the convention decides the
    split between the lapse total and the maturity count.
    """
    if t >= proj_len() - 1:
        return 0.0
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """Policies in force at the **start** of month t.

    ``pols_if(proj_start()) = pols_if_init()`` exactly, and the count on a
    :func:`result_cf` row is the weight applied to every cash flow on that same row, so
    dividing a flow by it recovers the per-policy amount.  End-of-month state is
    :func:`pols_if_at`.

    ``pols_if(proj_len()) = 0``, one past the frame's last index: the survivors of the last
    projected month leave as :func:`pols_maturity` and there is nothing after
    *Rentenbeginn* in this model.
    """
    if t <= proj_start():
        return pols_if_init()
    if t >= proj_len():
        return 0.0
    return (pols_if(t - 1) * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1)))


def pols_if_at(t, timing):
    """The in-force count at a named point inside month t.

    ``"BEF_DECR"``
        the start-of-month count, ``pols_if(t)``.
    ``"AFT_DEATH"``
        after deaths and before lapses — the ordering, deaths first, is **[std]**.
    ``"AFT_DECR"``
        after both, which for ``t < proj_len() - 1`` is ``pols_if(t + 1)``.  At
        ``t = proj_len() - 1`` it is the surviving cohort **before** the maturity sweep,
        and so equals ``pols_maturity(proj_len() - 1)`` rather than ``pols_if(proj_len())``,
        which is zero.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    elif timing == "AFT_DEATH":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    elif timing == "AFT_DECR":
        return pols_if_at(t, "AFT_DEATH") * (1.0 - lapse_rate_mth(t))
    else:
        raise ValueError("invalid timing")


def pols_death(t):
    """Expected deaths in month t, on the **best-estimate** basis.

    ``pols_if(t) x mort_rate_mth(t)``.  The tariff's first-order rate prices the charge;
    this rate produces the claims.  Their difference is the *Risikoergebnis*.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Expected surrenders in month t, on the survivors of the month's deaths.

    Zero in the last month by construction, where the whole surviving cohort is booked as
    :func:`pols_maturity` instead.
    """
    return pols_if_at(t, "AFT_DEATH") * lapse_rate_mth(t)


def pols_maturity(t):
    """Policies reaching *Rentenbeginn*: zero except in the last projected month.

    At ``t = proj_len() - 1`` it is the whole surviving cohort,
    ``pols_if_at(t, "AFT_DECR")``, since the lapse rate is zero there.  Named
    ``pols_maturity`` and not ``pols_expiry`` per the library's register: it is the count
    whose cover ends at the scheduled end of the contract, and what is paid for it is
    ``claims(t, "MATURITY")``.
    """
    if t < proj_len() - 1:
        return 0.0
    return pols_if_at(t, "AFT_DECR")


# ----------------------------------------  cash flows

def premiums(t):
    """Gross premium income in month t, including any *Zuzahlung*.

    ``(prem_pp(t) + topup_pp(t)) x pols_if(t)``.  It is published because the reader needs
    it, and it is **excluded from** :func:`net_cf`: almost all of it is the *Anlagebeitrag*,
    which is the policyholder's money passing into the unit fund.  What the insurer keeps
    out of it is :func:`charge_acq` and :func:`charge_admin_prem`, and
    :func:`check_prem_split` asserts that the three account for the whole premium.
    """
    return (prem_pp(t) + topup_pp(t)) * pols_if(t)


def prem_to_av(t):
    """The *Anlagebeitrag* credited to the unit fund in month t, in force."""
    return prem_to_av_pp(t) * pols_if(t)


def charge_acq(t):
    """*Abschluss- und Vertriebskosten* collected in month t, in force.

    Zero for ``t >= 60`` on every model point but 9, where a *Zuzahlung* books its
    *Zuzahlungskosten* here — ``charge_acq(120) = 312.63``.  Zero at every projected month
    of an in-force cell that opens past the window.
    """
    return charge_acq_pp(t) * pols_if(t)


def charge_admin_prem(t):
    """*Beitragsbezogene Verwaltungskosten* collected in month t, in force."""
    return charge_admin_prem_pp(t) * pols_if(t)


def charge_admin_fund(t):
    """*Kapitalbezogene Verwaltungskosten* collected in month t, in force.

    The charge that survives *Beitragsfreistellung*, and the one that grows with the fund
    — on a thirty-year contract it is the dominant term in the reduction in yield.
    """
    return charge_admin_fund_pp(t) * pols_if(t)


def charge_policy_fee(t):
    """*Stückkosten* collected in month t, in force."""
    return charge_policy_fee_pp(t) * pols_if(t)


def charge_risk(t):
    """*Risikobeitrag* collected in month t, in force.

    Priced on the first-order table.  ``sum(charge_risk) - sum(death_strain)`` is the
    *Risikoergebnis* and equals ``(1 - mort_be_factor) x sum(charge_risk)`` exactly.
    """
    return charge_risk_pp(t) * pols_if(t)


def stornoabzug(t):
    """*Stornoabzug* retained from surrenders in month t, in force.

    Income to the insurer, so it is a **plus** in :func:`net_cf`, and simultaneously part
    of the account value released — which is why it appears on both sides of
    :func:`check_benefit_funding`.  Zero on every model point but 5.
    """
    return stornoabzug_pp(t) * pols_lapse(t)


def withdrawals(t):
    """*Teilentnahmen* paid in month t, in force.

    An owner election funded entirely by cancelling the policyholder's own units, so it is
    outside :func:`net_cf` altogether.
    """
    return withdrawals_pp(t) * pols_if(t)


def claims(t, kind):
    """Benefit outgo in month t by kind: ``"DEATH"``, ``"LAPSE"`` or ``"MATURITY"``.

    ``"DEATH"``
        ``pols_death(t) x db_pp(t)`` — the closing *Fondsguthaben* plus the net amount at
        risk.
    ``"LAPSE"``
        the *Rückkaufswert*: the *Fondsguthaben*, less any *Stornoabzug*.  There is no
        formula behind it beyond that — § 169 VVG sends a fondsgebundene contract to the
        *Zeitwert*, and on a pure unit-linked contract the *Zeitwert* **is** the fund.
    ``"MATURITY"``
        the *Fondsguthaben* released at *Rentenbeginn*, whether it buys the annuity or is
        taken under the *Kapitalwahlrecht*: both routes release the same capital from this
        model.

    All three are funded from the unit fund and are therefore **outside** :func:`net_cf`;
    only the death benefit's net-amount-at-risk component, published separately as
    :func:`death_strain`, is an insurer cost.
    """
    if kind == "DEATH":
        return pols_death(t) * db_pp(t)
    elif kind == "LAPSE":
        return pols_lapse(t) * av_pp_at(t, "BEF_DECR") * (1.0 - stornoabzug_rate())
    elif kind == "MATURITY":
        return pols_maturity(t) * av_pp_at(t, "BEF_DECR")
    else:
        raise ValueError("invalid kind")


def av_releases(t):
    """The *Fondsguthaben* released from the unit fund in month t, in force.

    Every exit's closing balance plus any *Teilentnahme*.  It is the unit-side total that
    :func:`check_benefit_funding` reconciles against the benefits actually paid: the two
    differ by exactly the death strain, which the insurer funds, and by the *Stornoabzug*,
    which it retains.
    """
    return ((pols_death(t) + pols_lapse(t) + pols_maturity(t))
            * av_pp_at(t, "BEF_DECR") + withdrawals(t))


def death_strain(t):
    """The insurer's own cost of the death benefit in month t: ``pols_death(t) x nar_pp(t)``.

    The **only** part of any benefit this contract pays that is not the policyholder's own
    money.  Because the death benefit is observed before the month's *Risikobeitrag*, it is
    exactly the *riskiertes Kapital* — no more and no less — which is the discretization
    that makes the risk result a clean number.
    """
    return pols_death(t) * nar_pp(t)


def expense_acq_pp(t):
    """The issue expense per policy issued, at t = 0: ``expense_issue``, 200,00 EUR.

    The insurer's own acquisition cost **excluding the commission**, which is
    :func:`comm_acq_pp` — the split :func:`expenses` and :func:`commissions` publish
    separately, and which is why this cells is not the whole 2 000,00 EUR of acquisition
    cash that leaves at inception.

    It falls at ``t = 0``, the inception month, and only there, so an in-force model point
    whose frame opens at ``t = 96`` never incurs it.
    """
    if t != 0:
        return 0.0
    return expense_issue                                             # noqa: F821


def comm_acq_pp(t):
    """The *Abschlussprovision* per policy issued, at t = 0: ``comm_acq_rate x S``.

    On the anchor cell 2.50 % of a 72 000,00 EUR *Beitragssumme* = **1 800,00 EUR**, and
    zero at every other month.

    The commission is set **equal to the acquisition charge** deliberately, both at 2.50 %
    of the *Beitragssumme*: the insurer pays it at inception and recovers exactly that,
    undiscounted, over the following sixty months, so the model shows in one number the
    financing problem the *Höchstzillmersatz* and the five-year spread exist to regulate.
    No German commission scale was established, so any other level would be an unsourced
    number pretending to be an observation.

    ``comm_acq_rate`` is a **flat scalar**, so that equality holds on ``std_gross`` and
    fails on the two low-load tariffs: on ``std_netto`` and ``std_low`` the assumed
    commission exceeds the tariff's own acquisition charge and those cells carry a
    projected loss.  That is the flat assumption showing, not a product fact — a real
    *Nettotarif* pays **no** acquisition commission at all, the adviser being paid a fee
    by the client under a separate *Vergütungsvereinbarung*.  It is left flat because the
    alternative is a second unsourced commission scale, and it is said here rather than
    left to be discovered in a negative ``net_cf`` total.

    It falls at ``t = 0``, the inception month, and only there, so an in-force model point
    whose frame opens at ``t = 96`` never incurs it.
    """
    if t != 0:
        return 0.0
    return comm_acq_rate * beitragssumme()                           # noqa: F821


def expense_maint_pp(t):
    """Maintenance expense per policy in month t, inflating from inception.

    ``expense_maint_mth x (1 + expense_infl)^(t/12)`` — 4,00 EUR a month at 2 % p.a., and
    exactly 4,00 EUR in the inception month ``t = 0``.  Inflated off the policy month
    rather than the projection's own start, so an in-force cell picks up the inflation its
    elapsed duration has already accrued.
    """
    return expense_maint_mth * (1.0 + expense_infl) ** (t / 12.0)     # noqa: F821


def expenses(t):
    """Total insurer expense in month t, **excluding commission**.

    Five components: the issue expense at ``t = 0``; the inflating monthly maintenance
    expense; and the per-event expenses of a death, a surrender and an annuitisation.

    Commission is **not** in here.  It is :func:`commissions`, its own
    :func:`result_cf` column, and :func:`net_cf` subtracts the two separately — the delib
    convention, and the opposite of the frlib chassis, where commission sits inside the
    expense total.  Folding it back in while leaving the ``commissions`` column in the
    frame would charge it twice.
    """
    return (expense_acq_pp(t) * pols_if(t)
            + expense_maint_pp(t) * pols_if(t)
            + expense_claim * pols_death(t)                          # noqa: F821
            + expense_surr * pols_lapse(t)                           # noqa: F821
            + expense_annuitisation * pols_maturity(t))              # noqa: F821


def commissions(t):
    """Commission outgo in month t, published beside :func:`expenses`.

    The *Abschlussprovision* at ``t = 0`` — :func:`comm_acq_pp` on the count in force in
    that month, and nil on an in-force model point whose frame opens later, the commission
    being sunk — plus the *Bestandsprovision* ``comm_renew_rate x prem_pp(t)`` on every
    gross *Beitrag* collected.  Both **[std]**: no German unit-linked commission scale was
    established.
    """
    return (comm_acq_pp(t) * pols_if(t)
            + comm_renew_rate * prem_pp(t) * pols_if(t))             # noqa: F821


def net_cf(t):
    """The **non-unit** net cash flow in month t, income positive.

    ``charges collected + stornoabzug - expenses - commissions - death_strain``.  Every
    benefit paid before *Rentenbeginn* is funded by cancelling the policyholder's own units
    and is therefore absent from this line; what the insurer earns is the charge stack and
    what it bears is its own expenses, its commission and the net amount at risk.

    On the anchor cell the inception month ``t = 0`` is **-1 966,22 EUR** — the acquisition
    commission and the issue expense both fall there while the acquisition charge that
    funds them arrives over sixty months — after which the margin turns positive and grows
    with the fund.
    """
    return (charge_acq(t) + charge_admin_prem(t) + charge_admin_fund(t)
            + charge_policy_fee(t) + charge_risk(t) + stornoabzug(t)
            - expenses(t) - commissions(t) - death_strain(t))


def liability_cf(t):
    """The same stream outgo positive, ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: the non-unit best estimate is
    ``sum v(t) x liability_cf(t)`` over whatever discount curve it supplies, with the unit
    liability — the *Fondsguthaben* itself, backed one-for-one by the *Anlagestock* —
    added at market value.  This model discounts nothing.
    """
    return -net_cf(t)


# ----------------------------------------  Rentenbeginn and the reduction in yield

def rentenfaktor_guar():
    """The *garantierter Rentenfaktor*: euro of monthly annuity per 10 000 EUR of fund.

    Read from ``rentenfaktor_table.csv`` at **``annuity_age()``**, not at
    ``age(proj_len() - 1)``, which is one lower: the annuity begins at the *end* of the
    last projected month.  On the anchor cell 25.00 at age 67; the off-by-one would fetch
    24.45.

    **[std]** and derived rather than observed — ``10 000 / (12 T_eff)`` at a 0 %
    *Rechnungszins* — and it is fixed for the life of the contract.  A reduction under
    § 163 VVG with an independent *Treuhänder*'s confirmation is recorded as a model risk
    and not implemented.
    """
    return float(data.rentenfaktor_table().loc[                      # noqa: F821
        (rentenfaktor_id(), annuity_age()), "rentenfaktor_guar"])


def rentenfaktor_curr():
    """The *aktueller Rentenfaktor* on the insurer's tariff at *Rentenbeginn*.

    Equal to the guaranteed factor on ``std_2026``, so the ``max()`` is exercised without
    injecting an unsourced uplift, and 12 % higher on ``rich_current``, where it visibly
    bites.  Both are **[std]**.
    """
    return float(data.rentenfaktor_table().loc[                      # noqa: F821
        (rentenfaktor_id(), annuity_age()), "rentenfaktor_curr"])


def rentenfaktor_applied():
    """``max(rentenfaktor_guar(), rentenfaktor_curr())`` — the factor actually applied.

    The German rule is a **guarantee with upside**: the guaranteed factor is a floor, and
    where the insurer's current tariff is richer at *Rentenbeginn* the current one applies.
    A model that applies only the guaranteed factor understates the benefit whenever that
    happens.

    Note what is and is not guaranteed here.  Only the **conversion terms** are; the
    capital they multiply is the market's.  A guaranteed *Rentenfaktor* is therefore not a
    guaranteed pension, and any document implying otherwise is wrong.
    """
    return max(rentenfaktor_guar(), rentenfaktor_curr())


def av_maturity_pp():
    """The *Fondsguthaben* per policy at *Rentenbeginn*.

    ``av_pp_at(proj_len() - 1, "BEF_DECR")``: the closing balance of the frame's last
    month, after that month's charges.  It is what the surviving cohort releases, and what
    the *Rentenfaktor* converts.
    """
    return av_pp_at(proj_len() - 1, "BEF_DECR")


def annuity_mth_pp():
    """The monthly annuity the *Fondsguthaben* buys at *Rentenbeginn*, per policy.

    ``av_maturity_pp() / 10 000 x rentenfaktor_applied()``.

    **This model stops here.**  The annuity is published, not projected: the payout phase —
    the *Überschussrente*, the *Rentengarantiezeit*, the *Rentenbezugskosten* — belongs to
    ``products/sofortrente/``.  Under the *Kapitalwahlrecht* the same capital is taken as a
    lump sum instead, which is why that flag changes no cash flow here.
    """
    return av_maturity_pp() / 10000.0 * rentenfaktor_applied()


def gross_return_ref():
    """The reference gross fund return over the projection, annualised.

    The geometric mean of the scenario's **gross** returns over the projected months,
    before the TER and before every policy charge.  It is the yardstick the reduction in
    yield is measured against, and on a level path it is simply that path's rate — 5.00 %
    on the base scenario.
    """
    prod = 1.0
    for t in range(proj_start(), proj_len()):
        prod *= (1.0 + fund_return_gross_ann(t)) ** (1.0 / 12.0)
    return prod ** (12.0 / (proj_len() - proj_start())) - 1.0


def irr_ann():
    """The internal rate of return the policyholder's own money earns, annualised.

    Solved by bisection on a **single persisting contract** — no survivorship and no lapse
    — because a reduction in yield is a statement about one policy rather than about a
    cohort.  The premiums and any *Zuzahlung* are accumulated from the start of their month
    to *Rentenbeginn*, any *Teilentnahme* is accumulated from the end of its month and
    subtracted, and an in-force cell's opening *Fondsguthaben* enters as an inflow at the
    projection's start; the accumulated value is matched to :func:`av_maturity_pp`.

    The opening-fund term matters only on an in-force model point — it is zero on every
    new-business cell — but without it the measure would credit that cell's charges with
    growing money the projection never received.
    """
    n = proj_len()
    t0 = proj_start()
    flows = [(prem_pp(t) + topup_pp(t), (n - t) / 12.0)
             for t in range(t0, n)]
    flows += [(-withdrawals_pp(t), (n - 1 - t) / 12.0) for t in range(t0, n)]
    flows += [(av_pp(t0), (n - t0) / 12.0)]
    target = av_maturity_pp()
    lo, hi = -0.99, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if sum(a * (1.0 + mid) ** m for a, m in flows) - target > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def reduction_in_yield():
    """The charge stack expressed as an annual reduction of the contract's return.

    ``gross_return_ref() - irr_ann()``.  The product's defining metric, because on a
    contract with no *Rechnungszins* the charge stack **is** the economics: everything the
    policyholder does not get is either a charge or the fund's own TER, and this number is
    both of them together.

    **It is a delib-defined measure and it is not the statutory *Effektivkostenquote***.
    The German figure is aligned to the total-cost-indicator method of the PRIIPs RTS over
    a specified recommended holding period, and this model implements neither.  Any level
    it produces is arithmetic on this library's own **[std]** charge stack and **must never
    be quoted as a market figure**.
    """
    return gross_return_ref() - irr_ann()


# ----------------------------------------  the published identities

def check_net_cf_resid(t):
    """The residual of the cash flow statement's own reconciliation in month t; zero.

    **delib's first ruling.**  ``net_cf(t)`` must be reconstructible from the parts
    :func:`result_cf` publishes, so that the headline number of a cash flow model is not
    the one quantity nothing checks.  The identity is::

        net_cf = charge_acq + charge_admin_prem + charge_admin_fund
                 + charge_policy_fee + charge_risk + stornoabzug
                 - expenses - commissions - death_strain

    and this residual rebuilds the first two terms **by a different route** — as
    ``premiums - prem_to_av``, which is what the *Beitragsverrechnung* leaves behind —
    so the check crosses the unit / non-unit boundary rather than restating the formula.
    A charge added to the ledger and not to ``net_cf``, or an account-value benefit
    wrongly booked as an insurer outgo, fails here.
    """
    rebuilt = (premiums(t) - prem_to_av(t)
               + charge_admin_fund(t) + charge_policy_fee(t)
               + charge_risk(t) + stornoabzug(t)
               - expenses(t) - commissions(t) - death_strain(t))
    return net_cf(t) - rebuilt


def check_net_cf():
    """True when the cash flow statement reconciles in every projected month.

    No argument, one bool over all t, the library-wide shape;
    :func:`check_net_cf_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_net_cf_resid(t)) <= val_tol * max(1.0, abs(net_cf(t)))  # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_prem_split_resid(t):
    """The *Beitragsverrechnung* residual in month t; zero.

    ``premiums - (prem_to_av + charge_acq + charge_admin_prem)``.  What is withheld from a
    German unit-linked premium is the acquisition instalment and the premium-based
    administration charge, and what is left buys units: nothing else may come out of the
    premium.  A model that also netted the *Stückkosten* or the fund-based charge out of
    the *Beitrag* — the single most common way to get this product wrong — fails here.
    """
    return premiums(t) - (prem_to_av(t) + charge_acq(t)
                          + charge_admin_prem(t))


def check_prem_split():
    """True when the premium splits exactly three ways in every projected month."""
    return all(abs(check_prem_split_resid(t))
               <= val_tol * max(1.0, abs(premiums(t)))               # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_units_roll_fwd_resid(t):
    """The unit roll-forward residual at the end of month t; zero.

    ``units_pp(t+1) - (units_pp(t) + units_bought_pp(t) - units_cancelled_pp(t))``.

    **This identity has no price term in it at all**, which is what makes it worth
    publishing beside :func:`check_av_roll_fwd_resid`.  Units move only when they are
    bought or cancelled, so a charge taken in euro without cancelling the matching units
    fails here while every euro total in the frame still looks plausible.
    """
    return units_pp(t + 1) - (units_pp(t) + units_bought_pp(t)
                              - units_cancelled_pp(t))


def check_units_roll_fwd():
    """True when the unit count rolls forward exactly in every projected month."""
    return all(abs(check_units_roll_fwd_resid(t))
               <= val_tol * max(1.0, abs(units_pp(t)))               # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_av_roll_fwd_resid(t):
    """The account-value roll-forward residual in month t; zero.

    ``av_pp_at(t, "BEF_DECR") - [ (av_pp(t) + prem_to_av_pp(t)) (1 + i(t))
    - charges - withdrawal ]``.

    The companion to :func:`check_units_roll_fwd_resid`, and not redundant with it: this
    one **carries the price**, so it fails if the month's return is applied at the wrong
    point in the order — to the fund before the premium is credited, or after the charges
    are taken instead of before.  An implementation can pass either identity alone.
    """
    rolled = ((av_pp(t) + prem_to_av_pp(t)) * (1.0 + fund_return_net_mth(t))
              - charge_admin_fund_pp(t) - charge_policy_fee_pp(t)
              - withdrawals_pp(t) - charge_risk_pp(t))
    return av_pp_at(t, "BEF_DECR") - rolled


def check_av_roll_fwd():
    """True when the *Fondsguthaben* rolls forward exactly in every projected month."""
    return all(abs(check_av_roll_fwd_resid(t))
               <= val_tol * max(1.0, abs(av_pp_at(t, "BEF_DECR")))   # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_benefit_funding_resid(t):
    """The unit / non-unit funding residual in month t; zero.

    ``claims_death + claims_lapse + claims_maturity + withdrawals + stornoabzug
    - (av_releases + death_strain)``.

    Everything this contract pays before *Rentenbeginn* comes from one of exactly two
    places: the policyholder's own *Fondsguthaben*, or the insurer's pocket.  This
    identity says so arithmetically, and it is the check that catches the product's
    first-order failure mode — booking the whole account value as an insurer outgo, which
    would leave every column in the frame looking reasonable and the liability overstated
    by the entire fund.
    """
    return ((claims(t, "DEATH") + claims(t, "LAPSE") + claims(t, "MATURITY")
             + withdrawals(t) + stornoabzug(t))
            - (av_releases(t) + death_strain(t)))


def check_benefit_funding():
    """True when every benefit is funded from the fund or the insurer, in every month."""
    return all(abs(check_benefit_funding_resid(t))
               <= val_tol * max(1.0, abs(av_releases(t)))            # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero.

    ``pols_if(t) - (pols_death(t) + pols_lapse(t) + pols_maturity(t) + pols_if(t+1))``.
    Everyone who starts a month either dies, surrenders, reaches *Rentenbeginn* or is
    still there at the start of the next one.  Summed over the projection it is the
    closure identity — the three exits account for the whole opening cohort — and at
    ``t = proj_len() - 1`` it is what the ``lapse_rate_mth(proj_len() - 1) = 0``
    convention closes.
    """
    return pols_if(t) - (pols_death(t) + pols_lapse(t) + pols_maturity(t)
                         + pols_if(t + 1))


def check_pols_roll_fwd():
    """True when the in-force count rolls forward exactly in every projected month."""
    return all(abs(check_pols_roll_fwd_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(proj_start(), proj_len()))


def check_acq_charge_resid(t):
    """The acquisition-charge ledger residual at the end of month t; zero.

    ``cum_charge_acq_pp(t)`` against an expectation **counted rather than accumulated**:
    the number of instalment dates elapsed, times the instalment, plus the
    *Zuzahlungskosten* on any *Zuzahlung* already received.  Because the count is closed
    form and the ledger is a recursion, the two disagree if the window runs one month too
    long, if a shortened premium term is still spread over sixty months, or if an
    instalment is charged in a month with no premium.

    At ``t = proj_len() - 1`` on a new-business cell it says that the whole acquisition
    charge has been collected and no more: ``alpha_rate x beitragssumme()`` exactly, which
    on the anchor is 1 800,00 EUR.
    """
    if prem_form() == "einmal":
        elapsed = 1 if t >= proj_start() else 0
    else:
        hi = min(t, acq_window_months() - 1)
        if pup_month() > 0:
            hi = min(hi, pup_month() - 1)
        elapsed = 0 if hi < proj_start() else (
            (hi - proj_start()) // prem_mode_months() + 1)
    instalment = (charge_acq_total() / acq_instalments()
                  if acq_instalments() else 0.0)
    topups = (topup_amount()
              if 0 < topup_month() <= t and topup_month() >= proj_start()
              else 0.0)
    return cum_charge_acq_pp(t) - (elapsed * instalment
                                   + zuzahlung_charge_rate() * topups)


def check_acq_charge():
    """True when the acquisition-charge ledger matches its counted expectation everywhere."""
    return all(abs(check_acq_charge_resid(t))
               <= val_tol * max(1.0, charge_acq_total())             # noqa: F821
               for t in range(proj_start(), proj_len()))


# ----------------------------------------  result tables

def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month count and is the weight applied to every cash flow
    on the same row, so dividing a flow by it recovers the per-policy amount.  The frame
    is ``range(proj_start(), proj_len())`` — ``t = proj_start() ... proj_len() - 1`` — and
    stops there: the end of the last month is *Rentenbeginn*.

    The columns fall into three groups and the grouping is the point.  ``premiums`` and
    ``prem_to_av`` are the money coming in and the part of it that goes straight into the
    unit fund.  The six ``charge_*`` columns plus ``stornoabzug`` are what the insurer
    keeps.  ``claims_*``, ``withdrawals`` and ``av_releases`` are the unit fund paying
    itself out, and are **excluded from** ``net_cf`` — only ``death_strain``, the net
    amount at risk the insurer funds, crosses over.  ``expenses`` and ``commissions`` are
    two columns and not one: ``expenses`` excludes commission on every delib model that
    has a commission to publish.  ``liability_cf`` is ``net_cf`` outgo positive, published
    so the sign convention is verifiable in the frame.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "prem_to_av": [prem_to_av(t) for t in ts],
            "charge_acq": [charge_acq(t) for t in ts],
            "charge_admin_prem": [charge_admin_prem(t) for t in ts],
            "charge_admin_fund": [charge_admin_fund(t) for t in ts],
            "charge_policy_fee": [charge_policy_fee(t) for t in ts],
            "charge_risk": [charge_risk(t) for t in ts],
            "stornoabzug": [stornoabzug(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "av_releases": [av_releases(t) for t in ts],
            "death_strain": [death_strain(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_fund():
    """Result table of the unit fund and the decrements, indexed by policy month t.

    The per-policy view the cash flow table weights: the *Anteilspreis*, the unit count,
    the four within-month *Fondsguthaben* balances, the *Beitragsrückgewähr* base, the net
    amount at risk, and the three decrement rates.  This is roughly what a German
    *Standmitteilung* reports, which is not a coincidence — the statement's line items are
    this model's state vector.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "unit_price": [unit_price(t) for t in ts],
            "units_pp": [units_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "av_pp_bef_charge": [av_pp_at(t, "BEF_CHARGE") for t in ts],
            "av_pp_aft_charge": [av_pp_at(t, "AFT_CHARGE") for t in ts],
            "av_pp_aft_wd": [av_pp_at(t, "AFT_WD") for t in ts],
            "av_pp_bef_decr": [av_pp_at(t, "BEF_DECR") for t in ts],
            "cum_prem_pp": [cum_prem_pp(t) for t in ts],
            "db_floor_pp": [db_floor_pp(t) for t in ts],
            "nar_pp": [nar_pp(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "mort_rate_tariff_mth": [mort_rate_tariff_mth(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 0.75

lapse_cap = 0.4

lapse_dyn_beta = 0.0

mmkt_return_ann = 0.015

glide_months = 60

comm_acq_rate = 0.025

expense_issue = 200.0

expense_maint_mth = 4.0

expense_infl = 0.02

comm_renew_rate = 0.015

expense_claim = 150.0

expense_surr = 50.0

expense_annuitisation = 100.0

roll_fwd_tol = 1e-10

val_tol = 1e-10

pd = ("Module", "pandas")
