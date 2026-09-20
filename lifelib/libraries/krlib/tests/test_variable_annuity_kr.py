"""Golden and structural tests for VA_KR_S.

The golden values are the worked example in
``products/variable_annuity/technical-notes.md`` ("Worked example"), which projects the
anchor cell: 남자, **보험나이 40**, 기본보험료 ₩300,000 월납, 10년납, 연금개시나이 60,
보증형, 채권형 50% / 주식형 50%, on the ``base`` return path and the ``decl_2026``
crediting basis — the illustration cell three independent carriers publish, and the only
cell at which the composite's parameters can be checked against published surrender-value
tables.  They are hard-coded here rather than pickled so that a reviewer can compare them
against the notes by eye.

Tolerances follow the precision the notes display: money to the won's second decimal in
the cash-flow tables, and to the tenth decimal in the hand traces, which print the model's
own double-precision residues rather than the round contractual amounts.

This is the library's only **특별계정** (separate account) product, so the module carries
more than a cash-flow comparison.  A 변액연금보험 has to cross the 특별계정 / 일반계정
boundary to state its own cash-flow identity, and a model that cannot state it has not
represented the boundary; ``check_net_cf()`` is that statement and it is asserted here on
both ledgers as well as in aggregate.  The fee stack a Korean 상품요약서 discloses is
asserted line by line, because the lines come off **four bases at three deduction points**
and collapsing them into one charge is the error the split columns exist to prevent.

Every product fact the notes list under **Known modeling pitfalls** earns its own test,
named after the pitfall, because each of them is a way an implementation can look right
and be wrong:

* the GMAB charge has **two** components on **two** bases, in the ratio 1 : 158;
* the premium-based component stops at the *shorter* of the 납입기간 and seven years;
* the monthly deduction **rises** at 납입완료 and does not fall;
* the front-end charges never reach the 특별계정 at all;
* the 운용보수 is a factor inside the 기준가격, not a cancellation of units;
* the GMAB is a **European option struck on one date**, not a floor at every duration;
* its residual against the charge collected on one path is not a profit;
* the death benefit is gross, and splits exactly into fund and guarantee;
* the surrender value is floored at zero, and is nil for the first three months;
* the 해약공제 runs off linearly in the **amount**, not in the ratio;
* the 표준해약공제액 cap binds on three shipped points and is invisible on the anchor;
* the guaranteed instalment is owed to every contract that annuitised, alive or not;
* both the death and the surrender streams stop dead at 연금개시;
* the deferral and the payout are priced on **two** mortality tables;
* ``proj_len()`` is the number of projected months and not the last row index;
* death is decremented before 해지;
* the asset-based charges are struck **after** the premium goes in;
* the mandatory 채권형 ladder is by 연금개시 전 보험기간, not by fund choice;
* the pre-annuitisation de-risking fires inside its window and conserves the total;
* a 중도인출 re-bases **both** guarantee strikes proportionally;
* no ``claims`` subtotal is published beside the split columns;
* ``net_cf`` excludes investment return and ``charge_income`` is a memo;
* every age is **보험나이**; and
* ``mort_table.csv`` is a [std] construction and not the 경험생명표.

The eight ``check_*`` cells this model publishes are asserted **by name**, because a
generic sweep discovers checks and so cannot notice one that has quietly disappeared, and
the [std] scalar assumptions the notes state are read off the model so that a silent
change to an assumption fails a test rather than moving a result.
"""
import pathlib

import pandas as pd
import pytest

from kr_registry import LIB, MODELS

WON = 0.005          # money displayed to 2 d.p.
FINE = 5e-10         # money and rates displayed to 10 d.p. in the hand traces
INFORCE = 5e-11      # in-force counts, displayed to 10 d.p.

MODEL_DIR = LIB / MODELS["VA_KR_S"][0]
CSV_DIR = MODEL_DIR.parent


def near(x):
    """The notes' full-precision figures: 1e-12 relative, or 5e-10 absolute.

    The traces print the model's own doubles — ``0.2305555556 x 3,600,000`` is
    ``830000.0001599999`` and not ₩830,000 — so an exact equality here would assert the
    last two bits of a float rather than anything about the product.
    """
    return pytest.approx(x, rel=1e-12, abs=FINE)


# ---------------------------------------------------------------------------
# The notes' worked example, hard-coded
#
# "The anchor cell and every assumption it uses" — the derived quantities.

PROJ_LEN = 960  # the month *count*, the frame's exclusive end; the last row is t = 959
SURR_CHG_CAP_PP = 1643940.00

# "The charge stack in month 0, per contract": five lines, three deduction points,
# four bases.  cells name -> the notes' figure.
CHARGE_STACK_0 = {
    "acq_charge_pp": 15510.00,
    "maint_charge_in_pp": 10500.00,
    "other_charge_pp": 0.00,
    "prem_to_av_pp": 273990.00,
    "risk_prem_pp": 24.000000000000004,
    "maint_charge_after_pp": 0.00,
    "gmdb_charge_pp": 15.98275,
    "gmab_charge_asset_pp": 57.081250000000004,
    "gmab_charge_prem_pp": 9000.00,
    "mth_deduct_pp": 9097.063999999998,
    "mgmt_fee_pp": 110.64426393373063,
    "fund_expense_pp": 0.00,
    "surr_chg_pp": 830000.0001599999,
}

# "The surrender-charge scale, to the won": surr_chg_pp(12k) for k = 0 ... 8.
SURR_SCALE = {
    0: 830000.0001599999, 1: 711428.5715657143, 2: 592857.1429714285,
    3: 474285.7143771428, 4: 355714.2857828572, 5: 237142.8571885714,
    6: 118571.4285942857, 7: 0.0, 8: 0.0,
}

# "First periods of the base run", per contract, income-positive, two decimals.
# t -> (pols_if, premiums, claims_death, claims_lapse, expenses, commissions, net_cf)
WORKED_EXAMPLE = {
    0:  (1.0000000000, 300000.00,  27.86,     0.00, 303000.00, 40200.00, -43227.86),
    1:  (0.9729056091, 291871.68,  54.21,     0.00,   2918.72, 39110.81, 249787.95),
    2:  (0.9465453242, 283963.60,  79.11,     0.00,   2839.64, 38051.12, 242993.73),
    3:  (0.9208992552, 276269.78, 102.63,  5833.06,   2762.70, 37020.15, 230551.24),
    4:  (0.8959480508, 268784.42, 124.81, 12142.30,   2687.84, 36017.11, 217812.35),
    5:  (0.8716728841, 261501.87, 145.71, 18116.58,   2615.02, 35041.25, 205583.30),
    6:  (0.8480554382, 254416.63, 165.39, 23769.13,   2544.17, 34091.83, 193846.11),
    7:  (0.8250778927, 247523.37, 183.90, 29112.73,   2475.23, 33168.13, 182583.38),
    8:  (0.8027229098, 240816.87, 201.28, 34159.69,   2408.17, 32269.46, 171778.28),
    9:  (0.7809736215, 234292.09, 217.58, 38921.90,   2342.92, 31395.14, 161414.54),
    10: (0.7598136169, 227944.09, 232.86, 43410.83,   2279.44, 30544.51, 151476.44),
    11: (0.7392269297, 221768.08, 247.14, 50004.27,   2217.68, 29716.92, 139582.06),
    12: (0.7191980263, 215759.41, 280.40, 40913.80,   2157.59,  8846.14, 163561.47),
    13: (0.7043896277, 211316.89, 295.75, 43992.11,   2113.17,  8663.99, 156251.87),
    14: (0.6898861362, 206965.84, 310.35, 46933.14,   2069.66,  8485.60, 149167.09),
    15: (0.6756812739, 202704.38, 324.23, 49741.13,   2027.04,  8310.88, 142301.11),
}

# "The account behind those rows", per contract.
# t -> (av_pp, mth_deduct_pp, surr_chg_pp, cv_pp, prem_paid_pp, db_pp, gmdb_claim_pp)
WORKED_EXAMPLE_AV = {
    0:  (265435.59,  9097.06, 830000.00,       0.00,  300000.00,  300000.00,  34564.41),
    1:  (531344.02,  9167.85, 830000.00,       0.00,  600000.00,  600000.00,  68655.98),
    2:  (797726.13,  9238.76, 830000.00,       0.00,  900000.00,  900000.00, 102273.87),
    3:  (1064582.77, 9309.79, 830000.00,  234582.77, 1200000.00, 1200000.00, 135417.23),
    4:  (1331914.78, 9380.95, 830000.00,  501914.78, 1500000.00, 1500000.00, 168085.22),
    11: (3216620.89, 9882.65, 711428.57, 2505192.32, 3600000.00, 3600000.00, 383379.11),
    12: (3487786.59, 9954.83, 711428.57, 2776358.02, 3900000.00, 3900000.00, 412213.41),
}

