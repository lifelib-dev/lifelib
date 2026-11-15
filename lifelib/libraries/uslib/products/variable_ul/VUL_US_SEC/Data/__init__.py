# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The ten input CSVs are read here, **once per model**, and referenced from
:mod:`~.VUL_US_SEC.Projection` as ``data``. :mod:`~.VUL_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized
Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/variable_ul/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values --
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VUL_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Nine of the tables are VUL_US_S's.** The subaccount lineup, the return scenario, the
guaranteed COI scale, the corridor factors, the mortality table, the class factors, the
lapse table, the premium persistency scale and the surrender charge schedules are the
files :mod:`~.VUL_US_S` reads, read here in place: one copy of each table serves both
models, so an edit to one reaches both. The model point table is this model's own,
``model_point_table_sec.csv``; it sits beside ``VUL_US_S``'s ``model_point_table.csv``,
which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ============================  ==============================
Reference               Cells                         File
======================  ============================  ==============================
model_point_file        model_point_table()           model_point_table_sec.csv
subaccount_file         subaccount_table()            subaccount_table.csv
scenario_file           scenario_table()              scenario_table.csv
coi_rates_file          coi_rates()                   coi_rates.csv
corridor_file           corridor_factors()            corridor_factors.csv
mort_table_file         mort_table()                  mort_table.csv
class_factor_file       class_factor_table()          class_factor_table.csv
lapse_table_file        lapse_table()                 lapse_table.csv
prem_persistency_file   prem_persistency_table()      prem_persistency.csv
surr_charge_file        surr_charge_table()           surr_charge_table.csv
======================  ============================  ==============================

**The model point table is checked as it is read.** Ten of its columns are the in-force
interface, with the shipped lineup of two subaccounts: ``policy_count`` and
``duration_mth``, as in ``basiclife.BasicTerm_SE``; six columns of an in-force policy's
opening state, one ``sa_pp_init_<i>`` for each subaccount, the value of the fixed option
and of the loan account, the debt and the face in force; and ``VUL_US_S``'s two
first-month pins, which are not state. :func:`model_point_table` refuses a table that lacks
any of them, or any column of ``VUL_US_S``'s own that the projection reads as a number,
repeats a ``point_id``, holds a count, a duration, an issue age or an amount no policy can
have, a surrender-charge flag that is not ``True`` or ``False``, or an opening state no
policy can be in. The checks run in turn, and the first that fails raises, naming the
missing column or every point that fails it. It also refuses a policy to be issued more
than ``future_horizon_mth`` months after the valuation date, 120 months as shipped:
future new business is written over a stated horizon, so that no frame runs longer than
the projection from issue plus that horizon. Set to 0, the Reference refuses future new
business altogether. Whether a point is still inside the projection at the valuation
date is a rule of the product rather than of the table, and ``Projection.proj_len``
checks it.

**So are the nine assumption tables.** Each table read at a policy year or an attained
age has one reader in ``Projection``, keyed by the year or the age, and that reader takes
the table's extent -- the last policy year, or the first and last ages, beyond which it
reads the nearest row -- from a cell here that reads the key column by value, once, and
checks the table: :func:`prem_persistency_last_year`, :func:`lapse_last_year`,
:func:`corridor_age_first` and :func:`corridor_age_last`, :func:`mort_age_first` and
:func:`mort_age_last`, and, for the COI scale, whose issue-age cells are numbered as
schedules, :func:`coi_schedules`, which every COI vector asks first. A key that is blank,
text or not a whole number is refused, naming the file, the column and the lines it is
on, and so is a negative age, since an age table is held from age 0. So are keys that do
not run one row a year or an age, without a gap or a repeat, policy years from 1, the
message naming each key that repeats, with its lines, and each that is missing. And so is
a rate that is blank, text or infinite, naming the column and its lines, and a lapse or
mortality rate outside 0 to 1: each is a probability, and the monthly rate
``1 - (1 - q)^(1/12)`` has no real value past 1. :func:`class_count` and
:func:`surr_charge_count` check the class factors and the surrender-charge schedules
the same way, for the per-point joins that read them, and :func:`surr_charge_count`
refuses a run-off that is not a whole number of years, 1 or more, which the projection
divides by and counts policy years on. A class factor, a guaranteed COI rate, a fund
expense, a premium persistency factor, a surrender charge and a corridor factor below 0
are refused too: each would project, with every check passing, a count or a charge no
policy can have, a negative death or premium, a credit for the insurance or the fund, a
surrender charge that rises once its schedule has run off, or a death benefit past the
option's amount on an account value below 0.
:func:`subaccount_count` checks the lineup, whose ids name the model point table's
columns, and :func:`scenario_count` the return scenario, whose months run one row a month
for each scenario and subaccount. Each reader asks for its extent, the count or the
lineup before it reads a value, so a projection meets the checks first.

``VUL_US_S``'s readers take each extent from the key column as pandas reads it, where a
blank key is a missing value the extent skips: the table is cut short, and every later
year reads the last good row, without a word. A blank value is a missing value to it
too, which shows in its flows or is lost in a ``min`` or a ``max``: a blank corridor
factor reads as no corridor, a blank surrender charge as none, and a blank COI rate, fund
expense or return reaches the account value as a missing value, which the cash value's
floor at zero then reads as nothing to pay on a surrender. Here each is refused, by name,
and so is a blank, text or infinite amount in the model point table.

``scenario_table.csv`` is the **separate-account return scenario**: monthly *gross*
subaccount returns keyed by ``scenario_id``, ``subaccount_id`` and the month ``t``, the
same index as ``Projection``'s ``t``, which counts months from the valuation date: a
scenario is a path of the economy from that date, one path for every point of a block,
however old the policy, with the last month of a scenario repeating for the rest of the
projection. Fund expenses and the M&E charge are applied on top of these in
:func:`~.VUL_US_SEC.Projection.inv_return_mth`, so the table holds gross returns only. A
stochastic set is a data change -- more ``scenario_id`` values -- not a formula change.
The shipped scenarios are deterministic: ``WE`` is the worked example's month (+1.00%
equity, -0.50% bond) followed by a level 6% a year gross path, and ``LEVEL6`` is that
level path throughout. A scenario's months may start after month 0 -- a path re-based to
a policy issued after the valuation date holds nothing before its issue month -- and a
read before a scenario's first month raises. The scenario's vectors hold its months to
``return_horizon_mth``, 1,585 as shipped, the last month a frame the contract allows can
read, however far the table runs (:func:`gross_return_array`), and a read past it raises.

``coi_rates.csv`` carries the **guaranteed maximum** monthly rate per $1,000 of net
amount at risk; the current scale is that times
``Projection.coi_curr_factor``, or the model point's first-month pin. The notes require
the 2017 CSO ultimate ANB table for the guaranteed maximum and the 2015 VBT for
best-estimate mortality; both are licensed and may not be reproduced here, so
``coi_rates.csv`` and ``mort_table.csv`` ship small illustrative **[std]** tables
instead -- the COI scale anchored on the one disclosed guaranteed point in the notes
(male 45 standard non-tobacco, policy year 1 = $0.22 [S4]) and the mortality table well
below it, because the notes insist the COI *charge* basis and the death *decrement*
basis must never be conflated. To swap in a licensed basis, replace either file with a
same-schema one, or point ``mort_table_file`` at a different name before the model
computes anything. No formula changes. Replacing the file changes :mod:`~.VUL_US_S` too,
which reads the same one.

**The vectors.** The readers return what the files hold, and no
:mod:`~.VUL_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them. The
others read the arrays below instead, one element at a time, a model point's attribute
being the element at its position, ``data.sum_assured()[idx]``, and a subaccount's the
element at its position in the lineup, ``data.alloc()[idx, i]``. That is what lets the
model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy vector or
table of int64 or float64, which compiles to a typed memoryview, never one of bools,
objects or text, and each check of a table is an int.

