# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.RILA_US_SEC.Projection` as ``data``. :mod:`~.RILA_US_SEC.Projection` is
parameterized by ``idx``, a point's position in the table, so each ``Projection[i]`` is a
separate ItemSpace with its own cells cache; if the readers lived there, every model point
would re-read every file. Holding them in an unparameterized Space reads each file once no
matter how many contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/registered_index_linked_annuity/``, rather than data stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RILA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

**Five of the tables are RILA_US_S's.** The mortality table, the withdrawal charge
schedule, the guaranteed minimum rates, the base surrender rates and the withdrawal
programmes are the files :mod:`~.RILA_US_S` reads, read here in place by ``RILA_US_S``'s
own readers: one copy of each table serves both models, so an edit to one reaches both.
The model point table and the market scenarios are this model's own,
``model_point_table_sec.csv`` and ``market_scenario_sec.csv``; they sit beside
``RILA_US_S``'s ``model_point_table.csv`` and ``market_scenario.csv``, which this model
never opens.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader cell:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table_sec.csv
mort_table_file            mort_table()                    mort_table.csv
market_scenario_file       market_scenario()               market_scenario_sec.csv
surr_charge_file           surr_charge_table()             surr_charge_table.csv
guar_min_rate_file         guar_min_rate_table()           guar_min_rate_table.csv
lapse_file                 lapse_table()                   lapse_table.csv
withdrawal_file            withdrawal_table()              withdrawal_table.csv
=========================  ==============================  ==========================

**The model point table is checked as it is read.** Fifteen of its columns are the
in-force interface: ``policy_count`` and ``duration_mth``, as in ``basiclife.BasicTerm_SE``,
and the thirteen columns of a contract's opening state — the investment amount, the Fixed
and Holding Accounts, the account value, the account value at the anniversary on or before
the valuation date, the free withdrawal amount still unused, the return-of-premium base,
and, where the term under way began before the valuation month, the five market values of
its Term Start Date and the cap re-solved there. :func:`model_point_table` refuses a table
that lacks any of them, repeats a ``point_id``, holds a count, a duration, a contract term
or an opening state no contract can have, or a key its tables do not hold. The checks run
in turn, and the first that fails raises, naming the missing column or every point that
fails it. It also refuses a policy to be issued more than ``future_horizon_mth`` months
after the valuation date, 120 months as shipped: future new business is written over a
stated horizon, so that no frame runs longer than cover from issue plus that horizon. Set
to 0, the Reference refuses future new business altogether. Two rules of the product
rather than of the table need ``Projection`` References, and ``Projection.proj_len``
checks them: whether a point is still in cover at the valuation date, and whether the free
withdrawal amount it carries is within the contract year's, where that year's base is 0 or
more.

**So are the five assumption tables and the scenarios**, each by a count cell beside its
reader, which is ``RILA_US_S``'s, unchanged: :func:`market_scenario_count`,
:func:`mort_table_count`, :func:`surr_charge_count`, :func:`guar_min_rate_count`,
:func:`lapse_table_count` and :func:`withdrawal_count`. Each reads its table's keys by
value, once, as the join in ``Projection`` matches them, so that a month written ``36.0``
is 36, and refuses a key that is blank, text or not a whole number, and a key on more than
one row; where a reader reads every key from the first to the last, a gap too. Each
refuses a value that is blank, text, infinite or outside its range, every value a cap, a
``min`` or a ``max`` reads among them, which would lose a blank without a word. Every
message names the file, the column and the lines at fault. ``Data``'s vectors and
arrays, which ``Projection`` reads, ask for their table's count before they are built, and
``Projection``'s lapse and surrender-charge readers ask it themselves, so a projection
meets the checks first.

``market_scenario`` is the file peculiar to this product. A RILA's *contractual* formula
consumes market data — an index level, a Constant Maturity Treasury yield at the term's
maturity, an implied volatility and a dividend yield — so the market state is an input
class of its own alongside the contractual, declared and behavioural classes, not a
valuation overlay. It is indexed by ``(scenario_id, month_end)`` and read as a step
function of the month end: each row states the market state that holds from that month
end until the next row of the same scenario, so the notes' Scenario A is three rows.

``month_end`` is a **time** in months from the **valuation date**, ``0`` at the valuation
date: the market runs on the valuation clock, which every model point of a block shares.
``market_scenario_sec.csv`` holds ``RILA_US_S``'s scenarios as they stand, under their own
ids, which on a contract issued at the valuation date is ``RILA_US_S``'s own clock, and
for each model point restated in force or issued later a copy of its scenario re-based to
that point's month, under an id of its own. ``Projection.market_state`` reads the file at
the month end ``t + 1`` for the state month ``t`` is valued at, and, for a term that
starts at or after the valuation date, at the time its Term Start Date falls at — a month
*start*; a term that began before the valuation date reads its start from the model point
instead. The name records the commoner of those two uses and not the key's meaning: the
key is a general time, and the row every scenario opens with, ``month_end = 0``, is the
valuation date, an instant no month ends at.

``withdrawal_table`` is indexed by ``(wd_schedule_id, month_end)``, the **policy** month
end the withdrawal is taken at, counted from the Issue Date: the withdrawal programme is a
contractual schedule and stays on the policy clock, and a month end with no row takes no
scheduled withdrawal. ``surr_charge_table`` is indexed by complete contract years
``cy = 0 .. 6``, an elapsed count that is 0-based already; ``guar_min_rate_table`` by
``term_years``, the contractual floors on the declared Cap, Step and Edge rates at 1, 3 and
6 years [S1][S2]; and ``lapse_table`` by ``contract_year`` - the 1-based contractual label,
read through ``Projection.policy_year`` - as a step function, so the notes' three-row
reference shape stays three rows.

To swap in the prescribed mortality basis — the 2012 IAM **Basic** table (VM-M §2.C) with
generational Projection Scale G2 [REG-R59], which may not be redistributed here — replace
``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a different
name, before the model computes anything. No formula changes. Replacing a file changes
:mod:`~.RILA_US_S` too, which reads the same one. The same is true of the market data: a
production implementation supplies a volatility *surface* rather than the flat scalar
shipped here, and that is a change to the scenario file plus a strike-and-maturity
lookup, not to the crediting or interim-value formulas.

A compiled model clears no cache, so there a file name is set on a package just imported,
before anything is read.

**The vectors.** The readers and the checked tables return what the files hold, and no
:mod:`~.RILA_US_SEC.Projection` cell but ``model_point``, a reporting cell, reads them.
The others read the arrays below instead, one element at a time, a model point's
attribute being the element at its position, ``data.premium()[idx]``. That is what lets
the model compile to C, as ``basiclife.BasicTerm_SC`` does: each array is a numpy vector
or table of int64 or float64, which compiles to a typed memoryview, never one of bools,
objects or text, and each count and extent is an int.

Text the projection needs is decoded here, into the number it selects: each value of the
three categorical columns ``RILA_US_S`` branches on, ``crediting_type``, ``iv_family`` and
``amort_rule``, into a 0/1 flag, the ten ``is_*`` cells, the ``nge_reset`` flag into
another, and a blank ``declared_cap``, an uncapped option, into a third. Each table keyed
by more than a number becomes an integer-indexed array: the mortality table, the scenarios
and the withdrawal programmes are numbered, each point carrying the number of its own,
``mort_schedule``, ``scenario_number`` and ``wd_schedule_number``, all three numbered from
1 in the sorted order of their keys; the mortality is held by attained age, the surrender
charge by complete contract year, the scenarios step-filled by valuation month and the
programmes by policy month end, so that the age, the year or the month is the index; the
guaranteed minimum rates are joined to each point's term; and the lapse table, a short
step function keyed by contract years no contract bounds, stays two row vectors, scanned
by its one reader:

====================================  =======  ===================  ======================
Cells                                 dtype    Shape                From
====================================  =======  ===================  ======================
point_id()                            int64    [point]              the table's index
age_at_entry(), duration_mth()        int64    [point]              the two columns, 0
                                                                    where too large
term_years()                          int64    [point]              ``term_years``, the
                                                                    same
age_at_entry_ok() and two more        int64    [point]              1 where an int64
                                                                    holds the value
policy_count() .. wd_rate_ann()       float64  [point]              ``policy_count``,
                                                                    ``premium`` and seven
                                                                    more
inv_amt_pp_init() and twelve more     float64  [point]              the thirteen columns
                                                                    of the opening state
nge_reset()                           int64    [point]              the checked flag
is_uncapped()                         int64    [point]              ``declared_cap``
                                                                    blank
cap_uncapped()                        float    scalar               ``+inf``
is_cap_crediting() and nine more      int64    [point]              the ten decodes, 1 on
                                                                    the value
guar_min_cap(), guar_min_step(),      float64  [point]              the point's term's
guar_min_edge()                                                     row, joined
scenario_count()                      int      scalar               the companion
scenario_number()                     int64    [point]              ``scenario_id``,
                                                                    joined
scenario_first_mths()                 int64    [scenario]           each first ``t``
scenario_last_mth()                   int      scalar               ``read_last_mth``
index_level_array() and four more     float64  [scenario, t]        step-filled, one a
                                                                    scenario column
mort_sexes()                          int      scalar               *mort_table.csv*
mort_schedule()                       int64    [point]              ``sex``, joined
mort_age_firsts(), mort_age_lasts()   int64    [schedule]           each sex's ages
mort_age_held()                       int      scalar               ``read_last_age``
mort_rate_array()                     float64  [schedule, age]      *mort_table.csv*
surr_charge_array()                   float64  [cy]                 *surr_charge_table.csv*
lapse_years(), lapse_rates()          float64  [row]                *lapse_table.csv*
wd_schedule_count()                   int      scalar               *withdrawal_table.csv*
wd_schedule_number()                  int64    [point]              ``wd_schedule_id``,
                                                                    joined