# "The rows where the product does something": every event row of the statement.
# t -> (pols_if, premiums, claims_death, claims_lapse, claims_annuity, expenses,
#       commissions, net_cf)
EVENT_ROWS = {
    0: (1.0000000000, 300000.00, 27.86, 0.00, 0.00, 303000.00, 40200.00, -43227.86),
    3: (0.9208992552, 276269.78, 102.63, 5833.06, 0.00, 2762.70, 37020.15, 230551.24),
    12: (0.7191980263, 215759.41, 280.40, 40913.80, 0.00, 2157.59, 8846.14, 163561.47),
    83: (0.2883626523, 86508.80, 1072.96, 54234.14, 0.00, 865.09, 0.00, 30336.61),
    84: (0.2860629838, 85818.90, 1168.83, 48216.27, 0.00, 858.19, 0.00, 35575.60),
    119: (0.2229441583, 66883.25, 1519.23, 55276.40, 0.00, 668.83, 0.00, 9418.79),
    120: (0.2213584991, 0.00, 1641.83, 54973.95, 0.00, 664.08, 0.00, -57279.86),
    121: (0.2197804374, 0.00, 1630.13, 54673.17, 0.00, 659.34, 0.00, -56962.64),
    203: (0.1215837337, 0.00, 1744.87, 34696.10, 0.00, 364.75, 0.00, -36805.73),
    204: (0.1206998103, 0.00, 1897.78, 34502.45, 0.00, 362.10, 0.00, -36762.34),
    239: (0.0932722265, 0.00, 1866.77, 28329.63, 0.00, 279.82, 0.00, -30476.22),
    240: (0.0925841296, 0.00, 0.00, 0.00, 200728.58, 277.75, 0.00, -201006.33),
    241: (0.0925471325, 0.00, 0.00, 0.00, 0.00, 277.64, 0.00, -277.64),
    252: (0.0921411381, 0.00, 0.00, 0.00, 200728.58, 276.42, 0.00, -201005.00),
    348: (0.0868296734, 0.00, 0.00, 0.00, 200728.58, 260.49, 0.00, -200989.07),
    360: (0.0858776937, 0.00, 0.00, 0.00, 186188.58, 257.63, 0.00, -186446.21),
    959: (0.0000000917, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
}

# "The two guarantees at t_ann() = 240".
AV_ANN_PP = 43883943.57329801
ANNUITY_FACTOR = 20.139842488678187
ANNUITY_NET_PP = 2168066.7999254693
POLS_ANNUITISED = 0.09258412964405735
ANNUITY_FACTOR_FEMALE = 21.762174205458386

# "Undiscounted totals" over t = 0 ... 959, income-positive.
TOTALS = {
    "pols_if": 99.6122423885,
    "premiums": 15215257.48,
    "claims_death": 310883.37,
    "claims_lapse": 11077101.66,
    "claims_annuity": 5759786.33,
    "claims_maturity": 0.00,
    "withdrawals": 0.00,
    "fund_expenses": 0.00,
    "expenses": 598836.73,
    "commissions": 617364.10,
    "net_cf": -3148714.71,
}
MEMOS = {"gmdb_charges": 79244.38, "gmdb_claims": 4945.39,
         "gmab_charges": 657417.59, "gmab_claims": 0.00}
SURR_CHARGES_TOTAL = 430510.48    # named in "Key sensitivities", sensitivity 5
FIRST_TWELVE_NET_CF = 2104181.53

# "Contrasts across model points": point -> (av_ann_pp, gmab_claim_pp, annuity_net_pp,
# sum net_cf).  ``None`` where the notes print an em dash rather than a figure.
CONTRASTS = {
    1: (43883943.5733, 0.0,           2168066.7999, -3148714.7117),
    2: (43883943.5733, 0.0,           2006441.2426, None),
    3: (46722879.2288, None,          2308323.1589, -4033326.0),
    4: (25958820.3874, 10041179.6126, 1778564.0588, -192370.8500),
    5: (52811343.3686, 0.0,           2609121.0337, -5173103.5565),
}

# The eight identities the model publishes, by name.
CHECK_CELLS = {
    "check_net_cf", "check_pols_roll_fwd", "check_av_roll_fwd", "check_charge_split",
    "check_gmdb_floor", "check_bond_floor", "check_surr_chg_cap", "check_prem_alloc",
}


# ---------------------------------------------------------------------------
# The worked example


def test_the_anchor_cell_is_the_three_carrier_illustration_point(kr_va_anchor):
    """Model point 1's fourteen attributes, as the notes list them.

    The whole worked example is arithmetic on these columns, so a model point table edited
    without the notes being re-run moves every figure below at once; this test is the one
    that says which column moved.
    """
    a = kr_va_anchor
    assert a.policy_id() == "VA-000001"
    assert (a.sex(), a.age_at_entry(), a.basic_prem_pp()) == ("M", 40, 300000.0)
    assert (a.pay_term(), a.annuity_age(), a.gmab_flag()) == (10, 60, 1)
    assert a.fund_set() == "bond50_eq50"
    assert a.scenario_id() == "base"
    assert a.crediting_basis() == "decl_2026"
    assert (a.addl_prem_ratio(), a.wd_ratio(), a.wd_start_year()) == (0.0, 0.0, 0)
    assert a.pols_if_init() == 1.0


def test_the_derived_quantities_of_the_anchor_cell(kr_va_anchor):
    """The notes' derived block: the two dates that cut the projection in two.

    ``pay_months()`` ends the premium-paying period and ``t_ann()`` empties the 특별계정.
    Between them they define all four regions of the statement, and every boundary test
    below is written against one of them.
    """
    a = kr_va_anchor
    assert a.pay_months() == 120
    assert a.t_ann() == 240 == (a.annuity_age() - a.age_at_entry()) * 12
    assert a.defer_years() == 20
    assert a.proj_len() == PROJ_LEN == (a.omega_age - a.age_at_entry()) * 12
    assert a.prem_ann_pp() == near(3600000.0)
    assert a.prem_total_pp() == near(36000000.0)
    assert a.loading_rate() == near(0.0867)
    assert a.bond_floor() == near(0.50)
    assert a.surr_chg_cap_pp() == near(SURR_CHG_CAP_PP)


def test_the_charge_stack_in_month_zero(kr_va_anchor):
    """Every line of the notes' month-0 fee-stack table, and the subtotals it feeds.

    Five charge lines, three deduction points and four bases in one month.  The lines are
    asserted individually rather than through the 월공제액 subtotal, because the subtotal
    is exactly what a model that has collapsed the stack still reproduces; the subtotals
    are asserted beside them so that a line moved from one deduction point to the other
    fails here too.
    """
    a = kr_va_anchor
    for name, expected in CHARGE_STACK_0.items():
        assert getattr(a, name)(0) == near(expected), name
    assert a.prem_alloc_ratio(0) == near(0.9133)
    assert a.maint_charge_after_pp(120) == near(3990.00)
    assert a.prem_charge_pp(0) == near(26010.00)
    assert a.prem_charge_pp(0) == near(
        a.acq_charge_pp(0) + a.maint_charge_in_pp(0) + a.other_charge_pp(0))
    assert a.prem_to_av_pp(0) == near(a.basic_prem_pp() - a.prem_charge_pp(0))
    assert a.mth_deduct_pp(0) == near(
        a.risk_prem_pp(0) + a.maint_charge_after_pp(0) + a.gmdb_charge_pp(0)
        + a.gmab_charge_pp(0))
    assert a.gmab_charge_pp(0) == near(
        a.gmab_charge_asset_pp(0) + a.gmab_charge_prem_pp(0))
    assert a.loading_rate() == near(0.0517 + 0.0350 + 0.0000)


def test_the_first_year_charge_totals_sit_inside_the_industry_band(kr_va_anchor):
    """₩425,984.29 on ₩3,600,000 of premium — 11.83%, inside [R1]'s 5–15% band.

    Over a quarter of it is the premium-based guarantee component alone, which is not on
    the fund; the two charges that *are* on the fund come to ₩5,576.29 in a year in which
    the account is still being built.
    """
    a = kr_va_anchor
    ts = range(0, 12)
    acq = sum(a.acq_charge_pp(t) for t in ts)
    maint = sum(a.maint_charge_in_pp(t) for t in ts)
    risk = sum(a.risk_prem_pp(t) for t in ts)
    gmab_prem = sum(a.gmab_charge_prem_pp(t) for t in ts)
    gmdb = sum(a.gmdb_charge_pp(t) for t in ts)
    gmab_asset = sum(a.gmab_charge_asset_pp(t) for t in ts)
    assert (acq, maint) == (near(186120.00), near(126000.00))
    assert risk == near(288.00)
    assert gmab_prem == near(108000.00)
    assert gmdb == pytest.approx(1219.81, abs=WON)
    assert gmab_asset == pytest.approx(4356.47, abs=WON)
    total = acq + maint + risk + gmab_prem + gmdb + gmab_asset
    assert total == pytest.approx(425984.29, abs=WON)
    assert total / (12 * a.basic_prem_pp()) == pytest.approx(0.1183, abs=5e-5)
    assert 0.05 < total / (12 * a.basic_prem_pp()) < 0.15
    assert gmab_prem / total > 0.25


@pytest.mark.parametrize("k", sorted(SURR_SCALE))
def test_the_surrender_charge_scale_to_the_won(kr_va_anchor, k):
    """The specification's published 해약공제 table, ``surr_chg_pp(12k)`` for k = 0 … 8.

    The most consumer-visible schedule on the product and the quantity the statutory cap
    is measured against, so it is asserted at every published rung rather than through the
    cash-flow line that consumes it.
    """
    assert kr_va_anchor.surr_chg_pp(12 * k) == near(SURR_SCALE[k])


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(kr_va_anchor, t):
    """Every cell of the notes' sixteen-row cash-flow table, to two decimals.

    The four columns the notes omit are asserted to be zero here, because "the notes do
    not print it" and "the model does not produce it" are different statements and only
    the second is a test.
    """
    pols, prem, death, lapse, exp, comm, net = WORKED_EXAMPLE[t]
    a = kr_va_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=WON)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=WON)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=WON)
    assert a.claims(t, "ANNUITY") == 0.0
    assert a.claims(t, "MATURITY") == 0.0
    assert a.withdrawals(t) == 0.0
    assert a.fund_expenses(t) == 0.0
    assert a.expenses(t) == pytest.approx(exp, abs=WON)
    assert a.commissions(t) == pytest.approx(comm, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_AV))
def test_worked_example_account_row(kr_va_anchor, t):
    """The notes' account table: the 계약자적립액 and the six quantities struck on it.

    ``av_pp`` carries the whole product — every charge, every benefit and both guarantee
    strikes are a function of it — so it is asserted separately from the cash-flow rows
    that consume it rather than being inferred from them.
    """
    av, deduct, chg, cv, paid, db, gmdb = WORKED_EXAMPLE_AV[t]
    a = kr_va_anchor
    assert a.av_pp(t) == pytest.approx(av, abs=WON)
    assert a.mth_deduct_pp(t) == pytest.approx(deduct, abs=WON)
    assert a.surr_chg_pp(t) == pytest.approx(chg, abs=WON)
    assert a.cv_pp(t) == pytest.approx(cv, abs=WON)
    assert a.prem_paid_pp(t) == pytest.approx(paid, abs=WON)
    assert a.db_pp(t) == pytest.approx(db, abs=WON)
    assert a.gmdb_claim_pp(t) == pytest.approx(gmdb, abs=WON)


def test_worked_example_month_zero_trace(kr_va_anchor):
    """The notes' month-0 hand trace, in the order the month applies it.

    Premium into the 일반계정, front-end deduction retained there, transfer to the 특별계정
    at the fixed allocation, 월공제액 struck on the post-transfer account and spread pro
    rata, then growth fund by fund.  The subtotals reconcile under several wrong orderings
    and the intermediates do not, so every intermediate the notes print is asserted.
    """
    a = kr_va_anchor
    assert a.premium_mth_pp(0) == near(300000.0)
    assert a.acq_charge_pp(0) == near(0.0517 * 300000.0)
    assert a.maint_charge_in_pp(0) == near(0.0350 * 300000.0)
    assert a.other_charge_pp(0) == 0.0
    assert a.prem_to_av_pp(0) == near(273990.0)

    assert a.fund_pp_at(0, 1, "BEF_PREM") == 0.0
    assert a.fund_pp_at(0, 1, "BEF_DEDUCT") == near(136995.0)
    assert a.fund_pp_at(0, 2, "BEF_DEDUCT") == near(136995.0)
    assert a.av_pp_at(0, "BEF_DEDUCT") == near(273990.0)

    assert a.risk_prem_pp(0) == near(0.000080 * 300000.0)
    assert a.gmdb_charge_pp(0) == near(0.0007 / 12.0 * 273990.0)
    assert a.gmab_charge_asset_pp(0) == near(0.0025 / 12.0 * 273990.0)
    assert a.gmab_charge_prem_pp(0) == near(0.0030 / 12.0 * 36000000.0)
    assert a.mth_deduct_pp(0) == near(9097.0640000000)

    assert a.av_pp_at(0, "AFT_DEDUCT") == near(264892.9360000000)
    assert a.fund_pp_at(0, 1, "AFT_DEDUCT") == near(132446.4680000000)
    assert a.fund_pp_at(0, 2, "AFT_DEDUCT") == near(132446.4680000000)
    assert a.derisk_amount_pp(0) == 0.0
    assert a.av_pp_at(0, "AFT_DERISK") == near(a.av_pp_at(0, "AFT_DEDUCT"))

    assert a.fund_growth(1) == near(1.0021321143490463)
    assert a.fund_growth(2) == near(1.0019650366374175)
    assert a.fund_pp(0, 1) == near(132728.8590149033)
    assert a.fund_pp(0, 2) == near(132706.7301621166)
    assert a.av_pp(0) == near(265435.5891770198)
    assert a.inv_income_pp(0) == near(653.2974409536)
    assert a.mgmt_fee_pp(0) == near(110.6442639337)
    assert a.av_pp_at(0, "AFT_DERISK") + a.inv_income_pp(0) - a.mgmt_fee_pp(0) == (
        pytest.approx(a.av_pp(0), abs=1e-8))


def test_worked_example_month_zero_decrements_benefits_and_boundary(kr_va_anchor):
    """The rest of the month-0 trace, and the notes' reading of the account boundary.

    ``d(0)`` is struck on the opening count and ``s(0)`` on the survivors of it; the
    benefits are struck on the **end-of-month** account.  The 일반계정 received ₩300,000,
    kept ₩26,010, sent ₩273,990 across and took back ₩9,207.71; the two ledgers sum to
    the whole-contract external cash flow and nothing else.
    """
    a = kr_va_anchor
    assert a.mort_rate(0) == near(0.0011138523)
    assert a.mort_rate_mth(0) == near(9.286844533373806e-05)
    assert a.pols_death(0) == near(9.286844533373806e-05)
    assert a.lapse_rate(0) == near(0.28)
    assert a.lapse_rate_mth(0) == near(0.027004030272665847)
    assert a.pols_lapse(0) == near(0.02700152245035668)
    assert a.pols_if(1) == near(0.9729056091043096)

    assert a.prem_paid_pp(0) == near(300000.0)
    assert a.db_pp(0) == near(300000.0)
    assert a.cv_pp(0) == 0.0
    assert a.claims(0, "DEATH") == near(27.8605336001)
    assert a.claims(0, "LAPSE") == 0.0
    assert a.expenses(0) == near(303000.0)
    assert a.commissions(0) == near(40200.0)
    assert a.net_cf(0) == near(-43227.8605336001)

    assert a.net_cf_gen(0) == near(-300818.3366588763)
    assert a.net_cf_sep(0) == near(257590.4761252762)
    assert a.net_cf_gen(0) + a.net_cf_sep(0) == pytest.approx(a.net_cf(0), abs=1e-9)
    assert abs(a.check_net_cf_resid(0)) < 1e-9
    assert a.prem_charges(0) == near(26010.0)
    assert a.prem_to_av(0) == near(273990.0)
    assert a.av_charges(0) == near(9097.063999999998 + 110.64426393373063)


