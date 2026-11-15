"""In-force tests for Term_US_SEC: the splice, future business, counts and regeneration.

``Term_US_SEC`` is ``Term_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M1).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t``.  A model point may be a
policy already in force at the valuation date, one issued at it, or one to be issued after
it, as in ``basiclife/BasicTerm_SE``.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``Term_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's two points (T1), so every golden of
``test_term_life_us.py`` holds on this model with no number copied.  The conventions also
hold the SEC family's other rules: every frame opens at ``t = 0``, ``pols_if`` is the
``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business
enters once, and nothing happens before issue.  This module holds the rest of the plan's
tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the count S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's.  The
  months straddle the shock, the first ART premium and expiry, and variants of S's
  points, in a copy of S's table, add what S's own points cannot reach: the age limit of
  the conversion window, the three premium cycles that are not the anniversary, a level
  period of twenty years, cover that ends with the level period, and every value the
  model decodes or joins its tables on, each with a premium schedule of its own.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate evaluated there.
* D11's R1 and R2, and D3's and D5's chains: on the splice's grid no cell is called at a
  negative month or reads beyond ``t + 1``; on the committed points no recursion runs
  backward over the frame; the policy clock is a closed form; and a cold call runs one
  cell a month back to issue, on the committed points and at the contract's extremes.
* T4, the count algebra: the count rolls forward through new business and decrements, and
  multiplying ``policy_count`` by 2.5, with conversion switched on, multiplies every flow
  and every counted cell by 2.5 and moves no per-policy value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point; the future horizon is a Reference that bounds future business, and at 0 refuses
  it; a point past its cover, or one the contract does not issue, is refused by the
  frame, each bound just inside it; the edges of the interface are accepted; and so is
  every state ``Term_US_S`` reaches, on each set of inputs on which those states differ.
* Phase 2's decoding: every value a column can hold decodes as ``Term_US_S`` reads it,
  what cannot be decoded is refused by name, and so is a read beyond a table; and a value
  a cap, a ``min`` or a ``max`` reads, a class factor, a base rate, a premium, an issue
  age or an M(1) override, is a finite number, or ``Data`` refuses it, blank, text or
  infinite, a blank M(1) override excepted, the notes' rule, naming the file, the column
  and every line or point at fault, when its array is first read.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``Term_US_S`` and its table as they stand.
* Then the two clocks on the shipped points, the policy in force mid-ART, expense inflation
  on the valuation clock, acquisition on new business, the values outside cover, the block,
  an in-force extract labelled otherwise than by position, the runner, the docstrings and
  the shared input tables.
* The cap: where the annual mortality product passes 1, the rate is 1 in both models,
  every policy then in force dies that month, on new business and in force, and the two
  models agree in every cell.  A NaN that reaches the cap, or the ``min`` of the M(1)
  rule or the ``max`` of the PLT grading, stays NaN, and is not turned into the bound.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).
* Compiled (marked ``cython``): C4 on the splice grid, at the contract's extremes and where
  the cap binds, the compiled model refusing what modelx refuses, the deepest cold call on
  a 1 MiB stack, a Reference set late, which clears no compiled cache, and the runner
  compiled.  ``test_compiled_conventions.py`` holds the rest of Phase 2's tests for every
  compiled model: C3, C5, C4 on the committed points and the release.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, ``-k``
for one issued ``k`` months on.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.term_life`` holds S's default name, and reading a model under a name in use
renames the open one.  No test writes inside the library tree: every changed input goes
through ``sec_support.temp_inputs`` into a temporary directory, because a CSV added beside
the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  And a timing or a phase is the model's own int Reference,
``p.BEF_DECR`` or ``p.LEVEL``, as at stage ``"EC"`` it is (R9, R10), and every comparison
with S passes ``sec_support.codes``, which turns S's strings into those ints: Phase 2
changed the call syntax only (C1).
"""
import dataclasses
import itertools
import json
import math
import os
import re
import shutil
import subprocess
import sys

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, compiled_case, compiled_mismatches, exact_here, fingerprint_mismatches,
    frame_mismatches, label_mismatches, run_compiled, sweep, temp_inputs,
    twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "Term_US_SEC", "Term_US_S", "model_point_table_sec.csv"

# S's two points, both issued at t = 0.  Point 1 takes M(1) from its override, point 2 from
# the notes' formula through jump_ratio, so the two differ wherever the PLT years are read.
S_POINTS = (1, 2)

# T2's months (USLIB-SEC-PLAN.md §7.1): the second month, the year's premium already paid;
# the first anniversary, a premium due at t = 0; the last level month, 119, which carries
# the shock; 120, the first ART premium, and the month after it; and 719, the last month of
# cover.  T3's: issued one month on, which puts the policy anniversaries a month off the
# valuation years, and twelve, which puts them back on.
SPLICE_MTHS = (1, 12, 119, 120, 121, 719)
FUTURE_MTHS = (1, 12)

# Three more S points, in the splice's copy of S's table and never in the committed one,
# each S's anchor cell changed so as to reach what S's own points cannot.  On those, issued
# at 35 on the ten-year plan and paying annually, the conversion window closes with the
# level period, long before attained age 70, every premium falls due on the anniversary,
# the level period is ten years in every formula that reads it, and cover outlasts it by
# fifty.  Each variant is (the S point it changes, the columns it changes); the policy_id
# keeps the generated ids apart.  T2 restates each at the months given, T3 issues each a
# month on, and each pays in a mode no other point pays in.
#
# 3, S point 1 at 65, quarterly: the window is policy years 1 to 5, closed by age 70, and
#   the premium falls due every third month.  Restated in the second month, between two
#   instalments, at the last month before the final eligible year (47), at the final
#   year's last month (59) and at the first month outside the window (60).
# 4, S point 2 at 45 on a twenty-year plan, semi-annually: the shock in month 239, the jump
#   ratio read at years 20 and 21, and from it M(1) by the notes' rule, as point 2 has no
#   override.  Restated either side of the shock and the first ART premium, at 12n - 2,
#   12n - 1, 12n and 12n + 1.  premium_rates.csv has no T20 scale, so the copies get the
#   one _premium_rates_with_t20 builds.
# 5, S point 1 at 85, monthly: cover ends with the level period, so the shock falls in the
#   last covered month and S's jump ratio reads policy year 11, past S's own frame, where
#   SEC's cells answer that the month is outside cover (sec_support.twin_mismatches compares
#   S's frame alone).  Restated in the second month, then in the last two.
VARIANTS = {
    3: (1, {"policy_id": "TL-000003", "age_at_entry": 65, "premium_mode": "Q"}),
    4: (2, {"policy_id": "TL-000004", "age_at_entry": 45, "plan": "T20",
            "premium_mode": "SA"}),
    5: (1, {"policy_id": "TL-000005", "age_at_entry": 85, "premium_mode": "M"}),
}

# Ten more, for what Phase 2 rewrote: the decoding of the model point's text and the join of
# the premium schedule by plan, sex, class and band, which every shipped point, all M,
# StdNT and band 1, takes at one value only (USLIB-SEC-PLAN.md R6, R7).  Each carries a
# value no shipped point does: the other sex, each other class, and each side of every
# face-amount boundary.  Every key but the anchor cell's gets a schedule of its own in the
# copies, at a scale of its own (_premium_rates_with_variants), so that a point joined to
# the wrong schedule, or banded wrongly at a boundary, reads another premium, and a class
# factor joined wrongly another mortality.  Each is restated in its second month: what the
# splice compares then is every premium S reads, every policy year's, and every month's
# mortality.  Point 2 leaves M(1) to the notes' rule, which reads the schedule's jump
# ratio, so most are built on it.
VARIANTS.update({
    6: (2, {"policy_id": "TL-000006", "sex": "F"}),
    7: (1, {"policy_id": "TL-000007", "rate_class": "PPlusNT"}),
    8: (2, {"policy_id": "TL-000008", "rate_class": "PNT"}),
    9: (2, {"policy_id": "TL-000009", "rate_class": "StdTob"}),
    10: (2, {"policy_id": "TL-000010", "sum_assured": 249999.99}),
    11: (2, {"policy_id": "TL-000011", "sum_assured": 250000.0}),
    12: (2, {"policy_id": "TL-000012", "sum_assured": 499999.99}),
    13: (2, {"policy_id": "TL-000013", "sum_assured": 500000.0}),
    14: (2, {"policy_id": "TL-000014", "sum_assured": 999999.99}),
    15: (1, {"policy_id": "TL-000015", "sum_assured": 1000000.0}),
})
VARIANT_SPLICE_MTHS = {3: (1, 47, 59, 60), 4: (238, 239, 240, 241), 5: (1, 118, 119),
                       **{point_id: (1,) for point_id in range(6, 16)}}
VARIANT_FUTURE_MTHS = {3: (1,), 4: (1,), 5: (1,)}

# The premium schedules the decoding variants join to, beyond the anchor cell's: (sex,
# rate_class, band) on the ten-year plan, in the order of their scales.
DECODED_SCHEDULES = (("F", "StdNT", 1), ("M", "PPlusNT", 1), ("M", "PNT", 1),
                     ("M", "StdTob", 1), ("M", "StdNT", 2), ("M", "StdNT", 3),
                     ("M", "StdNT", 4))

# T2's cases, as (row_kind, S point, source_mth): each S point restated in force at each of
# its splice months, then the twins of S's own in-force rows.  Those are splice cases too
# (§5.2), aligned at their twin's source_mth, the first row of the S frame.  Term_US_S has
# no in-force row, so the second list is empty here; WholeLife's would hold
# ("twin", 1, 108).  T3's cases, as (S point, k).
SPLICES = (tuple(("derived", p, d) for p in S_POINTS for d in SPLICE_MTHS)
           + tuple(("derived", p, d) for p, mths in VARIANT_SPLICE_MTHS.items()
                   for d in mths))
IN_FORCE_TWINS = ()
FUTURES = (tuple((p, k) for p in S_POINTS for k in FUTURE_MTHS)
           + tuple((p, k) for p, mths in VARIANT_FUTURE_MTHS.items() for k in mths))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is the one input Term reads on the valuation clock (D7): S inflates from
# issue and SEC from the valuation date, so at the shipped 2% the expenses of a point
# opened at d differ by 1.02^(d/12), by design, and at 0 both factors are 1.  The clock
# itself is then asserted on its own, at the shipped rate, because a zero rate hides any
# clock.  Term has no mortality improvement.  Conversion ships at 0, as the worked example
# requires, which multiplies the conversion window, its final-year rule and the conversion
# credit by zero in every month; the notes' own [std] magnitudes, 1% a year while eligible
# and 2% in the final eligible year, make them visible.  The identity does not depend on
# the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "conv_rate_base": 0.01, "conv_rate_final": 0.02}

# The cells T2 and T3 skip beyond T1's.  proj_len counts from the valuation date on SEC and
# from issue on S, so it differs by d, or by -k, by design; frame_mismatches asserts what
# it must get right, that both frames end at the same instant.  result_cf_annual groups by
# policy year, and a point opened at d lacks S's earlier years and, opened mid-year, holds
# only the rest of the current one (the mid-ART test compares the later years).  A future
# point's years are all whole once its pre-issue months are dropped, so T3 compares it.
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | {"proj_len", "result_cf_annual"}
FUTURE_EXEMPT = TWIN_EXEMPT_DEFAULT | {"proj_len"}

# The decrement rates, none of which may be evaluated before issue (R1, D4).
DECREMENT_RATES = ("mort_rate_base", "mort_rate", "mort_rate_mth", "lapse_rate",
                   "lapse_rate_mth", "conv_rate", "conv_rate_mth")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a rate,
# a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_death", "pols_surv", "pols_conv", "pols_lapse", "pols_maturity",
    "premiums", "commissions", "premium_taxes", "expenses", "claims", "conv_credits",
    "net_cf", "result_cf", "result_cf_annual", "result_pols"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# decrements in processing order, then the expiries of the last covered month.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_conv", "pols_lapse",
               "pols_maturity"]
OUTFLOWS = RESULT_POLS[2:]

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow, no question about the contract answered
# yes, and no contractual scale read at a policy year the month does not have.  The type
# is part of the value.  A count is a float in every branch and a flag a bool, because
# Phase 2 types a cell by the values it returns (USLIB-SEC-PLAN.md F3).
OUTSIDE_COVER = {
    "is_active": False, "prem_due": False, "conv_elig": False,
    "premium_pp_ann": 0.0, "premium_pp": 0.0, "mort_rate_base": 0.0, "comm_rate": 0.0,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0, "pols_surv": 0.0,
    "pols_conv": 0.0, "pols_lapse": 0.0, "pols_maturity": 0.0,
    "premiums": 0.0, "commissions": 0.0, "premium_taxes": 0.0, "expenses": 0.0,
    "claims": 0.0, "conv_credits": 0.0, "net_cf": 0.0}

# The cells a month outside cover may not reach: the decrement rates, and the reads keyed by
# a policy year, a PLT duration or an attained age.  mort_rate_base is the one rate the
# guard test calls itself, and is held by its value instead.
IN_COVER_ONLY = ("age", "premium_pp_ann_py", "conv_elig_py", "plt_mort_factor",
                 *(rate for rate in DECREMENT_RATES if rate != "mort_rate_base"))

# The cells this model adds to Term_US_S's, running in force and then compiling, each of
# which the symbol map must name.
NEW_CELLS = ("policy_count", "expiry_mth", "duration_mth_init", "t_entry", "is_active",
             "premium_pp_ann_py", "conv_elig_py", "pols_if_at", "pols_new_biz",
             "result_pols", "point_id", "premium_schedule")

INFLATION = 0.02        # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the rules test runs the
# reports on a fresh read (R2, F7).  A report evaluates each column in ascending t, so a
# forward recursion, through t - 1, finds the month before already cached: the committed
# points' reports open chains of 10 formula calls at most, and the splice's grid 13.  A
# backward recursion over the frame, through t + 1, opens a chain as long as the frame.
CALL_DEPTH = 40

