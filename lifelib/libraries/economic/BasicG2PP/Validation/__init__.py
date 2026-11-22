# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Checks of the G2PP space against closed forms and martingale properties.

Every test returns a DataFrame with the columns

* ``mc``: the Monte Carlo estimate over the stochastic scenarios 1 to N,
* ``theory``: the value it should converge to,
* ``se``: its standard error, from antithetic pair means when antithetic variates are on,
* ``z``: :math:`(\\mathrm{mc} - \\mathrm{theory}) / \\mathrm{se}`.

With correct formulas, each z is roughly standard normal, so :math:`|z| > 3` is rare for a
single check. Tests that cover many months or moments contain many z-scores, so a larger
maximum is expected by chance: :func:`summary` compares the largest :math:`|z|` of each
test with a limit that allows for the number of z-scores. Where the estimate is exact by
construction, z is 0 (see ``mcstats.check``).

The tests read the scenarios through the Reference :attr:`g2pp`, so they run on whatever
input the G2PP space uses. Statistical power grows with ``scen_size``; 10,000 antithetic
scenarios is a good setting for validation.

Attributes:

    g2pp: The G2PP space.

    mcstats: User module with :func:`check`, which turns samples into the DataFrame
        above. Saved in the model folder as ``mcstats.py``.

    np: The numpy module.

    pd: The pandas module.

    stats: The scipy.stats module, for the normal distribution.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def martingale_test():
    r"""Mean deflator against the initial curve, for every month

    :math:`E[D(t_i)] = P^M(0, t_i)` for i = 0 to n.

    Returns:
        pandas.DataFrame indexed by month ``t``, columns ``mc``, ``theory``, ``se``, ``z``
    """
    paths = g2pp.disc_factor_paths()
    return mcstats.check(paths[1:], paths[0], g2pp.antithetic(),
                         pd.RangeIndex(paths.shape[1], name="t"))


def fund_martingale_test():
    r"""Deflated value of the selected fund against 1, for every month

    :math:`E[D(t_i) AV(t_i)/AV_0] = 1` with :math:`AV(t_i)/AV_0 = \prod_{k<i}(1 + R^F_k)`,
    because the fund trades only bonds and the bank account. For an all-cash fund this
    holds in every scenario, so z is 0.

    Returns:
        pandas.DataFrame indexed by month ``t``, columns ``mc``, ``theory``, ``se``, ``z``
    """
    returns = g2pp.fund_return_paths()
    growth = np.cumprod(np.hstack([np.ones((len(returns), 1)), 1 + returns]), axis=1)
    values = g2pp.disc_factor_paths() * growth
    return mcstats.check(values[1:], 1.0, g2pp.antithetic(),
                         pd.RangeIndex(values.shape[1], name="t"))


def curve_fit_test():
    r"""Spot rates implied by the mean deflators against the input curve

    At each maturity of the selected curve that is a whole number of months no later
    than :math:`t_n`, the spot rate implied by the mean of :math:`D(t)` (compounded as
    the input) against the input spot rate. The standard error comes from that of
    :func:`martingale_test` by the delta method.

    Returns:
        pandas.DataFrame indexed by ``maturity`` in years, columns ``mc``, ``theory``,
        ``se``, ``z``
    """
    col = g2pp.curve_table()[g2pp.curve_id()].dropna()
    years = col.index.to_numpy(dtype=float)
    months = np.round(years * 12).astype(int)
    keep = (np.abs(years * 12 - months) < 1e-9) & (months <= g2pp.step_size())
    years, months, spot = years[keep], months[keep], col.to_numpy(dtype=float)[keep]
    mart = martingale_test()
    mean, se_mean = mart["mc"].to_numpy()[months], mart["se"].to_numpy()[months]
    if g2pp.compounding() == "annual":
        implied = mean ** (-1 / years) - 1
        slope = mean ** (-1 / years - 1) / years
    else:
        implied = -np.log(mean) / years
        slope = 1 / (mean * years)
    se = slope * se_mean
    return pd.DataFrame({"mc": implied, "theory": spot, "se": se, "z": (implied - spot) / se},
                        index=pd.Index(years, name="maturity"))


