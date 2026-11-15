"""mx2cy's sample run for SPIA_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The two reports
and the two checks reach every cell but these: ``model_point`` and the five label
accessors, which only a reader asks for; ``point_id``, which only a refusal names;
``premium_tax_rate``, ``premium_net_pp`` and ``qualified``, which the model reports and no
flow reads; ``lives_death``, each life's death density, which the last-death density
replaces in every flow; and ``surr_charge``, the charge the insurer keeps, which no
column shows.  Those are called here too, the monthly ones in every month of the frame and
the month after it, ``lives_death`` for both lives.  Every timing of ``pols_if_at`` and the
one kind of ``claim_pp`` are reached by the reports.  A code a cell refuses is not called,
since a raise is not traced.

The projections run on the committed points alone, and they leave branches untaken:
quarterly, semi-annual and annual payments in arrears, a withdrawal taken, the residual
floor binding, the simple discount, a rating that caps mortality, the age stop inside a
certain period, the installment refund's trim below monthly, a COLA on a refund form.
That is enough to type every cell, because every branch of a cell returns the one type
its other branches return, a rate a float in every branch, ``0.0`` or ``False`` outside
the frame.  What the compiled model computes on those branches is not traced but tested:
the compile tests run it on points that take them, and compare it with modelx.

The label accessors are typed from more than the committed points.  ``form()``,
``reduction_trigger()``, ``payment_timing()`` and ``mort_basis()`` validate their column,
as ``SPIA_US_S``'s do, so each returns text or raises, and compiles to ``str``.  But
``sex(life)`` returns its column as read, and ``Data`` accepts a table whose sex is not
text: a blank on a single-life point's second life, which the committed table holds, or
a number, which pandas reads as an int and ``SPIA_US_S`` projects on the scenario basis,
which never joins a table.  An accessor traced on text alone would compile to ``str`` and
raise ``TypeError`` on a number.  So the run also calls ``sex(1)`` and ``sex(2)`` on a copy
of the table's first point with both sexes blank, written to a temporary directory and
read by a second instance of the export, whose ``Data`` reads it by an absolute
``model_point_file``.  mx2cy then types ``sex`` as a Python object, the reporting cell it
is, and the compiled model returns what modelx returns.  Nothing is written beside the
export, and no other cell is called there but ``model_point``, ``model_point_table`` and
``input_dir``, which are typed already.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest cover, a joint life
# annuity certain issued at 0 and 0 with 1,440 certain months, commencing 120 months on,
# needs a limit of 2,931 in the export (a certain_only annuity at issue age 0, 2,929), and
# the reports below, which run in ascending t, need 154 with the export's import among
# their frames.  So the build itself needs 154, and the rest is margin for an edit that
# calls a cell cold.  The limit is four times the first, rounded up to the thousand,
# 12,000, which a test holds to this comment.
sys.setrecursionlimit(12_000)

import pandas as pd  # noqa: E402

from SPIA_US_SEC_nomx import mx_model  # noqa: E402
from SPIA_US_SEC_nomx._mx_model import _c_SPIA_US_SEC  # noqa: E402

projection = mx_model.Projection
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.check_lives_roll_fwd()
    p.check_payment_factor()
    p.model_point(), p.form(), p.reduction_trigger(), p.payment_timing(), p.mort_basis()
    p.sex(1), p.sex(2)
    p.point_id(), p.premium_tax_rate(), p.premium_net_pp(), p.qualified()
    for t in range(p.proj_len() + 1):
        p.lives_death(t, 1)
        p.lives_death(t, 2)
        p.surr_charge(t)

data = mx_model.Data
blank = pd.read_csv(data.input_dir() / data.model_point_file).iloc[[0]]
blank = blank.assign(primary_sex=None, joint_sex=None)
with tempfile.TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "blank_sex.csv"
    blank.to_csv(path, index=False)
    second = _c_SPIA_US_SEC()
    second.Data.model_point_file = str(path)
    p = second.Projection[0]
    p.sex(1), p.sex(2)
    del p, second
