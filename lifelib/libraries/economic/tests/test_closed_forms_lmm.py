"""Closed forms and identities of the numpy reference implementation of the LMM.

These tests check the reference itself, so that "the model equals the reference"
(test_model_lmm.py) means the model is right. They cover the fit to the initial curve, the
identities of the interpolated bonds, and the Monte Carlo against closed forms: caplets
against Black's formula, and a maturity guarantee against the floorlet it equals. The
specification is section 4 of the design note, ``_research/lmm_design.md``.

A check with m z-scores passes if its largest |z| is below Phi^-1(1 - 0.00135/m), the rule
of the Validation spaces.
"""
import numpy as np
import pandas as pd
import pytest
from scipy import stats

from lmm_registry import INPUT
from reference_lmm import DT, ReferenceLMM, black, read_inputs


def make(**kwargs):
    """The reference on the delivered workbook, with some inputs replaced."""
    return ReferenceLMM(**{**read_inputs(INPUT), **kwargs})


def mean_se(samples):
    """Mean and standard error over the first axis, from antithetic pair means."""
    half = len(samples) // 2
    pairs = 0.5 * (samples[:half] + samples[half:])
    return pairs.mean(axis=0), pairs.std(axis=0, ddof=1) / np.sqrt(half)


def assert_z_within_limit(mc, se, theory):
    """Where the estimate is exact by construction (se near 0), z is 0, as in mcstats."""
    mc, se = np.atleast_1d(mc), np.atleast_1d(se)
    theory = np.broadcast_to(theory, mc.shape)
    tol = 1e-12 * np.maximum(1.0, np.abs(theory))
    z = np.where(np.abs(mc - theory) <= 1e3 * tol, 0.0, np.inf)
    np.divide(mc - theory, se, out=z, where=se > tol)
    limit = stats.norm.isf(0.00135 / z.size)
    assert np.abs(z).max() < limit, f"max |z| {np.abs(z).max():.2f}, limit {limit:.2f}: {z}"


# ---- the initial curve -------------------------------------------------------------------

@pytest.mark.parametrize("compounding", ["annual", "continuous"])
def test_curve_reproduces_spot_rates_at_knots(compounding):
    kwargs = read_inputs(INPUT)
    m = ReferenceLMM(**{**kwargs, "compounding": compounding})
    years = kwargs["maturities"]
    p = m.mkt_zcb((years * 12).astype(int))
    implied = p ** (-1 / years) - 1 if compounding == "annual" else -np.log(p) / years
    np.testing.assert_allclose(implied, kwargs["spot_rates"], rtol=1e-12, atol=1e-15)


def test_curve_is_not_extrapolated():
    m = make()
    m.mkt_zcb(1800)
    with pytest.raises(ValueError):
        m.mkt_zcb(1801)


@pytest.mark.parametrize("tenor", [12, 3, 1])
def test_bonds_of_every_month_fit_the_initial_curve(tenor):
    m = make(tenor_mth=tenor, step_size=120, scen_size=2)
    months = np.arange(m.K * tenor + 1)
    F, Dc = np.tile(m.F0, (1, 1)), np.ones(1)
    initial = np.array([m.deflated_bond(0, F, Dc, j)[0] for j in months])
    np.testing.assert_allclose(initial, m.mkt_zcb(months), rtol=1e-14)
    kappa = m.kappa(months)
    assert (kappa[::tenor] == 1).all()
    assert np.abs(kappa - 1).max() < 2e-4


def test_vol_loadings_are_read_at_the_middle_of_each_month():
    kwargs = read_inputs(INPUT)
    m = ReferenceLMM(**kwargs)
    for months in (1, 7, 12, 119):
        u = (months - 0.5) / 12
        expected = [np.interp(u, kwargs["vol_maturities"], kwargs["vol_table"][:, q])
                    for q in range(2)]
        np.testing.assert_allclose(m.lam[months], expected, rtol=1e-14)
    assert (m.lam[0] == 0).all()