def zcb_martingale_test(i, j):
    r"""Deflated bond prices: :math:`E[D(t_i) P(t_i, t_j)] = P^M(0, t_j)`

    Returns:
        pandas.DataFrame with one row indexed by (``i``, ``j``)
    """
    values = g2pp.disc_factor(i) * g2pp.P_t_T(i, j)
    return mcstats.check(values, g2pp.mkt_zcb(j), g2pp.antithetic(),
                         pd.MultiIndex.from_tuples([(i, j)], names=["i", "j"]))


def moments_test():
    r"""Means, variances and covariance of :math:`x`, :math:`y` and :math:`r`, every year

    At each whole year up to :math:`t_n` (or at :math:`t_n` if the run is shorter than
    a year), against

    .. math::

        E[x] = E[y] = 0, \quad E[r] = \varphi(t), \quad
        \mathrm{Var}[x] = \frac{\sigma^2}{2a}(1 - e^{-2at}), \quad
        \mathrm{Var}[y] = \frac{\eta^2}{2b}(1 - e^{-2bt}), \quad
        \mathrm{Cov}[x, y] = \frac{\rho\sigma\eta}{a + b}(1 - e^{-(a+b)t})

    and :math:`\mathrm{Var}[r]` from ``Var_rt``. With antithetic variates the three
    means are exact by construction, so their z is 0.

    Returns:
        pandas.DataFrame indexed by (``t``, ``moment``), columns ``mc``, ``theory``,
        ``se``, ``z``
    """
    a, b, s, e, r = g2pp.a(), g2pp.b(), g2pp.sigma(), g2pp.eta(), g2pp.rho()
    n = g2pp.step_size()
    names = ["mean x", "mean y", "mean r", "var x", "var y", "cov xy", "var r"]
    frames = []
    for i in list(range(12, n + 1, 12)) or [n]:
        t = g2pp.t_(i)
        x, y, rate = g2pp.x(i), g2pp.y(i), g2pp.short_rate(i)
        dx, dy, dr = x - x.mean(), y - y.mean(), rate - rate.mean()
        samples = np.column_stack([x, y, rate, dx**2, dy**2, dx * dy, dr**2])
        theory = [0.0, 0.0, g2pp.phi(i),
                  s**2 / (2 * a) * -np.expm1(-2 * a * t),
                  e**2 / (2 * b) * -np.expm1(-2 * b * t),
                  r * s * e / (a + b) * -np.expm1(-(a + b) * t),
                  g2pp.Var_rt()[i]]
        index = pd.MultiIndex.from_product([[i], names], names=["t", "moment"])
        frames.append(mcstats.check(samples, theory, g2pp.antithetic(), index))
    return pd.concat(frames)


def zbp_cf(i, j, K):
    r"""Closed-form price of a put on a zero-coupon bond (Brigo and Mercurio, section 4.2)

    The price at time 0 of a European put with expiry :math:`T = t_i` and strike
    :math:`K` on the bond maturing at :math:`S = t_j`:

    .. math::

        \mathrm{ZBP} = K P^M(0, T)\Phi(-h + \Sigma) - P^M(0, S)\Phi(-h), \quad
        h = \frac{1}{\Sigma}\ln\frac{P^M(0, S)}{K P^M(0, T)} + \frac{\Sigma}{2}

        \Sigma^2 = \frac{\sigma^2}{2a^3}(1 - e^{-a(S-T)})^2(1 - e^{-2aT})
        + \frac{\eta^2}{2b^3}(1 - e^{-b(S-T)})^2(1 - e^{-2bT})
        + \frac{2\rho\sigma\eta}{ab(a+b)}(1 - e^{-a(S-T)})(1 - e^{-b(S-T)})(1 - e^{-(a+b)T})
    """
    a, b, s, e, r = g2pp.a(), g2pp.b(), g2pp.sigma(), g2pp.eta(), g2pp.rho()
    T, S = g2pp.t_(i), g2pp.t_(j)
    var = (s**2 / (2 * a**3) * np.expm1(-a * (S - T))**2 * -np.expm1(-2 * a * T)
           + e**2 / (2 * b**3) * np.expm1(-b * (S - T))**2 * -np.expm1(-2 * b * T)
           + 2 * r * s * e / (a * b * (a + b)) * np.expm1(-a * (S - T)) * np.expm1(-b * (S - T))
           * -np.expm1(-(a + b) * T))
    vol = np.sqrt(var)
    p_T, p_S = g2pp.mkt_zcb(i), g2pp.mkt_zcb(j)
    h = np.log(p_S / (K * p_T)) / vol + vol / 2
    return float(K * p_T * stats.norm.cdf(-h + vol) - p_S * stats.norm.cdf(-h))


