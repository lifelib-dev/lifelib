"""Golden and structural tests for Dep_FR_S.

The golden values are the worked example in
products/dependance/technical-notes.md ("Worked example"): a female entry age 70 on the
*formule* Dépendance Totale et Partielle, *rente totale* 1,000 EUR a month, *rente
partielle* 500, *capital d'équipement* 3,500, premium 75 EUR a month, *carence*
0 / 12 / 36 months by cause, *franchise* three months, *mise en réduction* from eight
years.  Model point 1 is that cell.  The notes give sixteen monthly rows, the policy-year
1 aggregates, the lifetime totals and three month-by-month derivations, and all four are
asserted here.

They are hard-coded rather than pickled so that a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to four decimals,
state probabilities to six, derived monthly rates to ten.

Beyond the worked example this module asserts the product facts the notes list as
modelling pitfalls, because each is a way an implementation can look right and be wrong:
flat mortality across states, dropping the *mise en réduction*, confusing the *carence*
with the *franchise*, treating the *franchise* as a premium holiday, bolting an
aggravation rate onto an identity derived without one, charging premium to the whole
in-force block, paying the *capital* twice, collapsing the two indexations, and
restarting the duration clock.

Several of those are asserted by **replacing a formula** on a freshly read copy of the
model, which is the only faithful way to express a mis-implementation: setting a
Reference would move the incidence identity as well, and the whole point of these tests
is that the two must move together or not at all.
"""
import csv
import math

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from fr_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.00005        # money displayed to 4 d.p.
STATE = 5e-7          # state probabilities to 6 d.p.
RATE = 5e-10          # derived monthly rates to 10 d.p.

MODEL_DIR = LIB / MODELS["Dep_FR_S"][0]

# t: (pols_auto, pols_part, pols_tot, premiums, claims_rente, claims_capital,
#     refunds_carence, expenses + claim_expenses, net_cf)
WORKED_EXAMPLE = {
    0: (1.000000, 0.000000, 0.000000, 75.0000, 0.0000, 0.0433, 0.0084, 154.2031, -79.2548),
    1: (0.991949, 0.000007, 0.000005, 74.3962, 0.0000, 0.0430, 0.0166, 4.1693, 70.1673),
    2: (0.983963, 0.000015, 0.000010, 73.7972, 0.0000, 0.0426, 0.0247, 4.1358, 69.5942),
    3: (0.976041, 0.000022, 0.000015, 73.2031, 0.0000, 0.0423, 0.0326, 4.1025, 69.0257),
    4: (0.968183, 0.000029, 0.000020, 72.6137, 0.0087, 0.0419, 0.0404, 4.0697, 68.4530),
    5: (0.960388, 0.000035, 0.000025, 72.0291, 0.0174, 0.0416, 0.0481, 4.0371, 67.8849),
    6: (0.952656, 0.000042, 0.000030, 71.4492, 0.0260, 0.0413, 0.0557, 4.0048, 67.3215),
    7: (0.944987, 0.000048, 0.000035, 70.8740, 0.0346, 0.0409, 0.0631, 3.9727, 66.7627),
    8: (0.937379, 0.000055, 0.000041, 70.3034, 0.0431, 0.0406, 0.0705, 3.9409, 66.2083),
    9: (0.929832, 0.000061, 0.000046, 69.7374, 0.0516, 0.0403, 0.0777, 3.9093, 65.6585),
    10: (0.922346, 0.000066, 0.000051, 69.1759, 0.0600, 0.0399, 0.0847, 3.8780, 65.1132),
    11: (0.914920, 0.000072, 0.000057, 68.6190, 0.0684, 0.0396, 0.0917, 3.8470, 64.5723),
    12: (0.907554, 0.000078, 0.000062, 68.7472, 0.0779, 0.3173, 0.0472, 3.8930, 64.4119),
    13: (0.901730, 0.000130, 0.000099, 68.3060, 0.0863, 0.3152, 0.0505, 3.8685, 63.9855),
    14: (0.895943, 0.000181, 0.000137, 67.8677, 0.0947, 0.3132, 0.0538, 3.8442, 63.5619),
    15: (0.890194, 0.000230, 0.000175, 67.4322, 0.1029, 0.3112, 0.0570, 3.8200, 63.1410),
}

# The notes' policy-year-1 aggregates.  These are sums of unrounded monthly values, so
# the twelve displayed rows above do not re-add to them.
YEAR_1 = {"premiums": 861.1983, "claims_rente": 0.3098, "claims_capital": 0.4973,
          "refunds_carence": 0.6141, "expenses": 198.2304, "claim_expenses": 0.0398,
          "net_cf": 661.5068}

# The notes' lifetime totals, undiscounted, per policy issued, over all 480 months.
LIFETIME = {"premiums": 10867.00, "claims_rente": 5885.08, "claims_capital": 632.92,
            "refunds_carence": 2.86, "expenses": 828.71, "claim_expenses": 113.18,
            "net_cf": 3404.24}

# The notes' derived monthly rates at attained ages 70 and 71.
MONTHLY_RATES = {
    70: {"q_h": 0.0010098056, "q_p": 0.0017664906, "q_t": 0.0043047564,
         "i_pm": 0.0000753503, "i_tm": 0.0000493741, "w": 0.0069243826},
    71: {"q_h": 0.0011279321, "q_p": 0.0019730461, "q_t": 0.0048073955,
         "i_pm": 0.0000914562, "i_tm": 0.0000616541, "w": 0.0051430128},
}

# The notes' annual entry forces by attained age.
INCIDENCE = {70: (0.000904, 0.000593), 75: (0.002365, 0.001823),
             80: (0.005961, 0.005704), 85: (0.013650, 0.017325),
             90: (0.025599, 0.048116), 95: (0.035422, 0.118892),
             100: (0.034902, 0.262330)}

# Replacement formulas that express a mis-implementation, used by the pitfall tests.
FLAT_STATE_MORTALITY = "lambda t: mort_rate_mth(t)"

NO_AGGRAVATION_IN_IDENTITY_P = '''
def inc_rate_partial(t):
    pi_p, pi_t = prev_partial(t), prev_total(t)
    pi_h = 1.0 - pi_p - pi_t
    num = (severity_share("partial") * prev_slope(t)
           + mort_partial_mult * mort_force(t) * pi_p - pi_p * mort_force_avg(t))
    return max(0.0, num / pi_h)
'''

NO_AGGRAVATION_IN_IDENTITY_T = '''
def inc_rate_total(t):
    pi_p, pi_t = prev_partial(t), prev_total(t)
    pi_h = 1.0 - pi_p - pi_t
    num = (severity_share("total") * prev_slope(t)
           + mort_total_mult * mort_force(t) * pi_t - pi_t * mort_force_avg(t))
    return max(0.0, num / pi_h)
'''


def lifetime_claims(proj):
    """Undiscounted lifetime *rente* plus *capital* outgo, the notes' comparator."""
    df = proj.result_cf()
    return df["claims_rente"].sum() + df["claims_capital"].sum()


def read_variant(name):
    """A fresh copy of the model, for a test that edits formulas or References."""
    return mx.read_model(MODEL_DIR, name="Dep_FR_S_" + name)


