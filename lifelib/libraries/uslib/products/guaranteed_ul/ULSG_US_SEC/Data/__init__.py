# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.ULSG_US_SEC.Projection` as ``data``. :mod:`~.ULSG_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized Space
reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/guaranteed_ul/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded
values -- so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ULSG_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Seven of the tables are ULSG_US_S's.** The guaranteed COI scale, the corridor
factors, the mortality table, the class factors, the lapse table, the surrender charge
schedules and the return-of-premium windows are the files :mod:`~.ULSG_US_S` reads, read
here in place: one copy of each table serves both models, so an edit to one reaches
both. The model point table is this model's own, ``model_point_table_sec.csv``; it sits
beside ``ULSG_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader cell:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
coi_rates_file          coi_rates()                 coi_rates.csv
corridor_file           corridor_factors()          corridor_factors.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
surr_charge_file        surr_charge_table()         surr_charge_table.csv
rop_file                rop_table()                 rop_table.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Seven of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and five columns of an in-force policy's opening state, the
account value, the shadow account, the loan and the premiums paid to date, which are
``ULSG_US_S``'s own, and the months already spent in grace. :func:`model_point_table`
refuses a table that lacks any of them, or any column of ``ULSG_US_S``'s own that the
projection reads as a number or a flag, repeats a ``point_id``, holds a count, a
duration, an age or an amount no policy can have, a share of the premium or a
probability outside 0 to 1, a quoting precision that is not a whole number, a flag that
is not ``True`` or ``False``, or an opening state no policy can be in. The checks run in
turn, by 19 rules, and the first that fails raises, naming the missing column or every
point that fails it. It also refuses a policy to be issued more than
``future_horizon_mth`` months after the valuation date, 120 months as shipped: future new
business is written over a stated horizon, so that no frame runs longer than the
projection from issue plus that horizon. Set to 0, the Reference refuses future new
business altogether. A longer horizon projects in modelx, but the compiled model's
caches are sized for the shipped 120 months (``spec_sec.py``): it needs ``t`` there raised
to 12 x (charges_cease_age - issue_age_min) + the horizon + 2 and a rebuild, or a frame of
more than 1,357 months, the longest the caches hold with the month after it, raises
``IndexError`` compiled, naming nothing, at the first month past the caches. Whether a point
is still inside the projection at the valuation date, issued at an age with any cover, or
past the end of its grace is a rule of the product rather than of the table, and
``Projection.proj_len`` checks it, against two Projection References the caches are sized
from as they are from the horizon: ``charges_cease_age`` and ``issue_age_min``.

**So are the seven assumption tables.** Each table read at an attained age or a policy year
has one reader in ``Projection``, keyed by the age or the year, and that reader takes the
table's extent -- the first and last ages, or the last policy year, beyond which it reads
the nearest row -- from a cell here that reads the key column by value, once, and checks the
table: :func:`corridor_age_first` and :func:`corridor_age_last`, :func:`mort_age_first` and
:func:`mort_age_last`, :func:`lapse_last_year`, and, for the COI scale, whose sex and rate
class cells are numbered as schedules, :func:`coi_schedules`, which every COI vector asks
first. A key that is blank, text or not a whole number is refused, naming the file, the
column and the lines it is on, and so is an age below 0, since an age table is indexed by
the age. So are keys that do not run one row an age or a year, without a gap or a repeat,
policy years from 1, the message naming each key that repeats, with its lines, and each that
is missing. And so is a rate that is blank, text or infinite, naming the column and its
lines, and a lapse or mortality rate outside 0 to 1: each is a probability, and the monthly
rate ``1 - (1 - q)^(1/12)`` has no real value past 1. :func:`class_count` and
:func:`surr_charge_count` check the class factors and the surrender-charge schedules the
same way, for the per-point joins that read them, and :func:`surr_charge_count` refuses a
run-off that is not a whole number of years, 1 or more, which the projection divides by.
:func:`rop_count` checks the return-of-premium windows, read by membership of their
anniversaries: an anniversary that is not a whole number of years, 1 or more, or that is on
more than one row, is refused, and so is a refund ratio or an exercise rate outside 0 to 1.
A class factor, a guaranteed COI rate and a surrender charge below 0 are refused too: each
would project, with every check passing, a negative death, a credit for the insurance, or a
surrender charge that rises once its schedule has run off. So is a corridor factor below 0,
which no statutory percentage is. Each reader asks for its extent or its count before it
reads a value, so a projection meets the checks first. :func:`rop_last_anniv`, which asks
:func:`rop_count`, is the windows' extent.

``ULSG_US_S``'s readers take each extent from the key column as pandas reads it, where a
blank key is a missing value the extent skips: the table is cut short, and every later
age or year reads the last good row, without a word. A blank value is a missing value
to it too, which shows in its flows or is lost in a ``min`` or a ``max``: a blank lapse
rate reaches the lapse rate's floor and is read as it, a blank corridor factor reads as
no corridor, a blank surrender charge as none, and a blank COI rate reaches the account
value's floor at zero, which reads it as an exhausted account. Here each is refused, by
name, and so is a blank, text or infinite amount in the model point table.

``coi_rates.csv`` carries the **guaranteed maximum annual** rate per $1,000, by
attained age; ``Projection.coi_rate_guar`` divides it by twelve, which is the notes'
simple-twelfth conversion and one of their named pitfalls. The current scale is that
rate times ``Projection.coi_curr_factor`` (65%) and the shadow scale times
``Projection.coi_sg_factor`` (55%), because no carrier publishes either **[std]**.

Both mortality tables are small illustrative ones **[std]**, *not* published tables:
the notes forbid hard-coding the licensed 2017 CSO and 2015 VBT families, so
``coi_rates.csv`` ships a Perks curve fitted to the two figures the notes state -- the
8.615 per $1,000 per month guaranteed maximum at attained age 85, and a solved level
lifetime no-lapse premium near $10,800 for the anchor cell -- and ``mort_table.csv``
ships the same curve at 72% of the guaranteed basis. To swap in a licensed basis,
replace a file with a same-schema one, or point its filename Reference at a different
name before the model computes anything: a compiled model clears no cache, so there the
name is set on a package just imported, before anything is read. No formula changes.
Replacing the file changes :mod:`~.ULSG_US_S` too, which reads the same one.

