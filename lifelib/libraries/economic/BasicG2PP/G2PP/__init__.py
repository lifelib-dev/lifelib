# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Monthly G2++ interest rate scenarios fitted to an initial curve.

The two-additive-factor Gaussian model G2++ (Brigo and Mercurio, 2nd ed. 2006, section
4.2) under the risk-neutral measure:

.. math::

    r(t) = x(t) + y(t) + \\varphi(t), \\quad
    dx(t) = -a x(t) dt + \\sigma dW_1(t), \\quad
    dy(t) = -b y(t) dt + \\eta dW_2(t), \\quad
    dW_1 dW_2 = \\rho dt

with :math:`x(0) = y(0) = 0` and :math:`\\varphi` fitted exactly to the initial curve
:math:`P^M(0, t)`. Each month, :math:`x`, :math:`y` and :math:`\\int (x + y) du` are drawn
together from their exact Gaussian transition (:func:`cov_step`), so the deflators
reproduce the initial curve up to Monte Carlo noise. Time is in years, and month ``i`` is
:math:`t_i = i/12` (:func:`t_`). N is :func:`scen_size` and n is :func:`step_size`.

**Inputs** are read at run time from the Excel file :attr:`input_file`, located next to
the model folder: sheet ``Params`` (G2++ parameters and run settings), sheet ``Curve``
(initial spot rates by maturity, one column per curve ID) and sheet ``Fund`` (shares of
bond funds by years to maturity). The initial curve is not extrapolated, so it must reach
every maturity a run needs. After editing the file in place, call ``clear_all()`` on the
model; assigning another :attr:`input_file` recalculates automatically.

**Outputs** for liability models are arrays with one row per scenario. Row 0 is the
certainty-equivalent (CE) scenario, which follows the initial forward curve, and row k
is stochastic scenario k (see :func:`scen_index`):

* :func:`disc_factor_paths`: deflators :math:`D(t_i)`, for discounting cash flows at
  :math:`t_i`
* :func:`fund_return_paths`: returns over :math:`[t_i, t_{i+1})` of the bond fund chosen
  by :func:`fund_id`
* :func:`bank_return_paths`: bank-account returns over :math:`[t_i, t_{i+1})`
* :func:`short_rate_paths`, :func:`spot_rate_paths`: short rates and yields

Attributes:

    input_file: Name of the Excel input file, relative to the folder that contains the
        model folder, or an absolute path. ``"g2pp_input.xlsx"`` by default.

    dt: Length of a monthly step in years, 1/12.

    np: The numpy module.

    pd: The pandas module.

.. seealso::

   * Damiano Brigo, Fabio Mercurio (2001, 2nd Ed. 2006). Interest Rate Models - Theory
     and Practice with Smile, Inflation and Credit
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
    default ``g2pp_input.xlsx`` sits next to ``BasicG2PP/``. An absolute
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
    ``a``, ``b`` or ``sigma`` not positive, ``eta`` negative, ``rho`` outside [-1, 1],
    sizes below 1, a negative seed, an odd ``scen_size`` with ``antithetic`` on, or a
    ``compounding`` other than ``annual`` or ``continuous``.

    Returns:
        pandas.Series indexed by parameter name, with object dtype (values are float,
        int, bool or str)
    """
    raw = pd.read_excel(input_path(), sheet_name="Params", index_col="parameter")["value"]
    kinds = {
        "a": float, "b": float, "sigma": float, "eta": float, "rho": float,
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
            (v["a"] > 0, f"a must be > 0, got {v['a']}"),
            (v["b"] > 0, f"b must be > 0, got {v['b']}"),
            (v["sigma"] > 0, f"sigma must be > 0, got {v['sigma']}"),
            (v["eta"] >= 0, f"eta must be >= 0, got {v['eta']}"),
            (-1 <= v["rho"] <= 1, f"rho must be in [-1, 1], got {v['rho']}"),
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


def a():
    r"""Mean reversion speed :math:`a` of :math:`x(t)`, from the ``Params`` sheet"""
    return param_table()["a"]


def b():
    r"""Mean reversion speed :math:`b` of :math:`y(t)`, from the ``Params`` sheet"""
    return param_table()["b"]


def sigma():
    r"""Volatility :math:`\sigma` of :math:`x(t)`, from the ``Params`` sheet"""
    return param_table()["sigma"]


def eta():
    r"""Volatility :math:`\eta` of :math:`y(t)`, from the ``Params`` sheet"""
    return param_table()["eta"]


def rho():
    r"""Correlation :math:`\rho` of :math:`W_1` and :math:`W_2`, from the ``Params`` sheet"""
    return param_table()["rho"]


def scen_size():
    """Number of stochastic scenarios N, from the ``Params`` sheet"""
    return param_table()["scen_size"]


def step_size():
    """Number of monthly steps n, from the ``Params`` sheet

    The projection runs from month 0 to month n, so :math:`t_n` = n/12 years must not be
    later than the last maturity of the curve.
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


