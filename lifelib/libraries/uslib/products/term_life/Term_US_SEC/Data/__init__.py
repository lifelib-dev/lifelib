# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.Term_US_SEC.Projection` as ``data``. :mod:`~.Term_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized
Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/term_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Four of the tables are Term_US_S's.** The premium schedule, the mortality table, the
class factors and the shock-lapse buckets are the files :mod:`~.Term_US_S` reads, read
here in place: one copy of each table serves both models, so an edit to one reaches
both. The model point table is this model's own, ``model_point_table_sec.csv``; it sits
beside ``Term_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
premium_rates_file      premium_rates()             premium_rates.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
shock_lapse_file        shock_lapse_table()         shock_lapse_table.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Two of its columns are the
in-force interface, ``policy_count`` and ``duration_mth``, and :func:`model_point_table`
refuses a table that lacks either, repeats a ``point_id``, or holds a count or a
duration no policy can have. The checks run in turn, and the first that fails raises,
naming the missing column or every point that fails it. It also refuses a policy to be
issued more than ``future_horizon_mth`` months after the valuation date, 120 months as
shipped: future new business is written over a stated horizon, so that no frame runs
longer than cover from issue plus that horizon. Set to 0, the Reference refuses future
new business altogether. A longer horizon projects in modelx, but the compiled model's
caches are sized for the shipped 120 months (``spec_sec.py``): it needs ``t`` there raised
to 12 x 77 + the horizon + 2 and a rebuild, or a frame longer than 1,044 months raises
``IndexError`` compiled, naming nothing, at the first month past the caches. Whether a
point is still in cover at the valuation date, and whether the contract issues it, are
rules of the product rather than of the table, and ``Projection.proj_len`` checks them,
against three Projection References the caches are sized from as they are from the
horizon: ``expiry_age``, ``issue_age_min`` and ``policy_term_min``.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache. No formula
changes. A compiled model clears no cache, so there the name is set on a package just
imported, before anything is read.