def write_csv(path, header, rows):
    """Write a throwaway input file for an input-swap test."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_dep_anchor, t):
    """Every cell of the notes' sixteen-month table, to the displayed precision."""
    auto, part, tot, prem, rente, cap, refund, exp, net = WORKED_EXAMPLE[t]
    p = fr_dep_anchor
    assert p.pols_auto(t) == pytest.approx(auto, abs=STATE)
    assert p.pols_part(t) == pytest.approx(part, abs=STATE)
    assert p.pols_tot(t) == pytest.approx(tot, abs=STATE)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "RENTE") == pytest.approx(rente, abs=CENT)
    assert p.claims(t, "CAPITAL") == pytest.approx(cap, abs=CENT)
    assert p.refunds_carence(t) == pytest.approx(refund, abs=CENT)
    # The notes' `expenses` column is the combined expense of the month; the model
    # publishes the per-policy and the per-event halves as two columns.
    assert p.expenses(t) + p.claim_expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_worked_example_year_one_and_the_first_anniversary(fr_dep_anchor):
    """The notes' policy-year-1 aggregates and the state at t = 12."""
    p = fr_dep_anchor
    df = p.result_cf().loc[0:11]
    for column, total in YEAR_1.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    # The notes' own remark: the year-1 net_cf differs by EUR 0.0001 from the difference
    # of the six rounded lines, because the totals are sums of unrounded values.
    rounded = (YEAR_1["premiums"] - YEAR_1["claims_rente"] - YEAR_1["claims_capital"]
               - YEAR_1["refunds_carence"] - YEAR_1["expenses"]
               - YEAR_1["claim_expenses"])
    assert abs(rounded - YEAR_1["net_cf"]) == pytest.approx(0.0001, abs=1e-9)
    assert p.pols_auto(12) == pytest.approx(0.907554, abs=STATE)
    assert p.pols_part(12) == pytest.approx(0.000078, abs=STATE)
    assert p.pols_tot(12) == pytest.approx(0.000062, abs=STATE)
    assert p.pols_if(12) == pytest.approx(0.907694, abs=STATE)
    assert p.pols_red(12) == 0.0                       # the first reduction is at t = 95


def test_worked_example_lifetime_totals_and_counts(fr_dep_anchor):
    """The notes' lifetime table: claims are 60.0% of premiums, 65.0% of them past 85."""
    p = fr_dep_anchor
    df = p.result_cf()
    assert len(df) == p.proj_len() == 480 and df.index[-1] == 479
    for column, total in LIFETIME.items():
        assert df[column].sum() == pytest.approx(total, abs=0.005), column
    claims = lifetime_claims(p)
    assert claims / df["premiums"].sum() == pytest.approx(0.600, abs=0.0005)
    late = sum(df.loc[t, "claims_rente"] + df.loc[t, "claims_capital"]
               for t in range(480) if p.age(t) >= 85)
    assert late / claims == pytest.approx(0.650, abs=0.0005)
    assert sum(p.pols_recognition(t) for t in range(480)) == pytest.approx(
        0.198, abs=0.0005)
    assert sum(p.instalments(t) for t in range(480)) == pytest.approx(6.368, abs=0.0005)
    assert df["pols_red"].max() == pytest.approx(0.082685, abs=STATE)
    assert int(df["pols_red"].idxmax()) == 194 and p.age(194) == 86


@pytest.mark.parametrize("x", sorted(MONTHLY_RATES))
def test_worked_example_monthly_rates(fr_dep_anchor, x):
    """The notes' derived monthly factors at attained ages 70 and 71."""
    p = fr_dep_anchor
    t, r = 12 * (x - 70), MONTHLY_RATES[x]
    assert p.age(t) == x
    assert p.mort_rate_mth(t) == pytest.approx(r["q_h"], abs=RATE)
    assert p.mort_rate_partial_mth(t) == pytest.approx(r["q_p"], abs=RATE)
    assert p.mort_rate_total_mth(t) == pytest.approx(r["q_t"], abs=RATE)
    assert p.inc_rate_partial_mth(t) == pytest.approx(r["i_pm"], abs=RATE)
    assert p.inc_rate_total_mth(t) == pytest.approx(r["i_tm"], abs=RATE)
    assert p.lapse_rate_mth(t) == pytest.approx(r["w"], abs=RATE)


def test_worked_example_assumption_values(fr_dep_anchor):
    """The prevalence, severity shares, identity terms and revalorisation at age 70."""
    p = fr_dep_anchor
    assert p.mort_rate(0) == pytest.approx(0.0120506, abs=5e-8)
    assert p.mort_rate(12) == pytest.approx(0.0134515, abs=5e-8)
    assert p.prev_rate(0) == pytest.approx(0.01494159, abs=5e-9)
    assert p.prev_rate(12) == pytest.approx(0.01809552, abs=5e-9)
    assert (p.severity_share("partial"), p.severity_share("total")) == (0.15, 0.30)
    assert p.prev_partial(0) == pytest.approx(0.002241239, abs=5e-10)
    assert p.prev_total(0) == pytest.approx(0.004482477, abs=5e-10)
    assert p.mort_force(0) == pytest.approx(0.012123789, abs=5e-10)
    assert p.mort_force_avg(0) == pytest.approx(0.012321875, abs=5e-10)
    assert p.inc_rate_partial(0) == pytest.approx(0.000904237, abs=5e-10)
    assert p.inc_rate_total(0) == pytest.approx(0.000592504, abs=5e-10)
    assert p.aggravation_rate_mth() == pytest.approx(0.0165285462, abs=RATE)
    assert p.rente_total_pp(12) == pytest.approx(1010.00, abs=CENT)
    assert p.capital_pp(12) == pytest.approx(3535.00, abs=CENT)
    assert p.premium_mth_pp(12) == pytest.approx(75.75, abs=CENT)
    assert p.premium_pp(12) == pytest.approx(12 * 75.75, abs=CENT)
    assert p.rente_pay_pp(12, 12) == pytest.approx(1015.00, abs=CENT)
    assert p.rente_pay_partial_pp(12, 12) == pytest.approx(507.50, abs=CENT)


def test_worked_example_month_zero_end_to_end(fr_dep_anchor):
    """The notes' month-0 derivation, term by term."""
    p = fr_dep_anchor
    assert p.pols_auto(0) == 1.0
    assert p.premiums(0) == pytest.approx(75.0, abs=CENT)
    assert p.pols_surv(0) == pytest.approx(0.9989901944, abs=5e-10)
    assert p.pols_lapse(0) == pytest.approx(0.0069173903, abs=5e-10)
    assert p.pols_base(0) == pytest.approx(0.9920728040, abs=5e-10)
    assert p.pols_entry_partial(0) == pytest.approx(0.0000074753, abs=5e-11)
    assert p.pols_entry_total(0) == pytest.approx(0.0000048983, abs=5e-11)
    assert p.pols_carence_exit(0) == pytest.approx(0.0001113621, abs=5e-11)
    assert p.claims(0, "CAPITAL") == pytest.approx(0.0433, abs=CENT)
    assert p.refunds_carence(0) == pytest.approx(0.0084, abs=CENT)
    assert p.claim_expenses(0) == pytest.approx(0.0031, abs=CENT)
    assert p.expenses(0) == pytest.approx(150.0 + 3.0 + 1.2, abs=CENT)
    assert p.pols_auto(1) == pytest.approx(0.9919490683, abs=5e-10)


def test_worked_example_month_four_is_the_first_instalment(fr_dep_anchor):
    """The franchise is exactly three dropped instalments; the model pays the fourth.

    The cohort recognised at the end of month 0 reaches ``z = 4`` at the start of month 4
    and is paid at its end.  The notes give the two surviving cohort values behind the
    0.0087 EUR.
    """
    p = fr_dep_anchor
    assert p.franchise_months() == 3
    assert all(p.claims(t, "RENTE") == 0.0 for t in (0, 1, 2, 3))
    part_s = p.pols_part_dur(4, 4) * (1 - p.mort_rate_partial_mth(4))
    tot_s = p.pols_tot_dur(4, 4) * (1 - p.mort_rate_total_mth(4))
    assert part_s == pytest.approx(0.000007060611, abs=5e-13)
    assert tot_s == pytest.approx(0.000005174632, abs=5e-13)
    assert p.claims(4, "RENTE") == pytest.approx(500 * part_s + 1000 * tot_s, rel=1e-12)
    assert p.claims(4, "RENTE") == pytest.approx(0.0087, abs=CENT)
    assert p.instalments(4) == pytest.approx(0.000012235, abs=5e-10)
    # Nothing else in the month moves: the handling expense adds 0.0001.
    assert p.claim_expenses(4) - 250.0 * p.pols_recognition(4) == pytest.approx(
        0.0001, abs=CENT)