# How deep a cold call may run beyond the count chain, one cell a month from its month back
# to t_entry (D5): the cells above the chain, net_cf to pols_if, and below it, the first
# month's rates and Data's first reads of its tables.  Measured at 9, on the committed
# twin's 720-month frame, 728 cells deep, and at the contract's longest, 932 (M14).  A
# chain of two cells a month doubles the depth, and needs twice the stack compiled.
CHAIN_OVERHEAD = 16


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    keys = dict(zip(model.Data.model_point_table().index, point_keys(model)))
    return projection(model, keys[point_id])


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for a twin, ``d`` for a derived row, ``-k`` for
    a future one.  The twins keep S's ``point_id`` and ``policy_id``, so the S policy is the
    twin's.
    """
    policy = table.at[s_point, "policy_id"]
    hit = table.index[(table["row_kind"] == kind) & (table["source_policy_id"] == policy)
                      & (table["source_mth"] == month)].tolist()
    assert len(hit) == 1, f"{kind} rows of S point {s_point} at month {month}: {hit}"
    return hit[0]


def _row(model, kind, s_point, month):
    """The ItemSpace of that row of ``model``'s table (:func:`_label`)."""
    return _point(model, _label(model.Data.model_point_table(), kind, s_point, month))


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``, and whose other
    inputs ``edits`` changes, as :func:`sec_support.temp_inputs` takes them; its SEC
    folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit):
    """Term_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
    return mx.read_model(_sec_inputs(tmp_path, edit(_committed())), name=_name("edited"))


def _set(column, points, value):
    """An edit of the table that writes ``value`` into ``column`` at ``points`` alone.

    The column is made ``object`` first, so a text or a number of another type can go in
    beside the numbers it holds: the file then carries what an extract with a bad cell
    would.
    """
    def edit(table):
        cells = table[column].astype(object)
        return table.assign(**{column: cells.where(~table.index.isin(points), value)})
    return edit


def _refused(call, message):
    """``call()`` raises ``ValueError`` with ``message``, inside modelx's wrapper.

    modelx re-raises an error inside a formula as ``FormulaError``, with the original type
    and message in its text, so the text is asserted rather than a modelx class.
    """
    with pytest.raises(Exception) as excinfo:
        call()
    text = str(excinfo.value)
    assert "ValueError" in text and message in text, text


def _raised(err):
    """The line that names an error: modelx's ``FormulaError`` puts it second."""
    lines = [line for line in str(err).splitlines() if line.strip()]
    if type(err).__name__ == "FormulaError" and len(lines) > 1:
        return lines[1]
    return f"{type(err).__name__}: {lines[0] if lines else ''}"


def _sweep_s(proj):
    """Evaluate on an S point what the splice compares: the sweep, and three cells more.

    :func:`sec_support.sweep` reaches neither ``pols_lapse``, ``pols_maturity`` nor
    ``phase``, because no result column reads them on S, and a cell S never evaluates is
    compared nowhere.  They are evaluated here over the frame, so the splice and the future
    comparison see them too.  The month after the frame is not: the comparison is held to
    S's own frame (:func:`sec_support.twin_mismatches`), and ``phase`` reads ``EXPIRED``
    there by the two-clocks test.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        proj.pols_lapse(t)
        proj.pols_maturity(t)
        proj.phase(t)


def _case_id(kind, s_point, month):
    """A T2 case's id: ``point1-d12`` for a derived row, ``point1-twin108`` for a twin."""
    return f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}")


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module")
def sec_model():
    """Term_US_SEC read in place, as committed."""
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def s_model():
    """Term_US_S read in place, as committed, with every point swept.

    T6 regenerates the SEC table from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it.
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        sweep(projection(model, key))
    yield model
    model.close()


def _s_table_with_variants():
    """S's committed table with the :data:`VARIANTS` appended, under their own point_ids."""
    table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                        index_col="point_id")
    rows = []
    for point_id, (base, changes) in VARIANTS.items():
        row = table.loc[[base]].assign(**changes)
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    return pd.concat([table, *rows])


def _premium_rates_with_t20(rates):
    """``premium_rates.csv`` with a T20 scale beside the T10 one, for variant 4 alone.

    T10's level premium for twenty policy years, then T10's renewal premiums from its jump
    on, moved ten years later: the jump falls at year 21, the jump ratio is T10's, and the
    scale runs to year 60 like T10's.  A copy's file only, never the committed one.
    """
    t10 = rates[rates["plan"] == "T10"]
    level, renewal = t10[t10["policy_year"] <= 10], t10[t10["policy_year"].between(11, 50)]
    t20 = pd.concat([level, level.assign(policy_year=level["policy_year"] + 10),
                     renewal.assign(policy_year=renewal["policy_year"] + 10)])
    return pd.concat([rates, t20.assign(plan="T20", provenance="T10 moved on, for a test")],
                     ignore_index=True)


def _premium_rates_with_variants(rates):
    """``premium_rates.csv`` with every schedule the splice's variants join to.

    The T20 scale of :func:`_premium_rates_with_t20`, and a schedule for each key of
    :data:`DECODED_SCHEDULES`, the anchor cell's own scaled by 1.01, 1.02, ... in turn,
    so that no two keys share a premium.  A copy's file only, never the committed one.
    """
    rates = _premium_rates_with_t20(rates)
    anchor = rates[(rates["plan"] == "T10") & (rates["sex"] == "M")
                   & (rates["rate_class"] == "StdNT") & (rates["band"] == 1)]
    scaled = [anchor.assign(sex=sex, rate_class=rate_class, band=band,
                            premium_pp=anchor["premium_pp"] * (1 + k / 100),
                            provenance="the anchor cell scaled, for a test")
              for k, (sex, rate_class, band) in enumerate(DECODED_SCHEDULES, start=1)]
    return pd.concat([rates, *scaled], ignore_index=True)


# The input files the splice's copies change, S's and SEC's alike.
SPLICED_EDITS = {"premium_rates.csv": _premium_rates_with_variants}


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`SPLICED_REFS` set in both.

    S is read from a copy of the product directory whose table has the variants appended,
    and whose premium table has their schedules (:data:`SPLICED_EDITS`).  SEC runs
    on the same premium table, and on a model point table of its own, built by the
    generator from the registered spec with its rows replaced by :data:`SPLICES` and
    :data:`FUTURES`, out of this S model, so each row opens with the count of the very run
    it is compared with.  No input table moves with ``d``: Term's one valuation-clock input
    is the ``inflation_rate`` Reference.
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants(), edits=SPLICED_EDITS)
    s = mx.read_model(s_folder, name=_name("s_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(s.Projection, ref, value)
    spec = dataclasses.replace(SEC_SPECS[SEC], derived=tuple((p, d) for _, p, d in SPLICES),
                               future=FUTURES)
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file, edits=SPLICED_EDITS)
    sec = mx.read_model(sec_folder, name=_name("sec_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(sec.Projection, ref, value)
    for key in point_keys(s):
        _sweep_s(projection(s, key))
    yield s, sec
    sec.close()
    s.close()


# ---------------------------------------------------------------------------
# T2 -- the splice


@pytest.mark.parametrize("kind, s_point, month", SPLICES + IN_FORCE_TWINS,
                         ids=[_case_id(*case) for case in SPLICES + IN_FORCE_TWINS])
def test_an_in_force_point_continues_its_s_projection(spliced, kind, s_point, month):
    """Opened with S's count at month d, the point is S from d on, in every cell of S's.

    This is the test that says the opening state is complete: a state variable the SEC row
    did not carry would make SEC part from S here, and nowhere else, because on a point
    issued at ``t = 0`` the two clocks coincide.  For the same reason it is the test that
    catches a policy month passed as ``t`` (R1a).  The frame comparison reads SEC row ``t``
    against S row ``t + d`` in every ``result_cf`` column and fails frames that end apart;
    the cell comparison then evaluates every cell of S's but :data:`SPLICE_EXEMPT`, at
    every argument S cached inside its own frame from month ``d`` on, moved onto SEC's
    clock, the state cell ``pols_if`` and every result column among them.  Both compare to
    1e-9 relative with no absolute floor (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): on
    the tobacco variant the count falls to 1.1e-6 by the last month of cover, and its
    lapses to 9.2e-9, where a floor of 1e-9 would pass an error of 11%.  ``Term_US_S`` has
    no roll-forward residual, the one kind of cell, a rounding about an exact 0, that keeps
    the floor.  An S cell this model lacked would fail it.  The variants' cases, on S
    points 3 to 5, are the only ones that see the conversion window's age limit, a premium
    cycle shorter than a year, a level period other than ten years, and cover that ends
    with the level period.  Those on points 6 to 15 are the only ones that see a sex, a
    class or a band other than the anchor cell's, each with a premium schedule of its own,
    so they are what holds ``Data``'s decoding and its join of the schedule to
    ``Term_US_S``'s lookups.
    """
    s, sec = spliced
    s_proj, sec_proj = _point(s, s_point), _row(sec, kind, s_point, month)
    assert frame_mismatches(s_proj.result_cf(), sec_proj.result_cf(), t_offset=month,
                            atol=0.0) == []
    assert twin_mismatches(s_proj, sec_proj, t_offset=month, exempt=SPLICE_EXEMPT,
                           codes=codes(sec_proj), atol=0.0) == []


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize("s_point, k", FUTURES, ids=[f"point{p}-k{k}" for p, k in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of cover, and every
    cell of S's but :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own
    frame, moved ``k`` later, ``result_cf_annual`` included: once its pre-issue months are
    dropped, its policy years are S's.  Both compare to 1e-9 relative with no absolute
    floor, as the splice does.  An S cell this model lacked would fail it.  Before issue
    every ``result_cf`` and ``result_pols`` column is an exact zero, and the policies
    arrive in month ``k`` as new business.

    The last assertion is R1 and D4's base rule made testable.  After every report, no
    decrement rate has been evaluated at a month before issue.  A count recursion based at
    ``t == 0`` rather than at ``t_entry()``, or a decrement count that evaluates its rate
    before asking whether the month is in cover, still gives the right numbers.  This is
    the only test that sees the first, and the guard test sees the second too.

    The pre-issue rows are asserted present before they are asserted zero: a frame that
    opened at issue would have none, and their zeros would hold of nothing.
    """
    s, sec = spliced
    s_proj, sec_proj = _point(s, s_point), _row(sec, "future", s_point, -k)
    df, pols = sec_proj.result_cf(), sec_proj.result_pols()
    sec_proj.result_cf_annual()
    assert frame_mismatches(s_proj.result_cf(), df, t_offset=-k, atol=0.0) == []
    assert twin_mismatches(s_proj, sec_proj, t_offset=-k, exempt=FUTURE_EXEMPT,
                           codes=codes(sec_proj), atol=0.0) == []
    assert list(df.index[:k]) == list(pols.index[:k]) == list(range(k))
    assert (df.loc[:k - 1] == 0.0).all().all()
    assert (pols.loc[:k - 1] == 0.0).all().all()
    assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
    early = {name: sorted(t for t in sec_proj.cells[name].keys() if t < k)
             for name in DECREMENT_RATES}
    assert not any(early.values()), f"rates evaluated before issue: {early}"


# ---------------------------------------------------------------------------
# D11's R1 and R2, and D3's closed-form clock


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced):
    """R1, R2 and D3, on the splice's grid and on a fresh read of the committed model.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's grid holds points in force at every month T2 names, the variants among
    them, and points issued later, and on each the three reports are run first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents.
      ``Term_US_S``'s ``conv_rate`` asked twelve months ahead for the final year.

    The other two need a model on which nothing has been evaluated yet, so they run on a
    fresh read of the committed model:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(500)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 501 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, the three reports run on every committed point, each column in
      ascending ``t``.  A forward recursion, through ``t - 1``, finds the month before
      already cached and stays shallow, which is why D3 is asserted on its own.  A
      backward recursion over the frame, through ``t + 1``, keeps every step within the
      look-ahead but opens a chain as long as the frame, which a compiled model would run
      on the C stack (F7), and fails here.
    """
    sec = spliced[1]
    negative, ahead = set(), set()
    for key in point_keys(sec):
        p = projection(sec, key)
        for report in ("result_cf", "result_pols", "result_cf_annual"):
            p.cells[report]()
        for name, cells in p.cells.items():
            t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
            for args in _cached_args(cells):
                if any(_month(a) and a < 0 for a in args):
                    negative.add(f"{name}{args}")
                if t_pos is None:
                    continue
                for node in cells.preds(*args):
                    params = getattr(node.obj, "parameters", None) or ()
                    u = node.args[params.index("t")] if "t" in params else None
                    if _month(u) and u > args[t_pos] + 1:
                        ahead.add(f"{name}{args} -> {node.obj.name}{node.args}")
    assert not negative, f"called before the valuation date: {sorted(negative)[:10]}"
    assert not ahead, f"read beyond t + 1: {sorted(ahead)[:10]}"
    deep, limit = [], mx.get_recursion()
    fresh = mx.read_model(model_path(SEC), name=_name("fresh"))
    try:
        p = _row(fresh, "twin", 1, 0)
        assert p.duration_mth(500) == 500
        assert list(p.cells["duration_mth"].keys()) == [500]
        labels = fresh.Data.model_point_table().index
        mx.set_recursion(CALL_DEPTH)
        try:
            for key, point_id in zip(point_keys(fresh), labels):
                p = projection(fresh, key)
                for report in ("result_cf", "result_pols", "result_cf_annual"):
                    try:
                        p.cells[report]()
                    except Exception as err:    # reported, so every point is run
                        deep.append(f"point {point_id}: {report}() raised {_raised(err)}")
                        break
        finally:
            mx.set_recursion(limit)
    finally:
        fresh.close()
    assert not deep, f"under a recursion limit of {CALL_DEPTH}: {deep}"


def _cold_depth(proj, cell, args):
    """How many cells deep ``cell(*args)`` runs on ``proj``, by modelx's stack trace."""
    mx.start_stacktrace(maxlen=None)
    try:
        proj.cells[cell](*args)
        trace = mx.get_stacktrace(summarize=False)
    finally:
        mx.stop_stacktrace()
    level = deepest = 0
    for event, *_ in trace:
        level += 1 if event == "ENTER" else -1
        deepest = max(deepest, level)
    return deepest


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold ``net_cf`` in the last month runs one cell a month back to ``t_entry`` (D5).

    On a model just read, nothing is cached, so ``net_cf(proj_len() - 1)`` runs the count
    chain from the end of the frame back to the first month on the books, and modelx's
    stack trace counts how deep.  The chain may be one cell a month and no more, plus at
    most :data:`CHAIN_OVERHEAD` cells above and below it: on the committed twin's
    720-month frame, and on the contract's two longest, issued at 18 and 120 months on
    (:func:`_contract_extremes`), where 924 months of cover run to 1,043.  No number shows
    the depth, and a compiled model runs the chain on the C stack, so a chain of two
    cells a month, which gives the same numbers, needs twice the stack the 1 MiB test
    allows for, on every platform (F7).
    """
    rows, edits = _contract_extremes()
    reads = [(model_path(SEC), [0]), (_sec_inputs(tmp_path, rows, edits), [0, 1])]
    found = []
    for folder, keys in reads:
        for key in keys:
            fresh = mx.read_model(folder, name=_name("depth"))
            try:
                assert fresh.Projection.issue_age_min == CONTRACT_MIN_AGE
                p = projection(fresh, key)
                last = p.proj_len() - 1
                depth = _cold_depth(p, "net_cf", (last,))
                allowed = last - p.t_entry() + CHAIN_OVERHEAD
                if depth > allowed:
                    found.append(f"point {p.point_id()}: net_cf({last}) cold runs {depth} "
                                 f"cells deep, beyond {allowed}, one a month back to "
                                 f"t_entry() {p.t_entry()} and {CHAIN_OVERHEAD} more")
            finally:
                fresh.close()
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, conversions, lapses and expiries alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, BEF_DECR)``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, BEF_NB)``, is the four outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month too
    long: the expiries would then leave a month late, and the count would carry over.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_conv(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, p.BEF_DECR) - p.pols_if_at(t + 1, p.BEF_NB)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


# What T4 multiplies policy_count by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5


def test_scaling_the_count_scales_every_flow_and_no_per_policy_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    policy.

    The committed table, and a copy with every count multiplied by :data:`COUNT_FACTOR`,
    are each read with :data:`CONVERSION_ON` set before either computes anything: the two
    conversion rates, which ship at zero, switched on at the splice's values, so that every
    flow is nonzero on some point, the conversions and their credit among them, which the
    shipped zeros make 0 on every point.  On every point ``result_cf``, ``result_pols`` and
    ``result_cf_annual`` are 2.5 times the committed table's, element by element, to 1e-12
    relative: a scaled count is a computed float, which may come back from the CSV within
    two ulps (``sec_support``'s module docstring).  So is every other cell of
    :data:`COUNTED`, at every argument the sweep of the committed table's point cached: the
    survivors of the month's deaths, which no report shows, and the count at each timing
    among them.  And every cell outside :data:`COUNTED` (the premium per policy, the face
    amount, the rates, both clocks, the phases, the flags) agrees bit for bit at every
    argument that sweep cached.  So a flow that dropped the count, or read it as whole
    policies, which a table of counts of 1 hides from every comparison with S and a count
    doubled hides here, fails (USLIB-SEC-PLAN.md §5.2, T4, precised at M11).  Each counted
    cell is nonzero on some point.
    """
    table = _committed()
    base = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("counted"))
    scaled = mx.read_model(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), name=_name("scaled"))
    reports = ("result_cf", "result_pols", "result_cf_annual")
    counted = sorted(COUNTED - set(reports))
    nonzero = set()
    try:
        for model in (base, scaled):
            for ref, value in CONVERSION_ON.items():
                setattr(model.Projection, ref, value)
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
            one, many = projection(base, key), projection(scaled, scaled_key)
            sweep(one)
            for report in reports:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                want = COUNT_FACTOR * b
                bad = ((d - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
            for name in counted:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= 1e-12 * abs(want), (key, name, args, got,
                                                                  want)
                    if want != 0.0:
                        nonzero.add(name)
            assert twin_mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED,
                                   rtol=0.0, atol=0.0) == []
    finally:
        scaled.close()
        base.close()
    assert nonzero == set(counted), f"0 on every point: {sorted(set(counted) - nonzero)}"


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, read from a copy.  The checks
# run over the whole table as it is read, in Data, and the message names the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, or a duration, that is not a
# number.  The repeated point_id holds another policy under the same label, as a bad
# extract would, so that the check must look at the labels and not at whole rows.

MALFORMED = [
    ("a negative count", _set("policy_count", [4], -0.1),
     "policy_count must be a number, zero or more; it is not at point_id [4]"),
    ("a blank count", _set("policy_count", [3], float("nan")),
     "policy_count must be a number, zero or more; it is not at point_id [3]"),
    ("two bad counts", _set("policy_count", [3, 5], -1.0),
     "policy_count must be a number, zero or more; it is not at point_id [3, 5]"),
    ("a text count", _set("policy_count", [4], "abc"),
     "policy_count must be a number, zero or more; it is not at point_id [4]"),
    ("an infinite count", _set("policy_count", [4], float("inf")),
     "policy_count must be a number, zero or more; it is not at point_id [4]"),
    ("a fractional duration", _set("duration_mth", [4], 126.5),
     "duration_mth must be a whole number of months; it is not at point_id [4]"),
    ("a blank duration", _set("duration_mth", [6], float("nan")),
     "duration_mth must be a whole number of months; it is not at point_id [6]"),
    ("a text duration", _set("duration_mth", [4], "x12"),
     "duration_mth must be a whole number of months; it is not at point_id [4]"),
    ("issued beyond the horizon", _set("duration_mth", [6], -121),
     "duration_mth must be -120 or more, a policy issued at most 120 months after the "
     "valuation date; it is not at point_id [6]"),
    ("no duration column", lambda t: t.drop(columns="duration_mth"),
     "model_point_table_sec.csv has no duration_mth column"),
    ("no count column", lambda t: t.drop(columns="policy_count"),
     "model_point_table_sec.csv has no policy_count column"),
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[3]].assign(policy_id="TL-000009")]),
     "model_point_table_sec.csv: point_id [3] appears more than once"),
]


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(tmp_path, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5)."""
    model = _read_edited(tmp_path, edit)
    try:
        _refused(model.Data.model_point_table, message)
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued three months on.  It reads at the
    shipped 120 months and at 3, the shortest horizon that admits it, and is refused at 2,
    by name.  At 0 the model takes no future new business, D4's fallback for a product
    that cannot support it, and the message says so.  A negative horizon is itself
    refused.  Setting the Reference clears the table, so each value is read afresh.
    """
    future = _label(_committed(), "future", 1, -3)
    later = (f"model_point_table_sec.csv: duration_mth must be -2 or more, a policy issued "
             f"at most 2 months after the valuation date; it is not at point_id [{future}]")
    no_future = (f"model_point_table_sec.csv: duration_mth must be 0 or more: this model "
                 f"takes no future new business; it is not at point_id [{future}]")
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("horizon"))
    try:
        assert model.Data.future_horizon_mth == 120
        negative = "future_horizon_mth must be 0 months or more, not -1"
        for horizon, refusal in ((3, None), (2, later), (0, no_future), (-1, negative),
                                 (120, None)):
            model.Data.future_horizon_mth = horizon
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(_committed()), horizon
            else:
                _refused(model.Data.model_point_table, refusal)
    finally:
        model.close()


