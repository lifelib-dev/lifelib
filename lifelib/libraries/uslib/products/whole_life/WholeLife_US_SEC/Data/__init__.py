# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.WholeLife_US_SEC.Projection` as ``data``. :mod:`~.WholeLife_US_SEC.Projection` is
parameterized by ``idx``, the position of a model point in the table, so each
``Projection[i]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized
Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/whole_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WholeLife_US_SEC`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

**Five of the tables are WholeLife_US_S's.** The guaranteed cash value schedule, the net
single premiums, the nonforfeiture net level premiums, the guaranteed mortality and the
final-expense premium rates are the files :mod:`~.WholeLife_US_S` reads, read here in
place: one copy of each table serves both models, so an edit to one reaches both. The
model point table is this model's own, ``model_point_table_sec.csv``; it sits beside
``WholeLife_US_S``'s ``model_point_table.csv``, which this model never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table_sec.csv
cv_file                 cv_table()                  cv_table.csv
nsp_file                nsp_table()                 nsp_table.csv
np_guar_file            np_guar_table()             np_guar_table.csv
mort_table_file         mort_table()                mort_table.csv
premium_rates_file      premium_rates()             premium_rates.csv
======================  ==========================  ==============================

**The model point table is checked as it is read.** Nine of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in
``basiclife.BasicTerm_SE``, and the seven columns of an in-force policy's opening
state. :func:`model_point_table` refuses a table that lacks any of them, repeats a
``point_id``, holds a count or a duration no policy can have, or holds an opening state
no policy can be in. The checks run in turn, and the first that fails raises, naming the
missing column or every point that fails it. It also refuses a policy to be issued more
than ``future_horizon_mth`` months after the valuation date, 120 months as shipped:
future new business is written over a stated horizon, so that no frame runs longer than
cover from issue plus that horizon. Set to 0, the Reference refuses future new business
altogether. A longer horizon projects in modelx, but the compiled model's caches are sized
for the shipped 120 months (``spec_sec.py``): it needs ``t`` there raised to
12 x (maturity_age - issue_age_min) + the horizon + 2 and a rebuild, or a frame longer
than 1,320 months raises ``IndexError`` compiled, naming nothing, at the first month past
the caches. Whether a point is still in cover at the valuation date, and whether the
contract issues it, are rules of the product rather than of the table, and
``Projection.proj_len`` checks them, against two Projection References the caches are
sized from as they are from the horizon: ``maturity_age`` and ``issue_age_min``.

The four guarantee-basis tables belong together. ``mort_table.csv`` holds the
guaranteed mortality ``q^g``, ``nsp_table.csv`` the endowment-at-100 net single
premiums that price paid-up additions, ``np_guar_table.csv`` the nonforfeiture net
level premium that the dividend's interest margin is credited on, and ``cv_table.csv``
the guaranteed cash value schedule. The technical notes' first "known modeling
pitfall" is exactly a mismatch between them, and it prescribes regenerating all four
from one 2017 CSO / 4% source.

**The shipped four are not one construction, and no set carrying the worked example's
anchors could be.** On a single mortality basis at 4% the notes' own definition
collapses to ``NNLP = 1000 d NSP_45 / (1 - NSP_45)``, so the worked example's
``NNLP = 13.00`` forces ``NSP_45 = 0.252616`` and hence ``NSP_55 <= 0.252616 x 1.04^10
= 0.373933`` — short of the worked example's ``NSP_55 = 0.42``, whatever mortality is
assumed. Each shipped table is therefore pinned to its own worked-example anchor
independently: ``q^g_54 = 0.00320``, ``NSP_55 = 0.42``, ``NP_g = 13.00``, and 95.00 and
112.00 per $1,000 on the policy-year 9 and 10 rows of the cash value schedule — the
worked example's ``CV_107`` and ``CV_119``. The anchor cell, in force 108 months at the
valuation date, reaches them as ``cv_pp_anniv(9)``, the value entering its ``t = 0``,
which ``WholeLife_US_S`` reads as ``cv_pp(107)``, and as ``cv_pp(11)``, its tenth
anniversary, ``WholeLife_US_S``'s month 119. Reconciling ``nsp_table.csv`` with
``mort_table.csv`` would need a guarantee interest rate falling from 5.99% at age 45
to 0.02% at age 99. ``model.md`` and the ``Projection`` docstring carry the
arithmetic; a test pins the mismatch by age so it cannot quietly close.

What *is* guaranteed, because the two consequences the pitfall names would otherwise
bite, is the pair of endpoints: ``nsp = 1.000000`` at attained age 100, so the
paid-up-additions cash value reaches paid-up-additions face at maturity, and
``cv_per_1000 = 1000.00`` on the last policy year of each cell — the schedule's
``policy_year = 100 - issue_age`` row, read by the model at ``t = proj_len() - 1`` — so
the base block endows at face.
Both are asserted by the tests. Every rate is also **sex-distinct**, as the notes
require — including the pay-to-100 cash value schedule.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache; a compiled
model clears no cache, so there the name is set on a package just imported, before
anything is read. No formula changes — but regenerate ``nsp_table.csv``,
``np_guar_table.csv`` and ``cv_table.csv`` from the same basis, or the pitfall above is
exactly what happens.
Doing so is the only way to satisfy the notes' one-basis instruction, and it will stop
the worked example reproducing. Replacing the files changes :mod:`~.WholeLife_US_S`
too, which reads the same ones.

**The vectors.** The readers return what the files hold, and no
:mod:`~.WholeLife_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads
them. The others read the arrays below instead, one element at a time, a model point's
attribute being the element at its position, ``data.issue_age()[idx]``. That is what lets
the model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy vector
or table of int64 or float64, which compiles to a typed memoryview, never one of bools,
objects or text, and each count of rows or schedules is an int.

Text the projection needs is decoded here, into the number it selects: the product into
two flags, the premium period and the dividend option into their codes, the premium mode
into the months between instalments. Each table keyed by more than a number becomes an
integer-indexed array or a join. The cash value schedules, keyed by premium period, sex
and issue age, are numbered, each point carrying the number of its own, and tabled by
schedule and policy year. The guaranteed mortality and the net single premiums are
numbered by sex the same way and tabled by schedule and attained age, padded from age 0,
so that the column index is the age. The final-expense rates and the net level premiums,
each one number a point and read by one design alone, are joined to the points, a flag
beside each saying whether the table has the point's key:

