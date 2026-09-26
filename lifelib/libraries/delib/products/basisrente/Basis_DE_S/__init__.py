# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German Basisrente (Rürup), Schicht 1.

:mod:`~.Basis_DE_S` is the executable counterpart of
``products/basisrente/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows, **undiscounted**, for a single model point of
the *Basisrentenvertrag* of § 10 Abs. 1 Nr. 2 Buchst. b EStG — a deferred lifelong
annuity written on the general account, with an accumulation phase that builds a
*Deckungskapital* and a payout phase that pays a monthly annuity struck through a
*Rentenfaktor* — on a **monthly** grid, ``t = 0 ... proj_len() - 1``.

**The product is defined by prohibitions, and the model is too.** The entitlement is
*nicht vererblich*, *nicht übertragbar*, *nicht beleihbar*, *nicht veräußerbar* and
*nicht kapitalisierbar*, so there is **no surrender value at any duration, no
*Rückkaufswert*, no *Kapitalwahlrecht* and no *Teilkapitalauszahlung*** anywhere in this
model. There is no commutation of a *Kleinbetragsrente* either, but that one is a
**standardization and not a prohibition**: § 10 Abs. 1 Nr. 2 Satz 3 EStG permits the
*Abfindung* of a *Kleinbetragsrente* out of a *Basisrentenvertrag*, and ``model.md``
gives the reasons this model leaves it out. There is no ``lapse_rate``, no
``surr_rate``, no ``cv_pp``, no ``loan_pp`` and no ``claims_lapse`` column: these are
structural absences rather than switched-off options, and :func:`~.Basis_DE_S.Projection.check_no_capital`
asserts them in code rather than in prose. A modeller arriving from the endowment or the
Schicht-3 annuity chassis has one thing to unlearn, and that is it.

Three mechanics carry the rest of the model.

**A *Beitragsfreistellung* is not a lapse.** § 165 VVG survives on this contract and is
its only behavioural exit, but it removes the *premium*, not the *policy*: the contract
stays certified, stays protected and still converts at *Rentenbeginn*. The model
therefore carries two ledgers — a premium-paying cohort per policy and a premium-free
cohort at fund level — whose account values diverge from the first freeze, and
``pols_if(t+1) = pols_if(t) x (1 - mort_rate_mth(t))`` with ``bf_rate`` absent from the
identity. Treating the freeze as an exit is the second listed modeling pitfall. The
freeze itself stays annual: § 165 VVG takes effect "für den Schluss der laufenden
Versicherungsperiode" and § 12 Abs. 1 VVG makes that period the *Versicherungsjahr*, so
``pols_freeze`` is non-zero only in the last month of a projection year.

**The declared rate is the *total* credited rate, not a spread.** A German *laufende
Verzinsung* already includes the *Rechnungszins*, so ``cred_rate(k) = max(gtd_rate,
decl_rate(k))``. Adding one to the other is the sixth pitfall, and on a book spanning
seven guarantee vintages it is worth a great deal.

**The conversion basis is not the projection basis.** The whole *Deckungskapital*, plus
a *Schlussüberschussanteil* allocated at that single date, converts at *Rentenbeginn* at
``max(rentenfaktor_gtd, rf_curr(ret_age))`` — a contractual rate struck on first-order
DAV 2004 R — while the projection runs on the best estimate. The wedge between the two
is the payout phase's *Risikoüberschuss*, and ``ann_bonus_rate`` is what gives it back.
Converting on the projection's own mortality abolishes it, which is the eleventh pitfall.

**Spaces.** The model contains two:

