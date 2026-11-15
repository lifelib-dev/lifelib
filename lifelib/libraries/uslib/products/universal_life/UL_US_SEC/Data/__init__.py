# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.UL_US_SEC.Projection` as ``data``. :mod:`~.UL_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized
Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/universal_life/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded
values -- so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``UL_US_SEC`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

**Seven of the tables are UL_US_S's.** The guaranteed COI scale, the corridor factors,
the mortality table, the class factors, the lapse table, the premium persistency scale
and the surrender charge schedules are the files :mod:`~.UL_US_S` reads, read here in
place: one copy of each table serves both models, so an edit to one reaches both. The
model point table is this model's own, ``model_point_table_sec.csv``; it sits beside
``UL_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
coi_rates_file          coi_rates()                 coi_rates.csv
corridor_file           corridor_factors()          corridor_factors.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
prem_persistency_file   prem_persistency_table()    prem_persistency.csv
surr_charge_file        surr_charge_table()         surr_charge_table.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Eight of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the six columns of an in-force policy's opening state.
:func:`model_point_table` refuses a table that lacks any of them, repeats a
``point_id``, holds a count or a duration no policy can have, or holds an opening state
no policy can be in. The checks run in turn, and the first that fails raises, naming the
missing column or every point that fails it. It also refuses a policy to be issued more
than ``future_horizon_mth`` months after the valuation date, 120 months as shipped:
future new business is written over a stated horizon, so that no frame runs longer than
the projection from issue plus that horizon. Set to 0, the Reference refuses future new
business altogether. A longer horizon projects in modelx, but the compiled model's
caches are sized for the shipped 120 months (``spec_sec.py``): it needs ``t`` there raised
to 12 x (omega_age - issue_age_min + 1) + the horizon + 2 and a rebuild, or a frame
longer than 1,356 months raises ``IndexError`` compiled, naming nothing, at the first
month past the caches. Whether a point is still inside the projection at the valuation
date, and whether the contract issues it, are rules of the product rather than of the
table, and ``Projection.proj_len`` checks them, against two Projection References the
caches are sized from as they are from the horizon: ``omega_age`` and
``issue_age_min``.

The table is checked, too, wherever a projection reads a column as a number: each value
of the contract, the face, the premiums, the withdrawal, the load and the tax limits'
inputs, must be a number in the range the quantity can take, the surrender-charge flag
True or False, and the issue age a finite number (:func:`model_point_table`).

**So are the seven assumption tables.**  Each table read at a policy year or an attained
age has one reader in ``Projection``, keyed by the year or the age, and that reader takes
the table's extent -- the last policy year, or the first and last ages, beyond which it
reads the nearest row -- from a cell here that reads the key column by value, once, and
checks the table: :func:`prem_persistency_last_year`, :func:`lapse_last_year`,
:func:`corridor_age_first` and :func:`corridor_age_last`, :func:`mort_age_first` and
:func:`mort_age_last`, and, for the COI scale, whose issue-age cells are numbered as
schedules, :func:`coi_schedules`, which every COI vector asks first.  A key that is
blank, text or not a whole number is refused, naming the file, the column and the lines
it is on, and so is a negative age, since an age table is held from age 0.  So are keys
that do not run one row a year or an age, without a gap or a repeat, policy years from
1, the message naming each key that repeats, with its lines, and each that is missing.
And so is a rate that is blank, text or infinite, naming the column and its lines.
:func:`class_count` and :func:`surr_charge_count` check the class factors and the
surrender-charge schedules the same way, for the joins that read them,
:func:`class_factor`, :func:`surr_charge_rate_max`, :func:`surr_charge_runoff_years`
and :func:`has_surr_charge_schedule`. Each reader and each join asks for its extent, or
the count, before it reads a value, so a projection meets the checks first.

``UL_US_S``'s readers take the extent from the key column as pandas reads it, where a blank
key is a missing value the extent skips: the table is cut short, and every later year reads
the last good row, without a word.  A blank rate is a missing value to it too, which shows
in its flows or is lost in a ``min`` or a ``max``: a blank lapse rate reads as the cap of
35%, a blank corridor factor as no corridor and a blank surrender charge as none.  Here
a blank rate or class factor would make the mortality rate a missing value, as in
``UL_US_S``, and every flow after it, so each is refused, by name.

``coi_rates.csv`` carries the *guaranteed maximum* monthly rate per $1,000 of net
amount at risk; the current scale is the guaranteed scale times
``Projection.coi_curr_factor``, because current COI scales are not published **[std]**.
``mort_table.csv`` is a small illustrative best-estimate table **[std]**, not a
published one -- the notes forbid hard-coding the licensed 2015 VBT and 2017 CSO
families. To swap in a licensed basis, replace the file with a same-schema one, or
point ``mort_table_file`` at a different name before the model computes anything: a
compiled model clears no cache, so there the name is set on a package just imported,
before anything is read. No formula changes. Replacing the file changes
:mod:`~.UL_US_S` too, which reads the same one.

**The vectors.** The readers return what the files hold, and no
:mod:`~.UL_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them. The
others read the arrays below instead, one element at a time, a model point's attribute
being the element at its position, ``data.sum_assured()[idx]``. That is what lets the
model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy vector or
table of int64 or float64, which compiles to a typed memoryview, never one of bools,
objects or text, and each count of schedules is an int.