def curve_knots():
    r"""Knots of the selected initial curve

    The maturities :math:`t_k` of the curve :func:`curve_id` and the log discount
    factors :math:`\ln P^M(0, t_k) = -t_k \ln(1 + s_k)` for annually compounded spot
    rates :math:`s_k`, or :math:`-t_k s_k` for continuously compounded ones. Both arrays
    start with the knot :math:`t = 0`, :math:`\ln P^M(0, 0) = 0`.

    Raises ``ValueError`` if :func:`curve_id` is not a column of the ``Curve`` sheet, or
    if the curve ends before the projection horizon :math:`t_n`. The curve is not
    extrapolated.

    Returns:
        tuple of two 1-D numpy arrays of equal length: knot times and log discount factors
    """
    table = curve_table()
    if curve_id() not in table.columns:
        raise ValueError(f"curve_id {curve_id()!r} is not a column of the Curve sheet; "
                         f"available: {', '.join(map(str, table.columns))}")
    col = table[curve_id()].dropna()
    mats = col.index.to_numpy(dtype=float)
    rates = col.to_numpy(dtype=float)
    lnp = -mats * (np.log1p(rates) if compounding() == "annual" else rates)
    horizon = t_(step_size())
    if mats[-1] < horizon - 1e-9:
        raise ValueError(
            f"curve {curve_id()} ends at {mats[-1]:g} years, before the projection horizon "
            f"of {horizon:g} years (step_size {step_size()}); the curve is not extrapolated")
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


def mkt_fwd(i):
    r"""Initial instantaneous forward rate :math:`f^M(0, t_i)`

    The flat forward of the knot interval :math:`[t_k, t_{k+1})` that contains
    :math:`t_i`, and of the last interval at the final knot, so no curve beyond
    :math:`t_i` is needed:

    .. math::

        f^M(0, t_i) = \frac{\ln P^M(0, t_k) - \ln P^M(0, t_{k+1})}{t_{k+1} - t_k}
    """
    knots_t, knots_lnp = curve_knots()
    t = t_(i)
    if t > knots_t[-1] + 1e-9:
        raise ValueError(
            f"maturity {t:g} years (month {i}) is past the last maturity of curve "
            f"{curve_id()} ({knots_t[-1]:g} years); the curve is not extrapolated")
    k = min(int(np.searchsorted(knots_t, t + 1e-9, side="right")) - 1, len(knots_t) - 2)
    return float((knots_lnp[k] - knots_lnp[k + 1]) / (knots_t[k + 1] - knots_t[k]))


def Ba_t_T(i, j):
    r""":math:`B_a(t_i, t_j) = (1 - e^{-a(t_j - t_i)})/a`, the loading of :math:`x(t_i)` in :math:`\ln P(t_i, t_j)`"""
    tau = t_(j) - t_(i)
    return -np.expm1(-a() * tau) / a()


def Bb_t_T(i, j):
    r""":math:`B_b(t_i, t_j) = (1 - e^{-b(t_j - t_i)})/b`, the loading of :math:`y(t_i)` in :math:`\ln P(t_i, t_j)`"""
    tau = t_(j) - t_(i)
    return -np.expm1(-b() * tau) / b()


