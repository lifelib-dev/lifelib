"""mx2cy's sample run for RILA_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The four
reports and the three checks reach every cell but these, and every code but a few: the
cells ``model_point`` and the seven label accessors, which only a reader asks for;
``point_id``, which only a refusal names; the eleven engine cells, ``norm_cdf``, the five
Black-Scholes cells, ``opt_component``, ``opt_portfolio``, ``opt_portfolio_abs``,
``credit_rate_at`` and ``opt_budget_at_cap``, which no projection cell calls;
``lapse_shock_year`` and ``guar_min_rate`` at a rate kind a point's crediting type does
not read, ``roll_share`` at each bucket and the legs, ``opt_leg_count`` and ``opt_leg``;
and the cells and codes no report reads, the fixed-leg yield and the implied spread, the
free-withdrawal base and allowance away from an anniversary, the pre-AG 54 rate on a
priced family, the cap solve off ``nge_reset``, the option-pricing market at each month
end, each leg on each basis, the decomposition and each leg after the withdrawal, the
opening notional, the balances after the withdrawal, the block's Account Value before it,
and the claims released from and paid above the Account Value at every kind and ``ALL``.
Those are called here too, the monthly ones in every month of the frame and the month
after it, each timed cell at every code of its family, each kinded cell at its three
kinds, each bucketed one at its three buckets, the market at every name to the instant
after that month, and the engine cells at the arguments ``RILA_US_S``'s own tests use.

The projections run on the committed points alone, and they leave branches untaken: a
Floor option at a one-year renewal under every family, a negative base under a power, a
power past the largest float, a market read before a scenario's first month.  That is
enough to type every cell, because every branch of a cell returns the one type its other
branches return, a rate a float in every branch and a code an int in every branch.  What
the compiled model computes on those branches is not traced but tested: the compile tests
run it on points that take them, and compare it with modelx.  A code a cell refuses,
``pols_if_at(t, BEF_WD)`` or ``claim_from_av_pp(t, ALL)``, is not called: a raise types
nothing.

The six free labels are typed from more than the committed points.  Each returns its
point's column as read, and ``Data`` accepts a table whose label is not text: a blank or
numeric ``policy_id``, read by no cell, a blank or numeric ``crediting_type``,
``iv_family`` or ``amort_rule``, read only through their decodes, which answer False, and a
``scenario_id`` or ``wd_schedule_id`` that is a number, where its table's keys are numbers.
modelx returns the value; an accessor traced on text alone would compile to ``str`` and
raise ``TypeError`` on it.  So the run also calls the six on a copy of the table's first
point with its four free labels blank and its two keys the number 1, beside one-key
copies of the scenario and withdrawal tables keyed by 1, all written to a temporary
directory and read by a second instance of the export, whose ``Data`` reads them by
absolute file names.  mx2cy then types the six as Python objects, as the reporting cells
they are, and the compiled model returns what modelx returns.  ``sex`` stays text: the
mortality table's check admits no sex but ``M`` and ``F``, and ``sex`` refuses any other
value itself.  Nothing is written beside the export, and no other cell is called there but
``model_point``, ``model_point_table`` and ``input_dir``, which are Python objects already,
and the checks ``model_point_table`` runs.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, net_cf cold in the last month of the longest cover, issue age 0, issued
# now or 120 months on, needs a limit of 2,213 in the export from a script's top level,
# and the reports below, which run in ascending t, need 154, the export's import among
# the frames they run under, and 49 once it is imported (measured at M25).  So the build
# itself needs 154, and the rest is margin for an edit that calls a cell cold.  The limit
# is four times the first, rounded up to the thousand, 9,000, which a test holds to this
# comment.
sys.setrecursionlimit(9_000)

import pandas as pd  # noqa: E402

from RILA_US_SEC_nomx import mx_model  # noqa: E402
from RILA_US_SEC_nomx._mx_model import _c_RILA_US_SEC  # noqa: E402

LABELS = ("policy_id", "crediting_type", "iv_family", "amort_rule", "scenario_id",
          "wd_schedule_id")
KEYS = ("scenario_id", "wd_schedule_id")

projection = mx_model.Projection
FAMILIES = {
    "pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "BEF_TERM_SURR", "AFT_DECR"),
    "inv_amt_pp_at": ("BEF_CREDIT", "BEF_ROLL", "BEF_WD", "AFT_WD"),
    "interim_value_pp_at": ("BEF_ROLL", "BEF_WD", "AFT_WD"),
    "iv_notional_pp": ("BEF_ROLL", "AFT_WD"),
    "fixed_proxy_pp": ("BEF_ROLL", "AFT_WD"),
    "budget_amort_pp": ("BEF_ROLL", "AFT_WD"),
    "deriv_proxy_pp": ("BEF_ROLL", "AFT_WD"),
    "trading_cost_pp": ("BEF_ROLL", "AFT_WD"),
    "fixed_acct_pp_at": ("BEF_WD", "AFT_WD"),
    "holding_acct_pp_at": ("BEF_WD", "AFT_WD"),
    "av_pp_at": ("BEF_WD", "AFT_WD"),
    "av_at": ("BEF_WD", "AFT_WD"),
}
KINDED = ("pols_decr", "claim_pp", "claim_from_av_pp", "claims", "claims_from_av",
          "claims_over_av")
KINDS = ("DEATH", "LAPSE", "MATURITY")
BUCKETED = ("roll_to_acct_pp", "wd_bucket_value_pp", "wd_alloc_pp")
BUCKETS = ("OPTION", "FIXED", "HOLDING")
NAMES = ("INDEX_LEVEL", "MVR", "RISK_FREE", "DIV_YIELD", "IMPL_VOL")
BASES = ("CURRENT", "TERM_START", "UPDATED_EXPIRY")
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_av()
    p.result_iv()
    p.check_av_roll_fwd()
    p.check_pols_roll_fwd()
    p.check_term_end_identity()
    p.model_point(), p.point_id(), p.sex()
    for label in LABELS:
        getattr(p, label)()
    p.lapse_shock_year()
    for kind in ("CAP", "STEP", "EDGE"):
        p.guar_min_rate(getattr(projection, kind))
    for bucket in BUCKETS:
        p.roll_share(getattr(projection, bucket))
    legs = [p.opt_leg(i) for i in range(p.opt_leg_count())]
    for t in range(p.proj_len() + 1):
        p.duration_mth(t), p.fixed_leg_yield(t), p.nge_spread_implied(t)
        p.free_wd_base(t), p.free_wd_allow(t)
        p.credit_rate_accrued(t), p.declared_cap_solved(t)
        for cell, labels in FAMILIES.items():
            for label in labels:
                getattr(p, cell)(t, getattr(projection, label))
        for cell in KINDED:
            for kind in KINDS:
                getattr(p, cell)(t, getattr(projection, kind))
        p.claims(t, projection.ALL), p.claims_over_av(t, projection.ALL)
        for cell in BUCKETED:
            for bucket in BUCKETS:
                getattr(p, cell)(t, getattr(projection, bucket))
        for basis in BASES:
            p.opt_portfolio_at(t, getattr(projection, basis))
            p.opt_portfolio_abs_at(t, getattr(projection, basis))
            for leg in legs:
                p.opt_component_at(t, leg, getattr(projection, basis))
        for leg in legs:
            for timing in ("BEF_ROLL", "AFT_WD"):
                p.opt_component_pp(t, leg, getattr(projection, timing))
        p.credit_rate_by(t, projection.TERM_END), p.credit_rate_by(t, projection.PRORATED)
    for t in range(p.t_entry(), p.proj_len() + 1):
        p.risk_free(t), p.div_yield(t), p.impl_vol(t), p.index_level(t), p.mvr(t)
    for t in range(p.t_entry(), p.proj_len() + 2):
        for name in NAMES:
            p.market_state(t, getattr(projection, name))
    # The engine cells, at the arguments RILA_US_S's tests use.
    e = p.t_entry()
    for x in (-1.0, 0.0, 0.5):
        p.norm_cdf(x)
    for tau_ in (0.0, 1.0, 6.0):
        p.bs_call(100.0, 100.0, tau_, 0.04, 0.02, 0.2)
        p.bs_put(100.0, 90.0, tau_, 0.04, 0.02, 0.2)
        p.bs_binary_call(100.0, 100.0, tau_, 0.04, 0.02, 0.2)
    p.bs_d1(100.0, 100.0, 1.0, 0.04, 0.02, 0.2), p.bs_d2(100.0, 100.0, 1.0, 0.04, 0.02, 0.2)
    for leg in legs:
        p.opt_component(e, leg, 100.0, 1.0, projection.CURRENT)
        p.opt_component(e, leg, 100.0, 1.0, projection.TERM_START)
    p.opt_portfolio(e, 100.0, 1.0, projection.CURRENT)
    p.opt_portfolio_abs(e, 100.0, 1.0, projection.CURRENT)
    p.credit_rate_at(e, 1.0), p.credit_rate_at(e, 0.5), p.opt_budget_at_cap(e, 0.5)

data = mx_model.Data
here = data.input_dir()
point = pd.read_csv(here / data.model_point_file).iloc[[0]]
first = point.iloc[0]
point = point.assign(**{label: None for label in LABELS if label not in KEYS},
                     **{key: 1 for key in KEYS})
steps = pd.read_csv(here / data.market_scenario_file)
steps = steps[steps["scenario_id"] == first["scenario_id"]].assign(**{"scenario_id": 1})
programmes = pd.read_csv(here / data.withdrawal_file)
programmes = programmes[programmes["wd_schedule_id"] == first["wd_schedule_id"]].assign(
    **{"wd_schedule_id": 1})
with tempfile.TemporaryDirectory() as folder:
    second = _c_RILA_US_SEC()
    for ref, table in (("model_point_file", point), ("market_scenario_file", steps),
                       ("withdrawal_file", programmes)):
        path = pathlib.Path(folder) / getattr(data, ref)
        table.to_csv(path, index=False)
        setattr(second.Data, ref, str(path))
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
