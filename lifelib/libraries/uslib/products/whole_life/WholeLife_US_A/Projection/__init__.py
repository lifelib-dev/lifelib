# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WholeLife_US_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/whole_life/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WholeLife_US_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on the ``Data`` Space,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
cv_file                 data.cv_table()                 cv_table.csv
nsp_file                data.nsp_table()                nsp_table.csv
np_guar_file            data.np_guar_table()            np_guar_table.csv
mort_table_file         data.mort_table()               mort_table.csv
premium_rates_file      data.premium_rates()            premium_rates.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns
for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claim_pp(t, kind)`` and ``pols_if_at(t, timing)`` for the argument-keyed families.
The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ============================  ==========================
Notes symbol               Cells                         Meaning
=========================  ============================  ==========================
x                          age_at_entry                  Issue age (ANB)
x + t - 1                  age(t)                        Attained age at BOY of year t
x + t                      age_anniv(t)                  Attained age at anniversary t
T = 100 - x                proj_len                      Last policy year
t0                         duration_inforce              Durations already elapsed
t0 + 1                     proj_start                    First projected policy year
m                          policy_term                   Premium-paying period, years
F                          sum_assured                   Base face amount
G                          premium_pp(t)                 Gross annual premium
G^net_t                    premium_net_pp(t)             Premium after dividend offset
A_t                        rider_premium_pp(t)           PUA rider premium
i_g                        int_rate_guar                 Guarantee interest, 4.00%
i_d                        int_rate_div                  Dividend interest rate, 6.00%
i_L                        int_rate_loan                 Policy loan rate, 6.00%
q^g_{x+t-1}                mort_rate_guar(t)             Guarantee mortality
q^g_y                      mort_rate_guar_at(y)          The same, keyed by age
q^sc_{x+t-1}               mort_rate_scale(t)            Dividend-scale mortality
q^e_{x+t-1}                mort_rate(t)                  Best-estimate mortality
w_t                        lapse_rate(t)                 Surrender rate
w^dyn multiplier           dyn_lapse_factor(t)           Interest-sensitive overlay
l_{t-1}                    pols_if(t)                    In force at BOY t (weight)
l_t                        pols_if_at(t, "AFT_DECR")     In force at EOY t
l_{t-1}(1-q^e)             pols_if_at(t, timing)         In force inside year t
(none)                     pols_death(t)                 Deaths in year t
(none)                     pols_lapse(t)                 Surrenders at EOY t
(none)                     pols_maturity(t)              Maturities at T
CV_t                       cv_pp(t)                      Guaranteed cash value
F - CV_t                   net_amt_at_risk(t)            Guarantee net amount at risk
NSP_y                      nsp(y)                        Net single premium, endow 100
NP_g                       np_guar()                     Nonforfeiture net level premium
D^int_t                    div_int(t)                    Interest margin
D^mort_t                   div_mort(t)                   Mortality margin
D^exp_t (e^m_t)            div_exp(t)                    Expense margin
D_t                        div_base(t)                   Base-block dividend, floored
D^PUA_t                    div_pua(t)                    PUA-block dividend
D_t + D^PUA_t              div_credited(t)               Dividend credited at EOY t
D^cash_t                   div_cash(t)                   Cash dividend per policy
(none)                     div_to_pua(t)                 Dividend applied to PUAs
dPUAF_t                    pua_face_purch(t)             PUA face bought by dividend
dPUAF^rider_t              pua_face_rider(t)             PUA face bought by the rider
(none)                     pua_face_offset(t)            PUA face from the RPD excess
PUAF_t                     pua_face(t)                   PUA face in force at EOY t
PUACV_t                    pua_cv(t)                     PUA cash value at EOY t
DA_t                       div_accum(t)                  Dividend accumulation balance
L_t                        loan_bal(t)                   Loan balance at EOY t
(none)                     loan_int(t)                   Loan interest capitalized
(none)                     loan_draw(t)                  Net new borrowing per policy
TF                         term_blend_target             Term-blend target face
OYT_t                      oyt_face(t)                   One-year-term face in the blend
(none)                     oyt_cost(t)                   Dividend absorbed by the OYT
DB_t                       claim_pp(t, "DEATH")          Death benefit per policy
CSV_t                      claim_pp(t, "LAPSE")          Surrender value per policy
MAT                        claim_pp(t, "MATURITY")       Maturity benefit per policy
(none)                     prem_cum(t)                   Cumulative premiums paid
E_t                        expenses(t)                   Acquisition + maintenance
(none)                     premium_taxes(t)              Premium tax outgo
(none)                     premiums(t)                   Premium income
(none)                     rider_premiums(t)             PUA rider premium income
(none)                     claims(t, kind)               Benefit outgo
(none)                     div_cash_paid(t)              Cash dividend outgo
(none)                     loan_draws(t)                 Net loan advances
NetCF_t                    liability_cf(t)               Net liability CF, outgo +
(none)                     net_cf(t)                     The same, income positive
=========================  ============================  ==========================

Seven names needed care.

``mort_rate`` is the **best-estimate** rate — the one that actually decrements the
block — while the guarantee and dividend-scale rates are ``mort_rate_guar`` and
``mort_rate_scale``. All three come off the same shipped table through the References
``ae_best_est`` and ``ae_scale``. The notes call this out as a consistency trap: the
same table feeds claim outgo and the dividend's mortality margin **with opposite
signs**, so raising best-estimate mortality raises claims *and*, if the scale factor
moves with it, cuts the dividend.

``policy_term`` is the **premium-paying** period ``m``, not the coverage period.
Coverage runs to ``proj_len()`` in every variant; on the base pay-to-100 design the two
coincide, on ``PAY_10`` they do not.

``pols_lapse`` counts **surrenders**. The notes say "surrenders", ``BasicTerm_S`` says
``pols_lapse``, and ``CashValue_SE``'s ``kind`` string is ``"LAPSE"``; the model keeps
the lifelib name so the ``kind`` vocabulary stays intact.