Text the projection needs is decoded here, into the number it selects: each value of the
death benefit option, the qualification test and the premium pattern a monthly cell
branches on into a 0/1 flag, the surrender-charge flag into another, and each first-month
pin into its value, NaN where blank as ``VUL_US_S`` reads it, and a flag that says whether
the point gives one. Each table keyed by more than a number becomes an integer-indexed
array or a join. The COI scales, keyed by sex, class and issue age, are numbered, each
point carrying the number of its own, and tabled by schedule and policy year; the return
scenarios, keyed by their ID, are numbered too, each point carrying the number of its
own, and tabled by scenario, subaccount and month. The subaccounts are positions in the
lineup, from 0, in the file's order, their ids kept in a vector for the reports. The
persistency and lapse tables are held by policy year, and the corridor and mortality
tables by attained age, each padded from 0, so that the year or the age is the index.
The class factor and the surrender-charge schedule, each one number a point, are joined to
the points:

==============================  =======  ===================  ==========================
Cells                           dtype    Shape                From
==============================  =======  ===================  ==========================
point_id()                      int64    [point]              the table's index
age_at_entry()                  int64    [point]              ``age_at_entry``
duration_mth()                  int64    [point]              ``duration_mth``
sum_assured()                   float64  [point]              ``sum_assured``
policy_count()                  float64  [point]              ``policy_count``
premium_pp_ann()                float64  [point]              ``premium_pp_ann``
wd_pp()                         float64  [point]              ``wd_pp``
load_prem_rate()                float64  [point]              ``load_prem_rate``
alloc_fixed()                   float64  [point]              ``alloc_fixed``
alloc()                         float64  [point, sa]          ``alloc_<id>``, by position
sa_pp_init()                    float64  [point, sa]          ``sa_pp_init_<id>``, by
                                                              position
fa_pp_init()                    float64  [point]              ``fa_pp_init``
la_pp_init()                    float64  [point]              ``la_pp_init``
loan_bal_init()                 float64  [point]              ``loan_bal_init``
sum_assured_init()              float64  [point]              ``sum_assured_init``
has_surr_charge()               int64    [point]              ``has_surr_charge``, 1 on
                                                              True
is_db_option_a()                int64    [point]              ``db_option``, 1 on A
is_db_option_b()                int64    [point]              ``db_option``, 1 on B
is_gpt()                        int64    [point]              ``qual_test``, 1 on GPT
is_level_premium()              int64    [point]              ``premium_type``, 1 on LEVEL
is_single_premium()             int64    [point]              ``premium_type``, 1 on
                                                              SINGLE
corridor_override_m1()          float64  [point]              the pin, NaN where blank
has_corridor_override_m1()      int64    [point]              the pin, 1 where given
coi_rate_override_m1()          float64  [point]              the pin, NaN where blank
has_coi_rate_override_m1()      int64    [point]              the pin, 1 where given
class_factor()                  float64  [point]              *class_factor_table.csv*,
                                                              joined
surr_charge_rate_max()          float64  [point]              *surr_charge_table.csv*,
                                                              joined
surr_charge_runoff_years()      float64  [point]              *surr_charge_table.csv*,
                                                              joined
has_surr_charge_schedule()      int64    [point]              the same, 1 where the
                                                              table holds the id
subaccount_count()              int      scalar               *subaccount_table.csv*,
                                                              checked
subaccounts()                   int64    [sa]                 ``subaccount_id``
fund_expense_ann()              float64  [sa]                 ``fund_expense_ann``
coi_schedules()                 int      scalar               *coi_rates.csv*, checked
coi_schedule()                  int64    [point]              sex, class and issue age,
                                                              joined; 0 where not
coi_rate_last_years()           int64    [schedule]           *coi_rates.csv*
coi_rate_array()                float64  [schedule, y]        *coi_rates.csv*
scenario_count()                int      scalar               *scenario_table.csv*,
                                                              checked
scenario_index()                int64    [point]              ``scenario_id``, joined
scenario_first_mths()           int64    [scenario, sa]       *scenario_table.csv*
scenario_last_mths()            int64    [scenario, sa]       *scenario_table.csv*
gross_return_array()            float64  [scenario, sa, t]    *scenario_table.csv*
prem_persistency_array()        float64  [y]                  *prem_persistency.csv*
lapse_rate_array()              float64  [y]                  *lapse_table.csv*
corridor_factor_array()         float64  [age]                *corridor_factors.csv*
mort_table_array()              float64  [age]                *mort_table.csv*
==============================  =======  ===================  ==========================

The table checks are the ints they were, :func:`prem_persistency_last_year`,
:func:`lapse_last_year`, the four age extents, :func:`class_count` and
:func:`surr_charge_count`, and the three that were Series and DataFrames are now ints,
each the check of its table: :func:`subaccount_count` the lineup's, :func:`scenario_count`
the return scenario's and :func:`coi_schedules` the COI scale's. ``scenario_rows`` stays
the scenario table's reader, a plain DataFrame, and ``scenario_table`` its indexed copy.

**An array is read by element, never whole,** in this Space as in
:mod:`~.VUL_US_SEC.Projection`. The compiler types an array cell as a memoryview only once
it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python
object. So an array derived here from another reads the table's column, or the other
cell element by element, ``subaccounts()[k]``, and a width comes from a table or a
check's int, never from another cell's array, nor from an index that calls one. Each
table's check is one int cell that every array, extent and number of the table reads
first, so that a projection, which reads an extent or a number first, meets the same
refusal as a reader of the array. The column keywords of a ``DataFrame.assign`` are passed
as ``**{...}``, since a keyword named as a cell of this Space, ``age_at_entry``, would be
rewritten by the export.