wd_last_mth()                         int      scalar               ``read_last_mth``
wd_amount_array()                     float64  [programme, m]       ``wd_amount``, 0.0
                                                                    without a row
====================================  =======  ===================  ======================

The table checks are what they were, :func:`model_point_table` and the six checked
tables, beside their int counts, and their refusals are stage ``E``'s, messages included.
No copy of the numeric columns is read beside the table: :func:`model_point_table`
refuses every numeric column the projection reads, by column and point, where it is
blank, text or out of range, so each vector is the checked column, read as
``RILA_US_S``'s ``float()``, ``int()`` or ``bool()`` reads it.

**Every array is held to the last age or month a read reaches.** Two References say
where: ``read_last_mth``, 1,202, the last element of ``Projection``'s ``t`` cache,
``12 x max(maturity_age - issue_age_min, maturity_min_years) + future_horizon_mth + 2``,
and ``read_last_age``, 121, the last element of its ``a`` cache,
``max(maturity_age, issue_age_max + maturity_min_years)``, both derived in
``spec_sec.py``, since ``Data`` cannot read ``Projection``'s References; a test holds
each to the spec. The scenarios are held by valuation month to ``read_last_mth``, a
scenario's last row holding to the end, as ``RILA_US_S``'s step function holds it, and
the programmes by policy month end to the same month; the mortality is held by age to
``read_last_age``. So a key far past any read, which ``RILA_US_S`` holds and never
reaches, neither widens an array nor refuses a point ``RILA_US_S`` projects: it is
dropped before it is cast, whatever its size, ``1e20`` or ``2**60`` among them. A read
past an array, which no projection makes, is refused by its reader in
:mod:`~.RILA_US_SEC.Projection`, naming the point, rather than clamped. The mortality is
indexed from age 0, where no attained age is below; a sex's first and last ages are held
as read, clamped to ``-1 .. read_last_age + 1``, so that a table rating more than the
array holds is told apart from one rating less (``Projection.proj_len``). A change to
``maturity_age``, ``maturity_min_years``, ``issue_age_min``, ``issue_age_max`` or
``future_horizon_mth`` needs both References recomputed with the spec.

**An array is read by element, never whole,** in this Space as in
:mod:`~.RILA_US_SEC.Projection`. The compiler types an array cell as a memoryview only
once it has seen that every use of it, in either Space, is an element read: one ``len()``,
slice, loop over it or numpy call on it anywhere, and the cell compiles as a Python
object. So an array derived here reads the table's column itself, never another cell's
array, and a width comes from a table or a count cell. Each table's check is the one cell
that every array, extent and number of the table reads first, so that a projection, which
reads an extent or a number first, meets the same refusal as a reader of the array. A
keyword named as a cell of this Space would be rewritten by the export, so none is
passed, and a local of a formula is named apart from the cells.

**What cannot be decoded is refused,** when the vector is first read, naming every point
at fault, where it is not ``RILA_US_S``'s reading: a ``point_id`` that is not a whole
number below ``2**53``. A decode compares the text exactly, element by element, as
``RILA_US_S`` compares it, so a value written in another case or with a space, ``Cap``,
or ``CAP`` with a leading space, is no flag, and the projection answers as ``RILA_US_S``
answers it, raising ``invalid crediting_type``, ``invalid iv_family`` or ``invalid
amort_rule`` where it raises it. A join number maps the point's key as ``RILA_US_S``'s
``.loc`` matches it, by the value pandas read, and :func:`model_point_table` has refused a
key its table lacks. A read beyond a table's extent is refused where ``RILA_US_S``'s
lookup raised, by the one :mod:`~.RILA_US_SEC.Projection` cell that reads the table,
naming the point: an attained age outside the sex's in ``mort_rate_base_at``, a month
before the scenario's first in ``market_state``, a contract year before the lapse
table's first in ``lapse_rate_base_py``, each a ``ValueError`` where ``RILA_US_S`` raised
``KeyError`` or its own message. A year past the charge schedule, and a month end a
programme has no row at, are no charge and no withdrawal, as there.

