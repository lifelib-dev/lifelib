# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.IUL_US_SEC.Projection` as ``data``. :mod:`~.IUL_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized Space
reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/indexed_ul/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values --
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IUL_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Six of the tables are IUL_US_S's.** The guaranteed COI scale, the corridor factors,
the mortality table, the class factors, the lapse table and the surrender charge
schedules are the files :mod:`~.IUL_US_S` reads, read here in place: one copy of each
table serves both models, so an edit to one reaches both. The model point table and the
segment ladder are this model's own, ``model_point_table_sec.csv`` and
``inforce_segments_sec.csv``; the first sits beside ``IUL_US_S``'s
``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
inforce_segments_file   inforce_segments()          inforce_segments_sec.csv
coi_rates_file          coi_rates()                 coi_rates.csv
corridor_file           corridor_factors()          corridor_factors.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
surr_charge_file        surr_charge_table()         surr_charge_table.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Ten of its columns are the in-force
interface: ``policy_count`` and ``duration_mth``, as in ``basiclife.BasicTerm_SE``, and
eight columns of an in-force policy's opening state, the account value and the loan,
which are ``IUL_US_S``'s own, the fixed account and the loan collateral apart from the
loan, the face in force, the premiums paid to date, the no-lapse accumulator and the MEC
latch. :func:`model_point_table` refuses a table that lacks any of them, or any column of
``IUL_US_S``'s own that the projection reads as a number or a flag, repeats a
``point_id``, holds a count, a duration, an age, a policy year or an amount no policy can
have, a share of the premium or of the fixed account outside 0 to 1, a flag that is not
``True`` or ``False``, or an opening state no policy can be in. The checks run in turn, by
20 rules, and the first that fails raises, naming the missing column or every point that
fails it. It also refuses a policy to be issued more than ``future_horizon_mth`` months
after the valuation date, 120 months as shipped: future new business is written over a
stated horizon, so that no frame runs longer than the projection from issue plus that
horizon. Set to 0, the Reference refuses future new business altogether. Whether a point
is still inside the projection at the valuation date, issued at an age with any cover,
withdrawing less than its fee, or holding one ladder row for each live segment is a rule
of the product rather than of the table, and ``Projection.proj_len`` checks it.

**So is the segment ladder.** ``IUL_US_S`` opens a point with no live segment, its whole
account value outside the collateral in the fixed account, which re-opening a policy in
force restates wrongly. So each live segment of a point in force is a row of
``inforce_segments_sec.csv``, keyed by ``point_id`` and ``slot``, the months since the
segment's creation at the valuation date, with its balance, the deductions and draws
charged to it, the index level at its creation and the cap declared then.
:func:`inforce_segments` refuses a row that names no point of the table, repeats a
slot, has a slot outside its point's life, or holds a value no segment can, and a point
whose account value is not its fixed account, its collateral and its segments, to the
cent. :func:`inforce_segment_count` and :func:`inforce_segment_last` give each point's
row count and last slot, which ``Projection.proj_len`` holds to the segments a policy in
force holds, one a month for its last twelve.

**So are the six assumption tables.** Each table read at an attained age or a policy
year has one reader in ``Projection``, keyed by the age or the year, and that reader
takes the table's extent -- the first and last ages, or the last policy year, beyond
which it reads the nearest row -- from a cell here that reads the key column by value,
once, and checks the table: :func:`corridor_age_first` and :func:`corridor_age_last`,
:func:`mort_age_first` and :func:`mort_age_last`, :func:`lapse_last_year`, and, for the
COI scale, whose issue-age cells are numbered as schedules, :func:`coi_schedules`, which
every COI vector asks first. A key that is blank, text or not a whole number is refused,
naming the file, the column and the lines it is on, and so is an age below 0 in the
corridor and mortality tables, since each is indexed by the age. So are keys that do not
run one row an age or a year, without a gap or a repeat, policy years from 1, the message
naming each key that repeats, with its lines, and each that is missing. And so is a rate
that is blank, text or infinite, naming the column and its lines, and a lapse or
mortality rate outside 0 to 1: each is a probability, and the monthly rate
``1 - (1 - q)^(1/12)`` has no real value past 1. :func:`class_count` and
:func:`surr_charge_count` check the class factors and the surrender-charge schedules the
same way, for the per-point joins that read them, and :func:`surr_charge_count` refuses a
run-off that is not a whole number of years, 1 or more, which the projection divides by.
A class factor, a guaranteed COI rate and a surrender charge below 0 are refused too:
each would project, with every check passing, a negative death, a credit for the
insurance, or a surrender charge that rises once its schedule has run off. So is a
corridor factor below 0, which no statutory percentage is, and which ``IUL_US_S``'s death
benefit, the ``max`` of the face and the corridor's amount with no floor on the account
value, would turn above the face on an exhausted account. Each reader asks for its extent
or its count before it reads a value, so a projection meets the checks first.

``IUL_US_S``'s readers take each extent from the key column as pandas reads it, where a
blank key is a missing value the extent skips: the table is cut short, and every later
age or year reads the last good row, without a word. A blank value is a missing value
to it too, which shows in its flows or is lost in a ``min`` or a ``max``: a blank lapse
rate reaches the lapse cap's ``min`` and is read as the cap, a blank corridor factor
reads as no corridor, and a blank surrender charge as none. Here each is refused, by
name, and so is a blank, text or infinite amount in the model point table.

``coi_rates.csv`` carries the *guaranteed maximum* monthly rate per $1,000 of net amount
at risk; the notes set that basis at 2017 CSO ANB ultimate [REG-R17], which may not be
reproduced here, and the current scale is the guaranteed scale times
``Projection.coi_curr_factor`` (65% **[std]**) because carrier COI tables are not public.
``mort_table.csv`` is a small illustrative best-estimate table **[std]**, not the 2015
VBT the notes recommend [REG-R18]; it is the same illustrative table shipped with
``UL_US_S``, so the chassis and this model share a basis.

There is deliberately **no premium persistency table**. The universal life chassis reads
one, because its notes give a 16-row schedule; these notes instead give a closed form --
``expected premium_y = planned x 0.98^(y-1)`` -- which is implemented as
:func:`~.IUL_US_SEC.Projection.prem_persistency` with the rate in a Reference. Nor is
there an index scenario file: the base deterministic run generates
:func:`~.IUL_US_SEC.Projection.index_level` from a level annual return on the valuation
clock, and a stochastic or historical path is substituted by overriding that one cell,
a formula override, which only modelx can make; compiled, the path is changed by editing
the formula and rebuilding.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name before the model computes
anything: a compiled model clears no cache, so there the name is set on a package just
imported, before anything is read. No formula changes. Replacing the file changes
:mod:`~.IUL_US_S` too, which reads the same one.