**What cannot be decoded or joined is refused** when the array is first read, naming
every point at fault: a ``point_id`` that is not a whole number; a ``rate_class`` the
class factors lack; a ``scenario_id`` the return scenario lacks, or one without a row for
a subaccount of the lineup; and on a point that ``has_surr_charge`` a ``surr_charge_id``
the schedules lack, or a run-off of ``2**53`` years or more in size (below). ``VUL_US_S``
fails every projection of a point whose class, scenario or charged schedule the tables
lack, since it reads its class factor and every subaccount's return in its first month
on the books, and its schedule in every month of a point with a charge; here the table is
refused, as in the family's other compiled models. A point without a charge is never
refused for its schedule, whatever its id, as ``VUL_US_S`` never reads it: its schedule
is read where the table holds its id, and where it does not,
``Projection.surr_charge_rate_max`` raises ``KeyError``, as at stage ``E``. A point whose
COI cell the scale lacks is another matter: it reads its scale only while charges run,
and a point valued or issued at or past ``charges_cease_age`` never does, so ``VUL_US_S``
projects it. It is given schedule 0, and ``Projection.coi_rate_last_year`` refuses it,
naming it, where a rate is read. A value of ``db_option``, ``qual_test`` or
``premium_type`` none of the flags names is no flag, and the cell that branches on them
raises ``VUL_US_S``'s message, as in ``VUL_US_S``. A read beyond a table's extent is
refused where ``VUL_US_S``'s lookup raised ``KeyError``, by the one
:mod:`~.VUL_US_SEC.Projection` cell that reads the table, naming the point: a policy year
below 1 in ``prem_persistency_py``, ``lapse_rate_base_py`` and ``coi_rate_guar_at``, a
month before a scenario's first in ``gross_return_mth``, and a subaccount's position past
the lineup in the four cells that read a subaccount's input. An age outside its table
reads the nearest row, as in ``VUL_US_S``, so no padding is read.

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is first refused unless it is
below ``2**53`` in size, where the int64 holds ``VUL_US_S``'s reading of it: the issue age
and ``duration_mth`` (:func:`model_point_table`) and the ``point_id`` (:func:`point_id`).
A charged point's run-off is held to the same bound, though no cast is silent there: its
``int()``, in ``Projection.lapse_shock_month``, compiles to a Python int converted to a C
``long long``, exact below ``2**63`` and raising ``OverflowError`` past it, where
``VUL_US_S`` projects a charge that never runs off. modelx and the compiled model refuse
alike, before any cast. A fractional issue age stays refused, as at stage ``E``: ``Data``
refuses it with the other values no policy can have, where ``UL_US_SEC``'s truncates as
``UL_US_S``'s ``int`` does.
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

    Indexed by ``point_id``.  Ten columns are the in-force interface, with the shipped
    lineup of two subaccounts: ``policy_count`` and ``duration_mth``, the completed policy
    months at the valuation date, as in ``basiclife.BasicTerm_SE``; six columns of the
    opening state, per policy, as the policy stands at the start of month 0, before any
    month-0 event, one ``sa_pp_init_<i>`` for each subaccount among them; and
    ``VUL_US_S``'s two first-month pins, which are not state:

    * ``sa_pp_init_<i>``, one for each id :func:`subaccounts` lists, and
      ``fa_pp_init``: the value of each subaccount and of the fixed option entering
      month 0, ``VUL_US_S``'s own columns;
    * ``la_pp_init``: the loan account, the collateral the loan has moved out of the
      investment options, entering month 0;
    * ``loan_bal_init``: the policy debt entering month 0, ``VUL_US_S``'s own column;
    * ``sum_assured_init``: the face in force entering month 0, after every Option A
      withdrawal cut to date;
    * ``corridor_override_m1`` and ``coi_rate_override_m1``: ``VUL_US_S``'s first-month
      pins, which apply in the valuation month, ``t = 0``, blank where a point pins
      nothing.

    The rest are ``VUL_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the in-force columns are present, and so are ``age_at_entry``, the
      surrender-charge flag ``has_surr_charge``, the amounts the projection reads as
      numbers, ``sum_assured``, ``premium_pp_ann`` and ``wd_pp``, and the shares it
      reads, ``load_prem_rate``, each ``alloc_<i>`` and ``alloc_fixed``;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later; and below
      ``2**53`` months in size, where its int64 vector holds it (the Space docstring);
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more.  At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * ``age_at_entry`` is a whole number of years, 0 or more: the projection takes its
      ``int()`` and counts its frame and every attained age on it.  And it is below
      ``2**53`` in size, where its int64 vector holds it.  A fraction is refused, as at
      stage ``E``, where ``UL_US_SEC``'s truncates; an age the contract does not issue is
      ``Projection.proj_len``'s to refuse;
    * ``sum_assured`` is a number above 0, the face at issue, which every policy holds;
      each of ``premium_pp_ann`` and ``wd_pp`` is a number, zero or more; and each of
      ``load_prem_rate``, ``alloc_<i>`` and ``alloc_fixed``, the share of each premium
      the load takes and the shares of each net premium the accounts take, is a number
      from 0 to 1.  Each reaches the account value, and a blank one would reach it as a
      missing value, which the cash value's floor, the net amount at risk's and the
      corridor's ``max`` then lose without a word: in ``VUL_US_S`` a blank face projects
      no death claim on Option A, and a missing value on Option B.  A load past 1 would
      credit the accounts a net premium below 0, every check passing, and allocations
      past 1 more than the net premium;
    * ``has_surr_charge`` is ``True`` or ``False``, as pandas reads those words in any
      case.  A blank, a number or any other text is refused: one text value turns the
      whole column into text, where ``"False"`` is a true string, so every point would
      read as carrying a surrender charge;
    * each subaccount, the fixed option, the loan account, the debt and the face in force
      is a number, zero or more.  A balance is never negative in force.  ``VUL_US_S``
      lets a subaccount fall below zero once the point is in permanent shortfall, because
      it does not implement the grace cascade that would end such a policy; no policy in
      force can hold that balance, so a point in permanent shortfall is restated no later
      than the last month its subaccounts are still zero or more;
    * a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: it is
      issued with none, at the face :func:`~.VUL_US_SEC.Projection.sum_assured`;
    * ``sum_assured_init`` is above 0 on a policy in force, which holds a face, so an
      extract that leaves the column at zero is refused rather than projected on the
      corridor alone;
    * ``sum_assured_init`` is at most ``sum_assured``, the face at issue, since face
      increases are not modelled.  A face below it is accepted, whether a withdrawal cut
      it or an elective decrease the model does not implement, and is projected from the
      value given;
    * the loan account is above 0 exactly where the debt is: a loan moves value out of
      the investment options into the loan account, and the model takes no new loan and
      no repayment, so the two are held together from the loan's first day, each at its
      own rate;
    * each pin is blank, or a number, zero or more;
    * each pin is blank on a policy issued after the valuation date: a pin applies in the
      valuation month, ``t = 0``, before such a policy is issued, so it would never apply.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    accounts = []
    allocations = []
    for k in range(subaccount_count()):
        accounts.append(f"sa_pp_init_{int(subaccounts()[k])}")
        allocations.append(f"alloc_{int(subaccounts()[k])}")
    state = (*accounts, "fa_pp_init", "la_pp_init", "loan_bal_init", "sum_assured_init")
    pins = ("corridor_override_m1", "coi_rate_override_m1")
    amounts = ("premium_pp_ann", "wd_pp")
    shares = ("load_prem_rate", *allocations, "alloc_fixed")
    for column in ("policy_count", "duration_mth", "age_at_entry", "sum_assured", *amounts,
                   *shares, "has_surr_charge", *state, *pins):
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
    for column in (*accounts, "fa_pp_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more: no "
                             f"policy in force holds a negative account value, so restate "
                             f"a point in permanent shortfall no later than the last month "
                             f"its account value is still zero or more; it is not at "
                             f"point_id {bad}")
    for column in ("la_pp_init", "loan_bal_init", "sum_assured_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
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
    lent = values["loan_bal_init"] > 0
    bad = table.index[(values["la_pp_init"] > 0) != lent].tolist()
    if bad:
        raise ValueError(f"{name}: la_pp_init must be above 0 where loan_bal_init is, and "
                         f"0 where it is 0: the loan account holds a loan's collateral "
                         f"while the loan is outstanding; it is not at point_id {bad}")
    for column in pins:
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[table[column].notna()
                          & ~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a number, zero or more; "
                             f"it is not at point_id {bad}")
    for column in pins:
        bad = table.index[(months < 0) & table[column].notna()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank on a policy issued after "
                             f"the valuation date, duration_mth below 0: a pin applies in "
                             f"the valuation month, t = 0, before such a policy is "
                             f"issued; it is not at point_id {bad}")
    return table


def subaccount_table():
    """The separate-account subaccount lineup, read from *subaccount_table.csv*.

    One row per subaccount, giving its name and its annual fund operating expense
    ratio.  The two-subaccount lineup is a **[std]** collapse of the observed menus.
    The projection reads it through :func:`subaccounts`, its checked copy.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / subaccount_file,                               # noqa: F821
        index_col="subaccount_id")


def subaccount_count():
    """The number of subaccounts in the lineup, *subaccount_table.csv* checked.

    The lineup's one check, which every vector of the lineup asks first:
    :func:`subaccounts`, :func:`fund_expense_ann`, :func:`alloc` and :func:`sa_pp_init`,
    and :func:`model_point_table`, which names the columns it checks from the ids.  The
    ``subaccount_id`` column is read by value, once, as an int: an id written ``1.0`` is
    subaccount 1, and names the model point table's ``alloc_1`` and ``sa_pp_init_1``,
    where ``VUL_US_S``, which names the column from the id as pandas reads it, asks a
    projection for ``sa_pp_init_1.0`` and raises.  An id that is blank, text or not a whole
    number is refused, naming the file and the lines it is on; so is a table with no
    subaccount, and an id on more than one row, naming each such id with its lines; and
    so is a ``fund_expense_ann`` that is blank, text, infinite or below 0, naming its
    lines.  ``Projection.subaccount_count`` reads it, and ``Projection.proj_len`` refuses a
    lineup of more than ``subaccount_max`` subaccounts, the most the compiled model's
    caches hold.  Rows keep the file's order, and a subaccount's position in it, from 0,
    is the ``i`` every ``Projection`` cell of a subaccount takes.
    """
    name = subaccount_file                                           # noqa: F821
    rows = subaccount_table().reset_index()
    ids = pd.to_numeric(rows["subaccount_id"], errors="coerce")      # noqa: F821
    bad = (rows.index[~(ids % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: subaccount_id must be a whole number; it is not on "
                         f"line {bad}")
    if not len(rows):
        raise ValueError(f"{name}: no line holds a subaccount")
    ids = ids.astype("int64")
    faults = []
    for key in sorted(set(ids[ids.duplicated()])):
        faults.append(f"subaccount_id {key} is on line "
                      f"{(ids.index[ids == key] + 2).tolist()}")
    if faults:
        raise ValueError(f"{name}: each subaccount_id must have one row; "
                         + "; ".join(faults))
    values = pd.to_numeric(rows["fund_expense_ann"], errors="coerce")  # noqa: F821
    bad = (rows.index[~((values >= 0) & (values < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: fund_expense_ann must be a number, zero or more; it is "
                         f"not on line {bad}")
    return len(rows)


def subaccounts():
    """The ``subaccount_id`` of each subaccount of the lineup, in file order: int64 [sa].

    Element ``i`` is the id of the subaccount at position ``i`` of *subaccount_table.csv*,
    read by value once :func:`subaccount_count` has checked the lineup, so an id written
    ``1.0`` is 1.  The ids name the model point table's ``alloc_<id>`` and
    ``sa_pp_init_<id>`` columns, which :func:`alloc` and :func:`sa_pp_init` read by
    position, and ``Projection.result_av``'s columns; no projection cell reads an id.
    """
    subaccount_count()
    ids = pd.to_numeric(subaccount_table().reset_index()["subaccount_id"])  # noqa: F821
    return ids.to_numpy(dtype="int64")


def fund_expense_ann():
    """The annual fund operating expense ratio of each subaccount: float64 [sa].

    The ``fund_expense_ann`` column of *subaccount_table.csv*, in file order, so that the
    subaccount's position is the index, once :func:`subaccount_count` has checked the
    lineup, which refuses a ratio that is blank, text, infinite or below 0.
    """
    subaccount_count()
    return pd.to_numeric(                                            # noqa: F821
        subaccount_table()["fund_expense_ann"]).to_numpy(dtype="float64")


def scenario_rows():
    """Monthly gross subaccount returns, read from *scenario_table.csv* in the file's order.

    The table's one read, a plain table on a default index, so that a refusal can name
    the lines a fault is on: :func:`scenario_count` checks it, the scenario's vectors,
    :func:`scenario_index`, :func:`scenario_first_mths`, :func:`scenario_last_mths` and
    :func:`gross_return_array`, are built from it, and :func:`scenario_table` indexes it
    as ``VUL_US_S`` reads it.
    """
    return pd.read_csv(input_dir() / scenario_file)                  # noqa: F821


def scenario_table():
    """Monthly gross subaccount returns, from *scenario_table.csv*, indexed for lookup.

    Keyed by ``scenario_id``, ``subaccount_id`` and the month ``t``, counted from the
    valuation date, 0-based; months past a scenario's last row repeat it.  Returns are
    **gross**: fund expenses and the M&E charge are applied on top of them in the
    projection, so a table row is the fund's own return before any charge.  The index is
    sorted so partial slices of the three-level key are lexsorted.  It is
    :func:`scenario_rows` indexed, the same frame ``VUL_US_S``'s reader reads, kept for a
    reader who wants the table so; no projection cell reads it, and
    ``Projection.gross_return_mth`` reads :func:`gross_return_array` instead.
    """
    return scenario_rows().set_index(
        ["scenario_id", "subaccount_id", "t"]).sort_index()


def scenario_count():
    """The number of scenarios *scenario_table.csv* holds, the table checked.

    The return scenario's one check, which every vector of the scenario asks first:
    :func:`scenario_index`, :func:`scenario_first_mths`, :func:`scenario_last_mths` and
    :func:`gross_return_array`, each of which numbers the scenarios from 1 in the order of
    their ``scenario_id``, as ``groupby`` sorts them, whatever the order of the file's
    lines.  Each cell of the table is the rows of one scenario and subaccount, the return
    path one subaccount is read from on that scenario, months past the last repeating it.
    ``scenario_id`` may not be blank, and the two numeric keys, ``subaccount_id`` and
    ``t``, are read by value, once: a key that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on, and
    ``return_horizon_mth``, the last month the scenario's vectors hold, must be 0 or more.
    A cell whose months do not run one row a month, from 0 or later, without a gap or a
    repeat is refused: the message names the cell, each month that repeats or falls below
    0, with its lines, and each month missing between the cell's first and its last.  A
    cell may start after month 0: a path re-based to a policy issued after the valuation
    date holds nothing before its issue month, so that a read there raises.  And a
    ``gross_return_mth`` that is blank, text or infinite is refused, naming its lines.  A
    subaccount the lineup does not hold is checked as any other, and not read.
    """
    name = scenario_file                                             # noqa: F821
    reach = return_horizon_mth                                       # noqa: F821
    if reach < 0:
        raise ValueError(f"return_horizon_mth must be 0 months or more, not {reach}")
    rows = scenario_rows()
    bad = (rows.index[rows["scenario_id"].isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    for column in ("subaccount_id", "t"):
        keys = pd.to_numeric(rows[column], errors="coerce")          # noqa: F821
        bad = (rows.index[~(keys % 1 == 0)] + 2).tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on line "
                             f"{bad}")
    rows = rows.assign(**{
        "subaccount_id": pd.to_numeric(rows["subaccount_id"]).astype("int64"),  # noqa: F821
        "t": pd.to_numeric(rows["t"]).astype("int64")})                         # noqa: F821
    months = rows.groupby(["scenario_id", "subaccount_id"])["t"]
    last = months.max()
    count = months.count()
    run = ((months.min() >= 0) & (last - months.min() + 1 == count)
           & (months.nunique() == count))
    faults = []
    for cell in last.index[~run].tolist():
        held = months.get_group(cell)
        for key in sorted(set(held[held.duplicated() | (held < 0)])):
            faults.append(f"at {cell}, t {key} is on line "
                          f"{(held.index[held == key] + 2).tolist()}")
        cell_run = sorted(set(held[held >= 0]))
        for a, b in zip(cell_run, cell_run[1:]):
            if b - a > 1:
                faults.append(f"at {cell}, no line holds t {a + 1}"
                              + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the months of each scenario_id and subaccount_id must "
                         f"run one row a month, from 0 or later, without a gap or a "
                         f"repeat; " + "; ".join(faults))
    values = pd.to_numeric(rows["gross_return_mth"], errors="coerce")  # noqa: F821
    bad = (rows.index[~(values.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: gross_return_mth must be a number; it is not on line "
                         f"{bad}")
    return int(rows["scenario_id"].nunique())


def scenario_last_mths():
    """The last month of each scenario and subaccount of *scenario_table.csv*: int64
    [scenario, sa].

    Row ``s`` is scenario ``s``, numbered from 1 in the order of the table's
    ``scenario_id``, as :func:`scenario_index` numbers it, and column ``i`` the
    subaccount at position ``i`` of the lineup, :func:`subaccounts`: the last ``t`` the
    table holds for the cell, read by value once :func:`scenario_count` has checked it,
    or, where the cell runs past ``return_horizon_mth``, the last month
    :func:`gross_return_array` holds, which falls below the cell's first month,
    :func:`scenario_first_mths`, where the cell starts past the horizon.
    -1 where the scenario holds no row for the subaccount, and in row 0, padding, which
    no point is given: :func:`scenario_index` refuses a point whose scenario lacks a
    subaccount of the lineup.  ``Projection.scenario_last_mth`` reads it, and
    ``Projection.gross_return_mth`` reads a month past it, to the horizon, at the last.
    """
    n = scenario_count()
    rows = scenario_rows()
    rows = rows.assign(**{
        "subaccount_id": pd.to_numeric(rows["subaccount_id"]).astype("int64"),  # noqa: F821
        "t": pd.to_numeric(rows["t"]).astype("int64")})                         # noqa: F821
    kept = rows["t"][rows["t"] <= return_horizon_mth]                # noqa: F821
    top = int(kept.max()) if len(kept) else 0
    position = {}
    for k in range(subaccount_count()):
        position[int(subaccounts()[k])] = k
    out = np.full((n + 1, subaccount_count()), -1, dtype="int64")    # noqa: F821
    s = 0
    for _, held in rows.groupby("scenario_id"):
        s += 1
        for sa, months in held.groupby("subaccount_id")["t"]:
            if int(sa) in position:
                out[s, position[int(sa)]] = min(int(months.max()), top)
    return out


def scenario_first_mths():
    """The first month of each scenario and subaccount of *scenario_table.csv*: int64
    [scenario, sa].

    Numbered as :func:`scenario_last_mths` numbers its rows and columns: the first ``t``
    the table holds for the cell, 0 on a scenario that starts at the valuation date and
    later on one re-based to a policy issued after it.  0 where the scenario holds no row
    for the subaccount, and in row 0, padding no point is given.
    ``Projection.gross_return_mth`` refuses a month before it, naming the point, where
    ``VUL_US_S``'s ``.loc`` raised ``KeyError``, so that the padding before a cell's first
    month is never read.
    """
    n = scenario_count()
    rows = scenario_rows()
    rows = rows.assign(**{
        "subaccount_id": pd.to_numeric(rows["subaccount_id"]).astype("int64"),  # noqa: F821
        "t": pd.to_numeric(rows["t"]).astype("int64")})                         # noqa: F821
    position = {}
    for k in range(subaccount_count()):
        position[int(subaccounts()[k])] = k
    out = np.zeros((n + 1, subaccount_count()), dtype="int64")       # noqa: F821
    s = 0
    for _, held in rows.groupby("scenario_id"):
        s += 1
        for sa, months in held.groupby("subaccount_id")["t"]:
            if int(sa) in position:
                out[s, position[int(sa)]] = int(months.min())
    return out


def gross_return_array():
    """The gross monthly return of each scenario, subaccount and month: float64
    [scenario, sa, t].

    Row ``s`` and column ``i`` are numbered as :func:`scenario_last_mths` numbers them,
    and the third index is the month ``t`` from the valuation date, so that the month is
    the index, to the last ``t`` the table holds at or before ``return_horizon_mth``,
    once :func:`scenario_count` has checked the table.  NaN in row 0, before
    each cell's first month, after its last, and where a scenario holds no row for a
    subaccount, all padding, which ``Projection.gross_return_mth`` never reads: it reads a
    month past a cell's last at the last, to the horizon, refuses one before its first and
    one past the horizon, and :func:`scenario_index` refuses a point whose scenario lacks
    a subaccount.

    The months stop at ``return_horizon_mth``, 1,585 as shipped, the last month a
    compiled cache keyed by ``t`` holds (``spec_sec.py``), and no frame the contract
    allows reads past it.  So the array is no larger than the months the contract reads,
    whatever months the table holds: a cell that starts or runs past the horizon, as a
    path re-based far ahead may, adds nothing to it, where an array to the table's last
    ``t`` would grow with that month alone.  A cell that runs past the horizon is held to
    it, and :func:`scenario_last_mths` gives it that month as its last; a cell that starts
    past it holds nothing, its last month falling below its first, every month a frame
    reads being before its first, which ``Projection.gross_return_mth`` refuses as
    ``VUL_US_S``'s lookup raised there.  A month past the horizon, which only a call
    outside every frame makes, ``Projection.gross_return_mth`` refuses, naming the point
    and the scenario's number, as it refuses every month of a cell whose last falls below
    its first, so that no read meets the padding past a cell's last month.  A longer
    horizon, a higher ``omega_age`` or a lower ``issue_age_min`` needs it raised with
    ``t``'s size in ``spec_sec.py``.
    """
    n = scenario_count()
    rows = scenario_rows()
    rows = rows.assign(**{
        "subaccount_id": pd.to_numeric(rows["subaccount_id"]).astype("int64"),  # noqa: F821
        "t": pd.to_numeric(rows["t"]).astype("int64")})                         # noqa: F821
    position = {}
    for k in range(subaccount_count()):
        position[int(subaccounts()[k])] = k
    reach = return_horizon_mth                                       # noqa: F821
    kept = rows["t"][rows["t"] <= reach]
    top = int(kept.max()) if len(kept) else 0
    out = np.full((n + 1, subaccount_count(), top + 1), np.nan)      # noqa: F821
    s = 0
    for _, held in rows.groupby("scenario_id"):
        s += 1
        for sa, cell in held.groupby("subaccount_id"):
            if int(sa) in position:
                cell = cell[cell["t"] <= reach]
                out[s, position[int(sa)], cell["t"].to_numpy(dtype="int64")] = (
                    pd.to_numeric(cell["gross_return_mth"]).to_numpy(  # noqa: F821
                        dtype="float64"))
    return out


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.  An
    illustrative **[std]** stand-in for the licensed 2017 CSO ultimate ANB table.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*."""
    return pd.read_csv(input_dir() / corridor_file, index_col="age")  # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


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
    face and the number of policy years over which it runs off linearly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col="surr_charge_id")