def zbp_mc(i, j, K):
    r"""Monte Carlo price of the bond put of :func:`zbp_cf`, against the closed form

    The mean of :math:`D(t_i)\max(K - P(t_i, t_j), 0)`.

    Returns:
        pandas.DataFrame with one row indexed by (``i``, ``j``, ``K``)
    """
    values = g2pp.disc_factor(i) * np.maximum(K - g2pp.P_t_T(i, j), 0)
    return mcstats.check(values, zbp_cf(i, j, K), g2pp.antithetic(),
                         pd.MultiIndex.from_tuples([(i, j, K)], names=["i", "j", "K"]))


def deflator_call_test(i, k):
    r"""Call on the deflator :math:`D(t_i)` with strike :math:`K = k P^M(0, t_i)`

    :math:`\ln D(T) \sim N(\ln P^M(0, T) - V/2, V)` with :math:`V = V(0, T)`, so

    .. math::

        E[(D(T) - K)^+] = P^M(0, T)\Phi(d_1) - K\Phi(d_1 - \sqrt{V}), \quad
        d_1 = \frac{\ln(P^M(0, T)/K) + V/2}{\sqrt{V}}

    This is also the GMAB of a single-premium policy whose fund is all cash, per unit of
    sum assured, with :math:`k = AV_0 / (SA\, P^M(0, T))`.

    Returns:
        pandas.DataFrame with one row indexed by (``i``, ``k``)
    """
    p = g2pp.mkt_zcb(i)
    strike = k * p
    var = g2pp.V_t_T(0, i)
    d1 = (np.log(p / strike) + var / 2) / np.sqrt(var)
    theory = p * stats.norm.cdf(d1) - strike * stats.norm.cdf(d1 - np.sqrt(var))
    values = np.maximum(g2pp.disc_factor(i) - strike, 0)
    return mcstats.check(values, theory, g2pp.antithetic(),
                         pd.MultiIndex.from_tuples([(i, k)], names=["i", "k"]))


def summary():
    r"""Largest :math:`|z|` of each test on the current input, against its limit

    Runs every test, with the bond tests at :math:`t_i`, i = n // 2: the deflated bond
    and the at-the-money bond put maturing five years later, and the deflator call with
    k = 0.9.

    A test with m z-scores passes if its largest :math:`|z|` is below
    :math:`\Phi^{-1}(1 - 0.00135/m)`. That keeps the chance of a false alarm at that of a
    single 3-sigma check, 0.27%, if the z-scores were independent; positively correlated
    ones, such as those of neighbouring months, make it smaller still. The limit is 3
    for a single check and about 4.5 for 600 months.

    Returns:
        pandas.DataFrame indexed by test, columns ``checks`` (number of z-scores),
        ``max_abs_z``, ``limit``, ``ok`` and ``at`` (the row of the largest :math:`|z|`)
    """
    i = max(1, g2pp.step_size() // 2)
    j = i + 60
    atm = g2pp.mkt_zcb(j) / g2pp.mkt_zcb(i)
    tests = {
        "martingale_test()": martingale_test(),
        "fund_martingale_test()": fund_martingale_test(),
        "curve_fit_test()": curve_fit_test(),
        "moments_test()": moments_test(),
        f"zcb_martingale_test({i}, {j})": zcb_martingale_test(i, j),
        f"zbp_mc({i}, {j}, at the money)": zbp_mc(i, j, atm),
        f"deflator_call_test({i}, 0.9)": deflator_call_test(i, 0.9),
    }
    rows = {}
    for name, df in tests.items():
        z = df["z"].abs()
        m = int(z.notna().sum())
        limit = float(stats.norm.isf(0.00135 / m))
        rows[name] = {"checks": m, "max_abs_z": z.max(), "limit": limit,
                      "ok": bool(z.max() < limit), "at": z.idxmax()}
    return pd.DataFrame.from_dict(rows, orient="index")


# ---------------------------------------------------------------------------
# References

g2pp = ("Interface", ("..", "G2PP"), "auto")

np = ("Module", "numpy")

pd = ("Module", "pandas")

stats = ("Module", "scipy.stats")

mcstats = ("IOSpec", 1)  # ModuleData path='mcstats.py'