def V_t_T(i, j):
    r"""Variance :math:`V(t_i, t_j)` of :math:`\int_{t_i}^{t_j} (x(u) + y(u)) du` given :math:`\mathcal{F}_{t_i}`

    With :math:`\tau = t_j - t_i` (Brigo and Mercurio, section 4.2):

    .. math::

        V(t, T) = \frac{\sigma^2}{a^2}\left[\tau + \frac{2}{a}e^{-a\tau}
        - \frac{1}{2a}e^{-2a\tau} - \frac{3}{2a}\right]
        + \frac{\eta^2}{b^2}\left[\tau + \frac{2}{b}e^{-b\tau}
        - \frac{1}{2b}e^{-2b\tau} - \frac{3}{2b}\right]
        + \frac{2\rho\sigma\eta}{ab}\left[\tau + \frac{e^{-a\tau} - 1}{a}
        + \frac{e^{-b\tau} - 1}{b} - \frac{e^{-(a+b)\tau} - 1}{a + b}\right]

    Computed with ``expm1``, which keeps the digits that :math:`e^{-a\tau} - 1` loses for
    small :math:`\tau`.
    """
    tau = t_(j) - t_(i)
    a_, b_, s, e, r = a(), b(), sigma(), eta(), rho()
    return (s**2 / a_**2 * (tau + 2 / a_ * np.expm1(-a_ * tau) - np.expm1(-2 * a_ * tau) / (2 * a_))
            + e**2 / b_**2 * (tau + 2 / b_ * np.expm1(-b_ * tau) - np.expm1(-2 * b_ * tau) / (2 * b_))
            + 2 * r * s * e / (a_ * b_) * (tau + np.expm1(-a_ * tau) / a_ + np.expm1(-b_ * tau) / b_
                                           - np.expm1(-(a_ + b_) * tau) / (a_ + b_)))


def phi(i):
    r"""Deterministic shift :math:`\varphi(t_i)` that fits the model to the initial curve

    .. math::

        \varphi(t) = f^M(0, t) + \frac{\sigma^2}{2a^2}(1 - e^{-at})^2
        + \frac{\eta^2}{2b^2}(1 - e^{-bt})^2
        + \frac{\rho\sigma\eta}{ab}(1 - e^{-at})(1 - e^{-bt})
    """
    t = t_(i)
    a_, b_, s, e, r = a(), b(), sigma(), eta(), rho()
    ua, ub = -np.expm1(-a_ * t), -np.expm1(-b_ * t)
    return (mkt_fwd(i) + s**2 / (2 * a_**2) * ua**2 + e**2 / (2 * b_**2) * ub**2
            + r * s * e / (a_ * b_) * ua * ub)


def E_rt():
    r"""Expected short rates :math:`E[r(t_i)] = \varphi(t_i)` for i = 0 to n

    Returns:
        numpy array of shape (n+1,)
    """
    return np.array([phi(i) for i in range(step_size() + 1)])


def Var_rt():
    r"""Variances of the short rates :math:`r(t_i)` for i = 0 to n

    .. math::

        \mathrm{Var}[r(t)] = \frac{\sigma^2}{2a}(1 - e^{-2at}) + \frac{\eta^2}{2b}(1 - e^{-2bt})
        + \frac{2\rho\sigma\eta}{a + b}(1 - e^{-(a+b)t})

    Returns:
        numpy array of shape (n+1,)
    """
    t = np.arange(step_size() + 1) * dt
    a_, b_, s, e, r = a(), b(), sigma(), eta(), rho()
    return (s**2 / (2 * a_) * -np.expm1(-2 * a_ * t) + e**2 / (2 * b_) * -np.expm1(-2 * b_ * t)
            + 2 * r * s * e / (a_ + b_) * -np.expm1(-(a_ + b_) * t))