**The vectors.** The readers return what the files hold, and no
:mod:`~.ULSG_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them.
The others read the arrays below instead, one element at a time, a model point's
attribute being the element at its position, ``data.sum_assured()[idx]``. That is what
lets the model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy
vector or table of int64 or float64, which compiles to a typed memoryview, never one of
bools, objects or text, and each count or extent is an int.

Text the projection needs is decoded here, into the number it selects: each value of the
premium pattern a monthly cell branches on into a 0/1 flag, the premium mode into its
payments a year, and the surrender-charge and return-of-premium flags into two more. The
model point's two pins become numbers: the persistency pin a value, NaN where blank, and
a flag of whether the point gives one, and the COI precision an int, -1 where blank,
``ULSG_US_S``'s own "exact". Each table keyed by more than a number becomes an
integer-indexed array or a join. The COI scales, keyed by sex and class, are numbered,
each point carrying the number of its own, and tabled by schedule and attained age. The
lapse table is held by policy year, the corridor and mortality tables by attained age,
each padded from 0, so that the year or the age is the index, and the return-of-premium
windows by anniversary, a flag of membership and the two values, so that the
anniversary is the index. The class factor and the surrender-charge schedule, each one
number a point, are joined to the points:

================================  =======  ===============  ==============================
Cells                             dtype    Shape            From
================================  =======  ===============  ==============================
point_id()                        int64    [point]          the table's index
age_at_entry()                    int64    [point]          ``age_at_entry``
guarantee_age()                   int64    [point]          ``guarantee_age``
duration_mth()                    int64    [point]          ``duration_mth``
grace_mth_init()                  int64    [point]          ``grace_mth_init``
coi_rate_dp()                     int64    [point]          ``coi_rate_dp``, -1 where blank
sum_assured()                     float64  [point]          ``sum_assured``
policy_count()                    float64  [point]          ``policy_count``
premium_pp_ann()                  float64  [point]          ``premium_pp_ann``
wd_pp()                           float64  [point]          ``wd_pp``
load_prem_rate()                  float64  [point]          ``load_prem_rate``
av_pp_init()                      float64  [point]          ``av_pp_init``
sg_pp_init()                      float64  [point]          ``sg_pp_init``
loan_bal_init()                   float64  [point]          ``loan_bal_init``
cum_prem_init()                   float64  [point]          ``cum_prem_init``
prem_persistency_override()       float64  [point]          ``prem_persistency_override``,
                                                            NaN where blank
has_prem_persistency_override()   int64    [point]          the same, 1 where not blank
has_surr_charge()                 int64    [point]          ``has_surr_charge``, 1 on True
rop_elected()                     int64    [point]          ``rop_elected``, 1 on True
is_level_premium()                int64    [point]          ``premium_type``, 1 on LEVEL
is_single_premium()               int64    [point]          ``premium_type``, 1 on SINGLE
is_ten_pay_premium()              int64    [point]          ``premium_type``, 1 on TEN_PAY
premium_freq()                    int64    [point]          ``premium_mode``, 1, 2, 4 or
                                                            12; 0 where unknown
class_factor()                    float64  [point]          *class_factor_table.csv*,
                                                            joined
surr_charge_rate_max()            float64  [point]          *surr_charge_table.csv*,
                                                            joined
surr_charge_runoff_years()        float64  [point]          *surr_charge_table.csv*,
                                                            joined
has_surr_charge_schedule()        int64    [point]          the same, 1 where the table
                                                            holds the id
coi_schedules()                   int      scalar           *coi_rates.csv*, checked
coi_schedule()                    int64    [point]          sex and class, joined
coi_rate_first_ages()             int64    [schedule]       *coi_rates.csv*
coi_rate_last_ages()              int64    [schedule]       *coi_rates.csv*
coi_rate_array()                  float64  [schedule, age]  *coi_rates.csv*
corridor_factor_array()           float64  [age]            *corridor_factors.csv*
mort_table_array()                float64  [age]            *mort_table.csv*
lapse_rate_array()                float64  [y]              *lapse_table.csv*
rop_last_anniv()                  int      scalar           *rop_table.csv*
rop_anniv_flags()                 int64    [anniversary]    *rop_table.csv*, 1 at a window
rop_ratio_array()                 float64  [anniversary]    *rop_table.csv*
rop_rate_array()                  float64  [anniversary]    *rop_table.csv*
================================  =======  ===============  ==============================

The table checks are the ints they were: :func:`lapse_last_year`, the four age extents,
:func:`class_count`, :func:`surr_charge_count` and :func:`rop_count`. The COI table's
check, which at stage ``E`` returned a Series of last ages, is the int
:func:`coi_schedules`, holding every message it held.

**An array is read by element, never whole,** in this Space as in
:mod:`~.ULSG_US_SEC.Projection`. The compiler types an array cell as a memoryview only
once it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python
object. So an array derived here from another reads the table's column, and a width
comes from a table or a check, never from another cell's array. Each table's check is one
cell that every array, extent and schedule number of the table reads first,
:func:`coi_schedules` for the COI scale, so that a projection, which reads an extent or a
schedule number first, meets the same refusal as a reader of the array. The column
keywords of a ``DataFrame.assign`` are passed as ``**{...}``, since a keyword named as a
cell of this Space, ``age``, ``age_at_entry``, would be rewritten by the export.

**What cannot be decoded or joined is refused** when the array is first read, naming every
point at fault: a ``point_id`` that is not a whole number; a ``rate_class`` the class
factors lack; a ``sex`` and ``rate_class`` the COI scale lacks; and on a point that
``has_surr_charge`` a ``surr_charge_id`` the schedules lack. ``ULSG_US_S`` fails every
projection of a point of the first two kinds, since it reads its class factor and its COI
scale in its first month in cover, and of the third its cash flows and margin check, which
read the schedule in every month of a point with a charge (its counts, accounts and
guarantee report do not); here that refusal is the table's, so every point with a charge is
refused those two reports with it, as ``Term_US_SEC``'s refusals at the first read are; a
point without a charge is never refused a projection for its schedule, whatever its id, as
``ULSG_US_S`` never reads it: its schedule is read where the table holds its id, and where
it does not, ``Projection.surr_charge_rate_max`` raises ``KeyError``, as at stage ``E``. A
value of ``premium_type`` none of the flags names, or of ``premium_mode`` none of the
frequencies, is no flag and frequency 0, and the cell that branches on it raises
``ULSG_US_S``'s message, as in ``ULSG_US_S``, so a SINGLE point, which never reads its mode,
projects whatever it is. Every decode and join compares the text exactly, as ``ULSG_US_S``
does, so ``"level"`` or ``"StdNT "`` is not ``"LEVEL"`` or ``"StdNT"``. A read beyond a
table's extent is refused where ``ULSG_US_S``'s lookup raised ``KeyError``, by the one
:mod:`~.ULSG_US_SEC.Projection` cell that reads the table, naming the point: a policy year
below 1 in ``lapse_rate_base_py``, an age below the scale's first in ``coi_rate_guar_at``,
and an anniversary without a window in ``rop_ratio_anniv`` and ``rop_rate_anniv``. An age
outside the corridor or mortality table reads the nearest row, as in ``ULSG_US_S``, and an
anniversary outside the windows' is in none, so no padding is read.

A table is held from age, year or anniversary 0 to its last key, so a key far past any a
policy reaches, an anniversary of 10**9 say, makes an array of that many elements, where
``ULSG_US_S`` reads the row or tests the membership without one. No rule bounds the keys
from above: a table's last key is its own, and each shipped table ends at an age or a
year the projection reaches.

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is first refused unless it is
below ``2**53`` in size, where the int64 holds ``ULSG_US_S``'s reading of it: the issue
age, the guarantee age, ``duration_mth``, the months in grace and the COI precision
(:func:`model_point_table`'s rule 19) and the ``point_id`` (:func:`point_id`). modelx
and the compiled model refuse alike, before any cast. Every other number is read into a
float64, as ``ULSG_US_S`` reads it, and no ``int()`` of a float is taken in a projection.
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

    Indexed by ``point_id``.  Seven columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``; and five columns of the opening state, per policy, as the
    policy stands at the start of month 0, before any month-0 event:

    * ``av_pp_init``, ``sg_pp_init``, ``loan_bal_init`` and ``cum_prem_init``: the
      account value, the shadow account, the loan and the premiums paid to date entering
      month 0, ``ULSG_US_S``'s own columns;
    * ``grace_mth_init``: the months already spent in grace entering month 0, which
      ``ULSG_US_S`` reads as 0 at the start of its frame.

    The rest are ``ULSG_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, by 19 rules in turn, and the first that
    fails raises ``ValueError``, naming the missing column or every point it fails on:

    1. the in-force columns are present, and so are the columns of ``ULSG_US_S``'s own
       that the projection reads as a number or a flag: ``age_at_entry``,
       ``sum_assured``, ``guarantee_age``, ``premium_pp_ann``, ``wd_pp``,
       ``load_prem_rate``, the two pins ``prem_persistency_override`` and
       ``coi_rate_dp``, and the flags ``has_surr_charge`` and ``rop_elected``;
    2. no ``point_id`` appears twice;
    3. ``policy_count`` is a number, zero or more;
    4. ``duration_mth`` is a whole number of months: positive for a policy in force, 0
       for one issued at the valuation date, negative for one issued later;
    5. no policy is issued more than ``future_horizon_mth`` months after the valuation
       date, so ``duration_mth`` is ``-future_horizon_mth`` or more.  At 0 the model takes
       no future new business, and the message says so; a negative horizon is itself
       refused;
    6. ``age_at_entry`` is a whole number of years, 0 or more: the projection takes its
       ``int()`` and counts its frame and every attained age on it;
    7. so is ``guarantee_age``, which ``ULSG_US_S`` takes the ``int()`` of, truncating
       95.5 to 95, and which decides the lifetime lapse multiplier;
    8. ``sum_assured`` is a number above 0, the face, which every policy holds: it
       reaches the death benefit, the per-unit charges and the surrender charge, and a
       blank one would reach them as a missing value, which the death benefit's ``max``
       then loses without a word;
    9. each of ``premium_pp_ann`` and ``wd_pp`` is a number, zero or more;
    10. ``load_prem_rate``, the share of each premium the load takes, is a number from 0 to
        1: past 1 the account would be credited a net premium below 0, which the account
        value's floor at zero absorbs, and at a load of 1.5 ``ULSG_US_S``'s account-value
        and margin checks fail on each of its points;
    11. ``prem_persistency_override`` is blank, where the point takes the rule, or a
        number from 0 to 1, a probability;
    12. ``coi_rate_dp`` is blank, where the point quotes its scales exact, or a whole
        number of decimal places, 0 or more: ``ULSG_US_S`` takes the ``int()`` of 2.5;
    13. each of ``has_surr_charge`` and ``rop_elected`` is ``True`` or ``False``, as
        pandas reads those words in any case.  A blank, a number or any other text is
        refused: one text value turns the whole column into text, where ``"False"`` is a
        true string, so every point would read as carrying the flag;
    14. ``av_pp_init`` is a number, zero or more.  A balance is never negative in force.
        ``ULSG_US_S`` lets the account value close a month below zero with a loan on an
        exhausted account, through the loaned part's lower credited rate; no policy in
        force can hold that balance, so such a point is restated no later than the last
        month its account value is still zero or more;
    15. ``sg_pp_init`` is a number, of either sign: the shadow account is never floored,
        and a negative balance is the catch-up shortfall;
    16. each of ``loan_bal_init`` and ``cum_prem_init`` is a number, zero or more;
    17. ``grace_mth_init`` is a whole number of months, 0 or more;
    18. a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: each
        of the five columns is 0, and the issue values come from the formulas;
    19. each of ``age_at_entry``, ``guarantee_age``, ``duration_mth``, ``grace_mth_init``
        and ``coi_rate_dp`` is below ``2**53`` in size, where the int64 vector it is read
        into holds it exactly: past int64 a float casts to the least int64 without a
        word.  Last, so that every earlier rule keeps its message.  ``ULSG_US_S`` projects
        a precision of ``2**53`` or more, which ``round`` reads as exact; the rule refuses
        it, as it does every number read into an int64.

    The text columns ``sex``, ``rate_class``, ``premium_type``, ``premium_mode`` and
    ``surr_charge_id`` are keys and labels, which this Space decodes or joins on at their
    first read (the Space docstring's *The vectors*).  The grace counter is not held to the
    account value: ``ULSG_US_S`` can carry a positive account value in grace, once the
    loaned part earns more than the unloaned, so no such rule could be right.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("av_pp_init", "sg_pp_init", "loan_bal_init", "cum_prem_init",
             "grace_mth_init")
    pins = ("prem_persistency_override", "coi_rate_dp")
    amounts = ("premium_pp_ann", "wd_pp")
    flags = ("has_surr_charge", "rop_elected")
    for column in ("policy_count", "duration_mth", "age_at_entry", "sum_assured",
                   "guarantee_age", *amounts, "load_prem_rate", *pins, *flags, *state):
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
    for column in ("age_at_entry", "guarantee_age"):
        ages = pd.to_numeric(table[column], errors="coerce")         # noqa: F821
        bad = table.index[~((ages % 1 == 0) & (ages >= 0))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number of years, 0 or "
                             f"more; it is not at point_id {bad}")
    face = pd.to_numeric(table["sum_assured"], errors="coerce")      # noqa: F821
    bad = table.index[~((face > 0) & (face < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured must be a number above 0, the face, "
                         f"which every policy holds; it is not at point_id {bad}")
    for column in amounts:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    v = pd.to_numeric(table["load_prem_rate"], errors="coerce")      # noqa: F821
    bad = table.index[~((v >= 0) & (v <= 1))].tolist()
    if bad:
        raise ValueError(f"{name}: load_prem_rate must be a number from 0 to 1; it is "
                         f"not at point_id {bad}")
    column = "prem_persistency_override"
    v = pd.to_numeric(table[column], errors="coerce")                # noqa: F821
    bad = table.index[table[column].notna() & ~((v >= 0) & (v <= 1))].tolist()
    if bad:
        raise ValueError(f"{name}: {column} must be blank or a number from 0 to 1; it "
                         f"is not at point_id {bad}")
    column = "coi_rate_dp"
    v = pd.to_numeric(table[column], errors="coerce")                # noqa: F821
    bad = table.index[table[column].notna() & ~((v % 1 == 0) & (v >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: {column} must be blank or a whole number, 0 or more; "
                         f"it is not at point_id {bad}")
    for column in flags:
        words = table[column].astype(str).str.lower()
        bad = table.index[~words.isin(["true", "false"])].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be True or False; it is not at "
                             f"point_id {bad}")
    values = {}
    for column in state:
        values[column] = pd.to_numeric(table[column], errors="coerce")  # noqa: F821
    v = values["av_pp_init"]
    bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: av_pp_init must be a number, zero or more: no policy "
                         f"in force holds a negative account value, so restate a point "
                         f"with a loan on an exhausted account no later than the last "
                         f"month its account value is still zero or more; it is not at "
                         f"point_id {bad}")
    v = values["sg_pp_init"]
    bad = table.index[~(v.abs() < float("inf"))].tolist()
    if bad:
        raise ValueError(f"{name}: sg_pp_init must be a number; it is not at point_id "
                         f"{bad}")
    for column in ("loan_bal_init", "cum_prem_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    v = values["grace_mth_init"]
    bad = table.index[~((v % 1 == 0) & (v >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: grace_mth_init must be a whole number of months, 0 "
                         f"or more; it is not at point_id {bad}")
    for column in state:
        bad = table.index[(months <= 0) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    for column in ("age_at_entry", "guarantee_age", "duration_mth", "grace_mth_init",
                   "coi_rate_dp"):
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[table[column].notna() & ~(v.abs() < 2.0 ** 53)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be below 2**53 in size, where an "
                             f"int64 holds it; it is not at point_id {bad}")
    return table


def coi_rates():
    """Guaranteed maximum **annual** COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by sex, rate class and **attained** age.
    The monthly rate is the annual rate divided by twelve **[std]** structure; [R3]
    requires the guaranteed maxima to be stated in the policy, and [REG-R17] names the
    2017 CSO family the notes point at.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*."""
    return pd.read_csv(input_dir() / corridor_file, index_col="age")  # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by attained age, from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / class_factor_file, index_col="rate_class")


def lapse_table():
    """The base annual lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")


def surr_charge_table():
    """The surrender charge schedules, read from *surr_charge_table.csv*.

    One row per ``surr_charge_id``, giving the initial charge per $1,000 of initial
    face and the number of years over which it runs off linearly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col="surr_charge_id")


def rop_table():
    """The return-of-premium exercise windows, read from *rop_table.csv*.

    One row per policy anniversary carrying a window: the refund ratio applied to
    cumulative premiums [S1] and the **[std]** exercise rate.
    """
    return pd.read_csv(input_dir() / rop_file, index_col="anniversary")  # noqa: F821


def coi_schedules():
    """The number of cells *coi_rates.csv* gives a scale for, the table checked.

    One schedule a cell, each ``sex`` and ``rate_class`` the table holds:
    :func:`coi_rate_array` holds each schedule in a row, numbered from 1 in the order of
    those keys, and :func:`coi_schedule` gives each point its number.  The table's one
    check, which each of them, :func:`coi_rate_first_ages` and :func:`coi_rate_last_ages`
    ask first.  The two text keys may not be blank, and the numeric key, ``age``, is read
    by value, once: an age that is blank, text or not a whole number is refused, naming
    the file and the lines it is on.  So is a cell whose ages do not run one row an age,
    without a gap or a repeat: the message names the cell, each age that repeats, with its
    lines, and each age missing between the cell's first and its last.  And so is a
    ``coi_rate_guar_ann`` that is blank, text, infinite or below 0, naming its lines: a
    charge per $1,000 of net amount at risk a year, never a credit, which the shipped scale
    holds above 1 at every age it charges, from 1.48 at 45 to 1,000 at 120, and at 0 at
    121, where charges cease; the current monthly rate passes 1 from attained age 69.  And
    so is an age below 0, since each schedule is held from age 0.
    ``Projection.coi_rate_last_age`` takes a point's extent from :func:`coi_rate_last_ages`
    before ``Projection.coi_rate_guar_at`` reads its scale.  A blank rate is a missing
    value to ``ULSG_US_S``, which its account value's floor at zero, a ``max``, then reads
    as an exhausted account.

    At stage ``E`` this check was :func:`coi_rate_last_ages`, which returned the last ages
    as a Series; a check is an int here, the number of schedules, and the arrays ask it,
    so every message is the one it was.
    """
    name = coi_rates_file                                            # noqa: F821
    rates = coi_rates().reset_index()
    for column in ("sex", "rate_class"):
        bad = (rates.index[rates[column].isna()] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must not be blank; it is on line {bad}")
    keys = pd.to_numeric(rates["age"], errors="coerce")              # noqa: F821
    bad = (rates.index[~(keys % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    rates = rates.assign(**{
        "age": pd.to_numeric(rates["age"]).astype("int64")})         # noqa: F821
    ages = rates.groupby(["sex", "rate_class"])["age"]
    last = ages.max()
    count = ages.count()
    run = (last - ages.min() + 1 == count) & (ages.nunique() == count)
    faults = []
    for cell in last.index[~run].tolist():
        held = ages.get_group(cell)
        for key in sorted(set(held[held.duplicated()])):
            faults.append(f"at {cell}, age {key} is on line "
                          f"{(held.index[held == key] + 2).tolist()}")
        cell_run = sorted(set(held))
        for a, b in zip(cell_run, cell_run[1:]):
            if b - a > 1:
                faults.append(f"at {cell}, no line holds age {a + 1}"
                              + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the ages of each sex and rate_class must run one row "
                         f"an age, without a gap or a repeat; " + "; ".join(faults))
    values = pd.to_numeric(rates["coi_rate_guar_ann"], errors="coerce")  # noqa: F821
    bad = (rates.index[~((values >= 0) & (values < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: coi_rate_guar_ann must be a number, zero or more; it "
                         f"is not on line {bad}")
    bad = (rates.index[rates["age"] < 0] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be 0 or more; it is not on line {bad}")
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
    since :func:`corridor_factor_array` holds the table from age 0.
    ``Projection.corridor_factor_at``, the table's one reader, takes both of its extents,
    this and :func:`corridor_age_first`, before it reads a factor.  A blank factor is a
    missing value to ``ULSG_US_S``, whose death benefit, the ``max`` of the face and the
    corridor's amount, then reads it as no corridor at all.  A factor below 1 only makes
    the corridor bind later, or never; below 0 it would make the corridor's amount on an
    account value below 0 a positive one, which only ``Projection.db_pp``'s floor on the
    account value keeps from the death benefit.
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
    checked being ``mort_rate``, which must also be from 0 to 1, as a probability; the
    shipped table reaches 1.0 at attained age 120.  An age below 0 is refused, as there.
    ``Projection.mort_rate_base_at``, the table's one reader, takes both of its extents,
    this and :func:`mort_age_first`, before it reads a rate.  A blank rate is a missing
    value to ``ULSG_US_S``, whose mortality is then not a number, and to
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
    before it reads a rate.  A blank rate is a missing value to ``ULSG_US_S``, which its
    lapse rate's floor, a ``max``, then reads as the floor.
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
    ``ULSG_US_S``, whose mortality is then not a number, and to ``Projection.mort_rate``,
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
    charge by the run-off, where ``ULSG_US_S`` divides by zero at 0.
    ``Projection.surr_charge_rate_max`` and ``Projection.surr_charge_runoff_years``, the
    table's two readers, ask for the count before they read a value, so a projection meets
    the checks first.  A blank charge is a missing value to ``ULSG_US_S``, whose surrender
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


def rop_count():
    """The number of windows *rop_table.csv* gives, the table checked.

    The return-of-premium endorsement's windows are read by membership of their
    anniversaries (``Projection.is_rop_anniv``), so the ``anniversary`` column is read by
    value, once, as the membership test matches it, so that an anniversary written
    ``20.0`` is 20.  One that is blank, text or not a whole number of years, 1 or more, is
    refused, naming the file and the lines it is on, and so is one on more than one row,
    naming each such anniversary with its lines: a window at an anniversary before the
    first, or two rows for one, would be read by no rule.  And so is a ``refund_ratio`` or
    an ``exercise_rate`` that is blank, text or outside 0 to 1, naming its lines: a share
    of the premiums paid, and a probability.  ``Projection.is_rop_anniv``,
    ``Projection.rop_ratio_anniv`` and ``Projection.rop_rate_anniv``, the table's three
    readers, ask for the count before they read the table, so a projection meets the
    checks first.
    """
    name = rop_file                                                  # noqa: F821
    table = rop_table()
    keys = pd.to_numeric(pd.Series(table.index), errors="coerce")    # noqa: F821
    bad = (keys.index[~((keys % 1 == 0) & (keys >= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: anniversary must be a whole number of years, 1 or "
                         f"more; it is not on line {bad}")
    faults = []
    for key in sorted(set(keys[keys.duplicated()])):
        faults.append(f"anniversary {int(key)} is on line "
                      f"{(keys.index[keys == key] + 2).tolist()}")
    if faults:
        raise ValueError(f"{name}: each anniversary must have one row; "
                         + "; ".join(faults))
    for column in ("refund_ratio", "exercise_rate"):
        v = pd.to_numeric(pd.Series(table[column].to_numpy()),       # noqa: F821
                          errors="coerce")
        bad = (v.index[~((v >= 0) & (v <= 1))] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number from 0 to 1; it is not "
                             f"on line {bad}")
    return len(table)


def coi_schedule():
    """The number of each model point's guaranteed COI scale, in table order: int64
    [point].

    The point's row of :func:`coi_rate_array`: the schedules of *coi_rates.csv*, one for
    each ``sex`` and ``rate_class`` it holds, numbered from 1 in the order of those keys,
    as :func:`coi_rate_array` numbers its rows, whatever the order of the file's lines.
    The point's key is its ``sex`` and its ``rate_class``, compared exactly, as
    ``ULSG_US_S`` slices the scale.  Every point reads its scale in its first month in
    cover, so ``ULSG_US_S`` fails every projection of a point whose key the table lacks:
    such a point is refused here, at the first read, naming every such point.  Asks
    :func:`coi_schedules` first, which checks the table.
    """
    coi_schedules()
    number = {}
    for key, _ in coi_rates().reset_index().groupby(["sex", "rate_class"]):
        number[key] = len(number) + 1
    table = model_point_table()
    sexes, classes = table["sex"].tolist(), table["rate_class"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    missing = []
    for i in range(len(sexes)):
        out[i] = number.get((sexes[i], classes[i]), 0)
        if out[i] == 0:
            missing.append(table.index[i])
    if missing:
        raise ValueError(f"{coi_rates_file} has no scale for the sex and rate_class of "
                         f"point_id {missing}")                      # noqa: F821
    return out


def coi_rate_first_ages():
    """The first attained age of each guaranteed COI scale: int64 [schedule].

    Element ``s`` is the first ``age`` *coi_rates.csv* holds for schedule ``s``, numbered
    as :func:`coi_schedule` numbers it, read by value once :func:`coi_schedules` has
    checked the table: 45 on the shipped anchor cell.  0 at element 0, which no point is
    given.  ``Projection.coi_rate_first_age`` reads it at the point's schedule.
    """
    n = coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age": pd.to_numeric(rates["age"]).astype("int64")})         # noqa: F821
    out = np.zeros(n + 1, dtype="int64")                             # noqa: F821
    s = 0
    for _, rows in rates.groupby(["sex", "rate_class"]):
        s += 1
        out[s] = int(rows["age"].min())
    return out


def coi_rate_last_ages():
    """The last attained age of each guaranteed COI scale: int64 [schedule].

    Element ``s`` is the last ``age`` *coi_rates.csv* holds for schedule ``s``, numbered
    as :func:`coi_schedule` numbers it, read by value once :func:`coi_schedules` has
    checked the table: 121 on the shipped anchor cell.  0 at element 0, which no point is
    given.  ``Projection.coi_rate_last_age`` reads it at the point's schedule before
    ``Projection.coi_rate_guar_at`` reads the scale.
    """
    n = coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age": pd.to_numeric(rates["age"]).astype("int64")})         # noqa: F821
    out = np.zeros(n + 1, dtype="int64")                             # noqa: F821
    s = 0
    for _, rows in rates.groupby(["sex", "rate_class"]):
        s += 1
        out[s] = int(rows["age"].max())
    return out


def coi_rate_array():
    """The guaranteed maximum annual COI rates by schedule and attained age: float64
    [schedule, age].

    Row ``s`` is schedule ``s`` of *coi_rates.csv*, numbered from 1 in the order of its
    keys, ``sex`` and ``rate_class``, as :func:`coi_schedule` numbers it, and column ``a``
    is attained age ``a``, so that the age is the index: one more column than the table's
    last age, one more row than its schedules.  Per $1,000 of net amount at risk a year.
    NaN in row 0, schedule 0, which no point is given, and outside each schedule's ages,
    below its first and past its last, all padding, which
    ``Projection.coi_rate_guar_at`` never reads: it refuses an age below the schedule's
    first and reads a later age at the schedule's last.  Asks :func:`coi_schedules`
    first, which checks the table.
    """
    n = coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age": pd.to_numeric(rates["age"]).astype("int64")})         # noqa: F821
    out = np.full((n + 1, int(rates["age"].max()) + 1), np.nan)      # noqa: F821
    s = 0
    for _, rows in rates.groupby(["sex", "rate_class"]):
        s += 1
        ages = rows["age"].to_numpy(dtype="int64")
        out[s, ages] = pd.to_numeric(                                # noqa: F821
            rows["coi_rate_guar_ann"]).to_numpy(dtype="float64")
    return out


def corridor_factor_array():
    """The GPT corridor factors by attained age: float64 [age].

    Element ``a`` is the ``corridor_factor`` of age ``a`` in *corridor_factors.csv*, so
    that the age is the index, to the last age :func:`corridor_age_last` gives once it
    has checked the table, which refuses a negative age.  NaN from 0 to below the first
    age, which ``Projection.corridor_factor_at`` never reads: it reads an age outside the
    table at the nearest row, as ``ULSG_US_S`` does.
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


def rop_last_anniv():
    """The last anniversary *rop_table.csv* gives a window at, the table checked.

    Read by value once :func:`rop_count` has checked the anniversaries and the values, so
    an anniversary written ``25.0`` is 25: the extent of :func:`rop_anniv_flags` and the
    two value arrays.  0 for a table with no window, where every flag array holds one
    element, 0.  ``Projection.is_rop_anniv`` asks it first, so a projection meets the check
    before it reads a flag, and answers an anniversary past it without a read.
    """
    rop_count()
    keys = pd.to_numeric(pd.Series(rop_table().index))               # noqa: F821
    return int(keys.max()) if len(keys) else 0


def rop_anniv_flags():
    """Whether a return-of-premium window follows each policy anniversary: int64
    [anniversary].

    Element ``y`` is 1 where *rop_table.csv* lists anniversary ``y`` and 0 elsewhere, from
    0 to :func:`rop_last_anniv`: ``ULSG_US_S``'s membership of the table's key column,
    ``y in rop_table().index``, held as an array padded with zeros, so that the
    anniversary is the index.
    """
    last = rop_last_anniv()
    keys = pd.to_numeric(pd.Series(rop_table().index)).to_numpy(dtype="int64")  # noqa: F821
    out = np.zeros(last + 1, dtype="int64")                          # noqa: F821
    out[keys] = 1
    return out


def rop_ratio_array():
    """The refund ratio of each return-of-premium window by anniversary: float64
    [anniversary].

    Element ``y`` is the ``refund_ratio`` of anniversary ``y`` in *rop_table.csv*, and NaN
    at each anniversary the table does not list, from 0 to :func:`rop_last_anniv`: padding,
    which ``Projection.rop_ratio_anniv`` never reads, since it asks
    ``Projection.is_rop_anniv`` first.
    """
    last = rop_last_anniv()
    table = rop_table()
    keys = pd.to_numeric(pd.Series(table.index)).to_numpy(dtype="int64")  # noqa: F821
    out = np.full(last + 1, np.nan)                                  # noqa: F821
    out[keys] = pd.to_numeric(                                       # noqa: F821
        table["refund_ratio"]).to_numpy(dtype="float64")
    return out


def rop_rate_array():
    """The exercise rate of each return-of-premium window by anniversary: float64
    [anniversary].

    Element ``y`` is the ``exercise_rate`` of anniversary ``y`` in *rop_table.csv*, held as
    :func:`rop_ratio_array` holds the refund ratio, and read only by
    ``Projection.rop_rate_anniv``, at a window.
    """
    last = rop_last_anniv()
    table = rop_table()
    keys = pd.to_numeric(pd.Series(table.index)).to_numpy(dtype="int64")  # noqa: F821
    out = np.full(last + 1, np.nan)                                  # noqa: F821
    out[keys] = pd.to_numeric(                                       # noqa: F821
        table["exercise_rate"]).to_numpy(dtype="float64")
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


def guarantee_age():
    """The elected guarantee age of every model point: int64 [point].

    The ``guarantee_age`` column, which :func:`model_point_table` holds to a whole number
    below ``2**53`` in size, 0 or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["guarantee_age"]).to_numpy(dtype="int64")


def duration_mth():
    """The completed policy months at the valuation date of every model point: int64
    [point].

    The ``duration_mth`` column, which :func:`model_point_table` holds to a whole number
    below ``2**53`` in size.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["duration_mth"]).to_numpy(dtype="int64")


def grace_mth_init():
    """The months already spent in grace entering month 0: int64 [point].

    The ``grace_mth_init`` column, which :func:`model_point_table` holds to a whole number
    below ``2**53`` in size, 0 or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["grace_mth_init"]).to_numpy(dtype="int64")


def coi_rate_dp():
    """The decimal places each model point quotes its COI scales to: int64 [point].

    The ``coi_rate_dp`` column, which :func:`model_point_table` holds to blank or a whole
    number, 0 or more, below ``2**53``, read as ``ULSG_US_S`` reads it: -1 where it is
    blank, ``ULSG_US_S``'s own "exact", so that ``Projection.coi_rate`` tests a number,
    not a missing value.
    """
    v = pd.to_numeric(model_point_table()["coi_rate_dp"])            # noqa: F821
    return v.fillna(-1).to_numpy(dtype="int64")


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
    """The scheduled annual premium per policy of every model point: float64 [point].

    The ``premium_pp_ann`` column, which :func:`model_point_table` holds to a number, zero
    or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["premium_pp_ann"]).to_numpy(dtype="float64")


def wd_pp():
    """The planned monthly withdrawal per policy of every model point: float64 [point].

    The ``wd_pp`` column, which :func:`model_point_table` holds to a number, zero or
    more.  ``Projection.wd_pp_mth`` reads it, since ``Projection.wd_pp`` is the month's
    withdrawal.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["wd_pp"]).to_numpy(dtype="float64")


def load_prem_rate():
    """The base premium load of every model point: float64 [point].

    The ``load_prem_rate`` column, which :func:`model_point_table` holds to a number from 0
    to 1.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["load_prem_rate"]).to_numpy(dtype="float64")


def av_pp_init():
    """The account value per policy entering month 0: float64 [point].

    The ``av_pp_init`` column, which :func:`model_point_table` holds to a number, zero or
    more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["av_pp_init"]).to_numpy(dtype="float64")


def sg_pp_init():
    """The shadow account per policy entering month 0: float64 [point].

    The ``sg_pp_init`` column, which :func:`model_point_table` holds to a number, of either
    sign.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["sg_pp_init"]).to_numpy(dtype="float64")


def loan_bal_init():
    """The loan per policy entering month 0: float64 [point].

    The ``loan_bal_init`` column, which :func:`model_point_table` holds to a number, zero or
    more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["loan_bal_init"]).to_numpy(dtype="float64")


def cum_prem_init():
    """The premiums paid per policy entering month 0: float64 [point].

    The ``cum_prem_init`` column, which :func:`model_point_table` holds to a number, zero or
    more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["cum_prem_init"]).to_numpy(dtype="float64")


def prem_persistency_override():
    """The premium persistency pin of every model point: float64 [point].

    The ``prem_persistency_override`` column, which :func:`model_point_table` holds to
    blank or a number from 0 to 1, NaN where it is blank, as ``ULSG_US_S`` reads it: a
    value read only where :func:`has_prem_persistency_override` says the point pins it.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["prem_persistency_override"]).to_numpy(dtype="float64")


def has_prem_persistency_override():
    """Whether each model point pins its premium persistency: int64 [point].

    1 where the ``prem_persistency_override`` column holds a number, 0 where it is blank,
    ``ULSG_US_S``'s ``pd.isna`` decided once for the table.
    """
    column = model_point_table()["prem_persistency_override"]
    return column.notna().to_numpy(dtype="int64")


def has_surr_charge():
    """Whether a surrender charge schedule applies to each model point: int64 [point].

    1 where the ``has_surr_charge`` column reads True, in any case, and 0 where it reads
    False: :func:`model_point_table` refuses any other value.
    """
    flags = model_point_table()["has_surr_charge"].astype(str).str.lower()
    return (flags == "true").to_numpy(dtype="int64")


def rop_elected():
    """Whether each model point elects the return-of-premium endorsement: int64 [point].

    1 where the ``rop_elected`` column reads True, in any case, and 0 where it reads
    False, as :func:`has_surr_charge` decodes its own.
    """
    flags = model_point_table()["rop_elected"].astype(str).str.lower()
    return (flags == "true").to_numpy(dtype="int64")


def is_level_premium():
    """Whether each model point's premium pattern is LEVEL: int64 [point].

    1 where ``premium_type`` is ``"LEVEL"``, compared element by element as ``ULSG_US_S``
    compares it, so that ``"level"`` or ``" LEVEL"`` is not, and 0 elsewhere.  A pattern
    none of the three is not refused here: it is no flag, and the projection cell that
    branches on the pattern raises ``ULSG_US_S``'s message on it.
    """
    return (model_point_table()["premium_type"] == "LEVEL").to_numpy(dtype="int64")


def is_single_premium():
    """Whether each model point's premium pattern is SINGLE: int64 [point].

    1 where ``premium_type`` is ``"SINGLE"``, as :func:`is_level_premium` decodes LEVEL.
    """
    return (model_point_table()["premium_type"] == "SINGLE").to_numpy(dtype="int64")


def is_ten_pay_premium():
    """Whether each model point's premium pattern is TEN_PAY: int64 [point].

    1 where ``premium_type`` is ``"TEN_PAY"``, as :func:`is_level_premium` decodes LEVEL.
    """
    return (model_point_table()["premium_type"] == "TEN_PAY").to_numpy(dtype="int64")


def premium_freq():
    """The scheduled premium payments a year of every model point: int64 [point].

    ``premium_mode`` decoded element by element, compared exactly as ``ULSG_US_S``
    compares it: ``"A"`` 1, ``"S"`` 2, ``"Q"`` 4 and ``"M"`` 12.  Any other value, a blank
    or ``"a"`` among them, is 0, and not refused here: ``ULSG_US_S`` reads the mode only
    on a point paying more than a single premium, so ``Projection.premium_freq`` raises
    ``ULSG_US_S``'s message on a 0 where it is read, and a SINGLE point projects whatever
    its mode.
    """
    modes = model_point_table()["premium_mode"].tolist()
    out = np.zeros(len(modes), dtype="int64")                        # noqa: F821
    for i in range(len(modes)):
        m = modes[i]
        if m == "A":
            out[i] = 1
        elif m == "S":
            out[i] = 2
        elif m == "Q":
            out[i] = 4
        elif m == "M":
            out[i] = 12
    return out


def class_factor():
    """The underwriting-class factor of each model point: float64 [point].

    The ``factor`` *class_factor_table.csv* gives the point's ``rate_class``, compared
    exactly, once :func:`class_count` has checked the table.  A point reads its class
    factor in its first month in cover, so ``ULSG_US_S`` fails every projection of a point
    whose class the table lacks: such a point is refused here, at the first read, naming
    every such point.
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
    every point whose id the table holds, with a charge or without, as ``ULSG_US_SEC``'s
    accessor read it at stage ``E``: a point without a charge reads its schedule, though
    no cell reads it there.  An id the table lacks, on a point with a charge, where
    ``ULSG_US_S``'s ``.loc`` raised ``KeyError`` in every month of such a point's cover, is
    refused, naming every such point.  On a point without a charge it is NaN, and
    :func:`has_surr_charge_schedule` 0: the point projects, and
    ``Projection.surr_charge_rate_max`` raises ``KeyError`` on it, as the ``.loc`` did at
    stage ``E``.  :func:`surr_charge_count` already refuses a run-off that is not a whole
    number of years, 1 or more, so no further rule is needed for the division by it.  The
    same check runs in :func:`surr_charge_runoff_years`, the join's other vector, so that
    whichever a projection reads first refuses the point.
    """
    surr_charge_count()
    table = model_point_table()
    values = pd.to_numeric(surr_charge_table()["sc_per_1000_init"])  # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing = []
    for i in range(len(ids)):
        if ids[i] in values.index:
            out[i] = float(values[ids[i]])
        elif flags[i]:
            missing.append(table.index[i])
    if missing:
        raise ValueError(f"{surr_charge_file} has no schedule for the surr_charge_id of "
                         f"point_id {missing}, each of which has_surr_charge")  # noqa: F821
    return out


def surr_charge_runoff_years():
    """The run-off, in policy years, of each model point's surrender charge: float64
    [point].

    The ``runoff_years`` of the point's ``surr_charge_id`` in *surr_charge_table.csv*, on
    every point whose id the table holds, NaN on a point without a charge whose id it
    lacks, joined and checked as :func:`surr_charge_rate_max` joins and checks the charge,
    with its refusal.
    """
    surr_charge_count()
    table = model_point_table()
    values = pd.to_numeric(surr_charge_table()["runoff_years"])      # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing = []
    for i in range(len(ids)):
        if ids[i] in values.index:
            out[i] = float(values[ids[i]])
        elif flags[i]:
            missing.append(table.index[i])
    if missing:
        raise ValueError(f"{surr_charge_file} has no schedule for the surr_charge_id of "
                         f"point_id {missing}, each of which has_surr_charge")  # noqa: F821
    return out


def has_surr_charge_schedule():
    """Whether *surr_charge_table.csv* holds each model point's schedule: int64 [point].

    1 where the point's ``surr_charge_id`` is a ``surr_charge_id`` of the table, compared
    exactly, as ``ULSG_US_S``'s ``.loc`` compares it, and 0 where it is not, blank
    included, once :func:`surr_charge_count` has checked the table.  0 only on a point
    without a charge, since :func:`surr_charge_rate_max` refuses the table where a point
    with a charge names an id it lacks: there ``Projection.surr_charge_rate_max`` and
    ``Projection.surr_charge_runoff_years`` raise ``KeyError``, naming the point.
    """
    surr_charge_count()
    known = surr_charge_table().index                                # noqa: F821
    ids = model_point_table()["surr_charge_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    for i in range(len(ids)):
        if ids[i] in known:
            out[i] = 1
    return out


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

surr_charge_file = "surr_charge_table.csv"

rop_file = "rop_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")

np = ("Module", "numpy")