def test_volatility_table_that_ends_too_early():
    kwargs = read_inputs(INPUT)
    short = kwargs["vol_maturities"] <= 40
    with pytest.raises(ValueError, match="volatility table ends"):
        ReferenceLMM(**{**kwargs, "vol_maturities": kwargs["vol_maturities"][short],
                        "vol_table": kwargs["vol_table"][short]})


# ---- identities of the scenarios ---------------------------------------------------------

@pytest.mark.parametrize("tenor", [12, 3])
def test_zero_volatility_gives_the_ce_scenario(tenor):
    kwargs = read_inputs(INPUT)
    m = ReferenceLMM(**{**kwargs, "vol_table": np.zeros_like(kwargs["vol_table"]),
                        "tenor_mth": tenor, "scen_size": 10, "step_size": 120})
    for paths in (m.disc_factor_paths(), m.bank_return_paths(), m.fund_return_paths(),
                  m.libor_rate_paths(), m.spot_rate_paths(120)):
        np.testing.assert_allclose(paths[1:], np.broadcast_to(paths[0], paths[1:].shape),
                                   rtol=1e-12, atol=1e-15)


@pytest.mark.parametrize("tenor", [12, 3, 1])
def test_bank_return_is_known_at_the_start_of_each_month(tenor):
    """The deflated price of a bond does not change in its last month."""
    sim = make(tenor_mth=tenor, scen_size=100, step_size=60).simulate()
    assert np.array_equal(sim["D"][1:], sim["dz"][1][:-1])


def test_all_cash_fund_earns_the_bank_return():
    m = make(fund_cash=1.0, fund_bonds={}, scen_size=200, step_size=120)
    assert np.array_equal(m.fund_returns(), m.bank_returns())


def test_antithetic_random_numbers():
    m = make(scen_size=100, step_size=12)
    z = m.normals()
    assert np.array_equal(z[:, :50], -z[:, 50:])


@pytest.mark.parametrize("longer", [dict(step_size=240), dict(maturity_size=240)])
def test_extending_the_run_keeps_earlier_months(longer):
    """Equal up to rounding: the matrix products of longer arrays can round differently."""
    short = make(scen_size=200, step_size=120)
    long = make(**{"scen_size": 200, "step_size": 120, **longer})
    np.testing.assert_allclose(long.disc_factor_paths()[:, :121], short.disc_factor_paths(),
                               rtol=1e-12)
    np.testing.assert_allclose(long.fund_return_paths()[:, :120], short.fund_return_paths(),
                               rtol=1e-12, atol=1e-15)


# ---- Monte Carlo against closed forms ----------------------------------------------------

@pytest.fixture(scope="module")
def caplet_run():
    """40,000 scenarios over 10 years, with annual forward rates."""
    m = make(scen_size=40_000, step_size=120, maturity_size=12, fund_cash=1.0, fund_bonds={})
    m.simulate()
    return m


def caplet_checks(m, ks):
    mc, se, theory = [], [], []
    for k in ks:
        for moneyness in (0.75, 1.0, 1.5):
            x = moneyness * (m.F0[k - 1] + m.alpha) - m.alpha
            mean, err = mean_se(m.caplet_payoffs(k, x))
            mc.append(mean), se.append(err), theory.append(m.caplet(k, x))
    return np.array(mc), np.array(se), np.array(theory)


def test_caplets_match_black(caplet_run):
    """Caplets expiring in 1, 5 and 10 years at 0.75, 1 and 1.5 times the forward rate."""
    assert_z_within_limit(*caplet_checks(caplet_run, [2, 6, 11]))


def test_caplets_match_black_with_a_monthly_tenor():
    """With tenor_mth 1 nothing is interpolated: caplets expiring in 1, 3 and 5 years."""
    m = make(tenor_mth=1, scen_size=10_000, step_size=60, maturity_size=12,
             fund_cash=1.0, fund_bonds={})
    assert_z_within_limit(*caplet_checks(m, [13, 37, 61]))