def prem_persistency_last_year():
    """The last policy year *prem_persistency.csv* gives a factor for, the table checked.

    The ``policy_year`` column is read by value, once, as the lookup matches it, so a year
    written ``5.0`` is year 5.  A key that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on.  So are policy years
    that do not run from 1, one row a year, without a gap or a repeat: the message names
    each year that repeats or falls below 1, with its lines, and each year missing from 1
    to the last.  And so is a ``prem_persistency`` factor that is blank, text, infinite or
    below 0, naming its lines: a fraction of the planned premium, which below 0 would pay
    a negative premium, every check passing.  ``Projection.prem_persistency_py``, the
    table's one reader, takes its extent from here before it reads a factor, so a
    projection meets the checks first.
    Only the behaviour module reads the table, so a run with ``dyn_behavior_on`` off never
    asks for it.
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
    bad = (factors.index[~((factors >= 0) & (factors < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: prem_persistency must be a number, zero or more; it is "
                         f"not on line {bad}")
    return int(years.max())


def lapse_last_year():
    """The last policy year *lapse_table.csv* gives a rate for, the table checked.

    Read and checked as :func:`prem_persistency_last_year` reads and checks its own
    table, the rate checked being ``lapse_rate_ann``, which must be from 0 to 1, as a
    probability: ``Projection.lapse_rate_mth``'s ``1 - (1 - q)^(1/12)`` has no real value
    past 1, and below 0 the count would grow by its lapses.
    ``Projection.lapse_rate_base_py``, the table's one reader, takes its extent from here
    before it reads a rate.
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


