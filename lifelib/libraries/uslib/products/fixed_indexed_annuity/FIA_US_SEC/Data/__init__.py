# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.FIA_US_SEC.Projection` as ``data``. :mod:`~.FIA_US_SEC.Projection` is
parameterized by ``idx``, a point's position in the table, so each ``Projection[i]`` is a
separate ItemSpace with its own cells cache; if the readers lived there, every model point
would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/fixed_indexed_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FIA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Five of the tables are FIA_US_S's.** The mortality table, the surrender charge and
vesting schedule, the rollup schedules, the lifetime withdrawal percentage bands and the
withdrawal programmes are the files :mod:`~.FIA_US_S` reads, read here in place: one copy
of each table serves both models, so an edit to one reaches both. The other two are this
model's own, each generated from :mod:`~.FIA_US_S` and its inputs, never typed:
``model_point_table_sec.csv``, beside ``FIA_US_S``'s ``model_point_table.csv``, and
``rate_scenario_sec.csv``, the rate scenarios moved onto the valuation clock, beside
``FIA_US_S``'s ``rate_scenario.csv``. This model opens neither of ``FIA_US_S``'s two.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table_sec.csv
mort_table_file            mort_table()                    mort_table.csv
surr_charge_file           surr_charge_table()             surr_charge_table.csv
rollup_file                rollup_table()                  rollup_table.csv
payout_rate_file           payout_rate_table()             payout_rate_table.csv
rate_scenario_file         rate_scenario()                 rate_scenario_sec.csv
withdrawal_file            withdrawal_table()              withdrawal_table.csv
=========================  ==============================  ==========================

**The model point table is checked as it is read.** Fourteen of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the twelve columns of an in-force contract's opening
state. :func:`model_point_table` refuses a table that lacks any of them, repeats a
``point_id``, holds a count, a duration, an age or a contract parameter no contract can
have, holds an opening state no contract can be in, or holds a key that the table it joins
lacks: a scenario that sets no level by the point's first month on the books, a rollup
schedule, a withdrawal programme, or a sex and an attained age the mortality table gives
no rate at. The checks run in turn, and the first that fails raises, naming the missing
column or every point that fails it. It also refuses a contract to be issued more than
``future_horizon_mth`` months after the valuation date, 120 months as shipped: future
new business is written over a stated horizon, so that no frame runs longer than cover
from issue plus that horizon. Set to 0, the Reference refuses future new business
altogether. Whether a point is still in cover at the valuation date is a rule of the
product rather than of the table, and ``Projection.proj_len`` checks it.

**So are the keys and values of the six assumption tables.** Each reader above is
``FIA_US_S``'s, unchanged, and beside it a cell reads the table's keys by value, once,
checks them and its values, and returns the table indexed by the checked keys. Every
array the projection reads is built from that checked table, and takes the table's
extents from the same checked keys, as int cells:

=========================  ================================  ===========================
FIA_US_S's reader          Checked cell                      Its extents
=========================  ================================  ===========================
mort_table()               mort_rates()
surr_charge_table()        surr_charge_scale()               surr_charge_last_year()
rollup_table()             rollup_steps()
payout_rate_table()        payout_rates()                    payout_rate_first_age(),
                                                             payout_rate_last_age()
rate_scenario()            rate_scenario_steps()
withdrawal_table()         wd_schedules()
=========================  ================================  ===========================

A key that is not a whole number, text and a blank among them, is refused, naming the
file, the column and the lines it is on, and so are a blank text key, a value that is not
a number in its range, blank, text and infinite values among them, a repeated key, and,
where the projection reads every year or age between a table's first and last, keys that
do not run one row a year or an age: the message names each repeated key with its lines
and each key or span of keys missing. A key written as a float, ``1.0``, is the whole
number it holds, as ``FIA_US_S``'s lookups match it. Those lookups take the keys as
pandas reads them: one key written as text turns its whole column to text, so that every
withdrawal is then zero without a word, and every other lookup on the column raises
Python's own ``TypeError``, ``KeyError`` or ``ValueError``, naming no file. And every
value a cap, a ``min`` or a ``max`` reads is refused blank, as text or infinite, because
``min`` and ``max`` lose a NaN in a later argument without a word. A key is also refused
unless it is below ``2**53`` in size, so that the int64 it is cast to holds it
(*The vectors*, below).

Two tables are read as **step functions**, so a schedule is a handful of rows rather than
one row per contract year or month. ``rollup_table`` is indexed by
``(rollup_id, contract_year)`` and each row states the guaranteed simple rollup rate that
holds from its own contract year until the next row of the same schedule, which turns the
blended 5.00%/2.00%/0% [S2] and the flat 3.00%/0% [S9] designs into three rows and two.
``rate_scenario`` is indexed by ``(scenario_id, t)`` and carries the index level ``I`` and
the MVA reference yield ``i_t``; there ``t`` is a **valuation** month, 0 at the valuation
date, and each row holds from its month until the next row of the same scenario. The
projection reads the level at each anniversary of the contract, at the valuation month
that anniversary falls in, and differences consecutive anniversaries' levels into
``R = I(y+1)/I(y) - 1``, the return over the contract year, so holding a level flat is
how a scenario says "no index credit this year". ``FIA_US_S`` keys the same levels by
anniversary number from issue, so on the valuation clock a contract needs them where its
own anniversaries fall: the file holds ``FIA_US_S``'s scenarios at ``t = 12 x``
anniversary, for the contracts issued at the valuation date, and a copy of a contract's
scenario re-based to its month for every row valued in force or issued later, under an id
of its own, ``{id}-M{d}`` or ``{id}-F{k}``. ``withdrawal_table`` is indexed by
``(wd_schedule_id, t)``, there an **elapsed contract year** count, on the policy clock,
rather than a month, and is *not* a step function — a contract year with no row simply
takes no ad hoc withdrawal.

``surr_charge_table`` carries **two** contract-year vectors in one file, the surrender
charge percentage and the bonus vesting percentage, because [S5] supplies them as a
single schedule pair and both are read at the same key. ``payout_rate_table`` is banded
rather than keyed: each row gives an inclusive attained-age band and the single-life and
joint-life percentages, the joint column being the single column less 0.50% [S1][S3].
:func:`payout_rates` expands the bands to one row an age, so that the projection reads
the percentage at the exercise age directly.

To swap in the prescribed annuitant mortality — the 2012 IAM/IAR family with Projection
Scale G2 [REG-R59][REG-R60], which may not be redistributed here — replace
``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a different
name, before the model computes anything. No formula changes. The shipped table is the
same illustrative Makeham annuitant curve as ``products/fixed_deferred_annuity``, so the
two annuity models sit on one mortality basis. Replacing a file changes
:mod:`~.FIA_US_S` too, which reads the same ones. A compiled model clears no cache, so
there the name is set on a package just imported, before anything is read.