============================  =======  ===============  ===============================
Cells                         dtype    Shape            From
============================  =======  ===============  ===============================
point_id()                    int64    [point]          the table's index
issue_age()                   int64    [point]          ``issue_age``
face_amount()                 float64  [point]          ``face_amount``
annual_premium()              float64  [point]          ``annual_premium``, NaN if blank
pua_rider_premium()           float64  [point]          ``pua_rider_premium``
term_blend_target()           float64  [point]          ``term_blend_target``
loan_utilization()            float64  [point]          ``loan_utilization``
policy_count()                float64  [point]          ``policy_count``
duration_mth()                int64    [point]          ``duration_mth``
pua_face_init()               float64  [point]          ``pua_face_init``
pua_face_prev_anniv_init()    float64  [point]          ``pua_face_prev_anniv_init``
loan_bal_init()               float64  [point]          ``loan_bal_init``
loan_bal_prev_anniv_init()    float64  [point]          ``loan_bal_prev_anniv_init``
div_accum_init()              float64  [point]          ``div_accum_init``
div_prev_anniv_init()         float64  [point]          ``div_prev_anniv_init``
prem_cum_init()               float64  [point]          ``prem_cum_init``
is_par()                      int64    [point]          ``product``, 1 on WL_PAR
is_graded()                   int64    [point]          ``product``, 1 on WL_FE_GRADED
premium_period_code()         int64    [point]          ``premium_period``, decoded
dividend_option_code()        int64    [point]          ``dividend_option``, decoded
prem_cycle()                  int64    [point]          ``premium_mode``, decoded
premium_rate_rows()           int      scalar           *premium_rates.csv*, checked
premium_rate_per_1000()       float64  [point]          *premium_rates.csv*, joined
has_premium_rate()            int64    [point]          1 where joined, 0 where not
np_guar_rows()                int      scalar           *np_guar_table.csv*, checked
np_guar_per_1000()            float64  [point]          *np_guar_table.csv*, joined
has_np_guar()                 int64    [point]          1 where joined, 0 where not
cv_schedules()                int      scalar           *cv_table.csv*, checked
cv_schedule()                 int64    [point]          period, sex and issue age, joined
cv_array()                    float64  [schedule, y]    *cv_table.csv*
cv_year_first()               int64    [schedule]       *cv_table.csv*
cv_year_last()                int64    [schedule]       *cv_table.csv*
mort_schedules()              int      scalar           *mort_table.csv*, checked
mort_schedule()               int64    [point]          ``sex``, joined
mort_table_array()            float64  [schedule, age]  *mort_table.csv*
mort_age_first()              int64    [schedule]       *mort_table.csv*
mort_age_last()               int64    [schedule]       *mort_table.csv*
nsp_schedules()               int      scalar           *nsp_table.csv*, checked
nsp_schedule()                int64    [point]          ``sex``, joined
nsp_array()                   float64  [schedule, age]  *nsp_table.csv*
nsp_age_first()               int64    [schedule]       *nsp_table.csv*
nsp_age_last()                int64    [schedule]       *nsp_table.csv*
============================  =======  ===============  ===============================

**An array is read by element, never whole,** in this Space as in
:mod:`~.WholeLife_US_SEC.Projection`. The compiler types an array cell as a memoryview
only once it has seen that every use of it, in either Space, is an element read: one
``len()``, slice, loop over it or numpy call on it anywhere, and the cell compiles as a
Python object. So an array derived here from another reads the table's column, or the
other cell element by element, as :func:`cv_schedule` reads :func:`issue_age`; a flag
beside a join is formed from the tables again, not read off the join's values; and a
width comes from a table, never from another cell's array. Each table's check is one cell
that every array, extent and schedule number of the table reads first,
:func:`cv_schedules` for the cash values, so that a projection, which reads an extent or a
schedule number first, meets the same refusal as a reader of the array.

**What cannot be decoded is refused** when the array is first read, naming every point
at fault: a ``point_id`` that is not a whole number, a premium period other than TO_100,
PAY_10, PAY_20 or TO_65, a premium mode other than A, SA, Q or M. A dividend option none
of the four is ``WholeLife_US_S``'s none, and is read so, not refused. So is a table the
arrays cannot hold: a cash value schedule whose policy years are not whole, leave a gap,
repeat or start below 1; a mortality or net single premium schedule with an age that is
not whole, a gap, a repeated or negative age; an issue age key of the cash values, the
net level premiums or the rates that is not whole; a key of the net level premiums or the
rates that appears twice. ``WholeLife_US_S`` met each of these only when a projection
reached it. A key written as a float, a policy year ``9.0`` or an age ``54.0``, is read by
its value, as ``WholeLife_US_S``'s lookups match it, and so is every key an extent or a
join is taken from: a key written as text is not whole, and the table's check refuses it.
A read beyond a table's extent is refused where ``WholeLife_US_S``'s lookup raised
``KeyError``, by the one :mod:`~.WholeLife_US_SEC.Projection` cell that reads the table,
naming the point: ``cv_pp_anniv``, ``nsp`` and ``mort_rate_guar_at``; and so is a point
whose key a joined table lacks, by the cell that reads the join, ``premium_rate`` or
``np_guar``. ``Data`` refuses neither, since ``WholeLife_US_S`` projects a point that reads
no such key, a participating point without a final-expense rate among them.

