"""Build the key-rate DV01 and CS01 model on MYGA_US_SEC policies and G2++ market paths.

The model has six Spaces:

* ``Data``: MYGA_US_SEC's Data Space, copied, with the key-rate tenors (``shock_key_months``)
  and the book's projection end (``book_projection_end``) added.
* ``ESG``: the G2++ generator of ``economic/CashValue_ME_G2PP``, copied, with one Cell added,
  ``P_t_T_path``, the zero-coupon price on one generated path.
* ``Market``: one zero-coupon curve, keyed by the close it is observed after, the ESG path and
  the key-rate shock (``-1`` for none).
* ``Actual``: one policy on one ESG path, projected from the valuation date with MYGA_US_SEC's
  formulas, its quotes read from the market observed each month (``actual.py``).
* ``Valuation``: the same policy restarted in force after a close, its opening state read from
  ``Actual`` through the dynamic Reference ``act``, valued on one ``Market`` (``valuation.py``):
  the policy's Actual ItemSpace, or, on the collect route (``collect_history``), the policy's
  openings from ``Actual.collect``, which releases the ItemSpaces it projects.
* ``Outer``: the portfolio results and the annual risk report (``outer.py``), summed policy by
  policy through the ItemSpaces.

MYGA_US_SEC's own deterministic rate scenario is not used: its three Cells are left out, and
the market rate, renewal quote and MVA yields come from the Market Space (``contract.py``).
"""
import math
import pathlib
from pathlib import Path

import numpy as np
import pandas as pd

import lifelib

from . import actual, contract, market, outer, valuation

# Months of Actual's cash flows that Outer.actual_cashflows reports.
OUTER_MONTHS = 36

# The key-rate tenors, relative to the input directory MYGA_US_SEC reads its CSVs from.
SHOCK_STEPS_FILE = 'dv01_sec/shock_steps.csv'

# MYGA_US_SEC cells the example replaces by market quotes: the deterministic rate scenario.
_DROPPED = ('scenario_rate', 'scenario_number', 'scenario_id')

TABLES = ('model_point_table', 'mort_table', 'surr_charge_table', 'surr_charge_age_cap_table',
          'rate_scenario', 'withdrawal_table', 'mva_factor_table')


def _valuation_collect_outputs():
    """Sum liability PV and the base-curve cash flows across the book."""
    return {'sum': {'pv': liability_pv(), 'cf': {
        k: cashflow_at_offset(k) for k in projection_months(valuation_month)
    } if shock == -1 else {}}}


def _actual_collect_outputs():
    """Keep the policy openings that Valuation reads at the requested closes."""
    return {'individual': {
        'pols_if_open': {t: pols_if_open(t) for t in opening_months},
        'av_pp_open': {t: av_pp_open(t) for t in opening_months},
        'mgsv_pp_open': {t: mgsv_pp_open(t) for t in opening_months},
        'prem_accum_gmir_pp_open': {t: prem_accum_gmir_pp_open(t) for t in opening_months},
        'interest_credited_pp_open': {t: interest_credited_pp_open(t) for t in opening_months},
        'interest_credited_pp_prev_anniv_open': {
            t: interest_credited_pp_prev_anniv_open(t) for t in opening_months},
        'free_wd_allow_open': {t: free_wd_allow_open(t) for t in opening_months},
        'free_wd_remain_open': {t: free_wd_remain_open(t) for t in opening_months},
        'tax_basis_pp_open': {t: tax_basis_pp_open(t) for t in opening_months},
        'credit_rate_open': {t: credit_rate_open(t) for t in opening_months},
        'mva_ref_yield_locked_open': {t: mva_ref_yield_locked_open(t) for t in opening_months},
    }}


def _shock_key_months():
    """Ordered key tenors in whole months, read once from the input directory."""
    table = pd.read_csv(input_dir() / shock_steps_file)
    if list(table.columns) != ['tenor_months'] or table.empty:
        raise ValueError('shock_steps.csv requires one tenor_months column and at least one row')
    values = table['tenor_months']
    if (not pd.api.types.is_integer_dtype(values.dtype) or values.min() <= 0
            or not values.is_monotonic_increasing or not values.is_unique):
        raise ValueError('shock tenors must be positive whole months in strictly increasing order')
    return values.tolist()


def _book_projection_end():
    """Exclusive month end, from the valuation date, of the longest contract in the book."""
    months = 12 * (maturity_age - age_at_entry()) - duration_mth()
    return max(0, int(months.max()))


def _market_key(as_of_month, scen_id, shock=-1):
    if (isinstance(as_of_month, bool) or not isinstance(as_of_month, (int, np.integer))
            or not 0 <= as_of_month <= ESG.step_size()):
        raise ValueError('as_of_month is outside the generated ESG time grid')
    if (isinstance(scen_id, bool) or not isinstance(scen_id, (int, np.integer))
            or not 1 <= scen_id <= ESG.scen_size()):
        raise ValueError('scen_id must identify a generated ESG path')
    if (isinstance(shock, bool) or not isinstance(shock, (int, np.integer))
            or not -1 <= shock < len(data.shock_key_months())):
        raise ValueError('shock must be -1 or a key-rate index')
    return None


def _actual_point(idx, scen_id):
    if (isinstance(scen_id, bool) or not isinstance(scen_id, (int, np.integer))
            or not 1 <= scen_id <= ESG.scen_size()):
        raise ValueError('scen_id must identify a generated ESG path')
    return None


