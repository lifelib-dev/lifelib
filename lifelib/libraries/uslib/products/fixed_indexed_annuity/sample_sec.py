"""mx2cy's sample run for FIA_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The five
reports and the two checks reach every cell but these, and every code but a few: the
cells ``model_point`` and the eight label accessors, which only a reader asks for;
``point_id``, which only a refusal names; the four engine cells, ``credit_rate_on``,
``payout_rate``, ``mgsv_rate_statutory`` and ``mgsv_rate_is_compliant``, which no
projection cell calls; ``bonus_factor``, the clawback factor, and ``activation_rate``,
the activation incidence, which only a reader asks for; the withdrawals to date,
``wd_cum_pp`` with ``wd_cum_pp_init``, the indexed account, ``av_indexed_pp``, and the
benefit paid above the account value, ``claims_over_av``, at every kind and ``ALL``, none
of which a report reads; the five decodes no committed point and no shipped Reference
asks, ``is_credit_spread``, ``is_credit_trigger``, ``is_step_up_at_exercise``,
``is_rb_dollar`` and ``is_collar_surrender_value``, each asked only where the decodes
before it in its cell answer False; and the timings no report reads, the fixed and the
indexed account at each, the account value before the fee, the count before its
lapses.  Those are called here too, the monthly ones in every month of the frame and the
month after it, each timed cell at every code of its family and each kinded cell at its
three kinds, and the engine cells at the arguments ``FIA_US_S``'s own tests use.

The projections run on the committed points alone, and they leave branches untaken: the
female mortality, the spread and trigger methods, the at-exercise step-up, the dollar
rollup base, the surrender-value collar, a joint income below the first band, a
withdrawal programme past its first years, the youngest and oldest issue ages.  That is
enough to type every cell, because every branch of a cell returns the one type its other
branches return, a rate a float in every branch and a phase an int in every branch.  What
the compiled model computes on those branches is not traced but tested: the compile tests
run it on points that take them, and compare it with modelx.  A code a cell refuses,
``pols_if_at(t, BEF_WD)`` or ``claim_from_av_pp(t, ALL)``, is not called: a raise types
nothing.

The eight label accessors are typed from more than the committed points.  Each returns its
point's column as read, and ``Data`` accepts a table whose label is not text: a blank or
numeric ``policy_id``, ``tax_status``, ``glwb_basis`` or ``credit_method``, the first two
read by no cell, the last two read only through their decodes, which answer False; and a
``sex``, ``rollup_id``, ``scenario_id`` or ``wd_schedule_id`` that is a number, where its
table's keys are numbers.  modelx returns the value; an accessor traced on text alone would
compile to ``str`` and raise ``TypeError`` on it.  So the run also calls the eight on a
copy of the table's first point with its four free labels blank and its four keys the
number 1, beside one-key copies of the mortality, rollup, scenario and withdrawal tables
keyed by 1, all written to a temporary directory and read by a second instance of the
export, whose ``Data`` reads them by absolute file names.  mx2cy then types the eight as
Python objects, as the reporting cells they are, and the compiled model returns what modelx
returns.  Nothing is written beside the export, and no other cell is called there but
``model_point``, ``model_point_table`` and ``input_dir``, which are Python objects already,
and the checks ``model_point_table`` runs.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest calls the
# contract allows, check_pols_roll_fwd_resid, expenses and pols_lapse cold in the last month
# of the longest frame, issue age 40, issued now or 120 months on, each need a limit of
# 2,001 in the export, and the reports below, which run in ascending t, need 742, the
# export's import among the frames they run under (measured at M21).  So the build itself
# needs 742, and the rest is margin for an edit that calls a cell cold.  The limit is four
# times the first, rounded up to the thousand, 9,000, which a test holds to this comment.
sys.setrecursionlimit(9_000)

import pandas as pd  # noqa: E402

from FIA_US_SEC_nomx import mx_model  # noqa: E402
from FIA_US_SEC_nomx._mx_model import _c_FIA_US_SEC  # noqa: E402

LABELS = ("policy_id", "sex", "tax_status", "glwb_basis", "credit_method", "rollup_id",
          "scenario_id", "wd_schedule_id")
KEYS = ("sex", "rollup_id", "scenario_id", "wd_schedule_id")

projection = mx_model.Projection
FAMILIES = {
    "pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_MORT", "BEF_LAPSE", "AFT_DECR"),
    "av_pp_at": ("BEF_PREM", "BEF_INV", "BEF_FEE", "BEF_WD", "EOY"),
    "av_fixed_pp_at": ("BEF_PREM", "BEF_INV", "BEF_FEE", "BEF_WD", "EOY"),
    "av_indexed_pp_at": ("BEF_PREM", "BEF_INV", "BEF_FEE", "BEF_WD", "EOY"),
    "av_at": ("BEF_PREM", "BEF_INV", "BEF_FEE", "BEF_WD", "EOY"),
    "benefit_base_pp_at": ("BEF_ROLLUP", "BEF_STEP_UP", "BEF_WD", "EOY"),
    "lw_pp_at": ("BEF_WD", "EOY"),
}
KINDED = ("pols_decr", "claim_pp", "claim_from_av_pp", "claims", "claims_from_av",
          "claims_over_av")
KINDS = ("DEATH", "LAPSE", "MATURITY")
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_av()
    p.result_glwb()
    p.result_cf_annual()
    p.check_av_roll_fwd()
    p.check_pols_roll_fwd()
    p.model_point(), p.point_id()
    for label in LABELS:
        getattr(p, label)()
    p.bonus_factor()
    p.is_credit_spread(), p.is_credit_trigger(), p.is_step_up_at_exercise()
    p.is_rb_dollar(), p.is_collar_surrender_value()
    for a in (55, 60, 72, 73, 74):
        p.activation_rate(a)
    for r in (-0.1, 0.0, 0.03, 0.1):
        for method in ("cap", "par", "par_cap", "spread", "trigger"):
            p.credit_rate_on(r, method)
    for basis in ("single", "joint"):
        for a in range(40, 121):
            p.payout_rate(a, basis)
    for args in ((0.0, 0.0), (0.02, 0.0), (0.04, 0.01), (0.08, 0.0), (0.08, 0.02)):
        p.mgsv_rate_statutory(*args), p.mgsv_rate_is_compliant(*args)
    for t in range(p.proj_len() + 1):
        p.wd_cum_pp(t)
        p.av_indexed_pp(t)
        for cell, labels in FAMILIES.items():
            for label in labels:
                getattr(p, cell)(t, getattr(projection, label))
        for cell in KINDED:
            for kind in KINDS:
                getattr(p, cell)(t, getattr(projection, kind))
        p.claims_over_av(t, projection.ALL)

data = mx_model.Data
here = data.input_dir()
point = pd.read_csv(here / data.model_point_file).iloc[[0]]
first = point.iloc[0]
point = point.assign(**{label: None for label in LABELS if label not in KEYS},
                     **{key: 1 for key in KEYS})
mort = pd.read_csv(here / data.mort_table_file)
mort = mort[mort["sex"] == first["sex"]].assign(**{"sex": 1})
rollups = pd.read_csv(here / data.rollup_file)
rollups = rollups[rollups["rollup_id"] == first["rollup_id"]].assign(**{"rollup_id": 1})
steps = pd.read_csv(here / data.rate_scenario_file)
steps = steps[steps["scenario_id"] == first["scenario_id"]].assign(**{"scenario_id": 1})
programmes = pd.read_csv(here / data.withdrawal_file)
programmes = programmes[programmes["wd_schedule_id"] == first["wd_schedule_id"]].assign(
    **{"wd_schedule_id": 1})
with tempfile.TemporaryDirectory() as folder:
    second = _c_FIA_US_SEC()
    for ref, table in (("model_point_file", point), ("mort_table_file", mort),
                       ("rollup_file", rollups), ("rate_scenario_file", steps),
                       ("withdrawal_file", programmes)):
        path = pathlib.Path(folder) / getattr(data, ref)
        table.to_csv(path, index=False)
        setattr(second.Data, ref, str(path))
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