def test_worked_example_month_twelve_carence_step(fr_dep_anchor):
    """The notes decompose the 8.0076x jump in claims_capital into exactly four factors.

    The *carence* widening, the age step in the incidence identity, the *revalorisation*
    of the *capital*, and the in-force run-off - and every one of them is a cells here.
    """
    p = fr_dep_anchor
    assert p.pols_base(12) == pytest.approx(0.90186807, abs=5e-9)
    entrants = p.pols_entry_partial(12) + p.pols_entry_total(12)
    assert entrants == pytest.approx(0.000089755, abs=5e-10)
    assert p.cum_prem_pp(12) == pytest.approx(975.75, abs=CENT)
    assert p.cum_prem_pp(11) == pytest.approx(900.00, abs=CENT)
    assert p.claims(12, "CAPITAL") == pytest.approx(3535.00 * entrants, rel=1e-12)
    ratio = p.claims(12, "CAPITAL") / p.claims(11, "CAPITAL")
    assert ratio == pytest.approx(8.0076, abs=0.00005)
    carence = p.carence_factor(12) / p.carence_factor(11)
    incidence = ((p.inc_rate_partial_mth(12) + p.inc_rate_total_mth(12))
                 / (p.inc_rate_partial_mth(0) + p.inc_rate_total_mth(0)))
    reval = p.capital_pp(12) / p.capital_pp(11)
    runoff = p.pols_base(12) / p.pols_base(11)
    assert carence == pytest.approx(6.5, rel=1e-12)
    assert incidence == pytest.approx(1.227589, abs=5e-7)
    assert reval == pytest.approx(1.01, rel=1e-12)
    assert runoff == pytest.approx(0.993611, abs=5e-7)
    assert carence * incidence * reval * runoff == pytest.approx(ratio, rel=1e-9)


@pytest.mark.parametrize("x", sorted(INCIDENCE))
def test_the_incidence_identity_reproduces_the_notes_table(fr_dep_anchor, x):
    """The notes' annual entry forces from the prevalence-to-incidence identity."""
    p = fr_dep_anchor
    i_p, i_t = INCIDENCE[x]
    assert p.inc_rate_partial(12 * (x - 70)) == pytest.approx(i_p, abs=5e-7)
    assert p.inc_rate_total(12 * (x - 70)) == pytest.approx(i_t, abs=5e-7)


def test_the_severity_mix_worsens_with_age(fr_dep_anchor):
    """i_T overtakes i_P between attained ages 80 and 85.

    It arrives through the mortality terms of the identity, not through the severity
    shares, which are constant across age and cannot produce it.
    """
    p = fr_dep_anchor
    assert p.inc_rate_total(120) < p.inc_rate_partial(120)      # age 80
    assert p.inc_rate_total(180) > p.inc_rate_partial(180)      # age 85
    assert p.severity_share("total") / p.severity_share("partial") == 2.0
    # The notes' gradient from 70 to 90: a factor of 28 for i_P and 81 for i_T.
    assert p.inc_rate_partial(240) / p.inc_rate_partial(0) == pytest.approx(28, abs=1)
    assert p.inc_rate_total(240) / p.inc_rate_total(0) == pytest.approx(81, abs=1)


# ---------------------------------------------------------------------------
# Pitfall: flat mortality across states


def test_flat_state_mortality_would_raise_claims_by_160_percent(fr_dep_anchor):
    """The notes' first-listed pitfall, quantified: +159.7% of lifetime claims.

    Replacing the two monthly-rate formulas is the faithful expression of the mistake -
    healthy mortality applied to dependent lives **while the incidence basis is left
    unchanged**.  Setting the two multiples to 1 instead would also re-derive the
    identity, which is a different and much smaller error.  The state rates
    themselves are asserted below: 0.06179 healthy, 0.10562 and 0.23841 at age 85.
    """
    base = lifetime_claims(fr_dep_anchor)
    model = read_variant("flat")
    try:
        model.Projection.mort_rate_partial_mth.formula = FLAT_STATE_MORTALITY
        model.Projection.mort_rate_total_mth.formula = FLAT_STATE_MORTALITY
        model.Projection.clear_all()
        assert lifetime_claims(model.Projection[1]) / base - 1 == pytest.approx(
            1.597, abs=0.005)
    finally:
        model.close()
    # The notes' rates at 85: healthy 0.06179, partielle 0.10562, totale 0.23841.
    p, t = fr_dep_anchor, 180
    assert p.age(t) == 85
    assert p.mort_rate(t) == pytest.approx(0.06179, abs=5e-6)
    assert p.mort_rate_partial(t) == pytest.approx(0.10562, abs=5e-6)
    assert p.mort_rate_total(t) == pytest.approx(0.23841, abs=5e-6)
    assert p.mort_rate(t) < p.mort_rate_partial(t) < p.mort_rate_total(t)
    # A GIR 1-2 life at 84 dies at 0.216 a year against 0.055 for a healthy life.
    assert p.mort_rate_total(168) == pytest.approx(0.216, abs=0.0005)
    assert p.mort_rate(168) == pytest.approx(0.055, abs=0.0005)
    # The multiples are proportional hazards on the force, not on the probability.
    assert p.mort_rate_total(t) != pytest.approx(4.27 * p.mort_rate(t), rel=1e-3)


def test_the_totale_mortality_multiple_is_calibrated_not_picked(fr_dep_anchor):
    """sojourn_total(84) = 2.9989 years at k_T = 4.27, 4.19 at 2.75 and 3.50 at 3.50.

    The multiple is calibrated against the CCSF's mean duration of about three years
    for heavy dependents, and lightening it moves both sides of the account.
    """
    p = fr_dep_anchor
    assert p.mort_total_mult == 4.27
    assert p.sojourn_total(84) == pytest.approx(2.9989, abs=0.00005)
    assert p.sojourn_partial(82) == pytest.approx(3.14, abs=0.005)
    model = read_variant("kt")
    try:
        for k, expected in ((2.75, 4.19), (3.50, 3.50)):
            model.Projection.mort_total_mult = k
            model.Projection.clear_all()
            assert model.Projection[1].sojourn_total(84) == pytest.approx(
                expected, abs=0.005)
    finally:
        model.close()
    # And lightening it to 2.75 moves claims +9.05% and premiums +2.0%: the
    # identity lowers i_T when dependent lives live longer, so fewer autonomous
    # lives reach an exonerating state.
    base = lifetime_claims(fr_dep_anchor)
    base_prem = fr_dep_anchor.result_cf()["premiums"].sum()
    model = read_variant("kt275")
    try:
        model.Projection.mort_total_mult = 2.75
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert lifetime_claims(proj) / base - 1 == pytest.approx(0.0905, abs=0.0005)
        assert proj.result_cf()["premiums"].sum() / base_prem - 1 == pytest.approx(
            0.020, abs=0.0005)
    finally:
        model.close()
# ---------------------------------------------------------------------------
# Pitfall: ignoring the mise en reduction


