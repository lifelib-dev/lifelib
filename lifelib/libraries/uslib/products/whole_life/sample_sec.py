"""mx2cy's sample run for WholeLife_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The four
reports and the two checks reach every cell but eleven, and every timing but one: the
cells ``model_point`` and the six label accessors, which only a reader asks for;
``point_id``, which only a refusal names; ``mec_flag`` and ``policy_year``, which no cell
reads; ``dyn_lapse_factor``, which the lapse rate reads only with its overlay
switched on, and it ships off; and the timing ``AFT_DECR`` of ``pols_if_at``, a cell the
reports reach, the one timing no formula asks for.  Those are called here too,
``policy_year``, ``dyn_lapse_factor`` and ``pols_if_at`` at ``AFT_DECR`` in every month of
the frame and the month after it, and so is the count carried into that month, which the
roll-forward reads.

The run takes the committed points alone, and they leave branches untaken: the
semi-annual and quarterly cycles, the twenty-year and to-65 premium periods, the three
overlays and the dividend on the paid-up additions, all shipped off, rounding switched off,
the cap on mortality.  That is enough to type every cell, because every branch of a cell
returns the one type its other branches return, a count a float in every branch.  What
the compiled model computes on those branches is not traced but tested: the compile
tests run it on points that take them, and compare it with modelx.

The six label accessors are typed from more than the committed points.  Each returns its
point's column as read, and ``Data`` accepts a table whose label is blank, which pandas
reads as NaN, or a number, on a point that carries no paid-up additions, dividends or
rider premium, which a product other than WL_PAR may not carry: modelx returns the value
as it is, and the point's first projection refuses it.  An accessor traced on text alone
would compile to ``str`` and raise ``TypeError`` on it.  So the run also calls the six on
a copy of the table's first point with every label blank and those five amounts 0,
written to a temporary directory and read by a second instance of the export, whose
``Data`` reads it by an absolute ``model_point_file``.  mx2cy then types the six as Python
objects, as the reporting cells they are, and the compiled model returns what modelx
returns.  Nothing is written beside the export, and no other cell is called there but
``model_point``, ``model_point_table`` and ``input_dir``, which are Python objects already.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest frame, issue age 0, needs
# a limit of 2,448 in the export, and the reports below, which run in ascending t, need
# 128 (measured at M15).  So the build itself needs 128, and the rest is margin for an
# edit that calls a cell cold.  The limit is four times the first, rounded up to the
# thousand, 10,000, which a test holds to this comment.
sys.setrecursionlimit(10_000)

import pandas as pd  # noqa: E402

from WholeLife_US_SEC_nomx import mx_model  # noqa: E402
from WholeLife_US_SEC_nomx._mx_model import _c_WholeLife_US_SEC  # noqa: E402

projection = mx_model.Projection
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_cv()
    p.result_cf_annual()
    p.check_pols_roll_fwd()
    p.check_pua_roll_fwd()
    p.model_point(), p.product(), p.premium_period(), p.sex(), p.risk_class()
    p.dividend_option(), p.premium_mode()
    p.point_id(), p.mec_flag()
    for t in range(p.proj_len() + 1):
        p.policy_year(t)
        p.dyn_lapse_factor(t)
        p.pols_if_at(t, projection.AFT_DECR)
    p.pols_if_at(p.proj_len(), projection.BEF_NB)

LABELS = ("product", "premium_period", "sex", "risk_class", "dividend_option",
          "premium_mode")
DIVIDEND_STATE = ("pua_rider_premium", "pua_face_init", "pua_face_prev_anniv_init",
                  "div_accum_init", "div_prev_anniv_init")
data = mx_model.Data
blank = pd.read_csv(data.input_dir() / data.model_point_file).iloc[[0]]
blank = blank.assign(**{label: None for label in LABELS},
                     **{column: 0.0 for column in DIVIDEND_STATE})
with tempfile.TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "blank_labels.csv"
    blank.to_csv(path, index=False)
    second = _c_WholeLife_US_SEC()
    second.Data.model_point_file = str(path)
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
    del p, second
