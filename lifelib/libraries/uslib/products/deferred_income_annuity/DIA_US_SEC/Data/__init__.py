# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.DIA_US_SEC.Projection` as ``data``. :mod:`~.DIA_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/deferred_income_annuity/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``DIA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Four of the tables are DIA_US_S's.** The mortality table, the improvement scale and
the two factor tables are the files :mod:`~.DIA_US_S` reads, read here in place: one copy
of each table serves both models, so an edit to one reaches both. The model point table
and the premium schedule are this model's own, ``model_point_table_sec.csv`` and
``premium_schedule_sec.csv``; they sit beside ``DIA_US_S``'s ``model_point_table.csv``
and ``premium_schedule.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ==============================  ==========================
Reference                 Cells                           File
========================  ==============================  ==========================
model_point_file          model_point_table()             model_point_table_sec.csv
premium_schedule_file     premium_schedule_table()        premium_schedule_sec.csv
mort_table_file           mort_table()                    mort_table.csv
improvement_scale_file    improvement_scale()             improvement_scale.csv
payout_factor_file        payout_factor_table()           payout_factor_table.csv
rop_factor_file           rop_factor_table()              rop_factor_table.csv
========================  ==============================  ==========================

**The model point table is checked as it is read.** Ten of its columns are the in-force
interface: ``policy_count`` and ``duration_mth``, as in ``basiclife.BasicTerm_SE``, and
the eight columns of a contract's opening state — each covered life's survival at the
valuation date, the premiums paid and the income bought by then, the guarantee period the
kernel prices with, the two frozen cohort weights and the reference rate's change since
issue. :func:`model_point_table` refuses a table that lacks any of them, repeats a
``point_id``, holds a count, a duration, a month or a contract term no contract can have,
or holds an opening state no contract can be in. The checks run in turn, and the first
that fails raises, naming the missing column or every point that fails it. It also
refuses a policy to be issued more than ``future_horizon_mth`` months after the valuation
date, 120 months as shipped: future new business is written over a stated horizon, so
that no frame runs longer than the stop rule from issue plus that horizon. Set to 0, the
Reference refuses future new business altogether. Whether a contract still owes a payment
at the valuation date is a rule of the product rather than of the table, and
``Projection.proj_len`` checks it.

**So is the premium schedule.** A DIA is a flexible-premium contract: "any number of
premiums during the deferral period" [S2][S3][S4][R13], each buying its own paid-up income
slice at the purchase rate then in force. A fixed set of premium columns on the model
point table would cap that number, so the schedule is a long table keyed by ``point_id``
with one row per slice, and :func:`premium_array` collapses it to a table of each point's
premium by policy month, read by :func:`~.DIA_US_SEC.Projection.premium_pm`, as
``DIA_US_S``'s ``premium_by_mth`` collapses it to a month-to-amount mapping once per
contract. This model's schedule holds the premiums
**still due** at the valuation date: those paid before it are in the contract's opening
state, as the premiums paid and the income they bought. :func:`premium_schedule_table`
refuses a row that names no point of the table, a month or an amount no premium can have,
a premium before the valuation date or at or after the income start month, and a point
that buys no income at all, which ``DIA_US_S`` would project silently.

**So are the four assumption tables**, each by a count cell beside ``DIA_US_S``'s reader,
which is unchanged: :func:`mort_table_count`, :func:`improvement_scale_count`,
:func:`payout_factor_count` and :func:`rop_factor_count`. Each reads its table's keys by
value, once, as the per-point join in ``Projection`` matches them, so that an age written
``70.0`` is 70, and refuses a key that is blank, text or not a whole number, a sex or a
payout form no join reads, and a key on more than one row; the mortality table and the
improvement scale, read at every age from a life's issue age up, refuse a gap in a sex's
ages too. Each refuses a value that is blank, text, infinite or outside its table's range.
Every message names the file, the column and the lines at fault. A rate, a scale or a
factor reaches the projection through survival and the purchase rates, where the refund
balance's ``max(0, ·)`` and the payment factor's ``max`` would lose a blank,
``max(0.0, nan)`` being 0.0; mortality's cap, written with the rate first, keeps it a NaN
until then. Each join asks its table's count before it reads a value, so a projection
meets the checks first, and reads ``DIA_US_S``'s frame.

**The two factor tables are the pricing kernel's data, and both are [std].** No
purchase-rate table was obtained and none is published — the Compact expressly relieves
the insurer of disclosing the deferral-period mortality and interest basis
[R13 §1.B(1)(a)] — so ``payout_factor_table.csv`` and ``rop_factor_table.csv`` carry the
technical notes' *illustrative* factors, marked as such in their ``provenance`` columns.
A model point can bypass them entirely by setting ``factor_basis = "formula"``, which
computes equation (2) and the equation (3) mid-band approximation from the shipped
mortality table instead.

The mortality table and the improvement scale are keyed by ``(age, sex)``. They are
separate files on purpose: the technical notes prescribe the **2012 IAM Basic** table
projected generationally with **Projection Scale G2** [R9][REG-R59], two distinct
objects with distinct provenance, and neither may be embedded in the model — the shipped
tables are illustrative **[std]** stand-ins, the mortality table being the one that
reproduces the notes' worked-example survival anchors. To swap in a licensed basis,
replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a
different name before the model computes anything. No formula changes. Replacing a file
changes :mod:`~.DIA_US_S` too, which reads the same one.

**The vectors.** The readers return what the files hold, and no
:mod:`~.DIA_US_SEC.Projection` cell but ``model_point`` and the cells kept for a reader,
the premium schedule's two among them, reads them. The others read the arrays below
instead, one element at a time, a model point's attribute being the element at its
position, ``data.issue_age()[idx]``. That is what lets the model compile to C, as
``basiclife.BasicTerm_SC`` does: each array is a numpy vector or table of int64 or
float64, which compiles to a typed memoryview, never one of bools, objects or text, and
each check of a table is an int. Each model point column a projection reads is one vector
of the column's own name, read element by element as ``DIA_US_SEC`` read the point's value
at stage ``E``, ``float()`` of an amount or a rate, ``int()`` of an age, a month or a year;
and where a point's value can be one its projection cannot use, a 0/1 vector beside it,
``<column>_ok``, says whether it is usable. The text the projection branches on is decoded
into 0/1 flags, each with a ``has_*`` flag that says the value is one ``DIA_US_S`` names.
The mortality table and the improvement scale, keyed by age and sex, are tabled by
schedule, one per sex, and age, padded from age 0, each point carrying the schedule of
each life's sex. The two factor tables are row vectors, in the file's order, each key a
number, read by a scan over the table's rows. And the premium schedule is a table by point
and policy month:

===============================  =======  =====================  ======================
Cells                            dtype    Shape                  From
===============================  =======  =====================  ======================
point_id()                       int64    [point]                the table's index
policy_count()                   float64  [point]                ``policy_count``
duration_mth()                   int64    [point]                ``duration_mth``
duration_mth_ok()                int64    [point]                ``duration_mth``, its
                                                                 flag
issue_age()                      int64    [point]                ``issue_age``
issue_age_ok()                   int64    [point]                ``issue_age``, its
                                                                 flag
joint_age()                      int64    [point]                ``joint_age``, 0 where
                                                                 blank
joint_age_ok()                   int64    [point]                ``joint_age``, its
                                                                 flag
is_joint()                       int64    [point]                ``joint``, 1 on True
survivor_pct()                   float64  [point]                ``survivor_pct``
certain_period()                 int64    [point]                ``certain_period``
certain_period_ok()              int64    [point]                ``certain_period``,
                                                                 its flag
income_start_mth()               int64    [point]                ``income_start_mth``
income_start_mth_ok()            int64    [point]                ``income_start_mth``,
                                                                 its flag
frequency()                      int64    [point]                ``frequency``
frequency_ok()                   int64    [point]                ``frequency``, its
                                                                 flag
cola_rate()                      float64  [point]                ``cola_rate``
issue_year()                     int64    [point]                ``issue_year``
issue_year_ok()                  int64    [point]                ``issue_year``, its
                                                                 flag
purchase_rate_dp()               int64    [point]                ``purchase_rate_dp``,
                                                                 -1 where blank
purchase_rate_dp_ok()            int64    [point]                ``purchase_rate_dp``,
                                                                 its flag
adjust_mth()                     int64    [point]                ``adjust_mth``, -1
                                                                 where blank
adjust_mth_ok()                  int64    [point]                ``adjust_mth``, its
                                                                 flag
adjust_start_mth()               int64    [point]                ``adjust_start_mth``,
                                                                 -1 where blank
adjust_start_mth_ok()            int64    [point]                ``adjust_start_mth``,
                                                                 its flag
accel_mth()                      int64    [point]                ``accel_mth``, -1
                                                                 where blank
accel_mth_ok()                   int64    [point]                ``accel_mth``, its
                                                                 flag
commute_mth()                    int64    [point]                ``commute_mth``, -1
                                                                 where blank
commute_mth_ok()                 int64    [point]                ``commute_mth``, its
                                                                 flag
commute_frac()                   float64  [point]                ``commute_frac``, 0.0
                                                                 where blank
other_qlac_premium()             float64  [point]                ``other_qlac_premium``
lives_if_init_1()                float64  [point]                ``lives_if_init_1``
lives_if_init_2()                float64  [point]                ``lives_if_init_2``
cum_premium_pp_init()            float64  [point]                the column
annual_income_init()             float64  [point]                the column
guarantee_mths_pricing_init()    float64  [point]                the column, NaN where
                                                                 blank
surv_to_payout_init()            float64  [point]                the column, NaN where
                                                                 blank