def test_the_reduced_ledger_is_a_second_decrement_not_the_absence_of_one(
        fr_dep_anchor, dependance):
    """A lapse from year 8 converts the liability, it does not release it.

    And the guarantee it converts to is **frozen**: the reduced amount moves at neither
    of the two indexation rates.
    """
    p = fr_dep_anchor
    assert p.reduction_qualifying_years() == 8
    assert p.years_premiums_paid(94) == 7 and p.years_premiums_paid(95) == 8
    assert p.pols_reduction(94) == 0.0
    assert p.pols_reduction(95) == pytest.approx(p.pols_lapse(95), rel=1e-14)
    assert p.pols_lapse_exit(95) == pytest.approx(0.0, abs=1e-15)
    assert p.pols_lapse_exit(94) == pytest.approx(p.pols_lapse(94), rel=1e-14)
    assert p.pols_red(95) == 0.0 and p.pols_red(96) > 0.0
    # The coefficient at first qualification is the CNP bareme's 25%.
    assert p.reduction_coeff(7) == 0.0
    assert p.reduction_coeff(8) == 0.25
    assert p.reduction_coeff(10) == 0.30
    assert p.reduction_coeff(30) == 0.70 == p.reduction_coeff(60)
    # The first reduction cohort enters at G(y) x c(8) and is never revalued after.
    assert p.red_rente_pp(96) == pytest.approx(p.rente_total_pp(95) * 0.25, rel=1e-9)
    assert p.reval_guarantee == 0.010 and p.reval_rente == 0.015
    assert p.reval_guarantee != p.reval_rente       # so a test can tell them apart
    # Model point 11 is a paid-up membership with twelve years behind it.
    p = dependance.Projection[11]
    assert p.status() == "reduced" and p.years_paid() == 12
    assert p.pols_red(0) == 1.0 and p.pols_auto(0) == 0.0
    assert p.red_rente_pp(0) == pytest.approx(1000.0 * 0.34, rel=1e-12)
    df = p.result_cf()
    assert (df["premiums"] == 0.0).all()
    assert (df["claims_capital"] == 0.0).all()      # the option is lost on reduction
    assert df["claims_rente"].sum() > 0.0


# ---------------------------------------------------------------------------
# Pitfall: the carence and the franchise are different things


def test_dropping_the_reduced_ledger_understates_claims_by_four_and_a_half_percent():
    """Treating a qualifying lapse as an exit costs 4.57% of lifetime claims.

    The residual matters as much as the total: the dropped ledger peaks at 8.27% of the
    original policy, the largest state in the model after the autonomous one there.
    """
    base_model = read_variant("redbase")
    try:
        base = lifetime_claims(base_model.Projection[1])
    finally:
        base_model.close()
    model = read_variant("nored")
    try:
        model.Projection.pols_reduction.formula = "lambda t: 0.0"
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert lifetime_claims(proj) / base - 1 == pytest.approx(-0.0457, abs=0.0002)
        assert proj.result_cf()["pols_red"].max() == 0.0
    finally:
        model.close()


def test_the_carence_is_a_decrement_with_a_cash_flow(fr_dep_anchor):
    """A carence claim ends the membership and refunds every premium paid.

    Modelling it as a multiplier on incidence alone would leave the terminated
    membership in force and omit the refund - two errors running the same way.  In policy
    year 1 the refund is 0.6141 EUR against 0.8071 of rente and capital claims combined.
    """
    p = fr_dep_anchor
    assert (p.carence_accident_months(), p.carence_illness_months(),
            p.carence_neuro_months()) == (0, 12, 36)
    assert [p.carence_factor(t) for t in (0, 11, 12, 35, 36, 200)] == pytest.approx(
        [0.10, 0.10, 0.65, 0.65, 1.00, 1.00], abs=1e-12)
    for t in (0, 5, 11, 20):
        assert p.refunds_carence(t) == pytest.approx(
            p.pols_carence_exit(t) * p.cum_prem_pp(t), rel=1e-14)
        assert p.pols_carence_exit(t) > 0.0
    # pols_auto(t+1) does not depend on the carence factor at all.
    blocked = p.pols_base(0) * (p.inc_rate_partial_mth(0) + p.inc_rate_total_mth(0))
    assert p.pols_auto(1) == pytest.approx(p.pols_base(0) - blocked, rel=1e-14)
    assert p.pols_carence_exit(0) + p.pols_entry_partial(0) + p.pols_entry_total(
        0) == pytest.approx(blocked, rel=1e-12)
    assert p.pols_carence_exit(36) == 0.0
    df = p.result_cf().loc[0:11]
    refunds = df["refunds_carence"].sum()
    claims = df["claims_rente"].sum() + df["claims_capital"].sum()
    assert refunds == pytest.approx(0.6141, abs=CENT)
    assert claims == pytest.approx(0.8071, abs=CENT)
    assert refunds / claims == pytest.approx(0.76, abs=0.005)


def test_removing_the_carence_and_the_franchise_cost_different_amounts(dependance):
    """+3.99% for the carence and +7.09% for the franchise: different sizes.

    Model points 6 and 7 are model point 1 with one of the two switched off, so the two
    are separable rather than confounded.
    """
    base = lifetime_claims(dependance.Projection[1])
    no_carence, no_franchise = dependance.Projection[6], dependance.Projection[7]
    assert no_carence.carence_illness_months() == 0
    assert no_carence.carence_neuro_months() == 0
    assert no_carence.franchise_months() == 3
    assert no_franchise.franchise_months() == 0
    assert no_franchise.carence_neuro_months() == 36
    assert lifetime_claims(no_carence) / base - 1 == pytest.approx(0.0399, abs=0.0002)
    assert lifetime_claims(no_franchise) / base - 1 == pytest.approx(0.0709, abs=0.0002)
    # Removing the carence also removes the refund, which is the other half of it.
    assert (no_carence.result_cf()["refunds_carence"] == 0.0).all()
    assert no_franchise.result_cf()["refunds_carence"].sum() > 0.0
    # Without a franchise the first cohort is paid in the month after recognition.
    assert no_franchise.claims(1, "RENTE") > 0.0
    assert dependance.Projection[1].claims(1, "RENTE") == 0.0


def test_the_franchise_is_not_a_premium_holiday(fr_dep_anchor):
    """Exoneration runs from recognition, so the franchise is neither paid nor paying."""
    p = fr_dep_anchor
    for t in (1, 2, 3):
        assert p.claims(t, "RENTE") == 0.0
        assert p.premiums(t) == pytest.approx(p.premium_mth_pp(t) * p.pols_auto(t),
                                              rel=1e-14)
    # The population inside the franchise is in a dependent ledger, so it is outside
    # pols_prem entirely: no band is both premium-paying and benefit-free.
    assert p.pols_part(2) > 0.0
    assert p.pols_prem(2) == p.pols_auto(2) < p.pols_if(2)


# ---------------------------------------------------------------------------
# Pitfall: aggravation and incidence are not independent


def test_varying_the_aggravation_rate_consistently_barely_moves_claims(fr_dep_anchor):
    """0 / 0.20 / 0.40 moves lifetime claims +0.54% / 0 / -0.52%.

    The stock of *totale* lives is pinned by the assumed prevalence, so aggravations
    arriving from *partielle* displace direct entries one for one.
    """
    base = lifetime_claims(fr_dep_anchor)
    model = read_variant("ia")
    try:
        for rate, expected in ((0.0, 0.0054), (0.20, 0.0), (0.40, -0.0052)):
            model.Projection.aggravation_rate = rate
            model.Projection.clear_all()
            assert lifetime_claims(model.Projection[1]) / base - 1 == pytest.approx(
                expected, abs=0.0002), rate
    finally:
        model.close()