**An int64 holds what it is read from.** A float past int64 casts to the least int64
without a word, so a number read into an int64 vector is refused unless it is below
``2**53`` in size, where the int64 holds ``RILA_US_S``'s reading of it: the ``point_id``
(:func:`point_id`), at its first read, and ``term_years``, which
*guar_min_rate_table.csv* may floor at any whole number, ``age_at_entry`` and
``duration_mth``, by the point's own ``Projection`` accessor, through
:func:`term_years_ok`, :func:`age_at_entry_ok` and :func:`duration_mth_ok`, so that no
point is refused for another's value. ``RILA_US_S`` projects such a term, so that is a
recorded refusal; an issue age or a duration of that size passes
:func:`model_point_table` only where the mortality table rates the attained age it
reaches, a table of one row there, and ``RILA_US_S`` projects it too. A table key is never
cast before its hold has dropped it.
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

    Indexed by ``point_id``. Fifteen columns are the in-force interface: ``policy_count``,
    the contracts the point stands for, and ``duration_mth``, the months elapsed from issue
    at the valuation date, as in ``basiclife.BasicTerm_SE``; then the opening state, per
    contract, as it stands at the start of month 0, before any month-0 event:

    * ``inv_amt_pp_init``: the Investment Amount entering month 0, the notional the
      month's crediting and interim value apply to;
    * ``fixed_acct_pp_init`` and ``holding_acct_pp_init``: the Fixed and Holding Accounts;
    * ``av_pp_init``: the Account Value, after the previous month's withdrawal;
    * ``av_pp_prev_anniv_init``: the Account Value before withdrawals at the Contract
      Anniversary on or before the valuation date, the base of the contract year's Free
      Withdrawal Amount; the purchase payment in the first contract year;
    * ``free_wd_remain_init``: the Free Withdrawal Amount still unused in the contract year;
    * ``rop_pp_init``: the return-of-premium death benefit base;
    * ``index_at_term_start_init``, ``mvr_at_term_start_init``,
      ``risk_free_at_term_start_init``, ``div_yield_at_term_start_init`` and
      ``impl_vol_at_term_start_init``: where the term under way began before the valuation
      month, the index level, the Market Value Rate and the option-pricing market on its
      Term Start Date; blank otherwise;
    * ``cap_rate_init``: where that term began at a renewal under ``nge_reset``, the cap
      re-solved there; blank otherwise.

    The rest are ``RILA_US_S``'s, ``pols_if_init`` renamed ``policy_count``, except
    ``row_kind``, ``source_policy_id`` and ``source_mth``, which record where the
    generator took each shipped row from and which no formula reads.

    The checks run over the whole table at once, and the first that fails raises
    ``ValueError``, naming the missing column or every point it fails on. First the
    table's own shape:

    * the fifteen in-force columns are present;
    * no ``point_id`` appears twice;
    * ``policy_count`` is a number, zero or more;
    * ``duration_mth`` is a whole number of months, read by value, so that ``12.0`` is
      12: positive for a contract in force, 0 for one issued at the valuation date,
      negative for one issued later;
    * no policy is issued more than ``future_horizon_mth`` months after the valuation
      date, so ``duration_mth`` is ``-future_horizon_mth`` or more. At 0 the model takes
      no future new business, and the message says so; a negative horizon is itself
      refused.

    Then the contract's terms, ``term_years`` before every check that reads the term
    clock:

    * ``age_at_entry`` is a whole number of years, 0 or more, and ``term_years`` a whole
      number of years, 1 or more, each read by value; ``RILA_US_S`` reads both by
      ``int()``, which truncates a fraction without a word, and the term clock counts
      months modulo ``12 x term_years``;
    * ``premium`` is a number above 0, the purchase payment;
    * ``buffer`` and ``floor_rate`` are fractions, 0 or more and below 1, each the strike
      ``I_s (1 - x)`` of a put; ``participation`` is a number above 0, by which the cap's
      strike divides;
    * ``declared_cap`` is blank, for an uncapped option, or a number, zero or more, and
      ``declared_step``, ``declared_edge`` and ``wd_rate_ann`` are numbers, zero or more:
      each reaches a ``max`` or a ``min`` that would lose a blank;
    * ``nge_reset`` is a flag, read by value: ``True`` or ``False``, as pandas reads
      either, or 1 or 0, where ``RILA_US_S``'s ``bool()`` reads any text, a blank among
      them, as ``True``;
    * ``nge_reset`` is set only on a capped Cap Rate option, ``crediting_type`` ``CAP``
      with ``declared_cap`` given. ``RILA_US_S``'s solver prices the at-the-money call,
      the call at the cap and the buffer's put: on a Floor option it would solve the
      wrong portfolio, and on a Step, an Edge or an uncapped option the flag does nothing,
      and ``RILA_US_S`` projects either without a word.

    Then the opening state:

    * the investment amount, the two accounts, the free withdrawal amount unused and the
      return-of-premium base are numbers, zero or more; the account value and the account
      value at the anniversary are finite numbers of either sign, the interim value being
      able to fall below 0 under the contract [S2];
    * each term-start value, where given, is a number in its range: the index level and
      the volatility above 0, the index being what ``Projection.index_perf`` divides by;
      the Market Value Rate, the risk-free rate and the dividend yield above -1, each
      added to 1 under a division or a logarithm; the cap a finite number;
    * a contract not yet in force, ``duration_mth`` 0 or less, holds nothing yet: its
      seven amounts are 0, and it enters with its purchase payment in its issue month;
    * the five term-start values are given exactly where the term under way began before
      the valuation month, ``duration_mth`` positive and not a multiple of
      ``12 x term_years``, and ``cap_rate_init`` exactly where, besides, that term began
      at a renewal, ``duration_mth`` above ``12 x term_years``, under ``nge_reset``: at or
      after the valuation month the projection reads a term's start from the scenario, and
      a cap re-solves there, or is the declared cap. A table written with the value
      entering month 0 on every row is refused here;
    * a contract in force holds an investment amount or an account balance;
      ``RILA_US_S`` reaches a contract holding nothing only by a full withdrawal;
    * ``rop_pp_init`` is at most the purchase payment, to a cent: withdrawals only reduce
      the base;
    * in the first contract year, ``duration_mth`` 1 to 11, ``free_wd_remain_init`` is 0,
      to a cent, the year having no free withdrawal amount, and ``av_pp_prev_anniv_init``
      is the purchase payment, to a cent, the year having opened at issue;
    * before the first Term End Date, ``duration_mth`` 1 to ``12 x term_years - 1``, the
      Fixed and Holding Accounts are 0, to a cent: only a term end transfers to them;
    * on a renewal valuation, ``duration_mth`` a positive multiple of
      ``12 x term_years``, ``av_pp_init`` is the investment amount plus the two accounts,
      to two and a half cents: the month before closed a term, where the interim value is
      the Investment Amount itself. Carried to the cent, each of the four amounts is within
      half a cent of its exact value, so the identity can miss by two cents, and floating
      point may read that as a little more;
    * on an anniversary valuation, ``duration_mth`` a positive multiple of 12,
      ``av_pp_prev_anniv_init``, the account value before the anniversary's withdrawal, is
      at least ``av_pp_init``, the value after it, to a cent.

    Last, each point's keys into the tables it is joined with, each table's count cell
    asked first, so that a malformed table is refused by its own message:

    * ``scenario_id`` names a scenario of ``market_scenario_file`` that sets its levels by
      the point's first month on the books, ``t = 0`` or its issue month if later;
    * ``wd_schedule_id`` names a programme of ``withdrawal_file``;
    * ``term_years`` is a term of ``guar_min_rate_file``;
    * ``mort_table_file`` rates the point's sex at its attained age in its first month on
      the books;
    * ``cap_rate_init``, where given, is at least the guaranteed minimum cap of its term,
      which ``Projection.cap_rate`` floors every re-solved cap at.

    An extract may carry each amount of money to the cent, as an administration system
    holds it, each within half a cent of its exact value, and every rule between amounts
    allows for that without a tie falling to floating point: a cent where a rule compares
    one amount with another or with 0, and two and a half cents in the renewal rule, whose
    four amounts rounding can move apart by two.

    The table is returned with the columns those checks read by value as the numbers they
    were checked as: ``duration_mth``, ``age_at_entry`` and ``term_years`` int64, or
    float64 where a value of the column is ``2**53`` or more in size, which an int64
    cannot be trusted to hold and ``Projection`` refuses for its own point;
    ``policy_count``, ``premium``, the rates and the thirteen opening-state columns
    float64, blank as NaN; and ``nge_reset`` the flags it was checked as. What it cannot
    check, ``Projection.proj_len`` does where it can: whether the point is still in cover
    at the valuation date, which needs ``maturity_age`` and ``maturity_min_years``, and
    whether the free withdrawal amount unused is within the contract year's, where the
    year's base is 0 or more, which needs ``free_wd_rate``. A mortality table that stops
    before the age the last covered year is entered at is refused by
    ``Projection.proj_len``, naming the point. Left to the projection: whether a
    term-start value is the one the point's history ran on, since no scenario holds a path
    before ``t = 0``.
    """
    name = model_point_file                                          # noqa: F821
    table = pd.read_csv(input_dir() / name, index_col="point_id")    # noqa: F821
    balances = ("inv_amt_pp_init", "fixed_acct_pp_init", "holding_acct_pp_init",
                "free_wd_remain_init", "rop_pp_init")
    signed = ("av_pp_init", "av_pp_prev_anniv_init")
    market = ("index_at_term_start_init", "mvr_at_term_start_init",
              "risk_free_at_term_start_init", "div_yield_at_term_start_init",
              "impl_vol_at_term_start_init")
    amounts = ("inv_amt_pp_init", "fixed_acct_pp_init", "holding_acct_pp_init",
               "av_pp_init", "av_pp_prev_anniv_init", "free_wd_remain_init", "rop_pp_init")
    state = (*amounts, *market, "cap_rate_init")
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
    checked = {"policy_count": count.astype("float64"),        # an int64 holds no
               "duration_mth": months.astype(                  # value of 2**53 or more
                   "float64" if (~(months.abs() < 2.0 ** 53)).any() else "int64")}
    ages = pd.to_numeric(table["age_at_entry"], errors="coerce")     # noqa: F821
    bad = table.index[~((ages % 1 == 0) & (ages >= 0))].tolist()
    if bad:
        raise ValueError(f"{name}: age_at_entry must be a whole number of years, 0 or "
                         f"more; it is not at point_id {bad}")
    checked["age_at_entry"] = ages.astype(
        "float64" if (~(ages.abs() < 2.0 ** 53)).any() else "int64")
    term = pd.to_numeric(table["term_years"], errors="coerce")       # noqa: F821
    bad = table.index[~((term % 1 == 0) & (term >= 1))].tolist()
    if bad:
        raise ValueError(f"{name}: term_years must be a whole number of years, 1 or more: "
                         f"the term clock counts months modulo 12 x term_years; it is not "
                         f"at point_id {bad}")
    checked["term_years"] = term.astype(
        "float64" if (~(term.abs() < 2.0 ** 53)).any() else "int64")
    premium = pd.to_numeric(table["premium"], errors="coerce")       # noqa: F821
    bad = table.index[~((premium > 0) & (premium < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: premium must be a number above 0, the purchase "
                         f"payment; it is not at point_id {bad}")
    checked["premium"] = premium.astype("float64")
    for column in ("buffer", "floor_rate"):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~((value >= 0) & (value < 1))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a fraction, 0 or more and below 1, "
                             f"the strike of a put below the index at the Term Start "
                             f"Date; it is not at point_id {bad}")
        checked[column] = value.astype("float64")
    value = pd.to_numeric(table["participation"], errors="coerce")   # noqa: F821
    bad = table.index[~((value > 0) & (value < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: participation must be a number above 0, by which the "
                         f"cap's strike divides; it is not at point_id {bad}")
    checked["participation"] = value.astype("float64")
    cap = pd.to_numeric(table["declared_cap"], errors="coerce")      # noqa: F821
    bad = table.index[~(table["declared_cap"].isna()
                        | ((cap >= 0) & (cap < float("inf"))))].tolist()
    if bad:
        raise ValueError(f"{name}: declared_cap must be blank, for an uncapped option, or "
                         f"a number, zero or more; it is not at point_id {bad}")
    checked["declared_cap"] = cap.astype("float64")
    for column in ("declared_step", "declared_edge", "wd_rate_ann"):
        value = pd.to_numeric(table[column], errors="coerce")        # noqa: F821
        bad = table.index[~((value >= 0) & (value < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is not "
                             f"at point_id {bad}")
        checked[column] = value.astype("float64")
    flag = table["nge_reset"].astype(str).str.strip().str.lower()
    reset = flag.isin(["true", "1", "1.0"])
    bad = table.index[~(reset | flag.isin(["false", "0", "0.0"]))].tolist()
    if bad:
        raise ValueError(f"{name}: nge_reset must be True or False, a flag; it is not at "
                         f"point_id {bad}")
    checked["nge_reset"] = reset
    capped = (table["crediting_type"] == "CAP") & table["declared_cap"].notna()
    bad = table.index[reset & ~capped].tolist()
    if bad:
        raise ValueError(f"{name}: nge_reset re-solves the cap of a capped Cap Rate "
                         f"option, crediting_type CAP with declared_cap given; it is set "
                         f"at point_id {bad}, where there is no cap to re-solve or the "
                         f"solver would price the Cap Rate portfolio for another crediting "
                         f"method")
    values = {c: pd.to_numeric(table[c], errors="coerce") for c in state}  # noqa: F821
    for column in balances:
        v = values[column]
        bad = table.index[~((v >= 0) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a number, zero or more; it is "
                             f"not at point_id {bad}")
    for column in signed:
        v = values[column]
        bad = table.index[~((v > -float("inf")) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a finite number, of either sign, "
                             f"the interim value being able to fall below 0; it is not at "
                             f"point_id {bad}")
    for column, low, what in (
            ("index_at_term_start_init", 0.0, "above 0, the index level index_perf "
             "divides by"),
            ("mvr_at_term_start_init", -1.0, "above -1, 1 + mvr dividing the interim "
             "value's rate adjustment"),
            ("risk_free_at_term_start_init", -1.0, "above -1, an annual effective rate"),
            ("div_yield_at_term_start_init", -1.0, "above -1, an annual effective rate"),
            ("impl_vol_at_term_start_init", 0.0, "above 0, the volatility the option "
             "prices divide by")):
        v = values[column]
        bad = table.index[table[column].notna()
                          & ~((v > low) & (v < float("inf")))].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank or a number {what}; it is "
                             f"not at point_id {bad}")
    v = values["cap_rate_init"]
    bad = table.index[table["cap_rate_init"].notna()
                      & ~((v > -float("inf")) & (v < float("inf")))].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be blank or a finite number; it is "
                         f"not at point_id {bad}")
    issued = months <= 0
    for column in amounts:
        bad = table.index[issued & (values[column] != 0)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 on a policy not yet in force, "
                             f"duration_mth 0 or less, which enters with its purchase "
                             f"payment in its issue month; it is not at point_id {bad}")
    in_force = months > 0
    mid_term = in_force & (months % (12 * term) != 0)
    for column in market:
        given = table[column].notna()
        bad = table.index[mid_term & ~given].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be given where the term under way "
                             f"began before the valuation month; it is blank at point_id "
                             f"{bad}")
        bad = table.index[~mid_term & given].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be blank unless the term under way "
                             f"began before the valuation month: at or after it the "
                             f"projection reads the term start from the scenario; it is "
                             f"given at point_id {bad}")
    renewed = mid_term & (months > 12 * term) & reset
    given = table["cap_rate_init"].notna()
    bad = table.index[renewed & ~given].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be given where the term under way "
                         f"began at a renewal under nge_reset before the valuation month; "
                         f"it is blank at point_id {bad}")
    bad = table.index[~renewed & given].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be blank unless the term under way "
                         f"began at a renewal under nge_reset before the valuation month: "
                         f"elsewhere the cap is the declared cap, or is re-solved from the "
                         f"scenario; it is given at point_id {bad}")
    held = (values["inv_amt_pp_init"] + values["fixed_acct_pp_init"]
            + values["holding_acct_pp_init"])
    bad = table.index[in_force & (held == 0)].tolist()
    if bad:
        raise ValueError(f"{name}: a contract in force must hold an investment amount or "
                         f"an account balance; none does at point_id {bad}")
    cent = 0.01
    bad = table.index[~(values["rop_pp_init"] <= premium + cent)].tolist()
    if bad:
        raise ValueError(f"{name}: rop_pp_init must be at most the premium, to a cent: "
                         f"withdrawals only reduce the return-of-premium base; it is not "
                         f"at point_id {bad}")
    first_year = in_force & (months < 12)
    bad = table.index[first_year & ~(values["free_wd_remain_init"] <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: free_wd_remain_init must be 0 in the first contract "
                         f"year, duration_mth 1 to 11, which has no free withdrawal "
                         f"amount; it is not at point_id {bad}")
    gap = (values["av_pp_prev_anniv_init"] - premium).abs()
    bad = table.index[first_year & ~(gap <= cent)].tolist()
    if bad:
        raise ValueError(f"{name}: av_pp_prev_anniv_init must be the premium in the first "
                         f"contract year, duration_mth 1 to 11, the year having opened at "
                         f"issue; it is not at point_id {bad}")
    first_term = in_force & (months < 12 * term)
    for column in ("fixed_acct_pp_init", "holding_acct_pp_init"):
        bad = table.index[first_term & ~(values[column] <= cent)].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be 0 before the first Term End "
                             f"Date, duration_mth 1 to 12 x term_years - 1: only a term "
                             f"end transfers to it; it is not at point_id {bad}")
    renewal = in_force & (months % (12 * term) == 0)
    gap = (values["av_pp_init"] - held).abs()
    slack = 2.5 * cent          # half a cent from each of the four amounts, and half more
    bad = table.index[renewal & ~(gap <= slack)].tolist()
    if bad:
        raise ValueError(f"{name}: on a renewal valuation, duration_mth a multiple of 12 x "
                         f"term_years, av_pp_init must be inv_amt_pp_init + "
                         f"fixed_acct_pp_init + holding_acct_pp_init, to two and a half "
                         f"cents: the month before closed a term, where the interim value "
                         f"is the Investment Amount; it is not at point_id {bad}")
    anniversary = in_force & (months % 12 == 0)
    low = values["av_pp_init"] - cent
    bad = table.index[anniversary & ~(values["av_pp_prev_anniv_init"] >= low)].tolist()
    if bad:
        raise ValueError(f"{name}: on an anniversary valuation av_pp_prev_anniv_init, the "
                         f"account value before the anniversary's withdrawal, must be at "
                         f"least av_pp_init, the value after it, to a cent; it is not at "
                         f"point_id {bad}")
    # Each point's keys into the tables it is joined with, each table checked first.
    entry = (-months).clip(lower=0)         # the first month the point is on the books
    scenarios, programmes = market_scenario_file, withdrawal_file    # noqa: F821
    floors_file, rates_file = guar_min_rate_file, mort_table_file    # noqa: F821
    market_scenario_count()
    steps = market_scenario().reset_index()
    first = pd.to_numeric(steps["month_end"],                         # noqa: F821
                          errors="coerce").groupby(steps["scenario_id"]).min()
    bad = table.index[~(table["scenario_id"].map(first) <= entry)].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must name a scenario of {scenarios} that "
                         f"sets its levels by the point's first month on the books, t = 0 "
                         f"or its issue month if later; it does not at point_id {bad}")
    withdrawal_count()
    held_ids = withdrawal_table().index.get_level_values("wd_schedule_id")
    bad = table.index[~table["wd_schedule_id"].isin(held_ids)].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must name a programme of {programmes}; "
                         f"it does not at point_id {bad}")
    guar_min_rate_count()
    floors = guar_min_rate_table()
    terms = pd.to_numeric(floors.index.to_series(), errors="coerce")  # noqa: F821
    bad = table.index[~term.isin(terms)].tolist()
    if bad:
        raise ValueError(f"{name}: term_years must be a term of {floors_file}; it is not "
                         f"at point_id {bad}")
    mort_table_count()
    rates = mort_table().reset_index()
    rated = pd.to_numeric(rates["age"], errors="coerce")             # noqa: F821
    youngest = rated.groupby(rates["sex"]).min()
    oldest = rated.groupby(rates["sex"]).max()
    attained = ages + months.clip(lower=0) // 12
    sexes = table["sex"]
    bad = table.index[~((attained >= sexes.map(youngest))
                        & (attained <= sexes.map(oldest)))].tolist()
    if bad:
        raise ValueError(f"{name}: {rates_file} must rate the point's sex at its attained "
                         f"age in its first month on the books; it does not at point_id "
                         f"{bad}")
    minimum = pd.Series(                                             # noqa: F821
        pd.to_numeric(floors["guar_min_cap"], errors="coerce").to_numpy(),  # noqa: F821
        index=terms.to_numpy())
    cap_given = table["cap_rate_init"].notna()
    bad = table.index[cap_given
                      & ~(values["cap_rate_init"] >= term.map(minimum))].tolist()
    if bad:
        raise ValueError(f"{name}: cap_rate_init must be at least guar_min_cap for its "
                         f"term in {floors_file}; it is not at point_id {bad}")
    return table.assign(**checked, **{c: values[c].astype("float64") for c in state})


def mort_table():
    """Annual mortality by attained age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def market_scenario():
    """The exogenous market-data scenarios, read from *market_scenario_sec.csv*.

    Indexed by ``(scenario_id, month_end)`` and read as a step function of the month end:
    each row states the index level, the Market Value Rate, the risk-free rate, the
    dividend yield and the implied volatility that hold from that month end until the next
    row of the same scenario. ``month_end`` is a time in months from the **valuation
    date**, ``0`` at the valuation date, one more than the index ``t`` of the projection
    month it closes. ``RILA_US_S``'s scenarios stand under their own ids, which on a
    contract issued at the valuation date is ``RILA_US_S``'s own clock; each model point
    restated in force or issued later reads its own copy, re-based to its month, which
    holds no level before the point's issue month. :func:`market_scenario_count` checks
    the table, and ``Data``'s scenario arrays, which ``Projection.market_state`` reads, ask
    for the count before they are built.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / market_scenario_file,                          # noqa: F821
        index_col=["scenario_id", "month_end"])


def surr_charge_table():
    """The withdrawal charge schedule by complete contract year.

    Read from *surr_charge_table.csv*, ``RILA_US_S``'s file, in place, and checked by
    :func:`surr_charge_count`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="contract_year")   # noqa: F821