Text the projection needs is decoded here, into the number it selects: each value of the
death benefit option, the qualification test and the premium pattern a monthly cell
branches on into a 0/1 flag, and the surrender-charge flag into another. Each table keyed
by more than a number becomes an integer-indexed array or a join. The COI scales, keyed
by sex, class and issue age, are numbered, each point carrying the number of its own, and
tabled by schedule and policy year. The persistency and lapse tables are held by policy
year, and the corridor and mortality tables by attained age, each padded from 0, so that
the year or the age is the index. The class factor and the surrender-charge schedule,
each one number a point, are joined to the points:

==============================  =======  ===============  ==============================
Cells                           dtype    Shape            From
==============================  =======  ===============  ==============================
point_id()                      int64    [point]          the table's index
age_at_entry()                  int64    [point]          ``age_at_entry``
duration_mth()                  int64    [point]          ``duration_mth``
sum_assured()                   float64  [point]          ``sum_assured``
policy_count()                  float64  [point]          ``policy_count``
premium_pp_ann()                float64  [point]          ``premium_pp_ann``
wd_pp()                         float64  [point]          ``wd_pp``
load_prem_rate()                float64  [point]          ``load_prem_rate``
gsp()                           float64  [point]          ``gsp``
glp()                           float64  [point]          ``glp``
seven_pay_prem()                float64  [point]          ``seven_pay_prem``
av_pp_init()                    float64  [point]          ``av_pp_init``
loan_bal_init()                 float64  [point]          ``loan_bal_init``
sum_assured_init()              float64  [point]          ``sum_assured_init``
wd_used_year_init()             float64  [point]          ``wd_used_year_init``
cum_prem_init()                 float64  [point]          ``cum_prem_init``
is_mec_init()                   int64    [point]          ``is_mec_init``
has_surr_charge()               int64    [point]          ``has_surr_charge``, 1 on True
is_db_option_a()                int64    [point]          ``db_option``, 1 on A
is_db_option_b()                int64    [point]          ``db_option``, 1 on B
is_gpt()                        int64    [point]          ``qual_test``, 1 on GPT
is_level_premium()              int64    [point]          ``premium_type``, 1 on LEVEL
is_single_premium()             int64    [point]          ``premium_type``, 1 on SINGLE
is_target_premium()             int64    [point]          ``premium_type``, 1 on TARGET
class_factor()                  float64  [point]          *class_factor_table.csv*,
                                                          joined
surr_charge_rate_max()          float64  [point]          *surr_charge_table.csv*,
                                                          joined
surr_charge_runoff_years()      float64  [point]          *surr_charge_table.csv*,
                                                          joined
has_surr_charge_schedule()      int64    [point]          the same, 1 where the table
                                                          holds the id
coi_schedules()                 int      scalar           *coi_rates.csv*, checked
coi_schedule()                  int64    [point]          sex, class and issue age,
                                                          joined; 0 where not
coi_rate_last_years()           int64    [point]          *coi_rates.csv*, by schedule
coi_rate_array()                float64  [schedule, y]    *coi_rates.csv*
prem_persistency_array()        float64  [y]              *prem_persistency.csv*
lapse_rate_array()              float64  [y]              *lapse_table.csv*
corridor_factor_array()         float64  [age]            *corridor_factors.csv*
mort_table_array()              float64  [age]            *mort_table.csv*
==============================  =======  ===============  ==============================

The table checks are the ints they were: :func:`prem_persistency_last_year`,
:func:`lapse_last_year`, the four age extents, :func:`class_count` and
:func:`surr_charge_count`.

**An array is read by element, never whole,** in this Space as in
:mod:`~.UL_US_SEC.Projection`. The compiler types an array cell as a memoryview only once
it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python
object. So an array derived here from another reads the table's column, or the other
cell element by element, and a width comes from a table, never from another cell's array.
Each table's check is one cell that every array, extent and schedule number of the table
reads first, :func:`coi_schedules` for the COI scale, so that a projection, which reads
an extent or a schedule number first, meets the same refusal as a reader of the array.
The column keywords of a ``DataFrame.assign`` are passed as ``**{...}``, since a keyword
named as a cell of this Space, ``age_at_entry``, would be rewritten by the export.