def test_bolting_on_aggravation_without_re_deriving_incidence(fr_dep_anchor):
    """Adding i_A to an identity derived at i_A = 0 double-counts entries into totale.

    It raises claims 0.84% against the consistent basis - which matters less than the
    fact that it puts the lives in the wrong state, because *partielle* pays half.
    """
    base = lifetime_claims(fr_dep_anchor)
    model = read_variant("bolted")
    try:
        model.Projection.inc_rate_partial.formula = NO_AGGRAVATION_IN_IDENTITY_P
        model.Projection.inc_rate_total.formula = NO_AGGRAVATION_IN_IDENTITY_T
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.aggravation_rate == 0.20            # still aggravating
        assert lifetime_claims(proj) / base - 1 == pytest.approx(0.0084, abs=0.0002)
        # The same identity run consistently, with no aggravation anywhere, is +0.54%.
        model.Projection.aggravation_rate = 0.0
        model.Projection.clear_all()
        assert lifetime_claims(model.Projection[1]) / base - 1 == pytest.approx(
            0.0054, abs=0.0002)
    finally:
        model.close()


def test_the_identity_carries_its_mortality_terms_and_floors_both_rates(dependance):
    """Dropping mu_T pi_T would understate i_T: the terms are not refinements.

    And i_P can go negative at extreme ages.  On the notes' female basis the floor never
    binds below the terminal age - i_P is still 0.004 at attained age 109 - but on the
    male basis it does, at 109 on model point 10, so the guard is not decoration.
    """
    p = dependance.Projection[1]
    t = 180                                             # attained age 85
    pi_p, pi_t = p.prev_partial(t), p.prev_total(t)
    slope_only = p.severity_share("total") * p.prev_slope(t) / (1.0 - pi_p - pi_t)
    assert slope_only < p.inc_rate_total(t)
    assert p.inc_rate_total(t) / slope_only > 1.5
    assert p.mort_force_avg(t) > p.mort_force(t)        # two of three states are heavier
    assert all(p.inc_rate_partial(u) >= 0.0 for u in range(0, 480, 12))
    assert all(p.inc_rate_total(u) >= 0.0 for u in range(0, 480, 12))
    assert 0.0 < p.inc_rate_partial(12 * 39) < p.inc_rate_partial(12 * 30)
    male = dependance.Projection[10]
    assert male.sex() == "M"
    assert male.inc_rate_partial(12 * 30) > 0.0         # attained age 108
    assert male.inc_rate_partial(12 * 31) == 0.0        # attained age 109: floored
    assert male.inc_rate_total(12 * 31) > 0.0


# ---------------------------------------------------------------------------
# Pitfall: premium income rides on the autonomous ledger


def test_premiums_are_never_carried_on_the_whole_in_force_block(dependance):
    """Recognised lives are exonerated and reduced lives are paid up.

    On the base cell, at attained age 90 those two bands together are 44.6% of the
    in-force block, so charging premium to pols_if would overstate income by that
    much.  The same fact makes lapse a decrement of the autonomous ledger alone.
    """
    for point_id in dependance.Data.model_point_table().index:
        proj = dependance.Projection[point_id]
        for t in (0, 12, 120):
            if t >= proj.proj_len() or not proj.premium_due(t):
                continue
            assert proj.premiums(t) == pytest.approx(
                proj.premium_mth_pp(t) * proj.premium_months() * proj.pols_prem(t),
                rel=1e-14), (point_id, t)
            assert proj.pols_prem(t) <= proj.pols_if(t) + 1e-15
    p, t = dependance.Projection[1], 240
    assert p.age(t) == 90
    assert p.pols_auto(t) == pytest.approx(0.133256, abs=STATE)
    assert p.pols_red(t) == pytest.approx(0.070326, abs=STATE)
    assert p.pols_part(t) == pytest.approx(0.010324, abs=STATE)
    assert p.pols_tot(t) + p.pols_totr(t) == pytest.approx(0.026742, abs=STATE)
    assert p.pols_if(t) == pytest.approx(0.240648, abs=STATE)
    assert (p.pols_if(t) - p.pols_auto(t)) / p.pols_if(t) == pytest.approx(
        0.446, abs=0.0005)
    # The same fact seen twice: lapse applies to the autonomous ledger alone.
    p = dependance.Projection[1]
    for t in (0, 12, 200):
        assert p.pols_lapse(t) == pytest.approx(
            p.pols_auto(t) * (1 - p.mort_rate_mth(t)) * p.lapse_rate_mth(t), rel=1e-14)
    claim_cell = dependance.Projection[9]
    assert claim_cell.status() == "partial"
    assert all(claim_cell.pols_lapse(t) == 0.0 for t in (0, 12, 200))
    assert all(dependance.Projection[11].pols_lapse(t) == 0.0 for t in (0, 12, 200))


def test_turning_lapse_off_raises_both_sides(fr_dep_anchor):
    """+78.1% claims and +56.8% premiums: persistency is a first-order assumption.

    Doubles as the input-swap test: pointing a filename Reference at a different file
    changes the projection with no formula change at all, which is what a production user
    does with a portfolio persistency study.
    """
    base = lifetime_claims(fr_dep_anchor)
    base_prem = fr_dep_anchor.result_cf()["premiums"].sum()
    model = read_variant("nolapse")
    alt = model.Data.input_dir() / "lapse_table_zero.csv"
    try:
        write_csv(alt, ["policy_year", "lapse_rate", "provenance"],
                  [[1, "0.00", "test only"]])
        model.Data.lapse_table_file = "lapse_table_zero.csv"
        model.Data.clear_all()
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.lapse_rate(0) == 0.0
        assert lifetime_claims(proj) / base - 1 == pytest.approx(0.781, abs=0.002)
        assert proj.result_cf()["premiums"].sum() / base_prem - 1 == pytest.approx(
            0.568, abs=0.002)
        assert proj.result_cf()["pols_red"].max() == 0.0
    finally:
        alt.unlink(missing_ok=True)
        model.close()


# ---------------------------------------------------------------------------
# Pitfall: the capital is paid once per membership, and the duration clock


def test_the_capital_is_paid_once_per_membership_not_once_per_state(dependance):
    """An aggravating life takes nothing further, and a reduced membership has lost it."""
    p = dependance.Projection[1]
    assert p.cover_partial() is True
    for t in (0, 12, 200, 300):
        assert p.pols_capital_claims(t) == pytest.approx(
            p.pols_entry_partial(t) + p.pols_entry_total(t), rel=1e-12)
        assert p.claims(t, "CAPITAL") == pytest.approx(
            p.capital_pp(t) * p.pols_capital_claims(t), rel=1e-14)
    assert p.pols_aggravation(200) > 0.0               # real, and carrying no capital
    assert p.pols_entry_total_red(300) > 0.0
    assert p.pols_recognition(300) > p.pols_capital_claims(300)
    # A cell that declines the option pays nothing at all on that line.
    p3 = dependance.Projection[3]
    assert p3.capital_option() is False and p3.capital_amount() == 0.0
    assert (p3.result_cf()["claims_capital"] == 0.0).all()
    assert p3.result_cf()["claims_rente"].sum() > 0.0