commute_weight_init()            float64  [point]                the column, NaN where
                                                                 blank
ref_rate_shift_init()            float64  [point]                the column
has_market_type()                int64    [point]                ``market_type``, 1 on
                                                                 one of four
is_qlac()                        int64    [point]                the same, 1 on QLAC
has_income_form()                int64    [point]                ``income_form``, 1 on
                                                                 one of five
is_life_only()                   int64    [point]                the same, 1 on LO or
                                                                 LO_ROP
is_cash_refund()                 int64    [point]                the same, 1 on CR
is_installment_refund()          int64    [point]                the same, 1 on IR
is_period_certain()              int64    [point]                the same, 1 on PC
has_db_form()                    int64    [point]                ``db_form``, 1 on ROP
                                                                 or NONE
is_rop()                         int64    [point]                the same, 1 on ROP
has_timing()                     int64    [point]                ``timing``, 1 on
                                                                 arrears or advance
is_arrears()                     int64    [point]                the same, 1 on arrears
has_reduction_trigger()          int64    [point]                ``reduction_trigger``,
                                                                 1 on either or primary
is_trigger_either()              int64    [point]                the same, 1 on either
has_mort_basis()                 int64    [point]                ``mort_basis``, 1 on
                                                                 anchor or generational
is_generational()                int64    [point]                the same, 1 on
                                                                 generational
has_factor_basis()               int64    [point]                ``factor_basis``, 1 on
                                                                 table or formula
is_formula_basis()               int64    [point]                the same, 1 on formula
mort_sexes()                     int      scalar                 *mort_table.csv*,
                                                                 checked
mort_table_array()               float64  [schedule, age]        *mort_table.csv*
mort_age_first()                 int64    [schedule]             *mort_table.csv*
mort_age_last()                  int64    [schedule]             *mort_table.csv*
mort_schedule_1()                int64    [point]                ``sex``, joined; 0
                                                                 where not
mort_schedule_2()                int64    [point]                ``joint_sex``, joined;
                                                                 0 where not
improvement_sexes()              int      scalar                 the improvement scale,
                                                                 checked
improvement_array()              float64  [schedule, age]        the improvement scale
improvement_age_first()          int64    [schedule]             the improvement scale
improvement_age_last()           int64    [schedule]             the improvement scale
improvement_schedule_1()         int64    [point]                ``sex``, joined; 0
                                                                 where not
improvement_schedule_2()         int64    [point]                ``joint_sex``, joined;
                                                                 0 where not
payout_income_start_age()        int64    [row]                  the payout table
payout_sex()                     int64    [row]                  the same, its sex
                                                                 numbered
payout_form_code()               int64    [row]                  the same, LO 1, CR 2,
                                                                 IR 3, PC 4
payout_factor_value()            float64  [row]                  the same, its factor
payout_schedule()                int64    [point]                ``sex``, in the
                                                                 table's numbering; 0
                                                                 where not
rop_issue_age()                  int64    [row]                  *rop_factor_table.csv*
rop_sex()                        int64    [row]                  the same, its sex
                                                                 numbered
rop_deferral_years()             int64    [row]                  the same
rop_factor_value()               float64  [row]                  the same, its factor
rop_schedule()                   int64    [point]                ``sex``, in the
                                                                 table's numbering; 0
                                                                 where not
premium_width()                  int      scalar                 the premium schedule
premium_array()                  float64  [point, policy month]  the same, summed by
                                                                 month
premium_rows()                   int64    [point, policy month]  the same, its rows by
                                                                 month
premium_last()                   int64    [point]                the same, the last
                                                                 month with a row; -1
                                                                 where none
===============================  =======  =====================  ======================

Each age table is numbered by its own sexes, in sorted order, from schedule 1, so the two
tables need not hold the same sexes: :func:`mort_sexes` and :func:`improvement_sexes`, each
asking the table's count cell first, give the count. Schedule 0 is a row of padding whose
first age is 1 and whose last is 0, so that no age lies between them: a life whose sex a
table lacks, a blank among them, has schedule 0 there, and ``Projection``'s reader of the
table refuses it, naming the point, the age and the life, at the first age it reads, where
``DIA_US_S``'s ``.loc`` raised ``KeyError``. The two factor tables number their sexes the
same way, each by its own, and ``Projection.payout_factor`` and ``Projection.rop_factor``
scan the table's rows for the point's key, the first match its only one, since the count
cell refuses a key on two rows; a sex the table lacks, schedule 0, matches no row, and a
key no row holds is refused there, naming the point and the key. Neither table is held as
an array by its keys: ``DIA_US_S`` reads the ROP factor at every premium month, at an
attained age and a deferral no contract bounds, so an array sized by the keys would be
sized by the file's largest, and both tables are a handful of rows.

**The premium schedule** is :func:`premium_array`, each point's premiums by policy month,
``0.0`` in a month with none, read by ``Projection.premium_pm``. A point's rows are summed
month by month as ``DIA_US_S``'s ``premium_by_mth`` sums them: its rows sorted by
``premium_mth`` as ``DIA_US_S`` sorts them, each amount added in that order to the month's
total from 0.0, so that a month with two rows holds ``DIA_US_S``'s float to the last bit.
:func:`premium_rows` counts each month's rows, so that ``Projection`` visits a month with
a premium of 0.0, as ``DIA_US_S``'s dict holds it, and :func:`premium_last` is a point's
last month with a row. The table is :func:`premium_width` months wide, the schedule's
latest month and one, but no wider than ``premium_last_mth`` and one, 1,440: a premium
after policy month 1,439 belongs to a point whose income starts later than the caches
hold, which ``Projection.stop_mth``, asked by ``Projection.proj_len``, refuses before any
premium is read, so no premium a projection reads is left out. That bound keeps a month
far out, ``1e10`` say, from asking for a table of 80 GB a point before the point is
refused. The arrays hold 16 bytes a point and month, about 25 KB on the committed table,
about 1 KB a point, and up to 23 KB a point where income starts late.

**What a point's projection cannot use is refused where it reads it,** by the point's own
``Projection`` cell, naming the point, never here: no point is refused for another's
value, nor for a column its projection never reads, beyond what :func:`model_point_table`
refused at stage ``E``, as it still does. Where a vector cannot hold a value, the vector
holds 0 there and its ``_ok`` flag 0, and the ``Projection`` accessor that reads the
element raises: on a blank or text value ``int()`` refuses, a single-life point's blank
``joint_age``, which no projection reads, among them; and on an int of ``2**53`` or more in
size, which an int64 cannot be trusted to hold, since a float past int64 casts to the least
int64 without a word. ``DIA_US_S`` projects such a value as exact, so that is a recorded
refusal. The text the decodes branch on is compared exactly, case and whitespace included,
as ``DIA_US_S`` compares it, and a value ``DIA_US_S`` does not name sets no ``has_*`` flag,
so the decode that reads it raises ``DIA_US_S``'s message there, as at stage ``E``. And
:func:`point_id` refuses a label that is not a whole number below ``2**53``, naming every
label at fault, when a label is first read.