def corridor_age_last():
    """The last attained age *corridor_factors.csv* gives a factor for, the table checked.

    The ``age`` column is read by value, once, so an age written ``40.0`` is 40.  A key
    that is blank, text or not a whole number is refused, naming the file, the column and
    the lines it is on, and so is a negative age, naming its lines:
    :func:`corridor_factor_array` holds the table from age 0, so that the age is the
    index, and ``VUL_US_S``, which reads the nearest row, projects such a table.  So are
    ages that do not run one row an age, without a gap or a repeat: the message names
    each age that repeats, with its lines, and each age missing between the first and the
    last.  And so is a ``corridor_factor`` that is blank, text, infinite or below 0,
    naming its lines.  ``Projection.corridor_factor_at``, the table's one reader, takes
    both of its extents, this and :func:`corridor_age_first`, before it reads a factor.
    A blank factor is a missing value to ``VUL_US_S``, whose death benefit, the ``max`` of
    the option's amount and the corridor's, then reads it as no corridor at all; and one
    below 0 is a corridor no policy has, which, once an account value runs below 0 in a
    shortfall the model does not end, takes the death benefit past the option's amount,
    every check passing.  The model point's corridor pin is held to 0 or more by the same
    rule (:func:`model_point_table`).
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
    bad = (factors.index[~((factors >= 0) & (factors < float("inf")))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: corridor_factor must be a number, zero or more; it is "
                         f"not on line {bad}")
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
    age 0, the rate checked being ``mort_rate``, which must also be from 0 to 1, as a
    probability; the
    shipped table reaches 1.0 at attained age 119.  ``Projection.mort_rate_base_at``, the
    table's one reader, takes both of its extents, this and :func:`mort_age_first`, before
    it reads a rate.  A blank rate is a missing value to ``VUL_US_S``, whose mortality is
    then not a number, and to ``Projection.mort_rate``, whose cap, ``min(q, 1.0)``, keeps it
    missing; a negative one would project negative deaths.
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
    bad = (rates.index[~((rates >= 0) & (rates <= 1))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a number from 0 to 1; it is not on "
                         f"line {bad}")
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
    order of those keys, :func:`coi_rate_last_years` the last policy year of each, and
    :func:`coi_schedule` gives each point its number.  The table's one check, which each
    of them asks first.  The two text keys may not be blank, and the two numeric keys,
    ``age_at_entry`` and ``policy_year``, are read by value, once: a key that is blank,
    text or not a whole number is refused, naming the file, the column and the lines it is
    on.  So is a cell whose policy years do not run from 1, one row a year, without a gap
    or a repeat: the message names the cell, each year that repeats or falls below 1, with
    its lines, and each year missing from 1 to the last.  And so is a ``coi_rate_guar``
    that is blank, text, infinite or below 0, naming its lines: a charge per $1,000 of net
    amount at risk, which may pass 1, as the current scale does from attained age 72, but
    is never a credit.  ``Projection.coi_rate_last_year`` reads a point's extent before
    ``Projection.coi_rate_guar_at`` reads its scale, so a projection meets the checks
    first.  A blank rate is a missing value to ``VUL_US_S``, whose account value is then
    not a number, and whose cash value and net amount at risk, each floored at zero by a
    ``max``, then read it as nothing.
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


def coi_schedule():
    """The number of each model point's guaranteed COI scale, in table order: int64
    [point].

    The point's row of :func:`coi_rate_array`: the schedules of *coi_rates.csv*, one for
    each ``sex``, ``rate_class`` and ``age_at_entry`` it holds, numbered from 1 in the
    order of those keys, as :func:`coi_rate_array` numbers its rows, whatever the order of
    the file's lines.  The point's key is its ``sex``, its ``rate_class`` and its
    ``age_at_entry``, a whole number, as ``VUL_US_S`` slices the scale.  A point whose key
    the table lacks gets schedule 0, a row of padding, and is not refused here:
    ``VUL_US_S`` projects such a point while it reads no COI rate, as one valued, or
    issued, at or past ``charges_cease_age`` never does, and
    ``Projection.coi_rate_last_year`` refuses it, naming it, when one is read.  Asks
    :func:`coi_schedules` first, which checks the table.
    """
    coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64")})  # noqa: F821
    number = {}
    for key, _ in rates.groupby(["sex", "rate_class", "age_at_entry"], sort=True):
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
    numbered as :func:`coi_schedule` numbers it, in the sorted order of its keys, whatever
    the order of the file's lines, read by value once :func:`coi_schedules` has checked
    the table: 77 on the shipped anchor cell, whose scale runs to attained age 121.  0 in
    element 0, schedule 0, which a point the table has no scale for is given, and which
    ``Projection.coi_rate_last_year`` refuses where it is read.  A vector by schedule,
    read at the point's :func:`coi_schedule`, rather than ``UL_US_SEC``'s by point.
    """
    n = coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64"),  # noqa: F821
        "policy_year": pd.to_numeric(rates["policy_year"]).astype("int64")})   # noqa: F821
    out = np.zeros(n + 1, dtype="int64")                             # noqa: F821
    s = 0
    for _, rows in rates.groupby(["sex", "rate_class", "age_at_entry"], sort=True):
        s += 1
        out[s] = int(rows["policy_year"].max())
    return out