**The vectors.** The readers return what the files hold, and no
:mod:`~.Term_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them.
The others read the arrays below instead, one element at a time, a model point's
attribute being the element at its position, ``data.age_at_entry()[idx]``. That is what
lets the model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy
vector or table of int64 or float64, which compiles to a typed memoryview, never one of
bools, objects or text, and each count of buckets or extent of a table is an int.

Text the projection needs is decoded here, into the number it selects: the plan into the
level period, the premium mode into the months between instalments, the underwriting
class into its mortality factor, and the face amount into its band. A blank M(1)
override becomes a 0/1 flag beside a value, so no NaN reaches a formula. And each table
keyed by more than a number becomes an integer-indexed array. The premium schedules,
keyed by plan, sex, class and band, are numbered, each point carrying the number of its
own, and tabled by schedule and policy year. The mortality table is padded from age 0, so
that the index is the attained age:

==============================  =======  =============  =================================
Cells                           dtype    Shape          From
==============================  =======  =============  =================================
point_id()                      int64    [point]        the table's index
age_at_entry()                  int64    [point]        ``age_at_entry``
sum_assured()                   float64  [point]        ``sum_assured``
policy_count()                  float64  [point]        ``policy_count``
duration_mth()                  int64    [point]        ``duration_mth``
policy_term()                   int64    [point]        ``plan``, decoded
prem_cycle()                    int64    [point]        ``premium_mode``, decoded
band()                          int64    [point]        ``sum_assured``, banded
class_factor()                  float64  [point]        ``rate_class``, joined
plt_mort_factor_override()      float64  [point]        the override, 0.0 where blank
has_plt_mort_factor_override()  int64    [point]        1 where given, 0 where blank
premium_schedule()              int64    [point]        plan, sex, class and band, joined
premium_schedules()             int      scalar         *premium_rates.csv*, checked
premium_rates_array()           float64  [schedule, y]  *premium_rates.csv*
premium_first_year()            int64    [schedule]     *premium_rates.csv*
premium_last_year()             int64    [schedule]     *premium_rates.csv*
mort_table_array()              float64  [age]          *mort_table.csv*
mort_age_first()                int      scalar         *mort_table.csv*
mort_age_last()                 int      scalar         *mort_table.csv*
shock_lapse_buckets()           int      scalar         *shock_lapse_table.csv*
shock_lapse_jump_lo()           float64  [bucket]       *shock_lapse_table.csv*
shock_lapse_jump_hi()           float64  [bucket]       *shock_lapse_table.csv*
shock_lapse_bucket_rate()       float64  [bucket]       *shock_lapse_table.csv*
==============================  =======  =============  =================================

**An array is read by element, never whole,** in this Space as in
:mod:`~.Term_US_SEC.Projection`. The compiler types an array cell as a memoryview only
once it has seen that every use of it, in either Space, is an element read: one
``len()``, slice, loop over it or numpy call on it anywhere, and the cell compiles as a
Python object. So an array derived here from another reads the table's column, as
:func:`band` reads ``sum_assured``, or the other cell element by element, as
:func:`premium_schedule` reads :func:`band`; and a width comes from a table, never from
another cell's array.

**What cannot be decoded is refused** when the array is first read, naming every point
at fault: a ``point_id`` that is not a whole number, a plan whose number of years ``int``
cannot read, a premium mode other than A, SA, Q or M, a class *class_factor_table.csv*
lacks. So is a table the arrays cannot hold: a premium schedule whose policy years are
not whole, leave a gap, repeat or start below 1; a mortality table with an age that is
not whole, a gap, a repeated or negative age; a shock-lapse table with no bucket.
``Term_US_S`` met each of these only when a projection reached it. A key written as a
float, a policy year ``1.0`` or an age ``35.0``, is read by its value, as ``Term_US_S``'s
lookups match it, and so is every key an extent is taken from: a key written as text is
not whole, and the table's extents refuse it as its array does. A read beyond a table's
extent is refused where ``Term_US_S``'s lookup raised ``KeyError``, by the one
:mod:`~.Term_US_SEC.Projection` cell that reads the table, naming the point:
``premium_pp_ann_py`` and ``mort_rate_base``.

**A value a capped rate, a min or a max reads is a finite number,** or it is refused
when its array is first read, naming the file, the column and every line or point at
fault. ``Projection.mort_rate`` caps the annual rate with ``min``, and the notes' M(1)
rule and the post-level-term grading bound theirs with ``min`` and ``max``. Each keeps
its first argument unless a later one compares smaller, or larger, and no comparison
with NaN holds, so each is written with the value first and the bound second, and a NaN
would stay NaN; but an infinity is a number, which the cap reads as 1, certain death. So
every value they read is checked, over its whole column, and a blank, text or infinite
one is refused: a factor of *class_factor_table.csv*, by ``rate_class``, whether or not
a point carries the class; a rate of *mort_table.csv*, by age; a premium of
*premium_rates.csv*, by schedule and policy year, whether or not a point carries the
schedule; an ``age_at_entry`` and a ``plt_mort_factor_override``, by ``point_id``. A blank
override is the notes' rule, and is left so, and so is the padding, which no formula reads.
``Term_US_S`` met each only when a projection reached it: it raised on text and on a blank
or infinite age, read an infinite factor, base rate or M(1) override as certain death at its
cap and a negative infinite override as its grading's floor, 2.0, without a word, and
projected NaN or an infinity from any other such value.
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

    Indexed by ``point_id``. Two columns are the in-force interface, as in
    ``basiclife.BasicTerm_SE``: ``policy_count``, and ``duration_mth``, the completed
    policy months at the valuation date. The rest are ``Term_US_S``'s, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * both in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    for column in ("policy_count", "duration_mth"):
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
    return table


def premium_rates():
    """The guaranteed premium schedule, read from *premium_rates.csv*.

    Keyed by the contractual, 1-based ``policy_year`` (1 = the issue year), not by the
    0-based projection index; ``Projection.premium_pp_ann_py(y)`` looks it up at policy
    year ``y``: ``premium_pp_ann(t)`` at ``policy_year(t) = duration(t) + 1``, the policy
    year containing month ``t``, and ``jump_ratio()`` at years ``n`` and ``n + 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / premium_rates_file,                            # noqa: F821
        index_col=["plan", "sex", "rate_class", "band", "policy_year"])


def mort_table():
    """The base mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(input_dir() / class_factor_file,             # noqa: F821
                       index_col="rate_class")


def shock_lapse_table():
    """The shock-lapse buckets by jump ratio, read from *shock_lapse_table.csv*."""
    return pd.read_csv(input_dir() / shock_lapse_file)               # noqa: F821


def point_id():
    """The ``point_id`` of every model point, in table order: int64 [point].

    ``Projection`` is indexed by position, ``idx``, so this is how a projection names its
    point: ``Projection.point_id()`` is the element at ``idx``, and every refusal quotes
    it. A label that is not a whole number is refused, naming every such label.
    """
    table = model_point_table()
    labels = pd.to_numeric(pd.Series(table.index), errors="coerce")  # noqa: F821
    bad = table.index[~(labels % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: point_id must be a whole number; "
                         f"{bad} is not")
    return labels.to_numpy(dtype="int64")


def age_at_entry():
    """The issue age (ANB) of every model point: int64 [point].

    Read as ``Term_US_S`` reads it, ``int`` of the number. The attained age it opens
    indexes *mort_table.csv*, whose rate ``Projection.mort_rate`` caps, so an age that is
    not a finite number, blank, text or infinite, is refused, naming every point that
    carries one: numpy would read a blank or infinite age as the least int64, without a
    word.
    """
    table = model_point_table()
    ages = pd.to_numeric(table["age_at_entry"], errors="coerce")     # noqa: F821
    bad = table.index[~((ages > -float("inf")) & (ages < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: age_at_entry must be a finite number; it "
                         f"is not at point_id {bad}")
    return ages.to_numpy(dtype="int64")


def sum_assured():
    """The face amount of every model point: float64 [point]."""
    return model_point_table()["sum_assured"].to_numpy(dtype="float64")


def policy_count():
    """The ``policy_count`` of every model point: float64 [point].

    :func:`model_point_table` has checked it: a number, zero or more.
    """
    return model_point_table()["policy_count"].to_numpy(dtype="float64")


def duration_mth():
    """The ``duration_mth`` of every model point, in whole months: int64 [point].

    :func:`model_point_table` has checked that each is whole, so a duration written as
    ``12.0`` is the int 12.
    """
    return model_point_table()["duration_mth"].to_numpy(dtype="int64")


def policy_term():
    """The level period of every model point in years, decoded from ``plan``: int64 [point].

    The number after the plan's letter, ``T10`` 10, read on each point exactly as
    ``Term_US_S`` reads it, ``int(plan[1:])``. A plan that ``int`` cannot read so, such as
    ``TX`` or ``T10.0``, is refused, naming every point that carries one.
    """
    table = model_point_table()
    labels, plans = table.index.tolist(), table["plan"].tolist()
    out = np.zeros(len(plans), dtype="int64")                        # noqa: F821
    bad = []
    for i in range(len(plans)):
        try:
            out[i] = int(plans[i][1:])
        except (TypeError, ValueError):
            bad.append(labels[i])
    if bad:
        raise ValueError(f"{model_point_file}: plan must be a letter and a whole number "
                         f"of years, as T10; it is not at point_id {bad}")
    return out


def prem_cycle():
    """Months between premium instalments, decoded from ``premium_mode``: int64 [point].

    A 12, SA 6, Q 3, M 1, the arithmetic of the mode, as ``Term_US_S``'s ``prem_cycle``
    has it, and ``Projection.modal_factor`` selects the mode's factor by it. Any other
    mode is refused, naming every point that carries it.
    """
    table = model_point_table()
    cycles = {"A": 12, "SA": 6, "Q": 3, "M": 1}
    mode = table["premium_mode"]
    bad = table.index[~mode.isin(list(cycles))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: premium_mode must be A, SA, Q or M; it is "
                         f"not at point_id {bad}")
    return mode.map(cycles).to_numpy(dtype="int64")


def band():
    """Face-amount band 1-4 of every model point: int64 [point].

    ``Term_US_S``'s rule, point by point: boundaries at $250,000 / $500,000 /
    $1,000,000 [S5], the four-band choice **[std]**, so a face below the first boundary is
    band 1 and one at it band 2. :func:`premium_schedule` joins the schedule by it.
    """
    faces = model_point_table()["sum_assured"].to_numpy(dtype="float64").tolist()
    out = np.zeros(len(faces), dtype="int64")                        # noqa: F821
    for i in range(len(faces)):
        f = faces[i]
        out[i] = 1 if f < 250000 else 2 if f < 500000 else 3 if f < 1000000 else 4
    return out


def class_factor():
    """The underwriting-class factor of every model point **[std]**: float64 [point].

    Each point's ``rate_class`` joined to *class_factor_table.csv*, the factor
    ``Term_US_S`` looks up. ``Projection.mort_rate`` caps the rate the factor scales, so
    every factor in the table must be a finite number: a blank, text or infinite one is
    refused, naming every class that carries one, whether or not a point carries it. A
    class the table lacks is refused too, naming every point that carries it.
    """
    table = model_point_table()
    factors = pd.to_numeric(class_factor_table()["factor"], errors="coerce")  # noqa: F821
    bad = factors.index[~((factors > -float("inf")) & (factors < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{class_factor_file}: factor must be a finite number; it is not "
                         f"at rate_class {bad}")
    bad = table.index[~table["rate_class"].isin(factors.index)].tolist()
    if bad:
        raise ValueError(f"{class_factor_file} has no factor for the rate_class of "
                         f"point_id {bad}")
    return table["rate_class"].map(factors).to_numpy(dtype="float64")


def plt_mort_factor_override():
    """M(1) where a model point overrides it, 0.0 where it leaves it blank: float64 [point].

    A blank is :func:`has_plt_mort_factor_override`'s 0, and ``Projection`` asks the flag,
    never the value, whether a point overrides M(1), so no NaN reaches a formula. A blank
    is the column's own meaning, the notes' rule, and is left so. An override is read by
    the ``max`` of ``Projection.plt_mort_factor`` and the cap of ``Projection.mort_rate``,
    so one that is neither a finite number nor blank, text or infinite, is refused, naming
    every point that carries one.
    """
    table = model_point_table()
    column = table["plt_mort_factor_override"]
    values = pd.to_numeric(column, errors="coerce")                  # noqa: F821
    bad = table.index[column.notna()
                      & ~((values > -float("inf")) & (values < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: plt_mort_factor_override must be a finite "
                         f"number or blank; it is not at point_id {bad}")
    return values.fillna(0.0).to_numpy(dtype="float64")


def has_plt_mort_factor_override():
    """Whether each model point overrides M(1): int64 [point], 1 where it does, 0 blank.

    An int, not a bool: a numpy bool array compiles as a Python object, not a memoryview.
    """
    return model_point_table()["plt_mort_factor_override"].notna().to_numpy(dtype="int64")


def premium_schedule():
    """Each model point's premium schedule, its row of :func:`premium_rates_array`: int64
    [point].

    A schedule is the rows of *premium_rates.csv* for one plan, sex, class and band,
    numbered from 1 in the order of those keys, and a point's is the one of its plan, sex,
    ``rate_class`` and :func:`band`, the key ``Term_US_S`` looks the premium up by. A point
    whose key has no schedule has 0, a schedule whose extent holds no policy year, so that
    ``Projection.premium_pp_ann_py`` refuses every year of it, naming the point, where
    ``Term_US_S``'s lookup raised ``KeyError``.
    """
    rates = premium_rates().reset_index()
    groups = rates.groupby(["plan", "sex", "rate_class", "band"])
    number = {}
    for key, _ in groups:
        number[key] = len(number) + 1
    table = model_point_table()
    plans, sexes = table["plan"].tolist(), table["sex"].tolist()
    classes = table["rate_class"].tolist()
    out = np.zeros(len(plans), dtype="int64")                        # noqa: F821
    for i in range(len(plans)):
        out[i] = number.get((plans[i], sexes[i], classes[i], int(band()[i])), 0)
    return out


def premium_schedules():
    """The number of premium schedules in *premium_rates.csv*, each checked: an int.

    A schedule is the table's rows for one plan, sex, class and band, numbered from 1 in
    the order of those keys, as :func:`premium_schedule` numbers them. Its policy years are
    read by their value, as ``Term_US_S``'s lookup matches them, so a year written ``1.0``
    is year 1. A schedule whose policy years are not whole numbers, text among them, leave
    a gap, repeat or start below 1 is refused, naming it. Once every schedule's years are
    checked, a premium that is not a finite number, blank, text or infinite, is refused,
    naming every schedule that holds one, whether or not a point carries it, and every
    such policy year in it: ``Projection.jump_ratio`` reads two premiums of a schedule,
    and the ``min`` of the notes' M(1) rule reads their ratio. :func:`premium_rates_array`
    and both of its extents, :func:`premium_first_year` and :func:`premium_last_year`, are
    sized by this count, so each meets the refusal first, whichever of them a projection
    reads first.
    """
    rates = premium_rates().reset_index()
    years = pd.to_numeric(rates["policy_year"], errors="coerce")     # noqa: F821
    premiums = pd.to_numeric(rates["premium_pp"], errors="coerce")   # noqa: F821
    groups = rates.assign(policy_year=years, premium_pp=premiums).groupby(
        ["plan", "sex", "rate_class", "band"])
    found = []
    for key, rows in groups:
        y = rows["policy_year"]
        whole = bool((y % 1 == 0).all())
        if (not whole or y.min() < 1
                or sorted(y.tolist()) != list(range(int(y.min()), int(y.max()) + 1))):
            raise ValueError(
                f"{premium_rates_file}: the schedule of plan {key[0]}, sex {key[1]}, class "
                f"{key[2]}, band {key[3]} must run in whole policy years from 1 or more, "
                f"without a gap or a repeat")
        p = rows["premium_pp"]
        bad = y[~((p > -float("inf")) & (p < float("inf")))].tolist()
        if bad:
            found.append(f"the schedule of plan {key[0]}, sex {key[1]}, class {key[2]}, "
                         f"band {key[3]}, at policy year {bad}")
    if found:
        where = ", nor in ".join(found)
        raise ValueError(f"{premium_rates_file}: premium_pp must be a finite number; it is "
                         f"not in {where}")
    return groups.ngroups


def premium_rates_array():
    """AP by premium schedule and policy year, from *premium_rates.csv*: float64
    [schedule, policy year].

    Row ``s`` is schedule ``s`` (:func:`premium_schedule`) and column ``y`` policy year
    ``y``, so ``Projection.premium_pp_ann_py`` reads a point's AP at
    ``[premium_schedule(), y]``. The width is the table's last policy year plus one. Row 0,
    no schedule, and column 0, no policy year, hold NaN, and so do the years outside a
    schedule's :func:`premium_first_year` and :func:`premium_last_year`; no formula reads
    them. Each schedule's years are read by value, and :func:`premium_schedules` refuses a
    schedule this array cannot hold.
    """
    n = premium_schedules()
    rates = premium_rates().reset_index()
    years = pd.to_numeric(rates["policy_year"], errors="coerce")     # noqa: F821
    groups = rates.assign(policy_year=years).groupby(["plan", "sex", "rate_class", "band"])
    width = int(years.max()) + 1 if n else 1
    out = np.full((n + 1, width), np.nan)                            # noqa: F821
    s = 0
    for _, rows in groups:
        s += 1
        y = rows["policy_year"].to_numpy(dtype="int64")
        out[s, y] = rows["premium_pp"].to_numpy(dtype="float64")
    return out


def premium_first_year():
    """The first policy year of each premium schedule: int64 [schedule].

    1 for row 0, no schedule, whose last year is 0, so that no year lies between them. The
    years are read by value, from the schedules :func:`premium_schedules` has checked.
    """
    out = np.ones(premium_schedules() + 1, dtype="int64")            # noqa: F821
    rates = premium_rates().reset_index()
    years = pd.to_numeric(rates["policy_year"], errors="coerce")     # noqa: F821
    s = 0
    for _, rows in rates.assign(policy_year=years).groupby(
            ["plan", "sex", "rate_class", "band"]):
        s += 1
        out[s] = int(rows["policy_year"].min())
    return out


def premium_last_year():
    """The last policy year of each premium schedule: int64 [schedule], 0 for no schedule.

    Read as :func:`premium_first_year` reads the first.
    """
    out = np.zeros(premium_schedules() + 1, dtype="int64")           # noqa: F821
    rates = premium_rates().reset_index()
    years = pd.to_numeric(rates["policy_year"], errors="coerce")     # noqa: F821
    s = 0
    for _, rows in rates.assign(policy_year=years).groupby(
            ["plan", "sex", "rate_class", "band"]):
        s += 1
        out[s] = int(rows["policy_year"].max())
    return out


def mort_age_first():
    """The first attained age *mort_table.csv* gives a rate for.

    An age is read by its value, as ``Term_US_S``'s lookup matches it, so one written
    ``35.0`` is 35. One that is not a whole number, text among them, is refused, naming
    every such age, here and in :func:`mort_age_last`, either of which a projection may
    read first.
    """
    ages = pd.to_numeric(pd.Series(mort_table().index), errors="coerce")  # noqa: F821
    bad = mort_table().index[~(ages % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{mort_table_file}: an age must be a whole number; {bad} is not")
    return int(ages.min())


def mort_age_last():
    """The last attained age *mort_table.csv* gives a rate for, read as
    :func:`mort_age_first` reads the first."""
    ages = pd.to_numeric(pd.Series(mort_table().index), errors="coerce")  # noqa: F821
    bad = mort_table().index[~(ages % 1 == 0).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{mort_table_file}: an age must be a whole number; {bad} is not")
    return int(ages.max())


def mort_table_array():
    """Base mortality by attained age, from *mort_table.csv*: float64 [age].

    Padded from age 0, so that the index **is** the age, as
    ``basiclife.BasicTerm_SC.Data.mort_table_array`` pads its table; the ages below the
    table's first, 0 to 34 as shipped, hold NaN, which no formula reads. The ages must run
    from :func:`mort_age_first` to :func:`mort_age_last` without a gap or a repeat, none
    negative, or the table is refused. ``Projection.mort_rate`` caps the rate, so each
    must be a finite number: a blank, text or infinite one is refused, naming every age
    that carries one. ``Projection.mort_rate_base`` refuses an age outside the table,
    naming the point.
    """
    rates = pd.to_numeric(mort_table()["mort_rate"], errors="coerce")  # noqa: F821
    ages = rates.index.tolist()
    first, last = mort_age_first(), mort_age_last()
    if first < 0 or sorted(ages) != list(range(first, last + 1)):
        raise ValueError(f"{mort_table_file}: the ages must run from {first} to {last} "
                         f"without a gap or a repeat, none negative")
    bad = rates.index[~((rates > -float("inf")) & (rates < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{mort_table_file}: mort_rate must be a finite number; it is not "
                         f"at age {bad}")
    out = np.full(last + 1, np.nan)                                  # noqa: F821
    out[rates.index.to_numpy(dtype="int64")] = rates.to_numpy(dtype="float64")
    return out


def shock_lapse_buckets():
    """The number of jump-ratio buckets in *shock_lapse_table.csv*: one or more, or the
    table is refused."""
    n = len(shock_lapse_table())
    if n < 1:
        raise ValueError(f"{shock_lapse_file} has no bucket")
    return n


def shock_lapse_jump_lo():
    """Each bucket's lower bound on the jump ratio, exclusive: float64 [bucket]."""
    return shock_lapse_table()["jump_lo"].to_numpy(dtype="float64")


def shock_lapse_jump_hi():
    """Each bucket's upper bound on the jump ratio, inclusive: float64 [bucket]."""
    return shock_lapse_table()["jump_hi"].to_numpy(dtype="float64")


def shock_lapse_bucket_rate():
    """Each bucket's shock lapse rate **[std]**: float64 [bucket]."""
    return shock_lapse_table()["shock_lapse_rate"].to_numpy(dtype="float64")


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

premium_rates_file = "premium_rates.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

shock_lapse_file = "shock_lapse_table.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")

np = ("Module", "numpy")