**An array is read by element, never whole,** in this Space as in
:mod:`~.DIA_US_SEC.Projection`. The compiler types an array cell as a memoryview only once
it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python object.
So an array derived here reads the table's column, and a width comes from a table or a
check's int, never from another cell's array; each table's check is one int cell that its
arrays, its extents and its schedules read first. The column keywords of
:func:`premium_schedule_table`'s ``DataFrame.assign`` are passed as ``**{...}``, since a
keyword named as a cell of this Space, ``point_id``, would be rewritten by the export. And
:func:`model_point_table` reads the file whole, ``low_memory=False``, so that pandas types
each column once, not chunk by chunk, which on a large extract warned and changed nothing.
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

    Indexed by ``point_id``. Ten columns are the in-force interface: ``policy_count``, the
    contracts the point stands for, and ``duration_mth``, the months elapsed from issue at
    the valuation date, as in ``basiclife.BasicTerm_SE``; then the opening state, per
    contract, as it stands at the start of month 0, before any month-0 event:

    * ``lives_if_init_1`` and ``lives_if_init_2``: each covered life's probability of
      being alive at the valuation date, 1 or 0 on a real record, where a joint contract
      may carry one life already dead, and 0 for the second life of a single-life
      contract;
    * ``cum_premium_pp_init`` and ``annual_income_init``: the premiums paid and the
      guaranteed annual income they bought, per contract, before the valuation date;
    * ``guarantee_mths_pricing_init``: on a cash or installment refund in force, the
      guarantee period in months with which the pricing kernel prices every slice, a
      fixed point over the whole premium schedule; blank otherwise;
    * ``surv_to_payout_init``: where the income start month precedes the valuation month,
      the cohort that reached the income phase, ``l_last(T)``; blank otherwise;
    * ``commute_weight_init``: where the commutation month precedes the valuation month,
      the cohort that commuted, ``l_last(t_c)``; blank otherwise;
    * ``ref_rate_shift_init``: the reference rate at the valuation date less the reference
      rate at issue, as a decimal.

    The rest are ``DIA_US_S``'s, ``pols_if_init`` renamed ``policy_count``, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on. First the
    table's own shape:

    * the ten in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months, read by value, so that ``12.0`` is
      12: positive for a contract in force, 0 for one issued at the valuation date,
      negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused.

    Then the contract's terms, the income start month in force first, because the later
    checks read it:

    * ``income_start_mth`` is a whole number of months, 0 or more, a policy month;
    * each option month, ``adjust_mth``, ``adjust_start_mth``, ``accel_mth`` and
      ``commute_mth``, is blank or a whole number of months, a policy month; a negative
      month reads as never, as ``DIA_US_S`` reads -1;
    * the start-date adjustment's two months go together, and the new start month
      follows the exercise, so the income start month in force,
      ``adjust_start_mth`` where an adjustment is named and ``income_start_mth``
      otherwise, is a policy month after every premium priced to the old one;
    * a start-date adjustment is a deferral option: ``adjust_mth`` precedes the
      ``income_start_mth`` it moves, where ``DIA_US_S`` would pay nothing from that month
      to the exercise;
    * an acceleration and a commutation, payout-phase options, fall at or after the income
      start month in force;
    * an acceleration and a commutation fall six months apart or more, the product's
      interlock between its two payout options [S4]: inside the acceleration's blackout,
      ``DIA_US_S``'s commuted value counts the instalments the lump sum has paid;
    * ``joint`` is a flag, read by value: ``True`` or ``False``, as pandas reads either, or
      1 or 0, where ``DIA_US_S``'s ``bool()`` reads any text, a blank among them, as
      ``True``; ``sex`` is ``M`` or ``F``, and so is ``joint_sex`` on a joint contract,
      the two values the tables keyed by sex hold;
    * ``issue_age``, ``certain_period`` and, on a joint contract, ``joint_age`` are whole
      numbers of years, 0 or more; ``frequency`` is a whole number of payments a year and
      ``issue_year`` a whole calendar year; ``purchase_rate_dp`` is blank or a whole number
      of decimal places, 0 or more. Each is read by value, so that ``60.0`` is 60;
    * ``survivor_pct`` is a probability, and ``cola_rate`` and ``other_qlac_premium``
      numbers zero or more, each reaching a ``max`` or a comparison that would lose a
      blank; ``commute_frac`` is blank, for none, or a fraction, 0 to 1;
    * the table basis is single-life: a joint contract carries
      ``factor_basis = "formula"``.

    Then the opening state:

    * each covered life is a probability, 0 to 1; the premiums paid and the income
      bought are numbers, zero or more; the guarantee period is blank or a number of
      months, zero or more; each frozen weight is blank or a probability; the reference
      rate's change is a number, of either sign, the floor applying to the whole change
      since issue in ``Projection.commute_disc_rate``;
    * a single-life contract has no second life: ``lives_if_init_2`` is 0;
    * a contract not yet in force, ``duration_mth`` 0 or less, holds its values at issue:
      each covered life 1, no premium paid, no income bought and no change in the
      reference rate;
    * ``guarantee_mths_pricing_init`` is given exactly on a contract in force on a refund
      form, ``income_form`` CR or IR, and blank on every other: on new business the kernel
      derives it from the premium schedule, and the other forms fix it;
    * ``surv_to_payout_init`` is given exactly where ``duration_mth`` is after the income
      start month in force, and ``commute_weight_init`` exactly where the commutation month
      precedes ``duration_mth``: at or after the valuation month the projection derives
      each from the lives;
    * a commutation is taken in the income phase by part of the cohort that reached it, so
      ``commute_weight_init`` is at most ``surv_to_payout_init``, and each frozen weight is
      at least the probability that a covered life is alive at the valuation date, the
      cohort it weighs including every life still alive;
    * each frozen weight, where given, is above 0: a contract in force past its income start
      month reached it, and a commutation is exercised by an owner alive to exercise it, so
      neither cohort is empty. At 0 the guarantee of a contract whose lives have all died
      would pay nothing, a contract owing nothing that would project.

    The table is returned with the columns those checks read by value, the policy months
    and the contract's whole numbers and rates, as the numbers they were checked as (int64
    where a whole-number column has no blank, float64 otherwise, blank as NaN), which the
    vectors below read with ``int()`` and ``float()``, and ``joint`` as the flags it was
    checked as. Whether the contract still owes a payment at the valuation date needs the
    certain period, which an installment refund derives in ``Projection``, so
    ``Projection.proj_len`` checks it.

    The file is read whole, ``low_memory=False``, so that pandas types each column once,
    not chunk by chunk, which on a large extract warned and changed nothing.  Every check
    here is stage ``E``'s, and refuses the whole table, values a projection never reads
    among them: no check of that kind is added at stage ``EC``, where a value a point's
    projection cannot use is refused by that point's projection alone.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id",    # noqa: F821
                        low_memory=False)
    state = ("lives_if_init_1", "lives_if_init_2", "cum_premium_pp_init",
             "annual_income_init", "guarantee_mths_pricing_init", "surv_to_payout_init",
             "commute_weight_init", "ref_rate_shift_init")
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
    checked = {}
    start = pd.to_numeric(table["income_start_mth"], errors="coerce")  # noqa: F821
    bad = table.index[~((start % 1 == 0) & (start >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: income_start_mth must be a whole number of months, 0 "
                         f"or more, a policy month; it is not at point_id {bad}")
    checked["income_start_mth"] = start
    options = {}
    for column in ("adjust_mth", "adjust_start_mth", "accel_mth", "commute_mth"):
        month = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~(table[column].isna() | (month % 1 == 0))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a whole number of "
                             f"months, a policy month; it is not at point_id {bad}")
        checked[column] = month
        options[column] = month.where(month >= 0)
    adjust, moved = options["adjust_mth"], options["adjust_start_mth"]
    bad = table.index[adjust.notna() != moved.notna()].tolist()
    if bad:
        raise ValueError(f"{name}: adjust_mth and adjust_start_mth go together, both "
                         f"blank or both a policy month; they do not at point_id {bad}")
    bad = table.index[adjust.notna() & ~(moved > adjust)].tolist()
    if bad:
        raise ValueError(f"{name}: adjust_start_mth must follow adjust_mth: an income "
                         f"start date moves to a month after the exercise; it does not "
                         f"at point_id {bad}")
    bad = table.index[adjust.notna() & ~(adjust < start)].tolist()
    if bad:
        raise ValueError(f"{name}: adjust_mth must precede income_start_mth: a start-date "
                         f"adjustment is a deferral option; it does not at point_id {bad}")
    start = moved.where(adjust.notna(), start)
    for column, option in (("accel_mth", "payment acceleration"),
                           ("commute_mth", "commutation")):
        bad = table.index[options[column] < start].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or the income start month "
                             f"in force or later: {option} is a payout-phase option; it "
                             f"is not at point_id {bad}")
    apart = (options["accel_mth"] - options["commute_mth"]).abs()
    bad = table.index[apart < 6].tolist()
    if bad:
        raise ValueError(f"{name}: accel_mth and commute_mth must fall six months apart or "
                         f"more, the product's interlock between its two payout options; "
                         f"they do not at point_id {bad}")
    flag = table["joint"].astype(str).str.strip().str.lower()
    joint = flag.isin(["true", "1", "1.0"])
    bad = table.index[~(joint | flag.isin(["false", "0", "0.0"]))].tolist()
    if bad:
        raise ValueError(f"{name}: joint must be True or False, a flag; it is not at "
                         f"point_id {bad}")
    checked["joint"] = joint
    bad = table.index[~(table["sex"].isin(["M", "F"])
                        & (table["joint_sex"].isin(["M", "F"]) | ~joint))].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F, and so must joint_sex on a joint "
                         f"contract; it is not at point_id {bad}")
    every = pd.Series(True, index=table.index)                       # noqa: F821
    for column, what, read, least in (
            ("issue_age", "a whole number of years, 0 or more", every, 0),
            ("joint_age", "a whole number of years, 0 or more, on a joint contract",
             joint, 0),
            ("certain_period", "a whole number of years, 0 or more", every, 0),
            ("frequency", "a whole number of payments a year", every, None),
            ("issue_year", "a whole number, a calendar year", every, None)):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        whole = value % 1 == 0
        if least is not None:
            whole = whole & (value >= least)
        bad = table.index[read & ~whole].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be {what}; it is not at point_id "
                             f"{bad}")
        checked[column] = value
    digits = pd.to_numeric(table["purchase_rate_dp"], errors="coerce")  # noqa: F821
    bad = table.index[~(table["purchase_rate_dp"].isna()
                        | ((digits % 1 == 0) & (digits >= 0)))].tolist()
    if bad:
        raise ValueError(f"{name}: purchase_rate_dp must be blank, for full precision, "
                         f"or a whole number of decimal places, 0 or more; it is not at "
                         f"point_id {bad}")
    checked["purchase_rate_dp"] = digits
    for column, what, most in (("survivor_pct", "a probability, 0 to 1", 1.0),
                               ("cola_rate", "a number, zero or more", None),
                               ("other_qlac_premium", "a number, zero or more", None)):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        if most is None:
            ok = (value >= 0) & (value < float("inf"))
        else:
            ok = (value >= 0) & (value <= most)
        bad = table.index[~ok].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be {what}; it is not at point_id "
                             f"{bad}")
        checked[column] = value
    frac = pd.to_numeric(table["commute_frac"], errors="coerce")     # noqa: F821
    bad = table.index[~(table["commute_frac"].isna()
                        | ((frac >= 0) & (frac <= 1)))].tolist()
    if bad:
        raise ValueError(f"{name}: commute_frac must be blank or a fraction, 0 to 1; it "
                         f"is not at point_id {bad}")
    checked["commute_frac"] = frac
    bad = table.index[joint & (table["factor_basis"] == "table")].tolist()
    if bad:
        raise ValueError(f"{name}: factor_basis must be formula on a joint contract: the "
                         f"table basis, equation (1), factors a single life's survival "
                         f"out of the payout factor; it is not at point_id {bad}")
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
    for column in ("lives_if_init_1", "lives_if_init_2"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v <= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a probability, 0 to 1; it is "
                             f"not at point_id {bad}")
    for column in ("cum_premium_pp_init", "annual_income_init"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    column = "guarantee_mths_pricing_init"
    v = values[column]
    bad = table.index[~(table[column].isna()
                        | ((v >= 0) & (v < float("inf"))))].tolist()
    if bad:
        raise ValueError(f"{name}: {column} must be blank or a number of months, zero or "
                         f"more; it is not at point_id {bad}")
    for column in ("surv_to_payout_init", "commute_weight_init"):
        v = values[column]
        bad = table.index[~(table[column].isna() | ((v >= 0) & (v <= 1)))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a probability, 0 to 1; "
                             f"it is not at point_id {bad}")
    shift = values["ref_rate_shift_init"]
    bad = table.index[~((shift > -float("inf")) & (shift < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: ref_rate_shift_init must be a number, the change in "
                         f"the reference rate since issue; it is not at point_id {bad}")
    bad = table.index[~joint & (values["lives_if_init_2"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: lives_if_init_2 must be 0 on a single-life "
                         f"contract, which covers no second life; it is not at "
                         f"point_id {bad}")
    issued = months <= 0
    for column, at_issue in (("lives_if_init_1", 1.0),
                             ("lives_if_init_2", joint.astype(float)),
                             ("cum_premium_pp_init", 0.0),
                             ("annual_income_init", 0.0),
                             ("ref_rate_shift_init", 0.0)):
        bad = table.index[issued & (values[column] != at_issue)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must hold its value at issue on a "
                             f"contract not yet in force, duration_mth 0 or less: each "
                             f"covered life alive, no premium paid, no income bought and "
                             f"no change in the reference rate; it does not at point_id "
                             f"{bad}")
    in_force = months > 0
    refund = in_force & table["income_form"].isin(["CR", "IR"])
    given = table["guarantee_mths_pricing_init"].notna()
    bad = table.index[refund & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: guarantee_mths_pricing_init must be given on a "
                         f"contract in force on a refund form, income_form CR or IR, "
                         f"whose premiums still due the kernel prices with it; it is "
                         f"blank at point_id {bad}")
    bad = table.index[~refund & given].tolist()
    if bad:
        raise ValueError(f"{name}: guarantee_mths_pricing_init must be blank unless the "
                         f"contract is in force on a refund form: on new business the "
                         f"kernel derives it from the premium schedule, and the other "
                         f"forms fix it; it is not at point_id {bad}")
    paying = months > start
    given = table["surv_to_payout_init"].notna()
    bad = table.index[paying & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: surv_to_payout_init must be given on a contract past "
                         f"its income start month in force; it is blank at point_id "
                         f"{bad}")
    bad = table.index[~paying & given].tolist()
    if bad:
        raise ValueError(f"{name}: surv_to_payout_init must be blank unless duration_mth "
                         f"is after the income start month in force, where the "
                         f"projection derives it; it is not at point_id {bad}")
    commuted = options["commute_mth"] < months
    given = table["commute_weight_init"].notna()
    bad = table.index[commuted & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: commute_weight_init must be given on a contract whose "
                         f"commutation month precedes the valuation date; it is blank "
                         f"at point_id {bad}")
    bad = table.index[~commuted & given].tolist()
    if bad:
        raise ValueError(f"{name}: commute_weight_init must be blank unless the "
                         f"commutation month precedes the valuation date, where the "
                         f"projection derives it; it is not at point_id {bad}")
    weight, reached = values["commute_weight_init"], values["surv_to_payout_init"]
    bad = table.index[weight > reached].tolist()
    if bad:
        raise ValueError(f"{name}: commute_weight_init must be at most "
                         f"surv_to_payout_init: a commutation is taken in the income "
                         f"phase, by part of the cohort that reached it; it is not at "
                         f"point_id {bad}")
    l1, l2 = values["lives_if_init_1"], values["lives_if_init_2"]
    alive = (l1 + l2 - l1 * l2).where(joint, l1)
    for column in ("surv_to_payout_init", "commute_weight_init"):
        bad = table.index[values[column] < alive].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be at least the probability that a "
                             f"covered life is alive at the valuation date: the cohort "
                             f"it weighs includes every life still alive; it is not at "
                             f"point_id {bad}")
    for column, why in (("surv_to_payout_init", "a contract in force past its income "
                         "start month reached it"),
                        ("commute_weight_init", "a commutation is exercised by an owner "
                         "alive to exercise it")):
        bad = table.index[values[column] <= 0].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be above 0 where it is given: {why}, "
                             f"so the cohort it weighs is not empty; it is not at point_id "
                             f"{bad}")
    return table.assign(**checked)


def premium_schedule_table():
    """The premiums still due, from *premium_schedule_sec.csv*, checked as they are read.

    Long format, one row per premium slice, keyed by ``point_id`` - deliberately not
    indexed, so that selecting a contract's rows returns a DataFrame whether it has one
    slice or many - with ``DIA_US_S``'s columns: ``point_id``, ``slice``, ``premium_mth``,
    the policy month whose start the premium is paid at, ``premium_amt``, the amount per
    contract, and ``provenance``. The point key is the ``point_id`` column, and nothing else
    in the file names a point.

    It holds each contract's premiums **still due** at the valuation date, the premiums of
    policy months ``duration_mth`` and later, on a point in force, and its whole schedule on
    a point issued at or after the valuation date. A premium paid before the valuation date
    is in the contract's opening state, in ``cum_premium_pp_init`` and, through the slice it
    bought, ``annual_income_init``, so the schedule holds none.

    It is checked against :func:`model_point_table`, as checked, and the first check that
    fails raises ``ValueError``, naming the column, the label or every point at fault:

    * the ``point_id``, ``premium_mth`` and ``premium_amt`` columns are present;
    * each ``point_id`` is a whole number, a model point's label, below ``2**53`` in
      size, and labels a point of the model point table;
    * each ``premium_mth`` is a whole number of months, 0 or more, a policy month, read by
      value, so that ``60.0`` is 60, and below ``2**53``, which an int64 holds exactly;
      ``DIA_US_S`` takes ``int()`` of the raw month, so ``60.5`` is 60 there and text
      raises Python's own message;
    * each ``premium_amt`` is a number, zero or more;
    * no premium falls before the valuation date on a point in force, ``premium_mth``
      below ``duration_mth``: those paid are in the opening state;
    * no premium falls at or after the income start month in force. The product takes no
      premium within 13 months of it, and the projection's payout schedule rests on a
      level income from the income start month on, as ``DIA_US_S``'s refund base
      ``CP(T)`` does, which a premium after it would leave out;
    * every point buys an income: a point with no income bought by the valuation date,
      ``annual_income_init`` 0, has a positive premium due. ``DIA_US_S`` projects a point
      with no premium row silently, with no premium and no income.

    Returns the table with ``point_id`` and ``premium_mth`` as int64 and ``premium_amt``
    as float64, the numbers checked, every other column as read.  The three columns are
    passed to ``DataFrame.assign`` as ``**{...}``, since ``point_id`` is a cell of this
    Space, which the export would rewrite as a keyword.
    """
    name = premium_schedule_file                                     # noqa: F821
    points = model_point_table()
    tbl = pd.read_csv(input_dir() / name)                            # noqa: F821
    for column in ("point_id", "premium_mth", "premium_amt"):
        if column not in tbl.columns:
            raise ValueError(f"{name} has no {column} column")
    pid = pd.to_numeric(tbl["point_id"], errors="coerce")            # noqa: F821
    bad = tbl["point_id"][~(pid % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{name}: point_id must be a whole number, a model point's "
                         f"label; {bad} is not")
    bad = tbl["point_id"][~(pid.abs() < 2.0 ** 53)].tolist()
    if bad:
        raise ValueError(f"{name}: point_id must be below 2**53 in size, which an int64 "
                         f"holds exactly; {bad} is not")
    pid = pid.astype("int64")
    known = pid.isin(points.index)
    bad = sorted(set(pid[~known].tolist()))
    if bad:
        raise ValueError(f"{name}: point_id {bad} is no model point of "
                         f"{model_point_file}")                       # noqa: F821
    month = pd.to_numeric(tbl["premium_mth"], errors="coerce")       # noqa: F821
    bad = sorted(set(pid[~((month % 1 == 0) & (month >= 0))].tolist()))
    if bad:
        raise ValueError(f"{name}: premium_mth must be a whole number of months, 0 or "
                         f"more, a policy month; it is not at point_id {bad}")
    bad = sorted(set(pid[~(month < 2.0 ** 53)].tolist()))
    if bad:
        raise ValueError(f"{name}: premium_mth must be below 2**53 months, which an int64 "
                         f"holds exactly; it is not at point_id {bad}")
    amount = pd.to_numeric(tbl["premium_amt"], errors="coerce")      # noqa: F821
    bad = sorted(set(pid[~((amount >= 0) & (amount < float("inf")))].tolist()))
    if bad:
        raise ValueError(f"{name}: premium_amt must be a number, zero or more; it is "
                         f"not at point_id {bad}")
    duration = pid.map(points["duration_mth"])
    bad = sorted(set(pid[(duration > 0) & (month < duration)].tolist()))
    if bad:
        raise ValueError(f"{name}: a premium falls before the valuation date at point_id "
                         f"{bad}: those paid before it are in cum_premium_pp_init and "
                         f"annual_income_init, and the schedule holds the premiums still "
                         f"due")
    moved = points["adjust_mth"] >= 0
    start = points["adjust_start_mth"].where(moved, points["income_start_mth"])
    bad = sorted(set(pid[month >= pid.map(start)].tolist()))
    if bad:
        raise ValueError(f"{name}: a premium falls at or after the income start month in "
                         f"force at point_id {bad}: the income is level in payout")
    due = amount.groupby(pid).sum()
    bought = pd.to_numeric(points["annual_income_init"], errors="coerce")  # noqa: F821
    paying = due.reindex(points.index, fill_value=0.0) > 0
    bad = points.index[(bought == 0) & ~paying].tolist()
    if bad:
        raise ValueError(f"{name}: point_id {bad} buys no income: annual_income_init is 0 "
                         f"and no premium is due")
    return tbl.assign(**{"point_id": pid, "premium_mth": month.astype("int64"),
                         "premium_amt": amount.astype("float64")})


def mort_table():
    """The base annuitant mortality table by age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def improvement_scale():
    """The generational improvement scale by age and sex, from *improvement_scale.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / improvement_scale_file, index_col=["age", "sex"])  # noqa: F821


def payout_factor_table():
    """The illustrative payout annuity factors, from *payout_factor_table.csv*.

    Keyed by ``(income_start_age, sex, payout_form)``; the value is
    ``a^(m)_y(f; i_p)``, the APV at the income start age of $1 per annum of income.
    **[std]** - no insurer publishes payout factors for this product.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / payout_factor_file,                            # noqa: F821
        index_col=["income_start_age", "sex", "payout_form"])


def rop_factor_table():
    """The illustrative return-of-premium factors, from *rop_factor_table.csv*.

    Keyed by ``(issue_age, sex, deferral_years)``; the value is ``A_rop(x, d; i_p)``,
    the APV at the premium date of $1 payable at the end of the month of death within a
    ``d``-year deferral.  **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rop_factor_file,                               # noqa: F821
        index_col=["issue_age", "sex", "deferral_years"])


def mort_table_count():
    """The number of rows *mort_table.csv* gives a rate for, the table checked: an int.

    :func:`mort_table` reads the table as ``DIA_US_S`` reads it, and this cell checks it.
    The ``age`` key is read by value, once, as ``Projection.mort_rate_base_at``'s join
    matches it, so an age written ``70.0`` is 70. An age that is blank, text or not a whole
    number is refused, naming the file, the column and the lines it is on; so is a ``sex``
    that is not ``M`` or ``F``, the two values a model point's sex can take, a blank among
    them; so is an age and sex on more than one row, naming each with its lines; and so is
    a sex whose ages do not run one row an age, from its first to its last, the message
    naming each age missing. And so is a ``mort_rate`` that is blank, text, infinite or
    below 0, naming its lines: through the cap on mortality the rate reaches every
    survival probability, and a blank would survive the cap as a NaN, text fail far from
    here. A rate above 1 is accepted, and capped. ``Projection.mort_rate_base_at``, the
    table's one reader, asks for the count before it reads a rate, so a projection meets
    the checks first.  So is an age of ``2**53`` or more in size, which an int64 cannot be
    trusted to hold, or below 0, since :func:`mort_table_array` holds the table from age 0.
    """
    name = mort_table_file                                           # noqa: F821
    rows = mort_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = lines[(~(ages.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be below 2**53 in size, which an int64 holds "
                         f"exactly; it is not on line {bad}")
    bad = lines[(ages < 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be 0 or more, the table being held from age 0; "
                         f"it is not on line {bad}")
    bad = lines[(~rows["sex"].isin(["M", "F"])).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F; it is not on line {bad}")
    ages = ages.astype("int64")
    where = {}
    for line, key in zip(lines.tolist(), zip(ages.tolist(), rows["sex"].tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"age {key[0]}, sex {key[1]} is on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each age and sex must have one row; "
                         + "; ".join(repeated))
    missing = []
    for sex in sorted(set(rows["sex"])):
        run = sorted(set(ages[rows["sex"] == sex].tolist()))
        for a, b in zip(run, run[1:]):
            if b - a > 1:
                missing.append(f"no line holds age {a + 1}"
                               + (f" to {b - 1}" if b - a > 2 else "") + f" of sex {sex}")
    if missing:
        raise ValueError(f"{name}: the ages of each sex must run one row an age, without a "
                         f"gap; " + "; ".join(missing))
    rates = pd.to_numeric(rows["mort_rate"], errors="coerce")        # noqa: F821
    bad = lines[(~((rates >= 0) & (rates < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a finite number, zero or more; it is "
                         f"not on line {bad}")
    return int(len(rows))


def improvement_scale_count():
    """The number of rows *improvement_scale.csv* gives a rate for, the table checked.

    An int. :func:`improvement_scale` reads the scale as ``DIA_US_S`` reads it, and this
    cell checks its keys as :func:`mort_table_count` checks the mortality table's, for
    ``Projection.improvement_rate_at``'s join. And it refuses an ``improvement_rate`` that
    is blank, text, infinite, or 1 or more, naming its lines: at 1 or more ``1 - G2`` is
    zero or negative, and the improved rate is 0 or changes sign with the calendar year. A
    negative rate is a deterioration, which the generational basis projects as
    ``DIA_US_S`` does, the improved rate rising year on year, and it is accepted.
    ``Projection.improvement_rate_at``, the scale's one reader, asks for the count before
    it reads a rate, so a projection meets the checks first.  An age of ``2**53`` or more in
    size, or below 0, is refused as :func:`mort_table_count` refuses it.
    """
    name = improvement_scale_file                                    # noqa: F821
    rows = improvement_scale().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = lines[(~(ages.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be below 2**53 in size, which an int64 holds "
                         f"exactly; it is not on line {bad}")
    bad = lines[(ages < 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be 0 or more, the table being held from age 0; "
                         f"it is not on line {bad}")
    bad = lines[(~rows["sex"].isin(["M", "F"])).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F; it is not on line {bad}")
    ages = ages.astype("int64")
    where = {}
    for line, key in zip(lines.tolist(), zip(ages.tolist(), rows["sex"].tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"age {key[0]}, sex {key[1]} is on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each age and sex must have one row; "
                         + "; ".join(repeated))
    missing = []
    for sex in sorted(set(rows["sex"])):
        run = sorted(set(ages[rows["sex"] == sex].tolist()))
        for a, b in zip(run, run[1:]):
            if b - a > 1:
                missing.append(f"no line holds age {a + 1}"
                               + (f" to {b - 1}" if b - a > 2 else "") + f" of sex {sex}")
    if missing:
        raise ValueError(f"{name}: the ages of each sex must run one row an age, without a "
                         f"gap; " + "; ".join(missing))
    rates = pd.to_numeric(rows["improvement_rate"], errors="coerce")  # noqa: F821
    bad = lines[(~((rates > -float("inf")) & (rates < 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: improvement_rate must be a finite number below 1; it is "
                         f"not on line {bad}")
    return int(len(rows))


def payout_factor_count():
    """The number of rows *payout_factor_table.csv* gives a factor for, the table checked.

    An int. :func:`payout_factor_table` reads the table as ``DIA_US_S`` reads it, and this
    cell checks it for ``Projection.payout_factor``'s join, which reads one key a point. An
    ``income_start_age`` that is blank, text or not a whole number is refused, naming the
    file, the column and the lines it is on; so is a ``sex`` that is not ``M`` or ``F`` and
    a ``payout_form`` that is not ``LO``, ``CR``, ``IR`` or ``PC``, the forms the join
    reads, a blank among them; and so is a key on more than one row, naming each with its
    lines. And so is a ``payout_factor`` that is blank, text, infinite or not above zero,
    naming its lines: the factor divides the purchase rate, through
    ``Projection.annuity_factor_def``, where ``DIA_US_S``'s guard turns a factor of zero
    into a purchase rate of 0, a premium that buys nothing. ``Projection.payout_factor``
    asks for the count before it reads a factor, so a projection meets the checks first.
    An ``income_start_age`` of ``2**53`` or more in size, which an int64 cannot be trusted
    to hold, is refused too.
    """
    name = payout_factor_file                                        # noqa: F821
    rows = payout_factor_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["income_start_age"], errors="coerce")  # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: income_start_age must be a whole number; it is not on "
                         f"line {bad}")
    bad = lines[(~(ages.abs() < 2.0 ** 53)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: income_start_age must be below 2**53 in size, which an "
                         f"int64 holds exactly; it is not on line {bad}")
    for column, held, what in (("sex", ["M", "F"], "M or F"),
                               ("payout_form", ["LO", "CR", "IR", "PC"],
                                "LO, CR, IR or PC")):
        bad = lines[(~rows[column].isin(held)).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be {what}; it is not on line {bad}")
    where = {}
    for line, key in zip(lines.tolist(), zip(ages.astype("int64").tolist(),
                                             rows["sex"].tolist(),
                                             rows["payout_form"].tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"income_start_age {key[0]}, sex {key[1]}, payout_form "
                            f"{key[2]} is on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each income_start_age, sex and payout_form must have "
                         f"one row; " + "; ".join(repeated))
    factors = pd.to_numeric(rows["payout_factor"], errors="coerce")  # noqa: F821
    bad = lines[(~((factors > 0) & (factors < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: payout_factor must be a finite number above zero; it is "
                         f"not on line {bad}")
    return int(len(rows))


def rop_factor_count():
    """The number of rows *rop_factor_table.csv* gives a factor for, the table checked.

    An int. :func:`rop_factor_table` reads the table as ``DIA_US_S`` reads it, and this cell
    checks it for ``Projection.rop_factor``'s join, which reads one key a premium. An
    ``issue_age`` or a ``deferral_years`` that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on; so is a ``sex`` that is
    not ``M`` or ``F``, a blank among them; and so is a key on more than one row, naming
    each with its lines. And so is a ``rop_factor`` that is blank, text, infinite or below
    zero, naming its lines; zero is a return of premium that costs nothing.
    ``Projection.rop_factor`` asks for the count before it reads a factor, so a projection
    meets the checks first.  A key of ``2**53`` or more in size, which an int64 cannot be
    trusted to hold, is refused too.
    """
    name = rop_factor_file                                           # noqa: F821
    rows = rop_factor_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    whole = {}
    for column in ("issue_age", "deferral_years"):
        whole[column] = pd.to_numeric(rows[column], errors="coerce")  # noqa: F821
        bad = lines[(~(whole[column] % 1 == 0)).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a whole number; it is not on line "
                             f"{bad}")
        bad = lines[(~(whole[column].abs() < 2.0 ** 53)).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be below 2**53 in size, which an "
                             f"int64 holds exactly; it is not on line {bad}")
    bad = lines[(~rows["sex"].isin(["M", "F"])).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: sex must be M or F; it is not on line {bad}")
    where = {}
    for line, key in zip(lines.tolist(), zip(whole["issue_age"].astype("int64").tolist(),
                                             rows["sex"].tolist(),
                                             whole["deferral_years"].astype("int64")
                                             .tolist())):
        where.setdefault(key, []).append(line)
    repeated = []
    for key in sorted(where):
        if len(where[key]) > 1:
            repeated.append(f"issue_age {key[0]}, sex {key[1]}, deferral_years {key[2]} is "
                            f"on line {where[key]}")
    if repeated:
        raise ValueError(f"{name}: each issue_age, sex and deferral_years must have one "
                         f"row; " + "; ".join(repeated))
    factors = pd.to_numeric(rows["rop_factor"], errors="coerce")     # noqa: F821
    bad = lines[(~((factors >= 0) & (factors < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: rop_factor must be a finite number, zero or more; it is "
                         f"not on line {bad}")
    return int(len(rows))


def point_id():
    """The model points' labels, int64 by position: the table's ``point_id`` index.

    The label ``Projection.point_id`` reports for a position, and the one every refusal
    names.  Read by value, so that a label written ``3.0`` is 3, and refused when a label
    is first read, naming every label at fault, where one is not a whole number, text and
    a blank among them, or is ``2**53`` or more in size: the labels are the table's keys,
    as in the family's other compiled models.  A projection that names no point reads no
    label, and runs.
    """
    table = model_point_table()
    labels = pd.to_numeric(pd.Series(table.index), errors="coerce")  # noqa: F821
    bad = table.index[~(labels % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: point_id must be a whole "  # noqa: F821
                         f"number; {bad} is not")
    bad = table.index[~(labels.abs() < 2.0 ** 53).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: point_id must be below 2**53 "  # noqa: F821
                         f"in size; {bad} is not")
    return labels.to_numpy(dtype="int64")


def policy_count():
    """The ``policy_count`` column, float64 by point, as :func:`model_point_table` checked
    it."""
    return pd.to_numeric(model_point_table()["policy_count"]).to_numpy(  # noqa: F821
        dtype="float64")


def duration_mth():
    """The ``duration_mth`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`duration_mth_ok` is 0.

    :func:`model_point_table` has refused a value that is not a whole number, read by
    value, so that ``12.0`` is 12.
    """
    values = model_point_table()["duration_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def duration_mth_ok():
    """1 where ``int()`` reads the point's ``duration_mth`` below ``2**53`` in size.

    0 on a value ``int()`` refuses, a blank or text, and on a number the int64 vector
    cannot be trusted to hold; a number read as one, ``12.0``, is 12.
    """
    values = model_point_table()["duration_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = 1
    return out


def issue_age():
    """The ``issue_age`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`issue_age_ok` is 0."""
    values = model_point_table()["issue_age"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def issue_age_ok():
    """1 where ``int()`` reads the point's ``issue_age`` below ``2**53`` in size, as
    :func:`duration_mth_ok`."""
    values = model_point_table()["issue_age"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = 1
    return out


def joint_age():
    """The ``joint_age`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`joint_age_ok` is 0, a single-life point's blank among them."""
    values = model_point_table()["joint_age"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def joint_age_ok():
    """1 where ``int()`` reads the point's ``joint_age`` below ``2**53`` in size.

    As :func:`duration_mth_ok`.  A single-life point's blank is 0 here, and no projection
    of such a point reads it.
    """
    values = model_point_table()["joint_age"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = 1
    return out


def is_joint():
    """The ``joint`` column, int64 by point: 1 where :func:`model_point_table` checked it
    True."""
    values = model_point_table()["joint"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        out[i] = 1 if bool(values[i]) else 0
    return out


def survivor_pct():
    """The ``survivor_pct`` column, float64 by point, as :func:`model_point_table` checked
    it, a probability."""
    return pd.to_numeric(model_point_table()["survivor_pct"]).to_numpy(  # noqa: F821
        dtype="float64")


def certain_period():
    """The ``certain_period`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`certain_period_ok` is 0."""
    values = model_point_table()["certain_period"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def certain_period_ok():
    """1 where ``int()`` reads the point's ``certain_period`` below ``2**53`` in size, as
    :func:`duration_mth_ok`.  Only a period certain reads it."""
    values = model_point_table()["certain_period"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = 1
    return out


def income_start_mth():
    """The ``income_start_mth`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`income_start_mth_ok` is 0."""
    values = model_point_table()["income_start_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def income_start_mth_ok():
    """1 where ``int()`` reads the point's ``income_start_mth`` below ``2**53`` in size, as
    :func:`duration_mth_ok`."""
    values = model_point_table()["income_start_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = 1
    return out


def frequency():
    """The ``frequency`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`frequency_ok` is 0.

    Any whole number is held; ``Projection.payment_freq`` refuses one that is not 12, 4,
    2 or 1, with ``DIA_US_S``'s message.
    """
    values = model_point_table()["frequency"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def frequency_ok():
    """1 where ``int()`` reads the point's ``frequency`` below ``2**53`` in size, as
    :func:`duration_mth_ok`."""
    values = model_point_table()["frequency"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = 1
    return out


def cola_rate():
    """The ``cola_rate`` column, float64 by point, as :func:`model_point_table` checked it,
    a number zero or more."""
    return pd.to_numeric(model_point_table()["cola_rate"]).to_numpy(  # noqa: F821
        dtype="float64")


def issue_year():
    """The ``issue_year`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`issue_year_ok` is 0."""
    values = model_point_table()["issue_year"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def issue_year_ok():
    """1 where ``int()`` reads the point's ``issue_year`` below ``2**53`` in size, as
    :func:`duration_mth_ok`.  Only the generational basis and the calendar year read it."""
    values = model_point_table()["issue_year"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = 1
    return out


def purchase_rate_dp():
    """The ``purchase_rate_dp`` column, int64 by point: -1 where blank, for full precision,
    as ``Projection.purchase_rate_dp`` reads it at stage ``E``, ``int()`` of the value
    elsewhere, and 0 where :func:`purchase_rate_dp_ok` is 0."""
    values = model_point_table()["purchase_rate_dp"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v:
            out[i] = -1
        elif abs(v) < 2 ** 53:
            out[i] = int(v)
    return out


def purchase_rate_dp_ok():
    """1 where :func:`purchase_rate_dp` holds the point's value: blank, or below ``2**53``
    in size."""
    values = model_point_table()["purchase_rate_dp"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v or abs(v) < 2 ** 53:
            out[i] = 1
    return out


def adjust_mth():
    """The ``adjust_mth`` column, int64 by point: -1 where blank, for never, ``int()`` of
    the value elsewhere, and 0 where :func:`adjust_mth_ok` is 0."""
    values = model_point_table()["adjust_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v:
            out[i] = -1
        elif abs(v) < 2 ** 53:
            out[i] = int(v)
    return out


def adjust_mth_ok():
    """1 where :func:`adjust_mth` holds the point's month: blank, or below ``2**53`` in
    size."""
    values = model_point_table()["adjust_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v or abs(v) < 2 ** 53:
            out[i] = 1
    return out


def adjust_start_mth():
    """The ``adjust_start_mth`` column, int64 by point: -1 where blank, as
    :func:`adjust_mth`."""
    values = model_point_table()["adjust_start_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v:
            out[i] = -1
        elif abs(v) < 2 ** 53:
            out[i] = int(v)
    return out


def adjust_start_mth_ok():
    """1 where :func:`adjust_start_mth` holds the point's month: blank, or below ``2**53``
    in size."""
    values = model_point_table()["adjust_start_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v or abs(v) < 2 ** 53:
            out[i] = 1
    return out


def accel_mth():
    """The ``accel_mth`` column, int64 by point: -1 where blank, as :func:`adjust_mth`."""
    values = model_point_table()["accel_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v:
            out[i] = -1
        elif abs(v) < 2 ** 53:
            out[i] = int(v)
    return out


def accel_mth_ok():
    """1 where :func:`accel_mth` holds the point's month: blank, or below ``2**53`` in
    size."""
    values = model_point_table()["accel_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v or abs(v) < 2 ** 53:
            out[i] = 1
    return out


def commute_mth():
    """The ``commute_mth`` column, int64 by point: -1 where blank, as :func:`adjust_mth`."""
    values = model_point_table()["commute_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v:
            out[i] = -1
        elif abs(v) < 2 ** 53:
            out[i] = int(v)
    return out


def commute_mth_ok():
    """1 where :func:`commute_mth` holds the point's month: blank, or below ``2**53`` in
    size."""
    values = model_point_table()["commute_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v or abs(v) < 2 ** 53:
            out[i] = 1
    return out


def commute_frac():
    """The ``commute_frac`` column, float64 by point: 0.0 where blank, for none, as
    ``Projection.commute_frac`` reads it at stage ``E``."""
    values = model_point_table()["commute_frac"].tolist()
    out = np.zeros(len(values))                                      # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if v == v:
            out[i] = float(v)
    return out


def other_qlac_premium():
    """The ``other_qlac_premium`` column, float64 by point, as :func:`model_point_table`
    checked it."""
    return pd.to_numeric(model_point_table()["other_qlac_premium"]).to_numpy(  # noqa
        dtype="float64")


def lives_if_init_1():
    """The ``lives_if_init_1`` column, float64 by point: checked by
    :func:`model_point_table`."""
    return pd.to_numeric(model_point_table()["lives_if_init_1"]).to_numpy(  # noqa: F821
        dtype="float64")


def lives_if_init_2():
    """The ``lives_if_init_2`` column, float64 by point: checked by
    :func:`model_point_table`."""
    return pd.to_numeric(model_point_table()["lives_if_init_2"]).to_numpy(  # noqa: F821
        dtype="float64")


def cum_premium_pp_init():
    """The ``cum_premium_pp_init`` column, float64 by point: checked by
    :func:`model_point_table`."""
    return pd.to_numeric(model_point_table()["cum_premium_pp_init"]).to_numpy(  # noqa
        dtype="float64")


def annual_income_init():
    """The ``annual_income_init`` column, float64 by point: checked by
    :func:`model_point_table`."""
    return pd.to_numeric(model_point_table()["annual_income_init"]).to_numpy(  # noqa
        dtype="float64")


def guarantee_mths_pricing_init():
    """The ``guarantee_mths_pricing_init`` column, float64 by point, NaN where blank: given
    exactly on a refund form in force, as :func:`model_point_table` checks, and read only
    there."""
    column = model_point_table()["guarantee_mths_pricing_init"]
    return pd.to_numeric(column).to_numpy(dtype="float64")           # noqa: F821


def surv_to_payout_init():
    """The ``surv_to_payout_init`` column, float64 by point, NaN where blank: given exactly
    on a contract past its income start month, and read only there."""
    return pd.to_numeric(model_point_table()["surv_to_payout_init"]).to_numpy(  # noqa
        dtype="float64")


def commute_weight_init():
    """The ``commute_weight_init`` column, float64 by point, NaN where blank: given exactly
    where the commutation month precedes the valuation month, and read only there."""
    return pd.to_numeric(model_point_table()["commute_weight_init"]).to_numpy(  # noqa
        dtype="float64")


def ref_rate_shift_init():
    """The ``ref_rate_shift_init`` column, float64 by point: checked by
    :func:`model_point_table`."""
    return pd.to_numeric(model_point_table()["ref_rate_shift_init"]).to_numpy(  # noqa
        dtype="float64")


def has_market_type():
    """1 where the point's ``market_type`` is one of ``DIA_US_S``'s four, compared
    exactly."""
    return model_point_table()["market_type"].isin(
        ["NQ", "TradIRA", "RothIRA", "QLAC"]).to_numpy(dtype="int64")


def is_qlac():
    """1 where the point's ``market_type`` is ``QLAC``."""
    return (model_point_table()["market_type"] == "QLAC").to_numpy(dtype="int64")


def has_income_form():
    """1 where the point's ``income_form`` is one of ``DIA_US_S``'s five, compared
    exactly."""
    return model_point_table()["income_form"].isin(
        ["LO", "LO_ROP", "CR", "IR", "PC"]).to_numpy(dtype="int64")


def is_life_only():
    """1 where the point's ``income_form`` is ``LO`` or ``LO_ROP``, life only in payout."""
    f = model_point_table()["income_form"]
    return ((f == "LO") | (f == "LO_ROP")).to_numpy(dtype="int64")


def is_cash_refund():
    """1 where the point's ``income_form`` is ``CR``."""
    return (model_point_table()["income_form"] == "CR").to_numpy(dtype="int64")


def is_installment_refund():
    """1 where the point's ``income_form`` is ``IR``."""
    return (model_point_table()["income_form"] == "IR").to_numpy(dtype="int64")


def is_period_certain():
    """1 where the point's ``income_form`` is ``PC``."""
    return (model_point_table()["income_form"] == "PC").to_numpy(dtype="int64")


def has_db_form():
    """1 where the point's ``db_form`` is ``ROP`` or ``NONE``."""
    return model_point_table()["db_form"].isin(["ROP", "NONE"]).to_numpy(dtype="int64")


def is_rop():
    """1 where the point's ``db_form`` is ``ROP``."""
    return (model_point_table()["db_form"] == "ROP").to_numpy(dtype="int64")


def has_timing():
    """1 where the point's ``timing`` is ``arrears`` or ``advance``."""
    return model_point_table()["timing"].isin(["arrears", "advance"]).to_numpy(
        dtype="int64")


def is_arrears():
    """1 where the point's ``timing`` is ``arrears``."""
    return (model_point_table()["timing"] == "arrears").to_numpy(dtype="int64")


def has_reduction_trigger():
    """1 where the point's ``reduction_trigger`` is ``either`` or ``primary``."""
    return model_point_table()["reduction_trigger"].isin(
        ["either", "primary"]).to_numpy(dtype="int64")


def is_trigger_either():
    """1 where the point's ``reduction_trigger`` is ``either``."""
    return (model_point_table()["reduction_trigger"] == "either").to_numpy(dtype="int64")


def has_mort_basis():
    """1 where the point's ``mort_basis`` is ``anchor`` or ``generational``."""
    return model_point_table()["mort_basis"].isin(
        ["anchor", "generational"]).to_numpy(dtype="int64")


def is_generational():
    """1 where the point's ``mort_basis`` is ``generational``."""
    return (model_point_table()["mort_basis"] == "generational").to_numpy(dtype="int64")


def has_factor_basis():
    """1 where the point's ``factor_basis`` is ``table`` or ``formula``."""
    return model_point_table()["factor_basis"].isin(["table", "formula"]).to_numpy(
        dtype="int64")


def is_formula_basis():
    """1 where the point's ``factor_basis`` is ``formula``."""
    return (model_point_table()["factor_basis"] == "formula").to_numpy(dtype="int64")


def mort_sexes():
    """*mort_table.csv*'s sexes, an int: the number of schedules, the table checked first.

    :func:`mort_table_count` checks the table as stage ``E`` did, and refuses an age of
    ``2**53`` or more in size or below 0, naming its lines; this asks it first, so that
    every array, extent and schedule of the table, each of which asks this, meets the
    checks.  Each sex is a schedule, numbered in sorted order from 1.
    """
    mort_table_count()
    return int(mort_table().reset_index()["sex"].nunique())


def mort_table_array():
    """*mort_table.csv*'s rates, float64 by schedule and attained age, ``[s, x]``.

    Schedule ``s`` is the ``s``-th of the table's sexes in sorted order, from 1; row 0, and
    every age below a sex's first, is NaN padding, which ``Projection.mort_rate_base_at``
    never reads, since it checks the age against :func:`mort_age_first` and
    :func:`mort_age_last` first.
    """
    n = mort_sexes()
    rows = mort_table().reset_index()
    rows = rows.assign(age=pd.to_numeric(rows["age"]).astype("int64"))  # noqa: F821
    out = np.full((n + 1, int(rows["age"].max()) + 1), np.nan)       # noqa: F821
    s = 0
    for _, part in rows.groupby("sex", sort=True):
        s += 1
        out[s, part["age"].to_numpy()] = pd.to_numeric(              # noqa: F821
            part["mort_rate"]).to_numpy(dtype="float64")
    return out


def mort_age_first():
    """Each mortality schedule's first age, int64 by schedule: 1 on schedule 0."""
    out = np.ones(mort_sexes() + 1, dtype="int64")                  # noqa: F821
    rows = mort_table().reset_index()
    rows = rows.assign(age=pd.to_numeric(rows["age"]).astype("int64"))  # noqa: F821
    s = 0
    for _, part in rows.groupby("sex", sort=True):
        s += 1
        out[s] = int(part["age"].min())
    return out


def mort_age_last():
    """Each mortality schedule's last age, int64 by schedule: 0 on schedule 0, so that no
    age lies between its extents."""
    out = np.zeros(mort_sexes() + 1, dtype="int64")                 # noqa: F821
    rows = mort_table().reset_index()
    rows = rows.assign(age=pd.to_numeric(rows["age"]).astype("int64"))  # noqa: F821
    s = 0
    for _, part in rows.groupby("sex", sort=True):
        s += 1
        out[s] = int(part["age"].max())
    return out


def mort_schedule_1():
    """The mortality schedule of each point's ``sex``, int64 by point.

    The sex's number in :func:`mort_table_array`, matched as ``DIA_US_S``'s ``.loc``
    matches it, and 0 where the table lacks it, which ``Projection.mort_rate_base_at``
    refuses where it first reads schedule 0.
    """
    mort_sexes()
    keys = sorted(mort_table().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def mort_schedule_2():
    """The mortality schedule of each point's ``joint_sex``, int64 by point, as
    :func:`mort_schedule_1`: 0 on a single-life point's blank, which nothing reads."""
    mort_sexes()
    keys = sorted(mort_table().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["joint_sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def improvement_sexes():
    """*improvement_scale.csv*'s sexes, an int: the number of schedules, the scale checked
    first by :func:`improvement_scale_count`, and numbered by its own sexes, as
    :func:`mort_sexes` numbers the mortality table's: the two need not hold the same
    ones."""
    improvement_scale_count()
    return int(improvement_scale().reset_index()["sex"].nunique())


def improvement_array():
    """*improvement_scale.csv*'s rates, float64 by schedule and attained age, ``[s, x]``,
    padded as :func:`mort_table_array` is."""
    n = improvement_sexes()
    rows = improvement_scale().reset_index()
    rows = rows.assign(age=pd.to_numeric(rows["age"]).astype("int64"))  # noqa: F821
    out = np.full((n + 1, int(rows["age"].max()) + 1), np.nan)       # noqa: F821
    s = 0
    for _, part in rows.groupby("sex", sort=True):
        s += 1
        out[s, part["age"].to_numpy()] = pd.to_numeric(              # noqa: F821
            part["improvement_rate"]).to_numpy(dtype="float64")
    return out


def improvement_age_first():
    """Each improvement schedule's first age, int64 by schedule: 1 on schedule 0."""
    out = np.ones(improvement_sexes() + 1, dtype="int64")           # noqa: F821
    rows = improvement_scale().reset_index()
    rows = rows.assign(age=pd.to_numeric(rows["age"]).astype("int64"))  # noqa: F821
    s = 0
    for _, part in rows.groupby("sex", sort=True):
        s += 1
        out[s] = int(part["age"].min())
    return out


def improvement_age_last():
    """Each improvement schedule's last age, int64 by schedule: 0 on schedule 0."""
    out = np.zeros(improvement_sexes() + 1, dtype="int64")          # noqa: F821
    rows = improvement_scale().reset_index()
    rows = rows.assign(age=pd.to_numeric(rows["age"]).astype("int64"))  # noqa: F821
    s = 0
    for _, part in rows.groupby("sex", sort=True):
        s += 1
        out[s] = int(part["age"].max())
    return out


def improvement_schedule_1():
    """The improvement schedule of each point's ``sex``, int64 by point, numbered by the
    scale's own sexes, as :func:`mort_schedule_1` by the table's."""
    improvement_sexes()
    keys = sorted(improvement_scale().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def improvement_schedule_2():
    """The improvement schedule of each point's ``joint_sex``, int64 by point, as
    :func:`improvement_schedule_1`."""
    improvement_sexes()
    keys = sorted(improvement_scale().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["joint_sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def payout_income_start_age():
    """*payout_factor_table.csv*'s ``income_start_age``, int64 by row, in the file's order.

    Read by value, as :func:`payout_factor_count`, asked first, checked it, so that an age
    written ``80.0`` is 80.  ``Projection.payout_factor`` scans the rows for its key.
    """
    payout_factor_count()
    rows = payout_factor_table().reset_index()
    return pd.to_numeric(rows["income_start_age"]).to_numpy(dtype="int64")  # noqa: F821


def payout_sex():
    """*payout_factor_table.csv*'s ``sex``, int64 by row, numbered by the table's own sexes
    in sorted order from 1, as :func:`payout_schedule` numbers a point's."""
    payout_factor_count()
    rows = payout_factor_table().reset_index()
    keys = sorted(rows["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = rows["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number[sexes[i]]
    return out


def payout_form_code():
    """*payout_factor_table.csv*'s ``payout_form``, int64 by row: LO 1, CR 2, IR 3 and PC
    4, the forms :func:`payout_factor_count` admits, which ``Projection.payout_factor``
    numbers from the decodes."""
    payout_factor_count()
    rows = payout_factor_table().reset_index()
    number = {"LO": 1, "CR": 2, "IR": 3, "PC": 4}
    forms = rows["payout_form"].tolist()
    out = np.zeros(len(forms), dtype="int64")                        # noqa: F821
    for i in range(len(forms)):
        out[i] = number[forms[i]]
    return out


def payout_factor_value():
    """*payout_factor_table.csv*'s ``payout_factor``, float64 by row, as
    :func:`payout_factor_count` checked it."""
    payout_factor_count()
    rows = payout_factor_table().reset_index()
    return pd.to_numeric(rows["payout_factor"]).to_numpy(dtype="float64")  # noqa: F821


def payout_schedule():
    """Each point's ``sex`` in *payout_factor_table.csv*'s numbering, int64 by point.

    As :func:`payout_sex` numbers the table's rows, and 0 where the table lacks the sex,
    which matches no row, so ``Projection.payout_factor`` refuses it on the table basis.
    """
    payout_factor_count()
    keys = sorted(payout_factor_table().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def rop_issue_age():
    """*rop_factor_table.csv*'s ``issue_age``, int64 by row, in the file's order, read by
    value as :func:`rop_factor_count`, asked first, checked it."""
    rop_factor_count()
    rows = rop_factor_table().reset_index()
    return pd.to_numeric(rows["issue_age"]).to_numpy(dtype="int64")  # noqa: F821


def rop_sex():
    """*rop_factor_table.csv*'s ``sex``, int64 by row, numbered by the table's own sexes in
    sorted order from 1, as :func:`rop_schedule` numbers a point's."""
    rop_factor_count()
    rows = rop_factor_table().reset_index()
    keys = sorted(rows["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = rows["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number[sexes[i]]
    return out


def rop_deferral_years():
    """*rop_factor_table.csv*'s ``deferral_years``, int64 by row, read by value as
    :func:`rop_factor_count` checked it."""
    rop_factor_count()
    rows = rop_factor_table().reset_index()
    return pd.to_numeric(rows["deferral_years"]).to_numpy(dtype="int64")  # noqa: F821


def rop_factor_value():
    """*rop_factor_table.csv*'s ``rop_factor``, float64 by row, as :func:`rop_factor_count`
    checked it."""
    rop_factor_count()
    rows = rop_factor_table().reset_index()
    return pd.to_numeric(rows["rop_factor"]).to_numpy(dtype="float64")  # noqa: F821


def rop_schedule():
    """Each point's ``sex`` in *rop_factor_table.csv*'s numbering, int64 by point, 0 where
    the table lacks it, as :func:`payout_schedule`."""
    rop_factor_count()
    keys = sorted(rop_factor_table().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def premium_width():
    """The width of the premium tables, an int: the schedule's latest policy month and one,
    no more than ``premium_last_mth`` and one, and 1 on a schedule with no row.

    :func:`premium_schedule_table`, asked first, checks the schedule.  ``premium_last_mth``,
    1,439, is the last policy month a premium of a point the compiled model's caches hold
    can fall in, ``12 * (Projection.omega_age - Projection.issue_age_min) - 1``, which this
    Space cannot read from ``Projection``: a test holds the two together.
    """
    tbl = premium_schedule_table()
    if len(tbl) == 0:
        return 1
    return min(int(tbl["premium_mth"].max()), premium_last_mth) + 1  # noqa: F821


def premium_array():
    """Each point's premiums still due, float64 by point and policy month, ``[i, k]``.

    The rows of each point of :func:`premium_schedule_table` sorted by ``premium_mth`` as
    ``DIA_US_S``'s ``premium_schedule`` sorts them, and each amount added in that order to
    its month's total from 0.0, as ``DIA_US_S``'s ``premium_by_mth`` adds it, so that a
    month with two rows holds ``DIA_US_S``'s float to the last bit.  0.0 in a month with no
    row, and on a point with none.  A row after :func:`premium_width`'s last month is not
    held: its point's income starts later than ``Projection.proj_len`` admits.
    """
    width = premium_width()
    table = model_point_table()
    labels = pd.to_numeric(pd.Series(table.index), errors="coerce").tolist()  # noqa: F821
    position = {}
    for i in range(len(labels)):
        position[labels[i]] = i
    out = np.zeros((len(labels), width))                             # noqa: F821
    for label, part in premium_schedule_table().groupby("point_id", sort=False):
        i = position[label]
        part = part.sort_values("premium_mth")
        months = part["premium_mth"].tolist()
        amounts = part["premium_amt"].tolist()
        for j in range(len(months)):
            if months[j] < width:
                out[i, months[j]] = out[i, months[j]] + float(amounts[j])
    return out


def premium_rows():
    """The number of rows of each point's schedule in each policy month, int64 by point and
    policy month, ``[i, k]``, as :func:`premium_array` holds them.

    ``DIA_US_S``'s ``premium_by_mth`` holds a key for every month with a row, a premium of
    0.0 among them, and its pricing guarantee visits each, so ``Projection`` visits a month
    with a row, not a month with a positive premium.
    """
    width = premium_width()
    table = model_point_table()
    labels = pd.to_numeric(pd.Series(table.index), errors="coerce").tolist()  # noqa: F821
    position = {}
    for i in range(len(labels)):
        position[labels[i]] = i
    out = np.zeros((len(labels), width), dtype="int64")              # noqa: F821
    for label, part in premium_schedule_table().groupby("point_id", sort=False):
        i = position[label]
        months = part["premium_mth"].tolist()
        for j in range(len(months)):
            if months[j] < width:
                out[i, months[j]] = out[i, months[j]] + 1
    return out


def premium_last():
    """Each point's last policy month with a row of the schedule, int64 by point: -1 on a
    point with none, and no later than :func:`premium_width`'s last month."""
    width = premium_width()
    table = model_point_table()
    labels = pd.to_numeric(pd.Series(table.index), errors="coerce").tolist()  # noqa: F821
    position = {}
    for i in range(len(labels)):
        position[labels[i]] = i
    out = np.full(len(labels), -1, dtype="int64")                   # noqa: F821
    for label, part in premium_schedule_table().groupby("point_id", sort=False):
        i = position[label]
        months = part["premium_mth"].tolist()
        for j in range(len(months)):
            if out[i] < months[j] < width:
                out[i] = months[j]
    return out


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

premium_schedule_file = "premium_schedule_sec.csv"

mort_table_file = "mort_table.csv"

improvement_scale_file = "improvement_scale.csv"

payout_factor_file = "payout_factor_table.csv"

rop_factor_file = "rop_factor_table.csv"

future_horizon_mth = 120

premium_last_mth = 1439

np = ("Module", "numpy")

pd = ("Module", "pandas")