**What cannot be decoded or joined is refused** when the array is first read, naming
every point at fault: a ``point_id`` that is not a whole number; a ``rate_class`` the
class factors lack, and on a point that ``has_surr_charge`` a ``surr_charge_id`` the
schedules lack, a run-off of 0 years, which the charge's run-off divides by, or a run-off
of ``2**53`` years or more in size (below). ``UL_US_S`` fails every projection of a point
whose class or charged schedule the tables lack, or whose run-off is 0, since it reads its
class factor in every month on the books, and its schedule in every month of a point with
a charge. It projects a run-off of ``2**53`` years or more, which is refused for the
compiled ``int()`` of it (below). A point without a charge is never refused for its
schedule, whatever its id, as ``UL_US_S`` never reads it: its schedule is read where the
table holds its id, and where it does not, ``Projection.surr_charge_rate_max`` raises
``KeyError``, as at stage ``E``. A point whose COI cell the
scale lacks is another matter: it reads its scale only while charges run, and a point
valued or issued at or past ``charges_cease_age`` never does, so ``UL_US_S`` projects it.
It is given schedule 0, and ``Projection.coi_rate_last_year`` refuses it, naming it, where
a rate is read. A value of ``db_option``, ``qual_test`` or ``premium_type`` none of the
flags names is no flag, and the cell that branches on them raises ``UL_US_S``'s message,
as in ``UL_US_S``. A read beyond a table's extent is refused where ``UL_US_S``'s lookup
raised ``KeyError``, by the one :mod:`~.UL_US_SEC.Projection` cell that reads the table,
naming the point: a policy year below 1 in ``prem_persistency_py``, ``lapse_rate_base_py``
and ``coi_rate_guar_py``. An age outside its table reads the nearest row, as in
``UL_US_S``, so no padding is read.

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is first refused unless it is
below ``2**53`` in size, where the int64 holds ``UL_US_S``'s reading of it: the issue age
and ``duration_mth`` (:func:`model_point_table`) and the ``point_id`` (:func:`point_id`).
A charged point's run-off is held to the same bound, though no cast is silent there: its
``int()``, in ``Projection.lapse_shock_year``, compiles to a Python int converted to a C
``long long``, exact below ``2**63`` and raising ``OverflowError`` past it, where
``UL_US_S`` projects a charge that never runs off. modelx and the compiled model refuse
alike, before any cast. A fractional issue age is not refused: it truncates toward
zero, as ``UL_US_S``'s ``int`` truncates it.
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

    Indexed by ``point_id``.  Eight columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``, and the six columns of the opening state, per policy, as
    the policy stands at the start of month 0, before any month-0 event:

    * ``av_pp_init`` and ``loan_bal_init``: the account value and the loan entering month
      0, ``UL_US_S``'s own two columns;
    * ``sum_assured_init``: the face in force entering month 0, after every withdrawal
      cut to date;
    * ``wd_used_year_init``: the free withdrawal allowance already used in the policy
      year under way;
    * ``cum_prem_init``: the premiums less withdrawals paid before the valuation date;
    * ``is_mec_init``: the MEC latch, an int code, 1 for a policy that has already
      failed the 7-pay test and 0 for one that has not.

    The rest are ``UL_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the eight in-force columns are present, and so is every other column a projection
      reads: ``age_at_entry``, ``sex``, ``rate_class``, ``sum_assured``, ``db_option``,
      ``qual_test``, ``premium_type``, ``premium_pp_ann``, ``load_prem_rate``, ``wd_pp``,
      ``has_surr_charge``, ``surr_charge_id``, ``gsp``, ``glp`` and ``seven_pay_prem``;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later; and below
      ``2**53`` months in size, where its int64 vector holds it (the Space docstring);
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more.  At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * ``age_at_entry`` is a finite number, below ``2**53`` in size, where its int64
      vector holds it.  A fraction is not refused: it truncates toward zero, as
      ``UL_US_S``'s ``int`` truncates it, and an age the contract does not issue is
      ``Projection.proj_len``'s to refuse;
    * the values of the contract, each of which a projection reads as a number, through a
      floor, a ``max`` or a ``min`` included, are each a number in the range the
      quantity can take: ``sum_assured``, the face at issue, a number above 0, which
      every policy holds; the planned premium ``premium_pp_ann``, the planned withdrawal
      ``wd_pp`` and the tax limits' inputs ``gsp``, ``glp`` and ``seven_pay_prem``, each a
      number, zero or more; and ``load_prem_rate``, a number from 0 to 1.  A blank, a text
      or an infinity is no such number;
    * ``has_surr_charge`` is True or False, as pandas reads those words in any case.  Any
      other value, a 1, a 0 or a blank among them, would make the column numbers or
      text, and ``UL_US_S``'s ``bool()`` reads the text ``"False"`` as true;
    * the account value, the loan, the face and the year's usage are each a number, zero
      or more.  A balance is never negative in force.  ``UL_US_S`` lets a point's account
      value fall below zero once it is in permanent shortfall, because it does not
      implement the grace cascade that would end such a policy; no policy in force can
      hold that balance, so a point in permanent shortfall is restated no later than the
      last month its account value is still zero or more.  Without a loan that is the
      month its shortfall begins, as point 7 is; with one, the shortfall test, which nets
      the loan, fails months earlier;
    * ``cum_prem_init`` is a number, of either sign.  Premiums less withdrawals is a tax
      measure, not a balance, and withdrawals taken in full count against it **[std]**;
    * ``is_mec_init`` is 0 or 1, an int code; 1.0 reads as True;
    * a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: it is
      issued with none, at the face :func:`~.UL_US_SEC.Projection.sum_assured`;
    * ``sum_assured_init`` is above 0 on a policy in force, which holds a face, so an
      extract that leaves the column at zero is refused rather than projected on the
      corridor alone;
    * ``sum_assured_init`` is at most ``sum_assured``, the face at issue, since face
      increases are not modelled.  A face below it is accepted, whether a withdrawal cut
      it or an elective decrease the model does not implement, and is projected from the
      value given;
    * on a point valued on a policy anniversary, ``duration_mth`` a multiple of 12,
      ``wd_used_year_init`` is 0: the year's free allowance restarts there, before any
      usage is read, so any other value would be dropped without a word;
    * ``is_mec_init`` is 1 where the 7-pay test has already failed in the month before
      the valuation date: ``cum_prem_init`` above ``seven_pay_prem`` times the policy
      years to date, in the first seven.  An earlier failure the cumulative premium no
      longer shows is the column's to record, and is accepted either way.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("av_pp_init", "loan_bal_init", "sum_assured_init", "wd_used_year_init",
             "cum_prem_init", "is_mec_init")
    read = ("age_at_entry", "sex", "rate_class", "sum_assured", "db_option", "qual_test",
            "premium_type", "premium_pp_ann", "load_prem_rate", "wd_pp", "has_surr_charge",
            "surr_charge_id", "gsp", "glp", "seven_pay_prem")
    for column in ("policy_count", "duration_mth", *state, *read):
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
    bad = table.index[~(ages.abs() < float("inf"))].tolist()
    if bad:
        raise ValueError(f"{name}: age_at_entry must be a finite number; it is not at "
                         f"point_id {bad}")
    bad = table.index[~(ages.abs() < 2.0 ** 53)].tolist()
    if bad:
        raise ValueError(f"{name}: age_at_entry must be below 2**53 in size; it is not "
                         f"at point_id {bad}")
    face = pd.to_numeric(table["sum_assured"], errors="coerce")      # noqa: F821
    bad = table.index[~((face > 0) & (face < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured must be a number above 0, the face at "
                         f"issue, which every policy holds; it is not at point_id {bad}")
    for column in ("premium_pp_ann", "wd_pp", "gsp", "glp", "seven_pay_prem"):
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
    flags = table["has_surr_charge"].astype(str).str.lower()
    bad = table.index[~flags.isin(["true", "false"])].tolist()
    if bad:
        raise ValueError(f"{name}: has_surr_charge must be True or False; it is not at "
                         f"point_id {bad}")
    values = {}
    for column in state:
        values[column] = pd.to_numeric(table[column], errors="coerce")  # noqa: F821
    v = values["av_pp_init"]
    bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: av_pp_init must be a number, zero or more: no policy "
                         f"in force holds a negative account value, so restate a point in "
                         f"permanent shortfall no later than the last month its account "
                         f"value is still zero or more; it is not at point_id {bad}")
    for column in ("loan_bal_init", "sum_assured_init", "wd_used_year_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    v = values["cum_prem_init"]
    bad = table.index[~(v.abs() < float("inf"))].tolist()
    if bad:
        raise ValueError(f"{name}: cum_prem_init must be a number; it is not at "
                         f"point_id {bad}")
    bad = table.index[~values["is_mec_init"].isin([0, 1])].tolist()
    if bad:
        raise ValueError(f"{name}: is_mec_init must be 0 or 1, an int code; it is not "
                         f"at point_id {bad}")
    for column in state:
        bad = table.index[(months <= 0) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    bad = table.index[(months > 0) & ~(values["sum_assured_init"] > 0)].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured_init must be above 0 on a policy in force, "
                         f"duration_mth above 0, which holds a face; it is not at "
                         f"point_id {bad}")
    bad = table.index[(months > 0) & ~(values["sum_assured_init"] <= face)].tolist()
    if bad:
        raise ValueError(f"{name}: sum_assured_init must be at most sum_assured, the "
                         f"face at issue, since face increases are not modelled; it is "
                         f"not at point_id {bad}")
    on_anniv = (months > 0) & (months % 12 == 0)
    bad = table.index[on_anniv & (values["wd_used_year_init"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: wd_used_year_init must be 0 on a point valued on a "
                         f"policy anniversary, duration_mth a multiple of 12, where the "
                         f"year's free allowance restarts; it is not at point_id {bad}")
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


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, from *corridor_factors.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / corridor_file, index_col="age")                # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col="age")              # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / class_factor_file, index_col="rate_class")     # noqa: F821


def lapse_table():
    """The base annual lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def prem_persistency_table():
    """Premium persistency (paid/planned) by policy year, from *prem_persistency.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / prem_persistency_file,                         # noqa: F821
        index_col="policy_year")


def surr_charge_table():
    """The surrender charge schedules, read from *surr_charge_table.csv*.

    One row per ``surr_charge_id``, giving the initial charge per $1,000 of initial
    face and the number of years over which it runs off linearly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col="surr_charge_id")


def prem_persistency_last_year():
    """The last policy year *prem_persistency.csv* gives a factor for, the table checked.

    The ``policy_year`` column is read by value, once, as the lookup matches it, so a year
    written ``16.0`` is year 16.  A key that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on.  So are policy years
    that do not run from 1, one row a year, without a gap or a repeat: the message names
    each year that repeats or falls below 1, with its lines, and each year missing from 1
    to the last.  And so is a ``prem_persistency`` factor that is blank, text or infinite,
    naming its lines.  ``Projection.prem_persistency_py``, the table's one reader, takes
    its extent from here before it reads a factor, so a projection meets the checks first.
    """
    name = prem_persistency_file                                     # noqa: F821
    table = prem_persistency_table()
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
    factors = pd.to_numeric(pd.Series(table["prem_persistency"].to_numpy()),  # noqa: F821
                            errors="coerce")
    bad = (factors.index[~(factors.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: prem_persistency must be a number; it is not on line "
                         f"{bad}")
    return int(years.max())


def lapse_last_year():
    """The last policy year *lapse_table.csv* gives a rate for, the table checked.

    Read and checked as :func:`prem_persistency_last_year` reads and checks its own
    table, the rate checked being ``lapse_rate_ann``.  ``Projection.lapse_rate_base_py``,
    the table's one reader, takes its extent from here before it reads a rate.
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
    bad = (rates.index[~(rates.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: lapse_rate_ann must be a number; it is not on line "
                         f"{bad}")
    return int(years.max())


def corridor_age_last():
    """The last attained age *corridor_factors.csv* gives a factor for, the table checked.

    The ``age`` column is read by value, once, so an age written ``40.0`` is 40.  A key
    that is blank, text or not a whole number is refused, naming the file, the column and
    the lines it is on, and so is a negative age, naming its lines:
    :func:`corridor_factor_array` holds the table from age 0, so that the age is the
    index, and ``UL_US_S``, which reads the nearest row, projects such a table.  So are
    ages that do not run one row an age, without a gap or a repeat: the message names
    each age that repeats, with its lines, and each age missing between the first and the
    last.  And so is a ``corridor_factor`` that is blank, text
    or infinite, naming its lines.  ``Projection.corridor_factor_at``, the table's one
    reader, takes both of its extents, this and :func:`corridor_age_first`, before it
    reads a factor.
    """
    name = corridor_file                                             # noqa: F821
    table = corridor_factors()
    ages = pd.to_numeric(pd.Series(table.index), errors="coerce")    # noqa: F821
    bad = (ages.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    ages = ages.astype("int64")
    bad = (ages.index[ages < 0] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be 0 or more; it is not on line {bad}")
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
    bad = (factors.index[~(factors.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: corridor_factor must be a number; it is not on line "
                         f"{bad}")
    return int(ages.max())


def corridor_age_first():
    """The first attained age *corridor_factors.csv* gives a factor for.

    Counted back from :func:`corridor_age_last`, which checks the table's keys first: the
    ages run one row an age, so the first is the last less the rows after it.
    """
    return corridor_age_last() - len(corridor_factors()) + 1


def mort_age_last():
    """The last attained age *mort_table.csv* gives a rate for, the table checked.

    Read and checked as :func:`corridor_age_last` reads and checks its own table, a
    negative age refused as there, since :func:`mort_table_array` holds the table from
    age 0, the rate checked being ``mort_rate``.  ``Projection.mort_rate_base_at``, the
    table's one reader, takes both of its extents, this and :func:`mort_age_first`,
    before it reads a rate.  A blank rate is a missing value to ``UL_US_S``, whose
    mortality is then not a number, and to ``Projection.mort_rate``, whose cap,
    ``min(q, 1.0)``, keeps it missing.
    """
    name = mort_table_file                                           # noqa: F821
    table = mort_table()
    ages = pd.to_numeric(pd.Series(table.index), errors="coerce")    # noqa: F821
    bad = (ages.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    ages = ages.astype("int64")
    bad = (ages.index[ages < 0] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be 0 or more; it is not on line {bad}")
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
    bad = (rates.index[~(rates.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a number; it is not on line {bad}")
    return int(ages.max())


def mort_age_first():
    """The first attained age *mort_table.csv* gives a rate for.

    Counted back from :func:`mort_age_last`, which checks the table's keys first, as
    :func:`corridor_age_first` counts its own.
    """
    return mort_age_last() - len(mort_table()) + 1


def coi_schedules():
    """The number of issue-age cells *coi_rates.csv* gives a scale for, the table checked.

    One schedule a cell, each ``sex``, ``rate_class`` and ``age_at_entry`` the table
    holds: :func:`coi_rate_array` holds each schedule in a row, numbered from 1 in the
    order of those keys, and :func:`coi_schedule` gives each point its number.  The table's
    one check, which each of them, and :func:`coi_rate_last_years`, asks first.  The two
    text keys may not be blank, and the two numeric keys, ``age_at_entry`` and
    ``policy_year``, are read by value, once: a key that is blank, text or not a whole
    number is refused, naming the file, the column and the lines it is on.  So is a cell
    whose policy years do not run from 1, one row a year, without a gap or a repeat: the
    message names the cell, each year that repeats or falls below 1, with its lines, and
    each year missing from 1 to the last.  And so is a ``coi_rate_guar`` that is blank,
    text or infinite, naming its lines.  ``Projection.coi_rate_last_year`` takes a
    point's extent from :func:`coi_rate_last_years` before ``Projection.coi_rate_guar_py``
    reads its scale, so a projection meets the checks first.
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
    bad = (rates.index[~(values.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: coi_rate_guar must be a number; it is not on line "
                         f"{bad}")
    return int(len(last))


def class_count():
    """The number of classes *class_factor_table.csv* gives a factor for, the table checked.

    A ``rate_class`` that is blank is refused, naming the file and the lines it is on, and
    so is one on more than one row, naming each such class with its lines; and so is a
    ``factor`` that is blank, text or infinite, naming its lines.
    ``Projection.class_factor``, the table's one reader, asks for the count before it reads
    a factor, so a projection meets the checks first.  A blank factor is a missing value to
    ``UL_US_S``, whose mortality is then not a number, and to ``Projection.mort_rate``,
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
    bad = (factors.index[~(factors.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: factor must be a number; it is not on line {bad}")
    return len(table)


def surr_charge_count():
    """The number of schedules *surr_charge_table.csv* gives, the table checked.

    A ``surr_charge_id`` that is blank is refused, naming the file and the lines it is on,
    and so is one on more than one row, naming each such schedule with its lines; and so
    is a ``sc_per_1000_init`` or a ``runoff_years`` that is blank, text or infinite,
    naming the column and its lines.  ``Projection.surr_charge_rate_max`` and
    ``Projection.surr_charge_runoff_years``, the table's two readers, ask for the count
    before they read a value, so a projection meets the checks first.  A blank charge is a
    missing value to ``UL_US_S``, whose surrender charge rate, the ``max`` of 0 and the
    charge left, is then 0 in every month, as though the schedule had run off.
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
    for column in ("sc_per_1000_init", "runoff_years"):
        values = pd.to_numeric(pd.Series(table[column].to_numpy()),  # noqa: F821
                               errors="coerce")
        bad = (values.index[~(values.abs() < float("inf"))] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number; it is not on line "
                             f"{bad}")
    return len(table)


def coi_schedule():
    """The number of each model point's guaranteed COI scale, in table order: int64
    [point].

    The point's row of :func:`coi_rate_array`: the schedules of *coi_rates.csv*, one for
    each ``sex``, ``rate_class`` and ``age_at_entry`` it holds, numbered from 1 in the
    order of those keys, as :func:`coi_rate_array` numbers its rows, whatever the order of
    the file's lines.  The point's key is its ``sex``, its ``rate_class`` and
    ``int`` of its ``age_at_entry``, as ``UL_US_S`` slices the scale.  A point whose key
    the table lacks gets schedule 0, a row of padding, and is not refused here:
    ``UL_US_S`` projects such a point while it reads no COI rate, as one valued, or
    issued, at or past ``charges_cease_age`` never does, and
    ``Projection.coi_rate_last_year`` refuses it, naming it, when one is read.  Asks
    :func:`coi_schedules` first, which checks the table.
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
    """The last policy year of each model point's guaranteed COI scale: int64 [point].

    The last ``policy_year`` *coi_rates.csv* holds for the point's schedule, numbered as
    :func:`coi_schedule` numbers it, read by value once :func:`coi_schedules` has checked
    the table: 87 on the shipped anchor cell.  0 for a point the table has no scale for,
    schedule 0, which ``Projection.coi_rate_last_year`` refuses where it is read.
    """
    coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64"),  # noqa: F821
        "policy_year": pd.to_numeric(rates["policy_year"]).astype("int64")})   # noqa: F821
    last = {}
    for key, rows in rates.groupby(["sex", "rate_class", "age_at_entry"]):
        last[key] = int(rows["policy_year"].max())
    table = model_point_table()
    sexes, classes = table["sex"].tolist(), table["rate_class"].tolist()
    ages = pd.to_numeric(table["age_at_entry"]).tolist()             # noqa: F821
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = last.get((sexes[i], classes[i], int(ages[i])), 0)
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


def prem_persistency_array():
    """The premium persistency factors by policy year: float64 [y].

    Element ``y`` is the ``prem_persistency`` of policy year ``y`` in
    *prem_persistency.csv*, so that the year is the index, to the last year
    :func:`prem_persistency_last_year` gives once it has checked the table.  NaN at 0,
    before the first year, which ``Projection.prem_persistency_py`` never reads.
    """
    last = prem_persistency_last_year()
    table = prem_persistency_table()
    years = pd.to_numeric(pd.Series(table.index)).to_numpy(dtype="int64")  # noqa: F821
    out = np.full(last + 1, np.nan)                                  # noqa: F821
    out[years] = pd.to_numeric(                                      # noqa: F821
        table["prem_persistency"]).to_numpy(dtype="float64")
    return out


def lapse_rate_array():
    """The base annual lapse rates by policy year: float64 [y].

    Element ``y`` is the ``lapse_rate_ann`` of policy year ``y`` in *lapse_table.csv*,
    held as :func:`prem_persistency_array` holds its own table, to the last year
    :func:`lapse_last_year` gives.  NaN at 0, which ``Projection.lapse_rate_base_py``
    never reads.
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
    table at the nearest row, as ``UL_US_S`` does.
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

    The ``age_at_entry`` column, which :func:`model_point_table` holds to a finite number
    below ``2**53`` in size, read as ``UL_US_S`` reads it, ``int`` of the number: a
    fraction truncates toward zero, so 35.5 projects as 35.
    """
    ages = pd.to_numeric(model_point_table()["age_at_entry"])        # noqa: F821
    return ages.to_numpy(dtype="int64")


def duration_mth():
    """The completed policy months at the valuation date of every model point: int64
    [point].

    The ``duration_mth`` column, which :func:`model_point_table` holds to a whole number
    of months below ``2**53`` in size.
    """
    months = pd.to_numeric(model_point_table()["duration_mth"])      # noqa: F821
    return months.to_numpy(dtype="int64")


def sum_assured():
    """The face at issue of every model point: float64 [point].

    The ``sum_assured`` column, which :func:`model_point_table` holds to a number above 0.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["sum_assured"]).to_numpy(dtype="float64")


def policy_count():
    """The policies each model point stands for: float64 [point].

    The ``policy_count`` column, which :func:`model_point_table` holds to a number, zero
    or more.
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
    more.  ``Projection.wd_pp_mth`` reads it, since ``Projection.wd_pp`` is the month's
    withdrawal.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["wd_pp"]).to_numpy(dtype="float64")


def load_prem_rate():
    """The current premium load rate of every model point: float64 [point].

    The ``load_prem_rate`` column, which :func:`model_point_table` holds to a number from
    0 to 1.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["load_prem_rate"]).to_numpy(dtype="float64")


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

    The ``seven_pay_prem`` column, which :func:`model_point_table` holds to a number,
    zero or more.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["seven_pay_prem"]).to_numpy(dtype="float64")


def av_pp_init():
    """The account value per policy entering month 0: float64 [point].

    The ``av_pp_init`` column of the opening state, checked by :func:`model_point_table`.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["av_pp_init"]).to_numpy(dtype="float64")


def loan_bal_init():
    """The loan per policy entering month 0: float64 [point].

    The ``loan_bal_init`` column of the opening state, checked by
    :func:`model_point_table`.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["loan_bal_init"]).to_numpy(dtype="float64")


def sum_assured_init():
    """The face in force entering month 0: float64 [point].

    The ``sum_assured_init`` column of the opening state, checked by
    :func:`model_point_table`.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["sum_assured_init"]).to_numpy(dtype="float64")


def wd_used_year_init():
    """The free withdrawal allowance used in the policy year under way: float64 [point].

    The ``wd_used_year_init`` column of the opening state, checked by
    :func:`model_point_table`.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["wd_used_year_init"]).to_numpy(dtype="float64")


def cum_prem_init():
    """The premiums less withdrawals per policy before the valuation date: float64
    [point].

    The ``cum_prem_init`` column of the opening state, checked by
    :func:`model_point_table`.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["cum_prem_init"]).to_numpy(dtype="float64")


def is_mec_init():
    """The MEC latch entering month 0: int64 [point].

    The ``is_mec_init`` column of the opening state, which :func:`model_point_table`
    holds to 0 or 1, so a 1.0 reads as 1.
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
    """Whether each model point's death benefit is Option A: int64 [point].

    1 where ``db_option`` is ``"A"``, compared element by element as ``UL_US_S``
    compares it, and 0 elsewhere.  A value neither A nor B is not refused here: it is no
    flag, and ``Projection.db_pp`` raises ``UL_US_S``'s message on it.
    """
    return (model_point_table()["db_option"] == "A").to_numpy(dtype="int64")


def is_db_option_b():
    """Whether each model point's death benefit is Option B: int64 [point].

    1 where ``db_option`` is ``"B"``, as :func:`is_db_option_a` decodes A.
    """
    return (model_point_table()["db_option"] == "B").to_numpy(dtype="int64")


def is_gpt():
    """Whether each model point elected the Guideline Premium Test: int64 [point].

    1 where ``qual_test`` is ``"GPT"``, and 0 elsewhere, where
    ``Projection.corridor_factor`` raises ``UL_US_S``'s message.
    """
    return (model_point_table()["qual_test"] == "GPT").to_numpy(dtype="int64")


def is_level_premium():
    """Whether each model point's premium pattern is LEVEL: int64 [point].

    1 where ``premium_type`` is ``"LEVEL"``, and 0 elsewhere.  A pattern none of the
    three is no flag, and ``Projection.premium_pp`` raises ``UL_US_S``'s message on it.
    """
    return (model_point_table()["premium_type"] == "LEVEL").to_numpy(dtype="int64")


def is_single_premium():
    """Whether each model point's premium pattern is SINGLE: int64 [point].

    1 where ``premium_type`` is ``"SINGLE"``, as :func:`is_level_premium` decodes LEVEL.
    """
    return (model_point_table()["premium_type"] == "SINGLE").to_numpy(dtype="int64")


def is_target_premium():
    """Whether each model point's premium pattern is TARGET: int64 [point].

    1 where ``premium_type`` is ``"TARGET"``, as :func:`is_level_premium` decodes LEVEL.
    """
    return (model_point_table()["premium_type"] == "TARGET").to_numpy(dtype="int64")


def class_factor():
    """The underwriting-class factor of each model point: float64 [point].

    The ``factor`` *class_factor_table.csv* gives the point's ``rate_class``, once
    :func:`class_count` has checked the table.  A point reads its class factor in every
    month on the books, so ``UL_US_S`` fails every projection of a point whose class the
    table lacks: such a point is refused here, at the first read, naming every such
    point.
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
    every point whose id the table holds, with a charge or without, as ``UL_US_SEC``'s
    accessor read it at stage ``E``: a point without a charge reads its schedule, though
    no cell reads it there.  On a point without a charge whose id the table lacks, blank
    included, it is NaN, and :func:`has_surr_charge_schedule` 0: the point projects, and
    ``Projection.surr_charge_rate_max`` raises ``KeyError`` on it, as the ``.loc`` did at
    stage ``E``.  The join refuses, naming every such point with a charge, and only on a
    point with one, since ``UL_US_S`` reads the schedule in every month of such a point's
    cover: an id the table lacks, where ``UL_US_S``'s ``.loc`` raised ``KeyError``; a
    ``runoff_years`` of 0, which ``Projection.surr_charge_rate`` divides by; and one of
    ``2**53`` years or more in size, the bound of every number read as an int, past which
    the compiled ``int()`` in ``Projection.lapse_shock_year`` would in time raise
    ``OverflowError``.  The same checks run in :func:`surr_charge_runoff_years`, the
    join's other vector, so that whichever a projection reads first refuses the point.
    """
    surr_charge_count()
    table = model_point_table()
    schedules = surr_charge_table()
    charges = pd.to_numeric(schedules["sc_per_1000_init"])           # noqa: F821
    years = pd.to_numeric(schedules["runoff_years"])                 # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing, zero, huge = [], [], []
    for i in range(len(ids)):
        if ids[i] not in charges.index:
            if flags[i]:
                missing.append(table.index[i])
        elif flags[i] and years[ids[i]] == 0:
            zero.append(table.index[i])
        elif flags[i] and not abs(years[ids[i]]) < 2.0 ** 53:
            huge.append(table.index[i])
        else:
            out[i] = float(charges[ids[i]])
    if missing:
        raise ValueError(f"{surr_charge_file} has no schedule for the surr_charge_id of "
                         f"point_id {missing}, each of which has_surr_charge")  # noqa: F821
    if zero:
        raise ValueError(f"{surr_charge_file}: runoff_years must not be 0 on the "
                         f"schedule of point_id {zero}, each of which has_surr_charge, "
                         f"since the charge runs off over it")       # noqa: F821
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
    with its refusals.  A point without a charge reads the run-off as written, 0 or
    ``2**53`` years included, which no cell reads there.
    """
    surr_charge_count()
    table = model_point_table()
    years = pd.to_numeric(surr_charge_table()["runoff_years"])       # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing, zero, huge = [], [], []
    for i in range(len(ids)):
        if ids[i] not in years.index:
            if flags[i]:
                missing.append(table.index[i])
        elif flags[i] and years[ids[i]] == 0:
            zero.append(table.index[i])
        elif flags[i] and not abs(years[ids[i]]) < 2.0 ** 53:
            huge.append(table.index[i])
        else:
            out[i] = float(years[ids[i]])
    if missing:
        raise ValueError(f"{surr_charge_file} has no schedule for the surr_charge_id of "
                         f"point_id {missing}, each of which has_surr_charge")  # noqa: F821
    if zero:
        raise ValueError(f"{surr_charge_file}: runoff_years must not be 0 on the "
                         f"schedule of point_id {zero}, each of which has_surr_charge, "
                         f"since the charge runs off over it")       # noqa: F821
    if huge:
        raise ValueError(f"{surr_charge_file}: runoff_years must be below 2**53 years in "
                         f"size on the schedule of point_id {huge}, each of which "
                         f"has_surr_charge")                         # noqa: F821
    return out


def has_surr_charge_schedule():
    """Whether *surr_charge_table.csv* holds each model point's schedule: int64 [point].

    1 where the point's ``surr_charge_id`` is a ``surr_charge_id`` of the table, compared
    exactly, as ``UL_US_S``'s ``.loc`` compares it, and 0 where it is not, blank
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

prem_persistency_file = "prem_persistency.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")

np = ("Module", "numpy")