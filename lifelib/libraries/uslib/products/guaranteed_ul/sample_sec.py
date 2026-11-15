"""mx2cy's sample run for ULSG_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The four
reports and the three checks reach every cell but eight, and every code but eight: the
cells ``model_point`` and the five label accessors, which only a reader asks for;
``point_id``, which only a refusal names; and ``cure_premium_pp``, the payment that would
cure a grace, a diagnostic no report shows; and the codes ``BEF_MAT`` of ``pols_if_at``,
``BEF_WD``, ``BEF_FEE``, ``BEF_COI``, ``BEF_INV`` and ``EOM`` of ``av_at``, ``GRACE`` of
``claim_pp``, and ``WITHDRAWAL`` and ``MATURITY`` of ``claims_from_av``, cells the reports
reach, at codes no formula passes them.  Those are called here too, the monthly ones in
every month of the frame and the month after it.  Every committed point carries a load
below 1, so ``cure_premium_pp`` divides by no zero here; it is called apart from the codes,
on the committed points alone.

The projections run on the committed points alone, and they leave branches untaken:
withdrawals, the TEN_PAY pattern, the non-annual modes, a single premium's lapse factor,
the corridor binding, the lapse rate's cap, the cap on mortality and a loan.  That is
enough to type every cell, because every branch of a cell returns the one type its other
branches return, a rate a float in every branch.  What the compiled model computes on
those branches is not traced but tested: the compile tests run it on points that take
them, and compare it with modelx.  The two ``round`` calls of ``coi_rate`` and
``sg_coi_rate`` are reached on points 1 and 5, which pin the precision.

The five label accessors are typed from more than the committed points.  Each returns its
point's column as read, and ``Data`` accepts a table whose label is not text: a blank
``surr_charge_id`` on a point without a charge, or a column of numbers, which pandas reads
as NaN or an int and ``ULSG_US_S`` projects, since it never reads the schedule of such a
point; a blank or numeric ``premium_mode`` on a SINGLE point, which never reads its mode;
and a blank or numeric ``premium_type``, ``sex`` or ``rate_class``, which the point's
first projection, or ``Data``'s join, refuses.  modelx returns the value; an accessor
traced on text alone would compile to ``str`` and raise ``TypeError`` on it.  So the run
also calls the five on a copy of the table's first point with every label blank, written
to a temporary directory and read by a second instance of the export, whose ``Data``
reads it by an absolute ``model_point_file``.  mx2cy then types the five as Python
objects, as the reporting cells they are, and the compiled model returns what modelx
returns.  Nothing is written beside the export, and no other cell is called there but
``model_point``, ``model_point_table`` and ``input_dir``, which are Python objects already.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest frame, issue age 18,
# needs a limit of 2,526 in the export, and the reports below, which run in ascending t,
# need 128, the export's import among the frames they run under (measured at M18; 58 once
# the import has returned).  So the build itself needs 128, and the rest is margin for an
# edit that calls a cell cold.  The limit is four times the first, rounded up to the
# thousand, 11,000, which a test holds to this comment.
sys.setrecursionlimit(11_000)

import pandas as pd  # noqa: E402

from ULSG_US_SEC_nomx import mx_model  # noqa: E402
from ULSG_US_SEC_nomx._mx_model import _c_ULSG_US_SEC  # noqa: E402

projection = mx_model.Projection
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_av()
    p.result_guar()
    p.check_av_roll_fwd()
    p.check_sg_roll_fwd()
    p.check_margin()
    p.model_point(), p.sex(), p.rate_class(), p.premium_type(), p.premium_mode()
    p.surr_charge_id(), p.point_id()
    for t in range(p.proj_len() + 1):
        p.cure_premium_pp(t)
    for t in range(p.proj_len() + 1):
        p.pols_if_at(t, projection.BEF_MAT)
        for timing in (projection.BEF_WD, projection.BEF_FEE, projection.BEF_COI,
                       projection.BEF_INV, projection.EOM):
            p.av_at(t, timing)
        p.claim_pp(t, projection.GRACE)
        for kind in (projection.WITHDRAWAL, projection.MATURITY):
            p.claims_from_av(t, kind)

LABELS = ("sex", "rate_class", "premium_type", "premium_mode", "surr_charge_id")
data = mx_model.Data
blank = pd.read_csv(data.input_dir() / data.model_point_file).iloc[[0]]
blank = blank.assign(has_surr_charge=False, **{label: None for label in LABELS})
with tempfile.TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "blank_labels.csv"
    blank.to_csv(path, index=False)
    second = _c_ULSG_US_SEC()
    second.Data.model_point_file = str(path)
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
