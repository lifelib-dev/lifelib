# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the French euro support (fonds en euros).

:mod:`~.Euro_FR_S` is the executable counterpart of
``products/assurance_vie_euro/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for single model points on the euro
support of a `contrat d'assurance vie` — the standardized composite specified in
``product-spec.md``, not any single insurer's fund — together with the two state
variables that make the product what it is: the `épargne acquise` and the `provision
pour participation aux bénéfices` (PPB).

**The rate is an allocation, not an assumption.** That sentence is the model. Every
year the insurer builds the `compte de participation aux résultats` that art. A132-11
of the Code des assurances prescribes — 85% of the `compte financier`, plus the
`compte technique` less the greater of 10% of it and 4.5% of premiums — and the whole
of that balance must reach policyholders. What the insurer chooses is only *when*: what
it does not credit this year is carried to the PPB, and what it carried in an earlier
year it may credit now. The credited rate `taux servi` is therefore the statutory floor
moved up or down by the PPB lever, floored again by the `taux minimum garanti`, and
never by an assumption typed into a table.

**The eight-year clock is a deadline, not an average.** A dotation carried to the PPB in
financial year ``v`` must be applied to mathematical provisions or paid to policyholders
within the eight financial years that follow. The model therefore carries a **per-vintage
ledger**, ``ppb_vintage_pp(y, v)`` on the financial-year clock, released oldest-first,
so that the clock is a real date on a real balance. Modelling the PPB as a single pot
with an average age would meet the eight-year rule on average and breach it on every
vintage.

**The `effet cliquet` is asserted, not assumed.** Credited `participation aux bénéfices`
is definitively acquired and cannot be called back, so ``check_cliquet()`` asserts that
the credited interest is never negative and that the cumulative-PB ledger never falls.
What the ratchet does *not* say is that the account never falls: under the `garantie
nette` the `frais de gestion sur encours` keeps biting in a nil-PB year, and both
statements are true at once.

**Spaces.** The model contains two:

:mod:`~.Euro_FR_S.Data`
    Reads the four input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Euro_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the notes' worked example. It reaches the input
    tables through its ``data`` Reference, which resolves to the single
    :mod:`~.Euro_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed
there would re-read every file for every policy. In ``Data`` they are evaluated once,
however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, because the movements the contract actually bills
monthly — the `versements libres programmés`, the `rachats partiels programmés` — and
the decrements that end a contract are continuous, while the crediting machinery is not.
``t`` counts policy **months** from the valuation date and is **0-based**: ``t = 0`` is
the first projected month, month ``t`` runs from time ``t / 12`` to ``(t + 1) / 12``, and
the frame is ``t = 0 … proj_len() − 1`` with ``proj_len() = 12 * proj_years = 480``
months. The contractual policy year is the 1-based label derived from it,
``policy_year(t) = duration_init + t // 12 + 1``, and the attained age — age last
birthday — is ``issue_age + duration_init + t // 12``, so both step at the policy
anniversary and never inside the year. `Versements` and `rachats partiels` fall at the
beginning of the month, the insurer's expense accrues through it, and deaths and
`rachats totaux` act at its end, deaths first.

Underneath that grid the product carries an **annual layer**, indexed by the projection
year ``y = t // 12``, and it is left whole. The `participation aux bénéfices` is fixed
for the closing financial year and credited at 31 December value date, the art. A132-16
PPB clock counts financial years, and the `frais de gestion` and the `prélèvements
sociaux` land with the interest they are struck on — so the whole of the year's
revalorisation, charge and levy arrives in the anniversary month, ``is_anniv(t)``, and
eleven months of twelve carry none of it. The crediting base ``pm_avg_pp(y)`` is built
from the twelve monthly movements at the mid-month weight ``(11.5 − k)/12``, the twelve
weighted twelfths of which sum to exactly one half — so the notes' ``AV + 0.5 P − 0.5 W``
is derived here rather than asserted. Decrements follow the library's two-speed convention:
``mort_rate(t)`` and ``lapse_rate(t)`` are the **annual** rates of the policy year
containing month ``t``, and ``mort_rate_mth(t)`` and ``lapse_rate_mth(t)`` are the
monthly rates actually applied, ``1 − (1 − r)^(1/12)``.

Because those monthly rates compound back to the annual ones and every contractual event
sits on a year boundary, the in force and every financial-year quantity **at every
anniversary** are exactly what the annual-step model this replaced carried. The cash
flows are not, and are not meant to be: instalments are collected from a block that
decrements every month, expenses accrue where they are incurred, and a claim falls at the
end of the month of exit — which also means a mid-year `dénouement` is now paid the
account value **without** the year's `taux servi`, the contractual floor rate `pro rata
temporis` at the nil TMG every model point carries, rather than the full year's credit an
annual grid was forced to give it. ``result_cf_annual()`` sums the frame into projection
years so the two can be read side by side.

**`Prélèvements sociaux` are inside the account and outside ``net_cf``.** The 17.2% levy
is withheld as the interest is credited, every year, because the rights are expressed in
euros — this is the euro fund's signature mechanic and the commonest foreign-model
error. It sits inside the account roll-forward, because it is money that genuinely
leaves the contract; it sits outside ``net_cf``, because it is a policyholder tax the
insurer remits to the State rather than a benefit or an insurer expense. It has its own
``soc_levy`` column so a fund-level asset projection can add it back in one step.

**What is sourced and what is not.** The mechanics are sourced: the A132-11 split and
which limb attaches to which account, the A132-12 minimum benefit, the eight-year PPB
release horizon, the `effet cliquet`, the `garantie nette` capital floor and its
measurement before levies, the death benefit being the account value and nothing more,
the absence of a surrender charge, and the annual timing of the social levies. Every
*rate* is a standardization: no insurer publishes its dotation or release policy, no
French euro-fund lapse experience is public, no contract in the source set publishes a
TMG, and the statutory mortality tables are cited but not redistributable — the shipped
table is an INSEE-shaped proxy. **This model is a mechanics demonstration, not a pricing
or reserving result.**

**Verification.** ``tests/test_assurance_vie_euro_fr.py`` asserts the notes' worked
example row by row to the cent — the `taux servi` and PPB table, the `épargne acquise`
roll-forward, the year-5 trace at full precision, the twelve-year levy and account
identities, and the PPB clock closing exactly at its last date — and then one test per
modelling pitfall the notes list, plus the monthly grid's own invariants: that twelve
monthly decrements compound back to the annual ones, that the revalorisation and the
levy land only in the anniversary month, and that ``result_cf_annual()`` is the monthly
frame regrouped rather than a second projection.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/assurance_vie_euro/Euro_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Euro_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
