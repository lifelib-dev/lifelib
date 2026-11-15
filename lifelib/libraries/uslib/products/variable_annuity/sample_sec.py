"""mx2cy's sample run for VA_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  And a call that raises types
its cell, and every cell beneath it on the stack, as a Python object too: mx2cy logs a
call unwound by an exception as returning ``None``, which merges with the type the cell
returns elsewhere to ``object`` (M22).  So the run calls every cell, of ``Data`` and of
``Projection``, at least once, on every point of the committed table, and each only where
the point computes it, so that no call raises: no code a cell refuses, no key past an
array's hold, no scenario read before its first month, no quarter before the point's
first on the books.

First every ``Data`` cell of no parameter, bare, so that each vector and extent is typed
whatever the projections reach: ``gawa_pct_zero_by_point``, which only a depleted point
that has not withdrawn asks for, and ``gawa_last_band``, which only an age past
``read_last_age`` asks for, among them.  Then, on each point: the four reports and the
three checks; every ``Projection`` cell of no parameter, ``model_point``, ``point_id`` and
the thirteen label accessors among them, and ``sub_ids``, an engine cell; every monthly
cell, from ``t = 0`` to the month after the frame, ``t = proj_len()``, which C4's sweep
calls: each is guarded outside cover and returns its value there, but the scenario
readers, which are called from the point's first month on the books, ``t_entry()``; each
timed cell at every code of its family, ``sa_pp_at`` and the subaccount cells at every
subaccount the point's set holds, and each kinded cell at its three kinds, ``claims`` and
``claims_over_av`` at ``ALL`` too; the rate scenario at both columns; the quarter readers,
``vix_sq`` and ``phi_glwb_vix``, at every quarter from the point's first on the books,
``max(duration_mth_init(), 0) // 3 + 1``, to its last; the keyed readers at every policy
month, completed year and attained age of cover; the subaccount readers at every id the
set holds and ``subaccount_id`` at every position; and the three engine cells keyed by a
float, ``lapse_itm_mult``, ``fee_rate_vix_raw`` and ``fee_rate_vix_clip``, at the
arguments the module's own tests use, ``ITM_RATIOS``, ``VIX_RAW_ARGS`` and
``VIX_CLIP_ARGS``, which a test holds equal to the module's.

The projections run on the committed points alone, and they leave branches untaken: the
female mortality, an issue age other than 60, a three-subaccount set, a grid with a 0%
band, a programme past its first years.  That is enough to type every cell, because every
branch of a cell returns the one type its other branches return, a rate a float in every
branch and a phase an int in every branch.  What the compiled model computes on those
branches is not traced but tested: the compile tests run it on points that take them, and
compare it with modelx.

The thirteen label accessors are typed from more than the committed points.  Each returns
its point's column as read, and ``Data`` accepts a table whose label is not text: a blank
or numeric ``policy_id``, ``designated_lives`` or ``tax_status``, which no cell reads; a
blank ``glwb_stepup_basis``, ``gmdb_option``, ``fee_reset_rule`` or ``rollup_rule``, read
only through their decodes, which answer False; and a ``sex``, ``fund_set``,
``glwb_option``, ``cdsc_schedule``, ``scenario_id`` or ``txn_id`` that is a number, where
its table's keys are numbers.  modelx returns the value; an accessor traced on text alone
would compile to ``str`` and raise ``TypeError`` on it.  So the run also calls the thirteen
on a copy of the table's first point, issued at the valuation date, with its three free
labels and its four switches blank and its six keys the number 1, beside one-key copies
of the mortality, fund, GAWA%, withdrawal charge, return, rate and programme tables keyed
by 1, all written to a temporary directory and read by a second instance of the export,
whose ``Data`` reads them by absolute file names.  mx2cy then types the thirteen as Python
objects, as the reporting cells they are, and the compiled model returns what modelx
returns.  Nothing is written beside the export, and no other cell is called there but
``model_point``, ``model_point_table`` and ``input_dir``, which are Python objects already,
and the checks ``model_point_table`` runs.
"""
import inspect
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest calls the
# contract allows, pols_decr at DEATH and at LAPSE cold in the last month of the longest
# frame, issue age 35, issued now or 120 months on, need a limit of 2,092 in the export
# (check_pols_roll_fwd_resid and pols_lapse 2,090, net_cf 2,079), and the reports below,
# which run in ascending t, need 1,149, on the point whose GAWA is first read at policy
# month 563, the export's import among the frames they run under (measured at M22).  So
# the build itself needs 1,149, and the rest is margin for an edit that calls a cell cold.
# The limit is four times the first, rounded up to the thousand, 9,000, which a test holds
# to this comment.
sys.setrecursionlimit(9_000)