def coi_rate_array():
    """The guaranteed maximum monthly COI rates by schedule and policy year: float64
    [schedule, y].

    Row ``s`` is schedule ``s`` of *coi_rates.csv*, numbered from 1 in the order of its
    keys, ``sex``, ``rate_class`` and ``age_at_entry``, as :func:`coi_schedule` numbers
    it, sorted, whatever the order of the file's lines, and column ``y`` is policy year
    ``y``, so that the year is the index: one more column than the table's last policy
    year, one more row than its schedules.  Per $1,000 of net amount at risk.  NaN in
    row 0, schedule 0, which no point the table holds is given, in column 0, before any
    policy year, and past each schedule's last year, all padding, which
    ``Projection.coi_rate_guar_at`` never reads: it refuses a year below 1 and a point of
    schedule 0, and reads a later year at the schedule's last.  Asks
    :func:`coi_schedules` first, which checks the table.
    """
    n = coi_schedules()
    rates = coi_rates().reset_index()
    rates = rates.assign(**{
        "age_at_entry": pd.to_numeric(rates["age_at_entry"]).astype("int64"),  # noqa: F821
        "policy_year": pd.to_numeric(rates["policy_year"]).astype("int64")})   # noqa: F821
    out = np.full((n + 1, int(rates["policy_year"].max()) + 1), np.nan)  # noqa: F821
    s = 0
    for _, rows in rates.groupby(["sex", "rate_class", "age_at_entry"], sort=True):
        s += 1
        years = rows["policy_year"].to_numpy(dtype="int64")
        out[s, years] = pd.to_numeric(                               # noqa: F821
            rows["coi_rate_guar"]).to_numpy(dtype="float64")
    return out


