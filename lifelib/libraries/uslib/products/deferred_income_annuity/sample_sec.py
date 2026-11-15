"""mx2cy's sample run for DIA_US_SEC: the calls that type every cell.

mx2cy compiles the model's export, and it types each cell from the values this run passes
it and gets back: a cell it never calls compiles as a Python object, with a dict cache,
and the typing guard fails on it (USLIB-SEC-PLAN.md F3, C3).  So the run calls every
``Projection`` cell at least once, on every point of the committed table.  The three
reports and the four checks reach every cell but these: ``model_point`` and the label
accessors, which only a reader asks for; ``point_id``, which only a refusal names; the
cells ``DIA_US_S`` keeps for a reader, ``guarantee_yrs``, ``accel_cost``,
``payout_factor_calc``, ``is_qlac``, ``other_qlac_premium`` and the three that return a
DataFrame, a dict and a list, ``premium_schedule``, ``premium_by_mth`` and
``qlac_flags``; the two engine cells of float parameters, ``annuity_factor`` and
``pricing_disc_factor``, which no other cell calls, called at the arguments
``DIA_US_S``'s payout factor passes; and over the frame and the month after it, ``phase``,
``accel_payment_factor``, ``cola_factor``, ``calendar_year`` and ``qlac_room``, and for
each covered life the attained age, the base-table rate, the improvement rate and the
deaths, which the rates by policy year replace in every flow.  Those are called here too.
Every timing of ``pols_if_at``, the two kinds of ``claim_pp`` and the three of ``claims``
are reached by the reports, the start-date adjustment's two bases of
``annuity_factor_at`` by the adjusting point and its purchase basis by every point on the
formula basis.  A call a cell refuses is not made, since a raise is not traced: the
second life's age on a single life reads a blank ``joint_age``, and ``claim_pp`` refuses
the total.

The projections run on the committed points alone, and they leave branches untaken:
payments other than monthly, the ``LO_ROP`` form, a part commutation, the table basis on a
male life, the generational basis on a joint life, an installment refund in advance whose
income starts at the age stop.  That is enough to type every cell, because every branch
of a cell returns the one type its other branches return, a rate a float in every branch,
``0.0`` or ``False`` outside the frame.  What the compiled model computes on those
branches is not traced but tested: the compile tests run it on points that take them, and
compare it with modelx.

The label accessors are typed from more than the committed points.  ``market_type()``,
``income_form()``, ``payout_form()``, ``db_form()``, ``payment_timing()``,
``mort_basis()``, ``factor_basis()`` and ``reduction_trigger()`` validate their column,
as ``DIA_US_S``'s do, so each returns text or raises, and compiles to ``str``.  But
``sex(life)`` returns its column as read, and ``Data`` accepts a single-life point whose
``joint_sex`` is not text: a blank, which the committed table holds, or a number, which
pandas reads as an int and no projection reads.  An accessor traced on text alone would
compile to ``str`` and raise ``TypeError`` on a number.  So the run also calls ``sex(2)``
on a copy of the table's first point, a single life, with its ``joint_sex`` blank,
written to a temporary directory and read by a second instance of the export, whose
``Data`` reads it by an absolute ``model_point_file``; ``Data`` refuses a ``sex`` other
than M or F on every point, so ``sex(1)`` is text.  mx2cy then types ``sex`` as a Python
object, the reporting cell it is, and the compiled model returns what modelx returns.
Nothing is written beside the export, and no other cell is called there but
``model_point``, ``model_point_table`` and ``input_dir``, which are typed already: the
premium schedule names points the copy lacks, and no call reads it.
"""
import pathlib
import sys
import tempfile

# The export does not raise the recursion limit as modelx does (F7).  The deepest call the
# contract allows, a cold net_cf in the last month of the longest cover, a cash refund
# issued at 0 and commencing 1,440 months of cover 120 months on, needs a limit of 2,924
# in the export (an installment refund 2,899), and the reports and checks below, which run
# in ascending t, need 48 from a script's top level, and 64 where the installment refund's
# twin is the first point read (measured at M24).  So the build itself needs 48, and the
# rest is margin for an edit that calls a cell cold.  The limit is four times the first,
# rounded up to the thousand, 12,000, which a test holds to this comment.
sys.setrecursionlimit(12_000)

import pandas as pd  # noqa: E402

from DIA_US_SEC_nomx import mx_model  # noqa: E402
from DIA_US_SEC_nomx._mx_model import _c_DIA_US_SEC  # noqa: E402

LABELS = ("market_type", "income_form", "payout_form", "db_form", "payment_timing",
          "mort_basis", "factor_basis", "reduction_trigger")

projection = mx_model.Projection
for idx in range(len(mx_model.Data.model_point_table())):
    p = projection[idx]
    p.result_cf()
    p.result_pols()
    p.result_annual()
    p.check_lives_roll_fwd()
    p.check_income_roll_fwd()
    p.check_payment_factor()
    p.check_commutation_value()
    p.model_point(), p.point_id()
    for label in LABELS:
        getattr(p, label)()
    p.sex(1), p.sex(2)
    p.premium_schedule(), p.premium_by_mth(), p.qlac_flags()
    p.guarantee_yrs(), p.accel_cost(), p.payout_factor_calc()
    p.is_qlac(), p.other_qlac_premium()
    start = p.income_start_mth()
    p.annuity_factor(start, p.guarantee_mths_pricing(), projection.pricing_rate, start)
    p.pricing_disc_factor(20.0)
    lives = (1, 2) if p.is_joint() else (1,)
    for t in range(p.proj_len() + 1):
        p.phase(t)
        p.accel_payment_factor(t)
        p.cola_factor(t)
        p.calendar_year(t)
        p.qlac_room(t)
        for life in lives:
            p.age(t, life)
            p.mort_rate_base(t, life)
            p.improvement_rate(t, life)
            p.lives_death(t, life)

data = mx_model.Data
blank = pd.read_csv(data.input_dir() / data.model_point_file).iloc[[0]]
blank = blank.assign(joint=False, joint_sex=None)
with tempfile.TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "blank_sex.csv"
    blank.to_csv(path, index=False)
    second = _c_DIA_US_SEC()
    second.Data.model_point_file = str(path)
    p = second.Projection[0]
    p.sex(1), p.sex(2)
    del p, second