**The vectors.** The readers return what the files hold, and no
:mod:`~.IUL_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them.
The others read the arrays below instead, one element at a time, a model point's
attribute being the element at its position, ``data.sum_assured()[idx]``. That is what
lets the model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy
vector or table of int64 or float64, which compiles to a typed memoryview, never one of
bools, objects or text, and each count or extent is an int.

Text the projection needs is decoded here, into the number it selects: each value of the
death benefit option, the qualification test, the premium pattern and the premium mode a
monthly cell branches on into a 0/1 flag, and the surrender-charge flag into another.
Each table keyed by more than a number becomes an integer-indexed array or a join. The
COI scales, keyed by sex, class and issue age, are numbered, each point carrying the
number of its own, and tabled by schedule and policy year. The lapse table is held by
policy year, the corridor and mortality tables by attained age, each padded from 0, so
that the year or the age is the index. The segment ladder, keyed by point and slot, is
held by the point's position and the slot, so that the slot is the column. The class
factor and the surrender-charge schedule, each one number a point, are joined to the
points:

================================  =======  ===============  ==============================
Cells                             dtype    Shape            From
================================  =======  ===============  ==============================
point_id()                        int64    [point]          the table's index
age_at_entry()                    int64    [point]          ``age_at_entry``
duration_mth()                    int64    [point]          ``duration_mth``
wd_first_year()                   int64    [point]          ``wd_first_year``
loan_first_year()                 int64    [point]          ``loan_first_year``
is_mec_init()                     int64    [point]          ``is_mec_init``, by value
has_surr_charge()                 int64    [point]          ``has_surr_charge``, 1 on True
is_db_option_a()                  int64    [point]          ``db_option``, 1 on A
is_db_option_b()                  int64    [point]          ``db_option``, 1 on B
is_gpt()                          int64    [point]          ``qual_test``, 1 on GPT
is_level_premium()                int64    [point]          ``premium_type``, 1 on LEVEL
is_single_premium()               int64    [point]          ``premium_type``, 1 on SINGLE
is_target_premium()               int64    [point]          ``premium_type``, 1 on TARGET
is_annual_premium()               int64    [point]          ``premium_mode``, 1 on ANNUAL
is_monthly_premium()              int64    [point]          ``premium_mode``, 1 on MONTHLY
sum_assured()                     float64  [point]          ``sum_assured``
policy_count()                    float64  [point]          ``policy_count``
premium_pp_ann()                  float64  [point]          ``premium_pp_ann``
wd_pp()                           float64  [point]          ``wd_pp``
loan_new_pp_ann()                 float64  [point]          ``loan_new_pp_ann``
mnlp_rate()                       float64  [point]          ``mnlp_rate``
gsp()                             float64  [point]          ``gsp``
glp()                             float64  [point]          ``glp``
seven_pay_prem()                  float64  [point]          ``seven_pay_prem``
load_prem_rate()                  float64  [point]          ``load_prem_rate``
index_alloc_rate()                float64  [point]          ``index_alloc_rate``
av_pp_init()                      float64  [point]          ``av_pp_init``
loan_bal_init()                   float64  [point]          ``loan_bal_init``
fa_pp_init()                      float64  [point]          ``fa_pp_init``
lca_pp_init()                     float64  [point]          ``lca_pp_init``
sum_assured_init()                float64  [point]          ``sum_assured_init``
cum_prem_init()                   float64  [point]          ``cum_prem_init``
cum_prem_net_init()               float64  [point]          ``cum_prem_net_init``
class_factor()                    float64  [point]          *class_factor_table.csv*,
                                                            joined
surr_charge_rate_max()            float64  [point]          *surr_charge_table.csv*,
                                                            joined
surr_charge_runoff_years()        float64  [point]          *surr_charge_table.csv*,
                                                            joined
has_surr_charge_schedule()        int64    [point]          the same, 1 where the table
                                                            holds the id
coi_schedules()                   int      scalar           *coi_rates.csv*, checked
coi_schedule()                    int64    [point]          sex, class and issue age,
                                                            joined
coi_rate_last_years()             int64    [schedule]       *coi_rates.csv*
coi_rate_array()                  float64  [schedule, y]    *coi_rates.csv*
lapse_rate_array()                float64  [y]              *lapse_table.csv*
corridor_factor_array()           float64  [age]            *corridor_factors.csv*
mort_table_array()                float64  [age]            *mort_table.csv*
inforce_segment_count()           int64    [point]          *inforce_segments_sec.csv*
inforce_segment_last()            int64    [point]          *inforce_segments_sec.csv*
inforce_segment_max()             int      scalar           *inforce_segments_sec.csv*,
                                                            checked
seg_bal_pp_init()                 float64  [point, slot]    *inforce_segments_sec.csv*
seg_ded_cum_pp_init()             float64  [point, slot]    *inforce_segments_sec.csv*
seg_wd_cum_pp_init()              float64  [point, slot]    *inforce_segments_sec.csv*
seg_index_start_init()            float64  [point, slot]    *inforce_segments_sec.csv*
seg_index_cap_init()              float64  [point, slot]    *inforce_segments_sec.csv*
================================  =======  ===============  ==============================

The table checks are the ints they were: :func:`lapse_last_year`, the four age extents,
:func:`class_count` and :func:`surr_charge_count`. The COI table's check, which at stage
``E`` returned a Series of last policy years by cell, is the int :func:`coi_schedules`,
holding every message it held, and :func:`inforce_segment_count` and
:func:`inforce_segment_last`, which at stage ``E`` were Series by ``point_id``, are
vectors by position.

**An array is read by element, never whole,** in this Space as in
:mod:`~.IUL_US_SEC.Projection`. The compiler types an array cell as a memoryview only
once it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python
object. So an array derived here from another reads the table's column or the reader's
frame, and a width comes from a table or a check, never from another cell's array. Each
table's check is one cell that every array, extent and schedule number of the table reads
first, :func:`coi_schedules` for the COI scale and :func:`inforce_segment_max` for the
ladder, so that a projection, which reads an extent or a schedule number first, meets the
same refusal as a reader of the array. The column keywords of a ``DataFrame.assign`` are
passed as ``**{...}``, since a keyword named as a cell of this Space, ``age_at_entry``,
``point_id``, would be rewritten by the export.

**What cannot be decoded or joined is refused** when the array is first read, naming every
point at fault: a ``point_id`` that is not a whole number; a ``rate_class`` the class
factors lack; and on a point that ``has_surr_charge`` a ``surr_charge_id`` the schedules
lack, or one whose ``runoff_years`` is ``2**53`` or more. ``IUL_US_S`` fails every
projection of a point of the first two kinds, since it reads its class factor in its
first month in cover, and of the third its cash flows, which read the schedule in every
month of a point with a charge; here that refusal is the table's, so every point is
refused with it, as ``Term_US_SEC``'s refusals at the first read are. A point without a
charge is never refused a projection for its schedule, whatever its id, as ``IUL_US_S``
never reads it: its schedule is read where the table holds its id, as at stage ``E``,
and where it does not, ``Projection.surr_charge_rate_max`` raises stage ``E``'s
``ValueError``. A ``sex``, ``rate_class`` and ``age_at_entry`` the COI scale lacks is
schedule 0, and ``Projection.coi_rate_last_year`` refuses it where a rate is read, which
a point valued at or past ``charges_cease_age`` never does. A value of ``db_option``,
``qual_test``, ``premium_type`` or ``premium_mode`` none of the flags names is no flag,
and the cell that branches on it raises ``IUL_US_S``'s message, as in ``IUL_US_S``. Every
decode and join compares the text exactly, as ``IUL_US_S`` does, so ``"level"`` or
``"GPT "`` is not ``"LEVEL"`` or ``"GPT"``. A read beyond a table's extent is refused
where ``IUL_US_S``'s lookup raised ``KeyError``, by the one
:mod:`~.IUL_US_SEC.Projection` cell that reads the table, naming the point: a policy year
below 1 in ``lapse_rate_base_py`` and ``coi_rate_guar_py``, and a slot the point does not
hold in the five ladder readers. An age outside the corridor or mortality table reads
the nearest row, as in ``IUL_US_S``, so no padding is read.

A table is held from age or year 0 to its last key, so a key far past any a policy
reaches, an age of 10**9 say, makes an array of that many elements, where ``IUL_US_S``
reads the row without one. No rule bounds the keys from above: a table's last key is its
own, and each shipped table ends at an age or a year the projection reaches. The ladder
is as wide as the most segments one point holds, not as its largest slot, so a row in a
far slot refuses only its own point (:func:`inforce_segment_max`).

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is first refused unless it is
below ``2**53`` in size, where the int64 holds ``IUL_US_S``'s reading of it: the issue
age, ``duration_mth`` and the first years of the withdrawal and the loan
(:func:`model_point_table`'s rules 4, 6 and 7) and the ``point_id`` (:func:`point_id`).
modelx and the compiled model refuse alike, before any cast. The run-off of a charged
point's schedule, which ``Projection.lapse_shock_year`` takes the ``int()`` of, is held
below ``2**53`` years by the join. Every other number is read into a float64, as
``IUL_US_S`` reads it.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_dir():
    """The directory holding the input CSVs: the model folder's parent.

    Inputs are *external* files, not data stored inside the model, so the model
    folder is pure formulas.  The path is resolved at run time from where the model
    was read, following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table_sec.csv* and checked.

    Indexed by ``point_id``.  Ten columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``; and eight columns of the opening state, per policy, as the
    policy stands at the start of month 0, before any month-0 event:

    * ``av_pp_init`` and ``loan_bal_init``: the account value and the loan entering month
      0, ``IUL_US_S``'s own columns;
    * ``fa_pp_init`` and ``lca_pp_init``: the fixed (holding) account and the loan
      collateral account entering month 0, which ``IUL_US_S`` takes as the account value
      less the loan and as the loan;
    * ``sum_assured_init``: the face in force entering month 0, after every Option A
      withdrawal cut to date;
    * ``cum_prem_init`` and ``cum_prem_net_init``: the premiums less withdrawals paid to
      date, and the same less loans, the no-lapse guarantee's accumulator, each of which
      ``IUL_US_S`` opens at 0;
    * ``is_mec_init``: 1 where the 7-pay test failed before the valuation date, 0
      otherwise, an int code.

    The live index segments are the companion :func:`inforce_segments`.  The rest are
    ``IUL_US_S``'s, except ``row_kind``, ``source_policy_id`` and ``source_mth``, which
    record where the generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, by 20 rules in turn, and the first that
    fails raises ``ValueError``, naming the missing column or every point it fails on:

    1. the in-force columns are present, and so are the columns of ``IUL_US_S``'s own
       that the projection reads as a number or a flag: ``age_at_entry``,
       ``wd_first_year``, ``loan_first_year``, ``sum_assured``, ``premium_pp_ann``,
       ``wd_pp``, ``loan_new_pp_ann``, ``mnlp_rate``, ``gsp``, ``glp``,
       ``seven_pay_prem``, ``load_prem_rate``, ``index_alloc_rate`` and the flag
       ``has_surr_charge``;
    2. no ``point_id`` appears twice;
    3. ``policy_count`` is a number, zero or more;
    4. ``duration_mth`` is a whole number of months: positive for a policy in force, 0
       for one issued at the valuation date, negative for one issued later; and below
       ``2**53`` months in size, where its int64 vector holds it (the Space docstring);
    5. no policy is issued more than ``future_horizon_mth`` months after the valuation
       date, so ``duration_mth`` is ``-future_horizon_mth`` or more.  At 0 the model takes
       no future new business, and the message says so; a negative horizon is itself
       refused;
    6. ``age_at_entry`` is a whole number of years, 0 or more: the projection counts its
       frame and every attained age on it.  And it is below ``2**53`` in size, where its
       int64 vector holds it.  A fraction is refused, as at stage ``E``; an age the
       contract does not issue is ``Projection.proj_len``'s to refuse;
    7. each of ``wd_first_year`` and ``loan_first_year`` is a whole number of policy
       years, 1 or more: ``IUL_US_S`` takes the ``int()`` of each and compares the policy
       year with it, so a fraction would move the first year without a word.  And each
       is below ``2**53`` years, where its int64 vector holds it;
    8. ``sum_assured`` is a number above 0, the face at issue, which every policy holds:
       it reaches the death benefit's ``max``, the per-unit charge and the surrender
       charge, and a blank one would reach them as a missing value;
    9. each of ``premium_pp_ann``, ``wd_pp``, ``loan_new_pp_ann``, ``mnlp_rate``, ``gsp``,
       ``glp`` and ``seven_pay_prem`` is a number, zero or more: ``gsp`` and ``glp`` are
       read by the guideline limit's ``max`` and the single premium's ``min``, which a
       blank one would be lost in;
    10. ``load_prem_rate`` and ``index_alloc_rate``, the share of each premium the load
        takes and the share of the fixed account each month's sweep moves into a segment,
        are numbers from 0 to 1;
    11. ``has_surr_charge`` is ``True`` or ``False``, as pandas reads those words in any
        case.  A blank, a number or any other text is refused: one text value turns the
        whole column into text, where ``"False"`` is a true string, so every point would
        read as carrying a surrender charge;
    12. each of ``av_pp_init`` and ``fa_pp_init`` is a number, of either sign.
        ``IUL_US_S`` lapses no policy for insufficiency and charges an exhausted policy on,
        its fixed account carrying every deduction and draw the segments cannot, so the
        fixed account and then the account value run below zero, as its point 5's do,
        from policy months 383 and 604; a model restating ``IUL_US_S`` restates those
        states, and :func:`inforce_segments` holds the two together;
    13. each of ``lca_pp_init``, ``loan_bal_init`` and ``sum_assured_init`` is a number,
        zero or more.  The face in force may be 0: withdrawals under Option A can cut it
        to nothing while the policy stays in force, as ``IUL_US_S`` carries it;
    14. each of ``cum_prem_init`` and ``cum_prem_net_init`` is a number, of either sign:
        each is a tax or guarantee measure, not a balance, and withdrawals and loans can
        exceed the premiums paid;
    15. ``is_mec_init`` is 0 or 1, an int code, read by value, so that 1.0 is 1;
    16. a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: each
        of the eight columns is 0, and the issue values come from the formulas;
    17. ``sum_assured_init`` is at most ``sum_assured``, the face at issue, on a policy in
        force, since face increases are not modelled.  A face below it is accepted,
        whether a withdrawal cut it or an elective decrease the model does not implement,
        and is projected from the value given;
    18. ``lca_pp_init`` is above 0 exactly where ``loan_bal_init`` is: a standard loan
        moves value into the collateral account on the day it is taken, and the model
        takes no repayment, so the two are held together from the loan's first day, each
        at its own rate;
    19. ``cum_prem_net_init`` is at most ``cum_prem_init``, to a cent and a half -- half a
        cent for each of the two and half a cent more -- since loans only lower it;
    20. ``is_mec_init`` is 1 where the 7-pay test has already failed in the month before
        the valuation date: ``cum_prem_init`` above ``seven_pay_prem`` times the policy
        years to date, inside the first seven.

    The text columns ``sex``, ``rate_class``, ``db_option``, ``qual_test``,
    ``premium_type``, ``premium_mode`` and ``surr_charge_id`` are keys and labels, which
    the projection decodes or joins on at their first read, naming the point where none
    fits.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("av_pp_init", "loan_bal_init", "fa_pp_init", "lca_pp_init",
             "sum_assured_init", "cum_prem_init", "cum_prem_net_init", "is_mec_init")
    years = ("wd_first_year", "loan_first_year")
    amounts = ("premium_pp_ann", "wd_pp", "loan_new_pp_ann", "mnlp_rate", "gsp", "glp",
               "seven_pay_prem")
    shares = ("load_prem_rate", "index_alloc_rate")
    for column in ("policy_count", "duration_mth", "age_at_entry", *years, "sum_assured",
                   *amounts, *shares, "has_surr_charge", *state):
        if column not in table.columns:
            raise ValueError(f"{name} has no {column} column")
    repeated = table.index[table.index.duplicated()].unique().tolist()
    if repeated:
        raise ValueError(f"{name}: point_id {repeated} appears more than once")
    count = pd.to_numeric(table["policy_count"], errors="coerce")    # noqa: F821
    bad = table.index[~((count >= 0) & (count < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: policy_count must be a number, zero or more; it is "
                         f"not at point_id {bad}")
    months = pd.to_numeric(table["duration_mth"], errors="coerce")   # noqa: F821
    bad = table.index[~(months % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{name}: duration_mth must be a whole number of months; it "
                         f"is not at point_id {bad}")
    bad = table.index[~(months.abs() < 2.0 ** 53)].tolist()
    if bad:
        raise ValueError(f"{name}: duration_mth must be below 2**53 months in size; it "
                         f"is not at point_id {bad}")
    horizon = future_horizon_mth                                     # noqa: F821
    if horizon < 0:
        raise ValueError(f"future_horizon_mth must be 0 months or more, not {horizon}")
    bad = table.index[months < -horizon].tolist()
    if bad and horizon == 0:
        raise ValueError(f"{name}: duration_mth must be 0 or more: this model takes no "
                         f"future new business; it is not at point_id {bad}")
    if bad:
        raise ValueError(f"{name}: duration_mth must be -{horizon} or more, a policy "
                         f"issued at most {horizon} months after the valuation date; it "
                         f"is not at point_id {bad}")
    ages = pd.to_numeric(table["age_at_entry"], errors="coerce")     # noqa: F821
    bad = table.index[~((ages % 1 == 0) & (ages >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: age_at_entry must be a whole number of years, 0 or "
                         f"more; it is not at point_id {bad}")
    bad = table.index[~(ages < 2.0 ** 53)].tolist()
    if bad:
        raise ValueError(f"{name}: age_at_entry must be below 2**53 in size; it is not "
                         f"at point_id {bad}")
    for column in years:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v % 1 == 0) & (v >= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number of policy years, "
                             f"1 or more; it is not at point_id {bad}")
        bad = table.index[~(v < 2.0 ** 53)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be below 2**53 policy years; it is "
                             f"not at point_id {bad}")
    face = pd.to_numeric(table["sum_assured"], errors="coerce")      # noqa: F821
    bad = table.index[~((face > 0) & (face < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured must be a number above 0, the face at "
                         f"issue, which every policy holds; it is not at point_id {bad}")
    for column in amounts:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column in shares:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v >= 0) & (v <= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number from 0 to 1; it is not "
                             f"at point_id {bad}")
    flags = table["has_surr_charge"].astype(str).str.lower()
    bad = table.index[~flags.isin(["true", "false"])].tolist()
    if bad:
        raise ValueError(f"{name}: has_surr_charge must be True or False; it is not at "
                         f"point_id {bad}")
    values = {}
    for column in state:
        values[column] = pd.to_numeric(table[column], errors="coerce")  # noqa: F821
    for column in ("av_pp_init", "fa_pp_init"):
        v = values[column]
        bad = table.index[~(v.abs() < float("inf"))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not at point_id "
                             f"{bad}")
    for column in ("lca_pp_init", "loan_bal_init", "sum_assured_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column in ("cum_prem_init", "cum_prem_net_init"):
        v = values[column]
        bad = table.index[~(v.abs() < float("inf"))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not at point_id "
                             f"{bad}")
    bad = table.index[~values["is_mec_init"].isin([0, 1])].tolist()
    if bad:
        raise ValueError(f"{name}: is_mec_init must be 0 or 1, an int code; it is not "
                         f"at point_id {bad}")
    for column in state:
        bad = table.index[(months <= 0) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    bad = table.index[(months > 0) & ~(values["sum_assured_init"] <= face)].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured_init must be at most sum_assured, the "
                         f"face at issue, since face increases are not modelled; it is "
                         f"not at point_id {bad}")
    lent = values["loan_bal_init"] > 0
    bad = table.index[(values["lca_pp_init"] > 0) != lent].tolist()
    if bad:
        raise ValueError(f"{name}: lca_pp_init must be above 0 where loan_bal_init is, "
                         f"and 0 where it is 0: the collateral account holds a loan's "
                         f"collateral while the loan is outstanding; it is not at "
                         f"point_id {bad}")
    over = values["cum_prem_net_init"] > values["cum_prem_init"] + 0.015
    bad = table.index[over].tolist()
    if bad:
        raise ValueError(f"{name}: cum_prem_net_init must be at most cum_prem_init, to a "
                         f"cent and a half, since loans only lower it; it is not at "
                         f"point_id {bad}")
    year = (months - 1) // 12 + 1
    limit = (pd.to_numeric(table["seven_pay_prem"], errors="coerce")  # noqa: F821
             * year.where(year <= 7, 7))
    failed = (months > 0) & (year <= 7) & (values["cum_prem_init"] > limit)
    bad = table.index[failed & (values["is_mec_init"] != 1)].tolist()
    if bad:
        raise ValueError(f"{name}: is_mec_init must be 1 where the 7-pay test has "
                         f"already failed, cum_prem_init above seven_pay_prem times the "
                         f"policy years to date, in the first seven; it is not at "
                         f"point_id {bad}")
    return table


def inforce_segments():
    """The live index segments of each point in force, from *inforce_segments_sec.csv*.

    Indexed by ``point_id`` and ``slot``, both read by value as ints.  One row per live
    segment of a point in force at the valuation date, as it stands entering month 0:
    ``slot`` is the months since the segment's creation at the valuation date, 1 to 12,
    so the segment in slot ``k`` was born in policy month ``duration_mth - k``, and the
    one in slot 12 matures at ``t = 0``.  Its columns, per policy:

    * ``seg_bal_pp_init``: the segment's balance;
    * ``seg_ded_cum_pp_init`` and ``seg_wd_cum_pp_init``: the monthly deductions, and the
      withdrawals and loan transfers, charged to it since its creation, which with the
      balance are its credit base;
    * ``seg_index_start_init``: the index level at its creation, on the valuation-clock
      path, whose level at the valuation date is ``Projection.index_level_init``;
    * ``seg_index_cap_init``: the cap declared at its creation.

    ``point_id`` is the only key to a point, and nothing else in the file names one.  A
    point not yet in force holds no row; a point in force holds one for each of its last
    ``min(12, duration_mth)`` months, a month that swept nothing included, which
    ``Projection.proj_len`` checks, since the twelve is ``Projection.seg_term_mth``.

    The checks run over the whole file at once, by 9 rules in turn, and the first that
    fails raises ``ValueError``, naming the missing column or the lines, the header line
    1, or the points it fails on:

    1. the seven columns are present;
    2. each of ``point_id`` and ``slot`` is a whole number, below ``2**53`` in size,
       which numpy would otherwise cast to the least int64 without a word;
    3. each ``point_id`` is a point of :func:`model_point_table`;
    4. no ``point_id`` and ``slot`` appear together twice;
    5. ``slot`` is from 1 to its point's ``duration_mth``: no segment predates issue, and a
       point not yet in force holds none;
    6. each of ``seg_bal_pp_init``, ``seg_ded_cum_pp_init`` and ``seg_wd_cum_pp_init`` is
       a number, ``-1e-8`` or more: a balance a draw or a deduction took to exactly
       nothing can close on a rounding about zero of either sign, which an extract carried
       to the cent writes as 0, and ``Projection.check_seg_ladder`` holds every live
       balance to the same ``-1e-8``, ``IUL_US_S``'s tolerance;
    7. ``seg_index_start_init`` is a number above 0, the level the segment's return
       divides by;
    8. ``seg_index_cap_init`` is a number, zero or more: the credited rate's ``min``
       reads the cap first, so a blank cap would credit the floor without a word;
    9. each point's ``av_pp_init`` is its ``fa_pp_init`` plus its ``lca_pp_init`` plus the
       balances of its segments here, to half a cent an amount and half a cent more: the
       identity ``Projection.check_av_components`` holds every month, the opening state
       being the close of the month before.  The projection opens the account value from
       the parts, so the column is held to them, not read.
    """
    name = inforce_segments_file                                     # noqa: F821
    points = model_point_file                                        # noqa: F821
    table = pd.read_csv(input_dir() / name)                          # noqa: F821
    values = ("seg_bal_pp_init", "seg_ded_cum_pp_init", "seg_wd_cum_pp_init",
              "seg_index_start_init", "seg_index_cap_init")
    for column in ("point_id", "slot", *values):
        if column not in table.columns:
            raise ValueError(f"{name} has no {column} column")
    keys = {}
    for column in ("point_id", "slot"):
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = (table.index[~(v % 1 == 0)] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on "
                             f"line {bad}")
        bad = (table.index[~(v.abs() < 2.0 ** 53)] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be below 2**53 in size; it is not "
                             f"on line {bad}")
        keys[column] = v.astype("int64")
    model_points = model_point_table()
    known = keys["point_id"].isin(model_points.index)
    bad = (table.index[~known] + 2).tolist()
    if bad:
        ids = sorted(set(keys["point_id"][~known]))
        raise ValueError(f"{name}: point_id {ids} on line {bad} is no point of {points}")
    pairs = pd.MultiIndex.from_arrays([keys["point_id"], keys["slot"]])  # noqa: F821
    faults = []
    for p, k in sorted(set(pairs[pairs.duplicated()])):
        lines = (table.index[(keys["point_id"] == p) & (keys["slot"] == k)] + 2).tolist()
        faults.append(f"point_id {p} slot {k} is on line {lines}")
    if faults:
        raise ValueError(f"{name}: each point_id and slot must have one row; "
                         + "; ".join(faults))
    months = pd.to_numeric(model_points["duration_mth"], errors="coerce")  # noqa: F821
    life = months.reindex(keys["point_id"].to_numpy()).to_numpy()
    bad = (table.index[~((keys["slot"] >= 1) & (keys["slot"] <= life))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: slot must be from 1 to its point's duration_mth, the "
                         f"months since the segment's creation at the valuation date; it "
                         f"is not on line {bad}")
    numbers = {}
    for column in values:
        numbers[column] = pd.to_numeric(table[column], errors="coerce")  # noqa: F821
    for column in values[:3]:
        v = numbers[column]
        bad = (table.index[~((v >= -1e-8) & (v < float("inf")))] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, -1e-8 or more, zero "
                             f"to IUL_US_S's tolerance; it is not on line {bad}")
    v = numbers["seg_index_start_init"]
    bad = (table.index[~((v > 0) & (v < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: seg_index_start_init must be a number above 0, the "
                         f"level the segment's return divides by; it is not on line {bad}")
    v = numbers["seg_index_cap_init"]
    bad = (table.index[~((v >= 0) & (v < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: seg_index_cap_init must be a number, zero or more; it "
                         f"is not on line {bad}")
    held = pd.Series(numbers["seg_bal_pp_init"].to_numpy(),          # noqa: F821
                     index=keys["point_id"].to_numpy())
    segments = held.groupby(level=0).sum().reindex(model_points.index, fill_value=0.0)
    count = held.groupby(level=0).size().reindex(model_points.index, fill_value=0)
    av = pd.to_numeric(model_points["av_pp_init"], errors="coerce")  # noqa: F821
    parts = (pd.to_numeric(model_points["fa_pp_init"], errors="coerce")  # noqa: F821
             + pd.to_numeric(model_points["lca_pp_init"], errors="coerce")  # noqa: F821
             + segments)
    slack = 0.005 * (count + 3) + 0.005
    bad = model_points.index[~((av - parts).abs() <= slack)].tolist()
    if bad:
        raise ValueError(f"{points}: av_pp_init must be fa_pp_init plus lca_pp_init plus "
                         f"the point's segments in {name}, to half a cent an amount and "
                         f"half a cent more; it is not at point_id {bad}")
    out = table.assign(**{"point_id": keys["point_id"], "slot": keys["slot"]})
    return out.set_index(["point_id", "slot"]).sort_index()


def inforce_segment_count():
    """The number of live segments *inforce_segments_sec.csv* holds for each point: int64
    [point].

    Element ``i`` is the count of the table's point at position ``i``, 0 where the file
    holds none, read from :func:`inforce_segments`, which checks the file first.
    ``Projection.proj_len`` holds it, with :func:`inforce_segment_last`, to the segments
    a policy in force holds: one for each of its last ``min(seg_term_mth, duration_mth)``
    months.  At stage ``E`` it was a Series by ``point_id``; it is a vector here, read at
    the point's position, as every vector is.
    """
    held = inforce_segments().groupby(level="point_id").size()
    held = held.reindex(model_point_table().index, fill_value=0)
    return held.to_numpy(dtype="int64")


def inforce_segment_last():
    """The last slot *inforce_segments_sec.csv* holds for each point: int64 [point].

    Element ``i`` is the last slot of the table's point at position ``i``, 0 where the
    file holds no segment, read from :func:`inforce_segments`, which checks the file first
    and refuses a slot below 1 or held twice.  So a point whose last slot equals its count
    holds slots 1 to that count, one each, which is what ``Projection.proj_len`` asks.
    """
    tbl = inforce_segments().reset_index()
    last = tbl.groupby("point_id")["slot"].max()
    last = last.reindex(model_point_table().index, fill_value=0)
    return last.to_numpy(dtype="int64")


def inforce_segment_max():
    """The most segments any one point holds in *inforce_segments_sec.csv*, 0 if none.

    Read from :func:`inforce_segments`, which checks the file first: the ladder's check,
    an int, which each ladder array asks bare, and one less than their width, so that a
    slot is its own column.  It counts rows, not slots: a point ``Projection.proj_len``
    projects holds slots 1 to its count, so its every slot is a column, and a row in a
    slot past the widest count belongs to a point holding a gap, which ``proj_len``
    refuses before any of its slots is read.  So the width is bounded by the file's
    length, not by the largest slot a row may name: a slot of ``10**9`` on a point in
    force that long refuses that point, by name, where an array that wide would refuse
    every point, out of memory, at its first read.  12 on the shipped ladder,
    ``Projection.seg_term_mth``, which ``Data`` cannot read.
    """
    held = inforce_segments().groupby(level="point_id").size()
    return int(held.max()) if len(held) else 0


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*.

    The IRC 7702(d)(2) applicable percentages [R4]: 250% to attained age 40, grading to
    100% at 90-95.
    """
    return pd.read_csv(input_dir() / corridor_file, index_col="age")  # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / class_factor_file, index_col="rate_class")    # noqa: F821


def lapse_table():
    """The base annual lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")    # noqa: F821


def surr_charge_table():
    """The surrender charge schedules, read from *surr_charge_table.csv*.

    One row per ``surr_charge_id``, giving the initial charge per $1,000 of initial
    face and the number of years over which it runs off linearly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col="surr_charge_id")


def coi_schedules():
    """The number of issue-age cells *coi_rates.csv* gives a scale for, the table checked.

    One schedule a cell, each ``sex``, ``rate_class`` and ``age_at_entry`` the table
    holds: :func:`coi_rate_array` holds each schedule in a row, numbered from 1 in the
    order of those keys, :func:`coi_rate_last_years` each schedule's last policy year, and
    :func:`coi_schedule` gives each point its number.  The table's one check, which each
    of them asks first.  The two text keys may not be blank, and the two numeric keys,
    ``age_at_entry`` and ``policy_year``, are read by value, once: a key that is blank,
    text or not a whole number is refused, naming the file, the column and the lines it is
    on.  So is a cell whose policy years do not run from 1, one row a year, without a gap
    or a repeat: the message names the cell, each year that repeats or falls below 1, with
    its lines, and each year missing from 1 to the last.  And so is a ``coi_rate_guar``
    that is blank, text, infinite or below 0, naming its lines: a charge per $1,000 of net
    amount at risk, which may pass 1, as the current scale does from attained age 69, but
    is never a credit.  ``Projection.coi_rate_last_year`` takes a point's extent from
    :func:`coi_rate_last_years`, and refuses a point whose cell the table lacks, before
    ``Projection.coi_rate_guar_py`` reads its scale, so a projection meets the checks
    first.

    At stage ``E`` this check was :func:`coi_rate_last_years`, which returned the last
    years as a Series by cell; a check is an int here, the number of schedules, and the
    arrays ask it, so every message is the one it was.
    """
    name = coi_rates_file                                            # noqa: F821
    rates = coi_rates().reset_index()
    for column in ("sex", "rate_class"):
        bad = (rates.index[rates[column].isna()] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must not be blank; it is on line {bad}")
    for column in ("age_at_entry", "policy_year"):
        keys = pd.to_numeric(rates[column], errors="coerce")         # noqa: F821
        bad = (rates.index[~(keys % 1 == 0)] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on line "
                             f"{bad}")
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64"),  # noqa: F821
        "policy_year": pd.to_numeric(rates["policy_year"]).astype("int64")})   # noqa: F821
    years = rates.groupby(["sex", "rate_class", "age_at_entry"])["policy_year"]
    last = years.max()
    count = years.count()
    run = (years.min() == 1) & (last == count) & (years.nunique() == count)
    faults = []
    for cell in last.index[~run].tolist():
        held = years.get_group(cell)
        for key in sorted(set(held[held.duplicated() | (held < 1)])):
            faults.append(f"at {cell}, policy_year {key} is on line "
                          f"{(held.index[held == key] + 2).tolist()}")
        cell_run = [0] + sorted(set(held[held >= 1]))
        if len(cell_run) == 1:
            faults.append(f"at {cell}, no line holds policy_year 1")
        for a, b in zip(cell_run, cell_run[1:]):
            if b - a > 1:
                faults.append(f"at {cell}, no line holds policy_year {a + 1}"
                              + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the policy years of each sex, rate_class and "
                         f"age_at_entry must run from 1, one row a year, without a gap or "
                         f"a repeat; " + "; ".join(faults))
    values = pd.to_numeric(rates["coi_rate_guar"], errors="coerce")  # noqa: F821
    bad = (rates.index[~((values >= 0) & (values < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: coi_rate_guar must be a number, zero or more; it is not "
                         f"on line {bad}")
    return int(len(last))


def corridor_age_last():
    """The last attained age *corridor_factors.csv* gives a factor for, the table checked.

    The ``age`` column is read by value, once, so an age written ``40.0`` is 40.  A key
    that is blank, text or not a whole number is refused, naming the file, the column and
    the lines it is on.  So are ages that do not run one row an age, without a gap or a
    repeat: the message names each age that repeats, with its lines, and each age missing
    between the first and the last.  And so is a ``corridor_factor`` that is blank, text,
    infinite or below 0, naming its lines: a multiple of the account value, which the
    statute's applicable percentages hold to 100% or more.  And so is an age below 0,
    naming its lines, since :func:`corridor_factor_array` is held from age 0, so that the
    age is the index; ``IUL_US_S`` reads such a row, which no projection reaches.
    ``Projection.corridor_factor_at``, the table's one reader, takes both of its extents,
    this and :func:`corridor_age_first`, before it reads a factor.  A blank factor is a
    missing value to ``IUL_US_S``, whose death benefit, the ``max`` of the face and the
    corridor's amount, then reads it as no corridor at all.  A factor below 1 only makes
    the corridor bind later, or never; below 0 it would make the corridor's amount on an
    account value below 0 a positive one, which ``IUL_US_S``'s death benefit, with no floor
    on the account value, would pay: at -0.5 from attained age 95, its point 5 pays
    58,155,653.50 on a face of 92,200 at its month 800, every account check passing.
    """
    name = corridor_file                                             # noqa: F821
    table = corridor_factors()
    ages = pd.to_numeric(pd.Series(table.index), errors="coerce")    # noqa: F821
    bad = (ages.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    ages = ages.astype("int64")
    faults = []
    for key in sorted(set(ages[ages.duplicated()])):
        faults.append(f"age {key} is on line {(ages.index[ages == key] + 2).tolist()}")
    run = sorted(set(ages))
    if not run:
        faults.append("no line holds an age")
    for a, b in zip(run, run[1:]):
        if b - a > 1:
            faults.append(f"no line holds age {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the ages must run one row an age, without a gap or a "
                         f"repeat; " + "; ".join(faults))
    factors = pd.to_numeric(pd.Series(table["corridor_factor"].to_numpy()),  # noqa: F821
                            errors="coerce")
    bad = (factors.index[~((factors >= 0) & (factors < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: corridor_factor must be a number, zero or more; it is "
                         f"not on line {bad}")
    bad = (ages.index[ages < 0] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be 0 or more; it is not on line {bad}")
    return int(ages.max())


def corridor_age_first():
    """The first attained age *corridor_factors.csv* gives a factor for.

    Counted back from :func:`corridor_age_last`, which checks the table's keys first: the
    ages run one row an age, so the first is the last less the rows after it.
    """
    return corridor_age_last() - len(corridor_factors()) + 1


def mort_age_last():
    """The last attained age *mort_table.csv* gives a rate for, the table checked.

    Read and checked as :func:`corridor_age_last` reads and checks its own table, the rate
    checked being ``mort_rate``, which must also be from 0 to 1, as a probability, and an
    age below 0 refused, as there; the shipped table reaches 1.0 at attained age 119.
    ``Projection.mort_rate_base_at``, the table's one reader, takes both of its extents,
    this and :func:`mort_age_first`, before it reads a rate.  A blank rate is a missing
    value to ``IUL_US_S``, whose mortality is then not a number, and to
    ``Projection.mort_rate``, whose cap, ``min(q, 1.0)``, keeps it missing; a negative one
    would project negative deaths.
    """
    name = mort_table_file                                           # noqa: F821
    table = mort_table()
    ages = pd.to_numeric(pd.Series(table.index), errors="coerce")    # noqa: F821
    bad = (ages.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    ages = ages.astype("int64")
    faults = []
    for key in sorted(set(ages[ages.duplicated()])):
        faults.append(f"age {key} is on line {(ages.index[ages == key] + 2).tolist()}")
    run = sorted(set(ages))
    if not run:
        faults.append("no line holds an age")
    for a, b in zip(run, run[1:]):
        if b - a > 1:
            faults.append(f"no line holds age {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the ages must run one row an age, without a gap or a "
                         f"repeat; " + "; ".join(faults))
    rates = pd.to_numeric(pd.Series(table["mort_rate"].to_numpy()),  # noqa: F821
                          errors="coerce")
    bad = (rates.index[~((rates >= 0) & (rates <= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a number from 0 to 1; it is not on "
                         f"line {bad}")
    bad = (ages.index[ages < 0] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be 0 or more; it is not on line {bad}")
    return int(ages.max())


def mort_age_first():
    """The first attained age *mort_table.csv* gives a rate for.

    Counted back from :func:`mort_age_last`, which checks the table's keys first, as
    :func:`corridor_age_first` counts its own.
    """
    return mort_age_last() - len(mort_table()) + 1


def lapse_last_year():
    """The last policy year *lapse_table.csv* gives a rate for, the table checked.

    The ``policy_year`` column is read by value, once, as the lookup matches it, so a year
    written ``5.0`` is year 5.  A key that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on.  So are policy years that
    do not run from 1, one row a year, without a gap or a repeat: the message names each
    year that repeats or falls below 1, with its lines, and each year missing from 1 to the
    last.  And so is a ``lapse_rate_ann`` that is blank, text or outside 0 to 1, naming its
    lines: a probability, which below 0 would grow the count by its lapses, and past 1
    would leave ``Projection.lapse_rate_mth``'s ``1 - (1 - q)^(1/12)`` no real value.
    ``Projection.lapse_rate_base_py``, the table's one reader, takes its extent from here
    before it reads a rate.  A blank rate is a missing value to ``IUL_US_S``, which its
    lapse cap, ``min(lapse_rate_cap, rate)``, a bound written first, then reads as the
    cap.
    """
    name = lapse_table_file                                          # noqa: F821
    table = lapse_table()
    years = pd.to_numeric(pd.Series(table.index), errors="coerce")   # noqa: F821
    bad = (years.index[~(years % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: policy_year must be a whole number; it is not on line "
                         f"{bad}")
    years = years.astype("int64")
    faults = []
    for key in sorted(set(years[years.duplicated() | (years < 1)])):
        faults.append(f"policy_year {key} is on line "
                      f"{(years.index[years == key] + 2).tolist()}")
    run = [0] + sorted(set(years[years >= 1]))
    if len(run) == 1:
        faults.append("no line holds policy_year 1")
    for a, b in zip(run, run[1:]):
        if b - a > 1:
            faults.append(f"no line holds policy_year {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the policy years must run from 1, one row a year, "
                         f"without a gap or a repeat; " + "; ".join(faults))
    rates = pd.to_numeric(pd.Series(table["lapse_rate_ann"].to_numpy()),  # noqa: F821
                          errors="coerce")
    bad = (rates.index[~((rates >= 0) & (rates <= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: lapse_rate_ann must be a number from 0 to 1; it is not "
                         f"on line {bad}")
    return int(years.max())


def class_count():
    """The number of classes *class_factor_table.csv* gives a factor for, the table checked.

    A ``rate_class`` that is blank is refused, naming the file and the lines it is on, and
    so is one on more than one row, naming each such class with its lines; and so is a
    ``factor`` that is blank, text, infinite or below 0, naming its lines: a multiple of the
    base mortality, which below 0 would project negative deaths.
    ``Projection.class_factor``, the table's one reader, asks for the count before it reads
    a factor, so a projection meets the checks first.  A blank factor is a missing value to
    ``IUL_US_S``, whose mortality is then not a number, and to ``Projection.mort_rate``,
    whose cap, ``min(q, 1.0)``, keeps it missing.
    """
    name = class_factor_file                                         # noqa: F821
    table = class_factor_table()
    classes = pd.Series(table.index)                                 # noqa: F821
    bad = (classes.index[classes.isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: rate_class must not be blank; it is on line {bad}")
    faults = []
    for label in sorted(set(classes[classes.duplicated()])):
        faults.append(f"rate_class {label} is on line "
                      f"{(classes.index[classes == label] + 2).tolist()}")
    if faults:
        raise ValueError(f"{name}: each rate_class must have one row; "
                         + "; ".join(faults))
    factors = pd.to_numeric(pd.Series(table["factor"].to_numpy()),   # noqa: F821
                            errors="coerce")
    bad = (factors.index[~((factors >= 0) & (factors < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: factor must be a number, zero or more; it is not on "
                         f"line {bad}")
    return len(table)


def surr_charge_count():
    """The number of schedules *surr_charge_table.csv* gives, the table checked.

    A ``surr_charge_id`` that is blank is refused, naming the file and the lines it is on,
    and so is one on more than one row, naming each such schedule with its lines.  So is a
    ``sc_per_1000_init`` that is blank, text, infinite or below 0, naming its lines, and a
    ``runoff_years`` that is not a whole number of years, 1 or more -- blank, text,
    infinite, a fraction or below 1 alike -- naming its lines: the projection divides the
    charge by the run-off and counts policy years on it, where ``IUL_US_S`` divides by the
    float, takes the ``int()`` of a fraction for its lapse spike, and divides by zero at 0.
    ``Projection.surr_charge_rate_max`` and ``Projection.surr_charge_runoff_years``, the
    table's two readers, ask for the count before they read a value, so a projection meets
    the checks first.  A blank charge is a missing value to ``IUL_US_S``, whose surrender
    charge rate, the ``max`` of 0 and the charge left, then reads it as no charge at all.
    A charge below 0 leaves a charge below 0 through the schedule's years, which the
    ``max`` reads as none, and after them, where the share of the run-off left turns
    negative, a charge above 0 that rises each month, every check passing.
    """
    name = surr_charge_file                                          # noqa: F821
    table = surr_charge_table()
    ids = pd.Series(table.index)                                     # noqa: F821
    bad = (ids.index[ids.isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: surr_charge_id must not be blank; it is on line {bad}")
    faults = []
    for label in sorted(set(ids[ids.duplicated()])):
        faults.append(f"surr_charge_id {label} is on line "
                      f"{(ids.index[ids == label] + 2).tolist()}")
    if faults:
        raise ValueError(f"{name}: each surr_charge_id must have one row; "
                         + "; ".join(faults))
    values = pd.to_numeric(pd.Series(table["sc_per_1000_init"].to_numpy()),  # noqa: F821
                           errors="coerce")
    bad = (values.index[~((values >= 0) & (values < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: sc_per_1000_init must be a number, zero or more; it is "
                         f"not on line {bad}")
    years = pd.to_numeric(pd.Series(table["runoff_years"].to_numpy()),  # noqa: F821
                          errors="coerce")
    bad = (years.index[~((years % 1 == 0) & (years >= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: runoff_years must be a whole number of years, 1 or "
                         f"more; it is not on line {bad}")
    return len(table)


def coi_schedule():
    """The number of each model point's guaranteed COI scale, in table order: int64
    [point].

    The point's row of :func:`coi_rate_array`: the schedules of *coi_rates.csv*, one for
    each ``sex``, ``rate_class`` and ``age_at_entry`` it holds, numbered from 1 in the
    order of those keys, as :func:`coi_rate_array` numbers its rows, whatever the order of
    the file's lines.  The point's key is its ``sex``, its ``rate_class`` and its
    ``age_at_entry``, compared exactly, as ``IUL_US_S`` slices the scale.  A point whose
    key the table lacks gets schedule 0, a row of padding, and is not refused here:
    ``IUL_US_S`` projects such a point while it reads no COI rate, as one valued at or
    past ``charges_cease_age`` never does, and ``Projection.coi_rate_last_year`` refuses
    it, naming it, when one is read.  Asks :func:`coi_schedules` first, which checks the
    table.
    """
    coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64")})  # noqa: F821
    number = {}
    for key, _ in rates.groupby(["sex", "rate_class", "age_at_entry"]):
        number[key] = len(number) + 1
    table = model_point_table()
    sexes, classes = table["sex"].tolist(), table["rate_class"].tolist()
    ages = pd.to_numeric(table["age_at_entry"]).tolist()             # noqa: F821
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get((sexes[i], classes[i], int(ages[i])), 0)
    return out


def coi_rate_last_years():
    """The last policy year of each guaranteed COI scale: int64 [schedule].

    Element ``s`` is the last ``policy_year`` *coi_rates.csv* holds for schedule ``s``,
    numbered as :func:`coi_schedule` numbers it, read by value once :func:`coi_schedules`
    has checked the table: 76 on the shipped anchor cell.  0 at element 0, schedule 0,
    which ``Projection.coi_rate_last_year`` refuses where it is read.  At stage ``E`` this
    was the table's check, a Series by cell; the check is :func:`coi_schedules` here.
    """
    n = coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64"),  # noqa: F821
        "policy_year": pd.to_numeric(rates["policy_year"]).astype("int64")})   # noqa: F821
    out = np.zeros(n + 1, dtype="int64")                             # noqa: F821
    s = 0
    for _, rows in rates.groupby(["sex", "rate_class", "age_at_entry"]):
        s += 1
        out[s] = int(rows["policy_year"].max())
    return out


def coi_rate_array():
    """The guaranteed maximum monthly COI rates by schedule and policy year: float64
    [schedule, y].

    Row ``s`` is schedule ``s`` of *coi_rates.csv*, numbered from 1 in the order of its
    keys, ``sex``, ``rate_class`` and ``age_at_entry``, as :func:`coi_schedule` numbers
    it, and column ``y`` is policy year ``y``, so that the year is the index: one more
    column than the table's last policy year, one more row than its schedules.  Per
    $1,000 of net amount at risk.  NaN in row 0, schedule 0, which no point the table
    holds is given, in column 0, before any policy year, and past each schedule's last
    year, all padding, which ``Projection.coi_rate_guar_py`` never reads: it refuses a
    year below 1 and a point of schedule 0, and reads a later year at the schedule's
    last.  Asks :func:`coi_schedules` first, which checks the table.
    """
    n = coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64"),  # noqa: F821
        "policy_year": pd.to_numeric(rates["policy_year"]).astype("int64")})   # noqa: F821
    out = np.full((n + 1, int(rates["policy_year"].max()) + 1), np.nan)  # noqa: F821
    s = 0
    for _, rows in rates.groupby(["sex", "rate_class", "age_at_entry"]):
        s += 1
        years = rows["policy_year"].to_numpy(dtype="int64")
        out[s, years] = pd.to_numeric(                               # noqa: F821
            rows["coi_rate_guar"]).to_numpy(dtype="float64")
    return out


def lapse_rate_array():
    """The base annual lapse rates by policy year: float64 [y].

    Element ``y`` is the ``lapse_rate_ann`` of policy year ``y`` in *lapse_table.csv*, so
    that the year is the index, to the last year :func:`lapse_last_year` gives once it has
    checked the table.  NaN at 0, before the first year, which
    ``Projection.lapse_rate_base_py`` never reads: it refuses a year below 1.
    """
    last = lapse_last_year()
    table = lapse_table()
    years = pd.to_numeric(pd.Series(table.index)).to_numpy(dtype="int64")  # noqa: F821
    out = np.full(last + 1, np.nan)                                  # noqa: F821
    out[years] = pd.to_numeric(                                      # noqa: F821
        table["lapse_rate_ann"]).to_numpy(dtype="float64")
    return out


def corridor_factor_array():
    """The GPT corridor factors by attained age: float64 [age].

    Element ``a`` is the ``corridor_factor`` of age ``a`` in *corridor_factors.csv*, so
    that the age is the index, to the last age :func:`corridor_age_last` gives once it
    has checked the table, which refuses a negative age.  NaN from 0 to below the first
    age, which ``Projection.corridor_factor_at`` never reads: it reads an age outside the
    table at the nearest row, as ``IUL_US_S`` does.
    """
    last = corridor_age_last()
    table = corridor_factors()
    ages = pd.to_numeric(pd.Series(table.index)).to_numpy(dtype="int64")  # noqa: F821
    out = np.full(last + 1, np.nan)                                  # noqa: F821
    out[ages] = pd.to_numeric(                                       # noqa: F821
        table["corridor_factor"]).to_numpy(dtype="float64")
    return out


def mort_table_array():
    """The best-estimate annual mortality rates by attained age: float64 [age].

    Element ``a`` is the ``mort_rate`` of age ``a`` in *mort_table.csv*, held as
    :func:`corridor_factor_array` holds its own table, to the last age
    :func:`mort_age_last` gives.  NaN from 0 to below the first age, which
    ``Projection.mort_rate_base_at`` never reads.
    """
    last = mort_age_last()
    table = mort_table()
    ages = pd.to_numeric(pd.Series(table.index)).to_numpy(dtype="int64")  # noqa: F821
    out = np.full(last + 1, np.nan)                                  # noqa: F821
    out[ages] = pd.to_numeric(table["mort_rate"]).to_numpy(dtype="float64")  # noqa: F821
    return out


def point_id():
    """The ``point_id`` of every model point, in table order: int64 [point].

    ``Projection`` is indexed by position, ``idx``, so this is how a projection names its
    point: ``Projection.point_id()`` is the element at ``idx``, and every refusal quotes
    it.  A label that is not a whole number is refused, naming every such label, and so
    is one of ``2**53`` or more in size, which numpy would read as the least int64 once
    past int64.  pandas reads a column of whole labels as int64 exactly, so the bound
    refuses some labels the vector could hold, none of them a label a table needs.
    """
    table = model_point_table()
    labels = pd.to_numeric(pd.Series(table.index), errors="coerce")  # noqa: F821
    bad = table.index[~(labels % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: point_id must be a whole number; "
                         f"{bad} is not")                            # noqa: F821
    bad = table.index[~(labels.abs() < 2.0 ** 53).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: point_id must be below 2**53 in size; "
                         f"{bad} is not")                            # noqa: F821
    return labels.to_numpy(dtype="int64")


def age_at_entry():
    """The issue age (ANB) of every model point: int64 [point].

    The ``age_at_entry`` column, which :func:`model_point_table` holds to a whole number
    below ``2**53`` in size, 0 or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["age_at_entry"]).to_numpy(dtype="int64")


def duration_mth():
    """The completed policy months at the valuation date of every model point: int64
    [point].

    The ``duration_mth`` column, which :func:`model_point_table` holds to a whole number
    below ``2**53`` in size.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["duration_mth"]).to_numpy(dtype="int64")


def wd_first_year():
    """The first policy year of each model point's withdrawals: int64 [point].

    The ``wd_first_year`` column, which :func:`model_point_table` holds to a whole number
    of policy years, 1 or more, below ``2**53``.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["wd_first_year"]).to_numpy(dtype="int64")


def loan_first_year():
    """The first policy year of each model point's loans: int64 [point].

    The ``loan_first_year`` column, which :func:`model_point_table` holds to a whole number
    of policy years, 1 or more, below ``2**53``.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["loan_first_year"]).to_numpy(dtype="int64")


def is_mec_init():
    """Whether each model point is a MEC entering month 0: int64 [point].

    The ``is_mec_init`` column, which :func:`model_point_table` holds to 0 or 1, an int
    code, read by value, so that 1.0 is 1.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["is_mec_init"]).to_numpy(dtype="int64")


def has_surr_charge():
    """Whether a surrender charge schedule applies to each model point: int64 [point].

    1 where the ``has_surr_charge`` column reads True, in any case, and 0 where it reads
    False: :func:`model_point_table` refuses any other value.
    """
    flags = model_point_table()["has_surr_charge"].astype(str).str.lower()
    return (flags == "true").to_numpy(dtype="int64")


def is_db_option_a():
    """Whether the death benefit option is A, the level face, for each model point:
    int64 [point].

    1 where ``db_option`` is ``"A"``, compared element by element as ``IUL_US_S`` compares
    it, so that ``"a"`` or ``"A "`` is not, and 0 elsewhere.  A value no flag of its
    column names is not refused here: it is no flag, and the projection cell that
    branches on the column raises ``IUL_US_S``'s message on it, ``"invalid db_option"``.
    """
    return (model_point_table()["db_option"] == "A").to_numpy(dtype="int64")


def is_db_option_b():
    """Whether the death benefit option is B, the face plus the account value, for each
    model point: int64 [point].

    1 where ``db_option`` is ``"B"``, decoded as :func:`is_db_option_a` decodes A, and 0
    elsewhere; a value no flag names raises ``"invalid db_option"`` where a projection
    branches on it.
    """
    return (model_point_table()["db_option"] == "B").to_numpy(dtype="int64")


def is_gpt():
    """Whether the point elects the guideline premium test, for each model point:
    int64 [point].

    1 where ``qual_test`` is ``"GPT"``, decoded as :func:`is_db_option_a` decodes A, and 0
    elsewhere; a value no flag names raises ``"invalid qual_test"`` where a projection
    branches on it.
    """
    return (model_point_table()["qual_test"] == "GPT").to_numpy(dtype="int64")


def is_level_premium():
    """Whether the premium pattern is LEVEL, for each model point: int64 [point].

    1 where ``premium_type`` is ``"LEVEL"``, decoded as :func:`is_db_option_a` decodes A,
    and 0 elsewhere; a value no flag names raises ``"invalid premium type"`` where a
    projection branches on it.
    """
    return (model_point_table()["premium_type"] == "LEVEL").to_numpy(dtype="int64")


def is_single_premium():
    """Whether the premium pattern is SINGLE, for each model point: int64 [point].

    1 where ``premium_type`` is ``"SINGLE"``, decoded as :func:`is_db_option_a` decodes A,
    and 0 elsewhere; a value no flag names raises ``"invalid premium type"`` where a
    projection branches on it.
    """
    return (model_point_table()["premium_type"] == "SINGLE").to_numpy(dtype="int64")


def is_target_premium():
    """Whether the premium pattern is TARGET, for each model point: int64 [point].

    1 where ``premium_type`` is ``"TARGET"``, decoded as :func:`is_db_option_a` decodes A,
    and 0 elsewhere; a value no flag names raises ``"invalid premium type"`` where a
    projection branches on it.
    """
    return (model_point_table()["premium_type"] == "TARGET").to_numpy(dtype="int64")


def is_annual_premium():
    """Whether the premium mode is ANNUAL, for each model point: int64 [point].

    1 where ``premium_mode`` is ``"ANNUAL"``, decoded as :func:`is_db_option_a` decodes A,
    and 0 elsewhere; a value no flag names raises ``"invalid premium mode"`` where a
    projection branches on it.
    """
    return (model_point_table()["premium_mode"] == "ANNUAL").to_numpy(dtype="int64")


def is_monthly_premium():
    """Whether the premium mode is MONTHLY, for each model point: int64 [point].

    1 where ``premium_mode`` is ``"MONTHLY"``, decoded as :func:`is_db_option_a` decodes A,
    and 0 elsewhere; a value no flag names raises ``"invalid premium mode"`` where a
    projection branches on it.
    """
    return (model_point_table()["premium_mode"] == "MONTHLY").to_numpy(dtype="int64")


def sum_assured():
    """The face at issue of every model point: float64 [point].

    The ``sum_assured`` column, which :func:`model_point_table` holds to a number above 0.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["sum_assured"]).to_numpy(dtype="float64")


def policy_count():
    """The policies each model point stands for: float64 [point].

    The ``policy_count`` column, which :func:`model_point_table` holds to a number, zero or
    more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["policy_count"]).to_numpy(dtype="float64")


def premium_pp_ann():
    """The planned annual premium per policy of every model point: float64 [point].

    The ``premium_pp_ann`` column, which :func:`model_point_table` holds to a number, zero
    or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["premium_pp_ann"]).to_numpy(dtype="float64")


def wd_pp():
    """The planned monthly withdrawal per policy of every model point: float64 [point].

    The ``wd_pp`` column, which :func:`model_point_table` holds to a number, zero or
    more.  ``Projection.wd_pp_mth`` reads it, since ``Projection.wd_pp`` is the
    month's withdrawal.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["wd_pp"]).to_numpy(dtype="float64")


def loan_new_pp_ann():
    """The planned annual loan per policy of every model point: float64 [point].

    The ``loan_new_pp_ann`` column, which :func:`model_point_table` holds to a number, zero
    or more.  ``Projection.loan_new_pp_ann`` reads it.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["loan_new_pp_ann"]).to_numpy(dtype="float64")


def mnlp_rate():
    """The minimum no-lapse premium per $1,000 a year of every model point: float64 [point].

    The ``mnlp_rate`` column, which :func:`model_point_table` holds to a
    number, zero or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["mnlp_rate"]).to_numpy(dtype="float64")


def gsp():
    """The guideline single premium of every model point: float64 [point].

    The ``gsp`` column, which :func:`model_point_table` holds to a number, zero or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["gsp"]).to_numpy(dtype="float64")


def glp():
    """The guideline level premium of every model point: float64 [point].

    The ``glp`` column, which :func:`model_point_table` holds to a number, zero or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["glp"]).to_numpy(dtype="float64")


def seven_pay_prem():
    """The 7-pay premium of every model point: float64 [point].

    The ``seven_pay_prem`` column, which :func:`model_point_table` holds to a number, zero
    or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["seven_pay_prem"]).to_numpy(dtype="float64")


def load_prem_rate():
    """The current premium load of every model point: float64 [point].

    The ``load_prem_rate`` column, which :func:`model_point_table` holds to a number from 0
    to 1.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["load_prem_rate"]).to_numpy(dtype="float64")


def index_alloc_rate():
    """The indexed allocation share of every model point: float64 [point].

    The ``index_alloc_rate`` column, which :func:`model_point_table` holds to a number from
    0 to 1.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["index_alloc_rate"]).to_numpy(dtype="float64")


def av_pp_init():
    """The account value per policy entering month 0: float64 [point].

    The ``av_pp_init`` column, which :func:`model_point_table` holds to a number, of either
    sign.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["av_pp_init"]).to_numpy(dtype="float64")


def loan_bal_init():
    """The loan per policy entering month 0: float64 [point].

    The ``loan_bal_init`` column, which :func:`model_point_table` holds to a number, zero or
    more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["loan_bal_init"]).to_numpy(dtype="float64")


def fa_pp_init():
    """The fixed account per policy entering month 0: float64 [point].

    The ``fa_pp_init`` column, which :func:`model_point_table` holds to a number, of either
    sign.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["fa_pp_init"]).to_numpy(dtype="float64")


def lca_pp_init():
    """The loan collateral account per policy entering month 0: float64 [point].

    The ``lca_pp_init`` column, which :func:`model_point_table` holds to a number,
    zero or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["lca_pp_init"]).to_numpy(dtype="float64")


def sum_assured_init():
    """The face in force per policy entering month 0: float64 [point].

    The ``sum_assured_init`` column, which :func:`model_point_table` holds to a number, zero
    or more, at most ``sum_assured`` on a policy in force.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["sum_assured_init"]).to_numpy(dtype="float64")


def cum_prem_init():
    """The premiums less withdrawals paid per policy entering month 0: float64 [point].

    The ``cum_prem_init`` column, which :func:`model_point_table` holds to a
    number, of either sign.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["cum_prem_init"]).to_numpy(dtype="float64")


def cum_prem_net_init():
    """The premiums less withdrawals and loans per policy entering month 0: float64 [point].

    The ``cum_prem_net_init`` column, which :func:`model_point_table` holds to a number, of
    either sign.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["cum_prem_net_init"]).to_numpy(dtype="float64")


def class_factor():
    """The underwriting-class factor of each model point: float64 [point].

    The ``factor`` *class_factor_table.csv* gives the point's ``rate_class``, compared
    exactly, once :func:`class_count` has checked the table.  A point reads its class
    factor in its first month in cover, so ``IUL_US_S`` fails every projection of a point
    whose class the table lacks: such a point is refused here, at the first read, naming
    every such point, where stage ``E`` refused it, by name, at its own first read.
    """
    class_count()
    table = model_point_table()
    factors = pd.to_numeric(class_factor_table()["factor"])          # noqa: F821
    bad = table.index[~table["rate_class"].isin(factors.index)].tolist()
    if bad:
        raise ValueError(f"{class_factor_file} has no factor for the rate_class of "
                         f"point_id {bad}")                          # noqa: F821
    return table["rate_class"].map(factors).to_numpy(dtype="float64")


def surr_charge_rate_max():
    """The surrender charge per $1,000 of initial face of each model point, before any of
    it runs off: float64 [point].

    The ``sc_per_1000_init`` of the point's ``surr_charge_id`` in
    *surr_charge_table.csv*, once :func:`surr_charge_count` has checked the table, on
    every point whose id the table holds, with a charge or without, as stage ``E``'s
    accessor read it: a point without a charge reads its schedule, though no cell reads it
    there.  NaN where the table lacks the id, and :func:`has_surr_charge_schedule` 0
    there.  The join refuses the table, naming every such point, only on a point with a
    charge, since ``IUL_US_S`` reads the schedule in every month of such a point's cover:
    an id the table lacks, where ``IUL_US_S``'s ``.loc`` raised ``KeyError``; and a
    ``runoff_years`` of ``2**53`` years or more in size, the bound of every number read as
    an int, past which the compiled ``int()`` in ``Projection.lapse_shock_year`` would in
    time raise ``OverflowError``.  :func:`surr_charge_count` already refuses a run-off
    that is not a whole number of years, 1 or more, so the division by it never meets 0.
    A point without a charge whose id the table lacks projects, as in ``IUL_US_S``, and
    ``Projection.surr_charge_rate_max`` raises stage ``E``'s ``ValueError`` on it where it
    is read, which no projection does.  The same checks run in
    :func:`surr_charge_runoff_years`, the join's other vector, so that whichever a
    projection reads first refuses the point.
    """
    surr_charge_count()
    table = model_point_table()
    schedules = surr_charge_table()
    values = pd.to_numeric(schedules["sc_per_1000_init"])                       # noqa: F821
    years = pd.to_numeric(schedules["runoff_years"])                 # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing, huge = [], []
    for i in range(len(ids)):
        if ids[i] in values.index:
            out[i] = float(values[ids[i]])
            if flags[i] and not abs(years[ids[i]]) < 2.0 ** 53:
                huge.append(table.index[i])
        elif flags[i]:
            missing.append(table.index[i])
    if missing:
        raise ValueError(f"{surr_charge_file} has no schedule for the surr_charge_id of "
                         f"point_id {missing}, each of which has_surr_charge")  # noqa: F821
    if huge:
        raise ValueError(f"{surr_charge_file}: runoff_years must be below 2**53 years in "
                         f"size on the schedule of point_id {huge}, each of which "
                         f"has_surr_charge")                         # noqa: F821
    return out


def surr_charge_runoff_years():
    """The run-off, in policy years, of each model point's surrender charge: float64
    [point].

    The ``runoff_years`` of the point's ``surr_charge_id`` in *surr_charge_table.csv*, on
    every point whose id the table holds, NaN on a point without a charge whose id it
    lacks, joined and checked as :func:`surr_charge_rate_max` joins and checks the charge,
    with its refusals.  A float, as ``IUL_US_S`` reads it, whole by the table's check.
    """
    surr_charge_count()
    table = model_point_table()
    schedules = surr_charge_table()
    values = pd.to_numeric(schedules["runoff_years"])                       # noqa: F821
    years = pd.to_numeric(schedules["runoff_years"])                 # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing, huge = [], []
    for i in range(len(ids)):
        if ids[i] in values.index:
            out[i] = float(values[ids[i]])
            if flags[i] and not abs(years[ids[i]]) < 2.0 ** 53:
                huge.append(table.index[i])
        elif flags[i]:
            missing.append(table.index[i])
    if missing:
        raise ValueError(f"{surr_charge_file} has no schedule for the surr_charge_id of "
                         f"point_id {missing}, each of which has_surr_charge")  # noqa: F821
    if huge:
        raise ValueError(f"{surr_charge_file}: runoff_years must be below 2**53 years in "
                         f"size on the schedule of point_id {huge}, each of which "
                         f"has_surr_charge")                         # noqa: F821
    return out


def has_surr_charge_schedule():
    """Whether *surr_charge_table.csv* holds each model point's schedule: int64 [point].

    1 where the point's ``surr_charge_id`` is a ``surr_charge_id`` of the table, compared
    exactly, as ``IUL_US_S``'s ``.loc`` compares it, and 0 where it is not, blank
    included, once :func:`surr_charge_count` has checked the table.  0 only on a point
    without a charge, since :func:`surr_charge_rate_max` refuses the table where a point
    with a charge names an id it lacks: there ``Projection.surr_charge_rate_max`` and
    ``Projection.surr_charge_runoff_years`` raise stage ``E``'s ``ValueError``, naming
    the point.
    """
    surr_charge_count()
    known = surr_charge_table().index                                # noqa: F821
    ids = model_point_table()["surr_charge_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    for i in range(len(ids)):
        if ids[i] in known:
            out[i] = 1
    return out


def seg_bal_pp_init():
    """The balance of each live segment entering month 0, by point and slot:
    float64 [point, slot].

    Row ``i`` is the table's point at position ``i`` and column ``k`` its slot ``k`` of
    *inforce_segments_sec.csv*, the column ``seg_bal_pp_init``, per policy, so that the slot
    is the index: :func:`inforce_segment_max` plus one wide, 13 on the shipped ladder.  NaN
    in column 0, which is no slot, and wherever the point holds no row, padding that
    ``Projection.seg_bal_pp_init`` never reads: it asks ``Projection.proj_len`` first, which
    refuses a point whose slots are not 1 to its count, one each, and then refuses a slot
    below 1 or past the point's last.  A row in a slot past the width belongs to such a
    point and is left out.  The width is the file's, not ``Projection.seg_term_mth``, which
    ``Data`` cannot read, so a model run at another segment term reads a ladder written for
    it.  Asks :func:`inforce_segment_max` first, which checks the file.
    """
    n = inforce_segment_max()
    table = model_point_table()
    ladder = inforce_segments().reset_index()
    rows = table.index.get_indexer(ladder["point_id"])
    slots = ladder["slot"].to_numpy(dtype="int64")
    held = slots <= n
    out = np.full((len(table), n + 1), np.nan)                       # noqa: F821
    out[rows[held], slots[held]] = pd.to_numeric(                    # noqa: F821
        ladder["seg_bal_pp_init"]).to_numpy(dtype="float64")[held]
    return out


def seg_ded_cum_pp_init():
    """The deductions charged to each live segment since its creation, by point and slot:
    float64 [point, slot].

    The column ``seg_ded_cum_pp_init`` of *inforce_segments_sec.csv*, per policy, held as
    :func:`seg_bal_pp_init` holds the balance, and read only by
    ``Projection.seg_ded_cum_pp_init``, after its checks.
    """
    n = inforce_segment_max()
    table = model_point_table()
    ladder = inforce_segments().reset_index()
    rows = table.index.get_indexer(ladder["point_id"])
    slots = ladder["slot"].to_numpy(dtype="int64")
    held = slots <= n
    out = np.full((len(table), n + 1), np.nan)                       # noqa: F821
    out[rows[held], slots[held]] = pd.to_numeric(                    # noqa: F821
        ladder["seg_ded_cum_pp_init"]).to_numpy(dtype="float64")[held]
    return out


def seg_wd_cum_pp_init():
    """The draws out of each live segment since its creation, by point and slot:
    float64 [point, slot].

    The column ``seg_wd_cum_pp_init`` of *inforce_segments_sec.csv*, per policy, held as
    :func:`seg_bal_pp_init` holds the balance, and read only by
    ``Projection.seg_wd_cum_pp_init``, after its checks.
    """
    n = inforce_segment_max()
    table = model_point_table()
    ladder = inforce_segments().reset_index()
    rows = table.index.get_indexer(ladder["point_id"])
    slots = ladder["slot"].to_numpy(dtype="int64")
    held = slots <= n
    out = np.full((len(table), n + 1), np.nan)                       # noqa: F821
    out[rows[held], slots[held]] = pd.to_numeric(                    # noqa: F821
        ladder["seg_wd_cum_pp_init"]).to_numpy(dtype="float64")[held]
    return out


def seg_index_start_init():
    """The index level at each live segment's creation, by point and slot:
    float64 [point, slot].

    The column ``seg_index_start_init`` of *inforce_segments_sec.csv*, per policy, held as
    :func:`seg_bal_pp_init` holds the balance, and read only by
    ``Projection.seg_index_start_init``, after its checks.
    """
    n = inforce_segment_max()
    table = model_point_table()
    ladder = inforce_segments().reset_index()
    rows = table.index.get_indexer(ladder["point_id"])
    slots = ladder["slot"].to_numpy(dtype="int64")
    held = slots <= n
    out = np.full((len(table), n + 1), np.nan)                       # noqa: F821
    out[rows[held], slots[held]] = pd.to_numeric(                    # noqa: F821
        ladder["seg_index_start_init"]).to_numpy(dtype="float64")[held]
    return out


def seg_index_cap_init():
    """The cap declared at each live segment's creation, by point and slot:
    float64 [point, slot].

    The column ``seg_index_cap_init`` of *inforce_segments_sec.csv*, per policy, held as
    :func:`seg_bal_pp_init` holds the balance, and read only by
    ``Projection.seg_index_cap_init``, after its checks.
    """
    n = inforce_segment_max()
    table = model_point_table()
    ladder = inforce_segments().reset_index()
    rows = table.index.get_indexer(ladder["point_id"])
    slots = ladder["slot"].to_numpy(dtype="int64")
    held = slots <= n
    out = np.full((len(table), n + 1), np.nan)                       # noqa: F821
    out[rows[held], slots[held]] = pd.to_numeric(                    # noqa: F821
        ladder["seg_index_cap_init"]).to_numpy(dtype="float64")[held]
    return out


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

inforce_segments_file = "inforce_segments_sec.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")

np = ("Module", "numpy")