def class_count():
    """The number of classes *class_factor_table.csv* gives a factor for, the table checked.

    A ``rate_class`` that is blank is refused, naming the file and the lines it is on, and
    so is one on more than one row, naming each such class with its lines; and so is a
    ``factor`` that is blank, text, infinite or below 0, naming its lines: a multiple of the
    base mortality, which below 0 would project negative deaths.
    ``Projection.class_factor``, the table's one reader, asks for the count before it reads
    a factor, so a projection meets the checks first.  A blank factor is a missing value to
    ``VUL_US_S``, whose mortality is then not a number, and to ``Projection.mort_rate``,
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
    charge by the run-off and counts policy years on it, where ``VUL_US_S`` truncates a
    fraction with ``int()`` and divides by zero at 0.  ``Projection.surr_charge_rate_max``
    and ``Projection.surr_charge_runoff_years``, the table's two readers, ask for the count
    before they read a value, so a projection meets the checks first.  A blank charge is a
    missing value to ``VUL_US_S``, whose surrender charge rate, the ``max`` of 0 and the
    charge left, is then 0 in every policy year, as though the schedule had run off.  A
    charge below 0 leaves a charge below 0 through the schedule's years, which the ``max``
    reads as none, and after them, where the share of the run-off left turns negative, a
    charge above 0 that rises each policy year, every check passing: the shipped schedule
    written at -18.00 charges $1.29 per $1,000 in policy year 16.
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
    age, 18 as shipped, which ``Projection.corridor_factor_at`` never reads: it reads an
    age outside the table at the nearest row, as ``VUL_US_S`` does, so an issue age below
    18 reads age 18's factor.
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

    The ``age_at_entry`` column, which :func:`model_point_table` holds to a whole number,
    0 or more and below ``2**53``, where the int64 holds it exactly.
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


def alloc_fixed():
    """The share of each net premium allocated to the fixed option: float64 [point].

    The ``alloc_fixed`` column, which :func:`model_point_table` holds to a number from 0
    to 1.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["alloc_fixed"]).to_numpy(dtype="float64")


def alloc():
    """The share of each net premium allocated to each subaccount: float64 [point, sa].

    Element ``[p, i]`` is point ``p``'s ``alloc_<id>`` column, ``id`` the id of the
    subaccount at position ``i`` of the lineup, :func:`subaccounts`, read by element, so
    that the position is the index.  :func:`model_point_table` holds each such column to a
    number from 0 to 1, and asks :func:`subaccount_count` first, which checks the lineup.
    """
    n = subaccount_count()
    table = model_point_table()
    out = np.zeros((len(table), n), dtype="float64")                 # noqa: F821
    for k in range(n):
        out[:, k] = pd.to_numeric(                                   # noqa: F821
            table[f"alloc_{int(subaccounts()[k])}"]).to_numpy(dtype="float64")
    return out


def sa_pp_init():
    """The value of each subaccount per policy entering month 0: float64 [point, sa].

    Element ``[p, i]`` is point ``p``'s ``sa_pp_init_<id>`` column, read as :func:`alloc`
    reads ``alloc_<id>``.  :func:`model_point_table` holds each such column to a number,
    zero or more, and to 0 on a policy not yet in force.
    """
    n = subaccount_count()
    table = model_point_table()
    out = np.zeros((len(table), n), dtype="float64")                 # noqa: F821
    for k in range(n):
        out[:, k] = pd.to_numeric(                                   # noqa: F821
            table[f"sa_pp_init_{int(subaccounts()[k])}"]).to_numpy(dtype="float64")
    return out


def fa_pp_init():
    """The fixed-option value per policy entering month 0: float64 [point].

    The ``fa_pp_init`` column of the opening state, checked by :func:`model_point_table`.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["fa_pp_init"]).to_numpy(dtype="float64")


def la_pp_init():
    """The loan-account collateral per policy entering month 0: float64 [point].

    The ``la_pp_init`` column of the opening state, checked by :func:`model_point_table`.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["la_pp_init"]).to_numpy(dtype="float64")


def loan_bal_init():
    """The policy debt per policy entering month 0: float64 [point].

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


def has_surr_charge():
    """Whether a surrender charge schedule applies to each model point: int64 [point].

    1 where the ``has_surr_charge`` column reads True, in any case, and 0 where it reads
    False: :func:`model_point_table` refuses any other value.
    """
    flags = model_point_table()["has_surr_charge"].astype(str).str.lower()
    return (flags == "true").to_numpy(dtype="int64")


def is_db_option_a():
    """Whether each model point's death benefit is Option A: int64 [point].

    1 where ``db_option`` is ``"A"``, compared element by element as ``VUL_US_S``
    compares it, and 0 elsewhere.  A value neither A nor B is not refused here: it is no
    flag, and ``Projection.db_pp`` raises ``VUL_US_S``'s message on it.
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
    ``Projection.corridor_factor`` raises ``VUL_US_S``'s message.
    """
    return (model_point_table()["qual_test"] == "GPT").to_numpy(dtype="int64")


def is_level_premium():
    """Whether each model point's premium pattern is LEVEL: int64 [point].

    1 where ``premium_type`` is ``"LEVEL"``, and 0 elsewhere.  A pattern neither LEVEL
    nor SINGLE is no flag, and ``Projection.premium_pp`` raises ``VUL_US_S``'s message on
    it.
    """
    return (model_point_table()["premium_type"] == "LEVEL").to_numpy(dtype="int64")


def is_single_premium():
    """Whether each model point's premium pattern is SINGLE: int64 [point].

    1 where ``premium_type`` is ``"SINGLE"``, as :func:`is_level_premium` decodes LEVEL.
    """
    return (model_point_table()["premium_type"] == "SINGLE").to_numpy(dtype="int64")


def corridor_override_m1():
    """Each model point's first-month corridor factor pin: float64 [point].

    The ``corridor_override_m1`` column, which :func:`model_point_table` holds to blank or
    a number, zero or more: the number, and NaN where it is blank, as
    ``Projection.corridor_override_m1`` read it at stage ``E``.  The flag
    :func:`has_corridor_override_m1`, never this value, says whether a point pins its
    factor, so no NaN reaches a formula.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["corridor_override_m1"]).to_numpy(dtype="float64")