def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path):
    """A point whose cover has ended has no frame, and ``proj_len()`` refuses it by name.

    The point in its last covered month is moved on to ``duration_mth`` 720, the month
    cover ends.  That is a rule of the product, not of the table: it needs ``expiry_age``,
    a Projection Reference, so the table reads, and the point is refused where its frame is
    defined, on its first projection, rather than projecting nothing.  A loop over the
    block would meet it only at that point, after projecting the points before it, so
    ``run_sec.py --block``, run beside the table, asks every point for its frame first: it
    fails naming the point, and prints nothing before.
    """
    last = _label(_committed(), "derived", 1, 719)
    model = _read_edited(tmp_path, _set("duration_mth", [last], 720))
    message = (f"point_id {last}: duration_mth 720 is at or past the end of cover, "
               f"policy month 720")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_row(model, "derived", 1, 719).result_cf, message)
    finally:
        model.close()
    runner = tmp_path / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def _premium_rates_with_plan(plan):
    """An edit of ``premium_rates.csv`` that adds a scale for ``plan``, the anchor cell's
    own under it: a level period the contract does not offer, with a premium for every year
    of cover, so that nothing but ``proj_len()`` stands between such a point and its
    projection.  A copy's file only, never the committed one."""
    def edit(rates):
        anchor = rates[_anchor_rows(rates)]
        added = anchor.assign(plan=plan, provenance="the anchor cell's, for a test")
        return pd.concat([rates, added], ignore_index=True)
    return edit


# What the contract does not issue, refused by proj_len() as a point past its cover is, as
# (case, the table's edit, the other inputs' edits, the point it is made at, the message,
# and the bound which, lowered, lets the point project).  Data decodes a plan and reads an
# issue age as Term_US_S does, so each reads; the plans are T10, T20 and T30, and none
# issues below 18 (product-spec.md), from which spec_sec.py sizes the compiled caches.
# Each bound is refused just inside it, nine years and age 17, and accepted at it: every
# committed point's plan is T10 or longer, and the depth test projects the contract's
# extremes, issued at 18 (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).
NOT_ISSUED = [
    ("a nine-year level period", _set("plan", [2], "T9"),
     {"premium_rates.csv": _premium_rates_with_plan("T9")}, 2,
     "point_id 2: the plan's level period, 9 years, is below policy_term_min, 10",
     ("policy_term_min", 9)),
    ("a five-year level period", _set("plan", [2], "T5"),
     {"premium_rates.csv": _premium_rates_with_plan("T5")}, 2,
     "point_id 2: the plan's level period, 5 years, is below policy_term_min, 10",
     ("policy_term_min", 5)),
    ("a level period of no years", _set("plan", [2], "T0"), None, 2,
     "point_id 2: the plan's level period, 0 years, is below policy_term_min, 10", None),
    ("a negative level period", _set("plan", [2], "T-5"), None, 2,
     "point_id 2: the plan's level period, -5 years, is below policy_term_min, 10", None),
    ("an issue age below 18", _set("age_at_entry", [6], 17), None, 6,
     "point_id 6: issue age 17 is below issue_age_min, 18", None),
]


@pytest.mark.parametrize("case, edit, edits, point, message, bound", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    edits, point, message,
                                                                    bound):
    """``proj_len()`` refuses a level period below ten years and an issue age below 18.

    Each reads: ``Data`` decodes ``T9`` as a level period of 9, ``T5`` as 5, ``T0`` as 0
    and ``T-5`` as -5, as ``Term_US_S`` reads its plans, and an issue age is any whole
    number.  ``Term_US_S`` projects such a point as far as its tables let it, and so would
    modelx here, but the compiled model's caches are sized from the contract, from issue
    at 18, PLT years after the shortest level period, ten years, and the shipped horizon
    (``spec_sec.py``): a point issued at 17 runs past them, and so does a five-year plan
    issued at 18, whose PLT years run to 72.  So the frame refuses such a point, naming it,
    as it refuses a point past its cover, and every report with it, in modelx as compiled.
    Each bound is refused just inside it, at nine years and at 17, where a bound off by one
    would let the point through.  The nine- and five-year plans have schedules of their own
    in the copy, and each projects once ``policy_term_min`` is lowered to its level period:
    the Reference is what refuses it.
    """
    model = mx.read_model(_sec_inputs(tmp_path, edit(_committed()), edits),
                          name=_name("not_issued"))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point).result_cf, message)
        if bound is not None:
            reference, value = bound
            setattr(model.Projection, reference, value)
            assert len(_point(model, point).result_cf()) == 720
    finally:
        model.close()


def test_the_edges_of_the_in_force_interface_are_accepted(tmp_path):
    """A zero count, durations written as floats and the horizon itself read and project.

    A count of 0 is a point that projects zeros; ``12.0`` is a whole number of months, read
    back as the int the policy clock counts in; and a policy issued 120 months after the
    valuation date, the shipped ``future_horizon_mth``, is the last one the table admits,
    with a frame of 840 months, 720 of cover after 120 before issue.
    """
    committed = _committed()
    last = _label(committed, "derived", 1, 719)
    future = _label(committed, "future", 1, -3)

    def edit(table):
        table = _set("policy_count", [last], 0.0)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        return _set("duration_mth", [future], -120.0)(table)

    model = _read_edited(tmp_path, edit)
    try:
        assert model.Data.model_point_table()["duration_mth"].dtype == float
        df = _row(model, "derived", 1, 719).result_cf()
        assert len(df) == 1 and (df == 0.0).all().all()
        mid = _row(model, "derived", 1, 126)
        assert mid.duration_mth(0) == 126 and type(mid.duration_mth(0)) is int
        late = _row(model, "future", 1, -3)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 840, 1.0)
    finally:
        model.close()


# The every-state test restates each S point at the edges of its windows by default, and at
# every month of its frame with USLIB_SEC_FULL=1, which one leg of the CI matrix sets
# (USLIB-SEC-PLAN.md K6).
SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"


def _every_state_months(start, end):
    """The S months a point whose S frame runs from ``start`` to ``end`` is restated at.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of the
    first policy year, each anniversary and the month before it, where the level period,
    the conversion window and the shock close and a year's premiums fall due, and the last
    month of the frame, where cover ends.  With ``USLIB_SEC_FULL=1``, every month.  Each
    after ``start``, the twin's month.
    """
    if SEC_FULL:
        return list(range(start + 1, end))
    months = {*range(1, 12), end - 1, *(m for a in range(12, end, 12) for m in (a - 1, a))}
    return sorted(m for m in months if start < m < end)


def _states(s):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``."""
    labels = s.Data.model_point_table().index
    return [(point_id, d) for key, point_id in zip(point_keys(s), labels)
            for d in _every_state_months(0, projection(s, key).proj_len())]


def _restated(root, s, states, edits=None):
    """The twins of ``s``'s points and a row in force at each of ``states``, ``(S point,
    month)``, built by the generator out of ``s`` into a copy of the product directory
    whose other inputs ``edits`` changes: ``(folder, table)``."""
    spec = dataclasses.replace(SEC_SPECS[SEC], derived=tuple(states), future=())
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    return _sec_inputs(root, table, edits), table


def _refused_in_force(folder, refs):
    """What ``Data`` and ``proj_len()`` refuse of the table in ``folder``, read with
    ``refs`` set first: ``Data``'s refusal, or each row's ``proj_len()``'s, each by the line
    that names it.  Each row is released once asked, as ``run_sec.py --block`` releases its
    points."""
    model = mx.read_model(folder, name=_name("every"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        try:
            model.Data.model_point_table()
        except Exception as err:                # reported, with the rows' states
            return [f"Data: {_raised(err)}"]
        refused = []
        for key in point_keys(model):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused.append(_raised(err))
            del model.Projection[key]
        return refused
    finally:
        model.close()


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``Term_US_S`` reaches is a valid opening state (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can be, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So each
    point of S is restated in force by the generator at the edges of its windows, or with
    ``USLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
    one table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses it
    (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  Term's state is its count, which the
    conversion rates and the cap on mortality move and expense inflation does not, so the
    test runs on each set of inputs on which the counts S reaches differ (precised at M9):

    * S as shipped, its two points under its own References, conversion off, as T1 and
      the committed rows read it (``s_model``);
    * the splice's, its two points and thirteen variants under :data:`SPLICED_REFS`,
      conversion on (``spliced``);
    * the cap's, its point under the splice's References (:data:`CAPPED`), whose count
      falls below 1e-7 before the cap binds and is exactly 0 from it, which neither other
      set reaches.

    ``Term_US_SEC`` refuses no state ``Term_US_S`` reaches, so none is set aside.
    """
    s_row, _ = _capped_tables()
    capped = mx.read_model(temp_inputs(tmp_path / "capped", model_path(TWIN),
                                       model_points=s_row, edits=SPLICED_EDITS),
                           name=_name("every_capped"))
    try:
        for ref, value in SPLICED_REFS.items():
            setattr(capped.Projection, ref, value)
        sets = {"shipped": (s_model, {}, None),
                "spliced": (spliced[0], SPLICED_REFS, SPLICED_EDITS),
                "capped": (capped, SPLICED_REFS, SPLICED_EDITS)}
        found, counts = {}, {}
        for tag, (s, refs, edits) in sets.items():
            states = _states(s)
            folder, table = _restated(tmp_path / tag, s, states, edits)
            assert len(table) == len(s.Data.model_point_table()) + len(states)
            rows = table.set_index(["source_policy_id", "source_mth"])
            counts[tag] = rows["policy_count"]
            refused = _refused_in_force(folder, refs)
            if refused:
                found[tag] = f"{len(refused)} refused, first: {refused[:5]}"
    finally:
        capped.close()
    assert not found, found
    shipped, splice, cap = counts["shipped"], counts["spliced"], counts["capped"]
    both = shipped.index.intersection(splice.index)
    assert len(both) and (shipped[both] != splice[both]).any()
    assert (cap == 0.0).any() and ((cap > 0.0) & (cap < 1e-7)).any()


