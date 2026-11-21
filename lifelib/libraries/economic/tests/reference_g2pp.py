"""Pure-numpy reference implementation of the G2++ scenario generator.

It implements section 4 of the design note, ``_research/g2pp_design.md``, without modelx.
The tests run it with the same inputs and seed as BasicG2PP and require the two to agree
to 1e-12. Formulas use ``expm1`` where the textbook form ``1 - exp(-x)`` loses digits for
small x, exactly as the model does.

Notation follows Brigo and Mercurio (2nd ed. 2006), section 4.2: r = x + y + phi,
dx = -a x dt + sigma dW1, dy = -b y dt + eta dW2, dW1 dW2 = rho dt, on a monthly grid
t_i = i * DT.
"""
import numpy as np
import pandas as pd

DT = 1 / 12


def read_inputs(path):
    """Read a g2pp_input.xlsx workbook into keyword arguments of :class:`ReferenceG2PP`.

    Only parses; the model is responsible for validation.
    """
    params = pd.read_excel(path, sheet_name="Params", index_col="parameter")["value"]
    curve = pd.read_excel(path, sheet_name="Curve", index_col="maturity")
    curve = curve[params["curve_id"]].dropna()
    fund = pd.read_excel(path, sheet_name="Fund", index_col="maturity")[params["fund_id"]]
    cash, bonds = 0.0, {}
    for label, share in fund.fillna(0.0).items():
        if isinstance(label, str) and label.strip().lower() == "cash":
            cash = float(share)
        elif share > 0:
            bonds[int(round(float(label) * 12))] = float(share)
    return dict(
        a=params["a"], b=params["b"], sigma=params["sigma"], eta=params["eta"],
        rho=params["rho"], maturities=curve.index.to_numpy(dtype=float),
        spot_rates=curve.to_numpy(dtype=float), compounding=params["compounding"],
        scen_size=params["scen_size"], step_size=params["step_size"], seed=params["seed"],
        antithetic=bool(params["antithetic"]), fund_cash=cash, fund_bonds=bonds,
    )