def fund_logvar(j):
    r"""Variance :math:`s^2` of :math:`\ln(AV(t_j)/AV_0)` for the selected fund

    Used by the closed-form GMAB value of CashValue_ME_G2PP,
    :func:`~economic.CashValue_ME_G2PP.Projection.formula_gmab_g2pp`. For an all-cash fund,
    :math:`AV(t_j)/AV_0 = 1/D(t_j)` and :math:`s^2 = V(0, t_j)`. For a fund that holds a
    single maturity :math:`\tau`, the monthly log return is linear in :math:`x` and
    :math:`y` (see :func:`zcb_return_mth`), and :math:`s^2` follows from a covariance
    recursion for :math:`(x, y, \ln AV)` over the months. Raises ``ValueError`` for
    other funds, which have no exact closed form.
    """
    cash, bonds = fund_cash_share(), fund_bond_shares()
    if len(bonds) == 0:
        return V_t_T(0, j)
    if cash > 0 or len(bonds) > 1:
        raise ValueError(f"fund_logvar needs an all-cash or single-maturity fund; "
                         f"fund {fund_id()} has several holdings")
    m = int(bonds.index[0])
    ea, eb = np.exp(-a() * dt), np.exp(-b() * dt)
    al, be = Ba_t_T(0, m), Bb_t_T(0, m)
    al1, be1 = Ba_t_T(0, m - 1), Bb_t_T(0, m - 1)
    trans = np.array([[ea, 0.0, 0.0], [0.0, eb, 0.0], [al - al1 * ea, be - be1 * eb, 1.0]])
    load = np.array([[1.0, 0.0], [0.0, 1.0], [-al1, -be1]])
    noise = load @ cov_step()[:2, :2] @ load.T
    cov = np.zeros((3, 3))
    for _ in range(j):
        cov = trans @ cov @ trans.T + noise
    return float(cov[2, 2])