def test_worked_example_month_three_trace(kr_va_anchor):
    """The notes' month-3 hand trace: the first month a surrender pays anything.

    The pro-rata share across the funds has drifted off 0.5 by then — the 채권형 carries
    the lower 운용보수 on the same gross return — so this trace catches a deduction spread
    equally instead of pro rata.
    """
    a = kr_va_anchor
    assert a.av_pp(2) == near(797726.1281495993)
    assert a.fund_pp(2, 1) == near(398929.0515490024)
    assert a.fund_pp(2, 2) == near(398797.0766005968)

    assert a.prem_to_av_pp(3) == near(273990.0)
    assert a.fund_pp_at(3, 1, "BEF_DEDUCT") == near(535924.0515490024)
    assert a.fund_pp_at(3, 2, "BEF_DEDUCT") == near(535792.0766005968)
    assert a.av_pp_at(3, "BEF_DEDUCT") == near(1071716.1281495993)

    assert a.risk_prem_pp(3) == near(24.000000000000004)
    assert a.gmdb_charge_pp(3) == near(62.5167741421)
    assert a.gmab_charge_asset_pp(3) == near(223.2741933645)
    assert a.gmab_charge_prem_pp(3) == near(9000.0)
    assert a.mth_deduct_pp(3) == near(9309.7909675066)

    assert a.av_pp_at(3, "AFT_DEDUCT") == near(1062406.3371820927)
    share = a.fund_pp_at(3, 1, "BEF_DEDUCT") / a.av_pp_at(3, "BEF_DEDUCT")
    assert share == near(0.5000615718)
    assert a.fund_pp_at(3, 1, "AFT_DEDUCT") == near(531268.5828448085)
    assert a.fund_pp_at(3, 2, "AFT_DEDUCT") == near(531137.7543372842)
    assert a.fund_pp(3, 1) == near(532401.3082134894)
    assert a.fund_pp(3, 2) == near(532181.4594840726)
    assert a.av_pp(3) == near(1064582.7676975620)

    assert a.yrs_completed(3) == 0
    assert a.surr_chg_pp(3) == near(830000.0001599999)
    assert a.cv_pp(3) == near(234582.7675375621)
    assert a.cv_pp(2) == 0.0

    assert a.pols_if(3) == near(0.9208992552115434)
    assert a.pols_death(3) == near(8.552248214049331e-05)
    assert a.pols_lapse(3) == near(0.024865681914111235)
    assert a.premiums(3) == near(276269.7765634630)
    assert a.claims(3, "DEATH") == near(102.6269785686)
    assert a.claims(3, "LAPSE") == near(5833.0604801209)
    assert a.expenses(3) == near(2762.6977656346)
    assert a.commissions(3) == near(37020.1500595040)
    assert a.net_cf(3) == near(230551.2412796349)


def test_the_gmdb_is_in_the_money_by_construction_at_short_durations(kr_va_anchor):
    """In the money at every month to t = 122; ``gmdb_claim_pp(123)`` is the first zero.

    A return-of-premium GMDB on a 91.33% allocation cannot be out of the money until
    compound return has had a decade to work, so its cost is a **decreasing function of
    duration** rather than a random one.  A model whose GMDB first bites late has almost
    certainly let the front-end charges into the fund.
    """
    a = kr_va_anchor
    assert a.gmdb_claim_pp(3) == near(135417.232302438)
    assert all(a.gmdb_claim_pp(t) > 0.0 for t in range(0, 123))
    assert a.gmdb_claim_pp(123) == 0.0
    assert all(a.gmdb_claim_pp(t) == 0.0 for t in range(123, a.t_ann()))


def test_worked_example_month_120_trace(kr_va_anchor):
    """The notes' 납입완료 trace: the premium stops, the deduction rises 42%, sign flips.

    Three of the five lines of the 월공제액 have changed since month 0 — the age band, the
    계약관리비용 stepping *in*, the premium-based guarantee component having stopped — so
    this is the month at which a fee stack modelled as one charge is furthest from right.
    Month 119 is +₩9,418.79 and month 120 is −₩57,279.86, and every later deferral month
    is negative.
    """
    a = kr_va_anchor
    assert a.av_pp(119) == near(35813337.7735828300)
    assert a.fund_pp(119, 1) == near(17998819.2913504020)
    assert a.fund_pp(119, 2) == near(17814518.4822324300)
    assert a.premium_mth_pp(120) == 0.0
    assert a.prem_to_av_pp(120) == 0.0
    assert a.av_pp_at(120, "BEF_DEDUCT") == near(35813337.7735828300)

    assert a.risk_prem_rate(50) == near(0.000095)
    assert a.risk_prem_pp(120) == near(28.50)
    assert a.maint_charge_after_pp(120) == near(3990.0)
    assert a.gmdb_charge_pp(120) == near(2089.1113701257)
    assert a.gmab_charge_asset_pp(120) == near(7461.1120361631)
    assert a.gmab_charge_prem_pp(120) == 0.0
    assert a.mth_deduct_pp(120) == near(13568.7234062888)
    assert a.mth_deduct_pp(119) == near(9557.2436254184)
    assert a.gmdb_charge_pp(119) == near(2085.3970430603)
    assert a.gmab_charge_asset_pp(119) == near(7447.8465823581)
    assert a.mth_deduct_pp(120) - a.mth_deduct_pp(119) == pytest.approx(4011.48, abs=WON)

    assert a.av_pp_at(120, "AFT_DEDUCT") == near(35799769.0501765460)
    assert a.fund_pp_at(120, 1, "AFT_DEDUCT") == near(17992000.0163041000)
    assert a.fund_pp_at(120, 2, "AFT_DEDUCT") == near(17807769.0338724400)
    assert a.fund_pp(120, 1) == near(18030361.0177069050)
    assert a.fund_pp(120, 2) == near(17842761.9524546680)
    assert a.av_pp(120) == near(35873122.9701615730)

    assert a.prem_paid_pp(120) == near(36000000.0)
    assert a.db_pp(120) == near(36000000.0)
    assert a.gmdb_claim_pp(120) == near(126877.0298384279)
    assert a.surr_chg_pp(120) == 0.0
    assert a.cv_pp(120) == near(a.av_pp(120))
    assert a.claims(120, "DEATH") == near(1641.8340747357)
    assert a.claims(120, "LAPSE") == near(54973.9519946892)
    assert a.expenses(120) == near(664.0754971924)
    assert a.commissions(120) == 0.0
    assert a.net_cf(120) == near(-57279.8615666174)

    assert a.net_cf(119) == near(9418.788455924689)
    assert all(a.net_cf(t) < 0.0 for t in range(120, a.t_ann()))
    assert a.net_cf_gen(120) == near(5640.336569994052)
    assert a.net_cf_sep(120) == near(-62920.198136611405)
    paid_up = [a.net_cf(t) for t in range(120, a.t_ann())]
    assert min(paid_up) == near(-57279.8615666174)
    assert max(paid_up) == near(-30476.219155346327)


def test_worked_example_month_204_derisking_trace(kr_va_anchor):
    """The notes' de-risking trace at t = T − 36, and its two visible consequences.

    ₩12,113,087.24 moves into the 채권형 and the total is unchanged; the 운용보수 falls
    11.6% in one month with no change in the account, and the weight then stays above 80%
    on its own, so the two later windows do not fire.
    """
    a = kr_va_anchor
    assert a.bond_weight(203) == near(0.5060742578243943)
    assert a.av_pp_at(204, "AFT_DEDUCT") == near(41211386.0778102300)
    assert a.fund_pp_at(204, 1, "AFT_DEDUCT") == near(20856021.6232423860)
    assert a.fund_pp_at(204, 2, "AFT_DEDUCT") == near(20355364.4545678000)
    assert a.derisk_amount_pp(204) == near(12113087.239005797)
    assert a.derisk_amount_pp(204) == pytest.approx(
        0.80 * a.av_pp_at(204, "AFT_DEDUCT") - a.fund_pp_at(204, 1, "AFT_DEDUCT"),
        abs=1e-6)
    assert a.fund_pp_at(204, 1, "AFT_DERISK") == near(32969108.8622481820)
    assert a.fund_pp_at(204, 2, "AFT_DERISK") == near(8242277.2155620450)
    assert a.av_pp_at(204, "AFT_DERISK") == pytest.approx(
        a.av_pp_at(204, "AFT_DEDUCT"), abs=1e-6)
    assert a.mgmt_fee_pp(203) == near(17143.341517276796)
    assert a.mgmt_fee_pp(204) == near(15148.108973641843)
    assert a.mgmt_fee_pp(204) / a.mgmt_fee_pp(203) == pytest.approx(0.884, abs=5e-4)
    assert a.derisk_amount_pp(216) == 0.0
    assert a.derisk_amount_pp(228) == 0.0
    assert all(a.bond_weight(t) > 0.80 for t in range(204, a.t_ann()))


@pytest.mark.parametrize("t", sorted(EVENT_ROWS))
def test_every_event_row_of_the_statement(kr_va_anchor, t):
    """The notes' seventeen-row event table — every row where the product does something.

    Issue, the surrender-value floor releasing, the commission step, the guarantee charge
    stopping, 납입완료, the de-risking, 연금개시, the end of the 보증기간 and the horizon.
    Each is a boundary the model crosses exactly once, so a row that has moved by a month
    is a boundary condition written the wrong way round.
    """
    pols, prem, death, lapse, annuity, exp, comm, net = EVENT_ROWS[t]
    a = kr_va_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=WON)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=WON)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=WON)
    assert a.claims(t, "ANNUITY") == pytest.approx(annuity, abs=WON)
    assert a.expenses(t) == pytest.approx(exp, abs=WON)
    assert a.commissions(t) == pytest.approx(comm, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)


def test_the_commission_step_at_the_first_anniversary(kr_va_anchor):
    """₩29,716.92 to ₩8,846.14 at t = 12 — a factor of 3.36 on a 2.7% fall in force.

    Essentially the whole of the step is the commission scale and not the in-force count,
    which is what makes it a test of ``comm_rate`` rather than of the decrements.
    """
    a = kr_va_anchor
    assert a.commissions(11) / a.commissions(12) == pytest.approx(3.36, abs=0.005)
    assert a.pols_if(12) / a.pols_if(11) == pytest.approx(0.9729, abs=5e-5)
    assert a.commissions(0) == near(0.0134 / 12.0 * 36000000.0)
    assert a.comm_rate(1) == near(0.0134) and a.comm_rate(2) == near(0.0041)


def test_the_two_guarantees_at_annuitisation(kr_va_anchor):
    """The notes' table at t_ann() = 240, every line of it.

    Four one-off scalars are struck here and never move again.  The GMAB finishes out of
    the money on this path, so its intrinsic cost is exactly zero while the full charge was
    collected — a single-path residual, which this test does not quietly turn into profit.
    """
    a = kr_va_anchor
    assert a.av_ann_pp() == near(AV_ANN_PP)
    assert a.av_ann_pp() == near(a.av_pp(a.t_ann() - 1))
    assert a.gmab_base_pp() == near(36000000.0)
    assert a.gmab_claim_pp() == 0.0
    assert a.annuity_fund_pp() == near(AV_ANN_PP)
    assert a.annuity_int_rate() == near(0.025)
    assert a.annuity_factor() == near(ANNUITY_FACTOR)
    assert a.annuity_ann_pp() == near(2178961.6079652957)
    assert a.annuity_charge_pp() == near(10894.80803982648)
    assert a.annuity_net_pp() == near(ANNUITY_NET_PP)
    assert a.pols_annuitised() == near(POLS_ANNUITISED)
    assert a.claims(240, "ANNUITY") == near(200728.5776812762)
    assert a.annuity_ann_pp() == pytest.approx(
        a.annuity_fund_pp() / a.annuity_factor(), rel=1e-14)
    assert a.annuity_net_pp() == pytest.approx(
        a.annuity_ann_pp() * (1.0 - 0.005), rel=1e-14)
    assert a.claims(240, "ANNUITY") == pytest.approx(
        a.annuity_net_pp() * a.pols_annuitised(), rel=1e-14)
    # Only 9.26% of contracts reach it: a 90.7% exit probability before the strike date.
    assert a.pols_annuitised() == pytest.approx(0.0926, abs=5e-5)


def test_annuitisation_empties_the_separate_account_in_one_movement(kr_va_anchor):
    """₩4,062,956.72 crosses 특별계정 → 일반계정 at t = 240 and the fund is empty after.

    ``net_cf_sep(240)`` is exactly the transfer and ``net_cf_gen(240)`` the same amount
    less the instalment and the month's expense: the account-boundary reading of the hinge
    between the product's two halves.
    """
    a = kr_va_anchor
    assert a.av_transfer(240) == near(4062956.72108272)
    assert a.net_cf_sep(240) == near(-4062956.72108272)
    assert a.net_cf_gen(240) == near(3861950.3910125117)
    assert a.av_pp(239) == near(AV_ANN_PP)
    assert all(a.av_pp(t) == 0.0 for t in (240, 300, 600, 959))
    assert all(a.fund_pp(240, j) == 0.0 for j in a.fund_ids())
    assert all(a.net_cf_sep(t) == 0.0 for t in (241, 300, 600, 959))


