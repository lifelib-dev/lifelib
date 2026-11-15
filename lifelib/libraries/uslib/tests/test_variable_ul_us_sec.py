"""In-force tests for VUL_US_SEC: the splice, future business, counts, regeneration.

``VUL_US_SEC`` is ``VUL_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M4).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t``.  A model point may be a
policy already in force at the valuation date, in any month of its policy year, one issued
at it, or one to be issued after it, as in ``basiclife/BasicTerm_SE``.  A policy in force
opens with the state its past has left it, per policy: each subaccount's value, the fixed
option's and the debt, which are ``VUL_US_S``'s own columns, and two more, the loan
account's collateral and the face in force.

The worked example is not restated here.  ``VUL_US_S`` counts its months from the start of
its own projection, and opens its points 1 and 2, in force 24 months, and 4, in force 120,
at its own ``t = 0``, so the twins of those three points open at offset 0 and are splice
cases (T2): each is S's point in every cell of S's, at no tolerance beyond the relative
1e-9, which carries every golden of ``test_variable_ul_us.py`` on them over, the worked
example's month, asserted at ``t = 0`` on point 1, among them.  S's point 3 is new
business, issued at the valuation date, where the two clocks coincide, and
``test_model_conventions.py`` asserts the model is S there cell by cell (T1).  The
conventions also hold the SEC family's other rules: every frame opens at ``t = 0``,
``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the month's new
business, new business enters once, and nothing happens before issue.  This module holds
the rest of the plan's tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's, the
  four reports among them, its subaccounts, fixed option, loan account, debt and face
  at every timing, and the pricing path behind the funding ratio, at S's own policy
  months.  The months straddle the product's events: the first anniversaries, the loan's
  preferred tier, the lapse table's last year, the surrender charge's cliff and its
  one-month lapse spike, the month a shortfall begins, the attained age at which the
  splice's charges cease, the corridor's first binding month and the last covered month.
  Nine variants of S's points, in a copy of S's table and each with input rows of its own,
  add withdrawals on either death benefit option, a single premium with no surrender
  charge, an Option B point funded past its face, a point on a second surrender-charge
  schedule with a loan, an issue age below the tables' first age, each first-month pin
  alone, the COI pin above the guaranteed rate that bounds it, and a withdrawal that cuts
  the face past 0, and between them every sex and every class.  Each row reads the return
  scenario re-based to its own month.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate, table or return read
  there.
* D11's R1, R1a and R2, and D3 and D5's chains: on the splice's grid no cell is called at a
  negative month, none evaluated on the books reads a month before them, none reads
  beyond ``t + 1``, and the pricing path, keyed by the policy month from issue, reads
  nothing on the valuation clock; on the committed points no recursion runs backward over
  the frame, the policy clock is a closed form and no label accessor is read; and every
  chain of the model runs one cell a month from a cold start, as far as the contract's
  longest cover.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, and a count 2.5 times the
  table's, with every assumption that ships at zero switched on, scales every counted cell
  and moves no per-policy value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, by one rule; each assumption table is refused, naming its file and the column,
  if a key is blank, text or fractional, with the lines it is on, or if the keys repeat or
  leave a gap, with each key that repeats, its lines, and each that is missing; so is one
  whose rates, class factors, surrender charges, fund expenses or returns hold a value
  that is blank, text or infinite, a lapse or mortality rate outside 0 to 1, a class
  factor, a COI rate, a fund expense, a premium persistency factor or a surrender charge
  below 0, and a run-off that is not a whole number of years, 1 or more, while the bounds
  of each range are read; a text value no decode knows raises ``VUL_US_S``'s message; the
  future horizon is a Reference that bounds future business, and at 0 refuses it; a point
  at or past the end of the projection is refused by ``proj_len()``; the edges of the
  interface are accepted, the tables' keys written as floats among them, each rule over a
  window of policy months refused just inside each end and read just outside; and every
  state ``VUL_US_S`` reaches, restated in force under each set of References on which
  those states differ, is accepted, but an account below 0, refused by name.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``VUL_US_S`` and its table as they stand, and each of its derived and future rows
  projects its S point's numbers from its month on.
* Then the two clocks on the shipped points, S's in-force points as their twins, the
  values outside cover, the survivors the end of the projection carries, the face, the
  collateral and each subaccount opening from their own columns, the return scenario,
  expense inflation and the declared rate on the valuation clock and the pricing path
  off it, the COI rate's bound by the guaranteed rate and the declared rate's floor where
  they bind, a check whose residual is not a number, a lapse rate past 1, which makes
  every check raise, each check deciding as S's where its sides are small, the margin
  identity once a loan exceeds the cash value, acquisition on new business, the
  mortality cap and a NaN that reaches it or a bound on the COI rate, the docstrings, the
  shared input tables, what the default grid reaches, the block, an in-force extract and
  the runner.
* Stage EC, held in modelx: the split totals, ``claims(t)`` and ``me_charge_pp(t)``, are
  S's bit for bit, the sign of a zero included; the padding of every array is NaN and no
  reader reads it, the extract labelled otherwise than by position naming each point it
  refuses, and the scenarios are numbered by their ids whatever the file's order; a
  scenario month far past every frame adds nothing to ``Data``'s return array; what
  ``Data`` cannot number or join, and a value no decode or join knows, its case or its
  spaces changed, is refused by name; a point the contract does not issue is refused by
  ``proj_len()``; the runner refuses to build from a copy without the repository, and
  sums the block as ``groupby`` does; and the sample's recursion limit and the spec's
  sizes are what their comments derive.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).
* The compiled model (Phase 2), in the ``cython`` job: it computes what modelx computes on
  the splice grid, at the contract's extremes and on a lineup of nine, where the cap on
  mortality binds and a NaN meets a bound, on labels that are not text and on keys
  written as floats; it refuses what modelx refuses, and what only its caches bound; its
  deepest call runs on a 1 MiB stack and on the main thread; past a lapse rate of 1 its
  checks fail rather than raise; it clears no cache when a Reference is set; and the
  runner prints it as it prints modelx.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 0 for
the twins of S's points, in force or not, ``-k`` for one issued ``k`` months on.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  A VUL projection runs up to
1,344 months on the grid, and T2 and T3 over every case, 48 restated rows, six in-force
twins and 9 future points, would take this module far past three minutes in every run.
By default they run a core of 17 and 5 cases, chosen so that between them they reach
every branch, every opening-state column, every kind of valuation month and every premium
pattern the full grid reaches, which ``test_the_core_grid_reaches_every_branch`` asserts.
VUL premiums are annual amounts paid monthly, the one mode the product models, so there is
no mode to reach.  The other cases, the rules test's scan of their rows and the depth
test's run with the behaviour module on at the longest cover carry the ``sec_full``
marker and are skipped, with the reason shown, unless ``USLIB_SEC_FULL=1`` is set.  They
are never dropped: one leg of the CI matrix sets it, so every CI run runs the full grid,
and ``USLIB_SEC_FULL=1 python -m pytest -m sec_full tests/test_variable_ul_us_sec.py``
runs them alone.  Memory is the other cost: a projected point holds tens of megabytes of
cached values and their dependency graph, so a row read once, a splice case's or a point
of a temporary copy, is released as soon as it has been read (``_release``), and the
splice's rows are held one at a time, however large the grid.  And the splice's two models
are fixtures of the class that holds every test reading them, so they are closed before
the committed model and S are first read, and the module never holds both.

Every test keeps five rules.  Each model is read under a name of its own and closed:
``test_variable_ul_us.py`` reads S under its default name, and reading a model under a
name in use renames the open one.  Every Reference a test sets, ``Data``'s included, is
set on a model just read, before anything is computed: a compiled model never clears a
cache.  No test writes inside the library tree: every changed input goes through
``sec_support.temp_inputs`` into a temporary directory, because a CSV added beside the
models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  The one exception is a table ``Data`` refuses, which has
no keys to give: it is read through the base ``Projection``'s default point.  And a timing
or a kind is passed through ``_code``, which gives the model's Reference of that name
where the model defines one and the string otherwise, a subaccount through ``_sa`` and the
lineup through ``_subaccounts``, and every cell-by-cell comparison goes through ``_twin``:
Phase 2 changes the call syntax only (C1), each in one place.  At stage ``"EC"``, where the
model now stands, the codes are the model's int References (USLIB-SEC-PLAN.md R9),
``Projection`` is keyed by position, a subaccount is its position in the lineup, and
``_twin`` maps S's ``claims(t, None)`` and ``me_charge_pp(t, None)`` onto the totals
``claims(t)`` and ``me_charge_pp(t)``, and S's subaccount ids onto positions.
"""
import ast
import dataclasses
import gc
import itertools
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys
import warnings

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, _VUL_LINEUP, _vul_c4_also,
    build_sec_table, check_generated, codes, compiled_case, compiled_mismatches,
    exact_here, fingerprint_mismatches, frame_mismatches, run_compiled, shift_months,
    sweep, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "VUL_US_SEC", "VUL_US_S", "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's four points, all the anchor cell, M45 StdNT, $500,000 of face, LEVEL at $6,000 a year
# on the VUL14 schedule, withdrawing nothing: 1, the worked example's policy, in force 24
# months on Option A on the WE scenario with its first-month pins; 2, the same without the
# pins; 3, new business on Option B on LEVEL6, the one point S issues at its t = 0; and 4,
# in force 120 months on Option A with a fixed option and a loan.  S opens 1, 2 and 4 at
# its own t = 0, so their twins open at offset 0.
NEW_BUSINESS = (3,)
IN_FORCE = (1, 2, 4)

# Six more S points, in the splice's copy of S's table and never in the committed one.  Each
# changes S's columns, never a formula, to reach what S's four cannot, and carries one of
# the sexes and classes they lack:
#
# 5, withdrawals of $100 a month on Option B, F PNT: the face never moves, and its
#   withdrawals outrun its unloaned accounts once its shortfall has begun, where the
#   withdrawal is shared by the premium allocation;
# 6, the same withdrawals on Option A, M PPlusNT: each cuts the face in proportion to the
#   account value, so the face in force is far below the face at issue a year on;
# 7, a single premium of $100,000 on Option A with no surrender charge, M StdPlusNT, whose
#   lapse spike has no cliff to fall at;
# 8, LEVEL at $60,000 a year on Option B, M PTob: the account value outgrows the face, and
#   the corridor binds on Option B;
# 9, S's in-force point 4 in force at 60 months, M StdTob, on VUL10, a second schedule of
#   $12.00 per $1,000 run off over 10 years: its loan steps to the preferred rate at S
#   month 48, policy year 10, and its lapse spike falls at S month 60, policy month 120;
#   S opens it at its own t = 0, so its twin is a splice case too;
# 10, issue age 10, below the mortality and corridor tables' first age, 18, which both
#   models read at 18: its own COI rows, the longest cover the grid runs, 1,344 months,
#   and a guaranteed COI scale steep enough to reach the cap of $83.34 before charges
#   cease, so that the cap moves the current rate and the charge;
# 11, S's point 2 with a COI pin alone, $0.50, above its guaranteed rate in policy year 3,
#   $0.259467, which bounds it: the pin applied at t = 0 without the corridor's, and the
#   bound on it binding; S opens it at its own t = 0, so its twin is a splice case;
# 12, S's point 2 with a corridor pin alone, the worked example's 2.15: the corridor's pin
#   without the COI rate's, so that neither pin's flag stands in for the other's;
# 13, S's point 3 on Option A, paying $1,200 a year and withdrawing $100 a month: in its
#   issue month the withdrawal is more than the 96.00 of account value its first net
#   premium buys, so the proportionate cut is 500,000 x 100 / 96, more than the face, and
#   the face is floored at 0.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.
VARIANTS = {
    5: (3, {"policy_id": "VUL-900005", "wd_pp": 100.0, "sex": "F", "rate_class": "PNT"}),
    6: (3, {"policy_id": "VUL-900006", "db_option": "A", "wd_pp": 100.0,
            "rate_class": "PPlusNT"}),
    7: (3, {"policy_id": "VUL-900007", "db_option": "A", "premium_type": "SINGLE",
            "premium_pp_ann": 100000.0, "has_surr_charge": False,
            "rate_class": "StdPlusNT"}),
    8: (3, {"policy_id": "VUL-900008", "premium_pp_ann": 60000.0, "rate_class": "PTob"}),
    9: (4, {"policy_id": "VUL-900009", "duration_mth": 60, "rate_class": "StdTob",
            "surr_charge_id": "VUL10"}),
    10: (3, {"policy_id": "VUL-900010", "age_at_entry": 10, "db_option": "A"}),
    11: (2, {"policy_id": "VUL-900011", "coi_rate_override_m1": 0.5}),
    12: (2, {"policy_id": "VUL-900012", "corridor_override_m1": 2.15}),
    13: (3, {"policy_id": "VUL-900013", "db_option": "A", "premium_pp_ann": 1200.0,
             "wd_pp": 100.0}),
}

# The variants' own input rows, in the copies only.  The shipped COI table covers the anchor
# cell, M StdNT 45, alone, so each new key gets the anchor's rows at a scale of its own, and
# a COI read under the wrong key reads a different number.  Issue age 10 gets rows
# geometric in the policy year, never flat, for every policy year its cover reaches, so that
# a scale read at the wrong year changes a number too, and steep enough to pass the cap of
# $83.34 at policy year 79, attained age 88, inside the splice's charging ages.  Variant 7's
# scale stops at policy year 50, short of its cover's 77, as a scale may, so that both
# models read its later years at year 50's rate (COI_LAST_YEAR).  VUL10 is the second
# schedule.
COI_KEYS = ["sex", "rate_class", "age_at_entry", "policy_year"]
COI_SCALES = {("F", "PNT", 45): 0.70, ("M", "PPlusNT", 45): 0.55,
              ("M", "StdPlusNT", 45): 0.85, ("M", "PTob", 45): 0.95,
              ("M", "StdTob", 45): 0.90}
COI_LAST_YEAR = {("M", "StdPlusNT", 45): 50}
SECOND_AGE = 10


def _coi_rates_with_variants(rates):
    """S's COI table with rows for every key the variants use, sorted.

    Sorted by its four keys, as ``Data.coi_rates()`` indexes it, so that pandas can slice
    a cell's scale without a warning about the index's sort order.
    """
    anchor = rates[(rates["sex"] == "M") & (rates["rate_class"] == "StdNT")
                   & (rates["age_at_entry"] == 45)]
    blocks = [rates]
    for (sex, rate_class, age), scale in COI_SCALES.items():
        last = COI_LAST_YEAR.get((sex, rate_class, age), anchor["policy_year"].max())
        blocks.append(anchor[anchor["policy_year"] <= last].assign(
            sex=sex, rate_class=rate_class, age_at_entry=age,
            coi_rate_guar=(anchor["coi_rate_guar"] * scale).round(6),
            provenance="test copy"))
    years = list(range(1, 113))
    blocks.append(pd.DataFrame({
        "sex": "M", "rate_class": "StdNT", "age_at_entry": SECOND_AGE, "policy_year": years,
        "coi_rate_guar": [round(0.05 * 1.10 ** (y - 1), 6) for y in years],
        "provenance": "test copy"}))
    return pd.concat(blocks, ignore_index=True).sort_values(COI_KEYS, ignore_index=True)


def _surr_charges_with_vul10(table):
    """S's surrender charge schedules with VUL10: $12.00 per $1,000 over 10 years."""
    vul10 = pd.DataFrame([{"surr_charge_id": "VUL10", "sc_per_1000_init": 12.0,
                           "runoff_years": 10, "provenance": "test copy"}])
    return pd.concat([table, vul10], ignore_index=True)


def _stepped_scenarios(_):
    """S's two return scenarios replaced by paths that move every month, months 0 to 240.

    ``VUL_US_S``'s ``WE`` is level after its first month and ``LEVEL6`` is flat, so a
    return read in another month than its own would change no number.  Here each scenario
    and subaccount has a path of its own that differs from one month to the next, around a
    base of 0.35% a month on ``WE`` and 0.50% on ``LEVEL6``, swinging by 1.2% on the equity
    subaccount and 0.4% on the bond one, and its last month repeats past month 240.
    """
    rows = []
    for scenario, base in (("WE", 0.0035), ("LEVEL6", 0.0050)):
        for i, amp in ((1, 0.012), (2, 0.004)):
            for t in range(241):
                r = base + amp * (((7 * t + 3 * i) % 13) - 6) / 6
                rows.append((scenario, i, t, round(r, 10), "stepped for a test"))
    return pd.DataFrame(rows, columns=["scenario_id", "subaccount_id", "t",
                                       "gross_return_mth", "provenance"])


# The input files the splice's copies change, S's and SEC's alike.  SEC's scenario file is
# then replaced by its re-based copies (_rebase).
SPLICED_EDITS = {"coi_rates.csv": _coi_rates_with_variants,
                 "surr_charge_table.csv": _surr_charges_with_vul10,
                 "scenario_table.csv": _stepped_scenarios}

# T2's months (USLIB-SEC-PLAN.md §7.6), by event rather than month by month, so that the
# grid is sized for what T2 and Phase 2's C4 both need.  All are S's months, under the
# splice's References and scenarios.  On S's point 3, new business on Option B: 1, the
# first month after issue; 11, the month before the first anniversary, which falls at
# t = 1; 12, the anniversary; 13; 23 and 25, either side of the second anniversary; 37, 96
# and 200, §7.6's re-opening months; 108, the anniversary that opens policy year 10, where
# the loan rate would step; 119 and 121, either side of the anniversary that opens policy
# year 11, the lapse table's last; 167 and 168, either side of the lapse spike at policy
# month 168, where VUL14's surrender charge reaches 0; and 570, the month its shortfall
# begins on the stepped scenario.  On S's point 1, in force at 24 on Option A on the WE
# scenario: 1; 12, its anniversary; 143 and 144, either side of its spike; 635, the last
# month before charges cease at attained age 100; 899, its last covered month, a frame of
# one row whose t = 1 is the month carried into.  On S's point 2: 12, and 47, the month
# before its sixth anniversary.  On S's point 4, in force at 120 with the fixed option and
# a loan: 1, the first month its collateral and its loan have parted, which S opens equal;
# 6, the committed row's month; 47, the month before its spike; 300, the anniversary that
# opens its policy year 36; 446 and 447, either side of the corridor's first binding month
# on Option A; 539, before charges cease; 803, its last covered month.  On the variants:
#   5, withdrawals on B: 12; 18, mid-year after six withdrawals; 590, its shortfall's start;
#   6, withdrawals on A: 13, the face already cut, and cut again at t = 0; 18; 25, mid-year
#     in a later year; 186, the month before its corridor binds;
#   7, the single premium: 12, and 485, its corridor's first month;
#   8, over-funded on B: 283 and 284, either side of its corridor binding; 515, the last
#     month of its second run;
#   9, VUL10 with a loan: 1, its collateral and loan parted; 47, where the loan's tier
#     steps at t = 1 and the spike falls at t = 13; 59, the month before its spike;
#   10, issue age 10: 12, and its last covered month, 1343.
# Variants 11 and 12 are their twins alone: restated later, a row's pins are blank, and the
# row is S's point 2's.  Variant 13 has none, since its face is 0 from its issue month, and
# a point in force holds a face.
# T3's: S's point 3 issued one month on, which puts the policy anniversaries a month off
# the valuation years, twelve, which puts them back on, and thirteen; and each
# new-business variant issued thirteen months on, more than a year, so that its months
# before issue read policy years -1 and 0, where a cell read without its guard would show:
# issued within a year, a point reads policy year 0 alone before issue (USLIB-SEC-PLAN.md
# D4).  Variants 9, 11 and 12 are in force in S and cannot be issued later.
PT_MTHS = {3: (1, 11, 12, 13, 23, 25, 37, 96, 108, 119, 121, 167, 168, 200, 570),
           1: (1, 12, 143, 144, 635, 899), 2: (12, 47),
           4: (1, 6, 47, 300, 446, 447, 539, 803)}
VARIANT_MTHS = {5: (12, 18, 590), 6: (13, 18, 25, 186), 7: (12, 485), 8: (283, 284, 515),
                9: (1, 47, 59), 10: (12, 1343)}
SPLICES = tuple(("derived", p, d)
                for p, mths in (*PT_MTHS.items(), *VARIANT_MTHS.items()) for d in mths)
IN_FORCE_TWINS = (("twin", 1, 0), ("twin", 2, 0), ("twin", 4, 0), ("twin", 9, 0),
                  ("twin", 11, 0), ("twin", 12, 0))
FUTURES = ((3, 1), (3, 12), (3, 13), (5, 13), (6, 13), (7, 13), (8, 13), (10, 13),
           (13, 13))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES, IN_FORCE_TWINS and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("twin", 1, 0): "S's in-force point 1 at offset 0: the worked example's month and its "
                    "pins at t = 0",
    ("twin", 4, 0): "S's in-force point 4: the fixed option and the loan, the corridor on "
                    "Option A",
    ("derived", 1, 899): "the last covered month: t = 1 is the month carried into",
    ("derived", 3, 12): "new business on its first anniversary; the block test's row",
    ("derived", 3, 167): "the month before the spike, which falls at t = 1",
    ("derived", 3, 168): "on the spike: the lapse spike in the valuation month, t = 0",
    ("derived", 3, 570): "Option B where its shortfall begins: the funding ratio below 0, "
                         "the dynamic bounds, the deduction's fallback share",
    ("derived", 4, 6): "in force six months on: the collateral and the loan parted",
    ("derived", 5, 12): "withdrawals on Option B, F PNT: the face never moves",
    ("derived", 5, 590): "withdrawals in shortfall: the withdrawal's fallback share",
    ("derived", 6, 13): "withdrawals on Option A: the face already cut, and cut at t = 0",
    ("derived", 7, 12): "a single premium with no surrender charge, Option A",
    ("derived", 8, 283): "over-funded on Option B: the corridor binds from t = 1",
    ("derived", 9, 47): "StdTob on VUL10: the loan's tier steps at t = 1, the spike at "
                        "t = 13",
    ("derived", 10, 12): "issue age 10: the tables read at 18, the COI cap with an effect",
    ("twin", 11, 0): "a COI pin alone, above the guaranteed rate, which bounds it",
    ("twin", 12, 0): "a corridor pin alone",
}
CORE_FUTURES = {
    (3, 1): "issued a month off the valuation anniversaries",
    (3, 12): "issued on them, a year on; the block test's row",
    (6, 13): "withdrawals on Option A, more than a year on: policy year -1 before issue",
    (7, 13): "the single premium in its issue month, with no surrender charge",
    (13, 13): "a withdrawal that cuts more than the face, floored at 0, in the issue month",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Each switches on what the shipped values leave unreached:
#   dyn_behavior_on, which ships off and with it the pricing path, the funding ratio, the
#     premium persistency scale and both dynamic multipliers, none of which a shipped run
#     reads;
#   lapse_shock_mult at 3, where the shipped 1 makes the spike at the surrender charge's
#     cliff change nothing; VUL's lapse rate has no cap, so no cap needs a shock to meet it;
#   expense_acq at $250, which ships at 0, so that acquisition on future business shows;
#   mort_ae_factor at 0.56, which leaves lives at the end of every frame, so that the
#     survivors carried into t = proj_len(), which S's roll-forwards read there, are
#     compared on every row, and which keeps every class's annual rate below 1, StdTob's
#     oldest at 1.75 x 0.56 = 0.98: at an A/E of 1 its product passes 1 at attained age
#     113, where both models cap it (the mortality cap test);
#   charges_cease_age at 100, inside every frame, where the shipped 121 is the frame's last
#     age: premiums, withdrawals and monthly deductions cease in cover;
#   crediting_rate_curr at 2.5%, the declared fixed rate set apart from the guaranteed 1%,
#     equal as shipped, so that a max that read the wrong one would show, and from the
#     loan account's 1%.
# Expense inflation ships at 0, and stays there: it runs on the two clocks by design, and
# the inflation test sets it on its own.  rider_charge_pp is S's placeholder and reads no
# input.  The identity does not depend on the values, only on both models having the same.
SPLICED_REFS = {"dyn_behavior_on": True, "lapse_shock_mult": 3.0, "expense_acq": 250.0,
                "mort_ae_factor": 0.56, "charges_cease_age": 100,
                "crediting_rate_curr": 0.025}

# The cells T2 and T3 skip beyond T1's, which already drops result_pols as a whole (the
# spec's exempt).  The twins of S's in-force points take no more: S opens them at its own
# t = 0, from the columns their twins carry, so S's opening accessors are theirs, and S's
# frame is theirs.  On a restated row, S's own accessors of the point it opens differ by
# design: proj_len counts from the valuation date on SEC and from S's own start on S, so it
# differs by d, or by -k, and frame_mismatches asserts what it must get right, that both
# frames end at the same instant; duration_mth_init is d, or -k, on SEC and S's own on S;
# and sa_pp_init, fa_pp_init, loan_bal_init and av_pp_init hold S's month-0 values on S
# and month d's on SEC.  Every cell that reads them is compared.  scenario_id names a
# restated row's own re-based copy of its S scenario (_rebase); every cell the scenario
# drives is compared.  And first_default_month and first_shortfall_month are months on
# each model's own clock, the first of which S finds may fall before d, outside SEC's
# frame: each is asserted against the first month S's own is_default and is_shortfall
# hold at or after d, less d (_first_month), and the two flags are compared month by month.
TWIN_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt
FIRST_MONTHS = {"first_default_month": "is_default",
                "first_shortfall_month": "is_shortfall"}
SPLICE_EXEMPT = (TWIN_EXEMPT
                 | {"proj_len", "duration_mth_init", "sa_pp_init", "fa_pp_init",
                    "loan_bal_init", "av_pp_init", "scenario_id", *FIRST_MONTHS})
FUTURE_EXEMPT = TWIN_EXEMPT | {"proj_len", "duration_mth_init", "scenario_id",
                               *FIRST_MONTHS}


def _issued_later(name, args):
    """The ``arg_map`` of a point issued at or after the valuation date, compared with S.

    S's keys as they are, but ``pols_if_at(0, "BEF_NB")``, S's issue month, which it
    leaves out (``None``): there S's cell counts the issued policies, as it does under
    every timing, and this model counts them as the month's new business, not yet in.
    """
    return None if name == "pols_if_at" and args == (0, "BEF_NB") else args


# The decrement rates keyed by month, none of which may be evaluated before issue (R1,
# D4); the readers keyed by a policy year, by an attained age reached in cover, and by an
# attained age from issue on, which the pricing path reads too; and the pricing path, keyed
# by the policy month from issue.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "lapse_rate_base", "lapse_rate",
                   "lapse_rate_mth")
KEYED_BY_YEAR = ("coi_rate_guar_at", "coi_rate_at", "lapse_rate_base_py",
                 "prem_persistency_py")
KEYED_BY_AGE = ("mort_rate_base_at",)
KEYED_FROM_ISSUE = ("corridor_factor_at",)
PRICING = ("prem_pricing_pp", "sa_pricing_pp_at", "sa_pricing_pp", "fa_pricing_pp_at",
           "fa_pricing_pp", "av_pricing_pp_at", "av_pricing_pp", "naar_pricing_pp",
           "mth_deduction_pricing_pp", "db_pricing_pp", "age_pricing",
           "policy_year_pricing")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a
# rate, a clock or a flag, and must not move when the count does.  The three residuals are
# relative, so a scaled count moves them in the last digits.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz", "pols_death",
    "pols_lapse", "pols_maturity", "premiums", "prem_to_av", "premium_loads", "coi",
    "maint_fee", "mth_deduction", "inv_income", "me_charge", "loan_spread", "av_at",
    "av_change", "surr_charge", "claims_from_av", "claims_over_av", "claims", "claims_net",
    "claims_death", "claims_lapse", "withdrawals", "wd_fees", "sa_transfer", "expenses",
    "premium_taxes", "margin_expense", "margin_mortality", "net_cf", "net_cf_ga"})
RELATIVE = ("check_av_roll_fwd_resid", "check_margin_resid", "check_net_view_resid")

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths and lapses in processing order, the maturities, always zero, then S's two monthly
# decrement rates, which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_maturity",
               "mort_rate_mth", "lapse_rate_mth"]
OUTFLOWS = RESULT_POLS[2:5]
RATES = RESULT_POLS[5:]
REPORTS = ("result_cf", "result_pols", "result_av", "result_net")

# The timings and kinds the model knows: the count's three, which S's stub names and
# answers with pols_if for each; the five intra-month points of the accounts, and av_at's
# EOM; and the claim kinds, with claim_pp's WITHDRAWAL and claims_from_av's MATURITY,
# always zero.  At stage EC each is the model's int Reference of its name, through _code,
# and S's claims(t, kind=None) is two cells, claims_death and claims_lapse, and their
# total, claims(t), and S's me_charge_pp(t, i=None) a cell of a subaccount,
# me_charge_sa_pp(t, i), and their total, me_charge_pp(t), which this module calls by name
# (USLIB-SEC-PLAN.md D11, R12).
TIMINGS = ("BEF_MAT", "BEF_NB", "BEF_DECR")
AV_TIMINGS = ("BEF_PREM", "BEF_WD", "BEF_FEE", "BEF_INV", "BEF_ME")
KINDS = ("DEATH", "LAPSE")
CLAIM_KINDS = ("DEATH", "LAPSE", "WITHDRAWAL")
AV_KINDS = ("DEATH", "LAPSE", "MATURITY")

# The opening state, in Data's order, as each column is read: (the column, the accessor and
# its arguments, a subaccount by its id, which _state_args passes through _sa).  And the
# two first-month pins.
STATE = {"sa_pp_init_1": ("sa_pp_init", (1,)), "sa_pp_init_2": ("sa_pp_init", (2,)),
         "fa_pp_init": ("fa_pp_init", ()), "la_pp_init": ("la_pp_init", ()),
         "loan_bal_init": ("loan_bal_init", ()),
         "sum_assured_init": ("sum_assured_init", ())}
PINS = ("corridor_override_m1", "coi_rate_override_m1")

# The cells running in force adds to VUL_US_S's or gives a new meaning, each of which the
# symbol map must name, and S's label accessors, which no projection cell may read.
NEW_CELLS = ("policy_count", "duration_mth_init", "t_entry", "omega_mth", "is_active",
             "pols_new_biz", "pols_if_at", "la_pp_init", "sum_assured_init", "wd_pp_mth",
             "is_db_option_a", "is_db_option_b", "is_gpt", "is_level_premium",
             "is_single_premium", "mort_rate_base_at", "lapse_rate_base_py",
             "prem_persistency_py", "coi_rate_last_year", "scenario_last_mth",
             "surr_charge_rate_max", "surr_charge_runoff_years",
             "pricing_fixed_return_mth", "corridor_override_m1",
             "has_corridor_override_m1", "coi_rate_override_m1",
             "has_coi_rate_override_m1", *RELATIVE, "result_pols", "point_id",
             "subaccount_count", "coi_schedule", "scenario_index", "claims_death",
             "claims_lapse", "me_charge_sa_pp")
LABELS = ("sex", "rate_class", "db_option", "qual_test", "premium_type", "surr_charge_id",
          "scenario_id")

INFLATION = 0.025       # set by the inflation, scaling and acquisition tests; VUL ships 0
COUNT_FACTOR = 2.5      # T4's factor, not a whole number (USLIB-SEC-PLAN.md §5.2)

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached, and the committed
# points' sweep runs under a limit of 17, where VUL_US_S's runs under 16, with the
# behaviour module off, as shipped.  A backward recursion over the frame, through t + 1,
# opens a chain as long as the frame, and the shortest committed frame is 36 months, so a
# limit of 40 lets every forward sweep through and stops every backward one.  With the
# module on, a point not yet in force at the valuation date sweeps under 21, and one in
# force at policy month d needs d + 14, 38 on S's point 1 and 134 on its point 4: its first
# month's funding ratio reads the pricing path cold, back to issue (the depth test).
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to
# the chain's base (D5): the cells above the chain and those below it, the first month's
# charges and Data's first reads of its tables.  A cold net_cf in the last month runs 21
# cells beyond one cell a month back to t_entry() at the shipped References, on the
# committed points and at the contract's longest cover, and with the behaviour module on,
# 16 beyond one cell a month back to issue on the committed points, through the pricing
# path, and 21 at the longest cover; the pricing path alone runs 8 beyond, and each chain
# called alone at most 10 (measured at M17, at stage EC, where a Data vector and its
# table's check stand below each reader: 20 or 21 at stage E).  25 leaves four levels.
# Any chain of two cells a month runs a frame's length beyond.
CHAIN_OVERHEAD = 25


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _code(proj, label):
    """The argument that selects timing or kind ``label`` on ``proj``, a Space.

    The model's int Reference of that name where it defines one, as Phase 2 does (R9:
    ``pols_if_at(t, BEF_DECR)`` with ``BEF_DECR = 1``), else the string itself, as at stage
    ``"E"``.  The conventions' ``_timing`` does the same, so every call in this module reads
    the same at both stages.
    """
    value = proj.refs.get(label)
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _subaccounts(proj):
    """The arguments that select each subaccount of ``proj``'s lineup, in lineup order.

    Its positions, ``range(subaccount_count())``, where the model names a subaccount by its
    position, as Phase 2 does (R9, R10), else its ids, ``subaccount_ids()``, as ``VUL_US_S``
    does and the model did at stage ``"E"``.
    """
    if "subaccount_count" in proj.cells:
        return range(proj.subaccount_count())
    return proj.subaccount_ids()


def _sa(proj, sa_id):
    """The argument that selects subaccount ``sa_id`` on ``proj``: its position in the
    lineup, ``Data.subaccounts()``, where the model names a subaccount by its position,
    else the id itself."""
    if "subaccount_count" in proj.cells:
        return list(proj.data.subaccounts()).index(sa_id)
    return sa_id


def _state_args(proj, name, args):
    """The arguments of :data:`STATE`'s accessor ``name`` on ``proj``: a subaccount's id
    through :func:`_sa`."""
    return tuple(_sa(proj, a) for a in args) if name == "sa_pp_init" else args


def _twin(s_proj, sec_proj, *, arg_map=None, **kwargs):
    """``sec_support.twin_mismatches``, which every comparison in this module calls here.

    It passes the SEC Space's ``sec_support.codes``, which map S's timing and kind strings
    to the int codes Phase 2 gives them, and the spec's ``twin_arg_map``, which maps S's
    ``claims(t, None)`` and ``me_charge_pp(t, None)``, the totals, onto Phase 2's
    ``claims(t)`` and ``me_charge_pp(t)``, skips S's ``claims(t, kind)`` and
    ``me_charge_pp(t, i)``, whose values are Phase 2's ``claims_death``, ``claims_lapse``
    and ``me_charge_sa_pp``, and maps S's subaccount ids onto Phase 2's positions (R9,
    R12).  The spec's map runs first, then the caller's ``arg_map``, on S's arguments.  It
    maps S's keys alone, so where ``s_proj`` is a projection of this model, as T4's scaled
    count compares one with another, it is not applied.  At stage ``"E"`` there were no
    codes; every comparison goes through here, so each took Phase 2's codes and splits
    when they came.
    """
    first = SPEC.twin_arg_map if "subaccount_ids" in s_proj.cells else None

    def both(name, args):
        if first is not None:
            args = first(name, args)
        if args is not None and arg_map is not None:
            args = arg_map(name, args)
        return args
    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), arg_map=both,
                           **kwargs)


def _key(model, point_id):
    """The registry's key for the row labelled ``point_id`` (``us_registry.point_keys``)."""
    return dict(zip(model.Data.model_point_table().index, point_keys(model)))[point_id]


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    return projection(model, _key(model, point_id))


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for a twin, S's in-force points included,
    which S opens at its own ``t = 0``; ``d`` for a derived row; ``-k`` for a future one.
    The twins keep S's ``point_id`` and ``policy_id``, so the S policy is the twin's.
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


def _release(model, key, collect=True):
    """Drop the ItemSpace at ``key``, the registry's key, and every value it has cached.

    A projected VUL point holds tens of megabytes of cached values and their dependency
    graph.  The splice's rows and the scaled and extract copies' points are each needed
    once, so each is released when read, as ``run_sec.py --block`` releases its points
    (USLIB-SEC-PLAN.md F5), and collected at once.  That costs little, because the swept
    models the module holds are frozen out of the collector (:func:`_freeze`), so the
    collection scans only what the row made.  Asked for again, the ItemSpace is made afresh
    and recomputes.  With ``collect`` false the collection is left to the caller, as the
    every-state test leaves it, whose thousands of rows each hold one value.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds.  The collection first means no garbage is frozen with
    them.  The splice's fixture undoes its freeze as it closes its models, and
    :func:`_collector` the rest as the module ends.
    """
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read(folder, tag, refs=None):
    """The model in ``folder``, read under a name of its own, with ``refs`` set first.

    ``refs`` are ``Projection`` References, set on the model just read, before anything is
    computed: a compiled model clears no cache.
    """
    model = mx.read_model(folder, name=_name(tag))
    for ref, value in (refs or {}).items():
        setattr(model.Projection, ref, value)
    return model


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


def _moved(point, month, **columns):
    """An edit that moves row ``point`` to policy month ``month`` and sets ``columns``."""
    def edit(table):
        table = _set("duration_mth", [point], month)(table)
        for column, value in columns.items():
            table = _set(column, [point], value)(table)
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


def _refused_exactly(call, message):
    """``call()`` raises ``ValueError`` with ``message`` as its whole message.

    :func:`_refused` finds the message in the error's text; this compares the line that
    names the error (:func:`_raised`), so that a point, a key or a line named wrongly, or
    one too many, fails.
    """
    with pytest.raises(Exception) as excinfo:
        call()
    assert _raised(excinfo.value) == f"ValueError: {message}"


# The S cells no report or check of VUL_US_S evaluates (USLIB-SEC-PLAN.md §7.6, C), which
# the comparisons compare only because _sweep_s evaluates them first: the guaranteed COI
# rate by month, the base premium persistency, the default and shortfall tests, and the
# funding ratio, which with the behaviour module on reads the pricing path.
NEVER_REACHED = ("coi_rate_guar", "prem_persistency_base", "is_default", "is_shortfall",
                 "funding_ratio")


def _sweep_s(proj):
    """Evaluate on an S point what the comparisons compare: the sweep, and more.

    :func:`sec_support.sweep` reaches none of :data:`NEVER_REACHED`, the net unit-value
    return or ``pols_if_at`` on ``VUL_US_S``, and the two searches for the first default
    and shortfall months, because no result column or check reads them, and a cell S
    never evaluates is compared nowhere.  So they are evaluated here, over the frame, the
    return at each subaccount and ``pols_if_at`` at each of its timings, then the two
    searches, so that the comparisons see them too.
    """
    sweep(proj)
    ids = _subaccounts(proj)
    for t in range(proj.proj_len()):
        for i in ids:
            proj.inv_return_mth(t, i)
        for timing in TIMINGS:
            proj.pols_if_at(t, _code(proj, timing))
        for name in NEVER_REACHED:
            proj.cells[name](t)
    proj.first_default_month()
    proj.first_shortfall_month()


def _first_month(s_proj, flag, month):
    """The first month of a row restated at S month ``month``, or issued later, that S's
    ``flag`` holds: the first S month at or after ``max(month, 0)`` where it holds, less
    ``month``, or -1 if none does.

    What ``first_default_month`` and ``first_shortfall_month`` must give on the row, on the
    valuation clock: on a row restated at ``d`` the month S finds may fall before ``d``,
    outside the row's frame, and on a row issued ``k`` months on every month before issue
    is clear, so S's month ``u`` is the row's ``u + k``.
    """
    for u in range(max(month, 0), s_proj.proj_len()):
        if s_proj.cells[flag](u):
            return u - month
    return -1


def _continues_s(s_proj, sec_proj, month, arg_map=None):
    """Where a twin departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison, on a model at S's own assumptions: frame by frame, the four
    reports, then cell by cell over every cell of S's but T1's exemptions, every one to
    1e-9 relative with no absolute floor, through ``arg_map`` where it is given
    (:func:`_issued_later`, for a point issued at the valuation date).  ``VUL_US_S`` ships
    no expense inflation and flat scenarios after the worked example's month, so on S's
    in-force points, which open at offset 0, nothing is left out.
    """
    found = []
    for report in REPORTS:
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month, atol=0.0)]
    return found + _twin(s_proj, sec_proj, t_offset=month, exempt=TWIN_EXEMPT,
                         arg_map=arg_map, atol=0.0)


def _case_id(kind, s_point, month):
    """A case's id: ``point3-d12``, ``point4-twin0``, or ``point3-k13`` if issued later."""
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


def _rebase(table, scenarios):
    """Give each derived and future row of ``table`` its own copy of its S scenario.

    The rows of the splice's table share S's two scenarios, and each reads its scenario at
    its own valuation month: a row whose SEC ``t = 0`` is S month ``s`` reads S's month
    ``t + s``.  So each gets a copy re-based to its month, each subaccount's path as a step
    function of its own (:func:`sec_support.shift_months`), under an id of its own, the S
    id with the month, ``WE_m12`` or ``LEVEL6_f13``: the month in force at S month ``s``
    becomes month 0, and for a future row, ``s = -k``, months ``0 .. k - 1`` hold no row, so
    that a read before issue fails loudly.  The twins keep S's scenarios.  Returns
    ``(table, scenarios)``.
    """
    copies, ids, made = [], [], set()
    for _, row in table.iterrows():
        month, scenario = int(row["source_mth"]), row["scenario_id"]
        if month == 0:
            ids.append(scenario)
            continue
        copy = f"{scenario}_{'m' if month > 0 else 'f'}{abs(month)}"
        if copy not in made:
            path = scenarios[scenarios["scenario_id"] == scenario]
            copies.append(shift_months(path, "t", month, by="subaccount_id")
                          .assign(scenario_id=copy))
            made.add(copy)
        ids.append(copy)
    return table.assign(scenario_id=ids), pd.concat([scenarios, *copies], ignore_index=True)


def _spliced_folders(root, s, derived, future, edits=SPLICED_EDITS):
    """The SEC folder for ``derived`` and ``future`` rows of ``s``, a model on S's copy.

    The generator builds the rows from the registered spec, out of ``s`` as it stands, so
    each opens with the state of the very run it is compared with; each restated or
    future row's scenario is then a copy re-based to its month (:func:`_rebase`), and the
    folder holds ``edits`` and the re-based scenario table.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(derived), future=tuple(future))
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    scenarios = pd.read_csv(s.Data.input_dir() / "scenario_table.csv")
    table, scenarios = _rebase(table, scenarios)
    return temp_inputs(root, model_path(SEC), model_points=table,
                       model_point_file=spec.model_point_file,
                       edits={**edits, "scenario_table.csv": scenarios})


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module", autouse=True)
def _collector():
    """Undo, as the module ends, the freezes its module fixtures made (:func:`_freeze`).

    Set up before every other fixture of the module, it is torn down after them all, once
    every model the module read is closed, and then returns what was frozen to the
    collector and collects it, so that nothing frozen here outlives the module.
    """
    yield
    gc.unfreeze()
    gc.collect()


@pytest.fixture(scope="module")
def sec_read():
    """VUL_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  Last, the keys ``VUL_US_S``'s label accessors hold on each point, which no
    projection cell may read, are counted.  So the record says what a cold model does,
    which the clock test asserts (D3, R2), and every test on the committed model reads a
    model already swept: the sweep is paid once, not once for each.  The swept model is
    then frozen out of the collector (:func:`_freeze`).  Returns ``(model, record)``.
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    first = _row(model, "twin", 1, 0)
    record = {"duration_mth(500)": first.duration_mth(500),
              "keys": list(first.cells["duration_mth"].keys()), "deep": [], "labels": {}}
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
        read = {name: len(p.cells[name].keys()) for name in LABELS}
        record["labels"][point_id] = {name: n for name, n in read.items() if n}
    _freeze()
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """VUL_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """VUL_US_S read in place, as committed, with every point swept (:func:`_sweep_s`).

    T6 regenerates the SEC table from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it, the cells its own sweep misses among them.  Frozen once swept (:func:`_freeze`).
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep_s(projection(model, key))
    _freeze()
    yield model
    model.close()


@pytest.fixture(scope="class")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`SPLICED_REFS` set in both.

    S is read from a copy of the product directory whose table has the variants appended
    and whose COI, surrender charge and scenario tables are the splice's
    (:data:`SPLICED_EDITS`).  SEC runs on the same tables, and on a model point table of
    its own, built by the generator from the registered spec with its rows replaced by the
    cases this run selects, the core or the full grid (:func:`_selected`), out of this S
    model, so each row opens with the state of the very run it is compared with; each row's
    scenario is a copy re-based to its own month (:func:`_spliced_folders`).  Every S point
    is then swept (:func:`_sweep_s`), and stays swept; each SEC row is projected by the case
    that compares it and released once compared (:func:`_settle`).

    Scoped to the class that holds every test of the splice, so that its two models are
    closed before the committed model and S are first read: the module never holds both,
    which keeps its peak at the larger of the two.  Once S is swept the heap is frozen, so
    that the collections the released rows trigger scan the rows alone; at teardown the
    models are closed, then the freeze is undone and the collector run.
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants(), edits=SPLICED_EDITS)
    s = _read(s_folder, "s_spliced", SPLICED_REFS)
    sec = None
    try:
        derived = [(p, d) for kind, p, d in _selected(SPLICES, CORE_SPLICES)]
        sec_folder = _spliced_folders(root / "sec", s, derived,
                                      _selected(FUTURES, CORE_FUTURES))
        sec = _read(sec_folder, "sec_spliced", SPLICED_REFS)
        for key in point_keys(s):
            _sweep_s(projection(s, key))
        gc.collect()
        gc.freeze()
        yield s, sec
    finally:
        if sec is not None:
            sec.close()
        s.close()
        gc.unfreeze()
        gc.collect()


@pytest.fixture(scope="class")
def splice_records():
    """What each splice row was found to do, by case (:func:`_scanned`, :func:`_settle`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case scans its row for the rules test before it compares the row with S
# (_scanned), because the comparison then evaluates SEC cells at S's cached keys; once
# compared, it records what the guard test, the end-of-projection test and the core grid's
# reach need of the row, and releases it (_settle).  So each of those tests reads the
# records, and computes any case no earlier test has recorded, which keeps it whole when
# run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


# The cells that loop over the frame by design: the reports, the checks and the two
# searches for a first month.  Every other cell without a t reads none keyed by t, which
# the rules test asserts, since it is what lets the scan judge a read through a cell keyed
# by a policy month, a policy year, an age or a subaccount by the month that asked.
LOOPS = frozenset({*REPORTS, "check_av_roll_fwd", "check_margin", "check_net_view",
                   *FIRST_MONTHS})


def _sweep_on_the_books(proj):
    """Evaluate every monthly cell of ``proj`` at every month on the books.

    Each cell whose first parameter is ``t``, at each month from ``t_entry()`` to
    ``proj_len() - 1``, at each subaccount and at each timing or kind the guard test's
    sets give it, as Phase 2's full sweep does; the months outside cover are the guard
    test's (:func:`_outside_cover_faults`).  The loops over the frame leave cells unread on
    the books, the guaranteed COI rate, the default and shortfall flags and the rates past
    the age at which charges cease among them, and a read no cell makes is a read the scan
    cannot judge: no loop reads the account value's opening balance at ``t_entry()`` on a
    point issued later.  A cell with a parameter the sets give no values raises.
    """
    ids = _subaccounts(proj)
    months = range(proj.t_entry(), proj.proj_len())
    for name in sorted(_monthly_cells(proj)):
        cells, rest = proj.cells[name], proj.cells[name].parameters[1:]
        kinds = AV_TIMINGS if name == "sa_pp_at" else (*BY_ARGUMENT.get(name, ()),
                                                       *OPENING.get(name, ()))
        values = [_code(proj, kind) for kind in kinds]
        if rest not in ((), ("i",)) and not values:
            raise ValueError(f"{name}{cells.parameters}: no timing or kind to sweep it at")
        for t in months:
            if not rest:
                cells(t)
            elif rest == ("i",):
                for i in ids:
                    cells(t, i)
            elif rest[0] == "i":
                for i in ids:
                    for value in values:
                        cells(t, i, value)
            else:
                for value in values:
                    cells(t, value)


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has run on the books.

    The row runs each loop over the frame, the four reports first (:data:`LOOPS`), and
    then every monthly cell at every month on the books (:func:`_sweep_on_the_books`):
    what the row computes of itself, at its own months, which is what Phase 2 sweeps, and
    not S's keys, at which the comparison then evaluates SEC's cells.  Returns
    ``{"negative": [...], "early": [...], "ahead": [...], "unjudged": [...], "edges": n}``:
    every cached call with a negative argument, a month, a policy month, a policy year or
    an age; every precedent keyed by a month before ``t_entry()`` of a call keyed by a month
    at or after it; every precedent keyed by a month beyond ``t + 1`` of a call keyed by
    ``t``, and every call of the pricing path that reads one keyed by a policy month beyond
    its own plus one; every call of a cell without a ``t``, the loops over the frame
    excepted (:data:`LOOPS`), that reads one keyed by ``t``; and how many precedents the
    scan read, which must not be 0, or the scans held of nothing.  A precedent is a call's
    as modelx's dependency graph records it.

    The pricing path is keyed by the policy month from issue, ``m = duration_mth(t)``, and
    a read of it from a call keyed by ``t`` is judged at ``m - duration_mth_init()``, the
    month on the valuation clock it stands for: no read beyond ``t + 1``.  The look-back
    does not apply to it: it is a projection made at issue, deterministic and reading no
    state, based at issue on purpose, so a point in force reads it from issue (R2, as
    precised for VUL).  It reads no cell keyed by ``t``, which ``unjudged`` asserts, so no
    read of the valuation clock hides behind it.  VUL reads nothing further ahead than
    ``t + 1`` anywhere: R2's one exception, a read at the anniversary that closes the
    policy year, has no use here.
    """
    for name in (*REPORTS, *sorted(LOOPS - set(REPORTS))):
        proj.cells[name]()
    _sweep_on_the_books(proj)
    entry, start = proj.t_entry(), proj.duration_mth_init()
    negative, early, ahead, unjudged, edges = [], [], [], [], 0
    for name, cells in proj.cells.items():
        params = cells.parameters
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if "t" in params:
                t = args[params.index("t")]
                for node in cells.preds(*args):
                    edges += 1
                    node_params = getattr(node.obj, "parameters", None) or ()
                    if "t" in node_params:
                        u = node.args[node_params.index("t")]
                        if _month(u) and u < entry <= t:
                            early.append(f"{name}{args} -> {node.obj.name}{node.args}")
                    elif "m" in node_params:
                        u = node.args[node_params.index("m")] - start
                    else:
                        continue
                    if _month(u) and u > t + 1:
                        ahead.append(f"{name}{args} -> {node.obj.name}{node.args}")
            elif name not in LOOPS:
                m = args[params.index("m")] if "m" in params else None
                for node in cells.preds(*args):
                    edges += 1
                    node_params = getattr(node.obj, "parameters", None) or ()
                    if "t" in node_params:
                        unjudged.append(f"{name}{args} -> {node.obj.name}{node.args}")
                    elif m is not None and "m" in node_params:
                        if node.args[node_params.index("m")] > m + 1:
                            ahead.append(f"{name}{args} -> {node.obj.name}{node.args}")
    return {"negative": negative, "early": early, "ahead": ahead, "unjudged": unjudged,
            "edges": edges}


# What each monthly cell holds outside cover, before issue and in the month after the
# frame, t = proj_len(), which the roll-forwards read, as its docstring says: no count
# carried, no value, premium, withdrawal, charge, rate, decrement, claim or flow, and no
# question about the contract answered yes.  The type is part of the value: an amount, a
# rate or a count is a float in every branch and a flag a bool, because Phase 2 types a
# cell by the values it returns (USLIB-SEC-PLAN.md F3).
OUTSIDE_COVER = {
    # flags
    "is_active": False, "is_default": False, "is_shortfall": False,
    # premiums and withdrawals
    "premium_pp": 0.0, "prem_to_av_pp": 0.0, "prem_persistency": 0.0,
    "prem_persistency_base": 0.0, "premium_loads": 0.0, "wd_pp": 0.0, "wd_fee_pp": 0.0,
    "wd_fa_pp": 0.0, "face_reduction_pp": 0.0,
    # the face, the death benefit and the cost of insurance
    "sum_assured_at": 0.0, "corridor_factor": 0.0, "db_corridor_pp": 0.0, "db_pp": 0.0,
    "db_pp_eom": 0.0, "net_amt_at_risk": 0.0, "net_amt_at_risk_eom": 0.0,
    "coi_rate_guar": 0.0, "coi_rate": 0.0, "coi_pp": 0.0, "rider_charge_pp": 0.0,
    # charges, values and the loan
    "maint_fee_pp": 0.0, "mth_deduction_pp": 0.0, "mth_deduction_fa_pp": 0.0,
    "inv_income_pp": 0.0, "av_pp": 0.0, "fa_pp": 0.0, "la_pp": 0.0, "loan_bal_pp": 0.0,
    "loan_rate_ann": 0.0, "loan_rate_mth": 0.0, "surr_charge_rate": 0.0,
    "surr_charge_pp": 0.0, "csv_pp": 0.0, "ncsv_pp": 0.0,
    # rates
    "mort_rate": 0.0, "mort_rate_mth": 0.0, "lapse_rate_base": 0.0, "lapse_rate": 0.0,
    "lapse_rate_mth": 0.0,
    # counts
    "pols_new_biz": 0.0, "pols_death": 0.0, "pols_lapse": 0.0, "pols_maturity": 0.0,
    # flows
    "premiums": 0.0, "prem_to_av": 0.0, "coi": 0.0, "maint_fee": 0.0,
    "mth_deduction": 0.0, "inv_income": 0.0, "withdrawals": 0.0, "wd_fees": 0.0,
    "surr_charge": 0.0, "expenses": 0.0, "premium_taxes": 0.0, "claims_over_av": 0.0,
    "claims_net": 0.0, "me_charge": 0.0, "loan_spread": 0.0, "sa_transfer": 0.0,
    "claims": 0.0, "claims_death": 0.0, "claims_lapse": 0.0, "me_charge_pp": 0.0,
    "margin_expense": 0.0, "margin_mortality": 0.0, "net_cf": 0.0, "net_cf_ga": 0.0,
    # the cells that read t + 1, which return their zero before they read it
    "av_change": 0.0, "check_av_roll_fwd_resid": 0.0, "check_margin_resid": 0.0,
    "check_net_view_resid": 0.0,
}
# 1.0, each multiplier's neutral value and the funding ratio's: no month outside cover is
# the surrender charge's cliff, which a run-off of n years puts at policy month 12 n, the
# month after the frame on some points, and the funding ratio is not asked of a pricing
# path that, before issue, would be asked for a negative policy month.
NEUTRAL = {"lapse_rate_sc_mult": 1.0, "lapse_rate_dyn_mult": 1.0, "funding_ratio": 1.0}
# The policy clock, a Python int at every month, outside cover too: before issue its
# values are negative, or 0, and a cell keyed by them must not read a table there.
CLOCK = ("duration_mth", "duration", "policy_year", "age")
# The economic inputs read on the valuation clock (D7), floats at every month, one
# function of t for every point; and the loan account's credited rate, a level contractual
# rate, the same float in every month.
VALUATION_CLOCK = ("crediting_rate_ann", "fixed_return_mth", "inflation_factor")
LEVEL = ("loan_cr_rate_ann", "loan_cr_rate_mth")
# The return scenario's readers, one function of t for every point, unguarded: no formula
# reads them outside cover, and a re-based copy of a future row holds no month before
# issue, so a read there raises.  At t = proj_len() they read the scenario's last month.
IN_COVER_ONLY = ("gross_return_mth", "inv_return_mth")
# Cells keyed by a subaccount as well, 0.0 at every subaccount of the lineup outside cover;
# and sa_pp_at at every subaccount and every one of its timings.
BY_SUBACCOUNT = ("sa_pp", "wd_sa_pp", "mth_deduction_sa_pp", "me_charge_sa_pp",
                 "sa_pp_at")
# Cells with a timing or a kind, 0.0 at every one of these outside cover.
BY_ARGUMENT = {"claim_pp": CLAIM_KINDS, "claims_from_av": AV_KINDS,
               "av_pp_at": AV_TIMINGS[1:], "av_at": (*AV_TIMINGS[1:], "EOM"),
               "unloaned_av_pp_at": AV_TIMINGS, "fa_pp_at": AV_TIMINGS,
               "la_pp_at": AV_TIMINGS, "loan_bal_pp_at": AV_TIMINGS}
# The opening timings, 0.0 before issue, and in the month after the frame what the
# survivors of its last month carry into it (CARRIED): the count, at every timing, and the
# account value per policy and in force.
OPENING = {"pols_if_at": TIMINGS, "av_pp_at": AV_TIMINGS[:1], "av_at": AV_TIMINGS[:1]}
CARRIED = ("pols_if",)
# The sets above, which together must hold every cell whose first parameter is t, once.
GUARD_SETS = {"OUTSIDE_COVER": set(OUTSIDE_COVER), "NEUTRAL": set(NEUTRAL),
              "CLOCK": set(CLOCK), "VALUATION_CLOCK": set(VALUATION_CLOCK),
              "LEVEL": set(LEVEL), "IN_COVER_ONLY": set(IN_COVER_ONLY),
              "BY_SUBACCOUNT": set(BY_SUBACCOUNT),
              "BY_ARGUMENT, OPENING": set(BY_ARGUMENT) | set(OPENING),
              "CARRIED": set(CARRIED)}


def _monthly_cells(proj):
    """Every cell of ``proj`` whose first parameter is ``t``."""
    return {name for name, cells in proj.cells.items()
            if cells.parameters and cells.parameters[0] == "t"}


def _on_the_clocks(p, t):
    """What each cell of :data:`CLOCK`, :data:`VALUATION_CLOCK` and :data:`LEVEL` holds.

    The policy clock in closed form from the point's ``duration_mth``, and the inputs on
    the valuation clock from the Projection's References and ``t`` alone, the same for
    every point: the flat declared rate, floored at the guaranteed one, and expense
    inflation stepping on valuation years; and the loan account's level credited rate.
    """
    d = p.duration_mth_init() + t
    rate = max(p.guar_rate_ann, p.crediting_rate_curr)
    lent = p.loan_cr_rate_ann_lvl
    return {"duration_mth": d, "duration": d // 12, "policy_year": d // 12 + 1,
            "age": p.age_at_entry() + d // 12,
            "crediting_rate_ann": rate, "fixed_return_mth": (1 + rate) ** (1 / 12) - 1,
            "inflation_factor": (1 + p.inflation_rate) ** (t // 12),
            "loan_cr_rate_ann": lent, "loan_cr_rate_mth": (1 + lent) ** (1 / 12) - 1}


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace, departs from what each monthly cell holds outside cover.

    In every month before issue and at ``t = proj_len()``: every cell of
    :data:`OUTSIDE_COVER` and :data:`NEUTRAL`, each cell of :data:`BY_SUBACCOUNT` at each
    subaccount and :data:`BY_ARGUMENT` at each of its timings or kinds, and before issue
    :data:`OPENING`'s and ``pols_if``, against their values with their types;
    :data:`CLOCK`, :data:`VALUATION_CLOCK` and :data:`LEVEL` against
    :func:`_on_the_clocks`.  At ``t = proj_len()`` :data:`IN_COVER_ONLY` reads a float, the
    count at every timing is the survivors of the last month, out of its count by its
    deaths and lapses, in the products those take, and the account value per policy is the
    last month's close.  Then the keyed readers: those keyed by a policy year hold keys
    from 1 to the year of the last month, the mortality table's keys from the age at the
    first month on the books to the age of the last, the corridor's from the issue age,
    which the pricing path reads from, and the pricing path's policy months from 0, issue,
    to the last month's, so no table was read at a year, an age or a policy month the
    policy does not have.  And no monthly cell holds a ``t`` past ``proj_len()``.  A cell
    that raises is a fault too, so the scan goes on.
    """
    faults = []
    L, entry = p.proj_len(), p.t_entry()
    ids = _subaccounts(p)

    def check(name, args, want):
        try:
            got = p.cells[name](*args)
        except Exception as err:                # reported, so the scan goes on
            faults.append(f"{where}: {name}{args} raised {_raised(err)}")
            return
        if got != want or type(got) is not type(want):
            faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")

    for t in [*range(entry), L]:
        for name, want in [*OUTSIDE_COVER.items(), *NEUTRAL.items()]:
            check(name, (t,), want)
        for i in ids:
            for name in BY_SUBACCOUNT[:-1]:
                check(name, (t, i), 0.0)
            for timing in AV_TIMINGS:
                check("sa_pp_at", (t, i, _code(p, timing)), 0.0)
        for name, labels in BY_ARGUMENT.items():
            for label in labels:
                check(name, (t, _code(p, label)), 0.0)
        if t < entry:
            for name, labels in OPENING.items():
                for label in labels:
                    check(name, (t, _code(p, label)), 0.0)
            check("pols_if", (t,), 0.0)
        for name, want in _on_the_clocks(p, t).items():
            check(name, (t,), want)
    for i in ids:
        for name in IN_COVER_ONLY:
            try:
                got = p.cells[name](L, i)
            except Exception as err:            # reported, so the scan goes on
                faults.append(f"{where}: {name}{(L, i)} raised {_raised(err)}")
                continue
            if type(got) is not float:
                faults.append(f"{where}: {name}{(L, i)} = {got!r}, not a float")
    survivors = p.pols_if(L - 1) - p.pols_death(L - 1) - p.pols_lapse(L - 1)
    check("pols_if", (L,), survivors)
    for timing in TIMINGS:
        check("pols_if_at", (L, _code(p, timing)), survivors)
    bef_prem = _code(p, "BEF_PREM")
    check("av_pp_at", (L, bef_prem), p.av_pp(L - 1))
    check("av_at", (L, bef_prem), p.av_pp_at(L, bef_prem) * p.pols_if(L))
    ranges = {**{name: range(1, p.policy_year(L - 1) + 1) for name in KEYED_BY_YEAR},
              **{name: range(p.age(entry), p.age(L - 1) + 1) for name in KEYED_BY_AGE},
              **{name: range(p.age_at_entry(), p.age(L - 1) + 1)
                 for name in KEYED_FROM_ISSUE}}
    for name, allowed in ranges.items():
        outside = sorted(k for k in p.cells[name].keys() if k not in allowed)
        if outside:
            faults.append(f"{where}: {name} read at {outside[:5]}, outside "
                          f"{allowed.start}..{allowed.stop - 1}")
    months = range(0, p.duration_mth(L - 1) + 1)
    for name in PRICING:
        outside = sorted({args[0] for args in _cached_args(p.cells[name])
                          if args[0] not in months})
        if outside:
            faults.append(f"{where}: {name} read at policy months {outside[:5]}, outside "
                          f"0..{months.stop - 1}")
    past = sorted(f"{name}{key}" for name in _monthly_cells(p)
                  for key in p.cells[name].keys()
                  if (key[0] if isinstance(key, tuple) else key) > L)
    if past:
        faults.append(f"{where}: evaluated past t = proj_len() = {L}: {past[:5]}")
    return faults


def _carry(p):
    """What the survivors of the last month carry into ``t = proj_len()`` on ``p``.

    The values the end-of-projection test asserts, read once the row is projected: the
    count there, at every timing, and the survivors it must be; the account value per
    policy there and the last month's close; the account value in force there; the three
    checks, which read it; and the flows of that month, which must be zero.
    """
    L = p.proj_len()
    bef_prem = _code(p, "BEF_PREM")
    return {
        "L": L, "pols_if": p.pols_if(L),
        "timings": [p.pols_if_at(L, _code(p, timing)) for timing in TIMINGS],
        "survivors": p.pols_if(L - 1) - p.pols_death(L - 1) - p.pols_lapse(L - 1),
        "av_pp": p.av_pp_at(L, bef_prem), "av_pp_last": p.av_pp(L - 1),
        "av_at": p.av_at(L, bef_prem),
        "checks": (p.check_av_roll_fwd(), p.check_margin(), p.check_net_view()),
        "flows": [p.premiums(L), p.pols_death(L), p.pols_lapse(L), p.expenses(L),
                  p.withdrawals(L), p.net_cf(L), p.claims_death(L), p.claims_lapse(L)]}


def _dyn_raw(x, t):
    """The dynamic lapse multiplier before its bounds: ``1 + beta (1 - phi_t)``."""
    return 1 + x.lapse_dyn_beta * (1 - x.funding_ratio(t))


def _pers_raw(x, t):
    """The premium persistency adjustment before its bounds, or None where phi <= 0."""
    phi = x.funding_ratio(t)
    return phi ** (-x.prem_pers_delta) if phi > 0 else None


def _face_raw(x, t):
    """The face after month ``t``'s Option A cut, before its floor at 0.

    The face entering month ``t``, as ``sum_assured_at`` reads it, less the cut: the
    previous month's face after ``t_entry()``; in the first month on the books, the face in
    force at the valuation date on a point in force, and the face at issue on any other.
    """
    if t > x.t_entry():
        face = x.sum_assured_at(t - 1)
    elif x.duration_mth_init() > 0:
        face = x.sum_assured_init()
    else:
        face = x.sum_assured()
    return face - x.face_reduction_pp(t)


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, on a row in force there, every
# opening-state column is in use, the face in force is below the face at issue, the face is
# cut in the valuation month, the collateral stands apart from the loan, each pin is
# applied at t = 0, each alone, with the other's month-0 value the rule's, the COI pin
# above the guaranteed rate that bounds it, and the shortfall has begun; and the end of the
# frame leaves survivors to carry.  Later in the frame, on every row, the branches the
# account value, the behaviour module, the corridor, the lapse spike, the loan, the COI cap
# and the ages that end the charges and begin the tables drive, each bound passed by the
# raw value it bounds, a COI scale read past its last year, and a face cut past 0, the face
# entering the month less the cut below 0 before the floor.
AT_VALUATION = {
    **{f"{column} in use": (lambda x, name=name, args=args: bool(
        x.cells[name](*_state_args(x, name, args))))
       for column, (name, args) in STATE.items()},
    "the face in force below the face at issue": lambda x: (
        0.0 < x.sum_assured_init() < x.sum_assured()),
    "a face cut at t = 0": lambda x: x.face_reduction_pp(0) > 0.0,
    "the collateral apart from the loan": lambda x: (
        0.0 < x.la_pp_init() != x.loan_bal_init()),
    "a corridor pin applied at t = 0": lambda x: (
        x.has_corridor_override_m1()
        and x.corridor_factor(0) != x.corridor_factor_at(x.age(0))),
    "a COI pin applied at t = 0": lambda x: (
        x.has_coi_rate_override_m1() and x.coi_rate(0) != x.coi_rate_at(x.policy_year(0))),
    "a corridor pin alone": lambda x: (
        x.has_corridor_override_m1() and not x.has_coi_rate_override_m1()
        and x.corridor_factor(0) == x.corridor_override_m1()
        and x.coi_rate(0) == x.coi_rate_at(x.policy_year(0))),
    "a COI pin alone": lambda x: (
        x.has_coi_rate_override_m1() and not x.has_corridor_override_m1()
        and x.coi_rate(0) != x.coi_rate_at(x.policy_year(0))
        and x.corridor_factor(0) == x.corridor_factor_at(x.age(0))),
    "a COI pin bound by the guaranteed rate": lambda x: (
        x.has_coi_rate_override_m1()
        and x.coi_rate_override_m1() > x.coi_rate(0) == x.coi_rate_guar(0)),
    "the shortfall at t = 0": lambda x: x.is_shortfall(0),
    "survivors carried into proj_len()": lambda x: x.pols_if(x.proj_len()) > 0.0,
}
IN_FRAME = {
    "the corridor binding on Option A": lambda x, t: (
        x.is_db_option_a() and x.db_pp(t) > x.sum_assured_at(t)),
    "the corridor binding on Option B": lambda x, t: (
        x.is_db_option_b()
        and x.db_pp(t) > x.sum_assured_at(t) + x.av_pp_at(t, _code(x, "BEF_FEE"))),
    "the lapse spike": lambda x, t: x.lapse_rate_sc_mult(t) > 1.0,
    "charges ceased in cover": lambda x, t: x.age(t) >= x.charges_cease_age,
    "the funding ratio at or below 0": lambda x, t: x.funding_ratio(t) <= 0.0,
    "the pricing path at or below 0": lambda x, t: (
        x.av_pricing_pp_at(x.duration_mth(t), _code(x, "BEF_PREM")) <= 0.0),
    "the dynamic lapse multiplier's floor binding": lambda x, t: (
        _dyn_raw(x, t) < x.lapse_dyn_floor),
    "the dynamic lapse multiplier's cap binding": lambda x, t: (
        _dyn_raw(x, t) > x.lapse_dyn_cap),
    "the premium persistency adjustment's floor binding": lambda x, t: (
        _pers_raw(x, t) is not None and _pers_raw(x, t) < x.prem_pers_floor),
    "the premium persistency adjustment's cap binding": lambda x, t: (
        _pers_raw(x, t) is not None and _pers_raw(x, t) > x.prem_pers_cap),
    "the deduction's fallback share": lambda x, t: (
        x.unloaned_av_pp_at(t, _code(x, "BEF_FEE")) <= 0.0),
    "the withdrawal's fallback share": lambda x, t: (
        x.wd_pp(t) > 0.0 and x.unloaned_av_pp_at(t, _code(x, "BEF_WD")) <= 0.0),
    "a subaccount below 0": lambda x, t: any(x.sa_pp(t, i) < 0.0
                                            for i in _subaccounts(x)),
    "the loan's preferred tier stepping in": lambda x, t: (
        x.duration_mth(t) == 12 * (x.loan_pref_year - 1)
        and x.loan_bal_pp_at(t, _code(x, "BEF_PREM")) > 0.0),
    "the COI cap binding with an effect": lambda x, t: (
        x.coi_rate_guar(t) == x.coi_rate_cap and x.coi_pp(t) > 0.0),
    "a table read below its first age": lambda x, t: x.age(t) < x.data.mort_age_first(),
    "a COI scale read past its last year": lambda x, t: (
        x.policy_year(t) > x.coi_rate_last_year()),
    "a face cut past 0, floored": lambda x, t: _face_raw(x, t) < 0.0,
    "a withdrawal": lambda x, t: x.wd_pp(t) > 0.0,
    "the single premium collected": lambda x, t: (
        x.is_single_premium() and x.premium_pp(t) > 0.0),
}


def _branches(x):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``.

    :data:`AT_VALUATION` asks about the state at the valuation date, which only a row in
    force holds; :data:`IN_FRAME` about the frame on the books, which a future row has too,
    and which alone has the single premium of new business and the pricing path's first
    month.
    """
    reached = set()
    if x.duration_mth_init() > 0:
        reached = {what for what, holds in AT_VALUATION.items() if holds(x)}
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in range(x.t_entry(), x.proj_len()))}


def _scanned(records, case, proj):
    """Run the row on the books and record :func:`_rule_breaches` for ``case``.

    Each T2 and T3 case calls this first, before it compares the row with S: the
    comparison evaluates SEC cells at S's cached keys, and the scan must see only what the
    row computes of itself, at its own months (USLIB-SEC-PLAN.md §7.9, *Carried into every
    product still to come*).  A row that raises is recorded as raising, which each test of
    the records reports.
    """
    try:
        record = {**_rule_breaches(proj), "raised": None}
    except Exception as err:                    # recorded, and reported by each test
        record = {"negative": [], "early": [], "ahead": [], "unjudged": [], "edges": 0,
                  "raised": _raised(err)}
    records[case] = record
    return record


def _settle(records, case, model, key):
    """Record what the tests after the splice need of a row, and release it.

    ``case`` is the row's (row_kind, S point, source_mth) and ``key`` its registry key in
    ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
    the row, whatever the comparison found, so the row is released either way.  To the
    scan's record it adds the row's :func:`_branches`, what :func:`_carry` reads at
    ``t = proj_len()`` and, last, so that its key ranges see every read the others made,
    :func:`_outside_cover_faults`.  A row no case has scanned is scanned here first.
    """
    try:
        proj = projection(model, key)
        record = records.get(case) or _scanned(records, case, proj)
        record.update(branches=set(), carry=None, guard=[])
        if record["raised"] is None:
            record["branches"] = _branches(proj)
            record["carry"] = _carry(proj)
            record["guard"] = _outside_cover_faults(proj, _case_id(*case))
    except Exception as err:                    # recorded, and reported by each test
        record = records.setdefault(case, {"negative": [], "early": [], "ahead": [],
                                           "unjudged": [], "edges": 0})
        record.update(branches=set(), carry=None, guard=[], raised=_raised(err))
    finally:
        _release(model, key)
    records[case] = record
    return record


def _record_of(spliced, records, case):
    """The record of ``case``, from the case that compared its row or, failing it, now."""
    if case not in records or "guard" not in records[case]:
        sec = spliced[1]
        _settle(records, case, sec, _row_key(sec, *case))
    return records[case]


# ---------------------------------------------------------------------------
# The every-state test (T5)
#
# Every state VUL_US_S reaches, restated in force by the generator, must be an opening state
# Data and proj_len() accept, but a state the product refuses by name, which is set aside
# and shown refused (USLIB-SEC-PLAN.md §5.2, T5, precised at M10 and M9).  The test runs
# under each set of inputs on which the states S reaches differ, and names them: the
# splice's, in the splice's class, S's shipped References and inputs, and BOUND_REFS, the
# References under which two bounds S ships idle bind, in the T5 section.


def _below(sp, d):
    """Whether an account of S point ``sp`` enters month ``d`` below 0.

    Each subaccount and the fixed option, at ``VUL_US_S``'s opening timing, the values the
    generator restates: the one bound of ``Data``'s that a state S reaches can fail.
    """
    accounts = [sp.sa_pp_at(d, i, "BEF_PREM") for i in _subaccounts(sp)]
    return min(*accounts, sp.fa_pp_at(d, "BEF_PREM")) < 0.0


def _every_state_months(sp):
    """The months S point ``sp`` is restated at by the every-state test.

    By default the edges of the windows ``Data`` and ``proj_len()`` hold a state over,
    and ``Data`` keys no rule of ``VUL_US_SEC``'s to a policy year or an anniversary: every
    month of its first year on S's frame, where the in-force rules' window opens, the month
    either side of each change in the sign of an account entering a month
    (:func:`_below`), where a state meets the bound ``Data`` holds the accounts to, and
    the last month of its frame, where ``proj_len()``'s window ends.  With
    ``USLIB_SEC_FULL=1``, every month of its frame.
    """
    n = sp.proj_len()
    if SEC_FULL:
        return list(range(1, n))
    below = [_below(sp, d) for d in range(n)]
    months = {*range(1, min(12, n)), n - 1}
    for d in range(1, n):
        if below[d] != below[d - 1]:
            months |= {d - 1, d}
    return sorted(m for m in months if m >= 1)


def _states_s_reaches(s):
    """The states ``s``'s points reach, as ``(S point, month)``: ``(kept, below)``.

    Each month of :func:`_every_state_months` of each point of ``s``, an S model, each
    point read in ascending months.  ``below`` holds the months an account enters below 0
    (:func:`_below`), the one state the product refuses by name: ``VUL_US_S`` carries an
    account below 0 once a permanent shortfall begins, or from issue where a withdrawal
    outruns the account, since it has no grace that would end such a policy, and no policy
    in force holds one (D6).  ``kept`` holds every other.
    """
    kept, below = [], []
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        sp = projection(s, key)
        for d in _every_state_months(sp):
            (below if _below(sp, d) else kept).append((point_id, d))
    return kept, below


def _restated(s, states, root, refs, edits=None):
    """A model of ``s``'s twins and a derived row at each of ``states``, and its table.

    The generator builds the table out of ``s`` as it stands, so each row opens with the
    state of the very run ``s`` made; the rows keep S's scenarios, which neither ``Data``
    nor ``proj_len()`` reads.  The model is read beside ``edits`` with ``refs`` set first.
    Returns ``(model, table)``, the table indexed by ``point_id``.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=())
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    folder = temp_inputs(root, model_path(SEC), model_points=table,
                         model_point_file=spec.model_point_file, edits=edits)
    return _read(folder, "every", refs), table.set_index("point_id")


def _refused_in_force(s, states, root, refs, edits=None):
    """What ``Data`` and ``proj_len()`` refuse of ``states`` of ``s``, restated in force.

    ``Data`` reads the table of :func:`_restated`, and then every row is asked for its
    frame and released, the collector run every 500.  Returns each refusal, the line naming
    it, ``Data``'s or each row's ``proj_len()``'s.
    """
    model, table = _restated(s, states, root, refs, edits)
    try:
        try:
            read = model.Data.model_point_table()
        except Exception as err:                # reported, with the rows' states
            return [f"Data: {_raised(err)}"]
        assert len(read) == len(table) == len(s.Data.model_point_table()) + len(states)
        refused = []
        for i, key in enumerate(point_keys(model)):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused.append(_raised(err))
            _release(model, key, collect=i % 500 == 499)
        return refused
    finally:
        model.close()


def _refused_by_name(s, state, root, refs, edits=None):
    """``Data`` refuses ``state`` of ``s``, an account below 0, restated in force, by name.

    The message, matched whole, names the row and says when a point in permanent shortfall
    may be restated; the first subaccount is the first account it names.
    """
    model, table = _restated(s, [state], root, refs, edits)
    try:
        _refused_exactly(model.Data.model_point_table, _AV_NUMBER.format(
            column="sa_pp_init_1", point=_label(table, "derived", *state)).format(
                file=TABLE))
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The splice: T2, T3 and what their rows show
#
# Every test that reads the splice's models is in this class, whose fixtures they are, so
# that the models are closed before the committed model and S are read (the module
# docstring).


class TestTheSplice:
    """T2 and T3 on the splice's grid, and the tests that read its rows' records."""

    @pytest.mark.parametrize(
        "kind, s_point, month",
        [_case(case, CORE_SPLICES, _case_id(*case)) for case in SPLICES + IN_FORCE_TWINS])
    def test_an_in_force_point_continues_its_s_projection(self, spliced, splice_records,
                                                          kind, s_point, month):
        """Opened with S's state at month d, the point is S from d on, in every cell of S's.

        This is the test that says the opening state is complete: a state column the SEC
        row did not carry, or carried from the wrong instant, would make SEC part from S
        here, and nowhere else, because on a point issued at ``t = 0`` the two clocks
        coincide and the opening state is zero.  Each subaccount and the fixed option open
        from their own columns, never the allocation of the account value, the loan
        account from its own, apart from the debt once interest has accrued, and the face
        from the face in force.  For the same reason it is the test that catches a policy
        month passed as ``t`` (R1a), a look-back that stops at the wrong month, a pin
        applied in the wrong month, and a return read on the wrong clock: each row reads
        its S scenario re-based to its own month, and the scenarios move every month.
        The frame comparisons read SEC row ``t`` against S row ``t + d`` in every column of
        the four reports both models hold, and fail frames that end apart.  The cell
        comparison then evaluates every cell of S's but :data:`SPLICE_EXEMPT`, at every
        argument S cached inside its own frame from month ``d`` on, moved onto SEC's
        clock: the accounts at every timing, the debt, the face, the counts, the checks,
        and the pricing path at S's own keys, policy months from issue, which are the same
        months on both models.  An S cell this model lacked would fail it.  The first
        default and shortfall months are then the first S finds at or after ``d``, less
        ``d`` (:func:`_first_month`).

        S's own in-force points, opened at its ``t = 0``, are cases too, at offset 0, and
        their twins skip only T1's exemptions: their opening accessors are S's.  Every
        value is held to 1e-9 relative with no absolute floor, because near the end of a
        long frame the counts fall far below 1e-7, to 2.8e-14 on variant 9, where the floor
        would compare them against nothing.  ``VUL_US_S`` has no residual cell, its checks
        being bools, so no compared cell is a residual rounding around 0 that keeps the
        floor; this model's three residual cells are held through the checks, which are
        compared as bools.

        The row is scanned for the rules test first (:func:`_scanned`), then compared, then
        recorded for the tests after this one and released (:func:`_settle`).
        """
        s, sec = spliced
        case = (kind, s_point, month)
        key = _row_key(sec, *case)
        try:
            sec_proj = projection(sec, key)
            _scanned(splice_records, case, sec_proj)
            s_proj = _point(s, s_point)
            for report in REPORTS:
                assert frame_mismatches(s_proj.cells[report](), sec_proj.cells[report](),
                                        t_offset=month, atol=0.0) == [], report
            exempt = TWIN_EXEMPT if kind == "twin" else SPLICE_EXEMPT
            assert _twin(s_proj, sec_proj, t_offset=month, exempt=exempt, atol=0.0) == []
            for cell, flag in FIRST_MONTHS.items():
                assert sec_proj.cells[cell]() == _first_month(s_proj, flag, month), cell
        finally:
            _settle(splice_records, case, sec, key)

    @pytest.mark.parametrize(
        "s_point, k",
        [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
         for case in FUTURES])
    def test_future_new_business_is_the_s_projection_k_months_on(self, spliced,
                                                                 splice_records, s_point,
                                                                 k):
        """Issued k months after the valuation date, the point is S's projection k on.

        SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of the
        projection, in the four reports, and every cell of S's but :data:`FUTURE_EXEMPT`
        agrees at every argument S cached inside its own frame, moved ``k`` later, to 1e-9
        relative with no absolute floor, ``pols_if_at`` at every timing but ``"BEF_NB"`` in
        the issue month (:func:`_issued_later`), and the pricing path at S's own policy
        months.  An S cell this model lacked would fail it.  The first default and
        shortfall months are S's, ``k`` later.  Before issue every column of the four
        reports is an exact zero, and the policies arrive in month ``k`` as new business.  A
        single premium is collected once, in the issue month.

        The last assertions are R1 and D4's base rule made testable.  After every report,
        no decrement rate keyed by month has been evaluated at a month before issue; no
        table keyed by a policy year has been read below year 1, the mortality table below
        the issue age, or the corridor below it, the pricing path's first age; no cell of
        the pricing path has been read at a policy month before issue; and no return has
        been read before issue, where the row's re-based scenario holds none
        (:func:`_rebase`) and a read would have raised.  A chain based at ``t == 0`` rather
        than at ``t_entry()``, or a rate evaluated before the month is asked whether it is
        in cover, still gives the right numbers.  This is the only test that sees the
        first, and the guard test sees the second too.

        The pre-issue rows are asserted present before they are asserted zero, in each of
        the reports: a frame that opened at issue would have none, its zeros would hold of
        nothing, and the comparisons with S, which start at issue, would not see it.  The
        row is scanned for the rules test first (:func:`_scanned`), and recorded and
        released once compared (:func:`_settle`).
        """
        s, sec = spliced
        case = ("future", s_point, -k)
        key = _row_key(sec, *case)
        try:
            sec_proj = projection(sec, key)
            _scanned(splice_records, case, sec_proj)
            s_proj = _point(s, s_point)
            frames = {report: sec_proj.cells[report]() for report in REPORTS}
            for report, frame in frames.items():
                assert frame_mismatches(s_proj.cells[report](), frame, t_offset=-k,
                                        atol=0.0) == [], report
            assert _twin(s_proj, sec_proj, t_offset=-k, exempt=FUTURE_EXEMPT,
                         arg_map=_issued_later, atol=0.0) == []
            for cell, flag in FIRST_MONTHS.items():
                assert sec_proj.cells[cell]() == _first_month(s_proj, flag, -k), cell
            for report, frame in frames.items():
                assert list(frame.index[:k]) == list(range(k)), report
                assert (frame.loc[:k - 1] == 0.0).all().all(), report
            assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
            early = {name: sorted(t for t in sec_proj.cells[name].keys() if t < k)
                     for name in DECREMENT_RATES}
            assert not any(early.values()), f"rates evaluated before issue: {early}"
            floors = {**dict.fromkeys(KEYED_BY_YEAR, 1),
                      **dict.fromkeys(KEYED_BY_AGE + KEYED_FROM_ISSUE,
                                      sec_proj.age_at_entry())}
            for name, floor in floors.items():
                keys = sorted(sec_proj.cells[name].keys())
                assert all(key >= floor for key in keys), f"{name} read at {keys[:5]}"
            assert sec_proj.cells["mort_rate_base_at"].keys(), "no mortality rate was read"
            for name in PRICING:
                low = sorted({args[0] for args in _cached_args(sec_proj.cells[name])
                              if args[0] < 0})
                assert not low, f"{name} read at policy months {low[:5]}"
            for name in IN_COVER_ONLY:
                low = sorted({t for t, i in _cached_args(sec_proj.cells[name]) if t < k})
                assert not low, f"{name} read before issue, at {low[:5]}"
            if sec_proj.is_single_premium():
                assert [sec_proj.premium_pp(t) for t in range(sec_proj.proj_len())] == [
                    sec_proj.premium_pp_ann() if t == k else 0.0
                    for t in range(sec_proj.proj_len())]
        finally:
            _settle(splice_records, case, sec, key)

    @pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                      pytest.param("full", id="full", marks=FULL_ONLY)])
    def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(
            self, spliced, splice_records, grid):
        """R1, its look-back and R2's look-ahead, on the rows T2 and T3 compare.

        Each is a rule of how the model computes, not of what, so no number shows a
        breach, and on a point issued at ``t = 0`` the two clocks coincide and hide it from
        T1 too.  The splice's rows are points in force at every month T2 names, the variants
        among them, and points issued later, each with the behaviour module on, which reads
        the pricing path; and each is run on the books first, its four reports, its checks
        and every monthly cell at every month on the books, as Phase 2's sweep
        (:func:`_sweep_on_the_books`), so that a read no report makes is judged too:

        * R1: no cell holds a negative argument, a month, a policy month, a policy year or
          an age.  modelx evaluates one without complaint, and a compiled cache raises
          ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  The pricing path's policy months
          among them: a funding ratio asked before issue would ask it for a negative one.
        * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
          ``t_entry()`` on read a month before it.  On a point issued later a chain based at
          ``t == 0``, as ``VUL_US_S``'s subaccounts, fixed option, loan account, debt, face
          and count all were, and the account value's opening balance, reads the pre-issue
          zeros, so no number shows it and no argument goes negative.  This is the test
          that holds those bases at ``t_entry()`` (R1a).  No report reads the account
          value's opening balance in the issue month, where the funding ratio returns
          before it, so the checks and the sweep are what reach that base.  The pricing
          path is the one look-back allowed: a projection made at issue, based at issue on
          purpose (:func:`_rule_breaches`).
        * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month
          beyond ``t + 1``, nor the pricing path at a policy month beyond the one ``t + 1``
          is, as modelx's dependency graph records each cached call's precedents.  VUL has
          no read further ahead, so R2's one exception has no use here.
        * The premise of the two scans: no cell without a ``t`` but the loops over the frame
          reads one keyed by ``t``, so a read through a cell keyed by a policy month, a
          policy year, an age or a subaccount is a read of the month that asked, and the
          pricing path reads nothing on the valuation clock.

        Each row was scanned by the T2 or T3 case that compared it, before the comparison
        (:func:`_scanned`), and a row no case has scanned is scanned here.  The core case
        covers the core's rows, the full case every other row of the full grid, with
        ``USLIB_SEC_FULL=1``.  The new-business twins in the splice's table are no case's,
        and are left out: on them the clocks coincide, and T1 compares them with S cell by
        cell.  The closed-form clock and the recursion depth are asserted on the committed
        model, in the tests after this class.
        """
        cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
        found = {"negative": [], "early": [], "ahead": [], "unjudged": []}
        raised, unscanned = [], []
        for case in cases:
            record, where = _record_of(spliced, splice_records, case), _case_id(*case)
            for rule, calls in found.items():
                calls += [f"{where}: {call}" for call in record[rule]]
            if record["raised"]:
                raised.append(f"{where}: {record['raised']}")
            elif not record["edges"]:
                unscanned.append(where)
        assert cases, f"the {grid} grid has no rows"
        assert not raised, f"rows that raised: {raised[:10]}"
        assert not unscanned, f"rows whose scan read no precedent: {unscanned[:10]}"
        assert not found["negative"], (
            f"called before the valuation date: {found['negative'][:10]}")
        assert not found["early"], (
            f"read before issue from the books: {found['early'][:10]}")
        assert not found["ahead"], f"read beyond t + 1: {found['ahead'][:10]}"
        assert not found["unjudged"], (
            f"a cell without a month reads one keyed by t: {found['unjudged'][:10]}")

    def test_every_guarded_cell_holds_its_outside_cover_value_on_the_splice(
            self, spliced, splice_records):
        """Outside cover each monthly cell holds its value on every row the splice compared.

        :data:`GUARD_SETS` say what each cell whose first parameter is ``t`` holds before
        issue and at ``t = proj_len()``, the month after the frame, which the roll-forwards
        read (:func:`_outside_cover_faults`).  On every row the splice compared, the core's
        or, with ``USLIB_SEC_FULL=1``, all of them, as each was recorded once compared
        (:func:`_settle`): there the survivors carried into ``t = proj_len()`` are not zero,
        the behaviour module is on, so the funding ratio is asked of the pricing path in
        cover and must not be before issue, and the variants' future rows read policy years
        -1 and 0 before issue, the single premium's among them, which has no cliff.  Then on
        two withdrawal rows read afresh from the splice's folder with charges ceasing at
        attained age 125, past the frame's end, where no contractual age stops a withdrawal,
        a premium or a charge at ``t = proj_len()`` and only the guard can: variant 6 issued
        13 months on and variant 5 restated at 12.

        That every monthly cell is in one set, and in one only, is asserted on the committed
        model (:func:`test_every_guarded_cell_holds_its_outside_cover_value`).
        """
        faults = []
        cases = _selected(GRID, CORE_GRID)
        for case in cases:
            record = _record_of(spliced, splice_records, case)
            if record["raised"]:
                faults.append(f"{_case_id(*case)}: raised {record['raised']}")
            faults += record["guard"]
        sec = spliced[1]
        late = _read(sec.Data.input_dir() / SEC, "charges_125",
                     {**SPLICED_REFS, "charges_cease_age": 125})
        try:
            for case in (("future", 6, -13), ("derived", 5, 12)):
                key = _row_key(late, *case)
                faults += _outside_cover_faults(projection(late, key),
                                                f"{_case_id(*case)}, charges_cease_age 125")
                _release(late, key)
        finally:
            late.close()
        assert cases and not faults, (
            f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))

    def test_the_end_of_the_projection_carries_the_survivors(self, spliced, splice_records):
        """The survivors of the last month, and their account value, are carried, as in S.

        The projection ends where the mortality table does, at attained age 122, not where
        the contract does, which never matures, and S's roll-forwards read the month after
        the frame.  At the splice's A/E of 0.56 there are lives left at the end of every
        frame, 1.13e-5 of a policy on S's in-force point 4, so on every row the splice
        compared, the core's or, with ``USLIB_SEC_FULL=1``, all of them:

        * the count at ``t = proj_len()``, at every timing, is the survivors of the last
          month, exactly, and not zero;
        * the account value per policy there is the last month's close, exactly, and the
          account value in force there the two multiplied;
        * both are S's at the same month, ``proj_len() + source_mth`` on S's clock, exactly
          on the twins and the future rows, whose opening values are S's own and not read
          back from a CSV, and to 1e-9 on the rest; and the three checks, which read them,
          hold in both models;
        * and nothing else happens there: no premium, death, lapse, withdrawal, claim or
          expense, and a net cash flow of 0.

        On the committed points, at the shipped A/E, every life has died by then, and the
        count carried is exactly 0 (the count test).
        """
        s = spliced[0]
        cases = _selected(GRID, CORE_GRID)
        faults = []
        for case in cases:
            kind, s_point, month = case
            where = _case_id(*case)
            record = _record_of(spliced, splice_records, case)
            carry = record["carry"]
            if carry is None:
                faults.append(f"{where}: raised {record['raised']}")
                continue
            exact = kind != "derived"
            s_proj, s_month = _point(s, s_point), carry["L"] + month
            theirs = (s_proj.pols_if(s_month),
                      s_proj.av_at(s_month, _code(s_proj, "BEF_PREM")))
            mine = (carry["pols_if"], carry["av_at"])
            if not carry["survivors"] > 0.0:
                faults.append(f"{where}: no survivors at t = proj_len()")
            if carry["pols_if"] != carry["survivors"] or any(
                    count != carry["survivors"] for count in carry["timings"]):
                faults.append(f"{where}: the count carried is not the survivors: {carry}")
            if (carry["av_pp"] != carry["av_pp_last"]
                    or carry["av_at"] != carry["av_pp"] * carry["pols_if"]):
                faults.append(f"{where}: the account value carried is not the close: "
                              f"{carry}")
            close = pytest.approx(theirs, rel=1e-9, abs=0.0)
            if not (mine == theirs if exact else mine == close):
                faults.append(f"{where}: {mine} carried, where S carries {theirs}")
            s_checks = (s_proj.check_av_roll_fwd(), s_proj.check_margin(),
                        s_proj.check_net_view())
            if carry["checks"] != (True, True, True) or s_checks != (True, True, True):
                faults.append(f"{where}: a check fails: SEC {carry['checks']}, "
                              f"S {s_checks}")
            if any(flow != 0.0 for flow in carry["flows"]):
                faults.append(f"{where}: flows at t = proj_len(): {carry['flows']}")
        assert cases and not faults, faults[:10]
        twin = _record_of(spliced, splice_records, ("twin", 4, 0))["carry"]
        assert twin["pols_if"] == pytest.approx(1.1309e-5, rel=1e-3)

    def test_the_face_in_force_opens_from_its_own_column(self, spliced, tmp_path):
        """The face in force, not the face at issue, is cut and insured in month 0.

        ``VUL_US_S`` opens a point at the face at issue.  Variant 6, withdrawing $100 a
        month on Option A, has cut its face by S's month 13 to 195,991.00 of the 500,000 it
        was issued at; restated there, month 0's withdrawal cuts it by 4,926.76 more, in the
        proportion the withdrawal bears to the account value, and month 0's death benefit
        is 191,064.25, the face that leaves.  Read again with ``sum_assured_init`` at the
        face at issue, as ``VUL_US_S`` would open it, the same withdrawal cuts the face by
        the same proportion of 500,000, and the death benefit is what that leaves.  Both
        rows charge the surrender charge on the face at issue, through ``units()``, which no
        cut moves.
        """
        sec = spliced[1]
        table = sec.Data.model_point_table()
        built = table.loc[[_label(table, "derived", 6, 13)]]
        restart = built.assign(sum_assured_init=built["sum_assured"],
                               policy_id=built["policy_id"] + "-S")
        restart.index = pd.Index([1000], name="point_id")
        model = _read(temp_inputs(tmp_path, sec.Data.input_dir() / SEC,
                                  model_points=pd.concat([built, restart]),
                                  model_point_file=TABLE), "face", SPLICED_REFS)
        try:
            a, z = _point(model, built.index[0]), _point(model, 1000)
            assert a.sum_assured_init() == pytest.approx(195991.00, abs=0.005)
            assert a.face_reduction_pp(0) == pytest.approx(4926.76, abs=0.005)
            assert a.db_pp(0) == pytest.approx(191064.25, abs=0.005)
            assert a.sum_assured_at(0) == a.sum_assured_init() - a.face_reduction_pp(0)
            assert z.sum_assured_init() == z.sum_assured() == 500000.0
            cut = a.face_reduction_pp(0) * 500000.0 / a.sum_assured_init()
            assert z.face_reduction_pp(0) == pytest.approx(cut, rel=1e-12)
            assert z.sum_assured_at(0) == pytest.approx(500000.0 - cut, rel=1e-12)
            assert z.db_pp(0) == pytest.approx(z.sum_assured_at(0), rel=1e-12)
            assert a.surr_charge_pp(0) == z.surr_charge_pp(0) > 0.0
        finally:
            model.close()

    def test_the_core_grid_reaches_every_branch(self, spliced, splice_records):
        """What the default run's T2 and T3 cases reach, which the full grid multiplies.

        The default run thins the splice to a core (the module docstring), and this test is
        what keeps the thinning from costing a branch.  First, statically, over S's table
        with the variants, each property below holds of some core case: each death benefit
        option, each premium pattern, withdrawals on either option, a loan, a fixed option,
        each scenario, each sex, each of the six classes, each surrender charge schedule and
        none, each issue age, S's in-force points as their twins and restated, and each kind
        of valuation month, on the policy clock: mid-year, the month before an anniversary,
        on an anniversary, the month before the lapse spike and the spike's own month, in
        shortfall, and the last covered month.  The core is chosen by the lines it covers,
        and a branch that differs only in the month it fires covers no line of its own: a
        spike skipped in the first month on the books passed every core row until one was
        valued in its spike month.  And of some core future case: issued off the valuation
        anniversaries and on them, more than a year on, with withdrawals, a single premium
        and no surrender charge.  VUL premiums are annual amounts paid monthly, the one mode
        the product models, so no mode is asked for.

        Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
        :data:`IN_FRAME`, what no column of the table shows: every opening-state column in
        use, the face in force below the face at issue and cut at ``t = 0``, the collateral
        apart from the loan, each pin applied at ``t = 0``, each pin alone, so that
        neither's flag can stand in for the other's, the COI pin above the guaranteed rate
        that bounds it, the shortfall at ``t = 0`` and survivors carried into
        ``t = proj_len()``; and
        later in the frame the corridor on either option, the lapse spike, charges ceased in
        cover, the funding ratio and the pricing path at or below 0, each bound of the
        dynamic lapse multiplier and of the premium persistency adjustment passed, the
        deduction's and the withdrawal's fallback shares, a subaccount below 0, the loan's
        preferred tier stepping in, the COI cap binding where it moves the charge, a table
        read below its first age, a COI scale read past its last year, a face cut past 0
        before its floor, a withdrawal and the single premium collected.  The two bounds
        no splice reference can bind, the guaranteed rate over a current scale above it and
        the declared rate's floor, are asserted, against ``VUL_US_S``, by
        :func:`test_the_coi_bound_and_the_declared_rate_floor_bind_as_in_vul_us_s`.

        Each core row's branches were recorded by the T2 or T3 case that compared it
        (:func:`_settle`), and a row no case has recorded is evaluated here.
        """
        s = spliced[0]
        s_table = _s_table_with_variants()
        schedules = _surr_charges_with_vul10(pd.read_csv(
            model_path(TWIN).parent / "surr_charge_table.csv")).set_index("surr_charge_id")
        classes = pd.read_csv(model_path(TWIN).parent / "class_factor_table.csv")[
            "rate_class"]

        def at(p, column):
            return s_table.at[p, column]

        def month(p, d):
            return int(at(p, "duration_mth")) + d

        def frame(p):
            return 12 * (s.Projection.omega_age - int(at(p, "age_at_entry")) + 1)

        def spike(p):
            if not at(p, "has_surr_charge"):
                return None
            return 12 * int(schedules.at[at(p, "surr_charge_id"), "runoff_years"])

        splices = {
            **{f"Option {o}": (lambda k, p, d, o=o: at(p, "db_option") == o) for o in "AB"},
            **{f"{pattern} premiums": (
                lambda k, p, d, x=pattern: at(p, "premium_type") == x)
               for pattern in ("LEVEL", "SINGLE")},
            **{f"withdrawals on Option {o}": (
                lambda k, p, d, o=o: at(p, "wd_pp") > 0.0 and at(p, "db_option") == o)
               for o in "AB"},
            "a loan": lambda k, p, d: at(p, "loan_bal_init") > 0.0,
            "a fixed option": lambda k, p, d: (
                at(p, "fa_pp_init") > 0.0 and at(p, "alloc_fixed") > 0.0),
            **{f"scenario {x}": (lambda k, p, d, x=x: at(p, "scenario_id") == x)
               for x in ("WE", "LEVEL6")},
            **{f"sex {x}": (lambda k, p, d, x=x: at(p, "sex") == x) for x in "MF"},
            **{f"class {c}": (lambda k, p, d, c=c: at(p, "rate_class") == c)
               for c in classes},
            **{f"schedule {i}": (
                lambda k, p, d, i=i: at(p, "has_surr_charge")
                and at(p, "surr_charge_id") == i)
               for i in schedules.index},
            "no surrender charge": lambda k, p, d: not at(p, "has_surr_charge"),
            **{f"issue age {a}": (lambda k, p, d, a=a: at(p, "age_at_entry") == a)
               for a in (45, SECOND_AGE)},
            "S's in-force point as its twin": lambda k, p, d: (
                k == "twin" and at(p, "duration_mth") > 0),
            "S's in-force point restated": lambda k, p, d: (
                k == "derived" and at(p, "duration_mth") > 0),
            "mid-year": lambda k, p, d: month(p, d) % 12 not in (0, 11),
            "the month before an anniversary": lambda k, p, d: month(p, d) % 12 == 11,
            "on an anniversary": lambda k, p, d: month(p, d) > 0 and month(p, d) % 12 == 0,
            "the month before the lapse spike": lambda k, p, d: (
                spike(p) is not None and month(p, d) == spike(p) - 1),
            "on the lapse spike": lambda k, p, d: (
                spike(p) is not None and month(p, d) == spike(p)),
            "in shortfall": lambda k, p, d: _point(s, p).is_shortfall(d),
            "the last covered month": lambda k, p, d: month(p, d) == frame(p) - 1,
        }
        futures = {
            "issued off the anniversaries": lambda p, k: k % 12 != 0,
            "issued on them": lambda p, k: k % 12 == 0,
            "issued more than a year on": lambda p, k: k > 12,
            "withdrawals": lambda p, k: at(p, "wd_pp") > 0.0,
            "a single premium": lambda p, k: at(p, "premium_type") == "SINGLE",
            "no surrender charge": lambda p, k: not at(p, "has_surr_charge"),
        }
        missing = [what for what, holds in splices.items()
                   if not any(holds(*case) for case in CORE_SPLICES)]
        missing += [what for what, holds in futures.items()
                    if not any(holds(*case) for case in CORE_FUTURES)]
        assert not missing, f"no core case reaches: {missing}"

        reached, raised = set(), []
        for case in CORE_GRID:
            record = _record_of(spliced, splice_records, case)
            reached |= record["branches"]
            if record["raised"]:
                raised.append(f"{_case_id(*case)}: {record['raised']}")
        assert not raised, raised
        missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
        assert not missing, f"no core row reaches: {missing}"

    def test_the_points_sum_row_by_row_into_a_block(self, spliced):
        """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

        S point 3's twin, the point restated at month 12 and the point issued 12 months on,
        each reading its scenario on its own valuation clock, summed as ``run_sec.py
        --block`` sums them, are indexed 0..935 and equal S's frame added to itself moved
        12 months earlier and 12 months later, with no tolerance beyond 1e-9 relative.  A
        model whose frames sat on the policy clock would fail it.
        """
        s, sec = spliced
        keys = [_row_key(sec, *case)
                for case in (("twin", 3, 0), ("derived", 3, 12), ("future", 3, -12))]
        try:
            frames = [projection(sec, key).result_cf() for key in keys]
        finally:
            for key in keys:
                _release(sec, key)
        block = pd.concat(frames).groupby(level="t").sum()
        sdf = _point(s, 3).result_cf()
        expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                              sdf.set_axis(sdf.index + 12)]).groupby(level=0).sum()
        assert list(block.index) == list(range(936))
        assert frame_mismatches(expected, block, atol=0.0) == []

    def test_every_state_s_reaches_is_accepted_in_force(self, spliced, tmp_path):
        """Every state the splice's S reaches is a valid opening state, but one (T5).

        ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in
        force can hold, so they must accept each state ``VUL_US_S`` reaches: a rule
        exercised only on the rows the other tests choose could refuse a state S reaches
        elsewhere (D6; §5.2, T5, precised at M10).  So every S point of the splice, S's four
        and the nine variants, under the splice's References and inputs and swept, is
        restated in force by the generator at the edges of its windows, or with
        ``USLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
        one table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses
        it (:func:`_refused_in_force`).  But for one state, set aside first: an account
        below 0, which ``VUL_US_S`` reaches on S's point 3 and variant 5 once their
        permanent shortfall begins and on variant 13 from its first month, where its
        withdrawal outruns its account, and which ``Data`` refuses by name, since no policy
        in force holds one.  It is the only state set aside, and a table holding one is
        refused, naming the point and saying what to do.  This is one of the three sets of
        inputs the test runs under, each one on which the states S reaches differ (§5.2,
        T5, precised at M9): the splice's here, S's shipped References and inputs, and
        :data:`BOUND_REFS` (the T5 section).  Expense inflation and the A/E move no state
        but the count, which ``Data`` holds only to a number, zero or more, so the
        splice's References with either changed reach these states; and at the module's
        other inputs, the cap test's point, the loan test's and the rising returns, probed
        at every month, ``Data`` and ``proj_len()`` refuse none but an account below 0.
        """
        s = spliced[0]
        kept, below = _states_s_reaches(s)
        assert {point for point, _ in below} == {3, 5, 13}, sorted(set(below))[:5]
        assert {point for point, _ in kept} == set(s.Data.model_point_table().index) - {13}
        refused = _refused_in_force(s, kept, tmp_path / "every", SPLICED_REFS,
                                    SPLICED_EDITS)
        assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
        _refused_by_name(s, below[0], tmp_path / "below", SPLICED_REFS, SPLICED_EDITS)


# ---------------------------------------------------------------------------
# D3's closed-form clock, R2's forward recursions and D5's chains, on the committed model


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(500)`` on
      the twin of S's point 1, in force 24 months, is 524 and evaluates ``duration_mth``
      once, where ``BasicTerm_SE``'s recursion would evaluate it at all 501 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow, which is why D3 is asserted on its own.  A backward recursion over the
      frame, through ``t + 1``, keeps every step within the look-ahead but opens a chain as
      long as the frame, which a compiled model would run on the C stack (F7), and fails
      here.
    * No projection cell reads a label accessor (``sex``, ``rate_class``, ``db_option``,
      ``qual_test``, ``premium_type``, ``surr_charge_id``, ``scenario_id``): once every
      point is swept, none holds a key.  The decodes and the per-point joins read
      ``model_point()``, and the accessors are kept for reporting, as Phase 2 declares
      them (USLIB-SEC-PLAN.md R17).
    """
    record = sec_read[1]
    assert record["duration_mth(500)"] == 524
    assert record["keys"] == [500]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"
    read = {point: labels for point, labels in record["labels"].items() if labels}
    assert not read, f"label accessors read by the sweep, by point: {read}"


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


def _one_cell_a_month(label, depth, chain, call):
    """Whether a cold call ran ``depth`` cells deep over a chain ``chain`` months long.

    It must run at least as deep as its chain, or it did not run its chain cold, and at
    most :data:`CHAIN_OVERHEAD` cells deeper.  Returns the finding, or nothing.
    """
    if chain <= depth <= chain + CHAIN_OVERHEAD:
        return []
    return [f"point {label}: {call} cold runs {depth} cells deep, where its chain is "
            f"{chain} months and {CHAIN_OVERHEAD} more are allowed"]


def _longest_cover(tmp_path):
    """A copy whose table holds S point 3 at issue age 0, issued now and 120 months on.

    ``VUL_US_S``'s frame from issue is ``12 * (omega_age - issue age + 1)`` months, and the
    product spec issues from age 0, so the longest cover is 1,464 months, and the longest
    frame that issued 120 months on, the shipped ``future_horizon_mth``, 1,584 months,
    whose chains stop at ``t_entry()``.  The copy's COI table gains rows for ``(M, StdNT,
    0)``, for policy years 1 to 122, and its mortality and corridor tables ages 0 to 17,
    each geometric or graded in its key, so that a key read for another changes a number.
    """
    committed = _committed()
    now, later = _label(committed, "twin", 3, 0), _label(committed, "future", 3, -25)
    table = _set("duration_mth", [later], -120)(
        committed.loc[[now, later]].assign(age_at_entry=0))

    def coi(rates):
        years = list(range(1, 123))
        young = pd.DataFrame({
            "sex": "M", "rate_class": "StdNT", "age_at_entry": 0, "policy_year": years,
            "coi_rate_guar": [round(0.03 * 1.065 ** (y - 1), 6) for y in years],
            "provenance": "test copy"})
        return pd.concat([rates, young], ignore_index=True).sort_values(
            COI_KEYS, ignore_index=True)

    def younger(column, value):
        def edit(rates):
            ages = list(range(18))
            young = pd.DataFrame({"age": ages, column: [value(a) for a in ages],
                                  "provenance": "test copy"})
            return pd.concat([young, rates], ignore_index=True)
        return edit

    edits = {"coi_rates.csv": coi,
             "mort_table.csv": younger("mort_rate", lambda a: round(0.0002 * 1.04 ** a, 6)),
             "corridor_factors.csv": younger(
                 "corridor_factor", lambda a: round(2.5 + 0.001 * (18 - a), 6))}
    return _sec_inputs(tmp_path, table, edits=edits), (now, later)


# Each chain of the model and the cell that heads it, called cold at the last month the
# chain reaches: (cell, its month as months from proj_len(), its other arguments, the
# chain's own recursive cells).  They are called in this order on one fresh read, an order
# in which no chain is reached before its own head is called, which is checked: the debt,
# the loan account, the face, the accounts and the count.  The subaccounts and the fixed
# option are one chain: each month's withdrawal and deduction are shared over them in
# proportion to their values, so whichever is called first runs the others alongside it,
# one cell a month.  The face reads the accounts only through a withdrawal, and the points
# this test reads withdraw nothing; the accounts read the face through the death benefit,
# by then cached.
CHAIN_HEADS = (("loan_bal_pp", -1, (), ("loan_bal_pp_at",)),
               ("la_pp", -1, (), ("la_pp_at",)),
               ("sum_assured_at", -1, (), ("sum_assured_at",)),
               ("sa_pp_at", -1, (2, "BEF_PREM"), ("sa_pp_at", "fa_pp_at")),
               ("pols_if_at", 0, ("BEF_NB",), ("pols_if_at",)))


def _chains_cold(folder, labels, refs):
    """The cold depths of :data:`CHAIN_HEADS` on ``labels`` of the model in ``folder``.

    One fresh read a point, with ``refs`` set first, each head called in turn, each chain
    checked cold before its head is called.  With the behaviour module off a chain runs
    back to ``t_entry()``.  Returns the findings.
    """
    found = []
    for label in labels:
        fresh = _read(folder, "chains", refs)
        try:
            p = _point(fresh, label)
            end = p.proj_len()
            for cell, offset, rest, chain in CHAIN_HEADS:
                warm = [name for name in chain if len(p.cells[name].keys())]
                if warm:
                    found.append(f"point {label}: {warm} reached before {cell} was "
                                 f"called, so its chain was not cold")
                    continue
                t = end + offset
                args = (t, *(_code(p, x) if isinstance(x, str) else _sa(p, x)
                             for x in rest))
                found += _one_cell_a_month(label, _cold_depth(p, cell, args),
                                           t - p.t_entry(), f"{cell}{args}")
        finally:
            fresh.close()
    return found


def _net_cf_cold(folder, labels, refs, from_issue):
    """The cold depth of ``net_cf`` in the last month of each of ``labels``, one read each.

    The chain runs back to ``t_entry()``, or with the behaviour module on back to issue,
    through the pricing path, whose depth is the policy month from issue: ``from_issue``.
    """
    found = []
    for label in labels:
        fresh = _read(folder, "cold", refs)
        try:
            p = _point(fresh, label)
            last = p.proj_len() - 1
            chain = p.duration_mth(last) if from_issue else last - p.t_entry()
            found += _one_cell_a_month(label, _cold_depth(p, "net_cf", (last,)), chain,
                                       f"net_cf({last})")
        finally:
            fresh.close()
    return found


def _pricing_cold(folder, labels, refs):
    """The cold depth of the pricing path's opening value in each point's last month.

    One fresh read a point, ``av_pricing_pp_at`` alone at the policy month of the last
    month of the frame: the path is based at issue, so its chain is that policy month.
    """
    found = []
    for label in labels:
        fresh = _read(folder, "pricing", refs)
        try:
            p = _point(fresh, label)
            m = p.duration_mth(p.proj_len() - 1)
            args = (m, _code(p, "BEF_PREM"))
            found += _one_cell_a_month(label, _cold_depth(p, "av_pricing_pp_at", args), m,
                                       f"av_pricing_pp_at{args}")
        finally:
            fresh.close()
    return found


def _ascending(folder, limits, refs):
    """Whether each point sweeps in ascending ``t`` under its own recursion limit.

    ``limits`` maps a label to the limit, as ``mx.set_recursion`` takes it.  One fresh
    read a point, with ``refs`` set first, and :func:`sec_support.sweep` run on the point
    under the limit, as the committed model is first swept (:func:`sec_read`).  Returns the
    findings.
    """
    found = []
    for label, limit in limits.items():
        fresh = _read(folder, "ascending", refs)
        old = mx.get_recursion()
        try:
            mx.set_recursion(limit)
            try:
                sweep(_point(fresh, label))
            except Exception as err:            # reported, so every point is swept
                found.append(f"point {label}: its ascending sweep exceeds a recursion "
                             f"limit of {limit}: {_raised(err)}")
        finally:
            mx.set_recursion(old)
            fresh.close()
    return found


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
@pytest.mark.parametrize("case", [
    pytest.param("shipped", id="shipped"),
    pytest.param("module on", id="module-on"),
    pytest.param("module on, longest cover", id="module-on-longest", marks=FULL_ONLY)])
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path, case):
    """Called cold, each chain runs one cell a month back to its base, no more (D5, R2).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7).  ``VUL_US_S``'s subaccounts ran through six cells a month, its
    fixed option through five, its loan account and debt through two, and its pricing path
    through four; here each forms the previous month's close itself.  On a model just read,
    nothing is cached, so modelx's stack trace counts how deep a call runs, against one
    cell a month and :data:`CHAIN_OVERHEAD` more:

    * ``shipped``, at the shipped References: on the twins of S's in-force points 1 and 4,
      ``net_cf`` in the last month, on a read of its own, the deepest call a projection
      makes, down the accounts' chain to ``t_entry()``; then, on a second read, each of
      :data:`CHAIN_HEADS` alone, in an order that leaves each chain cold until its own head
      is called, which is checked, so the chains a ``net_cf`` call reaches from the side
      are measured too; and the same at the contract's longest cover, issue age 0, issued
      now and 120 months on (:func:`_longest_cover`).
    * ``module on``, with the behaviour module on: on the same two twins, a cold ``net_cf``
      in the last month runs one cell a month back to **issue**, not to ``t_entry()``,
      through the funding ratio, which reads the pricing path at the policy month from
      issue, a projection made at issue and based there (R2, as precised for VUL); and on a
      third read the pricing path alone, ``av_pricing_pp_at`` at that policy month, the
      same chain.  And swept in ascending ``t``, as a report or Phase 2's sample sweeps
      it, a point in force runs back to issue too, since its first month reads the path
      cold: the two twins sweep under a recursion limit of ``duration_mth_init()`` and
      :data:`CHAIN_OVERHEAD`, and the twin of S's new business and the row issued 25
      months on, whose paths start at their issue months, under :data:`CALL_DEPTH`, the
      limit of the module off (:func:`_ascending`).
    * ``module on, longest cover``, with the full grid: the module on at the longest cover,
      whose pricing path is the deepest chain the contract allows, 1,463 months, whether
      the policy is issued at the valuation date or 120 months on.
    """
    committed = _committed()
    twins = [_label(committed, "twin", p, 0) for p in (1, 4)]
    on = {"dyn_behavior_on": True}
    found = []
    if case == "shipped":
        found += _net_cf_cold(model_path(SEC), twins, {}, from_issue=False)
        found += _chains_cold(model_path(SEC), twins, {})
        folder, labels = _longest_cover(tmp_path)
        found += _net_cf_cold(folder, labels, {}, from_issue=False)
        found += _chains_cold(folder, labels, {})
    elif case == "module on":
        found += _net_cf_cold(model_path(SEC), twins, on, from_issue=True)
        found += _pricing_cold(model_path(SEC), twins, on)
        limits = {label: int(committed.at[label, "duration_mth"]) + CHAIN_OVERHEAD
                  for label in twins}
        for later in (_label(committed, "twin", 3, 0), _label(committed, "future", 3, -25)):
            limits[later] = CALL_DEPTH
        found += _ascending(model_path(SEC), limits, on)
    else:
        folder, labels = _longest_cover(tmp_path)
        found += _net_cf_cold(folder, labels, on, from_issue=True)
        found += _pricing_cold(folder, labels, on)
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths and lapses alone, and nothing matures.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, "BEF_DECR")``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, "BEF_NB")``, is the outflows of month ``t``, to 1e-12, the last row
    included, whose survivors are carried into ``t = proj_len()``: ``pols_if`` there is the
    last month's count less its deaths and lapses, exactly, the products they take.  At the
    shipped A/E every life has died by then, since the table's rate is 1.0 from attained
    age 119, so the count carried is exactly 0.  And ``"BEF_MAT"``, the count before any
    maturity, is the ``"BEF_DECR"`` count in every month, that one included,
    ``VUL_US_S``'s meaning, since nothing matures.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb, bef_decr, bef_mat = (_code(p, x) for x in ("BEF_NB", "BEF_DECR", "BEF_MAT"))
        end = p.proj_len()
        for t in range(end):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, bef_decr) - p.pols_if_at(t + 1, bef_nb)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
        assert all(p.pols_if_at(t, bef_mat) == p.pols_if_at(t, bef_decr)
                   for t in range(end + 1)), point_id
        assert p.pols_if(end) == (p.pols_if(end - 1) - p.pols_death(end - 1)
                                  - p.pols_lapse(end - 1)) == 0.0, point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(end))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, all at offset 0: the new-business one
    and S's three in force.  Every column S's report has agrees, to 1e-9 relative with no
    absolute floor, frames ending together, and ``pols_new_biz`` holds the count in the
    issue month and 0 in every other, so 0 throughout on the points in force.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == [theirs.columns[0], "pols_new_biz",
                                      *theirs.columns[1:]], point_id
        month = int(table.at[point_id, "source_mth"])
        assert frame_mismatches(theirs, mine, t_offset=month, atol=0.0) == [], point_id
        issue = -int(table.at[point_id, "duration_mth"])
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == issue else 0.0 for t in mine.index], point_id


# The References the scaling test sets in both copies: the splice's, which switch on every
# assumption that ships at zero or off, and expense inflation, which the splice leaves at 0
# (USLIB-SEC-PLAN.md §5.2, T4).
SWITCHED_ON = {**SPLICED_REFS, "inflation_rate": INFLATION}

# The counted cells, and report columns, that are differences of products of the count:
# each side scales by the factor rounded its own way, so where the two sides nearly cancel
# the difference keeps their rounding, which is relative to the sides, not to it.  These
# are held to 1e-12 of their largest magnitude on the point; every other counted value to
# 1e-12 relative, value by value.  Measured on the five points of the test: av_change at
# 95 keys, up to 1.7e-8 relative, net_cf and margin_expense at one key each, 1.4e-12 and
# 4.5e-12, each within 1.2e-13 of its peak; net_cf_ga and margin_mortality, differences
# of the same kind, at 1.5e-13 and 5e-15.  claims_over_av is not one of them: its
# difference is per policy, scaled once, within 6e-15 of each value.
DIFFERENCES = frozenset({"av_change", "net_cf", "net_cf_ga", "margin_expense",
                         "margin_mortality"})
REPORT_DIFFERENCES = {"result_cf": ("net_cf",), "result_net": ("net_cf_ga",)}
# The per-policy columns of the reports: the rates of result_pols, the net amount at risk
# of result_net, and the whole of result_av.
PER_POLICY = {"result_pols": RATES, "result_net": ("naar",)}


def _scaled_faults(base, scaled, where):
    """Where ``scaled`` is not :data:`COUNT_FACTOR` times ``base``, cell by cell.

    Every key the base point's sweep cached of every cell of :data:`COUNTED`, value by
    value: to 1e-12 relative, or for :data:`DIFFERENCES` to 1e-12 of the cell's largest
    magnitude on the point.
    """
    faults = []
    for name in sorted(COUNTED):
        cells = base.cells[name]
        keys = _cached_args(cells)
        values = [(args, cells(*args), scaled.cells[name](*args)) for args in keys]
        peak = max((abs(a) for _, a, _ in values), default=0.0)
        for args, a, b in values:
            want = COUNT_FACTOR * a
            scale = COUNT_FACTOR * peak if name in DIFFERENCES else abs(want)
            if not abs(b - want) <= 1e-12 * scale:
                faults.append(f"{where}: {name}{args} = {b!r}, not {want!r}")
    return faults


def test_scaling_the_count_scales_every_flow_and_no_per_policy_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow (T4).

    Two copies of the committed table's twins of S points 1, 3 and 4, its row restated six
    months after point 4 and its row issued 25 months on, each withdrawing $100 a month,
    the second with every count :data:`COUNT_FACTOR` times the first's, are read with
    :data:`SWITCHED_ON` set first: every assumption that ships at zero or off switched on,
    so that every flow is nonzero on some point, acquisition on new business, the behaviour
    module, inflation, the loan's spread and the collateral, the pins and the withdrawals
    and their fees among them; every row pays a level premium.  A factor that is not whole
    sees a count truncated to whole policies, and a flow left at zero sees no count at all.
    Point by point, each released once compared:

    * every counted column of the four reports is 2.5 times the first's, to 1e-12 relative,
      value by value, a difference of products (``net_cf``, ``net_cf_ga``) to 1e-12 of its
      peak;
    * every cell of :data:`COUNTED` at every key the first's sweep cached is 2.5 times the
      first's, value by value (:func:`_scaled_faults`);
    * ``result_pols``' rates, ``result_net``'s net amount at risk and the whole of
      ``result_av``, the account value roll-forward per policy, are the first's exactly;
    * every other cell is the first's exactly, at every key, but the three residuals, which
      are relative and move in the last digits; and the three checks hold on both;

    and every cell of :data:`COUNTED` but ``pols_maturity`` is nonzero on some point.
    """
    committed = _committed()
    rows = [_label(committed, kind, p, m)
            for kind, p, m in (("twin", 1, 0), ("twin", 3, 0), ("twin", 4, 0),
                               ("derived", 4, 6), ("future", 3, -25))]
    base_table = committed.loc[rows].assign(wd_pp=100.0)
    models = {}
    try:
        for tag, factor in (("one", 1.0), ("scaled", COUNT_FACTOR)):
            table = base_table.assign(policy_count=factor * base_table["policy_count"])
            models[tag] = _read(_sec_inputs(tmp_path / tag, table), tag, SWITCHED_ON)
        one, scaled = models["one"], models["scaled"]
        faults, nonzero = [], set()
        for key, two_key, point_id in zip(point_keys(one), point_keys(scaled), rows):
            base, two = projection(one, key), projection(scaled, two_key)
            sweep(base)
            for report in REPORTS:
                b, d = base.cells[report](), two.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                if report == "result_av":
                    assert d.equals(b), (point_id, report)
                    continue
                same = PER_POLICY.get(report, ())
                assert d[list(same)].equals(b[list(same)]), (point_id, report)
                for c in b.columns:
                    if c in same:
                        continue
                    want = COUNT_FACTOR * b[c]
                    if c in REPORT_DIFFERENCES.get(report, ()):
                        scale = COUNT_FACTOR * b[c].abs().max()
                    else:
                        scale = want.abs()
                    bad = (d[c] - want).abs() > 1e-12 * scale
                    assert not bad.any(), (point_id, report, c, list(b.index[bad])[:5])
            faults += _scaled_faults(base, two, f"point {point_id}")
            nonzero |= {name for name in COUNTED
                        if any(base.cells[name](*args) != 0.0
                               for args in _cached_args(base.cells[name]))}
            assert _twin(base, two, exempt=TWIN_EXEMPT_DEFAULT | COUNTED | set(RELATIVE)
                         | set(REPORTS), rtol=0.0, atol=0.0) == [], point_id
            assert (base.check_av_roll_fwd(), base.check_margin(), base.check_net_view(),
                    two.check_av_roll_fwd(), two.check_margin(), two.check_net_view()
                    ) == (True,) * 6, point_id
            del base, two
            _release(one, key)
            _release(scaled, two_key)
        assert not faults, f"{len(faults)} values do not scale, first: {faults[:10]}"
        assert nonzero == COUNTED - {"pols_maturity"}, sorted(COUNTED - nonzero)
    finally:
        for model in models.values():
            model.close()


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration, an amount, a
# share or a balance that is not a number, and a share, the premium load or an allocation,
# past 1 as well as below 0.  The repeated point_id holds another policy under the same
# label, as a bad extract would, so that the check must look at the labels and not at whole
# rows.  The point_ids are the committed table's: 1 and 2, S's points in force at 24, 1
# with its pins; 3, S's new business; 4, S's point in force at 120 with a loan; 5, S point
# 3 at 12; 6, S point 4 six months on, at 126, its collateral and its loan parted; 7, S
# point 3 at 593; 8, S point 4 at 888; 9, issued 25 months on.  Each case is refused by
# its own rule alone, or, where a case pins a rule's place, by its rule first, on a row a
# later rule would refuse differently: a fractional duration on the future row, which the
# horizon would refuse; a blank face at issue on a row in force, which the face-at-most
# rule would; a negative or text collateral or loan, or one on a row not yet in force,
# beside the rule that pairs the two; a negative, infinite or text face in force, which
# the in-force face rules would read as written; and a negative pin on the future row.  A
# rule over a window of policy months is refused just inside each end of it (§5.2, T5,
# precised at M10): an opening state on a point not yet in force at the horizon, -120, as
# well as at 0 and -25, where that window's last month is 0; a face in force of 0, or above
# the face at issue, a month in force, the first month of the in-force rules' window; and
# a pin on a point issued a month after the valuation date and at the horizon, the ends of
# its window, as well as at -25.  The edges test accepts each just outside its window,
# where a state can be: an opening state a month in force, and a pin on a point issued at
# the valuation date.  A {file} in a message is the table's filename: every case is read
# from a file of its own (the malformed fixture).

_NUMBER = ("{{file}}: {column} must be a number, zero or more; it is not at point_id "
           "[{point}]")
_SHARE = ("{{file}}: {column} must be a number from 0 to 1; it is not at point_id "
          "[{point}]")
_AV_NUMBER = ("{{file}}: {column} must be a number, zero or more: no policy in force holds "
              "a negative account value, so restate a point in permanent shortfall no "
              "later than the last month its account value is still zero or more; it is "
              "not at point_id [{point}]")
_NOT_IN_FORCE = ("{{file}}: {column} must be 0 on a policy not yet in force, "
                 "duration_mth 0 or less; it is not at point_id [{point}]")
_PIN = ("{{file}}: {column} must be blank or a number, zero or more; it is not at "
        "point_id [{point}]")
_PIN_LATER = ("{{file}}: {column} must be blank on a policy issued after the valuation "
              "date, duration_mth below 0: a pin applies in the valuation month, t = 0, "
              "before such a policy is issued; it is not at point_id [{point}]")
_FACE = ("{file}: sum_assured must be a number above 0, the face at issue, which every "
         "policy holds; it is not at point_id [{point}]")
_FLAG = "{file}: has_surr_charge must be True or False; it is not at point_id [{point}]"
_AGE = ("{file}: age_at_entry must be a whole number of years, 0 or more; it is not at "
        "point_id [{point}]")
_PAIRED = ("{file}: la_pp_init must be above 0 where loan_bal_init is, and 0 where it is "
           "0: the loan account holds a loan's collateral while the loan is outstanding; "
           "it is not at point_id [{point}]")

# The columns Data reads, each refused when the table lacks it.
READ_COLUMNS = ("policy_count", "duration_mth", "age_at_entry", "sum_assured",
                "premium_pp_ann", "load_prem_rate", "alloc_1", "alloc_2", "alloc_fixed",
                "wd_pp", "has_surr_charge", *STATE, *PINS)

MALFORMED = [
    ("a negative count", _set("policy_count", [4], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [4]"),
    ("a blank count", _set("policy_count", [5], float("nan")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [5]"),
    ("two bad counts", _set("policy_count", [4, 6], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [4, 6]"),
    ("a text count", _set("policy_count", [6], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [6]"),
    ("an infinite count", _set("policy_count", [6], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [6]"),
    ("a fractional duration on the future row", _set("duration_mth", [9], -120.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a blank duration", _set("duration_mth", [9], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a text duration", _set("duration_mth", [6], "x126"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [6]"),
    ("issued beyond the horizon", _set("duration_mth", [9], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [9]"),
    ("a duration of 2**53 months", _set("duration_mth", [6], 2.0 ** 53),
     "{file}: duration_mth must be below 2**53 months in size; it is not at point_id [6]"),
    *[(f"an age_at_entry {what}", _set("age_at_entry", [5], value), _AGE.format(
        file="{file}", point=5))
      for what, value in (("of 45.5", 45.5), ("below 0", -1), ("as text", "45y"),
                          ("blank", float("nan")))],
    ("an age_at_entry of 2**53", _set("age_at_entry", [5], 2.0 ** 53),
     "{file}: age_at_entry must be below 2**53 in size; it is not at point_id [5]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in READ_COLUMNS],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[4]].assign(policy_id="VUL-900099")]),
     "{file}: point_id [4] appears more than once"),
    ("a blank face at issue on a row not in force", _set("sum_assured", [3], float("nan")),
     _FACE.format(file="{file}", point=3)),
    ("a blank face at issue in force", _set("sum_assured", [5], float("nan")),
     _FACE.format(file="{file}", point=5)),
    ("a face at issue of 0", _set("sum_assured", [1], 0.0),
     _FACE.format(file="{file}", point=1)),
    ("a text face at issue", _set("sum_assured", [9], "500k"),
     _FACE.format(file="{file}", point=9)),
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("text", "premium_pp_ann", 4, "x"), ("blank", "premium_pp_ann", 3, float("nan")),
          ("text", "wd_pp", 2, "a lot"), ("infinite", "wd_pp", 8, float("inf")))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _SHARE.format(column=column, point=point))
      for what, column, point, value in (
          ("infinite", "load_prem_rate", 6, float("inf")),
          ("negative", "load_prem_rate", 2, -0.04), ("above 1", "load_prem_rate", 3, 1.5),
          ("blank", "alloc_1", 4, float("nan")), ("text", "alloc_2", 7, "40%"),
          ("above 1", "alloc_1", 4, 1.5), ("negative", "alloc_fixed", 4, -0.1))],
    *[(f"has_surr_charge {what}", _set("has_surr_charge", [point], value),
       _FLAG.format(file="{file}", point=point))
      for what, point, value in (("blank", 3, float("nan")), ("Yes", 2, "Yes"),
                                 ("1", 2, 1))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _AV_NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("negative", "sa_pp_init_1", 7, -1.0), ("blank", "sa_pp_init_2", 6, float("nan")),
          ("text", "fa_pp_init", 4, "x10000"),
          ("infinite", "sa_pp_init_1", 5, float("inf")))],
    *[(f"a {what} {column}", _set(column, [point], value),
       _NUMBER.format(column=column, point=point))
      for what, column, point, value in (
          ("negative", "la_pp_init", 6, -1.0), ("text", "loan_bal_init", 6, "x"),
          ("infinite", "la_pp_init", 4, float("inf")),
          ("negative", "sum_assured_init", 5, -1.0),
          ("infinite", "sum_assured_init", 5, float("inf")),
          ("text", "sum_assured_init", 5, "100k"))],
    *[(f"{column} before issue", _set(column, [point], value),
       _NOT_IN_FORCE.format(column=column, point=point))
      for column, point, value in (
          ("sa_pp_init_1", 3, 100.0), ("sa_pp_init_2", 9, 50.0), ("fa_pp_init", 3, 10.0),
          ("la_pp_init", 9, 5.0), ("loan_bal_init", 9, 10.0),
          ("sum_assured_init", 3, 500000.0))],
    ("a zero face in force", _set("sum_assured_init", [5], 0.0),
     "{file}: sum_assured_init must be above 0 on a policy in force, duration_mth above 0, "
     "which holds a face; it is not at point_id [5]"),
    ("a face above the face at issue", _set("sum_assured_init", [5], 500000.01),
     "{file}: sum_assured_init must be at most sum_assured, the face at issue, since face "
     "increases are not modelled; it is not at point_id [5]"),
    ("collateral with no loan", _set("la_pp_init", [1], 100.0),
     _PAIRED.format(file="{file}", point=1)),
    ("a loan with no collateral", _set("la_pp_init", [4], 0.0),
     _PAIRED.format(file="{file}", point=4)),
    *[(f"a {what} {column}", _set(column, [point], value),
       _PIN.format(column=column, point=point))
      for what, column, point, value in (
          ("text", "corridor_override_m1", 1, "2.15x"),
          ("negative", "coi_rate_override_m1", 1, -0.04),
          ("infinite", "corridor_override_m1", 2, float("inf")),
          ("negative, on the future row,", "coi_rate_override_m1", 9, -0.04))],
    *[(f"a {column} on the future row", _set(column, [9], value),
       _PIN_LATER.format(column=column, point=9))
      for column, value in (("corridor_override_m1", 2.15),
                            ("coi_rate_override_m1", 0.04))],
    ("sa_pp_init_1 before issue, issued at the horizon",
     _moved(9, -120, sa_pp_init_1=100.0), _NOT_IN_FORCE.format(column="sa_pp_init_1",
                                                                point=9)),
    ("a zero face a month in force", _moved(5, 1, sum_assured_init=0.0),
     "{file}: sum_assured_init must be above 0 on a policy in force, duration_mth above 0, "
     "which holds a face; it is not at point_id [5]"),
    ("a face above the face at issue a month in force",
     _moved(5, 1, sum_assured_init=500000.01),
     "{file}: sum_assured_init must be at most sum_assured, the face at issue, since face "
     "increases are not modelled; it is not at point_id [5]"),
    *[(f"a {column} on a point issued {when}", _moved(9, month, **{column: value}),
       _PIN_LATER.format(column=column, point=9))
      for column, value, month, when in (
          ("corridor_override_m1", 2.15, -1, "a month on"),
          ("coi_rate_override_m1", 0.04, -120, "at the horizon"))],
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """One copy of the product directory, and beside it each table of :data:`MALFORMED`.

    Each table is a file of its own, so each case reads the model afresh and points
    ``Data.model_point_file`` at its file before anything is computed.  Returns
    ``(the copy's SEC folder, {case: filename})``.
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

    And so does the base ``Projection``'s first month, at its default point, read on its
    own: the projection reaches the table through ``model_point()``, and a compiled model's
    must reach the same check, rather than a value it has no number for.  The message is
    matched whole, so that a case another rule refused first would fail here.
    """
    folder, files = malformed
    model = mx.read_model(folder, name=_name("malformed"))
    try:
        model.Data.model_point_file = files[case]
        text = message.format(file=files[case])
        _refused_exactly(model.Data.model_point_table, text)
        _refused_exactly(lambda: model.Projection.net_cf(0), text)
    finally:
        model.close()


# Each assumption table, with one fault in its key column, as an extract or an edit by hand
# can leave it: a blank key, which pandas reads as a missing value, a key written as text,
# a fractional one, keys that repeat or leave a gap, a first policy year missing or below
# 1, and no row at all.  The blank is the case that matters most: VUL_US_S's readers take a
# table's extent from the key column as pandas reads it, where a blank last key is a
# missing value the extent skips, so the table is cut short and every later year reads the
# last good row without a word.  Here each table is checked once, in the Data cell its
# reader takes its extent, its count or its lineup from, and refused naming the file and
# the column: the lines a key that is blank, text or fractional is on, and each key that
# repeats or falls below 1, with its lines, and each that is missing.  Each case is (case,
# the file, its edit, the Data cell that checks it, the message), and the message is
# matched whole.  The lines count the header as line 1: the policy year y of a table that
# starts at year 1 is on line y + 1, and the anchor cell's year y of the COI scale too; the
# age tables start at age 18, on line 2.
_WHOLE = "{file}: {column} must be a whole number; it is not on line {lines}"
_RUNS = {"policy_year": ("{file}: the policy years must run from 1, one row a year, "
                         "without a gap or a repeat; "),
         "age": "{file}: the ages must run one row an age, without a gap or a repeat; "}
_COI_RUN = ("coi_rates.csv: the policy years of each sex, rate_class and age_at_entry "
            "must run from 1, one row a year, without a gap or a repeat; at ('M', "
            "'StdNT', 45), ")
_SCENARIO_RUN = ("scenario_table.csv: the months of each scenario_id and subaccount_id "
                 "must run one row a month, from 0 or later, without a gap or a repeat; "
                 "at ('WE', 1), ")


def _write_at(column, row, value):
    """An edit that writes ``value`` into ``column`` of the table's ``row``-th row."""
    def edit(table):
        cells = table[column].astype(object)
        cells.iloc[row] = value
        return table.assign(**{column: cells})
    return edit


def _write_rows(column, rows, value):
    """An edit that writes ``value`` into ``column`` of each of the table's ``rows``."""
    def edit(table):
        cells = table[column].astype(object)
        for row in rows:
            cells.iloc[row] = value
        return table.assign(**{column: cells})
    return edit


def _repeat_key(column, row):
    """An edit that gives the table's ``row``-th row the key of the row before it."""
    def edit(table):
        cells = table[column].astype(object)
        cells.iloc[row] = cells.iloc[row - 1]
        return table.assign(**{column: cells})
    return edit


def _drop_row(row):
    """An edit that drops the table's ``row``-th row, which leaves a gap in its keys."""
    return lambda table: table.drop(index=table.index[row])


def _no_row(table):
    """An edit that leaves the table its header and no row."""
    return table.iloc[0:0]


def _twice(row):
    """An edit that writes the table's ``row``-th row again, at its end."""
    return lambda table: pd.concat([table, table.iloc[[row]]], ignore_index=True)


# Each table read at a policy year or an attained age: (its key column, the Data cell that
# checks it, its first key, the row each case edits, which leaves a key before it).  The
# premium persistency scale holds six years, the lapse table eleven, and the corridor and
# mortality tables the ages 18 to 121.
KEY_TABLES = {
    "prem_persistency.csv": ("policy_year", "prem_persistency_last_year", 1, 3),
    "lapse_table.csv": ("policy_year", "lapse_last_year", 1, 4),
    "corridor_factors.csv": ("age", "corridor_age_last", 18, 9),
    "mort_table.csv": ("age", "mort_age_last", 18, 9),
}
_LAST_LINE = {"prem_persistency.csv": 7, "lapse_table.csv": 12, "corridor_factors.csv": 105,
              "mort_table.csv": 105}
MALFORMED_KEYS = [
    *[(f"{file}: {what}", file, _write_at(column, row, value), check,
       _WHOLE.format(file=file, column=column, lines=f"[{line}]"))
      for file, (column, check, _, edited) in KEY_TABLES.items()
      for what, row, value, line in (
          ("its last key blank", -1, float("nan"), _LAST_LINE[file]),
          ("a key written as text", edited, "6x", edited + 2),
          ("a fractional key", edited, 10.5, edited + 2))],
    *[(f"{file}: {what}", file, edit, check, _RUNS[column].format(file=file) + fault)
      for file, (column, check, first, edited) in KEY_TABLES.items()
      for what, edit, fault in (
          ("a repeated key", _repeat_key(column, edited),
           f"{column} {first + edited - 1} is on line [{edited + 1}, {edited + 2}]; "
           f"no line holds {column} {first + edited}"),
          ("a gap", _drop_row(edited), f"no line holds {column} {first + edited}"),
          ("no row", _no_row, "no line holds policy_year 1" if column == "policy_year"
           else "no line holds an age"))],
    *[(f"{file}: a negative age", file, _write_at("age", 0, -1), check,
       f"{file}: age must be 0 or more; it is not on line [2]")
      for file, (column, check, _, _) in KEY_TABLES.items() if column == "age"],
    *[(f"{file}: its first year missing", file, _drop_row(0), check,
       _RUNS[column].format(file=file) + "no line holds policy_year 1")
      for file, (column, check, _, _) in KEY_TABLES.items() if column == "policy_year"],
    ("lapse_table.csv: a policy year below 1", "lapse_table.csv",
     _write_at("policy_year", 0, 0), "lapse_last_year",
     _RUNS["policy_year"].format(file="lapse_table.csv")
     + "policy_year 0 is on line [2]; no line holds policy_year 1"),
    ("prem_persistency.csv: its policy years from 0", "prem_persistency.csv",
     lambda table: table.assign(policy_year=table["policy_year"] - 1),
     "prem_persistency_last_year",
     _RUNS["policy_year"].format(file="prem_persistency.csv")
     + "policy_year 0 is on line [2]"),
    *[(f"coi_rates.csv: {what}", "coi_rates.csv", edit, "coi_rate_last_years", message)
      for what, edit, message in (
          ("its last policy year blank", _write_at("policy_year", -1, float("nan")),
           _WHOLE.format(file="coi_rates.csv", column="policy_year", lines="[78]")),
          ("an issue age written as text", _write_at("age_at_entry", 4, "45x"),
           _WHOLE.format(file="coi_rates.csv", column="age_at_entry", lines="[6]")),
          ("a fractional policy year", _write_at("policy_year", 9, 10.5),
           _WHOLE.format(file="coi_rates.csv", column="policy_year", lines="[11]")),
          ("its last sex blank", _write_at("sex", -1, float("nan")),
           "coi_rates.csv: sex must not be blank; it is on line [78]"),
          ("a blank rate_class", _write_at("rate_class", 3, float("nan")),
           "coi_rates.csv: rate_class must not be blank; it is on line [5]"),
          ("a repeated policy year", _repeat_key("policy_year", 9),
           _COI_RUN + "policy_year 9 is on line [10, 11]; at ('M', 'StdNT', 45), no line "
           "holds policy_year 10"),
          ("a gap", _drop_row(4), _COI_RUN + "no line holds policy_year 5"),
          ("its first year missing", _drop_row(0),
           _COI_RUN + "no line holds policy_year 1"),
          ("its first policy year written 0", _write_at("policy_year", 0, 0),
           _COI_RUN + "policy_year 0 is on line [2]; at ('M', 'StdNT', 45), no line holds "
           "policy_year 1"))],
    ("class_factor_table.csv: a blank rate_class", "class_factor_table.csv",
     _write_at("rate_class", 2, float("nan")), "class_count",
     "class_factor_table.csv: rate_class must not be blank; it is on line [4]"),
    ("class_factor_table.csv: a repeated rate_class", "class_factor_table.csv",
     _repeat_key("rate_class", 3), "class_count",
     "class_factor_table.csv: each rate_class must have one row; rate_class StdPlusNT is "
     "on line [4, 5]"),
    ("surr_charge_table.csv: a blank surr_charge_id", "surr_charge_table.csv",
     _write_at("surr_charge_id", 0, float("nan")), "surr_charge_count",
     "surr_charge_table.csv: surr_charge_id must not be blank; it is on line [2]"),
    ("surr_charge_table.csv: a repeated surr_charge_id", "surr_charge_table.csv",
     _twice(0), "surr_charge_count",
     "surr_charge_table.csv: each surr_charge_id must have one row; surr_charge_id VUL14 "
     "is on line [2, 3]"),
    *[(f"subaccount_table.csv: {what}", "subaccount_table.csv", edit, "subaccounts",
       message)
      for what, edit, message in (
          ("a blank subaccount_id", _write_at("subaccount_id", 0, float("nan")),
           _WHOLE.format(file="subaccount_table.csv", column="subaccount_id",
                         lines="[2]")),
          ("a subaccount_id written as text", _write_at("subaccount_id", 1, "two"),
           _WHOLE.format(file="subaccount_table.csv", column="subaccount_id",
                         lines="[3]")),
          ("a fractional subaccount_id", _write_at("subaccount_id", 1, 1.5),
           _WHOLE.format(file="subaccount_table.csv", column="subaccount_id",
                         lines="[3]")),
          ("a repeated subaccount_id", _repeat_key("subaccount_id", 1),
           "subaccount_table.csv: each subaccount_id must have one row; subaccount_id 1 is "
           "on line [2, 3]"),
          ("no row", _no_row, "subaccount_table.csv: no line holds a subaccount"))],
    *[(f"scenario_table.csv: {what}", "scenario_table.csv", edit, "scenario_last_mths",
       message)
      for what, edit, message in (
          ("a blank scenario_id", _write_at("scenario_id", 2, float("nan")),
           "scenario_table.csv: scenario_id must not be blank; it is on line [4]"),
          ("a subaccount_id written as text", _write_at("subaccount_id", 1, "one"),
           _WHOLE.format(file="scenario_table.csv", column="subaccount_id", lines="[3]")),
          ("a blank month", _write_at("t", 1, float("nan")),
           _WHOLE.format(file="scenario_table.csv", column="t", lines="[3]")),
          ("a fractional month", _write_at("t", 1, 0.5),
           _WHOLE.format(file="scenario_table.csv", column="t", lines="[3]")),
          ("a repeated month", _repeat_key("t", 1),
           _SCENARIO_RUN + "t 0 is on line [2, 3]"),
          ("a gap", _write_at("t", 1, 3), _SCENARIO_RUN + "no line holds t 1 to 2"),
          ("a month below 0", _write_at("t", 0, -1),
           _SCENARIO_RUN + "t -1 is on line [2]"))],
]

# Each value a reader reads, blank, written as text and infinite, in every table: the rates
# and factors keyed by a policy year or an age, the class factors, the surrender charge,
# the fund expenses and the returns.  VUL_US_S reads a blank as a missing value, which
# shows in its flows or is lost in a min or a max: a blank corridor factor reads as no
# corridor, a blank surrender charge as none, a blank COI rate, fund expense or return as
# an account value that is not a number, which the cash value's floor then reads as
# nothing to pay; and this model's capped mortality, min(q, 1.0), keeps a blank base rate
# or class factor missing, where its bound first would read it as 1.  Then values outside
# their range: a lapse or mortality rate above 1 or below 0, which is no probability, and a
# class factor, a guaranteed COI rate, a fund expense, a premium persistency factor or a
# surrender charge below 0, each of which projects, with every check passing, a negative
# death or premium, a credit, or a surrender charge that rises once its schedule has run
# off.  Then values no point reads, a factor of a class no point carries and a rate at an
# age none reaches, and two lines at fault in one column; and the run-off, which must be a
# whole number of years, 1 or more, since the model divides by it and counts policy years
# on it.  Each case is as in MALFORMED_KEYS.
_RATE = "{file}: {column} must be {what}; it is not on line {lines}"
# Each table: (its value column, the Data cell that checks it, the row edited, its line,
# what each value must be).
RATE_TABLES = {
    "prem_persistency.csv": ("prem_persistency", "prem_persistency_last_year", 2, 4,
                             "a number, zero or more"),
    "lapse_table.csv": ("lapse_rate_ann", "lapse_last_year", 4, 6, "a number from 0 to 1"),
    "corridor_factors.csv": ("corridor_factor", "corridor_age_last", 29, 31,
                             "a number, zero or more"),
    "mort_table.csv": ("mort_rate", "mort_age_last", 29, 31, "a number from 0 to 1"),
    "coi_rates.csv": ("coi_rate_guar", "coi_rate_last_years", 9, 11,
                      "a number, zero or more"),
    "class_factor_table.csv": ("factor", "class_count", 3, 5, "a number, zero or more"),
    "surr_charge_table.csv": ("sc_per_1000_init", "surr_charge_count", 0, 2,
                              "a number, zero or more"),
    "subaccount_table.csv": ("fund_expense_ann", "subaccounts", 1, 3,
                             "a number, zero or more"),
    "scenario_table.csv": ("gross_return_mth", "scenario_last_mths", 1, 3, "a number"),
}
# The values outside a range, by table, each read on the row RATE_TABLES edits.
OUT_OF_RANGE = {"prem_persistency.csv": (-0.5,), "lapse_table.csv": (1.2, -0.05),
                "mort_table.csv": (1.01, -0.01), "coi_rates.csv": (-0.22,),
                "corridor_factors.csv": (-0.5,),
                "class_factor_table.csv": (-1.0,), "surr_charge_table.csv": (-18.0,),
                "subaccount_table.csv": (-0.0075,)}


def _rate_refusal(file, lines):
    """The message that refuses ``file``'s values on ``lines``."""
    column, _, _, _, what = RATE_TABLES[file]
    return _RATE.format(file=file, column=column, what=what, lines=lines)


_RUNOFF = ("surr_charge_table.csv: runoff_years must be a whole number of years, 1 or "
           "more; it is not on line [2]")
MALFORMED_RATES = [
    *[(f"{file}: {what.format(column)}", file, _write_at(column, row, value), check,
       _rate_refusal(file, f"[{line}]"))
      for file, (column, check, row, line, _) in RATE_TABLES.items()
      for what, value in (("a blank {}", float("nan")), ("{} written as text", "x"),
                          ("an infinite {}", float("inf")))],
    *[(f"{file}: a {RATE_TABLES[file][0]} of {value}", file,
       _write_at(RATE_TABLES[file][0], RATE_TABLES[file][2], value), RATE_TABLES[file][1],
       _rate_refusal(file, f"[{RATE_TABLES[file][3]}]"))
      for file, values in OUT_OF_RANGE.items() for value in values],
    ("mort_table.csv: a mort_rate no point reads", "mort_table.csv",
     _write_at("mort_rate", 0, float("nan")), "mort_age_last",
     _rate_refusal("mort_table.csv", "[2]")),
    ("mort_table.csv: two mort_rate lines", "mort_table.csv",
     _write_rows("mort_rate", (30, 33), "n/a"), "mort_age_last",
     _rate_refusal("mort_table.csv", "[32, 35]")),
    ("class_factor_table.csv: a factor no point reads", "class_factor_table.csv",
     _write_at("factor", 0, float("inf")), "class_count",
     _rate_refusal("class_factor_table.csv", "[2]")),
    ("corridor_factors.csv: a factor no point reads", "corridor_factors.csv",
     _write_at("corridor_factor", 0, float("nan")), "corridor_age_last",
     _rate_refusal("corridor_factors.csv", "[2]")),
    *[(f"surr_charge_table.csv: runoff_years {what}", "surr_charge_table.csv",
       _write_at("runoff_years", 0, value), "surr_charge_count", _RUNOFF)
      for what, value in (("blank", float("nan")), ("written as text", "x"),
                          ("infinite", float("inf")), ("of 7.5", 7.5), ("of 0", 0))],
]


def _table_refused(tmp_path, file, edit, check, message):
    """Data's ``check``, then a projection, refuse the copy whose ``file`` is ``edit``-ed.

    The Data cell is asked first, and with it the first-age cell an age table's reader
    also asks, and then ``net_cf(0)`` of the base ``Projection``'s default point, S's
    worked-example policy in force, with the behaviour module switched on before anything
    is computed, which reads every one of these tables: the lineup and the returns through
    its accounts; the COI scale through the month's deduction, and the corridor through
    the pricing path's death benefit, its month-0 corridor being pinned; the mortality
    table and the class factor through the month's deaths; the lapse table, the
    surrender-charge schedule and, through the funding ratio, the premium persistency
    scale through its premium and its lapses.  ``Data.model_point_table()`` reads the
    lineup first too, to name the columns it checks.
    """
    folder = temp_inputs(tmp_path, model_path(SEC), edits={file: edit})
    model = _read(folder, "tables", {"dyn_behavior_on": True})
    try:
        _refused_exactly(model.Data.cells[check], message)
        if check.endswith("_age_last"):
            _refused_exactly(model.Data.cells[check.replace("_last", "_first")], message)
        _refused_exactly(lambda: model.Projection.net_cf(0), message)
    finally:
        model.close()


@pytest.mark.parametrize("case, file, edit, check, message", MALFORMED_KEYS,
                         ids=[c[0] for c in MALFORMED_KEYS])
def test_an_assumption_table_with_a_malformed_key_is_refused(tmp_path, case, file, edit,
                                                             check, message):
    """The Data cell a reader takes its extent, count or lineup from refuses the table (T5).

    And so does the projection of the committed table's first point, in its first month
    (:func:`_table_refused`).  The reader asks for its extent before it reads a value, so a
    projection meets the check first, as a compiled model's must.  The age tables' first
    age is counted from their last, so it meets the same check.  The message is matched
    whole, so that each key it names, repeated or missing, is held, and nothing else.
    """
    _table_refused(tmp_path, file, edit, check, message)


@pytest.mark.parametrize("case, file, edit, check, message", MALFORMED_RATES,
                         ids=[c[0] for c in MALFORMED_RATES])
def test_an_assumption_table_with_a_value_that_is_not_a_number_is_refused(
        tmp_path, case, file, edit, check, message):
    """A value blank, text, infinite or out of range is refused, naming its lines (T5).

    By the Data cell that checks the table's keys, its classes, its schedules, its lineup
    or its months, and by the projection of the committed table's first point, in its first
    month (:func:`_table_refused`), a value no point reads included, since a table is
    checked whole.  So is a run-off that is not a whole number of years, 1 or more, by one
    rule: ``VUL_US_S`` truncates a fraction with ``int()`` and divides by zero at 0.  And so
    is a lapse or mortality rate outside 0 to 1, and a class factor, a guaranteed COI
    rate, a fund expense, a premium persistency factor or a surrender charge below 0, each
    by the one rule that refuses a blank in its column: past 1 a rate has no monthly rate
    but a complex one, and below 0 a rate, a factor or a charge projects negative deaths,
    lapses, premiums or charges, or a surrender charge that rises once its schedule has run
    off, every check passing.
    ``VUL_US_S`` reads a blank value as a missing one, and so would this model's capped
    mortality, ``min(q, 1.0)``, which written ``min(1.0, q)`` would read one as 1.0, every
    policy in force dying in that month without a word.
    """
    _table_refused(tmp_path, file, edit, check, message)


# The bounds of each range, which a table may hold, by file: (column, row, value).  A lapse
# rate of 0 in policy year 2 and of 1 in policy year 3, where S's point 1 is at t = 0; a
# mortality rate of 0 at the table's first age; and a class factor, the anchor cell's
# guaranteed COI rate in policy year 1, the bond subaccount's fund expense, the premium
# persistency factor of policy year 3, the schedule's initial surrender charge and the
# corridor factor at attained age 47, S's point 1's in policy year 3, at 0.
AT_BOUNDS = {"prem_persistency.csv": (("prem_persistency", 2, 0.0),),
             "corridor_factors.csv": (("corridor_factor", 29, 0.0),),
             "lapse_table.csv": (("lapse_rate_ann", 1, 0.0), ("lapse_rate_ann", 2, 1.0)),
             "mort_table.csv": (("mort_rate", 0, 0.0),),
             "class_factor_table.csv": (("factor", 0, 0.0),),
             "coi_rates.csv": (("coi_rate_guar", 0, 0.0),),
             "surr_charge_table.csv": (("sc_per_1000_init", 0, 0.0),),
             "subaccount_table.csv": (("fund_expense_ann", 1, 0.0),)}


def _written(cells):
    """An edit that writes each ``(column, row, value)`` of ``cells``."""
    def edit(table):
        for column, row, value in cells:
            table = _write_at(column, row, value)(table)
        return table
    return edit


def test_a_rate_or_factor_at_the_bound_of_its_range_is_read(tmp_path):
    """A rate of 0 or 1, and a factor, a fund expense or a charge of 0, are read (T5).

    The ranges ``Data`` holds the tables to are closed: a lapse or mortality rate from 0 to
    1, the shipped mortality table reaching 1.0 at attained age 119, and a class factor, a
    guaranteed COI rate, a fund expense, a premium persistency factor, a surrender charge
    or a corridor factor of 0 or more.  So a copy holding each bound (:data:`AT_BOUNDS`)
    reads, every extent and count as shipped, and S's point 1, in policy year 3 at
    ``t = 0``, projects its first month with the whole lapse rate of 1.0, a base
    persistency factor of 0 and no surrender charge, and its second with a corridor of 0,
    which leaves the death benefit at the face.
    """
    folder = temp_inputs(tmp_path, model_path(SEC),
                         edits={file: _written(cells) for file, cells in AT_BOUNDS.items()})
    model = _read(folder, "bounds_read")
    try:
        assert (model.Data.prem_persistency_last_year(), model.Data.lapse_last_year(),
                model.Data.mort_age_last(), model.Data.class_count(),
                model.Data.surr_charge_count()) == (6, 11, 121, 6, 1)
        assert model.Data.coi_schedules() == 1
        p = _row(model, "twin", 1, 0)
        assert p.fund_expense_ann(_sa(p, 2)) == 0.0
        assert (p.lapse_rate(0), p.lapse_rate_mth(0)) == (1.0, 1.0)
        assert (p.prem_persistency_base(0), p.surr_charge_rate(0)) == (0.0, 0.0)
        assert type(p.net_cf(0)) is float and math.isfinite(p.net_cf(0))
        assert (p.corridor_factor(1), p.db_pp(1)) == (0.0, p.sum_assured_at(1))
    finally:
        model.close()


# A text column VUL_US_S branches on or joins on, holding a value its formulas or tables do
# not know, on S point 2's twin, which pins nothing, so that month 0 asks the corridor its
# rule, with one column changed: an option, a test or a pattern no decode names, and a case
# or a whitespace variant of every value each decode and each join names, which S's
# comparisons and lookups, exact, do not know either.  The decodes read such a value as no
# known value, and the cell that branches on it raises VUL_US_S's own message; the joins
# refuse it, the class, the charged schedule and the scenario by the table, naming the
# point, and the COI scale's keys where a rate is read, as VUL_US_S's lookups raised.
# (case, column, value, message).
_NO_CLASS_2 = "class_factor_table.csv has no factor for the rate_class of point_id [2]"
_NO_SCHEDULE_2 = ("surr_charge_table.csv has no schedule for the surr_charge_id of "
                  "point_id [2], each of which has_surr_charge")
_NO_SCENARIO_2 = ("scenario_table.csv has no returns for every subaccount of the lineup on "
                  "the scenario_id of point_id [2]")
_NO_SCALE_2 = ("point_id 2: coi_rates.csv has no scale for the point's sex, rate_class and "
               "age_at_entry")
UNDECODABLE = [
    ("db_option C", "db_option", "C", "invalid db_option"),
    ("qual_test CVAT", "qual_test", "CVAT", "invalid qual_test"),
    ("premium_type FLEX", "premium_type", "FLEX", "invalid premium type"),
    *[(f"db_option {value!r}", "db_option", value, "invalid db_option")
      for value in ("a", " A", "b", "B ")],
    *[(f"qual_test {value!r}", "qual_test", value, "invalid qual_test")
      for value in ("gpt", "GPT ")],
    *[(f"premium_type {value!r}", "premium_type", value, "invalid premium type")
      for value in ("level", " LEVEL", "single", "SINGLE ")],
    *[(f"rate_class {value!r}", "rate_class", value, _NO_CLASS_2)
      for value in ("stdnt", "StdNT ")],
    *[(f"sex {value!r}", "sex", value, _NO_SCALE_2) for value in ("m", " M")],
    ("surr_charge_id 'vul14'", "surr_charge_id", "vul14", _NO_SCHEDULE_2),
    *[(f"scenario_id {value!r}", "scenario_id", value, _NO_SCENARIO_2)
      for value in ("we", " WE")],
]


@pytest.mark.parametrize("case, column, value, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_a_value_no_decode_knows_is_refused_as_in_vul_us_s(tmp_path, case, column, value,
                                                          message):
    """A value no decode or join knows is refused, by ``VUL_US_S``'s message or by name.

    The five decodes each compare the text with one value, exactly, as ``VUL_US_S``'s
    formulas do, so a value none of them names reads as no known one, a case or a
    whitespace variant of a value it names among them, and the cell that branches on them
    must raise as ``VUL_US_S``'s does, rather than take its last branch.  The joins match
    exactly too, as ``VUL_US_S``'s lookups do: a class, a charged schedule or a scenario
    written otherwise than its table writes it is refused, naming the point, and a sex so
    written leaves the point without a COI scale, refused where a rate is read.  A decode
    or a join that folded case or stripped space would project a point ``VUL_US_S``
    refuses.  The table reads, because the text columns are the product's to judge, and
    the point's first projection raises (:data:`UNDECODABLE`).
    """
    point = _label(_committed(), "twin", 2, 0)
    model = mx.read_model(_sec_inputs(tmp_path, _set(column, [point], value)(_committed())),
                          name=_name("undecodable"))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point).result_cf, message)
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued 25 months on.  It reads at the shipped
    120 months and at 25, the shortest horizon that admits it, where it also projects, its
    frame opening at the valuation date and its policies arriving at ``t = 25``, and it is
    refused at 24, by name.  At 0 the model takes no future new business, D4's fallback for
    a product that cannot support it, and the message says so.  A negative horizon is
    itself refused, and so is a negative ``Data.return_horizon_mth``, the return
    scenario's, by the scenario's check.  Each value is set on a model just read, before
    its table is.
    """
    future = _label(_committed(), "future", 3, -25)
    later = (f"model_point_table_sec.csv: duration_mth must be -24 or more, a policy "
             f"issued at most 24 months after the valuation date; it is not at point_id "
             f"[{future}]")
    no_future = (f"model_point_table_sec.csv: duration_mth must be 0 or more: this model "
                 f"takes no future new business; it is not at point_id [{future}]")
    negative = "future_horizon_mth must be 0 months or more, not -1"
    folder = _sec_inputs(tmp_path, _committed())
    for horizon, refusal in ((None, None), (25, None), (24, later), (0, no_future),
                             (-1, negative)):
        model = mx.read_model(folder, name=_name("horizon"))
        try:
            if horizon is None:
                assert model.Data.future_horizon_mth == 120
            else:
                model.Data.future_horizon_mth = horizon
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(_committed()), horizon
            else:
                _refused_exactly(model.Data.model_point_table, refusal)
            if horizon == 25:
                p = _point(model, future)
                assert len(p.result_cf()) == p.proj_len() == 949
                assert p.pols_new_biz(25) == p.policy_count()
        finally:
            model.close()
    model = mx.read_model(folder, name=_name("return_horizon"))
    try:
        assert model.Data.return_horizon_mth == 1585
        model.Data.return_horizon_mth = -1
        _refused_exactly(model.Data.scenario_count,
                         "return_horizon_mth must be 0 months or more, not -1")
    finally:
        model.close()


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


# The refusals of proj_len(), as (case, the policy month S's in-force point 4's twin is
# moved to): to the month the projection ends, the first at attained age 122, and a year
# past it.
PAST_COVER = [("at the end", 924), ("past the end", 936)]


@pytest.mark.parametrize("case, month", PAST_COVER, ids=[c[0] for c in PAST_COVER])
def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path, case, month):
    """A point at or past the end of the projection has no frame, and is refused by name.

    S's in-force point 4's twin is moved on to a policy month at or past ``omega_mth()``,
    the month the projection ends at attained age 122.  That is a rule of the product, not
    of the table: it needs ``omega_age``, a Projection Reference, so the table reads, and
    the point is refused where its frame is defined, on its first projection, rather than
    projecting nothing.  A loop over the block would meet the point only when it reached
    it, after projecting the points before it, so ``run_sec.py --block``, run beside the
    table, asks every point for its frame first: it fails naming the point, and prints
    nothing before.
    """
    moved = _label(_committed(), "twin", 4, 0)
    folder = _sec_inputs(tmp_path, _set("duration_mth", [moved], month)(_committed()))
    message = (f"point_id {moved}: duration_mth {month} is at or past the end of the "
               f"projection, policy month 924, attained age 122")
    model = mx.read_model(folder, name=_name("past"))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_exactly(_point(model, moved).proj_len, message)
        _refused(_point(model, moved).result_cf, message)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


# The key columns of every keyed table and of the lineup and the scenario, which the edges
# test writes as floats, 16.0 for 16, as a spreadsheet can save them; and the extents Data
# reads from them.
FLOAT_KEYS = {"prem_persistency.csv": ("policy_year",), "lapse_table.csv": ("policy_year",),
              "corridor_factors.csv": ("age",), "mort_table.csv": ("age",),
              "coi_rates.csv": ("age_at_entry", "policy_year"),
              "subaccount_table.csv": ("subaccount_id",),
              "scenario_table.csv": ("subaccount_id", "t"),
              "surr_charge_table.csv": ("runoff_years",)}
EXTENTS = ("prem_persistency_last_year", "lapse_last_year", "corridor_age_first",
           "corridor_age_last", "mort_age_first", "mort_age_last")


def _as_floats(columns):
    """An edit that writes the table's ``columns`` as floats."""
    def edit(table):
        return table.assign(**{column: table[column].astype(float) for column in columns})
    return edit


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and the state's edges are read.

    One copy of the committed table, edited at the edges a real extract reaches, is read
    beside a copy of every keyed table with its keys written as floats, 16.0 for 16, as a
    spreadsheet can save them (:data:`FLOAT_KEYS`), and again beside the tables as
    shipped, both with the behaviour module on, so that every table is read:

    * ``Data`` reads each key by value, so every extent is the committed table's, an int,
      the lineup's ids are ints that name ``alloc_1`` and ``sa_pp_init_1``, the scenario's
      last months and the COI scale's last years are the committed ones, and the twins of
      S's points 1, 3 and 4 and the row issued 25 months on, which between them read every
      table, project exactly what they project beside the tables as shipped;
    * ``126.0`` is a whole number of months and ``45.0`` of years, read back as the ints
      the clocks count in;
    * a premium load of 1, a share at its bound, is read as written, the load taking the
      whole premium and the accounts none of it;
    * a count of 0 is a point that projects zeros;
    * a pin of 0 is a pin, applied at ``t = 0``, as the shipped blank is none, and the
      corridor's alone leaves the COI rate the rule's, with every flow a number;
    * the collateral equal to the loan, as ``VUL_US_S`` takes it on its own points, the face
      in force equal to the face at issue, and an account at 0 in every subaccount and the
      fixed option are a policy in force, projected from the values given;
    * a point in its last covered month, 923, has a frame of one row;
    * a policy issued 120 months after the valuation date, the shipped
      ``future_horizon_mth``, is the last one the table admits, with a frame of 1,044
      months, 924 of cover after 120 before issue;
    * and the windows of policy months, each just outside where a state can be (§5.2, T5,
      precised at M10), on copies appended under ids of their own: S point 3's row at 12
      moved to a month in force, 1, holds an opening state, which the rule of a policy not
      yet in force refuses at 0, and its face in force, which the in-force face rules hold
      from 1; and the twin of S's point 3, issued at the valuation date, holds both pins,
      which the rule of a policy issued later refuses at -1, each applied at ``t = 0``, its
      issue month, as ``VUL_US_S`` applies a pin on its own new business, and the rule's
      rate from ``t = 1``.
    """
    committed = _committed()
    zero = _label(committed, "derived", 4, 768)
    whole = _label(committed, "derived", 4, 6)
    pinned = _label(committed, "twin", 2, 0)
    equal = _label(committed, "derived", 3, 12)
    empty = _label(committed, "derived", 3, 593)
    future = _label(committed, "future", 3, -25)
    probes = [_label(committed, "twin", p, 0) for p in (1, 3, 4)] + [future]
    a_month_in, pinned_new = 101, 102
    copies = {a_month_in: (equal, {"duration_mth": 1}),
              pinned_new: (_label(committed, "twin", 3, 0),
                           {"corridor_override_m1": 2.5, "coi_rate_override_m1": 0.04})}

    def edit(table):
        table = pd.concat([table, *(
            table.loc[[row]].assign(**changes, row_kind="copy").set_axis([label])
            for label, (row, changes) in copies.items())]).rename_axis("point_id")
        table = _set("policy_count", [zero], 0.0)(table)
        table = _set("corridor_override_m1", [pinned], 0.0)(table)
        table = _set("la_pp_init", [whole], table.at[whole, "loan_bal_init"])(table)
        table = _set("load_prem_rate", [whole], 1.0)(table)
        table = _set("sum_assured_init", [equal], table.at[equal, "sum_assured"])(table)
        for column in ("sa_pp_init_1", "sa_pp_init_2"):
            table = _set(column, [empty], 0.0)(table)
        table = _moved(equal, 923)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float),
                             age_at_entry=table["age_at_entry"].astype(float))
        return _set("duration_mth", [future], -120.0)(table)

    edited = edit(committed)
    floats = _sec_inputs(tmp_path / "floats", edited, edits={
        file: _as_floats(columns) for file, columns in FLOAT_KEYS.items()})
    for file, columns in FLOAT_KEYS.items():
        written = pd.read_csv(floats.parent / file)
        assert all(written[c].dtype == float for c in columns), file
    shipped = _sec_inputs(tmp_path / "shipped", edited)
    on = {"dyn_behavior_on": True}
    model = _read(floats, "edges", on)
    plain = _read(shipped, "edges_shipped", on)
    try:
        for cell in EXTENTS:
            value = model.Data.cells[cell]()
            assert (type(value), value) == (int, sec_model.Data.cells[cell]()), cell
        for cell in ("coi_rate_last_years", "scenario_last_mths"):
            got, want = model.Data.cells[cell](), sec_model.Data.cells[cell]()
            assert np.array_equal(got, want) and got.dtype == "int64", cell
        lineup = model.Data.subaccounts()
        assert list(lineup) == [1, 2] and lineup.dtype == "int64"
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float and read["age_at_entry"].dtype == float
        for label in probes:
            mine, base = _point(model, label), _point(plain, label)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (label, report)
        p = _point(model, zero)
        df = p.result_cf()
        assert len(df) == 36 and (df == 0.0).all().all()
        p = _point(model, whole)
        assert p.duration_mth(0) == 126 and type(p.duration_mth(0)) is int
        assert p.age_at_entry() == 45 and type(p.age_at_entry()) is int
        assert p.la_pp_init() == p.loan_bal_init() == p.la_pp_at(0, _code(p, "BEF_PREM"))
        assert p.load_prem_rate() == 1.0 and p.prem_to_av_pp(0) == 0.0 < p.premium_pp(0)
        p = _point(model, pinned)
        assert (p.has_corridor_override_m1(), p.corridor_factor(0)) == (True, 0.0)
        assert p.corridor_factor(1) == p.corridor_factor_at(p.age(1)) > 0.0
        assert not p.has_coi_rate_override_m1()
        assert p.coi_rate(0) == p.coi_rate_at(p.policy_year(0)) > 0.0
        assert all(math.isfinite(v) for v in p.result_cf().to_numpy().ravel())
        p = _point(model, equal)
        assert (p.proj_len(), p.sum_assured_init()) == (1, p.sum_assured())
        assert p.db_pp(0) == p.sum_assured() + p.av_pp_at(0, _code(p, "BEF_FEE"))
        p = _point(model, empty)
        assert p.av_pp_init() == 0.0 and p.is_shortfall(0)
        assert all(math.isfinite(v) for v in p.result_cf().to_numpy().ravel())
        p = _point(model, future)
        assert (p.t_entry(), p.proj_len(), p.pols_new_biz(120)) == (120, 1044, 1.0)
        p = _point(model, a_month_in)
        assert (p.duration_mth(0), p.t_entry(), p.proj_len()) == (1, 0, 923)
        for column, (cell, args) in STATE.items():
            got = p.cells[cell](*_state_args(p, cell, args))
            assert got == committed.at[equal, column], column
        assert 0.0 < p.sum_assured_init() <= p.sum_assured()
        assert math.isfinite(p.net_cf(0))
        p = _point(model, pinned_new)
        assert (p.duration_mth(0), p.pols_new_biz(0)) == (0, p.policy_count())
        assert (p.has_corridor_override_m1(), p.corridor_factor(0)) == (True, 2.5)
        assert (p.has_coi_rate_override_m1(), p.coi_rate(0)) == (True, 0.04)
        assert p.corridor_factor(1) == p.corridor_factor_at(p.age(1)) != 2.5
        assert p.coi_rate(1) == p.coi_rate_at(p.policy_year(1)) != 0.04
        assert math.isfinite(p.net_cf(0))
    finally:
        plain.close()
        model.close()


def test_every_state_s_reaches_where_its_bounds_bind_is_accepted_in_force(tmp_path):
    """Under :data:`BOUND_REFS` too, every state S reaches is accepted, but one.

    At the guaranteed COI scale and the declared rate at its floor, with the behaviour
    module on, the References under which two of ``VUL_US_S``'s bounds bind, every one of
    S's four points runs into a permanent shortfall, S's point 4 after its loan has passed
    its cash value, so the states S reaches differ again, and the every-state test runs
    here too (§5.2, T5, precised at M9): on S read afresh with them set before it computes
    anything, each point restated in force at the edges of its windows, or at every month
    with ``USLIB_SEC_FULL=1``, is read by ``Data`` and has a frame
    (:func:`_refused_in_force`), but an account below 0, on every point, which a table
    holding one is refused for, by name.  It runs before the committed S is first read, so
    the two never sit in memory together.
    """
    s = _read(model_path(TWIN), "s_every_bounds", BOUND_REFS)
    try:
        kept, below = _states_s_reaches(s)
        assert {point for point, _ in below} == {1, 2, 3, 4}, below[:3]
        assert {point for point, _ in kept} == {1, 2, 3, 4}
        refused = _refused_in_force(s, kept, tmp_path / "every", BOUND_REFS)
        assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
        _refused_by_name(s, below[0], tmp_path / "below", BOUND_REFS)
    finally:
        s.close()


def test_every_state_s_reaches_as_shipped_is_accepted_in_force(s_model, tmp_path):
    """At S's shipped References and inputs too, every state S reaches is accepted, but one.

    The states ``VUL_US_S`` reaches differ from the splice's here, with the behaviour module
    off, charges to the end of the table and S's own scenarios, so the every-state test runs
    here too (§5.2, T5, precised at M9): each of S's four points, swept, restated in force
    at the edges of its windows, or with ``USLIB_SEC_FULL=1`` at every month of its frame
    (:func:`_every_state_months`), is read by ``Data`` and has a frame
    (:func:`_refused_in_force`), but an account below 0, which S's point 3 reaches once its
    permanent shortfall begins, at policy month 594, the month after the committed row at
    593, and which a table holding it is refused for, by name.
    """
    kept, below = _states_s_reaches(s_model)
    assert {point for point, _ in below} == {3} and min(below)[1] == 594, below[:3]
    assert {point for point, _ in kept} == {1, 2, 3, 4}
    refused = _refused_in_force(s_model, kept, tmp_path / "every", {})
    assert not refused, f"{len(refused)} refused, first: {refused[:5]}"
    _refused_by_name(s_model, below[0], tmp_path / "below", {})


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what VUL_US_S and its table generate today.

    Every row and column, the text cells and the opening-state columns included: an edit
    to an S row the table copies or derives from, or to an S formula a row's state is read
    from, fails here until ``python tools/gen_sec_points.py VUL_US_SEC`` regenerates it, in
    the same commit.  Text and integers compare exactly, and a float by its value, to
    1e-12, because the text the writer picks for a computed float depends on the platform's
    parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


def test_the_spec_restates_the_lineup_and_leaves_future_rows_unpinned(sec_model, s_model):
    """The spec's state names each subaccount the lineup has, and a future row pins nothing.

    ``sec_support._VUL_STATE`` reads one ``sa_pp_init_<i>`` column for each subaccount of
    the shipped lineup, 1 and 2, which ``subaccount_table.csv`` gives: a lineup with another
    id would leave its subaccount's opening value unread on every restated row, so its ids
    and the spec's columns must agree.  And a future row copies its twin's columns, the
    first-month pins among them, which ``Data`` refuses on a point issued after the
    valuation date, where they would never apply: so every S point the spec issues later
    has both pins blank, and a pinned new-business point fails here, by name, rather than
    in ``Data``.
    """
    ids = sec_model.Data.subaccounts().tolist()
    lineup = {f"sa_pp_init_{i}" for i in ids}
    named = {column for column in SPEC.state if column.startswith("sa_pp_init_")}
    assert named == lineup, (
        f"sec_support._VUL_STATE reads {sorted(named)}, the lineup has {sorted(lineup)}")
    assert _VUL_LINEUP == {i: k for k, i in enumerate(ids)}, (
        f"sec_support._VUL_LINEUP is {_VUL_LINEUP}, the lineup's ids are {ids}")
    s_table = s_model.Data.model_point_table()
    pinned = [(p, pin) for p, _ in SPEC.future for pin in PINS
              if not pd.isna(s_table.at[p, pin])]
    assert SPEC.future and not pinned, (
        f"S points the spec issues later with a pin: {pinned}")


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On the twin of S's new business the two coincide, its policies enter as new business
    at ``t = 0``, and its frame is 924 months, the projection's end at attained age 122.
    S's point 1 is in policy year 3 at attained age 47 at ``t = 0``, with 900 months left,
    and its first-month pins apply in the valuation month alone, the worked example's: the
    corridor factor is the pinned 2.15 at ``t = 0`` and the rule's 2.03 at 47 from
    ``t = 1``, and the current COI rate the pinned $0.04 at ``t = 0`` and the scale's from
    ``t = 1``.  S's point 4 is in policy year 11 at 55, past its loan's first nine years,
    and opens its collateral and its debt equal, as S does, each growing at its own rate
    from there.  The point valued six months after it opens each from its own column,
    8,039.90 and 8,041.89.  The point valued at 593 is in shortfall from ``t = 0``, its
    first shortfall month 0 on the valuation clock.  The point valued at 888, the first
    month at attained age 119, where the table's rate reaches 1, loses every life in
    month 0.  The point issued 25 months on has nothing in force and nothing to do before
    ``t = 25``, and before issue its policy years are -2, -1 and 0, which the guards must
    answer for.

    ``pols_if_at``'s ``"BEF_NB"`` counts the policies before the month's new business, so
    in the issue month it is 0 where ``pols_if`` holds the issued count; ``"BEF_MAT"``
    keeps ``VUL_US_S``'s meaning, that count, since nothing matures; and a timing the
    model does not know is refused by every cell that takes one, rather than answered with
    another value.
    """
    twin = _row(sec_model, "twin", 3, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 923)] == [0, 1, 923]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.omega_mth() == twin.proj_len() == 924
    assert twin.is_active(923) and not twin.is_active(924)
    assert twin.pols_if_at(0, _code(twin, "BEF_MAT")) == twin.pols_if(0) == 1.0
    assert twin.pols_if_at(0, _code(twin, "BEF_NB")) == 0.0
    anchor = _row(sec_model, "twin", 1, 0)
    assert (anchor.duration_mth(0), anchor.policy_year(0), anchor.age(0),
            anchor.proj_len()) == (24, 3, 47, 900)
    assert (anchor.corridor_factor(0), anchor.corridor_factor(1)) == (2.15, 2.03)
    assert anchor.corridor_factor(1) == anchor.corridor_factor_at(47)
    assert anchor.coi_rate(0) == min(0.04, anchor.coi_rate_guar(0), anchor.coi_rate_cap)
    assert anchor.coi_rate(0) == 0.04 and anchor.coi_rate(1) == anchor.coi_rate_at(3)
    lent = _row(sec_model, "twin", 4, 0)
    bef_prem = _code(lent, "BEF_PREM")
    assert (lent.duration_mth(0), lent.policy_year(0), lent.age(0), lent.proj_len()) == (
        120, 11, 55, 804)
    assert lent.la_pp_at(0, bef_prem) == lent.loan_bal_pp_at(0, bef_prem) == 8000.0
    assert lent.la_pp_at(1, bef_prem) == 8000.0 * (1 + lent.loan_cr_rate_mth(0))
    assert lent.loan_bal_pp_at(1, bef_prem) == 8000.0 * (1 + lent.loan_rate_mth(0))
    assert lent.loan_rate_ann(0) == lent.loan_rate_ann_pref < lent.loan_rate_ann_std
    moved = _row(sec_model, "derived", 4, 6)
    assert (moved.duration_mth(0), moved.policy_year(0), moved.age(0)) == (126, 11, 55)
    assert moved.la_pp_at(0, bef_prem) == moved.la_pp_init() == pytest.approx(
        8039.90, abs=0.005)
    assert moved.loan_bal_pp_at(0, bef_prem) == moved.loan_bal_init() == pytest.approx(
        8041.89, abs=0.005)
    short = _row(sec_model, "derived", 3, 593)
    assert short.is_shortfall(0) and short.first_shortfall_month() == 0
    last = _row(sec_model, "derived", 4, 768)
    assert (last.proj_len(), last.age(0), last.mort_rate(0)) == (36, 119, 1.0)
    assert last.pols_if(0) > 0.0 and last.pols_if(1) == 0.0
    fut = _row(sec_model, "future", 3, -25)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-25, 25, 949)
    assert [fut.policy_year(t) for t in range(26)] == [-2] + [-1] * 12 + [0] * 12 + [1]
    assert not any(fut.is_active(t) for t in range(25)) and fut.is_active(25)
    assert (fut.pols_if(24), fut.pols_new_biz(25), fut.pols_if(25), fut.premium_pp(25)) == (
        0.0, 1.0, 1.0, 500.0)
    for name, rest in (("pols_if_at", ()), ("av_pp_at", ()), ("sa_pp_at", (1,)),
                       ("fa_pp_at", ()), ("la_pp_at", ()), ("loan_bal_pp_at", ())):
        _refused(lambda: twin.cells[name](0, *rest, "BEF_LUNCH"), "invalid timing")


def test_s_in_force_points_are_their_twins_from_the_valuation_date(sec_model, s_model):
    """At the shipped assumptions S's in-force points are S's own projections, in force.

    ``VUL_US_S`` opens its points 1, 2 and 4 at its own ``t = 0``, 24 and 120 months in,
    with the subaccounts, the fixed option and the debt of their own columns, and with the
    two values it assumes: the loan account equal to the debt, 8,000 on point 4, and the
    face at issue in force.  Their twins carry those as their opening state, point 1 its
    first-month pins too and point 2 none, and from the valuation date on each is S's
    point in every cell of S's and every report, nothing left out, to 1e-9 relative with
    no absolute floor (:func:`_continues_s`).  So every golden of ``test_variable_ul_us.py``
    on S's point 1, the worked example's month at ``t = 0`` among them, holds on its twin
    with no number restated.
    """
    opening = {1: (30000.0, 20000.0, 0.0, 0.0), 2: (30000.0, 20000.0, 0.0, 0.0),
               4: (40000.0, 25000.0, 10000.0, 8000.0)}
    for point, (sa1, sa2, fa, loan) in opening.items():
        p, s = _row(sec_model, "twin", point, 0), _point(s_model, point)
        assert (p.sa_pp_init(_sa(p, 1)), p.sa_pp_init(_sa(p, 2)), p.fa_pp_init(),
                p.loan_bal_init()) == (sa1, sa2, fa, loan), point
        assert (s.sa_pp_init(1), s.sa_pp_init(2), s.fa_pp_init(), s.loan_bal_init()) == (
            sa1, sa2, fa, loan), point
        assert p.la_pp_init() == p.loan_bal_init(), point
        assert p.sum_assured_init() == p.sum_assured() == 500000.0, point
        assert p.av_pp_init() == s.av_pp_init(), point
        assert _continues_s(s, p, 0) == [], point
    p = _row(sec_model, "twin", 1, 0)
    assert (p.has_corridor_override_m1(), p.corridor_override_m1(),
            p.has_coi_rate_override_m1(), p.coi_rate_override_m1()) == (True, 2.15, True,
                                                                        0.04)
    p = _row(sec_model, "twin", 2, 0)
    assert (p.has_corridor_override_m1(), p.has_coi_rate_override_m1()) == (False, False)


def test_every_committed_row_continues_its_s_point(sec_model, s_model):
    """Each derived and future row of the committed table is its S point from its month on.

    T6 holds the committed table to what the generator makes of S, each float to 1e-12
    absolute and relative, which pins a count as small as point 8's, 4.0e-10, only to
    about a quarter of a percent.  So each derived and future row is projected too, at the
    shipped assumptions, and its four reports compared with its S point's from the row's
    ``source_mth`` on, frame by frame, to 1e-9 relative with no absolute floor: a count or
    an opening value gone stale moves the flows by far more than that.  The first default
    and shortfall months are the first S finds at or after the row's month, less it
    (:func:`_first_month`): the point restated at 593, in the month its shortfall begins,
    is in shortfall from ``t = 0``.  S's in-force points, the twins, are compared cell by
    cell by the test before this one.
    """
    table = sec_model.Data.model_point_table()
    s_points = {policy: point for point, policy
                in s_model.Data.model_point_table()["policy_id"].items()}
    rows = table.index[table["row_kind"] != "twin"].tolist()
    assert rows, "the committed table has no derived or future row"
    for point_id in rows:
        month = int(table.at[point_id, "source_mth"])
        theirs = _point(s_model, s_points[table.at[point_id, "source_policy_id"]])
        mine = _point(sec_model, point_id)
        found = []
        for report in REPORTS:
            found += frame_mismatches(theirs.cells[report](), mine.cells[report](),
                                      t_offset=month, atol=0.0)
        for cell, flag in FIRST_MONTHS.items():
            if mine.cells[cell]() != _first_month(theirs, flag, month):
                found.append(f"{cell}: {mine.cells[cell]()}, S's from its month "
                             f"{_first_month(theirs, flag, month)}")
        assert found == [], (point_id, found)
    assert _row(sec_model, "derived", 3, 593).first_shortfall_month() == 0


def test_every_guarded_cell_holds_its_outside_cover_value(sec_model):
    """Outside cover each monthly cell holds its value, and no table is read past cover.

    The sets of the guard (:data:`GUARD_SETS`) are disjoint and together hold every cell of
    the model whose first parameter is ``t``, so a new cell must be placed in one before
    this test passes.  Then on every committed point, once swept, at the shipped
    References, in every month before issue and at ``t = proj_len()``, the month after the
    frame, which the roll-forwards read, every one of them holds its value
    (:func:`_outside_cover_faults`); the splice's rows are held to the same in the splice's
    class, where the survivors carried there are not zero and the behaviour module is on.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too.  They are held here because they are what the
    docstrings promise a caller, and because Phase 2 needs them: its full sweep calls every
    cell of ``t`` at every month from 0 to ``proj_len()``, and a table read at a policy year
    or an age the policy does not have would wrap round in a compiled model rather than fail
    (USLIB-SEC-PLAN.md F4, R1).
    """
    sets = list(GUARD_SETS.values())
    union = set().union(*sets)
    assert sum(len(cells) for cells in sets) == len(union), "the guard's sets overlap"
    monthly = _monthly_cells(_row(sec_model, "twin", 1, 0))
    assert union == monthly, (f"unplaced: {sorted(monthly - union)}; "
                              f"not cells: {sorted(union - monthly)}")
    faults = []
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        faults += _outside_cover_faults(projection(sec_model, key), f"point {point_id}")
    assert not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_collateral_and_each_subaccount_open_from_their_own_columns(tmp_path):
    """The loan account, the subaccounts and the fixed option open from their own values.

    The committed row of S's point 4 six months on carries 8,039.90 of collateral against a
    debt of 8,041.89, S's own values entering its month 6, and 41,701.23, 26,052.83 and
    10,454.95 in its two subaccounts and its fixed option.  In one copy at the shipped
    References it is read beside two rows that open as a model might have assumed:

    * the collateral equal to the debt, as ``VUL_US_S`` takes it at the start of its own
      frame: the account value entering month 0 is then 86,250.89 against 86,248.90, 1.99
      high, a month's credit on it 0.00165 high, and ``net_cf`` 0.00496 low in month 0 and
      0.00487 in month 11, every month off by the collateral's growth;
    * each subaccount and the fixed option at its premium allocation, 0.5, 0.3 and 0.2, of
      the unloaned value, 39,104.50, 23,462.70 and 15,641.80: the account value entering
      month 0 is the same, but the subaccounts' returns and the fixed rate fall on the
      wrong amounts, so it closes month 0 at 86,781.31 against 86,797.44, 16.12 low, and
      month 11 196.05 low, and ``net_cf`` is 0.040 high in month 0 and 0.473 in month 11.

    Every row passes its three checks: each projection is consistent with itself, and only
    the opening value says which is the policy's.  T2 holds the same on every restated row.
    """
    committed = _committed()
    label = _label(committed, "derived", 4, 6)
    row = committed.loc[[label]]
    unloaned = row["sa_pp_init_1"] + row["sa_pp_init_2"] + row["fa_pp_init"]
    restart = row.assign(la_pp_init=row["loan_bal_init"]).set_axis(
        pd.Index([1001], name="point_id"))
    allocated = row.assign(sa_pp_init_1=row["alloc_1"] * unloaned,
                           sa_pp_init_2=row["alloc_2"] * unloaned,
                           fa_pp_init=row["alloc_fixed"] * unloaned).set_axis(
        pd.Index([1002], name="point_id"))
    model = _read(_sec_inputs(tmp_path, pd.concat([row, restart, allocated])), "opened")
    try:
        p, r, a = (_point(model, i) for i in (label, 1001, 1002))
        bef_prem = _code(p, "BEF_PREM")
        assert (p.la_pp_init(), p.loan_bal_init()) == pytest.approx((8039.90, 8041.89),
                                                                    abs=0.005)
        assert (p.sa_pp_init(_sa(p, 1)), p.sa_pp_init(_sa(p, 2)),
                p.fa_pp_init()) == pytest.approx((41701.23, 26052.83, 10454.95), abs=0.005)
        assert (a.sa_pp_init(_sa(a, 1)), a.sa_pp_init(_sa(a, 2)),
                a.fa_pp_init()) == pytest.approx((39104.50, 23462.70, 15641.80), abs=0.005)
        assert (p.av_pp_at(0, bef_prem), r.av_pp_at(0, bef_prem)) == pytest.approx(
            (86248.90, 86250.89), abs=0.005)
        assert r.inv_income_pp(0) - p.inv_income_pp(0) == pytest.approx(0.00165, abs=5e-6)
        assert [r.net_cf(t) - p.net_cf(t) for t in (0, 11)] == pytest.approx(
            [-0.00496, -0.00487], abs=5e-6)
        assert a.av_pp_at(0, bef_prem) == pytest.approx(p.av_pp_at(0, bef_prem),
                                                        rel=1e-12)
        assert (p.av_pp(0), a.av_pp(0)) == pytest.approx((86797.44, 86781.31), abs=0.005)
        assert p.av_pp(11) - a.av_pp(11) == pytest.approx(196.05, abs=0.005)
        assert [a.net_cf(t) - p.net_cf(t) for t in (0, 11)] == pytest.approx(
            [0.040, 0.473], abs=5e-4)
        for x in (p, r, a):
            assert x.check_av_roll_fwd() and x.check_margin() and x.check_net_view()
    finally:
        model.close()


def test_a_restated_row_reads_the_return_scenario_on_the_valuation_clock(s_model,
                                                                         tmp_path):
    """A row restated at S month 12 reads the scenario from the valuation date (D7).

    The return scenario is a path of the economy from the valuation date, one for every
    point of a block, so a point in force reads its month ``t`` at ``t``, whatever its
    duration: ``VUL_US_S`` reads it at its own projection month, which on its own points
    is the same month.  S's point 1 restated at its month 12, once on ``WE`` as shipped and
    once on a copy re-based to month 12 (:func:`_rebase`), as T2 reads every row:

    * on ``WE`` as shipped, month 0 reads the worked example's month, +1.00% on the equity
      subaccount, where S read the level 0.4868% at its month 12, so the subaccount closes
      month 0 at 34,396.04 against S's 34,221.25, 174.79 high, the account value 46.71
      low, and ``net_cf`` 0.152 high in month 0 and 0.129 in month 100;
    * on the re-based copy the row is S's from month 12 on, in every report and every cell
      of S's, as T2 holds every restated row.
    """
    spec = dataclasses.replace(SPEC, derived=((1, 12),), future=())
    table, _ = build_sec_table(spec, s_model)
    row = table[table["row_kind"] == "derived"]
    scenarios = pd.read_csv(model_path(TWIN).parent / "scenario_table.csv")
    rebased, with_copy = _rebase(row, scenarios)
    s = _point(s_model, 1)
    for tag, rows, edits in (("as shipped", row, None),
                             ("re-based", rebased, {"scenario_table.csv": with_copy})):
        model = _read(_sec_inputs(tmp_path / tag.replace(" ", "_"), rows, edits), "scen")
        try:
            p = _point(model, int(rows["point_id"].iloc[0]))
            if tag == "as shipped":
                assert (p.gross_return_mth(0, _sa(p, 1)), s.gross_return_mth(12, 1)) == (
                    0.01, 0.0048675506)
                assert (p.sa_pp(0, _sa(p, 1)), s.sa_pp(12, 1)) == pytest.approx(
                    (34396.04, 34221.25), abs=0.005)
                assert p.av_pp(0) - s.av_pp(12) == pytest.approx(-46.71, abs=0.005)
                assert [p.net_cf(t) - s.net_cf(t + 12) for t in (0, 100)] == (
                    pytest.approx([0.152, 0.129], abs=5e-4))
            else:
                assert p.scenario_id() == "WE_m12"
                for report in REPORTS:
                    assert frame_mismatches(s.cells[report](), p.cells[report](),
                                            t_offset=12, atol=0.0) == [], report
                assert _twin(s, p, t_offset=12, exempt=SPLICE_EXEMPT, atol=0.0) == []
        finally:
            model.close()


def test_expense_inflation_runs_on_the_valuation_clock(tmp_path):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    ``VUL_US_S`` ships no inflation, so both models are read with it at 2.5% before
    anything is computed.  The factor at ``t`` is then ``1.025^(t // 12)`` on every point,
    whatever its duration: ``VUL_US_S``'s step by policy year moved onto ``t``, so every
    point of a block steps on the valuation anniversaries.  So S's point 1, valued on its
    second anniversary, pays S's expenses deflated by ``1.025^2``, the inflation S had
    applied since issue, in every month, and S's point 4, on its tenth, by ``1.025^10``.
    The point valued six months after S's point 4 pays S's month ``6 + t`` deflated by
    ``1.025^10`` for ``t = 0 .. 5``, by ``1.025^11`` for ``t = 6 .. 11``, where S has
    stepped at the policy anniversary and this model has not, and by ``1.025^10`` again at
    ``t = 12``, where this model steps.  The point issued 25 months on pays S's month-``s``
    expenses inflated by the valuation years that have passed before its policy years,
    ``1.025^((25 + s) // 12 - s // 12)``.  This is the only test but the acquisition test
    that sees inflation run on its clock: the splice leaves it at 0, and on a point issued
    at ``t = 0`` the clocks agree.
    """
    refs = {"inflation_rate": INFLATION}
    sec = _read(model_path(SEC), "inflated", refs)
    s = _read(model_path(TWIN), "s_inflated", refs)
    try:
        for key in point_keys(sec):
            p = projection(sec, key)
            assert all(p.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
                       for t in range(p.proj_len())), key
        for point, years in ((1, 2), (4, 10)):
            p, sp = _row(sec, "twin", point, 0), _point(s, point)
            for t in range(p.proj_len()):
                assert p.expenses(t) == pytest.approx(
                    sp.expenses(t) / (1 + INFLATION) ** years, rel=1e-12), (point, t)
        p, sp = _row(sec, "derived", 4, 6), _point(s, 4)
        for t, years in [*((t, 10) for t in range(6)), *((t, 11) for t in range(6, 12)),
                         (12, 10)]:
            assert sp.expenses(6 + t) == pytest.approx(
                p.expenses(t) * (1 + INFLATION) ** years, rel=1e-12), t
        p, sp = _row(sec, "future", 3, -25), _point(s, 3)
        for s_t in range(sp.proj_len()):
            steps = (25 + s_t) // 12 - s_t // 12
            assert p.expenses(25 + s_t) == pytest.approx(
                sp.expenses(s_t) * (1 + INFLATION) ** steps, rel=1e-12), s_t
    finally:
        s.close()
        sec.close()


# The last month of each subaccount's rising path: a scenario's subaccounts may end apart,
# and each repeats its own last month past it.
RISING_LAST = {1: 240, 2: 180}


def _rising_returns(_):
    """Return scenarios that rise a little every month, a path of their own per subaccount.

    ``WE`` from 0.20% and 0.10% a month on the two subaccounts and ``LEVEL6`` from 0.25%
    and 0.15%, rising 0.001% and 0.002% a month, so that a return read in another month
    than its own changes a number, on either scenario; the equity paths run to month 240
    and the bond paths to month 180 (:data:`RISING_LAST`), so that an extent read for the
    wrong subaccount changes one too.
    """
    rows = []
    for scenario, lift in (("WE", 0.0), ("LEVEL6", 0.0005)):
        for i, (base, step) in ((1, (0.002, 0.00001)), (2, (0.001, 0.00002))):
            for t in range(RISING_LAST[i] + 1):
                rows.append((scenario, i, t, round(base + lift + step * t, 10),
                             "rising for a test"))
    return pd.DataFrame(rows, columns=["scenario_id", "subaccount_id", "t",
                                       "gross_return_mth", "provenance"])


def _rising_credited_rate(t):
    """The declared rate, rising a basis point a month from the valuation date."""
    return crediting_rate_curr + 0.0001 * t                          # noqa: F821


# The points the clock tests read: S's points 1 and 4 in force at 24 and 120, the point
# valued six months after point 4 and the point issued 25 months on.
CLOCK_POINTS = (("twin", 1, 0), ("twin", 4, 0), ("derived", 4, 6), ("future", 3, -25))


def test_fund_returns_and_the_declared_rate_run_on_the_valuation_clock(tmp_path):
    """The returns and the declared rate are paths on ``t``; the pricing path is off it.

    Fund returns, through a copy of ``scenario_table.csv`` whose paths rise every month
    (:func:`_rising_returns`), both models at the shipped References, which needs no
    formula override, so it runs unchanged compiled (K7): at ``t`` = 0, 1 and 12 every
    point of :data:`CLOCK_POINTS` reads its scenario's month ``t``, whatever its duration,
    and each subaccount's path past its own last month repeats that month, 240 on the
    equity subaccount and 180 on the bond one.
    The account value entering each month, ``av_pp_at(t, "BEF_PREM")``, which each part
    forms from the previous month's close itself, is that close, ``av_pp(t - 1)``, exactly,
    from ``t_entry() + 1`` on, so month ``t - 1`` is grown at its own return; the three
    checks hold; and ``VUL_US_S``, given the same paths, which on its own points are the
    same months, projects what the twins of its points 1, 3 and 4 project, in every report
    and every cell of S's (:func:`_continues_s`).

    The declared rate, by a formula override in models just read with the behaviour module
    on, so modelx's alone: the rate rising a basis point a month from the valuation date,
    ``crediting_rate_ann(t)`` and the fixed option's monthly rate are one number at each
    ``t`` for every point, the rate's at ``t``; on S's point 4 and the point six months on,
    the fixed option entering each month is the previous month's close, exactly.  And the
    pricing path does not move: it is a projection made at issue, credited at the declared
    rate's level, ``pricing_fixed_return_mth()``, so on S's point 4 the fixed option's path
    and the account value's are the unmoved model's at policy months 1, 120 and 923, where
    ``VUL_US_S``'s ``fa_pricing_pp(m)``, which reads the projection's rate at the policy
    month ``m`` (R1a), moves with the path.
    """
    folder = temp_inputs(tmp_path / "sec", model_path(SEC),
                         edits={"scenario_table.csv": _rising_returns})
    s_folder = temp_inputs(tmp_path / "s", model_path(TWIN),
                           edits={"scenario_table.csv": _rising_returns})
    paths = _rising_returns(None).set_index(["scenario_id", "subaccount_id", "t"])
    sec, s = _read(folder, "returns"), _read(s_folder, "s_returns")
    try:
        for case in CLOCK_POINTS:
            p = _row(sec, *case)
            for t in (0, 1, 12):
                for i in (1, 2):
                    want = paths.at[(p.scenario_id(), i, t), "gross_return_mth"]
                    assert p.gross_return_mth(t, _sa(p, i)) == want, (case, t, i)
            for i, last in RISING_LAST.items():
                assert p.scenario_last_mth(_sa(p, i)) == last, (case, i)
                want = paths.at[(p.scenario_id(), i, last), "gross_return_mth"]
                assert p.gross_return_mth(300, _sa(p, i)) == want, (case, i)
            bef_prem = _code(p, "BEF_PREM")
            apart = [t for t in range(p.t_entry() + 1, p.proj_len())
                     if p.av_pp_at(t, bef_prem) != p.av_pp(t - 1)]
            assert not apart, (case, apart[:5])
            assert p.check_av_roll_fwd() and p.check_margin() and p.check_net_view(), case
        for point in (1, 3, 4):
            sp = _point(s, point)
            _sweep_s(sp)
            arg_map = _issued_later if point in NEW_BUSINESS else None
            assert _continues_s(sp, _row(sec, "twin", point, 0), 0, arg_map) == [], point
    finally:
        s.close()
        sec.close()
    on = {"dyn_behavior_on": True}
    models = {}
    try:
        for tag, name in (("sec", SEC), ("s", TWIN)):
            for moved in (False, True):
                model = _read(model_path(name), f"{tag}_rates", on)
                if moved:
                    model.Projection.cells["crediting_rate_ann"].formula = (
                        _rising_credited_rate)
                models[tag, moved] = model
        rising = models["sec", True]
        ps = [_row(rising, *case) for case in CLOCK_POINTS]
        for t in (0, 1, 12):
            rate = 0.01 + 0.0001 * t
            for cell, value in (("crediting_rate_ann", rate),
                                ("fixed_return_mth", (1 + rate) ** (1 / 12) - 1)):
                got = [p.cells[cell](t) for p in ps]
                assert got == pytest.approx([value] * len(ps), rel=1e-12), (cell, t)
        for case in CLOCK_POINTS[1:3]:
            p = _row(rising, *case)
            bef_prem = _code(p, "BEF_PREM")
            apart = [t for t in range(1, p.proj_len())
                     if p.fa_pp_at(t, bef_prem) != p.fa_pp(t - 1)]
            assert not apart, (case, apart[:5])
        months = (1, 120, 923)
        for tag in ("sec", "s"):
            plain = _row(models[tag, False], "twin", 4, 0) if tag == "sec" else _point(
                models[tag, False], 4)
            moved = _row(models[tag, True], "twin", 4, 0) if tag == "sec" else _point(
                models[tag, True], 4)
            bef_prem = _code(moved, "BEF_PREM")
            fixed = [(plain.fa_pricing_pp(m), moved.fa_pricing_pp(m)) for m in months]
            if tag == "sec":
                assert all(a == b for a, b in fixed), fixed
                assert [moved.av_pricing_pp_at(m, bef_prem) for m in months] == [
                    plain.av_pricing_pp_at(m, bef_prem) for m in months]
            else:
                assert all(a != b for a, b in fixed), fixed
    finally:
        for model in models.values():
            model.close()


# The COI copy the numbering test reads: the splice's scales (_coi_rates_with_variants),
# seven, written scale by scale in this order, which is not their keys' order, each scale's
# lines in reverse, so that every scale's place in the file differs from its number; and
# the keys S's four points are given on it, by S point, three of them not the anchor's, one
# a scale whose last policy year, 50, is before the point's cover ends.
COI_FILE_ORDER = (("M", "StdNT", 45), ("M", "StdPlusNT", 45), ("F", "PNT", 45),
                  ("M", "StdTob", 45), ("M", "PPlusNT", 45), ("M", "StdNT", SECOND_AGE),
                  ("M", "PTob", 45))
COI_KEYS_OF = {1: ("M", "StdNT"), 2: ("F", "PNT"), 3: ("M", "StdTob"),
               4: ("M", "StdPlusNT")}


def _coi_shuffled(rates):
    """The splice's COI scales, in :data:`COI_FILE_ORDER`, each scale's lines reversed."""
    rates = _coi_rates_with_variants(rates)
    place = {key: k for k, key in enumerate(COI_FILE_ORDER)}
    rates = rates.iloc[::-1].reset_index(drop=True)
    order = rates[["sex", "rate_class", "age_at_entry"]].apply(
        lambda row: place[tuple(row)], axis=1)
    return rates.iloc[order.argsort(kind="stable")].reset_index(drop=True)


def _coi_keys(table):
    """``table`` with the sex and class :data:`COI_KEYS_OF` gives S's point of each row's
    ``policy_id``, which a twin keeps."""
    s_points = dict(zip(_s_policies(), COI_KEYS_OF))
    rows = table.copy()
    for at, policy_id in table["policy_id"].items():
        if policy_id in s_points:
            rows.loc[at, ["sex", "rate_class"]] = COI_KEYS_OF[s_points[policy_id]]
    return rows


def _s_policies():
    """The ``policy_id`` of S's points 1 to 4, in that order."""
    table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                        index_col="point_id")
    return [table.at[point, "policy_id"] for point in sorted(COI_KEYS_OF)]


# VUL_US_S slices its COI scale from a MultiIndex the file leaves unsorted, which pandas
# warns may be slow; the slice is the scale all the same.
@pytest.mark.filterwarnings("ignore:indexing past lexsort depth")
def test_the_coi_scales_are_numbered_by_key_on_a_file_out_of_key_order(tmp_path):
    """On a COI file written out of its keys' order, each point reads its own scale, as S.

    ``Data`` numbers the COI scales in their keys' order in all three cells that number
    them, ``coi_schedule()``, the point's number, and ``coi_rate_array()`` and
    ``coi_rate_last_years()``, the scales and their last policy years by number, so that
    a point's number is the row of its own scale, whatever order the file is written in.
    A ``Data`` numbering cannot be held by the compiled model's comparison with modelx,
    which share ``Data``, nor by the fingerprint, on a file of one scale: it is held here,
    against the file and against ``VUL_US_S``.  On a copy of seven scales, written in an
    order of their own, each scale's lines reversed (:func:`_coi_shuffled`), S's four
    points are given four of them (:data:`COI_KEYS_OF`), in both models: each scale's row
    of ``coi_rate_array()`` is the file's rates for its keys, found by key, and its last
    year the file's; and the twin of each S point is S's point, in every report and every
    cell of S's (:func:`_continues_s`), its COI rate in every month among them, the point
    whose scale ends at policy year 50 reading that year's rate past it.
    """
    edits = {"coi_rates.csv": _coi_shuffled}
    committed = _committed()
    twins = [_label(committed, "twin", point, 0) for point in sorted(COI_KEYS_OF)]
    sec = _read(_sec_inputs(tmp_path / "sec", _coi_keys(committed.loc[twins]), edits),
                "coi_order")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN),
                          edits={**edits, "model_point_table.csv": _coi_keys}),
              "s_coi_order")
    try:
        data = sec.Data
        written = pd.read_csv(data.input_dir() / "coi_rates.csv")
        keys = list(dict.fromkeys(zip(written["sex"], written["rate_class"],
                                      written["age_at_entry"])))
        assert keys == list(COI_FILE_ORDER) and keys != sorted(keys)
        coi, last = data.coi_rate_array(), data.coi_rate_last_years()
        assert data.coi_schedules() == len(keys)
        for number, key in enumerate(sorted(keys), start=1):
            scale = written[(written["sex"] == key[0]) & (written["rate_class"] == key[1])
                            & (written["age_at_entry"] == key[2])]
            assert last[number] == scale["policy_year"].max(), key
            assert np.array_equal(coi[number, scale["policy_year"].to_numpy()],
                                  scale["coi_rate_guar"].to_numpy()), key
        for point in sorted(COI_KEYS_OF):
            sp, p = _point(s, point), _row(sec, "twin", point, 0)
            assert (p.sex(), p.rate_class()) == (sp.sex(), sp.rate_class()) == (
                COI_KEYS_OF[point])
            assert p.coi_schedule() == sorted(keys).index(
                (*COI_KEYS_OF[point], 45)) + 1
            _sweep_s(sp)
            arg_map = _issued_later if point in NEW_BUSINESS else None
            assert _continues_s(sp, p, 0, arg_map) == [], point
    finally:
        s.close()
        sec.close()


# The References under which two bounds of VUL_US_S's bind, which idle at the splice's: a
# current COI scale 1.2 times the guaranteed one, which coi_rate_at bounds by it, and a
# declared rate of 0.5%, below the guaranteed 1%, at which crediting_rate_ann floors it;
# with the behaviour module on, so that the pricing path's rate is read too.  The splice
# sets the declared rate above the floor, so between them both sides of that max are seen.
BOUND_REFS = {"coi_curr_factor": 1.2, "crediting_rate_curr": 0.005,
              "dyn_behavior_on": True}


def test_the_coi_bound_and_the_declared_rate_floor_bind_as_in_vul_us_s():
    """Where its bounds bind, the twin of S's point 4 is S's point, in every cell of S's.

    Two of ``VUL_US_S``'s bounds idle wherever the splice's References leave the current COI
    scale at half the guaranteed one and the declared rate at 2.5%: the guaranteed rate
    over the current one, ``min(rate, coi_rate_guar_at(y), coi_rate_cap)``, and the
    guaranteed 1% under the declared rate, ``max(guar_rate_ann, crediting_rate_curr)``,
    which the pricing path's rate takes too.  With :data:`BOUND_REFS` set in both models
    before anything is computed, on S's point 4, in force 120 months with its fixed option,
    every current rate is the guaranteed one, at every policy year read, where 1.2 times it
    would be more; and the declared rate, the fixed option's monthly rate and the pricing
    path's are the floor's, ``1.01^(1/12) - 1``, in every month.  And the twin is S's point
    from the valuation date, in every report and every cell of S's, the pricing path
    included, to 1e-9 relative with no absolute floor: a bound left out would part them.
    S's margin and net-view identities are the two cells left out.  At the guaranteed
    charges the cash value runs down until the loan exceeds it, from ``t = 322``, at
    attained age 81, so ``VUL_US_S``'s identities, which add back the whole loan on a lapse,
    fail, where this model's three checks hold
    (:func:`test_the_margin_identity_holds_once_a_loan_exceeds_the_cash_value`).
    """
    identities = {"check_margin", "check_net_view"}
    sec = _read(model_path(SEC), "bounds", BOUND_REFS)
    s = _read(model_path(TWIN), "s_bounds", BOUND_REFS)
    try:
        p, sp = _row(sec, "twin", 4, 0), _point(s, 4)
        _sweep_s(sp)
        for report in REPORTS:
            assert frame_mismatches(sp.cells[report](), p.cells[report](),
                                    atol=0.0) == [], report
        assert _twin(sp, p, exempt=TWIN_EXEMPT | identities, atol=0.0) == []
        lent = [t for t in range(p.proj_len())
                if p.loan_bal_pp(t) > p.csv_pp(t) and p.pols_lapse(t) > 0.0]
        assert lent and lent[0] == 322, lent[:3]
        assert (p.check_av_roll_fwd(), p.check_margin(), p.check_net_view()) == (True,) * 3
        assert (sp.check_av_roll_fwd(), sp.check_margin(), sp.check_net_view()) == (
            True, False, False)
        years, factor = sorted(p.cells["coi_rate_at"].keys()), p.coi_curr_factor
        assert years and all(
            p.coi_rate_guar_at(y) == p.coi_rate_at(y) < factor * p.coi_rate_guar_at(y)
            for y in years), years
        floor = (1 + p.guar_rate_ann) ** (1 / 12) - 1
        assert p.fa_pp_init() > 0.0 and p.alloc_fixed() > 0.0
        assert all((p.crediting_rate_ann(t), p.fixed_return_mth(t)) == (0.01, floor)
                   for t in range(p.proj_len()))
        assert p.pricing_fixed_return_mth() == floor
        assert p.cells["fa_pricing_pp_at"].keys(), "the pricing path was not read"
    finally:
        s.close()
        sec.close()


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``VUL_US_S``'s ``isclose`` does.

    The checks are the model's one guard against an account value that is not a number:
    the floors at zero in the cash surrender value and the maxes of the death benefit turn
    a NaN account value into a number, so the cash flows stay numbers and nothing else
    shows it.  On models just read, with the M&E rate, a Reference, set to NaN before
    anything is computed, which runs compiled as it runs here, every subaccount grows by a
    factor that is not a number, and each check's residual is NaN, on S's points 1 and 4,
    and each check is ``False``, where a check that asked whether the residual is above its
    tolerance would pass it.  The year's cash flows are finite floats, so the checks are
    what fails.  ``VUL_US_S``, read alike, fails its checks too.
    """
    models = []
    try:
        for name in (SEC, TWIN):
            models.append(_read(model_path(name), "nan_rate",
                                {"me_rate_ann": float("nan")}))
        sec, s = models
        for point in (1, 4):
            p = _row(sec, "twin", point, 0)
            for check in ("check_av_roll_fwd", "check_margin", "check_net_view"):
                resid, months = p.cells[f"{check}_resid"], range(p.proj_len())
                assert any(math.isnan(resid(t)) for t in months), (point, check)
                assert p.cells[check]() is False, (point, check)
                assert _point(s, point).cells[check]() is False, (point, check)
            flows = [p.cells[c](t) for c in ("premiums", "expenses", "net_cf")
                     for t in range(12)]
            assert all(math.isfinite(v) for v in flows), point
    finally:
        for model in models:
            model.close()


# The lapse shock at which the annual lapse rate passes 1: S's point 3 reaches its cliff at
# policy month 168, in policy year 15, whose base rate is 3%, so 40 times it is 1.2.  Data
# holds each base rate to 0 to 1, but the shock and the dynamic multiplier's bound are
# References, which nothing refuses.
LAPSE_SHOCK, SHOCK_MTH = 40.0, 168


def test_a_lapse_rate_past_1_makes_each_check_raise_as_in_vul_us_s():
    """Past 1 the monthly lapse rate is complex, and every check raises, in both models.

    ``VUL_US_S``'s lapse rate, the base rate times the cliff's spike times the dynamic
    multiplier, has no cap, and this model keeps it so.  So a spike of :data:`LAPSE_SHOCK`,
    set before anything is computed in models just read, takes S's point 3's annual rate to
    1.2 in its cliff month, where ``1 - (1 - q)^(1/12)`` has no real value, and every count
    after it is complex.  ``VUL_US_S``'s ``math.isclose`` raises ``TypeError`` on it, and
    each of this model's three residuals is a ``float`` of its ratio, so it raises too,
    where a residual left complex would have passed its check: the magnitude of a complex
    residual is a real number, 0.0 in the months the reports still balance.  The months
    before the cliff are real, so the checks raise in the cliff month, not before.
    """
    models = {}
    try:
        for name in (SEC, TWIN):
            models[name] = _read(model_path(name), "lapse_past_1",
                                 {"lapse_shock_mult": LAPSE_SHOCK})
        p, s = _row(models[SEC], "twin", 3, 0), _point(models[TWIN], 3)
        for x in (p, s):
            assert (type(x.lapse_rate(SHOCK_MTH)), x.lapse_rate(SHOCK_MTH)) == (float, 1.2)
            assert type(x.lapse_rate_mth(SHOCK_MTH)) is complex
            assert type(x.pols_if(SHOCK_MTH)) is float
            assert type(x.pols_if(SHOCK_MTH + 1)) is complex
        assert type(p.check_av_roll_fwd_resid(SHOCK_MTH - 1)) is float
        for x in (p, s):
            for check in ("check_av_roll_fwd", "check_margin", "check_net_view"):
                with pytest.raises(Exception) as excinfo:
                    x.cells[check]()
                text = str(excinfo.value)
                assert "TypeError" in text and "complex" in text, (x.name, check, text)
    finally:
        for model in models.values():
            model.close()


# How far each check's two sides are moved apart, and whether every check then passes:
# inside the checks' absolute tolerance, and outside it wherever the sides are below 2.
CHECK_MISSES = {5e-10: True, 2e-9: False}


def test_each_check_decides_as_isclose_does_where_its_sides_are_small():
    """Each check decides as ``VUL_US_S``'s ``isclose`` does, where its sides are small too.

    ``VUL_US_S`` asks ``isclose`` with both tolerances at ``1e-9``, which holds where the
    two sides differ by at most ``1e-9`` times the larger of them and 1.  ``VUL_US_SEC``
    divides each month's difference by that larger value and asks whether the residual is
    within ``1e-9`` (:func:`check_av_roll_fwd_resid`), which is the same test only through
    the floor of 1: over the larger side alone, a miss inside the absolute tolerance fails
    where the sides are below 1, and over a floor above 1 a miss outside it passes.  So on
    models just read, ``inv_income``, the investment credit, which only the three checks
    read, is moved by each miss of :data:`CHECK_MISSES` in both models before anything is
    computed (a formula override through a new cell, so modelx's alone), and on S's point
    1, whose account value in force and net cash flow fall below 0.5 late in its frame,
    each check of each model passes the miss of ``5e-10`` and fails the one of ``2e-9``.
    """
    for miss, passes in CHECK_MISSES.items():
        models = []
        try:
            for name in (SEC, TWIN):
                model = mx.read_model(model_path(name), name=_name("moved_credit"))
                models.append(model)
                proj = model.Projection
                proj.new_cells(name="inv_income_unmoved",
                               formula=proj.cells["inv_income"].formula.source)
                proj.cells["inv_income"].formula = (
                    f"lambda t: inv_income_unmoved(t) + {miss!r}")
            sec, s = models
            p, sp = _row(sec, "twin", 1, 0), _point(s, 1)
            bef_prem = _code(p, "BEF_PREM")
            assert any(max(abs(p.av_at(t, bef_prem)), abs(p.av_at(t + 1, bef_prem)),
                           abs(p.net_cf(t))) < 0.5 for t in range(p.proj_len()))
            for check in ("check_av_roll_fwd", "check_margin", "check_net_view"):
                assert (p.cells[check](), sp.cells[check]()) == (passes, passes), (
                    miss, check)
        finally:
            for model in models:
                model.close()


# S's in-force point 4 withdrawing $600 a month on Option B, F PNT, with its loan: its
# withdrawals run its unloaned accounts down until the loan exceeds the cash value, where a
# surrender pays the net cash value floored at 0 and recovers only the cash value of the
# loan.  Restated in force at S's month 225, the month before, its account value still
# above 0, it is read under the splice's References and inputs, its scenario re-based to
# its month.
LENT = (4, {"policy_id": "VUL-900016", "wd_pp": 600.0, "db_option": "B", "sex": "F",
            "rate_class": "PNT"})
LENT_MTH = 225


def test_the_margin_identity_holds_once_a_loan_exceeds_the_cash_value(tmp_path):
    """Once the loan exceeds the cash value, the margin identities still close.

    ``VUL_US_S``'s two identities add back the whole loan on every lapse,
    ``L(t) x pols_lapse(t)``, as though the lapse claim were ``CSV - L``.  The claim is the
    net cash value, floored at 0, so once the loan exceeds the cash value each identity is
    off by ``(CSV(t) - L(t)) x pols_lapse(t)``, and ``VUL_US_S``'s ``check_margin`` and
    ``check_net_view`` fail on a projection that is right.  This model's add back the loan
    the surrender recovers, ``min(L(t), CSV(t)) x pols_lapse(t)``, and the whole loan on a
    death, whose claim has no floor.  On the point of :data:`LENT`, restated in force in
    the month before its loan passes its cash value:

    * its four reports are S's from that month on, to 1e-9 relative with no absolute floor:
      the projection is S's;
    * from ``t = 1`` its loan exceeds its cash value while policies lapse, and in each such
      month S's margin identity misses by ``(CSV - L) x pols_lapse``, to the identity's own
      tolerance;
    * this model's three checks hold, ``VUL_US_S``'s ``check_margin`` and ``check_net_view``
      fail, and its account value roll-forward holds.
    """
    base, changes = LENT
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    row = s_table.loc[[base]].assign(**changes)
    row.index = pd.Index([16], name="point_id")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=row,
                          edits=SPLICED_EDITS), "lent_s", SPLICED_REFS)
    sec = None
    try:
        sec = _read(_spliced_folders(tmp_path / "sec", s, ((16, LENT_MTH),), ()), "lent",
                    SPLICED_REFS)
        sp, p = _point(s, 16), _row(sec, "derived", 16, LENT_MTH)
        for report in REPORTS:
            assert frame_mismatches(sp.cells[report](), p.cells[report](),
                                    t_offset=LENT_MTH, atol=0.0) == [], report
        lent = [t for t in range(p.proj_len())
                if p.loan_bal_pp(t) > p.csv_pp(t) and p.pols_lapse(t) > 0.0]
        assert lent and lent[0] == 1, lent[:3]
        for t in lent:
            s_rhs = (p.margin_expense(t) + p.margin_mortality(t) + p.av_change(t)
                     - p.inv_income(t) + p.loan_bal_pp(t) * p.pols_lapse(t))
            gap = p.net_cf(t) - s_rhs
            floored = (p.csv_pp(t) - p.loan_bal_pp(t)) * p.pols_lapse(t)
            assert abs(gap - floored) <= 1e-9 * max(abs(p.net_cf(t)), 1.0), t
        assert p.check_margin() and p.check_net_view() and p.check_av_roll_fwd()
        assert (sp.check_margin(), sp.check_net_view(), sp.check_av_roll_fwd()) == (
            False, False, True)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# Inputs at which a product or sum taken in another order than VUL_US_S's differs in its
# last bit: an acquisition expense, a maintenance expense and a multiple of the counts that
# no binary fraction holds exactly; and expense inflation, which acquisition must not take.
ACQ, MAINT, COUNTS = 123.456, 77.7, 3.7


def test_acquisition_is_charged_on_new_business_only(tmp_path):
    """``expense_acq`` per policy issued, in the issue month, never inflated or in force.

    ``expense_acq`` ships at 0 and so does inflation.  On a copy whose counts are
    :data:`COUNTS` times the committed table's, with :data:`ACQ`, :data:`MAINT` and
    inflation at 2.5% set, a charge per model point would show beside one per policy, and
    an inflated one beside one that is not.  On every point, what ``expenses(t)`` holds
    beyond its maintenance part is ``ACQ * policy_count()`` in the issue month,
    ``t = -duration_mth``, and 0 in every other month to ``t = 26``, to 1e-9: the twin of
    S's new business bears it at ``t = 0``, the point issued 25 months on at ``t = 25``,
    where the maintenance part is inflated by ``1.025^2``, two valuation years on, and the
    acquisition is not, and the points already in force never, though on the valuation
    clock their row 0 is ``t = 0``.

    ``VUL_US_S`` charges acquisition on the count in force in the issue month, which on a
    point issued at the valuation date is the issued count, so the twin agrees with S at
    any count, and T1 needs no S point to count one policy.  The formula is S's, in S's
    order, no product or sum reordered, so on the twin of S's new business, read by S at
    the same counts and inputs, the expenses are S's bit for bit.
    """
    refs = {"expense_acq": ACQ, "expense_maint": MAINT, "inflation_rate": INFLATION}
    table = _committed()
    model = _read(_sec_inputs(tmp_path / "sec", table.assign(
        policy_count=COUNTS * table["policy_count"])), "acquisition", refs)
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_table.assign(
        pols_if_init=COUNTS * s_table["pols_if_init"])), "acquisition_s", refs)
    try:
        read = model.Data.model_point_table()
        months = range(27)
        for key, point_id in zip(point_keys(model), read.index):
            p = projection(model, key)
            acq = [p.expenses(t)
                   - p.expense_maint / 12 * p.inflation_factor(t) * p.pols_if(t)
                   for t in months]
            issue = -read.at[point_id, "duration_mth"]
            expected = [ACQ * p.policy_count() if t == issue else 0.0 for t in months]
            assert acq == pytest.approx(expected, abs=1e-9), point_id
            assert (issue in months) == (sum(expected) > 0.0), point_id
        later = _row(model, "future", 3, -25)
        assert later.inflation_factor(25) == (1 + INFLATION) ** 2 == 1.050625
        assert later.expenses(25) == pytest.approx(
            (ACQ + MAINT / 12 * 1.050625) * COUNTS, rel=1e-12)
        for twin in NEW_BUSINESS:
            mine, theirs = _row(model, "twin", twin, 0), _point(s, twin)
            assert [mine.expenses(t) for t in months] == [theirs.expenses(t)
                                                          for t in months], twin
    finally:
        s.close()
        model.close()


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate caps the annual rate at 1, as VUL_US_S's does since USLIB-SEC-PLAN.md §8.2
# item 4's fix, so the cap is no departure.  At the shipped A/E VUL_US_S's StdTob class,
# 1.75 times the base table, takes the product past 1 at attained age 113, at 1.095, and
# keeps it past 1 to the end of the projection.  The committed points are all StdNT, and
# the splice's A/E of 0.56 keeps every class below 1, so neither comes near it.  One point
# is made to pass it, the way the variants are made: S's new-business point 3 in the StdTob
# class on Option A, with its own COI rows, alone in a copy of S's table, under the splice's
# References with the A/E back at the shipped 1.0 (CAPPED_REFS).  Its scenario, LEVEL6, is
# flat, so no row needs a re-based copy.
CAPPED = (3, {"policy_id": "VUL-900020", "rate_class": "StdTob", "db_option": "A"})
CAPPED_REFS = {**SPLICED_REFS, "mort_ae_factor": 1.0}
CAPPED_EDITS = {"coi_rates.csv": _coi_rates_with_variants}
CAPPED_MTH = 816        # the first month at attained age 113, where the product passes 1


def _uncapped_mort_rate(proj, t):
    """``VUL_US_S``'s annual mortality product in month t, the one its cap bounds.

    The base table's rate at the attained age, read at the table's nearest age, times the
    class factor and the A/E, computed from S's own cells and tables.
    """
    table = proj.data.mort_table()
    a = min(max(proj.age(t), int(table.index.min())), int(table.index.max()))
    return float(table.loc[a, "mort_rate"]) * proj.class_factor() * proj.mort_ae_factor


def _sweep_months(proj):
    """Evaluate every monthly cell of an S point at every month of its frame.

    At each subaccount, timing or kind it takes, as :func:`_sweep_s` reaches them, so that
    the cap test compares every monthly cell in every month the cap binds, those no report
    or check reads among them.
    """
    arguments = {**BY_ARGUMENT, **OPENING, "av_pp_at": AV_TIMINGS,
                 "av_at": (*AV_TIMINGS, "EOM")}
    ids = _subaccounts(proj)
    names = sorted(_monthly_cells(proj))
    for t in range(proj.proj_len()):
        for name in names:
            cells = proj.cells[name]
            if name == "sa_pp_at":
                for i in ids:
                    for timing in AV_TIMINGS:
                        cells(t, i, _code(proj, timing))
            elif cells.parameters[1:] == ("i",):
                for i in ids:
                    cells(t, i)
            elif name in arguments:
                for label in arguments[name]:
                    cells(t, _code(proj, label))
            else:
                cells(t)


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On the point of :data:`CAPPED`, ``VUL_US_S``'s product of the base rate, the class
    factor and the A/E (:func:`_uncapped_mort_rate`) passes 1 in month :data:`CAPPED_MTH`
    and stays past it to the end of the projection, on a point the contract issues.  Both
    models cap it: ``mort_rate`` and the monthly rate, ``1 - (1 - q)^(1/12)``, are 1.0 in
    every one of those months, the float, not the int 1, which compares equal to it, and
    S's are floats below 1 in every month before.  So every policy in force at the start
    of the first capped month dies in it, and none is in force after it.  The four reports
    hold finite floats alone, and the three checks hold.

    In every cell of S's this model agrees with S at every argument S cached, the capped
    months and the reports included, at 1e-9 relative with no absolute floor, because the
    counts before the cap fall to 1.4e-13, where the default floor of 1e-9 would compare
    them against nothing.  S is swept as the splice sweeps it (:func:`_sweep_s`), and every
    monthly cell in every month (:func:`_sweep_months`).

    Four rows of the point, built from S by the generator under :data:`CAPPED_REFS`:
    issued at the valuation date, compared as a new-business twin, and 25 months after it;
    restated in force in the month before the cap, opened with S's count and state there,
    and compared cell by cell as a splice row is; and restated five months into the capped
    year, opened with S's state there and one policy, since S's count there is 0.  On each,
    the rate is 1.0 from its first capped month, every policy in force there dies in it,
    and the count is 0.0 after it: a cap applied to new business alone would pass both
    comparisons, which see S's capped rate, and fail here, on the rows in force.
    """
    base, changes = CAPPED
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN),
                          model_points=s_table.loc[[base]].assign(**changes),
                          edits=CAPPED_EDITS), "capped_s", CAPPED_REFS)
    sec = None
    try:
        sp = _point(s, base)
        end = sp.proj_len()
        cap = next(t for t in range(end) if _uncapped_mort_rate(sp, t) > 1)
        assert (cap, sp.age(cap)) == (CAPPED_MTH, 113)
        assert _uncapped_mort_rate(sp, cap) == pytest.approx(0.625687 * 1.75, rel=1e-12)
        after = range(cap, end)
        assert all(_uncapped_mort_rate(sp, t) > 1 for t in after)
        for rate in (sp.mort_rate, sp.mort_rate_mth):
            assert all(type(rate(t)) is float and rate(t) < 1.0 for t in range(cap))
            assert [(type(rate(t)), rate(t)) for t in after] == [(float, 1.0)] * len(after)
        _sweep_s(sp)
        _sweep_months(sp)
        assert sp.pols_if(cap) > 0.0 and sp.pols_death(cap) == sp.pols_if(cap)
        assert [sp.pols_if(t) for t in range(cap + 1, end)] == [0.0] * (len(after) - 1)
        spec = dataclasses.replace(SPEC, derived=((base, cap - 1),), future=((base, 25),))
        table, _ = build_sec_table(spec, s)
        inside = cap + 5
        row = table[table["source_mth"] == cap - 1].assign(
            point_id=table["point_id"].max() + 1, duration_mth=inside, source_mth=inside,
            policy_id=f"{changes['policy_id']}-M{inside}", policy_count=1.0,
            **{column: extract(sp, inside) for column, extract in SPEC.state.items()})
        table = pd.concat([table, row], ignore_index=True)
        sec = _read(_sec_inputs(tmp_path / "sec", table, CAPPED_EDITS), "capped",
                    CAPPED_REFS)
        # Each row with the month its rate is first capped and, for the three S's count
        # opens, the exemptions of its comparison with S.
        rows = ((("twin", base, 0), cap, TWIN_EXEMPT),
                (("future", base, -25), cap + 25, FUTURE_EXEMPT),
                (("derived", base, cap - 1), 1, SPLICE_EXEMPT),
                (("derived", base, cap + 5), 0, None))
        for case, first, exempt in rows:
            key = _row_key(sec, *case)
            p = projection(sec, key)
            if exempt is not None:
                assert _twin(sp, p, t_offset=case[2], exempt=exempt,
                             arg_map=_issued_later, atol=0.0) == [], case
            capped, later = range(first, p.proj_len()), range(first + 1, p.proj_len() + 1)
            for rate in (p.mort_rate, p.mort_rate_mth):
                assert [(type(rate(t)), rate(t)) for t in capped] == (
                    [(float, 1.0)] * len(capped)), case
            assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first), case
            assert [p.pols_if(t) for t in later] == [0.0] * len(later), case
            for report in REPORTS:
                frame = p.cells[report]()
                assert (frame.dtypes == "float64").all(), (case, report)
                assert all(math.isfinite(v) for v in frame.to_numpy().ravel()), (
                    case, report)
            assert p.check_av_roll_fwd() and p.check_margin() and p.check_net_view(), case
            del p
            _release(sec, key)
    finally:
        if sec is not None:
            sec.close()
        s.close()


def _nan_factor():
    """NaN, what a blank factor carries: the formula a test puts in place of a cell's."""
    return float("nan")


# How a NaN is sent to the cap: (case, the cell whose formula returns NaN, or the Reference
# set to NaN).  The class factor's formula is modelx's alone; the A/E, a Reference set
# before the model computes anything, runs compiled as it runs here.
NAN_CAP = [("a class factor's formula", "class_factor", None),
           ("the A/E, a Reference", None, "mort_ae_factor")]


@pytest.mark.parametrize("case, cell, ref", NAN_CAP, ids=[c[0] for c in NAN_CAP])
def test_a_nan_that_reaches_the_cap_stays_nan(case, cell, ref):
    """A NaN that reaches the cap on mortality stays NaN, and is not read as 1.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first the cap would
    turn a NaN into 1.0: a blank class factor read as certain death, every flow finite.  It
    is written ``min(q, 1.0)``, in both models.  ``Data`` refuses a blank factor or rate as
    it reads the tables, so to send the cap a NaN, in models read for the test, either the
    formula of ``class_factor``, which feeds it, is replaced by one returning NaN, which
    modelx allows, or the A/E, ``mort_ae_factor``, is set to NaN before anything is computed
    (:data:`NAN_CAP`).  ``mort_rate`` must then be the float NaN in the first month in both
    models, and in this one in the last month too, and so must the monthly rate and the
    count after the first month.
    """
    models = []
    try:
        for name in (SEC, TWIN):
            model = _read(model_path(name), "nan_factor",
                          {ref: float("nan")} if ref else None)
            models.append(model)
            if cell:
                model.Projection.cells[cell].formula = _nan_factor
        sec, s = models
        p = _row(sec, "twin", 1, 0)
        calls = [(p, "mort_rate", (0,)), (p, "mort_rate", (p.proj_len() - 1,)),
                 (p, "mort_rate_mth", (0,)), (p, "pols_if", (1,)),
                 (_point(s, 1), "mort_rate", (0,))]
        lost = [f"{x.name}.{name}{args} = {value!r}" for x, name, args in calls
                for value in [x.cells[name](*args)]
                if not (type(value) is float and math.isnan(value))]
        assert not lost, f"the cap loses a NaN sent through {case}: {lost}"
    finally:
        for model in models:
            model.close()


def _nan_scale():
    """A guaranteed COI scale that is not a number in any policy year, as a blank is."""
    return pd.Series(float("nan"), index=range(1, 123))


def _nan_coi_array():
    """The guaranteed COI rates, by schedule and policy year, not a number in any, as
    ``Data.coi_rate_array`` holds them at stage ``"EC"``."""
    return np.full((coi_schedules() + 1, 123), float("nan"))         # noqa: F821


def _nan_pin():
    """A first-month COI pin that is not a number."""
    return float("nan")


# Each min written with its bound second that a NaN can reach, beyond the cap on mortality:
# VUL_US_S's own bounds on the COI rate, the cap of $83.34 on the guaranteed scale and the
# guaranteed rate and the cap over the current one, which the model keeps in S's order, and
# the first-month pin's.  (case, by model, the space and the cell whose formula is
# replaced and its replacement, the calls on the twin of S's point 1 that must be NaN.)  A
# COI rate is a charge, not a decrement, and is never capped at 1.  S's scale is a Series,
# coi_rate_scale, which SEC at stage EC holds in Data's coi_rate_array instead, the one
# change the dropped cell forces on this test.
NAN_BOUNDS = [
    ("the COI scale's bounds",
     {SEC: ("Data", "coi_rate_array", _nan_coi_array),
      TWIN: ("Projection", "coi_rate_scale", _nan_scale)},
     (("coi_rate_guar_at", (1,)), ("coi_rate_guar", (1,)), ("coi_rate_at", (3,)),
      ("coi_rate", (1,)))),
    ("the COI pin's bounds",
     {SEC: ("Projection", "coi_rate_override_m1", _nan_pin)},
     (("coi_rate", (0,)),)),
]


@pytest.mark.parametrize("case, replaced, calls", NAN_BOUNDS,
                         ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_written_second_stays_nan(case, replaced, calls):
    """A NaN that reaches a ``min`` with its bound second stays NaN, in both models.

    ``min(x, cap)`` keeps ``x`` unless the cap compares smaller, and no comparison with NaN
    holds, so a NaN COI rate stays NaN, where the bound first would turn it into the cap:
    a blank rate read as the most the contract charges.  ``Data`` refuses a blank rate as
    it reads the scale, so the formula that feeds the bound is replaced, in models read for
    the test, by one that returns NaN, and every call is then the float NaN.
    """
    models = {}
    try:
        for name, (space, cell, formula) in replaced.items():
            models[name] = mx.read_model(model_path(name), name=_name("nan_bound"))
            models[name].spaces[space].cells[cell].formula = formula
        lost = []
        for name, model in models.items():
            p = _row(model, "twin", 1, 0) if name == SEC else _point(model, 1)
            lost += [f"{name}.{cells}{args} = {value!r}" for cells, args in calls
                     for value in [p.cells[cells](*args)]
                     if not (type(value) is float and math.isnan(value))]
        assert not lost, f"{case} lose a NaN: {lost}"
    finally:
        for model in models.values():
            model.close()


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


# What only VUL_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting S's own projected months; its
# opening, at t == 0, where this model opens at t_entry(); the loan account taken equal to
# the debt, which this model's opening state replaces; the stub's timings, which here part
# in the issue month; and inflation by policy year, which here steps on the valuation
# clock.
STALE = re.compile(r"~\.VUL_US_S\.|projected months?\b|is taken equal to it"
                   r"|All three ``CashValue_SE`` timings coincide"
                   r"|when ``t == 0``|pols_if\(0\) = l_0"
                   r"|inflation_rate\)\^\(y - 1\)")


def test_the_docstrings_describe_the_valuation_clock(sec_model):
    """The docstrings say what this model is, and none says what only VUL_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock and the product.  The symbol map in the
    Projection docstring maps every cell running in force adds or gives a new meaning, and
    names nothing the model lacks: every name in it is a cell, or a Reference the technical
    notes give a symbol to, as the M&E rate and the cap on the COI rate are in
    ``VUL_US_S``'s map.  And no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "policy year",
                   "variable universal life"):
        assert phrase in flat["model"], phrase
    for phrase in ("valuation date", "duration_mth", "t_entry", "la_pp_init",
                   "sum_assured_init", TABLE):
        assert phrase in flat["Projection"], phrase
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe VUL_US_S: {stale}"


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


def _months(n):
    """``n`` with its unit, as ``run_sec.py`` writes it: "1 month", "25 months"."""
    return f"{n} month" + ("" if n == 1 else "s")


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {_months(-d)} after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {_months(d)}: policy year {p.policy_year(0)}, attained age "
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, account value "
            f"{p.av_pp_init():,.2f}, loan {p.loan_bal_init():,.2f}, collateral "
            f"{p.la_pp_init():,.2f}, face {p.sum_assured_init():,.0f}")


def _heading(point, origin, option, scenario):
    """``run_sec.py``'s first line for a committed point of S's anchor cell."""
    return (f"model point {point}: {origin} - M45 StdNT face 500,000 option {option} GPT, "
            f"LEVEL premium 6,000.00/yr, scenario {scenario}")


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them.  Every generated table
    also numbers its points 1, 2, ... in table order, so an extract here is relabelled too,
    ``100 + point_id``, in reverse order, 109 first: a label read as a position would then
    project the wrong point, which no other table can show.  Read so, every point projects
    what the committed point it came from projects, in ``result_cf`` and ``result_pols``, to
    1e-12, and ``run_sec.py``, run beside that extract, prints the point it is given by its
    label, without saying where it came from, and refuses a label the extract lacks, naming
    the labels it has, or a label that is not a number, without a traceback.  Its refusals
    name the label too: ``Data``'s of a malformed row, and ``proj_len()``'s of a point past
    the end of the projection, which ``run_sec.py --block`` meets before it projects any
    point.  On S's in-force rows ``source_mth`` is 0 and ``duration_mth`` 24 or 120, so a
    formula that read the one for the other would pass every test that leaves
    ``duration_mth`` as generated but this one.
    """
    extract = _committed().drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(extract.index + 100, name="point_id")
    extract = extract.iloc[::-1]
    folder = _sec_inputs(tmp_path / "extract", extract)
    model = mx.read_model(folder, name=_name("extract"))
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(range(109, 100, -1))
        for key, label in zip(point_keys(model), table.index):
            mine, base = projection(model, key), _point(sec_model, label - 100)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (label, report)
            _release(model, key)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "106")
    assert out.splitlines()[:2] == [
        _heading(106, "VUL-000004-M6", "A", "LEVEL6"),
        f"at the valuation date: {_standing(_row(sec_model, 'derived', 4, 6))}"]
    for label in ("6", "x"):
        done = _run_sec(runner, label, check=False)
        errors = done.stderr.decode(errors="replace")
        assert done.returncode == 1 and done.stdout == b"", label
        assert (f"no model point {label} in the table: {list(range(109, 100, -1))}"
                in errors and "Traceback" not in errors), errors
    model = mx.read_model(_sec_inputs(tmp_path / "unpaired", _set("la_pp_init", [101], 1.0)(
        extract)), name=_name("unpaired"))
    try:
        _refused(model.Data.model_point_table,
                 "la_pp_init must be above 0 where loan_bal_init is, and 0 where it is 0: "
                 "the loan account holds a loan's collateral while the loan is "
                 "outstanding; it is not at point_id [101]")
    finally:
        model.close()
    moved = _sec_inputs(tmp_path / "moved", _set("duration_mth", [104], 924)(extract))
    message = ("point_id 104: duration_mth 924 is at or past the end of the projection, "
               "policy month 924, attained age 122")
    model = mx.read_model(moved, name=_name("moved"))
    try:
        _refused(_point(model, 104).proj_len, message)
    finally:
        model.close()
    runner = moved.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def test_run_sec_prints_a_point_and_the_block(sec_model, s_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The runner's default is S's point 1, in force 24 months, whose row
    ``t = 0`` is the worked example's month: its lines at the valuation date, each asserted
    whole, so that a longer number cannot pass for the one asserted, and its first twelve
    rows of cash flows, of the account value roll-forward and of counts, the first two
    ``VUL_US_S``'s own, row for row, since the point is S's point 1.  Point 6, restated in
    force at S's month 6 on S's point 4, and point 9, to be issued 25 months on, each with
    the two lines that say where its row came from and where it stands, which only the
    committed table's generator columns can say.  And the block: a line for each of the
    nine points, in table order, its first twelve rows, which must be the committed points'
    frames summed row by row, as this test sums them, and those frames summed into
    projection years, each year's count the one in force in its first month.  Nothing else
    runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    anchor, s_anchor = _row(sec_model, "twin", 1, 0), _point(s_model, 1)
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        _heading(1, "VUL-000001 (S's VUL-000001)", "A", "WE"),
        f"at the valuation date: {_standing(anchor)}",
        "proj_len = 900 months from the valuation date (t = 0..899); the projection ends "
        "at policy month 924, attained age 122"]
    for report in ("result_cf", "result_av", "result_pols"):
        assert anchor.cells[report]().head(12).round(
            6 if report == "result_pols" else 2).to_string() in out, report
    for report in ("result_cf", "result_av"):
        assert s_anchor.cells[report]().head(12).round(2).to_string() in out, report
    for point, kind, s_point, month, origin, option in (
            ("6", "derived", 4, 6, "VUL-000004-M6 (S's VUL-000004 at its month 6)", "A"),
            ("9", "future", 3, -25,
             "VUL-000003-F25 (S's VUL-000003, issued 25 months on)", "B")):
        p = _row(sec_model, kind, s_point, month)
        assert _run_sec(runner, point).splitlines()[:2] == [
            _heading(point, origin, option, "LEVEL6"),
            f"at the valuation date: {_standing(p)}"], point
    out = _run_sec(runner, "--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<16} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert annual.head(12).round(2).to_string() in out


# ---------------------------------------------------------------------------
# Stage EC -- what compiling changed, held in modelx (USLIB-SEC-PLAN.md Phase 2)


def test_the_split_totals_are_s_totals_bit_for_bit(sec_model, s_model):
    """``claims(t)`` and ``me_charge_pp(t)`` are ``VUL_US_S``'s totals, bit for bit (R12).

    S's ``claims(t, kind=None)`` is the two kinds and their total in one cell, and its
    ``me_charge_pp(t, i=None)`` each subaccount's charge and their total, each total a
    ``sum`` of a generator.  Here the kinds are ``claims_death`` and ``claims_lapse``, a
    subaccount's charge is ``me_charge_sa_pp(t, i)``, and each total is written out from
    ``0.0``; T1 reaches S's totals through the spec's ``twin_arg_map`` to its tolerance,
    and skips S's keys of a kind or a subaccount.  So they are held here, exactly: on the
    twins of S's four points, which S opens at its own ``t = 0``, in every month of the
    frame, each total equal to S's, its type and the sign of a zero included, each kind
    equal to S's ``claims(t, kind)``, and each subaccount's charge, at its position, to
    S's ``me_charge_pp(t, i)`` at its id.  Python's ``sum`` of two floats is their one
    rounded sum, so the totals written out are S's floats in every month of the shipped
    lineup of two.
    """
    found = []
    for point in (*IN_FORCE, *NEW_BUSINESS):
        mine, theirs = _row(sec_model, "twin", point, 0), _point(s_model, point)
        assert mine.proj_len() == theirs.proj_len()
        ids = theirs.subaccount_ids()
        for t in range(mine.proj_len()):
            for cell in ("claims", "me_charge_pp"):
                got, want = mine.cells[cell](t), theirs.cells[cell](t)
                if (got != want or type(got) is not type(want)
                        or math.copysign(1.0, got) != math.copysign(1.0, want)):
                    found.append(f"point {point}: {cell}({t}) {got!r}, S's {want!r}")
            for cell, kind in (("claims_death", "DEATH"), ("claims_lapse", "LAPSE")):
                if mine.cells[cell](t) != theirs.claims(t, kind):
                    found.append(f"point {point}: {cell}({t}) is not S's "
                                 f"claims({t}, {kind!r})")
            for i in ids:
                if mine.me_charge_sa_pp(t, _sa(mine, i)) != theirs.me_charge_pp(t, i):
                    found.append(f"point {point}: me_charge_sa_pp({t}, {_sa(mine, i)}) is "
                                 f"not S's me_charge_pp({t}, {i})")
    assert not found, found[:20]


# The month at which the sign test sets the kinds and the subaccounts' charges on the
# worked example's twin: in cover, where each is nonzero.
ZERO_MONTH = 5


def test_negative_zero_parts_total_a_positive_zero_as_s_sum_does():
    """Each total is ``0.0``, not ``-0.0``, where every part is ``-0.0``, as S's ``sum``.

    S's totals are ``sum`` of their parts, which starts at the int 0, and ``0 + -0.0`` is
    ``0.0``, so S's total of negative zeros is a positive zero.  ``claims(t)`` and
    ``me_charge_pp(t)`` start their sums at ``0.0`` for that reason, and the split test
    cannot hold it: no committed month has negative zero parts.  So here, on a read of each
    model of its own, the two kinds and the two subaccounts' charges of the worked
    example's twin at :data:`ZERO_MONTH` are set to ``-0.0`` as modelx input values, and
    so are S's ``claims(t, kind)`` and ``me_charge_pp(t, i)`` of its point 1 in the same
    month, and each total must be S's: ``0.0``, a float, with a positive sign.  A total
    started at its first part, or written without its ``0.0``, gives ``-0.0`` and fails.
    """
    s = mx.read_model(model_path(TWIN), name=_name("s_zeros"))
    sec = mx.read_model(model_path(SEC), name=_name("zeros"))
    try:
        theirs, mine = _point(s, 1), _row(sec, "twin", 1, 0)
        assert mine.claims_death(ZERO_MONTH) == theirs.claims(ZERO_MONTH, "DEATH") != 0.0
        for i in theirs.subaccount_ids():
            assert mine.me_charge_sa_pp(ZERO_MONTH, _sa(mine, i)) == theirs.me_charge_pp(
                ZERO_MONTH, i) != 0.0
            theirs.me_charge_pp[ZERO_MONTH, i] = -0.0
            mine.me_charge_sa_pp[ZERO_MONTH, _sa(mine, i)] = -0.0
        for kind in ("DEATH", "LAPSE"):
            theirs.claims[ZERO_MONTH, kind] = -0.0
        for cell in ("claims_death", "claims_lapse"):
            mine.cells[cell][ZERO_MONTH] = -0.0
        totals = (theirs.claims(ZERO_MONTH), mine.claims(ZERO_MONTH),
                  theirs.me_charge_pp(ZERO_MONTH), mine.me_charge_pp(ZERO_MONTH))
    finally:
        sec.close()
        s.close()
    for total in totals:
        assert type(total) is float and total == 0.0, totals
        assert math.copysign(1.0, total) == 1.0, totals


# The extract's labels, in the order its rows are written: the committed table's point_id
# plus 100, row 9 first, so that a label read as a position, or as a position plus one,
# names another point (test_an_in_force_extract_needs_none_of_the_generator_columns).
EXTRACT_LABELS = list(range(109, 100, -1))


def _extract():
    """The committed table as an administration extract would hold it: without the
    generator's columns, and labelled :data:`EXTRACT_LABELS`, row 9 first."""
    extract = _committed().drop(columns=list(GENERATED_COLUMNS)).iloc[::-1]
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    return extract


# The reads beyond a table on the committed inputs, as (cell, arguments, the message after
# the point's label): a policy year below 1, where VUL_US_S's .loc and slice raised
# KeyError, which each year reader refuses before it reads its padded array; and a
# subaccount's position past the lineup, either side, which each reader of a subaccount's
# input refuses before it reads, where VUL_US_S's column or .loc raised KeyError.
_NO_POSITION = "no subaccount at position {} of the lineup of 2"
BEYOND = [
    ("prem_persistency_py", (0,), "prem_persistency.csv has no factor for policy year 0"),
    ("lapse_rate_base_py", (0,), "lapse_table.csv has no rate for policy year 0"),
    ("coi_rate_guar_at", (0,), "coi_rates.csv has no rate for policy year 0"),
    ("prem_persistency_py", (-1,), "prem_persistency.csv has no factor for policy year -1"),
    ("lapse_rate_base_py", (-1,), "lapse_table.csv has no rate for policy year -1"),
    ("coi_rate_guar_at", (-1,), "coi_rates.csv has no rate for policy year -1"),
    *[(cell, (2,), _NO_POSITION.format(2))
      for cell in ("alloc", "fund_expense_ann", "sa_pp_init", "scenario_last_mth")],
    *[(cell, (-1,), _NO_POSITION.format(-1))
      for cell in ("alloc", "fund_expense_ann", "sa_pp_init", "scenario_last_mth")],
    ("gross_return_mth", (0, 2), _NO_POSITION.format(2)),
]
NO_SCALE = "coi_rates.csv has no scale for the point's sex, rate_class and age_at_entry"


def _scenarios_unsorted(_):
    """Three return scenarios, written out of their ids' order, one of them read by none.

    ``LEVEL6``, ``MID`` and ``WE``, sorted, written ``WE``, ``MID``, ``LEVEL6``, line by
    line in reverse, with ``MID``, which no point names, between the two that points read;
    each scenario and subaccount a path of its own, from its own first month, ``WE``'s
    bond path from month 3, so that a row or a first month read for another scenario
    changes a number or a refusal.
    """
    rows = []
    for scenario, base, first in (("LEVEL6", 0.0050, 0), ("MID", 0.0070, 0),
                                  ("WE", 0.0035, 0)):
        for i, step in ((1, 0.0001), (2, 0.00003)):
            start = 3 if (scenario, i) == ("WE", 2) else first
            for t in range(start, start + 30):
                rows.append((scenario, i, t, round(base + step * t, 10), "test copy"))
    return pd.DataFrame(rows[::-1], columns=["scenario_id", "subaccount_id", "t",
                                             "gross_return_mth", "provenance"])


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, the readers refuse a key before a table, by name (§7.1 item 9).

    Each reader of a padded table refuses a key below it (:data:`BEYOND`), naming the
    point by its label, on the extract labelled otherwise than by position, where a label
    read as ``idx + 1`` would name another: a policy year below 1 in the three year
    readers, and a subaccount's position past the lineup, either side, in the four readers
    of a subaccount's input and the return.  A year past a table reads its last row and an
    age outside the two age tables the nearest row, as ``VUL_US_S`` reads them.  A point
    whose COI scale the table lacks, issued at 36, has schedule 0 and is refused by
    ``coi_rate_last_year()`` once a rate is read, by its projection, and projects once
    ``charges_cease_age`` is 36, where no rate is read, as ``VUL_US_S`` projects it.

    The padding is NaN, as the ``Data`` docstrings say, so that a read past a check, were
    one lost, would make every number after it NaN rather than another key's value: row 0
    of the COI scale, its column of policy year 0 and every year past each schedule's last;
    year 0 of the two policy-year tables; the ages below each age table's first; row 0 of
    the return array, each month before a path's first and after its last; and nothing
    inside.  The scenarios are numbered in their ids' order in all four cells that number
    them, and on a copy written out of that order, with a scenario no point names between
    two that points name (:func:`_scenarios_unsorted`), each point's row of each array is
    its own scenario's, read from the file by key; the return the point reads in a month
    before its path's first is refused, naming the subaccount and the month.
    """
    extract = _extract()
    label = extract.index[0]
    model = mx.read_model(_sec_inputs(tmp_path / "extract", extract), name=_name("beyond"))
    try:
        p = _point(model, label)
        assert p.point_id() == label != point_keys(model)[0] + 1
        found = []
        for cell, args, message in BEYOND:
            with pytest.raises(Exception) as excinfo:
                p.cells[cell](*args)
            if _raised(excinfo.value) != f"ValueError: point_id {label}: {message}":
                found.append(f"{cell}{args}: {_raised(excinfo.value)}")
        assert not found, found
        assert p.prem_persistency_py(500) == p.prem_persistency_py(
            model.Data.prem_persistency_last_year())
        assert p.lapse_rate_base_py(500) == p.lapse_rate_base_py(
            model.Data.lapse_last_year())
        assert p.coi_rate_guar_at(500) == p.coi_rate_guar_at(p.coi_rate_last_year())
        data = model.Data
        assert [p.corridor_factor_at(a) for a in (0, 17, 18)] == [2.5] * 3
        assert p.corridor_factor_at(500) == p.corridor_factor_at(data.corridor_age_last())
        assert p.mort_rate_base_at(0) == p.mort_rate_base_at(data.mort_age_first())
        coi, last = data.coi_rate_array(), data.coi_rate_last_years()
        assert np.isnan(coi[0]).all() and np.isnan(coi[:, 0]).all() and last[0] == 0
        for s in range(1, data.coi_schedules() + 1):
            assert not np.isnan(coi[s, 1:last[s] + 1]).any(), s
            assert np.isnan(coi[s, last[s] + 1:]).all(), s
        for array, first in ((data.prem_persistency_array(), 1),
                             (data.lapse_rate_array(), 1),
                             (data.corridor_factor_array(), data.corridor_age_first()),
                             (data.mort_table_array(), data.mort_age_first())):
            assert np.isnan(array[:first]).all() and not np.isnan(array[first:]).any()
        assert first == 18
    finally:
        model.close()
    unscaled = _set("age_at_entry", [label], 36)(extract)
    for cease in (None, 36):
        model = mx.read_model(_sec_inputs(tmp_path / f"unscaled{cease}", unscaled),
                              name=_name("unscaled"))
        try:
            if cease is not None:
                model.Projection.charges_cease_age = cease
            p = _point(model, label)
            assert p.coi_schedule() == 0
            if cease is None:
                _refused_exactly(p.result_cf, f"point_id {label}: {NO_SCALE}")
                continue
            assert len(p.result_cf()) == p.proj_len() == 12 * (121 - 36 + 1) + 25
            assert not p.cells["coi_rate_guar_at"].keys()
        finally:
            model.close()
    model = mx.read_model(_sec_inputs(tmp_path / "unsorted", extract,
                                      {"scenario_table.csv": _scenarios_unsorted}),
                          name=_name("scenarios"))
    try:
        data = model.Data
        written = pd.read_csv(data.input_dir() / "scenario_table.csv")
        assert list(dict.fromkeys(written["scenario_id"])) == ["WE", "MID", "LEVEL6"]
        assert data.scenario_count() == 3
        returns, firsts, lasts = (data.gross_return_array(), data.scenario_first_mths(),
                                  data.scenario_last_mths())
        assert np.isnan(returns[0]).all() and (firsts[0] == 0).all()
        assert (lasts[0] == -1).all()
        ids = list(data.subaccounts())
        for s in range(1, 4):
            for k in range(len(ids)):
                held = returns[s, k]
                assert not np.isnan(held[firsts[s, k]:lasts[s, k] + 1]).any(), (s, k)
                assert np.isnan(held[:firsts[s, k]]).all(), (s, k)
                assert np.isnan(held[lasts[s, k] + 1:]).all(), (s, k)
        numbers = dict(zip(extract.index, data.scenario_index()))
        for point, scenario in extract["scenario_id"].items():
            s = numbers[point]
            assert s == {"LEVEL6": 1, "WE": 3}[scenario], (point, s)
            mine = written[written["scenario_id"] == scenario]
            for k, sa in enumerate(ids):
                path = mine[mine["subaccount_id"] == sa].set_index("t")["gross_return_mth"]
                assert (firsts[s, k], lasts[s, k]) == (path.index.min(), path.index.max())
                assert np.array_equal(returns[s, k, path.index.to_numpy()],
                                      path.to_numpy()), (point, sa)
        we = extract.index[extract["scenario_id"] == "WE"][0]
        p = _point(model, we)
        _refused_exactly(lambda: p.gross_return_mth(2, _sa(p, 2)),
                         f"point_id {we}: scenario_table.csv has no return for "
                         f"subaccount_id 2 at t 2")
        assert p.gross_return_mth(3, _sa(p, 2)) == returns[3, _sa(p, 2), 3]
    finally:
        model.close()


# Far months in the return scenario, as (case, the scenario edit): a scenario no point
# names, of one row at a month a billion months on, and LEVEL6, the scenario of every
# committed point but two, held to month 3,000, past every frame, each month its own
# return.  Neither may make Data's return array any longer than the months a frame reads.
FAR_MONTH = 10 ** 9


def _far_scenario(rows):
    """S's scenario table and ``ZFAR``, a scenario of one row at :data:`FAR_MONTH`, whose
    id sorts last, so that the shipped scenarios keep their numbers."""
    far = pd.DataFrame({"scenario_id": "ZFAR", "subaccount_id": [1, 2], "t": FAR_MONTH,
                        "gross_return_mth": [0.25, -0.25], "provenance": "test copy"})
    return pd.concat([rows, far], ignore_index=True)


def _long_scenario(rows):
    """S's scenario table with ``LEVEL6`` held to month 3,000, its months its own."""
    held = rows[rows["scenario_id"] != "LEVEL6"]
    level = pd.DataFrame([("LEVEL6", i, t, round(0.0048675506 + 1e-7 * t * i, 10),
                           "test copy") for i in (1, 2) for t in range(3001)],
                         columns=list(rows.columns))
    return pd.concat([held, level], ignore_index=True)


def test_a_far_month_of_the_return_scenario_allocates_nothing_and_projects_as_s(
        sec_model, tmp_path):
    """A scenario month far past every frame adds nothing to ``Data``'s return array.

    ``Data.gross_return_array`` holds the months a frame reads, to
    ``Data.return_horizon_mth``, 1,585, the last month a compiled cache keyed by ``t``
    holds: an array to the table's last month would allocate a billion months for each
    scenario and subaccount on a table of a few lines.  So, beside the shipped scenarios,
    a scenario no point names, of one row a billion months on (:func:`_far_scenario`),
    leaves the array as it was, its new row all NaN, and every committed point projects
    exactly what it projects on the shipped table.  And ``LEVEL6`` written to month 3,000,
    each month a return of its own (:func:`_long_scenario`), is held to month 1,585, the
    array no longer, its last month given as 1,585: every month a frame reads, to the
    month after the contract's longest, 1,584, is the table's own, and the committed
    points read the months they read on the table as written, as ``VUL_US_S`` reads them.
    A month past the horizon, which no frame reads, is refused, naming the point and the
    scenario's number, rather than answered with the horizon's return.  And ``ZLATE``, a
    scenario whose months start past the horizon, at 1,590 (:func:`_late_scenario`), holds
    nothing in the array, its last month falling below its first; on a point that names
    it, a month before its first is refused, as ``VUL_US_S``'s lookup raised there, and so
    is every month from its first on, which would otherwise read the padding.
    """
    reach = sec_model.Data.return_horizon_mth
    shipped = sec_model.Data.gross_return_array()
    far = _read(_sec_inputs(tmp_path / "far", _committed(),
                            {"scenario_table.csv": _far_scenario}), "far")
    try:
        held = far.Data.gross_return_array()
        assert held.shape == (shipped.shape[0] + 1, *shipped.shape[1:]), held.shape
        assert np.isnan(held[3]).all()
        assert np.array_equal(held[:3], shipped, equal_nan=True)
        for key in point_keys(far):
            mine, base = projection(far, key), projection(sec_model, key)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (key, report)
            _release(far, key)
    finally:
        far.close()
    long = _read(_sec_inputs(tmp_path / "long", _committed(),
                             {"scenario_table.csv": _long_scenario}), "long")
    try:
        data = long.Data
        written = pd.read_csv(data.input_dir() / "scenario_table.csv").set_index(
            ["scenario_id", "subaccount_id", "t"])["gross_return_mth"]
        assert data.gross_return_array().shape == (3, 2, reach + 1)
        assert (data.scenario_last_mths()[1] == reach).all()
        later = _label(_committed(), "future", 3, -25)
        p = _point(long, later)
        for i, sa in enumerate((1, 2)):
            for t in (0, 25, 1584, reach):
                assert p.gross_return_mth(t, i) == written[("LEVEL6", sa, t)], (t, sa)
            for t in (reach + 1, 3000):
                _refused_exactly(lambda: p.gross_return_mth(t, i),
                                 f"point_id {later}: {_PAST_HORIZON.format(reach, 1)} "
                                 f"{sa} at t {t}")
        assert len(p.result_cf()) == p.proj_len()
    finally:
        long.close()
    late_point = _committed().loc[[later]].assign(scenario_id="ZLATE")
    late = _read(_sec_inputs(tmp_path / "late", late_point,
                             {"scenario_table.csv": _late_scenario}), "late")
    try:
        data = late.Data
        s = list(data.scenario_index())[0]
        assert s == 3
        assert list(data.scenario_first_mths()[s]) == [LATE_FIRST] * 2
        assert (data.scenario_last_mths()[s] < LATE_FIRST).all()
        assert np.isnan(data.gross_return_array()[s]).all()
        p = _point(late, later)
        for i, sa in enumerate((1, 2)):
            _refused_exactly(lambda: p.gross_return_mth(reach, i),
                             f"point_id {later}: scenario_table.csv has no return for "
                             f"subaccount_id {sa} at t {reach}")
            for t in (LATE_FIRST, LATE_FIRST + 5):
                _refused_exactly(lambda: p.gross_return_mth(t, i),
                                 f"point_id {later}: {_PAST_HORIZON.format(reach, s)} "
                                 f"{sa} at t {t}")
    finally:
        late.close()


# The refusal of a return past Data.return_horizon_mth, to the subaccount's id: the
# scenario is named by its number, scenario_index(), since no projection cell may read the
# label scenario_id(), even to refuse (R17).
_PAST_HORIZON = ("scenario_table.csv is read to return_horizon_mth, {}, so its scenario "
                 "{}, in the order of the ids, has no return for subaccount_id")

# The first month of _late_scenario's path, past Data.return_horizon_mth.
LATE_FIRST = 1590


def _late_scenario(rows):
    """S's scenario table and ``ZLATE``, a path from :data:`LATE_FIRST` to month 1,600,
    past ``Data.return_horizon_mth``, whose id sorts last."""
    late = pd.DataFrame([("ZLATE", i, t, 0.001 * i, "test copy") for i in (1, 2)
                         for t in range(LATE_FIRST, 1601)], columns=list(rows.columns))
    return pd.concat([rows, late], ignore_index=True)


# What Data cannot number or join, refused when the vector is first read, naming every
# point at fault (the Data docstring): a label that is not a whole number, or one of 2**53
# or more in size, which numpy would read as the least int64 once past int64; a rate_class
# the class factors lack; a scenario_id the return scenario lacks, or one without a row for
# a subaccount of the lineup; and, on a point that has_surr_charge, a surr_charge_id the
# schedules lack, or a run-off of 2**53 years or more, the bound of every number read as an
# int, past which lapse_shock_month's compiled int() would in time raise OverflowError.
# The surrender-charge cases leave the charge on points 4 and 6 alone, so that the message
# names those two and not the table; a point without a charge projects whatever its
# schedule, which _a_schedule_no_charged_point_reads holds.  The class and scenario joins
# refuse the table: every point reads its class factor and every subaccount's return in
# its first month on the books.  Each case is (case, the table's edit, the schedules'
# run-off or None, the scenario edit or None, the Data cell asked, the message, the label
# whose projection meets it): a label's refusal is met by that point's own point_id(),
# which every refusal names it by; a table's by point 1's result_cf(); and the schedules'
# by point 4's, which has a charge.
_CHARGED = (4, 6)
_NO_CLASS = "class_factor_table.csv has no factor for the rate_class of point_id [3, 6]"
_NO_SCENARIO = ("scenario_table.csv has no returns for every subaccount of the lineup on "
                "the scenario_id of point_id {}")
_NO_SCHEDULE = ("surr_charge_table.csv has no schedule for the surr_charge_id of point_id "
                "[6], each of which has_surr_charge")
_RUNOFF_HUGE = ("surr_charge_table.csv: runoff_years must be below 2**53 years in size on "
                "the schedule of point_id [4, 6], each of which has_surr_charge")


def _charged_only(points, edit=None):
    """An edit that leaves the surrender charge on ``points`` alone, after ``edit``."""
    def charged(table):
        table = table if edit is None else edit(table)
        return table.assign(has_surr_charge=table.index.isin(points))
    return charged


def _relabelled(label, new):
    """An edit that labels the table's row ``label`` ``new``, a label as written."""
    return lambda table: table.rename(index={label: new})


def _no_bond_on_we(rows):
    """S's scenario table without ``WE``'s rows for subaccount 2."""
    return rows[~((rows["scenario_id"] == "WE") & (rows["subaccount_id"] == 2))]


UNJOINED = [
    ("a label that is not whole", _relabelled(4, 4.5), None, None, "point_id",
     f"{TABLE}: point_id must be a whole number; [4.5] is not", 4.5),
    ("a label written as text", _relabelled(4, "4x"), None, None, "point_id",
     f"{TABLE}: point_id must be a whole number; ['4x'] is not", "4x"),
    ("a label of 2**53", _relabelled(4, 2 ** 53), None, None, "point_id",
     f"{TABLE}: point_id must be below 2**53 in size; [{2 ** 53}] is not", 2 ** 53),
    ("a class the table lacks, at two points", _set("rate_class", [3, 6], "SuperPNT"),
     None, None, "class_factor", _NO_CLASS, 1),
    ("a scenario the table lacks, at two points", _set("scenario_id", [3, 7], "CRASH"),
     None, None, "scenario_index", _NO_SCENARIO.format([3, 7]), 1),
    ("a scenario without a row for subaccount 2", lambda table: table, None,
     {"scenario_table.csv": _no_bond_on_we}, "scenario_index",
     _NO_SCENARIO.format([1, 2]), 1),
    ("a schedule the table lacks, on a point with a charge",
     _charged_only(_CHARGED, _set("surr_charge_id", [6, 7], "VUL5")), None, None,
     "surr_charge_rate_max", _NO_SCHEDULE, 4),
    ("a schedule the table lacks, by the run-off's vector",
     _charged_only(_CHARGED, _set("surr_charge_id", [6, 7], "VUL5")), None, None,
     "surr_charge_runoff_years", _NO_SCHEDULE, 4),
    ("a run-off of 2**53 years", _charged_only(_CHARGED), 2.0 ** 53, None,
     "surr_charge_runoff_years", _RUNOFF_HUGE, 4),
    ("a run-off of 2**53 years, by the rate's vector", _charged_only(_CHARGED), 2.0 ** 53,
     None, "surr_charge_rate_max", _RUNOFF_HUGE, 4),
]


def _unjoined_edits(runoff, scenarios):
    """The edits of an :data:`UNJOINED` case: the schedules' run-off and the scenario."""
    edits = dict(scenarios or {})
    if runoff is not None:
        edits["surr_charge_table.csv"] = lambda table: table.assign(runoff_years=runoff)
    return edits or None


@pytest.mark.parametrize("case, edit, runoff, scenarios, cell, message, label", UNJOINED,
                         ids=[c[0] for c in UNJOINED])
def test_what_data_cannot_number_or_join_is_refused_naming_it(tmp_path, case, edit, runoff,
                                                             scenarios, cell, message,
                                                             label):
    """``Data`` refuses what it cannot number or join, naming every point at fault.

    ``VUL_US_S`` reads a point's class factor and every subaccount's return in its first
    month on the books, and the schedule of a point with a surrender charge in every month
    of its cover, so it fails every projection of a point whose class, scenario or charged
    schedule the tables lack, and this model refuses the table at the first read instead
    (:data:`UNJOINED`), in the vector's own cell and in a projection, with the message
    matched whole.  A label is read by no projection but in a refusal, which names the
    point by ``point_id()``, so that cell refuses it.  The message names every point at
    fault and no other.
    """
    model = mx.read_model(_sec_inputs(tmp_path, edit(_committed()),
                                      _unjoined_edits(runoff, scenarios)),
                          name=_name("unjoined"))
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_exactly(model.Data.cells[cell], message)
        call = "point_id" if cell == "point_id" else "result_cf"
        _refused_exactly(_point(model, label).cells[call], message)
    finally:
        model.close()


def test_a_schedule_no_charged_point_reads_is_accepted(tmp_path):
    """A schedule no point with a charge reads may be missing, or run off over 2**53 years.

    ``VUL_US_S`` reads a point's schedule only if it ``has_surr_charge``, so a point without
    one projects whatever its ``surr_charge_id`` names, as it does in ``VUL_US_S``.  With
    the charge off on every point, the schedule run off over ``2**53`` years, and the twin
    of S's point 2 naming a schedule the table lacks, the table reads; both join vectors
    read the schedule, 18.0 and ``2**53``, at every point but that one, which is NaN with a
    ``has_surr_charge_schedule`` of 0; and every point projects exactly what it projects on
    the committed schedule with the charge off.  The joins refuse a charged point alone
    (:data:`UNJOINED`).
    """
    committed = _committed()
    lost = _label(committed, "twin", 2, 0)
    uncharged = _charged_only([])(committed)
    base = mx.read_model(_sec_inputs(tmp_path / "base", uncharged), name=_name("uncharged"))
    model = mx.read_model(_sec_inputs(tmp_path / "huge",
                                      _set("surr_charge_id", [lost], "VUL5")(uncharged),
                                      _unjoined_edits(2.0 ** 53, None)),
                          name=_name("runoff_huge"))
    try:
        assert len(model.Data.model_point_table()) == len(committed)
        lost_at = list(committed.index).index(lost)
        for cell, value in (("surr_charge_rate_max", 18.0),
                            ("surr_charge_runoff_years", 2.0 ** 53)):
            want = np.full(len(committed), value)
            want[lost_at] = np.nan
            assert np.array_equal(model.Data.cells[cell](), want, equal_nan=True), cell
        flags = model.Data.has_surr_charge_schedule()
        assert flags.dtype == np.int64 and flags.tolist() == [
            int(i != lost_at) for i in range(len(committed))]
        for label in committed.index:
            mine, theirs = _point(model, label), _point(base, label)
            for report in REPORTS:
                assert frame_mismatches(theirs.cells[report](), mine.cells[report](),
                                        rtol=0, atol=0) == [], (label, report)
            _release(model, _key(model, label))
            _release(base, _key(base, label))
    finally:
        model.close()
        base.close()


# Points without a surrender charge, as (point_id, the surr_charge_id written, the charge
# and the run-off their accessors read, or None where the table lacks the id).  Each is the
# value bc8ce29's model, VUL_US_SEC at stage E, read there, its .loc reading the schedule
# of a point with a charge or without, and raising KeyError on an id the table lacks: SC7,
# a second schedule the copy adds; HUGE, a third, run off over 2**53 years, which only a
# point with a charge is refused; VUL14 as shipped; VUL5, which no table has; and a blank
# id.
UNCHARGED = ((3, "SC7", (9.5, 7.0)), (5, "HUGE", (3.0, 2.0 ** 53)),
             (6, "VUL14", (18.0, 14.0)), (7, "VUL5", None), (8, None, None))
_NO_ID = ("KeyError: 'point_id {}: surr_charge_table.csv has no schedule for its "
          "surr_charge_id'")


def _surr_charges_with_sc7(table):
    """The shipped schedules with SC7, $9.50 per $1,000 over 7 years, and HUGE, $3.00 per
    $1,000 over ``2**53`` years."""
    added = pd.DataFrame([
        {"surr_charge_id": "SC7", "sc_per_1000_init": 9.5, "runoff_years": 7,
         "provenance": "test copy"},
        {"surr_charge_id": "HUGE", "sc_per_1000_init": 3.0, "runoff_years": 2.0 ** 53,
         "provenance": "test copy"}])
    return pd.concat([table, added], ignore_index=True)


def _uncharged():
    """The committed table with :data:`UNCHARGED`'s points uncharged on their ids."""
    table = _committed()
    for point, label, _ in UNCHARGED:
        table = _set("has_surr_charge", [point], False)(_set("surr_charge_id", [point],
                                                             label)(table))
    return table


def test_a_point_without_a_charge_reads_its_schedule_as_at_stage_e(tmp_path):
    """On a point without a charge, the two schedule accessors read what they read at E.

    No cell reads ``surr_charge_rate_max`` or ``surr_charge_runoff_years`` on a point
    without a charge, since ``surr_charge_rate`` returns 0.0 and ``lapse_shock_month`` -1
    first, but each is a cell, and Phase 2 moves no number (D2): so each reads the point's
    schedule wherever the table holds its id, a run-off of ``2**53`` years included, and
    raises ``KeyError`` where it does not, naming the point, as the ``.loc`` of the model
    at stage ``E`` did (:data:`UNCHARGED`, pinned to bc8ce29's values).  ``Data`` joins
    the schedule wherever it can, NaN and a ``has_surr_charge_schedule`` of 0 where it
    cannot, and refuses no point without a charge, which projects as ``VUL_US_S`` projects
    it, its schedule unread.
    """
    folder = _sec_inputs(tmp_path, _uncharged(),
                         edits={"surr_charge_table.csv": _surr_charges_with_sc7})
    model = _read(folder, "uncharged")
    try:
        for point, label, want in UNCHARGED:
            p = _point(model, point)
            have = p.surr_charge_id()
            assert not p.has_surr_charge() and (have == label if label else have != have)
            assert len(p.result_cf()) == p.proj_len() and p.surr_charge_rate(0) == 0.0
            assert p.lapse_shock_month() == -1
            cells = (p.cells["surr_charge_rate_max"], p.cells["surr_charge_runoff_years"])
            if want is None:
                for cell in cells:
                    with pytest.raises(Exception) as excinfo:
                        cell()
                    assert _raised(excinfo.value) == _NO_ID.format(point)
            else:
                assert [(type(v), v) for v in (cell() for cell in cells)] == [
                    (float, want[0]), (float, want[1])]
            _release(model, _key(model, point))
        known = dict(zip(model.Data.model_point_table().index,
                         model.Data.has_surr_charge_schedule()))
        assert [known[point] for point, _, _ in UNCHARGED] == [1, 1, 1, 0, 0]
    finally:
        model.close()


# A point the contract does not issue, refused by proj_len() in its rules' order, as (case,
# the table's edit, the inputs' edits, the References set, the label, the message, and,
# where it projects once its bound is moved, the References that move it and its frame
# then).  The first rule, issued above omega_age, is asked before the cover's, so a point to
# be issued there, or in force there, is refused as never in cover; the cover's before the
# issue ages', so a point issued at 86 and past its cover is refused as past it.  The issue
# age of 86 projects once issue_age_max is 86, on a COI copy with rows of its own
# (_coi_at); the point refused at an issue_age_min raised to 46 projects at the shipped 0;
# and the lineup of ten, every point's, projects once subaccount_max is 10
# (_ten_subaccounts).  PAST_COVER's two cases, the cover's rule alone, are its own test's,
# with the block run.
_ABOVE_OMEGA = ("point_id {}: age_at_entry 122 is above omega_age, 121: a policy issued "
                "there would never be in cover")


def _coi_at(age):
    """An edit of the COI scale that adds ``(M, StdNT, age)``, geometric in the year."""
    def edit(rates):
        years = list(range(1, 122 - age + 1))
        added = pd.DataFrame({
            "sex": "M", "rate_class": "StdNT", "age_at_entry": age, "policy_year": years,
            "coi_rate_guar": [round(0.9 * 1.08 ** (y - 1), 6) for y in years],
            "provenance": "test copy"})
        return pd.concat([rates, added], ignore_index=True)
    return edit


# The ten subaccounts of _ten_subaccounts, by id.
TEN = tuple(range(1, 11))


def _ten_subaccounts(table):
    """A lineup of ten, and the table's columns for it: the inputs' edits and the table.

    Subaccounts 3 to 10 join the shipped two, each with a fund expense and a path in every
    scenario of its own, and each point holds none of them, its premium allocated as
    shipped, so that the lineup alone is past ``subaccount_max``.
    """
    def lineup(rows):
        more = pd.DataFrame({"subaccount_id": TEN[2:], "subaccount_name": "test copy",
                             "fund_expense_ann": [0.001 * i for i in TEN[2:]],
                             "provenance": "test copy"})
        return pd.concat([rows, more], ignore_index=True)

    def scenarios(rows):
        more = [rows[rows["subaccount_id"] == 1].assign(
            subaccount_id=i, gross_return_mth=rows["gross_return_mth"] + 0.0001 * i)
            for i in TEN[2:]]
        return pd.concat([rows, *more], ignore_index=True)

    table = table.assign(**{f"{column}_{i}": 0.0 for i in TEN[2:]
                            for column in ("alloc", "sa_pp_init")})
    return table, {"subaccount_table.csv": lineup, "scenario_table.csv": scenarios}


def _not_issued_cases():
    """:data:`NOT_ISSUED`'s inputs, as (case, the table, the edits, the References set,
    the label, the message, the References that issue it or None, its frame then)."""
    committed = _committed()
    ten, ten_edits = _ten_subaccounts(committed)
    return [
        ("an issue age of 86", _set("age_at_entry", [3], 86)(committed),
         {"coi_rates.csv": _coi_at(86)}, {}, 3,
         "point_id 3: issue age 86 is above issue_age_max, 85", {"issue_age_max": 86},
         12 * (121 - 86 + 1)),
        ("an issue age below a bound raised to 46", committed, None, {"issue_age_min": 46},
         3, "point_id 3: issue age 45 is below issue_age_min, 46", {}, 12 * (121 - 45 + 1)),
        ("to be issued above omega_age", _set("age_at_entry", [9], 122)(committed), None,
         {}, 9, _ABOVE_OMEGA.format(9), None, None),
        ("in force above omega_age: the first rule before the cover's",
         _set("age_at_entry", [4], 122)(committed), None, {}, 4, _ABOVE_OMEGA.format(4),
         None, None),
        ("issued at 86 and past its cover: the cover's rule before the bound's",
         _moved(4, 432, age_at_entry=86)(committed), None, {}, 4,
         "point_id 4: duration_mth 432 is at or past the end of the projection, policy "
         "month 432, attained age 122", None, None),
        ("a lineup of ten subaccounts", ten, ten_edits, {}, 1,
         "point_id 1: the subaccount lineup holds 10 subaccounts, above subaccount_max, 9",
         {"subaccount_max": 10}, 900),
    ]


NOT_ISSUED = _not_issued_cases()


@pytest.mark.parametrize("case, table, edits, refs, label, message, issue, frame",
                         NOT_ISSUED, ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, table,
                                                                    edits, refs, label,
                                                                    message, issue, frame):
    """``proj_len()`` refuses a point the contract does not issue, naming it (§6.1).

    ``VUL_US_S`` projects a point issued at any age its tables serve, on any lineup, and so
    would modelx here, but the compiled caches are sized from the contract, cover from
    ``issue_age_min``, 0, to attained age 122, the shipped horizon and a lineup of up to
    ``subaccount_max``, 9 (``spec_sec.py``), and a point past them runs past the caches.
    So the frame refuses such a point, naming it: issued above ``issue_age_max``, 85, the
    oldest age ``product-spec.md`` issues at, which no cache needs; issued below
    ``issue_age_min``; issued above ``omega_age``, which ``VUL_US_S`` projects as months in
    which nothing happens; or on a lineup past ``subaccount_max``, each by the rule asked
    first (:data:`NOT_ISSUED`).  The table reads, since these are rules of the product,
    and every report is refused with the frame.  The point issued at 86 projects once
    ``issue_age_max`` is 86, the one refused at a bound of 46 projects at the shipped 0,
    and the lineup of ten once ``subaccount_max`` is 10: the Reference is what refuses
    each, and a bound off by one, or a refusal lost or asked in another order, lets a point
    through or names the wrong rule.
    """
    model = _read(_sec_inputs(tmp_path, table, edits), "not_issued", refs)
    try:
        assert len(model.Data.model_point_table()) == len(table)
        for report in REPORTS:
            _refused_exactly(_point(model, label).cells[report], message)
    finally:
        model.close()
    if issue is None:
        return
    model = _read(_sec_inputs(tmp_path / "issued", table, edits), "issued", issue)
    try:
        p = _point(model, label)
        assert p.proj_len() == len(p.result_cf()) == frame
        assert p.check_av_roll_fwd() and p.check_margin() and p.check_net_view()
    finally:
        model.close()


# run_sec.py run as though it sat at /m/products/variable_ul, a copy too shallow to have a
# repository above it: the source compiled under that name, so that its own __file__ is
# it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/variable_ul/run_sec.py"
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


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: a cold ``net_cf`` in the last month of
    the longest frame, issue age 0 issued 120 months on, needs a limit of 2,994 in the
    export, and the reports the sample runs in ascending ``t`` with the behaviour module
    on, the export's import among the frames they run under, 1,834.  The limit is four
    times the first, rounded up to the thousand.  No build can tell a lower limit above
    the reports' need: a limit of 2,000 builds the same model.  So this holds the limit,
    read from the sample's code, to the value derived from its comment's need, and holds
    the call before the import of the export.  A change to the need is measured again and
    written in the comment.
    """
    source = (model_path(SEC).parent / "sample_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    need = re.search(r"needs a limit of ([\d,]+) in the export", comment)
    reports = re.search(r"ascending t with the module on, need ([\d,]+)", comment)
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


def _references(space):
    """The References a space's ``__init__.py`` assigns, a name to a literal value."""
    source = (model_path(SEC) / space / "__init__.py").read_text(encoding="utf-8")
    return {node.targets[0].id: node.value.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)}


# The codes, in their numbering's order: the timings, the count's three and the account
# value's six, one numbering; and the kinds.
TIMING_CODES = ("BEF_NB", "BEF_DECR", "BEF_MAT", "BEF_PREM", "BEF_WD", "BEF_FEE", "BEF_INV",
                "BEF_ME", "EOM")
KIND_CODES = ("DEATH", "LAPSE", "MATURITY", "WITHDRAWAL")


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size one below the comment's, which drops the headroom and reads the same numbers.
    So this reads the spec as mx2cy does, and the bounds of the contract from the model's
    own References, and holds each size to the comment's derivation from them: ``t`` to
    ``12 * (omega_age - issue_age_min + 1) + the horizon + 2``, ``m`` to
    ``12 * (omega_age - issue_age_min + 1) + 1``, ``y`` to ``omega_age - issue_age_min +
    3``, ``a`` to ``omega_age + 2`` and ``i`` to ``subaccount_max``; every dimension after
    the first to one width, the widest of the timings' count, the kinds' and
    ``subaccount_max``, the 2-D caches ``(N, width)`` and the 3-D ``(N, width, width)``
    (§7.2, *For M16 and later*, item 16); the codes dense from 0; and
    ``Data.return_horizon_mth``, the last month the return array holds, to ``t``'s last
    index.  A change to a bound or a size is derived again in the comment and here.
    """
    source = (model_path(SEC).parent / "spec_sec.py").read_text(encoding="utf-8")
    comment = " ".join(line.lstrip("# ") for line in source.splitlines()
                       if line.startswith("#"))
    for formula in ("needs t raised to 12 * (omega_age - issue_age_min + 1) + the "
                    "horizon + 2", "needs m raised to 12 * (omega_age - issue_age_min + "
                    "1) + 1", "needs y raised to omega_age - issue_age_min + 3",
                    "needs a raised to omega_age + 2",
                    "needs i and the width raised to it"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    low, omega, horizon = proj["issue_age_min"], proj["omega_age"], data[
        "future_horizon_mth"]
    lineup = proj["subaccount_max"]
    timings = [proj[code] for code in TIMING_CODES]
    kinds = [proj[code] for code in KIND_CODES]
    assert timings == list(range(len(timings))), timings
    assert kinds == list(range(len(kinds))), kinds
    t = 12 * (omega - low + 1) + horizon + 2
    m = 12 * (omega - low + 1) + 1
    width = max(len(timings), len(kinds), lineup)
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     ("t", "i"): (t, width), ("t", "i", "timing"): (t, width, width),
                     "m": m, ("m", "timing"): (m, width), ("m", "i"): (m, width),
                     ("m", "i", "timing"): (m, width, width), "i": lineup,
                     "y": omega - low + 3, "a": omega + 2}, sizes
    assert data["return_horizon_mth"] == t - 1, data["return_horizon_mth"]


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
    exactly.  ``python tools/gen_sec_fingerprint.py VUL_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# VUL_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: VUL_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 900, "months": (0, 224, 449, 674, 899),
        "result_cf": {
            "pols_if": (247.94551551192222, 1.0, (
                1.0, 0.4825291491169639, 0.18055436093150787, 0.009332941134936589, 0.0)),
            "premiums": (123972.7577559611, 500.0, (
                500.0, 241.26457455848194, 90.27718046575393, 4.666470567468294, 0.0)),
            "claims_death": (224826.37928794656, 646.0023939721268, (
                73.6429601961297, 165.95293805317922, 460.8147986380339, 350.09186251570924,
                0.0)),
            "claims_lapse": (152549.59455723898, 300.18315603456324, (
                145.30229633962662, 268.3054222468719, 276.4281988149108,
                36.137701286070644, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1549.6594719495138, 6.25, (
                6.25, 3.015807181981024, 1.128464755821924, 0.05833088209335368, 0.0)),
            "premium_taxes": (2479.455155119222, 10.0, (
                10.0, 4.825291491169639, 1.8055436093150785, 0.09332941134936588, 0.0)),
            "net_cf": (-257432.3307162932, 791.943593426434, (
                264.80474346424364, -200.83488441471982, -649.8998253523278,
                -381.7147535277543, 0.0)),
        },
        "result_pols": {
            "pols_if": (247.94551551192222, 1.0, (
                1.0, 0.4825291491169639, 0.18055436093150787, 0.009332941134936589, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.30214778625655514, 0.0007430700553498427, (
                0.0001472859203922594, 0.00033190587610635843, 0.0006945980173662265,
                0.00022371206569285053, 0.0)),
            "pols_lapse": (0.6978522137434444, 0.0033955530080964553, (
                0.0033955530080964553, 0.001222393453073608, 0.00045595324266049005,
                2.30923385251072e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (54.42304987432867, 1.0, (
                0.0001472859203922594, 0.0006878462714920985, 0.0038470298572833572,
                0.023970157151791627, 1.0)),
            "lapse_rate_mth": (2.3642001926207827, 0.003396053198917559, (
                0.003396053198917559, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    2: {"rows": 900, "months": (0, 224, 449, 674, 899),
        "result_cf": {
            "pols_if": (247.94551551192222, 1.0, (
                1.0, 0.4825291491169639, 0.18055436093150787, 0.009332941134936589, 0.0)),
            "premiums": (123972.7577559611, 500.0, (
                500.0, 241.26457455848194, 90.27718046575393, 4.666470567468294, 0.0)),
            "claims_death": (224750.90329483256, 645.7107000457024, (
                73.6429601961297, 165.95293805317922, 460.5958331069763, 349.93963061455935,
                0.0)),
            "claims_lapse": (152472.24899542448, 300.03481336826184, (
                145.1649104423321, 268.1781179595744, 276.29684832978813, 36.12198737906797,
                0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1549.6594719495138, 6.25, (
                6.25, 3.015807181981024, 1.128464755821924, 0.05833088209335368, 0.0)),
            "premium_taxes": (2479.455155119222, 10.0, (
                10.0, 4.825291491169639, 1.8055436093150785, 0.09332941134936588, 0.0)),
            "net_cf": (-257279.50916136464, 791.5652750462812, (
                264.9421293615382, -200.7075801274224, -649.5495093361476,
                -381.5468077196017, 0.0)),
        },
        "result_pols": {
            "pols_if": (247.94551551192222, 1.0, (
                1.0, 0.4825291491169639, 0.18055436093150787, 0.009332941134936589, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.30214778625655514, 0.0007430700553498427, (
                0.0001472859203922594, 0.00033190587610635843, 0.0006945980173662265,
                0.00022371206569285053, 0.0)),
            "pols_lapse": (0.6978522137434444, 0.0033955530080964553, (
                0.0033955530080964553, 0.001222393453073608, 0.00045595324266049005,
                2.30923385251072e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (54.42304987432867, 1.0, (
                0.0001472859203922594, 0.0006878462714920985, 0.0038470298572833572,
                0.023970157151791627, 1.0)),
            "lapse_rate_mth": (2.3642001926207827, 0.003396053198917559, (
                0.003396053198917559, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    3: {"rows": 924, "months": (0, 230, 461, 692, 923),
        "result_cf": {
            "pols_if": (243.37424415156346, 1.0, (
                1.0, 0.4549665359822978, 0.1731324746839645, 0.009664118427764753, 0.0)),
            "premiums": (121687.12207578172, 500.0, (
                500.0, 227.4832679911489, 86.56623734198226, 4.832059213882377, 0.0)),
            "claims_death": (148379.2779099692, 427.6540928795547, (
                62.83307018692546, 170.6763719347242, 403.7547252173157, 1.7661678479391487,
                -0.0)),
            "claims_lapse": (44063.42412961595, 118.34070469777345, (
                0.0, 110.65959775427456, 72.04919512290708, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1521.0890259472717, 6.25, (
                6.25, 2.843540849889361, 1.0820779667747782, 0.06040074017352971, 0.0)),
            "premium_taxes": (2433.7424415156347, 10.0, (
                10.0, 4.549665359822978, 1.731324746839645, 0.09664118427764753, 0.0)),
            "net_cf": (-74710.41143126632, 420.91692981307455, (
                420.91692981307455, -61.245907907562156, -392.0510857118549,
                2.9088494414920514, 0.0)),
        },
        "result_pols": {
            "pols_if": (243.37424415156346, 1.0, (
                1.0, 0.4549665359822978, 0.1731324746839645, 0.009664118427764753, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.27193113808074054, 0.00066148225927469, (
                0.00012558670981566156, 0.00028636703789566625, 0.0006073903726755874,
                0.0002089251865262915, 0.0)),
            "pols_lapse": (0.7280688619192595, 0.005142366937762858, (
                0.005142366937762858, 0.0011526363320215377, 0.00043735947583539063,
                2.3969374519759583e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (54.42618813386194, 1.0, (
                0.00012558670981566156, 0.0006294243977249536, 0.0035082405758036783,
                0.021618649242341137, 1.0)),
            "lapse_rate_mth": (2.477100171933386, 0.005143012831822946, (
                0.005143012831822946, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    4: {"rows": 804, "months": (0, 200, 401, 602, 803),
        "result_cf": {
            "pols_if": (235.35915844730042, 1.0, (
                1.0, 0.5313927872824623, 0.18082290278420488, 0.006632150891573719, 0.0)),
            "premiums": (117679.5792236502, 500.0, (
                500.0, 265.69639364123117, 90.41145139210244, 3.3160754457868595, 0.0)),
            "claims_death": (226048.53474506122, 562.7677226668303, (
                141.13747556737488, 306.7000116070909, 492.6605409861867,
                207.92805488113092, 0.0)),
            "claims_lapse": (124848.25997599248, 286.20370101478244, (
                184.89925895653485, 285.3461637445833, 208.6108372210296,
                17.273010901668346, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1470.9947402956277, 6.25, (
                6.25, 3.3212049205153895, 1.1301431424012804, 0.041450943072335746, 0.0)),
            "premium_taxes": (2353.5915844730043, 10.0, (
                10.0, 5.313927872824624, 1.8082290278420488, 0.0663215089157372, 0.0)),
            "net_cf": (-237041.80182217213, 667.3726742436738, (
                157.71326547609027, -334.98491450378316, -613.7982989853571,
                -221.9927627890005, 0.0)),
        },
        "result_pols": {
            "pols_if": (235.35915844730042, 1.0, (
                1.0, 0.5313927872824623, 0.18082290278420488, 0.006632150891573719, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.40437821004524366, 0.0010500364633632072, (
                0.00028686884969464366, 0.0006253180476054079, 0.0010082106669680182,
                0.00019639520704686105, 0.0)),
            "pols_lapse": (0.5956217899547573, 0.0025343213873569165, (
                0.0025343213873569165, 0.0013455213371534307, 0.0004558389859992721,
                1.6314953527051398e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (54.40383798041241, 1.0, (
                0.00028686884969464366, 0.0011767529830490897, 0.005575680134784822,
                0.0296125963141739, 1.0)),
            "lapse_rate_mth": (2.038179085524697, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    5: {"rows": 912, "months": (0, 227, 455, 683, 911),
        "result_cf": {
            "pols_if": (231.7158955576591, 0.9385843599999996, (
                0.9385843599999996, 0.44217815223453155, 0.16695778466795608,
                0.008982136993247682, 0.0)),
            "premiums": (115857.94777882956, 469.2921799999998, (
                469.2921799999998, 221.08907611726576, 83.47889233397804, 4.491068496623841,
                0.0)),
            "claims_death": (147644.1875334462, 427.6540928795547, (
                64.32965548739351, 167.1106853323286, 388.46659880803566,
                -2.830664047790999, -0.0)),
            "claims_lapse": (44063.42412961596, 118.34070469777345, (
                0.0, 112.50698159740496, 68.83988957786842, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1448.2243472353696, 5.866152249999997, (
                5.866152249999997, 2.7636134514658224, 1.0434861541747256,
                0.056138356207798015, 0.0)),
            "premium_taxes": (2317.1589555765913, 9.385843599999996, (
                9.385843599999996, 4.421781522345316, 1.6695778466795608,
                0.08982136993247682, 0.0)),
            "net_cf": (-79615.04718704453, 413.9198523835308, (
                389.71052866260635, -65.71398578627894, -376.5406600527803,
                7.175772818274564, 0.0)),
        },
        "result_pols": {
            "pols_if": (231.7158955576591, 0.9385843599999996, (
                0.9385843599999996, 0.44217815223453155, 0.16695778466795608,
                0.008982136993247682, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.27046700443894806, 0.00066148225927469, (
                0.0001275863879727851, 0.00027831771715735286, 0.0005857280746184168,
                0.0001941816691036783, 0.0)),
            "pols_lapse": (0.6681173555610519, 0.004002817298416356, (
                0.004002817298416356, 0.0011202375629479312, 0.0004217612514480996,
                2.227789396293e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (54.42468109334416, 1.0, (
                0.00013593491795749202, 0.0006294243977249536, 0.0035082405758036783,
                0.021618649242341137, 1.0)),
            "lapse_rate_mth": (2.4153840179515105, 0.004265318777560645, (
                0.004265318777560645, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    6: {"rows": 798, "months": (0, 199, 398, 597, 797),
        "result_cf": {
            "pols_if": (229.40131745500184, 0.9831917971586217, (
                0.9831917971586217, 0.5215534500096158, 0.17646621929723919,
                0.006419440730999807, 0.0)),
            "premiums": (114700.65872750092, 491.59589857931087, (
                491.59589857931087, 260.77672500480793, 88.23310964861959,
                3.2097203654999036, 0.0)),
            "claims_death": (225207.68983634489, 562.7677226668303, (
                138.75338291608438, 329.38651556894524, 484.0321095102283,
                202.0811900234655, 0.0)),
            "claims_lapse": (123726.56274501319, 286.20370101478244, (
                189.8123484926931, 285.73488419433266, 206.1698776665217,
                16.787299820088844, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1433.7582340937615, 6.144948732241386, (
                6.144948732241386, 3.259709062560099, 1.1029138706077448,
                0.04012150456874879, 0.0)),
            "premium_taxes": (2294.013174550019, 9.831917971586218, (
                9.831917971586218, 5.215534500096159, 1.7646621929723918,
                0.06419440730999808, 0.0)),
            "net_cf": (-237961.36526250094, 667.3726742436738, (
                147.0533004667058, -362.8199183211262, -604.8364535917106,
                -215.7630853899332, 0.0)),
        },
        "result_pols": {
            "pols_if": (229.40131745500184, 0.9831917971586217, (
                0.9831917971586217, 0.5215534500096158, 0.17646621929723919,
                0.006419440730999807, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.4026690910531194, 0.0010500364633632072, (
                0.0002820470998801032, 0.0006716295452774446, 0.0009839191933961986,
                0.0001900963069298627, 0.0)),
            "pols_lapse": (0.5805227061055034, 0.002491723999412978, (
                0.002491723999412978, 0.0013204607369408515, 0.00044485616163112085,
                1.5791690947349813e-05, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (54.40211676731424, 1.0, (
                0.00028686884969464366, 0.0012877482552652308, 0.005575680134784822,
                0.0296125963141739, 1.0)),
            "lapse_rate_mth": (2.022968793841677, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    7: {"rows": 331, "months": (0, 82, 165, 247, 330),
        "result_cf": {
            "pols_if": (3.1887252745537253, 0.055426389287530214, (
                0.055426389287530214, 0.014351739966369056, 0.0011046189139447748,
                4.1983893527370735e-06, 0.0)),
            "premiums": (1594.3626372768622, 27.713194643765107, (
                27.713194643765107, 7.175869983184528, 0.5523094569723874,
                0.0020991946763685367, 0.0)),
            "claims_death": (9968.347658399307, 270.7498105314534, (
                270.7498105314534, 36.47594370284919, -31.718129656485385,
                -1.0817861758117544, -0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (19.92953296596078, 0.34641493304706383, (
                0.34641493304706383, 0.0896983747898066, 0.006903868212154843,
                2.623993345460671e-05, 0.0)),
            "premium_taxes": (31.887252745537243, 0.5542638928753022, (
                0.5542638928753022, 0.14351739966369056, 0.011046189139447748,
                4.198389352737073e-05, 0.0)),
            "net_cf": (-8425.80180683394, 243.93729471361067, (
                -243.93729471361067, -29.533289494118165, 32.252489056106164,
                1.083817146661141, 0.0)),
        },
        "result_pols": {
            "pols_if": (3.1887252745537253, 0.055426389287530214, (
                0.055426389287530214, 0.014351739966369056, 0.0011046189139447748,
                4.1983893527370735e-06, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.04746313706017955, 0.0005494731243651203, (
                0.0005444917347686323, 0.000280204469793121, 4.567260499431345e-05,
                4.5826666906629015e-07, 0.0)),
            "pols_lapse": (0.007963252227350682, 0.00013912827831585536, (
                0.00013912827831585536, 3.5672026555148576e-05, 2.6844803726323442e-06,
                9.481392824818772e-09, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (53.176894477374795, 1.0, (
                0.009823691237472176, 0.019524076554461978, 0.041346933696082666,
                0.10915297047605421, 1.0)),
            "lapse_rate_mth": (0.8391010911799437, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    8: {"rows": 36, "months": (0, 8, 17, 26, 35),
        "result_cf": {
            "pols_if": (4.005982516040756e-10, 4.005982516040756e-10, (
                4.005982516040756e-10, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (2.0029912580203778e-07, 2.0029912580203778e-07, (
                2.0029912580203778e-07, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (0.0008253682799328843, 0.0008253682799328843, (
                0.0008253682799328843, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2.5037390725254722e-09, 2.5037390725254722e-09, (
                2.5037390725254722e-09, 0.0, 0.0, 0.0, 0.0)),
            "premium_taxes": (4.005982516040756e-09, 4.005982516040756e-09, (
                4.005982516040756e-09, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-0.0008251744905286709, 0.0008251744905286709, (
                -0.0008251744905286709, 0.0, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (4.005982516040756e-10, 4.005982516040756e-10, (
                4.005982516040756e-10, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (4.005982516040756e-10, 4.005982516040756e-10, (
                4.005982516040756e-10, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (36.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lapse_rate_mth": (0.09126175009812076, 0.002535048613836688, (
                0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688, 0.002535048613836688)),
        },
    },
    9: {"rows": 949, "months": (0, 237, 474, 711, 948),
        "result_cf": {
            "pols_if": (243.37424415156346, 1.0, (
                0.0, 0.481158679517615, 0.18577261410865942, 0.011187354007285629, 0.0)),
            "premiums": (121687.12207578172, 500.0, (
                0.0, 240.5793397588075, 92.8863070543297, 5.5936770036428145, 0.0)),
            "claims_death": (148379.27790996918, 427.6540928795547, (
                0.0, 149.03413400357258, 396.54079338279513, 12.990154511595334, -0.0)),
            "claims_lapse": (44063.42412961595, 118.34070469777345, (
                0.0, 106.36466840519643, 78.42877497790651, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1521.0890259472717, 6.25, (
                0.0, 3.007241746985094, 1.1610788381791213, 0.06992096254553518, 0.0)),
            "premium_taxes": (2433.7424415156347, 10.0, (
                0.0, 4.81158679517615, 1.8577261410865942, 0.1118735400728563, 0.0)),
            "net_cf": (-74710.41143126632, 420.91692981307455, (
                0.0, -22.638291192122754, -385.1020662856376, -7.5782720105709105, 0.0)),
        },
        "result_pols": {
            "pols_if": (243.37424415156346, 1.0, (
                0.0, 0.481158679517615, 0.18577261410865942, 0.011187354007285629, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.27193113808074054, 0.00066148225927469, (
                0.0, 0.0002537842896276664, 0.0005944512398314605, 0.00024185548223340755,
                0.0)),
            "pols_lapse": (0.7280688619192595, 0.005142366937762858, (
                0.0, 0.0012191172880349867, 0.00046943564509344674, 2.7747370863685147e-05,
                0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "mort_rate_mth": (54.42618813386194, 1.0, (
                0.0, 0.0005274440645695044, 0.0031998862840125764, 0.021618649242341137,
                1.0)),
            "lapse_rate_mth": (2.477100171933386, 0.005143012831822946, (
                0.0, 0.002535048613836688, 0.002535048613836688, 0.002535048613836688,
                0.002535048613836688)),
        },
    },
}
# END generated fingerprint: VUL_US_SEC


# ---------------------------------------------------------------------------
# Compiled (USLIB-SEC-PLAN.md Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython CI job, which sets USLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is VUL's
# own: the comparison on the splice grid, at the contract's extremes, on a lineup of nine,
# where the cap on mortality binds, on labels that are not text and on keys written as
# floats, the refusals, the deepest call, a lapse rate past 1, a Reference set late and the
# runner.  Each comparison but the cap's adds sec_support._vul_c4_also's calls, the codes
# and the pricing path's closes no swept cell reaches.  None asks for sec_read, sec_model
# or s_model, which sweep every committed point; the grid test alone asks for spliced.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _copied(folder, file):
    """An edit that replaces ``file`` with the copy in ``folder``, as written there."""
    return lambda _: pd.read_csv(pathlib.Path(folder) / file)


# How many rows of the splice grid C4 compares at once.  compiled_mismatches sweeps every
# row of its case in one modelx read, _vul_c4_also's calls with it, and keeps every value of
# every row, in the parent and in the child, until it compares them.  A VUL row runs up to
# 1,344 months on the grid, with the behaviour module on, which reads the pricing path from
# issue.  On the core grid, eight rows at a time peaked at 4.6 GB, the module's fixtures and
# the children included, and four at 3.6 GB, near the module's own peak, in 308 s against
# 305 (measured at M17, under load), so VUL compares four rows at a time
# (USLIB-SEC-PLAN.md §7.2, *For M16 and later*, item 7).
C4_CHUNK = 4


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's points, S's restated in force at T2's months and issued later,
    and the variants, withdrawals on either option, a single premium without a surrender
    charge, an Option B point funded past its face, a second surrender-charge schedule
    with a loan, an issue age below the tables' first age whose COI rate reaches its cap,
    each first-month pin alone, the COI pin above the guaranteed rate that bounds it and a
    withdrawal that cuts the face past 0, under the splice's References, with the
    behaviour module on, charges ceasing in cover and the lapse spike
    (:data:`SPLICED_REFS`),
    on the splice's COI, surrender-charge and stepped scenario copies, each row's scenario
    re-based to its month (:func:`_spliced_folders`).  The grid is the one this run's
    ``spliced`` selects, the core by default and the full grid under ``USLIB_SEC_FULL=1``,
    and the test carries no ``sec_full`` mark, since a skipped compile test fails the
    cython job.  The grid's SEC table goes beside the build :data:`C4_CHUNK` rows at a
    time, with the spliced folder's own tables; modelx sweeps every row fully, every
    account cell at every timing and the pricing path at every month with it
    (``sec_support._vul_c4_also``), and the compiled model must agree at every argument
    modelx caches, identically on x86-64 and to 1e-12 relative elsewhere, with every raise
    and every ``Data`` array (``sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    inputs = spliced[1].Data.input_dir()
    table = pd.read_csv(inputs / TABLE, index_col="point_id")
    assert len(table) == len(spliced[1].Data.model_point_table())
    edits = {file: _copied(inputs, file) for file in SPLICED_EDITS}
    chunks = [table.iloc[i:i + C4_CHUNK] for i in range(0, len(table), C4_CHUNK)]
    assert sum(len(chunk) for chunk in chunks) == len(table) and len(chunks) > 1
    found = []
    for i, chunk in enumerate(chunks):
        folder = compiled_case(build, tmp_path / f"grid{i}", model_points=chunk,
                               edits=edits)
        found += compiled_mismatches(build, folder, refs=SPLICED_REFS, also=_vul_c4_also)
        shutil.rmtree(tmp_path / f"grid{i}")
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The References at the contract's extremes: the splice's, inflation on, and the A/E at
# the shipped 1.0, so that StdTob's annual mortality passes 1 and is capped.
EXTREME_REFS = {**SWITCHED_ON, "mort_ae_factor": 1.0}

# The COI keys the contract's extremes read beyond S's, and one no point reads between
# them, each geometric in the policy year from a base of its own at a ratio of its own,
# every policy year its cover reaches, as (sex, rate_class, age_at_entry, base, ratio).
EXTREME_COI = ((("M", "StdNT", 0), 0.031, 1.064), (("M", "StdNT", 30), 0.052, 1.071),
               (("M", "StdTob", 85), 3.1, 1.09))


def _coi_extremes(rates):
    """S's COI scale with :data:`EXTREME_COI`'s keys, every line in reverse key order, so
    that a schedule numbered in file order is another schedule's number."""
    added = [pd.DataFrame({"sex": sex, "rate_class": rate_class, "age_at_entry": age,
                           "policy_year": range(1, 123 - age),
                           "coi_rate_guar": [round(base * ratio ** (y - 1), 6)
                                             for y in range(1, 123 - age)],
                           "provenance": "test copy"})
             for (sex, rate_class, age), base, ratio in EXTREME_COI]
    rates = pd.concat([rates, *added]).sort_values(COI_KEYS, ignore_index=True)
    return rates.iloc[::-1].reset_index(drop=True)


def _younger(column, value):
    """An edit of an age table that adds ages 0 to 17, ``value(age)`` at each."""
    def edit(rates):
        ages = list(range(18))
        young = pd.DataFrame({"age": ages, column: [value(a) for a in ages],
                              "provenance": "test copy"})
        return pd.concat([young, rates], ignore_index=True)
    return edit


# The tables the extremes and the lineup of nine read: the COI copy, and the mortality and
# corridor tables from age 0, each age's value its own.
EXTREME_EDITS = {
    "coi_rates.csv": _coi_extremes,
    "mort_table.csv": _younger("mort_rate", lambda a: round(0.00021 * 1.041 ** a, 6)),
    "corridor_factors.csv": _younger("corridor_factor",
                                     lambda a: round(2.5 + 0.0013 * (18 - a), 6))}

# The frames of the contract's extremes, in _contract_extremes' order, and the COI
# schedule each reads, its keys' place among the copy's four.
EXTREME_FRAMES = [1584, 1464, 564, 1, 1464, 900]
EXTREME_SCHEDULES = [1, 1, 4, 1, 1, 3]


def _contract_extremes():
    """Inputs for the contract's longest frames, its oldest issue age and the bounds of its
    values: a table.

    Six points made from the committed twins.  S's point 3 issued at 0, the youngest age
    the contract issues at, 120 months on, the shipped ``future_horizon_mth``: a frame of
    1,584 months, the longest the contract allows, which reads every cache as far as
    ``spec_sec.py`` sizes it, ``t`` to 1,584 in C4's sweep of the month after it, the
    policy year to 122, the attained age from 0 to 121 and, with the behaviour module on,
    the pricing path to policy month 1,463.  S's point 1 issued at 0 at the valuation date,
    with both pins, withdrawing $60 a month on Option A, each cutting the face.  StdTob
    issued at 85, the oldest age, 120 months on, whose annual mortality passes 1 at
    attained age 113 and is capped.  S's point 3 at 0 in force in its last covered month,
    policy month 1,463: a frame of one row, whose first month reads the pricing path cold
    from issue.  A single premium of $50,000 at 0 without a surrender charge.  And the
    worked example's twin at a premium load of 1, whose pricing path opens every month on
    an account of 0, the denominator of its shares.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    opened = {"sa_pp_init_1": 0.0, "sa_pp_init_2": 0.0, "fa_pp_init": 0.0,
              "la_pp_init": 0.0, "loan_bal_init": 0.0, "sum_assured_init": 0.0}
    rows = pd.concat([
        twin(3, age_at_entry=0, duration_mth=-120),
        twin(1, age_at_entry=0, duration_mth=0, wd_pp=60.0, **opened),
        twin(3, age_at_entry=85, rate_class="StdTob", duration_mth=-120),
        twin(3, age_at_entry=0, duration_mth=1463, policy_count=0.5, sa_pp_init_1=30000.0,
             sa_pp_init_2=20000.0, sum_assured_init=500000.0),
        twin(3, age_at_entry=0, premium_type="SINGLE", premium_pp_ann=50000.0,
             has_surr_charge=False),
        twin(1, load_prem_rate=1.0)])
    rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return rows


# The lineup of nine, subaccount_max, written out of their ids' order, and the shares and
# opening values each point holds of each, by id.
NINE = (3, 1, 9, 2, 7, 5, 8, 4, 6)


def _nine_subaccounts():
    """A lineup of nine and two points that hold every subaccount: a table and edits.

    ``subaccount_table.csv`` holds nine ids, written out of order (:data:`NINE`), each with
    a fund expense of its own; ``scenario_table.csv`` gives each id a path of its own, in
    each scenario, ``WE`` for 13 months and ``LEVEL6`` past ``Data.return_horizon_mth``,
    to month 2,000, beside ``ZFAR``, a scenario no point names of one row a billion months
    on; and two points, S's point 4 in force at 120 and S's point 3 issued 25 months on,
    hold a share of their premiums and, in force, an opening value of their own in each.
    """
    committed = _committed()
    rows = committed.loc[[_label(committed, "twin", 4, 0),
                          _label(committed, "future", 3, -25)]]
    rows = rows.drop(columns=["alloc_1", "alloc_2", "sa_pp_init_1", "sa_pp_init_2"])
    in_force = rows["duration_mth"] > 0
    rows = rows.assign(alloc_fixed=0.1, **{
        f"alloc_{i}": 0.02 * i for i in NINE}, **{
        f"sa_pp_init_{i}": in_force * (1000.0 * i + 37.5) for i in NINE})
    rows.index = pd.Index([1, 2], name="point_id")

    def lineup(table):
        return pd.DataFrame({"subaccount_id": NINE,
                             "subaccount_name": [f"fund {i}" for i in NINE],
                             "fund_expense_ann": [round(0.003 + 0.0007 * i, 6)
                                                  for i in NINE],
                             "provenance": "test copy"})

    def scenarios(_):
        paths = [(scenario, i, t, round(base + 0.0003 * i + step * t * i, 10))
                 for scenario, base, step, last in (("WE", 0.002, 0.00001, 12),
                                                    ("LEVEL6", 0.004, 0.0000007, 2000))
                 for i in NINE for t in range(last + 1)]
        paths += [("ZFAR", i, FAR_MONTH, 0.01) for i in NINE]
        return pd.DataFrame([(*path, "test copy") for path in paths],
                            columns=["scenario_id", "subaccount_id", "t",
                                     "gross_return_mth", "provenance"])

    return rows, {**EXTREME_EDITS, "subaccount_table.csv": lineup,
                  "scenario_table.csv": scenarios}


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest frames and a lineup of nine.

    The six points of :func:`_contract_extremes`, the longest frames the contract allows,
    its oldest issue age and the bounds of its values, read every cache keyed by ``t``,
    ``m``, ``y`` and ``a`` as far as ``spec_sec.py`` sizes it: ``t`` to 1,584, the month
    after the 1,584-month frame, which the roll-forwards read, the pricing month to 1,463,
    the policy year to 122 and the attained age from 0.  They run under
    :data:`EXTREME_REFS`, the behaviour module and inflation on, every premium pattern
    among them, from a COI copy written in reverse key order, with a schedule no point
    reads between two that points read, and mortality and corridor tables from age 0, each
    key with values of its own, so that a compiled read of the key beside the right one,
    which a padded array allows, changes a number the comparison sees.  ``Data``'s
    numbering of the scales, which both engines share, moves both alike, so the comparison
    cannot see it: it is held against the file and ``VUL_US_S`` by
    :func:`test_the_coi_scales_are_numbered_by_key_on_a_file_out_of_key_order`.  Frames
    and schedules are asserted first.

    And the lineup of ``subaccount_max``, nine, written out of its ids' order, each
    subaccount with a fund expense, a share, an opening value and a return path of its own
    (:func:`_nine_subaccounts`), on a point in force and one issued later: every cache
    keyed by a subaccount, and by a subaccount and a timing, is read to its last column.
    Its sums over nine subaccounts are this model's loops, which ``VUL_US_S``'s ``sum``
    would differ from in a last bit, so the comparison is the compiled model's with
    modelx's, which loop alike.  One scenario runs past ``Data.return_horizon_mth`` and
    another starts a billion months on: the return array holds the months a frame reads,
    no more, in both.

    modelx sweeps each point fully, with every code and the pricing path's closes
    (``sec_support._vul_c4_also``), and the compiled model must agree everywhere, every
    raise included.  A cache one too small for the contract raises ``IndexError`` compiled
    where modelx reads on, and fails here, though the spec check passes it, which holds
    the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "extremes", model_points=_contract_extremes(),
                           edits=EXTREME_EDITS)
    model = mx.read_model(folder, name=_name("extremes_frames"))
    try:
        frames = [projection(model, key).proj_len() for key in point_keys(model)]
        schedules = list(model.Data.coi_schedule())
    finally:
        model.close()
    assert frames == EXTREME_FRAMES, frames
    assert schedules == EXTREME_SCHEDULES, schedules
    found = compiled_mismatches(build, folder, refs=EXTREME_REFS, also=_vul_c4_also)
    rows, edits = _nine_subaccounts()
    folder = compiled_case(build, tmp_path / "nine", model_points=rows, edits=edits)
    model = mx.read_model(folder, name=_name("nine"))
    try:
        data = model.Data
        assert list(data.subaccounts()) == list(NINE)
        assert data.gross_return_array().shape == (4, 9, data.return_horizon_mth + 1)
        assert [projection(model, key).subaccount_count() for key in point_keys(model)] == (
            [9, 9])
    finally:
        model.close()
    found += compiled_mismatches(build, folder, refs=EXTREME_REFS, also=_vul_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The point in force near its end that the label cases make refuse, a frame of four
# months, since modelx sweeps a raise in every cell of every month: S's in-force point 4,
# moved to policy month 920.
LATE_MTH = 920


def _labels_not_text():
    """The labels ``Data`` accepts that are not text, as (case, the table's rows, edits).

    Made from the committed twins of S's points 1, 2 and 4: on a point without a charge, a
    blank ``surr_charge_id``, NaN as pandas reads it, beside a point with one, and a row
    with a blank option, test, pattern and sex, which the point's first projection
    refuses, in force in a month near its end, :data:`LATE_MTH`; a blank ``rate_class``,
    which ``Data`` refuses at its class join, on that row alone; an id column of numbers,
    ints, on points without a charge; and ``scenario_id`` written as numbers in both files,
    1 for ``WE`` and 2 for ``LEVEL6``, which pandas reads as ints in both and joins.
    """
    committed = _committed()

    def twin(s_point, **columns):
        return committed.loc[[_label(committed, "twin", s_point, 0)]].assign(**columns)

    def numbered(rows):
        return rows.assign(scenario_id=rows["scenario_id"].map({"WE": 1, "LEVEL6": 2}))

    late = {"duration_mth": LATE_MTH}
    cases = [
        ("blank", pd.concat([twin(1), twin(2, has_surr_charge=False, surr_charge_id=None),
                             twin(4, db_option=None, qual_test=None, premium_type=None,
                                  sex=None, **late)]), None),
        ("blank class", twin(4, rate_class=None, **late), None),
        ("numeric", pd.concat([twin(1, has_surr_charge=False, surr_charge_id=0),
                               twin(2, has_surr_charge=False, surr_charge_id=9)]), None),
        ("numeric scenarios", numbered(pd.concat([twin(1), twin(3)])),
         {"scenario_table.csv": numbered}),
    ]
    for _, rows, _ in cases:
        rows.index = pd.Index(range(1, len(rows) + 1), name="point_id")
    return cases


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: the compiled accessors return what modelx returns.

    ``Data`` accepts a blank ``surr_charge_id`` on a point without a charge, and an id
    column of numbers, since ``VUL_US_S`` never reads such a point's schedule and projects
    it; a ``scenario_id`` written as numbers in both files, which joins as text does; and
    blank options and a blank sex, which the point's first projection refuses, and a blank
    class, which the class join refuses.  modelx returns each label as pandas reads it,
    NaN or an int, and an accessor typed ``str`` would raise ``TypeError`` compiled; the
    sample types the seven as Python objects (sample_sec.py).  So on each case of
    :func:`_labels_not_text`, after checking that the file reads as the case says, modelx
    sweeps every point fully, with every code where no cell raises
    (``sec_support._vul_c4_also``), and the compiled model must agree everywhere, the
    label accessors and every raise included.
    """
    build = sec_build(SEC)
    found = []
    for case, rows, edits in _labels_not_text():
        folder = compiled_case(build, tmp_path / case, model_points=rows, edits=edits)
        model = mx.read_model(folder, name=_name(f"labels_{case.replace(' ', '_')}"))
        try:
            points = [projection(model, key) for key in point_keys(model)]
            labels = {label: [p.cells[label]() for p in points] for label in LABELS}
        finally:
            model.close()
        if case == "blank":
            ids, options = labels["surr_charge_id"], labels["db_option"]
            assert ids[0] == "VUL14" and math.isnan(ids[1]), ids
            assert options[:2] == ["A", "A"] and math.isnan(options[2]), options
            assert math.isnan(labels["sex"][2]), labels["sex"]
        elif case == "blank class":
            assert math.isnan(labels["rate_class"][0]), labels
        elif case == "numeric":
            ids = labels["surr_charge_id"]
            assert ids == [0, 9] and all(isinstance(i, (int, np.integer)) for i in ids), ids
        else:
            ids = labels["scenario_id"]
            assert ids == [1, 2] and all(isinstance(i, (int, np.integer)) for i in ids), ids
        also = _vul_c4_also if case.startswith("numeric") else None
        found += [f"{case}: {line}" for line in compiled_mismatches(build, folder,
                                                                     also=also)]
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 16.0 as 16, as modelx does.

    Every keyed table's key columns, the lineup's and the scenario's among them, written
    as floats, as a spreadsheet can save them (:data:`FLOAT_KEYS`), and the model point
    table's ``duration_mth`` and ``age_at_entry`` too: ``Data`` reads each key by value,
    so every extent, the lineup's ids and the scenario's months are ints, and the edges
    test holds modelx to the shipped tables' numbers.  Here the twins of S's points 1 and
    4 and the row issued 25 months on, which between them read every table, with the
    behaviour module on, are swept in modelx with every code
    (``sec_support._vul_c4_also``), and the compiled model must agree everywhere, every
    ``Data`` array included, in dtype and shape.  First, in seconds, modelx's ``Data`` on
    the floats is held to its ``Data`` on the same rows as written: every array of the
    same dtype, and every extent and count of the same type, so that a key read as a float
    fails here, naming its cell, and not in the compiled sweep, where each typed read of
    a float array would raise and the sweep run out of time.
    """
    build = sec_build(SEC)
    committed = _committed()
    rows = committed.loc[[_label(committed, "twin", 1, 0), _label(committed, "twin", 4, 0),
                          _label(committed, "future", 3, -25)]]
    as_written = _read(_sec_inputs(tmp_path / "ints", rows), "keys_ints")
    rows = rows.assign(duration_mth=rows["duration_mth"].astype(float),
                       age_at_entry=rows["age_at_entry"].astype(float))
    folder = compiled_case(build, tmp_path / "floats", model_points=rows, edits={
        file: _as_floats(columns) for file, columns in FLOAT_KEYS.items()})
    for file, columns in FLOAT_KEYS.items():
        written = pd.read_csv(folder.parent / file)
        assert all(written[c].dtype == float for c in columns), file
    floats = mx.read_model(folder, name=_name("keys_floats"))
    try:
        apart = []
        for name, cell in as_written.Data.cells.items():
            if cell.parameters:
                continue
            want, got = cell(), floats.Data.cells[name]()
            if isinstance(want, np.ndarray):
                if not isinstance(got, np.ndarray) or got.dtype != want.dtype:
                    apart.append(f"{name}: {getattr(got, 'dtype', type(got))}, not "
                                 f"{want.dtype}")
            elif isinstance(want, (int, float, np.integer, np.floating)):
                if type(got) is not type(want):
                    apart.append(f"{name}: {type(got).__name__}, not "
                                 f"{type(want).__name__}")
        assert not apart, apart
    finally:
        floats.close()
        as_written.close()
    found = compiled_mismatches(build, folder, refs={"dyn_behavior_on": True},
                                also=_vul_c4_also)
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


@pytest.mark.cython
def test_the_compiled_model_reads_the_schedule_of_a_point_without_a_charge(sec_build,
                                                                           tmp_path):
    """Compiled, a point without a charge reads its schedule as modelx does, as at E.

    On :data:`UNCHARGED`'s table, beside the copy's SC7 and HUGE, the compiled model's
    ``surr_charge_rate_max()`` and ``surr_charge_runoff_years()`` on each point without a
    charge are bc8ce29's numbers, pinned, of type float, and modelx's, and on the points
    whose id the table lacks, or which have none, each raises ``KeyError``, naming the
    point, with modelx's message; ``Data``'s two joins and ``has_surr_charge_schedule``
    are modelx's arrays, NaN where the id is missing included, and each point's
    ``net_cf(0)`` is modelx's.
    """
    build = sec_build(SEC)
    table = _uncharged()
    edits = {"surr_charge_table.csv": _surr_charges_with_sc7}
    folder = compiled_case(build, tmp_path / "uncharged", model_points=table, edits=edits)
    cells = ("surr_charge_rate_max", "surr_charge_runoff_years", "net_cf")
    data = ("surr_charge_rate_max", "surr_charge_runoff_years", "has_surr_charge_schedule")
    places = {point: list(table.index).index(point) for point, _, _ in UNCHARGED}
    model = _read(folder, "uncharged_cy")
    try:
        want = {idx: [_modelx_did(lambda: model.Projection[idx].cells[cell](
            *((0,) if cell == "net_cf" else ()))) for cell in cells]
            for idx in places.values()}
        want_data = {name: model.Data.cells[name]() for name in data}
    finally:
        model.close()
    job = {"refs": {}, "data": list(data), "calls": {
        idx: [(cell, (0,) if cell == "net_cf" else ()) for cell in cells]
        for idx in places.values()}}
    got = run_compiled(tmp_path / "uncharged", build.package.name, job)
    assert got["exit"] == 0, got["stderr"]
    assert all(got["compiled"].values()), got["compiled"]
    for point, _, pinned in UNCHARGED:
        idx = places[point]
        accessors = (("raised", _NO_ID.format(point)),) * 2 if pinned is None else tuple(
            ("ok", v) for v in pinned)
        have = got["values"][idx]
        assert tuple(want[idx][:2]) == accessors, (point, want[idx])
        assert [(status, type(v), v) for status, v in have[:2]] == [
            (status, type(v), v) for status, v in accessors], (point, have)
        assert have[2][0] == want[idx][2][0] == "ok", (point, have)
        assert _as_modelx(have[2][1], want[idx][2][1]), (point, have, want[idx])
    for name, array in want_data.items():
        status, value = got["data"][name]
        assert status == "ok" and np.array_equal(np.asarray(value), array, equal_nan=True)
        assert np.asarray(value).dtype == array.dtype, name


def _capped_table(tmp_path):
    """The cap test's rows, built by the generator from S under :data:`CAPPED_REFS`.

    The point of :data:`CAPPED`, alone in a copy of S's table on the splice's COI copy:
    its twin, issued at the valuation date; issued 25 months after it; and restated in
    force in the month before the cap first binds, :data:`CAPPED_MTH`, opened with S's
    count and state there.  As the cap test builds them.
    """
    base, changes = CAPPED
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    s = _read(temp_inputs(tmp_path, model_path(TWIN),
                          model_points=s_table.loc[[base]].assign(**changes),
                          edits=CAPPED_EDITS), "capped_s", CAPPED_REFS)
    try:
        spec = dataclasses.replace(SPEC, derived=((base, CAPPED_MTH - 1),),
                                   future=((base, 25),))
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    return table.set_index("point_id")


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1, and where a NaN meets a bound.

    The three rows of the cap's test (:func:`_capped_table`), on whose frames the annual
    rate passes 1 from attained age 113, go beside the build, under :data:`CAPPED_REFS`.
    modelx sweeps them fully, with every code (``sec_support._vul_c4_also``), and the
    compiled model must agree at every argument modelx caches, identically on x86-64 and
    to 1e-12 relative elsewhere.  The extremes reach the side of ``min(q, 1.0)`` that
    returns 1 too, on one point issued later; these reach it on a point issued at the
    valuation date, on one issued later and on one in force when it binds.

    And the committed twins of S's points 1 and 4 under an A/E of NaN, a Reference, which
    the compiled model reads as modelx does, so that a NaN reaches the cap compiled:
    ``min`` keeps its first argument there as in modelx, and C4 holds the compiled NaN to
    modelx's, in every cell it reaches.  The same for the M&E rate, ``me_rate_ann``, on the
    worked example's twin and the row issued 25 months on: a NaN that reaches every
    account and the residuals of the three checks, which modelx and the compiled model
    must fail alike.
    """
    build = sec_build(SEC)
    rows = _capped_table(tmp_path / "s")
    folder = compiled_case(build, tmp_path / "capped", model_points=rows,
                           edits=CAPPED_EDITS)
    found = compiled_mismatches(build, folder, refs=CAPPED_REFS, also=_vul_c4_also)
    committed = _committed()
    for ref, points in (("mort_ae_factor", (("twin", 1, 0), ("twin", 4, 0))),
                        ("me_rate_ann", (("twin", 1, 0), ("future", 3, -25)))):
        twins = committed.loc[[_label(committed, *point) for point in points]]
        folder = compiled_case(build, tmp_path / ref, model_points=twins)
        model = _read(folder, f"nan_{ref}", {ref: float("nan")})
        try:
            for key in point_keys(model):
                p = projection(model, key)
                t = p.t_entry()
                value = p.mort_rate(t) if ref == "mort_ae_factor" else p.me_charge_pp(t)
                assert math.isnan(value), (ref, key)
        finally:
            model.close()
        found += compiled_mismatches(build, folder, refs={ref: float("nan")})
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found)


# The compiled model's own refusals: what it does with a key past the caches spec_sec.py
# sizes, which no projection the contract allows reaches, as (cell, arguments, what modelx
# does).  modelx answers a month after cover with a zero, and runs a month before the
# valuation date of a point in force back through its accounts, the policy being in force
# then, until it reads a return before the scenario's first month, which it refuses; it
# answers a pricing month past the path with a number, and a policy year or an age past
# its table with the table's last row, as the cells say, and refuses a code past the
# timings and the kinds, a subaccount's position past the lineup and a policy year below 1
# by name; compiled, each is past a cache, and raises IndexError rather than read or write
# beyond it.  Every cache after its
# first dimension is nine wide (spec_sec.py), so the first code or position past it is 9.
COMPILED_ONLY = [
    ("net_cf", (1586,), ("ok", 0.0)),
    ("net_cf", (-1,), ("raised", "ValueError: point_id 1: scenario_table.csv has no return "
                                 "for subaccount_id 1 at t -25")),
    ("pols_if_at", (0, 9), ("raised", "ValueError: invalid timing")),
    ("av_at", (0, 9), ("raised", "ValueError: invalid timing")),
    ("claim_pp", (0, 9), ("raised", "ValueError: invalid kind")),
    ("claims_from_av", (0, 9), ("raised", "ValueError: invalid kind")),
    ("sa_pp_at", (0, 9, "BEF_PREM"),
     ("raised", "ValueError: point_id 1: no subaccount at position 9 of the lineup of 2")),
    ("alloc", (9,),
     ("raised", "ValueError: point_id 1: no subaccount at position 9 of the lineup of 2")),
    ("sa_pp", (0, -1),
     ("raised", "ValueError: point_id 1: no subaccount at position -1 of the lineup of 2")),
    ("av_pricing_pp_at", (1465, "BEF_PREM"), ("ok", None)),
    ("prem_persistency_py", (124,), ("ok", None)),
    ("prem_persistency_py", (-1,), ("raised", "ValueError: point_id 1: "
                                    "prem_persistency.csv has no factor for policy year "
                                    "-1")),
    ("coi_rate_guar_at", (124,), ("ok", None)),
    ("corridor_factor_at", (123,), ("ok", None)),
    ("mort_rate_base_at", (123,), ("ok", None)),
]

# The codes inside the timing and kind caches that a cell does not take, since one
# numbering serves every timing family and every cache after its first dimension is nine
# wide (spec_sec.py): there the cell itself refuses the code, compiled as in modelx.  As
# (cell, its arguments, a code by its name or number).
CODES_IN_CACHE = [
    ("pols_if_at", (0, "BEF_PREM")), ("pols_if_at", (0, "EOM")),
    ("av_pp_at", (0, "BEF_NB")), ("av_pp_at", (0, "EOM")), ("av_at", (0, "BEF_MAT")),
    ("sa_pp_at", (0, 0, "EOM")), ("sa_pp_at", (0, 0, "BEF_NB")), ("fa_pp_at", (0, "EOM")),
    ("la_pp_at", (0, "BEF_DECR")), ("loan_bal_pp_at", (0, "EOM")),
    ("unloaned_av_pp_at", (0, "BEF_MAT")), ("sa_pricing_pp_at", (0, 0, "BEF_WD")),
    ("fa_pricing_pp_at", (0, "BEF_ME")), ("av_pricing_pp_at", (0, "EOM")),
    ("claim_pp", (0, "MATURITY")), ("claim_pp", (0, 8)),
    ("claims_from_av", (0, "WITHDRAWAL")), ("claims_from_av", (0, 8)),
    ("sa_pp_at", (0, 2, "BEF_PREM")), ("sa_pp", (0, 8)), ("fund_expense_ann", (8,)),
]


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, the References, [(position, cell, arguments)], the Data cells to read).

    A position, not a label, since a table ``Data`` refuses has no keys to give: each is
    the row's place in the table written, ``Projection``'s ``idx``, which the test indexes
    ``Projection`` by in modelx too.
    """
    committed, extract = _committed(), _extract()

    def at(table, label):
        return list(table.index).index(label)

    moved = _label(committed, "twin", 4, 0)
    cases = [
        *[(f"past its cover, {case}", _set("duration_mth", [moved], month)(committed),
           None, {}, [(at(committed, moved), "proj_len", ())], ())
          for case, month in PAST_COVER],
        ("past its cover, on the extract", _set("duration_mth", [104], 924)(extract),
         None, {}, [(at(extract, 104), "proj_len", ())], ()),
        ("beyond the tables, on the extract", extract, None, {},
         [(0, cell, args) for cell, args, _ in BEYOND if min(args) >= 0], ()),
        ("a point without a COI scale, on the extract",
         _set("age_at_entry", [109], 36)(extract), None, {}, [(0, "result_cf", ())], ()),
        ("an issue age of 86, on the extract", _set("age_at_entry", [103], 86)(extract),
         None, {}, [(at(extract, 103), "proj_len", ())], ()),
        ("a class the table lacks, on the extract",
         _set("rate_class", [103, 106], "SuperPNT")(extract), None, {},
         [(0, "result_cf", ())], ("class_factor",)),
        ("a scenario the table lacks, on the extract",
         _set("scenario_id", [102], "CRASH")(extract), None, {},
         [(0, "result_cf", ())], ("scenario_index",)),
        ("a label written as text, on the extract", _relabelled(107, "7x")(extract),
         None, {}, [(at(extract, 107), "point_id", ())], ("point_id",)),
        ("codes and positions no cell takes, inside the caches", committed, None, {},
         [(0, cell, args) for cell, args in CODES_IN_CACHE], ()),
        ("a return before its path's first month", committed,
         {"scenario_table.csv": _scenarios_unsorted}, {},
         [(0, "gross_return_mth", (2, 1)), (0, "result_cf", ())], ()),
    ]
    for case, table, edits, refs, label, _, _, _ in NOT_ISSUED:
        cases.append((case, table, edits, refs, [(at(table, label), "result_cf", ())], ()))
    for case, edit, runoff, scenarios, cell, _, label in UNJOINED:
        table = edit(committed)
        call = "point_id" if cell == "point_id" else "result_cf"
        cases.append((case, table, _unjoined_edits(runoff, scenarios), {},
                      [(at(table, label), call, ())], (cell,)))
    point = _label(committed, "twin", 2, 0)
    for case, column, value, _ in UNDECODABLE:
        cases.append((case, _set(column, [point], value)(committed), None, {},
                      [(at(committed, point), "result_cf", ())], ()))
    for case, edit, _ in MALFORMED:
        cases.append((case, edit(committed), None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, file, edit, check, _ in MALFORMED_KEYS + MALFORMED_RATES:
        cases.append((case, committed, {file: edit}, {"dyn_behavior_on": True},
                      [(0, "net_cf", (0,))], (check,)))
    return cases


def _modelx_did(call):
    """``("ok", value)`` or ``("raised", "Type: message")``: what modelx did on ``call``."""
    try:
        return ("ok", call())
    except Exception as err:                    # what modelx raised is what compiled must
        return ("raised", _raised(err))


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`): ``proj_len()`` refuses a point past its cover, naming it
    by ``point_id()``, on the committed table (:data:`PAST_COVER`) and on the extract
    labelled otherwise than by position (:func:`_extract`), and a point the contract does
    not issue, which the compiled caches are not sized for (:data:`NOT_ISSUED`, each on
    its own inputs), and on the extract an issue age past ``issue_age_max``; each reader
    of a padded table refuses policy year 0, below it, each reader of a subaccount's input
    a position past the lineup, and a point without a COI scale is refused where its first
    rate is read, on the extract (:data:`BEYOND`; a key below 0 is past the cache, below);
    a return before its path's first month is refused; every case of :data:`UNJOINED`, on
    the extract a class and a scenario the tables lack and a label written as text among
    them, of :data:`UNDECODABLE`, each text variant among them, of :data:`MALFORMED` and of
    :data:`MALFORMED_KEYS` and :data:`MALFORMED_RATES`, is refused by a projection, and by
    the ``Data`` cell that checks it, compiled as in modelx, so a compiled ``Data`` cell
    refuses each value its modelx cell refuses; and a code a cell does not take, or a
    position past the lineup, inside its cache, is refused by the cell
    (:data:`CODES_IN_CACHE`).

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a code past the timing and kind caches, a position
    past the subaccount caches, a pricing month past the ``m`` cache, a policy year past
    the ``y`` cache either side and an age past the ``a`` cache, each raising
    ``IndexError`` compiled, beside what modelx does.

    The cases share one directory, which each case's inputs overwrite in turn, and one
    copy of the compiled package: each child reads its inputs afresh, as the compiled
    ``Data`` reads its files once an import.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    cases.append(("compiled only", _committed(), None, {},
                  [(0, cell, args) for cell, args, _ in COMPILED_ONLY], ()))
    dest = tmp_path / "refused"
    folder = compiled_case(build, dest)
    found, refused, only = [], 0, iter(COMPILED_ONLY)
    for case, table, edits, refs, calls, data in cases:
        temp_inputs(dest, model_path(SEC), model_points=table, model_point_file=TABLE,
                    edits=edits)
        model = mx.read_model(folder, name=_name("refused"))
        try:
            for ref, value in refs.items():
                setattr(model.Projection, ref, value)
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
            status, text = next(have[idx])
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == "compiled only":
                *_, expected = next(only)
                if (expected[1] is None and modelx_did[0] != "ok"
                        or expected[1] is not None and modelx_did != expected):
                    found.append(f"{where}: modelx {modelx_did}, not {expected}")
                if (status, text.split(":")[0]) != ("raised", "IndexError"):
                    found.append(f"{where}: compiled {status} {text!r}, not IndexError")
                continue
            if modelx_did[0] != "raised":
                found.append(f"{where}: modelx returned, where a refusal was meant")
            elif (status, text) != modelx_did:
                found.append(f"{where}: compiled {status} {text!r}, modelx {modelx_did}")
            refused += 1
        for name, modelx_did in want_data.items():
            if modelx_did[0] != "raised":
                found.append(f"{case}: Data.{name}: modelx returned, where a refusal was "
                             f"meant")
            elif got["data"][name] != modelx_did:
                found.append(f"{case}: Data.{name}: compiled {got['data'][name]}, modelx "
                             f"{modelx_did}")
            refused += 1
    assert not found, "\n".join(found)
    assert refused == sum(len(calls) + len(data) for *_, calls, data in cases[:-1])


# The cold call the stack test makes compiled, in a thread whose stack is reserved at each
# of these sizes in KiB, and then on the main thread.  1 MiB is the size asserted; the
# others bracket what the call needs, and the test reports the smallest that ran.
STACK_KIB = (256, 384, 512, 768, 1024, 1536, 2048)

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_frame_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the two points of :func:`_longest_cover`, S's point 3 at issue age 0, issued now
    and 120 months on, whose cover runs 1,464 months, a cold ``net_cf`` in the last month,
    with the behaviour module on, runs the funding ratio's pricing path from the policy
    month of the last month back to issue, 1,463 months, and the cells above and below it
    deep, 1,484 in modelx on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), and compiled it
    runs on the C stack, which the interpreter's recursion limit does not count.  1 MiB
    is the stack MSVC gives an executable's main thread unless the executable asks for
    more: a host that embeds Python, where python.exe itself asks for 2,000,000 bytes.  A
    thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``sec_support.exact_here``) and to 1e-12 elsewhere.
    With gcc the calls need between 256 and 384 KiB, about 240 bytes a level, the least
    margin under 1 MiB of the family's models: at the 325 to 433 bytes a level MSVC took
    on WholeLife's chain, they would need 470 to 630 KiB.  A stack too small kills the
    child, and the test fails naming the stack.  The thread's stack is read back too, from
    Windows or from glibc, and must be at most 1 MiB and a page: a stand-in larger than
    asked for would stand for nothing.  And the calls run again on the child's main
    thread, which is what ``run_sec.py --cython`` runs on.

    No run has measured what the calls need with MSVC.  So they run first at each size of
    :data:`STACK_KIB`, before anything is asserted, and every size's outcome goes into a
    warning, which the job's summary shows, and into the failure, if there is one: the
    smallest size that ran bounds the stack the chain needs on the compiler at hand.  A
    size below the need kills its child on a stack overflow, by design: with gcc, 256 KiB
    does.  Each bracketing child is waited for :data:`BRACKET_TIMEOUT` seconds and the two
    asserted runs :data:`ASSERTED_TIMEOUT`, so that an overflow that hangs, rather than
    ends its child, costs minutes, not the job's hour, and a bracketing size that timed
    out is recorded as such.
    """
    build = sec_build(SEC)
    longest, labels = _longest_cover(tmp_path / "copy")
    rows = pd.read_csv(longest.parent / TABLE, index_col="point_id")
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows, edits={
        file: _copied(longest.parent, file)
        for file in ("coi_rates.csv", "mort_table.csv", "corridor_factors.csv")})
    on = {"dyn_behavior_on": True}
    model = _read(folder, "longest", on)
    try:
        calls, want = {}, {}
        for key, label in zip(point_keys(model), labels):
            proj = projection(model, key)
            last = proj.proj_len() - 1
            assert proj.duration_mth(last) == 12 * 122 - 1, label
            calls[key] = [("net_cf", (last,))]
            want[key] = proj.net_cf(last)
    finally:
        model.close()
    job = {"refs": on, "calls": calls}

    def child(timeout, **where):
        try:
            return run_compiled(tmp_path / "extremes", build.package.name, job,
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
    record = (f"the compiled cold net_cf at the longest cover ran on a thread of "
              f"{ran or 'no size'} KiB and not of "
              f"{[kib for kib in STACK_KIB if kib not in ran]} KiB"
              f"{f', timed out at {late} KiB' if late else ''}; on the main thread "
              f"{'it ran' if runs['the main thread']['exit'] == 0 else 'it failed'}")
    warnings.warn(record, UserWarning)
    for where in ("a 1024 KiB thread", "the main thread"):
        got = runs[where]
        assert got["exit"] == 0, (
            f"the compiled model's deepest cold call failed on {where}, exit code "
            f"{got['exit']} ({record}):\n{got['stderr']}")
        assert all(got["compiled"].values()), got["compiled"]
        for key, value in want.items():
            assert got["values"][key][0][0] == "ok", (where, got["values"][key])
            have = got["values"][key][0][1]
            assert _as_modelx(have, value), (where, have, value)
        reserved = got["stack"]["reserved"]
        if where == "a 1024 KiB thread" and reserved is not None:
            assert reserved <= (1 << 20) + 4096, (
                f"the thread has {reserved} bytes of stack, not 1 MiB")


@pytest.mark.cython
def test_past_a_lapse_rate_of_1_the_compiled_checks_fail(sec_build, tmp_path):
    """Past a lapse rate of 1 the compiled checks return ``False``, where modelx raises.

    ``VUL_US_S``'s lapse rate has no cap, and this model keeps it so: under a spike of
    :data:`LAPSE_SHOCK` S's point 3's annual rate is 1.2 in its cliff month,
    :data:`SHOCK_MTH`, where ``1 - (1 - q)^(1/12)`` has no real value.  modelx computes
    it complex and every check raises ``TypeError``
    (:func:`test_a_lapse_rate_past_1_makes_each_check_raise_as_in_vul_us_s`).  Compiled,
    the power is C's ``pow`` of a negative base, NaN, and NaN runs through every count and
    residual after it, so each check's ``abs(residual) <= tolerance`` is false: the
    compiled model reports a failed check rather than an error.  This pins that
    behaviour, which ``model-sec.md`` records among what the compiled model does
    differently, on the twin of S's point 3: the rate itself is 1.2, its monthly rate
    NaN, and the three checks ``False``.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "lapse")
    committed = _committed()
    idx = list(committed.index).index(_label(committed, "twin", 3, 0))
    model = _read(folder, "lapse_past_1", {"lapse_shock_mult": LAPSE_SHOCK})
    try:
        assert projection(model, idx).lapse_rate(SHOCK_MTH) == 1.2
        assert type(projection(model, idx).lapse_rate_mth(SHOCK_MTH)) is complex
    finally:
        model.close()
    checks = ("check_av_roll_fwd", "check_margin", "check_net_view")
    job = {"refs": {"lapse_shock_mult": LAPSE_SHOCK},
           "calls": {idx: [("lapse_rate", (SHOCK_MTH,)), ("lapse_rate_mth", (SHOCK_MTH,)),
                           *((check, ()) for check in checks)]}}
    got = run_compiled(folder.parent, build.package.name, job)
    assert got["exit"] == 0, got["stderr"]
    assert all(got["compiled"].values()), got["compiled"]
    (rate, monthly, *verdicts) = got["values"][idx]
    assert rate == ("ok", 1.2), rate
    assert monthly[0] == "ok" and math.isnan(monthly[1]), monthly
    assert verdicts == [("ok", False)] * 3, verdicts


# A compiled model's Reference set after it has computed, in a child of its own: what the
# base Projection, an ItemSpace made before the change and one made after give for
# expenses(12), before expense_maint is set to 90.0 and after.
STALE_CHILD = """\\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[3]
values = [p.expenses(12), early.expenses(12)]
p.expense_maint = 90.0
values += [p.expenses(12), early.expenses(12), p[5].expenses(12)]
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
    imported.  This holds the compiled model to what they say, on ``expense_maint``, which
    moves ``expenses(12)`` on every point in force then (VUL ships ``inflation_rate`` at 0,
    which would move nothing): the base ``Projection``, the worked example's twin at
    ``idx`` 0, S's in-force point 4's twin, made before, and S's point 4 restated six
    months on, made after, so that a modelx-cython that began to clear caches would be
    seen here, and the advice changed with it.  A compiled value meets modelx's as C4
    holds it (:func:`_as_modelx`), and one the compiled model kept, its own value of
    before, identically.
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
        before = (p.expenses(12), projection(model, 3).expenses(12))
        p.expense_maint = 90.0
        fresh = (p.expenses(12), projection(model, 3).expenses(12),
                 projection(model, 5).expenses(12))
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
    modelx's: point 6's description, S's in-force point 4 restated six months on, with its
    loan, and its first twelve rows of cash flows, of the account value roll-forward and
    of counts, and the block's lines for each point, its first twelve rows and its first
    twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("6",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "6", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