def test_the_rente_in_payment_moves_at_a_different_rate_from_the_guarantee(
        fr_dep_anchor):
    """reval_guarantee sets the amount at recognition; reval_rente moves it after."""
    p = fr_dep_anchor
    assert p.rente_pay_pp(12, 12) == pytest.approx(1000.0 * 1.015, rel=1e-12)
    assert p.rente_pay_pp(13, 1) == pytest.approx(1000.0 * 1.010, rel=1e-12)
    old = p.rente_pay_pp(120, 120)                     # recognised in policy year 1
    new = p.rente_pay_pp(120, 1)                       # recognised in policy year 10
    assert p.policy_year(120 - 120) == 1 and p.policy_year(120 - 1) == 10
    assert old == pytest.approx(1000.0 * 1.015 ** 10, rel=1e-12)
    assert new == pytest.approx(1000.0 * 1.010 ** 9 * 1.015, rel=1e-12)
    # The older cohort is on the larger amount, because rentes in payment index faster
    # than guarantees do.  Collapsing the two rates into one would lose that entirely.
    assert old > new
    assert old != pytest.approx(new, rel=1e-6)


def test_the_duration_index_runs_from_first_recognition(fr_dep_anchor):
    """A cohort that aggravates keeps its z, so it does not serve a second franchise.

    Restarting the clock would drop three instalments per aggravated life.  The totale
    ledger at a given duration holds the direct entrants of that vintage plus everyone
    who has aggravated into it since.
    """
    p = fr_dep_anchor
    assert p.pols_tot_dur(1, 1) == pytest.approx(p.pols_entry_total(0), rel=1e-14)
    direct = p.pols_entry_total(0) * (1 - p.mort_rate_total_mth(0)) ** 3
    assert p.pols_tot_dur(4, 4) > direct
    assert p.pols_tot_dur(4, 1) == pytest.approx(p.pols_entry_total(3), rel=1e-14)
    assert p.pols_part_dur(4, 1) == pytest.approx(p.pols_entry_partial(3), rel=1e-14)
    # The two-dimensional view agrees with the ledger totals, and out of range is zero.
    for t in (1, 12, 200):
        n = p.max_dur()
        assert p.pols_part(t) == pytest.approx(
            sum(p.pols_part_dur(t, z) for z in range(1, n + 1)), rel=1e-12)
        assert p.pols_tot(t) == pytest.approx(
            sum(p.pols_tot_dur(t, z) for z in range(1, n + 1)), rel=1e-12)
    assert p.pols_part_dur(5, 0) == 0.0 == p.pols_part_dur(5, 10 ** 6)
    # Holding a returned list cannot corrupt the cache.
    before = p.pols_part(30)
    p.dep_cohorts(30)[0][0] = 999.0
    assert p.pols_part(30) == pytest.approx(before, rel=1e-14)


def test_a_seeded_claim_starts_at_its_stated_duration(dependance):
    """Model point 9 is a partielle claim already 18 months old, so it enters cohort 19."""
    p = dependance.Projection[9]
    assert p.status() == "partial" and p.claim_duration_months() == 18
    assert p.pols_part_dur(0, 19) == 1.0 and p.pols_part_dur(0, 1) == 0.0
    assert p.pols_auto(0) == 0.0 and p.pols_part(0) == 1.0
    assert p.claims(0, "RENTE") > 0.0          # past its franchise from month zero
    assert p.claims(0, "CAPITAL") == 0.0       # already taken, before the valuation
    assert p.premiums(0) == 0.0                # exonerated
    tot = dependance.Projection[10]
    assert tot.status() == "total" and tot.pols_tot_dur(0, 7) == 1.0
    # Paid on the survivors of the month, so a shade under the full rente.
    assert tot.claims(0, "RENTE") == pytest.approx(
        900.0 * (1 - tot.mort_rate_total_mth(0)), rel=1e-12)


# ---------------------------------------------------------------------------
# cover_type, recovery and the premium


def test_a_total_only_cell_does_not_recognise_partielle(dependance):
    """Model point 2 buys the rente totale alone.

    Partielle then pays no rente, carries no capital and does not exonerate the premium,
    and the carence and the franchise both attach at entry into totale.  The health chain
    is untouched, which is what keeps the prevalence identity intact.
    """
    p = dependance.Projection[2]
    assert p.cover_type() == "total_only" and p.cover_partial() is False
    assert p.partial_ratio() == 0.50           # the model point still records it
    assert p.partial_ratio_paid() == 0.0 and p.rente_partial_pp(0) == 0.0
    assert p.pols_part(120) > 0.0
    assert p.pols_prem(120) == pytest.approx(p.pols_auto(120) + p.pols_part(120),
                                             rel=1e-14)
    assert p.premiums(120) > p.premium_mth_pp(120) * p.pols_auto(120)
    assert p.pols_aggravation_recog(120) > 0.0
    assert p.pols_capital_claims(120) == pytest.approx(
        p.pols_entry_total(120) + p.pols_aggravation_recog(120), rel=1e-12)
    assert p.aggravation_carence(0) == p.carence_factor(0)
    assert dependance.Projection[1].aggravation_carence(0) == 1.0
    for q in (p, dependance.Projection[1]):
        assert q.pols_auto(1) == pytest.approx(
            q.pols_base(0) * (1 - q.inc_rate_partial_mth(0)
                              - q.inc_rate_total_mth(0)), rel=1e-14)


def test_recovery_is_a_named_input_held_at_zero(fr_dep_anchor):
    """Wired into the ledger roll and set to zero, as the actuarial reference does.

    Turning it on lowers claims and raises premiums - the direction of the error the base
    run accepts - and all three roll-forward checks still close.
    """
    p = fr_dep_anchor
    assert p.recovery_rate == 0.0 and p.recovery_rate_mth() == 0.0
    assert all(p.pols_recovery(t) == 0.0 for t in (0, 12, 200))
    assert all(p.pols_recovery_red(t) == 0.0 for t in (0, 12, 200))
    base, base_prem = lifetime_claims(p), p.result_cf()["premiums"].sum()
    model = read_variant("recovery")
    try:
        model.Projection.recovery_rate = 0.05
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.pols_recovery(200) > 0.0
        assert lifetime_claims(proj) < base
        assert proj.result_cf()["premiums"].sum() > base_prem
        assert proj.check_pols_roll_fwd() is True
        assert proj.check_part_roll_fwd() is True
        assert proj.check_tot_roll_fwd() is True
    finally:
        model.close()


def test_the_premium_indexes_with_the_guarantee_and_the_revision(fr_dep_anchor):
    """Nil revision for five years, then 1.5% on top of the 1.0% revalorisation.

    The premium-shock lapse module is off while the revision path stays below its 2%
    threshold; a revision at the 10% cap gives 1.24.
    """
    p = fr_dep_anchor
    assert [p.revision_rate(12 * (y - 1)) for y in (1, 5, 6, 40)] == pytest.approx(
        [0.0, 0.0, 0.015, 0.015], abs=1e-12)
    assert p.premium_mth_pp(0) == 75.0
    assert p.premium_mth_pp(12) == pytest.approx(75.0 * 1.01, rel=1e-12)
    assert p.premium_mth_pp(48) == pytest.approx(75.0 * 1.01 ** 4, rel=1e-12)
    assert p.premium_mth_pp(60) == pytest.approx(75.0 * 1.01 ** 5 * 1.015,
                                                 rel=1e-12)
    # steps on anniversaries only
    assert p.premium_mth_pp(11) == p.premium_mth_pp(0)
    # premium_pp is the ANNUAL amount library-wide; premium_mth_pp the monthly one
    assert p.premium_pp(60) == pytest.approx(12 * p.premium_mth_pp(60), rel=1e-14)
    assert all(p.revision_lapse_factor(t) == 1.0 for t in (0, 60, 200))
    assert p.lapse_rate(60) == p.lapse_rate_base(60)
    model = read_variant("shock")
    try:
        model.Projection.revision_rate.formula = "lambda t: 0.10"
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.revision_lapse_factor(0) == pytest.approx(1.24, rel=1e-12)
        assert proj.lapse_rate(0) > proj.lapse_rate_base(0)
    finally:
        model.close()


