# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.SPIA_US_SEC.Projection` as ``data``. :mod:`~.SPIA_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/immediate_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``SPIA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Three of the tables are SPIA_US_S's.** The mortality table, the improvement scale and
the surrender-charge scale are the files :mod:`~.SPIA_US_S` reads, read here in place: one
copy of each table serves both models, so an edit to one reaches both. The model point
table is this model's own, ``model_point_table_sec.csv``; it sits beside
``SPIA_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

========================  ==============================  ==========================
Reference                 Cells                           File
========================  ==============================  ==========================
model_point_file          model_point_table()             model_point_table_sec.csv
mort_table_file           mort_table()                    mort_table.csv
improvement_scale_file    improvement_scale()             improvement_scale.csv
surr_charge_file          surr_charge_table()             surr_charge_table.csv
========================  ==============================  ==========================

**The model point table is checked as it is read.** Six of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the four columns of a contract's opening state, each
covered life's survival at the valuation date, the commutation fraction taken by then and
the 10-year CMT's change since the annuity date. :func:`model_point_table` refuses a
table that lacks any of them, repeats a ``point_id``, holds a count, a duration or a month
of death no contract can have, or holds an opening state no contract can be in. The checks
run in turn, and the first that fails raises, naming the missing column or every point
that fails it. It also refuses an annuity to commence more than ``future_horizon_mth``
months after the valuation date, 120 months as shipped: future new business is written
over a stated horizon, so that no frame runs longer than the stop rule from the annuity
date plus that horizon. Set to 0, the Reference refuses future new business altogether.
Whether a contract still owes a payment at the valuation date is a rule of the product
rather than of the table, and ``Projection.proj_len`` checks it.

**So is the surrender-charge scale.** :func:`surr_charge_scale` reads its policy years by
value, once, and refuses a year that is not a whole number, a gap, a repeat or a blank
rate, naming the file; ``Projection.surr_charge_rate`` takes the scale's first and last
years and its rates from there, never from the raw column.

The two mortality tables are keyed by ``(age, sex)`` and the surrender-charge table by
``policy_year``. They are separate files on purpose: the technical notes require the
best-estimate basis to be the **2012 IAM Basic** table projected with **Projection Scale
G2**, two distinct objects with distinct provenance, and neither may be embedded in the
model — the shipped tables are illustrative **[std]** stand-ins. To swap in a licensed
basis, replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file``
at a different name before the model computes anything. No formula changes. The
improvement scale is swappable the same way, which is how the notes' first sensitivity —
a 50% / 150% scaling of tabulated improvement — is run. Replacing a file changes
:mod:`~.SPIA_US_S` too, which reads the same one.