def std_norm_rand():
    """Standard normal random numbers for all steps and scenarios

    Drawn by ``numpy.random.default_rng(seed())`` in step-major order, so a longer
    projection leaves earlier months unchanged. With :func:`antithetic`, the first N/2
    scenarios are drawn and the rest are their negatives.

    Returns:
        numpy array of shape (n, N, 3)
    """
    n, N = step_size(), scen_size()
    rng = np.random.default_rng(seed())
    if antithetic():
        half = rng.standard_normal((n, N // 2, 3))
        return np.concatenate([half, -half], axis=1)
    return rng.standard_normal((n, N, 3))


def cov_step():
    r"""Covariance :math:`C` of one exact monthly step

    The covariance of :math:`x(t+\Delta)`, :math:`y(t+\Delta)` and
    :math:`\int_t^{t+\Delta}(x + y)du` given :math:`\mathcal{F}_t`, with :math:`\Delta`
    = :attr:`dt`. It does not depend on :math:`t`:

    .. math::

        C_{11} = \frac{\sigma^2}{2a}(1 - e^{-2a\Delta}), \quad
        C_{22} = \frac{\eta^2}{2b}(1 - e^{-2b\Delta}), \quad
        C_{12} = \frac{\rho\sigma\eta}{a + b}(1 - e^{-(a+b)\Delta})

        C_{13} = \frac{\sigma^2}{2a^2}(1 - e^{-a\Delta})^2
        + \frac{\rho\sigma\eta}{b}\left[\frac{1 - e^{-a\Delta}}{a}
        - \frac{1 - e^{-(a+b)\Delta}}{a + b}\right]

        C_{23} = \frac{\eta^2}{2b^2}(1 - e^{-b\Delta})^2
        + \frac{\rho\sigma\eta}{a}\left[\frac{1 - e^{-b\Delta}}{b}
        - \frac{1 - e^{-(a+b)\Delta}}{a + b}\right]

        C_{33} = V(t, t + \Delta)

    Returns:
        numpy array of shape (3, 3)
    """
    a_, b_, s, e, r = a(), b(), sigma(), eta(), rho()
    ua, ub, uab = -np.expm1(-a_ * dt), -np.expm1(-b_ * dt), -np.expm1(-(a_ + b_) * dt)
    c11 = s**2 * -np.expm1(-2 * a_ * dt) / (2 * a_)
    c22 = e**2 * -np.expm1(-2 * b_ * dt) / (2 * b_)
    c12 = r * s * e * uab / (a_ + b_)
    c13 = s**2 * ua**2 / (2 * a_**2) + r * s * e / b_ * (ua / a_ - uab / (a_ + b_))
    c23 = e**2 * ub**2 / (2 * b_**2) + r * s * e / a_ * (ub / b_ - uab / (a_ + b_))
    c33 = V_t_T(0, 1)
    return np.array([[c11, c12, c13], [c12, c22, c23], [c13, c23, c33]])


def chol_step():
    r"""Square root :math:`L` of :func:`cov_step`, with :math:`LL^T = C`

    The Cholesky factor, or a symmetric square root from ``numpy.linalg.eigh`` when
    :math:`C` is singular, for example when :math:`\eta = 0`.

    Returns:
        numpy array of shape (3, 3)
    """
    cov = cov_step()
    try:
        return np.linalg.cholesky(cov)
    except np.linalg.LinAlgError:
        w, v = np.linalg.eigh(cov)
        return v @ np.diag(np.sqrt(np.clip(w, 0, None))) @ v.T


def shocks(i):
    r"""Correlated shocks :math:`(\varepsilon_1, \varepsilon_2, \varepsilon_3)` of the step from month i to i+1

    :math:`\varepsilon = L z` with :math:`L` = :func:`chol_step` and :math:`z` the
    random numbers of :func:`std_norm_rand` for step i.

    Returns:
        numpy array of shape (N, 3)
    """
    return std_norm_rand()[i] @ chol_step().T


def x(i):
    r"""Factor :math:`x(t_i)` by scenario

    :math:`x(0) = 0` and :math:`x(t_{i+1}) = x(t_i)e^{-a\Delta} + \varepsilon_1`.

    Returns:
        numpy array of shape (N,)
    """
    if i == 0:
        return np.zeros(scen_size())
    return x(i - 1) * np.exp(-a() * dt) + shocks(i - 1)[:, 0]


def y(i):
    r"""Factor :math:`y(t_i)` by scenario

    :math:`y(0) = 0` and :math:`y(t_{i+1}) = y(t_i)e^{-b\Delta} + \varepsilon_2`.

    Returns:
        numpy array of shape (N,)
    """
    if i == 0:
        return np.zeros(scen_size())
    return y(i - 1) * np.exp(-b() * dt) + shocks(i - 1)[:, 1]


def accum_xy(i):
    r"""Integrated factors :math:`A(t_i) = \int_0^{t_i}(x(u) + y(u))du` by scenario

    :math:`A(t_{i+1}) = A(t_i) + B_a(\Delta)x(t_i) + B_b(\Delta)y(t_i) + \varepsilon_3`,
    which is exact for the monthly step.

    Returns:
        numpy array of shape (N,)
    """
    if i == 0:
        return np.zeros(scen_size())
    return accum_xy(i - 1) + Ba_t_T(0, 1) * x(i - 1) + Bb_t_T(0, 1) * y(i - 1) + shocks(i - 1)[:, 2]


def short_rate(i):
    r"""Short rate :math:`r(t_i) = x(t_i) + y(t_i) + \varphi(t_i)` by scenario

    Returns:
        numpy array of shape (N,)
    """
    return x(i) + y(i) + phi(i)


def disc_factor(i):
    r"""Deflator :math:`D(t_i)`, the reciprocal of the bank account, by scenario

    .. math::

        D(t_i) = P^M(0, t_i)\exp\left(-\tfrac{1}{2}V(0, t_i) - A(t_i)\right)

    so that :math:`E[D(t_i)] = P^M(0, t_i)`.

    Returns:
        numpy array of shape (N,)
    """
    return mkt_zcb(i) * np.exp(-0.5 * V_t_T(0, i) - accum_xy(i))


def bank_return_mth(i):
    r"""Bank-account return :math:`R_i = D(t_i)/D(t_{i+1}) - 1` over :math:`[t_i, t_{i+1})` by scenario

    Returns:
        numpy array of shape (N,)
    """
    return disc_factor(i) / disc_factor(i + 1) - 1


def P_t_T(i, j):
    r"""Zero-coupon bond price :math:`P(t_i, t_j)` by scenario

    .. math::

        P(t, T) = \frac{P^M(0, T)}{P^M(0, t)}
        \exp\left(\tfrac{1}{2}[V(t, T) - V(0, T) + V(0, t)]
        - B_a(t, T)x(t) - B_b(t, T)y(t)\right)

    Needs the curve out to :math:`t_j`.

    Returns:
        numpy array of shape (N,)
    """
    return (mkt_zcb(j) / mkt_zcb(i)
            * np.exp(0.5 * (V_t_T(i, j) - V_t_T(0, j) + V_t_T(0, i))
                     - Ba_t_T(i, j) * x(i) - Bb_t_T(i, j) * y(i)))


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


def ce_short_rate(i):
    r"""Short rate of the CE scenario, the initial forward :math:`f^M(0, t_i)`"""
    return mkt_fwd(i)


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

    Bonds with a zero share are left out.

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

        \ln\frac{P(t_{i+1}, T)}{P(t_i, T)} = \ln P^M(0, t_i) - \ln P^M(0, t_{i+1})
        + \tfrac{1}{2}[V(t_{i+1}, T) - V(t_i, T) + V(0, t_{i+1}) - V(0, t_i)]
        - B_a(t_{i+1}, T)x(t_{i+1}) - B_b(t_{i+1}, T)y(t_{i+1})
        + B_a(t_i, T)x(t_i) + B_b(t_i, T)y(t_i)

    :math:`P^M(0, T)` cancels, so the return needs the curve only up to
    :math:`t_{i+1}`.

    Returns:
        numpy array of shape (N,)
    """
    j = i + m
    ln_ret = (np.log(mkt_zcb(i)) - np.log(mkt_zcb(i + 1))
              + 0.5 * (V_t_T(i + 1, j) - V_t_T(i, j) + V_t_T(0, i + 1) - V_t_T(0, i))
              - Ba_t_T(i + 1, j) * x(i + 1) - Bb_t_T(i + 1, j) * y(i + 1)
              + Ba_t_T(i, j) * x(i) + Bb_t_T(i, j) * y(i))
    return np.expm1(ln_ret)


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


def short_rate_paths():
    """Short rates :math:`r(t_i)` for every scenario and month

    Returns:
        numpy array of shape (N+1, n+1); row 0 is the CE scenario
    """
    n = step_size()
    ce = np.array([ce_short_rate(i) for i in range(n + 1)])
    return np.vstack([ce, np.array([short_rate(i) for i in range(n + 1)]).T])


def spot_rate_paths(m):
    """Annually compounded m-month yields for every scenario and month

    Needs the curve out to :math:`t_{n+m}`.

    Returns:
        numpy array of shape (N+1, n+1); row 0 is the CE scenario
    """
    n = step_size()
    ce = np.array([ce_spot_rate(i, m) for i in range(n + 1)])
    return np.vstack([ce, np.array([spot_rate(i, m) for i in range(n + 1)]).T])


def scenario_table():
    """Deflators, returns and short rates for every scenario and month, in long format

    For inspection and export to CSV or npz. The returns over the month after
    :math:`t_n` are NaN.

    Returns:
        pandas.DataFrame indexed by (``scen_id``, ``t``) with columns ``disc_factor``,
        ``bank_return_mth``, ``fund_return_mth`` and ``short_rate``
    """
    n = step_size()
    index = pd.MultiIndex.from_product([scen_index(), range(n + 1)], names=["scen_id", "t"])
    pad = np.full((scen_size() + 1, 1), np.nan)
    return pd.DataFrame({
        "disc_factor": disc_factor_paths().ravel(),
        "bank_return_mth": np.hstack([bank_return_paths(), pad]).ravel(),
        "fund_return_mth": np.hstack([fund_return_paths(), pad]).ravel(),
        "short_rate": short_rate_paths().ravel()}, index=index)


t_ = lambda i: i * dt
"""Time :math:`t_i = i/12` in years of month ``i``"""

# ---------------------------------------------------------------------------
# References

input_file = "g2pp_input.xlsx"

dt = 0.08333333333333333

np = ("Module", "numpy")

pd = ("Module", "pandas")