def test_the_premium_mode_and_the_couple_discount(dependance):
    """Model point 8 pays annually and point 5 takes the 10% reduction couple."""
    p = dependance.Projection[8]
    assert p.premium_mode() == "annual" and p.premium_months() == 12
    assert p.premium_due(0) and p.premium_due(12) and not p.premium_due(1)
    assert p.premiums(1) == 0.0
    assert p.premiums(0) == pytest.approx(12 * 75.0 * p.pols_auto(0), rel=1e-12)
    assert p.cum_prem_pp(0) == pytest.approx(900.0, rel=1e-12)
    # Paying in advance is worth money on a decrementing block.
    assert p.result_cf()["premiums"].sum() > dependance.Projection[1].result_cf()[
        "premiums"].sum()
    p5 = dependance.Projection[5]
    assert p5.couple_discount() is True
    assert p5.couple_factor() == pytest.approx(0.90, rel=1e-12)
    assert p5.premium_mth_pp(0) == pytest.approx(0.90 * p5.premium_mth(),
                                                 rel=1e-12)
    assert dependance.Projection[1].couple_factor() == 1.0


# ---------------------------------------------------------------------------
# The trigger grid and the shipped tables


def test_raising_the_severity_shares_raises_claims_and_lowers_premiums(
        fr_dep_anchor, dependance):
    """A tenth more prevalence read as insured moves claims +8.06% and premiums -1%.

    The shares are the whole of the public-to-insured translation and they are [std]
    against two indirect anchors, so this is the sensitivity the notes rank third.
    They are also the only route by which the trigger grid reaches the chain.
    """
    base = lifetime_claims(fr_dep_anchor)
    base_prem = fr_dep_anchor.result_cf()["premiums"].sum()
    model = read_variant("shares")
    alt = model.Data.input_dir() / "severity_share_alt.csv"
    try:
        write_csv(alt, ["trigger_grid", "share_partial", "share_total", "provenance"],
                  [["avq5", "0.165", "0.330", "test only"]])
        model.Data.severity_share_file = "severity_share_alt.csv"
        model.Data.clear_all()
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert lifetime_claims(proj) / base - 1 == pytest.approx(0.0806, abs=0.0005)
        assert proj.result_cf()["premiums"].sum() / base_prem - 1 == pytest.approx(
            -0.0096, abs=0.0005)
    finally:
        alt.unlink(missing_ok=True)
        model.close()
    # Three grids are three definitions of the same two states, and one lookup
    # stands between them and the chain.
    p1, p2, p3 = (dependance.Projection[1], dependance.Projection[2],
                  dependance.Projection[3])
    assert (p1.trigger_grid(), p2.trigger_grid(), p3.trigger_grid()) == (
        "avq5", "avq6", "aggir")
    assert p2.severity_share("total") == pytest.approx(0.30 * 0.85, abs=1e-6)
    assert p3.severity_share("total") == pytest.approx(0.30 * 1.25, abs=1e-6)
    assert p2.severity_share("total") < p1.severity_share("total") < p3.severity_share(
        "total")
    names = set(dependance.Projection.cells) | set(dependance.Projection.refs)
    assert not [n for n in names if "grid" in n and n != "trigger_grid"]


def test_the_shipped_tables_mark_their_own_provenance(dependance):
    """Every input file says in words what kind of claim each of its rows is.

    And the prevalence logistic reproduces the two sourced DREES anchors per sex that
    pin its slope, which is the only part of that curve any document supports.
    """
    import pandas as pd

    d = MODEL_DIR.parent
    mort = pd.read_csv(d / "mort_table.csv")
    assert mort["provenance"].notna().all()
    assert all("[std]" in v for v in mort["provenance"])
    assert set(mort["sex"]) == {"M", "F"}
    female = mort[mort["sex"] == "F"].set_index("age")["mort_rate"]
    male = mort[mort["sex"] == "M"].set_index("age")["mort_rate"]
    assert female[60] == pytest.approx(0.00400, abs=5e-6)
    assert female[90] == pytest.approx(0.10500, abs=5e-6)
    assert all(male[a] > female[a] for a in (60, 80, 100))

    prev = pd.read_csv(d / "prevalence_table.csv")
    assert set(prev["param"]) == {"prev_ceil", "prev_beta", "prev_x_mid"}
    assert all("[std]" in v for v in prev["provenance"])
    assert all(v == 0.90 for v in prev.loc[prev["param"] == "prev_ceil", "value"])

    shares = pd.read_csv(d / "severity_share_table.csv")
    assert set(shares["trigger_grid"]) == {"avq5", "avq6", "aggir"}
    assert sum("NO retrieved document" in v for v in shares["provenance"]) == 2

    for name in ("lapse_table.csv", "cause_mix_table.csv", "reduction_table.csv",
                 "revision_table.csv"):
        assert pd.read_csv(d / name)["provenance"].notna().all(), name
    assert pd.read_csv(d / "cause_mix_table.csv")["share"].sum() == pytest.approx(
        1.0, abs=1e-12)
    # The two slope parameters reproduce their sourced DREES anchors exactly:
    # 20% of women and 13% of men at 84.5, 54% and 40% at 93.  The ceiling is pinned
    # by nothing, and below age 60 APA has no anchor at all.
    for point_id, low, high in ((1, 0.20, 0.54), (2, 0.13, 0.40)):
        p = dependance.Projection[point_id]
        ceil = p.prev_param("prev_ceil")
        beta = p.prev_param("prev_beta")
        x_mid = p.prev_param("prev_x_mid")
        for x, target in ((84.5, low), (93.0, high)):
            got = ceil / (1.0 + math.exp(-beta * (x - x_mid)))
            assert got == pytest.approx(target, abs=1e-9), (point_id, x)
    # 9.1% of women against 4.8% of men receive APA, so the male curve sits lower.
    assert dependance.Projection[2].prev_rate(12 * 20) < dependance.Projection[
        1].prev_rate(12 * 15)                          # both at attained age 85
    p5 = dependance.Projection[5]
    assert p5.age_at_entry() == 55 and 0.0 < p5.prev_rate(0) < 0.005
# ---------------------------------------------------------------------------
# The population identities and what the product does not have


def test_the_population_identities_close_on_every_model_point(dependance):
    """Five ledgers plus every cumulative exit equals the starting population.

    Incidence, aggravation and the *mise en réduction* are deliberately absent from the
    in-force roll-forward, because they move lives between ledgers rather than out of the
    policy count - which is the point of running the check on the sum.
    """
    for point_id in dependance.Data.model_point_table().index:
        proj = dependance.Projection[point_id]
        for name in ("check_states", "check_pols_roll_fwd", "check_part_roll_fwd",
                     "check_tot_roll_fwd", "check_model_point"):
            value = getattr(proj, name)()
            assert isinstance(value, bool) and value is True, (point_id, name)
    p = dependance.Projection[1]
    for t in (0, 12, 95, 200, 479):
        out = p.pols_death(t) + p.pols_lapse_exit(t) + p.pols_carence_exit(t)
        assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-13)
    assert p.pols_entry_partial(200) > 0.0
    assert p.pols_aggravation(200) > 0.0
    assert p.pols_reduction(200) > 0.0
    assert p.pols_lapse_exit(200) == pytest.approx(0.0, abs=1e-15)
    for name in ("check_pols_roll_fwd_resid", "check_states_resid",
                 "check_part_roll_fwd_resid", "check_tot_roll_fwd_resid"):
        assert getattr(p, name)(100) == pytest.approx(0.0, abs=1e-13), name