@pytest.mark.parametrize("tenor, scen_size", [(12, 40_000), (6, 40_000), (1, 40_000)])
def test_gmab_at_the_second_tenor_date_is_a_floorlet(tenor, scen_size):
    """All-cash fund, maturity T_2: the guarantee against its closed form for five premiums."""
    m = make(tenor_mth=tenor, scen_size=scen_size, step_size=2 * tenor,
             fund_cash=1.0, fund_bonds={})
    deflator = m.simulate()["D"][2 * tenor]
    sa, premiums = 50e6, [30e6, 46e6, 47.5e6, 48e6, 50e6]
    payoffs = np.column_stack([np.maximum(sa * deflator - av0, 0) for av0 in premiums])
    mc, se = mean_se(payoffs)
    theory = np.array([m.gmab_floorlet(sa, av0) for av0 in premiums])
    assert theory[-1] == 0 and (payoffs[:, -1] == 0).all()     # out of reach: worth nothing
    assert_z_within_limit(mc[:-1], se[:-1], theory[:-1])


def test_floorlet_by_parity_equals_the_direct_formula():
    """The plan's floorlet formula of the GMAB against the reference's put-call parity."""
    m = make()
    sa = 50e6
    for av0 in (30e6, 46e6, 47.5e6, 48e6):
        x = (sa * m.P0[1] / av0 - 1) / m.tau
        F, X, v = m.F0[1] + m.alpha, x + m.alpha, m.caplet_total_vol(2)
        d1 = (np.log(F / X) + v**2 / 2) / v
        direct = (av0 / m.P0[1] * m.tau * m.P0[2]
                  * (X * stats.norm.cdf(v - d1) - F * stats.norm.cdf(-d1)))
        assert m.gmab_floorlet(sa, av0) == pytest.approx(direct, rel=1e-12)


def test_black_at_the_money_has_the_textbook_value():
    v = 0.2
    assert black(1.0, 1.0, v) == pytest.approx(2 * stats.norm.cdf(v / 2) - 1, rel=1e-14)


def test_deflators_and_fund_are_martingales():
    """4,000 scenarios over 20 years: mean deflators and the deflated fund, every month."""
    m = make(scen_size=4_000, step_size=240)
    D = m.simulate()["D"]
    p = m.mkt_zcb(np.arange(m.n + 1))
    mc, se = mean_se(D[1:].T / p[1:])
    assert_z_within_limit(mc, se, 1.0)
    growth = np.cumprod(1 + m.fund_returns(), axis=0)
    mc, se = mean_se((D[1:] * growth).T)
    assert_z_within_limit(mc, se, 1.0)


def test_swaption_approximation_at_the_money():
    """Rebonato's formula is an approximation: within 3% of the Monte Carlo volatility."""
    m = make(scen_size=20_000, step_size=60, maturity_size=60, fund_cash=1.0, fund_bonds={},
             snapshots=[60])
    vol, swap, annuity = m.swaption_vol(5, 5)
    F, Dc = m.simulate()["snapshots"][60]
    bonds = {j: m.deflated_bond(60, F, Dc, j) for j in range(60, 121, 12)}
    annuity_paths = sum(bonds[j] for j in range(72, 121, 12))
    payoffs = np.maximum(bonds[60] - bonds[120] - swap * annuity_paths, 0)
    price = mean_se(payoffs)[0] / annuity
    lo, hi = 0.0, 1.0
    for _ in range(60):                                    # implied total volatility
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if black(swap + m.alpha, swap + m.alpha, mid) < price else (lo, mid)
    assert lo / np.sqrt(5) == pytest.approx(vol, rel=0.03)
    assert pd.notna(vol) and 0.05 < vol < 0.3
