"""mx2cy's sample run for IUL_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The four
reports and the four checks reach every cell but these: ``model_point`` and the seven
label accessors, which only a reader asks for; ``point_id``, which only a refusal names;
``is_target_premium``, which every committed point, paying a LEVEL premium, decides
before it is asked; ``cum_prem_init``, ``is_mec_init``, ``gsp``, ``glp`` and
``seven_pay_prem``, which the guideline and 7-pay tests read; those tests themselves,
``gpt_ok``, ``is_mec``, ``gpt_limit``, ``seven_pay_limit`` and ``cum_prem_pp``; the
shortfall test, ``is_shortfall``; and the five engine cells, which no projection cell
calls (R14).  And they reach some cells at some codes alone: ``pols_if_at`` at
``BEF_MAT`` never, ``av_at`` only at ``BEF_PREM``, ``claims_from_av`` at ``MATURITY``
never.  Those are called here too, the monthly ones in every month of the frame and the
month after it, at every code they take but the ones the reports pass.  A code a cell
refuses is not called, since a raise is not traced.

The engine cells are called with every defaulted parameter both at its ``None`` default
and at a value: mx2cy types a parameter it sees only at a float or an int as a C
``double`` or ``long long`` and keeps its ``None`` default, which Cython refuses, so the
build fails; a parameter traced at ``None`` and at a value types as an object, as the
engine cell's dict cache keeps it.  Their arguments are the worked example's.

The projections run on the committed points alone, and they leave branches untaken: a
TARGET or a SINGLE premium, Option B's corridor on an exhausted account, the guaranteed
basis, the adjusted-beginning credit base, a point without a surrender charge, a lapse
shock year in frame.  That is enough to type every cell, because every branch of a cell
returns the one type its other branches return, a rate a float in every branch, ``0.0``,
``False`` or ``0`` outside cover.  What the compiled model computes on those branches is
not traced but tested: the compile tests run it on points that take them, and compare it
with modelx.

The seven label accessors are typed from more than the committed points.  Each returns its
point's column as read, and ``Data`` accepts a table whose label is not text: a blank
``surr_charge_id`` on a point without a charge, which pandas reads as NaN and
``IUL_US_S`` projects, since it never reads the schedule of such a point; and a blank or
numeric ``sex``, ``rate_class``, ``db_option``, ``qual_test``, ``premium_type`` or
``premium_mode``, which the point's first projection refuses.  modelx returns the value;
an accessor traced on text alone would compile to ``str`` and raise ``TypeError`` on it.
So the run also calls the seven on a copy of the table's first point with every label
blank, written to a temporary directory and read by a second instance of the export,
whose ``Data`` reads it by an absolute ``model_point_file``.  mx2cy then types the seven
as Python objects, as the reporting cells they are, and the compiled model returns what
modelx returns.  Nothing is written beside the export, and no other cell is called there
but ``model_point``, ``model_point_table`` and ``input_dir``, which are typed already.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest frame, issue age 0,
# needs a limit of 2,966 in the export, issued now or 120 months on, and the reports
# below, which run in ascending t, need 438, the guarantee's expiry on the twin of S point
# 5 and on point 8, S point 5 restated at 6, reading the account value cold back to
# policy month 49 (128 on the other points with the export's import among the frames, 60
# to 64 once it has returned; measured at M19).  So the build itself needs 438,
# and the rest is margin for an edit that calls a cell cold.  The limit is four times the
# first, rounded up to the thousand, 12,000, which a test holds to this comment.
sys.setrecursionlimit(12_000)

import pandas as pd  # noqa: E402

from IUL_US_SEC_nomx import mx_model  # noqa: E402
from IUL_US_SEC_nomx._mx_model import _c_IUL_US_SEC  # noqa: E402

projection = mx_model.Projection
ACCOUNT = (projection.BEF_PREM, projection.BEF_CREDIT, projection.BEF_WD,
           projection.BEF_FEE, projection.BEF_INV)
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_av()
    p.result_seg()
    p.check_av_components()
    p.check_av_roll_fwd()
    p.check_seg_ladder()
    p.check_margin()
    p.model_point(), p.sex(), p.rate_class(), p.db_option(), p.qual_test()
    p.premium_type(), p.premium_mode(), p.surr_charge_id()
    p.point_id()
    p.is_target_premium(), p.cum_prem_init(), p.is_mec_init()
    p.gsp(), p.glp(), p.seven_pay_prem()
    for t in range(p.proj_len() + 1):
        p.gpt_ok(t)
        p.is_mec(t)
        p.is_shortfall(t)
        p.pols_if_at(t, projection.BEF_MAT)
        for timing in ACCOUNT:
            p.av_at(t, timing)
        p.av_at(t, projection.EOM)
        p.claims_from_av(t, projection.MATURITY)
    # The engine, kept for S's worked example and called by no projection cell: each
    # defaulted parameter at its None default and at a value (the module docstring).
    p.index_change(4500.0, 5040.0)
    p.index_credit_rate(0.12)
    p.index_credit_rate(0.12, 0.02)
    p.seg_credit_base(12000.0, 180.0)
    p.seg_credit_base(12000.0, 180.0, projection.ADJ_BEGIN)
    p.index_credit(12000.0, 180.0, 0.12)
    p.index_credit(12000.0, 180.0, 0.12, projection.REMAINING, 0.1)
    p.seg_matured_value(12000.0, 180.0, 0.12)
    p.seg_matured_value(12000.0, 180.0, 0.12, projection.REMAINING, 0.1)

LABELS = ("sex", "rate_class", "db_option", "qual_test", "premium_type", "premium_mode",
          "surr_charge_id")
data = mx_model.Data
blank = pd.read_csv(data.input_dir() / data.model_point_file).iloc[[0]]
blank = blank.assign(has_surr_charge=False, **{label: None for label in LABELS})
with tempfile.TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "blank_labels.csv"
    blank.to_csv(path, index=False)
    second = _c_IUL_US_SEC()
    second.Data.model_point_file = str(path)
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