# ---------------------------------------------------------------------------
# Phase 2's decoding, and the reads beyond a table
#
# Data decodes the model point's text into the numbers the projection reads, and turns each
# table into an array indexed by integers (USLIB-SEC-PLAN.md R6, R7).  So Data must decode
# every value as Term_US_S's own cells read it, refuse what it cannot decode, and leave no
# read of an array's padding unrefused: a numpy read beyond a table's extent returns NaN,
# or, at -1, the last element, where Term_US_S's lookup raised KeyError.

# One point per value a decoded column can hold, each S's point 2 with that column changed:
# both sexes, every class of class_factor_table.csv, the three plans, the four modes, each
# side of every face-amount boundary, and a blank face, which both models put in band 4.
DECODED = ([("sex", value) for value in ("M", "F")]
           + [("rate_class", value) for value in ("PPlusNT", "PNT", "StdNT", "StdTob")]
           + [("plan", value) for value in ("T10", "T20", "T30")]
           + [("premium_mode", value) for value in ("A", "SA", "Q", "M")]
           + [("sum_assured", value) for value in (0.0, 249999.99, 250000.0, 499999.99,
                                                   500000.0, 999999.99, 1000000.0,
                                                   float("nan"))])

# The cells that read what Data decodes, each Term_US_S's too, which reads the text itself.
DECODING_CELLS = ("policy_term", "prem_cycle", "modal_factor", "band", "class_factor")


