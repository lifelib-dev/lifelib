# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Monthly LMM interest rate scenarios fitted to an initial curve.

The LIBOR market model (Brigo and Mercurio, 2nd ed. 2006, chapter 6), with the shift of
their section 10.1, under the spot-LIBOR measure. The forward rate :math:`F_k` covers the
period :math:`(T_{k-1}, T_k]` between the tenor dates :math:`T_k = k\\tau`, where
:math:`\\tau` is :func:`tenor_mth` months, and :math:`F_k + \\alpha` is lognormal, where
:math:`\\alpha` is :func:`shift`:

.. math::

    \\frac{d(F_k + \\alpha)}{F_k + \\alpha} = {} & \\lambda_k \\cdot \\sum_{j=\\beta(t)}^{k}
    \\frac{\\tau(F_j + \\alpha)}{1 + \\tau F_j}\\lambda_j\\,dt \\\\
    & + \\lambda_k \\cdot dW(t)

:math:`W` is a Brownian motion with as many dimensions as the volatility table has factors,
:math:`\\lambda_k` the volatility vector of :math:`F_k`, and :math:`\\beta(t)` the first rate
not yet set at :math:`t`. The rates start from the forward rates of the initial curve
:math:`P^M(0, t)` and move every month by a log-Euler step (:func:`fwd_rates`). Bonds that
mature on tenor dates are products of the rates, and bonds of every other monthly maturity
are interpolated between them (:func:`defl_zcb`), so the deflators reproduce the initial
curve up to Monte Carlo noise. Time is in years, and month ``i`` is :math:`t_i = i/12`
(:func:`t_`). N is :func:`scen_size`, n is :func:`step_size`, p is :func:`tenor_mth`, K is
:func:`tenor_size` and d is :func:`factor_size`.

**Inputs** are read at run time from the Excel file :attr:`input_file`, located next to
the model folder: sheet ``Params`` (the shift, the tenor and the run settings), sheet
``Curve`` (initial spot rates by maturity, one column per curve ID), sheet ``Vol`` (the
volatility of the forward rates by time to expiry, one column per factor) and sheet
``Fund`` (shares of bond funds by years to maturity). Neither the curve nor the volatility
table is extrapolated, so they must reach every maturity a run needs. After editing the
file in place, call ``clear_all()`` on the model; assigning another :attr:`input_file`
recalculates automatically.

**Outputs** for liability models are arrays with one row per scenario, named and shaped as
in :mod:`~economic.BasicG2PP`. Row 0 is the certainty-equivalent (CE) scenario, which
follows the initial forward curve, and row k is stochastic scenario k (see
:func:`scen_index`):

* :func:`disc_factor_paths`: deflators :math:`D(t_i)`, for discounting cash flows at
  :math:`t_i`
* :func:`fund_return_paths`: returns over :math:`[t_i, t_{i+1})` of the bond fund chosen
  by :func:`fund_id`
* :func:`bank_return_paths`: bank-account returns over :math:`[t_i, t_{i+1})`
* :func:`libor_rate_paths`, :func:`spot_rate_paths`: LIBOR rates and yields

Attributes:

    input_file: Name of the Excel input file, relative to the folder that contains the
        model folder, or an absolute path. ``"lmm_input.xlsx"`` by default.

    dt: Length of a monthly step in years, 1/12.

    np: The numpy module.

    pd: The pandas module.

.. seealso::

   * Damiano Brigo, Fabio Mercurio (2001, 2nd Ed. 2006). Interest Rate Models - Theory
     and Practice with Smile, Inflation and Credit
   * Erik Schlögl (2002). Arbitrage-free interpolation in models of market observable
     interest rates. In K. Sandmann and P. Schönbucher (eds), Advances in Finance and
     Stochastics
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_path():
    """Path of the Excel input file

    :attr:`input_file` resolved against the folder that contains the model folder, so the
    default ``lmm_input.xlsx`` sits next to ``BasicLMM/``. An absolute
    :attr:`input_file` is used as it is.

    Returns:
        pathlib.Path
    """
    if _model.path is None:
        raise ValueError(
            "the model has no path yet: write it with modelx.write_model and read it "
            "back, so that the input file can be found next to the model folder")
    return _model.path.parent / input_file