import pandas as pd  # noqa: E402

from VA_US_SEC_nomx import mx_model  # noqa: E402
from VA_US_SEC_nomx._mx_model import _c_VA_US_SEC  # noqa: E402

LABELS = ("policy_id", "sex", "designated_lives", "tax_status", "fund_set", "glwb_option",
          "stepup_basis", "gmdb_option", "cdsc_schedule", "fee_reset_rule", "rollup_rule",
          "scenario_id", "txn_id")
FREE = ("policy_id", "designated_lives", "tax_status", "glwb_stepup_basis", "gmdb_option",
        "fee_reset_rule", "rollup_rule")
KEYS = ("sex", "fund_set", "glwb_option", "cdsc_schedule", "scenario_id", "txn_id")
ITM_RATIOS = (0.0, 0.5, 1.0, 1.1, 1.3, 1.5, 2.0)
VIX_RAW_ARGS = ((0.0125, 204.42), (0.0145, 602.30), (0.0125, 0.0), (0.0125, 1500.0))
VIX_CLIP_ARGS = ((0.0142, 0.0186), (0.0142, 0.0126), (0.008, 0.002), (0.0245, 0.04))
FAMILIES = {
    "pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "AFT_DECR"),
    "av_pp_at": ("BEF_PREM", "BEF_WD", "BEF_INV", "BEF_FEE", "EOM"),
    "av_at": ("BEF_PREM", "BEF_WD", "BEF_INV", "BEF_FEE", "EOM"),
    "gwb_pp_at": ("BEF_PREM", "BEF_WD", "BEF_ANNIV"),
    "gawa_pp_at": ("BEF_PREM", "BEF_WD", "BEF_ANNIV"),
    "rb_pp_at": ("BEF_PREM", "BEF_WD", "BEF_ANNIV"),
}
SA_TIMINGS = ("BEF_PREM", "BEF_WD", "BEF_INV", "BEF_FEE", "EOM")
KINDED = ("pols_decr", "claim_pp", "claim_from_av_pp", "claims", "claims_from_av",
          "claims_over_av")
KINDS = ("DEATH", "LAPSE", "MATURITY")
TOTALLED = ("claims", "claims_over_av")
SCENARIO = ("cmt10",)             # keyed by t alone, but read from t_entry() only


def parameters(space):
    """Each formula of ``space``'s class, by name, and its parameters but ``self``."""
    found = {}
    for name, member in vars(type(space)).items():
        if not name.startswith("_") and inspect.isfunction(member):
            found[name] = tuple(inspect.signature(member).parameters)[1:]
    return found


data = mx_model.Data
for name, params in parameters(data).items():
    if not params:
        getattr(data, name)()

projection = mx_model.Projection
cells = parameters(projection)
NOARG = sorted(name for name, params in cells.items() if not params)
MONTHLY = sorted(name for name, params in cells.items()
                 if params == ("t",) and name not in SCENARIO)
