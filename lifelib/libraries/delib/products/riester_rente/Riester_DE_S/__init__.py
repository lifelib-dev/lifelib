# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German klassische Riester-Rentenversicherung.

:mod:`~.Riester_DE_S` is the executable counterpart of
``products/riester_rente/technical-notes.md`` in the lifelib-products delib library. It
projects gross best-estimate liability cash flows, undiscounted, for a single-policy
model point of a **certified Altersvorsorgevertrag under the AltZertG** — Schicht 2 of
the German pension system — on a **monthly** grid, through both phases of the contract:
the accumulation of a *Deckungskapital* with *Überschussbeteiligung*, and the lifelong
*Leibrente* the capital is converted into at *Rentenbeginn*.

Three things make this the Riester model rather than a translated Schicht-3 one.

**The state pays part of the premium, and it is a cash flow.** The *Zulage* is a
contribution paid by the *Zentrale Zulagenstelle für Altersvermögen* to the provider and
credited to the contract; it is not a benefit and it is not a tax refund. It is published
in its own ``zulagen`` column beside ``premiums``, never folded into it, because a
statement that folds the two cannot answer the one question this product is about. The
entitlement is driven by two **different** lags — the *Mindesteigenbeitrag* looks back one
*calendar* year for income, the cash arrives one *projection* year late — and collapsing
them into one is the first listed modeling pitfall.

**There is a 100 % Beitragsgarantie, and it is tested exactly once.** ``guar_pp(k)``
accumulates every *Altersvorsorgebeitrag* credited — the saver's own contribution, the
Zulagen, and any unsubsidised contribution above the § 10a ceiling — less the biometric
carve-out capped at 20 % of total contributions. It is compared with the account **only**
at *Rentenbeginn*, where ``garantieluecke_conv_pp()`` is the shortfall the insurer funds.
``garantieluecke_pp(k)`` is published for every ``k`` as a **diagnostic**: it is normally
positive in the early durations of any charged contract, and flooring a death, surrender
or transfer benefit at it is a modeling error, not prudence.

**The payout phase is part of the liability.** Conversion at ``k_conv()`` strikes the
capital, the *Schlussüberschussanteil*, the *Bewertungsreserven* share and the applied
*Rentenfaktor*, elects the *Teilkapitalauszahlung* of up to 30 %, and applies the
*Kleinbetragsrente* test — which is **computed rather than assumed**, so the commutation
rate on a book is an output. The annuity then runs on a **generational** second-order
annuitant basis to ``omega_age``, one **monthly** instalment at a time, with the
*Rentengarantiezeit* — ``12m`` guaranteed instalments — changing who is paid and never how
much.

**Spaces.** The model contains two:

:mod:`~.Riester_DE_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Riester_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the worked example's anchor cell. It reaches the
    input tables through its ``data`` Reference, which resolves to the single
    :mod:`~.Riester_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: plain CSVs in the model folder's parent directory, read at
run time rather than stored inside the model. The model folder itself holds no data — no
``_data/``, no IOSpec, no embedded values — so a diff of the model shows logic changes
only, and the model and its inputs must travel together.

**Projection basis.** Monthly steps over a contract that is almost entirely annual, so the
model runs on **two clocks** and the argument of a cells says which. ``t`` counts projection
**months** from the 1 January 2027 valuation date and is **0-based**, running
``0 ... proj_len() - 1`` with ``proj_len() = 12 x proj_len_y()`` and
``proj_len_y() = omega_age - age(0) + 1``; ``k = proj_year(t) = t // 12`` is the projection
**year**, and the contractual contract year is ``duration_y(k) + 1 = duration_init() + k
+ 1``, which is ``k + 1`` only on a point projected from its own inception
(``duration_init() == 0``).