def guar_min_rate_table():
    """The guaranteed minimum Cap, Step and Edge rates by term.

    Read from *guar_min_rate_table.csv*, ``RILA_US_S``'s file, in place, and checked by
    :func:`guar_min_rate_count`.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / guar_min_rate_file, index_col="term_years")    # noqa: F821


def lapse_table():
    """The un-shocked base annual surrender rate by contract year, from *lapse_table.csv*.

    The charge-expiry shock is not in this file: its size is the ``lapse_shock_mult``
    Reference on ``Projection`` and the year it lands in is derived from
    *surr_charge_table.csv*, so the two cannot drift apart.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="contract_year")         # noqa: F821


def withdrawal_table():
    """Scheduled gross withdrawals, read from *withdrawal_table.csv*.

    Indexed by ``(wd_schedule_id, month_end)`` - the **policy** month end the withdrawal
    is taken at, counted from the Issue Date, since a withdrawal programme is a contractual
    schedule and stays on the policy clock; a month end with no row takes no withdrawal.
    :func:`withdrawal_count` checks the table, and :func:`wd_amount_array`, which
    ``Projection.wd_amount_pm`` reads, asks for the count before it is built.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / withdrawal_file,                               # noqa: F821
        index_col=["wd_schedule_id", "month_end"])


def market_scenario_count():
    """The number of rows *market_scenario_sec.csv* holds, the scenarios checked: an int.

    :func:`market_scenario` reads the file as ``RILA_US_S`` reads its own, and this cell
    checks it. A ``scenario_id`` that is blank is refused, naming the file, the column and
    the lines it is on; so is a ``month_end`` that is blank, text, not a whole number or
    below 0, read by value, once, as ``Projection.market_state``'s step function compares
    it; and so is a scenario that sets two levels at one month end, naming the lines. And
    so is an ``index_level`` or an ``impl_vol`` that is blank, text, infinite or not above
    0, and an ``mvr``, a ``risk_free`` or a ``div_yield`` that is blank, text, infinite or
    not above -1, naming its lines: the index level divides the index performance and
    every strike, the volatility the Black-Scholes arguments, and each rate is added to 1
    under a division or a logarithm. ``RILA_US_S``'s step function compares the raw months
    with ``t``, so one written as text raises Python's own ``TypeError``, and a blank one
    is a level that never holds. A scenario may start after ``t = 0``, for business issued
    later, so the month a scenario must start by is the point's: :func:`model_point_table`
    refuses a point whose scenario sets no level by its first month on the books.
    ``Data``'s scenario arrays, which ``Projection.market_state`` reads, ask for the count
    before they are built, so a projection meets the checks first.
    """
    name = market_scenario_file                                      # noqa: F821
    rows = market_scenario().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    bad = lines[rows["scenario_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: scenario_id must not be blank; it is on line {bad}")
    months = pd.to_numeric(rows["month_end"], errors="coerce")       # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: month_end must be a whole number, 0 or more; it is not "
                         f"on line {bad}")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["scenario_id"], months.astype("int64")], names=["scenario_id", "month_end"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a scenario must set one level a month end; one sets two "
                         f"on lines {bad}")
    for column, low in (("index_level", 0.0), ("mvr", -1.0), ("risk_free", -1.0),
                        ("div_yield", -1.0), ("impl_vol", 0.0)):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v > low) & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a finite number above {low:g}; it "
                             f"is not on line {bad}")
    return int(len(rows))


def mort_table_count():
    """The number of rows *mort_table.csv* gives a rate for, the table checked: an int.

    :func:`mort_table` reads the table as ``RILA_US_S`` reads it, and this cell checks it.
    The ``age`` key is read by value, once, as ``Projection.mort_rate_base_at``'s join
    matches it, so an age written ``70.0`` is 70. An age that is blank, text or not a whole
    number is refused, naming the file, the column and the lines it is on; so is a ``sex``
    that is not ``M`` or ``F``, the two values a model point's sex can take, a blank among
    them; so is an age and sex on more than one row, naming each with its lines; and so is
    a sex whose ages do not run one row an age, from its first to its last, the message
    naming each age missing. And so is a ``mort_rate`` that is blank, text, infinite or
    below 0, naming its lines: through the cap on mortality the rate reaches every count in
    force, and a blank would survive the cap as a NaN, text fail far from here. A rate
    above 1 is accepted, and capped. :func:`mort_rate_array` and the age vectors, which
    ``Projection.mort_rate_base_at`` reads, ask for the count before they are built, so a
    projection meets the checks first.
    """
    name = mort_table_file                                           # noqa: F821
    rows = mort_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    ages = pd.to_numeric(rows["age"], errors="coerce")               # noqa: F821
    bad = lines[(~(ages % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: age must be a whole number; it is not on line {bad}")
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


def surr_charge_count():
    """The number of contract years *surr_charge_table.csv* charges, checked: an int.

    :func:`surr_charge_table` reads the table as ``RILA_US_S`` reads it, and this cell
    checks it. The ``contract_year`` key is read by value, once, so that a year written
    ``3.0`` is 3, and the years must run ``0 .. n - 1``, one row a year, without a gap or
    a repeat: ``Projection.surr_charge_rate_at`` reads every complete contract year from
    0, charges nothing from year ``n`` on, and ``Projection.lapse_shock_year`` finds the
    first charge-free year among them. A year that is blank, text or not a whole number is
    refused, naming the file, the column and the lines it is on, and so are years that do
    not run so. And so is a ``surr_charge_rate`` that is blank, text or not a fraction, 0
    to 1, naming its lines: a blank would read as no charge in a comparison. The count is
    ``n``. ``RILA_US_S`` reads a year the table lacks as no charge, so one written as text
    silently removes the charge of every year.
    """
    name = surr_charge_file                                          # noqa: F821
    rows = surr_charge_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    years = pd.to_numeric(rows["contract_year"], errors="coerce")    # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be a whole number; it is not on "
                         f"line {bad}")
    if sorted(years.astype("int64").tolist()) != list(range(len(rows))):
        raise ValueError(f"{name}: the contract years must run from 0, one row a year, "
                         f"without a gap or a repeat; they are "
                         f"{years.astype('int64').tolist()} on lines {lines.tolist()}")
    rates = pd.to_numeric(rows["surr_charge_rate"], errors="coerce")  # noqa: F821
    bad = lines[(~((rates >= 0) & (rates <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: surr_charge_rate must be a fraction, 0 to 1; it is not "
                         f"on line {bad}")
    return int(len(rows))


def guar_min_rate_count():
    """The number of terms *guar_min_rate_table.csv* floors, the table checked: an int.

    :func:`guar_min_rate_table` reads the table as ``RILA_US_S`` reads it, and this cell
    checks it. The ``term_years`` key is read by value, once, as
    ``Projection.guar_min_rate``'s join on the model point's term matches it, so a term
    written ``6.0`` is 6. A term that is blank, text, not a whole number or below 1 is
    refused, naming the file, the column and the lines it is on, and so is a term on more
    than one row. And so is a ``guar_min_cap``, a ``guar_min_step`` or a ``guar_min_edge``
    that is blank, text, infinite or below 0, naming its lines: each floors a declared
    rate through a ``max``, which would lose a blank. The floor vectors, which
    ``Projection.guar_min_rate`` reads, ask for the count before they are built, and
    :func:`model_point_table` refuses a point whose term the table lacks.
    """
    name = guar_min_rate_file                                        # noqa: F821
    rows = guar_min_rate_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    terms = pd.to_numeric(rows["term_years"], errors="coerce")       # noqa: F821
    bad = lines[(~((terms % 1 == 0) & (terms >= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: term_years must be a whole number, 1 or more; it is not "
                         f"on line {bad}")
    bad = lines[terms.duplicated(keep=False).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: each term must have one row; one has two on lines "
                         f"{bad}")
    for column in ("guar_min_cap", "guar_min_step", "guar_min_edge"):
        v = pd.to_numeric(rows[column], errors="coerce")             # noqa: F821
        bad = lines[(~((v >= 0) & (v < float("inf")))).to_numpy()].tolist()
        if bad:
            raise ValueError(f"{name}: {column} must be a finite number, zero or more; it "
                             f"is not on line {bad}")
    return int(len(rows))


def lapse_table_count():
    """The number of rows *lapse_table.csv* holds, the step function checked: an int.

    :func:`lapse_table` reads the table as ``RILA_US_S`` reads it, and this cell checks
    it. The ``contract_year`` key is read by value, once, as
    ``Projection.lapse_rate_base_py``'s step function compares it, so a year written
    ``7.0`` is 7. A year that is blank, text or not a whole number is refused, naming the
    file, the column and the lines it is on; so is a year on more than one row; and so is
    a table whose first year is not 1, under which a contract year before it would have no
    rate. And so is a ``lapse_rate_base`` that is blank, text or not a fraction, 0 to 1,
    naming its lines: the surrender rate's bound, ``min(lapse_rate_max, ...)``, is written
    first, and would lose a blank. ``Projection.lapse_rate_base_py``, the table's one
    reader, asks for the count before it reads a rate.
    """
    name = lapse_file                                                # noqa: F821
    rows = lapse_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    years = pd.to_numeric(rows["contract_year"], errors="coerce")    # noqa: F821
    bad = lines[(~(years % 1 == 0)).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: contract_year must be a whole number; it is not on "
                         f"line {bad}")
    bad = lines[years.duplicated(keep=False).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: each contract year must have one row; one has two on "
                         f"lines {bad}")
    if not years.min() == 1:
        raise ValueError(f"{name}: the first contract year must be 1, so that every "
                         f"contract year has a rate; it is {years.min():g}")
    rates = pd.to_numeric(rows["lapse_rate_base"], errors="coerce")  # noqa: F821
    bad = lines[(~((rates >= 0) & (rates <= 1))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: lapse_rate_base must be a fraction, 0 to 1; it is not "
                         f"on line {bad}")
    return int(len(rows))


def withdrawal_count():
    """The number of rows *withdrawal_table.csv* holds, the programmes checked: an int.

    :func:`withdrawal_table` reads the table as ``RILA_US_S`` reads it, and this cell
    checks it. A ``wd_schedule_id`` that is blank is refused, naming the file, the column
    and the lines it is on; so is a ``month_end`` that is blank, text, not a whole number or
    below 0, read by value, once, as ``Projection.wd_amount_pm``'s exact-key lookup
    matches it; and so is a programme that withdraws twice at one month end, naming the
    lines. And so is a ``wd_amount`` that is blank, text, infinite or below 0, naming its
    lines: the withdrawal reaches the account value through a ``min``, which would lose a
    blank. ``RILA_US_S``'s lookup matches the raw months, so one written as text turns them
    all to text, and every scheduled withdrawal is then zero. :func:`wd_amount_array`, which
    ``Projection.wd_amount_pm`` reads, asks for the count before it is built, and
    :func:`model_point_table` refuses a point whose programme the table lacks.
    """
    name = withdrawal_file                                           # noqa: F821
    rows = withdrawal_table().reset_index()
    lines = rows.index + 2                  # the header is line 1 of the file
    bad = lines[rows["wd_schedule_id"].isna().to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_schedule_id must not be blank; it is on line {bad}")
    months = pd.to_numeric(rows["month_end"], errors="coerce")       # noqa: F821
    bad = lines[(~((months % 1 == 0) & (months >= 0))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: month_end must be a whole number, 0 or more; it is not "
                         f"on line {bad}")
    keys = pd.MultiIndex.from_arrays(                                # noqa: F821
        [rows["wd_schedule_id"], months.astype("int64")],
        names=["wd_schedule_id", "month_end"])
    bad = lines[keys.duplicated(keep=False)].tolist()
    if bad:
        raise ValueError(f"{name}: a programme must withdraw once a month end at most; one "
                         f"withdraws twice on lines {bad}")
    amounts = pd.to_numeric(rows["wd_amount"], errors="coerce")      # noqa: F821
    bad = lines[(~((amounts >= 0) & (amounts < float("inf")))).to_numpy()].tolist()
    if bad:
        raise ValueError(f"{name}: wd_amount must be a finite number, zero or more; it is "
                         f"not on line {bad}")
    return int(len(rows))

def point_id():
    """The ``point_id`` of each row, an int64 vector, read by value from the table's index.

    ``Projection`` is indexed by position, ``idx``, and reads its point's label here, so
    that every refusal names the point by the label a reader finds in the table. A label
    that is not a whole number, or not below ``2**53`` in size, is refused, naming it:
    ``RILA_US_S`` keys its points by any label pandas reads.
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