The notes' ``CSV_t`` is the cash surrender value, not a file. It is reached as
``claim_pp(t, "LAPSE")`` so that all three benefit amounts share one cells and one
``kind`` vocabulary with ``CashValue_SE``.

``age(t)`` and ``age_anniv(t)`` are both needed: the notes index mortality at
``x + t - 1`` (the age entering policy year t) but price paid-up additions bought at the
end of that year at ``x + t``. Getting them the wrong way round shifts every dividend
purchase by a year.

``pols_if(t)`` is the **start**-of-year count — the notes' ``l_{t-1}``, not their
``l_t``. That is the library-wide convention (``Term_US_A.pols_if(1)`` is
``pols_if_init()``, ``CashValue_SE.pols_if(t)`` is ``pols_if_at(t, "BEF_MAT")``), and it
is the number every cash flow on the same ``result_cf()`` row is weighted by: the notes
themselves write every term of ``NetCF_t`` over ``l_{t-1}``. The notes' end-of-year
state variable is not lost — it is ``pols_if_at(t, "AFT_DECR")``, and
``pols_if_at(t, "AFT_DECR") == pols_if(t + 1)`` by construction.

``liability_cf(t)`` and ``net_cf(t)`` are the same stream with opposite signs — see the
sign-convention rubric below.

.. rubric:: Timing and kind arguments