def test_every_decoding_is_term_us_s_own_on_every_value(tmp_path):
    """``Data`` decodes every value a column can hold as ``Term_US_S``'s cells read it.

    A point of each value of :data:`DECODED` goes into a copy of S's table, and the same
    point into a copy of SEC's, and on each pair every cell of :data:`DECODING_CELLS`
    agrees exactly, in value and in type: the level period from the plan, the cycle and
    the modal factor from the mode, the class factor from the class, and the band from the
    face, on both sides of each boundary.  T1 and the splice see these through the cells
    that use them, at the values their points carry; this sees every value, on its own,
    and runs no projection.  The premium schedule's join by plan, sex, class and band is
    the splice's: its variants each join to a schedule of their own.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    rows = []
    for i, (column, value) in enumerate(DECODED, start=1):
        row = s_table.loc[[2]].assign(**{column: value, "policy_id": f"TL-9{i:05d}"})
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    table = pd.concat(rows)
    sec_table = table.drop(columns=["pols_if_init", "duration_inforce"]).assign(
        policy_count=1.0, duration_mth=0)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=table),
                      name=_name("decoded_s"))
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", sec_table), name=_name("decoded"))
    try:
        found = []
        for (column, value), key, label in zip(DECODED, point_keys(sec), table.index):
            s_proj, sec_proj = projection(s, label), projection(sec, key)
            for cell in DECODING_CELLS:
                want, got = s_proj.cells[cell](), sec_proj.cells[cell]()
                if got != want or type(got) is not type(want):
                    found.append(f"{column} {value!r}: {cell} is {got!r}, S {want!r}")
    finally:
        sec.close()
        s.close()
    assert not found, found


def _faulty(tmp_path, table_edit=None, edits=None):
    """Term_US_SEC read from a copy whose table is ``table_edit(_committed())`` and whose
    other inputs ``edits`` changes, as :func:`sec_support.temp_inputs` takes them."""
    table = _committed() if table_edit is None else table_edit(_committed())
    folder = temp_inputs(tmp_path, model_path(SEC), model_points=table,
                         model_point_file=TABLE, edits=edits)
    return mx.read_model(folder, name=_name("faulty"))


def _anchor_rows(rates):
    """Where ``premium_rates.csv``'s rows are the anchor cell's schedule, T10/M/StdNT/1."""
    return ((rates["plan"] == "T10") & (rates["sex"] == "M")
            & (rates["rate_class"] == "StdNT") & (rates["band"] == 1))


def _year_written(year, value):
    """An edit of ``premium_rates.csv`` that writes the anchor cell's policy ``year`` as
    ``value``, text or a number; pandas then reads the whole column as text."""
    def edit(rates):
        years = rates["policy_year"].astype(object)
        at = _anchor_rows(rates) & (rates["policy_year"] == year)
        return rates.assign(policy_year=years.where(~at, value))
    return edit


def _age_written(age, value):
    """An edit of ``mort_table.csv`` that writes ``age`` as ``value``, text or a number."""
    def edit(table):
        ages = table["age"].astype(object)
        return table.assign(age=ages.where(table["age"] != age, value))
    return edit


SCHEDULE = ("premium_rates.csv: the schedule of plan T10, sex M, class StdNT, band 1 must "
            "run in whole policy years from 1 or more, without a gap or a repeat")
MORTALITY = ("mort_table.csv: the ages must run from 35 to 94 without a gap or a repeat, "
             "none negative")

# What Data cannot decode, or cannot turn into an array, as (case, the table's edit, the
# other inputs' edits, the Data cell that refuses it, its message, and whether a projection
# meets it).  Each projection reads every Data vector it decodes on its first month, and
# each table at its first read of it, so the first point meets every refusal but the
# label's, which only a refusal or a report reads.
UNDECODABLE = [
    ("an unknown premium mode", _set("premium_mode", [4], "W"), None, "prem_cycle",
     f"{TABLE}: premium_mode must be A, SA, Q or M; it is not at point_id [4]", True),
    ("a class the factors lack", _set("rate_class", [4], "Unknown"), None, "class_factor",
     "class_factor_table.csv has no factor for the rate_class of point_id [4]", True),
    ("a plan with no years", _set("plan", [4], "TX"), None, "policy_term",
     f"{TABLE}: plan must be a letter and a whole number of years, as T10; it is not at "
     f"point_id [4]", True),
    ("a plan int cannot read", _set("plan", [3, 5], "T10.0"), None, "policy_term",
     f"{TABLE}: plan must be a letter and a whole number of years, as T10; it is not at "
     f"point_id [3, 5]", True),
    ("a label that is not whole", lambda t: t.rename(index={3: 3.5}), None, "point_id",
     f"{TABLE}: point_id must be a whole number; [3.5] is not", False),
    ("a gap in a premium schedule", None,
     {"premium_rates.csv": lambda r: r[~(_anchor_rows(r) & (r["policy_year"] == 30))]},
     "premium_rates_array", SCHEDULE, True),
    ("a repeated policy year", None,
     {"premium_rates.csv": lambda r: pd.concat(
         [r, r[_anchor_rows(r) & (r["policy_year"] == 30)]])},
     "premium_rates_array", SCHEDULE, True),
    ("a policy year that is not whole", None,
     {"premium_rates.csv": lambda r: r.assign(policy_year=r["policy_year"].where(
         ~(_anchor_rows(r) & (r["policy_year"] == 30)), 30.5))},
     "premium_rates_array", SCHEDULE, True),
    ("a blank policy year", None,
     {"premium_rates.csv": lambda r: r.assign(policy_year=r["policy_year"].where(
         ~(_anchor_rows(r) & (r["policy_year"] == 30))))},
     "premium_rates_array", SCHEDULE, True),
    ("a policy year written as text", None, {"premium_rates.csv": _year_written(30, "x")},
     "premium_rates_array", SCHEDULE, True),
    ("a policy year written as text, at the first year", None,
     {"premium_rates.csv": _year_written(30, "30x")}, "premium_first_year", SCHEDULE,
     True),
    ("the last policy year written as text", None,
     {"premium_rates.csv": _year_written(60, "x")}, "premium_last_year", SCHEDULE, True),
    ("a gap in the mortality table", None,
     {"mort_table.csv": lambda m: m[m["age"] != 50]}, "mort_table_array", MORTALITY, True),
    ("an age written as text", None, {"mort_table.csv": _age_written(50, "x")},
     "mort_table_array", "mort_table.csv: an age must be a whole number; ['x'] is not",
     True),
    ("an age that is not whole", None, {"mort_table.csv": _age_written(94, 94.5)},
     "mort_age_last", "mort_table.csv: an age must be a whole number; [94.5] is not", True),
    ("a shock-lapse table with no bucket", None,
     {"shock_lapse_table.csv": lambda b: b.iloc[0:0]}, "shock_lapse_buckets",
     "shock_lapse_table.csv has no bucket", True),
]


@pytest.mark.parametrize("case, table_edit, edits, cell, message, reached", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_what_data_cannot_decode_is_refused_naming_it(tmp_path, case, table_edit, edits,
                                                     cell, message, reached):
    """``Data`` refuses a value it cannot decode, or a table its array cannot hold (R6, R7).

    Each case of :data:`UNDECODABLE` is the committed inputs with one fault, read from a
    copy, and the ``Data`` cell refuses it with ``ValueError``, naming every point or the
    schedule at fault, the first time it is read; and the first point's projection, which
    reads the cell, meets the same refusal.  ``Term_US_S`` met each of these only when a
    projection reached the point or the year: an unknown mode in ``modal_factor``, an
    unknown class or a gap at ``.loc`` and a bad plan at ``int``.  A key written as text
    makes pandas read its column as text, where ``Term_US_S``'s ``.loc`` matches no
    number; here each extent of the table reads its keys by value, as its array does, so a
    projection, which reads an extent first, meets the table's own refusal, and not
    ``int``'s, nor an extent cut short.  A value that is not a finite number, a blank
    premium or rate among them, is :data:`NOT_FINITE`'s.
    """
    model = _faulty(tmp_path, table_edit, edits)
    try:
        _refused(model.Data.cells[cell], message)
        if reached:
            _refused(projection(model, point_keys(model)[0]).result_cf, message)
    finally:
        model.close()


# What a cap, a min or a max reads.  mort_rate caps the annual rate with min, and the notes'
# M(1) rule and the PLT grading bound theirs with min and max.  Each keeps its first
# argument unless a later one compares smaller, or larger, and no comparison with NaN
# holds, so each is written with its bound second, and a NaN stays NaN (the cap's tests,
# below).  And Data refuses, naming the file, the column and every line or point at fault,
# a blank, text or infinite value wherever one of them reads it: a class factor, a base
# mortality rate, a premium, two of which make the jump ratio, an issue age, whose attained
# age indexes the mortality table, and an M(1) override, which may be blank.


def _value_written(column, rows, value):
    """An edit of an input table that writes ``value``, text or a number, into ``column``
    on the rows ``rows(table)`` selects; pandas then reads a column holding text as text."""
    def edit(table):
        cells = table[column].astype(object)
        return table.assign(**{column: cells.where(~rows(table), value)})
    return edit


def _factor(classes, value):
    """The edit of *class_factor_table.csv* that writes ``value`` as the factor of each
    class of ``classes``."""
    return {"class_factor_table.csv": _value_written(
        "factor", lambda f: f["rate_class"].isin(classes), value)}


def _rate(ages, value):
    """The edit of *mort_table.csv* that writes ``value`` as the rate at each age of
    ``ages``."""
    return {"mort_table.csv": _value_written(
        "mort_rate", lambda m: m["age"].isin(ages), value)}


def _premium(years, value, sexes=("M",)):
    """The edit of *premium_rates.csv* that writes ``value`` as the premium of each policy
    year of ``years`` in the anchor cell's schedule, T10/M/StdNT/1, of each sex of
    ``sexes``.  For F the edit first adds a copy of the anchor cell's schedule for sex F,
    which no committed point carries, every one being of sex M."""
    def edit(rates):
        if "F" in sexes:
            rates = pd.concat([rates, rates[_anchor_rows(rates)].assign(sex="F")],
                              ignore_index=True)
        at = ((rates["plan"] == "T10") & rates["sex"].isin(sexes)
              & (rates["rate_class"] == "StdNT") & (rates["band"] == 1)
              & rates["policy_year"].isin(years))
        return _value_written("premium_pp", lambda r: at, value)(rates)
    return {"premium_rates.csv": edit}


NAN, INF = float("nan"), float("inf")
FACTOR = ("class_factor_table.csv: factor must be a finite number; it is not at "
          "rate_class ")
RATE = "mort_table.csv: mort_rate must be a finite number; it is not at age "
PREMIUM = "premium_rates.csv: premium_pp must be a finite number; it is not in "
IN_SCHEDULE = "the schedule of plan T10, sex {}, class StdNT, band 1, at policy year {}"
OVERRIDE = (f"{TABLE}: plt_mort_factor_override must be a finite number or blank; it is "
            f"not at point_id ")
AGE = f"{TABLE}: age_at_entry must be a finite number; it is not at point_id "

# A value a cap, a min or a max reads that is not a finite number, as (case, the table's
# edit, the other inputs' edits, the Data cell that refuses it, its message).  Each column
# is checked whole when its array is first read, so a value no point reads, such as the
# factor of a class or the premium of a schedule no point carries, or the rate at an age
# the first point reaches only at the end of cover, is refused at the first point's first
# read of the table; and an override is refused for every point that carries one, the
# first point's projection meeting the refusal through the array it reads.  Each refusal
# names every line or point at fault, and every schedule, so each column has a case that
# faults two lines of it, and the premiums one that faults two schedules: a refusal that
# named the first alone, or checked only what a point reads, would fail one.
NOT_FINITE = [
    ("a blank class factor", None, _factor(["StdNT"], NAN), "class_factor",
     FACTOR + "['StdNT']"),
    ("a class factor written as text", None, _factor(["StdNT"], "x"), "class_factor",
     FACTOR + "['StdNT']"),
    ("an infinite class factor", None, _factor(["StdNT"], INF), "class_factor",
     FACTOR + "['StdNT']"),
    ("a blank factor of a class no point carries", None, _factor(["PNT"], NAN),
     "class_factor", FACTOR + "['PNT']"),
    ("blank factors of two classes", None, _factor(["PNT", "StdNT"], NAN), "class_factor",
     FACTOR + "['PNT', 'StdNT']"),
    ("a blank mortality rate", None, _rate([50], NAN), "mort_table_array", RATE + "[50]"),
    ("a mortality rate written as text", None, _rate([50], "x"), "mort_table_array",
     RATE + "[50]"),
    ("an infinite mortality rate", None, _rate([94], INF), "mort_table_array",
     RATE + "[94]"),
    ("blank mortality rates at two ages", None, _rate([50, 60], NAN), "mort_table_array",
     RATE + "[50, 60]"),
    ("a blank premium", None, _premium([30], NAN), "premium_rates_array",
     PREMIUM + IN_SCHEDULE.format("M", [30])),
    ("a premium written as text", None, _premium([11], "x"), "premium_first_year",
     PREMIUM + IN_SCHEDULE.format("M", [11])),
    ("an infinite premium", None, _premium([11], INF), "premium_last_year",
     PREMIUM + IN_SCHEDULE.format("M", [11])),
    ("blank premiums in two policy years", None, _premium([30, 40], NAN),
     "premium_rates_array", PREMIUM + IN_SCHEDULE.format("M", [30, 40])),
    ("a blank premium of a schedule no point carries", None, _premium([30], NAN, ("F",)),
     "premium_rates_array", PREMIUM + IN_SCHEDULE.format("F", [30])),
    ("blank premiums in two schedules", None, _premium([30], NAN, ("F", "M")),
     "premium_schedules", PREMIUM + IN_SCHEDULE.format("F", [30]) + ", nor in "
     + IN_SCHEDULE.format("M", [30])),
    ("a text M(1) override", _set("plt_mort_factor_override", [1], "high"), None,
     "plt_mort_factor_override", OVERRIDE + "[1]"),
    ("an infinite M(1) override", _set("plt_mort_factor_override", [4, 6], INF), None,
     "plt_mort_factor_override", OVERRIDE + "[4, 6]"),
    ("a negative infinite M(1) override", _set("plt_mort_factor_override", [1], -INF),
     None, "plt_mort_factor_override", OVERRIDE + "[1]"),
    ("a blank issue age", _set("age_at_entry", [3], NAN), None, "age_at_entry",
     AGE + "[3]"),
    ("an issue age written as text", _set("age_at_entry", [1], "x"), None, "age_at_entry",
     AGE + "[1]"),
    ("an infinite issue age", _set("age_at_entry", [1], INF), None, "age_at_entry",
     AGE + "[1]"),
    ("blank issue ages at two points", _set("age_at_entry", [1, 3], NAN), None,
     "age_at_entry", AGE + "[1, 3]"),
]


@pytest.mark.parametrize("case, table_edit, edits, cell, message", NOT_FINITE,
                         ids=[c[0] for c in NOT_FINITE])
def test_a_value_a_bound_reads_is_refused_unless_it_is_a_finite_number(tmp_path, case,
                                                                       table_edit, edits,
                                                                       cell, message):
    """``Data`` refuses a blank, text or infinite value a cap, a ``min`` or a ``max`` reads.

    Each case of :data:`NOT_FINITE` is the committed inputs with one such value, or two in
    one column, read from a copy.  The ``Data`` cell refuses it with ``ValueError`` the
    first time it is read, naming the file, the column and every line or point at fault,
    and the first point's projection, which reads the cell, meets the same refusal.  No
    other rule refuses the copy: every other ``Data`` cell reads, or meets this refusal
    through the cell it reads.

    Without these refusals, the cap reads an infinite factor, base rate or M(1) override
    as certain death, and the ``max`` of the PLT grading a negative infinite M(1) as 2.0,
    without a word; a blank or infinite issue age reads as the least int64, and a text
    value raises numpy's error, or ``int``'s, naming nothing.  ``Term_US_S`` met each only
    when a projection reached it: it raised on text and on a blank or infinite age, read an
    infinite factor, base rate or M(1) override as certain death at its cap and a negative
    infinite M(1) override as its grading's floor, 2.0, without a word, and projected NaN
    or an infinity from the rest.
    """
    model = _faulty(tmp_path, table_edit, edits)
    try:
        _refused(model.Data.cells[cell], message)
        for name, cells in model.Data.cells.items():
            try:
                cells()
            except Exception as err:            # this case's refusal alone may be met
                assert message in str(err), f"Data.{name}: {_raised(err)}"
        _refused(projection(model, point_keys(model)[0]).result_cf, message)
    finally:
        model.close()


def test_a_read_beyond_a_table_is_refused_naming_its_point(tmp_path):
    """The one cell that reads each padded array refuses a key outside the table (R1, R7).

    ``mort_rate_base`` and ``premium_pp_ann_py`` check the attained age and the policy
    year against both ends of their table first, and raise ``ValueError`` naming the point
    and the key, where ``Term_US_S``'s lookup raised ``KeyError``: point 2 issued at 30,
    five years below the mortality table, in its first month; with the anchor cell's
    schedule cut to fifty policy years, point 1 at year 51, and at year 0, below any
    schedule; and point 4, of a sex no schedule has, at year 1.  Without the checks each
    read would return the array's padding.

    The padding is NaN, as the ``Data`` docstrings say, so that a read past a check, were
    one lost, would make every number after it NaN rather than another rate: the ages
    below the mortality table's first, row 0 and column 0 of the premium array, and every
    year outside a schedule's first and last.
    """
    young = _faulty(tmp_path / "young", _set("age_at_entry", [2], 30))
    try:
        twin = _row(young, "twin", 2, 0)
        message = "point_id 2: mort_table.csv has no rate at attained age 30"
        _refused(lambda: twin.mort_rate_base(0), message)
        _refused(twin.result_cf, message)
    finally:
        young.close()
    cut = _faulty(tmp_path / "cut", _set("sex", [4], "F"), {
        "premium_rates.csv": lambda r: r[~(_anchor_rows(r) & (r["policy_year"] > 50))]})
    try:
        anchor, other = _row(cut, "twin", 1, 0), _row(cut, "derived", 1, 126)
        for proj, year in ((anchor, 51), (anchor, 0), (other, 1)):
            label = proj.point_id()
            _refused(lambda: proj.premium_pp_ann_py(year),
                     f"point_id {label}: premium_rates.csv has no premium for policy "
                     f"year {year}")
        assert anchor.premium_pp_ann_py(50) == 30965.0
        data = cut.Data
        assert np.isnan(data.mort_table_array()[:data.mort_age_first()]).all()
        rates = data.premium_rates_array()
        assert np.isnan(rates[0]).all() and np.isnan(rates[:, 0]).all()
        first, last = data.premium_first_year(), data.premium_last_year()
        for s in range(1, len(rates)):
            outside = [y for y in range(rates.shape[1]) if not first[s] <= y <= last[s]]
            assert np.isnan(rates[s, outside]).all(), s
            assert not np.isnan(rates[s, first[s]:last[s] + 1]).any(), s
        assert last[anchor.premium_schedule()] == 50 and rates.shape == (2, 51)
    finally:
        cut.close()


def test_a_key_written_as_a_float_reads_as_term_us_s_reads_it(sec_model, tmp_path):
    """A table's key written ``1.0`` is the key 1, as ``Term_US_S``'s lookups match it.

    pandas reads a column as floats as soon as one of its cells is written so, or is
    blank, and ``Term_US_S``'s ``.loc`` matches 1 against 1.0, so its tables project the
    same with their keys written either way.  ``Data`` reads a key by its value too: with
    the premium schedule's policy years and bands and the mortality table's ages written
    as floats, and so read, every committed point projects exactly the committed model's
    ``result_cf`` and ``result_pols``.  A key that is not a whole number is refused
    (:data:`UNDECODABLE`).
    """
    def floats(*columns):
        return lambda df: df.assign(**{c: df[c].astype(float) for c in columns})

    model = _faulty(tmp_path, edits={"premium_rates.csv": floats("policy_year", "band"),
                                     "mort_table.csv": floats("age")})
    try:
        keys = model.Data.premium_rates().index
        assert keys.get_level_values("policy_year").dtype == float
        assert keys.get_level_values("band").dtype == float
        assert model.Data.mort_table().index.dtype == float
        for key, base_key in zip(point_keys(model), point_keys(sec_model)):
            mine, base = projection(model, key), projection(sec_model, base_key)
            for report in ("result_cf", "result_pols"):
                pd.testing.assert_frame_equal(mine.cells[report](), base.cells[report](),
                                              check_exact=True)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what ``Term_US_S`` and its table generate today.

    Every row and column, the text cells included: an edit to an S row the table copies or
    derives from fails here until ``python tools/gen_sec_points.py Term_US_SEC`` regenerates
    it, in the same commit.  Text and integers compare exactly, and a float by its value, to
    1e-12, because the text the writer picks for a computed float depends on the platform's
    parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin the two coincide, and its policies enter as new business at ``t = 0``.  The
    point in force 126 months is in policy year 11 at attained age 45 at ``t = 0``, has 594
    months of cover left, and expires at ``t = 594``.  The point issued three months on has
    nothing in force and nothing to do before ``t = 3``, its phase reading ``PRE_ISSUE``,
    and a frame of 723 months.  The point in its last covered month has a one-month frame,
    in which its survivors expire.  The phases are the model's codes.  And ``pols_if_at``
    knows its two timings alone: a code that names neither, such as the one after
    ``BEF_DECR``, where ``basiclife.BasicTerm_SE`` would number its ``BEF_MAT``, is refused
    rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 719)] == [0, 1, 719]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    mid = _row(sec_model, "derived", 1, 126)
    assert (mid.duration_mth(0), mid.duration(0), mid.policy_year(0), mid.age(0)) == (
        126, 10, 11, 45)
    assert (mid.duration_mth(6), mid.policy_year(6), mid.age(6)) == (132, 12, 46)
    assert (mid.t_entry(), mid.expiry_mth(), mid.proj_len()) == (0, 720, 594)
    assert mid.is_active(593) and not mid.is_active(594)
    assert (mid.phase(0), mid.phase(594)) == (mid.PLT, mid.EXPIRED)
    fut = _row(sec_model, "future", 1, -3)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-3, 3, 723)
    assert not fut.is_active(2) and fut.is_active(3)
    assert [fut.phase(t) for t in (0, 2, 3, 722, 723)] == [
        fut.PRE_ISSUE, fut.PRE_ISSUE, fut.LEVEL, fut.PLT, fut.EXPIRED]
    assert (fut.pols_if_init(), fut.pols_new_biz(3), fut.pols_if(3)) == (0.0, 1.0, 1.0)
    last = _row(sec_model, "derived", 1, 719)
    assert (last.proj_len(), last.age(0), last.policy_year(0)) == (1, 94, 60)
    assert last.pols_maturity(0) > 0.0 and last.pols_if(1) == 0.0
    assert last.pols_if(0) - last.pols_maturity(0) == pytest.approx(
        last.pols_death(0) + last.pols_lapse(0) + last.pols_conv(0), abs=1e-15)
    _refused(lambda: twin.pols_if_at(0, twin.BEF_DECR + 1), "invalid timing")


def test_a_policy_in_force_mid_art_pays_its_next_premium_on_its_anniversary(sec_model,
                                                                            s_model):
    """In force 126 months, the anchor cell is midway through its first ART year, year 11.

    It opens with the count S carries into month 126, which is ``pols_if_init()`` and the
    count of row 0.  The year's premium fell due on the tenth anniversary, six months before
    the valuation date, so none falls due until ``t = 6``, the eleventh anniversary, which
    collects policy year 12's 830.0.  Mortality is policy year 11's, at M(1), then year
    12's, at M(2); the lapse rate and the commission are the ART years'.  Every column that
    does not carry inflation is S's from month 126 on.  Summed into policy years, the table
    opens at year 11 with the rest of that year, which holds no premium and counts the
    policies in force at the valuation date, and from year 12 on it is S's.  Both compare
    to 1e-9 relative with no absolute floor, as the splice does.

    The opening count is S's, read back from the CSV, so it is compared with S's value to
    1e-12; among the SEC model's own cells the equality is exact.
    """
    p, s = _row(sec_model, "derived", 1, 126), _point(s_model, 1)
    assert p.policy_count() == pytest.approx(s.pols_if(126), rel=1e-12)
    assert p.pols_if(0) == p.pols_if_init() == p.policy_count()
    assert [p.premium_pp(t) for t in range(7)] == [0.0] * 6 + [830.0]
    assert p.mort_rate(0) == pytest.approx(0.0018 * 3.50, rel=1e-12)
    assert p.mort_rate(6) == pytest.approx(0.0020 * 3.35, rel=1e-12)
    assert (p.lapse_rate(0), p.lapse_rate(6), p.comm_rate(6)) == (0.30, 0.15, 0.02)
    cols = ["pols_if", "premiums", "claims", "commissions", "premium_taxes",
            "conv_credits"]
    assert frame_mismatches(s.result_cf(), p.result_cf(), t_offset=126,
                            columns=cols, atol=0.0) == []
    ann, s_ann = p.result_cf_annual(), s.result_cf_annual()
    assert list(ann.index) == list(range(11, 61))
    assert ann.loc[11, "pols_if"] == p.pols_if(0) and ann.loc[11, "premiums"] == 0.0
    pd.testing.assert_frame_equal(ann.loc[12:, cols], s_ann.loc[12:, cols],
                                  rtol=1e-9, atol=0.0)


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2%, the factor at ``t`` is ``1.02^(t/12)`` on the point in force 126
    months and on the point issued three months on alike, whatever their durations.  So the
    point in force pays S's month-``126 + t`` maintenance deflated by ``1.02^(126/12)``, the
    inflation S had already applied since issue, and the future point pays S's month-``t``
    maintenance inflated by ``1.02^(3/12)``, the inflation of the months before its issue.
    Acquisition is not inflated on either.  This is the only test that sees inflation run on
    the policy clock: the splice sets the rate to 0, and on a point issued at ``t = 0`` the
    clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    mid, fut = _row(sec_model, "derived", 1, 126), _row(sec_model, "future", 1, -3)
    s = _point(s_model, 1)
    for t in (0, 6, 12):
        assert mid.inflation_factor(t) == fut.inflation_factor(t) == (
            (1 + INFLATION) ** (t / 12))
    for t in range(mid.proj_len()):
        assert mid.expenses(t) == pytest.approx(
            s.expenses(126 + t) / (1 + INFLATION) ** (126 / 12), rel=1e-12), t
    for t in range(s.proj_len()):
        acq = s.expense_acq if t == 0 else 0.0
        assert fut.expenses(3 + t) - acq == pytest.approx(
            (s.expenses(t) - acq) * (1 + INFLATION) ** (3 / 12), rel=1e-12), t


def test_acquisition_is_charged_on_new_business_only(sec_model):
    """``expense_acq`` per policy issued, in the issue month, never on a policy in force.

    On every committed point, what ``expenses(t)`` holds beyond its maintenance part is
    ``expense_acq * policy_count()`` in the issue month, ``t = -duration_mth``, and 0 in
    every other month, to 1e-9: the twins bear it at ``t = 0``, the points already in force
    never, and the point issued three months on at ``t = 3``.

    ``Term_US_S`` charges it once per model point, whatever the count, so the twins (T1)
    and the future rows (T3) agree with S cell by cell only while each S point counts
    one policy, as S's points do.  That is asserted first, so that an S table with
    another count fails here, saying why, beside T1 and T3 failing on the issue month's
    ``expenses``.
    """
    table = sec_model.Data.model_point_table()
    twins = table[table["row_kind"] == "twin"]
    assert (twins["policy_count"] == 1.0).all(), (
        f"T1 and T3 hold on Term only while each S point counts one policy (sec_support's "
        f"SecSpec comment); the twins count {twins['policy_count'].tolist()}")
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        ts = range(p.proj_len())
        acq = [p.expenses(t) - p.expense_maint / 12 * p.inflation_factor(t) * p.pols_if(t)
               for t in ts]
        issue = -table.at[point_id, "duration_mth"]
        expected = [p.expense_acq * p.policy_count() if t == issue else 0.0 for t in ts]
        assert acq == pytest.approx(expected, abs=1e-9), point_id


def test_every_guarded_cell_holds_its_outside_cover_value():
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value at all:
    ``is_active``'s docstring promises that outside cover no count evaluates a rate, and no
    table is read at a policy year or an attained age the policy does not have.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, nothing reads ``mort_rate_base`` or ``conv_elig`` there, and an unguarded
    count multiplies its rate by zero.  They are held here because they are what the
    docstrings promise a caller, and because Phase 2 needs them: a table read at a policy
    year or an age the policy does not have would wrap round in a compiled model rather than
    fail (USLIB-SEC-PLAN.md F4, R1).  A cell that raises instead is reported as a fault too.
    """
    model = mx.read_model(model_path(SEC), name=_name("cover"))
    try:
        faults = []
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            for t in [*range(p.t_entry()), p.proj_len()]:
                calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
                calls += [("pols_if_at", (t, timing), 0.0)
                          for timing in (p.BEF_NB, p.BEF_DECR)]
                for name, args, want in calls:
                    where = f"point {point_id}: {name}{args}"
                    try:
                        got = p.cells[name](*args)
                    except Exception as err:        # reported, so the scan goes on
                        faults.append(f"{where} raised {_raised(err)}")
                        continue
                    if got != want or type(got) is not type(want):
                        faults.append(f"{where} = {got!r}, not {want!r}")
            read = {name: sorted(p.cells[name].keys()) for name in IN_COVER_ONLY
                    if len(p.cells[name].keys())}
            if read:
                faults.append(f"point {point_id}: evaluated outside cover: {read}")
    finally:
        model.close()
    assert not faults, f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(
        faults[:20])


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    For each S point, the frames of its twin, of the point restated at month 12 and of the
    point issued 12 months on, summed as ``run_sec.py --block`` sums them, are indexed
    0..731 and equal S's frame added to itself moved 12 months earlier and 12 months later.
    A model whose frames sat on the policy clock would fail it.
    """
    s, sec = spliced
    for s_point in S_POINTS:
        frames = [_row(sec, "twin", s_point, 0).result_cf(),
                  _row(sec, "derived", s_point, 12).result_cf(),
                  _row(sec, "future", s_point, -12).result_cf()]
        block = pd.concat(frames).groupby(level="t").sum()
        sdf = _point(s, s_point).result_cf()
        expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                              sdf.set_axis(sdf.index + 12)]).groupby(level=0).sum()
        assert list(block.index) == list(range(732))
        assert frame_mismatches(expected, block) == [], s_point


def _run_sec(script, *args, check=True):
    """Run ``script``, a ``run_sec.py``, with ``args``; its output, checked ASCII.

    With ``check=False`` the finished process is returned instead, whatever its exit code,
    for a test that expects the runner to fail.
    """
    done = subprocess.run([sys.executable, str(script), *args], capture_output=True,
                          timeout=300)
    if not check:
        return done
    assert done.returncode == 0, done.stderr.decode(errors="replace")
    assert done.stdout.isascii(), "run_sec.py printed a non-ASCII character"
    # Windows ends each printed line with "\r\n"; read them as "\n", as a frame's
    # to_string() writes them.
    return done.stdout.decode("ascii").replace("\r\n", "\n")


# The labels an extract carries in the tests below: the committed points' in reverse, from
# 106 down, so that a label is neither a position plus one nor in the order of the rows.
EXTRACT_LABELS = (106, 105, 104, 103, 102, 101)


def _extract():
    """The committed table as an administration extract would hold it: without the
    generator's columns, and labelled :data:`EXTRACT_LABELS`."""
    extract = _committed().drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    return extract


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from,
    and names each point by its label, wherever the row stands.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them.  Read without them,
    every point projects what the committed table projects, in ``result_cf`` and
    ``result_pols``, to 1e-12, and ``run_sec.py``, run beside that extract, prints the point
    without saying where it came from.  On the shipped rows ``source_mth`` equals
    ``duration_mth``, so a formula that read the one for the other would pass every test
    that leaves ``duration_mth`` as generated.

    The extract's labels are not the committed ones (:data:`EXTRACT_LABELS`), and every
    other table here numbers its points from 1 in table order, where a label and a
    position plus one cannot be told apart.  ``Projection`` is indexed by position (R4),
    so ``point_id()`` is the only way a projection learns its label: it must be the row's,
    and so must the label a refusal names, and the one the runner is given and prints.
    """
    extract = _extract()
    folder = _sec_inputs(tmp_path / "extract", extract)
    model = mx.read_model(folder, name=_name("extract"))
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(EXTRACT_LABELS)
        assert [projection(model, key).point_id() for key in point_keys(model)] == list(
            EXTRACT_LABELS)
        for key, base_key in zip(point_keys(model), point_keys(sec_model)):
            mine, base = projection(model, key), projection(sec_model, base_key)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "103")
    assert "model point 103: TL-000001-M126 - M35" in out
    assert "in force 126 months" in out
    last = extract.index[extract["policy_id"] == "TL-000001-M719"][0]
    moved = _set("duration_mth", [last], 720)(extract)
    folder = _sec_inputs(tmp_path / "moved", moved)
    message = (f"point_id {last}: duration_mth 720 is at or past the end of cover, "
               f"policy month 720")
    model = mx.read_model(folder, name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf, message)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and message in done.stderr.decode(errors="replace")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's: point 4's line at the valuation date and its first twelve rows, and the
    block's first twelve rows, which must be the committed points' frames summed row by
    row, as this test sums them.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner, "4")
    assert "TL-000001-M126 (S's TL-000001 at its month 126)" in out
    assert "in force 126 months: policy year 11, attained age 45, 0.108385 in force" in out
    mid = _row(sec_model, "derived", 1, 126)
    assert mid.result_cf().head(12).round(2).to_string() in out
    out = _run_sec(runner, "--block")
    assert "the block" in out and "TL-000001-F3" in out
    frames = [projection(sec_model, key).result_cf() for key in point_keys(sec_model)]
    block = pd.concat(frames).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out


# run_sec.py run as though it sat at /m/products/term_life, a copy too shallow to have a
# repository above it: the source compiled under that name, so that its own __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/term_life/run_sec.py"
sys.argv = [where, "--cython"]
exec(compile(source, where, "exec"), {"__name__": "__main__", "__file__": where})
"""