def age_at_entry():
    """The issue age of each point, an int64 vector; 0 where :func:`age_at_entry_ok` is
    0."""
    values = model_point_table()["age_at_entry"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        if abs(values[i]) < 2 ** 53:
            out[i] = int(values[i])
    return out


def age_at_entry_ok():
    """1 where the point's ``age_at_entry`` is below ``2**53`` in size, else 0, int64.

    :func:`model_point_table` refuses such an age unless the mortality table rates its
    sex there, which only a table of one row at that age does; ``Projection.age_at_entry``
    refuses the point where this is 0, as :func:`term_years_ok`'s does.
    """
    values = model_point_table()["age_at_entry"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        if abs(values[i]) < 2 ** 53:
            out[i] = 1
    return out


def duration_mth():
    """The policy months completed at the valuation date, an int64 vector; 0 where
    :func:`duration_mth_ok` is 0."""
    values = model_point_table()["duration_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        if abs(values[i]) < 2 ** 53:
            out[i] = int(values[i])
    return out


def duration_mth_ok():
    """1 where the point's ``duration_mth`` is below ``2**53`` in size, else 0, int64.

    As :func:`age_at_entry_ok`: the mortality table's key check refuses such a duration
    unless the table rates the attained age it reaches, and ``Projection.duration_mth_init``
    refuses the point where this is 0.
    """
    values = model_point_table()["duration_mth"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        if abs(values[i]) < 2 ** 53:
            out[i] = 1
    return out


def term_years():
    """T, the index-linked term of each point, an int64 vector; 0 where
    :func:`term_years_ok` is 0.

    :func:`model_point_table` has refused a term that is not a whole number, 1 or more,
    and one *guar_min_rate_table.csv* does not floor, but that table may floor any whole
    term, ``2**60`` or ``1e20`` among them, which an int64 cannot be trusted to hold.
    """
    values = model_point_table()["term_years"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        if abs(values[i]) < 2 ** 53:
            out[i] = int(values[i])
    return out


def term_years_ok():
    """1 where the point's ``term_years`` is below ``2**53`` in size, else 0, int64.

    ``Projection.term_years`` refuses the point where it is 0, before the term clock reads
    the term: ``RILA_US_S`` projects such a term on Python's exact ints, so that is a
    recorded refusal.
    """
    values = model_point_table()["term_years"].tolist()
    out = np.zeros(len(values), dtype="int64")                       # noqa: F821
    for i in range(len(values)):
        if abs(values[i]) < 2 ** 53:
            out[i] = 1
    return out


def policy_count():
    """The contracts each point stands for, a float64 vector."""
    return model_point_table()["policy_count"].to_numpy(dtype="float64")


def premium():
    """P, the single purchase payment per contract of each point, a float64 vector."""
    return model_point_table()["premium"].to_numpy(dtype="float64")


def buffer():
    """b, the buffer of each point, a float64 vector."""
    return model_point_table()["buffer"].to_numpy(dtype="float64")


def floor_rate():
    """f, the floor of each point's ``FLOOR`` module, a float64 vector."""
    return model_point_table()["floor_rate"].to_numpy(dtype="float64")


def participation():
    """PR, the participation rate of each point, a float64 vector."""
    return model_point_table()["participation"].to_numpy(dtype="float64")


def declared_cap():
    """c, the declared Cap Rate of each point, a float64 vector; NaN where blank.

    A blank is an uncapped option, which :func:`is_uncapped` decodes;
    ``Projection.declared_cap`` returns the NaN as ``RILA_US_S``'s ``float()`` does, and
    no cell reads it there.
    """
    return model_point_table()["declared_cap"].to_numpy(dtype="float64")


def declared_step():
    """s, the declared Step Rate of each point, a float64 vector."""
    return model_point_table()["declared_step"].to_numpy(dtype="float64")


def declared_edge():
    """e, the declared Edge Rate of each point, a float64 vector."""
    return model_point_table()["declared_edge"].to_numpy(dtype="float64")


def wd_rate_ann():
    """The behavioural withdrawal rate of each point, a float64 vector."""
    return model_point_table()["wd_rate_ann"].to_numpy(dtype="float64")


def inv_amt_pp_init():
    """The Investment Amount entering month 0, per contract, a float64 vector."""
    return model_point_table()["inv_amt_pp_init"].to_numpy(dtype="float64")


def fixed_acct_pp_init():
    """The Fixed Account entering month 0, per contract, a float64 vector."""
    return model_point_table()["fixed_acct_pp_init"].to_numpy(dtype="float64")


def holding_acct_pp_init():
    """The Holding Account entering month 0, per contract, a float64 vector."""
    return model_point_table()["holding_acct_pp_init"].to_numpy(dtype="float64")


def av_pp_init():
    """The Account Value entering month 0, per contract, a float64 vector."""
    return model_point_table()["av_pp_init"].to_numpy(dtype="float64")


def av_pp_prev_anniv_init():
    """The Account Value before withdrawals at the anniversary on or before the valuation
    date, per contract, a float64 vector."""
    return model_point_table()["av_pp_prev_anniv_init"].to_numpy(dtype="float64")


def free_wd_remain_init():
    """The Free Withdrawal Amount still unused entering month 0, a float64 vector."""
    return model_point_table()["free_wd_remain_init"].to_numpy(dtype="float64")


def rop_pp_init():
    """The return-of-premium base entering month 0, per contract, a float64 vector."""
    return model_point_table()["rop_pp_init"].to_numpy(dtype="float64")


def index_at_term_start_init():
    """The index level on the Term Start Date of a term begun before the valuation month,
    a float64 vector; NaN where blank, on every point whose term starts later."""
    return model_point_table()["index_at_term_start_init"].to_numpy(dtype="float64")


def mvr_at_term_start_init():
    """The Market Value Rate on that Term Start Date, a float64 vector; NaN where blank."""
    return model_point_table()["mvr_at_term_start_init"].to_numpy(dtype="float64")


def risk_free_at_term_start_init():
    """The risk-free rate on that Term Start Date, a float64 vector; NaN where blank."""
    return model_point_table()["risk_free_at_term_start_init"].to_numpy(dtype="float64")


def div_yield_at_term_start_init():
    """The dividend yield on that Term Start Date, a float64 vector; NaN where blank."""
    return model_point_table()["div_yield_at_term_start_init"].to_numpy(dtype="float64")


def impl_vol_at_term_start_init():
    """The implied volatility on that Term Start Date, a float64 vector; NaN where blank."""
    return model_point_table()["impl_vol_at_term_start_init"].to_numpy(dtype="float64")


def cap_rate_init():
    """The cap re-solved at a renewal under ``nge_reset`` before the valuation month, a
    float64 vector; NaN where blank, on every other point."""
    return model_point_table()["cap_rate_init"].to_numpy(dtype="float64")


def nge_reset():
    """Whether each point re-solves its cap at each renewal, 1 or 0, an int64 vector.

    :func:`model_point_table` has read the flag by value into bools, so ``"False"`` written
    as text is 0, not ``bool("False")``.
    """
    return model_point_table()["nge_reset"].to_numpy(dtype="int64")


def is_uncapped():
    """1 where a point leaves ``declared_cap`` blank, an uncapped option, else 0, int64.

    ``RILA_US_S`` asks ``pd.isna`` of the model point's column; it is asked here once, by
    element (R8).
    """
    return model_point_table()["declared_cap"].isna().to_numpy(dtype="int64")


def cap_uncapped():
    """The cap of an uncapped option, ``+inf``, a float.

    ``RILA_US_S``'s ``math.inf``, which ``Projection.cap_rate`` returns for an uncapped
    option: a C double holds it, and a compiled formula reads it here rather than from the
    ``math`` module.
    """
    return float("inf")


def is_cap_crediting():
    """1 where ``crediting_type`` is ``CAP``, else 0, an int64 vector.

    ``RILA_US_S``'s comparison, made element by element, exactly: ``Cap``, or ``CAP`` with
    a space, is 0, and so is a blank, so that the projection answers as ``RILA_US_S``
    answers it, raising ``invalid crediting_type`` where none of the four decodes is 1.
    """
    return (model_point_table()["crediting_type"] == "CAP").to_numpy(dtype="int64")


def is_step_crediting():
    """1 where ``crediting_type`` is ``STEP``, else 0, an int64 vector."""
    return (model_point_table()["crediting_type"] == "STEP").to_numpy(dtype="int64")


def is_edge_crediting():
    """1 where ``crediting_type`` is ``EDGE``, else 0, an int64 vector."""
    return (model_point_table()["crediting_type"] == "EDGE").to_numpy(dtype="int64")


def is_floor_crediting():
    """1 where ``crediting_type`` is ``FLOOR``, else 0, an int64 vector."""
    return (model_point_table()["crediting_type"] == "FLOOR").to_numpy(dtype="int64")


def is_iv_portfolio():
    """1 where ``iv_family`` is ``portfolio``, else 0, an int64 vector.

    Compared exactly, element by element, as :func:`is_cap_crediting` compares; the
    projection raises ``invalid iv_family`` where none of the four is 1.
    """
    return (model_point_table()["iv_family"] == "portfolio").to_numpy(dtype="int64")


def is_iv_notional():
    """1 where ``iv_family`` is ``notional``, else 0, an int64 vector."""
    return (model_point_table()["iv_family"] == "notional").to_numpy(dtype="int64")


def is_iv_delta():
    """1 where ``iv_family`` is ``delta``, else 0, an int64 vector."""
    return (model_point_table()["iv_family"] == "delta").to_numpy(dtype="int64")


def is_iv_legacy():
    """1 where ``iv_family`` is ``legacy``, else 0, an int64 vector."""
    return (model_point_table()["iv_family"] == "legacy").to_numpy(dtype="int64")


def is_straight_line():
    """1 where ``amort_rule`` is ``straight_line``, else 0, an int64 vector.

    Compared exactly, element by element; the projection raises ``invalid amort_rule``
    where neither decode of the column is 1.
    """
    return (model_point_table()["amort_rule"] == "straight_line").to_numpy(dtype="int64")


def is_updated_expiry():
    """1 where ``amort_rule`` is ``updated_expiry``, else 0, an int64 vector."""
    return (model_point_table()["amort_rule"] == "updated_expiry").to_numpy(dtype="int64")


def guar_min_cap():
    """The guaranteed minimum cap of each point's term, a float64 vector.

    *guar_min_rate_table.csv*'s row of the point's ``term_years``, joined by value, as
    ``RILA_US_S``'s ``.loc`` matches it, after :func:`guar_min_rate_count`'s checks;
    :func:`model_point_table` refuses a point whose term the table lacks.
    """
    guar_min_rate_count()
    floors = guar_min_rate_table()
    terms = pd.to_numeric(floors.index.to_series()).tolist()        # noqa: F821
    values = pd.to_numeric(floors["guar_min_cap"]).tolist()         # noqa: F821
    by_term = {}
    for j in range(len(terms)):
        by_term[terms[j]] = values[j]
    points = model_point_table()["term_years"].tolist()
    out = np.zeros(len(points))                                      # noqa: F821
    for i in range(len(points)):
        out[i] = by_term[points[i]]
    return out


def guar_min_step():
    """The guaranteed minimum Step Rate of each point's term, a float64 vector.

    Joined as :func:`guar_min_cap` joins the cap.
    """
    guar_min_rate_count()
    floors = guar_min_rate_table()
    terms = pd.to_numeric(floors.index.to_series()).tolist()        # noqa: F821
    values = pd.to_numeric(floors["guar_min_step"]).tolist()        # noqa: F821
    by_term = {}
    for j in range(len(terms)):
        by_term[terms[j]] = values[j]
    points = model_point_table()["term_years"].tolist()
    out = np.zeros(len(points))                                      # noqa: F821
    for i in range(len(points)):
        out[i] = by_term[points[i]]
    return out


def guar_min_edge():
    """The guaranteed minimum Edge Rate of each point's term, a float64 vector.

    Joined as :func:`guar_min_cap` joins the cap.
    """
    guar_min_rate_count()
    floors = guar_min_rate_table()
    terms = pd.to_numeric(floors.index.to_series()).tolist()        # noqa: F821
    values = pd.to_numeric(floors["guar_min_edge"]).tolist()        # noqa: F821
    by_term = {}
    for j in range(len(terms)):
        by_term[terms[j]] = values[j]
    points = model_point_table()["term_years"].tolist()
    out = np.zeros(len(points))                                      # noqa: F821
    for i in range(len(points)):
        out[i] = by_term[points[i]]
    return out


def scenario_count():
    """The number of scenarios *market_scenario_sec.csv* holds, an int, the table checked.
    """
    market_scenario_count()
    return int(len(set(market_scenario().reset_index()["scenario_id"].tolist())))


def scenario_number():
    """The row of the scenario arrays each point reads, by its ``scenario_id``, int64.

    The scenarios are numbered from 1 in the sorted order of their ids, and each point
    carries its own scenario's number, matched by the value pandas read, as
    ``RILA_US_S``'s ``.loc`` matches it. :func:`model_point_table` refuses a point whose
    scenario the table lacks, so 0, the number of no scenario, is never a point's.
    """
    market_scenario_count()
    number = {}
    for key in sorted(set(market_scenario().reset_index()["scenario_id"].tolist())):
        number[key] = len(number) + 1
    ids = model_point_table()["scenario_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    for i in range(len(ids)):
        out[i] = number.get(ids[i], 0)
    return out


def scenario_first_mths():
    """Each scenario's first month, by its number, an int64 vector.

    The least ``month_end`` the scenario holds, read by value; ``read_last_mth + 1`` where
    that is past ``read_last_mth``, a scenario no month the arrays hold can read, which no
    point runs on, since :func:`model_point_table` refuses a point whose scenario sets no
    level by its first month on the books. Row 0, no scenario, is 0.
    """
    market_scenario_count()
    rows = market_scenario().reset_index()
    months = pd.to_numeric(rows["month_end"]).tolist()              # noqa: F821
    ids = rows["scenario_id"].tolist()
    last = scenario_last_mth()
    number = {}
    for key in sorted(set(ids)):
        number[key] = len(number) + 1
    first = {}
    for i in range(len(ids)):
        s = number[ids[i]]
        if s not in first or months[i] < first[s]:
            first[s] = months[i]
    out = np.zeros(scenario_count() + 1, dtype="int64")             # noqa: F821
    for s in first:
        out[s] = int(first[s]) if first[s] <= last else last + 1
    return out


def scenario_last_mth():
    """The last valuation month the scenario arrays hold, ``read_last_mth``, an int.

    The last month any read reaches, whatever the scenario's keys: a scenario's last row
    holds to there, as ``RILA_US_S``'s step function holds it, and a row past it is held
    nowhere.
    """
    return read_last_mth                                             # noqa: F821


def index_level_array():
    """The index level by scenario and valuation month, ``[scenario, t]``.

    Each scenario's rows step-filled from their month to the next row's, the last to
    :func:`scenario_last_mth`, as ``RILA_US_S``'s step function reads them; NaN before a
    scenario's first month and in row 0. A row past ``read_last_mth`` is dropped before its
    month is cast, whatever its size.
    """
    market_scenario_count()
    rows = market_scenario().reset_index()
    months = pd.to_numeric(rows["month_end"]).tolist()              # noqa: F821
    values = pd.to_numeric(rows["index_level"]).tolist()            # noqa: F821
    ids = rows["scenario_id"].tolist()
    last = scenario_last_mth()
    number = {}
    for key in sorted(set(ids)):
        number[key] = len(number) + 1
    steps = {}
    for i in range(len(ids)):
        if months[i] <= last:
            steps.setdefault(number[ids[i]], []).append((int(months[i]), values[i]))
    out = np.full((scenario_count() + 1, last + 1), np.nan)          # noqa: F821
    for s in steps:
        pairs = sorted(steps[s])
        for j in range(len(pairs)):
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            out[s, pairs[j][0]:end] = pairs[j][1]
    return out


def mvr_array():
    """The Market Value Rate by scenario and valuation month, ``[scenario, t]``.

    As :func:`index_level_array`, from the ``mvr`` column.
    """
    market_scenario_count()
    rows = market_scenario().reset_index()
    months = pd.to_numeric(rows["month_end"]).tolist()              # noqa: F821
    values = pd.to_numeric(rows["mvr"]).tolist()                    # noqa: F821
    ids = rows["scenario_id"].tolist()
    last = scenario_last_mth()
    number = {}
    for key in sorted(set(ids)):
        number[key] = len(number) + 1
    steps = {}
    for i in range(len(ids)):
        if months[i] <= last:
            steps.setdefault(number[ids[i]], []).append((int(months[i]), values[i]))
    out = np.full((scenario_count() + 1, last + 1), np.nan)          # noqa: F821
    for s in steps:
        pairs = sorted(steps[s])
        for j in range(len(pairs)):
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            out[s, pairs[j][0]:end] = pairs[j][1]
    return out


def risk_free_array():
    """The risk-free rate by scenario and valuation month, ``[scenario, t]``.

    As :func:`index_level_array`, from the ``risk_free`` column.
    """
    market_scenario_count()
    rows = market_scenario().reset_index()
    months = pd.to_numeric(rows["month_end"]).tolist()              # noqa: F821
    values = pd.to_numeric(rows["risk_free"]).tolist()              # noqa: F821
    ids = rows["scenario_id"].tolist()
    last = scenario_last_mth()
    number = {}
    for key in sorted(set(ids)):
        number[key] = len(number) + 1
    steps = {}
    for i in range(len(ids)):
        if months[i] <= last:
            steps.setdefault(number[ids[i]], []).append((int(months[i]), values[i]))
    out = np.full((scenario_count() + 1, last + 1), np.nan)          # noqa: F821
    for s in steps:
        pairs = sorted(steps[s])
        for j in range(len(pairs)):
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            out[s, pairs[j][0]:end] = pairs[j][1]
    return out


def div_yield_array():
    """The dividend yield by scenario and valuation month, ``[scenario, t]``.

    As :func:`index_level_array`, from the ``div_yield`` column.
    """
    market_scenario_count()
    rows = market_scenario().reset_index()
    months = pd.to_numeric(rows["month_end"]).tolist()              # noqa: F821
    values = pd.to_numeric(rows["div_yield"]).tolist()              # noqa: F821
    ids = rows["scenario_id"].tolist()
    last = scenario_last_mth()
    number = {}
    for key in sorted(set(ids)):
        number[key] = len(number) + 1
    steps = {}
    for i in range(len(ids)):
        if months[i] <= last:
            steps.setdefault(number[ids[i]], []).append((int(months[i]), values[i]))
    out = np.full((scenario_count() + 1, last + 1), np.nan)          # noqa: F821
    for s in steps:
        pairs = sorted(steps[s])
        for j in range(len(pairs)):
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            out[s, pairs[j][0]:end] = pairs[j][1]
    return out


def impl_vol_array():
    """The implied volatility by scenario and valuation month, ``[scenario, t]``.

    As :func:`index_level_array`, from the ``impl_vol`` column.
    """
    market_scenario_count()
    rows = market_scenario().reset_index()
    months = pd.to_numeric(rows["month_end"]).tolist()              # noqa: F821
    values = pd.to_numeric(rows["impl_vol"]).tolist()               # noqa: F821
    ids = rows["scenario_id"].tolist()
    last = scenario_last_mth()
    number = {}
    for key in sorted(set(ids)):
        number[key] = len(number) + 1
    steps = {}
    for i in range(len(ids)):
        if months[i] <= last:
            steps.setdefault(number[ids[i]], []).append((int(months[i]), values[i]))
    out = np.full((scenario_count() + 1, last + 1), np.nan)          # noqa: F821
    for s in steps:
        pairs = sorted(steps[s])
        for j in range(len(pairs)):
            end = pairs[j + 1][0] if j + 1 < len(pairs) else last + 1
            out[s, pairs[j][0]:end] = pairs[j][1]
    return out


def mort_sexes():
    """The number of sexes *mort_table.csv* rates, an int, the table checked."""
    mort_table_count()
    return int(len(set(mort_table().reset_index()["sex"].tolist())))


def mort_schedule():
    """The row of :func:`mort_rate_array` each point reads, by its ``sex``, int64.

    The sexes are numbered from 1 in their sorted order, ``F`` 1 and ``M`` 2, and each
    point carries its own sex's number, matched by the value pandas read, as
    ``RILA_US_S``'s ``.loc`` matches it. :func:`model_point_table` refuses a point whose
    sex the table does not rate, so 0, the number of no sex, is never a point's.
    """
    mort_table_count()
    number = {}
    for key in sorted(set(mort_table().reset_index()["sex"].tolist())):
        number[key] = len(number) + 1
    sexes = model_point_table()["sex"].tolist()
    out = np.zeros(len(sexes), dtype="int64")                        # noqa: F821
    for i in range(len(sexes)):
        out[i] = number.get(sexes[i], 0)
    return out


def mort_age_firsts():
    """Each sex's first age in *mort_table.csv*, by its number, an int64 vector.

    Read by value; 0 where it is below 0, since no attained age is, and
    ``read_last_age + 1`` where it is past ``read_last_age``, an age the array does not
    hold. Row 0, no sex, is 1, so that no age reads it.
    """
    mort_table_count()
    rows = mort_table().reset_index()
    ages = pd.to_numeric(rows["age"]).tolist()                       # noqa: F821
    sexes = rows["sex"].tolist()
    held = mort_age_held()
    number = {}
    for key in sorted(set(sexes)):
        number[key] = len(number) + 1
    first = {}
    for i in range(len(sexes)):
        s = number[sexes[i]]
        if s not in first or ages[i] < first[s]:
            first[s] = ages[i]
    out = np.ones(mort_sexes() + 1, dtype="int64")                   # noqa: F821
    for s in first:
        out[s] = int(min(max(first[s], 0), held + 1))
    return out


def mort_age_lasts():
    """Each sex's last age in *mort_table.csv*, by its number, an int64 vector.

    Read by value; -1 where it is below 0, and ``read_last_age + 1`` where it is past
    ``read_last_age``, the table rating more than the array holds, which
    ``Projection.proj_len`` refuses only where a point's cover needs it. Row 0, no sex,
    is 0.
    """
    mort_table_count()
    rows = mort_table().reset_index()
    ages = pd.to_numeric(rows["age"]).tolist()                       # noqa: F821
    sexes = rows["sex"].tolist()
    held = mort_age_held()
    number = {}
    for key in sorted(set(sexes)):
        number[key] = len(number) + 1
    last = {}
    for i in range(len(sexes)):
        s = number[sexes[i]]
        if s not in last or ages[i] > last[s]:
            last[s] = ages[i]
    out = np.zeros(mort_sexes() + 1, dtype="int64")                  # noqa: F821
    for s in last:
        out[s] = int(min(max(last[s], -1), held + 1))
    return out


def mort_age_held():
    """The age of :func:`mort_rate_array`'s last column, ``read_last_age``, an int."""
    return read_last_age                                             # noqa: F821


def mort_rate_array():
    """The annual mortality by sex and attained age, ``[sex, age]``.

    Row ``mort_schedule()`` of a point holds its sex's rates, row 0 none; column ``a`` is
    attained age ``a``, from 0 to :func:`mort_age_held`, ``read_last_age``, the oldest age
    a read reaches. Every cell outside a sex's ages, and row 0, is NaN, and an age below 0
    or past ``read_last_age`` is held nowhere, so a row far past it, which ``RILA_US_S``
    holds and never reads, neither widens the array nor refuses a point.
    """
    mort_table_count()
    rows = mort_table().reset_index()
    ages = pd.to_numeric(rows["age"]).tolist()                       # noqa: F821
    rates = pd.to_numeric(rows["mort_rate"]).tolist()                # noqa: F821
    sexes = rows["sex"].tolist()
    held = mort_age_held()
    number = {}
    for key in sorted(set(sexes)):
        number[key] = len(number) + 1
    out = np.full((mort_sexes() + 1, held + 1), np.nan)              # noqa: F821
    for i in range(len(ages)):
        if 0 <= ages[i] <= held:
            out[number[sexes[i]], int(ages[i])] = rates[i]
    return out


def surr_charge_array():
    """The withdrawal charge rate by complete contract year, ``[cy]``, ``0 .. n - 1``.

    :func:`surr_charge_count`, ``n``, holds the table's years to that run, one row a year,
    so the year is the index.
    """
    n = surr_charge_count()
    rows = surr_charge_table().reset_index()
    years = pd.to_numeric(rows["contract_year"]).tolist()           # noqa: F821
    rates = pd.to_numeric(rows["surr_charge_rate"]).tolist()        # noqa: F821
    out = np.zeros(n)                                                # noqa: F821
    for i in range(n):
        out[int(years[i])] = rates[i]
    return out


def lapse_years():
    """The lapse table's contract years, row by row, a float64 vector.

    The keys as the table holds them, compared by value, never cast, so that a year of
    any size is read as ``RILA_US_S`` compares it; ``Projection.lapse_rate_base_py``
    scans them for the last year at or before its ``y``, its count
    :func:`lapse_table_count` the bound.
    """
    lapse_table_count()
    rows = lapse_table().reset_index()
    return pd.to_numeric(rows["contract_year"]).to_numpy(dtype="float64")  # noqa: F821


def lapse_rates():
    """The lapse table's base surrender rates, row by row, a float64 vector."""
    lapse_table_count()
    rows = lapse_table().reset_index()
    return pd.to_numeric(rows["lapse_rate_base"]).to_numpy(dtype="float64")  # noqa: F821


def wd_schedule_count():
    """The number of programmes *withdrawal_table.csv* holds, an int, the table checked."""
    withdrawal_count()
    return int(len(set(withdrawal_table().reset_index()["wd_schedule_id"].tolist())))


def wd_schedule_number():
    """The row of :func:`wd_amount_array` each point reads, by its ``wd_schedule_id``.

    Numbered from 1 in the sorted order of the ids, int64, as :func:`scenario_number`
    numbers the scenarios; :func:`model_point_table` refuses an id the table lacks.
    """
    withdrawal_count()
    number = {}
    for key in sorted(set(withdrawal_table().reset_index()["wd_schedule_id"].tolist())):
        number[key] = len(number) + 1
    ids = model_point_table()["wd_schedule_id"].tolist()
    out = np.zeros(len(ids), dtype="int64")                          # noqa: F821
    for i in range(len(ids)):
        out[i] = number.get(ids[i], 0)
    return out


def wd_last_mth():
    """The last policy month end :func:`wd_amount_array` holds, ``read_last_mth``, an int.

    Past any month end a read reaches: a row past it is held nowhere.
    """
    return read_last_mth                                             # noqa: F821


def wd_amount_array():
    """The scheduled withdrawal by programme and policy month end, ``[programme, m]``.

    0.0 at a month end a programme has no row for, a value, as ``RILA_US_S``'s exact-key
    lookup answers it, not padding; row 0, which no point reads, is NaN. A row past
    :func:`wd_last_mth` is dropped before its month is cast, whatever its size.
    """
    withdrawal_count()
    rows = withdrawal_table().reset_index()
    months = pd.to_numeric(rows["month_end"]).tolist()              # noqa: F821
    amounts = pd.to_numeric(rows["wd_amount"]).tolist()             # noqa: F821
    ids = rows["wd_schedule_id"].tolist()
    last = wd_last_mth()
    number = {}
    for key in sorted(set(ids)):
        number[key] = len(number) + 1
    out = np.zeros((wd_schedule_count() + 1, last + 1))              # noqa: F821
    out[0, :] = np.nan                                               # noqa: F821
    for i in range(len(ids)):
        if months[i] <= last:
            out[number[ids[i]], int(months[i])] = amounts[i]
    return out


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table_sec.csv"

mort_table_file = "mort_table.csv"

market_scenario_file = "market_scenario_sec.csv"

surr_charge_file = "surr_charge_table.csv"

guar_min_rate_file = "guar_min_rate_table.csv"

lapse_file = "lapse_table.csv"

withdrawal_file = "withdrawal_table.csv"

future_horizon_mth = 120

read_last_mth = 1202

read_last_age = 121

pd = ("Module", "pandas")

np = ("Module", "numpy")
