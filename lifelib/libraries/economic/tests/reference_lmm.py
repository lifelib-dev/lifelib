"""Pure-numpy reference implementation of the LMM scenario generator.

It implements section 4 of the design note, ``_research/lmm_design.md``, without modelx.
The tests run it with the same inputs and seed as BasicLMM and require the two to agree to
1e-10.

Notation follows Brigo and Mercurio (2nd ed. 2006), chapter 6, with the shift of their
section 10.1. The forward rate F_k covers the period (T_{k-1}, T_k] between the tenor
dates T_k = k * tenor_mth months, F_k + shift is lognormal, and the rates move under the
spot-LIBOR measure by a log-Euler step on the monthly grid t_i = i * DT. A bond that
matures between two tenor dates has a deflated price linear in maturity between those of
the two tenor bonds (Schlögl 2002), times a factor that fits the initial curve.
"""
import numpy as np
import pandas as pd
from scipy import stats

DT = 1 / 12


def read_inputs(path):
    """Read an lmm_input.xlsx workbook into keyword arguments of :class:`ReferenceLMM`.

    Only parses; the model is responsible for validation.
    """
    params = pd.read_excel(path, sheet_name="Params", index_col="parameter")["value"]
    curve = pd.read_excel(path, sheet_name="Curve", index_col="maturity")
    curve = curve[params["curve_id"]].dropna()
    vol = pd.read_excel(path, sheet_name="Vol", index_col="maturity")
    fund = pd.read_excel(path, sheet_name="Fund", index_col="maturity")[params["fund_id"]]
    cash, bonds = 0.0, {}
    for label, share in fund.fillna(0.0).items():
        if isinstance(label, str) and label.strip().lower() == "cash":
            cash = float(share)
        elif share > 0:
            bonds[int(round(float(label) * 12))] = float(share)
    return dict(
        shift=params["shift"], tenor_mth=params["tenor_mth"],
        maturity_size=params["maturity_size"], maturities=curve.index.to_numpy(dtype=float),
        spot_rates=curve.to_numpy(dtype=float), compounding=params["compounding"],
        vol_maturities=vol.index.to_numpy(dtype=float), vol_table=vol.to_numpy(dtype=float),
        scen_size=params["scen_size"], step_size=params["step_size"], seed=params["seed"],
        antithetic=bool(params["antithetic"]), fund_cash=cash, fund_bonds=bonds,
    )


def black(forward, strike, total_vol):
    """Undiscounted Black price of a call, with total volatility sigma * sqrt(T)."""
    d1 = (np.log(forward / strike) + total_vol**2 / 2) / total_vol
    return forward * stats.norm.cdf(d1) - strike * stats.norm.cdf(d1 - total_vol)