``pols_if_at(t, timing)`` takes ``"BEF_DECR"`` (start of year t, before any decrement —
the same number as ``pols_if(t)``), ``"BEF_SURR"`` (after deaths, before surrenders),
``"BEF_MAT"`` (after surrenders, before maturity) and ``"AFT_DECR"`` (after every
decrement, the notes' ``l_t``) — the notes' end-of-year processing order, deaths then
dividend then surrenders then maturity. ``"BEF_DECR"`` and ``"BEF_MAT"`` are
``CashValue_SE``'s names; ``"BEF_SURR"`` is added because this product settles deaths
and surrenders in one end-of-year step, and ``"AFT_DECR"`` because ``CashValue_SE`` has
no string for the point past the last decrement, which is where the notes' state
variable lives. ``claim_pp(t, kind)`` and ``claims(t, kind)`` take ``"DEATH"``,
``"LAPSE"`` and ``"MATURITY"``. Both raise ``ValueError("invalid timing")`` /
``ValueError("invalid kind")`` on anything else.

.. rubric:: The dividend is rounded to the cent

``div_round_digits = 2`` rounds the credited base dividend before it buys paid-up
additions. This is **[std]**, and it is not cosmetic: the notes' worked example adds the
*displayed* margins (216.00 + 85.25 + 25.00 = 326.25) and then divides 326.25 by the
net single premium. Carrying the unrounded 326.248 through instead moves the purchased
paid-up-additions face from 776.79 to 776.78 — a full displayed cent, because the exact
value sits just under the rounding boundary. Declared dividends are credited in whole
cents, so the model rounds; setting ``div_round_digits = None`` turns it off and a test
pins the size of the gap in both directions.

.. rubric:: The worked example sets the PUA-block dividend aside

The notes' worked-example table computes steps 11-15 from the base-block dividend
alone, saying so explicitly: "For clarity the PUA-block dividend ``D^PUA_10`` is
omitted from this table; in the model it adds ... to the amount in step 9." The
Reference ``pua_div_on`` ships **False** so the base deterministic run reproduces the
worked example exactly, the same way ``Term_US_A`` ships ``conv_rate_base = 0``. It is
a reproduction switch, not a claim that paid-up additions are excluded from the
dividend — they are dividend-eligible, and ``pua_div_on = True`` is the
product-faithful setting. ``div_pua(t)`` implements the notes' formula either way, and
a test asserts its value on the anchor cell against the notes' own parenthetical.

.. rubric:: The four guarantee-basis tables are not one construction

The notes' first "known modeling pitfall" is a mismatch between the cash value table and
the ``NSP``/annuity functions, and prescribes regenerating every guarantee-basis
quantity from one 2017 CSO / 4% source. **The shipped tables do not satisfy that**, and
no set of tables carrying the worked example's anchors could. On any single mortality
basis at interest ``i``, endowment insurance and the annuity-due satisfy
``A_{x:n} = 1 - d ae_{x:n}`` with ``d = i/(1+i)``, so the notes' own definition collapses
to ``NNLP = 1000 d NSP_45 / (1 - NSP_45)``; the worked example's ``NNLP = 13.00`` then
forces ``NSP_45 = 0.252616``. But ``NSP_y = v(NSP_{y+1} + q_y (1 - NSP_{y+1})) >= v NSP_{y+1}``
for any ``q_y >= 0``, so ``NSP_55 <= NSP_45 (1.04)^10 = 0.373933`` — below the worked
example's ``NSP_55 = 0.42``. Read the other way: ``NSP_55 = 0.42`` forces
``NSP_45 >= 0.283737`` and hence ``NNLP >= 15.236`` per $1,000, 17% above the notes'
13.00. The worked example's steps 3 and 10 are mutually unreachable, whatever mortality
table is used.

What the shipped tables do instead **[std]**: *mort_table.csv* is an illustrative Makeham
curve pinned to ``q^g_54 = 0.00320``; *nsp_table.csv* is a separate parametric curve
pinned to ``NSP_55 = 0.42`` and ``NSP_100 = 1``; *np_guar_table.csv* holds
``1000 NSP_x / ae_{x:(100-x)}`` with the annuity taken on the mortality table's own
survivorship, which is what makes ``NP_g = 13.00``; and *cv_table.csv* is a monotone
shape solved through ``CV_9 = 95.00`` and ``CV_10 = 112.00`` to ``1000.00`` at attained
age 100. Reconciling the NSP curve with the mortality table needs a guarantee interest
rate that falls from 5.99% at age 45 to 0.02% at age 99, and inverting the curve for the
implied ``q`` at 4% gives a negative rate at every age up to 57 and a rate above 1 from
age 89 on.

The two *consequences* the pitfall names are nevertheless absent, and are asserted by
tests: ``NSP_100 = 1`` exactly, so ``pua_cv(T) == pua_face(T)``, and the schedule reaches
exactly face in the final policy year, so ``cv_pp(T) == sum_assured()``. Neither block
leaks at maturity. What is missing is the *means* — one basis — not the endpoints. Swap
in a licensed 2017 CSO / 4% set and all four files must be replaced together; the worked
example will then no longer reproduce, which is the honest price of the notes' own
arithmetic.

.. rubric:: Sign convention — two names, one stream

The whole-life notes print ``NetCF_t`` with **outgo positive**, which is the opposite of
the sign the other eleven reference models in ``products/`` carry. Rather than pick one
and lose the other, the model publishes both and names them apart:

``liability_cf(t)``
    The notes' ``NetCF_t``, verbatim: **outgo positive**. Premium and rider income enter
    with a minus sign; expenses, premium tax, claims, cash dividends and net loan
    advances enter with a plus. A positive ``liability_cf`` is money leaving the
    insurer. This is the number to compare against the notes.

``net_cf(t)``
    ``-liability_cf(t)``: **income positive**, the sign convention every model in
    ``products/`` carries, so that ``result_cf()["net_cf"]`` can be summed or compared
    across products. A positive ``net_cf`` is money arriving at the insurer.

Both are columns of ``result_cf()``. The pattern is ``SPIA_US_S`` and
``DIA_US_S``'s, which face the same clash. Nothing about the whole-life
notes' own convention is being denied — it is being kept under a name that does not
collide with the library-wide one, because a sign error in a 55-year liability
projection is invisible in a summary statistic.
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


def product():
    """The product code: WL_PAR, WL_FE_LEVEL or WL_FE_GRADED."""
    return model_point()["product"]


def is_par():
    """True for the participating design, which is the only one that pays dividends."""
    return product() == "WL_PAR"


def premium_period():
    """The premium period code: TO_100, PAY_10, PAY_20 or TO_65."""
    return model_point()["premium_period"]


def age_at_entry():
    """The issue age (ANB) of the selected model point."""
    return int(model_point()["issue_age"])


def sex():
    """The sex of the selected model point; rates are sex-distinct throughout."""
    return model_point()["sex"]


def risk_class():
    """The underwriting class of the selected model point (PREF_NT / STD_NT / TOB)."""
    return model_point()["risk_class"]


def sum_assured():
    """The base face amount F of the selected model point."""
    return float(model_point()["face_amount"])


def dividend_option():
    """The elected dividend option: PUA, CASH, ACCUM, REDUCE_PREM, or NONE for non-par."""
    return model_point()["dividend_option"]


def pols_if_init():
    """Initial number of policies in force, l at duration_inforce()."""
    return float(model_point()["pols_if_init"])


def duration_inforce():
    """t0: policy years already elapsed at the valuation date; 0 for new business."""
    return int(model_point()["duration_inforce"])


def puaf_inforce():
    """PUAF at t0: paid-up additions face already in force at the valuation date."""
    return float(model_point()["puaf_inforce"])


def loan_inforce():
    """L at t0: policy loan balance already outstanding at the valuation date."""
    return float(model_point()["loan_inforce"])


def loan_utilization():
    """Fraction of the guaranteed cash value held as a policy loan **[std]**.

    0 in the base run; the notes' variant is 0.20, maintained by borrowing and
    repaying at each anniversary.
    """
    return float(model_point()["loan_utilization"])


def term_blend_target():
    """TF: the term-blend rider's target face amount; 0 switches the rider off."""
    return float(model_point()["term_blend_target"])


def is_blended():
    """True when the term-blend rider is active on this model point **[std]**.

    The blend needs the dividend to pay the one-year-term cost, so it is modelled only
    under the PUA dividend option and only on the participating design.
    """
    return is_par() and dividend_option() == "PUA" and term_blend_target() > sum_assured()


def proj_len():
    """T = maturity_age - x: the last policy year, ending at attained age 100.

    The contract itself matures at 121, but the guaranteed cash value equals face at
    100 and the paid-up-additions cash value equals paid-up-additions face there, so
    from 100 the policy is economically an endowment at face. Truncating at 100 is a
    **[std]** simplification that moves the age 100-121 payments from death to
    maturity without changing their amount per survivor.
    """
    return maturity_age - age_at_entry()                             # noqa: F821


def proj_start():
    """The first projected policy year, t0 + 1.

    New business starts at 1; an in-force model point starts at the year following the
    durations it has already run.
    """
    return duration_inforce() + 1


def policy_term():
    """m: the premium-paying period in years, from the premium period code.

    This is *not* the coverage period, which is proj_len() in every variant.
    """
    p = premium_period()
    if p == "TO_100":
        return proj_len()
    elif p == "PAY_10":
        return 10
    elif p == "PAY_20":
        return 20
    elif p == "TO_65":
        return max(65 - age_at_entry(), 1)
    else:
        raise ValueError("invalid premium_period")


def age(t):
    """The attained age x + t - 1 entering policy year t.

    Mortality in year t is indexed here; paid-up additions bought at the end of the
    year are priced at age_anniv(t).
    """
    return age_at_entry() + t - 1


def age_anniv(t):
    """The attained age x + t at the anniversary that ends policy year t."""
    return age_at_entry() + t


def mec_flag():
    """True where the model point would need a Sect. 7702A test this model does not run.

    The notes are explicit that the reference model does not police Sect. 7702 or
    Sect. 7702A limits and should **flag** model points that would fail rather than
    silently projecting them **[std]**. Limited-pay designs sit near the 7-pay limit
    and paid-up-additions rider payments consume 7-pay room, so both raise the flag.
    """
    return premium_period() != "TO_100" or float(model_point()["pua_rider_premium"]) > 0.0


def premium_rate():
    """Final-expense annual premium per $1,000 of face, from *premium_rates.csv* [S7]."""
    key = (product(), sex(), risk_class(), age_at_entry())
    return float(data.premium_rates().loc[key, "rate_per_1000"])     # noqa: F821


def premium_pp(t):
    """G: the gross annual premium per policy payable at the start of policy year t.

    Level and guaranteed while premiums are payable, zero after policy_term(). The
    participating design takes G from the model point (**[std illustrative]** — carrier
    rate books are not public); the final-expense variant computes it from the sourced
    rate table as ``(F / 1000) * rate(x, sex, class) + 36`` [S7].
    """
    if t < 1 or t > policy_term():
        return 0.0
    elif is_par():
        return float(model_point()["annual_premium"])
    else:
        return sum_assured() / 1000.0 * premium_rate() + fe_policy_fee  # noqa: F821


def premium_net_pp(t):
    """G^net_t: the premium actually collected at the start of policy year t.

    Under REDUCE_PREM the prior anniversary's dividend offsets the premium,
    ``max(G - D_{t-1}, 0)``, and any excess buys paid-up additions through
    pua_face_offset(). The dynamic premium-offset overlay (**[std]**, off by default)
    applies a prem_offset_share fraction of the same offset once the dividend has grown
    to cover the premium.
    """
    g = premium_pp(t)
    if g == 0.0:
        return 0.0
    d = div_credited(t - 1)
    if dividend_option() == "REDUCE_PREM":
        return max(g - d, 0.0)
    elif prem_offset_on and d >= g:                                  # noqa: F821
        return g - prem_offset_share * min(d, g)                     # noqa: F821
    else:
        return g


def rider_premium_pp(t):
    """A_t: the paid-up-additions rider premium paid at the start of policy year t.

    Level while base premiums are payable **[std]**; the notes set it within limits
    fixed at issue and do not schedule it.
    """
    if not is_par() or t < proj_start() or t > policy_term():
        return 0.0
    return float(model_point()["pua_rider_premium"])


def prem_cum(t):
    """Cumulative gross premium paid per policy through the start of policy year t.

    Only the final-expense graded plan uses it, for the 110%-of-premiums-paid death
    benefit in policy years 1-2 [S6][S7].
    """
    if t < 1:
        return 0.0
    return prem_cum(t - 1) + premium_pp(t)


def cv_pp(t):
    """CV_t: the guaranteed cash value per policy at the anniversary ending year t.

    Read from *cv_table.csv* per $1,000 of face. The notes give the Standard
    Nonforfeiture Law adjusted-premium formula conceptually but prescribe a table input
    in practice, because contractual cash value tables are policy-form documents that
    are not public. The shipped schedule is **[std]**, calibrated to the worked
    example's CV_9 and CV_10 and reaching exactly face at attained age 100.

    It is **sex-distinct**, as the notes require of every rate in this product: the male
    pay-to-100 schedule carries the worked example's anchors, and the female schedule is
    that schedule's funding-progress shape ``f_t = CV^M_t / (F NSP^M_{x+t})`` applied to
    the female paid-up value ``F NSP^F_{x+t}`` **[std]**. The shape — how far along the
    way to paid-up status the schedule has come — is a design choice that does not
    depend on sex; the value it is progressing towards does, through NSP. See the
    guarantee-basis rubric in the Space docstring for what this construction is *not*.
    """
    if t < 1 or t > proj_len():
        return 0.0
    key = (premium_period(), sex(), age_at_entry(), t)
    return sum_assured() / 1000.0 * float(
        data.cv_table().loc[key, "cv_per_1000"])                     # noqa: F821


def net_amt_at_risk(t):
    """F - CV_t: the guarantee-basis net amount at risk carried by the mortality margin."""
    return sum_assured() - cv_pp(t)


def nsp(y):
    """NSP_y: net single premium per 1 of paid-up endowment-at-100 face at attained age y.

    The purchase basis for paid-up additions, unloaded, on the guarantee basis
    **[std]**. NSP_100 = 1 by construction, which is what makes the paid-up-additions
    cash value equal paid-up-additions face at maturity.

    The shipped curve is *not* the endowment-at-100 net single premium implied by
    *mort_table.csv* at 4%, and cannot be: see the guarantee-basis rubric in the Space
    docstring, which shows that the worked example's own anchors rule out any single
    mortality basis at 4%.
    """
    return float(data.nsp_table().loc[(sex(), y), "nsp"])            # noqa: F821


def np_guar():
    """NP_g: the nonforfeiture net level premium per policy, from *np_guar_table.csv*.

    The dividend's interest margin is credited on the guaranteed fund *including* the
    year's net premium, so this quantity sits inside div_int() **[std]**.

    The notes define it over the **endowment** period, ``NNLP = F NSP_x / ae_{x:(100-x)}``,
    and annotate the *other* nonforfeiture quantity — the adjusted premium P_adj — with
    "(m = premium period)", so the (100 - x) subscript is deliberate: NNLP does not vary
    with the premium period. The shipped table therefore carries one value per (sex,
    issue age), repeated across the premium periods; the premium_period key is kept so a
    carrier table that *does* vary by m can be dropped in without a formula change.
    """
    key = (premium_period(), sex(), age_at_entry())
    return sum_assured() / 1000.0 * float(
        data.np_guar_table().loc[key, "np_guar_per_1000"])           # noqa: F821


def mort_rate_guar_at(y):
    """q^g_y: the guaranteed mortality rate at attained age y, from *mort_table.csv*.

    The shipped table is **[std]** illustrative and is *not* the 2017 CSO the notes
    name; that table is licensed and cannot be shipped here.
    """
    return float(data.mort_table().loc[(sex(), y), "mort_rate"])     # noqa: F821


def mort_rate_guar(t):
    """q^g at the attained age entering policy year t."""
    return mort_rate_guar_at(age(t))


def mort_rate_scale(t):
    """q^sc: the dividend scale's experience mortality, ae_scale x q^g **[std]**."""
    return ae_scale * mort_rate_guar(t)                              # noqa: F821


def mort_rate(t):
    """q^e: the best-estimate mortality rate that decrements the block **[std]**.

    ``ae_best_est`` x q^g. The notes' sensitivity list flags this as a consistency
    trap: the same table drives claim outgo here and the dividend's mortality margin
    through mort_rate_scale(), with opposite signs.
    """
    return ae_best_est * mort_rate_guar(t)                           # noqa: F821


def dyn_lapse_factor(t):
    """The interest-sensitive lapse multiplier **[std]**, for scenario runs.

    ``min(1 + 2.0 * max(0, r_cmp - i_d - 0.01), 3.0)``, where r_cmp is the competitor
    or market rate in the scenario. Off unless dyn_lapse_on; the calibration is
    judgmental and the research base records no dynamic-lapse study for whole life.
    """
    return min(1.0 + 2.0 * max(0.0, competitor_rate - int_rate_div - 0.01), 3.0)  # noqa: F821


def lapse_rate(t):
    """w_t: the surrender rate applied to survivors at the end of policy year t **[std]**.

    Participating: 5.0% in year 1 grading linearly to 2.0% at year 10, level 2.0%
    thereafter. Final expense (simplified issue, so heavier): 12% year 1, 10% year 2,
    grading linearly to 6% by year 5 and level after. Zero in the final policy year —
    the notes' "0 within 1 year of maturity" — so that the survivors of year T mature
    rather than surrender.
    """
    if t >= proj_len():
        return 0.0
    elif is_par():
        w = 0.05 - 0.03 * (min(t, 10) - 1) / 9.0
    elif t == 1:
        w = 0.12
    elif t == 2:
        w = 0.10
    else:
        w = max(0.10 - (0.04 / 3.0) * (t - 2), 0.06)
    return w * dyn_lapse_factor(t) if dyn_lapse_on else w            # noqa: F821


def div_int(t):
    """D^int_t: the dividend's interest margin, with direct recognition **[std]**.

    ``(i_d - i_g)(CV_{t-1} + NP_g - L_{t-1}) + (i_L - i_g) L_{t-1}`` — the loaned
    portion is credited at the loan rate rather than the portfolio dividend rate. With
    the snapshot i_L = i_d = 6.00% the adjustment is zero, which is a coincidence of the
    snapshot and not a model property.
    """
    fund = cv_pp(t - 1) + np_guar()
    loan = loan_bal(t - 1)
    return ((int_rate_div - int_rate_guar) * (fund - loan)           # noqa: F821
            + (int_rate_loan - int_rate_guar) * loan)                # noqa: F821


def div_mort(t):
    """D^mort_t: the dividend's mortality margin, (q^g - q^sc)(F - CV_t) **[std]**."""
    return (mort_rate_guar(t) - mort_rate_scale(t)) * net_amt_at_risk(t)


def div_exp(t):
    """D^exp_t: the dividend's expense margin, a flat per-policy amount **[std]**."""
    return expense_margin                                            # noqa: F821


def div_base(t):
    """D_t: the base-block dividend credited at the anniversary ending year t.

    ``max(D^int + D^mort + D^exp, 0)``, rounded to div_round_digits. The floor is
    **[std]**: dividends are non-negative distributions of surplus, so adverse
    experience does not claw back. No dividend is credited before div_first_year, a
    real cross-carrier design split that the notes keep as a parameter, and none at all
    on the non-participating final-expense design.
    """
    if not is_par() or t < div_first_year or t < proj_start() or t > proj_len():  # noqa: F821
        return 0.0
    d = max(div_int(t) + div_mort(t) + div_exp(t), 0.0)
    return d if div_round_digits is None else round(d, div_round_digits)  # noqa: F821


def div_pua(t):
    """D^PUA_t: the dividend earned by the paid-up-additions block **[std]**.

    ``(i_d - i_g) PUACV_{t-1} + (q^g - q^sc)(PUAF_{t-1} - PUACV_{t-1})``. Paid-up
    additions are dividend-eligible, and the compounding this creates is the notes'
    first-ranked sensitivity. Switched **off** by ``pua_div_on`` in the shipped base run
    because the worked example's table omits it; see the Space docstring.
    """
    if (not pua_div_on or not is_par() or t < div_first_year         # noqa: F821
            or t < proj_start() or t > proj_len()):
        return 0.0
    return ((int_rate_div - int_rate_guar) * pua_cv(t - 1)           # noqa: F821
            + (mort_rate_guar(t) - mort_rate_scale(t))
            * (pua_face(t - 1) - pua_cv(t - 1)))


def div_credited(t):
    """D_t + D^PUA_t: the whole dividend credited to survivors at the end of year t."""
    if t < proj_start() or t > proj_len():
        return 0.0
    return div_base(t) + div_pua(t)


def oyt_face(t):
    """OYT_t: the one-year-term face the term-blend rider carries at the end of year t.

    ``max(TF - F - PUAF_{t-1}, 0)``, capped at what the dividend can fund **[std]**.
    Two readings had to be settled here, and both are standardizations:

    The notes write the gap as ``TF - F - PUAF_t``, which is circular — the term cost
    is deducted from the dividend that buys those very additions — so the model uses
    the prior anniversary's paid-up-additions face.

    The notes are also silent on what happens when the dividend cannot pay for the
    whole gap. Leaving the formula uncapped would report a term face the model never
    charges for and would inflate the death benefit, so the layer is capped at
    ``D_t (1 + i_g) / q^sc_{x+t}`` — as much term as the dividend actually buys.

    Whether the cap binds is a property of how the blend is funded, not of the design.
    On model point 8, where a $5,000 paid-up-additions rider premium funds the 2x
    target, it binds only in policy year 1 — where no dividend is payable at all under
    div_first_year = 2 — and the gap closes at year 8. On model point 14, the same 2x
    target with no rider premium, it binds in years 1-3 while the dividend is small and
    again in every year from 30 on as ``q^sc`` outruns it, and the block never crosses
    over. Crossover, after which the rider is pure paid-up additions, is where the gap
    itself reaches zero.
    """
    if not is_blended() or t < proj_start() or t > proj_len():
        return 0.0
    gap = max(term_blend_target() - sum_assured() - pua_face(t - 1), 0.0)
    q = ae_scale * mort_rate_guar_at(age_anniv(t))                   # noqa: F821
    if gap == 0.0 or q <= 0.0:
        return gap
    return min(gap, div_credited(t) * (1.0 + int_rate_guar) / q)     # noqa: F821


def oyt_cost(t):
    """The dividend absorbed by the one-year-term layer, q^sc_{x+t} x OYT_t x v_g **[std]**."""
    if oyt_face(t) == 0.0:
        return 0.0
    return (ae_scale * mort_rate_guar_at(age_anniv(t))               # noqa: F821
            * oyt_face(t) / (1.0 + int_rate_guar))                   # noqa: F821


def div_to_pua(t):
    """The part of the credited dividend that buys paid-up additions at the end of year t.

    Under the PUA option, everything left after the term-blend cost. Under CASH it is
    paid out, under ACCUM it goes to div_accum(), and under REDUCE_PREM it offsets the
    next premium with the excess handled at the start of the following year by
    pua_face_offset() — except in the final policy year, where there is no year T + 1
    to offset. The notes are silent on that last dividend; routing it anywhere else
    would drop it, so the whole of D_T is treated as REDUCE_PREM excess and buys
    paid-up additions at NSP_100 = 1 **[std]**, which is the same rule the option
    already applies in every year whose premium the dividend has outgrown.
    """
    if t < proj_start() or t > proj_len():
        return 0.0
    elif dividend_option() == "PUA":
        return max(div_credited(t) - oyt_cost(t), 0.0)
    elif dividend_option() == "REDUCE_PREM" and t == proj_len():
        return div_credited(t)
    else:
        return 0.0


def div_cash(t):
    """D^cash_t: the cash dividend paid per surviving policy at the end of year t."""
    return div_credited(t) if dividend_option() == "CASH" else 0.0


def div_accum(t):
    """DA_t: the dividend accumulation balance at the anniversary ending year t.

    ``DA_{t-1}(1 + i_d) + D_t`` under the ACCUM option, zero otherwise. The credit rate
    reuses the dividend interest rate **[std]**: carriers declare an accumulation rate
    annually with the scale but publish no separate figure. The balance adds to the
    death, surrender and maturity proceeds.
    """
    if t <= duration_inforce() or t > proj_len() or dividend_option() != "ACCUM":
        return 0.0
    return div_accum(t - 1) * (1 + int_rate_div) + div_credited(t)   # noqa: F821


def pua_face_purch(t):
    """dPUAF_t: paid-up-additions face bought by the dividend, div / NSP_{x+t}."""
    d = div_to_pua(t)
    return d / nsp(age_anniv(t)) if d else 0.0


def pua_face_rider(t):
    """dPUAF^rider_t: paid-up-additions face bought by the rider payment at the start of year t.

    ``A_t (1 - load) / NSP_{x+t-1}``, a 10% load **[std]** chosen from the observed
    7.5%-10% range on rider payments. Dividend purchases carry no load; only rider
    payments do.
    """
    a = rider_premium_pp(t)
    return a * (1 - pua_rider_load) / nsp(age(t)) if a else 0.0      # noqa: F821


def pua_face_offset(t):
    """Paid-up-additions face bought at the start of year t by the REDUCE_PREM excess.

    Once the prior dividend exceeds the premium it is offsetting, the excess buys
    paid-up additions **[std]** rather than being paid out. This carries D_{t-1}, so it
    can never carry D_T; that last dividend is routed through div_to_pua() instead —
    see its docstring.
    """
    if dividend_option() != "REDUCE_PREM" or t < proj_start() or t > proj_len():
        return 0.0
    excess = max(div_credited(t - 1) - premium_pp(t), 0.0)
    return excess / nsp(age(t)) if excess else 0.0


def pua_face(t):
    """PUAF_t: paid-up-additions face in force at the anniversary ending year t.

    ``PUAF_{t-1}`` plus the dividend, rider and premium-offset purchases of year t. The
    t0 branch carries the model point's puaf_inforce, which is what makes the worked
    example's stipulated prior balance of 4,100 an input rather than a projection.
    """
    if t <= duration_inforce():
        return puaf_inforce()
    elif t > proj_len():
        return 0.0
    return (pua_face(t - 1) + pua_face_purch(t)
            + pua_face_rider(t) + pua_face_offset(t))


def pua_cv(t):
    """PUACV_t: the cash value of the paid-up additions, PUAF_t x NSP_{x+t} **[std]**.

    Valuing the whole block at the attained-age net single premium is exact at the
    issue of each layer and again at age 100, and approximate in between.
    """
    if t < 1 or t > proj_len():
        return 0.0
    return pua_face(t) * nsp(age_anniv(t))


def loan_int(t):
    """Loan interest capitalized on the anniversary ending year t, L_{t-1} x i_L."""
    return loan_bal(t - 1) * int_rate_loan                           # noqa: F821


def loan_bal(t):
    """L_t: the policy loan balance at the anniversary ending year t **[std]**.

    The notes' variant holds the loan at ``loan_utilization x CV_t``, maintained by
    borrowing and repaying at each anniversary; the base run sets loan_utilization to
    zero. Loans reduce the death, surrender and maturity proceeds.
    """
    if t <= duration_inforce():
        return loan_inforce()
    elif t > proj_len():
        return 0.0
    return loan_utilization() * cv_pp(t)


def loan_draw(t):
    """Net new borrowing per policy at the anniversary ending year t; negative repays.

    The balance change net of the interest that capitalized into it, so the cash the
    insurer actually advances.
    """
    return loan_bal(t) - loan_bal(t - 1) - loan_int(t)


def claim_pp(t, kind):
    """The benefit amount per policy in policy year t, by kind.

    ``"DEATH"``     DB_t = F + PUAF_{t-1} + OYT_t + DA_{t-1} - L_{t-1}. Deaths fall at
                    the end of the year *before* the dividend is credited, so the
                    benefit carries the prior anniversary's paid-up additions
                    **[std]**. The one-year-term layer is zero unless the term-blend
                    rider is active, where ``F + PUAF + OYT`` is the notes' "target face
                    plus excess paid-up additions" written so that it still holds when
                    the dividend funds only part of the gap. On the final-expense
                    graded plan, natural-cause deaths in policy years 1-2 pay 110% of
                    cumulative premiums paid and accidental deaths pay the full face
                    from day one [S6][S7]; the two are blended by fe_accid_share
                    **[std]**, since the model carries one mortality decrement.
    ``"LAPSE"``     CSV_t = CV_t + PUACV_t + DA_t - L_t, the surrender value at the end
                    of year t, including the dividend just credited.
    ``"MATURITY"``  MAT = F + PUAF_T + DA_T - L_T, paid at T and zero in every other
                    year. On the non-participating design this is F - L_T.
    """
    if kind == "DEATH":
        if product() == "WL_FE_GRADED" and t <= fe_graded_years:     # noqa: F821
            return ((1 - fe_accid_share) * fe_graded_factor * prem_cum(t)  # noqa: F821
                    + fe_accid_share * sum_assured())                # noqa: F821
        face = sum_assured() + pua_face(t - 1) + oyt_face(t)
        return face + div_accum(t - 1) - loan_bal(t - 1)
    elif kind == "LAPSE":
        return cv_pp(t) + pua_cv(t) + div_accum(t) - loan_bal(t)
    elif kind == "MATURITY":
        if t != proj_len():
            return 0.0
        return sum_assured() + pua_face(t) + div_accum(t) - loan_bal(t)
    else:
        raise ValueError("invalid kind")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        l_{t-1}, the start of year t, before any decrement; the same number
        as pols_if(t), and the weight on that year's cash flows.
    ``"BEF_SURR"``
        after deaths, before surrenders — the population the dividend is
        credited to and the one surrenders are taken from.
    ``"BEF_MAT"``
        after surrenders, before maturity; the survivors of the year.
    ``"AFT_DECR"``
        l_t, the notes' end-of-year state variable: what is left once the
        year's deaths, surrenders and — in the final policy year — the
        maturities have all been taken, so it is zero from T on. Equals
        pols_if(t + 1). The string is added to CashValue_SE's set because
        that model has no name for the point past the last decrement, which
        is where these notes keep their in-force probability.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    elif timing == "BEF_SURR":
        return pols_if_at(t, "BEF_DECR") * (1 - mort_rate(t))
    elif timing == "BEF_MAT":
        return pols_if_at(t, "BEF_SURR") * (1 - lapse_rate(t))
    elif timing == "AFT_DECR":
        if t <= duration_inforce():
            return pols_if_init()
        elif t >= proj_len():
            return 0.0
        return pols_if_at(t, "BEF_MAT")
    else:
        raise ValueError("invalid timing")


def pols_if(t):
    """The number of policies in force at the **start** of policy year t.

    The notes' l_{t-1}: the population that pays the year's premium, carries its
    expenses and is exposed to its decrements, so it is the weight on every cash flow
    of the same result_cf() row. Equal to pols_if_init() up to and including t0, and
    zero from T + 1 on, because everything still in force at T matures there and the
    contract terminates.

    The notes' end-of-year l_t is pols_if_at(t, "AFT_DECR"), which is this cells one
    year on.
    """
    if t <= duration_inforce():
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_death(t):
    """Deaths in policy year t, q^e applied to the policies in force at its start."""
    return pols_if_at(t, "BEF_DECR") * mort_rate(t)


def pols_lapse(t):
    """Surrenders at the end of policy year t, w_t applied to survivors of the year."""
    return pols_if_at(t, "BEF_SURR") * lapse_rate(t)


def pols_maturity(t):
    """Policies maturing at attained age 100; non-zero only in the final policy year.

    Not a decrement — the modelled contract simply ends — but the in-force
    roll-forward does not close without it.
    """
    return pols_if_at(t, "BEF_MAT") if t == proj_len() else 0.0


def inflation_factor(t):
    """The expense inflation factor in policy year t."""
    return (1 + inflation_rate) ** (t - 1)                           # noqa: F821


def premiums(t):
    """Premium income at the start of policy year t (an inflow)."""
    return premium_net_pp(t) * pols_if_at(t, "BEF_DECR")


def rider_premiums(t):
    """Paid-up-additions rider premium income at the start of policy year t (an inflow)."""
    return rider_premium_pp(t) * pols_if_at(t, "BEF_DECR")


def premium_taxes(t):
    """Premium tax at the start of policy year t **[std]**, on premium and rider income.

    The notes' processing order collects it at the beginning of the year alongside the
    expenses; their one-line NetCF formula omits it. The model follows the processing
    order and keeps it as its own line.
    """
    return premium_tax_rate * (premiums(t) + rider_premiums(t))      # noqa: F821


def expenses(t):
    """E_t: acquisition and inflating maintenance expense in policy year t **[std]**.

    90% of the first year's premium plus $250 per policy at issue, then $60 per policy
    per year inflating at 2%. An in-force model point never sees the acquisition
    charge, because its projection starts after policy year 1.
    """
    acq = expense_acq_prem_rate * premium_pp(t) + expense_acq if t == 1 else 0.0  # noqa: F821
    return ((acq + expense_maint * inflation_factor(t))              # noqa: F821
            * pols_if_at(t, "BEF_DECR"))


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted."""
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "MATURITY"))
    elif kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    elif kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    elif kind == "MATURITY":
        return claim_pp(t, "MATURITY") * pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def div_cash_paid(t):
    """Cash dividends paid out at the end of policy year t, to survivors of the year."""
    return div_cash(t) * pols_if_at(t, "BEF_SURR")


def loan_draws(t):
    """Net policy loans advanced at the end of policy year t **[std]**, an outflow.

    The notes report gross liability flows plus a separate loan account rather than
    netting the loan into a net-amount-at-risk presentation. Advances go to the
    policies still in force; the balance is recovered through the death, surrender and
    maturity benefits, which are all net of the loan.
    """
    return loan_draw(t) * pols_if_at(t, "BEF_MAT")


def liability_cf(t):
    """NetCF_t: the net liability cash flow in policy year t, **outgo positive**.

    The technical notes' formula verbatim, and the one to compare against them: premium
    and rider income enter with a minus sign; expenses, premium tax, death, surrender
    and maturity benefits, cash dividends and net loan advances enter with a plus, so a
    positive value is money leaving the insurer. Internal dividend applications —
    paid-up additions, accumulation, premium reduction — are not cash flows when
    credited: they emerge later through the death benefit, the surrender value and the
    maturity benefit.

    These notes are the only ones in the library that print the outgo-positive sign, so
    the stream is published twice: here under the notes' sign, and negated as net_cf(t)
    under the library's. See the sign-convention rubric in the Space docstring.
    """
    return (-premiums(t) - rider_premiums(t)
            + expenses(t) + premium_taxes(t)
            + claims(t) + div_cash_paid(t) + loan_draws(t))


def net_cf(t):
    """The net cash flow in policy year t, **income positive**: -liability_cf(t).

    Income less outgo, the sign every model in ``products/`` carries, so that a
    ``result_cf()["net_cf"]`` column can be summed or compared across products. A
    positive value is money arriving at the insurer. liability_cf(t) is the same stream
    under the technical notes' own outgo-positive sign; both are result_cf() columns
    because neither reading may be lost.
    """
    return -liability_cf(t)


def result_cf():
    """Result table of cashflows, indexed by policy year.

    ``pols_if`` is the start-of-year count, which is the weight applied to every cash
    flow on the same row. Both signs of the net flow are published: ``net_cf`` is
    income-positive, the library-wide convention, and ``liability_cf`` is the technical
    notes' outgo-positive ``NetCF_t``; the two are negatives of each other.
    """
    ts = list(range(proj_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "rider_premiums": [rider_premiums(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "div_cash_paid": [div_cash_paid(t) for t in ts],
            "loan_draws": [loan_draws(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy year."""
    ts = list(range(proj_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cv():
    """Result table of the guaranteed and non-guaranteed values, indexed by policy year.

    The account-value analogue for this product: the guaranteed cash value, the
    paid-up-additions block, the accumulation balance and the loan, plus the dividend
    that drives them and the two benefit amounts they feed.
    """
    ts = list(range(proj_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "cv_pp": [cv_pp(t) for t in ts],
            "div_base": [div_base(t) for t in ts],
            "div_pua": [div_pua(t) for t in ts],
            "pua_face": [pua_face(t) for t in ts],
            "pua_cv": [pua_cv(t) for t in ts],
            "div_accum": [div_accum(t) for t in ts],
            "loan_bal": [loan_bal(t) for t in ts],
            "db_pp": [claim_pp(t, "DEATH") for t in ts],
            "surr_value_pp": [claim_pp(t, "LAPSE") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``pols_if(t) - pols_if(t + 1) - deaths - surrenders - maturities``, the notes'
    ``l_{t-1} - l_t - ...``. Maturities are non-zero only in the final policy year,
    where the survivors neither die nor surrender: their contract ends. Without that
    term the last year appears to lose lives with no cause.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy year.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model. check_pols_roll_fwd_resid(t) gives the
    signed residual of the year that failed. The tolerance scales with pols_if_init(),
    since the residual is an accumulation of rounding on that many policies.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(proj_start(), proj_len() + 1))


def check_pua_roll_fwd_resid(t):
    """The paid-up-additions roll-forward residual in policy year t; zero everywhere.

    ``PUAF_t - PUAF_{t-1} - dividend purchases - rider purchases - offset purchases``.
    The analogue of ``CashValue_SE.check_av_roll_fwd`` for a product whose accumulating
    state is a face amount rather than an account value.
    """
    return (pua_face(t) - pua_face(t - 1) - pua_face_purch(t)
            - pua_face_rider(t) - pua_face_offset(t))


def check_pua_roll_fwd():
    """True when the paid-up-additions roll-forward closes in every projected year.

    No argument, one bool over all t, matching check_pols_roll_fwd();
    check_pua_roll_fwd_resid(t) gives the signed residual. The tolerance is relative to
    the block itself, which reaches six figures of face on a compounding projection.
    """
    return all(abs(check_pua_roll_fwd_resid(t)) <= 1e-9 * max(pua_face(t), 1.0)
               for t in range(proj_start(), proj_len() + 1))


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

maturity_age = 100

int_rate_guar = 0.04

int_rate_div = 0.06

int_rate_loan = 0.06

ae_scale = 0.7

ae_best_est = 0.7

expense_margin = 25.0

div_first_year = 2

div_round_digits = 2

pua_div_on = False

pua_rider_load = 0.1

expense_acq_prem_rate = 0.9

expense_acq = 250.0

expense_maint = 60.0

inflation_rate = 0.02

premium_tax_rate = 0.02

fe_policy_fee = 36.0

fe_graded_years = 2

fe_graded_factor = 1.1

fe_accid_share = 0.03

dyn_lapse_on = False

competitor_rate = 0.06

prem_offset_on = False

prem_offset_share = 0.5

pd = ("Module", "pandas")