:mod:`~.Basis_DE_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Basis_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Basis_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together — copying ``Basis_DE_S`` without its parent's
CSVs produces a model that reads and then fails on first evaluation.

**Projection basis.** Monthly steps over a contract that is almost entirely annual, so
the model runs on **two clocks** and the argument of a cells says which. ``t`` counts
projection **months** from the valuation date and is **0-based**; ``k = proj_year(t) =
t // 12`` is the projection **year**, ``duration_y(k) = duration_init + k`` the completed
policy years and ``policy_year(t) = duration(t) + 1`` the contractual label. The frame
runs ``t = 0 ... proj_len() - 1`` with ``proj_len() = 12 x proj_len_y()`` and
``proj_len_y() = omega_age() - age(0) + 1`` — to the end of the mortality table, because
the annuity is lifelong: 924 months on the anchor cell.

The in force, the decrements, the claims, the expenses and the *Rente* instalments take a
month. Everything the contract states per *Versicherungsjahr* takes a year: the
*Beitragsdynamik* step, the *Zuzahlung*, the four account charges, the annual declaration
of *Überschussbeteiligung*, the *Deckungskapital* and its interest credit, the
*Beitragsfreistellung* effective at the end of the current premium period, and the
conversion at *Rentenbeginn*. The *Beitrag* and the *Zuzahlung* fall in the first month of
a projection year and interest is credited at its end; deaths fall at the end of each
month and the *Beitragsfreistellung* transition after the deaths of the year's last month.

The decrements carry the library's two speeds — ``mort_rate(t)`` is the **annual** rate of
the year and ``mort_rate_mth(t)`` its geometric twelfth — so twelve months compound back to
the annual rate exactly and the whole *Aufschubphase* is **bit-identical** to the
annual-step model this replaced, on all thirteen model points. What the finer grid buys is
the *Rente*: a *Rentenfaktor* is quoted in euro a **month**, and where the annual model
booked twelve instalments at the start of each payout year on the opening count — its own
twelfth pitfall, and a stated approximation worth 4 290,52 € of the anchor's payout phase —
the instalment is now paid to whoever is alive at the start of each month. The
*Rentengarantiezeit* is ``12m`` instalments beginning in the month after the death that
triggered them, and a mid-year death now bears only the months of maintenance expense it
was there for.

**What is sourced and what is not.** The contractual mechanics are cited: the five
prohibitions and the absence of any surrender value, the confinement of survivor cover
to a spouse, registered partner or *Kindergeld*-eligible child, the *Beitragsfreistellung*
right, the *Höchstzillmersatz* of 25 ‰ of the *Beitragssumme*, the *Höchstrechnungszins*
ladder that fixes each cohort's ``gtd_rate``, and the statutory *Überschussbeteiligung*.
Every level is a standardization. **Not one carrier's Basisrente *Bedingungswerk*,
*Produktinformationsblatt* or declared-rate history was reached** — direct HTTP egress
was blocked and the session's search budget was exhausted before this product — so every
charge, every behavioural rate and both *Rentenfaktoren* are **[std]** figures with a
stated rationale and nothing behind them. The DAV tables (DAV 2004 R here) are the
property of the Deutsche Aktuarvereinigung, are not public, and are cited by name and
never redistributed; ``mort_table.csv`` is a shaped proxy anchored so the notes' worked
example reproduces exactly. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the decrement, charge and surplus tables with company data
before drawing any conclusion from the output.

**Model points.** Thirteen, covering both premium forms, all four payment frequencies,
all three in-force shapes (accumulating, *beitragsfrei*, already in payment), the
survivor's annuity and the *Rentengarantiezeit* separately and together, both age-floor
cohorts, four guarantee vintages, and four boundary cases — the whole *Höchstbetrag*, a
*Kleinbetragsrente* this model annuitises rather than commuting, the 50 % BUZ rule at
0.49, and a guaranteed
*Rentenfaktor* that binds over the current one. Model point 1 is the anchor cell of the
worked example in the technical notes.

**Verification.** ``tests/test_basisrente_de.py`` asserts the notes' worked example to
the cent and ``pols_if`` to six decimals, and one test per listed modeling pitfall. The
model publishes six ``check_*`` identities — :func:`~.Basis_DE_S.Projection.check_net_cf`,
:func:`~.Basis_DE_S.Projection.check_pols_roll_fwd`,
:func:`~.Basis_DE_S.Projection.check_av_roll_fwd`,
:func:`~.Basis_DE_S.Projection.check_conversion`,
:func:`~.Basis_DE_S.Projection.check_no_capital` and
:func:`~.Basis_DE_S.Projection.check_annuity_roll_fwd` — each a bool over the whole
projection with a per-period residual companion, whose argument follows its cells' clock:
the cash flow statement, the policy ledgers and the *nicht kapitalisierbar* limb take a
month, and the *Deckungskapital* roll-forward, the conversion and the *Überschussrente*
take a projection year, because the quantities they check move once a *Versicherungsjahr*.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/basisrente/Basis_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Basis_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