**A value a capped rate, a min or a max reads is a number in its range,** or it is
refused when its array is first read, naming the file, the column and every line, key or
point at fault. ``Projection.mort_rate`` caps the annual rate with ``min``, and the
dividend's floor, the REDUCE_PREM offset, the term-blend gap and its cap, the
paid-up-additions purchases bound theirs with ``min`` and ``max``.
Each keeps its first argument unless a later one compares smaller, or larger, and no
comparison with NaN holds, so a NaN would stay NaN; but an infinity is a number, which the
cap reads as 1, certain death, and a blank or a text is no number at all. Through the
dividend and the paid-up additions those bounds reach every amount and rate the
projection reads, so every one is checked, over its whole column, whether or not a point
carries its key: the face, the premium of the participating design, the rider premium
and the blend target, each a number, zero or more; the loan share, a number from 0 to 1;
a cash value, a net level premium and a final-expense rate, each a number, zero or more;
a guaranteed mortality rate, a number from 0 to 1, a probability; and a net single
premium, a number above 0, which the purchases divide by. The opening state and the count
are :func:`model_point_table`'s, and the issue age must be a finite number. A blank
premium off the participating design is final expense's own, and is left so, and so is
the padding, which no formula reads.

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is first refused unless it is below
``2**53`` in size, where the int64 holds ``WholeLife_US_S``'s reading of it: the issue age,
and ``duration_mth`` (:func:`model_point_table`). modelx and the compiled model refuse
alike, before any cast. A fractional issue age is not refused: it truncates toward zero,
as ``WholeLife_US_S``'s ``int`` truncates it.
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

    Indexed by ``point_id``. Nine columns are the in-force interface: ``policy_count``
    and ``duration_mth``, the completed policy months at the valuation date, as in
    ``basiclife.BasicTerm_SE``, and the seven columns of the opening state, per policy,
    as the policy stands at the start of month 0, before any month-0 event:

    * ``pua_face_init``, ``loan_bal_init`` and ``div_accum_init``: the paid-up-additions
      face, the loan and the accumulation balance entering month 0;
    * ``pua_face_prev_anniv_init`` and ``loan_bal_prev_anniv_init``: the same face and
      loan at the anniversary that opened the policy year under way, the one on or
      before the valuation date, and ``div_prev_anniv_init``, the dividend credited
      there;
    * ``prem_cum_init``: the gross premium paid before the valuation date.

    The rest are ``WholeLife_US_S``'s, except ``row_kind``, ``source_policy_id`` and
    ``source_mth``, which record where the generator took each shipped row from and which
    no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on:

    * the nine in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months: positive for a policy in force, 0
      for one issued at the valuation date, negative for one issued later;
    * ``duration_mth`` is below ``2**53`` months, which an int64 and a float both hold
      exactly: numpy would read a duration past int64 as the least int64, without a
      word, a policy to be issued ``2**63`` months on, past the horizon below;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused;
    * each opening-state column is a number, zero or more;
    * a policy not yet in force, ``duration_mth`` 0 or less, has no opening state: it is
      issued with none;
    * the non-participating final-expense design has no paid-up additions and no
      dividend;
    * only the ACCUM option has an accumulation balance, which on any other the
      projection would drop from every benefit;
    * on a point valued on a policy anniversary, ``duration_mth`` a multiple of 12, the
      two anniversary columns equal the two entering month 0, which are the same
      instant;
    * in the first policy year, ``duration_mth`` 1 to 11, the year opened at issue and
      has credited no dividend yet, so the three anniversary columns hold their issue
      values, 0, and so does ``div_accum_init``.

    A point whose paid-up additions at the anniversary exceed those entering month 0 is
    accepted. The model never shrinks the block, so such a row records a partial
    surrender of additions, which the model does not implement, and it is projected
    from the values it gives.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    state = ("pua_face_init", "pua_face_prev_anniv_init", "loan_bal_init",
             "loan_bal_prev_anniv_init", "div_accum_init", "div_prev_anniv_init",
             "prem_cum_init")
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
    bad = table.index[months >= 2.0 ** 53].tolist()
    if bad:
        raise ValueError(f"{name}: duration_mth must be below 2**53 months; it is not at "
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
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
    for column, v in values.items():
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column, v in values.items():
        bad = table.index[(months <= 0) & (v != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less; it is not at point_id {bad}")
    non_par = table["product"] != "WL_PAR"
    for column in ("pua_face_init", "pua_face_prev_anniv_init", "div_prev_anniv_init"):
        bad = table.index[non_par & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a non-participating "
                             f"product, which pays no dividend; it is not at point_id "
                             f"{bad}")
    bad = table.index[(table["dividend_option"] != "ACCUM")
                      & (values["div_accum_init"] != 0)].tolist()
    if bad:
        raise ValueError(f"{name}: div_accum_init must be 0 unless dividend_option is "
                         f"ACCUM; it is not at point_id {bad}")
    on_anniv = (months > 0) & (months % 12 == 0)
    for anniv, now in (("pua_face_prev_anniv_init", "pua_face_init"),
                       ("loan_bal_prev_anniv_init", "loan_bal_init")):
        bad = table.index[on_anniv & (values[anniv] != values[now])].tolist()
        if bad:
            raise ValueError(f"{name}: on a point valued on a policy anniversary, "
                             f"duration_mth a multiple of 12, {anniv} must equal {now}; "
                             f"it does not at point_id {bad}")
    first_year = (months > 0) & (months < 12)
    for column in ("pua_face_prev_anniv_init", "loan_bal_prev_anniv_init",
                   "div_accum_init", "div_prev_anniv_init"):
        bad = table.index[first_year & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 in the first policy year, "
                             f"duration_mth 1 to 11, which opened at issue and has "
                             f"credited no dividend yet; it is not at point_id {bad}")
    return table


def cv_table():
    """The guaranteed cash value schedule per $1,000 of face, from *cv_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / cv_file,                                       # noqa: F821
        index_col=["premium_period", "sex", "issue_age", "policy_year"])


def nsp_table():
    """The endowment-at-100 net single premiums by attained age, from *nsp_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / nsp_file, index_col=["sex", "age"])            # noqa: F821


def np_guar_table():
    """The nonforfeiture net level premiums per $1,000, from *np_guar_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / np_guar_file,                                  # noqa: F821
        index_col=["premium_period", "sex", "issue_age"])


def mort_table():
    """The guaranteed mortality table by sex and age, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"])     # noqa: F821


def premium_rates():
    """The final-expense premium rates per $1,000, read from *premium_rates.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / premium_rates_file,                            # noqa: F821
        index_col=["product", "sex", "risk_class", "issue_age"])


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


def issue_age():
    """The issue age (ANB) of every model point: int64 [point].

    The attained age it opens indexes *mort_table.csv*, whose rate
    ``Projection.mort_rate`` caps, and keys the cash value schedule, the net level premium
    and the final-expense rate, so an age that is not a finite number, blank, text or
    infinite, is refused, naming every point that carries one: numpy would read a blank or
    infinite age as the least int64, without a word. So is one of ``2**53`` or more in
    size, which numpy would read as the least int64 once past int64, before the cast.
    Otherwise the age is read as ``WholeLife_US_S`` reads it, ``int`` of the number: a
    fraction truncates toward zero, so 45.5 projects as 45, and -0.5 as 0, which
    ``proj_len`` then issues, as ``WholeLife_US_S`` does.
    """
    table = model_point_table()
    ages = pd.to_numeric(table["issue_age"], errors="coerce")       # noqa: F821
    bad = table.index[~((ages > -float("inf")) & (ages < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: issue_age must be a finite number; it is "
                         f"not at point_id {bad}")
    bad = table.index[~(ages.abs() < 2.0 ** 53)].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: issue_age must be below 2**53 in size; it "
                         f"is not at point_id {bad}")
    return ages.to_numpy(dtype="int64")


def face_amount():
    """The base face amount F of every model point: float64 [point].

    A number, zero or more: the face reaches the dividend's floor, the term-blend gap and
    the cap on the layer through the net amount at risk, so a blank, text, infinite or
    negative face is refused, naming every point that carries one.
    """
    table = model_point_table()
    faces = pd.to_numeric(table["face_amount"], errors="coerce")    # noqa: F821
    bad = table.index[~((faces >= 0) & (faces < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: face_amount must be a number, zero or "
                         f"more; it is not at point_id {bad}")
    return faces.to_numpy(dtype="float64")


def annual_premium():
    """The participating design's gross annual premium G, its model point's: float64
    [point].

    ``Projection.premium_pp_ann`` reads it on the participating design alone, where it is
    a number, zero or more, or the point is refused: the premium reaches the
    REDUCE_PREM offset's ``max``. Final expense prices its premium from
    *premium_rates.csv* and leaves the column blank, NaN here, which no formula reads; a
    number there is held to the same rule, and anything else is refused. Each refusal
    names every point that carries one.
    """
    table = model_point_table()
    column = table["annual_premium"]
    premiums = pd.to_numeric(column, errors="coerce")               # noqa: F821
    par = table["product"] == "WL_PAR"
    number = (premiums >= 0) & (premiums < float("inf"))
    bad = table.index[~(number | (~par & column.isna()))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: annual_premium must be a number, zero or "
                         f"more, or blank off the participating design; it is not at "
                         f"point_id {bad}")
    return premiums.to_numpy(dtype="float64")


def pua_rider_premium():
    """The annual paid-up-additions rider premium of every model point: float64 [point].

    A number, zero or more, or it is refused, naming every point that carries one: the
    rider's additions reach the dividend's floor and the term-blend gap.
    """
    table = model_point_table()
    premiums = pd.to_numeric(table["pua_rider_premium"], errors="coerce")  # noqa: F821
    bad = table.index[~((premiums >= 0) & (premiums < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: pua_rider_premium must be a number, zero "
                         f"or more; it is not at point_id {bad}")
    return premiums.to_numpy(dtype="float64")


def term_blend_target():
    """TF, the term-blend rider's target face, of every model point: float64 [point].

    A number, zero or more, or it is refused, naming every point that carries one: the
    term-blend gap's ``max`` and the layer's ``min`` read it.
    """
    table = model_point_table()
    targets = pd.to_numeric(table["term_blend_target"], errors="coerce")  # noqa: F821
    bad = table.index[~((targets >= 0) & (targets < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: term_blend_target must be a number, zero "
                         f"or more; it is not at point_id {bad}")
    return targets.to_numpy(dtype="float64")


def loan_utilization():
    """The share of the cash value held as a loan, of every model point: float64 [point].

    A share, so a number from 0 to 1, or it is refused, naming every point that carries
    one: the loan reaches the dividend's floor through the interest margin.
    """
    table = model_point_table()
    shares = pd.to_numeric(table["loan_utilization"], errors="coerce")  # noqa: F821
    bad = table.index[~((shares >= 0) & (shares <= 1))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: loan_utilization must be a number from 0 "
                         f"to 1; it is not at point_id {bad}")
    return shares.to_numpy(dtype="float64")


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


def pua_face_init():
    """The ``pua_face_init`` column, the additions entering month 0: float64 [point].

    :func:`model_point_table` has checked it, as every opening-state column: a number,
    zero or more.
    """
    return model_point_table()["pua_face_init"].to_numpy(dtype="float64")


def pua_face_prev_anniv_init():
    """The ``pua_face_prev_anniv_init`` column, the additions at the anniversary on or
    before the valuation date: float64 [point], checked by :func:`model_point_table`."""
    return model_point_table()["pua_face_prev_anniv_init"].to_numpy(dtype="float64")


def loan_bal_init():
    """The ``loan_bal_init`` column, the loan entering month 0: float64 [point], checked
    by :func:`model_point_table`."""
    return model_point_table()["loan_bal_init"].to_numpy(dtype="float64")


def loan_bal_prev_anniv_init():
    """The ``loan_bal_prev_anniv_init`` column, the loan at the anniversary on or before
    the valuation date: float64 [point], checked by :func:`model_point_table`."""
    return model_point_table()["loan_bal_prev_anniv_init"].to_numpy(dtype="float64")


def div_accum_init():
    """The ``div_accum_init`` column, the accumulation balance entering month 0: float64
    [point], checked by :func:`model_point_table`."""
    return model_point_table()["div_accum_init"].to_numpy(dtype="float64")


def div_prev_anniv_init():
    """The ``div_prev_anniv_init`` column, the dividend credited at the anniversary on or
    before the valuation date: float64 [point], checked by :func:`model_point_table`."""
    return model_point_table()["div_prev_anniv_init"].to_numpy(dtype="float64")


def prem_cum_init():
    """The ``prem_cum_init`` column, the gross premium paid before the valuation date:
    float64 [point], checked by :func:`model_point_table`."""
    return model_point_table()["prem_cum_init"].to_numpy(dtype="float64")


def is_par():
    """Whether each model point is the participating design: int64 [point], 1 where its
    ``product`` is WL_PAR, 0 elsewhere.

    ``WholeLife_US_S`` tests the product against that one value, so any other product is
    read as not participating, as there; nothing is refused. An int, not a bool: a numpy
    bool array compiles as a Python object, not a memoryview.
    """
    return (model_point_table()["product"] == "WL_PAR").to_numpy(dtype="int64")


def is_graded():
    """Whether each model point is the graded final-expense plan: int64 [point], 1 where
    its ``product`` is WL_FE_GRADED, 0 elsewhere.

    ``WholeLife_US_S``'s death benefit tests the product against that one value, and
    ``Projection.claim_pp`` reads this instead. Nothing is refused.
    """
    return (model_point_table()["product"] == "WL_FE_GRADED").to_numpy(dtype="int64")


def premium_period_code():
    """The premium period of every model point, as its code: int64 [point].

    TO_100 0, PAY_10 1, PAY_20 2, TO_65 3, the ``Projection`` References of the names,
    in the order ``product-spec.md`` lists them. ``Projection.policy_term`` and
    ``Projection.mec_flag`` branch on it where ``WholeLife_US_S`` compares the text. Any
    other period is refused, naming every point that carries it, where
    ``WholeLife_US_S``'s ``policy_term`` raised ``invalid premium_period`` once a
    projection reached it.
    """
    table = model_point_table()
    codes = {"TO_100": 0, "PAY_10": 1, "PAY_20": 2, "TO_65": 3}
    period = table["premium_period"]
    bad = table.index[~period.isin(list(codes))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: premium_period must be TO_100, PAY_10, "
                         f"PAY_20 or TO_65; it is not at point_id {bad}")
    return period.map(codes).to_numpy(dtype="int64")


def dividend_option_code():
    """The dividend option of every model point, as its code: int64 [point].

    PUA 0, CASH 1, ACCUM 2, REDUCE_PREM 3, the ``Projection`` References of the names,
    and NONE 4 for any other text, final expense's ``NONE`` among it: ``WholeLife_US_S``
    compares the text with each of the four and reads anything else as none of them, so
    an unknown option is read so here too, not refused, and earns no dividend benefit.
    """
    codes = {"PUA": 0, "CASH": 1, "ACCUM": 2, "REDUCE_PREM": 3}
    options = model_point_table()["dividend_option"].tolist()
    out = np.zeros(len(options), dtype="int64")                      # noqa: F821
    for i in range(len(options)):
        out[i] = codes.get(options[i], 4)
    return out


def prem_cycle():
    """Months between premium instalments, decoded from ``premium_mode``: int64 [point].

    A 12, SA 6, Q 3, M 1, the arithmetic of the mode, as ``WholeLife_US_S``'s
    ``prem_cycle`` has it, and ``Projection.modal_factor`` selects the mode's factor by
    it. Any other mode is refused, naming every point that carries it, where
    ``WholeLife_US_S`` raised once a projection reached it.
    """
    table = model_point_table()
    cycles = {"A": 12, "SA": 6, "Q": 3, "M": 1}
    mode = table["premium_mode"]
    bad = table.index[~mode.isin(list(cycles))].tolist()
    if bad:
        raise ValueError(f"{model_point_file}: premium_mode must be A, SA, Q or M; it is "
                         f"not at point_id {bad}")
    return mode.map(cycles).to_numpy(dtype="int64")


def premium_rate_rows():
    """The number of rates in *premium_rates.csv*, each checked: an int.

    A rate is keyed by product, sex, risk class and issue age, the key
    ``WholeLife_US_S``'s ``premium_rate`` looks it up by. The issue age is read by its
    value, as that lookup matches it, so one written ``65.0`` is 65; one that is not a
    whole number, text among them, is refused, naming every such age. A key that
    appears twice is refused, naming every such key: the lookup would return two rates.
    And every ``rate_per_1000`` must be a number, zero or more, whether or not a point
    carries its key, since the final-expense premium it prices reaches the REDUCE_PREM
    offset's ``max`` and the acquisition charge; the refusal names every key at fault.
    :func:`premium_rate_per_1000` and :func:`has_premium_rate` read this first, so either
    meets the refusal, whichever a projection reads first.
    """
    rates = premium_rates().reset_index()
    ages = pd.to_numeric(rates["issue_age"], errors="coerce")       # noqa: F821
    bad = rates["issue_age"][~(ages % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{premium_rates_file}: issue_age must be a whole number; {bad} "
                         f"is not")
    keys = list(zip(rates["product"].tolist(), rates["sex"].tolist(),
                    rates["risk_class"].tolist(), ages.to_numpy(dtype="int64").tolist()))
    seen, repeated = set(), []
    for key in keys:
        if key in seen and key not in repeated:
            repeated.append(key)
        seen.add(key)
    if repeated:
        raise ValueError(f"{premium_rates_file}: a rate appears more than once for the "
                         f"product, sex, risk_class and issue_age {repeated}")
    values = pd.to_numeric(rates["rate_per_1000"], errors="coerce")  # noqa: F821
    ok = ((values >= 0) & (values < float("inf"))).tolist()
    bad = [keys[i] for i in range(len(keys)) if not ok[i]]
    if bad:
        raise ValueError(f"{premium_rates_file}: rate_per_1000 must be a number, zero or "
                         f"more; it is not at the product, sex, risk_class and issue_age "
                         f"{bad}")
    return len(keys)


def premium_rate_per_1000():
    """Each model point's final-expense rate per $1,000 of face: float64 [point].

    The rate of *premium_rates.csv* keyed by the point's product, sex, ``risk_class`` and
    issue age, matched by value, as ``WholeLife_US_S`` looks it up, and NaN where the
    table has no rate for the key, which :func:`has_premium_rate` marks. Only final
    expense reads it, so a participating point, which has none as shipped, is not
    refused here: ``Projection.premium_rate`` refuses a point that reads a rate it lacks,
    naming it, where ``WholeLife_US_S``'s lookup raised ``KeyError``.
    :func:`premium_rate_rows` has checked the table.
    """
    premium_rate_rows()
    rates = premium_rates().reset_index()
    ages = pd.to_numeric(rates["issue_age"])                         # noqa: F821
    ages = ages.to_numpy(dtype="int64").tolist()
    values = pd.to_numeric(rates["rate_per_1000"]).tolist()         # noqa: F821
    products, sexes = rates["product"].tolist(), rates["sex"].tolist()
    classes = rates["risk_class"].tolist()
    look = {}
    for i in range(len(ages)):
        look[(products[i], sexes[i], classes[i], ages[i])] = float(values[i])
    table = model_point_table()
    products, sexes = table["product"].tolist(), table["sex"].tolist()
    classes = table["risk_class"].tolist()
    out = np.full(len(products), np.nan)                             # noqa: F821
    for i in range(len(products)):
        key = (products[i], sexes[i], classes[i], int(issue_age()[i]))
        if key in look:
            out[i] = look[key]
    return out


def has_premium_rate():
    """Whether *premium_rates.csv* has a rate for each model point's key: int64 [point],
    1 where it has, 0 where not.

    The key and the match are :func:`premium_rate_per_1000`'s, formed again from the
    tables rather than read off that array, which would read it whole. An int, not a
    bool: a numpy bool array compiles as a Python object, not a memoryview.
    """
    premium_rate_rows()
    rates = premium_rates().reset_index()
    ages = pd.to_numeric(rates["issue_age"])                         # noqa: F821
    ages = ages.to_numpy(dtype="int64").tolist()
    keys = set(zip(rates["product"].tolist(), rates["sex"].tolist(),
                   rates["risk_class"].tolist(), ages))
    table = model_point_table()
    products, sexes = table["product"].tolist(), table["sex"].tolist()
    classes = table["risk_class"].tolist()
    out = np.zeros(len(products), dtype="int64")                     # noqa: F821
    for i in range(len(products)):
        if (products[i], sexes[i], classes[i], int(issue_age()[i])) in keys:
            out[i] = 1
    return out


def np_guar_rows():
    """The number of net level premiums in *np_guar_table.csv*, each checked: an int.

    A premium is keyed by premium period, sex and issue age, the key
    ``WholeLife_US_S``'s ``np_guar`` looks it up by, the issue age read by its value. As
    :func:`premium_rate_rows` checks its table: an issue age that is not a whole number,
    text among them, and a key that appears twice are refused, naming every one, and
    every ``np_guar_per_1000`` must be a number, zero or more, whether or not a point
    carries its key, since the interest margin it enters reaches the dividend's floor.
    :func:`np_guar_per_1000` and :func:`has_np_guar` read this first.
    """
    premiums = np_guar_table().reset_index()
    ages = pd.to_numeric(premiums["issue_age"], errors="coerce")    # noqa: F821
    bad = premiums["issue_age"][~(ages % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{np_guar_file}: issue_age must be a whole number; {bad} is "
                         f"not")
    keys = list(zip(premiums["premium_period"].tolist(), premiums["sex"].tolist(),
                    ages.to_numpy(dtype="int64").tolist()))
    seen, repeated = set(), []
    for key in keys:
        if key in seen and key not in repeated:
            repeated.append(key)
        seen.add(key)
    if repeated:
        raise ValueError(f"{np_guar_file}: a net level premium appears more than once for "
                         f"the premium_period, sex and issue_age {repeated}")
    values = pd.to_numeric(premiums["np_guar_per_1000"], errors="coerce")  # noqa: F821
    ok = ((values >= 0) & (values < float("inf"))).tolist()
    bad = [keys[i] for i in range(len(keys)) if not ok[i]]
    if bad:
        raise ValueError(f"{np_guar_file}: np_guar_per_1000 must be a number, zero or "
                         f"more; it is not at the premium_period, sex and issue_age {bad}")
    return len(keys)


def np_guar_per_1000():
    """Each model point's nonforfeiture net level premium per $1,000: float64 [point].

    The premium of *np_guar_table.csv* keyed by the point's premium period, sex and issue
    age, matched by value, and NaN where the table has none, which :func:`has_np_guar`
    marks. Only the participating dividend reads it, so a final-expense point, which has
    none as shipped, is not refused here: ``Projection.np_guar`` refuses a point that
    reads a premium it lacks, naming it. :func:`np_guar_rows` has checked the table.
    """
    np_guar_rows()
    premiums = np_guar_table().reset_index()
    ages = pd.to_numeric(premiums["issue_age"])                      # noqa: F821
    ages = ages.to_numpy(dtype="int64").tolist()
    values = pd.to_numeric(premiums["np_guar_per_1000"]).tolist()   # noqa: F821
    periods, sexes = premiums["premium_period"].tolist(), premiums["sex"].tolist()
    look = {}
    for i in range(len(ages)):
        look[(periods[i], sexes[i], ages[i])] = float(values[i])
    table = model_point_table()
    periods, sexes = table["premium_period"].tolist(), table["sex"].tolist()
    out = np.full(len(periods), np.nan)                              # noqa: F821
    for i in range(len(periods)):
        key = (periods[i], sexes[i], int(issue_age()[i]))
        if key in look:
            out[i] = look[key]
    return out


def has_np_guar():
    """Whether *np_guar_table.csv* has a premium for each model point's key: int64
    [point], 1 where it has, 0 where not, formed as :func:`has_premium_rate` is."""
    np_guar_rows()
    premiums = np_guar_table().reset_index()
    ages = pd.to_numeric(premiums["issue_age"])                      # noqa: F821
    ages = ages.to_numpy(dtype="int64").tolist()
    keys = set(zip(premiums["premium_period"].tolist(), premiums["sex"].tolist(), ages))
    table = model_point_table()
    periods, sexes = table["premium_period"].tolist(), table["sex"].tolist()
    out = np.zeros(len(periods), dtype="int64")                      # noqa: F821
    for i in range(len(periods)):
        if (periods[i], sexes[i], int(issue_age()[i])) in keys:
            out[i] = 1
    return out


def cv_schedules():
    """The number of cash value schedules in *cv_table.csv*, each checked: an int.

    A schedule is the table's rows for one premium period, sex and issue age, numbered
    from 1 in the order of those keys, as :func:`cv_schedule` numbers them. The issue
    age and the policy years are read by their value, as ``WholeLife_US_S``'s lookup
    matches them, so a year written ``9.0`` is year 9. An issue age that is not a whole
    number, text among them, is refused, naming every such age; then a schedule whose
    policy years are not whole numbers, text among them, leave a gap, repeat or start
    below 1 is refused, naming it. Once every schedule's years are checked, a cash value
    that is not a number, zero or more, is refused, naming every schedule that holds
    one, whether or not a point carries it, and every such policy year in it: the cash
    value reaches the dividend's floor and the surrender value. :func:`cv_array`, its
    extents :func:`cv_year_first` and :func:`cv_year_last`, and :func:`cv_schedule` are
    sized or numbered by this count, so each meets the refusal first, whichever a
    projection reads first.
    """
    cv = cv_table().reset_index()
    ages = pd.to_numeric(cv["issue_age"], errors="coerce")          # noqa: F821
    bad = cv["issue_age"][~(ages % 1 == 0)].unique().tolist()
    if bad:
        raise ValueError(f"{cv_file}: issue_age must be a whole number; {bad} is not")
    # The columns go to assign as a dict: the export rewrites a keyword argument named as
    # a cell of this Space, issue_age, into self.issue_age=, which does not compile, in a
    # formula that names that cell.  A keyword named as no Data cell, the age=, mort_rate=
    # and nsp= of the mortality and net single premium tables below, Projection cells all,
    # is kept as written.
    years = pd.to_numeric(cv["policy_year"], errors="coerce")       # noqa: F821
    values = pd.to_numeric(cv["cv_per_1000"], errors="coerce")      # noqa: F821
    cv = cv.assign(**{"issue_age": ages, "policy_year": years, "cv_per_1000": values})
    groups = cv.groupby(["premium_period", "sex", "issue_age"], dropna=False)
    found = []
    for key, rows in groups:
        name = (f"the schedule of premium_period {key[0]}, sex {key[1]}, issue_age "
                f"{int(key[2])}")
        y = rows["policy_year"]
        whole = bool((y % 1 == 0).all())
        if (not whole or y.min() < 1
                or sorted(y.tolist()) != list(range(int(y.min()), int(y.max()) + 1))):
            raise ValueError(f"{cv_file}: {name} must run in whole policy years from 1 or "
                             f"more, without a gap or a repeat")
        v = rows["cv_per_1000"]
        bad = y[~((v >= 0) & (v < float("inf")))].to_numpy(dtype="int64").tolist()
        if bad:
            found.append(f"{name}, at policy year {bad}")
    if found:
        where = ", nor in ".join(found)
        raise ValueError(f"{cv_file}: cv_per_1000 must be a number, zero or more; it is "
                         f"not in {where}")
    return groups.ngroups


def cv_schedule():
    """Each model point's cash value schedule, its row of :func:`cv_array`: int64 [point].

    The schedule of the point's premium period, sex and issue age, the key
    ``WholeLife_US_S`` looks the cash value up by, matched by value. A point whose key has
    no schedule has 0, a schedule whose extent holds no policy year, so that
    ``Projection.cv_pp_anniv`` refuses every year of it, naming the point, where
    ``WholeLife_US_S``'s lookup raised ``KeyError``. :func:`cv_schedules` has checked the
    table.
    """
    cv_schedules()
    cv = cv_table().reset_index()
    cv = cv.assign(**{"issue_age": pd.to_numeric(cv["issue_age"])})  # noqa: F821
    number = {}
    for key, _ in cv.groupby(["premium_period", "sex", "issue_age"], dropna=False):
        number[(key[0], key[1], int(key[2]))] = len(number) + 1
    table = model_point_table()
    periods, sexes = table["premium_period"].tolist(), table["sex"].tolist()
    out = np.zeros(len(periods), dtype="int64")                      # noqa: F821
    for i in range(len(periods)):
        out[i] = number.get((periods[i], sexes[i], int(issue_age()[i])), 0)
    return out


def cv_array():
    """The guaranteed cash value per $1,000 by schedule and policy year, from
    *cv_table.csv*: float64 [schedule, policy year].

    Row ``s`` is schedule ``s`` (:func:`cv_schedule`) and column ``y`` policy year ``y``,
    so ``Projection.cv_pp_anniv`` reads a point's value at ``[cv_schedule(), y]``. The
    width is the table's last policy year plus one. Row 0, no schedule, and column 0, no
    policy year, hold NaN, and so do the years outside a schedule's
    :func:`cv_year_first` and :func:`cv_year_last`; no formula reads them.
    :func:`cv_schedules` refuses a schedule this array cannot hold.
    """
    n = cv_schedules()
    cv = cv_table().reset_index()
    ages = pd.to_numeric(cv["issue_age"])                            # noqa: F821
    years = pd.to_numeric(cv["policy_year"])                         # noqa: F821
    values = pd.to_numeric(cv["cv_per_1000"])                        # noqa: F821
    cv = cv.assign(**{"issue_age": ages, "policy_year": years, "cv_per_1000": values})
    width = int(cv["policy_year"].max()) + 1 if n else 1
    out = np.full((n + 1, width), np.nan)                            # noqa: F821
    s = 0
    for _, rows in cv.groupby(["premium_period", "sex", "issue_age"], dropna=False):
        s += 1
        y = rows["policy_year"].to_numpy(dtype="int64")
        out[s, y] = rows["cv_per_1000"].to_numpy(dtype="float64")
    return out


def cv_year_first():
    """The first policy year of each cash value schedule: int64 [schedule].

    1 for row 0, no schedule, whose last year is 0, so that no year lies between them. The
    years are read by value, from the schedules :func:`cv_schedules` has checked.
    """
    out = np.ones(cv_schedules() + 1, dtype="int64")                 # noqa: F821
    cv = cv_table().reset_index()
    ages = pd.to_numeric(cv["issue_age"])                            # noqa: F821
    years = pd.to_numeric(cv["policy_year"])                         # noqa: F821
    cv = cv.assign(**{"issue_age": ages, "policy_year": years})
    s = 0
    for _, rows in cv.groupby(["premium_period", "sex", "issue_age"], dropna=False):
        s += 1
        out[s] = int(rows["policy_year"].min())
    return out


def cv_year_last():
    """The last policy year of each cash value schedule: int64 [schedule], 0 for no
    schedule, read as :func:`cv_year_first` reads the first."""
    out = np.zeros(cv_schedules() + 1, dtype="int64")                # noqa: F821
    cv = cv_table().reset_index()
    ages = pd.to_numeric(cv["issue_age"])                            # noqa: F821
    years = pd.to_numeric(cv["policy_year"])                         # noqa: F821
    cv = cv.assign(**{"issue_age": ages, "policy_year": years})
    s = 0
    for _, rows in cv.groupby(["premium_period", "sex", "issue_age"], dropna=False):
        s += 1
        out[s] = int(rows["policy_year"].max())
    return out


def mort_schedules():
    """The number of guaranteed mortality schedules in *mort_table.csv*, one a sex, each
    checked: an int.

    A schedule is the table's rows for one sex, numbered from 1 in the order of the sexes,
    as :func:`mort_schedule` numbers them. An age is read by its value, as
    ``WholeLife_US_S``'s lookup matches it, so one written ``54.0`` is 54; one that is
    not a whole number, text among them, is refused, naming every such age. A schedule
    whose ages leave a gap, repeat or start below 0 is refused, naming its sex. Then
    every ``mort_rate`` must be a number from 0 to 1, a probability, whether or not a
    point carries its sex: ``Projection.mort_rate`` caps the best-estimate rate built on
    it, and the term-blend layer divides by the scale rate. The refusal names every sex
    and age at fault. :func:`mort_table_array`, its extents and :func:`mort_schedule` read
    this first.
    """
    mort = mort_table().reset_index()
    ages = pd.to_numeric(mort["age"], errors="coerce")              # noqa: F821
    bad = mort["age"][~(ages % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{mort_table_file}: an age must be a whole number; {bad} is not")
    rates = pd.to_numeric(mort["mort_rate"], errors="coerce")       # noqa: F821
    mort = mort.assign(age=ages, mort_rate=rates)
    groups = mort.groupby(["sex"], dropna=False)
    found = []
    for key, rows in groups:
        a = rows["age"].to_numpy(dtype="int64").tolist()
        first, last = min(a), max(a)
        if first < 0 or sorted(a) != list(range(first, last + 1)):
            raise ValueError(f"{mort_table_file}: the ages of sex {key[0]} must run from "
                             f"{first} to {last} without a gap or a repeat, none negative")
        q = rows["mort_rate"]
        bad = rows["age"][~((q >= 0) & (q <= 1))].to_numpy(dtype="int64").tolist()
        if bad:
            found.append(f"sex {key[0]}, age {bad}")
    if found:
        where = ", nor at ".join(found)
        raise ValueError(f"{mort_table_file}: mort_rate must be a number from 0 to 1; it "
                         f"is not at {where}")
    return groups.ngroups


def mort_schedule():
    """Each model point's guaranteed mortality schedule, its row of
    :func:`mort_table_array`: int64 [point].

    The schedule of the point's sex, the key ``WholeLife_US_S`` looks the rate up by
    beside the age. A sex the table lacks is 0, a schedule whose extent holds no age, so
    that ``Projection.mort_rate_guar_at`` refuses every age of it, naming the point, where
    ``WholeLife_US_S``'s lookup raised ``KeyError``.
    """
    mort_schedules()
    number = {}
    for key, _ in mort_table().reset_index().groupby(["sex"], dropna=False):
        number[key[0]] = len(number) + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def mort_table_array():
    """Guaranteed mortality by schedule and attained age, from *mort_table.csv*: float64
    [schedule, age].

    Row ``s`` is schedule ``s`` (:func:`mort_schedule`), and each row is padded from age
    0, so that the column index **is** the age, as ``basiclife.BasicTerm_SC`` pads its
    table; the ages below a schedule's first, 0 to 17 as shipped, row 0 and any age past a
    schedule's last hold NaN, which no formula reads. ``Projection.mort_rate_guar_at``
    refuses an age outside the schedule's :func:`mort_age_first` and
    :func:`mort_age_last`, naming the point.
    """
    n = mort_schedules()
    mort = mort_table().reset_index()
    mort = mort.assign(age=pd.to_numeric(mort["age"]))               # noqa: F821
    width = int(mort["age"].max()) + 1 if n else 1
    out = np.full((n + 1, width), np.nan)                            # noqa: F821
    s = 0
    for _, rows in mort.groupby(["sex"], dropna=False):
        s += 1
        a = rows["age"].to_numpy(dtype="int64")
        out[s, a] = pd.to_numeric(rows["mort_rate"]).to_numpy(dtype="float64")  # noqa: F821
    return out


def mort_age_first():
    """The first attained age of each guaranteed mortality schedule: int64 [schedule].

    1 for row 0, no schedule, whose last age is 0, so that no age lies between them. The
    ages are read by value, from the schedules :func:`mort_schedules` has checked.
    """
    out = np.ones(mort_schedules() + 1, dtype="int64")               # noqa: F821
    mort = mort_table().reset_index()
    s = 0
    mort = mort.assign(age=pd.to_numeric(mort["age"]))               # noqa: F821
    for _, rows in mort.groupby(["sex"], dropna=False):
        s += 1
        out[s] = int(rows["age"].min())
    return out


def mort_age_last():
    """The last attained age of each guaranteed mortality schedule: int64 [schedule], 0 for
    no schedule, read as :func:`mort_age_first` reads the first."""
    out = np.zeros(mort_schedules() + 1, dtype="int64")              # noqa: F821
    mort = mort_table().reset_index()
    s = 0
    mort = mort.assign(age=pd.to_numeric(mort["age"]))               # noqa: F821
    for _, rows in mort.groupby(["sex"], dropna=False):
        s += 1
        out[s] = int(rows["age"].max())
    return out


def nsp_schedules():
    """The number of net single premium schedules in *nsp_table.csv*, one a sex, each
    checked: an int.

    Numbered and checked as :func:`mort_schedules` numbers and checks the mortality
    schedules, but for the value: every ``nsp`` must be a number above 0, whether or not
    a point carries its sex, since the paid-up additions are bought by dividing by it and
    their value reaches the dividend's floor. A price per unit of face is no probability,
    and a negative interest rate would take it past 1, so no upper bound is set. The
    refusal names every sex and age at fault. :func:`nsp_array`, its extents and
    :func:`nsp_schedule` read this first.
    """
    nsps = nsp_table().reset_index()
    ages = pd.to_numeric(nsps["age"], errors="coerce")              # noqa: F821
    bad = nsps["age"][~(ages % 1 == 0)].tolist()
    if bad:
        raise ValueError(f"{nsp_file}: an age must be a whole number; {bad} is not")
    values = pd.to_numeric(nsps["nsp"], errors="coerce")            # noqa: F821
    nsps = nsps.assign(age=ages, nsp=values)
    groups = nsps.groupby(["sex"], dropna=False)
    found = []
    for key, rows in groups:
        a = rows["age"].to_numpy(dtype="int64").tolist()
        first, last = min(a), max(a)
        if first < 0 or sorted(a) != list(range(first, last + 1)):
            raise ValueError(f"{nsp_file}: the ages of sex {key[0]} must run from "
                             f"{first} to {last} without a gap or a repeat, none negative")
        v = rows["nsp"]
        bad = rows["age"][~((v > 0) & (v < float("inf")))].to_numpy(dtype="int64").tolist()
        if bad:
            found.append(f"sex {key[0]}, age {bad}")
    if found:
        where = ", nor at ".join(found)
        raise ValueError(f"{nsp_file}: nsp must be a number above 0; it is not at {where}")
    return groups.ngroups


def nsp_schedule():
    """Each model point's net single premium schedule, its row of :func:`nsp_array`:
    int64 [point].

    The schedule of the point's sex, 0 for a sex the table lacks, which
    ``Projection.nsp`` refuses at every age, naming the point, as :func:`mort_schedule`.
    """
    nsp_schedules()
    number = {}
    for key, _ in nsp_table().reset_index().groupby(["sex"], dropna=False):
        number[key[0]] = len(number) + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def nsp_array():
    """The endowment-at-100 net single premium by schedule and attained age, from
    *nsp_table.csv*: float64 [schedule, age].

    Padded from age 0 as :func:`mort_table_array` is, NaN where no formula reads.
    ``Projection.nsp`` refuses an age outside the schedule's :func:`nsp_age_first` and
    :func:`nsp_age_last`, naming the point.
    """
    n = nsp_schedules()
    nsps = nsp_table().reset_index()
    nsps = nsps.assign(age=pd.to_numeric(nsps["age"]))               # noqa: F821
    width = int(nsps["age"].max()) + 1 if n else 1
    out = np.full((n + 1, width), np.nan)                            # noqa: F821
    s = 0
    for _, rows in nsps.groupby(["sex"], dropna=False):
        s += 1
        a = rows["age"].to_numpy(dtype="int64")
        out[s, a] = pd.to_numeric(rows["nsp"]).to_numpy(dtype="float64")  # noqa: F821
    return out


def nsp_age_first():
    """The first attained age of each net single premium schedule: int64 [schedule], 1 for
    no schedule, read as :func:`mort_age_first` reads the mortality table's."""
    out = np.ones(nsp_schedules() + 1, dtype="int64")                # noqa: F821
    nsps = nsp_table().reset_index()
    s = 0
    nsps = nsps.assign(age=pd.to_numeric(nsps["age"]))               # noqa: F821
    for _, rows in nsps.groupby(["sex"], dropna=False):
        s += 1
        out[s] = int(rows["age"].min())
    return out


def nsp_age_last():
    """The last attained age of each net single premium schedule: int64 [schedule], 0 for
    no schedule."""
    out = np.zeros(nsp_schedules() + 1, dtype="int64")               # noqa: F821
    nsps = nsp_table().reset_index()
    s = 0
    nsps = nsps.assign(age=pd.to_numeric(nsps["age"]))               # noqa: F821
    for _, rows in nsps.groupby(["sex"], dropna=False):
        s += 1
        out[s] = int(rows["age"].max())
    return out


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

cv_file = "cv_table.csv"

nsp_file = "nsp_table.csv"

np_guar_file = "np_guar_table.csv"

mort_table_file = "mort_table.csv"

premium_rates_file = "premium_rates.csv"

future_horizon_mth = 120

pd = ("Module", "pandas")

np = ("Module", "numpy")