def test_the_guarantee_period_step_at_t_360(kr_va_anchor):
    """₩200,728.58 to ₩186,188.58 — a 7.24% step, and the annuity did not change.

    ``annuity_net_pp()`` is the same ₩2,168,066.80 either side; only the weight changed,
    from every contract that annuitised to the ones whose annuitant is still alive.  Ten
    years of annuitant mortality at 보험나이 60–70 is the whole of the step.
    """
    a = kr_va_anchor
    assert a.claims(348, "ANNUITY") == pytest.approx(200728.58, abs=WON)
    assert a.claims(360, "ANNUITY") == pytest.approx(186188.58, abs=WON)
    assert a.annuity_net_pp() == near(ANNUITY_NET_PP)
    step = 1.0 - a.claims(360, "ANNUITY") / a.claims(348, "ANNUITY")
    assert step == pytest.approx(0.0724, abs=5e-5)
    assert a.pols_annuity_oblig(348) == near(a.pols_annuitised())
    assert a.pols_annuity_oblig(360) == near(a.pols_if(360))
    assert a.pols_if(360) == near(0.08587769374658065)
    assert a.guar_period_years == 10


def test_worked_example_undiscounted_totals(kr_va_anchor):
    """The notes' undiscounted totals over t = 0 … 959, column by column.

    Four carry the economics: ``premiums`` is 42.26% of the contractual ₩36,000,000
    because most of the premium stream never arrives; ``claims_lapse`` is 72.8% of what
    does; ``Σ pols_if`` of 99.61 contract-months against a 960-month projection is the same
    persistency fact a third way; and the first twelve months sum to +₩2,104,181.53 with
    only month 0 negative.
    """
    a = kr_va_anchor
    df = a.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert df["premiums"].sum() / a.prem_total_pp() == pytest.approx(0.4226, abs=5e-5)
    assert df["claims_lapse"].sum() / df["premiums"].sum() == pytest.approx(
        0.728, abs=5e-4)
    assert df["net_cf"].sum() < 0.0
    assert a.expenses(0) / df["expenses"].sum() > 0.5
    assert df["net_cf"].iloc[0:12].sum() == pytest.approx(FIRST_TWELVE_NET_CF, abs=WON)
    assert a.net_cf(0) < 0.0
    assert all(a.net_cf(t) > 0.0 for t in range(1, 120))
    # The unweighted commission is the sum of the five shipped rates, 2.39%.
    assert df["commissions"].sum() / (0.0239 * 36000000.0) == pytest.approx(
        0.718, abs=5e-4)


def test_worked_example_guarantee_memo_totals(kr_va_anchor):
    """The four guarantee memo lines, and the fact that they are memos.

    ₩657,417.59 of GMAB charge against ₩0.00 of intrinsic cost, and ₩79,244.38 of GMDB
    charge against ₩4,945.39.  Neither difference is a profit and neither number is a
    valuation: on one path this is intrinsic value, a **lower bound** on expected cost.
    """
    a = kr_va_anchor
    ts = range(0, a.proj_len())
    got = {"gmdb_charges": sum(a.gmdb_charges(t) for t in ts),
           "gmdb_claims": sum(a.gmdb_claims(t) for t in ts),
           "gmab_charges": sum(a.gmab_charges(t) for t in ts),
           "gmab_claims": sum(a.gmab_claims(t) for t in ts)}
    for name, total in MEMOS.items():
        assert got[name] == pytest.approx(total, abs=WON), name
        assert name not in a.result_cf().columns
    assert sum(a.surr_charges(t) for t in ts) == pytest.approx(
        SURR_CHARGES_TOTAL, abs=WON)


@pytest.mark.parametrize("point_id", sorted(CONTRASTS))
def test_contrasts_across_model_points(variable_annuity, point_id):
    """The notes' five-row contrast table: which lever moves what.

    Sex moves the annuity factor and not the account; the 미보증형 moves both by 6.47%;
    the return path moves the terminal account by a factor of two and is the only thing
    that decides whether the GMAB pays at all.
    """
    av, claim, annuity, total = CONTRASTS[point_id]
    p = variable_annuity.Projection[point_id]
    assert p.av_ann_pp() == pytest.approx(av, abs=5e-5)
    assert p.annuity_net_pp() == pytest.approx(annuity, abs=5e-5)
    if claim is not None:
        assert p.gmab_claim_pp() == pytest.approx(claim, abs=5e-5)
    if total is not None:
        assert p.result_cf()["net_cf"].sum() == pytest.approx(total, abs=0.05)


def test_the_sex_effect_lands_entirely_at_annuitisation(variable_annuity):
    """Points 1 and 2 have the same account value to the last digit; the factor differs.

    The 계약자적립액 is a per-contract quantity, so mortality enters only through the
    *counts* and through the *annuity factor*: 20.1398 against 21.7622, so the same
    ₩43,883,943.57 buys 7.45% less annual income.
    """
    male, female = variable_annuity.Projection[1], variable_annuity.Projection[2]
    for t in (0, 3, 120, 239):
        assert female.av_pp(t) == pytest.approx(male.av_pp(t), rel=1e-15)
    assert female.av_ann_pp() == pytest.approx(male.av_ann_pp(), rel=1e-15)
    assert male.annuity_factor() == near(ANNUITY_FACTOR)
    assert female.annuity_factor() == near(ANNUITY_FACTOR_FEMALE)
    assert 1.0 - female.annuity_net_pp() / male.annuity_net_pp() == pytest.approx(
        0.0745, abs=5e-5)
    assert female.pols_annuitised() > male.pols_annuitised()


def test_the_guarantee_costs_the_policyholder_six_and_a_half_percent(variable_annuity):
    """Point 3, the 미보증형: removing the GMAB raises the account by ₩2,838,935.66.

    0.25% a year of the fund plus 0.30% a year of ₩36,000,000 for seven years is 6.47% of
    the terminal account after twenty years, and the annuity rises by the same 6.47%
    because nothing else about the contract changed.
    """
    on, off = variable_annuity.Projection[1], variable_annuity.Projection[3]
    assert off.gmab_flag() == 0
    assert off.gmab_charge_asset_pp(0) == 0.0
    assert off.gmab_charge_prem_pp(0) == 0.0
    assert off.gmab_claim_pp() == 0.0
    gap = off.av_ann_pp() - on.av_ann_pp()
    assert gap == pytest.approx(2838935.66, abs=WON)
    assert gap / on.av_ann_pp() == pytest.approx(0.0647, abs=5e-5)
    assert off.annuity_net_pp() / on.annuity_net_pp() - 1.0 == pytest.approx(
        0.0647, abs=5e-5)


# ---------------------------------------------------------------------------
# The product's own invariants, recursions and boundaries


def test_eight_check_cells_are_published_each_with_its_residual(variable_annuity):
    """The eight identities this model publishes, asserted **by name**.

    That they are *true*, on all ten points, is asserted in
    ``test_model_conventions_kr.py``: its sweep discovers every ``check_*`` generically and
    calls it on every model point of every model in the library.  Generic discovery cannot
    notice a check that has **gone** — it simply stops being discovered — so naming the set
    is the statement left here.
    """
    cells = set(variable_annuity.Projection.cells)
    checks = {c for c in cells
              if c.startswith("check_") and not c.endswith("_resid")}
    assert checks == CHECK_CELLS
    anchor = variable_annuity.Projection[1]
    for name in sorted(checks):
        assert name + "_resid" in cells, name
        assert getattr(anchor, name)() is True, name


def test_the_account_boundary_identity_closes_at_every_month(kr_va_anchor):
    """``net_cf = net_cf_gen + net_cf_sep``, at every one of the 960 months.

    Every transfer 감독규정 제5-7조 permits between the two accounts appears in the two
    ledgers with opposite signs, so their sum must be the whole-contract external cash flow
    and nothing else.  An internal transfer that leaked into ``net_cf`` — the 월공제액
    counted as income, say — would show up here and nowhere else in the statement.
    """
    a = kr_va_anchor
    assert a.check_net_cf() is True
    for t in (0, 3, 84, 120, 204, 239, 240, 360, 959):
        scale = max(1.0, abs(a.net_cf_gen(t)) + abs(a.net_cf_sep(t)))
        assert abs(a.check_net_cf_resid(t)) <= 1e-8 * scale
        assert a.net_cf_gen(t) + a.net_cf_sep(t) == pytest.approx(a.net_cf(t), abs=1e-6)


def test_the_in_force_roll_forward_closes_and_every_contract_leaves(kr_va_anchor):
    """``l(t) − l(t+1) = d(t) + s(t) + pols_maturity(t)``, and the counts sum to one.

    ``pols_maturity`` pays nothing — a 종신연금형 has no maturity — and exists so that the
    survivors at the horizon leave through a modelled decrement instead of being absorbed
    into the last row.  Without it the roll-forward would close only by accident.
    """
    a = kr_va_anchor
    assert a.check_pols_roll_fwd() is True
    for t in (0, 3, 120, 239, 240, 958, 959):
        assert abs(a.check_pols_roll_fwd_resid(t)) < 1e-10
    ts = range(0, a.proj_len())
    deaths = sum(a.pols_death(t) for t in ts)
    lapses = sum(a.pols_lapse(t) for t in ts)
    horizon = sum(a.pols_maturity(t) for t in ts)
    assert deaths == pytest.approx(0.10410284631497578, abs=INFORCE)
    assert lapses == pytest.approx(0.8958970712349685, abs=INFORCE)
    assert horizon == pytest.approx(8.245005547570906e-08, abs=INFORCE)
    assert deaths + lapses + horizon == pytest.approx(1.0, abs=1e-10)
    assert a.pols_if(a.proj_len()) == 0.0
    assert a.pols_maturity(a.proj_len() - 2) == 0.0   # the month before the horizon, t = 958


def test_the_account_recursion_closes_at_every_month(kr_va_anchor):
    """AV(t) = AV(t−1) + 투입보험료 − 월공제액 − 인출 + I(t) − M(t) − the 연금재원 transfer.

    The de-risking does not appear in the identity because it conserves the total: it moves
    money between funds and not out of the account, so a de-risking written as a net
    transfer rather than a reallocation breaks this and nothing else.

    ``t = 0`` is included: its opening balance is nil, and it is the row that carries the
    single premium, the 계약체결비용 and the whole first month's charge stack.
    """
    a = kr_va_anchor
    assert a.check_av_roll_fwd() is True
    for t in (0, 1, 3, 84, 120, 204, 216, 239, 240):
        assert abs(a.check_av_roll_fwd_resid(t)) <= 1e-8 * max(1.0, abs(a.av_pp(t)))
    for t in (0, 1, 3, 120, 204):
        opening = a.av_pp(t - 1) if t > 0 else 0.0
        expected = (opening + a.prem_to_av_pp(t) - a.mth_deduct_pp(t)
                    - a.wd_pp(t) + a.inv_income_pp(t) - a.mgmt_fee_pp(t))
        assert a.av_pp(t) == pytest.approx(expected, abs=1e-6)
    assert a.av_pp(240) == 0.0
    assert abs(a.check_av_roll_fwd_resid(240)) < 1e-6


def test_the_separate_account_investment_identity_separates_four_bases(kr_va_anchor):
    """``I(t) − M(t) = AV(t) − AV(t, AFT_DERISK)``, at every month of the deferral.

    The guard against the charge-base confusion the product is most often modelled wrong
    at.  Four bases sit in one stack: the 운용보수 is inside the 기준가격, the 월공제액
    cancels units, the 계약체결비용 never enters the fund at all, and the premium component
    of the GMAB charge is on a base that is not the fund.
    """
    a = kr_va_anchor
    assert a.check_charge_split() is True
    for t in (0, 3, 84, 120, 204, 239):
        lhs = a.inv_income_pp(t) - a.mgmt_fee_pp(t)
        assert lhs == pytest.approx(a.av_pp(t) - a.av_pp_at(t, "AFT_DERISK"), abs=1e-6)
        assert abs(a.check_charge_split_resid(t)) <= 1e-8 * max(1.0, abs(a.av_pp(t)))
    # Vacuous after annuitisation, and it says so rather than being skipped.
    assert a.check_charge_split_resid(240) == 0.0


def test_the_processing_order_is_asserted_by_a_quantity_that_would_move(kr_va_anchor):
    """Five of the notes' twelve processing steps, each caught by an order-sensitive value.

    Order is not presentational here.  The asset-based guarantee charges are struck on the
    account **after** the premium goes in, the deduction is spread **pro rata** and not
    equally, the de-risking happens **before** the growth, the decrements take death first,
    and the benefits are struck on the **end-of-month** account.  Each assertion compares
    the model against the value the wrong order would give.
    """
    a = kr_va_anchor
    # 3 then 4: the charge base includes the month's transfer.
    assert a.av_pp_at(0, "BEF_PREM") == 0.0
    assert a.gmdb_charge_pp(0) > 0.0
    assert a.gmdb_charge_pp(0) == near(0.0007 / 12.0 * 273990.0)
    # 4: pro rata, not equal — the shares have drifted off 0.5 by t = 3.
    share = a.fund_pp_at(3, 1, "BEF_DEDUCT") / a.av_pp_at(3, "BEF_DEDUCT")
    assert share != pytest.approx(0.5, abs=1e-9)
    assert a.fund_pp_at(3, 1, "AFT_DEDUCT") == pytest.approx(
        a.fund_pp_at(3, 1, "BEF_DEDUCT") - a.mth_deduct_pp(3) * share, abs=1e-6)
    # 7 then 8: de-risking before growth, so the month's growth is on the new mix.
    grown_without = sum(a.fund_pp_at(204, j, "AFT_DEDUCT") * a.fund_growth(j)
                        for j in a.fund_ids())
    assert a.av_pp(204) != pytest.approx(grown_without, abs=1.0)
    assert a.av_pp(204) == pytest.approx(
        sum(a.fund_pp_at(204, j, "AFT_DERISK") * a.fund_growth(j)
            for j in a.fund_ids()), abs=1e-6)
    # 9: death first, 해지 on the survivors of it.
    for t in (0, 3, 120):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) - a.pols_death(t), rel=1e-15)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate_mth(t), rel=1e-14)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(a.pols_if(t + 1), abs=1e-15)
    # 10: benefits on the end-of-month account, after growth.
    assert a.db_pp(200) == pytest.approx(a.av_pp(200), rel=1e-15)
    assert a.db_pp(200) != pytest.approx(a.av_pp_at(200, "AFT_DEDUCT"), rel=1e-9)