def test_run_sec_says_a_copy_without_the_repository_cannot_build(tmp_path):
    """``run_sec.py --cython`` outside the repository stops, saying it cannot build.

    ``--cython`` builds with the repository's ``tools/build_sec_cy.py``, which a
    ``lifelib.create()`` copy does not carry, wherever the copy is: beside a copy of the
    model and its inputs, and at a path too shallow to hold a repository above the product
    at all, which once raised ``IndexError`` where the runner looked for the tool.  Each
    must exit nonzero having printed nothing, and say why.  Neither needs modelx-cython,
    since neither gets as far as building.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    copy = _sec_inputs(tmp_path / "copy", _committed()).parent / "run_sec.py"
    shutil.copy(runner, copy)
    shallow = tmp_path / "shallow.py"
    shallow.write_text(SHALLOW_RUN, encoding="utf-8")
    for args in ((copy, "1", "--cython"), (shallow, runner)):
        done = _run_sec(*args, check=False)
        stderr = done.stderr.decode(errors="replace")
        assert done.returncode != 0 and done.stdout == b"", stderr
        assert "a lifelib.create() copy carries no tools/, so it cannot build" in stderr, (
            stderr)


def _docs(model):
    """``(where, docstring)`` for the model, each Space and each cells, blanks as ``""``."""
    yield "model", model.doc or ""
    for space in model.spaces.values():
        yield space.name, space.doc or ""
        for cells in space.cells.values():
            yield f"{space.name}.{cells.name}", cells.doc or ""


def _mapped_cells(doc):
    """The names in the Cells column of the symbol map in ``doc``, the Projection docstring.

    The map is an RST simple table whose header row starts ``Notes symbol``.  The runs of
    ``=`` in the border under the header give the column spans, and a row whose Cells
    column is blank continues the meaning of the row above.  A name is the identifier that
    opens the column, ``age`` of ``age(t)``.
    """
    lines = doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    start, end = [m.span() for m in re.finditer("=+", lines[head + 1])][1]
    names = set()
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        found = re.match(r"[a-z_][a-z0-9_]*", line[start:end].strip())
        if found:
            names.add(found.group())
    return names


def test_the_docstrings_describe_the_valuation_clock(sec_model):
    """The docstrings say what this model is, and none says what only Term_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, and names
    no cell the model lacks.  And no docstring carries a reference into the twin's Spaces
    (``~.Term_US_S.``), which the SEC pages would link to the wrong model, or S's
    "``t = 0`` is the issue month".
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "level premium term life insurance"):
        assert phrase in flat["model"], phrase
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    unknown = sorted(mapped - set(sec_model.Projection.cells))
    assert not unknown, f"the symbol map names cells the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items()
                   if re.search(r"~\.Term_US_S\.|t = 0`` is the issue month", doc))
    assert not stale, f"docstrings that describe Term_US_S: {stale}"


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1).

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` alone changed, to ``model_point_table_sec.csv``: an edit to a table
    reaches both models, and the two can never drift apart.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE}


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate caps the annual rate at 1, as Term_US_S's does (model-sec.md, *Departures from
# Term_US_S*).  On the shipped tables the product it caps passes 1 only after the level
# period and at an M(1) above the committed points', and neither they nor the splice grid
# come near it.  One point is made to pass it, the way the variants are made: S's anchor
# cell in the tobacco class, issued at 70, the ten-year plan's oldest tobacco issue age
# (product-spec.md), with M(1) at 8.0, the most the notes' rule gives, as its override.
# Its product passes 1 in policy year 21, at attained age 90, and stays past it to the end
# of cover.  It goes alone into a copy of S's table, and its twin into a copy of SEC's,
# beside the splice's premium table, which holds a tobacco schedule.
CAPPED = (1, {"policy_id": "TL-000016", "rate_class": "StdTob", "age_at_entry": 70,
              "plt_mort_factor_override": 8.0})
CAPPED_MTH = 12 * 20    # the first month of policy year 21, where the product passes 1


def _capped_tables():
    """S's table holding the :data:`CAPPED` point alone, and SEC's holding its twin."""
    base, changes = CAPPED
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s_row = s_table.loc[[base]].assign(**changes)
    sec_row = s_row.drop(columns=["pols_if_init", "duration_inforce"]).assign(
        policy_count=1.0, duration_mth=0)
    return s_row, sec_row


def _capped_in_force(sec_row, count):
    """SEC's table holding the :data:`CAPPED` point in force at the valuation date, twice.

    Point 2 is in force from the month before the cap, opened with ``count``; point 3 from
    five months into the first capped year, opened with the twin's one policy.
    """
    rows = pd.concat([sec_row.assign(duration_mth=CAPPED_MTH - 1, policy_count=count),
                      sec_row.assign(duration_mth=CAPPED_MTH + 5)])
    rows.index = pd.Index([2, 3], name="point_id")
    return rows


def _uncapped_mort_rate(s_proj, t):
    """``Term_US_S``'s annual mortality product in month t, the one its cap bounds."""
    d = s_proj.policy_year(t) - s_proj.policy_term()
    return (s_proj.mort_rate_base(t) * s_proj.class_factor()
            * (s_proj.plt_mort_factor(d) if d >= 1 else 1.0))


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On the point of :data:`CAPPED`, the product of ``Term_US_S``'s base rate, class factor
    and M(d) (:func:`_uncapped_mort_rate`) passes 1 in month :data:`CAPPED_MTH` and stays
    past it to the end of cover, on a point the contract issues.  Both models cap it:
    ``mort_rate`` and the monthly rate, ``1 - (1 - q)^(1/12)``, are 1.0 in every one of
    those months, the float, not the int 1, which compares equal to it, and floats below 1
    in every month before.  So every policy in force at the start of the first capped
    month dies in it, and none is in force after it, in both, and every report holds
    finite floats alone.

    In every cell of S's this model agrees with S at every argument S cached
    (``sec_support.twin_mismatches``), the capped months and the reports included.  It
    holds them to 1e-9 relative with no absolute floor, because the counts before the cap
    are near 1e-8.  S is swept as the splice sweeps it (:func:`_sweep_s`).

    The point in force from the month before the cap, opened with S's count, is S from
    that month on, cell by cell as a splice row is; the models run under
    :data:`SPLICED_REFS`, as the splice's do, so that its expenses are S's.  It loses every
    policy in the cap's month, and the point in force five months into the capped year
    loses every policy in its first month (:func:`_capped_in_force`).
    """
    s_row, sec_row = _capped_tables()
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_row,
                                  edits=SPLICED_EDITS), name=_name("capped_s"))
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", sec_row, SPLICED_EDITS),
                        name=_name("capped"))
    try:
        for model in (s, sec):
            for ref, value in SPLICED_REFS.items():
                setattr(model.Projection, ref, value)
        s_proj, p = projection(s, point_keys(s)[0]), projection(sec, point_keys(sec)[0])
        end = s_proj.proj_len()
        assert p.proj_len() == end == 12 * (95 - 70)
        cap = next(t for t in range(end) if _uncapped_mort_rate(s_proj, t) > 1)
        assert (cap, s_proj.age(cap), s_proj.policy_year(cap)) == (CAPPED_MTH, 90, 21)
        after = range(cap, end)
        assert all(_uncapped_mort_rate(s_proj, t) > 1 for t in after)
        for proj in (s_proj, p):
            for rate in (proj.mort_rate, proj.mort_rate_mth):
                assert all(type(rate(t)) is float and rate(t) < 1.0 for t in range(cap))
                assert [(type(rate(t)), rate(t)) for t in after] == (
                    [(float, 1.0)] * len(after))
            assert proj.pols_if(cap) > 0.0 and proj.pols_death(cap) == proj.pols_if(cap)
            assert [proj.pols_if(t) for t in range(cap + 1, end + 1)] == [0.0] * len(after)
        _sweep_s(s_proj)
        assert twin_mismatches(s_proj, p, codes=codes(p), atol=0.0) == []
        rows = _capped_in_force(sec_row, s_proj.pols_if(cap - 1))
        later = mx.read_model(_sec_inputs(tmp_path / "in_force", rows, SPLICED_EDITS),
                              name=_name("capped_in_force"))
        try:
            for ref, value in SPLICED_REFS.items():
                setattr(later.Projection, ref, value)
            before, inside = (projection(later, key) for key in point_keys(later))
            assert twin_mismatches(s_proj, before, t_offset=cap - 1, exempt=SPLICE_EXEMPT,
                                   codes=codes(before), atol=0.0) == []
            for point, capped in ((before, 1), (inside, 0)):
                rest = range(capped + 1, point.proj_len() + 1)
                assert point.mort_rate(capped) == 1.0
                assert point.pols_if(capped) > 0.0
                assert point.pols_death(capped) == point.pols_if(capped)
                assert [point.pols_if(t) for t in rest] == [0.0] * len(rest)
            frames = [s_proj.result_cf(), s_proj.result_cf_annual()]
            for point in (p, before, inside):
                frames += [point.result_cf(), point.result_pols(), point.result_cf_annual()]
            for frame in frames:
                assert (frame.dtypes == "float64").all(), frame.dtypes
                assert np.isfinite(frame.to_numpy()).all()
        finally:
            later.close()
    finally:
        sec.close()
        s.close()


def _not_a_number():
    """NaN, what a blank input carries: a formula a test puts in place of a cell's."""
    return float("nan")


# Each bound a NaN must pass through, as (the bound, the cell whose formula _not_a_number
# replaces, the row it is read on, the calls that must then be NaN).  Bound first, each call
# would be the bound or follow from it: mort_rate 1.0 in every month, every policy dead in
# month 0 and the count 0.0 after it; M(1) 8.0; every PLT factor 2.0.  Point 2 takes M(1)
# from the notes' rule, point 1 from its override.
NAN_BOUNDS = [
    ("the cap on mortality", "class_factor", ("twin", 1, 0),
     [("mort_rate", (0,)), ("mort_rate", (120,)), ("mort_rate", (719,)),
      ("mort_rate_mth", (0,)), ("pols_if", (1,))]),
    ("the min of the M(1) rule", "jump_ratio", ("twin", 2, 0),
     [("plt_mort_factor_init_formula", ()), ("plt_mort_factor_init", ()),
      ("plt_mort_factor", (1,)), ("mort_rate", (120,))]),
    ("the max of the PLT grading", "plt_mort_factor_init", ("twin", 1, 0),
     [("plt_mort_factor", (1,)), ("plt_mort_factor", (50,)), ("mort_rate", (120,)),
      ("mort_rate", (719,))]),
]


@pytest.mark.parametrize("bound, cell, row, calls", NAN_BOUNDS,
                         ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_stays_nan(bound, cell, row, calls):
    """A NaN that reaches the cap, or the M(1) rule's or the PLT grading's bound, stays NaN.

    The bounds are the M(1) rule's ``min`` and the PLT grading's ``max``.  A ``min`` or a
    ``max`` keeps its first argument unless a later one compares smaller, or larger, in
    modelx and compiled alike, and no comparison with NaN holds.  So with its bound first
    each would turn a NaN into the bound, and ``mort_rate`` would read a blank class
    factor as certain death, every flow finite.  Each is written with its bound second
    (``mort_rate``'s docstring).  ``Data`` refuses every blank input that could carry a
    NaN to one (:data:`NOT_FINITE`), so to send one a NaN, the formula of the cell that
    feeds it is replaced by one returning NaN, in a model read for the test, which modelx
    allows and a compiled model does not (USLIB-SEC-PLAN.md K7).  Each of ``calls`` must
    then be the float NaN, and not the bound: ``mort_rate`` NaN, not 1.0, where the class
    factor is NaN.  Where the product passes 1, the cap's tests above hold the other side,
    the float 1.0.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        model.Projection.cells[cell].formula = _not_a_number
        p = _row(model, *row)
        lost = []
        for name, args in calls:
            value = p.cells[name](*args)
            if not (type(value) is float and math.isnan(value)):
                lost.append(f"{name}{args} = {value!r}")
        assert not lost, f"{bound} loses a NaN {cell}(): {lost}"
    finally:
        model.close()


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when Phase 1 ended (C2).

    Phase 2 changes how the model is represented and no number it computes (D2), so before
    it changed anything the model as M1 committed it was frozen below
    (USLIB-SEC-PLAN.md §5.4): for each point, each column of ``result_cf()`` and
    ``result_pols()``, its sum, its largest absolute value and its values at five fixed
    months, the frame's first and last and the three quartiles between.  Every later
    version must reproduce it, to 1e-12 relative, floored at 1e-12 of the column's own
    magnitude (``sec_support.fingerprint_mismatches``), with the same points, frames and
    columns exactly.  ``python tools/gen_sec_fingerprint.py Term_US_SEC --check`` runs the
    same comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# Term_US_SEC's fingerprint, frozen from the model as M1 committed it and committed alone,
# before Phase 2 changed anything.  Each point is keyed by its point_id; each column holds
# (its sum over the frame, its largest absolute value, (its values at the months)).  The
# block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a refreeze
# goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: Term_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (105.59274191106616, 1.0, (
                1.0, 0.054952074038946065, 0.009515879529071392, 0.001060527490604866,
                1.9988090701711986e-05)),
            "premiums": (2933.563917599938, 140.0, (
                140.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1777.4074173656409, 8.683890549777864, (
                6.669112361223917, 3.4515200335473395, 1.5093493485977232,
                0.6274185006943673, 0.047422578259039394)),
            "commissions": (197.7504899909903, 112.0, (
                112.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (598.2770514570509, 302.5, (
                302.5, 0.18459077476354582, 0.04302069437037088, 0.006452871065825871,
                0.0001636835158481863)),
            "premium_taxes": (58.67127835199876, 2.8000000000000003, (
                2.8000000000000003, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (301.45768043425727, 283.96911236122395, (
                -283.96911236122395, -3.6361108083108853, -1.552370042968094,
                -0.6338713717601931, -0.04758626177488758)),
        },
        "result_pols": {
            "pols_if": (105.59274191106616, 1.0, (
                1.0, 0.054952074038946065, 0.009515879529071392, 0.001060527490604866,
                1.9988090701711986e-05)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.01777407417365641, 8.683890549777864e-05, (
                6.669112361223917e-05, 3.4515200335473394e-05, 1.5093493485977232e-05,
                6.2741850069436735e-06, 4.7422578259039396e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9822065825440406, 0.5198181893620692, (
                0.0051426698385184395, 0.00048006793394880006, 8.30521752869031e-05,
                9.215872245240029e-06, 1.7058261534546534e-07)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9343282303776128e-05)),
        },
    },
    2: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (105.59998511193011, 1.0, (
                1.0, 0.05498092222353764, 0.009528856477903377, 0.0010619737479832247,
                2.0015348763301852e-05)),
            "premiums": (2935.430014774729, 140.0, (
                140.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1770.8267607074974, 8.683890549777864, (
                6.669112361223917, 3.3952959396970543, 1.51140767113181, 0.6282741207928435,
                0.04748724914623046)),
            "commissions": (197.78781193448611, 112.0, (
                112.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (598.3055823777179, 302.5, (
                302.5, 0.1846876793633705, 0.04307936234192886, 0.006461670943691577,
                0.00016390673353429845)),
            "premium_taxes": (58.70860029549458, 2.8000000000000003, (
                2.8000000000000003, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (309.80125945953284, 283.96911236122395, (
                -283.96911236122395, -3.5799836190604246, -1.5544870334737388,
                -0.634735791736535, -0.04765115587976476)),
        },
        "result_pols": {
            "pols_if": (105.59998511193011, 1.0, (
                1.0, 0.05498092222353764, 0.009528856477903377, 0.0010619737479832247,
                2.0015348763301852e-05)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.017708267607074973, 8.683890549777864e-05, (
                6.669112361223917e-05, 3.395295939697054e-05, 1.51140767113181e-05,
                6.282741207928435e-06, 4.748724914623046e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9822723627318951, 0.5198181893620692, (
                0.0051426698385184395, 0.00048032502844679617, 8.31654347944232e-05,
                9.228440069601742e-06, 1.7081524143790395e-07)),
            "pols_maturity": (1.9369661030401644e-05, 1.9369661030401644e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9369661030401644e-05)),
        },
    },
    3: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (93.93790209606017, 0.939248, (
                0.939248, 0.05051368421473739, 0.00894771579513133, 0.001014988594739213,
                2.0015348763301852e-05)),
            "premiums": (2795.430014774729, 131.49472, (
                131.49472, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1693.0510187087393, 8.683890549777864, (
                6.65559997559641, 3.2216594091379847, 1.5481856181263005,
                0.6564953448394129, 0.04748724914623046)),
            "commissions": (85.78781193448613, 6.574736000000001, (
                6.574736000000001, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (263.61479994630275, 2.3481199999999998, (
                2.3481199999999998, 0.16884371768849551, 0.04005350957296639,
                0.0060847409066405725, 0.00016069287601401807)),
            "premium_taxes": (55.90860029549458, 2.6298944, (
                2.6298944, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (697.0677838897054, 113.28636962440359, (
                113.28636962440359, -3.3905031268264803, -1.588239127699267,
                -0.6625800857460534, -0.047647942022244476)),
        },
        "result_pols": {
            "pols_if": (93.93790209606017, 0.939248, (
                0.939248, 0.05051368421473739, 0.00894771579513133, 0.001014988594739213,
                2.0015348763301852e-05)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.016930510187087397, 8.683890549777864e-05, (
                6.65559997559641e-05, 3.221659409137985e-05, 1.5481856181263006e-05,
                6.564953448394129e-06, 4.748724914623046e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9222981201518827, 0.5198181893620692, (
                0.0040059082486307625, 0.000441289350361807, 7.808211405063976e-05,
                8.81524714968298e-06, 1.7081524143790395e-07)),
            "pols_maturity": (1.9369661030401644e-05, 1.9369661030401644e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9369661030401644e-05)),
        },
    },
    4: {"rows": 594, "months": (0, 148, 296, 444, 593),
        "result_cf": {
            "pols_if": (9.443086927428597, 0.10838474140322372, (
                0.10838474140322372, 0.022280560582628582, 0.00479811532002715,
                0.0006511542334572065, 1.9988090701711986e-05)),
            "premiums": (1698.3049221320648, 75.02791937521008, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (876.632544940142, 5.706695810923936, (
                5.706695810923936, 1.9255703644708833, 1.2840075283835228,
                0.5038665726999406, 0.047422578259039394)),
            "commissions": (33.9660984426413, 1.5005583875042015, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (27.907390849740615, 0.2709618535080593, (
                0.2709618535080593, 0.07111069239013718, 0.019550067471678468,
                0.0033871172630724564, 0.00013295453070536796)),
            "premium_taxes": (33.9660984426413, 1.5005583875042015, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (725.8327894568995, 66.7359420231921, (
                -5.977657664431995, -1.9966810568610205, -1.3035575958552013,
                -0.5072536899630131, -0.04755553278974476)),
        },
        "result_pols": {
            "pols_if": (9.443086927428597, 0.10838474140322372, (
                0.10838474140322372, 0.022280560582628582, 0.00479811532002715,
                0.0006511542334572065, 1.9988090701711986e-05)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.008766325449401419, 5.706695810923936e-05, (
                5.706695810923936e-05, 1.9255703644708832e-05, 1.2840075283835229e-05,
                5.038665726999407e-06, 4.7422578259039396e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.09959907267151849, 0.0031724334006080763, (
                0.0031724334006080763, 0.00019459966659596901, 4.18310145006872e-05,
                5.648090924870469e-06, 1.7058261534546534e-07)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9343282303776128e-05)),
        },
    },
    5: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (1.9988090701711986e-05, 1.9988090701711986e-05, (
                1.9988090701711986e-05,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "claims": (0.047422578259039394, 0.047422578259039394, (
                0.047422578259039394,)),
            "commissions": (0.0, 0.0, (
                0.0,)),
            "expenses": (4.997022675427996e-05, 4.997022675427996e-05, (
                4.997022675427996e-05,)),
            "premium_taxes": (0.0, 0.0, (
                0.0,)),
            "conv_credits": (0.0, 0.0, (
                0.0,)),
            "net_cf": (-0.04747254848579367, 0.04747254848579367, (
                -0.04747254848579367,)),
        },
        "result_pols": {
            "pols_if": (1.9988090701711986e-05, 1.9988090701711986e-05, (
                1.9988090701711986e-05,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (4.7422578259039396e-07, 4.7422578259039396e-07, (
                4.7422578259039396e-07,)),
            "pols_conv": (0.0, 0.0, (
                0.0,)),
            "pols_lapse": (1.7058261534546534e-07, 1.7058261534546534e-07, (
                1.7058261534546534e-07,)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                1.9343282303776128e-05,)),
        },
    },
    6: {"rows": 723, "months": (0, 180, 361, 541, 722),
        "result_cf": {
            "pols_if": (105.59274191106614, 1.0, (
                0.0, 0.05599587894051132, 0.00961504800996041, 0.0010762471490809084,
                1.9988090701711986e-05)),
            "premiums": (2933.563917599938, 140.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1777.4074173656406, 8.683890549777864, (
                0.0, 3.5170810445168987, 1.5250788333578011, 0.6367184053548686,
                0.047422578259039394)),
            "commissions": (197.7504899909903, 112.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (599.7573800532894, 302.512407328933, (
                0.0, 0.18840770135666277, 0.04361273269301639, 0.006570167369371906,
                0.00016449586593700227)),
            "premium_taxes": (58.67127835199876, 2.8000000000000003, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (299.97735183801893, 283.981519690157, (
                0.0, -3.7054887458735615, -1.5686915660508176, -0.6432885727242404,
                -0.0475870741249764)),
        },
        "result_pols": {
            "pols_if": (105.59274191106614, 1.0, (
                0.0, 0.05599587894051132, 0.00961504800996041, 0.0010762471490809084,
                1.9988090701711986e-05)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.01777407417365641, 8.683890549777864e-05, (
                0.0, 3.5170810445168987e-05, 1.525078833357801e-05, 6.367184053548686e-06,
                4.7422578259039396e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9822065825440406, 0.5198181893620692, (
                0.0, 0.0004891867392223722, 8.391769255544026e-05, 9.352474422493713e-06,
                1.7058261534546534e-07)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9343282303776128e-05)),
        },
    },
}
# END generated fingerprint: Term_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is Term's
# own: the comparison on the splice grid, at the contract's extremes and where the cap on
# mortality binds, the refusals, the deepest call, a Reference set late and the runner.

CONTRACT_MIN_AGE = 18   # the youngest issue age product-spec.md admits, issue_age_min


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)

# Conversion switched on, as the splice switches it on (SPLICED_REFS), at the shipped
# inflation: on the contract's longest frames the window runs thirty policy years.
CONVERSION_ON = {ref: value for ref, value in SPLICED_REFS.items()
                 if ref.startswith("conv_")}


def _contract_extremes(age=CONTRACT_MIN_AGE):
    """Inputs for the longest frames: a table and the edits of the tables it needs.

    Two points, S's point 2 issued at ``age`` on the ten- and the thirty-year plan,
    ``future_horizon_mth`` months after the valuation date: 12 * (95 - 18) + 120 = 1,044
    months at 18, the longest frame the contract allows (spec_sec.py).  The shipped tables
    stop short of such a policy, so the copies extend them: mortality down to ``age``,
    falling 3% a year below age 35's rate; the anchor cell's schedule on to the last
    policy year, rising 1% a year from year 60's premium; and a thirty-year schedule, its
    level premium for thirty years and then the ten-year plan's renewal premiums twenty
    years on.  The numbers mean nothing, but each key the copies add reads a value of its
    own, so that a read of the key beside the right one, which a padded array allows,
    changes a number the compiled comparison sees.  How deep a cold call runs follows from
    the frame alone.
    """
    years = 95 - age
    committed = _committed()
    rows = committed.loc[[2, 2]].assign(age_at_entry=age, duration_mth=-120,
                                        plan=["T10", "T30"])
    rows.index = pd.Index([1, 2], name="point_id")

    def mortality(m):
        first, rate = int(m["age"].min()), m["mort_rate"].iloc[0]
        low = pd.DataFrame({"age": range(age, first),
                            "mort_rate": [rate * 0.97 ** (first - a)
                                          for a in range(age, first)],
                            "provenance": "extended"})
        return pd.concat([low, m], ignore_index=True)

    def premiums(r):
        t10 = r[_anchor_rows(r)]
        end = int(t10["policy_year"].max())
        last = t10[t10["policy_year"] == end]
        more = [last.assign(policy_year=y,
                            premium_pp=last["premium_pp"] * 1.01 ** (y - end))
                for y in range(end + 1, years + 1)]
        level = t10[t10["policy_year"] <= 10]
        t30 = pd.concat([level.assign(policy_year=level["policy_year"] + k)
                         for k in (0, 10, 20)]
                        + [t10[t10["policy_year"] > 10].assign(
                            policy_year=t10[t10["policy_year"] > 10]["policy_year"] + 20)])
        return pd.concat([r, *more, t30.assign(plan="T30", provenance="extended")],
                         ignore_index=True)

    return rows, {"mort_table.csv": mortality, "premium_rates.csv": premiums}


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's points, S's restated in force at T2's months and issued
    later, and the variants, the quarterly, semi-annual and monthly cycles, a twenty-year
    plan, the conversion window's age limit, cover ending with the level period, and every
    sex, class and band, each joined to a premium schedule of its own, with conversion
    switched on (:data:`SPLICED_REFS`).  The grid's SEC table and premium table go beside
    the build, modelx sweeps every point fully, and the compiled model must agree at every
    argument modelx caches, identically on x86-64 and to 1e-12 relative elsewhere, with
    every raise and every ``Data`` array (``sec_support.compiled_mismatches``).  On
    x86-64 that is what holds ``cpow=True``: without it 240 of the grid's values differ
    in their last bits (M14).
    """
    build = sec_build(SEC)
    table = pd.read_csv(spliced[1].Data.input_dir() / TABLE, index_col="point_id")
    folder = compiled_case(build, tmp_path / "grid", model_points=table,
                           edits=SPLICED_EDITS)
    found = compiled_mismatches(build, folder, refs=SPLICED_REFS)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The two points of :func:`_contract_extremes`, issued at 18 on the ten- and the
    thirty-year plan 120 months after the valuation date, run 1,044 months, the longest
    frame the contract allows, and read every cache as far as ``spec_sec.py`` sizes it for:
    ``t`` to 1,044, the month after the frame, policy year 77 and, on the ten-year plan,
    PLT duration 68 in that month.  Conversion is on.  modelx sweeps both fully, and the
    compiled model must agree everywhere.  A cache one too small for the contract raises
    ``IndexError`` compiled where modelx reads on, and fails here, though the spec check
    passes it, which holds the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows, edits = _contract_extremes()
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows, edits=edits)
    found = compiled_mismatches(build, folder, refs=CONVERSION_ON)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1: compiled, every cell is modelx's.

    The twin of :data:`CAPPED`, whose annual rate passes 1 from policy year 21, and its two
    rows in force (:func:`_capped_in_force`) go beside the build with the splice's premium
    table.  modelx sweeps them fully, and the compiled model must agree at every argument
    modelx caches, identically on x86-64 and to 1e-12 relative elsewhere
    (``sec_support.compiled_mismatches``, which reads ``exact_here()``).  No other
    compiled test reaches the side of ``min(..., 1.0)`` that returns 1.  Uncapped, the
    compiled monthly rate there is NaN, silently, where modelx's is complex.
    """
    build = sec_build(SEC)
    twin = _capped_tables()[1]
    folder = compiled_case(build, tmp_path / "capped",
                           model_points=pd.concat([twin, _capped_in_force(twin, 1.0)]),
                           edits=SPLICED_EDITS)
    found = compiled_mismatches(build, folder)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The label accessors, which return the point's column as read (sample_sec.py).
LABELS = ("sex", "rate_class", "plan", "premium_mode")


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a table whose labels are blank, which pandas reads as NaN, or a
    number, on the first committed point.  modelx returns each label as
    pandas reads it, and an accessor typed ``str`` would raise ``TypeError`` compiled;
    the sample types the labels as Python objects from a blank copy (sample_sec.py, M26).
    So on a copy of that point with every label blank, and on one with every label the
    number 7, after checking that modelx returns NaN and 7, each label is called compiled
    and must return what modelx returns (``sec_support.label_mismatches``).
    """
    build = sec_build(SEC)
    first = _committed().iloc[[0]]
    found = []
    for case, value in (("blank", None), ("numeric", 7)):
        rows = first.assign(**{label: value for label in LABELS})
        folder = compiled_case(build, tmp_path / case, model_points=rows)
        want, lines = label_mismatches(build, folder, LABELS)
        (got,) = want.values()
        for label in LABELS:
            kind, read = got[label]
            assert kind == "ok", (case, label, got[label])
            assert (math.isnan(read) if value is None else read == value), (case, label,
                                                                             read)
        found += [f"{case}: {line}" for line in lines]
    assert not found, "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So ``proj_len()`` refuses a point past its cover,
    naming it by ``point_id()``, as M1's record asked a compiled test to show, on the
    committed table and on the extract whose labels are not its positions plus one
    (:func:`_extract`); and it refuses a level period below ten years, a five-year plan
    with a schedule of its own among them, and an issue age below 18, which the compiled
    caches are not sized for (:data:`NOT_ISSUED`).  The one reader of each padded table
    refuses an age below the mortality table and a policy year outside the schedule, at
    either end; a mode ``Data`` cannot decode is refused when another point first reads its
    premium; and a schedule whose policy year is text is refused by the schedule's message,
    which the extent read before the array gives too.  Every case of :data:`NOT_FINITE`, a
    value a cap, a ``min`` or a ``max`` reads that is blank, text or infinite, is refused
    by the first point's ``result_cf()``, on its own inputs, compiled as in modelx, so a
    compiled ``Data`` cell refuses each value its modelx cell refuses.

    And one refusal is the compiled model's alone: a call past the caches ``spec_sec.py``
    sizes, ``net_cf(1046)``, which modelx answers with a zero, the month being outside
    cover, raises ``IndexError`` compiled rather than reading or writing beyond them.
    """
    build = sec_build(SEC)
    extract = _extract()
    last = extract.index[extract["policy_id"] == "TL-000001-M719"][0]
    text_year = {"premium_rates.csv": _year_written(30, "30x")}
    cases = [
        ("past its cover", _set("duration_mth", [5], 720)(_committed()), None, 5,
         "proj_len", (), False),
        (f"past its cover, labelled {last}", _set("duration_mth", [last], 720)(extract),
         None, last, "proj_len", (), False),
        *((case, edit(_committed()), edits, point, "proj_len", (), False)
          for case, edit, edits, point, _, _ in NOT_ISSUED),
        ("below the mortality table", _set("age_at_entry", [2], 30)(_committed()), None, 2,
         "net_cf", (0,), False),
        ("beyond the schedule", _set("age_at_entry", [2], 30)(_committed()), None, 2,
         "premium_pp_ann_py", (61,), False),
        ("below the schedule", _committed(), None, 2, "premium_pp_ann_py", (0,), False),
        ("an unknown mode", _set("premium_mode", [4], "W")(_committed()), None, 1,
         "premiums", (0,), False),
        ("a policy year written as text", _committed(), text_year, 1, "premium_pp_ann_py",
         (11,), False),
        *((case, _committed() if edit is None else edit(_committed()), edits, 1,
           "result_cf", (), False) for case, edit, edits, _, _ in NOT_FINITE),
        ("a month past the caches", _committed(), None, 1, "net_cf", (1046,), True),
    ]
    found = []
    for i, (case, table, edits, label, cell, args, compiled_only) in enumerate(cases):
        dest = tmp_path / f"case{i}"
        folder = compiled_case(build, dest, model_points=table, edits=edits)
        model = mx.read_model(folder, name=_name("refused"))
        try:
            key = point_keys(model)[list(model.Data.model_point_table().index).index(label)]
            proj = projection(model, key)
            if compiled_only:
                assert proj.cells[cell](*args) == 0.0      # modelx answers outside cover
                want = ("raised", "IndexError")
            else:
                with pytest.raises(Exception) as excinfo:
                    proj.cells[cell](*args)
                want = ("raised", _raised(excinfo.value))
        finally:
            model.close()
        got = run_compiled(dest, build.package.name,
                           {"refs": {}, "calls": {key: [(cell, args)]}})
        assert got["exit"] == 0, f"{case}: the compiled run failed:\n{got['stderr']}"
        assert all(got["compiled"].values()), got["compiled"]
        status, text = got["values"][key][0]
        if status == "raised" and compiled_only:
            text = text.split(":")[0]           # the cache's own message, not modelx's
        if (status, text) != want:
            found.append(f"{case}: {cell}{args} compiled {status} {text!r}, modelx {want}")
    assert not found, "\n".join(found)


@pytest.mark.cython
def test_the_longest_frame_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the two longest frames of :func:`_contract_extremes`, 1,044 months, a cold
    ``net_cf`` in the last month runs the count chain from the end of the frame back to
    ``t_entry``, 932 cells deep in modelx on a model just read
    (:func:`test_the_deepest_cold_call_runs_one_cell_a_month`), and compiled it runs on
    the C stack, which the interpreter's recursion limit does not count.  1 MiB is the
    stack MSVC gives an executable's main thread unless the executable asks for more: a
    host that embeds Python, where python.exe itself asks for 2,000,000 bytes.  A thread
    whose stack is reserved at 1 MiB stands in for it on every platform
    (``sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12 elsewhere.
    With gcc the call needs between 232 and 240 KiB.  A stack too small kills the child,
    and the test fails naming the stack.

    The thread's stack is read back too, from Windows or from glibc, and must be at most
    1 MiB and a page: ``threading.stack_size`` sets only the stack a Windows thread
    commits, not the one it reserves, which is why the child makes the thread itself
    there, and a stand-in larger than asked for would stand for nothing.  And the calls
    run again on the child's main thread, which is what ``run_sec.py --cython`` runs on.
    """
    build = sec_build(SEC)
    rows, edits = _contract_extremes()
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows, edits=edits)
    model = mx.read_model(folder, name=_name("extremes"))
    try:
        calls, want = {}, {}
        for key in point_keys(model):
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert last == 12 * (95 - CONTRACT_MIN_AGE) + 120 - 1
            calls[key] = [("net_cf", (last,))]
            want[key] = proj.net_cf(last)
    finally:
        model.close()
    job = {"refs": {}, "calls": calls}
    for where, kwargs in (("a 1 MiB thread", {"stack_kib": 1024}),
                          ("the main thread", {"main_thread": True})):
        got = run_compiled(tmp_path / "extremes", build.package.name, job, **kwargs)
        assert got["exit"] == 0, (
            f"the compiled model's deepest cold call failed on {where}, exit code "
            f"{got['exit']}:\n{got['stderr']}")
        assert all(got["compiled"].values()), got["compiled"]
        for key, value in want.items():
            assert got["values"][key][0][0] == "ok", (where, got["values"][key])
            have = got["values"][key][0][1]
            assert _as_modelx(have, value), (where, have, value)
        reserved = got["stack"]["reserved"]
        if where == "a 1 MiB thread" and reserved is not None:
            assert reserved <= (1 << 20) + 4096, (
                f"the thread has {reserved} bytes of stack, not 1 MiB")


# A compiled model's Reference set after it has computed, in a child of its own: what the
# base Projection, an ItemSpace made before the change and one made after give for
# expenses(12), before inflation_rate is set to 0 and after.
STALE_CHILD = """\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[3]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
values += [p.expenses(12), early.expenses(12), p[1].expenses(12)]
print(json.dumps(values))
"""


@pytest.mark.cython
def test_a_compiled_model_clears_no_cache_when_a_reference_is_set(sec_build, tmp_path):
    """Compiled, a Reference set after a Space has computed leaves its values as they were.

    modelx recomputes what a Reference reaches when it is set.  The compiled model clears
    no cache: the base ``Projection``, and an ItemSpace made before the Reference was set,
    keep the values they computed, and only an ItemSpace made afterwards, which takes the
    References when it is made, computes with the new value.  The Projection docstring
    and ``model-sec.md`` say so, and tell a user to set every Reference on a model just
    imported.  This holds the compiled model to what they say, on ``inflation_rate``,
    which moves ``expenses(12)`` on every point in force then, so that a modelx-cython
    that began to clear caches would be seen here, and the advice changed with it.  A
    compiled value meets modelx's as C4 holds it (:func:`_as_modelx`), and one the
    compiled model kept, its own value of before, identically.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "stale")
    child = tmp_path / "stale_child.py"
    child.write_text(STALE_CHILD, encoding="utf-8")
    done = subprocess.run([sys.executable, "-P", str(child), str(folder.parent),
                           build.package.name], capture_output=True, text=True,
                          timeout=300)
    assert done.returncode == 0, done.stderr
    base, early, base_after, early_after, late = json.loads(done.stdout.splitlines()[-1])
    model = mx.read_model(folder, name=_name("stale"))
    try:
        p = model.Projection
        before = (p.expenses(12), p[3].expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), p[3].expenses(12), p[1].expenses(12))
    finally:
        model.close()
    assert _as_modelx(base, before[0]) and _as_modelx(early, before[1]), (base, early,
                                                                          before)
    assert fresh[0] != base and fresh[1] != early
    assert (base_after, early_after) == (base, early), "the compiled model cleared a cache"
    assert _as_modelx(late, fresh[2]), (late, fresh[2])


@pytest.mark.cython
def test_run_sec_prints_the_compiled_model_as_it_prints_modelx(sec_build, tmp_path):
    """``run_sec.py --cython`` prints, for a point and for the block, what modelx prints.

    Each run in an interpreter of its own, as a user runs it.  With ``--build`` it runs the
    session's build, so nothing is built in the tree, and it checks for itself that the
    package it imported is compiled.  Line for line, the compiled model's output is
    modelx's: point 4's description and its first twelve rows and counts, and the block's
    first twelve rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("4",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "4", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