def param_table():
    """Validated values from the ``Params`` sheet

    Reads the ``Params`` sheet (columns ``parameter``, ``value`` and ``description``) of
    :func:`input_path`, converts each value to its type and checks it. Raises
    ``ValueError`` listing every problem: a missing value or one of the wrong type,
    ``tenor_mth`` other than 1, 2, 3, 4, 6 or 12, ``shift`` negative or not below
    12 / ``tenor_mth``, ``maturity_size`` below ``tenor_mth``, sizes below 1, a negative
    seed, an odd ``scen_size`` with ``antithetic`` on, or a ``compounding`` other than
    ``annual`` or ``continuous``.

    Returns:
        pandas.Series indexed by parameter name, with object dtype (values are float,
        int, bool or str)
    """
    raw = pd.read_excel(input_path(), sheet_name="Params", index_col="parameter")["value"]
    kinds = {
        "shift": float, "tenor_mth": int, "maturity_size": int,
        "scen_size": int, "step_size": int, "seed": int, "antithetic": bool,
        "curve_id": str, "compounding": str, "fund_id": str}
    values, problems = {}, []
    if raw.index.duplicated().any():
        problems.append("repeated parameters: "
                        + ", ".join(sorted(set(raw.index[raw.index.duplicated()]))))
        raw = raw[~raw.index.duplicated()]
    for name, kind in kinds.items():
        v = raw.get(name)
        if v is None or (not isinstance(v, str) and pd.isna(v)):
            problems.append(f"{name} is missing")
        elif kind is str:
            values[name] = str(v).strip()
        elif kind is bool:
            text = str(v).strip().upper()
            if text in ("TRUE", "1", "1.0"):
                values[name] = True
            elif text in ("FALSE", "0", "0.0"):
                values[name] = False
            else:
                problems.append(f"{name} must be TRUE or FALSE, got {v!r}")
        elif isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, float, np.number)):
            problems.append(f"{name} must be a number, got {v!r}")
        elif kind is int and not float(v).is_integer():
            problems.append(f"{name} must be a whole number, got {v!r}")
        else:
            values[name] = kind(v)
    if not problems:
        v = values
        v["compounding"] = v["compounding"].lower()
        rules = [
            (v["tenor_mth"] in (1, 2, 3, 4, 6, 12),
             f"tenor_mth must be 1, 2, 3, 4, 6 or 12, got {v['tenor_mth']}"),
            (v["shift"] >= 0 and v["shift"] * v["tenor_mth"] < 12,
             f"shift must be >= 0 and below 12/tenor_mth, got {v['shift']}"),
            (v["maturity_size"] >= v["tenor_mth"],
             f"maturity_size must be >= tenor_mth, got {v['maturity_size']}"),
            (v["scen_size"] >= 1, f"scen_size must be >= 1, got {v['scen_size']}"),
            (v["step_size"] >= 1, f"step_size must be >= 1, got {v['step_size']}"),
            (v["seed"] >= 0, f"seed must be >= 0, got {v['seed']}"),
            (not v["antithetic"] or v["scen_size"] % 2 == 0,
             f"scen_size must be even when antithetic is TRUE, got {v['scen_size']}"),
            (v["compounding"] in ("annual", "continuous"),
             f"compounding must be annual or continuous, got {v['compounding']!r}"),
        ]
        problems = [message for ok, message in rules if not ok]
    if problems:
        raise ValueError(f"invalid Params in {input_path().name}: " + "; ".join(problems))
    return pd.Series(values, dtype=object).rename_axis("parameter")


def curve_table():
    """Spot rates from the ``Curve`` sheet

    Column ``maturity`` holds maturities in years and every other column is a curve,
    named by its curve ID. A curve ends at its last non-blank row. Raises ``ValueError``
    for maturities that are not positive and increasing, or a blank inside a curve.

    Returns:
        pandas.DataFrame indexed by ``maturity`` (years), one float column per curve ID
    """
    df = pd.read_excel(input_path(), sheet_name="Curve")
    if "maturity" not in df.columns:
        raise ValueError("the Curve sheet has no maturity column")
    mats = pd.to_numeric(df["maturity"], errors="coerce").to_numpy(dtype=float)
    rates = df.drop(columns="maturity").apply(pd.to_numeric, errors="coerce")
    problems = []
    if np.isnan(mats).any() or (mats <= 0).any():
        problems.append("maturities must be positive numbers")
    elif (np.diff(mats) <= 0).any():
        problems.append("maturities must be increasing")
    for col in rates.columns:
        filled = rates[col].notna().to_numpy()
        if not filled[:filled.sum()].all() or not filled.any():
            problems.append(f"curve {col} has a blank inside it or no values")
    if problems:
        raise ValueError(f"invalid Curve sheet in {input_path().name}: " + "; ".join(problems))
    rates.index = pd.Index(mats, name="maturity")
    return rates.astype(float)