def test_the_published_columns_sum_to_net_cf_on_every_shipped_point(variable_annuity):
    """income − outgo = ``net_cf``, column by column, on all ten model points.

    A benefit kind added to ``claims`` and left out of the statement would vanish silently
    without this.  It also fixes the sign convention: ``net_cf`` is income-positive and
    every other column is a gross flow.
    """
    outgo_cols = ["claims_death", "claims_lapse", "claims_annuity", "claims_maturity",
                  "withdrawals", "fund_expenses", "expenses", "commissions"]
    for point_id in variable_annuity.Data.model_point_table().index:
        p = variable_annuity.Projection[point_id]
        df = p.result_cf()
        assert list(df.columns)[0] == "pols_if"
        assert df.index.name == "t"
        assert len(df) == p.proj_len()
        assert df.notna().all().all()
        outgo = df[outgo_cols].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-8), point_id


def test_the_boundaries_of_every_charge_line(kr_va_anchor):
    """Each of the seven charge lines starts and stops where its own rule says.

    Five stopping rules run in one stack: ten years or the 납입기간 for the 계약체결비용,
    the 납입기간 for the 계약관리비용 inside it and for the 위험보험료, seven years or the
    납입기간 for the GMAB premium component, 납입완료 for the 계약관리비용 after it, and
    연금개시 for everything.  A month wrong on any of them is invisible in a total.
    """
    a = kr_va_anchor
    assert a.acq_charge_pp(119) == near(15510.0) and a.acq_charge_pp(120) == 0.0
    assert a.maint_charge_in_pp(119) == near(10500.0)
    assert a.maint_charge_in_pp(120) == 0.0
    assert a.maint_charge_after_pp(119) == 0.0
    assert a.maint_charge_after_pp(120) == near(3990.0)
    assert a.maint_charge_after_pp(239) == near(3990.0)
    assert a.maint_charge_after_pp(240) == 0.0
    assert a.gmab_charge_prem_pp(83) == near(9000.0)
    assert a.gmab_charge_prem_pp(84) == 0.0
    assert a.risk_prem_pp(239) > 0.0 and a.risk_prem_pp(240) == 0.0
    assert a.gmdb_charge_pp(239) > 0.0 and a.gmdb_charge_pp(240) == 0.0
    assert a.gmab_charge_asset_pp(239) > 0.0 and a.gmab_charge_asset_pp(240) == 0.0
    assert a.mgmt_fee_pp(239) > 0.0 and a.mgmt_fee_pp(240) == 0.0
    assert a.mth_deduct_pp(239) > 0.0 and a.mth_deduct_pp(240) == 0.0
    # 해약공제기간 is seven completed policy years, so the last charged month is t = 82.
    assert a.yrs_completed(82) == 6 and a.yrs_completed(83) == 7
    assert a.surr_chg_pp(82) > 0.0 and a.surr_chg_pp(83) == 0.0
    assert a.surr_chg_years == 7


def test_the_withdrawal_module_is_off_on_the_anchor_and_bounded_when_on(
        variable_annuity):
    """Point 9 takes 10% of the 해약환급금 once a year from the eleventh anniversary.

    Every published limit is applied: at most 50% of the 해약환급금, a residual 계약자적립액
    of at least ₩5,000,000 per 구좌, and cumulative withdrawals inside the first ten years
    no greater than the premiums actually paid — the last a tax rule showing through into
    the policy conditions.
    """
    anchor = variable_annuity.Projection[1]
    assert anchor.wd_ratio() == 0.0
    assert all(anchor.wd_pp(t) == 0.0 for t in (0, 12, 132, 239))
    assert anchor.result_cf()["withdrawals"].sum() == 0.0

    p = variable_annuity.Projection[9]
    assert (p.wd_ratio(), p.wd_start_year()) == (0.1, 11)
    assert (p.wd_max_cv_ratio, p.wd_min_residual_pp, p.wd_cum_cap_years) == (
        0.5, 5000000.0, 10)
    first = 12 * p.wd_start_year()
    assert p.wd_pp(first - 12) == 0.0        # nothing before the eleventh anniversary
    assert p.wd_pp(first + 1) == 0.0         # and nothing in a non-anniversary month
    assert p.wd_pp(first) > 0.0
    base = p.av_pp_at(first, "BEF_DEDUCT") - p.mth_deduct_pp(first)
    assert p.surr_chg_pp(first) == 0.0
    assert p.wd_pp(first) == pytest.approx(0.1 * base, abs=1e-6)
    assert p.wd_pp(first) <= p.wd_max_cv_ratio * base
    for t in range(first, p.t_ann(), 12):
        assert p.av_pp_at(t, "BEF_DEDUCT") - p.mth_deduct_pp(t) - p.wd_pp(t) >= (
            p.wd_min_residual_pp - 1e-6)
    assert p.wd_cum_pp(p.t_ann() - 1) == pytest.approx(
        sum(p.wd_pp(t) for t in range(0, p.t_ann())), abs=1e-6)


def test_the_additional_premium_module_is_off_on_the_anchor_and_uncapped_on_point_8(
        variable_annuity):
    """추가납입 carries no loading, doubles the strike, and does not reach its 200% cap.

    Point 8 accumulates ₩36,000,000 of additional premium against a cap of ₩72,000,000, so
    the closed form ``gmab_prem_base_pp`` uses is exact there; the notes state that
    limitation rather than leaving it to be discovered, and this test pins the margin.
    """
    anchor = variable_annuity.Projection[1]
    assert anchor.addl_prem_ratio() == 0.0
    assert all(anchor.addl_prem_pp(t) == 0.0 for t in (0, 60, 119))

    p = variable_annuity.Projection[8]
    assert p.addl_prem_ratio() == 1.0 and p.addl_prem_cap_ratio == 2.0
    assert p.addl_prem_pp(0) == near(300000.0)
    assert p.prem_pp(0) == near(600000.0)
    # No loading on the additional premium: it enters the fund in full.
    assert p.prem_to_av_pp(0) == near(573990.0)
    assert p.prem_alloc_ratio(0) == near(0.9133)
    assert p.check_prem_alloc() is True
    paid = sum(p.addl_prem_pp(t) for t in range(0, p.t_ann()))
    assert paid == near(36000000.0)
    assert paid < p.addl_prem_cap_ratio * p.prem_total_pp()
    assert p.addl_prem_pp(p.pay_months()) == 0.0
    # The charge base grows with 추가납입; the strike grows further and for longer.
    assert p.gmab_prem_base_pp(0) == near(36000000.0)
    assert p.gmab_prem_base_pp(83) == near(60900000.0)
    assert p.gmab_prem_base_pp(120) == near(72000000.0)
    assert p.gmab_charge_prem_pp(83) == near(0.0030 / 12.0 * 60900000.0)
    assert p.gmab_charge_prem_pp(84) == 0.0
    assert p.gmab_base_pp() == near(72000000.0)


def test_the_minimum_guaranteed_crediting_ladder_is_inert_on_the_anchor(
        variable_annuity):
    """1.00% / 0.75% / 0.50% by elapsed duration, never binding at a 2.50% 공시이율.

    Point 10 runs the ``min_guar`` basis, where the declared rate is zero and the floor is
    the whole of the credited rate — the configuration in which the ladder is the contract
    rather than a decoration, and the one that strikes the annuity at 1.00%.
    """
    a = variable_annuity.Projection[1]
    for k, floor in ((0, 0.0100), (5, 0.0075), (10, 0.0050), (20, 0.0050)):
        assert a.min_guar_rate(k) == near(floor)
        assert a.decl_rate(k) == near(0.025)
        assert a.credit_rate(k) == near(0.025)
    assert a.annuity_int_rate() == near(0.025)

    p = variable_annuity.Projection[10]
    assert p.crediting_basis() == "min_guar"
    assert p.decl_rate(0) == 0.0
    assert p.credit_rate(0) == near(0.0100)
    assert p.credit_rate(10) == near(0.0050)
    assert p.annuity_int_rate() == near(0.0100)


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test per pitfall, named after it


def test_pitfall_the_gmab_charge_has_two_components_on_two_bases(kr_va_anchor):
    """Pitfall 1: putting the guarantee charges on the account value.

    0.25% a year of the 계약자적립액 and 0.30% a year of the **보험료총액** are ₩57.08 and
    ₩9,000.00 at t = 0 — a factor of 158.  Collapsing them onto the fund understates
    month-0 charge income by ₩8,942.92 per contract.
    """
    a = kr_va_anchor
    assert a.gmab_charge_asset_pp(0) == near(57.081250000000004)
    assert a.gmab_charge_prem_pp(0) == near(9000.0)
    assert a.gmab_charge_prem_pp(0) / a.gmab_charge_asset_pp(0) == pytest.approx(
        158.0, abs=0.5)
    assert a.gmab_charge_prem_pp(0) - a.gmab_charge_asset_pp(0) == pytest.approx(
        8942.92, abs=WON)
    assert a.gmab_prem_base_pp(0) == near(a.prem_total_pp())
    assert a.gmab_prem_base_pp(0) != pytest.approx(a.av_pp_at(0, "BEF_DEDUCT"), rel=1e-3)
    assert a.gmab_charge_asset_pp(0) == near(
        0.0025 / 12.0 * a.av_pp_at(0, "BEF_DEDUCT"))
    assert a.gmab_charge_prem_pp(0) == near(0.0030 / 12.0 * a.gmab_prem_base_pp(0))


def test_pitfall_the_premium_based_component_stops_at_seven_years(kr_va_anchor):
    """Pitfall 2: running the premium-based guarantee charge for the whole premium term.

    It is levied 「납입기간(최대 7년) 동안」 — the *shorter* of the two.  On a 10년납
    contract it stops at t = 84, three years before the premiums do, and the 월공제액 falls
    57.8% in that one month, from ₩15,422.57 to ₩6,504.62.  Running it to t = 120 adds
    ₩324,000 of undiscounted charge the contract does not permit.
    """
    a = kr_va_anchor
    assert a.gmab_charge_years == 7
    assert all(a.gmab_charge_prem_pp(t) == near(9000.0) for t in range(0, 84))
    assert all(a.gmab_charge_prem_pp(t) == 0.0 for t in range(84, a.t_ann()))
    assert sum(9000.0 for _ in range(84, a.pay_months())) == near(324000.0)
    assert a.mth_deduct_pp(83) == near(15422.567687796552)
    assert a.mth_deduct_pp(84) == near(6504.620390932641)
    assert a.mth_deduct_pp(84) / a.mth_deduct_pp(83) == pytest.approx(0.4218, abs=5e-4)
    # Nothing else changes across the month, and the premium runs on for three years.
    assert a.gmab_charge_asset_pp(84) > a.gmab_charge_asset_pp(83)
    assert a.gmdb_charge_pp(84) > a.gmdb_charge_pp(83)
    assert a.premium_mth_pp(84) == near(300000.0)
    assert a.premium_mth_pp(119) == near(300000.0)


def test_pitfall_the_monthly_deduction_rises_at_paid_up(kr_va_anchor):
    """Pitfall 3: expecting the monthly deduction to fall at 납입완료.

    It **rises**, from ₩9,557.24 at t = 119 to ₩13,568.72 at t = 120, because the
    계약관리비용 for the period after 납입완료 was collected inside the premium and is now
    drawn out of the fund.  A model that stops all charges when premiums stop overstates
    the account by roughly ₩4,000 a month for the remaining ten years.
    """
    a = kr_va_anchor
    assert a.mth_deduct_pp(120) > a.mth_deduct_pp(119)
    assert a.mth_deduct_pp(119) == near(9557.2436254184)
    assert a.mth_deduct_pp(120) == near(13568.7234062888)
    assert a.maint_charge_after_pp(119) == 0.0
    assert a.maint_charge_after_pp(120) == near(3990.0)
    assert a.charge_rate("maint_charge_after") == near(0.0133)
    # The money it draws back was put in during the premium period, by construction: the
    # 특별계정 투입보험료 is the 순보험료 plus the 납입 후 계약관리비용.
    assert a.prem_to_av_pp(0) > a.basic_prem_pp() * (
        1.0 - a.loading_rate() - a.charge_rate("maint_charge_after"))


