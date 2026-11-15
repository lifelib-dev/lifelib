"""mx2cy's sample run for MYGA_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The three
reports and the two checks reach every cell but twenty, and every code but two: the
cells ``model_point`` and the ten label accessors, which only a reader asks for;
``point_id``, which only a refusal names; the three engine cells,
``mgsv_rate_statutory``, ``mgsv_rate_is_compliant`` and ``mva_ref_term_years``, which no
projection cell calls; the investment in the contract, ``tax_basis_pp``, with
``taxable_wd_pp`` and ``tax_basis_pp_init``, which only it reads; ``gp_end``, the months
left in the guarantee period; and ``claims_over_av``, the benefit paid above the account
value, at every kind and ``ALL``, none of which a report reads; and the codes ``EOM`` of
``av_pp_at`` and ``BEF_WD`` of ``av_at``, cells the reports reach, at codes no formula
passes them.  Those are called here too, the monthly ones in every month of the frame and
the month after it, and the engine cells at one argument each, the arguments
``MYGA_US_S``'s own tests use.

The projections run on the committed points alone, and they leave branches untaken: the
female mortality, the GMIR's other bands, a schedule that runs out, a declared-
differential term past the factor table's last year, the attained-age cap, utilization
withdrawals.  That is enough to type every cell, because every branch of a cell returns
the one type its other branches return, a rate a float in every branch and the whole
years of the MVA term an int in every branch.  What the compiled model computes on those
branches is not traced but tested: the compile tests run it on points that take them, and
compare it with modelx.  A code a cell refuses, ``pols_if_at(t, BEF_WD)`` or
``claim_pp(t, ALL)``, is not called: a raise types nothing.

The ten label accessors are typed from more than the committed points.  Each returns its
point's column as read, and ``Data`` accepts a table whose label is not text: a blank or
numeric ``policy_id`` or ``tax_status``, which no cell reads; a ``renewal_architecture``,
``mgsv_wd_convention``, ``free_wd_rule``, ``mva_family`` or ``mva_cap_rule`` none of whose
flags it names, which ``MYGA_US_S`` projects or refuses where it asks; and a ``sex``,
``scenario_id`` or ``wd_schedule_id`` that is a number, where its table's keys are
numbers.  modelx returns the value; an accessor traced on text alone would compile to
``str`` and raise ``TypeError`` on it.  So the run also calls the ten on a copy of the
table's first point with its seven free labels blank and its three keys the number 1,
beside one-key copies of the mortality, scenario and withdrawal tables keyed by 1, all
written to a temporary directory and read by a second instance of the export, whose
``Data`` reads them by absolute file names.  mx2cy then types the ten as Python objects,
as the reporting cells they are, and the compiled model returns what modelx returns.
Nothing is written beside the export, and no other cell is called there but
``model_point``, ``model_point_table`` and ``input_dir``, which are Python objects already,
and the checks ``model_point_table`` runs; the point's projection would raise
``invalid free_wd_rule``, as ``MYGA_US_S``'s would.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest frame, issue age 0,
# issued now or 120 months on, needs a limit of 2,444 in the export, and the reports
# below, which run in ascending t, need 128, the export's import among the frames they
# run under (54 once the import has returned; measured at M20).  So the build itself needs
# 128, and the rest is margin for an edit that calls a cell cold.  The limit is four times
# the first, rounded up to the thousand, 10,000, which a test holds to this comment.
sys.setrecursionlimit(10_000)

import pandas as pd  # noqa: E402

from MYGA_US_SEC_nomx import mx_model  # noqa: E402
from MYGA_US_SEC_nomx._mx_model import _c_MYGA_US_SEC  # noqa: E402

LABELS = ("policy_id", "sex", "tax_status", "mgsv_wd_convention", "renewal_architecture",
          "free_wd_rule", "mva_family", "mva_cap_rule", "scenario_id", "wd_schedule_id")
KEYS = ("sex", "scenario_id", "wd_schedule_id")

projection = mx_model.Projection
kinds = (projection.DEATH, projection.LAPSE, projection.ANNUITIZATION,
         projection.MATURITY, projection.ALL)
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_av()
    p.check_av_roll_fwd()
    p.check_pols_roll_fwd()
    p.model_point(), p.point_id()
    for label in LABELS:
        getattr(p, label)()
    p.mgsv_rate_statutory(0.02), p.mgsv_rate_is_compliant(0.02)
    p.mva_ref_term_years(985 / 365.25)
    for t in range(p.proj_len() + 1):
        p.tax_basis_pp(t)
        p.gp_end(t)
        p.av_pp_at(t, projection.EOM)
        p.av_at(t, projection.BEF_WD)
        for kind in kinds:
            p.claims_over_av(t, kind)

data = mx_model.Data
here = data.input_dir()
point = pd.read_csv(here / data.model_point_file).iloc[[0]]
point = point.assign(**{label: None for label in LABELS if label not in KEYS},
                     **{key: 1 for key in KEYS})
mort = pd.read_csv(here / data.mort_table_file)
mort = mort[mort["sex"] == "M"].assign(**{"sex": 1})
steps = pd.read_csv(here / data.rate_scenario_file)
steps = steps[steps["scenario_id"] == "base"].assign(**{"scenario_id": 1})
programmes = pd.read_csv(here / data.withdrawal_file)
programmes = programmes[programmes["wd_schedule_id"] == "anchor"].assign(
    **{"wd_schedule_id": 1})
with tempfile.TemporaryDirectory() as folder:
    second = _c_MYGA_US_SEC()
    for ref, table in (("model_point_file", point), ("mort_table_file", mort),
                       ("rate_scenario_file", steps), ("withdrawal_file", programmes)):
        path = pathlib.Path(folder) / getattr(data, ref)
        table.to_csv(path, index=False)
        setattr(second.Data, ref, str(path))
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