**The vectors.** The readers and the checked tables return what the files hold, and no
:mod:`~.FIA_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them.
The others read the arrays below instead, one element at a time, a model point's
attribute being the element at its position, ``data.premium()[idx]``. That is what lets
the model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy vector
or table of int64 or float64, which compiles to a typed memoryview, never one of bools,
objects or text, and each count and extent is an int.

Text the projection needs is decoded here, into the number it selects: each value of the
two categorical columns ``FIA_US_S`` branches on, ``glwb_basis`` and ``credit_method``,
into a 0/1 flag, the ``is_*`` cells, the rider election into another, and a blank
``joint_age`` into the issue age. Each table keyed by more than a number becomes an
integer-indexed array: the mortality table, the rollup schedules, the scenarios and the
withdrawal programmes are numbered, each point carrying the number of its own,
``mort_schedule``, ``rollup_number``, ``scenario_number`` and ``wd_schedule_number``, all
four numbered from 1 in the sorted order of their keys; the mortality is held by
attained age, the surrender charge, the vesting and the rollups by contract year, the
payout bands by exercise age, the scenarios step-filled by valuation month and the
programmes by elapsed contract year, so that the age, the year or the month is the index:

=====================================  =======  ==================  =======================
Cells                                  dtype    Shape               From
=====================================  =======  ==================  =======================
point_id()                             int64    [point]             the table's index
age_at_entry(), income_start_age()     int64    [point]             the two columns
joint_age()                            int64    [point]             ``joint_age``, blank
                                                                    the issue age
duration_mth()                         int64    [point]             ``duration_mth``
phase_prev_anniv_init()                int64    [point]             the phase code
glwb_elected()                         int64    [point]             the checked flag
premium() .. mva_ref_yield_at_issue()  float64  [point]             ``premium``,
                                                                    ``policy_count`` and
                                                                    seven more
av_pp_init() and ten more              float64  [point]             the eleven float
                                                                    columns of the opening
                                                                    state
is_single_basis() and six more         int64    [point]             the seven decodes,
                                                                    1 on the value
mort_schedule_count()                  int      scalar              *mort_table.csv*
mort_schedule()                        int64    [point]             ``sex``, joined
mort_age_firsts(), mort_age_lasts()    int64    [schedule]          each sex's ages
mort_age_base(), mort_age_held()       int      scalar              the array's first and
                                                                    last ages
mort_table_array()                     float64  [schedule, age]     *mort_table.csv*
surr_charge_rate_array(),              float64  [year]              *surr_charge_table.csv*
vest_rate_array()
rollup_count()                         int      scalar              *rollup_table.csv*
rollup_number()                        int64    [point]             ``rollup_id``, joined
rollup_last_year()                     int      scalar              ``read_last_mth``'s
                                                                    year
rollup_rate_array()                    float64  [schedule, year]    step-filled, 0.0 before
                                                                    the first row
payout_rate_held_age()                 int      scalar              ``read_last_age``
payout_rate_array()                    float64  [age, basis]        *payout_rate_table.csv*
scenario_count()                       int      scalar              the companion
scenario_number()                      int64    [point]             ``scenario_id``, joined
scenario_first_mths()                  int64    [scenario]          each first ``t``
scenario_last_mth()                    int      scalar              ``read_last_mth``
index_level_array(),                   float64  [scenario, t]       step-filled
mva_ref_yield_array()
wd_schedule_count()                    int      scalar              *withdrawal_table.csv*
wd_schedule_number()                   int64    [point]             ``wd_schedule_id``,
                                                                    joined
wd_last_year()                         int      scalar              ``read_last_mth``'s
                                                                    count
wd_amount_array()                      float64  [programme, count]  ``wd_amount``, 0.0
                                                                    without a row
=====================================  =======  ==================  =======================

The table checks are what they were, :func:`model_point_table` and the six checked
tables, beside their int extents. No copy of the numeric columns is read beside the table,
as ``MYGA_US_SEC`` reads one: :func:`model_point_table` refuses every numeric column the
projection reads, by column and point, where it is blank, text or out of range, so each
vector is the checked column, read as ``FIA_US_S``'s ``float()`` or ``int()`` reads it.

**Every array is held to the last age or month a read reaches.** Two References say
where: ``read_last_mth``, 1,093, the last element of ``Projection``'s ``t`` cache,
``12 x (maturity_age - issue_age_min + 1) + future_horizon_mth + 1``, and
``read_last_age``, 122, the last element of its ``a`` cache, ``maturity_age + 2``, both
derived in ``spec_sec.py``, since ``Data`` cannot read ``Projection``'s References; a test
holds each to the spec. The scenarios are held by valuation month to ``read_last_mth``,
the rollups by contract year to the year a month to it falls in, and the programmes by
the count to the count it falls in, a schedule's last row holding to the end, as
``FIA_US_S``'s step function holds it; the mortality and the payout bands are held by age
to ``read_last_age``, the last band holding to the end. So a key far past any read, which
``FIA_US_S`` holds and never reaches, neither widens an array nor refuses a point
``FIA_US_S`` projects, and a read past an array, which no projection makes, is refused by
its reader in :mod:`~.FIA_US_SEC.Projection`, naming the point, rather than clamped. The
payout array is indexed from the first band's age, however low, and the mortality from
the table's first age, or from 0 where that is below 0, since no attained age is: so no
age a table holds is refused, a negative one among them, which ``FIA_US_S`` projects
beside, and none widens an array. A change to ``maturity_age``, ``issue_age_min`` or
``future_horizon_mth`` needs both References recomputed with the spec.

**An array is read by element, never whole,** in this Space as in
:mod:`~.FIA_US_SEC.Projection`. The compiler types an array cell as a memoryview only once
it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python
object. So an array derived here from another reads the table's column, or the other
cell element by element, and a width comes from a table or a count cell, never from
another cell's array. Each table's check is one cell that every array, extent and number
of the table reads first, so that a projection, which reads an extent or a number first,
meets the same refusal as a reader of the array. A keyword named as a cell of this
Space would be rewritten by the export, so none is passed, and a local of a formula is
named apart from the cells.

**What cannot be decoded is refused,** when the vector is first read, naming every point
at fault, where it is not ``FIA_US_S``'s reading: a ``point_id`` that is not a whole
number. A decode compares the text exactly, element by element, as ``FIA_US_S`` compares
it, so a value written in another case or with a space, ``Cap``, or ``cap`` with a leading
space, is no flag, and the projection answers as ``FIA_US_S`` answers it, raising
``invalid credit_method`` where it raises it. A table without ``glwb_basis`` or
``credit_method`` raises pandas' ``KeyError`` at the decode's first read, as
``FIA_US_S`` raises it where a point first reads the column; a point without the rider
never reads the basis, and projects. A join number maps the point's key as
``FIA_US_S``'s ``.loc`` matches it, by the value pandas read, and
:func:`model_point_table` has refused a key its table lacks. A read beyond a table's
extent is refused where ``FIA_US_S``'s lookup raised, by the one
:mod:`~.FIA_US_SEC.Projection` cell that reads the table, naming the point: an attained
age outside the sex's in ``mort_rate_base_at``, a contract year below 1 in
``surr_charge_rate_py`` and ``vest_rate_py``, and a month before the scenario's first in
``scenario_value``, each a ``ValueError`` where ``FIA_US_S`` raised ``KeyError`` or its
own message. A year before a rollup schedule's first row, and a count a programme has no
row at, are no rollup and no withdrawal, as there.

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is first refused unless it is
below ``2**53`` in size, where the int64 holds ``FIA_US_S``'s reading of it:
``duration_mth``, the issue age, ``income_start_age`` and ``joint_age``
(:func:`model_point_table`), the ``point_id`` (:func:`point_id`), and each assumption
table's key, refused by the table's check, naming the file, the column and the lines: an
age, a band's bound, a contract year, a month or a count. Each is a whole number already,
so no fraction truncates. ``FIA_US_S`` projects a point whose ``income_start_age`` or
``joint_age`` is ``1e20``, so the first is a refusal it lacks.
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

    Inputs are *external* files, not data stored inside the model, so the model folder
    is pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table_sec.csv* and checked.

    Indexed by ``point_id``. Fourteen columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``, and the twelve columns of the opening state, per contract.
    Entering month 0, before any month-0 event:

    * ``av_pp_init`` and ``av_fixed_pp_init``: the account value and the fixed account
      within it;
    * ``benefit_base_pp_init``, ``rollup_base_pp_init`` and ``lw_pp_init``: the benefit
      base, the rollup base and the lifetime withdrawal, each flat between anniversaries;
    * ``mgsv_pp_init``: the Model #805 floor;
    * ``wd_cum_pp_init``: the gross withdrawals taken from issue to the valuation date.

    At the anniversary on or before the valuation date, the one that opened the contract
    year under way:

    * ``av_pp_prev_anniv_init`` and ``av_fixed_pp_prev_anniv_init``: the account value and
      the fixed account, the year's index-credit, fixed-interest and free-withdrawal bases;
    * ``phase_prev_anniv_init``: the phase, as a code, 1 ``ACCUM``, 2 ``INCOME`` or 3
      ``DEPLETED``, and 0 on a contract not yet in force;
    * ``payout_rate_locked_prev_anniv_init``: the lifetime withdrawal percentage locked at
      the first exercise, 0 before it;
    * ``index_level_prev_anniv_init``: the index level, where the year's index segment
      started.

    Seven are ``FIA_US_S``'s columns renamed: ``av_initial``, ``bb_initial``,
    ``rb_initial``, ``mgv_initial`` and ``lw_initial`` become the ``_init`` of the cell
    each opens, ``phase_initial``, text in ``FIA_US_S``, becomes the code, and
    ``payout_rate_initial`` the locked rate. The rest are ``FIA_US_S``'s, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the generator
    took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the fourteen in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a contract in force, 0
      for one issued at the valuation date, negative for one issued later;
    * ``age_at_entry`` and ``income_start_age`` are whole numbers of years, and
      ``joint_age`` is blank or a whole number of years, 0 or more. ``FIA_US_S`` reads each
      by ``int()``, which would truncate a fraction without a word;
    * ``duration_mth``, ``age_at_entry``, ``income_start_age`` and ``joint_age``, where
      given, are each below ``2**53`` in size, so that the int64 vector each is read into
      (:func:`duration_mth` and its neighbours) holds ``FIA_US_S``'s reading of it: past
      int64 a float casts to the least int64 without a word. ``FIA_US_S`` projects a point
      whose ``income_start_age`` or ``joint_age`` is ``1e20``, so this is a refusal it
      lacks;
    * no contract is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * ``glwb_elected`` is True or False, read by value: one cell written as text turns the
      column to text as pandas reads it, every flag with it, so ``"True"`` and ``"False"``
      are read as the flags they name, and the table is returned holding bools, where
      ``FIA_US_S``'s ``bool()`` would read ``"False"`` as elected;
    * the premium, the bonus rate, the utilization, the cap, the stacking factor and the
      share of the index credit reaching the account value are each a finite number, zero
      or more; ``alloc_indexed`` is a number from 0 to 1; and ``mva_ref_yield_at_issue`` is
      a finite number above -1, the base of the MVA's power;
    * the nine money columns of the opening state are each a finite number, zero or more;
      the locked payout percentage is a number from 0 to 1; the index level is a finite
      number, zero or more; and the phase is a whole number;
    * a contract not yet in force, ``duration_mth`` 0 or less, has no opening state: every
      state column is 0, the phase code included;
    * a contract in force, ``duration_mth`` 1 or more, is in phase 1, 2 or 3:
      ``TERMINATED`` is a deemed surrender of every contract, so none is in force in it;
    * its index level is above 0, since the year's index return divides by it;
    * it is in ``INCOME`` or ``DEPLETED`` only under the rider, and without the rider its
      benefit base, rollup base, lifetime withdrawal and locked percentage are all 0;
    * under the rider its benefit base is above 0: an anniversary that takes the base to 0
      terminates the contract;
    * in ``ACCUM`` its lifetime withdrawal and locked percentage are 0, before the first
      lifetime withdrawal, and in ``INCOME`` or ``DEPLETED`` its lifetime withdrawal is 0
      exactly where its locked percentage is: the withdrawal is the locked percentage of a
      benefit base above 0, and a reduction that took it to 0 would have taken the base to
      0 too. A percentage of 0 is locked where the contract exercises below the first age
      band, as it can where ``Projection.min_income_age`` is below the band's first age,
      both 50 as shipped, or in a band at 0%, which :func:`payout_rates` accepts. The
      withdrawal is then 0 for life, in ``INCOME`` and, once the account value is
      exhausted, in ``DEPLETED``, so ``INCOME`` or ``DEPLETED`` with both 0 is read;
    * in ``DEPLETED`` its account value and fixed account, entering month 0 and at the
      anniversary, are all 0, and in ``ACCUM`` or ``INCOME`` its account value at the
      anniversary is above 0: the anniversary that exhausts the account value leaves both;
    * the fixed account is part of the account value, at each instant, to a cent;
    * in the first policy year, ``duration_mth`` 1 to 11, the year opened at issue, so the
      values at the anniversary are the issue values, to a cent: the account value
      ``premium x (1 + bonus_rate)``, the fixed account ``(1 - alloc_indexed)`` of it, the
      benefit and rollup bases the premium under the rider and 0 without it; the
      withdrawals to date are 0; and the phase is ``ACCUM``;
    * on a point valued on a policy anniversary, ``duration_mth`` a multiple of 12, the
      account value and the fixed account at the anniversary equal those entering month 0,
      exactly: the two are one instant;
    * off an anniversary, the indexed account, ``av_pp_init - av_fixed_pp_init``, equals
      its value at the anniversary to three cents, since it moves only at an anniversary,
      and the fixed account has not fallen below its value at the anniversary by more than a
      cent, since between anniversaries it only accrues;
    * last, each point's keys into the tables it is joined with: its ``scenario_id`` is a
      scenario of :func:`rate_scenario_steps` that sets its levels by the first month the
      point is on the books, ``t = 0`` or its issue month if later; on a point valued on an
      anniversary, the index level at the anniversary is the one its scenario sets at
      ``t = 0``, exactly, since the model reads the scenario there and not the column; its
      ``rollup_id`` is a schedule of :func:`rollup_steps`; its ``wd_schedule_id`` is a
      programme of :func:`wd_schedules`; and :func:`mort_rates` gives a rate at its ``sex``
      and its attained age in that first month. So reading the table reads those four
      tables, checked.

    Amounts of money are compared to a cent, so that an extract may carry each to the cent,
    as an administration system holds it: each amount so carried is within half a cent of
    its exact value. The indexed account is compared to three cents, being the difference
    of two such amounts at each of two instants. Two columns that hold one amount at
    instants that coincide, on an anniversary, are compared exactly.

    Accepted, because a contract can be in each state: an account value of 0 in
    ``DEPLETED``, where the rider pays on; a lifetime withdrawal and a locked percentage of
    0 in ``INCOME`` or ``DEPLETED``, where the contract exercised below the first age band
    or in a band at 0%; a blank ``joint_age`` on the joint basis, which reads the
    annuitant's own age; and a ``duration_mth``, an age or a phase code written as a float,
    read as the whole number it holds.

    Left to the projection, because it needs ``maturity_age``, a ``Projection`` Reference,
    which ``Data`` cannot read: whether a point is still in cover, which
    ``Projection.proj_len`` checks, naming the point. On the shipped tables the mortality
    check refuses an attained age past 120 first, the table's last age. The index level at
    an anniversary before the valuation date is history, which nothing here can check beyond
    its being above 0.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    money = ("av_pp_init", "av_fixed_pp_init", "av_pp_prev_anniv_init",
             "av_fixed_pp_prev_anniv_init", "benefit_base_pp_init",
             "rollup_base_pp_init", "mgsv_pp_init", "lw_pp_init", "wd_cum_pp_init")
    state = (*money, "payout_rate_locked_prev_anniv_init", "phase_prev_anniv_init",
             "index_level_prev_anniv_init")
    for column in ("policy_count", "duration_mth", *state):
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
    for column in ("age_at_entry", "income_start_age"):
        years = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~(years % 1 == 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number of years; it is "
                             f"not at point_id {bad}")
    joint = pd.to_numeric(table["joint_age"], errors="coerce")       # noqa: F821
    bad = table.index[(table["joint_age"].notna() & ~((joint % 1 == 0) & (joint >= 0)))
                      ].tolist()
    if bad:
        raise ValueError(f"{name}: joint_age must be blank or a whole number of years, 0 "
                         f"or more; it is not at point_id {bad}")
    for column in ("duration_mth", "age_at_entry", "income_start_age", "joint_age"):
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[table[column].notna() & ~(v.abs() < 2.0 ** 53)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be below 2**53 in size; it is not at "
                             f"point_id {bad}")
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
    elected = table["glwb_elected"].map({True: True, False: False,
                                         "True": True, "False": False})
    bad = table.index[elected.isna()].tolist()
    if bad:
        raise ValueError(f"{name}: glwb_elected must be True or False; it is not at "
                         f"point_id {bad}")
    elected = elected.astype(bool)
    table = table.assign(**{"glwb_elected": elected})
    for column in ("premium", "bonus_rate", "utilization_intensity", "cap_rate",
                   "stack_factor", "av_int_factor"):
        v = pd.to_numeric(table[column], errors="coerce")            # noqa: F821
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    alloc = pd.to_numeric(table["alloc_indexed"], errors="coerce")   # noqa: F821
    bad = table.index[~((alloc >= 0) & (alloc <= 1))].tolist()
    if bad:
        raise ValueError(f"{name}: alloc_indexed must be a number from 0 to 1; it is not "
                         f"at point_id {bad}")
    i0 = pd.to_numeric(table["mva_ref_yield_at_issue"], errors="coerce")  # noqa: F821
    bad = table.index[~((i0 > -1) & (i0 < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: mva_ref_yield_at_issue must be a number above -1; it "
                         f"is not at point_id {bad}")
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
    for column in money:
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    rate = values["payout_rate_locked_prev_anniv_init"]
    bad = table.index[~((rate >= 0) & (rate <= 1))].tolist()
    if bad:
        raise ValueError(f"{name}: payout_rate_locked_prev_anniv_init must be a number "
                         f"from 0 to 1; it is not at point_id {bad}")
    level = values["index_level_prev_anniv_init"]
    bad = table.index[~((level >= 0) & (level < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: index_level_prev_anniv_init must be a number, zero or "
                         f"more; it is not at point_id {bad}")
    code = values["phase_prev_anniv_init"]
    bad = table.index[~(code % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{name}: phase_prev_anniv_init must be a whole number, a phase "
                         f"code; it is not at point_id {bad}")
    for column in state:
        bad = table.index[(months <= 0) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    in_force = months > 0
    bad = table.index[in_force & ~code.isin([1, 2, 3])].tolist()
    if bad:
        raise ValueError(f"{name}: phase_prev_anniv_init must be 1 (ACCUM), 2 (INCOME) or "
                         f"3 (DEPLETED) on a policy in force: 4 (TERMINATED) is a deemed "
                         f"surrender of every contract; it is not at point_id {bad}")
    bad = table.index[in_force & ~(level > 0)].tolist()
    if bad:
        raise ValueError(f"{name}: index_level_prev_anniv_init must be more than 0 on a "
                         f"policy in force; it is not at point_id {bad}")
    bad = table.index[in_force & code.isin([2, 3]) & ~(elected == True)].tolist()  # noqa
    if bad:
        raise ValueError(f"{name}: a policy without the rider is in phase 1 (ACCUM): "
                         f"income starts only under the rider; it is not at point_id {bad}")
    cent = 0.01
    rider_cols = ("benefit_base_pp_init", "rollup_base_pp_init", "lw_pp_init",
                  "payout_rate_locked_prev_anniv_init")
    for column in rider_cols:
        bad = table.index[in_force & ~(elected == True)              # noqa: E712
                          & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy without the rider; "
                             f"it is not at point_id {bad}")
    bad = table.index[in_force & (elected == True)                   # noqa: E712
                      & ~(values["benefit_base_pp_init"] > 0)].tolist()
    if bad:
        raise ValueError(
            f"{name}: benefit_base_pp_init must be more than 0 on a policy in force with "
            f"the rider: an anniversary that takes it to 0 terminates the contract; it is "
            f"not at point_id {bad}")
    for column in ("lw_pp_init", "payout_rate_locked_prev_anniv_init"):
        bad = table.index[in_force & (code == 1) & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 in phase 1 (ACCUM), before the "
                             f"first lifetime withdrawal; it is not at point_id {bad}")
    bad = table.index[in_force & code.isin([2, 3])
                      & ((values["lw_pp_init"] > 0)
                         != (values["payout_rate_locked_prev_anniv_init"] > 0))].tolist()
    if bad:
        raise ValueError(f"{name}: lw_pp_init must be 0 in phase 2 (INCOME) or 3 "
                         f"(DEPLETED) exactly where payout_rate_locked_prev_anniv_init is "
                         f"0: the lifetime withdrawal is the locked percentage of a "
                         f"benefit base above 0, and a reduction that took it to 0 would "
                         f"have taken the base to 0 and terminated the contract; it is not "
                         f"at point_id {bad}")
    depleted = in_force & (code == 3)
    for column in ("av_pp_init", "av_fixed_pp_init", "av_pp_prev_anniv_init",
                   "av_fixed_pp_prev_anniv_init"):
        bad = table.index[depleted & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 in phase 3 (DEPLETED), the "
                             f"account value exhausted; it is not at point_id {bad}")
    bad = table.index[in_force & code.isin([1, 2])
                      & ~(values["av_pp_prev_anniv_init"] > 0)].tolist()
    if bad:
        raise ValueError(f"{name}: av_pp_prev_anniv_init must be more than 0 in phase 1 "
                         f"(ACCUM) or 2 (INCOME): an anniversary that exhausts the account "
                         f"value leaves them; it is not at point_id {bad}")
    for whole, part in (("av_pp_init", "av_fixed_pp_init"),
                        ("av_pp_prev_anniv_init", "av_fixed_pp_prev_anniv_init")):
        bad = table.index[values[part] > values[whole] + cent].tolist()
        if bad:
            raise ValueError(f"{name}: {part}, the fixed account, must not exceed {whole}, "
                             f"the account value it is part of; it does at point_id {bad}")
    premium = pd.to_numeric(table["premium"], errors="coerce")       # noqa: F821
    bonus = pd.to_numeric(table["bonus_rate"], errors="coerce")      # noqa: F821
    issue_av = premium * (1.0 + bonus)
    issue_base = premium.where(elected == True, 0.0)                 # noqa: E712
    first = in_force & (months < 12)
    for column, issued in (("av_pp_prev_anniv_init", issue_av),
                           ("av_fixed_pp_prev_anniv_init", (1.0 - alloc) * issue_av),
                           ("benefit_base_pp_init", issue_base),
                           ("rollup_base_pp_init", issue_base),
                           ("wd_cum_pp_init", 0.0 * premium)):
        bad = table.index[first & ~((values[column] - issued).abs() <= cent)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be its issue value in the first "
                             f"policy year, duration_mth 1 to 11, to a cent; it is not at "
                             f"point_id {bad}")
    bad = table.index[first & (code != 1)].tolist()
    if bad:
        raise ValueError(f"{name}: phase_prev_anniv_init must be 1 (ACCUM) in the first "
                         f"policy year; it is not at point_id {bad}")
    on_anniv = in_force & (months % 12 == 0)
    for column, entering in (("av_pp_prev_anniv_init", "av_pp_init"),
                             ("av_fixed_pp_prev_anniv_init", "av_fixed_pp_init")):
        bad = table.index[on_anniv & (values[column] != values[entering])].tolist()
        if bad:
            raise ValueError(f"{name}: on a point valued on a policy anniversary, "
                             f"duration_mth a multiple of 12, {column} must equal "
                             f"{entering}; it does not at point_id {bad}")
    mid = in_force & (months % 12 != 0)
    indexed_now = values["av_pp_init"] - values["av_fixed_pp_init"]
    indexed_then = values["av_pp_prev_anniv_init"] - values["av_fixed_pp_prev_anniv_init"]
    bad = table.index[mid & ~((indexed_now - indexed_then).abs() <= 3 * cent)].tolist()
    if bad:
        raise ValueError(f"{name}: off an anniversary, the indexed account, av_pp_init "
                         f"less av_fixed_pp_init, must equal av_pp_prev_anniv_init less "
                         f"av_fixed_pp_prev_anniv_init, to three cents: it moves only at "
                         f"an anniversary; it does not at point_id {bad}")
    bad = table.index[mid & (values["av_fixed_pp_init"]
                             < values["av_fixed_pp_prev_anniv_init"] - cent)].tolist()
    if bad:
        raise ValueError(f"{name}: off an anniversary, av_fixed_pp_init must not be below "
                         f"av_fixed_pp_prev_anniv_init: the fixed account only accrues "
                         f"between anniversaries; it is at point_id {bad}")
    # join keys, last
    entry = (-months).clip(lower=0)
    steps = rate_scenario_steps().reset_index()
    firsts = steps.groupby("scenario_id")["t"].min()
    bad = table.index[~(table["scenario_id"].map(firsts) <= entry)].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must be a scenario of {rate_scenario_file} "
                         f"that sets its levels by the first month the point is on the "
                         f"books, t = 0 or its issue month if later; it is not at "
                         f"point_id {bad}")
    opening = steps[steps["t"] == 0].set_index("scenario_id")["index_level"]
    level0 = table["scenario_id"].map(opening)
    bad = table.index[in_force & (months % 12 == 0)
                      & (values["index_level_prev_anniv_init"] != level0)].tolist()
    if bad:
        raise ValueError(
            f"{name}: on a point valued on a policy anniversary, duration_mth a multiple "
            f"of 12, index_level_prev_anniv_init must equal the index_level its scenario "
            f"sets at t = 0, the valuation date; it does not at point_id {bad}")
    ids = rollup_steps().index.get_level_values("rollup_id")
    bad = table.index[~table["rollup_id"].isin(ids)].tolist()
    if bad:
        raise ValueError(f"{name}: rollup_id must be a schedule of {rollup_file}; it is "
                         f"not at point_id {bad}")
    programmes = wd_schedules().index.get_level_values("wd_schedule_id")
    bad = table.index[~table["wd_schedule_id"].isin(programmes)].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must be a programme of "
                         f"{withdrawal_file}; it is not at point_id {bad}")
    rates = mort_rates().reset_index()
    youngest = rates.groupby("sex")["age"].min()
    oldest = rates.groupby("sex")["age"].max()
    issued = pd.to_numeric(table["age_at_entry"], errors="coerce")   # noqa: F821
    attained = issued + months.clip(lower=0) // 12
    sexes = table["sex"]
    bad = table.index[~((attained >= sexes.map(youngest))
                        & (attained <= sexes.map(oldest)))].tolist()
    if bad:
        raise ValueError(f"{name}: {mort_table_file} must give a rate at the point's sex "
                         f"and its attained age in the first month it is on the books; it "
                         f"does not at point_id {bad}")
    return table


def mort_table():
    """Annual mortality by attained age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def surr_charge_table():
    """Surrender charge and bonus vesting percentages by contract year [S5].

    Read from *surr_charge_table.csv*.  One file because [S5] states the two vectors as
    a single contract-year schedule pair, read at the same key.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="contract_year")   # noqa: F821


def rollup_table():
    """The guaranteed simple rollup schedules, read from *rollup_table.csv*.

    Indexed by ``(rollup_id, contract_year)`` and read as a step function of the contract
    year: each row states the rate that holds from its own year until the next row of the
    same schedule.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rollup_file,                                   # noqa: F821
        index_col=["rollup_id", "contract_year"])


def payout_rate_table():
    """The lifetime withdrawal percentage bands, read from *payout_rate_table.csv*.

    Banded rather than keyed: each row gives an inclusive attained-age band with the
    single-life and joint-life percentages [S3].
    """
    return pd.read_csv(input_dir() / payout_rate_file)               # noqa: F821


def rate_scenario():
    """The exogenous scenarios, read from *rate_scenario_sec.csv*.

    Indexed by ``(scenario_id, t)``, where ``t`` is a **valuation** month, 0 at the
    valuation date, the month at which an anniversary's level takes effect: each row states
    the index level and the MVA reference yield that hold from that month until the next row
    of the same scenario, so a flat path is one row. ``FIA_US_S``'s reader, unchanged and
    pointed at this model's own file through ``rate_scenario_file``.

    The file is generated from ``FIA_US_S``'s *rate_scenario.csv*, whose ``t`` is an
    anniversary number from issue. Each of ``FIA_US_S``'s scenarios is here under its own id
    at ``t = 12 x`` anniversary, which is where the anniversaries of a contract issued at
    the valuation date fall. Each row of the model point table valued in force at policy
    month ``d`` reads a copy of its scenario re-based to ``d``, ``{id}-M{d}``: the levels
    ``FIA_US_S`` set before month ``d`` collapse to the level in force at ``d``, at
    ``t = 0``, and the later rows move ``d`` months earlier. Each row issued ``k`` months
    after the valuation date reads a copy moved ``k`` months later, ``{id}-F{k}``, which
    sets no level before its issue month. So every row reads each anniversary's level at
    the valuation month its own anniversary falls in, step-filled forward, and the model
    reproduces ``FIA_US_S`` at every anniversary.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_scenario_file,                            # noqa: F821
        index_col=["scenario_id", "t"])


def withdrawal_table():
    """Scheduled ad hoc gross withdrawals, read from *withdrawal_table.csv*.

    Indexed by ``(wd_schedule_id, t)``, where ``t`` is an **elapsed contract year** count
    rather than a month, on the policy clock: a row keyed ``k`` is withdrawn at the
    anniversary closing contract year ``k + 1``, read at ``duration(t)``, however old the
    contract is at the valuation date.  A contract year with no row takes no ad hoc
    withdrawal.  Lifetime withdrawals are *not* scheduled here — they are generated by the
    rider from ``utilization_intensity`` and the locked payout percentage.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / withdrawal_file,                               # noqa: F821
        index_col=["wd_schedule_id", "t"])


def mort_rates():
    """Annual mortality by attained age and sex, as :func:`mort_table` reads it, checked.

    Indexed by ``(age, sex)``, the age read by value, once, so that an age written
    ``61.0`` is 61, as ``FIA_US_S``'s lookup matches it. ``Projection.mort_rate_base_at``,
    the table's one reader, reads it here, so a projection meets the check first. An age
    that is not a whole number, text and a blank among them, a blank sex, a rate that is not
    a number from 0 to 1, blank and text among them, and a sex whose ages do not run one row
    an age, without a gap or a repeat, are refused, naming the file, the column and the
    lines they are on: for the last, each age a sex repeats, with its lines, and each age or
    span of ages it lacks between its first and its last, every one of them in one message.
    The projection caps the annual rate it builds on this one at 1, ``min(q, 1.0)``, and a
    blank rate never reaches the cap.
    """
    name = mort_table_file                                           # noqa: F821
    rows = mort_table().reset_index()
    lines = rows.index + 2
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = lines[(~(ages.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be below 2**53 in size; it is not on line "
                         f"{bad}")
    bad = lines[rows["sex"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must not be blank; it is on line {bad}")
    rates = pd.to_numeric(rows["mort_rate"], errors="coerce")        # noqa: F821
    bad = lines[(~((rates >= 0) & (rates <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a number from 0 to 1; it is not on "
                         f"line {bad}")
    ages = ages.astype("int64")
    faults = []
    for sex, run in ages.groupby(rows["sex"]):
        for key in sorted(set(run[run.duplicated()])):
            on = lines[((rows["sex"] == sex) & (ages == key)).to_numpy()].tolist()
            faults.append(f"sex {sex} age {key} repeats on lines {on}")
        held = sorted(set(run))
        for a, b in zip(held, held[1:]):
            if b - a > 1:
                faults.append(f"no line holds sex {sex} " + (
                    f"ages {a + 1} to {b - 1}" if b - a > 2 else f"age {a + 1}"))
    if faults:
        raise ValueError(f"{name}: the ages of each sex must run one row an age, without a "
                         f"gap or a repeat; " + "; ".join(faults))
    keys = pd.MultiIndex.from_arrays([ages, rows["sex"]], names=["age", "sex"])  # noqa
    return pd.DataFrame({"mort_rate": rates.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys)


def surr_charge_scale():
    """The surrender charge and vesting schedule, as :func:`surr_charge_table` reads it,
    checked.

    Indexed by ``contract_year``, read by value, once, as ``FIA_US_S``'s lookup matches it.
    ``Projection.surr_charge_rate_py`` and ``Projection.vest_rate_py``, the two readers of
    its two columns, read it here, and take its last year, :func:`surr_charge_last_year`,
    from the same checked years, so a projection meets the check first. A year that is not a
    whole number, text and a blank among them, a rate that is not a number from 0 to 1, and
    years that do not run from 1, one row a year, without a gap or a repeat, are refused,
    naming the file, the column and the lines they are on: for the last, each year below 1
    or repeated, with its lines, and each year or span of years missing from 1 to the last,
    every one of them in one message. The last row holds for every later year.
    ``FIA_US_S`` takes ``int()`` of the raw years for its last one: one written as text
    raises Python's own message, naming no file.
    """
    name = surr_charge_file                                          # noqa: F821
    rows = surr_charge_table().reset_index()
    lines = rows.index + 2
    years = pd.to_numeric(rows["contract_year"], errors="coerce")    # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be a whole number; it is not on "
                         f"line {bad}")
    bad = lines[(~(years.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be below 2**53 in size; it is not "
                         f"on line {bad}")
    cols = {}
    for column in ("surr_charge_rate", "vest_rate"):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v >= 0) & (v <= 1))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number from 0 to 1; it is not "
                             f"on line {bad}")
        cols[column] = v.to_numpy(dtype="float64")
    years = years.astype("int64")
    faults = []
    for key in sorted(set(years[years < 1])):
        faults.append(f"contract_year {key}, below 1, is on lines "
                      f"{lines[(years == key).to_numpy()].tolist()}")
    for key in sorted(set(years[years.duplicated() & (years >= 1)])):
        faults.append(f"contract_year {key} repeats on lines "
                      f"{lines[(years == key).to_numpy()].tolist()}")
    held = [0] + sorted(set(years[years >= 1]))
    if len(held) == 1:
        faults.append("no line holds contract_year 1")
    for a, b in zip(held, held[1:]):
        if b - a > 1:
            faults.append(f"no line holds contract_year {a + 1}"
                          + (f" to {b - 1}" if b - a > 2 else ""))
    if faults:
        raise ValueError(f"{name}: the contract years must run from 1, one row a year, "
                         f"without a gap or a repeat; " + "; ".join(faults))
    return pd.DataFrame(cols, index=pd.Index(years, name="contract_year"))  # noqa: F821


def surr_charge_last_year():
    """The last contract year :func:`surr_charge_scale` gives a rate for, an int."""
    return int(surr_charge_scale().index.max())


def rollup_steps():
    """The rollup schedules, as :func:`rollup_table` reads them, checked.

    Indexed by ``(rollup_id, contract_year)``, the year read by value, once, as
    ``FIA_US_S``'s step function compares it. ``Projection.rollup_rate_py``, the table's one
    reader, reads it here, so a projection meets the check first. A contract year that is
    not a whole number, 1 or more, text and a blank among them, a blank ``rollup_id``, a
    rate that is not a finite number, zero or more, and a schedule that sets two rates in
    one year are refused, naming the file, the column and the lines they are on. A schedule
    is a step function, so its years need not run one a year: each row holds until the next
    of the same schedule. ``FIA_US_S``'s step function compares the raw years with the
    contract year: one written as text raises Python's own ``TypeError``, and a blank one is
    a rate that never holds.
    """
    name = rollup_file                                               # noqa: F821
    rows = rollup_table().reset_index()
    lines = rows.index + 2
    years = pd.to_numeric(rows["contract_year"], errors="coerce")    # noqa: F821
    bad = lines[(~((years % 1 == 0) & (years >= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be a whole number, 1 or more; it is "
                         f"not on line {bad}")
    bad = lines[(~(years.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be below 2**53 in size; it is not "
                         f"on line {bad}")
    bad = lines[rows["rollup_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: rollup_id must not be blank; it is on line {bad}")
    rates = pd.to_numeric(rows["rollup_rate"], errors="coerce")      # noqa: F821
    bad = lines[(~((rates >= 0) & (rates < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: rollup_rate must be a number, zero or more; it is not "
                         f"on line {bad}")
    years = years.astype("int64")
    keys = pd.MultiIndex.from_arrays([rows["rollup_id"], years],     # noqa: F821
                                     names=["rollup_id", "contract_year"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a schedule must set one rate a year; one sets two on "
                         f"lines {bad}")
    return pd.DataFrame({"rollup_rate": rates.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys)


def payout_rates():
    """The lifetime withdrawal percentages, one row an attained age, from the bands of
    :func:`payout_rate_table`, checked.

    Indexed by attained age, from the first band's ``age_lo`` to the last band's
    ``age_hi``, each age carrying its band's single-life and joint-life percentages.
    ``Projection.payout_rate_at``, the table's one reader, reads it here, and takes its
    extents, :func:`payout_rate_first_age` and :func:`payout_rate_last_age`, from the same
    checked ages, so a projection meets the check first. An age bound that is not a whole
    number, text and a blank among them, a percentage that is not a number from 0 to 1, and
    bands that do not run one after another, each from its ``age_lo`` to its ``age_hi``,
    without a gap or an overlap, are refused, naming the file, the column and the lines: for
    the last, each age or span of ages two bands hold, with their lines, each age or span no
    band holds between the first age and the last, and each band that ends below its start,
    with its line, every one of them in one message. ``FIA_US_S`` walks the bands at each
    read and takes ``int()`` of each bound: one written as text raises Python's own message,
    and an age in a gap between two bands reads 0.
    """
    name = payout_rate_file                                          # noqa: F821
    rows = payout_rate_table()
    lines = rows.index + 2
    lo = pd.to_numeric(rows["age_lo"], errors="coerce")              # noqa: F821
    hi = pd.to_numeric(rows["age_hi"], errors="coerce")              # noqa: F821
    for column, v in (("age_lo", lo), ("age_hi", hi)):
        bad = lines[(~(v % 1 == 0)).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on line "
                             f"{bad}")
    for column, v in (("age_lo", lo), ("age_hi", hi)):
        bad = lines[(~(v.abs() < 2.0 ** 53)).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be below 2**53 in size; it is not on "
                             f"line {bad}")
    cols = {}
    for column in ("payout_rate_single", "payout_rate_joint"):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v >= 0) & (v <= 1))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number from 0 to 1; it is not "
                             f"on line {bad}")
        cols[column] = v
    faults, held = [], {}
    for i in range(len(rows)):
        a, b, line = int(lo.iloc[i]), int(hi.iloc[i]), int(lines[i])
        if b < a:
            faults.append(f"the band on line {line} ends at age_hi {b}, below its age_lo "
                          f"{a}")
        for x in range(a, b + 1):
            held[x] = held.get(x, []) + [line]
    if not held and not faults:
        faults.append("no line holds an age")
    ages = sorted(held)
    start, kind = None, None        # the run of ages held alike being read: none or two up
    for x in range(ages[0], ages[-1] + 2) if ages else []:
        on = held.get(x, [])
        now = None if len(on) == 1 or x > ages[-1] else tuple(on)
        if start is not None and now != kind:
            span = f"age {start}" if x - 1 == start else f"ages {start} to {x - 1}"
            faults.append(f"no line holds {span}" if not kind else
                          f"{span} {'is' if x - 1 == start else 'are'} in the bands on "
                          f"lines {list(kind)}")
            start = None
        if now is not None and start is None:
            start, kind = x, now
    if faults:
        raise ValueError(f"{name}: the bands must run one after another, each from its "
                         f"age_lo to its age_hi, without a gap or an overlap; "
                         + "; ".join(faults))
    single, joint = [], []
    for x in ages:
        row = held[x][0] - 2                                         # the band's position
        single.append(float(cols["payout_rate_single"].iloc[row]))
        joint.append(float(cols["payout_rate_joint"].iloc[row]))
    return pd.DataFrame({"payout_rate_single": single, "payout_rate_joint": joint},  # noqa
                        index=pd.Index(ages, name="age"))            # noqa: F821


def payout_rate_first_age():
    """The first attained age :func:`payout_rates` gives a percentage for, an int.

    Below it no lifetime withdrawal is permitted, and the percentage is 0.
    """
    return int(payout_rates().index.min())


def payout_rate_last_age():
    """The last attained age :func:`payout_rates` gives a percentage for, an int.

    Its band holds for every older age, as in ``FIA_US_S``.
    """
    return int(payout_rates().index.max())


def rate_scenario_steps():
    """The rate scenarios, as :func:`rate_scenario` reads them, checked.

    Indexed by ``(scenario_id, t)``, each ``t`` a valuation month read by value, once.
    ``Projection.scenario_value``, the table's one reader, reads it here, so a projection
    meets the check first. A month that is not a whole number, 0 or more, text and a blank
    among them, a blank ``scenario_id``, an index level that is not a finite number above 0,
    whose ratio the index return takes, a reference yield that is not a finite number above
    -1, the base of the MVA's power, and a scenario that sets two levels at one month are
    refused, naming the file, the column and the lines they are on. A scenario may start
    after ``t = 0``, for business issued later, so the month a scenario must start by is the
    point's: :func:`model_point_table` refuses a point whose scenario sets no level by the
    first month the point is on the books.
    """
    name = rate_scenario_file                                        # noqa: F821
    rows = rate_scenario().reset_index()
    lines = rows.index + 2
    months = pd.to_numeric(rows["t"], errors="coerce")               # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be a whole number, 0 or more; it is not on line "
                         f"{bad}")
    bad = lines[(~(months.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be below 2**53 in size; it is not on line {bad}")
    bad = lines[rows["scenario_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    lev = pd.to_numeric(rows["index_level"], errors="coerce")        # noqa: F821
    bad = lines[(~((lev > 0) & (lev < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: index_level must be a number above 0; it is not on line "
                         f"{bad}")
    yld = pd.to_numeric(rows["mva_ref_yield"], errors="coerce")      # noqa: F821
    bad = lines[(~((yld > -1) & (yld < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: mva_ref_yield must be a number above -1; it is not on "
                         f"line {bad}")
    months = months.astype("int64")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["scenario_id"], months], names=["scenario_id", "t"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a scenario must set one level a month; one sets two on "
                         f"lines {bad}")
    return pd.DataFrame(                                             # noqa: F821
        {"index_level": lev.to_numpy(dtype="float64"),
         "mva_ref_yield": yld.to_numpy(dtype="float64")}, index=keys)


def wd_schedules():
    """The withdrawal programmes, as :func:`withdrawal_table` reads them, checked.

    Indexed by ``(wd_schedule_id, t)``, each ``t`` an elapsed contract year count read by
    value, once, as ``FIA_US_S``'s exact-key lookup matches it.
    ``Projection.wd_scheduled_at``, the table's one reader, reads it here, so a projection
    meets the check first. A year that is not a whole number, 0 or more, text and a blank
    among them, a blank ``wd_schedule_id``, an amount that is not a finite number, zero or
    more, and a programme that withdraws twice in one year are refused, naming the file, the
    column and the lines they are on. ``FIA_US_S``'s lookup matches the raw years: one
    written as text turns them all to text, and every withdrawal of every programme is then
    zero.
    """
    name = withdrawal_file                                           # noqa: F821
    rows = withdrawal_table().reset_index()
    lines = rows.index + 2
    years = pd.to_numeric(rows["t"], errors="coerce")                # noqa: F821
    bad = lines[(~((years % 1 == 0) & (years >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be a whole number, 0 or more; it is not on line "
                         f"{bad}")
    bad = lines[(~(years.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: t must be below 2**53 in size; it is not on line {bad}")
    bad = lines[rows["wd_schedule_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must not be blank; it is on line {bad}")
    amounts = pd.to_numeric(rows["wd_amount"], errors="coerce")      # noqa: F821
    bad = lines[(~((amounts >= 0) & (amounts < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_amount must be a number, zero or more; it is not on "
                         f"line {bad}")
    years = years.astype("int64")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["wd_schedule_id"], years], names=["wd_schedule_id", "t"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a programme must withdraw once a year at most; one "
                         f"withdraws twice on lines {bad}")
    return pd.DataFrame({"wd_amount": amounts.to_numpy(dtype="float64")},  # noqa: F821
                        index=keys)



def point_id():
    """The ``point_id`` of each row, an int64 vector, read by value from the table's index.

    ``Projection`` is indexed by position, ``idx``, and reads its point's label here, so
    that every refusal names the point by the label a reader finds in the table. A label
    that is not a whole number, or not below ``2**53`` in size, is refused, naming it:
    ``FIA_US_S`` keys its points by any label pandas reads.
    """
    table = model_point_table()
    labels = pd.to_numeric(pd.Series(table.index), errors="coerce")  # noqa: F821
    bad = table.index[~(labels % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: point_id must be a whole number; {bad} "
                         f"is not")
    bad = table.index[~(labels.abs() < 2.0 ** 53).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: point_id must be below 2**53 in size; "
                         f"{bad} is not")
    return labels.to_numpy(dtype="int64")


def age_at_entry():
    """The issue age of each point, an int64 vector (``Projection.age_at_entry``)."""
    years = pd.to_numeric(model_point_table()["age_at_entry"])       # noqa: F821
    return years.to_numpy(dtype="int64")


def income_start_age():
    """The age each point takes its first lifetime withdrawal at, an int64 vector."""
    years = pd.to_numeric(model_point_table()["income_start_age"])   # noqa: F821
    return years.to_numpy(dtype="int64")


def joint_age():
    """The joint covered person's issue age, an int64 vector; the annuitant's if blank.

    ``FIA_US_S``'s rule, decoded element by element: a blank ``joint_age`` reads the
    point's own ``age_at_entry``, and any other is the whole number it holds, which
    :func:`model_point_table` has checked.
    """
    table = model_point_table()
    given = pd.to_numeric(table["joint_age"])                        # noqa: F821
    issued = pd.to_numeric(table["age_at_entry"])                    # noqa: F821
    out = np.zeros(len(table), dtype="int64")                        # noqa: F821
    for i in range(len(table)):
        out[i] = int(issued.iloc[i]) if pd.isna(given.iloc[i]) else int(given.iloc[i])
    return out


def duration_mth():
    """The policy months completed at the valuation date, an int64 vector."""
    months = pd.to_numeric(model_point_table()["duration_mth"])      # noqa: F821
    return months.to_numpy(dtype="int64")


def phase_prev_anniv_init():
    """The phase code at the anniversary on or before the valuation date, int64."""
    codes = pd.to_numeric(model_point_table()["phase_prev_anniv_init"])  # noqa: F821
    return codes.to_numpy(dtype="int64")


def glwb_elected():
    """Whether each point elects the rider, 1 or 0, an int64 vector.

    :func:`model_point_table` has read the column by value into bools, so ``"False"``
    written as text is 0, not ``bool("False")``.
    """
    flags = model_point_table()["glwb_elected"]
    return flags.to_numpy(dtype="int64")


def premium():
    """P, the single premium of each point, a float64 vector."""
    values = pd.to_numeric(model_point_table()["premium"])           # noqa: F821
    return values.to_numpy(dtype="float64")


def policy_count():
    """The contracts each point stands for, a float64 vector."""
    values = pd.to_numeric(model_point_table()["policy_count"])      # noqa: F821
    return values.to_numpy(dtype="float64")


def bonus_rate():
    """b, the premium bonus rate of each point, a float64 vector."""
    values = pd.to_numeric(model_point_table()["bonus_rate"])        # noqa: F821
    return values.to_numpy(dtype="float64")


def alloc_indexed():
    """The indexed account's share of each point's account value, a float64 vector."""
    values = pd.to_numeric(model_point_table()["alloc_indexed"])     # noqa: F821
    return values.to_numpy(dtype="float64")


def utilization_intensity():
    """The share of the lifetime withdrawal each point takes, a float64 vector."""
    values = pd.to_numeric(model_point_table()["utilization_intensity"])  # noqa: F821
    return values.to_numpy(dtype="float64")


def cap_rate():
    """c, the declared annual cap of each point, a float64 vector."""
    values = pd.to_numeric(model_point_table()["cap_rate"])          # noqa: F821
    return values.to_numpy(dtype="float64")


def stack_factor():
    """m, the stacking factor of each point, a float64 vector."""
    values = pd.to_numeric(model_point_table()["stack_factor"])      # noqa: F821
    return values.to_numpy(dtype="float64")


def av_int_factor():
    """kappa, the index credit's share reaching each point's account value, float64."""
    values = pd.to_numeric(model_point_table()["av_int_factor"])     # noqa: F821
    return values.to_numpy(dtype="float64")


def mva_ref_yield_at_issue():
    """i0, the MVA reference yield locked at each point's issue, a float64 vector."""
    values = pd.to_numeric(model_point_table()["mva_ref_yield_at_issue"])  # noqa: F821
    return values.to_numpy(dtype="float64")


def av_pp_init():
    """The account value entering month 0, per contract, a float64 vector."""
    values = pd.to_numeric(model_point_table()["av_pp_init"])        # noqa: F821
    return values.to_numpy(dtype="float64")


def av_fixed_pp_init():
    """The fixed account entering month 0, per contract, a float64 vector."""
    values = pd.to_numeric(model_point_table()["av_fixed_pp_init"])  # noqa: F821
    return values.to_numpy(dtype="float64")


def av_pp_prev_anniv_init():
    """The account value at the anniversary on or before the valuation date, float64."""
    values = pd.to_numeric(model_point_table()["av_pp_prev_anniv_init"])  # noqa: F821
    return values.to_numpy(dtype="float64")


def av_fixed_pp_prev_anniv_init():
    """The fixed account at that anniversary, per contract, a float64 vector."""
    values = pd.to_numeric(                                          # noqa: F821
        model_point_table()["av_fixed_pp_prev_anniv_init"])
    return values.to_numpy(dtype="float64")


def benefit_base_pp_init():
    """The benefit base entering month 0, per contract, a float64 vector."""
    values = pd.to_numeric(model_point_table()["benefit_base_pp_init"])  # noqa: F821
    return values.to_numpy(dtype="float64")


def rollup_base_pp_init():
    """The rollup base entering month 0, per contract, a float64 vector."""
    values = pd.to_numeric(model_point_table()["rollup_base_pp_init"])  # noqa: F821
    return values.to_numpy(dtype="float64")


def mgsv_pp_init():
    """The Model #805 floor entering month 0, per contract, a float64 vector."""
    values = pd.to_numeric(model_point_table()["mgsv_pp_init"])      # noqa: F821
    return values.to_numpy(dtype="float64")


def lw_pp_init():
    """The lifetime withdrawal entering month 0, per contract, a float64 vector."""
    values = pd.to_numeric(model_point_table()["lw_pp_init"])        # noqa: F821
    return values.to_numpy(dtype="float64")


def payout_rate_locked_prev_anniv_init():
    """The payout percentage locked at the anniversary on or before the valuation date."""
    values = pd.to_numeric(                                          # noqa: F821
        model_point_table()["payout_rate_locked_prev_anniv_init"])
    return values.to_numpy(dtype="float64")


def index_level_prev_anniv_init():
    """The index level at the anniversary on or before the valuation date, float64."""
    values = pd.to_numeric(                                          # noqa: F821
        model_point_table()["index_level_prev_anniv_init"])
    return values.to_numpy(dtype="float64")


def wd_cum_pp_init():
    """The gross withdrawals from issue to the valuation date, per contract, float64."""
    values = pd.to_numeric(model_point_table()["wd_cum_pp_init"])    # noqa: F821
    return values.to_numpy(dtype="float64")


def is_single_basis():
    """1 where ``glwb_basis`` is ``single``, else 0, an int64 vector.

    ``FIA_US_S``'s comparison, made element by element, exactly: ``Single`` or ``single``
    with a space is 0, and so is a blank. A table without the column raises pandas'
    ``KeyError`` here, at the first read, as ``FIA_US_S`` raises it where a rider point
    first asks the basis, and a point without the rider never asks.
    """
    flags = model_point_table()["glwb_basis"] == "single"
    return flags.to_numpy(dtype="int64")


def is_joint_basis():
    """1 where ``glwb_basis`` is ``joint``, else 0, an int64 vector.

    The other decode of the column, as :func:`is_single_basis` is.
    """
    flags = model_point_table()["glwb_basis"] == "joint"
    return flags.to_numpy(dtype="int64")


def is_credit_cap():
    """1 where ``credit_method`` is ``cap``, else 0, an int64 vector.

    ``FIA_US_S``'s comparison, made element by element, exactly, as
    :func:`is_single_basis`'s is; a table without the column raises pandas' ``KeyError``
    at the first read, as ``FIA_US_S`` raises it at a point's first credit.
    """
    flags = model_point_table()["credit_method"] == "cap"
    return flags.to_numpy(dtype="int64")


def is_credit_par():
    """1 where ``credit_method`` is ``par``, else 0, an int64 vector."""
    flags = model_point_table()["credit_method"] == "par"
    return flags.to_numpy(dtype="int64")


def is_credit_par_cap():
    """1 where ``credit_method`` is ``par_cap``, else 0, an int64 vector."""
    flags = model_point_table()["credit_method"] == "par_cap"
    return flags.to_numpy(dtype="int64")


def is_credit_spread():
    """1 where ``credit_method`` is ``spread``, else 0, an int64 vector."""
    flags = model_point_table()["credit_method"] == "spread"
    return flags.to_numpy(dtype="int64")


def is_credit_trigger():
    """1 where ``credit_method`` is ``trigger``, else 0, an int64 vector."""
    flags = model_point_table()["credit_method"] == "trigger"
    return flags.to_numpy(dtype="int64")


def mort_schedule_count():
    """The number of sexes :func:`mort_rates` holds, an int."""
    return int(mort_rates().index.get_level_values("sex").nunique())


def mort_schedule():
    """The row of :func:`mort_table_array` each point reads, by its ``sex``, int64.

    The sexes are numbered from 1 in their sorted order, the order ``groupby`` takes, and
    each point carries its own sex's number, matched by the value pandas read, as
    ``FIA_US_S``'s ``.loc`` matches it. :func:`model_point_table` refuses a point whose sex
    the table lacks, so 0, the number of no sex, is never a point's.
    """
    number = {}
    for key, _ in mort_rates().groupby(level="sex"):
        number[key] = len(number) + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def mort_age_firsts():
    """Each sex's first age in :func:`mort_rates`, by its number, an int64 vector."""
    out = np.zeros(mort_schedule_count() + 1, dtype="int64")         # noqa: F821
    s = 0
    for _, rows in mort_rates().groupby(level="sex"):
        s += 1
        out[s] = int(rows.index.get_level_values("age").min())
    return out


def mort_age_lasts():
    """Each sex's last age in :func:`mort_rates`, by its number, an int64 vector.

    The table's own last age, however far past ``read_last_age``:
    ``Projection.proj_len`` refuses a point whose sex's last age is below
    ``maturity_age``, the age the last contract year is entered at.
    """
    out = np.zeros(mort_schedule_count() + 1, dtype="int64")         # noqa: F821
    s = 0
    for _, rows in mort_rates().groupby(level="sex"):
        s += 1
        out[s] = int(rows.index.get_level_values("age").max())
    return out


def mort_age_base():
    """The age of :func:`mort_table_array`'s first column, an int.

    The table's first age, of any sex, or 0 where that is below 0: an attained age is
    never below the youngest issue age, so no read reaches a negative age, and a row at
    a negative age, which ``FIA_US_S`` holds and never reads, is not held. So neither a
    negative age nor one far below every other widens the array.
    """
    return max(int(mort_rates().index.get_level_values("age").min()), 0)


def mort_age_held():
    """The age of :func:`mort_table_array`'s last column, ``read_last_age``, an int."""
    return read_last_age                                             # noqa: F821


def mort_table_array():
    """The annual mortality by sex and attained age, ``[sex, age - mort_age_base()]``.

    Row ``mort_schedule()`` of a point holds its sex's rates, row 0 none; column ``j`` is
    attained age ``mort_age_base() + j``, to :func:`mort_age_held`, ``read_last_age``, the
    oldest age a read reaches. Every cell outside a sex's ages, and row 0, is NaN, and an
    age past ``read_last_age`` is held nowhere, so a row far past it, which ``FIA_US_S``
    holds and never reads, neither widens the array nor refuses a point.
    """
    rates = mort_rates()
    base = mort_age_base()
    last = mort_age_held()
    out = np.full((mort_schedule_count() + 1, max(last - base + 1, 0)), np.nan)  # noqa
    s = 0
    for _, rows in rates.groupby(level="sex"):
        s += 1
        ages = rows.index.get_level_values("age").tolist()
        values = rows["mort_rate"].tolist()
        for j in range(len(ages)):
            if base <= ages[j] <= last:
                out[s, ages[j] - base] = values[j]
    return out


def surr_charge_rate_array():
    """The surrender charge percentage by contract year, ``[year]``; year 0 NaN.

    Years 1 to :func:`surr_charge_last_year`, which :func:`surr_charge_scale` holds without
    a gap, so the year is the index.
    """
    scale = surr_charge_scale()
    out = np.full(surr_charge_last_year() + 1, np.nan)               # noqa: F821
    years = scale.index.tolist()
    values = scale["surr_charge_rate"].tolist()
    for j in range(len(years)):
        out[years[j]] = values[j]
    return out


def vest_rate_array():
    """The bonus vesting percentage by contract year, ``[year]``; year 0 NaN.

    As :func:`surr_charge_rate_array`, from the schedule's other column.
    """
    scale = surr_charge_scale()
    out = np.full(surr_charge_last_year() + 1, np.nan)               # noqa: F821
    years = scale.index.tolist()
    values = scale["vest_rate"].tolist()
    for j in range(len(years)):
        out[years[j]] = values[j]
    return out


def rollup_count():
    """The number of schedules :func:`rollup_steps` holds, an int."""
    return int(rollup_steps().index.get_level_values("rollup_id").nunique())


def rollup_number():
    """The row of :func:`rollup_rate_array` each point reads, by its ``rollup_id``, int64.

    Numbered from 1 in the sorted order of the ids, as :func:`mort_schedule` numbers the
    sexes; :func:`model_point_table` refuses an id the table lacks.
    """
    number = {}
    for key, _ in rollup_steps().groupby(level="rollup_id"):
        number[key] = len(number) + 1
    ids = model_point_table()["rollup_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    for i in range(len(ids)):
        out[i] = number.get(ids[i], 0)
    return out


def rollup_last_year():
    """The last contract year :func:`rollup_rate_array` holds, an int.

    The contract year a month to ``read_last_mth`` can fall in, ``read_last_mth // 12 +
    1``, past any contract year a read reaches, whatever the table's keys: a schedule's
    last row holds to there, as ``FIA_US_S``'s step function holds it, and a row past it
    is held nowhere.
    """
    return read_last_mth // 12 + 1                                   # noqa: F821


def rollup_rate_array():
    """The guaranteed rollup rate by schedule and contract year, ``[schedule, year]``.

    Each schedule's rows step-filled from its year to the next row's, the last to
    :func:`rollup_last_year`, and 0.0 in the years before its first row, where
    ``FIA_US_S``'s step function finds no row and answers 0.0. Row 0 and year 0, which no
    read reaches, are NaN.
    """
    last = rollup_last_year()
    out = np.zeros((rollup_count() + 1, last + 1))                   # noqa: F821
    out[0, :] = np.nan                                               # noqa: F821
    out[:, 0] = np.nan                                               # noqa: F821
    s = 0
    for _, rows in rollup_steps().groupby(level="rollup_id"):
        s += 1
        pairs = sorted(zip(rows.index.get_level_values("contract_year").tolist(),
                           rows["rollup_rate"].tolist()))
        for j in range(len(pairs)):
            start = pairs[j][0]
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            if start <= last:
                out[s, start:min(end, last + 1)] = pairs[j][1]
    return out


def payout_rate_held_age():
    """The last exercise age :func:`payout_rate_array` holds, ``read_last_age``, an int."""
    return read_last_age                                             # noqa: F821


def payout_rate_array():
    """The lifetime withdrawal percentage by exercise age and basis, ``[age, basis]``.

    Row ``j`` is exercise age ``payout_rate_first_age() + j``, to
    :func:`payout_rate_held_age`, ``read_last_age``; column 0 is the single-life
    percentage, column 1 the joint-life. Ages past the last band's hold its percentages,
    as in ``FIA_US_S``, and an age past ``read_last_age`` is held nowhere, so bands far
    past it neither widen the array nor refuse a point. Ages below the first band, which
    read 0, have no row: the array is indexed from the first age, however low.
    """
    rates = payout_rates()
    first = payout_rate_first_age()
    last = payout_rate_last_age()
    held = payout_rate_held_age()
    out = np.full((max(held - first + 1, 0), 2), np.nan)             # noqa: F821
    for j in range(max(held - first + 1, 0)):
        age = min(first + j, last)
        out[j, 0] = float(rates.at[age, "payout_rate_single"])
        out[j, 1] = float(rates.at[age, "payout_rate_joint"])
    return out


def scenario_count():
    """The number of scenarios :func:`rate_scenario_steps` holds, an int."""
    return int(rate_scenario_steps().index.get_level_values("scenario_id").nunique())


def scenario_number():
    """The row of the scenario arrays each point reads, by its ``scenario_id``, int64.

    Numbered from 1 in the sorted order of the ids, as :func:`mort_schedule` numbers the
    sexes; :func:`model_point_table` refuses an id the companion lacks.
    """
    number = {}
    for key, _ in rate_scenario_steps().groupby(level="scenario_id"):
        number[key] = len(number) + 1
    ids = model_point_table()["scenario_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    for i in range(len(ids)):
        out[i] = number.get(ids[i], 0)
    return out


def scenario_first_mths():
    """Each scenario's first month, by its number, an int64 vector."""
    out = np.zeros(scenario_count() + 1, dtype="int64")              # noqa: F821
    s = 0
    for _, rows in rate_scenario_steps().groupby(level="scenario_id"):
        s += 1
        out[s] = int(rows.index.get_level_values("t").min())
    return out


def scenario_last_mth():
    """The last valuation month the scenario arrays hold, ``read_last_mth``, an int.

    The last month any read reaches, whatever the companion's keys: a scenario's last row
    holds to there, as ``FIA_US_S``'s step function holds it, and a row past it is held
    nowhere.
    """
    return read_last_mth                                             # noqa: F821


def index_level_array():
    """The index level by scenario and valuation month, ``[scenario, t]``.

    Each scenario's rows step-filled from its month to the next row's, the last to
    :func:`scenario_last_mth`; NaN before a scenario's first month and in row 0.
    """
    last = scenario_last_mth()
    out = np.full((scenario_count() + 1, last + 1), np.nan)          # noqa: F821
    s = 0
    for _, rows in rate_scenario_steps().groupby(level="scenario_id"):
        s += 1
        pairs = sorted(zip(rows.index.get_level_values("t").tolist(),
                           rows["index_level"].tolist()))
        for j in range(len(pairs)):
            start = pairs[j][0]
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            if start <= last:
                out[s, start:min(end, last + 1)] = pairs[j][1]
    return out


def mva_ref_yield_array():
    """The MVA reference yield by scenario and valuation month, ``[scenario, t]``.

    As :func:`index_level_array`, from the companion's other column.
    """
    last = scenario_last_mth()
    out = np.full((scenario_count() + 1, last + 1), np.nan)          # noqa: F821
    s = 0
    for _, rows in rate_scenario_steps().groupby(level="scenario_id"):
        s += 1
        pairs = sorted(zip(rows.index.get_level_values("t").tolist(),
                           rows["mva_ref_yield"].tolist()))
        for j in range(len(pairs)):
            start = pairs[j][0]
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            if start <= last:
                out[s, start:min(end, last + 1)] = pairs[j][1]
    return out


def wd_schedule_count():
    """The number of programmes :func:`wd_schedules` holds, an int."""
    return int(wd_schedules().index.get_level_values("wd_schedule_id").nunique())


def wd_schedule_number():
    """The row of :func:`wd_amount_array` each point reads, by its ``wd_schedule_id``.

    Numbered from 1 in the sorted order of the ids, int64, as :func:`mort_schedule`
    numbers the sexes; :func:`model_point_table` refuses an id the table lacks.
    """
    number = {}
    for key, _ in wd_schedules().groupby(level="wd_schedule_id"):
        number[key] = len(number) + 1
    ids = model_point_table()["wd_schedule_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    for i in range(len(ids)):
        out[i] = number.get(ids[i], 0)
    return out


def wd_last_year():
    """The last elapsed contract year count :func:`wd_amount_array` holds, an int.

    The count a month to ``read_last_mth`` can fall in, ``read_last_mth // 12``, past any
    count a read reaches: a row past it is held nowhere.
    """
    return read_last_mth // 12                                       # noqa: F821


def wd_amount_array():
    """The ad hoc withdrawal by programme and elapsed contract years, ``[programme, k]``.

    0.0 at a count a programme has no row for, a value, as ``FIA_US_S``'s lookup answers
    it, not padding; row 0, which no point reads, is NaN.
    """
    last = wd_last_year()
    out = np.zeros((wd_schedule_count() + 1, last + 1))              # noqa: F821
    out[0, :] = np.nan                                               # noqa: F821
    s = 0
    for _, rows in wd_schedules().groupby(level="wd_schedule_id"):
        s += 1
        years = rows.index.get_level_values("t").tolist()
        amounts = rows["wd_amount"].tolist()
        for j in range(len(years)):
            if 0 <= years[j] <= last:
                out[s, years[j]] = amounts[j]
    return out


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

mort_table_file = "mort_table.csv"

surr_charge_file = "surr_charge_table.csv"

rollup_file = "rollup_table.csv"

payout_rate_file = "payout_rate_table.csv"

rate_scenario_file = "rate_scenario_sec.csv"

withdrawal_file = "withdrawal_table.csv"

future_horizon_mth = 120

read_last_mth = 1093

read_last_age = 122

pd = ("Module", "pandas")

np = ("Module", "numpy")