**The vectors.** The readers return what the files hold, and no
:mod:`~.SPIA_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them.
The others read the arrays below instead, one element at a time, a
model point's attribute being the element at its position, ``data.premium()[idx]``. That
is what lets the model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a
numpy vector or table of int64 or float64, which compiles to a typed memoryview, never one
of bools, objects or text, and each check of a table is an int. Each model point column a
projection reads is one vector of the column's own name, read element by element as
``SPIA_US_S`` reads the point's value, ``float()`` of an amount or a rate, ``int()`` of an
age, a month count or a year, ``bool()`` of a flag; and where a point's value can be one
its projection cannot use, a 0/1 vector beside it, ``<column>_ok``, says whether it is
usable. The text the projection branches on is decoded into 0/1 flags, each with a
``has_*`` flag that says the value is one ``SPIA_US_S`` names. The mortality table and the
improvement scale, keyed by age and sex, are tabled by schedule, one per sex, and age,
padded from age 0, each point carrying the schedule of each life's sex; the surrender
charges are a vector by policy year, padded from year 0:

===================================  =======  =================  ==========================
Cells                                dtype    Shape              From
===================================  =======  =================  ==========================
point_id()                           int64    [point]            the table's index
policy_count()                       float64  [point]            ``policy_count``
duration_mth(), duration_mth_ok()    int64    [point]            ``duration_mth``
premium()                            float64  [point]            ``premium``
premium_ok()                         int64    [point]            ``premium``, its flag
premium_tax_rate()                   float64  [point]            ``premium_tax_rate``
premium_tax_rate_ok()                int64    [point]            ``premium_tax_rate``, its
                                                                 flag
annual_income()                      float64  [point]            ``annual_income``
annual_income_ok()                   int64    [point]            ``annual_income``, its
                                                                 flag
cola_rate()                          float64  [point]            ``cola_rate``
cola_rate_ok()                       int64    [point]            ``cola_rate``, its flag
survivor_pct()                       float64  [point]            ``survivor_pct``
survivor_pct_ok()                    int64    [point]            ``survivor_pct``, its flag
rating_factor()                      float64  [point]            ``rating_factor``
rating_factor_ok()                   int64    [point]            ``rating_factor``, its
                                                                 flag
primary_age(), primary_age_ok()      int64    [point]            ``primary_age``
joint_age(), joint_age_ok()          int64    [point]            ``joint_age``
certain_months()                     int64    [point]            ``certain_months``
certain_months_ok()                  int64    [point]            ``certain_months``, its
                                                                 flag
frequency(), frequency_ok()          int64    [point]            ``frequency``
annuity_year(), annuity_year_ok()    int64    [point]            ``annuity_year``
is_joint()                           int64    [point]            ``joint``, 1 on True
commutation_enabled()                int64    [point]            the column, 1 on True
issue_state_excludes_withdrawal()    int64    [point]            the column, 1 on True
qualified()                          int64    [point]            the column, 1 on True
has_form()                           int64    [point]            ``form``, 1 on one of five
is_period_certain()                  int64    [point]            ``form``, 1 on
                                                                 life_certain or
                                                                 certain_only
is_certain_only()                    int64    [point]            ``form``, 1 on
                                                                 certain_only
is_cash_refund()                     int64    [point]            ``form``, 1 on cash_refund
is_installment_refund()              int64    [point]            ``form``, 1 on
                                                                 installment_refund
has_reduction_trigger()              int64    [point]            ``reduction_trigger``, 1
                                                                 on either or primary
is_trigger_either()                  int64    [point]            the same, 1 on either
has_timing()                         int64    [point]            ``timing``, 1 on arrears
                                                                 or advance
is_arrears()                         int64    [point]            the same, 1 on arrears
has_mort_basis()                     int64    [point]            ``mort_basis``, 1 on table
                                                                 or scenario
is_scenario()                        int64    [point]            the same, 1 on scenario
death_mth_1(), death_mth_1_ok()      int64    [point]            ``death_mth_1``, -1 where
                                                                 blank
death_mth_2(), death_mth_2_ok()      int64    [point]            ``death_mth_2``, -1 where
                                                                 blank
lives_if_init_1()                    float64  [point]            ``lives_if_init_1``
lives_if_init_2()                    float64  [point]            ``lives_if_init_2``
commute_frac_cum_init()              float64  [point]            the column
cmt10_shift_init()                   float64  [point]            the column
mort_sexes()                         int      scalar             *mort_table.csv*, checked
mort_table_array()                   float64  [schedule, age]    *mort_table.csv*
mort_age_first(), mort_age_last()    int64    [schedule]         *mort_table.csv*
mort_schedule_1()                    int64    [point]            ``primary_sex``, joined; 0
                                                                 where not
mort_schedule_2()                    int64    [point]            ``joint_sex``, joined; 0
                                                                 where not
improvement_sexes()                  int      scalar             *improvement_scale.csv*,
                                                                 checked
improvement_array()                  float64  [schedule, age]    *improvement_scale.csv*
improvement_age_first()              int64    [schedule]         *improvement_scale.csv*
improvement_age_last()               int64    [schedule]         *improvement_scale.csv*
improvement_schedule_1()             int64    [point]            ``primary_sex``, joined; 0
                                                                 where not
improvement_schedule_2()             int64    [point]            ``joint_sex``, joined; 0
                                                                 where not
surr_charge_rate_array()             float64  [policy_year]      :func:`surr_charge_scale`
surr_charge_year_first()             int      scalar             :func:`surr_charge_scale`
surr_charge_year_last()              int      scalar             :func:`surr_charge_scale`
===================================  =======  =================  ==========================

Each table is numbered by its own sexes, in sorted order, from schedule 1, so the two
tables need not hold the same sexes: :func:`mort_sexes` and :func:`improvement_sexes`, each
the table's one check, an int, give the count. Schedule 0 is a row of padding whose first
age is 1 and whose last is 0, so that no age lies between them: a life whose sex a table
lacks, a blank among them, has schedule 0 there, and ``Projection``'s reader of the table
refuses it, naming the point, the age and the life, at the first age it reads, as
``SPIA_US_S``'s ``.loc`` raised ``KeyError`` there. A point on the scenario basis, or a
single-life point's second life, never reads it. :func:`surr_charge_scale` stays the
scale's checked DataFrame, as at stage ``E``, and the vector and its two extents are read
from it.

**An array is read by element, never whole,** in this Space as in
:mod:`~.SPIA_US_SEC.Projection`. The compiler types an array cell as a memoryview only once
it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python
object. So an array derived here reads the table's column, and a width comes from a table
or a check's int, never from another cell's array. Each age table's check is one int cell
that its array, its extents and its schedules read first, so that a projection, which
reads an extent first, meets the same refusal as a reader of the array. The column
keywords of :func:`model_point_table`'s ``DataFrame.assign`` are passed as ``**{...}``,
since a keyword named as a cell of this Space, ``death_mth_1``, would be rewritten by the
export.

**What a point's projection cannot use is refused where it reads it,** by the point's own
``Projection`` cell, naming the point, never here: no point is refused for another's
value, nor for a column its projection never reads, so that the model projects every
point ``SPIA_US_S`` projects to a number, as at stage ``E`` (D2). Where a vector cannot hold
a value, the vector holds 0 or NaN there and its ``_ok`` flag 0, and the
:mod:`~.SPIA_US_SEC.Projection` accessor that reads the element raises:

* text in a column of numbers, which ``SPIA_US_S``'s ``float()`` or ``int()`` refuses in
  the same cell, on every point that reads it;
* a blank, which ``int()`` refuses, in an age, a month count, a frequency or a year, as
  in ``SPIA_US_S``: a blank ``joint_age`` on a single-life point, a blank
  ``certain_months`` on a form without an elected period and a blank ``annuity_year`` on
  the scenario basis are read by no projection, and refused only by a direct call;
* an int of ``2**53`` or more in size, which an int64 cannot be trusted to hold
  (below), in those columns and in ``duration_mth`` and the two death months;
* a blank or infinite amount or rate on a point whose projection reads it through a
  ``max``, a ``min`` or a comparison that would turn the missing value into a number, as
  ``SPIA_US_S``'s would: the premium on a cash or installment refund, whose refund
  balance is ``max(0, P - G)`` and whose refund period a search ``G(k) >= P``; the first
  year's income and the COLA rate on every point, whose instalments every projection
  pays and its refund, its refund period and its withdrawal's floor read through such a
  ``max``, ``min`` or search; the survivor percentage on a joint contract of the four
  forms with a life contingency, whose payment factor the certain floor's ``max`` reads;
  and the rating factor on the table basis, whose mortality the same ``max`` reads in the
  end.
  Elsewhere a blank stays NaN, as ``SPIA_US_S`` reads it, and so does every blank
  ``premium_tax_rate``, which only ``Projection.premium_net_pp`` reads, in a product.

That is the family's cap rule (USLIB-SEC-PLAN.md §7.1), applied by point: a point
``SPIA_US_S`` projects to a number only because a ``max`` or a ``min`` lost its missing
value is refused, in its projection, and no other. A fraction in an int column truncates,
as ``SPIA_US_S``'s ``int()`` does, so a frequency written 12.5 is monthly. A text value of
``form``, ``reduction_trigger``, ``timing`` or ``mort_basis`` that is none of
``SPIA_US_S``'s values sets no ``has_*`` flag, and the decode that reads the flag raises
``SPIA_US_S``'s message there, as at stage ``E``; the values are compared exactly, case and
whitespace included, as ``SPIA_US_S`` compares them. A flag column is ``bool()`` of each
element as pandas reads it, as ``SPIA_US_S``'s ``bool(model_point()[...])`` is, so a blank
reads as True there too. What the table's own checks refuse, :func:`model_point_table`
refuses for the whole table, as at stage ``E``, and :func:`point_id` refuses a label that
is not a whole number below ``2**53``, naming every label at fault, when a label is first
read: they are the table's keys and its in-force interface.

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is usable only below ``2**53`` in
size, where the int64 holds ``SPIA_US_S``'s reading of it exactly; past it the flag is 0.

**The large extract.** :func:`model_point_table` reads the file whole, not in chunks
(``low_memory=False``), so that pandas infers each column's type once: read in chunks, a
table of thousands of single lives with a joint point among them typed ``joint_sex`` chunk
by chunk and warned (``DtypeWarning``), though the frame was the same.
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

    Indexed by ``point_id``. Six columns are the in-force interface: ``policy_count``,
    the contracts the point stands for, and ``duration_mth``, the months elapsed from the
    annuity date at the valuation date, as in ``basiclife.BasicTerm_SE``; then the opening
    state, per contract, as it stands at the start of month 0, before any month-0 event:

    * ``lives_if_init_1`` and ``lives_if_init_2``: each covered life's probability of
      being alive at the valuation date, 1 or 0 on a real record, where a joint contract
      may carry one life already dead, and 0 for the second life of a single-life
      contract;
    * ``commute_frac_cum_init``: the cumulative commutation fraction applying in month 0,
      before any month-0 withdrawal;
    * ``cmt10_shift_init``: the 10-year CMT at the valuation date less the 10-year CMT at
      the annuity date, as a decimal, which moves the commutation discount rate.

    The rest are ``SPIA_US_S``'s, ``pols_if_init`` renamed ``policy_count``, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the six in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months, read by value, so that ``12.0`` is
      12: positive for a contract in payment, 0 for one whose annuity date is the
      valuation date, negative for one commencing later;
    * no annuity commences more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * ``lives_if_init_1`` and ``lives_if_init_2`` are probabilities, 0 to 1;
    * ``commute_frac_cum_init`` is a number, 0 or more and below 1;
    * ``cmt10_shift_init`` is a number, of either sign;
    * a single-life contract has no second life: ``lives_if_init_2`` is 0;
    * a contract not yet in payment, ``duration_mth`` 0 or less, holds its values at
      the annuity date: each covered life 1, no commutation and no change in the CMT;
    * each month of death, ``death_mth_1`` and ``death_mth_2``, is blank or a whole
      number of months, read by value, so that ``13.0`` is 13 and a fraction or text is
      refused, on every basis. The table is returned with the two columns as the numbers
      they were checked as, which is what ``Projection.death_mth`` reads;
    * on the scenario basis, each life's opening status is its death month's: 1 while
      the life survives to the valuation date, ``death_mth`` blank, negative or
      ``duration_mth`` or later, as ``Projection.death_mth`` and ``Projection.lives_if``
      read it, and 0 once it has died. So the scenario's step function, which
      ``lives_if`` follows after the valuation date, agrees with the opening value at it;
    * a commutation fraction appears only where a commutation could have been taken
      before the valuation date: the contract holds the right, its issue state allows
      it, it has a certain period, an elected one or an installment refund's, and
      ``duration_mth`` is 13 or more, the first withdrawal being taken in policy month 12
      and reducing the instalments from month 13. That is a necessary condition only: the
      check cannot see an installment refund's derived period, which needs the projection,
      nor whether a certain period long enough for a withdrawal remained, and it does not
      ask whether the model's own utilization assumption would have taken one, since a
      real record's withdrawals do not depend on it.

    Whether the contract still owes a payment at the valuation date needs the certain
    period, which an installment refund derives in ``Projection``, so
    ``Projection.proj_len`` checks it.

    The file is read whole, ``low_memory=False``, so that pandas types each column once,
    not chunk by chunk, which on a large extract warned and changed nothing.  The two
    death columns are returned through ``**{...}``, since their names are cells of this
    Space, which the export would rewrite as keywords.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id",    # noqa: F821
                        low_memory=False)
    state = ("lives_if_init_1", "lives_if_init_2", "commute_frac_cum_init",
             "cmt10_shift_init")
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
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
    for column in ("lives_if_init_1", "lives_if_init_2"):
        v = values[column]
        bad = table.index[~((v >= 0) & (v <= 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a probability, 0 to 1; it is "
                             f"not at point_id {bad}")
    theta = values["commute_frac_cum_init"]
    bad = table.index[~((theta >= 0) & (theta < 1))].tolist()
    if bad:
        raise ValueError(f"{name}: commute_frac_cum_init must be a number, 0 or more "
                         f"and below 1; it is not at point_id {bad}")
    shift = values["cmt10_shift_init"]
    bad = table.index[~((shift > -float("inf")) & (shift < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: cmt10_shift_init must be a number, the change in the "
                         f"10-year CMT since the annuity date; it is not at point_id {bad}")
    joint = table["joint"].astype(bool)
    bad = table.index[~joint & (values["lives_if_init_2"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: lives_if_init_2 must be 0 on a single-life "
                         f"contract, which covers no second life; it is not at "
                         f"point_id {bad}")
    issued = months <= 0
    for column, at_issue in (("lives_if_init_1", 1.0),
                             ("lives_if_init_2", joint.astype(float)),
                             ("commute_frac_cum_init", 0.0),
                             ("cmt10_shift_init", 0.0)):
        bad = table.index[issued & (values[column] != at_issue)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must hold its value at issue on a "
                             f"contract not yet in force, duration_mth 0 or less: each "
                             f"covered life alive, no commutation taken and no change in "
                             f"the CMT; it does not at point_id {bad}")
    deaths = {}
    for life in (1, 2):
        column = f"death_mth_{life}"
        death = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~(table[column].isna() | (death % 1 == 0))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a whole number of "
                             f"months, a policy month; it is not at point_id {bad}")
        deaths[life] = death
    scenario = table["mort_basis"] == "scenario"
    for life in (1, 2):
        death = deaths[life]
        alive = death.isna() | (death < 0) | (death >= months)
        covered = joint if life == 2 else pd.Series(True, index=table.index)  # noqa: F821
        want = alive.astype(float).where(covered, 0.0)
        column = f"lives_if_init_{life}"
        bad = table.index[scenario & (values[column] != want)].tolist()
        if bad:
            raise ValueError(f"{name}: on the scenario basis {column} must be 1 while "
                             f"the life survives to the valuation date, death_mth_{life} "
                             f"blank, negative or duration_mth or later, and 0 once it "
                             f"has died; it is not at point_id {bad}")
    form = table["form"]
    certain = (form.isin(["life_certain", "certain_only"])
               & (pd.to_numeric(table["certain_months"], errors="coerce") > 0)  # noqa: F821
               | (form == "installment_refund"))
    may = (table["commutation_enabled"].astype(bool)
           & ~table["issue_state_excludes_withdrawal"].astype(bool)
           & certain & (months >= 13))
    bad = table.index[(theta > 0) & ~may].tolist()
    if bad:
        raise ValueError(f"{name}: commute_frac_cum_init must be 0 unless a commutation "
                         f"could have been taken before the valuation date: the right "
                         f"held, the issue state allowing it, a certain period, and "
                         f"duration_mth 13 or more; it is not at point_id {bad}")
    return table.assign(**{"death_mth_1": deaths[1], "death_mth_2": deaths[2]})


def mort_table():
    """The base annuitant mortality table by age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def improvement_scale():
    """The generational improvement scale by age and sex, from *improvement_scale.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / improvement_scale_file, index_col=["age", "sex"])  # noqa: F821


def surr_charge_table():
    """The commutation surrender-charge scale by contract year, *surr_charge_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="policy_year")     # noqa: F821


def surr_charge_scale():
    """The surrender-charge scale by contract year, as :func:`surr_charge_table` reads it,
    checked.

    The rates of *surr_charge_table.csv*, indexed by its policy years read by value, as
    ``SPIA_US_S``'s lookup matches them, so that a year written ``2.0`` is year 2.
    ``Projection.surr_charge_rate`` takes the scale's first and last years and its rates
    from here, so the extents and the values come from one checked column. A year that is
    not a whole number, text and a blank among them, is refused, naming every such year;
    so is a scale with no year, or whose years do not run from the first to the last
    without a gap or a repeat, from year 1 on, each with a rate. ``SPIA_US_S`` takes
    ``int()`` of the raw years for the extents, so a year written ``x`` raises Python's own
    message there, and one written ``3a`` turns the years to text and makes every lookup
    miss.
    """
    file = surr_charge_file                                          # noqa: F821
    tbl = surr_charge_table()
    if len(tbl) == 0:
        raise ValueError(f"{file} has no policy year")
    years = pd.to_numeric(pd.Series(tbl.index), errors="coerce")     # noqa: F821
    bad = tbl.index[~(years % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{file}: a policy year must be a whole number; {bad} is not")
    whole = years.astype("int64").tolist()
    first, last = min(whole), max(whole)
    rates = pd.to_numeric(tbl["surr_charge_rate"], errors="coerce")  # noqa: F821
    if (first < 1 or sorted(whole) != list(range(first, last + 1))
            or rates.isna().any()):
        raise ValueError(f"{file}: the policy years must run from {first} to {last} "
                         f"without a gap or a repeat, from 1 on, each with a rate")
    return pd.DataFrame(                                             # noqa: F821
        {"surr_charge_rate": rates.to_numpy(dtype="float64")},
        index=pd.Index(whole, name="policy_year"))                   # noqa: F821



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
    return model_point_table()["policy_count"].to_numpy(dtype="float64")


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
    """1 where ``int()`` reads the point's ``duration_mth`` below ``2**53`` in size, as
    :func:`primary_age_ok`: 0 on a blank, and on text, ``"12.0"`` among them in a column
    pandas reads as text, which ``int()`` refuses; a number read as one, ``12.0``, is 12."""
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


def premium():
    """The ``premium`` column, float64 by point: ``float()`` of each value, NaN on text."""
    values = model_point_table()["premium"].tolist()
    out = np.full(len(values), np.nan)                               # noqa: F821
    for i in range(len(values)):
        try:
            out[i] = float(values[i])
        except (TypeError, ValueError):
            pass
    return out


def premium_ok():
    """1 where the point's projection may read its ``premium``.

    0 on text, which ``float()`` refuses, and on a blank or infinite premium on a cash or
    installment refund, whose refund balance ``max(0, P - G)`` and refund period
    ``G(k) >= P`` would turn it into a number.  A blank stays NaN on the other forms, which
    read it only in ``Projection.premium_net_pp``, as ``SPIA_US_S`` does.
    """
    table = model_point_table()
    values = table["premium"].tolist()
    forms = table["form"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = float(values[i])
        except (TypeError, ValueError):
            continue
        if abs(v) < float("inf") or not (forms[i] == "cash_refund"
                                          or forms[i] == "installment_refund"):
            out[i] = 1
    return out


def premium_tax_rate():
    """The ``premium_tax_rate`` column, float64 by point: ``float()`` of each value, NaN on
    text."""
    values = model_point_table()["premium_tax_rate"].tolist()
    out = np.full(len(values), np.nan)                               # noqa: F821
    for i in range(len(values)):
        try:
            out[i] = float(values[i])
        except (TypeError, ValueError):
            pass
    return out


def premium_tax_rate_ok():
    """1 where ``float()`` reads the point's ``premium_tax_rate``: 0 on text alone.

    A blank stays NaN, as ``SPIA_US_S`` reads it: only ``Projection.premium_net_pp``, which
    no report reaches, reads the rate.
    """
    values = model_point_table()["premium_tax_rate"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            float(values[i])
        except (TypeError, ValueError):
            continue
        out[i] = 1
    return out


def annual_income():
    """The ``annual_income`` column, B(1), float64 by point: ``float()`` of each value, NaN
    on text."""
    values = model_point_table()["annual_income"].tolist()
    out = np.full(len(values), np.nan)                               # noqa: F821
    for i in range(len(values)):
        try:
            out[i] = float(values[i])
        except (TypeError, ValueError):
            pass
    return out


def annual_income_ok():
    """1 where the point's ``annual_income`` is a finite number: 0 on text, a blank and an
    infinity.

    Every projection pays its instalments, and its refund, its refund period and its
    withdrawal's residual floor read them through a ``max``, a ``min`` or a search that
    would turn a missing income into a number.
    """
    values = model_point_table()["annual_income"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = float(values[i])
        except (TypeError, ValueError):
            continue
        if abs(v) < float("inf"):
            out[i] = 1
    return out


def cola_rate():
    """The ``cola_rate`` column, float64 by point: ``float()`` of each value, NaN on
    text."""
    values = model_point_table()["cola_rate"].tolist()
    out = np.full(len(values), np.nan)                               # noqa: F821
    for i in range(len(values)):
        try:
            out[i] = float(values[i])
        except (TypeError, ValueError):
            pass
    return out


def cola_rate_ok():
    """1 where the point's ``cola_rate`` is a finite number: 0 on text, a blank and an
    infinity.

    It compounds every instalment past the first policy year, which the projection reads
    as :func:`annual_income_ok` says.
    """
    values = model_point_table()["cola_rate"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = float(values[i])
        except (TypeError, ValueError):
            continue
        if abs(v) < float("inf"):
            out[i] = 1
    return out


def survivor_pct():
    """The ``survivor_pct`` column, float64 by point: ``float()`` of each value, NaN on
    text."""
    values = model_point_table()["survivor_pct"].tolist()
    out = np.full(len(values), np.nan)                               # noqa: F821
    for i in range(len(values)):
        try:
            out[i] = float(values[i])
        except (TypeError, ValueError):
            pass
    return out


def survivor_pct_ok():
    """1 where the point's projection may read its ``survivor_pct``.

    0 on text, and on a blank or infinite percentage on a joint contract of the four forms
    with a life contingency, whose payment factor, ``max(C, L)``, would turn a missing one
    into a number.  A single-life contract and a certain_only one never read it.
    """
    table = model_point_table()
    values = table["survivor_pct"].tolist()
    joint = table["joint"].tolist()
    forms = table["form"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = float(values[i])
        except (TypeError, ValueError):
            continue
        if (abs(v) < float("inf") or not bool(joint[i])
                or forms[i] == "certain_only"):
            out[i] = 1
    return out


def rating_factor():
    """The ``rating_factor`` column, float64 by point: ``float()`` of each value, NaN on
    text."""
    values = model_point_table()["rating_factor"].tolist()
    out = np.full(len(values), np.nan)                               # noqa: F821
    for i in range(len(values)):
        try:
            out[i] = float(values[i])
        except (TypeError, ValueError):
            pass
    return out


def rating_factor_ok():
    """1 where the point's projection may read its ``rating_factor``.

    0 on text, and on a blank or infinite factor on the table basis, whose survival the
    payment factor's ``max(C, L)`` reads in the end: the mortality caps put their bound
    second, so a missing rating stays missing there, and the ``max`` would turn it into a
    number.  The scenario basis never reads it.
    """
    table = model_point_table()
    values = table["rating_factor"].tolist()
    basis = table["mort_basis"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = float(values[i])
        except (TypeError, ValueError):
            continue
        if abs(v) < float("inf") or not basis[i] == "table":
            out[i] = 1
    return out


def primary_age():
    """The ``primary_age`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`primary_age_ok` is 0."""
    values = model_point_table()["primary_age"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def primary_age_ok():
    """1 where ``int()`` reads the point's ``primary_age`` below ``2**53`` in size.

    0 on text, a blank and an infinity, which ``SPIA_US_S``'s ``int()`` refuses, and on a
    number the int64 vector cannot be trusted to hold.  A fraction truncates, as ``int()``
    does.
    """
    values = model_point_table()["primary_age"].tolist()
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

    As :func:`primary_age_ok`.  A single-life point's blank is 0 here, and no projection
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


def certain_months():
    """The ``certain_months`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`certain_months_ok` is 0."""
    values = model_point_table()["certain_months"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def certain_months_ok():
    """1 where ``int()`` reads the point's ``certain_months`` below ``2**53`` in size.

    As :func:`primary_age_ok`.  Only a form with an elected certain period reads it.
    """
    values = model_point_table()["certain_months"].tolist()
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
    2 or 1, with ``SPIA_US_S``'s message.
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
    :func:`primary_age_ok`."""
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


def annuity_year():
    """The ``annuity_year`` column, int64 by point: ``int()`` of each value, 0 where
    :func:`annuity_year_ok` is 0."""
    values = model_point_table()["annuity_year"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        try:
            v = int(values[i])
        except (TypeError, ValueError, OverflowError):
            continue
        if abs(v) < 2 ** 53:
            out[i] = v
    return out


def annuity_year_ok():
    """1 where ``int()`` reads the point's ``annuity_year`` below ``2**53`` in size.

    As :func:`primary_age_ok`.  Only the table basis reads it, to date improvement.
    """
    values = model_point_table()["annuity_year"].tolist()
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
    """The ``joint`` column, int64 by point: 1 where ``bool()`` of the value is True."""
    values = model_point_table()["joint"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        out[i] = 1 if bool(values[i]) else 0
    return out


def commutation_enabled():
    """The ``commutation_enabled`` column, int64 by point: 1 where ``bool()`` of the value
    is True."""
    values = model_point_table()["commutation_enabled"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        out[i] = 1 if bool(values[i]) else 0
    return out


def issue_state_excludes_withdrawal():
    """The ``issue_state_excludes_withdrawal`` column, int64 by point: 1 where ``bool()``
    of the value is True."""
    values = model_point_table()["issue_state_excludes_withdrawal"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        out[i] = 1 if bool(values[i]) else 0
    return out


def qualified():
    """The ``qualified`` column, int64 by point: 1 where ``bool()`` of the value is True."""
    values = model_point_table()["qualified"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        out[i] = 1 if bool(values[i]) else 0
    return out


def has_form():
    """1 where the point's ``form`` is one of ``SPIA_US_S``'s five, compared exactly."""
    f = model_point_table()["form"]
    return f.isin(["life_only", "life_certain", "cash_refund", "installment_refund",
                   "certain_only"]).to_numpy(dtype="int64")


def is_period_certain():
    """1 where the point's ``form`` is ``life_certain`` or ``certain_only``."""
    f = model_point_table()["form"]
    return ((f == "life_certain") | (f == "certain_only")).to_numpy(dtype="int64")


def is_certain_only():
    """1 where the point's ``form`` is ``certain_only``."""
    return (model_point_table()["form"] == "certain_only").to_numpy(dtype="int64")


def is_cash_refund():
    """1 where the point's ``form`` is ``cash_refund``."""
    return (model_point_table()["form"] == "cash_refund").to_numpy(dtype="int64")


def is_installment_refund():
    """1 where the point's ``form`` is ``installment_refund``."""
    return (model_point_table()["form"] == "installment_refund").to_numpy(dtype="int64")


def has_reduction_trigger():
    """1 where the point's ``reduction_trigger`` is ``either`` or ``primary``."""
    return model_point_table()["reduction_trigger"].isin(
        ["either", "primary"]).to_numpy(dtype="int64")


def is_trigger_either():
    """1 where the point's ``reduction_trigger`` is ``either``."""
    return (model_point_table()["reduction_trigger"] == "either").to_numpy(dtype="int64")


def has_timing():
    """1 where the point's ``timing`` is ``arrears`` or ``advance``."""
    return model_point_table()["timing"].isin(["arrears", "advance"]).to_numpy(
        dtype="int64")


def is_arrears():
    """1 where the point's ``timing`` is ``arrears``."""
    return (model_point_table()["timing"] == "arrears").to_numpy(dtype="int64")


def has_mort_basis():
    """1 where the point's ``mort_basis`` is ``table`` or ``scenario``."""
    return model_point_table()["mort_basis"].isin(["table", "scenario"]).to_numpy(
        dtype="int64")


def is_scenario():
    """1 where the point's ``mort_basis`` is ``scenario``."""
    return (model_point_table()["mort_basis"] == "scenario").to_numpy(dtype="int64")


def death_mth_1():
    """The primary's scenario month of death, int64 by point: -1 where blank.

    The ``death_mth_1`` column as :func:`model_point_table` checked it, a whole number of
    policy months or blank, the blank being ``SPIA_US_S``'s survivor, which
    ``Projection.death_mth`` reads as -1; 0 where :func:`death_mth_1_ok` is 0.
    """
    values = model_point_table()["death_mth_1"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v:
            out[i] = -1
        elif abs(v) < 2 ** 53:
            out[i] = int(v)
    return out


def death_mth_1_ok():
    """1 where :func:`death_mth_1` holds the point's month: blank, or below ``2**53``."""
    values = model_point_table()["death_mth_1"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v or abs(v) < 2 ** 53:
            out[i] = 1
    return out


def death_mth_2():
    """The joint annuitant's scenario month of death, int64 by point: -1 where blank, as
    :func:`death_mth_1`."""
    values = model_point_table()["death_mth_2"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v:
            out[i] = -1
        elif abs(v) < 2 ** 53:
            out[i] = int(v)
    return out


def death_mth_2_ok():
    """1 where :func:`death_mth_2` holds the point's month: blank, or below ``2**53``."""
    values = model_point_table()["death_mth_2"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        v = values[i]
        if not v == v or abs(v) < 2 ** 53:
            out[i] = 1
    return out


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


def commute_frac_cum_init():
    """The ``commute_frac_cum_init`` column, float64 by point: checked by
    :func:`model_point_table`."""
    return pd.to_numeric(model_point_table()["commute_frac_cum_init"]).to_numpy(  # noqa
        dtype="float64")


def cmt10_shift_init():
    """The ``cmt10_shift_init`` column, float64 by point: checked by
    :func:`model_point_table`."""
    return pd.to_numeric(model_point_table()["cmt10_shift_init"]).to_numpy(  # noqa: F821
        dtype="float64")


def mort_sexes():
    """*mort_table.csv*'s check, an int: the number of its sexes, each a schedule.

    The table is read by value, as ``SPIA_US_S``'s ``.loc`` matches its keys, and refused,
    naming the file and every line at fault, where an age is not a whole number, text and
    a blank among them, a sex is blank, or a rate is not a finite number; and, naming the
    sex, where one sex's ages do not run from its first to its last without a gap or a
    repeat, or one is negative, since the table is held from age 0.  ``SPIA_US_S`` raised
    ``KeyError`` only where a projection read a missing key, and read a blank rate as NaN.
    Every array, extent and schedule of the table reads this first.
    """
    name = mort_table_file                                           # noqa: F821
    rows = mort_table().reset_index()
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = (rows.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = (rows.index[rows["sex"].isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: sex must not be blank; it is on line {bad}")
    rates = pd.to_numeric(rows["mort_rate"], errors="coerce")        # noqa: F821
    bad = (rows.index[~(rates.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: mort_rate must be a finite number; it is not on line "
                         f"{bad}")
    rows = rows.assign(age=ages.astype("int64"))
    for sex, part in rows.groupby("sex", sort=True):
        a = part["age"].tolist()
        if min(a) < 0 or sorted(a) != list(range(min(a), max(a) + 1)):
            raise ValueError(f"{name}: the ages of sex {sex} must run from {min(a)} to "
                             f"{max(a)} without a gap or a repeat, none negative")
    return int(rows["sex"].nunique())


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
    """The mortality schedule of each point's ``primary_sex``, int64 by point.

    The sex's number in :func:`mort_table_array`, matched as ``SPIA_US_S``'s ``.loc``
    matches it, and 0 where the table lacks it, a blank among them: a point on the
    scenario basis never reads the table, and one on the table basis is refused where
    ``Projection.mort_rate_base_at`` first reads schedule 0.
    """
    mort_sexes()
    keys = sorted(mort_table().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["primary_sex"].tolist()
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
    """*improvement_scale.csv*'s check, an int: the number of its sexes, each a schedule.

    The scale is read and refused as :func:`mort_sexes` reads and refuses the mortality
    table, and numbered by its own sexes: the two tables need not hold the same ones.
    """
    name = improvement_scale_file                                    # noqa: F821
    rows = improvement_scale().reset_index()
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = (rows.index[~(ages % 1 == 0)] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
    bad = (rows.index[rows["sex"].isna()] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: sex must not be blank; it is on line {bad}")
    rates = pd.to_numeric(rows["improvement_rate"], errors="coerce")  # noqa: F821
    bad = (rows.index[~(rates.abs() < float("inf"))] + 2).tolist()
    if bad:
        raise ValueError(f"{name}: improvement_rate must be a finite number; it is not "
                         f"on line {bad}")
    rows = rows.assign(age=ages.astype("int64"))
    for sex, part in rows.groupby("sex", sort=True):
        a = part["age"].tolist()
        if min(a) < 0 or sorted(a) != list(range(min(a), max(a) + 1)):
            raise ValueError(f"{name}: the ages of sex {sex} must run from {min(a)} to "
                             f"{max(a)} without a gap or a repeat, none negative")
    return int(rows["sex"].nunique())


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
    """The improvement schedule of each point's ``primary_sex``, int64 by point, numbered
    by the scale's own sexes, as :func:`mort_schedule_1` by the table's."""
    improvement_sexes()
    keys = sorted(improvement_scale().reset_index()["sex"].unique())
    number = {}
    for i in range(len(keys)):
        number[keys[i]] = i + 1
    sexes = model_point_table()["primary_sex"].tolist()
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


def surr_charge_rate_array():
    """The surrender-charge rates, float64 by policy year, from :func:`surr_charge_scale`.

    Indexed by the year itself, from 0, NaN below the scale's first year, which
    ``Projection.surr_charge_rate`` never reads: it clamps the year to
    :func:`surr_charge_year_first` and :func:`surr_charge_year_last` first, and the
    scale's check holds the first year to 1 or more.
    """
    scale = surr_charge_scale()
    out = np.full(int(scale.index.max()) + 1, np.nan)                # noqa: F821
    out[scale.index.to_numpy()] = scale["surr_charge_rate"].to_numpy(dtype="float64")
    return out


def surr_charge_year_first():
    """The surrender-charge scale's first policy year, an int, from
    :func:`surr_charge_scale`."""
    return int(surr_charge_scale().index.min())


def surr_charge_year_last():
    """The surrender-charge scale's last policy year, an int, from
    :func:`surr_charge_scale`."""
    return int(surr_charge_scale().index.max())


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

mort_table_file = "mort_table.csv"

improvement_scale_file = "improvement_scale.csv"

surr_charge_file = "surr_charge_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")

np = ("Module", "numpy")