"""In-force tests for RILA_US_SEC: the splice, future business, counts, regeneration.

``RILA_US_SEC`` is ``RILA_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M10).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months from issue, ``duration_mth_init() + t``.  A model point may be a contract already in
force at the valuation date, in any month of any term, one issued at it, or one issued up
to ten years after it, as in ``basiclife/BasicTerm_SE``.  A contract in force opens with
thirteen columns of state beside its count: seven amounts per contract entering month 0,
the Investment Amount, the Fixed and Holding Accounts, the Account Value, of either sign,
the Account Value before withdrawals at the anniversary on or before the valuation date,
the Free Withdrawal Amount still unused and the return-of-premium base; and, where the term
under way began before the valuation month, the index level, the Market Value Rate and the
option-pricing market of its Term Start Date, with the cap re-solved there at a renewal
under ``nge_reset``.  The market runs on the valuation clock, each row restated in force or
issued later reading its own copy of its scenario re-based to its month,
``market_scenario_sec.csv``; the terms, the anniversaries, the withdrawal programme and the
Maturity Date stay on the policy clock.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``RILA_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's fifteen points (T1), so every golden of
``test_registered_index_linked_annuity_us.py`` on a cell S's sweep reaches holds on this
model with no number copied: the worked example's table, the option budget and its
decomposition, the withdrawal-charge example and the term-end identity.  The conventions
also hold the SEC family's other rules: every frame opens at ``t = 0``, ``pols_if`` is the
``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business
enters once, and nothing happens before issue.  This module holds the rest of the plan's
tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months straddle each term end and renewal, 35, 36, 59, 60, 71 and
  72, a month mid-term, the anniversaries 12 and 24 and a year's last month, on stepped
  copies of the market paths, every field of which steps, each row valued mid-term on a
  copy whose state at ``t = 0`` is moved off its term-start columns, and ten variants of
  S's points, in a copy of S's table, reach what S's own points cannot: a three-year
  term, a one-year term under ``nge_reset``, a behavioural rate above the free rate, a
  Floor option whose cap binds, a crash path that takes the interim value below 0, a
  withdrawal above the account value, on the crash path a behavioural rate above the free
  rate and a positive request on a negative account value, an Edge term ending exactly at
  its buffer, and a withdrawal at a negative interim value on a positive account value,
  which the accounts alone pay.
* T3, future new business: a contract issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before it, no rate evaluated there, and its own
  scenario, which holds no level before its issue month.
* D11's R1, R1a and R2, and D3's clock: on the splice's grid no cell is called at a
  negative argument, nor a keyed table read at a key the contract does not have, none
  evaluated on the books reads a month before them, and none reads beyond ``t + 1``; on
  the committed points no recursion runs backward over the frame, a cold call runs one
  cell a month, and the policy clock is a closed form.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, multiplying
  ``policy_count`` by 2.5, with every assumption that ships at zero switched on,
  multiplies every flow and moves no per-contract value, and the checks' tolerances scale
  with the count.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, and again through a projection; each malformed assumption table, a key or a
  value, by the count cell beside its reader, naming the file's lines; a point at or past
  its maturity, or carrying more free withdrawal than its year allows, is refused by
  ``proj_len()``; a value no decode knows is refused where the projection meets it; the
  future horizon is a Reference that bounds future business; and every state S reaches,
  on the splice's inputs and on its shipped ones, the edges of the interface, and keys
  written as floats, are accepted.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and
  ``market_scenario_sec.csv`` are what the generator makes of ``RILA_US_S`` and its inputs
  as they stand, and each derived and future row in them is its S point from its month
  on, frame by frame and cell by cell.
* Then the product's own facts: the two clocks, the opening state as S carries it, each
  column shown on a committed row, a term begun before the valuation date, the cap
  re-solved at a renewal, a renewal at the valuation date, the year's free-withdrawal
  state, withdrawals on the policy clock, the scenario and expense inflation on the
  valuation clock, the capped mortality rate, the checks failing a residual that is not a
  number, the premium and acquisition on new business, the values outside cover, the
  set-apart inputs, the block, an in-force extract, the runner, the docstrings and their
  tables, the shared input tables, and what the default grid reaches.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).
* Stage EC, what compiling changed, held in modelx: the spec's sizes and the sample's
  recursion limit and label trace held to their derivations; S's totals and their sign of
  zero, a withdrawal over three buckets summed as S's ``sum``, the leg codes and the
  inlined Black-Scholes engine, each bit for bit; the cap solved once a term; every
  parameterless cell a Python number and every ``Data`` vector the dtype its docstring
  states, padded with NaN; the decodes and the numberings; the powers taken off their
  domain beside S's outcome, the issue ages and attained ages the caches cannot hold, and
  a whole number of ``2**53`` or more, each refused by its point; and the runner's build,
  its extension check and its block sum.
* Compiled (``cython``): the compiled model computes what modelx computes on the splice
  grid, at the contract's extremes, under moved References, a NaN through each among them,
  on labels that are not text, on keys written as floats and out of order and on keys far
  past every frame, at every power off its domain and in the total's sign of zero; it
  refuses what modelx refuses and, alone, past its caches; the deepest cold call runs on
  a 1 MiB stack and on the main thread; a Reference set late clears no cache; and the
  runner prints what modelx prints.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, ``-k``
for one issued ``k`` months on.  ``RILA_US_S`` has no point in force, so every twin is new
business, compared by T1, and every splice case is a derived row.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  T2 and T3 over every month the
product's events need, 101 splices and 16 future points, would take this module well past
three minutes in every run.  By default they run a core of 37 and 6, chosen so that
between them they reach every crediting method, interim-value family, amortization rule,
scenario and programme, ``nge_reset`` both ways, every opening-state column, every kind of
valuation month and every property ``test_the_core_grid_reaches_every_branch`` lists,
which between them run every line the full grid runs (measured at M10).  The other cases,
and the rules test's scan of their rows, carry the ``sec_full`` marker and are skipped,
with the reason shown, unless ``USLIB_SEC_FULL=1`` is set.  They are never dropped: one
leg of the CI matrix sets it, and ``USLIB_SEC_FULL=1 python -m pytest -m sec_full`` on
this module runs them alone.  Memory is the other cost.  A projected point holds its
cached values and their dependency graph, so a row read once, a splice case's or a point
of a temporary copy, is released as soon as it has been read (``_release``), and the
splice's rows are held one at a time, however large the grid.  The models the module
sweeps once and holds are frozen out of the collector (``gc.freeze``), so that a
collection scans only what a test has made since, and the freeze is undone as the module
ends (:func:`_freeze`).

Every test keeps four rules.  Each model is read under a name of its own and closed:
``test_registered_index_linked_annuity_us.py`` reads S under its default name, and reading
a model under a name in use renames the open one.  No test writes inside the library tree:
every changed input goes through ``sec_support.temp_inputs`` into a temporary directory,
because a CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  And every Reference a test changes, ``Data``'s included, is
set on a model just read, before it computes anything, because a compiled model never
clears a cache; timings, kinds and buckets pass through :func:`_code`, and every twin
comparison through :func:`_mismatches`, so that the same calls serve Phase 2's int codes
(C1).
"""
import ast
import dataclasses
import errno
import gc
import importlib.machinery
import inspect
import io
import itertools
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys
import types
import unicodedata
import warnings

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, compiled_case, compiled_mismatches, exact_here, fingerprint_mismatches,
    frame_mismatches, run_compiled, shift_months, sweep, temp_inputs, twin_mismatches)
from released_twins import read_released_twin, sec_test_model_path as model_path
from us_registry import meta, point_keys, projection

SEC, TWIN = "RILA_US_SEC", "RILA_US_S"
TABLE, SCENARIOS = "model_point_table_sec.csv", "market_scenario_sec.csv"
SPEC = SEC_SPECS[SEC]
NAN = float("nan")

# S's fifteen points, all issued at t = 0: the worked example's two anchor cells, the
# behavioural withdrawal rule, the four crediting methods on one-year terms, the four
# interim-value families, both amortization rules, participation above 1, the uncapped
# option, nge_reset, the charged withdrawal and the prospectus's withdrawal-charge example.
S_POINTS = tuple(range(1, 16))

# Ten more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed in its columns alone, never a formula, so as to reach what
# S's own points cannot.  Each is (the S point it changes, the columns it changes); the
# policy_id keeps the generated ids apart.
#
# 16, the anchor on a three-year term, the guarantee table's middle row, at a cap of 55%
#   that binds in neither of its first two terms;
# 17, nge_reset on a one-year term, which re-solves its cap every year, so that a renewal
#   falls inside every restated frame and one falls before each valuation month;
# 18, the behavioural rule at 15% of the account value, above the free rate, so that the
#   Free Withdrawal Amount binds it at every anniversary;
# 19, the Floor option on a three-year term at a cap of 8%, which binds at its first Term
#   End Date on the up path;
# 20, the behavioural rule on the crash path, whose index falls 85% at month 20, so that
#   the interim value is below 0 from month 19 and the account value entering months 21
#   and 22 too: RILA_US_S's value <= 0 branches;
# 21, the charged programme's contract withdrawing 250,000 at policy month end 30, above
#   its account value, which the clamp takes to the whole value and which leaves nothing
#   held;
# 22, the crash path at a behavioural rate of 15%: on a negative base the allowance is
#   negative, and the remainder it leaves is bounded by no allowance (proj_len()'s rule);
# 23, the crash path with a programme withdrawing 5,000 at policy month end 22, a positive
#   request on a negative account value, which the clamp pays at 0;
# 24, the Edge option at a buffer of 25% on the edge path, whose index falls from 100 to 75
#   at month end 24, so that its second term ends exactly at the buffer, -25% to the last
#   bit, where the Edge rate is credited and a loss below it would not be: each crediting
#   method's boundary met exactly, as point 4's Step terms meet theirs on flat years;
# 25, the anchor on a three-year term at a cap of 55% on the dip path, which falls 75% at
#   month end 40, with a programme withdrawing 5,000 at policy month end 42: the interim
#   value is below 0 there and the account value above it, held up by the accounts the
#   first term end fed, so the withdrawal comes from the accounts alone, the option's
#   share of it floored at 0, where an unfloored share would be negative.
VARIANTS = {
    16: (1, {"policy_id": "RILA-900016", "term_years": 3, "declared_cap": 0.55}),
    17: (13, {"policy_id": "RILA-900017", "term_years": 1, "declared_cap": 0.12}),
    18: (3, {"policy_id": "RILA-900018", "wd_rate_ann": 0.15}),
    19: (6, {"policy_id": "RILA-900019", "term_years": 3, "declared_cap": 0.08,
             "scenario_id": "up"}),
    20: (3, {"policy_id": "RILA-900020", "scenario_id": "crash"}),
    21: (14, {"policy_id": "RILA-900021", "wd_schedule_id": "big"}),
    22: (3, {"policy_id": "RILA-900022", "scenario_id": "crash", "wd_rate_ann": 0.15}),
    23: (3, {"policy_id": "RILA-900023", "scenario_id": "crash",
             "wd_schedule_id": "small"}),
    24: (5, {"policy_id": "RILA-900024", "buffer": 0.25, "scenario_id": "edge"}),
    25: (1, {"policy_id": "RILA-900025", "term_years": 3, "declared_cap": 0.55,
             "scenario_id": "dip", "wd_schedule_id": "dip"}),
}

# T2's months, by S point or variant, each chosen on the splice's edited inputs: either
# side of each Term End Date, a renewal at the valuation month and the month before it
# (35 and 36 on a three-year term, 71 and 72 on a six-year one, 11 and 12, 23 and 24 on a
# one-year one), the term midpoints and a month mid-term (5, 30, 40, 59), the anniversaries
# 12 and 24 with the base read from the opening state and 11 with it read from the frame,
# the month before the charge-free year's first term end (59), the months around each
# programme's withdrawal (23, 29, 21 for 22's, 40 and 41 for 42's), a month mid-term after
# a renewal under nge_reset (80) and the last covered months (119, 359).
SPLICE_MTHS = {
    1: (5, 11, 12, 24, 35, 36, 40, 59, 60, 71, 72, 359), 2: (35, 36, 71, 72),
    3: (11, 12, 23, 24, 30, 60), 4: (11, 12, 30, 35, 36), 5: (35, 36, 59, 60),
    6: (35, 36, 71, 72), 7: (35, 71, 72, 107, 119), 8: (35, 71, 72), 9: (5, 11, 12, 60),
    10: (35, 40, 71, 72), 11: (35, 71, 72), 12: (35, 40, 71, 72), 13: (71, 72, 80, 119),
    14: (23, 24, 36), 15: (59, 60, 71, 72), 16: (35, 36, 40, 71, 72),
    17: (11, 12, 30, 35, 36), 18: (11, 23, 24), 19: (12, 30, 35, 36),
    20: (12, 21, 22, 24, 30), 21: (23, 29), 22: (24, 30), 23: (12, 21), 24: (12, 23),
    25: (40, 41)}

# T2's cases, as (row_kind, S point, source_mth), and T3's, as (S point, k).  RILA_US_S has
# no point in force, so there is no twin to splice (§5.2's IN_FORCE_TWINS).  The future
# offset is 13, more than a year, so that a read before issue lands at policy year -1 or
# lower; 1 puts the anniversaries a month off the valuation years, and 120 is the horizon.
SPLICES = tuple(("derived", p, d) for p, ds in SPLICE_MTHS.items() for d in ds)
IN_FORCE_TWINS = ()
FUTURES = ((1, 1), *((p, 13) for p in (1, 2, 4, 5, 9, 13, 15, 16, 17, 19, 20, 21, 22,
                                       23)), (1, 120))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("derived", 1, 11): "a year's last month: its anniversary and base at t = 0",
    ("derived", 1, 12): "an anniversary valuation: the year's base from the opening state",
    ("derived", 1, 40): "mid-term and mid-year: the term start and the base from the point",
    ("derived", 1, 71): "the first term's last month: the term end at t = 0, under the cap",
    ("derived", 1, 72): "a renewal at the valuation month: the new term from the scenario",
    ("derived", 1, 359): "the last covered month: the maturity at t = 0",
    ("derived", 2, 36): "after the midpoint withdrawal, on an anniversary",
    ("derived", 2, 71): "the down path's term end at t = 0: the buffer's loss credited",
    ("derived", 3, 11): "the behavioural rule's first withdrawal at t = 0",
    ("derived", 3, 30): "mid-year after a behavioural withdrawal: part of the year used",
    ("derived", 4, 12): "a one-year Step term renewing at the valuation month",
    ("derived", 4, 30): "a one-year term mid-term, both accounts fed by two term ends",
    ("derived", 5, 36): "the Edge option renewing at the valuation month",
    ("derived", 6, 35): "the Floor option's term end at t = 0, on the down path",
    ("derived", 7, 71): "the notional family's term end: the shock year below the bound",
    ("derived", 7, 119): "the notional family's last covered month",
    ("derived", 8, 72): "the delta family renewing at the valuation month",
    ("derived", 9, 5): "the legacy family mid-term, the source example's month",
    ("derived", 9, 12): "the legacy family renewing, its cap floored at the minimum",
    ("derived", 10, 40): "updated-expiry amortization from the opening state's market",
    ("derived", 11, 35): "participation above 1 at the term midpoint",
    ("derived", 12, 40): "the uncapped option mid-term, past the return-of-premium band",
    ("derived", 13, 72): "a renewal under nge_reset at the valuation month, solved at 0",
    ("derived", 13, 80): "after a renewal under nge_reset: the cap from the opening state",
    ("derived", 13, 119): "nge_reset's last covered month",
    ("derived", 14, 23): "the excess withdrawal at t = 0, charged",
    ("derived", 15, 59): "the legacy family before the charge-free year's first term end",
    ("derived", 16, 40): "a three-year term in its second term",
    ("derived", 17, 30): "nge_reset on a one-year term: the column, a re-solve at t = 6",
    ("derived", 18, 23): "the behavioural rule at the allowance at t = 0",
    ("derived", 19, 12): "the Floor option's cap binding at its first term end, t = 23",
    ("derived", 20, 21): "the crash path: a negative account value entering the month",
    ("derived", 21, 23): "a withdrawal above the account value at t = 6, nothing after",
    ("derived", 22, 24): "a negative base on an anniversary valuation",
    ("derived", 23, 21): "a positive request on a negative account value at t = 0, paid 0",
    ("derived", 24, 23): "the Edge term end at t = 0 exactly at the buffer, from the point",
    ("derived", 25, 41): "the withdrawal at t = 0 from the accounts, the option below 0",
}
CORE_FUTURES = {
    (1, 13): "issued more than a year on: policy year -1 before issue",
    (4, 13): "a one-year Step term from its own issue",
    (9, 13): "the legacy family from its own issue",
    (13, 13): "nge_reset from its own issue: each renewal re-solved in the frame",
    (20, 13): "the crash path from its own issue",
    (1, 120): "issued at the horizon",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# The splice's market paths, each a step function of the month end from issue, in S's
# columns: (month_end, index_level, mvr, risk_free, div_yield, impl_vol).  Every field
# steps, at levels of its own, within every term and across every term start, so that a
# term-start value read from the current market, or the current market read at the term
# start, reads another number: on S's shipped paths the risk-free rate, the dividend yield
# and the volatility are flat, and a term-start volatility read at t = 0 passes every
# comparison.  "crash" falls 85% at month 20, with the Market Value Rate at 35%, which
# takes the interim value below 0; "edge" falls from 100 to 75 at month 24, a ratio that
# binary floating point holds exactly; and "dip" rises to 120 at month 36, a three-year
# term's renewal, and falls 75% at month 40, with the Market Value Rate at 35%, taking the
# renewed term's interim value below 0 while the accounts its first term end fed keep the
# account value above it.
STEPPED = {
    "up": [(0, 100.0, .040, .040, .020, .200), (5, 103.5, .042, .041, .021, .210),
           (13, 107.2, .045, .043, .019, .190), (20, 111.9, .047, .044, .022, .220),
           (30, 115.4, .048, .042, .020, .180), (37, 121.3, .050, .045, .021, .205),
           (47, 118.6, .052, .046, .023, .230), (55, 124.9, .049, .043, .020, .215),
           (61, 129.7, .051, .044, .018, .195), (66, 133.2, .053, .047, .019, .185),
           (73, 141.6, .051, .047, .018, .190), (80, 138.4, .055, .049, .021, .225),
           (90, 145.1, .054, .048, .022, .200), (100, 152.3, .050, .044, .020, .210),
           (125, 160.8, .047, .042, .019, .195), (150, 171.2, .045, .041, .021, .205),
           (200, 183.9, .043, .040, .020, .200), (260, 196.5, .046, .042, .022, .210)],
    "down": [(0, 100.0, .040, .040, .020, .200), (5, 97.1, .043, .041, .021, .215),
             (13, 93.6, .046, .042, .019, .230), (20, 88.2, .048, .044, .022, .245),
             (30, 84.9, .050, .046, .021, .250), (37, 79.8, .052, .047, .023, .260),
             (47, 76.3, .054, .045, .020, .240), (55, 72.4, .056, .048, .024, .255),
             (61, 70.1, .053, .046, .022, .235), (66, 68.8, .055, .049, .021, .245),
             (73, 74.6, .051, .047, .020, .225), (80, 71.9, .054, .048, .023, .240),
             (90, 66.5, .057, .050, .024, .260), (100, 63.2, .055, .049, .022, .250),
             (125, 61.7, .052, .046, .021, .235), (150, 64.4, .050, .045, .020, .225)],
    "legacy": [(0, 500.0, .030, .040, .020, .200), (3, 520.0, .032, .041, .021, .210),
               (6, 600.0, .034, .042, .019, .190), (13, 585.0, .031, .043, .022, .205),
               (25, 640.0, .033, .044, .020, .215), (37, 610.0, .035, .045, .021, .195),
               (61, 655.0, .036, .046, .023, .220), (85, 700.0, .034, .044, .020, .205)],
    "charge_ex": [(0, 100.0, .040, .040, .020, .200), (13, 92.0, .042, .041, .021, .210),
                  (37, 85.0, .044, .043, .022, .220),
                  (60, 71.66666667, .045, .042, .020, .215),
                  (73, 76.0, .046, .044, .021, .205), (100, 82.0, .043, .041, .019, .195)],
    "crash": [(0, 100.0, .040, .040, .020, .200), (13, 104.0, .042, .041, .021, .210),
              (20, 15.0, .350, .044, .022, .450), (30, 22.0, .300, .046, .021, .400)],
    "edge": [(0, 100.0, .040, .040, .020, .200), (5, 100.0, .042, .042, .021, .210),
             (13, 100.0, .044, .043, .019, .220), (24, 75.0, .047, .045, .022, .240),
             (37, 81.0, .046, .044, .021, .230), (61, 90.0, .045, .043, .020, .215)],
    "dip": [(0, 100.0, .040, .040, .020, .200), (5, 102.5, .041, .041, .021, .205),
            (13, 106.0, .043, .042, .019, .195), (20, 110.5, .044, .043, .022, .210),
            (30, 114.0, .042, .044, .021, .190), (36, 120.0, .045, .045, .020, .215),
            (40, 30.0, .350, .044, .022, .450), (44, 33.0, .330, .046, .023, .420),
            (55, 40.0, .300, .045, .021, .380), (66, 48.0, .250, .047, .024, .350),
            (73, 55.0, .200, .046, .022, .320), (90, 62.0, .150, .045, .021, .300),
            (110, 70.0, .100, .044, .020, .280), (150, 80.0, .080, .043, .019, .250)],
}


def _stepped(_):
    """The splice's paths (:data:`STEPPED`), in place of S's shipped scenarios."""
    rows = [(sid, m, i, r, rf, q, v, "stepped for a test")
            for sid, path in STEPPED.items() for m, i, r, rf, q, v in path]
    return pd.DataFrame(rows, columns=["scenario_id", "month_end", "index_level", "mvr",
                                       "risk_free", "div_yield", "impl_vol", "provenance"])


def _lapse_apart(df):
    """Contract year 1's base surrender rate set apart from year 7's, at 1.5%.

    Both ship at 2%, so a step lookup that read year 1 for the shock year, or the reverse,
    would read the same number, and no comparison with S could see it.  Year 1's rate is
    the one moved, because the shock year's feeds the bound on the surrender rate, and a
    rate set apart moves no comparison (test_the_set_apart_edits_move_no_branch).
    """
    return df.assign(lapse_rate_base=df["lapse_rate_base"].where(
        df["contract_year"] != 1, 0.015))


def _charges_apart(df):
    """Contract year 0's withdrawal charge set apart from year 1's, which ships equal."""
    return df.assign(surr_charge_rate=df["surr_charge_rate"].where(
        df["contract_year"] != 0, 0.075))


def _floors_binding(df):
    """The guaranteed minimum rates set so that each binds with an effect.

    The Edge floors are moved off the Step floors they ship equal to, and on the one-year
    term the Cap, Step and Edge floors are raised above S point 9's declared cap of 10%,
    point 4's step of 8% and point 5's edge of 6%: at the shipped 2% no floor binds on any
    point, and a floor read for the wrong term, or not at all, would pass.
    """
    df = df.assign(guar_min_edge=df["guar_min_edge"] + 0.005)
    one = df["term_years"] == 1
    return df.assign(guar_min_cap=df["guar_min_cap"].where(~one, 0.11),
                     guar_min_step=df["guar_min_step"].where(~one, 0.085),
                     guar_min_edge=df["guar_min_edge"].where(~one, 0.065))


def _programmes_added(df):
    """Three programmes the variants run: 250,000 at month end 30, 5,000 at month end 22
    and 5,000 at month end 42."""
    rows = pd.DataFrame([("big", 30, 250000.0, "a withdrawal above the account value"),
                         ("small", 22, 5000.0, "a request on the crash path"),
                         ("dip", 42, 5000.0, "a withdrawal at a negative interim value")],
                        columns=df.columns)
    return pd.concat([df, rows], ignore_index=True)


# The input files the splice's copies change, S's and SEC's alike; SEC's re-based scenarios
# are then built from S's edited ones by the spec's companion.
SPLICED_EDITS = {"market_scenario.csv": _stepped, "lapse_table.csv": _lapse_apart,
                 "surr_charge_table.csv": _charges_apart,
                 "guar_min_rate_table.csv": _floors_binding,
                 "withdrawal_table.csv": _programmes_added}

# What the splice sets in both models, S and SEC alike, before either computes anything.
# Expense inflation is the one input RILA reads on the valuation clock beside the market
# (D7): S inflates by policy year and SEC by valuation year, so at the shipped 2.5% the
# expenses of a point opened at d differ by design, and at 0 both factors are 1; the clock
# itself is asserted on its own, at the shipped rate.  The rest ship at a value that hides
# some of the state from any comparison:
#   roll_transfer_holding ships at 0, the Holding Account's share of a term end, and is
#     switched on at 4%, with the Fixed Account's 15% moved to 11%, so that the four shares
#     still sum to 1 and no two are equal: a swap of two shares reads another number;
#   premium_tax_rate ships at 0 and is switched on at 2%;
#   mort_ae_factor ships at 1, which hides a dropped factor;
#   lapse_shock_mult 27.5 takes the shock year's rate to lapse_rate_max in the months whose
#     moneyness factor is about 0.91 or more and not in the others, where the shipped 3
#     binds it nowhere and 30 everywhere it reaches, either of which hides a multiplier
#     read in the wrong year or a factor dropped;
#   iv_moneyness_floor 0.9 binds on the down paths, where the shipped 0.25 binds nowhere;
#   trading_cost_rate and iv_expense_rate ship equal, at 0.1%, and iv_credit_spread at
#     1%, the account rate's floor, and term_end_lapse_free at 10%, free_wd_rate: each is
#     set apart from the other;
#   declared_acct_rate 0.5%, below the 1% guaranteed minimum, so that the floor on the
#     account rate binds.
# The identity does not depend on the values, only on the two models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "roll_transfer_fixed": 0.11,
                "roll_transfer_holding": 0.04, "premium_tax_rate": 0.02,
                "mort_ae_factor": 1.05, "lapse_shock_mult": 27.5, "iv_moneyness_floor": 0.9,
                "trading_cost_rate": 0.0015, "iv_expense_rate": 0.0008,
                "iv_credit_spread": 0.012, "term_end_lapse_free": 0.12,
                "declared_acct_rate": 0.005}

# The assumptions that ship at zero, switched on as the splice switches them, for T4.
SWITCHED_ON = {"premium_tax_rate": 0.02, "roll_transfer_fixed": 0.11,
               "roll_transfer_holding": 0.04}

# The opening state, in Data's order, and the cells running in force adds to RILA_US_S's,
# each of which the symbol map must name.
STATE = ("inv_amt_pp_init", "fixed_acct_pp_init", "holding_acct_pp_init", "av_pp_init",
         "av_pp_prev_anniv_init", "free_wd_remain_init", "rop_pp_init",
         "index_at_term_start_init", "mvr_at_term_start_init",
         "risk_free_at_term_start_init", "div_yield_at_term_start_init",
         "impl_vol_at_term_start_init", "cap_rate_init")
AMOUNTS, FIXINGS = STATE[:7], STATE[7:]
DECODES = ("is_cap_crediting", "is_step_crediting", "is_edge_crediting",
           "is_floor_crediting", "is_iv_portfolio", "is_iv_notional", "is_iv_delta",
           "is_iv_legacy", "is_straight_line", "is_updated_expiry")
NEW_CELLS = ("policy_count", "duration_mth_init", "maturity_mth", "t_entry", "is_active",
             "pols_new_biz", *STATE, "risk_free_at_term_start", "div_yield_at_term_start",
             "impl_vol_at_term_start", "mort_rate_base_at", "surr_charge_rate_at",
             "lapse_rate_base_py", "wd_amount_pm", *DECODES)

# The cells compiling adds at stage "EC" (USLIB-SEC-PLAN.md section 6.1): the point's label
# and its three join numbers into Data's arrays (R4, R11); the leg count and the leg codes
# that replace RILA_US_S's opt_legs() (R10), which T1 exempts; and the int-keyed forms of
# S's float engine the projection prices through (R14).
COMPILED_CELLS = ("point_id", "scenario_number", "wd_schedule_number", "mort_schedule",
                  "opt_leg_count", "opt_leg", "opt_component_at", "opt_portfolio_at",
                  "opt_portfolio_abs_at", "credit_rate_by", "cap_solved_at_start")

# The three roll-forward residuals.  Each is 0 exactly or rounding around it, up to about
# 3e-11, and an opening state the CSV gives back an ulp off moves one by an ulp of what it
# closes, so T2 and T3 compare them at the default absolute floor of 1e-9, in a pass of
# their own, and every other cell with no floor (§5.2).
RESIDUALS = frozenset({"check_av_roll_fwd_resid", "check_pols_roll_fwd_resid",
                       "check_term_end_identity_resid"})
CHECKS = ("check_av_roll_fwd", "check_pols_roll_fwd", "check_term_end_identity")

# The cells T2 and T3 skip beyond T1's, which already drop result_pols (the spec's
# exempt).  proj_len counts from the valuation date on SEC and from issue on S, so it
# differs by d, or by -k, by design; frame_mismatches asserts what it must get right, that
# both frames end at the same instant.  scenario_id names a row's own re-based copy of its
# S scenario, so it differs by design; every cell the scenario drives is compared,
# market_state among them, at S's keys moved onto the valuation clock.
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len", "scenario_id"}
FUTURE_EXEMPT = SPLICE_EXEMPT

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed rows, at the shipped 2.5%, the only places a row in force departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "result_cf"})

# The decrement rates keyed by month, none of which may be evaluated before issue (R1, D4),
# and the table readers keyed by an attained age, a contract year or a policy month.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "lapse_rate_base", "lapse_rate",
                   "lapse_rate_mth", "term_end_lapse_rate")
KEYED_READERS = ("mort_rate_base_at", "surr_charge_rate_at", "lapse_rate_base_py",
                 "wd_amount_pm")

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# rate, a market value, a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz", "pols_death",
    "pols_lapse_term", "pols_lapse", "pols_maturity", "pols_decr", "premiums",
    "prem_to_av", "withdrawals", "claims", "claims_from_av", "claims_over_av", "expenses",
    "premium_taxes", "net_cf", "av_at", "inv_income", "wd_from_av", "av_change",
    "check_av_roll_fwd_resid", "check_pols_roll_fwd_resid", "result_cf", "result_pols"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths and surrenders, the term-end part of them, the forced annuitizations at the
# Maturity Date, and the notes' end-of-month l(t + 1), as RILA_US_S reports it.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_lapse_term",
               "pols_maturity", "pols_if_aft_decr"]

# The count's five timings, BEF_NB the one running in force adds; the Account Value's and
# the other balances' timings; the three benefit kinds, the three buckets, the option legs
# and the two markets.  Each label is passed through _code.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "BEF_TERM_SURR", "AFT_DECR")
KINDS = ("DEATH", "LAPSE", "MATURITY")
BUCKETS = ("OPTION", "FIXED", "HOLDING")
LEGS = ("ATM_CALL", "OTM_CALL", "OTM_PUT", "ATM_PUT", "FLOOR_PUT", "STEP_BINARY",
        "EDGE_BINARY")
MARKETS = ("CURRENT", "TERM_START")
BASES = ("CURRENT", "TERM_START", "UPDATED_EXPIRY")
RULES = ("TERM_END", "PRORATED")
REPORTS = ("result_cf", "result_pols", "result_av", "result_iv")

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached; the deepest stack of the
# ascending sweep is the option pricing of a term's first month, under the count's
# surrender rate, and runs 14 to 19 deep on fresh reads of the committed points, 19 on the
# reset point's twin and on its row valued at its renewal (13 at 72), where the leg at the
# cap re-solves the cap under nge_reset.  RILA_US_S's own sweep runs as deep on each of its
# points as this model's on its twin, 14 to 18, but for points 4, 5, 12 and 13, one level
# less: their deepest stack runs under the count, where this model's pols_if reads
# "BEF_DECR" and it "BEF_NB" (D5), so the depth is S's order of evaluation, not a
# recursion.  A backward recursion over the frame, through t + 1, needs a limit of hundreds.
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry (D5).  Every chain is one cell a month: the count, the Investment Amount, the
# Fixed and Holding Accounts, the return-of-premium base and the free-withdrawal carry,
# where RILA_US_S's run two and three; a cold net_cf in the last month runs 378 cells deep
# on the anchor's twin, where RILA_US_S's runs 1,095.  Beyond the chain are the cells above
# it, from net_cf down to the Investment Amount before the withdrawal, 8 levels, and below
# its first month that month's interim value, which prices the term's option portfolio at
# its start: the interim value, its ratio and factor, the fixed-leg factor, the amortized
# budget, the budget, the portfolio and a leg, and under the leg the market of the term's
# start, 10 levels on the anchor, or the cap, its solve and a Black-Scholes price where
# nge_reset re-solves the cap, 13.  Measured cold on fresh reads of the committed points,
# a call runs 13 to 21 levels beyond its chain: 16 to 19 on the twins, 13 to 21 on the
# rows in force, 21 on the reset point valued at its renewal (13 at 72), whose month 0
# re-solves the cap.  That is more than D5's 16 (USLIB-SEC-PLAN.md §7.8); 24 leaves room
# for the Data cells Phase 2 adds under each table reader.  A chain of two cells a month
# doubles the depth, and fails here, where every comparison passes.
CHAIN_OVERHEAD = 24

# The product's youngest issue age (product-spec), from which the longest cover runs to the
# Maturity Date at 90: 1,080 months.  The shipped mortality table starts at 40, so the depth
# test extends it below.
CONTRACT_MIN_AGE = 0


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _read(folder, tag, refs=None, data=None):
    """The model in ``folder``, read under a name of its own, its References set at once.

    ``refs`` go on ``Projection`` and ``data`` on ``Data``, before the model computes
    anything: a compiled model never clears a cache, so a Reference set after a Space has
    computed would leave its values as they were.
    """
    model = mx.read_model(folder, name=_name(tag))
    for ref, value in (refs or {}).items():
        setattr(model.Projection, ref, value)
    for ref, value in (data or {}).items():
        setattr(model.Data, ref, value)
    return model


def _key(model, point_id):
    """The registry's key for the row labelled ``point_id`` (``us_registry.point_keys``)."""
    return dict(zip(model.Data.model_point_table().index, point_keys(model)))[point_id]


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    return projection(model, _key(model, point_id))


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for a twin, ``d`` for a derived row, ``-k``
    for a future one.  The twins keep S's ``point_id`` and ``policy_id``, so the S policy
    is the twin's.
    """
    policy = table.at[s_point, "policy_id"]
    hit = table.index[(table["row_kind"] == kind) & (table["source_policy_id"] == policy)
                      & (table["source_mth"] == month)].tolist()
    assert len(hit) == 1, f"{kind} rows of S point {s_point} at month {month}: {hit}"
    return hit[0]


def _row_key(model, kind, s_point, month):
    """The registry's key for that row of ``model``'s table (:func:`_label`)."""
    return _key(model, _label(model.Data.model_point_table(), kind, s_point, month))


def _row(model, kind, s_point, month):
    """The ItemSpace of that row of ``model``'s table (:func:`_label`)."""
    return projection(model, _row_key(model, kind, s_point, month))


def _source(s_model, table, point_id):
    """The ItemSpace of the S point that row ``point_id`` of ``table`` was made from.

    Found by the row's ``source_policy_id`` among the S table's ``policy_id`` s, so that no
    numbering of either table is assumed.
    """
    s_table = s_model.Data.model_point_table()
    hit = s_table.index[s_table["policy_id"] == table.at[point_id, "source_policy_id"]]
    assert len(hit) == 1, (point_id, hit.tolist())
    return _point(s_model, hit[0])


def _release(model, key, collect=False):
    """Drop the ItemSpace at ``key``, the registry's key, and every value it has cached.

    A projected point holds its cached values and their dependency graph, and the splice's
    rows and the scaled and extract copies' points are each needed once, so each is
    released when read, as ``run_sec.py --block`` releases its points (USLIB-SEC-PLAN.md
    F5).  Asked for again, the ItemSpace is made afresh and recomputes.  With ``collect``,
    the collector runs at once, as it does for each splice row.  That costs little,
    because the swept models the module holds are frozen out of the collector
    (:func:`_freeze`), so the collection scans only what the row made.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each module fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds.  The collection first means no garbage is frozen with
    them.  The freeze is undone as the module ends (:func:`_collector`).
    """
    gc.collect()
    gc.freeze()


def _refreeze():
    """Return what is frozen to the collector, collect its garbage, and freeze the rest.

    An ItemSpace released after its model was frozen (:func:`_freeze`) leaves its cycles in
    the frozen generation, where no collection reaches them: the splice's S points, swept
    and frozen in the fixture, released one by one in T2.  Called once, after the last T2
    case, it frees them, at the cost of one full collection.
    """
    gc.unfreeze()
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _committed_scenarios():
    """The committed scenarios as the file holds them, on a default index."""
    return pd.read_csv(model_path(SEC).parent / SCENARIOS)


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder.

    ``edits`` go to ``sec_support.temp_inputs``, after the table: a
    ``market_scenario_sec.csv`` among them replaces the committed scenarios, which name the
    committed rows' copies.
    """
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit=None, tag="edited", refs=None, edits=None):
    """RILA_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
    table = (edit or (lambda t: t))(_committed())
    return _read(_sec_inputs(tmp_path, table, edits), tag, refs)


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


def _plus(column, points, amount):
    """An edit that adds ``amount`` to ``column`` at ``points`` alone."""
    def edit(table):
        moved = table[column].where(~table.index.isin(points), table[column] + amount)
        return table.assign(**{column: moved})
    return edit


def _both(*edits):
    """The edits applied in turn."""
    def edit(table):
        for one in edits:
            table = one(table)
        return table
    return edit


def _drop(column):
    return lambda table: table.drop(columns=column)


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


def _code(space, label):
    """The argument that selects timing, kind or bucket ``label``: at stage ``"E"``, the
    string itself.

    The conventions' lookup (``test_model_conventions._timing``), on ``Projection`` or any
    of its ItemSpaces, which see its References: Phase 2 turns S's timing, kind and bucket
    strings into int References of the same names (R9), and this passes whichever the
    model defines, so the calls below read the same at both stages.
    """
    value = space.refs.get(label)
    return value if isinstance(value, int) else label


def _market(space, column):
    """The argument that selects scenario column ``column`` in ``market_state``.

    ``RILA_US_S`` names it by the column, ``"index_level"``; at stage ``"EC"`` the SEC
    model names it by an int Reference of the column upper-cased, ``INDEX_LEVEL`` (R9),
    which this passes where the space defines it, and the column itself otherwise, so
    that one call reads the same on S and on SEC at either stage.
    """
    value = space.refs.get(column.upper())
    return value if isinstance(value, int) else column


def _legs(proj):
    """The legs of ``proj``'s replicating portfolio, in ``RILA_US_S``'s order.

    ``RILA_US_S``'s ``opt_legs()``, a tuple of leg names; at stage ``"EC"`` the SEC model
    names them by int codes, ``opt_leg(i)`` for ``i`` below ``opt_leg_count()`` (R10).
    """
    if "opt_legs" in proj.cells:
        return proj.opt_legs()
    return tuple(proj.opt_leg(i) for i in range(proj.opt_leg_count()))


def _mismatches(s_proj, sec_proj, **kwargs):
    """:func:`sec_support.twin_mismatches`, the one place this module calls it.

    It passes the SEC Space's :func:`sec_support.codes`, which map S's timing and kind
    strings to the int codes Phase 2 gives them, and the spec's ``twin_arg_map``,
    ``sec_support._rila_codes``, after any map of the caller's, which turns S's
    ``kind=None`` totals into ``ALL`` and its scenario columns into their upper-cased names
    (R9, R12).  At stage ``"E"`` there are none, and the codes are ``{}``; every comparison
    goes through here, so each takes Phase 2's codes.
    """
    spec_map = SPEC.twin_arg_map
    if spec_map is not None and codes(sec_proj):
        own = kwargs.pop("arg_map", None)
        kwargs["arg_map"] = (spec_map if own is None else
                             lambda name, args: own(name, spec_map(name, args)))
    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), **kwargs)


def _sweep(proj):
    """Evaluate on an S point or an SEC row what the splice compares: the reports and more.

    :func:`sec_support.sweep`, every report and check; then, over the frame from the first
    month on the books, the cells and arguments no report or check reaches on
    ``RILA_US_S``, compared nowhere otherwise (USLIB-SEC-PLAN.md §7.10, *never reached*):
    ``duration_mth``, the fixed-leg yield and the implied spread, the option-pricing market
    at each month end, which S reads on point 7 alone, the decomposition after the
    withdrawal and the amortized budget at both timings, each leg after the withdrawal, the
    term-start portfolio's assessment base, the opening notional and the Investment Amount
    after the withdrawal, the balances after it, the block's Account Value before it and the
    excess over the Account Value of each kind of claim.  And the free-withdrawal base and
    allowance at every month, where S reads them at anniversary months alone: the year
    under way's base, ``av_pp_prev_anniv_init`` on a row in force, is read nowhere else
    before the year's anniversary.  ``policy_id`` is left out: a generated row's is its own,
    which the clocks test asserts.  An S point and an SEC row are swept alike, so what S
    caches is what T2 compares.
    """
    sweep(proj)
    entry = proj.t_entry() if "t_entry" in proj.cells else 0
    legs = _legs(proj)
    for t in range(entry, proj.proj_len()):
        proj.duration_mth(t)
        proj.fixed_leg_yield(t)
        proj.nge_spread_implied(t)
        proj.free_wd_base(t)
        proj.free_wd_allow(t)
        proj.risk_free(t)
        proj.div_yield(t)
        proj.impl_vol(t)
        proj.av_at(t, _code(proj, "BEF_WD"))
        proj.av_pp_at(t, _code(proj, "AFT_WD"))
        proj.inv_amt_pp_at(t, _code(proj, "BEF_CREDIT"))
        proj.inv_amt_pp_at(t, _code(proj, "AFT_WD"))
        proj.fixed_acct_pp_at(t, _code(proj, "AFT_WD"))
        proj.holding_acct_pp_at(t, _code(proj, "AFT_WD"))
        for timing in ("BEF_ROLL", "AFT_WD"):
            proj.budget_amort_pp(t, _code(proj, timing))
            proj.fixed_proxy_pp(t, _code(proj, timing))
            proj.deriv_proxy_pp(t, _code(proj, timing))
            proj.trading_cost_pp(t, _code(proj, timing))
        for leg in legs:
            proj.opt_component_pp(t, leg, _code(proj, "AFT_WD"))
        proj.opt_portfolio_abs(t, proj.index_at_term_start(t), proj.tau(t),
                               _code(proj, "TERM_START"))
        for kind in KINDS:
            proj.claims_over_av(t, _code(proj, kind))


def _compared(s_proj, sec_proj, month, exempt):
    """Where row ``sec_proj``, restated at S month ``month``, departs from S cell by cell.

    In two passes (§5.2): every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every
    argument S cached inside its frame from month ``month`` on, to 1e-9 relative with no
    absolute floor; then the residuals alone, at the default floor of 1e-9.  On a row whose
    scenario's state at ``t = 0`` is moved off its term-start columns
    (:func:`_moved_term_starts`), ``market_state`` at ``t = 0``, which no cell of that row
    reads, is the one key left out: S holds there its market at the valuation month, and
    every month's market is compared through the cells that read it.
    """
    moved = sec_proj.scenario_id().endswith("-T")

    def arg_map(name, args):
        return None if moved and name == "market_state" and args[0] == month else args

    found = _mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                        atol=0.0, arg_map=arg_map)
    return found + _mismatches(s_proj, sec_proj, t_offset=month,
                               exempt=exempt | (set(s_proj.cells) - RESIDUALS))


def _frames(s_proj, sec_proj, month, keep=None):
    """Where the four reports of ``sec_proj`` depart from S's, frame by frame, at no floor.

    ``keep`` gives ``result_cf``'s columns to compare, all of them by default.
    """
    found = []
    for report in REPORTS:
        columns = keep if report == "result_cf" else None
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=columns, atol=0.0)]
    return found


def _continues_s(s_proj, sec_proj, month, exempt=SPLICE_EXEMPT):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison, on the committed model at the shipped assumptions: frame by
    frame, the four reports, then cell by cell over every cell of S's but ``exempt``
    (:func:`_compared`), :data:`SPLICE_EXEMPT` on a row restated in force and
    :data:`FUTURE_EXEMPT` on one issued later.  The shipped 2.5% expense inflation steps by
    policy year in S and by valuation year here (D7), so :data:`INFLATED`'s two columns,
    and :data:`INFLATION_CELLS`, differ by design and are left out; the inflation test
    holds them.  Every other column and cell must agree, to 1e-9 with no absolute floor.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    found = _frames(s_proj, sec_proj, month, keep)
    return found + _compared(s_proj, sec_proj, month, exempt | INFLATION_CELLS)


def _case_id(kind, s_point, month):
    """A case's id: ``point13-d80``, or ``point1-k13`` if it is issued later."""
    if kind == "future":
        return f"point{s_point}-k{-month}"
    return f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}")


def _case(case, core, case_id):
    """One parametrized case: run by default if it is in ``core``, else on the full grid."""
    return pytest.param(*case, id=case_id, marks=() if case in core else FULL_ONLY)


def _selected(cases, core):
    """The cases this run makes rows for: the core, or every one under USLIB_SEC_FULL."""
    return [case for case in cases if SEC_FULL or case in core]


# Every row the splice compares, as (row_kind, S point, source_mth), T3's included, and the
# default run's among them.
GRID = (*SPLICES, *IN_FORCE_TWINS, *(("future", p, -k) for p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k) for p, k in CORE_FUTURES)})

# This run's T2 cases, in the order they run, the last of them for each S point, after which
# that point's swept S ItemSpace is released, and the last of all, after which what the
# releases left is collected (:func:`_refreeze`).  A point a future case reads is kept.
T2_CASES = tuple(_selected(SPLICES + IN_FORCE_TWINS, CORE_SPLICES))
LATER = {p for p, k in _selected(FUTURES, CORE_FUTURES)}
LAST_OF_POINT = {case[1]: case for case in T2_CASES if case[1] not in LATER}


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


# The scenario's fields and the term-start column each fixes (_moved_term_starts).
TERM_START_FIELDS = {"index_level": "index_at_term_start_init",
                     "mvr": "mvr_at_term_start_init",
                     "risk_free": "risk_free_at_term_start_init",
                     "div_yield": "div_yield_at_term_start_init",
                     "impl_vol": "impl_vol_at_term_start_init"}


def _moved_term_starts(table, scenarios):
    """``table`` and ``scenarios`` with each mid-term row on a copy moved off its columns.

    A row valued mid-term carries the market of its term's start as five columns, and its
    re-based scenario's state at ``t = 0`` is S's at the valuation month, which a stepped
    path can leave equal to the term start's in some field: a model that read the
    scenario at ``t = 0`` for a column would then give S's numbers all the same.  So each
    such row runs on a copy of its scenario of its own, ``{id}-T``, since a row renewing
    at the valuation month on the same scenario reads the state at ``t = 0``: in it the
    state at ``t = 1``, which month 0 is valued at, is written first where the copy has no
    row there, and the state at ``t = 0`` is then moved off every column, each field by a
    quarter.  A correct model never reads it: month 0 is valued at ``t = 1``, a renewal in
    the frame at its own month, and the term's start comes from the row.  Each moved field
    is asserted apart from the column of every row that reads the copy.
    """
    mid = table["index_at_term_start_init"].notna()
    copies = []
    for sid in dict.fromkeys(table.loc[mid, "scenario_id"]):
        path = scenarios[scenarios["scenario_id"] == sid].assign(scenario_id=f"{sid}-T")
        start = path["month_end"] == 0
        if not (path["month_end"] == 1).any():
            path = pd.concat([path, path[start].assign(month_end=1)])
        start = path["month_end"] == 0
        path.loc[start, list(TERM_START_FIELDS)] = 1.25 * path.loc[
            start, list(TERM_START_FIELDS)]
        moved = path[start].iloc[0]
        for field, column in TERM_START_FIELDS.items():
            held = table.loc[mid & (table["scenario_id"] == sid), column]
            assert (held != moved[field]).all(), (sid, field)
        copies.append(path.sort_values("month_end"))
    table = table.assign(scenario_id=table["scenario_id"].where(
        ~mid, table["scenario_id"] + "-T"))
    return table, pd.concat([scenarios, *copies], ignore_index=True)


def _sec_built(root, s, derived=(), future=(), edits=None, moved=False):
    """SEC's inputs for a table the generator builds from S model ``s``: its folder.

    The registered spec with its rows replaced by ``derived`` and ``future``, built from
    ``s`` (``sec_support.build_sec_table``), written with its re-based scenarios into a copy
    of the product directory, with ``edits`` beside them.  With ``moved``, each row valued
    mid-term runs on a copy of its scenario whose state at ``t = 0`` is moved off its
    term-start columns (:func:`_moved_term_starts`), as the splice's rows do.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(derived), future=tuple(future))
    table, companions = build_sec_table(spec, s)
    assert set(companions) == {SCENARIOS}
    if moved:
        table, scenarios = _moved_term_starts(table, companions[SCENARIOS])
        companions = {SCENARIOS: scenarios}
    return temp_inputs(root, model_path(SEC), model_points=table, model_point_file=TABLE,
                       edits={**(edits or {}), **companions})


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module", autouse=True)
def _collector():
    """Undo, as the module ends, the freezes its fixtures made (:func:`_freeze`).

    Set up before every other fixture of the module, it is torn down after them all, once
    every model the module read is closed, and then returns what was frozen to the
    collector and collects it, so that nothing frozen here outlives the module.
    """
    yield
    gc.unfreeze()
    gc.collect()


@pytest.fixture(scope="module")
def sec_read():
    """RILA_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(400)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`_sweep`), in table order and each column in ascending ``t``, under a
    recursion limit lowered to :data:`CALL_DEPTH`, and whatever that raises is kept, point
    by point, rather than raised.  Last, the opening-state columns the sweep did not read,
    and the months and fields of the scenario it read, are kept, point by point, before
    any comparison with S evaluates a cell at S's keys.  So the record says what a cold
    model does, which the clock test and the tests of where each column is read assert
    (D3, R2), and every test on the committed model reads a model already swept: the sweep
    is paid once, not once for each.  The swept model is then frozen out of the collector
    (:func:`_freeze`).  Returns ``(model, record)``.
    """
    model = _read(model_path(SEC), "sec")
    first = _row(model, "twin", 1, 0)
    record = {"duration_mth(400)": first.duration_mth(400),
              "keys": list(first.cells["duration_mth"].keys()), "deep": [], "unread": {},
              "market": {}}
    labels = model.Data.model_point_table().index
    limit = mx.get_recursion()
    mx.set_recursion(CALL_DEPTH)
    try:
        for key, point_id in zip(point_keys(model), labels):
            try:
                _sweep(projection(model, key))
            except Exception as err:            # kept, so every point is swept
                record["deep"].append(f"point {point_id}: the sweep raised {_raised(err)}")
    finally:
        mx.set_recursion(limit)
    for key, point_id in zip(point_keys(model), labels):
        p = projection(model, key)
        record["unread"][point_id] = {c for c in STATE if not len(p.cells[c].keys())}
        record["market"][point_id] = set(p.cells["market_state"].keys())
    _freeze()
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """RILA_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """RILA_US_S read in place, as committed, with every point swept (:func:`_sweep`).

    T6 regenerates the SEC table and its scenarios from it, which would otherwise project
    every S point again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force
    tests read S's months off it, the cells its own sweep misses among them.  The swept
    model is then frozen out of the collector (:func:`_freeze`).
    """
    model = read_released_twin(TWIN, model_name=_name("s"))
    for key in point_keys(model):
        _sweep(projection(model, key))
    _freeze()
    yield model
    model.close()


# The rows the product's own tests read on the splice's inputs, whatever the grid: the
# charged withdrawal at its month and the contract issued 13 months on that takes it, and
# nge_reset on a one-year term mid-term, its cap re-solved at the renewal before the
# valuation month and again six months on.
EVENT_ROWS = ((14, 23), (17, 30))
EVENT_FUTURES = ((14, 13),)


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs: ``(s, sec, events)``.

    S is read from a copy of the product directory whose table has the variants appended
    and whose scenarios, surrender rates, withdrawal charges, guaranteed minimums and
    withdrawal programmes are the splice's (:data:`SPLICED_EDITS`), under
    :data:`SPLICED_REFS`, and every S point is swept (:func:`_sweep`) and stays swept until
    the last case that compares a row of it.  SEC runs on the same tables, and on a model
    point table and re-based scenarios of its own, built by the generator from the
    registered spec with its rows replaced by the cases this run selects, the core or the
    full grid (:func:`_selected`), out of this S model, so each row opens with the state of
    the very run it is compared with, each row valued mid-term on a copy of its scenario
    whose state at ``t = 0`` is moved off its term-start columns
    (:func:`_moved_term_starts`).  Each SEC row is projected by the case that compares it
    and released once compared.  The rows the product's own tests read on the splice's
    inputs (:data:`EVENT_ROWS`) are built into a table of their own from the same swept S
    model, in the folder ``events``, which the ``events`` fixture reads, so that no S point
    is projected again for them.

    Everything alive once S is swept is then frozen out of the collector (:func:`_freeze`),
    so that the collection after each row's release scans only what the row made, and once
    the last T2 case has run, what the releases left is collected (:func:`_refreeze`).
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants(), edits=SPLICED_EDITS)
    s = _read(s_folder, "s_spliced", SPLICED_REFS)
    for key in point_keys(s):
        _sweep(projection(s, key))
    derived = [(p, d) for kind, p, d in _selected(SPLICES, CORE_SPLICES)]
    sec_folder = _sec_built(root / "sec", s, derived, _selected(FUTURES, CORE_FUTURES),
                            SPLICED_EDITS, moved=True)
    events = _sec_built(root / "events", s, EVENT_ROWS, EVENT_FUTURES, SPLICED_EDITS,
                        moved=True)
    sec = _read(sec_folder, "sec_spliced", SPLICED_REFS)
    _freeze()
    yield s, sec, events
    sec.close()
    s.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do, by case (:func:`_record`)."""
    return {}


@pytest.fixture(scope="module")
def events(spliced):
    """SEC on the splice's inputs, its table the generator's for :data:`EVENT_ROWS`.

    Built by the ``spliced`` fixture from the splice's S model, swept, and read under
    :data:`SPLICED_REFS`, as the splice's own table is, so each row opens with the state of
    the very run it is compared with.  Each test projects the rows it reads and releases
    them.
    """
    sec = _read(spliced[2], "events", SPLICED_REFS)
    yield sec
    sec.close()


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case sweeps its row, records what the rules test and the core grid's reach
# need of it, compares it with S, and releases it: held together, the rows of the full grid
# would hold gigabytes.  The record is made before the comparison, because the comparison
# evaluates SEC's cells at S's own cached arguments, and those include keys SEC never reads
# itself: S's market at the issue month of a term begun before the valuation date, S's
# year-opening base at an anniversary before it.  Comparing them would plant those keys in
# SEC's cache, for the rules test to report as SEC's.  So each of the two tests reads the
# records, and computes any case no earlier test has recorded, which keeps it whole when
# run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _contract(p):
    """The keys each table reader may take on row ``p``: ``{cell: (lowest, highest)}``.

    The attained ages from the first month on the books to the last covered one, at which
    the mortality table is read; the complete contract years at a month end, from 0, which
    the charge-expiry year's search reads first, to the policy term, at which the last
    covered month ends; the contract years from the first month on the books's to the one
    the Maturity Date closes; and the policy month ends from the first on the books to the
    Maturity Date, at which the withdrawal programme is read.  A table read at a key the
    contract does not have, or one before the valuation date, would wrap round in a
    compiled model (R1, R1a).
    """
    entry, term = p.t_entry(), p.policy_term()
    return {"mort_rate_base_at": (p.age(entry), p.age_at_entry() + term - 1),
            "surr_charge_rate_at": (0, term),
            "lapse_rate_base_py": (p.policy_year(entry), term + 1),
            "wd_amount_pm": (max(1, p.duration_mth_init() + 1), p.maturity_mth())}


def _outside_contract(p):
    """Each cached argument of a table reader of row ``p`` not in :func:`_contract`."""
    found = []
    for name, (lo, hi) in _contract(p).items():
        found += [f"{name}{args}, outside {lo}..{hi}"
                  for args in _cached_args(p.cells[name])
                  if not (_month(args[0]) and lo <= args[0] <= hi)]
    return found


def _month_of(node):
    """The month a precedent ``node`` is keyed by, its ``t``, or None if it takes none."""
    params = getattr(node.obj, "parameters", None) or ()
    u = node.args[params.index("t")] if "t" in params else None
    return u if _month(u) else None


def _months_read(node, reach):
    """The calls keyed by a month that precedent ``node`` reads, as ``(text, month)``.

    ``node`` itself if it is keyed by ``t``.  Otherwise every month-keyed call its own
    precedents read, followed through every call keyed by no month, such as
    ``lapse_shock_year()`` or a Black-Scholes price, as far as the dependency graph goes:
    so a read that looks ahead through a cell taking no ``t`` is the reader's.  ``reach``
    holds what each call keyed by no month reads, so that each is walked once a row, and
    the walk is a loop, not a recursion.
    """
    month = _month_of(node)
    if month is not None:
        return {(f"{node.obj.name}{node.args}", month)}
    top = (id(node.obj), node.args)
    stack, seen = [(node, False)], set()
    while stack:
        here, done = stack.pop()
        key = (id(here.obj), here.args)
        if key in reach:
            continue
        if done:
            found = set()
            for pred in here.preds:
                month = _month_of(pred)
                if month is not None:
                    found.add((f"{here.obj.name}{here.args} -> {pred.obj.name}{pred.args}",
                               month))
                elif "t" not in (getattr(pred.obj, "parameters", None) or ()):
                    found |= reach.get((id(pred.obj), pred.args), set())
            reach[key] = found
            continue
        if key in seen:
            continue
        seen.add(key)
        stack.append((here, True))
        for pred in here.preds:
            if _month_of(pred) is None and (id(pred.obj), pred.args) not in reach:
                if "t" not in (getattr(pred.obj, "parameters", None) or ()):
                    stack.append((pred, False))
    return reach[top]


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has been swept.

    ``{"negative": [...], "early": [...], "ahead": [...], "outside": [...]}``: every cached
    call with a negative argument; every call keyed by a month before ``t_entry()`` that a
    call keyed by a month at or after it reads; every call keyed by a month beyond
    ``t + 1`` that a call keyed by ``t`` reads; and every table key the contract does not
    have (:func:`_contract`).  A call reads its precedents, as modelx's dependency graph
    records them, and, through a precedent keyed by no month, whatever that precedent reads
    in turn (:func:`_months_read`).  RILA admits no look-ahead at all.
    """
    entry = proj.t_entry()
    negative, early, ahead = [], [], []
    reach = {}
    for name, cells in proj.cells.items():
        t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if t_pos is None:
                continue
            t = args[t_pos]
            for node in cells.preds(*args):
                if _month_of(node) is None and "t" in (
                        getattr(node.obj, "parameters", None) or ()):
                    continue
                for read, u in sorted(_months_read(node, reach)):
                    if u < entry <= t:
                        early.append(f"{name}{args} -> {read}")
                    if u > t + 1:
                        ahead.append(f"{name}{args} -> {read}")
    return {"negative": negative, "early": early, "ahead": ahead,
            "outside": _outside_contract(proj)}


# The months of each S point the acceptance test restates: by default its first year's,
# every sixth after, which takes in every anniversary and every renewal, and each year's
# last month, and with USLIB_SEC_FULL=1 every month of its frame.
EVERY_STRIDE = 1 if SEC_FULL else 6


def _every_state_months(n):
    """The months a frame of ``n`` is restated at (:data:`EVERY_STRIDE`), from month 1."""
    return sorted({*range(1, min(12, n)), *range(EVERY_STRIDE, n, EVERY_STRIDE),
                   *range(11, n, 12)})


def _states_s_reaches(s):
    """The states ``s``'s points reach, as ``(S point, month)``: ``(kept, emptied)``.

    Each month of :func:`_every_state_months` of each point of ``s``, an S model whose
    References are set.  ``emptied`` holds the months a contract enters holding nothing,
    its Investment Amount and both accounts 0, the one state the product refuses by name:
    ``RILA_US_S`` keeps a contract in force once a withdrawal has taken its whole value.
    ``kept`` holds every other.
    """
    kept, emptied = [], []
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        p = projection(s, key)
        for d in _every_state_months(p.proj_len()):
            held = p.inv_amt_pp(d - 1) + p.fixed_acct_pp(d - 1) + p.holding_acct_pp(d - 1)
            (kept if held != 0.0 else emptied).append((point_id, d))
    return kept, emptied


def _refused_in_force(s, states, root, edits, refs):
    """What ``Data`` and ``proj_len()`` refuse of ``states`` of ``s``, restated in force.

    The generator builds one table of every point's twin and a derived row at each state,
    beside ``edits``, S's edited inputs (:func:`_sec_built`), which a model read with
    ``refs`` set first reads through ``Data``, and then asks every row for its frame,
    releasing each, collecting every 500.  Returns each refusal, the line naming it,
    ``Data``'s or each row's ``proj_len()``'s.
    """
    model = _read(_sec_built(root, s, states, (), edits), "every", refs)
    try:
        try:
            read = model.Data.model_point_table()
        except Exception as err:                # reported, with the rows' states
            return [f"Data: {_raised(err)}"]
        assert len(read) == len(s.Data.model_point_table()) + len(states)
        refused = []
        for i, key in enumerate(point_keys(model)):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so the scan goes on
                refused.append(_raised(err))
            _release(model, key, collect=i % 500 == 0)
        return refused
    finally:
        model.close()


def test_every_state_s_reaches_is_accepted_in_force(spliced, tmp_path):
    """Every state ``RILA_US_S`` reaches is a valid opening state, but a contract emptied.

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a contract in force
    can be, so they must accept each state the S model reaches, at References off their
    shipped values as at them: a rule exercised only on the rows the other tests choose
    could refuse a state S reaches elsewhere (D6).  This test runs on the splice's inputs:
    S's table with the variants, on the splice's market paths, surrender and charge rates,
    guaranteed minimums and programmes (:data:`SPLICED_EDITS`), under the splice's
    References (:data:`SPLICED_REFS`); the next runs on S's shipped ones, the other set
    of inputs the module reads every S point under, on which S's states differ (§5.2,
    T5, precised at M9).  So every S point of the splice, swept, is restated in force at
    every month of its first year, every sixth month after, each anniversary and each
    renewal among them, and the last month of each year, where the windows of ``Data``'s
    first-year, anniversary, renewal and term-start rules open and close
    (:func:`_every_state_months`), or with ``USLIB_SEC_FULL=1`` at every month of its
    frame, by the generator, into one table: ``Data`` accepts the table, and no row's
    ``proj_len()`` refuses it (:func:`_refused_in_force`).  But for one state, set aside
    first: ``RILA_US_S`` keeps a contract in force once a withdrawal has taken its whole
    value, holding nothing, as the programme of variant 21 leaves it from policy month 30,
    and ``Data`` refuses a contract in force that holds nothing, which its docstring
    states.  It is the only state set aside, and a table holding it is refused, by name.
    """
    s = spliced[0]
    twins = len(s.Data.model_point_table())         # each S point's twin leads the table
    kept, emptied = _states_s_reaches(s)
    assert emptied and all(p == 21 and d >= 30 for p, d in emptied), emptied
    refused = _refused_in_force(s, kept, tmp_path / "every", SPLICED_EDITS, SPLICED_REFS)
    assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
    model = _read(_sec_built(tmp_path / "emptied", s, emptied[:1], (), SPLICED_EDITS),
                  "emptied", SPLICED_REFS)
    try:
        _refused(model.Data.model_point_table,
                 f"{TABLE}: a contract in force must hold an investment amount or an "
                 f"account balance; none does at point_id [{twins + 1}]")
    finally:
        model.close()


def test_every_state_s_reaches_as_shipped_is_accepted_in_force(tmp_path):
    """Every state ``RILA_US_S`` reaches as shipped is a valid opening state too.

    The test above runs on the splice's inputs, and S's states differ on its own: its
    fifteen points on its shipped market paths, the Holding Account empty, the Fixed
    Account taking 15% of a term end, the declared account rate above its floor and the
    interim value's References as shipped, the set of References and inputs the committed
    table is generated from and the other the module reads every S point under
    (USLIB-SEC-PLAN.md §5.2, T5, precised at M9, taken at M13, §5.4).  So ``RILA_US_S``,
    read in place, is restated in force at the same months (:func:`_every_state_months`),
    or with ``USLIB_SEC_FULL=1`` at every month of each frame, by the generator, into one
    table: ``Data`` accepts it, and no row's ``proj_len()`` refuses it
    (:func:`_refused_in_force`).  No state is set aside, since no shipped programme takes
    a contract's whole value.  The References the module moves for one test alone, T4's
    switched-on assumptions, the cap test's A/E and the maturity age and free rate
    :data:`REFUSED` admits under, move S's states from these in one respect each, the
    split between the two accounts, the count, the remainder and the months of cover, and
    a probe at M13 read each such state at every month.
    """
    s = _read(model_path(TWIN), "every_s")
    try:
        kept, emptied = _states_s_reaches(s)
        assert not emptied, emptied[:5]
        assert len(kept) > 800, len(kept)
        refused = _refused_in_force(s, kept, tmp_path / "every", None, {})
        assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
    finally:
        s.close()


def _record(case, proj):
    """Sweep the splice row ``proj`` of ``case`` and record what the rules test needs of it.

    :func:`_rule_breaches`'s record, with the row's :func:`_branches`.  A row that raises is
    recorded as raising, which the rules test reports.
    """
    try:
        _sweep(proj)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj, case[0])
        record["raised"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "outside": [],
                  "branches": set(), "raised": _raised(err)}
    return record


def _record_of(spliced, records, case):
    """The record of ``case``, from the case that compared its row or, failing it, now."""
    if case not in records:
        sec = spliced[1]
        key = _row_key(sec, *case)
        try:
            records[case] = _record(case, projection(sec, key))
        finally:
            _release(sec, key, collect=True)
    return records[case]


# ---------------------------------------------------------------------------
# T2 -- the splice


@pytest.mark.parametrize(
    "kind, s_point, month",
    [_case(case, CORE_SPLICES, _case_id(*case)) for case in SPLICES + IN_FORCE_TWINS])
def test_an_in_force_point_continues_its_s_projection(spliced, splice_records, kind,
                                                      s_point, month):
    """Opened with S's state at month d, the point is S from d on, in every cell of S's.

    This is the test that says the opening state is complete: a state column the SEC row
    did not carry, or carried from the wrong instant, would make SEC part from S here, and
    nowhere else, because on a point issued at ``t = 0`` the two clocks coincide and the
    opening state is the purchase payment, nothing in the accounts and no term begun.  For
    the same reason it is the test that catches a policy month passed as ``t`` (R1a): the
    Term Start and End Dates, the anniversaries, the withdrawal programme and the Maturity
    Date all read the policy clock; and the market read on the wrong clock, since each
    row reads its own copy of its scenario re-based to its month, and every field of the
    splice's paths steps within every term; and a term's start read from the scenario at
    the valuation date instead of the row, since a row valued mid-term reads a copy whose
    state there is moved off its columns (:func:`_moved_term_starts`).  The frame
    comparisons read SEC row ``t`` against S row ``t + d`` in every column of the four
    reports, and fail frames that end apart.  The cell comparison then evaluates every
    cell of S's but
    :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from month ``d``
    on, moved onto SEC's clock, to 1e-9 relative with no absolute floor
    (:func:`_compared`): the Investment Amount and the interim value at each timing, the
    two accounts, the Account Value, the free-withdrawal base, allowance and remainder,
    the return-of-premium base, the term-start market and the cap, every leg of the
    option portfolio, the counts and the benefits among them.  The floor would hide what
    matters late in a frame, where the count falls to 1e-8.  The three roll-forward
    residuals are compared at the floor, since they are rounding around 0.  An S cell this
    model lacked would fail it.

    The row is swept and recorded for the rules test first (:func:`_record`), then compared,
    and released either way, and so is its S point after the last case that compares a row
    of it.
    """
    s, sec = spliced[0], spliced[1]
    case = (kind, s_point, month)
    key = _row_key(sec, *case)
    try:
        sec_proj = projection(sec, key)
        splice_records[case] = _record(case, sec_proj)
        s_proj = _point(s, s_point)
        assert _frames(s_proj, sec_proj, month) == []
        assert _compared(s_proj, sec_proj, month, SPLICE_EXEMPT) == []
    finally:
        _release(sec, key, collect=True)
        if LAST_OF_POINT.get(s_point) == case:
            _release(s, _key(s, s_point))
        if T2_CASES and case == T2_CASES[-1]:
            _refreeze()


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the Maturity Date, in the
    four reports, and every cell of S's but :data:`FUTURE_EXEMPT` agrees at every argument
    S cached inside its own frame, moved ``k`` later, to 1e-9 relative with no absolute
    floor, the residuals at the floor.  An S cell this model lacked would fail it.  Before
    issue every column of the four reports is an exact zero, and the contracts arrive in
    month ``k`` as new business, bringing the purchase payment.  The row's scenario is its
    own copy of S's, ``{id}-F{k}``, moved ``k`` months later, which holds no level before
    the issue month, so that a read there raises inside the comparison.

    The last assertions are R1 and D4's base rule made testable.  After every report, no
    decrement rate keyed by month has been evaluated at a month before issue, and the
    mortality table has not been read below the issue age, nor the surrender table below
    contract year 1.  A count, a balance or a carry based at ``t == 0`` rather than at
    ``t_entry()``, or a rate that reads its table before asking whether the month is in
    cover, still gives the right numbers.  The rules test's look-back and the guard test
    see the first too, and the guard test the second.

    The pre-issue rows are asserted present before they are asserted zero: a frame that
    opened at issue would have none, its zeros would hold of nothing, and the comparisons
    with S, which start there, would not see it.  The row is swept and recorded for the
    rules test first (:func:`_record`), and released after.  The S point is swept here,
    where T2 has released it.
    """
    s, sec = spliced[0], spliced[1]
    case = ("future", s_point, -k)
    key = _row_key(sec, *case)
    try:
        sec_proj = projection(sec, key)
        splice_records[case] = _record(case, sec_proj)
        s_proj = _point(s, s_point)
        _sweep(s_proj)
        assert _frames(s_proj, sec_proj, -k) == []
        assert _compared(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report in REPORTS:
            frame = sec_proj.cells[report]()
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        assert sec_proj.premiums(k) == s_proj.premiums(0) == s_proj.premium_pp() > 0.0
        assert sec_proj.scenario_id() == f"{s_proj.scenario_id()}-F{k}"
        early = {name: sorted(args for args in _cached_args(sec_proj.cells[name])
                              if args[0] < k)
                 for name in DECREMENT_RATES}
        assert not any(early.values()), f"rates evaluated before issue: {early}"
        low = [x for (x,) in _cached_args(sec_proj.cells["mort_rate_base_at"])
               if x < sec_proj.age_at_entry()]
        assert not low, f"mortality read below the issue age: {low[:5]}"
        years = [y for (y,) in _cached_args(sec_proj.cells["lapse_rate_base_py"]) if y < 1]
        assert not years, f"surrender rates read before contract year 1: {years[:5]}"
    finally:
        _release(sec, key, collect=True)


# ---------------------------------------------------------------------------
# D11's R1, R1a and R2, and D3's closed-form clock


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back, R1a's keys and R2's look-ahead, on the rows T2 and T3 compare.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, the variants among
    them, and points issued later, and each was swept first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative on
      a row valued after it: the Term Start Date of a term begun before the valuation
      month, and the anniversary month whose ``"BEF_WD"`` value is the year's
      free-withdrawal base.  So does a balance or a count read a month back without the
      opening state's branch, and ``RILA_US_S``'s ``market_state(k)`` would fail there on
      ``max([])``.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the months before, where every balance is 0, so no number shows
      it and no argument goes negative.
    * R1a's keys: the mortality table is read at attained ages from the first month on the
      books to the last covered one, the surrender table at contract years from that
      month's to the Maturity Date's, the withdrawal charges at complete years the contract
      has, and the withdrawal programme at policy month ends from the first on the books to
      the Maturity Date (:func:`_contract`): a table read at a key before the valuation
      date, or one the contract does not have, would wrap round in a compiled model.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents, read
      directly or through a precedent keyed by no month, which is followed to the
      month-keyed calls it reads (:func:`_months_read`).  The market is read at the month
      end, ``t + 1``, and the count carried out of the month, ``pols_if_at(t + 1,
      "BEF_NB")``, by the Account Value after the withdrawal and the count's roll-forward;
      RILA admits no other look-ahead.

    Each row was scanned by the T2 or T3 case that compared it (:func:`_record`), and a row
    no case has scanned is scanned here.  The core case covers the core's rows, the full
    case every other row of the full grid, with ``USLIB_SEC_FULL=1``.  The twins in the
    splice's table are no case's, and are left out: on them the clocks coincide, and T1
    compares them with S cell by cell.  The closed-form clock and the recursion depth are
    asserted on the committed model, in the tests after this one.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    found = {"negative": [], "early": [], "ahead": [], "outside": [], "raised": []}
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        for what in ("negative", "early", "ahead", "outside"):
            found[what] += [f"{where}: {item}" for item in record[what]]
        if record["raised"]:
            found["raised"].append(f"{where}: {record['raised']}")
    assert cases, f"the {grid} grid has no rows"
    assert not found["raised"], f"rows that raised: {found['raised'][:10]}"
    assert not found["negative"], f"called at a negative argument: {found['negative'][:10]}"
    assert not found["early"], f"read before issue from the books: {found['early'][:10]}"
    assert not found["ahead"], f"read beyond t + 1: {found['ahead'][:10]}"
    assert not found["outside"], f"outside the contract: {found['outside'][:10]}"


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(400)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 401 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow, which is why the depth is asserted on its own, in the next test.  A
      backward recursion over the frame, through ``t + 1``, keeps every step within the
      look-ahead but opens a chain as long as the frame, which a compiled model would run
      on the C stack (F7), and fails here.
    """
    record = sec_read[1]
    assert record["duration_mth(400)"] == 400
    assert record["keys"] == [400]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"


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


def _extended_mortality(table):
    """The mortality table extended below age 40 by a distinct rate per age and sex.

    ``q(40) x 0.97 ** (40 - x)``: geometric in age, never flat, so that a read at the wrong
    age reads another number, and an issue age of 0, the contract's youngest
    (product-spec), projects its whole cover.
    """
    rows = []
    for sex in ("M", "F"):
        q40 = float(table.loc[(table["age"] == 40) & (table["sex"] == sex),
                              "mort_rate"].iloc[0])
        rows += [{"age": x, "sex": sex, "mort_rate": q40 * 0.97 ** (40 - x),
                  "provenance": "extended below 40 for a test"} for x in range(40)]
    return pd.concat([pd.DataFrame(rows), table], ignore_index=True)


# The chains a cold call walks, each one cell a month back to t_entry(): the count, the
# Investment Amount, the two accounts, the return-of-premium base, the free-withdrawal
# carry and the Account Value, and net_cf, which walks them all.
CHAIN_HEADS = ("pols_if", "inv_amt_pp", "fixed_acct_pp", "holding_acct_pp", "rop_pp",
               "free_wd_avail", "av_pp")


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold call holds one frame a month back to ``t_entry()``, and a few more (F7).

    Every recursion here is one cell a month: the count, the Investment Amount, the Fixed
    and Holding Accounts, the return-of-premium base and the free-withdrawal carry, where
    ``RILA_US_S``'s count and carry ran two cells a month and its Investment Amount three.
    A compiled model runs each chain on the C stack, so the depth is what sizes it, and no
    comparison sees it: a chain of two cells a month gives the same numbers.  So a cold
    ``net_cf`` in the last month, on an ItemSpace of the committed model just read, holds
    at least one frame for each month back to ``t_entry()``, and so walked its chain, and
    at most :data:`CHAIN_OVERHEAD` more: on the twins of the anchor and of the behavioural
    rule, 360 months; on the anchor in force 71 months, the nge_reset point in force 80
    months and valued at its renewal at 72, the deepest of the committed points, 21 levels
    beyond its chain, whose month 0 re-solves its cap; and on the anchor issued 13 months
    on, whose chain stops at its issue: one that ran on through its months before issue,
    as one guarded by the frame rather than by cover would, walks 13 months further, and
    fails.  Each chain called alone on its own fresh read, in the last month of the anchor
    in force, runs at most as deep.

    The same holds at the contract's longest cover from issue, 1,080 months at issue age 0,
    which the shipped mortality, starting at 40, cannot price: on a copy whose mortality is
    extended below 40 (:func:`_extended_mortality`), the anchor issued at 0 at the
    valuation date and 120 months after it, the horizon, each cold.  That is the depth
    Phase 2's stack is sized from (USLIB-SEC-PLAN.md §7.8).
    """
    committed = _committed()
    found, depths = [], {}
    labels = [_label(committed, "twin", 1, 0), _label(committed, "twin", 3, 0),
              _label(committed, "derived", 1, 71), _label(committed, "derived", 13, 80),
              _label(committed, "derived", 13, 72), _label(committed, "future", 1, -13)]
    table = committed.loc[[labels[0], labels[-1]]].assign(age_at_entry=CONTRACT_MIN_AGE)
    table = _set("duration_mth", [labels[-1]], -120)(table)
    longest = _sec_inputs(tmp_path, table, edits={"mort_table.csv": _extended_mortality})
    reads = [("committed", model_path(SEC), labels, ("net_cf",)),
             ("committed", model_path(SEC), labels[2:3], CHAIN_HEADS),
             ("longest", longest, list(table.index), ("net_cf",))]
    for where, folder, points, cells in reads:
        for label, cell in itertools.product(points, cells):
            fresh = _read(folder, "depth")
            try:
                p = _point(fresh, label)
                months = p.proj_len() - p.t_entry()
                depth = _cold_depth(p, cell, (p.proj_len() - 1,))
                depths[where, label, cell] = (months, depth)
                low = months if cell == "net_cf" else 0
                if not low <= depth <= months + CHAIN_OVERHEAD:
                    found.append(f"{where} point {label}: {cell}({p.proj_len() - 1}) cold "
                                 f"runs {depth} cells deep, outside {low}..{months} and "
                                 f"{CHAIN_OVERHEAD} more")
            finally:
                fresh.close()
    assert not found, found
    assert [depths["longest", label, "net_cf"][0] for label in table.index] == [1080, 1080]


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and so is the new business
# entering once at its policy_count; neither is repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, surrenders and maturities alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, "BEF_DECR")``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, "BEF_NB")``, is the three outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month too
    long: the maturities would then leave a month late, and the count would carry over.
    The notes' end-of-month ``l(t + 1)``, ``pols_if_at(t, "AFT_DECR")``, is exactly the
    count carried into the next month before its new business, in every month but the last
    covered one, where it is what the Maturity Date annuitizes out, on the policy clock, at
    ``duration_mth(t) == maturity_mth() - 1``, and the next month opens empty: the two are
    one product in one order.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.  A timing the model does not have, ``basiclife.BasicTerm_SE``'s
    ``"BEF_MAT"``, which a formula ported from it might ask for, is refused rather than
    answered with another count.
    """
    nb, decr, aft = (_code(sec_model.Projection, label)
                     for label in ("BEF_NB", "BEF_DECR", "AFT_DECR"))
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        last = p.proj_len() - 1
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, decr) - p.pols_if_at(t + 1, nb)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
            if t < last:
                assert p.pols_if_at(t, aft) == p.pols_if_at(t + 1, nb), (point_id, t)
                assert p.pols_maturity(t) == 0.0, (point_id, t)
        assert p.duration_mth(last) == p.maturity_mth() - 1, point_id
        assert p.pols_maturity(last) == p.pols_if_at(last, aft) > 0.0, point_id
        assert p.pols_if_at(last + 1, nb) == 0.0, point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        outflows = pols[["pols_death", "pols_lapse", "pols_maturity"]].sum(axis=1)
        carried = (pols["pols_if"] - outflows).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id
    anchor = _row(sec_model, "derived", 1, 71)
    _refused(lambda: anchor.pols_if_at(0, _code(anchor, "BEF_MAT")), "invalid timing")


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, the fifteen issued at the valuation
    date: every column S's report has agrees, to 1e-9 with no absolute floor, frames ending
    together, and ``pols_new_biz`` holds the count in the issue month and 0 in every other.
    The derived and future rows' reports are compared with S's from their months on by
    :func:`test_every_committed_row_continues_its_s_point`.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index) == list(S_POINTS)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == [theirs.columns[0], "pols_new_biz",
                                      *theirs.columns[1:]], point_id
        assert frame_mismatches(theirs, mine, atol=0.0) == [], point_id
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in mine.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
COUNT_FACTOR = 2.5

# The counted cells that are a difference of two counted aggregates, the residuals among
# them: each is compared at an absolute floor of 1e-9 beside its relative 1e-12, since the
# difference of two numbers of the Account Value's size, scaled each to 1e-12, is exact only
# to about 1e-11 where the difference is small.
DIFFERENCES = RESIDUALS | {"av_change", "claims_over_av", "net_cf"}

# The twins T4 projects beside every row in force or issued later: the anchor, which
# matures at 90 and pays the purchase payment, its acquisition and its premium tax; the
# worked example's programme on the down path, whose withdrawal is free and whose death
# benefit is the return-of-premium base; the uncapped option at 81, past that band; and the
# charged programme, whose withdrawal bears a charge.  Between them and the rows in force
# they carry every flow, every opening-state column, the count in force and new business.
FLOW_TWINS = (1, 2, 12, 14)


def _flow_points(table):
    """The labels of ``table``'s rows that T4 and the extract test project."""
    return [p for p in table.index
            if table.at[p, "row_kind"] != "twin" or p in FLOW_TWINS]


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed table, and a copy with every count multiplied by :data:`COUNT_FACTOR`,
    are each read with :data:`SWITCHED_ON` set before either computes anything: the
    assumptions that ship at zero, premium tax and the Holding Account's share of a term
    end, switched on at the splice's values, so that every flow is nonzero on some point.
    On every point ``result_cf`` and ``result_pols`` are 2.5 times the committed table's,
    element by element, to 1e-12 relative: a scaled count is a computed float, which may
    come back from the CSV within two ulps (``sec_support``'s module docstring).  So is
    every other cell of :data:`COUNTED`, at every argument the sweep of the committed
    table's point cached: the counts at each timing, each kind of claim and the Account
    Value it releases, the block's Account Value either side of the withdrawal and its
    change, the latter and the two aggregate residuals, differences of aggregates, at a
    floor of 1e-9 (:data:`DIFFERENCES`).  And
    every cell outside :data:`COUNTED` (the Investment Amount, the interim value and its
    decomposition, the accounts, the allowance, the return-of-premium base, the benefits per
    contract, the opening state, the market, the rates, both clocks, the flags and the
    checks) agrees bit for bit at every argument that sweep cached.  So a flow that dropped
    the count, or read it as whole contracts, which a table of counts of 1 hides from every
    comparison with S, fails here.  Each counted cell is nonzero on some point.  The points
    are every row in force or issued later and the twins that carry each flow beside them
    (:data:`FLOW_TWINS`), each released once compared.
    """
    table = _committed()
    base = _read(_sec_inputs(tmp_path / "base", table), "counted", SWITCHED_ON)
    scaled = _read(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), "scaled", SWITCHED_ON)
    counted = sorted(COUNTED - {"result_cf", "result_pols"})
    nonzero = set()
    try:
        for point_id in _flow_points(table):
            key, scaled_key = _key(base, point_id), _key(scaled, point_id)
            one, many = projection(base, key), projection(scaled, scaled_key)
            _sweep(one)
            for report in ("result_cf", "result_pols"):
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                want = COUNT_FACTOR * b
                bad = ((d - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (point_id, report, list(bad[bad].index))
            for name in counted:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    floor = 1e-9 if name in DIFFERENCES else 0.0
                    assert abs(got - want) <= floor + 1e-12 * abs(want), (
                        point_id, name, args, got, want)
                    if want != 0.0 and name not in RESIDUALS:
                        nonzero.add(name)
            assert _mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED, rtol=0.0,
                               atol=0.0) == [], point_id
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    want = set(counted) - RESIDUALS
    assert want <= nonzero, f"0 on every point: {sorted(want - nonzero)}"


# The factor the scaled checks are shown at: at a million contracts the Account Value's
# residual, at most 2.4e-5, is still inside the tolerance it would have unscaled, 1e-4; it
# passes that tolerance between 3e6 and 1e7 contracts, so that at 1e8 only the scaling
# closes it.
CHECK_COUNT = 1e8


def test_the_roll_forward_checks_close_on_a_hundred_million_contracts(tmp_path):
    """Both roll-forward checks scale their tolerance with the count, and close at 1e8.

    A residual is an aggregate over the point's contracts, so ``check_av_roll_fwd`` holds
    it to ``roll_fwd_tol() x max(policy_count(), 1)`` and ``check_pols_roll_fwd`` to
    ``1e-12 x max(policy_count(), 1)``, where ``RILA_US_S``'s tolerances are fixed: at the
    counts the other tests use, about one contract, the residuals are far inside either.
    So every committed row is projected from a copy where it counts :data:`CHECK_COUNT`
    times as many: both checks close on every one, and on some row each residual exceeds
    the fixed tolerance it would have had, the count's ``1e-12`` and the Account Value's
    ``roll_fwd_tol()``, one part in a billion of the purchase payment, so the scaling is
    what closes each.
    """
    table = _committed()
    model = _read(_sec_inputs(tmp_path, table.assign(
        policy_count=CHECK_COUNT * table["policy_count"])), "scaled_checks")
    worst_count = worst_av = 0.0
    try:
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            assert p.policy_count() == pytest.approx(CHECK_COUNT * table.at[point_id,
                                                                           "policy_count"])
            assert p.check_av_roll_fwd() and p.check_pols_roll_fwd(), point_id
            months = range(p.proj_len())
            worst_count = max([worst_count,
                               *(abs(p.check_pols_roll_fwd_resid(t)) for t in months)])
            worst_av = max([worst_av, *(abs(p.check_av_roll_fwd_resid(t)) / p.roll_fwd_tol()
                                        for t in months)])
            _release(model, key)
    finally:
        model.close()
    assert worst_count > 1e-12 and worst_av > 1.0, (worst_count, worst_av)


def test_acquisition_and_the_premium_fall_on_new_business_only(sec_model, tmp_path):
    """The purchase payment, its tax and acquisition, per contract issued, at issue.

    On every committed point the premium is ``premium x policy_count()`` in the issue
    month, ``t = -duration_mth``, and so is the payment credited to the Investment Amount,
    and each is 0 in every other month: ``t = 0`` on the twins, ``t = 13`` on the anchor
    issued 13 months on, and never on a point already in force, though on the valuation
    clock its row 0 is ``t = 0``.  On a copy whose twin of the anchor, the anchor in force
    71 months and the anchor issued 13 months on each count 2.5 contracts, read with premium
    tax switched on before it computes anything, what ``expenses(t)`` holds beyond
    maintenance is ``(0.06 x P + 200) x policy_count()``, 15,500.00, in the issue month and
    0 in every other, and the premium tax is 2% of the premium there: a charge per model
    point, which every shipped point's count of one would pass, fails.  ``RILA_US_S``
    charges both on the count at issue, so the twins agree with S at any count, and T1
    needs no S point to count one contract.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        issue = -int(table.at[point_id, "duration_mth"])
        issued = [p.policy_count() if t == issue else 0.0 for t in range(p.proj_len())]
        assert [p.premiums(t) for t in range(p.proj_len())] == [
            p.premium_pp() * n for n in issued], point_id
        assert [p.prem_to_av(t) for t in range(p.proj_len())] == [
            p.premium_pp() * n for n in issued], point_id
    committed = _committed()
    cases = (("twin", 1, 0), ("derived", 1, 71), ("future", 1, -13))
    labels = [_label(committed, *case) for case in cases]
    fresh = _read_edited(tmp_path, _set("policy_count", labels, 2.5), "acquisition",
                         {"premium_tax_rate": 0.02})
    try:
        for case in cases:
            p = _row(fresh, *case)
            ts = range(p.proj_len())
            maintenance = [p.expense_maint / 12.0 * p.inflation_factor(t) * p.pols_if(t)
                           for t in ts]
            acq = [p.expenses(t) - m for t, m in zip(ts, maintenance)]
            issue = -p.duration_mth_init()
            per = p.expense_acq_rate * p.premium_pp() + p.expense_acq_fixed
            expected = [per * p.policy_count() if t == issue else 0.0 for t in ts]
            assert acq == pytest.approx(expected, abs=1e-9), case
            assert [p.premium_taxes(t) for t in ts] == [
                0.02 * p.premiums(t) for t in ts], case
            if case[0] != "derived":
                assert (p.policy_count(), acq[issue]) == (2.5, pytest.approx(15500.0)), case
                assert p.premium_taxes(issue) == pytest.approx(5000.0)
            else:
                assert not any(acq) and not any(p.premiums(t) for t in ts), case
    finally:
        fresh.close()


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, and only the rule under test
# refuses it.  The checks run over the whole table as it is read, in Data, and the message
# names the file it read and the column or every point at fault.  A blank cell reads as
# NaN, and so does a text cell once the checks coerce the column to numbers, so each is
# refused as a count, a duration, an age, a rate, a balance or a market value that is not
# a number.  The repeated point_id holds another contract under the same label, as a bad
# extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 16, the anchor in the last month of its first term,
# with every term-start column; 17, the worked example's programme on the anniversary after
# its withdrawal, its remainder partly used; 18, the nge_reset point mid-term after its
# first renewal, with its re-solved cap; 19, the same at that renewal, its term-start
# columns blank; 20, the Step option on a one-year term mid-term; 22, the uncapped option
# mid-term; 23, the notional family in its last covered month; 24, the anchor issued 13
# months on; and the twins 1, the anchor, and 13, nge_reset.
#
# Where the docs say a check runs before another, its case sits on a row the later check
# would refuse differently, so that a check moved after it fails its case: term_years 2.5
# on row 20, where the presence rule, reading the term as written, would refuse its
# term-start columns, and nge_reset on row 20, where it would ask for a cap.  The rules
# that hold a window of contract months are tested at both ends, refused just inside here
# and in REFUSED, the anniversary rule and proj_len()'s remainder rule at month 12, where
# each starts, and the first-term rule at month 1, its first, as at 71 and, on a one-year
# term, at 11, its last, and accepted just outside
# (test_the_edges_of_the_in_force_interface_are_accepted).  And each tolerance is pinned
# from both sides, refused just past it here or in REFUSED and accepted just inside it
# there (USLIB-SEC-PLAN.md §5.2, T5, precised at M10): the cents of the return-of-premium
# base, the anniversary rule and the remainder rule within two cents past, and the cent the
# first year's rules and the first term's hold the remainder, the base on either side of
# the premium and the two accounts to a tenth of a cent past, each read a part of a cent
# inside it.  Each case is read by a model of its own, its file named by a Reference set
# before the model computes anything (the malformed fixture), so a {file} in a message is
# the case's own filename.

_NUMBER = "{file}: {c} must be a number, zero or more; it is not at point_id [{p}]"
_SIGNED = ("{file}: {c} must be a finite number, of either sign, the interim value being "
           "able to fall below 0; it is not at point_id [{p}]")
_FRACTION = ("{file}: {c} must be a fraction, 0 or more and below 1, the strike of a put "
             "below the index at the Term Start Date; it is not at point_id [{p}]")
_RANGE = "{file}: {c} must be blank or a number {what}; it is not at point_id [{p}]"
_NOT_YET = ("{file}: {c} must be 0 on a policy not yet in force, duration_mth 0 or less, "
            "which enters with its purchase payment in its issue month; it is not at "
            "point_id [{p}]")
_GIVEN = ("{file}: {c} must be given where the term under way began before the valuation "
          "month; it is blank at point_id [{p}]")
_BLANK = ("{file}: {c} must be blank unless the term under way began before the valuation "
          "month: at or after it the projection reads the term start from the scenario; "
          "it is given at point_id [{p}]")
_CAP_GIVEN = ("{file}: cap_rate_init must be given where the term under way began at a "
              "renewal under nge_reset before the valuation month; it is blank at point_id "
              "[{p}]")
_CAP_BLANK = ("{file}: cap_rate_init must be blank unless the term under way began at a "
              "renewal under nge_reset before the valuation month: elsewhere the cap is "
              "the declared cap, or is re-solved from the scenario; it is given at "
              "point_id [{p}]")
_FIRST_TERM = ("{file}: {c} must be 0 before the first Term End Date, duration_mth 1 to 12 "
               "x term_years - 1: only a term end transfers to it; it is not at point_id "
               "[{p}]")
_REMAIN = ("{file}: free_wd_remain_init must be 0 in the first contract year, duration_mth "
           "1 to 11, which has no free withdrawal amount; it is not at point_id [{p}]")
_PREV = ("{file}: av_pp_prev_anniv_init must be the premium in the first contract year, "
         "duration_mth 1 to 11, the year having opened at issue; it is not at point_id "
         "[{p}]")
_RENEWAL = ("{file}: on a renewal valuation, duration_mth a multiple of 12 x term_years, "
            "av_pp_init must be inv_amt_pp_init + fixed_acct_pp_init + "
            "holding_acct_pp_init, to two and a half cents: the month before closed a "
            "term, where the interim value is the Investment Amount; it is not at "
            "point_id [{p}]")
_ANNIVERSARY = ("{file}: on an anniversary valuation av_pp_prev_anniv_init, the account "
                "value before the anniversary's withdrawal, must be at least av_pp_init, "
                "the value after it, to a cent; it is not at point_id [{p}]")
_SCENARIO = ("{file}: scenario_id must name a scenario of market_scenario_sec.csv that "
             "sets its levels by the point's first month on the books, t = 0 or its issue "
             "month if later; it does not at point_id [{p}]")
_MORTALITY = ("{file}: mort_table.csv must rate the point's sex at its attained age in its "
              "first month on the books; it does not at point_id [{p}]")
_WHAT = {"index_at_term_start_init": "above 0, the index level index_perf divides by",
         "mvr_at_term_start_init": "above -1, 1 + mvr dividing the interim value's rate "
                                   "adjustment",
         "risk_free_at_term_start_init": "above -1, an annual effective rate",
         "div_yield_at_term_start_init": "above -1, an annual effective rate",
         "impl_vol_at_term_start_init": "above 0, the volatility the option prices "
                                        "divide by"}

# A term-start value each fixing may take where it is given, inside its range.
_FIXED = {"index_at_term_start_init": 140.0, "mvr_at_term_start_init": 0.05,
          "risk_free_at_term_start_init": 0.04, "div_yield_at_term_start_init": 0.02,
          "impl_vol_at_term_start_init": 0.2}


def _m(template, **values):
    """A message of the templates above, ``{file}`` left for the case to fill."""
    return template.format(file="{file}", **values)


def _moved(point, month, **columns):
    """An edit that moves row ``point`` to policy month ``month`` and sets ``columns``."""
    def edit(table):
        table = _set("duration_mth", [point], month)(table)
        for column, value in columns.items():
            table = _set(column, [point], value)(table)
        return table
    return edit


def _in_first_year(point, month, **columns):
    """Row ``point`` moved into its first contract year, at policy month ``month``.

    The committed table has no row in its first contract year, so this makes one, at
    either end of it, month 1 or month 11, where an off-by-one check would let the row
    through.  The year opened at issue, so its state is set as ``Data`` requires there:
    the base the purchase payment, nothing in either account, no free withdrawal amount;
    and then ``columns`` alone are set.  The row keeps its term-start columns, a term
    begun at issue before the valuation month.  Every other check still passes, so the
    one under test is the first to fail.
    """
    def edit(table):
        state = {"av_pp_prev_anniv_init": table.at[point, "premium"],
                 "fixed_acct_pp_init": 0.0, "holding_acct_pp_init": 0.0,
                 "free_wd_remain_init": 0.0}
        return _moved(point, month, **{**state, **columns})(table)
    return edit


MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[16]].assign(policy_id="RILA-900099")]),
     "{file}: point_id [16] appears more than once"),
    ("a negative count", _set("policy_count", [16], -0.1),
     _m(_NUMBER, c="policy_count", p=16)),
    ("a count written as text", _set("policy_count", [17], "abc"),
     _m(_NUMBER, c="policy_count", p=17)),
    ("a blank count", _set("policy_count", [18], NAN), _m(_NUMBER, c="policy_count", p=18)),
    ("an infinite count", _set("policy_count", [19], float("inf")),
     _m(_NUMBER, c="policy_count", p=19)),
    ("two bad counts", _both(_set("policy_count", [16], -1.0),
                             _set("policy_count", [24], "x")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id "
     "[16, 24]"),
    ("a fractional duration", _set("duration_mth", [20], 30.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [20]"),
    ("a blank duration", _set("duration_mth", [21], NAN),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [21]"),
    ("a duration written as text", _set("duration_mth", [22], "forty"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [22]"),
    ("issued beyond the horizon", _set("duration_mth", [24], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [24]"),
    *[(f"an issue age {how}", _set("age_at_entry", [p], v),
       f"{{file}}: age_at_entry must be a whole number of years, 0 or more; it is not at "
       f"point_id [{p}]")
      for how, p, v in (("fractional", 16, 60.5), ("below 0", 24, -1),
                        ("written as text", 17, "sixty"))],
    *[(f"a term {how}", _set("term_years", [p], v),
       f"{{file}}: term_years must be a whole number of years, 1 or more: the term clock "
       f"counts months modulo 12 x term_years; it is not at point_id [{p}]")
      for how, p, v in (("of 2.5 years, mid-term", 20, 2.5), ("of 0 years", 1, 0),
                        ("written as text", 16, "six"))],
    *[(f"a premium {how}", _set("premium", [p], v),
       f"{{file}}: premium must be a number above 0, the purchase payment; it is not at "
       f"point_id [{p}]")
      for how, p, v in (("of 0", 1, 0.0), ("written as text", 16, "x"))],
    ("a buffer of 1", _set("buffer", [16], 1.0), _m(_FRACTION, c="buffer", p=16)),
    ("a negative floor", _set("floor_rate", [17], -0.1),
     _m(_FRACTION, c="floor_rate", p=17)),
    ("a participation of 0", _set("participation", [16], 0.0),
     "{file}: participation must be a number above 0, by which the cap's strike divides; "
     "it is not at point_id [16]"),
    *[(f"a declared cap {how}", _set("declared_cap", [p], v),
       f"{{file}}: declared_cap must be blank, for an uncapped option, or a number, zero "
       f"or more; it is not at point_id [{p}]")
      for how, p, v in (("written as text", 16, "x"), ("below 0", 17, -0.1))],
    ("a blank declared step", _set("declared_step", [20], NAN),
     _m(_NUMBER, c="declared_step", p=20)),
    ("a negative declared edge", _set("declared_edge", [16], -0.01),
     _m(_NUMBER, c="declared_edge", p=16)),
    ("a blank behavioural rate", _set("wd_rate_ann", [17], NAN),
     _m(_NUMBER, c="wd_rate_ann", p=17)),
    *[(f"nge_reset {how}", _set("nge_reset", [p], v),
       f"{{file}}: nge_reset must be True or False, a flag; it is not at point_id [{p}]")
      for how, p, v in (("written yes", 1, "yes"), ("blank", 16, NAN))],
    *[(f"nge_reset on {what}", _set("nge_reset", [p], True),
       f"{{file}}: nge_reset re-solves the cap of a capped Cap Rate option, crediting_type "
       f"CAP with declared_cap given; it is set at point_id [{p}], where there is no cap "
       f"to re-solve or the solver would price the Cap Rate portfolio for another "
       f"crediting method")
      for what, p in (("the Step option, past a renewal", 20),
                      ("the uncapped option", 22))],
    *[(f"{c} {how}", _set(c, [p], v), _m(_NUMBER, c=c, p=p))
      for c, how, p, v in (("inv_amt_pp_init", "below 0", 16, -1.0),
                           ("fixed_acct_pp_init", "written as text", 20, "x"),
                           ("holding_acct_pp_init", "infinite", 20, float("inf")),
                           ("free_wd_remain_init", "below 0", 17, -1.0),
                           ("rop_pp_init", "blank", 16, NAN))],
    *[(f"{c} {how}", _set(c, [p], v), _m(_SIGNED, c=c, p=p))
      for c, how, p, v in (("av_pp_init", "infinite", 16, float("inf")),
                           ("av_pp_prev_anniv_init", "blank", 17, NAN))],
    *[(f"{c} {how}", _set(c, [16], v), _m(_RANGE, c=c, what=_WHAT[c], p=16))
      for c, how, v in (("index_at_term_start_init", "of 0", 0.0),
                        ("mvr_at_term_start_init", "of -1", -1.0),
                        ("risk_free_at_term_start_init", "below -1", -1.5),
                        ("div_yield_at_term_start_init", "written as text", "x"),
                        ("impl_vol_at_term_start_init", "of 0", 0.0))],
    ("cap_rate_init written as text", _set("cap_rate_init", [18], "x"),
     "{file}: cap_rate_init must be blank or a finite number; it is not at point_id [18]"),
    *[(f"{c} held on {what}", _set(c, [p], 100.0), _m(_NOT_YET, c=c, p=p))
      for c, (what, p) in zip(AMOUNTS, itertools.cycle((("future business", 24),
                                                        ("new business", 1))))],
    *[(f"{c} blank mid-term", _set(c, [16], NAN), _m(_GIVEN, c=c, p=16)) for c in _FIXED],
    *[(f"{c} given at a renewal at the valuation month", _set(c, [19], v),
       _m(_BLANK, c=c, p=19)) for c, v in _FIXED.items()],
    ("a term-start index given on new business",
     _set("index_at_term_start_init", [1], 100.0),
     _m(_BLANK, c="index_at_term_start_init", p=1)),
    ("the twins carrying the term-start market entering month 0, M7's form",
     lambda t: t.assign(**{c: t[c].where(t["row_kind"] != "twin", v)
                           for c, v in _FIXED.items()}),
     "{file}: index_at_term_start_init must be blank unless the term under way began "
     "before the valuation month: at or after it the projection reads the term start from "
     "the scenario; it is given at point_id [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, "
     "14, 15]"),
    ("no cap after a renewal under nge_reset", _set("cap_rate_init", [18], NAN),
     _m(_CAP_GIVEN, p=18)),
    ("a cap in an initial term", _set("cap_rate_init", [16], 1.0), _m(_CAP_BLANK, p=16)),
    ("a cap at a renewal at the valuation month", _set("cap_rate_init", [19], 1.0),
     _m(_CAP_BLANK, p=19)),
    ("a contract in force holding nothing", _set("inv_amt_pp_init", [16], 0.0),
     "{file}: a contract in force must hold an investment amount or an account balance; "
     "none does at point_id [16]"),
    ("a return-of-premium base two cents above the premium",
     _set("rop_pp_init", [16], 100000.02),
     "{file}: rop_pp_init must be at most the premium, to a cent: withdrawals only reduce "
     "the return-of-premium base; it is not at point_id [16]"),
    *[(f"a free withdrawal amount in the first contract year, month {month}",
       _in_first_year(16, month, free_wd_remain_init=100.0), _m(_REMAIN, p=16))
      for month in (1, 11)],
    *[(f"a base two cents off the premium in the first contract year, month {month}",
       _in_first_year(16, month, av_pp_prev_anniv_init=100000.02), _m(_PREV, p=16))
      for month in (1, 11)],
    *[(f"{c} before the first term end, month {month}", _moved(22, month, **{c: 1.0}),
       _m(_FIRST_TERM, c=c, p=22))
      for c, month in (("fixed_acct_pp_init", 40), ("holding_acct_pp_init", 71))],
    ("a fixed account on a one-year term at month 11",
     _in_first_year(20, 11, fixed_acct_pp_init=1.0),
     _m(_FIRST_TERM, c="fixed_acct_pp_init", p=20)),
    ("a fixed account on a one-year term at month 1",
     _in_first_year(20, 1, fixed_acct_pp_init=1.0),
     _m(_FIRST_TERM, c="fixed_acct_pp_init", p=20)),
    ("a free withdrawal amount just over a cent in the first contract year",
     _in_first_year(16, 1, free_wd_remain_init=0.011), _m(_REMAIN, p=16)),
    *[(f"a base just over a cent {side} the premium in the first contract year",
       _in_first_year(16, month, av_pp_prev_anniv_init=100000.0 + gap), _m(_PREV, p=16))
      for side, month, gap in (("above", 11, 0.011), ("below", 1, -0.011))],
    ("a holding account just over a cent at month 1, the first term's first",
     _in_first_year(22, 1, holding_acct_pp_init=0.011),
     _m(_FIRST_TERM, c="holding_acct_pp_init", p=22)),
    ("a fixed account just over a cent in the first term's last month",
     _moved(22, 71, fixed_acct_pp_init=0.011),
     _m(_FIRST_TERM, c="fixed_acct_pp_init", p=22)),
    ("an account value three cents above the balances at a renewal",
     _plus("av_pp_init", [19], 0.03), _m(_RENEWAL, p=19)),
    ("an account value three cents below the balances at a renewal",
     _plus("av_pp_init", [19], -0.03), _m(_RENEWAL, p=19)),
    ("a base two cents below the account value on an anniversary",
     lambda t: _set("av_pp_prev_anniv_init", [17], t.at[17, "av_pp_init"] - 0.02)(t),
     _m(_ANNIVERSARY, p=17)),
    ("a base two cents below the account value on the first anniversary",
     _moved(16, 12, av_pp_prev_anniv_init=98999.98, av_pp_init=99000.0,
            free_wd_remain_init=0.0), _m(_ANNIVERSARY, p=16)),
    ("a scenario the scenarios lack", _set("scenario_id", [16], "nope"),
     _m(_SCENARIO, p=16)),
    ("a programme the programmes lack", _set("wd_schedule_id", [16], "nope"),
     "{file}: wd_schedule_id must name a programme of withdrawal_table.csv; it does not at "
     "point_id [16]"),
    ("a term the guaranteed minimums lack", _set("term_years", [1], 2),
     "{file}: term_years must be a term of guar_min_rate_table.csv; it is not at point_id "
     "[1]"),
    ("a sex the mortality table lacks", _set("sex", [1], "X"), _m(_MORTALITY, p=1)),
    ("an issue age below the mortality table's first", _set("age_at_entry", [1], 30),
     _m(_MORTALITY, p=1)),
    ("an attained age past the mortality table's last", _set("age_at_entry", [24], 121),
     _m(_MORTALITY, p=24)),
    ("a cap below the guaranteed minimum", _set("cap_rate_init", [18], 0.05),
     "{file}: cap_rate_init must be at least guar_min_cap for its term in "
     "guar_min_rate_table.csv; it is not at point_id [18]"),
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """A copy of the product directory holding every table of :data:`MALFORMED`.

    Each case is a file of its own beside one copy of the model, ``{case: filename}``.
    The cases do not share a model: each reads one of its own, with ``model_point_file``
    pointed at its file before the model computes anything (:func:`_read`).
    """
    root = tmp_path_factory.mktemp("malformed")
    files = {}
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"malformed_{number:02d}_sec.csv"
        temp_inputs(root, model_path(SEC), model_points=edit(_committed()),
                    model_point_file=files[case])
    return root / SEC, files


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(malformed, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5).

    And a projection, which reads the table at its first ``model_point()``, meets the same
    refusal before it computes a number: the base ``Projection``'s default point is asked
    for its ``result_cf()``, since a table that is refused gives no keys to ask by.
    """
    folder, files = malformed
    model = _read(folder, "malformed", data={"model_point_file": files[case]})
    try:
        _refused(model.Data.model_point_table, message.format(file=files[case]))
        _refused(model.Projection.result_cf, message.format(file=files[case]))
    finally:
        model.close()


# The points a rule of the product refuses, each in proj_len() and each by name, with the
# Reference whose change admits it.  A point at its Maturity Date and one past it: the
# notional family moved from its last covered month, 119, to 120, the first month the
# rule refuses, an anniversary, so its base is set to its account value, as Data's
# anniversary rule requires there, and to 121.  And a free withdrawal amount unused above
# the contract year's, where the rule holds from the first anniversary on: on the worked
# example's programme on its anniversary, whose year's allowance is 8,480.31, by 519.69
# and by 0.019, just over the cent the rule allows; and on the uncapped option moved to
# its first anniversary, month 12, the first month the rule reads, two cents over an
# allowance of 10,000.00.  As (case, point_id, edit, message, the admitting Reference).
REFUSED = [
    ("at the Maturity Date", 23,
     lambda t: _moved(23, 120, av_pp_prev_anniv_init=t.at[23, "av_pp_init"])(t),
     "point_id 23: duration_mth 120 is at or past the maturity date, policy month 120; "
     "the contract has matured", {"maturity_age": 91}),
    ("past the Maturity Date", 23, _set("duration_mth", [23], 121),
     "point_id 23: duration_mth 121 is at or past the maturity date, policy month 120; "
     "the contract has matured", {"maturity_age": 91}),
    ("a free withdrawal amount above the year's", 17,
     _set("free_wd_remain_init", [17], 9000.0),
     "point_id 17: free_wd_remain_init 9000.0 is more than the contract year's free "
     "withdrawal amount, free_wd_rate x av_pp_prev_anniv_init, 8480.31",
     {"free_wd_rate": 0.11}),
    ("a free withdrawal amount just over a cent above the year's", 17,
     _set("free_wd_remain_init", [17], 8480.33),
     "point_id 17: free_wd_remain_init 8480.33 is more than the contract year's free "
     "withdrawal amount, free_wd_rate x av_pp_prev_anniv_init, 8480.31",
     {"free_wd_rate": 0.11}),
    ("a free withdrawal amount above the year's on the first anniversary", 22,
     _moved(22, 12, av_pp_prev_anniv_init=100000.0, av_pp_init=99000.0,
            free_wd_remain_init=10000.02),
     "point_id 22: free_wd_remain_init 10000.02 is more than the contract year's free "
     "withdrawal amount, free_wd_rate x av_pp_prev_anniv_init, 10000.00",
     {"free_wd_rate": 0.11}),
]


@pytest.mark.parametrize("case, point_id, edit, message, refs", REFUSED,
                         ids=[c[0] for c in REFUSED])
def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path, case, point_id, edit,
                                                       message, refs):
    """A point no rule of the table refuses, but a rule of the product does (D6, T5).

    Each rule needs a ``Projection`` Reference, ``maturity_age`` and ``maturity_min_years``
    or ``free_wd_rate``, so ``Data`` cannot check it: the table reads, and the point is
    refused where its frame is defined, on its first projection, by name, rather than
    projecting nothing or a remainder no year allows.  The other points of the same table
    project.  And each is admitted once the Reference moves the bound, set on a model read
    afresh before it computes anything: at a maturity age of 91 the notional family's
    cover runs to policy month 132, and at a free rate of 11% the programme's year allows
    9,328.34, and the uncapped option's first anniversary 11,000.00.
    """
    table = edit(_committed())
    folder = _sec_inputs(tmp_path, table)
    model = _read(folder, "refused")
    try:
        assert len(model.Data.model_point_table()) == len(table)
        _refused(_point(model, point_id).result_cf, message)
        assert len(_point(model, 16).result_cf()) == 289
    finally:
        model.close()
    admitted = _read(folder, "admitted", refs)
    try:
        df = _point(admitted, point_id).result_cf()
        assert len(df) > 0 and np.isfinite(df.to_numpy()).all()
    finally:
        admitted.close()


def test_run_sec_block_refuses_before_printing(tmp_path):
    """``run_sec.py --block`` asks every point for its frame before it projects any.

    The point at its Maturity Date is refused in ``proj_len()`` when the block reaches
    it, which a loop over the block would do only after projecting the points before it.
    So the runner asks every point for its frame first: run beside the refused table, as
    an extract relabelled and reversed (:func:`_relabelled`) holds it, it exits non-zero,
    prints nothing, and names the point by its label, 123, not by its position.
    """
    extract = _relabelled(REFUSED[0][2](_committed()))
    folder = _sec_inputs(tmp_path, extract)
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert REFUSED[0][3].replace("point_id 23", "point_id 123") in done.stderr.decode(
        errors="replace")


# What the decodes refuse, as (case, the table's edit, the point, its message): each text
# value a projection branches on.  The decodes read the model point's columns and the
# cells that branch on them raise RILA_US_S's own message wherever the projection first
# meets an unknown value, and only the decode under test refuses each case.  Data validates
# no text column but nge_reset, a flag.
UNDECODABLE = [
    ("an unknown crediting method", _set("crediting_type", [1], "BUFFER"), 1,
     "invalid crediting_type"),
    ("an unknown interim-value family", _set("iv_family", [1], "hybrid"), 1,
     "invalid iv_family"),
    ("an unknown amortization rule", _set("amort_rule", [16], "linear"), 16,
     "invalid amort_rule"),
]


@pytest.mark.parametrize("case, edit, point_id, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_an_undecodable_value_is_refused_where_the_projection_meets_it(tmp_path, case,
                                                                        edit, point_id,
                                                                        message):
    """An invalid switch raises ``ValueError`` with S's message, not a quiet default.

    Each case is read by a model of its own, from a copy of the inputs with the one fault.
    The table reads, because these are rules of the projection, not of the in-force
    interface, and the point's projection meets the fault on its way to its first number.
    A decode that read an unknown crediting method as the Cap Rate method's, or an unknown
    family as the portfolio's, would project a contract no one wrote; the ten decodes are
    each a bool, so an unknown value is none of them, and the branch that finds none raises.
    """
    model = _read_edited(tmp_path, edit, "undecodable")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point_id).result_cf, message)
        decodes = [_point(model, point_id).cells[name]() for name in DECODES]
        assert all(type(d) is bool for d in decodes)
    finally:
        model.close()


def _at(df, file, key_columns, key):
    """The one row of an assumption table at ``key``, as a mask of ``df``'s rows."""
    at = pd.Series(True, index=df.index)
    for c, v in zip(key_columns, key):
        at &= df[c] == v
    assert at.sum() == 1, (file, key)
    return at


def _cell(file, key_columns, key, column, value):
    """An edit of an assumption table that writes ``value`` into ``column`` at ``key``."""
    def edit(df):
        at = _at(df, file, key_columns, key)
        cells = df[column].astype(object)
        return df.assign(**{column: cells.where(~at, value)})
    return edit


def _row_again(file, key_columns, key):
    """An edit of an assumption table that writes the row at ``key`` a second time, last."""
    def edit(df):
        return pd.concat([df, df[_at(df, file, key_columns, key)]], ignore_index=True)
    return edit


def _row_gone(file, key_columns, key):
    """An edit of an assumption table that leaves out the row at ``key``."""
    def edit(df):
        return df[~_at(df, file, key_columns, key)]
    return edit


# Where the cases below write.  The mortality table runs age 40 M, 40 F, 41 M, ... so the
# male rate at 70, which the anchor's life reaches, is line 62, and the female row at 120,
# the last line, 163, which no join reads, so that a fault in its key leaves no gap; the
# anchor's scenario opens S's companion at line 2; the surrender charge of contract year 3
# is line 5; the one-year term's floors are line 2; the lapse table's year 7 is line 3;
# the charged programme's row is line 4.
_MORT, _MORT_LAST = ("age", "sex"), (120, "F")
_SCEN = ("scenario_id", "month_end")
_BAD = (("blank", NAN), ("written as text", "x"), ("infinite", float("inf")))

TABLES = [
    *[(f"mort_table.csv: an age {how}", "mort_table.csv",
       _cell("mort_table.csv", _MORT, _MORT_LAST, "age", v),
       "mort_table.csv: age must be a whole number; it is not on line [163]")
      for how, v in (("blank", NAN), ("written as text", "x"), ("fractional", 120.5))],
    ("mort_table.csv: a sex neither M nor F", "mort_table.csv",
     _cell("mort_table.csv", _MORT, _MORT_LAST, "sex", "U"),
     "mort_table.csv: sex must be M or F; it is not on line [163]"),
    ("mort_table.csv: an age and sex on two rows", "mort_table.csv",
     _row_again("mort_table.csv", _MORT, (70, "M")),
     "mort_table.csv: each age and sex must have one row; age 70, sex M is on line "
     "[62, 164]"),
    ("mort_table.csv: an age missing", "mort_table.csv",
     _row_gone("mort_table.csv", _MORT, (70, "M")),
     "mort_table.csv: the ages of each sex must run one row an age, without a gap; no "
     "line holds age 70 of sex M"),
    *[(f"mort_table.csv: a rate {how}", "mort_table.csv",
       _cell("mort_table.csv", _MORT, (70, "M"), "mort_rate", v),
       "mort_table.csv: mort_rate must be a finite number, zero or more; it is not on "
       "line [62]")
      for how, v in (*_BAD, ("below 0", -0.1))],
    ("market_scenario_sec.csv: a blank scenario", SCENARIOS,
     _cell(SCENARIOS, _SCEN, ("up", 0), "scenario_id", NAN),
     "market_scenario_sec.csv: scenario_id must not be blank; it is on line [2]"),
    *[(f"market_scenario_sec.csv: a month {how}", SCENARIOS,
       _cell(SCENARIOS, _SCEN, ("up", 36), "month_end", v),
       "market_scenario_sec.csv: month_end must be a whole number, 0 or more; it is not on "
       "line [3]")
      for how, v in (("written as text", "x"), ("below 0", -1), ("fractional", 12.5))],
    ("market_scenario_sec.csv: a month set twice", SCENARIOS,
     _row_again(SCENARIOS, _SCEN, ("up", 36)),
     "market_scenario_sec.csv: a scenario must set one level a month end; one sets two on "
     "lines [3, 29]"),
    *[(f"market_scenario_sec.csv: {c} {how}", SCENARIOS,
       _cell(SCENARIOS, _SCEN, ("up", 36), c, v),
       f"market_scenario_sec.csv: {c} must be a finite number above {low}; it is not on "
       f"line [3]")
      for c, how, v, low in (("index_level", "of 0", 0.0, "0"),
                             ("impl_vol", "blank", NAN, "0"),
                             ("mvr", "of -1", -1.0, "-1"),
                             ("risk_free", "written as text", "x", "-1"),
                             ("div_yield", "infinite", float("inf"), "-1"))],
    ("surr_charge_table.csv: a year written as text", "surr_charge_table.csv",
     _cell("surr_charge_table.csv", ("contract_year",), (3,), "contract_year", "x"),
     "surr_charge_table.csv: contract_year must be a whole number; it is not on line [5]"),
    ("surr_charge_table.csv: a year missing", "surr_charge_table.csv",
     _row_gone("surr_charge_table.csv", ("contract_year",), (3,)),
     "surr_charge_table.csv: the contract years must run from 0, one row a year, without a "
     "gap or a repeat; they are [0, 1, 2, 4, 5, 6] on lines [2, 3, 4, 5, 6, 7]"),
    ("surr_charge_table.csv: a year on two rows", "surr_charge_table.csv",
     _row_again("surr_charge_table.csv", ("contract_year",), (3,)),
     "surr_charge_table.csv: the contract years must run from 0, one row a year, without a "
     "gap or a repeat; they are [0, 1, 2, 3, 4, 5, 6, 3] on lines [2, 3, 4, 5, 6, 7, 8, "
     "9]"),
    *[(f"surr_charge_table.csv: a charge {how}", "surr_charge_table.csv",
       _cell("surr_charge_table.csv", ("contract_year",), (3,), "surr_charge_rate", v),
       "surr_charge_table.csv: surr_charge_rate must be a fraction, 0 to 1; it is not on "
       "line [5]")
      for how, v in (("blank", NAN), ("of 1.5", 1.5))],
    *[(f"guar_min_rate_table.csv: a term {how}", "guar_min_rate_table.csv",
       _cell("guar_min_rate_table.csv", ("term_years",), (1,), "term_years", v),
       "guar_min_rate_table.csv: term_years must be a whole number, 1 or more; it is not "
       "on line [2]")
      for how, v in (("of 0", 0), ("written as text", "x"))],
    ("guar_min_rate_table.csv: a term on two rows", "guar_min_rate_table.csv",
     _row_again("guar_min_rate_table.csv", ("term_years",), (6,)),
     "guar_min_rate_table.csv: each term must have one row; one has two on lines [4, 5]"),
    *[(f"guar_min_rate_table.csv: {c} {how}", "guar_min_rate_table.csv",
       _cell("guar_min_rate_table.csv", ("term_years",), (1,), c, v),
       f"guar_min_rate_table.csv: {c} must be a finite number, zero or more; it is not on "
       f"line [2]")
      for c, how, v in (("guar_min_cap", "blank", NAN), ("guar_min_step", "below 0", -0.01),
                        ("guar_min_edge", "infinite", float("inf")))],
    ("lapse_table.csv: a year written as text", "lapse_table.csv",
     _cell("lapse_table.csv", ("contract_year",), (7,), "contract_year", "x"),
     "lapse_table.csv: contract_year must be a whole number; it is not on line [3]"),
    ("lapse_table.csv: a year on two rows", "lapse_table.csv",
     _row_again("lapse_table.csv", ("contract_year",), (7,)),
     "lapse_table.csv: each contract year must have one row; one has two on lines [3, 5]"),
    ("lapse_table.csv: no year 1", "lapse_table.csv",
     _row_gone("lapse_table.csv", ("contract_year",), (1,)),
     "lapse_table.csv: the first contract year must be 1, so that every contract year has "
     "a rate; it is 7"),
    *[(f"lapse_table.csv: a rate {how}", "lapse_table.csv",
       _cell("lapse_table.csv", ("contract_year",), (7,), "lapse_rate_base", v),
       "lapse_table.csv: lapse_rate_base must be a fraction, 0 to 1; it is not on line [3]")
      for how, v in (("blank", NAN), ("of 1.2", 1.2))],
    ("withdrawal_table.csv: a blank programme", "withdrawal_table.csv",
     _cell("withdrawal_table.csv", ("wd_schedule_id",), ("charged",), "wd_schedule_id",
           NAN),
     "withdrawal_table.csv: wd_schedule_id must not be blank; it is on line [4]"),
    ("withdrawal_table.csv: a fractional month", "withdrawal_table.csv",
     _cell("withdrawal_table.csv", ("wd_schedule_id",), ("charged",), "month_end", 23.5),
     "withdrawal_table.csv: month_end must be a whole number, 0 or more; it is not on line "
     "[4]"),
    ("withdrawal_table.csv: a withdrawal twice at one month", "withdrawal_table.csv",
     _row_again("withdrawal_table.csv", ("wd_schedule_id",), ("charged",)),
     "withdrawal_table.csv: a programme must withdraw once a month end at most; one "
     "withdraws twice on lines [4, 5]"),
    *[(f"withdrawal_table.csv: an amount {how}", "withdrawal_table.csv",
       _cell("withdrawal_table.csv", ("wd_schedule_id",), ("charged",), "wd_amount", v),
       "withdrawal_table.csv: wd_amount must be a finite number, zero or more; it is not "
       "on line [4]")
      for how, v in (("below 0", -1.0), ("written as text", "x"))],
]

# Each table's reader, RILA_US_S's and unchanged, and the count cell beside it, which
# checks it.  Every refusal is read through the twin of S point 14 too, whose projection
# reads every table: its charged withdrawal, its anniversaries and its maturity.
TABLE_READERS = {"mort_table.csv": ("mort_table", "mort_table_count"),
                 SCENARIOS: ("market_scenario", "market_scenario_count"),
                 "surr_charge_table.csv": ("surr_charge_table", "surr_charge_count"),
                 "guar_min_rate_table.csv": ("guar_min_rate_table", "guar_min_rate_count"),
                 "lapse_table.csv": ("lapse_table", "lapse_table_count"),
                 "withdrawal_table.csv": ("withdrawal_table", "withdrawal_count")}


@pytest.mark.parametrize("case, file, edit, message", TABLES, ids=[c[0] for c in TABLES])
def test_a_malformed_assumption_table_is_refused_naming_the_file(tmp_path, case, file,
                                                                 edit, message):
    """Each assumption table's count cell refuses a key or a value the joins cannot use,
    and a projection meets the refusal.

    Five of the tables are ``RILA_US_S``'s files, read in place by both models, and the
    scenarios this model's own companion, so each case is read by a model of its own from
    a copy of the inputs with the one fault.  ``RILA_US_S``'s reader, unchanged, reads the
    table as it stands; the count cell beside it refuses it, naming the file, the column
    and the lines at fault (§7.1, *Precised at M3*, item 9); and the twin of S point 14,
    whose projection reads every table, meets the same refusal in its ``result_cf()``
    before it computes a number, because each join asks the count before it reads a value.
    ``RILA_US_S`` reads a key written as text as a key no join matches, so that every
    surrender charge or withdrawal is silently zero, and its step lookups compare text
    with a month and raise Python's own message, naming no file.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), {file: edit}), "table")
    reader, count = TABLE_READERS[file]
    try:
        assert len(model.Data.cells[reader]()) > 0
        _refused(model.Data.cells[count], message)
        _refused(model.Projection[_file_key(model, _committed(), 14)].result_cf, message)
    finally:
        model.close()


def _file_key(model, table, label):
    """The ``Projection`` key of row ``label`` of ``table``, a table the model may refuse.

    A refused table gives no ``point_keys``, so the key is taken from the file, the way
    ``run_sec.py`` takes one: the row's position on a model indexed by position, and its
    label otherwise.
    """
    if model.Projection.parameters == ("idx",):
        return list(table.index).index(label)
    return label


# Every table's keys written as floats, as one blank or one 70.0 in a key column makes
# pandas read it.
FLOAT_KEYS = {
    "mort_table.csv": lambda df: df.assign(age=df["age"].astype(float)),
    SCENARIOS: lambda df: df.assign(month_end=df["month_end"].astype(float)),
    "surr_charge_table.csv": lambda df: df.assign(
        contract_year=df["contract_year"].astype(float)),
    "guar_min_rate_table.csv": lambda df: df.assign(
        term_years=df["term_years"].astype(float)),
    "lapse_table.csv": lambda df: df.assign(
        contract_year=df["contract_year"].astype(float)),
    "withdrawal_table.csv": lambda df: df.assign(month_end=df["month_end"].astype(float)),
}


def test_an_assumption_tables_keys_written_as_floats_are_read_by_value(sec_model,
                                                                       tmp_path):
    """An assumption table whose keys are written as floats is read as the same table.

    The joins match each key by value, as ``RILA_US_S``'s do, and each count cell reads
    the keys by value too.  On a copy of the inputs whose six tables carry every age,
    contract year, term and month written as a float (:data:`FLOAT_KEYS`), the readers
    read the keys as floats, each count cell counts what it counts on the committed
    tables, and the twins of the anchor, the worked example's programme, the Step option,
    the legacy family and the charged programme, the anchor in force and its programme in
    force project exactly what the committed model projects: between them they read every
    table at every kind of key.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), FLOAT_KEYS), "float_keys")
    try:
        assert model.Data.mort_table().index.levels[0].dtype == "float64"
        assert model.Data.withdrawal_table().index.levels[1].dtype == "float64"
        for name in ("mort_table_count", "market_scenario_count", "surr_charge_count",
                     "guar_min_rate_count", "lapse_table_count", "withdrawal_count"):
            assert model.Data.cells[name]() == sec_model.Data.cells[name](), name
        for point_id in (1, 2, 4, 9, 14, 16, 17):
            for report in REPORTS:
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0.0, atol=0.0) == [], (point_id, report)
    finally:
        model.close()


def test_a_points_scenario_must_set_its_levels_by_its_first_month_on_the_books(tmp_path):
    """A scenario may start after ``t = 0``, but not after a point that runs on it starts.

    The scenario is a step function of the valuation month, and a point reads it from the
    first month it is on the books, ``t = 0`` or its issue month if later, so the file may
    hold a scenario for business issued later that sets no level before then: the
    committed future row's own copy, ``up-F13``, starts at 13, its issue month.  Moved on
    a month, each copy is refused for the rows that run on it, by ``Data`` and by a
    projection, where ``RILA_US_S``'s step function finds no level and raises Python's own
    error: S's ``up`` at 1, for the seven twins on it; the uncapped option in force 40
    months's ``down-M40`` at 1; and ``up-F13`` at 14, for the anchor issued 13 months on.
    Each table is read on a model of its own.
    """
    def moved(sid, to):
        def edit(df):
            first = df.index[df["scenario_id"] == sid][0]
            assert df.at[first, "month_end"] == to - 1
            return df.assign(month_end=df["month_end"].where(df.index != first, to))
        return {SCENARIOS: edit}

    committed = _committed()
    for sid, to, refused in (("up", 1, [1, 3, 4, 10, 11, 13, 14]), ("down-M40", 1, [22]),
                             ("up-F13", 14, [24])):
        model = _read(_sec_inputs(tmp_path / sid, committed, moved(sid, to)), "scenario")
        try:
            text = _SCENARIO.format(file=TABLE, p=", ".join(map(str, refused)))
            _refused(model.Data.model_point_table, text)
            _refused(model.Projection[_file_key(model, committed, refused[0])].result_cf,
                     text)
        finally:
            model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a contract issued later, and 0 refuses all.

    The committed table's one future point is issued 13 months on.  It reads at the shipped
    120 months and at 13, the shortest horizon that admits it, where it also projects, and
    is refused at 12, by name.  At 0 the model takes no future new business, D4's fallback
    for a product that cannot support it, and the message says so.  A negative horizon is
    itself refused.  Each value is set on a model read for it, before the model computes
    anything.
    """
    future = _label(_committed(), "future", 1, -13)
    later = (f"{TABLE}: duration_mth must be -12 or more, a policy issued at most 12 "
             f"months after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    negative = "future_horizon_mth must be 0 months or more, not -1"
    folder = _sec_inputs(tmp_path, _committed())
    shipped = _read(folder, "horizon")
    try:
        assert shipped.Data.future_horizon_mth == 120
    finally:
        shipped.close()
    for horizon, refusal in ((120, None), (13, None), (12, later), (0, no_future),
                             (-1, negative)):
        model = _read(folder, "horizon", data={"future_horizon_mth": horizon})
        try:
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(_committed()), horizon
                if horizon == 13:
                    late = _point(model, future)
                    assert (late.proj_len(), late.pols_new_biz(13)) == (373, 1.0)
                    assert late.result_cf()["premiums"].iloc[13] == 100000.0
            else:
                _refused(model.Data.model_point_table, refusal)
        finally:
            model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_files_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` and ``market_scenario_sec.csv`` are what RILA_US_S and
    its inputs generate today.

    Every row and column of both files, the text cells and the opening-state columns
    included: an edit to an S row or a scenario the files copy or re-base, or to an S
    formula a row's state is read from, fails here until ``python tools/gen_sec_points.py
    RILA_US_SEC`` regenerates them, in the same commit.  Text and integers compare exactly,
    and a float by its value, to 1e-12, because the text the writer picks for a computed
    float depends on the platform's parser (§5.2).  The re-based scenarios are the spec's
    one companion, so both files are checked.
    """
    assert set(SPEC.companions) == {SCENARIOS}
    assert check_generated(SEC, s_model=s_model) == []


def test_every_committed_row_continues_its_s_point(sec_model, s_model):
    """Each derived and future row of the committed table is its S point from its month on.

    T6 holds the committed table to what the generator makes of ``RILA_US_S``, each float to
    1e-12 absolute and relative, which pins the notional family's count in its last month,
    0.33, only to about 3e-12 of itself and says nothing of what the model makes of a row.
    So each derived and future row is projected too, at the shipped assumptions, and
    compared with its S point from the row's ``source_mth`` on (:func:`_continues_s`): the
    four reports frame by frame, and every other cell of S's at every argument S cached, to
    1e-9 relative with no absolute floor, the roll-forward residuals at the floor.  The
    eight rows restated in force skip what the splice skips, and the anchor issued 13
    months on, its ``source_mth`` -13, what T3 skips.  Each reads its own copy of its
    scenario from the committed companion, so the comparison holds the re-based scenarios
    too.  The shipped expense inflation runs from issue in S and from the valuation date
    here (D7), so the cells it moves are left out; the inflation test holds them.
    """
    table = sec_model.Data.model_point_table()
    rows = table.index[table["row_kind"] != "twin"]
    assert set(table.loc[rows, "row_kind"]) == {"derived", "future"} and len(rows) == 9
    for point_id in rows:
        month = int(table.at[point_id, "source_mth"])
        later = table.at[point_id, "row_kind"] == "future"
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        found = _continues_s(s, p, month, FUTURE_EXEMPT if later else SPLICE_EXEMPT)
        assert found == [], point_id


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin the two coincide, and its contracts enter as new business at ``t = 0``.  The
    anchor in force 71 months is in contract year 6 at attained age 65 at ``t = 0``, in the
    last month of its first term, which ends there, and has 289 months of cover left, to
    its Maturity Date at the end of policy month 359; the year it is in closes at its
    month end, so a surrender there settles in contract year 7.  The notional family in
    its last covered month has a one-month frame, in which its survivors mature.  The
    anchor issued 13 months on has nothing in force and nothing to do before ``t = 13``,
    and its contract year is 0 before its issue, which no table is read at.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 359)] == [0, 1, 359]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.policy_id() == "RILA-000001"
    anchor = _row(sec_model, "derived", 1, 71)
    assert (anchor.duration_mth(0), anchor.duration(0), anchor.policy_year(0),
            anchor.age(0), anchor.term_elapsed_mth(0), anchor.term_start_month(0)) == (
        71, 5, 7, 65, 72, 0)
    assert anchor.is_term_end(0) and anchor.is_anniv(0) and not anchor.is_term_end(1)
    assert (anchor.maturity_mth(), anchor.proj_len(), anchor.policy_id()) == (
        360, 289, "RILA-000001-M71")
    assert anchor.is_active(288) and not anchor.is_active(289)
    assert anchor.duration_mth(288) == anchor.maturity_mth() - 1
    last = _row(sec_model, "derived", 7, 119)
    assert (last.proj_len(), last.age(0), last.policy_year(0)) == (1, 89, 11)
    assert last.pols_maturity(0) == last.pols_if_at(0, _code(last, "AFT_DECR")) > 0.0
    assert last.pols_if_at(1, _code(last, "BEF_NB")) == 0.0
    fut = _row(sec_model, "future", 1, -13)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-13, 13, 373)
    assert [fut.policy_year(t) for t in range(14)] == [0] * 12 + [1, 1]
    assert not fut.is_active(12) and fut.is_active(13)
    assert (fut.pols_if_init(), fut.pols_new_biz(13), fut.pols_if(13)) == (0.0, 1.0, 1.0)
    assert (fut.premiums(12), fut.premiums(13)) == (0.0, 100000.0)


def _close_or_blank(a, b):
    """Whether two opening-state values agree: both blank, or equal to 1e-12."""
    if a != a or b != b:
        return a != a and b != b
    return a == pytest.approx(b, rel=1e-12, abs=1e-12)


def test_the_opening_state_is_what_s_carries_into_the_valuation_month(sec_model, s_model):
    """Each committed row opens with S's state at its month, and nothing else.

    For each derived row, restated from S point ``p`` at its month ``d``, each of the
    thirteen opening-state columns is what the spec's extractor reads off S at ``d``, to
    1e-12 relative, because a computed float may come back from the CSV within two ulps:
    each amount S's close of month ``d - 1``, the base S's ``"BEF_WD"`` value at the
    anniversary month on or before ``d``, and each term-start value S's market on the Term
    Start Date of the term under way, blank where that term starts at ``d`` itself, and
    the cap S's in force at ``d`` on the reset point after a renewal, blank elsewhere.  And
    its scenario is S's re-based to ``d``, ``{id}-M{d}``, whose level at ``t = 0`` is S's
    at ``d``.  The twins and the future row hold S's opening at issue: every amount 0,
    every fixing blank, the twins on S's own scenario and the future row on its copy moved
    13 months on.
    """
    table = sec_model.Data.model_point_table()
    for point_id in table.index:
        p, kind = _point(sec_model, point_id), table.at[point_id, "row_kind"]
        s = _source(s_model, table, point_id)
        if kind == "derived":
            d = int(table.at[point_id, "source_mth"])
            want = {c: SPEC.state[c](s, d) for c in STATE}
            assert p.scenario_id() == f"{s.scenario_id()}-M{d}", point_id
            for name in ("index_level", "mvr", "risk_free", "div_yield", "impl_vol"):
                assert (p.market_state(0, _market(p, name))
                        == s.market_state(d, name)), (point_id, name)
        else:
            want = {c: (0.0 if c in AMOUNTS else NAN) for c in STATE}
            sid = s.scenario_id() if kind == "twin" else f"{s.scenario_id()}-F13"
            assert p.scenario_id() == sid, point_id
        for column, value in want.items():
            assert _close_or_blank(p.cells[column](), value), (point_id, column,
                                                               p.cells[column](), value)


def test_each_opening_state_column_shows_on_a_committed_row(sec_model, tmp_path):
    """Each column, changed alone, changes what its committed row gives at ``t = 0``.

    A column the projection never read, or read where another belongs, would pass every
    test that leaves the column as generated.  So each is changed on a copy of a committed
    row that reads it, appended to the committed table under an id of its own, and the
    copy's month 0 is asserted against the row's:

    * the Investment Amount, halved on the anchor at its term end, halves the credited
      amount, ``IA (1 + g)``, 70,000 rather than 140,000;
    * the Fixed and Holding Accounts, each 1,000 more on the Step option a month into a
      term, raise the account's value before the withdrawal by 1,000 accrued a month at
      the account rate;
    * the Account Value, 1,000 less on the anchor, raises the month's investment return by
      1,000, which it is measured from;
    * the base, 90,000 on the programme valued on its anniversary, is the year's base, and
      its allowance 9,000;
    * the remainder, 1,000 there, is the free withdrawal amount at ``t = 0``, and shelters
      more of a surrender;
    * the return-of-premium base, 95,000 there, where the account value is below it, is
      the death benefit;
    * the term-start index, 90 on the uncapped option mid-term, is ``I_s`` in the index
      performance, and the term-start Market Value Rate, 6%, in the interim value's rate
      adjustment;
    * the term-start risk-free rate, dividend yield and volatility, each moved, reprice
      the term's budget, which the option portfolio under the market of its start is;
    * the cap, 90% on the reset point after its renewal, is the cap in force.
    """
    committed = _committed()
    p16, p17, p18, p20, p22 = (_label(committed, "derived", s, d) for s, d in
                               ((1, 71), (2, 36), (13, 80), (4, 30), (12, 40)))
    copies = {
        "inv_amt": (p16, {"inv_amt_pp_init": committed.at[p16, "inv_amt_pp_init"] / 2}),
        "fixed": (p20, {"fixed_acct_pp_init": committed.at[p20, "fixed_acct_pp_init"]
                        + 1000.0}),
        "holding": (p20, {"holding_acct_pp_init": 1000.0}),
        "av": (p16, {"av_pp_init": committed.at[p16, "av_pp_init"] - 1000.0}),
        "base": (p17, {"av_pp_prev_anniv_init": 90000.0}),
        "remain": (p17, {"free_wd_remain_init": 1000.0}),
        "rop": (p17, {"rop_pp_init": 95000.0}),
        "index": (p22, {"index_at_term_start_init": 90.0}),
        "mvr": (p22, {"mvr_at_term_start_init": 0.06}),
        "risk_free": (p22, {"risk_free_at_term_start_init": 0.05}),
        "div_yield": (p22, {"div_yield_at_term_start_init": 0.03}),
        "impl_vol": (p22, {"impl_vol_at_term_start_init": 0.25}),
        "cap": (p18, {"cap_rate_init": 0.9}),
    }
    labels = {what: 100 + i for i, what in enumerate(copies, start=1)}
    rows = [committed.loc[[point]].assign(**changes).set_axis([labels[what]])
            for what, (point, changes) in copies.items()]
    table = pd.concat([committed, *rows]).rename_axis("point_id")
    model = _read(_sec_inputs(tmp_path, table), "shown")
    try:
        c = {what: _point(model, label) for what, label in labels.items()}
        r16, r17, r18, r20, r22 = (_point(sec_model, p) for p in (p16, p17, p18, p20, p22))
        assert r16.inv_amt_pp_at(0, _code(r16, "BEF_ROLL")) == pytest.approx(
            140000.0, rel=1e-12)
        assert c["inv_amt"].inv_amt_pp_at(0, _code(r16, "BEF_ROLL")) == pytest.approx(
            70000.0,
                                                                         rel=1e-12)
        month = (1.0 + r20.acct_rate()) ** (1.0 / 12.0)
        for what, cell in (("fixed", "fixed_acct_pp_at"),
                           ("holding", "holding_acct_pp_at")):
            wd = _code(r20, "BEF_WD")
            gap = c[what].cells[cell](0, wd) - r20.cells[cell](0, wd)
            assert gap == pytest.approx(1000.0 * month, rel=1e-9), what
        assert c["av"].inv_income_pp(0) - r16.inv_income_pp(0) == pytest.approx(
            1000.0, rel=1e-9)
        assert (c["base"].free_wd_base(0), c["base"].free_wd_allow(0)) == (
            90000.0, pytest.approx(9000.0, rel=1e-12))
        assert r17.free_wd_base(0) == r17.av_pp_prev_anniv_init() != 90000.0
        assert (c["remain"].free_wd_avail(0), r17.free_wd_avail(0)) == (
            1000.0, r17.free_wd_remain_init())
        assert c["remain"].surr_charge_pp(0) < r17.surr_charge_pp(0)
        assert r17.av_pp(0) < r17.rop_pp(0) == r17.rop_pp_init() == r17.death_ben_pp(0)
        assert c["rop"].rop_pp(0) == c["rop"].death_ben_pp(0) == 95000.0
        assert c["index"].index_perf(0) == c["index"].index_level(0) / 90.0 - 1.0
        assert r22.index_perf(0) == r22.index_level(0) / 100.0 - 1.0
        assert c["mvr"].mva_factor(0) == ((1.0 + 0.06) / (1.0 + c["mvr"].mvr(0))) ** c[
            "mvr"].tau(0)
        assert c["mvr"].mva_factor(0) != r22.mva_factor(0)
        for what in ("risk_free", "div_yield", "impl_vol"):
            assert c[what].opt_budget(0) != r22.opt_budget(0), what
            assert c[what].cells[f"{what}_at_term_start"](0) == copies[what][1][
                f"{what}_at_term_start_init"], what
        assert (c["cap"].cap_rate(0), r18.cap_rate(0)) == (0.9, r18.cap_rate_init())
        for p in c.values():
            assert np.isfinite(p.result_cf().to_numpy()).all()
    finally:
        model.close()


def test_a_term_begun_before_the_valuation_date_reads_its_start_from_the_model_point(
        sec_model, s_model, sec_read):
    """``I_s``, the Market Value Rate and the pricing market of a term begun before
    ``t = 0`` are the model point's.

    The anchor in force 71 months is in the last month of its first term, which ends at
    ``t = 0`` at the worked example's +40%: its credit is ``140 / 100 - 1``, the index at
    the month end on its re-based scenario over ``I_s`` from its column, 100, under the cap
    of 100%, and its interim value at the term end is the Investment Amount credited,
    140,000.00, S's at month 71.  The re-based scenario's own level at ``t = 0``, 120, S's
    at month 71, is never read for ``I_s``: no scenario re-based to the valuation date holds
    the Term Start Date's level, which is why the column exists.  The renewed term starts
    in the frame, at ``t = 1``, and reads its start from the scenario there, 140.  On the
    uncapped option in force 40 months, mid-term on the down path, the interim value's rate
    adjustment is ``((1 + r_0) / (1 + r(t))) ** tau(t)`` with ``r_0`` the column's 4%,
    and the option budget the one struck at the term's start, S's at month 40, under the
    column's market.
    """
    anchor = _row(sec_model, "derived", 1, 71)
    s1 = _point(s_model, 1)
    assert anchor.index_at_term_start_init() == 100.0 == anchor.index_at_term_start(0)
    level = _market(anchor, "index_level")
    assert anchor.index_level(0) == 140.0 and anchor.market_state(0, level) == 120.0
    assert anchor.credit_rate_term(0) == 140.0 / 100.0 - 1.0 == s1.credit_rate_term(71)
    roll = _code(anchor, "BEF_ROLL")
    assert anchor.interim_value_pp_at(0, roll) == pytest.approx(140000.0, abs=1e-9)
    assert anchor.interim_value_pp_at(0, roll) == s1.interim_value_pp_at(71, "BEF_ROLL")
    label = _label(sec_model.Data.model_point_table(), "derived", 1, 71)
    keys = sec_read[1]["market"][label]
    assert (0, level) not in keys and min(t for t, _ in keys) == 1
    assert anchor.index_at_term_start(1) == 140.0 == anchor.market_state(1, level)
    mid = _row(sec_model, "derived", 12, 40)
    s12 = _point(s_model, 12)
    assert (mid.mvr_at_term_start(0), mid.mvr(0)) == (0.04, 0.05)
    assert mid.mva_factor(0) == ((1.0 + 0.04) / (1.0 + 0.05)) ** mid.tau(0)
    assert mid.mva_factor(0) == s12.mva_factor(40)
    assert mid.opt_budget(0) == s12.opt_budget(40)
    label = _label(sec_model.Data.model_point_table(), "derived", 12, 40)
    assert not set(FIXINGS[:5]) & sec_read[1]["unread"][label]


def test_the_cap_re_solved_at_a_renewal_is_read_until_the_next(events, spliced, sec_model,
                                                              tmp_path):
    """A cap fixed at a past renewal is the column's; one fixed in the frame, the
    scenario's.

    On the one-year term under ``nge_reset`` valued at policy month 30, on the splice's
    inputs, the term under way began at the renewal at 24, where S re-solved its cap from
    the market of that date: ``cap_rate(t)`` is the column's for ``t`` 0 to 5, S's
    ``cap_rate(30)`` bit for bit, and at ``t = 6`` the renewal at 36 re-solves it from the
    row's scenario, S's ``cap_rate(36)`` bit for bit.  With the column at 20%, set on a copy
    of the row, the cap is 20% for ``t`` 0 to 5, the option the interim value prices is
    struck there, so the interim value moves in each of those months, while the cap at the
    renewal and everything from it on is the row's: the term's credit binds neither cap.
    On the reset point valued 80 months in, whose term runs to its Maturity Date, the
    column is the cap in every month of the frame.
    """
    s = spliced[0]
    key = _row_key(events, "derived", 17, 30)
    try:
        p, s17 = projection(events, key), _point(s, 17)
        caps = [p.cap_rate(t) for t in range(7)]
        assert caps[:6] == [p.cap_rate_init()] * 6 == [s17.cap_rate(30)] * 6
        assert caps[6] == s17.cap_rate(36) != caps[0]
        assert p.term_start_month(6) == 36 and p.term_start_month(5) == 24
        table = events.Data.model_point_table()
        label = table.index[table["policy_id"] == "RILA-900017-M30"][0]
        row = table.loc[[label]].assign(cap_rate_init=0.20)
        folder = temp_inputs(tmp_path, model_path(SEC), model_points=row,
                             model_point_file=TABLE,
                             edits={SCENARIOS: pd.read_csv(spliced[2].parent / SCENARIOS),
                                    **SPLICED_EDITS})
        fresh = _read(folder, "cap", SPLICED_REFS)
        try:
            q = _point(fresh, label)
            assert [q.cap_rate(t) for t in range(6)] == [0.20] * 6
            assert q.cap_rate(6) == caps[6]
            assert all(q.interim_value_pp_at(t, _code(q, "BEF_ROLL"))
                       != p.interim_value_pp_at(t, _code(p, "BEF_ROLL")) for t in range(5))
            assert q.credit_rate_term(5) == p.credit_rate_term(5) < 0.20
            assert frame_mismatches(p.result_av().loc[5:], q.result_av().loc[5:],
                                    rtol=1e-12, atol=0.0) == []
        finally:
            fresh.close()
    finally:
        _release(events, key, collect=True)
    reset = _row(sec_model, "derived", 13, 80)
    assert [reset.cap_rate(t) for t in range(reset.proj_len())] == (
        [reset.cap_rate_init()] * reset.proj_len())


def test_a_renewal_at_the_valuation_date_reads_its_term_from_the_scenario(sec_model,
                                                                          s_model,
                                                                          sec_read):
    """A term that starts at the valuation month reads its start, and re-solves its cap,
    from the scenario.

    The reset point valued at policy month 72 renews at ``t = 0``: its five term-start
    columns and its cap are blank, the sweep read none of them, its ``I_s`` is its
    re-based scenario's level at ``t = 0``, 140, S's at month 72, and its cap is re-solved
    there on that market, S's ``cap_rate(72)`` bit for bit, which is the cap the row
    valued at 80 carries in its column.
    """
    renewal = _row(sec_model, "derived", 13, 72)
    label = _label(sec_model.Data.model_point_table(), "derived", 13, 72)
    assert all(renewal.cells[c]() != renewal.cells[c]() for c in FIXINGS)
    assert set(FIXINGS) <= sec_read[1]["unread"][label]
    s13 = _point(s_model, 13)
    assert (renewal.index_at_term_start(0)
            == renewal.market_state(0, _market(renewal, "index_level")) == 140.0)
    assert renewal.index_at_term_start(0) == s13.index_at_term_start(72)
    assert renewal.cap_rate(0) == s13.cap_rate(72) == renewal.declared_cap_solved(0)
    assert renewal.cap_rate(0) == pytest.approx(
        _row(sec_model, "derived", 13, 80).cap_rate_init(), rel=1e-12)


def test_the_year_under_way_reads_its_free_withdrawal_state(sec_model):
    """The base of the year under way, and what is left of its allowance, are opening state.

    The worked example's programme valued on the anniversary after its 8,000 withdrawal,
    policy month 36, opens contract year 4 at ``t = 0``: the year's base is the column's,
    the account value before that withdrawal, 84,803.11, its allowance 8,480.31, and what
    the withdrawal left of it, 480.31, is the free withdrawal amount through ``t = 10``; a
    surrender at the end of month 0 bears 5% of the account value above that remainder,
    3,820.47.  At ``t = 11`` the anniversary at policy month 48 resets it to 10% of the
    frame's own account value before withdrawals there, 77,847.64.  The anchor valued in
    the last month of its sixth year carries its year's whole allowance, 11,998.16, 10% of
    its base, but its month 0 ends on an anniversary, which resets the allowance at once,
    from the frame's own account value before withdrawals at ``t = 0``: neither column is
    the free withdrawal amount or the base it reads, which only ``proj_len()``'s rule
    reads.
    """
    p17 = _row(sec_model, "derived", 2, 36)
    assert p17.av_pp_prev_anniv_init() == pytest.approx(84803.11, abs=0.005)
    assert [p17.free_wd_base(t) for t in range(11)] == [p17.av_pp_prev_anniv_init()] * 11
    assert [p17.free_wd_allow(t) for t in range(11)] == [
        p17.free_wd_rate * p17.av_pp_prev_anniv_init()] * 11
    assert p17.free_wd_allow(0) == pytest.approx(8480.31, abs=0.005)
    assert [p17.free_wd_avail(t) for t in range(11)] == [p17.free_wd_remain_init()] * 11
    assert p17.free_wd_remain_init() == pytest.approx(480.31, abs=0.005)
    assert p17.surr_charge_rate(0) == 0.05
    assert p17.surr_charge_pp(0) == pytest.approx(
        0.05 * (p17.av_pp(0) - p17.free_wd_remain_init()), rel=1e-12)
    assert p17.surr_charge_pp(0) == pytest.approx(3820.47, abs=0.005)
    assert p17.is_anniv(11) and p17.free_wd_base(11) == p17.av_pp_at(
        11, _code(p17, "BEF_WD"))
    assert p17.free_wd_base(11) == pytest.approx(77847.64, abs=0.005)
    assert p17.free_wd_avail(11) == p17.free_wd_allow(11) == pytest.approx(7784.76,
                                                                          abs=0.005)
    p16 = _row(sec_model, "derived", 1, 71)
    assert p16.free_wd_remain_init() == pytest.approx(
        p16.free_wd_rate * p16.av_pp_prev_anniv_init(), rel=1e-12)
    assert p16.free_wd_remain_init() == pytest.approx(11998.16, abs=0.005)
    assert p16.is_anniv(0) and p16.free_wd_avail(0) == p16.free_wd_allow(0)
    assert p16.free_wd_avail(0) != p16.free_wd_remain_init()
    assert (p16.free_wd_base(0) == p16.av_pp_at(0, _code(p16, "BEF_WD"))
            != p16.av_pp_prev_anniv_init())


def test_withdrawals_stay_on_the_policy_clock(sec_model, events):
    """A withdrawal programme falls where the contract has it, however old the contract.

    *withdrawal_table.csv*'s month end is a policy month end (D7): the worked example's
    8,000 at month end 36 falls in policy month 35, at ``t = 35`` on its twin and nowhere on
    the row valued at 36, whose opening state carries it.  The charged programme's 20,000 at
    month end 24, on the splice's inputs, falls at ``t = 0`` on the row valued at policy
    month 23 and at ``t = 36`` on the contract issued 13 months on.  No other month
    withdraws, the behavioural rule being off on both.
    """
    def taken(model, case):
        key = _row_key(model, *case)
        p = projection(model, key)
        return [(t, p.wd_pp(t)) for t in range(p.proj_len()) if p.wd_pp(t) != 0.0]

    assert taken(sec_model, ("twin", 2, 0)) == [(35, 8000.0)]
    assert taken(sec_model, ("derived", 2, 36)) == []
    try:
        assert taken(events, ("derived", 14, 23)) == [(0, 20000.0)]
        assert taken(events, ("future", 14, -13)) == [(36, 20000.0)]
    finally:
        for case in (("derived", 14, 23), ("future", 14, -13)):
            _release(events, _row_key(events, *case), collect=True)


def test_the_market_scenario_runs_on_the_valuation_clock(tmp_path):
    """The scenario is a path in calendar time, read at ``t`` on every point alike (D7).

    On a copy of the committed inputs whose anchor in force 71 months runs on S's own
    ``up`` path, as its twin does, both read the same level at the same ``t``, though one is
    71 months older: the market is no fact of the contract.  With a level added to ``up`` at
    month end 5, both see it from ``t = 4``, the month whose end it is, and nothing before;
    the anchor's twin, on its policy clock, is S's anchor, which sees it at its month 4.
    And ``RILA_US_S``'s own ``market_scenario.csv`` is not read: removed from the copy, the
    model reads and projects as before.  Each model is read afresh.
    """
    committed = _committed()
    twin, anchor = _label(committed, "twin", 1, 0), _label(committed, "derived", 1, 71)
    table = _set("scenario_id", [anchor], "up")(committed)

    def step(df):
        row = df[df["scenario_id"] == "up"].iloc[[0]].assign(month_end=5, index_level=103.0)
        return pd.concat([df, row], ignore_index=True)

    plain = _sec_inputs(tmp_path / "plain", table)
    stepped = _sec_inputs(tmp_path / "stepped", table, {SCENARIOS: step})
    (stepped.parent / "market_scenario.csv").unlink()
    before, after = _read(plain, "scenario"), _read(stepped, "scenario_stepped")
    try:
        p, q = _point(before, twin), _point(before, anchor)
        assert [p.index_level(t) for t in range(30)] == [q.index_level(t)
                                                         for t in range(30)]
        p2, q2 = _point(after, twin), _point(after, anchor)
        for old, new in ((p, p2), (q, q2)):
            assert [new.index_level(t) for t in range(4)] == [old.index_level(t)
                                                              for t in range(4)]
            assert [new.index_level(t) for t in range(4, 35)] == [103.0] * 31
            assert [old.index_level(t) for t in range(4, 35)] == [100.0] * 31
        assert np.isfinite(q2.result_cf().to_numpy()).all()
        assert after.Data.market_scenario_file == SCENARIOS
    finally:
        after.close()
        before.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, the factor at ``t`` is ``1.025 ** (t // 12)`` on every committed
    point, whatever its duration: ``RILA_US_S``'s annual steps, moved onto the valuation
    clock.  So the anchor in force 71 months, valued in a year's last month, pays S's month
    ``71 + t`` expenses divided by ``1.025 ** 5`` or ``1.025 ** 6`` as its policy years and
    the valuation years step apart, and the anchor issued 13 months on pays S's month
    ``t - 13`` maintenance, after its issue month, times 1.025 or 1.025 squared, valuation
    years against policy years; on a twin the two clocks give S's expenses in every month.
    This is the only test that sees inflation run on the valuation clock: the splice sets
    the rate to 0, and on a point issued at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.inflation_factor(t) == (1.0 + INFLATION) ** (t // 12), (key, t)
    s1 = _point(s_model, 1)
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.expenses(t) for t in range(360)] == [s1.expenses(t) for t in range(360)]
    for (kind, s_point, month), steps in ((("derived", 1, 71), {5, 6}),
                                          (("future", 1, -13), {-1, -2})):
        p = _row(sec_model, kind, s_point, month)
        ratios = set()
        for t in range(p.t_entry() + (kind == "future"), p.proj_len()):
            ratio = s1.expenses(month + t) / p.expenses(t)
            hit = {n for n in steps
                   if ratio == pytest.approx((1.0 + INFLATION) ** n, rel=1e-12)}
            assert hit, (kind, t, ratio)
            ratios |= hit
        assert ratios == steps, (kind, ratios)


# The cap on mortality
#
# RILA_US_S caps its annual mortality, the A/E factor times the table's rate, at 1, with the
# bound second, min(rate * mort_ae_factor, 1.0), so that its monthly rate stays real at any
# A/E and a lost rate stays NaN, and this model caps it as S does (USLIB-SEC-PLAN.md §5.1,
# step 6), no departure from S.  On the shipped table no covered age's rate comes near 1,
# so the cap binds only under an A/E that takes the rate past it: at 10, on every male
# point at attained age 89, and these are three of the S points on which it binds, each
# with the first S month it binds in, the anchor, the notional family and the uncapped
# option.
CAPPED_AE = 10.0
CAPPED = {1: 348, 7: 108, 12: 96}


def _uncapped_mort_rate(s, m):
    """``RILA_US_S``'s annual mortality in month ``m`` before its cap, from S's cells."""
    rate = float(s.data.mort_table().loc[(s.age(m), s.sex()), "mort_rate"])
    return rate * s.mort_ae_factor


def test_a_capped_annual_mortality_is_the_float_1_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is the float 1.0, and
    the count is exactly 0 after it.

    On a read of ``RILA_US_S`` with ``mort_ae_factor`` set to :data:`CAPPED_AE` before it
    computes anything, and with expense inflation at 0, which runs on the valuation clock
    here and from issue in S (D7), the product of the A/E and the table's rate, from S's own
    cells (:func:`_uncapped_mort_rate`), passes 1 in every month from each point's first
    capped month of :data:`CAPPED` to the end of its frame, and is below 1 in every month
    before.  Both models cap it there: ``mort_rate`` and ``mort_rate_mth`` are
    ``(float, 1.0)`` in each of those months, the type asserted with the value, since
    ``1 == 1.0`` would let an int cap through.  Every contract in force at the start of the
    first capped month dies in it, and the count is exactly 0 in every month after, in both
    models.  Two rows of each point are read, from a table the generator builds out of that
    S read, under the same A/E: its twin and the point restated in force the month before
    the cap, opened with S's count and state there.  On each, every report is float64 and
    finite, and every cell of S's agrees with S at every argument S cached, the capped
    months included, to 1e-9 relative with no absolute floor (:func:`_compared`), since the
    count where the cap binds is near 1e-7.  A cap applied to new business alone fails on
    the rows in force.

    And the cap's order: on reads of both models with ``mort_ae_factor`` set to NaN before
    they compute anything, the anchor's ``mort_rate(0)`` is NaN, not 1.0.  The cap with its
    bound second keeps a lost value a NaN, where ``min(1.0, nan)`` is 1.0 and would pass it
    as certain death in month 0 with every flow finite; so would a cap on the monthly rate.
    No formula is replaced, so the case runs compiled at Phase 2 too.
    """
    refs = {"mort_ae_factor": CAPPED_AE, "inflation_rate": 0.0}
    s = _read(model_path(TWIN), "capped_s", refs)
    sec = None
    try:
        for s_point, first in CAPPED.items():
            sp = _point(s, s_point)
            _sweep(sp)
            end = sp.proj_len()
            assert [m for m in range(end) if sp.mort_rate(m) == 1.0] == list(
                range(first, end)), s_point
            assert all(_uncapped_mort_rate(sp, m) > 1.0 for m in range(first, end))
            assert all(_uncapped_mort_rate(sp, m) < 1.0 for m in range(first))
            for rate in (sp.cells["mort_rate"], sp.cells["mort_rate_mth"]):
                assert [(type(rate(m)), rate(m)) for m in range(first, end)] == (
                    [(float, 1.0)] * (end - first)), (s_point, rate.name)
            assert sp.pols_if(first) > 0.0 and sp.pols_death(first) == sp.pols_if(first)
            assert [sp.pols_if(m) for m in range(first + 1, end)] == (
                [0.0] * (end - first - 1))
        folder = _sec_built(tmp_path, s, [(p, m - 1) for p, m in CAPPED.items()])
        sec = _read(folder, "capped", refs)
        for s_point, first in CAPPED.items():
            sp = _point(s, s_point)
            for case in (("twin", s_point, 0), ("derived", s_point, first - 1)):
                key = _row_key(sec, *case)
                try:
                    p = projection(sec, key)
                    _sweep(p)
                    n, at = p.proj_len(), first - case[2]
                    assert [t for t in range(n) if p.mort_rate(t) == 1.0] == list(
                        range(at, n)), case
                    for rate in (p.cells["mort_rate"], p.cells["mort_rate_mth"]):
                        assert [(type(rate(t)), rate(t)) for t in range(at, n)] == (
                            [(float, 1.0)] * (n - at)), (case, rate.name)
                    assert p.pols_if(at) > 0.0 and p.pols_death(at) == p.pols_if(at), case
                    assert [p.pols_if(t) for t in range(at + 1, n + 1)] == [0.0] * (n - at)
                    for report in REPORTS:
                        frame = p.cells[report]()
                        assert (frame.dtypes == "float64").all(), (case, report)
                        assert np.isfinite(frame.to_numpy()).all(), (case, report)
                    exempt = SPLICE_EXEMPT if case[0] == "derived" else FUTURE_EXEMPT
                    assert _compared(sp, p, case[2], exempt) == [], case
                finally:
                    _release(sec, key, collect=True)
    finally:
        if sec is not None:
            sec.close()
        s.close()
    for path, tag in ((model_path(SEC), "lost"), (model_path(TWIN), "lost_s")):
        lost = _read(path, tag, {"mort_ae_factor": NAN})
        try:
            q = _point(lost, 1).mort_rate(0)
            assert type(q) is float and q != q, f"{tag}: mort_rate(0) is {q!r}"
        finally:
            lost.close()


# The twins the NaN-residual test reads: the anchor, the Step, Edge and Floor options on
# one-year terms, the notional, delta and legacy families, and updated-expiry amortization.
NAN_TWINS = (1, 4, 5, 6, 7, 8, 9, 10)


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``RILA_US_S``'s does.

    Each check asks whether every month's residual is within its tolerance, ``all(abs(r)
    <= tol ...)``, never whether one is beyond it, so a NaN fails it, where ``abs(r) >
    tol`` would pass it.  On a model read with ``mort_ae_factor`` set to NaN before it
    computes anything, every monthly mortality rate is NaN, and with it every count from
    the first month's deaths on: on the twins of each crediting method and each
    interim-value family (:data:`NAN_TWINS`) both roll-forward residuals are NaN in every
    month, and both checks are ``False``.  On a model read with ``trading_cost_rate`` set
    to NaN, the interim value of the portfolio family is NaN in every month a term has left
    to run, and with it the Account Value: on each of those twins of that family the
    Account Value's residual is NaN in every month and its check ``False``; and
    the term-end identity's residual is NaN at every Term End Date, through the Investment
    Amount the month before it, and 0.0 in every other month, and its check ``False``.

    What each check fails is the NaN, and each is asserted only where its residual goes
    NaN: the count's check is not asserted under the trading cost, because ``RILA_US_S``'s
    moneyness factor, ``max(iv_moneyness_floor, iv_ratio)``, with its bound first, loses
    the NaN, and the count's residual stays finite; nor the term-end identity under the
    mortality, which no count reaches.  No formula is replaced, so the case runs compiled
    at Phase 2 too.
    """
    model = _read(model_path(SEC), "nan_mortality", {"mort_ae_factor": NAN})
    try:
        for point_id in NAN_TWINS:
            p = _point(model, point_id)
            for check in CHECKS[:2]:
                resid = [p.cells[f"{check}_resid"](t) for t in range(p.proj_len())]
                assert all(r != r for r in resid), (point_id, check)
                assert p.cells[check]() is False, (point_id, check)
            _release(model, _key(model, point_id))
    finally:
        model.close()
    model = _read(model_path(SEC), "nan_trading", {"trading_cost_rate": NAN})
    try:
        table = model.Data.model_point_table()
        family = [p for p in NAN_TWINS if table.at[p, "iv_family"] == "portfolio"]
        assert len(family) == 5
        for point_id in family:
            p = _point(model, point_id)
            n = p.proj_len()
            av = [p.check_av_roll_fwd_resid(t) for t in range(n)]
            assert all(r != r for r in av) and p.check_av_roll_fwd() is False, point_id
            ends = {t for t in range(n) if p.is_term_end(t)}
            identity = [p.check_term_end_identity_resid(t) for t in range(n)]
            assert ends and all(identity[t] != identity[t] for t in ends), point_id
            assert all(identity[t] == 0.0 for t in range(n) if t not in ends), point_id
            assert p.check_term_end_identity() is False, point_id
            _release(model, _key(model, point_id))
    finally:
        model.close()


# What each monthly cell holds outside cover, before issue and from the month after the
# Maturity Date on, as its docstring says: no count, so no cash flow; no Investment Amount,
# account, Account Value, allowance, withdrawal, charge or benefit; no market value, rate,
# option leg or interim-value factor; and no question about the contract answered yes.  The
# two surrender multipliers are 1.0, their neutral value.  The type is part of the value: an
# amount, a rate or a factor is a float in every branch and a flag a bool, because Phase 2
# types a cell by the values it returns (USLIB-SEC-PLAN.md F3).  The guard test also calls
# every monthly cell with more arguments than t at each of its timings, kinds, buckets,
# legs and markets, each 0.0 (:func:`_monthly_calls`).
OUTSIDE_COVER = {
    "is_active": False, "is_anniv": False, "is_term_end": False,
    "lapse_rate_sc_mult": 1.0, "lapse_iv_mult": 1.0,
    **{name: 0.0 for name in (
        "tau", "index_at_term_start", "mvr_at_term_start", "risk_free_at_term_start",
        "div_yield_at_term_start", "impl_vol_at_term_start", "index_perf",
        "declared_cap_solved", "cap_solved_at_start", "cap_rate", "step_rate",
        "edge_rate", "opt_budget",
        "fixed_leg_yield", "nge_spread_implied", "credit_rate_term", "credit_rate_accrued",
        "budget_amort_factor", "mva_factor", "fixed_proxy_factor", "deriv_proxy_factor",
        "trading_cost_factor", "cap_calc_factor", "iv_factor", "iv_ratio",
        "inv_amt_basis_pp", "inv_amt_pp", "fixed_acct_pp", "holding_acct_pp", "av_pp",
        "inv_income_pp", "free_wd_base", "free_wd_allow", "free_wd_avail",
        "wd_scheduled_pp", "wd_behavioral_pp", "wd_pp", "wd_free_pp", "free_wd_remain",
        "wd_excess_pp", "surr_charge_rate", "wd_charge_pp", "wd_payment_pp",
        "surr_excess_pp", "surr_charge_pp", "surr_value_pp", "rop_pp", "death_ben_pp",
        "mort_rate", "mort_rate_mth", "lapse_rate_base", "lapse_rate", "lapse_rate_mth",
        "term_end_lapse_rate", "pols_if", "pols_new_biz", "pols_death", "pols_lapse_term",
        "pols_lapse", "pols_maturity", "premiums", "prem_to_av_pp", "prem_to_av",
        "withdrawals", "expenses", "premium_taxes", "net_cf", "inv_income", "wd_from_av",
        "av_change", "check_av_roll_fwd_resid", "check_pols_roll_fwd_resid",
        "check_term_end_identity_resid")}}

# The cells a month outside cover may not reach: the clock arithmetic, defined at every
# month but meaning nothing outside cover, and the market readers, which raise before issue
# on a future row's scenario, the copy holding no level there, and read its last level after
# the Maturity Date (SCENARIO_READERS).  The rates and values that read them hold their
# outside-cover values by their own guards, which the guard test asserts first; these have
# none, and no formula may reach them there, nor a caller (USLIB-SEC-PLAN.md F4).  The table
# readers are keyed by an age, a year or a policy month, not a month of the frame, and
# :func:`_contract` bounds their keys instead.
SCENARIO_READERS = ("market_state", "index_level", "mvr", "risk_free", "div_yield",
                    "impl_vol")
IN_COVER_ONLY = ("duration", "duration_eom", "policy_year", "age", "term_elapsed_mth",
                 "term_start_month", *SCENARIO_READERS)

# The two monthly cells defined at every month, inside cover or out: the policy clock, and
# expense inflation, an input on the valuation clock (D7).
EVERY_MONTH = ("duration_mth", "inflation_factor")

# Each argument a monthly cell takes beside t, as Phase 2's full sweep will pass it.
BY_ARGUMENT = {
    "timing": {"pols_if_at": TIMINGS, "av_pp_at": ("BEF_WD", "AFT_WD"),
               "av_at": ("BEF_WD", "AFT_WD"),
               "inv_amt_pp_at": ("BEF_CREDIT", "BEF_ROLL", "BEF_WD", "AFT_WD"),
               "interim_value_pp_at": ("BEF_ROLL", "BEF_WD", "AFT_WD"),
               "fixed_acct_pp_at": ("BEF_WD", "AFT_WD"),
               "holding_acct_pp_at": ("BEF_WD", "AFT_WD")},
    "kind": KINDS, "bucket": BUCKETS}


def _monthly_calls(p, t, scenario=True):
    """Every call of a monthly cell of ``p`` at ``t``: each timing, kind, bucket, leg and
    market, and a cap, an accrual, a spot and a time to expiry of their own.

    With ``scenario=False`` the scenario readers are left out, on a month a future row's
    copy holds no level for.
    """
    calls = []
    for name, cells in p.cells.items():
        params = cells.parameters
        if not params or params[0] != "t" or (not scenario and name in SCENARIO_READERS):
            continue
        if params == ("t",):
            calls.append((name, (t,)))
        elif params == ("t", "timing"):
            labels = BY_ARGUMENT["timing"].get(name, ("BEF_ROLL", "AFT_WD"))
            calls += [(name, (t, _code(p, x))) for x in labels]
        elif params in (("t", "kind"), ("t", "bucket")):
            calls += [(name, (t, _code(p, x))) for x in BY_ARGUMENT[params[1]]]
        elif params == ("t", "leg", "timing"):
            calls += [(name, (t, _code(p, leg), _code(p, x))) for leg in LEGS
                      for x in ("BEF_ROLL", "AFT_WD")]
        elif params == ("t", "leg", "spot", "tau_", "mkt"):
            calls += [(name, (t, _code(p, leg), 100.0, 1.0, _code(p, mkt))) for leg in LEGS
                      for mkt in MARKETS]
        elif params == ("t", "spot", "tau_", "mkt"):
            calls += [(name, (t, 100.0, 1.0, _code(p, mkt))) for mkt in MARKETS]
        elif params in (("t", "accrual"), ("t", "cap")):
            calls += [(name, (t, 0.5))]
        elif params == ("t", "name"):
            calls += [(name, (t, _market(p, field))) for field in (
                "index_level", "mvr", "risk_free", "div_yield", "impl_vol")]
        elif params == ("t", "leg", "basis"):
            calls += [(name, (t, _code(p, leg), _code(p, basis))) for leg in LEGS
                      for basis in BASES]
        elif params == ("t", "basis"):
            calls += [(name, (t, _code(p, basis))) for basis in BASES]
        elif params == ("t", "rule"):
            calls += [(name, (t, _code(p, rule))) for rule in RULES]
        else:
            raise AssertionError(f"{name}{params}: a monthly cell the guard test does not "
                                 f"know how to call")
    return calls


def _guard_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, answers wrongly outside cover.

    In every month before issue and at ``t = proj_len()``, the first month after cover,
    which the count's and the Account Value's look-ahead reads: first every cell of
    :data:`OUTSIDE_COVER` against its value and its type, and every monthly cell with more
    arguments than ``t`` at 0.0, the scenario readers apart; then whether any of
    :data:`IN_COVER_ONLY` was evaluated at a month outside cover on the way, which only a
    fresh ItemSpace can say: ``market_state`` is keyed by a time, and from the first month
    on the books to the end of the last covered one, ``t_entry()`` to ``proj_len()``, is in
    cover.  Then every monthly cell is called at those months, as Phase
    2's full sweep will call it (:func:`_monthly_calls`): none may raise or return a numpy
    type, the scenario readers apart before issue, where they raise, which is asserted; and
    afterwards no monthly cell may hold a month past ``proj_len()``, the last month a
    compiled model's cache holds, nor ``market_state`` an instant past ``proj_len() + 1``,
    the close of the month after cover, which the scenario readers read there; and every
    table reader's keys must lie inside the contract (:func:`_contract`).  A cell that
    raises is reported as a fault too, so the scan goes on.
    """
    faults = []
    entry, end = p.t_entry(), p.proj_len()
    months = [*range(entry), end]

    def call(name, args, want=None):
        try:
            got = p.cells[name](*args)
        except Exception as err:            # reported, so the scan goes on
            faults.append(f"{where}: {name}{args} raised {_raised(err)}")
            return
        if want is not None and (got != want or type(got) is not type(want)):
            faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")
        if isinstance(got, (np.generic, np.ndarray)):
            faults.append(f"{where}: {name}{args} is a numpy {type(got).__name__}")

    for t in months:
        for name, want in OUTSIDE_COVER.items():
            call(name, (t,), want)
        for name, args in _monthly_calls(p, t, scenario=False):
            if len(args) > 1:
                call(name, args, 0.0)
    read = {}
    for name in IN_COVER_ONLY:
        params = p.cells[name].parameters
        keys = [args for args in _cached_args(p.cells[name])
                if not (entry <= args[0] <= end if name == "market_state"
                        else p.is_active(args[params.index("t")]))]
        if keys:
            read[name] = keys[:5]
    if read:
        faults.append(f"{where}: evaluated outside cover: {read}")
    for t in months:
        for name, args in _monthly_calls(p, t, scenario=t >= entry):
            call(name, args)
    for t in range(max(0, entry - 1)):
        for name in SCENARIO_READERS:
            args = (t, _market(p, "index_level")) if name == "market_state" else (t,)
            try:
                p.cells[name](*args)
                faults.append(f"{where}: {name}{args} read a level before issue")
            except Exception:                   # the copy holds no level there
                pass
    past = {}
    for name, cells in p.cells.items():
        if cells.parameters and cells.parameters[0] == "t":
            bound = end + 1 if name == "market_state" else end
            keys = [args for args in _cached_args(cells) if args[0] > bound]
            if keys:
                past[name] = keys[:5]
    if past:
        faults.append(f"{where}: past the frame: {past}")
    return faults + [f"{where}: {line}" for line in _outside_contract(p)]


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no market.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else (:func:`_guard_faults`).  ``is_active``'s docstring promises that outside
    cover no cell reads a market path, a rate or a table at a key the contract does not
    have, so afterwards none of :data:`IN_COVER_ONLY` may hold a key outside cover.  Then
    every monthly cell, guarded or not, is called there, as Phase 2's full sweep will call
    it: each answers, with a Python value, but the scenario readers before issue, whose
    future copy holds no level there and which raise.  Every monthly cell is one of those
    lists, or :data:`EVERY_MONTH`'s, or takes more arguments than ``t``, so that a cell
    added to the model is placed in one.

    The committed table's one point issued after the valuation date is the anchor, a Cap
    Rate option of the portfolio family with no withdrawal, so on it a cell tied to another
    crediting method, family, programme or nge_reset would hold zero before issue, guarded
    or not.  So the same scan runs on the splice's future rows, the core's or, with
    ``USLIB_SEC_FULL=1``, all of them, with the splice's assumptions switched on: the Step
    option, the legacy family, nge_reset and the crash path among them, 13 months on, so
    that a read before issue lands at policy year 0 or lower.  Each row is made afresh
    first and released after.

    And after it no cell holds a month past ``proj_len()``: the Account Value carried out of
    a month and the count's residual read ``t + 1``, and are zero outside cover before they
    read it, so that the month after cover reads nothing past it, which a compiled model's
    cache would not hold (USLIB-SEC-PLAN.md R1).

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    Phase 2 needs them: a table read at a key the contract does not have would wrap round in
    a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    model = _read(model_path(SEC), "cover")
    try:
        monthly = {n for n, c in model.Projection.cells.items()
                   if c.parameters and c.parameters[0] == "t"}
        single = {n for n in monthly if model.Projection.cells[n].parameters == ("t",)}
        placed = {*OUTSIDE_COVER, *IN_COVER_ONLY, *EVERY_MONTH}
        assert single <= placed, f"monthly cells unplaced: {sorted(single - placed)}"
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            faults += _guard_faults(projection(model, key), f"point {point_id}")
    finally:
        model.close()
    sec = spliced[1]
    futures = _selected(FUTURES, CORE_FUTURES)
    for s_point, k in futures:
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key, collect=True)
        try:
            faults += _guard_faults(projection(sec, key), _case_id("future", s_point, -k))
        finally:
            _release(sec, key, collect=True)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_set_apart_edits_move_no_branch():
    """Each input the splice sets apart moves numbers, never which side of a test they fall.

    A value set apart from another so that a mix-up of the two shows must not change which
    branch a comparison takes, or the splice would test other paths than the product's:
    contract year 1's surrender rate, 1.5% against the shipped 2%, is below the bound on
    the surrender rate at both, unshocked in years 1 to 6; contract year 0's withdrawal
    charge, 7.5% against 7%, is above 0 at both, where the charge-expiry year and the
    term-end surrender test it; the Edge floors of the three- and six-year terms, 2.5%
    against 2%, are below the 6% declared edge at both, so the declared edge holds; the
    four shares of a term end sum to 1 at both, 0.80, 0.05, 0.11 and 0.04 against 0.80,
    0.05, 0.15 and 0; and the A/E of 1.05 leaves the cap on mortality idle at every age a
    shipped point covers, as 1.0 does.  The one-year floors, the account rate's floor, the
    moneyness floor and the shock are not set apart: they are set where each binds.
    """
    folder = model_path(TWIN).parent
    model = _read(model_path(TWIN), "apart")
    try:
        refs = dict(model.Projection.refs)
        shock_year = _point(model, 1).lapse_shock_year()
    finally:
        model.close()
    lapse = pd.read_csv(folder / "lapse_table.csv")
    for df in (lapse, _lapse_apart(lapse)):
        year1 = float(df.loc[df["contract_year"] == 1, "lapse_rate_base"].iloc[0])
        assert year1 < refs["lapse_rate_max"] and shock_year == 7
    assert (_lapse_apart(lapse)["lapse_rate_base"].iloc[1:]
            == lapse["lapse_rate_base"].iloc[1:]).all()
    charges = pd.read_csv(folder / "surr_charge_table.csv")
    for df in (charges, _charges_apart(charges)):
        assert float(df.loc[df["contract_year"] == 0, "surr_charge_rate"].iloc[0]) > 0.0
    floors = pd.read_csv(folder / "guar_min_rate_table.csv")
    declared = pd.read_csv(folder / "model_point_table.csv")["declared_edge"]
    for df in (floors, _floors_binding(floors)):
        assert (df.loc[df["term_years"] > 1, "guar_min_edge"] < declared.min()).all()
    names = ("roll_renew_same", "roll_transfer_other", "roll_transfer_fixed",
             "roll_transfer_holding")
    shipped = [refs[r] for r in names]
    shares = [{**refs, **SPLICED_REFS}[r] for r in names]
    assert sum(shipped) == pytest.approx(1.0) == sum(shares)
    assert len(set(shares)) == 4 and shipped[3] == 0.0 < shares[3]
    mortality = pd.read_csv(folder / "mort_table.csv")
    covered = mortality.loc[mortality["age"] < refs["maturity_age"], "mort_rate"]
    for factor in (refs["mort_ae_factor"], SPLICED_REFS["mort_ae_factor"]):
        assert (covered * factor < 1.0).all()


def test_the_points_sum_row_by_row_into_a_block(sec_model, s_model):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The anchor's twin, the anchor restated at month 71 and the anchor issued 13 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..372 and equal S's frame added
    to itself moved 71 months earlier and 13 months later, in every column but the two
    expense inflation moves (:data:`INFLATED`).  A model whose frames sat on the policy
    clock would fail it.  The committed rows are already swept, so it costs a sum.
    """
    cases = (("twin", 1, 0), ("derived", 1, 71), ("future", 1, -13))
    block = pd.concat([_row(sec_model, *case).result_cf() for case in cases]).groupby(
        level="t").sum()
    sdf = _point(s_model, 1).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 71).loc[0:],
                          sdf.set_axis(sdf.index + 13)]).groupby(level=0).sum()
    assert list(block.index) == list(range(373))
    keep = [c for c in sdf.columns if c not in INFLATED]
    assert frame_mismatches(expected, block, columns=keep) == []


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


@pytest.fixture(scope="module")
def committed_runs():
    """``run_sec.py`` on the committed table: each argument list run once, its output kept.

    The runner test and the extract test both read ``run_sec.py 16``, and an interpreter
    that reads the model and projects a point costs seconds.
    """
    runs = {}

    def run(*args):
        if args not in runs:
            runs[args] = _run_sec(model_path(SEC).parent / "run_sec.py", *args)
        return runs[args]
    return run


def _relabelled(table):
    """An administration extract of ``table``: no generator columns, labels moved by 100,
    the rows in reverse order.

    Every generated table numbers its points from 1, in table order, so on it a label and a
    position look alike; on this one they never agree.
    """
    extract = table.drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(extract.index + 100, name="point_id")
    return extract.iloc[::-1]


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path,
                                                                 committed_runs):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them; nor does it number
    its points 1 to n in table order.  Read without them, relabelled 101..124 and reversed
    (:func:`_relabelled`), each point projects what the committed row it was relabelled
    from projects, in the four reports, to 1e-12: every row in force or issued later, and
    the twins that carry each flow beside them (:data:`FLOW_TWINS`).  On every shipped row
    ``source_mth`` equals ``duration_mth``, so a formula that read the one for the other
    would pass every test that leaves ``duration_mth`` as generated.  And ``run_sec.py``,
    run beside that extract, finds point 116 by its label and prints it without saying
    where it came from, every later line as it prints committed point 16, and refuses point
    16, which the extract does not have, naming the labels it does.
    """
    committed = _committed()
    folder = _sec_inputs(tmp_path, _relabelled(committed))
    model = _read(folder, "extract")
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(range(124, 100, -1))
        for point_id in (p + 100 for p in _flow_points(committed)):
            key = _key(model, point_id)
            mine, base = projection(model, key), _point(sec_model, point_id - 100)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (point_id, report)
            _release(model, key)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out, base = _run_sec(runner, "116").splitlines(), committed_runs("16").splitlines()
    assert out[0] == ("model point 116: RILA-000001-M71 - M60 premium 100,000, one 6-year "
                      "CAP option, buffer 10%")
    assert out[1:] == base[1:]
    refused = _run_sec(runner, "16", check=False)
    assert refused.returncode == 1 and refused.stdout == b""
    assert refused.stderr.decode(errors="replace").strip() == (
        f"no model point 16 in the table: {list(range(124, 100, -1))}")


def _months(n):
    """``n`` with its unit, as ``run_sec.py`` writes it: "1 month", "13 months"."""
    return f"{n} month" if n == 1 else f"{n} months"


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {_months(-d)} after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {_months(d)}: contract year {d // 12 + 1}, attained age {p.age(0)}, "
            f"{p.pols_if(0):.6f} in force, AV {p.av_pp_init():,.2f} per contract")


# The worked example's budget, the notional entering the month it is read on and the fixed
# leg, as run_sec.py prints them for the anchor in each of its three standings.
MONEY = ("10,063.19", "100,000.00", "89,936.81")


def test_run_sec_prints_a_point_and_the_block(sec_model, s_model, committed_runs):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  Point 1, the runner's default, the worked example's anchor issued at the
    valuation date, prints ``run.py``'s numbers, its first twelve rows of cash flows S's;
    point 16, the anchor in force 71 months, says where its row came from and where it
    stands, its term under way begun 71 months before the valuation date with ``I_s`` from
    the model point, and prints its decomposition at the term end at ``t = 0``, the worked
    example's +40%; point 24, the anchor issued 13 months on, starts its term in the frame,
    with ``I_s`` from the scenario.  Each line asserted whole, so that a longer number
    cannot pass for the one asserted.  And the block: a line for each of the 24 points, in
    table order, its first twelve rows, which must be the committed points' frames summed
    row by row, as this test sums them, and those frames summed into projection years, each
    year's count the one in force in its first month.  Nothing else runs the runner on the
    committed table.
    """
    head = ("proj_len = {} from the valuation date (t = 0..{}); the Maturity Date closes "
            "policy month 359, at attained age 90")
    budget = ("option budget of the term in force at t = {}: beta = 10.0632%, {} on the "
              "notional entering that month, {}; the fixed leg {}, accreting at 1.7834%, a "
              "2.22% spread")
    for args, origin, standing, term, frame, money, t in (
            ((), " (S's RILA-000001)", "issued at the valuation date, t = 0",
             "starts at policy month 0, t = 0: I_s = 100.00 from the scenario, cap 100.00%",
             head.format(_months(360), 359), MONEY, 0),
            (("16",), " (S's RILA-000001 at its month 71)",
             _standing(_row(sec_model, "derived", 1, 71)),
             "began at policy month 0, 71 months before the valuation date: I_s = 100.00 "
             "from the model point, cap 100.00%", head.format(_months(289), 288), MONEY,
             0),
            (("24",), " (S's RILA-000001, issued 13 months on)",
             "to be issued at t = 13, 13 months after the valuation date",
             "starts at policy month 0, t = 13: I_s = 100.00 from the scenario, cap "
             "100.00%", head.format(_months(373), 372), MONEY, 13)):
        out = committed_runs(*args)
        label = args[0] if args else "1"
        policy = sec_model.Data.model_point_table().at[int(label), "policy_id"]
        assert out.splitlines()[:6] == [
            f"model point {label}: {policy}{origin} - M60 premium 100,000, one 6-year CAP "
            f"option, buffer 10%",
            "interim value family = portfolio / straight_line   scenario = "
            f"{_point(sec_model, int(label)).scenario_id()}",
            f"at the valuation date: {standing}", f"term under way: {term}", frame,
            budget.format(t, *money)], args
        p = _point(sec_model, int(label))
        assert p.result_cf().head(12).round(2).to_string() in out, args
    assert _point(s_model, 1).result_cf().head(12).round(2).to_string() in committed_runs()
    assert ("0         140.0         0.4  0.0        100000.0  40000.00     -0.00    -0.00"
            in committed_runs("16"))
    out = committed_runs("--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<17} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert annual.head(12).round(2).to_string() in out


def test_run_sec_says_one_month_where_a_point_is_a_month_from_the_valuation_date(tmp_path):
    """The runner writes "1 month", not "1 months", on both sides of the valuation date.

    No committed point is in force one month or issued one month on, so the runner is run,
    with ``--block``, beside a table of two: the anchor in force moved back to policy month
    1, its first-year state as ``Data`` requires it, and the anchor issued a month on, on
    S's own scenario, which sets its levels from ``t = 0``.  Each block line is asserted
    whole.
    """
    committed = _committed()
    anchor = _label(committed, "derived", 1, 71)
    future = _label(committed, "future", 1, -13)
    table = _in_first_year(anchor, 1)(_moved(future, -1, scenario_id="up")(committed))
    folder = _sec_inputs(tmp_path, table.loc[[anchor, future]])
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "--block").splitlines()
    count, av = table.at[anchor, "policy_count"], table.at[anchor, "av_pp_init"]
    assert out[:3] == [
        "model points, t = 0 the valuation date for each:",
        f"  {anchor:>2}  RILA-000001-M71   in force 1 month: contract year 1, attained age "
        f"60, {count:.6f} in force, AV {av:,.2f} per contract; proj_len 359",
        f"  {future:>2}  RILA-000001-F13   to be issued at t = 1, 1 month after the "
        f"valuation date; proj_len 361"]


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


def _map_rows(doc):
    """The rows of the symbol map in ``doc``, each the list of its lines' column texts.

    A line whose Notes symbol column is blank continues the row above, as docutils reads
    a simple table, so a cell listed on such a line shares the row, and the meaning, of the
    cell above it.
    """
    lines = doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    spans = [m.span() for m in re.finditer("=+", lines[head + 1])]
    rows = []
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        texts = [line[start:(spans[k + 1][0] if k + 1 < len(spans) else None)].strip()
                 for k, (start, _) in enumerate(spans)]
        if texts[0] or not rows:
            rows.append([texts])
        else:
            rows[-1].append(texts)
    return rows


def _map_faults(doc):
    """The rows of the symbol map in ``doc`` that docutils would read into the wrong cells.

    A row, with the lines under it whose symbol is blank, must have text in every column,
    or its cell and meaning have run into the columns to their left; and a line under a row
    may list a further cell only after a comma, as a list of cells that share a meaning,
    since a cell with a meaning of its own needs a row with a symbol of its own, a
    parenthesis where the notes have none.  ``RILA_US_S``'s map runs its per-contract
    benefit and the benefit taken from and paid above the Account Value into the row of
    ``claims``.
    """
    faults = []
    for row in _map_rows(doc):
        if not all(any(line[k] for line in row) for k in range(len(row[0]))):
            faults.append(f"a blank column in the row of {row[0][1]!r}")
        for above, line in zip(row, row[1:]):
            if re.match(r"[a-z_][a-z0-9_]*\(", line[1]) and not above[1].endswith(","):
                faults.append(f"{line[1]} runs into the row of {row[0][1]!r}")
    return faults


_RULE = re.compile(r"^\s*=+(\s+=+)+\s*$")


def _columns_taken(line):
    """The display columns ``line``'s text occupies, an East Asian wide character two."""
    taken, col = set(), 0
    for ch in line:
        width = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if ch != " ":
            taken.update(range(col, col + width))
        col += width
    return taken


def _table_overruns(doc):
    """The rows of the RST simple tables in ``doc`` that put text between two columns.

    A simple table's rule lines, runs of ``=`` apart, give its columns' spans, and a row
    whose text runs into the gap between two spans is what docutils rejects as a malformed
    table, dropping the whole table from the page.  Only the last column may run past its
    rule.  Each table runs from a rule line to the blank line that ends it.
    """
    lines, found, i = doc.splitlines(), [], 0
    while i < len(lines):
        if not _RULE.match(lines[i]):
            i += 1
            continue
        spans = [m.span() for m in re.finditer("=+", lines[i])]
        gaps = set()
        for (_, end), (start, _) in zip(spans, spans[1:]):
            gaps.update(range(end, start))
        i += 1
        while i < len(lines) and lines[i].strip():
            if not _RULE.match(lines[i]) and _columns_taken(lines[i]) & gaps:
                found.append(lines[i].strip())
            i += 1
    return found


# What only RILA_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months, t = 0 its first policy
# month and its frame and contract year indexed by policy month t; and "then clear the
# cache", modelx-only advice that a compiled model cannot follow.  Each is a phrase of
# RILA_US_S's own, which the docstring test checks.
STALE_PHRASES = (r"~\.RILA_US_S\.", r"``t`` counts \*\*policy months\*\*",
                 r"``t = 0`` is the first policy month", r"indexed by policy month ``t",
                 r"months ``t = 0 \.\. 11``", r"then clear the cache")
STALE = re.compile("|".join(STALE_PHRASES))


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only RILA_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, both SEC files and the product.  The
    cells running in force adds are exactly :data:`NEW_CELLS`, beside every cell of
    ``RILA_US_S``'s, and the symbol map in the Projection docstring maps each of them and
    names nothing the model lacks: every name in it is a cell, or a Reference the notes
    give a symbol to, as the earned rate and the spread are, or ``t``, the cells' argument;
    and docutils reads each of its rows into the right cells (:func:`_map_faults`), which
    ``RILA_US_S``'s map does not.  No row of a simple table in any docstring puts text
    between two of its columns (:func:`_table_overruns`), which would drop the table from
    the rendered page.  And no docstring says what :data:`STALE` matches, each of whose
    phrases ``RILA_US_S``'s own docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, SCENARIOS,
                   "registered index-linked annuit"):
        assert phrase in flat["model"], phrase
    sec_cells, s_cells = set(sec_model.Projection.cells), set(s_model.Projection.cells)
    compiled = "idx" in sec_model.Projection.parameters
    added = {*NEW_CELLS, *(COMPILED_CELLS if compiled else ())}
    dropped = {"opt_legs"} if compiled else set()     # T1 exempts it (R10)
    assert s_cells - sec_cells == dropped, sorted((s_cells - sec_cells) ^ dropped)
    assert sec_cells - s_cells == added, sorted((sec_cells - s_cells) ^ added)
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in sorted(added) if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs) | {"t"}
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    assert _map_faults(sec_model.Projection.doc) == []
    assert _map_faults(s_model.Projection.doc) == [
        f"{cells} runs into the row of 'claims(t, kind)'"
        for cells in ("claim_pp(t, kind)", "claims_from_av(t, kind)",
                      "claims_over_av(t, kind)")]
    overruns = {where: rows for where, rows in ((where, _table_overruns(doc))
                                                for where, doc in _docs(sec_model)) if rows}
    assert not overruns, f"table rows that run into a column gap: {overruns}"
    broken = ("=" * 24 + "  " + "=" * 4 + "\n(above the Account Value) claims_over_av(t)\n"
              + "=" * 24 + "  " + "=" * 4 + "\n")
    assert _table_overruns(broken) == ["(above the Account Value) claims_over_av(t)"]
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe RILA_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    unsaid = [phrase for phrase in STALE_PHRASES
              if not any(re.search(phrase, doc) for doc in s_flat)]
    assert not unsaid, f"phrases RILA_US_S does not say, so STALE holds nothing: {unsaid}"


@pytest.mark.docutils
def test_the_docstrings_parse_as_rst(sec_model):
    """Every docstring of the model parses as reStructuredText, without a warning.

    The docs build reads each docstring through docutils, which reports a malformed table, a
    bad indentation or an unclosed inline markup and drops what it cannot read; a raw-text
    test sees none of it.  Each docstring, dedented as autodoc dedents it and its Sphinx
    roles read as plain interpreted text, which docutils alone does not know, is parsed
    here, and any warning or error is a fault.  docutils comes with the docs build, not with
    the models' requirements, so the test is skipped where it is absent; the column checks
    in the test above run everywhere.
    """
    core = pytest.importorskip("docutils.core")
    faults = []
    for where, doc in _docs(sec_model):
        stream = io.StringIO()
        core.publish_doctree(re.sub(r":[a-z]+:`", "`", inspect.cleandoc(doc)),
                             settings_overrides={"report_level": 2, "halt_level": 5,
                                                 "warning_stream": stream})
        faults += [f"{where}: {line}" for line in stream.getvalue().splitlines()
                   if re.search(r"\((WARNING|ERROR|SEVERE)/", line)]
    assert not faults, f"{len(faults)} docutils messages, first:\n  " + "\n  ".join(
        faults[:10])


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1).

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` and ``market_scenario_file`` alone changed, to
    ``model_point_table_sec.csv`` and ``market_scenario_sec.csv``: an edit to an assumption
    table reaches both models, and the two can never drift apart.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "market_scenario_file": SCENARIOS}


def _wd_asked(x, t):
    """What month ``t`` asks to withdraw, before the clamp: the programme and the rule."""
    return x.wd_scheduled_pp(t) + x.wd_behavioral_pp(t)


def _credited(x, t):
    """The credit of a Term End Date at month ``t``, or None in any other month."""
    return x.credit_rate_term(t) if x.is_term_end(t) else None


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use, the
# year's allowance used in part and not at all, the return-of-premium base below the
# premium, the cap read from its column and re-solved at t = 0, and an account value and a
# base below 0.  Later in the frame, each guaranteed floor and each cap binding with an
# effect, a loss inside the buffer and beyond it, the surrender bound and the shock year
# below it, the moneyness factor at its floor, between it and par and at par, the
# withdrawal clamp at the account value and at 0 on a negative one, the option's share of
# a withdrawal floored at 0 on a negative interim value, a negative behavioural
# withdrawal, the rule at and below its allowance, a charged withdrawal, each band of the
# death benefit, each non-positive branch of the interim value and the base, a re-solve in
# the frame, the term-end surrender charged and free, each account fed, premium tax,
# acquisition and the maturity.
AT_VALUATION = {
    **{f"{c} given": (lambda x, c=c: x.cells[c]() == x.cells[c]() and x.cells[c]() != 0.0)
       for c in STATE},
    "part of the year's allowance used": lambda x: (
        x.duration_mth_init() >= 12 and not x.is_anniv(0)
        and 0.0 < x.free_wd_remain_init() < x.free_wd_rate * x.av_pp_prev_anniv_init()
        - 0.01),
    "none of the year's allowance used": lambda x: (
        x.duration_mth_init() >= 12 and not x.is_anniv(0) and x.free_wd_remain_init() > 0.0
        and x.free_wd_remain_init() == pytest.approx(
            x.free_wd_rate * x.av_pp_prev_anniv_init(), rel=1e-12)),
    "the return-of-premium base below the premium": lambda x: (
        x.duration_mth_init() > 0 and x.rop_pp_init() < x.premium_pp() - 0.01),
    "the cap from its column": lambda x: (
        x.nge_reset() and x.cap_rate(0) == x.cap_rate_init()),
    "the cap re-solved at t = 0": lambda x: (
        x.nge_reset() and 0 < x.term_start_month(0) == x.duration_mth_init()),
    "a negative account value": lambda x: x.av_pp_init() < 0.0,
    "a negative base": lambda x: x.av_pp_prev_anniv_init() < 0.0,
}
IN_FRAME = {
    "the Cap Rate floor binding": lambda x, t: (
        x.is_cap_crediting() and not x.is_uncapped()
        and x.cap_rate(t) == x.guar_min_rate(_code(x, "CAP")) > x.declared_cap()),
    "the Step floor binding": lambda x, t: (
        x.is_step_crediting() and x.step_rate(t) == x.guar_min_rate(_code(x, "STEP"))
        > x.declared_step()),
    "the Edge floor binding": lambda x, t: (
        x.is_edge_crediting() and x.edge_rate(t) == x.guar_min_rate(_code(x, "EDGE"))
        > x.declared_edge()),
    "the Cap Rate option's cap binding": lambda x, t: (
        x.is_cap_crediting() and _credited(x, t) is not None
        and _credited(x, t) == x.cap_rate(t) < x.participation() * x.index_perf(t)),
    "the Floor option's cap binding": lambda x, t: (
        x.is_floor_crediting() and _credited(x, t) is not None
        and _credited(x, t) == x.cap_rate(t) < x.index_perf(t)),
    "the Floor option's floor binding": lambda x, t: (
        x.is_floor_crediting() and _credited(x, t) is not None
        and _credited(x, t) == -x.floor_rate() > x.index_perf(t)),
    "a loss inside the buffer credited as none": lambda x, t: (
        _credited(x, t) == 0.0 and -x.buffer() < x.index_perf(t) < 0.0),
    "a loss beyond the buffer credited": lambda x, t: (
        _credited(x, t) is not None and _credited(x, t) < 0.0
        and x.index_perf(t) < -x.buffer()),
    "the Step rate credited": lambda x, t: (
        x.is_step_crediting() and _credited(x, t) is not None
        and _credited(x, t) == x.step_rate(t)),
    "the Edge rate credited": lambda x, t: (
        x.is_edge_crediting() and _credited(x, t) is not None
        and _credited(x, t) == x.edge_rate(t)),
    "the Step rate credited on a flat index, its boundary": lambda x, t: (
        x.is_step_crediting() and _credited(x, t) is not None
        and x.index_perf(t) == 0.0 and _credited(x, t) == x.step_rate(t)),
    "the Edge rate credited at the buffer exactly, its boundary": lambda x, t: (
        x.is_edge_crediting() and _credited(x, t) is not None
        and x.index_perf(t) == -x.buffer() and _credited(x, t) == x.edge_rate(t)),
    "the surrender bound binding": lambda x, t: x.lapse_rate(t) == x.lapse_rate_max,
    "the shock year below the bound": lambda x, t: (
        x.lapse_rate_sc_mult(t) > 1.0 and 0.0 < x.lapse_rate(t) < x.lapse_rate_max),
    "the moneyness factor at its floor": lambda x, t: (
        x.iv_ratio(t) < x.iv_moneyness_floor
        and x.lapse_iv_mult(t) == x.iv_moneyness_floor ** 2),
    "the moneyness factor between its floor and par": lambda x, t: (
        x.iv_moneyness_floor < x.iv_ratio(t) < 1.0),
    "the moneyness factor at par": lambda x, t: (
        x.is_active(t) and x.iv_ratio(t) > 1.0 and x.lapse_iv_mult(t) == 1.0),
    "the withdrawal clamped at the account value": lambda x, t: (
        _wd_asked(x, t) > x.av_pp_at(t, _code(x, "BEF_WD")) > 0.0
        and x.wd_pp(t) == x.av_pp_at(t, _code(x, "BEF_WD"))),
    "a request on a negative account value paid at 0": lambda x, t: (
        x.av_pp_at(t, _code(x, "BEF_WD")) < 0.0 and _wd_asked(x, t) > 0.0
        and x.wd_pp(t) == 0.0),
    "a withdrawal allocated around a negative interim value": lambda x, t: (
        x.wd_pp(t) > 0.0 > x.interim_value_pp_at(t, _code(x, "BEF_WD"))
        and x.wd_alloc_pp(t, _code(x, "OPTION")) == 0.0),
    "a negative behavioural withdrawal": lambda x, t: x.wd_behavioral_pp(t) < 0.0,
    "the behavioural withdrawal at its allowance": lambda x, t: (
        x.is_anniv(t) and x.wd_behavioral_pp(t) == x.free_wd_allow(t) > 0.0),
    "the behavioural withdrawal below its allowance": lambda x, t: (
        x.is_anniv(t) and 0.0 < x.wd_behavioral_pp(t) < x.free_wd_allow(t)),
    "a withdrawal charged": lambda x, t: x.wd_charge_pp(t) > 0.0,
    "the death benefit at the return-of-premium base": lambda x, t: (
        x.pols_death(t) > 0.0 and x.rop_pp(t) > x.av_pp(t)
        and x.death_ben_pp(t) == x.rop_pp(t)),
    "the death benefit past the return-of-premium band": lambda x, t: (
        x.pols_death(t) > 0.0 and x.age_at_entry() > x.db_rop_max_issue_age),
    "nothing held after a withdrawal of the whole value": lambda x, t: (
        x.wd_pp(t) > 0.0 and x.wd_pp(t) == x.av_pp_at(t, _code(x, "BEF_WD"))
        and abs(x.av_pp(t)) < 1e-6),
    "an interim value at or below 0": lambda x, t: (
        x.interim_value_pp_at(t, _code(x, "BEF_WD")) <= 0.0),
    "an account value at or below 0 before the withdrawal": lambda x, t: (
        x.is_active(t) and x.av_pp_at(t, _code(x, "BEF_WD")) <= 0.0),
    "a negative surrender value paid": lambda x, t: (
        x.surr_value_pp(t) < 0.0 and x.pols_lapse(t) > 0.0),
    "a cap re-solved in the frame": lambda x, t: (
        x.nge_reset() and 0 < x.term_start_month(t) == x.duration_mth(t)),
    "a term-end surrender charged": lambda x, t: (
        x.is_term_end(t) and x.surr_charge_rate(t) > 0.0
        and x.term_end_lapse_rate(t) == x.term_end_lapse_charged),
    "a term-end surrender free of charge": lambda x, t: (
        x.is_term_end(t) and x.surr_charge_rate(t) == 0.0
        and x.term_end_lapse_rate(t) == x.term_end_lapse_free),
    "each account fed at a term end": lambda x, t: (
        x.roll_to_acct_pp(t, _code(x, "FIXED")) > 0.0
        and x.roll_to_acct_pp(t, _code(x, "HOLDING")) > 0.0),
    "a withdrawal from the Holding Account": lambda x, t: (
        x.wd_alloc_pp(t, _code(x, "HOLDING")) > 0.0),
    "premium tax": lambda x, t: x.premium_taxes(t) > 0.0,
    "acquisition": lambda x, t: (
        x.duration_mth(t) == 0 and x.expenses(t) > x.expense_maint / 12.0
        * x.inflation_factor(t) * x.pols_if(t) + 1e-9),
    "the maturity": lambda x, t: x.pols_maturity(t) > 0.0,
}


def _branches(x, kind):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``.

    A future row stands at its issue date with nothing in force, so only the frame's are
    asked of it.
    """
    reached = set() if kind == "future" else {
        what for what, holds in AT_VALUATION.items() if holds(x)}
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in range(x.t_entry(), x.proj_len()))}


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: each crediting method, each
    interim-value family, each amortization rule, each sex, each scenario, each withdrawal
    programme, each term, ``nge_reset`` both ways, an uncapped option, participation above
    1, an issue age past the return-of-premium band; and each kind of valuation month: the
    first contract year, a year's last month, where the year's base is read from the frame
    at ``t = 0`` (§7.10, *Year-opening state*), an anniversary, mid-year, a term end at
    ``t = 0``, a renewal at the valuation month, mid-term in the first term and after a
    renewal, and the last covered month.  And of some core future case: issued more than a
    year on and at the horizon, a one-year term, the legacy family, nge_reset and the crash
    path.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column in use
    and the state of the year under way, and each binding floor, cap, clamp, bound and
    branch of the interim value, the withdrawals, the benefits and the surrenders later in
    the frame, every one of which the full grid reaches.  Each core row's branches were
    recorded by the case that compared it (:func:`_record`), and a row no case has recorded
    is evaluated here.
    """
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def n12(p):
        return 12 * int(at(p, "term_years"))

    def cover(p):
        return 12 * max(90 - int(at(p, "age_at_entry")), 10)

    def choices(column, values):
        return {f"{column} {v}": (lambda k, p, d, v=v, column=column: at(p, column) == v)
                for v in values}

    splices = {
        **choices("crediting_type", ("CAP", "STEP", "EDGE", "FLOOR")),
        **choices("iv_family", ("portfolio", "notional", "delta", "legacy")),
        **choices("amort_rule", ("straight_line", "updated_expiry")),
        **choices("sex", ("M", "F")),
        **choices("scenario_id", ("up", "down", "legacy", "charge_ex", "crash", "edge",
                                  "dip")),
        **choices("wd_schedule_id", ("none", "worked", "charged", "big", "small", "dip")),
        **choices("term_years", (1, 3, 6)),
        **choices("nge_reset", (True, False)),
        "an uncapped option": lambda k, p, d: pd.isna(at(p, "declared_cap")),
        "participation above 1": lambda k, p, d: at(p, "participation") > 1.0,
        "an issue age past the return-of-premium band": lambda k, p, d: (
            at(p, "age_at_entry") > 80),
        "the first contract year": lambda k, p, d: 0 < d < 12,
        "a year's last month": lambda k, p, d: d % 12 == 11,
        "an anniversary": lambda k, p, d: d >= 12 and d % 12 == 0,
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "a term end at t = 0": lambda k, p, d: d % n12(p) == n12(p) - 1,
        "a renewal at the valuation month": lambda k, p, d: d > 0 and d % n12(p) == 0,
        "mid-term in the first term": lambda k, p, d: 0 < d < n12(p) - 1,
        "mid-term after a renewal": lambda k, p, d: (
            d > n12(p) and d % n12(p) not in (0, n12(p) - 1)),
        "the last covered month": lambda k, p, d: d == cover(p) - 1,
    }
    futures = {
        "issued more than a year on": lambda p, k: k > 12,
        "issued at the horizon": lambda p, k: k == 120,
        "a one-year term": lambda p, k: at(p, "term_years") == 1,
        "the legacy family": lambda p, k: at(p, "iv_family") == "legacy",
        "nge_reset": lambda p, k: bool(at(p, "nge_reset")),
        "the crash path": lambda p, k: at(p, "scenario_id") == "crash",
    }
    for what, holds in {**splices}.items():
        assert any(holds(*case) for case in SPLICES), f"no splice case reaches {what}"
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"

    reached = set()
    for case in sorted(CORE_GRID, key=str):
        reached |= _record_of(spliced, splice_records, case)["branches"]
    missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
    assert not missing, f"no core row reaches: {missing}"


def _from_s(s, p, d, label):
    """S point ``p``'s row restated in force at ``d``, under ``label``, from S's own state.

    The spec's extractors read off ``s`` (``SecSpec.state``), the count S has in force at
    ``d``, and S's own scenario, which a row at ``d`` reads re-based: so the row is the
    generator's but for its scenario, which the edges test re-bases itself.
    """
    row = s.model_point().to_frame().T.rename(columns={"pols_if_init": "policy_count"})
    row = row.assign(policy_count=s.pols_if(d), duration_mth=d,
                     **{c: f(s, d) for c, f in SPEC.state.items()})
    row.index = pd.Index([label], name="point_id")
    return row


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, s_model, tmp_path):
    """A zero count, whole numbers in any type, signed account values, the windows' edges.

    Each amount of money may be carried to the cent, so each rule between amounts allows
    for that, a cent where a rule compares one amount with another or with 0 and two and a
    half cents in the renewal rule, which ties four, and each window of contract months is
    accepted just outside it.  Copies of committed rows, appended under ids of their own,
    say so, each reading and projecting its whole frame in finite numbers:

    * a count of 0, which projects zeros;
    * an account value of 0 and of -1,000 on the anchor in force, the interim value being
      able to fall below 0;
    * the year's remainder at its allowance plus 0.009 on the programme valued on its
      anniversary, which ``proj_len()`` admits, and above it on a negative base, where no
      allowance bounds it;
    * the return-of-premium base at the premium plus 0.009;
    * the base at the account value less 0.009 on an anniversary valuation;
    * the account value at the balances plus 0.024 on a renewal valuation;
    * the cap at the guaranteed minimum, 8%, on the reset point after its renewal;
    * the first year's rules just outside their window, the anchor moved to its first
      anniversary, month 12, with a remainder and a base apart from the premium; the
      first term's, the Step option moved to its first renewal, month 12, with a Fixed
      Account; and the anniversary rule's, the anchor at months 11 and 13 with a base
      below its account value;
    * inside both windows, at months 1 and 11, the anchor carrying each amount the first
      year's and the first term's rules hold to a cent within it: a remainder and both
      accounts of 0.009, and a base 0.009 above the premium at month 1 and below it at
      month 11, each of which ``MALFORMED`` refuses a tenth of a cent past the cent;
    * a buffer of 0 on the anchor in force and a floor of 0 on the Floor option, each the
      least its rule admits.

    And the integer columns written as floats, as one blank or one ``1.0`` in a column
    makes pandas read it, are read by value, ``Data`` returning them as the ints it checked
    them as, and the committed rows that carry every flow (:func:`_flow_points`) project
    exactly what the committed table projects; and so does ``nge_reset`` written 1 or 0,
    decoded to the committed flags, the reset point's twin and its two rows in force
    projecting the committed frames bit for bit.  Last, the anchor restated in force from
    S's state at policy months 1, 12, 72 and 359, the first year's first month, the first
    anniversary, a renewal and the last covered month, each on its own scenario re-based to
    its month, continues S from there (:func:`_continues_s`), as the committed rows do, on
    a table whose ``nge_reset`` is written 1.0 or 0.0, as one blank makes pandas read it,
    and decoded as before; and the Edge option restated at its renewal at 36 with each of
    its seven amounts carried to the cent, whose identity then misses by a cent, read by
    floating point as a little more, is read and projects.
    """
    committed = _committed()
    p16, p17, p18, p19, p20, p22 = (_label(committed, "derived", s, d) for s, d in (
        (1, 71), (2, 36), (13, 80), (13, 72), (4, 30), (12, 40)))
    floor_twin = _label(committed, "twin", 6, 0)
    reset_twin = _label(committed, "twin", 13, 0)
    cent = 0.009
    allowance = committed.at[p17, "av_pp_prev_anniv_init"] * 0.1
    held = committed.loc[p19, ["inv_amt_pp_init", "fixed_acct_pp_init",
                               "holding_acct_pp_init"]].sum()
    renewal = {"duration_mth": 12, "fixed_acct_pp_init": 1.0,
               **{c: NAN for c in FIXINGS}}
    copies = {
        101: (p22, {"policy_count": 0.0}),
        102: (p16, {"av_pp_init": 0.0}),
        103: (p16, {"av_pp_init": -1000.0}),
        104: (p17, {"free_wd_remain_init": allowance + cent}),
        105: (p17, {"free_wd_remain_init": 9000.0, "av_pp_init": -1000.0,
                    "av_pp_prev_anniv_init": -900.0}),
        106: (p16, {"rop_pp_init": 100000.0 + cent}),
        107: (p17, {"av_pp_prev_anniv_init": committed.at[p17, "av_pp_init"] - cent}),
        108: (p19, {"av_pp_init": held + 0.024}),
        109: (p18, {"cap_rate_init": 0.08}),
        110: (p16, {"duration_mth": 12, "av_pp_prev_anniv_init": 100000.0 + 0.5,
                    "av_pp_init": 99000.0, "free_wd_remain_init": 100.0}),
        111: (p20, renewal),
        112: (p16, {"duration_mth": 11, "av_pp_prev_anniv_init": 100000.0,
                    "free_wd_remain_init": 0.0}),
        113: (p16, {"duration_mth": 13, "av_pp_prev_anniv_init": 100000.0,
                    "free_wd_remain_init": 5000.0}),
        114: (p16, {"buffer": 0.0}),
        115: (floor_twin, {"floor_rate": 0.0}),
        **{label: (p16, {"duration_mth": month, "av_pp_prev_anniv_init": 100000.0 + gap,
                         "free_wd_remain_init": cent, "fixed_acct_pp_init": cent,
                         "holding_acct_pp_init": cent})
           for label, month, gap in ((116, 1, cent), (117, 11, -cent))},
    }
    reset_rows = (reset_twin, p18, p19)

    def edit(table):
        rows = [table.loc[[row]].assign(**changes).set_axis([label])
                for label, (row, changes) in copies.items()]
        table = pd.concat([table, *rows]).rename_axis("point_id")
        step = table.loc[111]
        table.loc[111, "av_pp_init"] = (step["inv_amt_pp_init"] + 1.0
                                        + step["holding_acct_pp_init"])
        table.loc[111, "av_pp_prev_anniv_init"] = table.loc[111, "av_pp_init"]
        table.loc[111, "free_wd_remain_init"] = 0.0
        return table.assign(nge_reset=table["nge_reset"].astype(int),
                            **{c: table[c].astype(float)
                               for c in ("duration_mth", "age_at_entry", "term_years")})

    def decoded(model):
        """The flags ``model`` read, and its reset rows' frames, as committed."""
        flags = model.Data.model_point_table()["nge_reset"]
        assert flags.dtype == bool
        assert flags.loc[committed.index].tolist() == committed["nge_reset"].tolist()
        for point_id in reset_rows:
            for report in REPORTS:
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0.0, atol=0.0) == [], (point_id, report)

    model = _read_edited(tmp_path / "edges", edit)
    try:
        read = model.Data.model_point_table()
        assert all(read[c].dtype == "int64"
                   for c in ("duration_mth", "age_at_entry", "term_years"))
        assert pd.read_csv(model.Data.input_dir() / TABLE)["nge_reset"].dtype == "int64"
        decoded(model)
        for label in copies:
            df = _point(model, label).result_cf()
            assert len(df) > 0 and np.isfinite(df.to_numpy()).all(), label
        zero = _point(model, 101).result_cf()
        assert (zero == 0.0).all().all() and len(zero) == 80
        assert _point(model, 104).free_wd_avail(0) == pytest.approx(allowance + cent)
        assert _point(model, 105).free_wd_avail(0) == 9000.0
        assert _point(model, 109).cap_rate(0) == 0.08
        assert (_point(model, 114).buffer(), _point(model, 115).floor_rate()) == (0.0, 0.0)
        mid = _point(model, p20)
        assert type(mid.duration_mth(0)) is int and type(mid.term_years()) is int
        for point_id in _flow_points(committed):
            key = _key(model, point_id)
            assert frame_mismatches(_point(sec_model, point_id).result_cf(),
                                    projection(model, key).result_cf(), rtol=0.0,
                                    atol=0.0) == [], point_id
            _release(model, key)
    finally:
        model.close()
    s1, s5 = _point(s_model, 1), _point(s_model, 5)
    months = (1, 12, 72, 359)
    rows = pd.concat([_from_s(s1, 1, d, 200 + i) for i, d in enumerate(months)])
    scenarios = _committed_scenarios()
    path = scenarios[scenarios["scenario_id"] == "up"]
    copies = [shift_months(path, "month_end", d).assign(scenario_id=f"up-M{d}")
              for d in months if f"up-M{d}" not in set(scenarios["scenario_id"])]
    rows = rows.assign(scenario_id=[f"up-M{d}" for d in months])
    # The Edge option at its renewal at 36, every amount carried to the cent, on the
    # committed copy of S's down path re-based to 36, which the programme at 36 reads.
    cents = _from_s(s5, 5, 36, 204).assign(scenario_id=f"{s5.scenario_id()}-M36")
    cents = cents.assign(**{c: round(float(cents.at[204, c]), 2) for c in AMOUNTS})
    assert f"{s5.scenario_id()}-M36" in set(scenarios["scenario_id"])
    table = pd.concat([committed, rows, cents]).rename_axis("point_id")
    table = table.assign(nge_reset=table["nge_reset"].astype(float))
    edits = {SCENARIOS: pd.concat([scenarios, *copies], ignore_index=True)}
    model = _read(_sec_inputs(tmp_path / "restated", table, edits), "restated")
    try:
        assert pd.read_csv(model.Data.input_dir() / TABLE)["nge_reset"].dtype == "float64"
        decoded(model)
        for i, d in enumerate(months):
            p = _point(model, 200 + i)
            assert p.duration_mth_init() == d
            assert _continues_s(s1, p, d) == [], d
        p = _point(model, 204)
        assert p.term_start_month(0) == p.duration_mth_init() == 36
        gap = p.av_pp_init() - (p.inv_amt_pp_init() + p.fixed_acct_pp_init()
                                + p.holding_acct_pp_init())
        assert 0.01 < abs(gap) < 0.0101, gap
        assert np.isfinite(p.result_cf().to_numpy()).all()
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Stage EC -- what compiling changed, held in modelx (USLIB-SEC-PLAN.md Phase 2)


def _references(space):
    """The References a space's ``__init__.py`` assigns, a name to a literal value."""
    source = (model_path(SEC) / space / "__init__.py").read_text(encoding="utf-8")
    return {node.targets[0].id: node.value.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)}


def _comment(file):
    """The source of ``file`` beside the model, and its comment lines joined into one."""
    source = (model_path(SEC).parent / file).read_text(encoding="utf-8")
    return source, " ".join(line.strip().lstrip("# ") for line in source.splitlines()
                            if line.strip().startswith("#"))


def _did(call):
    """``("ok", value)`` or ``("raised", "Type: message")``: what ``call()`` did."""
    try:
        return ("ok", call())
    except Exception as err:                    # what was raised is what is compared
        return ("raised", _raised(err))


# The size of each one-parameter cache spec_sec.py gives, by the parameter's name, which
# _rila_c4_also reads every key of.
SPEC_SIZES = {name: size for name, size in ast.literal_eval(
    (model_path(SEC).parent / "spec_sec.py").read_text(encoding="utf-8"))[
        "spaces"]["Projection"]["cells_param_size"].items() if isinstance(name, str)}

# The codes, each family in its numbering's order: the timings, the count's five and the
# value cells' four, one numbering; the claim kinds, their total and the guaranteed
# minimum's rate kinds, one numbering; the buckets, the legs, the pricing bases, whose
# first two are the engine's markets, the scenario's columns and the crediting rules.
TIMING_CODES = (*TIMINGS, "BEF_CREDIT", "BEF_ROLL", "BEF_WD", "AFT_WD")
KIND_CODES = (*KINDS, "ALL", "CAP", "STEP", "EDGE")
NAME_CODES = ("INDEX_LEVEL", "MVR", "RISK_FREE", "DIV_YIELD", "IMPL_VOL")
FAMILIES = (TIMING_CODES, KIND_CODES, BUCKETS, LEGS, BASES, NAME_CODES, RULES)

# The most legs a replicating portfolio has, the Floor's four, which opt_leg's cache holds.
MOST_LEGS = 4


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one above the comment's, which only adds headroom, and C4 sees one below only on
    a point that reaches it.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: with ``years`` the longest cover, ``max(maturity_age -
    issue_age_min, maturity_min_years)``, ``t`` to ``12 * years + future_horizon_mth +
    3``, ``a`` to ``max(maturity_age, issue_age_max + maturity_min_years) + 1``, ``cy`` to
    ``years + 2``, ``y`` to ``years + 3`` and ``m`` to ``12 * years + 2``; ``kind`` to the
    kinds' numbering and one of headroom, ``i`` to the Floor's four legs and one, and
    ``bucket`` to the 2-D width.  Every 2-D cache has one inner width, the timings' nine,
    and both 3-D caches one inner shape, the seven legs by that width: MSVC, which builds
    the Windows leg, accepts two widths that gcc 14 refuses, and the build's
    ``-Werror=incompatible-pointer-types`` catches that only on gcc or clang, so this
    holds it on every platform (USLIB-SEC-PLAN.md §7.2, *For M16 and later*; *CI run 17*).
    Each family of codes is dense from 0 and of ints; and ``Data.read_last_mth`` and
    ``Data.read_last_age``, the last month and age the arrays hold, are the last ``t``
    and the last ``a``.  A change to a bound or a size is derived again in the comment
    and here.
    """
    source, comment = _comment("spec_sec.py")
    for formula in ("1,203 = 12 * max(maturity_age - issue_age_min, maturity_min_years) "
                    "+ future_horizon_mth + 3",
                    "122 = max(maturity_age, issue_age_max + maturity_min_years) + 1",
                    "max(maturity_age - issue_age_min, maturity_min_years) = 90: 91 "
                    "values, and one of headroom, 92",
                    "1 .. policy_term() + 1 = 91",
                    "1 .. 12 * policy_term() = 1,080 at issue age 0: 1,081 values from 0, "
                    "and one of headroom, 1,082",
                    "7 values from 0, and one of headroom, 8",
                    "the Floor's four legs, 0 .. 3, and one of headroom, 5",
                    "Data.read_last_mth", "Data.read_last_age"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    for family in FAMILIES:
        values = [proj[code] for code in family]
        assert values == list(range(len(family))), (family, values)
        assert all(type(v) is int for v in values), family
    low, high, top = proj["issue_age_min"], proj["issue_age_max"], proj["maturity_age"]
    least, horizon = proj["maturity_min_years"], data["future_horizon_mth"]
    years = max(top - low, least)
    t, a = 12 * years + horizon + 3, max(top, high + least) + 1
    width, legs = max(len(family) for family in FAMILIES), len(LEGS)
    assert width == len(TIMING_CODES) == 9 and legs == 7
    assert sizes == {
        "t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
        ("t", "bucket"): (t, width), ("t", "name"): (t, width), ("t", "basis"): (t, width),
        ("t", "rule"): (t, width), ("t", "leg", "timing"): (t, legs, width),
        ("t", "leg", "basis"): (t, legs, width), "kind": len(KIND_CODES) + 1,
        "bucket": width, "i": MOST_LEGS + 1, "a": a, "cy": years + 2, "y": years + 3,
        "m": 12 * years + 2}, sizes
    assert len({size[1:] for size in sizes.values() if isinstance(size, tuple)
                and len(size) == 2}) == 1
    assert len({size[1:] for size in sizes.values() if isinstance(size, tuple)
                and len(size) == 3}) == 1
    assert (t, a) == (1203, 122)
    assert data["read_last_mth"] == t - 1 and data["read_last_age"] == a - 1, data


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: a cold ``net_cf`` in the last month of
    the longest cover, issue age 0, issued now or 120 months on, needs a limit of 2,213 in
    the export from a script's top level, and the reports the sample runs in ascending
    ``t``, the export's import among the frames they run under, 154 (measured at M25).
    The limit is four times the first, rounded up to the thousand.  No build can tell a
    lower limit above the reports' need, which builds the same model.  So this holds the
    limit, read from the sample's code, to the value derived from its comment's need, and
    holds the call before the import of the export.  A change to the need is measured
    again and written in the comment.
    """
    source, comment = _comment("sample_sec.py")
    need = re.search(r"needs a limit of ([\d,]+) in the export", comment)
    reports = re.search(r"in ascending t, need ([\d,]+)", comment)
    assert need and reports, comment
    need, reports = (int(m.group(1).replace(",", "")) for m in (need, reports))
    tree = ast.parse(source)
    calls = [(node.lineno, node.args[0].value) for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
             and node.func.attr == "setrecursionlimit"
             and isinstance(node.args[0], ast.Constant)]
    imports = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
               and node.module == f"{SEC}_nomx"]
    assert len(calls) == 1 and len(imports) == 1, (calls, imports)
    (line, limit), = calls
    assert reports < need and line < imports[0], (reports, need, line, imports)
    assert limit == -(-4 * need // 1000) * 1000, (limit, need)


# The labels the sample types on its blank copy: the six that return their column as read
# and that Data accepts as other than text, and the two of them that key a table.
FREE_LABELS = ("policy_id", "crediting_type", "iv_family", "amort_rule", "scenario_id",
               "wd_schedule_id")
KEYED_LABELS = ("scenario_id", "wd_schedule_id")


def test_the_sample_traces_the_labels_on_a_blank_copy():
    """``sample_sec.py`` calls the six free labels on a second instance of the export,
    whose one point has its four free labels blank and its two keys the number 1.

    A label returns its column as read, so mx2cy must see each return something other
    than text, or it compiles to ``str`` and raises ``TypeError`` on a blank or a number
    (the sample's docstring).  The committed table's labels are text, so dropping the
    trace changes no declaration that a test of the committed points sees, and only the
    compiled label test, on a build, would fail.  So this holds the trace in the sample's
    code, in seconds: ``LABELS`` and ``KEYS`` are the six and the two; a copy of the
    table's first row assigned ``None`` at every label but the keys and 1 at the keys;
    then a second ``_c_RILA_US_SEC()`` instance, whose ``Data`` is pointed at the copies of
    the model point, scenario and withdrawal files, a ``Projection`` of it, and each of
    ``LABELS`` called on that, in that order.
    """
    source, _ = _comment("sample_sec.py")
    tree = ast.parse(source)
    literal = {node.targets[0].id: ast.literal_eval(node.value) for node in tree.body
               if isinstance(node, ast.Assign) and len(node.targets) == 1
               and isinstance(node.targets[0], ast.Name)
               and node.targets[0].id in ("LABELS", "KEYS")}
    assert literal == {"LABELS": FREE_LABELS, "KEYS": KEYED_LABELS}, literal
    lines = [(node.lineno, ast.unparse(node)) for node in ast.walk(tree)
             if isinstance(node, (ast.Assign, ast.Expr, ast.For))]

    def first(pattern, after=0):
        found = [(line, re.fullmatch(pattern, text, re.S)) for line, text in lines
                 if line > after and re.fullmatch(pattern, text, re.S)]
        assert found, pattern
        return min(found, key=lambda f: f[0])

    blank, _ = first(r"(\w+) = \1\.assign\(\*\*\{label: None for label in LABELS if label "
                     r"not in KEYS\}, \*\*\{key: 1 for key in KEYS\}\)")
    made, match = first(rf"(\w+) = _c_{SEC}\(\)", blank)
    second = match.group(1)
    pointed, match = first(r"for ref, table in \(\('model_point_file', \w+\), "
                           r"\('market_scenario_file', \w+\), \('withdrawal_file', \w+\)\)"
                           rf":.*setattr\({second}\.Data, ref, str\(\w+\)\)", made)
    proj, match = first(rf"(\w+) = {second}\.Projection\[0\]", pointed)
    p = match.group(1)
    first(rf"for label in LABELS:\s+getattr\({p}, label\)\(\)", proj)


def test_the_sample_calls_every_engine_cell():
    """``sample_sec.py`` calls each of the registry's eleven ``"engine"`` cells on a point.

    No projection cell calls an engine cell, so only the sample's own call types one: an
    engine cell the sample stops calling is traced at nothing and compiles with object
    parameters, and the typing guard still passes, since it admits the engine cells' dict
    caches by name (us_registry).  So this holds, in the sample's code, a call
    ``p.<cell>(...)`` of every engine cell, ``p`` the ItemSpace the sample's loop makes
    of each committed point.
    """
    source, _ = _comment("sample_sec.py")
    engine = set(meta(SEC)["engine"])
    called = {node.func.attr for node in ast.walk(ast.parse(source))
              if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
              and isinstance(node.func.value, ast.Name) and node.func.value.id == "p"}
    assert len(engine) == 11 and engine <= called, sorted(engine - called)


def test_sex_refuses_a_value_that_is_not_text_itself():
    """``sex()`` returns M or F, or raises ``ValueError`` naming the point (M26).

    ``Data`` already refuses a point of any other sex, since the mortality table's check
    admits no other, so ``sex()`` compiles to ``str``; the typing guard admits a label
    typed ``str`` only where its own formula refuses what is not text
    (``sec_support.labels_refusing_non_text``).  So the label is called on the committed
    model whose table, past ``Data``'s checks, holds the first point's sex blank, the
    number 7 and the text X: each raises, with ``Data``'s wording; and every committed
    point's sex is returned as the table holds it.
    """
    from sec_support import labels_refusing_non_text
    assert labels_refusing_non_text(SEC, {"sex"}) == {"sex"}
    for value in (None, 7, "X"):
        model = mx.read_model(model_path(SEC), name=_name("sex_refused"))
        try:
            table = model.Data.model_point_table().astype({"sex": object})
            table.iloc[0, table.columns.get_loc("sex")] = value
            model.Data.model_point_table[()] = table
            first = table.index[0]
            with pytest.raises(Exception) as raised:
                projection(model, point_keys(model)[0]).sex()
        finally:
            model.close()
        assert f"ValueError: point_id {first}: sex must be M or F" in str(raised.value), (
            value, str(raised.value))
    model = mx.read_model(model_path(SEC), name=_name("sex_read"))
    try:
        table = model.Data.model_point_table()
        got = [projection(model, key).sex() for key in point_keys(model)]
    finally:
        model.close()
    assert got == table["sex"].tolist(), got


def test_the_spec_maps_s_totals_and_scenario_columns_onto_sec_codes():
    """``SPEC.twin_arg_map`` hands T1 S's keys as SEC names them (R9, R12).

    ``sec_support._rila_codes`` maps S's ``kind=None`` totals of ``claims`` and
    ``claims_over_av`` onto ``"ALL"`` and S's ``market_state`` columns onto their codes'
    names, the column upper-cased, and passes every other key, SEC's own codes among
    them, as it is; ``sec_support.codes`` then turns each name into the SEC model's int
    code.  A map that dropped either, or touched a kind S names or a code SEC passes,
    would compare S's total with a kind, or a column with nothing, in T1.
    """
    arg_map = SPEC.twin_arg_map
    assert arg_map("claims", (5, None)) == (5, "ALL")
    assert arg_map("claims_over_av", (7, None)) == (7, "ALL")
    assert arg_map("claims", (5, "DEATH")) == (5, "DEATH")
    assert arg_map("claims", (5, 3)) == (5, 3)
    for column in ("index_level", "mvr", "risk_free", "div_yield", "impl_vol"):
        assert arg_map("market_state", (8, column)) == (8, column.upper())
    assert arg_map("market_state", (8, 2)) == (8, 2)
    assert arg_map("pols_if_at", (3, "BEF_DECR")) == (3, "BEF_DECR")
    assert arg_map("opt_component", (3, "OTM_PUT", 100.0, 1.0, "CURRENT")) == (
        3, "OTM_PUT", 100.0, 1.0, "CURRENT")


# The two totals S writes as kind=None and SEC as the code ALL.
TOTALLED = ("claims", "claims_over_av")


def test_the_all_totals_are_s_totals_bit_for_bit(sec_model, s_model):
    """``claims(t, ALL)`` and ``claims_over_av(t, ALL)`` are ``RILA_US_S``'s totals, bit
    for bit (R12).

    S's ``claims(t, kind=None)`` and ``claims_over_av(t, kind=None)`` are the three kinds'
    total, written as a chain of ``+`` in the kinds' order, and here they are the code
    ``ALL``, the same chain.  T1 reaches S's totals through the spec's ``twin_arg_map``
    to its tolerance; here they are held exactly, on the twins of S's fifteen points, in
    every month of the frame: each total S's float, its type and the sign of a zero
    included, by ``float.hex``, and each kind S's at the kind's name.  A total summed in
    another order, or one that sums a kind twice and another not at all, moves a last bit
    or a number in a month where two kinds are paid, and fails.
    """
    found = []
    for point in S_POINTS:
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        assert mine.proj_len() == theirs.proj_len()
        for t in range(mine.proj_len()):
            for cell in TOTALLED:
                got, want = mine.cells[cell](t, mine.ALL), theirs.cells[cell](t, None)
                if type(got) is not type(want) or got.hex() != want.hex():
                    found.append(f"point {point}: {cell}({t}, ALL) {got!r}, S's {want!r}")
                for kind in KINDS:
                    if mine.cells[cell](t, _code(mine, kind)).hex() != theirs.cells[cell](
                            t, kind).hex():
                        found.append(f"point {point}: {cell}({t}, {kind}) is not S's")
    assert not found, found[:20]


# The month at which the sign test sets the kinds on the anchor's twin: its sixth policy
# year, where deaths and surrenders are both paid.
ZERO_MONTH = 60


def test_negative_zero_kinds_total_a_negative_zero_as_s_chain_does():
    """Each ``ALL`` total is ``-0.0`` where every kind is ``-0.0``, as S's chain gives.

    S's totals add the three kinds with ``+``, starting at the first, and ``-0.0 + -0.0``
    is ``-0.0``, so S's total of negative zeros keeps its sign.  The bit-for-bit test
    cannot hold it: no committed month has negative zero kinds.  So here, on a read of
    each model of its own, the three kinds of ``claims`` and of ``claims_over_av`` at
    :data:`ZERO_MONTH` on the anchor's twin are set to ``-0.0`` as modelx input values, in
    both models, and each total must be S's: ``-0.0``, a float.  A total started at
    ``0.0``, as a ``sum`` from ``0.0`` is, gives ``0.0`` and fails.  The compiled model
    meets the same through a replaced input (:func:`_negative_zeros`).
    """
    s = _read(model_path(TWIN), "s_zeros")
    sec = _read(model_path(SEC), "zeros")
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        paid = [kind for kind in KINDS if theirs.claims(ZERO_MONTH, kind) != 0.0]
        assert paid == ["DEATH", "LAPSE"], paid
        for cell in TOTALLED:
            for kind in KINDS:
                theirs.cells[cell][ZERO_MONTH, kind] = -0.0
                mine.cells[cell][ZERO_MONTH, _code(mine, kind)] = -0.0
        totals = [proj.cells[cell](ZERO_MONTH, total) for cell in TOTALLED
                  for proj, total in ((theirs, None), (mine, mine.ALL))]
    finally:
        sec.close()
        s.close()
    for total in totals:
        assert type(total) is float and total.hex() == "-0x0.0p+0", totals


# The References under which every kind of claim is a negative zero wherever the Account
# Value is below 0: no death, no surrender and no term-end surrender, so that each kind's
# count is 0.0 while its benefit per contract, the Account Value past the return-of-premium
# band, is below 0.  On S point 12, issued at 81, on S's "down" path replaced by the
# splice's crash path, whose index falls 85% at month 20.
NEGATIVE_ZEROS = {"mort_ae_factor": 0.0, "lapse_rate_max": 0.0, "term_end_lapse_free": 0.0,
                  "term_end_lapse_charged": 0.0}
ZERO_POINT = 12


def _crash_for_down(df):
    """An edit of a scenario table that runs :data:`STEPPED`'s crash path as ``down``."""
    rows = pd.DataFrame([("down", m, i, r, rf, q, v, "the crash path, for a test")
                         for m, i, r, rf, q, v in STEPPED["crash"]], columns=df.columns)
    return pd.concat([df[df["scenario_id"] != "down"], rows], ignore_index=True)


def _negative_zeros(tmp_path):
    """S's and SEC's folders on :func:`_crash_for_down`'s scenarios, ``(s, sec)``."""
    s = temp_inputs(tmp_path / "s", model_path(TWIN),
                    edits={"market_scenario.csv": _crash_for_down})
    sec = _sec_inputs(tmp_path / "sec", _committed(), {SCENARIOS: _crash_for_down})
    return s, sec


def test_a_total_of_negative_zero_kinds_is_s_negative_zero(tmp_path):
    """Where every kind is a negative zero, through the inputs alone, so is each total.

    The test above sets the kinds by hand, which only modelx can.  Here the inputs make
    them: under :data:`NEGATIVE_ZEROS`, on the twin of S point 12 on the crash path
    (:func:`_negative_zeros`), each kind's count is 0.0 and its benefit below 0 in the
    months the Account Value is, so each of ``claims``' kinds is ``-0.0`` there and S's
    chain keeps the sign.  ``claims(t, ALL)`` and ``claims_over_av(t, ALL)`` are S's in
    every month by ``float.hex``, ``claims`` ``-0.0`` in 29 of its 120 months; a total
    begun at ``0.0`` gives ``0.0`` there and fails.  The compiled model is held to the same
    bits on the same inputs (:func:`test_the_compiled_all_total_keeps_s_sign_of_zero`).
    """
    s_folder, sec_folder = _negative_zeros(tmp_path)
    s = _read(s_folder, "s_negzero", NEGATIVE_ZEROS)
    sec = _read(sec_folder, "negzero", NEGATIVE_ZEROS)
    try:
        theirs, mine = _point(s, ZERO_POINT), _row(sec, "twin", ZERO_POINT, 0)
        months = range(theirs.proj_len())
        want = [theirs.cells[cell](t, None).hex() for cell in TOTALLED for t in months]
        have = [mine.cells[cell](t, mine.ALL).hex() for cell in TOTALLED for t in months]
    finally:
        sec.close()
        s.close()
    assert sum(h == "-0x0.0p+0" for h in want[:len(months)]) == 29
    assert have == want, [(i, h, w) for i, (h, w) in enumerate(zip(have, want)) if h != w]


# The References under which the Holding Account is fed at every term end, and the Fixed
# Account and the option too, so that a withdrawal is spread over three buckets (the
# critique of M25's design, M4): roll_transfer_holding 5%, with roll_renew_same moved to
# 75% so that the four shares still sum to 1.  The twins that withdraw: the worked
# example's programme, the behavioural rule and the charged programme.
HOLDING_ON = {"roll_transfer_holding": 0.05, "roll_renew_same": 0.75}
WITHDRAWING = (2, 3, 14)


def test_a_withdrawal_over_three_buckets_sums_them_as_s_sum_does(tmp_path):
    """``wd_alloc_pp`` sums the three buckets as S's ``sum`` does, bit for bit.

    ``RILA_US_S`` adds the buckets' values with Python's ``sum``, which CPython compensates
    on floats, and the allocation divides by that total, so a total an ulp off moves the
    allocation.  On the committed inputs the Holding Account is empty, and no test could
    tell a running sum, or one that dropped the Holding Account, from S's.  Under
    :data:`HOLDING_ON`, set in both models, on the twins of :data:`WITHDRAWING`: in some
    month a left-to-right sum of S's three values differs from S's ``sum`` of them, so
    that the comparison can fail, and in every month that withdraws, each bucket's
    allocation is S's by ``float.hex``.  And each twin is S's, cell by cell, through
    :func:`_mismatches` (T1's comparison), under the same References.
    """
    s = _read(model_path(TWIN), "s_holding", HOLDING_ON)
    sec = _read(model_path(SEC), "holding", HOLDING_ON)
    apart, found, months = 0, [], 0
    try:
        for point in WITHDRAWING:
            theirs, mine = _point(s, point), _row(sec, "twin", point, 0)
            _sweep(theirs)
            _sweep(mine)
            for t in range(theirs.proj_len()):
                if theirs.wd_pp(t) <= 0.0:
                    continue
                months += 1
                values = [theirs.wd_bucket_value_pp(t, b) for b in BUCKETS]
                apart += (values[0] + values[1]) + values[2] != sum(values)
                for b in BUCKETS:
                    got = mine.wd_alloc_pp(t, _code(mine, b))
                    if got.hex() != theirs.wd_alloc_pp(t, b).hex():
                        found.append(f"point {point}: wd_alloc_pp({t}, {b}) {got!r}")
            found += [f"point {point}: {line}" for line in _mismatches(
                theirs, mine, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt)]
    finally:
        sec.close()
        s.close()
    assert months > 0 and apart > 0, (months, apart)
    assert not found, found[:20]


def test_every_parameterless_cell_returns_a_python_number(sec_model):
    """Every parameterless cell but the reporting ones returns a Python int, float or bool.

    R11: a ``Projection`` cell that reads a ``Data`` vector converts the element, ``int()``,
    ``float()`` or ``bool()``, so that modelx returns a Python number, as the compiled cell
    does, and not a numpy scalar, whose arithmetic and printing differ, and which C4
    compares as a kind of its own.  A conversion left out moves no number and still
    compiles, so it is asserted here: on every committed point, each parameterless cell
    outside :func:`sec_support.reporting_cells` returns exactly an ``int``, a ``float`` or
    a ``bool``, and each flag a ``bool``.
    """
    from sec_support import reporting_cells
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    flags = ("nge_reset", "is_uncapped", *DECODES)
    assert {"point_id", "mort_schedule", "scenario_number", "wd_schedule_number",
            "opt_leg_count", *flags} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
        found += [f"{key}: {name} is not a bool" for name in flags
                  if type(proj.cells[name]()) is not bool]
    assert not found, found


# Data's readers, each a DataFrame or a path, which only the reporting cells and Data's own
# cells read; and the count cells, each a table's check, an int.
READERS = ("input_dir", "model_point_table", "mort_table", "market_scenario",
           "surr_charge_table", "guar_min_rate_table", "lapse_table", "withdrawal_table")
COUNTS = ("market_scenario_count", "mort_table_count", "surr_charge_count",
          "guar_min_rate_count", "lapse_table_count", "withdrawal_count")

# Every other Data cell, by what it holds (R5): an int64 vector for a whole number, a code,
# a flag or a number into another array; a float64 vector or table for an amount, a rate,
# a market value or a key compared by value; an int for an extent; and the uncapped cap,
# a float.  As {cell: (dtype, dimensions)}.
_INT64 = ("point_id", "age_at_entry", "age_at_entry_ok", "duration_mth", "duration_mth_ok",
          "term_years", "term_years_ok", "nge_reset", "is_uncapped", *DECODES,
          "scenario_number", "scenario_first_mths", "mort_schedule", "mort_age_firsts",
          "mort_age_lasts", "wd_schedule_number")
_FLOAT64 = ("policy_count", "premium", "buffer", "floor_rate", "participation",
            "declared_cap", "declared_step", "declared_edge", "wd_rate_ann", *STATE,
            "guar_min_cap", "guar_min_step", "guar_min_edge", "surr_charge_array",
            "lapse_years", "lapse_rates")
_TABLES = ("index_level_array", "mvr_array", "risk_free_array", "div_yield_array",
           "impl_vol_array", "mort_rate_array", "wd_amount_array")
_EXTENTS = ("scenario_count", "scenario_last_mth", "mort_sexes", "mort_age_held",
            "wd_schedule_count", "wd_last_mth")
DATA_KINDS = {**{name: ("int64", 1) for name in _INT64},
              **{name: ("float64", 1) for name in _FLOAT64},
              **{name: ("float64", 2) for name in _TABLES},
              **{name: ("int", 0) for name in _EXTENTS}, "cap_uncapped": ("float", 0)}

# The vectors one value a point, and the arrays one row a scenario, a sex or a programme.
BY_POINT = (*_INT64[:10], *DECODES, "scenario_number", "mort_schedule",
            "wd_schedule_number", *_FLOAT64[:-3])


def _docstring_kinds():
    """The Data docstring's table of its vectors: each cell a row names, its dtype and its
    number of dimensions, from the shape, ``[point]`` 1, ``[scenario, t]`` 2, ``scalar`` 0.

    The table's first three columns, by the widths its rules give; a row naming a cell
    ``x()`` names it, and a row's "and nine more" is counted, not named.
    """
    source = (model_path(SEC) / "Data" / "__init__.py").read_text(encoding="utf-8")
    lines = ast.get_docstring(ast.parse(source)).splitlines()
    head = next(i for i, line in enumerate(lines) if line.split()[:2] == ["Cells", "dtype"])
    widths = [len(rule) for rule in lines[head - 1].split()]
    starts = [0]
    for width in widths[:-1]:
        starts.append(starts[-1] + width + 2)
    kinds, row = {}, None
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        names = re.findall(r"(\w+)\(\)", line[:widths[0]])
        dtype = line[starts[1]:starts[1] + widths[1]].strip()
        shape = line[starts[2]:starts[2] + widths[2]].strip()
        if dtype:
            row = (dtype, 0 if shape == "scalar" else 1 + shape.count(","))
        for name in names:
            assert name not in kinds, name
            kinds[name] = row
    return kinds


def test_each_data_vector_is_the_int64_or_float64_its_docstring_states(sec_model):
    """Every ``Data`` cell but the readers and the counts is the int64 or float64 array,
    or the int, that :data:`DATA_KINDS` and the Data docstring's table of its vectors
    state; and each count is an int.

    That is what compiles to a typed memoryview or a C ``long long`` (the Data
    docstring): an array of bools, objects or text compiles as a Python object, and so does
    a check returned as a numpy int.  The typing guard, C3, finds that in the compiled
    model's declarations; this finds it in seconds, in every run, naming the cell.  And
    each vector is of R5's kind, int64 for ages, months, codes, flags and schedules,
    float64 for amounts, rates and keys compared by value, of its dimensions, one value a
    point where it is a point's: a flag held as bools reads the same numbers in modelx,
    and compiles otherwise, which neither C4 nor a number shows.  Every cell is in
    :data:`DATA_KINDS`, and every cell the docstring's table names is stated there as
    here.
    """
    data = sec_model.Data
    points = len(data.model_point_table())
    vectors = {name for name, cells in data.cells.items()
               if not cells.parameters and name not in READERS + COUNTS}
    assert set(DATA_KINDS) == vectors, set(DATA_KINDS) ^ vectors
    stated = _docstring_kinds()
    assert set(stated) <= vectors, set(stated) - vectors
    assert {name: DATA_KINDS[name] for name in stated} == stated
    found = [f"{name}: {type(data.cells[name]()).__name__}, not an int" for name in COUNTS
             if type(data.cells[name]()) is not int]
    for name, (kind, ndim) in DATA_KINDS.items():
        value = data.cells[name]()
        if ndim == 0:
            if type(value) is not {"int": int, "float": float}[kind]:
                found.append(f"{name}: {type(value).__name__}, not {kind}")
        elif not (isinstance(value, np.ndarray) and value.dtype == np.dtype(kind)
                  and value.ndim == ndim):
            found.append(f"{name}: {getattr(value, 'dtype', type(value).__name__)}, "
                         f"{getattr(value, 'ndim', 0)} dimensions, not {kind} of {ndim}")
        elif name in BY_POINT and len(value) != points:
            found.append(f"{name}: {len(value)} values for {points} points")
    assert not found, found
    assert set(READERS) < set(data.cells) and set(COUNTS) < set(data.cells)


def test_the_arrays_pad_with_nan_where_no_read_reaches(sec_model, tmp_path):
    """Every place an array holds no table value is NaN, so that a read of it shows (N3),
    and each reader refuses a key before it reads one, naming the point by its label.

    ``Data`` holds each table by number, age or month from 0, and to ``read_last_mth`` and
    ``read_last_age``, and a read the readers' guards should have stopped, at schedule 0,
    at an age outside a sex's rates or at a month before a scenario's first, would read
    padding: written NaN, it carries into every number that reads it, where 0.0 would pass
    for a rate.  So on the committed model: each array is as wide as its last month or age
    and one more, so that every key a guard lets through has a place, the programmes'
    to ``wd_last_mth()``; row 0 of the mortality, of every scenario array and of the
    programmes is NaN, and schedule 0's ages are ``(1, 0)``, so that no age lies between
    them; each sex's ages below its first, 40, and past its last, 120, are NaN, and none
    between; each scenario's months before its first, 13 for the anchor issued 13 months
    on, are NaN, and none after; and a programme's month without a withdrawal is 0.0, as
    ``RILA_US_S`` answers it, not padding.

    And on the extract labelled otherwise than by position (:func:`_relabelled`), where a
    label read as ``idx + 1`` would name another point, each reader refuses a key below
    its guard by the point's label: an age below the table's first, a month before the
    scenario's first, a contract year before the lapse table's first, where the scan finds
    no row and a read at row -1 would read the last row's rate, and a month end below 0.
    """
    data = sec_model.Data
    mort, firsts = data.mort_rate_array(), data.mort_age_firsts()
    lasts = data.mort_age_lasts()
    assert mort.shape == (data.mort_sexes() + 1, data.read_last_age + 1) == (3, 122)
    assert np.isnan(mort[0]).all() and (firsts[0], lasts[0]) == (1, 0)
    for s in (1, 2):
        assert (firsts[s], lasts[s]) == (40, 120), s
        assert np.isnan(mort[s, :40]).all() and np.isnan(mort[s, 121:]).all(), s
        assert not np.isnan(mort[s, 40:121]).any(), s
    starts = data.scenario_first_mths()
    for name in ("index_level_array", "mvr_array", "risk_free_array", "div_yield_array",
                 "impl_vol_array"):
        values = data.cells[name]()
        assert values.shape == (data.scenario_count() + 1, data.read_last_mth + 1), name
        assert np.isnan(values[0]).all(), name
        for s in range(1, len(values)):
            assert np.isnan(values[s, :starts[s]]).all(), (name, s)
            assert not np.isnan(values[s, starts[s]:]).any(), (name, s)
    late = data.scenario_number()[list(data.model_point_table().index).index(
        _label(data.model_point_table(), "future", 1, -13))]
    assert starts[late] == 13 and sorted(set(starts[1:])) == [0, 13], starts
    programmes = data.wd_amount_array()
    assert programmes.shape == (data.wd_schedule_count() + 1, data.wd_last_mth() + 1)
    assert data.wd_last_mth() == data.read_last_mth
    assert np.isnan(programmes[0]).all() and not np.isnan(programmes[1:]).any()
    assert (programmes[1:] == 0.0).sum() > 0
    extract = _relabelled(_committed())
    model = _read(_sec_inputs(tmp_path, extract), "padding")
    try:
        p = _point(model, 101)
        assert p.point_id() == 101 != point_keys(model)[0] + 1
        later = _point(model, 124)
        assert later.duration_mth_init() == -13
        for call, message in (
                (lambda: p.mort_rate_base_at(39), "point_id 101: the mortality table holds "
                                                  "no rate at age 39"),
                (lambda: p.lapse_rate_base_py(0), "point_id 101: the lapse table holds no "
                                                  "rate at or before contract year 0"),
                (lambda: p.wd_amount_pm(-1), "point_id 101: the withdrawal programme "
                                             "holds no month end -1"),
                (lambda: later.market_state(12, later.INDEX_LEVEL),
                 "point_id 124: its market scenario holds no level at month 12")):
            _refused(call, message)
    finally:
        model.close()


# Each text value S branches on, written in another case and beside a space, on a point
# whose projection reads the column, as {column: {S point: value}}; each must be refused
# with S's own message in both models.
SPELLED = {"crediting_type": {1: "Cap", 4: " STEP", 5: "EDGE ", 6: "floor"},
           "iv_family": {7: "Notional", 8: " delta", 9: "legacy ", 1: "PORTFOLIO"},
           "amort_rule": {10: "Updated_Expiry", 1: " straight_line"}}

# Each key a point joins a table on, written beside a space: refused by Data as a key the
# table lacks, naming the point, where S would read nothing or raise KeyError.
SPACED_KEYS = {"scenario_id": (1, " up", "scenario_id must name a scenario of"),
               "wd_schedule_id": (2, "worked ", "wd_schedule_id must name a programme of"),
               "sex": (4, " F", "mort_table.csv must rate the point's sex")}


def test_each_decode_is_s_exact_comparison(tmp_path):
    """Each text column is decoded by ``RILA_US_S``'s exact comparison: another case or a
    space is refused, in both models, with S's message.

    ``RILA_US_S`` compares the text as it stands, ``crediting_type() == "CAP"``, and so
    does each ``is_*`` vector of ``Data`` that ``Projection``'s decodes read, element by
    element (USLIB-SEC-PLAN.md §7.3, *For M17 and later*).  A decode that folded the case
    or stripped the text would project a point S refuses.  So each value S names, in every
    text column a projection branches on, is written in another case or beside a space
    (:data:`SPELLED`), each on a point of its own whose projection reads the column, and
    each point's ``result_cf`` raises in this model what it raises in ``RILA_US_S`` on the
    same table, ``ValueError("invalid crediting_type")`` and the like.  And each key a
    point joins a table on, written beside a space (:data:`SPACED_KEYS`), is refused by
    ``Data`` as a key the table lacks, naming the point, where a numbering that stripped
    it would join it.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    found = []
    for number, (column, values) in enumerate(SPELLED.items()):
        sec_rows, s_rows = _committed(), s_table
        for point, value in values.items():
            sec_rows = _set(column, [point], value)(sec_rows)
            s_rows = _set(column, [point], value)(s_rows)
        sec = _read(_sec_inputs(tmp_path / f"sec{number}", sec_rows), "decode")
        s = _read(temp_inputs(tmp_path / f"s{number}", model_path(TWIN),
                              model_points=s_rows), "s_decode")
        try:
            assert len(sec.Data.model_point_table()) == len(sec_rows)
            for point, value in values.items():
                want = ("raised", f"ValueError: invalid {column}")
                for model, name in ((sec, "SEC"), (s, "S")):
                    got = _did(_point(model, point).result_cf)
                    if got != want:
                        found.append(f"{name} {column} {value!r} on {point}: {got}")
        finally:
            s.close()
            sec.close()
    for column, (point, value, message) in SPACED_KEYS.items():
        model = _read_edited(tmp_path / column, _set(column, [point], value), "spaced")
        try:
            got = _did(model.Data.model_point_table)
        finally:
            model.close()
        if (got[0] != "raised" or message not in got[1]
                or f"point_id [{point}]" not in got[1]):
            found.append(f"{column} {value!r} on {point}: {got}")
    assert not found, "\n".join(found)


def _first_sorting(column, key):
    """An edit of a table keyed by ``column`` that writes its rows in reverse and adds a
    copy of ``key``'s rows under ``"0-first"``, a key that sorts before every other."""
    def edit(df):
        added = df[df[column] == key].assign(**{column: "0-first"})
        return pd.concat([df, added], ignore_index=True).iloc[::-1].reset_index(drop=True)
    return edit


def test_the_numberings_follow_the_keys(sec_model, tmp_path):
    """Each point's join number is its key's place among the table's keys, sorted, and
    each array's row of that number holds that key's rows, however the file is written.

    ``Data`` numbers the scenarios, the programmes and the sexes from 1 in the sorted
    order of their keys, and every array and every point's number read that one
    numbering.  A numbering by the order of the file, or two that disagree, reads another
    key's values wherever the two orders differ.  So the numbering is read twice: on the
    committed files, and on copies written in reverse with a key added that sorts before
    every other (:func:`_first_sorting`), so that every scenario and every programme
    numbers apart between the two.  On each, every point's number is its key's place in
    the sorted keys, plus 1, the scenario row of that number holds the key's first index
    level from its first month, and every point projects, on the copies, what it projects
    on the committed files, bit for bit.
    """
    edits = {SCENARIOS: _first_sorting("scenario_id", "up"),
             "withdrawal_table.csv": _first_sorting("wd_schedule_id", "worked"),
             "mort_table.csv": lambda df: df.iloc[::-1].reset_index(drop=True)}
    model = _read(_sec_inputs(tmp_path, _committed(), edits), "numbered")
    try:
        numbers = {}
        for tag, read in (("committed", sec_model), ("copies", model)):
            data, table = read.Data, read.Data.model_point_table()
            scenarios = read.Data.market_scenario().reset_index()
            for number, column, keys in (
                    ("scenario_number", "scenario_id", scenarios["scenario_id"]),
                    ("wd_schedule_number", "wd_schedule_id",
                     read.Data.withdrawal_table().reset_index()["wd_schedule_id"]),
                    ("mort_schedule", "sex", read.Data.mort_table().reset_index()["sex"])):
                order = sorted(set(keys))
                got = list(data.cells[number]())
                assert got == [order.index(k) + 1 for k in table[column]], (tag, number)
                numbers[tag, number] = got
            levels, starts = data.index_level_array(), data.scenario_first_mths()
            for sid, rows in scenarios.groupby("scenario_id"):
                s = sorted(set(scenarios["scenario_id"])).index(sid) + 1
                first = rows.sort_values("month_end").iloc[0]
                assert (starts[s], levels[s, starts[s]]) == (
                    first["month_end"], first["index_level"]), (tag, sid)
        for number in ("scenario_number", "wd_schedule_number"):
            assert all(a != b for a, b in zip(numbers["committed", number],
                                               numbers["copies", number])), number
        for key in point_keys(model):
            assert frame_mismatches(projection(sec_model, key).result_cf(),
                                    projection(model, key).result_cf(), rtol=0.0,
                                    atol=0.0) == [], key
            _release(model, key)
    finally:
        model.close()


def test_the_leg_codes_name_s_legs_in_s_order(sec_model, s_model):
    """``opt_leg(i)`` names, by code, ``RILA_US_S``'s ``opt_legs()[i]`` on every twin.

    ``RILA_US_S``'s ``opt_legs()``, a tuple of leg names, which no C type holds, is
    dropped for ``opt_leg_count()`` and ``opt_leg(i)``, int leg codes, and T1 exempts it
    (``SPEC.exempt``).  A leg mapped to another, a buffer's put for the cap's call, or two
    legs in another order, would price another portfolio, or sum one in another order,
    which T1 sees only to its tolerance.  So on the twins of S's fifteen points, every
    crediting type among them, the codes, named back by the SEC model's own References,
    are S's tuple, in its order, and an index past the count is refused.
    """
    named = {sec_model.Projection.refs[leg]: leg for leg in LEGS}
    assert sorted(named) == list(range(len(LEGS)))
    types = set()
    for point in S_POINTS:
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        count = mine.opt_leg_count()
        assert tuple(named[mine.opt_leg(i)] for i in range(count)) == theirs.opt_legs()
        _refused(lambda: mine.opt_leg(count), "invalid leg index")
        types.add(theirs.crediting_type())
    assert types == {"CAP", "STEP", "EDGE", "FLOOR"}, types


def _engine_args(p, t, basis):
    """``(spot, tau, mkt)`` at which ``RILA_US_S``'s engine prices what ``basis`` names."""
    if basis == "CURRENT":
        return p.index_level(t), p.tau(t), "CURRENT"
    if basis == "TERM_START":
        return p.index_at_term_start(t), float(p.term_years()), "TERM_START"
    return p.index_at_term_start(t), p.tau(t), "TERM_START"


def _bits(value):
    return value.hex() if type(value) is float else repr(value)


def _stepped_twins(df):
    """An edit of SEC's scenarios that runs the splice's paths (:data:`STEPPED`) under the
    ids S's points run on, as :func:`_stepped` runs them in S's file; every copy re-based
    to a row's month as committed."""
    return pd.concat([df[~df["scenario_id"].isin(STEPPED)], _stepped(None)],
                     ignore_index=True)


# The Floor option's floor set apart from its buffer, which it ships equal to, so that a
# floor read as the buffer, or the reverse, credits another number.
FLOOR_APART = _set("floor_rate", [6], 0.15)

# Rows the engine test adds, each the twin of S point 13, nge_reset, copied onto a path of
# its own, as (point_id, the columns changed): one-year terms, issued now at 40, so that the
# cap is solved fifty times in fifty markets, at buffers set apart from S's 10%.  On the
# twins' paths a regrouped comparison in the bisection, ``atm - (otm + otp)`` for ``atm -
# otm - otp``, solves every cap to the same bit; on these it moves solves on both rows.
NGE_YEARLY = ((101, {"policy_id": "RILA-T00101", "term_years": 1, "age_at_entry": 40,
                     "buffer": 0.2, "iv_family": "delta"}),
              (102, {"policy_id": "RILA-T00102", "term_years": 1, "age_at_entry": 40,
                     "sex": "M", "buffer": 0.15}))


def _yearly():
    """The engine test's own path, ``yearly``: every field steps every seven months to
    month 1,197, so that each one-year term starts on a market of its own, at levels
    written as closed forms of the step, which no library's random stream can move."""
    rows = [("yearly", 7 * k, 80.0 + (37 * k) % 53, 0.01 + 0.008 * ((13 * k) % 7),
             0.005 + 0.006 * ((17 * k) % 11), 0.004 * ((5 * k) % 7),
             0.10 + 0.025 * ((29 * k) % 13), "stepped for a test") for k in range(172)]
    return pd.DataFrame(rows, columns=["scenario_id", "month_end", "index_level", "mvr",
                                       "risk_free", "div_yield", "impl_vol", "provenance"])


def _with_yearly(table):
    """``table`` with :data:`NGE_YEARLY`'s rows added, each on :func:`_yearly`'s path and
    its own source, so that no twin of S point 13 but the committed one is found."""
    rows = []
    for point, columns in NGE_YEARLY:
        row = table.loc[[13]].assign(scenario_id="yearly",
                                     source_policy_id=columns["policy_id"], **columns)
        row.index = pd.Index([point], name=table.index.name)
        rows.append(row)
    return pd.concat([table, *rows])


def test_the_inlined_engine_is_s_engine_bit_for_bit(tmp_path):
    """The int-keyed pricing cells are ``RILA_US_S``'s engine, bit for bit (R14).

    The projection prices through ``opt_component_at(t, leg, basis)``, which writes
    ``RILA_US_S``'s Black-Scholes cells inline, and through the portfolios that sum it,
    ``credit_rate_by(t, rule)`` and the cap solve keyed by the term's start.  T1 compares
    S's keys to 1e-9 and C4 compiled with modelx, so a price an ulp off, a ``norm_cdf``
    written with another ``erf`` form, a leg priced on the other market, ``tau`` read as
    the term's length where ``tau(t)`` is due, or the floor credited as the buffer, could
    pass both where the two agree.  On the shipped paths the option-pricing market is flat
    and the Floor's floor equals its buffer, which hide the last two, so S and this model
    read the splice's stepped paths under S's ids (:func:`_stepped_twins`), every field of
    which steps within each term, with the floor set apart (:data:`FLOOR_APART`).  On the
    twins of S's fifteen points, in every month of the frame, each cell is held by
    ``float.hex`` to S's own engine cell at the arguments its basis stands for
    (:func:`_engine_args`): every leg on each basis to ``opt_component``, both portfolios
    to ``opt_portfolio`` and ``opt_portfolio_abs``, ``credit_rate_by`` to
    ``credit_rate_at(t, 1.0)`` and to S's ``credit_rate_accrued(t)``, and, on the twin
    under ``nge_reset``, ``declared_cap_solved`` to S's in every month.  And on every
    committed row, those in force and issued later among them, whose term began before
    the valuation month reads its start from the row, each is held the same way to this
    model's own engine cells, which are S's formulas.  The twins' and the rows' paths
    re-solve a cap a few times, where a regrouped comparison in the bisection solves the
    same bit, so two rows more under ``nge_reset`` re-solve a one-year cap fifty times on
    a path of their own (:data:`NGE_YEARLY`), the cap held to S's bisection on this
    model's engine (:func:`_solved_by_the_engine`).
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN),
                          model_points=FLOOR_APART(s_table),
                          edits={"market_scenario.csv": _stepped}), "s_engine")
    sec = _read(_sec_inputs(tmp_path / "sec", _with_yearly(FLOOR_APART(_committed())),
                            {SCENARIOS: lambda df: pd.concat(
                                [_stepped_twins(df), _yearly()], ignore_index=True)}),
                "engine")
    found = []
    try:
        pairs = [(f"twin {p}", _row(sec, "twin", p, 0), _point(s, p)) for p in S_POINTS]
        pairs += [(f"row {key}", projection(sec, key), projection(sec, key))
                  for key in point_keys(sec)]
        for where, mine, engine in pairs:
            found += _engine_faults(where, mine, engine)
    finally:
        sec.close()
        s.close()
    assert not found, f"{len(found)}: " + "\n".join(found[:20])


def _engine_faults(where, mine, engine):
    """Where ``mine``'s int-keyed pricing cells depart from ``engine``'s engine cells, by
    ``float.hex``, in every month of ``mine``'s frame from its first on the books."""
    found = []
    legs = [(code, name) for code, name in zip(_legs(mine), _legs(engine))]
    rules = {"TERM_END": lambda t: engine.credit_rate_at(t, 1.0),
             "PRORATED": (engine.credit_rate_accrued if engine is not mine else
                          lambda t: engine.credit_rate_at(
                              t, 1.0 - engine.tau(t) / engine.term_years()))}
    for t in range(mine.t_entry(), mine.proj_len()):
        for basis in BASES:
            code = _code(mine, basis)
            spot, tau, mkt = _engine_args(engine, t, basis)
            mkt = _code(engine, mkt)
            pairs_at = [(f"opt_component_at({t}, {leg}, {basis})",
                         mine.opt_component_at(t, leg, code),
                         engine.opt_component(t, name, spot, tau, mkt))
                        for leg, name in legs]
            pairs_at += [(f"opt_portfolio_at({t}, {basis})",
                          mine.opt_portfolio_at(t, code),
                          engine.opt_portfolio(t, spot, tau, mkt)),
                         (f"opt_portfolio_abs_at({t}, {basis})",
                          mine.opt_portfolio_abs_at(t, code),
                          engine.opt_portfolio_abs(t, spot, tau, mkt))]
            found += [f"{where}: {call} {_bits(got)}, the engine's {_bits(want)}"
                      for call, got, want in pairs_at if _bits(got) != _bits(want)]
        for rule, want in rules.items():
            got = mine.credit_rate_by(t, _code(mine, rule))
            if _bits(got) != _bits(want(t)):
                found.append(f"{where}: credit_rate_by({t}, {rule}) {_bits(got)}")
        if mine.nge_reset():
            got = mine.declared_cap_solved(t)
            want = (_solved_by_the_engine(mine, t) if engine is mine
                    else engine.declared_cap_solved(t))
            if _bits(got) != _bits(want):
                found.append(f"{where}: declared_cap_solved({t}) {_bits(got)}, "
                             f"{_bits(want)}")
    return found


def _solved_by_the_engine(p, t):
    """``RILA_US_S``'s bisection of ``declared_cap_solved``, on ``p``'s engine cell
    ``opt_budget_at_cap`` at the term's first month on the books."""
    if not p.is_active(t):
        return 0.0
    key = max(p.term_start_month(t) - p.duration_mth_init(), p.t_entry())
    target = p.opt_budget_target()
    lo, hi = 0.0, p.nge_cap_search_max
    for _ in range(p.nge_solve_iter):
        mid = 0.5 * (lo + hi)
        if p.opt_budget_at_cap(key, mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def test_sqrt_two_is_written_as_the_double_math_sqrt_returns():
    """The two pricing cells divide by ``1.4142135623730951``, ``math.sqrt(2.0)``'s double.

    ``RILA_US_S``'s ``norm_cdf`` divides by ``math.sqrt(2.0)``, a call each time; the
    inline copies write its value, which must be the same double, or every price moves by
    an ulp.  So the literal is that double, and each of the two cells writes it, and
    never the call.
    """
    assert math.sqrt(2.0) == 1.4142135623730951
    source = (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8")
    cells = {node.name: "\n".join(ast.get_source_segment(source, statement)
                                  for statement in node.body[1:])
             for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}
    for name in ("opt_component_at", "cap_solved_at_start"):
        code = cells[name]
        assert "1.4142135623730951" in code and "sqrt(2" not in code, name


def test_the_cap_is_solved_once_a_term_keyed_by_its_first_month_on_the_books(tmp_path):
    """``cap_solved_at_start`` is asked once a term, at the term's first month on the books.

    ``RILA_US_S`` repeats the cap's bisection in every month of a renewal term on the same
    market; here each month reads ``cap_solved_at_start`` at the term's Term Start Date as
    a month from the valuation date, or ``t_entry()`` for the term under way there, so it
    solves once a term.  Keyed on the month, it would give the same numbers, and solve
    in every month, which no comparison sees.  So on a model just read, every month of
    each committed row under ``nge_reset`` asks for ``declared_cap_solved``, and the
    keys ``cap_solved_at_start`` then holds are exactly the first months on the books of
    the renewal terms in the frame, none after a month that reads it nor before
    ``t_entry()``.
    """
    model = _read(model_path(SEC), "solved")
    try:
        table = model.Data.model_point_table()
        rows = [p for p in table.index if table.at[p, "nge_reset"]]
        assert len(rows) == 3, rows
        solves = 0
        for label in rows:
            p = _point(model, label)
            d, entry, want = p.duration_mth_init(), p.t_entry(), set()
            for t in range(entry, p.proj_len()):
                p.declared_cap_solved(t)
                want.add(max(p.term_start_month(t) - d, entry))
            keys = {key if isinstance(key, int) else key[0]
                    for key in p.cells["cap_solved_at_start"].keys()}
            assert keys == want, (label, sorted(keys), sorted(want))
            solves += len(keys)
        assert solves == 4, solves
    finally:
        model.close()


def _floors_for(*terms):
    """An edit of the floors table adding a row for each of ``terms``, the 6-year floors."""
    return lambda df: pd.concat([df, *(df[df["term_years"] == 6].assign(term_years=term)
                                       for term in terms)], ignore_index=True)


def _market_at(month, **columns):
    """An edit of a scenario table setting ``columns`` on every scenario at ``month``,
    the month 1 row, where none was, the month 0 row's as it was, first."""
    def edit(df):
        df = df.copy()
        if month == 0 and "mvr" in columns:
            ones = df[df["month_end"] == 0].assign(month_end=1)
            ones = ones[~ones["scenario_id"].isin(df.loc[df["month_end"] == 1,
                                                         "scenario_id"])]
            df = pd.concat([df, ones], ignore_index=True)
        at = df["month_end"] == month
        for column, value in columns.items():
            df.loc[at, column] = value
        return df.sort_values(["scenario_id", "month_end"], kind="stable").reset_index(
            drop=True)
    return edit


_VOL = 1.3407807929942596e154

# The powers a value Data accepts, or a moved Reference, takes off their domain (the
# Projection docstring's *Powers*; the critique of M25's design, M1 and M2), each beside
# RILA_US_S's own outcome, as (case, S point, References, the table's edit, the files'
# edits, [(cell, arguments, SEC's outcome)], S's outcome of the first call).  An outcome
# "S" is S's float, bit for bit; "complex" S's complex number; and any other text the
# raise, whole.  Each bound is met on both sides, a case that projects beside one refused.
# S's own `**` overflow raises with the platform's text for ERANGE: "Result too large" on
# Windows, "Numerical result out of range" with glibc (Tests run 30's Linux leg).
_S_OVERFLOW = f"OverflowError: (34, '{os.strerror(errno.ERANGE)}')"

_FAR = "is past the largest float"
POWERS = [
    ("a one-year term's budget past 1: an integral power of a negative base", 4, {},
     _set("declared_step", [4], 3.0), {},
     [("fixed_leg_yield", (0,), "S"), ("fixed_leg_yield", (11,), "S"),
      ("result_cf", (), "S")], "S"),
    ("a three-year term's budget past 1: a fractional power of a negative base", 4, {},
     _both(_set("declared_step", [4], 3.0), _set("term_years", [4], 3)), {},
     [("fixed_leg_yield", (0,), "ValueError: point_id 4: fixed_leg_yield(0): 1 - "
       "opt_budget, -0.2664927419869585, is below 0, and its power -1 / term_years is no "
       "real number"), ("result_cf", (), "S")], "complex"),
    ("the notional's base of 0 at a term end, a power of -0.0, and before it", 7,
     {"iv_credit_spread": -1.04}, None, {},
     [("fixed_proxy_factor", (71,), "S"),
      ("fixed_proxy_factor", (70,), "ZeroDivisionError: 0.0 cannot be raised to a "
       "negative power")], "S"),
    ("the accounts' twelfth root of 0", 1,
     {"declared_acct_rate": -1.0, "guar_min_acct_rate": -1.0}, None, {},
     [("fixed_acct_pp", (75,), "S"), ("result_cf", (), "S")], "S"),
    ("the accounts' twelfth root of a negative base", 1,
     {"declared_acct_rate": -1.5, "guar_min_acct_rate": -1.5}, None, {},
     [("fixed_acct_pp", (0,), "ValueError: point_id 1: fixed_acct_pp(0): 1 + acct_rate, "
       "-0.5, is below 0, and its power 1 / 12 is no real number"),
      ("holding_acct_pp", (0,), "ValueError: point_id 1: holding_acct_pp(0): 1 + "
       "acct_rate, -0.5, is below 0, and its power 1 / 12 is no real number")],
     "TypeError: '>' not supported between instances of 'complex' and 'float'"),
    ("a surrender rate of certainty, lapse_rate_max 1", 1,
     {"lapse_rate_max": 1.0, "lapse_shock_mult": 100.0}, None, {},
     [("lapse_rate_mth", (71,), "S"), ("result_cf", (), "S")], "S"),
    ("a surrender rate past certainty, lapse_rate_max 2", 1,
     {"lapse_rate_max": 2.0, "lapse_shock_mult": 100.0}, None, {},
     [("lapse_rate_mth", (71,), "ValueError: point_id 1: lapse_rate_mth(71): 1 - "
       "lapse_rate, -1.0, is below 0, lapse_rate_max being above 1, and its power 1 / 12 "
       "is no real number")], "complex"),
    ("the cap solve's base of 0", 13, {"earned_rate": -1.0, "nge_spread": 0.0}, None, {},
     [("opt_budget_target", (), "ZeroDivisionError: 0.0 cannot be raised to a negative "
       "power")], "ZeroDivisionError: 0.0 cannot be raised to a negative power"),
    ("inflation to the largest float and past it", 1, {"inflation_rate": 1e154}, None, {},
     [("inflation_factor", (24,), "S"),
      ("inflation_factor", (36,), f"OverflowError: point_id 1: inflation_factor(36): "
       f"1e+154 ** 3 {_FAR}")], "S"),
    ("a volatility whose square is the largest float", 1, {}, None,
     {SCENARIOS: _market_at(0, impl_vol=_VOL)}, [("result_cf", (), "S")], "S"),
    ("a volatility whose square is past the largest float", 1, {}, None,
     {SCENARIOS: _market_at(0, impl_vol=math.nextafter(_VOL, math.inf))},
     [("result_cf", (), f"OverflowError: point_id 1: opt_component_at(0, 0, 1), the "
       f"volatility 1.3407807929942597e+154 squared, {_FAR}")],
     _S_OVERFLOW),
    ("the interim value's rate adjustment below the largest float", 1, {}, None,
     {SCENARIOS: _market_at(0, mvr=1e50)}, [("mva_factor", (0,), "S")], "S"),
    ("the interim value's rate adjustment past the largest float", 1, {}, None,
     {SCENARIOS: _market_at(0, mvr=1e60)},
     [("mva_factor", (0,), f"OverflowError: point_id 1: mva_factor(0): "
       f"9.615384615384615e+59 ** 5.916666666666667 {_FAR}")],
     _S_OVERFLOW),
    ("the notional's discount on a 150-year term", 7, {"iv_credit_spread": -1.03},
     _set("term_years", [7], 150), {"guar_min_rate_table.csv": _floors_for(150)},
     [("fixed_proxy_factor", (0,), "S"), ("result_cf", (), "S")], "S"),
    ("the notional's discount on a 200-year term, past the largest float", 7,
     {"iv_credit_spread": -1.03}, _set("term_years", [7], 200),
     {"guar_min_rate_table.csv": _floors_for(200)},
     [("fixed_proxy_factor", (0,), f"OverflowError: point_id 7: fixed_proxy_factor(0): "
       f"0.010000000000000009 ** -199.91666666666666 {_FAR}")],
     _S_OVERFLOW),
    ("math.exp past the largest float, on a dividend yield near -1", 1, {},
     _set("term_years", [1], 20), {"guar_min_rate_table.csv": _floors_for(20),
                                   SCENARIOS: _market_at(0, div_yield=-1 + 2.0 ** -52)},
     [("opt_budget", (0,), "OverflowError: math range error")],
     "OverflowError: math range error"),
]


def _power_case(tmp_path, case, s_point, refs, edit, files):
    """S's and SEC's folders for a case of :data:`POWERS`: each table with ``edit``, the
    twin keeping S's label, and each with ``files``, the scenario edit on both models'
    scenario files."""
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s_files = {("market_scenario.csv" if file == SCENARIOS else file): change
               for file, change in files.items()}
    edit = edit or (lambda t: t)
    s = temp_inputs(tmp_path / "s", model_path(TWIN), model_points=edit(s_table),
                    edits=s_files)
    sec = _sec_inputs(tmp_path / "sec", edit(_committed()), files)
    return s, sec


@pytest.mark.parametrize("case, s_point, refs, edit, files, calls, s_did", POWERS,
                         ids=[c[0] for c in POWERS])
def test_a_power_off_its_domain_is_refused_beside_s(tmp_path, case, s_point, refs, edit,
                                                    files, calls, s_did):
    """A power is taken as ``RILA_US_S`` takes it, and refused only where S has no float.

    Compiled, a ``**`` is C's ``pow``, which raises nowhere: a base of 0 under a negative
    power gives ``inf``, a negative base under a fractional one NaN, and a result past the
    largest float ``inf``, where Python's ``**`` raises or returns a complex number.  So
    each power whose base or size inputs can take there is guarded, in both engines (the
    Projection docstring's *Powers*), and each case of :data:`POWERS` is read by S and by
    this model, from copies with the same table and files, under the same References:
    where S has a float, this model's is S's, bit for bit, the base of 0 under a power of
    ``-0.0`` and a negative base under a whole number among them; where S raises
    ``ZeroDivisionError`` or ``math``'s ``OverflowError``, this model raises S's own;
    where S returns a complex number, or raises downstream of one, this model refuses,
    naming the point and the base; and where S's power overflows, with Python's message,
    this model refuses before the power, naming the point, the base and the exponent.  A
    guard that refused where S has a float, or one lost, so that a compiled ``inf`` or NaN
    goes on, fails a case; :func:`test_the_compiled_model_takes_a_power_as_modelx_does`
    holds the compiled model to these.

    The bound's case is posed only where ``pandas.read_csv`` reads :data:`_VOL` back as
    itself.  Its default parser is not correctly rounded everywhere: on a Windows build it
    reads ``1.3407807929942596e+154`` as the next float up, past the bound, so both models
    see the case beside it, and the bound cannot be written to a file at all.
    """
    if (case == "a volatility whose square is the largest float"
            and pd.read_csv(io.StringIO(f"v\n{_VOL!r}\n"))["v"].iloc[0] != _VOL):
        pytest.skip("pandas.read_csv reads the bound volatility as the next float up here")
    s_folder, sec_folder = _power_case(tmp_path, case, s_point, refs, edit, files)
    s = _read(s_folder, "s_power", refs)
    sec = _read(sec_folder, "power", refs)
    try:
        theirs, mine = _point(s, s_point), _row(sec, "twin", s_point, 0)
        found = []
        for number, (cell, args, want) in enumerate(calls):
            got = _did(lambda: mine.cells[cell](*args))
            s_got = _did(lambda: theirs.cells[cell](*args))
            if number == 0:
                kinds = {float: "S", pd.DataFrame: "S", complex: "complex"}
                kind = (kinds.get(type(s_got[1]), s_got[1]) if s_got[0] == "ok"
                        else s_got[1])
                if kind != s_did:
                    found.append(f"{cell}{args}: S {s_got}, not {s_did}")
            if want != "S":
                if got != ("raised", want):
                    found.append(f"{cell}{args}: {got}, not {want}")
            elif cell == "result_cf":
                if got[0] != "ok" or s_got[0] != "ok" or frame_mismatches(
                        s_got[1], got[1], rtol=0.0, atol=0.0):
                    found.append(f"{cell}: {got[0]}, S {s_got[0]}, apart")
            elif not (got[0] == s_got[0] == "ok" and _bits(got[1]) == _bits(s_got[1])):
                found.append(f"{cell}{args}: {got}, S {s_got}")
    finally:
        sec.close()
        s.close()
    assert not found, "\n".join(found)


# What the caches cannot hold, refused by proj_len() before any frame is read, naming the
# point, as (case, the table's edit, the label, the files' edits, the References, the
# message, RILA_US_S's outcome on the same table and files, the References and Data
# References that issue it, its frame then).  The issue ages are moved through their
# References on the anchor's twin, issued at 60; the shipped mortality, to 120, rates an
# issue age of 111 to the end of its ten-year minimum cover, and 112 past it, which S
# refuses too, with pandas' KeyError; a table cut at 110 is short of 102's cover; and on a
# table extended to 125 with issue_age_max moved to 113, the cover needs age 122, past
# read_last_age, which only a raised Data.read_last_age admits.  The issue age's rule is
# asked before the table's.  S's outcome is None where S has no such Reference.
def _mortality_to(last):
    """An edit of the mortality table ending at ``last``: cut there, or extended to it by
    the last age's rates."""
    def edit(df):
        df = df[df["age"] <= last]
        top = int(df["age"].max())
        return pd.concat([df, *(df[df["age"] == top].assign(age=age)
                                for age in range(top + 1, last + 1))], ignore_index=True)
    return edit


NOT_ISSUED = [
    ("an issue age below issue_age_min", None, 1, {}, {"issue_age_min": 61},
     "point_id 1: age_at_entry 60 is below issue_age_min, 61", None,
     ({"issue_age_min": 60}, {}), 360),
    ("an issue age above issue_age_max", None, 1, {}, {"issue_age_max": 59},
     "point_id 1: age_at_entry 60 is above issue_age_max, 59, the oldest issue age the "
     "compiled model holds", None, ({"issue_age_max": 60}, {}), 360),
    ("an issue age of 112, past issue_age_max", _set("age_at_entry", [1], 112), 1, {}, {},
     "point_id 1: age_at_entry 112 is above issue_age_max, 111, the oldest issue age the "
     "compiled model holds", "KeyError: (121, 'M')", None, None),
    ("a mortality table short of the cover", _set("age_at_entry", [1], 102), 1,
     {"mort_table.csv": _mortality_to(110)}, {},
     "point_id 1: the mortality table rates its sex to age 110, short of age 111, at "
     "which its last covered year is entered", "KeyError: (111, 'M')", None, None),
    ("a cover past read_last_age", _set("age_at_entry", [1], 113), 1,
     {"mort_table.csv": _mortality_to(125)}, {"issue_age_max": 113},
     "point_id 1: its last covered year is entered at age 122, past read_last_age, 121, "
     "the oldest age the compiled model holds", "ok",
     ({"issue_age_max": 113}, {"read_last_age": 122}), 120),
    ("an issue age past issue_age_max on a table short of it: the age's rule first",
     _set("age_at_entry", [1], 112), 1, {"mort_table.csv": _mortality_to(115)}, {},
     "point_id 1: age_at_entry 112 is above issue_age_max, 111, the oldest issue age the "
     "compiled model holds", "KeyError: (116, 'M')", None, None),
]

# The issue ages just inside, each projecting its whole cover at the shipped References,
# as (the table's edit, the label, the files' edits, the frame): 111, the oldest, on the
# shipped mortality; 102 on the table that rates it to 111; and 0, the youngest, on a
# table extended below 40 (_extended_mortality).
JUST_ISSUED = [(_set("age_at_entry", [1], 111), 1, {}, 120),
               (_set("age_at_entry", [1], 102), 1, {"mort_table.csv": _mortality_to(111)},
                120),
               (_set("age_at_entry", [1], 0), 1, {"mort_table.csv": _extended_mortality},
                1080)]


@pytest.mark.parametrize("case, edit, label, files, refs, message, s_did, issue, frame",
                         NOT_ISSUED, ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(
        tmp_path, case, edit, label, files, refs, message, s_did, issue, frame):
    """``proj_len()`` refuses a point the caches cannot hold, naming it (§6.1, F4).

    ``RILA_US_S`` projects a contract at any issue age its mortality table rates for its
    cover, but the compiled caches are sized from the contract (``spec_sec.py``): issue
    ages from ``issue_age_min``, 0, to ``issue_age_max``, 111, the oldest S projects on
    the shipped tables, and attained ages to ``Data.read_last_age``, 121.  A point past
    them would run past a cache, so ``proj_len()`` refuses it before any frame is read:
    each case of :data:`NOT_ISSUED`, by the rule asked first, the issue ages before the
    table.  The table reads, since these are rules of the product, and every report is
    refused, with ``proj_len()`` itself.  Beside it, ``RILA_US_S`` on the same table and
    files: where it refuses too, with pandas' ``KeyError`` where it first reads an age the
    table lacks, this model refuses by name before reading any; where it projects, a cover
    past ``read_last_age``, the refusal is this model's, a recorded departure reached only
    through a moved ``issue_age_max``.  Each case that a Reference refuses projects once
    the Reference is moved, its checks passing: a bound off by one, a rule lost or asked in
    another order lets a point through or names the wrong rule.  The issue ages just
    inside (:data:`JUST_ISSUED`) project their whole cover at the shipped References.
    """
    model = _read_edited(tmp_path / "sec", edit, "not_issued", refs, files)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        p = _point(model, label)
        for cell in (*REPORTS, "proj_len"):
            _refused(p.cells[cell], message)
    finally:
        model.close()
    if s_did is not None:
        s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                              index_col="point_id")
        s_files = {f: e for f, e in files.items()}
        s = _read(temp_inputs(tmp_path / "s", model_path(TWIN),
                              model_points=(edit or (lambda t: t))(s_table),
                              edits=s_files), "s_not_issued")
        try:
            got = _did(lambda: len(_point(s, label).result_cf()))
        finally:
            s.close()
        assert (got[0] if s_did == "ok" else got[1]) == s_did, got
    if issue is None:
        if case != NOT_ISSUED[0][0]:
            return
        for number, (inside, at, more, cover) in enumerate(JUST_ISSUED):
            model = _read_edited(tmp_path / f"inside{number}", inside, "inside", None, more)
            try:
                p = _point(model, at)
                assert p.proj_len() == len(p.result_cf()) == cover, at
                assert all(p.cells[check]() for check in CHECKS), at
            finally:
                model.close()
        return
    proj_refs, data_refs = issue
    model = _read(_sec_inputs(tmp_path / "issued", (edit or (lambda t: t))(_committed()),
                              files), "issued", proj_refs, data_refs)
    try:
        p = _point(model, label)
        assert p.proj_len() == len(p.result_cf()) == frame
        assert all(p.cells[check]() for check in CHECKS)
    finally:
        model.close()


# A whole number of 2**53 or more in an int column, which an int64 cannot be trusted to
# hold, as (column, its value, the files' edits that admit it at load): a term of 2**60
# and one of 1e20, each of which the floors table may name; and an issue age of 2**53 on a
# female point, which a mortality table of one female row at that age rates.
def _female_at(age):
    """An edit of the mortality table whose female rows are one row, at ``age``."""
    return lambda df: pd.concat([df[df["sex"] == "M"],
                                 df[df["sex"] == "F"].iloc[[0]].assign(age=age)],
                                ignore_index=True)


HUGE = [("term_years", 2 ** 60, {"guar_min_rate_table.csv": _floors_for(2 ** 60)}),
        ("term_years", 1e20, {"guar_min_rate_table.csv": _floors_for(1e20)}),
        ("age_at_entry", 2 ** 53, {"mort_table.csv": _female_at(2 ** 53)})]


@pytest.mark.parametrize("column, value, files", HUGE,
                         ids=[f"{c[0]} {c[1]:.3g}" for c in HUGE])
def test_an_int_column_past_2_53_is_refused_by_its_point_alone(tmp_path, column, value,
                                                               files):
    """A whole number of ``2**53`` or more is refused by the point that holds it, alone.

    ``Data`` holds each int column in an int64 vector, which a float past ``2**63`` casts
    to the least int64 without a word, and compiled, ``12 * term_years()`` in C wraps where
    Python's int grows.  So a value of ``2**53`` or more is never cast: ``Data`` keeps a
    0/1 vector beside the column (``Data.term_years_ok`` and the two beside it), and the
    point's own accessor refuses it, naming the point, before any clock reads it, while
    every other point of the table projects.  Each case of :data:`HUGE` reads, the floors
    table naming the term or the mortality rating the age, and the point's ``result_cf``
    is refused by name; the anchor's twin, point 1, projects its 360 months; and
    ``RILA_US_S`` projects the term on the same files, its exact ints never wrapping, a
    recorded refusal of this model's (USLIB-SEC-PLAN.md template item 4).
    """
    label, sex = (4, "F") if column == "age_at_entry" else (2, None)
    edit = _set(column, [label], value)
    if sex:
        edit = _both(lambda t: t[(t["sex"] != sex) | (t.index == label)], edit)
    model = _read_edited(tmp_path / "sec", edit, "huge", None, files)
    try:
        ok = model.Data.cells[f"{column}_ok"]()
        assert list(ok).count(0) == 1, ok
        _refused(_point(model, label).result_cf,
                 f"point_id {label}: {column} must be below 2**53 in size; it is not")
        assert len(_point(model, 1).result_cf()) == 360
        if sex:
            assert model.Data.model_point_table().at[label, "sex"] == sex
    finally:
        model.close()
    if column != "term_years":
        return
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=edit(s_table),
                          edits=files), "s_huge")
    try:
        assert len(_point(s, label).result_cf()) == 360
    finally:
        s.close()


# run_sec.py run as though it sat at /m/products/registered_index_linked_annuity, a copy
# too shallow to have a repository above it: the source compiled under that name, so that
# its own __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/registered_index_linked_annuity/run_sec.py"
sys.argv = [where, "--cython"]
exec(compile(source, where, "exec"), {"__name__": "__main__", "__file__": where})
"""


def test_run_sec_says_a_copy_without_the_repository_cannot_build(tmp_path):
    """``run_sec.py --cython`` outside the repository stops, saying it cannot build.

    ``--cython`` builds with the repository's ``tools/build_sec_cy.py``, which a
    ``lifelib.create()`` copy does not carry, wherever the copy is: beside a copy of the
    model and its inputs, and at a path too shallow to hold a repository above the product
    at all.  Each must exit nonzero having printed nothing, and say why.  Neither needs
    modelx-cython, since neither gets as far as building, so this runs wherever the module
    does, on Windows and macOS among them.
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


def _runner_functions(names):
    """The runner's functions ``names``, read from ``run_sec.py``, which runs the model
    when imported, as a module's body of their own."""
    tree = ast.parse((model_path(SEC).parent / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in names]
    assert len(found) == len(names), [node.name for node in found]
    return ast.Module(found, [])


def test_run_sec_rebuilds_in_place_exactly_when_a_source_is_newer(tmp_path):
    """``run_sec.py --cython`` rebuilds its package where, and only where, it is stale.

    ``compiled_model`` builds in place when no build for this interpreter is there, or
    when the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it, and
    otherwise imports what is there.  So its two functions are read from the runner and
    run here on a fake product: empty sources, a tool and an empty file standing for the
    extension module, their times set by ``os.utime``, with the build and the import
    stubbed, so that nothing is built or imported.  Built after every source, it must not
    build; with any one source newer than the build, or no build, it must, and say so on
    stderr.
    """
    module = _runner_functions(("_built", "compiled_model"))
    here = tmp_path / "product"
    tool = tmp_path / "tools" / "build_sec_cy.py"
    sources = [here / SEC / "Projection" / "__init__.py",
               here / SEC / "Data" / "__init__.py", here / SEC / "__init__.py",
               here / "sample_sec.py", here / "spec_sec.py", tool]
    for path in sources:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    suffix = importlib.machinery.EXTENSION_SUFFIXES[0]
    built = here / f"{SEC}_nomx_cy" / f"_mx_classes{suffix}"
    built.parent.mkdir()
    builds = []

    class Imported(Exception):
        """Raised by the stubbed import, once the runner has decided."""

    def run(args, **kwargs):
        builds.append(args)
        return types.SimpleNamespace(returncode=0)

    def import_module(name):
        raise Imported(name)

    stub = types.SimpleNamespace(path=[], modules={}, executable=sys.executable,
                                 exit=sys.exit, stderr=None)
    space = {"HERE": here, "NAME": SEC, "SUFFIXES": (suffix,), "Path": pathlib.Path,
             "sys": stub, "subprocess": types.SimpleNamespace(run=run, DEVNULL=None),
             "importlib": types.SimpleNamespace(import_module=import_module),
             "_tool": lambda: tool}
    exec(compile(module, "run_sec.py", "exec"), space)

    def rebuilt(newer=None):
        base = 1_000_000_000
        for path in sources:
            os.utime(path, (base, base))
        if built.exists():
            os.utime(built, (base + 10, base + 10))
        if newer is not None:
            os.utime(newer, (base + 20, base + 20))
        builds.clear()
        said = []
        stub.stderr = types.SimpleNamespace(write=said.append, flush=lambda: None)
        with pytest.raises(Imported):
            space["compiled_model"](None)
        assert ("building" in "".join(said)) == bool(builds)
        return builds == [[sys.executable, str(tool), str(here)]]

    built.write_bytes(b"")
    assert not rebuilt(), "built after every source, the runner rebuilt"
    for source in sources:
        assert rebuilt(source), f"{source.name} newer than the build, the runner did not"
    built.unlink()
    assert rebuilt(), "with no build, the runner did not build"


def test_run_sec_refuses_a_package_that_imports_without_its_extension_modules(tmp_path):
    """``run_sec.py --cython`` stops, saying why, where the package imports uncompiled.

    A compiled package whose extension module does not load falls back to the
    ``_mx_classes.py`` beside it, which computes the same numbers uncompiled, so no output
    can show it, and ``compiled_model`` checks the file its ``Projection``'s class came
    from.  Its two functions are read from the runner and run here on a fake product, as
    :func:`test_run_sec_rebuilds_in_place_exactly_when_a_source_is_newer` runs them:
    empty sources and an empty file standing for the extension module, built after every
    source, so that the runner does not build, and a stubbed import whose ``Projection``
    comes from the extension module or from ``_mx_classes.py``.  In place and from
    ``--build DIR``, the package whose extension is missing must be refused, saying so,
    and the one whose extension loaded returned; nothing is built either way.  This needs
    neither modelx-cython nor a compiler, so it runs wherever the module does.
    """
    module = _runner_functions(("_built", "compiled_model"))
    here = tmp_path / "product"
    tool = tmp_path / "tools" / "build_sec_cy.py"
    sources = [here / SEC / "Projection" / "__init__.py",
               here / SEC / "Data" / "__init__.py", here / SEC / "__init__.py",
               here / "sample_sec.py", here / "spec_sec.py", tool]
    for path in sources:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    suffix = importlib.machinery.EXTENSION_SUFFIXES[0]
    package = here / f"{SEC}_nomx_cy"
    built = package / f"_mx_classes{suffix}"
    package.mkdir()
    built.write_bytes(b"")
    base = 1_000_000_000
    for path in sources:
        os.utime(path, (base, base))
    os.utime(built, (base + 10, base + 10))
    builds = []

    def run(args, **kwargs):
        builds.append(args)
        return types.SimpleNamespace(returncode=0)

    class Space:
        """The compiled ``Projection``'s class; ``stub.modules`` gives its module's file."""

    Space.__module__ = f"{SEC}_nomx_cy._mx_classes"
    model = types.SimpleNamespace(Projection=Space())
    stub = types.SimpleNamespace(path=[], modules={}, executable=sys.executable,
                                 exit=sys.exit, stderr=None)

    def import_module(name):
        assert name == f"{SEC}_nomx_cy", name
        return types.SimpleNamespace(mx_model=model)

    space = {"HERE": here, "NAME": SEC, "SUFFIXES": (suffix,), "Path": pathlib.Path,
             "sys": stub, "subprocess": types.SimpleNamespace(run=run, DEVNULL=None),
             "importlib": types.SimpleNamespace(import_module=import_module),
             "_tool": lambda: tool}
    exec(compile(module, "run_sec.py", "exec"), space)
    said = []
    stub.stderr = types.SimpleNamespace(write=said.append, flush=lambda: None)
    for build_dir in (None, str(here)):
        for loaded, compiled in ((built, True), (package / "_mx_classes.py", False)):
            stub.modules = {Space.__module__: types.SimpleNamespace(__file__=str(loaded))}
            if compiled:
                assert space["compiled_model"](build_dir) is model, (build_dir, loaded)
                continue
            with pytest.raises(SystemExit) as refused:
                space["compiled_model"](build_dir)
            message = str(refused.value.code)
            assert "imported without its extension modules" in message, (build_dir,
                                                                          message)
            assert package.name in message, message
    assert builds == [] and said == [], (builds, said)


def test_the_runner_sums_the_block_as_groupby_does(sec_model):
    """``run_sec.py``'s running sum of the block is pandas' ``groupby`` sum, bit for bit.

    A block run keeps one point's frame at a time, so it sums the frames as it goes,
    compensated, with ``add``, so that the block is the frames concatenated and summed by
    ``t``, to the last bit (USLIB-SEC-PLAN.md §7.9, *Record -- M23*, carried).  The
    printed block, to two decimals, cannot show a last bit, so ``add`` itself is read
    from the runner and run here on the committed points' frames.  A plain running sum
    differs from ``groupby``'s on them, so the comparison can fail.
    """
    space = {}
    exec(compile(_runner_functions(("add",)), "run_sec.py", "exec"), space)
    frames = [projection(sec_model, key).result_cf() for key in point_keys(sec_model)]
    columns = list(frames[0].columns)
    rows = max(len(frame) for frame in frames)
    total, compensation = np.zeros((rows, len(columns))), np.zeros((rows, len(columns)))
    plain = np.zeros((rows, len(columns)))
    for frame in frames:
        space["add"](total, compensation, frame[columns].to_numpy())
        plain[:len(frame)] += frame[columns].to_numpy()
    want = pd.concat(frames).groupby(level="t").sum()[columns].to_numpy()
    assert np.array_equal(total, want)
    assert not np.array_equal(plain, want)


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when Phase 1 ended (C2).

    Phase 2 changes how the model is represented and no number it computes (D2), so before
    it changed anything the model as Phase 1 left it was frozen below, at M13
    (USLIB-SEC-PLAN.md §5.4): for each point, each column of ``result_cf()`` and
    ``result_pols()``, its sum, its largest absolute value and its values at five fixed
    months, the frame's first and last and the three quartiles between.  Every later version
    must reproduce it, to 1e-12 relative, floored at 1e-12 of the column's own magnitude
    (``sec_support.fingerprint_mismatches``), with the same points, frames and columns
    exactly.  ``python tools/gen_sec_fingerprint.py RILA_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# RILA_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: RILA_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (153.99949605897504, 1.0, (
                1.0, 0.6870046052090497, 0.3433495539227757, 0.14837344612115183,
                0.04674634865189109)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (32696.920659205938, 114.44251406585195, (
                45.95168679397777, 91.29762742252119, 98.79162008363946, 106.38049478484044,
                76.68109346362904)),
            "claims_lapse": (105570.20731548713, 12454.885723241885, (
                156.51828285334597, 506.5790291329002, 267.6293317154337,
                125.83895450661993, 889.4195040872157)),
            "claims_maturity": (7611.30167390163, 7611.30167390163, (
                0.0, 0.0, 0.0, 0.0, 7611.30167390163)),
            "expenses": (7159.80974002473, 6205.0, (
                6205.0, 4.083162934582259, 2.425719655679512, 1.2771774050128315,
                0.47831036767151375)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-53038.239388619426, 93592.53003035267, (
                93592.53003035267, -601.9598194900036, -368.84667145475265,
                -233.4966266964732, -8577.880581820145)),
        },
        "result_pols": {
            "pols_if": (153.99949605897504, 1.0, (
                1.0, 0.6870046052090497, 0.3433495539227757, 0.14837344612115183,
                0.04674634865189109)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.21904616350000064, 0.0007373640889500974, (
                0.00045907401398581626, 0.0006361905035031719, 0.0006506040753253215,
                0.0006422980231613, 0.0004179075455035234)),
            "pols_lapse": (0.7394726804946288, 0.08893057043507308, (
                0.0016813703248057914, 0.003530001564188599, 0.0017625050965176857,
                0.0007597831903279014, 0.004847285101018411)),
            "pols_lapse_term": (0.1760338523097303, 0.0845591980066141, (
                0.0, 0.0, 0.0, 0.0, 0.004609017333929906)),
            "pols_maturity": (0.041481156005369155, 0.041481156005369155, (
                0.0, 0.0, 0.0, 0.0, 0.041481156005369155)),
            "pols_if_aft_decr": (153.04097721498042, 0.9978595556612084, (
                0.9978595556612084, 0.682838413141358, 0.3409364447509327,
                0.14697136490766263, 0.041481156005369155)),
        },
    },
    2: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (155.58392483877915, 1.0, (
                1.0, 0.6974274815923089, 0.34855867469089036, 0.15062449083868826,
                0.04745555992889431)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (7409.506172759155, 7409.506172759155, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (20545.06949455082, 67.79355635632393, (
                45.95168679397777, 58.49161547046699, 59.81680516747576, 59.38261659734363,
                42.80412478458075)),
            "claims_lapse": (60965.64542097879, 6952.43714708118, (
                156.51828285334597, 282.7772922479424, 149.39327014415852,
                70.24451619247455, 496.4825319926699)),
            "claims_maturity": (4248.7018886513815, 4248.7018886513815, (
                0.0, 0.0, 0.0, 0.0, 4248.7018886513815)),
            "expenses": (7170.444256859122, 6205.0, (
                6205.0, 4.145110557927385, 2.4625214120576957, 1.296554076014754,
                0.48556704367815345)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-339.36723379929026, 93592.53003035267, (
                93592.53003035267, -345.4140182763368, -211.67259672369198,
                -130.92368686583293, -4788.4741124723105)),
        },
        "result_pols": {
            "pols_if": (155.58392483877915, 1.0, (
                1.0, 0.6974274815923089, 0.34855867469089036, 0.15062449083868826,
                0.04745555992889431)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.22195501707561016, 0.0007485509932158172, (
                0.00045907401398581626, 0.0006458424547767725, 0.0006604747018104207,
                0.0006520426345450698, 0.00042424782132320166)),
            "pols_lapse": (0.7359344964050754, 0.09027977877415755, (
                0.0016813703248057914, 0.0035835569110629537, 0.0017892449067119438,
                0.0007713102255338106, 0.004920825588257149)),
            "pols_lapse_term": (0.17870454631670132, 0.08584208615788388, (
                0.0, 0.0, 0.0, 0.0, 0.004678942946590441)),
            "pols_maturity": (0.04211048651931397, 0.04211048651931397, (
                0.0, 0.0, 0.0, 0.0, 0.04211048651931397)),
            "pols_if_aft_decr": (154.62603532529846, 0.9978595556612084, (
                0.9978595556612084, 0.6931980822264693, 0.346108955082368,
                0.14920113797860937, 0.04211048651931397)),
        },
    },
    3: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (153.99949605897504, 1.0, (
                1.0, 0.6870046052090497, 0.3433495539227757, 0.14837344612115183,
                0.04674634865189109)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (28436.41867821729, 2153.6635795358025, (
                0.0, 0.0, 785.8413389448965, 0.0, 95.48649877780865)),
            "claims_death": (24217.154895507127, 86.7458901980885, (
                45.95168679397777, 79.25780149033658, 72.96443819405927, 68.20805588984936,
                41.82833407750874)),
            "claims_lapse": (84169.40445398272, 11033.065622465634, (
                156.51828285334597, 439.77418979760466, 197.66275536665705,
                80.68425005418268, 485.1643928324797)),
            "claims_maturity": (4151.845713202635, 4151.845713202635, (
                0.0, 0.0, 0.0, 0.0, 4151.845713202635)),
            "expenses": (7159.80974002473, 6205.0, (
                6205.0, 4.083162934582259, 2.425719655679512, 1.2771774050128315,
                0.47831036767151375)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-48134.63348093448, 93592.53003035267, (
                93592.53003035267, -523.1151542225234, -1058.8942521612923,
                -150.16948334904487, -4774.803249258103)),
        },
        "result_pols": {
            "pols_if": (153.99949605897504, 1.0, (
                1.0, 0.6870046052090497, 0.3433495539227757, 0.14837344612115183,
                0.04674634865189109)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.21904616350000064, 0.0007373640889500974, (
                0.00045907401398581626, 0.0006361905035031719, 0.0006506040753253215,
                0.0006422980231613, 0.0004179075455035234)),
            "pols_lapse": (0.7394726804946288, 0.08893057043507308, (
                0.0016813703248057914, 0.003530001564188599, 0.0017625050965176857,
                0.0007597831903279014, 0.004847285101018411)),
            "pols_lapse_term": (0.1760338523097303, 0.0845591980066141, (
                0.0, 0.0, 0.0, 0.0, 0.004609017333929906)),
            "pols_maturity": (0.041481156005369155, 0.041481156005369155, (
                0.0, 0.0, 0.0, 0.0, 0.041481156005369155)),
            "pols_if_aft_decr": (153.04097721498042, 0.9978595556612084, (
                0.9978595556612084, 0.682838413141358, 0.3409364447509327,
                0.14697136490766263, 0.041481156005369155)),
        },
    },
    4: {"rows": 180, "months": (0, 44, 89, 134, 179),
        "result_cf": {
            "pols_if": (88.52180552444085, 1.0, (
                1.0, 0.7778860869633653, 0.4540635577165104, 0.19551131979898922,
                0.0854721477145279)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (18270.617855184508, 2082.2658121434565, (
                0.0, 0.0, 0.0, 0.0, 274.970176428075)),
            "claims_death": (32564.491928183033, 242.54470082167066, (
                168.54304606305985, 213.0785631135617, 213.24249292254146,
                151.54512598349433, 96.44873982978548)),
            "claims_lapse": (87122.52477017257, 8805.461013763977, (
                156.62387886033696, 148.94218164817207, 315.44282011310077,
                147.833273029251, 1399.6276810457418)),
            "claims_maturity": (11977.462224100145, 11977.462224100145, (
                0.0, 0.0, 0.0, 0.0, 11977.462224100145)),
            "expenses": (6695.1617380765065, 6205.0, (
                6205.0, 4.188491171843912, 2.6986944115875997, 1.2826389707868509,
                0.603849535715153)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-56630.258515716785, 93469.8330750766, (
                93469.8330750766, -366.2092359335777, -531.3840074472298,
                -300.6610379835322, -13749.112670939463)),
        },
        "result_pols": {
            "pols_if": (88.52180552444085, 1.0, (
                1.0, 0.7778860869633653, 0.4540635577165104, 0.19551131979898922,
                0.0854721477145279)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2518768589180861, 0.0019286613167259056, (
                0.0016806145280660045, 0.0017817235925633472, 0.0015731859342666482,
                0.0010253582899168, 0.0006118423047449076)),
            "pols_lapse": (0.6721416600887808, 0.06798802415398164, (
                0.0016793155195271618, 0.0013055181749928827, 0.002327163788352415,
                0.0010002437956505832, 0.008878824416649734)),
            "pols_lapse_term": (0.41994136458718206, 0.06464608028925516, (
                0.0, 0.0, 0.0, 0.0, 0.008442386777014806)),
            "pols_maturity": (0.07598148099313325, 0.07598148099313325, (
                0.0, 0.0, 0.0, 0.0, 0.07598148099313325)),
            "pols_if_aft_decr": (87.59778700543397, 0.9966400699524068, (
                0.9966400699524068, 0.774798845195809, 0.45016320799389137,
                0.19348571771342185, 0.07598148099313325)),
        },
    },
    5: {"rows": 180, "months": (0, 44, 89, 134, 179),
        "result_cf": {
            "pols_if": (85.44428485562543, 1.0, (
                1.0, 0.761393406066542, 0.43039288559082806, 0.17676036010227528,
                0.07206288594805314)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (14951.563702783842, 2034.273459439965, (
                0.0, 0.0, 0.0, 0.0, 180.39483794304564)),
            "claims_death": (32731.77378562303, 243.11144284096676, (
                210.7703009160549, 222.1986214917825, 205.44924309804, 135.47668133377078,
                79.02285290507884)),
            "claims_lapse": (68419.68281467576, 6933.199828622298, (
                156.65765794234312, 124.2173046464759, 243.02874326655188,
                105.65580141755188, 916.5814344539721)),
            "claims_maturity": (7843.742771850186, 7843.742771850186, (
                0.0, 0.0, 0.0, 0.0, 7843.742771850186)),
            "expenses": (6676.492745176723, 6205.0, (
                6205.0, 4.0996871046493855, 2.5580094579098502, 1.1596245505917127,
                0.5091148565420867)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-30623.255820109523, 93427.5720411416, (
                93427.5720411416, -350.51561324290776, -451.0359958225017,
                -242.29210730191437, -9020.251012008825)),
        },
        "result_pols": {
            "pols_if": (85.44428485562543, 1.0, (
                1.0, 0.761393406066542, 0.43039288559082806, 0.17676036010227528,
                0.07206288594805314)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2994212884149476, 0.0023356071312192164, (
                0.002100343875829913, 0.0021792706212071726, 0.0018631399810715027,
                0.0011580280736573612, 0.0006442347831852089)),
            "pols_lapse": (0.6366325018721066, 0.06533429967837208, (
                0.0016786094749306544, 0.0012771064038739842, 0.0022039339804888008,
                0.0009031250469212155, 0.007472441451921956)),
            "pols_lapse_term": (0.39722779989275747, 0.0621227993489637, (
                0.0, 0.0, 0.0, 0.0, 0.0071051344125495535)),
            "pols_maturity": (0.06394620971294598, 0.06394620971294598, (
                0.0, 0.0, 0.0, 0.0, 0.06394620971294598)),
            "pols_if_aft_decr": (84.50823106533836, 0.9962210466492394, (
                0.9962210466492394, 0.7579370290414609, 0.42632581162926775,
                0.1746992069816967, 0.06394620971294598)),
        },
    },
    6: {"rows": 180, "months": (0, 44, 89, 134, 179),
        "result_cf": {
            "pols_if": (88.52180552444085, 1.0, (
                1.0, 0.7778860869633653, 0.4540635577165104, 0.19551131979898922,
                0.0854721477145279)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (13052.714637991778, 1928.0239001328302, (
                0.0, 0.0, 0.0, 0.0, 154.20842073165875)),
            "claims_death": (22976.193739703063, 174.33570741722176, (
                168.09428166307887, 167.6943991531882, 136.57228780814734,
                88.92154321580884, 54.09025823787947)),
            "claims_lapse": (58312.62391648631, 5784.607215524535, (
                156.2068505541489, 111.55301667179724, 200.19729981771894,
                86.74355371770102, 784.9373961573402)),
            "claims_maturity": (6717.184961456057, 6717.184961456057, (
                0.0, 0.0, 0.0, 0.0, 6717.184961456057)),
            "expenses": (6695.1617380765065, 6205.0, (
                6205.0, 4.188491171843912, 2.6986944115875997, 1.2826389707868509,
                0.603849535715153)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-7753.878993713712, 93470.69886778278, (
                93470.69886778278, -283.4359069968293, -339.4682820374539,
                -176.9477359042967, -7711.02488611865)),
        },
        "result_pols": {
            "pols_if": (88.52180552444085, 1.0, (
                1.0, 0.7778860869633653, 0.4540635577165104, 0.19551131979898922,
                0.0854721477145279)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2518768589180861, 0.0019286613167259056, (
                0.0016806145280660045, 0.0017817235925633472, 0.0015731859342666482,
                0.0010253582899168, 0.0006118423047449076)),
            "pols_lapse": (0.6721416600887808, 0.06798802415398164, (
                0.0016793155195271618, 0.0013055181749928827, 0.002327163788352415,
                0.0010002437956505832, 0.008878824416649734)),
            "pols_lapse_term": (0.41994136458718206, 0.06464608028925516, (
                0.0, 0.0, 0.0, 0.0, 0.008442386777014806)),
            "pols_maturity": (0.07598148099313325, 0.07598148099313325, (
                0.0, 0.0, 0.0, 0.0, 0.07598148099313325)),
            "pols_if_aft_decr": (87.59778700543397, 0.9966400699524068, (
                0.9966400699524068, 0.774798845195809, 0.45016320799389137,
                0.19348571771342185, 0.07598148099313325)),
        },
    },
    7: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (81.5954795968861, 1.0, (
                1.0, 0.8609763466120489, 0.7171499398614984, 0.48839192950980853,
                0.3328075696113262)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (10243.202459596807, 1675.3503955122148, (
                0.0, 0.0, 1127.7793932260668, 0.0, 473.71660169993703)),
            "claims_death": (39873.01478381778, 380.38239140379665, (
                351.9588238610094, 357.95115935324276, 345.2065575002947,
                308.09628977153534, 243.1008465962741)),
            "claims_lapse": (17402.0592138088, 5156.186608298546, (
                95.7488919668135, 106.7118771630784, 65.17591179049806, 136.86546221479614,
                114.06069449959467)),
            "claims_maturity": (22890.538883401383, 22890.538883401383, (
                0.0, 0.0, 0.0, 0.0, 22890.538883401383)),
            "expenses": (6647.378713142903, 6205.0, (
                6205.0, 4.522816370796419, 3.9579967406503256, 2.9027226440741956,
                2.078155249029326)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (2943.8059462323145, 93347.29228417217, (
                93347.29228417217, -469.18585288711756, -1542.1198592575097,
                -447.86447463040565, -23723.49518144622)),
        },
        "result_pols": {
            "pols_if": (81.5954795968861, 1.0, (
                1.0, 0.8609763466120489, 0.7171499398614984, 0.48839192950980853,
                0.3328075696113262)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.4361037663413196, 0.004208138508931324, (
                0.003519588238610094, 0.003727104949533973, 0.003818991207220499,
                0.0035489831593741965, 0.002975265417561888)),
            "pols_lapse": (0.23569929379965954, 0.06845302004535933, (
                0.0012101502386782194, 0.0012582414863894086, 0.0008697812113520503,
                0.0020105560124885334, 0.0016353643347429652)),
            "pols_lapse_term": (0.06508821935863147, 0.06508821935863147, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3281969398590213, 0.3281969398590213, (
                0.0, 0.0, 0.0, 0.0, 0.3281969398590213)),
            "pols_if_aft_decr": (80.9236765367451, 0.9952702615227117, (
                0.9952702615227117, 0.8559910001761255, 0.7124611674429259,
                0.48283239033794584, 0.3281969398590213)),
        },
    },
    8: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (83.97521125057204, 1.0, (
                1.0, 0.8714749528052383, 0.7436054345581786, 0.5148887365455679,
                0.3620219066720862)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (11501.00387138365, 1931.3279407941986, (
                0.0, 0.0, 1211.4689238803696, 0.0, 541.0737336140272)),
            "claims_death": (33222.79990053454, 316.0306231228264, (
                282.02850278086106, 299.36347135674566, 286.5041050252646,
                260.0389000672544, 211.7436980196166)),
            "claims_lapse": (22251.491855030734, 5425.4952312270525, (
                156.2002955566535, 136.8562388229764, 75.26009113104475, 199.17910265860604,
                135.37862946685337)),
            "claims_maturity": (26187.446899799477, 26187.446899799477, (
                0.0, 0.0, 0.0, 0.0, 26187.446899799477)),
            "expenses": (6661.127945196922, 6205.0, (
                6205.0, 4.5779668614550175, 4.10400632102061, 3.0602045292797095,
                2.26057876776309)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (176.12952805467648, 93356.77120166249, (
                93356.77120166249, -440.79767704117705, -1577.3371263576994,
                -462.27820725514016, -27077.90353966774)),
        },
        "result_pols": {
            "pols_if": (83.97521125057204, 1.0, (
                1.0, 0.8714749528052383, 0.7436054345581786, 0.5148887365455679,
                0.3620219066720862)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.36163140718722797, 0.0034962202909991327, (
                0.0028166437288553725, 0.003019383772425216, 0.0031695708964715416,
                0.002995406656163306, 0.002591491189459677)),
            "pols_lapse": (0.2807867325691197, 0.07202833451013127, (
                0.0016774045564673591, 0.0014608660678337557, 0.0009694649488724414,
                0.0026326739641457843, 0.0018485552389746014)),
            "pols_lapse_term": (0.06848778963332443, 0.06848778963332443, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.35758186024365196, 0.35758186024365196, (
                0.0, 0.0, 0.0, 0.0, 0.35758186024365196)),
            "pols_if_aft_decr": (83.33279311081569, 0.9955059517146773, (
                0.9955059517146773, 0.8669947029649794, 0.7394663987128347,
                0.5092606559252588, 0.35758186024365196)),
        },
    },
    9: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (70.71395306668421, 1.0, (
                1.0, 0.8019788807606142, 0.6194312098563673, 0.358825693795146,
                0.19450955951547688)),
            "premiums": (50000.0, 50000.0, (
                50000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (20789.86824637878, 202.1496098544208, (
                175.9794119305047, 192.7397521490736, 188.94994177932205,
                156.53329160469127, 110.47291082906088)),
            "claims_lapse": (26404.09454406632, 3326.1859808758, (
                77.9443278171808, 70.54223758025137, 1086.2361344580067, 109.98196349716015,
                1281.3688110910828)),
            "claims_maturity": (10965.44941045788, 10965.44941045788, (
                0.0, 0.0, 0.0, 0.0, 10965.44941045788)),
            "expenses": (3584.3547351296406, 3205.0, (
                3205.0, 4.212895307995601, 3.4186807714744876, 2.1326549513220114,
                1.214578930898553)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-11743.766936032625, 46541.07626025232, (
                46541.07626025232, -267.4948850373206, -1278.6047570088033,
                -268.64791005317346, -12358.505711308922)),
        },
        "result_pols": {
            "pols_if": (70.71395306668421, 1.0, (
                1.0, 0.8019788807606142, 0.6194312098563673, 0.358825693795146,
                0.19450955951547688)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.36356202281371797, 0.0035807736894013166, (
                0.003519588238610094, 0.0034717091447013402, 0.003298616108615007,
                0.0026074680343467055, 0.0017388954418538535)),
            "pols_lapse": (0.46383665931905776, 0.05707550711383071, (
                0.0016762221035952862, 0.0013432028920428488, 0.019489307980883278,
                0.001832034906016994, 0.02016934620639901)),
            "pols_lapse_term": (0.28997339296962, 0.05426996682642337, (
                0.0, 0.0, 0.01845288512681038, 0.0, 0.019177924207469336)),
            "pols_maturity": (0.17260131786722402, 0.17260131786722402, (
                0.0, 0.0, 0.0, 0.0, 0.17260131786722402)),
            "pols_if_aft_decr": (69.88655438455143, 0.9948041896577946, (
                0.9948041896577946, 0.7971639687238701, 0.596643285766869,
                0.3543861908547823, 0.17260131786722402)),
        },
    },
    10: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (83.47706637190652, 1.0, (
                1.0, 0.8714997449638501, 0.7367352239935335, 0.5080057311614559,
                0.3572089340220911)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (14876.014241115, 1902.778133972592, (
                0.0, 0.0, 1576.0865773175997, 0.0, 849.8240203440088)),
            "claims_death": (39440.845045339825, 400.2832035962573, (
                281.66437288553726, 289.98986704690026, 329.1804736323895,
                361.6837086612248, 298.0848938019335)),
            "claims_lapse": (32720.59823126225, 8816.16423932339, (
                155.8441663511855, 132.47743311260794, 125.7913168263738,
                317.70175711123346, 212.55222292117676)),
            "claims_maturity": (41130.73988013332, 41130.73988013332, (
                0.0, 0.0, 0.0, 0.0, 41130.73988013332)),
            "expenses": (6658.221100495481, 6205.0, (
                6205.0, 4.578097097763225, 4.066089186107794, 3.019295877067132,
                2.230525051173341)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-34826.41849834584, 93357.49146076328, (
                93357.49146076328, -427.0453972572715, -2035.1244569624707,
                -682.4047616495254, -42493.43154225161)),
        },
        "result_pols": {
            "pols_if": (83.47706637190652, 1.0, (
                1.0, 0.8714997449638501, 0.7367352239935335, 0.5080057311614559,
                0.3572089340220911)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.35891567159184834, 0.0034626253919444977, (
                0.0028166437288553725, 0.0030194696693763043, 0.003140287060654407,
                0.0029553642184896815, 0.002557038091490469)),
            "pols_lapse": (0.2882557524167405, 0.07106152919600867, (
                0.0016762937354768887, 0.0014601927533894631, 0.0012340112598891,
                0.0025959820214000668, 0.0018233199391900791)),
            "pols_lapse_term": (0.06756850752829817, 0.06756850752829817, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3528285759914105, 0.3528285759914105, (
                0.0, 0.0, 0.0, 0.0, 0.3528285759914105)),
            "pols_if_aft_decr": (82.82989494789793, 0.9955070625356678, (
                0.9955070625356678, 0.8670200825410843, 0.73236092567299,
                0.5024543849215661, 0.3528285759914105)),
        },
    },
    11: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (79.72171865951731, 1.0, (
                1.0, 0.8523529394841264, 0.6996907722049244, 0.4642825408052774,
                0.3107096564042318)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (14644.302938164472, 1926.6108885418935, (
                0.0, 0.0, 1562.8534016079138, 0.0, 803.9630210755503)),
            "claims_death": (48451.83717157618, 481.63872208356844, (
                352.4366236278959, 371.54320078453355, 407.80543968717325,
                435.54691990158466, 352.1799863011278)),
            "claims_lapse": (31838.947162109595, 8481.461346778218, (
                156.10028142201844, 135.82298989118556, 124.60200908744382,
                306.0199204581282, 200.79354836277417)),
            "claims_maturity": (38841.214498038054, 38841.214498038054, (
                0.0, 0.0, 0.0, 0.0, 38841.214498038054)),
            "expenses": (6636.534517020072, 6205.0, (
                6205.0, 4.477516535227552, 3.861638469055778, 2.7594302096605685,
                1.9401689214420377)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-40412.836286908365, 93286.46309495009, (
                93286.46309495009, -511.84370721094666, -2099.1224888515867,
                -744.3262705693734, -40200.091222698946)),
        },
        "result_pols": {
            "pols_if": (79.72171865951731, 1.0, (
                1.0, 0.8523529394841264, 0.6996907722049244, 0.4642825408052774,
                0.3107096564042318)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.4236513000078602, 0.004103787971412874, (
                0.003519588238610094, 0.003689774837603722, 0.003726017054871379,
                0.003373788179020884, 0.0027777123479543193)),
            "pols_lapse": (0.27000045387547217, 0.06646470898518947, (
                0.0016762221035952862, 0.001427572422194547, 0.0011707119298448826,
                0.0023704596290563453, 0.0015836979396096208)),
            "pols_lapse_term": (0.06319764351038148, 0.06319764351038148, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3063482461166679, 0.3063482461166679, (
                0.0, 0.0, 0.0, 0.0, 0.3063482461166679)),
            "pols_if_aft_decr": (79.02806690563398, 0.9948041896577946, (
                0.9948041896577946, 0.8472355922243281, 0.6947940432202081,
                0.45853829299720017, 0.3063482461166679)),
        },
    },
    12: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (78.31540826663084, 1.0, (
                1.0, 0.8420826724256353, 0.6880341989643561, 0.4490825841424635,
                0.292507739970152)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (10528.280741496, 1898.175365006509, (
                0.0, 0.0, 1101.8781586259327, 0.0, 433.65253787547545)),
            "claims_death": (38412.933126313146, 408.58054899053735, (
                390.53212136836015, 396.7757728433701, 318.9029101434405,
                272.14131342762914, 210.69849492464076)),
            "claims_lapse": (19914.536664038296, 4904.115087907947, (
                155.91284154751202, 130.7208937382351, 66.01916637369489, 172.2503598442625,
                108.20012271241843)),
            "claims_maturity": (20930.075738261232, 20930.075738261232, (
                0.0, 0.0, 0.0, 0.0, 20930.075738261232)),
            "expenses": (6628.454476485388, 6205.0, (
                6205.0, 4.423565538585915, 3.7973050900385097, 2.6690903499532626,
                1.8265104243590171)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (3585.7192534059286, 93248.55503708412, (
                93248.55503708412, -531.920232120191, -1490.5975402331064,
                -447.0607636218449, -21684.453404198124)),
        },
        "result_pols": {
            "pols_if": (78.31540826663084, 1.0, (
                1.0, 0.8420826724256353, 0.6880341989643561, 0.4490825841424635,
                0.292507739970152)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.45979101211207796, 0.004475296398118424, (
                0.003903212169360959, 0.004043000885615498, 0.004063861078232822,
                0.003619624711213784, 0.0029004195465279804)),
            "pols_lapse": (0.25209112162942565, 0.06510654363769965, (
                0.001675576793457121, 0.0014097021923813629, 0.0008651344021820353,
                0.002291021716456742, 0.001489454165128558)),
            "pols_lapse_term": (0.06190623863147136, 0.06190623863147136, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.28811786625849545, 0.28811786625849545, (
                0.0, 0.0, 0.0, 0.0, 0.28811786625849545)),
            "pols_if_aft_decr": (77.60352613288933, 0.994421211037182, (
                0.994421211037182, 0.8366299693476384, 0.6831052034839412,
                0.44317193771479296, 0.28811786625849545)),
        },
    },
    13: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (83.47334308897757, 1.0, (
                1.0, 0.8714749528052383, 0.7367107486979357, 0.5079607311068077,
                0.35715077712436777)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (15227.574053937742, 1930.7608150124447, (
                0.0, 0.0, 1630.594504633469, 0.0, 879.093822163643)),
            "claims_death": (40396.94476187981, 400.2699056712882, (
                281.9360854578509, 299.29316848632504, 340.56496582259365,
                368.15538434260964, 308.351590857022)),
            "claims_lapse": (33263.86238058309, 8815.871354961728, (
                156.14911061248506, 136.82408513133282, 130.14172755457696,
                323.5731259141702, 219.95249339194018)),
            "claims_maturity": (42547.29320176955, 42547.29320176955, (
                0.0, 0.0, 0.0, 0.0, 42547.29320176955)),
            "expenses": (6658.199544506605, 6205.0, (
                6205.0, 4.5779668614550175, 4.06595410537388, 3.019028422447759,
                2.2301619011932727)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-38093.87394267676, 93356.91480392967, (
                93356.91480392967, -440.6952204791129, -2105.367152116013,
                -694.7475386792275, -43956.92127008335)),
        },
        "result_pols": {
            "pols_if": (83.47334308897757, 1.0, (
                1.0, 0.8714749528052383, 0.7367107486979357, 0.5079607311068077,
                0.35715077712436777)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.35889574293865917, 0.0034625103590571697, (
                0.0028166437288553725, 0.003019383772425216, 0.0031401827362627288,
                0.002955102427050768, 0.002556621782186312)),
            "pols_lapse": (0.28833378401017273, 0.0710591684402364, (
                0.0016774045564673591, 0.0014608660678337557, 0.0012339702644413827,
                0.002597250428442804, 0.0018236822910142583)),
            "pols_lapse_term": (0.06756626281521676, 0.06756626281521676, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3527704730511672, 0.3527704730511672, (
                0.0, 0.0, 0.0, 0.0, 0.3527704730511672)),
            "pols_if_aft_decr": (82.82611356202875, 0.9955059517146773, (
                0.9955059517146773, 0.8669947029649794, 0.7323365956972316,
                0.5024083782513141, 0.3527704730511672)),
        },
    },
    14: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (79.72171865951731, 1.0, (
                1.0, 0.8523529394841264, 0.6996907722049244, 0.4642825408052774,
                0.3107096564042318)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (17150.98492038649, 17150.98492038649, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (43730.101469277404, 425.65809026668694, (
                352.2983472320345, 306.65963060641434, 359.9895677611764,
                389.87063829471424, 330.1582906425236)),
            "claims_lapse": (28623.698442581088, 7495.665265289734, (
                156.03903641267235, 111.52770016234658, 110.05453956751387,
                273.9272768749387, 188.23799556519012)),
            "claims_maturity": (36412.48646703915, 36412.48646703915, (
                0.0, 0.0, 0.0, 0.0, 36412.48646703915)),
            "expenses": (6636.534517020072, 6205.0, (
                6205.0, 4.477516535227552, 3.861638469055778, 2.7594302096605685,
                1.9401689214420377)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-32553.805816304222, 93286.66261635529, (
                93286.66261635529, -422.6648473039885, -473.905745797746,
                -666.5573453793135, -36932.82292216831)),
        },
        "result_pols": {
            "pols_if": (79.72171865951731, 1.0, (
                1.0, 0.8523529394841264, 0.6996907722049244, 0.4642825408052774,
                0.3107096564042318)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.4236513000078602, 0.004103787971412874, (
                0.003519588238610094, 0.003689774837603722, 0.003726017054871379,
                0.003373788179020884, 0.0027777123479543193)),
            "pols_lapse": (0.27000045387547217, 0.06646470898518947, (
                0.0016762221035952862, 0.001427572422194547, 0.0011707119298448826,
                0.0023704596290563453, 0.0015836979396096208)),
            "pols_lapse_term": (0.06319764351038148, 0.06319764351038148, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3063482461166679, 0.3063482461166679, (
                0.0, 0.0, 0.0, 0.0, 0.3063482461166679)),
            "pols_if_aft_decr": (79.02806690563398, 0.9948041896577946, (
                0.9948041896577946, 0.8472355922243281, 0.6947940432202081,
                0.45853829299720017, 0.3063482461166679)),
        },
    },
    15: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (154.65959805602722, 1.0, (
                1.0, 0.6918794753401298, 0.34578590510913887, 0.14942627935583047,
                0.04707805294768803)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (22113.318499048022, 74.25963015811323, (
                45.90740139858163, 64.07048052410194, 65.52206533655774, 64.6855662840306,
                45.04803900368476)),
            "claims_lapse": (64137.10997437521, 7316.9037177744485, (
                156.3674402069386, 292.41569267696104, 153.41981884549634, 72.3278876614748,
                522.5095613661667)),
            "claims_maturity": (4471.430951064384, 4471.430951064384, (
                0.0, 0.0, 0.0, 0.0, 4471.430951064384)),
            "expenses": (7164.335630842279, 6205.0, (
                6205.0, 4.112136377961248, 2.4429321579046595, 1.286240042929054,
                0.48170437828959084)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (2113.8049446700606, 93592.72515839447, (
                93592.72515839447, -360.5983095790242, -221.38481633995875,
                -138.29969398843446, -5039.4702558125255)),
        },
        "result_pols": {
            "pols_if": (154.65959805602722, 1.0, (
                1.0, 0.6918794753401298, 0.34578590510913887, 0.14942627935583047,
                0.04707805294768803)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.22035058191347348, 0.0007425963015811322, (
                0.00045907401398581626, 0.0006407048052410194, 0.0006552206533655774,
                0.000646855662840306, 0.00042087294776674093)),
            "pols_lapse": (0.7378739187144886, 0.0895616069350714, (
                0.0016813703248057914, 0.00355504986671445, 0.001775011538811878,
                0.0007651744851642713, 0.00488168062788477)),
            "pols_lapse_term": (0.17728295917477457, 0.0851592159767194, (
                0.0, 0.0, 0.0, 0.0, 0.004641722152448502)),
            "pols_maturity": (0.04177549937203652, 0.04177549937203652, (
                0.0, 0.0, 0.0, 0.0, 0.04177549937203652)),
            "pols_if_aft_decr": (153.70137355539924, 0.9978595556612084, (
                0.9978595556612084, 0.6876837206681744, 0.3433556729169614,
                0.14801424920782588, 0.04177549937203652)),
        },
    },
    16: {"rows": 289, "months": (0, 72, 144, 216, 288),
        "result_cf": {
            "pols_if": (88.23845972114063, 0.850606741874646, (
                0.850606741874646, 0.48836137034284416, 0.2623266736410539,
                0.1244134994943544, 0.04674634865189109)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (28363.271027826202, 114.44251406585195, (
                90.10783541383934, 98.05158188259777, 103.31573012291422, 98.87214069181795,
                76.68109346362904)),
            "claims_lapse": (93972.59372096346, 12454.885723241885, (
                12454.885723241885, 7356.901008885506, 4176.72669267576, 2144.3000511425075,
                889.4195040872157)),
            "claims_maturity": (7611.30167390163, 7611.30167390163, (
                0.0, 0.0, 0.0, 0.0, 7611.30167390163)),
            "expenses": (527.7843826050317, 4.25303370937323, (
                4.25303370937323, 2.83174733448012, 1.7640010584077952, 0.9702129954337172,
                0.422756669274552)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-130474.95080529632, 12549.246592365098, (
                -12549.246592365098, -7457.784338102584, -4281.806423857082,
                -2244.1424048297595, -8577.82502812175)),
        },
        "result_pols": {
            "pols_if": (88.23845972114063, 0.850606741874646, (
                0.850606741874646, 0.48836137034284416, 0.2623266736410539,
                0.1244134994943544, 0.04674634865189109)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.1802070099178189, 0.0007373640889500974, (
                0.0006433893800461637, 0.0006800591407829672, 0.0006771754029266629,
                0.0005973331421121465, 0.0004179075455035234)),
            "pols_lapse": (0.6289185759514571, 0.08893057043507308, (
                0.08893057043507308, 0.051025467237423315, 0.027376049878003572,
                0.012954725954327262, 0.004847285101018411)),
            "pols_lapse_term": (0.1760338523097303, 0.0845591980066141, (
                0.0845591980066141, 0.04851731599607088, 0.02603038315112485,
                0.012317937821990555, 0.004609017333929906)),
            "pols_maturity": (0.041481156005369155, 0.041481156005369155, (
                0.0, 0.0, 0.0, 0.0, 0.041481156005369155)),
            "pols_if_aft_decr": (87.42933413527136, 0.7610327820595268, (
                0.7610327820595268, 0.4366558439646379, 0.23427344836012362,
                0.110861440397915, 0.041481156005369155)),
        },
    },
    17: {"rows": 324, "months": (0, 80, 161, 242, 323),
        "result_cf": {
            "pols_if": (120.91595128813071, 0.9245529031459623, (
                0.9245529031459623, 0.5901044531258136, 0.3055797878263087,
                0.13815684305055642, 0.04745555992889431)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (18754.671764741794, 67.79355635632393, (
                51.80454236226095, 60.661681531397086, 64.43729879245205, 60.94683860530434,
                42.80412478458075)),
            "claims_lapse": (55458.50113305285, 6952.43714708118, (
                81.6460701521579, 245.60696219872898, 133.21879760414996, 64.97249322223608,
                496.4825319926699)),
            "claims_maturity": (4248.7018886513815, 4248.7018886513815, (
                0.0, 0.0, 0.0, 0.0, 4248.7018886513815)),
            "expenses": (736.2044043682454, 4.640864224917058, (
                4.622764515729811, 3.4217012517406142, 2.10622556301118, 1.1319303718063074,
                0.4508972707215773)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-79198.07919081429, 7016.126765133594, (
                -138.07337703014866, -309.6903449818667, -199.7623219596132,
                -127.05126219934672, -4788.439442699354)),
        },
        "result_pols": {
            "pols_if": (120.91595128813071, 0.9245529031459623, (
                0.9245529031459623, 0.5901044531258136, 0.3055797878263087,
                0.13815684305055642, 0.04745555992889431)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.20435456355271403, 0.0007485509932158172, (
                0.0005720063044715013, 0.0006698035093748712, 0.0007114924574499761,
                0.000663317578068997, 0.00042424782132320166)),
            "pols_lapse": (0.6780878530739338, 0.09027977877415755, (
                0.0011173794738186511, 0.0030314699664984067, 0.0015679415550980283,
                0.0007071309657975779, 0.004920825588257149)),
            "pols_lapse_term": (0.17870454631670132, 0.08584208615788388, (
                0.0, 0.0, 0.0, 0.0, 0.004678942946590441)),
            "pols_maturity": (0.04211048651931397, 0.04211048651931397, (
                0.0, 0.0, 0.0, 0.0, 0.04211048651931397)),
            "pols_if_aft_decr": (120.03350887150407, 0.9228635173676721, (
                0.9228635173676721, 0.5864031796499404, 0.30330035381376064,
                0.13678639450668983, 0.04211048651931397)),
        },
    },
    18: {"rows": 40, "months": (0, 9, 19, 29, 39),
        "result_cf": {
            "pols_if": (18.15952663116853, 0.5594850038296701, (
                0.5594850038296701, 0.5079607311068077, 0.4542177783003489,
                0.4040594973924094, 0.35715077712436777)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (4471.084032694795, 1368.088824310707, (
                0.0, 0.0, 0.0, 0.0, 879.0938221636429)),
            "claims_death": (14089.002856110455, 386.46181508922723, (
                368.6311086348681, 368.1553843426096, 362.0566166807887, 353.49379032334474,
                308.35159085702196)),
            "claims_lapse": (11488.445423261503, 359.6020853605639, (
                359.6020853605639, 323.5731259141702, 286.68326547104806,
                252.15320071508802, 219.95249339194015)),
            "claims_maturity": (42547.29320176954, 42547.29320176954, (
                0.0, 0.0, 0.0, 0.0, 42547.29320176954)),
            "expenses": (93.27079182088039, 2.797425019148351, (
                2.797425019148351, 2.5398036555340386, 2.327866113789288,
                2.1225750472395006, 1.92306161798348)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-72689.09630565718, 43956.61416980014, (
                -731.0306190145803, -694.2683139123138, -651.067748265626,
                -607.7695660856723, -43956.61416980014)),
        },
        "result_pols": {
            "pols_if": (18.15952663116853, 0.5594850038296701, (
                0.5594850038296701, 0.5079607311068077, 0.4542177783003489,
                0.4040594973924094, 0.35715077712436777)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.11390567062018958, 0.003122042931524436, (
                0.002934216736661049, 0.002955102427050768, 0.0029311914122187263,
                0.0028924123325453784, 0.002556621782186312)),
            "pols_lapse": (0.09280886015831322, 0.002862347839580506, (
                0.002862347839580506, 0.002597250428442804, 0.0023209727071952344,
                0.0020632074661678878, 0.0018236822910142583)),
            "pols_lapse_term": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3527704730511672, 0.3527704730511672, (
                0.0, 0.0, 0.0, 0.0, 0.3527704730511672)),
            "pols_if_aft_decr": (17.952812100390027, 0.5536884392534286, (
                0.5536884392534286, 0.5024083782513141, 0.44896561418093495,
                0.3991038775936961, 0.3527704730511672)),
        },
    },
    19: {"rows": 48, "months": (0, 11, 23, 35, 47),
        "result_cf": {
            "pols_if": (22.851500199536986, 0.6080963653369508, (
                0.6080963653369508, 0.5422748544431394, 0.4755438187444024,
                0.4138621788820945, 0.35715077712436777)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (4471.084032694795, 1368.088824310707, (
                0.0, 1368.088824310707, 1193.4423096457929, 1030.4590765746525,
                879.0938221636429)),
            "claims_death": (17160.68323137035, 396.1302019101928, (
                396.1302019101928, 351.57186663562914, 340.2043867577079, 325.8418628016764,
                308.35159085702196)),
            "claims_lapse": (14484.889951763502, 386.42763278642224, (
                386.42763278642224, 342.9606819252582, 299.0068909883503, 258.0077395395671,
                219.95249339194015)),
            "claims_maturity": (42547.29320176954, 42547.29320176954, (
                0.0, 0.0, 0.0, 0.0, 42547.29320176954)),
            "expenses": (118.12204880096422, 3.0404818266847538, (
                3.0404818266847538, 2.711374272215697, 2.437162071065062,
                2.1740697584400026, 1.92306161798348)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-78782.07246639916, 43956.61416980014, (
                -785.5983165232998, -2065.33274714381, -1835.0907494629162,
                -1616.482748674336, -43956.61416980014)),
        },
        "result_pols": {
            "pols_if": (22.851500199536986, 0.6080963653369508, (
                0.6080963653369508, 0.5422748544431394, 0.4755438187444024,
                0.4138621788820945, 0.35715077712436777)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.13851270615830258, 0.0031891588165205613, (
                0.0031891588165205613, 0.002843958180980852, 0.002766514430906055,
                0.0026707657043295303, 0.002556621782186312)),
            "pols_lapse": (0.11681318612748066, 0.0031110455251967453, (
                0.0031110455251967453, 0.002774300021358034, 0.0024314997426789736,
                0.002114762714308656, 0.0018236822910142583)),
            "pols_lapse_term": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3527704730511672, 0.3527704730511672, (
                0.0, 0.0, 0.0, 0.0, 0.3527704730511672)),
            "pols_if_aft_decr": (22.596174307251204, 0.6017961609952335, (
                0.6017961609952335, 0.5366565962408005, 0.47034580457081737,
                0.4090766504634563, 0.3527704730511672)),
        },
    },
    20: {"rows": 150, "months": (0, 37, 74, 111, 149),
        "result_cf": {
            "pols_if": (60.62955641461009, 0.8467119494563531, (
                0.8467119494563531, 0.663484953303173, 0.3579650837990747,
                0.1817652863148586, 0.0854721477145279)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (14152.955782029287, 1973.349698245477, (
                0.0, 0.0, 0.0, 0.0, 274.970176428075)),
            "claims_death": (27133.445885994908, 242.54470082167066, (
                198.88317814723857, 239.834531806526, 193.13040576798835,
                143.58878268522128, 96.44873982978548)),
            "claims_lapse": (76784.72949550391, 8805.461013763977, (
                152.70231993053915, 138.8863714753101, 257.47906490525315,
                140.07180750210392, 1399.6276810457418)),
            "claims_maturity": (11977.462224100145, 11977.462224100145, (
                0.0, 0.0, 0.0, 0.0, 11977.462224100145)),
            "expenses": (332.1440867096714, 4.233559747281765, (
                4.233559747281765, 3.572503630203748, 2.075648758159063, 1.13499967650281,
                0.5747526812279863)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-130380.73747433792, 13749.083574084976, (
                -355.81905782505953, -382.29340691203987, -452.68511943140055,
                -284.79558986382796, -13749.083574084976)),
        },
        "result_pols": {
            "pols_if": (60.62955641461009, 0.8467119494563531, (
                0.8467119494563531, 0.663484953303173, 0.3579650837990747,
                0.1817652863148586, 0.0854721477145279)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.201017591633118, 0.0019286613167259056, (
                0.0017490023074124502, 0.001868800732911282, 0.0013756085245806488,
                0.0009532672754378516, 0.0006118423047449076)),
            "pols_lapse": (0.5697128768301021, 0.06798802415398164, (
                0.0014213481288874725, 0.0011129326838182755, 0.0018339442470297342,
                0.0009299185340675559, 0.008878824416649734)),
            "pols_lapse_term": (0.36434576791006096, 0.06464608028925516, (
                0.0, 0.0, 0.0, 0.0, 0.008442386777014806)),
            "pols_maturity": (0.07598148099313325, 0.07598148099313325, (
                0.0, 0.0, 0.0, 0.0, 0.07598148099313325)),
            "pols_if_aft_decr": (59.85882594614688, 0.8435415990200531, (
                0.8435415990200531, 0.6605032198864434, 0.3547555310274643,
                0.17988210050535322, 0.07598148099313325)),
        },
    },
    21: {"rows": 301, "months": (0, 75, 150, 225, 300),
        "result_cf": {
            "pols_if": (99.26934086140733, 0.8758196359245679, (
                0.8758196359245679, 0.5216905008492948, 0.2767480702687198,
                0.12910016601406785, 0.04707805294768803)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (19007.488506138146, 74.25963015811323, (
                59.89729904689142, 72.64710423618087, 71.44030890653116, 61.98347295574805,
                45.04803900368476)),
            "claims_lapse": (55325.66358355493, 7316.9037177744485, (
                73.09883216096841, 224.41591764802027, 125.69083901954274,
                63.563221432552446, 522.5095613661667)),
            "claims_maturity": (4471.430951064384, 4471.430951064384, (
                0.0, 0.0, 0.0, 0.0, 4471.430951064384)),
            "expenses": (596.8414676111233, 4.3902928406329575, (
                4.379098179622839, 3.025005200895566, 1.8609769341806508,
                1.0067609969059885, 0.43640039211431997)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-79401.4245083686, 7386.089486996248, (
                -137.37522938748268, -300.0880270850967, -198.99212486025453,
                -126.55345538520648, -5039.4249518263505)),
        },
        "result_pols": {
            "pols_if": (99.26934086140733, 0.8758196359245679, (
                0.8758196359245679, 0.5216905008492948, 0.2767480702687198,
                0.12910016601406785, 0.04707805294768803)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.18929228198437476, 0.0007425963015811322, (
                0.0005989729904689142, 0.0007264710423618086, 0.0007144030890653115,
                0.0006198347295574805, 0.00042087294776674093)),
            "pols_lapse": (0.6447518545681556, 0.0895616069350714, (
                0.000939090855060671, 0.0026793246902152485, 0.0014196446923201076,
                0.0006607759924331, 0.00488168062788477)),
            "pols_lapse_term": (0.17728295917477457, 0.0851592159767194, (
                0.0, 0.0, 0.0, 0.0, 0.004641722152448502)),
            "pols_maturity": (0.04177549937203652, 0.04177549937203652, (
                0.0, 0.0, 0.0, 0.0, 0.04177549937203652)),
            "pols_if_aft_decr": (98.43529672485481, 0.8742815720790382, (
                0.8742815720790382, 0.5182847051167178, 0.2746140224873344,
                0.12781955529207725, 0.04177549937203652)),
        },
    },
    22: {"rows": 80, "months": (0, 19, 39, 59, 79),
        "result_cf": {
            "pols_if": (42.555386658270464, 0.7843657367800575, (
                0.7843657367800575, 0.6880341989643561, 0.5106575165933204,
                0.3923109513643728, 0.292507739970152)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (5588.754226202163, 1197.0952352290058, (
                0.0, 1101.8781586259327, 0.0, 0.0, 433.65253787547545)),
            "claims_death": (23185.98197001911, 351.99385182973054, (
                329.8931729527644, 318.9029101434405, 281.82696184272646,
                260.87960230035895, 210.69849492464076)),
            "claims_lapse": (14617.280282677293, 4904.115087907947, (
                69.4433744692041, 66.01916637369489, 198.01463517536706, 148.73911942448922,
                108.20012271241843)),
            "claims_maturity": (20930.075738261232, 20930.075738261232, (
                0.0, 0.0, 0.0, 0.0, 20930.075738261232)),
            "expenses": (225.39489136237296, 3.9218286839002876, (
                3.9218286839002876, 3.526175269692325, 2.7496114610256424,
                2.1651894262467595, 1.6960965040985638)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-64547.48710852217, 21684.322990277866, (
                -403.2583761058688, -1490.3264104127604, -482.5912084791192,
                -411.7839111510949, -21684.322990277866)),
        },
        "result_pols": {
            "pols_if": (42.555386658270464, 0.7843657367800575, (
                0.7843657367800575, 0.6880341989643561, 0.5106575165933204,
                0.3923109513643728, 0.292507739970152)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.30200794248442064, 0.004475296398118424, (
                0.004176931050969033, 0.004063861078232822, 0.003710779841134017,
                0.0035072195259512468, 0.0029004195465279804)),
            "pols_lapse": (0.19423992803714119, 0.06510654363769965, (
                0.0009216025699479979, 0.0008651344021820353, 0.0026072335721672637,
                0.00199962258190565, 0.001489454165128558)),
            "pols_lapse_term": (0.06190623863147136, 0.06190623863147136, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.28811786625849545, 0.28811786625849545, (
                0.0, 0.0, 0.0, 0.0, 0.28811786625849545)),
            "pols_if_aft_decr": (42.05913878774891, 0.7792672031591404, (
                0.7792672031591404, 0.6831052034839412, 0.5043395031800191,
                0.38680410925651587, 0.28811786625849545)),
        },
    },
    23: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.3328075696113262, 0.3328075696113262, (
                0.3328075696113262,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "withdrawals": (473.71660169993703, 473.71660169993703, (
                473.71660169993703,)),
            "claims_death": (243.1008465962741, 243.1008465962741, (
                243.1008465962741,)),
            "claims_lapse": (114.06069449959467, 114.06069449959467, (
                114.06069449959467,)),
            "claims_maturity": (22890.538883401383, 22890.538883401383, (
                22890.538883401383,)),
            "expenses": (1.664037848056631, 1.664037848056631, (
                1.664037848056631,)),
            "premium_taxes": (0.0, 0.0, (
                0.0,)),
            "net_cf": (-23723.081064045244, 23723.081064045244, (
                -23723.081064045244,)),
        },
        "result_pols": {
            "pols_if": (0.3328075696113262, 0.3328075696113262, (
                0.3328075696113262,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (0.002975265417561888, 0.002975265417561888, (
                0.002975265417561888,)),
            "pols_lapse": (0.0016353643347429652, 0.0016353643347429652, (
                0.0016353643347429652,)),
            "pols_lapse_term": (0.0, 0.0, (
                0.0,)),
            "pols_maturity": (0.3281969398590213, 0.3281969398590213, (
                0.3281969398590213,)),
            "pols_if_aft_decr": (0.3281969398590213, 0.3281969398590213, (
                0.3281969398590213,)),
        },
    },
    24: {"rows": 373, "months": (0, 93, 186, 279, 372),
        "result_cf": {
            "pols_if": (153.99949605897507, 1.0, (
                0.0, 0.7254039231496342, 0.3581911440435313, 0.1526604550457851,
                0.04674634865189109)),
            "premiums": (100000.0, 100000.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (32696.920659205938, 114.44251406585195, (
                0.0, 86.09241816219877, 102.30402926585239, 109.08384733030923,
                76.68109346362904)),
            "claims_lapse": (105570.20731548713, 12454.885723241885, (
                0.0, 528.6594593430028, 277.1445489104848, 129.0367875179501,
                889.4195040872157)),
            "claims_maturity": (7611.30167390163, 7611.30167390163, (
                0.0, 0.0, 0.0, 0.0, 7611.30167390163)),
            "expenses": (7185.79287417386, 6205.125, (
                0.0, 4.311386545515004, 2.5938378858705335, 1.346931348860476,
                0.502524830034884)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-53064.22252276858, 93592.40503035267, (
                0.0, -619.0632640507166, -382.0424160622077, -239.4675661971198,
                -8577.90479628251)),
        },
        "result_pols": {
            "pols_if": (153.99949605897507, 1.0, (
                0.0, 0.7254039231496342, 0.3581911440435313, 0.1526604550457851,
                0.04674634865189109)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2190461635000006, 0.0007373640889500974, (
                0.0, 0.0006070477018602105, 0.0006787270156540671, 0.0006608561778011703,
                0.0004179075455035234)),
            "pols_lapse": (0.7394726804946287, 0.08893057043507308, (
                0.0, 0.003727639630893079, 0.001838690948310409, 0.0007817358874099819,
                0.004847285101018411)),
            "pols_lapse_term": (0.1760338523097303, 0.0845591980066141, (
                0.0, 0.0, 0.0, 0.0, 0.004609017333929906)),
            "pols_maturity": (0.041481156005369155, 0.041481156005369155, (
                0.0, 0.0, 0.0, 0.0, 0.041481156005369155)),
            "pols_if_aft_decr": (153.04097721498042, 0.9978595556612084, (
                0.0, 0.7210692358168809, 0.3556737260795668, 0.15121786298057394,
                0.041481156005369155)),
        },
    },
}
# END generated fingerprint: RILA_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is RILA's
# own: the comparison on the splice grid, at the contract's extremes, where the caps bind
# and under the Holding Account's share and a NaN sent through a Reference, on labels that
# are not text, on keys written as floats and out of order and on keys far past every
# frame, the powers off their domain, the total's sign of zero, the refusals, the deepest
# call, a Reference set late and the runner.  Each comparison adds _rila_c4_also's calls,
# the codes and the keys no swept cell reaches.  None asks for sec_read, sec_model or
# s_model, which sweep every committed point; the grid test alone asks for spliced.


def _quiet(cell, *args):
    """``cell(*args)``, whatever it raises dropped: a key ``_rila_c4_also`` reads may be one
    the cell refuses, which the refusal test holds, and C4's ``also`` must not raise."""
    try:
        cell(*args)
    except Exception:                           # refused; the refusal test holds it
        pass


# Each timed cell and the timings it takes, as the sample calls them; the kinded and the
# bucketed cells.
TIMED = {"pols_if_at": TIMINGS,
         "inv_amt_pp_at": ("BEF_CREDIT", "BEF_ROLL", "BEF_WD", "AFT_WD"),
         "interim_value_pp_at": ("BEF_ROLL", "BEF_WD", "AFT_WD"),
         **{cell: ("BEF_ROLL", "AFT_WD") for cell in (
             "iv_notional_pp", "fixed_proxy_pp", "budget_amort_pp", "deriv_proxy_pp",
             "trading_cost_pp")},
         **{cell: ("BEF_WD", "AFT_WD") for cell in (
             "fixed_acct_pp_at", "holding_acct_pp_at", "av_pp_at", "av_at")}}
KINDED = ("pols_decr", "claim_pp", "claim_from_av_pp", "claims", "claims_from_av",
          "claims_over_av")
BUCKETED = ("roll_to_acct_pp", "wd_bucket_value_pp", "wd_alloc_pp")


def _rila_c4_also(proj):
    """What C4 compares of a ``RILA_US_SEC`` point beyond its full sweep (M25).

    ``sec_support.full_sweep`` reaches a cell of more than ``t`` only at the keys some
    swept cell asks of it, and an engine cell at none.  So, as ``sample_sec.py`` does,
    this calls, at ``t = 0 .. proj_len()``, each timed cell at every code of its family
    (:data:`TIMED`), each kinded cell at the three kinds and ``claims`` and
    ``claims_over_av`` at ``ALL``, each bucketed cell at the three buckets, every leg on
    every basis, both portfolios on every basis, each leg's amount at both timings, both
    crediting rules and the cap's solve; ``market_state`` at every name from
    ``t_entry()`` to ``proj_len() + 1``; every keyed reader at every key its cache holds,
    ``mort_rate_base_at`` at ages 0 to 121, ``surr_charge_rate_at`` at 0 to 91,
    ``lapse_rate_base_py`` at 0 to 92 and ``wd_amount_pm`` at 0 to 1,081, so that every key
    past a table's last row runs compiled; ``guar_min_rate`` at the three rate kinds,
    ``roll_share`` at the three buckets and ``opt_leg`` at each leg; and the engine cells
    at the arguments the sample passes.  A call the point refuses is dropped
    (:func:`_quiet`): the refusal test holds those, and the sweep's raises are compared.
    Passed to ``sec_support.compiled_mismatches`` as ``also``.
    """
    p, code = proj, (lambda label: _code(proj, label))
    kinds, buckets = [code(k) for k in KINDS], [code(b) for b in BUCKETS]
    bases, names = [code(b) for b in BASES], [code(n) for n in NAME_CODES]
    timed = {cell: [code(x) for x in xs] for cell, xs in TIMED.items()}
    roll, wd = code("BEF_ROLL"), code("AFT_WD")
    for t in range(p.proj_len() + 1):
        for cell, codes_ in timed.items():
            for x in codes_:
                _quiet(p.cells[cell], t, x)
        for cell in KINDED:
            for kind in kinds:
                _quiet(p.cells[cell], t, kind)
        _quiet(p.claims, t, p.ALL)
        _quiet(p.claims_over_av, t, p.ALL)
        for cell in BUCKETED:
            for bucket in buckets:
                _quiet(p.cells[cell], t, bucket)
        for basis in bases:
            _quiet(p.opt_portfolio_at, t, basis)
            _quiet(p.opt_portfolio_abs_at, t, basis)
            for leg in range(len(LEGS)):
                _quiet(p.opt_component_at, t, leg, basis)
        for leg in range(len(LEGS)):
            _quiet(p.opt_component_pp, t, leg, roll)
            _quiet(p.opt_component_pp, t, leg, wd)
        for rule in RULES:
            _quiet(p.credit_rate_by, t, code(rule))
        for cell in ("declared_cap_solved", "fixed_leg_yield", "nge_spread_implied",
                     "free_wd_base", "free_wd_allow", "credit_rate_accrued"):
            _quiet(p.cells[cell], t)
    try:
        entry = p.t_entry()
    except Exception:                           # a refused point: the sweep holds it
        entry = 0
    for t in range(entry, p.proj_len() + 2):
        for name in names:
            _quiet(p.market_state, t, name)
    for a in range(SPEC_SIZES["a"]):
        _quiet(p.mort_rate_base_at, a)
    for cy in range(SPEC_SIZES["cy"]):
        _quiet(p.surr_charge_rate_at, cy)
    for y in range(SPEC_SIZES["y"]):
        _quiet(p.lapse_rate_base_py, y)
    for m in range(SPEC_SIZES["m"]):
        _quiet(p.wd_amount_pm, m)
    for kind in ("CAP", "STEP", "EDGE"):
        _quiet(p.guar_min_rate, code(kind))
    for bucket in buckets:
        _quiet(p.roll_share, bucket)
    for i in range(MOST_LEGS):
        _quiet(p.opt_leg, i)
    _quiet(p.lapse_shock_year)
    for x in (-1.0, 0.0, 0.5):
        _quiet(p.norm_cdf, x)
    for tau in (0.0, 1.0, 6.0):
        _quiet(p.bs_call, 100.0, 100.0, tau, 0.04, 0.02, 0.2)
        _quiet(p.bs_put, 100.0, 90.0, tau, 0.04, 0.02, 0.2)
        _quiet(p.bs_binary_call, 100.0, 100.0, tau, 0.04, 0.02, 0.2)
    _quiet(p.bs_d2, 100.0, 100.0, 1.0, 0.04, 0.02, 0.2)
    for leg in range(len(LEGS)):
        for mkt in MARKETS:
            _quiet(p.opt_component, entry, leg, 100.0, 1.0, code(mkt))
    _quiet(p.opt_portfolio, entry, 100.0, 1.0, code("CURRENT"))
    _quiet(p.opt_portfolio_abs, entry, 100.0, 1.0, code("CURRENT"))
    _quiet(p.credit_rate_at, entry, 1.0)
    _quiet(p.credit_rate_at, entry, 0.5)
    _quiet(p.opt_budget_at_cap, entry, 0.5)


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _copied(folder, file):
    """An edit that replaces ``file`` with the copy in ``folder``, as written there."""
    return lambda _: pd.read_csv(pathlib.Path(folder) / file)


def _mismatch_text(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# How many rows C4 compares at once (compiled_mismatches sweeps every row of its case in
# one modelx read, _rila_c4_also's calls with it, and keeps every value of every row, in
# the parent and in the child, until it compares them).  A RILA row holds the nine timings
# of a dozen cells and seven legs on three bases a month: modelx holds about 48 MB a swept
# point on average and 97 MB on a 360-month one, so ten rows hold about a gigabyte
# (USLIB-SEC-PLAN.md §7.2, *For M16 and later*, item 7; measured at M25).  The contract's
# extremes, 1,080 to 1,200 months each, go four at a time.
C4_CHUNK = 10


def _chunked_mismatches(build, dest, table, *, edits=None, refs=None, also=_rila_c4_also,
                        chunk=C4_CHUNK):
    """``compiled_mismatches`` on ``table``, ``chunk`` rows at a time.

    Each chunk is a case of its own under ``dest`` (``sec_support.compiled_case``), on the
    same ``edits``, compared under the same ``refs`` with the same ``also`` and removed once
    compared, so that a run holds one chunk's sweep at a time.  A point's projection reads
    its own row alone, so a chunk projects each of its rows as the whole table does.
    Returns every chunk's lines, each prefixed with its chunk's first ``point_id``.
    """
    chunks = [table.iloc[i:i + chunk] for i in range(0, len(table), chunk)]
    assert sum(len(c) for c in chunks) == len(table)
    found = []
    for i, rows in enumerate(chunks):
        where = pathlib.Path(dest) / f"chunk{i}"
        folder = compiled_case(build, where, model_points=rows, edits=edits)
        found += [f"from point_id {rows.index[0]}: {line}"
                  for line in compiled_mismatches(build, folder, refs=refs, also=also)]
        shutil.rmtree(where)
    return found


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's rows, S's points and variants restated in force at T2's months
    and issued later, every crediting method, interim-value family and amortization rule,
    the crash, edge and dip paths with their negative interim values, the Step at
    ``R = 0`` and the Edge at ``R = -b`` exactly at a term end, the floors that bind and
    the Holding Account fed, under :data:`SPLICED_REFS`, on the splice's stepped scenarios,
    re-based to each row's month, and its programmes.  The grid is the one this run's
    ``spliced`` selects, the core by default and the full grid under ``USLIB_SEC_FULL=1``,
    and the test carries no ``sec_full`` mark, since a skipped compile test fails the
    cython job.  The grid's SEC table goes beside the build :data:`C4_CHUNK` rows at a
    time; modelx sweeps every row fully, with :func:`_rila_c4_also`'s calls, and the
    compiled model must agree at every argument modelx caches, identically on x86-64 and
    to 1e-12 relative elsewhere, with every raise and every ``Data`` array
    (``sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    here = spliced[1].Data.input_dir()
    table = pd.read_csv(here / TABLE, index_col="point_id")
    assert len(table) == len(spliced[1].Data.model_point_table()) > C4_CHUNK
    edits = {file: _copied(here, file) for file in (*SPLICED_EDITS, SCENARIOS)
             if file != "market_scenario.csv"}
    found = _chunked_mismatches(build, tmp_path / "grid", table, edits=edits,
                                refs=SPLICED_REFS)
    assert not found, _mismatch_text(found)


def _scenario_from_120(table):
    """The companion with ``up-F120``, S's ``up`` path moved 120 months on, the shipped
    horizon, so that its first level is in the issue month of a point issued then."""
    up = table[table["scenario_id"] == "up"]
    return pd.concat([table, up.assign(scenario_id="up-F120",
                                       month_end=up["month_end"] + 120)],
                     ignore_index=True)


def _far_programme(table):
    """The shipped programmes and ``far``, withdrawing at policy month ends 12, 540 and
    1,080, the last a contract issued at 0 reaches, each its own amount."""
    rows = pd.DataFrame([("far", 12, 1100.0), ("far", 540, 1600.0), ("far", 1080, 1900.0)],
                        columns=["wd_schedule_id", "month_end", "wd_amount"])
    return pd.concat([table, rows.assign(provenance="test copy")], ignore_index=True)


EXTREME_EDITS = {"mort_table.csv": _extended_mortality, SCENARIOS: _scenario_from_120,
                 "withdrawal_table.csv": _far_programme}

# The frames of the contract's extremes, in _contract_extremes' order.
EXTREME_FRAMES = [1080, 1200, 120, 240, 1, 180, 180, 180, 180, 120, 120]


def _contract_extremes():
    """The table for the contract's longest frames, its oldest issue age and the bounds of
    its tables, made from the committed points.

    Issued at 0, ``issue_age_min``, cover runs 1,080 months: the anchor issued now,
    withdrawing on ``far``'s programme to policy month end 1,080; and issued 120 months
    on, the shipped ``future_horizon_mth``, a frame of 1,200 months, the longest the
    contract allows, which reads every cache as far as ``spec_sec.py`` sizes it, ``t`` to
    1,200 in C4's sweep of the month after it and ``market_state`` to 1,201, the
    complete years to 90, the contract year to 91 and the attained age to 119, on
    ``up-F120``, a scenario that sets its first level in the point's issue month.  Then at
    111, ``issue_age_max``, the oldest, whose cover reaches age 120, the table's last,
    issued now and 120 months on.  The notional family in its last covered month, a frame
    of one month.  The Floor option on its one-year terms, renewing every year, under
    each interim-value family; the uncapped option and updated-expiry amortization.  The
    shipped mortality starts at 40, so the copy extends it below
    (:func:`_extended_mortality`), each age with a rate of its own.
    """
    committed = _committed()

    def row(kind, s_point, month, **columns):
        return committed.loc[[_label(committed, kind, s_point, month)]].assign(**columns)

    rows = pd.concat([
        row("twin", 1, 0, age_at_entry=0, wd_schedule_id="far"),
        row("twin", 1, 0, age_at_entry=0, duration_mth=-120, scenario_id="up-F120",
            wd_schedule_id="far"),
        row("twin", 1, 0, age_at_entry=111),
        row("twin", 1, 0, age_at_entry=111, duration_mth=-120, scenario_id="up-F120"),
        row("derived", 7, 119),
        *[row("twin", 6, 0, iv_family=family)
          for family in ("portfolio", "notional", "delta", "legacy")],
        row("twin", 12, 0), row("twin", 10, 0)])
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The points of :func:`_contract_extremes`, the longest frames the contract allows, its
    youngest and oldest issue ages and the bounds of its tables, read every cache as far
    as ``spec_sec.py`` sizes it: ``t`` to 1,200 and ``market_state`` to 1,201, the
    complete years to 90, the contract year to 91, the policy month end to 1,080 and the
    attained age to 120, and every keyed reader at every key its cache holds
    (:func:`_rila_c4_also`).  Frames are asserted first, in modelx.  modelx then sweeps
    each point fully, and the compiled model must agree everywhere, every raise included.
    A cache one too small for the contract raises ``IndexError`` compiled where modelx
    reads on, and fails here, though the spec check passes it, which holds the caches to
    the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    table = _contract_extremes()
    folder = compiled_case(build, tmp_path / "frames", model_points=table,
                           edits=EXTREME_EDITS)
    model = _read(folder, "extremes_frames")
    try:
        points = [projection(model, key) for key in point_keys(model)]
        assert [p.proj_len() for p in points] == EXTREME_FRAMES
        assert points[1].t_entry() == 120 and points[1].age(1199) == 89
        assert points[3].age(239) == 120
    finally:
        model.close()
    found = _chunked_mismatches(build, tmp_path / "extremes", table, edits=EXTREME_EDITS,
                                chunk=4)
    assert not found, _mismatch_text(found)


# The References each C4 case of the next test runs under, as (case, References): the
# mortality's cap, which binds at A/E 10 (test_a_capped_annual_mortality_is_the_float_1
# _in_both_models); the Holding Account fed, which spreads a withdrawal over three buckets
# (HOLDING_ON); the surrender rate's cap at certainty; and a NaN through each Reference a
# cap, a floor, a min or a max reads (the critique of M25's design, minor 12), which a
# compiled two-operand min or max must answer as Python's does, its operands taken in S's
# order.
REFERENCE_CASES = [
    ("mortality capped", {"mort_ae_factor": CAPPED_AE}),
    ("Holding Account fed", HOLDING_ON),
    ("surrender rate at certainty", {"lapse_rate_max": 1.0, "lapse_shock_mult": 100.0}),
    *[(f"{ref} NaN", {ref: NAN}) for ref in (
        "mort_ae_factor", "trading_cost_rate", "iv_credit_spread", "lapse_rate_max",
        "iv_moneyness_floor", "declared_acct_rate", "guar_min_acct_rate")],
]

# The twins those cases run on: the anchor, the behavioural rule, the Floor option, the
# notional family, the uncapped option and nge_reset, between them every cap, floor, min
# and max the References reach.
REFERENCE_TWINS = (1, 3, 6, 7, 12, 13)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_under_moved_references(
        sec_build, tmp_path):
    """C4 where a cap binds, a fourth bucket share is fed, and a NaN goes through a
    Reference: compiled, the same numbers, the same NaNs and the same verdicts.

    Each case of :data:`REFERENCE_CASES`, set before the model computes anything, on the
    twins of :data:`REFERENCE_TWINS`: first, in modelx, each case does what it is there
    for, the mortality's rate the float 1.0 on the anchor from month 348, a withdrawal on
    the behavioural rule spread over three buckets and the surrender rate 1.0 in the
    shock year, while each NaN carries on, or is lost where S's ``min`` or ``max`` with
    its bound first loses it; then modelx sweeps every twin fully, with
    :func:`_rila_c4_also`'s calls, and the compiled model must agree everywhere, a NaN
    where modelx has one and each check ``False`` where modelx's is.
    """
    build = sec_build(SEC)
    table = _committed().loc[list(REFERENCE_TWINS)]
    folder = compiled_case(build, tmp_path / "refs", model_points=table)
    found = []
    for case, refs in REFERENCE_CASES:
        model = _read(folder, "moved", refs)
        try:
            anchor, rule = _point(model, 1), _point(model, 3)
            if case == "mortality capped":
                assert anchor.mort_rate(348) == 1.0 > anchor.mort_rate(347), case
            elif case == "Holding Account fed":
                assert any(rule.wd_alloc_pp(t, _code(rule, "HOLDING")) > 0.0
                           and rule.wd_alloc_pp(t, _code(rule, "OPTION")) > 0.0
                           for t in range(rule.proj_len())), case
            elif case == "surrender rate at certainty":
                assert anchor.lapse_rate(71) == 1.0, case
        finally:
            model.close()
        found += [f"{case}: {line}" for line in compiled_mismatches(
            build, folder, refs=refs, also=_rila_c4_also)]
    assert not found, _mismatch_text(found)


# The labels Data accepts that are not text: the four a projection does not join on,
# blank, read by pandas as NaN; and the two it joins on, scenario_id and wd_schedule_id,
# as numbers, which pandas reads as ints, on tables keyed by numbers.
NUMBERED_FILES = {"scenario_id": SCENARIOS, "wd_schedule_id": "withdrawal_table.csv"}


def _numbering(column):
    """Each value of ``column``'s table, numbered from 1 in sorted order."""
    keys = pd.read_csv(model_path(SEC).parent / NUMBERED_FILES[column])[column]
    return {key: number for number, key in enumerate(sorted(set(keys)), start=1)}


def _numbered(column):
    """An edit of a table keyed by ``column`` that keys it by :func:`_numbering`'s ints."""
    numbers = _numbering(column)
    return lambda table: table.assign(**{column: table[column].map(numbers)})


def _labels_not_text():
    """The labels ``Data`` accepts that are not text, as (case, the table, the edits).

    ``blank``: the anchor's twin with a blank ``policy_id``, which no cell reads, so that
    it projects; and the uncapped option in force 40 months, whose month 0 prices its
    option and amortizes its budget, three times, with a blank ``crediting_type``,
    ``iv_family`` and ``amort_rule``, each of which its decodes answer False to and the
    projection refuses, as S's does.
    ``numeric``: the committed table with its scenario and programme keys numbers, on
    tables keyed by the same numbers (:func:`_numbering`).
    """
    committed = _committed()
    mid = committed.loc[[_label(committed, "derived", 12, 40)]]
    blank = pd.concat([committed.loc[[1]].assign(policy_id=None),
                       *(mid.assign(**{column: None})
                         for column in ("crediting_type", "iv_family", "amort_rule"))])
    blank.index = pd.Index(range(1, len(blank) + 1), name="point_id")
    numeric = committed.assign(**{column: committed[column].map(_numbering(column))
                                  for column in NUMBERED_FILES})
    return [("blank", blank, None),
            ("numeric", numeric,
             {file: _numbered(column) for column, file in NUMBERED_FILES.items()})]


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a blank label where no cell reads it, keys that are numbers on tables
    keyed by numbers, since ``RILA_US_S`` projects such a point, and a blank decoded
    label, which the point's projection refuses where it asks for it.  modelx returns each
    label as pandas reads it, NaN or an int, and an accessor typed ``str`` would raise
    ``TypeError`` compiled; the sample types the six as Python objects on a blank copy
    (sample_sec.py).  So on each case of :func:`_labels_not_text`, after checking that the
    file reads as the case says, modelx sweeps every point fully, every code with it
    (:func:`_rila_c4_also`), and the compiled model must agree everywhere, the label
    accessors and every raise included.
    """
    build = sec_build(SEC)
    found = []
    for case, rows, edits in _labels_not_text():
        folder = compiled_case(build, tmp_path / case, model_points=rows, edits=edits)
        model = _read(folder, f"labels_{case}")
        try:
            points = [projection(model, key) for key in point_keys(model)]
            if case == "blank":
                assert math.isnan(points[0].policy_id())
                assert len(points[0].result_cf()) == 360
                for p, (column, message) in zip(points[1:], (
                        ("crediting_type", "invalid crediting_type"),
                        ("iv_family", "invalid iv_family"),
                        ("amort_rule", "invalid amort_rule"))):
                    assert math.isnan(p.cells[column]()), column
                    _refused(p.result_cf, message)
            else:
                for column in NUMBERED_FILES:
                    got = [p.cells[column]() for p in points]
                    assert all(isinstance(v, (int, np.integer)) for v in got), got
                assert all(np.isfinite(p.result_cf().to_numpy()).all() for p in points)
        finally:
            model.close()
        found += [f"{case}: {line}" for line in _chunked_mismatches(
            build, tmp_path / f"{case}_c4", rows, edits=edits)]
    assert not found, _mismatch_text(found)


def _float_keys_apart(*columns):
    """An edit that writes a table in reverse key order with ``columns`` as floats."""
    def edit(table):
        table = table.iloc[::-1].reset_index(drop=True)
        return table.assign(**{c: table[c].astype(float) for c in columns})
    return edit


KEYS_APART = {"mort_table.csv": _float_keys_apart("age"),
              SCENARIOS: _float_keys_apart("month_end"),
              "surr_charge_table.csv": _float_keys_apart("contract_year"),
              "guar_min_rate_table.csv": _float_keys_apart("term_years"),
              "lapse_table.csv": _float_keys_apart("contract_year"),
              "withdrawal_table.csv": _float_keys_apart("month_end")}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                        tmp_path):
    """C4 on tables written out of key order, with keys as floats.

    ``Data`` numbers each table's keys by their sorted order and reads each row's value
    at its key, by value; :func:`test_an_assumption_tables_keys_written_as_floats_are_read
    _by_value` holds the model to the committed one on floats.  This holds the compiled
    ``Data``, and every projection on it, to modelx, on :data:`KEYS_APART`'s copy, every
    input table in reverse order with its keys as floats, ``1.0``, and the model point
    table's whole numbers as floats: modelx sweeps every committed point fully, and every
    ``Data`` array and every cell compiled must agree.
    """
    build = sec_build(SEC)
    table = _committed()
    table = table.assign(**{c: table[c].astype(float)
                            for c in ("duration_mth", "age_at_entry", "term_years")})
    found = _chunked_mismatches(build, tmp_path / "keys", table, edits=KEYS_APART)
    assert not found, _mismatch_text(found)


def _far_rows(row):
    """An edit that appends ``row``, a dict of a table's columns, beside its rows."""
    return lambda table: pd.concat([table, pd.DataFrame([row])], ignore_index=True)


# Keys far past every frame, in each table keyed by a month, a year or a term without a
# check of its last key: a level of the anchor's scenario at 1e20 and at 2**60, a
# withdrawal of the worked example's programme at 1e20, a lapse year at 1e20 and a floors
# term at 2**60, each held nowhere, never cast (the Data docstring).
FAR_KEYS = {
    SCENARIOS: _both(*(_far_rows({"scenario_id": "up", "month_end": far,
                                  "index_level": 9999.0, "mvr": 0.09, "risk_free": 0.09,
                                  "div_yield": 0.09, "impl_vol": 0.9,
                                  "provenance": "test copy"}) for far in (1e20, 2 ** 60))),
    "withdrawal_table.csv": _far_rows({"wd_schedule_id": "worked", "month_end": 1e20,
                                       "wd_amount": 777.0, "provenance": "test copy"}),
    "lapse_table.csv": _far_rows({"contract_year": 1e20, "lapse_rate_base": 0.9,
                                  "provenance": "test copy"}),
    "guar_min_rate_table.csv": _far_rows({"term_years": 2 ** 60, "guar_min_cap": 0.5,
                                          "guar_min_step": 0.5, "guar_min_edge": 0.5,
                                          "provenance": "test copy"})}


@pytest.mark.cython
def test_the_compiled_model_holds_a_far_key_as_modelx_does(sec_build, tmp_path):
    """C4 with a scenario level, a withdrawal, a lapse year and a floors term far past
    every frame (:data:`FAR_KEYS`).

    ``Data`` holds the arrays to ``read_last_mth``, and drops a key past it before it is
    cast, whatever its size, and the lapse table's rows are compared by value, so the
    model projects as though the rows were not there, as ``RILA_US_S``, whose readers never
    reach them, does: in modelx, every committed point's ``result_cf`` is the committed
    model's, bit for bit; and compiled, every committed point, swept fully, and every
    ``Data`` array, as in modelx.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "far", edits=FAR_KEYS)
    model = _read(folder, "far")
    base = _read(model_path(SEC), "far_base")
    try:
        for key in point_keys(model):
            assert frame_mismatches(projection(base, key).result_cf(),
                                    projection(model, key).result_cf(), rtol=0,
                                    atol=0) == [], key
    finally:
        base.close()
        model.close()
    found = _chunked_mismatches(build, tmp_path / "far_c4", _committed(), edits=FAR_KEYS)
    assert not found, _mismatch_text(found)


@pytest.mark.cython
def test_the_compiled_model_takes_a_power_as_modelx_does(sec_build, tmp_path):
    """Compiled, every power of :data:`POWERS` gives modelx's float or modelx's raise.

    C's ``pow`` raises nowhere, so the guards before each power are what make the
    compiled model refuse where modelx does, and only there
    (:func:`test_a_power_off_its_domain_is_refused_beside_s` holds modelx beside S).  On
    each case's copy, under its References, the case's calls on the S point's twin,
    compiled, must be modelx's: a float bit for bit, a frame column by column, and a raise
    with the same type and message, ``math``'s ``OverflowError`` among them.  A guard
    lost compiled returns ``inf`` or NaN where modelx raises, and fails.
    """
    build = sec_build(SEC)
    found = []
    for number, (case, s_point, refs, edit, files, calls, _) in enumerate(POWERS):
        dest = tmp_path / f"power{number}"
        _, sec_folder = _power_case(dest / "inputs", case, s_point, refs, edit, files)
        table = pd.read_csv(sec_folder.parent / TABLE, index_col="point_id")
        folder = compiled_case(build, dest / "case", model_points=table,
                               edits={file: _copied(sec_folder.parent, file)
                                      for file in (SCENARIOS, "guar_min_rate_table.csv")})
        idx = list(table.index).index(_label(table, "twin", s_point, 0))
        model = _read(folder, "power_cy", refs)
        try:
            want = [_did(lambda: model.Projection[idx].cells[cell](*args))
                    for cell, args, _ in calls]
        finally:
            model.close()
        got = run_compiled(folder.parent, build.package.name,
                           {"refs": refs, "calls": {idx: [(c, a) for c, a, _ in calls]}})
        assert got["exit"] == 0, f"{case}: the compiled run failed:\n{got['stderr']}"
        assert all(got["compiled"].values()), got["compiled"]
        for (cell, args, _), modelx_did, have in zip(calls, want, got["values"][idx]):
            status, value = have
            if modelx_did[0] == "raised":
                same = (status, value) == modelx_did
            elif isinstance(modelx_did[1], pd.DataFrame):
                same = status == "ok" and frame_mismatches(modelx_did[1], value,
                                                           rtol=0.0, atol=0.0) == []
            else:
                same = status == "ok" and _bits(value) == _bits(modelx_did[1])
            if not same:
                found.append(f"{case}: {cell}{args}: modelx {modelx_did}, compiled "
                             f"{status} {value!r:.200}")
    assert not found, "\n".join(found)


@pytest.mark.cython
def test_the_compiled_all_total_keeps_s_sign_of_zero(sec_build, tmp_path):
    """Compiled, ``claims(t, ALL)`` is ``RILA_US_S``'s ``claims(t)`` with its sign of zero.

    C4 compares numbers, and ``-0.0 == 0.0``, so a compiled total begun at ``0.0`` would
    pass it; :func:`test_a_total_of_negative_zero_kinds_is_s_negative_zero` holds modelx
    to S's bits.  Here the compiled model is: on the twin of S point 12 on the crash path
    under :data:`NEGATIVE_ZEROS`, set before it computes (:func:`_negative_zeros`), every
    month's ``claims(t, ALL)`` and ``claims_over_av(t, ALL)`` are S's by ``float.hex``,
    ``claims`` ``-0.0`` in 29 of its months.
    """
    build = sec_build(SEC)
    s_folder, sec_folder = _negative_zeros(tmp_path / "inputs")
    s = _read(s_folder, "s_negzero_c", NEGATIVE_ZEROS)
    try:
        theirs = _point(s, ZERO_POINT)
        months = range(theirs.proj_len())
        want = [theirs.cells[cell](t, None).hex() for cell in TOTALLED for t in months]
    finally:
        s.close()
    folder = compiled_case(build, tmp_path / "negzero",
                           edits={SCENARIOS: _copied(sec_folder.parent, SCENARIOS)})
    total = _references("Projection")["ALL"]
    position = list(_committed().index).index(ZERO_POINT)
    calls = [(cell, (t, total)) for cell in TOTALLED for t in months]
    got = run_compiled(folder.parent, build.package.name,
                       {"refs": NEGATIVE_ZEROS, "calls": {position: calls}})
    assert got["exit"] == 0, got["stderr"]
    have = [value.hex() if status == "ok" and type(value) is float else (status, value)
            for status, value in got["values"][position]]
    assert sum(h == "-0x0.0p+0" for h in have[:len(months)]) == 29
    assert have == want, [(c, h, w) for c, h, w in zip(calls, have, want) if h != w][:10]


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (cell, arguments, what modelx
# does, a value of None any number).  modelx answers a month outside cover with a zero, a
# complete year or a policy month end past a table with what the table holds there, and
# refuses a code past each family, an age outside the mortality's and a contract year
# before the lapse table's first by name; compiled, each is past a cache, and raises
# IndexError rather than read or write beyond it.  Every 2-D cache is nine wide and both
# 3-D caches seven legs by nine (spec_sec.py), so the first code past them is 9 and the
# first leg 7.  On the extract's anchor issued at the valuation date (_relabelled), 101.
_NO_AGE = "ValueError: point_id 101: the mortality table holds no rate at age {a}"
COMPILED_ONLY = [
    ("net_cf", (1203,), ("ok", None)),
    ("net_cf", (-1,), ("ok", None)),
    ("pols_if_at", (0, 9), ("raised", "ValueError: invalid timing")),
    ("av_pp_at", (0, 9), ("raised", "ValueError: invalid timing")),
    ("claims", (0, 9), ("raised", "ValueError: invalid kind")),
    ("claims_over_av", (0, 9), ("raised", "ValueError: invalid kind")),
    ("wd_bucket_value_pp", (0, 9), ("raised", "ValueError: invalid bucket")),
    ("market_state", (1, 9), ("raised", "ValueError: invalid name")),
    ("opt_portfolio_at", (0, 9), ("raised", "ValueError: invalid basis")),
    ("credit_rate_by", (0, 9), ("raised", "ValueError: invalid rule")),
    ("opt_component_at", (0, 7, 0), ("raised", "ValueError: invalid leg")),
    ("opt_component_pp", (0, 7, 8), ("raised", "ValueError: invalid leg")),
    ("opt_leg", (5,), ("raised", "ValueError: invalid leg index")),
    ("guar_min_rate", (8,), ("raised", "ValueError: invalid kind")),
    ("roll_share", (9,), ("raised", "ValueError: invalid bucket")),
    ("mort_rate_base_at", (122,), ("raised", _NO_AGE.format(a=122))),
    ("mort_rate_base_at", (-1,), ("raised", _NO_AGE.format(a=-1))),
    ("surr_charge_rate_at", (92,), ("ok", 0.0)),
    ("surr_charge_rate_at", (-1,), ("ok", 0.0)),
    ("lapse_rate_base_py", (93,), ("ok", 0.06)),
    ("lapse_rate_base_py", (-1,), ("raised", "ValueError: point_id 101: the lapse table "
                                   "holds no rate at or before contract year -1")),
    ("wd_amount_pm", (1082,), ("ok", 0.0)),
    ("wd_amount_pm", (-1,), ("raised", "ValueError: point_id 101: the withdrawal "
                             "programme holds no month end -1")),
]

# The codes inside the caches that a cell does not take, since one numbering serves each
# family's cells and every 2-D cache is nine wide: there the cell itself refuses the code,
# compiled as in modelx.  As (cell, arguments), on the anchor at month 1: a value cell's
# timing for the count and a count's for the value cells, the total for a kind cell and a
# rate kind for a claim cell, a claim kind for the guaranteed minimum, and a code past
# each smaller family.
CODES_IN_CACHE = [("pols_if_at", (1, 7)), ("av_pp_at", (1, 0)), ("inv_amt_pp_at", (1, 4)),
                  ("interim_value_pp_at", (1, 5)), ("iv_notional_pp", (1, 7)),
                  ("fixed_acct_pp_at", (1, 6)), ("av_at", (1, 2)),
                  ("claim_from_av_pp", (1, 3)), ("pols_decr", (1, 3)), ("claims", (1, 4)),
                  ("claim_pp", (1, 8)), ("guar_min_rate", (1,)), ("guar_min_rate", (3,)),
                  ("roll_share", (3,)), ("roll_share", (8,)),
                  ("wd_bucket_value_pp", (1, 3)), ("market_state", (2, 5)),
                  ("market_state", (2, 8)), ("opt_portfolio_at", (1, 3)),
                  ("opt_portfolio_abs_at", (1, 8)), ("opt_component_at", (1, 0, 3)),
                  ("credit_rate_by", (1, 2)), ("credit_rate_by", (1, 8)),
                  ("opt_leg", (3,)), ("opt_leg", (4,))]

# What a direct call refuses on points that project, on the extract, as (label, cell,
# arguments): each reader below its guard, the market before a later point's issue.
DIRECT = [(101, "mort_rate_base_at", (39,)), (101, "lapse_rate_base_py", (0,)),
          (124, "market_state", (12, 0)), (124, "index_level", (11,))]


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, the References, [(position, cell, arguments)], the Data cells to read).

    Each table is an extract, labelled otherwise than by position (:func:`_relabelled`),
    so that a refusal naming a point by ``idx + 1`` names another.  A position, not a
    label, since a table ``Data`` refuses has no keys to give: each is the row's place in
    the table written, ``Projection``'s ``idx``, which the test indexes ``Projection`` by in
    modelx too.
    """
    committed = _committed()

    def at(table, label):
        return list(table.index).index(label)

    def extract(edit=None):
        return _relabelled(edit(committed) if edit is not None else committed)

    cases = []
    for case, edit, _ in MALFORMED:
        cases.append((case, extract(edit), None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, file, edit, _ in TABLES:
        table = extract()
        cases.append((case, table, {file: edit}, {}, [(at(table, 114), "result_cf", ())],
                      (TABLE_READERS[file][1],)))
    for case, point, edit, *_ in REFUSED:
        table = extract(edit)
        cases.append((case, table, None, {}, [(at(table, point + 100), "result_cf", ())],
                      ()))
    for case, edit, point, _ in UNDECODABLE:
        table = extract(edit)
        cases.append((case, table, None, {}, [(at(table, point + 100), "result_cf", ())],
                      ()))
    for column, values in SPELLED.items():
        table = extract(_both(*(_set(column, [p], v) for p, v in values.items())))
        cases.append((f"{column} in another case or spaced", table, None, {},
                      [(at(table, p + 100), "result_cf", ()) for p in values], ()))
    for case, edit, label, files, refs, *_ in NOT_ISSUED:
        table = extract(edit)
        cases.append((case, table, files, refs,
                      [(at(table, label + 100), cell, ()) for cell in ("result_cf",
                                                                       "proj_len")], ()))
    for column, value, files in HUGE:
        label = 4 if column == "age_at_entry" else 2
        edit = _set(column, [label], value)
        if column == "age_at_entry":
            edit = _both(lambda t: t[(t["sex"] != "F") | (t.index == label)], edit)
        table = extract(edit)
        cases.append((f"{column} at {value:.3g}", table, files, {},
                      [(at(table, label + 100), "result_cf", ()),
                       (at(table, 101), "net_cf", (0,))], ()))
    table = extract()
    cases.append(("codes no cell of the family takes, inside the caches", table, None, {},
                  [(at(table, 101), cell, args) for cell, args in CODES_IN_CACHE]
                  + [(at(table, label), cell, args) for label, cell, args in DIRECT], ()))
    table = extract()
    table.index = pd.Index([*table.index[:-1], "1x"], name="point_id")
    cases.append(("a label written as text", table, None, {},
                  [(len(table) - 1, "point_id", ())], ("point_id",)))
    table = extract()
    table.index = pd.Index([*table.index[:-1], 2 ** 53], name="point_id")
    cases.append(("a label at 2**53", table, None, {}, [(len(table) - 1, "point_id", ())],
                  ("point_id",)))
    return cases


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position: every
    case of :data:`MALFORMED` and of :data:`TABLES`, refused by a projection and by the
    ``Data`` cell that checks the table, so that a compiled ``Data`` cell refuses each
    value its modelx cell refuses; every case of :data:`REFUSED`, a point past its cover
    or carrying more free withdrawal than its year allows; of :data:`UNDECODABLE` and
    :data:`SPELLED`, a value no decode knows; of :data:`NOT_ISSUED`, a point the caches
    cannot hold, by ``result_cf`` and ``proj_len``; of :data:`HUGE`, a whole number of
    ``2**53`` or more refused by its point while another projects; a label written as
    text or at ``2**53``, by ``Data.point_id``; a code a cell does not take, inside its
    cache (:data:`CODES_IN_CACHE`); and the direct calls of :data:`DIRECT`, each reader
    below its guard, where a read at index -1 would read a table's last row.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past each 2-D cache, a leg past the 3-D ones,
    a leg index, a rate kind and a bucket past their caches, and an age, a complete year,
    a contract year and a policy month end past the ``a``, ``cy``, ``y`` and ``m`` caches
    either side, each raising ``IndexError`` compiled, beside what modelx does.

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    first = list(_relabelled(_committed()).index).index(101)
    cases.append(("compiled only", _relabelled(_committed()), None, {},
                  [(first, cell, args) for cell, args, _ in COMPILED_ONLY], ()))
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused, projected, only = [], 0, 0, iter(COMPILED_ONLY)
    for case, table, edits, refs, calls, data in cases:
        temp_inputs(dest, model_path(SEC), model_points=table, model_point_file=TABLE,
                    edits=edits)
        model = _read(folder, "refused", refs)
        try:
            want = [_did(lambda: model.Projection[idx].cells[cell](*args))
                    for idx, cell, args in calls]
            want_data = {name: _did(model.Data.cells[name]) for name in data}
        finally:
            model.close()
        job = {"refs": refs, "calls": {}, "data": list(data)}
        for idx, cell, args in calls:
            job["calls"].setdefault(idx, []).append((cell, args))
        got = run_compiled(dest, build.package.name, job)
        assert got["exit"] == 0, f"{case}: the compiled run failed:\n{got['stderr']}"
        assert all(got["compiled"].values()), got["compiled"]
        have = {idx: iter(values) for idx, values in got["values"].items()}
        for (idx, cell, args), modelx_did in zip(calls, want):
            status, value = next(have[idx])
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == "compiled only":
                *_, (does, what) = next(only)
                if modelx_did[0] != does or (what is not None and modelx_did[1] != what):
                    found.append(f"{where}: modelx {modelx_did}, not {(does, what)}")
                if (status, str(value).split(":")[0]) != ("raised", "IndexError"):
                    found.append(f"{where}: compiled {status} {value!r}, not IndexError")
                continue
            if cell == "net_cf":
                if modelx_did[0] != "ok" or (status, value) != modelx_did:
                    found.append(f"{where}: modelx {modelx_did}, compiled {status} "
                                 f"{value!r}, where both project")
                projected += 1
                continue
            if modelx_did[0] != "raised":
                found.append(f"{where}: modelx returned, where a refusal was meant")
            elif (status, value) != modelx_did:
                found.append(f"{where}: compiled {status} {value!r}, modelx {modelx_did}")
            refused += 1
        for name, modelx_did in want_data.items():
            if modelx_did[0] != "raised":
                found.append(f"{case}: Data.{name}: modelx returned, where a refusal was "
                             f"meant")
            elif tuple(got["data"][name]) != modelx_did:
                found.append(f"{case}: Data.{name}: compiled {got['data'][name]}, modelx "
                             f"{modelx_did}")
            refused += 1
    assert not found, "\n".join(found)
    assert projected == len(HUGE)
    assert refused + projected == sum(len(calls) + len(data)
                                      for *_, calls, data in cases[:-1])


def _longest_cover():
    """The two rows at the contract's longest cover, issue age 0, issued now and 120 months
    on, the second on ``up-F120``, and each again: four points, two for each head of
    :data:`STACK_HEADS`."""
    committed = _committed()
    row = committed.loc[[1]]
    rows = pd.concat([row.assign(age_at_entry=0),
                      row.assign(age_at_entry=0, duration_mth=-120,
                                 scenario_id="up-F120")] * len(STACK_HEADS))
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows


# The cold calls the stack test makes, each on a point of its own, in the last month: the
# net cash flow, which walks every chain, and the count's residual.
STACK_HEADS = ("net_cf", "check_pols_roll_fwd_resid")

# The stacks the cold calls run on compiled, in a thread whose stack is reserved at each of
# these sizes in KiB, and then on the main thread.  1 MiB is the size asserted; the others
# bracket what the calls need, and the test reports the smallest that ran.  Each is a
# multiple of 64 KiB, the step Windows reserves a thread's stack in.
STACK_KIB = (256, 320, 384, 448, 512, 640, 768, 1024, 2048)

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the anchor at issue age 0, issued now and 120 months on, whose cover runs 1,080
    months (:func:`_longest_cover`), each on a point of its own, a cold ``net_cf`` and a
    cold ``check_pols_roll_fwd_resid`` in the last month run the chains from the end of
    the cover back to ``t_entry()``, 1,100 levels deep in modelx on a model just read
    (:func:`test_the_deepest_cold_call_runs_one_cell_a_month`), the longest the contract
    allows.  Compiled they run on the C stack, which the interpreter's recursion limit
    does not count.  1 MiB is the stack MSVC gives an executable's main thread unless the
    executable asks for more: a host that embeds Python, where python.exe itself asks for
    2,000,000 bytes.  A thread whose stack is reserved at 1 MiB stands in for it on every
    platform (``sec_support.run_compiled``), and in one each call runs cold and returns
    modelx's number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12
    elsewhere.  With MSVC 14.37, on the machine they were measured on, the calls ran on a
    reservation of 384 KiB and died on one of 320 (measured at M25).  Windows rounds a
    reservation up to 64 KiB, so the need lies between the two, and a finer step measures
    only the rounding: 2.7 to 3.2 times under 1 MiB.  From fixed reservations the chain
    takes about 287 bytes a level and 31 KiB besides, about 340 KiB (model-sec.md, *What a
    compiled run needs*).  gcc's need comes from the ``cython``
    job's Linux leg, whose warning records it, estimated at about twice MSVC's bytes a
    level, about 680 KiB, 1.5 times under 1 MiB.  A stack too small kills the child, and
    the test fails naming the stack.  The thread's stack is read back too, from Windows or
    from glibc, and must be at most 1 MiB and a page: a stand-in larger than asked for
    would stand for nothing.  And the calls run again on the child's main thread, which
    is what ``run_sec.py --cython`` runs on.

    The calls run first at each size of :data:`STACK_KIB`, before anything is asserted,
    and every size's outcome goes into a warning, which the job's summary shows, and into
    the failure, if there is one: the smallest size that ran bounds the stack the chain
    needs on the compiler at hand.  A size below the need kills its child on a stack
    overflow, by design.  Each bracketing child is waited for :data:`BRACKET_TIMEOUT`
    seconds and the two asserted runs :data:`ASSERTED_TIMEOUT`.
    """
    build = sec_build(SEC)
    rows = _longest_cover()
    folder = compiled_case(build, tmp_path / "longest", model_points=rows,
                           edits=EXTREME_EDITS)
    calls, want = {}, {}
    for key in range(len(rows)):
        head = STACK_HEADS[key // 2]
        model = _read(folder, "longest")
        try:
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert last - proj.t_entry() == 1079, key
            calls[key] = [(head, (last,))]
            want[key] = proj.cells[head](last)
        finally:
            model.close()
    job = {"refs": {}, "calls": calls}

    def child(timeout, **where):
        try:
            return run_compiled(folder.parent, build.package.name, job, timeout=timeout,
                                **where)
        except subprocess.TimeoutExpired:
            return {"exit": f"none, timed out after {timeout} s", "stderr": ""}

    runs = {f"a {kib} KiB thread": child(ASSERTED_TIMEOUT if kib == 1024
                                         else BRACKET_TIMEOUT, stack_kib=kib)
            for kib in STACK_KIB}
    runs["the main thread"] = child(ASSERTED_TIMEOUT, main_thread=True)
    ran = [kib for kib in STACK_KIB if runs[f"a {kib} KiB thread"]["exit"] == 0]
    late = [kib for kib in STACK_KIB
            if str(runs[f"a {kib} KiB thread"]["exit"]).startswith("none")]
    record = (f"the compiled cold calls at the longest cover ran on a thread of "
              f"{ran or 'no size'} KiB and not of "
              f"{[kib for kib in STACK_KIB if kib not in ran]} KiB"
              f"{f', timed out at {late} KiB' if late else ''}; on the main thread "
              f"{'they ran' if runs['the main thread']['exit'] == 0 else 'they failed'}")
    warnings.warn(record, UserWarning)
    for where in ("a 1024 KiB thread", "the main thread"):
        got = runs[where]
        assert got["exit"] == 0, (
            f"the compiled model's deepest cold call failed on {where}, exit code "
            f"{got['exit']} ({record}):\n{got['stderr']}")
        assert all(got["compiled"].values()), got["compiled"]
        for key, value in want.items():
            status, have = got["values"][key][0]
            assert status == "ok", (where, got["values"][key])
            assert _as_modelx(have, value), (where, have, value)
        reserved = got["stack"]["reserved"]
        if where == "a 1024 KiB thread" and reserved is not None:
            assert reserved <= (1 << 20) + 4096, (
                f"the thread has {reserved} bytes of stack, not 1 MiB")


# A compiled model's Reference set after it has computed, in a child of its own: what the
# base Projection, an ItemSpace made before the change and one made after give for
# expenses(12), before expense_maint is set to 0 and after.
STALE_CHILD = """\\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[0]
values = [p.expenses(12), early.expenses(12)]
p.expense_maint = 0.0
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
    imported.  This holds the compiled model to what they say, on ``expense_maint``,
    which moves ``expenses(12)`` on every point in force then: the base ``Projection``,
    the anchor's twin at ``idx`` 0, made before, and the worked example's twin, at ``idx``
    1, made after, so that a modelx-cython that began to clear caches would be seen here,
    and the advice changed with it.  A compiled value meets modelx's as C4 holds it
    (:func:`_as_modelx`), and one the compiled model kept, its own value of before,
    identically.
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
    model = _read(folder, "stale")
    try:
        p = model.Projection
        before = (p.expenses(12), projection(model, 0).expenses(12))
        p.expense_maint = 0.0
        fresh = (p.expenses(12), projection(model, 0).expenses(12),
                 projection(model, 1).expenses(12))
    finally:
        model.close()
    assert _as_modelx(base, before[0]) and _as_modelx(early, before[1]), (base, early,
                                                                          before)
    assert fresh[0] != base and fresh[1] != early
    assert (base_after, early_after) == (base, early), "the compiled model cleared a cache"
    assert _as_modelx(late, fresh[2]), (late, fresh[2])


@pytest.mark.cython
def test_run_sec_prints_the_compiled_model_as_it_prints_modelx(sec_build, tmp_path,
                                                                committed_runs):
    """``run_sec.py --cython`` prints, for a point and for the block, what modelx prints.

    Each run in an interpreter of its own, as a user runs it.  With ``--build`` it runs the
    session's build, so nothing is built in the tree, and it checks for itself that the
    package it imported is compiled.  Line for line, the compiled model's output is
    modelx's: the default point, the anchor issued at the valuation date, the anchor in
    force 71 months and the anchor issued 13 months on, each with where it came from,
    where it stands, its option budget, its interim values and its cash flows; and the
    block's lines for each point, its first twelve rows and its first twelve projection
    years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything; and a label the table lacks is refused under
    ``--cython`` as under modelx, naming the table's labels.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in ((), ("16",), ("24",), ("--block",)):
        expected = committed_runs(*args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "8", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
    done = _run_sec(runner, "99", "--cython", "--build", str(build.out), check=False)
    assert done.returncode == 1 and done.stdout == b""
    assert done.stderr.decode(errors="replace").strip() == (
        f"no model point 99 in the table: {list(range(1, 25))}")