def test_pitfall_the_front_end_charges_never_reach_the_separate_account(kr_va_anchor):
    """Pitfall 4: letting the front-end charges reach the 특별계정.

    계약체결비용, 납입 중 계약관리비용 and 기타비용 are deducted from the premium **in the
    일반계정**; only the 월공제액 and the 운용보수 come out of the account.  Conflating the
    two deduction points either double-charges the fund or gives it ₩26,010 a month it
    never receives.  The observable is the allocation ratio: 0.9133.
    """
    a = kr_va_anchor
    assert a.check_prem_alloc() is True
    for t in (0, 12, 84, 119):
        assert a.check_prem_alloc_resid(t) == pytest.approx(0.0, abs=1e-8)
        assert a.prem_alloc_ratio(t) == near(0.9133)
    assert a.prem_alloc_ratio(120) == 0.0     # no premium, so no ratio
    assert a.prem_to_av_pp(0) == near(a.basic_prem_pp() - a.prem_charge_pp(0))
    assert a.prem_charges(0) == near(26010.0)
    assert a.av_charges(0) == near(a.mth_deduct_pp(0) + a.mgmt_fee_pp(0))
    assert a.mth_deduct_pp(0) < a.prem_charge_pp(0)
    # 91.3% / 91.3% / 91.4% is what three carriers publish on this cell.
    assert 0.913 <= a.prem_alloc_ratio(0) <= 0.915
    assert a.acq_charge_years == 10 and a.pay_months() == 12 * a.acq_charge_years


def test_pitfall_the_management_fee_is_inside_the_unit_price(kr_va_anchor):
    """Pitfall 5: treating the 운용보수 as a unit cancellation.

    It is deducted inside the 기준가격, out of net assets before the unit price is struck,
    so it is a **factor on the growth** and not a deduction from the account.  Modelled as
    a cancellation it would change the base every other charge is struck on.
    """
    a = kr_va_anchor
    assert a.check_charge_split() is True
    assert a.mgmt_fee_pp(0) == near(110.64426393373063)
    assert a.fund_growth(1) == near(
        (1.03) ** (1 / 12) * (1.0 - a.fund_mgmt_fee(1) / 12.0))
    assert a.fund_growth(2) == near(
        (1.03) ** (1 / 12) * (1.0 - a.fund_mgmt_fee(2) / 12.0))
    # The fee is not part of the 월공제액 and is not subtracted before the growth.
    assert a.mth_deduct_pp(0) == near(
        a.risk_prem_pp(0) + a.gmdb_charge_pp(0) + a.gmab_charge_pp(0))
    cancelled = (a.av_pp_at(0, "AFT_DERISK") - a.mgmt_fee_pp(0)) * (1.03) ** (1 / 12)
    assert a.av_pp(0) != pytest.approx(cancelled, abs=1e-6)
    assert a.av_pp(0) == pytest.approx(
        a.av_pp_at(0, "AFT_DERISK") + a.inv_income_pp(0) - a.mgmt_fee_pp(0), abs=1e-8)


def test_pitfall_the_gmab_is_a_european_option_not_a_floor(kr_va_anchor):
    """Pitfall 6: treating the GMAB as a floor on the account at every duration.

    It is a European option struck on one date, void on 해지, on death before T and on
    조기연금개시.  Weighting it by ``pols_if(t)`` at every t rather than by
    ``pols_annuitised()`` at T alone overstates its cost by the whole 90.74%
    pre-annuitisation exit probability — roughly tenfold on this cell.
    """
    a = kr_va_anchor
    assert a.pols_annuitised() == near(POLS_ANNUITISED)
    assert all(a.gmab_claims(t) == 0.0
               for t in range(0, a.proj_len()) if t != a.t_ann())
    assert a.gmab_claims(a.t_ann()) == near(a.gmab_claim_pp() * a.pols_annuitised())
    # The account is never floored at the strike before T: it is free to sit below it.
    assert a.av_pp(0) < a.gmab_base_pp()
    assert a.cv_pp(3) < a.gmab_base_pp()
    assert a.db_pp(3) == near(a.prem_paid_pp(3))     # the GMDB floors, the GMAB does not
    assert 1.0 - a.pols_annuitised() == pytest.approx(0.9074, abs=5e-5)
    assert 1.0 / a.pols_annuitised() == pytest.approx(10.8, abs=0.05)


def test_pitfall_the_gmab_residual_is_not_profit(variable_annuity):
    """Pitfall 7: reading the GMAB residual as profit.

    ₩657,417.59 of charge against ₩0.00 of intrinsic cost on the base path is a single-path
    residual: the option was written and the path finished out of the money.  Point 4, on
    the mandated −1.00% illustration return, is the counter-example — there the charge does
    not cover the guarantee.
    """
    base, low = variable_annuity.Projection[1], variable_annuity.Projection[4]
    assert base.gmab_claim_pp() == 0.0
    assert sum(base.gmab_charges(t) for t in range(0, base.proj_len())) == (
        pytest.approx(657417.59, abs=WON))
    assert sum(base.gmab_claims(t) for t in range(0, base.proj_len())) == 0.0

    assert low.scenario_id() == "low"
    # −1.00% net of the 0.50% blended 운용보수 is a −0.50% gross asset return.
    assert low.gross_return(1) == near(-0.0050)
    assert low.gmab_claim_pp() == pytest.approx(10041179.61262558, abs=5e-6)
    assert low.av_ann_pp() == pytest.approx(25958820.38737442, abs=5e-6)
    assert low.gmab_claim_pp() == near(low.gmab_base_pp() - low.av_ann_pp())
    charge = sum(low.gmab_charges(t) for t in range(0, low.proj_len()))
    cost = sum(low.gmab_claims(t) for t in range(0, low.proj_len()))
    assert charge == pytest.approx(603909.13, abs=WON)
    assert cost == pytest.approx(929653.88, abs=WON)
    assert cost > charge


def test_pitfall_the_death_benefit_is_gross_and_splits_exactly(kr_va_anchor):
    """Pitfall 8: netting the GMDB and paying only the excess.

    The death benefit is Max[계약자적립액, 이미 납입한 보험료] and it splits **exactly**
    into the account value released from the 특별계정 and the top-up met from the 일반계정
    보증준비금.  Projecting only the top-up understates gross benefit outgo by the whole
    account value; projecting both double-counts.
    """
    a = kr_va_anchor
    assert a.check_gmdb_floor() is True
    for t in (0, 3, 120, 200, 239):
        assert a.db_pp(t) == pytest.approx(a.av_pp(t) + a.gmdb_claim_pp(t), abs=1e-8)
        assert a.check_gmdb_floor_resid(t) == pytest.approx(0.0, abs=1e-8)
    assert a.claims(0, "DEATH") == near(27.860533600121418)
    assert a.claims(0, "DEATH") == near(a.db_pp(0) * a.pols_death(0))
    assert a.gmdb_claims(0) == near(a.gmdb_claim_pp(0) * a.pols_death(0))
    assert a.claims_from_av(0, "DEATH") == near(a.av_pp(0) * a.pols_death(0))
    assert a.claims(0, "DEATH") == pytest.approx(
        a.claims_from_av(0, "DEATH") + a.gmdb_claims(0), abs=1e-9)
    assert a.gmdb_claims(0) / a.claims(0, "DEATH") == pytest.approx(0.115, abs=5e-4)


def test_pitfall_the_surrender_value_is_floored_at_zero(kr_va_anchor):
    """Pitfall 9: forgetting the statutory zero floor on the surrender value.

    ``cv_pp`` is max(0, AV − C).  Without the floor the first three months produce a
    *negative* surrender value — −₩564,564.41 at t = 0 — which a naive model would book as
    income.  ``claims_lapse`` is 0.00 at t = 0, 1 and 2 and ₩5,833.06 at t = 3, and a
    retrieved carrier illustration publishes exactly this shape.
    """
    a = kr_va_anchor
    assert a.cv_pp(0) == a.cv_pp(1) == a.cv_pp(2) == 0.0
    assert a.cv_pp(3) == near(234582.76753756206)
    assert a.av_pp(0) - a.surr_chg_pp(0) == pytest.approx(-564564.41, abs=WON)
    assert a.claims(0, "LAPSE") == a.claims(1, "LAPSE") == a.claims(2, "LAPSE") == 0.0
    assert a.claims(3, "LAPSE") == pytest.approx(5833.06, abs=WON)
    assert a.pols_lapse(0) > 0.0        # the exits happen; they are simply unpaid
    assert all(a.cv_pp(t) >= 0.0 for t in range(0, a.t_ann()))
    # The insurer never recovers more than the account holds, either.
    assert a.surr_charges(0) == near(min(a.surr_chg_pp(0), a.av_pp(0)) * a.pols_lapse(0))


def test_pitfall_the_surrender_charge_runs_off_in_the_amount(kr_va_anchor):
    """Pitfall 10: running the 해약공제 off linearly in the *ratio*.

    All three retrieved scales are ``C x (7 − k) ÷ 7`` in the **amount**; the published
    ratio falls far faster only because its denominator is growing.  A ratio-linear run-off
    over-recovers at every duration but the first.
    """
    a = kr_va_anchor
    c = a.surr_chg_pp(0)
    n = min(a.pay_term(), a.surr_chg_years)
    assert n == 7
    for k in range(0, 8):
        assert a.surr_chg_pp(12 * k) == near(SURR_SCALE[k])
        assert a.surr_chg_pp(12 * k) == pytest.approx(c * max(0, n - k) / n, abs=1e-6)
    # Linear in the amount: the differences are constant, the ratios are not.
    diffs = [a.surr_chg_pp(12 * k) - a.surr_chg_pp(12 * (k + 1)) for k in range(0, 6)]
    assert max(diffs) - min(diffs) == pytest.approx(0.0, abs=1e-6)
    ratios = [a.surr_chg_pp(12 * k) / a.av_pp(12 * k) for k in range(1, 6)]
    assert ratios == sorted(ratios, reverse=True)
    assert ratios[0] / ratios[-1] > 3.0
    # It steps at a completed policy year — the end of month 11 — not month by month.
    assert a.surr_chg_pp(10) == near(a.surr_chg_pp(0))
    assert a.surr_chg_pp(11) != pytest.approx(a.surr_chg_pp(10), rel=1e-6)
    assert a.surr_chg_pp(11) == near(a.surr_chg_pp(12))


def test_pitfall_the_statutory_cap_is_invisible_on_the_anchor(variable_annuity):
    """Pitfall 11: ignoring the 표준해약공제액 cap because it does not bind on the anchor.

    ₩1,643,940 against a level charge of ₩830,000 — 50.5% — so it is invisible on point 1
    and **binds exactly** on points 6, 7 and 10, all 5년납, where the scaled charge would
    otherwise exceed it.  A model tested only on its anchor cell would never learn that the
    cap exists.
    """
    anchor = variable_annuity.Projection[1]
    assert anchor.surr_chg_cap_pp() == near(SURR_CHG_CAP_PP)
    assert anchor.surr_chg_pp(0) / anchor.surr_chg_cap_pp() == pytest.approx(
        0.505, abs=5e-4)
    assert anchor.surr_chg_pp(0) < anchor.surr_chg_cap_pp()
    assert anchor.check_surr_chg_cap_resid(0) == 0.0
    # 5% x 연납순보험료 x min(납입기간, 12), 별표 14.
    assert anchor.surr_chg_cap_pp() == pytest.approx(
        0.05 * anchor.prem_ann_pp() * (1.0 - anchor.loading_rate())
        * min(anchor.pay_term(), 12), rel=1e-12)
    for point_id, cap in ((6, 1369950.0), (7, 547980.0), (10, 2739900.0)):
        p = variable_annuity.Projection[point_id]
        assert p.pay_term() == 5
        assert p.surr_chg_cap_pp() == near(cap)
        assert p.surr_chg_pp(0) == near(cap)
        assert p.check_surr_chg_cap() is True
        assert p.charge_rate("surr_charge") * p.prem_ann_pp() > p.surr_chg_cap_pp()