class ReferenceG2PP:
    """G2++ scenarios with exact monthly steps, computed with plain numpy arrays.

    Arrays indexed by month have the month as the first axis: ``x[i]`` is x(t_i) for all
    N stochastic scenarios. The ``*_paths`` methods return (N+1, ...) arrays whose row 0
    is the certainty-equivalent (CE) scenario, like the model's outputs.
    """

    def __init__(self, *, a, b, sigma, eta, rho, maturities, spot_rates,
                 compounding="annual", scen_size=1000, step_size=600, seed=1234,
                 antithetic=True, fund_cash=1.0, fund_bonds=None):
        self.a, self.b = float(a), float(b)
        self.sigma, self.eta, self.rho = float(sigma), float(eta), float(rho)
        self.N, self.n = int(scen_size), int(step_size)
        self.seed, self.antithetic = int(seed), bool(antithetic)
        mats = np.asarray(maturities, dtype=float)
        rates = np.asarray(spot_rates, dtype=float)
        lnp = -mats * (np.log1p(rates) if compounding == "annual" else rates)
        self.knots_t = np.concatenate([[0.0], mats])
        self.knots_lnp = np.concatenate([[0.0], lnp])
        self.fund_cash = float(fund_cash)
        self.fund_bonds = dict(fund_bonds or {})
        self._sim = None

    # ---- time grid and initial curve ------------------------------------------------
    @staticmethod
    def t(i):
        return np.asarray(i) * DT

    def mkt_zcb(self, i):
        """P^M(0, t_i), log-linear between knots, no extrapolation."""
        t = self.t(i)
        if np.any(t > self.knots_t[-1] + 1e-9):
            raise ValueError("maturity past the last knot of the curve")
        return np.exp(np.interp(t, self.knots_t, self.knots_lnp))

    def mkt_fwd(self, i):
        """Flat forward of the knot interval containing t_i (last interval at the end)."""
        t = self.t(i)
        if np.any(t > self.knots_t[-1] + 1e-9):
            raise ValueError("maturity past the last knot of the curve")
        k = np.minimum(np.searchsorted(self.knots_t, t + 1e-9, side="right") - 1,
                       len(self.knots_t) - 2)
        return (self.knots_lnp[k] - self.knots_lnp[k + 1]) / (self.knots_t[k + 1] - self.knots_t[k])

    # ---- closed forms ---------------------------------------------------------------
    def Ba(self, tau):
        return -np.expm1(-self.a * tau) / self.a

    def Bb(self, tau):
        return -np.expm1(-self.b * tau) / self.b

    def V(self, tau):
        """V(t, t + tau), the variance of the integral of x + y over tau years."""
        a, b, s, e, r = self.a, self.b, self.sigma, self.eta, self.rho
        return (s**2 / a**2 * (tau + 2 / a * np.expm1(-a * tau) - np.expm1(-2 * a * tau) / (2 * a))
                + e**2 / b**2 * (tau + 2 / b * np.expm1(-b * tau) - np.expm1(-2 * b * tau) / (2 * b))
                + 2 * r * s * e / (a * b) * (tau + np.expm1(-a * tau) / a + np.expm1(-b * tau) / b
                                             - np.expm1(-(a + b) * tau) / (a + b)))

    def phi(self, i):
        t = self.t(i)
        a, b, s, e, r = self.a, self.b, self.sigma, self.eta, self.rho
        ua, ub = -np.expm1(-a * t), -np.expm1(-b * t)
        return (self.mkt_fwd(i) + s**2 / (2 * a**2) * ua**2 + e**2 / (2 * b**2) * ub**2
                + r * s * e / (a * b) * ua * ub)

    def var_r(self, i):
        t = self.t(i)
        a, b, s, e, r = self.a, self.b, self.sigma, self.eta, self.rho
        return (s**2 / (2 * a) * -np.expm1(-2 * a * t) + e**2 / (2 * b) * -np.expm1(-2 * b * t)
                + 2 * r * s * e / (a + b) * -np.expm1(-(a + b) * t))

    def cov_step(self):
        """Covariance C of (x(t+DT), y(t+DT), integral of x + y) given time t."""
        a, b, s, e, r = self.a, self.b, self.sigma, self.eta, self.rho
        ua, ub, uab = -np.expm1(-a * DT), -np.expm1(-b * DT), -np.expm1(-(a + b) * DT)
        c11 = s**2 * -np.expm1(-2 * a * DT) / (2 * a)
        c22 = e**2 * -np.expm1(-2 * b * DT) / (2 * b)
        c12 = r * s * e * uab / (a + b)
        c13 = s**2 * ua**2 / (2 * a**2) + r * s * e / b * (ua / a - uab / (a + b))
        c23 = e**2 * ub**2 / (2 * b**2) + r * s * e / a * (ub / b - uab / (a + b))
        c33 = self.V(DT)
        return np.array([[c11, c12, c13], [c12, c22, c23], [c13, c23, c33]])

    def chol_step(self):
        cov = self.cov_step()
        try:
            return np.linalg.cholesky(cov)
        except np.linalg.LinAlgError:
            w, v = np.linalg.eigh(cov)
            return v @ np.diag(np.sqrt(np.clip(w, 0, None))) @ v.T

    def normals(self):
        rng = np.random.default_rng(self.seed)
        if self.antithetic:
            half = rng.standard_normal((self.n, self.N // 2, 3))
            return np.concatenate([half, -half], axis=1)
        return rng.standard_normal((self.n, self.N, 3))

    # ---- simulation -----------------------------------------------------------------
    def simulate(self):
        if self._sim is not None:
            return self._sim
        n, N = self.n, self.N
        z, L = self.normals(), self.chol_step()
        ea, eb = np.exp(-self.a * DT), np.exp(-self.b * DT)
        ba1, bb1 = self.Ba(DT), self.Bb(DT)
        x, y, A = np.zeros((n + 1, N)), np.zeros((n + 1, N)), np.zeros((n + 1, N))
        for i in range(n):
            e = z[i] @ L.T
            x[i + 1] = x[i] * ea + e[:, 0]
            y[i + 1] = y[i] * eb + e[:, 1]
            A[i + 1] = A[i] + ba1 * x[i] + bb1 * y[i] + e[:, 2]
        steps = np.arange(n + 1)
        D = self.mkt_zcb(steps)[:, None] * np.exp(-0.5 * self.V(self.t(steps))[:, None] - A)
        R = D[:-1] / D[1:] - 1
        r = x + y + self.phi(steps)[:, None]
        self._sim = dict(x=x, y=y, A=A, D=D, R=R, r=r)
        F = self.fund_cash * R
        for m, w in self.fund_bonds.items():
            F = F + w * self.zcb_return(m)
        self._sim["F"] = F
        return self._sim

    def zcb_return(self, m):
        """(n, N) returns over [t_i, t_{i+1}) of zeros with m months to maturity at t_i.

        Uses the cancelled formula of the design note's section 4, which needs no curve
        beyond t_n.
        """
        sim = self.simulate()
        x, y = sim["x"], sim["y"]
        i = np.arange(self.n)
        ti, ti1, T = self.t(i), self.t(i + 1), self.t(i + m)
        lnp = np.log(self.mkt_zcb(np.arange(self.n + 1)))
        det = (lnp[:-1] - lnp[1:]
               + 0.5 * (self.V(T - ti1) - self.V(T - ti) + self.V(ti1) - self.V(ti)))
        ln_ret = (det[:, None]
                  - self.Ba(T - ti1)[:, None] * x[1:] - self.Bb(T - ti1)[:, None] * y[1:]
                  + self.Ba(T - ti)[:, None] * x[:-1] + self.Bb(T - ti)[:, None] * y[:-1])
        return np.expm1(ln_ret)

    def P(self, i, j):
        """P(t_i, t_j) for each stochastic scenario (Brigo and Mercurio, with the curve fit)."""
        sim = self.simulate()
        ti, tj = self.t(i), self.t(j)
        return (self.mkt_zcb(j) / self.mkt_zcb(i)
                * np.exp(0.5 * (self.V(tj - ti) - self.V(tj) + self.V(ti))
                         - self.Ba(tj - ti) * sim["x"][i] - self.Bb(tj - ti) * sim["y"][i]))

    def swap_rate(self, i, k):
        annuity = sum(self.P(i, i + 12 * l) for l in range(1, k + 1))
        return (1 - self.P(i, i + 12 * k)) / annuity

    def fund_logvar(self, j):
        """Var[ln(AV(t_j)/AV0)] for an all-cash or single-maturity fund.

        Computed as a quadratic form in the Gaussian vector (x(t_k), y(t_k)), k = 0..j,
        independently of the model's covariance recursion.
        """
        if not self.fund_bonds:
            return float(self.V(self.t(j)))
        if self.fund_cash > 0 or len(self.fund_bonds) > 1:
            raise ValueError("no closed form for a fund with several maturities")
        (m, _), = self.fund_bonds.items()
        a, b, s, e, r = self.a, self.b, self.sigma, self.eta, self.rho
        tk = self.t(np.arange(j + 1))
        S, T = np.meshgrid(tk, tk, indexing="ij")
        mn = np.minimum(S, T)
        cxx = s**2 / (2 * a) * (np.exp(-a * np.abs(S - T)) - np.exp(-a * (S + T)))
        cyy = e**2 / (2 * b) * (np.exp(-b * np.abs(S - T)) - np.exp(-b * (S + T)))
        cxy = r * s * e / (a + b) * (np.exp(-a * (S - mn) - b * (T - mn)) - np.exp(-a * S - b * T))
        cov = np.block([[cxx, cxy], [cxy.T, cyy]])
        k = np.arange(j + 1)
        tau, tau1 = self.t(m), self.t(m - 1)
        hx = self.Ba(tau) * (k < j) - self.Ba(tau1) * (k >= 1)
        hy = self.Bb(tau) * (k < j) - self.Bb(tau1) * (k >= 1)
        h = np.concatenate([hx, hy])
        return float(h @ cov @ h)

    # ---- outputs with the CE scenario as row 0 ----------------------------------------
    def disc_factor_paths(self):
        ce = self.mkt_zcb(np.arange(self.n + 1))
        return np.vstack([ce, self.simulate()["D"].T])

    def ce_bank_returns(self):
        p = self.mkt_zcb(np.arange(self.n + 1))
        return p[:-1] / p[1:] - 1

    def bank_return_paths(self):
        return np.vstack([self.ce_bank_returns(), self.simulate()["R"].T])

    def fund_return_paths(self):
        return np.vstack([self.ce_bank_returns(), self.simulate()["F"].T])

    def short_rate_paths(self):
        ce = self.mkt_fwd(np.arange(self.n + 1))
        return np.vstack([ce, self.simulate()["r"].T])

    def spot_rate_paths(self, m):
        i = np.arange(self.n + 1)
        ce = (self.mkt_zcb(i) / self.mkt_zcb(i + m)) ** (12 / m) - 1
        sto = np.array([self.P(k, k + m) ** (-12 / m) - 1 for k in i])
        return np.vstack([ce, sto.T])
