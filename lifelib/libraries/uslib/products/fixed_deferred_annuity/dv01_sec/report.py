"""The annual risk report, computed policy by policy, in live modelx or in the compiled model.

:func:`live_report` asks the model's own ``Outer`` Cells for the report's values, and
releases the Valuation ItemSpaces of each close and curve once summed, so that a book's
projections are not all held at once.

:func:`pooled_report` gives the same numbers from the compiled model: one task per policy,
which values the policy at every close and on every curve and returns its PVs and base cash
flows, the tasks run by a pool of threads, and the results summed in policy order, as the
``Outer`` Cells sum them.  With more than one worker the main thread submits every task and
then waits once for all of them with ``concurrent.futures.wait``; it does not wait on each
result in turn, as ``list(pool.map(...))`` does, because on free-threaded CPython 3.14 a
thread waiting on a lock spins while attached to the interpreter, and that holds back the
reuse of the memory the workers free (``dv01-sec.md``, *The driver*).

:func:`collect_report` gives the same numbers through ``Valuation.collect``: one collect per close
and curve over the book, each policy's ItemSpace evaluated, added and released by the compiled
collect, on ``workers`` threads; each reads its policy's openings from ``Actual.collect``.
"""
from concurrent.futures import ThreadPoolExecutor, wait

import numpy as np
import pandas as pd


def closes(annual_steps):
    """The valuation months of years 0..annual_steps: the close before each year starts."""
    return tuple(12 * year - 1 for year in range(annual_steps + 1))


def _frames(model, num_scenarios, annual_steps, dv01_rows, cs01_rows):
    index = pd.MultiIndex.from_product(
        [range(1, num_scenarios + 1), range(annual_steps + 1)], names=['scenario', 'year'])
    tenors = pd.Index(model.Data.shock_key_months(), name='tenor_months')
    return (pd.DataFrame(dv01_rows, index=index, columns=tenors),
            pd.DataFrame(cs01_rows, index=index, columns=tenors))


def live_report(model, num_scenarios, annual_steps):
    """``Outer.annual_risk_report``'s frames from the ``Outer`` Cells, close by close.

    Each value is read from ``Outer.dv01`` and ``Outer.cs01``, which is what
    ``Outer.annual_risk_report`` arranges, and each close's Valuation ItemSpaces are released
    once its values are read: on a shocked curve after the key, and on the base curve after
    the close.  Releasing an ItemSpace clears the ``Outer`` values computed from it, so the
    frames are assembled here rather than by calling ``Outer.annual_risk_report`` after.
    """
    outer, valuation = model.Outer, model.Valuation
    ids = valuation.point_indices()
    keys = range(len(model.Data.shock_key_months()))
    dv01_rows, cs01_rows = [], []
    for scen_id in range(1, num_scenarios + 1):
        for month in closes(annual_steps):
            dv, cs = [], []
            for key in keys:
                dv.append(outer.dv01(month, scen_id, key))
                cs.append(outer.cs01(month, scen_id, key))
                for i in ids:
                    del valuation[month, i, scen_id, key]
            for i in ids:
                del valuation[month, i, scen_id, -1]
            dv01_rows.append(dv)
            cs01_rows.append(cs)
    return _frames(model, num_scenarios, annual_steps, dv01_rows, cs01_rows)


def pooled_report(model, num_scenarios, annual_steps, workers=1):
    """The annual risk report from one task per policy, run by ``workers`` threads."""
    valuation, actual = model.Valuation, model.Actual
    ids = list(valuation.point_indices())
    keys = range(len(model.Data.shock_key_months()))
    scenarios = range(1, num_scenarios + 1)
    months = closes(annual_steps)

    def policy(i):
        out = {}
        for s in scenarios:
            for m in months:
                v = valuation[m, i, s, -1]
                pv = v.liability_pv()
                cf = [v.cashflow_at_offset(k) for k in valuation.projection_months(m)]
                del v, valuation[m, i, s, -1]
                shocked = []
                for key in keys:
                    v = valuation[m, i, s, key]
                    shocked.append(v.liability_pv())
                    del v, valuation[m, i, s, key]
                out[s, m] = (pv, cf, shocked)
            del actual[i, s]
        return out

    if workers == 1:
        results = [policy(i) for i in ids]
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(policy, i) for i in ids]
            wait(futures)
            results = [f.result() for f in futures]

    dv01_rows, cs01_rows = [], []
    for s in scenarios:
        for m in months:
            base = 0.0
            for r in results:
                base += r[s, m][0]
            offsets = list(valuation.projection_months(m))
            cf = {k: 0.0 for k in offsets}
            for r in results:
                for k, x in zip(offsets, r[s, m][1]):
                    cf[k] += x
            dv, cs = [], []
            for key in keys:
                shocked = 0.0
                for r in results:
                    shocked += r[s, m][2][key]
                dv.append(base - shocked)
                market = model.Market(m + 1, s, key)
                discounts = [market.price(m + k + 2) for k in cf]
                cs.append(base - float(-np.dot(tuple(cf.values()), discounts)))
            dv01_rows.append(dv)
            cs01_rows.append(cs)
    return _frames(model, num_scenarios, annual_steps, dv01_rows, cs01_rows)


def collect_report(model, num_scenarios, annual_steps, workers=1):
    """The annual risk report from one collect per close and curve, over the book.

    Each Valuation item reads its policy's openings from ``Actual.collect`` (``collect_history``),
    collected once per path at the months after the closes, so that no Actual ItemSpace is
    kept: Actual's collect releases each one once its openings are read."""
    model._mx_collect_workers = workers
    valuation = model.Valuation
    keys = range(len(model.Data.shock_key_months()))
    openings = tuple(m + 1 for m in closes(annual_steps))
    if tuple(model.Actual.opening_months) != openings:
        model.Actual.opening_months = openings
    dv01_rows, cs01_rows = [], []
    valuation.collect_history = True
    try:
        for s in range(1, num_scenarios + 1):
            model.Actual.collect(s)     # the book's openings on path s, once, on the workers
            for m in closes(annual_steps):
                base = valuation.collect(m, s, -1).sum
                dv, cs = [], []
                for key in keys:
                    dv.append(base.pv - valuation.collect(m, s, key).sum.pv)
                    market = model.Market(m + 1, s, key)
                    discounts = [market.price(m + k + 2) for k in base.cf]
                    cs.append(base.pv - float(-np.dot(tuple(base.cf.values()), discounts)))
                dv01_rows.append(dv)
                cs01_rows.append(cs)
    finally:
        valuation.collect_history = False
    return _frames(model, num_scenarios, annual_steps, dv01_rows, cs01_rows)