for idx in range(len(data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_av()
    p.result_bases()
    p.check_av_roll_fwd()
    p.check_pols_roll_fwd()
    p.check_charge_split()
    for name in NOARG:
        getattr(p, name)()
    ids = [p.subaccount_id(j) for j in range(p.subaccount_count())]
    entry, n = p.t_entry(), p.proj_len()
    s = p.rate_scenario_number()
    rate_first = data.rate_first_mths()[s] if s > 0 else n + 1
    for t in range(n + 1):
        for name in MONTHLY:
            getattr(p, name)(t)
        for cell, labels in FAMILIES.items():
            for label in labels:
                getattr(p, cell)(t, getattr(projection, label))
        for cell in KINDED:
            for kind in KINDS:
                getattr(p, cell)(t, getattr(projection, kind))
        for cell in TOTALLED:
            getattr(p, cell)(t, projection.ALL)
        for i in ids:
            p.sa_pp(t, i)
            p.sa_weight(t, i)
            for label in SA_TIMINGS:
                p.sa_pp_at(t, i, getattr(projection, label))
            if t >= entry:
                p.inv_return_mth(t, i)
                p.unit_growth(t, i)
        if t >= max(entry, rate_first):
            p.cmt10(t)
            p.scenario_rate(t, projection.VIX_SQ)
            p.scenario_rate(t, projection.CMT10)
    if s > 0:
        for k in range(max(p.duration_mth_init(), 0) // 3 + 1, p.maturity_mth() // 3 + 1):
            p.vix_sq(k)
            p.phi_glwb_vix(k)
    for m in range(p.maturity_mth()):
        p.t_of_month(m)
        p.prem_scheduled_pm(m)
        p.wd_scheduled_pm(m)
    for k in range(p.policy_term()):
        p.surr_charge_rate_at(k)
    for a in range(p.age_at_entry(), p.omega_age):
        p.mort_rate_base_at(a)
        p.gawa_pct_at_age(a)
    for i in ids:
        p.alloc(i)
        p.fund_expense_rate(i)
        p.sa_pp_init(i)
    for ratio in ITM_RATIOS:
        p.lapse_itm_mult(ratio)
    for args in VIX_RAW_ARGS:
        p.fee_rate_vix_raw(*args)
    for args in VIX_CLIP_ARGS:
        p.fee_rate_vix_clip(*args)

here = data.input_dir()
point = pd.read_csv(here / data.model_point_file).iloc[[0]]
first = point.iloc[0]
point = point.assign(**{label: None for label in FREE}, **{key: 1 for key in KEYS})
mort = pd.read_csv(here / data.mort_table_file)
mort = mort[mort["sex"] == first["sex"]].assign(**{"sex": 1})
funds = pd.read_csv(here / data.fund_file)
funds = funds[funds["fund_set"] == first["fund_set"]].assign(**{"fund_set": 1})
grids = pd.read_csv(here / data.gawa_pct_file)
grids = grids[grids["gawa_grid"] == first["glwb_option"]].assign(**{"gawa_grid": 1})
scales = pd.read_csv(here / data.cdsc_file)
scales = scales[scales["cdsc_schedule"] == first["cdsc_schedule"]].assign(
    **{"cdsc_schedule": 1})
returns = pd.read_csv(here / data.return_scenario_file)
returns = returns[returns["scenario_id"] == first["scenario_id"]].assign(
    **{"scenario_id": 1})
rates = pd.read_csv(here / data.rate_scenario_file)
rates = rates[rates["scenario_id"] == first["scenario_id"]].assign(**{"scenario_id": 1})
programmes = pd.read_csv(here / data.transaction_file)
programmes = programmes[programmes["txn_id"] == first["txn_id"]].assign(**{"txn_id": 1})
with tempfile.TemporaryDirectory() as folder:
    second = _c_VA_US_SEC()
    for ref, table in (("model_point_file", point), ("mort_table_file", mort),
                       ("fund_file", funds), ("gawa_pct_file", grids),
                       ("cdsc_file", scales), ("return_scenario_file", returns),
                       ("rate_scenario_file", rates), ("transaction_file", programmes)):
        path = pathlib.Path(folder) / getattr(data, ref)
        table.to_csv(path, index=False)
        setattr(second.Data, ref, str(path))
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
    del p, second