class ReferenceLMM:
    """LMM scenarios on a monthly grid, computed with plain numpy arrays.

    The state at month i is an (N, K) array of all the forward rates, ``F[:, k - 1]`` being
    F_k(t_i); a rate keeps its value once it is set. Arrays indexed by month have the month
    as the first axis: ``D[i]`` is D(t_i) for all N stochastic scenarios. The ``*_paths``
    methods return (N+1, ...) arrays whose row 0 is the certainty-equivalent (CE) scenario,
    like the model's outputs.

    ``keep`` adds bond maturities, in months from each month, whose deflated prices are
    kept for every month, and ``snapshots`` the months at which the whole state is kept.
    """

    def __init__(self, *, shift, tenor_mth, maturity_size, maturities, spot_rates,
                 vol_maturities, vol_table, compounding="annual", scen_size=1000,
                 step_size=600, seed=1234, antithetic=True, fund_cash=1.0, fund_bonds=None,
                 keep=(), snapshots=()):
        self.alpha, self.p = float(shift), int(tenor_mth)
        self.tau = self.p / 12
        self.mbar = int(maturity_size)
        self.N, self.n = int(scen_size), int(step_size)
        self.seed, self.antithetic = int(seed), bool(antithetic)
        self.K = -(-(self.n + self.mbar) // self.p)                  # number of forward rates
        mats = np.asarray(maturities, dtype=float)
        rates = np.asarray(spot_rates, dtype=float)
        lnp = -mats * (np.log1p(rates) if compounding == "annual" else rates)
        self.knots_t = np.concatenate([[0.0], mats])
        self.knots_lnp = np.concatenate([[0.0], lnp])
        self.P0 = self.mkt_zcb(np.arange(self.K + 1) * self.p)      # P^M(0, T_k), k = 0..K
        self.F0 = (self.P0[:-1] / self.P0[1:] - 1) / self.tau        # F_k(0), k = 1..K
        vol_t = np.asarray(vol_maturities, dtype=float)
        vol_f = np.asarray(vol_table, dtype=float).reshape(len(vol_t), -1)
        u = (np.arange((self.K - 1) * self.p + 1) - 0.5) * DT        # mid-month time to expiry
        if u[-1] > vol_t[-1] + 1e-9:
            raise ValueError("the volatility table ends before the longest time to expiry")
        self.lam = np.column_stack([np.interp(u, vol_t, vol_f[:, q])
                                    for q in range(vol_f.shape[1])])
        self.lam[0] = 0.0                                             # a rate at its expiry
        self.d = self.lam.shape[1]
        self.fund_cash = float(fund_cash)
        self.fund_bonds = dict(fund_bonds or {})
        self.keep = sorted({0, 1, self.p, *keep, *self.fund_bonds,
                            *(m - 1 for m in self.fund_bonds)})
        self.snapshots = set(snapshots)
        self._sim = None

    # ---- initial curve ---------------------------------------------------------------
    @staticmethod
    def t(i):
        return np.asarray(i) * DT

    def mkt_zcb(self, i):
        """P^M(0, t_i), log-linear between knots, no extrapolation."""
        t = self.t(i)
        if np.any(t > self.knots_t[-1] + 1e-9):
            raise ValueError("maturity past the last knot of the curve")
        return np.exp(np.interp(t, self.knots_t, self.knots_lnp))

    def kappa(self, j):
        """Factor that fits the interpolated bond maturing at month j to the initial curve."""
        j = np.asarray(j)
        l, r = np.divmod(j, self.p)
        w = r / self.p
        upper = self.P0[np.minimum(l + 1, self.K)]
        return self.mkt_zcb(j) / ((1 - w) * self.P0[l] + w * upper)

    # ---- simulation ------------------------------------------------------------------
    def normals(self):
        rng = np.random.default_rng(self.seed)
        if self.antithetic:
            half = rng.standard_normal((self.n, self.N // 2, self.d))
            return np.concatenate([half, -half], axis=1)
        return rng.standard_normal((self.n, self.N, self.d))

    def step(self, i, F, z):
        """Forward rates at month i+1 from those at month i, by the log-Euler step."""
        c = i // self.p
        if c + 2 > self.K:
            return F
        ks = np.arange(c + 2, self.K + 1)                 # the rates not yet set at t_i
        lam = self.lam[(ks - 1) * self.p - i]             # their volatility vectors, (A, d)
        alive = F[:, c + 1:]
        g = self.tau * (alive + self.alpha) / (1 + self.tau * alive)
        drift = np.zeros_like(alive)
        for q in range(self.d):
            drift += lam[:, q] * np.cumsum(g * lam[:, q], axis=1)
        x = (np.log(alive + self.alpha) + (drift - 0.5 * (lam**2).sum(axis=1)) * DT
             + np.sqrt(DT) * (z @ lam.T))
        F = F.copy()
        F[:, c + 1:] = np.exp(x) - self.alpha
        return F

    def deflated_bond(self, i, F, Dc, j):
        """D(t_i; t_j), j >= i, from the state F and the deflator Dc = D(T_c) of month i."""
        c = i // self.p
        l, r = divmod(int(j), self.p)
        if j < i or l + (r > 0) > self.K:
            raise ValueError(f"no bond maturing at month {j} at month {i}")

        def tenor(k):                                     # D(t_i; T_k), k >= c
            return Dc / np.prod(1 + self.tau * F[:, c:k], axis=1)
        if r == 0:
            return tenor(l)
        w = r / self.p
        return self.kappa(j) * ((1 - w) * tenor(l) + w * tenor(l + 1))

    def simulate(self):
        """Run the scenarios once, keeping what the outputs and the tests need."""
        if self._sim is not None:
            return self._sim
        n, p, tau = self.n, self.p, self.tau
        z = self.normals()
        F = np.tile(self.F0, (self.N, 1))
        D = np.empty((n + 1, self.N))
        dz = {m: np.empty((n + 1, self.N)) for m in self.keep}
        tenor_D, fixings, snaps = {0: np.ones(self.N)}, {}, {}
        for i in range(n + 1):
            c = i // p
            Dc = tenor_D[c]
            if i % p == 0:
                fixings[c + 1] = F[:, c].copy()                # F_{c+1} is set at T_c
                tenor_D[c + 1] = Dc / (1 + tau * F[:, c])     # D(T_{c+1}), known at T_c
            D[i] = self.deflated_bond(i, F, Dc, i)
            for m in self.keep:
                dz[m][i] = self.deflated_bond(i, F, Dc, i + m)
            if i in self.snapshots:
                snaps[i] = (F.copy(), Dc.copy())
            if i < n:
                F = self.step(i, F, z[i])
        self._sim = dict(D=D, dz=dz, tenor_D=tenor_D, fixings=fixings, snapshots=snaps)
        return self._sim

    def P(self, i, j):
        """P(t_i, t_j) for each stochastic scenario; month i must be a snapshot."""
        F, Dc = self.simulate()["snapshots"][i]
        return self.deflated_bond(i, F, Dc, j) / self.deflated_bond(i, F, Dc, i)

    def swap_rate(self, i, k):
        annuity = sum(self.P(i, i + 12 * l) for l in range(1, k + 1))
        return (1 - self.P(i, i + 12 * k)) / annuity

    # ---- outputs with the CE scenario as row 0 -----------------------------------------
    def disc_factor_paths(self):
        ce = self.mkt_zcb(np.arange(self.n + 1))
        return np.vstack([ce, self.simulate()["D"].T])

    def ce_bank_returns(self):
        p = self.mkt_zcb(np.arange(self.n + 1))
        return p[:-1] / p[1:] - 1

    def bank_returns(self):
        D = self.simulate()["D"]
        return D[:-1] / D[1:] - 1

    def bank_return_paths(self):
        return np.vstack([self.ce_bank_returns(), self.bank_returns().T])

    def zcb_returns(self, m):
        """(n, N) returns over [t_i, t_{i+1}) of zeros with m months to maturity at t_i."""
        dz = self.simulate()["dz"]
        return (1 + self.bank_returns()) * dz[m - 1][1:] / dz[m][:-1] - 1

    def fund_returns(self):
        ret = self.fund_cash * self.bank_returns()
        for m, w in self.fund_bonds.items():
            ret = ret + w * self.zcb_returns(m)
        return ret

    def fund_return_paths(self):
        return np.vstack([self.ce_bank_returns(), self.fund_returns().T])

    def libor_rate_paths(self):
        sim, i = self.simulate(), np.arange(self.n + 1)
        ce = (self.mkt_zcb(i) / self.mkt_zcb(i + self.p) - 1) / self.tau
        libor = (1 / (sim["dz"][self.p] / sim["D"]) - 1) / self.tau
        return np.vstack([ce, libor.T])

    def spot_rate_paths(self, m):
        sim, i = self.simulate(), np.arange(self.n + 1)
        ce = (self.mkt_zcb(i) / self.mkt_zcb(i + m)) ** (12 / m) - 1
        return np.vstack([ce, ((sim["dz"][m] / sim["D"]) ** (-12 / m) - 1).T])

    # ---- closed forms ----------------------------------------------------------------
    def caplet_total_vol(self, k):
        """Total volatility of F_k + shift up to its expiry T_{k-1}."""
        m = (k - 1) * self.p
        return np.sqrt(DT * (self.lam[1:m + 1] ** 2).sum())

    def caplet(self, k, x):
        """Price at time 0 of tau (F_k(T_{k-1}) - x)+ paid at T_k, by Black's formula."""
        v = self.caplet_total_vol(k)
        return self.tau * self.P0[k] * black(self.F0[k - 1] + self.alpha, x + self.alpha, v)

    def floorlet(self, k, x):
        """Price of tau (x - F_k(T_{k-1}))+ paid at T_k, from the caplet by put-call parity."""
        return self.caplet(k, x) - self.tau * self.P0[k] * (self.F0[k - 1] - x)

    def caplet_payoffs(self, k, x):
        """Deflated payoffs of the caplet by scenario: D(T_k) tau (F_k(T_{k-1}) - x)+."""
        sim = self.simulate()
        return sim["tenor_D"][k] * self.tau * np.maximum(sim["fixings"][k] - x, 0)

    def gmab_floorlet(self, sa, av0):
        """Cost of a GMAB maturing at T_2 on a single premium AV0 in an all-cash fund.

        The account value at T_2 is AV0 (1 + tau F_1(0)) (1 + tau F_2(T_1)), so the
        guarantee is AV0 / P^M(0, T_1) floorlets on F_2 with strike
        x = (SA P^M(0, T_1) / AV0 - 1) / tau.
        """
        x = (sa * self.P0[1] / av0 - 1) / self.tau
        if x + self.alpha <= 0:
            return 0.0
        return av0 / self.P0[1] * self.floorlet(2, x)

    def swaption_vol(self, a, b):
        """Black volatility of S + shift for the swaption expiring in a years on the b-year
        swap with a yearly fixed leg, by Rebonato's formula; also S(0) and the annuity."""
        per = 12 // self.p                                # tenor periods in a year
        ia, ib = a * per, (a + b) * per
        fixed = np.arange(ia + per, ib + 1, per)          # tenor indexes of the fixed dates
        P = self.P0
        annuity = P[fixed].sum()
        swap = (P[ia] - P[ib]) / annuity
        js = np.arange(ia + 1, ib + 1)                    # the rates of the swap
        later = np.array([P[fixed[fixed >= j]].sum() for j in js])
        slope = self.tau / (1 + self.tau * self.F0[js - 1]) * (P[ib] + swap * later) / annuity
        weight = slope * (self.F0[js - 1] + self.alpha) / (swap + self.alpha)
        var = 0.0
        for i in range(12 * a):
            vec = weight @ self.lam[(js - 1) * self.p - i]
            var += DT * vec @ vec
        return np.sqrt(var / a), swap, annuity