def test_pitfall_the_guaranteed_instalment_is_owed_to_every_annuitant(kr_va_anchor):
    """Pitfall 12: using ``pols_if(t)`` as the annuity payment weight inside the 보증기간.

    The instalment is owed to every contract that annuitised, alive or not, for ten years.
    ``pols_annuity_oblig(348)`` = 0.09258413 while ``pols_if(348)`` = 0.08682967 — a 6.6%
    difference on the last guaranteed instalment.
    """
    a = kr_va_anchor
    assert a.pols_annuity_oblig(348) == near(a.pols_annuitised())
    assert a.pols_annuitised() == near(POLS_ANNUITISED)
    assert a.pols_if(348) == near(0.08682967335056192)
    assert a.pols_annuity_oblig(348) / a.pols_if(348) - 1.0 == pytest.approx(
        0.066, abs=5e-4)
    for k in range(0, 10):
        assert a.pols_annuity_oblig(a.t_ann() + 12 * k) == near(a.pols_annuitised())
    for k in (10, 11, 20):
        t = a.t_ann() + 12 * k
        assert a.pols_annuity_oblig(t) == near(a.pols_if(t))
    assert a.pols_annuity_oblig(241) == 0.0
    assert a.is_annuity_month(240) is True and a.is_annuity_month(241) is False


def test_pitfall_the_death_and_surrender_streams_stop_at_annuitisation(kr_va_anchor):
    """Pitfall 13: keeping the death benefit or the surrender value alive after 연금개시.

    Both stop: the cover extinguishes at 연금개시 and no retrieved document permits
    surrender of a 종신연금형.  ``claims_death`` and ``claims_lapse`` are 0.00 for every
    t ≥ 240, and the decrement that remains is annuitant mortality alone.
    """
    a = kr_va_anchor
    for t in (240, 241, 360, 600, 959):
        assert a.claims(t, "DEATH") == 0.0
        assert a.claims(t, "LAPSE") == 0.0
        assert a.db_pp(t) == 0.0
        assert a.cv_pp(t) == 0.0
        assert a.lapse_rate(t) == 0.0
        assert a.lapse_rate_mth(t) == 0.0
        assert a.pols_lapse(t) == 0.0
    assert a.pols_death(240) > 0.0
    df = a.result_cf()
    assert df["claims_death"].iloc[240:].sum() == 0.0
    assert df["claims_lapse"].iloc[240:].sum() == 0.0


def test_pitfall_two_mortality_bases_across_the_join(kr_va_anchor):
    """Pitfall 14: using one mortality table across the join.

    Korea prices the deferral on the 보험사망률 and the payout on a separate, lighter
    연금사망률.  ``mort_rate(239)`` = 0.0054591503 and ``mort_rate(240)`` = 0.0047847455 —
    a 12.35% fall across one month that is a change of *table*, not of risk.
    """
    a = kr_va_anchor
    assert a.mort_rate(239) == near(0.0054591503)
    assert a.mort_rate(240) == near(0.0047847455)
    assert 1.0 - a.mort_rate(240) / a.mort_rate(239) == pytest.approx(0.1235, abs=5e-5)
    assert a.age(239) == 59 and a.age(240) == 60
    assert a.mort_rate_at_age(60) == near(0.0059773504)
    assert a.ann_mort_rate_at_age(60) == near(0.0047847455)
    assert a.mort_rate_at_age(60) != a.ann_mort_rate_at_age(60)
    # The insurance basis is the annuitant basis at mu / 0.80, so it is the heavier one.
    assert a.mort_rate_at_age(60) > a.ann_mort_rate_at_age(60)
    assert a.mort_rate(239) == near(a.mort_rate_at_age(59))
    assert a.mort_rate(240) == near(a.ann_mort_rate_at_age(60))
    # And the annuity factor is struck on the annuitant basis alone.
    assert a.ann_surv(0) == 1.0
    assert a.ann_surv(1) == near(1.0 - a.ann_mort_rate_at_age(60))


def test_pitfall_proj_len_is_the_month_count_not_the_last_index(variable_annuity):
    """Pitfall 15: reading ``proj_len()`` as the last row index.

    It is the **number of projected months**, the frame's exclusive end: the frame is
    ``range(proj_len())`` and the last row is ``proj_len() − 1``.  The anchor has 960
    rows, 0 … 959, and (120 − 40) × 12 = 960.  An off-by-one either drops the horizon
    month, in which ``pols_maturity`` carries out the survivors and the roll-forward
    closes, or adds a phantom row past it.
    """
    for point_id in variable_annuity.Data.model_point_table().index:
        p = variable_annuity.Projection[point_id]
        assert p.proj_len() == (p.omega_age - p.age_at_entry()) * 12
        assert len(p.result_cf()) == p.proj_len()
        assert p.result_cf().index[0] == 0
        assert p.result_cf().index[-1] == p.proj_len() - 1
        assert p.check_pols_roll_fwd() is True
        assert p.pols_maturity(p.proj_len() - 1) > 0.0
        assert p.pols_if(p.proj_len()) == 0.0
    anchor = variable_annuity.Projection[1]
    assert anchor.proj_len() == 960 and len(anchor.result_cf()) == 960
    assert anchor.result_cf().index[-1] == 959
    assert anchor.age(anchor.proj_len() - 1) == anchor.omega_age - 1


def test_pitfall_death_is_decremented_before_lapse(kr_va_anchor):
    """Pitfall 16: reversing the decrement order, or applying both to the opening count.

    Death is taken first and 해지 on the survivors: ``s(0) = (1 − d_rate) x w_mth``, not
    ``l(0) x w_mth``.  The difference is second-order in a month and first-order over 240
    of them.
    """
    a = kr_va_anchor
    assert a.pols_lapse(0) == near(0.02700152245035668)
    naive = a.pols_if(0) * a.lapse_rate_mth(0)
    assert naive == near(0.027004030272665847)
    assert a.pols_lapse(0) != pytest.approx(naive, rel=1e-9)
    assert a.pols_lapse(0) < naive
    assert a.pols_lapse(0) == pytest.approx(
        (a.pols_if(0) - a.pols_death(0)) * a.lapse_rate_mth(0), rel=1e-15)
    assert a.pols_death(0) == near(a.pols_if(0) * a.mort_rate_mth(0))
    assert a.pols_if(1) == pytest.approx(
        a.pols_if(0) - a.pols_death(0) - a.pols_lapse(0), rel=1e-15)


def test_pitfall_the_asset_based_charges_are_struck_after_the_premium(kr_va_anchor):
    """Pitfall 17: striking the asset-based guarantee charges before the premium goes in.

    They are struck on ``av_pp_at(t, "BEF_DEDUCT")`` — **after** the transfer.  At t = 0
    that is the difference between charging on ₩273,990 and charging on zero:
    ``gmdb_charge_pp(0)`` would be 0.00 instead of ₩15.98.
    """
    a = kr_va_anchor
    assert a.av_pp_at(0, "BEF_PREM") == 0.0
    assert a.av_pp_at(0, "BEF_DEDUCT") == near(273990.0)
    assert a.gmdb_charge_pp(0) > 0.0
    assert a.gmdb_charge_pp(0) == near(15.98275)
    assert a.gmab_charge_asset_pp(0) == near(57.081250000000004)
    assert a.gmdb_charge_pp(0) == near(
        a.charge_rate("gmdb_charge") / 12.0 * a.av_pp_at(0, "BEF_DEDUCT"))
    # And they are struck before the growth, so a rising month raises next month's charge.
    assert a.av_pp_at(1, "BEF_DEDUCT") == near(a.av_pp(0) + a.prem_to_av_pp(1))
    assert a.gmdb_charge_pp(1) == near(
        a.charge_rate("gmdb_charge") / 12.0 * a.av_pp_at(1, "BEF_DEDUCT"))
    assert a.gmdb_charge_pp(1) > a.gmdb_charge_pp(0)


def test_pitfall_the_bond_ladder_is_by_deferral_period(variable_annuity):
    """Pitfall 18: forgetting the mandatory 채권형 ladder, or applying the wrong rung.

    It is by **연금개시 전 보험기간** and not by fund choice: <12년 ≥80%, =12년 ≥70%,
    >12년 ≥50%.  The anchor's 20-year deferral takes the 50% rung; points 6 and 7 take 80%
    and 70%.  It binds both the premium allocation and the account mix and survives every
    later 펀드변경.
    """
    rungs = {1: (20, 0.50), 6: (10, 0.80), 7: (12, 0.70)}
    for point_id, (years, floor) in rungs.items():
        p = variable_annuity.Projection[point_id]
        assert p.defer_years() == years
        assert p.bond_floor() == near(floor)
        assert p.check_bond_floor() is True
        assert all(p.check_bond_floor_resid(t) == 0.0 for t in (0, 12, p.t_ann() - 1))
        assert p.bond_weight(0) >= floor
        assert p.bond_weight(p.t_ann() - 1) >= floor
        # It binds the premium allocation too: the initial mix sits on the floor.
        assert sum(p.fund_alloc(j) for j in p.fund_ids()
                   if p.fund_is_bond(j)) >= p.bond_floor()
    anchor = variable_annuity.Projection[1]
    assert (anchor.bond_floor_short, anchor.bond_floor_mid, anchor.bond_floor_long) == (
        0.80, 0.70, 0.50)
    # With no rebalancing the weight drifts, and on these scenarios it drifts upwards.
    assert anchor.bond_weight(119) > anchor.bond_weight(0)


def test_pitfall_the_derisking_fires_inside_its_window_and_conserves(kr_va_anchor):
    """Pitfall 19: skipping the pre-annuitisation de-risking, or applying it at wrong times.

    Its window is the three annual 계약해당일 inside 「개시일 − 3년」 — t = 204, 216, 228 on
    the anchor — it tops the 채권형 to 80%, and it **conserves the total**.  On the anchor it
    moves ₩12,113,087.24 at t = 204 and nothing afterwards, because the bond fund's lower
    운용보수 keeps the weight above 80% on its own.
    """
    a = kr_va_anchor
    assert a.derisk_lead_years == 3 and a.derisk_bond_target == 0.80
    assert a.derisk_amount_pp(204) == near(12113087.239005797)
    assert a.derisk_amount_pp(216) == 0.0
    assert a.derisk_amount_pp(228) == 0.0
    assert [t for t in range(0, a.t_ann()) if a.derisk_amount_pp(t) > 0.0] == [204]
    assert a.derisk_amount_pp(192) == 0.0     # outside the window
    assert a.derisk_amount_pp(205) == 0.0     # not a 계약해당일
    # It conserves the total, which is why check_av_roll_fwd does not see it.
    assert a.av_pp_at(204, "AFT_DERISK") == pytest.approx(
        a.av_pp_at(204, "AFT_DEDUCT"), abs=1e-6)
    assert a.check_av_roll_fwd() is True
    assert a.bond_weight(204) >= 0.80


def test_pitfall_a_withdrawal_rebases_both_guarantee_strikes(variable_annuity):
    """Pitfall 20: failing to re-base the guarantee strikes on a 중도인출.

    이미 납입한 보험료 is reduced **proportionally**, by (AV − W) ÷ AV, and it is the strike
    of **both** guarantees.  Without it a policyholder withdraws the fund and keeps the
    strike.  On point 9 the strike falls from a contractual ₩48,000,000 to ₩25,509,168.
    """
    p = variable_annuity.Projection[9]
    assert p.prem_total_pp() == near(48000000.0)
    assert p.gmab_base_pp() == near(25509167.99999999)
    assert p.gmab_base_pp() < p.prem_total_pp()
    first = 12 * p.wd_start_year()
    before = p.prem_paid_pp(first - 1)
    av_bef = p.av_pp_at(first, "BEF_DEDUCT") - p.mth_deduct_pp(first)
    assert p.wd_pp(first) > 0.0
    assert p.prem_paid_pp(first) == pytest.approx(
        (before + p.prem_pp(first)) * (av_bef - p.wd_pp(first)) / av_bef, abs=1e-6)
    assert p.prem_paid_pp(first) < before
    # The gross premium series is *not* reduced: the ten-year tax cap runs on it.
    assert p.prem_paid_gross_pp(p.t_ann() - 1) == near(48000000.0)
    # And the GMDB strike is the same object, so it falls too.
    assert p.db_pp(first) == near(max(p.av_pp(first), p.prem_paid_pp(first)))
    assert variable_annuity.Projection[1].prem_paid_pp(239) == near(36000000.0)