def vol_table():
    """Volatility of the forward rates from the ``Vol`` sheet

    Column ``maturity`` holds times to expiry in years, and every other column is a
    factor. A row is the volatility vector of a forward rate with that time to expiry: its
    length is the rate's volatility, and the angle between two rows gives the correlation
    of two rates. Raises ``ValueError`` for times to expiry that are negative or not
    increasing, a sheet with no factor column, or a value that is blank or not a number.

    Returns:
        pandas.DataFrame indexed by ``maturity`` (years), one float column per factor
    """
    df = pd.read_excel(input_path(), sheet_name="Vol")
    if "maturity" not in df.columns:
        raise ValueError("the Vol sheet has no maturity column")
    mats = pd.to_numeric(df["maturity"], errors="coerce").to_numpy(dtype=float)
    loadings = df.drop(columns="maturity").apply(pd.to_numeric, errors="coerce")
    problems = []
    if len(mats) == 0 or np.isnan(mats).any() or (mats < 0).any():
        problems.append("maturities must be numbers of years, at least 0")
    elif (np.diff(mats) <= 0).any():
        problems.append("maturities must be increasing")
    if loadings.shape[1] == 0:
        problems.append("there is no factor column")
    elif loadings.isna().any().any():
        problems.append("a volatility is blank or not a number")
    if problems:
        raise ValueError(f"invalid Vol sheet in {input_path().name}: " + "; ".join(problems))
    loadings.index = pd.Index(mats, name="maturity")
    return loadings.astype(float)


def fund_table():
    """Fund shares from the ``Fund`` sheet

    Column ``maturity`` holds the years to maturity of zero-coupon bonds (a whole number
    of months), or ``cash`` for the bank account. Every other column is a fund, named by
    its fund ID, holding its shares; a blank share is 0. Raises ``ValueError`` for a
    maturity that is neither ``cash`` nor a positive whole number of months, a repeated
    maturity, a negative share, or a fund whose shares do not sum to 1 within 1e-9.

    Returns:
        pandas.DataFrame indexed by ``maturity`` (``"cash"`` or years), one float
        column per fund ID
    """
    df = pd.read_excel(input_path(), sheet_name="Fund")
    if "maturity" not in df.columns:
        raise ValueError("the Fund sheet has no maturity column")
    labels, keys, problems = [], [], []
    for v in df["maturity"]:
        if isinstance(v, str) and v.strip().lower() == "cash":
            labels.append("cash")
            keys.append("cash")
            continue
        try:
            years = float(v)
        except (TypeError, ValueError):
            years = float("nan")
        months = years * 12
        if not (years > 0 and abs(months - round(months)) < 1e-9):
            problems.append(f"maturity {v!r} is neither cash nor a positive whole number of months")
        labels.append(years)
        keys.append(round(months) if months == months else v)
    if pd.Index(keys).duplicated().any():
        problems.append("a maturity appears more than once")
    shares = df.drop(columns="maturity")
    try:
        shares = shares.apply(pd.to_numeric).fillna(0.0).astype(float)
    except (TypeError, ValueError):
        raise ValueError(f"Fund shares in {input_path().name} must be numbers or blank")
    for col in shares.columns:
        if (shares[col] < 0).any():
            problems.append(f"fund {col} has a negative share")
        if abs(shares[col].sum() - 1) > 1e-9:
            problems.append(f"shares of fund {col} sum to {shares[col].sum():.12g}, not 1")
    if problems:
        raise ValueError(f"invalid Fund sheet in {input_path().name}: " + "; ".join(problems))
    shares.index = pd.Index(labels, name="maturity", dtype=object)
    return shares


def shift():
    r"""Shift :math:`\alpha` of the forward rates, from the ``Params`` sheet

    :math:`F_k + \alpha` is lognormal, so the forward rates stay above :math:`-\alpha`. A
    shift of 0 gives the lognormal LMM.
    """
    return param_table()["shift"]


def tenor_mth():
    r"""Tenor p of the forward rates in months, from the ``Params`` sheet

    The tenor dates are :math:`T_k = t_{kp}`, and :math:`\tau = p/12` years. p is 1, 2, 3,
    4, 6 or 12, so every anniversary is a tenor date.
    """
    return param_table()["tenor_mth"]


def maturity_size():
    """Number of monthly bond maturities carried at every month, from the ``Params`` sheet

    Bonds that mature up to ``maturity_size`` months after a projection month are
    available at that month, for the fund and for yields: :func:`tenor_size` covers them.
    """
    return param_table()["maturity_size"]


def scen_size():
    """Number of stochastic scenarios N, from the ``Params`` sheet"""
    return param_table()["scen_size"]


def step_size():
    """Number of monthly steps n, from the ``Params`` sheet

    The projection runs from month 0 to month n. The forward rates cover n plus
    :func:`maturity_size` months, so the curve must reach the tenor date that ends them,
    :math:`T_K` (:func:`tenor_size`).
    """
    return param_table()["step_size"]


def seed():
    """Seed of the random number generator, from the ``Params`` sheet"""
    return param_table()["seed"]


