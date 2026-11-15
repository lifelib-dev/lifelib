"""In-force tests for FIA_US_SEC: the splice, future business, counts, regeneration.

``FIA_US_SEC`` is ``FIA_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M8).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the contract has been in force, ``duration_mth_init() + t``.  A model point may be a
contract already in force at the valuation date, in any month of its contract year, one
issued at it, or one to be issued after it, as in ``basiclife/BasicTerm_SE``.  A contract in
force opens with twelve columns of state beside its count: the account value, the fixed
account, the benefit base, the rollup base, the Model #805 floor, the lifetime withdrawal
and the withdrawals to date entering month 0; and, at the anniversary on or before the
valuation date, the account value and the fixed account, the phase as a code, the locked
payout percentage and the index level.  Its rate scenario is a copy of S's re-based to the
month it is valued at, in the companion ``rate_scenario_sec.csv``.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``FIA_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's six new-business points (T1).  S's goldens sit on its
in-force point 1, entered at anniversary 7, at its policy month 95; the twin of that point
is in force 84 months at the valuation date, so the goldens fall at its ``t = 11``, and
both the splice on S's in-force twins and the opening-state test, which continues the
committed twin from S, carry them over, cell by cell, with no number copied.  The
conventions also hold the SEC family's other rules: every frame opens at ``t = 0``,
``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the month's new
business, new business enters once, nothing happens before issue, and every month in
cover sits in one of the four GLWB phases.  This module holds the rest of the plan's tests
(its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  S's own in-force points 1, 3 and 7 are splice cases at 84, the month
  they enter S (§5.2).  The months straddle the product's events: an anniversary in
  accumulation; the exercise anniversary and the year under way before it, read in its
  last month; the first month of income; income after the surrender charge; the
  exhaustion of the account value and the income that runs on after it; joint income;
  the shock-lapse year; the end of the growth window; the first policy year and the year
  of a pre-exercise withdrawal; and the last covered month.  They run on stepped
  scenarios, and variants of S's points, in a copy of S's table, add each crediting
  method, the female table, two more withdrawal programmes and exercises either side of
  two payout band boundaries.  The same fixture, read again under the switched
  References, runs those S ships idle: the step-up at exercise, the dollar rollup-base
  reduction, the surrender-value collar, the caps on the lapse rate and the rider charge,
  the floors on the fixed rate, the cap and the credit, a trigger credit on a zero net
  return, and a minimum exercise age above the points' own.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue, every decrement rate 0.0 there,
  and no age, year or anniversary read before the contract's first.
* D11's R1, R1a and R2, and D3's clock: on the splice's rows no cell is called at a
  negative month, none evaluated on the books reads a month before them, none reads
  beyond ``t + 1`` but the one R2 admits, and no index level, scenario level or reference
  yield is read at an anniversary before the books; on the committed points no recursion
  runs backward over the frame, the deepest cold call runs one cell a month, and the policy
  clock is a closed form.  The admitted read is ``lapse_rate``'s: it reads the phase, the
  account value and the benefit base at the anniversary closing the contract year,
  ``anniv_mth(t)``, up to 11 months ahead, and the rules test walks what each such read
  depends on, which may hold no count, nothing after that anniversary and nothing the
  reader itself holds that year.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, and 2.5 times the count,
  with every assumption that ships at zero switched on, is 2.5 times every flow and moves
  no per-contract value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, by the one rule its case is built for, a key that the table it joins lacks among
  them (``MALFORMED``), and each assumption table whose keys or values cannot be read is
  refused, naming the file and the lines, each repeated key and each missing span, before
  a projection reads a value from it (``TABLE_FAULTS``); a text value no decode knows
  raises ``FIA_US_S``'s own message in both models (``UNDECODABLE``); the future horizon
  is a Reference that bounds future business, and at 0 refuses it; a point past
  maturity, or with no cover at all, is refused by ``proj_len()`` (``NOT_ISSUED``); the
  edges of the interface are accepted, each rule over a window of policy months refused
  just inside each end and read just outside, and each tolerance pinned from both sides;
  and every state ``FIA_US_S`` reaches, restated in force under each set of References on
  which those states differ, is accepted, exactly and carried to the cent, but a contract
  terminated, refused by name.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and its scenario companion
  are what the generator makes of ``FIA_US_S`` and its inputs as they stand, and every
  text cell in them is S's or composed from S's keys; and every committed row in force,
  and the one issued later, is its S point from its month on, cell by cell.
* Then the product's own facts: the two clocks on the shipped points, the opening state as
  S carries it, each column shown on a committed row, the year under way read from its
  columns, the phase as a code, the scenario on the valuation clock, withdrawals on the
  policy clock, expense inflation on the valuation clock, the premium and acquisition on
  new business, the lapse read at the closing anniversary, a depleted row in force, the
  cap on mortality and a NaN sent to it, a check whose residual is not a number, the
  guaranteed scale, the keyed readers against S's lookups, the checks' tolerance on a
  point of a million contracts, the values outside cover, the block, an in-force extract,
  the runner, the docstrings and their tables, the shared input tables, and what the
  default grid reaches.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen after this module's modelx tests before Phase 2 changed anything (§5.4).
* Stage EC, what compiling changed, held in modelx: the spec's sizes and the sample's
  recursion limit to their comments' derivations, the spec's map of S's totals and
  scenario columns onto SEC's codes, the ``ALL`` totals S's bit for bit, a negative zero
  among them, every parameterless cell a Python number, ``Data``'s arrays int64 or float64
  and padded with NaN where no read reaches, a table without a decoded column refused
  where S's is, the bounds the caches are sized from refused by ``proj_len()``, and the
  runner's in-place rebuild, its refusal to build in a ``lifelib.create()`` copy and its
  compensated block sum.
* The compiled tests, after the fingerprint, marked ``cython``: C4 on the splice grid
  under both sets of References, at the contract's extremes, where the caps bind, on
  labels that are not text, on keys written as floats and out of order, on keys far past
  every frame and with a NaN sent through a Reference; every refusal compiled as in modelx,
  and the compiled model's own past its caches; a zero divisor and a negative power base;
  the deepest cold call on a 1 MiB stack and on the main thread; a Reference set after a
  Space has computed; and the runner, with its refusal of a directory without a build.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 84 for
the twin of an S point that S enters at 84, and ``-k`` for one issued ``k`` months on.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  An FIA projection costs about
as much as a MYGA one, and T2, T3 and the switched References over every point at every
month, 44, 15 and 9 cases, would add about half again to this module's run time in every
run.  By default they run a core of 12, 5 and 5 cases, chosen so that between them they
reach every branch, every opening-state column, every phase at the valuation date and
every kind of valuation month the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts, and every line of ``Projection``'s
formulas the full grid's rows execute when swept, as line coverage of the two grids
showed when the core was last chosen: the shipped References' core reaches every line its
full grid does, and the switched References' core every line its own full grid does but
those the shipped core reaches.  The other cases, and the rules
test's scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason
shown, unless ``USLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of the CI
matrix sets it, so every CI run runs the full grid, and ``USLIB_SEC_FULL=1 python -m
pytest -m sec_full`` on this module runs them alone.  Memory is the other cost: a
projected point holds its cached values and their dependency graph, so a row read once, a
splice case's or a point of a temporary copy, is released as soon as it has been read
(``_release``), the splice's rows are held one at a time, however large the grid, and the
two splice fixtures, the shipped References' and the switched ones', are one fixture that
holds one of them at a time.  The committed models, swept, are most of what the module
holds, so the two tests that read S and SEC afresh under References of their own, the cap
on mortality and the guaranteed scale, run before those are read, never beside them.  The
swept models the module holds are frozen out of the collector, and the freeze is undone as
the module ends.

Every test keeps five rules.  Each model is read under a name of its own and closed:
``test_fixed_indexed_annuity_us.py`` reads S under its default name, and reading a model
under a name in use renames the open one.  No test writes inside the library tree: every
changed input goes through ``sec_support.temp_inputs`` into a temporary directory, because
a CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row; a table the model refuses has no keys, and a row's is taken
from the file as ``run_sec.py`` takes one (``_file_key``).  Every Reference a test changes
is set on a model read afresh, before it computes anything, because a compiled model never
clears a cache.  And a timing, a kind or a phase is passed through ``_code``, which hands
the model its own Reference where it defines one and the string otherwise, and every twin
comparison goes through ``_mismatches``, which passes the SEC Space's codes, so that the
same calls serve Phase 2's int codes.  The phases are codes already: ``FIA_US_SEC`` brings
them forward to stage E, and the comparisons map S's phase strings onto them.
"""
import ast
import dataclasses
import gc
import importlib.machinery
import inspect
import io
import itertools
import json
import math
import numbers
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
    _FIA_PHASE_CODES, GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table,
    check_generated, codes, compiled_case, compiled_mismatches, exact_here,
    fingerprint_mismatches, frame_mismatches, run_compiled, sweep, temp_inputs,
    twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "FIA_US_SEC", "FIA_US_S", "model_point_table_sec.csv"
COMPANION = "rate_scenario_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's six new-business points, the worked example's anchor issued at t = 0 (2) and its
# variants on the switches the technical notes make first-class: pure stacking with a
# fifth of the premium in the fixed account (4), the joint basis (5), no rider (6), a
# $60,000 withdrawal before exercise (8) and income deferred to 85 (9).
S_POINTS = (2, 4, 5, 6, 8, 9)

# S's in-force points, 1 (the anchor), 3 (the simple rollup) and 7 (the anchor overdrawing
# at 105%), each entered at anniversary 7, policy month 84.  FIA_US_S runs on the policy
# clock, so each is a splice case at offset 84 (§5.2): its twin is in force 84 months at
# the valuation date, and SEC's t = 0 is S's month 84.
IN_FORCE_TWINS = (("twin", 1, 84), ("twin", 3, 84), ("twin", 7, 84))

# Eight more S points, in the splice's copy of S's table and never in the committed one, for
# the categories S's own points do not carry, each at a scale of its own:
#
# 10, S point 2 crediting by participation, with no stack and no rollup, on the growth
#   path: the par method, and the 'none' rollup on a capped contract;
# 11, S point 2 crediting by spread, on the growth path;
# 12, S point 9 crediting by trigger, female: the trigger method, and the female mortality
#   rows at every age a contract deferred to 85 reaches;
# 13, S point 6, without the rider, withdrawing $150,000 at anniversary 3, more than its
#   account value: a contract emptied in accumulation, ACCUM to TERMINATED;
# 14, S point 8 withdrawing $20,000 at anniversary 3, against the anchor programme's
#   $60,000: a withdrawal past the free amount but well inside the account value;
# 16, 17 and 18, the anchor exercising at 69, 79 and 80, so that with its own 70 and
#   point 9's 85 a projection reads both sides of the 69/70 and 79/80 band boundaries.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.  The anchor's issue age, 62, puts the 54/55 and 59/60 boundaries
# out of an exercise's reach: the keyed-reader test reads every age of the bands on both
# bases, which is what holds those, and in Phase 2 that test runs compiled too.
VARIANTS = {
    10: (2, {"policy_id": "FIA-900010", "credit_method": "par", "stack_factor": 0.0,
             "rollup_id": "none", "scenario_id": "growth"}),
    11: (2, {"policy_id": "FIA-900011", "credit_method": "spread",
             "scenario_id": "growth"}),
    12: (9, {"policy_id": "FIA-900012", "credit_method": "trigger", "sex": "F"}),
    13: (6, {"policy_id": "FIA-900013", "wd_schedule_id": "overdraw"}),
    14: (8, {"policy_id": "FIA-900014", "wd_schedule_id": "small"}),
    16: (2, {"policy_id": "FIA-900016", "income_start_age": 69}),
    17: (2, {"policy_id": "FIA-900017", "income_start_age": 79}),
    18: (2, {"policy_id": "FIA-900018", "income_start_age": 80}),
}

# One more, for the switched References alone: 15, S point 2 with a cap of 0.1%, below
# cap_rate_min, on the growth path, so that the cap's floor binds where the credit floor,
# raised to 0.1%, is apart from it.
SWITCHED_VARIANTS = {
    15: (2, {"policy_id": "FIA-900015", "cap_rate": 0.001, "scenario_id": "growth"}),
}

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is read on the valuation clock in SEC and on the policy clock in S
# (D7): S inflates its in-force points from issue, so at the shipped 2.5% the expenses of
# a row opened at d differ by 1.025 ** (d / 12), by design, and at 0 both factors are 1;
# the clock itself is asserted on its own, at the shipped rate.  The rest are assumptions
# that ship at a value that hides some of the state from any comparison:
#   index_cost_rate 0.5%, deducted from the index return before the cap, the
#     participation and the spread, so that a credit taken on the gross return shows;
#   rider_charge_from_mgsv True, so that the rider charge also comes off the Model #805
#     floor, and the floor's chain reads the benefit base;
#   mgsv_annual_charge $50, the floor's annual charge, 0 as shipped;
#   comm_rate_acq 5% and premium_tax_rate 2%, a commission and a premium tax on new
#     business, both 0 as shipped;
#   mgsv_rate 3%, against the shipped 1%, so that the floor overtakes the surrender value
#     and pays a surrender, and the floor's state shows in the claims.
# The identity does not depend on the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "index_cost_rate": 0.005,
                "rider_charge_from_mgsv": True, "mgsv_annual_charge": 50.0,
                "comm_rate_acq": 0.05, "premium_tax_rate": 0.02, "mgsv_rate": 0.03}

# The switched References, beside SPLICED_REFS: the three string switches at their other
# settings, the step-up at exercise only, the rollup base reduced dollar for dollar and the
# MVA collared at the surrender value; the index cost back at its shipped 0, which the
# spliced grid exercises, so that a flat index year is a net return of exactly 0, where
# the trigger credits (net >= 0, and a trigger read as net > 0 fails); and each cap and
# floor S ships idle, set where it binds with an effect:
#   shock_lapse_no_rider 40%, past lapse_rate_max, 35%, in the shock year of a contract
#     without the rider;
#   rider_charge_rate 2%, past rider_charge_rate_max, 1.5%;
#   fixed_rate 0.5%, below fixed_rate_min, 1%;
#   floor_rate 0.1%, the credit floor raised from 0, strictly between 0 and cap_rate_min,
#     0.25%, so that a floor written as 0.0 in place of floor_rate fails, and so does one
#     that reads the cap's floor for it: variant 15's cap of 0.1% is floored at 0.25%;
#   min_income_age 71, above the income start age of 70 that every point but 9 carries,
#     so that the contractual minimum exercise age binds, a year later.
SWITCHED_REFS = {**SPLICED_REFS, "index_cost_rate": 0.0, "step_up_mode": "at_exercise",
                 "rb_wd_convention": "dollar", "mva_collar_basis": "surrender_value",
                 "shock_lapse_no_rider": 0.40, "rider_charge_rate": 0.02,
                 "fixed_rate": 0.005, "floor_rate": 0.001, "min_income_age": 71}
REFS = {"spliced": SPLICED_REFS, "switched": SWITCHED_REFS}

# The worked scenario stepped in the splice's copies, (anniversary, index level, reference
# yield): the shipped path is flat through anniversary 7 and steps once, at 8, so a row
# re-based to the wrong month reads the same level at nearly every anniversary.  Stepped,
# the yield moves at 6, both move at 8, 12, 18 and 25, and the index falls at 25, so that
# a level read a year off, or at the wrong row's month, reads another number.  The growth
# path, flat after anniversary 20, is extended likewise, with a fall at 30.
WORKED_STEPS = ((0, 5000.0, 0.030), (6, 5000.0, 0.032), (8, 5450.0, 0.035),
                (12, 5800.0, 0.033), (18, 6100.0, 0.036), (25, 6000.0, 0.034))
GROWTH_STEPS = ((25, 3800.0, 0.042), (30, 3700.0, 0.038), (40, 4100.0, 0.041))


def _stepped(table):
    """S's scenarios with the worked path stepped and the growth path extended."""
    rest = table[table["scenario_id"] != "worked"]
    rows = [("worked", *step) for step in WORKED_STEPS]
    rows += [("growth", *step) for step in GROWTH_STEPS]
    extra = pd.DataFrame([(*row, "stepped for a test") for row in rows],
                         columns=table.columns)
    return pd.concat([extra.iloc[:len(WORKED_STEPS)], rest,
                      extra.iloc[len(WORKED_STEPS):]], ignore_index=True)


def _programmes(table):
    """S's withdrawal programmes with variants 13's and 14's, at anniversary 3."""
    extra = pd.DataFrame([("overdraw", 2, 150000.0, "a test"),
                          ("small", 2, 20000.0, "a test")], columns=table.columns)
    return pd.concat([table, extra], ignore_index=True)


def _mortality_cut(table):
    """The mortality table with age 120 at 0.5, both sexes, rather than certain death.

    At the shipped rate of 1 every contract dies in the first month of the year it enters
    at 120, so its last eleven months, the deemed maturity among them, hold no count, and a
    row restated there projects zeros.  At 0.5 they hold one.
    """
    out = table.copy()
    out.loc[out["age"] == 120, "mort_rate"] = 0.5
    return out


# The input files the splice's copies change, S's and SEC's alike.  SEC reads its scenario
# from rate_scenario_sec.csv, which the generator writes afresh from the stepped S.
SPLICED_EDITS = {"rate_scenario.csv": _stepped, "withdrawal_table.csv": _programmes,
                 "mort_table.csv": _mortality_cut}
SEC_EDITS = {name: edit for name, edit in SPLICED_EDITS.items()
             if name != "rate_scenario.csv"}

# T2's rows restated from S's new-business points and the variants, as (row_kind, S point,
# source_mth).  The months are S's, each chosen for what falls there:
#   on the anchor issued at t = 0 (2), the plan's six: 60, an anniversary in accumulation;
#     84, anniversary 7, where S's in-force points enter; 95, the last month of contract
#     year 8, whose closing anniversary is the exercise; 96, the first month of income;
#     144, income after the surrender charge; and 240, DEPLETED, the account value
#     exhausted and the income running on; with 216 between, income near exhaustion;
#   on S's in-force points, the anchor at 95 and the overdraw at 216, and the simple
#     rollup at 96;
#   on the fixed account (4): at 60, 95 and 96 as on the anchor, the fixed account accrued
#     since the anniversary at 95, and 144 and 240 in income;
#   on the joint basis (5): 95, 119, its exercise month, 150 in income, 288 near
#     exhaustion;
#   without the rider (6): 60, 125 in the shock-lapse year 11, 240, 696 the last policy
#     year, entered at 120, and 707, the last covered month;
#   on the pre-exercise programme (8): 6, the first policy year, and 30, 35 and 36, either
#     side of its $60,000 withdrawal at policy month 35, and 96;
#   on income deferred to 85 (9): 125, the shock lapse with the rider idle, 240, the end of
#     the growth window, and 270 and 275 in its exercise year, 23;
#   and the variants, each mid-year or on its own exercise month.
SPLICES = (
    ("derived", 1, 95), ("derived", 3, 96), ("derived", 7, 216),
    *(("derived", 2, d) for d in (60, 84, 95, 96, 144, 216, 240)),
    *(("derived", 4, d) for d in (60, 95, 96, 144, 240)),
    *(("derived", 5, d) for d in (95, 119, 150, 288)),
    *(("derived", 6, d) for d in (60, 125, 240, 696, 707)),
    *(("derived", 8, d) for d in (6, 30, 35, 36, 96)),
    *(("derived", 9, d) for d in (125, 240, 270, 275)),
    ("derived", 10, 95), ("derived", 10, 144), ("derived", 11, 95), ("derived", 11, 216),
    ("derived", 12, 125), ("derived", 12, 270), ("derived", 13, 30), ("derived", 14, 30))

# T3's cases, as (S point, k): four of S's new-business points and the eight variants
# issued a month on, which puts their anniversaries a month off the valuation years, and
# three S points issued more than a year on, the anchor and the pre-exercise programme 15
# months on and the joint point 13, so that a missing guard reads contract year -1, or an
# anniversary before issue, there.  So every one of S's six new-business points is among
# them, the anchor twice.
FUTURES = ((2, 1), (2, 15), (4, 1), (5, 13), (6, 1), (8, 15), (9, 1), (10, 1), (11, 1),
           (12, 1), (13, 1), (14, 1), (16, 1), (17, 1), (18, 1))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("twin", 1, 84): "S's anchor in force: the exercise year under way, the goldens at 11",
    ("twin", 3, 84): "the simple rollup, in force; the step-up binding",
    ("twin", 7, 84): "the overdraw: an excess every year, INCOME to TERMINATED",
    ("derived", 4, 95): "a year's last month: the fixed account accrued since",
    ("derived", 4, 96): "income on an anniversary, the fixed account in income",
    ("derived", 5, 95): "joint, the exercise year opened before the valuation date",
    ("derived", 8, 6): "the first policy year: the issue values by rule",
    ("derived", 13, 30): "no rider, its account value emptied: ACCUM to TERMINATED",
    ("derived", 6, 125): "no rider in the shock-lapse year, the shipped 33% applied",
    ("derived", 2, 240): "DEPLETED: no account value, the income running on",
    ("derived", 2, 216): "income at 80, the rate locked at 70 carried past a band",
    ("derived", 6, 707): "the last covered month: the deemed maturity at t = 0",
}
CORE_FUTURES = {
    (2, 15): "issued more than a year on: an anniversary before issue",
    (10, 1): "the par method, no stack, no rollup",
    (11, 1): "the spread method",
    (12, 1): "the trigger method, female",
    (14, 1): "a withdrawal past the free amount, before exercise",
}

# The switched References' grid and its core, as T2's and T3's, each at a month where a
# switch or a bound acts: S's simple rollup in force at 84, whose account value overtakes
# its base, so that the step-up binds at exercise, a year later under the minimum
# exercise age, and not at the anniversary before; the anchor at anniversary 7; the fixed
# account in the last month of its contract year 8; the shock year without the rider; the
# pre-exercise and the small programmes; the cap of 0.1%; the trigger; and a future row.
SWITCHED_GRID = (("twin", 3, 84), ("derived", 2, 84), ("derived", 4, 95),
                 ("derived", 6, 125), ("derived", 8, 30), ("derived", 14, 30),
                 ("derived", 15, 95), ("derived", 12, 125), ("future", 8, -15))
SWITCHED_CORE = {
    ("twin", 3, 84): "the step-up at exercise, and none at the anniversary before",
    ("derived", 15, 95): "the cap's floor apart from the credit floor; the collar",
    ("derived", 4, 95): "the fixed rate's floor, the dollar rollup base",
    ("derived", 6, 125): "the lapse cap in the shock year without the rider",
    ("derived", 12, 125): "the trigger's floor and the raised credit floor",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# The cells T2 and T3 skip beyond T1's (TWIN_EXEMPT_DEFAULT and the spec's exempt, which
# drop S's opening-state cells, entry_year, entry_mth and result_pols as a whole):
#   proj_len counts from the valuation date on SEC and from issue on S, so it differs by
#     d, or by -k, by design; frame_mismatches asserts what it must get right, that both
#     frames end at the same instant;
#   scenario_id names a row's own re-based copy of its S scenario, -M{d} or -F{k};
#   anniv_mth and year_open_mth are months of the frame, on the valuation clock, S's less
#     d, or plus k;
#   lw_pp_init, on a row restated in force, is the lifetime withdrawal S carries into d,
#     where S's cell is its own column, the withdrawal at entry; on a future row both are 0;
#   result_cf_annual, on a row restated mid-year, has a first row that is part of a
#     contract year, by design; its months are each compared in result_cf, and the clocks
#     test holds the report.
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "scenario_id", "anniv_mth", "year_open_mth", "lw_pp_init",
                    "result_cf_annual"})
FUTURE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "scenario_id", "anniv_mth", "year_open_mth"})

# The roll-forward residuals, whose exact value is 0 and whose computed value is rounding
# around it, up to about 3e-11 in most months: the splice compares them at the harness's
# absolute floor of 1e-9 and everything else with none (§5.2, precised at M11).  On a
# contract wholly in the fixed account, alloc_indexed 0, the indexed account and its credit
# are exactly 0 too, and computed as rounding, the account value less the fixed account:
# in S up to 7.3e-12 for the account and 1.0e-12 for the credit, and on a row restated from
# such a contract at month 6, whose opening columns the CSV gives back an ulp off, as low
# as -1.1e-11 for the account and -1.4e-12 for the credit, the credit's floor of 0 applying
# to the rate and not to a base that is negative by rounding.  So a variant with
# alloc_indexed 0 compares av_indexed_pp_at, av_indexed_pp, av_indexed_pp_year_open,
# index_credit_pp and result_av at the floor as well, and adds them to this set.  No row of
# the grid has one.
RESIDUALS = frozenset({"check_av_roll_fwd_resid", "check_pols_roll_fwd_resid"})

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 2.5%, the only places an in-force row departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "result_cf",
                             "result_cf_annual"})

# The decrement rates, which result_pols reports in every month: before issue each is the
# float 0.0 (R1, D4).
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
                   "lapse_rate_base", "shock_lapse_rate")

# The cells keyed by an age, a contract year, a count of completed years or an anniversary
# number, which a future row may not read below its first: the attained ages from the issue
# age, the contract years from 1, the completed years and the anniversaries from 0.
AGE_READERS = ("mort_rate_base_at", "payout_rate_at")
YEAR_READERS = ("surr_charge_rate_py", "vest_rate_py", "rollup_rate_py")
ANNIV_READERS = ("index_level", "scenario_value", "mva_ref_yield", "wd_scheduled_at")

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# rate, a clock, a code or a flag, and must not move when the count does.  The residuals
# are rounding on that many contracts, and scale with nothing; the checks over them must
# still close.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_death", "pols_lapse", "pols_maturity", "pols_decr",
    "premiums", "prem_to_av", "withdrawals", "wd_guar", "wd_excess", "income_payments",
    "claims", "claims_from_av", "claims_over_av", "commissions", "expenses",
    "premium_taxes", "net_cf", "av_at", "inv_income", "rider_charges", "wd_from_av",
    "av_depletion", "av_change", "result_cf", "result_pols", "result_cf_annual"})
SCALED = sorted(COUNTED - {"result_cf", "result_pols", "result_cf_annual"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# rates, its deaths, surrenders and deemed maturities in processing order, and the notes'
# end-of-month l(t), as FIA_US_S reports it.
RESULT_POLS = ["pols_if", "pols_new_biz", "mort_rate", "mort_rate_mth", "lapse_rate",
               "lapse_rate_mth", "pols_death", "pols_lapse", "pols_maturity",
               "pols_if_aft_decr"]
OUTFLOWS = ["pols_death", "pols_lapse", "pols_maturity"]
POLS_RATES = ["mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth"]

# The five count timings, BEF_NB the one running in force adds; the account value's five,
# which the fixed account, the indexed account and the account value in force share; the
# benefit base's four; the lifetime withdrawal's two; and the three benefit kinds.  Each is
# passed through _code.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_MORT", "BEF_LAPSE", "AFT_DECR")
AV_TIMINGS = ("BEF_PREM", "BEF_INV", "BEF_FEE", "BEF_WD", "EOY")
BB_TIMINGS = ("BEF_ROLLUP", "BEF_STEP_UP", "BEF_WD", "EOY")
LW_TIMINGS = ("BEF_WD", "EOY")
KINDS = ("DEATH", "LAPSE", "MATURITY")
KINDED = ("pols_decr", "claim_pp", "claim_from_av_pp", "claims", "claims_from_av",
          "claims_over_av")
TIMED = {"pols_if_at": TIMINGS, "av_pp_at": AV_TIMINGS, "av_fixed_pp_at": AV_TIMINGS,
         "av_indexed_pp_at": AV_TIMINGS, "av_at": AV_TIMINGS,
         "benefit_base_pp_at": BB_TIMINGS, "lw_pp_at": LW_TIMINGS}

# FIA_US_SEC's phase labels, in the order of their codes, as result_glwb() reports them.
PHASES = ("PRE_ISSUE", "ACCUM", "INCOME", "DEPLETED", "TERMINATED", "MATURED")

# What each monthly cell holds outside cover, before issue and from the month cover has
# ended, as its docstring says: no count, so no cash flow; no account value, benefit base,
# floor, withdrawal or charge; no rate; no question about the contract answered yes; and
# the moneyness factor that gates the dynamic lapse at 1.0, "no adjustment".  The phase
# cells hold PRE_ISSUE before issue and MATURED from maturity on.  The type is part of the
# value: a count, an amount or a rate is a float in every branch, a flag a bool and a phase
# an int code, because Phase 2 types a cell by the values it returns (USLIB-SEC-PLAN.md
# F3).  The guard test also calls each of TIMED at each of its timings and the KINDED cells
# at each kind, all 0.0.  (S's mva_pp_on, on a base of 1,000, was among them at stage E;
# stage EC writes it inline in wd_mva_pp and mva_pp, which are here.)
OUTSIDE_COVER = {
    "is_active": False, "is_exercise": False, "in_growth_period": False,
    "step_up_applies": False, "rider_in_force": False, "rider_in_force_open": False,
    "depletion_cause": False, "mva_in_force": False,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0, "pols_lapse": 0.0,
    "pols_maturity": 0.0,
    "index_return": 0.0, "credit_rate": 0.0, "surr_charge_rate": 0.0, "vest_rate": 0.0,
    "rollup_rate": 0.0, "payout_rate_locked": 0.0, "mort_rate": 0.0, "mort_rate_mth": 0.0,
    "shock_lapse_rate": 0.0, "lapse_rate_base": 0.0, "lapse_moneyness_factor": 1.0,
    "lapse_rate": 0.0, "lapse_rate_mth": 0.0, "mva_term": 0.0, "mva_rate": 0.0,
    "wd_reduction_rate": 0.0,
    "index_credit_pp": 0.0, "fixed_interest_pp": 0.0, "fixed_interest_ann_pp": 0.0,
    "inv_income_pp": 0.0, "rider_charge_pp": 0.0, "av_pp": 0.0, "av_pp_year_open": 0.0,
    "av_fixed_pp": 0.0, "av_fixed_pp_year_open": 0.0, "av_indexed_pp": 0.0,
    "av_indexed_pp_year_open": 0.0, "av_depletion_pp": 0.0, "prem_to_av_pp": 0.0,
    "prem_to_mgsv_pp": 0.0, "rollup_base_pp_year_open": 0.0, "rollup_pp": 0.0,
    "stack_pp": 0.0, "benefit_base_pp": 0.0, "rollup_base_pp": 0.0, "lw_pp": 0.0,
    "wd_scheduled_pp": 0.0, "wd_pp": 0.0, "wd_guar_pp": 0.0, "wd_excess_pp": 0.0,
    "wd_unfunded_pp": 0.0, "wd_guar_paid_pp": 0.0, "wd_excess_paid_pp": 0.0,
    "wd_cum_pp": 0.0, "free_wd_base": 0.0, "free_wd_allow": 0.0, "wd_free_pp": 0.0,
    "free_wd_remain": 0.0, "wd_charge_base_pp": 0.0, "surr_charge_base_pp": 0.0,
    "wd_charge_pp": 0.0, "wd_clawback_pp": 0.0, "wd_mva_pp": 0.0, "wd_payment_pp": 0.0,
    "surr_charge_pp": 0.0, "surr_clawback_pp": 0.0, "mva_pp": 0.0, "surr_value_pp": 0.0,
    "surr_benefit_pp": 0.0, "mgsv_charge_pp": 0.0, "mgsv_pp": 0.0,
    "premiums": 0.0, "prem_to_av": 0.0, "wd_guar": 0.0, "wd_excess": 0.0,
    "income_payments": 0.0, "withdrawals": 0.0, "commissions": 0.0, "premium_taxes": 0.0,
    "expenses": 0.0, "net_cf": 0.0, "inv_income": 0.0, "rider_charges": 0.0,
    "wd_from_av": 0.0, "av_depletion": 0.0, "av_change": 0.0,
    "check_av_roll_fwd_resid": 0.0, "check_pols_roll_fwd_resid": 0.0,
    "phase": ("PRE_ISSUE", "MATURED"), "phase_open": ("PRE_ISSUE", "MATURED"),
    "phase_year_open": ("PRE_ISSUE", "MATURED")}

# The cells a month outside cover may not reach: the clock cells keyed by the contract
# year, the attained age and the anniversary, and every reader keyed by a contract year,
# an age, a count of completed years or an anniversary number, which no month outside
# cover has, with S's two age-keyed cells no projection cell calls.  None has a guard of its
# own: the clock cells are arithmetic and would answer harmlessly, the readers would read
# a table at a key the contract does not have, and the scenario readers are inputs, left
# unguarded so that a pre-issue read of a future row's re-based scenario fails loudly
# (T3).  No formula reaches them outside cover, and a caller must not either
# (USLIB-SEC-PLAN.md F4).
IN_COVER_ONLY = ("age", "covered_age", "exercise_age", "policy_year", "duration",
                 "anniv_mth", "year_open_mth", "surr_charge_rate_py", "vest_rate_py",
                 "rollup_rate_py", "mort_rate_base_at", "payout_rate_at", "wd_scheduled_at",
                 "index_level", "scenario_value", "mva_ref_yield", "activation_rate",
                 "payout_rate")
SCENARIO_READERS = ("scenario_value", "mva_ref_yield", "index_level")

# The monthly cells defined at every month, inside cover or out: the policy clock, the
# anniversary month, which stack_pp and rollup_pp ask first, in S's order, before their
# guarded test, and expense inflation, an input on the valuation clock (D7).
EVERY_MONTH = ("duration_mth", "is_anniv", "inflation_factor")

# The bools each text column S branches on, and each string switch, is decoded into, once
# a point, so that no monthly cell compares a column's or a switch's text or calls a label
# accessor (USLIB-SEC-PLAN.md §7.1, *Record — M14*), each read where S asks its question.
# The text a monthly cell still compares is S's own timing and kind strings; the four joins
# on text keys, the scenario, the rollup schedule, the withdrawal programme and the
# mortality, are each made in the one cell that reads its table.
DECODES = ("is_single_basis", "is_joint_basis", "is_credit_cap", "is_credit_par",
           "is_credit_par_cap", "is_credit_spread", "is_credit_trigger",
           "is_step_up_annual", "is_step_up_at_exercise", "is_rb_pro_rata", "is_rb_dollar",
           "is_collar_gross", "is_collar_surrender_value")

# The opening state, in Data's order: the nine amounts of money, the payout rate, the phase
# code and the index level.  And the cells running in force adds to FIA_US_S's, each of
# which the symbol map must name.
MONEY = ("av_pp_init", "av_fixed_pp_init", "av_pp_prev_anniv_init",
         "av_fixed_pp_prev_anniv_init", "benefit_base_pp_init", "rollup_base_pp_init",
         "mgsv_pp_init", "lw_pp_init", "wd_cum_pp_init")
STATE = (*MONEY, "payout_rate_locked_prev_anniv_init", "phase_prev_anniv_init",
         "index_level_prev_anniv_init")
NEW_CELLS = ("point_id", "mort_schedule", "rollup_number", "scenario_number",
             "wd_schedule_number",
             "policy_count", "duration_mth_init", "maturity_mth", "t_entry", "is_active",
             "pols_new_biz", "prem_to_mgsv_pp", "phase_year_open",
             "rollup_base_pp_year_open", "surr_charge_rate_py", "vest_rate_py",
             "rollup_rate_py", "payout_rate_at", "wd_scheduled_at", "mort_rate_base_at",
             "av_pp_prev_anniv_init", "av_fixed_pp_prev_anniv_init",
             "payout_rate_locked_prev_anniv_init", "phase_prev_anniv_init",
             "index_level_prev_anniv_init", "wd_cum_pp_init", *DECODES)

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

REPORTS = ("result_cf", "result_pols", "result_av", "result_glwb", "result_cf_annual")

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  Every chain runs forward, one cell a month, and a report evaluates
# each column in ascending t, so a forward recursion, through t - 1, finds the month before
# already cached.  But the floor's chain is first read cold deep in the frame:
# lapse_rate reads the phase closing the contract year, which at an anniversary that
# exhausts the account value reads depletion_cause, then wd_mva_pp and mgsv_pp, inside
# result_cf's pols_if column, before any other column has evaluated the floor.  The
# committed points' sweep reaches 370 on point 9, as FIA_US_S's same sweep does on the same
# point, in the same order of evaluation (M21: stage E's 371 held S's mva_pp_on, which
# stage EC writes inline): it runs under 400 and not under 360.  A
# backward recursion over the frame, through t + 1, opens a chain as long as the frame, and
# every committed frame but the last policy year's, 12 months, is longer than 460.
CALL_DEPTH = 400

# The frames a cold call may hold on modelx's stack beyond one a month back to t_entry()
# (asserted as a bound, as Term's is).  Measured on a model just read, at the last month:
# on the committed points 10 at most on net_cf (the last policy year's), 9 on av_pp, 8 on
# av_fixed_pp, and 12 on mgsv_pp and wd_cum_pp, on the overdraw's twin, whose first
# anniversary evaluates the account value's chain under the floor's; at the contract's
# longest cover, 972 months from issue age 40, 7 on net_cf and 3 on mgsv_pp, at the
# valuation date and 120 months on.  A chain of two cells a month doubles the depth and
# fails here.
CHAIN_OVERHEAD = 16

# The months R2's one admitted read reaches ahead, at most: lapse_rate(t) reads the state
# at anniv_mth(t), up to 11 months on.  A count called cold, alone, opens its chain at its
# first month on the books, where lapse_rate reads the anniversary closing that contract
# year, and so the account value's chain up to 11 months long, under the count's: the
# count's cold depth is bounded by CHAIN_OVERHEAD and this together.  Measured: 25 over the
# month count on the committed points (the future row's), and 25 at the longest cover.
LOOK_AHEAD_MTHS = 11

# What only FIA_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t from issue with the frame opening at
# entry_mth() and proj_len() = 12 policy_term(); entry by entry_year(); pols_if(entry_mth())
# = l(0) = 1; the scenario's t an anniversary number; the single premium in a new issue's
# month 0; and "then clear the cache", modelx-only advice that a compiled model cannot
# follow.  Each is a phrase of FIA_US_S's own, which the docstring test checks.
STALE_PHRASES = (r"~\.FIA_US_S\.",
                 r"``t = 0`` is the first month of a model point projected from issue",
                 r"The frame is ``t = entry_mth\(\)",
                 r"``proj_len\(\)`` is ``12 \* policy_term\(\)``",
                 r"``proj_len\(\) = 12 \* policy_term\(\)``",
                 r"``entry_year\(\)`` completed contract years",
                 r"is indexed from ``entry_mth\(\)``",
                 r"``pols_if\(entry_mth\(\)\) = l\(0\) = 1``",
                 r"``t`` is an \*\*anniversary\*\* number", r"a new issue's month 0",
                 r"pols_if\(0\) == pols_if_init", r"then clear the cache")
STALE = re.compile("|".join(STALE_PHRASES))


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
    computed would leave its values as they were.  The three switches are text in
    ``FIA_US_S`` and int codes in SEC at stage ``"EC"`` (:func:`_switch`), so each of S's
    settings goes on SEC as its code, and any other text as it is.
    """
    model = mx.read_model(folder, name=_name(tag))
    for ref, value in (refs or {}).items():
        setattr(model.Projection, ref, _switch(model.Projection, ref, value))
    for ref, value in (data or {}).items():
        setattr(model.Data, ref, value)
    return model


# S's settings of its three string switches, and the code SEC names each by at stage "EC":
# step_up_mode, rb_wd_convention and mva_collar_basis hold S's text in FIA_US_S and an int
# code in FIA_US_SEC, as its timings and kinds do (R9, R10).
SWITCHES = {"step_up_mode": {"annual": "ANNUAL", "at_exercise": "AT_EXERCISE"},
            "rb_wd_convention": {"pro_rata": "PRO_RATA", "dollar": "DOLLAR"},
            "mva_collar_basis": {"gross": "GROSS", "surrender_value": "SURRENDER_VALUE"}}


def _switch(space, ref, value):
    """``value`` for Reference ``ref`` on ``space``: S's setting of a switch as SEC's code.

    On a model whose ``Projection`` names the code, :data:`SWITCHES` maps each of S's
    settings onto it, through :func:`_code`; any other value, a text no decode knows among
    them, goes on as it is, so that it meets S's refusal.  On ``FIA_US_S``, and at stage
    ``"E"``, every value goes on as it is.
    """
    name = SWITCHES.get(ref, {}).get(value) if isinstance(value, str) else None
    code = _code(space, name) if name is not None else value
    return code if isinstance(code, int) else value


def _key(model, point_id):
    """The registry's key for the row labelled ``point_id`` (``us_registry.point_keys``)."""
    return dict(zip(model.Data.model_point_table().index, point_keys(model)))[point_id]


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    return projection(model, _key(model, point_id))


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for the twin of a new-business point, 84 for
    the twin of one S enters at 84, ``d`` for a derived row, ``-k`` for a future one.  The
    twins keep S's ``point_id`` and ``policy_id``, so the S policy is the twin's.
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


def _release(model, key, collect=False):
    """Drop the ItemSpace at ``key``, the registry's key, and every value it has cached.

    The splice's rows and the points of the temporary copies are each needed once, so each
    is released when read, as ``run_sec.py --block`` releases its points
    (USLIB-SEC-PLAN.md F5): held together they would raise this module's memory several
    times over.  Asked for again, the ItemSpace is made afresh and recomputes.  With
    ``collect``, the collector runs at once, as it does for each splice row; the swept
    models the module holds are frozen out of it (:func:`_freeze`), so the collection
    scans only what the row made.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each module fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds.  The collection first means no garbage is frozen with
    them.  The freeze is undone as the module ends (:func:`_collector`), and before the
    splice fixture closes one pair of models to read the other (:class:`_Splices`).
    """
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _companion():
    """The committed scenario companion as the file holds it, on a default index."""
    return pd.read_csv(model_path(SEC).parent / COMPANION)


def _relabeled(table):
    """``table`` relabeled ``100 + point_id`` and written in reverse order.

    Every generated table numbers its points from 1 in table order, so on it no test can
    tell a label from a position; on this one none is the other.
    """
    return table.set_axis(table.index + 100).iloc[::-1]


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder.

    The copy holds the committed scenario companion, which ``edits`` may replace under
    ``COMPANION`` where ``table`` names a scenario the committed one lacks.
    """
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit, tag="edited", refs=None):
    """FIA_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
    return _read(_sec_inputs(tmp_path, edit(_committed())), tag, refs)


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


def _cells(point, **columns):
    """An edit that sets each of ``columns`` at row ``point``."""
    def edit(table):
        for column, value in columns.items():
            table = _set(column, [point], value)(table)
        return table
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
    """The argument or value that stands for timing, kind or phase ``label``.

    The conventions' lookup (``test_model_conventions._timing``), on ``Projection`` or any
    of its ItemSpaces, which see its References: the model's own int Reference named
    ``label`` where it defines one, and the string otherwise.  At stage ``"E"`` the timings
    and kinds are S's strings and the phases already int codes, ``PRE_ISSUE`` 0 to
    ``MATURED`` 5; Phase 2 makes the timings and kinds codes too (R9), and every call below
    reads the same at both stages.
    """
    value = space.refs.get(label)
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _at(space, cell, t, label):
    """``cell(t, label)`` on ``space``, the timing or kind passed through :func:`_code`."""
    return space.cells[cell](t, _code(space, label))


def _mismatches(s_proj, sec_proj, **kwargs):
    """:func:`sec_support.twin_mismatches`, the one place this module calls it.

    It passes the SEC Space's :func:`sec_support.codes`, which map S's strings onto the
    int codes the SEC model names as its References: at stage ``"E"`` the six phases, S's
    ``"ACCUM"`` against SEC's ``ACCUM``, in S's arguments and in S's values; at stage
    ``"EC"`` the timings and kinds too.  Every comparison goes through here, so each takes
    Phase 2's codes when they come.  It passes the spec's ``twin_arg_map`` too, which maps
    S's ``kind=None`` totals onto the code ``ALL`` and S's scenario columns onto their
    codes' names (R9, R12), and passes SEC's own codes through, where SEC is compared with
    SEC; the spec's map runs first, then the caller's ``arg_map``, on S's arguments.
    """
    first = SPEC.twin_arg_map
    arg_map = kwargs.pop("arg_map", None)

    def both(name, args):
        if first is not None:
            args = first(name, args)
        if args is not None and arg_map is not None:
            args = arg_map(name, args)
        return args
    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), arg_map=both,
                           **kwargs)


def _timed(proj, t, timings):
    """Evaluate each cell of :data:`TIMED` at month ``t`` and every timing it has."""
    for name, labels in TIMED.items():
        for label in labels:
            if label in timings:
                proj.cells[name](t, _code(proj, label))


def _sweep_s(proj):
    """Evaluate on an S point what the splice compares: the sweep, and the cells it misses.

    :func:`sec_support.sweep` reaches neither ``wd_cum_pp``, ``av_indexed_pp`` and
    ``claims_over_av``, nor ``bonus_factor``, ``tax_status``, ``activation_rate``,
    ``payout_rate``, ``credit_rate_on``, ``mgsv_rate_statutory`` and
    ``mgsv_rate_is_compliant`` on ``FIA_US_S``, because no result column or check reads
    them, and a cell S never evaluates is compared nowhere (USLIB-SEC-PLAN.md §7.11,
    *never reached*).  Nor does it reach every timing of the timed cells: no report reads
    the fixed or the indexed account at a timing, the account value before the fee, or the
    count before its lapses.  So they are evaluated here, the monthly ones over the frame at
    every timing and kind each has, and the others at arguments of their own: the
    activation incidence either side of each of its ages; the statutory floor rate at CMT
    levels below its floor, between and above its cap, with an option cost under and over
    its gate; the payout percentage at every age from 40 to 120 on both bases, every band
    and both ends of each; and the crediting engine on a loss, a flat year, a gain under
    the cap and one over it, by each of the five methods.
    """
    sweep(proj)
    timings = set(TIMINGS) - {"BEF_NB"}             # S has no BEF_NB, which SEC adds
    for t in range(proj.entry_mth(), proj.proj_len()):
        proj.wd_cum_pp(t)
        proj.av_indexed_pp(t)
        proj.claims_over_av(t)
        for kind in KINDS:
            proj.claims_over_av(t, kind)
        _timed(proj, t, timings | set(AV_TIMINGS) | set(BB_TIMINGS))
    proj.tax_status()
    proj.bonus_factor()
    for a in (55, 60, 72, 73, 74):
        proj.activation_rate(a)
    for args in ((0.0, 0.0), (0.02, 0.0), (0.04, 0.01), (0.08, 0.0), (0.08, 0.02)):
        proj.mgsv_rate_statutory(*args)
        proj.mgsv_rate_is_compliant(*args)
    for basis in ("single", "joint"):
        for a in range(40, 121):
            proj.payout_rate(a, basis)
    for method in ("cap", "par", "par_cap", "spread", "trigger"):
        for r in (-0.1, 0.0, 0.03, 0.1):
            proj.credit_rate_on(r, method)


def _sweep_sec(proj):
    """:func:`_sweep_s` on an SEC row, its monthly cells over the whole frame.

    Every month from ``t = 0``, so a future row's cells are evaluated before its issue too,
    where each holds its guard's value; the timings include ``BEF_NB``.  The cells keyed by
    no month the comparison evaluates at S's own arguments.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        proj.wd_cum_pp(t)
        proj.av_indexed_pp(t)
        proj.claims_over_av(t, _code(proj, "ALL"))
        for kind in KINDS:
            proj.claims_over_av(t, _code(proj, kind))
        _timed(proj, t, set(TIMINGS) | set(AV_TIMINGS) | set(BB_TIMINGS))
    proj.tax_status()
    proj.bonus_factor()


def _on_the_books(d):
    """T2's ``arg_map`` for a row opened at S month ``d``: the anniversaries it reads.

    S reads its scenario by anniversary number from issue, at every anniversary of its
    frame, and the year's opening index level at the anniversary that opened the year.  A
    row opened at ``d`` reads none of those before ``d``: an anniversary that fell before
    its first month is history, and the level at the one that opened the year under way is
    the row's ``index_level_prev_anniv_init``.  So S's ``scenario_value`` and
    ``mva_ref_yield`` at an anniversary ``y`` with ``12 y < d`` are skipped, and
    ``index_level`` at a ``y`` before ``d // 12``, the year under way; every later
    anniversary's month falls on the books (R1a).  Every other key passes unchanged, its
    ``t`` moved by the comparison itself.
    """
    def arg_map(name, args):
        if name in ("scenario_value", "mva_ref_yield") and 12 * args[0] < d:
            return None
        if name == "index_level" and args[0] < d // 12:
            return None
        return args
    return arg_map


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on, in two passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_pols``, SEC row ``t`` against S row ``t + month``, frames ending together;
    then every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every argument S cached
    inside its frame from ``month`` on, moved onto SEC's clock, the anniversaries before
    the books skipped (:func:`_on_the_books`).  Both to 1e-9 relative with no absolute
    floor: a count late in a long frame, or under the last policy year's certain death,
    falls far below 1e-7, where a floor of 1e-9 would hide any error.  Then the cells of
    :data:`RESIDUALS` alone, at the floor of 1e-9: their exact value is 0, and the computed
    one is rounding of what they close (§5.2, precised at M11), as the indexed account's
    would be on a contract wholly in the fixed account, which no row of the grid is.
    Returns the mismatch lines, empty when the row is S's.
    """
    found = []
    for report, keep in (("result_cf", columns), ("result_pols", None)):
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=keep, atol=0.0)]
    books = _on_the_books(month)
    found += _mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                         arg_map=books, atol=0.0)
    found += _mismatches(s_proj, sec_proj, t_offset=month, arg_map=books,
                         exempt=(set(s_proj.cells) - RESIDUALS) | exempt)
    return found


def _continues_s(s_proj, sec_proj, month, exempt=SPLICE_EXEMPT):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions, skipping ``exempt``, T2's exemptions or, on the row issued later, T3's
    (:data:`FUTURE_EXEMPT`).  The shipped 2.5% expense inflation runs from issue in S and
    from the valuation date here (D7), so :data:`INFLATED`'s two columns, and
    :data:`INFLATION_CELLS`, differ by design and are left out; the inflation test holds
    them.  The committed companion re-bases each row's scenario to its month, so nothing
    else moves with the clock, and every other column and cell must agree.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, exempt | INFLATION_CELLS, keep)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d60``, ``point1-twin84``, or ``point2-k15`` if issued later."""
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
# default run's among them; and the switched References' likewise.
GRID = (*IN_FORCE_TWINS, *SPLICES, *(("future", p, -k) for p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k) for p, k in CORE_FUTURES)})
GRIDS = {"spliced": (GRID, CORE_GRID),
         "switched": (SWITCHED_GRID, frozenset(SWITCHED_CORE))}


def _s_table_with(variants):
    """S's committed table with ``variants`` appended, under their own point_ids."""
    table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                        index_col="point_id")
    rows = []
    for point_id, (base, changes) in variants.items():
        row = table.loc[[base]].assign(**changes)
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    return pd.concat([table, *rows])


def _moved_opening_levels(table, companion):
    """``companion`` with each mid-year row's year-opening index level moved off ``t = 0``.

    The generator step-fills each re-based copy from S's anniversary levels, so on a row
    valued mid-year in force its scenario's level at ``t = 0`` is the level of the
    anniversary that opened the year under way, which the row also carries, as
    ``index_level_prev_anniv_init``: a model that read the scenario there instead of the
    column would give S's numbers all the same.  So in each such row's copy the level its
    next anniversary reads is first written at that anniversary's month, where the copy
    has no row there, and the level at ``t = 0`` is then moved off it, by a quarter.  A
    correct model never reads that level mid-year: the next anniversary's comes from its
    own row, and the year's opening one from the column.  ``Data`` holds the level at
    ``t = 0`` to the column on an anniversary only, and a row valued on one keeps its copy
    as generated.
    """
    out = companion.copy()
    mid = table[(table["duration_mth"] > 0) & (table["duration_mth"] % 12 != 0)]
    extra = []
    for sid, d in dict.fromkeys(zip(mid["scenario_id"], mid["duration_mth"])):
        mine = out["scenario_id"] == sid
        first = out.index[mine & (out["t"] == 0)][0]
        next_mth = 12 * (int(d) // 12 + 1) - int(d)
        if not (mine & (out["t"] == next_mth)).any():
            extra.append({**out.loc[first].to_dict(), "t": next_mth})
        out.loc[first, "index_level"] = 1.25 * out.at[first, "index_level"]
    return pd.concat([out, pd.DataFrame(extra, columns=out.columns)], ignore_index=True)


def _splice_pair(root, which):
    """S and SEC on the splice's inputs under ``which``'s References: ``(s, sec)``.

    S is read from a copy of the product directory whose table has the variants appended,
    :data:`SWITCHED_VARIANTS` too under the switched References, and whose scenarios,
    withdrawal programmes and mortality are the splice's (:data:`SPLICED_EDITS`).  SEC runs
    on the same tables, and on a model point table of its own, built by the generator from
    the registered spec with its rows replaced by the cases this run selects, the core or
    the full grid (:func:`_selected`), out of this S model, so that each row opens with the
    state of the very run it is compared with; and on the scenario companion the generator
    builds from it, which re-bases the stepped scenarios to each row's month under an id
    of its own, each mid-year row's level at ``t = 0`` then moved off the column it carries
    (:func:`_moved_opening_levels`).  Both read ``which``'s References before either
    computes anything.
    """
    variants = {**VARIANTS, **(SWITCHED_VARIANTS if which == "switched" else {})}
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with(variants), edits=SPLICED_EDITS)
    s = _read(s_folder, f"s_{which}", REFS[which])
    grid, core = GRIDS[which]
    cases = _selected(grid, core)
    spec = dataclasses.replace(
        SPEC, derived=tuple((p, d) for kind, p, d in cases if kind == "derived"),
        future=tuple((p, -d) for kind, p, d in cases if kind == "future"))
    table, companions = build_sec_table(spec, s)
    assert set(companions) == {COMPANION}
    companion = _moved_opening_levels(table, companions[COMPANION])
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file,
                             edits={**SEC_EDITS, COMPANION: companion})
    return s, _read(sec_folder, f"sec_{which}", REFS[which])


class _Splices:
    """The splice's two pairs of models, the shipped References' and the switched ones'.

    One pair is held at a time: :meth:`pair` reads the pair asked for, closing the other
    first, so that the module never holds both, each with its swept S points, beside the
    committed models.  The tests that read a pair run together in the module's order, so
    each pair is read once a run.  Each S point is swept the first time a case asks for it
    (:meth:`s_point`) and stays swept while its pair is held.
    """

    def __init__(self, root):
        self.root, self.which, self.s, self.sec, self.swept = root, None, None, None, set()

    def pair(self, which):
        """``(s, sec)`` under ``which``'s References, read now if not already held."""
        if which != self.which:
            self.close()
            self.s, self.sec = _splice_pair(self.root / which, which)
            self.which = which
            _freeze()
        return self.s, self.sec

    def s_point(self, which, point_id):
        """S point ``point_id`` of ``which``'s pair, swept (:func:`_sweep_s`)."""
        s, _ = self.pair(which)
        proj = _point(s, point_id)
        if point_id not in self.swept:
            _sweep_s(proj)
            self.swept.add(point_id)
        return proj

    def close(self):
        """Close the pair held, if any, and collect it.

        Its models are frozen out of the collector with everything else alive, and a frozen
        cycle is never collected, so the freeze is undone first; the next pair's read
        freezes what is then alive.
        """
        if self.which is None:
            return
        gc.unfreeze()
        self.sec.close()
        self.s.close()
        self.which, self.s, self.sec, self.swept = None, None, None, set()
        gc.collect()


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
    """FIA_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(400)`` on the twin of S point 2, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  Last, the opening-state columns the sweep did not read are kept, point by
    point, before any test reads one.  So the record says what a cold model does, which
    the clock test and the tests of where each column is read assert (D3, R2), and every
    test on the committed model reads a model already swept: the sweep is paid once, not
    once for each.  The swept model is then frozen out of the collector (:func:`_freeze`).
    Returns ``(model, record)``.
    """
    model = _read(model_path(SEC), "sec")
    first = _row(model, "twin", 2, 0)
    record = {"duration_mth(400)": first.duration_mth(400),
              "keys": list(first.cells["duration_mth"].keys()), "deep": [], "unread": {}}
    labels = model.Data.model_point_table().index
    limit = mx.get_recursion()
    mx.set_recursion(CALL_DEPTH)
    try:
        for key, point_id in zip(point_keys(model), labels):
            try:
                sweep(projection(model, key))
            except Exception as err:            # kept, so every point is swept
                record["deep"].append(f"point {point_id}: the sweep raised {_raised(err)}")
    finally:
        mx.set_recursion(limit)
    for key, point_id in zip(point_keys(model), labels):
        p = projection(model, key)
        record["unread"][point_id] = {c for c in STATE if not len(p.cells[c].keys())}
    _freeze()
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """FIA_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """FIA_US_S read in place, as committed, with every point swept (:func:`_sweep_s`).

    T6 regenerates the SEC files from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it, the cells its own sweep misses among them.  The swept model is then frozen out
    of the collector (:func:`_freeze`).
    """
    model = _read(model_path(TWIN), "s")
    for key in point_keys(model):
        _sweep_s(projection(model, key))
    _freeze()
    yield model
    model.close()


@pytest.fixture(scope="module")
def splices(tmp_path_factory):
    """The splice's pairs of models, one held at a time (:class:`_Splices`)."""
    held = _Splices(tmp_path_factory.mktemp("spliced"))
    yield held
    held.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do, by ``(which, case)`` (:func:`_record`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case sweeps its row, records what the rules test and the core grid's reach
# need of it, compares it with S, and releases it: held together, the rows of the full grid
# would hold gigabytes.  The record is made before the comparison, because the comparison
# evaluates SEC's cells at S's own cached arguments, keys SEC never asks for itself among
# them, and the rules test judges what the model asks for.  So each of the two tests reads
# the records, and computes any case no earlier test has recorded, which keeps it whole
# when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _month_reads(proj, node, memo):
    """The calls keyed by a month that ``node``, a call keyed by none, makes or has made.

    ``node`` is a call of a cell of ``proj`` with no ``t``: one keyed by an anniversary, a
    contract year, an age or a count of completed years, or by nothing.  Its precedents
    keyed by ``t`` are its own reads, and through each precedent of ``proj``'s keyed by no
    month, that precedent's, down every path to the first call keyed by ``t``, so that the
    reads are judged against the month that asked.  ``memo`` holds each call's reads, once,
    by cells and arguments.
    """
    key = (node.obj.name, node.args)
    if key not in memo:
        memo[key] = []                      # a call met again on its own path adds nothing
        found = []
        for pred in node.obj.preds(*node.args):
            if pred.obj.parent is not proj:
                continue
            if "t" in (pred.obj.parameters or ()):
                found.append(pred)
            else:
                found += _month_reads(proj, pred, memo)
        memo[key] = found
    return memo[key]


# R2's one admitted read (USLIB-SEC-PLAN.md D11, precised at M2): lapse_rate(t) reads the
# phase opening and closing the anniversary that ends the contract year, and
# lapse_moneyness_factor(t) the account value and the benefit base there, at anniv_mth(t),
# up to 11 months ahead.  Admitted by reader and cell, at that month alone and inside the
# frame, and only where the state read depends on no cell of FORBIDDEN, the counts and the
# decrements, the reader itself among them, and on no month after that anniversary.
LOOK_AHEAD = frozenset({("lapse_rate", "phase_open"), ("lapse_rate", "phase"),
                        ("lapse_moneyness_factor", "av_pp"),
                        ("lapse_moneyness_factor", "benefit_base_pp")})
FORBIDDEN = frozenset({"pols_if", "pols_if_at", "pols_new_biz", "pols_death", "pols_lapse",
                       "pols_maturity", "pols_decr", "lapse_rate", "lapse_rate_mth",
                       "lapse_moneyness_factor", "mort_rate", "mort_rate_mth",
                       "policy_count", "pols_if_init"})


def _closing(proj, t, u):
    """Whether month ``u`` is the anniversary closing the contract year of ``t``, ahead of
    it and inside the frame."""
    return (u == proj.anniv_mth(t) and t < u <= t + 11
            and proj.duration_mth(u) % 12 == 11 and u < proj.proj_len())


def _closure(proj, node, memo):
    """What ``node``'s value rests on: ``(latest month, FORBIDDEN cells)`` over its
    precedents.

    The latest ``t`` of any call of ``proj``'s that ``node`` reaches through its
    precedents, itself included, and the names of :data:`FORBIDDEN` among them, walked
    down modelx's dependency graph without recursion, so that a chain as long as the frame
    walks too.  ``memo`` holds each call's answer once, by cells and arguments, so the
    thousands of reads a row admits share the walk.
    """
    stack = [node]
    preds = {}
    while stack:
        n = stack[-1]
        key = (n.obj.name, n.args)
        if key in memo:
            stack.pop()
            continue
        if key not in preds:
            preds[key] = [p for p in n.obj.preds(*n.args) if p.obj.parent is proj]
            todo = [p for p in preds[key] if (p.obj.name, p.args) not in memo]
            if todo:
                stack.extend(todo)
                continue
        params = n.obj.parameters or ()
        latest = (n.args[params.index("t")] if "t" in params
                  and _month(n.args[params.index("t")]) else -1)
        reached = {n.obj.name} & FORBIDDEN
        for p in preds.pop(key):
            their_latest, theirs = memo[(p.obj.name, p.args)]
            latest, reached = max(latest, their_latest), reached | theirs
        memo[key] = (latest, frozenset(reached))
        stack.pop()
    return memo[(node.obj.name, node.args)]


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has been swept.

    ``{"negative", "early", "ahead", "condition", "year", "admitted"}``: every cached call
    with a negative argument, a month, an anniversary, a contract year, a count of years or
    an age; every read keyed by a month before ``t_entry()`` of a call keyed by a month at
    or after it; every read keyed by a month beyond ``t + 1`` of a call keyed by ``t``,
    but R2's admitted read (:data:`LOOK_AHEAD`) at the closing anniversary inside the
    frame; every admitted read whose state rests on a count, a decrement or a month after
    the anniversary (:func:`_closure`); every index level read at an anniversary before
    the contract year under way at ``t_entry()``, and every scenario level or reference
    yield read at an anniversary whose month precedes ``t_entry()``; and how many reads
    were admitted.  A read is a precedent of the call's, as modelx's dependency graph
    records it, keyed by a month, or one a precedent keyed by no month makes on the call's
    behalf (:func:`_month_reads`).
    """
    entry, d0 = proj.t_entry(), proj.duration_mth_init()
    negative, early, ahead, condition, year = [], [], [], [], []
    admitted = 0
    memo, closures = {}, {}
    for name, cells in proj.cells.items():
        t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if t_pos is None:
                continue
            t = args[t_pos]
            for pred in cells.preds(*args):
                params = getattr(pred.obj, "parameters", None) or ()
                if "t" in params:
                    reads, via = [pred], ""
                elif pred.obj.parent is proj:
                    reads = _month_reads(proj, pred, memo)
                    via = f"{pred.obj.name}{pred.args} -> "
                else:
                    continue
                for node in reads:
                    u = node.args[node.obj.parameters.index("t")]
                    if not _month(u):
                        continue
                    if u < entry <= t:
                        early.append(f"{name}{args} -> {via}{node.obj.name}{node.args}")
                    if u <= t + 1:
                        continue
                    if (name, node.obj.name) in LOOK_AHEAD and _closing(proj, t, u):
                        admitted += 1
                        latest, counts = _closure(proj, node, closures)
                        if latest > u or counts:
                            condition.append(f"{name}{args} -> {node.obj.name}{node.args}: "
                                             f"rests on month {latest}, {sorted(counts)}")
                        continue
                    ahead.append(f"{name}{args} -> {via}{node.obj.name}{node.args}")
    first = proj.duration(entry)
    for name in ("index_level", "scenario_value", "mva_ref_yield"):
        for args in _cached_args(proj.cells[name]):
            y = args[0]
            if y < first or (name != "index_level" and 12 * y - d0 < entry):
                year.append(f"{name}{args}")
    return {"negative": negative, "early": early, "ahead": ahead, "condition": condition,
            "year": year, "admitted": admitted}


def _credit(decode):
    """Whether a row credits the index by the method ``decode`` decodes, in month t."""
    return lambda x, t: (x.is_anniv(t) and x.cells[decode]()
                         and x.index_credit_pp(t) > 0.0)


def _phase_is(x, t, *labels, cell="phase"):
    """Whether phase cell ``cell`` holds one of ``labels`` in month ``t``, as codes."""
    return x.cells[cell](t) in [_code(x, label) for label in labels]


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column is in use,
# each phase is the year's opening phase, and the year under way is read in each of its
# states: on an anniversary, mid-year, in its last month, in the first policy year, in the
# exercise year, with the index level read from the row, the fixed account accrued since
# the anniversary, and the last covered month; a locked rate that the band at the
# valuation date's exercise age would not give, and a year-opening index level that the
# row's scenario does not hold at t = 0 (_splice_pair moves it), so that a model reading
# either afresh fails T2.  Later in the frame, every phase transition,
# each crediting method, the floor and the cap, the step-up, the rollup and the stack, the
# withdrawals and their charges, the guarantee's reduction, each shock lapse and the
# moneyness factor, the floor on a surrender, a maturity, and each assumption the splice
# switches on, on the shipped References.
AT_VALUATION = {
    **{f"{c} non-zero": (lambda x, c=c: x.cells[c]() != 0.0)
       for c in STATE if c != "phase_prev_anniv_init"},
    **{f"phase {label} at the anniversary": (
        lambda x, label=label: x.phase_prev_anniv_init() == _code(x, label))
       for label in ("ACCUM", "INCOME", "DEPLETED")},
    "an anniversary valuation": lambda x: x.duration_mth_init() % 12 == 0,
    "a mid-year valuation": lambda x: x.duration_mth_init() % 12 not in (0, 11),
    "a year's last month": lambda x: x.duration_mth_init() % 12 == 11,
    "the first policy year": lambda x: 0 < x.duration_mth_init() < 12,
    "the exercise year under way": lambda x: (
        x.phase_prev_anniv_init() == _code(x, "ACCUM") and x.is_exercise(0)),
    "the index level read from the row": lambda x: (
        x.duration_mth_init() % 12 != 0 and x.index_credit_pp(x.anniv_mth(0)) > 0.0),
    "the fixed account accrued since the anniversary": lambda x: (
        x.av_fixed_pp_init() > x.av_fixed_pp_prev_anniv_init()),
    "the last covered month": lambda x: x.proj_len() == 1,
    "a locked rate apart from the band at the exercise age": lambda x: (
        x.phase_prev_anniv_init() in [_code(x, "INCOME"), _code(x, "DEPLETED")]
        and x.payout_rate_locked_prev_anniv_init() != x.payout_rate_at(x.exercise_age(0))),
    "the year's opening index level apart from the scenario's at t = 0": lambda x: (
        x.duration_mth_init() % 12 != 0
        and x.index_level_prev_anniv_init() != float(x.data.rate_scenario_steps().loc[
            (x.model_point()["scenario_id"], 0), "index_level"])),
}

IN_FRAME = {
    "ACCUM to INCOME": lambda x, t: x.is_anniv(t) and x.is_exercise(t),
    "INCOME to DEPLETED": lambda x, t: (
        _phase_is(x, t, "DEPLETED") and _phase_is(x, t, "INCOME", cell="phase_open")),
    "INCOME to TERMINATED": lambda x, t: (
        _phase_is(x, t, "TERMINATED") and _phase_is(x, t, "INCOME", cell="phase_open")),
    "ACCUM to TERMINATED": lambda x, t: (
        _phase_is(x, t, "TERMINATED") and _phase_is(x, t, "ACCUM", cell="phase_open")),
    "income after depletion": lambda x, t: x.income_payments(t) > 0.0,
    **{f"a {method} credit": _credit(f"is_credit_{method}")
       for method in ("cap", "par", "par_cap", "spread", "trigger")},
    "the credit floor binding": lambda x, t: (
        x.is_anniv(t) and x.index_return(t) < 0.0 and x.credit_rate(t) == 0.0
        and _phase_is(x, t, "ACCUM", "INCOME", cell="phase_open")),
    "the cap binding": lambda x, t: (
        x.is_anniv(t) and (x.is_credit_cap() or x.is_credit_par_cap())
        and x.index_return(t) > 0.0 and x.credit_rate(t) == x.cap_rate_in_force()),
    "the step-up binding": lambda x, t: (
        x.step_up_applies(t) and _at(x, "benefit_base_pp_at", t, "BEF_WD")
        > _at(x, "benefit_base_pp_at", t, "BEF_STEP_UP")),
    "a rollup credit": lambda x, t: x.rollup_pp(t) > 0.0,
    "a stack credit on fixed interest": lambda x, t: (
        x.stack_pp(t) > 0.0 and x.fixed_interest_ann_pp(t) > 0.0),
    "out of the growth window in ACCUM": lambda x, t: (
        x.is_anniv(t) and x.phase_year_open(t) == _code(x, "ACCUM") and x.glwb_elected()
        and x.policy_year(t) > x.growth_period_max),
    "the LW ratchet": lambda x, t: (
        x.is_anniv(t) and _phase_is(x, t, "INCOME", cell="phase_open")
        and not x.is_exercise(t) and x.year_open_mth(t) >= x.t_entry()
        and _at(x, "lw_pp_at", t, "BEF_WD") > x.lw_pp(x.year_open_mth(t))),
    "an excess withdrawal in INCOME": lambda x, t: (
        _phase_is(x, t, "INCOME", cell="phase_open") and x.wd_excess_pp(t) > 0.0),
    "a withdrawal before exercise": lambda x, t: (
        _phase_is(x, t, "ACCUM", cell="phase_open") and x.wd_pp(t) > 0.0),
    "a surrender charge on a withdrawal": lambda x, t: x.wd_charge_pp(t) > 0.0,
    "a clawback on a withdrawal": lambda x, t: x.wd_clawback_pp(t) > 0.0,
    "a negative MVA on a withdrawal": lambda x, t: x.wd_mva_pp(t) < 0.0,
    "the collar holding a withdrawal's MVA": lambda x, t: (
        x.wd_charge_base_pp(t) > 0.0 and x.mva_rate(t) != 0.0
        and x.wd_mva_pp(t) != x.mva_rate(t) * x.wd_charge_base_pp(t)),
    "the guarantee reduced to 0": lambda x, t: x.wd_reduction_rate(t) == 1.0,
    "the guarantee reduced in part": lambda x, t: 0.0 < x.wd_reduction_rate(t) < 1.0,
    "an unfunded withdrawal": lambda x, t: x.wd_unfunded_pp(t) > 0.0,
    "the no-rider shock": lambda x, t: (
        x.policy_year(t) == x.surr_charge_period + 1 and not x.glwb_elected()
        and 0.0 < x.lapse_rate(t) < 1.0),
    "the idle-rider shock": lambda x, t: (
        x.policy_year(t) == x.surr_charge_period + 1 and x.glwb_elected()
        and _phase_is(x, t, "ACCUM", cell="phase_open") and 0.0 < x.lapse_rate(t) < 1.0),
    "the active-rider shock": lambda x, t: (
        x.policy_year(t) == x.surr_charge_period + 1
        and _phase_is(x, t, "INCOME", cell="phase_open") and 0.0 < x.lapse_rate(t) < 1.0),
    "the moneyness floor": lambda x, t: (
        0.0 < x.lapse_rate(t) < 1.0
        and x.lapse_moneyness_factor(t) == x.lapse_money_floor),
    "the moneyness factor below 1": lambda x, t: (
        x.lapse_rate(t) > 0.0 and x.lapse_money_floor < x.lapse_moneyness_factor(t) < 1.0),
    "the floor binding on a surrender": lambda x, t: (
        x.surr_benefit_pp(t) > x.surr_value_pp(t) and x.av_pp(t) > 0.0),
    "a maturity": lambda x, t: x.pols_maturity(t) > 0.0,
    "the floor's charge and the rider charge on it": lambda x, t: (
        x.mgsv_charge_pp(t) > 0.0 and x.rider_charge_pp(t) > 0.0 and x.mgsv_pp(t) > 0.0),
    "premium tax and commission": lambda x, t: (
        x.premium_taxes(t) > 0.0 and x.commissions(t) > 0.0),
    "the female table": lambda x, t: x.sex() == "F" and x.pols_death(t) > 0.0,
    "the joint basis": lambda x, t: (
        x.is_joint_basis() and x.is_anniv(t) and x.is_exercise(t)),
    "the 80+ band": lambda x, t: (
        x.is_anniv(t) and x.is_exercise(t) and x.exercise_age(t) >= 80),
    "the simple rollup": lambda x, t: x.rollup_id() == "simple" and x.rollup_pp(t) > 0.0,
    "the step-down to 2%": lambda x, t: x.rollup_rate(t) == 0.02 and x.rollup_pp(t) > 0.0,
}

# What the switched References' core must reach in the frame: each switch at its other
# setting doing what only it does, and each cap and floor binding with an effect.
SWITCHED_FRAME = {
    "the step-up at exercise binding": lambda x, t: (
        x.is_step_up_at_exercise() and x.is_anniv(t) and x.is_exercise(t)
        and _at(x, "benefit_base_pp_at", t, "BEF_WD")
        > _at(x, "benefit_base_pp_at", t, "BEF_STEP_UP")),
    "no step-up before exercise, where the annual one would bind": lambda x, t: (
        x.is_step_up_at_exercise() and x.is_anniv(t) and not x.step_up_applies(t)
        and _phase_is(x, t, "ACCUM", cell="phase_open")
        and _at(x, "av_pp_at", t, "BEF_WD")
        > _at(x, "benefit_base_pp_at", t, "BEF_STEP_UP")),
    "the rollup base reduced dollar for dollar": lambda x, t: (
        x.is_rb_dollar() and x.wd_pp(t) > 0.0
        and 0.0 < x.rollup_base_pp(t) < x.rollup_base_pp_year_open(t)),
    "the surrender-value collar holding an MVA": lambda x, t: (
        x.is_collar_surrender_value() and x.mva_rate(t) != 0.0
        and x.mva_pp(t) != x.mva_rate(t) * x.surr_charge_base_pp(t)),
    "the lapse cap binding": lambda x, t: x.lapse_rate(t) == x.lapse_rate_max,
    "the rider charge's cap binding": lambda x, t: (
        x.rider_charge_pp(t) > 0.0 and x.rider_charge_rate > x.rider_charge_rate_max
        and x.rider_charge_pp(t)
        == x.rider_charge_rate_max * _at(x, "benefit_base_pp_at", t, "BEF_ROLLUP")),
    "the fixed rate's floor": lambda x, t: (
        x.fixed_interest_pp(t) > 0.0 and x.fixed_rate < x.fixed_rate_min
        and x.fixed_rate_in_force() == x.fixed_rate_min),
    "the cap's floor binding apart from the credit floor": lambda x, t: (
        x.is_anniv(t) and x.cap_rate() < x.cap_rate_min
        and x.credit_rate(t) == x.cap_rate_min > x.floor_rate),
    "the raised credit floor binding": lambda x, t: (
        x.is_anniv(t) and x.index_return(t) < 0.0
        and x.credit_rate(t) == x.floor_rate > 0.0
        and _phase_is(x, t, "ACCUM", "INCOME", cell="phase_open")),
    "the trigger's floor": lambda x, t: (
        x.is_credit_trigger() and x.is_anniv(t)
        and x.index_return(t) - x.index_cost_rate < 0.0
        and x.credit_rate(t) == x.floor_rate > 0.0),
    "a trigger credit at a zero net return": lambda x, t: (
        x.is_credit_trigger() and x.is_anniv(t)
        and x.index_return(t) - x.index_cost_rate == 0.0
        and x.credit_rate(t) == x.trigger_rate),
    "the minimum exercise age binding": lambda x, t: (
        x.is_anniv(t) and x.is_exercise(t)
        and x.exercise_age(t) == x.min_income_age > x.income_start_age()),
}
REACH = {"spliced": (AT_VALUATION, IN_FRAME), "switched": ({}, SWITCHED_FRAME)}


def _branches(x, kind, which):
    """The names in ``which``'s reach dicts (:data:`REACH`) that hold of row ``x``.

    The dict of the valuation date asks about the state at the valuation date, which only
    a row in force holds; the frame's about the frame, which a future row has too, and
    which alone has the premium tax and the commission of new business.
    """
    at, frame = REACH[which]
    reached = set() if kind == "future" else {what for what, holds in at.items()
                                              if holds(x)}
    return reached | {what for what, holds in frame.items()
                      if any(holds(x, t) for t in range(x.t_entry(), x.proj_len()))}


def _record(which, case, proj):
    """Sweep the splice row ``proj`` of ``case`` and record what the rules test needs of it.

    :func:`_rule_breaches`'s record, with the row's :func:`_branches`.  A row that raises is
    recorded as raising, which the rules test reports.
    """
    try:
        _sweep_sec(proj)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj, case[0], which)
        record["raised"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "condition": [], "year": [],
                  "admitted": 0, "branches": set(), "raised": _raised(err)}
    return record


def _record_of(splices, records, which, case):
    """The record of ``case``, from the case that compared its row or, failing it, now."""
    if (which, case) not in records:
        _, sec = splices.pair(which)
        key = _row_key(sec, *case)
        try:
            records[which, case] = _record(which, case, projection(sec, key))
        finally:
            _release(sec, key, collect=True)
    return records[which, case]


def _future_facts(proj, k):
    """What a row issued ``k`` months on holds before issue, and what it reads (R1, D4).

    The pre-issue rows of the four reports with a row a month are present, and zeros, the
    phase ``PRE_ISSUE``; the contracts arrive in month ``k`` as new business; every
    decrement rate is the float 0.0 before issue, where ``result_pols`` reports it; and no
    reader keyed by an age, a contract year, a count of completed years or an anniversary
    number has been read below the contract's first, so no rate read its table there.
    Returns the faults found.
    """
    faults = []
    for report in REPORTS[:4]:
        frame = proj.cells[report]()
        if list(frame.index[:k]) != list(range(k)):
            faults.append(f"{report}: no row for each month before issue")
        numeric = frame.loc[:k - 1].select_dtypes("number")
        if not (numeric == 0.0).all().all():
            faults.append(f"{report}: a number before issue")
    labels = set(proj.result_glwb()["phase"].iloc[:k])
    if labels != {"PRE_ISSUE"}:
        faults.append(f"result_glwb: the phase before issue is {sorted(labels)}")
    if not proj.pols_new_biz(k) == proj.policy_count() == 1.0:
        faults.append(f"new business at k: {proj.pols_new_biz(k)}")
    for name in DECREMENT_RATES:
        early = [(t, proj.cells[name](t)) for t in range(k)]
        if any((type(rate), rate) != (float, 0.0) for _, rate in early):
            faults.append(f"{name} before issue: {early[:5]}")
    youngest = min(proj.age_at_entry(), proj.joint_age())
    floors = {"mort_rate_base_at": proj.age_at_entry(), "payout_rate_at": youngest + 1,
              **{name: 1 for name in YEAR_READERS}, **{name: 0 for name in ANNIV_READERS}}
    for name, lowest in floors.items():
        low = [args for args in _cached_args(proj.cells[name]) if args[0] < lowest]
        if low:
            faults.append(f"{name} read below {lowest}: {low[:5]}")
    return faults


# ---------------------------------------------------------------------------
# The every-state test (T5)
#
# Every state FIA_US_S reaches, restated in force by the generator, must be an opening
# state Data and proj_len() accept, but a state the product refuses by name, which is set
# aside and shown refused (USLIB-SEC-PLAN.md §5.2, T5, precised at M10 and M9).  The test
# runs under each set of inputs on which the states S reaches differ, and names them: the
# splice's References and the switched ones, each on its pair, beside the splice's tests,
# and S's shipped References and inputs, on the committed S, in the T5 section.

TERMINATED = _FIA_PHASE_CODES["TERMINATED"]


def _every_state_months(sp):
    """The months S point ``sp`` is restated at by the every-state test, after S's entry.

    By default the edges of the windows ``Data`` and ``proj_len()`` hold a state over:
    every month of the first policy year, where the first year's rules hold, each
    anniversary, where the anniversary's exact rules hold, and the month before it, where
    the rules off an anniversary hold last, and the last month of its frame, where
    ``proj_len()``'s window ends.  With ``USLIB_SEC_FULL=1``, every month.
    """
    entry, n = sp.entry_mth(), sp.proj_len()
    if SEC_FULL:
        return list(range(entry + 1, n))
    months = {*range(1, 12), n - 1}
    months |= {12 * y + k for y in range(1, n // 12 + 1) for k in (-1, 0)}
    return sorted(m for m in months if entry < m < n)


def _states_s_reaches(s):
    """The states ``s``'s points reach, as ``(S point, month)``: ``(kept, terminated)``.

    Each month of :func:`_every_state_months` of each point of ``s``.  ``terminated``
    holds the months that open in ``TERMINATED``, the phase at the anniversary on or
    before the month read as the generator reads it, the one state the product refuses by
    name: ``FIA_US_S`` keeps a contract on its frame once a withdrawal or an anniversary has
    terminated it, every contract surrendered, and none is in force in that phase (D6).
    ``kept`` holds every other.
    """
    phase = SPEC.state["phase_prev_anniv_init"]
    kept, terminated = [], []
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        sp = projection(s, key)
        for d in _every_state_months(sp):
            (terminated if phase(sp, d) == TERMINATED else kept).append((point_id, d))
    return kept, terminated


def _restated(s, states):
    """The generator's table of ``s``'s twins and a derived row at each of ``states``.

    Built out of ``s`` as it stands, so each row opens with the state of the very run ``s``
    made, on its scenario re-based to its month.  Returns ``(table, companion)``.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=())
    table, companions = build_sec_table(spec, s)
    return table, companions[COMPANION]


def _read_restated(root, table, companion, refs, edits=None):
    """The model of ``table`` and ``companion``, beside ``edits``, ``refs`` set first."""
    return _read(temp_inputs(root, model_path(SEC), model_points=table,
                             model_point_file=TABLE,
                             edits={**(edits or {}), COMPANION: companion}), "every", refs)


def _refused_in_force(s, states, root, refs, edits=None):
    """What ``Data`` and ``proj_len()`` refuse of ``states`` of ``s``, restated in force.

    ``Data`` reads the table of :func:`_restated`, and then every row is asked for its
    frame and released, the collector run every 500.  Then ``Data`` reads the table again
    with every amount of money carried to the cent (:data:`MONEY`), as an extract carries
    it, which each rule between amounts allows for (§5.2, T5, precised at M10).  Returns
    each refusal, the line naming it, ``Data``'s or each row's ``proj_len()``'s.  S has
    computed every state once the table is built, so it is frozen out of the collector
    then (:func:`_freeze`), and the collections the released rows trigger scan the rows
    alone.
    """
    table, companion = _restated(s, states)
    _freeze()
    refused = []
    model = _read_restated(root / "exact", table, companion, refs, edits)
    try:
        try:
            read = model.Data.model_point_table()
        except Exception as err:                # reported, with the rows' states
            return [f"Data: {_raised(err)}"]
        assert len(read) == len(table) == len(s.Data.model_point_table()) + len(states)
        for i, key in enumerate(point_keys(model)):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused.append(_raised(err))
            _release(model, key, collect=i % 500 == 499)
    finally:
        model.close()
    cents = table.assign(**{column: table[column].round(2) for column in MONEY})
    model = _read_restated(root / "cents", cents, companion, refs, edits)
    try:
        model.Data.model_point_table()
    except Exception as err:                    # reported, beside the exact table's
        refused.append(f"Data, carried to the cent: {_raised(err)}")
    finally:
        model.close()
    return refused


def _refused_by_name(s, state, root, refs, edits=None):
    """``Data`` refuses ``state`` of ``s``, a contract terminated, restated, by name.

    The message, matched whole, names the row and says why no contract is in force in
    ``TERMINATED``.
    """
    table, companion = _restated(s, [state])
    model = _read_restated(root, table, companion, refs, edits)
    try:
        with pytest.raises(Exception) as excinfo:
            model.Data.model_point_table()
        point = _label(table.set_index("point_id"), "derived", *state)
        assert _raised(excinfo.value) == "ValueError: " + _says(
            _IN_FORCE_PHASE, [point]).format(file=TABLE)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T2 -- the splice


def _splice_case(splices, records, which, case):
    """Record, compare and release the row of ``case`` in ``which``'s pair (T2, T3).

    Returns the mismatches with S, then, on a row issued later, :func:`_future_facts`'s.
    """
    kind, s_point, month = case
    _, sec = splices.pair(which)
    key = _row_key(sec, *case)
    try:
        proj = projection(sec, key)
        records[which, case] = _record(which, case, proj)
        exempt = FUTURE_EXEMPT if kind == "future" else SPLICE_EXEMPT
        found = _compare(splices.s_point(which, s_point), proj, month, exempt)
        if kind == "future":
            found += _future_facts(proj, -month)
        return found
    finally:
        _release(sec, key, collect=True)


@pytest.mark.parametrize(
    "kind, s_point, month",
    [_case(case, CORE_SPLICES, _case_id(*case)) for case in (*IN_FORCE_TWINS, *SPLICES)])
def test_an_in_force_point_continues_its_s_projection(splices, splice_records, kind,
                                                      s_point, month):
    """Opened with S's state at month d, the point is S from d on, in every cell of S's.

    This is the test that says the opening state is complete: a state column the SEC row
    did not carry, or carried from the wrong instant, would make SEC part from S here, and
    nowhere else, because on a point issued at ``t = 0`` the two clocks coincide and the
    opening state is zero.  For the same reason it is the test that catches a policy month
    passed as ``t`` (R1a), a year-open quantity read at the wrong anniversary, and a
    scenario read on the wrong clock: each row reads its S scenario re-based to its own
    month, and the scenarios step at anniversaries of their own.  S's own in-force points
    1, 3 and 7 are cases too, at 84, where S enters them: the twin of each reproduces S's
    frame from there, the worked example's anniversary 8 at its ``t = 11``.  The frame
    comparisons read SEC row ``t`` against S row ``t + d`` in every column of ``result_cf``
    and of ``result_pols`` both reports hold, and fail frames that end apart.  The cell
    comparison then evaluates every cell of S's but :data:`SPLICE_EXEMPT`, at every
    argument S cached inside its own frame from month ``d`` on, moved onto SEC's clock, to
    1e-9 relative with no absolute floor but on the residuals (:func:`_compare`): the
    account value and the fixed account at every timing, the benefit base, the rollup base,
    the lifetime withdrawal, the phase as a code, the payout rate, the floor, the
    withdrawals to date, the surrender trace, the counts and the reports among them.  The
    anniversaries before the books are skipped (:func:`_on_the_books`).  An S cell this
    model lacked would fail it.

    The row is swept and recorded for the rules test first (:func:`_record`), then
    compared, and released either way.
    """
    found = _splice_case(splices, splice_records, "spliced", (kind, s_point, month))
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:20])


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(splices, splice_records,
                                                             s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of cover, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later, ``result_av``, ``result_glwb`` and ``result_cf_annual`` included, to 1e-9
    relative with no absolute floor (:func:`_compare`).  An S cell this model lacked would
    fail it.  The row's scenario is a copy of S's moved ``k`` months later, with no level
    before issue, so a scenario read there raises inside the comparison.

    Then :func:`_future_facts`, R1 and D4's base rule made testable: before issue every row
    of the four monthly reports is present, and zeros, the phase ``PRE_ISSUE``; the
    contracts arrive in month ``k`` as new business; every decrement rate is the float 0.0
    before issue, where ``result_pols`` reports it; and no age, contract year or
    anniversary has been read below the contract's first, so no rate read its table there.
    A rate left unguarded before issue still gives the right numbers, a count of 0 times
    the rate, but it is not 0.0 there, and it reads its table at an age or a year the
    contract never reaches: the last two checks see it, and the guard test does too.  (A
    recursion based at ``t == 0`` rather than at ``t_entry()`` gives the right numbers as
    well, every cell before issue holding its guard's value; the rules test sees it, as a
    read before the books.)  The pre-issue rows are asserted present before they are
    asserted zero: a frame that opened at issue would have none, its zeros would hold of
    nothing, and the comparisons with S, which start at issue, would not see it.  The row
    is recorded for the rules test first, and released after.
    """
    found = _splice_case(splices, splice_records, "spliced", ("future", s_point, -k))
    assert not found, f"{len(found)} faults, first:\n  " + "\n  ".join(found[:20])


def test_every_state_s_reaches_is_accepted_in_force(splices, tmp_path):
    """Every state the splice's S reaches is a valid opening state, but one (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a contract in force
    can be, so they must accept each state ``FIA_US_S`` reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6; §5.2, T5,
    precised at M10).  So every S point of the splice, S's nine and the eight variants,
    under the splice's References and inputs, is restated in force by the generator at the
    edges of its windows, or with ``USLIB_SEC_FULL=1`` at every month after its entry
    (:func:`_every_state_months`), each on its scenario re-based to its month, into one
    table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses it; and
    ``Data`` reads it again with every amount carried to the cent, as an extract carries it
    (:func:`_refused_in_force`).  But for one state, set aside first: a contract
    terminated, which ``FIA_US_S`` keeps on its frame in ``TERMINATED``, the overdraw's from
    policy month 228 and variant 13's, emptied by its withdrawal in accumulation, from 36,
    and which ``Data`` refuses by name, since that phase is a surrender of every contract.
    It is the only state set aside, and a table holding one is refused, naming the point
    (:func:`_refused_by_name`).  The test runs under each set of inputs on which the states
    S reaches differ (§5.2, T5, precised at M9): the splice's here, the switched
    References' and S's shipped References and inputs.  The module's other References,
    probed at every month on the same points, reach no other state: the cap test's A/E
    moves none but the count, and under T4's raised credit floor and the guaranteed scale
    ``Data`` and ``proj_len()`` refuse none but a contract terminated.
    """
    s, _ = splices.pair("spliced")
    kept, terminated = _states_s_reaches(s)
    assert {point for point, _ in terminated} == {7, 13}, terminated[:5]
    assert {point for point, _ in kept} == set(s.Data.model_point_table().index)
    refused = _refused_in_force(s, kept, tmp_path / "every", SPLICED_REFS, SEC_EDITS)
    assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
    _refused_by_name(s, terminated[0], tmp_path / "terminated", SPLICED_REFS, SEC_EDITS)


# ---------------------------------------------------------------------------
# The values outside cover


def _monthly_args(p, name, cells, t):
    """Every argument tuple Phase 2's full sweep calls monthly cell ``name`` with at ``t``.

    ``t`` alone, or ``t`` with each timing or each kind, the total, ``ALL``, too, each
    passed through :func:`_code`.  (S's collared MVA, ``mva_pp_on``, which took a base
    and a gross, is inline at stage ``"EC"``.)
    """
    if len(cells.parameters) == 1:
        return [(t,)]
    if name in TIMED:
        return [(t, _code(p, label)) for label in TIMED[name]]
    if name in KINDED:
        totals = ([(t, _code(p, "ALL"))] if name in ("claims", "claims_over_av")
                  else [])
        return totals + [(t, _code(p, kind)) for kind in KINDS]
    raise AssertionError(f"{name}{cells.parameters}: a monthly cell _monthly_args lacks")


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, answers wrongly outside cover.

    In every month before issue and at ``t = proj_len()``, the first month after cover,
    which the count's and the account value's look-ahead reads: first every cell of
    :data:`OUTSIDE_COVER`, each of :data:`TIMED` at each of its timings and the
    :data:`KINDED` cells at each kind, against its value and its type, a phase as the
    model's own code; then whether any of :data:`IN_COVER_ONLY` was evaluated on the
    way, which only a fresh ItemSpace can say. Then every monthly cell is called at
    those months, as Phase 2's full sweep will call it, with each of its arguments
    (:func:`_monthly_args`): none may raise or return a numpy type, and afterwards none
    of the readers of :data:`IN_COVER_ONLY`, keyed by an age, a year or an anniversary,
    may hold a key, the sweep calling the monthly ones itself, and no cell keyed by the
    month may hold one past ``t = proj_len()``, the last month Phase 2's ``t`` cache
    holds: a cell that reads ``t + 1`` is guarded there.  A cell that raises is reported
    as a fault too, so the scan goes on.
    """
    faults = []
    entry = p.t_entry()
    months = [*range(entry), p.proj_len()]

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

    def reached(names):
        found = {name: list(p.cells[name].keys())[:5] for name in names}
        return {name: keys for name, keys in found.items() if keys}

    readers = [name for name in IN_COVER_ONLY if "t" not in p.cells[name].parameters]

    for t in months:
        for name, want in OUTSIDE_COVER.items():
            if isinstance(want, tuple):
                want = _code(p, want[0] if t < entry else want[1])
            call(name, (t,), want)
        for name, labels in TIMED.items():
            for label in labels:
                call(name, (t, _code(p, label)), 0.0)
        for name in KINDED:
            for kind in KINDS:
                call(name, (t, _code(p, kind)), 0.0)
    if reached(IN_COVER_ONLY):
        faults.append(f"{where}: evaluated outside cover: {reached(IN_COVER_ONLY)}")
    for name, cells in p.cells.items():
        if "t" not in cells.parameters:
            continue
        for t in months:
            for args in _monthly_args(p, name, cells, t):
                call(name, args)
    if reached(readers):
        faults.append(f"{where}: read outside cover by Phase 2's sweep: {reached(readers)}")
    end = p.proj_len()
    past = {name: [args for args in _cached_args(cells)
                   if _month(args[cells.parameters.index("t")])
                   and args[cells.parameters.index("t")] > end][:5]
            for name, cells in p.cells.items() if "t" in cells.parameters}
    past = {name: keys for name, keys in past.items() if keys}
    if past:
        faults.append(f"{where}: read past t = proj_len() = {end}: {past}")
    return faults


@pytest.mark.parametrize("which", [
    pytest.param("spliced", id="spliced"),
    pytest.param("switched", id="switched", marks=FULL_ONLY)])
def test_every_guarded_cell_holds_its_outside_cover_value(splices, which):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else (:func:`_outside_cover_faults`).  ``is_active``'s docstring promises that
    outside cover no count evaluates a rate, and no table is read at a contract year, an
    age or an anniversary the contract does not have, so afterwards none of
    :data:`IN_COVER_ONLY` may hold a key.  Then every monthly cell, guarded or not, is
    called there, as Phase 2's full sweep will call it: each answers, with a Python value,
    no reader of :data:`IN_COVER_ONLY` keyed by an age, a year or an anniversary is read on
    the way, and no month past ``t = proj_len()`` is, which Phase 2's ``t`` cache does not
    hold: the count's roll-forward residual, which reads ``t + 1``, is guarded there.  Every
    monthly cell is one of those lists, or :data:`EVERY_MONTH`'s, so that a cell added to
    the model is placed in one.

    The committed table's one point issued after the valuation date is the anchor, which
    reads the worked scenario and carries neither another crediting method, nor a fixed
    account, nor a premium tax, nor a withdrawal before exercise, so on it a cell tied to
    one of those would hold zero before issue, guarded or not.  So the same scan runs on
    the splice's future rows, the core's or, with ``USLIB_SEC_FULL=1``, all of them, under
    the shipped References with the splice's assumptions switched on, and, on the full
    grid, under the switched ones: each crediting method, the female table, the two
    programmes and the contract without the rider among them.  Their scenarios hold no
    level before issue, and a scenario level or a reference yield read at the anniversary
    before issue raises,
    which is asserted, rather than answering with a level the path does not hold, while
    the index level there is the row's opening column, 0 on new business.  Each row is
    made afresh first and released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    Phase 2 needs them: a table read at a contract year or an age the contract does not
    have would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    if which == "spliced":
        model = _read(model_path(SEC), "cover")
        try:
            monthly = {n for n, c in model.Projection.cells.items() if "t" in c.parameters}
            placed = {*OUTSIDE_COVER, *IN_COVER_ONLY, *EVERY_MONTH, *TIMED, *KINDED}
            assert monthly <= placed, f"monthly cells unplaced: {sorted(monthly - placed)}"
            table = model.Data.model_point_table()
            for key, point_id in zip(point_keys(model), table.index):
                faults += _outside_cover_faults(projection(model, key), f"point {point_id}")
        finally:
            model.close()
    _, sec = splices.pair(which)
    grid, core = GRIDS[which]
    futures = [case for case in _selected(grid, core) if case[0] == "future"]
    for case in futures:
        key = _row_key(sec, *case)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            p = projection(sec, key)
            faults += _outside_cover_faults(p, f"{which} {_case_id(*case)}")
            for reader, args in (("scenario_value", (-1, _code(p, "INDEX_LEVEL"))),
                                 ("mva_ref_yield", (-1,))):
                with pytest.raises(Exception, match="scenario sets no level by month"):
                    p.cells[reader](*args)
            assert p.index_level(-1) == p.index_level_prev_anniv_init() == 0.0
        finally:
            _release(sec, key, collect=True)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


# ---------------------------------------------------------------------------
# T2 and T3 on the switched References


@pytest.mark.parametrize(
    "kind, s_point, month",
    [_case(case, SWITCHED_CORE, _case_id(*case)) for case in SWITCHED_GRID])
def test_the_switched_references_continue_s(splices, splice_records, kind, s_point,
                                            month):
    """Under :data:`SWITCHED_REFS`, each row is S from its month on, as under the shipped.

    S ships three string switches at one setting and several caps and floors where they
    never bind, and the splice's comparison sees a switch or a bound only where it acts.
    So both models are read again with the other settings and the bounds where they bind
    (:data:`SWITCHED_REFS`), the cap of 0.1% (:data:`SWITCHED_VARIANTS`) beside S's points,
    and each row of :data:`SWITCHED_GRID` is compared with S as T2 and T3 compare theirs
    (:func:`_compare`): the step-up only at exercise, the rollup base reduced by the
    withdrawal itself, the MVA collared by the surrender value, the lapse and the rider
    charge at their caps, the fixed rate, the cap and the credit at their floors, the
    trigger's floor branch and exercise a year later under the minimum age.  What each
    case reaches is recorded for the core's reach test, and the row released.
    """
    found = _splice_case(splices, splice_records, "switched", (kind, s_point, month))
    assert not found, f"{len(found)} faults, first:\n  " + "\n  ".join(found[:20])


def test_every_state_s_reaches_under_the_switched_references_is_accepted_in_force(
        splices, tmp_path):
    """Under :data:`SWITCHED_REFS` too, every state S reaches is accepted, but one (T5).

    The switches and the bounds S ships idle move the states ``FIA_US_S`` reaches, so the
    every-state test runs here too (§5.2, T5, precised at M9): every S point of the
    switched pair, the variants and the cap of 0.1% among them, restated in force at the
    edges of its windows, or at every month with ``USLIB_SEC_FULL=1``, is read by ``Data``,
    exactly and carried to the cent, and has a frame (:func:`_refused_in_force`), but a
    contract terminated, ``TERMINATED``, the overdraw's and variant 13's, which a table
    holding one is refused for, by name.
    """
    s, _ = splices.pair("switched")
    kept, terminated = _states_s_reaches(s)
    assert {point for point, _ in terminated} == {7, 13}, terminated[:5]
    assert {point for point, _ in kept} == set(s.Data.model_point_table().index)
    refused = _refused_in_force(s, kept, tmp_path / "every", SWITCHED_REFS, SEC_EDITS)
    assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
    _refused_by_name(s, terminated[0], tmp_path / "terminated", SWITCHED_REFS, SEC_EDITS)


# ---------------------------------------------------------------------------
# D11's R1, R1a and R2


@pytest.mark.parametrize("which, grid", [
    pytest.param("spliced", "core", id="spliced-core"),
    pytest.param("spliced", "full", id="spliced-full", marks=FULL_ONLY),
    pytest.param("switched", "core", id="switched-core"),
    pytest.param("switched", "full", id="switched-full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(
        splices, splice_records, which, grid):
    """R1, its look-back, R1a and R2's look-ahead, on the rows T2 and T3 compare.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, S's own in-force points
    and the variants among them, and points issued later, under both sets of References,
    and each row was swept first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it, as ``FIA_US_S``'s ``year_open_mth`` would, and so does
      a balance read a month back without the opening state's branch.  The anniversary,
      contract year, age and year-count keys are held to it too.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the pre-issue zeros, so no number shows it and no argument goes
      negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents, but
      the one R2 admits (:data:`LOOK_AHEAD`): ``lapse_rate`` reads the phase, and the
      moneyness factor the account value and the benefit base, at the anniversary closing
      the contract year, ``anniv_mth(t)``, at most 11 months on and inside the frame.  Each
      such read is admitted only where what it reads rests on no count, no decrement and
      nothing the reader holds, and on no month after that anniversary, which is walked
      over the read's precedents (:func:`_closure`); and some read is admitted, so the
      exception is exercised.  A read through a cell keyed by no month is judged against
      the month that asked (:func:`_month_reads`).
    * No index level is read at an anniversary before the contract year under way at
      ``t_entry()``, and no scenario level or reference yield at an anniversary whose month
      precedes ``t_entry()``: the level that opened the year under way is the row's
      column, and the rest is history, which a re-based scenario does not hold.

    Each row was scanned by the case that compared it, and a row no case has scanned is
    scanned here.  The core case covers the core's rows, the full case every other row of
    the full grid, with ``USLIB_SEC_FULL=1``.  The new-business twins in the splice's table
    are no case's, and are left out: on them the clocks coincide, T1 compares the committed
    twins with S cell by cell, and T3 compares every S point and variant issued later, a
    month on or more than a year on.
    """
    grid_cases, core = GRIDS[which]
    cases = [case for case in grid_cases if (case in core) == (grid == "core")]
    found = {"negative": [], "early": [], "ahead": [], "condition": [], "year": []}
    raised, admitted = [], 0
    for case in cases:
        record = _record_of(splices, splice_records, which, case)
        where = _case_id(*case)
        for rule in found:
            found[rule] += [f"{where}: {line}" for line in record[rule]]
        admitted += record["admitted"]
        if record["raised"]:
            raised.append(f"{where}: {record['raised']}")
    assert cases, f"the {which} {grid} grid has no rows"
    assert not raised, f"rows that raised: {raised[:10]}"
    assert not found["negative"], (f"called before the valuation date: "
                                   f"{found['negative'][:10]}")
    assert not found["early"], f"read before issue from the books: {found['early'][:10]}"
    assert not found["ahead"], f"read beyond t + 1: {found['ahead'][:10]}"
    assert not found["condition"], (f"an admitted read rests on a count or a later month: "
                                    f"{found['condition'][:10]}")
    assert not found["year"], (f"read at an anniversary before the books: "
                               f"{found['year'][:10]}")
    assert admitted > 0, "no read of the closing anniversary was admitted"


def test_the_core_grid_reaches_every_branch(splices, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case, T2's or T3's: each crediting
    method, rollup schedule, withdrawal programme, scenario, sex and basis, a fixed account
    and no rider; S's own in-force points; each kind of valuation month, the first policy
    year, an anniversary, mid-year, a year's last month and the last covered month; and a
    point issued more than a year on.

    Then, on the splice's rows, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column non-zero
    and every phase at the anniversary that opened the year under way; the year under way
    read on an anniversary, mid-year, in its last month, in the first policy year and in
    the exercise year, the index level read from the row and the fixed account accrued
    since the anniversary; the last covered month; and in the frame every phase transition,
    each crediting method, the floor and the cap binding, the step-up, the rollup and its
    step-down, the stack, the growth window's end, the withdrawal's ratchet, its excess,
    charge, clawback, negative MVA and collar, the guarantee reduced in part and to 0, an
    unfunded withdrawal, each shock lapse, the moneyness factor and its floor, the floor
    binding on a surrender, a maturity, the floor's charge, the premium tax and commission,
    the female table, the joint basis and the 80+ band.  And of some row of the switched
    References' core, each of :data:`SWITCHED_FRAME`.

    Each core row's branches were recorded by the case that compared it (:func:`_record`),
    and a row no case has recorded is evaluated here.  The splice's models are the last
    thing a test of this module reads, so they are closed here, and the module's other
    tests run without them.
    """
    s_table = _s_table_with({**VARIANTS, **SWITCHED_VARIANTS})

    def at(p, column):
        return s_table.at[p, column]

    def choices(column, values):
        return {f"{column} {v}": (lambda k, p, d, v=v, column=column: at(p, column) == v)
                for v in values}

    static = {
        **choices("credit_method", ("cap", "par", "par_cap", "spread", "trigger")),
        **choices("rollup_id", ("blended", "simple", "none")),
        **choices("wd_schedule_id", ("none", "preexercise", "overdraw", "small")),
        **choices("scenario_id", ("worked", "growth")),
        **choices("sex", ("M", "F")),
        **choices("glwb_basis", ("single", "joint")),
        "a fixed account": lambda k, p, d: at(p, "alloc_indexed") < 1.0,
        "no rider": lambda k, p, d: not at(p, "glwb_elected"),
        "S's own in-force points": lambda k, p, d: k == "twin",
        "the first policy year": lambda k, p, d: k == "derived" and 0 < d < 12,
        "an anniversary": lambda k, p, d: k == "derived" and d % 12 == 0,
        "mid-year": lambda k, p, d: k == "derived" and d % 12 not in (0, 11),
        "a year's last month": lambda k, p, d: k == "derived" and d % 12 == 11,
        "the last covered month": lambda k, p, d: (
            d == 12 * (120 - int(at(p, "age_at_entry")) + 1) - 1),
        "issued more than a year on": lambda k, p, d: k == "future" and -d > 12,
    }
    missing = [what for what, holds in static.items()
               if not any(holds(*case) for case in sorted(CORE_GRID))]
    assert not missing, f"no core case reaches: {missing}"
    try:
        for which, (grid, core) in GRIDS.items():
            reached = set()
            for case in sorted(core):
                reached |= _record_of(splices, splice_records, which, case)["branches"]
            at_valuation, frame = REACH[which]
            missing = [what for what in (*at_valuation, *frame) if what not in reached]
            assert not missing, f"no core row of the {which} grid reaches: {missing}"
    finally:
        splices.close()


# ---------------------------------------------------------------------------
# Models read afresh under References of their own: the cap on mortality, a NaN sent to
# it, and the guaranteed scale
#
# The cap's test and the guaranteed scale's read S and SEC afresh and compare them cell by
# cell, as T1 and T2 do, and the NaN tests read SEC with a NaN Reference.  They run here,
# once the splice's pairs are closed and before the committed models are read and swept,
# so that the models they read never sit in memory beside those.


# FIA_US_S caps the annual mortality already, and SEC writes the cap with its bound
# second, min(q, 1.0): the same float as min(1.0, q) wherever q is a number, and NaN where
# it is NaN (§5.1, step 6).  At the shipped factor of 1 the cap binds at age 120 only,
# where the table is 1; at 1.25 the product of the factor and the table's rate first
# passes 1 on the anchor at age 115, policy month 636, at 1.0028, and stays past it.
CAPPED_REFS = {**SPLICED_REFS, "mort_ae_factor": 1.25}
CAP_MTH, CAP_AGE = 636, 115


def _uncapped_mort_rate(s_proj, t):
    """The annual mortality ``FIA_US_S`` caps in month ``t``, from its own cells.

    ``mort_ae_factor`` times the rate S's ``mort_table`` gives at the point's attained age
    and sex, the product ``mort_rate`` caps.
    """
    rate = s_proj.data.mort_table().loc[(s_proj.age(t), s_proj.sex()), "mort_rate"]
    return s_proj.mort_ae_factor * float(rate)


def test_a_capped_annual_mortality_is_the_float_1_and_kills_every_contract(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1, the float.

    On S and SEC read afresh under :data:`CAPPED_REFS`, set before either computes
    anything, the product of S's A/E factor and its table's rate on the anchor
    (:func:`_uncapped_mort_rate`) first passes 1 at :data:`CAP_MTH`, attained age
    :data:`CAP_AGE`, and stays past it to the end of cover.  Both models cap it: on S's
    point and on the twin issued at the valuation date, ``mort_rate`` and the monthly
    rate, ``1 - (1 - q)^(1/12)``, are 1.0 in every one of those months, the float, not the
    int 1, which compares equal to it, and floats below 1 in every month before.  So every
    contract in force at the start of the first capped month dies in it, and none is in
    force after it, in both.  In every cell of S's the twin agrees with S at every
    argument S cached, the capped months and the reports included, with no absolute
    floor: the counts there are near 1e-10, where a floor of 1e-9 hides any difference.
    Then the point is restated in force the month before the cap, opened with S's count
    there, and compared from that month on as T2 compares; and once more five months into
    the capped year, opened with one contract.  On each, in its first capped month, both
    rates are ``(float, 1.0)``, every contract in force dies in that month, and none is in
    force after it.  And every number of every report, S's and SEC's, is a finite float.
    """
    s = _read(model_path(TWIN), "capped_s", CAPPED_REFS)
    try:
        s2 = _point(s, 2)
        end = s2.proj_len()
        cap = next(t for t in range(end) if _uncapped_mort_rate(s2, t) > 1.0)
        assert (cap, s2.age(cap)) == (CAP_MTH, CAP_AGE)
        after = range(cap, end)
        assert all(_uncapped_mort_rate(s2, t) > 1.0 for t in after)
        _sweep_s(s2)
        spec = dataclasses.replace(SPEC, derived=((2, cap - 1), (2, cap + 4)), future=())
        table, companions = build_sec_table(spec, s)
        later = table.index[table["source_mth"] == cap + 4]
        table.loc[later, "policy_count"] = 1.0
        sec = _read(temp_inputs(tmp_path, model_path(SEC), model_points=table,
                                model_point_file=TABLE,
                                edits={COMPANION: companions[COMPANION]}),
                    "capped", CAPPED_REFS)
        try:
            twin, before, inside = (_row(sec, *case) for case in (
                ("twin", 2, 0), ("derived", 2, cap - 1), ("derived", 2, cap + 4)))
            for p in (s2, twin):
                assert p.proj_len() == end
                for rate in ("mort_rate", "mort_rate_mth"):
                    values = [p.cells[rate](t) for t in range(end)]
                    assert all(type(q) is float and q < 1.0 for q in values[:cap]), rate
                    assert [(type(q), q) for q in values[cap:]] == [(float, 1.0)] * len(
                        after), rate
                assert p.pols_if(cap) > 0.0 and p.pols_death(cap) == p.pols_if(cap)
                assert [p.pols_if(t) for t in range(cap + 1, end + 1)] == [0.0] * len(after)
            assert _mismatches(s2, twin, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt,
                               atol=0.0) == []
            assert before.policy_count() == s2.pols_if(cap - 1) < 1e-9
            assert _compare(s2, before, cap - 1, SPLICE_EXEMPT) == []
            for p, first in ((before, 1), (inside, 0)):
                for rate in ("mort_rate", "mort_rate_mth"):
                    q = p.cells[rate](first)
                    assert (type(q), q) == (float, 1.0), (first, rate)
                assert p.pols_if(first) > 0.0
                assert p.pols_death(first) == p.pols_if(first)
                assert [p.pols_if(t) for t in range(first + 1, p.proj_len() + 1)] == [
                    0.0] * (p.proj_len() - first)
            for p in (s2, twin, before, inside):
                for report in REPORTS:
                    frame = p.cells[report]().select_dtypes("number")
                    assert (frame.dtypes == "float64").all(), report
                    assert np.isfinite(frame.to_numpy()).all(), report
        finally:
            sec.close()
    finally:
        s.close()


# A NaN, what a blank rate would carry, sent to the mortality through its one factor, a
# Reference, set on a model read for the test before it computes anything, which a
# compiled model runs too (USLIB-SEC-PLAN.md K7).
NAN_FACTOR = {"mort_ae_factor": float("nan")}

# The calls of the anchor issued at the valuation date that a NaN mortality rate must reach
# as NaN: the annual rate in the first month, at the exercise and in the last covered month,
# the monthly rate, and the count the month after the first.
NAN_CALLS = (("mort_rate", 0), ("mort_rate", 95), ("mort_rate", 707), ("mort_rate_mth", 0),
             ("pols_if", 1))


def test_a_nan_that_reaches_the_cap_on_mortality_stays_nan():
    """A NaN that reaches the cap on mortality stays NaN, and is not read as certain death.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds.  So with its bound first,
    ``min(1.0, q)``, the cap would turn a NaN into 1.0: a blank rate would read as certain
    death in month 0, every flow finite, and nothing would show it.  This model writes the
    bound second, ``min(q, 1.0)`` (``mort_rate``'s docstring), the same float wherever
    ``q`` is a number, so no comparison with S can tell the two apart.  ``Data`` refuses a
    blank, text or infinite rate (:data:`TABLE_FAULTS`), so the cap is sent a NaN through
    ``mort_ae_factor``, the factor the table's rate is multiplied by, a Reference set to
    NaN on a model read for the test, before it computes anything (:data:`NAN_FACTOR`),
    which the compiled model runs too
    (:func:`test_the_compiled_model_carries_a_nan_reference_as_modelx_does`).  Each of
    :data:`NAN_CALLS` must then be the float NaN: the annual and the monthly rate, not
    1.0, and the count the month after, not 0.0.  Where the product passes 1, the cap's
    test above holds the other side, the float 1.0.  The one other ``min`` a NaN can
    reach with its bound written second, the rider charge's, has a test of its own, below.
    """
    model = _read(model_path(SEC), "nan", NAN_FACTOR)
    try:
        p = _row(model, "twin", 2, 0)
        lost = []
        for name, t in NAN_CALLS:
            value = p.cells[name](t)
            if not (type(value) is float and math.isnan(value)):
                lost.append(f"{name}({t}) = {value!r}")
        assert not lost, f"the cap on mortality loses a NaN rate: {lost}"
    finally:
        model.close()


def test_a_nan_rider_charge_rate_stays_nan_past_its_cap():
    """A NaN rider charge rate reaches the charge as NaN, and the months before it finite.

    ``FIA_US_S``'s own cap on the rider charge, ``min(rider_charge_rate,
    rider_charge_rate_max)``, kept in S's order (USLIB-SEC-PLAN.md §5.1, step 6), holds
    a NaN rate as NaN, where a cap written the other way round would charge the cap.  On
    a model read with the rate set to NaN, before it computes anything, the anchor issued
    now pays its first charge at its first anniversary, ``t = 11``: there the charge is
    the float NaN, not the capped rate times the base; and in each month before it, which
    computes the account value and the flows without the charge, every cash flow and the
    account value are finite numbers, the account value above 0, not NaN from the start
    (N5).
    """
    model = _read(model_path(SEC), "nan_rider", {"rider_charge_rate": float("nan")})
    try:
        p = _row(model, "twin", 2, 0)
        charge = p.rider_charge_pp(11)
        assert type(charge) is float and math.isnan(charge), charge
        before = p.result_cf().loc[:10]
        assert np.isfinite(before.to_numpy()).all()
        assert all(math.isfinite(p.av_pp(t)) and p.av_pp(t) > 0.0 for t in range(11))
    finally:
        model.close()


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``FIA_US_S``'s ``isclose`` does.

    Each check asks of every month whether the residual is within its tolerance,
    ``not abs(r) <= tol`` failing it, so that a residual that is not a number fails, where
    a check that asked whether the residual exceeds its tolerance would pass it: no
    comparison with NaN holds (USLIB-SEC-PLAN.md §7.1, precised at M3).  The checks are
    what a reader runs to trust the frame, so a NaN must not pass them.  On a model read
    for the test with :data:`NAN_FACTOR`, a NaN mortality, both residuals are NaN in each
    point's first month in force, on the anchor issued at the valuation date and on its
    twin in force at 84, and both checks are ``False``.  On the anchor issued 15 months
    on, both residuals are 0.0 before issue, where no count is held, and NaN from its
    issue month, and both checks are ``False``.  And on the same rows of the committed
    model, under the shipped References, both checks are ``True``, so that a check that
    always failed would fail here (N5).
    """
    model = _read(model_path(SEC), "nan_check", NAN_FACTOR)
    shipped = _read(model_path(SEC), "nan_check_base")
    try:
        for case, first in ((("twin", 2, 0), 0), (("twin", 1, 84), 0),
                            (("future", 2, -15), 15)):
            p, base = _row(model, *case), _row(shipped, *case)
            for check in ("check_av_roll_fwd", "check_pols_roll_fwd"):
                resid = p.cells[f"{check}_resid"]
                before = [resid(t) for t in range(first)]
                assert before == [0.0] * first, (case, check, before)
                assert type(resid(first)) is float and math.isnan(resid(first)), (
                    case, check, resid(first))
                assert p.cells[check]() is False, (case, check)
                assert base.cells[check]() is True, (case, check)
    finally:
        shipped.close()
        model.close()


def test_the_guaranteed_scale_is_s_s():
    """Under the guaranteed scale the model is S, cell by cell, as under the declared one.

    ``use_guaranteed_scale`` ships False, so T1 never sees the guaranteed minimum cap and
    fixed rate a contract falls back to.  On S and SEC read afresh with it True, before
    either computes anything, the twins of S points 2, 4 and 9, the anchor, the fixed
    account and the deferred income, issued at the valuation date, agree with S in every
    cell at every argument S cached, bit for bit, the cap in force at ``cap_rate_min`` and
    the fixed rate at ``fixed_rate_min``.
    """
    s = _read(model_path(TWIN), "guaranteed_s", {"use_guaranteed_scale": True})
    sec = _read(model_path(SEC), "guaranteed", {"use_guaranteed_scale": True})
    try:
        for point_id in (2, 4, 9):
            s_proj = _point(s, point_id)
            _sweep_s(s_proj)
            p = _row(sec, "twin", point_id, 0)
            assert (p.cap_rate_in_force(), p.fixed_rate_in_force()) == (
                p.cap_rate_min, p.fixed_rate_min)
            assert p.cap_rate_in_force() < p.cap_rate()
            assert _mismatches(s_proj, p, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt, rtol=0,
                               atol=0) == [], point_id
            _release(s, _key(s, point_id), collect=True)
            _release(sec, _row_key(sec, "twin", point_id, 0), collect=True)
    finally:
        sec.close()
        s.close()


def test_a_credit_floor_above_the_cap_is_s_s():
    """With the credit floor above the cap in force, the model is S, cell by cell.

    ``FIA_US_S`` credits ``max(f, min(c, R))``: the cap first, then the floor, so that a
    floor above the cap credits the floor.  Wherever the floor is at or below the cap,
    as shipped and under every set of References the grids run, the other order,
    ``min(c, max(f, R))``, gives the same number, and no comparison can tell the two
    apart.  So on S and SEC read afresh with ``floor_rate`` at 8%, above the anchor's
    5.25% cap and point 4's 6%, before either computes anything, the twins of S points 2
    and 4, the cap and the capped participation methods, issued at the valuation date,
    agree with S in every cell at every argument S cached, bit for bit, and each first
    credit is the floor.
    """
    refs = {"floor_rate": 0.08}
    s = _read(model_path(TWIN), "floor_s", refs)
    sec = _read(model_path(SEC), "floor", refs)
    try:
        for point_id in (2, 4):
            s_proj = _point(s, point_id)
            _sweep_s(s_proj)
            p = _row(sec, "twin", point_id, 0)
            assert p.cap_rate_in_force() < p.floor_rate
            assert p.credit_rate(11) == p.floor_rate
            assert _mismatches(s_proj, p, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt, rtol=0,
                               atol=0) == [], point_id
            _release(s, _key(s, point_id), collect=True)
            _release(sec, _row_key(sec, "twin", point_id, 0), collect=True)
    finally:
        sec.close()
        s.close()


# Each switch at its other setting alone, as S's text, with the S point whose projection
# it moves: the step-up at exercise on the anchor, and the dollar rollup base on the
# pre-exercise programme, which reduces the base.  The surrender-value collar binds on no
# committed point under any References alone, only on the switched grid's variant 15.
SWITCHED_ALONE = (("step_up_mode", "at_exercise", 2), ("rb_wd_convention", "dollar", 8))


def test_each_switch_set_alone_is_s_s():
    """Each switch, set alone to its other setting, gives S's projection, cell by cell.

    The switched grid sets the three switches together, and each holds the same code, 1,
    at its other setting, so a decode that read another switch's Reference, ``is_rb_dollar``
    comparing ``mva_collar_basis``, say, would pass there, and at the shipped settings,
    all 0.  So on S and SEC read afresh with each switch of :data:`SWITCHED_ALONE` set,
    S's text on S and its code on SEC (:func:`_switch`), before either computes anything,
    the twin of the S point it moves agrees with S in every cell at every argument S
    cached, bit for bit, and differs from the shipped setting's projection.
    """
    base = _read(model_path(SEC), "alone_base")
    try:
        for ref, value, point_id in SWITCHED_ALONE:
            s = _read(model_path(TWIN), "alone_s", {ref: value})
            sec = _read(model_path(SEC), "alone", {ref: value})
            try:
                s_proj = _point(s, point_id)
                _sweep_s(s_proj)
                p = _row(sec, "twin", point_id, 0)
                assert _mismatches(s_proj, p, exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt,
                                   rtol=0, atol=0) == [], ref
                shipped = _row(base, "twin", point_id, 0)
                assert any(frame_mismatches(shipped.cells[report](), p.cells[report](),
                                            rtol=0, atol=0)
                           for report in ("result_av", "result_glwb")), ref
            finally:
                sec.close()
                s.close()
    finally:
        base.close()


# ---------------------------------------------------------------------------
# D3's closed-form clock, and R2's recursions on the committed model


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(400)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 401 months from 0.  And on every committed point, at every month of its
      frame, ``duration_mth(t)`` is ``duration_mth_init() + t``, ``anniv_mth(t)`` is the
      month whose policy month closes the contract year of ``t``, and ``year_open_mth(t)``
      the month before that year's first, twelve months earlier: both months of the
      frame, on the valuation clock, before the valuation date where the year opened
      before it.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow; the floor's chain, first read deep in the frame through the
      depletion test, takes the sweep to 370, which is what sets the limit.  A backward
      recursion over the frame, through ``t + 1``, keeps every step within the look-ahead
      but opens a chain as long as the frame, which a compiled model would run on the C
      stack (F7), and fails here, on every committed frame but the last policy year's.
    """
    model, record = sec_read
    assert record["duration_mth(400)"] == 400
    assert record["keys"] == [400]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"
    table = model.Data.model_point_table()
    short = []
    for key, point_id in zip(point_keys(model), table.index):
        p = projection(model, key)
        d0 = p.duration_mth_init()
        assert d0 == table.at[point_id, "duration_mth"]
        for t in range(p.proj_len()):
            year = p.duration(t)
            assert p.duration_mth(t) == d0 + t, (point_id, t)
            assert p.duration_mth(p.anniv_mth(t)) == 12 * year + 11, (point_id, t)
            assert t <= p.anniv_mth(t) <= t + 11, (point_id, t)
            assert p.year_open_mth(t) == p.anniv_mth(t) - 12, (point_id, t)
            assert p.duration_mth(p.year_open_mth(t) + 1) == 12 * year, (point_id, t)
        if p.proj_len() <= CALL_DEPTH + 60:
            short.append(point_id)
    assert short == [_label(table, "derived", 6, 696)], short


def _cold_depth(proj, cell, args):
    """The frames on modelx's stack at the deepest point of ``cell(*args)``, called cold.

    The deepest stack position modelx's trace records, plus one, on an ItemSpace that has
    evaluated nothing.  modelx warns as the trace starts and as it stops.
    """
    with pytest.warns(UserWarning, match="call stack trace"):
        mx.start_stacktrace(maxlen=None)
        try:
            proj.cells[cell](*args)
            trace = mx.get_stacktrace()
        finally:
            mx.stop_stacktrace()
    return 1 + max(depth for event, depth, *_ in trace if event == "ENTER")


# The cold calls the depth test makes on the committed model, each on an ItemSpace of its
# own, and the chains each walks the length of: the last month's net cash flow walks the
# count, the account value, the fixed account, the floor and the withdrawals' year chains
# on S's anchor in force, on the anchor issued at the valuation date, in the last policy
# year, and on the point issued 15 months on, from issue, not from t = 0; the floor's chain
# and the withdrawals to date are called alone on the overdraw's twin, whose first
# anniversary reads the account value's chain under the floor's, and the account value's
# and the fixed account's on the future row.
COLD_CALLS = ((("twin", 1, 84), "net_cf"), (("twin", 2, 0), "net_cf"),
              (("derived", 6, 696), "net_cf"), (("future", 2, -15), "net_cf"),
              (("twin", 7, 84), "mgsv_pp"), (("twin", 7, 84), "wd_cum_pp"),
              (("future", 2, -15), "av_pp"), (("future", 2, -15), "av_fixed_pp"))

# The count's chain called alone, cold: its first month on the books reads the lapse at
# the anniversary closing the first contract year, R2's admitted read, and so walks the
# account value's chain there, up to LOOK_AHEAD_MTHS long, under the count's.
COUNT_CALLS = ((("twin", 1, 84), "pols_if"), (("future", 2, -15), "pols_if"))


def _longest_cover(committed):
    """The anchor issued at age 40, at the valuation date and 120 months on: its table and
    the scenario companion with the anchor's path moved 120 months on, ``worked-F120``.

    40 is the youngest issue age the product allows (product-spec.md) and the mortality
    table's first, so 972 months of cover, to the contract year entered at 120, is the
    longest a contract has, and 120 months on is the horizon.
    """
    twin, future = _label(committed, "twin", 2, 0), _label(committed, "future", 2, -15)
    table = committed.loc[[twin, future]].assign(age_at_entry=40)
    table = _cells(future, duration_mth=-120, scenario_id="worked-F120")(table)
    scenarios = _companion()
    worked = scenarios[scenarios["scenario_id"] == "worked"]
    later = worked.assign(scenario_id="worked-F120", t=worked["t"] + 120)
    return table, pd.concat([scenarios, later], ignore_index=True)


@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold call holds one frame a month back to ``t_entry()``, and a few more (F7).

    Every recursion here is one cell a month: the count, the account value, the fixed
    account, the floor and the withdrawals to date, and the year chains through the
    anniversary opening each year.  A compiled model runs each chain on the C stack, so
    the depth is what sizes it, and no comparison sees it: a chain of two cells a month
    gives the same numbers.  So each cold call of :data:`COLD_CALLS`, on an ItemSpace of
    the committed model that has evaluated nothing, holds at least one frame for each month
    back to ``t_entry()``, and so walked its chain, and at most :data:`CHAIN_OVERHEAD`
    more.  The point issued 15 months on walks from its issue: a chain that ran on through
    its months before issue, as one guarded by the frame rather than by cover would, walks
    15 months further.  The count's chain alone (:data:`COUNT_CALLS`) holds at most
    :data:`LOOK_AHEAD_MTHS` more, R2's admitted read of the closing anniversary, which
    opens the account value's chain under the count's first month.

    The same holds at the contract's longest cover from issue, 972 months at issue age 40
    (:func:`_longest_cover`), at the valuation date and 120 months after it, the horizon,
    each cold: that is the depth Phase 2's stack is sized from (USLIB-SEC-PLAN.md §7.11),
    979 levels on ``net_cf`` and 997 on the count alone, against 972 months.  And so, at
    stage EC, does the count's residual, ``check_pols_roll_fwd_resid``, the deepest cold
    head of the export (``sample_sec.py``), which reads the count a month on and so opens
    the count's chain, and the look-ahead under its first month, from the last.
    """
    model = _read(model_path(SEC), "depth")
    try:
        for case, cell in (*COLD_CALLS, *COUNT_CALLS):
            key = _row_key(model, *case)
            p = projection(model, key)
            months = p.proj_len() - p.t_entry()
            depth = _cold_depth(p, cell, (p.proj_len() - 1,))
            extra = LOOK_AHEAD_MTHS if (case, cell) in COUNT_CALLS else 0
            assert months <= depth <= months + CHAIN_OVERHEAD + extra, (case, cell, months,
                                                                         depth)
            _release(model, key)
    finally:
        model.close()
    table, scenarios = _longest_cover(_committed())
    model = _read(_sec_inputs(tmp_path, table, {COMPANION: scenarios}), "depth40")
    try:
        for key in point_keys(model):
            for cell, extra in (("net_cf", 0), ("pols_if", LOOK_AHEAD_MTHS),
                                ("check_pols_roll_fwd_resid", LOOK_AHEAD_MTHS)):
                p = projection(model, key)
                months = p.proj_len() - p.t_entry()
                assert months == 972, (key, p.proj_len(), p.t_entry())
                depth = _cold_depth(p, cell, (p.proj_len() - 1,))
                assert months <= depth <= months + CHAIN_OVERHEAD + extra, (key, cell,
                                                                             depth)
                _release(model, key)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, surrenders and deemed maturities alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, "BEF_DECR")``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, "BEF_NB")``, is the three outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month
    too long: the maturities would then leave a month late, and the count would carry
    over.  And the notes' end-of-month ``l(t)``, ``pols_if_at(t, "AFT_DECR")``, is exactly
    the count carried into the next month before its new business, in every month but the
    last covered one, where it is what the deemed maturity takes out and the next month
    opens empty: the two are one product in one order.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.  A timing the model does not have, ``basiclife.BasicTerm_SE``'s
    ``"BEF_MAT"``, which a formula ported from it might ask for, is refused rather than
    answered with another count.
    """
    bef_nb, bef_decr, aft_decr = (_code(sec_model.Projection, label)
                                  for label in ("BEF_NB", "BEF_DECR", "AFT_DECR"))
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        last = p.proj_len() - 1
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, bef_decr) - p.pols_if_at(t + 1, bef_nb)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
            if t < last:
                assert p.pols_if_at(t, aft_decr) == p.pols_if_at(t + 1, bef_nb), (
                    point_id, t)
                assert p.pols_maturity(t) == 0.0, (point_id, t)
        assert p.pols_maturity(last) == p.pols_if_at(last, aft_decr), point_id
        assert p.pols_if_at(last + 1, bef_nb) == 0.0, point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id
    anchor = _row(sec_model, "twin", 1, 84)
    _refused(lambda: anchor.pols_if_at(0, _code(anchor, "BEF_MAT")), "invalid timing")


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin: the six issued at the valuation date,
    row for row, and S's three in force at 84 from S's month 84 on, which is their
    ``t = 0``.  Every column S's report has agrees, to 1e-9 relative with no absolute floor,
    frames ending together, and ``pols_new_biz`` holds the count in the issue month and 0
    in every other, so on the twins in force, 0 throughout.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        month = int(table.at[point_id, "source_mth"])
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == [theirs.columns[0], "pols_new_biz",
                                      *theirs.columns[1:]], point_id
        assert frame_mismatches(theirs, mine, t_offset=month, atol=0.0) == [], point_id
        issue = -p.duration_mth_init()
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == issue else 0.0 for t in mine.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
# And the rows it multiplies: S's anchor in force, the fixed account on its anniversary,
# joint income mid-year, the overdraw near exhaustion, the anchor depleted, the
# pre-exercise programme in its first policy year and the anchor issued 15 months on,
# between them every flow: an income paid after depletion, an excess withdrawal and its
# charges, an unfunded withdrawal, a depletion, the premium, its commission, tax and
# acquisition, and, on mortality cut at 120, the deemed maturity.
COUNT_FACTOR = 2.5
SCALED_ROWS = (("twin", 1, 84), ("derived", 4, 60), ("derived", 5, 150),
               ("derived", 7, 216), ("derived", 2, 240), ("derived", 8, 6),
               ("future", 2, -15))
COUNTED_REFS = {**SPLICED_REFS, "floor_rate": 0.001}


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed rows of :data:`SCALED_ROWS`, and a copy of them with every count
    multiplied by :data:`COUNT_FACTOR`, are each read on mortality cut at 120
    (:func:`_mortality_cut`), so that contracts survive to the deemed maturity, and with
    :data:`COUNTED_REFS` set before either computes anything: the assumptions that ship at
    zero switched on at the splice's values, the credit floor among them, so that every
    flow is nonzero on some row, the commission, the premium tax and the floor's charge
    among them.  On every row ``result_cf`` and the counts of ``result_pols`` are 2.5 times
    the committed rows', element by element, to 1e-12 relative: a scaled count is a
    computed float, which may come back from the CSV within two ulps (``sec_support``'s
    module docstring).  So is every other cell of :data:`COUNTED`, at every argument the
    sweep of the committed row cached, the counts and the account value in force at each
    timing among them, and the rates of ``result_pols`` are the committed rows' exactly.
    And every cell outside :data:`COUNTED` (the account value, the fixed account, the
    benefit base, the rollup base, the lifetime withdrawal, the floor, the phase, the
    opening state, the rates, both clocks, the flags) agrees at every argument that sweep
    cached, the checks still closing.  So a flow that dropped the count, or read it as
    whole contracts, which a table of counts of 1 hides from every comparison with S, fails
    here.  Each row is released once compared.
    """
    committed = _committed()
    table = committed.loc[[_label(committed, *case) for case in SCALED_ROWS]]
    base = _read(_sec_inputs(tmp_path / "base", table, SEC_EDITS), "counted", COUNTED_REFS)
    scaled = _read(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"]), SEC_EDITS), "scaled",
                   COUNTED_REFS)
    nonzero = set()
    try:
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
            one, many = projection(base, key), projection(scaled, scaled_key)
            _sweep_sec(one)
            for report in ("result_cf", "result_pols"):
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in POLS_RATES]
                bad = ((d[flows] - COUNT_FACTOR * b[flows]).abs()
                       > 1e-12 * (COUNT_FACTOR * b[flows]).abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                rates = [c for c in b.columns if c in POLS_RATES]
                assert d[rates].equals(b[rates]), (key, report)
            for name in SCALED:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= 1e-12 * abs(want), (key, name, args, got,
                                                                  want)
                    if want != 0.0:
                        nonzero.add(name)
            assert _mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED | RESIDUALS,
                               rtol=1e-12, atol=0.0) == []
            assert many.check_av_roll_fwd() and many.check_pols_roll_fwd(), key
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    assert nonzero == set(SCALED), f"0 on every row: {sorted(set(SCALED) - nonzero)}"


def test_the_roll_forward_checks_close_on_a_million_contracts(tmp_path):
    """Both roll-forward checks scale their tolerance with the count, and close at 1e6.

    A residual is rounding on that many contracts, so ``check_av_roll_fwd`` holds it to
    ``check_tol_av x max(policy_count(), 1)`` and ``check_pols_roll_fwd`` likewise, where
    ``FIA_US_S``'s tolerance is fixed: at the counts the other tests use, one contract or
    less, the residuals are far inside either.  So the anchor's twin issued at the
    valuation date and joint income in force mid-year are projected from a copy where each
    counts a million contracts: both checks close, and each residual somewhere exceeds the
    fixed tolerance it would have had, so the scaling is what closes them.
    """
    committed = _committed()
    rows = [_label(committed, "twin", 2, 0), _label(committed, "derived", 5, 150)]
    model = _read_edited(tmp_path, _set("policy_count", rows, 1e6), "million")
    try:
        for row in rows:
            p = _point(model, row)
            assert p.policy_count() == 1e6
            assert p.check_av_roll_fwd() and p.check_pols_roll_fwd(), row
            av = max(abs(p.check_av_roll_fwd_resid(t)) for t in range(p.proj_len()))
            pols = max(abs(p.check_pols_roll_fwd_resid(t)) for t in range(p.proj_len()))
            assert av > p.check_tol_av and pols > p.check_tol_pols, (row, av, pols)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, built so that only the rule
# under test refuses it, wherever one can be: a column the rules tie to another is moved
# with it.  The checks run over the whole table as it is read, in Data, and the message
# names the file it read and the column or every point at fault.  A blank cell reads as NaN,
# and so does a text cell once the checks coerce the column to numbers, so each is refused
# as a number that is not one.  The repeated point_id holds another contract under the same
# label, as a bad extract would, so that the check must look at the labels and not at whole
# rows.  The point_ids are the committed table's: 1, S's anchor in force at 84, on an
# anniversary; 2, the anchor issued at the valuation date; 3, the simple rollup; 4, the
# fixed account, issued at the valuation date; 5, joint; 8, the pre-exercise programme; 9,
# income deferred to 85; 10, the fixed account on an anniversary in accumulation, 60; 11,
# the anchor at 95, the last month of its accumulation; 12, joint income mid-year, 150; 13,
# the overdraw near exhaustion, 216; 14, the anchor depleted, 240, an anniversary; 15, the
# pre-exercise programme in its first policy year, 6; 16, no rider in the last policy year,
# 696; 17, the fixed account in income mid-year, 100; and 18, the anchor issued 15 months
# on.  The checks that turn on the policy month are tested at the ends of their window
# (§5.2, T5, precised at M10): the first policy year's at months 1 and 11, accepted at 12;
# an anniversary's at the first, 12, accepted at 11 and 13; the rules off an anniversary at
# months 1, 11 and 13, either side of the first anniversary, where the anniversary's exact
# rules leave no state to accept; and no state before issue at the horizon, -120, as well
# as at 0 and -15, accepted at 1.  The money rules are pinned from both sides of their
# tolerance, 1.1 cents past a cent refused and 0.9 of a cent read, on both signs where a
# rule takes an absolute value, the indexed account's at 3.1 and 2.9 cents; the rules a
# cent cannot touch, two values of one instant on an anniversary, are refused half a cent
# apart.  Where a
# fault breaks two rules by its nature, a value no rule can take alone, the case is named
# for the order it pins: the earlier rule must refuse it, with its own message, before the
# later one would refuse it otherwise (listed above MALFORMED).  The last checks join each
# point's keys to the tables they key: a scenario that sets its levels by the point's first
# month on the books, a rollup schedule, a withdrawal programme, and a sex and an attained
# age in the mortality table.  A {file} in a message is the table's filename: every case
# reads its own file (the malformed fixture).

_POINT = "it is not at point_id {points}"
_COUNT = "{{file}}: policy_count must be a number, zero or more; " + _POINT
_DURATION = "{{file}}: duration_mth must be a whole number of months; " + _POINT
_YEARS = "{{file}}: {column} must be a whole number of years; " + _POINT
_JOINT = ("{{file}}: joint_age must be blank or a whole number of years, 0 or more; "
          + _POINT)
_ELECTED = "{{file}}: glwb_elected must be True or False; " + _POINT
_NUMBER = "{{file}}: {column} must be a number, zero or more; " + _POINT
_ALLOC = "{{file}}: alloc_indexed must be a number from 0 to 1; " + _POINT
_I0 = "{{file}}: mva_ref_yield_at_issue must be a number above -1; " + _POINT
_PAYOUT = ("{{file}}: payout_rate_locked_prev_anniv_init must be a number from 0 to 1; "
           + _POINT)
_LEVEL = ("{{file}}: index_level_prev_anniv_init must be a number, zero or more; "
          + _POINT)
_CODE = ("{{file}}: phase_prev_anniv_init must be a whole number, a phase code; "
         + _POINT)
_NO_STATE = ("{{file}}: {column} must be 0 on a policy not yet in force, duration_mth 0 or "
             "less; " + _POINT)
_IN_FORCE_PHASE = ("{{file}}: phase_prev_anniv_init must be 1 (ACCUM), 2 (INCOME) or 3 "
                   "(DEPLETED) on a policy in force: 4 (TERMINATED) is a deemed surrender "
                   "of every contract; " + _POINT)
_IN_FORCE_LEVEL = ("{{file}}: index_level_prev_anniv_init must be more than 0 on a policy "
                   "in force; " + _POINT)
_RIDER_INCOME = ("{{file}}: a policy without the rider is in phase 1 (ACCUM): income "
                 "starts only under the rider; " + _POINT)
_NO_RIDER = "{{file}}: {column} must be 0 on a policy without the rider; " + _POINT
_RIDER_BASE = ("{{file}}: benefit_base_pp_init must be more than 0 on a policy in force "
               "with the rider: an anniversary that takes it to 0 terminates the contract; "
               + _POINT)
_ACCUM = ("{{file}}: {column} must be 0 in phase 1 (ACCUM), before the first lifetime "
          "withdrawal; " + _POINT)
_INCOME = ("{{file}}: lw_pp_init must be 0 in phase 2 (INCOME) or 3 (DEPLETED) exactly "
           "where payout_rate_locked_prev_anniv_init is 0: the lifetime withdrawal is the "
           "locked percentage of a benefit base above 0, and a reduction that took it to 0 "
           "would have taken the base to 0 and terminated the contract; " + _POINT)
_DEPLETED = ("{{file}}: {column} must be 0 in phase 3 (DEPLETED), the account value "
             "exhausted; " + _POINT)
_YEAR_OPEN_AV = ("{{file}}: av_pp_prev_anniv_init must be more than 0 in phase 1 (ACCUM) "
                 "or 2 (INCOME): an anniversary that exhausts the account value leaves "
                 "them; " + _POINT)
_FIXED_PART = ("{{file}}: {part}, the fixed account, must not exceed {whole}, the account "
               "value it is part of; it does at point_id {points}")
_FIRST_YEAR = ("{{file}}: {column} must be its issue value in the first policy year, "
               "duration_mth 1 to 11, to a cent; " + _POINT)
_FIRST_PHASE = ("{{file}}: phase_prev_anniv_init must be 1 (ACCUM) in the first policy "
                "year; " + _POINT)
_ANNIVERSARY = ("{{file}}: on a point valued on a policy anniversary, duration_mth a "
                "multiple of 12, {column} must equal {entering}; it does not at point_id "
                "{points}")
_INDEXED = ("{{file}}: off an anniversary, the indexed account, av_pp_init less "
            "av_fixed_pp_init, must equal av_pp_prev_anniv_init less "
            "av_fixed_pp_prev_anniv_init, to three cents: it moves only at an anniversary; "
            "it does not at point_id {points}")
_FIXED_FALLEN = ("{{file}}: off an anniversary, av_fixed_pp_init must not be below "
                 "av_fixed_pp_prev_anniv_init: the fixed account only accrues between "
                 "anniversaries; it is at point_id {points}")
_SCENARIO = ("{{file}}: scenario_id must be a scenario of rate_scenario_sec.csv that sets "
             "its levels by the first month the point is on the books, t = 0 or its issue "
             "month if later; " + _POINT)
_ANNIVERSARY_LEVEL = ("{{file}}: on a point valued on a policy anniversary, duration_mth a "
                      "multiple of 12, index_level_prev_anniv_init must equal the "
                      "index_level its scenario sets at t = 0, the valuation date; it does "
                      "not at point_id {points}")
_ROLLUP = "{{file}}: rollup_id must be a schedule of rollup_table.csv; " + _POINT
_PROGRAMME = ("{{file}}: wd_schedule_id must be a programme of withdrawal_table.csv; "
              + _POINT)
_MORTALITY = ("{{file}}: mort_table.csv must give a rate at the point's sex and its "
              "attained age in the first month it is on the books; it does not at point_id "
              "{points}")


def _says(template, points, **names):
    """``template``'s message for ``points``, its ``{file}`` left for the case's file."""
    return template.format(points=points, **names)


def _year_open_moved(point, column, by):
    """An edit that moves ``column``, a fixed account, and the account value it is part of.

    The fixed account at the valuation date, or at the anniversary, is part of the account
    value at the same instant, and off an anniversary the indexed account, the one less
    the other, is flat, so a fixed account moved alone would break that rule too.  So the
    account value at the same instant, ``av_pp_init`` or ``av_pp_prev_anniv_init``, moves
    by ``by`` with it, and only the rule under test sees the move.
    """
    whole = "av_pp_prev_anniv_init" if "prev_anniv" in column else "av_pp_init"
    return _both(_plus(column, [point], by), _plus(whole, [point], by))


def _no_state_value(column):
    """A value of ``column`` that passes every check before the no-state rule."""
    return {"payout_rate_locked_prev_anniv_init": 0.04, "phase_prev_anniv_init": 1,
            "index_level_prev_anniv_init": 1000.0}.get(column, 100.0)


def _anniversary_less(point, amount):
    """Row ``point``'s fixed account and account value at the valuation date, each its
    anniversary value less ``amount``: off an anniversary, the indexed account still flat.
    """
    def edit(table):
        fixed = table.at[point, "av_fixed_pp_prev_anniv_init"] - amount
        whole = table.at[point, "av_pp_prev_anniv_init"] - amount
        return _cells(point, av_fixed_pp_init=fixed, av_pp_init=whole)(table)
    return edit


def _in_first_year(point, month, **columns):
    """Row 15, the pre-exercise programme at policy month 6, moved to ``month``.

    It holds the issue values Data requires in the first policy year, so the move breaks
    no rule, and then ``columns`` alone are set.
    """
    return _cells(point, duration_mth=month, **columns)


def _moved_by(point, month, column, by):
    """An edit that moves row ``point`` to month ``month`` and its ``column`` by ``by``."""
    return _both(_set("duration_mth", [point], month), _plus(column, [point], by))


def _in_first_year_fixed(table, point, month, accrued):
    """The columns that move row ``point`` of ``table`` to ``month`` of its first year.

    Its values at the anniversary become its issue values, which Data requires there: the
    account value ``premium x (1 + bonus_rate)``, the fixed account its share of it, and
    the benefit and rollup bases the premium.  Entering month 0 its fixed account has
    ``accrued`` more, and its account value with it, so the indexed account is flat, as
    between anniversaries.
    """
    issued = table.at[point, "premium"] * (1.0 + table.at[point, "bonus_rate"])
    fixed = (1.0 - table.at[point, "alloc_indexed"]) * issued
    return {"duration_mth": month, "av_pp_prev_anniv_init": issued,
            "av_fixed_pp_prev_anniv_init": fixed, "av_pp_init": issued + accrued,
            "av_fixed_pp_init": fixed + accrued,
            "benefit_base_pp_init": table.at[point, "premium"],
            "rollup_base_pp_init": table.at[point, "premium"]}


def _at_first_anniversary(column, by):
    """Row 10, valued on its anniversary at 60, moved to the first anniversary, 12, and
    ``column`` moved by ``by``: unmoved, the row reads there, no first-year rule holding."""
    def edit(table):
        return _cells(10, duration_mth=12, **{column: table.at[10, column] + by})(table)
    return edit


# The cases whose fault no rule can be the only one to refuse, each refused by the rule
# whose message it asserts, and, with that rule dropped, by the second named here, so that
# each pins the order of the two: a blank or a text duration_mth, before the scenario's and
# the mortality's joins, which read the point's first month on the books from it; an issue
# age of 39.5 or written as text, before the mortality's join; an account value written as
# text, before the rule that holds the indexed account flat mid-year, and a negative one at
# the anniversary before that rule too, and before the rules that it is above 0 in ACCUM and
# INCOME and holds the fixed account; an index level written as text, before the rule that
# it is above 0 in force; a phase written as text or fractional, before the rule of the
# phases in force; the fixed account at either instant on new business, before the rule that
# it is part of the account value; income without the rider, before the rule that the
# rider's columns are 0 without it; a lifetime withdrawal and a payout rate without the
# rider, each before the rule that it is 0 in ACCUM; and an unknown scenario on an
# anniversary, before the rule that the index level there is the scenario's.  Within a rule
# that checks its columns in turn, each column has a case of its own, refused at that
# column, so that a column dropped from the rule fails: the five of the first policy year,
# the four of the rider and of DEPLETED, and the twelve of a policy not yet in force.  The
# DEPLETED cases take amounts within the cent the rules of the fixed account allow, so
# that the DEPLETED rule, which is exact, refuses them alone, two of them on row 14 moved
# five months off its anniversary, where its anniversary values need not equal those
# entering month 0; and the fixed account's rule has a case at each of its two instants,
# the anniversary's on row 17 with the whole account value fixed entering month 0, so that
# the indexed account still moves by less than three cents.
MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[12]].assign(policy_id="FIA-900099")]),
     "{file}: point_id [12] appears more than once"),
    ("a negative count", _set("policy_count", [11], -0.1), _says(_COUNT, [11])),
    ("a blank count", _set("policy_count", [12], float("nan")), _says(_COUNT, [12])),
    ("a text count", _set("policy_count", [13], "abc"), _says(_COUNT, [13])),
    ("an infinite count", _set("policy_count", [17], float("inf")), _says(_COUNT, [17])),
    ("two bad counts", _set("policy_count", [10, 14], -1.0), _says(_COUNT, [10, 14])),
    ("a fractional duration", _set("duration_mth", [1], 84.5), _says(_DURATION, [1])),
    ("a blank duration", _set("duration_mth", [18], float("nan")), _says(_DURATION, [18])),
    ("a text duration", _set("duration_mth", [11], "x95"), _says(_DURATION, [11])),
    ("a fractional issue age", _set("age_at_entry", [2], 62.5),
     _says(_YEARS, [2], column="age_at_entry")),
    ("an issue age of 39.5", _set("age_at_entry", [2], 39.5),
     _says(_YEARS, [2], column="age_at_entry")),
    ("a text issue age", _set("age_at_entry", [12], "x62"),
     _says(_YEARS, [12], column="age_at_entry")),
    ("a fractional income start age", _set("income_start_age", [9], 70.5),
     _says(_YEARS, [9], column="income_start_age")),
    ("a fractional joint age", _set("joint_age", [5], 60.5), _says(_JOINT, [5])),
    ("a negative joint age", _set("joint_age", [12], -1), _says(_JOINT, [12])),
    ("issued beyond the horizon", _set("duration_mth", [18], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [18]"),
    ("a blank rider flag", _set("glwb_elected", [2], float("nan")), _says(_ELECTED, [2])),
    ("a rider flag written as text", _set("glwb_elected", [4], "yes"),
     _says(_ELECTED, [4])),
    ("a negative premium", _set("premium", [2], -1.0),
     _says(_NUMBER, [2], column="premium")),
    ("a blank bonus", _set("bonus_rate", [4], float("nan")),
     _says(_NUMBER, [4], column="bonus_rate")),
    ("a negative utilization", _set("utilization_intensity", [7], -0.5),
     _says(_NUMBER, [7], column="utilization_intensity")),
    ("a blank cap", _set("cap_rate", [1], float("nan")),
     _says(_NUMBER, [1], column="cap_rate")),
    ("a stack written as text", _set("stack_factor", [3], "1.5x"),
     _says(_NUMBER, [3], column="stack_factor")),
    ("an infinite credit factor", _set("av_int_factor", [4], float("inf")),
     _says(_NUMBER, [4], column="av_int_factor")),
    ("an allocation above 1", _set("alloc_indexed", [4], 1.2), _says(_ALLOC, [4])),
    ("an issue yield of -100%", _set("mva_ref_yield_at_issue", [2], -1.0),
     _says(_I0, [2])),
    ("an account value written as text", _set("av_pp_init", [12], "x"),
     _says(_NUMBER, [12], column="av_pp_init")),
    ("a negative fixed account",
     _both(_year_open_moved(12, "av_fixed_pp_init", -1.0),
           _year_open_moved(12, "av_fixed_pp_prev_anniv_init", -1.0)),
     _says(_NUMBER, [12], column="av_fixed_pp_init")),
    ("a negative anniversary account value", _set("av_pp_prev_anniv_init", [12], -5.0),
     _says(_NUMBER, [12], column="av_pp_prev_anniv_init")),
    ("a negative anniversary fixed account",
     _year_open_moved(12, "av_fixed_pp_prev_anniv_init", -1.0),
     _says(_NUMBER, [12], column="av_fixed_pp_prev_anniv_init")),
    ("an infinite benefit base", _set("benefit_base_pp_init", [13], float("inf")),
     _says(_NUMBER, [13], column="benefit_base_pp_init")),
    ("a negative rollup base", _set("rollup_base_pp_init", [12], -1.0),
     _says(_NUMBER, [12], column="rollup_base_pp_init")),
    ("a negative floor", _set("mgsv_pp_init", [11], -1.0),
     _says(_NUMBER, [11], column="mgsv_pp_init")),
    ("an infinite lifetime withdrawal", _set("lw_pp_init", [12], float("inf")),
     _says(_NUMBER, [12], column="lw_pp_init")),
    ("negative withdrawals to date", _set("wd_cum_pp_init", [12], -1.0),
     _says(_NUMBER, [12], column="wd_cum_pp_init")),
    ("a payout rate above 1", _set("payout_rate_locked_prev_anniv_init", [12], 1.5),
     _says(_PAYOUT, [12])),
    ("an infinite index level", _set("index_level_prev_anniv_init", [11], float("inf")),
     _says(_LEVEL, [11])),
    ("an index level written as text", _set("index_level_prev_anniv_init", [11], "x"),
     _says(_LEVEL, [11])),
    ("a phase written as text", _set("phase_prev_anniv_init", [13], "INCOME"),
     _says(_CODE, [13])),
    ("a fractional phase", _set("phase_prev_anniv_init", [13], 2.5), _says(_CODE, [13])),
    *[(f"{column} on new business", _set(column, [2], _no_state_value(column)),
       _says(_NO_STATE, [2], column=column))
      for column in STATE],
    *[(f"{column} on future business", _set(column, [18], _no_state_value(column)),
       _says(_NO_STATE, [18], column=column))
      for column in ("lw_pp_init", "phase_prev_anniv_init")],
    ("lw_pp_init on future business issued at the horizon",
     _cells(18, duration_mth=-120, lw_pp_init=_no_state_value("lw_pp_init")),
     _says(_NO_STATE, [18], column="lw_pp_init")),
    ("TERMINATED in force", _set("phase_prev_anniv_init", [13], 4),
     _says(_IN_FORCE_PHASE, [13])),
    ("no phase in force", _set("phase_prev_anniv_init", [11], 0),
     _says(_IN_FORCE_PHASE, [11])),
    ("an index level of 0 in force", _set("index_level_prev_anniv_init", [11], 0.0),
     _says(_IN_FORCE_LEVEL, [11])),
    ("income without the rider",
     _cells(12, glwb_elected=False, benefit_base_pp_init=0.0, rollup_base_pp_init=0.0),
     _says(_RIDER_INCOME, [12])),
    ("a benefit base without the rider", _set("benefit_base_pp_init", [16], 100.0),
     _says(_NO_RIDER, [16], column="benefit_base_pp_init")),
    ("a rollup base without the rider", _set("rollup_base_pp_init", [16], 100.0),
     _says(_NO_RIDER, [16], column="rollup_base_pp_init")),
    ("a lifetime withdrawal without the rider", _set("lw_pp_init", [16], 5.0),
     _says(_NO_RIDER, [16], column="lw_pp_init")),
    ("a payout rate without the rider",
     _set("payout_rate_locked_prev_anniv_init", [16], 0.05),
     _says(_NO_RIDER, [16], column="payout_rate_locked_prev_anniv_init")),
    ("no benefit base under the rider", _set("benefit_base_pp_init", [10], 0.0),
     _says(_RIDER_BASE, [10])),
    ("no benefit base under the rider, DEPLETED", _set("benefit_base_pp_init", [14], 0.0),
     _says(_RIDER_BASE, [14])),
    ("a lifetime withdrawal in ACCUM", _set("lw_pp_init", [10], 5.0),
     _says(_ACCUM, [10], column="lw_pp_init")),
    ("a payout rate in ACCUM", _set("payout_rate_locked_prev_anniv_init", [10], 0.05),
     _says(_ACCUM, [10], column="payout_rate_locked_prev_anniv_init")),
    *[(f"{what} in {phase}, point {point}", _set(column, [point], 0.0),
       _says(_INCOME, [point]))
      for point, phase in ((12, "INCOME"), (14, "DEPLETED"))
      for what, column in (("no lifetime withdrawal on a locked rate", "lw_pp_init"),
                           ("a lifetime withdrawal on no locked rate",
                            "payout_rate_locked_prev_anniv_init"))],
    ("no lifetime withdrawal on a locked rate mid-year in INCOME, with a fixed account",
     _set("lw_pp_init", [17], 0.0), _says(_INCOME, [17])),
    ("an account value in DEPLETED",
     _cells(14, av_pp_init=5.0, av_pp_prev_anniv_init=5.0),
     _says(_DEPLETED, [14], column="av_pp_init")),
    ("a fixed account of half a cent in DEPLETED",
     _cells(14, av_fixed_pp_init=0.005, av_fixed_pp_prev_anniv_init=0.005),
     _says(_DEPLETED, [14], column="av_fixed_pp_init")),
    ("an anniversary account value of 2 cents in DEPLETED, mid-year",
     _cells(14, duration_mth=245, av_pp_prev_anniv_init=0.02),
     _says(_DEPLETED, [14], column="av_pp_prev_anniv_init")),
    ("an anniversary fixed account of half a cent in DEPLETED, mid-year",
     _cells(14, duration_mth=245, av_fixed_pp_prev_anniv_init=0.005),
     _says(_DEPLETED, [14], column="av_fixed_pp_prev_anniv_init")),
    ("no account value in INCOME", _cells(12, av_pp_init=0.0, av_pp_prev_anniv_init=0.0),
     _says(_YEAR_OPEN_AV, [12])),
    ("no account value in ACCUM", _cells(11, av_pp_init=0.0, av_pp_prev_anniv_init=0.0),
     _says(_YEAR_OPEN_AV, [11])),
    ("a fixed account above the account value",
     _cells(10, av_fixed_pp_init=200000.0, av_fixed_pp_prev_anniv_init=200000.0),
     _says(_FIXED_PART, [10], part="av_fixed_pp_init", whole="av_pp_init")),
    ("a fixed account 1.1 cents above the account value",
     lambda t: _cells(10, av_fixed_pp_init=t.at[10, "av_pp_init"] + 0.011,
                      av_fixed_pp_prev_anniv_init=t.at[10, "av_pp_init"] + 0.011)(t),
     _says(_FIXED_PART, [10], part="av_fixed_pp_init", whole="av_pp_init")),
    ("an anniversary fixed account 2 cents above its account value, mid-year",
     lambda t: _cells(17, av_fixed_pp_init=t.at[17, "av_pp_init"],
                      av_fixed_pp_prev_anniv_init=t.at[17, "av_pp_prev_anniv_init"]
                      + 0.02)(t),
     _says(_FIXED_PART, [17], part="av_fixed_pp_prev_anniv_init",
           whole="av_pp_prev_anniv_init")),
    ("an anniversary fixed account 1.1 cents above its account value, mid-year",
     lambda t: _cells(17, av_fixed_pp_init=t.at[17, "av_pp_init"],
                      av_fixed_pp_prev_anniv_init=t.at[17, "av_pp_prev_anniv_init"]
                      + 0.011)(t),
     _says(_FIXED_PART, [17], part="av_fixed_pp_prev_anniv_init",
           whole="av_pp_prev_anniv_init")),
    *[(f"an account value at the anniversary off its issue value, month {month}",
       _in_first_year(15, month, av_pp_init=100000.0, av_pp_prev_anniv_init=100000.0),
       _says(_FIRST_YEAR, [15], column="av_pp_prev_anniv_init"))
      for month in (1, 11)],
    ("an issue account value 1.1 cents off in the first policy year",
     _both(_plus("av_pp_init", [15], 0.011), _plus("av_pp_prev_anniv_init", [15], 0.011)),
     _says(_FIRST_YEAR, [15], column="av_pp_prev_anniv_init")),
    ("an issue account value 1.1 cents under in the first policy year",
     _both(_plus("av_pp_init", [15], -0.011),
           _plus("av_pp_prev_anniv_init", [15], -0.011)),
     _says(_FIRST_YEAR, [15], column="av_pp_prev_anniv_init")),
    ("a benefit base off the premium in the first policy year",
     _cells(15, benefit_base_pp_init=100.0, rollup_base_pp_init=100.0),
     _says(_FIRST_YEAR, [15], column="benefit_base_pp_init")),
    ("a fixed account off its issue share in the first policy year",
     _cells(15, av_fixed_pp_init=100.0, av_fixed_pp_prev_anniv_init=100.0),
     _says(_FIRST_YEAR, [15], column="av_fixed_pp_prev_anniv_init")),
    ("a rollup base off the premium in the first policy year",
     _set("rollup_base_pp_init", [15], 50000.0),
     _says(_FIRST_YEAR, [15], column="rollup_base_pp_init")),
    ("withdrawals to date in the first policy year", _set("wd_cum_pp_init", [15], 50.0),
     _says(_FIRST_YEAR, [15], column="wd_cum_pp_init")),
    *[(f"income in the first policy year, month {month}",
       _in_first_year(15, month, phase_prev_anniv_init=2, lw_pp_init=1.0,
                      payout_rate_locked_prev_anniv_init=0.05),
       _says(_FIRST_PHASE, [15]))
      for month in (1, 11)],
    ("an anniversary account value apart from the one entering month 0",
     _set("av_pp_prev_anniv_init", [10], 110000.0),
     _says(_ANNIVERSARY, [10], column="av_pp_prev_anniv_init", entering="av_pp_init")),
    ("an anniversary fixed account apart from the one entering month 0",
     _set("av_fixed_pp_prev_anniv_init", [10], 18000.0),
     _says(_ANNIVERSARY, [10], column="av_fixed_pp_prev_anniv_init",
           entering="av_fixed_pp_init")),
    *[(f"an anniversary {what} half a cent apart at the first anniversary",
       _at_first_anniversary(column, 0.005),
       _says(_ANNIVERSARY, [10], column=column, entering=entering))
      for what, column, entering in (
          ("account value", "av_pp_prev_anniv_init", "av_pp_init"),
          ("fixed account", "av_fixed_pp_prev_anniv_init", "av_fixed_pp_init"))],
    ("a stale year-open account value mid-year",
     _set("av_pp_prev_anniv_init", [12], 100000.0), _says(_INDEXED, [12])),
    ("the indexed account 3.1 cents off mid-year", _plus("av_pp_init", [17], 0.031),
     _says(_INDEXED, [17])),
    ("the indexed account 3.1 cents under mid-year", _plus("av_pp_init", [17], -0.031),
     _says(_INDEXED, [17])),
    *[(f"the indexed account 3.1 cents off at month {month}",
       _moved_by(point, month, "av_pp_init", 0.031), _says(_INDEXED, [point]))
      for point, month in ((15, 1), (15, 11), (17, 13))],
    ("the fixed account fallen a dollar mid-year", _anniversary_less(17, 1.0),
     _says(_FIXED_FALLEN, [17])),
    ("the fixed account fallen 1.1 cents mid-year", _anniversary_less(17, 0.011),
     _says(_FIXED_FALLEN, [17])),
    ("the fixed account fallen 1.1 cents at month 11",
     lambda t: _cells(10, **_in_first_year_fixed(t, 10, 11, -0.011))(t),
     _says(_FIXED_FALLEN, [10])),
    ("the fixed account fallen 1.1 cents at month 13",
     _both(_set("duration_mth", [17], 13), _anniversary_less(17, 0.011)),
     _says(_FIXED_FALLEN, [17])),
    ("an unknown scenario mid-year", _set("scenario_id", [11], "Worked-M95"),
     _says(_SCENARIO, [11])),
    ("a blank scenario", _set("scenario_id", [12], float("nan")), _says(_SCENARIO, [12])),
    ("an unknown scenario on an anniversary", _set("scenario_id", [1], "worked-M85"),
     _says(_SCENARIO, [1])),
    ("an anniversary index level apart from the scenario's",
     _set("index_level_prev_anniv_init", [10], 4999.0), _says(_ANNIVERSARY_LEVEL, [10])),
    ("an anniversary index level half a cent apart at the first anniversary",
     _at_first_anniversary("index_level_prev_anniv_init", 0.005),
     _says(_ANNIVERSARY_LEVEL, [10])),
    ("a rollup schedule the table lacks", _set("rollup_id", [3], "Simple"),
     _says(_ROLLUP, [3])),
    ("a programme the table lacks", _set("wd_schedule_id", [8], "Preexercise"),
     _says(_PROGRAMME, [8])),
    ("an issue age below the mortality table's first", _set("age_at_entry", [2], 39),
     _says(_MORTALITY, [2])),
    ("a sex the mortality table lacks", _set("sex", [2], "X"), _says(_MORTALITY, [2])),
    ("an attained age past the mortality table's last", _set("age_at_entry", [16], 63),
     _says(_MORTALITY, [16])),
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """Every table of :data:`MALFORMED`, each a file of its own, beside one model folder.

    Returns ``(folder, {case: filename})``.  Each case reads the model afresh and points
    ``Data.model_point_file`` at its own file before the model computes anything (a
    Reference set after a Space has computed does not reach a compiled model), so the
    files share one copy of the product directory, and no read.
    """
    root = tmp_path_factory.mktemp("malformed")
    files = {}
    folder = None
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"malformed_{number:03d}_sec.csv"
        folder = temp_inputs(root, model_path(SEC), model_points=edit(_committed()),
                             model_point_file=files[case])
    return folder, files


def _file_key(model, table, label):
    """The ``Projection`` key of row ``label`` of ``table``, a table the model may refuse.

    A refused table gives no ``point_keys``, so the key is taken from the file, the way
    ``run_sec.py`` takes one: the row's position on a model indexed by position, and its
    label otherwise.
    """
    if model.Projection.parameters == ("idx",):
        return list(table.index).index(label)
    return label


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(malformed, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5).

    And a projection meets the same refusal: the base ``Projection``'s default point and
    the first point of the file each read the table through their model point, and raise
    the table's own message, so that no point projects from a table the model refuses,
    compiled or not.  Each case is refused by the one rule it is built for; a case named
    that breaks two by its nature, listed above the table, is refused by the earlier
    rule, with its message.
    """
    folder, files = malformed
    model = _read(folder, "malformed", data={"model_point_file": files[case]})
    try:
        text = message.format(file=files[case])
        _refused(model.Data.model_point_table, text)
        _refused(model.Projection.result_cf, text)
        table = pd.read_csv(folder.parent / files[case], index_col="point_id")
        _refused(model.Projection[_file_key(model, table, table.index[0])].result_cf, text)
    finally:
        model.close()


# The six assumption tables, each with the Data Reference naming its file and the cell that
# checks it, which is the only way the projection reads the table (Data's docstring).
CHECKED = {"mort_table.csv": ("mort_table_file", "mort_rates"),
           "surr_charge_table.csv": ("surr_charge_file", "surr_charge_scale"),
           "rollup_table.csv": ("rollup_file", "rollup_steps"),
           "payout_rate_table.csv": ("payout_rate_file", "payout_rates"),
           COMPANION: ("rate_scenario_file", "rate_scenario_steps"),
           "withdrawal_table.csv": ("withdrawal_file", "wd_schedules")}


def _cell(column, row, value):
    """An edit of a plain table that writes ``value`` into ``column`` at row ``row``.

    ``row`` is the position among the data rows, so the file's line is ``row + 2``, its
    header line 1.  The column is made ``object`` first, so that text can go in.
    """
    def edit(table):
        table = table.assign(**{column: table[column].astype(object)})
        table.loc[row, column] = value
        return table
    return edit


def _drop_row(row):
    """An edit of a plain table that leaves out data row ``row``."""
    return lambda table: table.drop(index=row).reset_index(drop=True)


def _append(*values):
    """An edit of a plain table that adds a row of ``values`` at its end."""
    def edit(table):
        return pd.concat([table, pd.DataFrame([values], columns=table.columns)],
                         ignore_index=True)
    return edit


def _line(source, **cells):
    """The file line, 2 for the first data row, of the one row of ``source`` with
    ``cells``."""
    table = pd.read_csv(model_path(SEC).parent / source)
    hit = table.index[(table[list(cells)] == pd.Series(cells)).all(axis=1)].tolist()
    assert len(hit) == 1, (source, cells, hit)
    return hit[0] + 2


# The lines a row appended to the companion, the withdrawal table, the mortality and the
# surrender scale takes, and the line of the pre-exercise programme's one withdrawal,
# which such a row repeats.
_LAST_SCENARIO_LINE = len(_companion()) + 2
_LAST_WD_LINE = len(pd.read_csv(model_path(SEC).parent / "withdrawal_table.csv")) + 2
_LAST_MORT_LINE = len(pd.read_csv(model_path(SEC).parent / "mort_table.csv")) + 2
_LAST_SURR_LINE = len(pd.read_csv(model_path(SEC).parent / "surr_charge_table.csv")) + 2
_PREEXERCISE_LINE = _line("withdrawal_table.csv", wd_schedule_id="preexercise")

# The rules whose message lists every fault it finds after it: each repeated key with its
# lines, each key or span missing, and each payout band that ends below its start.
_AGES = "{file}: the ages of each sex must run one row an age, without a gap or a repeat"
_YEARS_RUN = ("{file}: the contract years must run from 1, one row a year, without a gap "
              "or a repeat")
_BANDS = ("{file}: the bands must run one after another, each from its age_lo to its "
          "age_hi, without a gap or an overlap")

# Each assumption table with one fault: (case, file, edit, message, S point).  The message
# names the faulty file by {file}, the column and the file's lines; the S point is a twin
# whose projection reads the table: the anchor issued at the valuation date, which
# reaches the payout bands at its exercise in month 95 and reads the surrender scale from
# month 0.  The model point table joins the mortality, rollup, scenario and withdrawal
# tables, so a projection meets those faults as the table is read.  In every table a key
# written as text is refused, and each value a cap, a floor, a min or a max reads, blank,
# text or infinite; then a key out of its range, a blank text key, a repeated key, and
# keys that leave a gap where the projection reads every year or age between the first and
# the last, the message naming each repeated key with its lines and each key or span
# missing, a single one and a span of several, and two faults in one table together.
TABLE_FAULTS = [
    ("mortality, an age written as text", "mort_table.csv", _cell("age", 42, "61x"),
     "{file}: age must be a whole number; it is not on line [44]", 2),
    ("mortality, a blank sex", "mort_table.csv", _cell("sex", 0, None),
     "{file}: sex must not be blank; it is on line [2]", 2),
    ("mortality, a blank rate", "mort_table.csv", _cell("mort_rate", 3, None),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [5]", 2),
    ("mortality, a rate written as text", "mort_table.csv", _cell("mort_rate", 4, "x"),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [6]", 2),
    ("mortality, an infinite rate", "mort_table.csv",
     _cell("mort_rate", 5, float("inf")),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [7]", 2),
    ("mortality, a rate above 1", "mort_table.csv", _cell("mort_rate", 3, 1.5),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [5]", 2),
    ("mortality, a male age missing", "mort_table.csv", _drop_row(60),
     f"{_AGES}; no line holds sex M age 70", 2),
    ("mortality, three male ages missing", "mort_table.csv",
     _both(_drop_row(64), _drop_row(62), _drop_row(60)),
     f"{_AGES}; no line holds sex M ages 70 to 72", 2),
    ("mortality, a male age repeated", "mort_table.csv", _append(61, "M", 0.5, "a test"),
     f"{_AGES}; sex M age 61 repeats on lines [44, {_LAST_MORT_LINE}]", 2),
    ("mortality, a female age missing and a male one repeated", "mort_table.csv",
     _both(_drop_row(61), _append(61, "M", 0.5, "a test")),
     f"{_AGES}; no line holds sex F age 70; sex M age 61 repeats on lines "
     f"[44, {_LAST_MORT_LINE - 1}]", 2),
    ("surrender charges, a contract year written as text", "surr_charge_table.csv",
     _cell("contract_year", 0, "1x"),
     "{file}: contract_year must be a whole number; it is not on line [2]", 2),
    ("surrender charges, a fractional contract year", "surr_charge_table.csv",
     _cell("contract_year", 6, 2.5),
     "{file}: contract_year must be a whole number; it is not on line [8]", 2),
    ("surrender charges, 9 for 9%", "surr_charge_table.csv",
     _cell("surr_charge_rate", 0, 9.0),
     "{file}: surr_charge_rate must be a number from 0 to 1; it is not on line [2]", 2),
    ("surrender charges, a vesting rate written as text", "surr_charge_table.csv",
     _cell("vest_rate", 2, "x"),
     "{file}: vest_rate must be a number from 0 to 1; it is not on line [4]", 2),
    ("surrender charges, a year missing", "surr_charge_table.csv", _drop_row(3),
     f"{_YEARS_RUN}; no line holds contract_year 4", 2),
    ("surrender charges, three years missing", "surr_charge_table.csv",
     _both(_drop_row(5), _drop_row(4), _drop_row(3)),
     f"{_YEARS_RUN}; no line holds contract_year 4 to 6", 2),
    ("surrender charges, a year repeated", "surr_charge_table.csv",
     _append(4, 0.07, 0.3, "a test"),
     f"{_YEARS_RUN}; contract_year 4 repeats on lines [5, {_LAST_SURR_LINE}]", 2),
    ("surrender charges, a year 0", "surr_charge_table.csv", _cell("contract_year", 0, 0),
     f"{_YEARS_RUN}; contract_year 0, below 1, is on lines [2]; no line holds "
     f"contract_year 1", 2),
    ("rollup, a contract year written as text", "rollup_table.csv",
     _cell("contract_year", 0, "x"),
     "{file}: contract_year must be a whole number, 1 or more; it is not on line [2]", 2),
    ("rollup, a contract year 0", "rollup_table.csv", _cell("contract_year", 0, 0),
     "{file}: contract_year must be a whole number, 1 or more; it is not on line [2]", 2),
    ("rollup, a blank schedule", "rollup_table.csv", _cell("rollup_id", 5, None),
     "{file}: rollup_id must not be blank; it is on line [7]", 2),
    ("rollup, a blank rate", "rollup_table.csv", _cell("rollup_rate", 0, None),
     "{file}: rollup_rate must be a number, zero or more; it is not on line [2]", 2),
    ("rollup, two rates in one year", "rollup_table.csv",
     _append("blended", 1, 0.06, "a second rate in year 1"),
     "{file}: a schedule must set one rate a year; one sets two on lines [2, 8]", 2),
    ("payout bands, an age written as text", "payout_rate_table.csv",
     _cell("age_lo", 0, "x"),
     "{file}: age_lo must be a whole number; it is not on line [2]", 2),
    ("payout bands, a fractional upper age", "payout_rate_table.csv",
     _cell("age_hi", 1, 59.5),
     "{file}: age_hi must be a whole number; it is not on line [3]", 2),
    ("payout bands, a blank rate", "payout_rate_table.csv",
     _cell("payout_rate_single", 1, None),
     "{file}: payout_rate_single must be a number from 0 to 1; it is not on line [3]", 2),
    ("payout bands, an infinite joint rate", "payout_rate_table.csv",
     _cell("payout_rate_joint", 2, float("inf")),
     "{file}: payout_rate_joint must be a number from 0 to 1; it is not on line [4]", 2),
    ("payout bands, two overlapping", "payout_rate_table.csv", _cell("age_lo", 1, 53),
     f"{_BANDS}; ages 53 to 54 are in the bands on lines [2, 3]", 2),
    ("payout bands, a gap between two", "payout_rate_table.csv", _cell("age_lo", 1, 56),
     f"{_BANDS}; no line holds age 55", 2),
    ("payout bands, a gap of two ages", "payout_rate_table.csv", _cell("age_lo", 1, 57),
     f"{_BANDS}; no line holds ages 55 to 56", 2),
    ("payout bands, one ending below its start", "payout_rate_table.csv",
     _cell("age_hi", 1, 52),
     f"{_BANDS}; the band on line 3 ends at age_hi 52, below its age_lo 55; no line holds "
     f"ages 55 to 59", 2),
    ("scenarios, a month written as text", COMPANION, _cell("t", 1, "x"),
     "{file}: t must be a whole number, 0 or more; it is not on line [3]", 2),
    ("scenarios, a negative month", COMPANION, _cell("t", 1, -12),
     "{file}: t must be a whole number, 0 or more; it is not on line [3]", 2),
    ("scenarios, a blank level", COMPANION, _cell("index_level", 1, None),
     "{file}: index_level must be a number above 0; it is not on line [3]", 2),
    ("scenarios, a yield written as text", COMPANION, _cell("mva_ref_yield", 1, "x"),
     "{file}: mva_ref_yield must be a number above -1; it is not on line [3]", 2),
    ("scenarios, a blank scenario", COMPANION, _cell("scenario_id", 2, None),
     "{file}: scenario_id must not be blank; it is on line [4]", 2),
    ("scenarios, two levels at one month", COMPANION,
     _append("worked", 0, 5100.0, 0.03, "a second level at t = 0"),
     f"{{file}}: a scenario must set one level a month; one sets two on lines "
     f"[2, {_LAST_SCENARIO_LINE}]", 2),
    ("withdrawals, a year written as text", "withdrawal_table.csv", _cell("t", 0, "x"),
     "{file}: t must be a whole number, 0 or more; it is not on line [2]", 2),
    ("withdrawals, a blank programme", "withdrawal_table.csv",
     _cell("wd_schedule_id", 0, None),
     "{file}: wd_schedule_id must not be blank; it is on line [2]", 2),
    ("withdrawals, a blank amount", "withdrawal_table.csv", _cell("wd_amount", 1, None),
     "{file}: wd_amount must be a number, zero or more; it is not on line [3]", 2),
    ("withdrawals, two in one year", "withdrawal_table.csv",
     _append("preexercise", 2, 1000.0, "a second withdrawal in one year"),
     f"{{file}}: a programme must withdraw once a year at most; one withdraws twice on "
     f"lines [{_PREEXERCISE_LINE}, {_LAST_WD_LINE}]", 2),
]


@pytest.fixture(scope="module")
def malformed_tables(tmp_path_factory):
    """Every table of :data:`TABLE_FAULTS`, each a file of its own beside one model folder.

    Returns ``(folder, {case: filename})``.  Each file is the shipped table with the case's
    fault, written as plain CSV under the table's name and a number, so that each case
    points the table's Reference at its own file before the model computes anything, as
    the malformed fixture does with the model point table.
    """
    root = tmp_path_factory.mktemp("malformed_tables")
    folder = temp_inputs(root, model_path(SEC))
    files = {}
    for number, (case, source, edit, _, _) in enumerate(TABLE_FAULTS):
        files[case] = f"{source[:-4]}_fault_{number:02d}.csv"
        edit(pd.read_csv(folder.parent / source)).to_csv(folder.parent / files[case],
                                                         index=False)
    return folder, files


@pytest.mark.parametrize("case, source, edit, message, s_point", TABLE_FAULTS,
                         ids=[c[0] for c in TABLE_FAULTS])
def test_an_assumption_table_whose_keys_cannot_be_read_is_refused(malformed_tables, case,
                                                                 source, edit, message,
                                                                 s_point):
    """The cell that checks the table refuses it, naming the file and the lines (T5).

    ``FIA_US_S`` reads each assumption table's keys and values as pandas reads them: one
    key written as text turns its column to text, and then a lookup raises an error that
    names no file, a rollup schedule or a withdrawal is silently missed, or, through
    ``int()``, a band of the payout table is misread; and a blank rate in a table a cap or
    a floor reads becomes a number, the cap's, without a word.  Here the table's checked
    cell, the one way the projection reads it, refuses the table, and so does a projection
    that reads it, the twin's ``result_cf()``, with the same message, before it reads a
    value from the table.  The twin's key is taken from the file (:func:`_file_key`): the
    model point table checks each point's keys against the scenarios, the rollup schedules,
    the withdrawals and the mortality, so it reads those four tables and is refused with
    them.
    """
    folder, files = malformed_tables
    reference, checked = CHECKED[source]
    committed = _committed()
    model = _read(folder, "table")
    try:
        setattr(model.Data, reference, files[case])
        text = message.format(file=files[case])
        _refused(model.Data.cells[checked], text)
        key = _file_key(model, committed, _label(committed, "twin", s_point, 0))
        _refused(model.Projection[key].result_cf, text)
    finally:
        model.close()


# Each text value no decode knows (T5, USLIB-SEC-PLAN.md §7.1, precised at M3): a column of
# the model point table, on the anchor issued at the valuation date, or a string Reference,
# set to a spelling FIA_US_S does not know, in S and in SEC alike, as (case, the columns,
# the References, the message).  Every decode of the column or Reference answers False for
# it, as each of FIA_US_S's comparisons does, and the cell that branches on the decodes
# raises FIA_US_S's own message, where FIA_US_S raises it: the crediting method at the
# first anniversary's credit, the basis at the exercise's payout percentage, the step-up
# mode at the first anniversary, the rollup-base convention at the second, and the collar
# basis on the surrender value of month 0.  So a decode that answered an unknown value as
# one of the known, the last of a chain read as the fall-through, fails here.
UNDECODABLE = [
    ("a crediting method", {"credit_method": "Cap"}, {}, "invalid credit_method"),
    ("a rider basis", {"glwb_basis": "Joint"}, {}, "invalid glwb_basis"),
    ("a step-up mode", {}, {"step_up_mode": "Annual"}, "invalid step_up_mode"),
    ("a rollup-base convention", {}, {"rb_wd_convention": "pro rata"},
     "invalid rb_wd_convention"),
    ("an MVA collar basis", {}, {"mva_collar_basis": "Gross"},
     "invalid mva_collar_basis"),
]

# And each value the two columns' decodes name, upper-cased and with a space before it,
# which FIA_US_S's exact comparisons refuse as they refuse any other text, so that a
# decode that folded case or stripped space, and so took a value S refuses, fails here
# (USLIB-SEC-PLAN.md §7.3, *For M17 and later*, item 2).  Stage EC decodes the columns in
# Data, element by element, and the compiled refusal test runs every case again.
DECODED = {"credit_method": ("cap", "par", "par_cap", "spread", "trigger"),
           "glwb_basis": ("single", "joint")}
UNDECODABLE += [(f"{column} {variant!r}", {column: variant}, {}, f"invalid {column}")
                for column, values in DECODED.items() for value in values
                for variant in (value.upper(), " " + value)]


@pytest.mark.parametrize("case, columns, refs, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_a_text_value_no_decode_knows_raises_s_message(tmp_path, case, columns, refs,
                                                       message):
    """An unknown text value raises ``FIA_US_S``'s message in both models, through a
    projection.

    S point 2 and its twin are each read from a copy holding the case's columns, on a model
    read afresh with the case's References set before it computes anything, and each
    projection raises ``ValueError`` with ``FIA_US_S``'s message, matched whole: the line
    that names the error is the same in both.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    committed = _committed()
    label = _label(committed, "twin", 2, 0)
    s_folder = temp_inputs(tmp_path / "s", model_path(TWIN),
                           model_points=_cells(2, **columns)(s_table))
    s = _read(s_folder, "undecodable_s", refs)
    sec = _read(_sec_inputs(tmp_path / "sec", _cells(label, **columns)(committed)),
                "undecodable", refs)
    try:
        for model, point_id in ((s, 2), (sec, label)):
            with pytest.raises(Exception) as excinfo:
                _point(model, point_id).result_cf()
            assert _raised(excinfo.value) == f"ValueError: {message}", (model.name, case)
    finally:
        sec.close()
        s.close()


def test_a_points_scenario_must_set_its_levels_by_its_first_month_on_the_books(tmp_path):
    """A scenario may start after ``t = 0``, but not after a point that runs on it starts.

    The scenario is a step function of the valuation month, and a point reads it from the
    first month it is on the books, ``t = 0`` or its issue month if later, so the companion
    holds, for the anchor issued 15 months on, ``worked-F15``, a copy of its path that sets
    no level before month 15.  That copy, cut to start at 16, is refused for that point,
    by ``Data`` and by its projection, where the scenario's lookup would find no level and
    raise naming no file; moved to start at 15, as committed, it projects its frame, reading
    its first level in its issue month.  And ``worked-M95``, the copy of the anchor valued
    at 95, cut to start at 1, is refused for that point, on the books from ``t = 0``.  Each
    table is read on a model of its own.
    """
    committed = _committed()
    future = _label(committed, "future", 2, -15)
    mid_year = _label(committed, "derived", 1, 95)

    def starting(scenario, month):
        """The companion with ``scenario``'s first level at ``month``: the levels before it
        dropped, but for the one in force there, which moves to ``month``."""
        def edit(table):
            mine = table["scenario_id"] == scenario
            before = table.index[mine & (table["t"] < month)]
            moved = before[-1:] if not (mine & (table["t"] == month)).any() else before[:0]
            table = table.drop(index=before.difference(moved)).copy()
            table.loc[moved, "t"] = month
            return table
        return {COMPANION: edit}

    for scenario, month, refused in (("worked-F15", 16, future),
                                     ("worked-F15", 15, None),
                                     ("worked-M95", 1, mid_year)):
        folder = _sec_inputs(tmp_path / f"{scenario}_{month}", committed,
                             starting(scenario, month))
        model = _read(folder, "scenario")
        try:
            if refused is None:
                assert len(model.Data.model_point_table()) == len(committed)
                p = _point(model, future)
                assert p.index_level(0) == 5000.0 and len(p.result_cf()) == 723
                assert np.isfinite(p.result_cf().to_numpy()).all()
            else:
                text = _says(_SCENARIO, [refused]).replace("{file}", TABLE)
                _refused(model.Data.model_point_table, text)
                _refused(model.Projection[_file_key(model, committed, refused)].result_cf,
                         text)
        finally:
            model.close()


def test_table_keys_written_as_floats_are_read_by_value(sec_model, tmp_path):
    """A key written ``1.0`` is the whole number it holds, in every table, as in S.

    On a copy whose six assumption tables carry every integer key as a float, the age, the
    contract year, the band's ages and the months, and whose model point table carries
    ``duration_mth``, the issue age, the income start age, the joint age and the phase code
    as floats, the anchor issued at the valuation date, the pre-exercise programme, joint
    income in force mid-year and the fixed account in income project exactly what the
    committed model projects, which together read all six tables and every integer column.
    Each integer column is read back as the int the clocks and the codes count in.
    """
    def floats(*columns):
        return lambda table: table.assign(**{c: table[c].astype(float) for c in columns})

    edits = {"mort_table.csv": floats("age"),
             "surr_charge_table.csv": floats("contract_year"),
             "rollup_table.csv": floats("contract_year"),
             "payout_rate_table.csv": floats("age_lo", "age_hi"),
             COMPANION: floats("t"), "withdrawal_table.csv": floats("t")}
    table = floats("duration_mth", "age_at_entry", "income_start_age", "joint_age",
                   "phase_prev_anniv_init")(_committed())
    model = _read(_sec_inputs(tmp_path, table, edits), "floats")
    try:
        written = pd.read_csv(tmp_path / "payout_rate_table.csv")
        assert written["age_lo"].dtype == float
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == read["phase_prev_anniv_init"].dtype == float
        for case in (("twin", 2, 0), ("twin", 8, 0), ("derived", 5, 150),
                     ("derived", 4, 100)):
            mine, base = _row(model, *case), _row(sec_model, *case)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](), rtol=0,
                                        atol=0) == [], (case, report)
            for cell in ("duration_mth_init", "age_at_entry", "income_start_age",
                         "joint_age", "phase_prev_anniv_init"):
                value = mine.cells[cell]()
                assert type(value) is int and value == base.cells[cell](), (case, cell)
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a contract issued later than it; 0 refuses all.

    The committed table's one future point is issued 15 months on.  It reads at the
    shipped 120 months and at 15, the shortest horizon that admits it, and is refused at
    14, by name, and at 15 it projects its 723 months.  At 0 the model takes no future new
    business, D4's fallback for a product that cannot support it, and the message says so.
    A negative horizon is itself refused, even on a table holding only contracts in force,
    which no horizon could refuse.  Each value is set on a model read afresh, before it
    computes anything.
    """
    committed = _committed()
    future = _label(committed, "future", 2, -15)
    later = (f"{TABLE}: duration_mth must be -14 or more, a policy issued at most 14 "
             f"months after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    negative = "future_horizon_mth must be 0 months or more, not -1"
    folder = _sec_inputs(tmp_path / "all", committed)
    in_force = _sec_inputs(tmp_path / "in_force", committed[committed["duration_mth"] > 0])
    for where, horizon, refusal in ((folder, None, None), (folder, 15, None),
                                    (folder, 14, later), (folder, 0, no_future),
                                    (in_force, -1, negative)):
        data = {} if horizon is None else {"future_horizon_mth": horizon}
        model = _read(where, "horizon", data=data)
        try:
            if horizon is None:
                assert model.Data.future_horizon_mth == 120
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(committed), horizon
            else:
                _refused(model.Data.model_point_table, refusal)
            if horizon == 15:
                assert len(_point(model, future).result_cf()) == 723
        finally:
            model.close()


def _beyond_120(table):
    """The mortality table extended to age 121 by a distinct rate per sex, for a test.

    A point whose cover has ended is refused where its frame is defined, ``proj_len()``,
    but at the shipped ``maturity_age`` such a point is aged 121 in its first month on the
    books, and the mortality's join refuses it first.  With a rate at 121 the table reads,
    and ``proj_len()`` is what refuses the point.
    """
    rows = [{"age": 121, "sex": sex, "mort_rate": rate, "provenance": "a test"}
            for sex, rate in (("M", 0.75), ("F", 0.7))]
    return pd.concat([table, pd.DataFrame(rows)], ignore_index=True)


def _mortality_from(first):
    """An edit that adds both sexes' rates from age ``first`` to 39, each its own.

    Geometric in age, distinct by sex, so that a read of the age beside the right one, or
    of the other sex's, which a padded array allows, changes a number C4 sees.
    """
    def edit(table):
        rows = [{"age": a, "sex": sex, "mort_rate": base * 1.09 ** (a - first),
                 "provenance": "test copy"}
                for sex, base in (("M", 0.00031), ("F", 0.00023)) for a in range(first, 40)]
        return pd.concat([pd.DataFrame(rows), table], ignore_index=True)
    return edit


def _female_to(last):
    """An edit that drops every female rate past age ``last``."""
    return lambda table: table[(table["sex"] != "F") | (table["age"] <= last)]


# proj_len()'s refusals (T5), each a case of its own: (case, the row as (kind, S point,
# month), the columns changed on it, the Projection References set on the model read
# afresh, the input tables edited, and the message, or None where the point projects).
# Whether a point is in cover is a rule of the product, not of the table: it needs
# maturity_age, a Projection Reference, so the table reads, and the point is refused where
# its frame is defined, on its first projection, rather than projecting nothing.  With
# maturity_age lowered to 100, the anchor depleted at 240 moved on to 468, the month its
# cover then ends, is refused, and the anchor issued at 101, past the age the contract
# matures at, is refused as a contract with no cover at all, which at the shipped 120
# projects, as issued at 100 it projects its one year of cover, the age just outside that
# window (§5.2, T5, precised at M10).  At the shipped 120, on a copy whose mortality reads
# at 121 (_beyond_120), the last policy year's point moved on to 708 is refused likewise,
# and moved on to 707, its last covered month, projects that month.  The three cases issued
# at 100 or 101 raise issue_age_max to 121 (stage EC): at the product's 80 proj_len
# refuses each first, as above issue_age_max, and the rule each holds is the cover's.  And
# the three bounds the compiled caches are sized from, each refused by proj_len() and each
# projected once its Reference admits the point (stage EC): the anchor issued at 39, below
# issue_age_min, on a mortality that reads at 39 (_mortality_from), so that the table
# reads; issued at 81, above issue_age_max; and female, on a mortality whose female rates
# stop at 119, below maturity_age, which Data cannot read, and which projects once
# maturity_age is 119: no committed point is female, so the table reads.  Every
# table is the committed one relabeled 100 + point_id and written in reverse order
# (_relabeled), so that the label a refusal names is no position.
NOT_ISSUED = [
    ("in force at a lowered maturity", ("derived", 2, 240), {"duration_mth": 468},
     {"maturity_age": 100}, {},
     "point_id {label}: duration_mth 468 is at or past maturity, policy month 468"),
    ("issued past a lowered maturity_age", ("twin", 2, 0), {"age_at_entry": 101},
     {"maturity_age": 100, "issue_age_max": 121}, {},
     "point_id {label}: age_at_entry 101 is past maturity_age 100: the contract has no "
     "cover"),
    ("issued at a lowered maturity_age", ("twin", 2, 0), {"age_at_entry": 100},
     {"maturity_age": 100, "issue_age_max": 121}, {}, None),
    ("issued at 101 under the shipped maturity_age", ("twin", 2, 0), {"age_at_entry": 101},
     {"issue_age_max": 121}, {}, None),
    ("in force at the shipped maturity", ("derived", 6, 696), {"duration_mth": 708}, {},
     {"mort_table.csv": _beyond_120},
     "point_id {label}: duration_mth 708 is at or past maturity, policy month 708"),
    ("in its last covered month under the shipped maturity", ("derived", 6, 696),
     {"duration_mth": 707}, {}, {"mort_table.csv": _beyond_120}, None),
    ("issued below issue_age_min", ("twin", 2, 0), {"age_at_entry": 39}, {},
     {"mort_table.csv": _mortality_from(39)},
     "point_id {label}: issue age 39 is below issue_age_min, 40"),
    ("issued at a lowered issue_age_min", ("twin", 2, 0), {"age_at_entry": 39},
     {"issue_age_min": 39}, {"mort_table.csv": _mortality_from(39)}, None),
    ("issued above issue_age_max", ("twin", 2, 0), {"age_at_entry": 81}, {}, {},
     "point_id {label}: issue age 81 is above issue_age_max, 80"),
    ("issued at a raised issue_age_max", ("twin", 2, 0), {"age_at_entry": 81},
     {"issue_age_max": 81}, {}, None),
    ("on mortality that stops at 119", ("twin", 2, 0), {"sex": "F"}, {},
     {"mort_table.csv": _female_to(119)},
     "point_id {label}: the mortality table gives no rate at attained age 120, the age "
     "the last contract year is entered at"),
    ("on mortality that stops at 119, maturing at 119", ("twin", 2, 0), {"sex": "F"},
     {"maturity_age": 119}, {"mort_table.csv": _female_to(119)}, None),
]


@pytest.mark.parametrize("case, row, columns, refs, inputs, message", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path, case, row, columns, refs,
                                                       inputs, message):
    """A point whose cover has ended, or that has none, has no frame: ``proj_len()`` says.

    Each case of :data:`NOT_ISSUED` is read on a model of its own, its References set
    before the model computes anything: the table reads, and the point's projection
    raises ``ValueError`` naming it, the message matched whole, or, where the case is one
    the rule admits, projects its frame, every number finite.
    """
    committed = _committed()
    label = 100 + _label(committed, *row)
    table = _cells(label, **columns)(_relabeled(committed))
    model = _read(_sec_inputs(tmp_path, table, inputs), "past", refs=refs)
    try:
        assert len(model.Data.model_point_table()) == len(committed)
        p = _point(model, label)
        if message is None:
            frame = p.result_cf()
            assert len(frame) == p.proj_len() > 0 and np.isfinite(frame.to_numpy()).all()
        else:
            with pytest.raises(Exception) as excinfo:
                p.result_cf()
            assert _raised(excinfo.value) == "ValueError: " + message.format(label=label)
    finally:
        model.close()



# The three References whose rate is the base of a power less 1, (case, References, the
# cell that takes the power and its arguments, the refusal, and what FIA_US_S does).  A
# rate below -1 gives the power a negative base: Python's power is then a complex number,
# which S projects as complex cash flows or refuses with a TypeError at the next max,
# and C's pow, which the compiled model calls, is NaN, which that max would answer 0 to.
# So SEC refuses each at the cell that takes the power, naming the point and the
# Reference, in both engines; at exactly -1 the base is 0, and both engines project as S
# does (M21, a refusal S lacks).
NEGATIVE_BASES = [
    ("fixed_rate_min and fixed_rate below -1", {"fixed_rate_min": -1.5, "fixed_rate": -1.5},
     ("fixed_interest_pp", (0,)),
     "point_id {label}: the fixed rate in force, fixed_rate_min or fixed_rate, must be -1 "
     "or more, not -1.5", "TypeError"),
    ("mgsv_rate below -1", {"mgsv_rate": -1.5}, ("mgsv_pp", (0,)),
     "point_id {label}: mgsv_rate must be -1 or more, not -1.5", "TypeError"),
    ("inflation_rate below -1", {"inflation_rate": -1.5}, ("inflation_factor", (0,)),
     "point_id {label}: inflation_rate must be -1 or more, not -1.5", "complex"),
]
AT_MINUS_ONE = [{"fixed_rate_min": -1.0, "fixed_rate": -1.0}, {"mgsv_rate": -1.0},
                {"inflation_rate": -1.0}]


def _s_did(s_point, refs):
    """What ``FIA_US_S``'s ``result_cf()`` does on ``s_point`` under ``refs``."""
    s = _read(model_path(TWIN), "s_base", refs)
    try:
        frame = _point(s, s_point).result_cf()
        return "complex" if any(frame[c].dtype.kind == "c" for c in frame) else frame
    except Exception as err:                    # what S raised, recorded
        return _raised(err).split(":")[0]
    finally:
        s.close()


def test_a_rate_below_minus_one_that_a_power_takes_is_refused_naming_it():
    """A Reference rate below -1 under a power is refused at that power, naming it (M21).

    Each case of :data:`NEGATIVE_BASES` on the anchor issued at the valuation date: the
    cell that takes the power, and ``result_cf()``, raise ``ValueError`` naming the point
    and the Reference, where ``FIA_US_S`` raises ``TypeError`` or projects complex numbers,
    which no compiled double can hold; the compiled model is held to the same refusal by
    :func:`test_the_compiled_model_refuses_a_negative_power_base_as_modelx_does`.  At
    exactly -1, :data:`AT_MINUS_ONE`, the base is 0, and the point projects S's frame,
    every number finite.
    """
    found = []
    for case, refs, (cell, args), message, s_does in NEGATIVE_BASES:
        assert _s_did(2, refs) == s_does, case
        model = _read(model_path(SEC), "base", refs)
        try:
            p = _row(model, "twin", 2, 0)
            want = "ValueError: " + message.format(label=p.point_id())
            for call in (lambda: p.cells[cell](*args), p.result_cf):
                did = _modelx_did(call)
                if did != ("raised", want):
                    found.append(f"{case}: {did}")
        finally:
            model.close()
    for refs in AT_MINUS_ONE:
        theirs = _s_did(2, refs)
        model = _read(model_path(SEC), "minus_one", refs)
        try:
            mine = _row(model, "twin", 2, 0).result_cf()
            assert np.isfinite(mine.to_numpy()).all(), refs
            assert not frame_mismatches(theirs, mine), refs
        finally:
            model.close()
    assert not found, found


def _modelx_did(call):
    """``("ok", value)`` or ``("raised", "Type: message")``: what modelx did on ``call``."""
    try:
        return ("ok", call())
    except Exception as err:                    # what modelx raised is what compiled must
        return ("raised", _raised(err))


def _short_female_mortality(table):
    """The mortality table with the female rates held to ages 45 to 119 alone."""
    keep = (table["sex"] != "F") | ((table["age"] >= 45) & (table["age"] <= 119))
    return table[keep]


def test_each_sex_is_read_at_its_own_ages(tmp_path):
    """Each sex's mortality is read, and checked, at its own ages, not another's (M21).

    Every shipped sex runs from 40 to 120, so a reader or a check that took another sex's
    ages, or the table's, would pass on the shipped table.  Here the female rates run from
    45 to 119 alone (:func:`_short_female_mortality`), on a copy where the anchor issued
    at the valuation date is female and the derived row of point 2 at 240 male: the female
    point is refused by ``proj_len()``, which finds no female rate at 120, the age its last
    contract year is entered at, naming the point, and the male point projects; and on
    each, ``mort_rate_base_at`` is the rate ``FIA_US_S``'s reader holds at every age of its
    sex, and refuses every age outside them.  Data numbers the sexes F 1 and M 2, so
    ``proj_len()`` reading ``mort_age_lasts()[1]``, or the table's last age, in place of
    the point's own, fails here.
    """
    edits = {"mort_table.csv": _short_female_mortality}
    committed = _committed()
    female, male = _label(committed, "twin", 2, 0), _label(committed, "derived", 2, 240)
    table = _cells(female, sex="F")(committed)
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s_table = _cells(2, sex="F")(s_table)
    model = _read(_sec_inputs(tmp_path / "sec", table, edits), "sexes")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_table,
                          edits=edits), "s_sexes")
    try:
        f, m = _point(model, female), _point(model, male)
        assert _modelx_did(f.proj_len) == ("raised", (
            f"ValueError: point_id {female}: the mortality table gives no rate at attained "
            f"age 120, the age the last contract year is entered at"))
        assert m.proj_len() == 468 and np.isfinite(m.result_cf().to_numpy()).all()
        for p, sex, ages, s_point in ((f, "F", range(45, 120), 2), (m, "M", range(40, 121),
                                                                     None)):
            for a in range(0, 123):
                did = _modelx_did(lambda: p.mort_rate_base_at(a))
                if a in ages:
                    want = s.Data.mort_table().loc[(a, sex), "mort_rate"]
                    assert did == ("ok", float(want)), (sex, a)
                else:
                    assert did[0] == "raised" and "gives no rate" in did[1], (sex, a)
    finally:
        s.close()
        model.close()


def _late_rollup(table):
    """The rollup table with a schedule ``late`` whose first row is contract year 3."""
    rows = pd.DataFrame([{"rollup_id": "late", "contract_year": 3, "rollup_rate": 0.04},
                         {"rollup_id": "late", "contract_year": 9, "rollup_rate": 0.01}])
    return pd.concat([table, rows], ignore_index=True)


def test_a_rollup_schedule_that_starts_late_rolls_up_nothing_before_it(tmp_path):
    """A rollup schedule whose first row is after year 1 rolls up nothing before it (M21).

    Every shipped schedule starts at contract year 1, so an array step-filled from year 1
    with the first row's rate, rather than 0.0 before it, would pass on them.  Here a
    schedule ``late`` starts at year 3 (:func:`_late_rollup`), and the anchor issued at the
    valuation date reads it, in ``FIA_US_S`` and in SEC: ``rollup_rate_py`` is 0.0 at years
    1 and 2 and the first row's rate from year 3, ``rollup_rate`` is S's at every month of
    the frame, and the anchor's frame is S's.
    """
    edits = {"rollup_table.csv": _late_rollup}
    committed = _committed()
    label = _label(committed, "twin", 2, 0)
    table = _cells(label, rollup_id="late")(committed)
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s_table = _cells(2, rollup_id="late")(s_table)
    model = _read(_sec_inputs(tmp_path / "sec", table, edits), "late")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_table,
                          edits=edits), "s_late")
    try:
        mine, theirs = _point(model, label), _point(s, 2)
        assert [mine.rollup_rate(t) for t in range(708)] == [
            theirs.rollup_rate(t) for t in range(708)]
        assert mine.rollup_rate_py(1) == mine.rollup_rate_py(2) == 0.0
        assert mine.rollup_rate_py(3) == 0.04
        assert not frame_mismatches(theirs.result_cf(), mine.result_cf(),
                                    columns=[c for c in theirs.result_cf().columns
                                             if c not in INFLATED])
        assert not frame_mismatches(theirs.result_glwb(), mine.result_glwb())
    finally:
        s.close()
        model.close()


def _band_below(table):
    """The payout bands with a band of 0% from age -10 before the first."""
    first = pd.DataFrame([{"age_lo": -10, "age_hi": int(table["age_lo"].min()) - 1,
                           "payout_rate_single": 0.0, "payout_rate_joint": 0.0}])
    return pd.concat([first, table], ignore_index=True)


def _bands_lowered(table):
    """Every payout band 200 years lower, every age bound negative."""
    return table.assign(**{"age_lo": table["age_lo"] - 200,
                           "age_hi": table["age_hi"] - 200})


def _mortality_below(table):
    """The mortality table with both sexes' rates from age -3 to 39 added."""
    rows = pd.DataFrame([{"age": a, "sex": sex, "mort_rate": 0.0005}
                         for sex in ("M", "F") for a in range(-3, 40)])
    return pd.concat([rows, table], ignore_index=True)


def _mortality_far(table):
    """The mortality table with a sex no point is, at one age, 10**9."""
    return pd.concat([table, pd.DataFrame([{"age": 10 ** 9, "sex": "X",
                                            "mort_rate": 0.5}])], ignore_index=True)


# Age tables FIA_US_S projects on, which an array padded from age 0, or as wide as its
# largest age, would refuse or could not hold: (case, the edit, the S points it reads).
AGE_TABLES = [
    ("a payout band from age -10", "payout_rate_table.csv", _band_below, (2, 5)),
    ("every payout band negative", "payout_rate_table.csv", _bands_lowered, (2,)),
    ("mortality from age -3", "mort_table.csv", _mortality_below, (2,)),
    ("mortality to age 10**9", "mort_table.csv", _mortality_far, (2,)),
]


@pytest.mark.parametrize("case, name, edit, s_points", AGE_TABLES,
                         ids=[c[0] for c in AGE_TABLES])
def test_an_age_table_s_projects_on_is_read_wherever_its_ages_run(tmp_path, case, name,
                                                                  edit, s_points):
    """An age table ``FIA_US_S`` projects on is neither refused nor held whole (M21).

    The payout bands and the mortality are held in arrays indexed from the table's first
    age and held to ``Data.read_last_age``, the last a read reaches, so that a table with
    negative ages, which S projects, is not refused at load, and one whose ages run far
    past any read does not make an array as wide (:data:`AGE_TABLES`).  On each, every
    twin of the S points named projects S's frame, from S's own point on the same edit.
    """
    edits = {name: edit}
    model = _read(_sec_inputs(tmp_path / "sec", _committed(), edits), "ages")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), edits=edits), "s_ages")
    try:
        for s_point in s_points:
            mine, theirs = _row(model, "twin", s_point, 0), _point(s, s_point)
            for report in ("result_cf", "result_glwb"):
                keep = [c for c in theirs.cells[report]().columns if c not in INFLATED]
                assert not frame_mismatches(theirs.cells[report](), mine.cells[report](),
                                            columns=keep), (case, s_point, report)
    finally:
        s.close()
        model.close()


def test_run_sec_block_asks_every_point_for_its_frame_first(tmp_path):
    """``run_sec.py --block`` refuses a point past its cover before it prints anything.

    A loop over the block would meet such a point only when it reached it, after
    projecting the points before it, so the runner asks every point for its frame first:
    run beside :data:`NOT_ISSUED`'s table at the shipped maturity, the last policy year's
    point moved on to 708, it fails naming the point, and prints nothing before.
    """
    committed = _committed()
    last = 100 + _label(committed, "derived", 6, 696)
    folder = _sec_inputs(tmp_path, _set("duration_mth", [last], 708)(_relabeled(committed)),
                         {"mort_table.csv": _beyond_120})
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert (f"point_id {last}: duration_mth 708 is at or past maturity, policy month 708"
            in done.stderr.decode(errors="replace"))


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """What a contract in force can be is read: the edges each rule allows, and no more.

    Copies of committed rows, appended under ids of their own, each read and projected,
    every number of its frame finite:

    * the first policy year at both ends, the pre-exercise programme moved to policy
      months 1 and 11 on its issue values, and month 12, the second year, with the account
      value at the anniversary, the benefit base and the rollup base each apart from its
      issue value, which the first-year rule no longer requires;
    * the money rules a part of a cent inside their tolerance: the issue account value
      0.9 of a cent off in the first year, and 0.9 under; the fixed account 0.9 of a cent
      above the account value, at both instants on an anniversary and at the anniversary's
      alone mid-year; the indexed account 2.9 cents off mid-year, and 2.9 under, where 3.1
      is refused (the malformed table); and the fixed account 0.9 of a cent below its
      anniversary value, where 1.1 cents is refused;
    * an anniversary's exact rules just outside their window (§5.2, T5, precised at M10),
      either side of the first anniversary: the fixed account in income moved to month 13,
      and the fixed account in its first year's last month, 11, on its issue values with
      interest accrued since, each with its account value and fixed account at the
      anniversary apart from those entering month 0 and an index level apart from the one
      its scenario sets at ``t = 0``, which the anniversary rules refuse at month 12;
    * a blank joint age under the joint basis, which reads the issue age, as S does;
    * a count of 0, a point that projects zeros;
    * a lifetime withdrawal and a locked percentage of 0, in ``INCOME`` on the joint row
      and in ``DEPLETED`` on the anchor's row restated at 240: the states of a contract
      that exercised below the first age band or in a band at 0%, where both models lock
      0, before its account value is exhausted and after.  Each takes no withdrawal and
      pays no income at its next anniversary, where the depleted row it copies pays its
      own.

    Each copy's ``row_kind`` says what it is, which no formula reads, so the rows it copies
    are still found as the ones they are.  The committed table already holds a zero
    account value with the rider live, in DEPLETED, and the depleted test projects it.
    """
    committed = _committed()
    first, fixed_mid, fixed_anniv, joint, depleted = (
        _label(committed, "derived", s_point, month)
        for s_point, month in ((8, 6), (4, 100), (4, 60), (5, 150), (2, 240)))
    at = committed.at
    copies = {
        101: (first, {"duration_mth": 1}),
        102: (first, {"duration_mth": 11}),
        103: (first, {"duration_mth": 12, "av_pp_init": 110000.0,
                      "av_pp_prev_anniv_init": 110000.0, "benefit_base_pp_init": 101000.0,
                      "rollup_base_pp_init": 101000.0}),
        104: (first, {"av_pp_init": at[first, "av_pp_init"] + 0.009,
                      "av_pp_prev_anniv_init": at[first, "av_pp_prev_anniv_init"] + 0.009}),
        105: (fixed_anniv, {"av_fixed_pp_init": at[fixed_anniv, "av_pp_init"] + 0.009,
                            "av_fixed_pp_prev_anniv_init": at[fixed_anniv, "av_pp_init"]
                            + 0.009}),
        106: (fixed_mid, {"av_pp_init": at[fixed_mid, "av_pp_init"] + 0.029}),
        107: (fixed_mid, {"av_fixed_pp_init": at[fixed_mid, "av_fixed_pp_prev_anniv_init"]
                          - 0.009,
                          "av_pp_init": at[fixed_mid, "av_pp_prev_anniv_init"] - 0.009}),
        108: (joint, {"joint_age": float("nan")}),
        109: (joint, {"policy_count": 0.0}),
        110: (joint, {"lw_pp_init": 0.0, "payout_rate_locked_prev_anniv_init": 0.0}),
        111: (depleted, {"lw_pp_init": 0.0, "payout_rate_locked_prev_anniv_init": 0.0}),
        112: (first, {"av_pp_init": at[first, "av_pp_init"] - 0.009,
                      "av_pp_prev_anniv_init": at[first, "av_pp_prev_anniv_init"] - 0.009}),
        113: (fixed_mid, {"av_pp_init": at[fixed_mid, "av_pp_init"] - 0.029}),
        114: (fixed_mid, {"av_fixed_pp_init": at[fixed_mid, "av_pp_init"],
                          "av_fixed_pp_prev_anniv_init":
                          at[fixed_mid, "av_pp_prev_anniv_init"] + 0.009}),
        115: (fixed_mid, {"duration_mth": 13, "index_level_prev_anniv_init": 1700.0}),
        116: (fixed_anniv, {**_in_first_year_fixed(committed, fixed_anniv, 11, 10.0),
                            "index_level_prev_anniv_init": 1500.0}),
    }
    rows = [committed.loc[[row]].assign(**changes, row_kind="copy").set_axis([label])
            for label, (row, changes) in copies.items()]
    table = pd.concat([committed, *rows]).rename_axis("point_id")
    model = _read(_sec_inputs(tmp_path, table), "edges")
    try:
        assert list(model.Data.model_point_table().index) == list(table.index)
        for label in copies:
            p = _point(model, label)
            assert np.isfinite(p.result_cf().to_numpy()).all(), label
            _release(model, _key(model, label))
        assert [_point(model, label).policy_year(0) for label in (101, 102, 103)] == [
            1, 1, 2]
        for label, year in ((115, 2), (116, 1)):
            p = _point(model, label)
            assert p.policy_year(0) == year, label
            assert p.av_pp_prev_anniv_init() < p.av_pp_init(), label
            assert p.av_fixed_pp_prev_anniv_init() < p.av_fixed_pp_init(), label
        blank = _point(model, 108)
        assert blank.is_joint_basis() and blank.joint_age() == blank.age_at_entry() == 62
        assert blank.covered_age(0) == 62 + 150 // 12
        zero = _point(model, 109)
        assert (zero.result_cf() == 0.0).all().all()
        assert zero.av_pp(0) == _row(sec_model, "derived", 5, 150).av_pp(0)
        unpaid = _point(model, 110)
        assert unpaid.phase_open(5) == _code(unpaid, "INCOME") and unpaid.is_anniv(5)
        assert (unpaid.lw_pp(5), unpaid.wd_pp(5), unpaid.income_payments(5)) == (
            0.0, 0.0, 0.0)
        paid, unpaid = _point(model, depleted), _point(model, 111)
        assert paid.income_payments(11) > 0.0
        assert unpaid.phase_open(11) == _code(unpaid, "DEPLETED") and unpaid.is_anniv(11)
        assert (unpaid.lw_pp(11), unpaid.wd_pp(11), unpaid.income_payments(11)) == (
            0.0, 0.0, 0.0)
    finally:
        model.close()


def test_every_state_s_reaches_as_shipped_is_accepted_in_force(s_model, tmp_path):
    """At S's shipped References and inputs too, every state S reaches is accepted, but one.

    The states ``FIA_US_S`` reaches differ from the splice's here, on S's own scenarios,
    programmes and mortality, so the every-state test runs here too (§5.2, T5, precised at
    M9): each of S's nine points restated in force at the edges of its windows, or at
    every month after its entry with ``USLIB_SEC_FULL=1`` (:func:`_every_state_months`), is
    read by ``Data``, exactly and carried to the cent, and has a frame
    (:func:`_refused_in_force`), but a contract terminated, ``TERMINATED``, the overdraw's
    from policy month 228, which a table holding one is refused for, by name.
    """
    kept, terminated = _states_s_reaches(s_model)
    assert {point for point, _ in terminated} == {7}, terminated[:5]
    assert min(terminated) == (7, 228)
    assert {point for point, _ in kept} == set(s_model.Data.model_point_table().index)
    refused = _refused_in_force(s_model, kept, tmp_path / "every", {})
    assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
    _refused_by_name(s_model, terminated[0], tmp_path / "terminated", {})


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_tables_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` and its companion are what FIA_US_S generates today.

    Every row and column, the text cells, the twelve opening-state columns and every
    re-based scenario included: an edit to an S row or an S scenario the files copy or
    derive from, or to an S formula a row's state is read from, fails here until
    ``python tools/gen_sec_points.py FIA_US_SEC`` regenerates them, in the same commit.
    Text and integers compare exactly, and a float by its value, to 1e-12, because the text
    the writer picks for a computed float depends on the platform's parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# The words the generator composes ids and provenance from, beside S's keys and a month:
# FIA-000001-M95, FIA-000002-F15, worked-M84, "S point 1 (FIA-000001) restated in force at
# S month 95", "... issued 15 months after the valuation date".  A word outside this set
# in a generated text cell is one the generator added, which CLAUDE.md forbids.
TEMPLATE_WORDS = {"M", "F", "S", "point", "restated", "in", "force", "at", "month",
                  "months", "issued", "after", "the", "valuation", "date"}


def _composed(value, keys):
    """Whether ``value`` is ``keys`` and :data:`TEMPLATE_WORDS` with punctuation, alone."""
    rest = value
    for key in sorted(keys, key=len, reverse=True):
        rest = rest.replace(key, " ")
    return set(re.findall(r"[A-Za-z]+", rest)) <= TEMPLATE_WORDS and not re.search(
        r"\d", rest)


def test_generated_text_is_s_text_or_composed_from_s_keys():
    """Every text cell of both committed files is S's, or composed from S's keys (D8).

    ``CLAUDE.md`` holds every input file to naming no company or product, and the
    generator keeps to it by adding no word of its own.  So each text cell of
    ``model_point_table_sec.csv`` is its S row's text in the same column, or, with S's
    policy id, scenario id and point id and the row's month taken out, nothing but the
    template's words and punctuation: an id, a re-based scenario's id or a provenance.  And
    each row of the scenario companion is a level S's ``rate_scenario.csv`` sets, its
    provenance S's for that level, under S's scenario id or one composed from it and the
    month of a row of the table that reads it.  The test holds no list of names: what it
    holds is the template, and a word outside it fails.
    """
    s_dir = model_path(TWIN).parent
    s_table = pd.read_csv(s_dir / "model_point_table.csv", index_col="point_id")
    s_rows = {row["policy_id"]: {**row, "point_id": point_id}
              for point_id, row in s_table.to_dict("index").items()}
    rename = {"pols_if_init": "policy_count", **SPEC.column_map}
    s_column = {new: old for old, new in rename.items() if new is not None}
    table = _committed().reset_index()
    foreign = []
    for record in table.to_dict("records"):
        source = s_rows[record["source_policy_id"]]
        keys = (source["policy_id"], source["scenario_id"], str(abs(record["source_mth"])),
                str(source["point_id"]))
        for column, value in record.items():
            if not isinstance(value, str):
                continue
            if column == "row_kind" and value in ("twin", "derived", "future"):
                continue
            if source.get(s_column.get(column, column)) == value:
                continue
            if not _composed(value, keys):
                foreign.append((TABLE, record["point_id"], column, value))
    s_levels = pd.read_csv(s_dir / "rate_scenario.csv")
    said = {(r["scenario_id"], r["index_level"], r["mva_ref_yield"]): r["provenance"]
            for r in s_levels.to_dict("records")}
    readers = {}
    for record in table.to_dict("records"):
        source = s_rows[record["source_policy_id"]]
        readers.setdefault(record["scenario_id"], (source["scenario_id"],
                                                    str(abs(record["source_mth"]))))
    for record in _companion().to_dict("records"):
        scenario = record["scenario_id"]
        base, month = readers.get(scenario, (scenario, ""))
        if scenario != base and not _composed(scenario, (base, month)):
            foreign.append((COMPANION, scenario, "scenario_id", scenario))
        level = (base, record["index_level"], record["mva_ref_yield"])
        if said.get(level) != record["provenance"]:
            foreign.append((COMPANION, scenario, "provenance", record["provenance"]))
    assert not foreign, f"text the generator did not take from S: {foreign}"


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin issued at the valuation date the two coincide, and its contracts enter as
    new business at ``t = 0``.  S's anchor in force at anniversary 7 is in contract year
    8 at attained age 69 at ``t = 0``, with 624 months of cover left, to policy month 708,
    the anniversary at attained age 121 that closes the contract year entered at 120; it
    is on the books from the start, with no new business.  The anchor valued at 95 is in
    its contract year's last month, so the anniversary closing the year is ``t = 0`` and
    the one that opened it, policy month 84, is twelve months before the valuation date.
    The last policy year's point has a twelve-month frame.  The anchor issued 15 months on
    has nothing in force and nothing to do before ``t = 15``, and contract year -1, then
    0, before issue, which no schedule is read at.  ``result_cf_annual()`` keeps the
    months in cover alone: on the point valued at 95 its first contract year is the one
    month left of it, and on the point issued later the months before issue are no
    contract year.
    """
    twin = _row(sec_model, "twin", 2, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 707)] == [0, 1, 707]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.policy_id() == "FIA-000002"
    anchor = _row(sec_model, "twin", 1, 84)
    assert (anchor.duration_mth(0), anchor.policy_year(0), anchor.age(0)) == (84, 8, 69)
    assert (anchor.maturity_mth(), anchor.proj_len(), anchor.policy_id()) == (
        708, 624, "FIA-000001")
    assert anchor.is_active(623) and not anchor.is_active(624)
    assert anchor.pols_if_init() == anchor.policy_count() == anchor.pols_if(0) == 1.0
    assert [anchor.pols_new_biz(t) for t in range(624)] == [0.0] * 624
    last_month = _row(sec_model, "derived", 1, 95)
    assert (last_month.duration_mth(0), last_month.anniv_mth(0),
            last_month.year_open_mth(0)) == (95, 0, -12)
    assert last_month.is_anniv(0) and last_month.policy_id() == "FIA-000001-M95"
    last_year = _row(sec_model, "derived", 6, 696)
    assert (last_year.proj_len(), last_year.age(0), last_year.policy_year(0)) == (
        12, 120, 59)
    fut = _row(sec_model, "future", 2, -15)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-15, 15, 723)
    assert [fut.policy_year(t) for t in range(16)] == [-1] * 3 + [0] * 12 + [1]
    assert not fut.is_active(14) and fut.is_active(15)
    assert (fut.pols_if_init(), fut.pols_new_biz(15), fut.pols_if(15)) == (0.0, 1.0, 1.0)
    assert (fut.premiums(14), fut.premiums(15)) == (0.0, 100000.0)
    annual, monthly = last_month.result_cf_annual(), last_month.result_cf()
    assert list(annual.index[:2]) == [8, 9] and annual.index.name == "policy_year"
    assert annual.loc[8].tolist() == monthly.loc[0].tolist()
    assert annual.loc[9, "net_cf"] == pytest.approx(monthly.loc[1:12, "net_cf"].sum(),
                                                    rel=1e-12)
    assert annual.loc[9, "pols_if"] == monthly.loc[1, "pols_if"]
    assert list(fut.result_cf_annual().index[:2]) == [1, 2]


# The worked example's anniversary-8 cells, which test_fixed_indexed_annuity_us.py reads on
# S's point 1 at its policy month 95, each with its timing where it has one: on the twin
# of that point, in force 84 months at the valuation date, the same cells are read at
# t = 11.
WORKED_CELLS = (("index_return", ()), ("credit_rate", ()), ("index_credit_pp", ()),
                ("av_pp_at", ("BEF_FEE",)), ("rider_charge_pp", ()),
                ("av_pp_at", ("BEF_WD",)), ("rollup_pp", ()), ("stack_pp", ()),
                ("benefit_base_pp_at", ("BEF_STEP_UP",)),
                ("benefit_base_pp_at", ("BEF_WD",)),
                ("lw_pp_at", ("BEF_WD",)), ("free_wd_allow", ()), ("wd_excess_pp", ()),
                ("av_pp", ()), ("mgsv_pp", ()), ("benefit_base_pp", ()))


def test_the_opening_state_is_what_s_carries_into_the_valuation_month(sec_model, s_model):
    """Each committed in-force row opens with S's state at its month, and continues S.

    For each derived row, restated from S point ``p`` at its month ``d``, and for each twin
    of S's points in force at 84, each of the twelve opening-state columns is what the
    spec's extractor reads off S at ``d``, to 1e-12 relative, because a computed float may
    come back from the CSV within two ulps, and the row's scenario is S's re-based to
    ``d``.  Then the row is S's point from month ``d`` on, at the shipped assumptions, in
    every cell but those expense inflation moves (:func:`_continues_s`): the committed rows
    themselves are splices, on the shipped inputs and the committed companion, as T2's rows
    are on the splice's.  So the worked example's anniversary 8, S's month 95, is the
    twin's ``t = 11``, cell for cell (:data:`WORKED_CELLS`), exactly.
    """
    table = sec_model.Data.model_point_table()
    in_force = table[table["duration_mth"] > 0]
    assert sorted(in_force["row_kind"].value_counts().items()) == [("derived", 8),
                                                                   ("twin", 3)]
    s_table = s_model.Data.model_point_table()
    s_of = {policy: point_id for point_id, policy in s_table["policy_id"].items()}
    for point_id, row in in_force.iterrows():
        s, d = _point(s_model, s_of[row["source_policy_id"]]), int(row["source_mth"])
        p = _point(sec_model, point_id)
        assert p.duration_mth_init() == d, point_id
        for column, extract in SPEC.state.items():
            value = extract(s, d)
            if isinstance(value, str):
                assert p.scenario_id() == value, point_id
            else:
                assert p.cells[column]() == pytest.approx(value, rel=1e-12, abs=1e-12), (
                    point_id, column)
        found = _continues_s(s, p, d)
        assert not found, f"point {point_id}: " + "\n  ".join(found[:20])
    anchor, s1 = _row(sec_model, "twin", 1, 84), _point(s_model, 1)
    for cell, timing in WORKED_CELLS:
        codes_ = [_code(anchor, label) for label in timing]
        assert anchor.cells[cell](11, *codes_) == s1.cells[cell](95, *timing), cell
    assert anchor.av_pp(11) == pytest.approx(122865.84, abs=0.005)


def test_the_committed_future_row_is_s_anchor_15_months_on(sec_model, s_model):
    """The committed row issued 15 months on is S's anchor 15 months on, cell by cell.

    T6 holds the row to the generator only to 1e-12, and the block test holds it only in a
    sum beside two other rows, column by column of ``result_cf``.  So it is compared alone
    with its S point, the anchor, frame by frame, as T3 compares a future row on the
    splice's inputs (§7.1, *Precised at M3*, item 11, taken into FIA at M13, §5.4): SEC
    rows ``15 ..`` are S rows ``0 ..``, ending together, in ``result_cf`` and every column
    of ``result_pols`` S's has, and every cell of S's but T3's exemptions
    (:data:`FUTURE_EXEMPT`), at every argument S cached, moved 15 months later, to 1e-9
    relative with no absolute floor but on the residuals (:func:`_continues_s`).  The
    shipped 2.5% expense inflation runs from issue in S and from the valuation date here
    (D7), 15 months apart, so the two columns and the cells it moves are left out, as on
    the rows in force; the inflation test holds them.  Before issue the row holds T3's facts
    (:func:`_future_facts`): a row of zeros a month, ``PRE_ISSUE``, no decrement rate and
    no table read before the contract's first age, year or anniversary.
    """
    p, s2 = _row(sec_model, "future", 2, -15), _point(s_model, 2)
    assert p.duration_mth_init() == -15 and p.scenario_id() == f"{s2.scenario_id()}-F15"
    found = _continues_s(s2, p, -15, FUTURE_EXEMPT) + _future_facts(p, 15)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:20])


def test_each_opening_state_column_shows_on_a_committed_row(sec_model, tmp_path):
    """Each column, changed, changes what its committed row gives, where it is read.

    A column the projection never read, or read where another belongs, would pass every
    test that leaves the column as generated.  So each is changed on a copy of a committed
    row that reads it, appended to the committed table under an id of its own, with any
    column ``Data`` ties it to moved with it, so that the copy still reads, and the copy's
    months are asserted against the row's:

    * the account value entering month 0 and at the anniversary, on the fixed account
      valued on its anniversary, 60: each $1,000 more, the account value at ``t = 0`` is
      $1,000 more, and the free withdrawal at the anniversary closing the year, at
      ``t = 11``, 10% of the account value that opened it, $100 more;
    * the account value and the fixed account entering month 0, on the fixed account in
      income mid-year, 100: each $1,000 more, both close month 0 $1,000 and a month's
      fixed interest on it more, and the account value at the anniversary that opened the
      year is the row's, from its own column;
    * the account value at that anniversary, on the same row, $1,000 more with the account
      value entering month 0, the indexed account still flat: the year's base for the
      index credit and the free withdrawal at ``t = 7`` is $1,000 more;
    * the fixed account at that anniversary, $1,000 less with the account value there: the
      year's annual fixed interest at ``t = 7`` is the fixed rate on $1,000 less, and the
      free withdrawal on $1,000 less, and the index credit is the row's;
    * the benefit base, on joint income mid-year, 150: $10,000 more, the rider charge at its
      anniversary, ``t = 5``, is 0.95% of it more;
    * the rollup base, on S's simple rollup in force at 84: $10,000 more, the rollup at the
      exercise anniversary, ``t = 11``, is 3% of it more;
    * the Model #805 floor, on the anchor valued at 95: zeroed, the floor at ``t = 0``, its
      exercise anniversary, is 0 rather than the worked example's 84,605.80;
    * the lifetime withdrawal, on joint income mid-year: $1,000 more, it holds through
      month 0 and is withdrawn at ``t = 5``, $1,000 more than the row's;
    * the withdrawals to date: $1,000 more at ``t = 0``;
    * the locked payout rate: at 6% for the row's 4.7%, the lifetime withdrawal at ``t = 5``
      is 6% of the benefit base there;
    * the phase at the anniversary, on the anchor valued at 95, in its exercise year: in
      INCOME already, with a lifetime withdrawal and a locked rate as ``Data`` then
      requires, its anniversary at ``t = 0`` is no exercise, and neither rollup nor stack
      is credited there, where the row's rollup is the worked example's 5,000.00;
    * the index level at the anniversary that opened the year, on joint income mid-year:
      at 2,290 for the row's 2,015.71, the year's index return at ``t = 5`` is read on it,
      and its credit falls below the cap.
    """
    committed = _committed()
    p10, p12, p17 = (_label(committed, "derived", s_point, month)
                     for s_point, month in ((4, 60), (5, 150), (4, 100)))
    p11, p3 = _label(committed, "derived", 1, 95), _label(committed, "twin", 3, 84)
    at = committed.at
    copies = {
        "av": (p10, {"av_pp_init": at[p10, "av_pp_init"] + 1000.0,
                     "av_pp_prev_anniv_init": at[p10, "av_pp_prev_anniv_init"] + 1000.0}),
        "av_mid_year": (p17, {"av_pp_init": at[p17, "av_pp_init"] + 1000.0,
                              "av_fixed_pp_init": at[p17, "av_fixed_pp_init"] + 1000.0}),
        "av_year_open": (p17, {"av_pp_init": at[p17, "av_pp_init"] + 1000.0,
                               "av_pp_prev_anniv_init": at[p17, "av_pp_prev_anniv_init"]
                               + 1000.0}),
        "fixed_year_open": (p17, {
            "av_fixed_pp_prev_anniv_init": at[p17, "av_fixed_pp_prev_anniv_init"] - 1000.0,
            "av_pp_prev_anniv_init": at[p17, "av_pp_prev_anniv_init"] - 1000.0}),
        "benefit_base": (p12, {"benefit_base_pp_init": at[p12, "benefit_base_pp_init"]
                               + 10000.0}),
        "rollup_base": (p3, {"rollup_base_pp_init": at[p3, "rollup_base_pp_init"]
                             + 10000.0}),
        "floor": (p11, {"mgsv_pp_init": 0.0}),
        "lw": (p12, {"lw_pp_init": at[p12, "lw_pp_init"] + 1000.0}),
        "wd_cum": (p12, {"wd_cum_pp_init": at[p12, "wd_cum_pp_init"] + 1000.0}),
        "payout_rate": (p12, {"payout_rate_locked_prev_anniv_init": 0.06}),
        "phase": (p11, {"phase_prev_anniv_init": 2, "lw_pp_init": 9000.0,
                        "payout_rate_locked_prev_anniv_init": 0.052}),
        "index_level": (p12, {"index_level_prev_anniv_init": 2290.0}),
    }
    labels = {what: 100 + i for i, what in enumerate(copies, start=1)}
    rows = [committed.loc[[point]].assign(**changes).set_axis([labels[what]])
            for what, (point, changes) in copies.items()]
    model = _read(_sec_inputs(tmp_path, pd.concat([committed, *rows]).rename_axis(
        "point_id")), "shown")
    try:
        c = {what: _point(model, label) for what, label in labels.items()}
        r3, r10, r11, r12, r17 = (_point(sec_model, p) for p in (p3, p10, p11, p12, p17))
        monthly = (1.0 + r17.fixed_rate_in_force()) ** (1.0 / 12.0) - 1.0
        assert c["av"].av_pp(0) - r10.av_pp(0) == pytest.approx(1000.0, abs=1e-6)
        assert c["av"].free_wd_allow(11) - r10.free_wd_allow(11) == pytest.approx(
            100.0, abs=1e-6)
        mid = c["av_mid_year"]
        for cell in ("av_pp", "av_fixed_pp"):
            assert mid.cells[cell](0) - r17.cells[cell](0) == pytest.approx(
                1000.0 * (1.0 + monthly), abs=1e-6), cell
        assert mid.av_pp_year_open(0) == r17.av_pp_year_open(0)
        year_open = c["av_year_open"]
        assert year_open.av_pp_year_open(0) - r17.av_pp_year_open(0) == pytest.approx(
            1000.0, abs=1e-6)
        assert year_open.index_credit_pp(7) - r17.index_credit_pp(7) == pytest.approx(
            1000.0 * r17.credit_rate(7), abs=1e-6)
        assert year_open.free_wd_allow(7) - r17.free_wd_allow(7) == pytest.approx(
            100.0, abs=1e-6)
        fixed = c["fixed_year_open"]
        assert fixed.av_fixed_pp_year_open(0) - r17.av_fixed_pp_year_open(0) == (
            pytest.approx(-1000.0, abs=1e-6))
        assert fixed.fixed_interest_ann_pp(7) - r17.fixed_interest_ann_pp(7) == (
            pytest.approx(-1000.0 * r17.fixed_rate_in_force(), abs=1e-6))
        assert fixed.free_wd_allow(7) - r17.free_wd_allow(7) == pytest.approx(-100.0,
                                                                                abs=1e-6)
        assert fixed.index_credit_pp(7) == pytest.approx(r17.index_credit_pp(7), rel=1e-12)
        assert c["benefit_base"].rider_charge_pp(5) - r12.rider_charge_pp(5) == (
            pytest.approx(0.0095 * 10000.0, abs=1e-6))
        assert c["rollup_base"].rollup_pp(11) - r3.rollup_pp(11) == pytest.approx(
            0.03 * 10000.0, abs=1e-6)
        assert r11.mgsv_pp(0) == pytest.approx(84605.80, abs=0.005)
        assert c["floor"].mgsv_pp(0) == 0.0
        lw = c["lw"]
        assert _at(lw, "lw_pp_at", 0, "BEF_WD") - _at(r12, "lw_pp_at", 0, "BEF_WD") == (
            pytest.approx(1000.0, abs=1e-6))
        assert lw.wd_pp(5) - r12.wd_pp(5) == pytest.approx(1000.0, abs=1e-6)
        assert c["wd_cum"].wd_cum_pp(0) - r12.wd_cum_pp(0) == pytest.approx(1000.0,
                                                                            abs=1e-6)
        rate = c["payout_rate"]
        assert rate.payout_rate_locked(0) == 0.06 and r12.payout_rate_locked(0) == 0.047
        assert _at(rate, "lw_pp_at", 5, "BEF_WD") == pytest.approx(
            0.06 * _at(rate, "benefit_base_pp_at", 5, "BEF_WD"), rel=1e-12)
        assert _at(rate, "lw_pp_at", 5, "BEF_WD") > _at(r12, "lw_pp_at", 5, "BEF_WD")
        phase = c["phase"]
        assert r11.is_exercise(0) and not phase.is_exercise(0)
        assert phase.phase_year_open(0) == _code(phase, "INCOME")
        assert (r11.rollup_pp(0), phase.rollup_pp(0), phase.stack_pp(0)) == (
            pytest.approx(5000.0, abs=0.005), 0.0, 0.0)
        level = c["index_level"]
        assert level.index_return(5) == pytest.approx(
            level.index_level(level.duration(5) + 1) / 2290.0 - 1.0, rel=1e-12)
        assert 0.0 < level.credit_rate(5) < r12.credit_rate(5) == r12.cap_rate_in_force()
    finally:
        model.close()


def test_the_year_under_way_reads_its_opening_state(sec_model, sec_read):
    """The quantities of the contract year under way are its columns, then the frame's.

    A year-open quantity is read three ways: from its column where the year opened before
    the valuation date, from the frame where it opened on the books, and by the issue rule
    in the first year of a contract issued at or after the valuation date.  Joint income
    valued mid-year, 150, opens month 0 on its columns: the account value and the fixed
    account at the anniversary that opened the year, the phase, INCOME, the locked payout
    rate, the index level, the rollup base, the benefit base and the lifetime withdrawal,
    each read where its year opened, until the anniversary at ``t = 5``, from which the
    next year reads the frame.  Its account is wholly indexed, so its account value is
    flat between anniversaries, and the one entering month 0 would give the same numbers;
    the fixed account valued mid-year, 100, whose fixed interest accrues every month,
    reads its year's account value and fixed account from their anniversary columns, each
    apart from the one entering month 0, until the anniversary at ``t = 7``.  The fixed
    account valued on its anniversary, 60, reads the account value at the anniversary from
    its column, which ``Data`` holds equal to the one entering month 0, and the index level
    there from the scenario at ``t = 0``, which ``Data`` holds equal to its column: the
    sweep read that column nowhere.  The pre-exercise programme in its first policy year
    reads the issue values, which its columns hold.  And the anchor issued 15 months on
    opens its first year, in its issue month, on the issue rule: the premium and the
    bonus, a benefit base and a rollup base of the premium, ACCUM, no lifetime withdrawal
    and no payout rate.
    """
    unread = sec_read[1]["unread"]
    table = sec_model.Data.model_point_table()
    joint = _row(sec_model, "derived", 5, 150)
    for cell, column in (("av_pp_year_open", "av_pp_prev_anniv_init"),
                         ("av_fixed_pp_year_open", "av_fixed_pp_prev_anniv_init"),
                         ("payout_rate_locked", "payout_rate_locked_prev_anniv_init"),
                         ("phase_year_open", "phase_prev_anniv_init"),
                         ("rollup_base_pp_year_open", "rollup_base_pp_init")):
        assert [joint.cells[cell](t) for t in range(6)] == [joint.cells[column]()] * 6, cell
    assert joint.phase_year_open(0) == _code(joint, "INCOME")
    assert [_at(joint, "benefit_base_pp_at", t, "BEF_ROLLUP") for t in range(6)] == [
        joint.benefit_base_pp_init()] * 6
    assert [_at(joint, "lw_pp_at", t, "BEF_WD") for t in range(5)] == [
        joint.lw_pp_init()] * 5
    assert joint.index_level(joint.duration(0)) == joint.index_level_prev_anniv_init()
    assert joint.av_pp_year_open(6) == joint.av_pp(5)
    assert joint.phase_year_open(6) == joint.phase(5)
    assert "index_level_prev_anniv_init" not in unread[_label(table, "derived", 5, 150)]
    fixed_mid = _row(sec_model, "derived", 4, 100)
    for cell, column, entering in (
            ("av_pp_year_open", "av_pp_prev_anniv_init", "av_pp_init"),
            ("av_fixed_pp_year_open", "av_fixed_pp_prev_anniv_init", "av_fixed_pp_init")):
        assert [fixed_mid.cells[cell](t) for t in range(8)] == [
            fixed_mid.cells[column]()] * 8, cell
        assert fixed_mid.cells[column]() != fixed_mid.cells[entering](), column
    assert fixed_mid.av_pp_year_open(8) == fixed_mid.av_pp(7)
    on_anniv = _row(sec_model, "derived", 4, 60)
    assert on_anniv.av_pp_year_open(0) == on_anniv.av_pp_prev_anniv_init() == (
        on_anniv.av_pp_init())
    assert on_anniv.index_level(on_anniv.duration(0)) == (
        on_anniv.data.rate_scenario_steps().loc[(on_anniv.scenario_id(), 0),
                                                "index_level"])
    assert on_anniv.index_level(5) == on_anniv.index_level_prev_anniv_init()
    assert "index_level_prev_anniv_init" in unread[_label(table, "derived", 4, 60)]
    first = _row(sec_model, "derived", 8, 6)
    issue = first.premium_pp() * (1.0 + first.bonus_rate())
    assert first.av_pp_year_open(0) == first.av_pp_prev_anniv_init() == issue
    assert _at(first, "benefit_base_pp_at", 0, "BEF_ROLLUP") == first.premium_pp()
    fut = _row(sec_model, "future", 2, -15)
    assert fut.av_pp_year_open(15) == fut.prem_to_av_pp(15) == 107000.0
    assert fut.av_fixed_pp_year_open(15) == 0.0
    assert fut.phase_year_open(15) == _code(fut, "ACCUM")
    assert fut.rollup_base_pp_year_open(15) == 100000.0
    assert _at(fut, "benefit_base_pp_at", 15, "BEF_ROLLUP") == 100000.0
    assert (fut.payout_rate_locked(15), _at(fut, "lw_pp_at", 15, "BEF_WD")) == (0.0, 0.0)


def test_the_phase_is_a_code_and_the_report_keeps_its_labels(sec_model, s_model):
    """The phase is an int code from stage E; ``result_glwb()`` reports S's labels.

    The six References ``PRE_ISSUE`` to ``MATURED`` are 0 to 5, the order of
    :data:`PHASES`, the four ``sec_support`` maps S's strings onto are theirs, and
    ``sec_support.codes`` finds them: at stage E they were every code the model named,
    and at stage ``"EC"`` the timings, kinds, scenario columns and switches' settings
    are codes beside them, each named as S's string.  On every committed point every
    phase cell is an int at every month, the frame and the month after it, ``PRE_ISSUE``
    before issue and ``MATURED`` from maturity on, and ``result_glwb()`` labels each
    month with the label of its code.  On the anchor's twin the labels are S's phases,
    month for month.  And the opening phase is a column of whole numbers, read as such.
    """
    refs = sec_model.Projection.refs
    assert {label: refs[label] for label in PHASES} == {
        label: code for code, label in enumerate(PHASES)}
    assert _FIA_PHASE_CODES == {label: refs[label] for label in PHASES[1:5]}
    table = sec_model.Data.model_point_table()
    assert table["phase_prev_anniv_init"].dtype == "int64"
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        assert {label: codes(p)[label] for label in PHASES} == {
            label: refs[label] for label in PHASES}, point_id
        months = range(p.proj_len() + 1)
        for cell in ("phase", "phase_open", "phase_year_open"):
            assert {type(p.cells[cell](t)) for t in months} == {int}, (point_id, cell)
        labels = p.result_glwb()["phase"]
        assert list(labels) == [PHASES[p.phase(t)] for t in range(p.proj_len())], point_id
        assert p.phase(p.proj_len()) == _code(p, "MATURED"), point_id
        assert set(labels.iloc[:p.t_entry()]) <= {"PRE_ISSUE"}, point_id
    twin, s2 = _row(sec_model, "twin", 2, 0), _point(s_model, 2)
    assert list(twin.result_glwb()["phase"]) == [s2.phase(t) for t in range(708)]


def test_the_rate_scenario_runs_on_the_valuation_clock(sec_model):
    """The index level and the reference yield are read at the valuation month (D7).

    ``FIA_US_S`` keys its scenario by anniversary number from issue; this model reads
    anniversary ``y``'s level at the valuation month it falls in, ``12 y -
    duration_mth_init()``, from the companion, where each row's path is S's re-based to
    the month it is valued at.  The worked path steps at anniversary 8: S's anchor in force
    84 months reads that step at ``t = 12`` of its copy, the anchor issued at the valuation
    date at ``t = 96`` of S's own path, the anchor valued at 95 at ``t = 1`` of its copy,
    and the anchor issued 15 months on at ``t = 111``, each at its own policy month 96, and
    each credits the worked example's 9% index return at the anniversary closing contract
    year 8, the month before.  Every row's copy sets its first level in the first month the
    row is on the books, and none before.
    """
    steps = sec_model.Data.rate_scenario_steps()
    for case, month, step in ((("twin", 1, 84), 0, 12), (("twin", 2, 0), 0, 96),
                              (("derived", 1, 95), 0, 1), (("future", 2, -15), 15, 111)):
        p = _row(sec_model, *case)
        path = steps.loc[p.scenario_id()]
        assert path.index[0] == month == p.t_entry(), case
        assert path.loc[step, "index_level"] == 5450.0, case
        assert path.loc[step - 1 if step - 1 in path.index else month,
                        "index_level"] == 5000.0, case
        assert 12 * 8 - p.duration_mth_init() == step, case
        assert (p.index_level(7), p.index_level(8), p.mva_ref_yield(8)) == (
            5000.0, 5450.0, 0.035), case
        anniversary = step - 1
        assert p.duration_mth(anniversary) == 95 and p.is_anniv(anniversary), case
        assert p.index_return(anniversary) == pytest.approx(0.09, abs=1e-12), case
    table = sec_model.Data.model_point_table()
    for point_id, row in table.iterrows():
        first = steps.loc[row["scenario_id"]].index[0]
        assert first == max(0, -int(row["duration_mth"])), point_id


def test_withdrawals_stay_on_the_policy_clock(sec_model, tmp_path):
    """A withdrawal programme falls where the contract has it, however old the contract.

    *withdrawal_table.csv* is keyed by the completed contract years at the anniversary
    (D7): the pre-exercise programme's $60,000 at the anniversary closing contract year 3,
    policy month 35, falls at ``t = 35`` on its twin, at ``t = 29`` on the point valued in
    its first policy year at 6, and nowhere on the anchor, whose programme is none.  On
    those two the years completed at each anniversary are ``t // 12`` too, so the twin is
    also read issued 18 months on, from a copy of the table where it is a point of its own:
    there the $60,000 falls at ``t = 53``, where ``t // 12`` is 4.  It is withdrawn in
    accumulation, before exercise, on all three.
    """
    def scheduled(p):
        return [(t, p.wd_scheduled_pp(t)) for t in range(p.proj_len())
                if p.wd_scheduled_pp(t) != 0.0]

    def later(table):
        row = table.loc[[_label(table, "twin", 8, 0)]]
        row = row.assign(duration_mth=-18, row_kind="copy").set_axis([201])
        return pd.concat([table, row]).rename_axis("point_id")

    twin, first = _row(sec_model, "twin", 8, 0), _row(sec_model, "derived", 8, 6)
    assert scheduled(twin) == [(35, 60000.0)]
    assert scheduled(first) == [(29, 60000.0)]
    assert scheduled(_row(sec_model, "twin", 2, 0)) == []
    model = _read_edited(tmp_path, later, "later")
    try:
        issued_later = _point(model, 201)
        assert scheduled(issued_later) == [(53, 60000.0)]
        for p, t in ((twin, 35), (first, 29), (issued_later, 53)):
            assert p.duration_mth(t) == 35 and p.wd_pp(t) == 60000.0, t
            assert p.phase_open(t) == _code(p, "ACCUM"), t
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, on every committed point and in every month, ``expenses(t)`` is
    the acquisition, 6% of the premiums of the contracts issued that month, plus
    ``80 / 12 x 1.025 ** (t / 12)`` per contract in force, whatever the contract's age:
    ``FIA_US_S``'s formula, on ``t``.  So S's anchor in force 84 months pays S's
    month-``84 + t`` expenses deflated by ``1.025 ** 7``, the inflation S took from its
    issue to its entry, before the valuation date, and the anchor issued 15 months on is
    already ``1.025 ** (15 / 12)`` dearer at its issue; on a twin issued at the valuation
    date the two clocks give S's expenses in every month.  This is the only test that sees
    inflation on the valuation clock: the splice sets the rate to 0, and on a point issued
    at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        assert p.inflation_factor(0) == 1.0, point_id
        for t in range(p.proj_len()):
            want = (p.expense_acq_rate * p.premiums(t)
                    + p.expense_maint / 12 * (1 + INFLATION) ** (t / 12) * p.pols_if(t))
            assert p.expenses(t) == pytest.approx(want, rel=1e-12, abs=1e-12), (
                point_id, t)
    s1, s2 = _point(s_model, 1), _point(s_model, 2)
    anchor, twin = _row(sec_model, "twin", 1, 84), _row(sec_model, "twin", 2, 0)
    for t in range(anchor.proj_len()):
        assert anchor.expenses(t) == pytest.approx(
            s1.expenses(84 + t) / (1 + INFLATION) ** 7, rel=1e-12), t
    assert [twin.expenses(t) for t in range(708)] == pytest.approx(
        [s2.expenses(t) for t in range(708)], rel=1e-12)
    fut = _row(sec_model, "future", 2, -15)
    assert fut.inflation_factor(15) == pytest.approx(1.025 ** (15 / 12), rel=1e-15)


def test_acquisition_and_the_premium_fall_on_new_business_only(sec_model, tmp_path):
    """The premium, the bonus, the commission and acquisition, per contract issued.

    On every committed point the premium is ``premium x policy_count()`` in the issue
    month, ``t = -duration_mth``, the premium credited to the account value that and the
    bonus, and acquisition 6% of the premium, and each is 0 in every other month:
    ``t = 0`` on the twins issued at the valuation date, ``t = 15`` on the anchor issued 15
    months on, and never on a point already in force, though on the valuation clock its
    row 0 is ``t = 0``.  The commission and the premium tax ship at 0, so they are asserted
    on a model read afresh with ``comm_rate_acq`` at 5% and ``premium_tax_rate`` at 2%
    before it computes anything, from a copy whose twin and future anchor each count 2.5
    contracts: in the issue month the premium is 250,000, the acquisition 15,000, the
    commission 12,500 and the tax 5,000, and on the anchor in force each is 0 throughout.
    Every shipped point counts one contract, at which a charge per model point would pass.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        issue = -int(table.at[point_id, "duration_mth"])
        issued = [p.policy_count() if t == issue else 0.0 for t in range(p.proj_len())]
        assert [p.premiums(t) for t in range(p.proj_len())] == [
            p.premium_pp() * n for n in issued], point_id
        assert [p.prem_to_av(t) for t in range(p.proj_len())] == [
            p.premium_pp() * (1.0 + p.bonus_rate()) * n for n in issued], point_id
    committed = _committed()
    issued = [_label(committed, "twin", 2, 0), _label(committed, "future", 2, -15)]
    fresh = _read_edited(tmp_path, _set("policy_count", issued, 2.5), "acquisition",
                         refs={"comm_rate_acq": 0.05, "premium_tax_rate": 0.02})
    try:
        for case in (("twin", 2, 0), ("future", 2, -15), ("twin", 1, 84)):
            p = _row(fresh, *case)
            issue = -p.duration_mth_init()
            flows = [(p.premiums(t), p.commissions(t), p.premium_taxes(t),
                      p.expenses(t) - p.expense_maint / 12 * p.inflation_factor(t)
                      * p.pols_if(t)) for t in range(p.proj_len())]
            want = (250000.0, 12500.0, 5000.0, 15000.0)
            for t, flow in enumerate(flows):
                assert flow == pytest.approx(want if t == issue else (0.0,) * 4,
                                             abs=1e-9), (case, t)
    finally:
        fresh.close()


def test_lapse_reads_the_anniversary_closing_its_year(sec_model):
    """The lapse rate is the contract year's, read at the anniversary that closes it (R2).

    ``lapse_rate(t)`` reads the phase, and the moneyness factor the account value and the
    benefit base, at ``anniv_mth(t)``, the anniversary closing the contract year of ``t``,
    up to 11 months ahead: R2's one admitted read.  So on every committed point the rate is
    one number over each contract year in cover.  Joint income valued at 150 reads its
    moneyness at ``t = 5``, its anniversary, after the year's withdrawal, not at ``t = 0``.
    The overdraw valued at 216 terminates at its anniversary at ``t = 11``: the year's rate
    is 1.0, spread as no lapse until the anniversary month and every contract lapsing in
    it, after which nothing is in force.  And the anchor depleted at 240 never lapses.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.lapse_rate(t) == p.lapse_rate(p.anniv_mth(t)), (point_id, t)
    joint = _row(sec_model, "derived", 5, 150)
    assert joint.anniv_mth(0) == 5

    def moneyness(av, base):
        return min(1.0, max(joint.lapse_money_floor,
                            1.0 - joint.lapse_money_slope * max(0.0, base / av - 1.0)))

    assert joint.lapse_moneyness_factor(0) == moneyness(joint.av_pp(5),
                                                        joint.benefit_base_pp(5))
    assert joint.lapse_moneyness_factor(0) != moneyness(joint.av_pp(0),
                                                        joint.benefit_base_pp(0))
    overdraw = _row(sec_model, "derived", 7, 216)
    assert overdraw.phase(11) == _code(overdraw, "TERMINATED")
    assert [overdraw.lapse_rate(t) for t in range(12)] == [1.0] * 12
    assert [overdraw.lapse_rate_mth(t) for t in range(12)] == [0.0] * 11 + [1.0]
    assert overdraw.pols_lapse(11) == _at(overdraw, "pols_if_at", 11, "BEF_LAPSE") > 0.0
    assert overdraw.pols_if(12) == 0.0
    depleted = _row(sec_model, "derived", 2, 240)
    assert [depleted.lapse_rate(t) for t in range(depleted.proj_len())] == [0.0] * 468


def test_a_depleted_row_projects_its_whole_frame_at_a_zero_account_value(sec_model):
    """In force with no account value and the rider live, the income runs on (D6, M7).

    The anchor restated at 240 has exhausted its account value, its lifetime withdrawal
    still paid, so it opens DEPLETED on an account value of 0, which ``Data`` accepts for
    a contract whose rider pays on.  Its frame runs to the end of cover, 468 months, every
    number finite: every ratio over the account value, the moneyness factor, the share of
    the fixed account a withdrawal takes and the guarantee's reduction among them, is
    guarded.  It stays DEPLETED, its account value 0, no surrender value; the income is paid
    at each anniversary, the lifetime withdrawal on the contracts still in force; the
    moneyness factor sits at its floor, and no contract lapses.
    """
    p = _row(sec_model, "derived", 2, 240)
    assert p.proj_len() == 468 and p.av_pp_init() == 0.0
    for report in REPORTS:
        frame = p.cells[report]().select_dtypes("number")
        assert np.isfinite(frame.to_numpy()).all(), report
    depleted = _code(p, "DEPLETED")
    for t in range(468):
        assert p.phase(t) == depleted and p.av_pp(t) == 0.0, t
        assert p.surr_value_pp(t) == 0.0 and p.wd_reduction_rate(t) == 0.0, t
        assert p.lapse_moneyness_factor(t) == p.lapse_money_floor, t
        paid = p.income_payments(t)
        if p.is_anniv(t):
            assert paid == pytest.approx(p.lw_pp_init() * p.pols_if(t), rel=1e-12), t
        else:
            assert paid == 0.0, t
    assert p.income_payments(11) > 0.0


def test_each_keyed_reader_is_s_lookup_at_every_key(sec_model, s_model):
    """Each table is read through one cell keyed by an age, a year or a count, as S reads.

    ``FIA_US_S`` looks each table up inside its monthly cells; this model reads each
    through one keyed cell, from ``Data``'s checked copy, which is what Phase 2's caches are
    sized on.  At every key the contract can ask for, each returns what S's own lookup
    does: the payout percentage at every exercise age from 40 to 120 on both bases, against
    S's ``payout_rate``; the surrender charge and the vesting at every policy year of S's
    frame, against S's, and at each later year to 81, the youngest issue age's last, the
    table's last year's; each rollup schedule at every policy year S's frame reaches,
    against S's ``rollup_rate``; the mortality at every age of the table, a male point's
    against S's ``mort_table`` and ``Data``'s checked copy on both sexes; and the
    pre-exercise programme at every count of completed years in S's frame, against S's
    ``wd_scheduled_pp``.
    """
    single, joint = _row(sec_model, "twin", 2, 0), _row(sec_model, "twin", 5, 0)
    s2, s5 = _point(s_model, 2), _point(s_model, 5)
    for p, s_proj, basis in ((single, s2, "single"), (joint, s5, "joint")):
        assert [p.payout_rate_at(a) for a in range(40, 121)] == [
            s_proj.payout_rate(a, basis) for a in range(40, 121)], basis
    years = range(1, s2.proj_len() // 12 + 1)
    assert [single.surr_charge_rate_py(y) for y in years] == [
        s2.surr_charge_rate(12 * (y - 1)) for y in years]
    assert [single.vest_rate_py(y) for y in years] == [
        s2.vest_rate(12 * (y - 1)) for y in years]
    assert [single.surr_charge_rate_py(y) for y in range(60, 82)] == [0.0] * 22
    assert [single.vest_rate_py(y) for y in range(60, 82)] == [1.0] * 22
    for point_id in (2, 3, 4):
        p, s_proj = _row(sec_model, "twin", point_id, 84 if point_id == 3 else 0), (
            _point(s_model, point_id))
        first = s_proj.policy_year(s_proj.entry_mth())
        rollup = range(first, s_proj.proj_len() // 12 + 1)
        assert [p.rollup_rate_py(y) for y in rollup] == [
            s_proj.rollup_rate(12 * (y - 1)) for y in rollup], point_id
    rates = s_model.Data.mort_table()
    for sex, p in (("M", single), ("F", None)):
        if p is None:
            continue
        assert [p.mort_rate_base_at(x) for x in range(40, 121)] == [
            float(rates.loc[(x, sex), "mort_rate"]) for x in range(40, 121)], sex
    female = sec_model.Data.mort_rates()
    assert [float(female.loc[(x, "F"), "mort_rate"]) for x in range(40, 121)] == [
        float(rates.loc[(x, "F"), "mort_rate"]) for x in range(40, 121)]
    programme, s8 = _row(sec_model, "twin", 8, 0), _point(s_model, 8)
    counts = range(s8.proj_len() // 12)
    assert [programme.wd_scheduled_at(k) for k in counts] == [
        s8.wd_scheduled_pp(12 * k + 11) for k in counts]


def test_the_points_sum_row_by_row_into_a_block(sec_model, s_model):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The anchor issued at the valuation date, the anchor restated at 240 and the anchor
    issued 15 months on, summed as ``run_sec.py --block`` sums them, are indexed 0..722 and
    equal S's frame added to itself moved 240 months earlier and 15 months later, in every
    column but the two expense inflation moves (:data:`INFLATED`).  A model whose frames sat
    on the policy clock would fail it.  The committed rows are already swept, so it costs a
    sum.
    """
    cases = (("twin", 2, 0), ("derived", 2, 240), ("future", 2, -15))
    block = pd.concat([_row(sec_model, *case).result_cf() for case in cases]).groupby(
        level="t").sum()
    sdf = _point(s_model, 2).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 240).loc[0:],
                          sdf.set_axis(sdf.index + 15)]).groupby(level=0).sum()
    assert list(block.index) == list(range(723))
    keep = [c for c in sdf.columns if c not in INFLATED]
    assert frame_mismatches(expected, block, columns=keep, atol=0.0) == []


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

    The runner test and the extract test both read ``run_sec.py``'s default point, and an
    interpreter that reads the model and projects a point costs seconds.
    """
    runs = {}

    def run(*args):
        if args not in runs:
            runs[args] = _run_sec(model_path(SEC).parent / "run_sec.py", *args)
        return runs[args]
    return run


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path,
                                                                 committed_runs):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them.  Read without them,
    relabeled ``100 + point_id`` and written in reverse order, so that no label is its
    position, every point projects what the committed point it was made from projects, in
    ``result_cf`` and ``result_pols``, exactly.  On every shipped row ``source_mth`` equals
    ``duration_mth``, so a formula that read the one for the other would pass every test
    that leaves ``duration_mth`` as generated.  And ``run_sec.py``, run beside the extract,
    finds point 101 by its label and prints it without saying where it came from, every
    later line as it prints committed point 1, and refuses point 1, which the extract does
    not have, naming the labels it does.
    """
    committed = _committed()
    extract = _relabeled(committed.drop(columns=list(GENERATED_COLUMNS)))
    folder = _sec_inputs(tmp_path, extract)
    model = _read(folder, "extract")
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == [100 + p for p in reversed(committed.index)]
        for label in table.index:
            mine, base = _point(model, label), _point(sec_model, label - 100)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](), rtol=0,
                                        atol=0) == [], (label, report)
            _release(model, _key(model, label))
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out, base = _run_sec(runner, "101").splitlines(), committed_runs().splitlines()
    assert out[0] == ("model point 101: FIA-000001 - M62 NQ premium 100,000, bonus 7%, "
                      "100% indexed")
    assert out[1:] == base[1:]
    refused = _run_sec(runner, "1", check=False)
    assert refused.returncode == 1 and refused.stdout == b""
    labels = [100 + p for p in reversed(committed.index)]
    assert refused.stderr.decode(errors="replace").strip() == (
        f"no model point 1 in the table: {labels}")


def _months(n):
    """``n`` with its unit, as ``run_sec.py`` writes it: "1 month", "15 months"."""
    return f"{n} month" if n == 1 else f"{n} months"


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {_months(-d)} after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {_months(d)}: contract year {p.policy_year(0)}, attained age "
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, AV {p.av_pp_init():,.2f} per "
            f"contract, phase {p.result_glwb()['phase'].iloc[0]} in month 0")


def test_run_sec_prints_a_point_and_the_block(sec_model, s_model, committed_runs):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  S's anchor in force at 84, the runner's default, the anchor restated
    after its account value ran out, and the anchor issued 15 months on, each with its
    lines at the valuation date asserted whole, so that a longer number cannot pass for
    the one asserted: where its row came from, which only the committed table's generator
    columns can say, the contract and its rider, where it stands, its frame, and when its
    first lifetime withdrawal falls and its account value runs out, by contract year and
    ``t``, or that each fell before the valuation date.  Then the account value, the
    benefit base and the lifetime withdrawal at the first fourteen anniversaries on the
    books, among them, on the default point, the worked example's anniversary 8 at
    ``t = 11``, S's own month 95, which the test reads from S; and the cash flows month by
    month and by contract year.  And the block: a line for each of the 18 points, in table
    order, its first twelve rows, which must be the committed points' frames summed row by
    row, as this test sums them, and those frames summed into projection years, each year's
    count the one in force in its first month.  Nothing else runs the runner on the
    committed table.
    """
    anchor, depleted = _row(sec_model, "twin", 1, 84), _row(sec_model, "derived", 2, 240)
    future = _row(sec_model, "future", 2, -15)
    header = "{} - M62 NQ premium 100,000, bonus 7%, 100% indexed"
    rider = ("GLWB elected  basis single  income from age 70  utilization 100%  cap 5.25%  "
             "rollup blended  stack 1.50x")
    frame = ("proj_len = {} from the valuation date (t = 0..{}); cover ends at policy "
             "month 708, the anniversary at attained age 121")
    events = "first lifetime withdrawal {}; account value runs out {}"
    for args, p, lines in (
            ((), anchor, [
                header.format("model point 1: FIA-000001 (S's FIA-000001, in force at its "
                              "month 84)"),
                rider, f"at the valuation date: {_standing(anchor)}",
                frame.format(_months(624), 623),
                events.format("in contract year 8, at t = 11",
                              "in contract year 19, at t = 143 (DEPLETED)")]),
            (("14",), depleted, [
                header.format("model point 14: FIA-000002-M240 (S's FIA-000002 at its "
                              "month 240)"),
                rider, f"at the valuation date: {_standing(depleted)}",
                frame.format(_months(468), 467),
                events.format("before the valuation date", "before the valuation date")]),
            (("18",), future, [
                header.format("model point 18: FIA-000002-F15 (S's FIA-000002, issued 15 "
                              "months on)"),
                rider, f"at the valuation date: {_standing(future)}",
                frame.format(_months(723), 722),
                events.format("in contract year 8, at t = 110",
                              "in contract year 19, at t = 242 (DEPLETED)")])):
        out = committed_runs(*args)
        assert out.splitlines()[:5] == lines, args
        anniversaries = [t for t in range(p.t_entry(), p.proj_len()) if p.is_anniv(t)]
        cols = ["av_pp_bef_inv", "index_credit_pp", "rider_charge_pp", "wd_pp", "av_pp",
                "mgsv_pp"]
        trace = p.result_av().loc[anniversaries[:14], cols].join(
            p.result_glwb().loc[anniversaries[:14], ["benefit_base_pp", "lw_pp", "phase"]])
        assert trace.round(2).to_string() in out, args
        assert p.result_cf().head(12).round(2).to_string() in out, args
        assert p.result_cf_annual().head(14).round(2).to_string() in out, args
    assert _standing(anchor) == ("in force 84 months: contract year 8, attained age 69, "
                                 "1.000000 in force, AV 128,000.00 per contract, phase "
                                 "INCOME in month 0")
    s1 = _point(s_model, 1).result_av()
    assert anchor.result_av().loc[11].tolist() == s1.loc[95].tolist()
    assert anchor.result_av().loc[11, "av_pp"] == pytest.approx(122865.84, abs=0.005)
    out = committed_runs("--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<16} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    assert ("  18  FIA-000002-F15   to be issued at t = 15, 15 months after the valuation "
            "date; proj_len 723") in out
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert annual.head(12).round(2).to_string() in out


def test_run_sec_says_one_month_where_a_point_is_a_month_from_the_valuation_date(tmp_path):
    """The runner writes "1 month", not "1 months", on both sides of the valuation date.

    No committed point is in force one month or issued one month on, so the runner is run,
    with ``--block``, beside a table of two: the pre-exercise programme moved back to
    policy month 1, its first-year state as ``Data`` requires it, and the anchor issued a
    month on.  Each block line is asserted whole.
    """
    committed = _committed()
    first, future = _label(committed, "derived", 8, 6), _label(committed, "future", 2, -15)
    table = _both(_set("duration_mth", [first], 1),
                  _set("duration_mth", [future], -1),
                  _set("scenario_id", [future], "worked"))(committed)
    folder = _sec_inputs(tmp_path, table.loc[[first, future]])
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "--block").splitlines()
    count = committed.at[first, "policy_count"]
    assert out[:3] == [
        "model points, t = 0 the valuation date for each:",
        f"  {first:>2}  FIA-000008-M6    in force 1 month: contract year 1, attained age "
        f"62, {count:.6f} in force, AV 107,000.00 per contract, phase ACCUM in month 0; "
        f"proj_len 707",
        f"  {future:>2}  FIA-000002-F15   to be issued at t = 1, 1 month after the "
        f"valuation date; proj_len 709"]


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
    whose text runs into the gap between two spans is what docutils rejects as a
    malformed table, dropping the whole table from the page.  Only the last column may run
    past its rule.  Each table runs from a rule line to the blank line that ends it.
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


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only FIA_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, which are
    exactly the cells ``FIA_US_S`` lacks, and every opening-state column, and names nothing
    the model lacks: every name in it is a cell or a Reference.  No row of a simple table in
    any docstring puts text between two of its columns (:func:`_table_overruns`), which
    would drop the table from the rendered page, as a 25-character label in the symbol
    map's 24-character first column once dropped the whole map.  And no docstring says
    what :data:`STALE` matches, each of whose phrases ``FIA_US_S``'s docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "fixed indexed annuit"):
        assert phrase in flat["model"], phrase
    assert set(NEW_CELLS) == set(sec_model.Projection.cells) - set(s_model.Projection.cells)
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in (*NEW_CELLS, *STATE) if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    overruns = {where: rows for where, rows in ((where, _table_overruns(doc))
                                                for where, doc in _docs(sec_model)) if rows}
    assert not overruns, f"table rows that run into a column gap: {overruns}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe FIA_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    unsaid = [phrase for phrase in STALE_PHRASES
              if not any(re.search(phrase, doc) for doc in s_flat)]
    assert not unsaid, f"phrases FIA_US_S does not say, so STALE holds nothing: {unsaid}"
    broken = ("=" * 24 + "  " + "=" * 4 + "\n(shortfall at exhaustion) av_depletion_pp(t)\n"
              + "=" * 24 + "  " + "=" * 4 + "\n")
    assert _table_overruns(broken) == ["(shortfall at exhaustion) av_depletion_pp(t)"]


@pytest.mark.docutils
def test_the_docstrings_parse_as_rst(sec_model):
    """Every docstring of the model parses as reStructuredText, without a warning.

    The docs build reads each docstring through docutils, which reports a malformed table, a
    bad indentation or an unclosed inline markup and drops what it cannot read; a raw-text
    test sees none of it.  Each docstring, dedented as autodoc dedents it and its Sphinx
    roles read as plain interpreted text, which docutils alone does not know, is parsed
    here, and any warning or error is a fault.  docutils comes with the docs build, not with
    the models' requirements, so the test is skipped where it is absent; the column check
    in the test above runs everywhere.
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
    two changed: ``model_point_file``, to ``model_point_table_sec.csv``, and
    ``rate_scenario_file``, to the companion ``rate_scenario_sec.csv``, the scenarios
    re-based to each row's valuation month (D8).  An edit to any other table reaches both
    models, and the two can never drift apart; an edit to S's scenarios reaches this model
    through the companion's regeneration, which T6 holds.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "rate_scenario_file": COMPANION}


# ---------------------------------------------------------------------------
# Stage EC -- what compiling changed, held in modelx (USLIB-SEC-PLAN.md Phase 2)


def _references(space):
    """The References a space's ``__init__.py`` assigns, a name to a literal value."""
    source = (model_path(SEC) / space / "__init__.py").read_text(encoding="utf-8")
    return {node.targets[0].id: node.value.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)}


def _comment(path):
    """The comment lines of ``path``, one string, each line's ``#`` and indent dropped."""
    source = path.read_text(encoding="utf-8")
    return " ".join(line.strip().lstrip("# ") for line in source.splitlines()
                    if line.strip().startswith("#"))


# The size of each one-parameter cache spec_sec.py gives, by the parameter's name, which
# _fia_c4_also reads every key of.
SPEC_SIZES = {name: size for name, size in ast.literal_eval(
    (model_path(SEC).parent / "spec_sec.py").read_text(encoding="utf-8"))[
        "spaces"]["Projection"]["cells_param_size"].items() if isinstance(name, str)}

# The codes, each family in its numbering's order: the timings, the count's five, the
# account value's five and the benefit base's own two, one numbering; the kinds and their
# total; the scenario's columns; the three switches' settings; and the phases.
TIMING_CODES = ("BEF_NB", "BEF_DECR", "BEF_MORT", "BEF_LAPSE", "AFT_DECR", "BEF_PREM",
                "BEF_INV", "BEF_FEE", "BEF_WD", "EOY", "BEF_ROLLUP", "BEF_STEP_UP")
KIND_CODES = ("DEATH", "LAPSE", "MATURITY", "ALL")
NAME_CODES = ("INDEX_LEVEL", "MVA_REF_YIELD")
SWITCH_SETTINGS = (("ANNUAL", "AT_EXERCISE"), ("PRO_RATA", "DOLLAR"),
                   ("GROSS", "SURRENDER_VALUE"))


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one above the comment's, which only adds headroom, and C4 sees one below only on
    a point that reaches it.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * (maturity_age - issue_age_min + 1) +
    future_horizon_mth + 2``, ``y`` to ``maturity_age - issue_age_min + 3``, ``a`` to
    ``maturity_age + 3`` and ``k`` to ``maturity_age - issue_age_min + 2``; every 2-D
    cache to one width, the timings' count, the widest family (§7.2, *For M16 and later*,
    item 16), each family of codes dense from 0, and the switches' and the phases' codes
    too; and ``Data.read_last_mth`` and ``Data.read_last_age``, the last month and age the
    arrays hold, to the last ``t`` and the last ``a``.  A change to a bound or a size is
    derived again in the comment and here.
    """
    path = model_path(SEC).parent / "spec_sec.py"
    comment = _comment(path)
    for formula in ("1,094 = 12 * (maturity_age - issue_age_min + 1) + future_horizon_mth "
                    "+ 2", "81 = maturity_age - issue_age_min + 1, so 82, and one of "
                    "headroom, 83", "123 = maturity_age + 3",
                    "82 = maturity_age - issue_age_min + 2", "Data.read_last_mth",
                    "Data.read_last_age"):
        assert formula in comment, formula
    sizes = ast.literal_eval(path.read_text(encoding="utf-8"))[
        "spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    low, top, horizon = (proj["issue_age_min"], proj["maturity_age"],
                         data["future_horizon_mth"])
    families = [[proj[code] for code in family]
                for family in (TIMING_CODES, KIND_CODES, NAME_CODES, *SWITCH_SETTINGS,
                               PHASES)]
    for family in families:
        assert family == list(range(len(family))), family
    t = 12 * (top - low + 1) + horizon + 2
    width = max(len(family) for family in families[:3])
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     ("y", "name"): (top - low + 3, width), "y": top - low + 3,
                     "a": top + 3, "k": top - low + 2}, sizes
    assert (t, width) == (1094, 12)
    assert data["read_last_mth"] == t - 1 and data["read_last_age"] == top + 2


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: the deepest cold calls of the longest
    frame need a limit of 2,001 in the export, and the reports the sample runs in
    ascending ``t``, the export's import among the frames they run under, 742.  The limit
    is four times the first, rounded up to the thousand.  No build can tell a lower limit
    above the reports' need, which builds the same model.  So this holds the limit, read
    from the sample's code, to the value derived from its comment's need, and holds the
    call before the import of the export.  A change to the need is measured again and
    written in the comment.
    """
    path = model_path(SEC).parent / "sample_sec.py"
    comment = _comment(path)
    need = re.search(r"need a limit of ([\d,]+) in the export", comment)
    reports = re.search(r"which run in ascending t, need ([\d,]+)", comment)
    assert need and reports, comment
    need, reports = (int(m.group(1).replace(",", "")) for m in (need, reports))
    tree = ast.parse(path.read_text(encoding="utf-8"))
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


def test_the_spec_maps_s_totals_and_scenario_columns_onto_sec_codes():
    """``SPEC.twin_arg_map`` hands T1 S's keys as SEC names them (R9, R12).

    ``sec_support._fia_codes`` maps S's ``kind=None`` totals of ``claims`` and
    ``claims_over_av`` onto ``"ALL"`` and S's ``scenario_value`` columns onto their codes'
    names, ``"INDEX_LEVEL"`` and ``"MVA_REF_YIELD"``, and passes every other key, SEC's
    own codes among them, as it is; ``sec_support.codes`` then turns each name into the
    SEC model's int code.  A map that dropped either, or touched a kind S names or a
    code SEC passes, would compare S's total with a kind, or a column with nothing, in
    T1.
    """
    arg_map = SPEC.twin_arg_map
    assert arg_map("claims", (5, None)) == (5, "ALL")
    assert arg_map("claims_over_av", (7, None)) == (7, "ALL")
    assert arg_map("claims", (5, "DEATH")) == (5, "DEATH")
    assert arg_map("claims", (5, 3)) == (5, 3)
    assert arg_map("scenario_value", (8, "index_level")) == (8, "INDEX_LEVEL")
    assert arg_map("scenario_value", (8, "mva_ref_yield")) == (8, "MVA_REF_YIELD")
    assert arg_map("scenario_value", (8, 1)) == (8, 1)
    assert arg_map("pols_if_at", (3, "BEF_DECR")) == (3, "BEF_DECR")
    assert arg_map("payout_rate", (70, "single")) == (70, "single")


# The two totals S writes as kind=None and SEC as the code ALL.
TOTALLED = ("claims", "claims_over_av")


def test_the_all_totals_are_s_totals_bit_for_bit(sec_model, s_model):
    """``claims(t, ALL)`` and ``claims_over_av(t, ALL)`` are ``FIA_US_S``'s totals, bit
    for bit (R12).

    S's ``claims(t, kind=None)`` and ``claims_over_av(t, kind=None)`` are the three kinds'
    total, written as a chain of ``+`` in the kinds' order, and here they are the code
    ``ALL``, the same chain.  T1 reaches S's totals through the spec's ``twin_arg_map``
    to its tolerance; here they are held exactly, on the twins of S's six new-business
    points, in every month of the frame: each total S's float, its type and the sign of a
    zero included, by ``float.hex``, and each kind S's at the kind's name.  A total
    summed in another order, or one that sums a kind twice and another not at all, moves
    a last bit or a number in a month where two kinds are paid, and fails.
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
    ``0.0``, as a ``sum`` from ``0.0`` is, gives ``0.0`` and fails.
    """
    s = _read(model_path(TWIN), "s_zeros")
    sec = _read(model_path(SEC), "zeros")
    try:
        theirs, mine = _point(s, 2), _row(sec, "twin", 2, 0)
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


def test_every_parameterless_cell_returns_a_python_number(sec_model):
    """Every parameterless cell but the reporting ones returns a Python int, float or bool.

    R11: a ``Projection`` cell that reads a ``Data`` vector converts the element, ``int()``,
    ``float()`` or ``bool()``, so that modelx returns a Python number, as the compiled cell
    does, and not a numpy scalar, whose arithmetic and printing differ.  A conversion left
    out moves no number and still compiles, so it is asserted here: on every committed
    point, each parameterless cell outside :func:`sec_support.reporting_cells` returns
    exactly an ``int``, a ``float`` or a ``bool``, and each flag a ``bool``.
    """
    from sec_support import reporting_cells
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    assert {"mort_schedule", "point_id", "glwb_elected", *DECODES} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
        found += [f"{key}: {name} is not a bool" for name in ("glwb_elected", *DECODES)
                  if type(proj.cells[name]()) is not bool]
    assert not found, found


def test_every_data_vector_is_an_int64_or_float64_array_and_every_extent_an_int(
        sec_model):
    """``Data`` hands a projection C's types: int64 and float64 arrays and Python ints.

    A compiled ``Projection`` cell reads a ``Data`` array as a typed memoryview,
    ``const long long[:]`` or ``const double[:]`` or ``[:, :]``, and an extent as a C
    integer, so a bool array, a float32 one or a numpy integer for an extent would be read
    otherwise, or not at all (N6).  So every ``Data`` cell that returns an array returns
    an int64 or float64 one, of one or two dimensions, every one of the model point
    table's vectors one value a point; and every one that returns a number returns exactly
    a Python ``int``, the extents and counts among them, and these thirteen at least.
    """
    data = sec_model.Data
    points = len(data.model_point_table())
    arrays, ints = {}, {}
    for name, cells in data.cells.items():
        value = cells()
        if isinstance(value, np.ndarray):
            arrays[name] = value
        elif isinstance(value, (numbers.Number, np.generic)):
            ints[name] = value
    assert len(arrays) == 49, sorted(arrays)
    for name, value in arrays.items():
        assert value.dtype in (np.int64, np.float64) and value.ndim in (1, 2), (
            name, value.dtype, value.ndim)
    vectors = [name for name, value in arrays.items()
               if value.ndim == 1 and len(value) == points]
    assert {"point_id", "glwb_elected", "is_single_basis", "mort_schedule"} <= set(vectors)
    assert {"surr_charge_last_year", "payout_rate_first_age", "payout_rate_last_age",
            "mort_schedule_count", "mort_age_base", "mort_age_held", "rollup_count",
            "rollup_last_year", "payout_rate_held_age", "scenario_count",
            "scenario_last_mth", "wd_schedule_count", "wd_last_year"} <= set(ints)
    assert all(type(value) is int for value in ints.values()), {
        name: type(value).__name__ for name, value in ints.items()}


def test_the_arrays_pad_with_nan_where_no_read_reaches(tmp_path):
    """Every place an array holds no table value is NaN, so that a read of it shows (N3).

    ``Data`` sizes each array past the keys its table gives, from 0 or to
    ``read_last_mth`` and ``read_last_age``, and a read the readers' guards should have
    stopped, at a schedule number of 0, at year 0, at an age outside a sex's rates or at a
    month before a scenario's first, would read padding: written NaN, it carries into
    every number that reads it, where 0.0 would pass for a rate.  So, on a copy whose
    female rates run from 45 to 119 alone, and with the committed scenario that starts at
    month 15: row 0 of every by-schedule array, the mortality's, the rollup's, the two
    scenarios' and the withdrawals', is NaN; so is year 0 of the surrender charge, the
    vesting and the rollup; the female rates at ages 40 to 44 and 120 to 122, and the male
    at 121 and 122; and the scenario's months 0 to 14.  And what is a value is not
    padding: a rollup schedule before its first row and a withdrawal programme at a count
    without one are 0.0, as ``FIA_US_S`` answers them, and every other cell is a number.
    """
    model = _read(_sec_inputs(tmp_path, _committed(),
                              {"mort_table.csv": _short_female_mortality}), "padding")
    try:
        data = model.Data
        for name in ("mort_table_array", "rollup_rate_array", "index_level_array",
                     "mva_ref_yield_array", "wd_amount_array"):
            assert np.isnan(data.cells[name]()[0]).all(), name
        for name in ("surr_charge_rate_array", "vest_rate_array"):
            values = data.cells[name]()
            assert math.isnan(values[0]) and not np.isnan(values[1:]).any(), name
        rollups = data.rollup_rate_array()
        assert np.isnan(rollups[:, 0]).all() and not np.isnan(rollups[1:, 1:]).any()
        mort, base = data.mort_table_array(), data.mort_age_base()
        sexes = {sex: number for number, (sex, _) in enumerate(
            data.mort_rates().groupby(level="sex"), start=1)}
        padded = {"F": [*range(40, 45), *range(120, 123)], "M": [121, 122]}
        for sex, number in sexes.items():
            row = mort[number]
            gaps = [base + j for j in range(len(row)) if math.isnan(row[j])]
            assert gaps == padded[sex], (sex, gaps)
        assert not np.isnan(data.payout_rate_array()).any()
        scenario = data.scenario_number()[_key(model, _label(_committed(), "future", 2,
                                                             -15))]
        for name in ("index_level_array", "mva_ref_yield_array"):
            row = data.cells[name]()[scenario]
            assert np.isnan(row[:15]).all() and not np.isnan(row[15:]).any(), name
        assert not np.isnan(data.wd_amount_array()[1:]).any()
        assert (data.wd_amount_array()[1:] == 0.0).sum() > 0
    finally:
        model.close()
    late = _read(_sec_inputs(tmp_path / "late", _committed(),
                             {"rollup_table.csv": _late_rollup}), "padding_late")
    try:
        rollups = late.Data.rollup_rate_array()
        number = sorted(set(late.Data.rollup_steps().index.get_level_values(
            "rollup_id"))).index("late") + 1
        assert not np.isnan(rollups[1:, 1:]).any()
        assert list(rollups[number, 1:4]) == [0.0, 0.0, 0.04], rollups[number, :4]
    finally:
        late.close()


@pytest.mark.parametrize("column, s_point", [("glwb_basis", 2), ("glwb_basis", 6),
                                             ("credit_method", 2)])
def test_a_table_without_a_decoded_column_is_refused_where_s_reads_it(tmp_path, column,
                                                                     s_point):
    """A table without ``glwb_basis`` or ``credit_method`` fails where S's does (N7).

    ``FIA_US_S`` reads the basis only on a rider point that reaches its exercise, and the
    crediting method at every credit, and stage E's ``Data`` requires every other column
    a projection reads, but not these two.  So, as at stage E, a table without either
    reads, and its decodes raise pandas' ``KeyError`` where a projection first asks for
    them: on S's copy and on SEC's, the anchor issued now raises ``KeyError`` naming the
    column, the same line in both, and the point without the rider, which never asks for
    the basis, projects without it what it projects with it, in both.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    committed = _committed()
    label = _label(committed, "twin", s_point, 0)
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN),
                          model_points=s_table.drop(columns=column)), "dropped_s")
    sec = _read(_sec_inputs(tmp_path / "sec", committed.drop(columns=column)), "dropped")
    base = _read(model_path(SEC), "dropped_base")
    try:
        did = [_modelx_did(_point(model, point).result_cf)
               for model, point in ((s, s_point), (sec, label))]
        if s_point == 6:
            assert [status for status, _ in did] == ["ok", "ok"], did
            assert frame_mismatches(_point(base, label).result_cf(), did[1][1], rtol=0,
                                    atol=0) == []
        else:
            assert did == [("raised", f"KeyError: '{column}'")] * 2, did
    finally:
        base.close()
        sec.close()
        s.close()


# run_sec.py run as though it sat at /m/products/fixed_indexed_annuity, a copy too shallow
# to have a repository above it: the source compiled under that name, so that its own
# __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/fixed_indexed_annuity/run_sec.py"
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


def test_run_sec_rebuilds_in_place_exactly_when_a_source_is_newer(tmp_path):
    """``run_sec.py --cython`` rebuilds its package where, and only where, it is stale.

    ``compiled_model`` builds in place when no build for this interpreter is there, or
    when the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it, and
    otherwise imports what is there.  So its two functions are read from the runner, which
    runs the model when imported, and run here on a fake product: empty sources, a tool
    and an empty file standing for the extension module, their times set by ``os.utime``,
    with the build and the import stubbed, so that nothing is built or imported.  Built
    after every source, it must not build; with any one source newer than the build, or
    no build, it must, and say so on stderr.
    """
    tree = ast.parse((model_path(SEC).parent / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in ("_built", "compiled_model")]
    assert len(found) == 2
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
    exec(compile(ast.Module(found, []), "run_sec.py", "exec"), space)

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
    from.  Its two functions are read from the runner, which runs the model when imported,
    and run here on a fake product, as
    :func:`test_run_sec_rebuilds_in_place_exactly_when_a_source_is_newer` runs them: empty
    sources and an empty file standing for the extension module, built after every
    source by ``os.utime``, so that the runner does not build, and a stubbed import whose
    ``Projection`` comes from the extension module or from ``_mx_classes.py``.  In place
    and from ``--build DIR``, the package whose extension is missing must be refused,
    saying so, and the one whose extension loaded returned; nothing is built either way.
    This needs neither modelx-cython nor a compiler, so it runs wherever the module does.
    """
    tree = ast.parse((model_path(SEC).parent / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in ("_built", "compiled_model")]
    assert len(found) == 2
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
    exec(compile(ast.Module(found, []), "run_sec.py", "exec"), space)
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
    ``t``, to the last bit.  The printed block, to two decimals, cannot show a last bit,
    so ``add`` itself is read from the runner, which runs the model when imported, and run
    here on the committed points' frames.  A plain running sum differs from ``groupby``'s
    on them, so the comparison can fail.
    """
    tree = ast.parse((model_path(SEC).parent / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "add"]
    assert len(found) == 1
    space = {}
    exec(compile(ast.Module(found, []), "run_sec.py", "exec"), space)
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
    exactly.  ``python tools/gen_sec_fingerprint.py FIA_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# FIA_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: FIA_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 624, "months": (0, 155, 311, 467, 623),
        "result_cf": {
            "pols_if": (189.06716986633313, 1.0, (
                1.0, 0.5969896776148823, 0.15485591731092543, 0.0008299536011489307, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (155227.60907680204, 9780.166366656205, (
                0.0, 6055.958808073784, 1570.8832021487974, 8.419182122630936, 0.0)),
            "wd_guar": (96541.45470940889, 9780.166366656205, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (58686.15436739317, 6055.958808073784, (
                0.0, 6055.958808073784, 1570.8832021487974, 8.419182122630936, 0.0)),
            "claims_death": (13805.78789771752, 148.42525419684375, (
                145.28758213201343, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (12017.07496671763, 263.2237804841653, (
                263.2237804841653, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1665.139087051949, 6.666666666666667, (
                6.666666666666667, 5.475101282830039, 1.9577777606175526,
                0.014464374225554636, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-182715.61102828916, 10164.61614807533, (
                -415.1780292828454, -6061.433909356614, -1572.840979909415,
                -8.43364649685649, 0.0)),
        },
        "result_pols": {
            "pols_if": (189.06716986633313, 1.0, (
                1.0, 0.5969896776148823, 0.15485591731092543, 0.0008299536011489307, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.09100800000004, 1.0, (
                0.013536, 0.045846, 0.165881, 0.505141, 1.0)),
            "mort_rate_mth": (35.44068152575704, 1.0, (
                0.001135059235406355, 0.003903212169360959, 0.015001276167648236,
                0.056938266786213165, 1.0)),
            "lapse_rate": (1.981264685347871, 0.025894046384251312, (
                0.025894046384251312, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.16637862150052163, 0.0021838784689754975, (
                0.0021838784689754975, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.8590706611342465, 0.0031972051289156284, (
                0.001135059235406355, 0.0023301773746492844, 0.002323036381775692,
                4.725611956239617e-05, 0.0)),
            "pols_lapse": (0.14092933886575443, 0.0021813996375502818, (
                0.0021813996375502818, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (188.0671698663331, 0.9966835411270434, (
                0.9966835411270434, 0.5946595002402331, 0.15253288092914974,
                0.0007826974815865345, 0.0)),
        },
    },
    2: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (225.04125575615194, 1.0, (
                1.0, 0.5974476531111299, 0.2125514937660179, 0.0021147796969922775, 0.0)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (93449.39133639247, 5907.961773545727, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (58139.070500646994, 5907.961773545727, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (35310.32083574548, 3643.752956488752, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (15433.107185991284, 91.29050122360486, (
                59.89899720728786, 62.69873308822546, 0.0, 0.0, 0.0)),
            "claims_lapse": (21919.504443003105, 205.65433019504536, (
                154.56406122875467, 27.014763844311403, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (8111.189581261103, 6006.666666666667, (
                6006.666666666667, 5.721263622438291, 2.929768302383844, 0.0419576601935435,
                0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-38913.19254664796, 93778.87027489729, (
                93778.87027489729, -95.43476055497514, -2.929768302383844,
                -0.0419576601935435, 0.0)),
        },
        "result_pols": {
            "pols_if": (225.04125575615194, 1.0, (
                1.0, 0.5974476531111299, 0.2125514937660179, 0.0021147796969922775, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.86615999999998, 1.0, (
                0.006697, 0.027585, 0.124275, 0.469427, 1.0)),
            "mort_rate_mth": (35.50556348888881, 1.0, (
                0.0005598037122176436, 0.002328336119712171, 0.010997675514194838,
                0.05144592202933218, 1.0)),
            "lapse_rate": (4.0287110574099465, 0.031115390716231248, (
                0.02, 0.012, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.3389767555555041, 0.002630680051440848, (
                0.001682142552739574, 0.0010055425391276573, 0.0, 0.0, 0.0)),
            "pols_death": (0.7352941135316162, 0.0025208332858406724, (
                0.0005598037122176436, 0.0013910589503759114, 0.002337572358496072,
                0.00010879679140067944, 0.0)),
            "pols_lapse": (0.26470588646838383, 0.0021750746821034865, (
                0.001681200883094071, 0.0005993602611561881, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (224.04125575615194, 0.9977589954046883, (
                0.9977589954046883, 0.5954572338995978, 0.21021392140752182,
                0.002005982905591598, 0.0)),
        },
    },
    3: {"rows": 624, "months": (0, 155, 311, 467, 623),
        "result_cf": {
            "pols_if": (161.826162653208, 1.0, (
                1.0, 0.4844922252074108, 0.1210825916142911, 0.0006489447396766424, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (90514.96028885074, 6615.80269321624, (
                0.0, 3365.121175887456, 840.9992397672667, 4.507353414250905, 0.0)),
            "wd_guar": (73596.51112884299, 6615.80269321624, (
                0.0, 3365.121175887456, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (16918.449160007738, 2351.4975146999473, (
                0.0, 0.0, 840.9992397672667, 4.507353414250905, 0.0)),
            "claims_death": (19748.400297066542, 150.95785462777835, (
                145.28758213201343, 53.04431162058884, 0.0, 0.0, 0.0)),
            "claims_lapse": (28975.019092100956, 395.6094074356339, (
                395.6094074356339, 13.611896750736868, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1405.5979881792487, 6.666666666666667, (
                6.666666666666667, 4.4433666162407155, 1.5307959113014267,
                0.011309764248741078, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-140643.97766619746, 7132.272807070699, (
                -547.563656234314, -3436.2207508750225, -842.5300356785681,
                -4.518663178499646, 0.0)),
        },
        "result_pols": {
            "pols_if": (161.826162653208, 1.0, (
                1.0, 0.4844922252074108, 0.1210825916142911, 0.0006489447396766424, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.09100800000004, 1.0, (
                0.013536, 0.045846, 0.165881, 0.505141, 1.0)),
            "mort_rate_mth": (35.44068152575704, 1.0, (
                0.001135059235406355, 0.003903212169360959, 0.015001276167648236,
                0.056938266786213165, 1.0)),
            "lapse_rate": (4.869330326011815, 0.044717948717948715, (
                0.038683544303797474, 0.012, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.41194918376577805, 0.0038051287842019166, (
                0.0032822371346300505, 0.0010055425391276573, 0.0, 0.0, 0.0)),
            "pols_death": (0.6965472024786253, 0.0024999101723334363, (
                0.001135059235406355, 0.0018910759493903362, 0.0018163933959005492,
                3.6949788717218315e-05, 0.0)),
            "pols_lapse": (0.30345279752137544, 0.003333944193991873, (
                0.0032785116010575948, 0.00048527598501083545, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (160.826162653208, 0.995586429163536, (
                0.995586429163536, 0.4821158732730096, 0.11926619821839055,
                0.0006119949509594241, 0.0)),
        },
    },
    4: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (228.6713063538404, 1.0, (
                1.0, 0.6126032041909938, 0.21794332182676512, 0.002168425655016423, 0.0)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (116884.22148736934, 7303.113486278382, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (72641.23943873848, 7303.113486278382, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (44242.982048630845, 4565.5347453082395, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (16668.852795916377, 102.8762311958571, (
                59.92171993756423, 69.44701354369924, 0.0, 0.0, 0.0)),
            "claims_lapse": (21342.592989261535, 203.57211527436002, (
                150.3658198741551, 29.92236969024264, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (8149.4234435944845, 6006.666666666667, (
                6006.666666666667, 5.866395840499079, 3.00408820794833, 0.04302200693412147,
                0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-63045.09071614174, 93783.04579352161, (
                93783.04579352161, -105.23577907444096, -3.00408820794833,
                -0.04302200693412147, 0.0)),
        },
        "result_pols": {
            "pols_if": (228.6713063538404, 1.0, (
                1.0, 0.6126032041909938, 0.21794332182676512, 0.002168425655016423, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.86615999999998, 1.0, (
                0.006697, 0.027585, 0.124275, 0.469427, 1.0)),
            "mort_rate_mth": (35.50556348888881, 1.0, (
                0.0005598037122176436, 0.002328336119712171, 0.010997675514194838,
                0.05144592202933218, 1.0)),
            "lapse_rate": (3.7344546333686623, 0.028614915167433443, (
                0.019454463469043223, 0.012, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.31397057763449077, 0.002416434334767348, (
                0.001635843236763579, 0.0010055425391276573, 0.0, 0.0, 0.0)),
            "pols_death": (0.752222919199763, 0.0025847796708142064, (
                0.0005598037122176436, 0.0014263461673693014, 0.0023968699339365,
                0.00011155665717437846, 0.0)),
            "pols_lapse": (0.24777708080023605, 0.0020137226233686487, (
                0.0016349274856470326, 0.0006145643296731391, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (227.6713063538404, 0.9978052688021353, (
                0.9978052688021353, 0.6105622936939514, 0.21554645189282862,
                0.0020568689978420446, 0.0)),
        },
    },
    5: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (216.1567599075283, 1.0, (
                1.0, 0.5638271089212062, 0.1888404287976075, 0.0018788666111757236, 0.0)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (97560.53186129831, 6944.6364546102695, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (75893.10977804323, 6944.6364546102695, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (21667.422083255085, 3011.557897349604, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (27283.352515339262, 137.7140248508364, (
                59.89899720728786, 126.9104713459178, 0.0, 0.0, 0.0)),
            "claims_lapse": (33014.27127584414, 234.82852972534369, (
                153.0899596234268, 54.68143045180713, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (8006.8372113374035, 6006.666666666667, (
                6006.666666666667, 5.39930738838374, 2.6029396109953713,
                0.03727709649039321, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-65864.99286381915, 93780.34437650262, (
                93780.34437650262, -186.99120918610865, -2.6029396109953713,
                -0.03727709649039321, 0.0)),
        },
        "result_pols": {
            "pols_if": (216.1567599075283, 1.0, (
                1.0, 0.5638271089212062, 0.1888404287976075, 0.0018788666111757236, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.86615999999998, 1.0, (
                0.006697, 0.027585, 0.124275, 0.469427, 1.0)),
            "mort_rate_mth": (35.50556348888881, 1.0, (
                0.0005598037122176436, 0.002328336119712171, 0.010997675514194838,
                0.05144592202933218, 1.0)),
            "lapse_rate": (5.429600508540425, 0.0303552164680678, (
                0.019811001410437235, 0.012, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.4571291556583845, 0.0025654932410160702, (
                0.0016660996963493435, 0.0010055425391276573, 0.0, 0.0, 0.0)),
            "pols_death": (0.6750200289036895, 0.002239623115278908, (
                0.0005598037122176436, 0.001312779022974133, 0.0020768057598775018,
                9.666002518206187e-05, 0.0)),
            "pols_lapse": (0.32497997109631094, 0.0021270578991404005, (
                0.0016651670075544024, 0.0005656320875815611, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (215.15675990752828, 0.997775029280228, (
                0.997775029280228, 0.5619486978106506, 0.18676362303773,
                0.0017822065859936617, 0.0)),
        },
    },
    6: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (153.48624324883897, 1.0, (
                1.0, 0.3106292954955293, 0.04618696292154572, 0.0001844829425385433, 0.0)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (52078.16947155232, 173.98859670236948, (
                59.89899720728786, 128.85705513882812, 111.89673543928255,
                2.0907604743777966, 0.0)),
            "claims_lapse": (107741.48408326488, 3174.3727483862554, (
                154.56406122875467, 283.96693359736946, 51.75251200767975,
                0.19825905390302898, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7295.194285762282, 6006.666666666667, (
                6006.666666666667, 2.974640672078487, 0.636632081729254,
                0.0036601791787324303, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-67114.84784057944, 93778.87027489729, (
                93778.87027489729, -415.79862940827604, -164.28587952869157,
                -2.2926797074595577, 0.0)),
        },
        "result_pols": {
            "pols_if": (153.48624324883897, 1.0, (
                1.0, 0.3106292954955293, 0.04618696292154572, 0.0001844829425385433, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.86615999999998, 1.0, (
                0.006697, 0.027585, 0.124275, 0.469427, 1.0)),
            "mort_rate_mth": (35.50556348888881, 1.0, (
                0.0005598037122176436, 0.002328336119712171, 0.010997675514194838,
                0.05144592202933218, 1.0)),
            "lapse_rate": (42.360000000000014, 0.33, (
                0.02, 0.06, 0.06, 0.06, 0.06)),
            "lapse_rate_mth": (3.681504708744997, 0.03282239126053954, (
                0.001682142552739574, 0.005143012831822946, 0.005143012831822946,
                0.005143012831822946, 0.005143012831822946)),
            "pols_death": (0.28947454234273495, 0.0009975409780108107, (
                0.0005598037122176436, 0.000723249408542986, 0.0005079492311973082,
                9.490895077579669e-06, 0.0)),
            "pols_lapse": (0.7105254576572657, 0.02118869905479569, (
                0.001681200883094071, 0.0015938507716848841, 0.00023492775355447794,
                8.99986345558706e-07, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (152.486243248839, 0.9977589954046883, (
                0.9977589954046883, 0.30831219531530146, 0.045444085936793936,
                0.00017409206111540493, 0.0)),
        },
    },
    7: {"rows": 624, "months": (0, 155, 311, 467, 623),
        "result_cf": {
            "pols_if": (116.26759241404865, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (92199.4497217416, 10269.174684989017, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (87831.81093007515, 9780.166366656205, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (4367.638791666435, 489.0083183328108, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (13449.144136958355, 147.81253322956212, (
                145.28758213201343, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (11845.200597180143, 263.2237804841653, (
                263.2237804841653, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (891.1482511544823, 6.666666666666667, (
                6.666666666666667, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-118384.94270703457, 10652.065909388806, (
                -415.1780292828454, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (116.26759241404865, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.09100800000004, 1.0, (
                0.013536, 0.045846, 0.165881, 0.505141, 1.0)),
            "mort_rate_mth": (35.44068152575704, 1.0, (
                0.001135059235406355, 0.003903212169360959, 0.015001276167648236,
                0.056938266786213165, 1.0)),
            "lapse_rate": (13.98126468534787, 1.0, (
                0.025894046384251312, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (1.1663786215005219, 1.0, (
                0.0021838784689754975, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2358384572759246, 0.002288318922630616, (
                0.001135059235406355, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.7641615427240761, 0.6232322038583218, (
                0.0021813996375502818, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (115.26759241404866, 0.9966835411270434, (
                0.9966835411270434, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    8: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (221.45865027452209, 1.0, (
                1.0, 0.5875784446517662, 0.20160485711018375, 0.002005866207183576, 0.0)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (102568.1421594716, 46551.61020401425, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (41466.58734032941, 3649.0037853478634, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (46551.61020401425, 46551.61020401425, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (14549.944615127934, 1789.1377619365628, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (11569.776288491877, 71.69307989772366, (
                59.89899720728786, 48.15498808496698, 0.0, 0.0, 0.0)),
            "claims_lapse": (15622.243581197356, 155.78228490881003, (
                153.0899596234268, 20.748355939034354, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (8067.620924353382, 6006.666666666667, (
                6006.666666666667, 5.626754349455483, 2.7788819993815195,
                0.03979679435849424, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-37827.78295351423, 93780.34437650262, (
                93780.34437650262, -74.53009837345682, -2.7788819993815195,
                -0.03979679435849424, 0.0)),
        },
        "result_pols": {
            "pols_if": (221.45865027452209, 1.0, (
                1.0, 0.5875784446517662, 0.20160485711018375, 0.002005866207183576, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.86615999999998, 1.0, (
                0.006697, 0.027585, 0.124275, 0.469427, 1.0)),
            "mort_rate_mth": (35.50556348888881, 1.0, (
                0.0005598037122176436, 0.002328336119712171, 0.010997675514194838,
                0.05144592202933218, 1.0)),
            "lapse_rate": (4.657418159202556, 0.0303552164680678, (
                0.019811001410437235, 0.012, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.3918109840587314, 0.0025654932410160702, (
                0.0016660996963493435, 0.0010055425391276573, 0.0, 0.0, 0.0)),
            "pols_death": (0.7083584340862816, 0.002391007587789323, (
                0.0005598037122176436, 0.001368080115847006, 0.002217184800583417,
                0.00010319363649603852, 0.0)),
            "pols_lapse": (0.29164156591371987, 0.0021270578991404005, (
                0.0016651670075544024, 0.0005894594584183978, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (220.4586502745221, 0.997775029280228, (
                0.997775029280228, 0.5856209050775009, 0.19938767230960033,
                0.0019026725706875376, 0.0)),
        },
    },
    9: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (199.90357352312208, 1.0, (
                1.0, 0.5132401544217824, 0.14080492131782055, 0.001400937643690785, 0.0)),
            "premiums": (100000.0, 100000.0, (
                100000.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (39971.14631724265, 5141.178770321501, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (29887.532520420027, 5141.178770321501, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (10083.613796822625, 2072.3737550681535, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (52817.68641927748, 260.91013457851136, (
                59.89899720728786, 178.8596716039583, 19.844641636233252, 0.0, 0.0)),
            "claims_lapse": (55632.38021641758, 501.8246408813029, (
                153.0899596234268, 212.68937981066264, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7814.051020396063, 6006.666666666667, (
                6006.666666666667, 4.91487783034569, 1.9408275518906524,
                0.02779488837060465, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-56235.2639733338, 93780.34437650262, (
                93780.34437650262, -396.46392924496666, -21.785469188123905,
                -0.02779488837060465, 0.0)),
        },
        "result_pols": {
            "pols_if": (199.90357352312208, 1.0, (
                1.0, 0.5132401544217824, 0.14080492131782055, 0.001400937643690785, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.86615999999998, 1.0, (
                0.006697, 0.027585, 0.124275, 0.469427, 1.0)),
            "mort_rate_mth": (35.50556348888881, 1.0, (
                0.0005598037122176436, 0.002328336119712171, 0.010997675514194838,
                0.05144592202933218, 1.0)),
            "lapse_rate": (8.876664361085219, 0.063137735082525, (
                0.019811001410437235, 0.032798544832645035, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.750126262559994, 0.0054201745062765205, (
                0.0016660996963493435, 0.002775181641358593, 0.0, 0.0, 0.0)),
            "pols_death": (0.5601687989390554, 0.0017203117561660306, (
                0.0005598037122176436, 0.0011949955896268882, 0.0015485268354551258,
                7.207252878527247e-05, 0.0)),
            "pols_lapse": (0.4398312010609458, 0.003755906860795972, (
                0.0016651670075544024, 0.0014210183243375427, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (198.90357352312208, 0.997775029280228, (
                0.997775029280228, 0.510624140507818, 0.13925639448236543,
                0.0013288651149055124, 0.0)),
        },
    },
    10: {"rows": 648, "months": (0, 161, 323, 485, 647),
        "result_cf": {
            "pols_if": (172.59028907660712, 0.8615476776454951, (
                0.8615476776454951, 0.5164419978413288, 0.149866092633567,
                0.0009538192989202879, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (116884.22148736933, 7303.113486278382, (
                0.0, 0.0, 1417.6701215274857, 0.0, 0.0)),
            "wd_guar": (72641.23943873848, 7303.113486278382, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (44242.982048630845, 4565.5347453082395, (
                0.0, 0.0, 1417.6701215274857, 0.0, 0.0)),
            "claims_death": (12444.6709014697, 102.8762311958571, (
                89.97033787374704, 11.324231331027208, 0.0, 0.0, 0.0)),
            "claims_lapse": (12125.619708271244, 203.57211527436002, (
                169.71074834533718, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1548.9540298857944, 5.743651184303301, (
                5.743651184303301, 4.795223133843558, 1.9420608590986395,
                0.017250343174879754, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-143003.46612699606, 7545.82010456104, (
                -265.42473740338755, -16.119454464870767, -1419.6121823865842,
                -0.017250343174879754, 0.0)),
        },
        "result_pols": {
            "pols_if": (172.59028907660712, 0.8615476776454951, (
                0.8615476776454951, 0.5164419978413288, 0.149866092633567,
                0.0009538192989202879, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.370476, 1.0, (
                0.011056, 0.041427, 0.150778, 0.505141, 1.0)),
            "mort_rate_mth": (35.464096077905, 1.0, (
                0.0009260352822665352, 0.003519588238610094, 0.013527227066951197,
                0.056938266786213165, 1.0)),
            "lapse_rate": (2.458005567227036, 0.028614915167433443, (
                0.023482593658268186, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.2065260757400691, 0.002416434334767348, (
                0.00197826594654249, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.7136919858162593, 0.0025847796708142064, (
                0.0007978235468545239, 0.0018176631815266405, 0.0020272726646910033,
                5.4308817707762154e-05, 0.0)),
            "pols_lapse": (0.14785569182923491, 0.0020084477853378165, (
                0.0017027921248547575, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (171.72874139896163, 0.8590470619737858, (
                0.8590470619737858, 0.5146243346598022, 0.14783881996887602,
                0.0008995104812125257, 0.0)),
        },
    },
    11: {"rows": 613, "months": (0, 153, 306, 459, 612),
        "result_cf": {
            "pols_if": (178.24777226777084, 0.9641179128342027, (
                0.9641179128342027, 0.5743749296346888, 0.14026116602640412,
                0.0006871878417098112, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (155227.60907680204, 9780.166366656205, (
                9780.166366656205, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (96541.45470940889, 9780.166366656205, (
                9780.166366656205, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (58686.15436739316, 6055.958808073784, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (12233.863780497495, 148.42525419684375, (
                134.45589030188648, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (9163.771474494637, 243.41929463849132, (
                243.41929463849132, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1556.6312961225494, 6.427452752228018, (
                6.427452752228018, 5.246062981696005, 1.7551116679469567,
                0.011780726109411548, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-178181.87562791677, 10164.469004348812, (
                -10164.469004348812, -5.246062981696005, -1.7551116679469567,
                -0.011780726109411548, 0.0)),
        },
        "result_pols": {
            "pols_if": (178.24777226777084, 0.9641179128342027, (
                0.9641179128342027, 0.5743749296346888, 0.14026116602640412,
                0.0006871878417098112, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (188.942112, 1.0, (
                0.013536, 0.050728, 0.182331, 0.541975, 1.0)),
            "mort_rate_mth": (35.42819587416757, 1.0, (
                0.001135059235406355, 0.004328928389496611, 0.016634892190936612,
                0.06299746621429037, 1.0)),
            "lapse_rate": (1.6964301751211064, 0.025894046384251312, (
                0.025894046384251312, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.14235595834179116, 0.0021838784689754975, (
                0.0021838784689754975, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.8467900039684649, 0.0031972051289156284, (
                0.0010943309409831609, 0.002486427939110723, 0.0023332293754242937,
                4.329109284098495e-05, 0.0)),
            "pols_lapse": (0.11732790886573825, 0.002103126465612264, (
                0.002103126465612264, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (177.28365435493666, 0.9609204554276072, (
                0.9609204554276072, 0.5718885016955781, 0.13792793665097983,
                0.0006438967488688262, 0.0)),
        },
    },
    12: {"rows": 558, "months": (0, 139, 278, 417, 557),
        "result_cf": {
            "pols_if": (93.53621431654665, 0.6189213830544456, (
                0.6189213830544456, 0.32391208500604257, 0.059228673867649004,
                0.00020220318790473824, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (77659.63663437346, 6024.546483162223, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (55992.21455111837, 6024.546483162223, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (21667.422083255085, 3011.557897349604, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (12217.451450675007, 135.15959617041997, (
                131.94798908630995, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (5056.175510283529, 143.96552326411378, (
                143.96552326411378, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (779.8751094394637, 4.126142553696304, (
                4.126142553696304, 2.8744449789344784, 0.6996437594257716,
                0.003179443132774513, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-95713.13870477145, 6284.628192394918, (
                -280.03965490412, -2.8744449789344784, -0.6996437594257716,
                -0.003179443132774513, 0.0)),
        },
        "result_pols": {
            "pols_if": (93.53621431654665, 0.6189213830544456, (
                0.6189213830544456, 0.32391208500604257, 0.059228673867649004,
                0.00020220318790473824, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (187.950582, 1.0, (
                0.022503, 0.075845, 0.219601, 0.579659, 1.0)),
            "mort_rate_mth": (35.34486416955307, 1.0, (
                0.0018948738039474833, 0.006551401417078551, 0.020450489305592345,
                0.06967759670054263, 1.0)),
            "lapse_rate": (1.6514125572069116, 0.02457532284549586, (
                0.02457532284549586, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.1384961196762744, 0.002071379767775716, (
                0.002071379767775716, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.550153191628596, 0.002239623115278908, (
                0.0011727779154528147, 0.002122078092717455, 0.0012112553615147728,
                1.4089032178390391e-05, 0.0)),
            "pols_lapse": (0.06876819142584935, 0.0012795919622565794, (
                0.0012795919622565794, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (92.91729293349219, 0.6164690131767362, (
                0.6164690131767362, 0.3217900069133251, 0.05801741850613423,
                0.00018811415572634785, 0.0)),
        },
    },
    13: {"rows": 492, "months": (0, 122, 245, 368, 491),
        "result_cf": {
            "pols_if": (7.652728761126852, 0.6501666579992569, (
                0.6501666579992569, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (479.0350967465159, 479.0350967465159, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (479.0350967465159, 479.0350967465159, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (52.753852778132895, 4.880796202082157, (
                4.880796202082157, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (51.595707997744334, 4.334444386661713, (
                4.334444386661713, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-583.3846575223931, 483.30010691690705, (
                -9.215240588743871, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (7.652728761126852, 0.6501666579992569, (
                0.6501666579992569, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (185.964204, 1.0, (
                0.041427, 0.112709, 0.287513, 0.617869, 1.0)),
            "mort_rate_mth": (35.17694131551315, 1.0, (
                0.003519588238610094, 0.009915701877919347, 0.027854182450576137,
                0.07703686261280218, 1.0)),
            "lapse_rate": (12.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.026934454140935267, 0.002288318922630616, (
                0.002288318922630616, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.6232322038583218, 0.6232322038583218, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (7.002562103127595, 0.6478783390766263, (
                0.6478783390766263, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    14: {"rows": 468, "months": (0, 116, 233, 350, 467),
        "result_cf": {
            "pols_if": (51.6270689045374, 0.46885870674659413, (
                0.46885870674659413, 0.20561561755067112, 0.020918900399864163,
                3.799988716889142e-05, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (31666.567879256723, 3460.391573861199, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (31666.567879256723, 3460.391573861199, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (404.7254595243158, 3.125724711643961, (
                3.125724711643961, 1.7403190395634218, 0.22525234077887799,
                0.0005205595943454128, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-32071.293338781037, 3463.4398599064384, (
                -3.125724711643961, -1.7403190395634218, -0.22525234077887799,
                -0.0005205595943454128, 0.0)),
        },
        "result_pols": {
            "pols_if": (51.6270689045374, 0.46885870674659413, (
                0.46885870674659413, 0.20561561755067112, 0.020918900399864163,
                3.799988716889142e-05, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (184.91692799999998, 1.0, (
                0.050728, 0.124275, 0.313569, 0.656229, 1.0)),
            "mort_rate_mth": (35.08786771061749, 1.0, (
                0.004328928389496611, 0.010997675514194838, 0.03086768722505151,
                0.08513761910628403, 1.0)),
            "lapse_rate": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.4688587067465941, 0.0025208332858406724, (
                0.0020296557662979977, 0.0022612938424730663, 0.0006457180746350119,
                3.2352199198668475e-06, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (51.158210197790815, 0.46682905098029615, (
                0.46682905098029615, 0.20335432370819806, 0.02027318232522915,
                3.476466724902457e-05, 0.0)),
        },
    },
    15: {"rows": 702, "months": (0, 175, 350, 525, 701),
        "result_cf": {
            "pols_if": (215.4919259904982, 0.9867242131750941, (
                0.9867242131750941, 0.5777091585775392, 0.19502618617942002,
                0.0019026725706875376, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (102568.1421594716, 46551.61020401425, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (41466.58734032941, 3649.0037853478634, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (46551.61020401425, 46551.61020401425, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (14549.944615127932, 1789.1377619365628, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (11212.375487266472, 71.69307989772366, (
                59.10379088933828, 44.094016862309154, 0.0, 0.0, 0.0)),
            "claims_lapse": (14708.798001472016, 155.78228490881003, (
                151.05756995443275, 17.131636196885133, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2002.757957479185, 6.578161421167294, (
                6.578161421167294, 5.520872240337301, 2.671659310804569,
                0.03736301456252825, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-130492.07360568926, 46655.972133303985, (
                -216.73952226493833, -66.74652529953158, -2.671659310804569,
                -0.03736301456252825, 0.0)),
        },
        "result_pols": {
            "pols_if": (215.4919259904982, 0.9867242131750941, (
                0.9867242131750941, 0.5777091585775392, 0.19502618617942002,
                0.0019026725706875376, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.82597799999996, 1.0, (
                0.006697, 0.030541, 0.124275, 0.469427, 1.0)),
            "mort_rate_mth": (35.5022046666155, 1.0, (
                0.0005598037122176436, 0.002581420308989446, 0.010997675514194838,
                0.05144592202933218, 1.0)),
            "lapse_rate": (4.538552150739933, 0.0303552164680678, (
                0.019811001410437235, 0.012, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.3818143858806353, 0.0025654932410160702, (
                0.0016660996963493435, 0.0010055425391276573, 0.0, 0.0, 0.0)),
            "pols_death": (0.7050182396823059, 0.002391007587789323, (
                0.0005523718774704512, 0.0014913101546412642, 0.002144834712372211,
                9.788474471894008e-05, 0.0)),
            "pols_lapse": (0.2817059734927896, 0.0021270578991404005, (
                0.0016430606053342437, 0.0005794115583938364, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (214.50520177732312, 0.9845287806922893, (
                0.9845287806922893, 0.5756384368645042, 0.19288135146704782,
                0.0018047878259685975, 0.0)),
        },
    },
    16: {"rows": 12, "months": (0, 2, 5, 8, 11),
        "result_cf": {
            "pols_if": (4.554486125517145e-13, 4.554486125517145e-13, (
                4.554486125517145e-13, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1.0033131221551412e-07, 1.0033131221551412e-07, (
                1.0033131221551412e-07, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3.036324083678097e-12, 3.036324083678097e-12, (
                3.036324083678097e-12, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-1.003343485395978e-07, 1.003343485395978e-07, (
                -1.003343485395978e-07, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (4.554486125517145e-13, 4.554486125517145e-13, (
                4.554486125517145e-13, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (12.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "mort_rate_mth": (12.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lapse_rate": (0.7200000000000002, 0.06, (
                0.06, 0.06, 0.06, 0.06, 0.06)),
            "lapse_rate_mth": (0.061716153981875355, 0.005143012831822946, (
                0.005143012831822946, 0.005143012831822946, 0.005143012831822946,
                0.005143012831822946, 0.005143012831822946)),
            "pols_death": (4.554486125517145e-13, 4.554486125517145e-13, (
                4.554486125517145e-13, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    17: {"rows": 608, "months": (0, 151, 303, 455, 607),
        "result_cf": {
            "pols_if": (140.13085085168868, 0.7608935974654959, (
                0.7608935974654959, 0.45834887697500926, 0.10965288487997003,
                0.0005205581623547499, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (109581.10800109095, 7054.4387859738745, (
                0.0, 4335.787346587619, 0.0, 0.0, 0.0)),
            "wd_guar": (65338.1259524601, 7054.4387859738745, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (44242.98204863085, 4565.5347453082395, (
                0.0, 4335.787346587619, 0.0, 0.0, 0.0)),
            "claims_death": (8640.47137175903, 101.08929114795588, (
                101.08929114795588, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (5306.7566491789, 123.94869833439347, (
                123.94869833439347, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1219.2320887344094, 5.072623983103306, (
                5.072623983103306, 4.16914390118049, 1.3636609501117753,
                0.008850977382929268, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-124747.56811076328, 7262.9755940082005, (
                -230.11061346545267, -4339.956490488799, -1.3636609501117753,
                -0.008850977382929268, 0.0)),
        },
        "result_pols": {
            "pols_if": (140.13085085168868, 0.7608935974654959, (
                0.7608935974654959, 0.45834887697500926, 0.10965288487997003,
                0.0005205581623547499, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (188.868648, 1.0, (
                0.014982, 0.050728, 0.182331, 0.541975, 1.0)),
            "mort_rate_mth": (35.42203219051165, 1.0, (
                0.0012571561051298863, 0.004328928389496611, 0.016634892190936612,
                0.06299746621429037, 1.0)),
            "lapse_rate": (1.4844358380225626, 0.019190810725806688, (
                0.019190810725806688, 0.0, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.12446109881421075, 0.0016134756698104047, (
                0.0016134756698104047, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.6796777169701436, 0.0025847796708142064, (
                0.0009565620314079904, 0.001984159465831007, 0.0018240639184034849,
                3.279384524551644e-05, 0.0)),
            "pols_lapse": (0.0812158804953515, 0.001226139917260748, (
                0.001226139917260748, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (139.36995725422318, 0.7587108955168271, (
                0.7587108955168271, 0.45636471750917823, 0.10782882096156655,
                0.00048776431710923347, 0.0)),
        },
    },
    18: {"rows": 723, "months": (0, 180, 361, 541, 722),
        "result_cf": {
            "pols_if": (225.0412557561519, 1.0, (
                0.0, 0.6193615988347699, 0.22915706629115126, 0.0025850717749405, 0.0)),
            "premiums": (100000.0, 100000.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (93449.39133639247, 5907.961773545727, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_guar": (58139.070500646994, 5907.961773545727, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "wd_excess": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "income_payments": (35310.32083574547, 3643.752956488752, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (15433.107185991283, 91.29050122360486, (
                0.0, 68.15503794019519, 0.0, 0.0, 0.0)),
            "claims_lapse": (21919.504443003105, 205.65433019504536, (
                0.0, 32.560786005640686, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (8177.369151868098, 6006.875647016558, (
                0.0, 5.9801351199449, 3.211083595204982, 0.05246249548917506, 0.0)),
            "premium_taxes": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-38979.37211725493, 93778.6612945474, (
                0.0, -106.69595906578077, -3.211083595204982, -0.05246249548917506, 0.0)),
        },
        "result_pols": {
            "pols_if": (225.0412557561519, 1.0, (
                0.0, 0.6193615988347699, 0.22915706629115126, 0.0025850717749405, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate": (189.86615999999998, 1.0, (
                0.0, 0.024915, 0.112709, 0.43505, 1.0)),
            "mort_rate_mth": (35.505563488888804, 1.0, (
                0.0, 0.002100343875829913, 0.009915701877919347, 0.04647042515181832, 1.0)),
            "lapse_rate": (4.0287110574099465, 0.031115390716231248, (
                0.0, 0.012, 0.0, 0.0, 0.0)),
            "lapse_rate_mth": (0.3389767555555041, 0.002630680051440848, (
                0.0, 0.0010055425391276573, 0.0, 0.0, 0.0)),
            "pols_death": (0.7352941135316163, 0.0025208332858406724, (
                0.0, 0.0013008723410368325, 0.002272253152561657, 0.00012012938442945064,
                0.0)),
            "pols_lapse": (0.26470588646838383, 0.0021750746821034865, (
                0.0, 0.0006214863522535929, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_if_aft_decr": (224.04125575615194, 0.9977589954046883, (
                0.0, 0.6174392401414796, 0.2268848131385896, 0.0024649423905110496, 0.0)),
        },
    },
}
# END generated fingerprint: FIA_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is FIA's
# own: the comparison on the splice grid under both sets of References, at the contract's
# extremes, where the caps bind, on labels that are not text, on keys written as floats
# and out of order and on keys far past every frame, with a NaN sent through a Reference,
# the refusals, a zero divisor, a negative power base, the deepest call, a Reference set
# late and the runner.  Each comparison adds _fia_c4_also's calls, the codes and the keys
# no swept cell reaches.  None asks for sec_read, sec_model or s_model, which sweep every
# committed point; the grid test alone asks for splices.


def _quiet(cell, *args):
    """``cell(*args)``, whatever it raises dropped: a key ``_fia_c4_also`` reads may be one
    the cell refuses, which the refusal test holds, and C4's ``also`` must not raise."""
    try:
        cell(*args)
    except Exception:                           # refused; the refusal test holds it
        pass


def _fia_c4_also(proj):
    """What C4 compares of an ``FIA_US_SEC`` point beyond its full sweep (M21).

    ``sec_support.full_sweep`` reaches a cell of more than ``t`` only at the keys some
    swept cell asks of it, and an engine cell at none.  So, as ``sample_sec.py`` does,
    this calls, at ``t = 0 .. proj_len()``, each timed cell at every code of its family
    (:data:`TIMED`), each kinded cell at the three kinds and ``claims`` and
    ``claims_over_av`` at ``ALL``; the four engine cells at the arguments this module
    sweeps ``FIA_US_S``'s at (:func:`_sweep_s`); and every keyed reader at every key its
    cache holds, ``payout_rate_at``, ``mort_rate_base_at`` and ``activation_rate`` at ages
    0 to 122, the year and anniversary readers and both scenario columns at 0 to 82, and
    ``wd_scheduled_at`` at 0 to 81, so that the payout band boundaries 54/55 and 59/60,
    out of the anchor's reach, and every key past a table's last row run compiled.  A key
    a reader refuses is dropped (:func:`_quiet`): the refusal test holds those.  Passed
    to ``sec_support.compiled_mismatches`` as ``also``; it lives here, as M18's module
    keeps its own, so that the shared module holds only shared machinery.
    """
    kinds = [_code(proj, kind) for kind in KINDS]
    total = _code(proj, "ALL")
    for t in range(proj.proj_len() + 1):
        for cell, labels in TIMED.items():
            for label in labels:
                proj.cells[cell](t, _code(proj, label))
        for cell in KINDED:
            for kind in kinds:
                proj.cells[cell](t, kind)
        proj.claims(t, total)
        proj.claims_over_av(t, total)
    for a in range(SPEC_SIZES["a"] - 1):
        for cell in ("payout_rate_at", "mort_rate_base_at", "activation_rate"):
            _quiet(proj.cells[cell], a)
    names = [_code(proj, "INDEX_LEVEL"), _code(proj, "MVA_REF_YIELD")]
    for y in range(SPEC_SIZES["y"]):
        for cell in ("surr_charge_rate_py", "vest_rate_py", "rollup_rate_py",
                     "index_level", "mva_ref_yield"):
            _quiet(proj.cells[cell], y)
        for name in names:
            _quiet(proj.scenario_value, y, name)
    for k in range(SPEC_SIZES["k"]):
        _quiet(proj.wd_scheduled_at, k)
    for method in ("cap", "par", "par_cap", "spread", "trigger"):
        for r in (-0.1, 0.0, 0.03, 0.1):
            proj.credit_rate_on(r, method)
    for basis in ("single", "joint"):
        for a in range(40, 122):
            proj.payout_rate(a, basis)
    for args in ((0.0, 0.0), (0.02, 0.0), (0.04, 0.01), (0.08, 0.0), (0.08, 0.02)):
        proj.mgsv_rate_statutory(*args)
        proj.mgsv_rate_is_compliant(*args)


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _copied(folder, file):
    """An edit that replaces ``file`` with the copy in ``folder``, as written there."""
    return lambda _: pd.read_csv(pathlib.Path(folder) / file)


def _sec_refs(model, refs):
    """``refs`` as the SEC model takes them: each of S's switch settings as its code
    (:func:`_switch`), every other value as it is."""
    return {ref: _switch(model.Projection, ref, value) for ref, value in refs.items()}


def _mismatch_text(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# How many rows C4 compares at once, on the splice grid and on every case of more rows
# (_chunked_mismatches).  compiled_mismatches sweeps every row of its case in one modelx
# read, _fia_c4_also's calls with it, and keeps every value of every row, in the parent
# and in the child, until it compares them.  An FIA row runs up to 723 months on the grid,
# against MYGA's 495, and a point holds about 200 cells a month and the timed cells at
# every code: about 135 MB of modelx a committed point, swept with _fia_c4_also.  Eight
# rows at a time peaked near 6 GB in one process, and so did the committed points' 18
# swept at once, so FIA compares four, a fifth of MYGA's twenty (USLIB-SEC-PLAN.md §7.2,
# *For M16 and later*, item 7; measured at M21, under load).
C4_CHUNK = 4


def _chunked_mismatches(build, dest, table=None, *, edits=None, refs=None,
                        also=_fia_c4_also):
    """``compiled_mismatches`` on ``table``, the committed table by default,
    :data:`C4_CHUNK` rows at a time.

    Each chunk is a case of its own under ``dest`` (``sec_support.compiled_case``), on the
    same ``edits``, compared under the same ``refs`` with the same ``also`` and removed once
    compared, so that a run holds one chunk's sweep at a time.  A point's projection reads
    its own row alone, so a chunk projects each of its rows as the whole table does.
    Returns every chunk's lines, each prefixed with its chunk's first ``point_id``.
    """
    table = _committed() if table is None else table
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table)
    found = []
    for i, chunk in enumerate(chunks):
        where = pathlib.Path(dest) / f"chunk{i}"
        folder = compiled_case(build, where, model_points=chunk, edits=edits)
        found += [f"from point_id {chunk.index[0]}: {line}"
                  for line in compiled_mismatches(build, folder, refs=refs, also=also)]
        shutil.rmtree(where)
    return found


@pytest.mark.parametrize("which", ["spliced", "switched"])
@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(splices,
                                                                             sec_build,
                                                                             tmp_path,
                                                                             which):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's rows, S's points and variants restated in force at T2's
    months and issued later, each crediting method, the female table, the programmes, the
    exercises either side of two band boundaries, under :data:`SPLICED_REFS`, and the
    switched grid under :data:`SWITCHED_REFS`, the step-up at exercise, the dollar rollup
    base, the surrender-value collar and every cap and floor S ships idle, the switches
    set as their codes; on the splice's stepped scenarios, re-based to each row's month,
    its programmes and its cut mortality.  The grid is the one this run's ``splices``
    selects, the core by default and the full grid under ``USLIB_SEC_FULL=1``, and the
    test carries no ``sec_full`` mark, since a skipped compile test fails the cython job.
    The grid's SEC table goes beside the build :data:`C4_CHUNK` rows at a time; modelx
    sweeps every row fully, with :func:`_fia_c4_also`'s calls, and the compiled model
    must agree at every argument modelx caches, identically on x86-64 and to 1e-12
    relative elsewhere, with every raise and every ``Data`` array
    (``sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    _, sec = splices.pair(which)
    here = sec.Data.input_dir()
    refs = _sec_refs(sec, REFS[which])
    table = pd.read_csv(here / TABLE, index_col="point_id")
    assert len(table) == len(sec.Data.model_point_table())
    edits = {file: _copied(here, file) for file in (*SEC_EDITS, COMPANION)}
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table) and len(chunks) > 1
    found = []
    for i, chunk in enumerate(chunks):
        folder = compiled_case(build, tmp_path / f"grid{i}", model_points=chunk,
                               edits=edits)
        found += compiled_mismatches(build, folder, refs=refs, also=_fia_c4_also)
        shutil.rmtree(tmp_path / f"grid{i}")
    assert not found, _mismatch_text(found)


def _far_programme(table):
    """The shipped programmes and ``far``, with withdrawals at counts 0, 40 and 80, the
    last a contract issued at 40 reaches, each its own amount."""
    rows = [("far", 0, 1100.0), ("far", 40, 1600.0), ("far", 80, 1900.0)]
    added = pd.DataFrame(rows, columns=["wd_schedule_id", "t", "wd_amount"]).assign(
        provenance="test copy")
    return pd.concat([table, added], ignore_index=True)


def _late_rollup_steps(table):
    """The shipped schedules and ``long``, stepping at years 1, 40 and 81, the last
    contract year a contract issued at 40 reaches, each its own rate."""
    rows = [("long", 1, 0.031), ("long", 40, 0.017), ("long", 81, 0.009)]
    added = pd.DataFrame(rows, columns=["rollup_id", "contract_year", "rollup_rate"])
    return pd.concat([table, added.assign(provenance="test copy")], ignore_index=True)


def _scenario_from_120(table):
    """The companion with ``worked-F120``, the anchor's path moved 120 months on, the
    shipped horizon, so that its first level is in the issue month of a point issued
    then."""
    worked = table[table["scenario_id"] == "worked"]
    later = worked.assign(scenario_id="worked-F120", t=worked["t"] + 120)
    return pd.concat([table, later], ignore_index=True)


EXTREME_EDITS = {"mort_table.csv": _mortality_from(30), COMPANION: _scenario_from_120,
                 "withdrawal_table.csv": _far_programme,
                 "rollup_table.csv": _late_rollup_steps}

# The frames of the contract's extremes, in _contract_extremes' order.
EXTREME_FRAMES = [972, 1092, 972, 492, 612, 1, 972, 972, 972, 972]


def _contract_extremes():
    """The table for the contract's longest frames, its oldest issue age and the bounds of
    its tables, made from the committed points.

    Issued at 40, ``issue_age_min``, the youngest issue age, cover runs 972 months: the
    anchor issued now, withdrawing on ``far``'s programme at counts 0, 40 and 80 and
    rolling up on ``long``'s schedule to year 81; and issued 120 months on, the shipped
    ``future_horizon_mth``, a frame of 1,092 months, the longest the contract allows,
    which reads every cache as far as ``spec_sec.py`` sizes it, ``t`` to 1,092 in C4's
    sweep of the month after it, the contract year and the anniversary to 81 and the
    attained age to 121 at exercise, on ``worked-F120``, a scenario that sets its first
    level in the point's issue month; the joint basis at 40 with a joint age of 30,
    below every band; and S's point without the rider at 40.  Then at 80,
    ``issue_age_max``, the oldest, issued now and 120 months on.  The point without the
    rider in its last covered month at issue age 40, policy month 971, a frame of one
    month, its state that of the committed row in its last covered month.  And the
    anchor at 40 exercising at 54, 55, 59 and 60, either side of the payout bands'
    boundaries 54/55 and 59/60, which no committed exercise reaches.

    The shipped tables stop short of such policies, so the copies extend them
    (:data:`EXTREME_EDITS`), each added key with values of its own: the mortality from
    30 (:func:`_mortality_from`), for the joint age.
    """
    committed = _committed()

    def row(kind, s_point, month, **columns):
        return committed.loc[[_label(committed, kind, s_point, month)]].assign(**columns)

    rows = pd.concat([
        row("twin", 2, 0, age_at_entry=40, wd_schedule_id="far", rollup_id="long"),
        row("twin", 2, 0, age_at_entry=40, duration_mth=-120, scenario_id="worked-F120",
            wd_schedule_id="far", rollup_id="long"),
        row("twin", 5, 0, age_at_entry=40, joint_age=30),
        row("twin", 2, 0, age_at_entry=80),
        row("twin", 6, 0, age_at_entry=80, duration_mth=-120, scenario_id="worked-F120"),
        row("derived", 6, 696, age_at_entry=40, duration_mth=971),
        *[row("twin", 2, 0, age_at_entry=40, income_start_age=age)
          for age in (54, 55, 59, 60)]])
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames, every cell compiled.

    The ten points of :func:`_contract_extremes`, the longest frames the contract allows,
    its youngest and oldest issue ages and the bounds of its tables, read every cache as
    far as ``spec_sec.py`` sizes it: ``t`` to 1,092, the month after the 1,092-month
    frame, the contract year and the anniversary to 81, the count of completed years to
    80 and the attained age to 121; a scenario from a first month above 0, a withdrawal
    programme and a rollup schedule to the last year, and the payout bands either side of
    two boundaries.  modelx sweeps each fully, with :func:`_fia_c4_also`'s calls, and the
    compiled model must agree everywhere, every raise included.  A cache one too small for
    the contract raises ``IndexError`` compiled where modelx reads on, and fails here,
    though the spec check passes it, which holds the caches to the spec and not the spec
    to the contract.  Under the shipped References, and with ``USLIB_SEC_FULL=1`` again
    under :data:`SWITCHED_REFS`.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "extremes", model_points=_contract_extremes(),
                           edits=EXTREME_EDITS)
    model = _read(folder, "extremes_frames")
    try:
        points = [projection(model, key) for key in point_keys(model)]
        frames = [p.proj_len() for p in points]
        longest = points[1]
        assert longest.t_entry() == 120 and longest.age(1091) == 120
        exercised = [next(t for t in range(p.proj_len()) if p.is_exercise(t))
                     for p in points[6:]]
        assert [p.exercise_age(t) for p, t in zip(points[6:], exercised)] == [
            54, 55, 59, 60]
        coded = _sec_refs(model, SWITCHED_REFS)
    finally:
        model.close()
    assert frames == EXTREME_FRAMES, frames
    found = []
    for i, refs in enumerate(({}, coded) if SEC_FULL else ({},)):
        found += _chunked_mismatches(build, tmp_path / f"extremes_c4_{i}",
                                     _contract_extremes(), edits=EXTREME_EDITS, refs=refs)
    assert not found, _mismatch_text(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_caps_bind(sec_build,
                                                                              tmp_path):
    """C4 where a cap binds: the mortality's cap and the rider charge's, the lapse's.

    FIA's caps are ``min``s whose other side the committed points rarely reach: the
    annual mortality, ``min(q, 1.0)``, binds at age 120 alone under the shipped factor,
    and from 115 on the anchor at :data:`CAPPED_REFS`' 1.25; the rider charge's cap
    ``rider_charge_rate_max`` and the lapse's ``lapse_rate_max`` bind under
    :data:`SWITCHED_REFS`.  So every committed point runs under :data:`CAPPED_REFS`,
    and under the switched References with the mortality factor at 1.25 beside them:
    in modelx the mortality's cap binds, its uncapped product past 1, on some point and
    month, and so do the other two.  modelx sweeps each point fully, and the compiled
    model must agree at every argument modelx caches, identically on x86-64 and to
    1e-12 relative elsewhere, on both sides of every cap.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "capped")
    switched = {**SWITCHED_REFS, "mort_ae_factor": 1.25}
    bound = set()
    for i, refs in enumerate((CAPPED_REFS, switched)):
        model = _read(folder, "capped", refs)
        try:
            for key in point_keys(model):
                p = projection(model, key)
                for t in range(p.proj_len()):
                    if not p.is_active(t):
                        continue
                    q = p.mort_ae_factor * p.mort_rate_base_at(p.age(t))
                    if q > 1.0 and p.mort_rate(t) == 1.0:
                        bound.add("mortality")
                    if p.lapse_rate(t) == p.lapse_rate_max > 0.0:
                        bound.add("lapse")
                if p.rider_charge_rate > p.rider_charge_rate_max and any(
                        p.rider_charge_pp(t) > 0.0 for t in range(p.proj_len())):
                    bound.add("rider charge")
                _release(model, key)
            coded = _sec_refs(model, refs)
        finally:
            model.close()
        found = _chunked_mismatches(build, tmp_path / f"capped_c4_{i}", refs=coded)
        assert not found, _mismatch_text(found)
    assert bound == {"mortality", "lapse", "rider charge"}, bound


# The labels Data accepts that are not text: the four a projection does not join on,
# blank, read by pandas as NaN; and the four it joins on, sex, rollup_id, scenario_id and
# wd_schedule_id, as numbers, which pandas reads as ints, on tables keyed by numbers.
NUMBERED_FILES = {"sex": "mort_table.csv", "rollup_id": "rollup_table.csv",
                  "scenario_id": COMPANION, "wd_schedule_id": "withdrawal_table.csv"}


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

    ``blank``: S's anchor in force; its twin issued now with a blank ``policy_id`` and
    ``tax_status``, which no cell reads, so that it projects; and the point in its last
    covered month, a frame of one month, since modelx sweeps a raise in every cell of
    every month, twice, once with a blank ``glwb_basis``, which its projection does not
    read without the rider, and once with a blank ``credit_method``, which the credit
    refuses, as S's does.  ``numeric``: the committed table with its sex, rollup,
    scenario and programme keys numbers, on tables keyed by the same numbers
    (:func:`_numbering`).
    """
    committed = _committed()
    last = committed.loc[[_label(committed, "derived", 6, 696)]].assign(duration_mth=707)
    blank = pd.concat([
        committed.loc[[_label(committed, "twin", 1, 84)]],
        committed.loc[[_label(committed, "twin", 2, 0)]].assign(policy_id=None,
                                                                 tax_status=None),
        last.assign(glwb_basis=None), last.assign(credit_method=None)])
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

    ``Data`` accepts a blank label where no cell reads it, and keys that are numbers on
    tables keyed by numbers, since ``FIA_US_S`` projects such a point; and it accepts a
    blank decoded label, which the point's projection refuses where it asks for it.
    modelx returns each label as pandas reads it, NaN or an int, and an accessor typed
    ``str`` would raise ``TypeError`` compiled; the sample types the eight as Python
    objects (sample_sec.py).  So on each case of :func:`_labels_not_text`, after checking
    that the file reads as the case says, modelx sweeps every point fully, with every code
    where no cell raises (:func:`_fia_c4_also`), and the compiled model must agree
    everywhere, the label accessors and every raise included.
    """
    build = sec_build(SEC)
    found = []
    for case, rows, edits in _labels_not_text():
        folder = compiled_case(build, tmp_path / case, model_points=rows, edits=edits)
        model = _read(folder, f"labels_{case}")
        try:
            points = [projection(model, key) for key in point_keys(model)]
            if case == "blank":
                assert math.isnan(points[1].policy_id()) and math.isnan(
                    points[1].tax_status())
                assert points[1].result_cf() is not None
                assert math.isnan(points[2].glwb_basis())
                assert points[2].result_cf() is not None
                assert math.isnan(points[3].credit_method())
                _refused(points[3].result_cf, "invalid credit_method")
            else:
                for column in NUMBERED_FILES:
                    got = [p.cells[column]() for p in points]
                    assert all(isinstance(v, (int, np.integer)) for v in got), got
                assert all(np.isfinite(p.result_cf().to_numpy()).all() for p in points)
        finally:
            model.close()
        also = _fia_c4_also if case == "numeric" else None
        found += [f"{case}: {line}" for line in _chunked_mismatches(
            build, tmp_path / f"{case}_c4", rows, edits=edits, also=also)]
    assert not found, _mismatch_text(found)


def _float_keys_apart(column, *more):
    """An edit that writes a table in reverse key order with its keys as floats."""
    def edit(table):
        table = table.iloc[::-1].reset_index(drop=True)
        return table.assign(**{c: table[c].astype(float) for c in (column, *more)})
    return edit


KEYS_APART = {"mort_table.csv": _float_keys_apart("age"),
              "surr_charge_table.csv": _float_keys_apart("contract_year"),
              "rollup_table.csv": _float_keys_apart("contract_year"),
              "payout_rate_table.csv": _float_keys_apart("age_lo", "age_hi"),
              COMPANION: _float_keys_apart("t"),
              "withdrawal_table.csv": _float_keys_apart("t")}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                        tmp_path):
    """C4 on tables written out of key order, with keys as floats.

    ``Data`` numbers each table's keys by their sorted order and reads each row's value
    at its key, read by value; :func:`test_table_keys_written_as_floats_are_read_by_value`
    holds the model to the committed one on floats.  This holds the compiled ``Data``,
    and every projection on it, to modelx, on :data:`KEYS_APART`'s copy, every input
    table in reverse order with its keys as floats, ``1.0``, and the model point table's
    whole numbers as floats: modelx sweeps every committed point fully, and every ``Data``
    array and every cell compiled must agree.
    """
    build = sec_build(SEC)
    table = _committed()
    table = table.assign(**{c: table[c].astype(float) for c in (
        "duration_mth", "age_at_entry", "income_start_age", "joint_age",
        "phase_prev_anniv_init")})
    found = _chunked_mismatches(build, tmp_path / "keys", table, edits=KEYS_APART)
    assert not found, _mismatch_text(found)


def _far_rows(column, row):
    """An edit that appends ``row``, a dict, beside the table's rows, at ``column``'s far
    key."""
    return lambda table: pd.concat([table, pd.DataFrame([row])], ignore_index=True)


# A key at 1e10, far past every frame, in the three tables keyed by a month or a year
# without a check of their last key: a scenario level of the anchor's re-based path, a
# withdrawal of the anchor's programme and a step of the blended rollup schedule.
FAR_KEYS = {COMPANION: _far_rows("t", {"scenario_id": "worked-M84", "t": 1e10,
                                       "index_level": 9999.0, "mva_ref_yield": 0.09,
                                       "provenance": "test copy"}),
            "withdrawal_table.csv": _far_rows("t", {"wd_schedule_id": "none", "t": 1e10,
                                                    "wd_amount": 777.0,
                                                    "provenance": "test copy"}),
            "rollup_table.csv": _far_rows("contract_year", {
                "rollup_id": "blended", "contract_year": 1e10, "rollup_rate": 0.09,
                "provenance": "test copy"})}


@pytest.mark.cython
def test_the_compiled_model_holds_a_far_key_as_modelx_does(sec_build, tmp_path):
    """C4 with a scenario level, a withdrawal and a rollup step at 1e10 (:data:`FAR_KEYS`).

    ``Data`` holds the arrays to ``read_last_mth``, and its contract year and count, and
    projects as though the rows were not there: in modelx, every committed point's
    ``result_cf`` is the committed model's, bit for bit; and compiled, every committed
    point, swept fully, and every ``Data`` array, as in modelx.
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
    found = _chunked_mismatches(build, tmp_path / "far_c4", edits=FAR_KEYS)
    assert not found, _mismatch_text(found)


# A NaN sent through a Reference, set before the model computes anything, which a compiled
# model runs as modelx does, and a cell of the anchor issued now it reaches as NaN: the
# mortality's factor, which the cap holds NaN, and the rider charge's rate, which its cap,
# kept in S's order, holds NaN too, from the first anniversary's charge.
NAN_REFS = ((NAN_FACTOR, ("mort_rate", 0)),
            ({"rider_charge_rate": float("nan")}, ("rider_charge_pp", 11)))


@pytest.mark.cython
def test_the_compiled_model_carries_a_nan_reference_as_modelx_does(sec_build, tmp_path):
    """C4 with a NaN sent through each of :data:`NAN_REFS`: compiled, the same NaNs.

    :func:`test_a_nan_that_reaches_the_cap_on_mortality_stays_nan` and
    :func:`test_a_residual_that_is_not_a_number_fails_its_check` hold modelx to what a
    NaN must do at the caps and the checks.  A compiled ``min`` of two doubles keeps its
    first argument where no comparison holds, as Python's does, and a compiled check
    compares as modelx's, so here every committed point, under each Reference, swept
    fully, must be modelx's in every cell, a NaN where modelx has one, and the checks
    ``False`` where modelx's are.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "nan")
    found = []
    for i, (refs, (cell, t)) in enumerate(NAN_REFS):
        model = _read(folder, "nan_refs", refs)
        try:
            assert math.isnan(_row(model, "twin", 2, 0).cells[cell](t)), refs
        finally:
            model.close()
        found += [f"{refs}: {line}" for line in _chunked_mismatches(
            build, tmp_path / f"nan_c4_{i}", refs=refs, also=None)]
    assert not found, _mismatch_text(found)


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (position, cell, arguments,
# what modelx does).  modelx answers a month outside cover with a zero, or computes it
# where the point was in force then, a key past a reader's array with its refusal or with
# what the table's last row holds, and one below 0 with a zero, the column or a refusal,
# as the cells say, and refuses a code past the timings, the kinds and the names;
# compiled, each is past a cache, and raises IndexError rather than read or write beyond
# it.  The timing, kind and name caches are twelve wide (spec_sec.py), so their first code
# past the cache is 12.  Position 0 is S's anchor in force at 84.
COMPILED_ONLY = [
    (0, "net_cf", (1094,), ("ok", 0.0)),
    (0, "net_cf", (-1,), ("ok", -348.13391814693523)),
    (0, "pols_if_at", (0, 12), ("raised", "ValueError: invalid timing")),
    (0, "av_at", (0, 12), ("raised", "ValueError: invalid timing")),
    (0, "claims", (0, 12), ("raised", "ValueError: invalid kind")),
    (0, "claims_over_av", (0, 12), ("raised", "ValueError: invalid kind")),
    (0, "scenario_value", (8, 12), ("raised", "ValueError: invalid name")),
    (0, "scenario_value", (83, 0), ("ok", 5450.0)),
    (0, "scenario_value", (-1, 0), ("raised", "ValueError: point_id 1: scenario sets no "
                                    "level by month -96")),
    (0, "index_level", (-1,), ("ok", 5000.0)),
    (0, "index_level", (83,), ("ok", 5450.0)),
    (0, "mva_ref_yield", (83,), ("ok", 0.035)),
    (0, "mva_ref_yield", (-1,), ("raised", "ValueError: point_id 1: scenario sets no "
                                 "level by month -96")),
    (0, "surr_charge_rate_py", (83,), ("ok", 0.0)),
    (0, "surr_charge_rate_py", (-1,), ("raised", "ValueError: point_id 1: the surrender "
                                       "charge table gives no rate at contract year -1")),
    (0, "vest_rate_py", (83,), ("ok", 1.0)),
    (0, "vest_rate_py", (-1,), ("raised", "ValueError: point_id 1: the surrender charge "
                                "table gives no vesting at contract year -1")),
    (0, "rollup_rate_py", (83,), ("ok", 0.0)),
    (0, "rollup_rate_py", (-1,), ("ok", 0.0)),
    (0, "payout_rate_at", (123,), ("raised", "ValueError: point_id 1: the payout bands "
                                   "are held to age 122, Data.read_last_age, and no "
                                   "projection reads age 123")),
    (0, "payout_rate_at", (-1,), ("ok", 0.0)),
    (0, "mort_rate_base_at", (123,), ("raised", "ValueError: point_id 1: the mortality "
                                      "table gives no rate at attained age 123")),
    (0, "mort_rate_base_at", (-1,), ("raised", "ValueError: point_id 1: the mortality "
                                     "table gives no rate at attained age -1")),
    (0, "wd_scheduled_at", (82,), ("ok", 0.0)),
    (0, "wd_scheduled_at", (-1,), ("ok", 0.0)),
    (0, "activation_rate", (123,), ("ok", 0.15)),
    (0, "activation_rate", (-1,), ("ok", 0.0)),
]

# The codes inside the timing, kind and name caches that a cell does not take, since one
# numbering serves the three timing families and every 2-D cache is timing's width
# (spec_sec.py): there the cell itself refuses the code, compiled as in modelx.  As
# (cell, the code's name or number).
CODES_IN_CACHE = [("pols_if_at", "BEF_PREM"), ("pols_if_at", "EOY"), ("pols_if_at", 11),
                  ("av_pp_at", "BEF_NB"), ("av_pp_at", "BEF_ROLLUP"),
                  ("av_fixed_pp_at", "AFT_DECR"), ("av_indexed_pp_at", "BEF_STEP_UP"),
                  ("av_at", "BEF_MORT"), ("benefit_base_pp_at", "BEF_PREM"),
                  ("benefit_base_pp_at", "BEF_DECR"), ("lw_pp_at", "BEF_ROLLUP"),
                  ("lw_pp_at", "BEF_FEE"), ("pols_decr", "ALL"), ("claim_pp", "ALL"),
                  ("claim_from_av_pp", "ALL"), ("claims_from_av", "ALL"), ("claims", 4),
                  ("claims_over_av", 11), ("pols_decr", 7)]

# The scenario's codes inside its cache that name no column, on S's anchor in force, at
# its anniversary 8, the month after the valuation date's 7.
NAMES_IN_CACHE = (2, 5, 11)

# Each switch Reference's codes that name no setting, beside its two: refused by the cell
# that branches on its decodes, with FIA_US_S's message, compiled as in modelx, on the
# anchor issued now.
SWITCH_CODES = {"step_up_mode": ("invalid step_up_mode", (2, -1)),
                "rb_wd_convention": ("invalid rb_wd_convention", (2, -1)),
                "mva_collar_basis": ("invalid mva_collar_basis", (2, -1))}

# The whole-number columns Data holds as int64 vectors, each refused at 2**53 before the
# cast, naming its point.
WHOLE = ("age_at_entry", "income_start_age", "joint_age", "duration_mth")


def _with_key(columns, value):
    """An edit that appends a copy of a table's first row with ``columns`` at ``value``."""
    def edit(table):
        return pd.concat([table, table.iloc[[0]].assign(**dict.fromkeys(columns, value))],
                         ignore_index=True)
    return edit


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, the References, [(position, cell, arguments)], the Data cells to read).

    A position, not a label, since a table ``Data`` refuses has no keys to give: each is
    the row's place in the table written, ``Projection``'s ``idx``, which the test indexes
    ``Projection`` by in modelx too.
    """
    committed, relabeled = _committed(), _relabeled(_committed())

    def at(table, label):
        return list(table.index).index(label)

    twin = _label(committed, "twin", 2, 0)
    rider_less = _label(committed, "twin", 6, 0)
    mid_year = _label(committed, "derived", 1, 95)
    cases = [
        ("the scenario read before its first month", committed, None, {},
         [(at(committed, mid_year), "scenario_value", (7, "INDEX_LEVEL")),
          (at(committed, mid_year), "mva_ref_yield", (7,))], ()),
        ("an age outside the mortality table", committed, None, {},
         [(0, "mort_rate_base_at", (39,)), (0, "mort_rate_base_at", (121,))], ()),
        ("codes no cell of the family takes, inside the caches", committed, None, {},
         [(0, cell, (0, code)) for cell, code in CODES_IN_CACHE]
         + [(0, "scenario_value", (8, code)) for code in NAMES_IN_CACHE], ()),
        ("a label at 2**53, relabeled", relabeled.rename(index={101: 2 ** 53}), None, {},
         [(at(relabeled, 101), "point_id", ())], ("point_id",)),
        ("a label written as text, relabeled", relabeled.rename(index={107: "7x"}), None,
         {}, [(at(relabeled, 107), "point_id", ())], ("point_id",)),
        ("no glwb_basis column", committed.drop(columns="glwb_basis"), None, {},
         [(at(committed, twin), "result_cf", ()), (at(committed, rider_less), "net_cf",
                                                   (0,))], ()),
        ("no credit_method column", committed.drop(columns="credit_method"), None, {},
         [(at(committed, twin), "result_cf", ())], ()),
    ]
    for column in WHOLE:
        cases.append((f"{column} at 2**53", _set(column, [twin], 2 ** 53)(committed), None,
                      {}, [(at(committed, twin), "result_cf", ())],
                      ("model_point_table",)))
    for source, columns in (("mort_table.csv", ("age",)),
                            ("surr_charge_table.csv", ("contract_year",)),
                            ("rollup_table.csv", ("contract_year",)),
                            ("payout_rate_table.csv", ("age_lo", "age_hi")),
                            (COMPANION, ("t",)), ("withdrawal_table.csv", ("t",))):
        cases.append((f"{source} {' and '.join(columns)} at 2**53", committed,
                      {source: _with_key(columns, 2.0 ** 53)}, {},
                      [(at(committed, twin), "result_cf", ())], (CHECKED[source][1],)))
    for ref, (message, values) in SWITCH_CODES.items():
        for value in values:
            cases.append((f"{ref} {value}", committed, None, {ref: value},
                          [(at(committed, twin), "result_cf", ())], ()))
    for case, row, columns, refs, inputs, message in NOT_ISSUED:
        if message is None:
            continue
        label = 100 + _label(committed, *row)
        table = _cells(label, **columns)(relabeled)
        cases.append((case, table, inputs, refs, [(at(table, label), "result_cf", ())], ()))
    for case, columns, refs, message in UNDECODABLE:
        if refs:
            continue                            # a text Reference, which compiles as a code
        cases.append((case, _cells(twin, **columns)(committed), None, {},
                      [(at(committed, twin), "result_cf", ())], ()))
    for case, edit, _ in MALFORMED:
        cases.append((case, edit(committed), None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, source, edit, _, s_point in TABLE_FAULTS:
        twin_of = at(committed, _label(committed, "twin", s_point, 0))
        cases.append((case, committed, {source: edit}, {}, [(twin_of, "result_cf", ())],
                      (CHECKED[source][1],)))
    return cases


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs
    (:func:`_refusal_cases`): ``proj_len()`` refuses a point past its cover, relabeled
    ``100 + point_id`` in reverse order, where a label is no position, and every refusal
    of :data:`NOT_ISSUED`, the issue ages below ``issue_age_min`` and above
    ``issue_age_max`` and the mortality that stops short of ``maturity_age`` among them,
    which the compiled caches are not sized for, relabeled too; the scenario read before
    its first month and the mortality outside its ages are refused by name; a label at
    ``2**53`` or written as text by ``Data.point_id``, a whole number at ``2**53`` in each
    of the four integer columns by the table and in each key of the six tables by the
    table's check; a table without ``glwb_basis`` refused where a rider point asks for the
    basis, pandas' ``KeyError``, while a point without the rider projects, and one
    without ``credit_method`` at the first credit, as ``FIA_US_S`` refuses them (N7);
    each switch Reference set to a code that names no setting, and each text value of
    :data:`UNDECODABLE`'s columns, by the projection, with S's message; and every case of
    :data:`MALFORMED` and of :data:`TABLE_FAULTS` is refused by a projection, and by the
    ``Data`` cell that checks it, compiled as in modelx, so a compiled ``Data`` cell
    refuses each value its modelx cell refuses; and a code a cell does not take, inside
    its cache, is refused by the cell (:data:`CODES_IN_CACHE`, :data:`NAMES_IN_CACHE`).

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past the timing, kind and name caches, an
    anniversary or a contract year past the ``y`` cache either side, a count past the
    ``k`` cache and an age past the ``a`` cache, each raising ``IndexError`` compiled,
    beside what modelx does.

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    cases.append(("compiled only", _committed(), None, {},
                  [(idx, cell, args) for idx, cell, args, _ in COMPILED_ONLY], ()))
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused, projected = [], 0, 0
    for case, table, edits, refs, calls, data in cases:
        temp_inputs(dest, model_path(SEC), model_points=table, model_point_file=TABLE,
                    edits=edits)
        model = _read(folder, "refused", refs)
        try:
            calls = [(idx, cell, tuple(_code(model.Projection, a) if isinstance(a, str)
                                       else a for a in args))
                     for idx, cell, args in calls]
            want = [_modelx_did(lambda: model.Projection[idx].cells[cell](*args))
                    for idx, cell, args in calls]
            want_data = {name: _modelx_did(model.Data.cells[name]) for name in data}
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
                expected = next(w for i, c, a, w in COMPILED_ONLY
                                if (i, c, a) == (idx, cell, args))
                if modelx_did != expected:
                    found.append(f"{where}: modelx {modelx_did}, not {expected}")
                if (status, str(value).split(":")[0]) != ("raised", "IndexError"):
                    found.append(f"{where}: compiled {status} {value!r}, not IndexError")
                continue
            if case == "no glwb_basis column" and cell == "net_cf":
                if modelx_did[0] != "ok" or (status, value) != ("ok", modelx_did[1]):
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
    assert projected == 1
    assert refused + projected == sum(len(calls) + len(data)
                                      for *_, calls, data in cases[:-1])


@pytest.mark.cython
def test_the_compiled_model_divides_by_zero_as_modelx_does(sec_build, tmp_path):
    """Compiled, a divisor of zero raises modelx's ``ZeroDivisionError``, word for word.

    Cython's division of C doubles raises ``ZeroDivisionError("float division")``, where
    Python says ``float division by zero``; so ``mgsv_rate_statutory``, the one cell whose
    divisor a Reference can bring to zero, ``mgsv_stat_step``, tests it and raises
    Python's own message, as ``FIA_US_S``'s division does.  With the step at 0, on the
    committed anchor issued now, the statutory rate and its compliance test raise in
    ``FIA_US_S``, in modelx and compiled, each ``float division by zero``.
    """
    build = sec_build(SEC)
    refs = {"mgsv_stat_step": 0.0}
    calls = [("mgsv_rate_statutory", (0.02, 0.0)), ("mgsv_rate_is_compliant", (0.04, 0.01))]
    s = _read(model_path(TWIN), "zero_s", refs)
    try:
        theirs = [_modelx_did(lambda: _point(s, 2).cells[cell](*args))
                  for cell, args in calls]
    finally:
        s.close()
    folder = compiled_case(build, tmp_path / "zero")
    model = _read(folder, "zero_cy", refs)
    try:
        idx = list(model.Data.model_point_table().index).index(
            _label(model.Data.model_point_table(), "twin", 2, 0))
        want = [_modelx_did(lambda: model.Projection[idx].cells[cell](*args))
                for cell, args in calls]
    finally:
        model.close()
    got = run_compiled(tmp_path / "zero", build.package.name,
                       {"refs": refs, "calls": {idx: calls}})
    assert got["exit"] == 0, got["stderr"]
    assert all(got["compiled"].values()), got["compiled"]
    division = ("raised", "ZeroDivisionError: float division by zero")
    assert theirs == want == [division] * 2, (theirs, want)
    assert [tuple(did) for did in got["values"][idx]] == want


@pytest.mark.cython
def test_the_compiled_model_refuses_a_negative_power_base_as_modelx_does(sec_build,
                                                                         tmp_path):
    """Compiled, a Reference rate below -1 under a power raises modelx's refusal (M21).

    C's ``pow`` of a negative base is NaN, which a later ``max`` answers 0 to without a
    word, so each cell that takes such a power tests its base first.  On each case of
    :data:`NEGATIVE_BASES`, with the case's References set, the compiled model must raise
    what modelx raises on the same copy, the refusal
    :func:`test_a_rate_below_minus_one_that_a_power_takes_is_refused_naming_it` asserts;
    and at exactly -1, :data:`AT_MINUS_ONE`, it must compute what modelx computes, bit for
    bit, every month of the anchor's frame.
    """
    build = sec_build(SEC)
    table = _committed()
    idx = list(table.index).index(_label(table, "twin", 2, 0))
    found = []
    cases = [(case, refs, [call, ("net_cf", (1,))]) for case, refs, call, _, _
             in NEGATIVE_BASES]
    cases += [(f"at -1: {refs}", refs, [("net_cf", (t,)) for t in range(709)])
              for refs in AT_MINUS_ONE]
    for number, (case, refs, calls) in enumerate(cases):
        dest = tmp_path / f"base{number}"
        folder = compiled_case(build, dest)
        model = _read(folder, "base_cy", refs)
        try:
            want = [_modelx_did(lambda: model.Projection[idx].cells[cell](*args))
                    for cell, args in calls]
        finally:
            model.close()
        got = run_compiled(dest, build.package.name, {"refs": refs, "calls": {idx: calls}})
        assert got["exit"] == 0, f"{case}: the compiled run failed:\n{got['stderr']}"
        assert all(got["compiled"].values()), got["compiled"]
        for (cell, args), modelx_did, compiled_did in zip(calls, want, got["values"][idx]):
            same = (tuple(compiled_did) == modelx_did if modelx_did[0] == "raised" else
                    compiled_did[0] == "ok"
                    and float(compiled_did[1]).hex() == float(modelx_did[1]).hex())
            if not same:
                found.append(f"{case}: {cell}{args}: modelx {modelx_did}, compiled "
                             f"{compiled_did}")
        if case in [c[0] for c in NEGATIVE_BASES]:
            assert want[0][0] == "raised", case
    assert not found, "\n".join(found)


# The cold calls the stack test makes compiled, in a thread whose stack is reserved at each
# of these sizes in KiB, and then on the main thread.  1 MiB is the size asserted; the
# others bracket what the calls need, and the test reports the smallest that ran.
STACK_KIB = (256, 384, 512, 768, 1024, 1536, 2048)

# How long the stack test waits for each child, in seconds: one runs in about a second, a
# few under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300

# The cold calls the stack test makes, each on a point of its own, in the last month: the
# net cash flow, and the count's residual and the surrenders, the deepest heads
# (sample_sec.py), each of whose chains opens the account value's under the count's first
# month on the books.
STACK_HEADS = ("net_cf", "check_pols_roll_fwd_resid", "pols_lapse")


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the anchor at issue age 40, issued now and 120 months on, whose cover runs 972
    months (:func:`_longest_cover`), each on a point of its own, a cold ``net_cf``, a cold
    ``check_pols_roll_fwd_resid`` and a cold ``pols_lapse`` in the last month each run the
    count's, the account value's and the floor's chains from the end of the frame back to
    ``t_entry``, 971 months and the cells above and below them deep in modelx on a model
    just read (:func:`test_the_deepest_cold_call_runs_one_cell_a_month`), and compiled
    they run on the C stack, which the interpreter's recursion limit does not count.
    1 MiB is the stack MSVC gives an executable's main thread unless the executable asks
    for more: a host that embeds Python, where python.exe itself asks for 2,000,000
    bytes.  A thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12 elsewhere.
    A stack too small kills the child, and the test fails naming the stack.  The thread's
    stack is read back too, from Windows or from glibc, and must be at most 1 MiB and a
    page: a stand-in larger than asked for would stand for nothing.  And the calls run
    again on the child's main thread, which is what ``run_sec.py --cython`` runs on.

    No run has measured what the calls need with MSVC.  So they run first at each size of
    :data:`STACK_KIB`, before anything is asserted, and every size's outcome goes into a
    warning, which the job's summary shows, and into the failure, if there is one: the
    smallest size that ran bounds the stack the chain needs on the compiler at hand.  A
    size below the need kills its child on a stack overflow, by design.  Each bracketing
    child is waited for :data:`BRACKET_TIMEOUT` seconds and the two asserted runs
    :data:`ASSERTED_TIMEOUT`, so that an overflow that hangs, rather than ends its child,
    costs minutes, not the job's hour, and a bracketing size that timed out is recorded as
    such.
    """
    build = sec_build(SEC)
    table, scenarios = _longest_cover(_committed())
    rows = pd.concat([table] * len(STACK_HEADS))
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    folder = compiled_case(build, tmp_path / "longest", model_points=rows,
                           edits={COMPANION: lambda _: scenarios})
    calls, want = {}, {}
    for key in range(len(rows)):
        head = STACK_HEADS[key // len(table)]
        model = _read(folder, "longest")
        try:
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert last - proj.t_entry() == 971, key
            calls[key] = [(head, (last,))]
            want[key] = [proj.cells[head](last)]
        finally:
            model.close()
    job = {"refs": {}, "calls": calls}

    def child(timeout, **where):
        try:
            return run_compiled(tmp_path / "longest", build.package.name, job,
                                timeout=timeout, **where)
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
        for key, values in want.items():
            for (status, have), value in zip(got["values"][key], values):
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
    S's anchor in force at ``idx`` 0, made before, and the anchor issued now, at ``idx``
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
    modelx's: the default point, S's anchor in force, the anchor restated after its
    account value ran out, and the anchor issued 15 months on, each with where it came
    from, where it stands, its anniversaries and its cash flows; and the block's lines for
    each point, its first twelve rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in ((), ("14",), ("18",), ("--block",)):
        expected = committed_runs(*args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "8", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
