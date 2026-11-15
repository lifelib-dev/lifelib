"""mx2cy's sample run for VUL_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  It switches the
behaviour module on first, ``dyn_behavior_on``, which the shipped References leave off:
off, no report reaches the pricing path behind the funding ratio, the premium
persistency scale or its reader.  With it on, the four reports and the three checks reach
every cell but these: ``model_point`` and the seven label accessors, which only a reader
asks for; ``point_id``, which only a refusal names; ``inv_return_mth``, the unit-value
factor the account chain forms inline; the default and shortfall tests, ``is_default``
and ``is_shortfall``, and their searches, ``first_default_month`` and
``first_shortfall_month``; and the pricing path's three closes, ``sa_pricing_pp``,
``fa_pricing_pp`` and ``av_pricing_pp``, which each opening timing forms itself.  And
they reach some cells at some codes alone: ``pols_if_at`` at ``BEF_MAT``, ``claim_pp`` at
``WITHDRAWAL``'s only through ``withdrawals``, ``claims_from_av`` at ``MATURITY`` never,
and the account cells and ``av_at`` at the timings no formula passes them.  Those are
called here too, the monthly ones in every month of the frame and the month after it,
every account cell at every timing it takes, and the pricing path at every policy month a
point reads, from issue to its last month in cover, at every timing it takes.  A code a
cell refuses is not called, since a raise is not traced.

The projections run on the committed points alone, and they leave branches untaken: a
withdrawal, a SINGLE premium, a point without a surrender charge, the COI rate's cap and
the guaranteed bound binding, mortality capped at 1, a lapse spike above 1, a first-month
pin on a point issued at the valuation date, the corridor pin alone.  That is enough to
type every cell, because every branch of a cell returns the one type its other branches
return, a rate a float in every branch, ``0.0``, ``False`` or ``-1`` outside cover.  What
the compiled model computes on those branches is not traced but tested: the compile tests
run it on points that take them, and compare it with modelx.

The seven label accessors are typed from more than the committed points.  Each returns its
point's column as read, and ``Data`` accepts a table whose label is not text: a blank
``surr_charge_id`` on a point without a charge, or a column of numbers, which pandas reads
as NaN or an int and ``VUL_US_S`` projects, since it never reads the schedule of such a
point; a numeric ``scenario_id``, ``sex`` or ``rate_class`` written so in both files,
which joins and projects as text does; and a blank or numeric ``db_option``,
``qual_test`` or ``premium_type``, which the point's first projection refuses.  modelx
returns the value; an accessor traced on text alone would compile to ``str`` and raise
``TypeError`` on it.  So the run also calls the seven on a copy of the table's first point
with every label blank, written to a temporary directory and read by a second instance of
the export, whose ``Data`` reads it by an absolute ``model_point_file``.  mx2cy then types
the seven as Python objects, as the reporting cells they are, and the compiled model
returns what modelx returns.  Nothing is written beside the export, and no other cell is
called there but ``model_point``, ``model_point_table``, the lineup's check and its ids,
and ``input_dir``, which are typed already.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest cover, issue age 0, needs
# a limit of 2,994 in the export with the behaviour module off and 2,984 with it on, and
# the reports below, which run in ascending t with the module on, need 1,834, the export's
# import among the frames they run under or not: a point in force reads the pricing path
# cold back to issue in its first month, point 8, in force at policy month 888, the
# deepest (measured at M17).  So the build itself needs 1,834, and the rest is margin for
# an edit that calls a cell cold.  The limit is four times the first, rounded up to the
# thousand, 12,000, which a test holds to this comment.
sys.setrecursionlimit(12_000)

import pandas as pd  # noqa: E402

from VUL_US_SEC_nomx import mx_model  # noqa: E402
from VUL_US_SEC_nomx._mx_model import _c_VUL_US_SEC  # noqa: E402

projection = mx_model.Projection
projection.dyn_behavior_on = True          # so the pricing path and its readers are traced
ACCOUNT = (projection.BEF_PREM, projection.BEF_WD, projection.BEF_FEE, projection.BEF_INV,
           projection.BEF_ME)
PRICING = (projection.BEF_PREM, projection.BEF_FEE, projection.BEF_INV)
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_av()
    p.result_net()
    p.check_av_roll_fwd()
    p.check_margin()
    p.check_net_view()
    p.first_default_month()
    p.first_shortfall_month()
    p.model_point(), p.sex(), p.rate_class(), p.db_option(), p.qual_test()
    p.premium_type(), p.surr_charge_id(), p.scenario_id()
    p.point_id()
    n = p.subaccount_count()
    for t in range(p.proj_len() + 1):
        p.is_default(t)
        p.is_shortfall(t)
        p.pols_if_at(t, projection.BEF_MAT)
        for timing in ACCOUNT:
            p.av_pp_at(t, timing)
            p.unloaned_av_pp_at(t, timing)
            p.av_at(t, timing)
            p.fa_pp_at(t, timing)
            p.la_pp_at(t, timing)
            p.loan_bal_pp_at(t, timing)
        p.av_at(t, projection.EOM)
        for i in range(n):
            p.inv_return_mth(t, i)
            for timing in ACCOUNT:
                p.sa_pp_at(t, i, timing)
        p.claim_pp(t, projection.WITHDRAWAL)
        p.claims_from_av(t, projection.MATURITY)
    for m in range(p.duration_mth(p.proj_len() - 1) + 1):   # the path, issue to the end
        p.fa_pricing_pp(m)
        p.av_pricing_pp(m)
        for timing in PRICING:
            p.fa_pricing_pp_at(m, timing)
            p.av_pricing_pp_at(m, timing)
        for i in range(n):
            p.sa_pricing_pp(m, i)
            for timing in PRICING:
                p.sa_pricing_pp_at(m, i, timing)

LABELS = ("sex", "rate_class", "db_option", "qual_test", "premium_type", "surr_charge_id",
          "scenario_id")
data = mx_model.Data
blank = pd.read_csv(data.input_dir() / data.model_point_file).iloc[[0]]
blank = blank.assign(has_surr_charge=False, **{label: None for label in LABELS})
with tempfile.TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "blank_labels.csv"
    blank.to_csv(path, index=False)
    second = _c_VUL_US_SEC()
    second.Data.model_point_file = str(path)
    p = second.Projection[0]
    for label in LABELS:
        getattr(p, label)()