def antithetic():
    """Whether antithetic variates are used, from the ``Params`` sheet

    If ``True``, stochastic scenario k + N/2 uses the negated random numbers of
    scenario k. See :func:`std_norm_rand`.
    """
    return param_table()["antithetic"]


def curve_id():
    """Column of the ``Curve`` sheet to use, from the ``Params`` sheet"""
    return param_table()["curve_id"]


def compounding():
    """Compounding of the input spot rates, ``"annual"`` or ``"continuous"``"""
    return param_table()["compounding"]


def fund_id():
    """Column of the ``Fund`` sheet to use, from the ``Params`` sheet"""
    return param_table()["fund_id"]


def tenor_size():
    r"""Number K of forward rates

    The smallest K with :math:`Kp \ge n + \bar{m}`, where p is :func:`tenor_mth`, n is
    :func:`step_size` and :math:`\bar{m}` is :func:`maturity_size`: the rates cover every
    bond maturity that a run needs. The curve must reach the last tenor date
    :math:`T_K`.
    """
    return -(-(step_size() + maturity_size()) // tenor_mth())


def curve_knots():
    r"""Knots of the selected initial curve

    The maturities :math:`t_k` of the curve :func:`curve_id` and the log discount
    factors :math:`\ln P^M(0, t_k) = -t_k \ln(1 + s_k)` for annually compounded spot
    rates :math:`s_k`, or :math:`-t_k s_k` for continuously compounded ones. Both arrays
    start with the knot :math:`t = 0`, :math:`\ln P^M(0, 0) = 0`.

    Raises ``ValueError`` if :func:`curve_id` is not a column of the ``Curve`` sheet, or
    if the curve ends before the last tenor date :math:`T_K` (:func:`tenor_size`). The
    curve is not extrapolated.

    Returns:
        tuple of two 1-D numpy arrays of equal length, the knot times and the log
        discount factors
    """
    table = curve_table()
    if curve_id() not in table.columns:
        raise ValueError(f"curve_id {curve_id()!r} is not a column of the Curve sheet; "
                         f"available: {', '.join(map(str, table.columns))}")
    col = table[curve_id()].dropna()
    mats = col.index.to_numpy(dtype=float)
    rates = col.to_numpy(dtype=float)
    lnp = -mats * (np.log1p(rates) if compounding() == "annual" else rates)
    last = t_(tenor_size() * tenor_mth())
    if mats[-1] < last - 1e-9:
        raise ValueError(
            f"curve {curve_id()} ends at {mats[-1]:g} years, before the last tenor date of "
            f"{last:g} years, which covers step_size ({step_size()}) plus maturity_size "
            f"({maturity_size()}) months; the curve is not extrapolated")
    return np.concatenate([[0.0], mats]), np.concatenate([[0.0], lnp])


def mkt_zcb(i):
    r"""Initial discount factor :math:`P^M(0, t_i)`

    :math:`\ln P^M(0, t)` is interpolated linearly in :math:`t` between the knots of
    :func:`curve_knots`, so instantaneous forwards are flat between knots. Raises
    ``ValueError`` for :math:`t_i` past the last maturity: the curve is not extrapolated.
    """
    knots_t, knots_lnp = curve_knots()
    t = t_(i)
    if t > knots_t[-1] + 1e-9:
        raise ValueError(
            f"maturity {t:g} years (month {i}) is past the last maturity of curve "
            f"{curve_id()} ({knots_t[-1]:g} years); the curve is not extrapolated")
    return float(np.exp(np.interp(t, knots_t, knots_lnp)))


def mkt_fwd_rates():
    r"""Initial forward rates :math:`F_k(0)`, k = 1 to K

    .. math::

        F_k(0) = \frac{1}{\tau}\left(\frac{P^M(0, T_{k-1})}{P^M(0, T_k)} - 1\right)

    Raises ``ValueError`` if a rate is not above :math:`-\alpha`, the lower bound of the
    shifted-lognormal rates, and names the shift it needs.

    Returns:
        numpy array of shape (K,)
    """
    p = tenor_mth()
    zcb = np.array([mkt_zcb(k * p) for k in range(tenor_size() + 1)])
    fwd = (zcb[:-1] / zcb[1:] - 1) / (p / 12)
    low = np.flatnonzero(fwd <= -shift())
    if len(low):
        raise ValueError(
            f"the initial forward rate F_{low[0] + 1}(0) = {fwd[low[0]]:.6g} is not above "
            f"-shift ({-shift():g}); the shift must be above {-fwd.min():.6g}")
    return fwd


def curve_adj(j):
    r"""Factor :math:`\kappa_j` that fits the bond maturing at month j to the initial curve

    For :math:`j = lp + r` with :math:`0 \le r < p` and :math:`w = r/p`:

    .. math::

        \kappa_j = \frac{P^M(0, t_j)}{(1 - w)P^M(0, T_l) + wP^M(0, T_{l+1})}

    :math:`\kappa_j` is 1 on tenor dates. On the example curves it stays within 1.5e-4 of
    1 with a tenor of 12 months.
    """
    p = tenor_mth()
    l, r = divmod(j, p)
    if r == 0:
        return 1.0
    w = r / p
    return mkt_zcb(j) / ((1 - w) * mkt_zcb(l * p) + w * mkt_zcb((l + 1) * p))


def factor_size():
    """Number d of factors, the factor columns of the ``Vol`` sheet"""
    return vol_table().shape[1]


def vol_loadings():
    r"""Volatility vectors :math:`\lambda(m)` of the forward rates by months to expiry

    Row m is the volatility vector of a forward rate with m months to its expiry at the
    start of a month, read from :func:`vol_table` at the middle of that month,
    :math:`u = (m - \frac{1}{2})/12` years: linear between the rows of the table, and flat
    before its first row. Row 0, a rate at its expiry, is 0. A rate's volatility vector is
    constant within each month, so caplet volatilities are exact sums
    (:func:`caplet_vol`).

    Raises ``ValueError`` if the table ends before the longest time to expiry of the run,
    :math:`((K-1)p - \frac{1}{2})/12` years. The table is not extrapolated.

    Returns:
        numpy array of shape ((K-1)p + 1, d)
    """
    table = vol_table()
    knots = table.index.to_numpy(dtype=float)
    u = (np.arange((tenor_size() - 1) * tenor_mth() + 1) - 0.5) * dt
    if u[-1] > knots[-1] + 1e-9:
        raise ValueError(
            f"the Vol sheet ends at {knots[-1]:g} years, before the longest time to expiry "
            f"of the run, {u[-1]:g} years; the table is not extrapolated")
    lam = np.column_stack([np.interp(u, knots, table[col].to_numpy(dtype=float))
                           for col in table.columns])
    lam[0] = 0.0
    return lam


def caplet_vol(k):
    r"""Black volatility :math:`\sigma_k` of :math:`F_k + \alpha` up to its expiry :math:`T_{k-1}`, k >= 2

    .. math::

        \sigma_k^2 T_{k-1} = \frac{1}{12}\sum_{m=1}^{(k-1)p} |\lambda(m)|^2

    A caplet on :math:`F_k` with strike :math:`x` is then worth
    :math:`\tau P^M(0, T_k)\,\mathrm{Black}(F_k(0) + \alpha, x + \alpha, \sigma_k)`.
    """
    m = (k - 1) * tenor_mth()
    if m < 1:
        raise ValueError("caplet_vol needs k >= 2: F_1 is set at time 0")
    lam = vol_loadings()[1:m + 1]
    return float(np.sqrt(dt * (lam**2).sum() / t_(m)))


def std_norm_rand():
    """Standard normal random numbers for all steps, scenarios and factors

    Drawn by ``numpy.random.default_rng(seed())`` in step-major order, so a longer
    projection leaves earlier months unchanged. With :func:`antithetic`, the first N/2
    scenarios are drawn and the rest are their negatives.

    Returns:
        numpy array of shape (n, N, d)
    """
    n, N, d = step_size(), scen_size(), factor_size()
    rng = np.random.default_rng(seed())
    if antithetic():
        half = rng.standard_normal((n, N // 2, d))
        return np.concatenate([half, -half], axis=1)
    return rng.standard_normal((n, N, d))


def fwd_rates(i):
    r"""Forward rates :math:`F_k(t_i)`, k = c+1 to K, by scenario, with :math:`c = \lfloor i/p \rfloor`

    Column 0 is :math:`F_{c+1}`, the rate of the current tenor period, set at
    :math:`T_c`. The other columns are the rates not yet set. Each month they take a
    log-Euler step, with :math:`\Delta` = :attr:`dt`, :math:`Z \sim N(0, I_d)` from
    :func:`std_norm_rand` and :math:`\lambda_k = \lambda((k-1)p - i)` from
    :func:`vol_loadings`:

    .. math::

        \ln(F_k(t_{i+1}) + \alpha) = {} & \ln(F_k(t_i) + \alpha)
        + \left(\mu_k - \tfrac{1}{2}|\lambda_k|^2\right)\Delta \\
        & + \sqrt{\Delta}\,\lambda_k \cdot Z \\
        \mu_k = {} & \lambda_k \cdot \sum_{j=c+2}^{k}
        \frac{\tau(F_j(t_i) + \alpha)}{1 + \tau F_j(t_i)}\lambda_j

    The rates stay above :math:`-\alpha`. On a tenor date, the rate of the period just
    ended is dropped. ``fwd_rates(0)`` is :func:`mkt_fwd_rates` in every scenario.

    Returns:
        numpy array of shape (N, K - c)
    """
    if i == 0:
        return np.tile(mkt_fwd_rates(), (scen_size(), 1))
    prev, h = fwd_rates(i - 1), i - 1                 # the step from month h to month i
    p, alpha = tenor_mth(), shift()
    tau = p / 12
    ks = np.arange(h // p + 2, tenor_size() + 1)       # the rates not yet set at t_h
    lam = vol_loadings()[(ks - 1) * p - h]
    alive = prev[:, 1:]
    g = tau * (alive + alpha) / (1 + tau * alive)
    drift = np.zeros_like(alive)
    for q in range(lam.shape[1]):
        drift += lam[:, q] * np.cumsum(g * lam[:, q], axis=1)
    x = (np.log(alive + alpha) + (drift - 0.5 * (lam**2).sum(axis=1)) * dt
         + np.sqrt(dt) * (std_norm_rand()[h] @ lam.T))
    stepped = np.exp(x) - alpha
    if i % p == 0:                       # the period of column 0 has ended
        return stepped
    return np.hstack([prev[:, :1], stepped])


def tenor_disc_factor(l):
    r"""Deflator :math:`D(T_l)` at the tenor date :math:`T_l`, by scenario

    .. math::

        D(T_l) = \prod_{j=1}^{l} \frac{1}{1 + \tau F_j(T_{j-1})}

    It is known at :math:`T_{l-1}`, when :math:`F_l` is set.

    Returns:
        numpy array of shape (N,)
    """
    if l == 0:
        return np.ones(scen_size())
    p = tenor_mth()
    return tenor_disc_factor(l - 1) / (1 + p / 12 * fwd_rates((l - 1) * p)[:, 0])


def defl_tenor_zcb(i, k):
    r"""Deflated price :math:`D(t_i; T_k)` of the bond maturing at the tenor date :math:`T_k`, by scenario

    For :math:`c = \lfloor i/p \rfloor \le k \le K`:

    .. math::

        D(t_i; T_k) = \frac{P(t_i, T_k)}{B_d(t_i)}
        = D(T_c)\prod_{j=c+1}^{k}\frac{1}{1 + \tau F_j(t_i)}

    where :math:`B_d` is the bank account of the spot-LIBOR measure, and
    :math:`D(T_c)` is :func:`tenor_disc_factor`. Each is a martingale, and once
    :math:`T_k` has passed it is the deflator :math:`D(T_k)`.

    Returns:
        numpy array of shape (N,)
    """
    p, K = tenor_mth(), tenor_size()
    c = i // p
    if not c <= k <= K:
        raise ValueError(f"defl_tenor_zcb({i}, {k}) needs a tenor date from T_{c}, the "
                         f"last on or before month {i}, to T_{K}")
    rates = fwd_rates(i)[:, :k - c]
    return tenor_disc_factor(c) / np.prod(1 + p / 12 * rates, axis=1)


def defl_zcb(i, j):
    r"""Deflated price :math:`D(t_i; t_j)` of the bond maturing at month :math:`j \ge i`, by scenario

    For :math:`j = lp + r` with :math:`0 \le r < p` and :math:`w = r/p`, the price is
    linear in maturity between those of the two tenor bonds, times :func:`curve_adj`:

    .. math::

        D(t_i; t_j) = \kappa_j\left[(1 - w)D(t_i; T_l) + wD(t_i; T_{l+1})\right]

    This is Schlögl's (2002) interpolation, in which a bond that matures within the
    current tenor period has no volatility. As a fixed combination of martingales, it is
    a martingale, and :math:`\kappa_j` makes it start at :math:`P^M(0, t_j)`.

    Raises ``ValueError`` for a bond that matures after :math:`T_K`: raise
    :func:`maturity_size` to carry it.

    Returns:
        numpy array of shape (N,)
    """
    p, K = tenor_mth(), tenor_size()
    l, r = divmod(j, p)
    if l + (r > 0) > K:
        raise ValueError(
            f"maturity {t_(j):g} years (month {j}) is past the last tenor date of the "
            f"forward rates, {t_(K * p):g} years; raise maturity_size (now "
            f"{maturity_size()} months) to carry it")
    if r == 0:
        return defl_tenor_zcb(i, l)
    w = r / p
    return curve_adj(j) * ((1 - w) * defl_tenor_zcb(i, l) + w * defl_tenor_zcb(i, l + 1))


def disc_factor(i):
    r"""Deflator :math:`D(t_i)`, the reciprocal of the bank account, by scenario

    The deflated price of the bond that matures at :math:`t_i`,
    :math:`D(t_i) = D(t_i; t_i)` (:func:`defl_zcb`), so that
    :math:`E[D(t_i)] = P^M(0, t_i)`.

    Returns:
        numpy array of shape (N,)
    """
    return defl_zcb(i, i)


def bank_return_mth(i):
    r"""Bank-account return :math:`R_i = D(t_i)/D(t_{i+1}) - 1` over :math:`[t_i, t_{i+1})` by scenario

    The deflated price of a bond does not change in its last month, so
    :math:`R_i = 1/P(t_i, t_{i+1}) - 1` is known at :math:`t_i`.

    Returns:
        numpy array of shape (N,)
    """
    return disc_factor(i) / disc_factor(i + 1) - 1


def P_t_T(i, j):
    r"""Zero-coupon bond price :math:`P(t_i, t_j) = D(t_i; t_j) / D(t_i)` by scenario

    Needs :math:`t_j` no later than :math:`T_K`.

    Returns:
        numpy array of shape (N,)
    """
    return defl_zcb(i, j) / disc_factor(i)


def libor_rate(i):
    r"""LIBOR rate :math:`L(t_i)`, the simply compounded rate for the tenor from :math:`t_i`, by scenario

    .. math::

        L(t_i) = \frac{1}{\tau}\left(\frac{1}{P(t_i, t_{i+p})} - 1\right)

    On a tenor date :math:`T_c` it is the rate just set, :math:`F_{c+1}(T_c)`.

    Returns:
        numpy array of shape (N,)
    """
    return (1 / P_t_T(i, i + tenor_mth()) - 1) / (tenor_mth() / 12)


def spot_rate(i, m):
    r"""Annually compounded m-month yield at :math:`t_i`, :math:`P(t_i, t_{i+m})^{-12/m} - 1`, by scenario

    Returns:
        numpy array of shape (N,)
    """
    return P_t_T(i, i + m) ** (-12 / m) - 1


def swap_rate(i, k):
    r"""k-year par rate at :math:`t_i` with an annual fixed leg, by scenario

    .. math::

        \frac{1 - P(t_i, t_i + k)}{\sum_{l=1}^{k} P(t_i, t_i + l)}

    Returns:
        numpy array of shape (N,)
    """
    annuity = sum(P_t_T(i, i + 12 * l) for l in range(1, k + 1))
    return (1 - P_t_T(i, i + 12 * k)) / annuity


def ce_disc_factor(i):
    r"""Deflator of the CE scenario, :math:`P^M(0, t_i)`"""
    return mkt_zcb(i)


def ce_bank_return_mth(i):
    r"""Bank-account return of the CE scenario, the one-month forward :math:`P^M(0, t_i)/P^M(0, t_{i+1}) - 1`"""
    return mkt_zcb(i) / mkt_zcb(i + 1) - 1


def ce_libor_rate(i):
    r"""LIBOR rate of the CE scenario, the forward :math:`(P^M(0, t_i)/P^M(0, t_{i+p}) - 1)/\tau`"""
    return (mkt_zcb(i) / mkt_zcb(i + tenor_mth()) - 1) / (tenor_mth() / 12)


def ce_spot_rate(i, m):
    r"""Annually compounded m-month yield at :math:`t_i` in the CE scenario, :math:`(P^M(0, t_i)/P^M(0, t_{i+m}))^{12/m} - 1`"""
    return (mkt_zcb(i) / mkt_zcb(i + m)) ** (12 / m) - 1


def fund_cash_share():
    """Share of the selected fund held in the bank account (0 if it has no cash row)"""
    table = fund_table()
    if fund_id() not in table.columns:
        raise ValueError(f"fund_id {fund_id()!r} is not a column of the Fund sheet; "
                         f"available: {', '.join(map(str, table.columns))}")
    col = table[fund_id()]
    return float(col["cash"]) if "cash" in col.index else 0.0


def fund_bond_shares():
    """Shares of the selected fund in zero-coupon bonds, by maturity in months

    Bonds with a zero share are left out. Their longest maturity must not exceed
    :func:`maturity_size`.

    Returns:
        pandas.Series of floats indexed by maturity in months (int)
    """
    table = fund_table()
    if fund_id() not in table.columns:
        raise ValueError(f"fund_id {fund_id()!r} is not a column of the Fund sheet; "
                         f"available: {', '.join(map(str, table.columns))}")
    col = table[fund_id()]
    bonds = col[[label != "cash" for label in col.index]]
    bonds = bonds[bonds > 0]
    months = [int(round(years * 12)) for years in bonds.index]
    return pd.Series(bonds.to_numpy(dtype=float), index=pd.Index(months, name="months"),
                     name=fund_id())


def zcb_return_mth(i, m):
    r"""Return over :math:`[t_i, t_{i+1})` of a zero-coupon bond with m months to maturity at :math:`t_i`, by scenario

    The bond is bought at :math:`t_i` and sold a month later. With :math:`T = t_{i+m}`:

    .. math::

        \frac{P(t_{i+1}, T)}{P(t_i, T)} - 1 = (1 + R_i)\frac{D(t_{i+1}; T)}{D(t_i; T)} - 1

    Returns:
        numpy array of shape (N,)
    """
    return (1 + bank_return_mth(i)) * defl_zcb(i + 1, i + m) / defl_zcb(i, i + m) - 1


def fund_return_mth(i):
    r"""Market-value return :math:`R^F_i` of the selected fund over :math:`[t_i, t_{i+1})`, by scenario

    The fund holds the bank account and zero-coupon bonds in the shares of
    :func:`fund_cash_share` and :func:`fund_bond_shares`, sells the bonds after a month
    and rebalances to the same shares:

    .. math::

        R^F_i = w_c R_i + \sum_m w_m \left[\frac{P(t_{i+1}, t_{i+m})}{P(t_i, t_{i+m})} - 1\right]

    Returns:
        numpy array of shape (N,)
    """
    ret = fund_cash_share() * bank_return_mth(i)
    for m, w in fund_bond_shares().items():
        ret = ret + w * zcb_return_mth(i, int(m))
    return ret


def scen_index():
    """Scenario IDs 0 to N, where 0 is the CE scenario

    Returns:
        pandas.RangeIndex named ``scen_id``
    """
    return pd.Index(range(scen_size() + 1), name="scen_id")


def disc_factor_paths():
    """Deflators :math:`D(t_i)` for every scenario and month

    Returns:
        numpy array of shape (N+1, n+1); row 0 is the CE scenario
    """
    n = step_size()
    ce = np.array([ce_disc_factor(i) for i in range(n + 1)])
    return np.vstack([ce, np.array([disc_factor(i) for i in range(n + 1)]).T])


def bank_return_paths():
    """Bank-account returns over :math:`[t_i, t_{i+1})` for every scenario and month

    Returns:
        numpy array of shape (N+1, n); row 0 is the CE scenario
    """
    n = step_size()
    ce = np.array([ce_bank_return_mth(i) for i in range(n)])
    return np.vstack([ce, np.array([bank_return_mth(i) for i in range(n)]).T])


def fund_return_paths():
    """Returns of the selected fund over :math:`[t_i, t_{i+1})` for every scenario and month

    In the CE scenario every bond earns the one-month forward, so row 0 is the CE
    bank-account return whatever the fund's shares.

    Returns:
        numpy array of shape (N+1, n); row 0 is the CE scenario
    """
    n = step_size()
    ce = np.array([ce_bank_return_mth(i) for i in range(n)])
    return np.vstack([ce, np.array([fund_return_mth(i) for i in range(n)]).T])


def libor_rate_paths():
    """LIBOR rates :math:`L(t_i)` for every scenario and month

    Returns:
        numpy array of shape (N+1, n+1); row 0 is the CE scenario
    """
    n = step_size()
    ce = np.array([ce_libor_rate(i) for i in range(n + 1)])
    return np.vstack([ce, np.array([libor_rate(i) for i in range(n + 1)]).T])


def spot_rate_paths(m):
    """Annually compounded m-month yields for every scenario and month

    Needs m no longer than :func:`maturity_size`.

    Returns:
        numpy array of shape (N+1, n+1); row 0 is the CE scenario
    """
    n = step_size()
    ce = np.array([ce_spot_rate(i, m) for i in range(n + 1)])
    return np.vstack([ce, np.array([spot_rate(i, m) for i in range(n + 1)]).T])


def scenario_table():
    """Deflators, returns and LIBOR rates for every scenario and month, in long format

    For inspection and export to CSV or npz. The returns over the month after
    :math:`t_n` are NaN.

    Returns:
        pandas.DataFrame indexed by (``scen_id``, ``t``) with columns ``disc_factor``,
        ``bank_return_mth``, ``fund_return_mth`` and ``libor_rate``
    """
    n = step_size()
    index = pd.MultiIndex.from_product([scen_index(), range(n + 1)], names=["scen_id", "t"])
    pad = np.full((scen_size() + 1, 1), np.nan)
    return pd.DataFrame({
        "disc_factor": disc_factor_paths().ravel(),
        "bank_return_mth": np.hstack([bank_return_paths(), pad]).ravel(),
        "fund_return_mth": np.hstack([fund_return_paths(), pad]).ravel(),
        "libor_rate": libor_rate_paths().ravel()}, index=index)


t_ = lambda i: i * dt
"""Time :math:`t_i = i/12` in years of month ``i``"""

# ---------------------------------------------------------------------------
# References

input_file = "lmm_input.xlsx"

dt = 0.08333333333333333

np = ("Module", "numpy")

pd = ("Module", "pandas")