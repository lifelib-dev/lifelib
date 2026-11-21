"""Closed forms and formulas of the numpy reference implementation.

These tests check the reference itself, so that "the model equals the reference"
(test_model_g2pp.py) means the model is right. Integrals use scipy's adaptive quadrature
on the covariance kernels of x and y, which are simpler than the closed forms being
tested.
"""
import numpy as np
import pytest
from scipy import integrate

from g2pp_registry import INPUT
from reference_g2pp import DT, ReferenceG2PP, read_inputs

PARAMS = dict(a=0.773, b=0.082, sigma=0.022, eta=0.0104, rho=-0.7)


@pytest.fixture(scope="module")
def ref():
    """Default workbook inputs (EUR_BASE, BOND_MIX, 600 months) with 10,000 scenarios."""
    kwargs = read_inputs(INPUT)
    kwargs["scen_size"] = 10_000
    return ReferenceG2PP(**kwargs)


def flat_curve(rate=0.03, years=150, **kwargs):
    mats = np.arange(1, years + 1, dtype=float)
    return ReferenceG2PP(**{**PARAMS, **kwargs}, maturities=mats,
                         spot_rates=np.full(years, rate))


def kernels(m):
    """Covariances of x(u), y(v) with x(0) = y(0) = 0."""
    a, b, s, e, r = m.a, m.b, m.sigma, m.eta, m.rho

    def cxx(u, v):
        return s**2 / (2 * a) * (np.exp(-a * abs(u - v)) - np.exp(-a * (u + v)))

    def cyy(u, v):
        return e**2 / (2 * b) * (np.exp(-b * abs(u - v)) - np.exp(-b * (u + v)))

    def cxy(u, v):                      # Cov(x(u), y(v))
        mn = min(u, v)
        return r * s * e / (a + b) * (np.exp(-a * (u - mn) - b * (v - mn)) - np.exp(-a * u - b * v))

    def czz(u, v):                      # Cov(x(u) + y(u), x(v) + y(v))
        return cxx(u, v) + cyy(u, v) + cxy(u, v) + cxy(v, u)

    return cxx, cyy, cxy, czz


def quad(f, lo, hi):
    return integrate.quad(f, lo, hi, epsabs=0, epsrel=1e-13, limit=200)[0]


def var_integral(m, tau):
    """Var of the integral of x + y over [0, tau]: twice the integral over u < v."""
    czz = kernels(m)[3]
    val = integrate.dblquad(lambda u, v: czz(u, v), 0, tau, 0, lambda v: v,
                            epsabs=0, epsrel=1e-12)[0]
    return 2 * val


@pytest.mark.parametrize("kwargs", [{}, dict(rho=0.5, b=0.3), dict(eta=0.0, rho=0.0)])
def test_cov_step_against_quadrature(kwargs):
    m = flat_curve(**kwargs)
    a, b, s, e, r = m.a, m.b, m.sigma, m.eta, m.rho
    cxx, cyy, cxy, _ = kernels(m)
    expected = np.empty((3, 3))
    expected[0, 0] = quad(lambda u: s**2 * np.exp(-2 * a * (DT - u)), 0, DT)
    expected[1, 1] = quad(lambda u: e**2 * np.exp(-2 * b * (DT - u)), 0, DT)
    expected[0, 1] = quad(lambda u: r * s * e * np.exp(-(a + b) * (DT - u)), 0, DT)
    expected[0, 2] = quad(lambda u: cxx(DT, u) + cxy(DT, u), 0, DT)
    expected[1, 2] = quad(lambda u: cyy(DT, u) + cxy(u, DT), 0, DT)
    expected[2, 2] = var_integral(m, DT)
    expected[1, 0], expected[2, 0], expected[2, 1] = expected[0, 1], expected[0, 2], expected[1, 2]
    np.testing.assert_allclose(m.cov_step(), expected, rtol=1e-9, atol=1e-20)


@pytest.mark.parametrize("tau", [DT, 1.0, 10.0])
def test_V_against_double_integral(tau):
    m = flat_curve()
    np.testing.assert_allclose(m.V(tau), var_integral(m, tau), rtol=1e-9)


def test_singular_cov_falls_back_to_symmetric_root():
    m = flat_curve(eta=0.0, rho=0.0)
    cov, L = m.cov_step(), m.chol_step()
    with pytest.raises(np.linalg.LinAlgError):
        np.linalg.cholesky(cov)
    np.testing.assert_allclose(L @ L.T, cov, rtol=0, atol=1e-18)