def test_check_model_point_rejects_a_policy_that_could_not_be_written(fr_dep_anchor):
    """A validation of the input, not an identity of the projection.

    A cause mix that does not sum to one would silently scale every claim on the block.
    """
    model = read_variant("badpoint")
    alt = model.Data.input_dir() / "cause_mix_alt.csv"
    try:
        write_csv(alt, ["cause", "share", "provenance"],
                  [["accident", 0.10, "test only"], ["illness", 0.55, "test only"],
                   ["neuro", 0.20, "test only"]])
        model.Data.cause_mix_file = "cause_mix_alt.csv"
        model.Data.clear_all()
        model.Projection.clear_all()
        assert model.Projection[1].check_model_point() is False
    finally:
        alt.unlink(missing_ok=True)
        model.close()


def test_the_product_has_no_surrender_value_no_death_benefit_and_no_maturity(dependance):
    """Three absences that are product facts, not gaps."""
    for point_id in dependance.Data.model_point_table().index:
        assert (dependance.Projection[point_id].result_cf()["claims_lapse"]
                == 0.0).all(), point_id
    names = set(dependance.Projection.cells) | set(dependance.Projection.refs)
    for absent in ("claims_death", "av_pp_at", "av_at", "cv_pp", "asset_share",
                   "surr_charge_rate", "pols_maturity", "maturity_age"):
        assert absent not in names
    with pytest.raises(FormulaError):
        dependance.Projection[1].claims(0, "DEATH")
    # Cover is viagere: what ends the projection is the terminal age of the basis.
    p = dependance.Projection[1]
    assert p.proj_len() == 12 * (p.terminal_age - p.age_at_entry())
    assert p.age(p.proj_len() - 1) == 109
    # The enum accessors validate rather than propagating a typo into a lookup.
    for call in (lambda: p.pols_if_at(0, "BEF_NOTHING"),
                 lambda: p.claims(0, "MATURITY"),
                 lambda: p.severity_share("moderate"),
                 lambda: p.carence_months("cancer")):
        with pytest.raises(FormulaError):
            call()


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_decomposition(dependance):
    """The columns are a decomposition of net_cf and of pols_if, not a selection."""
    df = dependance.Projection[1].result_cf()
    assert df.index.name == "t" and list(df.index) == list(range(480))
    assert list(df.columns) == [
        "pols_if", "pols_auto", "pols_red", "pols_part", "pols_tot", "pols_totr",
        "premiums", "claims_rente", "claims_capital", "claims_lapse",
        "refunds_carence", "expenses", "claim_expenses", "net_cf",
    ]
    assert "claims" not in df.columns        # no subtotal beside its parts
    assert "disc_factor" not in df.columns   # nothing here is discounted
    for point_id in (1, 2, 9, 11):
        d = dependance.Projection[point_id].result_cf()
        outgo = d[["claims_rente", "claims_capital", "claims_lapse",
                   "refunds_carence", "expenses", "claim_expenses"]].sum(axis=1)
        assert (d["premiums"] - outgo - d["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-9), point_id
        ledgers = d[["pols_auto", "pols_red", "pols_part", "pols_tot",
                     "pols_totr"]].sum(axis=1)
        assert (d["pols_if"] - ledgers).abs().max() == pytest.approx(0.0, abs=1e-12)


def test_every_model_point_projects(dependance):
    """A point the shipped tables cannot serve is a defect, not a limitation."""
    ids = list(dependance.Data.model_point_table().index)
    assert 8 <= len(ids) <= 12
    columns = None
    for point_id in ids:
        df = dependance.Projection[point_id].result_cf()
        assert len(df) > 0 and df.notna().all().all(), point_id
        assert abs(df["net_cf"].sum()) < float("inf")
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns, point_id
    assert {dependance.Projection[i].status() for i in ids} == {
        "autonomous", "partial", "total", "reduced"}


def test_expenses_split_the_per_policy_and_the_per_event_halves(fr_dep_anchor):
    """3.00 and 1.20 a month inflating at 1.5%, against 250 and 10 flat per event."""
    p = fr_dep_anchor
    for t in (0, 12, 200):
        f = 1.015 ** p.duration(t)
        expected = 3.0 * f * p.pols_if(t) + 1.2 * f * (p.pols_if(t) - p.pols_red(t))
        if t == 0:
            expected += 150.0
        assert p.expenses(t) == pytest.approx(expected, rel=1e-12)
        assert p.claim_expenses(t) == pytest.approx(
            250.0 * p.pols_recognition(t) + 10.0 * p.instalments(t), rel=1e-12)
    # Assistance ends on mise en reduction, so its base excludes the reduced ledger.
    assert p.pols_red(200) > 0.0
    assert p.expenses(200) < 4.2 * 1.015 ** p.duration(200) * p.pols_if(200)


def test_the_documentation_describes_the_current_structure(dependance):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = dependance.doc
    for phrase in ("dependance", "mechanics demonstration", "external",
                   "once per model", "carence", "franchise",
                   "State-dependent mortality", "Data", "Projection"):
        assert phrase in doc, phrase
    proj = dependance.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "pols_auto", "pols_red", "pols_part",
                  "dep_cohorts", "carence_factor", "inc_rate_total", "sojourn_total"):
        assert cells in proj
    data = dependance.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "prevalence_table",
                  "severity_share_table"):
        assert cells in data


def test_cells_names_follow_the_library_vocabulary(dependance):
    """Names shared with lifelib and with the rest of this library must not drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "proj_len", "age", "pols_if",
        "pols_if_at", "pols_if_init", "pols_lapse", "mort_rate", "mort_rate_mth",
        "lapse_rate", "lapse_rate_mth", "premiums", "claims", "expenses",
        "expense_maint", "inflation_rate", "inflation_factor", "net_cf",
        "result_cf", "policy_year", "duration", "duration_mth",
    }
    names = set(dependance.Projection.cells) | set(dependance.Projection.refs)
    assert shared <= names, "missing: %s" % sorted(shared - names)
    retired = {"lapse_rate_ann", "free_wd_used_pp", "free_wd_taken_pp", "prem_net_pp",
               "mort_a_e_factor", "ae_factor", "omega", "check_tol"}
    assert not (names & retired)
    # A monthly rate must be strictly smaller than the annual one it comes from.
    p = dependance.Projection[1]
    for t in (0, 12, 200):
        assert p.mort_rate_mth(t) < p.mort_rate(t)
        assert p.mort_rate_partial_mth(t) < p.mort_rate_partial(t)
        assert p.mort_rate_total_mth(t) < p.mort_rate_total(t)
        assert p.lapse_rate_mth(t) < p.lapse_rate(t)
        assert p.inc_rate_partial_mth(t) < p.inc_rate_partial(t)
        assert p.inc_rate_total_mth(t) < p.inc_rate_total(t)


def test_inputs_live_beside_the_model_and_are_read_once(dependance):
    """Eight external CSVs in the parent directory, and one Data Space behind them."""
    expected = {"model_point_table.csv", "mort_table.csv", "prevalence_table.csv",
                "severity_share_table.csv", "lapse_table.csv", "cause_mix_table.csv",
                "reduction_table.csv", "revision_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}
    assert {p.name for p in MODEL_DIR.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}
    assert dependance.Projection[1].data is dependance.Data
    assert dependance.Projection[1].data is dependance.Projection[9].data
    assert "input_dir" not in dependance.Projection.cells


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Dep_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv_file in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv_file, tmp_path / csv_file.name)

    reread = mx.read_model(dest, name="Dep_FR_S_rt")
    try:
        proj = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert proj.pols_auto(t) == pytest.approx(row[0], abs=STATE)
            assert proj.net_cf(t) == pytest.approx(row[8], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