The annual clock is the contract's own in every respect that matters: the Zulage is an
annual entitlement determined on a calendar year and paid once by the ZfA, the *Überschuss*
is declared annually, the two charges and the interest credit fall once a year, and the
*Beitragsgarantie* is tested once. The *Eigenbeitrag* keeps it too, because the
*Ratenzuschlag* prices a fractionated payment mode by loading the **amount** rather than by
moving the contribution year. The monthly clock carries the in force, the three decrements,
the claims, the expenses, the commission and the *Rente* instalments.

The decrements carry the library's two speeds — ``mort_rate``, ``lapse_rate`` and
``transfer_rate`` are the **annual** rates and ``*_mth`` their geometric twelfths — so
twelve months compound back to each annual rate exactly and the whole accumulation is
**bit-identical** to the annual-step model this replaced, on all thirteen model points:
every contribution, both balances, the guarantee accumulator, the capital at *Rentenbeginn*,
the *Garantielücke* and the *Kleinbetragsrente* verdict are unchanged. What the finer grid
buys is the *Leibrente*, which the AltZertG requires to be lifelong and monthly and which
the annual model compressed into one payment at the start of each payout year on that
year's opening count — worth 361,74 € of the anchor's annuity outgo and 573,50 € of model
point 12's, which has no *Rentengarantiezeit* to hold the count still. It also dates the
three accumulation exits, which now compete month by month instead of running in sequence
at one year end: 5,62 € moves off the anchor's death outgo and 2,64 € off its surrender
outgo onto 8,30 € of transfers.

**What is sourced and what is not.** The statutory mechanics are cited: who is
*zulageberechtigt*, the *Grundzulage* / *Kinderzulage* / *Berufseinsteiger-Bonus*
structure, the § 86 *Mindesteigenbeitrag* with its 4 % rate, its 2 100 € ceiling, its
60 € *Sockelbeitrag* floor and its **proportional** Kürzung, the ZfA payment lag, the
*Beitragserhaltungszusage*, the 30 % *Teilkapitalauszahlung* cap, the five-year floor on
acquisition-cost spreading, the *Wechselrecht*, the *Kleinbetragsrenten-Abfindung* and
the *schädliche Verwendung* consequences of a *Kündigung*. **No carrier-specific
parameter was established for any German Riester product, at any house, for any year**,
so every charge, every declared rate, every *Rentenfaktor*, every behavioural rate and
both decrement tables are standardizations marked ``[std]`` in the shipped CSVs and in
the notes. The DAV tables (DAV 2008 T, DAV 2004 R) are the property of the Deutsche
Aktuarvereinigung, are not public and are **not redistributed here**: they are cited by
name and stood in for by anchored proxies, and :mod:`~.Riester_DE_S.Data` says what a
replacement must preserve. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the decrement, charge and surplus tables with company data
before drawing any conclusion from the output.

**Model points.** Thirteen, covering both contribution forms, all four payment
frequencies, an at-inception point beside the in-force ones, both *Kinderzulage* rates
running at once, the *Sockelbeitrag* floor, the *Berufseinsteiger-Bonus*, the § 86
proportional Kürzung, an unsubsidised second contribution pool, the 20 % biometric
carve-out cap, a *Beitragsfreistellung*, a stressed declared rate on which the
*Garantielücke* binds, a pure lifelong annuity with no lump sum and no guarantee period,
and a late entrant at the statutory earliest *Rentenbeginn* of 62. Model point 1 is the
anchor cell of the worked example in the technical notes.

**Verification.** ``tests/test_riester_rente_de.py`` asserts the notes' worked example to
the cent and ``pols_if`` to six decimals, and one test per listed modeling pitfall. The
model publishes six ``check_*`` identities — ``check_net_cf``, ``check_av_roll_fwd``,
``check_guar_roll_fwd``, ``check_pols_roll_fwd``, ``check_conversion`` and
``check_zulage_lag`` — and the library's conventions suite calls all six on every model
point. Their residuals follow their cells' clock: the cash flow statement and the policy
ledger take a **month**, and the account, the guarantee accumulator, the conversion and the
ZfA lag take a projection **year**, because the quantities they check move once a year.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/riester_rente/Riester_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Riester_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