def test_pitfall_no_claims_column_beside_the_split_columns(kr_va_anchor):
    """Pitfall 21: publishing a ``claims`` column beside the ``claims_*`` columns.

    The house rule is that the columns of ``result_cf()`` sum to ``net_cf``; a subtotal
    beside its parts breaks that and silently double-counts in any downstream aggregation.
    The ``claims(t, kind)`` cells stays and takes all four kinds.
    """
    a = kr_va_anchor
    df = a.result_cf()
    assert "claims" not in df.columns
    assert set(df.columns) == {
        "pols_if", "premiums", "claims_death", "claims_lapse", "claims_annuity",
        "claims_maturity", "withdrawals", "fund_expenses", "expenses", "commissions",
        "net_cf"}
    assert all(c == c.lower() for c in df.columns)
    assert a.claims(3) == pytest.approx(
        sum(a.claims(3, k) for k in ("DEATH", "LAPSE", "ANNUITY", "MATURITY")), abs=1e-9)
    outgo = df[["claims_death", "claims_lapse", "claims_annuity", "claims_maturity",
                "withdrawals", "fund_expenses", "expenses", "commissions"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() < 1e-8


def test_pitfall_net_cf_excludes_investment_return(kr_va_anchor):
    """Pitfall 22: reading ``net_cf`` as including investment return.

    It does not: this library projects **gross liability cash flows** and the
    separate-account return is an asset-side quantity.  ``inv_income_pp`` and
    ``mgmt_fee_pp`` exist and are not columns.  A reader who adds them gets a number that
    is neither a liability cash flow nor a profit.
    """
    a = kr_va_anchor
    df = a.result_cf()
    for name in ("inv_income", "inv_income_pp", "mgmt_fee", "mgmt_fee_pp"):
        assert name not in df.columns
    assert a.inv_income_pp(0) > 0.0     # the quantity exists; it is simply not a column
    assert a.mgmt_fee_pp(0) > 0.0
    assert a.check_net_cf() is True
    assert a.net_cf(0) == near(
        a.premiums(0) - a.claims(0) - a.withdrawals(0) - a.fund_expenses(0)
        - a.expenses(0) - a.commissions(0))
    # Neither ledger carries it either: the separate account's return is not a flow.
    assert a.net_cf_sep(0) == near(
        a.prem_to_av(0) - a.av_charges(0) - a.surr_charges(0)
        - a.claims_from_av(0, "DEATH") - a.claims(0, "LAPSE")
        - a.withdrawals(0) - a.av_transfer(0) - a.fund_expenses(0))


def test_pitfall_charge_income_is_a_memo_not_revenue(kr_va_anchor):
    """Pitfall 23: treating ``charge_income(t)`` as revenue.

    Most of it is an **internal transfer** between the two accounts, and adding it to
    ``premiums`` counts the same money twice.  It is a memo cells and the external cash
    flow is ``net_cf``; ``check_net_cf()`` would fail if any transfer reached it.
    """
    a = kr_va_anchor
    assert a.charge_income(0) == near(
        a.prem_charges(0) + a.av_charges(0) + a.surr_charges(0) + a.annuity_charges(0))
    assert a.charge_income(0) > 0.0
    assert "charge_income" not in a.result_cf().columns
    for t in (0, 3, 120, 240):
        assert abs(a.check_net_cf_resid(t)) <= 1e-8 * max(
            1.0, abs(a.net_cf_gen(t)) + abs(a.net_cf_sep(t)))
    assert a.net_cf(0) < a.premiums(0)
    assert a.net_cf(0) != pytest.approx(a.premiums(0) + a.charge_income(0), rel=1e-6)
    # 연금수령기간 중 계약관리비용 is netted off the instalment, so it is a memo as well.
    assert a.annuity_charges(240) == near(a.annuity_charge_pp() * a.pols_annuitised())
    assert a.claims(240, "ANNUITY") == near(a.annuity_net_pp() * a.pols_annuitised())


def test_pitfall_the_model_runs_on_boheom_nai(variable_annuity):
    """Pitfall 24: running the model on 만나이.

    Every table, every model point age and the whole rate card are **보험나이**; the
    완전생명표 and every Korean population statistic are 만나이.  The six-month rule makes
    the two differ for half of all issue dates, so the error is worth about half a year of
    ageing on every row and raises nothing.
    """
    assert MODELS["VA_KR_S"][1]["age_basis"] == "보험나이"
    assert MODELS["VA_KR_S"][1]["grid"] == "monthly"
    assert MODELS["VA_KR_S"][1]["discounted"] is False
    doc = " ".join(variable_annuity.Projection.doc.split())
    assert "보험나이" in doc
    assert "만나이" in doc          # the basis it is *not*, named so a reader can tell
    # 보험나이 increments on the policy anniversary, not on the birthday.
    a = variable_annuity.Projection[1]
    assert a.age(0) == a.age_at_entry() == 40
    assert a.age(11) == 40 and a.age(12) == 41
    assert a.age(239) == 59 and a.age(240) == 60
    # No shift is applied anywhere: the model point age indexes the tables directly.
    assert a.mort_rate(0) == near(a.mort_rate_at_age(a.age_at_entry()))
    assert a.risk_prem_pp(0) == near(a.risk_prem_rate(40) * a.basic_prem_pp())


def test_pitfall_the_mortality_table_is_not_the_experience_table():
    """Pitfall 25: presenting ``mort_table.csv`` as the 경험생명표.

    It is a **[std]** Makeham construction on two published life expectancies, and the
    제10회 경험생명표 is not published.  Every row of the CSV carries a ``provenance`` cell
    that says so — either the [std] tag or the [REG-] citation of the anchor it was fitted
    to — and the same is required of every other input this model reads.
    """
    mort = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(mort.columns) == ["sex", "age", "mort_rate", "ann_mort_rate",
                                 "provenance"]
    assert (mort["provenance"].str.strip() != "").all()
    tagged = mort["provenance"].str.contains(r"\[std\]") | mort[
        "provenance"].str.contains(r"\[REG-R\d+\]")
    assert tagged.all()
    assert mort["provenance"].str.contains("gyeongheom saengmyeongpyo").any()
    assert set(mort["sex"]) == {"M", "F"}
    # The insurance basis is the annuitant basis at mu / 0.80, so it is heavier at every
    # age of both sexes: one table used for both would show up as equality here.
    below_omega = mort[mort["age"] < 120]
    assert (below_omega["mort_rate"] > below_omega["ann_mort_rate"]).all()
    assert (mort[mort["age"] == 120]["mort_rate"] == 1.0).all()
    for name in ("charge_table.csv", "fund_table.csv", "lapse_table.csv",
                 "return_scenario.csv", "risk_prem_table.csv", "crediting_table.csv"):
        df = pd.read_csv(CSV_DIR / name)
        assert "provenance" in df.columns, name
        assert df["provenance"].notna().all(), name
        assert (df["provenance"].str.strip() != "").all(), name


# ---------------------------------------------------------------------------
# The [std] parameters the notes state, read off the model


def test_the_std_scalar_assumptions_are_the_ones_the_notes_publish(kr_va_anchor):
    """Every scalar Reference of ``Projection``, asserted against the notes' value.

    These are the standardizations the notes carry a rationale for.  A silent change to any
    of them would move the worked example without any formula having changed, so they are
    read off the model here rather than being left to surface as a mismatched cash flow
    twenty tests further down.
    """
    a = kr_va_anchor
    assert a.omega_age == 120                 # terminal age of the shipped table [std]
    assert a.acq_charge_years == 10           # 계약체결비용 term, ten years [S2]
    assert a.gmab_charge_years == 7           # GMAB premium component, max 7 years [S1]
    assert a.surr_chg_years == 7              # 해약공제기간, statutory cap [REG-R19]
    assert a.guar_period_years == 10          # 보증지급기간, the modal election
    assert a.derisk_lead_years == 3           # 「연금개시일 − 3년」 window [S1]
    assert a.derisk_bond_target == 0.80       # the de-risking target weight [S1]
    assert a.bond_floor_short == 0.80         # <12년 rung of the mandatory ladder
    assert a.bond_floor_mid == 0.70           # =12년 rung
    assert a.bond_floor_long == 0.50          # >12년 rung
    assert a.addl_prem_cap_ratio == 2.0       # 추가납입 cap, 200% cumulative [S1]
    assert a.wd_max_cv_ratio == 0.5           # 중도인출 cap, 50% of the 해약환급금
    assert a.wd_min_residual_pp == 5000000.0  # residual 계약자적립액 per 구좌
    assert a.wd_cum_cap_years == 10           # the 소득세법 ten-year window [REG-R58]
    assert a.roll_fwd_tol == 1e-10
    assert a.val_tol == 1e-8
    assert a.point_id == 1


def test_the_charge_table_carries_the_notes_own_rates(kr_va_anchor):
    """The 수수료 안내표 as the notes print it, line by line, off ``charge_table.csv``.

    Some of these are sourced from a retrieved 상품요약서 and some are [std]; the test does
    not distinguish them, because the point of asserting them is that neither kind moves
    without the notes moving with it.
    """
    a = kr_va_anchor
    expected = {
        "acq_charge": 0.0517, "maint_charge_in": 0.0350, "other_charge": 0.0000,
        "maint_charge_after": 0.0133, "gmdb_charge": 0.0007,
        "gmab_charge_asset": 0.0025, "gmab_charge_prem": 0.0030,
        "fund_expense": 0.0000, "surr_charge": 0.2305555556, "surr_charge_cap": 0.0500,
        "annuity_charge": 0.0050, "expense_acq": 300000.0, "expense_maint": 3000.0,
        "comm_yr1": 0.0134, "comm_yr2": 0.0041, "comm_yr3": 0.0028,
        "comm_yr4": 0.0025, "comm_yr5": 0.0011,
    }
    for line, value in expected.items():
        assert a.charge_rate(line) == near(value), line
    # The five shipped commission years sum to 2.39% of 보험료총액, against [R1]'s
    # separately reported mean total of 2.11%; nothing is paid after year five.
    assert sum(a.comm_rate(y) for y in range(1, 6)) == pytest.approx(0.0239, abs=5e-6)
    assert a.comm_rate(0) == a.comm_rate(6) == 0.0


def test_the_fund_and_return_assumptions_are_the_ones_the_notes_publish(kr_va_anchor):
    """The allocation, the two 운용보수 and the gross asset return, all [std].

    Every return assumption on this product is [std] — no realised Korean fund return
    series was retrieved, and the base run works back from the 2026 평균공시이율 to a 3.00%
    gross return so that the 0.50% blended 운용보수 is a modelled cash flow rather than an
    assumption.  This is the largest single gap in the model and it is a CSV away.
    """
    a = kr_va_anchor
    assert a.fund_ids() == (1, 2)
    assert a.fund_is_bond(1) is True and a.fund_is_bond(2) is False
    assert a.fund_alloc(1) == near(0.5) and a.fund_alloc(2) == near(0.5)
    assert a.fund_mgmt_fee(1) == near(0.0040)
    assert a.fund_mgmt_fee(2) == near(0.0060)
    assert a.gross_return(1) == near(0.0300) and a.gross_return(2) == near(0.0300)
    blended = sum(a.fund_alloc(j) * a.fund_mgmt_fee(j) for j in a.fund_ids())
    assert blended == near(0.0050)
    # Net of the blended fee the base path is the 2026 평균공시이율 of 2.50%.
    assert 1.03 * (1 - blended) == pytest.approx(1.025, abs=5e-4)


def test_the_decrement_assumptions_are_the_ones_the_notes_publish(kr_va_anchor):
    """The lapse scale and both mortality bases at the durations the notes tabulate.

    The lapse scale's *level* is calibrated to a single second-hand sentence — a seven-year
    persistency of 28.9%, which is the product of the first seven annual 해지율 and not the
    in-force count, mortality being a separate decrement — and its shape is [std].  Both
    are the assumptions the guarantee costs are nine-tenths a function of.
    """
    a = kr_va_anchor
    assert a.lapse_rate(0) == near(0.28)
    assert a.lapse_rate(12) == near(0.22)
    assert a.lapse_rate(119) == near(0.08)
    assert a.lapse_rate_mth(0) == near(0.027004030272665847)
    assert a.lapse_rate_mth(0) == near(1.0 - (1.0 - 0.28) ** (1.0 / 12.0))
    persistency = 1.0
    for y in range(1, 8):
        persistency = persistency * (1.0 - a.lapse_rate(12 * (y - 1)))
    assert persistency == pytest.approx(0.289, abs=5e-4)
    assert a.mort_rate(0) == near(0.0011138523)
    assert a.mort_rate(12) == near(0.0011989710)
    assert a.mort_rate(120) == near(0.0024695609)
    assert a.mort_rate_mth(0) == near(1.0 - (1.0 - 0.0011138523) ** (1.0 / 12.0))
    assert a.risk_prem_rate(40) == near(0.000080)
    assert a.risk_prem_rate(50) == near(0.000095)


def test_the_inputs_live_beside_the_model_and_are_all_referenced(variable_annuity):
    """Every CSV in the product directory is read by a ``*_file`` Reference of ``Data``.

    The model folder holds ``__init__.py`` and ``_system.json`` only; the inputs are
    external, in the folder's parent, so a table can be replaced without touching a
    formula.  An orphan CSV beside them would mean a table nobody reads.
    """
    referenced = {variable_annuity.Data.refs[n] for n in variable_annuity.Data.refs
                  if n.endswith("_file")}
    assert {p.name for p in CSV_DIR.glob("*.csv")} == referenced
    assert variable_annuity.Data.input_dir() == pathlib.Path(MODEL_DIR).parent
    inside = {p.name for p in MODEL_DIR.rglob("*")
              if p.is_file() and "__pycache__" not in p.parts}
    assert inside == {"__init__.py", "_system.json"}
    assert not list(MODEL_DIR.glob("*.csv"))