def has_corridor_override_m1():
    """Whether each model point pins its corridor factor: int64 [point].

    1 where the ``corridor_override_m1`` column holds a number and 0 where it is blank:
    the decode ``Projection.has_corridor_override_m1`` made with ``pd.isna`` at stage
    ``E``, made here once for every point.
    """
    return model_point_table()["corridor_override_m1"].notna().to_numpy(dtype="int64")


def coi_rate_override_m1():
    """Each model point's first-month current COI rate pin: float64 [point].

    The ``coi_rate_override_m1`` column, held and read as :func:`corridor_override_m1`
    is: NaN where blank, and the flag :func:`has_coi_rate_override_m1` decides.
    """
    return pd.to_numeric(                                            # noqa: F821
        model_point_table()["coi_rate_override_m1"]).to_numpy(dtype="float64")


def has_coi_rate_override_m1():
    """Whether each model point pins its current COI rate: int64 [point].

    1 where the ``coi_rate_override_m1`` column holds a number and 0 where it is blank,
    as :func:`has_corridor_override_m1` decodes its own.
    """
    return model_point_table()["coi_rate_override_m1"].notna().to_numpy(dtype="int64")


def class_factor():
    """The underwriting-class factor of each model point: float64 [point].

    The ``factor`` *class_factor_table.csv* gives the point's ``rate_class``, joined
    exactly, once :func:`class_count` has checked the table.  A point reads its class
    factor in every month on the books, so ``VUL_US_S`` fails every projection of a point
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
    every point whose id the table holds, with a charge or without, as ``VUL_US_SEC``'s
    accessor read it at stage ``E``: a point without a charge reads its schedule, though
    no cell reads it there.  On a point without a charge whose id the table lacks, blank
    included, it is NaN, and :func:`has_surr_charge_schedule` 0: the point projects, and
    ``Projection.surr_charge_rate_max`` raises ``KeyError`` on it, as the ``.loc`` did at
    stage ``E``.  The join refuses, naming every such point with a charge, and only on a
    point with one, since ``VUL_US_S`` reads the schedule in every month of such a point's
    cover: an id the table lacks, where ``VUL_US_S``'s ``.loc`` raised ``KeyError``; and a
    ``runoff_years`` of ``2**53`` years or more in size, the bound of every number read as
    an int, past which the compiled ``int()`` in ``Projection.lapse_shock_month`` would
    raise ``OverflowError`` in time.  A run-off that is not a whole number of years, 1 or
    more, :func:`surr_charge_count` has refused already.  The same checks run in
    :func:`surr_charge_runoff_years`, the join's other vector, so that whichever a
    projection reads first refuses the point.
    """
    surr_charge_count()
    table = model_point_table()
    schedules = surr_charge_table()
    charges = pd.to_numeric(schedules["sc_per_1000_init"])           # noqa: F821
    years = pd.to_numeric(schedules["runoff_years"])                 # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing, huge = [], []
    for i in range(len(ids)):
        if ids[i] not in charges.index:
            if flags[i]:
                missing.append(i)
        elif flags[i] and not abs(years[ids[i]]) < 2.0 ** 53:
            huge.append(i)
        else:
            out[i] = float(charges[ids[i]])
    missing, huge = table.index[missing].tolist(), table.index[huge].tolist()
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
    with its refusals.  A point without a charge reads the run-off as written, ``2**53``
    years or more included, which no cell reads there.
    """
    surr_charge_count()
    table = model_point_table()
    years = pd.to_numeric(surr_charge_table()["runoff_years"])       # noqa: F821
    flags = (table["has_surr_charge"].astype(str).str.lower() == "true").tolist()
    ids = table["surr_charge_id"].tolist()
    out = np.full(len(ids), np.nan, dtype="float64")                 # noqa: F821
    missing, huge = [], []
    for i in range(len(ids)):
        if ids[i] not in years.index:
            if flags[i]:
                missing.append(i)
        elif flags[i] and not abs(years[ids[i]]) < 2.0 ** 53:
            huge.append(i)
        else:
            out[i] = float(years[ids[i]])
    missing, huge = table.index[missing].tolist(), table.index[huge].tolist()
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
    exactly, as ``VUL_US_S``'s ``.loc`` compares it, and 0 where it is not, blank
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


def scenario_index():
    """The number of each model point's return scenario, in table order: int64 [point].

    The point's row of :func:`gross_return_array`, :func:`scenario_first_mths` and
    :func:`scenario_last_mths`: the scenarios of *scenario_table.csv*, numbered from 1 in
    the order of their ``scenario_id``, as ``groupby`` sorts them, whatever the order of
    the file's lines, and each point given the number of its own ``scenario_id``, matched
    as pandas matches the two columns, so that a scenario written ``1`` in one file
    matches ``1.0`` in the other.  Every projection reads every subaccount's return in its
    first month in cover, so ``VUL_US_S`` fails every projection of a point whose scenario
    the table lacks, or holds no row for a subaccount of the lineup: such a point is
    refused here, at the first read, naming every such point.  Asks :func:`scenario_count`
    first, which checks the table.
    """
    scenario_count()
    rows = scenario_rows()
    held_ids = pd.to_numeric(rows["subaccount_id"]).astype("int64")  # noqa: F821
    rows = rows.assign(**{"subaccount_id": held_ids})
    lineup = set()
    for k in range(subaccount_count()):
        lineup.add(int(subaccounts()[k]))
    number, s = {}, 0
    for key, held in rows.groupby("scenario_id"):
        s += 1
        number[key] = s if lineup <= set(held["subaccount_id"].tolist()) else 0
    table = model_point_table()
    ids = table["scenario_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    at = []
    for i in range(len(ids)):
        out[i] = number.get(ids[i], 0)
        if not out[i]:
            at.append(i)
    bad = table.index[at].tolist()
    if bad:
        raise ValueError(f"{scenario_file} has no returns for every subaccount of the "
                         f"lineup on the scenario_id of point_id {bad}")  # noqa: F821
    return out


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

subaccount_file = "subaccount_table.csv"

scenario_file = "scenario_table.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

prem_persistency_file = "prem_persistency.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

return_horizon_mth = 1585

pd = ("Module", "pandas")

np = ("Module", "numpy")