def _valuation_point(valuation_month, idx, scen_id, shock=-1):
    if (isinstance(valuation_month, bool) or not isinstance(valuation_month, (int, np.integer))
            or not -1 <= valuation_month < ESG.step_size()):
        raise ValueError('valuation_month is outside the generated ESG time grid')
    if (isinstance(scen_id, bool) or not isinstance(scen_id, (int, np.integer))
            or not 1 <= scen_id <= ESG.scen_size()):
        raise ValueError('scen_id must identify a generated ESG path')
    if collect_history:      # the collect route: the policy's openings from Actual's collect
        return {'refs': {'act': Actual.collect(scen_id).individual[idx]}}
    return {'refs': {'act': Actual[idx, scen_id]}}


# The ESG's input file, found in the installed lifelib wherever the model is run from.
def _packaged_input_path():
    return pathlib.Path(lifelib.__file__).parent / 'libraries' / 'economic' / input_file


# The zero-coupon price from close i to month j on one path, numbered from one, computed for
# that path alone (P_t_T computes it for every path).
def _P_t_T_path(i, j, scen_id):
    if not 1 <= scen_id <= scen_size():
        raise ValueError("scen_id must identify a generated ESG path")
    return (mkt_zcb(j) / mkt_zcb(i)
            * math.exp(0.5 * (V_t_T(i, j) - V_t_T(0, j) + V_t_T(0, i))
                       - Ba_t_T(i, j) * float(x(i)[scen_id - 1])
                       - Bb_t_T(i, j) * float(y(i)[scen_id - 1])))


def _copy_esg(model):
    import modelx as mx

    economic = Path(__file__).resolve().parents[4] / 'economic'
    source = mx.read_model(economic / 'CashValue_ME_G2PP', name=model.name + 'ESGSource')
    try:
        esg = source.ESG.copy(model, 'ESG')
    finally:
        source.close()
    esg.math = math
    esg.lifelib = lifelib
    esg.pathlib = pathlib
    esg.input_path.formula = _packaged_input_path
    if 'P_t_T_path' not in esg.cells:
        esg.new_cells('P_t_T_path', _P_t_T_path)
    esg.param_table()
    esg.curve_knots()
    return esg


def _sec_data(model, source_path):
    import modelx as mx

    source = mx.read_model(source_path, name=model.name + 'InputSource')
    try:
        data = source.Data.copy(model, 'Data')
        projection = source.Projection
        formulas = {name: cell.formula.source for name, cell in projection.cells.items()
                    if name not in _DROPPED}
        refs = {name: getattr(projection, name) for name in projection.refs
                if not name.startswith('__') and name not in ('data', 'idx')}
    finally:
        source.close()
    data.maturity_age = refs['maturity_age']
    data.shock_steps_file = SHOCK_STEPS_FILE
    data.new_cells('shock_key_months', _shock_key_months)
    data.new_cells('book_projection_end', _book_projection_end)
    return data, formulas, refs


def _install(space, sec_formulas):
    """SEC formulas the Space does not define itself; SEC's net_cf kept as contract_net_cf."""
    for name, source in sec_formulas.items():
        if name not in space.cells:
            space.new_cells(name, source)
    space.new_cells('contract_net_cf', sec_formulas['net_cf'])


def build_model(*, model_name='MYGASECDV01', input_dir=None, outer_months=OUTER_MONTHS):
    """The DV01 model, reading MYGA_US_SEC's formulas and, from ``input_dir``, its CSVs.

    ``input_dir`` is the directory holding the model point table and the assumption tables,
    and ``dv01_sec/shock_steps.csv`` below it; by default the product directory, where
    MYGA_US_SEC's own inputs are.
    """
    import modelx as mx
    product = Path(__file__).resolve().parents[1]
    model = mx.new_model(model_name)
    try:
        data, sec_formulas, sec_refs = _sec_data(model, product / 'MYGA_US_SEC')
        model.path = Path(input_dir or product).resolve() / 'MYGA_US_SEC'
        esg = _copy_esg(model)
    except BaseException:
        model.close()
        raise
    market_space = model.new_space_from_module(market, name='Market', formula=_market_key,
        refs={'ESG': esg, 'data': data, 'shock_bp': 1.e-4, 'np': np})
    market_space.absref(Market=market_space)
    common = {**sec_refs, 'data': data, 'ESG': esg, 'Market': market_space, 'np': np}
    actual_space = model.new_space_from_module(actual, name='Actual', formula=_actual_point,
        refs={**common, 'projection_months': tuple(range(outer_months)), 'opening_months': (0, 12, 24)})
    valuation_space = model.new_space_from_module(valuation, name='Valuation',
        formula=_valuation_point, refs={**common, 'Actual': actual_space, 'act': None,
                                        'collect_history': False})
    for space in (actual_space, valuation_space):
        space.new_cells_from_module(contract)
    valuation_space.new_cells('point_indices', actual_space.cells['point_indices'].formula.source)
    _install(actual_space, sec_formulas)
    _install(valuation_space, sec_formulas)
    valuation_space.set_collect(
        over={'idx': valuation_space.point_indices}, outputs=_valuation_collect_outputs)
    actual_space.set_collect(
        over={'idx': actual_space.point_indices}, outputs=_actual_collect_outputs)

    outer_space = model.new_space_from_module(outer, name='Outer', refs={
        'Actual': actual_space, 'Valuation': valuation_space, 'ESG': esg,
        'Market': market_space, 'data': data, 'pd': pd, 'np': np})
    for table in TABLES:
        getattr(data, table)()
    return model