@pytest.mark.parametrize("compounding", ["annual", "continuous"])
def test_curve_reproduces_spot_rates_at_knots(compounding):
    kwargs = read_inputs(INPUT)
    kwargs["compounding"] = compounding
    m = ReferenceG2PP(**kwargs)
    years = kwargs["maturities"]
    p = m.mkt_zcb((years * 12).astype(int))
    implied = p ** (-1 / years) - 1 if compounding == "annual" else -np.log(p) / years
    np.testing.assert_allclose(implied, kwargs["spot_rates"], rtol=1e-12, atol=1e-15)


def test_forward_is_flat_within_each_knot_interval(ref):
    p = ref.mkt_zcb(np.arange(1801))
    one_month = np.log(p[:-1] / p[1:]) / DT
    np.testing.assert_allclose(ref.mkt_fwd(np.arange(1800)), one_month, rtol=1e-9)
    last = (ref.knots_lnp[-2] - ref.knots_lnp[-1]) / (ref.knots_t[-1] - ref.knots_t[-2])
    assert ref.mkt_fwd(1800) == pytest.approx(last, rel=1e-15)


def test_curve_is_not_extrapolated(ref):
    ref.mkt_zcb(1800)
    with pytest.raises(ValueError):
        ref.mkt_zcb(1801)
    with pytest.raises(ValueError):
        ref.mkt_fwd(1801)


@pytest.mark.parametrize("m", [1, 60, 120])
def test_bond_returns_equal_ratio_of_full_bond_prices(ref, m):
    lhs = ref.zcb_return(m)
    rhs = np.array([ref.P(i + 1, i + m) / ref.P(i, i + m) - 1 for i in range(ref.n)])
    np.testing.assert_allclose(lhs, rhs, rtol=0, atol=1e-13)


def test_all_cash_fund_earns_the_bank_return():
    kwargs = read_inputs(INPUT)
    kwargs.update(fund_cash=1.0, fund_bonds={}, scen_size=200)
    sim = ReferenceG2PP(**kwargs).simulate()
    assert np.array_equal(sim["F"], sim["R"])


def test_antithetic_pairs_are_exact_negatives(ref):
    x, y, half = ref.simulate()["x"], ref.simulate()["y"], ref.N // 2
    assert np.array_equal(x[1:, :half], -x[1:, half:])
    assert np.array_equal(y[1:, :half], -y[1:, half:])


def test_extending_the_horizon_keeps_earlier_months():
    kwargs = read_inputs(INPUT)
    kwargs["scen_size"] = 200
    short = ReferenceG2PP(**{**kwargs, "step_size": 120}).simulate()
    long = ReferenceG2PP(**{**kwargs, "step_size": 240}).simulate()
    assert np.array_equal(short["D"], long["D"][:121])
    assert np.array_equal(short["F"], long["F"][:120])


def pair_z(values):
    """z-score of mean(values) - 1 for each month, SE from antithetic pair means."""
    half = values.shape[1] // 2
    pairs = 0.5 * (values[:, :half] + values[:, half:])
    se = pairs.std(axis=1, ddof=1) / np.sqrt(half)
    return (pairs.mean(axis=1) - 1) / se


def test_deflators_and_fund_are_martingales(ref):
    sim = ref.simulate()
    p = ref.mkt_zcb(np.arange(ref.n + 1))
    assert np.abs(pair_z(sim["D"][1:] / p[1:, None])).max() < 3
    growth = np.cumprod(1 + sim["F"], axis=0)
    assert np.abs(pair_z(sim["D"][1:] * growth)).max() < 3


@pytest.mark.parametrize("fund", [dict(fund_cash=1.0, fund_bonds={}),
                                  dict(fund_cash=0.0, fund_bonds={120: 1.0}),
                                  dict(fund_cash=0.0, fund_bonds={24: 1.0})])
def test_fund_logvar_matches_simulated_variance(fund):
    kwargs = read_inputs(INPUT)
    kwargs.update(fund, scen_size=20_000, step_size=120)
    m = ReferenceG2PP(**kwargs)
    log_growth = np.log1p(m.simulate()["F"]).sum(axis=0)
    # pairs share one deviation, so 20,000 antithetic paths act like 10,000 draws:
    # the relative SE of the sample variance is about sqrt(2/10,000), 1.4%
    assert np.var(log_growth) == pytest.approx(m.fund_logvar(120), rel=0.05)
